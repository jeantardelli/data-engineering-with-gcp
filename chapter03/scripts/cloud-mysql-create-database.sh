#!/bin/bash

RESULT=$(gcloud sql databases list --instance=mysql-instance-source --format=json)
FLAG=0

for i in $(echo ${RESULT} | jq -c '.[]'); do
    AUX=$(echo ${i} | jq '.name')
    if [ "$AUX" == '"apps_db"' ]; then 
        FLAG=1
    fi
done 

if [ "${FLAG}" == 0 ]; then
    echo "Creating <apps_db> databases!"
    gcloud sql databases create apps_db --instance=mysql-instance-source
else
    echo "<apps_db> database already exists!"
fi


