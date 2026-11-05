# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through a
# TLS-intercepting proxy that refuses plain http. Same python:3.9-slim plus that proxy's CA (also kept for
# update-ca-certificates), https apt sources and the CA env vars, re-tagged under the same name so
# the tutorial Dockerfiles build unchanged.
FROM python:3.9-slim
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN mkdir -p /etc/ssl/certs && cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && for f in /etc/apt/sources.list /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/ubuntu.sources; do \
      [ -f "$f" ] && sed -i -e 's|http://deb.debian.org|https://deb.debian.org|g' -e 's|http://security.debian.org|https://security.debian.org|g' \
        -e 's|http://archive.ubuntu.com|https://archive.ubuntu.com|g' -e 's|http://security.ubuntu.com|https://security.ubuntu.com|g' "$f"; \
    done; true
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    AWS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    PIP_NO_CACHE_DIR=1
