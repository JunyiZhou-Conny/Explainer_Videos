#!/bin/bash
# Re-capture the L22 terminal transcripts (needs Docker and privileged containers).
#   bash assets/terminal/capture.sh relay laptop-setup pre tb-commit tb-shell tb-wait tb-readme tb-local \
#        kind-up kind-readme kind-extra kind-down tb-close laptop-teardown
#   docker rm -f l22-relay
# Each segment is one call of run_steps.sh (see its header); the containers persist between calls, so
# the capture can run in parts.
#
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind) stands in for the student's laptop with
#   Docker Desktop: user `student` in the docker group, bash, git, curl, python3, openssl. Its home
#   folder is the README's parent folder (cheese-app-v3/ and secrets/ side by side, as
#   src/deployment/docker-shell.sh:9 expects). `sh docker-shell.sh` and every gcloud / Pulumi / kubectl
#   command of the README runs here, in the deployment container it starts: repository code never
#   runs on the recording host.
# "kind": a LABELLED STAND-IN for the GKE cluster. kind (Kubernetes IN Docker, v0.31.0, node image
#   kindest/node:v1.34.11) makes a 3-node cluster (1 control plane + 2 workers, like the README's
#   `--num-nodes 2`) inside the laptop's Docker engine, with no cloud account. The deployment
#   container joins kind's Docker network and gets kind's kubeconfig (capture-only), so the README's
#   kubectl commands run unchanged, from the same toolbox, against a real API server. It is NOT GKE:
#   no node pools, no autoscaler, no cloud load balancer (a LoadBalancer Service stays <pending>).
# There are NO GCP credentials (ASSETS.md, "What cannot run here"): the key file in the laptop's
#   secrets/ is a well-formed file around a throwaway key generated at capture time for no account
#   (never written to the repository). Every Google call fails at its first real request.
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l22-relay) makes the proxy reachable from Docker's bridge network, and the CA is added to each
# machine's bundle and baked into capture-only re-tags of base images (ASSETS.md, "capture-only").
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RPORT=38722
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
mkdir -p "$HERE/laptop" "$HERE/kind"

for SEG in "$@"; do
  case $SEG in
    relay)
      [ -n "$HTTPS_PROXY" ] || continue
      PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
      if ! docker ps --format '{{.Names}}' | grep -qx l22-relay; then
        docker rm -f l22-relay >/dev/null 2>&1 || true
        docker run -d --name l22-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
          python:3.12-slim-bookworm python /proxy_relay.py "$GW" $RPORT "$PHOST" "$PPORT" >/dev/null
      fi
      for i in $(seq 30); do
        docker exec l22-relay python -c "import socket; socket.create_connection(('$GW', $RPORT), timeout=2).close()" >/dev/null 2>&1 && break
        sleep 1
      done ;;
    laptop-setup)
      docker rm -f l22-laptop >/dev/null 2>&1 || true
      docker volume rm l22-laptop-docker >/dev/null 2>&1 || true
      PROXY_JSON=
      [ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"
      docker run -d --privileged --name l22-laptop --hostname laptop \
        -v l22-laptop-docker:/var/lib/docker -v /lib/modules:/lib/modules:ro \
        -v "$HERE":/capture:ro -v "$HERE/../source":/source:ro -v "$HERE/laptop":/out -v "$HERE/kind":/out-kind -v "$CA":/ca.crt:ro \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        --entrypoint sh docker:29.8.2-dind -c '
          cp /ca.crt /etc/ssl/certs/ca-certificates.crt
          mkdir -p /etc/docker && echo "{\"features\":{\"containerd-snapshotter\":false}}" > /etc/docker/daemon.json
          exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
      docker exec -e PROXY_JSON="$PROXY_JSON" l22-laptop sh -c '
        set -e
        until docker info >/dev/null 2>&1; do sleep 1; done
        # the laptop baseline (not part of the tutorial): bash, git, curl, python3, openssl, a user in
        # the docker group, and the kind CLI for the stand-in cluster; Docker client proxy settings
        # (capture-only) pass the recording proxy to the builds and containers the tutorial starts
        apk add --no-cache -q bash python3 git curl openssl >/dev/null
        curl -fsSL -o /usr/local/bin/kind https://kind.sigs.k8s.io/dl/v0.31.0/kind-linux-amd64
        chmod 755 /usr/local/bin/kind
        adduser -D -s /bin/bash -u 1000 student && addgroup student docker
        mkdir -p /home/student/.docker
        [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
        chown -R student:student /home/student; chmod 777 /out /out-kind' ;;
    laptop-teardown)
      docker rm -f l22-laptop >/dev/null; docker volume rm l22-laptop-docker >/dev/null ;;
    tb-shell)
      # detached: the toolbox shell stays open while the next segments type commands into it
      docker exec -d -u student -w /home/student -e HOME=/home/student -e USER=student -e NAME_RE \
        -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_RELAY="$RELAY" \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        l22-laptop bash /capture/run_steps.sh /out "$SEG" ;;
    kind*)
      docker exec -u student -w /home/student -e HOME=/home/student -e USER=student -e NAME_RE \
        -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_RELAY="$RELAY" \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        l22-laptop bash /capture/run_steps.sh /out-kind "$SEG" ;;
    *)
      docker exec -u student -w /home/student -e HOME=/home/student -e USER=student -e NAME_RE \
        -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_RELAY="$RELAY" \
        -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
        l22-laptop bash /capture/run_steps.sh /out "$SEG" ;;
  esac
done
