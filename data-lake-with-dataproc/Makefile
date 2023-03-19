gcs-create-bucket:
	gcloud storage buckets create gs://${GCS_BUCKET_NAME} \
		--location=${GCS_BUCKET_LOCATION} \
		--project=${GCP_PROJECT_ID}

gcs-remove-bucket:
	gcloud storage rm --recursive gs://${GCS_BUCKET_NAME}

gcs-upload-source-files:
	gsutil -m cp -r ${GCS_DATA_SOURCE_PATH} gs://${GCS_BUCKET_NAME}/

gcs-upload-dag-files:
	gsutil -m cp -r ${GCS_DAGS_SOURCE_PATH} gs://${GCS_BUCKET_NAME}/

dataproc-create-cluster:
	bash ./scripts/dataproc_create_cluster.sh

dataproc-delete-cluster:
	yes | gcloud dataproc clusters delete ${DATAPROC_CLUSTER_NAME} \
		--region ${DATAPROC_CLUSTER_REGION}

dataproc-master-ssh-connection:
	gcloud compute ssh ${DATAPROC_CLUSTER_NAME}-m \
		--zone ${DATAPROC_CLUSTER_ZONE} \
		--project ${GCP_PROJECT_ID}

dataproc-load-data-from-gcs-to-hdfs:
	bash ./scripts/load_data_from_gcs_to_hdfs.sh

dataproc-submit-pyspark-job:
	gcloud dataproc jobs submit pyspark gs://${GCS_BUCKET_NAME}/${GCS_BUCKET_PYSPARK_PATH} \
		--cluster ${DATAPROC_CLUSTER_NAME} \
		--region ${DATAPROC_CLUSTER_REGION}

dataproc-submit-pyspark-job-to-bigquery:
	gcloud dataproc jobs submit pyspark gs://${GCS_BUCKET_NAME}/${GCS_BUCKET_PYSPARK_PATH} \
		--cluster ${DATAPROC_CLUSTER_NAME} \
		--region ${DATAPROC_CLUSTER_REGION} \
		--jars gs://spark-lib/bigquery/spark-bigquery-latest_2.12.jar

cloud-composer-setup-env:
	gcloud composer environments create ${CLOUD_COMPOSER_ENVIRONMENT_NAME} \
		--location=${CLOUD_COMPOSER_LOCATION} \
		--image-version=${CLOUD_COMPOSER_IMAGE_VERSION} \
		--node-count=${CLOUD_COMPOSER_NODE_COUNT} \
		--machine-type=${CLOUD_COMPOSER_MACHINE_TYPE} \
		--disk-size=${CLOUD_COMPOSER_DISK_SIZE} \
		--python-version=${CLOUD_COMPOSER_PYTHON_VERSION} \
		--zone=${CLOUD_COMPOSER_LOCATION}-a

cloud-composer-export-env-variables:
	gcloud beta composer environments update ${CLOUD_COMPOSER_ENVIRONMENT_NAME} \
		--location=${CLOUD_COMPOSER_LOCATION} \
		--update-env-variables=DATAPROC_CLUSTER_NAME=${DATAPROC_CLUSTER_NAME},GCP_PROJECT_ID=${GCP_PROJECT_ID},DATAPROC_CLUSTER_REGION=${DATAPROC_CLUSTER_REGION},GCS_BUCKET_PYSPARK_PATH=${GCS_BUCKET_PYSPARK_PATH},DATAPROC_CLUSTER_NUM_WORKERS=${DATAPROC_CLUSTER_NUM_WORKERS} 

cloud-composer-deploy-dag:
	gcloud composer environments storage dags import \
		--environment ${CLOUD_COMPOSER_ENVIRONMENT_NAME} \
		--location ${CLOUD_COMPOSER_LOCATION} \
		--source ${CLOUD_COMPOSER_DAG_FILENAME}

cloud-composer-delete-env:
	yes | gcloud composer environments delete ${CLOUD_COMPOSER_ENVIRONMENT_NAME} --location=${CLOUD_COMPOSER_LOCATION}

python-black:
	python -m black ./source/pyspark/* && python -m black ./dags/*.py

python-lint:
	python -m pylint ./source/pyspark/* && python -m pylint ./dags/*.py

gcs-setup: gcs-create-bucket gcs-upload-source-files gcs-upload-dag-files

dataproc-setup: dataproc-create-cluster dataproc-load-data-from-gcs-to-hdfs

all-dataproc: gcs-setup dataproc-setup

tear-down-dataproc: dataproc-delete-cluster gcs-remove-bucket

all-cloud-composer: gcs-setup cloud-composer-setup-env cloud-composer-export-env-variables

tear-down-cloud-composer: cloud-composer-delete-env gcs-remove-bucket
