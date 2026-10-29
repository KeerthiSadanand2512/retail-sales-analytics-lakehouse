# Save the Databricks charts

Two charts have been configured during the guided workspace run. Actual PNG exports are pending; this file does not claim images already exist.

1. Monthly net sales: save as `monthly_net_sales.png`. Include the month axis, GBP measure, and note that December 2011 ends on December 9.
2. Top ten reviewed merchandise codes: save as `top_merchandise_net_sales.png`. Use descending net sales, one color, product codes as categories, and a note excluding DOT and POST.

Use a chart image-download option if provided. Otherwise take a screenshot containing the Markdown heading, entire chart, axes, and explanatory note. Include no email addresses, workspace account URLs, or customer-level rows. Send the images in the chat so they can be added under `reports/figures/` and linked from the findings.

Also export the executed notebooks through the notebook's export menu using a source format. Capture the actual modified setup cell and added SQL analysis. Review notebook outputs before sharing; keep raw customer IDs and credentials out of public artifacts. Runtime version and exact revision are still required for a complete reproducibility record.
