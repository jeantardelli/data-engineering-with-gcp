#!/bin/bash

# Cloud Composer set up variables 
export CLOUD_COMPOSER_IMAGE_VERSION=composer-1.16.6-airflow-1.10.15
export CLOUD_COMPOSER_NODE_COUNT=3
export CLOUD_COMPOSER_DISK_SIZE=30
export CLOUD_COMPOSER_LOCATION=us-central1
export CLOUD_COMPOSER_ENVIRONMENT_NAME=composer-dev
export CLOUD_COMPOSER_MACHINE_TYPE=n1-standard-1
export CLOUD_COMPOSER_PYTHON_VERSION=3

# Cloud SQL set up variables
export CLOUD_SQL_INSTANCE_NAME=mysql-instance-dev
export CLOUD_SQL_DATABASE_VERSION=MYSQL_5_7
export CLOUD_SQL_TIER=db-g1-small
export CLOUD_SQL_REGION=us-central1
export CLOUD_SQL_ROOT_PASSWORD=foo
export CLOUD_SQL_AVAILABILITY_TYPE=zonal
export CLOUD_SQL_STORAGE_SIZE=10GB
export CLOUD_SQL_STORAGE_TYPE=HDD

export CLOUD_SQL_DATABASE_NAME=apps_db
export CLOUD_SQL_TABLE_NAME=stations

export CLOUD_SQL_SERVICE_ACCOUNT=$(gcloud sql instances describe ${CLOUD_SQL_INSTANCE_NAME} --project=${GCP_PROJECT_ID} --format="value(serviceAccountEmailAddress)")
export CLOUD_SQL_IMPORT_FILE_PATH=source/stations
export CLOUD_SQL_IMPORT_FILE_NAME=stations.csv

# Project wide variables
export GCP_PROJECT_ID=$(gcloud config get-value project)

# GCS variables
export GCS_BUCKET_NAME=${GCP_PROJECT_ID}-source-data-dev
export GCS_LOCATION=us-central1
export GCS_PROJECT=${GCP_PROJECT_ID}
export GCS_DATA_SOURCE_PATH=${PWD}'/source/'
