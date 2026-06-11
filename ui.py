"""
ui.py — Terminal UI utilities.

Provides all Rich-based rendering functions: menus, tables, and stat panels.
No business logic lives here — only presentation.
"""

from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

# Box style used for all data tables — clean, readable double-border
TABLE_BOX = box.DOUBLE_EDGE

# Accent colors
COL_INDEX = "bold bright_white"
COL_PRIMARY = "bold cyan"
COL_NUMBER = "bold bright_magenta"
COL_DATE = "yellow"
COL_SUCCESS = "bold green"
COL_DIM = "dim white"


def menu(
    name_menu: str = "Menu", param1: str = "Search films", param2: str = "Statistics"
) -> None:
    """
    Render the main or statistics navigation panel with five numbered options.

    Args:
        name_menu: Panel title shown in the header.
        param1:    Label prefix for search options (1–3).
        param2:    Label for option 4 (statistics / second-level menu).
    """

    table = Table(show_header=False, box=None, padding=(0, 1))

    table.add_row("[bold cyan]1[/bold cyan]",
                  f"[white]{param1} by title[/white]")
    table.add_row(
        "[bold cyan]2[/bold cyan]", f"[white]{param1} by genre and year[/white]"
    )
    table.add_row("[bold cyan]3[/bold cyan]",
                  f"[white]{param1} by rating[/white]")
    table.add_row("[bold cyan]4[/bold cyan]", f"[white]{param2}[/white]")
    table.add_row("[bold red]5[/bold red]", "[red]Exit[/red]")

    console.print(
        Panel(
            table,
            title=f"[bold yellow]◈  {name_menu}  ◈[/bold yellow]",
            border_style="bright_blue",
            padding=(1, 3),
            expand=False,
        )
    )


def print_table(data: list[dict], title: str = "Results") -> None:
    """
    Print a list of dictionaries as a Rich table.

    Args:
        data: List of dictionaries.
        title: Table title.
    """
    if not data:
        print("[yellow]⚠  No records found.[/yellow]")
        return

    table = Table(
        title=f"[bold white]{title}[/bold white]",
        box=TABLE_BOX,
        show_header=True,
        header_style="bold bright_blue on grey23",
        border_style="bright_blue",
        show_lines=True,
        padding=(0, 1),
    )

    # First column is usually a row-number — right-align it
    keys = list(data[0].keys())
    for i, key in enumerate(keys):
        header = key.replace("_", " ").title()
        if i == 0:
            table.add_column(header, justify="right",
                             style=COL_DIM, no_wrap=True)
        else:
            table.add_column(header, style="white")

    for row in data:
        table.add_row(*[str(v) for v in row.values()])

    console.print(table)


ColumnSpec = dict


def print_rich_table(data: list[dict], title: str, columns: list[ColumnSpec]) -> None:
    """
    Print a MongoDB stats result as a styled Rich table.

    Column layout is driven by a list of column-spec dicts defined in const.py.
    Dates are auto-formatted to DD.MM.YYYY when col["type"] == "date".

    Args:
        data:    List of result dicts from a MongoDB aggregation.
        title:   Table title.
        columns: Column descriptors — see const.py for the schema.
    """
    if not data:
        console.print(
            "[yellow]⚠  No statistics found yet. Start searching first.[/yellow]"
        )
        return

    table = Table(
        title=f"[bold white]{title}[/bold white]",
        box=TABLE_BOX,
        show_header=True,
        header_style="bold bright_blue on grey23",
        border_style="bright_blue",
        show_lines=True,
        padding=(0, 1),
    )

    for col in columns:
        table.add_column(
            col["header"],
            style=col.get("style"),
            justify=col.get("justify", "left"),
        )

    for row in data:
        values: list[str] = []
        for col in columns:
            value = row.get(col["key"])
            if col.get("type") == "date" and isinstance(value, datetime):
                value = value.strftime("%d.%m.%Y %H:%M")
            values.append(str(value) if value is not None else "—")
        table.add_row(*values)

    console.print(table)


def _format_query_label(doc: dict) -> str:
    """
    Convert a raw MongoDB log document to a human-readable query label.

    Args:
        doc: Single document from the recent-queries aggregation.

    Returns:
        A short descriptive string, e.g. "by genre: Action (2000-2005)".
    """
    t = doc.get("type_name", "")
    params = doc.get("params", {})

    if t == "title_search":
        return f"by title: [cyan]{params.get('keyword', '')}[/cyan]"

    if t == "genre_search":
        genre = params.get("genre_name", "unknown")
        start = params.get("start_year")
        end = params.get("end_year")
        yr = f" ({start}–{end})" if start and end else ""
        return f"by genre: [cyan]{genre}{yr}[/cyan]"

    if t == "rating_search":
        return f"by rating: [cyan]{params.get('rating', '')}[/cyan]"

    return "[dim]unknown[/dim]"


def print_top_5_recent_queries(data: list[dict]) -> None:
    """
    Print the five most recent search log entries as a numbered table.

    Args:
        data: List of up to 5 MongoDB log documents, newest first.
    """
    if not data:
        console.print("[yellow]⚠  No recent queries yet.[/yellow]")
        return

    table = Table(
        title="[bold white]5 Most Recent Queries[/bold white]",
        box=TABLE_BOX,
        show_header=True,
        header_style="bold bright_blue on grey23",
        border_style="bright_blue",
        show_lines=True,
        padding=(0, 1),
    )

    table.add_column("#", justify="right", style=COL_DIM, no_wrap=True)
    table.add_column("Query", style="white")
    table.add_column("Last Search", style=COL_DATE)
    table.add_column("Count", justify="right")

    for i, doc in enumerate(data, start=1):
        ts = doc.get("timestamp")
        date = ts.strftime("%d.%m.%Y %H:%M") if isinstance(
            ts, datetime) else "—"
        table.add_row(str(i), _format_query_label(
            doc), date, str(doc.get("count", 1)))

    console.print(table)
