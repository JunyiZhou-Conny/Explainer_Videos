#!/bin/bash
# Runs inside a fresh capture container as user `student`, recording each tutorial command's output
# to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <part>
#   part = laptop  (README "Developing App using Containers": a fresh Docker engine = your laptop)
#        | push    (its "Pushing Docker Image to Docker Hub" part, in a second fresh laptop engine)
#        | vm      (README "Running App on VM using Docker": a fresh Debian VM-like container)
# Steps marked "extra" are not in the README; they are checks the video uses.
OUT=$1; PART=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
cd ~

step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1; echo "[exit $?]"; } \
    | grep -v "^WARNING: apt does not have a stable CLI interface" > "$OUT/$name.txt"
}
istep() {  # istep <name> <command> [<prompt regex> <typed line>]...   (in a terminal, typed)
  local name=$1 cmd=$2; shift 2
  local args=()
  while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
  { echo "\$ $cmd"
    python3 "$HERE/ptyrun.py" --cols "${PTY_COLS:-80}" --rows "${PTY_ROWS:-24}" --timeout 900 \
      "${args[@]}" -- bash -c "$cmd"
    echo "[exit $?]"; } > "$OUT/$name.txt"
}
capture_only_base() {  # recording sandbox only (CAPTURE_CA set); see ASSETS.md, "capture-only"
  [ -n "$CAPTURE_CA" ] || return 0
  local d; d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"
  {
    echo "# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through"
    echo "# a TLS-intercepting proxy. Same python:3.12-slim-bookworm plus that proxy's CA and https apt"
    echo "# sources, re-tagged under the same name so that the README's Dockerfiles build unchanged."
    echo "FROM python:3.12-slim-bookworm"
    echo "COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt"
    echo "RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \\"
    echo " && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources"
    echo "ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt"
  } > "$d/Dockerfile"
  mkdir -p "$OUT/capture-only"; cp "$d/Dockerfile" "$OUT/capture-only/base.Dockerfile"
  { echo "\$ docker build -t python:3.12-slim-bookworm <folder with base.Dockerfile and the CA>"
    docker build -t python:3.12-slim-bookworm "$d" 2>&1; echo "[exit $?]"; } > "$OUT/capture-only/base-build.txt"
  rm -rf "$d"
}
hub_retry() {  # hub_retry step|istep <name> <args...>   (recording sandbox only: CAPTURE_HUB_WAIT set)
  # The sandbox's few egress IPs are shared with other jobs and Docker Hub limits anonymous pulls per
  # IP (100 per hour), so a pull can fail with "toomanyrequests" / "429 Too Many Requests" for reasons
  # that have nothing to do with the tutorial. Run the step again until it gets through; the file
  # keeps the run that did, capture-only/hub-retries.txt counts the failed attempts.
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
P='[:/]# $'      # the container's bash prompt, root@<id>:/#
PY='>>> $'       # the Python REPL prompt

if [ "$PART" = laptop ]; then
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; docker buildx version; git --version"

  # --- README: Make sure we do not have any running containers and clear up an unused images
  step 01-container-ls "docker container ls"
  istep 02-system-prune "docker system prune" '\[y/N\] $' y
  step 03-image-ls "docker image ls"

  # --- README: Clone the github repository (the command is the one at README.md:50)
  step 04-clone "git clone https://github.com/dlops-io/simple-translate.git"
  cd simple-translate
  step 05-ls "ls -a"                                       # extra
  step 06-git-log "git log --oneline -1"                   # extra: the commit the video uses
  step 07-build-no-dockerfile "docker build -t simple-translate -f Dockerfile ."   # extra: before the file exists

  # --- README: Create Dockerfile, Step 1..5 (each block copied from README.md), Build + Run after each
  sed -n 135,136p README.md > Dockerfile
  step 08-dockerfile-v1 "cat Dockerfile"
  hub_retry step 09-build-v1 "docker build -t simple-translate -f Dockerfile ."
  step 10-config-v1 "docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}} WorkingDir={{json .Config.WorkingDir}}'"   # extra
  istep 11-run-v1 "docker run --rm -ti simple-translate" "$PY" "exit()"
  step 12-git-status "git status"                          # extra: .gitignore hides Dockerfile

  { echo; sed -n 142p README.md; } >> Dockerfile
  step 13-dockerfile-v2 "cat Dockerfile"
  step 14-build-v2 "docker build -t simple-translate -f Dockerfile ."
  step 15-config-v2 "docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}'"   # extra
  istep 16-run-v2 "docker run --rm -ti simple-translate" "$P" "exit"

  capture_only_base   # sandbox only, before the first RUN that downloads (see ASSETS.md)

  { echo; sed -n 148,151p README.md; } >> Dockerfile
  step 17-dockerfile-v3 "cat Dockerfile"
  step 18-build-v3 "docker build -t simple-translate -f Dockerfile ."
  istep 19-run-v3 "docker run --rm -ti simple-translate" "$P" "ls" "$P" "python cli.py" "$P" "exit"

  { echo; sed -n 157p README.md; } >> Dockerfile
  step 20-dockerfile-v4 "cat Dockerfile"
  step 21-build-v4 "docker build -t simple-translate -f Dockerfile ."
  istep 22-run-v4 "docker run --rm -ti simple-translate" \
    "$P" "ls -a" "$P" "python cli.py" "$P" ".venv/bin/python --version" \
    "$P" "source .venv/bin/activate && python cli.py" "$P" "exit"

  { echo; sed -n 163,164p README.md; } >> Dockerfile
  step 23-dockerfile-v5 "cat Dockerfile"
  step 24-build-v5 "docker build -t simple-translate -f Dockerfile ."
  step 25-config-v5 "docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}} Cmd={{json .Config.Cmd}}'"   # extra
  istep 26-run-v5 "docker run --rm -ti simple-translate" \
    "$P" "which python" "$P" "python --version" "$P" 'echo $VIRTUAL_ENV' "$P" "exit"

  # --- README: Solution Dockerfile: Dockerfile.txt
  step 27-diff-solution "diff Dockerfile Dockerfile.txt"   # extra
  step 28-cp-solution "cp Dockerfile.txt Dockerfile"       # extra (the README only names the file)

  # --- README: Build Docker Image (typed in a terminal: the compact progress view you see)
  PTY_COLS=100 PTY_ROWS=60 istep 29-build "docker build -t simple-translate -f Dockerfile ."
  step 30-image-ls "docker image ls"                       # extra

  # --- README: Run Docker Container, Running the translate code, exit
  istep 31-run "docker run --rm -ti simple-translate" \
    "$P" 'python cli.py -t "Good morning" -s "en" -d "es"' "$P" "exit"
  step 32-ps-a "docker ps -a"                              # extra: --rm removed it

  # --- extras on the finished image (what the video explains)
  istep 33-inside "docker run --rm -ti simple-translate" \
    "$P" "pwd" "$P" 'echo $$' "$P" "which python" "$P" "python --version" \
    "$P" "/usr/local/bin/python --version" "$P" "ls /root/.local/share/uv/python" \
    "$P" "cat .venv/pyvenv.cfg" "$P" "ls -a /" "$P" "exit"
  step 34-history "docker history simple-translate"
  step 35-platform "uname -m; docker image inspect simple-translate --format '{{.Os}}/{{.Architecture}}'"
  istep 36-run-args "docker run --rm -ti simple-translate python cli.py"
  step 37-run-c "docker run --rm simple-translate -c \"source .venv/bin/activate && python cli.py -d fr\""
  step 38-rebuild-same "docker build --progress=plain -t simple-translate -f Dockerfile ."
  sed -i 's/default="I love cheese"/default="I love brie"/' cli.py
  step 39-edit-cli "git diff"
  step 40-rebuild-edited "docker build --progress=plain -t simple-translate -f Dockerfile ."
  git checkout -q cli.py
  step 41-rebuild-restored "docker build --progress=plain -t simple-translate -f Dockerfile ."
  PTY_COLS=100 PTY_ROWS=60 istep 42-docker-shell "sh docker-shell.sh" "$P" "exit"

  # --- README: Pushing Docker Image to Docker Hub (<USER NAME> = student; no Docker Hub login here)
  step 43-tag "docker tag simple-translate student/simple-translate-ac215"
  step 44-image-ls-tagged "docker image ls"
  # (push, login and the registry extras: part "push", in laptop-push/)
elif [ "$PART" = push ]; then
  # a second fresh laptop engine, for the push section (see ASSETS.md): rebuild the README image
  git clone -q https://github.com/dlops-io/simple-translate.git && cd simple-translate
  cp Dockerfile.txt Dockerfile
  capture_only_base
  { echo "\$ docker build -t simple-translate -f Dockerfile ."; docker build -t simple-translate -f Dockerfile . 2>&1; echo "[exit $?]"; } \
    > "$OUT/capture-only/build.txt"
  # --- README: Pushing Docker Image to Docker Hub (<USER NAME> = student; no Docker Hub login here)
  step 01-tag "docker tag simple-translate student/simple-translate-ac215"
  step 02-image-ls "docker image ls"
  hub_retry istep 03-push-no-login "docker push student/simple-translate-ac215"
  # extra: the same login/tag/push against a throwaway local registry, to show the real messages
  hub_retry step 04-registry "docker run -d -p 5000:5000 --name registry -v \$HOME/registry-auth:/auth -e REGISTRY_AUTH=htpasswd -e REGISTRY_AUTH_HTPASSWD_REALM=local -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd registry:3 >/dev/null && sleep 3 && docker ps --format '{{.Image}}  {{.Ports}}  {{.Names}}'"
  step 05-login-local "docker login localhost:5000 -u student -p not-a-real-token"
  step 06-tag-local "docker tag simple-translate localhost:5000/student/simple-translate-ac215"
  istep 07-push-local "docker push localhost:5000/student/simple-translate-ac215"
  istep 08-push-local-again "docker push localhost:5000/student/simple-translate-ac215"
  step 09-imagetools-local "docker buildx imagetools inspect localhost:5000/student/simple-translate-ac215"
  hub_retry step 10-imagetools-dlops "docker buildx imagetools inspect dlops/simple-translate"
  hub_retry step 11-imagetools-python "docker buildx imagetools inspect python:3.12-slim-bookworm"
  hub_retry step 12-arm64-on-amd64 "docker run --rm --platform linux/arm64 debian:12 uname -m"
  step 13-logout-local "docker logout localhost:5000"
else
  step 00-os "cat /etc/os-release | head -4; uname -m; date -u '+%Y-%m-%d %H:%M UTC'; which docker; echo which-docker-exit:\$?"
  # --- README: Install Docker on the newly created instance (no apt-get update in the README)
  step 01-apt-install-docker "yes | sudo apt install docker.io"
  step 02-apt-update "sudo apt-get update"                 # extra (README.md:44 has it, :210 not)
  step 03-apt-install-docker "yes | sudo apt install docker.io"
  # capture-only: a VM's systemd starts the docker service here; a container has no systemd
  sudo sh -c "nohup dockerd > /var/log/dockerd.log 2>&1 &"
  for i in $(seq 60); do sudo docker info >/dev/null 2>&1 && break; sleep 1; done
  # --- README: Check version of installed Docker
  step 04-docker-version "sudo docker --version"
  step 05-docker-no-sudo "docker ps"                       # extra: why the README uses sudo
  # --- README: Run the app using Docker, then Run the cli (typed at the container's prompt)
  hub_retry istep 06-docker-run "sudo docker run --rm -ti dlops/simple-translate" \
    "$P" "python cli.py" "$P" "python --version" "$P" "exit"
  step 07-images "sudo docker images"                     # extra
  step 08-platform "uname -m; sudo docker image inspect dlops/simple-translate --format '{{.Os}}/{{.Architecture}} created {{.Created}}'"
  step 09-history "sudo docker history dlops/simple-translate"
  step 10-image-files "sudo docker run --rm dlops/simple-translate -c 'wc -c cli.py; grep -n Translator cli.py; ls -l .venv/bin/python; cat .venv/pyvenv.cfg'"
  step 11-ps-a "sudo docker ps -a"
fi
