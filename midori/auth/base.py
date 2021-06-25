"""Base class for authentication clients."""
from abc import abstractmethod
import base64
from contextlib import contextmanager
import secrets
import typing as t
from urllib.parse import parse_qs, quote, urlencode, urlparse

import attr
import httpx

from midori.error import InvalidAuthState


class AuthInfo(t.TypedDict):
    """Contains info needed for authorization."""

    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: str


class _AuthClient(t.Protocol):
    """An abstract blueprint for authentication clients.

    Attributes
    ----------
    _uri
        the url to be visited for authentication
    _state
        an invariant during the authentication flow
    _code
        an authorization code to exchange for an access token
    """

    _uri: str
    _state: str
    _code: str

    def _consume_callback_url(self, url: str) -> None:
        """Parse, validate, and consume the callback URL."""
        parameters = parse_qs(urlparse(url).query)

        code, = parameters["code"]
        state, = parameters["state"]

        if state != self._state:
            raise InvalidAuthState(self._state, state)

        self._code = code

    @abstractmethod
    def _visit_auth_url(self) -> None:
        """Visit the authentication url."""

    @abstractmethod
    def request_token(self) -> AuthInfo:
        """Request a token from the API."""

    @abstractmethod
    def refresh_token(self, *, refresh_token: str) -> AuthInfo:
        """Refresh a token from the API."""


@attr.s
class AuthClient(_AuthClient):
    """Base class for synchronous authentication.

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

    client_id: str = attr.ib(kw_only=True)
    client_secret: str = attr.ib(kw_only=True)
    redirect_uri: str = attr.ib(kw_only=True)
    scope: str = attr.ib(kw_only=True)

    _client: t.Optional[httpx.Client] = attr.ib(kw_only=True, default=None)

    _uri: str = attr.ib(init=False)
    _state: str = attr.ib(init=False)
    _code: str = attr.ib(init=False, default="")

    def __attrs_post_init__(self) -> None:
        """Initialize complex non-init fields."""
        self._state = secrets.token_urlsafe()

        parameters = urlencode(
            {
                "client_id": self.client_id,
                "response_type": "code",
                "redirect_uri": self.redirect_uri,
                "scope": quote(self.scope),
                "state": self._state,
            }
        )

        self._uri = f"https://accounts.spotify.com/authorize?{parameters}"

    @contextmanager
    def _borrow_client(self) -> t.Iterator[httpx.Client]:
        """Temporarily create a client or use the provided instance."""
        client = httpx.Client()
        try:
            if self._client is None:
                yield client
            else:
                yield self._client
        finally:
            client.close()

    def _post_api_token(self, **data: t.Any) -> AuthInfo:
        """Create a POST request to the accounts service."""
        client_pair = f"{self.client_id}:{self.client_secret}".encode()
        authorization = base64.urlsafe_b64encode(client_pair).decode()

        with self._borrow_client() as client:
            response = client.post(
                "https://accounts.spotify.com/api/token",
                data=data,
                headers={
                    "Authorization": f"Basic {authorization}",
                }
            )

        return response.json()

    def request_token(self) -> AuthInfo:
        """Request a token from the API."""
        self._visit_auth_url()

        return self._post_api_token(
            grant_type="authorization_code",
            code=self._code,
            redirect_uri=self.redirect_uri,
        )

    def refresh_token(self, *, refresh_token: str) -> AuthInfo:
        """Refresh a token from the API."""
        auth_info = self._post_api_token(
            grant_type="refresh_token",
            refresh_token=refresh_token,
        )

        auth_info["refresh_token"] = refresh_token

        return auth_info
