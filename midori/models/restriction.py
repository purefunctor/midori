"""Restriction objects."""
from __future__ import annotations

from enum import Enum

import attr


@attr.s
class _Restriction:
    """Base restriction object."""

    reason: RestrictionReason = attr.ib()
    f: str = attr.ib()


class RestrictionReason(Enum):
    """Reason for the restriction."""

    MARKET = "market"
    PRODUCT = "product"
    EXPLICIT = "explicit"


class AlbumRestriction(_Restriction):
    """Restriction for an album."""


class EpisodeRestriction(_Restriction):
    """Restriction for an episode."""


class TrackRestriction(_Restriction):
    """Restriction for a track."""
