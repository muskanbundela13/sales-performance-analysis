
from pathlib import Path
import re

import pandas as pd
from sqlalchemy import text
from sqlalchemy.types import Text

from db_config import engine

data_dir = Path("data/raw")

files = [
    *data_dir.glob("*.csv"),
    *data_dir.glob("*.xlsx"),
    *data_dir.glob("*.xls"),
]

if len(files) != 1:
    raise ValueError(
        f"Expected exactly one dataset file, found {len(files)}."
    )

file_path = files[0]

if file_path.suffix.lower() == ".csv":
    df = pd.read_csv(file_path, dtype=str, keep_default_na=False)
else:
    df = pd.read_excel(file_path, dtype=str).fillna("")

original_columns = df.columns.tolist()

def normalize_column(name):
    name = re.sub(r"[^a-zA-Z0-9]+", "_", str(name).strip())
    return name.strip("_").lower()

df.columns = [normalize_column(c) for c in original_columns]

if len(set(df.columns)) != len(df.columns):
    raise ValueError("Duplicate column names after normalization.")

if df.empty:
    raise ValueError("The dataset has no rows.")

with engine.begin() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging"))

# Fail rather than overwrite an existing table.
df.to_sql(
    name="sales_raw",
    con=engine,
    schema="staging",
    if_exists="fail",
    index=False,
    dtype={col: Text() for col in df.columns},
    chunksize=1000,
    method="multi",
)

with engine.connect() as conn:
    count = conn.execute(
        text("SELECT COUNT(*) FROM staging.sales_raw")
    ).scalar_one()

print(f"Source file: {file_path.name}")
print(f"Rows imported: {len(df):,}")
print(f"Columns imported: {len(df.columns)}")
print(f"PostgreSQL row count: {count:,}")
print("\nImported columns:")
print(df.columns.tolist())
print("\nImport successful!")
