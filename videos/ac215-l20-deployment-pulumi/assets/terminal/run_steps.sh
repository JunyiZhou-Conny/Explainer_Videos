#!/bin/bash
# Runs inside a capture machine (see capture.sh) as user `student`, recording each tutorial command's
# output to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# README.md:N = dlops-io/cheese-app-v3 @ 3ecef56 (main), mounted read-only at /source/README.md;
# multi-line README commands are read from those exact lines, so they run byte for byte as printed.
# Segments (file prefix = part of the video):
#   vm1    (vm/0x)  "Deployment to GCP (Manual)", on the VM: get-docker.sh, docker --version
#   vm2    (vm/1x-6x) the rest of the manual deployment on the VM: folders, secret, network, vector-db,
#                   loader, api-service, frontend, nginx.conf, nginx; then the URLs and the README's
#                   later "SSH into the server" commands (README.md:371-383), on this VM
#   pre    (laptop/p..) clone, the commits, the sibling secrets/ folder, capture-only base images
#   partA  (laptop/a..) the laptop half of "Deployment to GCP (Manual)": docker login, docker-hub.sh
#   partB  (laptop/b..) "Deployment to GCP (Single VM Instance)": docker-shell.sh, the tool checks,
#                   SSH setup, both Pulumi projects, destroy
# Steps whose name contains "-x-" are extras (not README steps): checks the video uses.
# capture-only work (proxy CA, placeholder keys, waiting for a port) is never shown as a README step.
OUT=$1; SEG=$2; export OUT
HERE="$(cd "$(dirname "$0")" && pwd)"
README=/source/README.md
umask 022
cd ~

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
readme() { sed -n "$1,$2p" "$README"; }   # readme <first> <last>: README lines, verbatim
wait_http() {  # wait_http <url> <seconds>: quiet readiness probe (capture-only, not shown)
  local i; for i in $(seq "$2"); do curl -s -o /dev/null --max-time 5 "$1" && return 0; sleep 1; done; return 1
}
CTRLC=$'\x03'
DOCKER="docker"; case $SEG in vm*) DOCKER="sudo docker";; esac
capture_only_retag() {  # capture_only_retag <image> [base]: recording sandbox only (CAPTURE_CA set)
  # The sandbox's TLS is re-signed by its proxy (and plain http is refused). An image whose program
  # downloads over TLS is rebuilt with that proxy's CA (+ the CA env vars; for a base image also https
  # Debian sources and the proxy itself, so RUN steps can download) and re-tagged under the SAME name,
  # so the README's commands and the tutorial's Dockerfiles run unchanged. See ASSETS.md.
  [ -n "$CAPTURE_CA" ] || return 0
  local img=$1 kind=${2:-app} d user safe
  d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"; chmod 644 "$d/capture-ca.crt"
  user=$($DOCKER image inspect -f '{{.Config.User}}' "$img")
  safe=$(echo "$img" | tr '/:' '__')
  {
    echo "# capture-only, NOT part of the tutorial: $img + the recording proxy's CA, re-tagged as $img"
    echo "FROM $img"
    echo "USER root"
    echo "COPY capture-ca.crt /usr/local/share/capture-ca.crt"
    echo "RUN for f in /etc/ssl/certs/ca-certificates.crt; do [ -f \$f ] && cat /usr/local/share/capture-ca.crt >> \$f; done; \\"
    echo "    for f in /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list; do [ -f \$f ] && sed -i 's|http://deb.debian.org|https://deb.debian.org|g; s|http://security.debian.org|https://security.debian.org|g' \$f; done; true"
    echo "ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \\"
    echo "    PIP_CERT=/etc/ssl/certs/ca-certificates.crt NODE_EXTRA_CA_CERTS=/usr/local/share/capture-ca.crt UV_NATIVE_TLS=1"
    [ "$kind" = base ] && echo "ENV HTTPS_PROXY=$CAPTURE_RELAY https_proxy=$CAPTURE_RELAY NO_PROXY=localhost,127.0.0.1 no_proxy=localhost,127.0.0.1"
    [ -n "$user" ] && echo "USER $user"
  } > "$d/Dockerfile"
  mkdir -p "$OUT/capture-only"
  cp "$d/Dockerfile" "$OUT/capture-only/$safe.Dockerfile"
  step "capture-only/$safe-build" "$DOCKER build -q -t $img $d"
  rm -rf "$d"
}

case $SEG in
# ------------------------------------------------------------------------------------------------
vm1)
  umask 022
  step 00-x-env "date -u '+%Y-%m-%d %H:%M UTC'; hostname; head -4 /etc/os-release; uname -m; which docker; echo which-docker-exit:\$?; pwd"
  # README.md:46-51 "SSH into your newly created instance / Install Docker ... / Check version"
  step 01-get-docker-download "$(readme 48 48 | sed 's/^\* `//; s/`$//')"
  step 02-get-docker-install "$(readme 49 49 | sed 's/^\* `//; s/`$//')"
  step 03-docker-version "$(readme 51 51 | sed 's/^\* `//; s/`$//')"
  ;;
# ------------------------------------------------------------------------------------------------
vm2)
  step 04-x-docker-info "sudo docker info --format 'Server Version: {{.ServerVersion}} / Storage Driver: {{.Driver}} / OS: {{.OperatingSystem}}'; sudo docker images"
  # README.md:61-67 "Create folders and give permissions" (the code block; README.md:54-59 lists the
  # same six commands as bullets)
  n=10
  for l in 62 63 64 65 66 67; do step "$n-folders-$((l-61))" "$(readme $l $l)"; n=$((n+1)); done
  step 16-x-ls "ls -la"
  # README.md:73-75 "Add secrets file", verbatim: the README's placeholder, not a key
  step 17-secret-echo "$(readme 74 74)"
  step 18-x-cat-secret "cat secrets/gcp-service.json"
  # README.md:79-81 "Create Docker network"
  step 19-network-create "$(readme 80 80)"
  # README.md:85-98 "Run vector-db"
  step 20-chroma-pull "$(readme 86 86)"
  step 21-chroma-stop "$(readme 87 87)"
  step 22-chroma-rm "$(readme 88 88)"
  step 23-chroma-run "$(readme 89 97)"
  wait_http http://localhost:8000/api/v2/heartbeat 120
  step 24-x-chroma-check "sudo docker ps; curl -s http://localhost:8000/api/v2/heartbeat; echo; curl -s http://localhost:8000/api/v2/version; echo"
  step 25-x-chroma-logs "sudo docker logs cheese-app-vector-db 2>&1 | head -30"
  # README.md:102-113 "Run vector-db-cli"
  step 26-loader-pull "$(readme 103 103)"
  capture_only_retag dlops/cheese-app-vector-db-cli
  step 27-loader-run "$(readme 104 112)"
  step 28-x-chroma-volume "ls -la docker-volumes/ docker-volumes/chromadb; sudo docker exec cheese-app-vector-db sh -c 'ls -la /data /chroma 2>&1 | head -20'"
  ;;
# ------------------------------------------------------------------------------------------------
vm3)
  # capture-only: the loader image is not needed again, and the recording disk is small
  step capture-only/rmi-loader "sudo docker rmi dlops/cheese-app-vector-db-cli"
  # README.md:117-128 "Run api-service": the image is not on the VM yet, so docker run pulls it
  step 30-api-run "$(readme 118 127)"
  ;;
vm4)
  # capture-only: the first start above crashed on the recording proxy's TLS (the API downloads its
  # CNN model from GitHub at import, llm_cnn_utils.py:126); kept as capture-only/api-first-start.txt.
  # Re-tag the image with the proxy CA under the same name and run the README's command again.
  sleep 20
  step capture-only/api-first-start "sudo docker ps -a --filter name=api-service; sudo docker logs api-service 2>&1 | tail -12"
  capture_only_retag dlops/cheese-app-api-service
  step capture-only/api-rm "sudo docker rm -f api-service"
  step 30b-api-run-again "$(readme 118 127)"
  wait_http http://localhost:9000/ 300
  sleep 3
  step 31-x-api-logs "sudo docker logs api-service 2>&1 | head -60"
  step 32-x-api-ps "sudo docker ps; sudo docker images"
  step 33-x-curl-api-root "curl -s -i http://localhost:9000/"
  step 34-x-curl-api-status "curl -s -i http://localhost:9000/status"
  step 35-x-curl-api-docs "curl -s http://localhost:9000/docs | head -12; curl -s http://localhost:9000/openapi.json | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d[\"info\"]); print(sorted(d[\"paths\"]))'"
  step 37-x-entrypoint "sudo docker exec api-service cat docker-entrypoint.sh"
  ;;
vm4b)  # step 36 re-run alone (its first version had a template error)
  step 36-x-image-service-py "sudo docker exec api-service sh -c 'grep -c \"ROOT_PATH\\\\|mount\\\\|/status\" api/service.py; grep -n \"@app.get\\\\|include_router\" api/service.py; grep -n \"GENERATIVE_MODEL =\" api/utils/*.py'"
  ;;
vm5)
  PY_PROMPT='app@[0-9a-f]+:/app\$ $'
  # README.md:131-145 "If you want to run in interactive mode": same --name while the detached one runs
  istep 38-api-interactive "$(readme 133 144)"
  step 39-x-api-rm "sudo docker rm -f api-service"
  istep 40-x-api-interactive-after-rm "$(readme 133 144)" "$PY_PROMPT" "exit"
  step 41-x-api-run-detached-again "$(readme 118 127)"
  wait_http http://localhost:9000/ 300; sleep 2
  # README.md:147-151 "Run frontend"
  step 42-frontend-run "$(readme 150 150)"
  wait_http http://localhost:3000/ 120; sleep 2
  step 43-x-frontend-check "sudo docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'; curl -s http://localhost:3000/ | grep -o '<title>[^<]*</title>'; sudo docker logs frontend 2>&1 | head -10"
  # README.md:153-214 "Add NGINX config file", the echo exactly as printed
  step 44-nginx-conf-echo "$(readme 156 213)"
  step 45-x-nginx-conf-logformat "wc -l conf/nginx/nginx.conf; sed -n '7,13p' conf/nginx/nginx.conf | cat -A | cut -c1-90"
  # README.md:216-220 "Run NGINX Web Server"
  step 46-nginx-run "$(readme 219 219)"
  sleep 3
  step 47-x-container-ls "sudo docker container ls"
  step 48-x-curl-home "curl -s -i http://localhost/ | head -8; curl -s http://localhost/ | grep -o '<title>[^<]*</title>'"
  step 49-x-curl-api-via-nginx "curl -s -i http://localhost/api-service/; echo; curl -s -i http://localhost/api-service/status; echo"
  step 50-x-curl-api-port "curl -s http://localhost:9000/; echo; curl -s http://localhost/api-service/openapi.json | head -c 160; echo"
  step 51-x-nginx-logs "sudo docker logs nginx 2>&1 | tail -6"
  # README.md:370-382 (written for the Pulumi VM; the container names are the same here)
  step 52-container-ls "$(readme 372 372)"
  CUE=/tmp/l20-cue
  rm -f $CUE; ( sleep 5; touch $CUE ) &
  istep 53-logs-api-service "$(readme 373 373)" "file:$CUE" "$CTRLC"
  rm -f $CUE; ( sleep 5; touch $CUE ) &
  istep 54-logs-frontend "$(readme 374 374)" "file:$CUE" "$CTRLC"
  rm -f $CUE; ( sleep 5; touch $CUE ) &
  istep 55-logs-nginx "$(readme 375 375)" "file:$CUE" "$CTRLC"
  istep 56-exec-api-service "$(readme 380 380)" "$PY_PROMPT" "ls" "$PY_PROMPT" "exit"
  istep 57-exec-nginx "$(readme 381 381)" '# $' "nginx -v" '# $' "exit"
  # extra (digest gotchas 11/12): a stopped frontend takes nginx down with it
  step 58-x-frontend-down "sudo docker stop frontend; sudo docker restart nginx; sleep 3; sudo docker ps -a --format 'table {{.Names}}\t{{.Status}}'; sudo docker logs nginx 2>&1 | tail -2; curl -s -o /dev/null -w 'http://localhost/ -> %{http_code}\n' http://localhost/"
  step 59-x-frontend-up "sudo docker start frontend nginx; sleep 3; sudo docker ps --format 'table {{.Names}}\t{{.Status}}'; curl -s -o /dev/null -w 'http://localhost/ -> %{http_code}\n' http://localhost/"
  step 60-x-images "sudo docker images; sudo du -sh /var/lib/docker"
  ;;
esac
