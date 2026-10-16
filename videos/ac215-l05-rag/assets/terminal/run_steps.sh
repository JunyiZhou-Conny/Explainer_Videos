#!/bin/bash
# Types the L05 README commands (dlops-io/llm-rag, main) into "your laptop" one at a time and saves each one's
# output to its own file: "$ cmd", the output, "[exit N]". Called by capture.sh, which starts the laptop
# (container $LAPTOP, a fresh Docker engine) and exports RELAY/NOPX. Usage:
#   run_steps.sh <terminal_dir> <part>       part = main | gotchas
# Folders written (each is emptied first):
#   main:    laptop/ (your laptop's terminal), cli-container/ (typed at the llm-rag-cli container's prompt)
#   gotchas: gotchas/
#   and capture-only/<folder>-timings.txt.
# Steps not in the README are marked "extra" in the comments and have an "x-" in their file name (ASSETS.md).
HERE=$1; PART=$2
L=${LAPTOP:-l05-laptop}
WS=/home/student/AC215                      # the README's parent folder: llm-rag/ and secrets/ side by side
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
# cli_name: the name of the running llm-rag-cli container (`docker compose run` names it <project>-<service>-run-<id>)
cli_name() { docker exec $L docker ps --filter label=com.docker.compose.service=llm-rag-cli --format '{{.Names}}' | head -1; }
# cstep <folder> <name> <command>: typed at the prompt of the llm-rag-cli container the open session started.
# Run with `docker exec` into that container (as its user app, in /app, with the container's environment), after
# activating /.venv exactly as docker-entrypoint.sh:12 does, so each command gets its own file and exit status.
# stderr is joined to stdout inside the container (as on a terminal), so a traceback stays after the lines printed
# before it (Python's output is unbuffered there, Dockerfile:14).
cstep() {
  local f=$1 name=$2; shift 2; mkdir -p "$HERE/$f"
  local t0; t0=$(date +%s.%N)
  { echo "\$ $*"
    docker exec -u student "${EXEC_ENV[@]}" $L docker exec -w /app "$CLI" bash -c "source /.venv/bin/activate && { $*"$'\n'"} 2>&1" 2>&1 </dev/null
    echo "[exit $?]"; } | clean > "$HERE/$f/$name.txt"
  timing "$f" "$name" "$t0"
}
# ctstep <folder> <name> <command>: the same, in a real terminal (tty_session.py), for output that depends on one (ls).
ctstep() {
  local f=$1 name=$2; shift 2; mkdir -p "$HERE/$f"
  local sf; sf=$(mktemp)
  SHOW_CMD="$*" TIMING_FILE="$HERE/capture-only/$f-timings.txt" "$PY" -I "$HERE/tty_session.py" "$HERE/$f/$name.txt" "$sf" \
    docker exec -ti -u student "${EXEC_ENV[@]}" $L docker exec -ti -w /app "$CLI" bash -c "source /.venv/bin/activate && $*"
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
# as_student <dir> <command>: a capture-only action on the laptop (not typed by the student, not recorded).
as_student() { local d=$1; shift; docker exec -u student -w "$(wdir "$d")" "${EXEC_ENV[@]}" $L bash -lc "$*"; }

# Python typed at the container's prompt for the extras in recorded-embeddings/ (each a `python - <<'EOF'` block)
PY_NORMS=$(cat <<'XEOF'
python - <<'EOF'
import json, math
rows = [json.loads(l) for l in open("outputs/embeddings-char-split-Tolminc Cheese.jsonl")]
norms = [math.sqrt(sum(x * x for x in r["embedding"])) for r in rows]
print(len(rows), "rows,", len(rows[0]["embedding"]), "numbers each")
print("first 5:", [round(x, 4) for x in rows[0]["embedding"][:5]])
print(f"vector lengths: min {min(norms):.3f}, max {max(norms):.3f}")
EOF
XEOF
)
PY_META=$(cat <<'XEOF'
python - <<'EOF'
import chromadb
c = chromadb.HttpClient(host="llm-rag-chromadb", port=8000).get_collection("char-split-collection")
print("count:", c.count())
first = {}
for m in c.get(include=["metadatas"])["metadatas"]:
    first.setdefault(m["book"], m)
for book in sorted(first):
    print(first[book])
EOF
XEOF
)
PY_FILTERS=$(cat <<'XEOF'
python - <<'EOF'
import chromadb
c = chromadb.HttpClient(host="llm-rag-chromadb", port=8000).get_collection("char-split-collection")
bob = {"book": "The Complete Book of Cheese"}
print("all chunks:                      ", c.count())
print("where book = Bob Brown's book:   ", len(c.get(where=bob)["ids"]))
print("  ... and $contains 'Italian':   ", len(c.get(where=bob, where_document={"$contains": "Italian"})["ids"]))
print("  ... and $contains 'Tolminc':   ", len(c.get(where=bob, where_document={"$contains": "Tolminc"})["ids"]))
print("any book, $contains 'Tolminc':   ", len(c.get(where_document={"$contains": "Tolminc"})["ids"]))
EOF
XEOF
)
PY_QUERY=$(cat <<'XEOF'
python - <<'EOF'
import chromadb
c = chromadb.HttpClient(host="llm-rag-chromadb", port=8000).get_collection("char-split-collection")
t = c.get(where={"book": "Tolminc Cheese"}, include=["embeddings", "documents"])
i = next(k for k, d in enumerate(t["documents"]) if "curd" in d)
v = t["embeddings"][i]
print("stand-in query vector: the stored embedding of chunk", t["ids"][i], "(Tolminc Cheese)")
print(repr(t["documents"][i][:72]))
bob_italian = {"where": {"book": "The Complete Book of Cheese"}, "where_document": {"$contains": "Italian"}}
for label, kw in [("no filter", {}), ("where book + $contains 'Italian' (as cli.py:354-359)", bob_italian)]:
    r = c.query(query_embeddings=[v], n_results=10, **kw)
    print("--", label)
    for d, m in zip(r["distances"][0], r["metadatas"][0]):
        print(f"{d:.4f}  {m['book']}")
EOF
XEOF
)
NAMES="curl -s http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections | grep -oE '\"name\":\"[a-z-]+-collection\"|\"dimension\":[a-z0-9]+'"

case $PART in
main)  # ===================== dlops-io/llm-rag, README.md:45-236 (Prerequisites .. Semantic Chunking) ==============
  F=laptop; C=cli-container; E=recorded-embeddings; R=llm-rag
  fresh $F $C $E
  step $F 00-x-env "" "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}} (API {{.Server.APIVersion}}, {{.Server.Os}}/{{.Server.Arch}})'; docker compose version; docker buildx version; git --version; curl --version | head -1"   # extra
  # Prerequisites (README.md:45-48): "Have Docker installed", "Cloned this repository" (the README links the repo;
  # the clone command itself is not printed)
  step $F 01-x-docker-check "" "docker --version; docker compose version"                                  # extra
  step $F 02-clone "" "git clone https://github.com/dlops-io/llm-rag.git"
  # Setup GCP Service Account (README.md:52-69): console only (illustration); the folder layout README.md:64-69
  tstep $F 03-x-mkdir-secrets "" "" "mkdir secrets; ls"                                                     # extra
  # Run LLM RAG Container (README.md:75-85)
  step $F 04-cd "" "cd llm-rag"
  tstep $F 05-x-ls $R "" "ls -a; git log --oneline -1"                                                      # extra
  step $F 05b-x-git-size $R "du -sh .git; git count-objects -vH | grep size-pack"                           # extra (G15)
  # README.md:80 "Update GCP_PROJECT to your own project ID in docker-shell.sh": a capture-only sed sets the
  # placeholder your-project-id (a student types their own in an editor); the file shows the edit.
  as_student $R "sed -i 's/ac215-project/your-project-id/' docker-shell.sh"
  step $F 06-x-edit-gcp-project $R "git diff docker-shell.sh"
  s=$(now)
  session_start $F 07-docker-shell $R "" "sh docker-shell.sh"
  bplain $F 07-docker-shell "$s"
  CLI=$(cli_name); export CLI
  # ---- a second terminal on the laptop, while the container runs (all extra) ----
  step $F 08-x-docker-ps $R "docker ps"
  step $F 09-x-network-ls $R "docker network ls"
  tstep $F 10-x-heartbeat $R "" "curl http://localhost:8000/api/v2/heartbeat"
  tstep $F 11-x-version $R "" "curl http://localhost:8000/api/v2/version"
  step $F 11b-x-chroma-version $R "docker exec llm-rag-chromadb chroma --version; docker image inspect chromadb/chroma:latest --format '{{index .RepoDigests 0}} created {{.Created}}'"
  step $F 12-x-cors-allowed $R "curl -si -H 'Origin: https://ac215-llm-rag.dlops.io' http://localhost:8000/api/v2/heartbeat"
  step $F 12b-x-cors-other $R "curl -si -H 'Origin: https://example.com' http://localhost:8000/api/v2/heartbeat"
  step $F 13-x-docker-volumes $R "ls -la docker-volumes/chromadb"
  step $F 14-x-images $R "docker images"
  step $F 14b-x-image-contents $R "docker run --rm --entrypoint bash llm-rag-cli -c 'du -sh /app/.git; du -sh /.venv; ls -la /app/docker-volumes/chromadb'"  # G15
  step $F 15-x-mounts $R "docker inspect $CLI --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'; docker inspect llm-rag-chromadb --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'"
  # ---- at the container's prompt ----
  cstep $C 00-x-whoami "whoami; pwd; which python; python --version; uv --version"                          # extra
  cstep $C 01-x-env "echo GCP_PROJECT=\$GCP_PROJECT; echo GOOGLE_APPLICATION_CREDENTIALS=\$GOOGLE_APPLICATION_CREDENTIALS; ls -la /secrets"  # extra
  ctstep $C 02-x-ls "ls"                                                                                    # extra
  cstep $C 03-x-packages "uv pip list 2>/dev/null | grep -E '^(chromadb|google-genai|google-auth|langchain|langchain-community|langchain-text-splitters|numpy|pandas|openai|openai-agents) '"  # extra
  cstep $C 04-x-chroma-by-name "getent hosts llm-rag-chromadb; curl -s http://llm-rag-chromadb:8000/api/v2/heartbeat; echo"  # extra
  # Chunk Documents (README.md:91-116)
  cstep $C 10-chunk-char-split "python cli.py --chunk --chunk_type char-split"
  cstep $C 11-x-wc-char-split "wc -l outputs/chunks-char-split-*.jsonl"                                     # extra
  cstep $C 12-x-overlap-char-split $'python -c "import json; c = [json.loads(l)[\'chunk\'] for l in open(\'outputs/chunks-char-split-Tolminc Cheese.jsonl\')]; print(len(c)); print(repr(c[0][-40:])); print(repr(c[1][:40]))"'  # extra
  cstep $C 13-chunk-recursive-split "python cli.py --chunk --chunk_type recursive-split"
  cstep $C 14-x-wc-recursive-split "wc -l outputs/chunks-recursive-split-*.jsonl"                           # extra
  cstep $C 15-x-recursive-chunks $'python -c "import json; c = [json.loads(l)[\'chunk\'] for l in open(\'outputs/chunks-recursive-split-Tolminc Cheese.jsonl\')]; print(len(c)); print(c[0]); print(\'---\'); print(c[1]); print(\'---\'); print(c[2])"'  # extra
  cstep $C 16-x-ls-outputs "ls outputs | head -4; ls outputs | wc -l; du -sh outputs"                      # extra
  step $F 16-x-outputs-on-laptop $R "ls -la outputs | head -5"                                              # extra
  # Generate Embeddings (README.md:122-138): needs the service-account key (none here)
  cstep $C 20-embed-char-split "python cli.py --embed --chunk_type char-split"
  cstep $C 21-embed-recursive-split "python cli.py --embed --chunk_type recursive-split"
  cstep $C 22-x-after-embed "ls outputs | grep '^embeddings-' | wc -l; ls -la /secrets"                    # extra
  # Load Embeddings into Vector Database (README.md:144-165), with no embeddings files (embed failed)
  cstep $C 30-load-char-split "python cli.py --load --chunk_type char-split"
  cstep $C 31-load-recursive-split "python cli.py --load --chunk_type recursive-split"
  tstep $F 17-x-collections $R "" "curl http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections"  # extra
  step $F 17b-x-collection-names $R "$NAMES"                                                              # extra
  step $F 18-x-docker-volumes-after-load $R "ls -la docker-volumes/chromadb"                               # extra
  cstep $C 32-x-load-again "python cli.py --load --chunk_type char-split"                                   # extra
  # Query the Vector Database (README.md:171-186)
  cstep $C 40-query-char-split "python cli.py --query --chunk_type char-split"
  cstep $C 41-query-recursive-split "python cli.py --query --chunk_type recursive-split"
  cstep $C 42-x-get "python cli.py --get --chunk_type char-split"                                           # extra (E13)
  # Chat with LLM (README.md:192-214)
  cstep $C 50-chat-char-split "python cli.py --chat --chunk_type char-split"
  cstep $C 51-chat-recursive-split "python cli.py --chat --chunk_type recursive-split"
  # Advanced RAG: Semantic Chunking (README.md:220-236)
  cstep $C 60-semantic-split "python cli.py --chunk --embed --load --chunk_type semantic-split"
  cstep $C 61-x-after-semantic "ls outputs | grep semantic | wc -l"                                         # extra
  # ---- recorded-embeddings/: the README's --load with the staff's own embeddings files ----
  # The staff committed their outputs/ (chunks and Vertex AI embeddings, gemini-embedding-001, 256 numbers) in
  # 68e0bde (2026-10-07, the "Demo podcast" PR, under llmrag/outputs/; removed again in 58dd602 and the revert, but
  # still in main's history, so every clone has them). Their chunk files are byte-identical to the ones step 10/13
  # made here. Copying their embeddings files into outputs/ (extra, typed on the laptop) stands in for a
  # successful --embed; the --load runs and everything after them are real.
  step $E 00-x-copy-staff-embeddings $R 'git ls-tree -z --name-only 68e0bde llmrag/outputs/ | tr "\0" "\n" | grep "/embeddings-" | while IFS= read -r f; do git show "68e0bde:$f" > "outputs/${f##*/}"; done; ls outputs | grep "^embeddings-" | wc -l; du -ch outputs/embeddings-* | tail -1'
  cstep $E 01-load-char-split "python cli.py --load --chunk_type char-split"
  cstep $E 02-load-recursive-split "python cli.py --load --chunk_type recursive-split"
  step $E 03-x-collection-names $R "$NAMES"
  step $E 04-x-docker-volumes $R "ls -la docker-volumes/chromadb; du -sh docker-volumes/chromadb"
  cstep $E 05-x-get "python cli.py --get --chunk_type char-split"                                           # E13
  cstep $E 06-x-vector-norms "$PY_NORMS"
  cstep $E 07-x-metadata-per-book "$PY_META"                                                                # E8
  cstep $E 08-x-filter-counts "$PY_FILTERS"                                                                 # E2
  cstep $E 09-x-query-by-chunk-vector "$PY_QUERY"
  session_end
  # ---- back on the laptop: what is still running, teardown, persistence (all extra: not in the README) ----
  step $F 20-x-ps-after-exit $R "docker ps -a"
  tstep $F 21-x-compose-down $R "" "docker compose down"
  step $F 22-x-after-down $R "docker ps -a; docker network ls; ls -la docker-volumes/chromadb"
  session_start $F 23-x-docker-shell-again $R "" "sh docker-shell.sh"
  CLI=$(cli_name); export CLI
  step $F 24-x-collection-names-after-restart $R "$NAMES"
  cstep $C 70-x-get-after-restart "python cli.py --get --chunk_type char-split"
  session_end
  tstep $F 25-x-compose-down-final $R "" "docker compose down"
  step $F 26-x-images $R "docker images"
  step $F 27-x-git-status $R "git status; git status --short --ignored"
  # Run, but not kept: each ends in the same DefaultCredentialsError as the kept capture of its README section
  # (20-embed-char-split, 40-query-char-split), so it adds nothing (ASSETS.md; timings stay in capture-only/)
  rm -f "$HERE/$C/21-embed-recursive-split.txt" "$HERE/$C/41-query-recursive-split.txt" \
        "$HERE/$C/50-chat-char-split.txt" "$HERE/$C/51-chat-recursive-split.txt"
  ;;
gotchas)  # ===================== extras: gotchas G5 and G1 of the digest (not README steps) ===================
  F=gotchas; R=llm-rag
  fresh $F
  # G5: Compose without the script, so GCP_PROJECT / GOOGLE_APPLICATION_CREDENTIALS are not set
  tstep $F 01-x-g5-compose-run-direct $R "python cli.py --chunk --chunk_type char-split"$'\n'"exit" "docker compose run --rm llm-rag-cli"
  tstep $F 02-x-g5-compose-down $R "" "docker compose down"
  # G1: a copy of the repo that is not called llm-rag (e.g. GitHub's "Download ZIP" unpacks llm-rag-main/).
  # A second workspace ~/AC215-zip stands in for that student; the clone into llm-rag-main stands in for the unzip.
  as_student "" "mkdir -p $WS-zip"
  step $F 03-x-g1-clone-as-main "$WS-zip" "git clone https://github.com/dlops-io/llm-rag.git llm-rag-main; mkdir secrets; ls"
  tstep $F 04-x-g1-docker-shell "$WS-zip/llm-rag-main" "" "sh docker-shell.sh"
  step $F 05-x-g1-stray-folder "$WS-zip/llm-rag-main" "ls -la ..; ls -la ../llm-rag"
  tstep $F 06-x-g1-compose-down "$WS-zip/llm-rag-main" "" "docker compose down"
  ;;
esac
rm -rf "$SIG"
