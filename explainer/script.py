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


def compare_lang(path: str | Path, lang: str, tolerance: float = 0.15) -> None:
    """Synthesize a language version's narration (fills the TTS cache for the render) and compare
    every SAY block's duration with the English one: VoiceScene waits for each clip, so a much
    longer translation holds the frame and a much shorter one leaves silence after animations."""
    import os

    import yaml

    from . import i18n
    from .build import scene_env
    from .voice import get_backend

    path = Path(path).resolve()
    project = path.parent
    spec = yaml.safe_load((project / "video.yaml").read_text())
    saved = dict(os.environ)
    try:
        os.environ.update({k: v for k, v in scene_env(spec, None, "en").items() if k.startswith("EXPLAINER_")})
        en_backend = get_backend()
        os.environ.update({k: v for k, v in scene_env(spec, None, lang).items() if k.startswith("EXPLAINER_")})
        os.environ["EXPLAINER_PROJECT"] = str(project)
        tr_backend = get_backend()
        table = i18n.narration(lang, project)
        tot_en = tot_tr = 0.0
        flagged = 0
        for scene, lines in load_narration(path).items():
            for i, line in enumerate(lines):
                key = " ".join(line.split())
                en = en_backend.speak(key).duration
                t = table.get(key)
                if t is None:
                    print(f"{scene}[{i}] MISSING translation")
                    continue
                tr = tr_backend.speak_aligned(t).duration
                tot_en, tot_tr = tot_en + en, tot_tr + tr
                r = tr / max(0.1, en)
                flag = "  <-- " + ("longer" if r > 1 else "shorter") if abs(r - 1) > tolerance else ""
                flagged += bool(flag)
                print(f"{scene}[{i}] en {en:5.1f}s  {lang} {tr:5.1f}s  x{r:4.2f}{flag}   {t.sentences[0][:30]}",
                      flush=True)
        print(f"total: en {tot_en / 60:.1f} min, {lang} {tot_tr / 60:.1f} min (x{tot_tr / max(1, tot_en):.2f}); "
              f"{flagged} block(s) outside ±{tolerance:.0%}")
    finally:
        os.environ.clear()
        os.environ.update(saved)


if __name__ == "__main__":  # python -m explainer.script videos/<id>/script.md [--synth] [--lang zh]
    import sys

    if "--lang" in sys.argv:
        compare_lang(sys.argv[1], sys.argv[sys.argv.index("--lang") + 1])
        raise SystemExit
    if "--synth" in sys.argv:
        secs = synthesize_all(sys.argv[1])
        print(f"narration total: {secs / 60:.1f} min")
        raise SystemExit
    counts = word_count(sys.argv[1])
    for k, v in counts.items():
        print(f"{k}: {v:4d} words  ~{v / 155:4.1f} min")
    total = sum(counts.values())
    print(f"total: {total} words  ~{total / 155:.1f} min of narration")
