#!/bin/bash
# bld.sh <tag> <log> [extra args...]: docker build in the current folder with the proxy CA base
# substituted for python:3.12-slim-bookworm (named build context), plain log to <log>
tag=$1; log=$2; shift 2
docker build --progress=plain --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg https_proxy=$HTTPS_PROXY \
  --build-context python:3.12-slim-bookworm=docker-image://l02ex/base:3.12 "$@" -t "$tag" -f Dockerfile . > "$log" 2>&1
echo "exit $?"
grep -E '^#[0-9]+ \[[0-9]+/[0-9]+\]|^#[0-9]+ (CACHED|DONE [0-9.]+s$)|Downloading cpython|ERROR|error:|transferring context' "$log" | grep -v '^#[0-9]* DONE' | uniq
