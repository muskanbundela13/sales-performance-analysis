
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "processed"
CHART_DIR = PROJECT_ROOT / "reports" / "figures"

CHART_DIR.mkdir(parents=True, exist_ok=True)


def plot_category_performance():
    df = pd.read_csv(DATA_DIR / "category_performance.csv")

    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(df))
    width = 0.35

    ax.bar(
        [i - width / 2 for i in x],
        df["revenue"],
        width,
        label="Revenue",
    )
    ax.bar(
        [i + width / 2 for i in x],
        df["profit"],
        width,
        label="Profit",
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["category"])
    ax.set_title("Revenue vs Profit by Category")
    ax.set_ylabel("Amount")
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        CHART_DIR / "category_performance.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)

    print("Saved category_performance.png")


def plot_regional_performance():
    df = pd.read_csv(DATA_DIR / "regional_performance.csv")

    # Aggregate state-level rows into one row per region.
    regional = (
        df.groupby("region", as_index=False)
        .agg(
            revenue=("total_revenue", "sum"),
            profit=("total_profit", "sum"),
        )
        .sort_values("revenue", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(9, 5))
    x = range(len(regional))
    width = 0.35

    ax.bar(
        [i - width / 2 for i in x],
        regional["revenue"],
        width,
        label="Revenue",
    )
    ax.bar(
        [i + width / 2 for i in x],
        regional["profit"],
        width,
        label="Profit",
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(regional["region"])
    ax.set_title("Revenue vs Profit by Region")
    ax.set_ylabel("Amount")
    ax.legend()

    fig.tight_layout()
    fig.savefig(
        CHART_DIR / "regional_performance.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)

    print("Saved regional_performance.png")


def plot_discount_impact():
    df = pd.read_csv(DATA_DIR / "discount_impact.csv")

    # Use the discount bands and margins calculated by the analysis.
    band_column = "discount_band"
    margin_column = "profit_margin_pct"

    df = df.sort_values(band_column)

    fig, ax = plt.subplots(figsize=(10, 5))

    bars = ax.bar(
        df[band_column].astype(str),
        df[margin_column],
    )

    # Distinguish negative-margin bands from profitable bands.
    for bar, margin in zip(bars, df[margin_column]):
        if margin < 0:
            bar.set_hatch("//")

    ax.axhline(0, linewidth=1)
    ax.set_title("Profit Margin by Discount Band")
    ax.set_xlabel("Discount Band")
    ax.set_ylabel("Profit Margin (%)")
    ax.tick_params(axis="x", rotation=20)

    fig.tight_layout()
    fig.savefig(
        CHART_DIR / "discount_impact.png",
        dpi=300,
        bbox_inches="tight",
    )
    plt.close(fig)

    print("Saved discount_impact.png")


if __name__ == "__main__":
    plot_category_performance()
    plot_regional_performance()
    plot_discount_impact()
