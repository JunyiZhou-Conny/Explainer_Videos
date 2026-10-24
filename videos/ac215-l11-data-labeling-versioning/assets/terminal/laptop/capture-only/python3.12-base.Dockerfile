# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through a
# TLS-intercepting proxy that refuses plain http. Same python:3.12-slim-bookworm plus that proxy's CA,
# https apt sources, an apt hook that upgrades packages.cloud.google.com to https before each
# update, and the CA env vars, re-tagged under the same name so the tutorial Dockerfiles build
# unchanged.
FROM python:3.12-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
 && echo 'APT::Update::Pre-Invoke { "sed -i s,http://packages.cloud.google.com,https://packages.cloud.google.com,g /etc/apt/sources.list.d/*.list 2>/dev/null || true"; };' > /etc/apt/apt.conf.d/99capture-https
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    UV_NATIVE_TLS=1
