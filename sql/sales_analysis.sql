-- Run after 01_pipeline. Select the actual catalog and retail_learning schema in the SQL editor first.
-- Monthly orders are counted directly from Silver, not summed from product-level distinct counts.
SELECT date_trunc('MONTH', invoice_timestamp) AS month,
       currency,
       sum(CASE WHEN quantity > 0 THEN line_value ELSE 0 END) AS gross_sales,
       sum(CASE WHEN quantity < 0 THEN -line_value ELSE 0 END) AS return_value,
       sum(line_value) AS net_sales,
       count(DISTINCT CASE WHEN quantity > 0 THEN invoice_id END) AS sale_orders,
       try_divide(sum(CASE WHEN quantity > 0 THEN line_value ELSE 0 END),
                  count(DISTINCT CASE WHEN quantity > 0 THEN invoice_id END)) AS average_sale_order_value
FROM retail_silver WHERE eligible
GROUP BY 1, 2 ORDER BY 1;

SELECT product_id, currency, gross_sales, return_value, net_sales
FROM retail_gold_product ORDER BY net_sales DESC LIMIT 20;

SELECT currency, count(*) AS identified_purchasing_customers,
       sum(CASE WHEN sale_orders >= 2 THEN 1 ELSE 0 END) AS repeat_customers,
       try_divide(sum(CASE WHEN sale_orders >= 2 THEN 1 ELSE 0 END), count(*)) AS repeat_customer_share
FROM retail_gold_customer GROUP BY currency;

SELECT count(*) AS eligible_lines,
       count_if(customer_id IS NULL) AS missing_customer_lines
FROM retail_silver WHERE eligible;
