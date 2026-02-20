from nomad.config.models.plugins import ParserEntryPoint

class OpticalParserEntryPoint(ParserEntryPoint):
    name: str = "optical_parser"
    description: str = "Stub parser for optical constants."

    def load(self):
        # Ritorna un callable/parser; per ora stub.
        def _stub_parser(*args, **kwargs):
            raise NotImplementedError(
                "Optical parser stub: implement file parsing later."
            )
        return _stub_parser

optical_parser = OpticalParserEntryPoint()