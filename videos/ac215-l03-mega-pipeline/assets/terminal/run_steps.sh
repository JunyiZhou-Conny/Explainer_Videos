#!/bin/bash
# Runs the L03 README (dlops-io/mega-pipeline, branch main) one command at a time on "your laptop" and saves
# each command's output to its own file: "$ cmd", the output, "[exit N]". Called by capture.sh, which builds
# the capture-only images and exports DOCKER_CONFIG. Usage:
#   run_steps.sh <terminal_dir> <laptop_home> <part>      part = a | a2 | b | c | d | e | final
# Folders written: laptop/ (the laptop's terminal: git, uv, docker) and one folder per component for the
# commands typed at the container's prompt (app@<id>:/app$).
HERE=$1; LHOME=$2; PART=$3
OUT=$HERE
LAPTOP_IMG=l03-capture/laptop:debian12
CAPTURE_FROM=l03-capture/python:3.12-slim-bookworm
clean() { sed -r 's/\x1b\[[0-9;?]*[A-Za-z]//g'; }

# lstep <folder> <name> <dir under ~> <command>: typed in the laptop's terminal (git, uv, ls, cat). Runs as
# `student` (uid 1000) in a fresh "laptop" container whose home is <laptop_home>; bash -l = a new terminal.
lstep() {
  local f=$1 name=$2 dir=$3; shift 3; mkdir -p "$OUT/$f"
  { echo "\$ $*"
    docker run --rm --network host --hostname laptop -e https_proxy -e HTTPS_PROXY -e no_proxy -e NO_PROXY \
      -v "$LHOME":/home/student -w "/home/student/$dir" -u student "$LAPTOP_IMG" bash -lc "$*" 2>&1 </dev/null
    echo "[exit $?]"; } | clean > "$OUT/$f/$name.txt"
}
# dstep <folder> <name> <dir under ~> <command>: a docker command typed in the same terminal. It runs on this
# machine's Docker Engine (the laptop's Docker), from the same folder, so "$(pwd)" is that folder.
dstep() {
  local f=$1 name=$2 dir=$3; shift 3; mkdir -p "$OUT/$f"
  { echo "\$ $*"; (cd "$LHOME/$dir" && bash -c "$*") 2>&1 </dev/null; echo "[exit $?]"; } | clean > "$OUT/$f/$name.txt"
}
# tstep <folder> <name> <dir under ~> <typed lines> <command>: an interactive command in a real terminal
# (a pseudo-terminal, 80x40); the lines are typed one by one, each after the shell prompt appears.
# $PYTHON (default python3) runs tty_session.py; give it one with `pyte` for builds' live progress view.
tstep() {
  local f=$1 name=$2 dir=$3 typed=$4; shift 4; mkdir -p "$OUT/$f"
  local tf; tf=$(mktemp); printf '%s\n' "$typed" > "$tf"
  (cd "$LHOME/$dir" && SHOW_CMD="$*" "${PYTHON:-python3}" -I "$HERE/tty_session.py" "$OUT/$f/$name.txt" "$tf" bash -c "$*")
  rm -f "$tf"
}
# bstep <folder> <name> <dir under ~> <build command>: a docker build typed in a real terminal. <name>.txt is
# what the terminal shows when it ends (BuildKit's live progress view, rendered by tty_session.py with pyte);
# <name>.plain.txt is the same build's full step-by-step log, replayed from Docker's build history.
bstep() {
  local f=$1 name=$2 dir=$3; shift 3
  local since; since=$(date -u +%Y-%m-%dT%H:%M:%S)
  tstep "$f" "$name" "$dir" "" "$*"
  local ref r
  for r in $(docker buildx history ls --format json | python3 -c '
import json, sys
recs = [json.loads(l) for l in sys.stdin if l.strip()]
for d in sorted(recs, key=lambda d: d["created_at"], reverse=True):
    if d["created_at"][:19] >= sys.argv[1]:
        print(d["ref"].split("/")[-1])' "$since"); do
    if docker buildx history inspect "$r" 2>/dev/null | grep -q "l03-capture/python"; then ref=$r; break; fi
  done
  dstep "$f" "$name.plain" "$dir" "docker buildx history logs $ref"
}
# csession <folder> <dir under ~> <image> <name> <cmd> [<name> <cmd>]...: commands typed at the container's
# prompt. ONE container for the whole list, started like the README's `docker run --rm -ti -v "$(pwd):/app"
# <image>` but with -i (no terminal here) and --network host (uv reaches PyPI through the capture proxy);
# the image's own CMD activates the venv and its bash reads the commands from stdin.
csession() {
  local f=$1 dir=$2 img=$3; shift 3; mkdir -p "$OUT/$f"
  local script="" name cmd
  while [ $# -gt 0 ]; do
    name=$1; cmd=$2; shift 2
    script+="echo '@@STEP $name'; printf '%s\n' $(printf '%q' "\$ $cmd"); ( $cmd ) 2>&1 </dev/null; echo \"[exit \$?]\""$'\n'
  done
  (cd "$LHOME/$dir" && printf '%s' "$script" | docker run --rm -i --network host -v "$(pwd):/app" "$img" 2>&1) | clean |
    awk -v d="$OUT/$f" '/^@@STEP /{file=d"/"$2".txt"; next} file{print > file; next} {print "csession: " $0 > "/dev/stderr"}'
}
# the Dockerfile a student writes from the component README (transcribe_audio/README.md:41-90 and the same
# section of the others), code blocks in order, FROM line from the prose at :41. files/ keeps this version;
# the folder gets the capture copy, whose line 1 is the capture base instead (same line count).
write_dockerfile() {  # write_dockerfile <component dir> <DEBIAN_PACKAGES value>
  mkdir -p "$OUT/files"
  local name; name=$(basename "$1")
  cat > "$OUT/files/$name.Dockerfile" <<EOF
FROM python:3.12-slim-bookworm

ARG DEBIAN_PACKAGES="$2"

ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv
ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json

RUN apt-get update && \\
    apt-get upgrade -y && \\
    apt-get install -y --no-install-recommends \$DEBIAN_PACKAGES && \\
    apt-get clean && \\
    rm -rf /var/lib/apt/lists/* && \\
    pip install --no-cache-dir --upgrade pip && \\
    pip install uv && \\
    useradd -ms /bin/bash app -d /home/app -u 1000 && \\
    mkdir -p /app && \\
    chown app:app /app

USER app
WORKDIR /app

COPY --chown=app:app . ./
RUN uv sync

ENTRYPOINT ["/bin/bash"]
CMD ["-c", "source /home/app/.venv/bin/activate && exec bash"]
EOF
  sed "1s|.*|FROM $CAPTURE_FROM|" "$OUT/files/$name.Dockerfile" > "$LHOME/$1/Dockerfile"
  chown 1000:1000 "$LHOME/$1/Dockerfile"
}
keep_file() {  # keep_file <path under ~> <name in files/>
  cp "$LHOME/$1" "$OUT/files/$2"
}
MP=mega-pipeline

case $PART in
a)  # ---- README.md: Clone this Repository; Component A: transcribe_audio ----
  lstep laptop 00-laptop "" "head -4 /etc/os-release; python3 --version; git --version; date -u '+%Y-%m-%d %H:%M UTC'"
  dstep laptop 01-docker-version "" "docker version"
  dstep laptop 02-base-image "" "docker pull python:3.12-slim-bookworm; docker run --rm python:3.12-slim-bookworm python --version"
  lstep laptop 03-clone "" "git clone https://github.com/dlops-io/mega-pipeline.git"
  lstep laptop 04-ls $MP "ls; git log --oneline -1; git branch"
  lstep laptop 05-ls-components $MP "ls -a transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio"
  lstep laptop 06-uv-missing $MP/transcribe_audio "uv --version"
  lstep laptop 07-uv-install $MP/transcribe_audio "curl -LsSf https://astral.sh/uv/install.sh | sh"
  lstep laptop 08-uv-version $MP/transcribe_audio "uv --version"
  lstep laptop 09-uv-init $MP/transcribe_audio "uv init --bare"
  lstep laptop 10-cat-pyproject $MP/transcribe_audio "cat pyproject.toml"
  write_dockerfile $MP/transcribe_audio "build-essential ffmpeg"
  lstep laptop 11-ls-before-build $MP/transcribe_audio "ls -a; git status"
  dstep laptop 12-build $MP/transcribe_audio "docker build --network host -t transcribe_audio ."
  dstep laptop 13-images $MP/transcribe_audio "docker images transcribe_audio"
  tstep transcribe_audio 01-docker-run-tty $MP/transcribe_audio \
    "$(printf '%s\n' 'which python' 'python --version' 'ls -a' 'echo $GOOGLE_APPLICATION_CREDENTIALS' 'python cli.py --help' 'exit')" \
    'docker run --rm -ti -v "$(pwd):/app" transcribe_audio'
  ;;
a2)  # ---- Component A continued: inside the container, rebuild ----
  # "Change the group name in cli.py" (transcribe_audio/README.md:114): an edit in VS Code on the laptop, made
  # before the container below starts (a piped session can't pause for it); the container sees it via the mount
  sed -i 's/^group_name = "pavlos"/group_name = "group-01"/' "$LHOME/$MP/transcribe_audio/cli.py"
  csession transcribe_audio $MP/transcribe_audio transcribe_audio \
    02-uv-add 'uv add google-cloud-storage google-cloud-speech ffmpeg-python' \
    03-cat-pyproject 'cat pyproject.toml' \
    04-ls 'ls -la' \
    05-help 'python cli.py --help' \
    06-group-name 'grep -n "^group_name" cli.py' \
    07-download 'python cli.py --download' \
    08-ls-after-download 'ls -la input_audios text_prompts text_prompts/*' \
    09-uv-tree 'uv tree --depth 1' \
    10-venv-where 'which python; echo $VIRTUAL_ENV; ls /home/app/.venv/lib/python3.12/site-packages | head -5'
  keep_file $MP/transcribe_audio/pyproject.toml transcribe_audio.pyproject.toml
  lstep laptop 14-host-after-uv-add $MP/transcribe_audio "ls -a; cat pyproject.toml; head -c 300 uv.lock; echo; wc -c uv.lock; git status --short"
  # G10: a new container from the image that was built before `uv add`
  csession transcribe_audio $MP/transcribe_audio transcribe_audio \
    11-g10-new-container 'python cli.py --help'
  bstep laptop 15-rebuild $MP/transcribe_audio "docker build --network host -t transcribe_audio ."
  dstep laptop 16-images-after $MP/transcribe_audio "docker images transcribe_audio"
  dstep laptop 17-history $MP/transcribe_audio "docker history transcribe_audio"
  csession transcribe_audio $MP/transcribe_audio transcribe_audio \
    12-after-rebuild 'python -c "import google.cloud.storage, google.cloud.speech, ffmpeg; print(\"imports ok\")"; uv --version; python --version'
  # gotchas (not in the README)
  dstep laptop 18-g16-entrypoint $MP/transcribe_audio 'docker run --rm -v "$(pwd):/app" transcribe_audio python cli.py -d'
  dstep laptop 19-g16-fix $MP/transcribe_audio 'docker run --rm -v "$(pwd):/app" transcribe_audio -c "source /home/app/.venv/bin/activate && python cli.py --help"'
  # G1: a stand-in file where the Canvas key goes (its content says it is a placeholder; no key exists here)
  printf '{"placeholder": "stands in for the Canvas key in this capture; not a credential"}\n' > "$LHOME/$MP/transcribe_audio/secrets/mega-pipeline.json"
  chown 1000:1000 "$LHOME/$MP/transcribe_audio/secrets/mega-pipeline.json"
  lstep laptop 20-g1-git-ignores-key $MP/transcribe_audio "ls secrets; git status --short; git check-ignore -v secrets/mega-pipeline.json"
  dstep laptop 21-g1-rebuild-with-key $MP/transcribe_audio "docker build --network host -t transcribe_audio ."
  dstep laptop 22-g1-key-in-image $MP/transcribe_audio "docker run --rm --entrypoint ls transcribe_audio -la /app/secrets"
  printf 'secrets/\n' > "$LHOME/$MP/transcribe_audio/.dockerignore"; chown 1000:1000 "$LHOME/$MP/transcribe_audio/.dockerignore"
  lstep laptop 23-g1-dockerignore $MP/transcribe_audio "cat .dockerignore"
  dstep laptop 24-g1-rebuild-dockerignore $MP/transcribe_audio "docker build --network host -t transcribe_audio ."
  dstep laptop 25-g1-key-not-in-image $MP/transcribe_audio "docker run --rm --entrypoint ls transcribe_audio -la /app/secrets"
  rm -f "$LHOME/$MP/transcribe_audio/secrets/mega-pipeline.json" "$LHOME/$MP/transcribe_audio/.dockerignore"
  # G21: building before `uv init --bare` (a copy of the folder without pyproject.toml)
  mkdir -p "$LHOME/g21"; (cd "$LHOME/$MP/transcribe_audio" && cp -a README.md cli.py .gitignore secrets Dockerfile "$LHOME/g21/")
  chown -R 1000:1000 "$LHOME/g21"
  dstep laptop 26-g21-no-pyproject g21 "docker build --network host -t transcribe_audio ."
  # G7: the same folder owned by root (Linux host or VM working as root): the container's uid 1000 can't write
  mkdir -p "$LHOME/g7"; cp -a "$LHOME/$MP/transcribe_audio/." "$LHOME/g7/"; chown -R 0:0 "$LHOME/g7"
  csession transcribe_audio g7 transcribe_audio 13-g7-root-owned 'ls -ld /app; id; uv add requests'
  rm -rf "$LHOME/g21" "$LHOME/g7"
  ;;
b)  # ---- Component B: generate_text ----
  lstep laptop 30-b-ls $MP/generate_text "ls -a; cat pyproject.toml"
  lstep laptop 31-b-uv-init $MP/generate_text "uv init --bare"
  write_dockerfile $MP/generate_text "build-essential"
  bstep laptop 32-b-build $MP/generate_text "docker build --network host -t generate_text ."
  csession generate_text $MP/generate_text generate_text \
    01-python-version 'which python; python --version; readlink -f $(which python)' \
    02-uv-add 'uv add google-cloud-storage google-genai' \
    03-cat-pyproject 'cat pyproject.toml' \
    04-help 'python cli.py --help'
  bstep laptop 33-b-rebuild $MP/generate_text "docker build --network host -t generate_text ."
  # the fix for G3 (not in the README): requires-python ">=3.12", then rebuild
  sed -i 's/^requires-python = ">=3.14"/requires-python = ">=3.12"/' "$LHOME/$MP/generate_text/pyproject.toml"
  lstep laptop 34-b-fix-requires-python $MP/generate_text "grep -n requires-python pyproject.toml; git status --short ."
  bstep laptop 35-b-rebuild-312 $MP/generate_text "docker build --network host -t generate_text ."
  csession generate_text $MP/generate_text generate_text \
    05-python-version-312 'python --version; readlink -f $(which python)' \
    06-help-312 'python cli.py --help'
  ;;
c)  # ---- Component C: synthesis_audio_en ----
  lstep laptop 40-c-uv-init $MP/synthesis_audio_en "uv init --bare; cat pyproject.toml"
  write_dockerfile $MP/synthesis_audio_en "build-essential"
  bstep laptop 41-c-build $MP/synthesis_audio_en "docker build --network host -t synthesis_audio_en ."
  csession synthesis_audio_en $MP/synthesis_audio_en synthesis_audio_en \
    01-uv-add 'uv add google-cloud-storage google-cloud-texttospeech' \
    02-cat-pyproject 'cat pyproject.toml' \
    03-help 'python cli.py --help'
  keep_file $MP/synthesis_audio_en/pyproject.toml synthesis_audio_en.pyproject.toml
  bstep laptop 42-c-rebuild $MP/synthesis_audio_en "docker build --network host -t synthesis_audio_en ."
  ;;
d)  # ---- Component D: translate_text ----
  lstep laptop 50-d-uv-init $MP/translate_text "uv init --bare; cat pyproject.toml"
  write_dockerfile $MP/translate_text "build-essential"
  bstep laptop 51-d-build $MP/translate_text "docker build --network host -t translate_text ."
  csession translate_text $MP/translate_text translate_text \
    01-uv-add 'uv add google-cloud-storage google-cloud-translate' \
    02-cat-pyproject 'cat pyproject.toml' \
    03-help 'python cli.py --help'
  keep_file $MP/translate_text/pyproject.toml translate_text.pyproject.toml
  bstep laptop 52-d-rebuild $MP/translate_text "docker build --network host -t translate_text ."
  ;;
e)  # ---- Component E: synthesis_audio (+ the optional ElevenLabs bonus) ----
  lstep laptop 60-e-uv-init $MP/synthesis_audio "uv init --bare; cat pyproject.toml"
  write_dockerfile $MP/synthesis_audio "build-essential"
  bstep laptop 61-e-build $MP/synthesis_audio "docker build --network host -t synthesis_audio ."
  csession synthesis_audio $MP/synthesis_audio synthesis_audio \
    01-uv-add 'uv add google-cloud-storage google-cloud-texttospeech' \
    02-cat-pyproject 'cat pyproject.toml' \
    03-help 'python cli.py --help' \
    04-bonus-uv-add-requests 'uv add requests' \
    05-bonus-cli11-download 'python cli_11.py --download'
  keep_file $MP/synthesis_audio/pyproject.toml synthesis_audio.pyproject.toml
  bstep laptop 62-e-rebuild $MP/synthesis_audio "docker build --network host -t synthesis_audio ."
  ;;
final)  # ---- all five images; what Git sees; cleanup (not in the README) ----
  dstep laptop 70-images-all "" "docker image ls --filter reference=transcribe_audio --filter reference=generate_text --filter reference=synthesis_audio_en --filter reference=translate_text --filter reference=synthesis_audio"
  lstep laptop 71-git-status $MP "git status"
  dstep laptop 72-cleanup "" "docker image rm transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio"
  ;;
esac
