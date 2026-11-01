#!/bin/bash
# Re-capture the L08 terminal transcripts: dlops-io/llm-finetuning, branch main, the whole README
# (Generate Question Answer Dataset + Fine-tune Gemini).
#   bash assets/terminal/capture.sh
# Writes laptop/ (your laptop's terminal, in ~/AC215/llm-finetuning), dataset-creator/ and gemini-finetuner/ (typed
# at each container's prompt) and capture-only/ (the base image's build log, per-folder timings). Start from empty
# folders: run_steps.sh overwrites the files it writes and removes nothing. The README and Colab outputs in
# expected/ are made separately by expected_outputs.py (no Docker needed).
# Needs Docker with privileged containers, and python3 with `pyte` (pip install pyte; set PYTHON to it) so the live
# views of `docker build` render as a terminal shows them. Behind the recording proxy also export CA_BUNDLE (a PEM
# file with the proxy's CA). The laptop is removed at the end (KEEP=1 keeps it).
#
# "Your laptop" is a fresh, empty Docker Engine standing in for Docker Desktop (as in L05-L07): a docker:29.8.2-dind
# container with its own network namespace (so the fixed names llm-dataset-creator / gemini-finetuner are the
# laptop's and nobody else's), with bash, git, curl and dash, a user `student` (uid 1000) in the docker group, and the
# workspace ~/AC215 where the clone and secrets/ sit side by side (README.md:54-62). run_steps.sh types each command
# into the laptop with `docker exec` (a fresh login shell per command, or a real pseudo-terminal via tty_session.py
# for docker-shell.sh, which runs `docker run -ti`). Nothing from the tutorial repo runs on the recording machine.
#
# Capture-only additions (not part of the tutorial; ASSETS.md describes their visible effects):
#  - Behind an HTTPS-only proxy on the host's 127.0.0.1, proxy_relay.py (container l08-relay) makes the proxy
#    reachable from Docker's bridge network. The laptop's git, Docker engine, image builds and containers use it
#    (the laptop's ~/.docker/config.json "proxies" entry passes it to builds and containers).
#  - python:3.12-slim-bookworm is pulled into the laptop and rebuilt under the same name with the proxy's CA and https
#    apt sources (capture-only/base-python-3.12-slim-bookworm.Dockerfile), so the tutorial's Dockerfiles build
#    unchanged.
#  - The laptop's engine stores its images in an 8 GB tmpfs (the recording disk had about 5 GB free) and pulls Docker
#    Hub images through mirror.gcr.io; the student's home is a 1 GB tmpfs.
#  - There is no service-account key: secrets/ is created next to the clone as README.md:50 says, but stays empty.
#  - capture-only/scripted/cheese_qa_{0..4}.txt (hand-written, labelled "scripted" in ASSETS.md) stand in for the
#    Gemini output that --generate cannot fetch here, so --prepare runs on real files. They are copied to
#    ~/scripted on the laptop, outside the workspace.
set -e
HERE="$(cd "$(dirname "$0")" && pwd)"
RS=$(mktemp); cp "$HERE/run_steps.sh" "$RS"
CA=${CA_BUNDLE:-/etc/ssl/certs/ca-certificates.crt}
NOPX=localhost,127.0.0.1
RELAY=
if [ -n "$HTTPS_PROXY" ]; then
  GW=$(docker network inspect bridge --format '{{(index .IPAM.Config 0).Gateway}}')
  PHOST=${HTTPS_PROXY#*://}; PHOST=${PHOST%/}; PPORT=${PHOST##*:}; PHOST=${PHOST%:*}
  docker rm -f l08-relay >/dev/null 2>&1 || true      # the proxy's port changes when the machine restarts
  docker run -d --name l08-relay --network host -v "$HERE/proxy_relay.py":/proxy_relay.py:ro \
    python:3.12-slim-bookworm python /proxy_relay.py "$GW" 38708 "$PHOST" "$PPORT" >/dev/null
  RELAY=http://$GW:38708
  until (exec 3<>/dev/tcp/$GW/38708) 2>/dev/null; do sleep 0.5; done   # wait until the relay listens
fi
LAPTOP=l08-laptop
export RELAY NOPX CA LAPTOP

# ---- a fresh laptop: empty Docker engine, bash/git/curl/dash, user student, workspace ~/AC215 ----
docker rm -f $LAPTOP >/dev/null 2>&1 || true
docker run -d --privileged --name $LAPTOP --hostname laptop \
  --tmpfs /var/lib/docker:rw,exec,size=8g \
  --tmpfs /home/student:rw,exec,size=1g,mode=0755,uid=1000,gid=1000 \
  -v "$CA":/ca.crt:ro \
  -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY" -e NO_PROXY=$NOPX -e no_proxy=$NOPX \
  --entrypoint sh docker:29.8.2-dind -c '
    cp /ca.crt /etc/ssl/certs/ca-certificates.crt
    mkdir -p /etc/docker
    echo "{\"registry-mirrors\":[\"https://mirror.gcr.io\"],\"features\":{\"containerd-snapshotter\":false}}" > /etc/docker/daemon.json
    exec dockerd-entrypoint.sh dockerd --host=unix:///var/run/docker.sock' >/dev/null
PROXY_JSON=
[ -n "$RELAY" ] && PROXY_JSON="{\"proxies\":{\"default\":{\"httpsProxy\":\"$RELAY\",\"noProxy\":\"$NOPX\"}}}"
docker exec -e PROXY_JSON="$PROXY_JSON" $LAPTOP sh -c '
  set -e
  until docker info >/dev/null 2>&1; do sleep 1; done
  apk add --no-cache -q bash git curl coreutils diffutils grep findutils less ncurses dash >/dev/null
  adduser -D -H -h /home/student -u 1000 -s /bin/bash student && addgroup student docker
  mkdir -p /home/student/.docker /home/student/AC215 /home/student/scripted
  [ -n "$PROXY_JSON" ] && echo "$PROXY_JSON" > /home/student/.docker/config.json
  # the prompt a Linux/macOS terminal shows: user@host:dir$
  printf "%s\n" "export PS1=\"\\u@\\h:\\w\\$ \"" > /home/student/.profile
  chown -R student:student /home/student'
# (docker cp cannot write into the tmpfs home, so the files are streamed in)
for f in "$HERE"/capture-only/scripted/cheese_qa_*.txt; do
  docker exec -i -u student $LAPTOP sh -c "cat > /home/student/scripted/$(basename "$f")" < "$f"
done
# ---- capture-only base image (same name as the tutorial's FROM line) ----
mkdir -p "$HERE/capture-only"
docker exec $LAPTOP docker pull -q python:3.12-slim-bookworm >/dev/null
docker exec $LAPTOP mkdir -p /capture-ctx
docker cp "$CA" $LAPTOP:/capture-ctx/capture-ca.crt >/dev/null
docker cp "$HERE/capture-only/base-python-3.12-slim-bookworm.Dockerfile" $LAPTOP:/capture-ctx/base.Dockerfile >/dev/null
{ echo "\$ docker build -t python:3.12-slim-bookworm -f base-python-3.12-slim-bookworm.Dockerfile ."
  docker exec -w /capture-ctx $LAPTOP docker build --progress=plain -t python:3.12-slim-bookworm -f base.Dockerfile . 2>&1
  echo "[exit $?]"; } > "$HERE/capture-only/base-python-3.12-slim-bookworm-build.txt"
bash "$RS" "$HERE"
if [ -z "$KEEP" ]; then
  docker rm -f $LAPTOP >/dev/null
  docker rm -f l08-relay >/dev/null 2>&1 || true
fi
rm -f "$RS"
