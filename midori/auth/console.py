"""Authentication flow that makes use of the console."""
from midori.auth.base import AuthClient


class ConsoleAuthClient(AuthClient):
    """An authentication client that uses the console."""

    def _visit_auth_url(self) -> None:
        """Request a token from the API using the console."""
        print("Visit the following URL:", self._uri)
        url = input("Enter the URL you were redirected to: ")
        self._consume_callback_url(url)
