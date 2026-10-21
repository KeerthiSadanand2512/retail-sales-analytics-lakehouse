# Databricks source notebooks

Import all three `.py` files into the same workspace folder as notebooks.

- `00_transformations.py`: shared cleaning and Gold aggregation functions.
- `02_smoke_checks.py`: run first; synthetic edge cases; no persisted tables.
- `01_pipeline.py`: parameterized CSV-to-Delta pipeline; review six target tables and allow full refresh explicitly.

Execution in the actual Free Edition workspace remains pending. See `../docs/setup.md`.
