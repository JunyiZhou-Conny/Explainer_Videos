# Check-only image for the v1 API (not a tutorial file): python:3.12-slim-bookworm, the v1 uv.lock
# versions of the four packages service.py needs, curl, and the session proxy's CA (pip and apt need it).
FROM python:3.12-slim-bookworm
COPY ca.crt /usr/local/share/ca-certificates/session-proxy.crt
ENV PIP_CERT=/usr/local/share/ca-certificates/session-proxy.crt PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_ROOT_USER_ACTION=ignore
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get -o Acquire::https::CaInfo=$PIP_CERT update -qq && \
    apt-get -o Acquire::https::CaInfo=$PIP_CERT install -y -qq --no-install-recommends curl >/dev/null && \
    rm -rf /var/lib/apt/lists/* && \
    pip install -q fastapi==0.120.4 starlette==0.49.3 pydantic==2.12.3 uvicorn==0.38.0 && \
    useradd -ms /bin/bash app -d /home/app -u 1000
USER app
WORKDIR /app
