#!/bin/bash

export GCP_PROJECT_ID=$(gcloud config get-value project)
export PUBSUB_TOPIC_ID=bike-sharing-trips
export PUBSUB_SUBSCRIPTION_ID=bike-sharing-trips-subs-1
export PUBSUB_SUBSCRIPTION_EXPIRATION_PERIOD=1d
export PUBSUB_SUBSCRIPTION_MESSAGE_RETENTION_DURATION=10m

# GCS variables
export GCS_BUCKET_NAME=streaming-dev-${GCP_PROJECT_ID}
export GCS_BUCKET_LOCATION=us-central1
export GCS_DATA_SOURCE_PATH=./source/

# Beam variables
export BEAM_REGION=us-central1
export BEAM_PYTHON_FILE=./source/python/beam_gcs_to_gcs.py

# BigQuery variables
export BIGQUERY_TABLE_ID=${GCP_PROJECT_ID}:raw_bikesharing.bike_trips_streaming
