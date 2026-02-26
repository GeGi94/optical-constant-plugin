from nomad.config.models.plugins import ParserEntryPoint


# =========================
# OPTICAL PARSER (UNCHANGED)
# =========================

class OpticalParserEntryPoint(ParserEntryPoint):
    name: str = "optical_parser"
    description: str = "Minimal parser for optical constants (wavelength[nm], n, k)."

    def load(self):
        from nomad.parsing.parser import Parser
        import numpy as np
        import os

        class OpticalParser(Parser):
            def is_mainfile(self, filename, *args, **kwargs):
                if not filename:
                    return False
                fn = filename.lower()
                return fn.endswith(".txt") or fn.endswith(".nk")

            def parse(self, mainfile, archive, logger):
                from optical_constant_plugin.schema_packages.mypackage import (
                    OpticalConstantsEntry,
                    OpticalDataset,
                )

                base = os.path.splitext(os.path.basename(mainfile))[0]
                material_name = base.split("_", 1)[0]

                data = []
                with open(mainfile, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue

                        parts = line.split()
                        if len(parts) < 3:
                            continue

                        try:
                            wl = float(parts[0])
                            n = float(parts[1])
                            k = float(parts[2])
                            data.append((wl, n, k))
                        except ValueError:
                            continue

                if not data:
                    raise ValueError(f"No valid wavelength n k data found in {mainfile}")

                arr = np.array(data, dtype=float)
                arr = arr[np.argsort(arr[:, 0])]

                entry = OpticalConstantsEntry()
                entry.material = material_name

                dataset = OpticalDataset()
                dataset.source_name = base
                dataset.wavelength = arr[:, 0]
                dataset.n = arr[:, 1]
                dataset.k = arr[:, 2]

                entry.datasets = [dataset]
                archive.data = entry

                logger.info(
                    "Optical constants parsed successfully",
                    material=material_name,
                    n_points=len(arr),
                )

        return OpticalParser()


optical_parser = OpticalParserEntryPoint()


# =========================
# ELECTRICAL PARSER (NEW)
# =========================

class ElectricalParserEntryPoint(ParserEntryPoint):
    name: str = "electrical_parser"
    description: str = "Parser for electrical properties: TiberCAD .dat or standard .csv."

    def load(self):
        from nomad.parsing.parser import Parser
        import os
        import re
        import csv

        def ffloat(x):
            if x is None:
                return None
            if isinstance(x, (int, float)):
                return float(x)
            s = str(x).strip()
            if s == "":
                return None
            try:
                return float(s)
            except Exception:
                return None

        def parse_tibercad_dat(path):
            """
            Minimal extraction from TiberCAD .dat:
              [bandgap] Eg_G
              [valenceband] E_v (-> Ev)
              [conductionband] E_c (if present) (-> Ec)
              [permittivity] permittivity (scalar or tuple -> average)
              [mobility/constant] mu_max (mu_e, mu_h)
              [conductionband] m_dos -> mdos_e
              [valenceband]   m_dos -> mdos_h
            """
            section = None
            out = {
                "Eg": None, "Ec": None, "Ev": None,
                "eps_r": None,
                "mu_e": None, "mu_h": None,
                "mdos_e": None, "mdos_h": None,
            }

            re_section = re.compile(r"^\s*\[(.+?)\]\s*$")
            re_kv = re.compile(r"^\s*([A-Za-z0-9_]+)\s*=\s*(.+?)\s*$")
            re_tuple = re.compile(r"^\(\s*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*,\s*([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)\s*\)\s*$")

            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    m = re_section.match(line)
                    if m:
                        section = m.group(1).strip().lower()
                        continue

                    m = re_kv.match(line)
                    if not m:
                        continue

                    key = m.group(1).strip()
                    val = m.group(2).split("#", 1)[0].strip()

                    if section == "bandgap" and key == "Eg_G":
                        out["Eg"] = ffloat(val)

                    if section == "valenceband" and key in ("E_v", "Ev"):
                        out["Ev"] = ffloat(val)

                    if section == "conductionband" and key in ("E_c", "Ec", "E_c0"):
                        out["Ec"] = ffloat(val)

                    if section == "permittivity" and key == "permittivity":
                        mt = re_tuple.match(val)
                        if mt:
                            a = ffloat(mt.group(1))
                            b = ffloat(mt.group(2))
                            if a is not None and b is not None:
                                out["eps_r"] = 0.5 * (a + b)
                        else:
                            out["eps_r"] = ffloat(val)

                    if section == "mobility/constant" and key == "mu_max":
                        mt = re_tuple.match(val)
                        if mt:
                            out["mu_e"] = ffloat(mt.group(1))
                            out["mu_h"] = ffloat(mt.group(2))

                    if section == "conductionband" and key == "m_dos":
                        out["mdos_e"] = ffloat(val)

                    if section == "valenceband" and key == "m_dos":
                        out["mdos_h"] = ffloat(val)

            if all(v is None for v in out.values()):
                return None
            return out

        def parse_electrical_csv(path):
            """
            Standard CSV headers (one row is enough):
              Eg_eV, chi_eV, mobility_e_cm2_Vs, mobility_h_cm2_Vs,
              Nc_cm-3, Nv_cm-3, eps_r
            Optional helpers:
              Ec_eV, Ev_eV, mdos_e, mdos_h
            """
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            if not rows:
                return None

            def first(col):
                for r in rows:
                    v = r.get(col)
                    if v is None:
                        continue
                    if str(v).strip() == "":
                        continue
                    return v
                return None

            out = {
                "Eg": ffloat(first("Eg_eV")),
                "chi": ffloat(first("chi_eV")),
                "mu_e": ffloat(first("mobility_e_cm2_Vs")),
                "mu_h": ffloat(first("mobility_h_cm2_Vs")),
                "Nc": ffloat(first("Nc_cm-3")),
                "Nv": ffloat(first("Nv_cm-3")),
                "eps_r": ffloat(first("eps_r")),
                "Ec": ffloat(first("Ec_eV")),
                "Ev": ffloat(first("Ev_eV")),
                "mdos_e": ffloat(first("mdos_e")),
                "mdos_h": ffloat(first("mdos_h")),
            }

            if all(out[k] is None for k in out):
                return None
            return out

        class ElectricalParser(Parser):
            def is_mainfile(self, filename, *args, **kwargs):
                if not filename:
                    return False
                fn = filename.lower()
                return fn.endswith(".dat") or fn.endswith(".csv")

            def parse(self, mainfile, archive, logger):
                from optical_constant_plugin.schema_packages.mypackage import (
                    ElectricalConstantsEntry,
                    ElectricalDataset,
                )

                base = os.path.splitext(os.path.basename(mainfile))[0]
                material_name = base.split("_", 1)[0]

                low = mainfile.lower()
                entry = ElectricalConstantsEntry()
                entry.material = material_name

                ds = ElectricalDataset()
                ds.source_name = base
                ds.temperature = 300.0

                if low.endswith(".dat"):
                    d = parse_tibercad_dat(mainfile)
                    if not d:
                        raise ValueError(f"No recognized electrical fields in {mainfile}")
                    ds.method = "TiberCAD"
                    ds.bandgap = d.get("Eg")
                    ds.Ec = d.get("Ec")
                    ds.Ev = d.get("Ev")
                    ds.relative_permittivity = d.get("eps_r")
                    ds.mobility_e = d.get("mu_e")
                    ds.mobility_h = d.get("mu_h")
                    ds.mdos_e = d.get("mdos_e")
                    ds.mdos_h = d.get("mdos_h")

                elif low.endswith(".csv"):
                    d = parse_electrical_csv(mainfile)
                    if not d:
                        raise ValueError(f"No recognized electrical CSV fields in {mainfile}")
                    ds.method = "CSV"
                    ds.bandgap = d.get("Eg")
                    ds.electron_affinity = d.get("chi")
                    ds.mobility_e = d.get("mu_e")
                    ds.mobility_h = d.get("mu_h")
                    ds.Nc = d.get("Nc")
                    ds.Nv = d.get("Nv")
                    ds.relative_permittivity = d.get("eps_r")
                    ds.Ec = d.get("Ec")
                    ds.Ev = d.get("Ev")
                    ds.mdos_e = d.get("mdos_e")
                    ds.mdos_h = d.get("mdos_h")
                else:
                    raise ValueError(f"Unsupported mainfile: {mainfile}")

                entry.datasets = [ds]
                archive.data = entry

                logger.info(
                    "Electrical properties parsed successfully",
                    material=material_name,
                    method=ds.method,
                )

        return ElectricalParser()


electrical_parser = ElectricalParserEntryPoint()