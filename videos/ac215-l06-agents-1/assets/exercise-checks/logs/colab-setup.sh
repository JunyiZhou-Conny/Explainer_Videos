#!/bin/bash
# colab-setup.sh: three venvs standing in for the Colab runtimes (python:3.12-slim-bookworm, Python 3.12), in the
# named volume l06ex-colab (removed by name afterwards), each with exactly what its notebook's install cell asks for:
#   /colab/tp : Travel Planner cell 8       openai-agents==0.3.2
#   /colab/nl : Newsletter cell 8           agent-framework-core==1.18.0 agent-framework-openai==1.14.3 opentelemetry-api==1.42.1
#   /colab/cq : Cheese Quiz cell 10         fastmcp openai-agents   (unpinned, as the cell installs them)
set -e
CA=/root/.ccr/ca-bundle.crt
docker volume create l06ex-colab >/dev/null
docker run --rm --network host -v l06ex-colab:/colab -v $CA:/ca.crt:ro -e HTTPS_PROXY=$HTTPS_PROXY \
  -e https_proxy=$HTTPS_PROXY -e SSL_CERT_FILE=/ca.crt -e PIP_CERT=/ca.crt python:3.12-slim-bookworm bash -c '
  set -e
  for v in tp nl cq; do python -m venv /colab/$v; done
  /colab/tp/bin/pip install -q --disable-pip-version-check "openai-agents==0.3.2"
  /colab/nl/bin/pip install -q --disable-pip-version-check "agent-framework-core==1.18.0" "agent-framework-openai==1.14.3" "opentelemetry-api==1.42.1"
  /colab/cq/bin/pip install -q --disable-pip-version-check fastmcp openai-agents
  for v in tp nl cq; do echo "== $v"; /colab/$v/bin/pip list --disable-pip-version-check 2>/dev/null | grep -i -E "^(openai-agents|openai|fastmcp|mcp|agent-framework-core|agent-framework-openai|pydantic) "; done
  du -sh /colab/*'
