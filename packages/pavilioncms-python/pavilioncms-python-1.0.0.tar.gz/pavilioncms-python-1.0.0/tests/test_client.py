#!/usr/bin/env python

"""Tests for `pavilion_cms` package."""

# from pavilion_cms import pavilion_cms
from pavilion_cms import PavilionCMS

from .fixtures import ALL_CATEGORIES, ALL_TAGS


def test_get_all_tags(mocker):
    client = PavilionCMS("test_token")

    mocker.patch("pavilion_cms.client.Client.make_list_request", return_value=ALL_TAGS)

    resp = client.tags.all()

    assert resp is not None
    assert resp["count"] == 5
    assert len(resp["results"]) == 5


def test_get_single_tag(mocker):
    client = PavilionCMS("test_token")

    mocker.patch(
        "pavilion_cms.client.Client.make_single_request",
        return_value=ALL_TAGS["results"][0],
    )

    resp = client.tags.get(ALL_TAGS["results"][0]["id"])

    assert resp is not None
    assert resp["id"] == ALL_TAGS["results"][0]["id"]
    assert resp["name"] == ALL_TAGS["results"][0]["name"]


def test_get_all_categories(mocker):
    client = PavilionCMS("test_token")
    mocker.patch(
        "pavilion_cms.client.Client.make_list_request", return_value=ALL_CATEGORIES
    )

    resp = client.category.all()

    assert resp is not None
    assert resp["next"] is None
    assert resp["previous"] is None
    assert resp["count"] == 4
    assert len(resp["results"]) == 4


def test_get_single_category(mocker):
    client = PavilionCMS("test_token")

    mocker.patch(
        "pavilion_cms.client.Client.make_single_request",
        return_value=ALL_CATEGORIES["results"][0],
    )

    resp = client.category.get(ALL_CATEGORIES["results"][0]["id"])

    assert resp is not None
    assert resp["id"] == ALL_CATEGORIES["results"][0]["id"]
    assert resp["name"] == ALL_CATEGORIES["results"][0]["name"]
