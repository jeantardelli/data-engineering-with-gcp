#!/bin/bash

NOSQL_FILENAME=$(grep -oE '[^\/]+$' <<< ${GCS_BUCKET_OBJECT_NOSQL_PATH})

echo "Table will be created based on this staments: "
gsutil cat gs://${GCS_BUCKET_NAME}/${GCS_BUCKET_OBJECT_NOSQL_PATH} 

gcloud compute ssh ${DATAPROC_CLUSTER_NAME}-m \
	--zone ${DATAPROC_CLUSTER_ZONE} \
        --project ${GCP_PROJECT_ID} << EOF
    echo "Loading nosql to master node"
    gsutil cp gs://${GCS_BUCKET_NAME}/${GCS_BUCKET_OBJECT_NOSQL_PATH} ./
    echo "Create hive table" 
    hive -f ${NOSQL_FILENAME}
EOF
