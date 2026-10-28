#!/bin/bash
# rag-setup.sh <read-only clone of dlops-io/llm-rag>
# The llm-rag check environment. Everything lives in named Docker volumes and containers called l06ex-*,
# removed by name afterwards; nothing from the repo runs on the host.
#   l06ex-rag-work  -> /work/llm-rag : the repo's files at e17a39f (the pinned commit; git archive, no .git),
#                                      plus outputs/embeddings-char-split-*.jsonl from 68e0bde (the staff's
#                                      recorded vectors, as the video's laptop/08 copies them)
#   l06ex-rag-venv  -> /.venv        : `uv sync --frozen` of the repo's own uv.lock, as Dockerfile:45 does,
#                                      on the Dockerfile's base image python:3.12-slim-bookworm
#   l06ex-chroma    : chromadb/chroma@sha256:1e0b73a1... (the image L05/L06's captures pulled as `latest`),
#                     on a private network l06ex-net with the alias llm-rag-chromadb, data in l06ex-chroma-data
set -e
SRC=$1
CA=/root/.ccr/ca-bundle.crt
CHROMA=chromadb/chroma@sha256:1e0b73a187a28757c572acba508c46f48c9e8b0acaf5c20e6d95cdedce1acdf6
for v in l06ex-rag-work l06ex-rag-venv l06ex-chroma-data; do docker volume create "$v" >/dev/null; done
docker network create l06ex-net >/dev/null

# the work copy: today's files + the staff's char-split vectors
{ git -C "$SRC" archive --prefix=llm-rag/ e17a39f
} | docker run --rm -i -v l06ex-rag-work:/work python:3.12-slim-bookworm tar -x -C /work
git -C "$SRC" archive 68e0bde llmrag/outputs/ \
  | docker run --rm -i -v l06ex-rag-work:/work python:3.12-slim-bookworm \
      tar -x -C /work/llm-rag --strip-components=1 --wildcards 'llmrag/outputs/embeddings-char-split-*'

# the venv: uv (the capture's 0.13.1) + uv sync --frozen
docker run --rm --network host -v l06ex-rag-work:/work -v l06ex-rag-venv:/.venv -v $CA:/ca.crt:ro \
  -e HTTPS_PROXY=$HTTPS_PROXY -e https_proxy=$HTTPS_PROXY -e SSL_CERT_FILE=/ca.crt -e PIP_CERT=/ca.crt \
  -e REQUESTS_CA_BUNDLE=/ca.crt -e UV_LINK_MODE=copy -e UV_PROJECT_ENVIRONMENT=/.venv \
  -w /work/llm-rag python:3.12-slim-bookworm bash -c \
  'pip install -q --root-user-action=ignore "uv==0.13.1" && uv --version && uv sync --frozen 2>&1 | tail -n 3 \
   && ls outputs | wc -l && du -sh outputs /.venv'

# the database server
docker run -d --name l06ex-chroma --network l06ex-net --network-alias llm-rag-chromadb \
  -v l06ex-chroma-data:/data "$CHROMA" >/dev/null
echo "setup done"
