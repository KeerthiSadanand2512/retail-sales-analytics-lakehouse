# Databricks notebooks

Keep these notebooks in the same workspace folder:

| Notebook | Purpose |
| --- | --- |
| `00_transformations.py` | Shared cleaning and aggregation functions |
| `02_smoke_checks.py` | Synthetic edge cases; run before loading the source |
| `01_pipeline.py` | Ingestion, Delta tables, reconciliation, and SQL analysis |

`01_pipeline.py` is the only pipeline notebook. It includes configuration, ingestion, reconciliation, SQL analysis, and explanatory Markdown cells in Databricks source format. The shared functions and smoke checks remain separate supporting notebooks.

Edit the pipeline's configuration constants, review the six target tables, and set `ALLOW_FULL_REFRESH = True` when ready. Defaults use the sample file and disable writes. Run from the beginning so shared functions and SQL context are established.

The original full-data run passed reconciliation. The updated Python notebook also passed full-data reconciliation on Python 3.12.3 and Spark 4.2.0; see [validation](../docs/validation.md). Chart settings must be recreated after import; saved images are in [reports/figures](../reports/figures/).

