# Pipeline architecture

The pipeline runs as a manual batch in Databricks Free Edition. The source workbook is converted locally to CSV and uploaded to a Unity Catalog volume. PySpark then writes six managed Delta tables in a dedicated schema.

| Table | One row represents |
| --- | --- |
| `retail_bronze` | An input line with ingestion metadata |
| `retail_silver` | An input line with typed fields and quality flags |
| `retail_rejects` | An ineligible Silver line and its rejection reasons |
| `retail_gold_daily` | A date and currency |
| `retail_gold_product` | A product code and currency |
| `retail_gold_customer` | An identified customer and currency, using positive sale lines |

## Processing order

`00_transformations` holds the cleaning and aggregation functions shared by the pipeline and smoke checks. `01_pipeline` validates its configuration, checks the input, writes Bronze, builds Silver and Gold, and reconciles the results. SQL cells then calculate sales, repeat purchasing, and customer-ID coverage.

Bronze preserves the source. Silver retains both eligible and ineligible rows; `retail_rejects` is a convenient copy of the ineligible subset. Rejected rows must not be added to Silver counts as if they were extra input records.

## Refresh behavior

Each run replaces the six named tables. Full refresh is disabled by default, and the input is checked before Bronze is replaced. The file must remain unchanged during the run.

The tables are written separately, so a failed run can leave tables from different refreshes. Run one refresh at a time and rerun the entire pipeline after a failure. Incremental loading and scheduled orchestration are future work.

See [validation](validation.md) for completed checks and the remaining rerun of the latest notebook revision.
