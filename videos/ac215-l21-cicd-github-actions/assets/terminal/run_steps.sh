#!/bin/bash
# Runs inside the "laptop" capture container as user `student`, recording each command's output to
# its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
#   l-pre       pin check, clone, where GitHub looks for workflows (extras)
#   l-push      README Part 5 "Push to GitHub" (README.md:344-349), verbatim, in the plain clone
#   l-own       the same push to "your repository": a local bare repo stands in for GitHub (extra)
#   l-fix       turn it green: pre-commit (README Part 4, L09) fixes utils.py, commit, push (run 2)
#   l-noverify  slides 29-31: a messy "quick fix" blocked by the hooks, then `--no-verify` (run 3)
#   l-part6     README Part 6's "break the tests" line and the one that does break them (context)
# Steps marked "extra" are not in Part 5 of the README; they are checks the video uses.
OUT=$1; SEG=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
cd ~
umask 022                                               # a laptop default (docker exec starts with 000)
export PATH="$HOME/venv/bin:$PATH"                      # the laptop's Python (see capture.sh)
export PIP_CERT=/etc/ssl/certs/ca-certificates.crt     # capture-only: pip behind the TLS proxy
STANDIN=/home/student/github-standin/student/cheese-app-ci-cd.git

step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1; echo "[exit $?]"; } > "$OUT/$name.txt"
}
capture_only_base() {  # recording sandbox only (CAPTURE_CA set); see ASSETS.md, "capture-only"
  [ -n "$CAPTURE_CA" ] || return 0
  local d; d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"
  {
    echo "# capture-only, NOT part of the tutorial: the recording sandbox reaches the internet through"
    echo "# a TLS-intercepting proxy. Same python:3.11-slim-bookworm plus that proxy's CA, https apt"
    echo "# sources and the CA env vars, re-tagged under the same name so that the README's Dockerfile"
    echo "# builds unchanged."
    echo "FROM python:3.11-slim-bookworm"
    echo "COPY capture-ca.crt /usr/local/share/ca-certificates/capture-ca.crt"
    echo "RUN cat /usr/local/share/ca-certificates/capture-ca.crt >> /etc/ssl/certs/ca-certificates.crt \\"
    echo " && sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources"
    echo "ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \\"
    echo "    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \\"
    echo "    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt"
  } > "$d/Dockerfile"
  mkdir -p "$OUT/capture-only"; cp "$d/Dockerfile" "$OUT/capture-only/base.Dockerfile"
  step capture-only/base-build "docker build -t python:3.11-slim-bookworm $d"
  rm -rf "$d"
}

case $SEG in
l-pre)
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; git --version; python3 --version"   # extra
  step 01-ls-remote "git ls-remote https://github.com/dlops-io/cheese-app-ci-cd.git"   # extra: the pin is still the head of main
  step 02-clone "git clone https://github.com/dlops-io/cheese-app-ci-cd.git"
  cd cheese-app-ci-cd
  step 03-git-log "git log -3 --format='%h %ci %s'"      # extra: the commit the video uses
  step 04-ls-workflows "ls -la .github/workflows/"       # extra: where GitHub looks for workflows
  step 05-branches "git branch -a"                       # extra: main is the only branch
  # capture-only: a git identity, so that commits can exist (never shown as a step)
  git config --global user.email student@laptop >/dev/null 2>&1
  git config --global user.name student >/dev/null 2>&1
  ;;
l-push)
  cd cheese-app-ci-cd
  # --- README Part 5 "Push to GitHub" (README.md:344-349), verbatim, in the clone of the course repo
  step 10-git-add "git add ."
  step 11-git-commit 'git commit -m "Add CI pipeline"'
  # capture-only: the sandbox proxy refuses this push with its own message, not the one a laptop
  # gets (GitHub: permission denied / 403); kept as evidence only, see ASSETS.md
  mkdir -p "$OUT/capture-only"; step capture-only/12-git-push-sandbox-proxy "git push"
  step 13-git-remote "git remote -v"                     # extra: where `git push` was going
  step 14-git-status "git status"                        # extra
  ;;
l-own)
  cd cheese-app-ci-cd
  # extra: "your repository". This sandbox cannot push to GitHub, so a bare repository on the
  # laptop stands in for https://github.com/<you>/cheese-app-ci-cd (see ASSETS.md)
  step 20-standin-create "git init --bare -b main $STANDIN"
  step 21-set-url "git remote set-url origin $STANDIN"
  step 22-git-push "git push"                            # the README's push, now to "your" repo
  step 23-standin-log "git --git-dir=$STANDIN log --format='%H %s' -1"   # extra: what CI would check out (run 1)
  ;;
l-fix)
  cd cheese-app-ci-cd
  # --- make run 1's red Lint job green: README Part 4's pre-commit (L09) rewrites utils.py
  step 30-pip-install-pre-commit "pip install pre-commit"
  step 31-pre-commit-install "pre-commit install"
  step 32-run-all-files "pre-commit run --all-files"
  step 33-git-diff "git diff"                            # extra: what Black rewrote
  step 34-run-all-files-again "pre-commit run --all-files"
  step 35-git-add "git add ."
  step 36-git-commit 'git commit -m "Format utils.py with Black"'   # extra message (the README has none for this)
  step 37-git-push "git push"
  step 38-standin-log "git --git-dir=$STANDIN log --format='%H %s' -2"   # extra: run 2's commit
  ;;
l-noverify)
  cd cheese-app-ci-cd
  # extra (lecture slides 29-31): a hurried edit the hooks reject, then committed with --no-verify
  step 40-quick-edit "sed -i 's/z = power(x, 2) + power(y, 2)/z=power(x,2)+power(y,2)/' src/api-service/api/service.py && git diff"
  step 41-git-add "git add ."
  step 42-git-commit 'git commit -m "quick fix"'
  step 43-git-status "git status --short"
  step 44-commit-no-verify 'git commit --no-verify -m "quick fix"'
  step 45-git-push "git push"
  step 46-git-log "git log --oneline -4"
  step 47-standin-log "git --git-dir=$STANDIN log --format='%H %s' -1"   # run 3's commit
  step 48-git-status "git status --short"                # the hook's reformatted copy, never committed
  step 49-restore "git restore src/api-service/api/service.py && git status --short"
  ;;
l-part6)
  cd cheese-app-ci-cd
  # context for Part 6 (README.md:369-397): its "break the tests" line, run in the image locally
  capture_only_base
  step 50-build "docker build -t cheese-app-api:local ."
  step 51-echo-broken 'echo "def broken(): assert False" >> tests/unit/test_utils.py'
  step 52-build "docker build -t cheese-app-api:local ."
  step 53-unit "docker run --rm cheese-app-api:local pytest tests/unit/ -v"
  step 54-restore "git checkout -- tests/unit/test_utils.py"
  step 55-echo-test-broken 'echo "def test_broken(): assert False" >> tests/unit/test_utils.py'   # extra: the line that breaks
  step 56-build "docker build -t cheese-app-api:local ."
  step 57-unit "docker run --rm cheese-app-api:local pytest tests/unit/ -v"
  step 58-restore "git checkout -- tests/unit/test_utils.py && git status --short"
  ;;
*) echo "unknown segment $SEG" >&2; exit 2 ;;
esac
