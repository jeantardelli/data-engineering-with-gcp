#!/bin/bash

FILEPATH=$(grep -oE '^(.*[\\\/])' <<< ${GCS_BUCKET_OBJECT_PATH})

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
	--project ${GCP_PROJECT_ID} \
	--properties spark-env:DATAPROC_CLUSTER_NAME=${DATAPROC_CLUSTER_NAME}-m,spark-env:FILEPATH=${FILEPATH},spark-env:GCP_PROJECT_ID=${GCP_PROJECT_ID}
