#!/bin/bash
# Types the L04 README commands into "your laptop" one at a time and saves each one's output to its own file:
# "$ cmd", the output, "[exit N]". Called by capture.sh, which starts the laptop (container $LAPTOP, a fresh
# Docker engine) and exports RELAY/NOPX. Usage:
#   run_steps.sh <terminal_dir> <part>       part = port | mega | gcloud
# Folders written (each is emptied first):
#   port:   port-laptop/
#   mega:   mega-laptop/, mega-l03-laptop/, mega-transcribe_audio/, mega-generate_text/, mega-synthesis_audio_en/,
#           mega-translate_text/, mega-synthesis_audio/
#   gcloud: gcloud-laptop/
#   and capture-only/<folder>-timings.txt.
# Steps not in the README are marked "extra" in the comments and have an "x-" in their file name (ASSETS.md).
HERE=$1; PART=$2
L=${LAPTOP:-l04-laptop}
WS=/home/student/AC215                      # README: <your-workspace>
PY=${PYTHON:-python3}
SIG=$(mktemp -d)
EXEC_ENV=(-e HOME=/home/student -e USER=student -e HTTPS_PROXY="$RELAY" -e https_proxy="$RELAY"
          -e NO_PROXY="$NOPX" -e no_proxy="$NOPX")
mkdir -p "$HERE/capture-only"
clean() { sed -r 's/\x1b\[[0-9;?]*[A-Za-z]//g'; }
now() { date -u +%Y-%m-%dT%H:%M:%S; }
wdir() { case $1 in /*) echo "$1";; *) echo "$WS/$1";; esac; }   # <dir>: under ~/AC215 unless absolute
timing() { printf '%s\t%s UTC\t%ss\n' "$2" "$(date -u +%H:%M:%S)" \
  "$(awk "BEGIN{printf \"%.1f\", $(date +%s.%N) - $3}")" >> "$HERE/capture-only/$1-timings.txt"; }
fresh() { local f; for f in "$@"; do rm -rf "${HERE:?}/$f" "$HERE/capture-only/$f-timings.txt"; mkdir -p "$HERE/$f"; done; }

# step <folder> <name> <dir> <command>: typed in a new terminal on the laptop (a fresh login shell, no terminal
# attached, so Docker prints plain progress).
step() {
  local f=$1 name=$2 dir=$3; shift 3; mkdir -p "$HERE/$f"
  local t0; t0=$(date +%s.%N)
  { echo "\$ $*"
    docker exec -u student -w "$(wdir "$dir")" "${EXEC_ENV[@]}" $L bash -lc "$*" 2>&1 </dev/null
    echo "[exit $?]"; } | clean > "$HERE/$f/$name.txt"
  timing "$f" "$name" "$t0"
}
# tstep <folder> <name> <dir> <script> <command>: the same in a real terminal (pseudo-terminal 80x40,
# tty_session.py): what the terminal shows at the end. <script> = lines typed at the prompts, and directives.
tstep() {
  local f=$1 name=$2 dir=$3 typed=$4; shift 4; mkdir -p "$HERE/$f"
  local sf; sf=$(mktemp); printf '%s\n' "$typed" > "$sf"
  SHOW_CMD="$*" TIMING_FILE="$HERE/capture-only/$f-timings.txt" "$PY" -I "$HERE/tty_session.py" "$HERE/$f/$name.txt" "$sf" \
    docker exec -ti -u student -w "$(wdir "$dir")" "${EXEC_ENV[@]}" $L bash -lc "$*"
  rm -f "$sf"
}
# session_start <folder> <name> <dir> <typed lines> <command>: a terminal that stays open. tstep in the background:
# the typed lines (may be empty) go in at its prompts, then it waits at the next prompt until session_end, which
# types `exit`. Meanwhile run_steps.sh plays "a second terminal" (step / cstep).
session_start() {
  local f=$1 name=$2 dir=$3 typed=$4; shift 4
  rm -f "$SIG/up" "$SIG/stop"
  local script=""
  [ -n "$typed" ] && script="$typed"$'\n'
  script+="@@prompt"$'\n'"@@touch $SIG/up"$'\n'"@@waitfile $SIG/stop"$'\n'"exit"
  tstep "$f" "$name" "$dir" "$script" "$@" &
  BGPID=$!
  while [ ! -e "$SIG/up" ] && kill -0 $BGPID 2>/dev/null; do sleep 1; done
}
session_end() { touch "$SIG/stop"; wait $BGPID; }
# bg_tstep <folder> <name> <dir> <script> <command>: tstep in the background for a command that keeps running
# (docker compose up, docker compose logs -f). <script> must "@@touch $SIG/up" when ready and "@@waitfile
# $SIG/stop" before it stops the command. bg_end lets it stop and waits.
bg_tstep() {
  rm -f "$SIG/up" "$SIG/stop"
  tstep "$@" &
  BGPID=$!
  while [ ! -e "$SIG/up" ] && kill -0 $BGPID 2>/dev/null; do sleep 1; done
}
bg_end() { touch "$SIG/stop"; wait $BGPID; }
# cstep <folder> <name> <container> <command>: typed at the prompt of the container a running session started.
# Run with `docker exec` into that container, in /app as user app, after sourcing the venv exactly as the image's
# CMD does (Dockerfile:44-46), so each command gets its own file and exit status.
cstep() {
  local f=$1 name=$2 c=$3; shift 3; mkdir -p "$HERE/$f"
  local t0; t0=$(date +%s.%N)
  { echo "\$ $*"
    docker exec -u student "${EXEC_ENV[@]}" $L docker exec -w /app "$c" bash -c "source /home/app/.venv/bin/activate && $*" 2>&1 </dev/null
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
# as_root / as_student <command>: a capture-only action on the laptop (not typed by the student, not recorded).
as_root() { docker exec $L sh -c "$*"; }
as_student() { docker exec -u student -w "$WS" "${EXEC_ENV[@]}" $L bash -lc "$*"; }
# wait_log <container> <text>: capture-only, wait (max 20 s) until the container's log shows <text>, so that the
# next request does not race the server's start (a person clicks Send a few seconds later).
wait_log() { docker exec $L sh -c "for i in \$(seq 100); do docker logs $1 2>&1 | grep -q '$2' && exit 0; sleep 0.2; done; exit 1" || true; }

case $PART in
port)  # ===================== dlops-io/port_toy, README.md (whole) =====================
  F=port-laptop; P=port_toy
  fresh $F
  step $F 00-env "" "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}} (API {{.Server.APIVersion}}, {{.Server.Os}}/{{.Server.Arch}})'; docker compose version; docker buildx version; git --version; curl --version | head -1"   # extra
  # Prerequisites (README.md:26-30)
  tstep $F 01-hello-world "" "" "docker run hello-world"
  # Step 1: Get the code (README.md:79-85). The README says "Clone or download"; the clone command is extra.
  step $F 02-clone "" "git clone https://github.com/dlops-io/port_toy.git"
  step $F 03-cd "" "cd port_toy"
  step $F 04-ls $P "ls -a; ls gateway processor; git log --oneline -1"                                   # extra
  # Create the network (README.md:89-93), build the images (97-102)
  step $F 05-network-create $P "docker network create toynet"
  step $F 06-network-ls $P "docker network ls"                                                            # extra
  s=$(now); tstep $F 07-build-processor $P "" "docker build -t toy-processor ./processor"; bplain $F 07-build-processor "$s"
  s=$(now); tstep $F 08-build-gateway $P "" "docker build -t toy-gateway ./gateway"; bplain $F 08-build-gateway "$s"
  step $F 09-images $P "docker image ls 'toy-*'"                                                           # extra
  # Start the processor (106-111) and the gateway (117-125), check the logs (129-134)
  step $F 10-run-processor $P $'docker run -d --name processor --network toynet \\\n  -e PORT=9200 toy-processor'
  step $F 11-run-gateway $P $'docker run -d --name gateway --network toynet \\\n  -p 127.0.0.1:8090:9100 \\\n  -e PROCESSOR_HOST=processor \\\n  -e PROCESSOR_PORT=9200 \\\n  toy-gateway'
  wait_log processor listening; wait_log gateway listening
  step $F 12-logs-processor $P "docker logs processor"
  step $F 13-logs-gateway $P "docker logs gateway"
  # Send a message (145-157): the page's request (index.html:95-99: POST / with {"text": ...}), sent with curl.
  # extra (browser stand-in). -sS: quiet, but show an error; -w '\n': end the JSON line.
  SEND8090="curl -sS -X POST http://localhost:8090 -H 'Content-Type: application/json' -d '{\"text\": \"hello from the laptop\"}' -w '\n'"
  SEND8095="curl -sS -X POST http://localhost:8095 -H 'Content-Type: application/json' -d '{\"text\": \"hello from the laptop\"}' -w '\n'"
  step $F 14-send $P "$SEND8090"
  step $F 15-send-again $P "$SEND8090"
  # Step 2: Read the PORTS column (193-207)
  step $F 16-ps $P "docker ps"
  step $F 17-ps-short $P "docker ps --format 'table {{.Image}}\t{{.Ports}}\t{{.Names}}'"                    # extra
  # extra: "If you omit it: -p 8090:9100" (236-242) and "port is already allocated" (cheat sheet 550)
  step $F 18-x-all-addresses-taken $P "docker run -d --name gateway-all --network toynet -p 8090:9100 toy-gateway"
  step $F 19-x-rm-created $P "docker rm gateway-all"
  step $F 20-x-all-addresses $P "docker run -d --name gateway-all --network toynet -p 8091:9100 toy-gateway"
  step $F 21-x-ps-all-addresses $P "docker ps --format 'table {{.Image}}\t{{.Ports}}\t{{.Names}}'; docker rm -f gateway-all"
  # Test from your laptop (246-264), from inside the gateway (266-292). In a terminal: curl prints no progress
  # meter when its output is the terminal (22); `docker exec` without -t gives curl a pipe, so it does (24, 25).
  tstep $F 22-curl-8090 $P "" "curl http://localhost:8090"
  step $F 23-curl-9200 $P "curl --max-time 3 http://localhost:9200/health"
  tstep $F 24-exec-processor $P "" "docker exec gateway curl http://processor:9200/health"
  tstep $F 25-exec-localhost $P "" "docker exec gateway curl --max-time 3 http://localhost:9200/health"
  # extras: whose localhost; the network's phone book (Handy commands: docker network inspect toynet)
  step $F 26-x-exec-localhost-9100 $P "docker exec gateway curl -s http://localhost:9100 | head -4"
  step $F 27-x-processor-has-curl $P "docker exec processor curl --version | head -1"
  step $F 28-network-inspect $P "docker network inspect toynet"
  step $F 29-x-dns $P "docker exec gateway cat /etc/resolv.conf; docker exec gateway getent hosts processor gateway"
  # Handy commands (566): a shell inside the gateway; typed there: hostname, ls, exit
  tstep $F 29b-exec-it-sh $P $'hostname\nls\nexit' "docker exec -it gateway sh"
  # Step 3: Change the host port (335-355)
  step $F 30-rm-gateway $P "docker rm -f gateway"
  step $F 31-run-gateway-8095 $P $'docker run -d --name gateway --network toynet \\\n  -p 127.0.0.1:8095:9100 \\\n  -e PROCESSOR_HOST=processor \\\n  -e PROCESSOR_PORT=9200 \\\n  toy-gateway'
  wait_log gateway listening
  step $F 32-send-8095 $P "$SEND8095"                                                                       # browser stand-in
  step $F 33-curl-8090-gone $P "curl --max-time 3 http://localhost:8090"                                    # extra (README 355)
  step $F 34-logs-gateway-8095 $P "docker logs gateway"                                                     # extra (E15)
  step $F 35-ps-8095 $P "docker ps --format 'table {{.Image}}\t{{.Ports}}\t{{.Names}}'"                    # extra
  # Change the processor's port (365-382)
  step $F 36-rm-processor $P "docker rm -f processor"
  step $F 37-run-processor-9300 $P $'docker run -d --name processor --network toynet \\\n  -e PORT=9300 toy-processor'
  wait_log processor listening
  step $F 38-send-fails $P "$SEND8095"                                                                      # browser stand-in
  step $F 39-logs-gateway-refused $P "docker logs gateway"                                                  # extra (E16)
  step $F 40-logs-processor-9300 $P "docker logs processor"                                                 # extra
  # Update the gateway (384-409)
  step $F 41-rm-gateway $P "docker rm -f gateway"
  step $F 42-run-gateway-9300 $P $'docker run -d --name gateway --network toynet \\\n  -p 127.0.0.1:8090:9100 \\\n  -e PROCESSOR_HOST=processor \\\n  -e PROCESSOR_PORT=9300 \\\n  toy-gateway'
  wait_log gateway listening
  step $F 43-send-9300 $P "$SEND8090"                                                                       # browser stand-in
  # Clean up before Compose (411-420)
  step $F 44-rm-both $P "docker rm -f gateway processor"
  step $F 45-network-rm $P "docker network rm toynet"
  step $F 46-x-after-cleanup $P "docker ps -a; docker network ls"                                          # extra
  # Step 4: Start the app (450-460) in one terminal; the other commands in a second terminal while it runs
  bg_tstep $F 47-compose-up $P "$(printf '%s\n' '@@wait (?s)(processor listening.*gateway listening|gateway listening.*processor listening)' \
      "@@touch $SIG/up" "@@waitfile $SIG/stop" '@@ctrl-c')" "docker compose up"
  sleep 1
  step $F 48-compose-ps $P "docker compose ps"                                                              # README 480
  step $F 49-send-compose $P "$SEND8090"                                                                    # browser stand-in
  step $F 50-network-ls-compose $P "docker network ls"                                                      # extra
  tstep $F 51-compose-exec $P "" "docker compose exec gateway curl http://processor:9200/health"            # README 481
  bg_end                                  # press Ctrl+C in the first terminal (README 505-507)
  step $F 52-compose-ps-a-stopped $P "docker compose ps -a"                                                 # README 521-525
  tstep $F 53-compose-down $P "" "docker compose down"                                                      # README 509-515
  step $F 54-compose-ps-a-after $P "docker compose ps -a"
  # "After changing a setting, run: docker compose up -d" (487-495)
  tstep $F 55-compose-up-d $P "" "docker compose up -d"
  wait_log gateway listening
  step $F 56-compose-ps-d $P "docker compose ps"                                                            # extra
  # Handy commands (572-573): follow the gateway's log while a message is sent, then Ctrl+C; a shell in the gateway
  bg_tstep $F 56b-compose-logs-f $P "$(printf '%s\n' '@@wait gateway listening' "@@touch $SIG/up" "@@waitfile $SIG/stop" \
      '@@sleep 1' '@@ctrl-c')" "docker compose logs -f gateway"
  step $F 56c-x-send-while-logs $P "$SEND8090"                                                              # browser stand-in
  bg_end
  tstep $F 56d-compose-exec-sh $P $'hostname\necho $PROCESSOR_HOST $PROCESSOR_PORT\nexit' "docker compose exec gateway sh"
  as_student "cd port_toy && sed -i 's|\"127.0.0.1:8090:9100\"|\"127.0.0.1:8095:9100\"|' docker-compose.yml"   # the edit (capture-only sed)
  step $F 57-x-edit-port $P "git diff"                                                                      # extra
  tstep $F 58-compose-up-d-changed $P "" "docker compose up -d"
  wait_log gateway listening
  step $F 59-x-send-8095-compose $P "$SEND8095"                                                             # browser stand-in
  as_student "cd port_toy && git checkout -q docker-compose.yml"
  tstep $F 60-compose-up-d-restored $P "" "docker compose up -d"
  wait_log gateway listening
  # "If you change a Dockerfile or something copied into an image during its build" (497-501)
  as_student "cd port_toy && printf '\n# edited\n' >> processor/processor.py"
  step $F 61-x-edit-processor $P "git diff"                                                                 # extra
  s=$(now); tstep $F 62-compose-up-d-build $P "" "docker compose up -d --build"; bplain $F 62-compose-up-d-build "$s"
  as_student "cd port_toy && git checkout -q processor/processor.py"
  wait_log processor listening; wait_log gateway listening
  step $F 63-x-compose-logs $P "docker compose logs"                                                        # extra (Handy: logs)
  # Stop and remove the app (505-529), this time while it runs in the background
  tstep $F 64-compose-down-running $P "" "docker compose down"
  step $F 65-compose-ps-a-empty $P "docker compose ps -a"
  step $F 66-x-images-remain $P "docker image ls"                                                           # extra (README 515)
  # extra, gotcha G11: Compose right after the by-hand steps, without "Clean up before Compose"
  step $F 67-x-g11-by-hand $P $'docker network create toynet\ndocker run -d --name processor --network toynet \\\n  -e PORT=9200 toy-processor'
  tstep $F 68-x-g11-compose-up $P "" "docker compose up -d"
  step $F 69-x-g11-cleanup $P $'docker rm -f gateway processor\ndocker network rm toynet'
  tstep $F 69b-x-g11-compose-up-net $P "" "docker network create toynet; docker compose up -d"
  tstep $F 69c-x-g11-cleanup $P "" "docker compose down; docker network rm toynet; docker network ls"
  # extra, Exercise 3: the processor started without --network (cheat sheet: could not resolve host)
  step $F 70-x-ex3-no-network $P $'docker network create toynet\ndocker run -d --name processor -e PORT=9200 toy-processor\ndocker run -d --name gateway --network toynet \\\n  -p 127.0.0.1:8090:9100 \\\n  -e PROCESSOR_HOST=processor \\\n  -e PROCESSOR_PORT=9200 \\\n  toy-gateway'
  wait_log processor listening; wait_log gateway listening
  tstep $F 71-x-ex3-resolve $P "" "docker exec gateway curl --max-time 3 http://processor:9200/health"
  step $F 72-x-ex3-send $P "$SEND8090"
  step $F 73-x-ex3-logs $P "docker logs gateway"
  step $F 74-x-ex3-cleanup $P $'docker rm -f gateway processor\ndocker network rm toynet'
  ;;

mega)  # ======= dlops-io/mega-pipeline, branch flexible-workflow: README.md and the five component READMEs =======
  F=mega-laptop; M=mega-pipeline
  fresh $F mega-l03-laptop mega-transcribe_audio mega-generate_text mega-synthesis_audio_en mega-translate_text mega-synthesis_audio
  step $F 00-env "" "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}} (API {{.Server.APIVersion}}, {{.Server.Os}}/{{.Server.Arch}})'; docker buildx version; git --version"   # extra
  # Get the Code, "Starting fresh?" (README.md:32-37)
  step $F 01-clone "" "git clone --branch flexible-workflow https://github.com/dlops-io/mega-pipeline.git"
  step $F 02-cd "" "cd mega-pipeline"
  step $F 03-x-branch $M "git branch; git log --oneline -1"                                              # extra
  step $F 04-x-ls $M "ls; ls -a transcribe_audio"                                                         # extra
  step $F 05-x-modes $M "ls -l */docker-shell.sh; git ls-files -s '*/docker-shell.sh'"                    # extra (E12)
  # Recommended folder layout (README.md:105-119): secrets/ one level above the repo. The key itself cannot exist
  # here (no GCP account): the folder stays empty.
  step $F 06-x-secrets-folder "" "mkdir secrets; ls; ls -la secrets"                                      # extra
  step $F 07-x-cli-values $M "grep -n -E '^(gcp_project|bucket_name|group_name) *=' */cli.py"             # extra (E2/E4)
  # "Configure each cli.py" (README.md:123-134; component READMEs "2. Edit cli.py"): placeholder values, set by a
  # capture-only sed and shown with git diff. your-project-id / your-team-bucket are placeholders, not real ids.
  SEDX='s/^gcp_project = "[^"]*"/gcp_project = "your-project-id"/; s/^bucket_name = "[^"]*"/bucket_name = "your-team-bucket"/; s/^group_name = "[^"]*"/group_name = "group-01"/'
  setvals() { as_student "cd $M/$1 && sed -i -E '$SEDX' cli.py"; }

  # ---- Task A: transcribe_audio (README.md:207-240, transcribe_audio/README.md) ----
  A=$M/transcribe_audio; CA=mega-pipeline-transcribe-audio; FA=mega-transcribe_audio
  step $F 10-a-x-ls-l $A "ls -la"                                                                         # extra
  setvals transcribe_audio
  step $F 11-a-x-edit-cli $A "git diff cli.py"                                                            # extra
  s=$(now); session_start $F 12-a-docker-shell $A "python cli.py --help" "./docker-shell.sh"              # README.md:212
  bplain $F 12-a-docker-shell "$s"
  cstep $FA 01-help $CA "python cli.py --help"                                                    # transcribe_audio/README.md:98
  cstep $FA 02-x-whoami $CA "whoami; id"
  cstep $FA 03-x-which-python $CA "which python"
  cstep $FA 04-x-python-version $CA "python --version"
  cstep $FA 05-x-credentials-env $CA 'echo $GOOGLE_APPLICATION_CREDENTIALS'
  cstep $FA 06-x-ls-secrets $CA "ls -la /secrets"
  cstep $FA 07-x-ls-app $CA "pwd; ls -la"
  cstep $FA 08-x-venv $CA 'echo $VIRTUAL_ENV; ls /home/app/.venv; uv --version'
  cstep $FA 09-download $CA "python cli.py --download"                                            # README.md:237
  cstep $FA 10-transcribe $CA "python cli.py --transcribe"                                        # README.md:238
  cstep $FA 11-upload $CA "python cli.py --upload"                                                # README.md:239
  cstep $FA 12-x-ls-after $CA "ls -la . text_prompts"
  step $F 13-a-x-docker-ps $A "docker ps"                                                                 # extra
  step $F 14-a-x-mounts $A "docker inspect --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}' mega-pipeline-transcribe-audio"
  s=$(now); tstep $F 15-a-x-g9-second-shell $A "" "./docker-shell.sh"; bplain $F 15-a-x-g9-second-shell "$s"   # extra, G9
  session_end
  step $F 16-a-x-host-after $A "ls; git status --short --ignored ."                                      # extra
  s=$(now); tstep $F 17-a-dev $A "" "./docker-shell.sh dev"; bplain $F 17-a-dev "$s"                      # README.md:213
  TTY_PROMPT_TIMEOUT=120 tstep $F 18-a-run-local $A "exit" "./docker-shell.sh run"                         # README.md:214
  step $F 19-a-x-ls-l-script $A "ls -l docker-shell.sh"                                                   # extra (E12)
  step $F 20-a-chmod $A "chmod +x docker-shell.sh"                                                        # README.md:223
  step $F 21-a-x-images $A "docker images"                                                                # extra

  # ---- Task B: generate_text (README.md:244-248, generate_text/README.md) ----
  B=$M/generate_text; CB=mega-pipeline-generate-text; FB=mega-generate_text
  setvals generate_text
  step $F 30-b-x-edit-cli $B "git diff cli.py"                                                            # extra
  s=$(now); session_start $F 31-b-docker-shell $B "python cli.py --help" "./docker-shell.sh"
  bplain $F 31-b-docker-shell "$s"
  cstep $FB 01-help $CB "python cli.py --help"                                                    # generate_text/README.md:114
  cstep $FB 02-download $CB "python cli.py --download"                                            # README.md:245
  cstep $FB 03-generate $CB "python cli.py --generate"                                            # README.md:246
  cstep $FB 04-upload $CB "python cli.py --upload"                                                # README.md:247
  cstep $FB 05-gemini-model $CB $'export GEMINI_MODEL=gemini-2.5-flash\npython cli.py --generate'  # generate_text/README.md:91-94
  cstep $FB 06-x-python-version $CB "python --version; ls -la text_prompts/group-01 text_paragraphs/group-01"
  session_end

  # ---- Task C: synthesis_audio_en (README.md:252-255). Extra: cli.py not edited yet (G2), edited while it runs ----
  C=$M/synthesis_audio_en; CC=mega-pipeline-synthesis-audio-en; FC=mega-synthesis_audio_en
  s=$(now); session_start $F 40-c-docker-shell $C "python cli.py --help" "./docker-shell.sh"
  bplain $F 40-c-docker-shell "$s"
  cstep $FC 01-x-help-unedited $CC "python cli.py --help"                                         # extra, G2
  setvals synthesis_audio_en
  step $F 41-c-x-edit-cli $C "git diff cli.py"                                                            # extra
  cstep $FC 02-help $CC "python cli.py --help"                                                    # synthesis_audio_en/README.md:114
  cstep $FC 03-download $CC "python cli.py --download"                                            # README.md:253
  cstep $FC 04-synthesis $CC "python cli.py --synthesis"                                          # README.md:254
  session_end

  # ---- Task D: translate_text (README.md:261-265) ----
  D=$M/translate_text; CD=mega-pipeline-translate-text; FD=mega-translate_text
  setvals translate_text
  step $F 50-d-x-edit-cli $D "git diff cli.py"                                                            # extra
  s=$(now); session_start $F 51-d-docker-shell $D "python cli.py --help" "./docker-shell.sh"
  bplain $F 51-d-docker-shell "$s"
  cstep $FD 01-help $CD "python cli.py --help"                                                    # translate_text/README.md:114
  cstep $FD 02-download $CD "python cli.py --download"                                            # README.md:262
  cstep $FD 03-translate $CD "python cli.py --translate"                                          # README.md:263
  cstep $FD 04-upload $CD "python cli.py --upload"                                                # README.md:264
  session_end

  # ---- Task E: synthesis_audio (README.md:269-272) ----
  E=$M/synthesis_audio; CE=mega-pipeline-synthesis-audio; FE=mega-synthesis_audio
  setvals synthesis_audio
  step $F 60-e-x-edit-cli $E "git diff cli.py"                                                            # extra
  s=$(now); session_start $F 61-e-docker-shell $E "python cli.py --help" "./docker-shell.sh"
  bplain $F 61-e-docker-shell "$s"
  cstep $FE 01-help $CE "python cli.py --help"                                                    # synthesis_audio/README.md:99
  cstep $FE 02-download $CE "python cli.py --download"                                            # README.md:270
  cstep $FE 03-synthesis $CE "python cli.py --synthesis"                                          # README.md:271
  cstep $FE 04-x-cli11-help $CE "python cli_11.py --help"                                         # extra, E10
  session_end

  # ---- "run from a prebuilt image (falls back to DockerHub)" on a laptop without the local image (E1, G7) ----
  step $F 70-x-images $A "docker images"                                                                  # extra
  step $F 71-x-rm-local-image $A "docker image rm mega-pipeline-transcribe-audio"                         # extra
  TTY_PROMPT_TIMEOUT=420 TTY_END_TIMEOUT=120 tstep $F 72-run-registry $A \
    $'python --version\nwhich python\npython cli.py --help\nexit' "./docker-shell.sh run"                 # README.md:214
  as_root "docker rm -f $CA >/dev/null 2>&1 || true"
  step $F 73-x-host-after-registry $A "ls -la; git status --short"                                        # extra
  step $F 74-x-registry-image $A "docker image ls dlops/mega-pipeline-transcribe-audio; docker image inspect --format 'created {{.Created}}{{println}}env {{json .Config.Env}}{{println}}cmd {{json .Config.Cmd}}{{println}}user \"{{.Config.User}}\"' dlops/mega-pipeline-transcribe-audio"
  step $F 75-x-rm-local-image-b $B "docker image rm mega-pipeline-generate-text"                          # extra
  TTY_PROMPT_TIMEOUT=420 TTY_END_TIMEOUT=120 tstep $F 76-run-registry-b $B \
    $'python --version\npython cli.py --help\nexit' "./docker-shell.sh run"                               # README.md:214
  as_root "docker rm -f $CB >/dev/null 2>&1 || true"
  step $F 77-x-host-after-registry-b $B "ls -la; git status --short"                                      # extra
  step $F 78-x-images-all "" "docker images"                                                              # extra
  step $F 79-x-git-status-all $M "git status --short --ignored"                                           # extra

  # ===== Get the Code, "Already have the repo from the last tutorial?" (README.md:39-48), on a laptop that did L03 =====
  # A second workspace, ~/AC215-l03, holds L03's clone (branch main) with the files a student made in L03.
  F=mega-l03-laptop; W3=/home/student/AC215-l03; R3=$W3/mega-pipeline
  as_student "mkdir -p $W3"
  step $F 00-x-l03-clone $W3 "git clone https://github.com/dlops-io/mega-pipeline.git"                    # L03 README's clone
  # capture-only: L03 leftovers (ASSETS.md): the Dockerfile/pyproject.toml a student wrote in transcribe_audio and the
  # Dockerfile in generate_text (L03's captured versions), uv.lock stand-ins, the group-name edit, and a PLACEHOLDER
  # key file where L03 put the key (not a credential).
  L3F=$HERE/../../../ac215-l03-mega-pipeline/assets/terminal/files
  docker cp "$L3F/transcribe_audio.Dockerfile" $L:$R3/transcribe_audio/Dockerfile
  docker cp "$L3F/transcribe_audio.pyproject.toml" $L:$R3/transcribe_audio/pyproject.toml
  docker cp "$L3F/generate_text.Dockerfile" $L:$R3/generate_text/Dockerfile
  as_root "cd $R3 && printf '# placeholder for the uv.lock that L03 wrote (capture-only)\n' | tee transcribe_audio/uv.lock generate_text/uv.lock >/dev/null \
    && printf '{\"placeholder\": \"stands in for the L03 key in this capture; not a credential\"}\n' > transcribe_audio/secrets/mega-pipeline.json \
    && sed -i 's/^group_name = \"pavlos\"/group_name = \"group-01\"/' transcribe_audio/cli.py && chown -R student:student $W3"
  step $F 01-x-l03-state $R3 "git status --short; git status --short --ignored | grep '^!!'; head -1 transcribe_audio/Dockerfile"   # extra
  step $F 02-cd $W3 "cd mega-pipeline"
  step $F 03-fetch $R3 "git fetch origin"
  step $F 04-checkout $R3 "git checkout flexible-workflow"
  step $F 05-stash $R3 "git stash"                                                                        # README.md:48
  step $F 06-checkout-after-stash $R3 "git checkout flexible-workflow"
  step $F 07-x-stash-u $R3 "git stash -u"                                                                 # extra (G1 fix)
  step $F 08-checkout-ok $R3 "git checkout flexible-workflow"
  step $F 09-branch $R3 "git branch"
  step $F 10-x-after $R3 "git status --short --ignored; ls -la transcribe_audio transcribe_audio/secrets; git stash list"
  step $F 11-x-dockerfile-replaced $R3 "head -2 transcribe_audio/Dockerfile; ls transcribe_audio/secrets"   # extra (G1, G6)
  s=$(now); tstep $F 12-x-dev-old-key $R3/transcribe_audio "" "./docker-shell.sh dev"; bplain $F 12-x-dev-old-key "$s"   # README.md:213
  step $F 13-x-key-in-image $R3/transcribe_audio "docker run --rm --entrypoint ls mega-pipeline-transcribe-audio -la /app /app/secrets"
  # Run (see the timings), but not kept: without the key each fails with the same DefaultCredentialsError as the
  # component's `python cli.py --download` just before it, so they teach nothing new (ASSETS.md lists them).
  rm -f "$HERE"/mega-transcribe_audio/{10-transcribe,11-upload}.txt "$HERE"/mega-generate_text/04-upload.txt \
        "$HERE"/mega-synthesis_audio_en/04-synthesis.txt "$HERE"/mega-translate_text/{03-translate,04-upload}.txt \
        "$HERE"/mega-synthesis_audio/03-synthesis.txt
  ;;

gcloud)  # ===== mega-pipeline README.md:189-199 on a laptop with gcloud installed but no account =====
  F=gcloud-laptop; fresh $F
  SDK=$(dirname "$(dirname "$(readlink -f "$(command -v gcloud)")")")
  # each command in a fresh debian:12 shell with no network at all (nothing can reach Google), the Cloud SDK mounted
  # read-only, and one empty home folder kept between commands (no gcloud account, no credentials)
  GHOME=$(mktemp -d); chown 1000:1000 "$GHOME"
  gstep() {
    local name=$1; shift; local t0; t0=$(date +%s.%N)
    { echo "\$ $*"
      docker run --rm --network none --hostname laptop -u 1000:1000 -e HOME=/home/student -e USER=student \
        -v "$SDK":/opt/google-cloud-sdk:ro -v "$GHOME":/home/student -w /home/student debian:12 \
        bash -c "export PATH=/opt/google-cloud-sdk/bin:\$PATH; $*" 2>&1 </dev/null
      echo "[exit $?]"; } | clean > "$HERE/$F/$name.txt"
    timing "$F" "$name" "$t0"
  }
  gstep 00-env 'date -u "+%Y-%m-%d %H:%M UTC"; . /etc/os-release; echo "$PRETTY_NAME"; gcloud --version'  # extra
  # README.md:192 typed exactly as written, placeholder included, at the prompt of an interactive bash (a terminal):
  # user student, gcloud on the PATH. The file shows that terminal.
  SF=$(mktemp); printf '%s\n' 'gcloud config set project <your-project-id>' 'exit' > "$SF"
  SHOW_CMD="(a new terminal, bash on Debian 12; the lines below are typed at its prompt)" TIMING_FILE="$HERE/capture-only/$F-timings.txt" \
    "$PY" -I "$HERE/tty_session.py" "$HERE/$F/01-config-set-project.txt" "$SF" \
    docker run --rm -ti --network none --hostname laptop -v "$SDK":/opt/google-cloud-sdk:ro -v "$GHOME":/home/student debian:12 \
    bash -c 'useradd -M -d /home/student -s /bin/bash -u 1000 student; ln -s /opt/google-cloud-sdk/bin/gcloud /usr/local/bin/gcloud; exec su - student'
  rm -f "$SF"
  gstep 02-config-set-project-filled 'gcloud config set project your-project-id'                          # README.md:192, placeholder filled
  gstep 03-services-enable $'gcloud services enable \\\n  storage.googleapis.com \\\n  aiplatform.googleapis.com \\\n  speech.googleapis.com \\\n  texttospeech.googleapis.com \\\n  translate.googleapis.com'  # README.md:193-198
  gstep 04-x-auth-list 'gcloud auth list'                                                                  # extra
  gstep 05-x-config-list 'gcloud config list'                                                              # extra
  rm -rf "$GHOME"
  ;;
esac
rm -rf "$SIG"
