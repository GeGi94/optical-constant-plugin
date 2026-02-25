from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import App, Column, Menu, MenuItemTerms, SearchQuantities

# qualified name della tua sezione Entry (serve per bloccare i risultati a "solo le tue entry")
schema_def = "optical_constant_plugin.schema_packages.mypackage.OpticalConstantsEntry"

optical_app = AppEntryPoint(
    name="optical_app",
    description="Explore optical properties (n,k datasets) by material.",
    app=App(
        label="Optical properties",          # <--- rinomina qui
        path="optical-properties",           # (puoi lasciarlo optical-constants se preferisci)
        category="Materials",
        description="Browse optical n,k datasets and filter by material.",

        # rende disponibili in Explore le quantità scalari del tuo schema
        search_quantities=SearchQuantities(
            include=[
                f"data.material#{schema_def}",
                f"data.has_nk_any#{schema_def}",
            ]
        ),

        # mostra una tabella con almeno la colonna material
        columns=[
            Column(quantity="entry_name", selected=True),
            Column(quantity=f"data.material#{schema_def}", label="Material", selected=True),
            Column(quantity=f"data.has_nk_any#{schema_def}", label="Has n,k (any)", selected=True),
            Column(quantity="upload_create_time"),
        ],

        # filtro a sinistra: elenco dei materiali (terms facet)
        menu=Menu(
            size="sm",
            items=[
                MenuItemTerms(
                    search_quantity=f"data.material#{schema_def}",
                    options=15,   # quanti materiali mostrare prima di "show more"
                ),
                MenuItemTerms(
                    search_quantity=f"data.has_nk_any#{schema_def}",
                    options=2,
                ),
            ],
        ),

        # limita i risultati alle entry che sono del tuo tipo
        filters_locked={
            "section_defs.definition_qualified_name": [schema_def]
        },
    ),
)