"""
Movie Rating API Blueprint
"""

from functools import reduce

from flask import Blueprint, jsonify, request
from movie_dao import MovieDao
from movie import Movie
from utils import (
    calculate_average_rating,
    apply_function_to_movies,
    create_rating_filter,
    get_highest_rating_for_movie,
)

movie_blueprint = Blueprint("movie_blueprint", __name__)
movie_dao = MovieDao("movie_rating_example.db")


@movie_blueprint.route("/", methods=["GET"])
def list_routes():
    """
    List all available routes.
    :return:
    """
    routes = {
        "GET": [
            "/movies - Get all movies",
            "/movies/average_ratings_v1 - Get average ratings (v1)",
            "/movies/average_ratings_v2 - Get average ratings (v2)",
            "/movies/filter_v1?min_rating=<value>&title=<value> - Filter movies (v1)",
            "/movies/filter_v2?min_rating=<value> - Filter movies (v2)",
            "/movies/overall_average?min_rating=<value> - Get overall average rating",
            "/movies/sorted - Get sorted movies by average rating",
            "/movies/<int:movie_id> - Get a movie by ID",
            "/movies/<int:movie_id>/highest_rating - Get highest rating for a movie",
        ],
        "POST": ["/movies - Add a new movie"],
        "PUT": ["/movies/<int:movie_id> - Update a movie"],
        "DELETE": ["/movies/<int:movie_id> - Delete a movie"],
    }
    return jsonify(routes), 200


@movie_blueprint.route("/movies", methods=["GET"])
def get_all_movies():
    """
    Get all movies.
    :return:
    """
    movies = movie_dao.get_all_movies()
    return jsonify([movie.__dict__ for movie in movies]), 200


@movie_blueprint.route("/movies/average_ratings_v1", methods=["GET"])
def average_ratings_v1():
    """
    Get average ratings (v1).
    :return:
    """
    movies = movie_dao.get_all_movies()
    average_rating_func = calculate_average_rating
    average_ratings = apply_function_to_movies(movies, average_rating_func)

    return jsonify({"average_ratings": average_ratings}), 200


@movie_blueprint.route("/movies/average_ratings_v2", methods=["GET"])
def average_ratings_v2():
    """
    Get average ratings (v2).
    :return:
    """
    movies = movie_dao.get_all_movies()
    average_ratings = list(
        map(calculate_average_rating, [movie.ratings for movie in movies])
    )

    return jsonify({"average_ratings": average_ratings}), 200


@movie_blueprint.route("/movies/filter_v1", methods=["GET"])
def filter_movies_v1():
    """
    Filter movies (v1).
    :return:
    """
    min_rating = int(request.args.get("min_rating", 0))
    title = int(request.args.get("title", ""))

    filter_func = create_rating_filter(min_rating, title)

    filtered_movies = [
        movie for movie in movie_dao.get_all_movies() if filter_func(movie)
    ]
    return jsonify([movie.__dict__ for movie in filtered_movies]), 200


@movie_blueprint.route("/movies/filter_v2", methods=["GET"])
def filter_movies_v2():
    """
    Filter movies (v2).
    :return:
    """
    min_rating = request.args.get("min_rating", type=float, default=3.0)
    movies = movie_dao.get_all_movies()
    filtered_movies = list(
        filter(
            lambda movie: calculate_average_rating(movie.ratings) > min_rating, movies
        )
    )

    filtered_titles = list(map(lambda movie: movie.title, filtered_movies))

    total_average_rating = reduce(
        lambda acc, movie: acc + calculate_average_rating(movie.ratings),
        filtered_movies,
        0,
    )
    return jsonify(filtered_titles, total_average_rating), 200


@movie_blueprint.route("/movies/overall_average", methods=["GET"])
def overall_average():
    """
    Get overall average rating.
    :return:
    """
    min_rating = request.args.get("min_rating", type=float, default=3.0)
    movies = movie_dao.get_all_movies()

    filtered_movies = list(
        filter(lambda movie: len(movie.ratings) >= min_rating, movies)
    )
    average_ratings = list(
        map(calculate_average_rating, [movie.ratings for movie in filtered_movies])
    )
    overall_average_movies = (
        reduce(lambda acc, x: acc + x, average_ratings) / len(average_ratings)
        if average_ratings
        else 0
    )

    return jsonify(overall_average_movies), 200


def sort_movies_by_average_rating(movies):
    """
    Sort movies by average rating.
    :param movies:
    :return:
    """
    return sorted(
        movies, key=lambda movie: calculate_average_rating(movie.ratings), reverse=True
    )


@movie_blueprint.route("/movies/sorted", methods=["GET"])
def get_sorted_movies():
    """
    Get sorted movies by average rating.
    :return:
    """
    movies = movie_dao.get_all_movies()
    sorted_movies = sort_movies_by_average_rating(movies)
    return jsonify([movie.__dict__ for movie in sorted_movies]), 200


@movie_blueprint.route("/movies/<int:movie_id>", methods=["GET"])
def get_movie(movie_id):
    """
    Get a movie by ID.
    :param movie_id:
    :return:
    """
    movie = movie_dao.get_movie(movie_id)
    if movie:
        average_rating = calculate_average_rating(movie.ratings)
        return jsonify({"movie": movie.__dict__, "average_rating": average_rating}), 200

    return jsonify({"message": "Movie not found"}), 404


def create_movie(data):
    """
    Create a movie object from the given data.
    :param data:
    :return:
    """
    return Movie(None, data["title"], data["ratings"])


@movie_blueprint.route("/movies", methods=["POST"])
def add_movie():
    """
    Add a new movie.
    :return:
    """
    data = request.get_json()
    new_movie = create_movie(data)
    movie_dao.add_movie(new_movie)
    return jsonify({"message": "Movie created"}), 201


@movie_blueprint.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    """
    Update a movie.
    :param movie_id:
    :return:
    """
    data = request.get_json()
    updated_movie = Movie(movie_id, data["title"], data["ratings"])
    if movie_dao.update_movie(updated_movie):
        return jsonify({"message": "Movie updated"}), 200

    return jsonify({"message": "Movie not found or not updated"}), 404


def create_delete_response(deleted):
    """Helper function to create the appropriate response for movie deletion."""
    if deleted:
        return jsonify({"message": "Movie deleted"}), 200

    return jsonify({"message": "Movie not found or not deleted"}), 404


@movie_blueprint.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    """
    Delete a movie.
    :param movie_id:
    :return:
    """
    deleted = movie_dao.delete_movie(movie_id)
    return create_delete_response(deleted)


@movie_blueprint.route("/movies/<int:movie_id>/highest_rating", methods=["GET"])
def highest_rating_endpoint(movie_id):
    """
    Get highest rating for a movie.
    :param movie_id:
    :return:
    """
    movie = movie_dao.get_movie(movie_id)
    if movie:
        highest_rating = get_highest_rating_for_movie(movie)
        return jsonify({"title": movie.title, "highest_rating": highest_rating}), 200

    return jsonify({"message": "Movie not found"}), 404
