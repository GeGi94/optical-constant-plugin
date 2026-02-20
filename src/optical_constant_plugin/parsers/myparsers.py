from nomad.config.models.plugins import ParserEntryPoint

class OpticalParserEntryPoint(ParserEntryPoint):
    name: str = "optical_parser"
    description: str = "Stub parser for optical constants."

    def load(self):
        # Import lazy per evitare problemi di bootstrap
        from nomad.parsing.parser import Parser

        class OpticalParser(Parser):
            def parse(self, mainfile, archive, logger):
                raise RuntimeError(
                    f"Optical parser not implemented yet (stub). mainfile={mainfile}"
                )

        return OpticalParser()

optical_parser = OpticalParserEntryPoint()