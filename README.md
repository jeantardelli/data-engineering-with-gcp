[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

# data-engineering-with-gcp
This repo contains code for the exercises and practical examples from the book Data Engineering with Google Cloud Platform. Besides the exercises in the book, this repo contains code that launches the GCP services necessary for each DE tasks (read each directory README.md file to launch these services properly).

# Structure

This repo contains the following directories:

- [simple-data-engineer-pipeline](./simple-data-engineer-pipeline): data doesn't stay in one place, usually, it moves from one place to another (data life cycle). This repo contains one diagram example illustrating this.
- [basic-python-etl-examples](./basic-python-etl-examples): the power of a data warehouse is delivered when organizations combine multiple sources
of information into a single place. This repo contains Python sample codes that performs ETL and loads data into BigQuery.
- [orchestration-with-cloud-composer-and-airflow](./orchestration-with-cloud-composer-and-airflow): Cloud Composer is an Airflow-managed service in GCP. This directory contains the DAGs that orchestrate jobs/tasks and load data to BigQuery.
- [data-lake-with-dataproc](./data-lake-with-dataproc): A data lake is a concept similar to a data warehouse, but the key difference is what you
store in it. This directory contains sample codes that process data using HDFS, PySpark, Hive and GCP.
- [processing-streaming-data-with-pubsub-and-dataproc](./processing-streaming-data-with-pubsub-and-dataproc): Processing streaming data is becoming increasingly popular. This directory contains sample codes for streaming data as well as how to apply transformations to it using Cloud Dataflow and how to analyze it in BigQuery.
