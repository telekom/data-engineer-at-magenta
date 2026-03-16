"""Example tests for the ingestion assets — provided to all candidates.

These tests show the pattern for testing Dagster assets with mocked resources.
Run them with: pixi run -e dev test

Read the Dagster docs on testing:
https://docs.dagster.io/guides/test/unit-testing-assets-and-ops
"""

import json
from unittest.mock import MagicMock

import pandas as pd
import pytest
from dagster import materialize

from code_location_de.assets.ingestion.raw_data import raw_carts, raw_products, raw_users
from code_location_de.resources.api_client import FakeStoreAPIResource

# ── Fixtures ─────────────────────────────────────────────────────────────────


@pytest.fixture
def mock_products() -> list[dict]:
    return [
        {
            "id": 1,
            "title": "Test Product",
            "price": 9.99,
            "description": "A test product",
            "category": "electronics",
            "image": "http://example.com/img.jpg",
            "rating": {"rate": 4.5, "count": 100},
        }
    ]


@pytest.fixture
def mock_users() -> list[dict]:
    return [
        {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "phone": "555-1234",
            "name": {"firstname": "Test", "lastname": "User"},
            "address": {
                "city": "Berlin",
                "street": "Main St",
                "number": 42,
                "zipcode": "10115",
                "geolocation": {"lat": "52.52", "long": "13.40"},
            },
        }
    ]


@pytest.fixture
def mock_carts() -> list[dict]:
    return [
        {
            "id": 1,
            "userId": 1,
            "date": "2020-01-01T00:00:00.000Z",
            "products": [{"productId": 1, "quantity": 2}],
        }
    ]


@pytest.fixture
def mock_api_resource(mock_products, mock_users, mock_carts) -> FakeStoreAPIResource:
    resource = MagicMock(spec=FakeStoreAPIResource)
    resource.get_products.return_value = mock_products
    resource.get_users.return_value = mock_users
    resource.get_carts.return_value = mock_carts
    return resource


# ── Tests ─────────────────────────────────────────────────────────────────────


def test_raw_products_materializes(mock_api_resource):
    """raw_products should produce a DataFrame with expected columns."""
    result = materialize(
        [raw_products],
        resources={"fake_store_api": mock_api_resource, "io_manager": MagicMock()},
    )
    assert result.success


def test_raw_products_flattens_rating(mock_api_resource):
    """Nested 'rating' dict should be flattened into rating_rate and rating_count."""
    result = materialize(
        [raw_products],
        resources={"fake_store_api": mock_api_resource, "io_manager": MagicMock()},
    )
    assert result.success
    # The materialized DataFrame is captured via the MaterializeResult value
    output = result.output_for_node("raw_products")
    assert "rating_rate" in output.columns
    assert "rating_count" in output.columns
    assert "rating" not in output.columns


def test_raw_carts_products_is_json_string(mock_api_resource):
    """The 'products' column in raw_carts should be a JSON string, not a list."""
    result = materialize(
        [raw_carts],
        resources={"fake_store_api": mock_api_resource, "io_manager": MagicMock()},
    )
    assert result.success
    output = result.output_for_node("raw_carts")
    assert isinstance(output["products"].iloc[0], str)
    parsed = json.loads(output["products"].iloc[0])
    assert isinstance(parsed, list)
    assert parsed[0]["productId"] == 1
