"""Copyright object."""
from __future__ import annotations

from enum import Enum

from attr import define


@define
class Copyright:
    """The copyright of an item."""

    text: str
    type: CopyrightType


class CopyrightType(Enum):
    """The type of copyright."""

    COPYRIGHT = "C"
    PERFORMANCE = "P"
