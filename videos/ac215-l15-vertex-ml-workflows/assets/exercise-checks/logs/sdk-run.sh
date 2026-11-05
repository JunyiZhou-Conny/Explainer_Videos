#!/bin/sh
# Host wrapper for sdk.sh: python:3.11-slim, --network none, the venv from setup.sh, sources read-only.
# Usage: sdk-run.sh <scratch-dir>
D="$(cd "$(dirname "$0")" && pwd)"; SRC="$D/../../source"
docker run --rm --network none -v "$1/venv-sdk":/venv:ro -v "$SRC/model-deployment-aws":/md:ro \
  -v "$SRC/ml-workflow-aws/src/workflow":/wf:ro -v "$D":/checks:ro python:3.11-slim sh /checks/sdk.sh
