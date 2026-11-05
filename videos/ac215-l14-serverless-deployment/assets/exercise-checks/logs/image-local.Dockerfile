# Check-only copy of tutorial/app/Dockerfile (46cc62f), used because Docker Hub answered 429 to the pull
# of the public image during these checks. Identical lines, plus the recording proxy's CA (marked CHECK-ONLY)
# so pip can reach PyPI through the intercepting proxy. Built from tutorial/app/ at 46cc62f.
FROM python:3.12-slim-bookworm
# CHECK-ONLY: trust the session proxy's CA during the build and at run time
COPY proxy-ca.crt /usr/local/share/proxy-ca.crt
ENV PIP_CERT=/usr/local/share/proxy-ca.crt SSL_CERT_FILE=/usr/local/share/proxy-ca.crt REQUESTS_CA_BUNDLE=/usr/local/share/proxy-ca.crt
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PORT=8080
WORKDIR /app
COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock
COPY pyproject.toml ./
COPY translation_demo ./translation_demo
COPY examples ./examples
RUN pip install --no-cache-dir --no-deps . && useradd --uid 1000 --create-home app
USER app
EXPOSE 8080
CMD ["python", "-m", "translation_demo", "serve"]
