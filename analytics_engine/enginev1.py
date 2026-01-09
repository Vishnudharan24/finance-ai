import pandas as pd

def compute_basic_metrics(df: pd.DataFrame) -> dict:
    return {
        "total_revenue": df["revenue"].sum(),
        "avg_monthly_revenue": df["revenue"].mean(),
        "total_expenses": df["expenses"].sum(),
        "avg_monthly_expenses": df["expenses"].mean(),
        "total_profit": df["profit"].sum(),
        "avg_profit_margin": (df["profit"] / df["revenue"]).mean(),
        "avg_growth_pct": df["growth_pct"].mean()
    }

def compute_mom_trends(df):
    df = df.sort_values("date")
    
    trends_df = pd.DataFrame({
        "date": df["date"],
        "revenue_mom_pct": df["revenue"].pct_change() * 100,
        "expenses_mom_pct": df["expenses"].pct_change() * 100,
        "profit_mom_pct": df["profit"].pct_change() * 100
    })
    
    return trends_df
