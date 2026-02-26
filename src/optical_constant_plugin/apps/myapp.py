from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Column,
    SearchQuantities,
    Dashboard,
    WidgetTerms,
    Layout,
)

schema_def = "optical_constant_plugin.schema_packages.mypackage.OpticalConstantsEntry"

def q(name: str) -> str:
    return f"data.{name}#{schema_def}"

optical_app = AppEntryPoint(
    name="optical_app",
    description="Explore optical properties (n,k datasets) by material.",
    app=App(
        label="Optical properties",
        path="optical-properties",
        category="Materials",
        description="Browse optical n,k datasets and filter by material.",

        search_quantities=SearchQuantities(
            include=[
                q("material"),
                q("reference"),
            ]
        ),

        filters_locked={
            "section_defs.definition_qualified_name": [schema_def]
        },

        # niente filtri a sinistra
        menu=None,

        # widget centrale "tabella/lista" dei materiali
        dashboard=Dashboard(
            widgets=[
                WidgetTerms(
                    title="Materials",
                    search_quantity=q("material"),
                    # layout: in alto, a tutta larghezza (12 colonne)
                    layout={
                        "lg": Layout(x=0, y=0, w=12, h=6, minH=4),
                    },
                ),
            ]
        ),

        columns=[
            Column(quantity="entry_name", selected=True),
            Column(quantity=q("material"), label="Material", selected=True),
            Column(quantity=q("reference"), label="Reference", selected=True),
            Column(quantity="upload_create_time"),
        ],
    ),
)