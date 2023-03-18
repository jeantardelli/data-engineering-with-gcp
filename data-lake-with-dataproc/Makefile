gcs-create-bucket:
	gcloud storage buckets create gs://${GCS_BUCKET_NAME} \
		--location=${GCS_BUCKET_LOCATION} \
		--project=${GCP_PROJECT_ID}

gcs-remove-bucket:
	gcloud storage rm --recursive gs://${GCS_BUCKET_NAME}

gcs-upload-file:
	gsutil -m cp -r ${GCS_DATA_SOURCE_PATH} gs://${GCS_BUCKET_NAME}/

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

python-black:
	python -m black ./source/pyspark/*

python-lint:
	python -m pylint ./source/pyspark/*

gcs-setup: gcs-create-bucket gcs-upload-file

dataproc-setup: dataproc-create-cluster dataproc-load-data-from-gcs-to-hdfs

all: gcs-setup dataproc-setup

tear-down: dataproc-delete-cluster gcs-remove-bucket
