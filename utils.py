"""
Dieses Modul enthält Hilfsfunktionen, die in der main.py-Datei verwendet werden.
"""


def calculate_average_rating_algo(ratings):
    """
    Berechnet den Durchschnitt der Bewertungen mit einem Algorithmus.

    :param ratings: Liste von Integer-Bewertungen
    :return: Durchschnitt der Bewertungen oder None, wenn die Liste leer ist
    """
    if not ratings:
        return None
    total = sum(ratings)
    average = total / len(ratings)
    return round(average, 2)


def calculate_average_rating(ratings):
    """
    Berechnet den Durchschnitt der Bewertungen.

    :param ratings: Liste von Integer-Bewertungen
    :return: Durchschnitt der Bewertungen oder None, wenn die Liste leer ist
    """
    average_rating = lambda movie: sum(ratings) / len(ratings)
    return round(average_rating(ratings), 2)


def apply_function_to_movies(movies, func):
    """
    Wendet eine gegebene Funktion auf eine Liste von Filmen an.

    :param movies: Liste von Movie-Objekten
    :param func: Funktion, die auf jedes Movie-Objekt angewendet wird
    :return: Liste der Ergebnisse
    """
    return [func(movie) for movie in movies]


def create_rating_filter(min_rating, title):
    """
    Erstellt eine Filterfunktion, die überprüft, ob alle Bewertungen eines Films
    über einem bestimmten Mindestwert liegen.

    :param title: Titel des Films
    :param min_rating: Der Mindestwert, den jede Bewertung eines Films erfüllen muss
    :return: Eine Funktion, die ein Movie-Objekt als Argument akzeptiert und
             True zurückgibt, wenn alle Bewertungen des Films den Mindestwert erfüllen,
             andernfalls False
    """

    return (
        lambda movie: calculate_average_rating(movie.ratings) > min_rating
        and title.lower() in movie.title.lower()
    )


def filter_valid_ratings(ratings):
    """
    Filtert ungültige Bewertungen aus.

    :param ratings: Liste von Integer-Bewertungen
    :return: Liste von gültigen Bewertungen
    """
    return [rating for rating in ratings if rating is not None]


def calculate_average(ratings):
    """
    Berechnet den Durchschnitt der gültigen Bewertungen.

    :param ratings: Liste von Integer-Bewertungen
    :return: Durchschnitt der gültigen Bewertungen oder None
    """
    valid_ratings = filter_valid_ratings(ratings)
    return calculate_average_rating(valid_ratings)


def get_highest_rating_for_movie(movie):
    """
    Berechnet die höchste Bewertung für einen Film.

    :param movie: Filmobjekt
    :return: Höchste Bewertung oder None
    """

    find_highest_rating = lambda ratings: max(ratings) if ratings else None
    valid_ratings = filter_valid_ratings(movie.ratings)
    return find_highest_rating(valid_ratings)
