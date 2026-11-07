#!/bin/bash
# Capture-only stand-in for ONE GitHub-hosted runner job (see ASSETS.md, "runner/").
# Runs as root inside a fresh capture runner container (its own, empty Docker engine), executes
# the job's steps as ci_plan.py extracted them from ci.yml, and records each `run:` step's output
# to its own file: "$ script" (continuation lines "> "), the output, "[exit N]".
# GitHub's rules that matter here are applied: each `run:` runs as `bash --noprofile --norc -eo
# pipefail`; after a failed step, later steps are skipped unless they say `if: always()`; a
# failed step with `continue-on-error: true` does not fail the job. 00-steps.txt lists every
# step with its outcome, as the run page would; result.txt holds the job result.
# Steps whose file name starts with "x" are extras (not in ci.yml), run for the video.
# Usage: runner_job.sh <out_dir> <plan.sh> <sha>
OUT=$1; PLAN=$2; SHA=$3
WS=/home/runner/work/cheese-app-ci-cd/cheese-app-ci-cd
umask 022   # a hosted runner default (docker exec starts with 000)
mkdir -p "$WS" /tmp/gh-outputs
cd "$WS"
JOB_OK=1; JOB_ID=
LOG="$OUT/00-steps.txt"

say() { echo "$*" >> "$LOG"; }
slug() { echo "$1" | tr 'A-Z' 'a-z' | sed 's/[^a-z0-9]\+/-/g; s/^-//; s/-$//'; }
record() {  # record <file> <script>   ("$ " first line, "> " continuation lines, like a shell)
  local f=$1 script=$2 rc
  printf '%s\n' "$script" | sed '1s/^/$ /; 2,$s/^/> /' > "$f"
  bash --noprofile --norc -eo pipefail -c "$script" >> "$f" 2>&1; rc=$?
  echo "[exit $rc]" >> "$f"
  return $rc
}
xstep() {  # xstep <name> <cmd>   an extra check, never changes the job result
  record "$OUT/$1.txt" "$2"
}
job_begin() { JOB_ID=$1; echo "job: $1 (name: $2) on a fresh capture runner, commit $SHA" > "$LOG"; }
job_end() {
  if [ $JOB_OK = 1 ]; then echo success > "$OUT/result.txt"; else echo failure > "$OUT/result.txt"; fi
  say "job result: $(cat "$OUT/result.txt")"
}
uses_standin() {  # what this capture does in place of a `uses:` action (see ASSETS.md)
  local nn=$1 action=$2 f
  case $action in
    actions/checkout@*)
      f="$OUT/$nn-checkout-standin.txt"
      record "$f" "tar -xf /checkout.tar -C $WS && ls -A" ;;
    docker/setup-buildx-action@*)
      f="$OUT/$nn-buildx-standin.txt"
      record "$f" "docker buildx version" ;;
    actions/download-artifact@*)
      f="$OUT/$nn-download-artifact-standin.txt"
      record "$f" "cp /artifact/cheese-app-api.tar /tmp/ && ls -l /tmp/cheese-app-api.tar" ;;
    actions/upload-artifact@*)
      if [ "$JOB_ID" = build ]; then
        f="$OUT/$nn-upload-artifact-standin.txt"
        record "$f" "ls -l /tmp/cheese-app-api.tar"
      else
        f="$OUT/$nn-upload-artifact-standin.txt"
        record "$f" "find coverage/ -type f | wc -l"
      fi ;;
    *) return 99 ;;
  esac
}
gstep() {  # gstep <nn> <name> run|uses <if> <continue-on-error> <id> <script|action>
  local nn=$1 name=$2 kind=$3 cond=$4 coe=$5 sid=$6 body=$7 rc
  pre_hook "$nn" "$name"
  if [ $JOB_OK = 0 ] && [ "${cond#always()}" = "$cond" ]; then
    say "$nn  skipped   $name"; return
  fi
  if [ "$cond" = "always() && steps.slack-check.outputs.enabled == 'true'" ]; then
    local en; en=$(sed -n 's/^enabled=//p' /tmp/gh-outputs/slack-check 2>/dev/null)
    if [ "$en" != true ]; then say "$nn  skipped   $name   (steps.slack-check.outputs.enabled is '$en')"; return; fi
  fi
  if [ "$kind" = uses ]; then
    uses_standin "$nn" "$body"; rc=$?
    if [ $rc = 99 ]; then say "$nn  not run   $name   ($body needs GitHub)"; return; fi
  else
    export GITHUB_OUTPUT=/tmp/gh-outputs/${sid:-step$nn}; : > "$GITHUB_OUTPUT"
    record "$OUT/$nn-$(slug "$name").txt" "$body"; rc=$?
  fi
  if [ $rc = 0 ]; then say "$nn  success   $name"
  elif [ "$coe" = true ]; then say "$nn  failure   $name   (continue-on-error: the job stays green)"
  else say "$nn  failure   $name"; JOB_OK=0
  fi
  post_hook "$nn" "$name"
}

# --- extras the video uses (each file name starts with x, see ASSETS.md)
pre_hook() {
  case "$JOB_ID:$2" in
    lint-and-format:Load\ Docker\ image|unit-tests:Load\ Docker\ image|integration-tests:Load\ Docker\ image|system-tests:Load\ Docker\ image)
      xstep x1-images-before-load "docker images" ;;
  esac
}
post_hook() {
  case "$JOB_ID:$2" in
    build:Save\ Docker\ image) xstep x1-images-after-build "docker images" ;;
    *:Load\ Docker\ image) xstep x2-images-after-load "docker images" ;;
    unit-tests:Generate\ coverage\ report) xstep x3-coverage-dir "ls -la coverage/ && docker run --rm cheese-app-api:$SHA id" ;;
    system-tests:Start\ API\ server\ container) xstep x3-docker-ps "docker ps" ;;
  esac
}

source "$PLAN"

# extras after the job (never change its result)
case $JOB_ID in
  lint-and-format)
    # GitHub skips the Flake8 step when Black failed; this shows what it would have printed.
    xstep x4-flake8-if-run "docker run --rm cheese-app-api:$SHA flake8 --max-line-length=120 --extend-ignore=E203,W503 api/"
    xstep x5-black-diff "docker run --rm cheese-app-api:$SHA black --diff --line-length 120 api/" ;;
esac
exit 0
