"""
Movie Data Access Object
"""

import sqlite3
from movie import Movie

class MovieDao:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS movies""")
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS movies (
                movie_id INTEGER PRIMARY KEY,
                title TEXT,
                rating INTEGER)"""
        )
        self.conn.commit()

    def add_movie(self, movie):
        self.cursor.execute(
            "INSERT INTO movies (title, rating) VALUES (?, ?)",
            (movie.title, movie.rating),
        )
        self.conn.commit()

    def get_movie(self, movie_id):
        self.cursor.execute(
            "SELECT * FROM movies WHERE movie_id = ?",
            (movie_id,),
        )
        row = self.cursor.fetchone()
        if row:
            return Movie(row[0], row[1], row[2])
        return None

    def get_all_movies(self):
        self.cursor.execute("SELECT * FROM movies")
        rows = self.cursor.fetchall()
        movies = [Movie(row[0], row[1], row[2]) for row in rows]
        return movies

    def update_movie(self, movie):
        self.cursor.execute(
            "UPDATE movies SET title = ?, rating = ? WHERE movie_id = ?",
            (movie.title, movie.rating, movie.movie_id),
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