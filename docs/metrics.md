# Implemented metric definitions

Runtime validation is pending. All monetary measures are GBP under the UCI source description.

- **Line value:** signed quantity × decimal unit price for eligible rows.
- **Gross sales:** sum of positive eligible line values, including sales with missing customer IDs.
- **Return value:** absolute sum of negative eligible line values. This is a source-recorded return/cancellation adjustment proxy, not verified refunded cash.
- **Net sales:** gross sales minus return value. No cost, tax, or revenue-recognition model is inferred.
- **Sale orders:** distinct invoice IDs among eligible positive-quantity lines. Count at the requested grain; product-level distinct counts must not be summed into overall order counts.
- **Average sale-order value:** gross sales / distinct sale orders in the same period; NULL for zero denominator.
- **Repeat-customer share:** share of identified purchasing customers with at least two qualifying positive sale invoices in the observed input. Excludes missing IDs and cancellations from order counts; disclose ID coverage separately.

The small sample is a pipeline-learning input, not a basis for full-period claims. December 2011 ends on the ninth; raw month-to-month growth is not a comparable-period growth metric. Duplicate-looking lines remain in all metrics. High-volume lines and adjustments should be investigated before drawing business conclusions.
