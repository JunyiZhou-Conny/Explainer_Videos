#!/bin/bash
# Re-capture the L03 terminal transcripts (dlops-io/mega-pipeline, branch main). Needs Docker and python3.
#   bash assets/terminal/capture.sh <work_dir> [part ...]     parts: setup a a2 b c d e final (default: all)
# <work_dir> becomes the "laptop" home (the clone lands in <work_dir>/mega-pipeline); use an empty folder.
# Behind an HTTPS-only proxy, export https_proxy/HTTPS_PROXY and CA_BUNDLE (a PEM file) first. Set PYTHON to a
# python that has `pyte` (pip install pyte) so the terminal renders of docker build come out right.
#
# What it sets up (none of this is in the README; ASSETS.md explains each item):
#  - l03-capture/laptop:debian12  : the laptop's shell (git, curl, Debian's python3, user `student`, uid 1000).
#    git/uv/ls/cat steps run in a fresh container of it with <work_dir> mounted as /home/student.
#  - docker steps run on this machine's Docker Engine, from the same folder (the laptop's Docker).
#  - l03-capture/python:3.12-slim-bookworm : python:3.12-slim-bookworm + the proxy CA + https apt sources.
#    The Dockerfiles that are built use it in their FROM line instead of python:3.12-slim-bookworm
#    (files/ keeps the README version); everything below FROM is the README's text.
#  - DOCKER_CONFIG with a "proxies" entry, so docker build/run pass the proxy variables on, and
#    --network host on the build and on the containers that download (the proxy listens on 127.0.0.1).
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
WORK="$(mkdir -p "$1" && cd "$1" && pwd)"; shift
PARTS=${*:-setup a a2 b c d e final}
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
CTX="$WORK.capture"; mkdir -p "$CTX/dockercfg"   # capture-only files live next to <work_dir>, not in it
cp "$CA" "$CTX/ca-bundle.crt"
export DOCKER_CONFIG="$CTX/dockercfg"
if [ -n "$HTTPS_PROXY$https_proxy" ]; then
  printf '{"proxies": {"default": {"httpsProxy": "%s", "noProxy": "localhost,127.0.0.1"}}}\n' \
    "${HTTPS_PROXY:-$https_proxy}" > "$DOCKER_CONFIG/config.json"
else
  echo '{}' > "$DOCKER_CONFIG/config.json"
fi

if [[ " $PARTS " == *" setup "* ]]; then
  docker pull -q python:3.12-slim-bookworm >/dev/null
  # capture-only base image: trust the proxy CA, fetch apt over https
  cat > "$CTX/base.Dockerfile" <<'EOF'
FROM python:3.12-slim-bookworm
COPY ca-bundle.crt /usr/local/share/ca-certificates/capture-proxy-ca.crt
COPY ca-bundle.crt /etc/ssl/certs/ca-certificates.crt
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt PIP_CERT=/etc/ssl/certs/ca-certificates.crt
EOF
  docker build -q -t l03-capture/python:3.12-slim-bookworm -f "$CTX/base.Dockerfile" "$CTX" >/dev/null
  # capture-only laptop shell: Debian 12 with git, curl and the distribution's python3 (3.11)
  cat > "$CTX/laptop.Dockerfile" <<'EOF'
FROM debian:12
COPY ca-bundle.crt /etc/ssl/certs/ca-certificates.crt
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq git curl ca-certificates python3 >/dev/null && \
    rm -rf /var/lib/apt/lists/* && useradd -u 1000 -s /bin/bash student
COPY ca-bundle.crt /etc/ssl/certs/ca-certificates.crt
EOF
  docker build -q --network host --build-arg https_proxy --build-arg HTTPS_PROXY \
    -t l03-capture/laptop:debian12 -f "$CTX/laptop.Dockerfile" "$CTX" >/dev/null
  # an empty home for `student` (uid 1000) with Debian's default dotfiles
  docker run --rm -v "$WORK":/home/student l03-capture/laptop:debian12 \
    bash -c 'cp -rn /etc/skel/. /home/student/ && chown 1000:1000 /home/student /home/student/.[a-z]*'
fi

for p in $PARTS; do
  [ "$p" = setup ] && continue
  bash "$HERE/run_steps.sh" "$HERE" "$WORK" "$p"
done
