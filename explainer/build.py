"""Render a whole video project into one narrated mp4 with subtitles and chapter marks.

    python -m explainer.build videos/<video-id>                 # 1080p60 final (renders scenes that are
                                                                #   missing or older than their sources)
    python -m explainer.build videos/<video-id> -q l            # fast 480p15 draft
    python -m explainer.build videos/<video-id> --only s03,s04  # re-render some scenes, reuse the rest
    python -m explainer.build videos/<video-id> --no-render     # just re-stitch existing renders
    python -m explainer.build videos/<video-id> --lang zh       # the Chinese version (see explainer/i18n.py)

Reads <project>/video.yaml:

    id: dp-01-calibrating-noise
    title: "..."
    papers: [dwork2006calibrating]          # ids from library/catalog.yaml
    voice: {backend: kokoro, voice: af_heart, speed: 1.0}
    scenes:
      - {file: scenes/s01_hook.py, cls: Hook, title: "The differencing attack"}

    parts:                                   # optional: also cut the video into parts
      - {id: part1, title: "...", scenes: [s01_hook, s02_map]}

Writes <project>/output/<id>.mp4, <id>.srt, chapters.txt (YouTube/Bilibili format), transcript.md,
and <id>_<part>.mp4 / .srt / chapters_<part>.txt for each part.

Language versions (videos/<id>/i18n/<lang>/narration.yaml, see explainer/i18n.py):
  - the English build also writes <id>.<lang>.srt (translated subtitles on the English timing),
    <id>.<lang>-en.srt and <id>.<lang>-en.ass (bilingual), and with --burn <id>.<lang>-en.mp4;
  - `--lang zh` renders the Chinese version into output/zh/: <id>.mp4 with bilingual subtitles
    burned in under the picture (--no-burn keeps it clean), <id>.zh.srt, <id>.en.srt (English on the
    Chinese timing), <id>.zh-en.srt / .ass, chapters.txt and a bilingual transcript.md.
    video.yaml may set the voice per language:  languages: {zh: {voice: {backend: ..., voice: ...}}}
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import textwrap
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

from . import REPO_ROOT
from . import subtitles as subs
from .voice import backend_name, voice_identity

# default narrator per language when video.yaml has no `languages: {<lang>: {voice: ...}}`
# (edge voices switch to the official Azure endpoint when AZURE_SPEECH_KEY/REGION are set: see voice.py)
DEFAULT_VOICES = {"zh": {"backend": "edge", "voice": "zh-CN-XiaoyiNeural", "speed": 1.0}}

QUALITY_DIRS = {"l": "480p15", "m": "720p30", "h": "1080p60", "p": "1440p60", "k": "2160p60"}


def load_project(project: Path) -> dict:
    spec = yaml.safe_load((project / "video.yaml").read_text())
    spec.setdefault("id", project.name)
    return spec


def voice_spec(spec: dict, lang: str = "en") -> dict:
    if lang == "en":
        return spec.get("voice", {}) or {}
    v = ((spec.get("languages") or {}).get(lang) or {}).get("voice")
    return v or DEFAULT_VOICES.get(lang, {})


def scene_env(spec: dict, tts: str | None, lang: str | None = None) -> dict:
    env = dict(os.environ)
    lang = lang or env.get("EXPLAINER_LANG") or "en"
    v = voice_spec(spec, lang)
    if lang != "en":                       # the language's own voice, not the English one;
        for k in ("EXPLAINER_TTS", "EXPLAINER_VOICE", "EXPLAINER_SPEED"):   # EXPLAINER_TTS_ZH etc.
            env.pop(k, None)                                                  # override it
            if env.get(f"{k}_{lang.upper()}"):
                env[k] = env[f"{k}_{lang.upper()}"]
    env["EXPLAINER_LANG"] = lang
    env.setdefault("EXPLAINER_TTS", v.get("backend", "kokoro"))
    if tts:
        env["EXPLAINER_TTS"] = tts
    if v.get("voice") and "EXPLAINER_VOICE" not in env:
        env["EXPLAINER_VOICE"] = str(v["voice"])
    if v.get("speed") and "EXPLAINER_SPEED" not in env:
        env["EXPLAINER_SPEED"] = str(v["speed"])
    env["PYTHONPATH"] = os.pathsep.join(filter(None, [str(REPO_ROOT), env.get("PYTHONPATH")]))
    return env


def lang_suffix(lang: str) -> str:
    return "" if lang == "en" else f"_{lang}"


def media_dir(project: Path, quality: str, scene: dict, lang: str = "en") -> Path:
    # one media (and LaTeX) dir per scene: parallel renders must not share Manim's Tex cache,
    # whose temp files collide when two processes typeset the same formula at once
    return project / "build" / f"media_{quality}{lang_suffix(lang)}" / Path(scene["file"]).stem


def scene_movie(project: Path, quality: str, scene: dict, lang: str = "en") -> Path:
    stem = Path(scene["file"]).stem
    return (media_dir(project, quality, scene, lang) / "videos" / stem / QUALITY_DIRS[quality]
            / f"{scene['cls']}.mp4")


def voice_stamp(project: Path, quality: str, scene: dict, lang: str = "en") -> Path:
    """Records the narrator (voice.voice_identity) a scene render was made with."""
    return media_dir(project, quality, scene, lang) / "voice.json"


def is_stale(project: Path, quality: str, scene: dict, lang: str = "en", voice: str | None = None) -> bool:
    """A scene needs rendering if its movie is missing or older than anything it is built from:
    its own file, the other .py files next to it (shared helpers), the script, video.yaml, assets,
    and the toolkit; or (with `voice`, a voice.voice_identity()) if it was rendered with another
    narrator, e.g. after AZURE_SPEECH_KEY was set or the voice changed."""
    movie = scene_movie(project, quality, scene, lang)
    if not movie.exists():
        return True
    if voice is not None:
        stamp = voice_stamp(project, quality, scene, lang)
        if not stamp.exists() or stamp.read_text().strip() != voice:
            return True
    scene_file = project / scene["file"]
    sources = [scene_file, *scene_file.parent.glob("*.py"), project / "script.md", project / "video.yaml",
               *(project / "assets").glob("*"), *Path(__file__).parent.glob("*.py"),
               *Path(__file__).parent.glob("*.yaml")]
    if lang != "en":
        tr = project / "i18n" / lang                 # what a render reads (not the glossary or companions)
        sources += [p for d in ("narration", "strings", "assets") for p in (tr / d).rglob("*") if p.is_file()]
        sources += [p for p in tr.glob("*.yaml") if p.stem in ("narration", "strings")]
        sources += list((Path(__file__).parent / "locales").glob("*.yaml"))
    newest = max((p.stat().st_mtime for p in sources if p.is_file()), default=0.0)
    return movie.stat().st_mtime < newest


def render_scene(project: Path, quality: str, scene: dict, env: dict) -> Path:
    lang = env.get("EXPLAINER_LANG", "en")
    cmd = [sys.executable, "-m", "manim", "render", f"-q{quality}", "--disable_caching", "--no_latex_cleanup",
           "--media_dir", str(media_dir(project, quality, scene, lang)), scene["file"], scene["cls"]]
    log = project / "build" / "logs" / f"{Path(scene['file']).stem}_{scene['cls']}{lang_suffix(lang)}.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "w") as fh:
        res = subprocess.run(cmd, cwd=project, env=env, stdout=fh, stderr=subprocess.STDOUT)
    if res.returncode != 0:
        tail = "\n".join(log.read_text().splitlines()[-30:])
        raise RuntimeError(f"render failed for {scene['cls']} (see {log}):\n{tail}")
    out = scene_movie(project, quality, scene, lang)
    if not out.exists():
        raise FileNotFoundError(out)
    for line in log.read_text(errors="replace").splitlines():
        if "anchor not found" in line or "no zh translation" in line or "translation for narration" in line:
            print(f"  WARNING {scene['cls']}: {line.strip()}", flush=True)
    print(f"  rendered {scene['cls']:<24} -> {out.relative_to(project)}", flush=True)
    voice_stamp(project, quality, scene, lang).write_text(voice_identity(env))
    return out


def ffprobe_duration(path: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                        "csv=p=0", str(path)], capture_output=True, text=True, check=True)
    return float(r.stdout.strip())


def has_audio(path: Path) -> bool:
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                        "stream=index", "-of", "csv=p=0", str(path)], capture_output=True, text=True)
    return bool(r.stdout.strip())


def normalize(src: Path, dst: Path, crf: int | None = None) -> None:
    """Same audio layout for every scene (48 kHz stereo AAC, padded to video length).

    With `crf`, the video is re-encoded once here (x264, tuned for flat animation), so the full
    video and every part are later joined without re-encoding."""
    vcodec = ["-c:v", "copy"] if crf is None else [
        "-c:v", "libx264", "-preset", "medium", "-tune", "animation", "-crf", str(crf), "-pix_fmt", "yuv420p"]
    if has_audio(src):
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src), *vcodec, "-af",
               "aresample=48000,apad", "-ac", "2", "-c:a", "aac", "-b:a", "192k", "-shortest", str(dst)]
    else:
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-f", "lavfi", "-i",
               "anullsrc=r=48000:cl=stereo", *vcodec, "-c:a", "aac", "-b:a", "192k",
               "-shortest", str(dst)]
    subprocess.run(cmd, check=True)


def fmt_srt(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def fmt_chapter(t: float) -> str:
    t = int(t)
    return f"{t // 3600}:{t % 3600 // 60:02d}:{t % 60:02d}" if t >= 3600 else f"{t // 60:02d}:{t % 60:02d}"


def _fits(text: str, width: int, lines: int) -> bool:
    return len(textwrap.wrap(text, width)) <= lines


def _split_sentence(sent: str, width: int, lines: int) -> list[str]:
    """Split one sentence into the fewest balanced pieces that each fit in `lines` lines, cutting
    at a clause boundary (", ", ": ", "; ") near each ideal cut point when there is one, else at a
    space. Avoids a 1-2 word tail on its own cue."""
    import re

    sent = " ".join(sent.split())
    if _fits(sent, width, lines):
        return [sent]
    clause = [m.end() for m in re.finditer(r"[,:;]\s", sent)]
    spaces = [m.end() for m in re.finditer(r"\s", sent)]
    def penalty(c):                     # word gaps cost more than clause cuts (subtitles._cut_penalty)
        return subs._cut_penalty(sent, c) * 1.8

    for k in range(2, 12):
        for pool_of in (lambda prev, ideal: [c for c in clause if prev < c],      # clauses, if they fit
                        lambda prev, ideal: ([c for c in clause if prev < c and abs(c - ideal) <= len(sent) / (2.5 * k)]
                                             or [c for c in spaces if prev < c])):
            cuts, prev = [], 0
            for j in range(1, k):
                ideal = len(sent) * j / k
                pool = pool_of(prev, ideal)
                if not pool:
                    break
                cut = min(pool, key=lambda c: abs(c - ideal) + penalty(c))
                cuts.append(cut)
                prev = cut
            if len(cuts) != k - 1:
                continue
            pieces = [sent[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(sent)])]
            if all(p and _fits(p, width, lines) for p in pieces):
                return pieces
    return [" ".join(w) for w in [textwrap.wrap(sent, width)]]


def split_cues(start: float, end: float, text: str, width: int = 44, lines: int = 2,
               marks: list | None = None, min_dur: float = 1.0):
    """Break one narration clip into readable cues (<= 2 lines each), never across sentences.

    With `marks` ((char offset, seconds) of each sentence start, from the voice clip), every
    sentence's cues sit exactly where that sentence is spoken; without them, the whole clip is
    timed proportionally to characters. Inside a sentence, cues are timed by characters. Cues
    shorter than `min_dur` are merged with a neighbour when the result still fits."""
    from .voice import SENTENCE_GAP, split_sentences

    sentences = split_sentences(text) or [(0, text)]
    if marks and [int(o) for o, _ in marks] == [o for o, _ in sentences]:
        starts = [start + float(t) for _, t in marks]
        spans = [(a, (starts[i + 1] - SENTENCE_GAP) if i + 1 < len(starts) else end)
                 for i, a in enumerate(starts)]
    else:
        total = sum(len(s) for _, s in sentences) or 1
        spans, t = [], start
        for _, sent in sentences:
            dt = (end - start) * len(sent) / total
            spans.append((t, t + dt))
            t += dt
    cues = []
    for (a, b), (_, sent) in zip(spans, sentences):
        pieces = _split_sentence(sent, width, lines)
        total = sum(len(c) for c in pieces) or 1
        t = a
        for c in pieces:
            dt = max(0.0, b - a) * len(c) / total
            cues.append([t, t + dt, c])
            t += dt
    merged = True
    while merged:                       # fold too-short cues into a neighbour when the text fits
        merged = False
        for i, (a, b, c) in enumerate(cues):
            if b - a >= min_dur or len(cues) == 1:
                continue
            for j in (i - 1, i + 1) if i > 0 else (i + 1,):
                if 0 <= j < len(cues):
                    lo, hi = min(i, j), max(i, j)
                    joined = cues[lo][2] + " " + cues[hi][2]
                    if _fits(joined, width, lines):
                        cues[lo:hi + 1] = [[cues[lo][0], cues[hi][1], joined]]
                        merged = True
                        break
            if merged:
                break
    return [(a, b, "\n".join(textwrap.wrap(c, width))) for a, b, c in cues]


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project", type=Path)
    ap.add_argument("-q", "--quality", default="h", choices=list(QUALITY_DIRS))
    ap.add_argument("--only", help="comma-separated scene file stems or class names to (re)render")
    ap.add_argument("--no-render", action="store_true", help="only stitch existing scene renders")
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 2) // 2))
    ap.add_argument("--tts", help="override the voice backend (kokoro|elevenlabs|edge|azure|espeak|silent)")
    ap.add_argument("--crf", type=int, help="re-encode each scene with x264 at this CRF (smaller files; ~25 is good)")
    ap.add_argument("--render-only", action="store_true", help="render the selected scenes, don't stitch")
    ap.add_argument("--lang", default="en", help="language version to build (en, zh, ...)")
    ap.add_argument("--burn", action="store_true", help="English build: also burn bilingual subtitles "
                    "(<id>.<lang>-en.mp4) for each translation")
    ap.add_argument("--no-burn", action="store_true", help="translated build: keep the video clean")
    ap.add_argument("--subs-only", action="store_true", help="only (re)write subtitles, chapters and transcript "
                    "from existing renders; leave the video files alone")
    args = ap.parse_args(argv)

    project = args.project.resolve()
    spec = load_project(project)
    scenes = spec["scenes"]
    lang = args.lang
    env = scene_env(spec, args.tts, lang)
    env["EXPLAINER_PROJECT"] = str(project)
    only = set(args.only.split(",")) if args.only else None
    if lang != "en":
        from .i18n import check_narration
        problems = check_narration(project, lang)
        for p in problems:
            print("  WARNING", p)

    if args.no_render or args.subs_only:
        todo = []
    elif only is not None:  # exactly the named scenes
        todo = [s for s in scenes if Path(s["file"]).stem in only or s["cls"] in only]
    else:                   # whatever is missing or older than its sources
        voice = voice_identity(env)
        todo = [s for s in scenes if is_stale(project, args.quality, s, lang, voice)]
    if todo:
        print(f"Rendering {len(todo)} scene(s) at {QUALITY_DIRS[args.quality]} lang={lang} "
              f"with TTS={backend_name(env)} voice={env.get('EXPLAINER_VOICE', '-')} (jobs={args.jobs})",
              flush=True)
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            list(pool.map(lambda s: render_scene(project, args.quality, s, env), todo))
    if args.render_only:
        return

    build = project / "build" / f"stitch_{args.quality}{lang_suffix(lang)}"
    build.mkdir(parents=True, exist_ok=True)
    out_dir = project / "output" / ("" if lang == "en" else lang)
    out_dir.mkdir(parents=True, exist_ok=True)

    normalized = []
    for i, s in enumerate(scenes):
        movie = scene_movie(project, args.quality, s, lang)
        if not movie.exists():
            raise SystemExit(f"missing render for {s['cls']}: {movie}")
        norm = build / f"{i:02d}_{s['cls']}{'' if args.crf is None else f'_crf{args.crf}'}.mp4"
        if args.subs_only:
            norm = norm if norm.exists() else movie        # durations only
        elif not norm.exists() or norm.stat().st_mtime < movie.stat().st_mtime:
            normalize(movie, norm, args.crf)
        normalized.append((s, movie, norm))

    suffix = "" if args.quality == "h" else "_" + QUALITY_DIRS[args.quality]
    meta = {}
    if lang != "en":
        from .i18n import meta as lang_meta
        meta = lang_meta(lang, project)
    title = meta.get("title") or spec.get("title", spec["id"])
    ctx = dict(project=project, spec=spec, lang=lang, meta=meta, build=build, env=env,
               burn=(not args.no_burn) if lang != "en" else args.burn, subs_only=args.subs_only)
    stitch(normalized, out_dir / f"{spec['id']}{suffix}", title, build, chapters_file=out_dir / "chapters.txt",
           transcript_file=out_dir / "transcript.md", ctx=ctx)
    for part in spec.get("parts") or []:
        keep = set(part["scenes"])
        subset = [t for t in normalized if Path(t[0]["file"]).stem in keep or t[0]["cls"] in keep]
        ptitle = ((meta.get("parts") or {}).get(part["id"])) or part.get("title", part["id"])
        stitch(subset, out_dir / f"{spec['id']}_{part['id']}{suffix}", ptitle, build,
               chapters_file=out_dir / f"chapters_{part['id']}.txt", ctx=ctx)


def _scene_title(s: dict, meta: dict) -> str:
    titles = meta.get("chapters") or {}
    return titles.get(Path(s["file"]).stem) or titles.get(s["cls"]) or s.get("title", s["cls"])


def _clips_with_marks(subs_file: Path, env: dict | None) -> list[dict]:
    """Narration clips of one scene; English clips rendered before sentence marks were recorded get
    their marks from the (cached) voice, so subtitles still land on each sentence."""
    clips = json.loads(subs_file.read_text()) if subs_file.exists() else []
    need = [c for c in clips if not c.get("tr") and not c.get("marks")]
    if need and env and env.get("EXPLAINER_LANG", "en") == "en":
        old = {k: os.environ.get(k) for k in ("EXPLAINER_TTS", "EXPLAINER_VOICE", "EXPLAINER_SPEED")}
        try:
            for k in old:
                if env.get(k):
                    os.environ[k] = env[k]
            from .voice import get_backend
            backend = get_backend()
            for c in need:
                clip = backend.speak(c["text"])
                if abs(clip.duration - (c["end"] - c["start"])) < 0.05:
                    c["marks"] = [[o, t] for o, t in clip.marks]
        except Exception as e:  # subtitles fall back to proportional timing
            print(f"  (sentence marks unavailable: {e})")
        finally:
            for k, v in old.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
    return clips


def stitch(items, stem: Path, title: str, build: Path, chapters_file: Path,
           transcript_file: Path | None = None, ctx: dict | None = None) -> None:
    """Concatenate normalized scene files into stem.mp4 (+ subtitles, chapters, transcript)."""
    ctx = ctx or {}
    lang = ctx.get("lang", "en")
    meta = ctx.get("meta", {})
    project = ctx.get("project")
    translations = {}                          # English build: every language with a narration file
    if lang == "en" and project is not None:
        from .i18n import narration
        langs = sorted({p.parent.name for p in (project / "i18n").glob("*/narration.yaml")} |
                       {p.parent.parent.name for p in (project / "i18n").glob("*/narration/*.yaml")}) \
            if (project / "i18n").exists() else []
        for code in langs:
            translations[code] = narration(code, project)

    own_table = {}                             # translated build: the spoken forms (subtitle timing)
    if lang != "en" and project is not None:
        from .i18n import narration
        own_table = narration(lang, project)

    srt, chapters, transcript, offset = [], [], [f"# {title}\n"], 0.0
    pairs: dict[str, list] = {code: [] for code in translations}
    own_pairs = []
    for s, movie, norm in items:
        name = _scene_title(s, meta)
        if s.get("chapter", True):
            chapters.append(f"{fmt_chapter(offset)} {name}")
        transcript.append(f"\n## {fmt_chapter(offset)} — {name}\n")
        for cue in _clips_with_marks(movie.with_suffix(".subs.json"), ctx.get("env")):
            if cue.get("tr"):
                transcript.append("".join(cue["tr"]) + "\n> " + cue["text"] + "\n\n")
                own_pairs += subs.sentence_pairs(cue, offset, own_table.get(" ".join(cue["text"].split())))
            else:
                transcript.append(cue["text"] + "\n")
                srt.extend(split_cues(offset + cue["start"], offset + cue["end"], cue["text"],
                                      marks=cue.get("marks")))
                for code, table in translations.items():
                    line = table.get(" ".join(cue["text"].split()))
                    pairs[code] += subs.sentence_pairs(cue, offset, line)
        offset += ffprobe_duration(norm)

    subs_only = ctx.get("subs_only")
    final = stem.with_suffix(".mp4") if lang == "en" else build / f"{stem.name}.clean.mp4"
    if not subs_only:
        listing = build / f"concat_{stem.name}.txt"
        listing.write_text("".join(f"file '{n}'\n" for _, _, n in items))
        joined = build / f"joined_{stem.name}.mp4"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", str(listing),
                        "-c", "copy", str(joined)], check=True)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(joined), "-c:v", "copy", "-af",
                        "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "128k",
                        "-movflags", "+faststart", str(final)], check=True)
        joined.unlink(missing_ok=True)
    made = []
    if lang == "en":
        stem.with_suffix(".srt").write_text("".join(
            f"{n}\n{fmt_srt(a)} --> {fmt_srt(b)}\n{t}\n\n" for n, (a, b, t) in enumerate(srt, 1)))
        made.append(".srt")
        for code, prs in pairs.items():
            if not any(p[2] for p in prs):
                continue
            tr_ = subs.tracks(prs, timing="en")
            subs.write_srt(Path(f"{stem}.{code}.srt"), tr_["zh"])
            subs.write_srt(Path(f"{stem}.{code}-en.srt"), [(a, b, z, e) for a, b, z, e in tr_["zh-en"]])
            ass = Path(f"{stem}.{code}-en.ass")
            subs.write_ass(ass, tr_["zh-en"], title=title)
            made += [f".{code}.srt", f".{code}-en.srt/.ass"]
            if ctx.get("burn") and not subs_only:
                subs.burn(final, ass, Path(f"{stem}.{code}-en.mp4"))
                made.append(f".{code}-en.mp4")
    else:
        tr_ = subs.tracks(own_pairs, timing="tr")
        subs.write_srt(Path(f"{stem}.{lang}.srt"), tr_["zh"])
        subs.write_srt(Path(f"{stem}.en.srt"), tr_["en"])
        subs.write_srt(Path(f"{stem}.{lang}-en.srt"), [(a, b, z, e) for a, b, z, e in tr_["zh-en"]])
        ass = Path(f"{stem}.{lang}-en.ass")
        subs.write_ass(ass, tr_["zh-en"], title=title)
        made += [f".{lang}.srt", ".en.srt", f".{lang}-en.srt/.ass"]
        out = stem.with_suffix(".mp4")
        if subs_only:
            pass
        elif ctx.get("burn", True):
            subs.burn(final, ass, out)
            made.append(" (bilingual subtitles burned in)")
        else:
            subprocess.run(["cp", str(final), str(out)], check=True)
        final = out
    chapters_file.write_text("\n".join(chapters) + "\n")
    if transcript_file:
        transcript_file.write_text("".join(transcript))
    size = f"{final.stat().st_size / 1e6:.1f} MB" if final.exists() else "video not written"
    print(f"Done: {final.name}  ({fmt_chapter(offset)}, {size}) + {', '.join(made)}, {chapters_file.name}")


if __name__ == "__main__":
    main()
