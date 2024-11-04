"""
Movie Model
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Movie:
    """
    Movie Model
    """

    movie_id: int
    title: str
    ratings: [int]
