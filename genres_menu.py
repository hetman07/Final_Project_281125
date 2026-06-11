from ui import print_table, console
from pagination import Pagination


def genres_menu(db, mongo_db) -> None:
    """
    Interactive loop: choose a genre, enter a year range, paginate results.

    The outer loop repeats until the user chooses to go back to the main menu.
    Input validation keeps the user inside the loop on bad values instead of
    crashing or returning silently.

    Args:
        db:       Open MySQL connection wrapper.
        mongo_db: Open MongoDB connection wrapper.
    """
    paginator = Pagination()

    while True:
        # show available genres
        try:
            genres_years = db.get_genres_years()
        except Exception as e:
            console.print(f"[red]✗  Could not fetch genres: {e}[/red]")
            return

        print_table(genres_years, "Available Genres")

        # genre selection
        genre_id = _read_int("Select genre № ID: ")
        if genre_id is None:
            continue

        try:
            genre = db.get_films_by_genre(genre_id)
        except Exception as e:
            console.print(f"[red]✗  Database error: {e}[/red]")
            return

        if not genre:
            console.print("[yellow]⚠  Genre ID not found. Try again.[/yellow]")
            continue

        genre_row = genre[0]
        genre_name = genre_row["Genre"]
        valid_start = genre_row["start year"]
        valid_end = genre_row["end year"]

        console.print(
            f"  Genre: [bold cyan]{genre_name}[/bold cyan] — "
            f"available years [green]{valid_start}[/green] – [green]{valid_end}[/green]"
        )

        # year range
        start_year, end_year = _read_year_range(valid_start, valid_end)

        # count + log
        try:
            cnt_films: int = db.get_cnt_films_by_range_years(
                genre_id, start_year, end_year
            )["cnt_films"]
        except Exception as e:
            console.print(f"[red]✗  Could not count films: {e}[/red]")
            continue
        # log mongo_db
        try:
            mongo_db.log_genre_search(
                genre_id, genre_name, start_year, end_year, cnt_films
            )
        except Exception as e:
            console.print(
                f"[yellow]⚠  Could not write to activity log: {e}[/yellow]")

        if not cnt_films:
            console.print(
                f"[yellow]⚠  No films found for [bold]{genre_name}[/bold] "
                f"in {start_year}–{end_year}.[/yellow]"
            )
        else:
            paginator.set_total(cnt_films)
            console.print(
                f"\nFound [bold bright_magenta]{cnt_films}[/bold bright_magenta] "
                f"film(s) in [bold cyan]{genre_name}[/bold cyan] "
                f"({start_year}–{end_year})."
            )
            _paginate_results(db, paginator, genre_id, start_year, end_year)

        if not _ask_continue("genre"):
            return


def _paginate_results(
    db, paginator: Pagination, genre_id: int, start_year: int, end_year: int
) -> None:
    """
    Inner pagination loop for genre+year results.

    Args:
        db:         Open MySQL connection wrapper.
        paginator:  Pagination state (already initialised with total).
        genre_id:   Category ID used in the SQL query.
        start_year: Lower bound of the year filter.
        end_year:   Upper bound of the year filter.
    """
    while True:
        try:
            films = db.get_films_by_range_years(
                genre_id,
                start_year,
                end_year,
                paginator.limit,
                paginator.offset,
            )
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


def _read_int(prompt: str) -> int | None:
    """
    Prompt the user for an integer.  Returns None on invalid input so the
    caller can `continue` its loop instead of crashing.

    Args:
        prompt: Text shown to the user.

    Returns:
        Parsed integer, or None if the user entered a non-integer value.
    """
    try:
        return int(input(prompt).strip())
    except ValueError:
        console.print("[yellow]⚠  Please enter a whole number.[/yellow]")
        return None


def _ask_continue(search_type: str) -> bool:
    """
    Ask the user whether to search again or return to the main menu.

    Args:
        search_type: Short label for the prompt (e.g. "genre").

    Returns:
        True  → stay in this menu.
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


def _read_year_range(valid_start: int, valid_end: int) -> tuple[int, int]:
    """
    Prompt the user for a valid year range within [valid_start, valid_end].
    Loops until both values are correct — never returns invalid data.

    Args:
        valid_start: Minimum allowed year (from genre data).
        valid_end:   Maximum allowed year (from genre data).

    Returns:
        Tuple (start_year, end_year) — both guaranteed to be valid.
    """
    while True:
        start_year = _read_int(
            f" Enter the start year ({valid_start}–{valid_end}): ")
        if start_year is None:
            continue

        end_year = _read_int(
            f" Enter the end year ({valid_start}–{valid_end}): ")
        if end_year is None:
            continue

        if start_year > end_year:
            console.print(
                "[yellow]⚠  Start year must not exceed end year.[/yellow]")
            continue

        if start_year < valid_start or end_year > valid_end:
            console.print(
                f"[yellow]⚠  Year range must be within "
                f"{valid_start}–{valid_end}.[/yellow]"
            )
            continue

        return start_year, end_year