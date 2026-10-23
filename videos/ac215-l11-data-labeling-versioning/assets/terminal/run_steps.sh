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
  wait_http http://localhost:8080/health 240 || true
  step 12-docker-logs "docker logs data-label-studio 2>&1 | tail -n 40"   # extra: digest A6 checkpoint (first start migrates the database)
  step 13-ls-volume "ls -la docker-volumes docker-volumes/label-studio"   # extra: Label Studio's data folder on the host (git-ignored)
  ;;
*)
  echo "run_steps.sh: unknown segment $SEG" >&2; exit 2 ;;
esac
