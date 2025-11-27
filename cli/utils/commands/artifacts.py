from __future__ import annotations
from typing import List
from rich.table import Table

from ..base import BaseCLIApp, console

class ArtifactsApp(BaseCLIApp):
    def __init__(self):
        super().__init__(name="artifacts", help="Artifacts commands")
        self.register()

    def register(self) -> None:
        @self.app.command("list")
        def list_artifacts(run_id: str):
            """List artifacts for a run"""
            data = self.http_get(f"/runs/{run_id}")
            arts = data.get("artifacts", {})
            if not arts:
                console.print("[yellow]No artifacts found for this run[/yellow]")
                return

            table = Table(title=f"Artifacts of {run_id}")
            table.add_column("Name", style="cyan")
            table.add_column("Type")
            table.add_column("Path")
            table.add_column("Hash")

            for name, meta in arts.items():
                table.add_row(
                    str(name),
                    str(meta.get("type", "")),
                    str(meta.get("path", "")),
                    str(meta.get("hash", "")),
                )

            console.print(table)

def get_app() -> BaseCLIApp:
    return ArtifactsApp()
