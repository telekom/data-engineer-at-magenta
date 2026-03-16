# DWH Engineer Track

## Your mission

The raw ingestion layer is already provided. Three Dagster assets fetch data from the FakeStore API and write it to DuckDB as raw tables. Your job starts after that.

You will build a **complete dbt data model** on top of those raw tables: staging → intermediate → marts. The goal is a clean, well-documented, reporting-ready data warehouse that a BI team can query with confidence.

We are less interested in whether you implement every model, and more interested in **the quality of what you do implement**. A complete staging layer with excellent tests and documentation is worth more than a sketchy end-to-end implementation.

---

## What's already provided

| File | What it does |
|---|---|
| `src/code_location_de/code_location_de/assets/ingestion/` | Dagster assets that fetch and write the raw tables to DuckDB |
| `src/code_location_de_dbt/models/staging/_sources.yml` | Complete dbt source definitions — column names, descriptions, and notes |
| `src/code_location_de_dbt/dbt_project.yml` | dbt project config (staging → views, marts → tables) |
| `src/code_location_de_dbt/profiles.yml` | DuckDB connection config |
| `notebooks/explore.ipynb` | Data exploration notebook |

---

## The raw data

First, materialize the ingestion assets in Dagster to populate the DuckDB tables:

```bash
pixi run start-dev
# Open localhost:3000 → Materialize All on the ingestion group
```

Then you have three raw tables available:

**`main.raw_products`** — 20 products across 4 categories (electronics, jewelery, men's clothing, women's clothing). Flat structure with rating flattened into `rating_rate` and `rating_count`.

**`main.raw_users`** — 10 user accounts. Address fields flattened with underscore notation (`address_city`, `address_geo_lat`, etc.).

**`main.raw_carts`** — 20 shopping carts. Each cart has a `products` column that is a **JSON string**:

```json
[{"productId": 1, "quantity": 2}, {"productId": 3, "quantity": 1}]
```

This nested structure is the central modeling challenge of this track.

---

## What you build

### Staging layer (`models/staging/`)

One model per source table. Clean the raw data: consistent naming, type casting, null handling. The staging layer should map closely to the source — one row in, one row out (with the exception of `stg_orders`, where you'll need to decide what to do with the nested JSON).

| Model | Description |
|---|---|
| `stg_products.sql` | Clean product catalog with typed columns |
| `stg_users.sql` | Clean user accounts with readable column names |
| `stg_orders.sql` | Clean orders — see the decision point on nested JSON below |

### Intermediate layer (`models/intermediate/`)

Internal models for complex transformations. Not directly exposed to BI tools.

| Model | Description |
|---|---|
| `int_order_items.sql` | Explode cart line items into one row per product per order, joined to product details |
| `int_customer_orders.sql` | Aggregate order totals per customer (feeds `dim_customers`) |

### Mart layer (`models/marts/`)

The public API of your data warehouse. BI tools query these directly. Every column should be documented.

| Model | Description |
|---|---|
| `fct_orders.sql` | Orders fact table (see grain decision point below) |
| `dim_customers.sql` | Customer dimension with lifetime value stats |
| `dim_products.sql` | Product dimension |
| `rpt_sales_summary.sql` | Category-level sales report |

---

## Business questions your mart layer must answer

The BI team has four questions. Your models should make these queryable with a simple `SELECT`:

1. **What is total revenue per product category?**
2. **Who are the top 10 customers by lifetime value?**
3. **What is the average basket size** (number of distinct items per order)?
4. **Which products appear most frequently in orders?**

---

## Decision points

Mark each choice with a `-- DECISION:` comment in your SQL.

### 1. Grain of `fct_orders`

**Option A: One row per order** (`order_id` is the PK)
- Simpler to query for order-level KPIs (AOV, order count)
- Aggregation happens before the mart; some line-item detail is lost

**Option B: One row per order line item** (`order_id` + `product_id` is the PK)
- Full detail preserved; flexible for product and order analysis
- BI tools need to be careful not to double-count order-level metrics

Pick one. Implement it. Explain why.

### 2. Where to unnest the JSON

The `products` JSON array in `raw_carts` needs to be exploded into rows eventually. The question is where.

**Option A: Unnest in `stg_orders.sql`**
- Staging model is already flat
- Changes the grain of the staging model (1 cart → N line items)
- Staging models usually map 1:1 to source tables — this breaks that convention

**Option B: Unnest in `int_order_items.sql`**
- Staging stays clean and 1:1 with the source
- The JSON string travels through stg_orders before being processed
- Intermediate layer is the natural place for complex transformations

**DuckDB hint for unnesting:**
```sql
SELECT
    id AS order_id,
    UNNEST(json_extract(products, '$[*].productId')::INT[]) AS product_id,
    UNNEST(json_extract(products, '$[*].quantity')::INT[])  AS quantity
FROM {{ source('raw', 'raw_carts') }}
```

### 3. Test coverage philosophy

Add tests in `_staging.yml` and `_marts.yml`. Think about which tests genuinely catch data bugs vs. which are just ceremony.

Consider: `not_null`, `unique`, `accepted_values`, `relationships`, and dbt-utils tests like `expression_is_true`.

What test would have caught an actual bug during development?

### 4. Naming conventions

How did you decide what to name columns across models? Is there a project-wide convention?

Document your approach — even a one-line comment is enough.

---

## Data quality checks in Dagster (bonus)

If you want to go further: implement Dagster asset checks in `checks/raw_checks.py`. These run after the ingestion assets and validate the raw data before dbt runs.

Read the docs: https://docs.dagster.io/guides/test/asset-checks

---

## How to run

```bash
# Start Dagster and materialize ingestion assets first
pixi run start-dev

# Run all dbt models
make dbt-run

# Run dbt tests
make dbt-test

# Generate and serve dbt documentation
make dbt-docs
```

---

## Stretch goals (only if time allows)

- Add a `dim_date` seed and join it to `fct_orders` for calendar-based analysis
- Use a dbt macro to standardize monetary value formatting
- Add `meta` documentation to every column in every `.yml` file
- Write a custom dbt data test in `tests/`

---

## A note on AI tools

You're encouraged to use GitHub Copilot, Cursor, Claude Code, or any other AI assistant for writing SQL, generating documentation, or figuring out DuckDB syntax.

What we care about: do the models reflect sound data modeling judgment? Can you explain a model's design choices? Is the SQL readable and correct?

If you used an AI tool to generate SQL, leave a comment noting that — and explain what you validated or changed.
