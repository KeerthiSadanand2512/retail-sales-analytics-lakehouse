# Databricks notebooks

Import `00_transformations.py`, `02_smoke_checks.py`, and one pipeline format into the same folder. Choose either `01_pipeline.py` (Databricks source) or `01_pipeline.ipynb` (Jupyter), which contain the same cells; do not create two copies named 01_pipeline.

Run the smoke checks first. In the pipeline, edit the configuration constants and inspect the six target names, then enable `ALLOW_FULL_REFRESH` explicitly. Defaults point to the learning sample and disable writes. Run all cells sequentially so shared functions and SQL catalog/schema context are established.

The original export recorded passing full-data results. This reviewed revision is output-free and needs a new Databricks run. See [review](../reports/notebook-review.md), [original aggregate evidence](../reports/notebook-export-evidence.json), and [setup](../docs/setup.md). Recreate chart settings after importing; previous PNG exports are retained separately.

