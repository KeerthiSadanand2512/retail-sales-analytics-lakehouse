import csv
from datetime import datetime
import importlib.util
from pathlib import Path
import tempfile
import unittest
from openpyxl import Workbook

spec = importlib.util.spec_from_file_location('prepare_data', Path(__file__).resolve().parents[1] / 'scripts/prepare_data.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ConversionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.source = Path(self.temp.name)/'source.xlsx'
        self.output = Path(self.temp.name)/'out.csv'
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = 'Online Retail'
        sheet.append(module.COLUMNS)
        row = ['100001', '001A', 'Comma, newline\nquoted "item"', -2, datetime(2011, 1, 2, 3, 4), 2.5, None, 'UK']
        sheet.append(row)
        sheet.append(row)
        workbook.save(self.source)
        workbook.close()

    def test_round_trip_preserves_duplicate_rows_and_csv_quoting(self):
        result = module.convert(self.source, self.output)
        with self.output.open(newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(result['rows'], 2)
        self.assertEqual(rows[0], rows[1])
        self.assertEqual(rows[0]['StockCode'], '001A')
        self.assertEqual(rows[0]['CustomerID'], '')
        self.assertEqual(rows[0]['InvoiceDate'], '2011-01-02 03:04:00')
        self.assertEqual(rows[0]['Description'], 'Comma, newline\nquoted "item"')
        self.assertEqual(rows[0]['Quantity'], '-2')

    def test_sample_is_limited_and_labeled(self):
        result = module.convert(self.source, self.output, 1)
        self.assertEqual(result['rows'], 1)
        self.assertTrue(result['sample'])

    def test_no_overwrite(self):
        self.output.write_text('keep me')
        with self.assertRaises(ValueError):
            module.convert(self.source, self.output)
        self.assertEqual(self.output.read_text(), 'keep me')

    def test_reject_nonpositive_limit(self):
        with self.assertRaises(ValueError):
            module.convert(self.source, self.output, 0)
        self.assertFalse(self.output.exists())

if __name__ == '__main__':
    unittest.main()
