# capture-only, NOT part of the tutorial: a laptop with "Python and the Google Cloud CLI"
# (README "Before you begin" step 4), no Google account signed in.
FROM gcr.io/google.com/cloudsdktool/google-cloud-cli:slim
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \
 && rm -f /etc/apt/sources.list.d/google-cloud-sdk.list \
 && apt-get update -qq && apt-get install -y -qq --no-install-recommends python3 python-is-python3 >/dev/null \
 && cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && rm -rf /var/lib/apt/lists/* && useradd -m -s /bin/bash student
ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt
USER student
WORKDIR /home/student
