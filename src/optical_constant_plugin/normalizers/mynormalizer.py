from nomad.config.models.plugins import NormalizerEntryPoint
from nomad.normalizing.normalizer import Normalizer


class OpticalNormalizer(Normalizer):
    def normalize(self, archive, logger):
        # Stub: non fa nulla
        return


class OpticalNormalizerEntryPoint(NormalizerEntryPoint):
    name: str = "optical_normalizer"
    description: str = "Stub normalizer for optical constants."

    def load(self):
        # DEVE ritornare un'istanza di Normalizer
        return OpticalNormalizer()


optical_normalizer = OpticalNormalizerEntryPoint()