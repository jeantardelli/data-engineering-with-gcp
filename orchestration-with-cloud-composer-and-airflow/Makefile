gcs-create-bucket:
	gcloud storage buckets create gs://${GCS_BUCKET_NAME} \
		--location=${GCS_LOCATION} \
		--project=${GCS_PROJECT}
gcs-upload-file:
	gsutil cp -r ${GCS_DATA_SOURCE_PATH} gs://${GCS_BUCKET_NAME}/

cloud-sql-instance:
	gcloud sql instances create ${CLOUD_SQL_INSTANCE_NAME} \
		--database-version=${CLOUD_SQL_DATABASE_VERSION} \
		--tier=${CLOUD_SQL_TIER} \
		--region=${CLOUD_SQL_REGION} \
		--root-password=${CLOUD_SQL_ROOT_PASSWORD} \
		--availability-type=${CLOUD_SQL_AVAILABILITY_TYPE} \
		--storage-size=${CLOUD_SQL_STORAGE_SIZE} \
		--storage-type=${CLOUD_SQL_STORAGE_TYPE}

cloud-sql-create-database:
	gcloud sql databases create ${CLOUD_SQL_DATABASE_NAME} \
		--instance=${CLOUD_SQL_INSTANCE_NAME} 
cloud-sql-create-table:
	python ./scripts/cloud_sql_create_table.py

cloud-sql-grant-gcs-permissions:
	gsutil iam ch serviceAccount:${CLOUD_SQL_SERVICE_ACCOUNT}:objectAdmin gs://${GCS_BUCKET_NAME}

cloud-sql-import-data:
	yes | gcloud sql import csv ${CLOUD_SQL_INSTANCE_NAME} gs://${GCS_BUCKET_NAME}/${CLOUD_SQL_IMPORT_FILE_PATH}/${CLOUD_SQL_IMPORT_FILE_NAME} \
		--database=${CLOUD_SQL_DATABASE_NAME} \
		--table=${CLOUD_SQL_TABLE_NAME}

cloud-composer-api:
	gcloud services enable composer.googleapis.com

cloud-composer-environment:
	gcloud composer environments create ${CLOUD_COMPOSER_ENVIRONMENT_NAME} \
		--location ${CLOUD_COMPOSER_LOCATION} \
		--image-version ${CLOUD_COMPOSER_IMAGE_VERSION} \
		--node-count ${CLOUD_COMPOSER_NODE_COUNT} \
		--machine-type ${CLOUD_COMPOSER_MACHINE_TYPE} \
		--disk-size ${CLOUD_COMPOSER_DISK_SIZE} \
		--python-version ${CLOUD_COMPOSER_PYTHON_VERSION}

cloud-composer-env-variables:
	gcloud beta composer environment create --env-variables=["CLOUD_SQL_INSTANCE_NAME"="${CLOUD_SQL_INSTANCE_NAME}"]

cloud-composer-deploy-dag:
	gcloud composer environments storage dags import \
		--environment ${CLOUD_COMPOSER_ENVIRONMENT_NAME} \
		--location ${CLOUD_COMPOSER_LOCATION} \
		--source ${CLOUD_COMPOSER_FILENAME}

cloud-composer-delete-dag:
	gcloud composer environments storage dags delete \
		--environment ${CLOUD_COMPOSER_ENVIRONMENT_NAME} \
		--location ${CLOUD_COMPOSER_LOCATION} \
		--source ${CLOUD_COMPOSER_FILENAME}

python-install:
	pip install --upgrade pip && pip install -r ./requirements.txt

python-lint:
	python -m pylint ./code/*

python-black:
	python -m black ./code/*

cloud-sql-set-up: cloud-sql-instance cloud-sql-create-database cloud-sql-create-table cloud-sql-grant-gcs-permissions cloud-sql-import-data

gcs-set-up: gcs-create-bucket gcs-upload-file

all: gcs-set-up cloud-sql-set-up
