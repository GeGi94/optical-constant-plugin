from nomad.metainfo import SchemaPackage, MSection, Quantity, Section, SubSection
from nomad.datamodel.data import EntryData
from nomad.config.models.plugins import SchemaPackageEntryPoint
from nomad.datamodel.metainfo.plot import PlotSection

m_package = SchemaPackage()


# =========================
# OPTICAL (UNCHANGED)
# =========================

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

    # unit="nm" removed to avoid wrong scaling conversions
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
    reference = Quantity(type=str, description="Reference for the optical constants (DOI if available, otherwise source name).")

    n_400nm = Quantity(type=float, description="n at 400 nm (interpolated).")
    k_400nm = Quantity(type=float, description="k at 400 nm (interpolated).")
    n_700nm = Quantity(type=float, description="n at 700 nm (interpolated).")
    k_700nm = Quantity(type=float, description="k at 700 nm (interpolated).")
    n_800nm = Quantity(type=float, description="n at 800 nm (interpolated).")
    k_800nm = Quantity(type=float, description="k at 800 nm (interpolated).")
    n_900nm = Quantity(type=float, description="n at 900 nm (interpolated).")
    k_900nm = Quantity(type=float, description="k at 900 nm (interpolated).")
    n_1200nm = Quantity(type=float, description="n at 1200 nm (interpolated).")
    k_1200nm = Quantity(type=float, description="k at 1200 nm (interpolated).")

    wavelength_plot = Quantity(type=float, shape=["*"], description="Wavelength for main plot (nm).")
    n_plot = Quantity(type=float, shape=["*"], description="n for main plot.")
    k_plot = Quantity(type=float, shape=["*"], description="k for main plot.")

    datasets = SubSection(section_def=OpticalDataset, repeats=True)


# =========================
# ELECTRICAL (NEW)
# =========================

class ElectricalDataset(MSection):
    """
    Minimal electrical dataset for DD simulations (reference at 300 K).
    Required fields you requested:
      Eg [eV], chi [eV], mu_e/mu_h [cm^2/V/s], Nc/Nv [cm^-3], eps_r [-]
    Optional helpers:
      Ec/Ev (vacuum-referenced, eV), mdos_e/mdos_h (unitless, m0) to derive chi, Nc/Nv.
    """
    m_def = Section(label="ElectricalDataset")

    source_doi = Quantity(type=str, description="DOI of the source, if from literature.")
    source_name = Quantity(type=str, description="Source label if DOI is unknown.")
    method = Quantity(type=str, description="How values were obtained (TiberCAD, Hall, literature, ...)")
    temperature = Quantity(type=float, unit="K", description="Reference temperature for this dataset (default 300 K).")

    bandgap = Quantity(type=float, unit="eV", description="Eg [eV]")
    electron_affinity = Quantity(type=float, unit="eV", description="chi (electron affinity) [eV]")

    mobility_e = Quantity(type=float, unit="cm^2/(V*s)", description="electron mobility [cm^2/V/s]")
    mobility_h = Quantity(type=float, unit="cm^2/(V*s)", description="hole mobility [cm^2/V/s]")

    Nc = Quantity(type=float, unit="1/cm^3", description="CB effective DOS at 300 K [cm^-3]")
    Nv = Quantity(type=float, unit="1/cm^3", description="VB effective DOS at 300 K [cm^-3]")

    relative_permittivity = Quantity(type=float, description="static dielectric constant eps_r [-]")

    # Optional band edges (vacuum referenced, eV). If Ec present -> chi = -Ec
    Ec = Quantity(type=float, unit="eV", description="Conduction band edge vs vacuum (optional).")
    Ev = Quantity(type=float, unit="eV", description="Valence band edge vs vacuum (optional).")

    # Optional DOS masses (unitless, in units of m0) used to derive Nc/Nv@300K if Nc/Nv missing
    mdos_e = Quantity(type=float, description="DOS mass electrons (m0 units), optional.")
    mdos_h = Quantity(type=float, description="DOS mass holes (m0 units), optional.")

    chi_derived = Quantity(type=bool)
    Nc_derived = Quantity(type=bool)
    Nv_derived = Quantity(type=bool)


class ElectricalConstantsEntry(EntryData):
    """
    One entry per electrical dataset (.dat or .csv).
    """
    m_def = Section(label="ElectricalConstantsEntry")

    material = Quantity(type=str, description="Material name (e.g., ITO, ZnO, C60).")
    reference = Quantity(type=str, description="Reference for the electrical properties (DOI or source label).")

    # Promoted scalars for Explore filters/columns
    Eg = Quantity(type=float, unit="eV")
    chi = Quantity(type=float, unit="eV")
    mu_e = Quantity(type=float, unit="cm^2/(V*s)")
    mu_h = Quantity(type=float, unit="cm^2/(V*s)")
    Nc_300K = Quantity(type=float, unit="1/cm^3")
    Nv_300K = Quantity(type=float, unit="1/cm^3")
    eps_r = Quantity(type=float)

    datasets = SubSection(section_def=ElectricalDataset, repeats=True)


m_package.__init_metainfo__()


class TestSchema(SchemaPackageEntryPoint):
    name: str = "optical_schema"
    description: str = "Schema package for optical constants."

    def load(self):
        return m_package


optical_schema = TestSchema()