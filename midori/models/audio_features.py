"""Audio features."""
import attr


@attr.s
class _AudioFeatures:
    """Base class for audio features."""

    acousticness: float = attr.ib()
    danceability: float = attr.ib()
    duration_ms: int = attr.ib()
    energy: float = attr.ib()
    instrumentalness: float = attr.ib()
    key: int = attr.ib()
    liveness: float = attr.ib()
    loudness: float = attr.ib()
    mode: int = attr.ib()
    speechiness: float = attr.ib()
    tempo: float = attr.ib()
    time_signature: int = attr.ib()
    valence: float = attr.ib()


@attr.s
class AudioFeatures(_AudioFeatures):
    """Audio features of a track."""

    analysis_url: str = attr.ib()
    id: str = attr.ib()
    track_href: str = attr.ib()
    type: str = attr.ib()
    uri: str = attr.ib()
