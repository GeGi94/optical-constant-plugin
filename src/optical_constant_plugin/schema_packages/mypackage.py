from nomad.metainfo import SchemaPackage, MSection, Quantity, Section, SubSection
from nomad.datamodel.data import EntryData
from nomad.config.models.plugins import SchemaPackageEntryPoint

m_package = SchemaPackage()


class OpticalDataset(MSection):
    m_def = Section(label="OpticalDataset")

    source_doi = Quantity(type=str, description="DOI of the source, if from literature.")
    source_name = Quantity(type=str, description="Source label if DOI is unknown.")
    method = Quantity(type=str, description="How n,k were obtained (ellipsometry, literature, ...)")
    temperature = Quantity(type=float, unit="K", description="Measurement temperature (optional).")
    bandgap = Quantity(type=float, unit="eV", description="Bandgap Eg associated with this dataset (optional).")

    # NOTE: unit="nm" rimosso per evitare conversioni/scala errate (es. 400 -> 40000)
    wavelength = Quantity(type=float, shape=["*"], description="Wavelength axis (nm).")
    n = Quantity(type=float, shape=["*"], description="Refractive index n(λ).")
    k = Quantity(type=float, shape=["*"], description="Extinction coefficient k(λ).")


class OpticalConstantsEntry(EntryData):
    m_def = Section(
        label="OpticalConstantsEntry",
        a_plotly_graph_object=[
            {
                "label": "n,k vs wavelength",
                "data": [
                    {"type": "scatter", "mode": "lines", "name": "n", "x": "#wavelength_plot", "y": "#n_plot"},
                    {"type": "scatter", "mode": "lines", "name": "k", "x": "#wavelength_plot", "y": "#k_plot"},
                ],
                "layout": {
                    "xaxis": {"title": {"text": "Wavelength (nm)"}},
                    "yaxis": {"title": {"text": "Value"}},
                },
                "open": True,
            }
        ],
    )

    material = Quantity(type=str, description="Material name (e.g., ITO, ZnO, C60).")

    # True if at least one dataset provides valid n and k arrays
    has_nk_any = Quantity(type=bool)

    # Arrays usati SOLO per mostrare il plot nella pagina principale (copiati dal primo dataset valido)
    wavelength_plot = Quantity(type=float, shape=["*"], description="Wavelength for main plot (nm).")
    n_plot = Quantity(type=float, shape=["*"], description="n for main plot.")
    k_plot = Quantity(type=float, shape=["*"], description="k for main plot.")

    datasets = SubSection(section_def=OpticalDataset, repeats=True)


m_package.__init_metainfo__()


class TestSchema(SchemaPackageEntryPoint):
    name: str = "optical_schema"
    description: str = "Schema package for optical constants."

    def load(self):
        return m_package


optical_schema = TestSchema()