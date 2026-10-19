#!/bin/bash
# Runs inside the fresh capture container ("laptop", see capture.sh) as user `student`, recording
# each tutorial command's output to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# Segments (cheese-app-v0 README top to bottom, in README order):
#   pre   clone + pin check + the secrets/ folder next to the repo (placeholder key, see ASSETS.md)
#         + the capture-only base images
#   net   README "Create the Docker Network" + idempotence extras
#   rag1  README "Build the Vector DB": GCP_PROJECT edit, sh docker-shell.sh (build + ChromaDB up),
#         /secrets sanity extras, ChromaDB survives exit
#   rag2  the first cli.py command verbatim (chunk runs for real; embed fails with the documented
#         DefaultCredentialsError -- there are NO GCP credentials here, see ASSETS.md)
#   rag3  the second cli.py command verbatim + the chunk artifacts it left on the host
#   rag4  the google.auth sanity check (digest §4 step 3), honest DefaultCredentialsError
#   api1  README "Run API Service Container": GCP_PROJECT edit, the unmodified script aborting on
#         the existing network (the digest's gotcha #1), the line-14 fix
#   api2  sh docker-shell.sh (build + run) + uvicorn_server + curl/CORS/DNS extras while it runs
#   fe1   README "Run Frontend Container": sh docker-shell.sh + npm install
#   fe2   npm run dev + port/title/CORS extras while it runs
#   cors  ChromaDB's CORS guest list, probed with curl preflights (digest §3.6)
#   down  README:106 docker compose down + persistence extras + network rm
# Steps marked "extra" are not in the README; they are checks the video uses.
OUT=$1; SEG=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
cd ~

step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1; echo "[exit $?]"; } > "$OUT/$name.txt"
}
istep() {  # istep <name> <command> [<prompt regex> <typed line>]...   (in a terminal, typed)
  local name=$1 cmd=$2; shift 2
  local args=()
  while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
  { echo "\$ $cmd"
    python3 "$HERE/ptyrun.py" --cols "${PTY_COLS:-80}" --rows "${PTY_ROWS:-24}" --timeout "${PTY_TIMEOUT:-900}" \
      "${args[@]}" -- bash -c "$cmd"
    echo "[exit $?]"; } > "$OUT/$name.txt"
}
hub_retry() {  # hub_retry step|istep <name> <args...>   (recording sandbox only: CAPTURE_HUB_WAIT set)
  # Docker Hub limits anonymous pulls per IP and the sandbox's egress IPs are shared, so a pull can
  # fail with "toomanyrequests" / "429 Too Many Requests" for reasons that have nothing to do with
  # the tutorial. Run the step again until it gets through; the file keeps the run that did,
  # capture-only/hub-retries.txt counts the failed attempts.
  local fn=$1 name=$2 i
  for i in $(seq 60); do
    "$fn" "$name" "${@:3}"
    grep -q "toomanyrequests\|429 Too Many Requests" "$OUT/$name.txt" || return 0
    [ -n "$CAPTURE_HUB_WAIT" ] || return 0
    mkdir -p "$OUT/capture-only"
    echo "$name: attempt $i hit Docker Hub's rate limit, retrying in 30 s" >> "$OUT/capture-only/hub-retries.txt"
    sleep 30
  done
}
capture_only_bases() {  # recording sandbox only (CAPTURE_CA set); see ASSETS.md, "capture-only"
  # The tutorial's builds and npm installs need TLS, and the sandbox's TLS is re-signed by its
  # proxy. The two base images the repo's Dockerfiles use are rebuilt with that proxy's CA and
  # re-tagged under the same names, so every tutorial command builds/runs unchanged.
  [ -n "$CAPTURE_CA" ] || return 0
  local d; d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"
  mkdir -p "$OUT/capture-only"
  cat > "$d/Dockerfile" <<'EOF'
# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through a
# TLS-intercepting proxy. Same python:3.12-slim-bookworm plus that proxy's CA, https apt sources
# and the CA env vars, re-tagged under the same name so that llm-rag/Dockerfile and
# api-service/Dockerfile build unchanged.
FROM python:3.12-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    UV_NATIVE_TLS=1
EOF
  cp "$d/Dockerfile" "$OUT/capture-only/python-base.Dockerfile"
  hub_retry step capture-only/python-base-build "docker build -t python:3.12-slim-bookworm $d"
  cat > "$d/Dockerfile" <<'EOF'
# capture-only, NOT part of the tutorial: same node:20-alpine plus the recording proxy's CA
# (for apk and npm), re-tagged under the same name so that frontend-ai-chatbot/Dockerfile.dev
# builds unchanged and `npm install` can download through the proxy.
FROM node:20-alpine
COPY capture-ca.crt /tmp/capture-ca.crt
RUN cat /tmp/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt && rm /tmp/capture-ca.crt
ENV NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt \
    NPM_CONFIG_CAFILE=/etc/ssl/certs/ca-certificates.crt
EOF
  cp "$d/Dockerfile" "$OUT/capture-only/node-base.Dockerfile"
  hub_retry step capture-only/node-base-build "docker build -t node:20-alpine $d"
  rm -rf "$d"
}
CTRLC=$'\x03'
AUTHCHECK='python -c "import google.auth; c, p = google.auth.default(); print(type(c).__name__, getattr(c, '"'"'service_account_email'"'"', None), p)"'

case $SEG in
pre)
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; docker compose version; git --version"   # extra
  # --- README "Prerequisites": "Cloned this repository" (README:44; this is the repo's address)
  step 01-clone "git clone https://github.com/dlops-io/cheese-app-v0"
  cd cheese-app-v0
  step 02-git-log "git log -1 --format='%H %ci'"          # extra: the commit the video uses
  step 03-ls "ls -la"                                     # extra: the repo's top level
  # --- README "Setup GCP Service Account" step 7 + folder tree (README:56-67). The console steps
  # 1-6 are browser clicks (illustration; see ASSETS.md). There is NO real key here: an obviously
  # invalid placeholder stands in so the folder structure can be shown (ASSETS.md, capture-only).
  step 04-mkdir-secrets "mkdir ../secrets"                # extra: the README shows the tree, not a command
  mkdir -p "$OUT/capture-only"
  cat > ../secrets/llm-service-account.json <<'EOF'
{
  "type": "service_account",
  "project_id": "your-gcp-project",
  "private_key_id": "0000000000000000000000000000000000000000",
  "private_key": "-----BEGIN PRIVATE KEY-----\nPLACEHOLDER-THIS-IS-NOT-A-REAL-KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "llm-service-account@your-gcp-project.iam.gserviceaccount.com",
  "client_id": "000000000000000000000",
  "token_uri": "https://oauth2.googleapis.com/token"
}
EOF
  cp ../secrets/llm-service-account.json "$OUT/capture-only/placeholder-key.json"
  cd ~
  step 05-tree "tree -L 2 ."                              # extra: the README:60-67 folder structure
  step 06-ls-secrets "ls -la secrets"                     # extra: digest step-0/1 checkpoint
  capture_only_bases
  ;;
net)
  # --- README "Create the Docker Network" (README:74)
  step 10-network-create "docker network inspect cheese-app-network >/dev/null 2>&1 || docker network create cheese-app-network"
  step 11-network-create-again "docker network inspect cheese-app-network >/dev/null 2>&1 || docker network create cheese-app-network"   # extra: the README form is idempotent (exit 0 again)
  step 12-network-ls "docker network ls"                  # extra
  step 13-network-inspect "docker network inspect cheese-app-network"   # extra
  ;;
rag1)
  cd cheese-app-v0/llm-rag
  # --- README "Build the Vector DB" step 2 (README:84): the README says to edit the file; sed is
  # the editor here, and the step shows the edited line
  step 20-edit-gcp-project "sed -i 's|export GCP_PROJECT=\"ac215-project\" # CHANGE TO YOUR PROJECT ID|export GCP_PROJECT=\"your-gcp-project\"|' docker-shell.sh && sed -n '6,9p' docker-shell.sh"
  # --- README step 3: sh docker-shell.sh (README:88). Builds llm-rag-cli, pulls + starts ChromaDB,
  # opens bash in the CLI container. Typed inside (extras, digest §4 step 3 sanity checks):
  # ls -la /secrets, the env vars, exit. ChromaDB keeps running after exit (README:106).
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=2400 hub_retry istep 21-docker-shell "sh docker-shell.sh" \
    ':/app\$ $' 'ls -la /secrets' \
    ':/app\$ $' 'echo $GOOGLE_APPLICATION_CREDENTIALS $GCP_PROJECT' \
    ':/app\$ $' 'exit'
  step 22-docker-ps "docker ps"                           # extra: llm-rag-chromadb survived the exit
  step 23-curl-chroma-version "curl -s http://localhost:8000/api/v2/version"   # extra: digest checkpoint; the frontend calls the same route (hooks.jsx:14)
  ;;
rag2)
  cd cheese-app-v0/llm-rag
  # capture-only: there are no GCP credentials in this sandbox. The placeholder key is moved away
  # so the cloud steps fail with the honest, documented error (DefaultCredentialsError: File
  # /secrets/llm-service-account.json was not found) instead of a parse error on the placeholder.
  mkdir -p "$OUT/capture-only"
  if [ -f ~/secrets/llm-service-account.json ]; then
    mv ~/secrets/llm-service-account.json ~/placeholder-key-removed.json
    echo "rag2: moved the placeholder key out of ~/secrets so cloud steps show the documented DefaultCredentialsError" >> "$OUT/capture-only/placeholder-key-moves.txt"
  fi
  # --- README step 4, first command (README:94): chunk runs for real; embed needs Vertex AI and
  # fails honestly (see ASSETS.md, "What cannot run here")
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=2400 istep 24-cli-char-split "sh docker-shell.sh" \
    ':/app\$ $' 'python cli.py --chunk --embed --load --chunk_type char-split' \
    ':/app\$ $' 'exit'
  ;;
rag3)
  cd cheese-app-v0/llm-rag
  # --- README step 4, second command (README:95)
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=2400 istep 25-cli-recursive-split "sh docker-shell.sh" \
    ':/app\$ $' 'python cli.py --chunk --embed --load --chunk_type recursive-split' \
    ':/app\$ $' 'exit'
  step 26-outputs-ls "ls -la outputs | head -16"          # extra: the chunk JSONLs on the host, through the /app bind mount (README:101)
  step 27-chunk-counts "wc -l outputs/chunks-char-split-*.jsonl | tail -1; wc -l outputs/chunks-recursive-split-*.jsonl | tail -1"   # extra: how many chunks each splitter made
  step 28-chunk-sample "head -1 'outputs/chunks-char-split-Tolminc Cheese.jsonl' | cut -c1-300"   # extra: one real chunk
  ;;
rag4)
  cd cheese-app-v0/llm-rag
  # --- digest §4 step 3 sanity check (suggested, extra): who does ADC find? Honest answer here:
  # nobody -- the documented DefaultCredentialsError (digest §6 #2), because /secrets is empty.
  PTY_COLS=110 PTY_ROWS=50 istep 29-auth-check "sh docker-shell.sh" \
    ':/app\$ $' 'ls -la /secrets' \
    ':/app\$ $' "$AUTHCHECK" \
    ':/app\$ $' 'exit'
  ;;
api1)
  cd cheese-app-v0/api-service
  # --- README "Run API Service Container" step 2 (README:130)
  step 30-edit-gcp-project "sed -i 's|export GCP_PROJECT=\"ac215-project\" # CHANGE TO YOUR PROJECT ID|export GCP_PROJECT=\"your-gcp-project\"|' docker-shell.sh && sed -n '7,11p' docker-shell.sh"
  # --- README step 3 (README:134), unmodified script: docker-shell.sh:14 runs a bare
  # `docker network create` under `set -e`, and the network already exists (README:74 created it),
  # so the script aborts before building anything. The digest's gotcha #1, captured live.
  step 31-docker-shell-aborts "sh docker-shell.sh"
  # --- the digest §4 step 4.2 fix (extra): make line 14 the README's idempotent form
  step 32-fix-network-line "sed -i 's|^docker network create cheese-app-network$|docker network inspect cheese-app-network >/dev/null 2>\&1 \|\| docker network create cheese-app-network|' docker-shell.sh && sed -n '14p' docker-shell.sh"
  ;;
api2)
  cd cheese-app-v0/api-service
  # --- README step 3 again (now past the network line) and step 4: uvicorn_server (README:140).
  # While the server runs, a second shell (below) fetches the evidence the browser steps would
  # show, then requests /capture-done; its 404 access-log line is the cue to Ctrl-C and exit.
  ( for i in $(seq 3300); do curl -s -o /dev/null --max-time 5 http://localhost:9000/ && break; sleep 1; done
    sleep 2
    step 34-curl-root "curl -s http://localhost:9000/"                 # extra: README:147 'Serve the API at http://localhost:9000'
    step 35-curl-docs "curl -s -o /dev/null -w '%{http_code} %{content_type}\n' http://localhost:9000/docs"   # extra: README:149's /docs answers
    step 36-openapi-routes "curl -s http://localhost:9000/openapi.json | python3 -c 'import sys, json; [print(m.upper(), p) for p, ms in json.load(sys.stdin)[\"paths\"].items() for m in ms]'"   # extra: the five routes of README:263-269
    step 37-curl-embedding "curl -s -i 'http://localhost:9000/rag/embedding?text=hello'"   # extra: the digest's first-real-cloud-call check -- honest 500 here (no credentials); the traceback is in 33-docker-shell.txt
    step 38-cors-api "curl -s -D - -o /dev/null -X OPTIONS -H 'Origin: http://localhost:3300' -H 'Access-Control-Request-Method: POST' http://localhost:9000/rag/llm-response"   # extra: FastAPI's allow_origins=['*'] (service.py:17) says yes to any page origin
    step 39-docker-ps "docker ps"                                      # extra: port columns, 9000->9000 and 8000->8000
    step 40-network-inspect "docker network inspect cheese-app-network"   # extra: the API container attached
    step 41-exec-dns-fail "docker exec llm-rag-analysis-api-service python -c \"import urllib.request; print(urllib.request.urlopen('http://llm-rag-chromadb:8000/api/v2/version', timeout=10).read())\""   # extra: digest E5(a) -- different networks, no DNS
    step 42-network-connect "docker network connect cheese-app-network llm-rag-chromadb"   # extra: digest E5(b)
    step 43-exec-dns-ok "docker exec llm-rag-analysis-api-service python -c \"import urllib.request; print(urllib.request.urlopen('http://llm-rag-chromadb:8000/api/v2/version', timeout=10).read())\""   # extra: now Docker DNS resolves it
    step 44-exec-localhost-fail "docker exec llm-rag-analysis-api-service python -c \"import urllib.request; print(urllib.request.urlopen('http://localhost:8000/api/v2/version', timeout=10).read())\""   # extra: digest E5(c) -- localhost is the container itself
    step 45-network-disconnect "docker network disconnect cheese-app-network llm-rag-chromadb"   # extra: back to the tutorial's state
    curl -s -o /dev/null --max-time 20 http://localhost:9000/capture-done
  ) &
  CURLS=$!
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=3600 hub_retry istep 33-docker-shell "sh docker-shell.sh" \
    ':/app\$ $' 'uvicorn_server' \
    'capture-done HTTP/1.1" 404' "$CTRLC" \
    ':/app\$ $' 'exit'
  wait $CURLS
  step 46-docker-ps-after "docker ps"                     # extra: --rm removed the API container; ChromaDB stays
  ;;
fe1)
  cd cheese-app-v0/frontend-ai-chatbot
  # --- README "Run Frontend Container" (README:161): build + run, then npm install (README:167)
  # typed inside. node_modules lands in the host folder through the bind mount, so it survives
  # the exit for fe2.
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=2400 hub_retry istep 50-docker-shell-npm-install "sh docker-shell.sh" \
    'bash-[0-9.]+# $' 'npm install' \
    'bash-[0-9.]+# $' 'exit'
  ;;
fe2)
  cd cheese-app-v0/frontend-ai-chatbot
  # --- README step 3, npm run dev (README:168). While Next.js serves, a second shell fetches the
  # pages' titles and the port evidence (the browser steps' server-side half; the pages' cloud
  # calls happen only in a real browser and are recorded/illustrated, see ASSETS.md).
  ( for i in $(seq 1200); do curl -s -o /dev/null --max-time 10 http://localhost:3200/ && break; sleep 1; done
    sleep 2
    step 52-curl-home "curl -s --max-time 300 -o /tmp/l10-home.html -w 'HTTP %{http_code}\n' http://localhost:3200/ && grep -o '<title>[^<]*</title>' /tmp/l10-home.html"   # extra: README:177 'Go to http://localhost:3200'
    step 53-curl-3000-fail "curl -sS --max-time 10 http://localhost:3000/"   # extra: digest gotcha #10 -- the port Next prints is the container's, nothing is published there
    step 54-docker-ps "docker ps"                          # extra: the 3200->3000 port column
    step 55-exec-localhost-3000 "docker exec llm-rag-analysis-frontend-ai-chatbot wget -qO- -T 10 http://localhost:3000/ | grep -o '<title>[^<]*</title>'"   # extra: inside the container, 3000 answers -- one server, two addresses (digest §3.5)
    step 56-curl-chunkviz "curl -s --max-time 300 -o /tmp/l10-chunkviz.html -w 'HTTP %{http_code}\n' http://localhost:3200/chunkviz && grep -o '<title>[^<]*</title>' /tmp/l10-chunkviz.html"   # extra: README:188
    step 57-curl-chromaui "curl -s --max-time 300 -o /tmp/l10-chromaui.html -w 'HTTP %{http_code}\n' http://localhost:3200/chromaui && grep -o '<title>[^<]*</title>' /tmp/l10-chromaui.html"   # extra: README:202
    step 58-curl-chat "curl -s --max-time 300 -o /tmp/l10-chat.html -w 'HTTP %{http_code}\n' http://localhost:3200/chat && grep -o '<title>[^<]*</title>' /tmp/l10-chat.html"   # extra: README:215
    rm -f /tmp/l10-home.html /tmp/l10-chunkviz.html /tmp/l10-chromaui.html /tmp/l10-chat.html
    curl -s -o /dev/null --max-time 60 http://localhost:3200/capture-done
  ) &
  CURLS=$!
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1800 istep 51-npm-run-dev "sh docker-shell.sh" \
    'bash-[0-9.]+# $' 'npm run dev' \
    'capture-done|/_not-found' "$CTRLC" \
    'bash-[0-9.]+# $' 'exit'
  wait $CURLS
  ;;
cors)
  # --- digest §3.6 extras: ChromaDB's CORS guest list (docker-compose.yml:26), probed with curl.
  # The browser enforces CORS; curl just shows what the server answers each page origin.
  step 60-cors-preflight-3200 "curl -s -D - -o /dev/null -X OPTIONS -H 'Origin: http://localhost:3200' -H 'Access-Control-Request-Method: POST' http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections"
  step 61-cors-preflight-3300 "curl -s -D - -o /dev/null -X OPTIONS -H 'Origin: http://localhost:3300' -H 'Access-Control-Request-Method: POST' http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections"
  step 62-cors-get-3200 "curl -s -D - -o /dev/null -H 'Origin: http://localhost:3200' http://localhost:8000/api/v2/version"
  step 63-curl-collections "curl -s http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections"   # honest: empty, nothing could be loaded without credentials
  ;;
down)
  cd cheese-app-v0/llm-rag
  # --- README:106: "To stop it, run `docker compose down` inside llm-rag"
  step 70-compose-down "docker compose down"
  step 71-docker-ps-after "docker ps"                     # extra: nothing left running
  step 72-volumes-persist "ls -la docker-volumes/chromadb"   # extra: digest §3.7 -- the bind-mounted data survives the containers
  # extra: bring ChromaDB back (the same README command) and show it serves again from the same folder
  PTY_COLS=110 PTY_ROWS=50 istep 73-chroma-back "sh docker-shell.sh" \
    ':/app\$ $' 'exit'
  step 74-curl-version-again "curl -s http://localhost:8000/api/v2/version"   # extra
  step 75-compose-down-again "docker compose down"        # extra: leave the machine clean
  step 76-network-rm "docker network rm cheese-app-network"   # extra: digest §2 shutdown checklist
  ;;
*)
  echo "run_steps.sh: unknown segment $SEG" >&2; exit 2 ;;
esac
