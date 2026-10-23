#!/bin/bash
# Re-capture the L11 terminal transcripts (needs Docker and privileged containers):
#   bash assets/terminal/capture.sh laptop setup
#   bash assets/terminal/capture.sh laptop pre ls1 ls2 cli cmp aclean
#   bash assets/terminal/capture.sh laptop b-pre b-build b-v20 b-git20 b-v21 b-git21 b-up
#   bash assets/terminal/capture.sh laptop t-repo t-dvc bclean
#   bash assets/terminal/capture.sh laptop teardown
#   bash assets/terminal/capture.sh colab run
# Containers persist between calls, so a long capture can run in parts; `teardown` removes them.
#
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind) stands in for the student's machine
#   with Docker Desktop: user `student` in the docker group, bash, python3 (for ptyrun.py), git
#   (identity `student <student@example.com>`), curl, GNU sed, tree, unzip, an ssh client. There
#   are NO GCP credentials in this environment: ~/secrets holds an obviously-invalid placeholder key
#   for the folder-structure steps and is emptied before the cloud steps, so every Google call fails
#   with its documented missing-key error (see ASSETS.md, "What cannot run here").
# "colab": a python:3.12-slim-bookworm container (+ git, + the proxy CA; root in /content, like a
#   Colab runtime) stands in for Colab with no Google sign-in, for the notebook's `dvc` cells.
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l11-relay) makes the proxy reachable from Docker's bridge network, and the CA replaces the
# containers' bundles and is baked into capture-only re-tags of the base images
# (python:3.12-slim-bookworm, python:3.11-slim-bookworm) as ASSETS.md describes ("capture-only").
# Remove the relay with `docker rm -f l11-relay` when done.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
MODE=$1; shift
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1,data-label-studio
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l11-relay; then
    docker rm -f l11-relay >/dev/null 2>&1 || true
    docker run -d --name l11-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38695 "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:38695
  for i in $(seq 30); do   # wait until the relay listens, or the first apt/git call races it
    docker exec l11-relay python -c "import socket; socket.create_connection(('$GW', 38695), timeout=2).close()" >/dev/null 2>&1 && break
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
        docker rm -f l11-laptop >/dev/null 2>&1 || true
        docker volume rm l11-laptop-docker >/dev/null 2>&1 || true
        docker run -d --privileged --name l11-laptop --hostname laptop \
          -v l11-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
          -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
          --entrypoint sh docker:29.8.2-dind -c '
            cp /ca.crt /etc/ssl/certs/ca-certificates.crt
            exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
        docker exec -e PROXY_JSON="$PROXY_JSON" l11-laptop sh -c '
          set -e
          until docker info >/dev/null 2>&1; do sleep 1; done
          # the laptop baseline (not part of the tutorial): bash, git, curl, GNU sed, tree, unzip,
          # an ssh client, sudo (a Linux user would have it), python3 (for ptyrun.py), and a user in the docker group whose git
          # identity is already set (digest gotcha #4: set it before the first DVC container run).
          # The docker:dind image already ships the compose plugin, as Docker Desktop does.
          apk add --no-cache -q bash python3 git curl sed tree unzip openssh-client-default sudo >/dev/null
          echo "student ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/student && chmod 440 /etc/sudoers.d/student
          adduser -D -s /bin/bash student && addgroup student docker
          mkdir -p /home/student/.docker
          [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
          su student -c "git config --global user.name student && git config --global user.email student@example.com"
          chown -R student:student /home/student; chmod 777 /out' ;;
      teardown)
        docker rm -f l11-laptop >/dev/null; docker volume rm l11-laptop-docker >/dev/null ;;
      *)
        docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
          -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_HUB_WAIT="$([ -n "$RELAY" ] && echo 1)" \
          -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
          -e GIT_SSH_COMMAND="ssh -o ConnectTimeout=15 -o BatchMode=yes" \
          l11-laptop bash /capture/run_steps.sh /out "$SEG" ;;
    esac
  done
elif [ "$MODE" = colab ]; then
  DEST="$HERE/colab"; mkdir -p "$DEST"; chmod 777 "$DEST"
  # capture-only image: Colab's Python 3.12 + git + the recording proxy's CA (Colab itself needs none)
  D=$(mktemp -d); cp "$CA" "$D/capture-ca.crt"
  cat > "$D/Dockerfile" <<'EOF'
FROM python:3.12-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
 && apt-get update -qq && apt-get install -y -qq --no-install-recommends git >/dev/null \
 && mkdir /content
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt GIT_SSL_CAINFO=/etc/ssl/certs/ca-certificates.crt
WORKDIR /content
EOF
  mkdir -p "$DEST/capture-only"; cp "$D/Dockerfile" "$DEST/capture-only/colab-standin.Dockerfile"
  docker build --network host --build-arg HTTPS_PROXY="$HTTPS_PROXY" --build-arg https_proxy="$HTTPS_PROXY" \
    -t l11-colab-standin "$D" > "$DEST/capture-only/colab-standin-build.txt" 2>&1
  rm -rf "$D"
  docker run --rm --name l11-colab -v "$HERE":/capture:ro -v "$DEST":/out \
    -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
    l11-colab-standin bash /capture/run_steps.sh /out colab
else
  echo "usage: capture.sh laptop setup|<segment>...|teardown  |  capture.sh colab run" >&2; exit 2
fi
