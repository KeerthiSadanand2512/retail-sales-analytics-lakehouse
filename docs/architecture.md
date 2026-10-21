# First batch architecture

Implementation prepared; Databricks execution pending.

The local converter reads the UCI workbook and writes an immutable CSV. Upload this file to a Unity Catalog volume. The notebook uses the workspace's existing catalog, a dedicated `retail_` schema, and serverless compute.

| Managed Delta table | Grain |
| --- | --- |
| retail_bronze | One original input row, plus ingestion metadata |
| retail_silver | One source row, typed analytical fields and quality reasons |
| retail_rejects | Ineligible subset of Silver |
| retail_gold_daily | Date and currency |
| retail_gold_product | Product ID and currency |
| retail_gold_customer | Nonmissing customer ID and currency, positive sale lines only |

`00_transformations` defines reusable cleaning/aggregation functions. Both the pipeline and synthetic smoke checks import it with `%run`. `01_pipeline` enforces explicit full-refresh opt-in, writes six Delta tables, checks Bronze/Silver/reject row accounting, and reconciles daily/product totals to eligible Silver.

Each write replaces one table. This is a single-user learning workflow, not an atomic multi-table refresh or production orchestration system. Re-run the entire notebook if interrupted and never run concurrent refreshes. Same-input rerun behavior still needs workspace evidence. Incremental MERGE, streaming, production security, and scalability claims are out of scope.
