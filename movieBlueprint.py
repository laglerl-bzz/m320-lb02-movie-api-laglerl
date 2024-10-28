"""
Movie Rating API Blueprint
"""

from flask import Blueprint, jsonify, request
from movieDao import MovieDao
from movie import Movie

movie_blueprint = Blueprint("movie_blueprint", __name__)
movie_dao = MovieDao("movie_rating_example.db")


@movie_blueprint.route("/movies", methods=["GET"])
def get_all_movies():
    movies = movie_dao.get_all_movies()
    return jsonify([movie.__dict__ for movie in movies]), 200


@movie_blueprint.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = movie_dao.get_movie(movie_id)
    if movie:
        return jsonify(movie.__dict__), 200
    else:
        return jsonify({"message": "Movie not found"}), 404


@movie_blueprint.route("/movies", methods=["POST"])
def add_movie():
    data = request.get_json()
    new_movie = Movie(None, data["title"], data["rating"])
    movie_dao.add_movie(new_movie)
    return jsonify({"message": "Movie created"}), 201


@movie_blueprint.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    data = request.get_json()
    updated_movie = Movie(movie_id, data["title"], data["rating"])
    if movie_dao.update_movie(updated_movie):
        return jsonify({"message": "Movie updated"}), 200
    else:
        return jsonify({"message": "Movie not found or not updated"}), 404


@movie_blueprint.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    if movie_dao.delete_movie(movie_id):
        return jsonify({"message": "Movie deleted"}), 200
    else:
        return jsonify({"message": "Movie not found or not deleted"}), 404
