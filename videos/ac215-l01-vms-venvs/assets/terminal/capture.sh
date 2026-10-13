#!/bin/bash
# Re-capture the terminal transcripts in a fresh Debian container (needs Docker):
#   bash assets/terminal/capture.sh debian:12 A debian12-part-a
#   bash assets/terminal/capture.sh debian:12 B debian12-part-b
#   bash assets/terminal/capture.sh debian:13 B debian13-part-b
# Behind an HTTPS-only proxy, export https_proxy and CA_BUNDLE (a PEM file) first.
HERE="$(cd "$(dirname "$0")" && pwd)"
IMG=$1; PART=$2; DEST="$HERE/$3"
mkdir -p "$DEST"
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
docker run --rm --network host \
  -e https_proxy -e HTTPS_PROXY -e no_proxy -e NO_PROXY \
  -e SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt -e REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
  -v "$CA":/ca.crt:ro -v "$HERE/run_steps.sh":/run_steps.sh:ro -v "$DEST":/out \
  "$IMG" bash -c '
set -e
# the baseline of a GCP Debian image (not part of the tutorial): https apt sources, CA bundle,
# python3, sudo, curl, and a user with passwordless sudo, like the console-SSH user
mkdir -p /etc/ssl/certs && cp /ca.crt /etc/ssl/certs/ca-certificates.crt
sed -i "s|http://deb.debian.org|https://deb.debian.org|g" /etc/apt/sources.list.d/debian.sources
apt-get update -qq >/dev/null && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq python3 sudo curl ca-certificates >/dev/null 2>&1
cp /ca.crt /etc/ssl/certs/ca-certificates.crt
rm -rf /var/lib/apt/lists/*
useradd -m -s /bin/bash student && echo "student ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/student
echo "Defaults env_keep += \"https_proxy HTTPS_PROXY no_proxy NO_PROXY SSL_CERT_FILE REQUESTS_CA_BUNDLE\"" >> /etc/sudoers.d/student
chmod 777 /out
su - student -w https_proxy,HTTPS_PROXY,no_proxy,NO_PROXY,SSL_CERT_FILE,REQUESTS_CA_BUNDLE -c "/run_steps.sh /out '"$PART"'"
'
# file names: <part>-<nn>-<name>.txt -> <nn>-<name>.txt
for f in "$DEST"/?-*.txt; do mv "$f" "$DEST/$(basename "$f" | cut -c3-)"; done
