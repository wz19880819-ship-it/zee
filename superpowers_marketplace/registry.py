"""Local registry that tracks installed superpowers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_REGISTRY_DIR = Path.home() / ".superpowers"
_REGISTRY_FILE = _REGISTRY_DIR / "installed.json"


def _load() -> dict[str, Any]:
    if not _REGISTRY_FILE.exists():
        return {}
    with _REGISTRY_FILE.open() as f:
        return json.load(f)


def _save(data: dict[str, Any]) -> None:
    _REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    with _REGISTRY_FILE.open("w") as f:
        json.dump(data, f, indent=2)


def list_installed() -> list[dict[str, Any]]:
    """Return all installed superpowers as a list."""
    return list(_load().values())


def is_installed(name: str) -> bool:
    return name in _load()


def record_install(superpower: dict[str, Any]) -> None:
    data = _load()
    data[superpower["name"]] = superpower
    _save(data)


def record_uninstall(name: str) -> bool:
    """Remove *name* from the registry. Returns True if it was present."""
    data = _load()
    if name not in data:
        return False
    del data[name]
    _save(data)
    return True
