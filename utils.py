def calculate_average_rating(ratings):
    """
    Berechnet den Durchschnitt der Bewertungen.

    :param ratings: Liste von Integer-Bewertungen
    :return: Durchschnitt der Bewertungen oder None, wenn die Liste leer ist
    """
    if not ratings:
        return None
    return round(sum(ratings) / len(ratings), 2)


def apply_function_to_movies(movies, func):
    """
    Wendet eine gegebene Funktion auf eine Liste von Filmen an.

    :param movies: Liste von Movie-Objekten
    :param func: Funktion, die auf jedes Movie-Objekt angewendet wird
    :return: Liste der Ergebnisse
    """
    return [func(movie) for movie in movies]


def create_rating_filter(min_rating):
    """
    Erstellt eine Filterfunktion, die überprüft, ob alle Bewertungen eines Films
    über einem bestimmten Mindestwert liegen.

    :param min_rating: Der Mindestwert, den jede Bewertung eines Films erfüllen muss
    :return: Eine Funktion, die ein Movie-Objekt als Argument akzeptiert und
             True zurückgibt, wenn alle Bewertungen des Films den Mindestwert erfüllen,
             andernfalls False
    """
    def filter_movie(movie):
        return any(r > min_rating for r in movie.ratings)

    return filter_movie
