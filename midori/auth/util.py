"""Utilities shared among clients."""
from typing import Tuple
from urllib.parse import parse_qs, urlparse


def _parse_code_state(url: str) -> Tuple[str, str]:
    qs = parse_qs(urlparse(url).query)
    return qs["code"][0], qs["state"][0]
