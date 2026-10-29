# Databricks notebook source

# COMMAND ----------
# MAGIC %md
# MAGIC # Retail Sales Analytics Lakehouse
# MAGIC
# MAGIC Reviewed learning notebook for Databricks Free Edition. Run `02_smoke_checks` first and keep `00_transformations` in this notebook's folder. Import **either** the `.py` or `.ipynb` version, not both under the same name.
# MAGIC
# MAGIC The supplied export recorded 541,909 input rows, 539,392 eligible rows, 2,517 rejected rows and GBP 9,769,872.054 net sales. Those are historical run evidence, not outputs of this revised notebook. Revisions have been checked locally but require a fresh Databricks run.
# MAGIC
# MAGIC This notebook replaces six project tables when full refresh is enabled. Use a dedicated schema and run only one refresh at a time. Writes are separate transactions; rerun the full pipeline after an interruption.

# COMMAND ----------
# MAGIC %run ./00_transformations

# COMMAND ----------
# MAGIC %md
# MAGIC ## Configuration
# MAGIC
# MAGIC Set `INPUT_PATH` to the exact uploaded CSV. Start with the sample. Set `ALLOW_FULL_REFRESH = True` only after reviewing the six target names. No widgets are required. SQL analysis uses the catalog/schema selected by the ingestion cell.

# COMMAND ----------
import re
from decimal import Decimal

CATALOG = "workspace"
SCHEMA = "retail_learning"
INPUT_PATH = "/Volumes/workspace/retail_learning/retail_input/online_retail_sample.csv"
ALLOW_FULL_REFRESH = False

TARGET_TABLES = (
    "retail_bronze", "retail_silver", "retail_rejects",
    "retail_gold_daily", "retail_gold_product", "retail_gold_customer",
)

def validate_settings(catalog, schema, input_path):
    for label, value in [("catalog", catalog), ("schema", schema)]:
        if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value):
            raise ValueError(f"{label} must be a nonblank simple identifier without spaces")
    if not schema.startswith("retail_"):
        raise ValueError("Use a dedicated schema beginning with retail_")
    if not isinstance(input_path, str) or not re.fullmatch(r"/Volumes/[^/]+/[^/]+/[^/]+/.+\.csv", input_path):
        raise ValueError("Supply an exact CSV file path under a Unity Catalog volume")
    if any(part in (".", "..") for part in input_path.split("/")) or any(x in input_path for x in ("*", "?", "[", "]")):
        raise ValueError("Use a single explicit file path, without wildcards or traversal")

validate_settings(CATALOG, SCHEMA, INPUT_PATH)
namespace = f"`{CATALOG}`.`{SCHEMA}`"

def table(name):
    if name not in TARGET_TABLES:
        raise ValueError("Unexpected project table name")
    return f"{namespace}.`{name}`"

print("Target schema:", namespace)
print("Input file:", INPUT_PATH)
print("Tables to replace:", TARGET_TABLES)
print("Full refresh enabled:", ALLOW_FULL_REFRESH)

# COMMAND ----------
# MAGIC %md
# MAGIC ## Bronze ingestion
# MAGIC
# MAGIC Validate the input before replacing a table. The preflight count adds one CSV read. Keep the uploaded file unchanged during the run.

# COMMAND ----------
if ALLOW_FULL_REFRESH is not True:
    raise ValueError("Review the six target tables, then set ALLOW_FULL_REFRESH = True")
required = ["SOURCE_COLUMNS", "F", "clean_retail", "gold_models"]
missing = [name for name in required if name not in globals()]
if missing:
    raise RuntimeError(f"Run %run ./00_transformations first; missing: {missing}")

raw = (spark.read.option("header", True).option("inferSchema", False)
       .option("multiLine", True).option("escape", '"')
       .option("mode", "FAILFAST").csv(INPUT_PATH))
if raw.columns != SOURCE_COLUMNS:
    raise ValueError("Expected the exact columns exported by scripts/prepare_data.py")
input_rows = raw.count()
if input_rows == 0:
    raise ValueError("Input is empty; no project tables have been overwritten")

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {namespace}")
spark.sql(f"USE CATALOG `{CATALOG}`")
spark.sql(f"USE SCHEMA `{SCHEMA}`")
bronze = (raw.select("*", F.col("_metadata.file_path").alias("source_file"))
    .withColumn("ingested_at", F.current_timestamp())
    .withColumn("source_batch", F.lit(INPUT_PATH)))
bronze.write.format("delta").mode("overwrite").option("overwriteSchema", True).saveAsTable(table("retail_bronze"))
bronze = spark.table(table("retail_bronze"))
if bronze.count() != input_rows:
    raise ValueError("Bronze row count differs from the input preflight; investigate before proceeding")

# COMMAND ----------
# MAGIC %md
# MAGIC ## Silver, rejected rows, and Gold tables
# MAGIC
# MAGIC Quality and metric rules are unchanged from the shared transformations. Duplicate-looking lines are preserved. Missing customer IDs do not exclude otherwise eligible sales.

# COMMAND ----------
silver = clean_retail(bronze)
silver.write.format('delta').mode('overwrite').option('overwriteSchema', True).saveAsTable(table('retail_silver'))
silver = spark.table(table('retail_silver'))
silver.filter('NOT eligible').write.format('delta').mode('overwrite').option('overwriteSchema', True).saveAsTable(table('retail_rejects'))
models = gold_models(silver)
for name, frame in models.items():
    frame.write.format('delta').mode('overwrite').option('overwriteSchema', True).saveAsTable(table(name))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Reconciliation
# MAGIC
# MAGIC Require source row accounting and eligible Silver totals to agree with the daily and product Gold totals.

# COMMAND ----------
# Reconciliation is required before interpreting the Gold results.
source_rows = bronze.count()
accepted = silver.filter('eligible').count()
rejected = spark.table(table('retail_rejects')).count()
assert source_rows == silver.count() == accepted + rejected
silver_total = silver.filter('eligible').agg(F.sum('line_value')).first()[0] or Decimal(0)
for name in ['retail_gold_daily', 'retail_gold_product']:
    total = spark.table(table(name)).agg(F.sum('net_sales')).first()[0] or Decimal(0)
    assert total == silver_total, f'{name} failed reconciliation'
print({'input_rows': source_rows, 'accepted_rows': accepted, 'rejected_rows': rejected,
       'eligible_net_sales_GBP': str(silver_total), 'checks': 'row accounting and daily/product totals passed'})
display(silver.groupBy('quality_reasons').count().orderBy(F.desc('count')))
display(spark.table(table('retail_gold_daily')).orderBy('transaction_date'))

# COMMAND ----------
# MAGIC %md
# MAGIC ## Runtime evidence
# MAGIC
# MAGIC Record these values with input checksums and the repository revision in your run log. Environment version 6 came from the original export metadata; it is not a Spark version.

# COMMAND ----------
import platform
print({"python_version": platform.python_version(), "spark_version": spark.version,
       "input_rows": input_rows, "source_path": INPUT_PATH})

# COMMAND ----------
# MAGIC %md
# MAGIC ## Independent sales and order cross-check (GBP)
# MAGIC
# MAGIC Negative adjustments are not proof of refunded cash; profit is not measured. Decimal source precision is retained.

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT
# MAGIC     currency,
# MAGIC     COUNT(*) AS accepted_rows,
# MAGIC     SUM(CASE WHEN quantity > 0 THEN line_value ELSE 0 END) AS gross_sales,
# MAGIC     SUM(CASE WHEN quantity < 0 THEN -line_value ELSE 0 END) AS return_value,
# MAGIC     SUM(line_value) AS net_sales,
# MAGIC     COUNT(DISTINCT CASE WHEN quantity > 0 THEN invoice_id END) AS sale_orders
# MAGIC FROM retail_silver
# MAGIC WHERE eligible
# MAGIC GROUP BY currency;

# COMMAND ----------
# MAGIC %md
# MAGIC ## Rejection reasons
# MAGIC
# MAGIC Rows remain in Silver and the rejects table; they are excluded from current monetary measures.

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT
# MAGIC     quality_reasons,
# MAGIC     COUNT(*) AS rejected_rows
# MAGIC FROM retail_rejects
# MAGIC GROUP BY quality_reasons
# MAGIC ORDER BY rejected_rows DESC;

# COMMAND ----------
# MAGIC %md
# MAGIC ## Repeat purchasing among identified customers
# MAGIC
# MAGIC This measures at least two sale invoices during the observed input period, not long-term retention.

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT
# MAGIC     currency,
# MAGIC     COUNT(*) AS identified_purchasing_customers,
# MAGIC     SUM(CASE WHEN sale_orders >= 2 THEN 1 ELSE 0 END)
# MAGIC         AS repeat_customers,
# MAGIC     ROUND(
# MAGIC         100.0 * SUM(CASE WHEN sale_orders >= 2 THEN 1 ELSE 0 END)
# MAGIC         / NULLIF(COUNT(*), 0),
# MAGIC         2
# MAGIC     ) AS repeat_customer_pct
# MAGIC FROM retail_gold_customer
# MAGIC GROUP BY currency;

# COMMAND ----------
# MAGIC %md
# MAGIC ## Customer-ID coverage
# MAGIC
# MAGIC The percentage is a share of eligible lines, not customers or sales value.

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS accepted_lines,
# MAGIC     COUNT_IF(customer_id IS NULL) AS lines_without_customer_id,
# MAGIC     ROUND(
# MAGIC         100.0 * COUNT_IF(customer_id IS NULL)
# MAGIC         / NULLIF(COUNT(*), 0), 2
# MAGIC     ) AS missing_customer_id_pct
# MAGIC FROM retail_silver
# MAGIC WHERE eligible;

# COMMAND ----------
# MAGIC %md
# MAGIC ## Monthly net recorded sales (GBP)
# MAGIC
# MAGIC December 2011 includes December 1–9 only. Sale orders are counted distinctly from Silver at the monthly grain, rather than summed across dates.

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT
# MAGIC     date_format(transaction_date, 'yyyy-MM') AS month,
# MAGIC     currency,
# MAGIC     SUM(CASE WHEN quantity > 0 THEN line_value ELSE 0 END) AS gross_sales,
# MAGIC     SUM(CASE WHEN quantity < 0 THEN -line_value ELSE 0 END) AS return_value,
# MAGIC     SUM(line_value) AS net_sales,
# MAGIC     COUNT(DISTINCT CASE WHEN quantity > 0 THEN invoice_id END) AS sale_orders
# MAGIC FROM retail_silver
# MAGIC WHERE eligible
# MAGIC GROUP BY 1, 2
# MAGIC ORDER BY 1;

# COMMAND ----------
# MAGIC %md
# MAGIC ## Top sales codes, including postage
# MAGIC
# MAGIC Check source descriptions before interpreting codes as merchandise. Some codes have several descriptions.

# COMMAND ----------
# MAGIC %sql
# MAGIC WITH top_codes AS (
# MAGIC     SELECT product_id, gross_sales, return_value, net_sales
# MAGIC     FROM retail_gold_product
# MAGIC     ORDER BY net_sales DESC
# MAGIC     LIMIT 10
# MAGIC ),
# MAGIC descriptions AS (
# MAGIC     SELECT
# MAGIC         product_id,
# MAGIC         sort_array(collect_set(trim(Description))) AS descriptions
# MAGIC     FROM retail_silver
# MAGIC     WHERE eligible
# MAGIC     GROUP BY product_id
# MAGIC )
# MAGIC SELECT t.*, d.descriptions
# MAGIC FROM top_codes t
# MAGIC LEFT JOIN descriptions d USING (product_id)
# MAGIC ORDER BY t.net_sales DESC;

# COMMAND ----------
# MAGIC %md
# MAGIC ## Top 10 reviewed merchandise codes by net sales (GBP)
# MAGIC
# MAGIC Excludes identified postage codes DOT and POST. All ten codes in the original full-data ranking were checked against their source descriptions; this is not a complete classification of every dataset code. Product descriptions may vary within a code.
# MAGIC
# MAGIC For the original full-data run, code 22423 (REGENCY CAKESTAND 3 TIER) led at GBP 164,762.19. Results may differ for the sample. Configure a horizontal bar chart with product_id as Y, net_sales as X, Group by empty, and category sorting disabled to retain descending SQL result order.

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT
# MAGIC     product_id,
# MAGIC     net_sales
# MAGIC FROM retail_gold_product
# MAGIC WHERE product_id NOT IN ('DOT', 'POST')
# MAGIC ORDER BY net_sales DESC
# MAGIC LIMIT 10;

# COMMAND ----------
# MAGIC %md
# MAGIC ## Supporting description checks

# COMMAND ----------
# MAGIC %sql
# MAGIC SELECT
# MAGIC     product_id,
# MAGIC     sort_array(collect_set(trim(Description))) AS descriptions
# MAGIC FROM retail_silver
# MAGIC WHERE eligible AND product_id IN ('22502', '22197')
# MAGIC GROUP BY product_id;

# COMMAND ----------
# MAGIC %md
# MAGIC ## Complete the run record
# MAGIC
# MAGIC Save the printed summary, input SHA-256, Git revision, actual Python/Spark versions, and any failures. Rerun with the identical immutable input and compare business row counts and totals. Save aggregate chart exports only; keep credentials and customer-level records out of public outputs.
# MAGIC
# MAGIC Charts from the earlier run are stored separately under `reports/figures/`. Recreate visualizations after importing this clean notebook; old Databricks chart metadata and outputs have been removed.
