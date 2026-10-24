# Multi-stage Dockerfile for Cheese App API Service
FROM python:3.11-slim-bookworm

# Prevent apt from showing prompts
ENV DEBIAN_FRONTEND=noninteractive

# Python configuration
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        build-essential \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip

# Create non-root user
RUN useradd -ms /bin/bash app -d /home/app -u 1000 && \
    mkdir -p /app && \
    chown app:app /app

# Switch to non-root user
USER app
WORKDIR /app

# Copy pyproject.toml first for better caching
COPY --chown=app:app pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir --user .

# Copy application code
COPY --chown=app:app src/api-service/api/ ./api/
COPY --chown=app:app tests/ ./tests/
COPY --chown=app:app pytest.ini ./
COPY --chown=app:app docker-entrypoint.sh ./

# Make entrypoint executable
USER root
RUN chmod +x docker-entrypoint.sh
USER app

# Expose port
EXPOSE 9000

# Entry point
ENTRYPOINT ["/bin/bash", "docker-entrypoint.sh"]
