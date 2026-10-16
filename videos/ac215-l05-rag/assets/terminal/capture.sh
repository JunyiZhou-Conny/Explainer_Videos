#!/bin/bash
# Re-capture the L05 terminal transcripts (dlops-io/llm-rag, branch main, the whole RAG part of the README).
# Needs Docker with privileged containers, and python3 with `pyte` (pip install pyte; set PYTHON to it) so the
# live progress views of `docker compose` render as a terminal shows them.
#   bash assets/terminal/capture.sh main      -> laptop/ (your laptop's terminal) and cli-container/ (typed at
#                                                the llm-rag-cli container's prompt), README order, plus extras
#   bash assets/terminal/capture.sh gotchas   -> gotchas/ (G5: compose without the script; G1: a clone that is
#                                                not named llm-rag). Run after `main` (it reuses its laptop).
# `main` empties its folders first and keeps the laptop for `gotchas`; `gotchas` removes the laptop at the end
# (or: docker rm -f l05-laptop; docker volume rm l05-laptop-docker). Behind the proxy also export CA_BUNDLE.
#
# "Your laptop" is a fresh, empty Docker engine standing in for Docker Desktop: a docker:29.8.2-dind container
# with its own network namespace (so localhost:8000 and the fixed names llm-rag-cli / llm-rag-chromadb /
# llm-rag-network are the laptop's and nobody else's), with bash, git and curl, a user `student` (uid 1000) in
# the docker group, and the workspace ~/AC215 (the README's parent folder of llm-rag/ and secrets/).
# run_steps.sh types each README command into it with `docker exec` (a fresh login shell per command, or a real
# pseudo-terminal via tty_session.py for interactive commands and live progress views). Nothing from the
# tutorial repo runs on the recording machine itself.
#
# Capture-only additions (not part of the tutorial; ASSETS.md describes their visible effects):
#  - Behind an HTTPS-only proxy on the host's 127.0.0.1 (the recording sandbox), export HTTPS_PROXY and CA_BUNDLE
#    (a PEM file with the proxy's CA) first. proxy_relay.py (container l05-relay) makes the proxy reachable from
#    Docker's bridge network; the laptop's engine, git and curl use it, and ~/.docker/config.json "proxies"
#    (Docker Desktop: Settings > Resources > Proxies) passes it to builds and containers.
#  - The base image python:3.12-slim-bookworm is pulled into the laptop and rebuilt under the same name with the
#    proxy's CA and https apt sources (capture-only/base-python-3.12-slim-bookworm.Dockerfile), so the tutorial's
#    own Dockerfile builds unchanged.
#  - The laptop's engine pulls Docker Hub images through the registry mirror mirror.gcr.io (dockerd
#    --registry-mirror; Docker Desktop: Settings > Docker Engine > "registry-mirrors"): the recording machine
#    shares Docker Hub's anonymous pull limit with other jobs. docker pull prints the same lines either way.
#  - run_steps.sh is copied to a temporary file before it runs (so it can be edited while a capture runs).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
RS=$(mktemp); cp "$HERE/run_steps.sh" "$RS"
PART=$1
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
LAPTOP=l05-laptop
NOPX=localhost,127.0.0.1
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  docker rm -f l05-relay >/dev/null 2>&1 || true      # the proxy's port changes when the machine restarts
  docker run -d --name l05-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
    python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38705 "$PHOST" "$PPORT" >/dev/null
  RELAY=http://$GW:38705
fi
export RELAY NOPX LAPTOP

if [ "$PART" = main ]; then
  # ---- a fresh laptop: empty Docker engine, bash/git/curl, user student, workspace ~/AC215 ----
  docker rm -f $LAPTOP >/dev/null 2>&1 || true
  docker volume rm l05-laptop-docker >/dev/null 2>&1 || true
  docker run -d --privileged --name $LAPTOP --hostname laptop \
    -v l05-laptop-docker:/var/lib/docker -v "$CA":/ca.crt:ro \
    -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
    --entrypoint sh docker:29.8.2-dind -c '
      cp /ca.crt /etc/ssl/certs/ca-certificates.crt
      exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock --registry-mirror=https://mirror.gcr.io' >/dev/null
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

  # ---- capture-only base image (same name as the tutorial's FROM line) ----
  mkdir -p "$HERE/capture-only"
  docker exec $LAPTOP docker pull -q python:3.12-slim-bookworm >/dev/null
  docker exec $LAPTOP mkdir -p /capture-ctx
  docker cp "$CA" $LAPTOP:/capture-ctx/capture-ca.crt
  docker cp "$HERE/capture-only/base-python-3.12-slim-bookworm.Dockerfile" $LAPTOP:/capture-ctx/base.Dockerfile
  { echo "\$ docker build -t python:3.12-slim-bookworm -f base-python-3.12-slim-bookworm.Dockerfile ."
    docker exec -w /capture-ctx $LAPTOP docker build --progress=plain -t python:3.12-slim-bookworm -f base.Dockerfile . 2>&1
    echo "[exit $?]"; } > "$HERE/capture-only/base-python-3.12-slim-bookworm-build.txt"
  bash "$RS" "$HERE" main
elif [ "$PART" = gotchas ]; then
  bash "$RS" "$HERE" gotchas
  docker rm -f $LAPTOP >/dev/null
  docker volume rm l05-laptop-docker >/dev/null
  docker rm -f l05-relay >/dev/null 2>&1 || true
fi
