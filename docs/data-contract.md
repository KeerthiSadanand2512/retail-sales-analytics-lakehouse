# Source record and proposed data contract

Status: dataset not selected. The fields below are a proposed logical model, not claims about an existing file.

## Complete before ingestion

- Dataset title, publisher, and source URL: pending
- License and permitted redistribution: pending
- Download date, file checksum, and source version: pending
- Observation period, geography, currency, and timezone: pending
- Source grain, business key, and return/cancellation rules: pending
- Source-to-model field mapping and parsing formats: pending
- Personal information review: pending

Use a small openly licensed retail transaction dataset or clearly labeled synthetic data. Keep raw files outside Git until rights and privacy have been reviewed. Public availability alone does not grant redistribution rights.

| Logical field | Intended type | Rule to confirm against source |
| --- | --- | --- |
| transaction_id | string | Required for order metrics; not necessarily unique per line |
| transaction_timestamp | timestamp | Explicit date format and timezone policy |
| product_id | string | Required for product analysis; retain leading zeros |
| quantity | decimal | Signed return semantics; confirm whether fractional units are possible |
| unit_price | decimal | Explicit precision/scale and source currency |
| customer_id | string, nullable | Pseudonymous ID only; never publish identifiable values |
| country | string, nullable | Recorded location, not inferred nationality |
| currency | string | Source-supported currency; no guessing |

Define overflow, invalid-date, null, zero-price, negative-price, and duplicate policies after profiling. Rejected rows must be counted and explained. Preserve the immutable original input outside Git for reconciliation.
