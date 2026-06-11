from ui import print_table, console
from pagination import Pagination


def rating_menu(db, mongo_db) -> None:
    """
    Interactive loop: choose an MPAA rating, browse paginated results.

    The outer loop repeats until the user chooses to return to the main menu.

    Args:
        db:       Open MySQL connection wrapper.
        mongo_db: Open MongoDB connection wrapper.
    """
    paginator = Pagination()

    while True:
        # show available ratings
        try:
            rating_list = db.get_list_of_ratings()
        except Exception as e:
            console.print(f"[red]✗  Could not load rating list: {e}[/red]")
            return

        print_table(rating_list, "Available Ratings")
        # rating input
        rating = input("\nEnter rating (e.g. PG, R, G): ").strip().upper()

        if not rating:
            console.print("[yellow]⚠  Rating cannot be empty.[/yellow]")
            continue

        # count matching films
        try:
            cnt_films = db.get_cnt_films_by_rating(rating)["cnt_films"]
        except Exception as e:
            console.print(
                f"[red]✗  Database error while counting films: {e}[/red]")
            continue

        # log search
        # log mongo_db
        try:
            mongo_db.log_rating_search(rating, cnt_films)
        except Exception as e:
            console.print(
                f"[yellow]⚠  Could not write to activity log: {e}[/yellow]")

        if not cnt_films:
            console.print(
                f"[yellow]⚠  No films found for rating '[bold]{rating}[/bold]'.[/yellow]"
            )
        else:
            paginator.set_total(cnt_films)
            console.print(
                f"\nFound [bold bright_magenta]{cnt_films}[/bold bright_magenta] "
                f"film(s) with rating [bold cyan]{rating}[/bold cyan]."
            )
            _paginate_results(db, paginator, rating)

        if not _ask_continue("rating"):
            return


def _paginate_results(db, paginator: Pagination, rating: str) -> None:
    """
    Inner pagination loop for rating results.

    Args:
        db:        Open MySQL connection wrapper.
        paginator: Pagination state (already initialised with total).
        rating:    Rating string used in the SQL query.
    """
    while True:
        try:
            films = db.get_films_by_rating(
                rating, paginator.limit, paginator.offset)
        except Exception as e:
            console.print(f"[red]✗  Could not fetch page: {e}[/red]")
            break

        print_table(films, f"Films — {paginator.status()}")

        if not paginator.has_next:
            console.print("[dim]  End of results.[/dim]")
            break

        choice = input("  Next page? (y / n): ").strip().upper()
        if choice == "Y":
            paginator.next()
        else:
            break


def _ask_continue(search_type: str) -> bool:
    """
    Ask whether to search again or go back to the main menu.

    Args:
        search_type: Short label for the prompt (e.g. "rating").

    Returns:
        True  → search again.
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