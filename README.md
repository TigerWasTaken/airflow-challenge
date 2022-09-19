# airflow-challenge

This pipeline is designed to ingest data from a Mercado Libre API, transform it, and load it into a Postgres database. The pipeline is designed to be run on a daily basis, and will only load data that has not been loaded before.

In order to run the pipeline you'll need to have a working docker/docker-compose environment.

Be sure to have the correct environment variables set in the `.env` file. You can copy the `.env.example` file and fill in the values.

Start the pipeline doing:

```bash
docker-compose up
```

This will start the airflow webserver and scheduler. You can access the webserver at http://localhost:8080

The pipeline is defined in the `dags` folder. The `dags` folder is mounted as a volume in the airflow container, so you can edit the pipeline without having to restart the containers.


When the webserver is up and running, you need to create the connection to the postgres database. Go to the admin page and create a new connection with the following values:

- Conn Id: `postgres_conn`
- Conn Type: `Postgres`
- Host: `postgres`
- Schema: `airflow`
- Login: `airflow`
- Password: `airflow`
- Port: `5432`

Also, you need to create the connection to the HTTP API. Go to the admin page and create a new connection with the following values:

- Conn Id: `meli_category_data_ingestion_api`
- Conn Type: `HTTP`
- Host: `https://api.mercadolibre.com/`

And the last connection for check the file availability in the local filesystem:

- Conn Id: `meli_data_path`
- Conn Type: `File`
- Extra: `{"path": "/opt/airflow/dags/datasets/"}`

And that's it! You can now run the pipeline.

To run the pipeline you need to create a new DAG run. Go to the DAG page and click on the `Trigger DAG` button of the `meli_category_data_pipeline`. This will run the pipeline.

Implementation details:

    I used the `PythonOperator` to run the most of the tasks. I could have used the `BashOperator` but I wanted to have more control over the execution of the tasks. 

    I used the `PostgresOperator` to run the SQL queries.

    I used the `HttpSensor` to check if the API is available.

    I used the `FileSensor` to check if the file is available in the local filesystem.

    To transform the data I used the `pandas` library, because the data was small enough to fit in memory. If the data was bigger, I would have used `spark` to process the data.

    To get the data from the API I used the `requests` library.

    I used the `datetime` library to get the current date and to format the date in the correct format.

    I used the `os` library to get the environment variables in runtime.

    I used a python operator to send the emails with the results of the pipeline. I could have used the `EmailOperator` but python combined with pandas is more flexible.


