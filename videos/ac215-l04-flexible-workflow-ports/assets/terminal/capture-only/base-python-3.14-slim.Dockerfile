# capture-only (not part of the tutorial): python:3.14-slim (Debian 13) plus the recording proxy's CA and
# https apt sources, rebuilt under the same name so port_toy's own Dockerfiles build unchanged behind the proxy.
FROM python:3.14-slim
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-proxy-ca.crt
COPY capture-ca.crt /etc/ssl/certs/ca-certificates.crt
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources && \
    echo 'Acquire::https::CaInfo "/etc/ssl/certs/ca-certificates.crt";' > /etc/apt/apt.conf.d/99capture-ca
