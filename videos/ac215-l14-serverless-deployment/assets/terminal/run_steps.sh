#!/bin/bash
# Runs inside a capture environment (see capture.sh) as user `student`, recording each tutorial
# command's output to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# Segments, in README order (dlops-io/serverless-deployment README.md @ 46cc62f):
#   laptop-pre   "Before you begin" step 4 (clone, work from the repo root) + the Terminal setup
#                exports (README:75-81; `gcloud auth login` runs in the gcloud environment)
#   laptop-run1  Part 2.1 (README:244-255): the docker run, verbatim, on an empty engine (the
#                image is pulled), + page/port/process/image extras while it runs, then Ctrl+C
#   laptop-ca    capture-only: the same image re-tagged with the recording proxy's CA, so its
#                outbound translation call can pass the sandbox's TLS-intercepting proxy
#   laptop-run2  Part 2.1 again, verbatim, + the browser's requests made with curl (translate,
#                speech disabled, bad input), then Ctrl+C
#   laptop-port  extra: digest exercise E1 (PORT=9090 behind -p 8086:8080)
#   laptop-job   extra: Part 4's batch command run locally from the same image
#                (tutorial/app/README.md:212-216 --plan; the real batch failing honestly without
#                speech/credentials; the one-chip and arguments-without-command mistakes)
#   dev-pre      Part 3.3's machine: clone + uv (installer) + versions
#   dev-local    Part 3.3 (README:558-564): cd tutorial/app, uv sync --frozen, the serve command
#                verbatim + curl extras, then Ctrl+C; tutorial/app/README.md:22-26 offline checks
#   dev-function extra: Part 1's handler run locally by functions-framework (what Cloud Run's
#                function build configures), + the README's own curl --get (README:202-204)
#   gcloud-run   every gcloud box needs a signed-in account: the Terminal setup + Part 1's deploy
#                command stopping at the sign-in error; flag checks in `gcloud ... --help`; the
#                Part 4.5/4.6 commands (helper verbatim + --dry-run); docs/lifecycle.md plans
# Steps marked "extra" are not in the README; they are checks the video uses.
OUT=$1; SEG=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
cd ~

step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1; echo "[exit $?]"; } > "$OUT/$name.txt"
}
istep() {  # istep <name> <command> [<prompt regex | file:PATH> <typed line>]...   (in a terminal)
  local name=$1 cmd=$2; shift 2
  local args=()
  while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
  { echo "\$ $cmd"
    python3 "$HERE/ptyrun.py" --cols "${PTY_COLS:-100}" --rows "${PTY_ROWS:-40}" --timeout "${PTY_TIMEOUT:-900}" \
      "${args[@]}" -- bash -c "$cmd"
    echo "[exit $?]"; } > "$OUT/$name.txt"
}
hub_retry() {  # hub_retry step|istep <name> <args...>   (recording sandbox only: CAPTURE_HUB_WAIT set)
  # Docker Hub limits anonymous pulls per IP and the sandbox's egress IPs are shared: retry a step
  # that hit "toomanyrequests"; capture-only/hub-retries.txt counts the failed attempts.
  local fn=$1 name=$2 i
  for i in $(seq 40); do
    "$fn" "$name" "${@:3}"
    grep -q "toomanyrequests\|429 Too Many Requests" "$OUT/$name.txt" || return 0
    [ -n "$CAPTURE_HUB_WAIT" ] || return 0
    mkdir -p "$OUT/capture-only"
    echo "$name: attempt $i hit Docker Hub's rate limit, retrying in 30 s" >> "$OUT/capture-only/hub-retries.txt"
    sleep 30
  done
}
wait_http() {  # wait_http <url> <seconds>: quiet readiness probe (capture-only, not shown)
  local i; for i in $(seq "$2"); do curl -s -o /dev/null --max-time 5 "$1" && return 0; sleep 1; done; return 1
}
wait_tcp() {  # wait_tcp <port> <seconds>: quiet readiness probe that sends no HTTP request (capture-only;
  # a GET / on the function would itself call the translation provider)
  local i; for i in $(seq "$2"); do (exec 3<>"/dev/tcp/127.0.0.1/$1") 2>/dev/null && return 0; sleep 1; done; return 1
}
CTRLC=$'\x03'
IMAGE_REF=cgumb/ac215-translation-demo:lecture14-agent-platform-20261022
# README "Terminal setup" (README:75-81), the exports exactly as written (YOUR_PROJECT_ID is the
# README's placeholder and stays one: there is no project here). Exported in this shell too, so
# the later README commands that use them see the same values.
SETUP='export PROJECT_ID=YOUR_PROJECT_ID
export REGION=northamerica-northeast2
export IMAGE=cgumb/ac215-translation-demo:lecture14-agent-platform-20261022
export WEB_SERVICE=translation-demo
export JOB_NAME=translation-audio
export WEB_EMAIL="translation-demo-runtime@${PROJECT_ID}.iam.gserviceaccount.com"
export JOB_EMAIL="translation-audio-job@${PROJECT_ID}.iam.gserviceaccount.com"'
eval "$SETUP"
REPO=https://github.com/dlops-io/serverless-deployment.git
DOCKER_RUN='docker run --rm -p 8086:8080 \
  cgumb/ac215-translation-demo:lecture14-agent-platform-20261022'
POST="curl -s -w '\n[HTTP %{http_code}]\n' -X POST -H 'Content-Type: application/json'"
JPOST="curl -s -X POST -H 'Content-Type: application/json'"   # + | python3 -m json.tool: the JSON as the page shows it (unescaped)

case $SEG in
laptop-pre)
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; git --version; docker images"   # extra
  # README "Before you begin" step 4 (README:38-41): "Clone or download the repository. Use the
  # repository root as the working directory for terminal examples." (no command spelled out)
  step 01-clone "git clone $REPO"
  cd serverless-deployment
  step 02-git-log "git log -1 --format='%H %ci %s'"     # extra: the commit the video follows
  step 03-ls "ls"                                       # extra: the repo root (2025 files + tutorial/)
  step 04-ls-tutorial "ls tutorial tutorial/function tutorial/app tutorial/app/translation_demo"   # extra
  # README "Terminal setup" (README:73-82) without `gcloud auth login` (see gcloud-run)
  step 05-terminal-setup "$SETUP
echo \"\$WEB_EMAIL\"; echo \"\$JOB_EMAIL\"; echo \"\$IMAGE\""
  ;;
laptop-run1)
  cd serverless-deployment
  # --- README Part 2.1 step 1 (README:244-249), verbatim, on an engine that has never pulled the
  # image. A second shell fetches what steps 2-4 look at, then drops the cue for Ctrl+C (step 4).
  CUE=/tmp/l14-cue-run1; rm -f $CUE
  ( wait_http http://localhost:8086/ 900; sleep 2
    step 11-curl-home "curl -s -i http://localhost:8086/ | grep -E 'HTTP/|Server:|Content-Type:|<title>|speech-button'"   # extra: step 2's page; Play audio disabled
    step 12-docker-ps "docker ps --format 'table {{.Image}}\t{{.Command}}\t{{.Ports}}'"   # extra: 0.0.0.0:8086->8080/tcp
    step 13-docker-top "docker top \$(docker ps -q) -o pid,user,args"    # extra: gunicorn is the container's process (os.execvp)
    step 14-curl-8080 "curl -sS http://localhost:8080/"                 # extra: the container port is not the laptop port
    step 15-image-digest "docker image inspect --format '{{index .RepoDigests 0}}' $IMAGE_REF"   # extra: README:1069's digest
    step 16-image-config "docker image inspect --format 'Os/Arch: {{.Os}}/{{.Architecture}}
User: {{.Config.User}}
WorkingDir: {{.Config.WorkingDir}}
ExposedPorts: {{.Config.ExposedPorts}}
Entrypoint: {{.Config.Entrypoint}}
Cmd: {{.Config.Cmd}}' $IMAGE_REF; docker image inspect --format '{{range .Config.Env}}{{println .}}{{end}}' $IMAGE_REF | grep -E '^(PORT|PYTHON)'"   # extra: what Cloud Run's command/arguments replace
    touch $CUE ) &
  BG=$!
  PTY_TIMEOUT=1200 hub_retry istep 10-docker-run "$DOCKER_RUN" "file:$CUE" "$CTRLC"
  wait $BG
  step 17-docker-ps-after "docker ps; docker images"    # extra: --rm removed the container; the image stays
  ;;
laptop-ca)
  # capture-only, NOT part of the tutorial (see ASSETS.md): the image's translation call goes out
  # through the sandbox's TLS-intercepting proxy, whose CA the image does not trust. Rebuild the
  # same image with that CA added and SSL_CERT_FILE set, re-tagged under the same name, so the
  # README's docker run stays verbatim.
  [ -n "$CAPTURE_CA" ] || exit 0
  mkdir -p "$OUT/capture-only"; d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"
  cat > "$d/Dockerfile" <<EOF
# capture-only: $IMAGE_REF + the recording proxy's CA (re-tagged under the same name)
FROM $IMAGE_REF
USER root
COPY capture-ca.crt /tmp/capture-ca.crt
RUN cat /etc/ssl/certs/ca-certificates.crt /tmp/capture-ca.crt > /etc/ssl/capture-bundle.crt && rm /tmp/capture-ca.crt
ENV SSL_CERT_FILE=/etc/ssl/capture-bundle.crt REQUESTS_CA_BUNDLE=/etc/ssl/capture-bundle.crt
USER app
EOF
  cp "$d/Dockerfile" "$OUT/capture-only/image-with-ca.Dockerfile"
  step capture-only/image-with-ca-build "docker build -t $IMAGE_REF $d"
  rm -rf "$d"
  ;;
laptop-run2)
  cd serverless-deployment
  # --- README Part 2.1 again, verbatim; the second shell sends what the page's Translate and
  # Play audio buttons send (index.html:76-80, 95-97): JSON POSTs, not Part 1's query string.
  CUE=/tmp/l14-cue-run2; rm -f $CUE
  ( wait_http http://localhost:8086/ 300; sleep 2
    step 21-translate-fr "$POST -d '{\"text\": \"Good afternoon everyone\", \"src\": \"en\", \"dest\": \"fr\"}' http://localhost:8086/api/translate"   # extra: step 3, the page's Translate
    step 22-translate-zh "$JPOST -d '{\"text\": \"Good afternoon everyone\", \"src\": \"en\", \"dest\": \"zh-cn\"}' http://localhost:8086/api/translate | python3 -m json.tool --no-ensure-ascii"   # extra
    python3 -c 'import json; print(json.dumps({"text": open("tutorial/app/examples/passage.txt").read(), "src": "en", "dest": "fr"}))' > /tmp/passage.json   # capture-only: the JSON body
    step 23-translate-passage "$JPOST -d @/tmp/passage.json http://localhost:8086/api/translate | python3 -m json.tool --no-ensure-ascii"   # extra: Part 4's passage, through the web app
    step 24-speech-disabled "$POST -d '{\"text\": \"Bonjour à tous\", \"src\": \"en\", \"dest\": \"fr\"}' http://localhost:8086/api/speech"   # extra: step 4, Play audio disabled
    step 25-bad-language "$POST -d '{\"text\": \"hello\", \"src\": \"en\", \"dest\": \"xx\"}' http://localhost:8086/api/translate"   # extra: validate() -> 400
    step 26-query-string "curl -s -w '\n[HTTP %{http_code}]\n' 'http://localhost:8086/api/translate?text=Good%20afternoon%20everyone&src=en&dest=fr' | tail -3"   # extra: Part 1's query string does not work here (POST route)
    touch $CUE ) &
  BG=$!
  PTY_TIMEOUT=600 istep 20-docker-run "$DOCKER_RUN" "file:$CUE" "$CTRLC"
  wait $BG
  ;;
laptop-port)
  # extra: digest exercise E1 -- the app listens on $PORT; -p maps the laptop's 8086 to 8080
  step 30-port-9090-run "docker run -d --name port-demo --rm -e PORT=9090 -p 8086:8080 $IMAGE_REF"
  sleep 6
  step 31-port-9090-curl "curl -sS http://localhost:8086/"
  step 32-port-9090-logs "docker logs port-demo 2>&1 | head -4"
  step 33-port-9090-stop "docker stop port-demo"
  step 34-port-fixed-run "docker run -d --name port-demo --rm -e PORT=9090 -p 8086:9090 $IMAGE_REF"
  sleep 6
  step 35-port-fixed-curl "curl -s http://localhost:8086/ | grep -o '<title>.*</title>'"
  step 36-port-fixed-stop "docker stop port-demo"
  ;;
laptop-job)
  cd serverless-deployment
  step 40-passage "cat tutorial/app/examples/passage.txt"            # extra: Part 4.1's input file
  # extra: tutorial/app/README.md:210-216 ("For a job, override its command"), with the public
  # image in place of the local build translation-demo:dev
  step 41-batch-plan "docker run --rm $IMAGE_REF \\
  python -m translation_demo batch --plan \\
  --text-file examples/passage.txt --src en --dest fr \\
  --output-uri gs://YOUR_OUTPUT_BUCKET/fresh-run-prefix"
  # extra: without --plan the batch really runs: translation succeeds, then speech stops it
  # (no ENABLE_SPEECH, as in Part 2) -> "Batch failed", exit 1 (__main__.py:58-61)
  step 42-batch-no-speech "docker run --rm $IMAGE_REF \\
  python -m translation_demo batch \\
  --text-file examples/passage.txt --src en --dest fr \\
  --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/"
  # extra: with the job's three variables but no Google identity (no attached account): ADC fails
  step 43-batch-no-identity "docker run --rm -e ENABLE_SPEECH=true -e GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID -e GOOGLE_CLOUD_LOCATION=us-central1 $IMAGE_REF \\
  python -m translation_demo batch \\
  --text-file examples/passage.txt --src en --dest fr \\
  --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/"
  # extra: README:750-753 "Do not paste the whole block into one argument field": the whole
  # argument list as ONE argv element after `python`
  step 44-one-chip "docker run --rm $IMAGE_REF python '-m translation_demo batch --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage.txt --src en --dest fr --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/'"
  # extra: arguments without the command `python` (Docker's analogue: arguments after the image
  # replace CMD; this image has no ENTRYPOINT, so "-m" becomes the program)
  step 45-args-without-command "docker run --rm $IMAGE_REF -m translation_demo batch --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage.txt --src en --dest fr --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/"
  # extra: a bad URI is an argparse error (exit 2), before any work
  step 46-bad-uri "docker run --rm $IMAGE_REF python -m translation_demo batch --input-uri YOUR_INPUT_BUCKET/run-001/passage.txt --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/"
  step 47-batch-help "docker run --rm $IMAGE_REF python -m translation_demo batch --help"   # extra
  step 48-docker-images "docker images; docker ps -a"                # extra: nothing left running
  ;;
dev-pre)
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; . /etc/os-release; echo \$PRETTY_NAME; python3 --version; git --version; which uv; echo which-uv-exit:\$?"   # extra
  step 01-clone "git clone $REPO"
  cd serverless-deployment
  step 02-git-log "git log -1 --format='%H %ci %s'"     # extra
  # README:556 "With uv installed" (the README links uv's docs; this is uv's documented installer)
  step 03-uv-install "curl -LsSf https://astral.sh/uv/install.sh | sh"   # extra
  step 04-uv-version "source \$HOME/.local/bin/env; uv --version; which uv"   # extra
  ;;
dev-local)
  source "$HOME/.local/bin/env"
  cd serverless-deployment
  # --- README Part 3.3 (README:558-564). The impersonated ADC login before it (README:547-548)
  # needs a Google account: not here, so the speech call fails with the app's own message.
  step 10-cd-uv-sync "cd tutorial/app
uv sync --frozen"
  cd tutorial/app
  CUE=/tmp/l14-cue-dev; rm -f $CUE
  ( wait_http http://localhost:8086/ 300; sleep 2
    step 12-curl-home "curl -s http://localhost:8086/ | grep -E '<title>|speech-button'"   # extra: Play audio enabled by ENABLE_SPEECH=true
    step 13-translate "$POST -d '{\"text\": \"Good afternoon everyone\", \"src\": \"en\", \"dest\": \"fr\"}' http://localhost:8086/api/translate"   # extra
    step 14-speech-no-adc "$POST -d '{\"text\": \"Bonjour à tous\", \"src\": \"en\", \"dest\": \"fr\"}' http://localhost:8086/api/speech"   # extra: no ADC here -> 503
    touch $CUE ) &
  BG=$!
  PTY_TIMEOUT=600 istep 11-uv-run-serve 'ENABLE_SPEECH=true GOOGLE_CLOUD_PROJECT="$PROJECT_ID" \
  GOOGLE_CLOUD_LOCATION=us-central1 PORT=8086 \
  uv run python -m translation_demo serve' "file:$CUE" "$CTRLC"
  wait $BG
  # extra: the application guide's offline checks (tutorial/app/README.md:22-26)
  step 15-unittest "uv run python -m unittest discover -s tests -v"
  step 16-batch-plan "uv run python -m translation_demo batch --plan \\
  --text-file examples/passage.txt --src en --dest fr \\
  --output-uri gs://YOUR_OUTPUT_BUCKET/fresh-run-prefix"
  step 17-uv-tree "uv tree --depth 1"                    # extra: the pinned direct dependencies
  step 18-cd-back "cd ../..; pwd" ;;                     # README:567 "Run cd ../.. when you return"
dev-function)
  cd serverless-deployment
  # extra: what the function build installs and starts (README:212-216), on this machine:
  # the two requirements, then functions-framework --target hello_http on $PORT (8080).
  step 20-function-files "cat tutorial/function/main.py; echo ---; cat tutorial/function/requirements.txt"
  step 21-function-venv "python3 -m venv ~/fn-venv && ~/fn-venv/bin/pip install -q -r tutorial/function/requirements.txt && ~/fn-venv/bin/pip list 2>/dev/null | grep -iE 'functions-framework|googletrans|flask|gunicorn|httpx'"
  CUE=/tmp/l14-cue-fn; rm -f $CUE
  ( wait_tcp 8080 120; sleep 2
    step 23-curl-default "curl -s -w '\n[HTTP %{http_code}]\n' http://localhost:8080/"   # README:158-159: no arguments -> English to Spanish
    istep 24-curl-readme "FUNCTION_URL=http://localhost:8080
curl --get \"\$FUNCTION_URL\" \\
  --data-urlencode 'text=Good afternoon everyone' \\
  --data-urlencode 'src=en' --data-urlencode 'dest=fr'"   # README:202-204, against the local stand-in
    istep 25-curl-query-fr "curl -s 'http://localhost:8080/?text=Good%20afternoon%20everyone&src=en&dest=fr'"   # README:163 query string
    istep 26-curl-el "curl -s 'http://localhost:8080/?text=Good%20afternoon%20everyone&src=en&dest=el'"    # README:166
    istep 27-curl-hi "curl -s 'http://localhost:8080/?text=Good%20afternoon%20everyone&src=en&dest=hi'"    # README:166
    istep 28-curl-zh "curl -s 'http://localhost:8080/?text=Good%20afternoon%20everyone&src=en&dest=zh-cn'" # README:166-167
    touch $CUE ) &
  BG=$!
  cd tutorial/function
  PTY_TIMEOUT=300 istep 22-functions-framework "~/fn-venv/bin/functions-framework --target hello_http" "file:$CUE" "$CTRLC"
  wait $BG
  # extra: digest gotcha #1 / exercise E4 -- the entry point does not match the def name
  step 29-wrong-target "timeout 20 ~/fn-venv/bin/functions-framework --target translate" ;;
gcloud-run)
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; gcloud version; python3 --version; which python python3"   # extra
  step 01-clone "git clone $REPO"
  cd serverless-deployment
  step 02-git-log "git log -1 --format='%H %ci %s'"     # extra
  # README "Terminal setup" (README:73-82): `gcloud auth login` opens a browser sign-in; with no
  # browser and no Google account here it cannot complete (ASSETS.md). What gcloud then knows:
  step 03-auth-list "gcloud auth list"                  # extra: no credentialed account
  step 04-terminal-setup "$SETUP
gcloud config list 2>&1"
  # README Part 1 "Equivalent gcloud commands" (README:195-198), verbatim: stops at sign-in
  step 05-function-deploy "gcloud run deploy translate-function \\
  --project=\"\$PROJECT_ID\" --region=\"\$REGION\" \\
  --source=tutorial/function --function=hello_http --base-image=python312 \\
  --no-invoker-iam-check"
  # extra: the README's flags, as this gcloud documents them
  step 06-help-run-deploy "gcloud run deploy --help | grep -E -A3 '^ +--(function|base-image|no-invoker-iam-check|source|concurrency|min-instances|max-instances)\b' | grep -v '^--$' | head -60"
  step 07-help-jobs-create "gcloud run jobs create --help | grep -E -A3 '^ +--(command|args|tasks|max-retries|task-timeout)\b' | grep -v '^--$' | head -50"
  step 08-help-jobs-execute "gcloud run jobs execute --help | grep -E -A4 '^ +--(args|wait)\b' | grep -v '^--$' | head -30"
  # README Part 4.5 (README:921-934): bucket variables + upload, verbatim
  export INPUT_BUCKET=YOUR_INPUT_BUCKET OUTPUT_BUCKET=YOUR_OUTPUT_BUCKET
  cp tutorial/app/examples/passage.txt ./passage.txt   # capture-only: "Save a new short UTF-8 passage as passage.txt"
  step 09-upload "export INPUT_BUCKET=YOUR_INPUT_BUCKET
export OUTPUT_BUCKET=YOUR_OUTPUT_BUCKET
gcloud storage cp ./passage.txt \"gs://\$INPUT_BUCKET/run-002/passage.txt\" \\
  --project=\"\$PROJECT_ID\""
  # README Part 4.6 (README:975-978), verbatim: the helper prints its first command, gcloud
  # fails at sign-in, the helper stops before the later steps
  step 10-helper "python tutorial/run_job.py ./passage.txt \\
  --project=\"\$PROJECT_ID\" --region=\"\$REGION\" --job=\"\$JOB_NAME\" \\
  --input-bucket=\"\$INPUT_BUCKET\" --output-bucket=\"\$OUTPUT_BUCKET\" \\
  --src=en --dest=fr --download-dir=./results"
  # README:1000 "--dry-run prints commands without uploads, executions, or local file writes"
  step 11-helper-dry-run "python tutorial/run_job.py ./passage.txt \\
  --project=\"\$PROJECT_ID\" --region=\"\$REGION\" --job=\"\$JOB_NAME\" \\
  --input-bucket=\"\$INPUT_BUCKET\" --output-bucket=\"\$OUTPUT_BUCKET\" \\
  --src=en --dest=fr --download-dir=./results --dry-run"
  step 12-helper-help "python tutorial/run_job.py --help"          # README:1002
  step 13-helper-gs-prefix "python tutorial/run_job.py ./passage.txt --project=\"\$PROJECT_ID\" --input-bucket=\"gs://\$INPUT_BUCKET\" --output-bucket=\"\$OUTPUT_BUCKET\" --dry-run"   # extra: README:1002 "without gs://"
  step 14-ls-results "ls -la; ls results 2>&1"          # extra: dry-run wrote nothing
  # docs/lifecycle.md (README:1060-1064, optional): both helpers print a plan by default
  step 15-spin-up-plan "python tutorial/spin_up.py \\
  --project=YOUR_PROJECT_ID \\
  --prefix=lecture14-demo \\
  --manifest=./local-state/lecture14-demo.json"
  step 16-tear-down-plan "python tutorial/tear_down.py \\
  --project=YOUR_PROJECT_ID \\
  --manifest=./local-state/lecture14-demo.json \\
  --delete-objects"
  step 17-helper-tests "python -m unittest discover -s tutorial/tests -v"   # docs/lifecycle.md's offline tests
  # extra: gcloud (and the lifecycle scripts) reject the literal placeholder YOUR_PROJECT_ID as a
  # project ID before anything else. With a lowercase stand-in in valid project-ID format (still a
  # placeholder, not a project), the same commands get one step further: to the missing sign-in.
  export PROJECT_ID=your-project-id
  step 18-function-deploy-signin "export PROJECT_ID=your-project-id
gcloud run deploy translate-function \\
  --project=\"\$PROJECT_ID\" --region=\"\$REGION\" \\
  --source=tutorial/function --function=hello_http --base-image=python312 \\
  --no-invoker-iam-check"
  step 19-helper-signin "export PROJECT_ID=your-project-id
python tutorial/run_job.py ./passage.txt \\
  --project=\"\$PROJECT_ID\" --region=\"\$REGION\" --job=\"\$JOB_NAME\" \\
  --input-bucket=\"\$INPUT_BUCKET\" --output-bucket=\"\$OUTPUT_BUCKET\" \\
  --src=en --dest=fr --download-dir=./results"
  step 20-spin-up-plan "python tutorial/spin_up.py \\
  --project=your-project-id \\
  --prefix=lecture14-demo \\
  --manifest=./local-state/lecture14-demo.json"
  step 21-tear-down-plan "python tutorial/tear_down.py \\
  --project=your-project-id \\
  --manifest=./local-state/lecture14-demo.json \\
  --delete-objects"
  step 22-ls-after "ls -a; ls local-state results 2>&1"   # extra: plans and the failed helper wrote nothing
  ;;
*) echo "unknown segment $SEG" >&2; exit 2 ;;
esac
