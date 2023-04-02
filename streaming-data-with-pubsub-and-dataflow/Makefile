pubsub-create-topic:
	gcloud pubsub topics create ${PUBSUB_TOPIC_ID}

pubsub-delete-topic:
	gcloud pubsub topics delete ${PUBSUB_TOPIC_ID}

pubsub-create-subscription:
	gcloud pubsub subscriptions create ${PUBSUB_SUBSCRIPTION_ID} \
		--expiration-period=${PUBSUB_SUBSCRIPTION_EXPIRATION_PERIOD} \
		--message-retention-duration=${PUBSUB_SUBSCRIPTION_MESSAGE_RETENTION_DURATION} \
		--topic=${PUBSUB_TOPIC_ID} \
		--topic-project=${GCP_PROJECT_ID}

pubsub-delete-subscription:
	gcloud pubsub subscriptions delete  ${PUBSUB_SUBSCRIPTION_ID}

gcs-create-bucket:
	gcloud storage buckets create gs://${GCS_BUCKET_NAME} \
		--location=${GCS_BUCKET_LOCATION} \
		--project=${GCP_PROJECT_ID}

gcs-remove-bucket:
	gcloud storage rm --recursive gs://${GCS_BUCKET_NAME}

gcs-upload-files:
	gsutil -m cp -r ${GCS_DATA_SOURCE_PATH} gs://${GCS_BUCKET_NAME}/

dataflow-batch-local-runner:
	python ${BEAM_PYTHON_FILE}\
		--project ${GCP_PROJECT_ID} \
		--region ${BEAM_REGION} \
		--runner DirectRunner \
		--temp-location gs://${GCS_BUCKET_NAME}/dataflow/temp \
		--input-file source/data/txt/* \
		--bucket-name ${GCS_BUCKET_NAME}

dataflow-stream-local-runner:
	python ${BEAM_PYTHON_FILE}\
		--project ${GCP_PROJECT_ID} \
		--region ${BEAM_REGION} \
		--runner DirectRunner \
		--temp-location gs://${GCS_BUCKET_NAME}/dataflow/temp \
		--subscription-id ${PUBSUB_SUBSCRIPTION_ID} \
		--table-id ${BIGQUERY_TABLE_ID}

dataflow-batch-dataflow-runner:
	python ${BEAM_PYTHON_FILE} \
		--project ${GCP_PROJECT_ID} \
		--region ${BEAM_REGION} \
		--runner DataflowRunner \
		--temp-location gs://${GCS_BUCKET_NAME}/dataflow/temp \
		--input-file source/data/txt/* \
		--bucket-name ${GCS_BUCKET_NAME}

dataflow-stream-dataflow-runner:
	python ${BEAM_PYTHON_FILE}\
		--project ${GCP_PROJECT_ID} \
		--region ${BEAM_REGION} \
		--runner DataflowRunner \
		--temp-location gs://${GCS_BUCKET_NAME}/dataflow/temp \
		--subscription-id projects/${GCP_PROJECT_ID}/subscriptions/${PUBSUB_SUBSCRIPTION_ID} \
		--table-id ${BIGQUERY_TABLE_ID}

python-install:
	pip install --upgrade pip && pip install -r requirements.txt

python-lint:
	python -m pylint ./source/python/*.py

python-black:
	python -m black ./source/python/*.py

all-pubsub-stream: gcs-create-bucket gcs-upload-files pubsub-create-topic pubsub-create-subscription

tear-down-pubsub-stream: pubsub-delete-subscription pubsub-delete-topic gcs-remove-bucket

all-dataflow: gcs-create-bucket gcs-upload-files pubsub-create-topic pubsub-create-subscription

tear-down-dataflow: pubsub-delete-subscription pubsub-delete-topic gcs-remove-bucket
