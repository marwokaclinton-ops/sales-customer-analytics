
from pathlib import Path
import pandas as pd

# 1. Locate the project folders
project_dir = Path(__file__).resolve().parent.parent
raw_file = project_dir / "data" / "raw" / "Online Retail.xlsx"
processed_dir = project_dir / "data" / "processed"
processed_file = processed_dir / "online_retail_cleaned.csv"

# 2. Create the processed folder if it does not exist
processed_dir.mkdir(parents=True, exist_ok=True)

# 3. Load the original dataset
df = pd.read_excel(raw_file)

print("ORIGINAL DATA")
print("Rows and columns:", df.shape)

# 4. Remove duplicate records
df = df.drop_duplicates()

# 5. Remove rows missing essential sales information
df = df.dropna(
    subset=["InvoiceNo", "StockCode", "Quantity", "InvoiceDate", "UnitPrice"]
)

# 6. Remove cancelled invoices
# In this dataset, invoice numbers beginning with C indicate cancellations
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# 7. Remove invalid quantities and prices
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# 8. Convert invoice dates to datetime format
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")
df = df.dropna(subset=["InvoiceDate"])

# 9. Calculate sales revenue
df["Sales"] = df["Quantity"] * df["UnitPrice"]

# 10. Save the cleaned dataset
df.to_csv(processed_file, index=False)

print("\nCLEANING COMPLETED SUCCESSFULLY")
print("Cleaned rows and columns:", df.shape)
print("Missing values:")
print(df.isna().sum())
print("\nTotal sales revenue:", round(df["Sales"].sum(), 2))
print("\nSaved cleaned data to:", processed_file)
