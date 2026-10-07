"""VoiceScene: a Manim Scene whose animations are timed to the narration.

Usage inside a scene::

    class Hook(VoiceScene):
        def construct(self):
            with self.voiceover("Here is a database of hospital patients.") as vo:
                self.play(FadeIn(db), run_time=vo.duration)       # fill the whole sentence

            with self.voiceover("The hospital answers forty one. Then Alice is admitted.") as vo:
                self.play(Write(answer))
                vo.wait_until("Then Alice")                        # sync to a phrase
                self.play(FadeIn(alice), run_time=vo.remaining())  # fill what's left

When a `with` block ends, the scene waits for the clip to finish (plus a short pad), so
narration never gets cut off. If your animations run longer than the clip, the next clip
simply starts later. Every clip is written to `<scene>.subs.json` next to the rendered
movie; `explainer.build` stitches those into an .srt for the whole video.
"""

from __future__ import annotations

import json
from contextlib import contextmanager
from pathlib import Path

from manim import Scene, logger

from . import i18n
from . import style  # noqa: F401  (sets the background colour; installs translation hooks)
from .voice import AlignedClip, Clip, get_backend

MIN_WAIT = 1 / 60


class Tracker:
    def __init__(self, scene: "VoiceScene", clip: Clip, start: float):
        self.scene, self.clip, self.start = scene, clip, start

    @property
    def duration(self) -> float:
        return self.clip.duration

    @property
    def elapsed(self) -> float:
        return self.scene.renderer.time - self.start

    def remaining(self, minimum: float = 0.3) -> float:
        """Seconds of narration left in this clip (at least `minimum`, handy as a run_time)."""
        return max(minimum, self.clip.duration - self.elapsed)

    def time_until(self, phrase: str) -> float:
        t = self.clip.time_of(phrase)
        if t is None:  # anchor phrase no longer in the narration: don't wait, but say so
            logger.warning(f"voiceover anchor not found: {phrase!r} in {self.clip.text[:60]!r}...")
            return 0.0
        return max(0.0, t - self.elapsed)

    def wait_until(self, phrase: str) -> None:
        """Pause until (approximately) the moment `phrase` is spoken."""
        t = self.time_until(phrase)
        if t > MIN_WAIT:
            self.scene.wait(t)

    def until(self, phrase: str, minimum: float = 0.3) -> float:
        """Run-time that ends when `phrase` starts: self.play(anim, run_time=vo.until("..."))."""
        return max(minimum, self.time_until(phrase))


class VoiceScene(Scene):
    pad_after_clip = 0.25  # breathing room after each narration clip

    def setup(self):
        super().setup()
        self._subs: list[dict] = []
        self._voice = get_backend()

    @contextmanager
    def voiceover(self, text: str, pad: float | None = None):
        """Narrate `text` (an English SAY line of script.md). In another language version
        (EXPLAINER_LANG), the sentence-aligned translation is spoken instead, and anchors given as
        English phrases are mapped onto it (see explainer.i18n)."""
        text = " ".join(text.split())
        line = i18n.line_for(text) if i18n.active() else None
        if i18n.active() and line is None:
            logger.warning(f"no {i18n.lang()} translation for narration: {text[:70]!r}... (speaking English)")
        clip = self._voice.speak_aligned(line) if line else self._voice.speak(text)
        start = self.renderer.time
        self.add_sound(str(clip.path))
        tracker = Tracker(self, clip, start)
        yield tracker
        pad = self.pad_after_clip if pad is None else pad
        left = start + clip.duration + pad - self.renderer.time
        if left > MIN_WAIT:
            self.wait(left)
        sub = {"start": round(start, 3), "end": round(start + clip.duration, 3),
               "text": text, "marks": [[o, round(t, 3)] for o, t in clip.marks]}
        if isinstance(clip, AlignedClip):   # the translated sentences, with their exact spans
            sub.update({"lang": i18n.lang(), "tr": clip.sentences,
                        "tr_spans": [[round(a, 3), round(b, 3)] for a, b in clip.spans]})
            if any(clip.en_display):
                sub["en_display"] = clip.en_display
            if line.spoken != line.sentences:   # what the voice read (say:): times the subtitles
                sub["tr_say"] = line.spoken
        self._subs.append(sub)

    def tear_down(self):  # Manim >= 0.19 (older versions call tearDown)
        getattr(super(), "tear_down", lambda: None)()
        self._write_subs()

    def tearDown(self):
        getattr(super(), "tearDown", lambda: None)()
        self._write_subs()

    def _write_subs(self):
        try:
            movie = Path(self.renderer.file_writer.movie_file_path)
        except AttributeError:  # e.g. rendering a still image only
            return
        movie.parent.mkdir(parents=True, exist_ok=True)
        movie.with_suffix(".subs.json").write_text(json.dumps(self._subs, indent=1))
