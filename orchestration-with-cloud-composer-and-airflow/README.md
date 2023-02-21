This directory contains code that builds orchestration batch data loading using Cloud Composer.

To run the code it is necessary to create a Cloud Composer environment. To create a Cloud Composer environment please run the following:

```bash
bash ./scripts/set-environment-variables.sh
make create-environment
```

Some examples read data from Cloud SQL. For this to run it is necessary to do the following:

1. Create a Cloud SQL instance
2. Configure the Cloud SQL service account identity and access management (IAM) permission as `GCS Object Admin`.
3. Create a stations table from the MySQL console.
4. Import the stations table data from a comma-separated values (CSV) file


## Parameterized DAG

Following is the parameterized DAG diagram:

![imagen](https://user-images.githubusercontent.com/42701946/220198968-f55a5b73-6e3c-4368-b0d2-ad3835bbc431.png)
