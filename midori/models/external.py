"""External objects."""
import attr


@attr.s
class ExternalId:
    """External identification."""

    ean: str = attr.ib()
    isrc: str = attr.ib()
    upc: str = attr.ib()


@attr.s
class ExternalUrl:
    """External links."""

    spotify: str = attr.ib()
