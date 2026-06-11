from ui import print_table, console
from pagination import Pagination

def films_menu(db, mongo_db) -> None:
    """
    Interactive loop: search films by keyword, paginate results, log to Mongo.

    The loop runs until the user explicitly chooses to return to the main menu.
    Every DB call is wrapped so a bad query or connectivity blip prints a
    friendly message and lets the user try again.

    Args:
        db:       Open MySQL connection wrapper.
        mongo_db: Open MongoDB connection wrapper.
    """
    paginator = Pagination()

    while True:
        keyword = input("\nEnter the title of the film: ").strip().upper()

        if not keyword:
            console.print(
                "[yellow]⚠  Please enter at least one character.[/yellow]")
            continue

        try:
            cnt_films: int = db.get_cnt_films_by_title(keyword)["cnt_films"]
        except Exception as e:
            console.print(
                f"[red]✗  Database error while counting films: {e}[/red]")
            continue

        # log mongo_db
        try:
            mongo_db.log_title_search(keyword, cnt_films)
        except Exception as e:
            console.print(
                f"[yellow]⚠  Could not write to activity log: {e}[/yellow]")

        if not cnt_films:
            console.print(
                f"[yellow]⚠  No films found for '[bold]{keyword}[/bold]'.[/yellow]"
            )
        else:
            paginator.set_total(cnt_films)
            console.print(
                f"\nFound [bold bright_magenta]{cnt_films}[/bold bright_magenta] "
                f"film(s) matching '[bold cyan]{keyword}[/bold cyan]'."
            )
            _paginate_results(db, paginator, keyword)

        if not _ask_continue("title"):
            return


def _paginate_results(db, paginator: Pagination, keyword: str) -> None:
    """
    Inner pagination loop: print pages of results until the user stops.

    Args:
        db:        Open MySQL connection wrapper.
        paginator: Pagination state object (already initialised with total).
        keyword:   The search term passed to the SQL query.
    """
    while True:
        try:
            films = db.get_films_by_title(
                keyword, paginator.limit, paginator.offset)
        except Exception as e:
            console.print(f"[red]✗  Could not fetch page: {e}[/red]")
            break

        print_table(films, f"Films - {paginator.status()}")

        if not paginator.has_next:
            console.print("[dim]  End of results.[/dim]")
            break

        choise = input("Next page? (y / n): ").strip().upper()
        if choise == "Y":
            paginator.next()
        else:
            break


def _ask_continue(search_type: str) -> bool:
    """
    Ask the user whether to search again or return to the main menu.

    Args:
        search_type: Short label used in the prompt text (e.g. "title").

    Returns:
        True  → stay in this menu (search again).
        False → return to the main menu.
    """
    while True:
        nav = input(
            f"\n  [1] Search by {search_type} again   [2] Main menu — choose: "
        ).strip()
        if nav == "1":
            return True
        if nav == "2":
            return False

        console.print("[yellow]  Please enter 1 or 2.[/yellow]")
