# Processing Streaming Data with Pub/Sub and Dataflow

Processing streaming data is becoming increasingly popular, as streaming enables
businesses to get real-time metrics on business operations. This repo contains code
for streaming data, how to apply transformations to streaming data using Cloud Dataflow,
and how to store processed records in BigQuery for analysis.

## GCP Services

This repo uses the following GCP products:

- [Dataflow](https://cloud.google.com/dataflow)
- [GCS](https://cloud.google.com/storage)
- [Pub/Sub](https://cloud.google.com/pubsub)
- [BigQuery](https://cloud.google.com/bigquery)

Make sure to enable the application programming interface (API) for these products.

## Creating a Dataflow streaming job without aggregation

To run this streaming pipeline execute the following steps:

1. `source ./scripts/environment_variables.sh`
2. `make all-pubsub-stream`
3. `make dataflow-stream-local-runner`

Make sure to create the BigQuery table and that the `table_id` match the one defined on the env var.
