# Tests

From the repository root:

```bash
python -m pip install -r requirements-preparation.txt
python -m unittest discover -s tests -v
```

There are eleven local tests: four for workbook conversion and seven for notebook preflight checks. The latter use mocked Spark access to check failure handling before writes.

Run [02_smoke_checks](../notebooks/02_smoke_checks.py) in Databricks for the PySpark edge cases. Delta writes, reconciliation, and repeat-run behavior are covered by the [workspace validation steps](../docs/validation.md).
