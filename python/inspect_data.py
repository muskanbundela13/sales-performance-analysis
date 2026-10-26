
from pathlib import Path
import pandas as pd

data_dir = Path("data/raw")

files = [
    *data_dir.glob("*.csv"),
    *data_dir.glob("*.xlsx"),
    *data_dir.glob("*.xls"),
]

if not files:
    raise FileNotFoundError(
        f"No CSV or Excel files found in {data_dir.resolve()}"
    )

file_path = files[0]

if file_path.suffix.lower() == ".csv":
    df = pd.read_csv(file_path)
else:
    df = pd.read_excel(file_path)

print(f"\nFile: {file_path.name}")
print(f"Rows: {len(df):,}")
print(f"Columns: {len(df.columns)}")

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types and non-null counts:")
df.info()

print("\nFirst five rows:")
print(df.head().to_string())

print("\nMissing values:")
print(df.isna().sum().sort_values(ascending=False))

print("\nExact duplicate rows:", df.duplicated().sum())
