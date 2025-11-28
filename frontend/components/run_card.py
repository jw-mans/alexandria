from rich.panel import Panel
from rich.table import Table

def run_summary_panel(run: dict) -> Panel:
    t = Table.grid(expand=True)
    t.add_column(justify='left')
    t.add_column(justify='right')
    t.add_row(
        f'[bold]{run.get("experiment_name", "")}[/bold]',
        run.get('id', '')
    )
    t.add_row('start',
        str(run.get('timestamp_start', ''))
    )
    t.add_row('end',
        str(run.get('timestamp_end', ''))
    )
    t.add_row('tags', 
        ', '.join(run.get('tags', []) or [])
    )
    return Panel(t, title='Run Summary', padding=(1, 2))
