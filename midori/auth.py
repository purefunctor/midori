"""Implements basic authorization flows for the Spotify API."""
from __future__ import annotations

from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
import typing as t
from urllib.parse import parse_qs, urlparse
import webbrowser

from authlib.integrations.httpx_client import OAuth2Client

from midori.error import InvalidAuthState


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

        qs = parse_qs(urlparse(self.path).query)
        if self._callback is not None:
            self._callback(qs["code"][0], qs["state"][0])

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


class AuthClient:
    """Code authentication client and manager.

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

    def __init__(
        self, *, client_id: str, client_secret: str, redirect_uri: str, scope: str
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope

        self._client = OAuth2Client(
            client_id=client_id,
            client_secret=client_secret,
            scope=scope,
            redirect_uri=redirect_uri,
        )

        self._uri, self._state = self._client.create_authorization_url(
            "https://accounts.spotify.com/authorize",
        )

        self._code: t.Optional[str] = None

    def _set_code_state(self, code: str, state: str) -> None:
        """Set the code and state."""
        if self._state != state:
            raise InvalidAuthState(self._state, state)

        self._code = code
        self._state = state

    def request_token(self) -> t.Mapping:
        """Request a token from the API."""
        with AuthRequestHandler.hook_callback(self._set_code_state):
            server = HTTPServer(("127.0.0.1", 8080), AuthRequestHandler)
            webbrowser.open(self._uri)
            server.handle_request()

        return self._client.fetch_token(
            "https://accounts.spotify.com/api/token",
            grant_type="authorization_code",
            code=self._code,
            state=self._state,
        )
