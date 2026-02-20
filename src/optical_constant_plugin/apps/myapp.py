from nomad.config.models.plugins import AppEntryPoint
from nomad.config.models.ui import App

optical_app = AppEntryPoint(
    name="optical_app",
    description="Stub app for optical constants.",
    app=App(
        label="Optical constants",
        path="optical-constants",
        category="Materials",
        description="Stub UI for optical constants."
    ),
)