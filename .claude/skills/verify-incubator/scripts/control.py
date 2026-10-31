#!/usr/bin/env python3
"""Drive the incubator the way its users do and keep the evidence.

Every command takes --run ID (lowercase letters/digits). A run owns, and cleanup removes:
  outputs/verify/<run>/work/          episode copies and the served Studio site
  outputs/<slug>-vfy<run>/            the renderer's output dir for those copies
  videos/verify-<run>*/               episodes scaffolded by the new-episode journey
Cleanup never touches outputs/verify/<run>/evidence/, which is where every proof lands.

  python3 .claude/skills/verify-incubator/scripts/control.py doctor --run r1
  python3 .claude/skills/verify-incubator/scripts/control.py render-sample --run r1 videos/skills-ecosystem s01
  python3 .claude/skills/verify-incubator/scripts/control.py render-sample --run r1 videos/skills-ecosystem s01 --prepare-only
  python3 .claude/skills/verify-incubator/scripts/control.py cli --run r1 --name scaffold -- python3 skill-library/conny-explainer-video/scripts/new_episode.py verify-r1 --topic "..." --workspace .
  python3 .claude/skills/verify-incubator/scripts/control.py studio-up --run r1 [--snapshot snap.json | --offline]
  python3 .claude/skills/verify-incubator/scripts/control.py browse --run r1 --name board steps.json
  python3 .claude/skills/verify-incubator/scripts/control.py cleanup --run r1
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[4]
HERE = Path(__file__).resolve().parent
RENDER = ROOT / "skill-library/conny-explainer-video/scripts/render.py"
PYTHON = ROOT / ".venv/bin/python"


def run_dir(run: str) -> Path:
    return ROOT / "outputs/verify" / run


def evidence(run: str) -> Path:
    path = run_dir(run) / "evidence"
    path.mkdir(parents=True, exist_ok=True)
    return path


def record(run: str, name: str, command: list[str], cwd: Path = ROOT, env=None) -> int:
    """Run a command, tee its output, and save command/stdout/stderr/exit code as evidence."""
    out = evidence(run)
    (out / f"{name}.cmd").write_text(" ".join(map(str, command)) + "\n")
    print("+", " ".join(map(str, command)), flush=True)
    proc = subprocess.run(list(map(str, command)), cwd=cwd, env=env, capture_output=True, text=True)
    (out / f"{name}.stdout").write_text(proc.stdout)
    (out / f"{name}.stderr").write_text(proc.stderr)
    (out / f"{name}.exit").write_text(f"{proc.returncode}\n")
    sys.stdout.write(proc.stdout[-4000:])
    sys.stderr.write(proc.stderr[-4000:])
    print(f"exit {proc.returncode}; evidence in {out.relative_to(ROOT)}/{name}.*", flush=True)
    return proc.returncode


def ffprobe(path: Path) -> dict:
    return json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)]))


def srt_cues(path: Path) -> list[tuple[float, float, str]]:
    def seconds(stamp):
        h, m, rest = stamp.split(":")
        s, ms = rest.split(",")
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
    cues = []
    for block in path.read_text(encoding="utf-8").strip().split("\n\n"):
        lines = block.strip().splitlines()
        if len(lines) >= 3 and "-->" in lines[1]:
            start, end = (seconds(x.strip()) for x in lines[1].split("-->"))
            cues.append((start, end, " / ".join(lines[2:])))
    return cues


# ------------------------------------------------------------------------------ doctor
def doctor(args) -> int:
    rows = []

    def check(name, ok, detail=""):
        rows.append((name, bool(ok), detail))

    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    check("checkout", head.returncode == 0, f"{ROOT} @ {head.stdout.strip()}")
    check("venv python", PYTHON.is_file(), str(PYTHON.relative_to(ROOT)))
    if PYTHON.is_file():
        probe = subprocess.run([str(PYTHON), "-c", "import manim, kokoro_onnx, soundfile; print(manim.__version__)"],
                               capture_output=True, text=True)
        check("engine imports", probe.returncode == 0, (probe.stdout or probe.stderr).strip()[-200:])
    manifest = json.loads((ROOT / "assets/manifest.json").read_text())
    wrong = [p for p, r in manifest.items() if not (ROOT / p).is_file() or (ROOT / p).stat().st_size != r["bytes"]]
    check("fonts + speech model", not wrong, "sizes match assets/manifest.json" if not wrong else f"missing/short: {wrong}")
    filters = subprocess.run(["ffmpeg", "-hide_banner", "-filters"], capture_output=True, text=True).stdout
    check("ffmpeg with libass + loudnorm", " ass " in filters and " loudnorm " in filters)
    check("ffprobe", shutil.which("ffprobe"))
    if args.run:
        state = run_dir(args.run) / "studio.json"
        if state.is_file():
            info = json.loads(state.read_text())
            try:
                marker = urllib.request.urlopen(f"http://127.0.0.1:{info['port']}/.verify-run", timeout=3).read().decode().strip()
            except OSError as error:
                marker = f"unreachable ({error})"
            check("studio server is this run's", marker == args.run,
                  f"pid {info['pid']} port {info['port']} answers {marker!r}")
    mine = re.compile(rf"(-vfy{args.run}|verify-{args.run})(-|$)") if args.run else None
    leftovers = sorted(str(p.relative_to(ROOT)) for p in
                       [*ROOT.glob("outputs/*-vfy*"), *ROOT.glob("videos/verify-*")]
                       if not (mine and mine.search(p.name)))
    check("no other run's leftovers", not leftovers,
          ", ".join(leftovers) + " (finish that run's cleanup)" if leftovers else "clean")
    width = max(len(r[0]) for r in rows)
    for name, ok, detail in rows:
        print(f"{'OK  ' if ok else 'FAIL'} {name:{width}}  {detail}")
    return 0 if all(ok for _, ok, _ in rows) else 1


# ------------------------------------------------------------------------------ renderer
def render_sample(args) -> int:
    source = (ROOT / args.episode).resolve() if not Path(args.episode).is_absolute() else Path(args.episode)
    if not (source / "script.json").is_file() or not (source / "scenes.py").is_file():
        sys.exit(f"{source} is not an episode.json-route episode (needs script.json and scenes.py)")
    name = f"{source.name}-vfy{args.run}"
    work = run_dir(args.run) / "work" / name
    if work.exists():
        shutil.rmtree(work)
    shutil.copytree(source, work, ignore=shutil.ignore_patterns("build", "output", "__pycache__"))
    out = evidence(args.run)
    label = f"{args.scene}-prepare" if args.prepare_only else args.scene
    command = ["python3", RENDER, work, "--sample", args.scene] + (["--prepare-only"] if args.prepare_only else [])
    started = time.time()
    code = record(args.run, f"render-{label}", command)
    produced = ROOT / "outputs" / name
    results: list[tuple[str, bool, str]] = [("render exit code 0", code == 0, f"{time.time() - started:.0f}s")]
    plan_path = produced / f"plan-{args.scene}.json"
    plan = json.loads(plan_path.read_text()) if plan_path.is_file() else None
    results.append(("plan written", plan is not None, str(plan_path.relative_to(ROOT))))
    if plan:
        shutil.copy2(plan_path, out / f"{label}.plan.json")
        clips = [Path(a["path"]) for s in plan["scenes"] for a in s["audio"]]
        lines = sum(len(s["lines"]) for s in plan["scenes"])
        results.append(("one speech clip per narration line",
                        len(clips) == lines and all(c.is_file() and c.stat().st_size > 0 for c in clips),
                        f"{len(clips)} clips for {lines} lines"))
    if not args.prepare_only and code == 0:
        stem = produced / f"sample-{args.scene}"
        for suffix in (".mp4", ".validation.json", ".zh-en.ass", ".zh-en.srt", ".chapters.txt"):
            if stem.with_suffix(suffix).is_file():
                shutil.copy2(stem.with_suffix(suffix), out / f"{label}{suffix}")
        final = out / f"{label}.mp4"
        meta = ffprobe(final)
        (out / f"{label}.ffprobe.json").write_text(json.dumps(meta, indent=2))
        video = next(s for s in meta["streams"] if s["codec_type"] == "video")
        validation = json.loads((out / f"{label}.validation.json").read_text())
        duration = float(meta["format"]["duration"])
        stdout = (out / f"render-{label}.stdout").read_text()
        results += [
            ("READY line printed", "READY " in stdout, next((l for l in stdout.splitlines() if l.startswith("READY")), "")),
            ("1920x1080 @ 30 fps", (video["width"], video["height"], video["r_frame_rate"]) == (1920, 1080, "30/1"),
             f"{video['width']}x{video['height']} @ {video['r_frame_rate']}"),
            ("has an audio stream", any(s["codec_type"] == "audio" for s in meta["streams"])),
            ("duration matches the plan", abs(duration - plan["target_duration_seconds"]) <= 0.1,
             f"{duration:.3f}s vs {plan['target_duration_seconds']}s"),
            ("validation: script unchanged during render", validation.get("source_matches_plan") is True),
            ("validation: narration audible", validation.get("audio_mean_db", -99) > -45, f"{validation.get('audio_mean_db')} dB"),
        ]
        if plan["resolved_settings"].get("music", {}).get("enabled"):
            results.append(("validation: music measured", "music" in validation,
                            json.dumps({k: validation.get("music", {}).get(k) for k in
                                        ("voice_lufs", "music_under_speech_lufs", "music_in_gaps_lufs")})))
        cues = srt_cues(out / f"{label}.zh-en.srt")
        both = [c for c in cues if re.search(r"[\u4e00-\u9fff]", c[2].split(" / ")[0])
                and re.search(r"[A-Za-z]", c[2].split(" / ")[-1])]
        results.append(("every cue: Chinese line above English line", cues and len(both) == len(cues),
                        f"{len(both)}/{len(cues)} cues"))
        frames = out / f"{label}.frames"
        frames.mkdir(exist_ok=True)
        for i, (start, end, text) in enumerate(cues, 1):
            at = (start + end) / 2
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{at:.3f}", "-i", str(final),
                            "-frames:v", "1", str(frames / f"cue{i:02d}-{at:06.2f}s.png")], check=True)
            (frames / f"cue{i:02d}-{at:06.2f}s.txt").write_text(text + "\n")
        results.append(("frame captured at every cue", len(list(frames.glob("*.png"))) == len(cues),
                        str(frames.relative_to(ROOT))))
    summary = {"run": args.run, "episode": str(source.relative_to(ROOT)), "copy": name, "scene": args.scene,
               "prepare_only": args.prepare_only,
               "commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip(),
               "checks": [{"check": c, "ok": bool(ok), "detail": d} for c, ok, *rest in results for d in [rest[0] if rest else ""]]}
    (out / f"{label}.summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    for item in summary["checks"]:
        print(f"{'PASS' if item['ok'] else 'FAIL'} {item['check']}  {item['detail']}")
    passed = all(c["ok"] for c in summary["checks"])
    print(f"{'PASS' if passed else 'FAIL'}: {out.relative_to(ROOT)}/{label}.summary.json")
    return 0 if passed else 1


def cli(args) -> int:
    command = args.command[1:] if args.command[:1] == ["--"] else args.command
    if not command:
        sys.exit("give the command after --")
    return record(args.run, args.name, command)


# ------------------------------------------------------------------------------ Studio site
def free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def studio_up(args) -> int:
    state = run_dir(args.run) / "studio.json"
    if state.is_file():
        sys.exit(f"run {args.run} already has a Studio server ({state}); studio-down first")
    site = run_dir(args.run) / "work/site"
    if site.exists():
        shutil.rmtree(site)
    shutil.copytree(ROOT / "site", site, ignore=shutil.ignore_patterns("data"))
    (site / ".verify-run").write_text(args.run + "\n")
    build = ["python3", "tools/studio_status.py", "--out", site / "data"]
    if args.snapshot:
        build += ["--snapshot", Path(args.snapshot).resolve()]
    elif args.offline:
        build += ["--offline"]
    else:
        build += ["--save-snapshot", evidence(args.run) / "studio-snapshot.json"]
    if record(args.run, "studio-build", build):
        return 1
    for name in ("status.json", "library.json"):
        shutil.copy2(site / "data" / name, evidence(args.run) / f"studio-{name}")
    port = args.port or free_port()
    log = (evidence(args.run) / "studio-server.log").open("w")
    server = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
                               "--directory", str(site)], stdout=log, stderr=subprocess.STDOUT,
                              start_new_session=True)
    state.write_text(json.dumps({"pid": server.pid, "port": port, "site": str(site)}))
    for _ in range(50):
        try:
            marker = urllib.request.urlopen(f"http://127.0.0.1:{port}/.verify-run", timeout=1).read().decode().strip()
            data = json.loads(urllib.request.urlopen(f"http://127.0.0.1:{port}/data/status.json", timeout=1).read())
            if marker == args.run and "episodes" in data:
                print(f"READY http://127.0.0.1:{port}/  (pid {server.pid}, {len(data['episodes'])} episodes on the board)")
                return 0
        except OSError:
            time.sleep(0.2)
    print("Studio server did not become ready; see studio-server.log", file=sys.stderr)
    return 1


def studio_down(args) -> int:
    state = run_dir(args.run) / "studio.json"
    if not state.is_file():
        print(f"run {args.run} has no Studio server")
        return 0
    info = json.loads(state.read_text())
    try:
        os.killpg(info["pid"], signal.SIGTERM)   # the server we started, in its own session
        print(f"stopped pid {info['pid']} (port {info['port']})")
    except ProcessLookupError:
        print(f"pid {info['pid']} already gone")
    state.unlink()
    return 0


def browse(args) -> int:
    out = evidence(args.run)
    state = run_dir(args.run) / "studio.json"
    base = f"http://127.0.0.1:{json.loads(state.read_text())['port']}/" if state.is_file() else ""
    return record(args.run, f"browse-{args.name}",
                  ["node", HERE / "browser.cjs", Path(args.steps).resolve(), out, args.name, base])


# ------------------------------------------------------------------------------ cleanup
def cleanup(args) -> int:
    studio_down(args)
    removed = []
    for path in [run_dir(args.run) / "work", *ROOT.glob(f"outputs/*-vfy{args.run}"),
                 *ROOT.glob(f"videos/verify-{args.run}*")]:
        if path.exists():
            shutil.rmtree(path)
            removed.append(str(path.relative_to(ROOT)))
    print("removed:", ", ".join(removed) or "nothing")
    kept = evidence(args.run)
    print(f"evidence kept: {kept.relative_to(ROOT)} ({sum(1 for _ in kept.rglob('*'))} files)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def command(name, func, run_required=True):
        p = sub.add_parser(name)
        p.add_argument("--run", required=run_required, type=lambda v: v if re.fullmatch(r"[a-z0-9]+", v)
                       else ap.error("--run takes lowercase letters and digits"))
        p.set_defaults(func=func)
        return p

    command("doctor", doctor, run_required=False)
    p = command("render-sample", render_sample)
    p.add_argument("episode")
    p.add_argument("scene")
    p.add_argument("--prepare-only", action="store_true")
    p = command("cli", cli)
    p.add_argument("--name", required=True)
    p.add_argument("command", nargs=argparse.REMAINDER)
    p = command("studio-up", studio_up)
    p.add_argument("--port", type=int)
    group = p.add_mutually_exclusive_group()
    group.add_argument("--snapshot")
    group.add_argument("--offline", action="store_true")
    command("studio-down", studio_down)
    p = command("browse", browse)
    p.add_argument("--name", required=True)
    p.add_argument("steps")
    command("cleanup", cleanup)
    args = ap.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
