# Planned Databricks notebooks

No executable notebooks are included yet.

1. `00_profile_source` — inspect the approved input and finalize the data contract.
2. `01_ingest_bronze` — preserve source rows and ingestion metadata in Delta.
3. `02_clean_silver` — type fields, record quality outcomes, and apply documented policies.
4. `03_build_gold` — create reconciled metric tables.
5. `04_analyze_sales` — answer business questions with SQL and visualizations.
6. `05_validate` — record reconciliation and rerun checks.

Export reviewable source files after implementation. Keep credentials and sensitive outputs out of notebooks. Record the execution order, parameters, and actual runtime environment.
