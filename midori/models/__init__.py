"""Models defined in the Spotify API."""

from .album import Album, SimplifiedAlbum  # noqa: F401
from .artist import (  # noqa: F401
    Artist,
    SimplifiedArtist,
)
from .audio_features import AudioFeatures  # noqa: F401
from .category import Category  # noqa: F401
from .context import Context, ContextType  # noqa: F401
from .copyright import Copyright, CopyrightType  # noqa: F401
from .currently_playing import (  # noqa: F401
    CurrentlyPlaying,
    CurrentlyPlayingContext,
    Disallows,
)
from .device import Device, Devices, DeviceType  # noqa: F401
from .episode import (  # noqa: F401
    Episode,
    ResumePoint,
    SavedEpisode,
    SimplifiedEpisode,
)
from .error import Error, PlayerError, PlayerErrorReason  # noqa: F401
from .external import ExternalId, ExternalUrl  # noqa: F401
from .member import Followers, Image  # noqa: F401
from .paging import Cursor, CursorPaging, Paging  # noqa: F401
from .play_history import PlayHistory  # noqa: F401
from .playlist import (  # noqa: F401
    Playlist,
    PlaylistTrack,
    PlaylistTracksRef,
    SimplifiedPlaylist,
)
from .recommendations import (  # noqa: F401
    Recommendations,
    RecommendationSeed,
    SeedId,
    SeedType,
)
from .restriction import (  # noqa: F401
    AlbumRestriction,
    EpisodeRestriction,
    RestrictionReason,
    TrackRestriction,
)
from .show import (  # noqa: F401
    SavedShow,
    Show,
    SimplifiedShow,
)
from .track import (  # noqa: F401
    LinkedTrack,
    SavedTrack,
    SimplifiedTrack,
    Track,
    TuneableTrack,
)
from .user import (  # noqa: F401
    ExplicitContentSettings,
    PrivateUser,
    PublicUser,
    UserProductType,
)
