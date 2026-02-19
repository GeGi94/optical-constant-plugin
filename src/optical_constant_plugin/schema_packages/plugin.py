from nomad.metainfo import SchemaPackage, MSection, Quantity, Section
from nomad.config.models.plugins import SchemaPackageEntryPoint  # <-- questa è la chiave

m_package = SchemaPackage()


class TestSection(MSection):
    m_def = Section(label="TestSection")
    name = Quantity(type=str, description="A simple test quantity.")


# registra le sezioni nel package
m_package.__init_metainfo__()

class TestSchema(SchemaPackageEntryPoint):
    name: str = "test_schema"
    description: str = "Minimal test schema package for verifying plugin loading."

    def load(self):
        return m_package



test_schema = TestSchema()
