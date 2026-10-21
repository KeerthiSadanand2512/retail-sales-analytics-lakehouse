# Databricks notebook source
# MAGIC %md
# MAGIC # Synthetic checks — run before the real data pipeline
# MAGIC These invented rows are test cases, not UCI findings. No persistent tables are written.

# COMMAND ----------
# MAGIC %run ./00_transformations

# COMMAND ----------
from decimal import Decimal
rows = [
    ('100001', 'A', 'Item A', '2', '2011-01-01 10:00:00', '10.00', '1', 'UK'),
    ('100001', 'A', 'Item A', '2', '2011-01-01 10:00:00', '10.00', '1', 'UK'),
    ('100002', 'B', 'Item B', '1', '2011-01-02 10:00:00', '5.00', '1', 'UK'),
    ('C100003', 'A', 'Return', '-1', '2011-01-02 11:00:00', '10.00', '1', 'UK'),
    ('100004', 'B', 'Anonymous', '1', '2011-01-02 12:00:00', '5.00', None, 'UK'),
    ('100005', 'B', 'Bad date', '1', 'invalid', '5.00', '2', 'UK'),
    ('100006', 'B', 'Bad quantity', '1.5', '2011-01-02 12:00:00', '5.00', '2', 'UK'),
    ('C100007', 'B', 'Conflicting cancellation', '1', '2011-01-02 12:00:00', '5.00', '2', 'UK'),
    ('100008', 'B', 'Zero price', '1', '2011-01-02 12:00:00', '0', '2', 'UK'),
    ('100009', 'B', 'Negative price', '1', '2011-01-02 12:00:00', '-5', '2', 'UK'),
    ('100010', 'B', 'Zero quantity', '0', '2011-01-02 12:00:00', '5', '2', 'UK'),
    (None, 'B', 'Missing invoice', '1', '2011-01-02 12:00:00', '5', '2', 'UK'),
]
fixture = spark.createDataFrame(rows, ', '.join(f'{c} STRING' for c in SOURCE_COLUMNS))
cleaned = clean_retail(fixture)
assert cleaned.count() == 12
assert cleaned.filter('eligible').count() == 5
assert cleaned.filter('NOT eligible').count() == 7
models = gold_models(cleaned)
for name in ['retail_gold_daily', 'retail_gold_product']:
    result = models[name].agg(F.sum('gross_sales'), F.sum('return_value'), F.sum('net_sales')).first()
    assert tuple(result) == (Decimal('50'), Decimal('10'), Decimal('40')), (name, result)
customer = models['retail_gold_customer'].collect()
assert len(customer) == 1 and customer[0].sale_orders == 2 and customer[0].gross_sales == Decimal('45')
# Repeated source rows remain; no unsupported deduplication. Missing customer still contributes sales.
assert cleaned.filter("eligible AND invoice_id = '100001'").count() == 2
empty = clean_retail(fixture.limit(0))
assert empty.count() == 0
assert gold_models(empty)['retail_gold_daily'].count() == 0
print('Synthetic transformation and aggregation checks passed. Real-data and Delta runtime checks remain separate.')
