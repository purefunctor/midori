"""Implements OAuth2 flows for the Spotify API."""
from midori.auth.base import AuthClient  # noqa: F401
from midori.auth.common import AuthInfo  # noqa: F401
from midori.auth.console import ConsoleAuthClient  # noqa: F401
from midori.auth.local import AuthRequestHandler, LocalAuthClient  # noqa: F401
