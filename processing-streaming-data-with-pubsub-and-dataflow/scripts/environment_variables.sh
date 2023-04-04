#!/bin/bash

export GCP_PROJECT_ID=$(gcloud config get-value project)
export PUBSUB_TOPIC_ID=bike-sharing-trips
export PUBSUB_SUBSCRIPTION_ID=bike-sharing-trips-subs-1
export PUBSUB_SUBSCRIPTION_EXPIRATION_PERIOD=1d
export PUBSUB_SUBSCRIPTION_MESSAGE_RETENTION_DURATION=10m
