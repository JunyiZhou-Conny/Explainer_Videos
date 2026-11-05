# capture-only: cgumb/ac215-translation-demo:lecture14-agent-platform-20261022 + the recording proxy's CA (re-tagged under the same name)
FROM cgumb/ac215-translation-demo:lecture14-agent-platform-20261022
USER root
COPY capture-ca.crt /tmp/capture-ca.crt
RUN cat /etc/ssl/certs/ca-certificates.crt /tmp/capture-ca.crt > /etc/ssl/capture-bundle.crt && rm /tmp/capture-ca.crt
ENV SSL_CERT_FILE=/etc/ssl/capture-bundle.crt REQUESTS_CA_BUNDLE=/etc/ssl/capture-bundle.crt
USER app
