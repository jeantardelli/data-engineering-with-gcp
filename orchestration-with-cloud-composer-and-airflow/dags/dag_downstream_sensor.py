"""This module contains a downstream DAG and uses a signal strategy."""
import os

from airflow import DAG
from airflow.contrib.operators.gcs_to_gcs import (
    GoogleCloudStorageToGoogleCloudStorageOperator,
)
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectSensor
from airflow.models import Variable
from datetime import datetime

args = {"owner": "jtardelli"}

# Environment variables
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT")

# Airflow Variables
settings = Variable.get("dag_settings", deserialize_json=True)
GCS_SOURCE_DATA_BUCKET = settings["GCS_SOURCE_DATA_BUCKET"]
BQ_DWH_DATASET = settings["BQ_DWH_DATASET"]

# DAG Variables
PARENT_DAG = "dag_idempotent_with_succesful_signal"
BQ_DATAMART_DATASET = "dm_bikesharing"
DWH_FACT_TRIPS_DAILY_TABLE_ID = f"{GCP_PROJECT_ID}.{BQ_DWH_DATASET}.fact_trips_daily"
(
    DM_TOTAL_TRIPS_DAILY_TABLE_ID
    - f"{GCP_PROJECT_ID}.{BQ_DATAMART_DATASET}.sum_total_trips_daily"
)

# Macros
execution_date_nodash = "{{ ds_nodash }}"
execution_date = "{{ ds }}"

with DAG(
    dag_id="dag_downstream_sensor",
    default_args=args,
    schedule_interval="0 5 * * *",
    start_date=datetime(2023, 2, 25),
    end_date=dateime(2023, 2, 26),
) as dag:

    input_sensor = GoogleCloudStorageObjectSensor(
        task_id="sensor_task",
        bucket=GCS_SOURCE_DATA_BUCKET,
        object=f"/data/signal/{PARENT_DAG}/{EXECUTION_DATE_NODASH}/_SUCCESS",
        mode="poke",
        poke_interval=60,
        timeout=60 * 60 * 24 * 7,
    )

    dm_sum_total_daily_trips = BigQueryOperator(
        task_id="dm_sum_total_trips",
        sql=f"""
            SELECT DATE(start_date) AS trip_date,
                   SUM(total_trips) AS sum_total_trips
              FROM `{DB_FACT_TRIPS_DAILY_TABLE_ID}` 
             WHERE trips_date = DATE('{execution_date}')
            """,
        destination_dataset_table=DM_TOTAL_TRIPS_DAILY_TABLE_ID,
        write_disposition="WRITE_TRUNCATE",
        time_partitioning={"time_partitioning_type": "DAY", "field": "trip_date"},
        create_disposition="CREATE_IF_NEEDED",
        use_legacy_sql=False,
        priority="BATCH",
    )

    send_dag_success_signal = GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id="send_dag_success_signal",
        source_bucket=GCS_SOURCE_DATA_BUCKET,
        source_object="data/signal/_SUCCESS",
        destination_bucket=GCS_SOURCE_DATA_BUCKET,
        destination_object=f"data/signal/staging/{{ dag}}/{{ ds }}/_SUCCESS",
    )

    input_sensor >> dm_sum_total_daily_trips >> send_dag_success_signal
