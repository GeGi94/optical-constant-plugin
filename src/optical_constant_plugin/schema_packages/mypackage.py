from nomad.metainfo import SchemaPackage, MSection, Quantity, Section, SubSection
from nomad.datamodel.data import EntryData
from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.datamodel.metainfo.plot import PlotSection

m_package = SchemaPackage()

class OpticalDataset(PlotSection, MSection):
    m_def = Section(
        label="OpticalDataset",
        a_plotly_graph_object=[
            {
                "label": "n,k vs wavelength",
                "data": [
                    {"type": "scatter", "mode": "lines", "name": "n", "x": "#wavelength", "y": "#n"},
                    {"type": "scatter", "mode": "lines", "name": "k", "x": "#wavelength", "y": "#k"},
                ],
                "layout": {
                    "xaxis": {"title": {"text": "Wavelength (nm)"}},
                    "yaxis": {"title": {"text": "Value"}},
                },
                "open": True,
            }
        ],
    )

    source_doi = Quantity(type=str, description="DOI of the source, if from literature.")
    source_name = Quantity(type=str, description="Source label if DOI is unknown.")
    method = Quantity(type=str, description="How n,k were obtained (ellipsometry, literature, ...)")
    temperature = Quantity(type=float, unit="K", description="Measurement temperature (optional).")
    bandgap = Quantity(type=float, unit="eV", description="Bandgap Eg associated with this dataset (optional).")

    wavelength = Quantity(type=float, shape=["*"], unit="nm", description="Wavelength axis.")
    n = Quantity(type=float, shape=["*"], description="Refractive index n(λ).")
    k = Quantity(type=float, shape=["*"], description="Extinction coefficient k(λ).")

class OpticalConstantsEntry(EntryData):
    m_def = Section(label="OpticalConstantsEntry")

    material = Quantity(type=str, description="Material name (e.g., ITO, ZnO, C60).")
    has_nk_any = Quantity(type=bool)

    datasets = SubSection(section_def=OpticalDataset, repeats=True)

m_package.__init_metainfo__()

class TestSchema(SchemaPackageEntryPoint):
    name: str = "optical_schema"
    description: str = "Stub schema package for optical constants."

    def load(self):
        return m_package

optical_schema = TestSchema()