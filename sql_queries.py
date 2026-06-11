sql_films_by_title = """
    SELECT
    ROW_NUMBER() OVER() AS rn,
    f.title,
    f.release_year,
    f.rating,
    GROUP_CONCAT(c.name ORDER BY c.name SEPARATOR ', ') AS genres
FROM sakila.film f
LEFT JOIN sakila.film_category fc 
    ON f.film_id = fc.film_id
LEFT JOIN sakila.category c 
    ON fc.category_id = c.category_id
WHERE UPPER(f.title) LIKE %s
GROUP BY 
    f.title,
    f.release_year,
    f.rating
LIMIT %s OFFSET %s
"""
sql_cnt_films_by_title = """
    SELECT count(DISTINCT f.film_id) AS cnt_films
    FROM sakila.film f
    LEFT JOIN sakila.film_category fc 
        ON f.film_id = fc.film_id
    LEFT JOIN sakila.category c 
        ON fc.category_id = c.category_id
    WHERE UPPER(f.title) LIKE %s
"""

sql_genres_years = """
    SELECT c.category_id as '№ ID'
        , c.name as Genre
        , MIN(f.release_year) as 'Start year'
        , MAX(f.release_year) as 'End year'
    FROM sakila.film f 
    LEFT JOIN sakila.film_category fc ON f.film_id = fc.film_id
    LEFT JOIN sakila.category c ON fc.category_id = c.category_id 
    WHERE c.name IS NOT NULL 
    GROUP BY c.category_id, c.name
    ORDER BY 1
"""

sql_films_by_genre = """
    SELECT c.name AS Genre
        , count(DISTINCT f.film_id) as cnt_films
        , MIN(f.release_year) as 'start year'
        , MAX(f.release_year) as 'end year'
    FROM sakila.film f 
    LEFT JOIN sakila.film_category fc ON f.film_id = fc.film_id
    LEFT JOIN sakila.category c ON fc.category_id = c.category_id 
    WHERE c.name IS NOT NULL 
        AND c.category_id = %s
    GROUP BY c.name
"""

sql_films_by_range_years = """
    SELECT ROW_NUMBER() OVER() AS rn
            , f.title AS Title
            , f.release_year as Year
            , c.category_id as '№ ID'
            , f.rating
        FROM sakila.film f 
        LEFT JOIN sakila.film_category fc ON f.film_id = fc.film_id
        LEFT JOIN sakila.category c ON fc.category_id = c.category_id 
        WHERE c.name IS NOT NULL 
            AND c.category_id = %s
            AND f.release_year BETWEEN %s AND %s 
    LIMIT %s OFFSET %s
"""

sql_cnt_films_by_range_years = """
    SELECT COUNT(DISTINCT f.film_id) as cnt_films
        FROM sakila.film f 
        LEFT JOIN sakila.film_category fc ON f.film_id = fc.film_id
        LEFT JOIN sakila.category c ON fc.category_id = c.category_id 
        WHERE c.name IS NOT NULL 
            AND c.category_id = %s
            AND f.release_year BETWEEN %s AND %s 
"""

sql_list_of_rating = """
        SELECT a.rating AS Rating
            , a.name_rating AS 'Name of Rating'
            , count(*) AS 'Quantity of movies' 
        FROM (
        SELECT f.*
            , CASE 
                WHEN UPPER(f.rating) = 'G' THEN 'General Audiences'
                WHEN UPPER(f.rating) = 'PG' THEN 'Parental Guidance Suggested'
                WHEN UPPER(f.rating) = 'PG-13' THEN 'Parents Strongly Cautioned'
                WHEN UPPER(f.rating) = 'R' THEN 'Restricted'
                WHEN UPPER(f.rating) = 'NC-17' THEN 'Adults Only'
                ELSE 'Others'
            END AS name_rating    
        FROM sakila.film f 
        )a
        GROUP BY a.rating, a.name_rating
        ORDER BY 1
"""
sql_cnt_films_by_rating = """
        SELECT COUNT(DISTINCT f.film_id) as cnt_films
        FROM sakila.film f 
        WHERE f.rating = %s
"""

sql_films_by_rating = """
        SELECT ROW_NUMBER() OVER() AS '№'
        , f.title AS Title
        , f.release_year as 'Release Year'
        , c.name as 'Genre'
FROM sakila.film f 
LEFT JOIN sakila.film_category fc ON f.film_id = fc.film_id
LEFT JOIN sakila.category c ON fc.category_id = c.category_id 
WHERE c.name IS NOT NULL
AND  f.rating = %s
ORDER BY f.release_year DESC
LIMIT %s OFFSET %s
"""