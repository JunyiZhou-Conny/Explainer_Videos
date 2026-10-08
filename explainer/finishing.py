"""After the picture: the finishing pass, captions in the picture, and the music mix.

Called by explainer.build. For a short (video.yaml `format: short`) the stitch is:

    scenes (normalized) --concat--> joined picture
        --finish (optional: bloom on bright strokes, film grain, vignette)--> build/.../<id>.finished.mp4
        --captions burned into the picture (one master per caption layout)
        --music (explainer.music: composed from the event logs, -14 LUFS, peaks <= -1 dBTP)-->
    output/<id>.mp4                 the short (first layout), with music
    output/<id>.<layout>.mp4        each further layout (e.g. en-first)
    output/<id>.nomusic.mp4         the same picture with a silent track (music-free master)
    output/<id>.music.wav           the music alone
    output/<id>.zh.srt / .en.srt / .zh-en.srt / .<layout>.ass, chapters.txt, transcript.md

For a narrated (long) video, `--music` (or a `music:` block in video.yaml) adds the score under the
narration after the normal stitch: <id>.mp4 gets the mix, <id>.nomusic.mp4 keeps the narration only.

video.yaml:

    finish: {bloom: true, grain: true, vignette: true}      # or numbers (strengths), or dicts:
    finish: {bloom: {strength: 0.55, threshold: 0.6, radius: 6, wide: 28}, grain: 5, vignette: 0.63}
"""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from pathlib import Path

from . import captions as cap
from .grid import Grid

BLOOM = {"strength": 0.55, "threshold": 0.6, "radius": 6.0, "wide": 28.0}
GRAIN = 5.0                 # ffmpeg noise strength on luma (0-100)
VIGNETTE = math.pi / 5      # ffmpeg vignette angle


def _number(v) -> float:
    """3, "0.6", "PI/5", "pi / 4" -> float."""
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().upper().replace(" ", "").replace("PI", repr(math.pi))
    if "/" in s:
        a, b = s.split("/", 1)
        return float(a) / float(b)
    return float(s)


def finish_config(spec: dict, enabled: bool = True) -> dict | None:
    """video.yaml `finish:` (or `look: {post: ...}`) -> {bloom: {...}, grain: strength, vignette: angle}."""
    f = spec.get("finish")
    if f is None:
        f = (spec.get("look") or {}).get("post")
    if not enabled or not f:
        return None
    if f is True:
        f = {"bloom": True, "grain": True, "vignette": True}
    out = {}
    b = f.get("bloom")
    if b:
        if isinstance(b, (list, tuple)):                 # [radius, wide]: the two blur sigmas
            b = {"radius": float(b[0]), "wide": float(b[-1])}
        out["bloom"] = {**BLOOM, **(b if isinstance(b, dict) else {} if b is True else {"strength": _number(b)})}
    g = f.get("grain")
    if g:
        out["grain"] = GRAIN if g is True else _number(g if not isinstance(g, dict) else g.get("strength", GRAIN))
    v = f.get("vignette")
    if v:
        out["vignette"] = VIGNETTE if v is True else _number(v if not isinstance(v, dict) else v.get("angle", VIGNETTE))
    return out or None


def finish_graph(cfg: dict, height: int = 1080, src: str = "0:v", out: str = "vout") -> str:
    """An ffmpeg filter graph: bloom (the bright parts, thresholded and blurred at two radii at half
    resolution, screened back onto the picture in colour), then vignette, then temporal film grain on
    luma. `radius` / `wide` are blur sigmas in pixels at 1080p."""
    k = height / 1080.0
    chain, last = [], src
    b = cfg.get("bloom")
    if b:
        thr = min(0.95, max(0.05, float(b["threshold"])))
        s1, s2 = max(0.5, float(b["radius"]) * k / 2), max(1.0, float(b["wide"]) * k / 2)
        chain.append(f"[{last}]format=gbrp,split=2[fb][fs]")
        chain.append(f"[fs]scale=iw/2:ih/2,curves=all='0/0 {thr:.3f}/0 1/1',split=2[fa][fw]")
        chain.append(f"[fa]gblur=sigma={s1:.2f}[ga]")
        chain.append(f"[fw]gblur=sigma={s2:.2f}[gw]")
        chain.append("[ga][gw]blend=all_mode=screen,scale=iw*2:ih*2[gl]")
        chain.append("[gl][fb]scale2ref[gls][fbs]")
        chain.append(f"[fbs][gls]blend=all_mode=screen:all_opacity={float(b['strength']):.3f},format=yuv420p[fbl]")
        last = "fbl"
    tail = []
    if cfg.get("vignette"):
        tail.append(f"vignette=angle={float(cfg['vignette']):.4f}")
    if cfg.get("grain"):
        tail.append(f"noise=c0s={float(cfg['grain']):.1f}:c0f=t+u")
    tail.append("format=yuv420p")
    chain.append(f"[{last}]" + ",".join(tail) + f"[{out}]")
    return ";".join(chain)


def _video_size(path: Path) -> tuple[int, int]:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                        "-of", "csv=p=0:s=x", str(path)], capture_output=True, text=True, check=True)
    w, h = (int(x) for x in r.stdout.strip().split("x"))
    return w, h


def apply_finish(src: Path, dst: Path, cfg: dict, crf: int = 12) -> Path:
    """Run the finishing pass once (cached: skipped when dst is newer than src with the same settings)."""
    stamp = dst.with_suffix(".finish.json")
    key = hashlib.sha1(json.dumps(cfg, sort_keys=True).encode()).hexdigest()
    if dst.exists() and stamp.exists() and stamp.read_text() == key and dst.stat().st_mtime >= src.stat().st_mtime:
        return dst
    _, h = _video_size(src)
    graph = finish_graph(cfg, h, "0:v", "vout")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-filter_complex", graph, "-map", "[vout]",
                    "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf), "-pix_fmt", "yuv420p",
                    str(dst)], check=True)
    stamp.write_text(key)
    return dst


# ---------------------------------------------------------------- captions of a stitched video

def gather_captions(project: Path, spec: dict, scenes: list[tuple[dict, Path, float]]) -> cap.Track:
    """All captions in video time. `scenes`: (scene entry, movie path, offset). Text (and the grid
    positions of `at` captions) come from the current captions.yaml; the moments that scene code chose
    come from each scene's events.json."""
    table = cap.load(cap.project_file(project, spec))
    track = cap.Track()
    for s, movie, offset in scenes:
        stem = Path(s["file"]).stem
        ev_path = movie.with_suffix(".events.json")
        log = json.loads(ev_path.read_text()) if ev_path.exists() else {}
        g = log.get("grid") or {}
        grid = Grid(float(g.get("bpm") or spec.get("tempo") or 100), int(g.get("beats_per_bar", 4)))
        yaml_caps = cap.for_scene(table, stem, s["cls"])
        by_id = {c.id: c for c in yaml_caps if c.id}
        placed = set()
        for c in yaml_caps:
            if c.at is not None:
                c.t = offset + grid.time(c.at)
                c.dur = cap.duration(c, grid)
                c.placed = "yaml"
                track.cues.append(c)
                placed.add(id(c))
        for d in log.get("captions") or []:
            if d.get("placed") != "code":
                continue
            c = cap.Caption.from_dict(d, stem)
            src = by_id.get(c.id) if c.id else None
            if src is not None:
                c.zh, c.en = src.zh, src.en
                placed.add(id(src))
            c.t = offset + float(d.get("t", 0.0))
            if src is not None and src.fixed:
                c.dur = cap.duration(src, grid)
            elif d.get("fixed"):
                c.dur = float(d["dur"])
            else:
                c.dur = cap.reading_time(c.zh, c.en)
            track.cues.append(c)
        if log:
            for c in yaml_caps:
                if id(c) not in placed and c.at is None and not any(
                        d.get("id") == c.id and c.id for d in log.get("captions") or []):
                    track.warnings.append(f"{stem}: caption never shown: {c.id or c.zh[:20]!r}")
    track.cues, warn = cap.tidy(track.cues)
    track.warnings += warn
    return track


# ---------------------------------------------------------------- muxing

def mux(picture: Path, audio: Path | None, dst: Path, ass: Path | None = None, crf: int = 18,
        tune: str | None = None) -> None:
    """picture (+ captions burned in) + audio -> dst. Without captions the video stream is copied."""
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(picture)]
    if audio is not None:
        cmd += ["-i", str(audio)]
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    if ass is not None:
        cmd += ["-vf", f"ass='{str(ass).replace(chr(39), '')}'", "-c:v", "libx264", "-preset", "medium",
                "-crf", str(crf), "-pix_fmt", "yuv420p"] + (["-tune", tune] if tune else [])
    else:
        cmd += ["-c:v", "copy"]
    cmd += ["-map", "0:v:0", "-map", "1:a:0", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2"]
    if audio is None:
        cmd += ["-shortest"]                  # (an endless silent source; a real track keeps every frame)
    cmd += ["-movflags", "+faststart", str(dst)]
    subprocess.run(cmd, check=True)


def silent_copy(src: Path, dst: Path) -> None:
    """The same picture with a silent stereo track (the music-free master)."""
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "128k", "-shortest",
                    "-movflags", "+faststart", str(dst)], check=True)


def extract_audio(src: Path, dst: Path) -> Path:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vn", "-ac", "2", "-ar", "48000",
                    "-c:a", "pcm_f32le", str(dst)], check=True)
    return dst


def frame_count(path: Path) -> tuple[int, float]:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_packets", "-show_entries",
                        "stream=nb_read_packets,r_frame_rate", "-of", "json", str(path)],
                       capture_output=True, text=True, check=True)
    st = json.loads(r.stdout)["streams"][0]
    a, b = st["r_frame_rate"].split("/")
    return int(st["nb_read_packets"]), float(a) / float(b)


# ---------------------------------------------------------------- music

def compose_music(project: Path, spec: dict, scenes: list[tuple[str, float, Path]], total: float, out_dir: Path,
                  voice_wav: Path | None = None) -> dict:
    """Compose and render the score for a stitched video; with `voice_wav`, mix it under the narration.
    Returns {"music": wav (the music as it sounds in the mix), "mix": wav or None, "report": {...}}."""
    import numpy as np
    import soundfile as sf

    from . import music as mu
    settings = mu.Settings.from_spec(spec)
    logs = mu.load_timeline(scenes)
    score, cues, ctx, bed, acc = mu.compose(logs, settings, total)
    report = {"sync_30ms": round(mu.sync_share(cues, score), 3), "notes": len(score.notes), "fx": len(score.fx),
              "chords": len(score.chords), "duration": round(total, 3)}
    mix_path = None
    if voice_wav is not None:
        voice, sr = sf.read(str(voice_wav), always_2d=True)
        if sr != mu.SR:
            from scipy import signal
            voice = signal.resample_poly(voice, mu.SR, sr, axis=0)
        mixed, music, rep = mu.mix_under_voice(bed, acc, voice.astype(float), settings)
        report.update(rep)
        mix_path = out_dir / "mix.wav"
        out_dir.mkdir(parents=True, exist_ok=True)
        sf.write(mix_path, mixed.astype(np.float32), mu.SR)
    else:
        music, rep = mu.music_only(bed, acc, settings)
        report.update(rep)
    paths = mu.write_outputs(out_dir, score, cues, ctx, bed, acc, music, report)
    return {"music": paths["music"], "mix": mix_path, "report": report}


def short_qa(track: cap.Track, offsets: list[float], total: float, grid: Grid | None) -> dict:
    """Numbers the style plan asks of a short: picture-only share, cuts on the bar grid."""
    out = {"picture_only": round(track.picture_only_share(total), 3), "captions": len(track.cues)}
    if grid is not None:
        off = [o for o in offsets[1:]]
        out["cuts_on_bars"] = f"{sum(grid.on_grid(o, 'bar') for o in off)}/{len(off)}"
    return out
