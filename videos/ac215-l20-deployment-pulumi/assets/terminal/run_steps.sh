#!/bin/bash
# Runs inside a capture machine (see capture.sh) as user `student`, recording each tutorial command's
# output to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# README.md:N = dlops-io/cheese-app-v3 @ 3ecef56 (main), mounted read-only at /source/README.md;
# multi-line README commands are read from those exact lines, so they run byte for byte as printed.
# Segments (file prefix = part of the video):
#   vm1    (vm/0x)  "Deployment to GCP (Manual)" on the VM: get-docker.sh, docker --version
#   vm2    (vm/1x-2x) folders, secret, network, vector-db (chroma), the loader
#   vm3/vm4/vm4b (vm/3x) api-service (vm4: capture-only CA re-tag after vm3's TLS crash, README run again)
#   vm5    (vm/38-51) interactive variant, frontend, nginx.conf, nginx, the URLs
#   vm6    (vm/52-60) the README's "SSH into the server" commands (README.md:371-383) + extras
#   pre    (laptop/p..) clone, the commits, the sibling secrets/ folder, capture-only base images
#   hubprep (capture-only) CA + local mirror for docker-hub.sh's docker-container BuildKit
#   partA  (laptop/a01-a03) docker login, frontend-react's docker-hub.sh; partA2 (a04-a06) builder extras
#   partB  (laptop/b01-b02) "Deployment to GCP (Single VM Instance)": docker-shell.sh as committed (fails)
#   partB2 (b02a-b02b) fix 1 (bookworm base), docker-shell.sh again (fails at the gcloud packages)
#   partB3 (b02c-b02d, then b03-b46) fix 2, docker-shell.sh builds; the README's commands in its shell
#   partB4 capture-only resume of partB3's commands (see capture.sh); partB5 (b35b/b36b) the image
#          stack's `pulumi up` with the provider's BuildKit given the proxy CA
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
make_key() {  # make_key <account>: capture-only, see the comment inside
  # There is NO real key here. A throwaway RSA key, generated now for no account and never written to
  # the repository, makes a well-formed service-account key file, so gcloud and Google's libraries load
  # it and the first real call fails where a student's would succeed (ASSETS.md, "What cannot run here").
  mkdir -p "$OUT/capture-only" ~/secrets
  openssl genrsa -out /tmp/throwaway.pem 2048 2>/dev/null
  ACCT=$1 python3 - <<'PYEOF'
import json, os
acct = os.environ["ACCT"]
info = {"type": "service_account", "project_id": "your-gcp-project",
        "private_key_id": "0000000000000000000000000000000000000000",
        "private_key": open("/tmp/throwaway.pem").read(),
        "client_email": f"{acct}@your-gcp-project.iam.gserviceaccount.com",
        "client_id": "000000000000000000000", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"}
json.dump(info, open(os.path.expanduser(f"~/secrets/{acct}.json"), "w"), indent=2)
info["private_key"] = "<a throwaway RSA key generated at capture time for no account; not committed>"
json.dump(info, open(os.environ["OUT"] + f"/capture-only/placeholder-{acct}.json", "w"), indent=2)
PYEOF
  rm -f /tmp/throwaway.pem
}
partB_commands() {  # the README's commands at the deployment container's prompt (partB3; partB4 resumes)
  C=cheese-app-deployment
  cstep() {  # cstep <name> <workdir> <command>: typed at the container's prompt (docker exec, same container)
    local name=$1 wd=$2; shift 2
    { echo "\$ $*"; docker exec -w "$wd" $C bash -c "$*" 2>&1 | sed 's/\x1b\[[0-9;]*m//g'; echo "[exit ${PIPESTATUS[0]}]"; } | mask > "$OUT/$name.txt"
  }
  ctstep() {  # ctstep <name> <workdir> <shown command> <exec'd command> [<regex> <typed>]...: the same, in a terminal
    local name=$1 wd=$2 shown=$3 cmd=$4; shift 4
    local args=()
    while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
    { echo "\$ $shown"
      python3 "$HERE/ptyrun.py" --cols 100 --rows 40 --timeout 600 "${args[@]}" -- docker exec -it -w "$wd" $C bash -c "$cmd"
      echo "[exit $?]"; } | mask > "$OUT/$name.txt"
  }
  # README.md:270-278 "Check versions of tools" + "gcloud auth list"
  cstep b03-gcloud-version /app "$(readme 272 272)"
  cstep b04-pulumi-version /app "$(readme 273 273)"
  cstep b05-kubectl-version /app "$(readme 274 274)"
  cstep b06-gcloud-auth-list /app "gcloud auth list"
  cstep b07-x-env /app "env | grep -E '^(GCP_|GOOGLE_|PULUMI_|USE_GKE)' | sort; ls -la /secrets; python --version; uv --version; which docker ssh; docker ps --format '{{.Names}}'"
  # README.md:283-291 "Configuring OS Login for service account": the template line, then the example
  cstep b08-oslogin-template /app "$(readme 286 286)"
  cstep b09-oslogin-example /app "$(readme 290 290)"
  # README.md:294-298 "Create SSH key for service account" (empty passphrase: Enter twice)
  ctstep b10-ssh-keygen /secrets "$(readme 295 297)" "ssh-keygen -f ssh-key-deployment" "passphrase" "" "passphrase" ""
  cstep b11-x-ls-keys /secrets "ls -la /secrets"
  # README.md:300-303 "Providing public SSH keys to instances"
  cstep b12-oslogin-ssh-keys-add /app "$(readme 302 302)"
  # README.md:318-322 "Deployment Setup": inventory.yml
  cstep b13-x-inventory /app "ls inventory.yml; find / -name inventory.yml -not -path '/proc/*' 2>/dev/null | head -3"
  # README.md:327-345 "Build and Push Docker Containers to Google Artifact Registry", verbatim
  ctstep b14-images-stack-init /app/deploy_images "cd deploy_images
$(readme 332 332)" "$(readme 332 332)" "(token|ENTER)" "$CTRLC"
  cstep b15-images-config-set /app/deploy_images "$(readme 333 333)"
  cstep b16-images-preview /app/deploy_images "$(readme 339 339)"
  cstep b17-images-up /app/deploy_images "$(readme 344 344)"
  # README.md:347-367 "Create Compute Instance (VM) & Deploy Containers", verbatim
  cstep b18-vm-stack-init /app/deploy_single_vm "$(readme 352 352)"
  for l in 353 354 355; do cstep b19-vm-config-set-$((l-352)) /app/deploy_single_vm "$(readme $l $l)"; done
  cstep b20-vm-preview /app/deploy_single_vm "$(readme 361 361)"
  cstep b21-vm-up /app/deploy_single_vm "$(readme 366 366)"
  # README.md:387-390 "Delete the Compute Instance / Persistent disk"
  cstep b22-destroy /app/deploy_single_vm "$(readme 389 389)"
  # extras: the same programs on Pulumi's local file backend (`pulumi login --local`), which needs no
  # cloud account, so each one runs up to its first call that needs Google (ASSETS.md)
  FRONT='urn:pulumi:dev::deploy-images::docker-build:index:Image::build-cheese-app-frontend-react'
  cstep b30-x-login-local /app/deploy_images "pulumi login --local"
  cstep b31-x-images-stack-init /app/deploy_images "$(readme 332 332)"
  cstep b32-x-images-config-set /app/deploy_images "$(readme 333 333)"
  cstep b33-x-images-config /app/deploy_images "pulumi config; cat Pulumi.dev.yaml; pulumi stack ls"
  cstep b34-x-images-preview-frontend /app/deploy_images "pulumi preview --stack dev --refresh --target '$FRONT'"
  cstep b35-x-images-up-frontend /app/deploy_images "pulumi up --stack dev --refresh -y --target '$FRONT'"
  cstep b36-x-images-after /app/deploy_images "pulumi stack ls; pulumi stack output; docker images"
  cstep b40-x-vm-stack-init /app/deploy_single_vm "$(readme 352 352)"
  for l in 353 354 355; do cstep b41-x-vm-config-set-$((l-352)) /app/deploy_single_vm "$(readme $l $l)"; done
  cstep b42-x-vm-config /app/deploy_single_vm "pulumi config"
  cstep b43-x-vm-preview /app/deploy_single_vm "$(readme 361 361)"
  cstep b44-x-vm-up /app/deploy_single_vm "$(readme 366 366)"
  cstep b45-x-destroy /app/deploy_single_vm "$(readme 389 389)"
  cstep b46-x-stacks-on-disk /app "pulumi stack ls --all; ls -R ~/.pulumi/stacks 2>/dev/null | head; ls /app/pulumi-plugins | head; git -C /app status --short 2>&1 | head"
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
  $DOCKER image inspect "$img" >/dev/null 2>&1 || $DOCKER pull -q "$img" >/dev/null
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
  ;;
vm6)
  PY_PROMPT='app@[0-9a-f]+:/app\$ $'
  # README.md:371-383 (written for the Pulumi VM; the container names are the same here)
  step 52-container-ls "$(readme 373 373)"
  CUE=/tmp/l20-cue
  rm -f $CUE; ( sleep 5; touch $CUE ) &
  istep 53-logs-api-service "$(readme 374 374)" "file:$CUE" "$CTRLC"
  rm -f $CUE; ( sleep 5; touch $CUE ) &
  istep 54-logs-frontend "$(readme 375 375)" "file:$CUE" "$CTRLC"
  rm -f $CUE; ( sleep 5; touch $CUE ) &
  istep 55-logs-nginx "$(readme 376 376)" "file:$CUE" "$CTRLC"
  istep 56-exec-api-service "$(readme 381 381)" "$PY_PROMPT" "ls" "$PY_PROMPT" "exit"
  istep 57-exec-nginx "$(readme 382 382)" '# $' "nginx -v" '# $' "exit"
  # extra (digest gotchas 11/12): a stopped frontend takes nginx down with it
  step 58-x-frontend-down "sudo docker stop frontend; sudo docker restart nginx; sleep 3; sudo docker ps -a --format 'table {{.Names}}\t{{.Status}}'; sudo docker logs nginx 2>&1 | tail -2; curl -s -o /dev/null -w 'http://localhost/ -> %{http_code}\n' http://localhost/"
  step 59-x-frontend-up "sudo docker start frontend nginx; sleep 3; sudo docker ps --format 'table {{.Names}}\t{{.Status}}'; curl -s -o /dev/null -w 'http://localhost/ -> %{http_code}\n' http://localhost/"
  step 60-x-images "sudo docker images; sudo du -sh /var/lib/docker"
  ;;
# ------------------------------------------------------------------------------------------------
pre)
  step p00-x-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; docker buildx version; git --version; docker images"
  # the README has no clone command (the course's repos are cloned in its setup); the usual one
  step p01-clone "git clone https://github.com/dlops-io/cheese-app-v3.git"
  step p02-x-git-log "git -C cheese-app-v3 log -1 --format='%H %ci %s'; git -C cheese-app-v3 branch -r | sed 's|work/[a-z]*|work/‹staff›|'"
  step p03-x-ls-remote "git ls-remote https://github.com/dlops-io/cheese-app-v3.git | sed 's|refs/heads/work/[a-z]*|refs/heads/work/‹staff›|'"
  # README.md:236-259: the two key files go into the secrets folder next to the repo
  step p04-mkdir-secrets "mkdir -p secrets"
  make_key deployment
  make_key gcp-service
  step p05-x-tree "ls -la; ls -la secrets; ls cheese-app-v3/src cheese-app-v3/src/deployment"
  capture_only_retag python:3.13-slim-bullseye base
  capture_only_retag node:20-alpine base
  ;;
# ------------------------------------------------------------------------------------------------
hubprep)
  # capture-only (recording sandbox): docker-hub.sh's builder is a docker-container BuildKit, which
  # pulls its base images itself (not from the laptop's image store) and does not trust the recording
  # proxy's CA. A buildkitd default config (picked up by `docker buildx create`, so docker-hub.sh runs
  # unchanged) gives it that CA for registries and a local mirror (registry:2 on localhost:5000) that
  # serves the CA-re-tagged node:20-alpine, so `apk add`/`npm ci` inside the build trust it too.
  mkdir -p "$OUT/capture-only" ~/.docker/buildx
  docker buildx rm multi-arch >/dev/null 2>&1; docker buildx use default
  docker rm -f l20-mirror >/dev/null 2>&1
  step capture-only/mirror-start "docker run -d --name l20-mirror -p 5000:5000 registry:2 >/dev/null && sleep 2 && docker tag node:20-alpine localhost:5000/library/node:20-alpine && docker push -q localhost:5000/library/node:20-alpine"
  cp "$CAPTURE_CA" ~/.docker/buildx/capture-ca.crt
  { echo '# capture-only, NOT part of the tutorial (see ASSETS.md)'
    echo '[registry."docker.io"]'
    echo '  mirrors = ["localhost:5000"]'
    echo "  ca = [\"$HOME/.docker/buildx/capture-ca.crt\"]"
    echo '[registry."localhost:5000"]'
    echo '  http = true'; } > ~/.docker/buildx/buildkitd.default.toml
  cp ~/.docker/buildx/buildkitd.default.toml "$OUT/capture-only/buildkitd.default.toml"
  ;;
# ------------------------------------------------------------------------------------------------
partA)
  # README.md:18-21 "Push Docker Images to Docker Hub": typed as printed, placeholders included
  step a01-docker-login "$(readme 21 21 | sed 's/^.*: `//; s/`$//')"
  # README.md:28-31 "Build, Tag & Push frontend-react": inside the folder, sh docker-hub.sh
  cd cheese-app-v3/src/frontend-react
  step a02-frontend-docker-hub "sh docker-hub.sh"
  step a03-x-buildx-ls "docker buildx ls"
  cd ~
  ;;
# ------------------------------------------------------------------------------------------------
partA2)
  # extras (digest gotcha 3): after docker-hub.sh, `multi-arch` (docker-container driver) is the
  # current builder in every terminal, and a plain `docker build` no longer lands in `docker images`
  d=$(mktemp -d); printf 'FROM node:20-alpine\nCMD ["node", "--version"]\n' > $d/Dockerfile
  step a04-x-build-after-hub "cd $d && docker build -q -t hello-node . ; docker run --rm hello-node"
  step a05-x-buildx-use-default "docker buildx use default; docker buildx ls | head -3"
  step a06-x-build-default "cd $d && docker build -q -t hello-node . >/dev/null; docker run --rm hello-node; docker rmi -f hello-node >/dev/null"
  rm -rf $d
  ;;
# ------------------------------------------------------------------------------------------------
partB)
  cd cheese-app-v3/src/deployment
  # README.md:265-267: "Go into docker-shell.sh and change GCP_PROJECT to your project id" (a placeholder)
  step b01-set-project "sed -i 's/\"ac215-project\" # Change/\"your-gcp-project\" # Change/' docker-shell.sh; grep -n 'GCP_PROJECT=' docker-shell.sh"
  # README.md:268 "Run sh docker-shell.sh", in a terminal. On 2026-11-05 the image does not build:
  # Debian 11 (bullseye) security updates have moved to archive.debian.org (ASSETS.md)
  istep b02-docker-shell "sh docker-shell.sh"
  cd ~
  ;;
# ------------------------------------------------------------------------------------------------
partB2)
  cd cheese-app-v3/src/deployment
  # extra: the fix the video shows, a newer Debian base (bookworm) on Dockerfile:4
  step b02a-x-fix-base "sed -i 's/^FROM python:3.13-slim-bullseye/FROM python:3.13-slim-bookworm/' Dockerfile; grep -n '^FROM' Dockerfile; git diff --stat"
  # capture-only: Docker Hub's anonymous pull limit (the sandbox's egress IP is shared) answered 429,
  # so the two images this build and the frontend build start FROM come from Google's Docker Hub
  # mirror (mirror.gcr.io, same digests), tagged under their Docker Hub names
  step capture-only/hub-mirror-pulls "for i in library/python:3.13-slim-bookworm docker/dockerfile:1.6; do docker image inspect \${i#library/} >/dev/null 2>&1 || { docker pull -q mirror.gcr.io/\$i && docker tag mirror.gcr.io/\$i \${i#library/}; }; done; docker images --digests | grep -E 'python|dockerfile'"
  capture_only_retag python:3.13-slim-bookworm base
  # README.md:268 again: the base now installs, and the next apt step fails (gcloud's package renamed)
  istep b02b-docker-shell-bookworm "sh docker-shell.sh"
  cd ~
  ;;
# ------------------------------------------------------------------------------------------------
partB3)
  cd cheese-app-v3/src/deployment
  # extra: the second fix, the package names Google's apt repository uses now (Dockerfile:30)
  step b02c-x-fix-gcloud-packages "sed -i 's/google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin/google-cloud-cli google-cloud-cli-gke-gcloud-auth-plugin/' Dockerfile; git diff Dockerfile"
  CUE=/tmp/l20-cue-shell; rm -f $CUE
  # README.md:268 a third time: it builds; the shell stays open (at its prompt) until $CUE exists
  istep b02d-docker-shell-fixed "sh docker-shell.sh" "file:$CUE" "exit" &
  SHELL_PID=$!
  for i in $(seq 1800); do docker top cheese-app-deployment -eo pid,args 2>/dev/null | awk '{print $NF}' | grep -qx '/bin/bash' && break; sleep 1; done
  sleep 2
  partB_commands
  touch $CUE
  wait $SHELL_PID
  cd ~
  ;;
# ------------------------------------------------------------------------------------------------
partB5)
  # capture-only: b35's build stopped at x509 because pulumi-docker-build created its own
  # docker-container BuildKit ("wonderful_wilbur", from inside the deployment container), which does
  # not trust the recording proxy's CA. Give root's buildx in that container the same default config
  # as hubprep (CA + the local node:20-alpine mirror, reached at the laptop's bridge gateway), drop
  # that builder, and run the same `pulumi up` again (b35b; without --refresh: after the failed create,
  # the refresh step refuses a --target that is not in the stack yet).
  C=cheese-app-deployment
  GWL=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  docker cp "$CAPTURE_CA" $C:/root/capture-ca.crt
  docker exec $C sh -c "mkdir -p /root/.docker/buildx && printf '%s\n' '# capture-only, NOT part of the tutorial (see ASSETS.md)' '[registry.\"docker.io\"]' '  mirrors = [\"$GWL:5000\"]' '  ca = [\"/root/capture-ca.crt\"]' '[registry.\"$GWL:5000\"]' '  http = true' '[registry.\"us-docker.pkg.dev\"]' '  ca = [\"/root/capture-ca.crt\"]' > /root/.docker/buildx/buildkitd.default.toml"
  docker exec $C cat /root/.docker/buildx/buildkitd.default.toml > "$OUT/capture-only/deployment-buildkitd.default.toml"
  step capture-only/drop-provider-builder "docker exec $C sh -c 'for b in \$(docker buildx ls --format \"{{.Name}}\" | grep -v \"^default\$\"); do docker buildx rm \$b; done'"
  FRONT='urn:pulumi:dev::deploy-images::docker-build:index:Image::build-cheese-app-frontend-react'
  { echo "\$ pulumi up --stack dev -y --target '$FRONT'"; docker exec -w /app/deploy_images $C bash -c "pulumi up --stack dev -y --target '$FRONT'" 2>&1 | sed 's/\x1b\[[0-9;]*m//g'; echo "[exit ${PIPESTATUS[0]}]"; } | mask > "$OUT/b35b-x-images-up-frontend-build.txt"
  { echo '$ pulumi stack ls; pulumi stack output; docker images | head -4'; docker exec -w /app/deploy_images $C bash -c 'pulumi stack ls; pulumi stack output; docker images | head -4' 2>&1; echo "[exit $?]"; } > "$OUT/b36b-x-images-after.txt"
  ;;
# ------------------------------------------------------------------------------------------------
partB4)
  # capture-only resume: partB3's readiness probe used `docker top -eo args`, which this engine
  # refuses ("Couldn't find PID field"); its shell (b02d) was left open and these commands ran in it
  CUE=/tmp/l20-cue-shell
  partB_commands
  touch $CUE
  ;;
esac
