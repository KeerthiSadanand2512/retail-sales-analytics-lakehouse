# Retail sales analysis — validated workspace results

Recorded October 29, 2026 from user-supplied Databricks output and screenshots. Full input runs and SQL reconciliation were reported October 28; product chart configuration and description checks were reviewed October 29. This is a historical learning project, not production or employment data.

## Results

| Metric | Full dataset result |
| --- | ---: |
| Input transaction lines | 541,909 |
| Eligible lines | 539,392 |
| Ineligible lines | 2,517 |
| Gross positive sales (GBP) | 10,666,684.544 |
| Negative adjustment value (GBP) | 896,812.490 |
| Net recorded sales (GBP) | 9,769,872.054 |
| Distinct positive sale invoices | 19,960 |
| Identified purchasing customers | 4,338 |
| Customers with at least two qualifying sale invoices | 2,845 |
| Repeat-purchasing share among identified purchasing customers | 65.58% |
| Eligible lines without a customer ID | 132,603 (24.58%) |

Decimal values retain source precision. Two-decimal chart labels are display rounding, not a change to stored totals. All 2,517 ineligible rows have the quality reason `nonpositive_price`. They remain in Silver and in the rejects table; they are excluded from monetary metrics rather than deleted.

## Findings and implications

**November 2011 is the peak observed month**, with GBP 1,461,756.25 in net sales and 2,769 sale orders. Net sales rise from September through November. December 2011 includes only December 1–9 and must not be presented as a comparable full-month decline. This single historical period does not establish recurring seasonality or predict future demand.

**Postage must be distinguished from merchandise.** DOTCOM POSTAGE (`DOT`) has GBP 206,245.48 net sales; POSTAGE (`POST`) has GBP 66,230.64. They are included in the overall monetary totals but excluded from the merchandise ranking. The remaining top ten codes were checked against source descriptions. This is a reviewed top-ten selection, not a validated classification of every code in the dataset.

**REGENCY CAKESTAND 3 TIER (`22423`) leads the reviewed merchandise ranking**, with GBP 164,762.19 net sales. PARTY BUNTING (`47566`) follows with GBP 98,302.98, and code `85123A` has GBP 97,894.50. Product codes, rather than descriptions, define the grouping because some codes have multiple descriptions. Description variants do not prove distinct products or reliable size-level identity.

**Repeat purchasing is common among identified purchasers**, with 2,845 of 4,338 making at least two qualifying sale purchases (65.58%). This measures purchasing within the observation window, not long-term retention. Missing IDs on 24.58% of eligible lines limit customer-level coverage; the customer percentage cannot be generalized to unidentified purchasers.

## Validation and limitations

The full notebook was run twice with unchanged reported input/eligible/reject counts and net totals. Row accounting and daily/product reconciliation passed in both reported outputs. Independent SQL from Silver reproduced gross sales, negative adjustments, net sales, and sale-order counts. Direct monthly distinct-invoice counts matched the daily-table rollup for this dataset; distinct counts are not generally additive.

Duplicate-looking source lines were preserved because a reliable unique line key was not established. Positive prices and nonzero quantities determine current eligibility; negative quantities are source-recorded adjustments, not verified refunded cash. Profit, margin, causal improvements, production scalability, and forecasts are not measured.

The workspace setup was edited during troubleshooting to use fixed catalog/schema/path variables after widget issues. The exact executed notebook export, environment version, and run revision remain to be captured before claiming that the current repository notebook was reproduced unchanged. Charts were reviewed in conversation but image exports have not yet been committed.

## Source and attribution

Chen, D. (2015). [Online Retail](https://doi.org/10.24432/C5BW33). UCI Machine Learning Repository. [Dataset](https://archive.ics.uci.edu/dataset/352/online+retail), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). This project converts the source workbook to CSV, applies documented eligibility rules, and aggregates the results. No raw customer-level data is published here.
