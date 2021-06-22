"""Category object."""
from typing import List

import attr

from .base import Id
from .member import Image


@attr.s
class Category(Id):
    """Category for tagging items in Spotify."""

    href: str = attr.ib()
    icons: List[Image] = attr.ib()
    name: str = attr.ib()
