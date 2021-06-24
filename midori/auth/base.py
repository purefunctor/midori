"""Base class for authentication clients."""
from abc import ABC, abstractmethod
import secrets
import typing as t
from urllib.parse import quote, urlencode

import attr
import httpx

from midori.error import InvalidAuthState


@attr.s
class AuthClient(ABC):
    """Base class for authentication.

    Attributes
    ----------
    client_id
        the client ID of the application
    client_secret
        the client secret of the application
    redirect_uri
        the URL to redirect to after authorization
    scope
        the selected scopes for the application
    """

    client_id: str = attr.field()
    client_secret: str = attr.field()
    redirect_uri: str = attr.field()
    scope: str = attr.field()

    _uri: str = attr.ib(init=False)
    _state: str = attr.ib(init=False)
    _code: t.Optional[str] = attr.ib(init=False, default=None)

    def __attrs_post_init__(self) -> None:
        """Initialize complex non-init fields."""
        self._uri, self._state = self._create_auth_url()

    def _create_auth_url(self) -> t.Tuple[str, str]:
        state = secrets.token_urlsafe()

        parameters = urlencode(
            {
                "client_id": self.client_id,
                "response_type": "code",
                "redirect_uri": self.redirect_uri,
                "scope": quote(self.scope),
                "state": state,
            }
        )

        url = f"https://accounts.spotify.com/authorize?{parameters}"

        return url, state

    def _set_code_state(self, code: str, state: str) -> None:
        """Set the code and state."""
        if self._state != state:
            raise InvalidAuthState(self._state, state)

        self._code = code

    @abstractmethod
    def _request_token(self) -> None:
        """Request a token from the API."""

    def request_token(self) -> t.Mapping:
        """Request a token from the API."""
        self._request_token()

        with httpx.Client() as client:
            response = client.post(
                "https://accounts.spotify.com/api/token",
                data={
                    "grant_type": "authorization_code",
                    "code": self._code,
                    "redirect_uri": self.redirect_uri,
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                },
            )
            return response.json()
