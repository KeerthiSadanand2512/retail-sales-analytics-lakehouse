# Databricks notebook source
# MAGIC %md
# MAGIC # Retail lakehouse: first batch pipeline
# MAGIC Run `02_smoke_checks` first. This full refresh replaces only the six named project tables in a dedicated schema.
# MAGIC Use a small sample first. No Databricks execution is claimed by the repository.

# COMMAND ----------
# MAGIC %run ./00_transformations

# COMMAND ----------
import re
from decimal import Decimal

dbutils.widgets.text('catalog', '', 'Existing catalog name')
dbutils.widgets.text('schema', 'retail_learning', 'Dedicated project schema')
dbutils.widgets.text('input_path', '', 'CSV path in a Unity Catalog volume')
dbutils.widgets.dropdown('allow_full_refresh', 'no', ['no', 'yes'], 'Replace project tables')
catalog = dbutils.widgets.get('catalog')
schema = dbutils.widgets.get('schema')
input_path = dbutils.widgets.get('input_path')
assert all(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', x) for x in [catalog, schema]), 'Use simple catalog/schema names'
assert schema.startswith('retail_'), 'Use a dedicated retail_ project schema'
assert input_path.startswith('/Volumes/') and input_path.endswith('.csv'), 'Supply the exact uploaded CSV path'
assert dbutils.widgets.get('allow_full_refresh') == 'yes', 'Set yes only after reviewing the target schema and six table names'
namespace = f'`{catalog}`.`{schema}`'
spark.sql(f'CREATE SCHEMA IF NOT EXISTS {namespace}')

def table(name):
    return f'{namespace}.`{name}`'

# COMMAND ----------
raw = (spark.read.option('header', True).option('inferSchema', False)
       .option('multiLine', True).option('escape', '"').option('mode', 'FAILFAST').csv(input_path))
assert raw.columns == SOURCE_COLUMNS, 'Expected CSV exported by scripts/prepare_data.py'
bronze = (raw.select('*', F.col('_metadata.file_path').alias('source_file'))
    .withColumn('ingested_at', F.current_timestamp())
    .withColumn('source_batch', F.lit(input_path)))
bronze.write.format('delta').mode('overwrite').option('overwriteSchema', True).saveAsTable(table('retail_bronze'))
bronze = spark.table(table('retail_bronze'))
assert bronze.count() > 0, 'Input is empty; fix the input before proceeding'

# COMMAND ----------
silver = clean_retail(bronze)
silver.write.format('delta').mode('overwrite').option('overwriteSchema', True).saveAsTable(table('retail_silver'))
silver = spark.table(table('retail_silver'))
silver.filter('NOT eligible').write.format('delta').mode('overwrite').option('overwriteSchema', True).saveAsTable(table('retail_rejects'))
models = gold_models(silver)
for name, frame in models.items():
    frame.write.format('delta').mode('overwrite').option('overwriteSchema', True).saveAsTable(table(name))

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
# MAGIC Save sanitized counts, runtime version, input checksum, revision and run date in the run log.
# MAGIC Re-run against the identical input and compare business counts/totals. Do not run concurrent refreshes.
# MAGIC Writes are per table, not one transaction across all tables. If interrupted, rerun the entire notebook.
