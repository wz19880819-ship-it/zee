"""Tests for marketplace search and catalog access."""

import pytest

from superpowers_marketplace import marketplace


def test_get_all_returns_list():
    result = marketplace.get_all()
    assert isinstance(result, list)
    assert len(result) > 0


def test_each_entry_has_required_fields():
    for sp in marketplace.get_all():
        assert "name" in sp
        assert "version" in sp
        assert "description" in sp
        assert "author" in sp


def test_get_by_name_found():
    sp = marketplace.get_by_name("healing")
    assert sp is not None
    assert sp["name"] == "healing"


def test_get_by_name_not_found():
    assert marketplace.get_by_name("nonexistent-superpower") is None


def test_search_by_name():
    results = marketplace.search("speed")
    names = [sp["name"] for sp in results]
    assert "speedforce" in names


def test_search_by_tag():
    results = marketplace.search("performance")
    names = [sp["name"] for sp in results]
    assert "superstrength" in names
    assert "speedforce" in names


def test_search_by_description():
    results = marketplace.search("circuit breaker")
    assert any("healing" == sp["name"] for sp in results)


def test_search_no_results():
    assert marketplace.search("zzz-no-match-xyz") == []


def test_search_is_case_insensitive():
    upper = marketplace.search("ASYNC")
    lower = marketplace.search("async")
    assert upper == lower
