#!/usr/bin/env python3
"""Run tools/publish_worker.py's real main() under every schedule a scenario allows.

The worker's only shared state is ~/.config/explainer-publish/state.json and the Bilibili
channel itself. This explorer runs one thread per worker run, replaces gh/biliup with a fake
GitHub and a fake Bilibili, and pauses every run at each step that touches shared state:

  read state.json   load_state()       -> STATE.read_text()
  write state.json  save_state()       -> STATE.write_text()
  biliup upload     main()             -> subprocess.run(["biliup", "upload", ...])

At each pause it chooses which run moves next and how the step ends (a crash first, a torn
write, an upload that fails, an upload Bilibili kept although biliup exited non-zero). It
then backtracks until it has tried every choice sequence. Steps that touch only one run's
own temp files, or that only add issue comments, commute with everything else, so pausing
there would add schedules without adding outcomes.

After each scenario, clean runs (no crashes, uploads succeed) drain the queue. Then two
properties are checked:

  at-most-once  every release tag reaches Bilibili at most once
  eventually    every release tag reaches Bilibili at least once

Usage (from the repository root; plain python3, stdlib only):
  python3 .claude/skills/verify-publish-worker/scripts/explore.py            # every scenario
  python3 .claude/skills/verify-publish-worker/scripts/explore.py baseline   # one scenario
  python3 .claude/skills/verify-publish-worker/scripts/explore.py --expect   # exit 1 on drift

Exit status: 0 when every scenario matches its expected verdict under --expect (otherwise
0 only when every property holds), 1 otherwise.
"""
from __future__ import annotations

import argparse
import base64
import contextlib
import hashlib
import io
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import threading
from dataclasses import dataclass, field

ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "tools"))
import publish_worker as pw  # noqa: E402  the code under verification

REPO = "o/r"
ARGV = ["publish_worker.py", "--repo", REPO, "--upload"]  # the command the Studio board shows
TAGS = ["episode/alpha-v1", "episode/beta-v1"]  # GitHub lists newest first; order is fixed


@dataclass(frozen=True)
class Scenario:
    name: str
    about: str
    runs: int           # scheduled runs before the clean drain
    parallel: int       # how many of them may be alive at once
    crashes: int        # process deaths (and torn writes) allowed per schedule
    failures: int       # biliup failures allowed per schedule
    ambiguous: bool     # may biliup exit non-zero after Bilibili kept the video?
    expect: dict        # property -> True (holds) / False (known finding)


SCENARIOS = [
    Scenario("baseline", "one run at a time; uploads may fail and are retried; nobody crashes",
             runs=3, parallel=1, crashes=0, failures=1, ambiguous=False,
             expect={"at-most-once": True, "eventually": True}),
    Scenario("overlap", "a scheduled run and a hand run (the Studio board's command) overlap",
             runs=2, parallel=2, crashes=0, failures=0, ambiguous=False,
             expect={"at-most-once": False, "eventually": True}),
    Scenario("crash", "one run at a time; one run dies at any step, mid-write included",
             runs=2, parallel=1, crashes=1, failures=0, ambiguous=False,
             expect={"at-most-once": False, "eventually": False}),
    Scenario("ambiguous", "one run at a time; biliup exits non-zero after Bilibili kept the video",
             runs=2, parallel=1, crashes=0, failures=1, ambiguous=True,
             expect={"at-most-once": False, "eventually": True}),
]


class Crash(BaseException):
    """The worker process dies here (launchd kill, sleep, power). Not an Exception, so the
    worker's own except-clauses cannot catch it, as with a real SIGKILL."""


# --------------------------------------------------------------------------- the world
@dataclass
class World:
    state_dir: pathlib.Path
    uploads: list = field(default_factory=list)   # (tag, run) for every video Bilibili kept
    trace: list = field(default_factory=list)     # plain-words steps, in schedule order
    errors: list = field(default_factory=list)    # (run, exception text) for runs that died on a bug
    serial: int = 0

    def video(self, tag: str) -> bytes:
        return f"video for {tag}".encode()

    def manifest(self, tag: str) -> dict:
        slug = tag.split("/")[1].rsplit("-v", 1)[0]
        return {"schema": 1, "slug": slug, "tag": tag, "issue": 100 + TAGS.index(tag),
                "bilibili": {"asset": f"{slug}.zh-en.mp4",
                             "sha256": hashlib.sha256(self.video(tag)).hexdigest(),
                             "title_zh": f"{slug} 标题", "description_zh": "简介",
                             "tags": ["explainer"], "tid": 201}}


WORLD: World | None = None
SCHED: "Scheduler | None" = None
LOCAL = threading.local()


def run_label() -> str:
    return getattr(LOCAL, "run", "?")


class FakeSubprocess:
    """Stands in for the subprocess module inside publish_worker only."""
    CalledProcessError = subprocess.CalledProcessError
    CompletedProcess = subprocess.CompletedProcess

    @staticmethod
    def check_output(args, **kw):
        args = [str(a) for a in args]
        if args[:2] == ["gh", "api"] and args[2] == f"repos/{REPO}/releases":
            releases = []
            for tag in TAGS:
                m = WORLD.manifest(tag)
                releases.append({"tag_name": tag, "assets": [
                    {"name": "PUBLISH.json"}, {"name": m["bilibili"]["asset"]}]})
            return json.dumps(releases)
        if args[:2] == ["gh", "api"] and args[2].endswith("contents/catalog/bilibili.json"):
            reg = {"schema_version": 1, "mid": 1, "episodes": {}, "unmatched": []}
            return json.dumps({"sha": "0", "content": base64.b64encode(json.dumps(reg).encode()).decode()})
        raise AssertionError(f"unexpected check_output {args}")

    @staticmethod
    def run(args, **kw):
        args = [str(a) for a in args]
        if args[:3] == ["gh", "release", "download"]:
            tag, pattern, out = args[3], args[args.index("--pattern") + 1], args[args.index("--dir") + 1]
            m = WORLD.manifest(tag)
            body = (json.dumps(m).encode() if pattern == "PUBLISH.json"
                    else WORLD.video(tag) if pattern == m["bilibili"]["asset"] else None)
            if body is None:
                raise AssertionError(f"unexpected asset {pattern}")
            pathlib.Path(out, pattern).write_bytes(body)
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[:2] == ["biliup", "upload"]:
            video = pathlib.Path(args[2]).read_bytes()
            tag = next(t for t in TAGS if WORLD.video(t) == video)
            outcome = SCHED.pause(f"biliup upload {tag}", "upload")
            if outcome in ("ok", "ambiguous"):
                WORLD.uploads.append((tag, run_label()))
            if outcome == "ok":
                WORLD.serial += 1
                return subprocess.CompletedProcess(args, 0, f"submitted BV1{WORLD.serial:09d}\n", "")
            raise subprocess.CalledProcessError(1, args, "", "code -352 (risk control)")
        if args[:2] == ["gh", "api"] and "-X" in args:   # catalog/bilibili.json PUT
            return subprocess.CompletedProcess(args, 0, "", "")
        if args[:2] == ["gh", "issue"]:
            return subprocess.CompletedProcess(args, 0, "", "")
        raise AssertionError(f"unexpected run {args}")


class StatePath(pathlib.PosixPath):
    """state.json, with a pause before every read and write the worker makes."""

    def read_text(self, *a, **kw):
        SCHED.pause("read state.json", "read")
        return super().read_text(*a, **kw)

    def write_text(self, data, *a, **kw):
        if SCHED.pause("write state.json", "write") == "torn":
            super().write_text(data[: len(data) // 2], *a, **kw)
            raise Crash()
        return super().write_text(data, *a, **kw)


# --------------------------------------------------------------------------- the scheduler
class Scheduler:
    """Stateless depth-first search over choice sequences, replaying a prefix each time."""

    def __init__(self, scenario: Scenario, prefix: list[int]):
        self.s = scenario
        self.prefix = prefix
        self.made: list[tuple[int, int]] = []   # (choice, number of options)
        self.cv = threading.Condition()
        self.status: dict[str, str] = {}        # run -> running / paused / done
        self.pending: dict[str, tuple] = {}     # run -> (what, kind)
        self.answer: dict[str, str] = {}
        self.crashes = self.failures = 0
        self.drain = False

    # called from worker threads
    def pause(self, what: str, kind: str) -> str:
        me = run_label()
        with self.cv:
            self.pending[me] = (what, kind)
            self.status[me] = "paused"
            self.cv.notify_all()
            self.cv.wait_for(lambda: me in self.answer)
            outcome = self.answer.pop(me)
        if outcome == "crash":
            WORLD.trace.append(f"{me} dies before: {what}")
            raise Crash()
        WORLD.trace.append(f"{me} {what}" + ("" if outcome == "ok" else f" -> {outcome}"))
        return outcome

    def outcomes(self, kind: str) -> list[str]:
        if self.drain:
            return ["ok"]
        out = ["ok"]
        if kind == "upload" and self.failures < self.s.failures:
            out.append("fails")
            if self.s.ambiguous:
                out.append("ambiguous")
        if self.crashes < self.s.crashes:
            out.append("crash")
            if kind == "write":
                out.append("torn")
        return out

    def choose(self, options: list) -> int:
        i = len(self.made)
        pick = self.prefix[i] if i < len(self.prefix) else 0
        self.made.append((pick, len(options)))
        return pick

    # called from the main thread
    def start(self, name: str) -> None:
        def body():
            LOCAL.run = name
            try:
                pw.main()
                WORLD.trace.append(f"{name} finishes")
            except Crash:
                pass
            except BaseException as error:   # a bug in the worker, not an injected death
                WORLD.errors.append((name, f"{type(error).__name__}: {error}"))
                WORLD.trace.append(f"{name} stops with {type(error).__name__}: {error}")
            finally:
                with self.cv:
                    self.status[name] = "done"
                    self.cv.notify_all()
        with self.cv:
            self.status[name] = "running"
        threading.Thread(target=body, daemon=True).start()
        # Run the new worker up to its first pause before anything else moves, so the code
        # before that pause (argument parsing; a lock, if one is ever added) runs in a fixed
        # order and every replay of a choice prefix sees the same options.
        with self.cv:
            self.cv.wait_for(lambda: self.status[name] != "running")

    def step(self) -> bool:
        """Let one paused run take its step; False when every live run has finished."""
        with self.cv:
            self.cv.wait_for(lambda: all(v != "running" for v in self.status.values()))
            paused = sorted(r for r, v in self.status.items() if v == "paused")
            if not paused:
                return False
            options = [(r, o) for r in paused for o in self.outcomes(self.pending[r][1])]
            run, outcome = options[self.choose(options)]
            if outcome in ("crash", "torn"):
                self.crashes += 1
            if outcome in ("fails", "ambiguous"):
                self.failures += 1
            self.answer[run] = outcome
            self.status[run] = "running"   # before releasing the lock, so no stale re-offer
            self.cv.notify_all()
            return True


# --------------------------------------------------------------------------- one schedule
def execute(scenario: Scenario, prefix: list[int]):
    global WORLD, SCHED
    with tempfile.TemporaryDirectory(prefix="publish-explore-") as td:
        WORLD = World(state_dir=pathlib.Path(td))
        SCHED = Scheduler(scenario, prefix)
        pw.STATE_DIR = WORLD.state_dir
        pw.STATE = StatePath(WORLD.state_dir / "state.json")
        queue = [f"run{i + 1}" for i in range(scenario.runs)]
        live: list[str] = []
        while True:
            live = [r for r in live if SCHED.status.get(r) != "done"]
            while queue and len(live) < scenario.parallel:
                live.append(queue.pop(0))
                SCHED.start(live[-1])
            if SCHED.step():
                continue
            if queue:
                continue
            break
        # Drain: clean runs, one at a time, enough to publish every tag once (limit 1 per run).
        SCHED.drain = True
        WORLD.trace.append("-- clean runs from here --")
        for i in range(len(TAGS) + 1):
            SCHED.start(f"clean{i + 1}")
            while SCHED.step():
                pass
        counts = {t: sum(1 for tag, _ in WORLD.uploads if tag == t) for t in TAGS}
        verdict = {"at-most-once": all(c <= 1 for c in counts.values()),
                   "eventually": all(c >= 1 for c in counts.values())}
        return SCHED.made, verdict, list(WORLD.trace), counts, list(WORLD.errors)


def explore(scenario: Scenario):
    prefix: list[int] = []
    schedules = 0
    shortest: dict[str, tuple] = {}
    while True:
        made, verdict, trace, counts, errors = execute(scenario, prefix)
        schedules += 1
        for prop, ok in verdict.items():
            if not ok and (prop not in shortest or len(trace) < len(shortest[prop][0])):
                shortest[prop] = (trace, counts, errors)
        # backtrack to the deepest choice with an untried option
        while made and made[-1][0] + 1 >= made[-1][1]:
            made.pop()
        if not made:
            return schedules, shortest
        prefix = [c for c, _ in made[:-1]] + [made[-1][0] + 1]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("scenario", nargs="*", help="scenario names (default: all)")
    ap.add_argument("--expect", action="store_true",
                    help="pass when each verdict matches the recorded expectation (known findings fail as expected)")
    args = ap.parse_args()
    chosen = [s for s in SCENARIOS if not args.scenario or s.name in args.scenario]
    unknown = set(args.scenario) - {s.name for s in SCENARIOS}
    if unknown:
        ap.error(f"unknown scenario(s): {', '.join(sorted(unknown))}")
    sys.argv = ARGV
    pw.subprocess = FakeSubprocess
    drift = violated = False
    for scenario in chosen:
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            schedules, shortest = explore(scenario)
        print(f"== {scenario.name}: {scenario.about}")
        print(f"   {schedules} schedules explored")
        for prop in ("at-most-once", "eventually"):
            holds = prop not in shortest
            expected = scenario.expect[prop]
            mark = "holds" if holds else "VIOLATED"
            note = "" if holds == expected else "   <-- differs from the recorded expectation"
            drift |= holds != expected
            violated |= not holds
            print(f"   {prop:13} {mark}{note}")
            if not holds:
                trace, counts, errors = shortest[prop]
                print("     shortest counterexample:")
                for i, line in enumerate(trace, 1):
                    print(f"       {i:2}. {line}")
                print("     uploads per tag: " + ", ".join(f"{t}={c}" for t, c in counts.items()))
        print()
    if args.expect:
        print("verdicts match the recorded expectations" if not drift else
              "VERDICTS DRIFTED from the recorded expectations (see '<--' above)")
        return 1 if drift else 0
    return 1 if violated else 0


if __name__ == "__main__":
    raise SystemExit(main())
