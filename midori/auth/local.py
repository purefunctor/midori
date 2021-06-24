"""Authentication flow that makes use of a local server."""
from __future__ import annotations

from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
import typing as t
from urllib.parse import urlparse
import webbrowser

from midori.auth.base import AuthClient
from midori.auth.util import _parse_code_state
from midori.error import InvalidRedirectUri


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
            server.shutdown()
