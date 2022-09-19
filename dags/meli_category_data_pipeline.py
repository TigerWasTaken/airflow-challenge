from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta
from meli_category_data_ingestion import import_category_data
from meli_category_data_transformation import transform_data
from meli_category_data_export import upload_data_to_postgres
from send_category_report import send_email_notif
import os


default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}


with DAG("meli_category_data_pipeline", start_date=datetime(2022, 9 ,10), 
    schedule_interval="@daily", default_args=default_args, catchup=False) as dag:
    
    is_meli_category_data_ingestion_available = HttpSensor(
        endpoint="sites/MLA/categories",
        task_id="is_meli_category_data_ingestion_available",
        http_conn_id="meli_category_data_ingestion_api",
        response_check=lambda response: "MLA5725" in response.text,
        poke_interval=5,
        timeout=20
    )

    download_category_data = PythonOperator(
        task_id="download_category_data",
        python_callable=import_category_data,
        op_kwargs={"category_id": "MLA1577"}
    )

    transform_category_data = PythonOperator(
        task_id="transform_category_data",
        python_callable=transform_data,
        op_kwargs={"category_id": "MLA1577"}
    )

    create_postgres_table = PostgresOperator(
        task_id="create_postgres_table",
        postgres_conn_id="postgres_conn",
        sql="/sql/create_table_meli_categories_info.sql"
    )

    is_meli_category_data_file_available = FileSensor(
        task_id="is_meli_category_data_file_available",
        fs_conn_id="meli_data_path",
        filepath="MLA1577_clean.csv",
        poke_interval=5,
        timeout=20
    )

    upload_category_data_to_postgres = PythonOperator(
        task_id="upload_category_data_to_postgres",
        python_callable=upload_data_to_postgres,
        op_kwargs={"category_id": "MLA1577"}
    )

    send_email_notification = PythonOperator(
        task_id="send_email_notification",
        python_callable=send_email_notif,
        op_kwargs={"user": os.environ.get("SFTP_EMAIL_USER"),
                    "pwd": os.environ.get("SFTP_EMAIL_PASSWORD"),
                    "recipient": "maty.tiger@gmail.com",
                    "subject": "Report with the most proffitable products",
                    "body": "Report with the most proffitable products.",
                    "category_id": "MLA1577"}
    )



    is_meli_category_data_ingestion_available >> download_category_data >> transform_category_data >> [is_meli_category_data_file_available, send_email_notification]
    is_meli_category_data_file_available >> create_postgres_table >> upload_category_data_to_postgres


