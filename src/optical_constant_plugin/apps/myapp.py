from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Column,
    SearchQuantities,
    Dashboard,
    WidgetTerms,
    Layout,
    Menu,
    MenuItemTerms,
    MenuItemHistogram,
)


# =========================
# OPTICAL APP (UNCHANGED)
# =========================

schema_def_opt = "optical_constant_plugin.schema_packages.mypackage.OpticalConstantsEntry"

def qopt(name: str) -> str:
    return f"data.{name}#{schema_def_opt}"

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
                qopt("material"),
                qopt("reference"),
            ]
        ),

        filters_locked={
            "section_defs.definition_qualified_name": [schema_def_opt]
        },

        # niente filtri a sinistra
        menu=None,

        # widget centrale "tabella/lista" dei materiali
        dashboard=Dashboard(
            widgets=[
                WidgetTerms(
                    title="Materials",
                    search_quantity=qopt("material"),
                    layout={"lg": Layout(x=0, y=0, w=12, h=6, minH=4)},
                ),
            ]
        ),

        columns=[
            Column(quantity="entry_name", selected=True),
            Column(quantity=qopt("material"), label="Material", selected=True),
            Column(quantity=qopt("reference"), label="Reference", selected=True),
            Column(quantity="upload_create_time"),
        ],
    ),
)


# =========================
# ELECTRICAL APP (NEW)
# =========================

schema_def_el = "optical_constant_plugin.schema_packages.mypackage.ElectricalConstantsEntry"

def qel(name: str) -> str:
    return f"data.{name}#{schema_def_el}"

electrical_app = AppEntryPoint(
    name="electrical_app",
    description="Explore electrical properties (Eg, chi, mobilities, Nc/Nv, eps_r) by material.",
    app=App(
        label="Electrical properties",
        path="electrical-properties",
        category="Materials",
        description="Browse electrical datasets (.dat/.csv) and filter by material.",

        search_quantities=SearchQuantities(
            include=[
                qel("material"),
                qel("reference"),
                qel("Eg"),
                qel("chi"),
                qel("mu_e"),
                qel("mu_h"),
                qel("Nc_300K"),
                qel("Nv_300K"),
                qel("eps_r"),
            ]
        ),

        filters_locked={
            "section_defs.definition_qualified_name": [schema_def_el]
        },

        menu=Menu(
            size="sm",
            items=[
                MenuItemTerms(search_quantity=qel("material"), options=50),
                MenuItemHistogram(search_quantity=qel("Eg")),
                MenuItemHistogram(search_quantity=qel("chi")),
                MenuItemHistogram(search_quantity=qel("eps_r")),
            ],
        ),

        dashboard=Dashboard(
            widgets=[
                WidgetTerms(
                    title="Materials",
                    search_quantity=qel("material"),
                    layout={"lg": Layout(x=0, y=0, w=12, h=6, minH=4)},
                ),
            ]
        ),

        columns=[
            Column(quantity="entry_name", selected=True),
            Column(quantity=qel("material"), label="Material", selected=True),
            Column(quantity=qel("reference"), label="Reference", selected=False),
            Column(quantity=qel("Eg"), label="Eg (eV)", selected=True),
            Column(quantity=qel("chi"), label="χ (eV)", selected=True),
            Column(quantity=qel("mu_e"), label="μe (cm²/Vs)", selected=True),
            Column(quantity=qel("mu_h"), label="μh (cm²/Vs)", selected=True),
            Column(quantity=qel("Nc_300K"), label="Nc (cm⁻³)", selected=False),
            Column(quantity=qel("Nv_300K"), label="Nv (cm⁻³)", selected=False),
            Column(quantity=qel("eps_r"), label="εr", selected=True),
            Column(quantity="upload_create_time"),
        ],
    ),
)


# =========================
# MATERIALS APP (NEW, GROUPING VIA FILTERS)
# =========================
# Nota: per NOMAD le quantities sono schema-specific, quindi qui mettiamo due Terms separati
# (ottico ed elettrico) ma nella stessa pagina.

materials_app = AppEntryPoint(
    name="materials_app",
    description="Browse optical + electrical entries and group them by material via filters.",
    app=App(
        label="Materials (all)",
        path="materials",
        category="Materials",
        description="Unified view: filter by material to see optical and electrical entries together.",

        search_quantities=SearchQuantities(
            include=[
                # optical
                qopt("material"),
                qopt("reference"),
                # electrical
                qel("material"),
                qel("Eg"),
                qel("chi"),
                qel("eps_r"),
            ]
        ),

        # lock to BOTH entry types
        filters_locked={
            "section_defs.definition_qualified_name": [schema_def_opt, schema_def_el]
        },

        menu=Menu(
            size="sm",
            items=[
                # Two material filters (one per schema)
                MenuItemTerms(search_quantity=qopt("material"), options=50),
                MenuItemTerms(search_quantity=qel("material"), options=50),
                MenuItemHistogram(search_quantity=qel("Eg")),
                MenuItemHistogram(search_quantity=qel("chi")),
            ],
        ),

        dashboard=Dashboard(
            widgets=[
                WidgetTerms(
                    title="Optical materials",
                    search_quantity=qopt("material"),
                    layout={"lg": Layout(x=0, y=0, w=6, h=6, minH=4)},
                ),
                WidgetTerms(
                    title="Electrical materials",
                    search_quantity=qel("material"),
                    layout={"lg": Layout(x=6, y=0, w=6, h=6, minH=4)},
                ),
            ]
        ),

        columns=[
            Column(quantity="entry_name", selected=True),
            # show both (one will be empty depending on schema)
            Column(quantity=qopt("material"), label="Material (opt)", selected=True),
            Column(quantity=qel("material"), label="Material (el)", selected=True),
            Column(quantity=qel("Eg"), label="Eg (eV)", selected=False),
            Column(quantity=qel("chi"), label="χ (eV)", selected=False),
            Column(quantity="upload_create_time", selected=True),
        ],
    ),
)