#!/bin/bash
# Re-capture the L04 terminal transcripts. Needs Docker with privileged containers, and python3 with `pyte`
# (pip install pyte; set PYTHON to it) so the live progress views of docker build / docker compose render.
#   bash assets/terminal/capture.sh port        -> port-laptop/   (dlops-io/port_toy, the whole README)
#   bash assets/terminal/capture.sh mega        -> mega-laptop/   (dlops-io/mega-pipeline, branch flexible-workflow)
#   bash assets/terminal/capture.sh gcloud      -> gcloud-laptop/ (the README's two gcloud commands, no account)
#
# "Your laptop" is a fresh, empty Docker engine standing in for Docker Desktop: a docker:29.8.2-dind container
# (its own network namespace, so `localhost:8090` and the fixed container names `gateway`/`processor` are the
# laptop's and nobody else's), with bash, git and curl, a user `student` (uid 1000) in the docker group, and the
# workspace ~/AC215 (README: <your-workspace>). run_steps.sh types each README command into it with
# `docker exec` (a fresh login shell per command, or a real pseudo-terminal via tty_session.py for interactive
# commands and live progress views). Nothing from the tutorial repos runs on the recording machine itself.
#
# Capture-only additions (not part of the tutorial; ASSETS.md describes their visible effects):
#  - Behind an HTTPS-only proxy on the host's 127.0.0.1 (the recording sandbox), export HTTPS_PROXY and CA_BUNDLE
#    (a PEM file with the proxy's CA) first. proxy_relay.py (container l04-relay) makes the proxy reachable from
#    Docker's bridge network; the laptop's engine, git and curl use it, and ~/.docker/config.json "proxies"
#    (Docker Desktop: Settings > Resources > Proxies) passes it to builds and containers.
#  - The base images python:3.14-slim-bookworm (mega-pipeline) and python:3.14-slim (port_toy) are pulled on the
#    recording machine, loaded into the laptop, and rebuilt under the same name with the proxy's CA and https apt
#    sources (capture-only/base-*.Dockerfile), so the tutorial's own Dockerfiles build unchanged.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
PART=$1
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
LAPTOP=l04-laptop
NOPX=localhost,127.0.0.1
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l04-relay; then
    docker rm -f l04-relay >/dev/null 2>&1 || true
    docker run -d --name l04-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38704 "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:38704
fi
export RELAY NOPX LAPTOP

if [ "$PART" = gcloud ]; then
  bash "$HERE/run_steps.sh" "$HERE" gcloud
  exit
fi

# ---- a fresh laptop: empty Docker engine, bash/git/curl, user student, workspace ~/AC215 ----
docker rm -f $LAPTOP >/dev/null 2>&1 || true
docker volume rm l04-laptop-docker >/dev/null 2>&1 || true
docker run -d --privileged --name $LAPTOP --hostname laptop \
  -v l04-laptop-docker:/var/lib/docker -v "$CA":/ca.crt:ro \
  -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
  --entrypoint sh docker:29.8.2-dind -c '
    cp /ca.crt /etc/ssl/certs/ca-certificates.crt
    exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
PROXY_JSON=
[ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"
docker exec -e PROXY_JSON="$PROXY_JSON" $LAPTOP sh -c '
  set -e
  until docker info >/dev/null 2>&1; do sleep 1; done
  apk add --no-cache -q bash git curl coreutils diffutils grep findutils less >/dev/null
  adduser -D -u 1000 -s /bin/bash student && addgroup student docker
  mkdir -p /home/student/.docker /home/student/AC215
  [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
  chown -R student:student /home/student'

# ---- capture-only base images (same names as the tutorial's FROM lines) ----
mkdir -p "$HERE/capture-only"
base() {  # base <image> <Dockerfile name>
  docker image inspect "$1" >/dev/null 2>&1 || docker pull -q "$1" >/dev/null
  docker save "$1" | docker exec -i $LAPTOP docker load -q >/dev/null
  docker exec $LAPTOP mkdir -p /capture-ctx
  docker cp "$CA" $LAPTOP:/capture-ctx/capture-ca.crt
  docker cp "$HERE/capture-only/$2" $LAPTOP:/capture-ctx/$2
  { echo "\$ docker build -t $1 -f $2 ."
    docker exec -u student -w /capture-ctx $LAPTOP docker build --progress=plain -t "$1" -f "$2" . 2>&1
    echo "[exit $?]"; } > "$HERE/capture-only/${2%.Dockerfile}-build.txt"
}
if [ "$PART" = port ]; then
  base python:3.14-slim base-python-3.14-slim.Dockerfile
  bash "$HERE/run_steps.sh" "$HERE" port
elif [ "$PART" = mega ]; then
  base python:3.14-slim-bookworm base-python-3.14-slim-bookworm.Dockerfile
  bash "$HERE/run_steps.sh" "$HERE" mega
fi
docker rm -f $LAPTOP >/dev/null
docker volume rm l04-laptop-docker >/dev/null
