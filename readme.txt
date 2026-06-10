# Brazilian E-Commerce (Olist) – Data Analytics Project

## Project Overview

This project analyzes a large Brazilian e-commerce dataset provided by Olist.

The objective was to build a complete data analytics pipeline using Python and Pandas, including data cleaning, validation, issue detection, table integration and business KPI generation.

The final result is a unified analytical dataset ready for reporting and visualization.

---

## Dataset

The project uses multiple related tables:

- Customers
- Orders
- Order Items
- Payments
- Reviews
- Products
- Sellers
- Product Category Translation

The original data contains approximately 1 million records distributed across several CSV files.

---

## Data Cleaning

The following cleaning tasks were performed:

- Validation of IDs using regular expressions
- Data type conversion
- Date parsing and validation
- Missing value analysis
- Text normalization
- Duplicate detection
- Business rule validation
- Export of problematic records to separate issue files

Examples of detected issues:

- Invalid geolocation coordinates
- Missing product information
- Inconsistent review dates
- Payment anomalies

---

## Data Integration

Multiple datasets were merged into a single analytical table.

Main joins included:

- Orders + Customers
- Orders + Items
- Orders + Payments
- Orders + Reviews
- Items + Products
- Products + Categories
- Items + Sellers

Final dataset:

- Rows: ~112,650
- Columns: 40

---

## Key Performance Indicators (KPIs)

The project includes analysis such as:

### Sales Analysis

- Revenue by month
- Revenue by state
- Average ticket size

### Customer Analysis

- Top customers by revenue
- Customers with most cancellations
- Pareto 80/20 analysis

### Product Analysis

- Top products by revenue
- Product category performance
- Top 20 products contribution

### Operational Analysis

- Order status distribution
- Payment methods
- Customer review scores
- Cancellation rates

---

## Tools Used

- Python
- Pandas
- NumPy
- VS Code

---

## Project Structure

RAW/
CLEAN/
ISSUES/
OUTPUT/

helpers.py
cleaning.py
merge.py
kpis.py
run_pipeline.py

---

## What I Learned

This project was my first large-scale multi-table analytics project.

Main skills developed:

- Data cleaning
- Data validation
- Business KPI generation
- Multi-table joins
- Data quality analysis
- Analytical thinking using Pandas

The project helped me move from small exercises to real-world analytical workflows involving hundreds of thousands of records.