"""
Movie Data Access Object
"""

import sqlite3
from movie import Movie

class MovieDao:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()  # Ensure the table is created

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS movies""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER PRIMARY KEY,
                title TEXT,
                ratings TEXT)"""  # Store ratings as a text field
        )
        self.conn.commit()

    def add_movie(self, movie):
        ratings_str = ','.join(map(str, movie.ratings))  # Convert list of ratings to a string
        self.cursor.execute(
            "INSERT INTO movies (title, ratings) VALUES (?, ?)",
            (movie.title, ratings_str),
        )
        self.conn.commit()

    def get_movie(self, movie_id):
        self.cursor.execute(
            "SELECT * FROM movies WHERE movie_id = ?",
            (movie_id,),
        )
        row = self.cursor.fetchone()
        if row:
            ratings = list(map(int, row[2].split(',')))  # Convert ratings string back to a list of integers
            return Movie(row[0], row[1], ratings)
        return None

    def get_all_movies(self):
        self.cursor.execute("SELECT * FROM movies")
        rows = self.cursor.fetchall()
        movies = []
        for row in rows:
            ratings = list(map(int, row[2].split(',')))  # Convert ratings string back to a list of integers
            movies.append(Movie(row[0], row[1], ratings))
        return movies

    def update_movie(self, movie):
        ratings_str = ','.join(map(str, movie.ratings))  # Convert list of ratings to a string
        self.cursor.execute(
            "UPDATE movies SET title = ?, ratings = ? WHERE movie_id = ?",
            (movie.title, ratings_str, movie.movie_id),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def delete_movie(self, movie_id):
        self.cursor.execute(
            "DELETE FROM movies WHERE movie_id = ?",
            (movie_id,),
        )
        if self.cursor.rowcount > 0:
            self.conn.commit()
            return True
        return False

    def close(self):
        self.conn.close()
