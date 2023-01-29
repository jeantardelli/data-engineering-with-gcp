"""Simple Python script that creates new tabels into BigQuery using sql."""
import argparse
from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()


def create_a_table_in_bigquery_using_sql(
    dataset_name, table_id, sql_filepath, load_date=None,
    write_mode="WRITE_TRUNCATE"
):
    """
    Creates a new table in BigQuery using sql.

    Args:
        dataset_name: String
        table_id: String
        sql_filepath: String
        load_date: String
        write_mode: String
    """
    # Set dataset_id to the ID of the dataset to create.
    dataset_id = f"{client.project}.{dataset_name}"

    # Set table_id to the ID of the table to create.
    table_id = f"{dataset_id}.{table_id}"

    # reads sql from a file
    with open(sql_filepath, "r") as sql:
        sql = sql.read()

    if load_date is None:
        sql = sql.format(project_id=client.project)
    else:
        sql = sql.format(project_id=client.project, load_date=load_date)

    # Rely on BigQuery schema auto-detection
    job_config = bigquery.QueryJobConfig(
        destination=table_id, write_disposition=write_mode
    )

    query_job = client.query(sql, job_config=job_config)

    try:
        print(sql)
        query_job = query_job.result()
        print("Query executed gracefully!")
    except Exception as err:
        print(f"Failed to execute the query!")
        print(err)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="BigQuery table creator reading a sql command.",
        description="Creates a new BigQuery table given a SQL command.",
    )
    parser.add_argument(
        "-d", "--dataset", type=str, help="The dataset name", required=True
    )
    parser.add_argument("-t", "--table", type=str, help="The table name", required=True)
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="The query command",
        required=True,
    )
    parser.add_argument(
        "-ld",
        "--load-date",
        type=str,
        help="Load date (for granularity)",
        required=False,
    )
    parser.add_argument(
        "-w",
        "--write-mode",
        type=str,
        help="Write mode",
        required=False,
    )


    args = parser.parse_args()

    create_a_table_in_bigquery_using_sql(
        args.dataset, args.table, args.query, args.load_date, args.write_mode
    )
