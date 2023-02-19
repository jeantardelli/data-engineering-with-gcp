"""Simple Python script that loads a CSV file into BigQuery table.
This example uses the schema auto-detection. It is a best practice to
define the schema properly though."""
import argparse
from google.cloud import bigquery


# Construct a BigQuery client object.
client = bigquery.Client()


def load_csv_file_to_bigquery(dataset_name, table_id, filepath):
    """
    Load a CSV file to a BigQuery tabler from a local file
    as a batch operation

    Args:
        dataset_name: String
        table_id: String
        filename: String
    """
    # Set dataset_id to the ID of the dataset to create.
    dataset_id = f"{client.project}.{dataset_name}"

    # Set table_id to the ID of the table to create.
    table_id = f"{dataset_id}.{table_id}"

    # Rely on BigQuery schema auto-detection
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        skip_leading_rows=1,
        # The source format defaults to CSV, so the line below is optional.
        source_format=bigquery.SourceFormat.CSV,
    )

    try:
        with open(filepath, "rb") as source_file:
            load_job = client.load_table_from_file(
                source_file, table_id, job_config=job_config
            )
    except Exception as err:
        print(f"Failed to load CSV file into {table_id}!")
        print(err)

    load_job.result()  # Waits for the job to complete.
    destination_table = client.get_table(table_id)  # Make an API request.
    print(f"Loaded {destination_table.num_rows} rows to {table_id}!.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="BigQuery local CSV loader script. It uses the schema \
                auto-detection.",
        description="This script loads a CSV into BigQuery.",
    )
    parser.add_argument(
        "-d", "--dataset", type=str, help="The dataset name", required=True
    )
    parser.add_argument("-t", "--table", type=str, help="The table name", required=True)
    parser.add_argument(
        "-f", "--filepath", type=str, help="The filepath", required=True
    )

    args = parser.parse_args()

    load_csv_file_to_bigquery(args.dataset, args.table, args.filepath)
