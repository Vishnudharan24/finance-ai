from Ingestion.data_loader import data_loader
from Ingestion.data_normalizer import normalize_columns
from Ingestion.data_validator import validate_dataframe

import pandas as pd

def ingest_financial_data(file_path: str):
    df_raw = data_loader(file_path)

    df_normalized = normalize_columns(df_raw)

    df_normalized["date"] = pd.to_datetime(df_normalized["date"])

    validate_dataframe(df_normalized)

    return df_normalized


if __name__ == "__main__":
    df = ingest_financial_data("sample_financials.csv")
    print(df.head())
