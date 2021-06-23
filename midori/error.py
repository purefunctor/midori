"""Exceptions for the library."""


class MidoriError(Exception):
    """Base exception."""


class InvalidAuthState(MidoriError):
    """Invalid authorization state."""

    def __init__(self, previous: str, current: str) -> None:
        self.previous = previous
        self.current = current
        super().__init__(previous, current)

    def __str__(self) -> str:  # noqa: D105
        return f"Invalid state: '{self.previous}' != '{self.current}'"


class InvalidRedirectUri(MidoriError):
    """Invalid redirect uri for the local server."""
