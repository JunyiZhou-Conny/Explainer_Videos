#!/bin/bash
# C8: where docker-entrypoint.dev.sh's api_server function exists. A stand-in with the same bash
# mechanics as its lines 12-16 and 27 (define, export -f, exec /bin/bash) in python:3.13-slim-bookworm,
# then a second shell opened the way docker-shell.sh does when the container already runs (docker exec).
D="$(cd "$(dirname "$0")" && pwd)"
. "$D/lib.sh"
step "docker run -dit --name l18ex-shell python:3.13-slim-bookworm bash -c 'api_server() { echo uvicorn would start here; }; export -f api_server; exec /bin/bash' >/dev/null && echo started"
step "docker exec l18ex-shell bash -c 'tr \"\\\\0\" \"\\\\n\" < /proc/1/environ | grep -A1 BASH_FUNC_api_server'"
step "docker exec l18ex-shell bash -c 'type api_server'"
step "docker rm -f l18ex-shell >/dev/null; docker ps -a --filter name=l18ex- --format '{{.Names}}' | wc -l"
