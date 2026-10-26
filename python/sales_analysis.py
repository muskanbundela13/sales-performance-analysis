
import pandas as pd
from sqlalchemy import text
from python.db_config import engine


def load_sales_data():
    """Load cleaned sales records from PostgreSQL."""
    query = text("""
        SELECT
            order_id,
            order_date,
            ship_date,
            region,
            state_province,
            category,
            sub_category,
            customer_id,
            sales,
            profit,
            quantity,
            discount
        FROM analytics.sales_clean
    """)

    with engine.connect() as connection:
        df = pd.read_sql(query, connection)

    return df


def main():
    df = load_sales_data()

    
    print("\n========== DATE QUALITY CHECK ==========")

    df["order_date"] = pd.to_datetime(df["order_date"])
    df["ship_date"] = pd.to_datetime(df["ship_date"])

    print(f"Earliest order date: {df['order_date'].min()}")
    print(f"Latest order date:   {df['order_date'].max()}")
    print(f"Earliest ship date:  {df['ship_date'].min()}")
    print(f"Latest ship date:    {df['ship_date'].max()}")

    today = pd.Timestamp.today().normalize()

    future_orders = df[df["order_date"] > today]

    print(f"Orders dated in the future: {len(future_orders):,}")

    print("\nRows with future order dates:")
    print(
        future_orders[
            ["order_id", "order_date", "ship_date", "sales", "profit"]
        ].head(10).to_string(index=False)
    )


    print("\n========== DATA OVERVIEW ==========")
    print(f"Total rows: {len(df):,}")
    print(f"Unique orders: {df['order_id'].nunique():,}")
    print(f"Unique customers: {df['customer_id'].nunique():,}")
    print(f"Total units sold: {df['quantity'].sum():,}")

    print("\n========== SALES KPIs ==========")
    print(f"Total revenue: {df['sales'].sum():,.2f}")
    print(f"Total profit: {df['profit'].sum():,.2f}")

    revenue = df["sales"].sum()
    profit = df["profit"].sum()

    margin = (profit / revenue * 100) if revenue else 0
    print(f"Overall profit margin: {margin:.2f}%")

    print("\n========== CATEGORY PERFORMANCE ==========")
    category_summary = (
        df.groupby("category")
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            units_sold=("quantity", "sum"),
        )
        .reset_index()
    )

    category_summary["profit_margin_pct"] = (
        category_summary["profit"]
        / category_summary["revenue"]
        * 100
    )

    print(
        category_summary.sort_values(
            "revenue", ascending=False
        ).round(2).to_string(index=False)
    )


    
    print("\n========== MONTHLY PERFORMANCE ==========")

    df["order_date"] = pd.to_datetime(df["order_date"])

    monthly_summary = (
        df.groupby(df["order_date"].dt.to_period("M"))
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
        )
        .reset_index()
    )

    monthly_summary["order_date"] = (
        monthly_summary["order_date"].astype(str)
    )

    print(monthly_summary.round(2).to_string(index=False))

    
    print("\n========== YEAR DISTRIBUTION ==========")

    print(
        df["order_date"]
        .dt.year
        .value_counts()
        .sort_index()
        .to_string()
    )

    
    print("\n========== ORDER ID YEAR VS DATE YEAR ==========")

    df["order_id_year"] = (
        df["order_id"]
        .astype(str)
        .str.extract(r"^[A-Z]{2}-(\d{4})-")[0]
    )

    df["date_year"] = df["order_date"].dt.year.astype(str)

    mismatches = df[
        df["order_id_year"].notna()
        & (df["order_id_year"] != df["date_year"])
    ]

    unmatched_ids = df[df["order_id_year"].isna()]

    print(f"Actual year mismatches: {len(mismatches):,}")
    print(f"IDs not matching the expected format: {len(unmatched_ids):,}")

    print("\nActual mismatch examples:")
    print(
        mismatches[
            ["order_id", "order_date", "ship_date"]
        ].head(10).to_string(index=False)
    )

    
    print("\n========== REGIONAL PERFORMANCE ==========")

    regional_summary = (
        df.groupby("region")
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            orders=("order_id", "nunique"),
            customers=("customer_id", "nunique"),
        )
        .reset_index()
    )

    regional_summary["profit_margin_pct"] = (
        regional_summary["profit"]
        / regional_summary["revenue"]
        * 100
    )

    regional_summary = regional_summary.sort_values(
        "revenue", ascending=False
    )

    print(regional_summary.round(2).to_string(index=False))


    
    print("\n========== SUBCATEGORY PROFITABILITY ==========")

    subcategory_summary = (
        df.groupby(["category", "sub_category"])
        .agg(
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            units_sold=("quantity", "sum"),
            loss_making_lines=("profit", lambda s: (s < 0).sum()),
        )
        .reset_index()
    )

    subcategory_summary["profit_margin_pct"] = (
        subcategory_summary["profit"]
        / subcategory_summary["revenue"]
        * 100
    )

    print(
        subcategory_summary
        .sort_values("profit")
        .round(2)
        .to_string(index=False)
    )


    
    print("\n========== DISCOUNT IMPACT ANALYSIS ==========")

    bins = [-0.001, 0, 0.10, 0.20, 0.30, float("inf")]
    labels = [
        "No discount",
        "0-10%",
        "10-20%",
        "20-30%",
        "Above 30%",
    ]

    df["discount_group"] = pd.cut(
        df["discount"],
        bins=bins,
        labels=labels,
        include_lowest=True,
    )

    discount_summary = (
        df.groupby("discount_group", observed=False)
        .agg(
            sales_lines=("sales", "size"),
            revenue=("sales", "sum"),
            profit=("profit", "sum"),
            loss_making_lines=("profit", lambda s: (s < 0).sum()),
        )
        .reset_index()
    )

    discount_summary["profit_margin_pct"] = (
        discount_summary["profit"]
        / discount_summary["revenue"]
        * 100
    )

    print(discount_summary.round(2).to_string(index=False))


    from pathlib import Path

    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    category_summary.to_csv(
        output_dir / "category_performance.csv",
        index=False,
    )

    regional_summary.to_csv(
        output_dir / "regional_performance.csv",
        index=False,
    )

    subcategory_summary.to_csv(
        output_dir / "subcategory_profitability.csv",
        index=False,
    )

    discount_summary.to_csv(
        output_dir / "discount_impact.csv",
        index=False,
    )

    print("\n========== EXPORT COMPLETE ==========")
    print(f"CSV files saved to: {output_dir.resolve()}")



if __name__ == "__main__":
    main()

