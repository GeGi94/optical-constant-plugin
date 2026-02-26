from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuItemTerms,
    SearchQuantities,
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

        # only scalars you want in Explore
        search_quantities=SearchQuantities(
            include=[
                q("material"),
                q("reference"),
            ]
        ),

        # only your schema entries
        filters_locked={
            "section_defs.definition_qualified_name": [schema_def]
        },

        # results table
        columns=[
            Column(quantity="entry_name", selected=True),
            Column(quantity=q("material"), label="Material", selected=True),
            Column(quantity=q("reference"), label="Reference", selected=True),
            Column(quantity="upload_create_time"),
        ],

        # left filters
        menu=Menu(
            size="sm",
            items=[
                MenuItemTerms(search_quantity=q("material"), options=30),
                MenuItemTerms(search_quantity=q("reference"), options=30),
            ],
        ),

        # IMPORTANT: no dashboard here -> no plots in Explorer
        dashboard=None,
    ),
)