from nomad.config.models.plugins import NormalizerEntryPoint

class OpticalNormalizerEntryPoint(NormalizerEntryPoint):
    name: str = "optical_normalizer"
    description: str = "Stub normalizer for optical constants."

    def load(self):
        # Deve restituire un normalizer callable/oggetto.
        # Stub: non fa nulla.
        def _stub_normalizer(*args, **kwargs):
            return
        return _stub_normalizer

optical_normalizer = OpticalNormalizerEntryPoint()