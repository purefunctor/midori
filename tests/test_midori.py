"""Tests for the top-level package."""
from midori import __version__


def test_version() -> None:
    """Test the package version."""
    assert __version__ == "0.1.0"
