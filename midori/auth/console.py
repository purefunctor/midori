"""Authentication flow that makes use of the console."""
from midori.auth.base import AuthClient
from midori.auth.util import _parse_code_state


class ConsoleAuthClient(AuthClient):
    """An authentication client that uses the console."""

    def _request_token(self) -> None:
        """Request a token from the API using the console."""
        print("Visit the following URL:", self._uri)
        url = input("Enter the URL you were redirected to: ")
        self._set_code_state(*_parse_code_state(url))
