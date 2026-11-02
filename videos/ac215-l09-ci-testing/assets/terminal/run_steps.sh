#!/bin/bash
# Runs inside a fresh capture container as user `student`, recording each tutorial command's output
# to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# Track A segments (the "laptop" container, cheese-app-ci-cd README Parts 1-4, in README order):
#   a-pre    clone + extras + the capture-only base image (see ASSETS.md)
#   a-part1  Part 1: docker-shell.sh, uvicorn, the three URL checks (curl extras), exit
#   a-part2  Part 2: Option A (in-image flake8/black) and Option B (pip install on the laptop)
#   a-part3  Part 3: Options 1 (unit/integration/coverage), 2 (system tests), 3 (interactive)
#   a-part4  Part 4: pre-commit install, hooks on a real commit, a blocked commit (extras)
#   a-clean  README "Docker Cleanup" + pre-commit uninstall (extra)
# Track B segments (the "babykev" container, the guest lecture's walk.md, step by step):
#   b-setup    uv + just (the walk's prerequisites), clone babykev, list the step tags
#   b-prewarm  capture-only: warm uv's and Hugging Face's caches in a throwaway clone
#   b-s00 b-s01 b-s02 b-s03 b-s04 b-s04b b-s05 b-s05a b-s05b   one segment per step tag
# Steps marked "extra" are not in the README/walk; they are checks the video uses. The walk's
# macOS `sed -i ''` is written `sed -i` here, as the walk's own README:66 says to do on Linux.
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
    python3 "$HERE/ptyrun.py" --cols "${PTY_COLS:-80}" --rows "${PTY_ROWS:-24}" --timeout 900 \
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
flaky_retry() {  # flaky_retry <name> <cmd>  (recording sandbox only: hypothesis' 200 ms deadline
  # can trip on torch's first call in a busy container — the walk itself hit this in rehearsal;
  # step-05a turns the deadline off. The file keeps a clean run; the retries are logged.)
  local name=$1 i; shift
  for i in 1 2 3; do
    step "$name" "$@"
    grep -q "DeadlineExceeded\|FlakyFailure\|hypothesis.errors.Flaky" "$OUT/$name.txt" || return 0
    mkdir -p "$OUT/capture-only"
    echo "$name: attempt $i hit a hypothesis deadline flake (torch warm-up), re-running" >> "$OUT/capture-only/flaky-retries.txt"
  done
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
  hub_retry step capture-only/base-build "docker build -t python:3.11-slim-bookworm $d"
  rm -rf "$d"
}
CTRLC=$'\x03'

# ---------------------------------------------------------------- Track A (laptop)
if [ "${SEG#a-}" != "$SEG" ]; then
  export PATH="$HOME/venv/bin:$PATH"                      # the laptop's Python (see capture.sh)
  export PIP_CERT=/etc/ssl/certs/ca-certificates.crt     # capture-only: pip behind the TLS proxy
fi
case $SEG in
a-pre)
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; git --version; python3 --version"   # extra
  # --- README "Clone the repository" (README.md:20 names no URL; this is the repo's address)
  step 01-clone "git clone https://github.com/dlops-io/cheese-app-ci-cd.git"
  cd cheese-app-ci-cd
  step 02-git-log "git log -1 --format='%H %ci'"          # extra: the commit the video uses
  step 03-ls "ls -la"                                     # extra: the README's project tree
  capture_only_base
  ;;
a-part1)
  cd cheese-app-ci-cd
  # --- README Part 1: sh docker-shell.sh (README:73), uvicorn inside it (README:82), the three
  # URLs (README:88-90, a browser there; curl from a second terminal here, extra), Ctrl-C, exit
  ( for i in $(seq 420); do (exec 3<>/dev/tcp/127.0.0.1/9000) 2>/dev/null && break; sleep 1; done
    sleep 2
    step part1-02-curl-root "curl -s http://localhost:9000"               # extra
    step part1-03-curl-health "curl -s http://localhost:9000/health"      # extra
    step part1-04-curl-distance "curl -s 'http://localhost:9000/euclidean_distance/?x=3&y=4'"   # extra
  ) &
  CURLS=$!
  PTY_COLS=100 PTY_ROWS=50 istep part1-01-docker-shell "sh docker-shell.sh" \
    ':/app\$ $' "uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload" \
    'euclidean_distance.*200 OK' "$CTRLC" \
    ':/app\$ $' "exit"
  wait $CURLS
  step part1-05-ps-after "docker ps -a"                   # extra: --rm removed it (README:92)
  ;;
a-part2)
  cd cheese-app-ci-cd
  # --- README Part 2, Option A (README:106-112)
  step part2-01-build "docker build -t cheese-app-api:local ."
  step part2-02-flake8 "docker run --rm cheese-app-api:local flake8 --max-line-length=120 api/"
  step part2-03-black "docker run --rm cheese-app-api:local black --check --diff api/"
  # --- README Part 2, Option B (README:118-124)
  step part2-04-pip-install "pip install black flake8"
  step part2-05-flake8-local "flake8 src/api-service/api/"
  step part2-06-black-local "black --check --diff src/api-service/api/"
  ;;
a-part3)
  cd cheese-app-ci-cd
  # --- README Part 3, Option 1 (README:169-181)
  step part3-opt1-01-build "docker build -t cheese-app-api:local ."
  step part3-opt1-02-unit "docker run --rm cheese-app-api:local pytest tests/unit/ -v"
  step part3-opt1-03-integration "docker run --rm cheese-app-api:local pytest tests/integration/ -v"
  step part3-opt1-04-both "docker run --rm cheese-app-api:local pytest tests/unit/ tests/integration/ -v"
  step part3-opt1-05-coverage "docker run --rm cheese-app-api:local pytest tests/unit/ --cov=api --cov-report=term"
  # --- README Part 3, Option 2 (README:190-199)
  step part3-opt2-01-build "docker build -t cheese-app-api:local ."
  step part3-opt2-02-run-server "docker run -d --name api-server -p 9000:9000 -e DEV=1 cheese-app-api:local"
  step part3-opt2-03-wait "until curl -sf http://localhost:9000/health; do sleep 1; done; echo"   # extra: mirrors ci.yml's wait; the README runs the tests right away (see ASSETS.md)
  step part3-opt2-04-ps "docker ps"                       # extra
  step part3-opt2-05-system "docker run --rm --network host cheese-app-api:local pytest tests/system/ -v"
  step part3-opt2-06-cleanup "docker stop api-server && docker rm api-server"
  step part3-opt2-07-system-no-server "docker run --rm --network host cheese-app-api:local pytest tests/system/ -v"   # extra: the same command with no server: the silent skip (README:202)
  # --- README Part 3, Option 3 (README:210-225), typed in the interactive container
  PTY_COLS=100 PTY_ROWS=50 istep part3-opt3-01-shell "sh docker-shell.sh" \
    ':/app\$ $' "pytest tests/unit/ -v" \
    ':/app\$ $' "pytest tests/integration/ -v" \
    ':/app\$ $' "pytest tests/unit/ tests/integration/ -v" \
    ':/app\$ $' "pytest tests/unit/ --cov=api --cov-report=html" \
    ':/app\$ $' "ls htmlcov/ | head -4" \
    ':/app\$ $' "exit"
  ;;
a-part4)
  cd cheese-app-ci-cd
  # capture-only: a git identity, so that a commit can exist (never shown as a step)
  git config --global user.email student@laptop >/dev/null 2>&1
  git config --global user.name student >/dev/null 2>&1
  # --- README Part 4 (README:240-265)
  step part4-01-pip-install-pre-commit "pip install pre-commit"
  step part4-02-pre-commit-install "pre-commit install"
  step part4-03-git-commit-clean 'git commit -m "Your commit message"'   # README:255 order, with a clean tree
  step part4-04-run-all-files "pre-commit run --all-files"
  step part4-05-git-diff "git diff"                       # extra: what black rewrote
  step part4-06-git-add "git add -u"                      # extra: re-stage the hook's fix
  step part4-07-git-commit 'git commit -m "Your commit message"'
  step part4-08-run-staged "pre-commit run"
  step part4-09-git-log "git log --oneline -3"            # extra: the commit exists
  # extras: a commit flake8 blocks (the digest's F401 demo; black cannot fix an unused import)
  step part4-10-break "sed -i '1i import os' src/api-service/api/service.py && git add -u"   # extra
  step part4-11-commit-blocked 'git commit -m "try an unused import"'    # extra
  step part4-12-status "git status"                       # extra: no commit was made
  step part4-13-restore "git restore --staged src/api-service/api/service.py && git restore src/api-service/api/service.py"   # extra
  ;;
a-clean)
  cd cheese-app-ci-cd
  # --- README "Docker Cleanup" (README:568-574)
  step clean-01-container-ls "docker container ls"
  istep clean-02-prune "docker system prune" '\[y/N\] $' y
  step clean-03-image-ls "docker image ls"
  step clean-04-uninstall "pre-commit uninstall"          # extra: not in the README
  ;;

# ---------------------------------------------------------------- Track B (babykev)
b-setup)
  export PATH="$HOME/.local/bin:$PATH"
  step 00-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; head -2 /etc/os-release; git --version"   # extra
  # --- the walk's prerequisites (babykev-walk/README.md:10-14 names uv, git, just, Quarto; the
  # install commands are uv's own and `uv tool install rust-just`, the way babykev's Dockerfile
  # installs just. Quarto is not installed: no step here renders the docs site, and `just setup`
  # says what is missing.)
  step 01-install-uv "curl -LsSf https://astral.sh/uv/install.sh | sh"
  step 02-uv-version "uv --version"                       # extra
  step 03-install-just "uv tool install rust-just"
  step 04-just-version "just --version"                   # extra
  # --- get babykev itself (babykev/README.md:148-150 works "without the page" on a plain clone)
  step 05-clone "git clone https://github.com/rahuldave/babykev"
  cd babykev
  step 06-git-log "git log -1 --format='%H %ci'"          # extra: the commit the video uses
  step 07-tags "git tag -n1 --list 'step-*'"
  # capture-only: a git identity, so the hook demos can attempt commits
  git config --global user.email student@laptop >/dev/null 2>&1
  git config --global user.name student >/dev/null 2>&1
  ;;
b-prewarm)
  # capture-only, NOT part of the walk: fill uv's cache (torch arrives at step-05) and the
  # Hugging Face cache (Qwen/Qwen2.5-0.5B, about 1 GB, which `just smoke local` needs) in a
  # throwaway clone, so the captured steps print cache-hit timings instead of sandbox download
  # times. Logged, kept out of the step files.
  export PATH="$HOME/.local/bin:$PATH"
  mkdir -p "$OUT/capture-only"
  { git clone -q ~/babykev ~/prewarm && cd ~/prewarm && git switch -q --detach step-05 \
      && uv sync --locked && uv run python -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen2.5-0.5B')" \
      && cd ~ && rm -rf ~/prewarm && echo PREWARM-OK; } >> "$OUT/capture-only/prewarm.txt" 2>&1
  ;;
b-s00)
  export PATH="$HOME/.local/bin:$PATH"; cd babykev
  git restore . >/dev/null 2>&1   # capture-only: timewalk's --discard-edits equivalent
  step s00-01-switch "git switch --detach step-00"
  step s00-02-uv-sync "uv sync --locked"
  step s00-03-show-setup "just --show setup"
  step s00-04-setup "just setup"
  step s00-05-just "just"
  step s00-06-help-setup "just help setup"
  step s00-07-babykev-help "uv run babykev help"
  step s00-08-babykev-train "uv run babykev train"
  step s00-09-pyproject "cat pyproject.toml"
  ;;
b-s01)
  export PATH="$HOME/.local/bin:$PATH"; cd babykev
  git restore . >/dev/null 2>&1
  step s01-01-switch "git switch --detach step-01"
  step s01-02-setup "just setup"
  step s01-03-pytest "uv run pytest"
  step s01-04-grep-addopts "grep -n -B1 addopts pyproject.toml"
  step s01-05-show-test "just --show test"
  step s01-06-two-failures 'just test -k "score_confidence_is_zero or rounded_probabilities"'
  step s01-07-help-tests "just test -k help_is_printed -v"
  ;;
b-s02)
  export PATH="$HOME/.local/bin:$PATH"; cd babykev
  git restore . >/dev/null 2>&1
  step s02-01-switch "git switch --detach step-02"
  step s02-02-setup "just setup"
  step s02-03-fix1 "just test -k score_confidence_is_zero"
  step s02-04-fix2 "just test -k rounded_probabilities"
  step s02-05-test "just test"
  step s02-06-missing-line "sed -n '88,91p' src/babykev/api.py"
  step s02-07-fmt-check "uv run ruff format --check"
  step s02-08-show-fmt "just --show fmt"
  step s02-09-fmt "just fmt"
  step s02-10-fmt-check "just fmt --check"
  step s02-11-test "just test"
  step s02-12-lint-stats "uv run ruff check --statistics"
  step s02-13-show-lint "just --show lint"
  step s02-14-lint-fix "just lint --fix"
  step s02-15-lint-unsafe "just lint --fix --unsafe-fixes"
  step s02-16-lint-stats "just lint --statistics"
  step s02-17-fmt-check "just fmt --check"
  step s02-18-test "just test"
  step s02-19-docstring "echo '\"\"\"babykev: a small decision model.\"\"\"' > src/babykev/__init__.py"
  step s02-20-lint-stats "just lint --statistics"
  ;;
b-s03)
  export PATH="$HOME/.local/bin:$PATH"; cd babykev
  git restore . >/dev/null 2>&1
  step s03-01-switch "git switch --detach step-03"
  step s03-02-setup "just setup"
  step s03-03-lint "just lint"
  step s03-04-hooks-dir 'ls "$(git rev-parse --git-path hooks)"'
  step s03-05-hook-file 'cat "$(git rev-parse --git-path hooks)/pre-commit"'
  step s03-06-test "just test"
  step s03-07-single-level "just test -k single_level"
  step s03-08-show-check "just --show check"
  step s03-09-check "just check"
  step s03-10-floor-fail "just test -k confidence --cov-fail-under=90"
  # config files, each checked clean, broken once, checked, restored (walk step-03 E; sed -i on Linux)
  step s03-11-yamllint "uv run yamllint --strict ."
  step s03-12-yaml-break "sed -i 's/^        args: \[--maxkb=1000\]$/          args: [--maxkb=1000]/' .pre-commit-config.yaml"
  step s03-13-yamllint "uv run yamllint --strict ."
  step s03-14-restore "git restore .pre-commit-config.yaml"
  step s03-15-validate "uv run validate-pyproject pyproject.toml"
  step s03-16-pyproject-break "sed -i 's/^requires-python = /requires_python = /' pyproject.toml"
  step s03-17-validate "uv run validate-pyproject pyproject.toml"
  step s03-18-restore "git restore pyproject.toml"
  step s03-19-lock-check "uv lock --check"
  step s03-20-lock-break 'sed -i '"'"'s/"pydantic>=2.11"/"pydantic>=2.12"/'"'"' pyproject.toml'
  step s03-21-lock-check "uv lock --check"
  step s03-22-restore "git restore pyproject.toml"
  step s03-23-justfmt "just --fmt --check --unstable"
  step s03-24-justfile-break 'sed -i '"'"'s/^program := "babykev"/program:="babykev"/'"'"' justfile'
  step s03-25-justfmt "just --fmt --check --unstable"
  step s03-26-restore "git restore justfile"
  step s03-27-show-lint-config "just --show lint-config"
  step s03-28-lint-config "just lint-config"
  step s03-29-hook-config "cat .pre-commit-config.yaml"
  # a bad commit (walk step-03 G), then a secret (H)
  BADIMPORT=$(cat <<'EOS'
perl -pi -e 's/^(from typing)/import os\n$1/' src/babykev/api.py
EOS
)
  step s03-30-bad-import "$BADIMPORT"
  step s03-31-commit-try 'git commit -am "try"'
  step s03-32-status "git status"
  step s03-33-restore "git restore src/babykev/api.py"
  step s03-34-env-add "echo X=1 > .env && git add -f .env"
  step s03-35-commit-try 'git commit -m "try"'
  step s03-36-env-undo "git rm --cached -q .env && rm .env"
  ;;
b-s04)
  export PATH="$HOME/.local/bin:$PATH"; cd babykev
  git restore . >/dev/null 2>&1
  step s04-01-switch "git switch --detach step-04"
  step s04-02-setup "just setup"
  step s04-03-docs-list "uv run babykev docs list"
  step s04-04-docs-check "just docs check"
  ;;
b-s04b)
  export PATH="$HOME/.local/bin:$PATH"; cd babykev
  git restore . >/dev/null 2>&1
  step s04b-01-switch "git switch --detach step-04b"
  step s04b-02-setup "just setup"
  step s04b-03-docs-check "just docs check"
  step s04b-04-docment "sed -n '68,72p' src/babykev/api.py"
  step s04b-05-show-check "just --show check"
  step s04b-06-check "just check"
  # delete one docment, watch the check and then the hook catch it (walk step-04b F-G)
  step s04b-07-del-docment "sed -i 's|,  # How deeply nested.*|,|' src/babykev/api.py"
  step s04b-08-docs-check "just docs check"
  step s04b-09-commit-try 'git commit -am "try"'
  step s04b-10-status "git status"
  step s04b-11-restore "git restore src/babykev/api.py"
  ;;
b-s05)
  export PATH="$HOME/.local/bin:$PATH"; cd babykev
  git restore . >/dev/null 2>&1
  step s05-01-switch "git switch --detach step-05"
  step s05-02-setup "just setup"
  flaky_retry s05-03-test "just test"
  MASKPRINT=$(cat <<'EOS'
uv run python -c "from babykev.model import branch_mask; m = branch_mask([0, 0, 1, 1, 2, 2], 'cpu')[0, 0] == 0; print('\n'.join(''.join('#' if x else '.' for x in r) for r in m))"
EOS
)
  step s05-04-mask-print "$MASKPRINT"
  step s05-05-mask-line "sed -n '140p' src/babykev/model.py"
  MASKCMP=$(cat <<'EOS'
uv run python - <<'EOF'
from babykev.model import branch_mask
picture = ["#.....", "##....", "###...", "####..", "##..#.", "##..##"]
mask = branch_mask([0, 0, 1, 1, 2, 2], "cpu")[0, 0] == 0
rows = ["".join("#" if ok else "." for ok in row) for row in mask]
for want, got in zip(picture, rows, strict=True): print(want, got, "ok" if want == got else "WRONG")
EOF
EOS
)
  step s05-06-mask-compare "$MASKCMP"
  step s05-07-ty "uv run ty check"
  step s05-08-show-types "just --show types"
  step s05-09-types "just types"
  step s05-10-show-check "just --show check"
  step s05-11-check "just check"
  PTY_COLS=100 istep s05-12-smoke "just smoke local"   # in a terminal: the loading bar redraws
  ;;
b-s05a)
  export PATH="$HOME/.local/bin:$PATH"; cd babykev
  git restore . >/dev/null 2>&1
  step s05a-01-switch "git switch --detach step-05a"
  step s05a-02-setup "just setup"
  step s05a-03-test "just test"
  WRONGFIX=$(cat <<'EOS'
perl -pi -e 's/^    same = \(s\[None, :\] == s\[:, None\]\) \| \(s\[None, :\] == 0\)$/    same = (s[None, :] == s[:, None]) | (s[None, :] == 0) | (s[None, :] < s[:, None] - 1)/' src/babykev/model.py
EOS
)
  MASKBACK=$(cat <<'EOS'
perl -pi -e 's/^    same = \(s\[None, :\] == s\[:, None\]\) \| \(s\[None, :\] == 0\)$/    same = torch.ones_like(causal) | (s[None, :] == 0)/' src/babykev/model.py
EOS
)
  CMP6=$(cat <<'EOS'
uv run python - <<'EOF'
from babykev.model import branch_mask
picture = ["#.....", "##....", "###...", "####..", "##..#.", "##..##"]
mask = branch_mask([0, 0, 1, 1, 2, 2], "cpu")[0, 0] == 0
rows = ["".join("#" if ok else "." for ok in row) for row in mask]
for want, got in zip(picture, rows, strict=True): print(want, got, "ok" if want == got else "WRONG")
EOF
EOS
)
  CMP4=$(cat <<'EOS'
uv run python - <<'EOF'
from babykev.model import branch_mask
picture = ["#...", "##..", "#.#.", "#..#"]
mask = branch_mask([0, 1, 2, 3], "cpu")[0, 0] == 0
rows = ["".join("#" if ok else "." for ok in row) for row in mask]
for want, got in zip(picture, rows, strict=True): print(want, got, "ok" if want == got else "WRONG")
EOF
EOS
)
  step s05a-04-wrong-fix "$WRONGFIX"
  step s05a-05-six-tokens "$CMP6"
  step s05a-06-four-tokens "$CMP4"
  step s05a-07-rule "sed -n '58,65p' tests/unit/test_mask.py"
  step s05a-08-hypothesis "just test -k no_question_sees_another"
  step s05a-09-restore "git restore src/babykev/model.py"
  step s05a-10-mask-back "$MASKBACK"
  step s05a-11-test "just test"
  step s05a-12-restore "git restore src/babykev/model.py"
  step s05a-13-fix-line "sed -n '151p' src/babykev/model.py"
  step s05a-14-types "just types"
  step s05a-15-show-check "just --show check"
  step s05a-16-check "just check"
  PTY_COLS=100 istep s05a-17-smoke "just smoke local"   # in a terminal: the loading bar redraws
  ;;
b-s05b)
  export PATH="$HOME/.local/bin:$PATH"; cd babykev
  git restore . >/dev/null 2>&1
  step s05b-01-switch "git switch --detach step-05b"
  step s05b-02-setup "just setup"
  step s05b-03-test "just test"
  step s05b-04-marker "sed -n '53,57p' pyproject.toml"
  step s05b-05-system-file "sed -n '1,27p' tests/system/test_real_model.py"
  PTY_COLS=100 istep s05b-06-test-system "just test -m system"   # in a terminal: the loading bar redraws
  step s05b-07-hadolint "uv run hadolint Dockerfile"
  DL3059=$(cat <<'EOS'
perl -pi -e 's/^RUN uv tool install "rust-just==\$\{JUST\}" \\$/RUN uv tool install "rust-just==\${JUST}"/; s/^    && git config /RUN git config /' Dockerfile
EOS
)
  step s05b-08-dl3059-break "$DL3059"
  PTY_COLS=110 istep s05b-09-hadolint "uv run hadolint Dockerfile"   # in a terminal (colours dropped)
  step s05b-10-restore "git restore Dockerfile"
  step s05b-11-dl3008-lines "sed -n '46,48p' Dockerfile"
  DL3008=$(cat <<'EOS'
perl -ni -e 'print unless /^# hadolint ignore=DL3008$/' Dockerfile
EOS
)
  step s05b-12-dl3008-break "$DL3008"
  PTY_COLS=110 istep s05b-13-hadolint "uv run hadolint Dockerfile"   # in a terminal (colours dropped)
  step s05b-14-restore "git restore Dockerfile"
  step s05b-15-show-lint-config "just --show lint-config"
  step s05b-16-lint-config "just lint-config"
  step s05b-17-check "just check"
  # the walk's Docker section, on this laptop WITHOUT Docker (the honest refusals; the walk's own
  # outputs for these steps are recorded in ASSETS.md as `recorded`)
  step s05b-18-docker-build "docker build --target run --tag babykev-run ."   # extra: no Docker here
  step s05b-19-image-build "just image build run"          # extra: the recipe says so itself
  ;;
*)
  echo "run_steps.sh: unknown segment $SEG" >&2; exit 2 ;;
esac
