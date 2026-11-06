#!/bin/bash
# main's API checks (B3, B5, C2, C3), from the host. Code: cheese-app-v2 src/api-service, byte-identical
# at e98fa55 and 447b5c3 (git archive of the read-only clone into a scratch folder, mounted at /app as
# docker-shell.sh mounts it). Image: l18ex/api313:check (main's uv.lock without TensorFlow).
# No Google credentials anywhere: GOOGLE_APPLICATION_CREDENTIALS is not set, GCP_PROJECT is a placeholder.
# Usage: bash api.sh <scratch dir>
D="$(cd "$(dirname "$0")" && pwd)"; W="$1/v2"; A="$W/src/api-service"
. "$D/lib.sh"
export A W
mkdir -p "$W/persistent" && chmod -R a+rwX "$W"
ENV="-e GCP_PROJECT=your-gcp-project -e PERSISTENT_DIR=/persistent"
S=00000000-0000-4000-8000-000000000001
J='-H Content-Type:application/json'

echo "### the tests, as in the README (pytest inside the container)"
step "docker run --rm -v $A:/app l18ex/api313:check pytest -q 2>&1 | tail -2"

echo "### B3, B5: the API without the model (TensorFlow is not in this check image, so the CNN never loads)"
step "docker run -d --name l18ex-api -p 19000:9000 $ENV -v $A:/app -v $W/persistent:/persistent l18ex/api313:check uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload --reload-dir api/ >/dev/null; sleep 6; docker logs l18ex-api 2>&1 | grep -E 'Application startup complete|ModuleNotFoundError'"
step "curl -sS -w ' [HTTP %{http_code}]\n' localhost:19000/healthz; curl -sS -w ' [HTTP %{http_code}]\n' localhost:19000/readyz"
step "curl -sS -i 'localhost:19000/api/newsletters/?limit=1' | tr -d '\r' | grep -iE '^(HTTP|location)'"
step "curl -sS -i -X POST $J -H 'X-Session-ID: $S' -d '{\"content\":\"hi\"}' localhost:19000/api/llm/chats/ | tr -d '\r' | grep -iE '^(HTTP|location)'"
step "curl -sS -w ' [HTTP %{http_code}]\n' -X POST $J -d '{\"content\":\"hi\"}' localhost:19000/api/llm/chats"
step "curl -sS -w ' [HTTP %{http_code}]\n' -X POST $J -H 'X-Session-ID: string' -d '{\"content\":\"hi\"}' localhost:19000/api/llm/chats"
step "curl -sS -w ' [HTTP %{http_code}]\n' -H 'X-Session-ID: ../../etc' localhost:19000/api/llm/chats"
step "curl -sS -w ' [HTTP %{http_code}]\n' -X POST $J -H 'X-Session-ID: $S' -d '{\"content\":\"\"}' localhost:19000/api/llm/chats"
step "curl -sS -w ' [HTTP %{http_code}]\n' -X POST $J -H 'X-Session-ID: $S' -d '{\"image\":\"aGVsbG8=\"}' localhost:19000/api/llm-cnn/chats"
step "curl -sS -w ' [HTTP %{http_code}]\n' -X POST $J -H 'X-Session-ID: $S' -d '{\"content\":\"How is cheese made?\",\"mode\":\"llm\"}' localhost:19000/api/llm/chats"
step "docker logs l18ex-api 2>&1 | grep -E '^[A-Za-z.]*(Error|Exception)[A-Za-z]*:' | sort | uniq -c"
step "find $W/persistent -maxdepth 4 | sed \"s|$W/||\" | sort"
step "docker rm -f l18ex-api >/dev/null"

echo "### C2: a persistent folder that belongs to root (what Docker creates on Linux when the folder is missing)"
step "mkdir -p $W/rootowned && chown root:root $W/rootowned && chmod 755 $W/rootowned && ls -ld $W/rootowned | awk '{print \$1, \$3, \$4}'"
step "docker run -d --name l18ex-api -p 19000:9000 $ENV -e PYTHONPATH=/tfstub -v $D/tfstub:/tfstub:ro -v $A:/app -v $W/rootowned:/persistent l18ex/api313:check uvicorn api.service:app --host 0.0.0.0 --port 9000 >/dev/null; sleep 6; docker logs l18ex-api 2>&1 | grep -E 'Application startup complete|PermissionError'"
step "sleep 10; curl -sS -w ' [HTTP %{http_code}]\n' localhost:19000/readyz"
step "curl -sS -w ' [HTTP %{http_code}]\n' -X POST $J -H 'X-Session-ID: $S' -d '{\"image\":\"aGVsbG8=\"}' localhost:19000/api/llm-cnn/chats"
step "docker rm -f l18ex-api >/dev/null"

echo "### C3: the model in place, but Chroma not started yet. Check-only: the GitHub packet download through the"
echo "### session proxy timed out (504) on the first run, so the model folder is pre-created with placeholder files"
echo "### (the TF stand-in never reads them); the API and Chroma share a private network, as on cheese-app-network"
M="$W/persistent/experiments/experiment_1760994796"
step "mkdir -p $M && echo '{}' > $M/data_details.json && touch $M/mobilenetv2_train_base_True.keras && chmod -R a+rwX $W/persistent && docker network create l18ex-net >/dev/null && echo network created"
step "docker run -d --name l18ex-api --network l18ex-net -p 19000:9000 $ENV -e PYTHONPATH=/tfstub -v $D/tfstub:/tfstub:ro -v $A:/app -v $W/persistent:/persistent l18ex/api313:check uvicorn api.service:app --host 0.0.0.0 --port 9000 >/dev/null; sleep 6; docker logs l18ex-api 2>&1 | grep -E 'Application startup complete|tf stand-in'"
step "curl -sS -w ' [HTTP %{http_code}]\n' localhost:19000/healthz; curl -sS -w ' [HTTP %{http_code}]\n' localhost:19000/readyz"
step "docker image inspect --format '{{index .RepoDigests 0}}' mirror.gcr.io/chromadb/chroma:1.5.9"
step "docker run -d --name l18ex-chroma --network l18ex-net --network-alias cheese-app-vector-db -e ANONYMIZED_TELEMETRY=FALSE mirror.gcr.io/chromadb/chroma:1.5.9 >/dev/null; for i in \$(seq 1 60); do docker exec l18ex-api curl -s -o /dev/null cheese-app-vector-db:8000/api/v2/heartbeat && break; sleep 1; done; docker exec l18ex-api curl -sS cheese-app-vector-db:8000/api/v2/heartbeat | cut -c1-24"
step "curl -sS -w ' [HTTP %{http_code}]\n' localhost:19000/readyz"
step "docker stop l18ex-chroma >/dev/null; curl -sS -w ' [HTTP %{http_code}]\n' localhost:19000/readyz"
step "docker start l18ex-chroma >/dev/null; for i in \$(seq 1 30); do curl -s -o /dev/null -w '%{http_code}' localhost:19000/readyz | grep -q 200 && break; sleep 1; done; curl -sS -w ' [HTTP %{http_code}]\n' localhost:19000/readyz"
step "docker logs l18ex-api 2>&1 | grep -E '\"GET /(healthz|readyz)' | sed -E 's/^INFO: +[0-9.:]+ - //' | uniq -c"
step "docker rm -f l18ex-api l18ex-chroma >/dev/null; docker network rm l18ex-net >/dev/null; docker ps -a --filter name=l18ex- --format '{{.Names}}' | wc -l"
