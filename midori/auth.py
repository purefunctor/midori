"""Implements basic authorization flows for the Spotify API."""
from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
import secrets
import typing as t
from urllib.parse import parse_qs, quote, urlencode, urlparse
import webbrowser

import attr
import httpx

from midori.error import InvalidAuthState, InvalidRedirectUri


CodeStateCallback = t.Callable[[str, str], None]


class AuthRequestHandler(BaseHTTPRequestHandler):
    """Default request handler for the project.

    Attributes
    ----------
    _callback
        a callback function that receives the `code` and `state`
    """

    _callback: t.Optional[CodeStateCallback] = None

    def do_GET(self) -> None:
        """Handle GET requests."""
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self._write("<html><body><script>window.close()</script></body></html>")

        if self._callback is not None:
            self._callback(*_parse_code_state(self.path))

    def _write(self, text: str) -> None:
        self.wfile.write(text.encode("utf-8"))

    def log_message(self, *args: t.Any) -> None:
        """Handle logging messages."""
        return None

    @classmethod
    @contextmanager
    def hook_callback(
        cls, callback: CodeStateCallback
    ) -> t.Iterator[t.Type[AuthRequestHandler]]:
        """Temporarily hook a callback."""
        try:
            cls._callback = callback
            yield cls
        finally:
            cls._callback = None


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
        self._state = state

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


class LocalAuthClient(AuthClient):
    """An authentication client that uses a local server."""

    def _parse_redirect(self) -> t.Tuple[str, int]:
        redirect = urlparse(self.redirect_uri)

        if redirect.hostname is None:
            raise InvalidRedirectUri(f"'{self.redirect_uri}' has no hostname")
        elif redirect.port is None:
            raise InvalidRedirectUri(f"'{self.redirect_uri}' has no port")
        else:
            host = redirect.hostname
            port = redirect.port

        return (host, port)

    def _open_server(self, host: str, port: int) -> HTTPServer:
        return HTTPServer((host, port), AuthRequestHandler)

    def _request_token(self) -> None:
        """Request a token from the API using a browser."""
        host, port = self._parse_redirect()
        with AuthRequestHandler.hook_callback(self._set_code_state):
            server = self._open_server(host, port)
            webbrowser.open(self._uri)
            server.handle_request()


class ConsoleAuthClient(AuthClient):
    """An authentication client that uses the console."""

    def _request_token(self) -> None:
        """Request a token from the API using the console."""
        print("Visit the following URL:", self._uri)
        url = input("Enter the URL you were redirected to: ")
        self._set_code_state(*_parse_code_state(url))


def _parse_code_state(url: str) -> t.Tuple[str, str]:
    qs = parse_qs(urlparse(url).query)
    return qs["code"][0], qs["state"][0]
