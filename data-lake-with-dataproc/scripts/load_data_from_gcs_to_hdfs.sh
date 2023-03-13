#!/bin/bash

FILEPATH=$(grep -oE '^(.*[\\\/])' <<< ${GCS_BUCKET_OBJECT_PATH})
FILENAME=$(grep -oE '[^\/]+$' <<< ${GCS_BUCKET_OBJECT_PATH})

echo "Filepath to be loaded: ${FILEPATH}"
echo "Filename to be loaded: ${FILENAME}"

gcloud compute ssh ${DATAPROC_CLUSTER_NAME}-m \
	--zone ${DATAPROC_CLUSTER_ZONE} \
        --project ${GCP_PROJECT_ID} << EOF

    echo "Loading file to master node"
    gsutil cp gs://${GCS_BUCKET_NAME}/${GCS_BUCKET_OBJECT_PATH} ./
    echo "Creating data directory in HDFS"
    hdfs dfs -mkdir ../../data
    echo "Creating a filepath to load the file"
    hdfs dfs -mkdir -p ../../data/${FILEPATH}
    echo "Loading file to HDFS"
    if hdfs dfs -test -e ../../data/${FILEPATH}/${FILENAME}
    then 
        echo "File exsits on HDFS"
        hdfs dfs -ls ../../data/${FILEPATH}
    else
        echo "Adding file to HDFS"
        hdfs dfs -put ${FILENAME} ../../data/${FILEPATH}
        hdfs dfs -ls ../../data/${FILEPATH}
    fi
EOF
