"""Play history."""
import attr

from .context import Context
from .track import SimplifiedTrack


@attr.s
class PlayHistory:
    """Play history of a track."""

    context: Context = attr.ib()
    played_at: str = attr.ib()
    track: SimplifiedTrack = attr.ib()
