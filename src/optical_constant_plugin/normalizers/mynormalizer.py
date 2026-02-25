from nomad.config.models.plugins import NormalizerEntryPoint

class OpticalNormalizerEntryPoint(NormalizerEntryPoint):
    name: str = "optical_normalizer"
    description: str = "Compute has_nk_any for optical constants."

    def load(self):
        from nomad.normalizing.normalizer import Normalizer

        class OpticalNormalizer(Normalizer):
            def normalize(self, archive, logger):
                data = getattr(archive, "data", None)
                if data is None or not hasattr(data, "has_nk_any"):
                    return

                datasets = getattr(data, "datasets", None)
                if not datasets:
                    data.has_nk_any = False
                    return

                has_any = False
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
                        has_any = True
                        break

                data.has_nk_any = bool(has_any)
                logger.info("Computed has_nk_any", has_nk_any=data.has_nk_any)

        return OpticalNormalizer()

optical_normalizer = OpticalNormalizerEntryPoint()