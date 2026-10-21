# Validation status

Four converter unit tests pass locally: CSV quoting/multiline descriptions, duplicate and leading-zero preservation, blank IDs and ISO dates, sample labeling, refusal to overwrite, and invalid sample limits (some cases share a test).

The original workbook has been converted locally. Source and CSV checksums are recorded in `../reports/preparation.md`. This validates preparation, not Spark execution.

## Workspace acceptance still required

1. Run `02_smoke_checks` and record the exact pass message and environment.
2. Run sample `01_pipeline`; require source rows = Silver rows = accepted + rejected.
3. Require Gold daily and product net totals to equal eligible Silver.
4. Repeat with the identical input; compare business rows/counts and totals. Ingestion timestamps may change.
5. Review quality reasons, cancellations, missing customer coverage, and duplicate-looking rows before full-data interpretation.
6. Run full input and save sanitized evidence using the run-log template.
7. Check independent SQL totals against the notebook output before publishing findings.

No Spark/Delta/SQL runtime tests have passed yet. Local preparation is not a substitute for these checks.
