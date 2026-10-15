#!/bin/bash
# Re-capture the terminal transcripts (needs Docker and privileged containers):
#   bash assets/terminal/capture.sh laptop                       -> laptop/
#   bash assets/terminal/capture.sh laptop-push                  -> laptop-push/  (tag/push extras)
#   bash assets/terminal/capture.sh vm debian:12 vm-debian12     -> vm-debian12/
#   bash assets/terminal/capture.sh vm debian:13 vm-debian13     -> vm-debian13/
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind) stands in for Docker Desktop, so
#   `docker system prune` and `docker image ls` see a clean machine and touch nothing of yours.
# "vm": a fresh Debian container stands in for the Compute Engine VM, given the baseline a GCP
#   Debian image has (python3, sudo, curl, a user with passwordless sudo, called `student`); it is
#   privileged only so that the Docker engine the README installs can run inside it.
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py makes the proxy
# reachable from Docker's bridge network, and the CA is added as ASSETS.md describes. The relay
# container (l02-relay) is reused by later runs; remove it with `docker rm -f l02-relay` when done.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
MODE=$1
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l02-relay; then
    docker rm -f l02-relay >/dev/null 2>&1 || true
    docker run -d --name l02-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38692 "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:38692
fi
PROXY_JSON=
[ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"

if [ "$MODE" = laptop ] || [ "$MODE" = laptop-push ]; then
  DEST="$HERE/$MODE"; mkdir -p "$DEST"
  docker rm -f l02-laptop >/dev/null 2>&1 || true
  docker volume rm l02-laptop-docker >/dev/null 2>&1 || true
  docker run -d --privileged --name l02-laptop --hostname laptop \
    -v l02-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
    -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
    --entrypoint sh docker:29.8.2-dind -c '
      cp /ca.crt /etc/ssl/certs/ca-certificates.crt
      exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
  docker exec -e PROXY_JSON="$PROXY_JSON" l02-laptop sh -c '
    set -e
    until docker info >/dev/null 2>&1; do sleep 1; done
    # the laptop baseline (not part of the tutorial): bash, python3 (for ptyrun.py), htpasswd for
    # the throwaway local registry of the push extras, and a user in the docker group
    apk add --no-cache -q bash python3 curl apache2-utils >/dev/null
    adduser -D -s /bin/bash student && addgroup student docker
    mkdir -p /home/student/.docker /home/student/registry-auth
    htpasswd -Bbn student not-a-real-token > /home/student/registry-auth/htpasswd
    [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
    chown -R student:student /home/student; chmod 777 /out'
  if [ "$MODE" = laptop-push ] && docker image inspect python:3.12-slim-bookworm >/dev/null 2>&1; then
    # capture-only: seed the base image from this machine (Docker Hub limits anonymous pulls)
    docker save python:3.12-slim-bookworm | docker exec -i l02-laptop docker load -q >/dev/null
  fi
  docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
    -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_HUB_WAIT="$([ -n "$RELAY" ] && echo 1)" \
    -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
    l02-laptop bash /capture/run_steps.sh /out "${MODE#laptop-}"
  docker rm -f l02-laptop >/dev/null; docker volume rm l02-laptop-docker >/dev/null
elif [ "$MODE" = vm ]; then
  IMG=$2; DEST="$HERE/$3"; mkdir -p "$DEST"
  VOL=l02-$3-docker
  docker volume rm "$VOL" >/dev/null 2>&1 || true
  docker run --rm --privileged --name "l02-$3" -v "$VOL":/var/lib/docker \
    -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
    -e https_proxy="$RELAY" -e HTTPS_PROXY="$RELAY" -e no_proxy=$NOPX -e NO_PROXY=$NOPX \
    -e PROXY_JSON="$PROXY_JSON" -e CAPTURE_HUB_WAIT="$([ -n "$RELAY" ] && echo 1)" "$IMG" bash -c '
set -e
# the baseline of a GCP Debian image (not part of the tutorial): https apt sources, CA bundle,
# python3, sudo, curl, and a user with passwordless sudo, like the console-SSH user
mkdir -p /etc/ssl/certs && cp /ca.crt /etc/ssl/certs/ca-certificates.crt
sed -i "s|http://deb.debian.org|https://deb.debian.org|g" /etc/apt/sources.list.d/debian.sources
CAOPT="-o Acquire::https::CaInfo=/etc/ssl/certs/ca-certificates.crt"   # Debian 13 apt has no default CA path yet
apt-get update -qq $CAOPT >/dev/null && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq $CAOPT python3 sudo curl ca-certificates >/dev/null 2>&1
cp /ca.crt /etc/ssl/certs/ca-certificates.crt
rm -rf /var/lib/apt/lists/*
useradd -m -s /bin/bash student && echo "student ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/student
echo "Defaults env_keep += \"https_proxy HTTPS_PROXY no_proxy NO_PROXY\"" >> /etc/sudoers.d/student
for h in /root /home/student; do mkdir -p $h/.docker; [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > $h/.docker/config.json; done
chown -R student:student /home/student/.docker
chmod 777 /out
su - student -w https_proxy,HTTPS_PROXY,no_proxy,NO_PROXY,CAPTURE_HUB_WAIT -c "bash /capture/run_steps.sh /out vm"
'
  docker volume rm "$VOL" >/dev/null 2>&1 || true
fi
