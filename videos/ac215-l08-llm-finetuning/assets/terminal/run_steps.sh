#!/bin/bash
# Types the L08 commands into "your laptop" one at a time and saves each one's output to its own file:
# "$ cmd", the output, "[exit N]". Called by capture.sh, which starts the laptop (container $LAPTOP) and exports
# RELAY/NOPX/CA. Usage:
#   run_steps.sh <terminal_dir>
# Folders written (start from empty folders; files are overwritten, nothing is removed):
#   laptop/            your laptop's terminal, in ~/AC215 (README.md:31-69 Prerequisites; README.md:83 "Make sure you
#                      are inside the dataset-creator folder and open a terminal at this location")
#   dataset-creator/   typed at the llm-dataset-creator container's prompt, app@<id>:/app$ (README.md:90-222)
#   gemini-finetuner/  typed at the gemini-finetuner container's prompt (README.md:243-286)
#   capture-only/<folder>-timings.txt
# The README's commands run in README order, exactly as written. Steps not in the README are marked "extra" in the
# comments and have an "x-" in their file name (ASSETS.md).
# Helpers step / tstep / session_start / session_end / cstep / bplain: L07's run_steps.sh, unchanged except that
# cstep takes the container name as an argument (two containers here).
HERE=$1
L=$LAPTOP
WS=/home/student/AC215
REPO=$WS/llm-finetuning                      # the clone; secrets/ sits next to it (README.md:54-62)
DC=$REPO/dataset-creator
GF=$REPO/gemini-finetuner
PY=${PYTHON:-python3}
SIG=$(mktemp -d)
EXEC_ENV=(-e HOME=/home/student -e USER=student -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY"
          -e NO_PROXY="$NOPX" -e no_proxy="$NOPX")
mkdir -p "$HERE/capture-only"
clean() { sed -r 's/\x1b\[[0-9;?]*[A-Za-z]//g'; }
timing() { printf '%s\t%s UTC\t%ss\n' "$2" "$(date -u +%H:%M:%S)" \
  "$(awk "BEGIN{printf \"%.1f\", $(date +%s.%N) - $3}")" >> "$HERE/capture-only/$1-timings.txt"; }

# step <folder> <name> <dir> <command>: typed in a new terminal on the laptop (a fresh login shell, no terminal
# attached, so progress views print plain lines).
step() {
  local f=$1 name=$2 dir=$3; shift 3; mkdir -p "$HERE/$f"
  local t0; t0=$(date +%s.%N)
  { echo "\$ $*"
    docker exec -u student -w "$dir" "${EXEC_ENV[@]}" $L bash -lc "$*" 2>&1 </dev/null
    echo "[exit $?]"; } | clean > "$HERE/$f/$name.txt"
  timing "$f" "$name" "$t0"
}
# tstep <folder> <name> <dir> <prompt-regex> <script> <command>: the same in a real terminal (pseudo-terminal 80x40,
# tty_session.py): what the terminal shows at the end. <script> = lines typed at the prompts, and directives.
# SHOW (optional) replaces the command on the file's first line.
tstep() {
  local f=$1 name=$2 dir=$3 prx=$4 typed=$5; shift 5; mkdir -p "$HERE/$f"
  local sf; sf=$(mktemp); printf '%s\n' "$typed" > "$sf"
  SHOW_CMD="${SHOW:-$*}" PROMPT_RE="$prx" TIMING_FILE="$HERE/capture-only/$f-timings.txt" \
    TTY_PROMPT_TIMEOUT=3000 "$PY" -I "$HERE/tty_session.py" "$HERE/$f/$name.txt" "$sf" \
    docker exec -ti -u student -w "$dir" "${EXEC_ENV[@]}" $L bash -lc "$*"
  rm -f "$sf"
}
# session_start <folder> <name> <dir> <command>: a terminal that stays open (docker-shell.sh's container shell):
# tstep in the background; it waits at the container's prompt until session_end, which types `exit`. Meanwhile
# run_steps.sh plays "a second terminal" (step) and types at the container's prompt (cstep).
session_start() {
  local f=$1 name=$2 dir=$3; shift 3
  rm -f "$SIG/up" "$SIG/stop"
  local script="@@prompt"$'\n'"@@touch $SIG/up"$'\n'"@@waitfile $SIG/stop"$'\n'"exit"
  tstep "$f" "$name" "$dir" '[$#] $' "$script" "$@" &
  BGPID=$!
  while [ ! -e "$SIG/up" ] && kill -0 $BGPID 2>/dev/null; do sleep 1; done
}
session_end() { touch "$SIG/stop"; wait $BGPID; }
# cstep <container> <folder> <name> <command>: typed at the prompt of the container the open session started.
# Run with `docker exec` into that container (as its user app, in /app, with the container's environment), after
# activating /.venv exactly as docker-entrypoint.sh:12 does, so each command gets its own file and exit status.
# stderr is joined to stdout inside the container (as on a terminal); Python is unbuffered there (Dockerfile:14).
cstep() {
  local ctr=$1 f=$2 name=$3; shift 3; mkdir -p "$HERE/$f"
  local t0; t0=$(date +%s.%N)
  { echo "\$ $*"
    docker exec -u student "${EXEC_ENV[@]}" $L docker exec -w /app $ctr bash -c "source /.venv/bin/activate && { $*"$'\n'"} 2>&1" 2>&1 </dev/null
    echo "[exit $?]"; } | clean > "$HERE/$f/$name.txt"
  timing "$f" "$name" "$t0"
}
# bplain <folder> <name> <since>: the step-by-step log of each docker build that started after <since>, replayed
# from Docker's build history (what `--progress=plain` prints): <name>.plain.txt, <name>.plain.2.txt, ...
bplain() {
  local f=$1 name=$2 since=$3 i=0 r suffix
  for r in $(docker exec $L docker buildx history ls --format json | "$PY" -I -c '
import json, sys
recs = [json.loads(l) for l in sys.stdin if l.strip()]
for d in sorted(recs, key=lambda d: d["created_at"]):
    if d["created_at"][:19] >= sys.argv[1]:
        print(d["ref"].split("/")[-1])' "$since"); do
    i=$((i+1)); suffix=""; [ $i -gt 1 ] && suffix=".$i"
    { echo "\$ docker buildx history logs $r"; docker exec -u student "${EXEC_ENV[@]}" $L docker buildx history logs "$r" 2>&1
      echo "[exit $?]"; } | clean > "$HERE/$f/$name.plain$suffix.txt"
  done
}

# ======================= laptop: Prerequisites (README.md:31-69) =======================
step laptop 00-x-env $WS 'date -u; uname -m; docker version --format "Docker Engine {{.Server.Version}} (client {{.Client.Version}}, API {{.Server.APIVersion}}, {{.Server.Os}}/{{.Server.Arch}})"; git --version; whoami; id -u; pwd'
# extra: README.md:34 links the repo ("Cloned this repository to your local machine") but prints no clone command
step laptop 01-x-clone $WS 'git clone https://github.com/dlops-io/llm-finetuning.git'
step laptop 02-x-git-log $REPO 'git log -1 --format="%h %H%n%cd %s" --date=iso; git branch -a'
step laptop 03-x-ls $REPO 'ls -a; ls -a dataset-creator gemini-finetuner'
step laptop 04-x-env-dev $REPO 'cat env.dev'
# README.md:50 "Create a folder called secrets next to the llm-finetuning repository" (no command given). The key
# (README.md:38-49, GCP Console) cannot be made here: the folder stays empty.
step laptop 05-x-mkdir-secrets $WS 'mkdir secrets'
step laptop 06-x-ls-workspace $WS 'ls -la; ls -la secrets'

# ======================= Generate Question Answer Dataset: Run Container (README.md:79-94) =======================
# README.md:83 "Make sure you are inside the dataset-creator folder"; README.md:87 `sh docker-shell.sh`
T0=$(date -u +%Y-%m-%dT%H:%M:%S)
session_start laptop 07-docker-shell-dataset-creator $DC 'sh docker-shell.sh'
# ----- a second terminal on the laptop, while the container runs (extras) -----
step laptop 08-x-docker-ps $DC 'docker ps'
step laptop 09-x-docker-images $DC 'docker images'
step laptop 10-x-mounts $DC "docker inspect llm-dataset-creator --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'; docker inspect llm-dataset-creator --format '{{range .Config.Env}}{{println .}}{{end}}' | grep -E '^(GCP_PROJECT|GCS_BUCKET_NAME|GOOGLE_APPLICATION_CREDENTIALS)='; docker inspect llm-dataset-creator --format 'ports: {{json .NetworkSettings.Ports}}  user: {{.Config.User}}  workdir: {{.Config.WorkingDir}}'"
bplain laptop 07-docker-shell-dataset-creator "$T0"
# extra (digest §6.11): a second `sh docker-shell.sh` while the first container runs -> name conflict
tstep laptop 11-x-docker-shell-again $DC '[$#] $' '' 'sh docker-shell.sh'
# extra (digest §6.11): a second shell with docker exec skips docker-entrypoint.sh, so the venv is not active
step laptop 12-x-exec-no-venv $DC "docker exec llm-dataset-creator bash -c 'which python; python -c \"import pandas\"'"

# ----- typed at the llm-dataset-creator container's prompt -----
step_d() { cstep llm-dataset-creator dataset-creator "$@"; }
step_d 00-x-whoami 'whoami; id; pwd; which python; python --version; uv --version; echo "VIRTUAL_ENV=$VIRTUAL_ENV"; echo "GCP_PROJECT=$GCP_PROJECT"; echo "GCS_BUCKET_NAME=$GCS_BUCKET_NAME"; echo "GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS"'
step_d 01-ls-secrets 'ls -la /secrets'                                                 # README.md:69 (tip)
step_d 02-x-packages 'uv pip list 2>/dev/null | grep -E "^(google-genai|google-cloud-storage|google-auth|pandas|scikit-learn|chromadb|langchain|langchain-community|openai|openai-agents|onnxruntime) "; echo "packages in /.venv: $(uv pip list 2>/dev/null | tail -n +3 | wc -l)"; du -sh /.venv'
step_d 03-x-ls-app 'ls -la /app'
step_d 04-help 'python cli.py --help'                                                    # README.md:93
step_d 05-generate 'python cli.py --generate'                                            # README.md:103 (no key)
step_d 06-x-ls-data 'ls -la data'
step_d 07-prepare-no-data 'python cli.py --prepare'                                      # README.md:184, right after 05
# extra: the scripted stand-in for Gemini's answers (capture-only/scripted), copied on the laptop into the
# bind-mounted folder, as the generator would have written them (data/cheese_qa_{0..4}.txt, cli.py:196)
step laptop 13-x-scripted-data $DC 'cp ~/scripted/cheese_qa_*.txt data/; ls -la data'
step_d 08-x-ls-data-scripted 'ls -la data; head -c 400 data/cheese_qa_0.txt; echo'
step_d 09-prepare 'python cli.py --prepare'                                              # README.md:184 (scripted data)
step_d 10-x-ls-data-after 'ls -la data; wc -l data/*.jsonl data/*.csv'
step_d 11-x-train-jsonl-head 'head -c 400 data/train.jsonl; echo'
step_d 12-x-jsonl-pretty 'head -1 data/train.jsonl | python -m json.tool'
step_d 13-x-csv-head 'head -4 data/train.csv; echo ...; head -3 data/instruct-dataset.csv'
step_d 14-upload 'python cli.py --upload'                                                # README.md:221 (no key)
session_end                                                                              # `exit`: removed (--rm)

# ======================= laptop: after exit (extras) =======================
step laptop 14-x-ps-after-exit $DC 'docker ps -a'
step laptop 15-x-data-on-host $DC 'ls -la data; git -C .. status --short --ignored'
step laptop 16-x-diff-folders $REPO 'diff dataset-creator/uv.lock gemini-finetuner/uv.lock && echo "uv.lock: identical"; diff dataset-creator/pyproject.toml gemini-finetuner/pyproject.toml && echo "pyproject.toml: identical"; diff dataset-creator/Dockerfile gemini-finetuner/Dockerfile && echo "Dockerfile: identical"; diff dataset-creator/docker-shell.sh gemini-finetuner/docker-shell.sh'

# ======================= Fine-tune Gemini: Run Container (README.md:232-247) =======================
# README.md:236 "Make sure you are inside the gemini-finetuner folder"; README.md:240 `sh docker-shell.sh`
step laptop 17-x-cd-gemini-finetuner $DC 'cd ../gemini-finetuner && pwd && ls'
T1=$(date -u +%Y-%m-%dT%H:%M:%S)
session_start laptop 18-docker-shell-gemini-finetuner $GF 'sh docker-shell.sh'
step laptop 19-x-docker-images $GF 'docker images'
bplain laptop 18-docker-shell-gemini-finetuner "$T1"

step_g() { cstep gemini-finetuner gemini-finetuner "$@"; }
step_g 00-x-whoami 'whoami; pwd; which python; python --version; echo "GCP_PROJECT=$GCP_PROJECT"; echo "GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS"; ls -la /secrets'
step_g 01-help 'python cli.py --help'                                                    # README.md:246
step_g 02-train 'python cli.py --train'                                                  # README.md:256 (no key)
step_g 03-chat 'python cli.py --chat'                                                    # README.md:285 (no key)
step_g 04-x-dataset-uris "grep -n 'gs://' cli.py"
session_end

# ======================= laptop: gotchas and teardown (extras) =======================
step laptop 20-x-dash $DC 'dash docker-shell.sh'                     # digest §6.1: /bin/sh on Debian/Ubuntu is dash
step laptop 21-x-wrong-folder $REPO 'sh dataset-creator/docker-shell.sh'                # digest §6.2
step laptop 22-x-image-rm $REPO 'docker image rm llm-dataset-creator gemini-finetuner'
rm -f "$SIG/up" "$SIG/stop"; rmdir "$SIG"
