# Dataset

This project uses [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail), by Daqing Chen (2015), under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Download the workbook from UCI and convert it with [prepare_data.py](../scripts/prepare_data.py). Keep both the workbook and CSV outside Git, then upload the CSV to the Databricks volume. The [setup guide](../docs/setup.md) has the commands and path format.

The converter preserves rows and formats timestamps as ISO text. Its 10,000-row sample contains the first source rows, not a representative sample of the full period.
