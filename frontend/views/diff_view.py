from textual.screen import Screen
from textual.widgets import Input, Button, Static
from textual.containers import Vertical, Horizontal
from ..api import get
from ..components.diff_table import diff_to_tables
from rich.console import Group

class DiffView(Screen):
    BINDINGS = [("b", "back", "Back")]

    def compose(self):
        self.input_a = Input(placeholder="run id 1", id="run_a")
        self.input_b = Input(placeholder="run id 2", id="run_b")
        self.btn = Button(label="Compare", id="compare")
        self.out = Static("")
        yield Vertical(
            Horizontal(self.input_a, self.input_b, self.btn),
            self.out
        )

    def on_button_pressed(self, event):
        if event.button.id == "compare":
            self.perform_diff()

    def perform_diff(self):
        a = self.input_a.value.strip()
        b = self.input_b.value.strip()
        if not a or not b:
            self.out.update("[yellow]Please provide two run ids[/yellow]")
            return
        try:
            data = get(f"/runs/{a}/diff/{b}")
        except Exception as e:
            self.out.update(f"[red]Failed to fetch diff: {e}[/red]")
            return
        tables = diff_to_tables(data)
        group = []
        for sec, t in tables.items():
            group.append(t)
        self.out.update(Group(*group))

    async def action_back(self):
        await self.app.pop_screen()
