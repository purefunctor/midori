"""Tests for the cache handlers."""
import json
from pathlib import Path

from midori.auth import AuthInfo, FileCache, InMemoryCache


AUTH_INFO: AuthInfo = {
    "access_token": "ACCESS_TOKEN",
    "token_type": "TOKEN_TYPE",
    "scope": "SCOPE",
    "expires_in": 0,
    "refresh_token": "REFRESH_TOKEN",
}


def test_in_memory_cache_read() -> None:
    """Test reading from the in-memory cache."""
    auth_cache = InMemoryCache()
    auth_cache.auth_info = AUTH_INFO

    assert auth_cache.read_auth() == AUTH_INFO


def test_in_memory_cache_save() -> None:
    """Test saving to the in-memory cache."""
    auth_cache = InMemoryCache()

    auth_cache.save_auth(AUTH_INFO)

    assert auth_cache.auth_info == AUTH_INFO


def test_file_cache_read(tmp_path: Path) -> None:
    """Test reading from the file cache."""
    auth_path = tmp_path / "auth.json"
    auth_cache = FileCache(auth_path)
    with auth_path.open("w") as f:
        json.dump(AUTH_INFO, f)

    assert auth_cache.read_auth() == AUTH_INFO


def test_file_cache_save(tmp_path: Path) -> None:
    """Test saving to the file cache."""
    auth_path = tmp_path / "auth.json"
    auth_cache = FileCache(auth_path)

    auth_cache.save_auth(AUTH_INFO)

    with auth_path.open("r") as f:
        assert json.load(f) == AUTH_INFO
