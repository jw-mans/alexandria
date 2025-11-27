from __future__ import annotations
from ..base import BaseCLIApp, console

class LogApp(BaseCLIApp):
    def __init__(self):
        super().__init__(name="log", help="Manual logging commands")
        self.register()

    def register(self) -> None:
        @self.app.command("info")
        def info():
            console.print("[yellow]Manual logging is not implemented yet.[/yellow]")
            console.print("Use the tracker decorator or examples to send runs to the backend.")

def get_app() -> BaseCLIApp:
    return LogApp()