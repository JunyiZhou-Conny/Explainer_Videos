#!/bin/bash
# Re-capture the L20 terminal transcripts (needs Docker and privileged containers).
#   bash assets/terminal/capture.sh relay vm-setup vm1 vm-dockerd vm2 vm-teardown
#   bash assets/terminal/capture.sh relay laptop-setup pre partA partB laptop-teardown
#   docker rm -f l20-relay
# Each segment is one call of run_steps.sh (see its header); the containers persist between calls, so
# the capture can run in parts.
#
# "vm": a privileged debian:12 container (its own network namespace, never --network host) stands in
#   for the README's Compute Engine VM ("select all the default values": Debian 12 bookworm). It gets
#   the baseline a GCP Debian image already has (sudo, curl, python3, ca-certificates, a console-SSH
#   user with passwordless sudo, here called `student`) and nothing else: Docker comes from the
#   README's own get-docker.sh. There is no systemd in a container, so after get-docker.sh the
#   segment vm-dockerd starts dockerd by hand (capture-only, see ASSETS.md); on a VM systemd does it.
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind) stands in for the student's laptop with
#   Docker Desktop: user `student` in the docker group, bash, git, curl, python3, openssl. Its home
#   folder is the README's parent folder (cheese-app-v3/ and secrets/ side by side, as
#   src/deployment/docker-shell.sh:9 expects). Every docker-shell.sh / docker-hub.sh and every Pulumi
#   command runs here: repository code never runs on the recording host.
# There are NO GCP credentials and no Docker Hub login (ASSETS.md, "What cannot run here"): the key
#   files in the laptop's secrets/ are well-formed files around throwaway keys generated at capture
#   time for no account (never written to the repository).
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l20-relay) makes the proxy reachable from Docker's bridge network, and the CA is added to each
# machine's bundle and baked into capture-only re-tags of base images (ASSETS.md, "capture-only").
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RPORT=38720
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  RELAY=http://$GW:$RPORT
fi
# Series rule: the instructor's name never appears in a capture. run_steps.sh masks it; the name is
# read here from the tutorial's own page at run time, so it is written nowhere in this repository.
if [ -z "$NAME_RE" ]; then
  FULL=$(curl -s https://raw.githubusercontent.com/dlops-io/cheese-app-v3/3ecef56fea879ac480d260c0906cd95baf05179a/src/frontend-simple/index.html \
    | grep -o 'My name is [A-Z][a-z]* [A-Z][a-z]*' | head -1 | cut -d' ' -f4-)
  [ -n "$FULL" ] && NAME_RE="${FULL}|${FULL%% *}|${FULL##* }"
fi
export NAME_RE
mkdir -p "$HERE/vm" "$HERE/laptop"

for SEG in "$@"; do
  case $SEG in
    relay)
      [ -n "$HTTPS_PROXY" ] || continue
      PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
      if ! docker ps --format '{{.Names}}' | grep -qx l20-relay; then
        docker rm -f l20-relay >/dev/null 2>&1 || true
        docker run -d --name l20-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
          python:3.12-slim-bookworm python /proxy_relay.py "$GW" $RPORT "$PHOST" "$PPORT" >/dev/null
      fi
      for i in $(seq 30); do
        docker exec l20-relay python -c "import socket; socket.create_connection(('$GW', $RPORT), timeout=2).close()" >/dev/null 2>&1 && break
        sleep 1
      done ;;
    vm-setup)
      docker rm -f l20-vm >/dev/null 2>&1 || true
      docker volume rm l20-vm-docker >/dev/null 2>&1 || true
      docker run -d --privileged --name l20-vm --hostname cheese-app-vm \
        -v l20-vm-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$HERE/../source":/source:ro -v "$HERE/vm":/out -v "$CA":/ca.crt:ro \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        debian:12 sleep infinity >/dev/null
      docker exec l20-vm bash -c '
        set -e
        # the baseline of a GCP Debian 12 image (not part of the tutorial): https apt sources (the
        # proxy refuses plain http), the proxy CA, sudo, curl, python3 (ptyrun.py), procps, and the
        # console-SSH user with passwordless sudo
        sed -i "s|http://deb.debian.org|https://deb.debian.org|g" /etc/apt/sources.list.d/debian.sources
        cp /ca.crt /tmp/ca.crt
        apt-get -o Acquire::https::CAInfo=/tmp/ca.crt update -qq >/dev/null
        DEBIAN_FRONTEND=noninteractive apt-get -o Acquire::https::CAInfo=/tmp/ca.crt install -y -qq sudo curl ca-certificates python3 procps >/dev/null 2>&1
        cp /ca.crt /usr/local/share/ca-certificates/capture-proxy.crt && update-ca-certificates >/dev/null 2>&1
        rm -rf /var/lib/apt/lists/*
        useradd -m -s /bin/bash student && echo "student ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/student
        echo "Defaults env_keep += \"https_proxy HTTPS_PROXY no_proxy NO_PROXY\"" >> /etc/sudoers.d/student
        chmod 440 /etc/sudoers.d/student; chmod 755 /home/student; chmod 777 /out' ;;
    vm-dockerd)
      # capture-only: a VM starts dockerd with systemd right after get-docker.sh; a container has no
      # systemd, so start it by hand, with the recording proxy for pulls, Docker's classic image store
      # (the recording disk could not hold the images twice; ASSETS.md) and, for root's docker client
      # (the README runs `sudo docker`), the proxy for the containers it starts.
      docker exec -e RELAY="$RELAY" l20-vm bash -c '
        mkdir -p /etc/docker /root/.docker
        echo "{\"features\":{\"containerd-snapshotter\":false}}" > /etc/docker/daemon.json
        [ -n "$RELAY" ] && echo "{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"localhost,127.0.0.1\"}}}" > /root/.docker/config.json
        (setsid dockerd > /var/log/dockerd.log 2>&1 &)
        for i in $(seq 60); do docker info >/dev/null 2>&1 && break; sleep 1; done
        docker info --format "dockerd {{.ServerVersion}} up, storage {{.Driver}}"' ;;
    vm-teardown)
      docker rm -f l20-vm >/dev/null; docker volume rm l20-vm-docker >/dev/null ;;
    vm[0-9]*)
      docker exec -u student -w /home/student -e HOME=/home/student -e USER=student -e NAME_RE \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" \
        l20-vm bash /capture/run_steps.sh /out "$SEG" ;;
    laptop-setup)
      docker rm -f l20-laptop >/dev/null 2>&1 || true
      docker volume rm l20-laptop-docker >/dev/null 2>&1 || true
      PROXY_JSON=
      [ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"
      docker run -d --privileged --name l20-laptop --hostname laptop \
        -v l20-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$HERE/../source":/source:ro -v "$HERE/laptop":/out -v "$CA":/ca.crt:ro \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        --entrypoint sh docker:29.8.2-dind -c '
          cp /ca.crt /etc/ssl/certs/ca-certificates.crt
          mkdir -p /etc/docker && echo "{\"features\":{\"containerd-snapshotter\":false}}" > /etc/docker/daemon.json
          exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
      docker exec -e PROXY_JSON="$PROXY_JSON" l20-laptop sh -c '
        set -e
        until docker info >/dev/null 2>&1; do sleep 1; done
        # the laptop baseline (not part of the tutorial): bash, git, curl, python3, openssl, and a
        # user in the docker group; Docker client proxy settings (capture-only) pass the recording
        # proxy to the builds and containers the tutorial starts
        apk add --no-cache -q bash python3 git curl openssl >/dev/null
        adduser -D -s /bin/bash -u 1000 student && addgroup student docker
        mkdir -p /home/student/.docker
        [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
        chown -R student:student /home/student; chmod 777 /out' ;;
    laptop-teardown)
      docker rm -f l20-laptop >/dev/null; docker volume rm l20-laptop-docker >/dev/null ;;
    *)
      docker exec -u student -w /home/student -e HOME=/home/student -e USER=student -e NAME_RE \
        -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_RELAY="$RELAY" \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        l20-laptop bash /capture/run_steps.sh /out "$SEG" ;;
  esac
done
