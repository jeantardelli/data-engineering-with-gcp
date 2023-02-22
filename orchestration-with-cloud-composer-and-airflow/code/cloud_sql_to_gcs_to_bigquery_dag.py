"""This module contains a DAG for a simple ETL that extract data from
Cloud SQL sources to GCS bucket and then to BigQuery."""

import os
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.contrib.operators.gcp_sql_operator import CloudSqlInstanceExportOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator


# Default args to be passed to the DAG
args = {"owner": "jtardelli"}

# GCS bucket
GCS_BUCKET = os.getenv("GCS_BUCKET")

# Define the Cloud SQL operator GCP Project parameter
GCP_PROJECT_ID = os.getenv("PROJECT_ID")

# Define the Cloud SQL operator instance name parameter
INSTANCE_NAME = os.getenv("INSTANCE_NAME")

# URI to export data to. Used by the Cloud SQL operator body parameter
EXPORT_URI = f"gs://{GCS_BUCKET}/mysql_export/from_composer/stations/stations.csv"

# SQL query to extract data from the database. Used by the Cloud SQL operator
# body parameter
SQL_QUERY = "SELECT * FROM apps_db.stations"

# Define body parameter as a JSON. Used by the Cloud SQL operator
export_body = {
    "exportContext": {
        "fileType": "csv",
        "uri": EXPORT_URI,
        "csvExportOptions": {"selectQuery": SQL_QUERY},
    }
}

# Declares the DAG that will use GCP operators
with DAG(
    dag_id="dag_load_data_from_cloud_sql_to_gcs_to_bigquery",
    default_args=args,
    schedule_interval="0 5 * * *",
    start_date=days_ago(1),
) as dag:

    # Cloud SQL operator. It contains the Cloud SQL project ID,
    # the Cloud SQL instance name, and the body
    sql_export_task = CloudSqlInstanceExportOperator(
        project_id=GCP_PROJECT_ID,
        body=export_body,
        instance=INSTANCE_NAME,
        task_id="sql_export_task",
    )

    # Google Cloud Storage to BigQuery operator. This operator has some
    # parameters similar to the BigQuery Python API
    gcs_to_bigquery = GoogleCloudStorageToBigQueryOperator(
        task_id="gcs_to_bigquery_example",
        bucket=GCS_BUCKET,
        source_objects=["mysql_export/from_composer/stations/stations.csv"],
        destination_project_dataset_table="raw_bikesharing.stations",
        schema_fields=[
            {"name": "station_id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "name", "type": "STRING", "mode": "NULLABLE"},
            {"name": "region_id", "type": "STRING", "mode": "NULLABLE"},
            {"name": "capacity", "type": "INTEGER", "mode": "NULLABLE"},
        ],
        write_disposition="WRITE_TRUNCATE",
    )

    # BigQuery Operator. It performs a very simple aggregation
    bigquery_to_bigquery = BigQueryOperator(
        task_id="bigquery_to_bigquery",
        sql="SELECT COUNT(*) AS count FROM `raw_bikesharing.stations`",
        destination_dataset_table="dwh_bikesharing.temporary_stations_count",
        write_disposition="WRITE_TRUNCATE",
        create_disposition="CREATE_IF_NEEDED",
        use_legacy_sql=False,
        priority="BATCH",
    )

    sql_export_task >> gcs_to_bigquery >> bigquery_to_bigquery
