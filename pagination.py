class Pagination:
    """
    Lightweight pagination cursor.
 
    Usage::
 
        p = Pagination(limit=10)
        p.set_total(42)          # called after the COUNT query
 
        while True:
            rows = db.query(limit=p.limit, offset=p.offset)
            print_table(rows, p.status())
            if not p.has_next:
                break
            p.next()
 
    Args:
        total: Initial total record count (default 0 — call set_total later).
        limit: Number of rows per page (default 10).
    """
    def __init__(self, total: int = 0, limit: int = 10) -> None:
        self.limit: int = limit
        self._total: int = total
        self._current_page: int = 1

# ------------------------------------------------------------------
# Properties — read-only computed values
# ------------------------------------------------------------------
 
    @property
    def total(self) -> int:
        """Total number of records across all pages."""
        return self._total
 
    @property
    def current_page(self) -> int:
        """Current 1-based page number."""
        return self._current_page
 
    @property
    def total_pages(self) -> int:
        """Number of pages needed to display all records."""
        if self._total == 0:
            return 0
        return (self._total + self.limit - 1) // self.limit
 
    @property
    def offset(self) -> int:
        """SQL OFFSET for the current page."""
        return (self._current_page - 1) * self.limit
 
    @property
    def has_next(self) -> bool:
        """True when a next page exists."""
        return self._current_page < self.total_pages
 
    @property
    def has_previous(self) -> bool:
        """True when a previous page exists."""
        return self._current_page > 1

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------
 
    def next(self) -> None:
        """Advance one page forward (no-op on the last page)."""
        if self.has_next:
            self._current_page += 1
 
    def previous(self) -> None:
        """Step one page back (no-op on the first page)."""
        if self.has_previous:
            self._current_page -= 1
 
    def reset(self) -> None:
        """Return to page 1 without changing the total."""
        self._current_page = 1
 
    def set_total(self, total: int) -> None:
        """
        Update the total record count and reset to page 1.
 
        Call this after every new search query so the cursor reflects the
        new result set.
 
        Args:
            total: Total number of records returned by the COUNT query.
        """
        self._total = total
        self._current_page = 1
        
# ------------------------------------------------------------------
# Display helpers
# ------------------------------------------------------------------
 
    def status(self) -> str:
        """Human-readable progress: 'Page 2 of 5 (42 records)'"""
        return f"Page {self._current_page} of {self.total_pages} ({self._total} records)"