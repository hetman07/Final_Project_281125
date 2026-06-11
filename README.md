# 🎬 Sakila Film Search — Terminal App

A Python terminal application for searching films from the **Sakila** MySQL database with activity logging to **MongoDB**.

---

## Features

- Search films by **title**, **genre + year range**, or **MPAA rating**
- Paginated results (10 films per page)
- All searches are automatically logged to MongoDB
- Statistics menu shows top search queries and recent activity

---

## Project Structure

```
├── main.py           # Entry point, database connections, main menu
├── films_menu.py     # Search by title
├── genres_menu.py    # Search by genre and year range
├── rating_menu.py    # Search by rating
├── stats_menu.py     # Statistics sub-menu
├── db_mysql.py       # MySQL connection and queries
├── db_mongo.py       # MongoDB connection, logging, aggregations
├── sql_queries.py    # All SQL query strings
├── pagination.py     # Reusable pagination cursor
├── ui.py             # Rich-based terminal UI components
├── const.py          # Column descriptors for stats tables
└── config.py         # MySQL and MongoDB connection settings
```

---

## Requirements

```
pymysql
pymongo
rich
```

Install with:
```bash
pip install pymysql pymongo rich
```

---

## Configuration

Edit `config.py` to set your connection details:

```python
# MySQL
config = {
    "host": "...",
    "user": "...",
    "password": "...",
    "database": "sakila",
}

# MongoDB
mongoconfig = "mongodb://user:password@host/..."

mongodbconfig = {
    "db_name": "your_db",
    "collection_name": "your_collection",
}
```

---

## Running

```bash
python main.py
```

---

## Menu Overview

```
◈  Menu  ◈
1  Search films by title
2  Search films by genre and year
3  Search films by rating
4  Statistics
5  Exit
```

The **Statistics** sub-menu shows:
1. Top-5 most searched titles
2. Top-5 most searched genre + year combinations
3. Top-5 most searched ratings
4. 5 most recent searches

---

## Databases

| Database | Purpose |
|----------|---------|
| MySQL `sakila` | Film data (titles, genres, ratings) |
| MongoDB `ich_edit` | Search activity log and statistics |
