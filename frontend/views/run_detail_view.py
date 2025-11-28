from textual.screen import Screen
from textual.widgets import Static, Button
from textual.containers import Vertical, Horizontal
from rich.console import Group
from rich.table import Table
from ..api import get
from ..utils.rich_helpers import pretty_kv_table

class RunDetailView(Screen):
    BINDINGS = [("b", "back", "Back")]

    def __init__(self, run_id: str = None):
        super().__init__()
        self.run_id = run_id

    def compose(self):
        self.header = Static("")
        self.body = Static("")
        yield Vertical(self.header, self.body)

    def on_mount(self):
        if not self.run_id:
            self.header.update("[red]No run id provided[/red]")
            return
        try:
            run = get(f"/runs/{self.run_id}")
        except Exception as e:
            self.header.update(f"[red]Failed to fetch run: {e}[/red]")
            return

        self.header.update(f"[bold]Run {self.run_id}[/bold]")
        group = []

        # summary table
        summary = pretty_kv_table({
            "experiment_name": run.get("experiment_name"),
            "start": run.get("timestamp_start"),
            "end": run.get("timestamp_end"),
            "tags": ", ".join(run.get("tags", []) or [])
        })
        group.append(summary)

        # parameters
        if run.get("parameters"):
            group.append(pretty_kv_table(run.get("parameters"), title="Parameters"))

        # metrics
        if run.get("metrics"):
            group.append(pretty_kv_table(run.get("metrics"), title="Metrics"))

        # dataset/code/env/artifacts
        for key in ("dataset", "code", "environment", "artifacts"):
            if run.get(key):
                group.append(pretty_kv_table(run.get(key), title=key))

        self.body.update(Group(*group))

    async def action_back(self):
        await self.app.pop_screen()
