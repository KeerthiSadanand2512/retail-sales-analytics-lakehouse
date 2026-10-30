# Data preparation — October 21, 2026

The original UCI Online Retail workbook was downloaded from the publisher's dataset-352 ZIP. It was converted locally with Python 3.12.14 and openpyxl 3.1.5 using `scripts/prepare_data.py`.

| Artifact | Rows | SHA-256 |
| --- | --- | --- |
| Original workbook | 541,909 data rows read during full conversion | `43465a06f2ccf7c8b5bd2892bc7defb52f97487934fe93b16ae4c3936424676d` |
| Full UTF-8 CSV | 541,909 | `7615e19743f2c3e8e641375743c276dbb0ed64a70cf210464ce72c335db3d221` |
| First-row learning sample | 10,000 | `2910edf122a2202d02ba7433fc6c30cf6cc687253b7ff3ea82abd4a460ee484d` |

Conversion formats datetimes as ISO text, retains blanks, preserves line order and duplicate rows, and does not apply analytics eligibility rules. The sample is the first 10,000 source rows and is not representative of the full dataset.

Four local conversion tests passed. This record covers workbook conversion only; subsequent Databricks runs are documented in [validation](../docs/validation.md).

No data files, customer-level results, or Databricks credentials are included in this repository. These row counts describe data preparation, not business findings.

Attribution: Chen, D. (2015). [Online Retail](https://doi.org/10.24432/C5BW33). UCI Machine Learning Repository. [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

