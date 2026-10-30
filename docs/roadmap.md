# Project progress

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
- Added local conversion and notebook preflight tests.
- Ran the updated Python notebook on Python 3.12.3 and Spark 4.2.0 with matching full-data reconciliation.

## Next

- Record a repeat run and independent SQL checks for the updated notebook, with its exact executed Git revision.
- Update the monthly chart axis from “Total Sales” to “Net Sales (GBP).”
- Build a dashboard from the validated metrics.

## Later

Consider incremental loading after establishing a reliable line key, followed by scheduling within Free Edition limits. These features are not implemented yet.
