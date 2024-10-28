"""
Movie Model
"""

from dataclasses import dataclass


@dataclass
class Movie:
    movie_id: int
    title: str
    rating: int  # Assuming rating is on a scale of 1-5