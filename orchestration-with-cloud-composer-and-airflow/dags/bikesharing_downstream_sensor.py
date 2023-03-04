"""This module contains a downstream DAG and uses a signal strategy."""
import os

from airflow import DAG
from airflow.models import Variable
from airflow.contrib.operators.gcs_to_gcs import (
    GoogleCloudStorageToGoogleCloudStorageOperator,
)
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.sensors.gcs_sensor import GoogleCloudStorageObjectSensor
from datetime import datetime

args = {"owner": "jtardelli"}

# Environment variables
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT")

# Reads Airflow environment variables
settings = Variable.get("parameterized_variables", deserialize_json=True)

# Passes Airflow environment variable to DAG variables
GCS_BUCKET_NAME = settings["gcs_bucket_name"]
BQ_DWH_DATASET = settings["bq_dwh_dataset"]

# Other Variables
BQ_DWH_TABLE_NAME = "fact_trips_daily"
BQ_DATAMART_DATASET = "dm_operations"
BQ_DATAMART_TABLE_NAME = "sum_total_trips_daily"
DWH_FACT_TRIPS_DAILY_TABLE_ID = f"{GCP_PROJECT_ID}.{BQ_DWH_DATASET}.{BQ_DWH_TABLE_NAME}"
DM_TOTAL_TRIPS_DAILY_TABLE_ID = f"{GCP_PROJECT_ID}.{BQ_DATAMART_DATASET}.{BQ_DATAMART_TABLE_NAME}"


# Macros
EXTRACTED_DATE_NODASH = "{{ ds_nodash }}"
EXTRACTED_DATE = "{{ ds }}"
DAG_NAME = "{{ dag }}"

with DAG(
    dag_id="dag_bikesharing_downstream_sensor",
    default_args=args,
    schedule_interval="0 5 * * *",
    start_date=datetime(2018, 1, 1),
    end_date=datetime(2018, 1, 2),
) as dag:

    input_sensor = GoogleCloudStorageObjectSensor(
        task_id="sensor_task",
        bucket=GCS_BUCKET_NAME,
        object=f"from-airflow/signals/{BQ_DWH_DATASET}/{BQ_DWH_TABLE_NAME}/{EXTRACTED_DATE_NODASH}/_SUCCESS",
        mode="poke",
        poke_interval=60,
        timeout=60 * 60 * 24 * 7,
    )

    dm_sum_total_daily_trips = BigQueryOperator(
        task_id="dm_sum_total_trips",
        sql=f"""
            SELECT trip_date,
                   SUM(total_trips) AS sum_total_trips
              FROM `{DWH_FACT_TRIPS_DAILY_TABLE_ID}` 
             WHERE trip_date = DATE('{EXTRACTED_DATE}')
             GROUP BY trip_date
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
        source_bucket=GCS_BUCKET_NAME,
        source_object=f"from-airflow/signals/{BQ_DWH_DATASET}/{BQ_DWH_TABLE_NAME}/{EXTRACTED_DATE_NODASH}/_SUCCESS",
        destination_bucket=GCS_BUCKET_NAME,
        destination_object=f"from-airflow/signals/{BQ_DATAMART_DATASET}/{BQ_DATAMART_TABLE_NAME}/{EXTRACTED_DATE_NODASH}/_SUCCESS",
    )

    input_sensor >> dm_sum_total_daily_trips >> send_dag_success_signal
