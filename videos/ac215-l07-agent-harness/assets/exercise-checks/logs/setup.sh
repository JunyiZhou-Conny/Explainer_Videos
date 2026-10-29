#!/bin/sh
# Disposable check environment for exercises.md (run on the session machine; nothing from the repo runs on the host).
# 1) the repo at the pinned commit into the volume l07ex-work (git archive of the read-only clone);
# 2) a venv in the volume l07ex-venv, made inside python:3.13-slim-bookworm (the Dockerfile's base) with uv 0.13.4
#    (the capture's uv), constrained to the exact versions of the repo's own uv.lock.
set -e
CLONE=${CLONE:?path of the read-only agent-harness clone}
docker volume create l07ex-work >/dev/null
docker volume create l07ex-venv >/dev/null
git -C "$CLONE" archive e25dfe9615d78b78e0764a636cc2462f530a1402 \
  | docker run --rm -i --network none -v l07ex-work:/work python:3.13-slim-bookworm \
      sh -c 'cd /work && tar -x && chown -R 1000:1000 /work && ls | wc -l'
docker run --rm --network host -e HTTPS_PROXY -e https_proxy="$HTTPS_PROXY" \
  -v /root/.ccr/ca-bundle.crt:/ca.crt:ro -e SSL_CERT_FILE=/ca.crt -e PIP_CERT=/ca.crt -e UV_NATIVE_TLS=1 \
  -v l07ex-work:/work:ro -v l07ex-venv:/venv python:3.13-slim-bookworm sh -c '
    set -e
    python --version
    pip install -q --root-user-action=ignore uv==0.13.4
    uv --version
    cd /work
    uv export --frozen --no-hashes --no-emit-project --no-header > /tmp/lock-versions.txt
    wc -l < /tmp/lock-versions.txt
    uv venv -q /venv --python /usr/local/bin/python3
    # The code imports agent_framework (core), agent_framework.openai, openai, httpx, pydantic, opentelemetry.
    # agent-framework==1.19.0 is a metapackage that pulls agent-framework-core[all] (~30 integrations);
    # it is installed --no-deps, so importlib.metadata still finds it, without the integrations.
    uv pip install -q --python /venv/bin/python -c /tmp/lock-versions.txt \
      agent-framework-core==1.19.0 agent-framework-openai==1.14.4 openai==3.19.2 httpx==0.28.1 \
      opentelemetry-api==1.40.0 opentelemetry-sdk==1.40.0 pydantic==2.13.5
    uv pip install -q --python /venv/bin/python --no-deps agent-framework==1.19.0
    uv pip list --python /venv/bin/python | tee /venv/packages.txt | wc -l
    chown -R 1000:1000 /venv
    du -sh /venv'
