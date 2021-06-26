"""Common types and utilities."""
import typing as t


class AuthInfo(t.TypedDict):
    """Contains info needed for authorization."""

    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: str
