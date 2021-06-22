"""User objects."""
from __future__ import annotations

from enum import Enum
from typing import List

import attr

from .base import Item
from .external import ExternalUrl
from .member import Followers, Image


class ExplicitContentSettings:
    """A user's explicit content settings."""


@attr.s
class _User(Item):
    """Base class for users."""

    display_name: str = attr.ib()
    external_urls: ExternalUrl = attr.ib()
    followers: Followers = attr.ib()
    images: List[Image] = attr.ib()


@attr.s
class PrivateUser(_User):
    """Private-facing user."""

    country: str = attr.ib()
    email: str = attr.ib()
    explicit_content: ExplicitContentSettings = attr.ib()
    product: str = attr.ib()


@attr.s
class PublicUser(_User):
    """Public-facing user."""


class UserProductType(Enum):
    """The user's Spotify subscription level."""

    PREMIUM = "PREMIUM"
    FREE = "FREE"
    OPEN = "OPEN"
