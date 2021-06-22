"""Playlist objects."""
from typing import List, Optional, Union

import attr

from .base import Item
from .episode import Episode
from .external import ExternalUrl
from .member import Image
from .track import Track
from .user import PublicUser


class PlaylistTrack:
    """A playlist track."""

    added_at: str = attr.ib()
    added_by: PublicUser = attr.ib()
    is_local: bool = attr.ib()
    track: Union[Track, Episode] = attr.ib()


class PlaylistTracksRef:
    """Reference to playlist tracks."""

    href: str = attr.ib()
    total: int = attr.ib()


@attr.s
class _Playlist(Item):
    """Base class for playlists."""

    collaborative: bool = attr.ib()
    description: Optional[str] = attr.ib()
    external_urls: ExternalUrl = attr.ib()
    images: List[Image] = attr.ib()
    name: str = attr.ib()
    owner: PublicUser = attr.ib()
    public: Optional[bool] = attr.ib()
    snapshot_id: str = attr.ib()


@attr.s
class SimplifiedPlaylist(_Playlist):
    """A simplified playlist."""

    tracks: PlaylistTracksRef = attr.ib()


@attr.s
class Playlist(_Playlist):
    """A playlist."""

    tracks: List[PlaylistTrack] = attr.ib()
