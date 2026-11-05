#!/bin/bash
# Runs inside the "laptop" capture container (see capture.sh) as user `student`, recording each
# tutorial command's output to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# L15 follows the AWS tutorials (Conny's series decision), README order:
#   dlops-io/model-deployment-aws @ 077f4dbc7b13ccef208c65a8e29489331261029e (main, 2025-08-25)
#   dlops-io/ml-workflow-aws      @ f165c6e17895d3d6c33a150d349f4b2649c807db (main, 2025-08-19)
# Segments (folder laptop/):
#   pre       versions, AWS CLI, capture-only base images (proxy CA)            -> 00-09
#   md-setup  model-deployment-aws: clone, aws configure (no keys), Option 2 exports, edit
#             docker-shell.sh, chmod                                            -> 10-19
#   md-shell  sh docker-shell.sh as written (arm64 build), the plain build line, what the
#             unpinned Pipfile resolves today (SageMaker SDK 3), the pin, the container and the
#             four cli.py commands, the README's clean-up commands             -> 20-39
#   md-local  extras: what --prepare builds before the upload, and the model served locally by
#             TensorFlow Serving (a stand-in for the SageMaker endpoint)         -> 40-49
#   md-clean  extras: remove the md images (disk)                                -> 49
#   mw-setup  ml-workflow-aws: clone, Test Configuration, data-collector's docker-shell.sh refusal,
#             aws configure with obviously fake placeholder keys (capture-only), the test again
#                                                                               -> 50-59
#   mw-coll   data collector container: python cli.py --search ...              -> 60-64
#   mw-proc   data processor: arm64 build, plain line, --clean, --prepare        -> 65-69
#   mw-train  model training: arm64 build, plain line, local training, package-trainer, --train
#                                                                               -> 70-79
#   mw-push   "Build & Push Images": the ECR variable block                     -> 80-84
#   mw-flow   workflow: what its unpinned Pipfile resolves today, the pin, the container:
#             --data_collector, --pipeline, the four component flags              -> 85-94
#   mw-lock   87 alone (re-run)
#   mw-dag    extra: the pipeline's JSON definition, built offline                -> 92
#   mw-end    extras: what is left on the laptop                                -> 95-99
# Steps marked "extra" are not in the README; they are checks the video uses.
OUT=$1; SEG=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
umask 022   # a login shell's default (docker exec would otherwise run with umask 0000)
cd ~

step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1 | sed 's/\x1b\[[0-9;]*m//g'; echo "[exit ${PIPESTATUS[0]}]"; } > "$OUT/$name.txt"
}
istep() {  # istep <name> <command> [<prompt regex> <typed line>]...   (in a terminal, typed)
  local name=$1 cmd=$2; shift 2
  local args=()
  while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
  { echo "\$ $cmd"
    python3 "$HERE/ptyrun.py" --cols "${PTY_COLS:-110}" --rows "${PTY_ROWS:-50}" --timeout "${PTY_TIMEOUT:-900}" \
      "${args[@]}" -- bash -c "$cmd"
    echo "[exit $?]"; } > "$OUT/$name.txt"
}
hub_retry() {  # hub_retry step|istep <name> <args...>   (recording sandbox only: CAPTURE_HUB_WAIT set)
  # Docker Hub limits anonymous pulls per IP and the sandbox's egress IPs are shared: retry a step
  # that hit the limit; capture-only/hub-retries.txt counts the failed attempts.
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
capture_only_bases() {  # recording sandbox only (CAPTURE_CA set); see ASSETS.md, "capture-only"
  # The tutorial's builds need TLS, and the sandbox's TLS is re-signed by its proxy, which also
  # refuses plain http. The base images of the tutorial Dockerfiles (ubuntu:20.04, python:3.11-slim)
  # are rebuilt with that proxy's CA, https apt sources and the CA env vars, then re-tagged under
  # the same names, so the tutorial Dockerfiles build unchanged.
  # PIP_NO_CACHE_DIR keeps pip/pipenv from keeping a second copy of every wheel in the image (the
  # sandbox's disk is small); it changes no version and no output line that a scene shows.
  [ -n "$CAPTURE_CA" ] || return 0
  local d b bases=("$@"); [ ${#bases[@]} -gt 0 ] || bases=(ubuntu:20.04 python:3.11-slim)
  d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"
  mkdir -p "$OUT/capture-only"
  for b in "${bases[@]}"; do
    cat > "$d/Dockerfile" <<EOF
# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through a
# TLS-intercepting proxy that refuses plain http. Same $b plus that proxy's CA (also kept for
# update-ca-certificates), https apt sources and the CA env vars, re-tagged under the same name so
# the tutorial Dockerfiles build unchanged.
FROM $b
COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt
RUN mkdir -p /etc/ssl/certs && cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \\
 && for f in /etc/apt/sources.list /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list.d/ubuntu.sources; do \\
      [ -f "\$f" ] && sed -i -e 's|http://deb.debian.org|https://deb.debian.org|g' -e 's|http://security.debian.org|https://security.debian.org|g' \\
        -e 's|http://archive.ubuntu.com|https://archive.ubuntu.com|g' -e 's|http://security.ubuntu.com|https://security.ubuntu.com|g' "\$f"; \\
    done; true
ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \\
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \\
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \\
    AWS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \\
    PIP_NO_CACHE_DIR=1
EOF
    cp "$d/Dockerfile" "$OUT/capture-only/${b/:/-}-base.Dockerfile"
    hub_retry step "capture-only/${b/:/-}-base-build" "docker build -t $b $d"
  done
  rm -rf "$d"
}

arm64_attempt() {  # arm64_attempt <name> <base image>: the README's `sh docker-shell.sh` with the
  # script's arm64 build line, on this x86_64 laptop. The capture-only re-tag of the base is
  # amd64-only, so it is removed first (the build then pulls Docker Hub's own arm64 base, as on a
  # student's machine) and re-made afterwards.
  local name=$1 base=$2
  [ -n "$CAPTURE_CA" ] && docker image rm "$base" >/dev/null 2>&1
  PTY_TIMEOUT=900 hub_retry step "$name" "sh docker-shell.sh"
  [ -n "$CAPTURE_CA" ] && docker image rm "$base" >/dev/null 2>&1; capture_only_bases "$base"
}

PH_BUCKET_MD=your-models-bucket-placeholder                       # capture-only names: obviously
PH_ROLE='arn:aws:iam::000000000000:role/SageMakerExecutionRole'   # placeholders, no real account
PH_AK=PLACEHOLDER_NOT_A_REAL_ACCESS_KEY                           # capture-only AWS "keys": obviously
PH_SK=PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000               # fake, rejected by AWS
P_APP='app@[0-9a-f]{12}:/app\$ $'      # the pipenv-shell prompt of the images that run as user app
P_ROOT='root@[0-9a-f]{12}:/app# $'     # the bash prompt of the images that run as root
MODEL_DIR=artifacts/model-mobilenetv2_train_base_True.v1

case $SEG in
pre)
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; git --version; docker images"   # extra
  # README (ml-workflow-aws:51-53) "Install AWS CLI": brew on macOS, snap or the curl installer on
  # Linux. This laptop is Alpine: its package manager's AWS CLI v2 (capture.sh setup).
  step 01-aws-version "aws --version; which aws"   # extra
  capture_only_bases
  ;;
md-setup)
  # === model-deployment-aws README ===
  # "Clone the github repository" (README:9-10): "Clone or download from here"
  step 10-clone "git clone https://github.com/dlops-io/model-deployment-aws.git"
  cd model-deployment-aws
  step 11-git-log "git log -1 --format='%H %ci %s'"   # extra: the commit the video uses
  step 12-ls "ls -la; ls data"                      # extra
  cd ~
  # "AWS Services to Enable", "Create AWS IAM User", "Create SageMaker Execution Role", "Create S3
  # Bucket" (README:12-52): console clicks -> illustration (ASSETS.md). No AWS account here.
  # "Option 1: AWS CLI Configuration (Recommended)" (README:64-75): aws configure. There are NO
  # keys in this recording: the two key prompts are answered with Enter (left empty), region and
  # output as the README says.
  PTY_COLS=100 PTY_ROWS=30 istep 13-aws-configure "aws configure" \
    'AWS Access Key ID \[None\]: $' '' \
    'AWS Secret Access Key \[None\]: $' '' \
    'Default region name \[None\]: $' 'us-east-1' \
    'Default output format \[None\]: $' 'json'
  step 14-aws-files "ls -la ~/.aws; cat ~/.aws/config"   # extra: README:75 "This will create ~/.aws/credentials and ~/.aws/config"
  step 15-sts-no-keys "aws sts get-caller-identity"      # extra: the first thing the container will try (docker-entrypoint.sh:7)
  # "Option 2: Environment Variables" (README:77-83), verbatim (the README's own placeholders), then
  # what AWS answers to them (extra)
  step 16-option2-exports "export AWS_ACCESS_KEY_ID=your_access_key_id
export AWS_SECRET_ACCESS_KEY=your_secret_access_key
export AWS_REGION=us-east-1
aws sts get-caller-identity"
  # "Update Configuration" (README:85-90): edit docker-shell.sh (sed is the editor). Placeholder
  # bucket and role, region as the README; the original line 8 holds a real-looking account id,
  # which no capture prints.
  cd model-deployment-aws
  step 17-edit-docker-shell "sed -i -e 's|^export S3_MODELS_BUCKET_NAME=.*|export S3_MODELS_BUCKET_NAME=\"$PH_BUCKET_MD\"|' -e 's|^export SAGEMAKER_ROLE=.*|export SAGEMAKER_ROLE=\"$PH_ROLE\"|' docker-shell.sh && sed -n '5,9p' docker-shell.sh"
  # "Quick Start Commands" (README:92-108), 1. Build and run the container (README:97-99)
  step 18-chmod "chmod +x docker-shell.sh"
  step 19-ls-l "ls -l docker-shell.sh"   # extra
  ;;
md-shell)
  cd model-deployment-aws
  # capture-only: a re-run starts from the pinned files plus 17's edit (silent)
  git checkout -q -- docker-shell.sh Pipfile
  sed -i -e "s|^export S3_MODELS_BUCKET_NAME=.*|export S3_MODELS_BUCKET_NAME=\"$PH_BUCKET_MD\"|" -e "s|^export SAGEMAKER_ROLE=.*|export SAGEMAKER_ROLE=\"$PH_ROLE\"|" docker-shell.sh
  # README:99 "sh docker-shell.sh", as written: docker-shell.sh:19 builds --platform=linux/arm64/v8
  # ("M1/2 chip macs use this line"). This laptop is x86_64 with no arm64 emulation installed.
  arm64_attempt 20-docker-shell-arm64 ubuntu:20.04
  # extra: the script's own other line (docker-shell.sh:17, commented out) for a non-Apple-silicon
  # machine: comment the arm64 line, uncomment the plain one
  step 21-use-plain-build "sed -i -e 's|^docker build -t \$IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .|#&|' -e 's|^#docker build -t \$IMAGE_NAME -f Dockerfile .|docker build -t \$IMAGE_NAME -f Dockerfile .|' docker-shell.sh && sed -n '17,21p' docker-shell.sh"
  # README:99 again, unchanged Pipfile: NOT kept. On this recording machine the build's
  # `RUN cd /app && pipenv lock && pipenv sync` (Dockerfile:55) ran for 13+ minutes and filled the
  # disk (several GB of downloads, source builds). Why, in two small extras (ASSETS.md):
  # what the resolver picks today on the image's Python 3.9 ...
  capture_only_bases python:3.9-slim
  step 22-resolve-today "docker run --rm --tmpfs /tmp:exec,size=4g -v /capture/helpers:/helpers:ro python:3.9-slim sh /helpers/resolve_check.sh boto3 sagemaker pillow tensorflow==2.18.0 numpy requests"
  # ... and what that SageMaker SDK 3 does to cli.py's imports (cli.py:20-24)
  step 23-sagemaker3-imports "docker run --rm -v /capture/helpers:/helpers:ro python:3.9-slim sh /helpers/sagemaker_import_check.sh 'sagemaker==3.13.1 sagemaker-core==2.13.1 sagemaker-train==1.13.1 sagemaker-serve==1.13.1 sagemaker-mlops==1.13.1' 'import sagemaker; from sagemaker.tensorflow import TensorFlowModel' 'from sagemaker import get_execution_role' 'from sagemaker.serializers import JSONSerializer'"
  # extra, the fix a student needs today: pin the SDK below version 3 in the Pipfile
  step 24-pin-sagemaker "sed -i 's/^sagemaker = \"\\*\"/sagemaker = \"<3\"/' Pipfile && git diff Pipfile"
  # README:99 a third time (with the pin), then extras typed inside the container
  PTY_TIMEOUT=3600 hub_retry istep 25-docker-shell "sh docker-shell.sh" \
    "$P_APP" 'python --version; which python pipenv aws' \
    "$P_APP" 'pip list 2>/dev/null | grep -i -E "^(tensorflow|keras|sagemaker|sagemaker-core|boto3|numpy|pillow) "' \
    "$P_APP" 'echo $S3_MODELS_BUCKET_NAME $AWS_REGION $SAGEMAKER_ROLE' \
    "$P_APP" 'ls -la /home/app/.aws' \
    "$P_APP" 'python cli.py --help' \
    "$P_APP" 'exit'
  step 26-docker-images "docker image ls model-deployment-cli-aws"   # extra
  # README:102 / "Prepare Model for Deployment" (README:110-117)
  PTY_TIMEOUT=900 istep 27-prepare "sh docker-shell.sh" "$P_APP" 'python cli.py --prepare' "$P_APP" 'ls -la artifacts' "$P_APP" 'exit'
  # README:103 / "Upload & Deploy Model to SageMaker" (README:119-129)
  PTY_TIMEOUT=900 istep 28-deploy "sh docker-shell.sh" "$P_APP" 'python cli.py --deploy' "$P_APP" 'exit'
  # README:104 / "Test Predictions" (README:131-148)
  PTY_TIMEOUT=900 istep 29-predict "sh docker-shell.sh" "$P_APP" 'python cli.py --predict' "$P_APP" 'exit'
  # README:106-107 / "Using the CLI Script" (README:166-176)
  PTY_TIMEOUT=900 istep 30-delete "sh docker-shell.sh" "$P_APP" 'python cli.py --delete' "$P_APP" 'exit'
  # "Using AWS CLI" (README:159-164), on the laptop: first exactly as written (the <...> are
  # placeholders the shell reads as redirections), then with a placeholder endpoint name (extra)
  step 31-aws-cli-delete-as-written "aws sagemaker delete-endpoint --endpoint-name <your-endpoint-name>"
  step 32-aws-cli-delete "aws sagemaker delete-endpoint --endpoint-name cheese-endpoint-placeholder"
  ;;
md-resolve)   # 22 alone (re-run)
  step 22-resolve-today "docker run --rm --tmpfs /tmp:exec,size=4g -v /capture/helpers:/helpers:ro python:3.9-slim sh /helpers/resolve_check.sh boto3 sagemaker pillow tensorflow==2.18.0 numpy requests"
  ;;
md-local)
  cd model-deployment-aws
  # extra (capture-only helper, ASSETS.md): what `--prepare` builds on the laptop before its upload.
  # The tutorial's own image and mounts; only the S3 client is a stub that sends nothing.
  step 40-prepare-local "docker run --rm --entrypoint pipenv -v \"\$PWD\":/app -v /capture/helpers:/helpers:ro -e S3_MODELS_BUCKET_NAME=$PH_BUCKET_MD -e AWS_REGION=us-east-1 model-deployment-cli-aws run python /helpers/prepare_offline.py"
  step 41-artifacts "ls -la artifacts; find $MODEL_DIR | sort; du -sh artifacts/*"
  step 42-tarball "tar tzvf $MODEL_DIR/model.tar.gz"
  step 43-signature "docker run --rm --entrypoint pipenv -v \"\$PWD\":/app model-deployment-cli-aws run saved_model_cli show --dir /app/$MODEL_DIR/1 --tag_set serve --signature_def serving_default"
  step 44-git-status "git status --short; git check-ignore -v artifacts $MODEL_DIR/model.tar.gz"
  # extra: a local stand-in for the SageMaker endpoint. SageMaker's TensorFlow 2.13 serving image
  # (cli.py:154 framework_version="2.13") runs TensorFlow Serving; here the public
  # tensorflow/serving:2.13.1 image serves the exported folder (version 1) on its REST port.
  hub_retry step 45-serving-pull "docker pull tensorflow/serving:2.13.1"
  step 46-serving-start "docker run -d --name cheese-serving --network host -v \"\$PWD/$MODEL_DIR\":/models/cheese:ro -e MODEL_NAME=cheese tensorflow/serving:2.13.1 >/dev/null; sleep 20; docker logs cheese-serving 2>&1 | tail -15; curl -s http://localhost:8501/v1/models/cheese"
  step 47-predict-local "docker run --rm --network host --entrypoint pipenv -v \"\$PWD\":/app -v /capture/helpers:/helpers:ro -e S3_MODELS_BUCKET_NAME=$PH_BUCKET_MD model-deployment-cli-aws run python /helpers/predict_local.py http://localhost:8501/v1/models/cheese:predict"
  step 48-serving-stop "docker rm -f cheese-serving"
  ;;
md-clean)
  # extra: the laptop's disk (the image alone is several GB)
  step 49-md-images "docker image ls; docker image rm model-deployment-cli-aws tensorflow/serving:2.13.1 >/dev/null; docker builder prune -af >/dev/null; docker system df"
  ;;
mw-setup)
  # === ml-workflow-aws README ===
  # "Clone the github repository" (README:15-16)
  step 50-clone "git clone https://github.com/dlops-io/ml-workflow-aws.git"
  cd ml-workflow-aws
  step 51-git-log "git log -1 --format='%H %ci %s'"   # extra
  step 52-tree "tree -a -I .git --dirsfirst ."        # extra
  cd ~
  # "AWS Services", "Create S3 Bucket", "Create IAM User", "Create Access Keys" (README:18-49):
  # console clicks -> illustration. "Configure AWS CLI" (README:55-63): done in 13 (no keys).
  # "Test Configuration" (README:65-69)
  step 53-test-config "aws sts get-caller-identity
aws s3 ls"
  # "Run Data Collector Container" (README:88-95): inside src/data-collector, sh docker-shell.sh
  cd ml-workflow-aws/src/data-collector
  step 54-collector-docker-shell-no-keys "sh docker-shell.sh"
  cd ~
  # capture-only: aws configure with obviously fake placeholder keys, so the scripts' key check
  # (docker-shell.sh:13-26) passes and every AWS call gets AWS's own answer to a key that does not
  # exist. A student types the keys from the downloaded .csv here (README:59-63).
  PTY_COLS=100 PTY_ROWS=30 istep 55-aws-configure-placeholder "aws configure" \
    'AWS Access Key ID \[None\]: $' "$PH_AK" \
    'AWS Secret Access Key \[None\]: $' "$PH_SK" \
    'Default region name \[us-east-1\]: $' '' \
    'Default output format \[json\]: $' ''
  step 56-aws-configure-list "aws configure list"   # extra
  step 57-test-config-placeholder "aws sts get-caller-identity
aws s3 ls"   # README:67-68 again
  ;;
mw-coll)
  cd ml-workflow-aws/src/data-collector
  # README:95 sh docker-shell.sh, then "Test Data Collector" (README:97-100) + extras (the build is
  # small: its terminal log is kept as it is)
  PTY_TIMEOUT=1800 hub_retry istep 60-collector "sh docker-shell.sh" \
    "$P_ROOT" 'python cli.py --search --nums 10 --query "brie cheese" "gouda cheese" "gruyere cheese" "parmigiano cheese"' \
    "$P_ROOT" 'ls /persistent/dataset; ls /persistent/dataset/raw' \
    "$P_ROOT" 'for d in /persistent/dataset/raw/*; do echo "$(ls "$d" | wc -l) $d"; done; ls -l /persistent/dataset/raw.zip' \
    "$P_ROOT" 'exit'
  step 61-persistent-on-laptop "ls -la ~; ls -la ~/persistent-folder/dataset"   # extra: where /persistent lives
  step 62-collector-image "docker image ls cheese-app-data-collector"           # extra
  ;;
mw-proc)
  cd ml-workflow-aws/src/data-processor
  git checkout -q -- docker-shell.sh Pipfile   # capture-only: a re-run starts from the pinned files
  # README:113 sh docker-shell.sh, as written (docker-shell.sh:31 --platform=linux/arm64/v8)
  arm64_attempt 65-processor-docker-shell-arm64 python:3.11-slim
  step 66-use-plain-build "sed -i -e 's|^docker build -t \$IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .|#&|' -e 's|^#docker build -t \$IMAGE_NAME -f Dockerfile .|docker build -t \$IMAGE_NAME -f Dockerfile .|' docker-shell.sh && sed -n '29,34p' docker-shell.sh"   # extra
  # extra: the build line docker-shell.sh now runs (line 29), alone and without a terminal, so the
  # build log is plain text; the README's `sh docker-shell.sh` below then reuses its cached layers
  PTY_TIMEOUT=3600 hub_retry step 67-processor-build "docker build -t cheese-app-data-processor -f Dockerfile ."
  # README:113 again, then "Test Data Processor" (README:115-120) + extras
  PTY_TIMEOUT=3600 hub_retry istep 68-processor "sh docker-shell.sh" \
    "$P_ROOT" 'python cli.py --clean' \
    "$P_ROOT" 'python cli.py --prepare' \
    "$P_ROOT" 'ls -la /persistent/dataset; ls -la /persistent/dataset/tfrecords' \
    "$P_ROOT" 'for d in /persistent/dataset/clean/*; do echo "$(ls "$d" | wc -l) $d"; done' \
    "$P_ROOT" 'pip list 2>/dev/null | grep -i -E "^(tensorflow|difpy|dask|boto3|scikit-learn) "' \
    "$P_ROOT" 'exit'
  step 69-processor-image "docker image ls cheese-app-data-processor; docker image rm cheese-app-data-processor >/dev/null; docker builder prune -af >/dev/null; docker system df"   # extra (disk)
  ;;
mw-train)
  cd ml-workflow-aws/src/model-training
  git checkout -q -- docker-shell.sh Pipfile   # capture-only: a re-run starts from the pinned files
  # README:131 sh docker-shell.sh, as written (docker-shell.sh:32 --platform=linux/arm64/v8)
  arm64_attempt 70-training-docker-shell-arm64 python:3.11-slim
  step 71-use-plain-build "sed -i -e 's|^docker build -t \$IMAGE_NAME --platform=linux/arm64/v8 -f Dockerfile .|#&|' -e 's|^#docker build -t \$IMAGE_NAME -f Dockerfile .|docker build -t \$IMAGE_NAME -f Dockerfile .|' docker-shell.sh && sed -n '29,34p' docker-shell.sh"   # extra
  # extra: the build line alone, plain log (as 67)
  PTY_TIMEOUT=3600 hub_retry step 72-training-build "docker build -t cheese-app-training-cli -f Dockerfile ."
  # README:131 again; "Local Training" (README:135-136), "Remote Training" (README:137-139) + extras
  PTY_TIMEOUT=3600 hub_retry istep 73-training "sh docker-shell.sh" \
    "$P_APP" 'python --version; pip list 2>/dev/null | grep -i -E "^(tensorflow|keras|sagemaker|boto3|awscli) "' \
    "$P_APP" 'ls -la /persistent /persistent/dataset' \
    "$P_APP" 'python -m package.trainer.task --epochs=1 --batch_size=4 --bucket_name=cheese-app-ml-workflow-demo' \
    "$P_APP" 'ls -laR /persistent/model' \
    "$P_APP" 'sh package-trainer.sh' \
    "$P_APP" 'ls -l trainer.tar.gz' \
    "$P_APP" 'python cli.py --train' \
    "$P_APP" 'exit'
  step 74-training-image "docker image ls cheese-app-training-cli; docker image rm cheese-app-training-cli >/dev/null; docker builder prune -af >/dev/null; docker system df"   # extra (disk)
  ;;
mw-push)
  # "Build & Push Images" (README:152-203): "This step has already been done for this tutorial."
  # Docker Hub login/push need an account (not run). "Set Environment Variables" (README:168-174),
  # verbatim, then README:198's echo
  step 80-ecr-variables "export REGION=us-east-1 [YOUR DEVELOPMENT REGION]
export ACCOUNT_ID=\$(aws sts get-caller-identity --query Account --output text)
export REPO=cheese-app-data-collector  # or cheese-app-data-processor
export TAG=latest
export ECR_URI=\"\$ACCOUNT_ID.dkr.ecr.\$REGION.amazonaws.com/\$REPO:\$TAG\"
echo \"ECR URI: \$ECR_URI\""
  # extra: README:182, the first AWS call of the push block ("|| true" hides its failure)
  step 81-ecr-create "export REGION=us-east-1 REPO=cheese-app-data-collector
aws ecr create-repository --repository-name \"\$REPO\" --region \"\$REGION\" || true"
  ;;
mw-flow)
  cd ml-workflow-aws/src/workflow
  git checkout -q -- docker-shell.sh Pipfile Dockerfile   # capture-only: a re-run starts from the pinned files
  # "Automate Running Data Collector Container" (README:210-224): sh docker-shell.sh in
  # src/workflow. Its Dockerfile copies only the Pipfile (Dockerfile:40) and runs `pipenv install`
  # (:42), so the committed Pipfile.lock (sagemaker 2.250.0) is NOT used: the image resolves
  # `sagemaker = "*"` afresh. Unchanged, that build is not kept here (several GB, as in 22); what
  # it resolves today on the image's Python 3.11, and what that does to cli.py's imports
  # (cli.py:12-22), in two extras:
  capture_only_bases python:3.11-slim
  step 85-resolve-today "docker run --rm --tmpfs /tmp:exec,size=4g -v /capture/helpers:/helpers:ro python:3.11-slim sh /helpers/resolve_check.sh sagemaker boto3"
  step 86-sagemaker3-imports "docker run --rm -v /capture/helpers:/helpers:ro python:3.11-slim sh /helpers/sagemaker_import_check.sh 'sagemaker==3.29.0 sagemaker-core==2.29.0 sagemaker-train==1.29.0 sagemaker-serve==1.29.0 sagemaker-mlops==1.29.0' 'from sagemaker.processing import ProcessingInput, ProcessingOutput, Processor' 'from sagemaker.workflow.pipeline import Pipeline' 'from sagemaker.tensorflow import TensorFlow'"
  step 87-committed-lock "python3 -c 'import json; d = json.load(open(\"Pipfile.lock\"))[\"default\"]; print(\"Pipfile.lock pins sagemaker\", d[\"sagemaker\"][\"version\"], \"and boto3\", d[\"boto3\"][\"version\"])'; grep -n 'ADD\|RUN pipenv' Dockerfile"   # extra
  # extra, the same fix as 24: pin the SDK below version 3
  step 88-pin-sagemaker "sed -i 's/^sagemaker = \"\\*\"/sagemaker = \"<3\"/' Pipfile && git diff Pipfile"
  # extra: the build line docker-shell.sh runs (line 29, --platform=linux/amd64), alone, plain log
  PTY_TIMEOUT=3600 hub_retry step 89-workflow-build "docker build -t cheese-app-workflow --platform=linux/amd64 -f Dockerfile ."
  # README:218 sh docker-shell.sh (with the pin); README:223 python cli.py --data_collector;
  # "SageMaker Pipelines" (README:226-248): --pipeline and the four component flags; + extras
  PTY_TIMEOUT=3600 hub_retry istep 90-workflow "sh docker-shell.sh" \
    "$P_APP" 'python --version; pip list 2>/dev/null | grep -i -E "^(sagemaker|sagemaker-core|boto3) "; aws --version' \
    "$P_APP" 'ls /data-collector /data-processor; docker ps --format "{{.Names}} {{.Image}}"' \
    "$P_APP" 'python cli.py --data_collector' \
    "$P_APP" 'python cli.py --pipeline' \
    "$P_APP" 'python cli.py --data_processor' \
    "$P_APP" 'python cli.py --model_training' \
    "$P_APP" 'python cli.py --model_deploy' \
    "$P_APP" 'exit'
  step 91-workflow-image "docker image ls cheese-app-workflow"   # extra
  ;;
mw-lock)   # 87 alone (re-run)
  cd ml-workflow-aws/src/workflow
  step 87-committed-lock "python3 -c 'import json; d = json.load(open(\"Pipfile.lock\"))[\"default\"]; print(\"Pipfile.lock pins sagemaker\", d[\"sagemaker\"][\"version\"], \"and boto3\", d[\"boto3\"][\"version\"])'; grep -n 'ADD\|RUN pipenv' Dockerfile"   # extra
  ;;
mw-dag)
  cd ml-workflow-aws/src/workflow
  # extra (capture-only helper, ASSETS.md): the pipeline cli.py's pipeline() defines, as the JSON
  # SageMaker would receive (Pipeline.definition()), built in the tutorial's own workflow image (with
  # 88's pin). Account lookups answer with the placeholder 000000000000; nothing is sent or created.
  step 92-pipeline-definition "docker run --rm --entrypoint pipenv -v \"\$PWD\":/app -v /capture/helpers:/helpers:ro -e AWS_ACCESS_KEY_ID=\$(aws configure get aws_access_key_id) -e AWS_SECRET_ACCESS_KEY=\$(aws configure get aws_secret_access_key) -e AWS_REGION=us-east-1 -e S3_BUCKET_NAME=cheese-app-ml-workflow-demo -e S3_PACKAGE_URI=s3://cheese-app-ml-workflow-demo cheese-app-workflow run python /helpers/pipeline_offline.py"
  ;;
mw-end)
  step 95-docker-ps "docker ps -a"   # extra: --rm left nothing running
  step 96-docker-images "docker image ls"
  step 97-laptop-files "ls -la ~ ~/persistent-folder ~/persistent-folder/dataset; cd ~/ml-workflow-aws && git status --short"
  ;;
*)
  echo "unknown segment $SEG" >&2; exit 2 ;;
esac
