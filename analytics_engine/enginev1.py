# analytics/metrics.py
import pandas as pd

def compute_basic_metrics(df: pd.DataFrame) -> dict:

    return {
        "total_revenue": df["revenue"].sum(),
        "avg_monthly_revenue": df["revenue"].mean(),
        "total_expenses": df["expenses"].sum(),
        "avg_monthly_expenses": df["expenses"].mean(),
        "total_profit": df["profit"].sum(),
        "avg_profit_margin": (df["profit"] / df["revenue"]).mean(),
        "avg_growth_pct" : df["growth_pct"].mean()
    }

def compute_mom_trends(df):

    df = df.sort_values("date")

    return{

        "mom_revenue_change": df["revenue"].pct_change(),
        "mom_expense_change": df["expenses"].pct_change(),
        "mom_profit_change": df["profit"].pct_change()

    }
