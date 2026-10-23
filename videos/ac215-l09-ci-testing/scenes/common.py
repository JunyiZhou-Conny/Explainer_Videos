"""Shared scene code for AC215 L9 (CI & unit testing: who gets to say no before a commit?).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example, the six trackers A-F, loaders for the real captures in assets/, terminal helpers, tags,
and the video's set pieces V1-V7.  The scene authors' contract is build/SCENE-NOTES.md; the
reference scene is s01_hook.py.

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == n   # one `with self.voiceover(SAY[i]) as vo:` each

Every text here is >= 20 pt.  Never .scale() a group that holds text below 1.0; set pieces take
size parameters instead (arch_w, cell, bar_w ...).  Never set width/height/color/depth on a VGroup
subclass (Manim properties): these classes use arch_w, slab_h, col_w ...
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, UL, UP, UR, AnimationGroup, Arc, Arrow,
                   Brace, Circle, Create, DashedVMobject, Dot, FadeIn, FadeOut, FadeTransform,
                   Indicate, LaggedStart, Line, MoveAlongPath, Polygon, Rectangle, ReplacementTransform,
                   Rotate, RoundedRectangle, Square, Succession, Text, Transform, VGroup, VMobject,
                   Wiggle, linear)

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon, ponder_card  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, ReadmeTracker,  # noqa: F401
                              Terminal, box, cell_width, check_mark, chip, code_block, code_panel,
                              code_span, cross_mark, file_glyph, file_tree, folder_glyph, glyph_range,
                              label, laptop, lecture_ref, line_bar, line_pitch, mono, mono_line,
                              server, step_badge, substring, tag, warning_sign)
from explainer.script import load_narration

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
TERMINAL = ASSETS / "terminal"
SOURCE = ASSETS / "source"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # the clone, working tree, staging area, host shell
CLOUD = S.BLUE           # GitHub, the CI runner (dashed), the Hugging Face Hub
IMAGE = S.TEAL           # images, containers, baked-in code slabs
SYSTEM = S.ORANGE        # host-owned: host pip installs, the host PATH
HOST = SYSTEM
VENV = S.GREEN           # project-owned, hermetic: uv venv, uv.lock, the hermetic border, passing
HERMETIC = VENV
PASS = VENV
TOOL = S.PURPLE          # pytest, black, flake8, pre-commit, uv, just, ruff, ty, hypothesis, docker
ERR = S.RED              # failing tests, F401/E231/E303/E501, wrong mask cells, Failed, refusals
TURN = S.YELLOW          # your turn, the tracker, the gate-table row being filled now
MODIFIED = TURN          # black's "files were modified" (the amber flash; script: YELLOW)
COST = S.GOLD            # unused on screen this lecture (nothing billable)
ROUTE = S.PINK           # the request token's path, the wire to port 9000, push to GitHub
FUTURE = S.GREY          # CI / L21, L10 credentials: GREY, dashed
SKIP = S.GREY            # skipped / deselected tests: GREY, dashed, never GREEN
INK = S.WHITE
DIMMED = S.GREY
# test kinds are coloured by what runs (episode-local, BRIEF.md)
UNIT = VENV              # one function, fully ours
INTEG = IMAGE            # our parts in-process (TestClient / the tiny model)
SYSTEM_TEST = CLOUD      # the real thing over the network
KIND = {"unit": UNIT, "integration": INTEG, "system": SYSTEM_TEST}
STATE = {"idle": S.GREY, "pass": PASS, "fail": ERR, "modified": MODIFIED, "skip": SKIP}

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TRACK_BOTTOM = 2.9           # the tracker's lowest point
BOTTOM = -3.5                # a terminal's bottom edge (kept when it grows or shrinks)


def strip_top(rows: int = 3, size: float = 22) -> float:
    """Top edge of a `rows`-row terminal standing on BOTTOM."""
    return BOTTOM + rows * line_pitch(size) + 0.85


STRIP_TOP = strip_top(3)     # -1.44: a picture over a 3-row strip lives in y in [-1.3, 2.8]


def steady(s: str, size: float = 20, color=INK, mono_font: bool = False, **kw) -> Text:
    """Text with a fixed vertical extent (an invisible '|' strut), so that a Transform between two
    steady texts keeps the size the check tool computes. Use it for anything that morphs (counters,
    captions, tile values)."""
    t = (mono if mono_font else label)("|" + s, size, color, **kw)
    pipe = t[0]
    if len(t) > 1:
        pipe.move_to([t[1].get_center()[0], pipe.get_center()[1], 0])
    pipe.set_opacity(0)
    return t


def note(s: str, color=S.GREY, size: float = 20, **kw) -> Text:
    """A caption line (label font, GREY by default)."""
    return label(s, size, color, **kw)


# ------------------------------------------------------------------ running example
USER = "student"
P_LAPTOP_HOME = "student@laptop:~$"
P_LAPTOP = "student@laptop:~/cheese-app-ci-cd$"
P_BABYKEV_HOME = P_LAPTOP_HOME
P_BABYKEV = "student@laptop:~/babykev$"
T_LAPTOP = "laptop"
T_BABYKEV = "laptop · babykev"
REQUEST = "GET /euclidean_distance/?x=3&y=4"
RESPONSE = '{"distance": 5.0}'
APP_CHAIN = ("routing", "validation", "handler", "power()")


def readme(n: int) -> str:
    """cheese-app-ci-cd/README.md line n (1-based), stripped: assert cap.cmd == readme(106)."""
    return excerpt("cheese-app-ci-cd/README.md", n, n).strip()


def walk(n: int) -> str:
    """babykev-walk/walk.md line n, stripped."""
    return excerpt("babykev-walk/walk.md", n, n).strip()


# ------------------------------------------------------------------ trackers (BRIEF.md, six)
SECTIONS = {
    "A": ("README", "Part 1: Understanding the Codebase"),
    "B": ("README", "Part 2: Identifying Code Quality Issues"),
    "C": ("README", "Part 3: Testing with Pytest"),
    "D": ("README", "Part 4: Automating with Pre-commit Hooks"),
    "E": ("guest lecture", "babykev walk, steps 00–05b"),
    "F": ("README", "Docker Cleanup"),
}
STEPS = {
    "A": ["Clone", "docker-shell", "Start server", "Browser checks", "Exit"],
    "B": ["Build image", "flake8 (Option A)", "black --check (Option A)", "pip install (Option B)",
          "flake8 local", "black local"],
    "C": ["Build", "Unit tests", "Integration tests", "Both", "Coverage", "Start server (Opt 2)",
          "System tests", "Clean up", "Interactive shell (Opt 3)", "Tests inside"],
    "D": ["Install pre-commit", "pre-commit install", "git commit", "run --all-files", "pre-commit run"],
    "E": ["step-00 env", "step-01 tests", "step-02 format+lint", "step-03 the hook",
          "step-04/04b docs", "step-05 the model", "step-05a properties", "step-05b marker+images"],
    "F": ["container ls", "system prune", "image ls"],
}


def place_tracker(tr: ReadmeTracker) -> ReadmeTracker:
    """Pin a tracker to the house corner (left edge -6.5, top 3.5)."""
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def _caption(tr: ReadmeTracker, k: int, extra: bool) -> Text:
    if not k:
        return steady("", tr.size, tr.hi_color).next_to(tr.dots, RIGHT, buff=0.25)
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    if extra:
        t = steady(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY})
    else:
        t = steady(s, tr.size, tr.hi_color)
    return t.next_to(tr.dots, RIGHT, buff=0.25)


def tracker(key: str, step: int | None = None, extra: bool = False) -> ReadmeTracker:
    """Tracker `key` ("A".."F") at `step` (1-based; None = no step lit yet), placed top-left.
    E's head reads 'guest lecture › babykev walk, steps 00–05b' (script S10)."""
    prefix, section = SECTIONS[key]
    tr = ReadmeTracker(section, STEPS[key])
    if prefix != "README":
        old = tr.head[0]
        new = label(prefix, tr.size, S.GREY).move_to(old, aligned_edge=LEFT)
        dx = new.width - old.width
        tr.head.remove(old)
        tr.head.submobjects.insert(0, new)
        for m in tr.head[1:]:
            m.shift(RIGHT * dx)
    if step:
        tr.set_step(step)
    tr.remove(tr.caption)
    tr.caption = _caption(tr, step or 0, extra)
    tr.add(tr.caption)
    tr.key = key
    return place_tracker(tr)


def tracker_a(step=None, extra=False): return tracker("A", step, extra)   # noqa: E704
def tracker_b(step=None, extra=False): return tracker("B", step, extra)   # noqa: E704
def tracker_c(step=None, extra=False): return tracker("C", step, extra)   # noqa: E704
def tracker_d(step=None, extra=False): return tracker("D", step, extra)   # noqa: E704
def tracker_e(step=None, extra=False): return tracker("E", step, extra)   # noqa: E704
def tracker_f(step=None, extra=False): return tracker("F", step, extra)   # noqa: E704


def track(tr: ReadmeTracker, k: int | None = None, extra: bool = False, run_time: float = 0.5):
    """Animation: move the tracker to step k (None: stay) and set/clear the ' · extra' caption.
    Use this, never tr.goto() (its caption morph reads as < 20 pt in the check)."""
    k = tr.k if k is None else k
    anims = []
    if k != tr.k:
        for i, d in enumerate(tr.dots, start=1):
            col = tr.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK)
            anims.append(d.animate.set_color(col).scale((1.5 if i == k else 1.0) / (d.width / 0.12)))
    anims.append(Transform(tr.caption, _caption(tr, k, extra)))
    tr.k = k
    return AnimationGroup(*anims, run_time=run_time)


def swap_tracker(scene, old: ReadmeTracker, new: ReadmeTracker, *anims, run_time: float = 0.6):
    """Tracker `old` becomes `new` in place (the section name and caption cross-fade, the dots
    regroup). `new` ends on the scene as one piece; `old` is gone."""
    same = old.head[0].text == new.head[0].text if hasattr(old.head[0], "text") else False
    keep = VGroup(old.head[0], old.head[1]) if same else VGroup()
    scene.remove(old)
    scene.add(*keep, *old.head[0 if not same else 2:], old.dots, old.caption)
    moves = [FadeTransform(old.head[2], new.head[2]), ReplacementTransform(old.dots, new.dots),
             FadeTransform(old.caption, new.caption)]
    if not same:
        moves += [FadeTransform(old.head[0], new.head[0]), FadeTransform(old.head[1], new.head[1])]
    scene.play(*moves, *anims, run_time=run_time)
    scene.remove(*keep, *new.head, new.dots, new.caption)
    scene.add(new)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 9 · slides 41, 98–99' tag, top right (one per scene, BRIEF)."""
    return lecture_ref(9, slides)


# ------------------------------------------------------------------ captures
LAPTOP_DIR, BABYKEV_DIR = "laptop", "babykev"
# file lines never to print (capture-only, ASSETS.md): checked by Capture.line()
NEVER = {("laptop", "clean-03-image-ls.txt"): {5}}

_PROMPT_RE = re.compile(r"^((?:\([^)]*\) )?[\w.-]+@[\w.-]+:[^#$\s]*[#$])(?: (.*))?$")


def split_prompt(s: str) -> tuple[str, str]:
    """'app@44b7ce455073:/app$ uvicorn …' -> ('app@44b7ce455073:/app$', 'uvicorn …').
    A line without a prompt -> ('', s)."""
    m = _PROMPT_RE.match(s)
    if not m:
        return "", s
    return m.group(1), m.group(2) or ""


class Capture:
    """One captured command (assets/terminal/<folder>/<file>). .cmd (as typed) .lines (output body,
    no [exit N]) .exit .raw (every file line, tabs expanded to 8) .path"""

    def __init__(self, cmd, lines, exit_code, raw, path, never=()):
        self.cmd, self.lines, self.exit, self.raw, self.path = cmd, lines, exit_code, raw, path
        self.never = set(never)

    def line(self, n: int) -> str:
        """File line n (1-based; line 1 is the '$ …' command, never printed)."""
        if not 1 <= n <= len(self.raw):
            raise IndexError(f"{self.path.name} has {len(self.raw)} lines, not {n}")
        if n in self.never:
            raise ValueError(f"{self.path.name}:{n} is capture-only and is never shown (ASSETS.md)")
        if re.fullmatch(r"\[exit -?\d+\]", self.raw[n - 1]):
            raise ValueError(f"{self.path.name}:{n} is the [exit N] line: never printed")
        return self.raw[n - 1]

    def at(self, *spec) -> list[str]:
        """Lines by FILE line numbers, as script.md writes them: ints, (a, b) inclusive ranges and
        '…' items (a literal '…' line). at(2, (5, 7), '…', 33). Never adds '…' by itself."""
        out: list[str] = []
        for r in spec:
            if isinstance(r, str):
                out.append(r)
                continue
            a, b = (r, r) if isinstance(r, int) else r
            if a < 2:
                raise ValueError("file line 1 is the '$ …' command; it is never printed")
            out += [self.line(n) for n in range(a, b + 1)]
        return out

    def pick(self, *ranges, ellipsis: str = "…") -> list[str]:
        """L1's picker: output BODY lines by 1-based ranges (pick index = file line - 1), adding '…'
        between ranges that skip lines. Prefer .at() with script.md's file line numbers."""
        n = len(self.lines)
        out, last = [], None
        for r in ranges:
            a, b = (r, r) if isinstance(r, int) else r
            a = a if a > 0 else n + a + 1
            b = b if b > 0 else n + b + 1
            if last is not None and a > last + 1:
                out.append(ellipsis)
            for k in range(a, b + 1):
                out.append(self.line(k + 1))
            last = b
        return out

    def istep(self, n: int) -> tuple[str, str]:
        """File line n split into (prompt, typed) (the istep captures part1-01, part3-opt3-01)."""
        return split_prompt(self.line(n))


def capture(name: str, folder: str | None = None) -> Capture:
    """capture("part4-07") (laptop), capture("s05a-08", BABYKEV_DIR), capture("babykev/07").
    name = 'NN-…' prefix, full stem, or file name; a prefix must match exactly one file.
    Fails loudly when missing: never show an output that wasn't captured."""
    if folder is None:
        folder, name = name.split("/", 1) if "/" in name else (LAPTOP_DIR, name)
    if folder == "capture-only" or name.startswith("capture-only"):
        raise ValueError("capture-only/ is plumbing: never shown")
    d = TERMINAL / folder
    stem = name[:-4] if name.endswith(".txt") else name
    p = d / f"{stem}.txt"
    if not p.exists():
        hits = sorted(d.glob(f"{stem}-*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"capture {folder}/{name}: {len(hits)} matches "
                                    f"{[h.name for h in hits]} (see ASSETS.md)")
        p = hits[0]
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    raw = [s.rstrip("\r").expandtabs(8) for s in text.rstrip("\n").split("\n")]
    cmd = raw[0][2:] if raw[0].startswith("$ ") else ""
    body = raw[1:]
    code = 0
    if body and re.fullmatch(r"\[exit -?\d+\]", body[-1]):
        code = int(body[-1][6:-1])
        body = body[:-1]
    return Capture(cmd, body, code, raw, p, NEVER.get((folder, p.name), ()))


# ---- line transforms (script.md conventions)
def hash12(s: str) -> str:
    """Every long sha256 shortened to its first 12 hex digits + '…'."""
    return re.sub(r"(sha256:[0-9a-f]{12})[0-9a-f]{13,}", r"\1…", s)


def cut(s: str, after: str, ellipsis: str = "…") -> str:
    """The line cut right after `after` (first occurrence), ending in '…'."""
    i = s.index(after) + len(after)
    return s[:i] + ellipsis


def ask(s: str, bracket: str = "[y/N]") -> str:
    """A question line cut right after its bracket (the answer is typed separately)."""
    return s[:s.index(bracket) + len(bracket)]


def _table(lines):
    head = lines[0].rstrip()
    starts = [0] + [m.end() for m in re.finditer(r"\s{2,}", head)]
    ends = starts[1:] + [None]
    names = [head[a:b].strip() if b else head[a:].strip() for a, b in zip(starts, ends)]
    rows = [[(ln[a:b] if b else ln[a:]).strip() for a, b in zip(starts, ends)] for ln in lines]
    right = []
    for j, (a, b) in enumerate(zip(starts, ends)):
        hend = a + len(names[j])
        data = [ln for ln in lines[1:] if (ln[a:b] if b else ln[a:]).strip()]
        right.append(bool(data) and all(len(ln[:b].rstrip() if b else ln.rstrip()) == hend for ln in data))
    return names, rows, right


def _align(rows, right, gutter=2):
    w = [max(len(r[j]) for r in rows) for j in range(len(rows[0]))]
    return [(" " * gutter).join((c.rjust(w[j]) if right[j] else c.ljust(w[j]))
                                for j, c in enumerate(r)).rstrip() for r in rows]


def squeeze(lines: list[str], gutter: int = 2) -> list[str]:
    """A docker table re-aligned with two-space gutters; columns empty in every row are dropped."""
    names, rows, right = _table(lines)
    keep = list(range(len(names)))
    if len(rows) > 1:
        keep = [j for j in keep if any(r[j] for r in rows[1:])]
    return _align([[r[j] for j in keep] for r in rows], [right[j] for j in keep], gutter)


def cols(lines: list[str], names: list[str], gutter: int = 2) -> list[str]:
    """Only the named columns of a docker table (header row first), re-aligned."""
    heads, rows, right = _table(lines)
    idx = [heads.index(n) for n in names]
    return _align([[r[j] for j in idx] for r in rows], [right[j] for j in idx], gutter)


# ------------------------------------------------------------------ sources
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".ini": "ini", ".txt": "text", ".json": "json"}


def source_text(path: str) -> str:
    return (SOURCE / path).read_text(encoding="utf-8")


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of assets/source/<path>."""
    return "\n".join(source_text(path).split("\n")[first - 1:last])


def shown_path(path: str) -> str:
    """The header name of a source file: repo-relative for the two clones; '<sha> · <file>' for
    cheese-app-ci-cd-history/<sha>-<file>; 'step-05 · model.py' for babykev-history; walk.md."""
    top, _, rest = path.partition("/")
    if top in ("cheese-app-ci-cd", "babykev", "babykev-walk"):
        return rest
    if top == "cheese-app-ci-cd-history":
        m = re.match(r"([0-9a-f]{7})-(.+)$", rest)
        return f"{m.group(1)} · {m.group(2)}" if m else rest
    if top == "babykev-history":
        m = re.match(r"(step-\d+[a-z]?)-(.+)$", rest)
        return f"{m.group(1)} · {m.group(2)}" if m else rest
    return path


def code(path: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, shown: str | None = None):
    """CODE(path: first–last) of script.md: a code_panel quoting assets/source/<path>, header
    '<shown> · lines a–b' (shown_path()). ≤ 12 lines. At 22 pt a 65-char line is ~12.3 wide (the
    frame's limit); use font_size=20 up to 72 chars. .code .header; code_span(p.code, k, "x"),
    line_bar(p.code, k, colour) with k = file line - first."""
    last = first if last is None else last
    if last - first + 1 > 12:
        raise ValueError(f"CODE {path}: {last - first + 1} lines; never more than 12 on screen")
    name = Path(path).name
    if language is None:
        language = ("docker" if name.startswith("Dockerfile") else
                    "make" if name == "justfile" else _LANG.get(Path(name).suffix, "text"))
    return code_panel(excerpt(path, first, last), shown or shown_path(path), first, language,
                      focus=focus, font_size=font_size)


def readme_card(lines, body, quote: bool = False, card_w: float | None = None, size: float = 22,
                file: str = "README.md") -> VGroup:
    """A GREY README card: header 'README.md · line n' (or 'lines a–b' for a tuple) and the README's
    own words (str: '\\n' separates lines, label font; or any mobject). .frame .head .body"""
    where = f"line {lines}" if isinstance(lines, int) else f"lines {lines[0]}–{lines[1]}"
    head = VGroup(mono(file, CAPTION, S.GREY), label(f"· {where}", CAPTION, S.GREY)).arrange(RIGHT, buff=0.12)
    if isinstance(body, str):
        body = VGroup(*[label(s, size, INK) for s in body.split("\n")]).arrange(DOWN, aligned_edge=LEFT,
                                                                               buff=0.12)
    content = body
    if quote:
        bar = Line(body.get_corner(UL) + np.array([-0.22, 0.04, 0]),
                   body.get_corner(DL) + np.array([-0.22, -0.04, 0]), color=S.GREY, stroke_width=4)
        content = VGroup(bar, body)
    inner = VGroup(head, content).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    frame = box(card_w or inner.width + 0.55, inner.height + 0.4, S.GREY, fill=S.GREY_DARKER,
                fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.28)
    g = VGroup(frame, inner)
    g.frame, g.head, g.body = frame, head, body
    return g


# ------------------------------------------------------------------ terminals
def term(prompt: str = P_LAPTOP, rows: int = 10, title: str | None = T_LAPTOP, width: float = 12.6,
         size: float = 22, place: bool = True) -> Terminal:
    """The house terminal: 12.6 wide, 22 pt, 65 characters a row, centred, bottom edge at BOTTOM.
    Height = rows x 0.403 + 0.85. Full width, or a 3-row strip (rows=3) under a picture."""
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)
    if place:
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def laptop_term(rows: int = 10, prompt: str = P_LAPTOP) -> Terminal:
    return term(prompt, rows, T_LAPTOP)


def babykev_term(rows: int = 10, prompt: str = P_BABYKEV) -> Terminal:
    return term(prompt, rows, T_BABYKEV)


def resize(scene, t: Terminal, rows: int, keep=None, extra=(), run_time: float = 0.8) -> Terminal:
    """Grow or shrink terminal `t` to `rows` (bottom edge kept). It keeps its last lines (at most
    `keep`), or exactly the line mobjects in `keep` (a list). `extra`: animations at the same time."""
    title = t.title.text if t.title is not None else None
    ref = Terminal(prompt=t.prompt, width=t.box.width, rows=rows, size=t.size, title=title)
    ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                        t.box.get_bottom()[1] - ref.box.get_bottom()[1], 0]))
    if isinstance(keep, (list, tuple)):
        assert len(keep) <= rows
        kept = [ln for ln in t.lines.submobjects if ln in keep]
    else:
        n_keep = min(len(t.lines), rows, len(t.lines) if keep is None else keep)
        kept = t.lines.submobjects[len(t.lines) - n_keep:]
    gone = [ln for ln in t.lines.submobjects if ln not in kept]
    if gone:
        scene.play(FadeOut(VGroup(*gone)), run_time=0.25)
        for ln in gone:
            t.lines.remove(ln)
            scene.remove(ln)
    anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar), t.dots.animate.move_to(ref.dots)]
    if t.title is not None:
        anims.append(t.title.animate.move_to(ref.title))
    for i, ln in enumerate(kept):
        anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
    scene.play(*anims, *extra, run_time=run_time)
    t.rows = rows
    return t


def bare_prompt(scene, t: Terminal):
    """The prompt returns (no output): a prompt line with nothing typed yet."""
    ln = t.type(scene, "", type_time=0)
    ln.bare = True
    return ln


def type_cmd(scene, t: Terminal, cmd: str, type_time: float | None = None):
    """Type at the waiting prompt (replacing a bare prompt line if there is one). Long commands
    fold at a space with ' \\' (Terminal.fold). Returns the line, or a VGroup with .rows."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    return t.type(scene, cmd, type_time)


def istep(scene, t: Terminal, line: str, type_time: float | None = None):
    """A typed line at a container prompt, from its capture ('app@44b7ce455073:/app$ uvicorn …'):
    set the terminal's prompt to the capture's own, then type the rest."""
    prompt, typed = split_prompt(line)
    if prompt:
        t.set_prompt(prompt)
    return type_cmd(scene, t, typed, type_time)


def cd_prompt(scene, t: Terminal, new_prompt: str, color=LAPTOP, run_time: float = 0.6):
    """After `cd`: the prompt changes; a bare prompt line appears and its path flashes."""
    t.set_prompt(new_prompt)
    ln = bare_prompt(scene, t)
    path = new_prompt.split(":", 1)[1].rstrip("$# ")
    scene.play(Indicate(substring(ln, path), color=color, scale_factor=1.08), run_time=run_time)
    scene.add(ln)
    return ln


def _row_of(line):
    """A terminal line, or the last row of a folded command."""
    return line.rows[-1] if hasattr(line, "rows") else line


def beside(mob, line, buff: float = 0.45, min_x: float | None = None):
    """Put `mob` right of terminal row `line` (a folded command: its last row), centred on it."""
    row = _row_of(line)
    x = row.strut.get_right()[0] + buff
    if min_x is not None:
        x = max(x, min_x)
    return mob.move_to([x + mob.width / 2, row.strut.get_center()[1], 0])


def covers_text(mob, line) -> bool:
    """True when `mob` (a tag, a chip) would hide glyphs of terminal row `line`."""
    hides = any(type(m).__name__ in ("Text", "MarkupText", "Paragraph")
                or (isinstance(m, Rectangle) and m.get_fill_opacity() > 0.3) for m in mob.get_family())
    g = getattr(_row_of(line), "glyphs", None)
    if not hides or g is None or not len(g):
        return False
    l, r, b, tp = mob.get_left()[0], mob.get_right()[0], mob.get_bottom()[1], mob.get_top()[1]
    return any(l < ch.get_right()[0] + 0.03 and r > ch.get_left()[0] - 0.03
               and b < ch.get_top()[1] and tp > ch.get_bottom()[1]
               for ch in g.family_members_with_points())


def attach(scene, line, mob):
    """Make `mob` part of terminal row `line` (it scrolls and fades with it)."""
    row = _row_of(line)
    scene.remove(mob)
    row.add(mob)
    scene.add(row)
    return mob


def pin(scene, line, mob, run_time: float = 0.4, anim=None):
    """Show `mob` (placed with beside()) and make it part of the row, so it scrolls with it.
    Refuses a tag that would cover the row's text."""
    row = _row_of(line)
    if covers_text(mob, row):
        raise ValueError(f"pin(): this {mob.width:.2f}-wide tag would cover the text of its row; "
                         "use a row_tag, put it on an output row, or under the terminal")
    scene.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
    return attach(scene, row, mob)


def unpin(scene, line, mob, *extra, run_time: float = 0.3):
    """Fade a pinned mark out and take it off its row (so it never snaps back)."""
    row = _row_of(line)
    scene.play(FadeOut(mob), *extra, run_time=run_time)
    if mob in row.submobjects:
        row.remove(mob)
    scene.remove(mob)


def row_tag(parts, color=S.GREY, size: float = 20) -> VGroup:
    """A tag that fits inside one 22 pt terminal row (0.36 tall; the house tag is taller).
    parts: a string, or (text, 'mono'|'label') pairs. .box .text"""
    if isinstance(parts, str):
        parts = [(parts, "label")]
    t = VGroup(*[mono(x, size, color) if k == "mono" else label(x, size, color) for x, k in parts])
    t.arrange(RIGHT, buff=0.12)
    h = 0.36
    b = RoundedRectangle(width=t.width + 0.34, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def turn_row() -> VGroup:
    """'▶ your turn' sized for a terminal row (YELLOW): beside(turn_row(), line); pin(...)."""
    return row_tag("▶ your turn", TURN)


def extra_row() -> VGroup:
    """'extra' sized for a terminal row (GREY)."""
    return row_tag("extra", S.GREY)


def time_row() -> VGroup:
    """'at the time of recording' sized for a terminal row (GREY)."""
    return row_tag("at the time of recording", S.GREY)


def under(g, color, stroke: float = 4, pad: float = 0.03, y: float | None = None) -> Line:
    """A line under glyphs `g`."""
    y = g.get_bottom()[1] - 0.06 if y is None else y
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def hl_bar(g, color=TURN, opacity: float = 0.25, buff: float = 0.05) -> Rectangle:
    """A translucent bar behind glyphs `g` (scene.add_to_back it, or bring the glyphs forward)."""
    return Rectangle(width=g.width + 2 * buff, height=g.height + 2 * buff, stroke_width=0) \
        .set_fill(color, opacity).move_to(g)


def ring(g, color=TURN, buff: float = 0.08, stroke: float = 3) -> RoundedRectangle:
    """An outline box around `g` (hides nothing: fine over terminal text)."""
    return RoundedRectangle(width=g.width + 2 * buff, height=g.height + 2 * buff,
                            corner_radius=0.08, stroke_color=color, stroke_width=stroke).move_to(g)


def strike(g, color=ERR, stroke: float = 4) -> Line:
    """A strike-through line over `g`."""
    return Line(g.get_left() + LEFT * 0.06, g.get_right() + RIGHT * 0.06, color=color, stroke_width=stroke)


# ------------------------------------------------------------------ tags and chips (>= 20 pt)
def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag (house size: beside a card, not inside a terminal row)."""
    return tag("▶ your turn", TURN)


def extra_tag() -> VGroup:
    return tag("extra", S.GREY)


def illustration_tag(s: str = "illustration") -> VGroup:
    return tag(s, S.GREY)


def recorded_tag(s: str = "recorded · walk.md") -> VGroup:
    """On every number that comes from the walk's own record, not a capture."""
    return tag(s, S.GREY)


def recording_tag(s: str = "at the time of recording") -> VGroup:
    """Beside versions, warning counts, timings and reclaimed sizes when first shown."""
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    return tag(s, S.GREY)


def expected_tag() -> VGroup:
    """Not needed this episode (no expected panels); kept for the series vocabulary."""
    return tag("expected output", S.GREY)


def preview_tag(s: str = "preview") -> VGroup:
    return tag(s, S.GREY)


def grey_chip(s: str, size: float = 20, mono_font: bool = False, color=S.GREY) -> VGroup:
    """A GREY chip for a short note ("committed live, in class"). .box .text"""
    return chip(s, color, size=size, font=MONO if mono_font else None)


def dashed_chip(s: str, color=FUTURE, size: float = 20, mono_font: bool = False) -> VGroup:
    """A dashed chip: future things (CI, L21) and things never matched/skipped. .box .text"""
    t = mono(s, size, color) if mono_font else label(s, size, color)
    ob = outline_box(t.width + 0.48, mono("|", size).height + 0.24, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def tool_chip(s: str, size: float = 20) -> VGroup:
    """A tool as a PURPLE mono chip (never a logo): pytest, black, pre-commit, just …"""
    return chip(s, TOOL, size=size, font=MONO)


def finding_chip(code_: str, text: str, size: float = 20) -> VGroup:
    """A RED lint finding: mono code + its words, e.g. finding_chip("F401", "'os' imported but
    unused"). .box .code .text"""
    c = mono(code_, size, ERR)
    t = label(text, size, INK)
    row = VGroup(c, t).arrange(RIGHT, buff=0.2)
    b = box(row.width + 0.45, row.height + 0.3, ERR, fill_opacity=0.12, radius=0.12)
    row.move_to(b)
    g = VGroup(b, row)
    g.box, g.code, g.text = b, c, t
    return g


def file_card(path: str, color=LAPTOP, size: float = 20, dashed: bool = False) -> VGroup:
    """A file as a card: file glyph + mono path (.git/hooks/pre-commit, .pre-commit-config.yaml).
    .box .glyph .text"""
    g0 = file_glyph(0.34, color)
    t = mono(path, size, INK)
    row = VGroup(g0, t).arrange(RIGHT, buff=0.16)
    w, h = row.width + 0.45, row.height + 0.32
    b = outline_box(w, h, color, solid=not dashed, fill_opacity=0.1)
    row.move_to(b)
    g = VGroup(b, row)
    g.box, g.glyph, g.text = b, g0, t
    return g


# ------------------------------------------------------------------ small glyphs and motion
def outline_box(box_w: float, box_h: float, color, solid: bool = False, fill_opacity: float = 0.1,
                radius: float = 0.14, stroke: float = 2.5) -> VGroup:
    """A box whose outline is made of dashes: dashed (solid=False) or closed (solid=True, faint
    fill). A dashed one Transforms cleanly into a solid one of the same size. .fill .frame"""
    r = RoundedRectangle(width=box_w, height=box_h, corner_radius=min(radius, box_h / 2, box_w / 2))
    n = max(12, int((box_w + box_h) * 7))
    frame = DashedVMobject(r.copy(), num_dashes=n, dashed_ratio=0.999 if solid else 0.55)
    frame.set_stroke(color, stroke)
    fill = r.copy().set_stroke(width=0).set_fill(color, fill_opacity if solid else 0)
    g = VGroup(fill, frame)
    g.fill, g.frame = fill, frame
    return g


def arrow(a, b, color=S.GREY, stroke: float = 3, buff: float = 0.12) -> Arrow:
    """A plain thin arrow between two mobjects or points."""
    pa = a if isinstance(a, np.ndarray) else a.get_center()
    pb = b if isinstance(b, np.ndarray) else b.get_center()
    return Arrow(pa, pb, buff=buff if not isinstance(a, np.ndarray) else 0, color=color,
                 stroke_width=stroke, tip_length=0.18, max_tip_length_to_length_ratio=0.25)


def route(a, b, arc: float = 0.0, color=ROUTE, stroke: float = 4) -> Arrow:
    """A PINK route arrow (curved by `arc` radians) from a to b (points or mobjects)."""
    pa = a if isinstance(a, np.ndarray) else a.get_center()
    pb = b if isinstance(b, np.ndarray) else b.get_center()
    return Arrow(pa, pb, buff=0.15 if not isinstance(a, np.ndarray) else 0, path_arc=arc, color=color,
                 stroke_width=stroke, tip_length=0.2, max_tip_length_to_length_ratio=0.2)


def travel(mob, path, run_time: float = 1.2):
    """Animation: `mob` rides along `path` (a Line/Arrow/VMobject)."""
    return MoveAlongPath(mob, path, run_time=run_time)


def bounce(mob, point, run_time: float = 0.9):
    """Animation: `mob` goes to `point` and comes back."""
    back = mob.get_center().copy()
    return Succession(mob.animate(run_time=run_time * 0.5).move_to(point),
                      mob.animate(run_time=run_time * 0.5).move_to(back))


def lock_glyph(lock_h: float = 0.32, color=VENV) -> VGroup:
    """A padlock (uv.lock, --locked)."""
    w = lock_h * 0.8
    body = RoundedRectangle(width=w, height=lock_h * 0.6, corner_radius=lock_h * 0.08,
                            stroke_color=color, stroke_width=2.5).set_fill(color, 0.3)
    shackle = Arc(radius=w * 0.32, start_angle=0, angle=PI, color=color, stroke_width=3)
    shackle.next_to(body, UP, buff=0)
    return VGroup(shackle, body)


# ================================================================== V1 · the gate and the vault
def _arch_path(arch_w: float, arch_h: float) -> VMobject:
    r = arch_w / 2
    p = VMobject()
    p.set_points_as_corners([[-r, 0, 0], [-r, arch_h - r, 0]])
    p.append_points(Arc(radius=r, start_angle=PI, angle=-PI, arc_center=[0, arch_h - r, 0]).points)
    p.append_points(Line([r, arch_h - r, 0], [r, 0, 0]).points)
    return p


class Arch(VGroup):
    """One scanner arch of a turnstile (one hook / one check): an inverted U with a lamp on top
    and a faint scanning beam. States: idle GREY, pass GREEN, fail RED, modified YELLOW (black's
    "files were modified"), skip GREY dashed ("(no files to check)Skipped").
        .frame (18 dashes) .lamp .beam .state ; .to(state) -> Animation"""

    N = 18

    def __init__(self, arch_w: float = 0.7, arch_h: float = 1.5, state: str = "idle",
                 stroke: float = 5, **kw):
        super().__init__(**kw)
        self.arch_w, self.arch_h, self.stroke = arch_w, arch_h, stroke
        self.frame = self._frame(state)
        self.lamp = Dot([0, arch_h + 0.02, 0], radius=0.07, color=STATE[state])
        self.beam = Line([-arch_w / 2 + 0.08, arch_h * 0.45, 0], [arch_w / 2 - 0.08, arch_h * 0.45, 0],
                         stroke_width=2, color=STATE[state], stroke_opacity=0.35)
        self.state = state
        self.add(self.beam, self.frame, self.lamp)

    def _frame(self, state: str) -> DashedVMobject:
        f = DashedVMobject(_arch_path(self.arch_w, self.arch_h), num_dashes=self.N,
                           dashed_ratio=0.55 if state == "skip" else 0.999)
        f.set_stroke(STATE[state], self.stroke)
        f.move_to(self.frame if hasattr(self, "frame") else f)
        return f

    def to(self, state: str, run_time: float = 0.3):
        """Animation: the arch takes `state` (frame colour/dashes, lamp, beam)."""
        new = self._frame(state)
        new.move_to(self.frame)
        self.state = state
        col = STATE[state]
        return AnimationGroup(Transform(self.frame, new), self.lamp.animate.set_color(col),
                              self.beam.animate.set_stroke(col, opacity=0.6 if state != "idle" else 0.35),
                              run_time=run_time)


class Turnstile(VGroup):
    """V1/V5 · a row of n scanner arches (the hooks / checks a commit must pass).
        ts = Turnstile(9, CHEESE_HOOKS)          # names are built, not added: ts.labels
        self.play(LaggedStart(*[FadeIn(l) for l in ts.labels], lag_ratio=0.15))
        self.play(ts.mark(7, "modified"))        # black's arch; ts.mark_all(["pass"] * 9)
    Labels alternate below / above the arches (20 pt); keep names <= 14 characters.
    .arches .labels .floor"""

    def __init__(self, n: int = 5, names=None, arch_w: float = 0.7, arch_h: float = 1.5,
                 gap: float = 0.22, size: float = 20, floor: bool = True, **kw):
        super().__init__(**kw)
        self.arch_w, self.arch_h, self.gap, self.size = arch_w, arch_h, gap, size
        self.arches = VGroup(*[Arch(arch_w, arch_h) for _ in range(n)]).arrange(RIGHT, buff=gap,
                                                                               aligned_edge=DOWN)
        self.add(self.arches)
        self.floor = None
        if floor:
            self.floor = Line(self.arches.get_corner(DL) + LEFT * 0.15, self.arches.get_corner(DR) + RIGHT * 0.15,
                              color=S.GREY_DARK, stroke_width=3)
            self.add(self.floor)
        self.labels = self.name_labels(names) if names else VGroup()

    def name_labels(self, names, color=INK, below_first: bool = True) -> VGroup:
        """Labels for the arches (not added): alternately below the floor and above the lamps."""
        out = VGroup()
        for i, (a, s) in enumerate(zip(self.arches, names)):
            t = label(s, self.size, color) if not s.startswith("just") else mono(s, self.size, color)
            if (i % 2 == 0) == below_first:
                t.next_to(a, DOWN, buff=0.18)
            else:
                t.next_to(a.lamp, UP, buff=0.14)
            out.add(t)
        self.labels = out
        return out

    def mark(self, i: int, state: str, run_time: float = 0.3):
        return self.arches[i].to(state, run_time)

    def mark_all(self, states, run_time: float = 0.6, lag: float = 0.12):
        return LaggedStart(*[a.to(s) for a, s in zip(self.arches, states)], lag_ratio=lag,
                           run_time=run_time)


def envelope(text: str = "your commit", env_w: float = 1.7, env_h: float = 1.05, color=LAPTOP,
             size: float = 20) -> VGroup:
    """A commit as an envelope (opaque, GREY outline, a flap, its name inside). .body .flap .text"""
    body = RoundedRectangle(width=env_w, height=env_h, corner_radius=0.06, stroke_color=color,
                            stroke_width=3).set_fill(S.BG, 1)
    flap = VMobject(stroke_color=color, stroke_width=3)
    flap.set_points_as_corners([[-env_w / 2 + 0.03, env_h / 2 - 0.03, 0], [0, env_h / 2 - 0.42, 0],
                                [env_w / 2 - 0.03, env_h / 2 - 0.03, 0]])
    t = label(text, size, INK).move_to([0, -env_h / 2 + 0.27, 0])
    g = VGroup(body, flap, t)
    g.body, g.flap, g.text = body, flap, t
    return g


def vault(text: str = "HISTORY", vault_w: float = 1.6, vault_h: float = 1.9, size: float = 20) -> VGroup:
    """The HISTORY vault: a frame, a round-wheeled door, the name above. .frame .door .text"""
    frame = RoundedRectangle(width=vault_w, height=vault_h, corner_radius=0.12, stroke_color=S.GREY,
                             stroke_width=4).set_fill(S.GREY_DARKER, 1)
    inner = RoundedRectangle(width=vault_w - 0.32, height=vault_h - 0.32, corner_radius=0.08,
                             stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARK, 1)
    wheel = VGroup(Circle(radius=0.26, stroke_color=INK, stroke_width=3),
                   *[Line(ORIGIN, 0.26 * np.array([np.cos(a), np.sin(a), 0]), color=INK, stroke_width=3)
                     for a in np.linspace(0, 2 * PI, 4, endpoint=False) + PI / 4])
    door = VGroup(inner, wheel)
    t = label(text, size, INK).next_to(frame, UP, buff=0.14)
    g = VGroup(frame, door, t)
    g.frame, g.door, g.text = frame, door, t
    return g


def tray(text: str = "staged", tray_w: float = 2.0, size: float = 20) -> VGroup:
    """The GREY staging tray the envelope sits in (and bounces back to). .shape .text"""
    shape = Polygon([-tray_w / 2, 0.22, 0], [tray_w / 2, 0.22, 0], [tray_w / 2 - 0.18, 0, 0],
                    [-tray_w / 2 + 0.18, 0, 0], stroke_color=LAPTOP, stroke_width=3).set_fill(LAPTOP, 0.15)
    t = label(text, size, LAPTOP).next_to(shape, DOWN, buff=0.12)
    g = VGroup(shape, t)
    g.shape, g.text = shape, t
    return g


class CommitGate(VGroup):
    """V1 · the commit, the turnstile, the HISTORY vault (slide 41 redrawn), left to right on a
    floor at y = 0 (move the whole group). Nothing is added to the scene for you.
        gate = CommitGate(5).move_to(...)                     # S01: unlabeled arches
        self.play(FadeIn(gate.envelope), FadeIn(gate.vault), FadeIn(gate.floor))
        self.play(gate.drop_in())                              # arches fall into place
        self.play(gate.approach())                             # the envelope stops before them
        gate.refuse(self, 2, "fail")                           # bounces back home
        gate.pass_through(self)                                # all pass; vault opens, letter in
    CommitGate(9, CHEESE_HOOKS, with_tray=True) for S09 (names: gate.turnstile.labels, not added).
    .envelope .turnstile (.arches) .vault (.door) .tray (None unless with_tray) .floor .home
    Width ~ 2.3 + n x (arch_w + gap) + 2.2: 5 arches ~ 9.1, 9 arches ~ 12.8 (arch_w 0.7, gap 0.22).
    After pass_through() the envelope is gone (gate.envelope is None): new_envelope() makes one."""

    def __init__(self, n: int = 5, names=None, arch_w: float = 0.7, arch_h: float = 1.5, gap: float = 0.22,
                 with_tray: bool = False, envelope_text: str = "your commit", vault_text: str = "HISTORY",
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.size, self.envelope_text = size, envelope_text
        self.turnstile = Turnstile(n, names, arch_w, arch_h, gap, size, floor=False)
        left_w, vault_w, sp = 1.9, 1.6, 0.55
        ts = self.turnstile
        ts.move_to([0, 0, 0], aligned_edge=DOWN)
        x_left = ts.get_left()[0] - sp - left_w / 2
        # the envelope's resting point, as an invisible dot that moves with the group
        self._home = Dot([x_left, 0.62, 0], radius=0.001).set_opacity(0)
        self.tray = tray(tray_w=left_w + 0.1, size=size).move_to([x_left, 0.11, 0]) if with_tray else None
        if self.tray is not None:
            self.tray.shift(DOWN * (self.tray.shape.get_bottom()[1]))
        self.envelope = envelope(envelope_text, size=size).move_to(self.home)
        self.vault = vault(vault_text, vault_w=vault_w, size=size)
        self.vault.move_to([ts.get_right()[0] + sp + vault_w / 2, 0, 0])
        self.vault.shift(UP * (0 - self.vault.frame.get_bottom()[1]))
        x0 = (self.tray.get_left()[0] if self.tray is not None else self.envelope.get_left()[0]) - 0.1
        self.floor = Line([x0, 0, 0], [self.vault.get_right()[0] + 0.1, 0, 0], color=S.GREY_DARK,
                          stroke_width=3)
        self._door_saved = self.vault.door.copy()
        self.add(self._home, self.floor, *([self.tray] if self.tray is not None else []), ts, self.vault,
                 self.envelope)

    @property
    def home(self) -> np.ndarray:
        """The envelope's resting point (follows the group when it moves)."""
        return self._home.get_center()

    @property
    def arches(self):
        return self.turnstile.arches

    def x_before(self, i: int) -> float:
        return self.arches[i].get_left()[0] - 0.25 - self.envelope.width / 2

    def drop_in(self, run_time: float = 0.8, height: float = 2.0):
        """Animation: the arches fall into place (the turnstile must not be on screen yet)."""
        return LaggedStart(*[FadeIn(a, shift=DOWN * height) for a in self.arches], lag_ratio=0.1,
                           run_time=run_time)

    def approach(self, run_time: float = 1.0):
        """Animation: the envelope slides to just before the first arch."""
        return self.envelope.animate(run_time=run_time).move_to([self.x_before(0), self.home[1], 0])

    def go_home(self, run_time: float = 0.7):
        return self.envelope.animate(run_time=run_time, path_arc=0.6).move_to(self.home)

    def refuse(self, scene, i: int, state: str = "fail", passed: bool = True, run_time: float = 0.3):
        """Play: the envelope goes through arches 0..i-1 (marked 'pass' if `passed`), arch i turns
        `state` and flashes, the envelope bounces back home (the tray)."""
        env = self.envelope
        for k in range(i):
            a = self.arches[k]
            anims = [env.animate.move_to([a.get_center()[0], self.home[1], 0])]
            if passed:
                anims.append(a.to("pass"))
            scene.play(*anims, run_time=run_time)
        a = self.arches[i]
        scene.play(env.animate.move_to([a.get_left()[0] - 0.05 - env.width / 2 + 0.35, self.home[1], 0]),
                   a.to(state), run_time=run_time + 0.1)
        scene.play(Indicate(a, color=STATE[state], scale_factor=1.12), run_time=0.5)
        scene.play(self.go_home(), run_time=0.7)

    def open(self, run_time: float = 0.5):
        """Animation: the vault door swings open (squeezed to its left edge)."""
        return self.vault.door.animate(run_time=run_time).stretch(0.08, 0, about_edge=LEFT)

    def shut(self, run_time: float = 0.5):
        tgt = self._door_saved.copy().move_to(self.vault.frame)
        return Transform(self.vault.door, tgt, run_time=run_time)

    def pass_through(self, scene, states=None, step_time: float = 0.28):
        """Play: through every arch (each takes its state, default 'pass'; 'skip' = GREY dashed),
        the door opens, the envelope goes in and fades, the door shuts. The envelope leaves the
        group (gate.envelope = None)."""
        env = self.envelope
        states = states or ["pass"] * len(self.arches)
        for a, s in zip(self.arches, states):
            scene.play(env.animate.move_to([a.get_center()[0], self.home[1], 0]), a.to(s), run_time=step_time)
        scene.play(env.animate.move_to([self.vault.get_left()[0] - env.width / 2 - 0.05, self.home[1], 0]),
                   self.open(), run_time=0.5)
        scene.play(env.animate.move_to(self.vault.frame), FadeOut(env), run_time=0.5)
        self.remove(env)
        scene.remove(env)
        self.envelope = None
        scene.play(self.shut(), run_time=0.4)

    def new_envelope(self, text: str | None = None) -> VGroup:
        """A fresh envelope at home (added to the group, not to the scene: FadeIn it)."""
        self.envelope = envelope(text or self.envelope_text, size=self.size).move_to(self.home)
        self.add(self.envelope)
        return self.envelope


# ---- the gate table (slide 98 redrawn): the running fixture of the video
GATE_COLUMNS = ("what is checked", "how", "command", "on every commit?")
# key: (what, how, command (mono), verdict, hermetic). Script wording where the script gives it
# (tests S07, system S08); format+lint, docs, config, types from slide 98 / S11 / S13.
GATE_ROWS = {
    "tests": ("unit + integration tests", "pytest in the image", "docker run … pytest", "yes · hermetic", True),
    "system": ("system tests", "real HTTP", "docker run --network host", "no: not hermetic", False),
    "format": ("format + lint", "black, flake8", "git commit", "yes", True),
    "docs": ("docs", "babykev docs check", "just docs check", "yes", True),
    "config": ("config files", "yamllint, uv, hadolint", "just lint-config", "yes", True),
    "types": ("types", "ty", "just types", "yes", True),
}
GATE_ORDER = ("tests", "format", "docs", "config", "types", "system")


class GateTable(VGroup):
    """V1 · the gate table: four columns (GATE_COLUMNS), hermetic rows inside the gate frame (a GREY
    frame with a small arch on its top-left corner), non-hermetic rows below it, outside, each in a
    GREY dashed outline. Build it with the rows THIS scene ends with; `filled` are on screen
    already, the others are empty slots until fill():
        gt = GateTable(keys=("tests", "system"), filled=("tests",)).move_to(...)
        self.play(FadeIn(gt))
        gt.fill(self, "system")            # row text appears YELLOW (the row being filled now)
        gt.settle(self, "system")          # final colours (verdict GREEN, or all GREY outside)
    GateTable() with no keys: the empty S03 table (header + an empty frame of two blank rows).
    rows={key: (what, how, cmd, verdict, hermetic)} overrides or adds rows. Columns size to the
    longest text: 12.6 wide with 'tests' alone, 13.1 with 'system' (centre it: x = 0). Overrides must
    not be longer than the default texts.
    .header (4 labels) .frame .rows{key} (each .cells .bar .outline) .slot(key) .header_pulse(i)"""

    def __init__(self, keys=(), filled=(), rows=None, size: float = 20, row_h: float = 0.52, **kw):
        super().__init__(**kw)
        self.data = {**GATE_ROWS, **(rows or {})}
        self.size, self.row_h = size, row_h
        keys = [k for k in GATE_ORDER if k in keys] + [k for k in keys if k not in GATE_ORDER]
        self.inside = [k for k in keys if self.data[k][4]]
        self.outside = [k for k in keys if not self.data[k][4]]
        cells = {k: self._cells(k) for k in keys}
        heads = [label(h, size, S.GREY) for h in GATE_COLUMNS]
        self.col_w = [max([h.width] + [c[j].width for c in cells.values()]) + 0.3 for j, h in enumerate(heads)]
        total = sum(self.col_w)
        x0 = -total / 2
        xs = [x0 + sum(self.col_w[:j]) + 0.15 for j in range(4)]      # left edge of each column's text
        y = 0.0
        self.header = VGroup(*[h.move_to([xs[j] + h.width / 2, y, 0]) for j, h in enumerate(heads)])
        y -= 0.78                     # room for the arch icon between the header and the frame
        n_in = max(len(self.inside), 0 if keys else 2)
        frame_h = n_in * row_h + 0.2
        self.frame = RoundedRectangle(width=total + 0.16, height=max(frame_h, 0.3), corner_radius=0.12,
                                      stroke_color=S.GREY, stroke_width=3)
        self.frame.move_to([0, y - frame_h / 2 + 0.25, 0])
        icon = Arch(0.32, 0.5, stroke=3.5)
        icon.remove(icon.beam)
        icon.move_to(self.frame.get_corner(UL) + RIGHT * 0.4, aligned_edge=DOWN)
        self.icon = icon
        self.add(self.header, self.frame, icon)
        self.rows, self._slots = {}, {}
        yi = self.frame.get_top()[1] - 0.1 - row_h / 2
        for k in self.inside:
            self._slots[k] = yi
            yi -= row_h
        yo = self.frame.get_bottom()[1] - 0.2 - row_h / 2
        for k in self.outside:
            self._slots[k] = yo
            yo -= row_h + 0.1
        self.markers = {}
        for k in keys:
            r = self._row(k, cells[k], xs, total)
            self.rows[k] = r
            # an invisible point at the slot's centre travels with the table; fill() puts the row there
            self.markers[k] = Dot([0, self._slots[k], 0], radius=0.001).set_opacity(0)
            self.add(self.markers[k])
            if k in filled:
                self._final(r, k)
                self.add(r)

    def _cells(self, k):
        what, how, cmd, verdict, herm = self.data[k]
        return VGroup(label(what, self.size, TURN), label(how, self.size, TURN), mono(cmd, self.size, TURN),
                      label(verdict, self.size, TURN))

    def _row(self, k, cells, xs, total):
        y = self._slots[k]
        for j, c in enumerate(cells):
            c.move_to([xs[j] + c.width / 2, y, 0])
        bar = Rectangle(width=total, height=self.row_h - 0.08, stroke_width=0).set_fill(TURN, 0.13)
        bar.move_to([0, y, 0])
        r = VGroup(bar, cells)
        r.cells, r.bar, r.outline = cells, bar, None
        if not self.data[k][4]:
            ob = outline_box(total + 0.16, self.row_h, FUTURE, solid=False)
            ob.move_to([0, y, 0])
            r.outline = ob
            r.add(ob)
        return r

    def slot(self, key) -> np.ndarray:
        """The centre of row `key`'s slot (where it is, or will be after fill())."""
        return self.markers[key].get_center()

    def header_pulse(self, i: int, run_time: float = 0.6):
        """Animation: header i lights YELLOW and back."""
        return Indicate(self.header[i], color=TURN, scale_factor=1.12, run_time=run_time)

    def _final(self, r, k):
        herm = self.data[k][4]
        r.bar.set_fill(opacity=0)
        for j, c in enumerate(r.cells):
            c.set_color((VENV if j == 3 else INK) if herm else S.GREY)
        return r

    def fill(self, scene, key: str, run_time: float = 0.8):
        """Play: row `key` appears YELLOW in its slot (outside rows with their dashed outline)."""
        r = self.rows[key]
        r.shift(self.slot(key) - r.bar.get_center())
        scene.play(FadeIn(r.bar), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in r.cells], lag_ratio=0.2),
                   *([Create(r.outline)] if r.outline is not None else []), run_time=run_time)
        scene.remove(r, r.bar, *r.cells, *([r.outline] if r.outline is not None else []))
        self.add(r)
        scene.add(self)

    def settle(self, scene, key: str, run_time: float = 0.5):
        """Play: row `key` takes its final colours (verdict GREEN inside; all GREY outside)."""
        r = self.rows[key]
        tgt = self._final(r.copy(), key)
        scene.play(Transform(r, tgt), run_time=run_time)


# ================================================================== V2 · one request, three sizes
class RequestToken(VGroup):
    """The glowing PINK request token `GET /euclidean_distance/?x=3&y=4` (mono 20 pt).
    .pill .text .glow"""

    def __init__(self, text: str = REQUEST, size: float = 20, color=ROUTE, **kw):
        super().__init__(**kw)
        t = mono(text, size, color)
        h = mono("|", size).height + 0.26
        pill = RoundedRectangle(width=t.width + 0.5, height=h, corner_radius=h / 2, stroke_color=color,
                                stroke_width=3).set_fill(color, 0.14)
        glow = pill.copy().set_fill(opacity=0).set_stroke(color, 12, opacity=0.18)
        t.move_to(pill)
        self.pill, self.text, self.glow = pill, t, glow
        self.add(glow, pill, t)


def kind_box(kind: str, title: str | None = None, box_w: float = 3.0, box_h: float = 1.6,
             dashed: bool = False, size: float = 20) -> VGroup:
    """A test kind as a box in its colour (unit GREEN, integration TEAL, system BLUE), title at the
    top-left inside. .frame .title .kind"""
    col = KIND[kind]
    f = outline_box(box_w, box_h, col, solid=not dashed, fill_opacity=0.08)
    t = label(title or kind, size, col)
    t.move_to(f.get_corner(UL) + np.array([0.18 + t.width / 2, -0.15 - t.height / 2, 0]))
    g = VGroup(f, t)
    g.frame, g.title, g.kind = f, t, kind
    return g


def app_chain(names=APP_CHAIN, color=IMAGE, size: float = 20) -> VGroup:
    """'routing → validation → handler → power()' as chips joined by arrows (inside the app).
    .chips .arrows"""
    chips = VGroup(*[chip(n, color, size=size, font=MONO if n.endswith(")") else None) for n in names])
    chips.arrange(RIGHT, buff=0.45)
    arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.06, color=color, stroke_width=3,
                            tip_length=0.14, max_tip_length_to_length_ratio=0.5)
                      for a, b in zip(chips, chips[1:])])
    g = VGroup(chips, arrows)
    g.chips, g.arrows = chips, arrows
    return g


class TestPyramid(VGroup):
    """V2 · the README's pyramid: wide GREEN base 'unit · many, fast', TEAL middle 'integration',
    narrow BLUE top 'system · few, slow' (width = how many, height = cost per test).
    .layers{"unit", "integration", "system"} (each .shape .text); .extra_rows() -> two faint dashed
    rows 'smoke · does it answer at all' / 'acceptance · none yet' under the base (not added)."""

    __test__ = False      # not a pytest class

    TEXTS = {"unit": "unit · many, fast", "integration": "integration", "system": "system · few, slow"}

    def __init__(self, base_w: float = 7.2, top_w: float = 2.6, layer_h: float = 0.85, gap: float = 0.08,
                 size: float = 22, texts=None, **kw):
        super().__init__(**kw)
        self.base_w, self.layer_h, self.size = base_w, layer_h, size
        texts = {**self.TEXTS, **(texts or {})}
        self.layers = {}
        n = 3
        tot = n * layer_h + (n - 1) * gap
        for i, k in enumerate(("unit", "integration", "system")):
            y0 = i * (layer_h + gap)
            w0 = base_w - (base_w - top_w) * (y0 / tot)
            w1 = base_w - (base_w - top_w) * ((y0 + layer_h) / tot)
            shape = Polygon([-w0 / 2, y0, 0], [w0 / 2, y0, 0], [w1 / 2, y0 + layer_h, 0],
                            [-w1 / 2, y0 + layer_h, 0], stroke_color=KIND[k], stroke_width=3)
            shape.set_fill(KIND[k], 0.18)
            t = label(texts[k], size, INK).move_to(shape)
            lay = VGroup(shape, t)
            lay.shape, lay.text = shape, t
            self.layers[k] = lay
            self.add(lay)
        self.move_to(ORIGIN)

    def extra_rows(self, size: float = 20) -> VGroup:
        rows = VGroup()
        for s in ("smoke · does it answer at all", "acceptance · none yet"):
            t = label(s, size, S.GREY)
            ob = outline_box(self.base_w, 0.5, S.GREY, solid=False)
            t.move_to(ob)
            rows.add(VGroup(ob, t))
        rows.arrange(DOWN, buff=0.1).next_to(self.layers["unit"], DOWN, buff=0.18)
        return rows


class HermeticBorder(VGroup):
    """V2 · the GREEN dashed hermetic border ('only your code can make it fail'), its name on the
    top edge. HermeticBorder.around(mob, buff=0.35). .frame .text"""

    def __init__(self, box_w: float, box_h: float, text: str = "hermetic", size: float = 20, **kw):
        super().__init__(**kw)
        self.frame = outline_box(box_w, box_h, HERMETIC, solid=False, stroke=3)
        t = label(text, size, HERMETIC)
        bg = Rectangle(width=t.width + 0.2, height=t.height + 0.08, stroke_width=0).set_fill(S.BG, 1)
        lab = VGroup(bg, t).move_to(self.frame.get_corner(UL) + np.array([0.35 + t.width / 2, 0, 0]))
        self.text = lab
        self.add(self.frame, lab)

    @classmethod
    def around(cls, mob, buff: float = 0.35, **kw) -> "HermeticBorder":
        b = cls(mob.width + 2 * buff, mob.height + 2 * buff, **kw)
        b.shift(mob.get_center() - b.frame.get_center())
        return b


class NestedKinds(VGroup):
    """V2 · the lecture's nested boxes (slides 66/95): a GREEN unit box `power(3, 2)` inside a TEAL
    integration box ('integration · TestClient + app'), the GREEN dashed hermetic border around it;
    the BLUE system box encloses all that and reaches past the border's right edge, where its PINK
    wire runs to `server :9000` (outside: a live server can be down for reasons not your bug).
    ~9.6 wide x 3.9 tall. .unit .integration .border .system .wire .server"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.unit = kind_box("unit", "unit", 2.6, 1.15, size=size)
        call = mono("power(3, 2)", size, INK).move_to(self.unit.frame).shift(DOWN * 0.17)
        self.unit.add(call)
        self.unit.call = call
        self.integration = kind_box("integration", "integration · TestClient + app", 5.4, 2.3, size=size)
        self.unit.move_to(self.integration.frame).shift(DOWN * 0.25 + RIGHT * 1.0)
        self.border = HermeticBorder.around(VGroup(self.integration, self.unit), buff=0.32, size=size)
        bf = self.border.frame
        sys_l, sys_r = bf.get_left()[0] - 0.3, bf.get_right()[0] + 3.2
        sys_b, sys_t = bf.get_bottom()[1] - 0.3, bf.get_top()[1] + 0.6
        self.system = kind_box("system", "system · the whole program", sys_r - sys_l, sys_t - sys_b, size=size)
        self.system.move_to([(sys_l + sys_r) / 2, (sys_b + sys_t) / 2, 0])
        self.server = chip("server :9000", SYSTEM_TEST, size=size, font=MONO)
        self.server.move_to([(bf.get_right()[0] + sys_r) / 2, self.integration.frame.get_center()[1], 0])
        self.wire = Line(self.integration.frame.get_right(), self.server.get_left(), color=ROUTE, stroke_width=4)
        self.add(self.system, self.border, self.integration, self.unit, self.wire, self.server)
        self.move_to(ORIGIN)


class TestDot(VGroup):
    """One test as a dot: idle (GREY outline), pass (filled in its kind colour + a check), fail
    (RED), skip (GREY dashed ring with an 's': never GREEN). .disc .ring .mark .letter .state"""

    __test__ = False

    def __init__(self, color=UNIT, r: float = 0.17, state: str = "idle", **kw):
        super().__init__(**kw)
        self.kind_color, self.r = color, r
        self.disc = Circle(radius=r, stroke_width=0).set_fill(color, 0)
        self.ring = DashedVMobject(Circle(radius=r), num_dashes=10, dashed_ratio=0.999)
        self.ring.set_stroke(S.GREY, 2.5)
        self.letter = label("s", 20, SKIP).move_to(ORIGIN).set_opacity(0)
        self.state = "idle"
        self.add(self.disc, self.ring, self.letter)
        if state != "idle":
            self.become_state(state)

    def _parts(self, state):
        col = {"pass": self.kind_color, "fail": ERR, "skip": SKIP, "idle": S.GREY, "run": self.kind_color}[state]
        ring = DashedVMobject(Circle(radius=self.r), num_dashes=10,
                              dashed_ratio=0.5 if state == "skip" else 0.999).move_to(self.disc)
        ring.set_stroke(col, 2.5)
        disc = self.disc.copy().set_fill(col, {"pass": 0.85, "fail": 0.85, "run": 0.4}.get(state, 0))
        return ring, disc

    def become_state(self, state: str):
        ring, disc = self._parts(state)
        self.ring.become(ring)
        self.disc.become(disc)
        self.letter.set_opacity(1 if state == "skip" else 0)
        self.state = state
        return self

    def to(self, state: str, run_time: float = 0.4):
        """Animation: the dot takes `state`."""
        ring, disc = self._parts(state)
        self.state = state
        return AnimationGroup(Transform(self.ring, ring), Transform(self.disc, disc),
                              self.letter.animate.set_opacity(1 if state == "skip" else 0), run_time=run_time)


class TestDots(VGroup):
    """A grid of TestDot (n, colours by kind). TestDots(5, SYSTEM_TEST, cols=5);
    TestDots(22, [UNIT] * 11 + [INTEG] * 11, cols=11). .dots ; .to(indices, state) -> Animation"""

    __test__ = False

    def __init__(self, n: int, color=UNIT, cols: int | None = None, r: float = 0.17, buff: float = 0.16,
                 state: str = "idle", **kw):
        super().__init__(**kw)
        colors = color if isinstance(color, (list, tuple)) else [color] * n
        self.dots = VGroup(*[TestDot(c, r, state) for c in colors])
        self.dots.arrange_in_grid(cols=cols or n, buff=buff)
        self.add(self.dots)

    def to(self, indices, state: str, run_time: float = 0.6, lag: float = 0.15):
        idx = [indices] if isinstance(indices, int) else list(indices)
        return LaggedStart(*[self.dots[i].to(state) for i in idx], lag_ratio=lag, run_time=run_time)


# ================================================================== V3 · collector and fixtures
# the repo's test functions (assets/source/cheese-app-ci-cd/tests, def lines); 11 + 10 + 5 = 26
COLLECT = {
    "unit": ("tests/unit/", "test_utils.py", [
        "test_power_positive_integers", "test_power_with_zero_exponent", "test_power_with_one",
        "test_power_negative_base", "test_power_negative_exponent", "test_power_with_floats",
        "test_power_large_numbers", "test_power_fractional_exponent", "test_power_special_float_values",
        "test_power_invalid_inputs", "test_power_boolean_values"]),
    "integration": ("tests/integration/", "test_api.py", [
        "test_root_endpoint", "test_root_returns_json", "test_euclidean_distance_endpoint",
        "test_euclidean_distance_default_parameters", "test_euclidean_distance_with_floats",
        "test_invalid_route_returns_404", "test_method_not_allowed", "test_cors_enabled",
        "test_cors_allows_all_origins", "test_api_health_check"]),
    "system": ("tests/system/", "test_system_api.py", [
        "is_api_running", "test_root_endpoint", "test_health_check", "test_euclidean_distance_endpoint_default",
        "test_euclidean_distance_endpoint_custom_values", "test_api_structure"]),
}


class Collector(VGroup):
    """V3 · pytest's collector over the tests/ tree: three columns (folder + file, one tile per
    function in file order); only `test_*` names light (lit_color, default GREEN as the script
    says); `is_api_running` (a helper) and any extra stays dark.
        col = Collector().move_to(...)
        col.sweep(self, run_time=3.0)        # a YELLOW scanner; tiles light; the counter climbs to 26
        b = col.extra("broken", "unit")       # a dark mono chip under the unit tiles (not added)
    .columns{kind} (.head .tiles) .tiles (all, in order) .names (parallel list) .counter .scanner"""

    def __init__(self, tile_w: float = 2.6, tile_h: float = 0.17, size: float = 20, lit_color=VENV, **kw):
        super().__init__(**kw)
        self.lit_color, self.size = lit_color, size
        self.columns, self.names, tiles = {}, [], []
        for kind, (folder, fname, funcs) in COLLECT.items():
            head = VGroup(folder_glyph(0.24, S.BLUE), mono(folder, size, INK)).arrange(RIGHT, buff=0.12)
            fl = VGroup(file_glyph(0.3, S.GREY), mono(fname, size, INK)).arrange(RIGHT, buff=0.12)
            ts = VGroup(*[RoundedRectangle(width=tile_w, height=tile_h, corner_radius=0.05,
                                           stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(S.GREY_DARK, 0.5)
                          for _ in funcs]).arrange(DOWN, buff=0.07)
            col = VGroup(head, fl, ts).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            fl.shift(RIGHT * 0.3)
            ts.align_to(fl, LEFT)
            col.head, col.file, col.tiles, col.funcs = head, fl, ts, funcs
            self.columns[kind] = col
        VGroup(*self.columns.values()).arrange(RIGHT, buff=0.5, aligned_edge=UP)
        for kind, col in self.columns.items():
            for tl, fn in zip(col.tiles, col.funcs):
                tl.fn = fn
                tiles.append(tl)
                self.names.append(fn)
            self.add(col)
        self.tiles = tiles
        self.counter = steady("collected 0", size, INK)
        self.counter.next_to(self.columns["system"], DOWN, buff=0.35).align_to(self.columns["system"], LEFT)
        self.add(self.counter)
        top, bot = self.get_top()[1] + 0.1, self.get_bottom()[1] - 0.05
        self.scanner = Line([0, top, 0], [0, bot, 0], color=TURN, stroke_width=5).move_to(
            [self.get_left()[0] - 0.15, (top + bot) / 2, 0])

    def matches(self, tile) -> bool:
        return tile.fn.startswith("test_")

    def _count(self, k):
        return steady(f"collected {k}", self.size, INK).move_to(self.counter, aligned_edge=LEFT)

    def sweep(self, scene, run_time: float = 3.0, again: bool = False):
        """Play the scanner over the three columns: matching tiles light, the counter climbs.
        again=True: the tiles are lit already (a second sweep only flashes them)."""
        scene.play(FadeIn(self.scanner), run_time=0.2)
        k = 0
        per = (run_time - 0.4) / len(self.columns)
        for col in self.columns.values():
            hits = [t for t in col.tiles if self.matches(t)]
            k += len(hits)
            x = col.get_right()[0] + 0.15
            anims = [self.scanner.animate.set_x(x)]
            if not again:
                anims.append(LaggedStart(*[t.animate.set_fill(self.lit_color, 0.85).set_stroke(self.lit_color)
                                           for t in hits], lag_ratio=0.15))
                anims.append(Transform(self.counter, self._count(k)))
            else:
                anims.append(LaggedStart(*[Indicate(t, color=self.lit_color, scale_factor=1.05) for t in hits],
                                         lag_ratio=0.1))
            scene.play(*anims, run_time=per, rate_func=linear)
        scene.play(FadeOut(self.scanner), run_time=0.2)
        self.scanner.set_x(self.get_left()[0] - 0.15)
        scene.remove(self.scanner)

    def extra(self, name: str = "broken", kind: str = "unit") -> VGroup:
        """A dark mono chip `name` placed under column `kind` (not added)."""
        c = chip(name, S.GREY_DARK, size=self.size, font=MONO, text_color=S.GREY)
        c.next_to(self.columns[kind].tiles, DOWN, buff=0.15).align_to(self.columns[kind].tiles, LEFT)
        return c


class FixtureWiring(VGroup):
    """V3 · slide 58's wiring, 'what it could look like' (not this repo's code): test cards on the
    right ask for `client` by name; a conftest.py box in the middle builds it.
        fw = FixtureWiring()
        self.play(FadeIn(fw))                                # cards, conftest box, 'asks for' arrows
        inst, anims = fw.session(); self.play(*anims)        # one instance shared by every test
        copies, anims = fw.per_test(); self.play(*anims)     # a fresh copy per test (default scope)
    .tests (cards) .conftest (.frame .title) .fixture (chip `client`) .asks (arrows)"""

    def __init__(self, tests=("test_root_endpoint", "test_cors_enabled", "test_api_health_check"),
                 fixture: str = "client", size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.tests = VGroup(*[chip(f"{t}({fixture})", S.GREY, size=size, font=MONO) for t in tests])
        self.tests.arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([1.0, 0, 0], aligned_edge=LEFT)
        self.fixture = chip(fixture, TOOL, size=size, font=MONO)
        cf_title = mono("conftest.py", size, S.GREY)
        frame = box(3.6, 2.2, S.GREY, fill_opacity=0.06)
        frame.move_to([-3.4, 0.5, 0])
        cf_title.next_to(frame.get_top(), DOWN, buff=0.15)
        self.fixture.move_to(frame).shift(DOWN * 0.2)
        self.conftest = VGroup(frame, cf_title)
        self.conftest.frame, self.conftest.title = frame, cf_title
        self.asks = VGroup(*[Arrow(t.get_left(), self.fixture.get_right(), buff=0.12, color=S.GREY,
                                   stroke_width=2.5, tip_length=0.15) for t in self.tests])
        self.ask_label = note("asks for", 20).move_to(
            [(frame.get_right()[0] + self.tests.get_left()[0]) / 2, self.tests[0].get_top()[1] + 0.2, 0])
        self.add(self.conftest, self.fixture, self.tests, self.asks)

    def _instance(self):
        return chip("TestClient(app)", INTEG, size=self.size, font=MONO)

    def session(self):
        """-> (instance, animations): one instance, built once (scope='session'), lines to all tests."""
        inst = self._instance().next_to(self.conftest.frame, DOWN, buff=0.35)
        links = VGroup(*[Line(inst.get_right(), t.get_left(), color=INTEG, stroke_width=2.5) for t in self.tests])
        g = VGroup(inst, links)
        return g, [FadeIn(inst, shift=DOWN * 0.2), LaggedStart(*[Create(ln) for ln in links], lag_ratio=0.2)]

    def per_test(self):
        """-> (copies + links, animations): a column of fresh instances under the conftest box, one
        line from each copy to its own test (the default, function scope)."""
        copies = VGroup(*[self._instance() for _ in self.tests]).arrange(DOWN, buff=0.1)
        copies.next_to(self.conftest.frame, DOWN, buff=0.3)
        links = VGroup(*[Line(c.get_right(), t.get_left(), color=INTEG, stroke_width=2.5)
                         for c, t in zip(copies, self.tests)])
        return VGroup(copies, links), [LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in copies], lag_ratio=0.25),
                                       LaggedStart(*[Create(ln) for ln in links], lag_ratio=0.2)]


PARAM_CASES = (("2, 3", "8"), ("3, 2", "9"), ("5, 2", "25"), ("10, 2", "100"))   # test_utils.py:15-18


class Parametrize(VGroup):
    """V3 · parametrize folds four copies of one test into one function with four inputs (the four
    asserts of test_power_positive_integers, tests/unit/test_utils.py:15-18).
        pz = Parametrize(); self.play(FadeIn(pz.cards)); self.play(*pz.fold())
    .cards (four 'assert power(2, 3) == 8' cards, 2 x 2) .merged (not added: the folded card,
    .head .chips)"""

    def __init__(self, cases=PARAM_CASES, size: float = 20, **kw):
        super().__init__(**kw)
        self.cards = VGroup(*[chip(f"assert power({a}) == {b}", S.GREY, size=size, font=MONO)
                              for a, b in cases]).arrange_in_grid(rows=2, buff=(0.4, 0.3))
        head = VGroup(mono('@pytest.mark.parametrize("base, exp, want", …)', size, TOOL),
                      mono("def test_power(base, exp, want): …", size, INK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.12)
        chips = VGroup(*[chip(f"({a}, {b})", UNIT, size=size, font=MONO) for a, b in cases]).arrange(RIGHT, buff=0.25)
        body = VGroup(head, chips).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        frame = box(body.width + 0.6, body.height + 0.5, S.GREY, fill_opacity=0.06)
        body.move_to(frame)
        self.merged = VGroup(frame, body)
        self.merged.head, self.merged.chips, self.merged.frame = head, chips, frame
        self.merged.move_to(self.cards)
        self.add(self.cards)

    def fold(self, run_time: float = 1.2):
        """Animations: each card turns into its input chip; the function header appears."""
        m = self.merged
        return [AnimationGroup(FadeIn(m.frame), FadeIn(m.head, shift=DOWN * 0.1),
                               *[FadeTransform(c, ch) for c, ch in zip(self.cards, m.chips)], run_time=run_time)]


# ================================================================== V4 · the ribbon and the funnel
class Ribbon(VGroup):
    """V4 · service.py line 15 (95 characters) as a ribbon of character cells, text-free, three
    segments: 'app = FastAPI(' (14 cells, INK) · its arguments (80, GREY) · ')' (1, INK).
    Black at width 88 folds it to three rows (head / 4-space indent + arguments / ')'), at 120 it
    unfolds to one. Cells are cell=0.1 wide, so width w sits at x = .x0 + w x cell. It is built
    with its left edge at x = -5.8 (the 120 post at 6.2): move it only vertically (rb.set_y(...)).
        rb = Ribbon(); rb.set_y(1.0)                     # one row, 9.5 wide
        p88 = rb.post(88); self.play(FadeIn(p88)); self.play(rb.fold())
        self.play(rb.move_post(p88, 120), rb.unfold())   # flip-flop: loop it
    .cells .segments .x0 (left edge) .y0 (first row's centre) ; post(width, color, text=None)"""

    SEGMENTS = ((14, INK), (80, S.GREY), (1, INK))

    def __init__(self, segments=SEGMENTS, cell: float = 0.1, cell_h: float = 0.3, gap: float = 0.012,
                 row_gap: float = 0.16, **kw):
        super().__init__(**kw)
        self.cell, self.cell_h, self.gap, self.row_gap = cell, cell_h, gap, row_gap
        self.seg_len = [n for n, _ in segments]
        self.cells = VGroup()
        for n, col in segments:
            for _ in range(n):
                self.cells.add(Rectangle(width=cell - gap, height=cell_h, stroke_width=0).set_fill(col, 0.8))
        self.n = len(self.cells)
        for i, c in enumerate(self.cells):
            c.move_to([i * cell + cell / 2, 0, 0])
        self.add(self.cells)
        self.move_to(ORIGIN)
        self.shift(RIGHT * (self.LEFT_EDGE - self.x0))

    LEFT_EDGE = -5.8      # so that a post at 120 (x = 6.2) and its label stay inside the frame

    @property
    def x0(self) -> float:
        return self.cells[0].get_left()[0] - self.gap / 2

    @property
    def y0(self) -> float:
        return self.cells[0].get_center()[1]

    def _layout(self, rows):
        """rows: list of (start_cell, indent_cells, count)."""
        anims, k = [], 0
        x0, y0 = self.x0, self.y0
        for r, (indent, count) in enumerate(rows):
            for j in range(count):
                c = self.cells[k]
                anims.append(c.animate.move_to([x0 + (indent + j) * self.cell + self.cell / 2,
                                                y0 - r * (self.cell_h + self.row_gap), 0]))
                k += 1
        return anims

    def fold(self, run_time: float = 1.0):
        """Animation: black's three-row layout (head; 4 + arguments; ')')."""
        a, b, c = self.seg_len
        return AnimationGroup(*self._layout([(0, a), (4, b), (0, c)]), run_time=run_time)

    def unfold(self, run_time: float = 1.0):
        """Animation: back to one row of 95."""
        return AnimationGroup(*self._layout([(0, self.n)]), run_time=run_time)

    def post(self, w: int, color=TURN, text: str | None = None, size: float = 20, post_h: float = 1.6) -> VGroup:
        """A width post at column w (a vertical line from above the ribbon down past three rows),
        its number above it (mono). .line .text .w"""
        x = self.x0 + w * self.cell
        top = self.y0 + self.cell_h / 2 + 0.3
        ln = Line([x, top, 0], [x, top - post_h, 0], color=color, stroke_width=4)
        t = mono(text or str(w), size, color).next_to(ln, UP, buff=0.08)
        g = VGroup(ln, t)
        g.line, g.text, g.w = ln, t, w
        return g

    def move_post(self, post, w: int, run_time: float = 0.8, text: str | None = None):
        """Animation: the post slides to column w; its number changes (steady Transform)."""
        x = self.x0 + w * self.cell
        new_t = mono(text or str(w), post.text.font_size, post.text.get_color())
        new_t.move_to([x, post.text.get_center()[1], 0])
        post.w = w
        return AnimationGroup(post.line.animate.set_x(x), Transform(post.text, new_t), run_time=run_time)


class FindingsFunnel(VGroup):
    """V4 · findings as a shrinking RED bar (width ∝ count), its count to the right ('70 findings'),
    a faint notch left where each earlier step ended, and a GREY note under each step.
        ff = FindingsFunnel([70, 69, 37], ["ruff check", "--fix", "--unsafe-fixes"])
        self.play(FadeIn(ff)); self.play(ff.step())  # -> 69; again -> 37
    babykev (S10, s02-12/14/15): 70 → 69 → 37 (slide 31's 79 before `just fmt` is `recorded`).
    cheese (S05): digest:190 measured 8 findings in 8eb63fc's service.py at 120 → 2 after black
    (not a terminal capture: the script names only the 2 survivors).
    .bar .count .notches .notes .k"""

    def __init__(self, counts, notes=None, bar_w: float = 8.0, bar_h: float = 0.5, size: float = 20,
                 unit: str = "findings", **kw):
        super().__init__(**kw)
        self.counts, self.bar_w, self.bar_h, self.size, self.unit = list(counts), bar_w, bar_h, size, unit
        self.notes_txt = list(notes) if notes else [None] * len(counts)
        self.k = 0
        self.track = Rectangle(width=bar_w, height=bar_h, stroke_color=S.GREY_DARK, stroke_width=1.5)
        self.bar = self._bar(0)
        self.count = self._count(0)
        self.notches = VGroup()
        self.note = self._note(0)
        self.add(self.track, self.bar, self.count, self.notches, *([self.note] if self.note else []))

    def _w(self, k):
        return max(0.05, self.bar_w * self.counts[k] / max(self.counts))

    def _bar(self, k):
        w = self._w(k)
        return Rectangle(width=w, height=self.bar_h, stroke_width=0).set_fill(ERR, 0.85).move_to(
            self.track.get_left() + RIGHT * w / 2)

    def _count(self, k):
        return steady(f"{self.counts[k]} {self.unit}", self.size, ERR).next_to(self.track, RIGHT, buff=0.25)

    def _note(self, k):
        s = self.notes_txt[k]
        return steady(s, self.size, S.GREY).next_to(self.track, DOWN, buff=0.15).align_to(self.track, LEFT) if s else None

    def step(self, run_time: float = 0.9):
        """Animation: to the next count (bar shrinks, count changes, a notch stays at the old end)."""
        old_x = self.bar.get_right()[0]
        self.k += 1
        notch = Line([old_x, self.track.get_top()[1] + 0.08, 0], [old_x, self.track.get_bottom()[1] - 0.08, 0],
                     color=ERR, stroke_width=2, stroke_opacity=0.45)
        self.notches.add(notch)
        anims = [Transform(self.bar, self._bar(self.k)), Transform(self.count, self._count(self.k)),
                 FadeIn(notch)]
        n = self._note(self.k)
        if n is not None and self.note is not None:
            anims.append(Transform(self.note, n))
        return AnimationGroup(*anims, run_time=run_time)


# ================================================================== V5 · the hand-over chain
# short arch names (<= 14 chars), in config order
CHEESE_HOOKS = ("whitespace", "end of file", "YAML", "large files", "JSON", "merge markers",
                "private keys", "black", "flake8")            # .pre-commit-config.yaml:12-44
BABYKEV_HOOKS = ("large files", "merge markers", "no .env", "just check")   # babykev config :9-24
SHARED_HOOKS = ("large files", "merge markers")


class HandoverChain(VGroup):
    """V5 · slide 34 redrawn, top-down then right: git commit (GREY chip) ↓ .git/hooks/pre-commit
    (GREY file card) ↓ pre-commit (PURPLE tool chip) ↓ .pre-commit-config.yaml (TEAL-outlined card)
    → a Turnstile of the config's hooks (9 for "cheese", 4 for "babykev"; names alternate below /
    above the arches; built, not added: hc.turnstile.labels). ~12.3 wide x 4.6 tall (cheese).
        hc = HandoverChain("cheese")
        self.play(LaggedStart(*[FadeIn(m) for m in hc.links], lag_ratio=0.4))
        self.play(FadeIn(hc.drop), hc.turnstile.animate ...)   # or FadeIn(hc.turnstile)
        self.play(LaggedStart(*[FadeIn(t) for t in hc.turnstile.labels], lag_ratio=0.15))
        n = hc.hook_note()   # GREY tag 'machine-specific · never committed' right of the hook card
    .git .hook .tool .config .arrows .links (chips and arrows interleaved) .drop .turnstile"""

    def __init__(self, variant: str = "cheese", size: float = 20, arch_w: float | None = None,
                 arch_h: float = 1.3, gap: float | None = None, **kw):
        super().__init__(**kw)
        self.size = size
        self.git = chip("git commit", LAPTOP, size=size, font=MONO)
        self.hook = file_card(".git/hooks/pre-commit", LAPTOP, size)
        self.tool = tool_chip("pre-commit", size)
        self.config = file_card(".pre-commit-config.yaml", IMAGE, size)
        col = VGroup(self.git, self.hook, self.tool, self.config).arrange(DOWN, buff=0.42)
        self.arrows = VGroup(*[Arrow(a.get_bottom(), b.get_top(), buff=0.05, color=S.GREY, stroke_width=3,
                                     tip_length=0.14, max_tip_length_to_length_ratio=0.5)
                               for a, b in zip(col, col[1:])])
        self.links = VGroup(self.git, self.arrows[0], self.hook, self.arrows[1], self.tool, self.arrows[2],
                            self.config)
        names = CHEESE_HOOKS if variant == "cheese" else BABYKEV_HOOKS
        if arch_w is None:
            arch_w = 0.6 if variant == "cheese" else 0.7
        if gap is None:
            gap = 0.18 if variant == "cheese" else 0.6
        self.turnstile = Turnstile(len(names), None, arch_w, arch_h, gap, size)
        self.turnstile.next_to(col, RIGHT, buff=0.9)
        self.turnstile.shift(UP * (self.config.get_center()[1] + 0.25 - self.turnstile.arches.get_center()[1]))
        self.turnstile.name_labels(names)
        self.drop = Arrow(self.config.get_right(), [self.turnstile.get_left()[0], self.config.get_center()[1], 0],
                          buff=0.08, color=S.GREY, stroke_width=3, tip_length=0.15)
        self.add(self.links, self.drop, self.turnstile)
        shift = -VGroup(self, self.turnstile.labels).get_center()
        self.shift(shift)
        self.turnstile.labels.shift(shift)

    def hook_note(self, text: str = "machine-specific · never committed") -> VGroup:
        return tag(text, S.GREY).next_to(self.hook, RIGHT, buff=0.3)


# ================================================================== V6 · the mask grid
def segment_ids(state: int, questions) -> list[int]:
    """A request shape -> per-token segment ids: (2, [2, 2]) -> [0, 0, 1, 1, 2, 2];
    (1, [1, 1, 1]) -> [0, 1, 2, 3] (0 = the state, k = question k)."""
    out = [0] * state
    for k, n in enumerate(questions, start=1):
        out += [k] * n
    return out


SEG_SIX = segment_ids(2, [2, 2])        # slide 72: tokens 1-2 state, 3-4 question 1, 5-6 question 2
SEG_FOUR = segment_ids(1, [1, 1, 1])    # slide 79/81: the shrunk shape (1, [1, 1, 1])
# an illustrative shrink path for the dice beat: every shape fails under the wrong fix, ending at
# hypothesis's real answer (s05a-08:25). The intermediate shapes are NOT hypothesis's own steps.
SHRINK_PATH = ((3, [2, 1, 3]), (2, [1, 1, 2]), (1, [1, 1, 1]))


def mask_matrix(seg, rule: str = "want") -> list[list[bool]]:
    """allowed[i][j] (row i = the token that looks, column j = the token looked at), causal:
      "want"      a question sees the state and itself (slide 72; model.py:151 after the fix)
      "ones"      step-05's bug: torch.ones_like makes every pair 'same question' (plain causal)
      "wrong_fix" step-05a's deliberate wrong fix: also sees any question more than one back
      "siblings"  pairs in two different questions (slide 81; not causal-restricted)"""
    n = len(seg)
    m = [[False] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            si, sj = seg[i], seg[j]
            if rule == "siblings":
                m[i][j] = si != 0 and sj != 0 and si != sj
                continue
            if j > i:
                continue
            if rule == "want":
                m[i][j] = sj == si or sj == 0
            elif rule == "ones":
                m[i][j] = True
            elif rule == "wrong_fix":
                m[i][j] = sj == si or sj == 0 or sj < si - 1
            else:
                raise ValueError(rule)
    return m


def mask_rows(seg, rule: str = "want") -> list[str]:
    """The '#'/'.' rows the walk prints: mask_rows(SEG_SIX, "ones") == s05-04 lines 2-7."""
    return ["".join("#" if x else "." for x in r) for r in mask_matrix(seg, rule)]


def shape_text(state: int, questions) -> str:
    """'shape = (1, [1, 1, 1])', as hypothesis prints it (s05a-08:25)."""
    return f"shape = ({state}, [{', '.join(str(q) for q in questions)}])"


def shape_caption(state: int, questions) -> str:
    """'state 1 · questions 1, 1, 1' (the S13 checker card's caption)."""
    return f"state {state} · questions {', '.join(str(q) for q in questions)}"


class MaskGrid(VGroup):
    """V6 · the n x n attention mask: '#' cells (allowed) filled in the colour of the token looked
    at (state GREEN, questions TEAL; siblings grid: GREY), '.' cells dark. Token numbers 1..n
    above the columns and left of the rows; a segment band under the columns ('state', 'q1' …).
        g = MaskGrid(SEG_SIX, "ones")                       # step-05's built mask
        g = MaskGrid.from_rows(cap.at((2, 7)), SEG_SIX)     # straight from the printed rows
        self.play(g.flash_rows([4, 5]))                     # 0-based rows 5-6 RED
        self.play(g.retarget("want"))                       # cells change to another rule
        marks = g.wrong_fix_marks()   # (RED boxes on correctly blocked adjacent-question cells,
                                      #  YELLOW boxes on wrongly open two-back cells) — not added
        sib = MaskGrid(SEG_FOUR, "siblings"); g.overlap(sib) -> [(i, j)] ; g.light([(3, 1)])
    cell=0.5: 6 x 6 is ~3.0 + labels ~3.8 wide; cell 0.7 for a big 4 x 4.
    .cells[i][j] .grid (VGroup of all) .rows_text .seg .rule .row_labels .col_labels .band"""

    def __init__(self, seg=SEG_SIX, rule: str = "want", cell: float = 0.5, size: float = 20,
                 numbers: bool = True, band: bool = True, rows=None, **kw):
        super().__init__(**kw)
        self.seg, self.rule, self.cell, self.size = list(seg), rule, cell, size
        n = len(self.seg)
        allowed = ([[ch == "#" for ch in r] for r in rows] if rows is not None else mask_matrix(self.seg, rule))
        self.allowed = allowed
        self.cells = []
        self.grid = VGroup()
        for i in range(n):
            row = []
            for j in range(n):
                sq = Square(side_length=cell * 0.92, stroke_width=1.5)
                self._paint(sq, i, j, allowed[i][j])
                sq.move_to([j * cell, -i * cell, 0])
                row.append(sq)
                self.grid.add(sq)
            self.cells.append(row)
        self.add(self.grid)
        self.row_labels = VGroup()
        self.col_labels = VGroup()
        if numbers:
            for k in range(n):
                self.col_labels.add(label(str(k + 1), size, S.GREY).next_to(self.cells[0][k], UP, buff=0.12))
                self.row_labels.add(label(str(k + 1), size, S.GREY).next_to(self.cells[k][0], LEFT, buff=0.14))
            self.add(self.col_labels, self.row_labels)
        self.band = VGroup()
        if band:
            for s in sorted(set(self.seg)):
                ks = [k for k, v in enumerate(self.seg) if v == s]
                a, b = self.cells[-1][ks[0]], self.cells[-1][ks[-1]]
                col = VENV if s == 0 else IMAGE
                ln = Line(a.get_corner(DL) + DOWN * 0.12 + RIGHT * 0.03, b.get_corner(DR) + DOWN * 0.12 + LEFT * 0.03,
                          color=col, stroke_width=5)
                t = label("state" if s == 0 else f"q{s}", size, col)
                t.next_to(ln, DOWN, buff=0.08)
                self.band.add(VGroup(ln, t))
            self.add(self.band)
        self.rows_text = ["".join("#" if x else "." for x in r) for r in allowed]
        self.move_to(ORIGIN)

    @classmethod
    def from_rows(cls, rows, seg=None, field: int = 0, **kw) -> "MaskGrid":
        """A grid from printed '#'/'.' rows: cap.at((2, 7)) of s05-04; for the checker captures
        ('##..#. #####. WRONG') field=0 is the wanted picture, field=1 the built mask."""
        rows = [r.split()[field] for r in rows]
        return cls(seg if seg is not None else list(range(len(rows))), "want", rows=rows, **kw)

    def _paint(self, sq, i, j, on: bool):
        if on:
            col = S.GREY if self.rule == "siblings" else (VENV if self.seg[j] == 0 else IMAGE)
            sq.set_fill(col, 0.6).set_stroke(col, 1.5)
        else:
            sq.set_fill(S.GREY_DARKER, 1).set_stroke(S.GREY_DARK, 1.5)
        return sq

    def cell_box(self, i: int, j: int, color=ERR, stroke: float = 4) -> Square:
        """An outline square around cell (i, j), 0-based (not added)."""
        return Square(side_length=self.cell, stroke_color=color, stroke_width=stroke).move_to(self.cells[i][j])

    def row_box(self, i: int, color=ERR, stroke: float = 4) -> Rectangle:
        """An outline around row i (0-based; not added)."""
        r = VGroup(*self.cells[i])
        return Rectangle(width=r.width + 0.1, height=self.cell + 0.04, stroke_color=color,
                         stroke_width=stroke).move_to(r)

    def flash_rows(self, rows, color=ERR, run_time: float = 0.9):
        """Animation: rows (0-based) flash in `color` (Indicate)."""
        return AnimationGroup(*[Indicate(VGroup(*self.cells[i]), color=color, scale_factor=1.06) for i in rows],
                              run_time=run_time)

    def retarget(self, rule: str, run_time: float = 0.8):
        """Animation: every cell takes the colours of `rule`'s mask (self.rule/allowed update)."""
        new = mask_matrix(self.seg, rule)
        self.rule = rule
        anims = []
        for i, row in enumerate(self.cells):
            for j, sq in enumerate(row):
                if new[i][j] != self.allowed[i][j]:
                    anims.append(Transform(sq, self._paint(sq.copy(), i, j, new[i][j])))
        self.allowed = new
        self.rows_text = ["".join("#" if x else "." for x in r) for r in new]
        return AnimationGroup(*anims, run_time=run_time) if anims else self.grid.animate(run_time=0.01).shift(ORIGIN)

    def diff(self, rule: str = "want") -> list[tuple[int, int]]:
        """Cells where this grid differs from `rule`'s mask (the wrong cells)."""
        ref = mask_matrix(self.seg, rule)
        return [(i, j) for i in range(len(ref)) for j in range(len(ref)) if ref[i][j] != self.allowed[i][j]]

    def overlap(self, other: "MaskGrid") -> list[tuple[int, int]]:
        """Cells that are '#' in both grids (allowed ∩ siblings: the rule's violations)."""
        n = len(self.seg)
        return [(i, j) for i in range(n) for j in range(n) if self.allowed[i][j] and other.allowed[i][j]]

    def light(self, cells, color=ERR, run_time: float = 0.6):
        """Animation: cells (0-based (i, j)) fill `color` and pulse."""
        return AnimationGroup(*[self.cells[i][j].animate.set_fill(color, 0.9).set_stroke(color, 3)
                                for i, j in cells], run_time=run_time)

    def wrong_fix_marks(self, ok_color=ERR, open_color=TURN) -> tuple[VGroup, VGroup]:
        """For the wrong fix: (boxes on the adjacent-question cells it correctly blocks, boxes on the
        two-back cells it wrongly leaves open). Not added. Needs >= 3 questions (SEG_FOUR)."""
        blocked, opened = VGroup(), VGroup()
        for i, si in enumerate(self.seg):
            for j, sj in enumerate(self.seg[:i + 1]):
                if si >= 2 and sj == si - 1:
                    blocked.add(self.cell_box(i, j, ok_color))
                elif si >= 2 and 0 < sj < si - 1:
                    opened.add(self.cell_box(i, j, open_color))
        return blocked, opened


def sequence_bar(seg, cell: float = 0.7, size: float = 20) -> VGroup:
    """A packed request as a row of token boxes (state GREEN, questions TEAL), a label under each
    segment ('state', 'question 1' …; 'q1' … when a segment is too short for the long name).
    .tokens .labels"""
    toks = VGroup(*[RoundedRectangle(width=cell * 0.9, height=cell * 0.9, corner_radius=0.06,
                                     stroke_color=VENV if s == 0 else IMAGE, stroke_width=2.5)
                    .set_fill(VENV if s == 0 else IMAGE, 0.35) for s in seg]).arrange(RIGHT, buff=cell * 0.1)
    labs = VGroup()
    groups = [(s, VGroup(*[toks[k] for k, v in enumerate(seg) if v == s])) for s in sorted(set(seg))]
    short = any(label(f"question {s}", size).width > g.width + 0.1 for s, g in groups if s)
    for s, grp in groups:
        name = "state" if s == 0 else (f"q{s}" if short else f"question {s}")
        labs.add(label(name, size, VENV if s == 0 else IMAGE).next_to(grp, DOWN, buff=0.12))
    g = VGroup(toks, labs)
    g.tokens, g.labels = toks, labs
    return g


class Dice(VGroup):
    """A PURPLE die (hypothesis drawing a request shape). Dice(3); self.play(d.roll(5))."""

    PIPS = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)],
            4: [(-1, 1), (1, 1), (-1, -1), (1, -1)], 5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
            6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}

    def __init__(self, value: int = 3, side: float = 0.6, **kw):
        super().__init__(**kw)
        self.side = side
        self.body = RoundedRectangle(width=side, height=side, corner_radius=side * 0.18, stroke_color=TOOL,
                                     stroke_width=3).set_fill(TOOL, 0.15)
        self.pips = self._pips(value)
        self.add(self.body, self.pips)

    def _pips(self, v):
        d = self.side * 0.27
        return VGroup(*[Dot(self.body.get_center() + np.array([x * d, y * d, 0]), radius=self.side * 0.07,
                            color=INK) for x, y in self.PIPS[v]])

    def roll(self, value: int, run_time: float = 0.5):
        """Animation: a quarter turn and new pips."""
        new = self._pips(value)
        return AnimationGroup(Rotate(self.body, PI / 2), Transform(self.pips, new), run_time=run_time)


def coverage_sweep(panel, lines=None, color=VENV, run_time: float = 1.5):
    """V6 · the coverage highlighter: -> (bars, Animation) a GREEN bar sweeps onto every line of a
    code panel (or the 0-based `lines`). Add nothing yourself: play the animation, then the bars
    are on screen; fade them with the panel."""
    c = panel.code if hasattr(panel, "code") else panel
    ks = range(len(c.code_lines)) if lines is None else lines
    bars = VGroup(*[line_bar(c, k, color, 0.22) for k in ks])
    return bars, LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in bars], lag_ratio=0.25, run_time=run_time)


# ================================================================== V7 · baked-in code (L02's slabs)
class Slab(VGroup):
    """One image layer: a translucent slab with a TEAL outline, filled by its owner.
        Slab("RUN pip install --user .", SYSTEM, slab_w=4.6, slab_h=0.8) -> .box .text .label_text"""

    def __init__(self, text: str | None = None, fill=LAPTOP, slab_w: float = 4.6, slab_h: float = 0.46,
                 size: float = 20, dashed: bool = False, text_color=INK, **kw):
        super().__init__(**kw)
        self.fill_hex, self.slab_w, self.slab_h, self.size, self.label_text = fill, slab_w, slab_h, size, text
        r = RoundedRectangle(width=slab_w, height=slab_h, corner_radius=min(0.06, slab_h / 2.5),
                             stroke_color=IMAGE, stroke_width=2.5).set_fill(fill, 0.35)
        if dashed:
            r = DashedVMobject(r.set_fill(fill, 0), num_dashes=40, dashed_ratio=0.55).set_stroke(IMAGE, 2.5)
        self.box = r
        self.add(r)
        self.text = None
        if text:
            self.text = steady(text, size, text_color, mono_font=True).move_to(r)
            self.add(self.text)


class LayerStack(VGroup):
    """V7 · an image as layers, bottom-up, standing on .floor (invisible; place the stack first).
        st = LayerStack().move_to([3.2, -1.0, 0])
        slabs = [st.make(t, fill, h) for t, fill, h in CHEESE_LAYERS]
        for s, k in zip(slabs, (32, 35, 38, 39, 40, 41)): st.drop(self, s)   # as Dockerfile lines light
        st.rebuild(self, slabs[2:])                 # only the COPY slabs are replaced
    .slabs .floor ; make() drop() accept() brace() rebuild() top_y()"""

    def __init__(self, stack_w: float = 4.6, size: float = 20, gap: float = 0.04, **kw):
        super().__init__(**kw)
        self.stack_w, self.size, self.gap = stack_w, size, gap
        self.floor = Line(LEFT * stack_w / 2, RIGHT * stack_w / 2, stroke_width=0)
        self.slabs = VGroup()
        self._pending: list[Slab] = []
        self.add(self.floor, self.slabs)

    def top_y(self) -> float:
        tops = [s.box.get_top()[1] for s in [*self.slabs, *self._pending]]
        return max(tops) if tops else self.floor.get_center()[1] - self.gap

    def make(self, text, fill=LAPTOP, slab_h: float = 0.46, dashed: bool = False) -> Slab:
        """A slab placed where it will land (on top of the stack and of slabs made before it)."""
        s = Slab(text, fill, self.stack_w, slab_h, self.size, dashed)
        c = self.floor.get_center()
        s.move_to([c[0], self.top_y() + self.gap + slab_h / 2, 0])
        self._pending.append(s)
        return s

    def accept(self, scene, *slabs) -> None:
        for s in slabs:
            if s in self._pending:
                self._pending.remove(s)
            scene.remove(s)
            self.slabs.add(s)
        scene.add(self)

    def drop(self, scene, *slabs, anim=None, height: float = 1.0, run_time: float = 0.8, extra=()) -> list:
        """Play the slabs landing (fall in from `height` above, or `anim`), then they join the stack."""
        a = anim or LaggedStart(*[FadeIn(s, shift=DOWN * height) for s in slabs], lag_ratio=0.15)
        scene.play(a, *extra, run_time=run_time)
        self.accept(scene, *slabs)
        return list(slabs)

    def brace(self, slabs, text: str, direction=LEFT, size: float = 20, color=S.GREY) -> VGroup:
        """A brace beside `slabs` with a label (not added). .brace .text"""
        b = Brace(VGroup(*[s.box for s in slabs]), direction=direction, color=color, buff=0.12)
        t = label(text, size, color).next_to(b, direction, buff=0.12)
        out = VGroup(b, t)
        out.brace, out.text = b, t
        return out

    def rebuild(self, scene, slabs, run_time: float = 1.0, glow=TURN) -> list:
        """Play: `slabs` lift out and fresh copies (same text/fill) drop into their places, glowing
        briefly; the slabs below stay ('packages before code'). Returns the new slabs."""
        new = []
        for s in slabs:
            n = Slab(s.label_text, s.fill_hex, s.slab_w, s.slab_h, s.size).move_to(s)
            new.append(n)
        scene.play(LaggedStart(*[FadeOut(s, shift=UP * 0.6) for s in slabs], lag_ratio=0.1), run_time=run_time * 0.4)
        for s in slabs:
            self.slabs.remove(s)
        scene.play(LaggedStart(*[FadeIn(n, shift=DOWN * 0.6) for n in new], lag_ratio=0.1), run_time=run_time * 0.4)
        for n in new:
            self.slabs.add(n)
        scene.add(self)
        scene.play(*[Indicate(n.box, color=glow, scale_factor=1.03) for n in new], run_time=run_time * 0.4)
        return new


# Dockerfile:32-41 (thin pyproject.toml copy, the fat pip install, four thin COPY slabs)
CHEESE_LAYERS = (("COPY pyproject.toml", LAPTOP, 0.42), ("RUN pip install --user .", SYSTEM, 1.0),
                 ("COPY api/", LAPTOP, 0.42), ("COPY tests/", LAPTOP, 0.42), ("COPY pytest.ini", LAPTOP, 0.42),
                 ("COPY docker-entrypoint.sh", LAPTOP, 0.42))
