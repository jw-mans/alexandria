from textual.screen import Screen
from textual.widgets import Header, Footer
from textual.containers import Container

class BaseView(Screen):
    def compose(self):
        yield Header(show_clock=True)
        yield Container(id='main')
        yield Footer()