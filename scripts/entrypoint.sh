#!/usr/bin/env bash
airflow db init
airflow users create -r Admin -u $AIRFLOW_USER -e $AIRFLOW_EMAIL -p $AIRFLOW_PASSWORD -f $AIRFLOW_FIRSTNAME -l $AIRFLOW_LASTNAME
airflow webserver