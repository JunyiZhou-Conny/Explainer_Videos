# capture-only, NOT part of the tutorial: same node:20-alpine plus the recording proxy's CA
# (for apk and npm), re-tagged under the same name so that frontend-ai-chatbot/Dockerfile.dev
# builds unchanged and `npm install` can download through the proxy.
FROM node:20-alpine
COPY capture-ca.crt /tmp/capture-ca.crt
RUN cat /tmp/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt && rm /tmp/capture-ca.crt
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt \
    NPM_CONFIG_CAFILE=/etc/ssl/certs/ca-certificates.crt
