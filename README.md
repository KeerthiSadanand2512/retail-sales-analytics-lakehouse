# Retail Sales Analytics Lakehouse

A Data Engineering + Analytics learning project using **Databricks Free Edition, PySpark, Delta Lake, and SQL**.

**Status: guided Databricks sample and full-data runs validated from user-supplied outputs.** Full-data row accounting, daily/product financial reconciliation, repeated-run counts/totals, and independent SQL totals passed in the reported workspace results. Four local conversion tests also passed. The executed notebook was edited during setup troubleshooting; its export and runtime version still need to be captured. This is a learning project, with no production experience claimed.

See [validated findings](reports/findings.md) for results and limitations and [chart export instructions](reports/chart-export.md) for the remaining visual artifacts.

## Dataset

[UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail), by Daqing Chen (2015), DOI [10.24432/C5BW33](https://doi.org/10.24432/C5BW33). UCI describes 541,909 retail transaction lines from December 1, 2010 through December 9, 2011, with prices in sterling. License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). These source facts are not pipeline findings.

The conversion preserves records and duplicates, formats timestamps as ISO text, and writes UTF-8 CSV. Raw data and customer-level outputs are excluded from Git. See [source contract](docs/data-contract.md).

## Start in Databricks

Follow [the step-by-step setup](docs/setup.md). Import the three Python source notebooks together into the same workspace folder, then run:

1. `02_smoke_checks` — invented edge cases, no persistent tables.
2. `01_pipeline` — enter the catalog, dedicated schema, and uploaded CSV path; explicitly allow full refresh.
3. `sql/sales_analysis.sql` — select the same catalog/schema in the SQL editor.

`00_transformations` supplies shared functions via `%run`. The guided workspace run passed synthetic checks and sample/full-data reconciliation; exact repository-version reproduction remains pending. Begin with the 10,000-row learning sample before the full dataset. The first rows are not representative of the whole observation period.

## Workflow

```text
UCI XLSX -> local CSV conversion -> uploaded CSV in Unity Catalog volume
       -> Bronze Delta -> Silver Delta + rejects -> Gold Delta -> SQL analytics
```

The pipeline creates or replaces six project tables in a dedicated schema: `retail_bronze`, `retail_silver`, `retail_rejects`, `retail_gold_daily`, `retail_gold_product`, and `retail_gold_customer`. It checks row accounting and daily/product financial reconciliation. It preserves duplicate-looking lines because the source does not supply a reliable unique line key. Tables refresh individually; this is not an atomic multi-table transaction. Run one refresh at a time.

## Business questions

- How do monthly recorded sales, returns, and sale-order counts change?
- Which products contribute the most recorded sales?
- What proportion of identified purchasing customers place repeat orders?
- How do invalid values and missing customer IDs affect metric coverage?

Profit and margin are out of scope because product costs are absent. Cancellation/negative-line values are reported as source-recorded adjustments, not proof of completed refunds. December 2010 and December 2011 have unequal coverage.

## Project files

| Folder | Contents |
| --- | --- |
| `scripts/` | Deterministic workbook-to-CSV conversion |
| `notebooks/` | Shared PySpark logic, batch pipeline, synthetic checks |
| `sql/` | Monthly sales, product contribution, repeat purchasing, coverage queries |
| `tests/` | Local converter unit tests |
| `docs/` | Setup, architecture, contract, metrics, roadmap, validation |
| `reports/` | Local preparation evidence and Databricks run-log template |
| `data/` | Instructions; source files remain outside Git |

## Zero-cost learning scope

Use [Databricks Free Edition](https://docs.databricks.com/aws/en/getting-started/free-edition), available serverless resources, manual upload, and small batches. No external paid cloud services are required. Free Edition has [usage and feature limits](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations); wait if quotas are exhausted. Documentation checked October 21, 2026.

See [validation evidence](reports/preparation.md), [metric rules](docs/metrics.md), and [roadmap](docs/roadmap.md). No new software license is applied by this update; the source dataset retains its own attribution requirements.
