"""
This module contains a Beam pipeline that reads a text file, splits the records
into fields, extracts the URLs, and writes the results to a text file.

Example usage:

    $ python my_module.py --bucket-name=my_bucket --input-file=my_input_file.txt

"""
import logging
import argparse
import apache_beam as beam

from apache_beam.transforms.combiners import Sample
from apache_beam.options.pipeline_options import PipelineOptions

parser = argparse.ArgumentParser()
args, beam_args = parser.parse_known_args()
beam_options = PipelineOptions(beam_args)


class Split(beam.DoFn):
    """
    A DoFn that splits a text element into a dictionary of fields.
    """
    def process(self, element):
        """
        Splits a text element into a dictionary of fields.

        Args:
            element (str): A text element.

        Returns:
            list: A list containing a dictionary of fields.
        """
        rows = element.split(" ")
        return [
            {
                "ip": str(rows[0]),
                "date": str(rows[3]),
                "method": str(rows[5]),
                "url": str(rows[6]),
            }
        ]


def split_map(records):
    """
    A function that splits a text record into a dictionary of fields.

    Args:
        records (str): A text record.

    Returns:
        dict: A dictionary of fields.
    """
    rows = records.split(" ")
    return {
        "ip": str(rows[0]),
        "date": str(rows[3]),
        "method": str(rows[5]),
        "url": str(rows[6]),
    }

def run(bucket_name:str, input_file:str, beam_args:list):
    """
    Runs the Beam pipeline.

    Args:
        bucket_name (str): The name of the GCS bucket where the input and output files reside.
        input_file (str): The path to the input file within the bucket.
        beam_args (list): A list of command-line arguments for Apache Beam.

    Returns:
        None
    """
    INPUT_FILE = f"gs://{bucket_name}/{input_file}"
    OUTPUT_PATH = f"gs://{bucket_name}/dataflow/output/output_file_"

    beam_options = PipelineOptions(beam_args)

    with beam.Pipeline(options=beam_options) as p: (
            p
            | "Read" >> beam.io.textio.ReadFromText(INPUT_FILE)
            | "Split" >> beam.ParDo(Split())
            | "Get URL" >> beam.Map(lambda s: (s["url"], 1))
            | "Sample" >> Sample.FixedSizeGlobally(19)
            | "Write" >> beam.io.textio.WriteToText(OUTPUT_PATH)
        )

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("--bucket-name", dest="bucket_name", required=True, help="Bucket name")
    parser.add_argument("--input-file", dest="input_file", required=True, help="Input file path")
    args, beam_args = parser.parse_known_args()

    run(args.bucket_name, args.input_file, beam_args)
