python-install:
	pip install --upgrade pip && pip install -r requirements.txt

python-lint:
	python -m pylint ./scripts/*.py

python-black:
	python -m black ./scripts/*.py

bigquery-copy-public-dataset:
	@echo "Copying credit_card_default table from BigQuery public data to the new dataset"
	bq --project_id=${GCP_PROJECT_ID} mk --force --dataset ${BIGQUERY_DATASET_NAME}
	bq --project_id=${GCP_PROJECT_ID} cp bigquery-public-data:${BIGQUERY_DATASET_NAME}.${BIGQUERY_TABLE_NAME} ${BIGQUERY_TABLE_ID}

gcs-create-bucket:
	@if ! gsutil ls -b gs://${GCS_BUCKET_NAME} 2>/dev/null; then \
		echo "Creating bucket: ${GCS_BUCKET_NAME}"; \
		gsutil mb gs://${GCS_BUCKET_NAME}; \
	else \
		echo "Bucket ${GCS_BUCKET_NAME} already exists"; \
	fi

gcs-upload-files:
	@echo "Uploading files from ${GCS_SOURCE_PATH} to gs://${GCS_BUCKET_NAME}/${GCS_DEST_PATH}"
	gsutil -m cp -r ${GCS_SOURCE_PATH} gs://${GCS_BUCKET_NAME}/${GCS_DEST_PATH}
	@echo "Upload complete"

gcs-delete-bucket:
	@if gsutil ls -b gs://${GCS_BUCKET_NAME} 2>/dev/null; then \
		echo "Deleting bucket: ${GCS_BUCKET_NAME}"; \
		gsutil -m rm -r gs://${GCS_BUCKET_NAME}; \
	else \
		echo "Bucket ${GCS_BUCKET_NAME} does not exist"; \
	fi

vertex-ai-create-dataset:
	@bash scripts/create_vertex_ai_dataset.sh ${VERTEX_AI_REGION} \
		${GCP_PROJECT_ID} \
		${BIGQUERY_DATASET_NAME} \
		gs://google-cloud-aiplatform/schema/dataset/metadata/tabular_1.0.0.yaml \
		bq://bigquery-public-data.${BIGQUERY_DATASET_NAME}.${BIGQUERY_TABLE_NAME} \
		${BIGQUERY_TABLE_NAME}

vertex-ai-train-model:
	@echo "Training a model using Vertex AI AutoML"
	python ./scripts/train_automl.py --project_id ${GCP_PROJECT_ID} \
		--region ${VERTEX_AI_REGION} \
		--dataset_id ${BIGQUERY_DATASET_NAME}_${BIGQUERY_TABLE_NAME} \
		--target_column ${BIGQUERY_TABLE_TARGET_COLUMN} \
		--train_budget ${VERTEX_AI_TRAIN_MILI_BUDGET_HOURS}
	@echo "Model training complete"

gcs-all: gcs-create-bucket gcs-upload-files

vertex-ai-all: vertex-ai-create-dataset vertex-ai-train-model
