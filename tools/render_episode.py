#!/usr/bin/env python3
"""Render an authored episode from script.json + saved production defaults.

Examples:
  .venv/bin/python tools/render_episode.py videos/skills-ecosystem --sample s01
  .venv/bin/python tools/render_episode.py videos/skills-ecosystem

The reusable engine handles speech, exact frame budgets, captions, chapters and validation.
Each topic still requires its own teaching diagrams in scenes.py.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("EXPLAINER_ROOT", str(ROOT))
os.environ.setdefault("KOKORO_MODEL_DIR", str(ROOT / "assets/tts-models/kokoro"))
os.environ.setdefault("EXPLAINER_FONTS_DIR", str(ROOT / "assets/fonts"))
os.environ.setdefault("EXPLAINER_TTS_THREADS", "2")
os.environ["EXPLAINER_TTS"] = "kokoro"
sys.path.insert(0, str(ROOT))

def run(args, **kwargs):
    return subprocess.run([str(a) for a in args], check=True, **kwargs)

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def probe(path):
    return json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
        "stream=codec_name,codec_type,width,height,r_frame_rate:format=duration", "-of", "json", str(path)], text=True))

def ass_time(t):
    cs = round(t * 100)
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"

def captions(pairs, stem):
    from explainer import subtitles
    tracks = subtitles.tracks(pairs, timing="en", bi_zh_limit=34, bi_en_limit=51, min_show=1.8)
    subtitles.write_srt(stem.with_suffix(".en.srt"), tracks["en"])
    subtitles.write_srt(stem.with_suffix(".zh.srt"), tracks["zh"])
    subtitles.write_srt(stem.with_suffix(".zh-en.srt"), tracks["zh-en"])
    header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Bilingual,Noto Sans CJK SC,43,&H00F3F0E7,&H00F3F0E7,&H00171717,&H00171717,0,0,0,0,100,100,0,0,1,0,0,2,90,90,27,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    def esc(s):
        return s.replace("\\", "\\\\").replace("{", "(").replace("}", ")").replace("\n", "\\N")
    for a, b, zh, en in tracks["zh-en"]:
        body = esc(zh) + r"\N{\fnInter\fs30\c&H00C9C9C9&}" + esc(en)
        events.append(f"Dialogue: 0,{ass_time(a)},{ass_time(b)},Bilingual,,0,0,0,,{body}")
    stem.with_suffix(".zh-en.ass").write_text(header + "\n".join(events) + "\n")
    return tracks

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project", type=Path)
    ap.add_argument("--defaults", type=Path, default=ROOT / "skill-library/conny-explainer-video/defaults.json")
    ap.add_argument("--sample", help="Render one scene, e.g. s01")
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--voice")
    ap.add_argument("--speed", type=float)
    ap.add_argument("--jobs", type=int, default=2)
    args = ap.parse_args()
    project = args.project.resolve()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', project.name):
        raise SystemExit('Use a lowercase hyphenated episode directory name.')
    script_path = project / "script.json"
    script = json.loads(script_path.read_text())
    defaults = json.loads(args.defaults.read_text())
    specification = project / "episode.json"
    if specification.exists():
        episode = json.loads(specification.read_text())
        for key in ("preset", "duration_seconds", "video", "narration", "subtitles"):
            if key in episode:
                defaults[key] = ({**defaults[key], **episode[key]}
                    if isinstance(episode[key], dict) else episode[key])
    if defaults["narration"]["language"] != "en" or script.get("narration_language", "en") != "en":
        raise SystemExit("The configured local engine currently supports English narration. Configure and verify another voice backend for this episode.")
    args.voice = args.voice or defaults["narration"].get("voice") or "af_heart"
    args.speed = args.speed or defaults["narration"].get("speed", 0.95)
    if args.speed <= 0 or args.jobs < 1:
        raise SystemExit("Speech speed and job count must be positive.")
    if script.get("preset", defaults["preset"]) != defaults["preset"]:
        raise SystemExit("Script preset and episode brief differ. Resolve the intended design before rendering.")
    fps = defaults["video"]["fps"]
    if (defaults["video"]["width"], defaults["video"]["height"], fps) != (1920, 1080, 30):
        raise SystemExit("This authored scene layout currently requires 1920×1080 @30fps.")
    if defaults['subtitles'].get('languages') != ['zh-CN', 'en'] or not defaults['subtitles'].get('burn_in'):
        raise SystemExit('This runner requires burned Chinese/English captions; implement another delivery route for other settings.')
    target = float(defaults["duration_seconds"] if specification.exists() else script.get("target_duration_seconds", defaults["duration_seconds"]))
    if not math.isfinite(target) or target <= 0:
        raise SystemExit('Duration must be finite and positive.')
    output = ROOT / "outputs" / project.name
    output.mkdir(parents=True, exist_ok=True)
    os.environ["EXPLAINER_VOICE"] = args.voice
    os.environ["EXPLAINER_SPEED"] = str(args.speed)
    os.environ["EXPLAINER_CACHE"] = str(output / ".tts-cache")
    from explainer.voice import KokoroBackend
    selected = [s for s in script["scenes"] if not args.sample or s["id"] == args.sample]
    if not selected:
        raise SystemExit("No matching scene; author script.json first")
    ids = [s["id"] for s in selected]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r"s\d{2,}", ident) for ident in ids):
        raise SystemExit("Scene IDs must be unique s01-style identifiers.")
    voice = KokoroBackend(args.voice, args.speed)
    prepared = []
    for scene in selected:
        audio = []
        for line in scene["lines"]:
            clip = voice.speak(line["en"])
            audio.append({"duration": clip.duration, "path": str(clip.path)})
        minimum = sum(a["duration"] for a in audio) + len(audio) * 0.18 + 1.10
        prepared.append({**scene, "audio": audio, "minimum": minimum})
        print(f"Speech {scene['id']}: {minimum:.2f}s minimum", flush=True)
    minimum = sum(s["minimum"] for s in prepared)
    if args.sample:
        target = round(minimum + 0.8, 1)
    elif minimum > target:
        raise SystemExit(f"Narration needs {minimum:.1f}s; target is {target:.1f}s. Tighten script or set a modestly faster --speed; audio will not be clipped.")
    slack = target - minimum
    frames_left = round(target * fps)
    for i, scene in enumerate(prepared):
        duration = scene["minimum"] + slack * scene["minimum"] / minimum
        frames = round(duration * fps) if i < len(prepared) - 1 else frames_left
        frames_left -= frames
        scene["frames"] = frames
        scene["duration"] = frames / fps
    plan = {"title": script["title_en"], "project": str(project), "script_sha256": digest(script_path),
        "defaults_sha256": digest(args.defaults), "episode_sha256": digest(specification) if specification.exists() else None,
        "resolved_settings": defaults, "voice": args.voice, "speed": args.speed,
        "fps": fps, "target_duration_seconds": target, "sample": args.sample, "scenes": prepared}
    plan_path = output / (f"plan-{args.sample}.json" if args.sample else "plan.json")
    plan_path.write_text(json.dumps(plan, ensure_ascii=False, indent=2))
    if args.prepare_only:
        print(plan_path)
        return
    env = dict(os.environ)
    env["EPISODE_PLAN"] = str(plan_path)
    env["PYTHONPATH"] = os.pathsep.join([str(ROOT), str(project)])
    env["EXPLAINER_PROJECT"] = str(project)
    env["PYTHONHASHSEED"] = "0"
    scenes_file = project / "scenes.py"
    def render(scene):
        ident = scene["id"]
        media = output / "build" / ident
        movie = media / "videos/scenes/1080p30" / f"{ident.upper()}.mp4"
        stamp = media / "render-input.json"
        sig = {"scenes": digest(scenes_file), "scene": scene, "voice": args.voice, "speed": args.speed,
               "fps": fps, "runner": digest(__file__),
               "toolkit": {name: digest(ROOT / 'explainer' / name) for name in
                           ('scene.py', 'voice.py', 'i18n.py', 'style.py', 'subtitles.py')}}
        if movie.exists() and stamp.exists() and json.loads(stamp.read_text()) == sig:
            print(f"Reusing {ident}", flush=True)
            return scene, movie
        media.mkdir(parents=True, exist_ok=True)
        log = media / "render.log"
        with log.open("w") as fh:
            result = subprocess.run([sys.executable, "-m", "manim", "render", "-qh", "--fps", str(fps),
                 "--disable_caching", "--media_dir", str(media), str(scenes_file), ident.upper()],
                 cwd=project, env=env, stdout=fh, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"{ident} render failed:\n" + "\n".join(log.read_text().splitlines()[-35:]))
        if not movie.exists():
            raise FileNotFoundError(movie)
        stamp.write_text(json.dumps(sig, ensure_ascii=False, indent=2))
        print(f"Rendered {ident}", flush=True)
        return scene, movie
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rendered = list(pool.map(render, prepared))
    # End-to-end captions use the measured timeline emitted by each actual scene.
    from explainer import subtitles
    from explainer.i18n import Line
    pairs, offset, chapters, normalized = [], 0.0, [], []
    for scene, movie in rendered:
        normalized_movie = movie.parent / f"{scene['id']}.normalized.mp4"
        run(["ffmpeg", "-y", "-v", "error", "-i", movie, "-c:v", "copy", "-af", "aresample=48000,apad",
             "-ac", "2", "-c:a", "aac", "-b:a", "160k", "-t", str(scene["duration"]), normalized_movie])
        normalized.append(normalized_movie)
        chapters.append({"start": offset, "id": scene["id"], "title": scene["title_en"]})
        actual = json.loads(movie.with_suffix(".subs.json").read_text())
        if len(actual) != len(scene["lines"]):
            raise RuntimeError(f"Narration cue mismatch for {scene['id']}")
        for cue, line in zip(actual, scene["lines"]):
            zh = [s for s in re.split(r"(?<=[。！？])\s*", line["zh"]) if s]
            translation = Line(line["en"], zh, zh)
            pairs += subtitles.sentence_pairs(cue, offset, translation)
        offset += scene["duration"]
    name = f"sample-{args.sample}" if args.sample else project.name
    stem = output / name
    tracks = captions(pairs, stem)
    listing = output / f"{name}.concat.txt"
    listing.write_text("".join("file '" + str(p).replace("'", "'\\''") + "'\n" for p in normalized))
    clean = output / f"{name}.clean.mp4"
    run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", listing,
         "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac",
         "-b:a", "160k", "-t", str(target), "-movflags", "+faststart", clean])
    ass = stem.with_suffix(".zh-en.ass")
    final = stem.with_suffix(".mp4")
    # Relative paths avoid FFmpeg filter escaping of arbitrary checkout/home names.
    filt = f"drawbox=x=0:y=910:w=1920:h=170:color=0x171717:t=fill,ass='{ass.relative_to(ROOT)}':fontsdir='assets/fonts'"
    run(["ffmpeg", "-y", "-v", "error", "-i", clean, "-vf", filt, "-c:v", "libx264", "-preset", "fast",
         "-tune", "animation", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "copy", "-t", str(target),
         "-movflags", "+faststart", final], cwd=ROOT)
    metadata = probe(final)
    duration = float(metadata["format"]["duration"])
    if abs(duration - target) > 0.1:
        raise RuntimeError(f"Final duration {duration} differs from target {target}")
    if not any(s["codec_type"] == "audio" for s in metadata["streams"]):
        raise RuntimeError("Final video is missing narration")
    audio_stats = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(final), "-vn", "-af", "volumedetect",
         "-f", "null", "-"], capture_output=True, text=True, check=True).stderr
    volume = re.search(r"mean_volume: (-?[\d.]+) dB", audio_stats)
    if not volume or float(volume.group(1)) < -45:
        raise RuntimeError("Narration energy is missing or implausibly quiet")
    validation = {"probe": metadata, "target_seconds": target, "audio_mean_db": float(volume.group(1)),
         "caption_cues": len(tracks["zh-en"]), "script_sha256": digest(script_path),
         "source_matches_plan": digest(script_path) == plan["script_sha256"], "chapters": chapters}
    if not validation["source_matches_plan"]:
        raise RuntimeError("Script changed during rendering. Rebuild before accepting output.")
    stem.with_suffix(".validation.json").write_text(json.dumps(validation, ensure_ascii=False, indent=2))
    stem.with_suffix(".chapters.txt").write_text("\n".join(f"{int(c['start'])//60:02d}:{int(c['start'])%60:02d} {c['title']}" for c in chapters) + "\n")
    print(f"READY {final} — {duration:.3f}s, narrated, {len(tracks['zh-en'])} bilingual cues", flush=True)

if __name__ == "__main__":
    main()
