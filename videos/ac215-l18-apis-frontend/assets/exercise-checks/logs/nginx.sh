#!/bin/bash
# Production-frontend checks (B6, C4, C5) with nginx:1.31.8-alpine (the base of main's production
# Dockerfile) and main's nginx.conf.template (byte-identical at e98fa55 and 447b5c3), mounted where the
# Dockerfile copies it. Check-only stand-ins: a two-file dist/ (index.html, assets/index-test.js) instead of
# the Vite build, and main's API without TensorFlow (l18ex/api313:check) as cheese-app-api-service on a
# private network. Host port 18080 stands in for the README's 8080.
# Usage: bash nginx.sh <scratch dir>
D="$(cd "$(dirname "$0")" && pwd)"; W="$1/v2"; A="$W/src/api-service"; T="$W/src/frontend-react/nginx.conf.template"
. "$D/lib.sh"
mkdir -p "$W/dist/assets" && echo '<!doctype html><title>Formaggio</title><div id="root"></div><script type="module" src="/assets/index-test.js"></script>' > "$W/dist/index.html" && echo 'console.log("app")' > "$W/dist/assets/index-test.js"
NG="-p 18080:80 -e API_URL=http://cheese-app-api-service:9000 -v $T:/etc/nginx/templates/default.conf.template:ro -v $W/dist:/usr/share/nginx/html:ro nginx:1.31.8-alpine"
C='-o /dev/null -w "%{http_code} %{content_type}\n"'

step "docker network create l18ex-net >/dev/null && echo network created"
echo "### C4: start nginx before the API exists"
step "docker run --name l18ex-web --network l18ex-net $NG 2>&1 | grep -E 'envsubst|emerg'; docker inspect -f 'exit code {{.State.ExitCode}}' l18ex-web; docker rm l18ex-web >/dev/null"
echo "### B6: the API first, then nginx"
step "docker run -d --name l18ex-api --network l18ex-net --network-alias cheese-app-api-service -e GCP_PROJECT=your-gcp-project -v $A:/app l18ex/api313:check uvicorn api.service:app --host 0.0.0.0 --port 9000 >/dev/null; docker run -d --name l18ex-web --network l18ex-net $NG >/dev/null; sleep 4; docker logs l18ex-web 2>&1 | grep -E 'emerg|start worker process' | head -1"
for u in /healthz '/api/newsletters?limit=1' /newsletters '/chat?model=llm' /assets/index-test.js /assets/nope.js /nope.js; do
  step "curl -sS $C 'localhost:18080$u'"
done
step "curl -sS -i 'localhost:18080/api/newsletters?limit=1' | tr -d '\r' | grep -iE '^(HTTP|server|content-type)'; curl -sS 'localhost:18080/api/newsletters?limit=1' | python3 -c 'import json,sys; print([n[\"title\"] for n in json.load(sys.stdin)])'"
step "curl -sS -i localhost:18080/assets/index-test.js | tr -d '\r' | grep -i '^cache-control'; curl -sS -i localhost:18080/newsletters | tr -d '\r' | grep -i '^cache-control'"
step "docker logs l18ex-api 2>&1 | grep -E '\"GET ' | sed -E 's/^INFO: +[0-9.:]+ - //'"
echo "### C4 (b): the API goes away while nginx keeps running"
step "docker stop l18ex-api >/dev/null; curl -sS $C 'localhost:18080/api/newsletters?limit=1'; curl -sS $C localhost:18080/newsletters"
step "docker logs l18ex-web 2>&1 | grep -E '\[error\]' | sed -E 's/^[0-9/: ]+//; s/, client.*//' | head -2"
step "docker rm -f l18ex-web >/dev/null; docker start l18ex-api >/dev/null && echo api started again"
echo "### C5: one changed character, proxy_pass \${API_URL}/; (a URI part after the address)"
sed 's|proxy_pass \${API_URL};|proxy_pass ${API_URL}/;|' "$T" > "$W/slash.conf.template"
step "diff $T $W/slash.conf.template"
step "sleep 3; docker run -d --name l18ex-web --network l18ex-net -p 18080:80 -e API_URL=http://cheese-app-api-service:9000 -v $W/slash.conf.template:/etc/nginx/templates/default.conf.template:ro -v $W/dist:/usr/share/nginx/html:ro nginx:1.31.8-alpine >/dev/null; sleep 3; curl -sS -w ' [HTTP %{http_code}]\n' 'localhost:18080/api/newsletters?limit=1'"
step "docker logs l18ex-api 2>&1 | grep -E '\"GET ' | sed -E 's/^INFO: +[0-9.:]+ - //' | tail -1"
step "docker rm -f l18ex-web l18ex-api >/dev/null; docker network rm l18ex-net >/dev/null; docker ps -a --filter name=l18ex- --format '{{.Names}}' | wc -l"
