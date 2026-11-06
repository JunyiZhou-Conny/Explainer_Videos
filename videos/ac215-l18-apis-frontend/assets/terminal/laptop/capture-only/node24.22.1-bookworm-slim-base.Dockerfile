# capture-only, NOT part of the tutorial: node:24.22.1-bookworm-slim + the recording proxy's CA for npm (and apk),
# re-tagged under the same name so the tutorial Dockerfile builds unchanged.
FROM node:24.22.1-bookworm-slim
COPY capture-ca.crt /usr/local/share/capture-ca.crt
RUN if [ -f /etc/ssl/certs/ca-certificates.crt ]; then cat /usr/local/share/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt; fi; chmod 644 /usr/local/share/capture-ca.crt
ENV NODE_EXTRA_CA_CERTS=/usr/local/share/capture-ca.crt
