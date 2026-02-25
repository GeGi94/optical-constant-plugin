from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuItemTerms,
    SearchQuantities,
    Dashboard,
    WidgetTerms,
    Layout,
)

schema_def = "optical_constant_plugin.schema_packages.mypackage.OpticalConstantsEntry"

optical_app = AppEntryPoint(
    name="optical_app",
    description="Explore optical properties (n,k datasets) by material.",
    app=App(
        label="Optical properties",
        path="optical-properties",
        category="Materials",
        description="Browse optical n,k datasets and filter by material.",

        # rende disponibili in Explore le quantità scalari del tuo schema
        search_quantities=SearchQuantities(
            include=[
                f"data.material#{schema_def}",
                f"data.has_nk_any#{schema_def}",
            ]
        ),

        # limita i risultati alle entry che sono del tuo tipo
        filters_locked={
            "section_defs.definition_qualified_name": [schema_def]
        },

        # tabella risultati
        columns=[
            Column(quantity="entry_name", selected=True),
            Column(quantity=f"data.material#{schema_def}", label="Material", selected=True),
            Column(quantity=f"data.has_nk_any#{schema_def}", label="Has n,k (any)", selected=True),
            Column(quantity="upload_create_time"),
        ],

        # filtro a sinistra (facoltativo)
        menu=Menu(
            size="sm",
            items=[
                MenuItemTerms(search_quantity=f"data.material#{schema_def}", options=15),
            ],
        ),

        # ✅ widget centrale tipo “Transport Layers” (terms con barre e conteggi)
        dashboard=Dashboard(
            widgets=[
                WidgetTerms(
                    title="Material",
                    search_quantity=f"data.material#{schema_def}",
                    showinput=True,
                    scale="linear",
                    size=200,
                    layout={"lg": Layout(h=9, w=12, x=0, y=0, minH=6, minW=6)},
                )
            ]
        ),
    ),
)