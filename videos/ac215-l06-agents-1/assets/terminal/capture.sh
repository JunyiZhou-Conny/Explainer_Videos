#!/bin/bash
# Re-capture the L06 terminal transcripts. Two "laptops", one per tutorial repo:
#   bash assets/terminal/capture.sh rag   -> laptop/ + cli-container/: dlops-io/llm-rag (main), README "Agents"
#                                            (README.md:242-271) and the L05 steps it stands on, plus extras
#   bash assets/terminal/capture.sh adk   -> adk-laptop/ + mcp-remote/: dlops-io/llm-agent-google-adk (main), the
#                                            whole root README, plus extras (the Python pin, the ADK pin, the folder
#                                            rename, MCP over stdio, port 8000, the remote MCP server)
# Needs Docker with privileged containers, and python3 with `pyte` (pip install pyte; set PYTHON to it) so the live
# progress views of `docker compose`, `uv` and `adk web` render as a terminal shows them. Behind the recording proxy
# also export CA_BUNDLE (a PEM file with the proxy's CA). Each part removes its laptop at the end (KEEP=1 keeps it).
# Start from empty capture folders: run_steps.sh overwrites the files it writes and removes nothing.
#
# rag: "your laptop" is a fresh, empty Docker engine standing in for Docker Desktop (as in L05): a docker:29.8.2-dind
#   container with its own network namespace (so localhost:8000 and the fixed names llm-rag-chromadb /
#   llm-rag-network are the laptop's and nobody else's), with bash, git and curl, a user `student` (uid 1000) in the
#   docker group and the workspace ~/AC215 (llm-rag/ and secrets/ side by side, README.md:64-69).
# adk: "your laptop" is a fresh debian:12 container (own network namespace) with git, curl, uv (Astral's installer,
#   as in L01) and Node.js (nodejs.org's Linux binaries; on a Mac: brew install node), a user `student` and the
#   workspace ~/AC215. No system Python: uv downloads one, as on a Mac whose python3 is older than 3.10.
# run_steps.sh types each command into the laptop with `docker exec` (a fresh login shell per command, or a real
# pseudo-terminal via tty_session.py for interactive commands and live views). Nothing from the tutorial repos runs
# on the recording machine itself.
#
# Capture-only additions (not part of the tutorial; ASSETS.md describes their visible effects):
#  - Behind an HTTPS-only proxy on the host's 127.0.0.1, proxy_relay.py (container l06-relay) makes the proxy
#    reachable from Docker's bridge network; both laptops, their builds and containers use it.
#  - rag: python:3.12-slim-bookworm is pulled into the laptop and rebuilt under the same name with the proxy's CA and
#    https apt sources (capture-only/base-python-3.12-slim-bookworm.Dockerfile, L05's file), so the tutorial's own
#    Dockerfile builds unchanged. The laptop's engine pulls Docker Hub images through mirror.gcr.io and stores
#    images with the classic overlay2 driver (containerd-snapshotter off) to halve its disk use; pull and build
#    lines read the same, except the wording of Compose's failed pull of llm-rag-cli (ASSETS.md).
#  - adk: the README's first `uv sync` runs as written and fails (CPython 3.15, see ASSETS.md). After the Python pin and
#    `uv sync --dry-run` (the plan a Linux PC gets), run_steps.sh removes the lockfile that sync wrote and puts
#    index-strategy = "unsafe-best-match" and an extra index https://download.pytorch.org/whl/cpu into the student's
#    ~/.config/uv/uv.toml, so every later uv command takes PyTorch (pulled in by sentence-transformers) as the CPU-only
#    Linux wheel (torch==<v>+cpu) instead of the CUDA build with its nvidia-* packages and triton (about 3 GB, more
#    than the recording machine could hold). A Mac gets neither: macOS wheels have no CUDA. The student's home is a
#    3 GB tmpfs. ~/.npmrc carries the proxy for npx (see below). The G3 check starts a Chroma container in the
#    laptop's network namespace (docker run --network container:l06-adk) to stand in for llm-rag's published 8000.
#  - run_steps.sh is copied to a temporary file before it runs (so it can be edited while a capture runs).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
RS=$(mktemp); cp "$HERE/run_steps.sh" "$RS"
PART=$1
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  docker rm -f l06-relay >/dev/null 2>&1 || true      # the proxy's port changes when the machine restarts
  docker run -d --name l06-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
    python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38706 "$PHOST" "$PPORT" >/dev/null
  RELAY=http://$GW:38706
fi
export RELAY NOPX CA

if [ "$PART" = rag ]; then
  LAPTOP=l06-laptop; export LAPTOP
  # ---- a fresh laptop: empty Docker engine, bash/git/curl, user student, workspace ~/AC215 ----
  docker rm -f $LAPTOP >/dev/null 2>&1 || true
  docker volume rm l06-laptop-docker >/dev/null 2>&1 || true
  docker run -d --privileged --name $LAPTOP --hostname laptop \
    -v l06-laptop-docker:/var/lib/docker -v "$CA":/ca.crt:ro \
    -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
    --entrypoint sh docker:29.8.2-dind -c '
      cp /ca.crt /etc/ssl/certs/ca-certificates.crt
      mkdir -p /etc/docker
      echo "{\"registry-mirrors\":[\"https://mirror.gcr.io\"],\"features\":{\"containerd-snapshotter\":false}}" > /etc/docker/daemon.json
      exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
  PROXY_JSON=
  [ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"
  docker exec -e PROXY_JSON="$PROXY_JSON" $LAPTOP sh -c '
    set -e
    until docker info >/dev/null 2>&1; do sleep 1; done
    apk add --no-cache -q bash git curl coreutils diffutils grep findutils less >/dev/null
    adduser -D -u 1000 -s /bin/bash student && addgroup student docker
    mkdir -p /home/student/.docker /home/student/AC215
    [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
    chown -R student:student /home/student'
  # ---- capture-only base image (same name as the tutorial's FROM line; L05's Dockerfile, unchanged) ----
  mkdir -p "$HERE/capture-only"
  docker exec $LAPTOP docker pull -q python:3.12-slim-bookworm >/dev/null
  docker exec $LAPTOP mkdir -p /capture-ctx
  docker cp "$CA" $LAPTOP:/capture-ctx/capture-ca.crt
  docker cp "$HERE/capture-only/base-python-3.12-slim-bookworm.Dockerfile" $LAPTOP:/capture-ctx/base.Dockerfile
  { echo "\$ docker build -t python:3.12-slim-bookworm -f base-python-3.12-slim-bookworm.Dockerfile ."
    docker exec -w /capture-ctx $LAPTOP docker build --progress=plain -t python:3.12-slim-bookworm -f base.Dockerfile . 2>&1
    echo "[exit $?]"; } > "$HERE/capture-only/base-python-3.12-slim-bookworm-build.txt"
  bash "$RS" "$HERE" rag
  if [ -z "$KEEP" ]; then
    docker rm -f $LAPTOP >/dev/null
    docker volume rm l06-laptop-docker >/dev/null
  fi
elif [ "$PART" = adk ]; then
  LAPTOP=l06-adk; export LAPTOP
  docker rm -f $LAPTOP l06-adk-chroma >/dev/null 2>&1 || true
  # the student's home is a 3 GB tmpfs (capture-only: keeps the venv, uv's cache and Python off the recording disk)
  docker run -d --name $LAPTOP --hostname laptop -v "$CA":/ca.crt:ro \
    --tmpfs /home/student:rw,exec,size=3g,mode=0755,uid=1000,gid=1000 \
    -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
    debian:12 sleep infinity >/dev/null
  # the laptop's baseline (not part of the tutorial): CA bundle, https apt sources, git, curl, a user, uv, Node.js
  docker exec $LAPTOP bash -c '
    set -e
    mkdir -p /etc/ssl/certs && cp /ca.crt /etc/ssl/certs/ca-certificates.crt
    sed -i "s|http://deb.debian.org|https://deb.debian.org|g" /etc/apt/sources.list.d/debian.sources
    apt-get update -qq >/dev/null
    DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git curl ca-certificates xz-utils less procps >/dev/null 2>&1
    cp /ca.crt /etc/ssl/certs/ca-certificates.crt
    rm -rf /var/lib/apt/lists/*
    useradd -M -u 1000 -s /bin/bash student
    cp -rT /etc/skel /home/student && mkdir -p /home/student/AC215
    # npm reads its proxy and CA from ~/.npmrc: npx started by MCP (3-mcp-tools) gets only HOME/PATH/USER/... from its
    # parent (mcp stdio_client), not the proxy variables. A laptop with direct internet needs neither.
    [ -n "$HTTPS_PROXY" ] && printf "https-proxy=%s\ncafile=/etc/ssl/certs/ca-certificates.crt\n" "$HTTPS_PROXY" > /home/student/.npmrc
    chown -R student:student /home/student
    # Node.js: the newest LTS release of nodejs.org, its Linux x64 binaries in /usr/local
    V=$(curl -fsSL https://nodejs.org/dist/index.json | grep -o "\"version\":\"v[0-9.]*\"[^}]*\"lts\":\"[A-Za-z]*\"" | head -1 | grep -o "v[0-9][0-9.]*" | head -1)
    curl -fsSL "https://nodejs.org/dist/$V/node-$V-linux-x64.tar.xz" | tar -xJ -C /usr/local --strip-components=1
    echo "export SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt" > /etc/profile.d/capture-ca.sh'
  # uv, installed the way L01 does (Astral's installer), as the student
  docker exec -u student -e HOME=/home/student -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" $LAPTOP bash -lc \
    'curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null 2>&1'
  bash "$RS" "$HERE" adk
  docker rm -f l06-adk-chroma >/dev/null 2>&1 || true
  [ -z "$KEEP" ] && docker rm -f $LAPTOP >/dev/null
fi
[ -z "$KEEP" ] && docker rm -f l06-relay >/dev/null 2>&1 || true
rm -f "$RS"
