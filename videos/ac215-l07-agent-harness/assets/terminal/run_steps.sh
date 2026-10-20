#!/bin/bash
# Types the L07 commands into "your laptop" one at a time and saves each one's output to its own file:
# "$ cmd", the output, "[exit N]". Called by capture.sh, which starts the laptop (container $LAPTOP) and exports
# RELAY/NOPX/CA. Usage:
#   run_steps.sh <terminal_dir>
# Folders written (start from empty folders; files are overwritten, nothing is removed):
#   laptop/      your laptop's terminal, in ~/AC215/agent-harness (README.md:92 "Run these commands on your host
#                machine, from agent-harness")
#   container/   typed at the agent-harness container's prompt, app@<id>:/app$ (README.md:108 "Run every remaining
#                command inside the container, from /app")
#   capture-only/<folder>-timings.txt
# The README's commands run in README order, exactly as written. Steps not in the README are marked "extra" in the
# comments and have an "x-" in their file name (ASSETS.md).
HERE=$1
L=$LAPTOP
WS=/home/student/AC215
REPO=$WS/agent-harness                       # the clone; ../secrets sits next to it (docker-shell.sh:9)
CTR=agent-harness                            # the container docker-shell.sh starts (docker run --name agent-harness)
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
# run_steps.sh plays "a second terminal" (step) and types at the container's prompt (cstep / ctstep).
session_start() {
  local f=$1 name=$2 dir=$3; shift 3
  rm -f "$SIG/up" "$SIG/stop"
  local script="@@prompt"$'\n'"@@touch $SIG/up"$'\n'"@@waitfile $SIG/stop"$'\n'"exit"
  tstep "$f" "$name" "$dir" '[$#] $' "$script" "$@" &
  BGPID=$!
  while [ ! -e "$SIG/up" ] && kill -0 $BGPID 2>/dev/null; do sleep 1; done
}
session_end() { touch "$SIG/stop"; wait $BGPID; }
# cstep <folder> <name> <command>: typed at the prompt of the agent-harness container the open session started.
# Run with `docker exec` into that container (as its user app, in /app, with the container's environment), after
# activating /.venv exactly as docker-entrypoint.sh:12 does, so each command gets its own file and exit status.
# stderr is joined to stdout inside the container (as on a terminal); Python is unbuffered there (Dockerfile:14).
cstep() {
  local f=$1 name=$2; shift 2; mkdir -p "$HERE/$f"
  local t0; t0=$(date +%s.%N)
  { echo "\$ $*"
    docker exec -u student "${EXEC_ENV[@]}" $L docker exec -w /app $CTR bash -c "source /.venv/bin/activate && { $*"$'\n'"} 2>&1" 2>&1 </dev/null
    echo "[exit $?]"; } | clean > "$HERE/$f/$name.txt"
  timing "$f" "$name" "$t0"
}
# ctstep <folder> <name> <prompt-regex> <script> <command>: the same in a real terminal, for a command that asks a
# question (approve/decline): <script> is typed at the question. The terminal is 250 columns wide here, so that long
# lines (the customer ask, the pairings) are not wrapped in the file; scenes fold them.
ctstep() {
  local f=$1 name=$2 prx=$3 typed=$4; shift 4; mkdir -p "$HERE/$f"
  local sf; sf=$(mktemp); printf '%s\n' "$typed" > "$sf"
  SHOW_CMD="$*" PROMPT_RE="$prx" TIMING_FILE="$HERE/capture-only/$f-timings.txt" TTY_COLS=250 \
    "$PY" -I "$HERE/tty_session.py" "$HERE/$f/$name.txt" "$sf" \
    docker exec -ti -u student "${EXEC_ENV[@]}" $L docker exec -ti -w /app $CTR bash -c "source /.venv/bin/activate && $*"
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
# runid <file> <pattern-before-id>: the first 32-hex run ID that follows <pattern> in a captured file
runid() { grep -oE "$2 [0-9a-f]{32}" "$HERE/$1" | head -1 | grep -oE '[0-9a-f]{32}$'; }

# ======================= laptop: clone, ../secrets, the key placeholder, docker-shell.sh =======================
step laptop 00-x-env $WS 'date -u; uname -m; docker version --format "Docker Engine {{.Server.Version}} (client {{.Client.Version}}, API {{.Server.APIVersion}}, {{.Server.Os}}/{{.Server.Arch}})"; git --version; whoami; id -u; pwd'
# extra: the README assumes "A local copy of this repository" (README.md:48) and prints no clone command
step laptop 01-x-clone $WS 'git clone https://github.com/dlops-io/agent-harness.git'
step laptop 02-x-git-log $REPO 'git log -1 --format="%h %H%n%cd %s" --date=iso; git branch -a'
step laptop 03-x-ls $REPO 'ls -a'
step laptop 04-mkdir-secrets $REPO 'mkdir -p ../secrets'                                   # README.md:96
step laptop 05-x-ls-workspace $REPO 'ls -la ..; ls -A ../secrets | wc -l'
step laptop 06-export-key $REPO 'export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"'             # README.md:99
# README.md:101, in the same shell as 06 (its export is in effect): build, run, the entrypoint's banner, the prompt
T0=$(date -u +%Y-%m-%dT%H:%M:%S)
SHOW='bash docker-shell.sh' session_start laptop 07-docker-shell $REPO \
  'export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"; bash docker-shell.sh'
# ----- a second terminal on the laptop, while the container runs (extras) -----
step laptop 08-x-docker-ps $REPO 'docker ps'
step laptop 09-x-docker-images $REPO 'docker images'
step laptop 10-x-container-env $REPO "docker inspect agent-harness --format '{{range .Config.Env}}{{println .}}{{end}}' | grep -E '^(OPENAI_API_KEY|GCP_PROJECT|GOOGLE_APPLICATION_CREDENTIALS)='"
step laptop 11-x-mounts $REPO "docker inspect agent-harness --format '{{range .Mounts}}{{.Source}} -> {{.Destination}}{{println}}{{end}}'; docker inspect agent-harness --format 'ports: {{json .NetworkSettings.Ports}}  user: {{.Config.User}}  workdir: {{.Config.WorkingDir}}'"
bplain laptop 07-docker-shell "$T0"
# README.md:106 + 110-116: docker-shell.sh again while the container runs (the docker exec path), then the README's
# three lines that set the key inside the container without echoing it. The value typed at the hidden prompt is the
# README's placeholder, YOUR_OPENAI_API_KEY. `echo ${#OPENAI_API_KEY}` (its length, not its value) is an extra check.
tstep laptop 12-docker-shell-again-read-key $REPO '([$#]|key:) $' \
  "$(printf '%s\n' 'read -rsp "OpenAI API key: " OPENAI_API_KEY' 'YOUR_OPENAI_API_KEY' 'export OPENAI_API_KEY' "printf '\\n'" 'echo ${#OPENAI_API_KEY}' 'exit')" \
  'bash docker-shell.sh'

# ======================= container: Setup and verification =======================
step_c() { cstep container "$@"; }
step_c 00-x-whoami 'whoami; id; pwd; which python; python --version; uv --version; echo "VIRTUAL_ENV=$VIRTUAL_ENV"; echo "GCP_PROJECT=$GCP_PROJECT"; echo "GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS"; ls -la /secrets'
step_c 01-x-packages 'uv pip list 2>/dev/null | grep -E "^(agent-framework|agent-framework-core|agent-framework-openai|agent-framework-gemini|claude-agent-sdk|openai|pydantic|httpx|opentelemetry-api|opentelemetry-sdk) "; echo "packages in /.venv: $(uv pip list 2>/dev/null | tail -n +3 | wc -l)"; du -sh /.venv; python -c "import IPython" 2>&1 | tail -1; python -c "import pandas" 2>&1 | tail -1'
step_c 02-x-ls-app 'ls -la /app'
step_c 03-check-sdk 'python -m scripts.check_sdk'                                         # README.md:123
step_c 04-tests 'python -m tests'                                                        # README.md:124
step_c 05-tests-show-logs 'python -m tests --show-logs'                                  # README.md:132
step_c 06-model "python -c 'from formaggio.config import MODEL; print(MODEL)'"           # README.md:142
step_c 07-tests-notebook 'python -m tests -p test_notebook.py'                           # README.md:69
step_c 08-tests-chat-view 'python -m tests -p test_chat_view.py'                         # README.md:88

# ======================= container: 1. Recap — agent and tools =======================
step_c 10-act1-standard 'python cli.py --act 1 --scenario standard'                      # README.md:178 (live)
step_c 11-act1-show-json 'python cli.py --act 1 --scenario standard --show-json'         # README.md:195 (live)
step_c 12-act1-missing-details 'python cli.py --act 1 --scenario missing-details'        # README.md:245 (live)
step_c 13-x-act1-fixture 'python cli.py --act 1 --fixture'                              # extra: digest §6 gotcha

# ======================= container: 2. Context Engineering =======================
step_c 20-act2-compare 'python cli.py --act 2 --compare'                                 # README.md:269 (live)
step_c 21-act2-personalized-basic 'python cli.py --act 2 --scenario personalized --context basic'          # :272 (live)
step_c 22-act2-personalized-enriched 'python cli.py --act 2 --scenario personalized --context enriched'    # :273 (live)
step_c 23-act2-preference-override 'python cli.py --act 2 --scenario preference-override --context enriched' # :274 (live)
step_c 24-act3-pa-shipping 'python cli.py --act 3 --scenario pa-shipping'                # README.md:286 (live)
step_c 25-act2-evaluate-live 'python cli.py --act 2 --evaluate core --case personalized --case preference-override --repeats 3 --label act2-context-live-1'  # :295 (live)
step_c 26-view-report-act2-live 'python cli.py --view-report act2-context-live-1'        # README.md:296
step_c 27-preview-context 'python cli.py --preview-context --scenario standard'          # README.md:311 (offline)
step_c 28-act2-standard 'python cli.py --act 2 --scenario standard'                      # README.md:321 (live)
# extra: the PA/NY counterexample every individual Act 2 run prints after its live run (README.md:277-281;
# act2_context.py print_shipping_demo), called directly: the validator's own output, no model involved
step_c 29-x-shipping-demo "python -c 'from acts.act2_context import print_shipping_demo; print_shipping_demo()'"

# ======================= container: 3. Agent Harness — Act 3 =======================
step_c 30-act3-standard 'python cli.py --act 3 --scenario standard'                      # README.md:364 (live)
step_c 31-act3-blocked 'python cli.py --act 3'                                           # README.md:376 (live)
step_c 32-act3-pa-shipping 'python cli.py --act 3 --scenario pa-shipping'                # README.md:379 (live)
ctstep container 33-act3-manager-approval 'decline: $' 'approve' \
  'python cli.py --act 3 --fixture --scenario manager-approval'                          # README.md:407, typed: approve
ctstep container 34-x-act3-manager-decline 'decline: $' 'decline' \
  'python cli.py --act 3 --fixture --scenario manager-approval'                          # extra: the same, typed: decline
step_c 35-act3-out-of-stock 'python cli.py --act 3 --fixture --scenario out-of-stock'    # README.md:415 (offline)
# extras: the shipping lesson's two scenarios with scripted proposals (README.md:401: "--fixture remains available for
# offline regression tests"): the same submitted cart, the same validator; fixtures skip the review-only intake
step_c 36-x-act3-pa-shipping-fixture 'python cli.py --act 3 --fixture --scenario pa-shipping'
step_c 37-x-act3-blocked-fixture 'python cli.py --act 3 --fixture --scenario pa-shipping-blocked'

# ======================= container: 3. Agent Harness — Act 4 =======================
step_c 40-act4 'python cli.py --act 4'                                                   # README.md:457 (live)
step_c 41-act4-compaction 'python cli.py --act 4 --fixture --demo-compaction --vendor-document malicious --email-decision decline'  # :476
step_c 42-x-act4-fixture-approve 'python cli.py --act 4 --fixture --email-decision approve'   # extra: the approved save (README.md:469)
step_c 43-act4-remember 'python cli.py --act 4 --customer shivas --remember-preference "Prefer nonalcoholic pairings today"'  # :484 (live)
step_c 44-act4-shivas 'python cli.py --act 4 --customer shivas'                          # README.md:485 (live)
step_c 45-x-memory-db "python -c 'import json, sqlite3; [print(c, json.loads(v)) for c, v in sqlite3.connect(\"outputs/customer_memory.sqlite\").execute(\"SELECT customer_id, value FROM preferences\")]'"

# ======================= container: 4. Skills — Act 5 =======================
step_c 50-act5 'python cli.py --act 5'                                                   # README.md:542 (live)
step_c 51-act5-stock-question 'python cli.py --act 5 --fixture --scenario stock-question'  # README.md:552 (offline)
step_c 52-act5-approve 'python cli.py --act 5 --fixture --email-decision approve'        # README.md:560 (offline)
R52=$(runid container/52-act5-approve.txt 'run')
step_c 53-x-saved-html "ls -la outputs/$R52/; sed -n 1,60p outputs/$R52/vendor-email-*.html"
step_c 54-x-act5-tasting-plan 'python cli.py --act 5 --fixture --scenario tasting-plan'   # extra: README.md:639 (Colab cell 47)

# ======================= container: 5. Agent Systems — Act 6 =======================
step_c 60-act6 'python cli.py --act 6 --scenario standard'                               # README.md:634 (live)
step_c 61-act6-two-orders 'python cli.py --act 6 --fixture --scenario two-orders --manager-decision approve'  # :648
step_c 62-x-act6-fixture 'python cli.py --act 6 --fixture'                                # extra: the CLI form of README.md:622

# ======================= container: 6. Evaluation =======================
step_c 70-list-runs 'python cli.py --list-runs'                                          # README.md:675
R33=$(runid container/33-act3-manager-approval.txt 'run')
step_c 71-inspect-run "python cli.py --inspect-run $R33"                                 # README.md:681, RUN_ID = the run of 33
step_c 72-x-inspect-run-literal 'python cli.py --inspect-run RUN_ID'                    # extra: the placeholder typed as is
R10=$(sed '1d;$d' "$HERE/container/70-list-runs.txt" | "$PY" -I -c 'import json, sys; print(json.load(sys.stdin)[0]["run_id"])')
step_c 73-x-inspect-failed-run "python cli.py --inspect-run $R10"                        # extra: the first run, 10's live failure
step_c 74-evaluate-fixture 'python cli.py --act 2 --evaluate core --fixture --case standard --repeats 2 --label context-fixture-1'  # :691
step_c 75-report 'python cli.py --report context-fixture-1'                              # README.md:699
step_c 76-view-report 'python cli.py --view-report context-fixture-1'                    # README.md:705
step_c 77-view-report-html-output 'python cli.py --view-report context-fixture-1 --html-output outputs/my-report.html'  # :713
step_c 78-view-report-colab 'python cli.py --view-report COLAB_LABEL --db outputs/colab.sqlite'  # README.md:714, placeholders as written
step_c 79-x-ls-reports 'ls -la outputs/reports/ outputs/*.html'
step_c 80-evaluate-live-a 'python cli.py --act 2 --evaluate core --context enriched --case standard --case missing-details --repeats 2 --label context-live-a'  # :728 (live)
step_c 81-cp-prompt 'cp prompts/shop_assistant.md prompts/shop_assistant_v2.md'          # README.md:734
# extra: README.md:737 "Open the copy in your editor. Make one deliberate change" -- the capture appends one line
step_c 82-x-edit-prompt "printf '%s\\n' '' 'Keep the customer message under 120 words. Start it with two labeled lines: \"Price:\" (the tool-derived cheese subtotal) and \"Action status:\" (proposed, pending review, placed or blocked).' >> prompts/shop_assistant_v2.md"
step_c 83-x-diff-prompt 'diff -u prompts/shop_assistant.md prompts/shop_assistant_v2.md'   # extra (diff exits 1 when the files differ)
step_c 84-evaluate-live-b 'python cli.py --act 2 --evaluate core --context enriched --case standard --case missing-details --repeats 2 --label context-live-b --prompt-file prompts/shop_assistant_v2.md'  # :742 (live)
step_c 85-compare 'python cli.py --compare context-live-a context-live-b --json-output outputs/context-comparison.json'  # :748 (offline)
# extras: the same A/B with scripted responses (both batches complete), a reused label, and the scorecard's text
step_c 86-x-evaluate-fixture-b 'python cli.py --act 2 --evaluate core --fixture --case standard --repeats 2 --label context-fixture-2 --prompt-file prompts/shop_assistant_v2.md'
step_c 87-x-compare-fixture 'python cli.py --compare context-fixture-1 context-fixture-2'
step_c 88-x-label-exists 'python cli.py --act 2 --evaluate core --fixture --case standard --repeats 2 --label context-fixture-1'
# the visible text of an HTML page (tags removed, one block or table row per line), as a browser would show it
HTML_TEXT='import html, re, sys
h = sys.stdin.read()
h = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", h)
h = re.sub(r"(?is)<tr\b.*?</tr>", lambda m: re.sub(r"\s*\n\s*", " ", m.group(0)), h)
h = re.sub(r"(?i)<br\s*/?>|</(p|div|h[1-6]|li|tr|summary|pre|header|section|details|table|thead|tbody)>", "\n", h)
h = re.sub(r"(?i)</t[dh]>", " | ", h)
h = re.sub(r"(?i)</span>", " ", h)
for line in html.unescape(re.sub(r"<[^>]+>", "", h)).splitlines():
    line = " ".join(line.split()).strip(" |")
    if line:
        print(line)'
step_c 89-x-report-text "python -c '$HTML_TEXT' < outputs/reports/context-fixture-1.html"
# ======================= container: 7. Additional Resources =======================
step_c 90-help 'python cli.py --help'                                                    # README.md:795
step_c 91-x-outputs 'ls -la outputs/; du -sh outputs/'
# extra: README.md:88 render_run(DB_PATH, run_id) -- the chat view's HTML without IPython, for the run of 33, as text
step_c 92-x-render-run "python -c 'from formaggio.operations.chat_view import render_run; print(render_run(\"outputs/observability.sqlite\", \"$R33\"))' | python -c '$HTML_TEXT'"
session_end                                                                              # `exit`: the container is removed (--rm)

# ======================= laptop: after exit (extras) =======================
step laptop 13-x-ps-after-exit $REPO 'docker ps -a'
step laptop 14-x-outputs-on-host $REPO 'ls -la outputs/ outputs/reports/; git status --short; git status --short --ignored | grep outputs'
step laptop 15-x-image-rm $REPO 'docker image rm agent-harness'
rm -f "$SIG/up" "$SIG/stop"; rmdir "$SIG"
