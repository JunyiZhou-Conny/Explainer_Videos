#!/bin/sh
# Host wrapper for tf.sh: python:3.11-slim, --network none, the venv from setup.sh, sources read-only.
# Usage: tf-run.sh <scratch-dir>   (<scratch-dir>/data holds brie-1.jpg and gouda-2.jpeg from
# `git show 077f4db:data/<name>` in a model-deployment-aws clone)
D="$(cd "$(dirname "$0")" && pwd)"; SRC="$D/../../source"
docker run --rm --network none -v "$1/venv-tf":/venv:ro -v "$1/data":/data:ro \
  -v "$SRC/model-deployment-aws":/md:ro -v "$SRC/ml-workflow-aws/src":/src:ro -v "$D":/checks:ro \
  python:3.11-slim sh /checks/tf.sh
