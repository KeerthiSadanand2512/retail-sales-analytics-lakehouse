# Proposed architecture

Status: design only; nothing has run in Databricks yet.

## Storage and naming

Use an available Unity Catalog catalog in the Free Edition workspace. Create a dedicated project schema such as `retail_learning`; do not assume permission to create a catalog. Upload a small approved CSV into a Unity Catalog volume when supported. Record the actual catalog, schema, and `/Volumes/<catalog>/<schema>/<volume>/...` path in the run log; keep credentials out of the repository.

Use fully qualified managed Delta table names. Proposed tables:

| Table | Grain and purpose |
| --- | --- |
| `bronze_retail` | Source row with original strings, source filename, ingestion time, and batch identifier |
| `silver_retail` | Typed transaction line retaining return flags and quality outcomes |
| `silver_retail_rejects` | Rows excluded from analytical eligibility, with explicit rejection reasons |
| `gold_daily_sales` | Date and currency, with documented measures |
| `gold_product_sales` | Product and currency, with documented measures |
| `gold_customer_summary` | Non-sensitive customer identifier and currency; exclude missing IDs from customer metrics only |

These names and grains must be finalized after source profiling. A missing customer ID need not invalidate an otherwise usable sales line.

## Transformation policy

Bronze preserves source information. Silver parses timestamps, quantities, and decimal prices, identifies cancellations/returns using source-specific rules, and documents handling of missing values and duplicates. Do not silently remove negative quantities or infer a line key from invoice and product alone: repeated legitimate lines may exist.

Gold separates gross positive sales, returns, and signed net sales when supported by source semantics. Preserve currency; never sum different currencies without a documented conversion policy.

## Reruns

Begin with a documented full-refresh strategy for project-owned tables only. On the same immutable input and configuration, reruns must produce identical business rows and aggregates, apart from ingestion metadata. Do not append the same batch twice. Incremental MERGE processing is a later milestone requiring a validated business key and late-data policy.

## Out of initial scope

Streaming, external cloud infrastructure, production SLAs, real customer identifiers, and claims about production scalability. Separate this new learning implementation from prior academic retail work; do not copy its data without reviewing reuse rights.
