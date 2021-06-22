"""Device object."""
from __future__ import annotations

from enum import Enum
from typing import List, Optional

import attr


@attr.s
class Device:
    """A device."""

    id: Optional[str] = attr.ib()
    is_active: bool = attr.ib()
    is_private_session: bool = attr.ib()
    is_restricted: bool = attr.ib()
    name: str = attr.ib()
    type: DeviceType = attr.ib()
    volume_percent: Optional[int] = attr.ib()


class DeviceType(Enum):
    """The type of a device."""

    COMPUTER = "computer"
    SMARTPHONE = "smartphone"
    SPEAKER = "speaker"


@attr.s
class Devices:
    """A collection of devices."""

    devices: List[Device] = attr.ib()
