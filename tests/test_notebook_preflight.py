"""Test non-Spark configuration and pre-write failures without a Databricks session."""
import contextlib
import io
import json
from pathlib import Path
import unittest
from unittest.mock import MagicMock

NOTEBOOK = Path(__file__).resolve().parents[1] / 'notebooks/01_pipeline.ipynb'
CELLS = json.loads(NOTEBOOK.read_text())['cells']
CODE = [''.join(c['source']) for c in CELLS if c['cell_type'] == 'code']
CONFIG = next(s for s in CODE if 'def validate_settings' in s)
INGEST = next(s for s in CODE if 'input_rows = raw.count()' in s)

class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.env = {}
        with contextlib.redirect_stdout(io.StringIO()):
            exec(CONFIG, self.env)

    def test_valid_dedicated_schema(self):
        self.env['validate_settings']('workspace', 'retail_learning', '/Volumes/workspace/retail_learning/retail_input/sample.csv')

    def test_bad_names_and_nonproject_schema(self):
        for catalog, schema in [('', 'retail_learning'), ('workspace;DROP', 'retail_learning'), ('workspace', 'default'), ('workspace', 'retail bad')]:
            with self.subTest(catalog=catalog, schema=schema), self.assertRaises(ValueError):
                self.env['validate_settings'](catalog, schema, self.env['INPUT_PATH'])

    def test_paths_cannot_be_globs_or_traversal(self):
        for path in ['sample.csv', '/Volumes/a/b/c/../sample.csv', '/Volumes/a/b/c/*.csv', '/Volumes/a/b/c/sample.xlsx']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.env['validate_settings']('workspace', 'retail_learning', path)

    def test_table_allowlist(self):
        with self.assertRaises(ValueError):
            self.env['table']('unrelated_customer_table')

    def test_refresh_opt_in_precedes_all_spark_access(self):
        self.env['spark'] = MagicMock()
        with self.assertRaisesRegex(ValueError, 'ALLOW_FULL_REFRESH'):
            exec(INGEST, self.env)
        self.assertEqual(self.env['spark'].mock_calls, [])

    def test_missing_shared_notebook_precedes_all_spark_access(self):
        self.env.update(ALLOW_FULL_REFRESH=True, spark=MagicMock())
        with self.assertRaisesRegex(RuntimeError, '00_transformations'):
            exec(INGEST, self.env)
        self.assertEqual(self.env['spark'].mock_calls, [])

    def test_empty_input_cannot_overwrite_tables(self):
        raw = MagicMock()
        raw.columns = ['InvoiceNo']
        raw.count.return_value = 0
        reader = MagicMock()
        reader.option.return_value = reader
        reader.csv.return_value = raw
        spark = MagicMock()
        spark.read = reader
        self.env.update(ALLOW_FULL_REFRESH=True, spark=spark, SOURCE_COLUMNS=raw.columns,
                        F=object(), clean_retail=object(), gold_models=object())
        with self.assertRaisesRegex(ValueError, 'Input is empty'):
            exec(INGEST, self.env)
        spark.sql.assert_not_called()
        self.assertEqual(raw.write.mock_calls, [])

if __name__ == '__main__':
    unittest.main()
