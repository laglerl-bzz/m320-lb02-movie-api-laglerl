"""
Movie Rating API
"""
from flask import Flask

from movieBlueprint import movie_blueprint

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.register_blueprint(movie_blueprint)


def generate_testdata():
    from movie import Movie
    from movieDao import MovieDao

    movie_dao = MovieDao("movie_rating_example.db")

    # Generate movies
    movie_dao.create_table()
    movie_dao.add_movie(Movie(1, "Inception", [1, 2, 1]))
    movie_dao.add_movie(Movie(2, "The Matrix", [4, 5, 4]))
    movie_dao.add_movie(Movie(3, "Interstellar", [5, 5, 5]))
    movie_dao.add_movie(Movie(4, "The Godfather", [5, 4, 5]))

    movie_dao.close()


if __name__ == "__main__":
    generate_testdata()
    app.run(debug=True)
