"""Album objects."""
from __future__ import annotations

from enum import Enum
from typing import List, Optional, TYPE_CHECKING

import attr

from .artist import SimplifiedArtist
from .base import Item
from .copyright import Copyright
from .external import ExternalId, ExternalUrl
from .member import Image
from .restriction import AlbumRestriction

if TYPE_CHECKING:
    from .track import SimplifiedTrack


@attr.s
class _Album(Item):
    """Base class for albums."""

    album_type: AlbumType = attr.ib()
    artists: List[SimplifiedArtist] = attr.ib()
    available_markets: Optional[List[str]] = attr.ib()
    external_urls: ExternalUrl = attr.ib()
    images: List[Image] = attr.ib()
    is_playable: Optional[bool] = attr.ib()
    name: str = attr.ib()
    release_date: str = attr.ib()
    release_date_precision: str = attr.ib()
    restrictions: AlbumRestriction = attr.ib()
    total_tracks: int = attr.ib()


@attr.s
class SimplifiedAlbum(_Album):
    """A simple album."""

    album_group: Optional[AlbumGroup] = attr.ib()


@attr.s
class Album(_Album):
    """An album."""

    copyrights: List[Copyright] = attr.ib()
    external_ids: ExternalId = attr.ib()
    genres: List[str] = attr.ib()
    label: str = attr.ib()
    popularity: int = attr.ib()
    tracks: List[SimplifiedTrack] = attr.ib()


@attr.s
class SavedAlbum:
    """A saved album."""

    added_at: str = attr.ib()
    album: Album = attr.ib()


class AlbumGroup(Enum):
    """The relationship between an artist and album."""

    ALBUM = "album"
    SINGLE = "single"
    COMPILATION = "compilation"
    APPEARS_ON = "appears_on"


class AlbumType(Enum):
    """The type of an album."""

    ALBUM = "album"
    SINGLE = "single"
    COMPILATION = "compilation"
    APPEARS_ON = "appears_on"
