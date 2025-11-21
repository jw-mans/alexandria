from __future__ import annotations
import os
from typing import Optional
import typer
import httpx
from rich.console import Console


console = Console()




class BaseCLIApp:
    """
    Base wrapper around Typer for shared utilities and http client.
    Subclasses should implement :meth:`register_commands` which will add commands
    to ``self.app``. Use ``get_app()`` to obtain the Typer instance.
    """


    def __init__(self, name: Optional[str] = None, help: Optional[str] = None):
        self.app = typer.Typer(name=name, help=help)


    def get_app(self) -> typer.Typer:
        # ensure commands registered lazily
        return self.app


    @staticmethod
    def get_backend_url() -> str:
        return os.environ.get("TRAINLOG_BACKEND", "http://127.0.0.1:8000").rstrip("/")


    @staticmethod
    def http_get(path: str, timeout: float = 10.0):
        url = f"{BaseCLIApp.get_backend_url()}{path}"
        try:
            with httpx.Client(timeout=timeout) as client:
                r = client.get(url)
                r.raise_for_status()
                return r.json()
        except httpx.RequestError as e:
            console.print(f"[red]Request error: {e}[/red]")
            raise typer.Exit(code=1)
        except httpx.HTTPStatusError as e:
            console.print(f"[red]HTTP error: {e.response.status_code} {e.response.text}[/red]")
            raise typer.Exit(code=1)