# Data Engineer Challenge

Congratulations — you made it to the technical challenge round. We're genuinely excited to see how you approach this.

This repository contains a hands-on data engineering challenge for two specialization tracks. We use it across our hiring process because it reflects the kind of work our team does every day.

**What matters most to us is not a perfect implementation — it's how you think.** We want to see the decisions you make, the trade-offs you consider, and how you communicate your reasoning.

---

## Choose your track
We belive that a modern data engineer has two main areas: 

### Platform Engineer

You're interested in the infrastructure layer: how data pipelines are built, orchestrated, and maintained. You care about reusability, testability, and making the right architectural decisions.

→ Read [docs/platform_track.md](docs/platform_track.md) for the full brief.

### DWH Engineer

You're interested in the data modeling layer: how raw data is shaped into clean, business-ready tables. You care about SQL quality, data contracts, and making data useful for analysts and BI tools.

→ Read [docs/dwh_track.md](docs/dwh_track.md) for the full brief.

---

## The scenario

You work at a fictional company that runs an online shop. The company's product catalog, user base, and order history are exposed through a REST API:

**FakeStore API:** https://fakestoreapi.com

Three endpoints are available:

| Endpoint | What it returns |
|---|---|
| `/products` | Product catalog (20 items across 4 categories) |
| `/users` | Registered customers (10 users) |
| `/carts` | Shopping carts / orders (20 carts with line items) |

The data engineering team needs to ingest this data, transform it, and make it available for reporting. Your task is to build that pipeline — or the data model on top of it, depending on your track.

---

## Quick start (GitHub Codespaces — recommended)

1. Click **"Code" → "Open with Codespaces"** at the top of this page
2. Wait for the environment to build (~2 minutes)
3. Run `pixi run start-dev` in the terminal
4. Open the Dagster UI at **localhost:3000**
5. Materialize the **`ingestion`** asset group (this fetches data from the API and writes it to DuckDB)
6. Open `notebooks/explore.ipynb` with the `dev` kernel to explore the raw data
7. Choose your track and start building — see `docs/` for your brief

---

## Local setup

Requirements: [pixi](https://pixi.sh) (the project uses pixi for dependency management)

```bash
# Install all dependencies
pixi install -e dev

# Start Dagster dev server
pixi run start-dev

# Open Jupyter Lab
pixi run notebook
```

Other useful commands:

```bash
make lint          # Run ruff linter
make format        # Auto-format with ruff
make typecheck     # Run pyright
make test          # Run pytest with coverage
make dbt-run       # Run all dbt models
make dbt-test      # Run all dbt tests
make dbt-docs      # Generate and serve dbt documentation
```

---

## Stack

| Tool | Purpose |
|---|---|
| [Dagster](https://dagster.io) | Data orchestration and asset lineage |
| [dbt](https://www.getdbt.com) | SQL transformations and data modeling |
| [DuckDB](https://duckdb.org) | Local analytical database |
| [Pixi](https://pixi.sh) | Dependency and environment management |
| [Ruff](https://docs.astral.sh/ruff/) | Python linting and formatting |
| [Pyright](https://github.com/microsoft/pyright) | Static type checking |
| [pytest](https://pytest.org) | Testing framework |
| [Jupyter Lab](https://jupyterlab.readthedocs.io) | Data exploration |

---

## What we're looking for

**For Platform Engineers:**
- Architectural decision-making — what trade-offs did you consider and why did you land where you did?
- Reusable, testable code — could another engineer extend this without needing to ask you?
- Observability — does the pipeline tell you what happened when something goes wrong?
- Pragmatism — a working, well-reasoned solution beats an elegant but incomplete one

**For DWH Engineers:**
- Data modeling craft — is the model correct, clear, and maintainable?
- SQL quality — is the SQL readable, well-structured, and appropriately tested?
- Business understanding — do the mart models answer real business questions?
- Documentation — would an analyst be able to use your models without asking you?

---

## Project structure

```
.
├── docs/
│   ├── platform_track.md     # Platform Engineer brief
│   └── dwh_track.md          # DWH Engineer brief
├── src/
│   ├── code_location_de/     # Dagster code location (Python)
│   │   └── code_location_de/
│   │       ├── assets/
│   │       │   ├── ingestion/    # PROVIDED: raw data ingestion from API
│   │       │   └── platform/     # STUB: Platform Engineer implements here
│   │       ├── resources/        # PROVIDED: API client, IO manager config
│   │       └── checks/           # STUB: DWH Engineer adds asset checks here
│   └── code_location_de_dbt/ # dbt project (SQL transformations)
│       └── models/
│           ├── staging/      # STUB: one model per raw source table
│           ├── intermediate/ # STUB: joins and unnesting
│           └── marts/        # STUB: reporting-ready tables
├── notebooks/
│   └── explore.ipynb         # PROVIDED: explore raw API data
├── pyproject.toml            # Dependencies and tool config (Pixi)
├── workspace.yaml            # Dagster workspace config
└── Makefile                  # Convenience commands
```

---

## Submitting your work

1. Fork this repository
2. Implement your solution on a branch
3. Open a pull request back to the main branch of your fork (so we can see a clean diff)
4. Share the repository link with us

Include a short write-up in your PR description:
- What you implemented vs. what you skipped and why
- Anything you'd do differently with more time
- Which AI tools you used and how

---

## Useful reading

Before you start, we recommend spending 30–60 minutes with these resources:

- [Dagster concepts: Assets](https://docs.dagster.io/guides/build/assets/)
- [Dagster concepts: Resources](https://docs.dagster.io/guides/build/external-resources/)
- [Dagster concepts: Asset checks](https://docs.dagster.io/guides/test/asset-checks)
- [dbt: How we structure our projects](https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview)
- [dbt: Testing](https://docs.getdbt.com/docs/build/data-tests)
- [DuckDB: JSON functions](https://duckdb.org/docs/extensions/json)

You don't need to read all of this — it's here so you know where to look when you need it.

---
