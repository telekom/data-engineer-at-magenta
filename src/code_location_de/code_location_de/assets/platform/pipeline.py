"""Platform Engineer track — your main implementation file.

Your task: build a production-quality Dagster pipeline that transforms the raw
ingestion data into clean, structured, reporting-ready tables.

Read docs/platform_track.md for the full brief and evaluation criteria.

The raw assets are already materialized by the ingestion group:
  - raw_products  (pd.DataFrame)
  - raw_users     (pd.DataFrame)
  - raw_carts     (pd.DataFrame — 'products' column is a JSON string)

Start by reading and exploring those assets, then design your pipeline below.

Guidelines:
  - Leave # DECISION: comments at every architectural choice point
  - Prefer clarity over cleverness
  - Treat this as production code: handle errors, add metadata, write tests
  - AI tools are welcome — explain what you used them for in a comment
"""

# import json
#
# import dagster as dg
# import pandas as pd
#
#
# ── DECISION POINT 1: Asset granularity ─────────────────────────────────────
# Option A: one @asset per entity (cleaned_products, cleaned_users, cleaned_carts)
#   Pro: each asset can be re-materialized independently; parallelism is explicit
#   Con: more boilerplate, three separate DuckDB table writes
# Option B: one @multi_asset that produces all three tables in one run
#   Pro: single function, fewer Dagster graph nodes
#   Con: all-or-nothing re-materialization; harder to test individual outputs
#
# # DECISION: I chose ... because ...
# ─────────────────────────────────────────────────────────────────────────────
#
#
# ── DECISION POINT 2: IO Manager vs. explicit writes ────────────────────────
# Option A: return a pd.DataFrame and let DuckDBPandasIOManager handle writes
#   Pro: clean separation of concerns; Dagster manages table creation
#   Con: less control over schema, partitioning, or write mode
# Option B: use duckdb.connect() inside the asset to write explicitly
#   Pro: full control (CREATE OR REPLACE, PARTITION BY, etc.)
#   Con: bypasses the IO manager; Dagster doesn't know output schema
#
# # DECISION: I chose ... because ...
# ─────────────────────────────────────────────────────────────────────────────
#
#
# @dg.asset(
#     deps=["raw_products"],
#     group_name="platform",
#     compute_kind="duckdb",
#     description="Cleaned and typed product catalog.",
# )
# def cleaned_products(
#     context: dg.AssetExecutionContext,
#     # DECISION POINT 3: Should you inject a DuckDB resource here, or use the IO manager?
#     # What makes this easier to unit-test?
# ) -> ...:
#     raise NotImplementedError("Implement me!")
#
#
# @dg.asset(
#     deps=["raw_users"],
#     group_name="platform",
#     compute_kind="duckdb",
#     description="Cleaned user accounts.",
# )
# def cleaned_users(context: dg.AssetExecutionContext) -> ...:
#     raise NotImplementedError("Implement me!")
#
#
# @dg.asset(
#     deps=["raw_carts"],
#     group_name="platform",
#     compute_kind="duckdb",
#     description="Cleaned orders with unnested line items.",
# )
# def cleaned_carts(context: dg.AssetExecutionContext) -> ...:
#     # DECISION POINT 4: Do you unnest the JSON 'products' array here in Python,
#     # or do you leave that for the dbt SQL layer?
#     # Consider: who is responsible for this logic? What happens when the schema changes?
#     # DECISION: I chose ... because ...
#     raise NotImplementedError("Implement me!")
#
#
# ── DECISION POINT 5: Partitioning ──────────────────────────────────────────
# raw_carts has a 'date' column ranging from 2019 to 2020.
# Should this pipeline be partitioned by date?
#
# Arguments for partitioning:
#   - Efficient backfills: re-run only a specific date range
#   - Incremental ingestion: only fetch new carts each day
#
# Arguments against:
#   - The dataset is tiny (20 rows); partitioning adds complexity for no gain
#   - FakeStore API doesn't support date filtering — you'd fetch all data anyway
#
# # DECISION: I chose ... because ...
# ─────────────────────────────────────────────────────────────────────────────
#
#
# ── DECISION POINT 6: Error handling ────────────────────────────────────────
# What's your strategy when:
#   a) The API returns a 500 (transient error)?
#   b) A required field is missing from a product record (data quality issue)?
#   c) The DuckDB write fails because of a schema mismatch?
#
# Dagster options: RetryPolicy, asset checks, op-level try/except, sensors
# # DECISION: I handled errors by ... because ...
# ─────────────────────────────────────────────────────────────────────────────
#
#
# ── DECISION POINT 7: Observability ─────────────────────────────────────────
# What metadata is worth attaching to MaterializeResult?
# What would a data platform team need to debug a silent data quality failure
# three days after it happened?
#
# Ideas: row counts, null rates, schema fingerprint, sample records, data ranges
# # DECISION: I added the following metadata because ...
# ─────────────────────────────────────────────────────────────────────────────
