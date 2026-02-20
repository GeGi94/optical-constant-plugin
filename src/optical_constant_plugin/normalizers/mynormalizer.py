from nomad.config.models.plugins import NormalizerEntryPoint

class OpticalNormalizerEntryPoint(NormalizerEntryPoint):
    name: str = "optical_normalizer"
    description: str = "Stub normalizer for optical constants."

    def load(self):
        # Import LAZY per evitare circular import durante config.load_plugins()
        from nomad.normalizing.normalizer import Normalizer

        class OpticalNormalizer(Normalizer):
            def normalize(self, archive, logger):
                # Stub: non fa nulla
                return

        return OpticalNormalizer()

optical_normalizer = OpticalNormalizerEntryPoint()