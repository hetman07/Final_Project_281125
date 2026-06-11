from pymongo import MongoClient
from datetime import datetime
from ui import console
from typing import Any


class MongoDB:
    def __init__(self, config, dbconfig) -> None:
        self.client: MongoClient = MongoClient(config)
        self.db = self.client[dbconfig["db_name"]]
        self.collection = self.db[dbconfig["collection_name"]]

    #  Write — log search events
    def log_title_search(self, keyword: str, results_count: int) -> None:
        """
        Persist a title-search event to the activity log.

        Args:
            keyword:       Raw search term (stored uppercased).
            results_count: Number of matching films returned by MySQL.
        """
        self.collection.insert_one(
            {
                "ID_type": 1,
                "type_name": "title_search",
                "params": {"keyword": keyword.upper()},
                "results_count": results_count,
                "timestamp": datetime.now(),
            }
        )

    def log_genre_search(
        self,
        genre_id: int,
        genre_name: str,
        start_year: int,
        end_year: int,
        results_count: int,
    ) -> None:
        """
        Persist a genre+year-range search event to the activity log.

        Args:
            genre_id:      Category ID from the sakila database.
            genre_name:    Human-readable genre label.
            start_year:    Lower bound of the year filter.
            end_year:      Upper bound of the year filter.
            results_count: Number of matching films returned by MySQL.
        """
        self.collection.insert_one(
            {
                "ID_type": 2,
                "type_name": "genre_search",
                "params": {
                    "genre_id": genre_id,
                    "genre_name": genre_name,
                    "start_year": start_year,
                    "end_year": end_year,
                },
                "results_count": results_count,
                "timestamp": datetime.now(),
            }
        )

    def log_rating_search(self, rating: str, results_count: int) -> None:
        """
        Persist a rating-search event to the activity log.

        Args:
            rating:        MPAA rating string (stored uppercased).
            results_count: Number of matching films returned by MySQL.
        """
        self.collection.insert_one(
            {
                "ID_type": 3,
                "type_name": "rating_search",
                "params": {
                    "rating": rating.upper(),
                },
                "results_count": results_count,
                "timestamp": datetime.now(),
            }
        )

    #  Read
    def get_top_queries_by_title(self, limit: int = 5):
        pipeline: list[dict[str, Any]] = [
            {"$match": {"ID_type": 1, "type_name": "title_search"}},
            {
                "$group": {
                    "_id": "$params.keyword",
                    "count": {"$sum": 1},
                    "last_search": {"$max": "$timestamp"},
                }
            },
            {"$project": {"_id": 0, "keyword": "$_id", "count": 1, "last_search": 1}},
            {"$sort": {"count": -1}},
            {"$limit": limit},
        ]
        return self.collection.aggregate(pipeline)

    def get_top_queries_by_genre(self, limit: int = 5):
        pipeline: list[dict[str, Any]] = [
            {"$match": {"ID_type": 2, "type_name": "genre_search"}},
            {
                "$group": {
                    "_id": {
                        "genre": "$params.genre_name",
                        "start_year": "$params.start_year",
                        "end_year": "$params.end_year",
                    },
                    "count": {"$sum": 1},
                    "avg_results": {"$avg": "$results_count"},
                    "last_search": {"$max": "$timestamp"},
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "genre": "$_id.genre",
                    "start_year": "$_id.start_year",
                    "end_year": "$_id.end_year",
                    "year_range": {
                        "$concat": [
                            {"$toString": "$_id.start_year"},
                            "-",
                            {"$toString": "$_id.end_year"},
                        ]
                    },
                    "count": 1,
                    "last_search": 1,
                    "periods": 1,
                }
            },
            {"$sort": {"count": -1, "last_search": -1}},
            {"$limit": limit},
        ]
        return self.collection.aggregate(pipeline)

    def get_top_queries_by_rating(self, limit: int = 5):
        pipeline: list[dict[str, Any]] = [
            {"$match": {"ID_type": 3, "type_name": "rating_search"}},
            {
                "$group": {
                    "_id": "$params.rating",
                    "count": {"$sum": 1},
                    "last_search": {"$max": "$timestamp"},
                }
            },
            {"$project": {"_id": 0, "keyword": "$_id", "count": 1, "last_search": 1}},
            {"$sort": {"count": -1, "last_search": -1}},
            {"$limit": limit},
        ]
        return self.collection.aggregate(pipeline)

    def get_top_the_last_queries(self, limit: int = 5):
        pipeline: list[dict[str, Any]] = [
            {
                "$group": {
                    "_id": {"type_name": "$type_name", "params": "$params"},
                    "count": {"$sum": 1},
                    "last_search": {"$max": "$timestamp"},
                }
            },
            {"$sort": {"last_search": -1}},
            {"$limit": limit},
            {
                "$project": {
                    "_id": 0,
                    "type_name": "$_id.type_name",
                    "params": "$_id.params",
                    "count": 1,
                    "timestamp": "$last_search",
                }
            },
        ]
        return self.collection.aggregate(pipeline)

    def __del__(self):
        """Close the MongoDB connection when the object is garbage-collected."""
        try:
            self.client.close()
            console.print("[green]✓  MongoDB connection closed.[/green]")
        except Exception as e:
            console.print(
                f"[red]✗  Could not close MongoDB connection: {e}[/red]")