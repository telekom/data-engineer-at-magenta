"""Raw ingestion assets — provided to all candidates.

These assets fetch data from the FakeStore API and land it in DuckDB as raw tables.
They are the starting point for both the Platform Engineer and DWH Engineer tracks.

You do not need to modify these files. If you do modify them, explain why in a comment.
"""

import json

import dagster as dg
import pandas as pd

from code_location_de.resources.api_client import FakeStoreAPIResource


@dg.asset(
    group_name="ingestion",
    compute_kind="python",
    description="Raw product catalog fetched from the FakeStore API.",
)
def raw_products(
    context: dg.AssetExecutionContext,
    fake_store_api: FakeStoreAPIResource,
) -> dg.MaterializeResult:
    """Fetch all products and store them as a flat table in DuckDB.

    The 'rating' field (nested dict) is flattened into 'rating_rate' and
    'rating_count' columns.
    """
    products = fake_store_api.get_products()

    rows = []
    for p in products:
        rows.append(
            {
                "id": p["id"],
                "title": p["title"],
                "price": p["price"],
                "description": p["description"],
                "category": p["category"],
                "image": p.get("image"),
                "rating_rate": p.get("rating", {}).get("rate"),
                "rating_count": p.get("rating", {}).get("count"),
            }
        )

    df = pd.DataFrame(rows)

    context.log.info(f"Fetched {len(df)} products across {df['category'].nunique()} categories")

    return dg.MaterializeResult(
        value=df,
        metadata={
            "row_count": dg.MetadataValue.int(len(df)),
            "categories": dg.MetadataValue.json(df["category"].unique().tolist()),
            "preview": dg.MetadataValue.md(df.head(3).to_markdown(index=False)),
        },
    )


@dg.asset(
    group_name="ingestion",
    compute_kind="python",
    description="Raw user accounts fetched from the FakeStore API.",
)
def raw_users(
    context: dg.AssetExecutionContext,
    fake_store_api: FakeStoreAPIResource,
) -> dg.MaterializeResult:
    """Fetch all users and store them as a flat table in DuckDB.

    Nested address and geolocation fields are flattened with underscore-separated
    names (e.g. address_city, address_geo_lat).
    """
    users = fake_store_api.get_users()

    rows = []
    for u in users:
        address = u.get("address", {})
        geo = address.get("geolocation", {})
        name = u.get("name", {})
        rows.append(
            {
                "id": u["id"],
                "username": u["username"],
                "email": u["email"],
                "phone": u.get("phone"),
                "name_firstname": name.get("firstname"),
                "name_lastname": name.get("lastname"),
                "address_city": address.get("city"),
                "address_street": address.get("street"),
                "address_number": address.get("number"),
                "address_zipcode": address.get("zipcode"),
                "address_geo_lat": geo.get("lat"),
                "address_geo_long": geo.get("long"),
            }
        )

    df = pd.DataFrame(rows)

    context.log.info(f"Fetched {len(df)} users")

    return dg.MaterializeResult(
        value=df,
        metadata={
            "row_count": dg.MetadataValue.int(len(df)),
            "preview": dg.MetadataValue.md(df[["id", "username", "email"]].head(3).to_markdown(index=False)),
        },
    )


@dg.asset(
    group_name="ingestion",
    compute_kind="python",
    description=(
        "Raw shopping carts (orders) fetched from the FakeStore API. "
        "The 'products' column contains a JSON string representing a list of "
        "{productId, quantity} objects — this nested structure is intentional "
        "and needs to be handled during transformation."
    ),
)
def raw_carts(
    context: dg.AssetExecutionContext,
    fake_store_api: FakeStoreAPIResource,
) -> dg.MaterializeResult:
    """Fetch all carts and store them in DuckDB.

    Note: The 'products' column is stored as a JSON string.
    Each value looks like: '[{"productId": 1, "quantity": 2}, ...]'

    This is a deliberate design choice: we preserve the raw structure and
    leave the unnesting decision to the transformation layer.
    """
    carts = fake_store_api.get_carts()

    rows = []
    for c in carts:
        rows.append(
            {
                "id": c["id"],
                "user_id": c["userId"],
                "date": c["date"],
                "products": json.dumps(c.get("products", [])),
            }
        )

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])

    context.log.info(f"Fetched {len(df)} carts spanning {df['date'].min()} to {df['date'].max()}")

    return dg.MaterializeResult(
        value=df,
        metadata={
            "row_count": dg.MetadataValue.int(len(df)),
            "date_range_start": dg.MetadataValue.text(str(df["date"].min().date())),
            "date_range_end": dg.MetadataValue.text(str(df["date"].max().date())),
            "preview": dg.MetadataValue.md(df[["id", "user_id", "date"]].head(3).to_markdown(index=False)),
        },
    )
