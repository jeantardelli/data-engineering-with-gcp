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
