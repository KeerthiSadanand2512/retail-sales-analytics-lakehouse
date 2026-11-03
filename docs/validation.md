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

The preflight tests mock Spark access. They test failure handling, not Delta persistence or Spark SQL. The Python notebook was checked against the earlier Jupyter version before the duplicate was removed. All code and Markdown cells were preserved. Preflight tests now read the Python source directly.

## Updated Python notebook run

The updated `01_pipeline.py` was run on Python 3.12.3 and Spark 4.2.0. Its reported full-data counts and net sales match the table above, and row accounting plus daily/product reconciliation passed. See [the run record](../reports/runtime-validation.md).

The updated Python notebook was run a second time with the same counts and net total, as recorded in the run record. Sales and customer SQL results were also checked during dashboard construction against the earlier validated totals.

The earlier export records Databricks environment version 6. Exact Python/Spark versions and the Git revision of that run were not captured. Use the [run-record template](../reports/databricks-run-template.md) for the next run.


## Dashboard import

On November 3, 2026, a new copy imported from the saved dashboard definition displayed the expected KPI values, both charts, merchandise sort order, and coverage notes. This was a visual check using the existing project tables, not a clean-workspace rebuild or an automated refresh audit. See [the import record and screenshot](../reports/dashboard-import-check.md).
