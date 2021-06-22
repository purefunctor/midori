"""Error object."""
from __future__ import annotations

from enum import Enum

import attr


@attr.s
class Error:
    """Errors raised by the API."""

    message: str = attr.ib()
    status: int = attr.ib()


@attr.s
class PlayerError(Error):
    """Errors raised by the player API."""

    reason: PlayerErrorReason = attr.ib()


class PlayerErrorReason(Enum):
    """The reason for player error."""

    NO_PREV_TRACK = "NO_PREV_TRACK"
    NO_NEXT_TRACK = "NO_NEXT_TRACK"
    NO_SPECIFIC_TRACK = "NO_SPECIFIC_TRACK"
    ALREADY_PAUSED = "ALREADY_PAUSED"
    NOT_PAUSED = "NOT_PAUSED"
    NOT_PLAYING_LOCALLY = "NOT_PLAYING_LOCALLY"
    NOT_PLAYING_TRACK = "NOT_PLAYING_TRACK"
    NOT_PLAYING_CONTEXT = "NOT_PLAYING_CONTEXT"
    ENDLESS_CONTEXT = "ENDLESS_CONTEXT"
    CONTEXT_DISALLOW = "CONTEXT_DISALLOW"
    ALREADY_PLAYING = "ALREADY_PLAYING"
    RATE_LIMITED = "RATE_LIMITED"
    REMOTE_CONTROL_DISALLOW = "REMOTE_CONTROL_DISALLOW"
    DEVICE_NOT_CONTROLLABLE = "DEVICE_NOT_CONTROLLABLE"
    VOLUME_CONTROL_DISALLOW = "VOLUME_CONTROL_DISALLOW"
    NO_ACTIVE_DEVICE = "NO_ACTIVE_DEVICE"
    PREMIUM_REQUIRED = "PREMIUM_REQUIRED"
    UNKNOWN = "UNKNOWN"
