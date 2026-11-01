#!/bin/sh
# hrun.sh <check.sh> <log>: run one check script in a throwaway container, the way a student types at the
# llm-dataset-creator container's prompt. The pristine work copy (volume l08ex-work: the repo at 44ef6f0 and the
# scripted data) is copied to /repo (a tmpfs) first, so every check starts from a fresh clone with no data/;
# the venv (volume l08ex-venv) is mounted read-only and on PATH, as docker-entrypoint.sh activates /.venv.
# The three variables are the ones docker-shell.sh passes (env.dev's defaults); /secrets is an empty folder, as in
# the captures (no key). --network none: nothing can reach Google. User 1000 (the image's `app` uid).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
docker run --rm --network none -u 1000:1000 \
  --mount type=tmpfs,destination=/repo,tmpfs-mode=1777 \
  --mount type=tmpfs,destination=/secrets,tmpfs-mode=1777 \
  -v l08ex-work:/work:ro -v l08ex-venv:/venv:ro -v "$HERE":/checks:ro \
  -e HOME=/tmp -e PATH=/venv/bin:/usr/local/bin:/usr/bin:/bin -e VIRTUAL_ENV=/venv \
  -e PYTHONDONTWRITEBYTECODE=1 \
  -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json \
  -e GCP_PROJECT=ac215-project -e GCS_BUCKET_NAME=cheese-dataset \
  -w /repo python:3.12-slim-bookworm \
  sh -c 'for f in /work/*; do cp -a "$f" /repo/ || exit 1; done; . /checks/lib.sh && . /checks/'"$1" > "$HERE/$2" 2>&1 || true
tail -n 3 "$HERE/$2"
