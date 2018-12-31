#!/usr/bin/env bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
JOB_NAME="netkeiba_$(date +"%Y%m%dT%H%M%S")"
JOB_DIR=gs://${GCLOUD_BUCKET}/ml-engine/jobs/${JOB_NAME}
MLE_TRAINING_PACKAGE_PATH="${SCRIPT_DIR}/../trainer"
MLE_MAIN_TRAINER_MODULE="trainer.task"

gcloud ml-engine jobs submit training ${JOB_NAME} \
  --job-dir ${JOB_DIR} \
  --package-path ${MLE_TRAINING_PACKAGE_PATH} \
  --module-name ${MLE_MAIN_TRAINER_MODULE} \
  --region ${MLE_REGION} \
  --runtime-version=${MLE_RUNTIME_VERSION} \
  --python-version=${MLE_PYTHON_VERSION} \
  --scale-tier ${MLE_SCALE_TIER}
