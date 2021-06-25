"""Tests for the console authentication client."""
from io import StringIO
from typing import Any

from pytest import CaptureFixture, fixture
from pytest_mock import MockerFixture

from midori.auth import ConsoleAuthClient


@fixture
def client(mocker: MockerFixture) -> Any:
    """Client fixture."""
    client = ConsoleAuthClient(
        client_id="CLIENT_ID",
        client_secret="CLIENT_SECRET",
        redirect_uri="REDIRECT_URI",
        scope="SCOPE",
        client=mocker.Mock(),
    )

    return client


def test_visit_auth_url_authenticates_using_the_console(
    capsys: CaptureFixture, client: Any, mocker: MockerFixture
) -> None:
    """Test if authentication is performed using the console."""
    mocker.patch(
        "sys.stdin",
        StringIO(f"http://localhost:8080/?code=CODE&state={client._state}"),
    )

    client._visit_auth_url()

    outerr = capsys.readouterr()

    assert outerr.out == (
        f"Visit the following URL: {client._uri}\n"
        "Enter the URL you were redirected to: "
    )
    assert client._code == "CODE"
    assert client._state == client._state
