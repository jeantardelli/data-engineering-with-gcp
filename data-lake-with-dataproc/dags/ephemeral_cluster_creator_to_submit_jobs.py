"""This module usea Airflow to create a Dataproc cluster, submit a pyspark job,
and delete the cluster when finished."""

import os

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.google.cloud.operators.dataproc import (
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator,
)


# Envrionment variables to be used by the DAG
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
GCS_BUCKET_PYSPARK_PATH = os.environ.get("GCS_BUCKET_PYSPARK_PATH")

# Dataproc cluster config
DATAPROC_CLUSTER_REGION = os.environ.get("DATAPROC_CLUSTER_REGION")
DATAPROC_CLUSTER_ZONE = os.environ.get("DATAPROC_CLUSTER_ZONE")
DATAPROC_CLUSTER_NAME = os.environ.get("DATAPROC_CLUSTER_NAME")
DATAPROC_CLUSTER_NAME += "-{{ ds_nodash }}"
DATAPROC_CLUSTER_MASTER_MACHINE_TYPE = os.environ.get("DATAPROC_CLUSTER_MASTER_MACHINE_TYPE")
DATAPROC_CLUSTER_MASTER_BOOT_DISK_SIZE = os.environ.get("DATAPROC_CLUSTER_MASTER_BOOT_DISK_SIZE")
DATAPROC_CLUSTER_NUM_WORKERS = os.environ.get("DATAPROC_CLUSTER_NUM_WORKERS")
DATAPROC_CLUSTER_WORKER_MACHINE_TYPE = os.environ.get("DATAPROC_CLUSTER_WORKER_MACHINE_TYPE")
DATAPROC_CLUSTER_WORKER_BOOT_DISK_SIZE = os.environ.get("DATAPROC_CLUSTER_WORKER_BOOT_DISK_SIZE")
DATAPROC_CLUSTER_IMAGE_VERSION = os.environ.get("DATAPROC_CLUSTER_IMAGE_VERSION")

PYSPARK_JOB = {
    "reference": {"project_id": "GCP_PROJECT_ID"},
    "placement": {"cluster_name": "DATAPROC_CLUSTER_NAME"},
    "pyspark_job": {
        "main_python_file_uri": GCS_BUCKET_PYSPARK_PATH,
        "jar_file_uris": ["gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar"],
    },
}

# More parameters can be passed here
DATAPROC_CLUSTER_CONFIG = {
    "gce_cluster_config": {
        "zone_uri": DATAPROC_CLUSTER_ZONE,
        "internal_ip_only": True,
    },
    "master_config": {
        "num_instances": 1,
        "machine_type_uri": DATAPROC_CLUSTER_MASTER_MACHINE_TYPE,
        "disk_config": {"boot_disk_size_gb": int(DATAPROC_CLUSTER_MASTER_BOOT_DISK_SIZE)},
    },
    "worker_config": {
        "num_instances": int(DATAPROC_CLUSTER_NUM_WORKERS),
        "machine_type_uri": DATAPROC_CLUSTER_WORKER_MACHINE_TYPE,
        "disk_config": {"boot_disk_size_gb": int(DATAPROC_CLUSTER_WORKER_BOOT_DISK_SIZE)},
    },
    "software_config": {"image_version": DATAPROC_CLUSTER_IMAGE_VERSION}
}

args = {"owner": "jtardelli"}

# Define DAG
with DAG(
    dag_id="dataproc_emphemeral_cluster_job",
    schedule_interval="0 5 * * *",
    start_date=days_ago(1),
    default_args=args,
) as dag:

    # Create Dataproc cluster
    create_cluster = DataprocCreateClusterOperator(
        task_id="create_dataproc_cluster",
        project_id=GCP_PROJECT_ID,
        cluster_config=DATAPROC_CLUSTER_CONFIG,
        region=DATAPROC_CLUSTER_REGION,
        cluster_name=DATAPROC_CLUSTER_NAME,
        idle_delete_ttl=600,
    )

    # Submit PySpark Job
    pyspark_task = DataprocSubmitJobOperator(
        task_id="pyspark_task",
        job=PYSPARK_JOB,
        location=DATAPROC_CLUSTER_REGION,
        project_id=GCP_PROJECT_ID,
    )

    # Delete Dataproc Cluster
    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_dataproc_cluster",
        project_id="GCP_PROJECT_ID",
        cluster_name=DATAPROC_CLUSTER_NAME,
        region=DATAPROC_CLUSTER_REGION,
    )

    create_cluster >> pyspark_task >> delete_cluster
