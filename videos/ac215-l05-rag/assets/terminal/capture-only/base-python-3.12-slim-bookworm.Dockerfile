# capture-only (not part of the tutorial): python:3.12-slim-bookworm plus the recording proxy's CA, https apt
# sources and the CA variables pip and uv read, rebuilt under the same name so llm-rag's own Dockerfile
# (FROM python:3.12-slim-bookworm, Dockerfile:2) builds unchanged behind the proxy.
FROM python:3.12-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-proxy-ca.crt
COPY capture-ca.crt /etc/ssl/certs/ca-certificates.crt
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt PIP_CERT=/etc/ssl/certs/ca-certificates.crt
