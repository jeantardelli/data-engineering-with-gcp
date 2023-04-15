"""
This module detects text in an image stored in Google Cloud Storage
using Google Cloud Vision API, and then detects the language of the text
using Google Cloud Translate API.
"""

import os
from google.cloud import vision
from google.cloud import translate_v2 as translate

GCS_BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME")
GCS_DEST_PATH = os.environ.get("GCS_DEST_PATH")
GCS_URI = f"gs://{GCS_BUCKET_NAME}/{GCS_DEST_PATH}"


def detect_text(gcs_uri):
    """
    Detects text in an image stored in Google Cloud Storage using
    Google Cloud Vision API, and then detects the language of the
    text using Google Cloud Translate API.

    Args:
        GCS_URI (str): The Google Cloud Storage URI of the image to be processed.

    Returns:
        None
    """
    print(f"Looking for text from image in GCS: {GCS_URI}")

    image = vision.Image(source=vision.ImageSource(gcs_image_uri=gcs_uri))

    text_detection_response = vision_client.text_detection(image=image)
    annotations = text_detection_response.text_annotations
    if len(annotations) > 0:
        text = annotations[0].description
    else:
        text = ""
    print(f"Extracted text : \n{text}")

    detect_language_response = translate_client.detect_language(text)
    src_lang = detect_language_response["language"]
    print(f"Detected language {src_lang}")


vision_client = vision.ImageAnnotatorClient()
translate_client = translate.Client()
detect_text(GCS_URI)
