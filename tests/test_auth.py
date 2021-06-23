"""Tests for the authentication clients."""
from abc import ABC, abstractmethod
from http.server import HTTPServer
from io import BytesIO, StringIO
from typing import Any

from pytest import CaptureFixture, raises
from pytest_mock import MockerFixture

from midori.auth import (
    AuthClient,
    AuthRequestHandler,
    ConsoleAuthClient,
    LocalAuthClient,
)
from midori.error import InvalidAuthState, InvalidRedirectUri


class _TestAuthClient(ABC):
    """Base class for tests against authentication clients."""

    @abstractmethod
    def _create_client(self, mocker: MockerFixture) -> Any:
        """Create a mocked client."""

    def create_client(self, mocker: MockerFixture) -> Any:
        """Mock dependencies and create a client."""
        _client = mocker.Mock()
        _client.create_authorization_url.return_value = ("URI", "STATE")

        mocker.patch("midori.auth.OAuth2Client", return_value=_client)

        return self._create_client(mocker)


class TestAuthClient(_TestAuthClient):
    """Tests for the base authentication client."""

    def _create_client(self, mocker: MockerFixture) -> Any:
        """Create a mocked client."""

        class _AuthClient(AuthClient):
            _request_token = mocker.Mock()

        client = _AuthClient(
            client_id="CLIENT_ID",
            client_secret="CLIENT_SECRET",
            redirect_uri="REDIRECT_URI",
            scope="SCOPE",
        )

        return client

    def test_set_code_state_sets_code_and_state(self, mocker: MockerFixture) -> None:
        """Test if code and state is set."""
        client = self.create_client(mocker)

        client._set_code_state("CODE", "STATE")

        assert client._code == "CODE"
        assert client._state == "STATE"

    def test_set_code_state_fails_on_invalid_state(self, mocker: MockerFixture) -> None:
        """Test if invalid states raise exceptions."""
        client = self.create_client(mocker)

        with raises(InvalidAuthState, match=".* 'STATE' .* 'INVALID_STATE'"):
            client._set_code_state("CODE", "INVALID_STATE")

    def test_request_token_calls_implementation(self, mocker: MockerFixture) -> None:
        """Test if the implementation method is called."""
        client = self.create_client(mocker)

        client.request_token()

        client._request_token.assert_called_once()
        client._client.fetch_token.assert_called_once()


class TestLocalAuthClient(_TestAuthClient):
    """Tests for the local authentication client."""

    def _create_client(self, mocker: MockerFixture) -> Any:
        return LocalAuthClient(
            client_id="CLIENT_ID",
            client_secret="CLIENT_SECRET",
            redirect_uri="REDIRECT_URI",
            scope="SCOPE",
        )

    def test_parse_redirect_uri_parses_valid_uris(self, mocker: MockerFixture) -> None:
        """Test if valid URIs are parsed."""
        client = self.create_client(mocker)
        client.redirect_uri = "https://localhost:8080"

        host, port = client._parse_redirect()

        assert host == "localhost"
        assert port == 8080

    def test_parse_redirect_uri_fails_on_missing_host(
        self, mocker: MockerFixture
    ) -> None:
        """Test if a missing host raises an exception."""
        client = self.create_client(mocker)
        client.redirect_uri = "https://:8080"

        with raises(InvalidRedirectUri):
            client._parse_redirect()

    def test_parse_redirect_uri_fails_on_missing_port(
        self, mocker: MockerFixture
    ) -> None:
        """Test if a missing port raises an exception."""
        client = self.create_client(mocker)
        client.redirect_uri = "https://localhost"

        with raises(InvalidRedirectUri):
            client._parse_redirect()

    def test_open_server_creates_an_http_server(self, mocker: MockerFixture) -> None:
        """Test if an HTTP server is created."""
        client = self.create_client(mocker)

        result = client._open_server("localhost", 8080)

        assert isinstance(result, HTTPServer)
        assert result.RequestHandlerClass == AuthRequestHandler

    def test_request_token_authenticates_using_a_browser(
        self, mocker: MockerFixture
    ) -> None:
        """Test if authentication is performed using a browser."""
        client = self.create_client(mocker)
        client.redirect_uri = "http://localhost:8080"

        server = mocker.Mock(spec=HTTPServer)
        mocker.patch("midori.auth.HTTPServer", return_value=server)
        ARH = mocker.patch("midori.auth.AuthRequestHandler")
        webbrowser_open = mocker.patch("webbrowser.open")

        client._request_token()

        # Implementation Contracts:
        # 1. The method must hook into the default request handler.
        # 2. The method must open the browser using `webbrowser`.
        # 3. The server must handle the request.
        #
        # Note: This does not test the functionality of the
        # AuthRequestHandler class.
        ARH.hook_callback.assert_called_once_with(client._set_code_state)
        webbrowser_open.assert_called_once_with(client._uri)
        server.handle_request.assert_called_once()


class TestConsoleAuthClient(_TestAuthClient):
    """Tests for the console authentication client."""

    def _create_client(self, mocker: MockerFixture) -> Any:
        return ConsoleAuthClient(
            client_id="CLIENT_ID",
            client_secret="CLIENT_SECRET",
            redirect_uri="REDIRECT_URI",
            scope="SCOPE",
        )

    def test_request_token_authenticates_using_the_console(
        self, capsys: CaptureFixture, mocker: MockerFixture
    ) -> None:
        """Test if authentication is performed using the console."""
        client = self.create_client(mocker)
        mocker.patch(
            "sys.stdin", StringIO("http://localhost:8080/?code=CODE&state=STATE")
        )

        client._request_token()

        outerr = capsys.readouterr()

        assert outerr.out == (
            f"Visit the following URL: {client._uri}\n"
            "Enter the URL you were redirected to: "
        )
        assert client._code == "CODE"
        assert client._state == "STATE"


class TestAuthHandler:
    """Tests for the request handler of the local callback server."""

    def create_handler(self, mocker: MockerFixture) -> AuthRequestHandler:
        """Create a mocked handler."""
        request = mocker.Mock()
        request.makefile.return_value = BytesIO(b"GET /?code=CODE&state=STATE")
        server = mocker.Mock()
        return AuthRequestHandler(request, ("localhost", 8080), server)

    def test_do_GET_callback(self, mocker: MockerFixture) -> None:
        """Test if the GET handler calls the callback."""
        handler = self.create_handler(mocker)
        callback = mocker.Mock()

        with AuthRequestHandler.hook_callback(callback):
            handler.do_GET()

        callback.assert_called_once_with("CODE", "STATE")

    def test_do_GET_no_callback(self, mocker: MockerFixture) -> None:
        """Test if the GET handler calls no callback."""
        handler = self.create_handler(mocker)
        handler.do_GET()

    def test_hook_callback(self, mocker: MockerFixture) -> None:
        """Test if a callback is properly set."""
        callback = mocker.Mock()

        with AuthRequestHandler.hook_callback(callback) as arh:
            assert arh is AuthRequestHandler
            assert AuthRequestHandler._callback is callback

        assert AuthRequestHandler._callback is None
