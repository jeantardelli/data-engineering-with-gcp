"""This DAG contains different sources and uses parameterized variables.
It also organizes table schemas in different files."""

import os
import json

from datetime import datetime
from airflow import DAG
from airflow.models import Variable
from airflow.contrib.operators.gcp_sql_operator import CloudSqlInstanceExportOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.gcs_to_gcs import (
    GoogleCloudStorageToGoogleCloudStorageOperator,
)
from airflow.contrib.operators.bigquery_check_operator import BigQueryCheckOperator
from airflow.contrib.operators.bigquery_to_gcs import BigQueryToCloudStorageOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator

# Default args passed to the DAG
args = {"owner": "jtardelli"}


def read_json_schema(gcs_file_path):
    """JSON schema loader manager. It loads a JSON schema outside of
    the code.

    Args:
        gcs_file_path (string): a string containing the gcs file path.

    Returns:
        A JSON schema
    """
    with open(gcs_file_path, "r", encoding="utf8") as file:
        schema_json = json.load(file)

    return schema_json


# Reads Cloud Composer environment variables
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT")
INSTANCE_NAME = os.environ.get("MYSQL_INSTANCE_NAME")

# Reads Airflow environment variables
settings = Variable.get("dag_with_parameterized_variables", deserialize_json=True)

# Passes Airflow environment variable to DAG variables
GCS_SOURCE_DATA_BUCKET = settings["gcs_source_data_bucket"]
BQ_RAW_DATASET = settings["bq_raw_dataset"]
BQ_DWH_DATASET = settings["bd_dwh_dataset"]

# Airflow macro
# Airflow macro variables are variables that return information about the DAG
EXTRACTED_DATE = "{{ ds }}"
EXTRACTED_DATE_NODASH = "{{ ds_nodash }}"

# Regions
GCS_REGIONS_SOURCE_OBJECT = f"{GCS_SOURCE_DATA_BUCKET}/source/regions/regions.csv"
GCS_REGIONS_TARGET_OBJECT = (
    f"{GCS_SOURCE_DATA_BUCKET}/regions/{EXTRACTED_DATE_NODASH}/regions.csv"
)
BQ_REGIONS_TABLE_NAME = "regions"
BQ_REGIONS_TABLE_ID = f"{GCP_PROJECT_ID}.{BQ_RAW_DATASET}.{BQ_REGIONS_TABLE_NAME}"
BQ_RETIONS_TABLE_SCHEMA = read_json_schema(
    "/home/airflow/gcs/data/schema/regions_schema.json"
)

# Stations
GCS_STATION_SOURCE_OBJECT = "stations/stations.csv"
export_body = {
    "exportContext": {
        "fileType": "csv",
        "uri": f"gs://{GCS_SOURCE_DATA_BUCKET}/{GCS_STATION_SOURCE_OBJECT}",
        "csvExportoptions": {"selectQuery": "SELECT * FROM apps_db.stations"},
    }
}

BQ_STATIONS_TABLE_NAME = "stations"
BQ_STATIONS_TABLE_ID = f"{GCP_PROJECT_ID}.{BQ_RAW_DATASET}.{BQ_STATIONS_TABLE_NAME}"
BQ_STATIONS_TABLE_SCHEMA = read_json_schema(
    "/home/airflow/gcs/data/schema/stations_schema.json"
)

# Trips
BQ_TEMP_EXTRACT_DATASET_NAME = "temp_staging"
BQ_TEMP_EXTRACT_TABLE_NAME = "trips"
BQ_TEMP_TABLE_ID = f"{GCP_PROJECT_ID}.{BQ_TEMP_EXTRACT_DATASET_NAME}.{BQ_TEMP_EXTRACT_TABLE_NAME}_{EXTRACTED_DATE_NODASH}"
GCS_TRIPS_SOURCE_OBJECT = "trips/{EXTRACTED_DATE_NODASH}/*.csv"
GCS_TRIPS_SOURCE_URI = f"gs://{GCS_SOURCE_DATA_BUCKET}/{GCS_TRIPS_SOURCE_OBJECT}"
BQ_TRIPS_TABLE_NAME = "trips"
BQ_TRIPS_TABLE_ID = f"{GCP_PROJECT_ID}.{BQ_RAW_DATASET}.{BQ_TRIPS_TABLE_NAME}"
BQ_TRIPS_TABLE_SCHEMA = read_json_schema(
    "/home/airflow/gcs/data/schema/trips_schema.json"
)

# DWH
BQ_FACT_TRIPS_DAILY_TABLE_NAME = "fact_trips_daily"
BQ_FACT_TRIPS_DAILY_TABLE_ID = f"{GCP_PROJECT_ID}.{BQ_DWH_DATASET}.{BQ_FACT_TRIPS_DAILY_TABLE_NAME}${EXTRACTED_DATE_NODASH}"
BQ_DIM_STATIONS_TABLE_NAME = "dim_stations"
BQ_DIM_STATIONS_TABLE_ID = (
    f"{GCP_PROJECT_ID}.{BQ_DWH_DATASET}.{BQ_FACT_TRIPS_DAILY_TABLE_NAME}"
)

# Declare DAG
with DAG(
    dag_id="dag_with_parameterized_variables",
    default_args=args,
    schedule_interval="0 5 * * *",
    start_date=datetime(2023, 2, 25),
    end_date=datetime(2023, 2, 26),
) as dag:

    # Regions
    # Copies objects from a bucket to another, with renaming if requested
    gcs_to_gcs_region = GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id="gcs_to_gcs_region",
        source_bucket=GCS_SOURCE_DATA_BUCKET,
        source_object=GCS_REGIONS_SOURCE_OBJECT,
        destination_bucket=GCS_SOURCE_DATA_BUCKET,
        destination_object=GCS_REGIONS_TARGET_OBJECT,
    )

    # Execute a BigQuery load job to load existing dataset from Google
    # Cloud Storage to BigQuery table
    gcs_to_bigquery_region = GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bigquery_region",
        bucket=GCS_SOURCE_DATA_BUCKET,
        source_objects=[GCS_REGIONS_SOURCE_OBJECT],
        destination_project_dataset_table=BQ_STATIONS_TABLE_ID,
        schema_fields=BQ_STATIONS_TABLE_SCHEMA,
        write_disposition="WRITE_TRUNCATE",
    )

    # Stations
    # Exports data from a Cloud SQL instance to a Cloud Storage bucket
    # as a SQL dump or CSV file
    export_mysql_station = CloudSqlInstanceExportOperator(
        task_id="export_mysql_station",
        project_id=GCP_PROJECT_ID,
        body=export_body,
        instance=INSTANCE_NAME,
    )

    # Execute a BigQuery load job to load existing dataset from Google
    # Cloud Storage to BigQuery table
    gcs_to_bigquery_station = GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bigquery_station",
        bucket=GCS_SOURCE_DATA_BUCKET,
        source_objects=[GCS_STATION_SOURCE_OBJECT],
        destination_project_dataset_table=BQ_STATIONS_TABLE_ID,
        schema_fields=BQ_STATIONS_TABLE_SCHEMA,
        write_disposition="WRITE_TRUNCATE",
    )

    # Trips
    # Executes BigQuery SQL queries in a specific BigQuery database
    bigquery_to_bigquery_temp_trips = BigQueryOperator(
        task_id="bigquery_to_bigquery_temp_trips",
        sql=f"""
            SELECT *
              FROM `bigquery-public-data.san_francisco_bikeshare.bikeshare_trips`
             WHERE DATE(start_date) = DATE('{EXTRACTED_DATE}')
            """,
        use_legacy=False,
        destination_dataset_table=BQ_TEMP_TABLE_ID,
        write_disposition="WRITE_TRUNCATE",
        create_disposition="CREATE_IF_NEEDED",
    )

    # Transfers a BigQuery table to a Google Cloud Storage bucket
    bigquery_to_gcs_extract_trips = BigQueryToCloudStorageOperator(
        task_id="bq_to_gcs_extract_trips",
        source_project_dataset_table=BQ_TEMP_TABLE_ID,
        destination_cloud_storage_uris=[GCS_TRIPS_SOURCE_URI],
        print_header=False,
        export_format="CSV",
    )

    # Execute a BigQuery load job to load existing dataset from Google
    # Cloud Storage to BigQuery table
    gcs_to_bigquery_trips = GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bigquery_trips",
        bucket=GCS_SOURCE_DATA_BUCKET,
        source_objects=[GCS_TRIPS_SOURCE_OBJECT],
        destination_project_dataset_table=BQ_TRIPS_TABLE_ID
        + f"${EXTRACTED_DATE_NODASH}",
        schema_fields=BQ_TRIPS_TABLE_SCHEMA,
        time_partitioning={"time_partitioning_type": "DAY", "field": "start_date"},
        write_disposition="WRITE_TRUNCATE",
    )

    # DWH
    # Executes BigQuery SQL queries in a specific BigQuery database
    dwh_fact_trips_daily = BigQueryOperator(
        task_id="dwh_fact_trips_daily",
        sql=f"""
            SELECT DATE(start_date) AS trip_date,
                   start_station_id,
                   COUNT(trip_id) AS total_trips,
                   SUM(duration_sec) AS sum_duration_sec,
                   AVG(duration_sec) AS avg_duration_sec
              FROM `{BQ_TRIPS_TABLE_ID}`
             WHERE DATE(start_date) = DATE('{EXTRACTED_DATE}')
             GROUP BY trip_date, start_station_id
            """,
        destination_dataset_table=BQ_FACT_TRIPS_DAILY_TABLE_ID,
        write_disposition="WRITE_TRUNCATE",
        create_disposition="CREATE_IF_NEEDED",
        use_legacy_sql=False,
        priority="BATCH",
    )

    # Executes BigQuery SQL queries in a specific BigQuery database
    dwh_dim_stations = BigQueryOperator(
        task_id="dwh_dim_stations",
        sql=f"""
            SELECT station_id,
                   stations.name AS station_name,
                   regions.name AS region_name,
                   capacity
              FROM `{BQ_STATIONS_TABLE_ID}` stations
              JOIN `{BQ_REGIONS_TABLE_ID}` regions
                   ON stations.region_id = CAST(regions.region_id AS STRING)
            """,
        destination_dataset_table=BQ_DIM_STATIONS_TABLE_ID,
        write_disposition="WRITE_TRUNCATE",
        create_disposition="CREATE_IF_NEEDED",
        use_legacy_sql=False,
        priority="BATCH",
    )

    # Performs checks against BigQuery
    bigquery_row_count_check_dwh_fact_trips_daily = BigQueryCheckOperator(
        task_id="bigquery_row_count_check_dwh_fact_trips_daily",
        sql=f"""
            SELECT COUNT(*)
              FROM `{BQ_FACT_TRIPS_DAILY_TABLE_ID}`
             WHERE trip_date = DATE('{EXTRACTED_DATE}')
            """,
        use_legacy=False,
    )

    bigquery_row_count_check_dwh_dim_stations = BigQueryCheckOperator(
        task_id="bigquery_row_count_check_dwh_dim_stations",
        sql=f"SELECT COUNT(*) FROM `{BQ_DIM_STATIONS_TABLE_ID}`",
        use_legacy=False,
    )

    send_dag_success_signal = GoogleCloudStorageToGoogleCloudStorageOperator(
        task_id="send_dag_success_signal",
        source_bucket=GCS_SOURCE_DATA_BUCKET,
        source_object="data/signal/_SUCCESS",
        destination_bucket=GCS_SOURCE_DATA_BUCKET,
        destination_object=f"data/signal/staging/sensor/{EXTRACTED_DATE_NODASH}/_SUCCESS",
    )

    # Define DAG dependencies
    export_mysql_station >> gcs_to_bigquery_trips
    gcs_to_gcs_region >> gcs_to_bigquery_region
    (
        bigquery_to_bigquery_temp_trips
        >> bigquery_to_gcs_extract_trips
        >> gcs_to_bigquery_trips
    )

    (
        [gcs_to_bigquery_station, gcs_to_bigquery_region, gcs_to_bigquery_trips]
        >> dwh_fact_trips_daily
        >> bigquery_row_count_check_dwh_fact_trips_daily
    )
    (
        [gcs_to_bigquery_station, gcs_to_bigquery_region, gcs_to_bigquery_trips]
        >> dwh_dim_stations
        >> bigquery_row_count_check_dwh_dim_stations
    )
    (
        [
            bigquery_row_count_check_dwh_fact_trips_daily,
            bigquery_row_count_check_dwh_dim_stations
        ]
        >> send_dag_success_signal
    )
