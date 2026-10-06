#!/usr/bin/env bash
# One-shot setup: system packages, Python venv, Kokoro voice model.
#   bash setup/install.sh            # Ubuntu/Debian (uses apt) or macOS (uses brew)
#   VENV=.venv bash setup/install.sh # choose the venv location (default .venv)
set -euo pipefail
cd "$(dirname "$0")/.."
VENV="${VENV:-.venv}"
MODEL_DIR="${KOKORO_MODEL_DIR:-$HOME/.cache/explainer/kokoro}"

if command -v apt-get >/dev/null; then
  SUDO=$([ "$(id -u)" = 0 ] && echo "" || echo sudo)
  $SUDO apt-get update
  $SUDO apt-get install -y --no-install-recommends \
    ffmpeg poppler-utils espeak-ng pkg-config libcairo2-dev libpango1.0-dev \
    texlive-latex-base texlive-latex-extra texlive-latex-recommended texlive-fonts-recommended \
    texlive-science dvisvgm cm-super fonts-cmu python3-venv python3-dev
  # Chinese versions (EXPLAINER_LANG=zh): CJK fonts for labels/subtitles, XeLaTeX + ctex for maths
  $SUDO apt-get install -y --no-install-recommends fonts-noto-cjk texlive-xetex texlive-lang-chinese
elif command -v brew >/dev/null; then
  brew install ffmpeg poppler espeak-ng pkg-config cairo pango
  brew install --cask mactex-no-gui font-computer-modern font-noto-sans-cjk-sc font-noto-serif-cjk-sc || true
else
  echo "Install ffmpeg, poppler, espeak-ng, cairo, pango and a LaTeX distribution manually." >&2
fi

python3 -m venv "$VENV"
"$VENV/bin/pip" install --upgrade pip
"$VENV/bin/pip" install -r requirements.txt

mkdir -p "$MODEL_DIR"
for f in kokoro-v1.0.onnx voices-v1.0.bin; do
  [ -s "$MODEL_DIR/$f" ] || curl -L --fail -o "$MODEL_DIR/$f" \
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/$f"
done

echo
echo "Done. Activate with:  source $VENV/bin/activate"
echo "Kokoro model in:      $MODEL_DIR   (export KOKORO_MODEL_DIR=$MODEL_DIR if you moved it)"
echo "Try:                  python -m explainer.voice 'Calibrating noise to sensitivity.'"
