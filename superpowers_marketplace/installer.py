"""Install and uninstall superpowers."""

from __future__ import annotations

from . import marketplace, registry


class AlreadyInstalledError(Exception):
    pass


class NotInstalledError(Exception):
    pass


class NotFoundError(Exception):
    pass


def install(name: str) -> dict:
    """Install a superpower by name. Returns the superpower dict."""
    sp = marketplace.get_by_name(name)
    if sp is None:
        raise NotFoundError(f"Superpower '{name}' not found in the marketplace.")
    if registry.is_installed(name):
        raise AlreadyInstalledError(f"'{name}' is already installed.")
    registry.record_install(sp)
    return sp


def uninstall(name: str) -> None:
    """Uninstall a superpower by name."""
    if not registry.is_installed(name):
        raise NotInstalledError(f"'{name}' is not installed.")
    registry.record_uninstall(name)


def update(name: str) -> dict:
    """Re-fetch and reinstall the latest version of an installed superpower."""
    if not registry.is_installed(name):
        raise NotInstalledError(f"'{name}' is not installed.")
    sp = marketplace.get_by_name(name)
    if sp is None:
        raise NotFoundError(f"Superpower '{name}' not found in the marketplace.")
    registry.record_uninstall(name)
    registry.record_install(sp)
    return sp
