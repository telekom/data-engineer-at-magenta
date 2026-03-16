# Platform Engineer Track

## Your mission

The raw ingestion assets are already provided. They fetch product, user, and order data from the FakeStore API and write it to DuckDB as three raw tables.

Your job is to build the next layer: a production-quality Dagster pipeline that takes the raw data, transforms it into clean and structured tables, and makes it reliable enough for a downstream team to depend on.

We are less interested in whether your implementation is complete, and more interested in **what decisions you made and why**. Every architectural choice is an opportunity to show us how you think.

---

## What's already provided

| File | What it does |
|---|---|
| `src/code_location_de/code_location_de/resources/api_client.py` | `FakeStoreAPIResource` — a Dagster `ConfigurableResource` wrapping the FakeStore HTTP API |
| `src/code_location_de/code_location_de/resources/__init__.py` | Environment-aware resource routing (local vs. prod) |
| `src/code_location_de/code_location_de/assets/ingestion/raw_data.py` | Three Dagster assets that fetch and land raw data: `raw_products`, `raw_users`, `raw_carts` |
| `src/code_location_de/code_location_de/assets/dbt_assets.py` | dbt integration (ignore this for Platform track — it's for DWH candidates) |
| `src/code_location_de/code_location_de_tests/test_ingestion.py` | Example tests showing the testing pattern |
| `notebooks/explore.ipynb` | Data exploration notebook |

---

## What you build

Implement your pipeline in:

```
src/code_location_de/code_location_de/assets/platform/pipeline.py
```

Your pipeline should:

1. **Consume the raw assets** — `raw_products`, `raw_users`, `raw_carts` are your inputs
2. **Clean and transform the data** — handle types, nulls, and the nested JSON in `raw_carts.products`
3. **Persist the results** — write structured tables that a BI tool or dbt could query
4. **Handle errors** — distinguish transient failures from data quality issues
5. **Be observable** — meaningful metadata on `MaterializeResult`, useful log messages
6. **Be testable** — add tests in `code_location_de_tests/test_pipeline.py`

---

## Decision points

These are the moments where there is no single right answer. We want to see what you chose and why. Mark each choice with a `# DECISION:` comment in your code.

### 1. Asset granularity

Should you implement one `@asset` per entity (cleaned_products, cleaned_users, cleaned_carts), or a single `@multi_asset` that produces all three?

Consider: parallelism, independent re-materialization, testing complexity, boilerplate.

### 2. IO Manager vs. explicit writes

Option A: Return a `pd.DataFrame` from your asset and let `DuckDBPandasIOManager` handle the write.
Option B: Use `duckdb.connect()` inside the asset body to write explicitly.

Consider: control vs. simplicity, schema ownership, what Dagster can see.

### 3. Resource design

The provided `FakeStoreAPIResource` is a starting point. Do you extend it? Replace it? Wrap it?

Consider: how do you make it testable (injectable vs. global)? What configuration does it need in production?

### 4. Partitioning

`raw_carts` has a `date` column ranging from late 2019 to early 2020. Should your pipeline be partitioned by date?

Consider: the FakeStore API returns all data at once — you can't filter by date on the API side. Does that change your answer? When does partitioning help vs. add complexity for no gain?

### 5. Error handling

Your pipeline will encounter at least two kinds of failures:
- **Transient errors**: the API returns a 500, DuckDB is temporarily locked
- **Data quality issues**: a required field is null, a product ID in a cart doesn't exist

How do you distinguish them? Where does the retry/alert boundary sit — at the asset level, with a `RetryPolicy`, with asset checks, or somewhere else?

### 6. Testing strategy

Look at `test_ingestion.py` for the testing pattern. Now decide: what do you actually unit-test with a mock, and what do you test with a real DuckDB connection?

Consider: what test would have caught a bug you introduced while building this? Are you testing behavior or just asserting that code runs?

### 7. Observability

What metadata is worth attaching to `MaterializeResult`? What would a data platform engineer need to debug a silent data quality failure three days after it happened — without re-running the pipeline?

---

## Stretch goals (only if time allows)

These are genuinely optional. Do them only if you have time and they interest you.

- Add a `ScheduleDefinition` or `SensorDefinition` that would trigger the pipeline automatically
- Implement a custom `IOManager` that writes to both DuckDB and a Parquet file
- Add `AssetChecks` in `checks/raw_checks.py` that validate the raw data before transformation begins
- Add freshness policies to your assets

---

## How to run

```bash
# Start Dagster UI
pixi run start-dev

# Run tests
make test

# Lint and format
make lint
make format
```

---

## A note on AI tools

You're encouraged to use GitHub Copilot, Cursor, Claude Code, or any other AI assistant. These are production tools and using them well is a skill.

What we care about: can you evaluate AI-generated code critically? Do you understand what it's doing? Have you adapted it to fit the actual requirements?

If you used an AI tool to generate a significant piece of code, leave a comment noting that — and explain what you changed or why you accepted it as-is.
