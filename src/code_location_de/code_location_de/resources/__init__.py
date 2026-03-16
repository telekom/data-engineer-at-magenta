import os

from dagster_duckdb_pandas import DuckDBPandasIOManager

from code_location_de.resources.api_client import FakeStoreAPIResource

RESOURCES_LOCAL: dict = {
    "io_manager": DuckDBPandasIOManager(
        database=os.getenv("ANALYTICS_DB_PATH", "analytics_database_dev.duckdb"),
        schema="main",
    ),
    "fake_store_api": FakeStoreAPIResource(),
}

RESOURCES_PROD: dict = {
    "io_manager": DuckDBPandasIOManager(
        database=os.getenv("ANALYTICS_DB_PATH", "analytics_database_prod.duckdb"),
        schema="main",
    ),
    "fake_store_api": FakeStoreAPIResource(),
}


def get_resources_for_deployment() -> dict:
    """Return the appropriate resource configuration based on DAGSTER_DEPLOYMENT env var.

    Set DAGSTER_DEPLOYMENT=prod to use production resources.
    Defaults to local/development resources.
    """
    deployment = os.getenv("DAGSTER_DEPLOYMENT", "local")
    if deployment == "prod":
        return RESOURCES_PROD
    return RESOURCES_LOCAL
