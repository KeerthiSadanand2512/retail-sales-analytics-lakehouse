# Project progress

The manual batch pipeline, SQL analysis, and dashboard scope is complete.

## Completed

- Selected UCI Online Retail and recorded its source, license, and field definitions.
- Converted the workbook to CSV and prepared a 10,000-row sample.
- Built the Bronze, Silver, rejects, and Gold Delta tables.
- Ran the synthetic checks and the sample pipeline in Databricks.
- Processed all 541,909 source lines and reconciled the sales totals.
- Repeated the full-data run with unchanged row counts and net sales.
- Cross-checked the totals and monthly order counts with SQL.
- Checked the descriptions of the top merchandise codes and separated postage.
- Published the findings and two chart exports.
- Built the Retail Sales Overview dashboard and saved its definition and screenshot.
- Imported the dashboard export into a new copy and checked its displayed metrics, charts, sorting, and notes.
- Added local conversion and notebook preflight tests.
- Ran the updated Python notebook on Python 3.12.3 and Spark 4.2.0 with matching full-data reconciliation.

## Next

- Capture the exact executed Git revision for future runs; the updated notebook's repeat run and dashboard SQL totals have been recorded.
- Update the monthly chart axis from “Total Sales” to “Net Sales (GBP).”
- Publish the dashboard in Databricks only if a hosted view is needed; the repository already includes its export and screenshots.

## Later

Incremental loading requires a reliable record or batch identity and remains unimplemented. Scheduling is configured as described below, within Free Edition limits.

## Scheduling extension

- [x] Create a serverless notebook job and pass one manual job run.
- [x] Save an active daily 09:00 America/Toronto schedule.
- [ ] Verify a schedule-triggered run and its reconciliation output.
- [x] Prepare incremental Bronze ingestion, stable source-row identities, and local checks.
- [ ] Validate the incremental batch/replay sequence in Databricks before deploying it.

