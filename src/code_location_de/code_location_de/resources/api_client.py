"""FakeStore API resource for the Data Engineer challenge.

This resource is provided to all candidates. It wraps the FakeStore API
(https://fakestoreapi.com) and exposes methods to fetch the three available
entities: products, users, and carts (orders).

Platform Engineer note: this is the starting point for your resource design
decisions. You may extend, replace, or wrap this resource as you see fit.
"""

import requests
from dagster import ConfigurableResource, get_dagster_logger


class FakeStoreAPIResource(ConfigurableResource):
    """Configurable Dagster resource for the FakeStore API.

    Attributes:
        base_url: Base URL for the FakeStore API.
        timeout: Request timeout in seconds.
    """

    base_url: str = "https://fakestoreapi.com"
    timeout: int = 30

    def get_products(self) -> list[dict]:
        """Fetch all products from the catalog."""
        log = get_dagster_logger()
        url = f"{self.base_url}/products"
        log.info(f"Fetching products from {url}")
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_users(self) -> list[dict]:
        """Fetch all registered users."""
        log = get_dagster_logger()
        url = f"{self.base_url}/users"
        log.info(f"Fetching users from {url}")
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def get_carts(self) -> list[dict]:
        """Fetch all shopping carts (orders).

        Each cart contains a 'products' field which is a list of
        {'productId': int, 'quantity': int} dictionaries. This nested
        structure is preserved in the raw data and will need to be
        handled during transformation.
        """
        log = get_dagster_logger()
        url = f"{self.base_url}/carts"
        log.info(f"Fetching carts from {url}")
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        return response.json()
