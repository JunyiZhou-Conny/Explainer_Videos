#!/bin/sh
# prun.sh <check.sh> <log>: run one check in the l08ex-peft venv (setup-peft.sh); no network, user 1000.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
docker run --rm --network none -u 1000:1000 -v l08ex-peft:/venv:ro -v "$HERE":/checks:ro \
  -e HOME=/tmp -e USER=student -e PATH=/venv/bin:/usr/local/bin:/usr/bin:/bin -e PYTHONDONTWRITEBYTECODE=1 \
  -e HF_HUB_OFFLINE=1 -w /tmp python:3.12-slim-bookworm sh -c '. /checks/lib.sh && . /checks/'"$1" > "$HERE/$2" 2>&1 || true
tail -n 3 "$HERE/$2"
