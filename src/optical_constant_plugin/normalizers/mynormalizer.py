from nomad.config.models.plugins import NormalizerEntryPoint


# =========================
# OPTICAL NORMALIZER (UNCHANGED)
# =========================

class OpticalNormalizerEntryPoint(NormalizerEntryPoint):
    name: str = "optical_normalizer"
    description: str = "Populate main plot arrays, reference, and fixed-wavelength n/k points."

    def load(self):
        from nomad.normalizing.normalizer import Normalizer
        import numpy as np

        class OpticalNormalizer(Normalizer):
            def normalize(self, archive, logger):
                data = getattr(archive, "data", None)
                if data is None:
                    return

                # defaults for main plot
                if hasattr(data, "wavelength_plot"):
                    data.wavelength_plot = []
                if hasattr(data, "n_plot"):
                    data.n_plot = []
                if hasattr(data, "k_plot"):
                    data.k_plot = []

                # defaults for reference (string)
                if hasattr(data, "reference"):
                    data.reference = None

                # defaults for fixed points (floats)
                targets = [400.0, 700.0, 800.0, 900.0, 1200.0]
                for t in targets:
                    if hasattr(data, f"n_{int(t)}nm"):
                        setattr(data, f"n_{int(t)}nm", None)
                    if hasattr(data, f"k_{int(t)}nm"):
                        setattr(data, f"k_{int(t)}nm", None)

                datasets = getattr(data, "datasets", None)
                if not datasets:
                    return

                def interp_safe(x, y, x0):
                    x = np.asarray(x, dtype=float)
                    y = np.asarray(y, dtype=float)
                    m = np.isfinite(x) & np.isfinite(y)
                    x = x[m]
                    y = y[m]
                    if x.size < 2:
                        return None
                    idx = np.argsort(x)
                    x = x[idx]
                    y = y[idx]
                    if x0 < x[0] or x0 > x[-1]:
                        return None
                    return float(np.interp(x0, x, y))

                for ds in datasets:
                    wl = getattr(ds, "wavelength", None)
                    n = getattr(ds, "n", None)
                    k = getattr(ds, "k", None)

                    valid = (
                        wl is not None and n is not None and k is not None
                        and len(wl) > 0
                        and len(n) == len(wl)
                        and len(k) == len(wl)
                    )
                    if not valid:
                        continue

                    # main plot
                    data.wavelength_plot = list(wl)
                    data.n_plot = list(n)
                    data.k_plot = list(k)

                    # reference (DOI preferred, else source_name)
                    if hasattr(data, "reference"):
                        ref = getattr(ds, "source_doi", None) or getattr(ds, "source_name", None)
                        data.reference = ref

                    # fixed-wavelength points for Explore scatter plots
                    for t in targets:
                        nval = interp_safe(wl, n, t)
                        kval = interp_safe(wl, k, t)
                        if hasattr(data, f"n_{int(t)}nm"):
                            setattr(data, f"n_{int(t)}nm", nval)
                        if hasattr(data, f"k_{int(t)}nm"):
                            setattr(data, f"k_{int(t)}nm", kval)

                    logger.info(
                        "Populated main plot arrays + reference + fixed n/k points",
                        n_points=len(wl),
                    )
                    break

        return OpticalNormalizer()


optical_normalizer = OpticalNormalizerEntryPoint()


# =========================
# ELECTRICAL NORMALIZER (NEW)
# =========================

class ElectricalNormalizerEntryPoint(NormalizerEntryPoint):
    name: str = "electrical_normalizer"
    description: str = "Derive chi from Ec (or Ev+Eg), derive Nc/Nv@300K from mdos; promote scalars to entry."

    def load(self):
        from nomad.normalizing.normalizer import Normalizer
        import numpy as np

        def ok(v):
            return v is not None and np.isfinite(v)

        def dos_3d_cm3(mdos_rel, T=300.0):
            """
            3D effective DOS (Nc or Nv) in cm^-3 at temperature T,
            using DOS effective mass mdos_rel in units of electron mass m0.
            """
            kB = 1.380649e-23
            h = 6.62607015e-34
            m0 = 9.1093837015e-31
            mdos = float(mdos_rel) * m0
            N_m3 = 2.0 * ((2.0 * np.pi * mdos * kB * T) / (h ** 2)) ** 1.5
            return float(N_m3 / 1e6)  # cm^-3

        def derive_chi(Ec=None, Ev=None, Eg=None):
            """
            Vacuum-referenced energies (eV).
            chi (electron affinity) = -Ec.
            If Ec missing but Ev and Eg available -> Ec = Ev + Eg, then chi = -(Ev+Eg).
            """
            if ok(Ec):
                return float(-Ec), True
            if ok(Ev) and ok(Eg):
                Ec2 = float(Ev + Eg)
                return float(-Ec2), True
            return None, False

        class ElectricalNormalizer(Normalizer):
            def normalize(self, archive, logger):
                data = getattr(archive, "data", None)
                if data is None:
                    return

                # only act on ElectricalConstantsEntry-like objects
                if not hasattr(data, "datasets"):
                    return
                if not hasattr(data, "material"):
                    return

                datasets = getattr(data, "datasets", None) or []
                if not datasets:
                    return

                # defaults promoted scalars
                if hasattr(data, "reference"):
                    data.reference = None
                data.Eg = None
                data.chi = None
                data.mu_e = None
                data.mu_h = None
                data.Nc_300K = None
                data.Nv_300K = None
                data.eps_r = None

                for ds in datasets:
                    # set reference
                    if hasattr(data, "reference"):
                        data.reference = getattr(ds, "source_doi", None) or getattr(ds, "source_name", None)

                    Eg = getattr(ds, "bandgap", None)
                    Ec = getattr(ds, "Ec", None)
                    Ev = getattr(ds, "Ev", None)

                    # chi: prefer explicit, else derive
                    chi = getattr(ds, "electron_affinity", None)
                    if not ok(chi):
                        chi_val, derived = derive_chi(Ec=Ec, Ev=Ev, Eg=Eg)
                        if chi_val is not None:
                            ds.electron_affinity = chi_val
                            ds.chi_derived = True
                            chi = chi_val
                        else:
                            ds.chi_derived = False
                    else:
                        ds.chi_derived = False

                    # Nc/Nv: prefer explicit, else derive from mdos
                    Nc = getattr(ds, "Nc", None)
                    if not ok(Nc):
                        mdos_e = getattr(ds, "mdos_e", None)
                        if ok(mdos_e):
                            try:
                                ds.Nc = dos_3d_cm3(mdos_e, T=300.0)
                                ds.Nc_derived = True
                                Nc = ds.Nc
                            except Exception:
                                ds.Nc_derived = False
                        else:
                            ds.Nc_derived = False
                    else:
                        ds.Nc_derived = False

                    Nv = getattr(ds, "Nv", None)
                    if not ok(Nv):
                        mdos_h = getattr(ds, "mdos_h", None)
                        if ok(mdos_h):
                            try:
                                ds.Nv = dos_3d_cm3(mdos_h, T=300.0)
                                ds.Nv_derived = True
                                Nv = ds.Nv
                            except Exception:
                                ds.Nv_derived = False
                        else:
                            ds.Nv_derived = False
                    else:
                        ds.Nv_derived = False

                    # Promote scalars to entry (first dataset only, MVP)
                    data.Eg = Eg
                    data.chi = chi
                    data.mu_e = getattr(ds, "mobility_e", None)
                    data.mu_h = getattr(ds, "mobility_h", None)
                    data.Nc_300K = Nc
                    data.Nv_300K = Nv
                    data.eps_r = getattr(ds, "relative_permittivity", None)

                    logger.info(
                        "Electrical normalized/promoted",
                        material=getattr(data, "material", None),
                    )
                    break

        return ElectricalNormalizer()


electrical_normalizer = ElectricalNormalizerEntryPoint()