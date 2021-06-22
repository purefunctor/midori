"""Track objects."""
from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

import attr

from .artist import Artist, SimplifiedArtist
from .audio_features import _AudioFeatures
from .base import Item
from .external import ExternalId, ExternalUrl
from .restriction import TrackRestriction

if TYPE_CHECKING:
    from .album import SimplifiedAlbum


@attr.s
class _Track(Item):
    """Base class for tracks."""

    available_markets: Optional[List[str]] = attr.ib()
    disc_number: int = attr.ib()
    duration_ms: int = attr.ib()
    explicit: bool = attr.ib()
    external_urls: ExternalUrl = attr.ib()
    is_local: bool = attr.ib()
    is_playable: Optional[bool] = attr.ib()
    name: str = attr.ib()
    preview_url: str = attr.ib()
    restrictions: Optional[TrackRestriction] = attr.ib()
    track_number: int = attr.ib()


@attr.s
class SimplifiedTrack(_Track):
    """A simple track."""

    artists: Optional[List[SimplifiedArtist]] = attr.ib()


@attr.s
class Track:
    """A track."""  # TODO: Add documentation

    album: SimplifiedAlbum = attr.ib()
    artists: List[Artist] = attr.ib()
    external_ids: ExternalId = attr.ib()
    popularity: int = attr.ib()


@attr.s
class LinkedTrack(Item):
    """A linked track."""

    external_urls: ExternalUrl = attr.ib()


@attr.s
class SavedTrack:
    """A saved track."""

    added_at: str = attr.ib()
    track: Track = attr.ib()


@attr.s
class TuneableTrack(_AudioFeatures):
    """A tuneable track."""

    popularity: int = attr.ib()
