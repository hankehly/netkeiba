#!/usr/bin/env bash

docker build -t netkeiba_lambda .
docker run --rm --env-file=".env" netkeiba_lambda ./update-function-code.sh
