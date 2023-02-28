#!/bin/bash

CLOUD_SQL_SERVICE_ACCOUNT=$(gcloud sql instances describe ${CLOUD_SQL_INSTANCE_NAME} --project=${GCP_PROJECT_ID} --format="value(serviceAccountEmailAddress)")
gsutil iam ch serviceAccount:${CLOUD_SQL_SERVICE_ACCOUNT}:objectAdmin gs://${GCS_BUCKET_NAME}
