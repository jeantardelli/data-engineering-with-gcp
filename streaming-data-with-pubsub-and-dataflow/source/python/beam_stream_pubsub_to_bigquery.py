import json
import logging
import argparse
import os

import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions


def run(beam_options, table_id, subscription_id):
    """
    Runs the Beam pipeline.

    Reads data from Pub/Sub, decodes the data, parses it as JSON and writes the data to a BigQuery table.
    """
    with beam.Pipeline(options=beam_options) as p:
        (
            p
            | "Read from Pub/Sub"
            >> beam.io.ReadFromPubSub(subscription=subscription_id)
            | "Decode" >> beam.Map(lambda x: x.decode("utf-8"))
            | "Parse JSON" >> beam.Map(json.loads)
            | "Write to Table"
            >> beam.io.WriteToBigQuery(
                table_id,
                schema="trip_id:STRING,start_date:TIMESTAMP,start_station_id:STRING,bike_number:STRING,duration_sec:INTEGER",
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            )
        )


if __name__ == "__main__":
    """
    The main function of the script.

    Parses command line arguments, sets up logging, and runs the pipeline.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--table-id", required=True, help="BigQuery table ID")
    parser.add_argument(
        "--subscription-id", required=True, help="Pub/Sub subscription ID"
    )
    args, beam_args = parser.parse_known_args()
    beam_options = PipelineOptions(beam_args, streaming=True)

    logging.getLogger().setLevel(logging.INFO)
    run(beam_options, args.table_id, args.subscription_id)
