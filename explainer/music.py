"""A quiet background-music bed, synthesized from scratch (no samples, so no licensing questions).

Calm ambient piano-and-pad music in the spirit of maths explainers: slow seventh chords on soft pads,
a low bass, and a sparse bell-like arpeggio, all through a long reverb. Deterministic for a given
seed, so a rebuild reproduces the same track.

    python -m explainer.music out.wav --seconds 90 --seed 3      # listen to a sample

video.yaml (see explainer/build.py):

    music: {seed: 2, volume_db: 0}           # generated bed; volume_db shifts it up or down
    music: {file: assets/music/track.mp3}    # or any track of your own (looped to length)

The build mixes it under the narration and ducks it while someone speaks.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import wave
from pathlib import Path

import numpy as np

SR = 48000
TARGET_RMS_DB = -24.0        # the bed's level before the build's volume_db and ducking

# Chord progressions as (bass MIDI note, pad MIDI notes). Slow, warm, unresolved: nothing pulls focus.
PROGRESSIONS = [
    [(36, [60, 64, 67, 71]), (33, [57, 60, 64, 67, 71]), (29, [57, 60, 64, 65]), (31, [55, 59, 62, 64])],
    [(29, [57, 60, 64, 65]), (31, [55, 59, 62, 64]), (33, [57, 60, 64, 67]), (36, [55, 60, 64, 71])],
    [(33, [57, 60, 64, 67, 71]), (29, [57, 60, 65, 69]), (36, [55, 60, 64, 67]), (31, [55, 59, 62, 67])],
]


def hz(midi: float) -> float:
    return 440.0 * 2 ** ((midi - 69) / 12)


def _env(n: int, attack: float, release: float) -> np.ndarray:
    """Raised-cosine attack and release over n samples."""
    e = np.ones(n)
    a, r = min(n // 2, int(attack * SR)), min(n // 2, int(release * SR))
    if a:
        e[:a] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, a))
    if r:
        e[-r:] *= 0.5 + 0.5 * np.cos(np.linspace(0, np.pi, r))
    return e


def _pad_note(f: float, n: int, rng: np.random.Generator) -> np.ndarray:
    """A soft pad voice: few harmonics, two slightly detuned copies (one per ear), slow breathing."""
    t = np.arange(n) / SR
    out = np.zeros((n, 2))
    for ch, detune in enumerate((0.9985, 1.0015)):
        ph = rng.uniform(0, 2 * np.pi, 4)
        sig = sum(a * np.sin(2 * np.pi * k * f * detune * t + ph[k - 1])
                  for k, a in zip(range(1, 5), (1.0, 0.32, 0.12, 0.05)))
        out[:, ch] = sig
    breath = 1 + 0.12 * np.sin(2 * np.pi * rng.uniform(0.05, 0.11) * t + rng.uniform(0, 6.28))
    return out * breath[:, None]


def _bell(f: float, rng: np.random.Generator, dur: float = 4.0) -> np.ndarray:
    """A soft, piano-ish struck note: decaying partials, the upper ones dying faster."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for k, (a, tau) in enumerate(((1.0, 1.6), (0.28, 0.8), (0.10, 0.45), (0.04, 0.25)), start=1):
        sig += a * np.sin(2 * np.pi * f * k * 1.0007 ** (k - 1) * t) * np.exp(-t / tau)
    sig *= np.minimum(1, t / 0.006)                       # 6 ms attack, no click
    pan = rng.uniform(0.3, 0.7)
    return np.stack([sig * np.sqrt(1 - pan), sig * np.sqrt(pan)], axis=1)


def _reverb_ir(seconds: float, rng: np.random.Generator) -> np.ndarray:
    n = int(seconds * SR)
    t = np.arange(n) / SR
    decay = np.exp(-6.9 * t / seconds)                    # -60 dB at `seconds`
    ir = rng.standard_normal((n, 2)) * decay[:, None]
    from scipy.signal import butter, sosfilt
    ir = sosfilt(butter(2, 3500, "low", fs=SR, output="sos"), ir, axis=0)   # darker tail
    ir[: int(0.02 * SR)] = 0                              # 20 ms pre-delay
    return ir / np.sqrt((ir ** 2).sum(axis=0))


def generate(seconds: float, seed: int = 0, bpm: float = 64.0) -> np.ndarray:
    """Stereo float32 music, `seconds` long, peak about -3 dBFS before the level target."""
    from scipy.signal import butter, oaconvolve, sosfilt

    rng = np.random.default_rng(seed)
    prog = PROGRESSIONS[seed % len(PROGRESSIONS)]
    beat = 60.0 / bpm
    chord_len = 8 * beat                                  # two bars of 4/4 per chord
    total = int((seconds + 6) * SR)                       # tail for the reverb, trimmed below
    mix = np.zeros((total, 2))

    i, start = 0, 0.0
    while start < seconds + chord_len:
        bass, notes = prog[i % len(prog)]
        a = int(start * SR)
        n = int((chord_len + 2.5) * SR)                   # overlap: the next chord fades in over this
        if a >= total:
            break
        n = min(n, total - a)
        env = _env(n, attack=1.8, release=2.6)[:, None]
        for m in notes:
            mix[a:a + n] += 0.055 * _pad_note(hz(m), n, rng) * env
        tb = np.arange(n) / SR
        mix[a:a + n] += (0.10 * np.sin(2 * np.pi * hz(bass + 12) * tb) * _env(n, 0.8, 2.0))[:, None]
        # a sparse arpeggio an octave up: on eighth notes, some of the time
        for e in range(16):
            if rng.random() < (0.55 if e % 4 == 0 else 0.22):
                at = a + int(e * beat / 2 * SR)
                note = _bell(hz(rng.choice(notes) + 12), rng)
                end = min(total, at + len(note))
                if at < total:
                    mix[at:end] += 0.07 * note[: end - at]
        start += chord_len
        i += 1

    mix = sosfilt(butter(2, 40, "high", fs=SR, output="sos"), mix, axis=0)
    mix = sosfilt(butter(2, 7000, "low", fs=SR, output="sos"), mix, axis=0)
    wet = np.stack([oaconvolve(mix[:, c], _reverb_ir(3.2, rng)[:, c])[:total] for c in range(2)], axis=1)
    out = 0.62 * mix + 0.55 * wet
    out = out[: int(seconds * SR)]
    rms = np.sqrt(np.mean(out ** 2)) or 1.0
    out *= 10 ** (TARGET_RMS_DB / 20) / rms
    out = np.tanh(out * 1.5) / 1.5                        # gentle safety limiter
    fade = min(len(out) // 4, int(4 * SR))
    out[:fade] *= np.linspace(0, 1, fade)[:, None]
    out[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return out.astype(np.float32)


def write_wav(path: Path, data: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pcm = (np.clip(data, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def bed(seconds: float, cache_dir: Path, seed: int = 0, bpm: float = 64.0) -> Path:
    """The generated bed for a video of this length, cached by its parameters."""
    key = hashlib.sha1(json.dumps([round(seconds, 1), seed, bpm, TARGET_RMS_DB, "v1"]).encode()).hexdigest()[:12]
    out = cache_dir / f"music_{key}.wav"
    if not out.exists():
        tmp = out.with_suffix(".tmp.wav")
        write_wav(tmp, generate(seconds, seed, bpm))
        tmp.replace(out)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", type=Path)
    ap.add_argument("--seconds", type=float, default=60)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--bpm", type=float, default=64.0)
    a = ap.parse_args(argv)
    write_wav(a.out, generate(a.seconds, a.seed, a.bpm))
    print(a.out)


if __name__ == "__main__":
    main()
