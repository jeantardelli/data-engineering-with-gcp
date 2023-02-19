#!/bin/bash


for i in raw_bikesharing dwh_bikesharing dm_bikesharing; do
    python ./basic-phython-examples/scripts/create_dataset.py -l ${LOCATION} -n ${i}
done
