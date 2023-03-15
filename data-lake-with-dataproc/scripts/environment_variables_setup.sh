#!/bin/bash

export DATAPROC_CLUSTER_NAME=dev-dataproc-cluster
export DATAPROC_CLUSTER_REGION=us-central1
export DATAPROC_CLUSTER_ZONE=us-central1-c
export DATAPROC_CLUSTER_MASTER_MACHINE_TYPE=n1-standard-2
export DATAPROC_CLUSTER_MASTER_BOOT_DISK_SIZE=30
export DATAPROC_CLUSTER_NUM_WORKERS=2
export DATAPROC_CLUSTER_WORKER_MACHINE_TYPE=n1-standard-2
export DATAPROC_CLUSTER_WORKER_BOOT_DISK_SIZE=30
export DATAPROC_CLUSTER_IMAGE_VERSION=2.0-debian10

export GCP_PROJECT_ID=$(gcloud config get-value project)

export GCS_BUCKET_NAME=dev-dataproc-cluster-${GCP_PROJECT_ID}
export GCS_BUCKET_LOCATION=us-central1
export GCS_DATA_SOURCE_PATH=./source/
export GCS_BUCKET_OBJECT_PATH=source/logs/*
export GCS_BUCKET_OBJECT_NOSQL_PATH=source/nosql/create_hive_table_example.sql
export GCS_BUCKET_PYSPARK_PATH=source/pyspark/hdfs_to_hdfs.py
