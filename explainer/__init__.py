"""explainer — a small toolkit for 3Blue1Brown-style paper explainer videos.

Pieces:
    explainer.voice       text-to-speech backends (Kokoro local, ElevenLabs, edge-tts, espeak, silent)
    explainer.scene       VoiceScene: a Manim Scene whose animations are timed to narration
    explainer.style       the shared colour palette and typography
    explainer.components  reusable visuals (database tables, paper cards, lineage maps, ...)
    explainer.build       render a whole video project -> mp4 + subtitles + chapters
    explainer.preview     quick low-res render + contact sheet for checking a scene's layout
"""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
