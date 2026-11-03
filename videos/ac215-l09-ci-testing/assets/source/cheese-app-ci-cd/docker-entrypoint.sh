#!/bin/bash

set -e

export PATH="/home/app/.local/bin:$PATH"

echo "Container is running!!!"

# If arguments are passed, execute them instead of starting the server
if [ $# -gt 0 ]; then
  echo "Executing command: $@"
  exec "$@"
fi

# Otherwise, start the server
if [ "${DEV}" = "1" ]; then
  echo "Running in DEV mode"
  # Development: auto-reload on code changes
  uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload --log-level debug
else
  echo "Running in PROD mode"
  # Production: optimized settings
  uvicorn api.service:app --host 0.0.0.0 --port 9000 --workers 4
fi
