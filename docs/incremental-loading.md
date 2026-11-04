# Incremental batch loading

Validated in Databricks Free Edition with two 5,000-row batches in `workspace.retail_incremental_demo`.

## What changes

`01_pipeline.py` now supports `LOAD_MODE = "incremental"` as well as `"full_refresh"`. Incremental mode inserts unseen source rows into Bronze using Delta MERGE. Replaying the same source rows inserts zero rows. Silver, rejects, and Gold are then rebuilt from all accumulated Bronze rows, including after a replay, so a retry can repair a failed downstream refresh.

This is incremental Bronze ingestion, not incremental aggregation or change-data capture. Updates and deletions are not implemented. Different snapshot IDs cannot share a test schema, and a changed payload for an existing source-row identity is rejected.

## Source-row identity

The source CSV has no reliable business line key. The batch-preparation script identifies each line by the SHA-256 of the complete immutable CSV plus its one-based row number. Repeated transaction values retain different row numbers and are not silently deduplicated. This identity is valid for this fixed-snapshot exercise only; reordering or replacing the snapshot creates a different dataset.

Each batch also has its own SHA-256, checked before ingestion. The manifest records total source rows, selected rows, each batch's rows and checksum. Copy these values into the notebook; do not relabel rows manually. Trust is placed in the prepared files and manifest. Keep inputs unchanged throughout a run and permit only one writer to the test schema at a time.

## Prepare batches locally

From the repository root, with Python 3.10+:

```bash
python scripts/prepare_incremental_batches.py /path/to/online_retail.csv /path/outside/repo/batches
```

Defaults select the first 10,000 rows and create two 5,000-row batches. The output directory must not exist. `--all` selects the entire file; `--batch-size` changes batch size. Source records are preserved, with two identity columns appended. These first rows are for pipeline checks, not representative business analysis. Keep the CSVs and manifest outside Git.

## Isolated Databricks test

Do not replace the workspace notebook used by the daily job while testing. Create a separate test folder, import the updated `01_pipeline.py` there, and place copies of `00_transformations` and `02_smoke_checks` beside it. This is still one pipeline source file in the repository.

Upload the two batch CSVs to the existing `retail_input` volume. Use a fresh schema named `retail_incremental_demo`; the notebook creates it if permitted. Full-refresh mode is blocked from targeting a `retail_incremental` schema, and incremental mode is blocked from targeting `retail_learning`.

In the configuration cell set:

```python
CATALOG = "workspace"
SCHEMA = "retail_incremental_demo"
LOAD_MODE = "incremental"
ALLOW_FULL_REFRESH = False
ALLOW_INCREMENTAL_APPEND = True
SOURCE_DATASET_ID = "<source_dataset_id from manifest>"
SOURCE_TOTAL_ROWS = 541909  # Use the actual manifest value
BATCH_EXPECTED_ROWS = 5000  # Use this batch's rows value
INPUT_PATH = "/Volumes/workspace/retail_learning/retail_input/retail_batch_0001.csv"
BATCH_SHA256 = "<first batch SHA-256 from manifest>"
```

Run the smoke checks first, then the pipeline from the beginning. In a fresh schema:

| Run | Batch | Expected inserted rows | Expected accumulated Bronze rows |
| --- | --- | ---: | ---: |
| 1 | First batch | 5,000 | 5,000 |
| 2 | Same first batch, unchanged | 0 | 5,000 |
| 3 | Second batch, its own path/checksum | 5,000 | 10,000 |
| 4 | Same second batch, unchanged | 0 | 10,000 |

All four runs matched the table above. On each replay, all 5,000 incoming rows were already present. The accumulated result matched the earlier 10,000-row sample with 9,954 accepted rows, 46 rejected rows, and £180,667.75 in eligible net sales. Row accounting and the daily and product reconciliations passed.

The initial Bronze creation hit an unsupported write mode in Spark Connect. Using `mode("ignore")` allowed the notebook to create the empty table and proceed with the insert-only merge.

A mismatched batch checksum stopped the run before table writes. For a completed full-input backfill, compare accumulated counts and totals to the full-refresh baseline; that is beyond the initial two-batch test.

## Limits

Only Bronze grows incrementally. Silver/Gold full rebuilds still consume compute. Table writes are separate transactions, and concurrent writers are unsupported. A failed run should be retried with the identical input. This does not make the existing daily full-refresh job incremental; that workspace job must remain unchanged until the new mode is tested and intentionally deployed.

The 20 local tests cover conversion, preflight settings, and deterministic batch preparation. See the official [Delta MERGE reference](https://docs.databricks.com/aws/en/delta/merge) for insert-only merge behavior.
