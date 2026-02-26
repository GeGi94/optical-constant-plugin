from nomad.config.models.plugins import NormalizerEntryPoint


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