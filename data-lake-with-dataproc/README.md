# Data Lake Using Dataproc

A data lake is a concept similar to a data warehouse, but the key difference is what you
store in it. A data lake's role is to store as much raw data as possible without knowing first
what the value or end goal of the data is.

This repo uses the following GCP services:

- GCS
- Dataproc

To set up everyting, just run the following:

```bash
source scripts/environment_variables.sh
make all
```

To submit a PySpark Job that loads data from HDFS to HDFS, run: `make dataproc-submit-pyspark-job`.
If you want to submit a PySpark Job directly to BigQuery, the: `make dataproc-submit-pyspark-job-to-bigquery`.

Note: to add a new script into GCS it is necessary to run `make gcs-upload-file`
