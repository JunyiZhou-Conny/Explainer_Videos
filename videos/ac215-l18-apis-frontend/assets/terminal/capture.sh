#!/bin/bash
# Re-capture the L18 terminal transcripts (needs Docker and privileged containers):
#   bash assets/terminal/capture.sh setup
#   bash assets/terminal/capture.sh pre v1 head
#   bash assets/terminal/capture.sh prune bases reset-v2 old
#   bash assets/terminal/capture.sh teardown
# The laptop container persists between calls, so the capture can run in parts (and its engine can be
# pruned between them: `capture.sh prune` removes every image, container and volume in it).
#
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind) stands in for the student's laptop with
#   Docker (both READMEs: "Have Docker installed" / "Docker, with ports 3000, 8000 and 9000 free"):
#   user `student` in the docker group, bash, git, curl, python3 (for ptyrun.py and JSON one-liners),
#   openssl. Its home folder is the README's parent folder (cheese-app-v1/, cheese-app-v2/, secrets/,
#   persistent-folder/). Every docker-shell.sh, docker build/run and every curl of a published port
#   runs here: repository code never runs on the recording host.
# There are NO GCP credentials (see ASSETS.md, "What cannot run here"): secrets/ml-workflow.json is a
#   well-formed key file around a throwaway key generated at capture time for no account.
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l18-relay) makes the proxy reachable from Docker's bridge network, and the CA replaces the laptop's
# bundle and is baked into capture-only re-tags of the base images (python:3.12/3.13-slim-bookworm,
# node:20-alpine, node:24.22.1-bookworm-slim) as ASSETS.md describes ("capture-only"). Docker's client
# proxy setting passes the relay to the builds and containers the tutorial starts. Remove the relay
# with `docker rm -f l18-relay` when done.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RPORT=38718
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l18-relay; then
    docker rm -f l18-relay >/dev/null 2>&1 || true
    docker run -d --name l18-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" $RPORT "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:$RPORT
  for i in $(seq 30); do   # wait until the relay listens, or the first apk/git call races it
    docker exec l18-relay python -c "import socket; socket.create_connection(('$GW', $RPORT), timeout=2).close()" >/dev/null 2>&1 && break
    sleep 1
  done
fi
PROXY_JSON=
[ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"
DEST="$HERE/laptop"; mkdir -p "$DEST"

for SEG in "$@"; do
  case $SEG in
    setup)
      docker rm -f l18-laptop >/dev/null 2>&1 || true
      docker volume rm l18-laptop-docker >/dev/null 2>&1 || true
      docker run -d --privileged --name l18-laptop --hostname laptop \
        -v l18-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        --entrypoint sh docker:29.8.2-dind -c '
          cp /ca.crt /etc/ssl/certs/ca-certificates.crt
          exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
      docker exec -e PROXY_JSON="$PROXY_JSON" l18-laptop sh -c '
        set -e
        until docker info >/dev/null 2>&1; do sleep 1; done
        # the laptop baseline (not part of the tutorial): bash, git, curl, python3, openssl, and a
        # user in the docker group. Docker client proxy settings (capture-only) pass the recording
        # proxy to the builds and containers the tutorial starts.
        apk add --no-cache -q bash python3 git curl openssl >/dev/null
        adduser -D -s /bin/bash -u 1000 student && addgroup student docker
        mkdir -p /home/student/.docker
        [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
        chown -R student:student /home/student; chmod 777 /out' ;;
    prune)
      docker exec l18-laptop sh -c 'docker ps -aq | xargs -r docker rm -f; docker system prune -af --volumes' >/dev/null ;;
    reset-v2)   # a fresh cheese-app-v2 clone + an empty persistent-folder (Chroma's data is root-owned)
      docker exec l18-laptop sh -c 'rm -rf /home/student/cheese-app-v2 /home/student/persistent-folder/* /home/student/persistent-folder/.[!.]* /tmp/l18-cue-*'
      docker exec -u student -w /home/student -e HOME=/home/student -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" \
        l18-laptop bash /capture/run_steps.sh /out reset-v2 ;;
    teardown)
      docker rm -f l18-laptop >/dev/null; docker volume rm l18-laptop-docker >/dev/null ;;
    *)
      docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
        -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_HUB_WAIT="$([ -n "$RELAY" ] && echo 1)" \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        l18-laptop bash /capture/run_steps.sh /out "$SEG" ;;
  esac
done
