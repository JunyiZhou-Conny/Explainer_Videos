#!/bin/bash
# adk-setup.sh <read-only clone of dlops-io/llm-agent-google-adk>: the ADK check laptop's home, in the named
# Docker volume l06ex-adk-home (removed by name afterwards). As student in ~/AC215: git clone (main = f89faa7),
# the README's `cp .env.example .env` and the video's .env edit (GEMINI_MODEL=gemini-3.1-flash-lite; the
# placeholder key stays), the video's fix `uv python pin 3.13`, then a .venv on uv's CPython 3.13 with the
# capture's package versions (adk-packages.txt). `uv run` is used with UV_NO_SYNC=1 from here on, so it
# does not add PyTorch back.
set -e
SRC=$1
here=$(cd "$(dirname "$0")" && pwd)
docker volume create l06ex-adk-home >/dev/null
docker run --rm -v l06ex-adk-home:/home/student l06ex/adk-laptop bash -c \
  'cp -rT /etc/skel /home/student && chown -R student:student /home/student'
docker run --rm --network host -u student -e HOME=/home/student -v "$SRC":/src:ro -v l06ex-adk-home:/home/student \
  -v "$here":/checks:ro -e HTTPS_PROXY=$HTTPS_PROXY -e https_proxy=$HTTPS_PROXY -w /home/student l06ex/adk-laptop bash -c '
  set -e
  git config --global --add safe.directory "*"
  printf "https-proxy=%s\ncafile=/etc/ssl/certs/ca-certificates.crt\n" "$HTTPS_PROXY" > ~/.npmrc
  mkdir -p AC215 && cd AC215
  git clone -q /src llm-agent-google-adk && cd llm-agent-google-adk && git log --oneline -1
  cp .env.example .env
  sed -i "s/^GEMINI_MODEL=.*/GEMINI_MODEL=gemini-3.1-flash-lite/" .env
  uv python pin 3.13
  uv venv -q
  uv pip install -q --no-deps -r /checks/adk-packages.txt
  UV_NO_SYNC=1 uv run adk --version
  .venv/bin/python --version
  du -sh .venv ~/.local/share/uv ~/.cache/uv 2>/dev/null || true'
