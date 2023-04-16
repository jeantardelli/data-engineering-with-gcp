# Building Machine Learning Solutions on Google Cloud Platform

This repo contains code that uses the following GCP services:

- BigQuery
- GCS
- Vertex AI Pipelines
- Vertex AI AutoML
- Google Cloud Vision AI
- Google Cloud Translate

## Simple ML using Python

To run a simple example of ML code using Python, run:

```bash
source .env
make bigquery-copy-public-dataset
python scripts/random_forest_model_from_bigquery_table.py 
```

## Simple Cloud Vision and Tranlation Example

To run the ML example that utilizes the Cloud Vision and Translation APIs, follow these steps:

```bash
source .env
make gcs-all
python scripts/pre_built_vision_ai.py
```
