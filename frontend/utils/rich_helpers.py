from rich.table import Table
from rich.console import Group
from rich.panel import Panel

def pretty_kv_table(
    d: dict,
    title: str | None = None
) -> Table:
    t = Table(title=title, show_lines=False)
    t.add_column('Field', style='cyan', no_wrap=True)
    t.add_column('Value', overflow='fold')
    for k, v in d.items():
        t.add_row(str(k), str(v))
    return t
