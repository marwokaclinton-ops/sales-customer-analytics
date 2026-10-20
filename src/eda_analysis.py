
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# 1. Locate and load the cleaned dataset
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "processed" / "online_retail_cleaned.csv"

df = pd.read_csv(file_path, parse_dates=["InvoiceDate"])

print("=" * 50)
print("SALES PERFORMANCE AND CUSTOMER ANALYTICS")
print("=" * 50)

# 2. Overall sales performance
print("\n1. OVERALL SALES PERFORMANCE")
print("Total revenue:", round(df["Sales"].sum(), 2))
print("Total transactions:", df["InvoiceNo"].nunique())
print("Unique products:", df["StockCode"].nunique())
print("Unique customers:", df["CustomerID"].nunique())

# 3. Top 10 products by revenue
print("\n2. TOP 10 PRODUCTS BY REVENUE")
top_products = (
    df.groupby("Description")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(top_products)

# 4. Sales by country
print("\n3. TOP 10 COUNTRIES BY REVENUE")
top_countries = (
    df.groupby("Country")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(top_countries)

# 5. Monthly sales trend
print("\n4. MONTHLY SALES TREND")
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("Month")["Sales"].sum()
print(monthly_sales)

# 6. Save monthly sales chart
visuals_dir = project_dir / "visuals"
visuals_dir.mkdir(parents=True, exist_ok=True)

monthly_sales.plot(kind="line", marker="o", figsize=(10, 5))
plt.title("Monthly Sales Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(visuals_dir / "monthly_sales.png", dpi=300)
plt.show()

# 7. Save top products chart
top_products.sort_values().plot(kind="barh", figsize=(10, 6))
plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig(visuals_dir / "top_products.png", dpi=300)
plt.show()

print("\nEDA COMPLETED SUCCESSFULLY")
print("Charts saved in:", visuals_dir)
