import apache_beam as beam
import argparse
import json
import logging

from apache_beam.options.pipeline_options import PipelineOptions


class BuildRecordFn(beam.DoFn):
    """A DoFn to build records with the window end timestamp added.

    Args:
        beam.DoFn: The base class for creating a DoFn.
    """

    def process(self, element, window=beam.DoFn.WindowParam):
        """
        Process function to add the window end timestamp to the input element.

        Args:
            element (Tuple): A single element read from the input source.
            window (window object): The window object to extract the window start timestamp from.

        Returns:
            List: A list with the processed element including the window end timestamp.
        """
        window_start = window.start.to_utc_datetime().isoformat()
        return [element + (window_start,)]


def run(subscription_id: str, table_id: str, beam_options: PipelineOptions):
    """
    Runs the Apache Beam pipeline.

    Args:
        subscription_id (str): The subscription to read messages from.
        table_id (str): The destination table to write the results to.
        beam_options (PipelineOptions): The pipeline options to use for the pipeline execution.
    """
    with beam.Pipeline(options=beam_options) as p:
        (
            p
            | "Read from Pub/Sub"
            >> beam.io.ReadFromPubSub(subscription=subscription_id)
            | "Decode" >> beam.Map(lambda x: x.decode("utf-8"))
            | "Parse JSON" >> beam.Map(json.loads)
            | "UseFixedWindow" >> beam.WindowInto(beam.window.FixedWindows(60))
            | "Group By Station ID"
            >> beam.Map(lambda elem: (elem["start_station_id"], elem["duration_sec"]))
            | "Sum" >> beam.CombinePerKey(sum)
            | "AddWindowEndTimestamp" >> (beam.ParDo(BuildRecordFn()))
            | "Parse to JSON"
            >> beam.Map(
                lambda x: {
                    "start_station_id": x[0],
                    "sum_duration_sec": x[1],
                    "window_timestamp": x[2],
                }
            )
            | "Write to Table"
            >> beam.io.WriteToBigQuery(
                table_id,
                schema="start_station_id:STRING,sum_duration_sec:INTEGER,window_timestamp:TIMESTAMP",
                create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
            )
        )


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument("--subscription-id", dest="subscription_id", required=True)
    parser.add_argument("--table-id", dest="table_id", required=True)
    args, beam_args = parser.parse_known_args()
    beam_options = PipelineOptions(beam_args, streaming=True)
    run(args.subscription_id, args.table_id, beam_options)
