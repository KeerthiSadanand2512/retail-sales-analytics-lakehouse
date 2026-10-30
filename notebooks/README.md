# Databricks notebooks

Keep these notebooks in the same workspace folder:

| Notebook | Purpose |
| --- | --- |
| `00_transformations.py` | Shared cleaning and aggregation functions |
| `02_smoke_checks.py` | Synthetic edge cases; run before loading the source |
| `01_pipeline.py` or `01_pipeline.ipynb` | Ingestion, Delta tables, reconciliation, and SQL analysis |

The two pipeline formats contain the same cells. Import one, not both under the same name.

Edit the pipeline's configuration constants, review the six target tables, and set `ALLOW_FULL_REFRESH = True` when ready. Defaults use the sample file and disable writes. Run from the beginning so shared functions and SQL context are established.

The original full-data run passed reconciliation. The current cleaned revision needs a fresh run; see [validation](../docs/validation.md). Chart settings must be recreated after import; saved images are in [reports/figures](../reports/figures/).
