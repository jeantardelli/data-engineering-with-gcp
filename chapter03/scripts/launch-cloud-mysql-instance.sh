#!/bin/bash

RUNNING_INSTANCE=$(gcloud sql instances list --uri)

if [ -z "$RUNNING_INSTANCE" ]
  then
    echo "No instance running, creating one!"
    gcloud sql instances create mysql-instance-source \
	    --database-version=MYSQL_5_7 \
	    --tier=db-g1-small \
	    --region=europe-west1 \
	    --root-password=password1234 \
	    --availability-type=zonal \
	    --storage-size=10GB \
	    --storage-type=HDD
  else
    echo "There is already an instance running!"
fi
