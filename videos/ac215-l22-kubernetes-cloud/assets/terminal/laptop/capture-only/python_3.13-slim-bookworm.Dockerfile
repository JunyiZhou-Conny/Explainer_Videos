# capture-only, NOT part of the tutorial: python:3.13-slim-bookworm + the recording proxy's CA, re-tagged as python:3.13-slim-bookworm
FROM python:3.13-slim-bookworm
USER root
COPY capture-ca.crt /usr/local/share/capture-ca.crt
RUN for f in /etc/ssl/certs/ca-certificates.crt; do [ -f $f ] && cat /usr/local/share/capture-ca.crt >> $f; done; \
    for f in /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list; do [ -f $f ] && sed -i 's|http://deb.debian.org|https://deb.debian.org|g; s|http://security.debian.org|https://security.debian.org|g' $f; done; true
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt NODE_EXTRA_CA_CERTS=/usr/local/share/capture-ca.crt UV_NATIVE_TLS=1 \
    CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE=/etc/ssl/certs/ca-certificates.crt
ENV HTTPS_PROXY=http://172.17.0.1:38722 https_proxy=http://172.17.0.1:38722 NO_PROXY=localhost,127.0.0.1 no_proxy=localhost,127.0.0.1
