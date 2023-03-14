#!/bin/bash

FILEPATH=$(grep -oE '^(.*[\\\/])' <<< ${GCS_BUCKET_OBJECT_PATH})
gcloud dataproc jobs submit pyspark gs://${GCS_BUCKET_NAME}/${GCS_BUCKET_PYSPARK_PATH} \
	--cluster ${DATAPROC_CLUSTER_NAME} \
	--region ${DATAPROC_CLUSTER_REGION} \
	--properties spark.executorEnv.DATAPROC_CLUSTER_NAME=${DATAPROC_CLUSTER_NAME}-m,spark.executorEnv.FILEPATH=${FILEPATH} \
