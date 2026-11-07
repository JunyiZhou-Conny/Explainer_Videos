# capture-only, NOT part of the tutorial: dlops/cheese-app-api-service + the recording proxy's CA, re-tagged as dlops/cheese-app-api-service
FROM dlops/cheese-app-api-service
USER root
COPY capture-ca.crt /usr/local/share/capture-ca.crt
RUN for f in /etc/ssl/certs/ca-certificates.crt; do [ -f $f ] && cat /usr/local/share/capture-ca.crt >> $f; done; \
    for f in /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list; do [ -f $f ] && sed -i 's|http://deb.debian.org|https://deb.debian.org|g; s|http://security.debian.org|https://security.debian.org|g' $f; done; true
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt NODE_EXTRA_CA_CERTS=/usr/local/share/capture-ca.crt UV_NATIVE_TLS=1
USER app
