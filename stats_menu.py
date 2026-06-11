from ui import menu, print_rich_table, print_top_5_recent_queries, console
from const import genre_columns, title_columns, rating_columns


def stats_menu(mongo_db):
    """
    Interactive statistics sub-menu.

    Loops until the user chooses option 5 (exit / back to main menu).
    Each option fetches and displays a different aggregation from MongoDB.

    Args:
        mongo_db: Open MongoDB connection wrapper.
    """
    while True:
        menu("STATISTICS", "TOP-5 queries", "TOP-5 recent queries")

        user_command = _read_menu_choice()

        if user_command is None:
            continue

        if user_command == 5:
            break
        elif user_command == 1:
            _show_stat(
                fetch=lambda: list(mongo_db.get_top_queries_by_title()),
                title="TOP-5 queries by Title",
                columns=title_columns,
            )
        elif user_command == 2:
            _show_stat(
                fetch=lambda: list(mongo_db.get_top_queries_by_genre()),
                title="TOP-5 queries by Genre",
                columns=genre_columns,
            )
        elif user_command == 3:
            _show_stat(
                fetch=lambda: list(mongo_db.get_top_queries_by_rating()),
                title="TOP-5 queries by Rating",
                columns=rating_columns,
            )
        elif user_command == 4:
            try:
                data = list(mongo_db.get_top_the_last_queries(limit=5))
                print_top_5_recent_queries(data)
            except Exception as e:
                console.print(
                    f"[red]✗  Could not fetch recent queries: {e}[/red]")
        else:
            console.print(
                "[yellow]⚠  Please enter a number from 1 to 5.[/yellow]")


def _read_menu_choice() -> int | None:
    """
    Read a single menu choice from stdin.

    Returns:
        Parsed integer, or None if the user entered a non-integer value.
    """
    try:
        return int(input("Select menu item: ").strip())
    except ValueError:
        console.print("[yellow]⚠  Please enter a number.[/yellow]")
        return None


def _show_stat(fetch, title: str, columns: list[dict]) -> None:
    """
    Fetch and display one stats table, with error handling.

    Args:
        fetch:   Zero-argument callable that returns a list of result dicts.
        title:   Table title passed to print_rich_table.
        columns: Column descriptors passed to print_rich_table.
    """
    try:
        data = fetch()
        print_rich_table(data, title, columns)
    except Exception as e:
        console.print(f"[red]✗  Could not load statistics: {e}[/red]")