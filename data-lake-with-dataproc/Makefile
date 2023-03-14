gcs-create-bucket:
	gcloud storage buckets create gs://${GCS_BUCKET_NAME} \
		--location=${GCS_BUCKET_LOCATION} \
		--project=${GCP_PROJECT_ID}

gcs-remove-bucket:
		gcloud storage rm --recursive gs://${GCS_BUCKET_NAME}

gcs-upload-file:
		gsutil -m cp -r ${GCS_DATA_SOURCE_PATH} gs://${GCS_BUCKET_NAME}/

dataproc-create-cluster:
	gcloud dataproc clusters create ${DATAPROC_CLUSTER_NAME} \
		--enable-component-gateway \
		--region ${DATAPROC_CLUSTER_REGION} \
		--zone ${DATAPROC_CLUSTER_ZONE} \
		--master-machine-type ${DATAPROC_CLUSTER_MASTER_MACHINE_TYPE} \
		--master-boot-disk-size ${DATAPROC_CLUSTER_MASTER_BOOT_DISK_SIZE} \
		--num-workers ${DATAPROC_CLUSTER_NUM_WORKERS} \
		--worker-machine-type ${DATAPROC_CLUSTER_WORKER_MACHINE_TYPE} \
		--worker-boot-disk-size ${DATAPROC_CLUSTER_WORKER_BOOT_DISK_SIZE} \
		--image-version ${DATAPROC_CLUSTER_IMAGE_VERSION} \
		--project ${GCP_PROJECT_ID}

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
	bash ./scripts/submit_pyspark_job.sh

python-black:
	python -m black ./source/pyspark/*

python-lint:
	python -m pylint ./source/pyspark/*

gcs-setup: gcs-create-bucket gcs-upload-file

dataproc-setup: dataproc-create-cluster dataproc-load-data-from-gcs-to-hdfs

all: gcs-setup dataproc-setup

tear-down: dataproc-delete-cluster gcs-remove-bucket
