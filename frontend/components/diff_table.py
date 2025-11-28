from rich.table import Table
from typing import Any

def diff_to_tables(diff: dict) -> dict:
    """
    Convert diff dict into a mapping of section -> rich.Table for display.
    """
    tables = {}
    for section, content in diff.items():
        if isinstance(content, dict) and content:
            t = Table(title=section, show_header=True)
            t.add_column('Key', style='magenta')
            t.add_column('Old', overflow='fold')
            t.add_column('New', overflow='fold')
            for k, v in content.items():
                if isinstance(v, dict) and \
                    'old' in v and \
                    'new' in v:
                    old, new = v.get('old'), v.get('new')
                else:
                    old = v
                    new = ''
                t.add_row(str(k), str(old), str(new))
            tables[section] = t
        elif isinstance(content, list) and content:
            t = Table(title=section)
            t.add_column('Item')
            for item in content:
                t.add_row(str(item))
            tables[section] = t
    return tables