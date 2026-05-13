"""Catalog access and search for the superpowers marketplace."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_CATALOG_PATH = Path(__file__).parent / "data" / "catalog.json"


def _load_catalog() -> list[dict[str, Any]]:
    with _CATALOG_PATH.open() as f:
        return json.load(f)


def search(query: str) -> list[dict[str, Any]]:
    """Return superpowers whose name, description, or tags contain *query*."""
    q = query.lower()
    return [
        sp
        for sp in _load_catalog()
        if q in sp["name"].lower()
        or q in sp["description"].lower()
        or any(q in tag.lower() for tag in sp.get("tags", []))
    ]


def get_all() -> list[dict[str, Any]]:
    """Return the full catalog."""
    return _load_catalog()


def get_by_name(name: str) -> dict[str, Any] | None:
    """Return a single superpower by exact name, or None if not found."""
    for sp in _load_catalog():
        if sp["name"] == name:
            return sp
    return None
