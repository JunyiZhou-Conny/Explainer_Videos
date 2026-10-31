#!/bin/sh
# A second disposable venv (volume l08ex-peft) for the LoRA counts: the notebook's pinned transformers 5.16.1,
# tokenizers 0.23.1 and huggingface-hub 1.29.0 (nb cell 8), peft 0.20.0 (the recorded run's, nb cell 12), and torch
# 2.11.0 as a CPU-only wheel (the recorded run had 2.11.0+cu128 on an A100; no GPU here). No bitsandbytes: it needs a GPU.
set -e
docker volume create l08ex-peft >/dev/null
docker run --rm --network host -e HTTPS_PROXY -e https_proxy="$HTTPS_PROXY" \
  -v /root/.ccr/ca-bundle.crt:/ca.crt:ro -e SSL_CERT_FILE=/ca.crt -e PIP_CERT=/ca.crt -e UV_NATIVE_TLS=1 \
  -v l08ex-peft:/venv python:3.12-slim-bookworm sh -c '
    set -e
    pip install -q --root-user-action=ignore uv==0.13.6
    uv venv -q /venv --python /usr/local/bin/python3
    uv pip install -q --python /venv/bin/python --index-url https://download.pytorch.org/whl/cpu torch==2.11.0
    uv pip install -q --python /venv/bin/python transformers==5.16.1 tokenizers==0.23.1 huggingface-hub==1.29.0 peft==0.20.0
    uv pip list --python /venv/bin/python | grep -iE "^(torch|transformers|peft|tokenizers|huggingface-hub|accelerate) "
    chown -R 1000:1000 /venv
    du -sh /venv'
