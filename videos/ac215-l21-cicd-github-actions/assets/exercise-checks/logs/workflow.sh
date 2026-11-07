#!/bin/bash
# Runs inside l21ex/laptop:check (laptop-check.Dockerfile) as user student, with
#   /src  = assets/source/cheese-app-ci-cd (ci.yml at b8458ff), /hist = assets/source/cheese-app-ci-cd-history,
#   /checks = this logs/ folder (read-only).
# actionlint reads a workflow the way GitHub's own parser does (syntax, expressions, which contexts
# are allowed where); runstep.py + bash play one step's run: script with the values GitHub would
# substitute. No GitHub, no Slack: the webhook URL is the placeholder below, and nothing calls it.
step() { printf '$ %s\n' "$1"; bash -c "$1" 2>&1; printf '[exit %s]\n\n' "$?"; }
cd /tmp && mkdir -p wf/.github/workflows && cd wf
echo "## actionlint on the tutorial's file and on the exercises' version"
step 'actionlint -version | head -1'
step 'cp /src/.github/workflows/ci.yml .github/workflows/ci.yml && actionlint -shellcheck= -pyflakes= .github/workflows/ci.yml && echo "no findings"'
step 'cp /checks/ci-exercises.yml .github/workflows/ci.yml && actionlint -shellcheck= -pyflakes= .github/workflows/ci.yml && echo "no findings"'
echo "## C2: the first Slack attempt (199abd9), the secret tested in the step's if:"
step 'cp /hist/199abd9-ci.yml .github/workflows/ci.yml && grep -n "secrets.SLACK_WEBHOOK_URL" .github/workflows/ci.yml; actionlint -shellcheck= -pyflakes= .github/workflows/ci.yml'
echo "## B2: the exercises' Check test results with run 1's results (lint failed, the tests passed)"
step 'export GITHUB_OUTPUT=/tmp/out1 GITHUB_STEP_SUMMARY=/tmp/sum1; python3 /checks/runstep.py /checks/ci-exercises.yml test-summary test-results needs.lint-and-format.result=failure needs.unit-tests.result=success needs.integration-tests.result=success needs.system-tests.result=success > /tmp/s1.sh && bash --noprofile --norc -eo pipefail /tmp/s1.sh; e=$?; echo "--- GITHUB_OUTPUT:"; cat $GITHUB_OUTPUT; echo "--- GITHUB_STEP_SUMMARY:"; cat $GITHUB_STEP_SUMMARY; exit $e'
echo "## B2: the same step with run 2's results (all six green)"
step 'export GITHUB_OUTPUT=/tmp/out2 GITHUB_STEP_SUMMARY=/tmp/sum2; python3 /checks/runstep.py /checks/ci-exercises.yml test-summary test-results needs.lint-and-format.result=success needs.unit-tests.result=success needs.integration-tests.result=success needs.system-tests.result=success > /tmp/s2.sh && bash --noprofile --norc -eo pipefail /tmp/s2.sh; e=$?; echo "--- GITHUB_OUTPUT:"; cat $GITHUB_OUTPUT; exit $e'
echo "## B2: the original step: the summary never sees lint (run 1's results)"
step 'export GITHUB_OUTPUT=/tmp/out3; python3 /checks/runstep.py /src/.github/workflows/ci.yml test-summary test-results needs.unit-tests.result=success needs.integration-tests.result=success needs.system-tests.result=success > /tmp/s3.sh && bash --noprofile --norc -eo pipefail /tmp/s3.sh'
echo "## C1: the hardened Slack check reads the secret from env:, unset and set (placeholder)"
step 'export GITHUB_OUTPUT=/tmp/out4; python3 /checks/runstep.py /checks/ci-exercises.yml test-summary slack-check > /tmp/s4.sh && cat /tmp/s4.sh && SLACK_WEBHOOK_URL= bash -eo pipefail /tmp/s4.sh && cat $GITHUB_OUTPUT'
step 'export GITHUB_OUTPUT=/tmp/out5; SLACK_WEBHOOK_URL="https://hooks.slack.com/services/<your-webhook-path>" bash -eo pipefail /tmp/s4.sh && cat $GITHUB_OUTPUT'
