"""DWH Engineer track — asset checks on raw ingestion data.

Dagster asset checks let you define data quality expectations that run
automatically after an asset is materialized. They appear as green/red
indicators in the Dagster UI and can block downstream assets if they fail.

Read the Dagster docs on asset checks:
https://docs.dagster.io/guides/test/asset-checks

Your task: implement at least three meaningful asset checks across the
raw_products, raw_users, and raw_carts assets.

Think about:
  - What invariants must always be true about this data?
  - What would break silently downstream if a check weren't in place?
  - Which checks add genuine value vs. which are just ceremony?

AI tools are welcome — explain what you used them for in a comment.
"""

# import dagster as dg
# import pandas as pd
#
#
# @dg.asset_check(asset="raw_products", description="Products table must not be empty.")
# def raw_products_not_empty(raw_products: pd.DataFrame) -> dg.AssetCheckResult:
#     # DECISION: I chose this check because ...
#     raise NotImplementedError("Implement me!")
#
#
# @dg.asset_check(asset="raw_users", description="Every user must have a non-null email address.")
# def raw_users_email_not_null(raw_users: pd.DataFrame) -> dg.AssetCheckResult:
#     raise NotImplementedError("Implement me!")
#
#
# @dg.asset_check(asset="raw_carts", description="All cart dates must be valid (parseable) timestamps.")
# def raw_carts_valid_dates(raw_carts: pd.DataFrame) -> dg.AssetCheckResult:
#     raise NotImplementedError("Implement me!")
#
#
# Add more checks here. Consider:
#   - Price must be > 0 for all products
#   - user_id in raw_carts must reference a known user
#   - products JSON in raw_carts must be parseable for every row
