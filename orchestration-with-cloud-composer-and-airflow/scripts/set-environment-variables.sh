#!/bin/bash

export IMAGE_VERSION=composer-1.16.6-airflow-1.10.15
export NODE_COUNT=3
export DISK_SIZE=20
export LOCATION=us-central1
export ENVIRONMENT_NAME=composer-dev
export MACHINE_TYPE=n1-standard-1
export PYTHON_VERSION=3

export GCS_BUCKET=composer-dev
export INSTANCE_NAME=instance-dev
export GCP_PROJECT_ID=cicd-data-engineer-pipelines

export MYSQL_INSTANCE_NAME=instance-dev
