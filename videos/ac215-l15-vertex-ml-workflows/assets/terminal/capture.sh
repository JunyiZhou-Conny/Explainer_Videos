#!/bin/bash
# Re-capture the L15 terminal transcripts (needs Docker and privileged containers):
#   bash assets/terminal/capture.sh setup
#   bash assets/terminal/capture.sh pre md-setup md-shell md-local md-clean
#   bash assets/terminal/capture.sh mw-setup mw-coll mw-proc mw-train mw-push mw-flow mw-end
#   bash assets/terminal/capture.sh teardown
# The laptop's Docker storage is a 9 GB tmpfs (capture-only: the sandbox's disk is too small for
# the unpinned `pipenv lock` of model-deployment-aws, which downloads several GB while it
# backtracks; see ASSETS.md). The laptop container persists between calls, so a long capture can run in parts (one segment
# per call keeps each call short); `teardown` removes it and its Docker volume.
#
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind, x86_64) stands in for the student's
#   machine with Docker: user `student` (uid 1000) in the docker group, bash, git, curl, GNU sed,
#   tree, python3 (for ptyrun.py) and the AWS CLI v2 from Alpine's package manager (README
#   ml-workflow-aws:51-53 "Install AWS CLI"). There is NO AWS account, NO access key and NO
#   SageMaker here (ASSETS.md, "What cannot run here"): the model-deployment part runs with
#   `aws configure` left without keys; the ml-workflow part, whose docker-shell.sh scripts refuse
#   to start without a key, gets obviously fake placeholder keys that AWS rejects.
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l15-relay) makes the proxy reachable from Docker's bridge network, the laptop engine and its
# containers get it through ~/.docker/config.json's `proxies`, and the CA is baked into
# capture-only re-tags of the tutorial's base images (ubuntu:20.04, python:3.11-slim), as
# ASSETS.md describes ("capture-only"). Remove the relay with `docker rm -f l15-relay` when done.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RPORT=38715
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l15-relay; then
    docker rm -f l15-relay >/dev/null 2>&1 || true
    docker run -d --name l15-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" $RPORT "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:$RPORT
  for i in $(seq 30); do   # wait until the relay listens, or the first apk/git call races it
    docker exec l15-relay python -c "import socket; socket.create_connection(('$GW', $RPORT), timeout=2).close()" >/dev/null 2>&1 && break
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
      docker rm -f l15-laptop >/dev/null 2>&1 || true
      docker volume rm l15-laptop-docker >/dev/null 2>&1 || true
      docker run -d --privileged --name l15-laptop --hostname laptop \
        --tmpfs /var/lib/docker:rw,exec,suid,dev,size=9g -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
        "${PXENV[@]}" --entrypoint sh docker:29.8.2-dind -c '
          cp /ca.crt /etc/ssl/certs/ca-certificates.crt
          # capture-only: the classic overlay2 store keeps each image once (unpacked), not twice
          # (compressed + unpacked) as the containerd store does; the sandbox disk is small
          mkdir -p /etc/docker && echo "{\"features\": {\"containerd-snapshotter\": false}}" > /etc/docker/daemon.json
          exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
      docker exec -e PROXY_JSON="$PROXY_JSON" l15-laptop sh -c '
        set -e
        until docker info >/dev/null 2>&1; do sleep 1; done
        # the laptop baseline (not part of the tutorial): bash, git, curl, GNU sed, tree, python3
        # (for ptyrun.py), the AWS CLI, and a user in the docker group. Docker client proxy
        # settings (capture-only) pass the recording proxy to the builds and containers.
        apk add --no-cache -q bash python3 git curl sed tree aws-cli >/dev/null
        adduser -D -u 1000 -s /bin/bash student && addgroup student docker
        mkdir -p /home/student/.docker
        [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
        chown -R student:student /home/student; chmod 777 /out' ;;
    teardown)
      docker rm -f l15-laptop >/dev/null; docker volume rm l15-laptop-docker >/dev/null 2>&1 || true ;;
    *)
      # capture-only watchdog: the recording sandbox's disk is shared with other jobs; stop this
      # segment's builds if free space drops below 1.5 GB (noted in capture-only/disk-watchdog.txt)
      ( while sleep 5; do
          docker inspect l15-laptop >/dev/null 2>&1 || exit 0
          [ "$(df --output=avail -k / | tail -1)" -gt 1572864 ] && continue
          mkdir -p "$DEST/capture-only"; echo "$(date -u +%FT%TZ) $SEG: free disk < 1.5 GB, builds stopped" >> "$DEST/capture-only/disk-watchdog.txt"
          docker exec l15-laptop sh -c 'pkill -f "buildx build"; pkill -f "docker build"' ; done ) &
      WD=$!
      docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
        -e AWS_CA_BUNDLE="$([ -n "$RELAY" ] && echo /etc/ssl/certs/ca-certificates.crt)" \
        -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_HUB_WAIT="$([ -n "$RELAY" ] && echo 1)" \
        "${PXENV[@]}" l15-laptop bash /capture/run_steps.sh /out "$SEG" || true
      kill $WD 2>/dev/null; wait $WD 2>/dev/null || true ;;
  esac
done
