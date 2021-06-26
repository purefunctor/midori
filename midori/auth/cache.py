"""Classes for caching auth information."""
from abc import abstractmethod
import json
from pathlib import Path
import typing as t

import attr

from midori.auth.common import AuthInfo


class _AuthCache(t.Protocol):
    """An abstract blueprint for caching auth information."""

    @abstractmethod
    def read_auth(self) -> AuthInfo:
        """Read the auth info from the cache."""

    @abstractmethod
    def save_auth(self, auth_info: AuthInfo) -> None:
        """Save the auth info to the cache."""


@attr.s
class InMemoryCache(_AuthCache):
    """Caches auth in-memory."""

    auth_info: AuthInfo = attr.ib(init=False, default=None)

    def read_auth(self) -> AuthInfo:
        """Read the auth info from the cache."""
        return self.auth_info

    def save_auth(self, auth_info: AuthInfo) -> None:
        """Save the auth info to the cache."""
        self.auth_info = auth_info


@attr.s
class FileCache(_AuthCache):
    """Caches auth in a file."""

    path: Path = attr.ib()

    def read_auth(self) -> AuthInfo:
        """Read the auth info from the cache."""
        with self.path.open("r") as f:
            return json.load(f)

    def save_auth(self, auth_info: AuthInfo) -> None:
        """Save the auth info to the cache."""
        with self.path.open("w") as f:
            json.dump(auth_info, f)
