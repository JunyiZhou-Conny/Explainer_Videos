# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through a
# TLS-intercepting proxy that refuses plain http. Same python:3.13-slim-bullseye plus that proxy's CA, https Debian
# sources (bullseye: /etc/apt/sources.list; bookworm: debian.sources) and the CA env vars,
# re-tagged under the same name so the tutorial Dockerfile builds unchanged.
FROM python:3.13-slim-bullseye
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && for f in /etc/apt/sources.list /etc/apt/sources.list.d/debian.sources; do \
      [ -f "$f" ] && sed -i -e 's|http://deb.debian.org|https://deb.debian.org|g' -e 's|http://security.debian.org|https://security.debian.org|g' "$f"; \
    done; true
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE=/etc/ssl/certs/ca-certificates.crt \
    UV_NATIVE_TLS=1
