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