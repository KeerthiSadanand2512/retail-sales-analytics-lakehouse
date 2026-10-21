# Databricks notebook source
# MAGIC %md
# MAGIC # Shared transformations
# MAGIC Source-specific UCI Online Retail rules. Called by the pipeline and smoke checks.

# COMMAND ----------
from pyspark.sql import functions as F

SOURCE_COLUMNS = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']

def clean_retail(bronze):
    typed = (bronze
        .withColumn('invoice_id', F.trim('InvoiceNo'))
        .withColumn('product_id', F.trim('StockCode'))
        .withColumn('customer_id', F.when(F.length(F.trim('CustomerID')) > 0, F.trim('CustomerID')))
        .withColumn('quantity', F.expr("CASE WHEN trim(Quantity) RLIKE '^[+-]?[0-9]+$' THEN try_cast(Quantity AS INT) END"))
        .withColumn('unit_price', F.expr('try_cast(UnitPrice AS DECIMAL(18,6))'))
        .withColumn('invoice_timestamp', F.expr('try_cast(InvoiceDate AS TIMESTAMP_NTZ)'))
        .withColumn('is_cancellation', F.upper(F.col('invoice_id')).startswith('C'))
        .withColumn('currency', F.lit('GBP')))
    issues = [
        (F.col('invoice_id').isNull() | (F.col('invoice_id') == ''), 'missing_invoice'),
        (F.col('product_id').isNull() | (F.col('product_id') == ''), 'missing_product'),
        (F.col('invoice_timestamp').isNull(), 'invalid_timestamp'),
        (F.col('quantity').isNull(), 'invalid_quantity'),
        (F.col('quantity') == 0, 'zero_quantity'),
        (F.col('unit_price').isNull(), 'invalid_price'),
        (F.col('unit_price') <= 0, 'nonpositive_price'),
        (F.col('is_cancellation') & (F.col('quantity') > 0), 'positive_cancellation_quantity'),
    ]
    typed = typed.withColumn('quality_reasons', F.concat_ws('|', *[F.when(condition, F.lit(reason)) for condition, reason in issues]))
    return (typed
        .withColumn('eligible', F.col('quality_reasons') == '')
        .withColumn('transaction_date', F.to_date('invoice_timestamp'))
        .withColumn('line_value', (F.col('quantity') * F.col('unit_price')).cast('decimal(30,6)'))
        .withColumn('is_return', F.col('quantity') < 0))

def gold_models(silver):
    eligible = silver.filter('eligible')
    def aggregate(keys):
        return eligible.groupBy(*keys).agg(
            F.sum(F.when(F.col('quantity') > 0, F.col('line_value')).otherwise(F.lit(0))).alias('gross_sales'),
            F.sum(F.when(F.col('quantity') < 0, -F.col('line_value')).otherwise(F.lit(0))).alias('return_value'),
            F.sum('line_value').alias('net_sales'),
            F.countDistinct(F.when(F.col('quantity') > 0, F.col('invoice_id'))).alias('sale_orders'),
            F.count('*').alias('eligible_lines'))
    return {
        'retail_gold_daily': aggregate(['transaction_date', 'currency']),
        'retail_gold_product': aggregate(['product_id', 'currency']),
        'retail_gold_customer': (eligible.filter('quantity > 0 AND customer_id IS NOT NULL')
            .groupBy('customer_id', 'currency').agg(
                F.countDistinct('invoice_id').alias('sale_orders'),
                F.sum('line_value').alias('gross_sales'))),
    }
