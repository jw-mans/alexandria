from textual import events
from textual.app import ComposeResult
from textual.widgets import DataTable, Static
from textual.screen import Screen
from textual.containers import Vertical, Horizontal

from ..api import get
from ..components.run_card import run_summary_panel


class RunsView(Screen):
    """Main list-of-runs screen."""

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("d", "diff", "Diff View"),
        ("r", "reload", "Reload Runs"),
    ]

    def compose(self) -> ComposeResult:
        self.table = DataTable(zebra_stripes=True)
        self.table.cursor_type = "row"
        self.details = Static("")

        yield Horizontal(
            Vertical(self.table, id="left"),
            Vertical(self.details, id="right"),
            id="layout",
        )

    def on_mount(self):
        self.load_runs()
        self.set_focus(self.table)

    def load_runs(self):
        try:
            runs = get("/runs")
        except Exception as ex:
            self.details.update(f"[red]Failed to fetch runs: {ex}[/red]")
            return

        self.table.clear(columns=True)
        self.table.add_columns("ID", "Experiment", "Start", "End")

        for r in runs:
            run_id = r.get("id")
            self.table.add_row(
                run_id,
                r.get("experiment_name"),
                r.get("timestamp_start") or "",
                r.get("timestamp_end") or "",
                key=run_id,
            )

    def get_run_id(self, row_key):
        """Extracts run_id safely from a DataTable row_key."""
        table = self.table

        try:
            row_index = table.get_row_index(row_key)
            row = table.get_row(row_index)
            return row[0] 
        except Exception:
            return None

    async def on_data_table_row_selected(
        self, event: DataTable.RowSelected
    ) -> None:
        run_id = self.get_run_id(event.row_key)
        if run_id:
            await self.show_run(run_id, preview=False)

    async def on_data_table_row_highlighted(
        self, event: DataTable.RowHighlighted
    ) -> None:
        run_id = self.get_run_id(event.row_key)
        if run_id:
            await self.show_run(run_id, preview=True)

    async def show_run(self, run_id: str, preview: bool = False):
        try:
            run = get(f"/runs/{run_id}")
        except Exception as ex:
            self.details.update(f"[red]Failed to fetch run: {ex}[/red]")
            return

        panel = run_summary_panel(run)
        self.details.update(panel)

        if not preview:
            await self.app.push_screen("run_detail", run_id=run_id)

    def action_reload(self):
        """Reload run table."""
        self.load_runs()
