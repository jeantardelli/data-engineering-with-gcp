#!/bin/bash

LOCATION=$1
PROJECT=$2
DATASET_NAME=$3
METADATA_SCHEMA_URI=$4
BIGQUERY_URI=$5
TABLE_NAME=$6

cat <<EOT > request.json
{
  "display_name": "${DATASET_NAME}_${TABLE_NAME}",
  "metadata_schema_uri": "${METADATA_SCHEMA_URI}",
  "metadata": {
    "input_config": {
      "bigquery_source": {
        "uri": "${BIGQUERY_URI}"
      }
    }
  }
}
EOT

curl -X POST \
    -H "Authorization: Bearer $(gcloud auth print-access-token)" \
    -H "Content-Type: application/json; charset=utf-8" \
    -d @request.json \
    "https://${LOCATION}-aiplatform.googleapis.com/v1/projects/${PROJECT}/locations/${LOCATION}/datasets"

rm request.json
