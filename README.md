# E-Commerce Sales & Analytics Dashboard

An end-to-end data analytics project built to analyze e-commerce transactional data using **Python/Pandas, MySQL, and Power BI**.

## Project Overview

The project converts raw e-commerce transaction data into cleaned, structured data, SQL-based business analysis, and an interactive Power BI dashboard.

### Pipeline

```text
Raw Excel Data
      ↓
Python + Pandas
      ↓
Data Exploration & Cleaning
      ↓
Clean CSV
      ↓
MySQL
      ↓
SQL Business Analysis
      ↓
Power BI + DAX
      ↓
Dashboard & Business Insights
```

## Objectives

- Clean and validate raw transactional data.
- Identify duplicates and missing values.
- Calculate revenue, profit, profit margin, and average order value.
- Analyze sales by month, category, region, customer segment, and product.
- Analyze the relationship between discount levels and profitability.
- Build an interactive Power BI dashboard for business reporting.
- Translate analytical results into business insights.

## Tech Stack

- **Python**
- **Pandas**
- **Excel / CSV**
- **MySQL**
- **SQL**
- **Power BI**
- **DAX**

## Dataset

The raw workbook contains:
- `orders_raw`
- `customers`
- `products`

The final analytical dataset contains **3,500 clean orders and 18 columns**.

Raw data initially contained **3,520 records**, including **20 exact duplicate rows**.

### Important columns

- `order_id`
- `customer_id`
- `product_id`
- `order_date`
- `quantity`
- `category`
- `selling_price`
- `cost_price`
- `discount_pct`
- `gross_sales`
- `discount_amount`
- `revenue`
- `cost`
- `profit`
- `payment_method`
- `region`
- `product_name`
- `segment`

## Data Cleaning

Using Python/Pandas:

1. Loaded the raw Excel workbook.
2. Inspected shape, columns, data types, and missing values.
3. Identified **20 exact duplicate rows**.
4. Removed duplicates, leaving **3,500 rows**.
5. Filled missing `discount_pct` values using the median.
6. Filled missing `payment_method` values with `Unknown`.
7. Filled missing `region` values with `Unknown`.
8. Converted `order_date` to a proper datetime type.
9. Performed a final data-quality audit.

### Why these choices?

- Exact duplicates were removed because they would artificially inflate business metrics.
- Median was used for missing discount percentages because it is less sensitive to extreme values than the mean.
- `Unknown` was used for missing categorical fields rather than guessing a category.

## Key Business KPIs

After cleaning:

| KPI | Value |
|---|---:|
| Valid orders | 3,500 |
| Total revenue | ₹15,223,645 |
| Total profit | ₹4,168,445 |
| Profit margin | 27.38% |
| Average order value | ~₹4,350 |
| Data period | 2025 |

## SQL Analysis

The cleaned data was imported into a MySQL table named `orders`.

The analysis included:

- Overall revenue/profit KPIs
- Category performance
- `HAVING` analysis
- Top customers
- Average order value
- AOV by customer segment
- Subqueries
- CTEs
- Product ranking using window functions
- Top-N product analysis

### Example: Overall KPIs

```sql
SELECT
    SUM(revenue) AS total_revenue,
    SUM(profit) AS total_profit,
    ROUND(SUM(profit) / SUM(revenue) * 100, 2) AS profit_margin
FROM orders;
```

### Example: Category Performance

```sql
SELECT
    category,
    SUM(revenue) AS total_revenue,
    SUM(profit) AS total_profit,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(profit) / SUM(revenue) * 100, 2) AS profit_margin
FROM orders
GROUP BY category
ORDER BY total_revenue DESC;
```

### Example: Customer Ranking

```sql
SELECT
    customer_id,
    SUM(revenue) AS total_revenue,
    SUM(profit) AS total_profit,
    COUNT(order_id) AS total_orders
FROM orders
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 10;
```

### Example: Product Ranking

```sql
SELECT
    product_id,
    product_name,
    SUM(revenue) AS total_revenue,
    RANK() OVER (
        ORDER BY SUM(revenue) DESC
    ) AS revenue_rank
FROM orders
GROUP BY product_id, product_name
ORDER BY revenue_rank;
```

### Example: CTE

```sql
WITH customer_sales AS (
    SELECT
        customer_id,
        SUM(revenue) AS total_revenue
    FROM orders
    GROUP BY customer_id
)
SELECT
    customer_id,
    total_revenue
FROM customer_sales
WHERE total_revenue > (
    SELECT AVG(total_revenue)
    FROM customer_sales
)
ORDER BY total_revenue DESC;
```

## Power BI Dashboard

The dashboard contains:

### KPI Cards
- Total Revenue
- Total Profit
- Total Orders
- Profit Margin
- Average Order Value

### Visual Analysis
- Monthly revenue and profit trend
- Revenue and profit by category
- Profit margin by category
- Revenue and profit by region

### DAX Measures

```DAX
Total Revenue = SUM(ecommerce_analytics_clean[revenue])
```

```DAX
Total Profit = SUM(ecommerce_analytics_clean[profit])
```

```DAX
Total Orders = DISTINCTCOUNT(ecommerce_analytics_clean[order_id])
```

```DAX
Profit Margin =
DIVIDE(
    [Total Profit],
    [Total Revenue],
    0
)
```

```DAX
Average Order Value =
DIVIDE(
    [Total Revenue],
    [Total Orders],
    0
)
```

## Key Findings

### 1. Revenue vs Profitability

Electronics generated the highest revenue at approximately **₹46.24 lakh**, but Fashion generated the highest total profit at approximately **₹12.82 lakh**.

### 2. Category Margin

Fashion had the highest profit margin at approximately **31.93%**, while Electronics had approximately **23.43%**.

### 3. Regional Performance

Pune generated the highest regional revenue at approximately **₹24.45 lakh** and the highest profit at approximately **₹6.65 lakh**.

Bengaluru had the highest regional profit margin at approximately **28.28%**.

### 4. Discount Analysis

In this dataset, higher discount levels were associated with lower profit per order.

Profit per order decreased from approximately **₹1,633 at 0% discount** to approximately **₹502 at 25% discount**.

This is an association, not proof of causality. Additional factors such as product mix, campaigns, customer type, and timing would need to be controlled to establish causation.

### 5. Product Performance

Smart Watch generated the highest revenue at approximately **₹21.95 lakh** and the highest total profit at approximately **₹4.62 lakh**.

Backpack had the highest profit margin at approximately **37.9%** and the highest order count with **268 orders**.

## Business Interpretation

The analysis shows why revenue alone is not sufficient for evaluating business performance.

For example:
- A category can have high revenue but lower margins.
- A region can generate high sales without having the highest margin.
- A product can generate high revenue without having the highest margin.
- Heavy discounts can be associated with lower profitability.

This makes it useful to evaluate **revenue, profit, margin, order volume, and customer/product characteristics together**.

## Project Structure

A suggested local project structure:

```text
Ecommerce Analytics project/
│
├── ecommerce_analytics_raw.xlsx
├── ecommerce_analytics_clean.csv
├── analysis.py
├── Ecommerce_Sales_Analytics_Dashboard.pbix
├── README.md
└── documentation/
    └── Project_Documentation.docx
```

## How to Reproduce

### 1. Install Python dependencies

```bash
py -m pip install pandas openpyxl
```

### 2. Place the raw workbook beside the Python script

The script should read:

```python
pd.read_excel(
    "ecommerce_analytics_raw.xlsx",
    sheet_name="orders_raw"
)
```

### 3. Run the cleaning/analysis script

```bash
py analysis.py
```

The cleaning stage should produce:

```text
ecommerce_analytics_clean.csv
```

### 4. Import into MySQL

Create/use a database such as:

```sql
CREATE DATABASE ecommerce_analytics;
USE ecommerce_analytics;
```

Import the cleaned CSV into an `orders` table.

### 5. Run SQL analysis

Run the business-analysis queries against `orders`.

### 6. Open Power BI

Load the cleaned dataset and use the DAX measures and visuals described above.

## Interview Explanation

> I built an end-to-end e-commerce analytics project using Python, SQL and Power BI. I started with 3,520 raw records and used Pandas to inspect and clean the data. I identified 20 duplicate records and handled missing values, resulting in 3,500 clean orders. I then loaded the data into MySQL and performed business analysis using aggregation, GROUP BY, HAVING, subqueries, CTEs and window functions. Finally, I created DAX measures and a Power BI dashboard to visualize KPIs, monthly trends, category performance and regional performance. One key finding was that Electronics generated the highest revenue, while Fashion generated the highest profit margin, showing why revenue alone is not enough to evaluate performance.

## Limitations

- The dataset is synthetic and should be presented as a project dataset rather than real company data.
- The discount analysis shows association, not causation.
- The dashboard is designed for portfolio/interview demonstration rather than production deployment.
- A production analytics system would normally include automated data ingestion, data validation, a proper dimensional model, scheduled refreshes, access controls, and monitoring.

## Future Improvements

- Build a proper star schema with fact and dimension tables.
- Add customer lifetime value and repeat-purchase analysis.
- Add cohort/retention analysis.
- Add automated data refresh.
- Add more detailed time-series analysis.
- Add campaign-level data to evaluate discount effectiveness.
- Publish the dashboard through Power BI Service with appropriate access control.

## Author

**Ayush Salve**  
B.Tech E&TC, IET DAVV Indore
