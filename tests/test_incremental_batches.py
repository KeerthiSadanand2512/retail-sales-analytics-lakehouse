import csv
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('prepare_batches', Path(__file__).resolve().parents[1] / 'scripts/prepare_incremental_batches.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class BatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'source.csv'
        with self.source.open('w', newline='') as handle:
            writer = csv.writer(handle)
            writer.writerow(module.COLUMNS)
            row = ['001', '001A', 'Quoted, item\nnew line', '2', '2011-01-01 00:00:00', '3.50', '', 'UK']
            writer.writerow(row)
            writer.writerow(row)
            writer.writerow(['C002', 'B', 'Return', '-1', '2011-01-02 00:00:00', '3.50', '1', 'UK'])

    def test_duplicate_values_have_different_stable_row_ids(self):
        result = module.prepare_batches(self.source, self.root/'batches', batch_size=1, limit=None)
        self.assertEqual(result['source_total_rows'], 3)
        rows = []
        for batch in result['batches']:
            path = self.root/'batches'/batch['file']
            self.assertEqual(module.sha256_file(path), batch['sha256'])
            with path.open(newline='') as handle:
                rows.extend(csv.DictReader(handle))
        self.assertEqual([r['_source_row_number'] for r in rows], ['1', '2', '3'])
        self.assertEqual(rows[0]['Description'], 'Quoted, item\nnew line')
        self.assertEqual(rows[0]['StockCode'], '001A')
        self.assertEqual(rows[0]['CustomerID'], '')
        self.assertEqual(rows[2]['Quantity'], '-1')

    def test_repeat_preparation_produces_identical_batch_bytes(self):
        a = module.prepare_batches(self.source, self.root/'a', 2, None)
        b = module.prepare_batches(self.source, self.root/'b', 2, None)
        self.assertEqual(a, b)
        for batch in a['batches']:
            self.assertEqual((self.root/'a'/batch['file']).read_bytes(), (self.root/'b'/batch['file']).read_bytes())

    def test_limit_does_not_change_source_snapshot_identity(self):
        result = module.prepare_batches(self.source, self.root/'limited', 2, 2)
        self.assertEqual(result['selected_rows'], 2)
        self.assertEqual(result['source_total_rows'], 3)
        self.assertEqual(result['source_dataset_id'], module.sha256_file(self.source))

    def test_existing_output_and_invalid_limits_are_rejected(self):
        (self.root/'existing').mkdir()
        with self.assertRaises(FileExistsError):
            module.prepare_batches(self.source, self.root/'existing')
        with self.assertRaises(ValueError):
            module.prepare_batches(self.source, self.root/'bad', 0)

if __name__ == '__main__':
    unittest.main()
