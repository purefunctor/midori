"""Context object."""
from __future__ import annotations

from enum import Enum

import attr

from .external import ExternalUrl


@attr.s
class Context:
    """Context for an object."""

    external_urls: ExternalUrl = attr.ib()
    href: str = attr.ib()
    type: ContextType = attr.ib()
    uri: str = attr.ib()


class ContextType(Enum):
    """The type of the object in a context."""

    ARTIST = "artist"
    PLAYLIST = "playlist"
    ALBUM = "album"
    SHOW = "show"
