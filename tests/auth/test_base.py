"""Tests for the base authentication client."""
from typing import Any

import httpx
from pytest import fixture, raises
from pytest_mock import MockerFixture

from midori.auth import AuthClient
from midori.error import InvalidAuthState


@fixture
def client(mocker: MockerFixture) -> Any:
    """Client fixture."""

    class MockedAuthClient(AuthClient):
        _visit_auth_url = mocker.Mock()

    client = MockedAuthClient(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        redirect_uri="REDIRECT_URI",
        scope="SCOPE",
        client=mocker.Mock(),
    )

    return client


def test_consume_callback_url_fails_on_state_mismatch(client: Any) -> None:
    """Test if an exception is raised on state mismatch."""
    with raises(InvalidAuthState, match=f".* '{client._state}' .* 'STATE'"):
        client._consume_callback_url("/?code=CODE&state=STATE")


def test_consume_callback_url_sets_code(client: Any) -> None:
    """Test if the code attribute becomes set."""
    client._state = "STATE"

    client._consume_callback_url("/?code=CODE&state=STATE")

    assert client._code == "CODE"


def test_borrow_client_creates_and_closes_a_client(client: Any) -> None:
    """Test if a new client is made and closed."""
    client._client = None

    with client._borrow_client() as borrowed_client:
        assert isinstance(borrowed_client, httpx.Client)

    assert borrowed_client.is_closed


def test_borrow_client_returns_the_provided_client(client: Any) -> None:
    """Test if the provided client is yielded."""
    with client._borrow_client() as borrowed_client:
        assert borrowed_client is client._client

    client._client.close.assert_not_called()


def test_post_api_token_calls_the_api(client: Any) -> None:
    """Test if the API is called using the client."""
    client._post_api_token(grant_type="authorization_code")

    client._client.post.assert_called_once()
    assert "data" in client._client.post.call_args[1]
    assert "headers" in client._client.post.call_args[1]


def test_request_token_calls_visit_auth_url_and_post_api_token(
    client: Any, mocker: MockerFixture
) -> None:
    """Test if the auth url is visited and the API is called."""
    client._post_api_token = mocker.MagicMock()

    client.request_token()

    client._visit_auth_url.assert_called_once()
    client._post_api_token.assert_called_once()


def test_refresh_token_calls_the_api(client: Any, mocker: MockerFixture) -> None:
    """Test if the API is called when refreshing."""
    client.request_token()
    client._post_api_token = mocker.MagicMock()

    client.refresh_token(refresh_token="REFRESH_TOKEN")

    client._post_api_token.assert_called_once()
