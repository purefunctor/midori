"""Episode object."""
from __future__ import annotations

from typing import List, Optional, TYPE_CHECKING

import attr

from .base import Item
from .external import ExternalUrl
from .member import Image
from .restriction import EpisodeRestriction

if TYPE_CHECKING:
    from .show import SimplifiedShow


@attr.s
class ResumePoint:
    """A resume point."""

    fully_played: bool = attr.ib()
    resume_position_ms: int = attr.ib()


@attr.s
class _Episode(Item):
    """Base class for episodes."""

    audio_preview_url: Optional[str] = attr.ib()
    description: str = attr.ib()
    duration_ms: int = attr.ib()
    explicit: bool = attr.ib()
    external_urls: ExternalUrl = attr.ib()
    html_description: str = attr.ib()
    images: List[Image] = attr.ib()
    is_externally_hosted: bool = attr.ib()
    is_playable: Optional[bool] = attr.ib()
    languages: List[str] = attr.ib()
    name: str = attr.ib()
    release_date: str = attr.ib()
    release_date_precision: str = attr.ib()
    restrictions: EpisodeRestriction = attr.ib()
    resume_point: ResumePoint = attr.ib()


@attr.s
class SimplifiedEpisode(_Episode):
    """A simplified episode."""


@attr.s
class Episode(_Episode):
    """An episode."""

    show: SimplifiedShow = attr.ib()


@attr.s
class SavedEpisode:
    """A saved episode."""

    added_at: str = attr.ib()
    episode: Episode = attr.ib()
