#!/bin/bash
# Types the L06 commands into "your laptop" one at a time and saves each one's output to its own file:
# "$ cmd", the output, "[exit N]". Called by capture.sh, which starts the laptop (container $LAPTOP) and exports
# RELAY/NOPX/CA. Usage:
#   run_steps.sh <terminal_dir> <part>       part = rag | adk
# Folders written (start from empty folders; files are overwritten, nothing is removed):
#   rag: laptop/ (your laptop's terminal), cli-container/ (typed at the llm-rag-cli container's prompt)
#   adk: adk-laptop/ (your laptop's terminal in ~/AC215/llm-agent-google-adk), mcp-remote/ (the Cheese Quiz's MCP server)
#   and capture-only/<folder>-timings.txt.
# Steps not in the README are marked "extra" in the comments and have an "x-" in their file name (ASSETS.md).
HERE=$1; PART=$2
L=$LAPTOP
WS=/home/student/AC215                      # the workspace: llm-rag/ and secrets/ side by side (llm-rag README.md:64-69)
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

# step <folder> <name> <dir> <command>: typed in a new terminal on the laptop (a fresh login shell, no terminal
# attached, so progress views print plain lines).
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
# session_start <folder> <name> <dir> <typed lines> <command>: a terminal that stays open (a shell inside a container):
# tstep in the background; the typed lines (may be empty) go in at its prompts, then it waits at the next prompt until
# session_end, which types `exit`. Meanwhile run_steps.sh plays "a second terminal" (step / cstep).
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
# server_start <folder> <name> <dir> <ready-regex> <command>: a terminal running a server (adk web) until session_end
# presses Ctrl+C: tstep in the background, ready once the output matches <ready-regex>.
server_start() {
  local f=$1 name=$2 dir=$3 ready=$4; shift 4
  rm -f "$SIG/up" "$SIG/stop"
  local script="@@wait $ready"$'\n'"@@touch $SIG/up"$'\n'"@@waitfile $SIG/stop"$'\n'"@@sleep 1"$'\n'"@@ctrl-c"
  tstep "$f" "$name" "$dir" "$script" "$@" &
  BGPID=$!
  while [ ! -e "$SIG/up" ] && kill -0 $BGPID 2>/dev/null; do sleep 1; done
}
# cli_name: the name of the running llm-rag-cli container (`docker compose run` names it <project>-<service>-run-<id>)
cli_name() { docker exec $L docker ps --filter label=com.docker.compose.service=llm-rag-cli --format '{{.Names}}' | head -1; }
# cstep <folder> <name> <command>: typed at the prompt of the llm-rag-cli container the open session started.
# Run with `docker exec` into that container (as its user app, in /app, with the container's environment), after
# activating /.venv exactly as docker-entrypoint.sh:12 does, so each command gets its own file and exit status.
# stderr is joined to stdout inside the container (as on a terminal); Python is unbuffered there (Dockerfile:14).
cstep() {
  local f=$1 name=$2; shift 2; mkdir -p "$HERE/$f"
  local t0; t0=$(date +%s.%N)
  { echo "\$ $*"
    docker exec -u student "${EXEC_ENV[@]}" $L docker exec -w /app "$CLI" bash -c "source /.venv/bin/activate && { $*"$'\n'"} 2>&1" 2>&1 </dev/null
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
# as_student <dir> <command>: a capture-only action on the laptop (not typed by the student, not recorded).
as_student() { local d=$1; shift; docker exec -u student -w "$(wdir "$d")" "${EXEC_ENV[@]}" $L bash -lc "$*"; }

# ---------------- Python typed at the llm-rag-cli prompt for the extras (each a `python - <<'EOF'` block) -----------
# The request of call 1, exactly as google-genai 1.39.1 would send it: cli.agent() runs unchanged; only the SDK's
# transport is replaced by a function that prints the URL and JSON body and stops. Nothing is sent, nothing is answered.
PY_CALL1=$(cat <<'XEOF'
python - <<'EOF'
import json, cli
api = cli.llm_client._api_client
def show(method, path, body, http_options=None):     # stands in for the HTTPS request
    req = api._build_request(method, path, body, http_options)
    print(method.upper(), req.url)
    print(json.dumps(body, indent=2))
    raise SystemExit("-- stopped here: nothing was sent to Vertex AI --")
api.request = show
cli.agent(method="char-split")
EOF
XEOF
)
# Your code makes the call: the FunctionCall the model wrote in the staff's recorded run (out.txt:20-27) goes through the
# tutorial's own dispatcher (agent_tools.execute_function_calls) against this laptop's collection. Only embed_func is a
# stand-in: generate_query_embedding needs Vertex AI, so it returns the stored vector of one Tolminc chunk (the first
# one in storage order that mentions "curd"). Then the request of call 2 (cli.py:465-477) is printed as in PY_CALL1: the
# question, the model's recorded turn (function call + its thought_signature, out.txt:20-28) and the function response.
PY_DISPATCH=$(cat <<'XEOF'
python - <<'EOF'
import ast, json, re, cli, agent_tools
from google.genai import types
from google.genai.types import Content, Part
collection = cli.chromadb.HttpClient(host=cli.CHROMADB_HOST, port=cli.CHROMADB_PORT).get_collection("char-split-collection")
t = collection.get(where={"book": "Tolminc Cheese"}, include=["embeddings", "documents"])
i = next(k for k, d in enumerate(t["documents"]) if "curd" in d)
print("stand-in embed_func: returns the stored vector of chunk", t["ids"][i], "(Tolminc Cheese)")
stand_in = lambda text: t["embeddings"][i]
# the model's turn, from the staff's recorded run
rec = open("out.txt").read().splitlines()
sig = ast.literal_eval(rec[27].strip().removeprefix("thought_signature=").rstrip(","))
call = types.FunctionCall(id="call_1212960", name="get_book_by_author",
                          args={"author": "Pavlos Protopapas", "search_content": "cheese making importance location"})
model_turn = Content(role="model", parts=[Part(function_call=call, thought_signature=sig)])
print("Function calls:", [call])
function_responses = agent_tools.execute_function_calls([call], collection, embed_func=stand_in)
print()
print("function_responses: %d part, name=%r, response keys=%s, %d characters" % (
    len(function_responses), function_responses[0].function_response.name,
    list(function_responses[0].function_response.response), len(function_responses[0].function_response.response["content"])))
print()
api = cli.llm_client._api_client
def show(method, path, body, http_options=None):     # stands in for the HTTPS request
    req = api._build_request(method, path, body, http_options)
    print(method.upper(), req.url)
    print(json.dumps(body, indent=2))
    raise SystemExit("-- stopped here: nothing was sent to Vertex AI --")
api.request = show
user_prompt_content = Content(role="user", parts=[Part(text="Describe where cheese making is important in Pavlos's book?")])
cli.llm_client.models.generate_content(          # the call of cli.py:465-477, with the same arguments
    model=cli.GENERATIVE_MODEL,
    contents=[user_prompt_content, model_turn, Content(parts=function_responses)],
    config=types.GenerateContentConfig(tools=[agent_tools.cheese_expert_tool]))
EOF
XEOF
)
# Which books can get_book_by_author reach? The enum of agent_tools.py:19-29 against the metadata in the collection.
PY_AUTHORS=$(cat <<'XEOF'
python - <<'EOF'
import cli, agent_tools
c = cli.chromadb.HttpClient(host=cli.CHROMADB_HOST, port=cli.CHROMADB_PORT).get_collection("char-split-collection")
enum = agent_tools.get_book_by_author_func.parameters.properties["author"].enum
metas = c.get(include=["metadatas"])["metadatas"]
print("chunks in char-split-collection:", len(metas))
print("author (enum value)                          chunks")
for a in enum:
    print(f"  {a:<42} {sum(m.get('author') == a for m in metas):>5}")
print("books whose chunks no enum value can select:")
for b in sorted({m["book"] for m in metas if m.get("author") not in enum}):
    n = sum(m["book"] == b for m in metas)
    print(f"  {b!r}: {n} chunks, author = {next(m.get('author') for m in metas if m['book'] == b)!r}")
EOF
XEOF
)
PY_MODE=$(cat <<'XEOF'
python -c 'from google.genai import types; print(repr(types.FunctionCallingConfig(mode="any")))'
XEOF
)
# ---------------- Python for the ADK extras (uv run python - <<'EOF') ----------------
# 3-mcp-tools without a model: the agent's own MCPToolset (3-mcp-tools/agent.py:20-29) starts the npx filesystem server
# over stdio, lists the tools it lets through tool_filter, and calls list_directory once.
PY_MCP=$(cat <<'XEOF'
uv run python - <<'EOF'
import asyncio, importlib.util
spec = importlib.util.spec_from_file_location("mcp_tools_agent", "3-mcp-tools/agent.py")
agent = importlib.util.module_from_spec(spec); spec.loader.exec_module(agent)
async def main():
    tools = await agent.toolset.get_tools()
    print("tools the agent sees:", [t.name for t in tools])
    session = await agent.toolset._mcp_session_manager.create_session()
    listed = await session.list_tools()
    print("tools the server offers:", len(listed.tools), [t.name for t in listed.tools])
    result = await session.call_tool("list_directory", {"path": agent.ALLOWED_PATH})
    print("list_directory", agent.ALLOWED_PATH, "->")
    print(result.content[0].text)
    await agent.toolset.close()
asyncio.run(main())
EOF
XEOF
)
MCP_URL=https://pavlos-fun-facts.dlops.io/mcp
MCP_H='-H "Content-Type: application/json" -H "Accept: application/json, text/event-stream"'

case $PART in
rag)  # ===================== dlops-io/llm-rag, README.md:242-271 (Agents) and the L05 steps it stands on ============
  F=laptop; C=cli-container; R=llm-rag
  step $F 00-x-env "" "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}} (API {{.Server.APIVersion}}, {{.Server.Os}}/{{.Server.Arch}})'; docker compose version; git --version; curl --version | head -1"   # extra
  # The Agents section runs inside the container of "Run LLM RAG Container" (README.md:75-85) and queries the collection
  # of "Load Embeddings" (README.md:144-165): L05's steps, repeated here on a fresh laptop.
  step $F 01-clone "" "git clone https://github.com/dlops-io/llm-rag.git"
  tstep $F 02-x-mkdir-secrets "" "" "mkdir secrets; ls"                                                     # extra
  step $F 03-cd "" "cd llm-rag"
  step $F 04-x-git-log $R "git log --oneline -1"                                                           # extra
  # README.md:80: a capture-only sed sets the placeholder your-project-id (a student types their own ID in an editor)
  as_student $R "sed -i 's/ac215-project/your-project-id/' docker-shell.sh"
  step $F 05-x-edit-gcp-project $R "git diff docker-shell.sh"                                              # extra
  s=$(now)
  session_start $F 06-docker-shell $R "" "sh docker-shell.sh"
  bplain $F 06-docker-shell "$s"
  CLI=$(cli_name); export CLI
  # ---- a second terminal on the laptop, while the container runs (extra) ----
  step $F 07-x-docker-ps $R "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'"
  # ---- at the container's prompt ----
  cstep $C 00-x-whoami "whoami; pwd; which python; python --version; echo GCP_PROJECT=\$GCP_PROJECT; echo GOOGLE_APPLICATION_CREDENTIALS=\$GOOGLE_APPLICATION_CREDENTIALS; ls -la /secrets"  # extra
  cstep $C 01-x-packages "uv pip list 2>/dev/null | grep -E '^(chromadb|google-genai|google-auth) '"          # extra
  cstep $C 02-x-help "python cli.py --help"                                                                # extra
  # A fresh clone has no collection yet (digest G6): the README's Agents command, run before any load
  cstep $C 10-agent-no-collection "python cli.py --agent --chunk_type char-split"
  cstep $C 11-x-get-no-collection "python cli.py --get --chunk_type char-split"                            # extra
  # Build the collection as L05 did: --embed needs Vertex AI, so the staff's own embeddings files (committed in
  # 68e0bde, the reverted "Demo podcast" PR; still in main's history) stand in for it (extra, typed on the laptop).
  step $F 08-x-copy-staff-embeddings $R 'mkdir -p outputs; git ls-tree -z --name-only 68e0bde llmrag/outputs/ | tr "\0" "\n" | grep "/embeddings-char-split-" | while IFS= read -r f; do git show "68e0bde:$f" > "outputs/${f##*/}"; done; ls outputs | wc -l; du -ch outputs/embeddings-* | tail -1'
  cstep $C 20-load-char-split "python cli.py --load --chunk_type char-split"                                # L05 README.md:150
  cstep $C 21-x-get "python cli.py --get --chunk_type char-split"                                           # extra (digest B2)
  # Agents (README.md:257-259)
  cstep $C 30-agent "python cli.py --agent --chunk_type char-split"
  cstep $C 31-x-call1-request "$PY_CALL1"                                                                   # extra
  cstep $C 32-x-mode-any "$PY_MODE"                                                                         # extra
  cstep $C 33-x-dispatch-recorded-call "$PY_DISPATCH"                                                       # extra
  cstep $C 34-x-authors "$PY_AUTHORS"                                                                       # extra (P1, E4)
  # ---- back in the second terminal (extras) ----
  step $F 09-x-book-changed $R "git show --stat --format='%h %ad %s' --date=short 85bba32; head -4 'input-datasets/books/Tolminc Cheese.txt'"
  step $F 10-x-old-words $R "for w in transhumance 'Soča' 'Monastic' 'cultural artifact'; do printf '%-18s out.txt %2s   book today %2s   book before 85bba32 %2s\n' \"\$w\" \"\$(grep -c \"\$w\" out.txt)\" \"\$(grep -c \"\$w\" 'input-datasets/books/Tolminc Cheese.txt')\" \"\$(git show '85bba32^:input-datasets/books/Tolminc Cheese.txt' | grep -c \"\$w\")\"; done"
  step $F 11-x-hosted-agent $R "curl -s -o /dev/null -w '%{http_code} %{content_type}\\n' https://ac215-llm-rag.dlops.io/agent"
  session_end
  # ---- after exit: the teardown of the digest (B6) ----
  step $F 12-x-ps-after-exit $R "docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Ports}}'"
  tstep $F 13-x-compose-down $R "" "docker compose down"
  step $F 14-x-git-status $R "git status --short"
  ;;
adk)  # ===================== dlops-io/llm-agent-google-adk, README.md (the whole root README) ======================
  F=adk-laptop; M=mcp-remote; A=llm-agent-google-adk
  step $F 00-x-env "" "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; head -1 /etc/os-release; uv --version; git --version; node --version; npm --version; command -v python3 python || echo 'no python3 on PATH'"   # extra
  # Getting Started 1 (README.md:74-79). The README writes `git clone <repository-url>`; this is the repo's URL.
  step $F 01-clone "" "git clone https://github.com/dlops-io/llm-agent-google-adk.git"
  step $F 02-cd-as-written "" "cd google-adk-tutorial"           # README.md:78 as written: the folder has another name
  step $F 03-cd "" "cd llm-agent-google-adk"
  tstep $F 04-x-ls $A "" "ls -a"                                                                            # extra
  # Getting Started 2 (README.md:81-86)
  step $F 05-cp-env $A "cp .env.example .env"
  step $F 06-x-env-file $A "grep -v '^#' .env | grep ."                                                    # extra
  # "Edit .env and add your GOOGLE_API_KEY" (README.md:85) and Getting Started 3 (AI Studio, README.md:88-94) need a
  # Google account: not done here. The .env keeps the placeholder key.
  # Getting Started 4 (README.md:96-101), exactly as written, on a laptop with no Python of its own
  tstep $F 07-uv-sync $A "" "uv sync"
  step $F 08-x-after-failed-sync $A "ls -a; grep -c '^name = ' uv.lock; grep -A1 '^name = \"google-adk\"' uv.lock; grep -A1 '^name = \"onnxruntime\"' uv.lock; head -3 .venv/pyvenv.cfg"
  # The fix (not in the README): a Python that every dependency has wheels for
  tstep $F 09-x-python-pin $A "" "uv python pin 3.13"
  step $F 10-x-sync-plan $A "uv sync --dry-run"                       # extra: the plan on Linux x86_64 (no override)
  # capture-only: from here on uv takes PyTorch's CPU-only wheels (capture.sh), from the user's uv config; the lockfile
  # the failed sync wrote pins the CUDA build, so it is removed and the next sync resolves again
  as_student $A "rm -f uv.lock; mkdir -p ~/.config/uv; printf '%s\n' '# capture-only (ASSETS.md): CPU-only PyTorch wheels instead of the CUDA build' 'index-strategy = \"unsafe-best-match\"' '' '[[index]]' 'url = \"https://download.pytorch.org/whl/cpu\"' > ~/.config/uv/uv.toml"
  step $F 11-x-capture-only-uv-config $A "cat ~/.config/uv/uv.toml; ls uv.lock"
  tstep $F 12-uv-sync $A "" "uv sync"                                  # README.md:100, again, with the pin
  step $F 13-x-adk-version $A "uv run adk --version"
  step $F 14-x-packages $A "uv pip list 2>/dev/null | grep -E '^(google-adk|google-genai|litellm|fastapi|uvicorn|mcp|chromadb|sentence-transformers|torch|onnxruntime) '; du -sh .venv"
  # Running Agents, option 1 (README.md:111-119): `uv run adk web`, then http://localhost:8000 in a browser
  server_start $F 15-adk-web $A "Uvicorn running on" "uv run adk web"
  step $F 16-x-root-page $A "curl -sI http://localhost:8000/ | head -3"
  step $F 17-x-list-apps $A "curl -s http://localhost:8000/list-apps; echo"
  step $F 18-x-select-1-baseline $A "curl -s http://localhost:8000/dev/apps/1-baseline/build_graph; echo"
  session_end
  # The fix of digest G1 (not in the README): pin ADK below 1.28, which still accepts folder names like 1-baseline
  tstep $F 19-x-uv-add-pin $A "" 'uv add "google-adk>=1.8.0,<1.28"'
  step $F 20-x-adk-version-pinned $A "uv run adk --version"
  step $F 21-x-diff-pyproject $A "git diff pyproject.toml"
  server_start $F 22-adk-web-pinned $A "Uvicorn running on" "uv run adk web"
  step $F 23-x-list-apps $A "curl -s http://localhost:8000/list-apps; echo"
  step $F 24-x-select-1-baseline $A "curl -s http://localhost:8000/dev/build_graph/1-baseline; echo"
  step $F 25-x-new-session $A "curl -s -X POST http://localhost:8000/apps/1-baseline/users/student/sessions; echo"
  step $F 26-x-send-placeholder-key $A "SID=\$(curl -s -X POST http://localhost:8000/apps/1-baseline/users/student/sessions | grep -o '\"id\":\"[^\"]*\"' | head -1 | cut -d'\"' -f4); curl -s -X POST http://localhost:8000/run -H 'Content-Type: application/json' -d '{\"app_name\": \"1-baseline\", \"user_id\": \"student\", \"session_id\": \"'\$SID'\", \"new_message\": {\"role\": \"user\", \"parts\": [{\"text\": \"2 adults, Boston to Montreal, Oct 30 - Nov 2, 1500 dollars, train preferred\"}]}}'; echo"
  session_end
  # QUICKSTART.md:24 (digest G9) and README variants without `web` (digest G10)
  step $F 27-x-quickstart-file $A "uv run adk web 1-baseline/agent.py"
  step $F 28-x-adk-without-web $A "uv run adk"
  # 3-mcp-tools (module README): MCP over stdio, without a model
  step $F 29-x-node $A "node --version; npx --version"
  step $F 30-x-mcp-toolset $A "$PY_MCP"
  # digest G3: llm-rag's Chroma still holds port 8000 (stand-in: a chromadb/chroma container in this laptop's network)
  # (CHROMA_IMAGE: the recording machine's copy of chromadb/chroma, by id, so nothing is pulled; default: latest)
  docker run -d --rm --name l06-adk-chroma --network container:$L "${CHROMA_IMAGE:-chromadb/chroma:latest}" >/dev/null
  sleep 5
  step $F 31-x-port-8000-busy $A "curl -s http://localhost:8000/api/v2/heartbeat; echo; uv run adk web"
  server_start $F 32-x-adk-web-port-8080 $A "Uvicorn running on" "uv run adk web --port 8080"
  step $F 33-x-list-apps-8080 $A "curl -s http://localhost:8080/list-apps; echo"
  session_end
  docker rm -f l06-adk-chroma >/dev/null 2>&1 || true
  step $F 34-x-git-status $A "git status --short; git status --short --ignored | grep '^!!'"
  # ---- mcp-remote/: the Cheese Quiz's remote MCP server (Colab cell 54), spoken to with curl (extras) ----
  step $M 01-x-browser-get "" "curl -si $MCP_URL | head -12"
  step $M 02-x-initialize "" "curl -s -D /tmp/mcp-headers -X POST $MCP_URL $MCP_H -d '{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"initialize\",\"params\":{\"protocolVersion\":\"2025-06-18\",\"capabilities\":{},\"clientInfo\":{\"name\":\"curl\",\"version\":\"8\"}}}'; echo; grep -i '^mcp-session-id' /tmp/mcp-headers | sed 's/: .*/: <id>/'"
  step $M 03-x-tools-list "" "SID=\$(grep -i '^mcp-session-id' /tmp/mcp-headers | cut -d' ' -f2 | tr -d '\r'); curl -s -X POST $MCP_URL $MCP_H -H \"mcp-session-id: \$SID\" -H 'mcp-protocol-version: 2025-06-18' -d '{\"jsonrpc\":\"2.0\",\"method\":\"notifications/initialized\"}'; curl -s -X POST $MCP_URL $MCP_H -H \"mcp-session-id: \$SID\" -H 'mcp-protocol-version: 2025-06-18' -d '{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/list\"}'; echo"
  step $M 04-x-tools-call "" "SID=\$(grep -i '^mcp-session-id' /tmp/mcp-headers | cut -d' ' -f2 | tr -d '\r'); curl -s -X POST $MCP_URL $MCP_H -H \"mcp-session-id: \$SID\" -H 'mcp-protocol-version: 2025-06-18' -d '{\"jsonrpc\":\"2.0\",\"id\":3,\"method\":\"tools/call\",\"params\":{\"name\":\"pavlos_fun_fact_mcp\",\"arguments\":{}}}'; echo"
  ;;
esac
rm -f "$SIG/up" "$SIG/stop"; rmdir "$SIG" 2>/dev/null || true
