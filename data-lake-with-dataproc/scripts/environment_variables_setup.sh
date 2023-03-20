#!/bin/bash

# Dataproc set up variables
export DATAPROC_CLUSTER_NAME=dev-dataproc-cluster
export DATAPROC_CLUSTER_REGION=us-central1
export DATAPROC_CLUSTER_ZONE=us-central1-c
export DATAPROC_CLUSTER_MASTER_MACHINE_TYPE=n1-standard-1
export DATAPROC_CLUSTER_MASTER_BOOT_DISK_SIZE=30
export DATAPROC_CLUSTER_NUM_WORKERS=2
export DATAPROC_CLUSTER_WORKER_MACHINE_TYPE=n1-standard-1
export DATAPROC_CLUSTER_WORKER_BOOT_DISK_SIZE=30
export DATAPROC_CLUSTER_IMAGE_VERSION=1.5

# GCP Project id
export GCP_PROJECT_ID=$(gcloud config get-value project)

# GCS set up variables
export GCS_BUCKET_NAME=dev-dataproc-cluster-${GCP_PROJECT_ID}
export GCS_BUCKET_LOCATION=us-central1
export GCS_DATA_SOURCE_PATH=./source/
export GCS_DAGS_SOURCE_PATH=./dags
export GCS_BUCKET_OBJECT_PATH=source/logs/*
export GCS_BUCKET_OBJECT_NOSQL_PATH=source/nosql/create_hive_table_example.sql
export GCS_BUCKET_PYSPARK_PATH=source/pyspark/gcs_to_bigquey.py

# Cloud Composer set up variables 
export CLOUD_COMPOSER_IMAGE_VERSION=composer-1.20.10-airflow-1.10.15
export CLOUD_COMPOSER_NODE_COUNT=2
export CLOUD_COMPOSER_DISK_SIZE=30
export CLOUD_COMPOSER_LOCATION=us-central1
export CLOUD_COMPOSER_ENVIRONMENT_NAME=composer-dev
export CLOUD_COMPOSER_MACHINE_TYPE=n1-standard-1
export CLOUD_COMPOSER_PYTHON_VERSION=3
export CLOUD_COMPOSER_DAG_FILENAME=./dags/ephemeral_cluster_creator_to_submit_jobs.py
