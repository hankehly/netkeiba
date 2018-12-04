#!/usr/bin/env bash

PROJECT_ID="burnished-edge-177907"
BUCKET_ID="television-markup"
JOB_NAME="netkeiba_$(date +"%Y%m%d_%H%M%S")"
JOB_DIR=gs://${BUCKET_ID}/ml-engine/jobs/${JOB_NAME}
TRAINING_PACKAGE_PATH="../trainer/"
MAIN_TRAINER_MODULE="trainer.task"
REGION=us-central1
RUNTIME_VERSION=1.10
PYTHON_VERSION=2.7
SCALE_TIER=BASIC

gcloud ml-engine jobs submit training ${JOB_NAME} \
  --job-dir ${JOB_DIR} \
  --package-path ${TRAINING_PACKAGE_PATH} \
  --module-name ${MAIN_TRAINER_MODULE} \
  --region ${REGION} \
  --runtime-version=${RUNTIME_VERSION} \
  --python-version=${PYTHON_VERSION} \
  --scale-tier ${SCALE_TIER}
