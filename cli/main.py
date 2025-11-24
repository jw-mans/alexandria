import typer
from . import (
    artifacts_app,
    datasets_app,
    diff_app,
    log_app,
    show_app,
)

app = typer.Typer(help="Alexandria CLI")

app.add_typer(log_app().get_app(), name="log")
app.add_typer(show_app().get_app(), name="show")
app.add_typer(diff_app().get_app(), name="diff")
app.add_typer(datasets_app().get_app(), name="datasets")
app.add_typer(artifacts_app().get_app(), name="artifacts")


def main():
    app()


if __name__ == "__main__":
    main()


