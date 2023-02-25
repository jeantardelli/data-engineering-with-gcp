"""Simple Python script that loads a CSV file in GCS into BigQuery table."""
import argparse
from google.cloud import bigquery

# Defines the table schema
# TODO: This can be refactored to accept a json file or be
# loaded from other module
TABLE_SCHEMA = [
    bigquery.SchemaField("station_id", "STRING"),
    bigquery.SchemaField("name", "STRING"),
    bigquery.SchemaField("region_id", "STRING"),
    bigquery.SchemaField("capacity", "INTEGER"),
]

# Construct a BigQuery client object.
client = bigquery.Client()


def load_gcs_csv_file_to_bigquery(dataset_name, table_id, uri):
    """
    Loads a CSV file on GCS to a BigQuery table as a batch operation.

    Args:
        dataset_name: String
        table_id: String
        uri: String
    """
    # Set dataset_id to the ID of the dataset to create.
    dataset_id = f"{client.project}.{dataset_name}"

    # Set table_id to the ID of the table to create.
    table_id = f"{dataset_id}.{table_id}"

    # Rely on BigQuery schema auto-detection
    job_config = bigquery.LoadJobConfig(
        schema=TABLE_SCHEMA,
        write_disposition="WRITE_TRUNCATE",
        source_format=bigquery.SourceFormat.CSV,
    )

    try:
        load_job = client.load_table_from_uri(uri, table_id, job_config=job_config)
    except Exception as err:
        print(f"Failed to load file into {table_id}!")
        print(err)

    load_job.result()  # Waits for the job to complete.
    destination_table = client.get_table(table_id)  # Make an API request.
    print(f"Loaded {destination_table.num_rows} rows to {table_id}!.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="BigQuery GCS CSV file loader script. Expects a schema config.",
        description="This script loads a GCS CSV file into BigQuery.",
    )
    parser.add_argument(
        "-d", "--dataset", type=str, help="The dataset name", required=True
    )
    parser.add_argument("-t", "--table", type=str, help="The table name", required=True)
    parser.add_argument("-u", "--uri", type=str, help="The GCS uri", required=True)

    args = parser.parse_args()

    load_gcs_csv_file_to_bigquery(args.dataset, args.table, args.uri)
