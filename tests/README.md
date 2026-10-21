# Tests

Local converter checks:

```bash
python -m pip install -r requirements-preparation.txt
python -m unittest discover -s tests -v
```

Four tests passed during preparation on October 21, 2026. PySpark edge-case checks live in `../notebooks/02_smoke_checks.py` and must run in Databricks before real input. Delta persistence and same-input reruns require the workspace acceptance checks in `../docs/validation.md`.
