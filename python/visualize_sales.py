
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


if __name__ == "__main__":
    plot_category_performance()
