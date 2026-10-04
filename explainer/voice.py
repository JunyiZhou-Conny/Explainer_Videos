"""Text-to-speech backends with an on-disk cache.

Pick a backend with environment variables (or the `voice:` block of a video.yaml):

    EXPLAINER_TTS     kokoro (default, local + free) | elevenlabs | edge | espeak | silent
    EXPLAINER_VOICE   backend-specific voice name, e.g. af_heart (kokoro),
                      an ElevenLabs voice id, en-US-AndrewNeural (edge)
    EXPLAINER_SPEED   speaking-rate multiplier (kokoro / edge), default 1.0

    ELEVENLABS_API_KEY        required for elevenlabs
    ELEVENLABS_MODEL          default eleven_multilingual_v2
    KOKORO_MODEL_DIR          folder holding kokoro-v1.0.onnx and voices-v1.0.bin
                              (default: ~/.cache/explainer/kokoro, then /opt/tts-models)

Every synthesized clip is cached under .cache/tts/ keyed by (backend, params, text),
so re-rendering a scene never re-synthesizes unchanged narration.

`speak()` returns a Clip with sentence-level timing marks. Kokoro clips are synthesized
sentence by sentence, so the marks are exact; other backends interpolate by text length.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import wave
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np

from . import REPO_ROOT

CACHE_DIR = Path(os.environ.get("EXPLAINER_CACHE", REPO_ROOT / ".cache" / "tts"))
SAMPLE_RATE = 24000
SENTENCE_GAP = 0.32  # seconds of silence between sentences inside one clip


@dataclass
class Clip:
    path: Path
    duration: float
    text: str
    # (character offset into text, seconds from clip start) for each sentence start
    marks: list[tuple[int, float]] = field(default_factory=list)

    def time_of(self, phrase: str) -> float | None:
        """Estimated time (s from clip start) at which `phrase` begins to be spoken.

        Returns None if the phrase is not in the narration (e.g. after a script edit)."""
        idx = self.text.find(phrase)
        if idx < 0:
            idx = self.text.lower().find(phrase.lower())
        if idx < 0:
            return None
        marks = self.marks or [(0, 0.0)]
        # interpolate inside the sentence that contains idx
        bounds = marks + [(len(self.text), self.duration)]
        for (c0, t0), (c1, t1) in zip(bounds, bounds[1:]):
            if c0 <= idx < c1 or c1 == len(self.text):
                if c1 == c0:
                    return t0
                return t0 + (t1 - t0) * (idx - c0) / (c1 - c0)
        return 0.0


# ---------------------------------------------------------------- helpers

_SENT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(“])")


def split_sentences(text: str) -> list[tuple[int, str]]:
    """Split narration into (offset, sentence) pairs."""
    out, pos = [], 0
    for m in _SENT_RE.finditer(text):
        out.append((pos, text[pos:m.start()]))
        pos = m.end()
    out.append((pos, text[pos:]))
    return [(o, s) for o, s in out if s.strip()]


def audio_duration(path: Path) -> float:
    if path.suffix == ".wav":
        with wave.open(str(path)) as w:
            return w.getnframes() / w.getframerate()
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(out.stdout.strip())


def write_wav(path: Path, samples: np.ndarray, sr: int = SAMPLE_RATE) -> None:
    peak = float(np.abs(samples).max()) if len(samples) else 0.0
    if peak > 0.99:  # scale instead of clipping
        samples = samples * (0.99 / peak)
    pcm = (np.clip(samples, -1.0, 1.0) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


@lru_cache(maxsize=1)
def load_lexicon() -> dict[str, dict]:
    import yaml

    path = Path(__file__).with_name("lexicon.yaml")
    return yaml.safe_load(path.read_text()) or {}


def _lexicon_regex(lex: dict) -> re.Pattern | None:
    if not lex:
        return None
    words = sorted(lex, key=len, reverse=True)
    return re.compile(r"(?<![\w-])(" + "|".join(re.escape(w) for w in words) + r")(?![\w-])")


def respell(text: str) -> str:
    """Apply the `say:` respellings from the lexicon (for text-input backends)."""
    lex = load_lexicon()
    rx = _lexicon_regex({k: v for k, v in lex.items() if v.get("say")})
    return rx.sub(lambda m: lex[m.group(1)]["say"], text) if rx else text


# ---------------------------------------------------------------- backends

class Backend:
    name = "base"
    ext = "wav"

    def params(self) -> dict:
        return {}

    def _cache_path(self, text: str, ext: str | None = None) -> Path:
        key = json.dumps({"b": self.name, "p": self.params(), "t": text}, sort_keys=True)
        digest = hashlib.sha1(key.encode()).hexdigest()[:20]
        return CACHE_DIR / self.name / f"{digest}.{ext or self.ext}"

    def synthesize(self, text: str, out: Path) -> None:  # pragma: no cover - interface
        raise NotImplementedError

    def speak(self, text: str) -> Clip:
        out = self._cache_path(text)
        if not out.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
            tmp = out.with_name(out.stem + f".tmp{os.getpid()}" + out.suffix)
            self.synthesize(text, tmp)
            tmp.replace(out)
        dur = audio_duration(out)
        # proportional sentence marks (no real timings from text-in/audio-out APIs)
        marks = [(off, dur * off / max(1, len(text))) for off, _ in split_sentences(text)]
        return Clip(out, dur, text, marks)


class SilentBackend(Backend):
    """Silence of a plausible length (~2.6 words/s). Fast layout previews, no TTS needed."""

    name = "silent"

    def __init__(self, wps: float = 2.6):
        self.wps = wps

    def params(self):
        return {"wps": self.wps}

    def synthesize(self, text, out):
        words = max(1, len(text.split()))
        write_wav(out, np.zeros(int(SAMPLE_RATE * (words / self.wps + 0.2)), dtype=np.float32))


class KokoroBackend(Backend):
    """Kokoro-82M via kokoro-onnx: a free, local, surprisingly natural neural voice."""

    name = "kokoro"

    def __init__(self, voice: str = "af_heart", speed: float = 1.0, lang: str = "en-us"):
        self.voice, self.speed, self.lang = voice, speed, lang
        self._engine = None

    def params(self):
        return {"voice": self.voice, "speed": self.speed, "lang": self.lang, "v": 2}

    @staticmethod
    def model_dir() -> Path:
        candidates = [os.environ.get("KOKORO_MODEL_DIR"),
                      Path.home() / ".cache" / "explainer" / "kokoro", "/opt/tts-models"]
        for c in candidates:
            if c and (Path(c) / "kokoro-v1.0.onnx").exists():
                return Path(c)
        raise FileNotFoundError(
            "Kokoro model files not found. Run `bash setup/install.sh` or set KOKORO_MODEL_DIR "
            "to a folder containing kokoro-v1.0.onnx and voices-v1.0.bin.")

    @property
    def engine(self):
        if self._engine is None:
            import onnxruntime as ort
            from kokoro_onnx import Kokoro

            d = self.model_dir()
            opts = ort.SessionOptions()
            opts.intra_op_num_threads = int(os.environ.get("EXPLAINER_TTS_THREADS", "2"))
            sess = ort.InferenceSession(str(d / "kokoro-v1.0.onnx"), sess_options=opts,
                                        providers=["CPUExecutionProvider"])
            self._engine = Kokoro.from_session(sess, str(d / "voices-v1.0.bin"))
        return self._engine

    def phonemize(self, text: str) -> str:
        """Phonemize with lexicon overrides spliced in at the phoneme level."""
        lex = {k: v for k, v in load_lexicon().items() if v.get("ipa")}
        rx = _lexicon_regex(lex)
        tok = self.engine.tokenizer
        if rx is None:
            return tok.phonemize(text, self.lang)
        parts, last = [], 0
        for m in rx.finditer(text):
            seg = text[last:m.start()]
            if seg.strip():
                parts.append(tok.phonemize(seg, self.lang))
            parts.append(lex[m.group(1)]["ipa"])
            last = m.end()
        tail = text[last:]
        if tail.strip():
            parts.append(tok.phonemize(tail, self.lang))
        joined = " ".join(p.strip() for p in parts if p.strip())
        return re.sub(r"\s+([.,!?;:])", r"\1", joined)

    def _lexicon_key(self, sentence: str) -> str:
        """The lexicon entries a sentence uses, so editing the lexicon re-voices only those sentences."""
        lex = {k: v for k, v in load_lexicon().items() if v.get("ipa")}
        rx = _lexicon_regex(lex)
        used = sorted({m.group(1) for m in rx.finditer(sentence)}) if rx else []
        return json.dumps({w: lex[w]["ipa"] for w in used}, ensure_ascii=False) if used else ""

    def _sentence_wav(self, sentence: str) -> Path:
        lex_key = self._lexicon_key(sentence)
        out = self._cache_path(sentence + (f"|lex={lex_key}" if lex_key else ""))
        if not out.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
            samples, sr = self.engine.create(self.phonemize(sentence), voice=self.voice,
                                             speed=self.speed, lang=self.lang, is_phonemes=True)
            tmp = out.with_name(out.stem + f".tmp{os.getpid()}.wav")
            write_wav(tmp, samples, sr)
            tmp.replace(out)
        return out

    def speak(self, text: str) -> Clip:
        sentences = split_sentences(text)
        joined = self._cache_path("\x1e".join(s for _, s in sentences) + f"|gap={SENTENCE_GAP}")
        pieces = [self._sentence_wav(s) for _, s in sentences]
        marks, t = [], 0.0
        durations = [audio_duration(p) for p in pieces]
        for (off, _), d in zip(sentences, durations):
            marks.append((off, t))
            t += d + SENTENCE_GAP
        if not joined.exists():
            gap = np.zeros(int(SAMPLE_RATE * SENTENCE_GAP), dtype=np.float32)
            chunks = []
            for i, p in enumerate(pieces):
                with wave.open(str(p)) as w:
                    data = np.frombuffer(w.readframes(w.getnframes()), dtype="<i2").astype(np.float32) / 32767
                chunks.append(data)
                if i < len(pieces) - 1:
                    chunks.append(gap)
            tmp = joined.with_name(joined.stem + f".tmp{os.getpid()}.wav")
            write_wav(tmp, np.concatenate(chunks))
            tmp.replace(joined)
        return Clip(joined, audio_duration(joined), text, marks)


class ElevenLabsBackend(Backend):
    """ElevenLabs REST API (paid). Needs ELEVENLABS_API_KEY."""

    name = "elevenlabs"
    ext = "mp3"

    def __init__(self, voice: str | None = None, model: str | None = None):
        self.voice = voice or os.environ.get("ELEVENLABS_VOICE_ID", "JBFqnCBsd6RMkjVDRZzb")
        self.model = model or os.environ.get("ELEVENLABS_MODEL", "eleven_multilingual_v2")
        self.key = os.environ.get("ELEVENLABS_API_KEY")
        if not self.key:
            raise RuntimeError("EXPLAINER_TTS=elevenlabs but ELEVENLABS_API_KEY is not set")

    def params(self):
        return {"voice": self.voice, "model": self.model}

    def synthesize(self, text, out):
        import urllib.request

        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice}?output_format=mp3_44100_128",
            data=json.dumps({"text": text, "model_id": self.model,
                             "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}}).encode(),
            headers={"xi-api-key": self.key, "Content-Type": "application/json", "Accept": "audio/mpeg"},
        )
        with urllib.request.urlopen(req, timeout=300) as r:
            out.write_bytes(r.read())


class EdgeBackend(Backend):
    """Microsoft Edge online voices via the `edge-tts` package (free, needs internet)."""

    name = "edge"
    ext = "mp3"

    def __init__(self, voice: str = "en-US-AndrewNeural", speed: float = 1.0):
        self.voice, self.speed = voice, speed

    def params(self):
        return {"voice": self.voice, "speed": self.speed}

    def synthesize(self, text, out):
        import asyncio

        import edge_tts

        rate = f"{round((self.speed - 1) * 100):+d}%"
        asyncio.run(edge_tts.Communicate(respell(text), self.voice, rate=rate).save(str(out)))


class EspeakBackend(Backend):
    """espeak-ng: robotic but always available offline."""

    name = "espeak"

    def __init__(self, voice: str = "en-us", speed: float = 1.0):
        self.voice, self.speed = voice, speed

    def params(self):
        return {"voice": self.voice, "speed": self.speed}

    def synthesize(self, text, out):
        exe = shutil.which("espeak-ng") or shutil.which("espeak")
        if not exe:
            raise RuntimeError("espeak-ng is not installed")
        subprocess.run([exe, "-v", self.voice, "-s", str(int(165 * self.speed)), "-w", str(out),
                        respell(text)], check=True)


def get_backend() -> Backend:
    """Backend chosen by EXPLAINER_TTS (default: kokoro if its model is present, else silent)."""
    name = os.environ.get("EXPLAINER_TTS", "").strip().lower()
    voice = os.environ.get("EXPLAINER_VOICE") or None
    speed = float(os.environ.get("EXPLAINER_SPEED", "1.0"))
    if not name:
        try:
            KokoroBackend.model_dir()
            name = "kokoro"
        except FileNotFoundError:
            name = "silent"
    if name == "kokoro":
        return KokoroBackend(voice or "af_heart", speed)
    if name == "elevenlabs":
        return ElevenLabsBackend(voice)
    if name == "edge":
        return EdgeBackend(voice or "en-US-AndrewNeural", speed)
    if name == "espeak":
        return EspeakBackend(voice or "en-us", speed)
    if name == "silent":
        return SilentBackend()
    raise ValueError(f"unknown EXPLAINER_TTS backend {name!r}")


if __name__ == "__main__":  # quick manual test: python -m explainer.voice "Some text."
    import sys

    clip = get_backend().speak(" ".join(sys.argv[1:]) or "Calibrating noise to sensitivity.")
    print(clip.path, f"{clip.duration:.2f}s", clip.marks)
