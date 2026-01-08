# ingestion/normalizer.py
import pandas as pd

column_map = {
    "date": ["date", "month", "period"],
    "revenue": ["revenue", "sales", "income"],
    "expenses": ["expenses", "costs"],
    "profit": ["profit", "net_profit"],
    "growth_pct": ["growth", "growth_pct", "growth_percentage"]
}

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    normalized = {}

    for standard_col, variants in column_map.items():
        for v in variants:
            if v in df.columns:
                normalized[standard_col] = df[v]
                break

    normalized_df = pd.DataFrame(normalized)

    return normalized_df


