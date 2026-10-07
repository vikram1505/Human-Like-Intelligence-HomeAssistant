"""Regression tests preventing obvious private data from entering the repository."""
from __future__ import annotations

from pathlib import Path
import re

ROOT = Path(__file__).parents[1]
PRIVATE_IPV4 = re.compile(
    r"(?<![\w.])(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
    r"192\.168\.\d{1,3}\.\d{1,3}|"
    r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})(?![\w.])"
)


def test_no_private_network_addresses() -> None:
    """Public files must not contain RFC1918 IPv4 addresses."""
    paths = [
        path
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts and path.suffix != ".pyc"
    ]
    repository_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore") for path in paths
    )
    assert not PRIVATE_IPV4.search(repository_text)
