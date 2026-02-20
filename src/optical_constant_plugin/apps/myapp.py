from nomad.config.models.plugins import AppEntryPoint

class OpticalAppEntryPoint(AppEntryPoint):
    name: str = "optical_app"
    description: str = "Stub app for optical constants."

    def load(self):
        # Stub: nessuna UI custom ancora.
        # Restituiamo un dict vuoto per non rompere la discovery.
        return {}

optical_app = OpticalAppEntryPoint()