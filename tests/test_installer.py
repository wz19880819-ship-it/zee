"""Tests for install/uninstall/update operations."""

import pytest

from superpowers_marketplace import registry
from superpowers_marketplace.installer import (
    AlreadyInstalledError,
    NotFoundError,
    NotInstalledError,
    install,
    uninstall,
    update,
)


@pytest.fixture(autouse=True)
def clean_registry(tmp_path, monkeypatch):
    """Redirect the registry to a temp dir so tests don't touch ~/.superpowers."""
    monkeypatch.setattr(registry, "_REGISTRY_DIR", tmp_path / ".superpowers")
    monkeypatch.setattr(
        registry, "_REGISTRY_FILE", tmp_path / ".superpowers" / "installed.json"
    )
    yield


def test_install_success():
    sp = install("healing")
    assert sp["name"] == "healing"
    assert registry.is_installed("healing")


def test_install_unknown_raises():
    with pytest.raises(NotFoundError):
        install("unknown-power")


def test_install_duplicate_raises():
    install("flight")
    with pytest.raises(AlreadyInstalledError):
        install("flight")


def test_uninstall_success():
    install("timewarp")
    uninstall("timewarp")
    assert not registry.is_installed("timewarp")


def test_uninstall_not_installed_raises():
    with pytest.raises(NotInstalledError):
        uninstall("telepathy")


def test_update_success():
    install("magnetism")
    sp = update("magnetism")
    assert sp["name"] == "magnetism"
    assert registry.is_installed("magnetism")


def test_update_not_installed_raises():
    with pytest.raises(NotInstalledError):
        update("invisibility")


def test_list_installed_empty():
    assert registry.list_installed() == []


def test_list_installed_after_installs():
    install("superstrength")
    install("xrayvision")
    names = {sp["name"] for sp in registry.list_installed()}
    assert names == {"superstrength", "xrayvision"}
