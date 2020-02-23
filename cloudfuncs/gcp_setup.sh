#!/bin/bash

# IoT core and Pub/Sub config
gcloud iot registries create CA2-Registry --region=asia-east1 --no-enable-http-config --event-notification-config=topic=alerts,subfolder=gas --event-notification-config=topic=alerts,subfolder=temp --event-notification-config=topic=data,subfolder=data --event-notification-config=topic=register,subfolder=register --event-notification-config=topic=alerts --state-pubsub-topic=state
gcloud pubsub topics create alerts data register

openssl genpkey -algorithm RSA -out rsa_private.pem -pkeyopt rsa_keygen_bits:2048
openssl rsa -in rsa_private.pem -pubout -out rsa_public.pem
gcloud iot devices create RPI --region=asia-east1 --registry=CA2-Registry  --public-key path=rsa_public.pem,type=rsa-pem
gcloud iot devices create mqtt-gateway --device-type=gateway --region=asia-east1 --registry=CA2-Registry --public-key path=rsa_public.pem,type=rsa-pem --auth-method=association-and-device-auth-token
gcloud iot devices gateways bind --gateway=mqtt-gateway --device=RPI --device-region=asia-east1 --device-registry=CA2-Registry --gateway-region=asia-east1 --gateway-registry=CA2-Registry

# Cloud SQL
gcloud sql instances create alarmy-postgres

# Cloud storage
gsutil mb gs://alarmy-person-images/

# Cloud functions
gcloud functions deploy data --runtime=python37 --trigger-topic=data --source=./data/ --entry-point=main --env-vars-file=../env.yaml
gcloud functions deploy register --runtime=python37 --trigger-topic=register --source=./register/ --entry-point=main --env-vars-file=../env.yaml
gcloud functions deploy envalert --r    untime=python37 --trigger-topic=envalert --source=./envalert/ --entry-point=main --env-vars-file=../env.yaml
gcloud functions deploy human_detection --runtime=python37 --trigger-topic=human_detection --source=./human_detection/ --entry-point=main --env-vars-file=../env.yaml

# Cloud vision API
gcloud services enable vision.googleapis.com
