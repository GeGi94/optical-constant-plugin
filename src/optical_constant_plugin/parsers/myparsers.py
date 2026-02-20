from nomad.config.models.plugins import ParserEntryPoint

def optical_parser(mainfile, archive, logger=None, **kwargs):
    raise RuntimeError(
        f"Optical parser not implemented yet (stub). mainfile={mainfile}"
    )

class OpticalParserEntryPoint(ParserEntryPoint):
    name: str = "optical_parser"
    description: str = "Stub parser for optical constants."

    def load(self):
        # Ritorna un callable compatibile con la chiamata del framework
        return optical_parser

optical_parser = OpticalParserEntryPoint()