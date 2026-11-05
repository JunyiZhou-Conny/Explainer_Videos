#!/bin/sh
# Host side, run once before the checks. Builds the two disposable virtual environments the checks
# use, in the session scratchpad (NOT in this folder), inside python:3.11-slim (the Python of the
# workflow and training images), with network only for pip, through the session proxy and its CA.
#   venv-sdk: sagemaker<3 (the fix), as the workflow image installs it after the pin
#   venv-tf:  tensorflow-cpu 2.20.0 + keras 3.11.2 (the training image lock) + pillow
# Usage: setup.sh <scratch-dir>
set -e
W=$1
mkdir -p "$W"
D="$(cd "$(dirname "$0")" && pwd)"
run() {
  docker run --rm --network host -e HTTPS_PROXY="$HTTPS_PROXY" -e https_proxy="$HTTPS_PROXY" \
    -e PIP_CERT=/ca.crt -e SSL_CERT_FILE=/ca.crt -e PIP_DISABLE_PIP_VERSION_CHECK=1 \
    -e PIP_ROOT_USER_ACTION=ignore -e PIP_NO_CACHE_DIR=1 \
    -v /root/.ccr/ca-bundle.crt:/ca.crt:ro -v "$W":/w -v "$D":/checks:ro python:3.11-slim sh -c "$1"
}
run '. /checks/lib.sh
step "python --version"
step "python -m venv /w/venv-sdk && /w/venv-sdk/bin/pip install -q \"sagemaker<3\" && /w/venv-sdk/bin/pip list 2>/dev/null | grep -i -E \"^(sagemaker|sagemaker-core|boto3|botocore|numpy) \""
step "python -m venv /w/venv-tf && /w/venv-tf/bin/pip install -q tensorflow-cpu==2.20.0 keras==3.11.2 pillow && /w/venv-tf/bin/pip list 2>/dev/null | grep -i -E \"^(tensorflow-cpu|tensorflow_cpu|keras|numpy|pillow) \""'
