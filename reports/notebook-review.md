# Notebook changes

The first full-data run used fixed catalog, schema, and input-path settings after problems with the widget setup. The executed notebook was exported on October 29, 2026. Its checksum and reconciliation summary are stored in [the execution record](notebook-export-evidence.json).

## Changes after that run

- Replaced widgets with validated configuration constants and a full-refresh flag that defaults to False.
- Added a six-table allowlist and checks for shared functions, expected columns, and nonempty input before writes.
- Selected the SQL catalog/schema once, removing fixed workspace paths from the queries.
- Removed duplicate queries and calculated monthly distinct orders directly from Silver.
- Moved the merchandise caption above its chart query and kept the description checks separate.
- Added Python/Spark version output for future run records.
- Kept matching Python and Jupyter formats, with outputs and old chart settings removed. Chart PNGs are stored separately.

Cleaning rules, financial calculations, and Gold aggregations were not changed by this cleanup. The shared notebook is loaded through relative `%run` and was not embedded in the original export.

## Checks and remaining work

Seven local preflight tests passed. Python syntax, notebook structure, cleared outputs, and matching cells between the two formats were checked. The Spark calls in these tests are mocked.

The revised notebook still needs a Databricks run. The earlier results remain valid for the executed version, but do not establish runtime validation of later changes. Environment version 6 is recorded in the export; the earlier Python/Spark versions and Git revision are unknown.
