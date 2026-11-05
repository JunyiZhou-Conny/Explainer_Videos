# capture-only, NOT part of the tutorial: a Linux developer machine with Python 3.12, git and
# curl, plus the recording proxy's CA (the sandbox's TLS is re-signed by its proxy).
FROM python:3.12-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
 && apt-get update -qq && apt-get install -y -qq --no-install-recommends git curl ca-certificates >/dev/null \
 && cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && rm -rf /var/lib/apt/lists/* && useradd -m -s /bin/bash student
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt UV_SYSTEM_CERTS=1
USER student
WORKDIR /home/student
