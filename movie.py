"""
Movie Model
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Movie:
    movie_id: int
    title: str
    ratings: [int]
