"""Read narration straight from a video's script.md, so the script is the single source of truth.

script.md format (see videos/*/script.md):

    ## S04 · Defining privacy — `s04_definition.py` · `Definition`
    SHOW: what is on screen ...
    SAY: The exact words the narrator speaks.

`load_narration(path)` -> {"S04": ["first SAY line", "second SAY line", ...], ...}
"""

from __future__ import annotations

import re
from pathlib import Path

_HEADER = re.compile(r"^##\s+(S\d+)\b")


def load_narration(path: str | Path) -> dict[str, list[str]]:
    out: dict[str, list[str]] = {}
    current = None
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        m = _HEADER.match(line)
        if m:
            current = m.group(1)
            out[current] = []
        elif current and line.startswith("SAY:"):
            out[current].append(line[4:].strip())
    return out


def word_count(path: str | Path) -> dict[str, int]:
    return {k: sum(len(s.split()) for s in v) for k, v in load_narration(path).items()}


def synthesize_all(path: str | Path) -> float:
    """Pre-render every SAY line with the configured TTS backend (fills the cache). Returns seconds."""
    from .voice import get_backend

    backend, total = get_backend(), 0.0
    for scene, lines in load_narration(path).items():
        for i, line in enumerate(lines):
            clip = backend.speak(" ".join(line.split()))   # same normalisation as VoiceScene
            total += clip.duration
            print(f"{scene}[{i}] {clip.duration:5.1f}s  {line[:60]}", flush=True)
    return total


if __name__ == "__main__":  # python -m explainer.script videos/<id>/script.md [--synth]
    import sys

    if "--synth" in sys.argv:
        secs = synthesize_all(sys.argv[1])
        print(f"narration total: {secs / 60:.1f} min")
        raise SystemExit
    counts = word_count(sys.argv[1])
    for k, v in counts.items():
        print(f"{k}: {v:4d} words  ~{v / 155:4.1f} min")
    total = sum(counts.values())
    print(f"total: {total} words  ~{total / 155:.1f} min of narration")
