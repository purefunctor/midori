"""Cursor for indexing results."""
from typing import Generic, List, TypeVar

import attr


T = TypeVar("T")


@attr.s
class _Paging(Generic[T]):
    """Base class for paging classes."""

    href: str = attr.ib()
    limit: int = attr.ib()
    items: List[T] = attr.ib()
    next: str = attr.ib()
    total: int = attr.ib()


@attr.s
class _Offset:
    """Base class for offsetted paging classes."""

    previous: str = attr.ib()
    offset: int = attr.ib()


@attr.s
class Cursor:
    """Indexes results."""

    after: str = attr.ib()


@attr.s
class CursorPaging(_Paging[T]):
    """Paginates results with a cursor."""

    cursors: Cursor = attr.ib()


@attr.s
class Paging(_Paging[T], _Offset):
    """Paginates results with an offset."""
