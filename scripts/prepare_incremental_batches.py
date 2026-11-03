"""Split an immutable retail CSV into numbered batches with stable source-row IDs."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

COLUMNS = ['InvoiceNo', 'StockCode', 'Description', 'Quantity', 'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
EXTRA_COLUMNS = ['_source_dataset_id', '_source_row_number']

def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()

def prepare_batches(source, output_dir, batch_size=5000, limit=10000):
    source, output_dir = Path(source), Path(output_dir)
    if batch_size <= 0 or (limit is not None and limit <= 0):
        raise ValueError('batch_size and limit must be positive')
    dataset_id = sha256_file(source)
    # Exclusive creation prevents silently replacing a batch already used in a run.
    output_dir.mkdir(parents=True, exist_ok=False)
    manifest = {'source_dataset_id': dataset_id, 'source_total_rows': 0,
                'selected_rows': 0, 'selection': 'first rows; not a representative sample', 'batches': []}
    writer = None
    handle = None
    try:
        with source.open(encoding='utf-8', newline='') as incoming:
            reader = csv.DictReader(incoming)
            if reader.fieldnames != COLUMNS:
                raise ValueError('Expected the CSV from prepare_data.py')
            for ordinal, row in enumerate(reader, start=1):
                if None in row or any(value is None for value in row.values()):
                    raise ValueError(f'Malformed CSV record at source row {ordinal}')
                manifest['source_total_rows'] = ordinal
                if limit is not None and ordinal > limit:
                    continue
                if manifest['selected_rows'] % batch_size == 0:
                    if handle is not None:
                        handle.close()
                    batch_path = output_dir / f"retail_batch_{len(manifest['batches']) + 1:04d}.csv"
                    handle = batch_path.open('x', encoding='utf-8', newline='')
                    writer = csv.DictWriter(handle, fieldnames=COLUMNS + EXTRA_COLUMNS, lineterminator='\n')
                    writer.writeheader()
                    manifest['batches'].append({'file': batch_path.name, 'rows': 0, 'first_source_row': ordinal})
                writer.writerow({**row, '_source_dataset_id': dataset_id, '_source_row_number': ordinal})
                manifest['selected_rows'] += 1
                manifest['batches'][-1]['rows'] += 1
                manifest['batches'][-1]['last_source_row'] = ordinal
    finally:
        if handle is not None:
            handle.close()
    if manifest['source_total_rows'] == 0:
        raise ValueError('Input is empty')
    if sha256_file(source) != dataset_id:
        raise ValueError('Source changed while splitting; discard this output directory')
    for batch in manifest['batches']:
        batch['sha256'] = sha256_file(output_dir / batch['file'])
    (output_dir / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source')
    parser.add_argument('output_dir')
    parser.add_argument('--batch-size', type=int, default=5000)
    parser.add_argument('--limit', type=int, default=10000, help='First N rows; use --all for the complete input')
    parser.add_argument('--all', action='store_true')
    args = parser.parse_args()
    print(json.dumps(prepare_batches(args.source, args.output_dir, args.batch_size, None if args.all else args.limit), indent=2))
