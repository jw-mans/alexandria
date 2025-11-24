from __future__ import annotations
from typing import Optional
from ..base import BaseCLIApp, console
from rich.table import Table
import typer

class DiffApp(BaseCLIApp):
    def __init__(self):
        super().__init__(name="diff", help="Show differences between runs")
        self.register()

    def register(self) -> None:
        @self.app.command("runs")
        def runs(id1: str, id2: str, json: Optional[bool] = typer.Option(False, "--json", help="Print raw JSON")):
            data = self.http_get(f"/runs/{id1}/diff/{id2}")
            if json:
                console.print(data)
                return

            # Pretty print sections
            for section, content in data.items():
                console.rule(f"[bold]{section}[/bold]")
                if isinstance(content, dict) and content:
                    table = Table(show_header=True, header_style="bold magenta")
                    table.add_column("Key")
                    table.add_column("Old", overflow="fold")
                    table.add_column("New", overflow="fold")
                    for k, v in content.items():
                        if isinstance(v, dict) and "old" in v and "new" in v:
                            old = v.get("old")
                            new = v.get("new")
                        else:
                            old = v
                            new = ""
                        table.add_row(str(k), str(old), str(new))
                    console.print(table)
                elif isinstance(content, list) and content:
                    for item in content:
                        console.print(f"- {item}")
                else:
                    console.print(str(content))

def get_app() -> BaseCLIApp:
    return DiffApp()
