"""Recommendations object."""
from __future__ import annotations

from enum import Enum
from typing import List, Optional

import attr

from .track import SimplifiedTrack


@attr.s
class RecommendationSeed:
    """Seed for recommendations."""

    afterFilteringSize: int = attr.ib()
    afterRelinkingSize: int = attr.ib()
    href: Optional[str] = attr.ib()
    id: str = attr.ib()
    initialPoolSize: int = attr.ib()
    type: str = attr.ib()


@attr.s
class Recommendations:
    """Recommendations for the user."""

    seeds: List[RecommendationSeed] = attr.ib()
    tracks: List[SimplifiedTrack] = attr.ib()


class SeedId(Enum):
    """Identification for the seeds."""

    ARTISTS = "seed_artists"
    TRACKS = "seed_tracks"
    GENRES = "seed_genres"


class SeedType(Enum):
    """The type of a seed."""

    ARTIST = "artist"
    TRACK = "track"
    GENRE = "genre"
