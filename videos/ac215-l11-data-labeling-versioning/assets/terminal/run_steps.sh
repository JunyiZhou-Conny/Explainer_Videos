#!/bin/bash
# Runs inside the fresh capture container ("laptop" or "colab", see capture.sh) as user `student`,
# recording each tutorial command's output to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# Segments, README order (Part A = data-labeling README @ 03c3e27; Part B = data-versioning README
# @ b240b1a, the course-map pin, with its starter branch data-versioning-ac215 @ 23762e4; route T =
# the data-versioning README as it reads today @ 2515e5e, which clones `main` instead):
#   pre     Part A prerequisites: clone, pin check, secrets/ next to the repo (placeholder key),
#           the dataset zip, + the capture-only base images
#   ls1     "Run Label Studio Container": sh docker-shell.sh, docker container ls, readiness
#   ls2     "Setup Label Studio" without a browser: HTTP status, login, token, project, the GCS
#           "Check Connection" (honest failure), API stand-ins for Sync + one annotation
#   cli     "Enable CORS": bucket-name edit, sh docker-shell-CLI.sh, cli.py -c / -m (honest
#           DefaultCredentialsError: NO GCP credentials here), cli.py -p / -t against the live server
#   cmp     "Extra: docker-compose": stop, sh docker-shell-compose.sh (+ the documented fixes)
#   aclean  Part A "Docker Cleanup"
#   b-pre   Part B step 1: docker cleanup, clone the starter (SSH, then HTTPS), new repo, first commit
#   b-build Part B steps 2-3: secrets, docker-shell.sh edit, sh docker-shell.sh (starter build fails
#           at google-cloud-sdk = digest gotcha #1), the one-line fix, the container's entrypoint
#   b-v20   Part B step 4 inside the container: dvc init, remote add, add, push (honest failure)
#   b-git20 Part B step 4 on the host: git status/add/commit/tag/push
#   b-v21   "Create an updated dataset version": dvc add, dvc push (inside)
#   b-git21 ... git status/add/commit/tag/push (host)
#   b-up    extras: the class repo's own tags and pointer files, for comparison
#   t-repo  route T: today's README (clone -b main ...) up to the first push
#   t-dvc   route T: sh docker-shell.sh + dvc init / remote add on a clone of main
#   bclean  Part B "Docker Cleanup"
#   colab   (colab machine) the notebook's dvc cells, signed out
# Steps marked "extra" are not in the README; they are checks the video uses.
OUT=$1; SEG=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
cd ~

step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1; echo "[exit $?]"; } > "$OUT/$name.txt"
}
istep() {  # istep <name> <command> [<prompt regex> <typed line>]...   (in a terminal, typed)
  local name=$1 cmd=$2; shift 2
  local args=()
  while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
  { echo "\$ $cmd"
    python3 "$HERE/ptyrun.py" --cols "${PTY_COLS:-80}" --rows "${PTY_ROWS:-24}" --timeout "${PTY_TIMEOUT:-900}" \
      "${args[@]}" -- bash -c "$cmd"
    echo "[exit $?]"; } > "$OUT/$name.txt"
}
hub_retry() {  # hub_retry step|istep <name> <args...>   (recording sandbox only: CAPTURE_HUB_WAIT set)
  # Docker Hub limits anonymous pulls per IP and the sandbox's egress IPs are shared, so a pull can
  # fail with "toomanyrequests" / "429 Too Many Requests" for reasons that have nothing to do with
  # the tutorial. Run the step again until it gets through; the file keeps the run that did,
  # capture-only/hub-retries.txt counts the failed attempts.
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
capture_only_bases() {  # recording sandbox only (CAPTURE_CA set); see ASSETS.md, "capture-only"
  # The tutorial's builds need TLS, and the sandbox's TLS is re-signed by its proxy; the proxy also
  # refuses plain-http requests. The two base images the repos' Dockerfiles use are rebuilt with
  # that proxy's CA, https apt sources, and an apt hook that turns the gcsfuse repo line the
  # data-versioning Dockerfile writes (http://packages.cloud.google.com) into https before each
  # `apt-get update`; they are re-tagged under the same names, so every tutorial build runs unchanged.
  [ -n "$CAPTURE_CA" ] || return 0
  local d v; d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"
  mkdir -p "$OUT/capture-only"
  for v in 3.12 3.11; do
    cat > "$d/Dockerfile" <<EOF
# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through a
# TLS-intercepting proxy that refuses plain http. Same python:$v-slim-bookworm plus that proxy's CA,
# https apt sources, an apt hook that upgrades packages.cloud.google.com to https before each
# update, and the CA env vars, re-tagged under the same name so the tutorial Dockerfiles build
# unchanged.
FROM python:$v-slim-bookworm
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \\
 && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources \\
 && echo 'APT::Update::Pre-Invoke { "sed -i s,http://packages.cloud.google.com,https://packages.cloud.google.com,g /etc/apt/sources.list.d/*.list 2>/dev/null || true"; };' > /etc/apt/apt.conf.d/99capture-https
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \\
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \\
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \\
    UV_NATIVE_TLS=1
EOF
    cp "$d/Dockerfile" "$OUT/capture-only/python$v-base.Dockerfile"
    hub_retry step capture-only/python$v-base-build "docker build -t python:$v-slim-bookworm $d"
  done
  rm -rf "$d"
}
wait_http() {  # wait_http <url> <seconds>: quiet readiness probe (capture-only, not shown)
  local i; for i in $(seq "$2"); do curl -s -o /dev/null --max-time 5 "$1" && return 0; sleep 1; done; return 1
}
TOKEN=student-demo-token-not-a-secret   # capture-only Label Studio API token (see ASSETS.md)
AUTH="Authorization: Token $TOKEN"
CTRLC=$'\x03'

case $SEG in
pre)
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; docker compose version; git --version"   # extra
  # --- data-labeling README "Prerequisites": "Cloned this repository ... https://github.com/dlops-io/data-labeling" (README:14)
  step 01-clone "git clone https://github.com/dlops-io/data-labeling"
  cd data-labeling
  step 02-git-log "git log -1 --format='%H %ci'"          # extra: the commit the video uses
  step 03-ls "ls -la"                                     # extra: the repo's top level
  cd ~
  # --- README "Create a local secrets folder" (README:31-40): "At the same level as the
  # data-labeling folder create a folder called secrets". The README shows the tree, not a command.
  step 04-mkdir-secrets "mkdir secrets"
  # --- README "Setup GCP Service Account" (README:42-50): console clicks (illustration, see
  # ASSETS.md). There is NO real key here: an obviously invalid placeholder stands in so the folder
  # structure can be shown (ASSETS.md, capture-only).
  mkdir -p "$OUT/capture-only"
  cat > secrets/data-service-account.json <<'EOF'
{
  "type": "service_account",
  "project_id": "your-gcp-project",
  "private_key_id": "0000000000000000000000000000000000000000",
  "private_key": "-----BEGIN PRIVATE KEY-----\nPLACEHOLDER-THIS-IS-NOT-A-REAL-KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "data-service-account@your-gcp-project.iam.gserviceaccount.com",
  "client_id": "000000000000000000000",
  "token_uri": "https://oauth2.googleapis.com/token"
}
EOF
  cp secrets/data-service-account.json "$OUT/capture-only/placeholder-key.json"
  step 05-tree "tree -L 1 ."                              # extra: README:37-40 folder structure
  step 06-ls-secrets "ls -la secrets"                     # extra: digest A2 checkpoint
  # --- README "Download data" (README:62-65): a browser download of the link, then "Extract the
  # zip file". curl downloads the same URL; unzip is the extraction.
  step 07-download-zip "curl -sSLO https://github.com/dlops-io/datasets/releases/download/v4.0/cheeses_unlabeled.zip && ls -l cheeses_unlabeled.zip"
  step 08-unzip "unzip cheeses_unlabeled.zip"
  step 09-ls-images "ls cheeses_unlabeled; ls cheeses_unlabeled | wc -l; ls -a __MACOSX/cheeses_unlabeled | head -5; ls -A __MACOSX/cheeses_unlabeled | wc -l"   # extra: 21 images + 21 macOS resource forks (digest gotcha #22)
  step 09b-md5-images "md5sum cheeses_unlabeled/Image_1.jpg cheeses_unlabeled/Image_2.jpg cheeses_unlabeled/Image_3.jpg cheeses_unlabeled/Image_4.jpg cheeses_unlabeled/Image_5.jpg; wc -c cheeses_unlabeled/Image_1.jpg cheeses_unlabeled/Image_2.jpg cheeses_unlabeled/Image_3.jpg cheeses_unlabeled/Image_4.jpg cheeses_unlabeled/Image_5.jpg"   # extra: the fingerprints DVC will compute (digest §3.5)
  capture_only_bases
  ;;
ls1)
  cd data-labeling
  # capture-only: the instructor's e-mail in the login env vars is replaced by a neutral stand-in,
  # and a fixed, obviously fake API token is added, so no real address and no real-looking token
  # reaches a capture (ASSETS.md, capture-only deviations). The password stays the README's.
  mkdir -p "$OUT/capture-only"
  if grep -q 'pavlos@seas.harvard.edu' docker-shell.sh; then
    sed -i -e 's|pavlos@seas.harvard.edu|student@example.com|' \
      -e "s|^  -e LABEL_STUDIO_PASSWORD=\"awesome\" \\\\$|&\n  -e LABEL_STUDIO_USER_TOKEN=\"$TOKEN\" \\\\|" docker-shell.sh
    sed -i -e 's|pavlos@seas.harvard.edu|student@example.com|' \
      -e "s|^            LABEL_STUDIO_PASSWORD: \"awesome\"$|&\n            LABEL_STUDIO_USER_TOKEN: \"$TOKEN\"|" docker-compose.yml
    git diff --stat > "$OUT/capture-only/login-standin.diff"; git diff | sed 's/^\(-.*\)pavlos@seas\.harvard\.edu/\1<instructor e-mail>/' >> "$OUT/capture-only/login-standin.diff"
  fi
  # --- README "Run docker-shell.sh" (README:82-89): sh docker-shell.sh
  hub_retry step 10-docker-shell "sh docker-shell.sh"
  # --- README:91 "open another terminal and run docker container ls"
  step 11-docker-container-ls "docker container ls"
  sleep 25
  step 12-docker-container-ls-a "docker container ls -a"   # extra: on a Linux engine the container has already exited
  step 13-docker-logs "docker logs data-label-studio 2>&1 | tail -n 40"   # extra: digest A6 checkpoint -> digest gotcha #12, live
  step 14-ls-volume "ls -la docker-volumes docker-volumes/label-studio"   # extra: Docker created the bind-mount source as root
  step 15-ls-uid "docker run --rm --entrypoint id heartexlabs/label-studio:latest"   # extra: digest gotcha #12's check -- the image runs as uid 1001
  # --- digest gotcha #12's fix (extra; Linux hosts only -- Docker Desktop on macOS does not hit this)
  step 16-fix-volume-perms "sudo chown -R 1001 docker-volumes/label-studio && ls -la docker-volumes"
  # --- README:87 again: the script removes the exited container and starts a fresh one
  step 17-docker-shell-again "sh docker-shell.sh"
  wait_http http://localhost:8080/health 300 || true
  step 18-docker-container-ls "docker container ls"       # README:91 checkpoint, now Up
  step 19-docker-logs "docker logs data-label-studio 2>&1 | grep -v '^\s*$' | tail -n 25"   # extra: the server is up
  ;;
ls2)
  # --- README "Setup Label Studio" (README:102-147) happens in a browser. Without one, the same
  # server is driven over HTTP with the browser's own session (cookie + CSRF header): every call
  # below is one the UI makes when you click (all extra; the UI itself is drawn as an
  # illustration, see ASSETS.md).
  step 20-curl-health "curl -s http://localhost:8080/health"
  step 21-curl-root "curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' http://localhost:8080/"   # README:108 'go to http://localhost:8080/'
  step 22-curl-login-page "curl -s -o /tmp/ls-login.html -w '%{http_code} %{content_type}\n' http://localhost:8080/user/login/ && grep -o '<title>[^<]*</title>' /tmp/ls-login.html | head -1"
  # README:109 "Login with <e-mail> / awesome": the account the env vars created (stand-in e-mail, see ASSETS.md)
  step 23-login "rm -f /tmp/ls.cookies; curl -s -c /tmp/ls.cookies -o /dev/null http://localhost:8080/user/login/; CSRF=\$(awk '\$6==\"csrftoken\"{print \$7}' /tmp/ls.cookies); curl -s -b /tmp/ls.cookies -c /tmp/ls.cookies -o /dev/null -w '%{http_code} -> %{redirect_url}\n' -H 'Referer: http://localhost:8080/user/login/' --data-urlencode csrfmiddlewaretoken=\$CSRF --data-urlencode email=student@example.com --data-urlencode password=awesome http://localhost:8080/user/login/"
  export LS_CSRF=$(awk '$6=="csrftoken"{print $7}' /tmp/ls.cookies)   # the session's CSRF token (rotated at login)
  S='-b /tmp/ls.cookies -H "X-CSRFToken: $LS_CSRF" -H "Referer: http://localhost:8080/"'
  step 24-whoami "curl -s -b /tmp/ls.cookies http://localhost:8080/api/current-user/whoami | python3 -m json.tool | head -12"
  # the token side of the API (digest gotcha #11): no token -> refused; /api/version is open
  step 25-api-no-token "curl -s -w '\nHTTP %{http_code}\n' http://localhost:8080/api/projects"
  step 26-api-version "curl -s -w '\nHTTP %{http_code}\n' http://localhost:8080/api/version"   # digest §5 open question: /api/version needs no token
  step 27-jwt-settings "curl -s -b /tmp/ls.cookies http://localhost:8080/api/jwt/settings"   # Organization > API token settings, as the UI reads them: legacy tokens OFF by default
  # README "Create Annotation Project" (README:104-115) through the UI's API: the Image
  # Classification template with the four cheese choices (stand-in for the clicks)
  mkdir -p ls-api
  cat > ls-api/project.json <<'EOF'
{
  "title": "Cheese labels",
  "label_config": "<View><Image name=\"image\" value=\"$image\"/><Choices name=\"choice\" toName=\"image\"><Choice value=\"brie\"/><Choice value=\"gouda\"/><Choice value=\"gruyere\"/><Choice value=\"parmigiano\"/></Choices></View>"
}
EOF
  step 28-create-project "cat ls-api/project.json; curl -s -w '\nHTTP %{http_code}\n' $S -H 'Content-Type: application/json' -d @ls-api/project.json http://localhost:8080/api/projects | python3 -c 'import sys; t=sys.stdin.read(); print(t[:700])'"
  PID=$(curl -s -b /tmp/ls.cookies http://localhost:8080/api/projects | python3 -c 'import sys, json; print(json.load(sys.stdin)["results"][0]["id"])')
  # README "Configure Cloud Storage" (README:117-147): the form's "Check Connection" button posts
  # to these validate endpoints. Honest result here: no key in /secrets (ASSETS.md).
  cat > ls-api/source-storage.json <<EOF
{"project": $PID, "title": "Cheese Images", "bucket": "your-bucket-placeholder", "prefix": "cheeses_unlabeled", "use_blob_urls": true, "presign": true}
EOF
  cat > ls-api/target-storage.json <<EOF
{"project": $PID, "title": "Cheese Images", "bucket": "your-bucket-placeholder", "prefix": "cheeses_labeled"}
EOF
  mkdir -p "$OUT/capture-only"
  if [ -f ~/secrets/data-service-account.json ]; then
    mv ~/secrets/data-service-account.json ~/placeholder-key-removed.json
    echo "ls2: moved the placeholder key out of ~/secrets so cloud steps show the documented missing-key errors" >> "$OUT/capture-only/placeholder-key-moves.txt"
  fi
  step 29-ls-secrets-in-container "docker exec data-label-studio ls -la /secrets"   # digest A8 'If it fails' check: no key there
  step 30-check-source-storage "cat ls-api/source-storage.json; curl -s -w '\nHTTP %{http_code}\n' $S -H 'Content-Type: application/json' -d @ls-api/source-storage.json http://localhost:8080/api/storages/gcs/validate"
  step 31-check-target-storage "cat ls-api/target-storage.json; curl -s -w '\nHTTP %{http_code}\n' $S -H 'Content-Type: application/json' -d @ls-api/target-storage.json http://localhost:8080/api/storages/export/gcs/validate"
  # stand-ins for "Sync Storage" + one click on "gouda" (the bucket cannot be listed here): three
  # tasks with the gs:// URIs a sync would create, and one annotation through the UI's API
  cat > ls-api/tasks.json <<'EOF'
[{"image": "gs://your-bucket-placeholder/cheeses_unlabeled/Image_1.jpg"},
 {"image": "gs://your-bucket-placeholder/cheeses_unlabeled/Image_2.jpg"},
 {"image": "gs://your-bucket-placeholder/cheeses_unlabeled/Image_3.jpg"}]
EOF
  cat > ls-api/annotation.json <<'EOF'
{"result": [{"from_name": "choice", "to_name": "image", "type": "choices", "value": {"choices": ["gouda"]}}]}
EOF
  step 32-import-tasks "cat ls-api/tasks.json; curl -s -w '\nHTTP %{http_code}\n' $S -H 'Content-Type: application/json' -d @ls-api/tasks.json http://localhost:8080/api/projects/$PID/import"
  TID=$(curl -s -b /tmp/ls.cookies "http://localhost:8080/api/tasks?project=$PID" | python3 -c '
import sys, json
d = json.load(sys.stdin)
t = d if isinstance(d, list) else (d.get("tasks") or d.get("results") or [])
print(min(x["id"] for x in t))')
  step 33-annotate "cat ls-api/annotation.json; curl -s -w '\nHTTP %{http_code}\n' $S -H 'Content-Type: application/json' -d @ls-api/annotation.json http://localhost:8080/api/tasks/$TID/annotations | python3 -c 'import sys; print(sys.stdin.read()[:900])'"
  ;;
cli)
  cd data-labeling
  export LS_CSRF=$(awk '$6=="csrftoken"{print $7}' /tmp/ls.cookies)   # the browser session from ls2
  # --- README "Enable CORS" (README:164): "Change the bucket name in docker-shell-CLI.sh" (sed is
  # the editor here; your-bucket-placeholder is the stand-in)
  step 40-edit-bucket "sed -i 's|GCS_BUCKET_NAME=\"cheese-app-data-demo\"|GCS_BUCKET_NAME=\"your-bucket-placeholder\"|' docker-shell-CLI.sh && sed -n '23,24p' docker-shell-CLI.sh"
  # --- README:165-168: run docker-shell-CLI.sh, then python cli.py -c and -m inside. Both need a
  # Google credential and fail honestly (no key; see ASSETS.md). Extras typed inside: the env, the
  # empty /secrets, and the two addresses of Label Studio (digest §3.4).
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=2400 hub_retry istep 41-docker-shell-CLI "sh docker-shell-CLI.sh" \
    ':/app\$ $' 'python cli.py -c' \
    ':/app\$ $' 'python cli.py -m' \
    ':/app\$ $' 'ls -la /secrets' \
    ':/app\$ $' 'echo $GCS_BUCKET_NAME $LABEL_STUDIO_URL' \
    ':/app\$ $' 'curl -s http://data-label-studio:8080/health' \
    ':/app\$ $' 'curl -sS http://localhost:8080/health' \
    ':/app\$ $' 'exit'
  # --- README "View Annotations using CLI" (README:189-199): python cli.py -p -k <token> and
  # -t -k <token>. First with Label Studio's defaults: legacy tokens are OFF (27-jwt-settings),
  # and cli.py's legacy Client sends "Authorization: Token <key>" (digest gotcha #11, live).
  # The token is the capture-only stand-in (ASSETS.md). Extras: the two ways to forget the token.
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1200 istep 42-cli-projects-401 "sh docker-shell-CLI.sh" \
    ':/app\$ $' "python cli.py -p -k $TOKEN" \
    ':/app\$ $' 'python cli.py -t' \
    ':/app\$ $' 'python cli.py -p -k' \
    ':/app\$ $' 'exit'
  # digest gotcha #11's first fix (extra): Organization > API Tokens Settings > enable legacy
  # tokens -- done with the UI's own call, as the logged-in admin
  step 43-enable-legacy-tokens "curl -s -w '\nHTTP %{http_code}\n' -b /tmp/ls.cookies -H \"X-CSRFToken: \$LS_CSRF\" -H 'Referer: http://localhost:8080/' -H 'Content-Type: application/json' -d '{\"api_tokens_enabled\": true, \"legacy_api_tokens_enabled\": true}' http://localhost:8080/api/jwt/settings"
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1200 istep 44-cli-projects-tasks "sh docker-shell-CLI.sh" \
    ':/app\$ $' "python cli.py -p -k $TOKEN" \
    ':/app\$ $' "python cli.py -t -k $TOKEN" \
    ':/app\$ $' 'exit'
  ;;
cmp)
  cd data-labeling
  # --- README "Extra: Using docker-compose" (README:214-229): stop the containers, then run
  # docker-shell-compose.sh. README:225/229 give `docker stop <name>` and `docker ps`.
  step 50-docker-stop "docker stop data-label-studio"
  step 51-docker-ps "docker ps"
  # the unmodified script: docker-compose (Compose v2's compatibility command) builds, then
  # compose tries to create data-label-studio -- but `docker stop` left the stopped container
  # behind (digest gotcha #6, live)
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1200 istep 52-docker-shell-compose "sh docker-shell-compose.sh"
  # digest gotcha #6's fix (extra)
  step 53-docker-rm "docker rm data-label-studio"
  # the same script again: compose starts Label Studio, then the CLI shell at once -- depends_on
  # does not wait until Label Studio is ready (digest §5), so the first cli.py call is refused.
  # Extras typed inside: the bucket name compose passes (digest errata #9), a wait loop.
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1200 istep 54-docker-shell-compose-run "sh docker-shell-compose.sh" \
    ':/app\$ $' 'echo $GCS_BUCKET_NAME' \
    ':/app\$ $' "python cli.py -p -k $TOKEN" \
    ':/app\$ $' 'until curl -s http://data-label-studio:8080/health; do sleep 2; done' \
    'UP"}.*:/app\$ $' "python cli.py -p -k $TOKEN" \
    ':/app\$ $' 'exit'
  step 55-docker-ps "docker ps"                           # extra: data-label-studio keeps running after the CLI exits (digest gotcha #8 note)
  ;;
aclean)
  cd data-labeling
  # --- README "Docker Cleanup" (README:239-246)
  step 60-docker-container-ls "docker container ls"
  step 61-docker-stop "docker stop data-label-studio"     # README:244 'Stop any container that is running'
  PTY_COLS=110 PTY_ROWS=30 istep 62-docker-system-prune "docker system prune" 'y/N\] $' 'y'
  step 63-docker-image-ls "docker image ls"
  step 64-volume-survives "sudo ls -la docker-volumes/label-studio"   # extra: prune removed the container, not the project data
  ;;
b-pre)
  # ===== Part B: data-versioning README @ b240b1a (the course-map pin; digest Part B) =====
  # --- README "Make sure we do not have any running containers..." (README:52-72)
  step 70-docker-container-ls "docker container ls"
  PTY_COLS=110 PTY_ROWS=30 istep 71-docker-system-prune "docker system prune" 'y/N\] $' 'y'
  step 72-docker-image-ls "docker image ls"
  # --- README "Clone the class repository" (README:76-84): the SSH command, then the HTTPS form
  # the tip offers. The recording sandbox has no SSH route to GitHub (ASSETS.md).
  step 73-clone-ssh "git clone -b data-versioning-ac215 git@github.com:dlops-io/data-versioning.git"
  step 74-clone-https "git clone -b data-versioning-ac215 https://github.com/dlops-io/data-versioning.git"
  cd data-versioning
  step 75-git-log "git log -1 --format='%H %ci'"          # extra: the starter commit (= digest pin 23762e4)
  # --- README:86-101
  step 76-rm-git "rm -rf .git"
  step 77-git-init "git init"
  step 78-ls-A "ls -A"                                    # extra: digest B2 checkpoint -- no .dvc/ folder
  # --- README "Create your own private GitHub repository" (README:103-126)
  step 79-git-branch-M "git branch -M main"
  step 80-git-remote-add "git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git"
  step 81-git-add "git add ."
  step 82-git-commit "git commit -m \"Initial commit\""
  step 83-git-push "git push -u origin main"
  ;;
b-build)
  # --- README "Add the secrets folder" (README:136-144): the folder next to data-versioning is
  # the same ~/secrets as Part A. The placeholder key goes back in for this one picture.
  mkdir -p "$OUT/capture-only"
  if [ -f ~/placeholder-key-removed.json ]; then
    mv ~/placeholder-key-removed.json ~/secrets/data-service-account.json
    echo "b-build: put the placeholder key back for the folder-structure step" >> "$OUT/capture-only/placeholder-key-moves.txt"
  fi
  step 84-tree "tree -L 2 -I 'cheeses_unlabeled|__MACOSX|ls-api|*.zip' ."   # extra: README:140-144 folder structure
  mv ~/secrets/data-service-account.json ~/placeholder-key-removed.json
  echo "b-build: moved the placeholder key out again before the DVC container (documented missing-key errors)" >> "$OUT/capture-only/placeholder-key-moves.txt"
  # --- README "Set up a GCP service account" (README:146-170) and "Create folders in your GCS
  # bucket" (README:174-187): console clicks, illustration (ASSETS.md)
  cd data-versioning
  # --- README "Configure the container parameters" (README:191-205): edit docker-shell.sh lines 7-9
  step 85-edit-docker-shell "sed -i -e 's|^export GCS_BUCKET_NAME=.*|export GCS_BUCKET_NAME=\"your-bucket-placeholder\"|' -e 's|^export GCP_PROJECT=.*|export GCP_PROJECT=\"your-gcp-project\"|' -e 's|^export GCP_ZONE=.*|export GCP_ZONE=\"us-central1-a\"|' docker-shell.sh && sed -n '5,10p' docker-shell.sh"
  # --- README "Run docker-shell.sh" (README:229-243): cd data-versioning; sh docker-shell.sh.
  # The starter's Dockerfile:36 still installs google-cloud-sdk (digest gotcha #1, live).
  hub_retry step 86-docker-shell-starter-fails "sh docker-shell.sh"
  # digest gotcha #1's fix (extra): the one line main changed in ebf09c8
  step 87-fix-dockerfile "sed -i '36s/google-cloud-sdk/google-cloud-cli/' Dockerfile && sed -n '36p' Dockerfile"
  # the same README command again: the build passes; the entrypoint's gcloud/gcsfuse/mount lines
  # need the key and the bucket, and fail honestly (no key here). Extras typed inside: what the
  # container sees.
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=3600 hub_retry istep 88-docker-shell "sh docker-shell.sh" \
    ':/app# $' 'ls -la cheese_dataset' \
    ':/app# $' 'which dvc' \
    ':/app# $' 'dvc --version' \
    ':/app# $' 'ls /mnt/gcs_data' \
    ':/app# $' 'exit'
  step 89-host-cheese-dataset "ls -la cheese_dataset"     # extra: the host side of the same folder
  ;;
b-v20)
  cd data-versioning
  # --- README "Create the first dataset version" (README:255-303), inside the container
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1800 istep 90-dvc-v20 "sh docker-shell.sh" \
    ':/app# $' 'dvc init' \
    ':/app# $' 'dvc remote add -d cheese_dataset gs://your-bucket-placeholder/dvc_store' \
    ':/app# $' 'cat .dvc/config' \
    ':/app# $' 'dvc add cheese_dataset' \
    ':/app# $' 'cat cheese_dataset.dvc' \
    ':/app# $' 'dvc push' \
    ':/app# $' 'exit'
  # capture-only stand-in for the bucket's images/ folder (no bucket can be mounted here): the
  # four photos the class's dataset_v20 was made of (digest §3.5) go into the folder DVC tracks.
  # The folder was created by the container's root, hence sudo.
  step 91-standin-images "sudo cp ../cheeses_unlabeled/Image_1.jpg ../cheeses_unlabeled/Image_2.jpg ../cheeses_unlabeled/Image_3.jpg ../cheeses_unlabeled/Image_4.jpg cheese_dataset/ && ls -la cheese_dataset"
  # the README's dvc add + dvc push again, now on four real images; extras: the pointer file, the
  # cache layout, and a push to a local stand-in remote (config.local, git-ignored) to show what
  # dvc push would upload
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1800 istep 92-dvc-add-push-v20 "sh docker-shell.sh" \
    ':/app# $' 'ls cheese_dataset' \
    ':/app# $' 'dvc add cheese_dataset' \
    ':/app# $' 'cat cheese_dataset.dvc' \
    ':/app# $' 'find .dvc/cache -type f | sort' \
    ':/app# $' 'dvc push' \
    ':/app# $' 'dvc remote add --local standin /app/.dvc/tmp/standin-remote' \
    ':/app# $' 'dvc push -r standin' \
    ':/app# $' 'exit'
  ;;
b-git20)
  cd data-versioning
  # --- README "Update Git to track the DVC metadata" (README:305-321), outside the container
  step 93-git-status "git status"
  step 94-git-add "git add ."
  step 95-git-commit "git commit -m \"Track initial cheese dataset with DVC\""
  step 96-git-tag "git tag -a dataset_v20 -m \"First version of cheese dataset\""
  step 97-git-push "git push --atomic origin main dataset_v20"
  step 98-git-log "git log --oneline --decorate"          # extra
  step 99-git-show-v20 "git show dataset_v20:cheese_dataset.dvc"   # extra: what the tag pins
  ;;
b-v21)
  cd data-versioning
  # --- README "Create an updated dataset version: dataset_v21" (README:330-369). Upload step:
  # capture-only stand-in again -- one more photo into the tracked folder
  step 100-standin-new-image "sudo cp ../cheeses_unlabeled/Image_5.jpg cheese_dataset/ && ls -la cheese_dataset"
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1800 istep 101-dvc-add-push-v21 "sh docker-shell.sh" \
    ':/app# $' 'ls cheese_dataset' \
    ':/app# $' 'dvc add cheese_dataset' \
    ':/app# $' 'cat cheese_dataset.dvc' \
    ':/app# $' 'dvc push' \
    ':/app# $' 'dvc push -r standin' \
    ':/app# $' 'exit'
  ;;
b-git21)
  cd data-versioning
  step 102-git-status "git status"
  step 103-git-add "git add ."
  step 104-git-commit "git commit -m \"Add images to cheese dataset\""
  step 105-git-tag "git tag -a dataset_v21 -m \"Updated cheese dataset with additional images\""
  step 106-git-push "git push --atomic origin main dataset_v21"
  step 107-git-diff "git diff HEAD~1 -- cheese_dataset.dvc"   # extra: digest B13 checkpoint
  step 108-git-log "git log --oneline --decorate"         # extra
  step 109-git-tag-n "git tag -n"                         # extra
  step 110-remote-add-again "git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git"   # extra: what README:372 warns about (the old ac215 README repeats it)
  # extra: time travel without Colab -- the tag's pointer file, then dvc checkout from the cache
  step 111-checkout-v20-pointer "git checkout dataset_v20 -- cheese_dataset.dvc && git status --short"
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1200 istep 112-dvc-checkout-v20 "sh docker-shell.sh" \
    ':/app# $' 'dvc checkout' \
    ':/app# $' 'ls cheese_dataset' \
    ':/app# $' 'exit'
  step 113-back-to-main "git checkout main -- cheese_dataset.dvc && git status --short"
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1200 istep 114-dvc-checkout-main "sh docker-shell.sh" \
    ':/app# $' 'dvc checkout' \
    ':/app# $' 'ls cheese_dataset' \
    ':/app# $' 'exit'
  ;;
b-up)
  # extras: the class repo's own tags and pointer files (digest §3.5, §3.6), and its bucket
  step 115-ls-remote-tags "git ls-remote --tags https://github.com/dlops-io/data-versioning"
  step 116-clone-class-repo "git clone -q https://github.com/dlops-io/data-versioning class-data-versioning && git -C class-data-versioning log -1 --format='%H %ci'"
  step 117-class-v20-v21 "git -C class-data-versioning show dataset_v20:cheese_dataset.dvc; echo ---; git -C class-data-versioning show dataset_v21:cheese_dataset.dvc"
  step 118-compare-v20 "diff <(git -C class-data-versioning show dataset_v20:cheese_dataset.dvc) <(git -C data-versioning show dataset_v20:cheese_dataset.dvc) && echo identical"
  step 119-class-bucket-anonymous "curl -s -w '\nHTTP %{http_code}\n' 'https://storage.googleapis.com/storage/v1/b/cheese-app-data-versioning/o?prefix=dvc_store/'"
  ;;
t-repo)
  # ===== route T: the data-versioning README as it reads today (@ 2515e5e, 2026-10-13) =====
  mkdir -p today/secrets && cd today
  # --- README:76-120 today: clone -b main (SSH, then the new HTTPS section), cd, cd, rm, init
  step 120-clone-ssh-main "git clone -b main git@github.com:dlops-io/data-versioning.git"
  step 121-clone-https-main "git clone -b main https://github.com/dlops-io/data-versioning.git"
  step 122-cd "cd data-versioning"                        # README:97
  cd data-versioning
  step 123-cd-again "cd data-versioning"                  # README:105, the second 'cd data-versioning'
  step 124-git-log "git log -1 --format='%H %ci'"         # extra: today's head of main
  step 125-rm-git "rm -rf .git"
  step 126-git-init "git init"
  step 127-ls-A "ls -A"                                   # extra: .dvc/ and cheese_dataset.dvc came with main
  # README:133-138 "Or, if you are using HTTPS, use this instead": the README's line carries a
  # teaching assistant's own GitHub user; YOUR_GITHUB_USERNAME stands in (ASSETS.md)
  step 128-remote-set-url "git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/data-versioning.git"
  step 129-git-branch-M "git branch -M main"
  step 130-git-remote-add "git remote add origin git@github.com:YOUR_GITHUB_USERNAME/data-versioning.git"
  step 131-git-add "git add ."
  step 132-git-commit "git commit -m \"Initial commit\""
  step 133-git-push "git push -u origin main"
  ;;
t-dvc)
  cd today/data-versioning
  step 134-edit-docker-shell "sed -i -e 's|^export GCS_BUCKET_NAME=.*|export GCS_BUCKET_NAME=\"your-bucket-placeholder\"|' -e 's|^export GCP_PROJECT=.*|export GCP_PROJECT=\"your-gcp-project\"|' -e 's|^export GCP_ZONE=.*|export GCP_ZONE=\"us-central1-a\"|' docker-shell.sh && sed -n '5,10p' docker-shell.sh"
  # README:256-268 + 288-328 today: sh docker-shell.sh, then dvc init / remote add / add / push
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=3600 hub_retry istep 135-docker-shell-dvc "sh docker-shell.sh" \
    ':/app# $' 'dvc init' \
    ':/app# $' 'dvc remote add -d cheese_dataset gs://your-bucket-placeholder/dvc_store' \
    ':/app# $' 'cat .dvc/config' \
    ':/app# $' 'cat cheese_dataset.dvc' \
    ':/app# $' 'dvc add cheese_dataset' \
    ':/app# $' 'dvc push' \
    ':/app# $' 'exit'
  ;;
bclean)
  # --- README "Docker Cleanup" (README:403-425 @ b240b1a; 427-449 today)
  step 140-docker-container-ls "docker container ls"
  PTY_COLS=110 PTY_ROWS=30 istep 141-docker-system-prune "docker system prune" 'y/N\] $' 'y'
  step 142-docker-image-ls "docker image ls"
  ;;
colab)
  # ===== the Colab notebook linked from README @ b240b1a (Drive id 1RRQ1SlHq5lKK76R8LoQdi5LjCnND3jTq),
  # code cells run as shell commands in a Python 3.12 container, signed out (cell 11,
  # auth.authenticate_user(), needs a browser sign-in and cannot run here)
  cd /content 2>/dev/null || { mkdir -p ~/content && cd ~/content; }
  step C00-env "date -u '+%Y-%m-%d %H:%M UTC'; python --version; git --version"   # extra
  step C07-pip-install "pip install dvc dvc-gs"
  step C07b-dvc-version "dvc --version"                    # extra
  step C13-dvc-list "dvc list -R https://github.com/dlops-io/data-versioning.git"
  step C15-dvc-get-v21 "rm -rf cheese_dataset; dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --rev dataset_v21"
  step C17-count "python -c 'import os; print(\"Number of items:\",len(os.listdir(\"cheese_dataset\")))'"
  step C19-dvc-get-v25-quiet "rm -rf cheese_dataset; dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --quiet --rev dataset_v25"
  step C20-count "python -c 'import os; print(\"Number of items:\",len(os.listdir(\"cheese_dataset\")))'"
  step C19b-dvc-get-v25-loud "dvc get https://github.com/dlops-io/data-versioning cheese_dataset --force --rev dataset_v25"   # extra: the same cell without --quiet (digest gotcha #13c)
  ;;
*)
  echo "run_steps.sh: unknown segment $SEG" >&2; exit 2 ;;
esac
