from dagster import Definitions, load_assets_from_package_module, with_source_code_references

from code_location_de.assets import ingestion, platform
from code_location_de.resources import get_resources_for_deployment

all_assets = with_source_code_references(
    [
        *load_assets_from_package_module(ingestion),
        *load_assets_from_package_module(platform),
    ]
)

defs = Definitions(
    assets=all_assets,
    resources=get_resources_for_deployment(),
)
