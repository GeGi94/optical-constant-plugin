from nomad.metainfo import SchemaPackage, MSection, Quantity, Section
from nomad.config.models.plugins import SchemaPackageEntryPoint

m_package = SchemaPackage()

class TestSection(MSection):
    m_def = Section(label="TestSection")
    name = Quantity(type=str, description="A simple test quantity.")

m_package.__init_metainfo__()

class TestSchema(SchemaPackageEntryPoint):
    name: str = "optical_schema"
    description: str = "Stub schema package for optical constants."

    def load(self):
        return m_package

optical_schema = TestSchema()