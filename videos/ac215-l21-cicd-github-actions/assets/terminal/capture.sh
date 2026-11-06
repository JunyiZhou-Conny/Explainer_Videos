#!/bin/bash
# Re-capture the L21 terminal transcripts (needs Docker and privileged containers):
#   bash assets/terminal/capture.sh laptop setup
#   bash assets/terminal/capture.sh laptop l-pre l-push l-own l-fix l-noverify l-part6
#   bash assets/terminal/capture.sh export <label> <sha>      # checkout of <sha> from the stand-in remote
#   bash assets/terminal/capture.sh run <label> <sha>         # the six ci.yml jobs, one fresh runner each
#   bash assets/terminal/capture.sh noload <label> <sha>      # extra: a check job without `docker load`
#   bash assets/terminal/capture.sh laptop teardown; bash assets/terminal/capture.sh cleanup
# Typical order (see ASSETS.md): laptop setup, l-pre, l-push, l-own, then `export run1 <sha>` +
# `run run1 <sha>` for the pushed head; l-fix + run2; l-noverify + run3; `demo` + run-demo.
#
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind) stands in for the student's machine
#   with Docker Desktop, as in L09: user `student` in the docker group, bash, python3, git, curl, a
#   Python virtualenv first on PATH (a laptop Python that allows `pip install`). A bare repository
#   inside it, ~/github-standin/student/cheese-app-ci-cd.git, stands in for "your repository" on
#   GitHub (this sandbox cannot push to GitHub); see ASSETS.md.
# "runner": every job of ci.yml runs in its OWN fresh container with its own empty Docker engine
#   (image l21-runner:capture = docker:29.8.2-dind + bash, curl, git), the way GitHub gives every
#   job a fresh ubuntu-latest VM. ci_plan.py extracts the job's steps from ci.yml (verbatim run:
#   scripts, ${{ }} substituted); runner_job.sh runs them. The image tar travels from the build
#   job to the others through a host folder, the stand-in for upload/download-artifact.
#   test-summary runs in a plain python:3.12-slim-bookworm container (it only needs bash).
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l21-relay) makes the proxy reachable from Docker's bridge network, and the CA is added to the
# containers as ASSETS.md describes ("capture-only"). Docker Hub pulls go through mirror.gcr.io
# (--registry-mirror) because the sandbox's shared IPs hit Docker Hub's anonymous rate limit.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../source/cheese-app-ci-cd"
WORK=${CAPTURE_WORK:-$HERE/../../build/capture-work}   # gitignored: checkouts, image tars
MODE=$1; shift
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l21-relay; then
    docker rm -f l21-relay >/dev/null 2>&1 || true
    docker run -d --name l21-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38721 "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:38721
  for i in $(seq 30); do
    docker exec l21-relay python -c "import socket; socket.create_connection(('$GW', 38721), timeout=2).close()" >/dev/null 2>&1 && break
    sleep 1
  done
fi
PROXY_JSON=
[ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"
PXENV=(-e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX)

runner_image() {  # capture-only: the stand-in runner image (dind + the tools a hosted runner has)
  docker image inspect l21-runner:capture >/dev/null 2>&1 && return
  local d; d=$(mktemp -d); cp "$CA" "$d/capture-ca.crt"
  cat > "$d/Dockerfile" <<'EOF'
FROM docker:29.8.2-dind
COPY capture-ca.crt /capture-ca.crt
RUN cp /capture-ca.crt /etc/ssl/certs/ca-certificates.crt && apk add --no-cache -q bash curl git
EOF
  docker build -q --network host --build-arg HTTPS_PROXY="$HTTPS_PROXY" --build-arg https_proxy="$HTTPS_PROXY" \
    -t l21-runner:capture "$d" >/dev/null
  rm -f "$d/Dockerfile" "$d/capture-ca.crt"; rmdir "$d"
}
start_runner() {  # start_runner <name> [net]: a fresh runner with an empty Docker engine; "net"
  # also gives its docker CLI the proxy and its engine the Docker Hub mirror (only the build job
  # downloads anything; the others pull from Docker Hub itself, as a hosted runner would)
  local mirror=; [ "$2" = net ] && mirror=--registry-mirror=https://mirror.gcr.io
  docker rm -f -v "$1" >/dev/null 2>&1 || true
  docker run -d --privileged --name "$1" --hostname runner -v /var/lib/docker "${PXENV[@]}" \
    -v "$HERE":/capture:ro --entrypoint sh l21-runner:capture -c \
    "exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock $mirror" >/dev/null
  local pj=; [ "$2" = net ] && pj=$PROXY_JSON
  docker exec -e PROXY_JSON="$pj" "$1" sh -c '
    until docker info >/dev/null 2>&1; do sleep 1; done
    mkdir -p /root/.docker; [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /root/.docker/config.json; true'
}
capture_only_base() {  # in runner $1: python:3.11-slim-bookworm + the proxy CA, same tag (as L09).
  # Off by default: on 2026-11-06 the unmodified base built fine here; set CAPTURE_BASE=1 if your
  # sandbox needs the CA inside the build.
  [ -n "$RELAY" ] && [ -n "$CAPTURE_BASE" ] || return 0
  docker exec "$1" sh -c '
    d=$(mktemp -d); cp /capture-ca.crt $d/capture-ca.crt
    cat > $d/Dockerfile <<EOF
# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through
# a TLS-intercepting proxy. Same python:3.11-slim-bookworm plus that proxy CA, https apt
# sources and the CA env vars, re-tagged under the same name so that the tutorial Dockerfile
# builds unchanged.
FROM python:3.11-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i "s|http://deb.debian.org|https://deb.debian.org|g" /etc/apt/sources.list.d/debian.sources
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
EOF
    docker build -q -t python:3.11-slim-bookworm $d >/dev/null && rm -rf $d'
}
run_job() {  # run_job <label> <sha> <job> [--needs ...]   -> runner/<label>/<job>/
  local label=$1 sha=$2 job=$3; shift 3
  local out="$HERE/runner/$label/$job" name="l21-runner-$job"
  rm -f "$out"/*.txt 2>/dev/null || true; mkdir -p "$out"
  python3 -I "$HERE/ci_plan.py" "$SRC/.github/workflows/ci.yml" "$job" "$sha" \
    /home/runner/work/cheese-app-ci-cd/cheese-app-ci-cd "$@" > "$WORK/$label/$job.plan.sh"
  if [ "$job" = build ]; then start_runner "$name" net; else start_runner "$name"; fi
  docker cp "$WORK/$label/checkout.tar" "$name":/checkout.tar >/dev/null
  docker cp "$WORK/$label/$job.plan.sh" "$name":/plan.sh >/dev/null
  if [ "$job" = build ]; then capture_only_base "$name"
  else docker exec "$name" mkdir -p /artifact; docker cp "$WORK/$label/artifact/cheese-app-api.tar" "$name":/artifact/ >/dev/null; fi
  docker exec "$name" mkdir -p /out
  docker exec "$name" bash /capture/runner_job.sh /out /plan.sh "$sha"
  docker cp "$name":/out/. "$out/" >/dev/null
  if [ "$job" = build ]; then mkdir -p "$WORK/$label/artifact"
    # (the dind entrypoint mounts a tmpfs on /tmp, which `docker cp` cannot see)
    docker exec "$name" cat /tmp/cheese-app-api.tar > "$WORK/$label/artifact/cheese-app-api.tar"; fi
  docker rm -f -v "$name" >/dev/null
}

case $MODE in
laptop)
  DEST="$HERE/laptop"; mkdir -p "$DEST"
  for SEG in "$@"; do
    case $SEG in
      setup)
        docker rm -f l21-laptop >/dev/null 2>&1 || true
        docker volume rm l21-laptop-docker >/dev/null 2>&1 || true
        docker run -d --privileged --name l21-laptop --hostname laptop \
          -v l21-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
          "${PXENV[@]}" --entrypoint sh docker:29.8.2-dind -c '
            cp /ca.crt /etc/ssl/certs/ca-certificates.crt
            exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock --registry-mirror=https://mirror.gcr.io' >/dev/null
        docker exec -e PROXY_JSON="$PROXY_JSON" l21-laptop sh -c '
          set -e
          until docker info >/dev/null 2>&1; do sleep 1; done
          # the laptop baseline (not part of the tutorial), as in L09
          apk add --no-cache -q bash python3 py3-virtualenv git curl sed >/dev/null
          adduser -D -s /bin/bash student && addgroup student docker
          virtualenv -q /home/student/venv
          mkdir -p /home/student/.docker
          [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
          chown -R student:student /home/student; chmod 777 /out' ;;
      act-setup)  # capture-only: act + Node.js (for the JavaScript actions) on the laptop.
        # GitHub release downloads are blocked in the recording sandbox, so act was built from
        # source through the Go module proxy, CGO_ENABLED=0 `go install github.com/nektos/act@v0.2.97`
        # in a golang:1.25-bookworm container; pass the binary as ACT_BIN.
        docker cp "$ACT_BIN" l21-laptop:/usr/local/bin/act >/dev/null
        docker exec l21-laptop sh -c 'apk add --no-cache -q nodejs >/dev/null' ;;
      teardown)
        docker rm -f l21-laptop >/dev/null; docker volume rm l21-laptop-docker >/dev/null ;;
      *)
        docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
          -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" "${PXENV[@]}" \
          l21-laptop bash /capture/run_steps.sh /out "$SEG" ;;
    esac
  done ;;
export)  # export <label> <sha>: what actions/checkout would fetch, from the stand-in remote
  label=$1; sha=$2; mkdir -p "$WORK/$label"
  docker exec -u student l21-laptop git -C /home/student/github-standin/student/cheese-app-ci-cd.git \
    archive --format=tar "$sha" > "$WORK/$label/checkout.tar" ;;
demo)    # demo <label> <sha> <clone>: a commit that is not on the stand-in remote (the class demo)
  label=$1; sha=$2; mkdir -p "$WORK/$label"
  git -C "$3" archive --format=tar "$sha" > "$WORK/$label/checkout.tar" ;;
run)     # run <label> <sha>: build, then the four check jobs, then test-summary
  label=$1; sha=$2; runner_image
  run_job "$label" "$sha" build
  B=$(cat "$HERE/runner/$label/build/result.txt")
  R=()
  for j in lint-and-format unit-tests integration-tests system-tests; do
    if [ "$B" = success ]; then run_job "$label" "$sha" "$j"; R+=("$j=$(cat "$HERE/runner/$label/$j/result.txt")")
    else R+=("$j=skipped"); fi
  done
  # test-summary: needs only the three test jobs (ci.yml:175), if: always() (ci.yml:176)
  out="$HERE/runner/$label/test-summary"; mkdir -p "$out"; rm -f "$out"/*.txt
  python3 -I "$HERE/ci_plan.py" "$SRC/.github/workflows/ci.yml" test-summary "$sha" \
    /home/runner/work/cheese-app-ci-cd/cheese-app-ci-cd --needs "${R[@]:1}" > "$WORK/$label/test-summary.plan.sh"
  docker run --rm -v "$HERE":/capture:ro -v "$WORK/$label/test-summary.plan.sh":/plan.sh:ro -v "$out":/out \
    python:3.12-slim-bookworm bash /capture/runner_job.sh /out /plan.sh "$sha"
  printf '%s\n' "build=$B" "${R[@]}" "test-summary=$(cat "$out/result.txt")" > "$HERE/runner/$label/results.txt" ;;
noload)  # extra: the unit-tests command on a fresh runner that skipped `docker load` (ponder)
  label=$1; sha=$2; runner_image; out="$HERE/runner/$label"; mkdir -p "$out"
  start_runner l21-runner-noload
  docker exec l21-runner-noload bash -c "mkdir -p /out; cd /; { echo '\$ docker images'; docker images 2>&1; echo \"[exit \$?]\"; } > /out/x1.txt
    { echo '\$ docker run --rm cheese-app-api:$sha pytest tests/unit/ -v --tb=short'
      docker run --rm cheese-app-api:$sha pytest tests/unit/ -v --tb=short 2>&1; echo \"[exit \$?]\"; } > /out/x2.txt"
  docker cp l21-runner-noload:/out/x1.txt "$out/x1-images.txt" >/dev/null
  docker cp l21-runner-noload:/out/x2.txt "$out/x2-unit-tests-without-load.txt" >/dev/null
  docker rm -f -v l21-runner-noload >/dev/null ;;
cleanup)
  docker rm -f l21-relay >/dev/null 2>&1 || true
  docker rmi l21-runner:capture >/dev/null 2>&1 || true ;;
*) echo "usage: capture.sh laptop|export|demo|run|noload|cleanup ..." >&2; exit 2 ;;
esac
