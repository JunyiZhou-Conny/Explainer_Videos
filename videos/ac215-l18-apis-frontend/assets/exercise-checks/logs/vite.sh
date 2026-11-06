#!/bin/bash
# Vite proxy checks (B7): the dev server alone (vite 8.3.5, no React, no app code) with a vite.config.js
# that keeps main's server block (vite.config.js lines 9-14) and changes only the proxy target; main's
# API without TensorFlow as cheese-app-api-service on a private network. Host port 13000 stands in for 3000.
# Usage: bash vite.sh <scratch dir>
D="$(cd "$(dirname "$0")" && pwd)"; W="$1"; A="$W/v2/src/api-service"
. "$D/lib.sh"
mkdir -p "$W/vite-ctx" && cp "$W/ca.crt" "$W/vite-ctx/"
step "docker build -q --network host --build-arg HTTPS_PROXY=$HTTPS_PROXY --build-arg https_proxy=$HTTPS_PROXY -t l18ex/vite:check -f $D/vite-check.Dockerfile $W/vite-ctx >/dev/null && docker run --rm l18ex/vite:check npx vite --version"
for target in "process.env.API_URL || 'http://cheese-app-api-service:9000'" "'http://localhost:9000'"; do
  mkdir -p "$W/vite-cfg" && cat > "$W/vite-cfg/vite.config.js" <<JS
import { defineConfig } from 'vite'
export default defineConfig({
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    proxy: { '/api': $target },
  },
})
JS
  chmod -R a+rX "$W/vite-cfg"
  step "grep proxy $W/vite-cfg/vite.config.js"
  step "docker network create l18ex-net >/dev/null; docker run -d --name l18ex-api --network l18ex-net --network-alias cheese-app-api-service -e GCP_PROJECT=your-gcp-project -v $A:/app l18ex/api313:check uvicorn api.service:app --host 0.0.0.0 --port 9000 >/dev/null; docker run -d --name l18ex-vite --network l18ex-net -p 13000:5173 -v $W/vite-cfg/vite.config.js:/app/vite.config.js:ro l18ex/vite:check npx vite >/dev/null; sleep 6; docker logs l18ex-vite 2>&1 | grep -E 'ready|Local|Network'"
  step "curl -sS -i 'localhost:13000/api/newsletters?limit=1' | tr -d '\r' | grep -iE '^(HTTP|server|content-length)'"
  step "docker logs l18ex-vite 2>&1 | grep -A1 'proxy error' | head -2"
  step "docker rm -f l18ex-vite l18ex-api >/dev/null; docker network rm l18ex-net >/dev/null; echo removed"
done
step "docker ps -a --filter name=l18ex- --format '{{.Names}}' | wc -l"
