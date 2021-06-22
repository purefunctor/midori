"""Currently playing."""
from typing import Optional, Union

import attr

from .context import Context
from .device import Device
from .episode import Episode
from .track import Track


@attr.s
class Disallows:
    """Disallowed actions."""

    interrupting_playback: bool = attr.ib()
    pausing: bool = attr.ib()
    resuming: bool = attr.ib()
    seeking: bool = attr.ib()
    skipping_next: bool = attr.ib()
    skipping_prev: bool = attr.ib()
    toggling_repeat_context: bool = attr.ib()
    toggling_repeat_track: bool = attr.ib()
    toggling_shuffle: bool = attr.ib()
    transferring_playback: bool = attr.ib()


@attr.s
class CurrentlyPlayingContext:
    """Context for the currently playing track."""

    actions: Disallows = attr.ib()
    context: Context = attr.ib()
    currently_playing_type: str = attr.ib()  # TODO: enum
    device: Device = attr.ib()
    is_playing: bool = attr.ib()
    item: Optional[Union[Track, Episode]] = attr.ib()
    progress_ms: Optional[int] = attr.ib()
    repeat_state: str = attr.ib()  # TODO: enum
    shuffle_state: str = attr.ib()
    timestamp: int = attr.ib()


@attr.s
class CurrentlyPlaying:
    """The currently playing track."""

    context: Context = attr.ib()
    currently_playing_type: str = attr.ib()  # TODO: enum
    is_playing: bool = attr.ib()
    item: Optional[Union[Track, Episode]] = attr.ib()
    progress_ms: Optional[int] = attr.ib()
    timestamp: int = attr.ib()
