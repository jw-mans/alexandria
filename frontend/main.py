from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer
from textual import work
from .views.runs_view import RunsView
from .views.run_detail_view import RunDetailView
from .views.diff_view import DiffView
from .views.datasets_view import DatasetsView

class Frontend(App):
    CSS = """
    Screen { background: #0b1220; color: white; }
    #layout { height: 1fr; }
    """
    TITLE = "Alexandria"
    SUB_TITLE = "Experiment Lineage Browser"
    LOG = "textual.log"

    SCREENS = {
        "runs": RunsView,
        "diff": DiffView,
        "datasets": DatasetsView,
        # run_detail must be dynamically created with run_id => we register a factory
    }

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

    async def on_mount(self):
        # push runs screen first
        await self.push_screen("runs")

    async def push_screen(self, screen, **kwargs):
        """
        Override to support pushing RunDetailView with run_id param.
        Accepts either screen name (str) or Screen instance.
        """
        if isinstance(screen, str) and screen == "run_detail":
            run_id = kwargs.get("run_id")
            if not run_id:
                return
            scr = RunDetailView(run_id=run_id)
            await super().push_screen(scr)
        else:
            await super().push_screen(screen if isinstance(screen, Screen) else screen)

if __name__ == "__main__":
    Frontend().run()
