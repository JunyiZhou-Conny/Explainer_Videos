#!/bin/bash
# Runs inside a fresh debian container as user `student`, recording each tutorial command's output.
# Usage: run_steps.sh <out_dir> <part>   part = A (manual install) | B (uv)
OUT=$1; PART=$2
cd ~
step() {  # step <name> <command...>
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1; echo "[exit $?]"; } | grep -v "^WARNING: apt does not have a stable CLI interface" > "$OUT/$PART-$name.txt"
}
step 00-os "cat /etc/os-release | head -4; python3 --version; which python; echo which-python-exit:\$?"
if [ "$PART" = A ]; then
  step 01-apt-update "sudo apt-get update"
  step 02-git "yes | sudo apt install git"
  step 03-clone "git clone https://github.com/dlops-io/simple-translate.git"
  cd simple-translate
  step 04-ls "ls"
  step 05-pip "yes | sudo apt install python3-pip"
  step 06-pip-version "pip3 --version"
  step 07-pip-refused "pip3 install googletrans==4.0.2 art"
  step 08-pip-break "sudo pip3 install --break-system-packages googletrans==4.0.2 art"
  step 09-where "python3 -c 'import googletrans; print(googletrans.__file__)'"
  step 10-run-default "python3 cli.py"
  step 11-run-es "python3 cli.py -t \"Good morning. It is a good morning for cheese.\" -s \"en\" -d \"es\""
  step 12-run-fr "python3 cli.py -t \"Good afternoon. Would you like some cheese?\" -s \"en\" -d \"fr\""
  step 13-help "python3 cli.py --help"
  step 14-badlang "python3 cli.py -t hello -d xx"
  step 15-syspath "python3 -c 'import sys; print(\"\\n\".join(sys.path))'"
else
  step 01-apt-update "sudo apt-get update"
  step 02-git "yes | sudo apt install git"
  step 03-clone "git clone https://github.com/dlops-io/simple-translate.git"
  cd simple-translate
  step 04-ls "ls -a"
  step 05-uv-install "curl -LsSf https://astral.sh/uv/install.sh | sh"
  step 06-uv-missing "uv --version"
  source $HOME/.local/bin/env
  step 07-uv-version "source \$HOME/.local/bin/env; uv --version; which uv"
  step 08-uv-sync "uv sync"
  step 09-ls-after "ls -a"
  step 10-pyvenv "cat .venv/pyvenv.cfg"
  step 11-venv-bin "ls -la .venv/bin"
  step 12-python-before "which python; echo exit:\$?; echo \$PATH | tr ':' '\n'"
  step 13-activate "source .venv/bin/activate; which python; python --version; which pip; echo pip-exit:\$?; echo \$PATH | tr ':' '\n' | head -3; echo VIRTUAL_ENV=\$VIRTUAL_ENV"
  step 14-run-default "source .venv/bin/activate; python cli.py"
  step 15-run-es "source .venv/bin/activate; python cli.py -t \"Good morning. It is a good morning for cheese.\" -s \"en\" -d \"es\""
  step 16-run-fr "source .venv/bin/activate; python cli.py -t \"Good afternoon. Would you like some cheese?\" -s \"en\" -d \"fr\""
  step 17-tree "uv tree"
  step 18-lock-head "head -30 uv.lock; grep -c '^\[\[package\]\]' uv.lock"
  step 19-git-status "git status"
  step 20-isolation "python3 -c 'import googletrans'"
  step 21-uv-run "uv run python -c 'import googletrans, sys; print(sys.prefix)'"
  step 22-syspath-venv "source .venv/bin/activate; python -c 'import sys; print(\"\\n\".join(sys.path))'"
  step 23-resync "uv sync"
  step 24-du "du -sh .venv ~/.local/share/uv/python 2>/dev/null; ls ~/.local/share/uv/python 2>/dev/null"
  step 25-activate-file "ls -l .venv/bin/activate; grep -n 'PATH=\|VIRTUAL_ENV_PROMPT=\|^VIRTUAL_ENV=' .venv/bin/activate | head"
  step 26-startup-files "grep -n local/bin ~/.profile ~/.bashrc; cat ~/.local/bin/env"
fi
