# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through
# a TLS-intercepting proxy. Same python:3.12-slim-bookworm plus that proxy's CA and https apt
# sources, re-tagged under the same name so that the README's Dockerfiles build unchanged.
FROM python:3.12-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
