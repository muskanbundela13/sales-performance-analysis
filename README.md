# Sales Performance Analysis

## Project Overview
An end-to-end data analytics project analyzing sales, profitability, product performance, and regional trends using PostgreSQL, Python, Jupyter Notebook, and Power BI.

The goal is to turn raw sales data into actionable business insights through data cleaning, SQL analysis, Python-based exploration, and interactive visualization.

## Tools & Technologies
- **PostgreSQL** — Data storage, cleaning, analytical views, and SQL queries
- **Python** — Data analysis and visualization
- **Pandas** — Data manipulation and aggregation
- **Matplotlib** — Chart generation
- **Jupyter Notebook** — Interactive analysis and documentation
- **Power BI** — Interactive business intelligence dashboard
- **Git & GitHub** — Version control and project sharing

## Project Structure

```text
sales-performance-analysis/
├── data/
│   ├── raw/
│   └── processed/
├── python/
│   ├── 01_sales_analysis.ipynb
│   ├── 02_business_insights.ipynb
│   ├── db_config.py
│   ├── import_data.py
│   ├── inspect_data.py
│   ├── sales_analysis.py
│   └── visualize_sales.py
├── sql/
│   ├── 01_executive_kpis.sql
│   ├── 02_monthly_performance.sql
│   ├── 03_product_profitability.sql
│   └── 04_regional_performance.sql
├── powerbi/
│   └── sales_performance_analysis.pbix
├── reports/
│   └── figures/
└── README.md
```

## Key Metrics

| Metric | Result |
|---|---:|
| Sales records | 10,194 |
| Unique orders | 5,111 |
| Unique customers | 804 |
| Units sold | 38,654 |
| Total revenue | 2,326,534.44 |
| Total profit | 292,295.93 |
| Overall profit margin | 12.56% |

*These figures reflect the current dataset and should be interpreted in light of the date-quality limitation described below.*

## Key Business Insights

### Category Performance
- **Technology** generated 839,893.35 in revenue and 146,543.85 in profit.
- **Office Supplies** generated 126,022.27 in profit.
- **Furniture** generated 754,747.86 in revenue but only 19,729.81 in profit, indicating a low profit margin.

### Regional Performance
- The West region generated the highest revenue and profit among the four regions.
- Central had the lowest regional profit margin at 7.92%.
- Regional comparisons can help identify areas for further profitability investigation.

### Product Profitability
- Tables recorded a total loss of 17,753.33.
- Bookcases and Supplies also recorded negative total profit.
- Copiers had a profit margin of 37.21%.

### Discount Analysis
- Lines with no discount had a profit margin of 29.56%.
- Lines discounted above 30% had a profit margin of -48.22%.
- This is an observed association in the dataset, not proof that discounts alone caused the losses.

## Data Quality Note
The dataset contains order dates later than October 26, 2026, the date of this analysis, including records extending into December 2026. Shipping dates extend into January 2027.

These records were present in the raw source data. They have not been silently removed or altered. Monthly and annual results should therefore be interpreted with this limitation in mind.

## How to Run

1. Install Python and PostgreSQL.
2. Create the `sales_performance_db` database.
3. Load the source dataset and prepare the `analytics.sales_clean` table.
4. Configure database connection environment variables, including `PGPASSWORD`.
5. Install the required Python dependencies.
6. Run the Python analysis scripts or open the Jupyter notebooks.
7. Open the Power BI file to explore the dashboard.

Database credentials should be supplied through environment variables and must never be committed to GitHub.

## Future Improvements
- Add automated data-quality checks.
- Improve date validation and document dataset provenance.
- Expand the dashboard with additional product and customer insights.
- Add reproducible setup instructions and dependency management.

## Author
**Muskan Bundela**

Data Analytics Portfolio Project