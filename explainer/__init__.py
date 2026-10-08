"""explainer — a small toolkit for 3Blue1Brown-style paper explainer videos.

Pieces:
    explainer.voice       text-to-speech backends (Kokoro local, ElevenLabs, edge-tts, espeak, silent)
    explainer.scene       VoiceScene: a Manim Scene whose animations are timed to narration
    explainer.style       the shared colour palette and typography
    explainer.components  reusable visuals (database tables, paper cards, lineage maps, ...)
    explainer.build       render a whole video project -> mp4 + subtitles + chapters
    explainer.preview     quick low-res render + contact sheet for checking a scene's layout
    explainer.events      the render-time event log every scene writes (<Scene>.events.json)
    explainer.short       the short format: BeatScene (beat grid, captions, HUD, camera), glow,
                          particles, rolling counters (docs/SHORTS.md)
    explainer.grid        the beat grid; explainer.captions: captions.yaml, layouts, .ass/.srt
    explainer.music       music composed from the event logs, synthesized in NumPy/SciPy
    explainer.finishing   the stitch stages after the picture: finishing pass, captions, music mix
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
