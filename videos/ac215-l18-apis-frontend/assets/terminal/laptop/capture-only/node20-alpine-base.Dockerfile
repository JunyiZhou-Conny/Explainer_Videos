# capture-only, NOT part of the tutorial: node:20-alpine + the recording proxy's CA for npm (and apk),
# re-tagged under the same name so the tutorial Dockerfile builds unchanged.
FROM node:20-alpine
COPY capture-ca.crt /usr/local/share/capture-ca.crt
RUN if [ -f /etc/ssl/certs/ca-certificates.crt ]; then cat /usr/local/share/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt; fi; chmod 644 /usr/local/share/capture-ca.crt
ENV NODE_EXTRA_CA_CERTS=/usr/local/share/capture-ca.crt
