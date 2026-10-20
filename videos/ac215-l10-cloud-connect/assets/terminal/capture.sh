#!/bin/bash
# Re-capture the L10 terminal transcripts (needs Docker and privileged containers):
#   bash assets/terminal/capture.sh laptop setup
#   bash assets/terminal/capture.sh laptop pre net rag1 rag2 rag3 rag4 api1 api2 fe1 fe2 cors down
#   bash assets/terminal/capture.sh laptop teardown
# Containers persist between calls, so a long capture can run in parts; `teardown` removes them.
#
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind) stands in for the student's machine
#   with Docker Desktop: user `student` in the docker group, bash, python3 (for ptyrun.py), git,
#   curl, GNU sed, tree. There are NO GCP credentials in this environment: ~/secrets holds an
#   obviously-invalid placeholder key for the folder-structure steps and is emptied before the
#   credential-error steps, so every cloud call fails with the documented DefaultCredentialsError
#   (see ASSETS.md, "What cannot run here").
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l10-relay) makes the proxy reachable from Docker's bridge network, and the CA replaces the
# container's bundle and is baked into capture-only re-tags of the two base images
# (python:3.12-slim-bookworm, node:20-alpine) as ASSETS.md describes ("capture-only"). Remove the
# relay with `docker rm -f l10-relay` when done.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
MODE=$1; shift
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l10-relay; then
    docker rm -f l10-relay >/dev/null 2>&1 || true
    docker run -d --name l10-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38694 "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:38694
  for i in $(seq 30); do   # wait until the relay listens, or the first apt/git call races it
    docker exec l10-relay python -c "import socket; socket.create_connection(('$GW', 38694), timeout=2).close()" >/dev/null 2>&1 && break
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
        docker rm -f l10-laptop >/dev/null 2>&1 || true
        docker volume rm l10-laptop-docker >/dev/null 2>&1 || true
        docker run -d --privileged --name l10-laptop --hostname laptop \
          -v l10-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
          -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
          --entrypoint sh docker:29.8.2-dind -c '
            cp /ca.crt /etc/ssl/certs/ca-certificates.crt
            exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
        docker exec -e PROXY_JSON="$PROXY_JSON" l10-laptop sh -c '
          set -e
          until docker info >/dev/null 2>&1; do sleep 1; done
          # the laptop baseline (not part of the tutorial): bash, git, curl, GNU sed, tree,
          # python3 (for ptyrun.py), and a user in the docker group. The docker:dind image
          # already ships the compose plugin, as Docker Desktop does.
          apk add --no-cache -q bash python3 git curl sed tree >/dev/null
          adduser -D -s /bin/bash student && addgroup student docker
          mkdir -p /home/student/.docker
          [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
          chown -R student:student /home/student; chmod 777 /out' ;;
      teardown)
        docker rm -f l10-laptop >/dev/null; docker volume rm l10-laptop-docker >/dev/null ;;
      *)
        docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
          -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_HUB_WAIT="$([ -n "$RELAY" ] && echo 1)" \
          -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
          l10-laptop bash /capture/run_steps.sh /out "$SEG" ;;
    esac
  done
else
  echo "usage: capture.sh laptop setup|<segment>...|teardown" >&2; exit 2
fi
