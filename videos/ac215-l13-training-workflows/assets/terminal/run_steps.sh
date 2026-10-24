#!/bin/bash
# Runs inside the fresh capture container ("laptop" or "colab", see capture.sh) as user `student`
# (colab: root), recording each tutorial command's output to its own file: "$ command", the output,
# "[exit N]". Usage: run_steps.sh <out_dir> <segment>
# Segments, in README order (dlops-io/model-training README @ b9aee1c, the course-map pin and the
# head of main on 2026-10-23):
#   pre     "Clone the github repository", "Create a local secrets folder" (placeholder key),
#           + the capture-only base images
#   cloud   extras for the console steps (no credentials needed): does the placeholder bucket exist,
#           does the README's bucket, are the prebuilt training images cli.sh names still served
#   wandb   "Get WandB Account API Key": export WANDB_KEY=... (an obviously fake placeholder)
#   bases   (capture-only) re-tag the base images alone
#   shell   "Run docker-shell.sh": edit lines 8-9, sh docker-shell.sh (fails at Dockerfile step 2:
#           bullseye-security's pool is gone), fix 1 (bookworm base), again (fails at google-cloud-sdk
#           = digest gotcha #20), fix 2, sh docker-shell.sh a third time + checks typed inside
#   pkg     "Run sh package-trainer.sh" inside the container (tar + gzip real; gsutil cp fails:
#           NO GCP credentials here)
#   job     "Create Jobs in Vertex AI": sh cli.sh inside the container (honest failure) + extras
#   mgpu    "OPTIONAL: Multi GPU Training": sh cli-multi-gpu.sh (honest failure)
#   clipy   extras: python cli.py (not in the README; digest B16), the console has no TensorFlow,
#           pip-installing the package on the console's Python 3.13 (digest gotcha #17)
#   nokey   extras: digest gotcha #1 (WANDB_KEY not exported) and #22 (a second docker-shell.sh)
#   vtx     capture-only stand-in for the first thing a Vertex job does: pip install the tarball in a
#           Python 3.10 container; then W&B's key check (task.py:153) offline
#   clean   extras: what is left on the laptop
#   colab   (colab machine) notebook B's `pip install wandb -U` + an offline check of its
#           `wandb.config = {...}` pattern (digest E14)
# Steps marked "extra" are not in the README; they are checks the video uses.
OUT=$1; SEG=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
umask 022   # a login shell's default (docker exec would otherwise run with umask 0000)
cd ~

step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1 | sed 's/\x1b\[[0-9;]*m//g'; echo "[exit ${PIPESTATUS[0]}]"; } > "$OUT/$name.txt"   # colours dropped, as in ptyrun.py
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
  # The tutorial's build needs TLS, and the sandbox's TLS is re-signed by its proxy; the proxy also
  # refuses plain-http requests. The base image of the repo's Dockerfile (python:3.13-slim-bullseye),
  # the bookworm base the build fix switches to, and the Vertex stand-in's python:3.10-slim-bookworm
  # are rebuilt with that proxy's CA, https
  # Debian sources and the CA env vars (incl. gcloud's custom-CA property), then re-tagged under the
  # same names, so the tutorial build runs unchanged.
  [ -n "$CAPTURE_CA" ] || return 0
  local d v; d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"
  mkdir -p "$OUT/capture-only"
  for v in 3.13-slim-bullseye 3.13-slim-bookworm 3.10-slim-bookworm; do
    cat > "$d/Dockerfile" <<EOF
# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through a
# TLS-intercepting proxy that refuses plain http. Same python:$v plus that proxy's CA, https Debian
# sources (bullseye: /etc/apt/sources.list; bookworm: debian.sources) and the CA env vars,
# re-tagged under the same name so the tutorial Dockerfile builds unchanged.
FROM python:$v
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \\
 && for f in /etc/apt/sources.list /etc/apt/sources.list.d/debian.sources; do \\
      [ -f "\$f" ] && sed -i -e 's|http://deb.debian.org|https://deb.debian.org|g' -e 's|http://security.debian.org|https://security.debian.org|g' "\$f"; \\
    done; true
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \\
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \\
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \\
    CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE=/etc/ssl/certs/ca-certificates.crt \\
    UV_NATIVE_TLS=1
EOF
    cp "$d/Dockerfile" "$OUT/capture-only/python$v-base.Dockerfile"
    hub_retry step capture-only/python$v-base-build "docker build -t python:$v $d"
  done
  rm -rf "$d"
}
PH_KEY=PLACEHOLDER_NOT_A_REAL_WANDB_KEY_0000000   # capture-only W&B key: obviously fake, 40 characters
P=':/app# $'                                       # the console container's root prompt

case $SEG in
pre)
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; git --version"   # extra
  # --- README "Clone the github repository" (README:16-17): "Clone or download from here"
  step 01-clone "git clone https://github.com/dlops-io/model-training"
  cd model-training
  step 02-git-log "git log -1 --format='%H %ci %s'"     # extra: the commit the video uses
  step 03-ls "ls -la"                                     # extra: the repo's top level
  cd ~
  # --- README "Create a local secrets folder" (README:50-58): "At the same level as the
  # model-training folder create a folder called secrets". The README shows the tree, not a command.
  step 04-mkdir-secrets "mkdir secrets"
  # --- README "Setup GCP Service Account" (README:60-64): console clicks (illustration, see
  # ASSETS.md). There is NO real key here: an obviously invalid placeholder stands in so the folder
  # structure can be shown (ASSETS.md, capture-only).
  mkdir -p "$OUT/capture-only"
  cat > secrets/model-trainer.json <<'EOF'
{
  "type": "service_account",
  "project_id": "your-gcp-project",
  "private_key_id": "0000000000000000000000000000000000000000",
  "private_key": "-----BEGIN PRIVATE KEY-----\nPLACEHOLDER-THIS-IS-NOT-A-REAL-KEY\n-----END PRIVATE KEY-----\n",
  "client_email": "model-trainer@your-gcp-project.iam.gserviceaccount.com",
  "client_id": "000000000000000000000",
  "token_uri": "https://oauth2.googleapis.com/token"
}
EOF
  cp secrets/model-trainer.json "$OUT/capture-only/placeholder-key.json"
  step 05-tree "tree -L 1 ."                              # extra: README:54-58 folder structure
  step 06-ls-secrets "ls -la secrets"                     # extra: the key's file name
  capture_only_bases
  ;;
cloud)
  # --- README "API's to enable", "Setup GPU Quotas", "Setup GCP Service Account", "Create GCS
  # Bucket" (README:19-71) are console clicks (illustration). Extras that need no credentials:
  # bucket names are global -- the placeholder used below must not exist, the README's one does.
  step 07-bucket-placeholder "curl -s -w 'HTTP %{http_code}\n' https://storage.googleapis.com/storage/v1/b/your-bucket-placeholder"   # extra
  step 08-bucket-readme "curl -s -w 'HTTP %{http_code}\n' https://storage.googleapis.com/storage/v1/b/cheese-app-trainer"   # extra (digest gotcha #18)
  # extra (digest §10 open question): are the prebuilt training images that cli.sh, cli-multi-gpu.sh
  # and cli.py name still served? (manifest only, nothing is pulled; total = compressed layer sizes)
  step 09-prebuilt-images "for i in tf-cpu.2-17.py310 tf-gpu.2-17.py310 tf-gpu.2-14.py310; do echo \"us-docker.pkg.dev/vertex-ai/training/\$i:latest\"; docker manifest inspect us-docker.pkg.dev/vertex-ai/training/\$i:latest | python3 -c 'import sys, json; m = json.load(sys.stdin); print(\"  \", m[\"mediaType\"].split(\".\")[-1], len(m[\"layers\"]), \"layers,\", round(sum(l[\"size\"] for l in m[\"layers\"]) / 1e9, 2), \"GB compressed\")'; done"
  ;;
wandb)
  # --- README "Get WandB Account API Key" (README:73-81): the key comes from wandb.ai/settings in a
  # browser (illustration); then "Set an environment variable using your terminal: export WANDB_KEY=..."
  # Here: an obviously fake 40-character placeholder (ASSETS.md, capture-only).
  step 10-export-wandb-key "export WANDB_KEY=$PH_KEY; echo \${#WANDB_KEY}"   # + extra echo: digest B6 checkpoint (40)
  step 11-wandb-key-new-terminal 'echo ${#WANDB_KEY}'    # extra: a new terminal forgets it (digest gotcha #1)
  ;;
bases)
  capture_only_bases   # (re-)tag the capture-only base images without re-running `pre`
  ;;
shell)
  export WANDB_KEY=$PH_KEY        # README:80, done in this terminal before docker-shell.sh
  cd model-training
  git checkout -q -- Dockerfile docker-shell.sh   # capture-only: a re-run starts from the pinned files
  # --- README "Run docker-shell.sh" (README:85-116): the script's lines 8-9 hold the bucket and the
  # project ("[REPLACE WITH YOUR BUCKET NAME]", README:93-94); sed is the editor.
  step 20-edit-docker-shell "sed -i -e 's|^export GCS_BUCKET_URI=.*|export GCS_BUCKET_URI=\"gs://your-bucket-placeholder\"|' -e 's|^export GCP_PROJECT=.*|export GCP_PROJECT=\"your-gcp-project\"|' docker-shell.sh && sed -n '5,9p' docker-shell.sh"
  # no real key exists; the placeholder leaves before the container starts, so gcloud fails with the
  # documented missing-file error rather than an undocumented parse error (ASSETS.md)
  if [ -f ~/secrets/model-trainer.json ]; then
    mv ~/secrets/model-trainer.json ~/placeholder-key-removed.json
    mkdir -p "$OUT/capture-only"; echo "shell: moved the placeholder key out of ~/secrets before the first docker-shell.sh" >> "$OUT/capture-only/placeholder-key-moves.txt"
  fi
  # README:115 "Run sh docker-shell.sh", unmodified Dockerfile. Found live (not in the digest): the
  # bullseye-security pool on deb.debian.org no longer has the files its (stale) index lists, so
  # Dockerfile step 2 (the first apt-get install, Dockerfile:18-19) fails with 404s.
  hub_retry step 21-docker-shell-fails "sh docker-shell.sh"
  # fix 1 (extra): Dockerfile:2 -> python:3.13-slim-bookworm (Debian 12, still supported; the
  # digest already recommends bookworm for native arm64 builds, gotcha #20)
  step 22-fix-base-image "sed -i '2s/python:3.13-slim-bullseye/python:3.13-slim-bookworm/' Dockerfile && sed -n '1,2p' Dockerfile"
  # the same README command again: now the build reaches Dockerfile:37 and fails at google-cloud-sdk
  # (digest gotcha #20, live)
  hub_retry step 23-docker-shell-fails-again "sh docker-shell.sh"
  # fix 2 (extra, digest gotcha #20's fix): Dockerfile:37 -> google-cloud-cli (no GKE auth plugin)
  step 24-fix-dockerfile "sed -i '37s/google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin/google-cloud-cli/' Dockerfile && sed -n '35,37p' Dockerfile"
  step 25-git-diff "git diff --stat; git diff Dockerfile"   # extra: the two capture fixes, nothing else
  # the same README command a third time; extras typed inside: what the console container holds
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=3600 hub_retry istep 26-docker-shell "sh docker-shell.sh" \
    "$P" 'ls -la /secrets' \
    "$P" 'echo $GCP_PROJECT $GCS_BUCKET_URI ${#WANDB_KEY}' \
    "$P" 'which python gcloud gsutil uv' \
    "$P" 'gcloud --version' \
    "$P" 'python -c "import google.cloud.aiplatform as aip; print(aip.__version__)"' \
    "$P" 'python -c "import tensorflow"' \
    "$P" 'exit'
  step 27-docker-images "docker image ls model-training-cli"   # extra
  ;;
pkg)
  export WANDB_KEY=$PH_KEY
  cd model-training
  # --- README "Review Trainer Code" (README:121-125) is reading (source/ panels).
  # --- README "Run sh package-trainer.sh" (README:127-129), inside the container
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=900 istep 30-package-trainer "sh docker-shell.sh" \
    "$P" 'sh package-trainer.sh' \
    "$P" 'ls -l trainer.tar.gz' \
    "$P" 'tar tzvf trainer.tar.gz' \
    "$P" 'gsutil ls $GCS_BUCKET_URI' \
    "$P" 'exit'
  step 31-host-tarball "ls -l trainer.tar.gz; git status --short; git check-ignore -v trainer.tar.gz"   # extra: on the host, through the bind mount
  ;;
job)
  export WANDB_KEY=$PH_KEY
  cd model-training
  # --- README "Create Jobs in Vertex AI" (README:132-150): review cli.sh (source/ panel), "Make any
  # required changes" (none: the default CPU block is what runs), "Run sh cli.sh". The OPTIONAL CPU
  # section (README:152-154) is already what cli.sh does (digest E2).
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=900 istep 40-cli-sh "sh docker-shell.sh" \
    "$P" 'sh cli.sh' \
    "$P" 'gcloud auth list' \
    "$P" 'sh -x cli.sh' \
    "$P" 'gcloud ai custom-jobs list --region=us-central1' \
    "$P" 'exit'
  # README "View Jobs in Vertex AI" / "View Training Metrics" (README:156-163): browser (illustration)
  ;;
mgpu)
  export WANDB_KEY=$PH_KEY
  cd model-training
  # --- README "OPTIONAL: Multi GPU Training" (README:165-170): review (source/ panels), "Run sh cli-multi-gpu.sh"
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=900 istep 50-cli-multi-gpu "sh docker-shell.sh" \
    "$P" 'sh cli-multi-gpu.sh' \
    "$P" 'exit'
  ;;
clipy)
  export WANDB_KEY=$PH_KEY
  cd model-training
  # extras (not in the README): the SDK launcher cli.py (digest B16 / gotcha #3), and what the
  # console's Python 3.13 makes of the trainer package (digest gotcha #17)
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=1200 istep 60-cli-py "sh docker-shell.sh" \
    "$P" 'python cli.py' \
    "$P" 'export GCP_REGION=us-central1' \
    "$P" 'python cli.py' \
    "$P" 'which pip' \
    "$P" 'pip install ./package' \
    "$P" 'exit'
  ;;
nokey)
  cd model-training
  # extra: digest gotcha #1 -- a new host terminal where WANDB_KEY was never exported (this segment
  # does not export it), and gotcha #22 -- a second `sh docker-shell.sh` while the first is open.
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=900 istep 70-docker-shell-no-wandb-key "sh docker-shell.sh" \
    "$P" 'echo ${#WANDB_KEY}' \
    "$P" 'sh -x cli.sh 2>&1 | grep -o -- "--args=.*"' \
    "$P" 'sleep 40' \
    "$P" 'exit' &
  BG=$!
  for i in $(seq 120); do docker ps --format '{{.Names}}' | grep -qx model-training-cli && break; sleep 1; done
  sleep 5
  PTY_COLS=110 PTY_ROWS=50 PTY_TIMEOUT=300 istep 71-docker-shell-second "sh docker-shell.sh"
  wait $BG
  ;;
vtx)
  cd model-training
  # capture-only stand-in, NOT the tutorial and NOT Vertex AI: the first thing the job's prebuilt
  # container does with --python-package-uris is install the tarball (digest B12). Here a plain
  # python:3.10 container (the images are "py310") installs the same trainer.tar.gz; then the
  # trainer's W&B login line (task.py:153) runs on its own, offline, with the values it can get.
  hub_retry step 80-standin-pip-install "docker run --name trainer-standin -v \"\$PWD/trainer.tar.gz\":/tmp/trainer.tar.gz python:3.10-slim-bookworm pip install /tmp/trainer.tar.gz"
  step 81-standin-commit "docker commit trainer-standin trainer-standin >/dev/null && docker rm trainer-standin"
  step 82-standin-pip-list "docker run --rm trainer-standin pip list"
  step 83-standin-task-help "docker run --rm --network none trainer-standin python -m trainer.task --help"
  # task.py:153 wandb.login(key=args.wandb_key) with: the argparse default "16" (task.py:52; what cli.py
  # sends, digest gotcha #2); an empty --wandb_key= (WANDB_KEY not exported, gotcha #1); the 40-char
  # placeholder; a placeholder longer than 40 characters (digest §10 open question on key formats)
  step 84-standin-login-default "docker run --rm --network none trainer-standin python -c \"import wandb; wandb.login(key='16')\""
  step 85-standin-login-empty "docker run --rm --network none trainer-standin python -c \"import wandb; wandb.login(key='')\""
  step 86-standin-login-placeholder "docker run --rm --network none trainer-standin python -c \"import wandb; wandb.login(key='$PH_KEY')\""
  step 87-standin-login-long "docker run --rm --network none trainer-standin python -c \"import wandb; wandb.login(key='${PH_KEY}_LONGER')\""
  ;;
clean)
  # the README has no clean-up section; extras: what is left on the laptop
  step 90-docker-ps "docker ps -a"
  step 91-docker-images "docker image ls"
  ;;
colab)
  # ===== notebook B (course-map Drive id 1aAE5vR9r6Syh4heZboDbQNZS048VToxS): cell 5's install, run as
  # a shell command in a Python 3.12 container (no Colab sign-in, no GPU, no W&B account)
  cd /content 2>/dev/null || { mkdir -p ~/content && cd ~/content; }
  step C00-env "date -u '+%Y-%m-%d %H:%M UTC'; python --version"   # extra
  step C05-pip-install-wandb "pip install -q wandb -U"
  step C05b-wandb-version "python -c 'import wandb; print(wandb.__version__)'"   # extra
  # extra (digest E14 / gotcha #21, checked on today's wandb): notebook B's cell-38 pattern
  # (wandb.init, then wandb.config = {...}, then wandb.config.update(...)) in W&B's offline mode
  cat > /tmp/e14.py <<'EOF'
import wandb
wandb.init(project="cheese-app-demo", mode="offline")
wandb.config = {"learning_rate": 0.001, "epochs": 25, "batch_size": 32, "model_name": "2_block"}
wandb.config.update({"execution_time": 1.5})
print("type(wandb.config):", type(wandb.config).__name__)
print("the run's config:", dict(wandb.run.config))
wandb.finish()
EOF
  step C38-config-rebind "cat /tmp/e14.py; python /tmp/e14.py"
  cat > /tmp/e14-fixed.py <<'EOF'
import wandb
wandb.init(project="cheese-app-demo", mode="offline",
           config={"learning_rate": 0.001, "epochs": 25, "batch_size": 32, "model_name": "2_block"})
wandb.config.update({"execution_time": 1.5})
print("type(wandb.config):", type(wandb.config).__name__)
print("the run's config:", dict(wandb.run.config))
wandb.finish()
EOF
  step C38b-config-init "cat /tmp/e14-fixed.py; python /tmp/e14-fixed.py"
  ;;
*)
  echo "run_steps.sh: unknown segment $SEG" >&2; exit 2 ;;
esac
