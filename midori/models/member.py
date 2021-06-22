"""Miscellaneous member models."""
from typing import Optional

from attr import define


@define
class Followers:
    """Followers of an item."""

    href: Optional[str]
    total: int


@define
class Image:
    """An image resource."""

    height: int
    url: str
    width: int
