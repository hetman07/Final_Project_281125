"""
const.py — Column descriptors for MongoDB stats tables.
 
Each entry in a column list is a dict understood by ui.print_rich_table():
  header   — visible column header text
  key      — dict key to read from the result row
  style    — Rich markup color/style string
  justify  — "left" | "right" | "center"  (optional, default "left")
  type     — "date" triggers strftime formatting  (optional)
"""

# Columns for the TOP-5 genre-search stats table
genre_columns = [
    {"header": "Genre", "key": "genre", "style": "cyan"},
    {"header": "Year Range", "key": "year_range", "style": "green"},
    {"header": "Last Search", "key": "last_search", "style": "yellow", "type": "date"},
    {"header": "Count", "key": "count", "style": "magenta", "justify": "right"},
]
# Columns for the TOP-5 title-search stats table
title_columns = [
    {"header": "Keyword", "key": "keyword", "style": "cyan"},
    {"header": "Searches", "key": "count", "style": "magenta", "justify": "right"},
    {"header": "Last Search", "key": "last_search", "style": "yellow", "type": "date"},
]
# Columns for the TOP-5 rating-search stats table
rating_columns = [
    {"header": "Rating", "key": "keyword", "style": "cyan"},
    {"header": "Searches", "key": "count", "style": "magenta", "justify": "right"},
    {"header": "Last Search", "key": "last_search", "style": "yellow", "type": "date"},
]