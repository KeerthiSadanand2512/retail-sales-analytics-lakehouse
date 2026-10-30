# UCI Online Retail data contract

## Attribution and source

Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. [DOI](https://doi.org/10.24432/C5BW33). [Dataset page](https://archive.ics.uci.edu/dataset/352/online+retail). [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Downloaded October 21, 2026. Original workbook checksum: `43465a06f2ccf7c8b5bd2892bc7defb52f97487934fe93b16ae4c3936424676d`. UCI describes 541,909 lines, December 1, 2010–December 9, 2011. Prices are sterling (GBP); country is the recorded customer country. Timezone is not supplied; use naive local timestamps (`TIMESTAMP_NTZ`) without applying a UTC conversion.

## Field mapping

| Source field | Analytical field/type | Policy |
| --- | --- | --- |
| InvoiceNo | invoice_id/string | Trim; required; C prefix means cancellation |
| StockCode | product_id/string | Trim; required; do not require numeric-only codes |
| Description | original string | Retained; not required for sales eligibility |
| Quantity | quantity/int | Signed whole number; nonzero; invalid/overflow rejected |
| InvoiceDate | invoice_timestamp/timestamp_ntz | Converter emits ISO text; invalid/missing rejected |
| UnitPrice | unit_price/decimal(18,6) | Positive required; invalid/overflow rejected; source precision retained up to six decimal places |
| CustomerID | customer_id/nullable string | Missing ID allowed for sales; excluded from customer aggregates |
| Country | original nullable string | Retained; no inference |

Bronze retains source values plus filename, ingestion time, and input path. Silver retains every row, adds `eligible` and pipe-delimited `quality_reasons`. Rejects are the ineligible subset, not additional source records. A positive quantity on a cancellation invoice is quarantined as inconsistent. Negative quantities on other invoices are retained as adjustments and must not be assumed to be confirmed refunds.

No deduplication: invoice/product alone is not a proven line key. Identical lines can be counted separately; quantify their impact before any future policy change. Zero and negative prices are retained in Silver but excluded from current monetary metrics. Product codes may include postage/charges; review code semantics before calling rankings merchandise demand.

Raw data and customer-level outputs are not committed. The conversion changes representation, not business records. Results are historical and do not measure profit or causal impact.

