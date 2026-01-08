import pandas as pd

required_columns = {"date", "revenue", "expenses", "profit"}

def validate_dataframe(df: pd.DataFrame):
    
    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(f"Missing required columns {missing}")
    
    if df.isnull().any().any():
        raise ValueError("Null Values detected in financial data")
    
    if (df["revenue"] < 0).any():
        raise ValueError("Revenue cannot be negative")
    
    if (df["expenses"] < 0).any():
        raise ValueError("Expenses cannot be negative")
    
    return True