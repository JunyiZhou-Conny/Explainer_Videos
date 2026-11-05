#!/bin/sh
# Host side: C3 (what reaches the Part A container) with the host's Docker, then shell-in.sh in
# debian:12, then B2 (what "sagemaker" resolves to on Python 3.9) in python:3.9-slim with network
# for pip only (session proxy + CA), --dry-run --no-deps: nothing is installed.
D="$(cd "$(dirname "$0")" && pwd)"; SRC="$D/../../source"
. "$D/lib.sh"
# C3: Option 2's three exports, then the docker run flags of model-deployment-aws/docker-shell.sh:25-27
# (the image replaced by debian:12 running env; placeholder values only)
step 'export AWS_ACCESS_KEY_ID=your_access_key_id AWS_SECRET_ACCESS_KEY=your_secret_access_key AWS_REGION=us-east-1
S3_MODELS_BUCKET_NAME=your-models-bucket-placeholder SAGEMAKER_ROLE=arn:aws:iam::000000000000:role/SageMakerExecutionRole
docker run --rm --network none -e AWS_REGION=$AWS_REGION -e S3_MODELS_BUCKET_NAME=$S3_MODELS_BUCKET_NAME -e SAGEMAKER_ROLE=$SAGEMAKER_ROLE debian:12 env | grep -E "^(AWS|S3|SAGEMAKER)" | sort; echo "---- with the two extra -e flags:"
docker run --rm --network none -e AWS_ACCESS_KEY_ID -e AWS_SECRET_ACCESS_KEY -e AWS_REGION=$AWS_REGION debian:12 env | grep -E "^AWS" | sort'
docker run --rm --network none -v "$SRC/ml-workflow-aws/src":/src:ro -v "$D":/checks:ro debian:12 sh /checks/shell-in.sh
docker run --rm --network host -e HTTPS_PROXY="$HTTPS_PROXY" -e https_proxy="$HTTPS_PROXY" -e PIP_CERT=/ca.crt \
  -e SSL_CERT_FILE=/ca.crt -e PIP_DISABLE_PIP_VERSION_CHECK=1 -e PIP_ROOT_USER_ACTION=ignore -e PIP_NO_CACHE_DIR=1 \
  -v /root/.ccr/ca-bundle.crt:/ca.crt:ro -v "$D":/checks:ro python:3.9-slim sh -c '. /checks/lib.sh
step "python --version; pip install -q --upgrade pip && pip --version | cut -d\" \" -f1,2"
step "pip install -q --dry-run --no-deps --ignore-installed --report - \"sagemaker\" | python -c \"import json,sys; print(\\\"sagemaker   ->\\\", [i[\\\"metadata\\\"][\\\"version\\\"] for i in json.load(sys.stdin)[\\\"install\\\"]])\""
step "pip install -q --dry-run --no-deps --ignore-installed --report - \"sagemaker<3\" | python -c \"import json,sys; print(\\\"sagemaker<3 ->\\\", [i[\\\"metadata\\\"][\\\"version\\\"] for i in json.load(sys.stdin)[\\\"install\\\"]])\""'
