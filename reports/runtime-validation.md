# Updated pipeline run

The following outputs were reported from the updated `01_pipeline.py` in Databricks. This record captures the reconciliation summary and runtime values; it is not an automated workspace audit.

| Field | Reported value |
| --- | --- |
| Python | 3.12.3 |
| Spark | 4.2.0 |
| Input file | `/Volumes/workspace/retail_learning/retail_input/online_retail.csv` |
| Input rows | 541,909 |
| Accepted rows | 539,392 |
| Rejected rows | 2,517 |
| Eligible net sales (GBP) | 9,769,872.054000 |
| Checks | Row accounting and daily/product totals passed |

The counts and net sales match the earlier full-data run. The latest run's exact timestamp, executed Git revision, and uploaded-file checksum were not independently captured. Runtime versions come from the notebook's printed output.

A second execution and independent SQL outputs for this updated revision have not yet been recorded. The earlier repeated full-data run and SQL checks are described in [validation](../docs/validation.md).
