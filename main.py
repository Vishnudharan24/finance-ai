from Ingestion.data_loader import data_loader
from Ingestion.data_normalizer import normalize_columns
from Ingestion.data_validator import validate_dataframe
from analytics_engine.enginev1 import compute_basic_metrics, compute_mom_trends

import pandas as pd

def ingest_financial_data(file_path: str):
    df_raw = data_loader(file_path)

    df_normalized = normalize_columns(df_raw)

    df_normalized["date"] = pd.to_datetime(df_normalized["date"])
    # print(df_normalized["date"])

    validate_dataframe(df_normalized)

    return df_normalized

def analyze_data(df_normal):

    basic_metrics = compute_basic_metrics(df_normal)
    mom_trends = compute_mom_trends(df_normal)

    return basic_metrics, mom_trends

if __name__ == "__main__":
    # df = ingest_financial_data("sample_financials.csv")

    file_path = input("Enter the file path")
    normal_df = ingest_financial_data(file_path)

    # print(normal_df.head())

    basic_metrics, mom_trends = analyze_data(normal_df)

    basic_metrics = pd.DataFrame([basic_metrics])

    # analytics = pd.concat([basic_metrics, mom_trends], axis = 1)

    basic_metrics.to_json("metrics_summary.json", orient = "records", date_format = "iso", indent = 4)
    mom_trends.to_json("mom_trends.json", orient = "records", date_format = "iso", indent = 4)

