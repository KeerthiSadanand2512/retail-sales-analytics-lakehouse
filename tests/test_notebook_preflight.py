"""Test non-Spark configuration and pre-write failures without a Databricks session."""
import contextlib
import io
from pathlib import Path
import unittest
from unittest.mock import MagicMock

NOTEBOOK = Path(__file__).resolve().parents[1] / 'notebooks/01_pipeline.py'
CELLS = NOTEBOOK.read_text().split('# COMMAND ----------')
CODE = [cell for cell in CELLS if not cell.lstrip().startswith('# MAGIC')]
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

class IncrementalSettingsTests(unittest.TestCase):
    setUp = PreflightTests.setUp
    def test_incremental_cannot_target_dashboard_schema(self):
        with self.assertRaisesRegex(ValueError, 'separate retail_incremental'):
            self.env['validate_load_mode']('incremental', 'retail_learning', 'a'*64, 10, 'b'*64, 5)

    def test_full_refresh_cannot_erase_incremental_history(self):
        with self.assertRaisesRegex(ValueError, 'cannot target'):
            self.env['validate_load_mode']('full_refresh', 'retail_incremental_demo', '', 0, '', 0)

    def test_manifest_settings_are_required(self):
        for dataset, total, sha, rows in [('', 10, 'b'*64, 5), ('a'*64, 0, 'b'*64, 5), ('a'*64, 10, 'x', 5), ('a'*64, 10, 'b'*64, 11)]:
            with self.subTest(dataset=dataset, total=total, rows=rows), self.assertRaises(ValueError):
                self.env['validate_load_mode']('incremental', 'retail_incremental_demo', dataset, total, sha, rows)

    def test_valid_incremental_manifest(self):
        self.env['validate_load_mode']('incremental', 'retail_incremental_demo', 'a'*64, 10, 'b'*64, 5)

    def test_incremental_opt_in_precedes_spark_access(self):
        self.env.update(LOAD_MODE='incremental', ALLOW_INCREMENTAL_APPEND=False, spark=MagicMock())
        with self.assertRaisesRegex(ValueError, 'ALLOW_INCREMENTAL_APPEND'):
            exec(INGEST, self.env)
        self.assertEqual(self.env['spark'].mock_calls, [])

if __name__ == '__main__':
    unittest.main()


