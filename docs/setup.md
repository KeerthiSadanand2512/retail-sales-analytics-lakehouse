# Databricks Free Edition setup plan

Status: instructions for future implementation; not executed for this repository.

1. Use the official [Free Edition signup guide](https://docs.databricks.com/aws/en/getting-started/free-edition). Confirm the account is Free Edition, not a paid trial or pay-as-you-go workspace.
2. Review [current limitations](https://docs.databricks.com/aws/en/getting-started/free-edition-limitations). It is serverless-only and quota-limited. Quota exhaustion can pause compute. Do not provision a classic cluster or paid cloud resources.
3. In the workspace, identify an available catalog and create a dedicated project schema if permitted. Use a Unity Catalog volume for the approved small input file when available. Avoid legacy DBFS mount instructions.
4. Select and document the dataset using `data-contract.md`. Download it locally if outbound networking prevents direct access, then upload it through the workspace interface.
5. Create the numbered notebooks described in `../notebooks/README.md`. Set the source path, catalog, and schema as explicit parameters. Use the workspace Spark session and available serverless compute; do not install an unrelated local Spark runtime into it.
6. Implement and run one stage at a time. Use a small sample first. Confirm quality and metric reconciliation before building a dashboard.
7. Record the actual environment version, source checksum, notebook revision, row counts, and run result in `../reports/`.
8. Export source notebooks without sensitive outputs. Stop idle interactive sessions and avoid unnecessary reruns. If a quota is exhausted, wait for availability instead of enabling paid services.

There is no runnable pipeline or dependency file yet. Add dependencies only when implementation requires them and document their compatibility with the actual Databricks environment. If a planned feature is unavailable, record the limitation and retain manual execution as the baseline.
