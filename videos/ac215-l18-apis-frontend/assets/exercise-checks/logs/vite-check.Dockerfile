# Check-only image (not a tutorial file): Dockerfile.dev's base and user, with only vite 8.3.5 (the
# version in main's package-lock.json) installed, plus curl, through the session proxy (its CA added).
FROM mirror.gcr.io/library/node:24.22.1-bookworm-slim
COPY ca.crt /usr/local/share/ca-certificates/session-proxy.crt
ENV NODE_EXTRA_CA_CERTS=/usr/local/share/ca-certificates/session-proxy.crt
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get -o Acquire::https::CaInfo=$NODE_EXTRA_CA_CERTS update -qq && \
    apt-get -o Acquire::https::CaInfo=$NODE_EXTRA_CA_CERTS install -y -qq --no-install-recommends curl >/dev/null && \
    rm -rf /var/lib/apt/lists/* && mkdir -p /app && chown node:node /app
USER node
WORKDIR /app
RUN npm config set cafile $NODE_EXTRA_CA_CERTS && echo '{"name":"vite-check","private":true,"type":"module"}' > package.json && \
    npm install --no-fund --no-audit --loglevel=error vite@8.3.5 && npx vite --version
