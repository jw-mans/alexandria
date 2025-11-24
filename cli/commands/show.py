from __future__ import annotations
from typing import Optional
from ..base import BaseCLIApp, console
from rich.table import Table
from rich.pretty import Pretty
import typer

class ShowApp(BaseCLIApp):
    def __init__(self):
        super().__init__(name="show", help="Show run information")
        self.register()

    def register(self) -> None:
        @self.app.command("run")
        def run(id: str, raw: Optional[bool] = typer.Option(False, "--raw", help="Print raw JSON")):
            data = self.http_get(f"/runs/{id}")
            if raw:
                console.print(Pretty(data))
                return

            table = Table(title=f"Run {id}", show_lines=False)
            table.add_column("Field", style="cyan", no_wrap=True)
            table.add_column("Value", style="white")

            order = [
                "experiment_name",
                "timestamp_start",
                "timestamp_end",
                "tags",
                "parameters",
                "metrics",
                "dataset",
                "code",
                "environment",
                "artifacts",
            ]
            for key in order:
                if key in data:
                    table.add_row(key, str(data[key]))
            for k, v in data.items():
                if k in order:
                    continue
                table.add_row(k, str(v))

            console.print(table)

def get_app() -> BaseCLIApp:
    return ShowApp()
