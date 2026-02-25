from nomad.config.models.plugins import NormalizerEntryPoint


class OpticalNormalizerEntryPoint(NormalizerEntryPoint):
    name: str = "optical_normalizer"
    description: str = "Compute has_nk_any and populate main plot arrays."

    def load(self):
        from nomad.normalizing.normalizer import Normalizer

        class OpticalNormalizer(Normalizer):
            def normalize(self, archive, logger):
                data = getattr(archive, "data", None)
                if data is None:
                    return

                # init default
                if hasattr(data, "has_nk_any"):
                    data.has_nk_any = False
                if hasattr(data, "wavelength_plot"):
                    data.wavelength_plot = []
                if hasattr(data, "n_plot"):
                    data.n_plot = []
                if hasattr(data, "k_plot"):
                    data.k_plot = []

                datasets = getattr(data, "datasets", None)
                if not datasets:
                    return

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
                    if valid:
                        data.has_nk_any = True
                        data.wavelength_plot = list(wl)
                        data.n_plot = list(n)
                        data.k_plot = list(k)
                        logger.info("Populated main plot arrays", n_points=len(wl))
                        break

        return OpticalNormalizer()


optical_normalizer = OpticalNormalizerEntryPoint()