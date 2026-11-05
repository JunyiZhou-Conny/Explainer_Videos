# Check-only image for main's API (not a tutorial file): Dockerfile.dev's base, uv and user, the
# packages of main's uv.lock (dev group included) EXCEPT tensorflow (2.21 is too big for these checks;
# the API imports it only inside load_cnn_model/make_prediction), curl, and the session proxy's CA.
FROM python:3.13-slim-bookworm
COPY ca.crt /usr/local/share/ca-certificates/session-proxy.crt
ENV PIP_CERT=/usr/local/share/ca-certificates/session-proxy.crt SSL_CERT_FILE=/usr/local/share/ca-certificates/session-proxy.crt \
    UV_NATIVE_TLS=1 PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_ROOT_USER_ACTION=ignore PYTHONUNBUFFERED=1
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get -o Acquire::https::CaInfo=$PIP_CERT update -qq && \
    apt-get -o Acquire::https::CaInfo=$PIP_CERT install -y -qq --no-install-recommends curl >/dev/null && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -q uv==0.13.6 && useradd -ms /bin/bash app -d /home/app -u 1000
COPY pyproject.toml uv.lock /tmp/lock/
RUN cd /tmp/lock && uv export --frozen --no-hashes --all-groups --no-emit-project > all.txt && \
    grep -v '^tensorflow' all.txt > req.txt && uv pip install --system -q -r req.txt && \
    grep -c . all.txt req.txt
USER app
WORKDIR /app
