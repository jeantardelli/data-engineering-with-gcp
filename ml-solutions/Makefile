python-install:
	pip install --upgrade pip && pip install -r requirements.txt

python-lint:
	python -m pylint ./scripts/*.py

python-black:
	python -m black ./scripts/*.py

.PHONY: bigquery-copy-public-dataset
bigquery-copy-public-dataset:
	@echo "Copying credit_card_default table from BigQuery public data to the new dataset"
	bq --project_id=${GCP_PROJECT_ID} mk --force --dataset ${BIGQUERY_DATASET_NAME}
	bq --project_id=${GCP_PROJECT_ID} cp bigquery-public-data:${BIGQUERY_DATASET_NAME}.${BIGQUERY_TABLE_NAME} ${BIGQUERY_TABLE_ID}
