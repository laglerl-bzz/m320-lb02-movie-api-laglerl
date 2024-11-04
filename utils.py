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

    return lambda movie: calculate_average_rating(movie.ratings) > min_rating and title.lower() in movie.title.lower()
