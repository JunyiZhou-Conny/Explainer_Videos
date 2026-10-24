#!/bin/bash
# Re-capture the L09 terminal transcripts (needs Docker and privileged containers):
#   bash assets/terminal/capture.sh laptop setup
#   bash assets/terminal/capture.sh laptop a-pre a-part1 a-part2 a-part3 a-part4 a-clean
#   bash assets/terminal/capture.sh laptop teardown
#   bash assets/terminal/capture.sh babykev setup
#   bash assets/terminal/capture.sh babykev b-setup b-prewarm b-s00 b-s01 b-s02 b-s03 b-s04 b-s04b b-s05 b-s05a b-s05b
#   bash assets/terminal/capture.sh babykev teardown
# Containers persist between calls, so a long capture can run in parts; `teardown` removes them.
#
# "laptop" (Track A, cheese-app-ci-cd Parts 1-4): a fresh, empty Docker engine
#   (docker:29.8.2-dind) stands in for the student's machine with Docker Desktop: user `student`
#   in the docker group, bash, python3, git, curl, GNU sed, and a Python virtualenv first on PATH
#   standing in for a laptop Python that allows `pip install` (capture-only: Alpine's own python
#   is PEP 668-protected; see ASSETS.md).
# "babykev" (Track B, the guest lecture): a fresh python:3.12-slim-bookworm container stands in
#   for a laptop WITHOUT Docker (the walk needs none until step-05b): user `student`, git, curl.
#   uv and just, the walk's prerequisites, are installed as captured steps. `b-prewarm` is
#   capture-only: it fills uv's package cache and the Hugging Face cache (torch, the Qwen base
#   model) in a throwaway clone, so the captured steps are not dominated by sandbox download
#   times; its log goes to babykev/capture-only/.
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l09-relay) makes the proxy reachable from Docker's bridge network, and the CA replaces each
# container's bundle as ASSETS.md describes ("capture-only"). Remove the relay with
# `docker rm -f l09-relay` when done.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
MODE=$1; shift
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l09-relay; then
    docker rm -f l09-relay >/dev/null 2>&1 || true
    docker run -d --name l09-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38693 "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:38693
  for i in $(seq 30); do   # wait until the relay listens, or the first apt/git call races it
    docker exec l09-relay python -c "import socket; socket.create_connection(('$GW', 38693), timeout=2).close()" >/dev/null 2>&1 && break
    sleep 1
  done
fi
PROXY_JSON=
[ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"

if [ "$MODE" = laptop ]; then
  DEST="$HERE/laptop"; mkdir -p "$DEST"
  for SEG in "$@"; do
    case $SEG in
      setup)
        docker rm -f l09-laptop >/dev/null 2>&1 || true
        docker volume rm l09-laptop-docker >/dev/null 2>&1 || true
        docker run -d --privileged --name l09-laptop --hostname laptop \
          -v l09-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
          -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
          --entrypoint sh docker:29.8.2-dind -c '
            cp /ca.crt /etc/ssl/certs/ca-certificates.crt
            exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
        docker exec -e PROXY_JSON="$PROXY_JSON" l09-laptop sh -c '
          set -e
          until docker info >/dev/null 2>&1; do sleep 1; done
          # the laptop baseline (not part of the tutorial): bash, git, curl, GNU sed, python3 (for
          # ptyrun.py) + a virtualenv first on PATH (a laptop Python that allows pip install),
          # and a user in the docker group
          apk add --no-cache -q bash python3 py3-virtualenv git curl sed >/dev/null
          adduser -D -s /bin/bash student && addgroup student docker
          virtualenv -q /home/student/venv
          mkdir -p /home/student/.docker
          [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
          chown -R student:student /home/student; chmod 777 /out' ;;
      teardown)
        docker rm -f l09-laptop >/dev/null; docker volume rm l09-laptop-docker >/dev/null ;;
      *)
        docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
          -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_HUB_WAIT="$([ -n "$RELAY" ] && echo 1)" \
          -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
          l09-laptop bash /capture/run_steps.sh /out "$SEG" ;;
    esac
  done
elif [ "$MODE" = babykev ]; then
  DEST="$HERE/babykev"; mkdir -p "$DEST"
  for SEG in "$@"; do
    case $SEG in
      setup)
        docker rm -f l09-babykev >/dev/null 2>&1 || true
        docker run -d --name l09-babykev --hostname laptop \
          -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
          -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
          -e SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
          -e REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
          -e UV_SYSTEM_CERTS=1 \
          python:3.12-slim-bookworm sleep infinity >/dev/null
        docker exec l09-babykev bash -c '
          set -e
          # the laptop baseline (not part of the walk): CA, https apt sources, git, curl, a user.
          # ca-certificates regenerates the bundle on install, so the CA is copied again after.
          cp /ca.crt /etc/ssl/certs/ca-certificates.crt
          sed -i "s|http://deb.debian.org|https://deb.debian.org|g" /etc/apt/sources.list.d/debian.sources
          apt-get update -qq >/dev/null
          DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git curl ca-certificates procps >/dev/null 2>&1
          cp /ca.crt /etc/ssl/certs/ca-certificates.crt
          rm -rf /var/lib/apt/lists/*
          useradd -m -s /bin/bash student
          chmod 777 /out' ;;
      teardown)
        docker rm -f l09-babykev >/dev/null ;;
      *)
        docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
          l09-babykev bash /capture/run_steps.sh /out "$SEG" ;;
    esac
  done
else
  echo "usage: capture.sh laptop|babykev setup|<segment>...|teardown" >&2; exit 2
fi
