"""This file has the function to apply the data transformation to the category data."""
import pandas as pd

def transform_data(**kwargs):
    """
    This function transforms the data from a csv file, removing the columns that are not relevant and adding new columns.
    
    kwargs:
        category_id: The category id to get the data from.
    """
    category_id = kwargs["category_id"]
    columns_desired=["id", "site_id", "title", "price", "sold_quantity", "thumbnail"]

    df = pd.read_csv(f"/opt/airflow/dags/datasets/{category_id}.csv")

    df = df[columns_desired]
    df["total_earnings"] = df["price"] * df["sold_quantity"]
    df["created_date"] = pd.to_datetime("today").tz_localize("UTC").tz_convert("America/Argentina/Buenos_Aires")

    df.to_csv(f"/opt/airflow/dags/datasets/{category_id}_clean.csv", index=False)