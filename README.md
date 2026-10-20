# Retail Sales Analytics Lakehouse

A planned Data Engineering + Analytics learning project using **Databricks Free Edition, PySpark, Delta Lake, and SQL**.

**Status: documentation scaffold only.** No ingestion pipeline, executed notebooks, Delta tables, tests, dashboard, or measured results are included yet. This is intended as a future flagship portfolio project, not a production system.

## Business questions

- How do recorded sales and order counts change by month?
- Which products and countries account for the largest share of recorded sales?
- How do basket value and repeat purchasing vary across customers?
- How do returns, missing identifiers, and duplicates affect these metrics?

Profit and margin will not be reported unless the selected dataset supports a documented cost model. Sales do not establish profit or causal business impact.

## Planned workflow

```text
Approved retail CSV -> Bronze Delta -> Silver Delta -> Gold Delta -> SQL analysis -> report/dashboard
                         raw records     typed/clean     metric tables
```

The initial scope is a small, manually triggered batch workflow. Dataset selection, licensing review, schema decisions, implementation, and runtime validation remain open.

## Start here

1. Read [the roadmap](docs/roadmap.md) and [architecture](docs/architecture.md).
2. Follow [Free Edition setup](docs/setup.md); use the no-cost Free Edition rather than a paid cloud trial.
3. Select a dataset and complete [the source record and proposed data contract](docs/data-contract.md).
4. Implement notebooks in the order described in [notebooks/README.md](notebooks/README.md).
5. Record quality checks and rerun evidence using [the validation plan](docs/validation.md).
6. Publish findings only after reconciling SQL outputs with the curated tables.

## Repository structure

| Folder | Purpose |
| --- | --- |
| `docs/` | Architecture, setup, data contract, metrics, roadmap, validation |
| `notebooks/` | Planned numbered Databricks notebooks |
| `src/` | Future reusable PySpark transformations |
| `sql/` | Future Gold models and analytical queries |
| `tests/` | Future fixtures and transformation/quality checks |
| `reports/` | Future findings, figures, and execution evidence |
| `data/` | Dataset instructions only; raw and generated data excluded |

## Zero-cost scope

Use the Databricks Free Edition workspace, its available serverless resources, small batches, and manual data upload. No paid cloud storage, external cloud account, paid connector, or always-on service is required by this plan. Free Edition is quota-limited; resource availability is not guaranteed. Stop when quota is exhausted instead of switching to paid compute.

See the official [Free Edition signup guide](https://docs.databricks.com/aws/en/getting-started/free-edition) and [limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations). Features and limits can change; verify them before implementing. Documentation checked on October 20, 2026.

## Evidence and attribution

All implementation milestones are pending. Record the dataset publisher, source URL, license, date range, units, and limitations before use. Do not reuse private project files or publish customer personal data. No dataset or software license is granted by this scaffold; choose an appropriate code license separately and retain source attribution.
