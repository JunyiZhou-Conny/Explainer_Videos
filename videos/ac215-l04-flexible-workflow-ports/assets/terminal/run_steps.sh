#!/bin/bash
# Types the L04 README commands into "your laptop" one at a time and saves each one's output to its own file:
# "$ cmd", the output, "[exit N]". Called by capture.sh, which starts the laptop (container $LAPTOP, a fresh
# Docker engine) and exports RELAY/NOPX. Usage:
#   run_steps.sh <terminal_dir> <part>       part = port | mega | gcloud
# Folders written: port-laptop/, mega-laptop/, gcloud-laptop/; capture-only/<folder>-timings.txt.
# Steps not in the README are marked "extra" in the comments (and in ASSETS.md).
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

# step <folder> <name> <dir under ~/AC215> <command>: typed in a new terminal on the laptop (a fresh login shell,
# no terminal attached, so Docker prints plain progress).
step() {
  local f=$1 name=$2 dir=$3; shift 3; mkdir -p "$HERE/$f"
  local t0; t0=$(date +%s.%N)
  { echo "\$ $*"
    docker exec -u student -w "$WS/$dir" "${EXEC_ENV[@]}" $L bash -lc "$*" 2>&1 </dev/null
    echo "[exit $?]"; } | clean > "$HERE/$f/$name.txt"
  printf '%s\t%s UTC\t%ss\n' "$name" "$(date -u +%H:%M:%S)" \
    "$(awk "BEGIN{printf \"%.1f\", $(date +%s.%N) - $t0}")" >> "$HERE/capture-only/$f-timings.txt"
}
# tstep <folder> <name> <dir> <script> <command>: the same in a real terminal (pseudo-terminal 80x40,
# tty_session.py): what the terminal shows at the end. <script> = lines typed at the prompts, and directives.
tstep() {
  local f=$1 name=$2 dir=$3 typed=$4; shift 4; mkdir -p "$HERE/$f"
  local sf; sf=$(mktemp); printf '%s\n' "$typed" > "$sf"
  SHOW_CMD="$*" TIMING_FILE="$HERE/capture-only/$f-timings.txt" "$PY" -I "$HERE/tty_session.py" "$HERE/$f/$name.txt" "$sf" \
    docker exec -ti -u student -w "$WS/$dir" "${EXEC_ENV[@]}" $L bash -lc "$*"
  rm -f "$sf"
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
# as_root <command>: a capture-only action on the laptop (not typed by the student, not recorded).
as_root() { docker exec $L sh -c "$*"; }
as_student() { docker exec -u student -w "$WS" "${EXEC_ENV[@]}" $L bash -lc "$*"; }

case $PART in
port)  # ===================== dlops-io/port_toy, README.md (whole) =====================
  F=port-laptop; P=port_toy
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
  sleep 2
  step $F 12-logs-processor $P "docker logs processor"
  step $F 13-logs-gateway $P "docker logs gateway"
  # Send a message (145-157): the browser's request (index.html:95-99), sent with curl. extra (browser stand-in)
  SEND8090="curl -s -X POST http://localhost:8090 -H 'Content-Type: application/json' -d '{\"text\": \"hello from the laptop\"}'; echo"
  SEND8095="curl -s -X POST http://localhost:8095 -H 'Content-Type: application/json' -d '{\"text\": \"hello from the laptop\"}'; echo"
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
  # Test from your laptop (246-264), from inside the gateway (266-292)
  step $F 22-curl-8090 $P "curl http://localhost:8090"
  step $F 23-curl-9200 $P "curl --max-time 3 http://localhost:9200/health"
  step $F 24-exec-processor $P "docker exec gateway curl http://processor:9200/health"
  step $F 25-exec-localhost $P "docker exec gateway curl --max-time 3 http://localhost:9200/health"
  # extras: whose localhost; the network's phone book (Handy commands: docker network inspect toynet)
  step $F 26-x-exec-localhost-9100 $P "docker exec gateway curl -s http://localhost:9100 | head -4"
  step $F 27-x-processor-has-curl $P "docker exec processor curl --version | head -1"
  step $F 28-network-inspect $P "docker network inspect toynet"
  step $F 29-x-dns $P "docker exec gateway cat /etc/resolv.conf; docker exec gateway getent hosts processor gateway"
  # Step 3: Change the host port (335-355)
  step $F 30-rm-gateway $P "docker rm -f gateway"
  step $F 31-run-gateway-8095 $P $'docker run -d --name gateway --network toynet \\\n  -p 127.0.0.1:8095:9100 \\\n  -e PROCESSOR_HOST=processor \\\n  -e PROCESSOR_PORT=9200 \\\n  toy-gateway'
  sleep 2
  step $F 32-send-8095 $P "$SEND8095"                                                                       # browser stand-in
  step $F 33-curl-8090-gone $P "curl --max-time 3 http://localhost:8090"                                    # extra (README 355)
  step $F 34-logs-gateway-8095 $P "docker logs gateway"                                                     # extra (E15)
  step $F 35-ps-8095 $P "docker ps --format 'table {{.Image}}\t{{.Ports}}\t{{.Names}}'"                    # extra
  # Change the processor's port (365-382)
  step $F 36-rm-processor $P "docker rm -f processor"
  step $F 37-run-processor-9300 $P $'docker run -d --name processor --network toynet \\\n  -e PORT=9300 toy-processor'
  sleep 2
  step $F 38-send-fails $P "$SEND8095"                                                                      # browser stand-in
  step $F 39-logs-gateway-refused $P "docker logs gateway"                                                  # extra (E16)
  step $F 40-logs-processor-9300 $P "docker logs processor"                                                 # extra
  # Update the gateway (384-409)
  step $F 41-rm-gateway $P "docker rm -f gateway"
  step $F 42-run-gateway-9300 $P $'docker run -d --name gateway --network toynet \\\n  -p 127.0.0.1:8090:9100 \\\n  -e PROCESSOR_HOST=processor \\\n  -e PROCESSOR_PORT=9300 \\\n  toy-gateway'
  sleep 2
  step $F 43-send-9300 $P "$SEND8090"                                                                       # browser stand-in
  # Clean up before Compose (411-420)
  step $F 44-rm-both $P "docker rm -f gateway processor"
  step $F 45-network-rm $P "docker network rm toynet"
  step $F 46-x-after-cleanup $P "docker ps -a; docker network ls"                                          # extra
  # Step 4: Start the app (450-460) in one terminal; the other commands in a second terminal while it runs
  rm -f "$SIG"/*
  tstep $F 47-compose-up $P "$(printf '%s\n' '@@wait (?s)(processor listening.*gateway listening|gateway listening.*processor listening)' \
      "@@touch $SIG/up" "@@waitfile $SIG/stop" '@@ctrl-c')" "docker compose up" &
  BG=$!
  while [ ! -e "$SIG/up" ] && kill -0 $BG 2>/dev/null; do sleep 1; done
  sleep 2
  step $F 48-compose-ps $P "docker compose ps"                                                              # README 480
  step $F 49-send-compose $P "$SEND8090"                                                                    # browser stand-in
  step $F 50-network-ls-compose $P "docker network ls"                                                      # extra
  step $F 51-compose-exec $P "docker compose exec gateway curl http://processor:9200/health"                # README 481
  touch "$SIG/stop"                       # press Ctrl+C in the first terminal (README 505-507)
  wait $BG
  step $F 52-compose-ps-a-stopped $P "docker compose ps -a"                                                 # README 521-525
  step $F 53-compose-down $P "docker compose down"                                                          # README 509-515
  step $F 54-compose-ps-a-after $P "docker compose ps -a"
  # "After changing a setting, run: docker compose up -d" (487-495)
  step $F 55-compose-up-d $P "docker compose up -d"
  step $F 56-compose-ps-d $P "docker compose ps"                                                            # extra
  as_student "cd port_toy && sed -i 's|\"127.0.0.1:8090:9100\"|\"127.0.0.1:8095:9100\"|' docker-compose.yml"   # the edit (capture-only sed)
  step $F 57-x-edit-port $P "git diff"                                                                      # extra
  step $F 58-compose-up-d-changed $P "docker compose up -d"
  step $F 59-x-send-8095-compose $P "$SEND8095"                                                             # browser stand-in
  as_student "cd port_toy && git checkout -q docker-compose.yml"
  step $F 60-compose-up-d-restored $P "docker compose up -d"
  # "If you change a Dockerfile or something copied into an image during its build" (497-501)
  as_student "cd port_toy && printf '\n# edited\n' >> processor/processor.py"
  step $F 61-x-edit-processor $P "git diff"                                                                 # extra
  s=$(now); step $F 62-compose-up-d-build $P "docker compose up -d --build"; bplain $F 62-compose-up-d-build "$s"
  as_student "cd port_toy && git checkout -q processor/processor.py"
  step $F 63-x-compose-logs $P "docker compose logs"                                                        # extra (Handy: logs)
  # Stop and remove the app (505-529), this time while it runs in the background
  step $F 64-compose-down-running $P "docker compose down"
  step $F 65-compose-ps-a-empty $P "docker compose ps -a"
  step $F 66-x-images-remain $P "docker image ls"                                                           # extra (README 515)
  # extra, gotcha G11: Compose right after the by-hand steps, without "Clean up before Compose"
  step $F 67-x-g11-by-hand $P $'docker network create toynet\ndocker run -d --name processor --network toynet \\\n  -e PORT=9200 toy-processor'
  step $F 68-x-g11-compose-up $P "docker compose up -d"
  step $F 69-x-g11-cleanup $P $'docker rm -f gateway processor\ndocker network rm toynet'
  step $F 69b-x-g11-compose-up-net $P "docker network create toynet; docker compose up -d"
  step $F 69c-x-g11-cleanup $P "docker compose down; docker network rm toynet; docker network ls"
  # extra, Exercise 3: the processor started without --network (cheat sheet: could not resolve host)
  step $F 70-x-ex3-no-network $P $'docker network create toynet\ndocker run -d --name processor -e PORT=9200 toy-processor\ndocker run -d --name gateway --network toynet \\\n  -p 127.0.0.1:8090:9100 \\\n  -e PROCESSOR_HOST=processor \\\n  -e PROCESSOR_PORT=9200 \\\n  toy-gateway'
  sleep 2
  step $F 71-x-ex3-resolve $P "docker exec gateway curl --max-time 3 http://processor:9200/health"
  step $F 72-x-ex3-send $P "$SEND8090"
  step $F 73-x-ex3-logs $P "docker logs gateway"
  step $F 74-x-ex3-cleanup $P $'docker rm -f gateway processor\ndocker network rm toynet'
  ;;
gcloud)  # ===== mega-pipeline README.md:189-199 on a laptop with gcloud installed but no account =====
  F=gcloud-laptop; mkdir -p "$HERE/$F"
  SDK=$(dirname "$(dirname "$(readlink -f "$(command -v gcloud)")")")
  # a fresh debian:12 shell, no network at all (nothing can reach Google), the SDK mounted read-only, an empty
  # gcloud configuration (no account, no credentials)
  SF=$(mktemp)
  printf '%s\n' 'gcloud --version' 'gcloud config set project <your-project-id>' \
    'gcloud config set project your-project-id' \
    'gcloud services enable \' '  storage.googleapis.com \' '  aiplatform.googleapis.com \' \
    '  speech.googleapis.com \' '  texttospeech.googleapis.com \' '  translate.googleapis.com' \
    'gcloud auth list' 'exit' > "$SF"
  PROMPT_RE='(\$|>) $' SHOW_CMD="(a new terminal; the lines below are typed at its prompt)" \
    "$PY" -I "$HERE/tty_session.py" "$HERE/$F/01-gcloud-session.txt" "$SF" \
    docker run --rm -ti --network none --hostname laptop -v "$SDK":/opt/google-cloud-sdk:ro debian:12 bash -c \
    'useradd -m -s /bin/bash student; ln -s /opt/google-cloud-sdk/bin/gcloud /usr/local/bin/gcloud; exec su - student'
  rm -f "$SF"
  ;;
esac
rm -rf "$SIG"
