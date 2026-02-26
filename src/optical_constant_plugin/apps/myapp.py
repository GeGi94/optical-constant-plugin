from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import (
    App,
    Column,
    Menu,
    MenuItemTerms,
    SearchQuantities,
    Dashboard,
    WidgetTerms,
    WidgetScatterPlot,
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
                q("n_400nm"), q("k_400nm"),
                q("n_700nm"), q("k_700nm"),
                q("n_800nm"), q("k_800nm"),
                q("n_900nm"), q("k_900nm"),
                q("n_1200nm"), q("k_1200nm"),
            ]
        ),
        filters_locked={
            "section_defs.definition_qualified_name": [schema_def]
        },
        columns=[
            Column(quantity="entry_name", selected=True),
            Column(quantity=q("material"), label="Material", selected=True),
            Column(quantity=q("reference"), label="Reference", selected=True),
            Column(quantity="upload_create_time"),
        ],
        menu=Menu(
            size="sm",
            items=[
                MenuItemTerms(search_quantity=q("material"), options=30),
                MenuItemTerms(search_quantity=q("reference"), options=30),
            ],
        ),
        dashboard=Dashboard(
            widgets=[
                WidgetTerms(
                    title="Material",
                    search_quantity=q("material"),
                    showinput=True,
                    scale="linear",
                    size=200,
                    layout={"lg": Layout(h=7, w=4, x=0, y=0, minH=6, minW=3)},
                ),
                WidgetScatterPlot(
                    title="n vs k @ 400 nm",
                    x=q("n_400nm"),
                    y=q("k_400nm"),
                    size=2000,
                    layout={"lg": Layout(h=7, w=4, x=4, y=0, minH=6, minW=3)},
                ),
                WidgetScatterPlot(
                    title="n vs k @ 700 nm",
                    x=q("n_700nm"),
                    y=q("k_700nm"),
                    size=2000,
                    layout={"lg": Layout(h=7, w=4, x=8, y=0, minH=6, minW=3)},
                ),
                WidgetScatterPlot(
                    title="n vs k @ 800 nm",
                    x=q("n_800nm"),
                    y=q("k_800nm"),
                    size=2000,
                    layout={"lg": Layout(h=7, w=4, x=0, y=7, minH=6, minW=3)},
                ),
                WidgetScatterPlot(
                    title="n vs k @ 900 nm",
                    x=q("n_900nm"),
                    y=q("k_900nm"),
                    size=2000,
                    layout={"lg": Layout(h=7, w=4, x=4, y=7, minH=6, minW=3)},
                ),
                WidgetScatterPlot(
                    title="n vs k @ 1200 nm",
                    x=q("n_1200nm"),
                    y=q("k_1200nm"),
                    size=2000,
                    layout={"lg": Layout(h=7, w=4, x=8, y=7, minH=6, minW=3)},
                ),
            ]
        ),
    ),
)