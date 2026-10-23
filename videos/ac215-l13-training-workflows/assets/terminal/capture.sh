#!/bin/bash
# Re-capture the L13 terminal transcripts (needs Docker and privileged containers):
#   bash assets/terminal/capture.sh laptop setup
#   bash assets/terminal/capture.sh laptop pre cloud wandb shell pkg job mgpu clipy nokey vtx clean
#   (`bases` alone re-tags the capture-only base images; `pre` already does it)
#   bash assets/terminal/capture.sh laptop teardown
#   bash assets/terminal/capture.sh colab run
# The laptop container persists between calls, so a long capture can run in parts; `teardown`
# removes it.
#
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind) stands in for the student's machine
#   with Docker Desktop: user `student` in the docker group, bash, python3 (for ptyrun.py), git,
#   curl, GNU sed, tree, sudo. There are NO GCP credentials and NO W&B account in this environment:
#   ~/secrets holds an obviously-invalid placeholder key for the folder-structure steps and is
#   emptied before the container steps, and WANDB_KEY is an obviously fake 40-character placeholder,
#   so every Google call fails with its documented missing-key error (ASSETS.md, "What cannot run
#   here"). The laptop's own engine also runs the "Vertex stand-in" (segment vtx): Google's step
#   "pip install the package" in a python:3.10 container, then W&B's login check, offline.
# "colab": a python:3.12-slim-bookworm container (+ the proxy CA; root in /content, like a Colab
#   runtime) stands in for Colab with no Google sign-in and no GPU, for notebook B's `pip install
#   wandb` cell and an offline check of its `wandb.config = {...}` pattern.
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l13-relay) makes the proxy reachable from Docker's bridge network, and the CA replaces the
# containers' bundles and is baked into capture-only re-tags of the base images
# (python:3.13-slim-bullseye, python:3.10-slim-bookworm) as ASSETS.md describes ("capture-only").
# Remove the relay with `docker rm -f l13-relay` when done.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
MODE=$1; shift
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RPORT=38713
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l13-relay; then
    docker rm -f l13-relay >/dev/null 2>&1 || true
    docker run -d --name l13-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" $RPORT "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:$RPORT
  for i in $(seq 30); do   # wait until the relay listens, or the first apt/git call races it
    docker exec l13-relay python -c "import socket; socket.create_connection(('$GW', $RPORT), timeout=2).close()" >/dev/null 2>&1 && break
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
        docker rm -f l13-laptop >/dev/null 2>&1 || true
        docker volume rm l13-laptop-docker >/dev/null 2>&1 || true
        docker run -d --privileged --name l13-laptop --hostname laptop \
          -v l13-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
          -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
          --entrypoint sh docker:29.8.2-dind -c '
            cp /ca.crt /etc/ssl/certs/ca-certificates.crt
            exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
        docker exec -e PROXY_JSON="$PROXY_JSON" l13-laptop sh -c '
          set -e
          until docker info >/dev/null 2>&1; do sleep 1; done
          # the laptop baseline (not part of the tutorial): bash, git, curl, GNU sed, tree, sudo,
          # python3 (for ptyrun.py and two JSON one-liners), and a user in the docker group.
          apk add --no-cache -q bash python3 git curl sed tree sudo >/dev/null
          echo "student ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/student && chmod 440 /etc/sudoers.d/student
          adduser -D -s /bin/bash student && addgroup student docker
          mkdir -p /home/student/.docker
          [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
          chown -R student:student /home/student; chmod 777 /out' ;;
      teardown)
        docker rm -f l13-laptop >/dev/null; docker volume rm l13-laptop-docker >/dev/null ;;
      *)
        docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
          -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_HUB_WAIT="$([ -n "$RELAY" ] && echo 1)" \
          -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
          l13-laptop bash /capture/run_steps.sh /out "$SEG" ;;
    esac
  done
elif [ "$MODE" = colab ]; then
  DEST="$HERE/colab"; mkdir -p "$DEST"; chmod 777 "$DEST"
  # capture-only image: Colab's Python 3.12 + the recording proxy's CA (Colab itself needs none)
  D=$(mktemp -d); cp "$CA" "$D/capture-ca.crt"
  cat > "$D/Dockerfile" <<'EOF'
FROM python:3.12-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && mkdir /content
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
WORKDIR /content
EOF
  mkdir -p "$DEST/capture-only"; cp "$D/Dockerfile" "$DEST/capture-only/colab-standin.Dockerfile"
  docker build --network host --build-arg HTTPS_PROXY="$HTTPS_PROXY" --build-arg https_proxy="$HTTPS_PROXY" \
    -t l13-colab-standin "$D" > "$DEST/capture-only/colab-standin-build.txt" 2>&1
  rm -rf "$D"
  docker run --rm --name l13-colab -v "$HERE":/capture:ro -v "$DEST":/out \
    -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
    l13-colab-standin bash /capture/run_steps.sh /out colab
else
  echo "usage: capture.sh laptop setup|<segment>...|teardown  |  capture.sh colab run" >&2; exit 2
fi
