# Retail sales findings

This analysis covers 541,909 transaction lines from UCI Online Retail, dated December 1, 2010–December 9, 2011. The aim was to understand sales trends, identify leading merchandise codes, and measure repeat purchasing while accounting for cancellations and missing customer IDs.

## Overall sales

| Measure | Full dataset |
| --- | ---: |
| Input lines | 541,909 |
| Eligible lines | 539,392 |
| Lines excluded for nonpositive prices | 2,517 |
| Gross positive sales (GBP) | 10,666,684.544 |
| Negative adjustments (GBP) | 896,812.490 |
| Net recorded sales (GBP) | 9,769,872.054 |
| Distinct sale orders | 19,960 |

The 2,517 excluded lines remain in Silver and the rejects table. They have zero or negative unit prices, so the current analysis does not include them in monetary measures. Negative quantities on otherwise eligible lines reduce net sales; they are recorded adjustments rather than verified cash refunds.

Values retain the source's decimal precision. Rounded labels in the charts are for display only. Without cost data, these figures cannot be used to calculate profit.

## Sales peaked in November

November 2011 recorded £1,461,756.25 in net sales and 2,769 sale orders, the highest monthly totals in the period. Net sales increased from September through November.

December 2011 covers only the first nine days. Its lower total should not be described as a full-month sales decline. One historical period also provides too little evidence to establish recurring seasonality.

## Postage changes the product ranking

`DOT` (DOTCOM POSTAGE) recorded £206,245.48 in net sales, and `POST` (POSTAGE) recorded £66,230.64. Both contribute to overall sales but are shown separately from merchandise.

After excluding those codes, REGENCY CAKESTAND 3 TIER (`22423`) led the merchandise ranking at £164,762.19. PARTY BUNTING (`47566`) followed at £98,302.98, then code `85123A` at £97,894.50.

I checked the source descriptions for all ten codes in the chart. Some had more than one description: `85123A` included cream and white hanging heart T-light holders, while `22502` had differing wicker picnic-basket descriptions. The analysis therefore groups by product code rather than treating each description as a separate item. This check covers the displayed top ten, not every code in the dataset.

## Repeat purchasing and missing IDs

| Measure | Result |
| --- | ---: |
| Identified purchasing customers | 4,338 |
| Customers with at least two sale orders | 2,845 |
| Repeat-purchasing share | 65.58% |
| Eligible lines without customer IDs | 132,603 |
| Share of eligible lines without customer IDs | 24.58% |

The repeat-purchasing percentage applies to identified customers within the observation window. It is not a long-term retention rate. Missing IDs limit how much customer behavior can be measured, even though those lines still contribute to sales totals.

## Charts

### Monthly net sales (GBP)

![Monthly net sales in GBP](figures/monthly_net_sales.png)

The exported axis says “Total Sales,” but the plotted values are net sales. December 2011 includes December 1–9 only.

### Top ten merchandise codes by net sales (GBP)

![Top ten merchandise codes by net sales in GBP](figures/top_merchandise_net_sales.png)

Excludes `DOT` and `POST`. Codes are sorted by net sales, with one color to keep attention on the ranking. Descriptions were checked before labeling these entries as merchandise.

## Checks and limits

The full-data notebook ran twice with unchanged row counts and net sales. Daily and product Gold totals reconciled to eligible Silver, and separate SQL queries reproduced the sales and order totals. Monthly distinct orders were checked directly from Silver rather than assuming daily distinct counts were additive.

Duplicate-looking source lines were retained because invoice and product codes do not establish a unique line key. The analysis describes recorded historical transactions; it does not demonstrate causal business improvements or predict future sales.

The exported notebook summary and checksum are in [the execution record](notebook-export-evidence.json). Its metadata records Databricks environment version 6, but the exact Python/Spark versions and Git revision of that run were not captured. The updated Python notebook has since passed full-data reconciliation on Python 3.12.3 and Spark 4.2.0 with unchanged counts and net sales. See [the latest run record](runtime-validation.md). See [validation](../docs/validation.md).

## Data source

Chen, D. (2015). [Online Retail](https://doi.org/10.24432/C5BW33). UCI Machine Learning Repository. [Source page](https://archive.ics.uci.edu/dataset/352/online+retail) · [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The source workbook was converted to CSV, processed using the documented eligibility rules, and aggregated for analysis. Raw data and customer-level results are not included in this repository.
