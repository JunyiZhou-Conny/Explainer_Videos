# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through a
# TLS-intercepting proxy that refuses plain http. Same ubuntu:20.04 plus that proxy's CA, https apt
# sources and the CA env vars, re-tagged under the same name so the tutorial Dockerfile builds
# unchanged.
FROM ubuntu:20.04
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN mkdir -p /etc/ssl/certs && cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i -e 's|http://archive.ubuntu.com|https://archive.ubuntu.com|g' -e 's|http://security.ubuntu.com|https://security.ubuntu.com|g' /etc/apt/sources.list
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    AWS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
