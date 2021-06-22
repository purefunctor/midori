"""Base classes."""
import attr


class Id:
    """Identifiable with an id."""

    id: str


class Item:
    """Identifiable with other attributes."""

    href: str = attr.ib()
    type: str = attr.ib()
    uri: str = attr.ib()
