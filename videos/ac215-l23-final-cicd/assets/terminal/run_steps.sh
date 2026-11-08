#!/bin/bash
# Runs inside the "laptop" capture container (see capture.sh) as user `student`, recording each
# command's output to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# L23 follows the AWS variant (series decision, as L15):
#   dlops-io/cheese-app-aws @ 5950118b0ed97c12c799920846d3eb70b1a47385 (main, 2024-11-21, "cleanup")
# README.md (148 lines) top to bottom, then the workflow .github/workflows/ci_cd_aws.yml (not in
# the README). Segments (folder laptop/):
#   pre       versions, ls-remote, clone, the capture-only base image          -> 00-09
#   secrets   policy JSON, ~/secrets (placeholder CSV, throwaway key), key names -> 10-19
#   shell-a   "Deployment Steps" (README:74-77): cd, the CSV line, sh docker-shell.sh, bash
#             docker-shell.sh with the Dockerfile as committed                  -> 20-26
#   shell-b   the toolbox without the Helm lines (capture-only), /secrets empty -> 27-29
#   shell-c   docker-shell.sh's other two values (extra), /secrets filled       -> 30-31
#   toolbox   extras inside the toolbox: versions, the ">=9.0.0" file, STS, inventory, syntax
#             checks, task lists                                               -> 32-37
#   toolbox-b the Ansible collections in the toolbox                           -> 38
#   playbooks README:89, 94, 97, 102, 107-111, 116, 141, 147, each typed in the toolbox -> 40-49
#   ci        the workflow's steps, run by hand on the laptop up to the first real error  -> 50-59
#   extras    Chroma latest vs 0.5.18, the nginx routes, `docker run -it`, prune  -> 60-69
# Steps whose name contains "-x-" are extras: not in the README; checks the video uses.
OUT=$1; SEG=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
umask 022   # a login shell's default (docker exec would otherwise run with umask 0000)
cd ~
PIN=5950118b0ed97c12c799920846d3eb70b1a47385
REPO=~/cheese-app-aws
DEP=$REPO/src/deployment
PH_AK=PLACEHOLDER_NOT_A_REAL_ACCESS_KEY                   # capture-only AWS "keys": obviously
PH_SK=PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000       # fake, rejected by AWS
P_ROOT='root@[0-9a-f]{12}:/app# $'                        # the toolbox prompt (it runs as root)

# --- masks (series rule): values the repo commits that no capture may print. They are read here,
# at run time, from the tutorial's own files at the pinned commit, so this script contains none:
# the author's AWS account id (docker-shell.sh:17), the server's public IP (inventory.yml:30), the
# committed NEXTAUTH_SECRET (inventory.yml:24) and the instructor's name (About.jsx:13).
if [ -d $REPO/.git ]; then
  M_ACCT=$(git -C $REPO show $PIN:src/deployment/docker-shell.sh | sed -n 17p | grep -oE '[0-9]{12}')
  M_IP=$(git -C $REPO show $PIN:src/deployment/inventory.yml | sed -n 30p | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sed 's/\./\\./g')
  M_SEC=$(git -C $REPO show $PIN:src/deployment/inventory.yml | sed -n 24p | sed -E 's/.*nextauth_secret: *"?([^"]*)"?.*/\1/' | sed -e 's/[^A-Za-z0-9\/]/[&]/g' -e 's/\//\\\//g')
  M_NAME=$(git -C $REPO show $PIN:src/frontend-react/src/components/home/About.jsx | grep -o 'My name is [A-Z][a-z]* [A-Z][a-z]*' | head -1 | cut -d' ' -f4-)
fi
mask() {
  if [ -z "$M_ACCT" ]; then sed 's/\x1b\[[0-9;?]*[A-Za-z]//g'; return; fi
  sed -E -e 's/\x1b\[[0-9;?]*[A-Za-z]//g' -e "s/$M_ACCT/YOUR_ACCOUNT_ID/g" -e "s/$M_IP/<EXTERNAL_IP>/g" \
    -e "s/$M_SEC/<nextauth-secret>/g" -e "s/${M_NAME}|${M_NAME%% *}|${M_NAME##* }/‹instructor›/g"
}
step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1; echo "[exit $?]"; } < /dev/null | mask > "$OUT/$name.txt"
}
istep() {  # istep <name> <command> [<prompt regex> <typed line>]...   (in a terminal, typed)
  local name=$1 cmd=$2; shift 2
  local args=()
  while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
  { echo "\$ $cmd"
    python3 "$HERE/ptyrun.py" --cols "${PTY_COLS:-110}" --rows "${PTY_ROWS:-50}" --timeout "${PTY_TIMEOUT:-900}" \
      "${args[@]}" -- bash -c "$cmd"
    echo "[exit $?]"; } | mask > "$OUT/$name.txt"
}
capture_only_base() {  # recording sandbox only (CAPTURE_CA set); see ASSETS.md, "capture-only"
  # The toolbox Dockerfile downloads over TLS, and the sandbox's TLS is re-signed by its proxy,
  # which also refuses plain http. ubuntu:20.04 is rebuilt with that proxy's CA (in
  # /usr/local/share/ca-certificates, so the Dockerfile's own `apt-get install ca-certificates`
  # keeps it), https apt sources and the CA env vars, then re-tagged under the same name, so the
  # tutorial's Dockerfile builds unchanged.
  [ -n "$CAPTURE_CA" ] || return 0
  local d; d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"
  mkdir -p "$OUT/capture-only"
  cat > "$d/Dockerfile" <<'EOF'
# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through a
# TLS-intercepting proxy that refuses plain http. Same ubuntu:20.04 plus that proxy's CA, https apt
# sources and the CA env vars, re-tagged under the same name so the tutorial Dockerfile builds
# unchanged.
FROM ubuntu:20.04
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN mkdir -p /etc/ssl/certs && cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \
 && sed -i -e 's|http://archive.ubuntu.com|https://archive.ubuntu.com|g' -e 's|http://security.ubuntu.com|https://security.ubuntu.com|g' /etc/apt/sources.list
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \
    AWS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt
EOF
  cp "$d/Dockerfile" "$OUT/capture-only/ubuntu-20.04-base.Dockerfile"
  step capture-only/ubuntu-20.04-base-build "docker build -t ubuntu:20.04 $d"
  rm -f "$d/Dockerfile" "$d/capture-ca.crt"; rmdir "$d"
}
toolbox() {  # toolbox <name> <typed line>...: README:77's script (bash, see 23-24), commands typed
  local name=$1; shift
  local pairs=()
  for c in "$@"; do pairs+=("$P_ROOT" "$c"); done
  PTY_COLS=${PTY_COLS:-160} PTY_TIMEOUT=${PTY_TIMEOUT:-1200} istep "$name" "bash docker-shell.sh" "${pairs[@]}" "$P_ROOT" 'exit'
}

case $SEG in
pre)
  step 00-x-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; . /etc/os-release; echo \$PRETTY_NAME; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; docker buildx version; git --version; bash --version | head -1; ls -l /bin/sh"
  step 01-x-ls-remote "git ls-remote https://github.com/dlops-io/cheese-app-aws.git"
  # The README has no clone command (it starts with the console steps); the folder layout of
  # README.md:55-60 puts the clone next to secrets/.
  step 02-x-clone "git clone https://github.com/dlops-io/cheese-app-aws.git"
  step 03-x-git-log "git -C cheese-app-aws log -1 --format='%H %ci %s'; git -C cheese-app-aws branch -a; git -C cheese-app-aws tag"
  step 04-x-ls "ls -a cheese-app-aws cheese-app-aws/src cheese-app-aws/src/deployment"
  capture_only_base
  ;;
secrets)
  # "Setup AWS Keys for Authentication" (README:15-60), "Create AWS EC2 Key Pair" (README:62-64):
  # console clicks -> illustration (ASSETS.md). Extra: the policy JSON the README pastes parses.
  step 10-x-policy-json "sed -n '23,43p' cheese-app-aws/README.md | python3 -m json.tool"
  # capture-only: what the two downloads would leave in ~/secrets. The CSV has AWS's column header
  # and obviously fake placeholder keys; the .pem is a throwaway RSA key made now, for no account.
  mkdir -p ~/secrets
  printf 'Access key ID,Secret access key\r\n%s,%s\r\n' "$PH_AK" "$PH_SK" > ~/secrets/deployment-ac215-user_accessKeys.csv
  mkdir -p "$OUT/capture-only"
  rm -f ~/secrets/cheese-app-ac215-key-pair.pem   # a re-run makes a new throwaway key
  step capture-only/11-throwaway-key "ssh-keygen -q -t rsa -b 2048 -m PEM -N '' -C '' -f ~/secrets/cheese-app-ac215-key-pair.pem && rm ~/secrets/cheese-app-ac215-key-pair.pem.pub && ls -l ~/secrets"
  step 12-secrets-layout "ls ~; ls -l ~/secrets"            # README:55-60 (+ the .pem of README:64)
  step 13-x-key-names "cd cheese-app-aws && grep -rn 'cheese-app-ac215-key-pair\|ac215_2024' README.md src/deployment .github"
  step 14-x-chmod-pem "chmod 400 ~/secrets/cheese-app-ac215-key-pair.pem && ls -l ~/secrets"
  ;;
shell-a)
  cd $DEP
  # "Deployment Steps" (README:74-77)
  step 20-cd-deployment "pwd; ls -a"                                       # README:75 "Go to src/deployment folder"
  step 21-x-as-cloned "bash docker-shell.sh"                               # extra: before the edit
  # README:76: "Change ... CSV_FILE=\"../../../secrets/deployment-ac215-user_accessKeys.csv\"" (sed is the editor)
  step 22-edit-csv-file "sed -i 's|^CSV_FILE=.*|CSV_FILE=\"../../../secrets/deployment-ac215-user_accessKeys.csv\"|' docker-shell.sh && sed -n '9,11p' docker-shell.sh && ls -l ../../../secrets/deployment-ac215-user_accessKeys.csv"
  step 23-sh-docker-shell "sh docker-shell.sh"                             # README:77, as written
  step 24-x-which-sh "ls -l /bin/sh; head -1 docker-shell.sh"
  # README:77 with bash (the script's own shebang): the Dockerfile as committed
  PTY_TIMEOUT=1500 istep 25-x-bash-docker-shell-as-committed "bash docker-shell.sh"
  step 26-x-helm-repo "curl -sS -o /dev/null -w '%{http_code} %{ssl_verify_result}\n' https://baltocdn.com/helm/signing.asc; curl -sS -o /dev/null -w '%{http_code}\n' https://packages.buildkite.com/helm-linux/helm-debian/gpgkey"
  ;;
shell-b)
  cd $DEP
  # capture-only: the toolbox without Helm (unused by every playbook), see ASSETS.md and 25
  step 27-x-drop-helm "sed -i -e '/baltocdn.com\/helm\/signing.asc/d' -e '/helm-stable-debian.list/d' -e 's/install -y --no-install-recommends kubectl helm /install -y --no-install-recommends kubectl /' Dockerfile && git diff Dockerfile"
  PTY_TIMEOUT=1500 toolbox 28-x-docker-shell 'ls -la /secrets; pwd; ls'
  step 29-x-docker-images "docker images"
  ;;
shell-c)
  cd $DEP
  # extra: the two lines README:76 does not mention: SECRETS_DIR (four ../ like CSV_FILE) and the
  # hard-coded account id (shown as YOUR_ACCOUNT_ID; a student types their own 12 digits)
  step 30-x-edit-secrets-dir-account "sed -i -e 's|^export SECRETS_DIR=.*|export SECRETS_DIR=\$(pwd)/../../../secrets/|' -e 's|^    export AWS_ACCOUNT_ID=.*|    export AWS_ACCOUNT_ID=\"YOUR_ACCOUNT_ID\"|' docker-shell.sh && sed -n '10p;17p;26p' docker-shell.sh"
  toolbox 31-docker-shell 'ls -la /secrets; env | grep ^AWS_ | cut -d= -f1 | sort'
  ;;
toolbox)
  cd $DEP
  toolbox 32-x-versions 'aws --version' 'ansible --version' 'pip3 show ansible ansible-core 2>/dev/null | grep -E "^(Name|Version)"' 'docker --version' 'kubectl version --client 2>&1 | head -1' 'which helm; echo helm-exit:$?'
  toolbox 33-x-redirect-file 'ls /' 'head -3 "/=9.0.0"; tail -1 "/=9.0.0"'
  toolbox 34-x-sts 'aws sts get-caller-identity'
  toolbox 35-x-inventory-graph 'ansible-inventory -i inventory.yml --graph'
  toolbox 36-x-syntax-check 'for f in deploy-*.yml; do ansible-playbook $f -i inventory.yml --syntax-check; done'
  toolbox 37-x-list-tasks 'for f in deploy-*.yml; do ansible-playbook $f -i inventory.yml --list-tasks; done'
  ;;
toolbox-b)
  cd $DEP
  toolbox 38-x-collections 'ansible-galaxy collection list 2>/dev/null | grep "^# \|amazon\|community"'
  ;;
playbooks)
  cd $DEP
  git checkout -q -- inventory.yml   # capture-only: a re-run starts from the committed inventory
  # README:89 "Build and Push Docker Containers to AWS ECR"
  toolbox 40-deploy-docker-images 'ansible-playbook deploy-docker-images.yml -i inventory.yml'
  step 41-x-docker-images "docker images"
  # README:94 "Create Compute Instance (VM) Server in GCP" (it is EC2)
  toolbox 42-create-instance 'ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=present'
  # README:97 "get the IP address ... update the appserver>hosts in inventory.yml": no instance here;
  # the placeholder host name EXTERNAL_IP stands where the console's address goes (sed is the
  # editor; a placeholder, not an address: the next playbooks stop where SSH cannot resolve it)
  step 43-edit-appserver-host "sed -i '30s/.*/        EXTERNAL_IP:/' inventory.yml && sed -n '27,30p' inventory.yml"
  # README:102 "Provision Compute Instance in GCP" (it is EC2)
  toolbox 44-provision-instance 'ansible-playbook deploy-provision-instance.yml -i inventory.yml'
  # README:107-111: the key line for "no ci/cd" (comment line 4, uncomment line 7)
  step 45-switch-key-line "sed -i -e '4s/^    ansible_ssh/    # ansible_ssh/' -e '7s/^    # ansible_ssh/    ansible_ssh/' inventory.yml && sed -n '3,8p' inventory.yml"
  # README:116
  toolbox 46-setup-containers 'ansible-playbook deploy-setup-containers.yml -i inventory.yml'
  # README:141
  toolbox 47-setup-webserver 'ansible-playbook deploy-setup-webserver.yml -i inventory.yml'
  # README:147 "Delete the Compute Instance / Persistent disk"
  toolbox 48-delete-instance 'ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=absent'
  step 49-x-git-status "cd $REPO && git status --short"
  ;;
ci)
  # .github/workflows/ci_cd_aws.yml is not in the README. Nothing here is a GitHub Actions run: the
  # runner's steps are run by hand on the laptop, on a fresh clone of the pinned commit (what
  # actions/checkout would fetch), with the placeholder secrets, up to the first real error.
  step 50-x-keyword-history "git -C $REPO log --format=%s | sort | uniq -c | sort -rn"
  rm -rf ~/runner && mkdir -p ~/runner && git clone -q $REPO ~/runner/cheese-app-aws
  W=~/runner/cheese-app-aws
  # ci_cd_aws.yml:46-50 "Generate Docker tag" ($GITHUB_ENV is a file on the runner)
  step 51-x-ci-docker-tag "cd $W && export GITHUB_ENV=~/runner/github_env && echo \$(date +%Y%m%d%H%M%S) > $W/src/deployment/.docker-tag
export DOCKER_TAG=\$(cat $W/src/deployment/.docker-tag)
echo \"DOCKER_TAG=\$DOCKER_TAG\" >> \$GITHUB_ENV
cat \$GITHUB_ENV"
  # ci_cd_aws.yml:72-90 "Setup SSH Config and Key" in a scratch HOME (the runner's ~), with the
  # throwaway key where ${{ secrets.AWS_SSH_KEY }} goes; :92-97 "Debug SSH Setup"
  step 52-x-ci-ssh-setup "export HOME=~/runner/home AWS_SSH_KEY=\"\$(cat ~/secrets/cheese-app-ac215-key-pair.pem)\" && mkdir -p \$HOME && cd $W && mkdir -p ~/.ssh
echo \"Host *
  StrictHostKeyChecking no
  UserKnownHostsFile=/dev/null\" > ~/.ssh/config
echo \"\$AWS_SSH_KEY\" > ~/.ssh/ac215_2024.pem
chmod 600 ~/.ssh/config
chmod 600 ~/.ssh/ac215_2024.pem
mkdir -p $W/src/deployment/secrets
cp ~/.ssh/config $W/src/deployment/secrets/
cp ~/.ssh/ac215_2024.pem $W/src/deployment/secrets/
echo \"Runner SSH directory:\"
ls -la ~/.ssh/
echo \"Deployment secrets directory:\"
ls -la $W/src/deployment/secrets/"
  # ci_cd_aws.yml:99-131 "Run Deployment Container" (the toolbox image is the one built in 28/31,
  # without Helm; the runner would build it from the committed Dockerfile at :41-44)
  step 53-x-ci-run-deployment-container "export AWS_ACCESS_KEY_ID=$PH_AK AWS_SECRET_ACCESS_KEY=$PH_SK AWS_ACCOUNT_ID=YOUR_ACCOUNT_ID AWS_DEFAULT_REGION=us-east-1 \$(cat ~/runner/github_env) SSH_KEY_PATH=/root/.ssh/ac215_2024.pem
echo \"Deploying with tag: \$DOCKER_TAG\"
docker run --rm --name cheese-app-deployment \\
  -v /var/run/docker.sock:/var/run/docker.sock \\
  -v $W/src/deployment:/deployment \\
  -v $W/src/deployment/secrets:/root/.ssh \\
  -e AWS_ACCESS_KEY_ID \\
  -e AWS_SECRET_ACCESS_KEY \\
  -e AWS_DEFAULT_REGION \\
  -e AWS_ACCOUNT_ID \\
  -e DOCKER_TAG \\
  cheese-app-deployment \\
  /bin/bash -c \"cd /deployment && \\
    chown -R root:root /root/.ssh && \\
    chmod 700 /root/.ssh && \\
    chmod 600 /root/.ssh/ac215_2024.pem && \\
    chmod 600 /root/.ssh/config && \\
    ls -la /root/.ssh && \\
    aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin \\\$AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com && \\
    ANSIBLE_STDOUT_CALLBACK=debug ansible-playbook deploy-setup-containers.yml -i inventory.yml --extra-vars \\\"aws_access_key=\\\$AWS_ACCESS_KEY_ID aws_secret_key=\\\$AWS_SECRET_ACCESS_KEY aws_region=\\\$AWS_DEFAULT_REGION aws_account_id=\\\$AWS_ACCOUNT_ID docker_network_name=appnetwork docker_tag=\\\$DOCKER_TAG\\\" -vv && \\
    ansible-playbook deploy-setup-webserver.yml -i inventory.yml\""
  ;;
extras)
  cd $DEP
  # G10: the server image the playbook runs (deploy-setup-containers.yml:151) vs the pin of the
  # local compose file (src/vector-db/docker-compose.yml:25) and the clients (chromadb 0.5.18)
  step 60-x-chroma-latest "docker run -d --name vector-db -p 8000:8000 chromadb/chroma:latest >/dev/null && for i in \$(seq 60); do curl -s localhost:8000/api/v2/heartbeat >/dev/null && break; sleep 1; done
docker image inspect chromadb/chroma:latest --format '{{index .RepoDigests 0}}'
curl -s localhost:8000/api/v2/version; echo
curl -s -w ' HTTP %{http_code}\n' localhost:8000/api/v1/heartbeat
curl -s -w ' HTTP %{http_code}\n' localhost:8000/api/v2/heartbeat
docker rm -f vector-db >/dev/null"
  step 61-x-chroma-0518 "docker run -d --name vector-db -p 8000:8000 chromadb/chroma:0.5.18 >/dev/null && for i in \$(seq 60); do curl -s localhost:8000/api/v1/heartbeat >/dev/null && break; sleep 1; done
curl -s localhost:8000/api/v1/version; echo
curl -s -w ' HTTP %{http_code}\n' localhost:8000/api/v1/heartbeat
docker rm -f vector-db >/dev/null"
  # The routes of nginx-conf/nginx/nginx.conf, on the laptop: the README's nginx (deploy-setup-
  # webserver.yml:23-35: nginx:stable, appnetwork, the conf mounted as /etc/nginx/nginx.conf) in
  # front of two stand-ins named api-service (:9000) and frontend (:3000) that answer with the path
  # they received. Then the README's server-side commands (README:122-131), without sudo and -f.
  docker network create appnetwork >/dev/null 2>&1
  for s in api-service:9000 frontend:3000; do
    docker run -d --name ${s%%:*} --network appnetwork python:3.12-slim-bookworm python -c "
import http.server
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        b = ('${s%%:*} received ' + self.path + '\n').encode()
        self.send_response(200); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
http.server.HTTPServer(('', ${s##*:}), H).serve_forever()" >/dev/null
  done
  step 62-x-nginx-routes "docker run -d --name nginx --network appnetwork -p 80:80 -p 443:443 -v $DEP/nginx-conf/nginx/nginx.conf:/etc/nginx/nginx.conf nginx:stable >/dev/null && sleep 3
curl -s localhost/api/newsletters
curl -s localhost/api/chat/llm
curl -s localhost/
curl -s localhost/chat
curl -s -w 'HTTP %{http_code}\n' -o /dev/null localhost/api"
  step 63-x-container-ls "docker container ls --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'"
  step 64-x-container-logs-nginx "docker container logs nginx 2>&1 | tail -8"
  step 65-x-exec-nginx "docker exec nginx nginx -v; docker exec nginx ls /etc/nginx"
  docker rm -f nginx api-service frontend >/dev/null 2>&1; docker network rm appnetwork >/dev/null 2>&1
  # G13: the loader task's `docker run --rm -it` (deploy-setup-containers.yml:165) without a terminal
  step 66-x-run-it-no-tty "docker run --rm -it nginx:stable true"
  # G14: the build playbook's last task (deploy-docker-images.yml:59-60), stdin at EOF
  step 67-x-system-prune "docker system prune -a"
  step 68-x-docker-images "docker images"
  ;;
*) echo "unknown segment $SEG" >&2; exit 2 ;;
esac
