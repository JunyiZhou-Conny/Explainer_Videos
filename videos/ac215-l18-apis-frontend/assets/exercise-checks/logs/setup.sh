#!/bin/bash
# Builds the two check-only images in a scratch context (the proxy CA is copied there, never here).
# Usage: bash setup.sh <scratch dir holding ca.crt>
D="$(cd "$(dirname "$0")" && pwd)"; SRC="$D/../../source"; W="$1"
. "$D/lib.sh"
mkdir -p "$W/py312" "$W/api313"
cp "$W/ca.crt" "$W/py312/"; cp "$W/ca.crt" "$W/api313/"
cp "$SRC/cheese-app-v2/src/api-service/pyproject.toml" "$SRC/cheese-app-v2/src/api-service/uv.lock" "$W/api313/"
B="docker build -q --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg https_proxy=$HTTPS_PROXY"
step "date -u; docker version --format 'Docker {{.Server.Version}}'"
step "$B -t l18ex/py312:check -f $D/py312-check.Dockerfile $W/py312"
step "docker run --rm l18ex/py312:check sh -c 'python --version; pip list 2>/dev/null | grep -iE \"^(fastapi|starlette|pydantic|uvicorn) \"'"
step "$B -t l18ex/api313:check -f $D/api313-check.Dockerfile $W/api313"
step "docker run --rm l18ex/api313:check sh -c 'python --version; pip list 2>/dev/null | grep -iE \"^(fastapi|starlette|pydantic|uvicorn|chromadb-client|google-genai|pytest|numpy|tensorflow.*) \"'"
