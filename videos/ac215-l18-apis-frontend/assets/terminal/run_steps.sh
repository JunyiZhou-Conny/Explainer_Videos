#!/bin/bash
# Runs inside the fresh "laptop" capture container (see capture.sh) as user `student`, recording each
# tutorial command's output to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# The laptop's home folder plays the README's parent folder (AC215/): cheese-app-v1/, cheese-app-v2/,
# secrets/, persistent-folder/ side by side.
# Segments (file prefix = part of the video):
#   bases  (capture-only) re-tag the base images alone; reset-v2: a fresh cheese-app-v2 clone
#   pre    (p..) clone both repos, the commits, the sibling folders, the placeholder key, + the
#                capture-only base images
#   v1     (a..) cheese-app-v1 @ ce03a10, the whole README: API container + uvicorn + square_root +
#                /docs, frontend-simple container + http-server + the index.html edit, Docker Cleanup
#   head   (b..) cheese-app-v2 @ main 447b5c3 (= e98fa55's code + src/docker-compose.yml), "Tutorial:
#                Environment Setup / Vector DB for RAG Setup / Backend APIs" (project id, download/load,
#                --chat, api_server, /healthz, /readyz, demo route, /api/docs, pytest)
#          (d..) and, with the same API still running, "Tutorial: React Frontend Setup" (npm run dev on
#                :3000, npm run check) + extras: e98fa55's "Production images" (nginx :8080), which
#                447b5c3 removed from the README (the Dockerfile and nginx template are still there)
#          (f..) "Tutorial: Setup & Run Cheese App" (docker compose up --build in src/), new in 447b5c3
#          (e..) "Docker Cleanup" + extras
#   old    (c..) cheese-app-v2 @ branch 2025 = 14f2a14, "Tutorial (24): Simple Frontend App" with
#                the 2025 vector DB and API it calls (HEAD removed the section, see ASSETS.md)
# README.md:N = cheese-app-v1 @ ce03a10 (v1), cheese-app-v2 @ 447b5c3 (head) or @ 14f2a14 (old).
# Steps whose name contains "-x-" are extras (not README steps): checks the video uses.
# capture-only work (proxy CA, placeholder key, waiting for a port) is never shown as a README step.
OUT=$1; SEG=$2; export OUT
HERE="$(cd "$(dirname "$0")" && pwd)"
umask 022   # a login shell's default (docker exec would otherwise run with umask 0000)
cd ~

# Series rule: the instructor's name never appears in a capture. It is read from the tutorial's own
# page at run time (so it is written nowhere in this repository) and replaced by ‹instructor›.
NAME_RE=
if [ -f ~/cheese-app-v1/src/frontend-simple/index.html ]; then
  FULL=$(grep -o 'My name is [A-Z][a-z]* [A-Z][a-z]*' ~/cheese-app-v1/src/frontend-simple/index.html | head -1 | cut -d' ' -f4-)
  [ -n "$FULL" ] && NAME_RE="${FULL}|${FULL%% *}|${FULL##* }"
fi
mask() { if [ -n "$NAME_RE" ]; then sed -E "s/${NAME_RE}/‹instructor›/Ig"; else cat; fi; }

step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1 | sed 's/\x1b\[[0-9;]*m//g'; echo "[exit ${PIPESTATUS[0]}]"; } | mask > "$OUT/$name.txt"
}
istep() {  # istep <name> <command> [<prompt regex | file:PATH> <typed line>]...   (in a terminal, typed)
  local name=$1 cmd=$2; shift 2
  local args=()
  while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
  { echo "\$ $cmd"
    python3 "$HERE/ptyrun.py" --cols "${PTY_COLS:-100}" --rows "${PTY_ROWS:-40}" --timeout "${PTY_TIMEOUT:-900}" \
      "${args[@]}" -- bash -c "$cmd"
    echo "[exit $?]"; } | mask > "$OUT/$name.txt"
}
hub_retry() {  # hub_retry step|istep <name> <args...>   (recording sandbox only: CAPTURE_HUB_WAIT set)
  # Docker Hub limits anonymous pulls per IP and the sandbox's egress IPs are shared: run a step that
  # hit "toomanyrequests" again; capture-only/hub-retries.txt counts the failed attempts.
  local fn=$1 name=$2 i
  for i in $(seq 40); do
    "$fn" "$name" "${@:3}"
    grep -q "toomanyrequests\|429 Too Many Requests" "$OUT/$name.txt" || return 0
    [ -n "$CAPTURE_HUB_WAIT" ] || return 0
    mkdir -p "$OUT/capture-only"
    echo "$name: attempt $i hit Docker Hub's rate limit, retrying in 30 s" >> "$OUT/capture-only/hub-retries.txt"
    sleep 30
  done
}
wait_http() {  # wait_http <url> <seconds>: quiet readiness probe (capture-only, not shown)
  local i; for i in $(seq "$2"); do curl -s -o /dev/null --max-time 5 "$1" && return 0; sleep 1; done; return 1
}
wait_code() {  # wait_code <url> <status> <seconds>: quiet probe until the URL answers that status
  local i; for i in $(seq "$3"); do [ "$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "$1")" = "$2" ] && return 0; sleep 1; done; return 1
}
capture_only_bases() {  # recording sandbox only (CAPTURE_CA set); see ASSETS.md, "capture-only"
  # The tutorial's builds and containers download over TLS, and the sandbox's TLS is re-signed by its
  # proxy, which also refuses plain http. Each base image a tutorial Dockerfile starts FROM and that
  # downloads something is rebuilt with that proxy's CA (+ https Debian sources and the CA env vars)
  # and re-tagged under the same name, so every tutorial Dockerfile builds unchanged.
  [ -n "$CAPTURE_CA" ] || return 0
  local d v; d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"
  mkdir -p "$OUT/capture-only"
  for v in 3.12-slim-bookworm 3.13-slim-bookworm; do
    cat > "$d/Dockerfile" <<EOF
# capture-only, NOT part of the tutorial: python:$v + the recording proxy's CA, https Debian
# sources and the CA env vars, re-tagged under the same name so the tutorial Dockerfile builds unchanged.
FROM python:$v
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \\
 && sed -i -e 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \\
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \\
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \\
    UV_SYSTEM_CERTS=1
EOF
    cp "$d/Dockerfile" "$OUT/capture-only/python$v-base.Dockerfile"
    hub_retry step capture-only/python$v-base-build "docker build -t python:$v $d"
  done
  for v in 20-alpine 24.22.1-bookworm-slim; do
    cat > "$d/Dockerfile" <<EOF
# capture-only, NOT part of the tutorial: node:$v + the recording proxy's CA for npm (and apk),
# re-tagged under the same name so the tutorial Dockerfile builds unchanged.
FROM node:$v
COPY capture-ca.crt /usr/local/share/capture-ca.crt
RUN if [ -f /etc/ssl/certs/ca-certificates.crt ]; then cat /usr/local/share/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt; fi; chmod 644 /usr/local/share/capture-ca.crt
ENV NODE_EXTRA_CA_CERTS=/usr/local/share/capture-ca.crt
EOF
    cp "$d/Dockerfile" "$OUT/capture-only/node$v-base.Dockerfile"
    hub_retry step capture-only/node$v-base-build "docker build -t node:$v $d"
  done
  rm -rf "$d"
}
CTRLC=$'\x03'
PY_PROMPT='app@[0-9a-f]+:/app\$ $'          # the Python containers' prompt (user app)
NODE_PROMPT='node@[0-9a-f]+:/app\$ $'       # the React dev container's prompt (user node)
ROOT_PROMPT=':/app# $'                      # node:20-alpine's bash as root, prompt <id>:/app# (frontend-simple)
SID=00000000-0000-4000-8000-000000000001    # a session id for the chat routes (any v4 UUID)
SID2=00000000-0000-4000-8000-000000000002
JSON="-H 'Content-Type: application/json'"
CODE="-w '\n[HTTP %{http_code}]\n'"

case $SEG in
# ------------------------------------------------------------------------------------------------
bases)
  capture_only_bases   # (re-)tag the capture-only base images alone, e.g. after `capture.sh prune`
  ;;
reset-v2)
  # capture-only: a fresh clone of cheese-app-v2 and an empty persistent-folder, as before Part B
  # (capture.sh removes the old clone as root first: Chroma's data folder is root-owned)
  git clone -q https://github.com/dlops-io/cheese-app-v2.git
  ;;
pre)
  step p00-x-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; docker compose version; git --version; docker images"
  # cheese-app-v1 README "Clone the github repository" (README.md:16-17); v2 README.md:27-28
  step p01-clone-v1 "git clone https://github.com/dlops-io/cheese-app-v1.git"
  step p02-clone-v2 "git clone https://github.com/dlops-io/cheese-app-v2.git"
  step p03-x-git-log "git -C cheese-app-v1 log -1 --format='%H %ci %s'; git -C cheese-app-v2 log -1 --format='%H %ci %s'; git -C cheese-app-v2 branch -r"
  step p04-x-ls-remote "git ls-remote https://github.com/dlops-io/cheese-app-v2.git; git ls-remote https://github.com/dlops-io/cheese-app-v1.git"
  # v1 README.md:20-36 "Create a local secrets folder"; v2 README.md:30-50 "Create the local folders"
  # (the READMEs show the tree, not a command)
  step p05-mkdir "mkdir -p secrets persistent-folder"
  # capture-only: there is NO real key here. A throwaway RSA key, generated now for no account and
  # never written to the repository, makes a well-formed key file, so Google's client libraries load
  # it and the first real call fails where a student's would succeed (ASSETS.md, "What cannot run here").
  mkdir -p "$OUT/capture-only"
  openssl genrsa -out /tmp/throwaway.pem 2048 2>/dev/null
  python3 - <<'EOF'
import json
key = open("/tmp/throwaway.pem").read()
info = {"type": "service_account", "project_id": "your-gcp-project",
        "private_key_id": "0000000000000000000000000000000000000000", "private_key": key,
        "client_email": "placeholder-not-a-real-account@your-gcp-project.iam.gserviceaccount.com",
        "client_id": "000000000000000000000", "token_uri": "https://oauth2.googleapis.com/token"}
import os
json.dump(info, open(os.path.expanduser("~/secrets/ml-workflow.json"), "w"), indent=2)
info["private_key"] = "<a throwaway RSA key generated at capture time for no account; not committed>"
json.dump(info, open(os.environ["OUT"] + "/capture-only/placeholder-key.json", "w"), indent=2)
EOF
  rm -f /tmp/throwaway.pem
  step p06-x-tree "find . -maxdepth 3 -not -path '*/.git*' -not -path './.*' | sort | head -40; ls -la secrets persistent-folder"
  capture_only_bases
  ;;
# ------------------------------------------------------------------------------------------------
v1)
  # --- README "Go into the api-service folder" (README.md:40-41): the README's path lacks src/
  step a01-cd-readme-path "cd cheese-app-v1/api-service"
  step a02-x-cd-api-src "cd cheese-app-v1/src/api-service && ls"   # the path that exists
  cd cheese-app-v1/src/api-service
  CUE=/tmp/l18-cue-v1api; rm -f $CUE
  ( wait_http http://localhost:9000/ 1500; sleep 2
    step a04-curl-root "curl -s -i http://localhost:9000/"                       # README:48 in the browser
    # README "Edit Code in VS Code" (README.md:50-58): add the route at the end of api/service.py
    step a05-edit-service "cat >> api/service.py <<'EOF'

@app.get(\"/square_root/\")
async def square_root(x: float = 1, y: float = 2):
    z = x**2 + y**2
    return z**0.5
EOF
git -C ~/cheese-app-v1 diff"
    sleep 6; wait_code http://localhost:9000/square_root/ 200 60
    step a06-curl-square-root "curl -s http://localhost:9000/square_root/; echo"          # README:59
    step a07-curl-square-root-params "curl -s 'http://localhost:9000/square_root/?x=2&y=10'; echo"   # README:61
    step a08-x-square-root-bad "curl -s $CODE 'http://localhost:9000/square_root/?x=abc'"
    step a09-x-square-root-no-slash "curl -s -i http://localhost:9000/square_root | head -6"
    step a10-docs "curl -s http://localhost:9000/docs | grep -E '<title>|openapi.json|swagger'"   # README:64-67
    step a11-x-openapi "curl -s http://localhost:9000/openapi.json | python3 -m json.tool"
    step a12-x-docker-ps "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'"
    # --- README "Frontend App (Simple) Container" (README.md:71-97), in a second terminal
    cd ~/cheese-app-v1/src/frontend-simple
    CUE2=/tmp/l18-cue-v1fe; rm -f $CUE2
    ( wait_http http://localhost:8080/ 900; sleep 2
      step a21-curl-8080 "curl -s -i http://localhost:8080/ | grep -E 'HTTP/|cache-control|content-type|<title>|hero-title|main.js'"   # README:83
      step a22-x-main-js "curl -s http://localhost:8080/main.js | grep -n -A3 'Sample Podcast Data'"
      # README "Edit Code in VS Code" (README.md:85-97): add a <p> to index.html. Inside the hero
      # section rather than replacing the whole <body> (the README's snippet predates this page and
      # would drop the main.js script tag; ASSETS.md)
      step a23-edit-index "python3 - <<'EOF'
p = 'index.html'
s = open(p).read()
s = s.replace('''<p class=\"hero-subtitle\">Discover the world of cheese through AI</p>''', '''<p class=\"hero-subtitle\">Discover the world of cheese through AI</p>
            <p>
                This is a placeholder for the awesome cheese identification app
            </p>''', 1)
open(p, 'w').write(s)
EOF
git -C ~/cheese-app-v1 diff -- src/frontend-simple/index.html"
      step a24-curl-8080-after "curl -s http://localhost:8080/ | grep -n -B1 -A1 'placeholder for the awesome'"   # README:96
      step a25-x-cache-header "curl -s -I http://localhost:8080/main.js | grep -i -E 'HTTP/|cache-control'"
      step a26-x-docker-ps "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'"
      touch $CUE2 ) &
    BG2=$!
    ( cd ~; step a19-cd-frontend-readme-path "cd cheese-app-v1/frontend-simple"     # README:75
      step a20-x-cd-frontend-src "cd cheese-app-v1/src/frontend-simple && ls" )
    hub_retry istep a20b-docker-shell-frontend "sh docker-shell.sh" "$ROOT_PROMPT" "http-server" "file:$CUE2" "$CTRLC" "$ROOT_PROMPT" "exit"
    wait $BG2
    touch $CUE ) &
  BG=$!
  # README "Build & Run Container" (README.md:43-44) + "Start API Service" (README.md:46-48)
  PTY_TIMEOUT=3000 hub_retry istep a03-docker-shell-api "sh docker-shell.sh" \
    "$PY_PROMPT" 'uvicorn api.service:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir api/ "$@"' \
    "file:$CUE" "$CTRLC" "$PY_PROMPT" "exit"
  wait $BG
  cd ~
  # --- README "Docker Cleanup" (README.md:99-106)
  step a30-docker-container-ls "docker container ls"
  istep a31-docker-system-prune "docker system prune" '\[y/N\] $' "y"
  step a32-docker-image-ls "docker image ls"
  ;;
# ------------------------------------------------------------------------------------------------
head)
  cd ~/cheese-app-v2
  step b01-x-git-log "git log -1 --format='%H %ci %s'; git status -sb | head -1"
  step b02-x-ls "ls; ls src"
  # README "Set your Google Cloud project" (README.md:47-50): a placeholder id, never a real one
  step b03-set-project "sed -i 's/\"ac215-project\"/\"your-gcp-project\"/' src/api-service/docker-shell.sh src/vector-db/docker-shell.sh
git diff"
  step b04-x-ls-secrets "ls ../secrets ../persistent-folder"
  # --- README "Tutorial: Vector DB for RAG Setup" (README.md:52-79)
  step b05-cd-vector-db "cd src/vector-db"
  cd src/vector-db
  PTY_TIMEOUT=2400 hub_retry istep b06-docker-shell-vector-db "./docker-shell.sh" \
    "$PY_PROMPT" "python cli.py --download --load --chunk_type recursive-split" \
    "$PY_PROMPT" "python cli.py --chat --chunk_type recursive-split" \
    "$PY_PROMPT" "exit"
  step b07-x-docker-ps "docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'"
  step b08-x-chroma-heartbeat "curl -s http://localhost:8000/api/v2/heartbeat; echo; curl -s http://localhost:8000/api/v2/version; echo"
  step b09-x-host-folders "ls outputs | head -30; ls outputs | wc -l; du -sh outputs docker-volumes/chromadb"
  step b10-x-network "docker network inspect cheese-app-network --format '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{println}}{{end}}'"
  cd ~/cheese-app-v2
  # --- README "Tutorial: Backend APIs" (README.md:81-145), in a new terminal
  step b20-cd-api "cd src/api-service"
  cd src/api-service
  CUE=/tmp/l18-cue-api; rm -f $CUE
  ( wait_http http://localhost:9000/healthz 3000
    step b22-healthz "curl -s -i http://localhost:9000/healthz"                       # README:101
    step b23-readyz-loading "curl -s -i http://localhost:9000/readyz"                 # README:102-103
    wait_code http://localhost:9000/readyz 200 900
    step b24-readyz-ready "curl -s -i http://localhost:9000/readyz"
    step b25-x-old-urls "curl -s $CODE http://localhost:9000/; curl -s $CODE http://localhost:9000/docs"
    step b26-x-persistent "ls -la ~/persistent-folder ~/persistent-folder/experiments; ls ~/persistent-folder/experiments/*/"
    # README "Create a demo route" (README.md:105-112): after get_status in api/service.py
    step b27-edit-service "python3 - <<'EOF'
p = 'api/service.py'
s = open(p).read()
s = s.replace('''    return {\"version\": \"2.0.0\"}
''', '''    return {\"version\": \"2.0.0\"}


@app.get(\"/api/square_root\")
def square_root(x: float = 1, y: float = 2):
    z = x**2 + y**2
    return z**0.5
''', 1)
open(p, 'w').write(s)
EOF
git diff api/service.py"
    sleep 6; wait_code http://localhost:9000/api/square_root 200 120
    step b28-curl-square-root "curl -s http://localhost:9000/api/square_root; echo"             # README:114
    step b29-curl-square-root-3-4 "curl -s 'http://localhost:9000/api/square_root?x=3&y=4'; echo"   # README:115
    step b30-x-readyz-after-reload "curl -s -i http://localhost:9000/readyz | sed -n '1p;\$p'"
    wait_code http://localhost:9000/readyz 200 600
    step b31-api-docs "curl -s $CODE http://localhost:9000/api/docs | grep -E '<title>|openapi.json|HTTP'"   # README:119
    step b32-x-openapi-paths "curl -s http://localhost:9000/api/openapi.json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d[\"info\"]); [print(m.upper().ljust(6), p) for p,v in d[\"paths\"].items() for m in v]'"
    # README:120 "Try GET /api/newsletters": the curl command /api/docs shows for "Try it out"
    step b33-get-newsletters "curl -X 'GET' 'http://localhost:9000/api/newsletters?limit=2' -H 'accept: application/json' | python3 -m json.tool | cut -c1-160"
    step b34-x-newsletter-404 "curl -s $CODE http://localhost:9000/api/newsletters/does-not-exist"
    step b35-x-podcasts "curl -s http://localhost:9000/api/podcasts | python3 -m json.tool; curl -s -o /dev/null -w 'audio: HTTP %{http_code} %{content_type} %{size_download} bytes\n' http://localhost:9000/api/podcasts/audio/9f2b7e84-5623-4029-bcfd-f99f2d7611e8-EN.mp3"
    step b36-x-chat-no-session "curl -s $CODE -X POST http://localhost:9000/api/llm/chats $JSON -d '{\"content\": \"How is cheese made?\"}'"
    step b37-x-chat-empty "curl -s $CODE -X POST http://localhost:9000/api/llm/chats $JSON -H 'X-Session-ID: $SID' -d '{}'"
    step b38-x-chat-ask "curl -s $CODE -X POST http://localhost:9000/api/llm/chats $JSON -H 'X-Session-ID: $SID' -d '{\"content\": \"How is cheese made?\"}'"
    python3 -c "import base64, json; print(json.dumps({'image': base64.b64encode(open('news-letters/assets/blue-cheese.jpg','rb').read()).decode()}))" > /tmp/identify.json   # capture-only: the JSON body
    step b39-x-chat-identify "curl -s $CODE -X POST http://localhost:9000/api/llm-cnn/chats $JSON -H 'X-Session-ID: $SID' -d @/tmp/identify.json | cut -c1-600"
    step b40-x-chat-books "curl -s $CODE -X POST http://localhost:9000/api/llm-rag/chats $JSON -H 'X-Session-ID: $SID' -d '{\"content\": \"How is Tolminc cheese made?\"}'"
    step b41-x-chats-list "curl -s http://localhost:9000/api/llm-cnn/chats -H 'X-Session-ID: $SID' | python3 -m json.tool; curl -s http://localhost:9000/api/llm-cnn/chats -H 'X-Session-ID: $SID2'; echo"
    step b42-x-chat-history "find ~/persistent-folder/chat-history -type f | sed 's|$HOME/||'"
    step b43-x-cors-none "curl -s -i -H 'Origin: http://localhost:8080' 'http://localhost:9000/api/newsletters?limit=1' | grep -i -E 'HTTP/|access-control|content-type'; curl -s -i -X OPTIONS -H 'Origin: http://localhost:8080' -H 'Access-Control-Request-Method: POST' http://localhost:9000/api/llm/chats | grep -i -E 'HTTP/|access-control|allow'"
    # README:140-143 "Run the tests inside the container": a second terminal; docker-shell.sh finds
    # the running container and shells into it
    istep b44-pytest "./docker-shell.sh" "$PY_PROMPT" "pytest" "$PY_PROMPT" "exit"
    step b45-x-docker-ps "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'"
    step b46-x-docker-images "docker images"
    # --- README "Tutorial: React Frontend Setup" (README.md:147-190), in a new terminal
    cd ~/cheese-app-v2
    step d01-cd-frontend "cd src/frontend-react"
    cd src/frontend-react
    CUE2=/tmp/l18-cue-react; rm -f $CUE2
    ( wait_http http://localhost:3000/ 1500; sleep 3
      step d03-curl-3000 "curl -s -i http://localhost:3000/ | grep -v '^\s*\$'"                       # README:164
      step d04-x-curl-3000-api "curl -s -i 'http://localhost:3000/api/newsletters?limit=2' | sed -n '1,8p'"
      step d05-x-curl-3000-main "curl -s http://localhost:3000/src/main.jsx | head -20"
      step d06-x-chat-via-3000 "curl -s $CODE -X POST http://localhost:3000/api/llm/chats $JSON -H 'X-Session-ID: $SID2' -d '{\"content\": \"How is cheese made?\"}'"
      step d07-x-identify-via-3000 "curl -s $CODE -X POST http://localhost:3000/api/llm-cnn/chats $JSON -H 'X-Session-ID: $SID2' -d @/tmp/identify.json | cut -c1-400"
      step d08-x-routes "for u in / /podcasts /newsletters /chat?model=llm /nope; do printf '%-20s ' \$u; curl -s -o /dev/null -w '%{http_code} %{content_type}\n' http://localhost:3000\$u; done"
      # open question 7 of the digest: what the browser gets when Vite cannot reach the API
      step d09-x-api-unreachable "docker network disconnect cheese-app-network cheese-app-api-service; curl -s $CODE 'http://localhost:3000/api/newsletters?limit=2'; docker network connect cheese-app-network cheese-app-api-service"
      wait_code 'http://localhost:3000/api/newsletters?limit=1' 200 60
      step d10-x-docker-ps "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'"
      step d11-x-volume "docker volume ls; docker run --rm -v cheese-app-frontend-react-node_modules:/m --entrypoint sh cheese-app-frontend-react -c 'ls /m | wc -l; du -sh /m'"
      # README:187-190 "npm run check": a second terminal shells into the running container
      PTY_TIMEOUT=900 istep d12-npm-run-check "./docker-shell.sh" "$NODE_PROMPT" "npm run check" "$NODE_PROMPT" "exit"
      touch $CUE2 ) &
    BG2=$!
    PTY_TIMEOUT=3000 hub_retry istep d02-docker-shell-react "./docker-shell.sh" "$NODE_PROMPT" "npm run dev" "file:$CUE2" "$CTRLC" "$NODE_PROMPT" "exit"
    wait $BG2
    # --- extras: README @ e98fa55 "Production images" (its README.md:197-215), commands as written there
    hub_retry step d20-x-docker-build-prod "docker build -t cheese-app-frontend-react:prod ."
    CUE3=/tmp/l18-cue-prod; rm -f $CUE3
    ( wait_http http://localhost:8080/ 300; sleep 2
      step d22-curl-8080 "curl -s -i http://localhost:8080/ | grep -E 'HTTP/|Server:|Content-Type|<title>|assets/'"   # e98fa55 README:210
      step d23-x-curl-8080-api "curl -s -i 'http://localhost:8080/api/newsletters?limit=1' | grep -E 'HTTP/|Server:|content-type|\"title\"' | cut -c1-120"
      step d24-x-curl-8080-healthz "curl -s -i http://localhost:8080/healthz | grep -v '^\s*\$'"
      step d25-x-curl-8080-deeplink "for u in /newsletters /chat?model=llm-rag /assets/; do printf '%-22s ' \$u; curl -s -o /dev/null -w '%{http_code} %{content_type}\n' http://localhost:8080\$u; done"
      step d26-x-docker-ps "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'"
      touch $CUE3 ) &
    BG3=$!
    istep d21-x-docker-run-prod "docker run --rm --network cheese-app-network -p 8080:80 cheese-app-frontend-react:prod" "file:$CUE3" "$CTRLC"
    wait $BG3
    step d27-x-docker-images-grep "docker images | grep cheese-app-frontend-react"         # e98fa55 README:213-215
    step d28-x-image-history "docker history --format '{{.Size}}\t{{.CreatedBy}}' cheese-app-frontend-react:prod | cut -c1-110 | head -12"
    touch $CUE ) &
  BG=$!
  # README "Start the API" steps 1-2 (README.md:84-98)
  PTY_TIMEOUT=6000 hub_retry istep b21-docker-shell-api "./docker-shell.sh" "$PY_PROMPT" "api_server" "file:$CUE" "$CTRLC" "$PY_PROMPT" "exit"
  wait $BG
  # extra (digest gotcha 11): the production frontend with no API on the network
  step e01-x-prod-without-api "timeout 30 docker run --rm --network cheese-app-network -p 8080:80 cheese-app-frontend-react:prod"
  # --- README "Tutorial: Setup & Run Cheese App" (447b5c3 README.md:192-222)
  cd ~/cheese-app-v2
  # step 1: GCP_PROJECT in src/docker-compose.yml, "It appears twice" (a placeholder, never a real id)
  step f01-set-project-compose "sed -i 's/ac215-project/your-gcp-project/' src/docker-compose.yml
git diff src/docker-compose.yml"
  # step 2: the API and frontend shells are already closed above; stop Chroma in src/vector-db
  cd src/vector-db
  step f02-docker-compose-down-vector-db "docker compose down"
  cd ~/cheese-app-v2
  # step 3
  step f03-cd-src "cd src"
  cd src
  compose_up() {  # compose_up <name>: README step 3-5 with the checks of step 4 from a second shell
    local CUE=/tmp/l18-cue-compose-$1; rm -f $CUE
    ( wait_http http://localhost:3000/ 2400 && wait_http http://localhost:9000/healthz 600; sleep 3
      step $1-curl-3000 "curl -s -i http://localhost:3000/ | grep -E 'HTTP/|<title>'"                    # step 4
      step $1-curl-api-docs "curl -s $CODE http://localhost:9000/api/docs | grep -E '<title>|HTTP'"       # step 4 (as meant)
      step $1-x-readme-url "curl -sS $CODE --max-time 5 http://localhost:900/api/docs"                   # step 4 as printed
      step $1-x-compose-ps "docker compose ps -a --format 'table {{.Name}}\t{{.Service}}\t{{.Status}}\t{{.Ports}}'"
      step $1-x-loader-logs "docker compose logs vector-db-loader"
      wait_code http://localhost:9000/readyz 200 600
      step $1-x-readyz "curl -s -i http://localhost:9000/readyz | sed -n '1p;\$p'"
      step $1-x-api-via-3000 "curl -s 'http://localhost:3000/api/newsletters?limit=1' | cut -c1-120"
      touch $CUE ) &
    local BG=$!
    PTY_TIMEOUT=3600 PTY_ROWS=50 PTY_COLS=120 hub_retry istep $1-docker-compose-up "docker compose up --build" "file:$CUE" "$CTRLC"
    kill $BG 2>/dev/null; wait $BG 2>/dev/null
  }
  compose_up f04
  if grep -q "incorrect label" "$OUT/f04-docker-compose-up.txt"; then
    # the network the docker-shell.sh scripts created is not Compose's: remove it, then step 3 again
    step f05-x-network-rm "docker network rm cheese-app-network"
    compose_up f06
  fi
  # step 5
  step f10-docker-compose-down "docker compose down"
  step f11-x-left-over "docker ps -a; docker volume ls; docker network ls"
  # --- README "Docker Cleanup" (447b5c3 README.md:235-246)
  cd ~/cheese-app-v2/src/vector-db
  step e02-docker-compose-down "docker compose down"
  istep e03-docker-system-prune "docker system prune" '\[y/N\] $' "y"
  step e04-x-left-over "docker ps -a; docker images; docker volume ls; docker network ls"
  ;;
# ------------------------------------------------------------------------------------------------
old)
  # Tutorial (24) exists only on branch 2025 (= 14f2a14); HEAD removed it (ASSETS.md "Which commit")
  cd ~/cheese-app-v2
  step c01-git-switch "git switch 2025"
  if [ "$(git branch --show-current)" != 2025 ]; then
    # the switch refused because of this session's own edits (project id, demo route): set them aside
    step c01b-x-stash-switch "git stash && git switch 2025"
  fi
  step c02-x-git-log "git log -1 --format='%H %ci %s'; ls src"
  # 2025 README "Create a local secrets folder" (README.md:23-38) names only ml-workflow.json; the
  # 2025 vector-db script reads llm-service-account.json (digest erratum 14): the same placeholder
  step c03-x-second-key-name "cp ../secrets/ml-workflow.json ../secrets/llm-service-account.json; ls ../secrets"
  step c04-x-set-project "sed -i 's/\"ac215-project\"/\"your-gcp-project\"/' src/api-service/docker-shell.sh src/vector-db/docker-shell.sh; git diff --stat"
  cd ~
  # --- 2025 README "Tutorial (23): Vector DB for RAG Setup" (README.md:40-65)
  step c05-cd-vector-db "cd cheese-app-v2/src/vector-db"
  cd cheese-app-v2/src/vector-db
  PTY_TIMEOUT=2400 hub_retry istep c06-docker-shell-vector-db "sh docker-shell.sh" \
    "$PY_PROMPT" "python cli.py --download --load --chunk_type recursive-split" "$PY_PROMPT" "exit"
  if grep -q "docker-compose: command not found\|docker-compose: not found" "$OUT/c06-docker-shell-vector-db.txt"; then
    # capture-only: Docker Desktop ships the hyphenated `docker-compose`; this Linux engine has only the
    # compose plugin. A one-line shim on PATH stands in for Docker Desktop's (ASSETS.md); the script runs unchanged.
    mkdir -p ~/bin "$OUT/capture-only"
    printf '#!/bin/sh\nexec docker compose "$@"\n' > ~/bin/docker-compose; chmod 755 ~/bin/docker-compose
    cp ~/bin/docker-compose "$OUT/capture-only/docker-compose-shim.sh"
    export PATH=~/bin:$PATH
    PTY_TIMEOUT=2400 hub_retry istep c06b-docker-shell-vector-db "sh docker-shell.sh" \
      "$PY_PROMPT" "python cli.py --download --load --chunk_type recursive-split" "$PY_PROMPT" "exit"
  fi
  step c07-x-docker-ps "docker ps -a --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'; docker image inspect chromadb/chroma:latest --format '{{.Id}} {{.Created}}' 2>&1 | cut -c1-90"
  cd ~
  # --- 2025 README "Tutorial (23): Backend APIs" (README.md:67-94)
  step c10-cd-api "cd cheese-app-v2/src/api-service"
  cd cheese-app-v2/src/api-service
  CUE=/tmp/l18-cue-old-api; rm -f $CUE
  ( wait_http http://localhost:9000/ 3000; sleep 2
    step c12-x-curl-root "curl -s -i http://localhost:9000/"                         # README:94
    step c13-x-square-root-present "grep -n -A3 'square_root' api/service.py; curl -s 'http://localhost:9000/square_root/?x=2&y=10'; echo"
    step c14-x-routers "sed -n '35,42p' api/service.py; curl -s http://localhost:9000/openapi.json | python3 -c 'import json,sys; [print(m.upper().ljust(6), p) for p,v in json.load(sys.stdin)[\"paths\"].items() for m in v]'"
    # --- 2025 README "Tutorial (24): Simple Frontend App" (README.md:147-183), a third terminal
    cd ~
    step c20-cd-frontend-simple "cd cheese-app-v2/src/frontend-simple"
    cd cheese-app-v2/src/frontend-simple
    CUE2=/tmp/l18-cue-old-fe; rm -f $CUE2
    ( wait_http http://localhost:8080/ 900; sleep 2
      step c22-curl-index "curl -s -i http://localhost:8080/index.html | grep -E 'HTTP/|<title>|href=\"(newsletters|chat)'"   # README:170
      step c23-curl-newsletters-page "curl -s -i http://localhost:8080/newsletters.html | grep -E 'HTTP/|<title>|script'"   # README:174
      step c24-x-newsletters-js "grep -n 'localhost:9000\|axios' newsletters-main.js chat-main.js | head"
      # what the newsletters page's JavaScript requests, from the page's origin (the browser adds Origin)
      step c25-x-browser-newsletters "curl -s -i -L -H 'Origin: http://localhost:8080' 'http://localhost:9000/newsletters?limit=100' | grep -i -E 'HTTP/|location|access-control|content-type|\"title\"' | cut -c1-120"
      # chat.html: the browser's preflight, then the POST (README:179-181)
      step c26-curl-chat-page "curl -s -i http://localhost:8080/chat.html | grep -E 'HTTP/|<title>|script'"
      step c27-x-browser-preflight "curl -s -i -X OPTIONS -H 'Origin: http://localhost:8080' -H 'Access-Control-Request-Method: POST' -H 'Access-Control-Request-Headers: content-type,x-session-id' http://localhost:9000/llm/chats | grep -i -E 'HTTP/|access-control'"
      step c28-x-browser-chat "curl -s -i -L -X POST -H 'Origin: http://localhost:8080' $JSON -H 'X-Session-ID: $SID' -d '{\"content\": \"How is cheese made?\"}' http://localhost:9000/llm/chats/ | grep -v '^\s*\$' | cut -c1-300"
      step c29-x-docker-ps "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'"
      touch $CUE2 ) &
    BG2=$!
    hub_retry istep c21-docker-shell-frontend "sh docker-shell.sh" "$ROOT_PROMPT" "http-server" "file:$CUE2" "$CTRLC" "$ROOT_PROMPT" "exit"
    wait $BG2
    touch $CUE ) &
  BG=$!
  PTY_TIMEOUT=6000 hub_retry istep c11-docker-shell-api "sh docker-shell.sh" "$PY_PROMPT" "uvicorn_server" "file:$CUE" "$CTRLC" "$PY_PROMPT" "exit"
  wait $BG
  cd ~/cheese-app-v2/src/vector-db
  step c30-x-stop "docker stop cheese-app-vector-db; docker ps -a"
  cd ~/cheese-app-v2
  step c31-x-git-switch-main "git checkout -- . && git switch main && git log -1 --format='%h %s'"
  ;;
*)
  echo "unknown segment $SEG" >&2; exit 2 ;;
esac
