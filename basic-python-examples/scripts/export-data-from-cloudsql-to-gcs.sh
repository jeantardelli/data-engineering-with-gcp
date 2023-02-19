#!/bin/bash

BUCKET=cicd-data-engineer-pipelines

gcloud sql export csv mysql-instance-source gs://$BUCKET/mysql-export/stations/20280101/stations.csv \
	--database=apps_db \
	--offload \
	--query='SELECT * FROM stations WHERE station_id <= 200;'

gcloud sql export csv mysql-instance-source gs://$BUCKET/mysql-export/stations/20280102/stations.csv \
	--database=apps_db \
	--offload \
	--query='SELECT * FROM stations WHERE station_id <= 400;'

