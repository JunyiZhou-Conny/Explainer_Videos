#!/bin/bash
# bld.sh <tag> <log> [extra args...]: docker build of the tutorial's Dockerfile in the current folder, with the
# check-only base (python:3.12-slim-bookworm + proxy CA) substituted through a named build context; plain log.
tag=$1; log=$2; shift 2
docker build --progress=plain --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg https_proxy=$HTTPS_PROXY \
  --build-context python:3.12-slim-bookworm=docker-image://l05ex/base:3.12 "$@" -t "$tag" -f Dockerfile . > "$log" 2>&1
echo "exit $?"
grep -E '^#[0-9]+ \[[0-9]+/[0-9]+\]|^#[0-9]+ CACHED|ERROR|error:|transferring context: [0-9]' "$log" | uniq
