import pandas as pd

df = pd.read_excel("ecommerce_analytics_raw.xlsx", sheet_name="orders_raw")

print(df.head())
print(df.shape)
print(df.columns.tolist())
df.info()

print(df.isnull().sum())


duplicates = df[df.duplicated()]
print(duplicates)
print("No. of duplicates", len(duplicates))

df = df.drop_duplicates()

print("Rows after removing duplicates:", len(df))

print(df["discount_pct"].describe())

df["discount_pct"] = df["discount_pct"].fillna(df["discount_pct"].median())

print("Missing discounts:", df["discount_pct"].isnull().sum())

print(df["payment_method"].value_counts(dropna=False))

df["payment_method"] = df["payment_method"].fillna("Unknown")

print("Missing payment methods:", df["payment_method"].isnull().sum())
print(df["payment_method"].value_counts())

print(df["region"].value_counts(dropna=False))

print("Missing regions:", df["region"].isnull().sum())
print(df["region"].value_counts(dropna=False))

print("\n--- NUMERIC SUMMARY ---")
print(df.describe())

print("\n--- KEY BUSINESS METRICS ---")

total_revenue = df["revenue"].sum()
total_profit = df["profit"].sum()

print("Total Revenue:", total_revenue)
print("Total Profit:", total_profit)

profit_margin = (total_profit / total_revenue) * 100
print("Profit Margin:", round(profit_margin, 2), "%")

df["order_date"] = pd.to_datetime(df["order_date"])

monthly_revenue = df.groupby(
    df["order_date"].dt.to_period("M")
)["revenue"].sum()

print("\n --- monthly revenue")
print(monthly_revenue)

average_monthly_revenue = monthly_revenue.mean()

highest_month = monthly_revenue.idxmax()
highest_revenue = monthly_revenue.max()

lowest_month = monthly_revenue.idxmin()
lowest_revenue = monthly_revenue.min()

print("Average monthly revenue:" ,round(average_monthly_revenue,2))
print("Highest Revenue Month:",highest_month , highest_revenue)
print("Lowest Revenue Month" , lowest_month , lowest_revenue) 

# category analysis

products = pd.read_excel(
    "ecommerce_analytics_raw.xlsx",
    sheet_name="products"
)

category_data = df.merge(
    products[["product_id", "category"]],
    on="product_id",
    how="left"
)

category_analysis = category_data.groupby("category_y").agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    orders=("order_id", "count")
).sort_values("revenue", ascending=False)

print("\n--- CATEGORY ANALYSIS ---")
print(category_analysis)

category_analysis["profit_per_order"] = (
    category_analysis["profit"] / category_analysis["orders"]
)

print("\n--- PROFIT PER ORDER ---")
print(category_analysis[["profit", "orders", "profit_per_order"]])

category_analysis["profit_margin"] = (
    category_analysis["profit"] / category_analysis["revenue"]
) * 100

print("\n--- CATEGORY PROFIT MARGIN ---")
print(
    category_analysis[
        ["revenue", "profit", "orders", "profit_per_order", "profit_margin"]
    ]
)

region_analysis = df.groupby("region").agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    orders=("order_id", "count")
).sort_values("revenue", ascending=False)

region_analysis["profit_margin"] = (
    region_analysis["profit"] / region_analysis["revenue"]
) * 100

print("\n--- REGIONAL ANALYSIS ---")
print(region_analysis)

# customer segment analysis

customer_data = df.merge(
    pd.read_excel(
        "ecommerce_analytics_raw.xlsx",
        sheet_name="customers"
    )[["customer_id", "segment"]],
    on="customer_id",
    how="left"
)

segment_analysis = customer_data.groupby("segment").agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    orders=("order_id", "count")
).sort_values("revenue", ascending=False)

segment_analysis["profit_margin"] = (
    segment_analysis["profit"] / segment_analysis["revenue"]
) * 100

print("\n--- CUSTOMER SEGMENT ANALYSIS ---")
print(segment_analysis)

print("\n --Discount Analysis--")

discount_analysis = df.groupby("discount_pct").agg(
    revenue = ("revenue","sum"),
    profit = ("profit" , 'sum'),
    orders = ("order_id","count")
)

discount_analysis["profit_margin"] = (
    discount_analysis["profit"] / discount_analysis["revenue"]
) * 100

print(discount_analysis)

discount_analysis["revenue_per_order"] = (
    discount_analysis["revenue"] / discount_analysis["orders"]
)

discount_analysis["profit_per_order"] = (
    discount_analysis["profit"] / discount_analysis["orders"]
)

print("\n--- DISCOUNT PER ORDER ANALYSIS ---")
print(
    discount_analysis[
        [
            "orders",
            "revenue_per_order",
            "profit_per_order",
            "profit_margin"
        ]
    ]
)

print("\n--- TOP PRODUCT ANALYSIS ---")

products = pd.read_excel(
    "ecommerce_analytics_raw.xlsx",
    sheet_name="products"
)

product_data = df.merge(
    products[["product_id", "product_name", "category"]],
    on="product_id",
    how="left"
)

product_analysis = product_data.groupby(
    ["product_id", "product_name"]
).agg(
    revenue=("revenue", "sum"),
    profit=("profit", "sum"),
    orders=("order_id", "count")
).sort_values("revenue", ascending=False)

product_analysis["profit_margin"] = (
    product_analysis["profit"] / product_analysis["revenue"]
) * 100

print(product_analysis)

print("\n -- Creating clean dataset--")

clean_df = df.copy()

products = pd.read_excel("ecommerce_analytics_raw.xlsx", sheet_name = "products")

customers = pd.read_excel(
    "ecommerce_analytics_raw.xlsx",
    sheet_name = "customers"
)
# Add product information
clean_df = clean_df.merge(
    products[["product_id" , "product_name"]],
    on="product_id",
    how = "left"
)
# Add customer information
clean_df = clean_df.merge(
    customers[["customer_id", "segment"]],
    on="customer_id",
    how="left"
)

print(clean_df.head())
print("\n Final columns:")
print(clean_df.columns.tolist())

print("\n Final shape:")
print(clean_df.shape)

clean_df.to_csv("ecommerce_analytics_clean.csv", index=False)

print("\nClean dataset saved successfully!")
