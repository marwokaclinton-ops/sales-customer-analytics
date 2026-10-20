
from pathlib import Path
import pandas as pd

# 1. Locate the cleaned dataset
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "processed" / "online_retail_cleaned.csv"

df = pd.read_csv(file_path, parse_dates=["InvoiceDate"])

# 2. Set the analysis date to one day after the last transaction
analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# 3. Calculate RFM metrics for each customer
rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda dates: (analysis_date - dates.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Sales", "sum")
).reset_index()

# 4. Remove customers without a valid ID
rfm = rfm.dropna(subset=["CustomerID"])

# 5. Assign scores from 1 to 5
# Lower recency is better; higher frequency and spending are better
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5, labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5, labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5, labels=[1, 2, 3, 4, 5]
).astype(int)

# 6. Create an overall RFM score
rfm["RFM_Score"] = (
    rfm["R_Score"].astype(str)
    + rfm["F_Score"].astype(str)
    + rfm["M_Score"].astype(str)
)

# 7. Assign simple customer segments
def segment_customer(row):
    if row["R_Score"] >= 4 and row["F_Score"] >= 4 and row["M_Score"] >= 4:
        return "Best Customers"
    elif row["R_Score"] >= 3 and row["F_Score"] >= 3:
        return "Loyal Customers"
    elif row["R_Score"] <= 2:
        return "At Risk"
    else:
        return "Regular Customers"

rfm["Segment"] = rfm.apply(segment_customer, axis=1)

# 8. Save the customer segmentation results
output_dir = project_dir / "data" / "processed"
output_file = output_dir / "customer_rfm_segments.csv"
rfm.to_csv(output_file, index=False)

# 9. Display summary results
print("=" * 45)
print("CUSTOMER RFM SEGMENTATION RESULTS")
print("=" * 45)

print("\nTotal customers analysed:", len(rfm))

print("\nCustomer segment counts:")
print(rfm["Segment"].value_counts())

print("\nAverage spending by segment:")
print(rfm.groupby("Segment")["Monetary"].mean().round(2))

print("\nTop 10 customers by spending:")
print(
    rfm.sort_values("Monetary", ascending=False)
       [["CustomerID", "Recency", "Frequency", "Monetary", "Segment"]]
       .head(10)
       .to_string(index=False)
)

print("\nResults saved to:", output_file)
