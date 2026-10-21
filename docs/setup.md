# First Databricks run

Status: local data preparation checked; workspace execution pending.

## 1. Create your free workspace

Open [Databricks Free Edition](https://www.databricks.com/learn/free-edition), follow signup, and select Free Edition rather than a paid trial. Complete sign-in yourself. No paid cloud account or classic cluster is needed. Free Edition is serverless-only and quota-limited; see [current limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations).

## 2. Prepare the CSV

Download the workbook from [UCI](https://archive.ics.uci.edu/dataset/352/online+retail) and unzip it outside your repository. The original workbook is named `Online Retail.xlsx`.

For a local setup with Python 3.10+:

```bash
python -m venv .venv
# Activate the environment for your operating system.
python -m pip install -r requirements-preparation.txt
python scripts/prepare_data.py "/path/to/Online Retail.xlsx" "/path/outside/repo/online_retail_sample.csv" --limit 10000
```

Omit `--limit 10000` and choose a new output filename to convert the full workbook. Existing output files are not overwritten. Conversion prints source/output checksums and row count. It preserves records, missing values, cancellations, and duplicate rows. Source datetimes become ISO strings; original timezone is unspecified. The sample is the first rows, not a random or representative sample.

## 3. Upload the CSV

In the workspace Catalog area, find an existing catalog you can use. Create a dedicated schema named `retail_learning` and a managed volume such as `retail_input` inside it if permitted. Upload the CSV using the volume's upload control and copy its path, for example:

```text
/Volumes/<your_catalog>/retail_learning/retail_input/online_retail_sample.csv
```

Use the actual catalog name. Do not paste the example placeholders into the notebook. If volume creation is unavailable, stop and record the exact message rather than switching to paid infrastructure.

## 4. Import and test the notebooks

Download the three `.py` files from `notebooks/`. Import them as Python source notebooks into the same workspace folder so relative `%run` resolves. Attach available serverless notebook compute.

Run `02_smoke_checks` first. Its printed pass message is required before running real data. It does not create tables. Record failures before changing quality rules.

## 5. Run the batch

Open `01_pipeline`. Enter your existing catalog, schema `retail_learning`, and exact uploaded CSV path. The default `allow_full_refresh=no` prevents writes. Review the six table names in the README and use a schema reserved for this project; set the widget to `yes` when ready. Run all cells.

The notebook overwrites the project's six named tables, preserving source rows in Bronze and all typed rows in Silver, with rejected rows copied to `retail_rejects`. Do not run simultaneous refreshes. If interrupted, rerun the whole notebook; tables are not committed together.

Confirm the printed row counts and checks, then fill in `reports/databricks-run-template.md`. Run again with the same immutable input and compare counts and net totals to check rerun behavior. This remains an acceptance step, not a completed test in this repository.

## 6. Explore with SQL

Open `sql/sales_analysis.sql` in the SQL editor, select your catalog and `retail_learning` schema, and run each statement. If SQL compute is unavailable under current quotas, wait. Record observed results and limitations before writing business findings. Do not publish raw customer IDs or customer-level exports.
