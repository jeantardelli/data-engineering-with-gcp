import argparse
from google.cloud import aiplatform

def get_dataset_id_by_display_name(project_id, region, display_name):
    """
    Retrieve the dataset ID using its display name.

    Args:
        project_id (str): Google Cloud Project ID.
        region (str): Vertex AI region.
        display_name (str): The display name of the dataset.

    Returns:
        str: The resource name (ID) of the dataset with the given display name.

    Raises:
        ValueError: If no dataset is found with the given display name.
    """
    aiplatform.init(project=project_id, location=region)
    filter_string = f'display_name="{display_name}"'
    datasets = aiplatform.TabularDataset.list(filter=filter_string)

    if len(datasets) == 0:
        raise ValueError(f"No dataset found with display_name: {display_name}")

    return datasets[0].resource_name.split("/")[-1]

def train_automl_model(
    project_id, region, dataset_name, target_column, train_budget_milli_node_hours
):
    """
    Train an AutoML model using Vertex AI Python SDK.

    Args:
        project_id (str): Google Cloud Project ID.
        region (str): Vertex AI region.
        dataset_name (str): Vertex AI Dataset name.
        target_column (str): Target column for the training.
        train_budget_milli_node_hours (int): Training budget for AutoML in milli-node-hours.
    """
    # Initialize Vertex AI SDK client
    aiplatform.init(project=project_id, location=region)

    # Get the dataset ID by its display name
    dataset_id = get_dataset_id_by_display_name(project_id, region, dataset_name)

    # Prepare model training configuration
    model_training_config = {
        "train_budget_milli_node_hours": train_budget_milli_node_hours,
        "disable_early_stopping": False,
        "optimization_objective": "maximize-au-prc",
        "target_column": target_column,
        "input_feature_column_transformation": [
            {"auto": {"column_name": "age"}},
            {"auto": {"column_name": "education_level"}},
            {"auto": {"column_name": "limit_balance"}},
        ],
    }

    # Set the model display name
    model_display_name = "automl_model"

    # Create a dataset object
    dataset = aiplatform.TabularDataset(dataset_id)

    # Create a training job
    training_job = aiplatform.AutoMLTabularTrainingJob(
        display_name=model_display_name,
        optimization_prediction_type="classification",
        column_transformations=model_training_config[
            "input_feature_column_transformation"
        ],
    )

    # Run the training job
    response = training_job.run(
        dataset=dataset,
        target_column=target_column,
        training_fraction_split=0.7,
        validation_fraction_split=0.2,
        test_fraction_split=0.1,
        weight_column=None,
        budget_milli_node_hours=train_budget_milli_node_hours,
        disable_early_stopping=False,
    )

    print(f"Model training has started: {response.operation.name}")
    response.result()  # Wait for the operation to complete
    print("Model training has completed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train an AutoML model using Vertex AI Python SDK."
    )
    parser.add_argument("--project_id", required=True, help="Google Cloud Project ID.")
    parser.add_argument("--region", required=True, help="Vertex AI region.")
    parser.add_argument("--dataset_name", required=True, help="Vertex AI Dataset name.")
    parser.add_argument(
        "--target_column", required=True, help="Target column for the training."
    )
    parser.add_argument(
        "--train_budget",
        required=True,
        type=int,
        help="The training budget for the model in milli node hours.",
    )
    args = parser.parse_args()

    train_automl_model(
        args.project_id,
        args.region,
        args.dataset_name,
        args.target_column,
        args.train_budget,
    )
