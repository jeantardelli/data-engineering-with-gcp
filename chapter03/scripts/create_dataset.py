"""Simple Python script that creates a BigQuery dataset."""

import argparse
from google.cloud import bigquery
from google.cloud.exceptions import NotFound


# Construct a BigQuery client object.
client = bigquery.Client()


def create_bigquery_dataset(dataset_name, dataset_location):
    """
    Create a BigQuery dataset. When we create a dataset in BigQuery, the
    dataset name must be unique for each project.

    Args:
        dataset_name: String
        dataset_location: String
    """
    # Set dataset_id to the ID of the dataset to create.
    dataset_id = f"{client.project}.{dataset_name}"

    try:
        # Verify dataset existence
        client.get_dataset(dataset_id)
        print(f"Dataset <{dataset_id}> already exists!")
    except NotFound:
        # Construct a full Dataset object to send to the API.
        dataset = bigquery.Dataset(dataset_id)
        # Specify the geographic location where the dataset should reside.
        dataset.location = dataset_location
        # Send the dataset to the API for creation, with an explicit timeout.
        # Raises google.api_core.exceptions.Conflict if the Dataset already
        # exists within the project.
        dataset = client.create_dataset(dataset, timeout=30)  # Make an API request.
        print(f"Created dataset <{client.project}.{dataset.dataset_id}>!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="BigQuery dataset creator script",
        description="This script creates a BigQuery dataset given \
                                in the name argument.",
    )
    parser.add_argument(
        "-n", "--name", type=str, help="The dataset name", required=True
    )
    parser.add_argument(
        "-l", "--location", type=str, help="The dataset location", required=True
    )

    args = parser.parse_args()

    create_bigquery_dataset(args.name, args.location)
