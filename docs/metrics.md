# Metric definitions

All monetary measures use GBP. Calculations retain decimal precision; chart labels may round for display.

| Metric | Definition |
| --- | --- |
| Line value | Signed quantity × unit price for an eligible line |
| Gross sales | Sum of eligible positive line values |
| Return value | Absolute sum of eligible negative line values |
| Net sales | Gross sales minus return value |
| Sale orders | Distinct invoice IDs on eligible positive-quantity lines |
| Average sale-order value | Gross sales divided by sale orders for the same population and period; NULL when there are no orders |
| Repeat-purchasing share | Identified purchasing customers with at least two qualifying sale invoices, divided by all identified purchasing customers |
| Missing customer-ID share | Eligible lines without a customer ID, divided by all eligible lines |

## Interpretation

`return_value` is the source-recorded adjustment amount. It does not establish that a refund was paid. Net sales include postage and other eligible charges; the merchandise chart separately excludes the identified postage codes `DOT` and `POST`.

Customer metrics exclude missing IDs, while sales totals include otherwise eligible lines with missing IDs. Repeat purchasing refers only to the observed period and is not a retention rate.

Count distinct invoices at the required reporting grain. Product-level or daily distinct counts are not generally additive; monthly order counts in the current notebook are calculated directly from Silver.

Duplicate-looking source lines remain in the totals. December 2011 ends on December 9, and the 10,000-row sample covers only the first source rows. Neither should be treated as a complete comparison period. The dataset has no product costs, so profit and margin are not calculated.
