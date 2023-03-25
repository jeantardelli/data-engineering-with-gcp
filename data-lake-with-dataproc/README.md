# Data Lake Using Dataproc

A data lake is a concept similar to a data warehouse, but the key difference is what you
store in it. A data lake's role is to store as much raw data as possible without knowing first
what the value or end goal of the data is.

This repo uses the following GCP services:

- [GCS](https://cloud.google.com/storage)
- [Dataproc](https://cloud.google.com/dataproc)

To set up everyting, just run the following:

```bash
source scripts/environment_variables.sh
make all-dataproc
```

To submit a PySpark Job that loads data from HDFS to HDFS, run: `make dataproc-submit-pyspark-job`.
If you want to submit a PySpark Job directly to BigQuery, the: `make dataproc-submit-pyspark-job-to-bigquery`.

Note: to add a new script into GCS it is necessary to run `make gcs-upload-file`. Another thing to note is that this is an alternative to the ephemeral cluster that can be created to execute jobs by setting a [Dataproc Workflow Template](https://cloud.google.com/dataproc/docs/concepts/workflows/overview).

Another way to achive the same results and separating computation from storage in a distributed system structure is by using the Airflow to orchestrate the creation of Dataproc's ephemeral clusters. To test this, run:

```bash
make all-cloud-composer
make cloud-composer-deploy-dag
```
