# check-only, NOT a tutorial file: the official python:3.11-slim-bookworm (same digest as the
# captures, sha256:a83ba18a...) plus the session proxy's CA and https apt sources, so that the
# tutorial's unchanged Dockerfile can download through the TLS-intercepting proxy. It replaces the
# Dockerfile's FROM image through a named build context (no tag on the shared engine is changed).
FROM mirror.gcr.io/library/python:3.11-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i "s|http://deb.debian.org|https://deb.debian.org|g" /etc/apt/sources.list.d/debian.sources
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
