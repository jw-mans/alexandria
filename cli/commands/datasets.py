from __future__ import annotations
from typing import Optional
from ..base import BaseCLIApp, console
from rich.table import Table
import typer


class DatasetsApp(BaseCLIApp):
    def __init__(self):
        super().__init__(name="datasets", help="Dataset commands")
        self.register()

    def register(self) -> None:
        @self.app.command("list")
        def list_datasets(limit: Optional[int] = typer.Option(50, "--limit", help="Max datasets to fetch")):
            """List datasets known to the backend."""
            data = self.http_get(f"/runs/datasets?limit={limit}")
            if not data:
                console.print("[yellow]No datasets found[/yellow]")
                return

            table = Table(title="Datasets", show_lines=False)
            table.add_column("Name", style="cyan")
            table.add_column("Path")
            table.add_column("Rows", justify="right")
            table.add_column("Cols", justify="right")
            table.add_column("Hash")

            for ds in data:
                table.add_row(
                    str(ds.get("name", "")),
                    str(ds.get("path", "")),
                    str(ds.get("num_rows", ds.get("rows", ""))),
                    str(ds.get("num_columns", ds.get("cols", ""))),
                    str(ds.get("hash", "")),
                )

            console.print(table)


def get_app() -> BaseCLIApp:
    return DatasetsApp()


