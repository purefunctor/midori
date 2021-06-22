"""Show objects."""
from __future__ import annotations

from typing import List, TYPE_CHECKING

import attr

from .base import Item
from .copyright import Copyright
from .external import ExternalUrl
from .member import Image

if TYPE_CHECKING:
    from .episode import SimplifiedEpisode


@attr.s
class _Show(Item):
    """Base class for shows."""

    available_markets: List[str] = attr.ib()
    copyrights: List[Copyright] = attr.ib()
    description: str = attr.ib()
    explicit: bool = attr.ib()
    external_urls: ExternalUrl = attr.ib()
    html_description: str = attr.ib()
    images: List[Image] = attr.ib()
    is_externally_hosted: str = attr.ib()
    languages: List[str] = attr.ib()
    media_type: str = attr.ib()
    name: str = attr.ib()
    publisher: str = attr.ib()


@attr.s
class SimplifiedShow(_Show):
    """A simplified show."""


@attr.s
class Show(_Show):
    """A simplified show."""

    episodes: List[SimplifiedEpisode] = attr.ib()


@attr.s
class SavedShow:
    """A saved show."""

    added_at: str = attr.ib()
    show: SimplifiedShow = attr.ib()
