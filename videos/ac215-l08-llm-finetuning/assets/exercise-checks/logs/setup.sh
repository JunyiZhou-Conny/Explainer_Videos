#!/bin/sh
# Disposable check environment for exercises.md (run on the session machine; nothing from the repo runs on the host).
# 1) the repo at the pinned commit (git archive of the read-only clone) and the capture's scripted data
#    (assets/terminal/capture-only/scripted/) into the volume l08ex-work;
# 2) a venv in the volume l08ex-venv, made inside python:3.12-slim-bookworm (the Dockerfile's base) with
#    uv 0.13.6 (the capture's uv), holding only the packages cli.py imports, constrained to the exact
#    versions of the repo's own dataset-creator/uv.lock (gemini-finetuner's lock is identical, laptop/16).
set -e
CLONE=${CLONE:?path of the read-only llm-finetuning clone}
SCRIPTED=${SCRIPTED:?path of assets/terminal/capture-only/scripted}
docker volume create l08ex-work >/dev/null
docker volume create l08ex-venv >/dev/null
git -C "$CLONE" archive 44ef6f0a70315aa0a551b8565ca862679a87c1eb README.md env.dev dataset-creator gemini-finetuner \
  | docker run --rm -i --network none -v l08ex-work:/work -v "$SCRIPTED":/scripted:ro python:3.12-slim-bookworm \
      sh -c 'cd /work && tar -x && mkdir -p scripted && cp /scripted/cheese_qa_*.txt scripted/ \
             && chown -R 1000:1000 /work && ls -A /work /work/dataset-creator /work/scripted'
docker run --rm --network host -e HTTPS_PROXY -e https_proxy="$HTTPS_PROXY" \
  -v /root/.ccr/ca-bundle.crt:/ca.crt:ro -e SSL_CERT_FILE=/ca.crt -e PIP_CERT=/ca.crt -e UV_NATIVE_TLS=1 \
  -v l08ex-work:/work:ro -v l08ex-venv:/venv python:3.12-slim-bookworm sh -c '
    set -e
    python --version
    pip install -q --root-user-action=ignore uv==0.13.6
    uv --version
    cd /work/dataset-creator
    uv export --frozen --no-hashes --no-emit-project --no-header > /tmp/lock-versions.txt
    wc -l < /tmp/lock-versions.txt
    uv venv -q /venv --python /usr/local/bin/python3
    # dataset-creator/cli.py imports pandas, sklearn, google.cloud.storage and google.genai;
    # gemini-finetuner/cli.py google.cloud.storage and google.genai. Nothing imports chromadb, langchain or openai.
    uv pip install -q --python /venv/bin/python -c /tmp/lock-versions.txt \
      pandas scikit-learn google-cloud-storage google-genai
    uv pip list --python /venv/bin/python | tee /venv/packages.txt | wc -l
    chown -R 1000:1000 /venv
    du -sh /venv'
