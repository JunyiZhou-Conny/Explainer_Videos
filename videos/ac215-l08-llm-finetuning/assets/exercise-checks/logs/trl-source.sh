#!/bin/sh
# Read (never run) trl 1.14.0's SFTTrainer source: which tokens the notebook's training loss covers.
# The wheel is downloaded into a throwaway container and unzipped there; nothing is imported.
docker run --rm --network host -e HTTPS_PROXY -e https_proxy="$HTTPS_PROXY" -v /root/.ccr/ca-bundle.crt:/ca.crt:ro \
  -e SSL_CERT_FILE=/ca.crt -e PIP_CERT=/ca.crt python:3.12-slim-bookworm sh -c '
  pip download -q --no-deps trl==1.14.0 -d /tmp/t >/dev/null 2>&1 && cd /tmp/t && ls *.whl &&
  python -m zipfile -e trl-1.14.0-py3-none-any.whl x && cd x/trl/trainer &&
  echo "--- sft_config.py:259-280" && sed -n 259,280p sft_config.py &&
  echo "--- sft_trainer.py:1625-1652" && sed -n 1625,1652p sft_trainer.py'
