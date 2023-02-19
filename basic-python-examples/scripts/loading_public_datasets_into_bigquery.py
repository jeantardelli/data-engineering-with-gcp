"""Simple Python script that loads a BiQuery public dataset
into a BigQuery table."""
import argparse
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()


def load_a_public_dataset_to_bigquery(target_dataset, target_table_id, public_table_id):
    """
    Loads a public available table id into a target BigQuery table.

    Args:
        target_dataset: String
        target_table_id: String
        public_table_id: String
    """
    # Set dataset_id to the ID of the dataset to create.
    dataset_id = f"{client.project}.{target_dataset}"

    # Set table_id to the ID of the table to create.
    table_id = f"{dataset_id}.{target_table_id}"

    # Rely on BigQuery schema auto-detection
    job_config = bigquery.QueryJobConfig(
        destination=table_id, write_disposition="WRITE_TRUNCATE"
    )

    sql = f"SELECT * FROM `{public_table_id}`;"
    query_job = client.query(sql, job_config=job_config)

    try:
        query_job = query_job.result()
        print("Query executed gracefully!")
    except Exception as err:
        print(f"Failed to execute the query!")
        print(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="BigQuery load data from a public dataset.",
        description="This script queries a public dataset \
                and loads to a table in BigQuery.",
    )
    parser.add_argument(
        "-d", "--dataset", type=str, help="The target dataset name", required=True
    )
    parser.add_argument(
        "-t", "--table", type=str, help="The target table name", required=True
    )
    parser.add_argument(
        "-p",
        "--public",
        type=str,
        help="The public dataset to be queried",
        required=True,
    )

    args = parser.parse_args()

    load_a_public_dataset_to_bigquery(args.dataset, args.table, args.public)
