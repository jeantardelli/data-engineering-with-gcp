enable-cloud-composer-api:
	gcloud services enable composer.googleapis.com

create-environment:
	gcloud composer environments create ${ENVIRONMENT_NAME} \
		--location ${LOCATION} \
		--image-version ${IMAGE_VERSION} \
		--node-count ${NODE_COUNT} \
		--machine-type ${MACHINE_TYPE} \
		--disk-size ${DISK_SIZE} \
		--python-version ${PYTHON_VERSION}
install:
	pip install --upgrade pip && pip install -r ./requirements.txt

lint:
	python -m pylint ./code/*

black:
	python -m black ./code/*

deploy-dag:
	gcloud composer environments storage dags import \
		--environment ${ENVIRONMENT_NAME} \
		--location ${LOCATION} \
		--source ${FILENAME}
delete-dag:
	gcloud composer environments storage dags delete \
		--environment ${ENVIRONMENT_NAME} \
		--location ${LOCATION} \
		--source ${FILENAME}
