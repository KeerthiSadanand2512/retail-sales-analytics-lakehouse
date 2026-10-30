# Validation

## Completed Databricks run

The full-data run produced the following reconciliation summary:

| Check | Result |
| --- | ---: |
| Input lines | 541,909 |
| Eligible lines | 539,392 |
| Rejected lines | 2,517 |
| Eligible net sales (GBP) | 9,769,872.054 |

Input lines equaled eligible plus rejected lines. Daily and product Gold totals matched eligible Silver. A second run returned the same counts and net total. Independent SQL matched gross sales, adjustments, net sales, and 19,960 sale orders. Monthly distinct-order counts were also checked directly from Silver.

The [export record](../reports/notebook-export-evidence.json) preserves the original notebook checksum and printed reconciliation summary. The [findings](../reports/findings.md) include the SQL results and coverage limits.

## Local tests

- Four workbook-conversion tests cover CSV quoting, date formatting, blanks, duplicates, sample limits, and overwrite protection.
- Seven notebook preflight tests cover configuration, allowed table names, refresh opt-in, shared-function availability, and empty input before writes.

The preflight tests mock Spark access. They test failure handling, not Delta persistence or Spark SQL. The source and Jupyter notebook formats have also been checked for matching cells, Python syntax, and cleared outputs.

## Remaining check

The current notebook includes configuration and query cleanup made after the successful run. It has not yet been rerun in Databricks. Run the smoke checks, sample, full input, repeat refresh, and SQL cross-check again before recording runtime validation for that revision.

The earlier export records Databricks environment version 6. Exact Python/Spark versions and the Git revision of that run were not captured. Use the [run-record template](../reports/databricks-run-template.md) for the next run.
