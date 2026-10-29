# Executed notebook review

The user supplied `01_pipeline.ipynb` after the guided Databricks run. The original file remains unchanged locally. Its source checksum and explicit aggregate reconciliation stream are preserved in [notebook-export-evidence.json](notebook-export-evidence.json). The notebook metadata specifies Databricks environment version **6**; it does not establish the original Python/Spark versions or the exact executed Git revision. The shared transformations notebook was referenced by relative `%run`, not embedded in the export.

## Changes

- Replace widget setup with explicit constants, identifier/path validation, a six-table allowlist, and an opt-in full-refresh flag defaulting to False.
- Check shared-function availability and input header/row count before any project table is overwritten. A second count checks Bronze against input; the file must stay immutable throughout the run.
- Select catalog/schema once for the subsequent unqualified SQL statements, removing embedded workspace paths from queries.
- Remove repeated sales/customer/coverage queries and redundant description-check queries.
- Compute monthly distinct sale invoices directly from Silver instead of summing daily distinct counts.
- Put the reviewed-merchandise caption directly above its ranking; retain separate postage and product-description checks, with partial-December and customer-coverage caveats.
- Add runtime-version output for future run logs. Export synchronized `.py` and `.ipynb` formats.
- Clear outputs, execution counts, command identifiers and old chart metadata. Keep only original aggregate reconciliation evidence in the separate JSON; no customer-level outputs are published. Earlier PNG chart exports remain in reports/figures.

## Validation

Seven local preflight tests passed: valid settings, invalid names/nonproject schema, unsafe or malformed input paths, the table allowlist, refresh opt-in before Spark access, missing shared functions before Spark access, and empty input preventing schema/table writes. These tests use mocks for Spark access and do not validate Spark SQL or Delta execution.

Python cells parse after excluding notebook magics. The exported source and Jupyter versions contain the same logical cells. JSON notebook structure is checked and all outputs/execution counts are cleared. Shared cleaning and Gold aggregation rules are unchanged from the repository version inspected during review.

**The revised notebook has not run in Databricks.** Historical validated results belong to the supplied executed export and conversation evidence. A fresh smoke check, full run, repeat run and SQL reconciliation are required before claiming runtime validation of this revision. The refresh remains a sequence of separate table transactions; partial failure requires a full rerun. This review does not establish production readiness or automated scheduling.

