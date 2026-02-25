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
                "label": "Optical constants (dataset)",
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "n",
                        "x": "#wavelength",
                        "y": "#n",
                        "line": {"width": 2},
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "k",
                        "x": "#wavelength",
                        "y": "#k",
                        "yaxis": "y2",
                        "line": {"width": 2},
                    },
                ],
                "layout": {
                    "title": {"text": "n and k vs wavelength", "x": 0.02, "xanchor": "left"},
                    "font": {"size": 16},
                    "hovermode": "x unified",
                    "margin": {"l": 70, "r": 70, "t": 60, "b": 60},
                    "legend": {
                        "orientation": "h",
                        "x": 0.02,
                        "y": 1.12,
                        "xanchor": "left",
                    },
                    "xaxis": {
                        "title": {"text": "Wavelength (nm)"},
                        "showgrid": True,
                        "zeroline": False,
                        "ticks": "outside",
                    },
                    "yaxis": {
                        "title": {"text": "Refractive index n"},
                        "showgrid": True,
                        "zeroline": False,
                        "ticks": "outside",
                    },
                    "yaxis2": {
                        "title": {"text": "Extinction coefficient k"},
                        "overlaying": "y",
                        "side": "right",
                        "showgrid": False,
                        "zeroline": False,
                        "ticks": "outside",
                    },
                },
                "open": False,
            }
        ],
    )

    source_doi = Quantity(type=str, description="DOI of the source, if from literature.")
    source_name = Quantity(type=str, description="Source label if DOI is unknown.")
    method = Quantity(type=str, description="How n,k were obtained (ellipsometry, literature, ...)")
    temperature = Quantity(type=float, unit="K", description="Measurement temperature (optional).")
    bandgap = Quantity(type=float, unit="eV", description="Bandgap Eg associated with this dataset (optional).")

    # unit="nm" rimosso per evitare conversioni/scala errate (es. 400 -> 40000)
    wavelength = Quantity(type=float, shape=["*"], description="Wavelength axis (nm).")
    n = Quantity(type=float, shape=["*"], description="Refractive index n(λ).")
    k = Quantity(type=float, shape=["*"], description="Extinction coefficient k(λ).")


class OpticalConstantsEntry(PlotSection, EntryData):
    m_def = Section(
        label="OpticalConstantsEntry",
        a_plotly_graph_object=[
            {
                "label": "Optical constants (main)",
                "data": [
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "n",
                        "x": "#wavelength_plot",
                        "y": "#n_plot",
                        "line": {"width": 2},
                    },
                    {
                        "type": "scatter",
                        "mode": "lines",
                        "name": "k",
                        "x": "#wavelength_plot",
                        "y": "#k_plot",
                        "yaxis": "y2",
                        "line": {"width": 2},
                    },
                ],
                "layout": {
                    "title": {"text": "n and k vs wavelength", "x": 0.02, "xanchor": "left"},
                    "font": {"size": 16},
                    "hovermode": "x unified",
                    "margin": {"l": 70, "r": 70, "t": 60, "b": 60},
                    "legend": {
                        "orientation": "h",
                        "x": 0.02,
                        "y": 1.12,
                        "xanchor": "left",
                    },
                    "xaxis": {
                        "title": {"text": "Wavelength (nm)"},
                        "showgrid": True,
                        "zeroline": False,
                        "ticks": "outside",
                    },
                    "yaxis": {
                        "title": {"text": "Refractive index n"},
                        "showgrid": True,
                        "zeroline": False,
                        "ticks": "outside",
                    },
                    "yaxis2": {
                        "title": {"text": "Extinction coefficient k"},
                        "overlaying": "y",
                        "side": "right",
                        "showgrid": False,
                        "zeroline": False,
                        "ticks": "outside",
                    },
                },
                "open": True,
            }
        ],
    )

    material = Quantity(type=str, description="Material name (e.g., ITO, ZnO, C60).")
    has_nk_any = Quantity(type=bool)

    # Copiati dal primo dataset valido per mostrare un plot in overview
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