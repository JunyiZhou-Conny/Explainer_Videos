#!/bin/bash
# Re-capture the L23 terminal transcripts (needs Docker and privileged containers):
#   bash assets/terminal/capture.sh setup
#   bash assets/terminal/capture.sh pre secrets shell-a shell-b shell-c toolbox playbooks ci extras
#   bash assets/terminal/capture.sh teardown          # removes the laptop, its Docker volume, the relay
# Each segment is one call of run_steps.sh (see its header); the laptop container persists between
# calls, so the capture can run in parts (one segment per call keeps each call short).
#
# "laptop": a Linux laptop with Docker Engine, the machine README.md:74-147 runs on (the README's
#   `secrets/` folder sits next to the clone, README.md:55-60). A privileged ubuntu:24.04 container
#   in its own network namespace (never --network host), with Docker Engine from Docker's own apt
#   repository (docker-ce, docker-ce-cli, containerd.io, docker-buildx-plugin) and nothing of the
#   tutorial preinstalled: user `student` (in the docker group), bash, git, curl, python3 (for
#   ptyrun.py and one JSON check), openssh-client (for the throwaway key pair, see below). There is
#   no systemd in a container, so setup starts dockerd by hand (capture-only); on a laptop the
#   service or Docker Desktop does it. On Ubuntu, as on Debian, /bin/sh is dash (README.md:77 runs
#   `sh docker-shell.sh`; on macOS /bin/sh is bash).
# There is NO AWS account, NO access key, NO EC2 instance and NO GitHub Actions run here (ASSETS.md,
#   "What cannot run here"): ~/secrets holds a CSV with obviously fake placeholder keys that AWS
#   rejects, and a throwaway RSA key generated at capture time for no account (never written to the
#   repository). Every AWS call stops at AWS's own answer to those keys.
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l23-relay) makes the proxy reachable from Docker's bridge network, the laptop's apt, curl, git,
# Docker daemon and Docker CLI get it, and the CA is added to the laptop's bundle and baked into a
# capture-only re-tag of the toolbox's base image ubuntu:20.04 (ASSETS.md, "capture-only"). Docker
# Hub pulls go through mirror.gcr.io (--registry-mirror): the sandbox's shared IPs hit Docker Hub's
# anonymous rate limit.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RPORT=38723
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l23-relay; then
    docker rm -f l23-relay >/dev/null 2>&1 || true
    docker run -d --name l23-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" $RPORT "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:$RPORT
  for i in $(seq 30); do   # wait until the relay listens
    docker exec l23-relay python -c "import socket; socket.create_connection(('$GW', $RPORT), timeout=2).close()" >/dev/null 2>&1 && break
    sleep 1
  done
fi
PROXY_JSON=
[ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"
PXENV=(-e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX)
DEST="$HERE/laptop"; mkdir -p "$DEST"

for SEG in "$@"; do
  case $SEG in
    setup)
      docker rm -f l23-laptop >/dev/null 2>&1 || true
      docker volume rm l23-laptop-docker >/dev/null 2>&1 || true
      docker run -d --privileged --name l23-laptop --hostname laptop \
        -v l23-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
        "${PXENV[@]}" ubuntu:24.04 sleep infinity >/dev/null
      docker exec -e PROXY_JSON="$PROXY_JSON" l23-laptop bash -c '
        set -e
        # capture-only: the proxy CA and https apt sources (the sandbox refuses plain http)
        mkdir -p /usr/local/share/ca-certificates /etc/ssl/certs
        cp /ca.crt /usr/local/share/ca-certificates/capture-ca.crt
        cat /ca.crt >> /etc/ssl/certs/ca-certificates.crt
        sed -i -e "s|http://archive.ubuntu.com|https://archive.ubuntu.com|g" -e "s|http://security.ubuntu.com|https://security.ubuntu.com|g" /etc/apt/sources.list.d/ubuntu.sources
        # the laptop baseline (not part of the tutorial)
        apt-get update -qq >/dev/null
        DEBIAN_FRONTEND=noninteractive apt-get install -y -qq ca-certificates curl gnupg git python3 openssh-client sudo >/dev/null 2>&1
        update-ca-certificates >/dev/null 2>&1
        # Docker Engine, as https://docs.docker.com/engine/install/ubuntu/ installs it
        install -m 0755 -d /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
        chmod a+r /etc/apt/keyrings/docker.asc
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo $VERSION_CODENAME) stable" > /etc/apt/sources.list.d/docker.list
        apt-get update -qq >/dev/null
        DEBIAN_FRONTEND=noninteractive apt-get install -y -qq docker-ce docker-ce-cli containerd.io docker-buildx-plugin >/dev/null 2>&1
        rm -rf /var/lib/apt/lists/*
        # capture-only: no systemd in a container, so dockerd is started by hand
        (setsid dockerd --registry-mirror=https://mirror.gcr.io > /var/log/dockerd.log 2>&1 &)
        for i in $(seq 60); do docker info >/dev/null 2>&1 && break; sleep 1; done
        useradd -m -s /bin/bash student && usermod -aG docker student
        mkdir -p /home/student/.docker
        [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
        chown -R student:student /home/student; chmod 777 /out' ;;
    teardown)
      docker rm -f l23-laptop >/dev/null 2>&1 || true
      docker volume rm l23-laptop-docker >/dev/null 2>&1 || true
      docker rm -f l23-relay >/dev/null 2>&1 || true ;;
    *)
      # dockerd does not survive a restart of the laptop container: start it again if needed
      docker exec l23-laptop bash -c 'docker info >/dev/null 2>&1 || { (setsid dockerd --registry-mirror=https://mirror.gcr.io > /var/log/dockerd.log 2>&1 &); for i in $(seq 60); do docker info >/dev/null 2>&1 && break; sleep 1; done; }'
      docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
        -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" "${PXENV[@]}" \
        l23-laptop bash /capture/run_steps.sh /out "$SEG" || true ;;
  esac
done
