# adk-laptop.Dockerfile: the check "laptop" for llm-agent-google-adk (check-only, not part of the tutorial):
# Debian 12 with a system Python 3.12 (python:3.12-slim-bookworm, so C4 can show which Python uv prefers),
# the sandbox proxy's CA, git and curl, uv 0.13.1 and Node.js v24.22.0 / npm 11.19.1 (the capture's versions),
# and the user student (uid 1000).
FROM python:3.12-slim-bookworm
COPY ca.crt /tmp/ca.crt
RUN cp /tmp/ca.crt /etc/ssl/certs/ca-certificates.crt \
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
 && apt-get update -qq && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
      git curl xz-utils procps >/dev/null \
 && cp /tmp/ca.crt /etc/ssl/certs/ca-certificates.crt && rm -rf /var/lib/apt/lists/*
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
RUN pip install -q --no-cache-dir --root-user-action=ignore "uv==0.13.1" \
 && curl -fsSL https://nodejs.org/dist/v24.22.0/node-v24.22.0-linux-x64.tar.xz | tar -xJ -C /usr/local --strip-components=1 \
 && useradd -m -u 1000 -s /bin/bash student
