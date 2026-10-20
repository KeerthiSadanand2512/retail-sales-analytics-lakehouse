# Validation plan

Status: proposed checks only; no tests have run.

## Required acceptance evidence

1. Record input checksum, source rows, schema, missingness, date range, and currency coverage.
2. Reconcile each Bronze row to an accepted or rejected processing outcome. Document any explicit deduplication separately and prove its key does not discard legitimate lines.
3. Check typed fields, decimal precision, date parsing, required identifiers, return flags, and quality reasons with small synthetic edge cases.
4. Reconcile Silver signed line value to Gold totals by currency and period. Explain all exclusions. Compare independent SQL and PySpark calculations.
5. Run twice against the same immutable input. Confirm unchanged business row counts and metrics, with no duplicate ingestion.
6. Check empty input, invalid timestamps, null customer IDs, duplicate-looking legitimate lines, returns, zero prices, and zero-denominator metrics.
7. Run in the actual Free Edition workspace and record the environment, revision, timestamp, row counts, check results, and limitations.

Completion requires executable source, reproducible setup, successful runtime evidence, and findings linked to reconciled outputs. A folder or test plan is not a passed test. Redact private identifiers and sensitive notebook outputs before publishing evidence.
