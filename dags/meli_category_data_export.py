"""This file has the functions to upload the data into a Postgres database."""

import os
import pandas as pd
from sqlalchemy import create_engine

def upload_data_to_postgres(**kwargs):
    """
    This function uploads the data from a csv file into a postgres table.
    kwargs:
        category_id: The category id to get the data from.
    """
    #read connection_string environment variable into a variable from os.
    connection_string = os.environ.get("AIRFLOW__CORE__SQL_ALCHEMY_CONN")
    
    db = create_engine(connection_string)
    conn = db.connect()

    category_id = kwargs["category_id"]
    df = pd.read_csv(f"/opt/airflow/dags/datasets/{category_id}_clean.csv")

    # insert data into postgres table.
    df.to_sql("meli_categories_info", conn, if_exists="replace", index=False)