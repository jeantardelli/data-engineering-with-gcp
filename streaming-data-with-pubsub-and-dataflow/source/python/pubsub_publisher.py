"""
This script sends messages to a Google Cloud Pub/Sub topic.
The topic and project ID are read from environment variables.
"""
import json
import os

from random import randint
from datetime import datetime
from concurrent import futures
from google.cloud import pubsub_v1

# Load environment variables
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
PUBSUB_TOPIC_ID = os.environ.get("PUBSUB_TOPIC_ID")

# Create a Pub/Sub publisher client and topic path
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(GCP_PROJECT_ID, PUBSUB_TOPIC_ID)

# Create a list to hold the futures of the publish calls
publish_futures = []


def get_callback(publish_future, data):
    """
    Returns a callback function that is called when the message has been
    published to the Pub/Sub topic.

    Args:
        publish_future: A future object representing the result of a call
            to the publish() method of a Pub/Sub publisher.
        data: The data that was published to the Pub/Sub topic.

    Returns:
        A callback function that prints the result of the publish call or
        a timeout message if the call timed out.
    """

    def callback(publish_future):
        try:
            # Wait 60 seconds for the publish call to succeed.
            print(publish_future.result(timeout=60))
        except futures.TimeoutError:
            print(f"Publishing {data} timed out.")

    return callback


def create_random_message():
    """
    Returns a JSON object representing a random bike-sharing trip.

    Returns:
        A JSON object representing a random bike-sharing trip, with the following fields:
        - trip_id: a random integer between 10000 and 99999
        - start_date: the current UTC datetime in string format
        - start_station_id: a random integer between 200 and 205
        - bike_number: a random integer between 100 and 999
        - duration_sec: a random integer between 1000 and 9999
    """
    trip_id = randint(10000, 99999)
    start_date = str(datetime.utcnow())
    start_station_id = randint(200, 205)
    bike_number = randint(100, 999)
    duration_sec = randint(1000, 9999)

    message_json = {
        "trip_id": trip_id,
        "start_date": start_date,
        "start_station_id": start_station_id,
        "bike_number": bike_number,
        "duration_sec": duration_sec,
    }
    return message_json


if __name__ == "__main__":
    # Publish 10 random bike-sharing trips to the Pub/Sub topic
    for i in range(10):
        message_json = create_random_message()
        data = json.dumps(message_json)

        # Publish the message and add a callback function to print the result
        publish_future = publisher.publish(topic_path, data.encode("utf-8"))
        publish_future.add_done_callback(get_callback(publish_future, data))
        publish_futures.append(publish_future)

    # Wait for all the publish futures to resolve before exiting
    futures.wait(publish_futures, return_when=futures.ALL_COMPLETED)

    # Print a message indicating that the messages have been published
    print(f"Published messages with error handler to {topic_path}.")
