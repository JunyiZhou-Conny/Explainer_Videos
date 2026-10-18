"""Render an authored episode (episode.json + script.json + scenes.py).

The engine behind tools/render_episode.py: speech, exact frame budgets, measured
captions, the composed score, burn-in and validation. It reuses the toolkit in this
package (voice backends, VoiceScene timing, subtitles, music/finishing) instead of
carrying private copies; each topic still authors its own teaching diagrams in
scenes.py.

The validated profile is 1920x1080 @30fps with burned Chinese-above-English captions.
Other resolutions/frame rates render with a warning and need their own sample review;
narration may be English (Kokoro, sentence-exact timing) or Chinese (edge-tts by
default, upgraded to Azure when AZURE_SPEECH_KEY/REGION are set — marks are then
character-proportional, so prefer sentence-start caption anchors).
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
import tempfile
from concurrent.futures import ThreadPoolExecutor

ROOT = Path(__file__).resolve().parents[1]

VALIDATED_PROFILE = (1920, 1080, 30)
CAPTION_BAND = 170 / 1080          # fraction of the frame height the presets reserve for captions
BAND_COLOUR = "0x171717"
# The episode caption face (today: the Swiss band). Style contracts move this into presets.
CAPTION_STYLE = {"font": "Noto Sans CJK SC", "zh_size": 43, "en_size": 30,
                 "zh_colour": "&H00F3F0E7", "en_colour": "&H00C9C9C9", "en_font": "Inter",
                 "outline_colour": "&H00171717", "back_colour": "&H00171717",
                 "border_style": 1, "outline": 0, "shadow": 0,
                 "margin_l": 90, "margin_r": 90, "margin_v": 27, "en_border": 0}
ZH_DEFAULT_VOICE = {"backend": "edge", "voice": "zh-CN-XiaoyiNeural", "speed": 1.0}


def digest(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def probe(path: Path) -> dict:
    return json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries",
         "stream=codec_name,codec_type,width,height,r_frame_rate:format=duration",
         "-of", "json", str(path)], text=True))


def resolve_settings(project: Path, defaults_path: Path) -> tuple[dict, dict]:
    """Merged settings for one episode: defaults.json <- episode.json. The duration is stated in
    ONE place: episode.json when it exists (script.json must then not disagree), else script.json,
    else the defaults."""
    script = json.loads((project / "script.json").read_text())
    defaults = json.loads(defaults_path.read_text())
    specification = project / "episode.json"
    if specification.exists():
        episode = json.loads(specification.read_text())
        for key in ("preset", "duration_seconds", "video", "narration", "subtitles", "music"):
            if key in episode:
                defaults[key] = ({**defaults.get(key, {}), **episode[key]}
                                 if isinstance(episode[key], dict) else episode[key])
        stated = script.get("target_duration_seconds")
        if stated is not None and float(stated) != float(defaults["duration_seconds"]):
            raise SystemExit("Duration is stated in both episode.json and script.json and they "
                             "disagree; keep it in episode.json only.")
        target = float(defaults["duration_seconds"])
    else:
        target = float(script.get("target_duration_seconds", defaults["duration_seconds"]))
    if not math.isfinite(target) or target <= 0:
        raise SystemExit("Duration must be finite and positive.")
    defaults["duration_seconds"] = target
    return defaults, script


def narration_key(settings: dict, script: dict) -> str:
    """'en' or 'zh': which text field of each line is spoken. Anything else is refused."""
    lang = str(script.get("narration_language") or settings["narration"].get("language", "en"))
    key = lang.split("-")[0].lower()
    if key not in ("en", "zh"):
        raise SystemExit(f"Narration language {lang!r} has no verified route here; the engine "
                         "speaks 'en' (Kokoro) or 'zh' (edge/Azure). Configure and sample-review "
                         "another backend before using it.")
    return key


def check_gates(settings: dict) -> tuple[int, int, int]:
    """The subtitle contract is fixed; the video profile is open but only one profile is validated."""
    if settings["subtitles"].get("languages") != ["zh-CN", "en"] or not settings["subtitles"].get("burn_in"):
        raise SystemExit("This runner delivers burned Chinese-above-English captions; implement "
                         "and review another delivery route before configuring one.")
    video = settings["video"]
    width, height, fps = int(video["width"]), int(video["height"]), int(video["fps"])
    if width <= 0 or height <= 0 or fps <= 0:
        raise SystemExit("Video width/height/fps must be positive.")
    if (width, height, fps) != VALIDATED_PROFILE:
        print(f"WARNING: {width}x{height}@{fps} is not the validated profile "
              f"{VALIDATED_PROFILE}; review a sample before trusting the layout.", flush=True)
    return width, height, fps


def frame_budget(prepared: list[dict], target: float, fps: int) -> None:
    """Distribute the slack between the narration minimum and the target proportionally; the last
    scene absorbs rounding so the frame counts sum exactly to round(target * fps)."""
    minimum = sum(s["minimum"] for s in prepared)
    slack = target - minimum
    frames_left = round(target * fps)
    for i, scene in enumerate(prepared):
        duration = scene["minimum"] + slack * scene["minimum"] / minimum
        frames = round(duration * fps) if i < len(prepared) - 1 else frames_left
        frames_left -= frames
        scene["frames"] = frames
        scene["duration"] = frames / fps


def zh_pairs(clip: dict, offset: float, line: dict) -> list[tuple]:
    """Caption pairs for a Chinese-narrated clip: timing from the zh audio (marks when the backend
    gives sentence marks, else proportional to characters), English text from the script line."""
    from .subtitles import SENTENCE_GAP
    from .voice import split_sentences

    zh_sents = [s for s in re.split(r"(?<=[。！？])\s*", line["zh"]) if s]
    en_sents = [s for _, s in split_sentences(line["en"])]
    base, end = offset + clip["start"], offset + clip["end"]
    marks = clip.get("marks") or []
    if len(marks) == len(zh_sents):
        starts = [base + t for _, t in marks]
    else:
        n = max(1, len(clip["text"]))
        total = clip["end"] - clip["start"]
        pos, starts = 0, []
        for s in zh_sents:
            starts.append(base + total * pos / n)
            pos += len(s)
    spans = [(a, (starts[i + 1] - SENTENCE_GAP) if i + 1 < len(starts) else end)
             for i, a in enumerate(starts)]
    if len(zh_sents) != len(en_sents):
        return [(spans[0][0], spans[-1][1], " ".join(zh_sents), " ".join(en_sents), None)]
    return [(a, b, zh, en, None) for (a, b), zh, en in zip(spans, zh_sents, en_sents)]


def build_pairs(actual: list[dict], lines: list[dict], offset: float, key: str) -> list[tuple]:
    """Caption pairs for one rendered scene from its measured .subs.json clips."""
    from .i18n import Line
    from . import subtitles

    if len(actual) != len(lines):
        raise RuntimeError("Narration cue mismatch: the scene spoke a different number of lines "
                           "than script.json holds")
    pairs = []
    for clip, line in zip(actual, lines):
        if key == "zh":
            pairs += zh_pairs(clip, offset, line)
        else:
            zh = [s for s in re.split(r"(?<=[。！？])\s*", line["zh"]) if s]
            pairs += subtitles.sentence_pairs(clip, offset, Line(line["en"], zh, zh))
    return pairs


def write_captions(pairs: list[tuple], stem: Path, width: int, height: int, timing: str) -> dict:
    from . import subtitles
    tracks = subtitles.tracks(pairs, timing=timing, bi_zh_limit=34, bi_en_limit=51, min_show=1.8)
    subtitles.write_srt(stem.with_suffix(".en.srt"), tracks["en"])
    subtitles.write_srt(stem.with_suffix(".zh.srt"), tracks["zh"])
    subtitles.write_srt(stem.with_suffix(".zh-en.srt"), tracks["zh-en"])
    subtitles.write_ass(stem.with_suffix(".zh-en.ass"), tracks["zh-en"], width=width, height=height,
                        band=CAPTION_BAND, style=CAPTION_STYLE)
    return tracks


def music_settings(settings: dict, no_music: bool) -> dict | None:
    """The resolved music block, or None when the episode leaves music out."""
    m = settings.get("music", {"enabled": True})
    if no_music or m is False or (isinstance(m, dict) and not m.get("enabled", True)):
        return None
    return dict(m) if isinstance(m, dict) else {}


def add_score(clean: Path, final: Path, rendered: list[tuple], music: dict, project: Path,
              build_dir: Path, target: float) -> dict:
    """Compose the score from the scenes' event logs, mix it under the narration (ducked), and
    write `final`. Returns the finishing report (LUFS of voice/music/mix)."""
    from . import finishing as fin

    scenes, offset = [], 0.0
    for scene, movie in rendered:
        events = movie.with_suffix(".events.json")
        if not events.exists():
            raise SystemExit(f"{events} is missing; re-render the scenes with the current toolkit "
                             "(explainer.events logs them), or set music.enabled false.")
        scenes.append((scene["id"], offset, events))
        offset += scene["duration"]
    work = build_dir / "music"
    work.mkdir(parents=True, exist_ok=True)
    voice_wav = work / "voice.wav"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(clean), "-vn",
                    "-ar", "48000", "-ac", "2", "-c:a", "pcm_f32le", str(voice_wav)], check=True)
    result = fin.compose_music(project, {"music": music}, scenes, target, work, voice_wav=voice_wav)
    fin.mux(clean, result["mix"], final)
    return result["report"]


def validate_output(final: Path, target: float, cues: int, script_path: Path, plan: dict,
                    chapters: list[dict], music_report: dict | None) -> dict:
    metadata = probe(final)
    duration = float(metadata["format"]["duration"])
    if abs(duration - target) > 0.1:
        raise RuntimeError(f"Final duration {duration} differs from target {target}")
    if not any(s["codec_type"] == "audio" for s in metadata["streams"]):
        raise RuntimeError("Final video is missing narration")
    audio_stats = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(final), "-vn", "-af",
                                  "volumedetect", "-f", "null", "-"],
                                 capture_output=True, text=True, check=True).stderr
    volume = re.search(r"mean_volume: (-?[\d.]+) dB", audio_stats)
    if not volume or float(volume.group(1)) < -45:
        raise RuntimeError("Narration energy is missing or implausibly quiet")
    validation = {"probe": metadata, "target_seconds": target,
                  "audio_mean_db": float(volume.group(1)), "caption_cues": cues,
                  "script_sha256": digest(script_path),
                  "source_matches_plan": digest(script_path) == plan["script_sha256"],
                  "chapters": chapters}
    if music_report is not None:
        validation["music"] = music_report
        mix = music_report.get("mix_lufs") or music_report.get("voice_lufs")
        if mix is not None and not (-30 <= float(mix) <= -8):
            raise RuntimeError(f"Mixed loudness {mix} LUFS is outside the plausible window")
    if not validation["source_matches_plan"]:
        raise RuntimeError("Script changed during rendering. Rebuild before accepting output.")
    return validation


def main(argv=None):
    os.environ.setdefault("KOKORO_MODEL_DIR", str(ROOT / "assets/tts-models/kokoro"))
    os.environ.setdefault("EXPLAINER_FONTS_DIR", str(ROOT / "assets/fonts"))
    os.environ.setdefault("EXPLAINER_TTS_THREADS", "2")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("project", type=Path)
    ap.add_argument("--defaults", type=Path,
                    default=ROOT / "skill-library/conny-explainer-video/defaults.json")
    ap.add_argument("--sample", help="Render one scene, e.g. s01")
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--voice")
    ap.add_argument("--speed", type=float)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--no-music", action="store_true", help="leave the score out of this build")
    args = ap.parse_args(argv)
    project = args.project.resolve()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", project.name):
        raise SystemExit("Use a lowercase hyphenated episode directory name.")
    script_path = project / "script.json"
    settings, script = resolve_settings(project, args.defaults)
    key = narration_key(settings, script)
    width, height, fps = check_gates(settings)
    target = settings["duration_seconds"]
    if script.get("preset", settings["preset"]) != settings["preset"]:
        raise SystemExit("Script preset and episode brief differ. Resolve the intended design "
                         "before rendering.")

    narration = settings["narration"]
    if key == "zh":
        backend = narration.get("backend", ZH_DEFAULT_VOICE["backend"])
        args.voice = args.voice or narration.get("voice") or ZH_DEFAULT_VOICE["voice"]
        args.speed = args.speed or narration.get("speed") or ZH_DEFAULT_VOICE["speed"]
    else:
        backend = narration.get("backend", "kokoro")
        args.voice = args.voice or narration.get("voice") or "af_heart"
        args.speed = args.speed or narration.get("speed", 0.95)
    if args.speed <= 0 or args.jobs < 1:
        raise SystemExit("Speech speed and job count must be positive.")

    output = ROOT / "outputs" / project.name
    output.mkdir(parents=True, exist_ok=True)
    os.environ["EXPLAINER_TTS"] = backend
    os.environ["EXPLAINER_VOICE"] = args.voice
    os.environ["EXPLAINER_SPEED"] = str(args.speed)
    os.environ["EXPLAINER_CACHE"] = str(output / ".tts-cache")
    from .voice import get_backend
    voice = get_backend()
    if backend != "kokoro":
        print(f"NOTE: backend {backend} gives character-proportional sentence marks; "
              "caption starts inside a clip are estimates.", flush=True)

    selected = [s for s in script["scenes"] if not args.sample or s["id"] == args.sample]
    if not selected:
        raise SystemExit("No matching scene; author script.json first")
    ids = [s["id"] for s in selected]
    if len(ids) != len(set(ids)) or any(not re.fullmatch(r"s\d{2,}", ident) for ident in ids):
        raise SystemExit("Scene IDs must be unique s01-style identifiers.")

    prepared = []
    for scene in selected:
        audio = []
        for line in scene["lines"]:
            clip = voice.speak(line[key])
            audio.append({"duration": clip.duration, "path": str(clip.path)})
        minimum = sum(a["duration"] for a in audio) + len(audio) * 0.18 + 1.10
        prepared.append({**scene, "audio": audio, "minimum": minimum})
        print(f"Speech {scene['id']}: {minimum:.2f}s minimum", flush=True)
    minimum = sum(s["minimum"] for s in prepared)
    if args.sample:
        target = round(minimum + 0.8, 1)
    elif minimum > target:
        raise SystemExit(f"Narration needs {minimum:.1f}s; target is {target:.1f}s. Tighten the "
                         "script or set a modestly faster --speed; audio will not be clipped.")
    frame_budget(prepared, target, fps)

    specification = project / "episode.json"
    plan = {"title": script["title_en"], "project": str(project),
            "script_sha256": digest(script_path), "defaults_sha256": digest(args.defaults),
            "episode_sha256": digest(specification) if specification.exists() else None,
            "resolved_settings": settings, "narration_key": key, "backend": backend,
            "voice": args.voice, "speed": args.speed, "fps": fps,
            "target_duration_seconds": target, "sample": args.sample, "scenes": prepared}
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
        movie = media / f"videos/scenes/{height}p{fps}" / f"{ident.upper()}.mp4"
        stamp = media / "render-input.json"
        sig = {"scenes": digest(scenes_file), "scene": scene, "voice": args.voice,
               "speed": args.speed, "backend": backend, "fps": fps, "size": [width, height],
               "runner": digest(__file__),
               "toolkit": {name: digest(ROOT / "explainer" / name) for name in
                           ("scene.py", "voice.py", "i18n.py", "style.py", "subtitles.py",
                            "events.py")}}
        if movie.exists() and stamp.exists() and json.loads(stamp.read_text()) == sig:
            print(f"Reusing {ident}", flush=True)
            return scene, movie
        media.mkdir(parents=True, exist_ok=True)
        log = media / "render.log"
        with log.open("w") as fh:
            result = subprocess.run([sys.executable, "-m", "manim", "render",
                                     "--resolution", f"{width},{height}", "--fps", str(fps),
                                     "--disable_caching", "--media_dir", str(media),
                                     str(scenes_file), ident.upper()],
                                    cwd=project, env=env, stdout=fh, stderr=subprocess.STDOUT)
        if result.returncode:
            raise RuntimeError(f"{ident} render failed:\n"
                               + "\n".join(log.read_text().splitlines()[-35:]))
        if not movie.exists():
            raise FileNotFoundError(movie)
        warnings = [l for l in log.read_text().splitlines() if "anchor not found" in l]
        if warnings and not args.sample:
            raise RuntimeError(f"{ident}: voiceover anchors missing — fix before a full build:\n"
                               + "\n".join(warnings[:5]))
        stamp.write_text(json.dumps(sig, ensure_ascii=False, indent=2))
        print(f"Rendered {ident}", flush=True)
        return scene, movie

    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        rendered = list(pool.map(render, prepared))

    # End-to-end captions use the measured timeline emitted by each actual scene.
    pairs, offset, chapters, normalized = [], 0.0, [], []
    for scene, movie in rendered:
        normalized_movie = movie.parent / f"{scene['id']}.normalized.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(movie), "-c:v", "copy",
                        "-af", "aresample=48000,apad", "-ac", "2", "-c:a", "aac", "-b:a", "160k",
                        "-t", str(scene["duration"]), str(normalized_movie)], check=True)
        normalized.append(normalized_movie)
        chapters.append({"start": offset, "id": scene["id"], "title": scene["title_en"]})
        actual = json.loads(movie.with_suffix(".subs.json").read_text())
        pairs += build_pairs(actual, scene["lines"], offset, key)
        offset += scene["duration"]

    name = f"sample-{args.sample}" if args.sample else project.name
    stem = output / name
    tracks = write_captions(pairs, stem, width, height, timing="tr" if key == "zh" else "en")
    listing = output / f"{name}.concat.txt"
    listing.write_text("".join("file '" + str(p).replace("'", "'\\''") + "'\n" for p in normalized))
    clean = output / f"{name}.clean.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
                    "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000",
                    "-c:a", "aac", "-b:a", "160k", "-t", str(target), "-movflags", "+faststart",
                    str(clean)], check=True)

    # Style conformance on real pixels, when the preset ships tokens (ready styles do).
    from .styles import tokens_path
    if tokens_path(settings["preset"]).is_file():
        from . import style_check
        with tempfile.TemporaryDirectory() as td:
            frames = style_check.sample_frames(clean, 4 if args.sample else 8, Path(td))
            problems = style_check.check_frames(frames, settings["preset"])
        if problems:
            raise RuntimeError("Style check failed:\n" + "\n".join(problems))
        print(f"Style check passed: {settings['preset']} tokens hold on sampled frames", flush=True)

    # Golden-frame regression, for episodes that committed signatures (full builds only).
    golden_path = project / "golden.json"
    if golden_path.is_file() and not args.sample:
        from . import golden
        diffs = output / "golden-diffs"
        scene_offsets = [{"id": c["id"], "start": c["start"], "duration": s["duration"]}
                         for (s, _), c in zip(rendered, chapters)]
        drift = golden.check(clean, golden_path, scene_offsets, save_diffs=diffs)
        if drift:
            where = f" (changed cells outlined in red under {diffs})" if diffs.is_dir() else ""
            raise RuntimeError(
                f"Golden-frame check failed{where}. If the change is intended, accept it "
                f"with:\n  python -m explainer.golden update {clean} --golden {golden_path}\n"
                + "\n".join(drift))
        shown = golden_path.relative_to(ROOT) if golden_path.is_relative_to(ROOT) else golden_path
        print(f"Golden frames match {shown}", flush=True)

    music = music_settings(settings, args.no_music)
    music_report = None
    burn_src = clean
    if music is not None:
        scored = output / f"{name}.scored.mp4"
        music_report = add_score(clean, scored, rendered, music, project, output / "build", target)
        burn_src = scored
        print(f"Music: voice {music_report.get('voice_lufs')} LUFS, "
              f"music {music_report.get('music_under_speech_lufs')} under speech / "
              f"{music_report.get('music_in_gaps_lufs')} in gaps", flush=True)

    from . import subtitles as subs
    ass = stem.with_suffix(".zh-en.ass")
    final = stem.with_suffix(".mp4")
    subs.burn(burn_src.relative_to(ROOT), ass.relative_to(ROOT), final.relative_to(ROOT),
              band=CAPTION_BAND, crf=20, bg=BAND_COLOUR, mode="overlay",
              fontsdir=Path("assets/fonts"), cwd=ROOT)

    validation = validate_output(final, target, len(tracks["zh-en"]), script_path, plan,
                                 chapters, music_report)
    stem.with_suffix(".validation.json").write_text(json.dumps(validation, ensure_ascii=False,
                                                               indent=2))
    stem.with_suffix(".chapters.txt").write_text("\n".join(
        f"{int(c['start']) // 60:02d}:{int(c['start']) % 60:02d} {c['title']}"
        for c in chapters) + "\n")
    duration = float(validation["probe"]["format"]["duration"])
    print(f"READY {final} — {duration:.3f}s, narrated"
          + (", scored" if music_report else "")
          + f", {len(tracks['zh-en'])} bilingual cues", flush=True)


if __name__ == "__main__":
    main()
