
from pathlib import Path
import pandas as pd

# Locate the project folder and raw dataset
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "raw" / "Online Retail.xlsx"

# Check whether the file exists
if not file_path.exists():
    raise FileNotFoundError(f"Dataset not found: {file_path}")

# Load the Excel dataset
df = pd.read_excel(file_path)

# Display basic information
print("DATASET LOADED SUCCESSFULLY")
print("-" * 40)

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset dimensions:")
print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types and missing values:")
df.info()

print("\nMissing values per column:")
print(df.isna().sum())