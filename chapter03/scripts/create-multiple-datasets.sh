#!/bin/bash


for i in raw_bikesharing dwh_bikesharing dm_bikesharing; do
    python ./chapter03/scripts/create_dataset.py -l ${LOCATION} -n ${i}
done
