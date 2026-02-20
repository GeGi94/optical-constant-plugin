from nomad.config.models.plugins import ParserEntryPoint

class OpticalParserEntryPoint(ParserEntryPoint):
    name: str = "optical_parser"
    description: str = "Stub parser for optical constants."

    def load(self):
        # lazy import per evitare problemi di bootstrap
        from nomad.parsing.parser import Parser

        class OpticalParser(Parser):
            # REQUIRED: metodo astratto
            def is_mainfile(self, filename: str, mime_type: str | None = None, buffer=None) -> bool:
                # Per ora: non matcha nulla (stub "inerte" che non prende file)
                return False

            # REQUIRED/expected
            def parse(self, mainfile, archive, logger):
                raise RuntimeError(
                    f"Optical parser not implemented yet (stub). mainfile={mainfile}"
                )

        return OpticalParser()

optical_parser = OpticalParserEntryPoint()