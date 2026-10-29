#!/bin/bash
# rrun.sh <log> <command...>: runs <command> in a throwaway python:3.12-slim-bookworm container with an llm-rag
# work copy on /app (a folder of the volume l06ex-rag-work: llm-rag, or COPY=<folder>), the venv on /.venv
# activated (as docker-entrypoint.sh:12 does), the checks' scripts read-only on /checks, GCP_PROJECT=your-project-id
# and the key path set as docker-shell.sh sets them, and an empty /secrets: what a student types at the
# container's prompt, without a key. Network: l06ex-net (Chroma by name, no internet).
# The log holds "$ command", the output and "[exit N]"; the instructor's name is masked as <instructor>.
log=$1; shift
here=$(cd "$(dirname "$0")" && pwd)
{ echo "\$ $*"
  docker run --rm --network l06ex-net \
    --mount "type=volume,src=l06ex-rag-work,dst=/app,volume-subpath=${COPY:-llm-rag}" \
    -v l06ex-rag-venv:/.venv -v "$here":/checks:ro \
    -e GCP_PROJECT=your-project-id -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json \
    -e PYTHONUNBUFFERED=1 -w /app python:3.12-slim-bookworm \
    bash -c "mkdir -p /secrets && source /.venv/bin/activate && { $*"$'\n'"} 2>&1" 2>&1 </dev/null
  echo "[exit $?]"; } | sed -e 's/Pavlos Protopapas/<instructor>/g' -e 's/[Pp]avlos/<instructor>/g' > "$log"
tail -n 30 "$log"
