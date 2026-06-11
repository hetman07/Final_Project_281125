import pymysql
from sql_queries import (
    sql_films_by_title,
    sql_cnt_films_by_title,
    sql_genres_years,
    sql_films_by_genre,
    sql_films_by_range_years,
    sql_cnt_films_by_range_years,
    sql_list_of_rating,
    sql_cnt_films_by_rating,
    sql_films_by_rating,
)
from ui import console


class DB:
    def __init__(self, config):
        self.connection = pymysql.connect(**config, charset="utf8mb4")

    # by title
    def get_films_by_title(self, film_title: str, limit: int, offset: int):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_films_by_title,
                           (f"%{film_title}%", limit, offset))
            return cursor.fetchall()

    def get_cnt_films_by_title(self, film_title: str):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_cnt_films_by_title, (f"%{film_title}%",))
            return cursor.fetchone()

    # by genre
    def get_genres_years(self):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_genres_years)
            return cursor.fetchall()

    def get_films_by_genre(self, category_id: int):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_films_by_genre, (category_id,))
            return cursor.fetchall()

    def get_films_by_range_years(
        self, category_id: int, start_year: int, end_year: int, limit: int, offset: int
    ):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                sql_films_by_range_years,
                (category_id, start_year, end_year, limit, offset),
            )
            return cursor.fetchall()

    def get_cnt_films_by_range_years(
        self, category_id: int, start_year: int, end_year: int
    ):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                sql_cnt_films_by_range_years, (category_id,
                                               start_year, end_year)
            )
            return cursor.fetchone()

    # by rating
    def get_list_of_ratings(self):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_list_of_rating)
            return cursor.fetchall()

    def get_cnt_films_by_rating(self, rating: str):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_cnt_films_by_rating, (rating,))
            return cursor.fetchone()

    def get_films_by_rating(self, rating: str, limit: int, offset: int):
        with self.connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql_films_by_rating, (rating, limit, offset))
            return cursor.fetchall()

    # close connection
    def __del__(self):
        if hasattr(self, "connection"):
            self.connection.close()
            console.print("[green]✓  MySQL connection closed.[/green]")