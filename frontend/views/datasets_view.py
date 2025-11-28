from textual.screen import Screen
from textual.widgets import DataTable, Static
from textual.containers import Vertical
from ..api import get
from rich.table import Table

class DatasetsView(Screen):
    BINDINGS = [("b", "back", "Back")]

    def compose(self):
        self.table = DataTable(zebra_stripes=True)
        yield Vertical(self.table)

    def on_mount(self):
        self.load()

    def load(self):
        try:
            datasets = get("/datasets")
        except Exception as e:
            self.table.clear()
            self.table.add_column("Error")
            self.table.add_row(str(e))
            return
        self.table.clear(columns=True)
        self.table.add_column("Name", style="cyan")
        self.table.add_column("Path")
        self.table.add_column("Rows", justify="right")
        self.table.add_column("Cols", justify="right")
        self.table.add_column("Hash")
        for ds in datasets:
            self.table.add_row(
                str(ds.get("name", "")),
                str(ds.get("path", "")),
                str(ds.get("num_rows", "")),
                str(ds.get("num_columns", "")),
                str(ds.get("hash", "")),
                key=ds.get("hash", None) or ds.get("path", "")
            )
