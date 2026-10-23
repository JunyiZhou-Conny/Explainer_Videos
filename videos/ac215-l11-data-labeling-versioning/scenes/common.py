"""Shared scene code for AC215 L11 (data labeling and versioning: where does a label live, and what
is a version?).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (placeholders only), the twelve README trackers A-L, loaders for the real captures in
assets/ (with the capture-only crops refused), terminal helpers, tags, small glyphs, and the video's
set pieces V1-V7 (StationMap, SignedTicket, OriginGate, FuseMount + MountLayers, HashShelf, TagRope,
PipelineMap). The scene authors' contract is build/SCENE-NOTES.md; the reference scene is
s01_hook.py; build/common_test.py (Bench) plays every set piece once.

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]   # one voiceover block per SAY

Every text here is >= 20 pt.  Never .scale() a group that holds text below 1.0; set pieces take
size parameters instead.  Never set width/height/color/depth on a VGroup subclass (Manim
properties): these classes use house_w, tile_w, card_w ...
Nothing is added to the scene for you unless a method's docstring says "plays".
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, UL, UP, UR, AnimationGroup, Arc, Arrow,
                   Circle, Create, DashedLine, DashedVMobject, Dot, FadeIn, FadeOut, FadeTransform,
                   GrowFromEdge, Indicate, LaggedStart, Line, MoveAlongPath, Polygon, Rectangle,
                   ReplacementTransform, RoundedRectangle, Rotate, ShowIncreasingSubsets, Succession,
                   Text, Transform, UpdateFromAlphaFunc, VGroup, VMobject, linear, there_and_back)

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon, ponder_card  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, TERM_BG,  # noqa: F401
                              FileTree, ReadmeTracker, Terminal, box, browser_window, cell_width, check_mark,
                              chip, code_block, code_panel, code_span, cross_mark, file_glyph, file_tree,
                              folder_glyph, form_rows, glyph_range, label, lecture_ref, line_bar, line_pitch,
                              mono, mono_line, step_badge, substring, tag, warning_sign)
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
# SAY lines per scene (script.md v2); every scene asserts its own count
SAY_COUNT = {"S01": 5, "S02": 7, "S03": 7, "S04": 8, "S05": 6, "S06": 8, "S07": 8, "S08": 7,
             "S09": 6, "S10": 8, "S11": 6, "S12": 11, "S13": 6, "S14": 7, "S15": 6, "S16": 7}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # your laptop: host shell, host filesystem, the browser, host cheese_dataset/, .dvc/cache
CLOUD = S.BLUE           # both buckets, storage.googleapis.com, dvc_store/, Colab, the signed-URL ticket
IMAGE = S.TEAL           # containers/images: data-label-studio, data-label-cli, data-version-cli, compose one-off
CONTAINER = IMAGE
SYSTEM = S.ORANGE        # root-owned folders, uid 1001 vs root, git's ownership check, apt, --privileged, /dev/fuse
ROOT = SYSTEM
OWNED = S.GREEN          # project-owned, protected: the secrets/ key, .dvc/config, cheese_dataset.dvc, tags
SECRET = OWNED
KEY = OWNED
POINTER = OWNED          # the pointer file and the tags (what your repo owns)
PASS = S.GREEN           # a check that passed
TOOL = S.PURPLE          # docker, compose, git, dvc, gcsfuse, gcloud, uv, the Label Studio SDK
ERR = S.RED              # 400/401, Exited (1), the failed build, the entrypoint's failure chain, refusals
TURN = S.YELLOW          # your turn, the tracker, the current step, "look here", ponder pointers
COST = S.GOLD            # money: GCS storage, the second copy in dvc_store/, what keeps billing
ROUTE = S.PINK           # the Docker street + DNS, mount pipes, md5 shelf paths, the tag → blob rope
HASH = ROUTE             # md5 strings are PINK (they are addresses)
FUTURE = S.GREY          # future / elsewhere / lecture-only: L13, lakeFS/Delta/Iceberg, monitoring: dashed
NOTE = INK = S.WHITE     # an annotation (a WHITE envelope: neutral data)
DOOR = S.GREY            # an open published port: neutral, never GREEN
DIMMED = S.GREY

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TRACK_BOTTOM = 2.9           # the tracker's lowest point
BOTTOM = -3.5                # a terminal's bottom edge (kept when it grows or shrinks)
PIC_TOP = 2.8                # pictures stay below this (tracker / lecture_ref above)


def strip_top(rows: int = 3, size: float = 22) -> float:
    """Top edge of a `rows`-row terminal standing on BOTTOM."""
    return BOTTOM + rows * line_pitch(size) + 0.85


STRIP_TOP = strip_top(3)     # -1.44: a picture over a 3-row strip lives in y in [-1.3, 2.8]


def steady(s: str, size: float = 20, color=INK, mono_font: bool = False, **kw) -> Text:
    """Text with a fixed vertical extent (an invisible '|' strut), so a Transform between two
    steady texts keeps the size the check tool computes. Use it for anything that morphs."""
    t = (mono if mono_font else label)("|" + s, size, color, **kw)
    pipe = t[0]
    if len(t) > 1:
        pipe.move_to([t[1].get_center()[0], pipe.get_center()[1], 0])
    pipe.set_opacity(0)
    return t


def note(s: str, color=S.GREY, size: float = 20, **kw) -> Text:
    """A caption line (label font, GREY by default). The 2nd positional arg is the colour."""
    return label(s, size, color, **kw)


# ------------------------------------------------------------------ running example (placeholders only)
USER = "student"
P_LAPTOP_HOME = "student@laptop:~$"
P_LABELING = "student@laptop:~/data-labeling$"
P_VERSIONING = "student@laptop:~/data-versioning$"
P_TODAY = "student@laptop:~/today$"
P_TODAY_DV = "student@laptop:~/today/data-versioning$"
P_COLAB = "$"
P_LAPTOP = P_LAPTOP_HOME
T_LAPTOP = "laptop"
T_SECOND = "laptop · second terminal"
T_TODAY = "laptop · second clone in ~/today"
T_COLAB = "colab stand-in · signed out"
PROJECT_ID = "your-gcp-project"            # the only project id ever shown as ours
BUCKET = "your-bucket-placeholder"         # our bucket (both parts)
BUCKET1 = "cheese-app-data-demo"           # the README's labeling bucket: V2/V7 vault name, RED in 54:38
CLASS_BUCKET = "cheese-app-data-versioning"  # only in quoted lines and RED class-repo beats
GH_USER = "YOUR_GITHUB_USERNAME"
LOGIN = ("student@example.com", "awesome")
TOKEN = "student-demo-token-not-a-secret"  # obviously fake (GREY chip "obviously fake")
SA_NAME = "data-service-account"
KEY_FILE = "data-service-account.json"
KEY_PATH = "/secrets/data-service-account.json"
ENV_VAR = "GOOGLE_APPLICATION_CREDENTIALS"
NETWORK = "data-labeling-network"
STORAGE_HOST = "https://storage.googleapis.com"
PAGE_ORIGIN = "http://localhost:8080"
CONTAINERS = {"studio": "data-label-studio", "cli": "data-label-cli", "dvc": "data-version-cli"}
CHOICES = ("brie", "gouda", "gruyere", "parmigiano")         # README:113-115 / 28's <Choice>s
SLIDE6_ROWS = ("brie", "gouda", "parmigiano", "gruyere")     # script S02: slide 6's 'Labeled' rows
STAGES = ("Authenticate", "Bucket Mounting", "Connecting the Application", "Using the Data")  # slides 29-32
STAGES_2L = ("Authenticate", "Bucket\nMounting", "Connecting the\nApplication", "Using the Data")


# ------------------------------------------------------------------ captures
LAPTOP_DIR = "laptop"
# file lines never to print (ASSETS "Capture-only deviations", script.md "Crops"): checked by Capture.line()
NEVER = {("laptop", "19-docker-logs.txt"): {8, 9},                  # PyPI fetch through the proxy
         ("laptop", "63-docker-image-ls.txt"): {5, 6},              # the re-tagged base images
         ("laptop", "72-docker-image-ls.txt"): {5, 6},
         ("laptop", "152-docker-image-ls.txt"): {6, 7}}
# lines refused in every file: Docker's proxy injection, the relay address, gcsfuse's JSON INFO log
NEVER_RE = (re.compile(r"^Added environment "), re.compile(r"172\.17\.0\.1"),
            re.compile(r'"severity":"INFO"'))
NEVER_FILES = {("laptop", "119-clone-class-repo.txt")}               # the class repo's head date: never shown

_PROMPT_RE = re.compile(r"^((?:\([^)]*\) )?(?:[\w.-]+@)?[\w.-]+:[^#$\s]*[#$])(?: (.*))?$")


def split_prompt(s: str) -> tuple[str, str]:
    """'app@5bf8945fb887:/app$ python cli.py -c' -> ('app@5bf8945fb887:/app$', 'python cli.py -c');
    'root@d5bf95465b66:/app# dvc init' too. A line without a prompt -> ('', s)."""
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
        """File line n (1-based; line 1 is the '$ …' command, never printed). Refuses the crops."""
        if not 1 <= n <= len(self.raw):
            raise IndexError(f"{self.path.name} has {len(self.raw)} lines, not {n}")
        s = self.raw[n - 1]
        if n in self.never or any(r.search(s) for r in NEVER_RE):
            raise ValueError(f"{self.path.name}:{n} is capture-only and is never shown (ASSETS.md crops)")
        if re.fullmatch(r"\[exit -?\d+\]", s):
            raise ValueError(f"{self.path.name}:{n} is the [exit N] line: never printed")
        return s

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

    def istep(self, n: int) -> tuple[str, str]:
        """File line n split into (prompt, typed): the istep captures 41, 42, 44, 54, 88, 90, 93,
        95, 104, 115, 117, 145."""
        return split_prompt(self.line(n))


def capture(name: str) -> Capture:
    """capture("41") / capture("41-docker-shell-CLI") / capture("laptop/41") / capture("C13") /
    capture("colab/C13"): the one file assets/terminal/<folder>/NN-*.txt (a name starting with C
    is a colab file). Fails loudly when missing: never show an uncaptured output. A trailing
    inline '[exit N]' (20:2, 27:2 …) is split off the last line."""
    if "/" in name:
        folder, name = name.split("/", 1)
    else:
        folder = "colab" if re.match(r"C\d", name) else LAPTOP_DIR
    if folder == "capture-only" or name.startswith("capture-only"):
        raise ValueError("capture-only/ is plumbing (placeholder key, base images): never shown")
    d = TERMINAL / folder
    stem = name[:-4] if name.endswith(".txt") else name
    p = d / f"{stem}.txt"
    if not p.exists():
        hits = sorted(d.glob(f"{stem}-*.txt"))
        if len(hits) != 1:
            raise FileNotFoundError(f"capture {folder}/{name}: {len(hits)} matches "
                                    f"{[h.name for h in hits]} (see ASSETS.md)")
        p = hits[0]
    if (folder, p.name) in NEVER_FILES:
        raise ValueError(f"{p.name} is never shown (script.md Crops)")
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    raw = [s.rstrip("\r").expandtabs(8) for s in text.rstrip("\n").split("\n")]
    m = re.fullmatch(r"(.*\S)\[exit (-?\d+)\]", raw[-1]) if len(raw) > 1 else None
    if m:                                   # '{"status": "UP"}[exit 0]': output and status on one line
        raw = raw[:-1] + [m.group(1), f"[exit {m.group(2)}]"]
    cmd = raw[0][2:] if raw[0].startswith("$ ") else ""
    body = raw[1:]
    code_ = 0
    if body and re.fullmatch(r"\[exit -?\d+\]", body[-1]):
        code_ = int(body[-1][6:-1])
        body = body[:-1]
    return Capture(cmd, body, code_, raw, p, NEVER.get((folder, p.name), ()))


def _field(cap: str, n: int, key: str) -> str:
    """The value after 'key:' on file line n of a capture (the pointer file's md5/size/nfiles)."""
    s = capture(cap).line(n)
    return s.split(key + ":", 1)[1].strip()


# ---- facts read from the captures (never typed by hand): md5s, sizes, counts
IMAGES = tuple(f"Image_{i}.jpg" for i in range(1, 6))
MD5 = {}           # 'Image_1.jpg' -> its md5 (laptop/09b lines 2-6)
SIZES = {}         # 'Image_1.jpg' -> its byte count (laptop/09b lines 7-11)
for _n in range(2, 7):
    _h, _p = capture("09b").line(_n).split()
    MD5[_p.split("/")[-1]] = _h
for _n in range(7, 12):
    _b, _p = capture("09b").line(_n).split()
    SIZES[_p.split("/")[-1]] = _b
V20 = {"md5": _field("95", 59, "md5"), "size": _field("95", 60, "size"), "nfiles": _field("95", 61, "nfiles")}
V21 = {"md5": _field("104", 59, "md5"), "size": _field("104", 60, "size"), "nfiles": _field("104", 61, "nfiles")}
EMPTY = {"md5": _field("93", 82, "md5"), "size": _field("93", 83, "size"), "nfiles": _field("93", 84, "nfiles")}
CLASS_V21 = {"md5": _field("120", 10, "md5"), "size": _field("120", 11, "size"),
             "nfiles": _field("120", 12, "nfiles")}
HOOK_LINE = capture("95").line(59).strip().lstrip("- ")       # 'md5: 89db50de27acfd6822faabc3da39b0a8.dir'
POINTER_LINES = capture("95").at((58, 63))                     # the six-line cheese_dataset.dvc (v20)


def short(h: str, n: int = 8) -> str:
    """An md5 as the pictures show it: its first n characters + '…' (+ '.dir' for a manifest)."""
    return h[:n] + "…" + (".dir" if h.endswith(".dir") else "")


def aisle(h: str) -> str:
    """The cache/remote shelf an md5 is filed on: its first two characters ('5b/')."""
    return h[:2] + "/"


# ------------------------------------------------------------------ trackers (script.md, twelve)
SECTIONS = {
    "A": "data-labeling › Setup",
    "B": "data-labeling › Run & set up Label Studio",
    "C": "data-labeling › CORS & annotate",
    "D": "data-labeling › View Annotations using CLI",
    "E": "data-labeling › Extra: docker-compose",
    "F": "data-labeling › Docker Cleanup",
    "G": "data-versioning › Prepare Docker and Create Your Repository",
    "H": "data-versioning › Set Up GCP Storage and Credentials",
    "I": "data-versioning › Start the DVC Container",
    "J": "data-versioning › Create and View Dataset Versions",
    "K": "data-versioning › Updated Dataset Version: dataset_v21",
    "L": "data-versioning › Docker Cleanup",
}
STEPS = {
    "A": ["Clone", "secrets folder", "Service account + key", "Download & extract", "Bucket + two folders",
          "Upload the 21 images"],
    "B": ["sh docker-shell.sh", "docker container ls", "Log in", "Create project", "Source storage",
          "Target storage"],
    "C": ["Edit bucket name", "sh docker-shell-CLI.sh", "python cli.py -c", "python cli.py -m", "Annotate",
          "View in GCS"],
    "D": ["Copy the token", "cli.py -p -k", "cli.py -t -k"],
    "E": ["Stop (docker stop / docker ps)", "docker-shell-compose.sh"],
    "F": ["docker container ls", "stop", "docker system prune", "docker image ls"],
    "G": ["Clean Docker", "Clone the starter", "cd / rm -rf .git / git init", "New private repo", "First push"],
    "H": ["secrets folder", "Service account", "Bucket folders"],
    "I": ["Edit docker-shell.sh", "cd data-versioning", "sh docker-shell.sh"],
    "J": ["dvc init", "dvc remote add", "dvc add", "dvc push", "git ×5", "Colab dataset_v20"],
    "K": ["Upload images", "dvc add", "dvc push", "git ×5", "Colab dataset_v21"],
    "L": ["docker container ls", "docker system prune", "docker image ls"],
}
# the README steps that are missing: an `extra` row after the dots (track(tr, k, extra="row"))
EXTRA_ROWS = {"H": "upload the first photos", "I": "Dockerfile:36 fix"}
EXTRA_KINDS = ("Linux", "stand-in", "local remote")


def place_tracker(tr: ReadmeTracker) -> ReadmeTracker:
    """Pin a tracker to the house corner (left edge -6.5, top 3.5)."""
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def _suffix(tr, extra) -> str:
    if not extra:
        return ""
    if extra is True:
        return " · extra"
    if extra == "row":
        return f" · extra: {EXTRA_ROWS[tr.key]}"
    if extra in EXTRA_KINDS:
        return f" · extra · {extra}"
    raise ValueError(f"extra must be False, True, 'row' or one of {EXTRA_KINDS}, not {extra!r}")


def _caption(tr: ReadmeTracker, k: int, extra) -> Text:
    anchor = tr.xdot if getattr(tr, "xdot", None) is not None else tr.dots
    if not k:
        return steady("", tr.size, tr.hi_color).next_to(anchor, RIGHT, buff=0.25)
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    suf = _suffix(tr, extra)
    t = steady(s + suf, tr.size, tr.hi_color, t2c={suf.strip(): S.GREY} if suf else None)
    return t.next_to(anchor, RIGHT, buff=0.25)


def _xdot(tr, lit: bool):
    d = Circle(radius=0.06, stroke_color=TURN if lit else S.GREY, stroke_width=2)
    d.set_fill(TURN if lit else S.BG, 1 if lit else 0)
    return d


def tracker(key: str, step: int | None = None, extra=False) -> ReadmeTracker:
    """Tracker `key` ("A".."L") at `step` (1-based; None = no step lit yet), placed top-left:
    'README › <repo> › <section>', one dot per step (H and I: plus a hollow GREY 'extra row' dot,
    .xdot), and 'step k of N: <step>' + the extra suffix: extra=True (' · extra'), 'Linux',
    'stand-in', 'local remote' (' · extra · Linux' …) or 'row' (H/I's missing step; .xdot lights)."""
    tr = ReadmeTracker(SECTIONS[key], STEPS[key])
    tr.key = key
    tr.xdot = None
    if key in EXTRA_ROWS:
        tr.xdot = _xdot(tr, extra == "row").next_to(tr.dots, RIGHT, buff=0.2)
        tr.add(tr.xdot)
    if step:
        tr.set_step(step)
    tr.remove(tr.caption)
    tr.caption = _caption(tr, step or 0, extra)
    tr.extra = extra
    tr.add(tr.caption)
    return place_tracker(tr)


def _tracker_factory(key):
    def make(step=None, extra=False):
        return tracker(key, step, extra)
    make.__name__ = f"tracker_{key.lower()}"
    make.__doc__ = f"tracker('{key}', step, extra): README › {SECTIONS[key]}"
    return make


tracker_a, tracker_b, tracker_c, tracker_d, tracker_e, tracker_f = map(_tracker_factory, "ABCDEF")
tracker_g, tracker_h, tracker_i, tracker_j, tracker_k, tracker_l = map(_tracker_factory, "GHIJKL")


def track(tr: ReadmeTracker, k: int | None = None, extra=False, run_time: float = 0.5):
    """Animation: move the tracker to step k (None: stay) and set/clear the extra suffix (see
    tracker()). Use this, never tr.goto(). The caption cross-fades in place."""
    k = tr.k if k is None else k
    anims = []
    if k != tr.k:
        for i, d in enumerate(tr.dots, start=1):
            col = tr.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK)
            anims.append(d.animate.set_color(col).scale((1.5 if i == k else 1.0) / (d.width / 0.12)))
    if tr.xdot is not None and (extra == "row") != (tr.extra == "row"):
        anims.append(Transform(tr.xdot, _xdot(tr, extra == "row").move_to(tr.xdot)))
    old, new = tr.caption.copy(), _caption(tr, k, extra)

    def fade_swap(m, a):
        src, f = (old if a < 0.5 else new), abs(1 - 2 * a)
        c = src.copy()
        for g, g0 in zip(c.family_members_with_points(), src.family_members_with_points()):
            g.set_fill(opacity=g0.get_fill_opacity() * f).set_stroke(opacity=g0.get_stroke_opacity() * f)
        m.become(c)

    anims.append(UpdateFromAlphaFunc(tr.caption, fade_swap))
    tr.k, tr.extra = k, extra
    return AnimationGroup(*anims, run_time=run_time)


def swap_tracker(scene, old: ReadmeTracker, new: ReadmeTracker, *anims, run_time: float = 0.6):
    """Plays: tracker `old` becomes `new` in place (section name and caption cross-fade, the dots
    regroup). `new` ends on the scene as one piece; `old` is gone."""
    keep = VGroup(old.head[0], old.head[1])          # 'README ›' stays put
    scene.remove(old)
    olds = [old.head[2], old.dots, old.caption] + ([old.xdot] if old.xdot is not None else [])
    scene.add(*keep, *olds)
    moves = [FadeTransform(old.head[2], new.head[2]), ReplacementTransform(old.dots, new.dots),
             FadeTransform(old.caption, new.caption)]
    if old.xdot is not None:
        moves.append(FadeOut(old.xdot))
    if new.xdot is not None:
        moves.append(FadeIn(new.xdot))
    scene.play(*moves, *anims, run_time=run_time)
    scene.remove(*keep, *new.head, new.dots, new.caption, *olds)
    if new.xdot is not None:
        scene.remove(new.xdot)
    scene.add(new)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 11 · slides 20, 24' tag, top right (one per scene, BRIEF span)."""
    return lecture_ref(11, slides)


# ---- line transforms (script.md conventions)
def cut(s: str, after: str, ellipsis: str = "…") -> str:
    """The line cut right after `after` (first occurrence), ending in '…'."""
    i = s.index(after) + len(after)
    return s[:i] + ellipsis


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
    """Only the named columns of a docker table (header row first), re-aligned. 54/46: never the
    CREATED/STATUS columns: cols(cap.at((2, 3)), ["IMAGE", "PORTS", "NAMES"])."""
    heads, rows, right = _table(lines)
    idx = [heads.index(n) for n in names]
    return _align([[r[j] for j in idx] for r in rows], [right[j] for j in idx], gutter)


def squash(s, gutter: int = 2):
    """Progress-line padding collapsed: every run of 3+ spaces inside the line becomes `gutter`
    spaces (compose/build rows are padded to 110 columns: ' ✔ Image chromadb/chroma:latest Pulled
    <80 spaces> 10.3s'). Leading indentation is kept. A list maps over its items."""
    if isinstance(s, (list, tuple)):
        return [squash(x, gutter) for x in s]
    lead = len(s) - len(s.lstrip(" "))
    return s[:lead] + re.sub(r" {3,}", " " * gutter, s[lead:]).rstrip()


def soft(lines, n: int = 65) -> list:
    """Long lines broken at their last space that fits `n` characters (the text is unchanged, only
    the row break moves; a token longer than a row breaks at the edge). Items may be (text, colour)."""
    out = []
    for x in lines:
        s, c = (x, None) if isinstance(x, str) else x
        while len(s) > n:
            k = s.rfind(" ", 0, n + 1)
            if k > 0 and s[:k].strip():
                out.append((s[:k].rstrip(), c))
                s = s[k + 1:]
            else:
                out.append((s[:n], c))
                s = s[n:]
        out.append((s, c))
    return [s if c is None else (s, c) for s, c in out]




# ------------------------------------------------------------------ sources
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".ini": "ini", ".txt": "text", ".json": "json", ".lock": "toml", ".dvc": "yaml"}
# folder under assets/source -> header prefix (script.md: "starter ·", "README today ·")
_REPOS = {"data-labeling": "data-labeling", "data-versioning": "data-versioning",
          "data-versioning@data-versioning-ac215": "starter", "data-versioning@2515e5e": "README today · 2515e5e",
          "colab": "notebook"}
# personal data in the snapshots (ASSETS.md): any e-mail but the placeholder's, and any GitHub user in
# a data-versioning URL but the course's and the placeholder, are replaced on the way in
_EMAIL_RE = re.compile(r"(?<![\w.+-])(?!git@)(?!student@example\.com)[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
_GHUSER_RE = re.compile(r"(github\.com[/:])(?!dlops-io/)(?!YOUR_GITHUB_USERNAME/)[\w-]+(/data-versioning)")


def mask(s: str) -> str:
    """Source text with the personal data replaced: e-mails -> student@example.com, a GitHub user
    in a data-versioning URL -> YOUR_GITHUB_USERNAME. excerpt()/code()/readme() apply it."""
    s = _EMAIL_RE.sub(LOGIN[0], s)
    return _GHUSER_RE.sub(r"\1" + GH_USER + r"\2", s)


def _src(path: str) -> Path:
    p = SOURCE / path
    if p.exists() and p.is_file():
        return p
    raise FileNotFoundError(f"assets/source/{path} (folders: {', '.join(_REPOS)})")


def source_text(path: str) -> str:
    """An assets/source file, masked: 'data-labeling/docker-shell.sh',
    'data-versioning@data-versioning-ac215/docker-entrypoint.sh', 'colab/notebook-1RRQ1SlH.cells.txt'."""
    return mask(_src(path).read_text(encoding="utf-8"))


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of assets/source/<path>, masked."""
    return "\n".join(source_text(path).split("\n")[first - 1:last])


def shown_path(path: str) -> str:
    """The header name of a source file: 'data-labeling · docker-shell.sh', 'starter ·
    docker-entrypoint.sh', 'README today · 2515e5e · README.md', 'notebook · 1RRQ1SlH'."""
    rel = _src(path).relative_to(SOURCE).as_posix()
    top, _, rest = rel.partition("/")
    if top == "colab":
        return "notebook · " + rest.split("-")[1].split(".")[0]
    return f"{_REPOS[top]} · {rest}"


def _lang(name: str) -> str:
    if name.startswith("Dockerfile"):
        return "docker"
    if name.startswith(".env") or name in (".gitignore", ".dvcignore"):
        return "bash"
    if name.endswith(".cells.txt"):
        return "python"
    if name == "config":
        return "ini"
    return _LANG.get(Path(name).suffix, "text")


def code(path: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, shown: str | None = None, max_lines: int = 12, cuts: dict | None = None,
         dedent: bool = False):
    """CODE(path: first–last) of script.md: a code_panel quoting assets/source/<path> (masked), header
    '<shown> · lines a–b' (shown_path()). <= 12 lines. 22 pt fits <= 66 characters a line, 20 pt
    <= 73: a longer line raises; cut it with cuts={file_line: 'text it ends after'} (the house '…',
    recoloured GREY; pygments would paint it pink-red) or use font_size=20 (<= 73).
    .code .header; highlight with code_span(p.code, k, "x"), line_bar(p.code, k, colour), k = file
    line - first. dedent=True removes the excerpt's common leading indentation, nothing else.
    Notebook cells: code('colab/notebook-1RRQ1SlH.cells.txt', 328, 329, shown='notebook · cell 15')."""
    last = first if last is None else last
    if last - first + 1 > max_lines:
        raise ValueError(f"CODE {path}: {last - first + 1} lines; never more than {max_lines} lines "
                         f"on screen (show a long file as successive windows of <= {max_lines} lines)")
    text = excerpt(path, first, last)
    if dedent:
        import textwrap
        text = textwrap.dedent(text)
    lines = text.split("\n")
    cuts = cuts or {}
    for n, after in cuts.items():
        lines[n - first] = cut(lines[n - first], after)
    limit = 66 if font_size >= 22 else 73
    for i, s in enumerate(lines):
        if len(s.expandtabs(4)) > limit:
            raise ValueError(f"CODE {path}:{first + i} is {len(s)} characters; > {limit} at {font_size} pt "
                             f"leaves the frame: cuts={{{first + i}: '...'}} or font_size=20")
    language = language or _lang(Path(path).name)
    p = code_panel("\n".join(lines), shown or shown_path(path), first, language, focus=focus,
                   font_size=font_size)
    for n in cuts:
        code_span(p.code, n - first, "…").set_color(S.GREY)
    return p


def readme(n: int, repo: str = "data-labeling") -> str:
    """README.md line n (1-based) of a source folder ('data-labeling', 'data-versioning' = the pin
    b240b1a, 'data-versioning@data-versioning-ac215' = the starter's, 'data-versioning@2515e5e' =
    today's), stripped and masked: assert capture("01").cmd == readme(14)."""
    return excerpt(f"{repo}/README.md", n, n).strip()


def readme_card(lines, body, quote: bool = False, card_w: float | None = None, size: float = 22,
                repo: str | None = None) -> VGroup:
    """A GREY README card: header 'README.md · line n' (or 'lines a–b' for a tuple; with repo=
    'data-versioning' / 'starter' …: 'data-versioning · README.md · line n') and the README's own
    words (str: '\\n' separates lines, label font; or any mobject). .frame .head .body"""
    where = f"line {lines}" if isinstance(lines, int) else f"lines {lines[0]}–{lines[1]}"
    name = f"{repo} · README.md" if repo else "README.md"
    head = VGroup(mono(name, CAPTION, S.GREY), label(f"· {where}", CAPTION, S.GREY)).arrange(RIGHT, buff=0.12)
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
def term(prompt: str = P_LAPTOP_HOME, rows: int = 10, title: str | None = T_LAPTOP, width: float = 12.6,
         size: float = 22, place: bool = True) -> Terminal:
    """The house terminal: 12.6 wide, 22 pt, 65 characters a row, centred, bottom edge at BOTTOM.
    Height = rows x 0.403 + 0.85. Full width, or a 3-row strip (rows=3) under a picture. size=20
    gives 72 characters a row (the long one-liners: 07, 09, 09b, the sed edits, 84, 120, 121)."""
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)
    if place:
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def laptop_term(rows: int = 10, prompt: str = P_LAPTOP_HOME) -> Terminal:
    return term(prompt, rows, T_LAPTOP)


def second_term(rows: int = 3, prompt: str = P_LAPTOP_HOME, title: str = T_SECOND) -> Terminal:
    """A second shell strip: 'laptop · second terminal' (S12/S13's class-repo checks); with
    title=T_TODAY and prompt=P_TODAY the route-T strip (S09/S12); T_COLAB + P_COLAB the Colab
    stand-in (S15)."""
    return term(prompt, rows, title)


def colab_term(rows: int = 3) -> Terminal:
    """The Colab stand-in strip: title 'colab stand-in · signed out', prompt '$'."""
    return term(P_COLAB, rows, T_COLAB)


def container_note() -> VGroup:
    """The GREY chip at a scene's second container prompt (script conventions)."""
    return grey_chip("our capture: a fresh container for each step · stay in yours")


def reenter(scene, t: Terminal, cap: str, type_time: float | None = None):
    """Plays the DVC-container re-entry of the script's conventions (93, 95, 104, 115, 117; 90 too):
    types `sh docker-shell.sh` and prints only lines 27-28, '…', 41-42 of capture `cap`, then
    sets the terminal's prompt to the capture's own container prompt (line 45; 90/93: the line
    after 44). Returns (the typed line, the printed rows). Add the GREY chip 'same entrypoint
    errors as before' (reentry_chip()) yourself."""
    c = capture(cap)
    line = type_cmd(scene, t, "sh docker-shell.sh", type_time)
    rows = out(scene, t, c.at((27, 28), "…", (41, 42)), wrap=True)
    for n in range(43, len(c.raw) + 1):
        p, _ = split_prompt(c.raw[n - 1])
        if p:
            t.set_prompt(p)
            break
    return line, rows


def reentry_chip() -> VGroup:
    return grey_chip("same entrypoint errors as before")


def resize(scene, t: Terminal, rows: int, keep=None, extra=(), run_time: float = 0.8) -> Terminal:
    """Plays: grow or shrink terminal `t` to `rows` (bottom edge kept). It keeps its last lines (at
    most `keep`), or exactly the line mobjects in `keep` (a list). `extra`: animations alongside."""
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


def room(scene, t: Terminal, n: int, run_time: float = 0.3) -> None:
    """Plays: make room for n new rows the gentle way: the oldest rows fade where they are, then the
    rest slide up (the toolkit's own scroll sails old rows over the tracker)."""
    over = len(t.lines) + n - t.rows
    if over <= 0:
        return
    gone = VGroup(*t.lines.submobjects[:over])
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(gone), run_time=run_time * 0.4)
    for m in gone:
        t.lines.remove(m)
    scene.remove(gone, *gone.get_family())
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=run_time * 0.6)


def bare_prompt(scene, t: Terminal):
    """Plays: the prompt returns (no output): a prompt line with nothing typed yet."""
    room(scene, t, 1)
    ln = t.type(scene, "", type_time=0)
    ln.bare = True
    return ln


def type_cmd(scene, t: Terminal, cmd: str, type_time: float | None = None):
    """Plays: type at the waiting prompt (replacing a bare prompt line if there is one; room is made
    first). Long commands fold at a space with ' \\' (Terminal.fold). Returns the line, or a VGroup
    with .rows when it folded."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    p = t.prompt + " "
    room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
    return t.type(scene, cmd, type_time)


def out(scene, t: Terminal, lines, wrap: bool = False, run_time: float = 0.6, lag: float = 0.08,
        chunk: int | None = None, color=OUTPUT) -> VGroup:
    """Plays: print capture lines (text or (text, colour)) in chunks that fit the box (`chunk` rows,
    default all rows), making room the gentle way. wrap=True breaks long lines at their last space
    that fits (soft()); otherwise a long line is refused (cut it, or wrap). Returns the new rows."""
    items = soft(lines, t.max_chars) if wrap else list(lines)
    for x in items:
        s = x if isinstance(x, str) else x[0]
        if len(s) > t.max_chars:
            raise ValueError(f"out(): {len(s)} > {t.max_chars} characters: wrap=True or cut it: {s!r}")
    items = [(x, color) if isinstance(x, str) else x for x in items]
    k = max(1, min(t.rows, chunk or t.rows))
    chunks = [items[i:i + k] for i in range(0, len(items), k)]
    rows = VGroup()
    for ch in chunks:
        room(scene, t, len(ch))
        rows.add(*t.print(scene, ch, run_time=run_time / len(chunks) + 0.1, lag=lag))
    return rows


def istep(scene, t: Terminal, line: str, type_time: float | None = None):
    """Plays: a typed line at a container prompt, from its capture ('app@3c41bc0606ad:/app$ ls …'):
    set the terminal's prompt to the capture's own, then type the rest."""
    prompt, typed = split_prompt(line)
    if prompt:
        t.set_prompt(prompt)
    return type_cmd(scene, t, typed, type_time)


def cd_prompt(scene, t: Terminal, new_prompt: str, color=LAPTOP, run_time: float = 0.6):
    """Plays: after `cd`, the prompt changes; a bare prompt line appears and its path flashes."""
    t.set_prompt(new_prompt)
    ln = bare_prompt(scene, t)
    path = new_prompt.split(":", 1)[1].rstrip("$# ")
    scene.play(Indicate(substring(ln, path), color=color, scale_factor=1.08), run_time=run_time)
    scene.add(ln)
    return ln


def rows_of(line) -> list:
    """The rows of a typed line (a folded command has several)."""
    return list(line.rows) if hasattr(line, "rows") else [line]


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
    """Plays: show `mob` (placed with beside()) and make it part of the row, so it scrolls with it.
    Refuses a tag that would cover the row's text."""
    row = _row_of(line)
    if covers_text(mob, row):
        raise ValueError(f"pin(): this {mob.width:.2f}-wide tag would cover the text of its row; "
                         "use a row_tag, put it on an output row, or under the terminal")
    scene.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
    return attach(scene, row, mob)


def unpin(scene, line, mob, *extra, run_time: float = 0.3):
    """Plays: fade a pinned mark out and take it off its row (so it never snaps back)."""
    row = _row_of(line)
    scene.play(FadeOut(mob), *extra, run_time=run_time)
    if mob in row.submobjects:
        row.remove(mob)
    scene.remove(mob)


def on_bar(t: Terminal, mob, buff: float = 0.15):
    """Put a row-sized tag (turn_row(), extra_row(), time_row() …) on terminal t's title bar, at its
    right end: for a command row too long to hold a tag beside it. Add/FadeIn it yourself (it is not
    part of any row, so it does not scroll)."""
    return mob.move_to([t.box.get_right()[0] - buff - mob.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])


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


def extra_row(kind=None) -> VGroup:
    """'extra' sized for a terminal row (GREY); kind 'Linux' / 'stand-in' / 'local remote' gives
    'extra · Linux' …"""
    return row_tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def standin_row() -> VGroup:
    """'extra · stand-in' sized for a terminal row (the photo copies 94/103, the time travel 114-117)."""
    return extra_row("stand-in")


def local_row() -> VGroup:
    """'extra · local remote' sized for a terminal row (dvc push -r standin, 95/104)."""
    return extra_row("local remote")


def time_row() -> VGroup:
    """'at the time of recording' sized for a terminal row (GREY)."""
    return row_tag("at the time of recording", S.GREY)


def editor_row(s: str = "our editor; use yours") -> VGroup:
    """The GREY row tag of the sed edits (40, 85, 87)."""
    return row_tag(s, S.GREY)


def cost_row(s: str = "storage: a fraction of a cent a month") -> VGroup:
    """The GOLD cost tag sized for a terminal row (never an amount: see cost_tag())."""
    return row_tag(_no_amount(s), COST)


def flash_tag(scene, tg, color=None, scale: float = 1.15, run_time: float = 0.8, *extra) -> None:
    """Plays: flash a tag's words and pulse an unfilled copy of its outline (then drops the copy).
    Never Indicate a whole tag, and never animate tg.box itself: the scene re-adds the box above its
    own word and the filled box hides the word for good (L09 trap, seen again in L10 S01)."""
    color = color or tg.text.get_color()
    edge = tg.box.copy().set_fill(opacity=0)
    scene.play(Indicate(tg.text, color=color, scale_factor=scale),
               edge.animate(rate_func=there_and_back).set_stroke(width=4), *extra, run_time=run_time)
    scene.remove(edge)


def each(pieces, color, scale: float = 1.1, lag: float = 0.15):
    """Animation: flash scattered pieces one by one (one Indicate on their group would scale them
    about the group's centre and pull glyphs off their rows)."""
    return LaggedStart(*[Indicate(p, color=color, scale_factor=scale) for p in pieces], lag_ratio=lag)


def under(g, color, stroke: float = 4, pad: float = 0.03, y: float | None = None) -> Line:
    """A line under glyphs `g`."""
    y = g.get_bottom()[1] - 0.06 if y is None else y
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def hl_bar(g, color=TURN, opacity: float = 0.25, buff: float = 0.05) -> Rectangle:
    """A translucent bar behind glyphs `g` (insert it behind: row.submobjects.insert(0, bar))."""
    return Rectangle(width=g.width + 2 * buff, height=g.height + 2 * buff, stroke_width=0) \
        .set_fill(color, opacity).move_to(g)


def ring(g, color=TURN, buff: float = 0.08, stroke: float = 3, dashed: bool = False):
    """An outline box around `g` (hides nothing: fine over terminal text); dashed=True for the
    'container's view' / 'no pass' rings."""
    r = RoundedRectangle(width=g.width + 2 * buff, height=g.height + 2 * buff,
                         corner_radius=0.08, stroke_color=color, stroke_width=stroke).move_to(g)
    if dashed:
        d = DashedVMobject(r, num_dashes=max(12, int((r.width + r.height) * 7)), dashed_ratio=0.55)
        return d.set_stroke(color, stroke)
    return r


def strike(g, color=ERR, stroke: float = 4) -> Line:
    """A strike-through line over `g`."""
    return Line(g.get_left() + LEFT * 0.06, g.get_right() + RIGHT * 0.06, color=color, stroke_width=stroke)




# ------------------------------------------------------------------ tags and chips (>= 20 pt)
_AMOUNT_RE = re.compile(r"[$€£¢]|\d\s*(cents?|dollars?|USD)\b", re.I)


def _no_amount(s: str) -> str:
    """Cost text never carries a money amount (sizes like '3.8 MB' are fine; amounts are not)."""
    if _AMOUNT_RE.search(s):
        raise ValueError(f"cost tag {s!r}: no money amounts on screen ('a fraction of a cent a month')")
    return s


def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag (house size: beside a card or panel, not inside a terminal row)."""
    return tag("▶ your turn", TURN)


def extra_tag(kind: str | None = None) -> VGroup:
    """GREY 'extra' tag; kind 'Linux' / 'stand-in' / 'local remote' -> 'extra · Linux' …"""
    return tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def standin_tag() -> VGroup:
    """'extra · stand-in': Label Studio's clicks replayed as its API calls (23, 24, 27, 28, 30-33,
    43), the photo copies (94, 103), the time travel on the stand-in folder (114-117)."""
    return extra_tag("stand-in")


def local_tag() -> VGroup:
    """'extra · local remote': dvc push -r standin (95, 104)."""
    return extra_tag("local remote")


def stand_in_label() -> VGroup:
    """The plain GREY 'stand-in' tag (S03: the key in 06, 'explained in scene 5')."""
    return tag("stand-in", S.GREY)


def illustration_tag(s: str = "illustration") -> VGroup:
    """On every console step, Label Studio screen, GitHub form, notebook frame, the hook's folders and
    invented file names, S11's working two-view and the drawn dvc_store/ (schematic; no screenshots)."""
    return tag(s, S.GREY)


def recorded_tag(s: str = "recorded") -> VGroup:
    """On every success a student sees that this machine could not produce; name the source:
    recorded_tag('recorded · cli.py:40 + :26–33')."""
    return tag(s, S.GREY)


def recording_tag(s: str = "at the time of recording") -> VGroup:
    """Beside versions and image sizes when first shown (never on md5s, sizes or counts of the photos:
    those are 'same bytes, same fingerprint')."""
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    """On every README/repo slip (the narration says 'a small slip' or 'a small gap')."""
    return tag(s, S.GREY)


def preview_tag(s: str = "preview") -> VGroup:
    return tag(s, S.GREY)


def editor_tag(s: str = "our editor; use yours") -> VGroup:
    """The sed edits of 40/85/87."""
    return tag(s, S.GREY)


def cost_tag(s: str = "storage: a fraction of a cent a month") -> VGroup:
    """The GOLD money tag: S01 (checklist), S03 (bucket 1), S10 (images/), S13 (dvc_store/), S16's
    card. Text says sizes and 'a fraction of a cent a month', never an amount (raises on '$', 'cents')."""
    return tag(_no_amount(s), COST)


def grey_chip(s: str, size: float = 20, mono_font: bool = False, color=S.GREY) -> VGroup:
    """A GREY chip for a short note. .box .text"""
    return chip(s, color, size=size, font=MONO if mono_font else None)


def dashed_chip(s: str, color=FUTURE, size: float = 20, mono_font: bool = False) -> VGroup:
    """A dashed chip: future/elsewhere things (L13, lakeFS, monitoring, the class bucket). .box .text"""
    t = mono(s, size, color) if mono_font else label(s, size, color)
    ob = outline_box(t.width + 0.48, mono("|", size).height + 0.24, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def tool_chip(s: str, size: float = 20) -> VGroup:
    """A tool as a PURPLE mono chip (never a logo): docker, git, dvc, gcsfuse, gcloud, uv …"""
    return chip(s, TOOL, size=size, font=MONO)


def err_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """A RED error chip: err_chip('401'), err_chip('Exited (1)'). .box .text"""
    return chip(s, ERR, size=size, font=MONO if mono_font else None, fill_opacity=0.14)


def fake_chip() -> VGroup:
    """GREY 'obviously fake' (beside student-demo-token-not-a-secret)."""
    return grey_chip("obviously fake")


def differ_chip(s: str = "yours will differ") -> VGroup:
    """GREY chip for container ids, image ids and our commit hashes (never read aloud)."""
    return grey_chip(s)


def file_card(path: str, color=LAPTOP, size: float = 20, dashed: bool = False) -> VGroup:
    """A file as a card: file glyph + mono path. .box .glyph .text"""
    g0 = file_glyph(0.34, color)
    t = mono(path, size, INK)
    row = VGroup(g0, t).arrange(RIGHT, buff=0.16)
    w, h = row.width + 0.45, row.height + 0.32
    b = outline_box(w, h, color, solid=not dashed, fill_opacity=0.1)
    row.move_to(b)
    g = VGroup(b, row)
    g.box, g.glyph, g.text = b, g0, t
    return g


def card(lines, color=S.GREY, size: float = 22, card_w: float | None = None, dashed: bool = False,
         head: str | None = None, buff: float = 0.16) -> VGroup:
    """A plain card of short lines (label font; an item may be a mobject), e.g. the erratum and
    honest-note cards. head: a GREY first line. .frame .body .head"""
    items = [label(s, size, INK) if isinstance(s, str) else s for s in lines]
    hd = label(head, CAPTION, S.GREY) if head else None
    body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=buff)
    inner = VGroup(*([hd] if hd else []), body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    w = card_w or inner.width + 0.6
    frame = outline_box(w, inner.height + 0.5, color, solid=not dashed, fill_opacity=0.08)
    if not dashed:
        frame.fill.set_fill(S.GREY_DARKER, 1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    g = VGroup(frame, inner)
    g.frame, g.body, g.head = frame, body, hd
    return g


def strip_head(call: str) -> VGroup:
    """The heading of an output-only stand-in strip (script conventions): GREY mono
    'POST /api/storages/gcs/validate · stand-in' — place it on the strip's title bar or above it."""
    return mono(call, 20, S.GREY)


def ponder(scene, question: str, seconds: float = 8, quick: bool = False, center=None,
           width: float = 9.5) -> VGroup:
    """Plays a PONDER card (timer drains over `seconds`); quick=True is the script's QUICK(4 s):
    the header says 'Quick predict'. center=(x, y) moves the card (default: the frame's centre).
    Returns the card (still on screen): FadeOut it at the start of the next block."""
    c = ponder_card(question, width=width)
    if quick:
        hd = c[1]
        new = S.text("Quick predict", S.SMALL_SIZE, TURN, weight="BOLD").move_to(hd)
        c.remove(hd)
        c.submobjects.insert(1, new)
    if center is not None:
        c.move_to([center[0], center[1], 0])
    scene.play(FadeIn(c, scale=0.95), run_time=0.6)
    bar = c[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return c


def quick_predict(scene, question: str, seconds: float = 4, **kw) -> VGroup:
    """The script's QUICK(4 s, …): a ponder card headed 'Quick predict'."""
    return ponder(scene, question, seconds, quick=True, **kw)


# ------------------------------------------------------------------ small glyphs and motion
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


def arrow(a, b, color=S.GREY, stroke: float = 3, buff: float = 0.12, arc: float = 0.0) -> Arrow:
    """A plain thin arrow between two mobjects or points (curved by `arc` radians)."""
    pa = a if isinstance(a, np.ndarray) else a.get_center()
    pb = b if isinstance(b, np.ndarray) else b.get_center()
    return Arrow(pa, pb, buff=buff if not isinstance(a, np.ndarray) else 0, color=color, path_arc=arc,
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


def lock_glyph(lock_h: float = 0.32, color=SECRET) -> VGroup:
    """A padlock."""
    w = lock_h * 0.8
    body = RoundedRectangle(width=w, height=lock_h * 0.6, corner_radius=lock_h * 0.08,
                            stroke_color=color, stroke_width=2.5).set_fill(color, 0.3)
    shackle = Arc(radius=w * 0.32, start_angle=0, angle=PI, color=color, stroke_width=3)
    shackle.next_to(body, UP, buff=0)
    return VGroup(shackle, body)


def key_glyph(key_w: float = 0.9, color=KEY) -> VGroup:
    """A key (bow, shaft, two teeth), GREEN: the JSON key's 'something you have'. Lies flat."""
    r = key_w * 0.2
    bow = Circle(radius=r, stroke_color=color, stroke_width=4).set_fill(color, 0.25)
    hole = Circle(radius=r * 0.35, stroke_color=color, stroke_width=3)
    shaft = Line([r, 0, 0], [key_w - r, 0, 0], color=color, stroke_width=5)
    t1 = Line([key_w * 0.62, 0, 0], [key_w * 0.62, -r * 0.8, 0], color=color, stroke_width=5)
    t2 = Line([key_w * 0.78, 0, 0], [key_w * 0.78, -r * 0.6, 0], color=color, stroke_width=5)
    g = VGroup(bow, hole, shaft, t1, t2)
    return g.move_to(ORIGIN)




def house(name: str | None = None, house_w: float = 1.3, house_h: float = 0.85, color=IMAGE,
          lit: bool = False, size: float = 20, dashed: bool = False) -> VGroup:
    """A container as a small house (TEAL): hollow (nothing runs) or lit (running). The name sits
    inside the body (20 pt; keep it <= house_w - 0.25 wide). .body .roof .text ; base at y=0 of
    its own frame: place with .move_to(point, aligned_edge=DOWN)."""
    roof_h = house_h * 0.36
    bw, bh = house_w, house_h - roof_h
    bd = Rectangle(width=bw, height=bh).move_to([0, bh / 2, 0])
    rf = Polygon([-bw / 2 - 0.08, bh, 0], [0, house_h, 0], [bw / 2 + 0.08, bh, 0])
    for m in (bd, rf):
        m.set_stroke(color, 3)
        if lit:
            m.set_fill(color, 0.3)
        else:
            m.set_fill(S.BG, 1)
    if dashed:
        bd = DashedVMobject(bd, num_dashes=24).set_stroke(color, 3)
        rf = DashedVMobject(rf, num_dashes=14).set_stroke(color, 3)
    g = VGroup(bd, rf)
    t = None
    if name:
        t = label(name, size, INK if lit else color).move_to([0, bh / 2, 0])
        g.add(t)
    g.body, g.roof, g.text, g.lit = bd, rf, t, lit
    return g


def lit_house(h: VGroup, lit: bool = True, color=IMAGE) -> VGroup:
    """A copy of house `h` lit (TEAL fill, WHITE name) or hollow again: Transform(h, lit_house(h))."""
    c = h.copy()
    for m in (c.body, c.roof):
        if lit:
            m.set_fill(color, 0.3)
        else:
            m.set_fill(S.BG, 1)
    if c.text is not None:
        c.text.set_color(INK if lit else color)
    c.lit = lit
    return c


def door_glyph(door_w: float = 0.34, door_h: float = 0.46, color=DOOR) -> VGroup:
    """A door (neutral GREY: an open published port is never GREEN). .frame .knob"""
    fr = Rectangle(width=door_w, height=door_h, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    knob = Dot(fr.get_right() + LEFT * 0.08, radius=0.035, color=color)
    g = VGroup(fr, knob)
    g.frame, g.knob = fr, knob
    return g


def bricks(bw: float = 0.4, bh: float = 0.5, color=S.GREY) -> VGroup:
    """A small brick patch (the 127.0.0.1: narrowing bricks up a door's Wi-Fi side)."""
    out_ = VGroup()
    rows = 4
    rh = bh / rows
    for i in range(rows):
        off = 0 if i % 2 == 0 else bw / 4
        x = -bw / 2 - off
        while x < bw / 2:
            a, b = max(x, -bw / 2), min(x + bw / 2, bw / 2)
            if b - a > 0.02:
                out_.add(Rectangle(width=b - a, height=rh, stroke_color=S.BG, stroke_width=1.5)
                         .set_fill(color, 0.9).move_to([(a + b) / 2, -bh / 2 + rh * (i + 0.5), 0]))
            x += bw / 2
    return out_


def browser_glyph(url: str | None = None, glyph_w: float = 0.9, size: float = 20, color=LAPTOP,
                  name: str | None = "browser", glyph_h: float | None = None) -> VGroup:
    """Your browser as a small window (GREY, no logo) with its name under it (and, when given, its
    address inside: keep it short, mono 20 pt). .window .bar .url .text"""
    h = glyph_w * 0.68
    if url:
        u = mono(url, size, S.GREY)
        glyph_w = max(glyph_w, u.width + 0.4)
        h = max(h, 1.0)
    h = glyph_h or h
    fr = RoundedRectangle(width=glyph_w, height=h, corner_radius=0.08, stroke_color=color,
                          stroke_width=3).set_fill(PANEL, 1)
    bar = Line(fr.get_corner(UL) + DOWN * 0.18, fr.get_corner(UR) + DOWN * 0.18, color=color, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.03, color=color) for _ in range(3)]).arrange(RIGHT, buff=0.05)
    dots.move_to(fr.get_corner(UL) + np.array([0.18, -0.09, 0]))
    win = VGroup(fr, bar, dots)
    g = VGroup(win)
    g.window, g.bar, g.url, g.text = win, bar, None, None
    if url:
        u.move_to(fr).shift(DOWN * 0.05)
        if glyph_h:                                  # a tall page: the address sits at its top
            u.next_to(bar, DOWN, buff=0.12)
        g.add(u)
        g.url = u
    if name:
        t = label(name, size, color).next_to(fr, DOWN, buff=0.1)
        g.add(t)
        g.text = t
    return g



class Rig(VGroup):
    """A set piece whose not-yet-shown parts ('riders': built, not added) follow it when it is
    placed with shift / move_to / next_to / align_to / to_edge before it plays. (An .animate move
    after it is on screen does not carry them: place pieces first.)"""

    def ride(self, *mobs):
        self._riders = getattr(self, "_riders", []) + [m for m in mobs if m is not None]
        return self

    def shift(self, *vectors):
        super().shift(*vectors)
        riders = getattr(self, "_riders", [])
        if riders:
            fam = set(map(id, self.get_family()))
            for m in riders:
                if id(m) not in fam:
                    m.shift(*vectors)
        return self


def _poly(points, color, stroke: float = 3, tip: bool = True, dashed: bool = False) -> VGroup:
    """A polyline route through `points` ending in an arrow tip (a Rig: line + tip are its children,
    so Create draws only what is seen). .path (the whole route, for travel(); an invisible rider that
    follows shift/move_to/next_to of the route or of the piece holding it) .line .tip_arrow"""
    pts = [np.array(p, dtype=float) for p in points]
    path = VMobject(stroke_width=0, stroke_opacity=0, fill_opacity=0).set_points_as_corners(pts)
    line = VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(pts)
    if dashed:
        line = DashedVMobject(line, num_dashes=max(8, int(sum(np.linalg.norm(b - a) for a, b in
                                                            zip(pts, pts[1:])) * 5)))
        line.set_stroke(color, stroke)
    g = Rig(line)
    g.path, g.line, g.tip_arrow = path, line, None
    g.ride(path)
    if tip:
        a, b = pts[-2], pts[-1]
        d = (b - a) / max(1e-6, np.linalg.norm(b - a))
        ta = Arrow(b - d * 0.3, b, buff=0, color=color, stroke_width=stroke, tip_length=0.18,
                   max_tip_length_to_length_ratio=0.9)
        g.add(ta)
        g.tip_arrow = ta
    return g


def greyed(m, shape=S.GREY_DARK, text=S.GREY):
    """A copy of `m` greyed out (shapes GREY_DARK, texts GREY): Transform(m, greyed(m))."""
    c = m.copy()
    for x in c.get_family():
        if isinstance(x, Text):
            x.set_color(text)
        elif len(x.points):
            x.set_stroke(shape)
            if x.get_fill_opacity() > 0 and x.get_fill_color().to_hex().upper() != S.BG.upper():
                x.set_fill(shape)
    return c



# ------------------------------------------------------------------ L11 glyphs (all text >= 20 pt)
def tile(name: str | None = None, tile_w: float = 0.6, color=LAPTOP, broken: bool = False,
         filled: bool = False, size: float = 20, name_color=INK) -> VGroup:
    """A photo as a blank tile (never a photo): a rounded square with a schematic hill-and-sun mark;
    `name` (mono) under it. broken=True: a RED-free GREY crack and dimmed mark (a thumbnail that did
    not load); filled=True: a light fill (the thumbnail loaded, schematic). .frame .icon .text"""
    fr = RoundedRectangle(width=tile_w, height=tile_w * 0.8, corner_radius=0.06, stroke_color=color,
                          stroke_width=2.5).set_fill(color if filled else S.BG, 0.35 if filled else 1)
    w, h = tile_w, tile_w * 0.8
    hill = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(
        [[-w * 0.38, -h * 0.28, 0], [-w * 0.1, h * 0.05, 0], [w * 0.08, -h * 0.12, 0], [w * 0.38, h * 0.18, 0]])
    sun = Circle(radius=w * 0.08, stroke_color=color, stroke_width=2).move_to([-w * 0.18, h * 0.22, 0])
    icon = VGroup(hill, sun)
    if broken:
        icon.set_stroke(opacity=0.35)
        crack = VMobject(stroke_color=S.GREY, stroke_width=2.5).set_points_as_corners(
            [[w * 0.2, h * 0.4, 0], [w * 0.05, h * 0.1, 0], [w * 0.18, -h * 0.05, 0], [-w * 0.02, -h * 0.4, 0]])
        icon.add(crack)
    g = VGroup(fr, icon)
    g.frame, g.icon, g.text = fr, icon, None
    if name:
        t = mono(name, size, name_color).next_to(fr, DOWN, buff=0.08)
        g.add(t)
        g.text = t
    return g


def annotation(word: str = "gouda", env_w: float = 1.3, env_h: float = 0.8, size: float = 22,
               color=NOTE) -> VGroup:
    """An annotation as a WHITE envelope; the label word is the only text inside. .body .flap .text"""
    body = RoundedRectangle(width=env_w, height=env_h, corner_radius=0.05, stroke_color=color,
                            stroke_width=3).set_fill(S.BG, 1)
    flap = VMobject(stroke_color=color, stroke_width=2.5)
    flap.set_points_as_corners([[-env_w / 2 + 0.03, env_h / 2 - 0.03, 0], [0, env_h / 2 - env_h * 0.4, 0],
                                [env_w / 2 - 0.03, env_h / 2 - 0.03, 0]])
    t = mono(word, size, color).move_to([0, -env_h / 2 + 0.22, 0])
    g = VGroup(body, flap, t)
    g.body, g.flap, g.text = body, flap, t
    return g


def drawer(name: str, color=CLOUD, size: float = 20, drawer_w: float | None = None, glyph: bool = True,
           mono_font: bool = True, dashed: bool = False) -> VGroup:
    """A folder/prefix as a drawer: (folder glyph +) name in a rounded box. .box .glyph .text"""
    t = mono(name, size, INK) if mono_font else label(name, size, INK)
    parts = [t]
    gl = None
    if glyph:
        gl = folder_glyph(0.26, color)
        parts = [gl, t]
    row = VGroup(*parts).arrange(RIGHT, buff=0.14)
    w = drawer_w or row.width + 0.36
    h = 0.44
    b = outline_box(w, h, color, solid=not dashed, fill_opacity=0.12, radius=0.08)
    row.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.18)
    g = VGroup(b, row)
    g.box, g.glyph, g.text = b, gl, t
    return g


def vault(title: str, drawers=(), color=CLOUD, size: float = 20, mono_title: bool = True,
          title_bottom: bool = False, vault_w: float | None = None, gap: float = 0.1) -> VGroup:
    """A bucket as a BLUE vault: a titled box with its folder drawers stacked (title on top, or at the
    bottom with title_bottom=True). .frame .title .drawers (dict name -> drawer) .rows"""
    tt = mono(title, size, color) if mono_title else label(title, size, color)
    ds = [drawer(d, color, size) for d in drawers]
    dw = max([d.width for d in ds] + [tt.width]) + 0.0
    ds = [drawer(d, color, size, drawer_w=dw) for d in drawers]
    col = VGroup(*ds).arrange(DOWN, buff=gap) if ds else VGroup()
    items = [col, tt] if title_bottom else [tt, col]
    inner = VGroup(*[m for m in items if len(m.submobjects) or m is tt]).arrange(DOWN, buff=0.14)
    w = vault_w or inner.width + 0.4
    fr = RoundedRectangle(width=w, height=inner.height + 0.32, corner_radius=0.16, stroke_color=color,
                          stroke_width=3).set_fill(color, 0.08)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.title, g.rows = fr, tt, col
    g.drawers = {d: m for d, m in zip(drawers, ds)}
    return g


def hourglass(glass_h: float = 0.42, color=CLOUD) -> VGroup:
    """An hourglass with no value on it (a signed URL is short-lived; no expiry is ever printed)."""
    w = glass_h * 0.62
    top = Polygon([-w / 2, glass_h / 2, 0], [w / 2, glass_h / 2, 0], [0, 0, 0], stroke_color=color,
                  stroke_width=2.5).set_fill(color, 0.25)
    bot = Polygon([-w / 2, -glass_h / 2, 0], [w / 2, -glass_h / 2, 0], [0, 0, 0], stroke_color=color,
                  stroke_width=2.5).set_fill(color, 0.1)
    caps = VGroup(Line([-w * 0.65, glass_h / 2, 0], [w * 0.65, glass_h / 2, 0]),
                  Line([-w * 0.65, -glass_h / 2, 0], [w * 0.65, -glass_h / 2, 0])).set_stroke(color, 3)
    return VGroup(top, bot, caps)


def wax_seal(r: float = 0.16, color=KEY) -> VGroup:
    """A wax seal: 'signed with the key' (GREEN: made with the key; the key itself never travels)."""
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(color, 0.45)
    star = VGroup(*[Line(ORIGIN, r * 0.55 * np.array([np.cos(a), np.sin(a), 0]), color=S.BG, stroke_width=2)
                    for a in np.linspace(0, 2 * PI, 6, endpoint=False)])
    return VGroup(c, star)


def url_ticket(name: str = "Image_1.jpg", size: float = 20, color=CLOUD) -> VGroup:
    """The pre-signed URL as a BLUE ticket: an hourglass (short-lived, no value), the photo's name,
    a wax seal (signed with the key). .frame .glass .text .seal"""
    t = mono(name, size, INK)
    gl = hourglass(0.38, color)
    se = wax_seal(0.16)
    row = VGroup(gl, t, se).arrange(RIGHT, buff=0.2)
    fr = RoundedRectangle(width=row.width + 0.5, height=0.62, corner_radius=0.08, stroke_color=color,
                          stroke_width=3).set_fill(color, 0.18)
    notches = VGroup(*[Dot(fr.get_edge_center(d), radius=0.08, color=S.BG) for d in (LEFT, RIGHT)])
    row.move_to(fr)
    g = VGroup(fr, notches, row)
    g.frame, g.glass, g.text, g.seal = fr, gl, t, se
    return g


def bouncer(fig_h: float = 0.75, color=S.GREY) -> VGroup:
    """CORS's bouncer (GREY, neutral: a browser rule, not access control): a figure with a rope post."""
    p = person_icon(color, fig_h)
    post = VGroup(Line([0, 0, 0], [0, fig_h * 0.7, 0], color=color, stroke_width=4),
                  Dot([0, fig_h * 0.7, 0], radius=0.05, color=color))
    post.next_to(p, RIGHT, buff=0.12).align_to(p, DOWN)
    return VGroup(p, post)


def stopwatch(word: str = "started", r: float = 0.24, color=S.GREY, size: float = 20) -> VGroup:
    """A stopwatch with a word under it (S08: depends_on reads 'started', not 'ready'). .dial .text"""
    dial = Circle(radius=r, stroke_color=color, stroke_width=3)
    knob = Line([0, r, 0], [0, r + 0.08, 0], color=color, stroke_width=4)
    hand = Line(ORIGIN, [r * 0.55, r * 0.45, 0], color=color, stroke_width=3)
    w = VGroup(dial, knob, hand)
    t = label(word, size, color).next_to(w, DOWN, buff=0.08)
    g = VGroup(w, t)
    g.dial, g.text = w, t
    return g


def flag(name: str = "dataset_v20", color=POINTER, pole_h: float = 0.75, size: float = 20,
         dashed: bool = False) -> VGroup:
    """A tag as a flag: pole, pennant, mono name right of the pennant (GREEN: your repo owns it;
    dashed GREY for a flag that was never planted). Its base is the pole's foot: place with
    .move_to(point, aligned_edge=DL) then shift left by the pole (or use flag_at()). .pole .pennant .text"""
    pole = Line([0, 0, 0], [0, pole_h, 0], color=color, stroke_width=3)
    pen = Polygon([0, pole_h, 0], [0.42, pole_h - 0.14, 0], [0, pole_h - 0.28, 0], stroke_color=color,
                  stroke_width=2.5).set_fill(color, 0.0 if dashed else 0.45)
    if dashed:
        pole = DashedLine([0, 0, 0], [0, pole_h, 0], color=color, stroke_width=3)
        pen = DashedVMobject(pen, num_dashes=10).set_stroke(color, 2.5)
    t = mono(name, size, color).next_to(pen, RIGHT, buff=0.1).align_to(pen, UP).shift(UP * 0.04)
    g = VGroup(pole, pen, t)
    g.pole, g.pennant, g.text = pole, pen, t
    return g


def flag_at(f: VGroup, point) -> VGroup:
    """Stand flag `f` with its pole's foot at `point`."""
    return f.shift(np.array(point) - f.pole.get_start())


def bead(r: float = 0.15, color=S.GREY) -> Circle:
    """A commit on the git line."""
    return Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)


def sticky(s: str, color=S.GREY, size: float = 20) -> VGroup:
    """A small sticky note (a -e line stuck on a house): a card with a folded corner. .frame .text"""
    t = label(s, size, INK)
    w, h = t.width + 0.36, t.height + 0.26
    fr = Polygon([-w / 2, h / 2, 0], [w / 2 - 0.12, h / 2, 0], [w / 2, h / 2 - 0.12, 0], [w / 2, -h / 2, 0],
                 [-w / 2, -h / 2, 0], stroke_color=color, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def slip(s: str, color=HASH, size: float = 20) -> VGroup:
    """An md5 (or a shelf path) as a small PINK slip: mono text in a thin rounded box. .box .text"""
    t = mono(s, size, color)
    b = RoundedRectangle(width=t.width + 0.24, height=t.height + 0.18, corner_radius=0.06, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def machine(word: str = "md5", m_w: float = 1.3, m_h: float = 1.1, color=TOOL, size: float = 24) -> VGroup:
    """The hash machine (a tool: PURPLE): a box with a hopper on top and a chute on the right.
    .frame .text .mouth (top point) .chute (right point)"""
    fr = RoundedRectangle(width=m_w, height=m_h, corner_radius=0.12, stroke_color=color,
                          stroke_width=3).set_fill(color, 0.12)
    hop = Polygon([-m_w * 0.35, m_h / 2 + 0.3, 0], [m_w * 0.35, m_h / 2 + 0.3, 0], [m_w * 0.15, m_h / 2, 0],
                  [-m_w * 0.15, m_h / 2, 0], stroke_color=color, stroke_width=3).set_fill(color, 0.08)
    t = mono(word, size, INK).move_to(fr)
    g = VGroup(fr, hop, t)
    g.frame, g.text = fr, t
    g.mouth_pt = Dot([0, m_h / 2 + 0.3, 0], radius=0.001).set_opacity(0)
    g.chute_pt = Dot([m_w / 2, 0, 0], radius=0.001).set_opacity(0)
    g.add(g.mouth_pt, g.chute_pt)
    return g


def task_cards(n: int = 21, card_w: float = 0.32, cols: int = 7, color=S.GREY) -> VGroup:
    """n small blank task cards in a grid (no numbers on them): Sync Storage's tasks."""
    cs = VGroup(*[RoundedRectangle(width=card_w, height=card_w * 0.75, corner_radius=0.04, stroke_color=color,
                                   stroke_width=2).set_fill(S.GREY_DARKER, 1) for _ in range(n)])
    cs.arrange_in_grid(cols=cols, buff=0.08)
    return cs


def window(url: str, win_w: float = 6.0, win_h: float = 3.6, size: float = 20) -> VGroup:
    """A schematic browser/console window (no logo, no screenshot): always tag it `illustration`.
    .frame .address .content (the page rectangle) — browser_window() at 20 pt."""
    return browser_window(url, win_w, win_h, size)


# ------------------------------------------------------------------ set-piece helpers
def pipe(points, color=ROUTE, stroke: float = 4, glow: bool = True, dashed: bool = False) -> VGroup:
    """A mount pipe / tube through `points` (a polyline with a soft glow): GREY for a host folder
    mount, GREEN for ../secrets, PINK for gcsfuse and mount --bind. Create() draws it. .core .glow"""
    pts = [np.array(p, dtype=float) for p in points]
    core = VMobject(stroke_color=color, stroke_width=stroke).set_points_as_corners(pts)
    if dashed:
        n = max(8, int(sum(np.linalg.norm(b - a) for a, b in zip(pts, pts[1:])) * 6))
        core = DashedVMobject(core, num_dashes=n).set_stroke(color, stroke)
    g = VGroup()
    gl = None
    if glow and not dashed:
        gl = core.copy().set_stroke(color, stroke * 3, opacity=0.18)
        g.add(gl)
    g.add(core)
    g.core, g.glow = core, gl
    return g


def roof_y(h: VGroup, x: float) -> float:
    """The y of house h's roof line at x (for a pipe that lands on the roof)."""
    rf = h.roof
    pts = rf.get_vertices() if hasattr(rf, "get_vertices") else rf.points
    left, apex, right = pts[0], pts[1], pts[2]
    if x <= apex[0]:
        f = (x - left[0]) / max(1e-6, apex[0] - left[0])
        return left[1] + f * (apex[1] - left[1])
    f = (x - apex[0]) / max(1e-6, right[0] - apex[0])
    return apex[1] + f * (right[1] - apex[1])


def street(a: float, b: float, y: float, name: str = NETWORK, laid: bool = True, size: float = 20,
           text_x: float | None = None, band_h: float = 0.32) -> VGroup:
    """A Docker network as a street from x=a to x=b at height y: PINK solid when it exists, GREY dashed
    while planned; its name masked on the band (centred, or at text_x). .band .mask .text"""
    w = b - a
    band = (outline_box(w, band_h, ROUTE, solid=True, fill_opacity=0.15) if laid
            else outline_box(w, band_h, S.GREY, solid=False)).move_to([(a + b) / 2, y, 0])
    t = mono(name, size, ROUTE if laid else S.GREY)
    t.move_to([(a + b) / 2 if text_x is None else text_x, y, 0])
    mask = RoundedRectangle(width=t.width + 0.2, height=band_h - 0.04, corner_radius=0.08, stroke_width=0) \
        .set_fill(S.BG, 0.85).move_to(t)
    g = VGroup(band, mask, t)
    g.band, g.mask, g.text = band, mask, t
    return g


def lay_street(st: VGroup, run_time: float = 0.8):
    """Animation: a planned (GREY dashed) street becomes a solid PINK one, in place."""
    a, b, y = st.band.get_left()[0], st.band.get_right()[0], st.band.get_center()[1]
    new = street(a, b, y, st.text.original_text, True, text_x=st.text.get_center()[0],
                 band_h=st.band.height)
    return AnimationGroup(Transform(st.band, new.band), Transform(st.text, new.text), run_time=run_time)


def phone_book(names, size: float = 20) -> VGroup:
    """Docker DNS as the street's phone book: a PINK-edged card 'phone book · Docker DNS' listing
    container names (not added). .head .rows"""
    rows = VGroup(*[mono(n, size, INK) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
    head = label("phone book · Docker DNS", size, ROUTE)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = RoundedRectangle(width=body.width + 0.3, height=body.height + 0.25, corner_radius=0.08,
                          stroke_color=ROUTE, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.head, g.rows = head, rows
    return g


def tag_on(mob, s: str, color=S.GREY, direction=UP, buff: float = 0.1) -> VGroup:
    """A house-size tag placed next to `mob` (not added)."""
    return tag(s, color).next_to(mob, direction, buff=buff)


# ================================================================== V1 · StationMap (slide 13, flag by flag)
class StationMap(Rig):
    """V1 · Label Studio in a box, assembled flag by flag (S04 build, S06/S07 the CLI house and the
    two addresses, S08 compose). 12.6 × 3.9, built centred at (0, 0.75) — exactly the band above a
    3-row strip (y -1.2 … 2.7); never scale it. Parts not shown yet are built (riders): FadeIn them
    or use the methods.
      inside the GREY laptop frame ('your laptop', floor bottom-left):
      .street (.band .mask .text; GREY dashed until lay())   .studio  TEAL house data-label-studio
      .cli (data-label-cli, the small house; not added)      .wall (inner wall; door gap under .studio)
      .door (.glyph .text '8080:8080', not added)            .browser (on the floor, not added)
      .db (GREY drawer 'database' = docker-volumes/label-studio, not added)  .secrets (GREEN, not added)
      .pipes['db' | 'secrets' | 'cli'] (not added)            .notes['login' | 'key path'] (not added)
    Animations: lay(), light(k) / darken(k) (k 'studio' | 'cli'), open_door(), pipe_on(k),
    stick(k), tip_over() / stand_up(), alert(color) (the db drawer: ORANGE root-owned, GREY again),
    join_cli(); builders (not added): call(kind) with kind 'browser' (PINK, floor → door → house,
    label localhost:8080), 'name' (PINK, CLI → studio along the street, data-label-studio:8080),
    'local' (the CLI's own localhost arc, refused: .cross RED), phone() (Docker DNS card),
    blanket() (compose file over both houses), order() (depends_on arrow + stopwatch 'started'),
    ghost() (the stopped container: GREY dashed house still holding its name tag).
    Showing together: notes + pipes (S04); calls + phone (S07); blanket + order + ghost (S08)."""

    def __init__(self, laid: bool = False, lit=("studio",), shown=(), size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        L, R, B, T = -6.3, 6.3, -1.95, 1.95
        self.frame = RoundedRectangle(width=R - L, height=T - B, corner_radius=0.2, stroke_color=LAPTOP,
                                      stroke_width=3).set_fill(LAPTOP, 0.04)
        self.header = label("your laptop", size, LAPTOP).move_to([L + 0.2, B + 0.25, 0], aligned_edge=LEFT)
        sy = -0.35
        self.street = street(-6.0, 5.9, sy, NETWORK, laid, size, text_x=3.85)
        base = sy + 0.16
        self.studio = house(CONTAINERS["studio"], 2.6, 1.0, lit="studio" in lit).move_to([-3.9, base, 0],
                                                                                       aligned_edge=DOWN)
        self.cli = house(CONTAINERS["cli"], 2.1, 0.85, lit="cli" in lit).move_to([0.9, base, 0], aligned_edge=DOWN)
        wy, gap = -0.88, 0.46
        dx = -3.9
        self.wall = VGroup(Line([L, wy, 0], [dx - gap / 2, wy, 0], color=S.GREY_DARK, stroke_width=3),
                           Line([dx + gap / 2, wy, 0], [R, wy, 0], color=S.GREY_DARK, stroke_width=3))
        dg = door_glyph(0.36, 0.5).move_to([dx, wy, 0])
        dt = mono("8080:8080", size, DOOR).next_to(dg, LEFT, buff=0.15).shift(DOWN * 0.32)
        self.door = VGroup(dg, dt)
        self.door.glyph, self.door.text = dg, dt
        self.browser = browser_glyph(name="your browser", glyph_w=1.0).move_to([-2.2, -1.42, 0])
        self.browser.text.next_to(self.browser.window, RIGHT, buff=0.15)
        # top band: the two host folders and their pipes
        self.db = drawer("database", LAPTOP, size, mono_font=False).move_to([-4.4, 1.55, 0])
        self.secrets = drawer("secrets/", KEY, size).move_to([-1.2, 1.55, 0])
        sb = self.secrets.get_bottom()[1]
        x1 = self.studio.roof.get_vertices()[2][0] - 0.3
        self.pipes = {
            "db": pipe([[-4.4, self.db.get_bottom()[1], 0], [-4.4, roof_y(self.studio, -4.4), 0]], LAPTOP),
            "secrets": pipe([[-1.6, sb, 0], [-1.6, 1.0, 0], [x1, 1.0, 0], [x1, roof_y(self.studio, x1), 0]], KEY),
            "cli": pipe([[-0.8, sb, 0], [-0.8, 1.0, 0], [0.5, 1.0, 0], [0.5, roof_y(self.cli, 0.5), 0]], KEY),
        }
        n1, n2 = sticky("login"), sticky("key path")
        n1.move_to([-1.75, 0.5, 0]).rotate(0.06)
        n2.move_to([-1.55, 0.02, 0]).rotate(-0.05)
        self.notes = {"login": n1, "key path": n2}
        self.add(self.frame, self.header, self.street, self.wall, self.studio)
        for k in shown:
            self.add(getattr(self, k))
        self.ride(self.cli, self.door, self.browser, self.db, self.secrets, *self.pipes.values(),
                  *self.notes.values())
        self.shift(UP * 0.75)

    # ---- state changes (Animations)
    def lay(self, run_time: float = 0.8):
        """Animation: the street (data-labeling-network) becomes solid PINK."""
        return lay_street(self.street, run_time)

    def _h(self, k):
        return self.studio if k == "studio" else self.cli

    def light(self, k: str = "studio", run_time: float = 0.6):
        """Animation: house k ('studio' | 'cli') lights TEAL (its container runs)."""
        h = self._h(k)
        return Transform(h, lit_house(h, True), run_time=run_time)

    def darken(self, k: str = "studio", run_time: float = 0.6):
        h = self._h(k)
        return Transform(h, lit_house(h, False), run_time=run_time)

    def open_door(self, run_time: float = 0.6):
        """Animation: the door is cut into the wall and its '8080:8080' label appears."""
        return AnimationGroup(FadeIn(self.door.glyph, scale=0.6), FadeIn(self.door.text, shift=UP * 0.1),
                              run_time=run_time)

    def pipe_on(self, k: str, run_time: float = 0.8):
        """Animation: drawer k ('db' GREY, 'secrets' GREEN) appears and its pipe into the house draws
        ('cli': the secrets pipe into the CLI house; the drawer must be on screen)."""
        p = self.pipes[k]
        if k == "cli":
            return Create(p, run_time=run_time)
        d = self.db if k == "db" else self.secrets
        return Succession(FadeIn(d, shift=DOWN * 0.1, run_time=run_time * 0.4), Create(p, run_time=run_time * 0.6))

    def stick(self, k: str, run_time: float = 0.5):
        """Animation: a -e note ('login' | 'key path') sticks on."""
        return FadeIn(self.notes[k], scale=1.3, run_time=run_time)

    def tip_over(self, run_time: float = 0.8):
        """Animation: the Label Studio house tips over (Exited (1)): it leans and greys."""
        h = self.studio
        self._pivot = h.body.get_corner(DR).copy()
        return AnimationGroup(Rotate(h, angle=-0.45, about_point=self._pivot), run_time=run_time)

    def stand_up(self, run_time: float = 0.8):
        """Animation: the house stands again (after the chown fix)."""
        return Rotate(self.studio, angle=0.45, about_point=self._pivot, run_time=run_time)

    def alert(self, color=ROOT, run_time: float = 0.6):
        """Animation: the db drawer (and its pipe) turns `color` (ORANGE: root-owned; LAPTOP: fixed)."""
        return AnimationGroup(self.db.box.animate.set_stroke(color).set_fill(color),
                              self.db.glyph.animate.set_color(color),
                              self.pipes["db"].core.animate.set_stroke(color), run_time=run_time)

    def join_cli(self, run_time: float = 0.8):
        """Animation: the CLI house moves onto the street from the right."""
        return FadeIn(self.cli, shift=LEFT * 0.8, run_time=run_time)

    # ---- builders (not added)
    def call(self, kind: str) -> VGroup:
        """'browser': PINK route browser → door → studio, label 'localhost:8080' (.label);
        'name': PINK route CLI → studio along the street, label 'data-label-studio:8080';
        'local': the CLI's own localhost arc curling back into its house, label 'localhost:8080'
        and a RED cross (.cross, not in the group: FadeIn it when the call is refused)."""
        s = self.size
        if kind == "browser":
            d = self.door.glyph
            w = self.browser.window
            g = _poly([w.get_top() + UP * 0.05, [w.get_center()[0], d.get_center()[1] - 0.05, 0],
                       [d.get_center()[0] + 0.05, d.get_center()[1] - 0.05, 0],
                       [d.get_center()[0], self.studio.body.get_bottom()[1] + 0.05, 0]], ROUTE, 4)
            g.label = mono("localhost:8080", s, ROUTE).next_to(w, DOWN, buff=0.08).align_to(w, LEFT)
            g.label.next_to(self.browser.text, RIGHT, buff=0.3)
            g.add(g.label)
            return g
        if kind == "name":
            y = self.street.band.get_center()[1]
            a = [self.cli.body.get_left()[0] - 0.05, y, 0]
            b = [self.studio.body.get_right()[0] + 0.05, y, 0]
            g = _poly([a, b], ROUTE, 4)
            g.label = mono("data-label-studio:8080", s, ROUTE).move_to(
                [(a[0] + b[0]) / 2, self.wall[1].get_center()[1] + 0.2, 0])
            g.add(g.label)
            return g
        if kind == "local":
            c = self.cli.roof.get_top()
            arc = Arc(radius=0.32, start_angle=-PI / 2 + 0.6, angle=2 * PI - 1.2, color=ROUTE, stroke_width=4)
            arc.add_tip(tip_length=0.16, tip_width=0.16)
            arc.move_to(c + UP * 0.42)
            g = VGroup(arc)
            g.label = mono("localhost:8080", s, ROUTE).next_to(arc, RIGHT, buff=0.15)
            g.add(g.label)
            g.cross = cross_mark(0.36, ERR).move_to(arc)
            g.path = arc
            return g
        raise ValueError(kind)

    def phone(self) -> VGroup:
        """Docker DNS: the street's phone book (both container names), at the street's right end."""
        pb = phone_book([CONTAINERS["studio"], CONTAINERS["cli"]], self.size)
        return pb.next_to(self.street.band, UP, buff=0.12).align_to(self.street.band, RIGHT).shift(LEFT * 0.1)

    def blanket(self) -> VGroup:
        """The compose file draped over both houses: a GREY dashed outline + 'docker-compose.yml'."""
        both = VGroup(self.studio, self.cli)
        ob = outline_box(both.width + 0.5, both.height + 0.35, S.GREY, solid=False).move_to(both)
        t = mono("docker-compose.yml", self.size, S.GREY).next_to(ob, RIGHT, buff=0.2).align_to(ob, UP)
        g = VGroup(ob, t)
        g.box, g.text = ob, t
        return g

    def order(self) -> VGroup:
        """depends_on as an order arrow (CLI → studio, over the roofs) and a stopwatch reading
        'started' (not 'ready'). .arrow .watch"""
        a = self.cli.roof.get_top() + UP * 0.1
        b = self.studio.roof.get_top() + UP * 0.1
        ar = Arrow(a, b, buff=0, path_arc=0.5, color=S.GREY, stroke_width=3, tip_length=0.18)
        w = stopwatch("started", size=self.size).next_to(self.cli, RIGHT, buff=0.4).shift(UP * 0.3)
        g = VGroup(ar, w)
        g.arrow, g.watch = ar, w
        return g

    def ghost(self) -> VGroup:
        """The stopped container still holding its name: a GREY dashed house with a name tag, where
        the studio house stands."""
        h = house(None, 2.6, 1.0, color=S.GREY, dashed=True).move_to(self.studio, aligned_edge=DOWN)
        t = tag(CONTAINERS["studio"], S.GREY).next_to(h, UP, buff=0.05)
        g = VGroup(h, t)
        g.house, g.tag = h, t
        return g


# ================================================================== V2 · SignedTicket (who touches the bytes)
class SignedTicket(Rig):
    """V2 · who touches the photo bytes (S05 list → ticket → vault door; S07 the label envelope).
    12.6 × 3.95, built centred at (0, 0.75) (the band above a 3-row strip). Three actors: inside the
    GREY laptop (left) the TEAL Label Studio house holding the GREEN key (.studio, .key), its GREY
    'database' drawer (.db) and, on the floor, your browser (.browser) with the GREY bouncer at its
    door (.bouncer, not added: V3 teaser); right, the BLUE vault cheese-app-data-demo (.vault:
    .frame .title .drawers['cheeses_unlabeled/' | 'cheeses_labeled/']) with its own door at the
    bottom-left (.door) and the address 'https://storage.googleapis.com' under it (.host).
    Methods (all 'plays' unless they return an Animation):
      reach(scene)              the key reaches into the vault (GREY arrow; .reach_arrow), the
                                unlabeled drawer flashes; returns the arrow (on screen)
      cards(n=21) -> VGroup     n blank task cards fanned out over the floor (not added)
      fan(cards) -> Animation   the cards fly out of the unlabeled drawer to their places
      hand() -> VGroup          the browser's ask: a GREY bubble 'task 1?' over the browser (not added)
      relay() -> VGroup         the dashed GREY relay route vault → house → browser and a GREY strike
                                (.route .strike; not added: Create the route, then the strike)
      stamp(scene)              a BLUE url_ticket appears at the house (the seal stamps on) and
                                slides to the browser; the key stays; returns the ticket
      walk(scene, ticket)       the ticket rides a PINK route to the vault's door; the seal is
                                checked (GREEN check); a blank tile rides back and bounces off the
                                bouncer (FadeIn the bouncer first); returns (route, tile, check)
      envelope_to_db(scene, word='gouda')   S07: a WHITE envelope leaves the house and stops at the
                                db drawer; returns it
      copy_out(scene, env)      S07: a copy flies on into cheeses_labeled/; a thin WHITE thread ties
                                it to a tile in cheeses_unlabeled/ (the photo never moved);
                                returns (copy, thread, photo_tile)"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        L, R, B, T = -6.3, 0.55, -1.95, 1.95
        self.frame = RoundedRectangle(width=R - L, height=T - B, corner_radius=0.2, stroke_color=LAPTOP,
                                      stroke_width=3).set_fill(LAPTOP, 0.04).move_to([(L + R) / 2, 0, 0])
        self.header = label("your laptop", size, LAPTOP).move_to([L + 0.2, B + 0.25, 0], aligned_edge=LEFT)
        self.studio = house(CONTAINERS["studio"], 2.6, 1.0, lit=True).move_to([-3.75, 0.55, 0], aligned_edge=DOWN)
        self.key = key_glyph(0.85).next_to(self.studio, LEFT, buff=0.25).shift(DOWN * 0.15)
        self.db = drawer("database", LAPTOP, size, mono_font=False).move_to([-1.1, 1.55, 0])
        self.browser = browser_glyph(name="your browser", glyph_w=1.2).move_to([-4.6, -1.15, 0])
        self.bouncer = bouncer(0.7).next_to(self.browser.window, RIGHT, buff=0.3).align_to(self.browser.window, DOWN)
        self.vault = vault(BUCKET1, ("cheeses_unlabeled/", "cheeses_labeled/"), CLOUD, size)
        self.vault.move_to([3.55, 0.45, 0])
        d = door_glyph(0.36, 0.5, CLOUD)
        d.move_to(self.vault.frame.get_corner(DL) + np.array([0.45, 0.3, 0]))
        self.door = d
        self.host = mono(STORAGE_HOST, size, CLOUD).next_to(self.vault.frame, DOWN, buff=0.15)
        self.host.align_to(self.vault.frame, RIGHT)
        self.add(self.frame, self.header, self.studio, self.key, self.db, self.browser, self.vault, self.door,
                 self.host)
        self.ride(self.bouncer)
        self.shift(UP * 0.75)

    def reach(self, scene, run_time: float = 1.2):
        a = self.studio.body.get_right() + RIGHT * 0.1 + UP * 0.1
        b = self.vault.frame.get_left() + LEFT * 0.08 + UP * 0.35
        ar = arrow(a, b, S.GREY, buff=0)
        k = self.key.copy()
        scene.play(Create(ar), run_time=run_time * 0.4)
        scene.play(bounce(k, b + LEFT * 0.5, run_time * 0.6),
                   Indicate(self.vault.drawers["cheeses_unlabeled/"].text, color=CLOUD, scale_factor=1.06))
        scene.remove(k)
        self.reach_arrow = ar
        return ar

    def cards(self, n: int = 21) -> VGroup:
        cs = task_cards(n, 0.3, 7)
        return cs.move_to([-1.35, 0.25 + 0.75, 0])

    def fan(self, cs: VGroup, run_time: float = 1.2):
        src = self.vault.drawers["cheeses_unlabeled/"].get_center()
        return LaggedStart(*[FadeIn(c, target_position=src, scale=0.5) for c in cs], lag_ratio=0.04,
                           run_time=run_time)

    def hand(self) -> VGroup:
        t = label("task 1?", self.size, INK)
        b = RoundedRectangle(width=t.width + 0.35, height=t.height + 0.25, corner_radius=0.12,
                             stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        t.move_to(b)
        g = VGroup(b, t).next_to(self.browser.window, UP, buff=0.15)
        g.text = t
        return g

    def relay(self) -> VGroup:
        v = self.vault.frame.get_left() + DOWN * 0.3
        h = self.studio.body.get_right() + DOWN * 0.15
        br = self.browser.window.get_top() + UP * 0.05
        rt = _poly([v, h, [h[0] - 1.3, h[1] - 0.2, 0], br], S.GREY, 3, dashed=True)
        st = Line(rt.line.get_corner(DL) + UP * 0.2, rt.line.get_corner(UR) + DOWN * 0.2, color=S.GREY,
                  stroke_width=5)
        g = VGroup(rt, st)
        g.route, g.strike = rt, st
        return g

    def stamp(self, scene, name: str = "Image_1.jpg"):
        tk = url_ticket(name, self.size).next_to(self.studio, DOWN, buff=0.15).shift(RIGHT * 0.6)
        seal = tk.seal
        scene.play(FadeIn(VGroup(tk.frame, tk[1], tk.glass, tk.text), shift=DOWN * 0.1), run_time=0.5)
        scene.play(FadeIn(seal, scale=2.2), Indicate(self.key, color=KEY, scale_factor=1.15), run_time=0.6)
        tgt = self.browser.window.get_right() + np.array([tk.width / 2 + 0.2, 0.75, 0])
        scene.play(tk.animate.move_to(tgt), run_time=0.9)
        return tk

    def walk(self, scene, ticket):
        w = self.browser.window
        a = w.get_right() + RIGHT * 0.05 + DOWN * 0.15
        dpt = self.door.get_left() + LEFT * 0.05
        rt = _poly([a, [dpt[0] - 0.6, a[1], 0], dpt], ROUTE, 4)
        scene.play(Create(rt), run_time=0.7)
        scene.play(ticket.animate.move_to(dpt + np.array([-ticket.width / 2 - 0.1, 0.45, 0])), run_time=0.9)
        ck = check_mark(0.35, PASS).next_to(ticket.seal, UP, buff=0.08)
        scene.play(Create(ck), Indicate(ticket.seal, color=KEY, scale_factor=1.3), run_time=0.6)
        tl = tile(None, 0.55, LAPTOP).move_to(dpt + LEFT * 0.3)
        scene.play(FadeIn(tl, scale=0.6), run_time=0.3)
        stop = self.bouncer.get_right() + RIGHT * 0.35
        scene.play(MoveAlongPath(tl, Line(tl.get_center(), stop)), run_time=0.9)
        scene.play(tl.animate.shift(RIGHT * 0.35), rate_func=there_and_back, run_time=0.4)
        scene.play(tl.animate.shift(RIGHT * 0.5).set_opacity(0.45), run_time=0.3)
        return rt, tl, ck

    def envelope_to_db(self, scene, word: str = "gouda"):
        env = annotation(word, 1.2, 0.72).move_to(self.studio.body.get_right() + RIGHT * 0.8)
        scene.play(FadeIn(env, scale=0.5), run_time=0.5)
        scene.play(env.animate.next_to(self.db, DOWN, buff=0.1), run_time=0.8)
        return env

    def copy_out(self, scene, env):
        c = env.copy()
        lab = self.vault.drawers["cheeses_labeled/"]
        unl = self.vault.drawers["cheeses_unlabeled/"]
        tgt = lab.box.get_right() + LEFT * (c.width / 2 + 0.12)
        scene.play(c.animate.move_to(tgt + UP * 0.0).set_z_index(5), run_time=1.0)
        ph = tile(None, 0.42, CLOUD).move_to(unl.box.get_right() + LEFT * 0.35)
        th = Line(c.get_top(), ph.get_bottom(), color=NOTE, stroke_width=2)
        scene.play(FadeIn(ph, scale=0.6), run_time=0.3)
        scene.play(Create(th), run_time=0.6)
        return c, th, ph


# ================================================================== V3 · OriginGate (CORS, set on the bucket)
def page_window(url: str = PAGE_ORIGIN, win_w: float | None = None, win_h: float = 2.3, size: float = 20) -> VGroup:
    """A compact schematic page (illustration): a title bar holding the address, an empty page.
    .frame .bar .address .content"""
    a = mono(url, size, S.GREY)
    w = win_w or a.width + 0.9
    fr = RoundedRectangle(width=w, height=win_h, corner_radius=0.12, stroke_color=S.GREY,
                          stroke_width=2.5).set_fill(PANEL, 1)
    bar = Line(fr.get_corner(UL) + DOWN * 0.45, fr.get_corner(UR) + DOWN * 0.45, color=S.GREY, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.04, color=S.GREY) for _ in range(3)]).arrange(RIGHT, buff=0.07)
    dots.move_to(fr.get_corner(UL) + np.array([0.3, -0.225, 0]))
    a.move_to([fr.get_center()[0] + 0.2, fr.get_top()[1] - 0.225, 0])
    content = Rectangle(width=w - 0.3, height=win_h - 0.6, stroke_width=0, fill_opacity=0)
    content.move_to(fr.get_bottom() + UP * (win_h - 0.45) / 2)
    g = VGroup(fr, bar, dots, a)
    g.frame, g.bar, g.address, g.content = fr, bar, a, content
    return g


ORIGIN_PARTS = ("scheme", "host", "port")
CORS_RULE = (("origin", "['*']"), ("method", "['GET']"), ("maxAgeSeconds", "3600"))   # cli.py:26-33
ACAO = "Access-Control-Allow-Origin: *"


class OriginGate(Rig):
    """V3 · CORS, configured on the bucket (S06). ~12.6 × 4.5, built centred at (0, 0.2); fits the
    frame without a terminal (y -2.0 … 2.5). Left island: the page (.page, a page_window at
    http://localhost:8080 with a broken tile .tile) under its origin (.origin_l + chips
    .parts_l['scheme'|'host'|'port']); right island: the BLUE bucket (.bucket, vault
    cheese-app-data-demo with an empty dashed rule slot .slot) under https://storage.googleapis.com
    (.origin_r, .parts_r). The GREY bouncer (.bouncer) stands at the browser's door (the page's
    bottom-right), facing the page; responses travel along .lane (y of the path, under the islands).
      differ() -> Animation          the three chips of each origin light (they all differ)
      deliver(scene, header=False)   a response package rides from the bucket to the bouncer; without
                                     the header: RED cross, it stays out (returns (pkg, cross)); with
                                     it (ACAO tag under the package): GREEN check, the package
                                     enters and the tile fills (returns (pkg, check))
      rule() -> VGroup               the rule card (cli.py:26-33's values; GREEN, not added)
      stick(scene, card)             the card flies into the bucket's slot
      preflight() -> VGroup          a dashed GREY OPTIONS knock page → bucket over the islands' gap,
                                     the GREY tag 'maxAgeSeconds: 3600' clipped on, caption
                                     'preflights only · a plain GET has none' (not added)
      curl_walk(scene)               a GREY curl figure strolls along the bottom, no bouncer at its door
      other_bucket() -> VGroup       Ponder 4: 'your other bucket' (BLUE, not added; bottom right)"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.page = page_window(PAGE_ORIGIN, 4.3, 2.3, size).move_to([-4.15, 0.2, 0])
        self.tile = tile(None, 0.9, S.GREY, broken=True).move_to(self.page.content)
        self.bucket = vault(BUCKET1, (), CLOUD, size, vault_w=4.3)
        slot = outline_box(3.7, 1.25, KEY, solid=False)
        self.bucket.add(slot)
        hdr = self.bucket.title
        self.bucket.frame.stretch_to_fit_height(2.3).move_to([4.15, 0.2, 0])
        hdr.move_to(self.bucket.frame.get_top() + DOWN * 0.3)
        slot.next_to(hdr, DOWN, buff=0.22)
        self.slot = slot
        self.origin_l = mono(PAGE_ORIGIN, size, S.GREY).next_to(self.page, UP, buff=0.65)
        self.origin_r = mono(STORAGE_HOST, size, CLOUD).next_to(self.bucket, UP, buff=0.65)
        self.parts_l = self._parts(self.origin_l)
        self.parts_r = self._parts(self.origin_r)
        self.bouncer = bouncer(0.75).move_to(self.page.frame.get_corner(DR) + np.array([0.55, -0.15, 0]))
        self.bouncer.flip()
        self.lane = self.page.frame.get_bottom()[1] - 0.45
        self.add(self.page, self.tile, self.bucket, self.origin_l, self.origin_r,
                 *self.parts_l.values(), *self.parts_r.values(), self.bouncer)
        self.shift(UP * 0.0)

    def _parts(self, origin):
        cs = VGroup(*[grey_chip(p) for p in ORIGIN_PARTS]).arrange(RIGHT, buff=0.15)
        cs.next_to(origin, DOWN, buff=0.12)
        return {p: c for p, c in zip(ORIGIN_PARTS, cs)}

    def differ(self, run_time: float = 0.8):
        anims = []
        for d in (self.parts_l, self.parts_r):
            for c in d.values():
                anims.append(c.box.animate.set_stroke(TURN).set_fill(TURN, 0.16))
        return AnimationGroup(*anims, run_time=run_time)

    def _pkg(self, header: bool):
        b = RoundedRectangle(width=0.7, height=0.5, corner_radius=0.06, stroke_color=S.GREY,
                             stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        tl = tile(None, 0.36, S.GREY).move_to(b)
        g = VGroup(b, tl)
        g.hdr = None
        if header:
            h = grey_chip(ACAO, mono_font=True, color=PASS).next_to(b, DOWN, buff=0.12)
            g.add(h)
            g.hdr = h
        return g

    def deliver(self, scene, header: bool = False):
        y = self.lane
        start = [self.bucket.frame.get_left()[0] - 0.4, y, 0]
        stop = [self.bouncer.get_right()[0] + 0.55, y, 0]
        pk = self._pkg(header)
        pk.move_to(start, aligned_edge=UP).shift(UP * 0.25)
        scene.play(FadeIn(pk, shift=LEFT * 0.3), run_time=0.4)
        scene.play(pk.animate.shift(RIGHT * (stop[0] - start[0])), run_time=1.2)
        if not header:
            x = cross_mark(0.45, ERR).move_to(pk[0])
            scene.play(Create(x), Indicate(self.bouncer, color=ERR, scale_factor=1.05), run_time=0.6)
            return pk, x
        ck = check_mark(0.4, PASS).next_to(self.bouncer, UP, buff=0.1)
        scene.play(Create(ck), Indicate(pk.hdr.text, color=PASS, scale_factor=1.05), run_time=0.6)
        filled = tile(None, 0.9, S.GREY, filled=True).move_to(self.tile)
        scene.play(pk.animate.move_to(self.tile).set_opacity(0), Transform(self.tile, filled), run_time=0.9)
        scene.remove(pk)
        return pk, ck

    def rule(self) -> VGroup:
        rows = VGroup(*[mono(f"{k}: {v}", self.size, INK, t2c={k: S.GREY}) for k, v in CORS_RULE])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        fr = RoundedRectangle(width=rows.width + 0.4, height=rows.height + 0.25, corner_radius=0.1,
                              stroke_color=KEY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        rows.move_to(fr)
        g = VGroup(fr, rows)
        g.frame, g.rows = fr, rows
        return g.move_to([0, -2.3, 0])

    def stick(self, scene, c: VGroup, run_time: float = 1.0):
        scene.play(c.animate.move_to(self.slot), run_time=run_time)

    def preflight(self) -> VGroup:
        y = self.page.frame.get_top()[1] - 0.6
        a = [self.page.frame.get_right()[0] + 0.1, y, 0]
        b = [self.bucket.frame.get_left()[0] - 0.1, y, 0]
        ln = DashedLine(a, b, color=S.GREY, stroke_width=3).add_tip(tip_length=0.16, tip_width=0.16)
        kn = mono("OPTIONS", self.size, S.GREY).next_to(ln, UP, buff=0.08)
        ma = tag("maxAgeSeconds: 3600", S.GREY).next_to(ln, DOWN, buff=0.1)
        cap = note("preflights only · a plain GET has none").next_to(ma, DOWN, buff=0.1)
        g = VGroup(ln, kn, ma, cap)
        g.line, g.knock, g.max_age, g.caption = ln, kn, ma, cap
        return g

    def curl_walk(self, scene, run_time: float = 2.0):
        fig = VGroup(person_icon(S.GREY, 0.6), mono("curl", self.size, S.GREY)).arrange(RIGHT, buff=0.12)
        y = self.lane - 0.85
        fig.move_to([5.6, y, 0])
        scene.play(FadeIn(fig, shift=LEFT * 0.3), run_time=0.4)
        scene.play(fig.animate.move_to([-1.2, y, 0]), rate_func=linear, run_time=run_time)
        return fig

    def other_bucket(self) -> VGroup:
        v = vault("your other bucket", (), CLOUD, self.size, mono_title=False, vault_w=3.3)
        v.frame.stretch_to_fit_height(1.0)
        v.title.move_to(v.frame)
        return v.move_to([4.4, -2.45, 0])


# ================================================================== V4 · FuseMount (a bucket that looks like a folder)
MOUNT_CHIPS = ("gcsfuse", "--key-file=$GOOGLE_APPLICATION_CREDENTIALS", "$GCS_BUCKET_NAME", "/mnt/gcs_data")


def mount_chips(size: float = 20) -> VGroup:
    """Slide 34's chips over the starter's docker-entrypoint.sh:10 (two hyphens, the full variable
    name): tool PURPLE, key GREEN, bucket BLUE, mount point PINK, plus .implicit, the dashed fifth chip
    '--implicit-dirs' (not passed here; not in the group). Two rows (the key chip alone is 7 wide):
    arrange as you need. .chips (the four, in order) .implicit"""
    cols = (TOOL, KEY, CLOUD, ROUTE)
    cs = VGroup(*[chip(s, c, size=size, font=MONO) for s, c in zip(MOUNT_CHIPS, cols)])
    cs.arrange_in_grid(rows=2, cols=2, buff=(0.25, 0.2), flow_order="rd")
    g = VGroup(cs)
    g.chips = cs
    g.implicit = dashed_chip("--implicit-dirs", S.GREY, size, mono_font=True)
    return g


class FuseMount(Rig):
    """V4 · the entrypoint's four stages (slides 29-32) over the starter's docker-entrypoint.sh 8-13.
    12.6 × 3.55, built centred at (0, 0.75) (the band above a 3-row strip). Top: four stage boxes
    (.stages[i]: .frame .text; 'Authenticate', 'Bucket Mounting', 'Connecting the Application',
    'Using the Data'), GREY until lit. Below: the BLUE bucket (.bucket, the WHOLE bucket: images/ and
    dvc_store/), and the TEAL container outline (.box, 'data-version-cli') holding the GREEN key
    (.key, /secrets), /mnt/gcs_data (.mnt) with its images/ (.mnt_images), /app/cheese_dataset
    (.app) and the PURPLE dvc chip (.dvc, not added). Pipes (not added): .gcsfuse (PINK, bucket →
    /mnt/gcs_data), .bind (PINK, images/ → /app/cheese_dataset) with labels .gcsfuse_label
    .bind_label.
      stage(i) -> Animation      box i lights YELLOW (earlier ones turn GREY-lit, later stay dark)
      authenticate(scene)        the key slides to the gcsfuse pipe's start and back (plays)
      mount() / bind() -> Animation   the pipe draws with its label
      use() -> Animation         the dvc chip sits on /app/cheese_dataset
      fetch(scene)               a request dot runs from dvc up both pipes to the bucket and a blank
                                 tile comes back down to /app/cheese_dataset (plays; returns the tile)
      side_note() -> VGroup      line 8's GREY note 'gcloud's own login · not used by gcsfuse or DVC'
      broken(scene)              S11's replay: the key gets a RED cross, the gcsfuse pipe stops short
                                 (RED dashed, never connects), images/ gets 'special device does not
                                 exist' (RED); returns the marks (plays)
      sign() -> VGroup           the YELLOW sign 'GCS bucket mounted' over /mnt/gcs_data (not added)
      inside_only() -> VGroup    Ponder 7: the pipes' glow copies + GREY label 'the container's own
                                 mounts' (not added)"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        xs = (-4.7, -1.57, 1.57, 4.7)
        self.stages = VGroup()
        for x, s in zip(xs, STAGES_2L):
            t = VGroup(*[label(w, size, S.GREY) for w in s.split("\n")]).arrange(DOWN, buff=0.04)
            fr = RoundedRectangle(width=3.0, height=0.8, corner_radius=0.1, stroke_color=S.GREY_DARK,
                                  stroke_width=2.5).set_fill(S.GREY_DARKER, 1).move_to([x, 1.37, 0])
            t.move_to(fr)
            g = VGroup(fr, t)
            g.frame, g.text = fr, t
            self.stages.add(g)
        # the container and its folders
        self.box = outline_box(12.6, 1.55, IMAGE, solid=False).move_to([0, -0.95, 0])
        self.box_title = mono(CONTAINERS["dvc"], size, IMAGE).move_to(
            self.box.get_corner(UR) + np.array([-0.15, -0.22, 0]), aligned_edge=RIGHT)
        self.key = VGroup(key_glyph(0.8), mono("/secrets", size, KEY)).arrange(DOWN, buff=0.1)
        self.key.move_to([-5.35, -1.05, 0])
        self.mnt = drawer("/mnt/gcs_data", ROUTE, size, glyph=False).move_to([-2.85, -1.25, 0])
        self.mnt_images = drawer("images/", ROUTE, size, glyph=False).next_to(self.mnt, RIGHT, buff=0.08)
        self.app = drawer("/app/cheese_dataset", ROUTE, size, glyph=False).move_to([4.15, -1.25, 0])
        self.dvc = tool_chip("dvc").next_to(self.app, UP, buff=0.12)
        # the bucket, outside the container
        self.bucket = vault("your bucket", ("images/", "dvc_store/"), CLOUD, size, mono_title=False)
        self.bucket.rows.arrange(RIGHT, buff=0.15)
        inner = VGroup(self.bucket.title, self.bucket.rows).arrange(RIGHT, buff=0.3)
        self.bucket.frame.stretch_to_fit_width(inner.width + 0.4).stretch_to_fit_height(0.75)
        inner.move_to(self.bucket.frame)
        self.bucket.move_to([-1.75, 0.25, 0])
        mx = self.mnt.get_center()[0]
        self.gcsfuse = pipe([[mx, self.bucket.frame.get_bottom()[1], 0], [mx, self.mnt.get_top()[1], 0]], ROUTE)
        self.gcsfuse_label = mono("gcsfuse", size, ROUTE).next_to(self.gcsfuse, LEFT, buff=0.15)
        a = self.mnt_images.get_right()
        b = self.app.get_left()
        self.bind = pipe([a + RIGHT * 0.02, b + LEFT * 0.02], ROUTE)
        self.bind_label = mono("mount --bind", size, ROUTE).next_to(self.bind, UP, buff=0.12)
        self.add(self.stages, self.box, self.box_title, self.key, self.mnt, self.mnt_images, self.app, self.bucket)
        self.ride(self.dvc, self.gcsfuse, self.gcsfuse_label, self.bind, self.bind_label)
        self.shift(UP * 0.75)

    def stage(self, i: int, run_time: float = 0.5):
        anims = []
        for j, g in enumerate(self.stages):
            col = TURN if j == i else (S.GREY if j < i else S.GREY_DARK)
            tcol = INK if j == i else S.GREY
            anims.append(g.frame.animate.set_stroke(col))
            anims.append(g.text.animate.set_color(tcol))
        return AnimationGroup(*anims, run_time=run_time)

    def authenticate(self, scene, run_time: float = 1.2):
        k = self.key[0].copy()
        tgt = self.gcsfuse.core.get_center() + LEFT * 0.45
        scene.play(bounce(k, tgt, run_time))
        scene.remove(k)

    def mount(self, run_time: float = 0.9):
        return AnimationGroup(Create(self.gcsfuse), FadeIn(self.gcsfuse_label), run_time=run_time)

    def bind_on(self, run_time: float = 0.9):
        return AnimationGroup(Create(self.bind), FadeIn(self.bind_label), run_time=run_time)

    def use(self, run_time: float = 0.6):
        return FadeIn(self.dvc, shift=DOWN * 0.2, run_time=run_time)

    def fetch(self, scene):
        d = Dot(self.dvc.get_bottom(), radius=0.08, color=ROUTE)
        up = VMobject().set_points_as_corners([self.app.get_left(), self.mnt_images.get_right(),
                                               self.mnt.get_top(), self.bucket.frame.get_bottom()])
        scene.play(FadeIn(d), run_time=0.2)
        scene.play(MoveAlongPath(d, up), run_time=1.2)
        tl = tile(None, 0.42, LAPTOP).move_to(self.bucket.frame.get_bottom())
        down = up.copy().reverse_points()
        scene.play(FadeOut(d), FadeIn(tl), run_time=0.2)
        scene.play(MoveAlongPath(tl, down), run_time=1.2)
        scene.play(tl.animate.move_to(self.app.get_right() + LEFT * 0.35 + UP * 0.45), run_time=0.4)
        return tl

    def side_note(self) -> VGroup:
        return note("gcloud's own login · not used by gcsfuse or DVC").next_to(self.key, UP, buff=0.2) \
            .align_to(self.box, LEFT).shift(RIGHT * 0.2)

    def broken(self, scene):
        x1 = cross_mark(0.45, ERR).move_to(self.key[0])
        mx = self.mnt.get_center()[0]
        top = self.bucket.frame.get_bottom()[1]
        stub = pipe([[mx, top, 0], [mx, top - 0.35, 0]], ERR, glow=False, dashed=True)
        x2 = cross_mark(0.3, ERR).move_to([mx, top - 0.55, 0])
        msg = note("special device does not exist", ERR).next_to(self.mnt_images, DOWN, buff=0.12)
        scene.play(Create(x1), run_time=0.5)
        scene.play(Create(stub), run_time=0.5)
        scene.play(Create(x2), run_time=0.4)
        scene.play(FadeIn(msg, shift=UP * 0.1), Indicate(self.mnt_images.text, color=ERR), run_time=0.6)
        return VGroup(x1, stub, x2, msg)

    def sign(self) -> VGroup:
        t = label("GCS bucket mounted", self.size, TURN)
        b = RoundedRectangle(width=t.width + 0.35, height=t.height + 0.25, corner_radius=0.06, stroke_color=TURN,
                             stroke_width=2.5).set_fill(S.BG, 1)
        t.move_to(b)
        g = VGroup(b, t).next_to(self.mnt, UP, buff=0.18).shift(RIGHT * 0.6)
        g.box, g.text = b, t
        return g

    def inside_only(self) -> VGroup:
        gl = VGroup(*[p.core.copy().set_stroke(ROUTE, 12, opacity=0.35) for p in (self.gcsfuse, self.bind)])
        t = note("the container's own mounts").next_to(self.box, DOWN, buff=0.1).align_to(self.box, RIGHT)
        g = VGroup(gl, t)
        g.glow, g.text = gl, t
        return g


class MountLayers(Rig):
    """V4's pull-back: two bind mounts at two layers (S10's last beat, S11's two-view and Ponder 7,
    S12's stand-in picture). 12.6 × 3.9, built centred at (0, 0.75). The GREY laptop (.laptop) holds,
    left, your repo on disk (.host: 'data-versioning/' with its cheese_dataset/ row, .host_data, GREY
    and dark) and, right, the TEAL container (.box) with the /app window (.app: the repo seen inside,
    with its cheese_dataset/ row .app_data) and /mnt/gcs_data/images (.mnt); the BLUE bucket
    (.bucket, images/) sits outside the laptop, top right.
      .v_pipe (GREY, repo ↔ /app, Docker -v) .v_label 'bind mount · host → container (-v)'
      .inner (PINK, mnt → /app/cheese_dataset, mount --bind) .inner_label 'bind mount · inside the
      container (mount --bind)' .fuse (PINK, bucket → mnt)   — all not added
      light_v() / light_inner() / light_fuse() -> Animation
      absent() -> VGroup        the inner bind drawn GREY dashed (S12: no bucket mounted)
      photos(n=4) -> VGroup     n blank tiles inside /app/cheese_dataset (illustration, not added)
      dark() -> Animation       the host's cheese_dataset/ row dims (empty, as seen from the laptop)"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.laptop = RoundedRectangle(width=9.6, height=3.9, corner_radius=0.2, stroke_color=LAPTOP,
                                       stroke_width=3).set_fill(LAPTOP, 0.04).move_to([-1.5, 0, 0])
        self.header = label("your laptop", size, LAPTOP).move_to(self.laptop.get_corner(DL) + np.array([0.2, 0.25, 0]),
                                                                 aligned_edge=LEFT)
        self.host = self._repo("data-versioning/", LAPTOP).move_to([-4.85, 0.75, 0])
        self.host_data = self.host.rows[1]
        self.box = outline_box(5.6, 3.3, IMAGE, solid=False).move_to([0.45, 0.05, 0])
        self.box_title = mono(CONTAINERS["dvc"], size, IMAGE).move_to(
            self.box.get_corner(UL) + np.array([0.15, -0.25, 0]), aligned_edge=LEFT)
        self.app = self._repo("/app", IMAGE).move_to([-0.35, 0.55, 0])
        self.app_data = self.app.rows[1]
        self.mnt = drawer("/mnt/gcs_data/images", ROUTE, size, glyph=False).move_to([0.45, -1.15, 0])
        self.bucket = vault("your bucket", ("images/",), CLOUD, size, mono_title=False).move_to([5.05, 0.6, 0])
        hy = self.host_data.get_center()[1]
        self.v_pipe = pipe([self.host.frame.get_right() + RIGHT * 0.02 + UP * 0.2,
                            self.app.frame.get_left() + LEFT * 0.02 + UP * 0.2], LAPTOP)
        self.v_label = note("bind mount · host → container (-v)").next_to(self.laptop, UP, buff=0.12) \
            .align_to(self.laptop, LEFT)
        ax = self.app.frame.get_right()[0] + 0.45
        self._inner_pts = [self.mnt.get_right() + RIGHT * 0.02, [ax, self.mnt.get_center()[1], 0],
                           [ax, self.app_data.get_center()[1], 0],
                           [self.app_data.get_right()[0] + 0.05, self.app_data.get_center()[1], 0]]
        self.inner = pipe(self._inner_pts, ROUTE)
        self.inner_label = note("bind mount · inside the container (mount --bind)").next_to(self.laptop, DOWN, buff=0.12) \
            .align_to(self.laptop, LEFT)
        self.fuse = pipe([self.bucket.frame.get_bottom(), [self.bucket.frame.get_center()[0], -1.6, 0],
                          [self.mnt.get_center()[0], -1.6, 0], self.mnt.get_bottom()], ROUTE)
        self._hy = hy
        self.add(self.laptop, self.header, self.host, self.box, self.box_title, self.app, self.mnt, self.bucket)
        self.ride(self.v_pipe, self.v_label, self.inner, self.inner_label, self.fuse)
        self.shift(UP * 0.75)

    def _repo(self, name, color):
        rows = VGroup(drawer(name, color, self.size), drawer("cheese_dataset/", color, self.size))
        rows[1].shift(RIGHT * 0.35)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rows[1].shift(RIGHT * 0.35)
        fr = RoundedRectangle(width=rows.width + 0.4, height=rows.height + 0.35, corner_radius=0.12,
                              stroke_color=color, stroke_width=2).set_fill(S.BG, 0)
        rows.move_to(fr)
        g = VGroup(fr, rows)
        g.frame, g.rows = fr, rows
        return g

    def light_v(self, run_time: float = 0.8):
        return AnimationGroup(Create(self.v_pipe), FadeIn(self.v_label), run_time=run_time)

    def light_inner(self, run_time: float = 0.8):
        return AnimationGroup(Create(self.inner), FadeIn(self.inner_label), run_time=run_time)

    def light_fuse(self, run_time: float = 0.8):
        return Create(self.fuse, run_time=run_time)

    def absent(self) -> VGroup:
        return DashedVMobject(self.inner.core.copy(), num_dashes=30).set_stroke(S.GREY, 3)

    def photos(self, n: int = 4) -> VGroup:
        ts = VGroup(*[tile(None, 0.36, CLOUD) for _ in range(n)]).arrange(RIGHT, buff=0.06)
        return ts.next_to(self.app.frame, DOWN, buff=0.12).align_to(self.app_data, LEFT)

    def dark(self, run_time: float = 0.6):
        return self.host_data.animate(run_time=run_time).fade(0.6)



# ================================================================== V5 · HashShelf (files named by fingerprint)
SHELF_AISLES = tuple(sorted({h[:2] for h in list(MD5.values()) + [V20["md5"], V21["md5"], EMPTY["md5"]]}))
POINTER_KEYS = ("md5", "size", "nfiles")


def pointer_card(md5: str = "", size_: str = "", nfiles: str = "", size: float = 20) -> VGroup:
    """cheese_dataset.dvc as a GREEN card: the six lines of 95:58-63 with md5/size/nfiles as given
    (blank fields are drawn as GREY underscores). .frame .head .lines (6) .fields{'md5'|'size'|'nfiles'}
    (the value Texts, steady() so they morph cleanly)."""
    vals = {"md5": md5, "size": size_, "nfiles": nfiles}
    blanks = {"md5": "________", "size": "______", "nfiles": "_"}
    head = mono("cheese_dataset.dvc", size, POINTER)
    lines, fields = VGroup(), {}
    pitch = line_pitch(size) + 0.02
    for i, raw in enumerate(("outs:", "- md5:", "  size:", "  nfiles:", "  hash: md5", "  path: cheese_dataset")):
        k = raw.strip(" -:")
        row = mono_line(raw, size, INK)
        row.shift(np.array([-row.strut.get_left()[0], -i * pitch - row.strut.get_center()[1], 0]))
        if k in vals:
            v = vals[k] or blanks[k]
            val = steady(v, size, HASH if (k == "md5" and vals[k]) else (INK if vals[k] else S.GREY),
                         mono_font=True)
            val.next_to(row.strut, RIGHT, buff=cell_width(size))
            val.shift(UP * (row.strut.get_center()[1] - val.get_center()[1]))
            row = VGroup(row, val)
            fields[k] = val
        lines.add(row)
    body = VGroup(head, lines).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    fr = RoundedRectangle(width=body.width + 0.5, height=body.height + 0.35, corner_radius=0.12,
                          stroke_color=POINTER, stroke_width=3).set_fill(S.GREY_DARKER, 1)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.head, g.lines, g.fields = fr, head, lines, fields
    return g


def manifest_card(names=IMAGES[:4], size: float = 20, md5s: dict | None = None) -> VGroup:
    """The .dir manifest: one row per photo '{md5, relpath}' (PINK md5 prefix, WHITE name), sorted by
    name. .frame .head .rows .names (dict name -> its name Text) .md5s (dict name -> md5 Text)"""
    md5s = md5s or MD5
    head = label("manifest · the folder's list", size, S.GREY)
    rows, nm, hs = VGroup(), {}, {}
    for n in sorted(names):
        h = steady(short(md5s[n]), size, HASH, mono_font=True)
        t = steady(n, size, INK, mono_font=True)
        r = VGroup(h, t).arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        rows.add(r)
        nm[n], hs[n] = t, h
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    fr = RoundedRectangle(width=body.width + 0.5, height=body.height + 0.35, corner_radius=0.12,
                          stroke_color=HASH, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.head, g.rows, g.names, g.md5s = fr, head, rows, nm, hs
    return g


class HashShelf(Rig):
    """V5 · files named by their fingerprint (S12 as a prediction, S14 the fifth photo, Ponder 8).
    12.6 × 4.0, built in place for the band above a 3-row strip (y -1.25 … 2.7). Left: four tiles
    Image_1-4.jpg (.tiles[name]; .tiles['Image_5.jpg'] waits outside, not added); the PURPLE md5
    machine (.machine); right: the GREY shelf '.dvc/cache' (.rack) with an aisle row per two-character
    prefix (.rows[aisle]: .label (PINK 'xx/'), not added until used) in find|sort order. md5s come
    from laptop/09b; the manifests' from 95/104/93.
      hash_photo(scene, name)     the tile drops into the machine; its PINK md5 slip comes out and a copy
                                  is filed on its aisle (the row appears); returns the slip on the shelf
      manifest() -> VGroup        the manifest card for the four photos (not added; left, where the
                                  tiles were: fade the tiles first)
      hash_manifest(scene, card, predict=True)   the card goes into the machine and comes out as the
                                  PINK '????????….dir' slip on a '??/' row (predict) or as
                                  '89db50de….dir' on 89/; returns the slip
      pointer(predict=True) -> VGroup   the GREEN six-line cheese_dataset.dvc card, fields blank (md5:
                                  '????????….dir'), placed left (not added)
      confirm(scene, card)        95:59-61 confirms: the pointer's fields fill (89db50de….dir, 611101,
                                  4), '??/' becomes 89/ and the slip 'db50de….dir'
      git_box(card) -> VGroup     a GREY box 'git' around the pointer card (not added)
      empty_run(scene)            the machine runs on nothing: a d7/ slip (the empty version, 93:82) is
                                  filed; returns it (RED; recolour GREY later)
      second(scene)               S14: Image_5 → 54081d12… on 54/, the old aisles flash 'already on the
                                  shelf', the v21 manifest 6b342844….dir on 6b/; returns the new slips
      rename(card) -> Animation   Ponder 8: on the manifest card Image_2.jpg becomes brie_2.jpg
    .slips{aisle: [slips]} holds what is on the shelf."""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        ys = (2.2, 1.38, 0.56, -0.26)
        self.tiles = {}
        for n, y in zip(IMAGES[:4], ys):
            self.tiles[n] = tile(n, 0.55, LAPTOP).move_to([-5.4, y, 0])
        self.tiles[IMAGES[4]] = tile(IMAGES[4], 0.55, LAPTOP).move_to([-3.5, -0.26, 0])
        self.machine = machine("md5").move_to([-3.2, 1.75, 0])
        top, bot = 2.6, -1.25
        self.rack = VGroup()
        fr = RoundedRectangle(width=5.05, height=top - bot, corner_radius=0.14, stroke_color=LAPTOP,
                              stroke_width=2.5).set_fill(LAPTOP, 0.05).move_to([3.825, (top + bot) / 2, 0])
        hd = mono(".dvc/cache", size, LAPTOP).move_to(fr.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=LEFT)
        self.rack.add(fr, hd)
        self.rack.frame, self.rack.head = fr, hd
        self.rows, self.slips = {}, {}
        y0 = 1.85
        for i, a in enumerate(SHELF_AISLES):
            y = y0 - i * 0.44
            shelf = Line([1.55, y - 0.2, 0], [6.15, y - 0.2, 0], color=S.GREY_DARK, stroke_width=2)
            lb = steady(a + "/", size, HASH, mono_font=True).move_to([1.95, y, 0])
            r = VGroup(shelf, lb)
            r.label, r.shelf, r.y = lb, shelf, y
            self.rows[a] = r
            self.slips[a] = []
        self.add(*[self.tiles[n] for n in IMAGES[:4]], self.machine, self.rack)
        self.ride(self.tiles[IMAGES[4]], *self.rows.values())

    # ---- helpers
    def _slot(self, a, slip_):
        r = self.rows[a]
        x = 2.45 + sum(s.width + 0.15 for s in self.slips[a])
        return np.array([x + slip_.width / 2, r.label.get_center()[1], 0])

    def _show_row(self, scene, a):
        r = self.rows[a]
        if r not in scene.mobjects and r.label not in scene.mobjects:
            scene.play(FadeIn(r), run_time=0.3)

    def _through(self, scene, mob, run_time: float = 0.6):
        m = self.machine
        scene.play(mob.animate.move_to(m.mouth_pt.get_center() + UP * 0.1).scale(0.5), run_time=run_time)
        scene.play(FadeOut(mob, shift=DOWN * 0.3), Indicate(m.frame, color=TOOL, scale_factor=1.05), run_time=0.4)

    def _file(self, scene, a, text, color=HASH, run_time: float = 0.8):
        """A slip `text` comes out of the chute and is filed on aisle a."""
        out_ = slip(text, color, self.size).move_to(self.machine.chute_pt.get_center() + RIGHT * 1.15)
        scene.play(FadeIn(out_, shift=RIGHT * 0.3), run_time=0.4)
        self._show_row(scene, a)
        tgt = self._slot(a, out_)
        scene.play(out_.animate.move_to(tgt), run_time=run_time)
        self.slips[a].append(out_)
        return out_

    # ---- beats
    def hash_photo(self, scene, name: str):
        t = self.tiles[name]
        self._through(scene, t.copy())
        scene.play(t.animate.fade(0.5), run_time=0.2)
        h = MD5[name]
        s = slip(short(h), HASH, self.size).move_to(self.machine.chute_pt.get_center() + RIGHT * 1.2)
        scene.play(FadeIn(s, shift=RIGHT * 0.3), run_time=0.4)
        a = h[:2]
        self._show_row(scene, a)
        filed = slip(h[2:8] + "…", HASH, self.size)
        filed.move_to(self._slot(a, filed))
        scene.play(ReplacementTransform(s, filed), run_time=0.8)
        self.slips[a].append(filed)
        return filed

    def manifest(self) -> VGroup:
        return manifest_card(IMAGES[:4], self.size).move_to([-4.3, 0.15, 0])

    def hash_manifest(self, scene, card, predict: bool = True):
        c = card.copy()
        scene.play(FadeOut(card), run_time=0.01)
        scene.remove(card)
        self._through(scene, c, 0.9)
        if predict:
            a = V20["md5"][:2]
            r = self.rows[a]
            self._pred_label = r.label
            q = steady("??/", self.size, HASH, mono_font=True).move_to(r.label)
            r.remove(r.label)
            r.add(q)
            r.label = q
            s = self._file(scene, a, "????????….dir")
            self._pred = s
            return s
        return self._file(scene, V20["md5"][:2], V20["md5"][2:8] + "….dir")

    def pointer(self, predict: bool = True) -> VGroup:
        p = pointer_card("????????….dir" if predict else short(V20["md5"]),
                         "" if predict else V20["size"], "" if predict else V20["nfiles"], self.size)
        return p.move_to([-4.2, 0.0, 0])

    def confirm(self, scene, card):
        new = {"md5": short(V20["md5"]), "size": V20["size"], "nfiles": V20["nfiles"]}
        anims = []
        for k, v in new.items():
            f = card.fields[k]
            t = steady(v, self.size, HASH if k == "md5" else INK, mono_font=True).move_to(f, aligned_edge=LEFT)
            anims.append(Transform(f, t))
        r = self.rows[V20["md5"][:2]]
        lb = steady(V20["md5"][:2] + "/", self.size, HASH, mono_font=True).move_to(r.label)
        anims.append(Transform(r.label, lb))
        s = self._pred
        ns = slip(V20["md5"][2:8] + "….dir", HASH, self.size).move_to(s, aligned_edge=LEFT)
        anims.append(Transform(s, ns))
        scene.play(*anims, run_time=1.0)

    def git_box(self, card) -> VGroup:
        ob = outline_box(card.width + 0.5, card.height + 0.75, LAPTOP, solid=True, fill_opacity=0.04)
        ob.move_to(card).shift(DOWN * 0.12)
        t = mono("git", self.size, LAPTOP).move_to(ob.get_corner(UR) + np.array([-0.35, -0.22, 0]))
        g = VGroup(ob, t)
        g.box, g.text = ob, t
        return g

    def empty_run(self, scene):
        m = self.machine
        scene.play(Rotate(m, 0.08, about_point=m.get_bottom()), rate_func=there_and_back, run_time=0.5)
        return self._file(scene, EMPTY["md5"][:2], EMPTY["md5"][2:8] + "….dir", ERR)

    def second(self, scene):
        name = IMAGES[4]
        t = self.tiles[name]
        if t not in scene.mobjects:
            scene.play(FadeIn(t), run_time=0.3)
        new = [self.hash_photo(scene, name)]
        old = [s for n in IMAGES[:4] for s in self.slips[MD5[n][:2]]]
        scene.play(LaggedStart(*[Indicate(s.text, color=PASS, scale_factor=1.1) for s in old], lag_ratio=0.15),
                   run_time=1.0)
        new.append(self._file(scene, V21["md5"][:2], V21["md5"][2:8] + "….dir"))
        return new

    def rename(self, card, new: str = "brie_2.jpg", run_time: float = 0.8):
        f = card.names["Image_2.jpg"]
        t = steady(new, self.size, TURN, mono_font=True).move_to(f, aligned_edge=LEFT)
        return Transform(f, t, run_time=run_time)


# ================================================================== V6 · TagRope (pointer in git, bytes in a bucket)
COMMITS = (("Initial commit", "0e04cc8"), ("Track initial cheese dataset with DVC", "b841355"),
           ("Add images to cheese dataset", "46483f8"))     # laptop/101, 111 (our hashes: 'yours differ')
BEAD_NAMES = ("Initial commit", "v20 commit", "v21 commit")


def blob(h: str, size: float = 20, color=HASH) -> VGroup:
    """One stored file in dvc_store/ (or the cache): a PINK slip with its md5's first 8 characters."""
    return slip(short(h), color, size)


class TagRope(Rig):
    """V6 · the tag → pointer → manifest → blobs rope (S13 build, S14 v21, S15 the pull and its
    failures, S16 recap). 12.6 × 4.0, built in place for the band above a 3-row strip
    (y -1.25 … 2.75). Top left: the git line (.line) with three beads (.beads[0..2]: Initial commit,
    the v20 commit, the v21 commit; .bead_labels) — beads 1 and 2 not added; GREEN flags
    .flags['dataset_v20' | 'dataset_v21'] (not added). Below the v20 bead: the six-line pointer card
    (.card, not added). Right: the BLUE warehouse dvc_store/ (.store: .frame .title) with the
    manifests .dirs['v20' | 'v21'] and the five blobs .blobs[name] (not added).
      bead(i) / plant(tag) -> Animation    a commit appears / a flag plants on its bead
      zoom() -> Animation                  the pointer card grows out of the v20 bead
      rope(v='v20', origin=None) -> VGroup  PINK rope from the card (v20) or the bead (v21) down to
                                  its .dir box, fanning out to its blobs (v21: five, four shared) —
                                  not added: FadeIn the dir/blobs, then Create(rope.main), rope.fans
      hop(tag) -> Animation                a GREY cursor (.cursor) moves onto the flag (S14)
      pull(scene, v='v20')        S15: the BLUE Colab box (.colab) clones at the tag (PINK dot to the
                                  bead), a chip '.dvc/config · which bucket' (.config), the dot visits
                                  the manifest then each blob; n blank tiles appear in Colab
      stop_at_manifest(scene)     the rope reaches the manifest and a RED '401' stops it (C13)
      ghost(tag='dataset_v25') -> VGroup   a dashed GREY flag on no bead, its rope ending in air
      burn() -> Animation                  the warehouse turns GREY dashed, its blobs go (recap Q5)
      homes() -> VGroup           the three homes of the bytes panel (.images .cache .store; not
                                  added; shown alone)
      silhouette() -> VGroup      S09's 2 s GREY sketch: flag → card → rope → bucket (not added)"""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        y = 1.95
        xs = (-5.7, -3.4, -0.75)
        self.line = Line([-6.2, y, 0], [0.2, y, 0], color=S.GREY, stroke_width=3)
        self.beads = VGroup(*[bead().move_to([x, y, 0]) for x in xs])
        self.bead_labels = VGroup(*[note(n).next_to(b, DOWN, buff=0.12) for n, b in zip(BEAD_NAMES, self.beads)])
        self.flags = {}
        for t, b in (("dataset_v20", self.beads[1]), ("dataset_v21", self.beads[2])):
            self.flags[t] = flag_at(flag(t, size=size, pole_h=0.6), b.get_top())
        self.card = pointer_card(short(V20["md5"]), V20["size"], V20["nfiles"], size).move_to([-3.9, -0.15, 0])
        # the warehouse
        fr = RoundedRectangle(width=5.85, height=3.75, corner_radius=0.16, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.07).move_to([3.43, 0.6, 0])
        tt = mono("dvc_store/", size, CLOUD).move_to(fr.get_corner(UL) + np.array([0.2, -0.27, 0]), aligned_edge=LEFT)
        self.store = VGroup(fr, tt)
        self.store.frame, self.store.title = fr, tt
        self.dirs = {"v20": blob(V20["md5"], size).move_to([2.15 + 0.2, 1.45, 0]),
                     "v21": blob(V21["md5"], size).move_to([4.95, 1.45, 0])}
        self.blobs = {}
        pos = [(1.55, 0.2), (3.43, 0.2), (5.31, 0.2), (2.45, -0.75), (4.35, -0.75)]
        for n, (bx, by) in zip(IMAGES, pos):
            self.blobs[n] = blob(MD5[n], size).move_to([bx, by, 0])
        self.cursor = Polygon([0, 0, 0], [-0.14, 0.26, 0], [0.14, 0.26, 0], stroke_color=S.GREY,
                              stroke_width=2).set_fill(S.GREY, 0.8)
        self.colab = self._colab()
        self.config = grey_chip(".dvc/config · which bucket", mono_font=False)
        self.add(self.line, self.beads[0], self.bead_labels[0], self.store)
        self.ride(self.beads[1], self.beads[2], self.bead_labels[1], self.bead_labels[2], *self.flags.values(),
                  self.card, *self.dirs.values(), *self.blobs.values(), self.cursor, self.colab, self.config)

    def _colab(self):
        fr = RoundedRectangle(width=3.4, height=1.7, corner_radius=0.14, stroke_color=CLOUD, stroke_width=3) \
            .set_fill(CLOUD, 0.08)
        t = label("Colab", self.size, CLOUD).move_to(fr.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=LEFT)
        g = VGroup(fr, t).move_to([-4.45, -0.4, 0])
        g.frame, g.text = fr, t
        return g

    def bead(self, i: int, run_time: float = 0.5):
        return AnimationGroup(FadeIn(self.beads[i], scale=0.5), FadeIn(self.bead_labels[i]), run_time=run_time)

    def plant(self, t: str, run_time: float = 0.6):
        f = self.flags[t]
        return AnimationGroup(Create(f.pole), FadeIn(f.pennant, shift=DOWN * 0.15), FadeIn(f.text),
                              run_time=run_time)

    def zoom(self, run_time: float = 0.8):
        return FadeIn(self.card, scale=0.3, target_position=self.beads[1].get_center(), run_time=run_time)

    def rope(self, v: str = "v20", origin=None) -> VGroup:
        d = self.dirs[v]
        if origin is None:
            if v == "v20":
                f = self.card.fields["md5"]
                origin = f.get_right() + RIGHT * 0.1
            else:
                origin = self.beads[2].get_bottom() + DOWN * 0.05
        o = np.array(origin)
        mid = [d.get_left()[0] - 0.35, o[1], 0]
        main = _poly([o, mid, [mid[0], d.get_center()[1], 0], d.get_left() + LEFT * 0.03], ROUTE, 4)
        names = IMAGES[:4] if v == "v20" else IMAGES
        fans = VGroup(*[Line(d.get_bottom(), self.blobs[n].get_top(), color=ROUTE, stroke_width=2)
                        for n in names])
        g = VGroup(main, fans)
        g.main, g.fans, g.names = main, fans, names
        return g

    def hop(self, t: str, run_time: float = 0.6):
        f = self.flags[t]
        tgt = f.pennant.get_top() + UP * 0.2
        if self.cursor.get_center()[1] < 2.0:
            self.cursor.move_to(tgt)
            return FadeIn(self.cursor, shift=DOWN * 0.2, run_time=run_time)
        return self.cursor.animate(run_time=run_time).move_to(tgt)

    def pull(self, scene, v: str = "v20"):
        bd = self.beads[1 if v == "v20" else 2]
        names = IMAGES[:4] if v == "v20" else IMAGES
        if self.colab not in scene.mobjects:
            scene.play(FadeIn(self.colab), run_time=0.4)
        d = Dot(self.colab.frame.get_top(), radius=0.09, color=ROUTE)
        scene.play(FadeIn(d), run_time=0.2)
        scene.play(d.animate.move_to(bd.get_center()), run_time=0.8)
        self.config.next_to(bd, DOWN, buff=0.5)
        scene.play(FadeIn(self.config, shift=UP * 0.1), Indicate(bd, color=ROUTE), run_time=0.6)
        dr = self.dirs[v]
        if dr not in scene.mobjects:
            scene.play(FadeIn(dr), run_time=0.3)
        scene.play(d.animate.move_to(dr.get_center()), run_time=0.8)
        scene.play(Indicate(dr.text, color=ROUTE, scale_factor=1.1), run_time=0.4)
        tiles = VGroup(*[tile(None, 0.4, CLOUD) for _ in names]).arrange(RIGHT, buff=0.1)
        tiles.move_to(self.colab.frame).shift(DOWN * 0.2)
        for n, t in zip(names, tiles):
            b = self.blobs[n]
            if b not in scene.mobjects:
                scene.add(b)
            scene.play(d.animate.move_to(b.get_center()), run_time=0.35)
            scene.play(FadeIn(t, target_position=b.get_center(), scale=0.5), run_time=0.35)
        scene.play(FadeOut(d), run_time=0.2)
        return tiles

    def stop_at_manifest(self, scene, v: str = "v21"):
        dr = self.dirs[v]
        d = Dot(self.colab.frame.get_top(), radius=0.09, color=ROUTE)
        scene.play(FadeIn(d), run_time=0.2)
        scene.play(d.animate.move_to(dr.get_left() + LEFT * 0.4), run_time=1.0)
        e = err_chip("401").next_to(dr, UP, buff=0.12)
        scene.play(FadeIn(e, scale=1.3), d.animate.set_color(ERR), run_time=0.5)
        return VGroup(d, e)

    def ghost(self, t: str = "dataset_v25") -> VGroup:
        f = flag_at(flag(t, S.GREY, 0.6, self.size, dashed=True), [0.35, 1.95, 0])
        tip = f.pole.get_start() + DOWN * 0.1
        r = DashedLine(tip, tip + DOWN * 1.1, color=S.GREY, stroke_width=3)
        g = VGroup(f, r)
        g.flag, g.rope = f, r
        return g

    def burn(self, run_time: float = 1.0):
        fr = self.store.frame
        ghost_ = DashedVMobject(fr.copy().set_fill(opacity=0), num_dashes=40).set_stroke(S.GREY, 3)
        return AnimationGroup(FadeOut(VGroup(*[b for b in self.blobs.values()], *self.dirs.values())),
                              Transform(fr, ghost_), self.store.title.animate.set_color(S.GREY),
                              run_time=run_time)

    def homes(self) -> VGroup:
        """The three homes of the bytes: images/ (BLUE, the folder you upload to · changes),
        .dvc/cache (GREY, your disk · copies made by dvc add), dvc_store/ (BLUE, named by
        fingerprint · never overwritten). Three columns, 12.4 wide, centred (0, 0.6)."""
        spec = (("images/", CLOUD, "the folder you upload to", "changes"),
                (".dvc/cache", LAPTOP, "your disk", "copies made by dvc add"),
                ("dvc_store/", CLOUD, "named by fingerprint", "never overwritten"))
        cols = VGroup()
        for name, c, a, b in spec:
            t = mono(name, 24, c)
            s1, s2 = label(a, 20, INK), label(b, 20, S.GREY)
            body = VGroup(t, s1, s2).arrange(DOWN, buff=0.14)
            fr = RoundedRectangle(width=3.9, height=1.9, corner_radius=0.16, stroke_color=c,
                                  stroke_width=3).set_fill(c, 0.07)
            body.move_to(fr)
            g = VGroup(fr, body)
            g.frame, g.title = fr, t
            cols.add(g)
        cols.arrange(RIGHT, buff=0.35).move_to([0, 0.6, 0])
        cols.images, cols.cache, cols.store = cols
        return cols

    def silhouette(self) -> VGroup:
        f = flag("tag", S.GREY, 0.5, 20)
        c = RoundedRectangle(width=0.9, height=0.7, corner_radius=0.08, stroke_color=S.GREY, stroke_width=2.5)
        b = vault("bucket", (), S.GREY, 20, mono_title=False)
        row = VGroup(f, c, b).arrange(RIGHT, buff=0.9)
        r1 = Arrow(f.get_right(), c.get_left(), buff=0.1, color=S.GREY, stroke_width=3, tip_length=0.15)
        r2 = Arrow(c.get_right(), b.get_left(), buff=0.1, color=S.GREY, stroke_width=3, tip_length=0.15)
        return VGroup(row, r1, r2)


# ================================================================== V7 · PipelineMap (the running map)
# the map at the START of each scene (script.md 'V7, the running map'; each scene lights its piece)
MAP_AT = {
    "S02": dict(), "S03": dict(secrets=True),
    "S04": dict(secrets=True, lit=("bucket1",)),
    "S05": dict(secrets=True, lit=("bucket1", "street", "studio")),
    "S06": dict(secrets=True, lit=("bucket1", "street", "studio")),
    "S07": dict(secrets=True, lit=("bucket1", "street", "studio", "cli")),
    "S08": dict(secrets=True, lit=("bucket1", "street", "studio", "cli", "labeled")),
    "S09": dict(secrets=True, lit=("bucket1", "labeled")),
    "S10": dict(secrets=True, lit=("bucket1", "labeled", "repo")),
    "S11": dict(secrets=True, lit=("bucket1", "labeled", "repo", "bucket2")),
    "S12": dict(secrets=True, lit=("bucket1", "labeled", "repo", "bucket2", "dvc")),
    "S13": dict(secrets=True, lit=("bucket1", "labeled", "repo", "bucket2", "dvc", "remote")),
    "S14": dict(secrets=True, lit=("bucket1", "labeled", "repo", "bucket2", "dvc", "remote", "flag_v20")),
    "S15": dict(secrets=True, lit=("bucket1", "labeled", "repo", "bucket2", "dvc", "remote", "flag_v20",
                                   "flag_v21")),
    "S16": dict(secrets=True, lit=("bucket1", "labeled", "repo", "bucket2", "dvc", "remote", "flag_v20",
                                   "flag_v21", "colab")),
}
MAP_PIECES = ("studio", "cli", "street", "bucket1", "labeled", "dvc", "bucket2", "repo", "colab", "remote",
              "fuse", "flag_v20", "flag_v21")
SLIDE6 = ("Unlabeled", "How do we do this?", "Labeled", "training · L13")


class PipelineMap(Rig):
    """V7 · the running map (built S02; each scene lights its piece; S08 closes part 1, S16 shows it
    complete, then unlit). 12.9 × 3.7, built in place for the band above a 3-row strip (body
    y -1.3 … 2.4; the thin slide-6 strip .slide6 at y 2.45 … 2.8 under the tracker). Never scale it.
      Row A, the labeling station: GREY frame (.lab) with the TEAL houses .houses['studio' | 'cli']
      ('command line container' caption .cli_caption, not added) on the PINK street .street; BLUE
      bucket 1 (.bucket1: cheese-app-data-demo, drawers cheeses_unlabeled/ cheeses_labeled/).
      Row B, the versioning station: GREY frame (.ver) with the TEAL data-version-cli house
      (.houses['dvc']); BLUE bucket 2 (.bucket2: images/, dvc_store/, title 'versioning bucket' at
      the bottom); right: your private GitHub repo (.repo, two GREEN flag stubs .flags['v20'|'v21'])
      and Colab (.colab, 'view versions').
      Left between the rows: the GREEN secrets/ drawer (.secrets) and its pipes (.pipes['studio' |
      'cli' | 'dvc'], not added). PINK links (.links['fuse' | 'remote'], not added): the DVC house →
      images/ (gcsfuse) and → dvc_store/ (the remote). The bridge (.bridge: GREY dashed line +
      three-line caption 'not connected / in the code / exercise E7' in the right column).
      .tower: the GREY dashed monitoring watchtower (S16, not added, top right).
      .slide6 (thin strip, not added) and .slide6_big (slide 6 redrawn full size, not added:
      .unlabeled (6 blank tiles) .question (RED) .labeled (.rows: brie gouda parmigiano gruyere)
      .training (GREY dashed)).
    Everything is drawn dark ('outline') until lit. PipelineMap.at('S08') = the map as S08 starts.
      light(*keys) / unlight(*keys) -> Animation   keys of MAP_PIECES (+ 'labeled' drawer, 'flag_v20')
      to_strip() -> Animation           .slide6_big shrinks into the thin strip (words fade, frames move)
      pipe_on(k) -> Animation           the secrets pipe into house k draws
      mark(k) -> VGroup                 a small round recap badge on its piece (S16): 'door', 'ticket',
                                        'rule', 'bouncer', 'envelope', 'fuse', 'shelf', 'rope'
      all_dark() -> Animation           everything unlit (S16's teardown)"""

    def __init__(self, secrets: bool = False, lit=(), size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        self.state = {k: False for k in MAP_PIECES}
        # ---- frames
        self.lab = self._frame(-4.72, -0.3, 0.64, 2.4, "labeling station")
        self.ver = self._frame(-4.72, -0.3, -1.3, 0.42, "versioning station")
        # ---- row A
        self.street = street(-4.6, -0.42, 0.79, NETWORK, False, size, band_h=0.28)
        self.houses = {
            "studio": house(CONTAINERS["studio"], 2.3, 0.82).move_to([-3.5, 0.94, 0], aligned_edge=DOWN),
            "cli": house(CONTAINERS["cli"], 1.84, 0.72).move_to([-1.39, 0.94, 0], aligned_edge=DOWN),
            "dvc": house(CONTAINERS["dvc"], 2.1, 0.82).move_to([-2.95, -1.12, 0], aligned_edge=DOWN),
        }
        self.cli_caption = note("command line container").next_to(self.lab.frame, UP, buff=0.05).align_to(
            self.lab.frame, RIGHT)
        self.bucket1 = vault(BUCKET1, ("cheeses_unlabeled/", "cheeses_labeled/"), CLOUD, size, vault_w=4.0)
        self.bucket1.move_to([1.93, 1.52, 0])
        self.bucket2 = vault("versioning bucket", ("images/", "dvc_store/"), CLOUD, size, mono_title=False,
                             title_bottom=True, vault_w=4.0)
        self.bucket2.move_to([1.93, -0.44, 0])
        # ---- right column
        self.repo = self._box(["your private", "GitHub repo"], LAPTOP, 2.3, 0.78).move_to([5.25, 0.03, 0])
        self.repo.align_to(self.repo, LEFT)
        self.repo.shift(RIGHT * (4.15 - self.repo.get_left()[0]))
        self.flags = {}
        for i, k in enumerate(("v20", "v21")):
            f = VGroup(Line([0, 0, 0], [0, 0.42, 0], color=POINTER, stroke_width=3),
                       Polygon([0, 0.42, 0], [0.26, 0.33, 0], [0, 0.24, 0], stroke_color=POINTER,
                               stroke_width=2).set_fill(POINTER, 0.45))
            f.move_to(self.repo.frame.get_corner(DR) + np.array([-0.62 + i * 0.32, 0.36, 0]))
            self.flags[k] = f
        self.repo.add(*self.flags.values())
        self.colab = self._box(["Colab", "view versions"], CLOUD, 2.3, 0.78).move_to([5.3, -0.9, 0])
        self.colab.shift(RIGHT * (4.15 - self.colab.get_left()[0]))
        # ---- secrets drawer and pipes
        self.secrets = drawer("secrets/", KEY, size, glyph=False).move_to([-5.62, 0.53, 0])
        sx, st, sb = self.secrets.get_center()[0], self.secrets.get_top()[1], self.secrets.get_bottom()[1]
        hs, hc, hd = self.houses["studio"], self.houses["cli"], self.houses["dvc"]
        self.pipes = {
            "studio": pipe([[sx - 0.3, st, 0], [sx - 0.3, 1.2, 0], [hs.body.get_left()[0], 1.2, 0]], KEY),
            "cli": pipe([[sx + 0.3, st, 0], [sx + 0.3, 1.88, 0], [-1.15, 1.88, 0], [-1.15, roof_y(hc, -1.15), 0]], KEY),
            "dvc": pipe([[sx, sb, 0], [sx, -0.85, 0], [hd.body.get_left()[0], -0.85, 0]], KEY),
        }
        # ---- links from the DVC house to bucket 2
        i2 = self.bucket2.drawers["images/"]
        ds = self.bucket2.drawers["dvc_store/"]
        hr = hd.body.get_right()[0]
        self.links = {
            "fuse": pipe([[hr, -0.7, 0], [-0.75, -0.7, 0], [-0.75, i2.get_center()[1], 0], i2.get_left()], ROUTE),
            "remote": pipe([[hr, -0.98, 0], [-0.55, -0.98, 0], [-0.55, ds.get_center()[1], 0], ds.get_left()],
                           ROUTE, stroke=3),
        }
        # ---- the bridge (labels → images, not connected)
        cl = self.bucket1.drawers["cheeses_labeled/"]
        bx = cl.get_center()[0] + 1.2
        br = DashedLine([bx, cl.get_bottom()[1], 0], [bx, i2.get_top()[1], 0], color=S.GREY, stroke_width=3)
        cap = VGroup(*[note(s) for s in ("not connected", "in the code", "exercise E7")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.06).move_to([4.15, 1.05, 0], aligned_edge=LEFT)
        lead = DashedLine([bx + 0.05, 0.54, 0], [4.05, 0.54, 0], color=S.GREY, stroke_width=2)
        lead2 = DashedLine([4.05, 0.54, 0], [4.05, cap.get_bottom()[1] + 0.1, 0], color=S.GREY, stroke_width=2)
        self.bridge = VGroup(br, lead, lead2, cap)
        self.bridge.line, self.bridge.caption = br, cap
        # ---- tower and the slide-6 rows
        self.tower = self._tower().move_to([5.3, 2.2, 0])
        self.slide6 = self._strip()
        self.slide6_big = self._big()
        # ---- assemble
        self.add(self.lab, self.ver, self.street, *self.houses.values(), self.bucket1, self.bucket2, self.repo,
                 self.colab, self.bridge)
        if secrets:
            self.add(self.secrets)
        self.ride(self.cli_caption, *self.pipes.values(), *self.links.values(), self.tower, self.slide6,
                  self.slide6_big)
        if not secrets:
            self.ride(self.secrets)
        self._lit = {k: self._targets(k).copy() for k in ("bucket1", "bucket2", "repo", "colab", "labeled",
                                                           "flag_v20", "flag_v21")}
        self.ride(*self._lit.values())
        for k in ("labeled", "flag_v20", "flag_v21"):
            self.state[k] = k in lit
        for k in MAP_PIECES:
            self._apply(k, k in lit)

    @classmethod
    def at(cls, scene_id: str, **kw) -> "PipelineMap":
        """The map as it stands when scene `scene_id` ('S08') starts (MAP_AT); kw overrides."""
        return cls(**{**MAP_AT[scene_id], **kw})

    # ---- building blocks
    def _frame(self, x0, x1, y0, y1, title):
        fr = RoundedRectangle(width=x1 - x0, height=y1 - y0, corner_radius=0.16, stroke_color=LAPTOP,
                              stroke_width=2.5).set_fill(LAPTOP, 0.04).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
        t = label(title, self.size, LAPTOP).move_to([x0 + 0.15, y1 - 0.2, 0], aligned_edge=LEFT)
        g = VGroup(fr, t)
        g.frame, g.text = fr, t
        return g

    def _box(self, lines, color, bw, bh):
        t = VGroup(*[label(s, self.size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        fr = RoundedRectangle(width=bw, height=bh, corner_radius=0.12, stroke_color=color, stroke_width=2.5) \
            .set_fill(color, 0.08)
        t.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.18)
        g = VGroup(fr, t)
        g.frame, g.text = fr, t
        return g

    def _tower(self):
        legs = VGroup(DashedLine([-0.3, 0, 0], [-0.12, 0.75, 0]), DashedLine([0.3, 0, 0], [0.12, 0.75, 0]))
        cab = DashedVMobject(Rectangle(width=0.5, height=0.3), num_dashes=12).move_to([0, 0.9, 0])
        roof = DashedVMobject(Polygon([-0.35, 1.05, 0], [0, 1.3, 0], [0.35, 1.05, 0]), num_dashes=10)
        g = VGroup(legs, cab, roof).set_stroke(FUTURE, 2.5)
        t = label("monitoring", self.size, FUTURE).next_to(g, RIGHT, buff=0.15).align_to(g, DOWN)
        return VGroup(g, t)

    def _strip(self):
        cs = [chip(SLIDE6[0], S.GREY, 20), label(SLIDE6[1], 20, ERR), chip(SLIDE6[2], S.GREY, 20),
              dashed_chip(SLIDE6[3])]
        row = VGroup()
        for i, c in enumerate(cs):
            row.add(c)
            if i < len(cs) - 1:
                row.add(Arrow(ORIGIN, RIGHT * 0.55, buff=0, color=S.GREY, stroke_width=3, tip_length=0.14))
        row.arrange(RIGHT, buff=0.12).move_to([-1.6, 2.62, 0])
        row.items = cs
        return row

    def _big(self):
        s = 22
        un = VGroup(*[tile(None, 0.6, S.GREY) for _ in range(6)]).arrange_in_grid(rows=2, cols=3, buff=0.18)
        ub = DashedVMobject(RoundedRectangle(width=un.width + 0.6, height=un.height + 0.9, corner_radius=0.16),
                            num_dashes=50, dashed_ratio=0.35).set_stroke(S.GREY, 2.5)
        un.move_to(ub).shift(DOWN * 0.15)
        ut = label(SLIDE6[0], s, INK).next_to(un, UP, buff=0.15)
        unl = VGroup(ub, un, ut)
        rows = VGroup(*[label(w, s, INK) for w in SLIDE6_ROWS]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        lb = RoundedRectangle(width=rows.width + 1.1, height=rows.height + 0.95, corner_radius=0.16,
                              stroke_color=S.GREY, stroke_width=2.5)
        rows.move_to(lb).shift(DOWN * 0.15)
        lt = label(SLIDE6[2], s, INK).next_to(rows, UP, buff=0.15)
        lab = VGroup(lb, rows, lt)
        lab.rows = rows
        tr = dashed_chip(SLIDE6[3], size=s)
        g = VGroup(unl, lab, tr).arrange(RIGHT, buff=2.6).move_to([0, 0.6, 0])
        a1 = Arrow(unl.get_right(), lab.get_left(), buff=0.15, color=S.GREY, stroke_width=4)
        q = label(SLIDE6[1], s, ERR).next_to(a1, UP, buff=0.12)
        a2 = Arrow(lab.get_right(), tr.get_left(), buff=0.15, color=S.GREY, stroke_width=3)
        big = VGroup(unl, a1, q, lab, a2, tr)
        big.unlabeled, big.question, big.labeled, big.training, big.arrows = unl, q, lab, tr, VGroup(a1, a2)
        return big

    # ---- lit / dark (dark = greyed(): shapes GREY_DARK, words GREY; the street: GREY dashed)
    def _targets(self, k):
        h = self.houses
        return {"studio": h["studio"], "cli": h["cli"], "dvc": h["dvc"], "street": self.street,
                "bucket1": self.bucket1, "bucket2": self.bucket2, "repo": self.repo, "colab": self.colab,
                "labeled": self.bucket1.drawers["cheeses_labeled/"], "flag_v20": self.flags["v20"],
                "flag_v21": self.flags["v21"]}[k]

    def _version(self, k, on: bool):
        """A fresh copy of piece k as it looks lit (on) or dark, where the piece is now."""
        m = self._targets(k)
        if k == "street":
            st = street(-4.6, -0.42, 0.79, NETWORK, on, self.size, band_h=0.28)
            return st.shift(m.band.get_center() - st.band.get_center())
        if k in ("studio", "cli", "dvc"):
            v = lit_house(m, True)
            return v if on else greyed(lit_house(m, False))
        v = self._lit[k].copy().move_to(m)
        if k == "bucket1" and not self.state["labeled"]:
            d = v.drawers["cheeses_labeled/"]
            d.become(greyed(d))
        if k == "repo":
            for f in ("v20", "v21"):
                if not self.state["flag_" + f]:
                    fl = v.submobjects[-2 if f == "v20" else -1]
                    fl.become(greyed(fl))
        return v if on else greyed(v)

    def _apply(self, k, on: bool):
        """Set piece k lit/dark in place (no animation)."""
        self.state[k] = on
        if k in ("fuse", "remote"):
            return
        m = self._targets(k)
        m.become(self._version(k, on))

    def _swap(self, keys, on, run_time):
        anims = []
        for k in keys:
            if k in ("fuse", "remote"):
                anims.append(Create(self.links[k]) if on else FadeOut(self.links[k]))
                self.state[k] = on
                continue
            self.state[k] = on
            anims.append(Transform(self._targets(k), self._version(k, on)))
        return AnimationGroup(*anims, run_time=run_time)

    def light(self, *keys, run_time: float = 0.7):
        """Animation: pieces `keys` (MAP_PIECES) light: houses TEAL, buckets BLUE, the street PINK."""
        return self._swap(keys, True, run_time)

    def unlight(self, *keys, run_time: float = 0.7):
        return self._swap(keys, False, run_time)

    def all_dark(self, run_time: float = 1.0):
        return self.unlight(*[k for k, v in self.state.items() if v], run_time=run_time)

    def to_strip(self, run_time: float = 1.0):
        b, s = self.slide6_big, self.slide6
        words = VGroup(b.unlabeled[1], b.unlabeled[2], b.labeled.rows, b.labeled[2], b.question)
        return AnimationGroup(FadeOut(words), ReplacementTransform(b.unlabeled[0], s.items[0]),
                              ReplacementTransform(b.labeled[0], s.items[2]),
                              ReplacementTransform(b.training, s.items[3]),
                              FadeIn(s.items[1]), ReplacementTransform(b.arrows, VGroup(*[m for m in s if isinstance(m, Arrow)])),
                              run_time=run_time)

    def pipe_on(self, k: str, run_time: float = 0.8):
        return Create(self.pipes[k], run_time=run_time)

    def mark(self, k: str) -> VGroup:
        """A recap badge (a small circle with a shape, no text) on its piece."""
        c = {"door": LAPTOP, "ticket": CLOUD, "rule": KEY, "bouncer": S.GREY, "envelope": NOTE,
             "fuse": ROUTE, "shelf": HASH, "rope": ROUTE}[k]
        ring_ = Circle(radius=0.27, stroke_color=c, stroke_width=3).set_fill(S.BG, 1)
        if k == "door":
            gl = door_glyph(0.18, 0.26, c)
        elif k == "ticket":
            gl = hourglass(0.26, c)
        elif k == "rule":
            gl = VGroup(*[Line([-0.1, y, 0], [0.12, y, 0], color=c, stroke_width=2.5) for y in (0.07, 0, -0.07)])
        elif k == "bouncer":
            gl = person_icon(c, 0.3)
        elif k == "envelope":
            gl = annotation("", 0.32, 0.22, 20)[:2]
        elif k == "shelf":
            gl = VGroup(*[Line([-0.13, y, 0], [0.13, y, 0], color=c, stroke_width=2.5) for y in (0.08, -0.04)])
        else:
            gl = Line([-0.13, -0.1, 0], [0.13, 0.1, 0], color=c, stroke_width=4)
        gl.move_to(ring_)
        g = VGroup(ring_, gl)
        h, b1 = self.houses, self.bucket1
        where = {"door": h["studio"].body.get_corner(DL) + np.array([0.0, 0.05, 0]),
                 "ticket": self.lab.frame.get_right() + np.array([0.12, 0.35, 0]),
                 "rule": b1.frame.get_corner(UR) + np.array([-0.05, -0.05, 0]),
                 "bouncer": self.lab.frame.get_corner(UR) + np.array([-0.05, -0.05, 0]),
                 "envelope": b1.drawers["cheeses_labeled/"].box.get_right() + LEFT * 0.33,
                 "fuse": self.links["fuse"].core.get_center(),
                 "shelf": [-1.0, 0.0, 0],
                 "rope": [self.repo.frame.get_left()[0] - 0.12, -0.45, 0]}[k]
        return g.move_to(where)
