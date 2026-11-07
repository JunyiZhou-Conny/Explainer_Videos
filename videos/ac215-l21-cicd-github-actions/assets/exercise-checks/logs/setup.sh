#!/bin/bash
# Build the tutorial's image from its UNCHANGED Dockerfile at b8458ff. Only the FROM image is
# swapped, through a named build context, for py311-ca-check.Dockerfile (the official base + the
# session proxy's CA), so the build can download through the sandbox's proxy.
. "$(dirname "$0")/lib.sh"
export W IMG
step 'cd $SCRATCH/dlops/cheese-app-ci-cd && git rev-parse b8458ff && git ls-remote https://github.com/dlops-io/cheese-app-ci-cd.git refs/heads/main'
step 'docker image inspect --format "{{index .RepoDigests 0}}" mirror.gcr.io/library/python:3.11-slim-bookworm'
step 'cd $W && docker build --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg https_proxy=$HTTPS_PROXY --build-context python:3.11-slim-bookworm=docker-image://l21ex/py311-ca:check -t $IMG . 2>&1 | grep -E "^#[0-9]+ \[|naming to|ERROR|DONE [0-9.]+s$" | grep -v "^#[0-9]* DONE" | tail -20'
step 'docker run --rm $IMG bash -c "python --version; pip list 2>/dev/null | grep -iE \"^(black|flake8|pytest|pytest-cov|fastapi|uvicorn|httpx|pre.commit) \""'
