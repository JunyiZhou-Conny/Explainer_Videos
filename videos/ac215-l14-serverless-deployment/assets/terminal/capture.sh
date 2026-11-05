#!/bin/bash
# Re-capture the L14 terminal transcripts (needs Docker; "laptop" needs privileged containers):
#   bash assets/terminal/capture.sh laptop setup
#   bash assets/terminal/capture.sh laptop pre run1 ca run2 port job
#   bash assets/terminal/capture.sh laptop teardown
#   bash assets/terminal/capture.sh dev pre local function
#   bash assets/terminal/capture.sh gcloud run
# Containers persist between calls ("laptop", "dev"), so a long capture can run in parts;
# `laptop teardown` and `dev teardown` remove them.
#
# "laptop": a fresh, empty Docker engine (docker:29.8.2-dind) stands in for the student's machine
#   with Docker Desktop (README "Before you begin" step 4: "Docker is needed for the local
#   demonstration in part 2"): user `student` in the docker group, bash, git, curl, python3 (for
#   ptyrun.py). Part 2.1's `docker run` and the image's offline `batch` command run here.
# "dev": python:3.12-slim-bookworm (+ git, curl, uv from its installer) as user `student`: the
#   machine of Part 3.3 ("With uv installed, run the app directly") and a local stand-in for
#   Part 1's function (functions-framework from tutorial/function/requirements.txt).
# "gcloud": the Google Cloud CLI image (gcr.io/google.com/cloudsdktool/google-cloud-cli:slim) +
#   Debian's python3 ("Python and the Google Cloud CLI are needed for the local helper in part 4")
#   with NO account signed in: every gcloud box of the README stops at its documented sign-in
#   error, and the helper/lifecycle scripts run in their offline (dry-run / plan) modes.
# There are NO GCP credentials in any environment (see ASSETS.md, "What cannot run here").
#
# Behind an HTTPS-only proxy that listens on the host's 127.0.0.1 (the recording sandbox), export
# HTTPS_PROXY and CA_BUNDLE (a PEM file with the proxy's CA) first: proxy_relay.py (container
# l14-relay) makes the proxy reachable from Docker's bridge network, and the CA is added to the
# environments as ASSETS.md describes ("capture-only"). Remove the relay with
# `docker rm -f l14-relay` when done.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
MODE=$1; shift
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  if ! docker ps --format '{{.Names}}' | grep -qx l14-relay; then
    docker rm -f l14-relay >/dev/null 2>&1 || true
    docker run -d --name l14-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
      python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38714 "$PHOST" "$PPORT" >/dev/null
  fi
  RELAY=http://$GW:38714
  for i in $(seq 30); do   # wait until the relay listens, or the first git/pull call races it
    docker exec l14-relay python -c "import socket; socket.create_connection(('$GW', 38714), timeout=2).close()" >/dev/null 2>&1 && break
    sleep 1
  done
fi
PROXY_JSON=
[ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"
PXENV=(-e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX)

if [ "$MODE" = laptop ]; then
  DEST="$HERE/laptop"; mkdir -p "$DEST"
  for SEG in "$@"; do
    case $SEG in
      setup)
        docker rm -f l14-laptop >/dev/null 2>&1 || true
        docker volume rm l14-laptop-docker >/dev/null 2>&1 || true
        docker run -d --privileged --name l14-laptop --hostname laptop \
          -v l14-laptop-docker:/var/lib/docker -v "$HERE":/capture:ro -v "$DEST":/out -v "$CA":/ca.crt:ro \
          "${PXENV[@]}" --entrypoint sh docker:29.8.2-dind -c '
            cp /ca.crt /etc/ssl/certs/ca-certificates.crt
            exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
        docker exec -e PROXY_JSON="$PROXY_JSON" l14-laptop sh -c '
          set -e
          until docker info >/dev/null 2>&1; do sleep 1; done
          # the laptop baseline (not part of the tutorial): bash, git, curl, python3 (for
          # ptyrun.py), and a user in the docker group. Docker client proxy settings (capture-only)
          # pass the recording proxy to the containers the tutorial starts.
          apk add --no-cache -q bash python3 git curl >/dev/null
          adduser -D -s /bin/bash student && addgroup student docker
          mkdir -p /home/student/.docker
          [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
          chown -R student:student /home/student; chmod 777 /out' ;;
      teardown)
        docker rm -f l14-laptop >/dev/null; docker volume rm l14-laptop-docker >/dev/null ;;
      *)
        docker exec -u student -w /home/student -e HOME=/home/student -e USER=student \
          -e CAPTURE_CA="$([ -n "$RELAY" ] && echo /ca.crt)" -e CAPTURE_HUB_WAIT="$([ -n "$RELAY" ] && echo 1)" \
          "${PXENV[@]}" l14-laptop bash /capture/run_steps.sh /out "laptop-$SEG" ;;
    esac
  done
elif [ "$MODE" = dev ]; then
  DEST="$HERE/dev"; mkdir -p "$DEST"; chmod 777 "$DEST"
  for SEG in "$@"; do
    case $SEG in
      pre)
        # capture-only image: python:3.12-slim-bookworm + git + curl + the recording proxy's CA
        D=$(mktemp -d); cp "$CA" "$D/capture-ca.crt"
        cat > "$D/Dockerfile" <<'EOF'
# capture-only, NOT part of the tutorial: a Linux developer machine with Python 3.12, git and
# curl, plus the recording proxy's CA (the sandbox's TLS is re-signed by its proxy).
FROM python:3.12-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
 && apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl ca-certificates >/dev/null \
 && cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && rm -rf /var/lib/apt/lists/* && useradd -m -s /bin/bash student
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt UV_SYSTEM_CERTS=1
USER student
WORKDIR /home/student
EOF
        mkdir -p "$DEST/capture-only"; cp "$D/Dockerfile" "$DEST/capture-only/dev-standin.Dockerfile"
        docker build --network host --build-arg HTTPS_PROXY="$HTTPS_PROXY" --build-arg https_proxy="$HTTPS_PROXY" \
          -t l14-dev-standin "$D" > "$DEST/capture-only/dev-standin-build.txt" 2>&1
        rm -rf "$D"
        docker rm -f l14-dev >/dev/null 2>&1 || true
        docker run -d --name l14-dev --hostname devbox -v "$HERE":/capture:ro -v "$DEST":/out \
          "${PXENV[@]}" l14-dev-standin sleep infinity >/dev/null
        docker exec l14-dev bash /capture/run_steps.sh /out dev-pre ;;
      teardown)
        docker rm -f l14-dev >/dev/null ;;
      *)
        docker exec "${PXENV[@]}" l14-dev bash /capture/run_steps.sh /out "dev-$SEG" ;;
    esac
  done
elif [ "$MODE" = gcloud ]; then
  DEST="$HERE/gcloud"; mkdir -p "$DEST/capture-only"; chmod 777 "$DEST"
  # capture-only image: the Google Cloud CLI image + Debian's python3/python-is-python3 (the
  # README's helper is run as `python ...`; the CLI image itself ships only gcloud's bundled
  # Python) + a user `student` + the recording proxy's CA
  D=$(mktemp -d); cp "$CA" "$D/capture-ca.crt"
  cat > "$D/Dockerfile" <<'EOF2'
# capture-only, NOT part of the tutorial: a laptop with "Python and the Google Cloud CLI"
# (README "Before you begin" step 4), no Google account signed in.
FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:slim
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
 && rm -f /etc/apt/sources.list.d/google-cloud-sdk.list \
 && apt-get update -qq && apt-get install -y -qq --no-install-recommends python3 python-is-python3 >/dev/null \
 && cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && rm -rf /var/lib/apt/lists/* && useradd -m -s /bin/bash student
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
USER student
WORKDIR /home/student
EOF2
  cp "$D/Dockerfile" "$DEST/capture-only/gcloud-standin.Dockerfile"
  docker build --network host --build-arg HTTPS_PROXY="$HTTPS_PROXY" --build-arg https_proxy="$HTTPS_PROXY" \
    -t l14-gcloud-standin "$D" > "$DEST/capture-only/gcloud-standin-build.txt" 2>&1
  rm -rf "$D"
  docker run --rm --name l14-gcloud --hostname laptop -v "$HERE":/capture:ro -v "$DEST":/out \
    "${PXENV[@]}" l14-gcloud-standin bash /capture/run_steps.sh /out gcloud-run
else
  echo "usage: capture.sh laptop setup|<segment>...|teardown | dev pre|<segment>...|teardown | gcloud run" >&2; exit 2
fi
