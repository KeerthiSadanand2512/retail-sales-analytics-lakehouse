# Notebook changes

The first full-data run used fixed catalog, schema, and input-path settings after problems with the widget setup. The executed notebook was exported on October 29, 2026. Its checksum and reconciliation summary are stored in [the execution record](notebook-export-evidence.json).

## Changes after that run

- Replaced widgets with validated configuration constants and a full-refresh flag that defaults to False.
- Added a six-table allowlist and checks for shared functions, expected columns, and nonempty input before writes.
- Selected the SQL catalog/schema once, removing fixed workspace paths from the queries.
- Removed duplicate queries and calculated monthly distinct orders directly from Silver.
- Moved the merchandise caption above its chart query and kept the description checks separate.
- Added Python/Spark version output for future run records.
- Consolidated the pipeline into `notebooks/01_pipeline.py`, preserving every code and Markdown cell from the earlier Jupyter version. Chart PNGs are stored separately.

Cleaning rules, financial calculations, and Gold aggregations were not changed by this cleanup. The shared notebook is loaded through relative `%run` and was not embedded in the original export.

## Checks and remaining work

Seven local preflight tests passed. Python source and cell parity with the earlier Jupyter version were checked before removing the duplicate. Preflight tests read the Python source directly. The Spark calls in these tests are mocked.

The updated Python notebook has now passed full-data row accounting and daily/product reconciliation on Python 3.12.3 and Spark 4.2.0; see [the run record](runtime-validation.md). A fresh repeat run and independent SQL outputs for this revision remain to be recorded. Environment version 6 is recorded in the export; the earlier Python/Spark versions and Git revision are unknown.

