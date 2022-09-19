"""This file has the functions to consume the Meli API and save the data into a csv file."""

import requests
import pandas as pd

def get_category_relevant_data(**kwargs):
    """
    This function gets the category data from the Meli API.

    kwargs:
        category_id: The category id to get the data from.
    """
    url = f"https://api.mercadolibre.com/sites/MLA/search?category={kwargs['category_id']}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def save_category_data(data, category_id):
    """
    This function saves the category data into a csv file.

    Args:
        data(dict): The data to save.
        category_id(string): The category id to save the data into.
    """
    df = pd.DataFrame(data["results"])
    print(df)
    df.to_csv(f"/opt/airflow/dags/datasets/{category_id}.csv", index=True)

def import_category_data(**kwargs):
    """
    This function gets the category data from the Meli API and saves it into a csv file.
    
    kwargs:
        category_id: The category id to get the data from.
    """
    category_id = kwargs["category_id"]
    data = get_category_relevant_data(category_id=category_id)
    save_category_data(data, category_id)