"""Tests for the local authentication client."""
from http.server import HTTPServer
from io import BytesIO
from typing import Any

from pytest import fixture, raises
from pytest_mock import MockerFixture

from midori.auth import LocalAuthClient
from midori.auth.local import AuthRequestHandler
from midori.error import InvalidRedirectUri


@fixture
def client(mocker: MockerFixture) -> Any:
    """Client fixture."""
    return LocalAuthClient(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        redirect_uri="REDIRECT_URI",
        scope="SCOPE",
        client=mocker.Mock(),
    )


@fixture
def handler(mocker: MockerFixture) -> Any:
    """Request handler fixture."""
    request = mocker.Mock()
    request.makefile.return_value = BytesIO(b"GET /?code=CODE&state=STATE")
    server = mocker.Mock()
    return AuthRequestHandler(request, ("localhost", 8080), server)


def test_parse_redirect_uri_parses_valid_uris(client: Any) -> None:
    """Test if valid URIs are parsed."""
    client.redirect_uri = "https://localhost:8080"

    host, port = client._parse_redirect()

    assert host == "localhost"
    assert port == 8080


def test_parse_redirect_uri_fails_on_missing_host(client: Any) -> None:
    """Test if a missing host raises an exception."""
    client.redirect_uri = "https://:8080"

    with raises(InvalidRedirectUri):
        client._parse_redirect()


def test_parse_redirect_uri_fails_on_missing_port(client: Any) -> None:
    """Test if a missing port raises an exception."""
    client.redirect_uri = "https://localhost"

    with raises(InvalidRedirectUri):
        client._parse_redirect()


def test_open_server_creates_an_http_server(client: Any) -> None:
    """Test if an HTTP server is created."""
    result = client._open_server("localhost", 8080)

    assert isinstance(result, HTTPServer)
    assert result.RequestHandlerClass == AuthRequestHandler


def test_visit_auth_url_authenticates_using_a_browser(
    client: Any, mocker: MockerFixture
) -> None:
    """Test if authentication is performed using a browser."""
    client.redirect_uri = "http://localhost:8080"

    server = mocker.Mock(spec=HTTPServer)
    mocker.patch("midori.auth.local.HTTPServer", return_value=server)
    ARH = mocker.patch("midori.auth.local.AuthRequestHandler")
    webbrowser_open = mocker.patch("webbrowser.open")

    client._visit_auth_url()

    # Implementation Contracts:
    # 1. The method must hook into the default request handler.
    # 2. The method must open the browser using `webbrowser`.
    # 3. The server must handle the request.
    #
    # Note: This does not test the functionality of the
    # AuthRequestHandler class.
    ARH.hook_callback.assert_called_once_with(client._consume_callback_url)
    webbrowser_open.assert_called_once_with(client._uri)
    server.handle_request.assert_called_once()


def test_auth_handler_hook_callback(mocker: MockerFixture) -> None:
    """Test if a callback is properly set."""
    callback = mocker.Mock()

    with AuthRequestHandler.hook_callback(callback) as arh:
        assert arh is AuthRequestHandler
        assert AuthRequestHandler._callback is callback

    assert AuthRequestHandler._callback is None


def test_auth_handler_do_GET_callback(handler: Any, mocker: MockerFixture) -> None:
    """Test if the GET handler calls the callback."""
    callback = mocker.Mock()

    with AuthRequestHandler.hook_callback(callback):
        handler.do_GET()

    callback.assert_called_once_with("/?code=CODE&state=STATE")


def test_auth_handler_do_GET_no_callback(handler: Any) -> None:
    """Test if the GET handler calls no callback."""
    handler.do_GET()
