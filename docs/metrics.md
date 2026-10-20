# Proposed metrics

Status: definitions to validate after dataset selection; no numerical results exist.

- **Signed line value:** quantity × unit price, using decimal arithmetic and the source currency.
- **Gross positive sales:** sum of eligible positive sale-line values.
- **Return value:** absolute value of eligible negative return-line values, if the source encodes returns that way.
- **Net recorded sales:** gross positive sales minus return value under documented source rules. Do not call this recognized revenue without evidence.
- **Orders:** distinct eligible transaction IDs under a declared sale/cancellation policy. Count orders from line data, not rows; do not sum distinct-order counts across overlapping product groups.
- **Average order value:** sale-only sales divided by sale-only distinct orders for the same population and currency. Return NULL for a zero denominator.
- **Repeat customers:** customers with at least two distinct qualifying sale orders in the observed period. Exclude missing IDs from the customer denominator and report their coverage.

Group by currency before aggregation. Define date boundaries, treatment of partial periods, missing IDs, returns, and price anomalies in the final findings. Customer behavior describes this dataset's observation window only. Profit, margin, forecasts, and business improvement claims are outside the initial evidence.
