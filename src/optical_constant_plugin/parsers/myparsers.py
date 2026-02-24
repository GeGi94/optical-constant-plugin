from nomad.config.models.plugins import ParserEntryPoint


class OpticalParserEntryPoint(ParserEntryPoint):
    name: str = "optical_parser"
    description: str = "Minimal parser for optical constants (wavelength[nm], n, k)."

    def load(self):
        from nomad.parsing.parser import Parser
        import numpy as np
        import os

        class OpticalParser(Parser):

            # Firma compatibile con tutte le versioni recenti NOMAD
            def is_mainfile(self, filename, *args, **kwargs):
                if not filename:
                    return False
                return filename.lower().endswith(".txt")

            def parse(self, mainfile, archive, logger):

                # Importa le classi dal tuo schema package
                from optical_constant_plugin.schema_packages.mypackage import (
                    OpticalConstantsEntry,
                    OpticalDataset,
                )

                # Materiale = nome file (senza estensione)
                material_name = os.path.splitext(
                    os.path.basename(mainfile)
                )[0]

                data = []

                with open(mainfile, "r", encoding="utf-8", errors="ignore") as f:
                    for line in f:
                        line = line.strip()

                        # ignora commenti e righe vuote
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
                    raise ValueError(
                        f"No valid wavelength n k data found in {mainfile}"
                    )

                arr = np.array(data, dtype=float)

                # Crea entry
                entry = OpticalConstantsEntry()
                entry.material = material_name

                dataset = OpticalDataset()
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