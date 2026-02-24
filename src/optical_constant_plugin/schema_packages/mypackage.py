from nomad.metainfo import SchemaPackage, MSection, Quantity, Section, SubSection
from nomad.datamodel.data import EntryData
from nomad.config.models.plugins import SchemaPackageEntryPoint


m_package = SchemaPackage()

class OpticalDataset(MSection):
    m_def = Section(label="OpticalDataset")

    source_doi = Quantity(type=str, description="DOI of the source, if from literature.")
    source_name = Quantity(type=str, description="Source label if DOI is unknown.")

    bandgap = Quantity(
        type=float,
        unit="eV",
        description="Bandgap Eg associated with this dataset (optional).",
    )

    wavelength = Quantity(type=float, shape=["*"], unit="nm", description="Wavelength axis.")
    n = Quantity(type=float, shape=["*"], description="Refractive index n(λ).")
    k = Quantity(type=float, shape=["*"], description="Extinction coefficient k(λ).")


class OpticalConstantsEntry(EntryData):
    m_def = Section(label="OpticalConstantsEntry")

    material = Quantity(type=str, description="Material name (e.g., ITO, ZnO, C60).")
    datasets = SubSection(section_def=OpticalDataset, repeats=True)

m_package.__init_metainfo__()

class TestSchema(SchemaPackageEntryPoint):
    name: str = "optical_schema"
    description: str = "Stub schema package for optical constants."

    def load(self):
        return m_package

optical_schema = TestSchema()