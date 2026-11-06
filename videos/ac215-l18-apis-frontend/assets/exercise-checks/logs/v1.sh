#!/bin/bash
# v1 API checks (B1, B2, B3, B4, C6), from the host: cheese-app-v1's api/service.py at ce03a10 copied
# into a scratch folder that is mounted at /app (as docker-shell.sh mounts your code), run by uvicorn
# in the check image l18ex/py312:check. Host port 19000 stands in for the README's 9000.
# Usage: bash v1.sh <scratch dir>
D="$(cd "$(dirname "$0")" && pwd)"; SRC="$D/../../source/cheese-app-v1/src/api-service"; W="$1/v1"
. "$D/lib.sh"
export W
mkdir -p "$W/api" && cp "$SRC/api/service.py" "$W/api/service.py" && chmod -R a+rwX "$W"
RUN="docker run -d --name l18ex-v1 -p 19000:9000 -v $W:/app l18ex/py312:check"
wait_up() { for i in $(seq 1 40); do docker exec l18ex-v1 curl -s -o /dev/null localhost:9000/ 2>/dev/null && return; sleep 0.25; done; }

echo "### B1: --host 127.0.0.1 instead of 0.0.0.0"
step "$RUN uvicorn api.service:app --host 127.0.0.1 --port 9000 >/dev/null; sleep 3; docker logs l18ex-v1 2>&1 | grep 'Uvicorn running'"
step "docker exec l18ex-v1 curl -sS http://localhost:9000/"
step "curl -sS http://localhost:19000/"
step "docker port l18ex-v1"
step "docker rm -f l18ex-v1 >/dev/null"
step "$RUN uvicorn api.service:app --host 0.0.0.0 --port 9000 >/dev/null; sleep 3; docker logs l18ex-v1 2>&1 | grep 'Uvicorn running'"
step "curl -sS http://localhost:19000/"
step "docker rm -f l18ex-v1 >/dev/null"

echo "### B2, B3: the README's square_root, plus a path parameter (README's uvicorn line, --reload)"
step "$RUN uvicorn api.service:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir api/ >/dev/null; sleep 3; docker logs l18ex-v1 2>&1 | grep -E 'Uvicorn running|reloader'"
cat >> "$W/api/service.py" <<'PY'


@app.get("/square_root/")
async def square_root(x: float = 1, y: float = 2):
    z = x**2 + y**2
    return z**0.5


@app.get("/hypot/{x}")
async def hypot(x: float, y: float = 0):
    return (x**2 + y**2) ** 0.5
PY
sleep 4
step "docker logs l18ex-v1 2>&1 | grep -E 'StatReload detected|Application startup complete' | tail -2"
step "curl -sS 'http://localhost:19000/hypot/3?y=4'; echo; curl -sS http://localhost:19000/hypot/3; echo; curl -sS -w ' [HTTP %{http_code}]' http://localhost:19000/hypot/abc"
step "curl -sS http://localhost:19000/openapi.json | python3 -c 'import json,sys; p=json.load(sys.stdin)[\"paths\"][\"/hypot/{x}\"][\"get\"][\"parameters\"]; [print(q[\"name\"], q[\"in\"], \"required\" if q.get(\"required\") else \"optional\", q[\"schema\"]) for q in p]'"
step "curl -sS -i 'http://localhost:19000/square_root?x=3&y=4' | tr -d '\r' | grep -iE '^(HTTP|location)'"
step "curl -sS -L -w ' [HTTP %{http_code}, %{num_redirects} redirect]' 'http://localhost:19000/square_root?x=3&y=4'"
step "curl -sS -w ' [HTTP %{http_code}]' 'http://localhost:19000/square_root/?x=abc'"
step "curl -sS -i -X POST 'http://localhost:19000/square_root?x=3&y=4' | tr -d '\r' | grep -iE '^(HTTP|location)'"
step "curl -sS -L -X POST -w ' [HTTP %{http_code}, %{num_redirects} redirect]' 'http://localhost:19000/square_root?x=3&y=4'"

echo "### B4: a slow route as async def vs def (two requests at the same time)"
cat >> "$W/api/service.py" <<'PY'


import time


@app.get("/slow_async")
async def slow_async():
    time.sleep(2)  # a blocking call inside async def
    return "done"


@app.get("/slow_def")
def slow_def():
    time.sleep(2)  # the same blocking call in a plain def: FastAPI runs it in a thread
    return "done"
PY
sleep 4
for r in slow_async slow_def; do
  step "s=\$(date +%s.%N); curl -s localhost:19000/$r >/dev/null & curl -s localhost:19000/$r >/dev/null & wait; python3 -c \"print('two requests to /$r took %.1f s' % (\$(date +%s.%N) - \$s))\""
done

echo "### C6: CORS on v1 (CORSMiddleware allow_origins=['*']), and an unhandled error"
cat >> "$W/api/service.py" <<'PY'


from fastapi import HTTPException


@app.get("/boom")
def boom():
    return 1 / 0  # an unhandled exception


@app.get("/handled")
def handled():
    raise HTTPException(status_code=500, detail="handled error")
PY
sleep 4
step "curl -sS -i -H 'Origin: http://localhost:8080' http://localhost:19000/ | tr -d '\r' | grep -iE '^(HTTP|access-control)'"
step "curl -sS -i -X OPTIONS -H 'Origin: http://localhost:8080' -H 'Access-Control-Request-Method: POST' -H 'Access-Control-Request-Headers: content-type,x-session-id' http://localhost:19000/square_root/ | tr -d '\r' | grep -iE '^(HTTP|access-control)'"
step "curl -sS -i -H 'Origin: http://localhost:8080' http://localhost:19000/handled | tr -d '\r' | grep -iE '^(HTTP|access-control|\{)'"
step "curl -sS -i -H 'Origin: http://localhost:8080' http://localhost:19000/boom | tr -d '\r' | grep -iE '^(HTTP|access-control|Internal)'"
step "docker logs l18ex-v1 2>&1 | grep -E 'ZeroDivisionError|GET /boom'"
echo "### C6: the same app without the middleware (service.py lines 7-14 removed, the way main has no CORS)"
python3 - "$W/api/service.py" <<'PY'
import sys
p = sys.argv[1]; s = open(p).read()
start = s.index("# Enable CORSMiddleware"); end = s.index(")\n", start) + 2
open(p, "w").write(s[:start] + s[end:])
PY
sleep 4
step "grep -c CORSMiddleware \$W/api/service.py"
step "curl -sS -i -H 'Origin: http://localhost:8080' http://localhost:19000/ | tr -d '\r' | grep -iE '^(HTTP|access-control)'"
step "curl -sS -i -X OPTIONS -H 'Origin: http://localhost:8080' -H 'Access-Control-Request-Method: POST' -H 'Access-Control-Request-Headers: content-type,x-session-id' http://localhost:19000/square_root/ | tr -d '\r' | grep -iE '^(HTTP|access-control|allow)'"
step "docker logs l18ex-v1 2>&1 | grep -E '\"(GET|POST|OPTIONS) ' | sed -E 's/^INFO: +[0-9.:]+ - //'"
step "docker rm -f l18ex-v1 >/dev/null; docker ps -a --filter name=l18ex- --format '{{.Names}}' | wc -l"
