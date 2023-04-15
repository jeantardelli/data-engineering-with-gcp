"""
This module provides functionality to train and predict using a RandomForestClassifier
on a credit card default dataset loaded from BigQuery. The model predicts whether a
customer will default on their payment in the next month.

The module reads environment variables for the project ID, dataset table ID, target
column, and model name. It contains functions to load data from BigQuery, train the
model, perform batch predictions, and perform online predictions.

Main functions:
    - load_data_from_bigquery: Load data from BigQuery table and return it as a pandas DataFrame.
    - train_model: Train a RandomForestClassifier model on the given dataset.
    - predict_batch: Predict a batch of data using the trained model.
    - predict_online: Predict online using the trained model.
"""

import os
import json
import joblib
import pandas as pd
from google.cloud import bigquery
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Read environment variables
GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
BIGQUERY_DATASET_NAME = os.environ["BIGQUERY_DATASET_NAME"]
BIGQUERY_TABLE_NAME = os.environ["BIGQUERY_TABLE_NAME"]
BIGQUERY_TABLE_ID = ".".join(
    [GCP_PROJECT_ID, BIGQUERY_DATASET_NAME, BIGQUERY_TABLE_NAME]
)
BIGQUERY_TABLE_TARGET_COLUMN = os.environ["BIGQUERY_TABLE_TARGET_COLUMN"]
MODEL_NAME = os.environ["MODEL_NAME"]


def load_data_from_bigquery(bigquery_table_id, bigquery_table_target_column):
    """
    Load data from BigQuery table and return it as a pandas DataFrame.

    Args:
        bigquery_table_id (str): The BigQuery dataset table ID.
        bigquery_table_target_column (str): The target column name in the BigQuery
            dataset table.

    Returns:
        pd.DataFrame: The loaded dataset in pandas DataFrame format.
    """
    client = bigquery.Client()
    sql = f"""SELECT 
            limit_balance, 
            education_level, 
            age, 
            {bigquery_table_target_column} 
            FROM `{bigquery_table_id}`"""

    dataframe = client.query(sql).result().to_dataframe()

    print("This is our training table from BigQuery")
    print(dataframe.head(5))

    return dataframe


def train_model(dataframe, bigquery_table_target_column, model_name):
    """
    Train a RandomForestClassifier model on the given dataset.

    Args:
        dataframe (pd.DataFrame): The input dataset in pandas DataFrame format.
        bigquery_table_target_column (str): The target column name in the BigQuery
            dataset table.
        model_name (str): The name of the file to save the trained model.

    Returns:
        RandomForestClassifier: The trained RandomForestClassifier model.
    """
    labels = dataframe[bigquery_table_target_column]
    features = dataframe.drop(bigquery_table_target_column, axis=1)

    print(f"Features : {features.head(5)}")
    print(f"Labels : {labels.head(5)}")

    x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.3)

    random_forest_classifier = RandomForestClassifier(n_estimators=100)
    random_forest_classifier.fit(x_train, y_train)

    y_pred = random_forest_classifier.predict(x_test)
    print(f"Simulate Prediction : {y_pred[:3]}")

    print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

    joblib.dump(random_forest_classifier, model_name)

    return random_forest_classifier


def predict_batch(bigquery_table_id, model_name):
    """
    Predict a batch of data using the trained model.

    Args:
        bigquery_table_id (str): The BigQuery dataset table ID.
        model_name (str): The name of the file containing the trained model.
    """
    loaded_model = joblib.load(model_name)

    client = bigquery.Client()
    sql = f"""SELECT 
                limit_balance, 
                education_level, 
                age 
                FROM `{bigquery_table_id}` 
                LIMIT 10;"""

    dataframe = client.query(sql).result().to_dataframe()

    prediction = loaded_model.predict(dataframe)
    print(f"Batch Prediction : {prediction}")


def predict_online(feature_json, model_name):
    """
    Predict online using the trained model.

    Args:
        feature_json (str): The features as a JSON string.
        model_name (str): The name of the file containing the trained model.
    """
    loaded_model = joblib.load(model_name)

    feature_list = json.loads(feature_json)
    feature_df = pd.DataFrame(feature_list)

    prediction = loaded_model.predict(feature_df)
    print("Online Prediction :")
    print(prediction)


# Load data from BigQuery public dataset to Pandas
data_in_pandas = load_data_from_bigquery(
    BIGQUERY_TABLE_ID, BIGQUERY_TABLE_TARGET_COLUMN
)

# Train ML model using RandomForest
random_forest_classifier = train_model(
    data_in_pandas, BIGQUERY_TABLE_TARGET_COLUMN, MODEL_NAME
)

# Predict Batch
# In practice, use a different table without target column for predictions.
predict_batch(BIGQUERY_TABLE_ID, MODEL_NAME)

# Predict Online
limit_balance = 1000
education_level = 1
age = 25
feature_json = json.dumps([[limit_balance, education_level, age]])
predict_online(feature_json, MODEL_NAME)
