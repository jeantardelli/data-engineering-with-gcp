# Building a Data Warehouse

## Scenario 1 | Load data from a App database

### Step 1 | Create MySQL Database

For this exercise, a [Cloud SQL](https://cloud.google.com/sql/docs/mysql) will be used to simulate data extraction from a application database. To create this environment just run the `cloudbuild-databases.yaml`. It consists of the following steps:

1. Create a CloudSQL instance.
2. Create a MySQL database.

Then it is necessary to connect to the Cloud SQL MySQL instance and manually create the table. After that, imports CSV data into the MySQL database. 

![imagen](https://user-images.githubusercontent.com/42701946/215279632-2972dc3e-7eda-4195-89ff-b89a8795a941.png)

### Step 2 | Extract data from MySQL to GCS

In the CloudSQL instance panel import a CSV into the created table. Just go to the Import tab and follow the steps.

Then give access to the `gcp-sa-cloud-sql.iam.gserviceaccount.com` through the IAM & Admin. This is necessary because CloudSQL service must have acces to the GCS Bucket to load data. 

Finally, run the `export-data-from-cloudsql-to-gcs.sh` script.

In a real-world scenario, most of the time, the extractions happen from the clone instance. Application databases usually have a clone instance for providing high availability. Hence,
it's good to extract data from there. That way, there is no interruptions in the production database.

Though manually, this is an example of the E in ETL, which is to extract data from a data source into a GCS bucket. 

![imagen](https://user-images.githubusercontent.com/42701946/215282134-d99b689b-15c5-417e-aa20-d000653473c9.png)

### Step 3 | Load GCS to BigQuery

In this step just creates a table importing the CSV from the GCS. For this, just create a new dataset and a new table that loads that from GSC. 

![imagen](https://user-images.githubusercontent.com/42701946/215282664-365c6088-6281-45c0-afcb-13a639148180.png)

### Step 4 | Create a BigQuery data mart

Depending on company regulations, most companies don't allow business users to access raw tables directly. Business users usually access data from data marts. Technically, we can use BigQuery as a data mart.

1. Create a new dataset `dm_regional_manager` and create the following view:

```sql
CREATE VIEW `cicd-data-engineer-pipelines.dm_regional_manager.top_2_region_by_capacity` AS

/* As a business user, I want to know the top two region IDs, ordered by the total stations'
capacity in that region. */

SELECT region_id,
       SUM(capacity) AS total_capacity
  FROM `cicd-data-engineer-pipelines.raw_bikesharing.stations`
 WHERE region_id != ''
 GROUP BY region_id
 ORDER BY total_capacity DESC
 LIMIT 2;
```

![imagen](https://user-images.githubusercontent.com/42701946/215283565-05fdc1b2-7fe7-4042-a7e0-502ba3c78649.png)

Done! We've practiced running an end-to-end ELT process on GCP. We extracted data from MySQL into a GCS bucket, loaded it into BigQuery, and transformed the table into a data mart table.

## Scenario 2 Loading more tables

Create more datasets running `sh scripts/create-multiple-datasets.sh`
To load the necessary data run the following scripts:

- `sh_scripts/loading_gcs_csg_file_into_bigquery.py` (only the last day)
- `sh scripts/loading_gcs_json_file_into_bigquery.py` (run one for each GCS trips/ day)
- `sh_scripts/loading_public_datasets_into_bigquery.py`

If you dataset is in another region from US, the only way to copy a public dataset is to setup a data transfer. The feature is free, but you will pay inter-region traffic from asia to us to transfer your data. And because you replicate the data, you will also pay the storage.

Run the following query to check for duplications:


```sql
SELECT COUNT(*) cnt_trip_id,
       trip_id
  FROM `cicd-data-engineer-pipelines.raw_bikesharing.trips`
 GROUP BY trip_id
HAVING cnt_trip_id > 1
```

Verify both days loaded correctly:

```sql
ELECT DISTINCT DATE(start_date)
  FROM `cicd-data-engineer-pipelines.raw_bikesharing.trips`
```

Check there is no dups in stations tabel:

```sql
SELECT station_id, COUNT(*) as cnt_station
  FROM `cicd-data-engineer-pipelines.raw_bikesharing.stations`
 GROUP BY station_id
HAVING cnt_station > 1;
```
The tables should have this number of records:

- Regions: 6 records
- Stations: 342 records
- Trips: 4,627 records
