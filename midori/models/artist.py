"""Artist objects."""
from typing import List

import attr

from .base import Item
from .external import ExternalUrl
from .member import Image


@attr.s
class _Artist(Item):
    """Base class for artists."""

    external_urls: ExternalUrl = attr.ib()
    name: str = attr.ib()


@attr.s
class SimplifiedArtist(_Artist):
    """A simple artist."""


@attr.s
class Artist(_Artist):
    """An artist."""

    images: List[Image] = attr.ib()
    popularity: int = attr.ib()
