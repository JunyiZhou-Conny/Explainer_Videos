"""Shared scene code for AC215 L13 (advanced training workflows: a run is a record, a job is a
rented machine).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example (placeholders only), the seven README/notebook trackers A-G (+ the clean-up tracker),
loaders for the real captures and sources in assets/ (with the capture-only crops refused and the
instructor's name masked), notebook frames, terminal helpers, tags, small glyphs, and the video's
set pieces V1-V7 (TrainingMap, RunLedger, ConfigBinding, TarballTrip, ThreeBadges, GpuSwitchboard,
MirroredReplicas). The scene authors' contract is build/SCENE-NOTES.md; the reference scene is
s01_hook.py; build/common_test.py (Bench) plays every set piece once.

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == SAY_COUNT["S07"]   # one voiceover block per SAY

Every text here is >= 20 pt.  Never .scale() a group that holds text below 1.0; set pieces take
size parameters instead.  Never set width/height/color/depth on a VGroup subclass (Manim
properties): these classes use box_w, tile_w, card_w ...
Nothing is added to the scene for you unless a method's docstring says "plays".
Adapted from L11's common.py (same producer); the L13 parts start at "L13 glyphs".
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import yaml
from manim import (DL, DOWN, DR, LEFT, ORIGIN, PI, RIGHT, UL, UP, UR, AnimationGroup, Arc, Arrow,
                   Circle, Create, DashedLine, DashedVMobject, Dot, FadeIn, FadeOut, FadeTransform,
                   GrowArrow, Indicate, LaggedStart, Line, MoveAlongPath, Polygon, Rectangle,
                   ReplacementTransform, RoundedRectangle, Rotate, Succession,
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
SAY_COUNT = {"S01": 4, "S02": 5, "S03": 8, "S04": 9, "S05": 7, "S06": 7, "S07": 9, "S08": 9,
             "S09": 7, "S10": 7, "S11": 8, "S12": 6, "S13": 7, "S14": 7, "S15": 6}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # your laptop: host shell, host filesystem, the secrets/ folder's home, the browser
CLOUD = S.BLUE           # GCP project boundary, bucket, Vertex AI, the job's VM, Cloud Logging, Colab, wandb.ai
IMAGE = S.TEAL           # containers/images: model-training-cli (the cockpit), Google's prebuilt tf-* images
CONTAINER = IMAGE
SYSTEM = S.ORANGE        # provided, not yours: Debian bases, apt packages, what the prebuilt image is assumed
PROVIDED = SYSTEM        #   to hold (TensorFlow, scikit-learn), the Google-managed service agent's badge
OWNED = S.GREEN          # project-owned, pinned: package/, setup.py, wandb==0.15.11, uv.lock, the tarball,
KEY = SECRET = OWNED     #   the model-trainer.json key, the W&B key in your shell, a run's config
PINNED = OWNED
PASS = S.GREEN           # a check that passed
TOOL = S.PURPLE          # docker, gcloud, gsutil, uv, pip, tar/gzip, the wandb library, tf.distribute
ERR = S.RED              # 404s, no installation candidate, auth errors, KeyError, no-tty, the key in --args
TURN = S.YELLOW          # your turn, the trackers, the current step, the run under discussion
COST = S.GOLD            # money only: the job VM while it runs, a GPU, the 32-vCPU box, bucket storage
ROUTE = S.PINK           # gsutil cp, --python-package-uris, stdout → logs, the W&B stream, all-reduce
FUTURE = S.GREY          # future / elsewhere / missing: the unsaved model, L15, Multi Worker: dashed
RUN = NOTE = INK = S.WHITE   # a run is a WHITE row in the ledger (a neutral record)
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
    pipe_ = t[0]
    if len(t) > 1:
        pipe_.move_to([t[1].get_center()[0], pipe_.get_center()[1], 0])
    pipe_.set_opacity(0)
    return t


def note(s: str, color=S.GREY, size: float = 20, **kw) -> Text:
    """A caption line (label font, GREY by default). The 2nd positional arg is the colour."""
    return label(s, size, color, **kw)


# ------------------------------------------------------------------ running example (placeholders only)
USER = "student"
P_LAPTOP = "student@laptop:~$"
P_LAPTOP_HOME = P_LAPTOP
P_REPO = "student@laptop:~/model-training$"
P_COCKPIT = "root@<id>:/app#"               # container ids are never shown (BRIEF crops)
P_COLAB = "$"
T_LAPTOP = "laptop"
T_NEW = "laptop · new terminal"             # S07 ponder 4, S10's no-key beat
T_COLAB = "colab stand-in · signed out"
PROJECT_ID = "your-gcp-project"             # the only project id ever shown as ours
BUCKET = "your-bucket-placeholder"          # exists nowhere (laptop/07)
BUCKET_URI = "gs://" + BUCKET
README_BUCKET = "cheese-app-trainer"        # the README's: only inside quoted lines and laptop/08
SA_NAME = "model-trainer"
KEY_FILE = "model-trainer.json"
KEY_PATH = "/secrets/model-trainer.json"
COCKPIT = "model-training-cli"
COCKPIT_SLIDE = "Model Trainer CLI Container"    # slide 24's words, said once (S06)
TARBALL = "cheese-app-trainer.tar.gz"       # the object name in the bucket (package-trainer.sh:4)
TAR_LOCAL = "trainer.tar.gz"
REGION = "us-central1"
CPU_IMAGE = "tf-cpu.2-17.py310"
GPU_IMAGE = "tf-gpu.2-17.py310"
MULTI_IMAGE = "tf-gpu.2-14.py310"
MACHINE = "n1-standard-4"
MACHINE_MULTI = "n1-standard-32"
JOB_NAME = "cheese_training_job_<12 hex>"   # the random hex is never shown
WB_HOST = "wandb.ai"
WB_PROJECT_NB = "cheese-app-demo"           # notebook B's W&B project
WB_PROJECT_REPO = "cheese-training-vertex-ai"   # task.py:314
WB_TEAM = "<team>"
SA_ROLES = ("Storage Admin", "AI Platform Admin", "Vertex AI Administrator")      # README:62
SERVICE_AGENT = ("Vertex AI Custom Code Service Agent", "service-…@gcp-sa-aiplatform-cc")   # digest §3.5
SLIDE9 = ("environment", "code", "data", "model", "metrics", "artifacts", "notes")
SLIDE10 = (("code", "GitHub"), ("data", "versioning (L11, DVC)"),
           ("environment", "pyproject.toml, uv.lock"), ("weights, metrics, logs", "?"))
SIDEBAR = (("Workbench", "notebooks"), ("Training", "jobs"), ("Pipelines", "workflows"))     # slides 19/21
THREE_LINES = (("Initialize wandb run", CLOUD), ("Add a callback to monitor model", OWNED),
               ("Let wandb know to finish the run", ERR))                                 # SLIDES.md:40
MULTI_EDITS = (("Create distribution Strategy", CLOUD), ("Adjust dataset batch size", OWNED),
               ("Create & Compile model in strategy scope", ERR))                         # SLIDES.md:46
LADDER = (("one machine · one GPU", "One Device"), ("one machine · many GPUs", "Mirrored"),
          ("many machines", "Multi Worker Mirrored"))                                    # slide 27
FLAGS = ("--epochs", "--batch_size", "--model_name", "--train_base", "--wandb_key")
FIVE_FILES = (".keras", ".weights.h5", ".json", "_train_history.json", "_model_metrics.json")
CONFIG_KEYS = ("learning_rate", "epochs", "batch_size", "model_name")                    # nbB:698-703
TRACKING_WORDS = ("reproducibility", "accountability")                                  # slide 8


# ------------------------------------------------------------------ captures
LAPTOP_DIR = "laptop"
# file lines never to print (ASSETS "Capture-only deviations", script.md "Crops"): checked by Capture.line()
NEVER = {("laptop", "84-standin-login-default.txt"): {3},           # printed before the check: reads as success
         ("laptop", "26-docker-shell.txt"): {28, 29, 30, 31}}       # BuildKit sha256 export lines
# lines refused in every file: the relay address, wandb's sandbox ProxyError, sha256 digests
NEVER_RE = (re.compile(r"172\.17\.0\.1"), re.compile(r"Network error \(ProxyError\)"),
            re.compile(r"sha256[:=][0-9a-f]{16,}"))
NEVER_FILES = {("laptop", "81-standin-commit.txt-never")}           # (none at present; kept for symmetry)

# series rule: the instructor's name never appears on screen. Any spelled-out name, and the Colab
# extracts' '<course instructor>' / '<notebook author>' placeholders, read '‹instructor›'.
# capture(), source_text(), nb_line() apply it.
_NAME_RE = re.compile(r"Pavlos(?:[ _]Protopapas)?|Protopapas|<course instructor>|<notebook author>",
                      re.IGNORECASE)


def unname(s: str) -> str:
    """s with the instructor's name masked: 'Pavlos Protopapas' / 'Pavlos' / '<course instructor>'
    -> '‹instructor›'."""
    return _NAME_RE.sub("‹instructor›", s)


# capture-only artefacts cropped on the way in (BRIEF "Crops"): the relay tail on apt lines, container
# ids in prompts and in 71's conflict line, the job name's random hex
_CROPS = ((re.compile(r"\s*\[IP: 172\.17\.0\.1 \d+\]"), ""),
          (re.compile(r"root@[0-9a-f]{12}:"), "root@<id>:"),
          (re.compile(r'container "[0-9a-f]{64}"'), 'container "…"'),
          (re.compile(r"cheese_training_job_[0-9a-f]{12}"), "cheese_training_job_<12 hex>"),
          (re.compile(r"UUID=[0-9a-f]{12}"), "UUID=<12 hex>"))


def crop(s: str) -> str:
    """A capture line with the BRIEF's crops applied (relay tail, container ids, the job's hex)."""
    for r, sub in _CROPS:
        s = r.sub(sub, s)
    return s


_PROMPT_RE = re.compile(r"^((?:\([^)]*\) )?(?:[\w.<>-]+@)?[\w.<>-]+:[^#$\s]*[#$])(?: (.*))?$")


def split_prompt(s: str) -> tuple[str, str]:
    """'root@<id>:/app# sh cli.sh' -> ('root@<id>:/app#', 'sh cli.sh'). A line without a prompt ->
    ('', s)."""
    m = _PROMPT_RE.match(s)
    if not m:
        return "", s
    return m.group(1), m.group(2) or ""


class Capture:
    """One captured command (assets/terminal/<folder>/<file>). .cmd (as typed) .lines (output body,
    no [exit N]) .exit .raw (every file line, tabs expanded to 8, crops applied) .path"""

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
        out_: list[str] = []
        for r in spec:
            if isinstance(r, str):
                out_.append(r)
                continue
            a, b = (r, r) if isinstance(r, int) else r
            if a < 2:
                raise ValueError("file line 1 is the '$ …' command; it is never printed")
            out_ += [self.line(n) for n in range(a, b + 1)]
        return out_

    def istep(self, n: int) -> tuple[str, str]:
        """File line n split into (prompt, typed): the istep captures 26, 30, 40, 50, 60, 70 (the
        prompt reads root@<id>:/app#)."""
        return split_prompt(self.line(n))


def capture(name: str) -> Capture:
    """capture("40") / capture("40-cli-sh") / capture("laptop/40") / capture("C38") /
    capture("colab/C38"): the one file assets/terminal/<folder>/NN-*.txt (a name starting with C
    is a colab file). Fails loudly when missing: never show an uncaptured output. Crops applied
    on the way in (crop()); the instructor's name masked (unname())."""
    if "/" in name:
        folder, name = name.split("/", 1)
    else:
        folder = "colab" if re.match(r"C\d", name) else LAPTOP_DIR
    if folder == "capture-only" or name.startswith("capture-only"):
        raise ValueError("capture-only/ is plumbing (placeholder key, base images, relay): never shown")
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
    raw = [crop(unname(s.rstrip("\r").expandtabs(8))) for s in text.rstrip("\n").split("\n")]
    m = re.fullmatch(r"(.*\S)\[exit (-?\d+)\]", raw[-1]) if len(raw) > 1 else None
    if m:
        raw = raw[:-1] + [m.group(1), f"[exit {m.group(2)}]"]
    cmd = raw[0][2:] if raw[0].startswith("$ ") else ""
    body = raw[1:]
    code_ = 0
    if body and re.fullmatch(r"\[exit -?\d+\]", body[-1]):
        code_ = int(body[-1][6:-1])
        body = body[:-1]
    return Capture(cmd, body, code_, raw, p, NEVER.get((folder, p.name), ()))


# ---- facts read from the captures (never typed by hand)
WANDB_KEY_PH = re.search(r"WANDB_KEY=(\S+);", capture("10").cmd).group(1)    # the 40-character placeholder
assert len(WANDB_KEY_PH) == int(capture("10").line(2)) == 40
CMDARGS = capture("40").line(75).split("CMDARGS=", 1)[1]                      # what cli.sh sends (sh -x)
ARGV = tuple(CMDARGS.split(","))                                             # gcloud splits --args at commas
TARBALL_BYTES = capture("30").line(54).split()[4]                             # '4016'
TAR_ENTRIES = tuple(capture("30").at((43, 50)))                               # tar cvf's eight entries
BUILD_LINE = capture("26").line(3)                                            # '[+] Building 314.2s (19/19) FINISHED …'


def _spec_chips() -> tuple:
    """40:77's --worker-pool-spec, split at its commas (the job card's chips)."""
    s = capture("40").line(77)
    spec = re.search(r"--worker-pool-spec=(\S+)", s).group(1)
    return tuple(spec.split(","))


SPEC_CHIPS = _spec_chips()     # ('machine-type=n1-standard-4', 'replica-count=1', 'executor-image-uri=…', 'python-module=trainer.task')


# ------------------------------------------------------------------ trackers (script.md, seven + clean-up)
SECTIONS = {
    "A": ("Notebook A", "›", "Cheese Classification Models"),
    "B": ("Notebook B", "›", "Experiment Tracking with W&B"),
    "C": ("README", "›", "model-training › Setup Environments & Credentials"),
    "D": ("README", "›", "model-training › Run Container"),
    "E": ("README", "›", "model-training › Package & Upload Python Code"),
    "F": ("README", "›", "model-training › Create & View Jobs in Vertex AI"),
    "G": ("README", "›", "model-training › OPTIONAL: Multi GPU Training"),
    "cleanup": ("extra", "·", "clean-up"),
}
STEPS = {
    "A": ["Setup Notebook", "Dataset", "Build Data Pipelines", "Image Classification Models",
          "Experiment Results", "Upload Experiment to Cloud Storage"],
    "B": ["Setup (pip install wandb)", "Dataset & pipelines", "W&B login", "Train five models",
          "Experiment Results", "Upload"],
    "C": ["Clone", "Vertex AI API", "GPU Quotas", "secrets folder", "Service account + key", "GCS bucket",
          "WandB key"],
    "D": ["Edit docker-shell.sh", "sh docker-shell.sh"],
    "E": ["Review setup.py", "Review task.py", "sh package-trainer.sh"],
    "F": ["Review cli.sh", "sh cli.sh", "CPU (optional — already the default)", "View Jobs",
          "View Training Metrics"],
    "G": ["Review cli-multi-gpu.sh", "Review task_multi_gpu.py", "Make changes", "sh cli-multi-gpu.sh"],
    "cleanup": ["jobs & bucket", "cockpit & images", "notebooks & keys"],
}
# the steps the README lacks: tracker D's two `extra` rows (hollow dots after the steps)
EXTRA_ROWS = {"D": ("fix 1 · Dockerfile:2", "fix 2 · Dockerfile:37")}
EXTRA_KINDS = ("local stand-in", "clean-up", "not captured")


def place_tracker(tr: ReadmeTracker) -> ReadmeTracker:
    """Pin a tracker to the house corner (left edge -6.5, top 3.5)."""
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def _suffix(tr, extra, note_) -> str:
    s = ""
    if extra is True:
        s = " · extra"
    elif extra in EXTRA_KINDS:
        s = f" · extra · {extra}"
    elif extra and not (isinstance(extra, str) and extra.startswith("fix")):
        raise ValueError(f"extra must be False, True, 'fix 1', 'fix 2' or one of {EXTRA_KINDS}, not {extra!r}")
    if note_:
        s += f" · {note_}"
    return s


def _caption(tr: ReadmeTracker, k: int, extra, note_=None) -> Text:
    anchor = tr.xdots if getattr(tr, "xdots", None) is not None else tr.dots
    if isinstance(extra, str) and extra.startswith("fix"):
        i = int(extra.split()[1]) - 1
        row = EXTRA_ROWS[tr.key][i]
        t = steady(f"extra: {row}", tr.size, tr.hi_color, t2c={"extra:": S.GREY})
        return t.next_to(anchor, RIGHT, buff=0.25)
    if not k:
        return steady("", tr.size, tr.hi_color).next_to(anchor, RIGHT, buff=0.25)
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    suf = _suffix(tr, extra, note_)
    t = steady(s + suf, tr.size, tr.hi_color, t2c={suf.strip(" ·"): S.GREY} if suf else None)
    return t.next_to(anchor, RIGHT, buff=0.25)


def _xdot(lit: bool):
    d = Circle(radius=0.06, stroke_color=TURN if lit else S.GREY, stroke_width=2)
    d.set_fill(TURN if lit else S.BG, 1 if lit else 0)
    return d


def _xdots(tr, extra) -> VGroup:
    lit = int(extra.split()[1]) - 1 if isinstance(extra, str) and extra.startswith("fix") else -1
    g = VGroup(*[_xdot(i == lit) for i in range(len(EXTRA_ROWS[tr.key]))]).arrange(RIGHT, buff=0.13)
    return g.next_to(tr.dots, RIGHT, buff=0.22)


def tracker(key: str, step: int | None = None, extra=False, note_: str | None = None) -> ReadmeTracker:
    """Tracker `key` ("A".."G", "cleanup") at `step` (1-based; None = no step lit yet), placed
    top-left: 'Notebook A › Cheese Classification Models' / 'README › model-training › …' /
    'extra · clean-up', one dot per step (D: plus two hollow GREY 'extra row' dots, .xdots), and
    'step k of N: <step>' + the suffix: extra=True (' · extra'), 'local stand-in', 'clean-up',
    'not captured' (' · extra · local stand-in' …); extra='fix 1' / 'fix 2' (tracker D only)
    lights that extra row and the caption reads 'extra: fix 1 · Dockerfile:2'. note_='already the
    default' appends ' · already the default' (S10/S13's F3)."""
    first, sep, section = SECTIONS[key]
    tr = ReadmeTracker(section, STEPS[key])
    tr.key = key
    # the head's first word: 'README' (mono, as the toolkit draws it), 'Notebook A', 'extra'
    old = tr.head
    w0 = mono(first, tr.size, S.GREY) if first == "README" else label(first, tr.size, S.GREY)
    head = VGroup(w0, label(sep, tr.size, S.GREY), label(section, tr.size, INK)).arrange(RIGHT, buff=0.12)
    head.move_to(old, aligned_edge=UL)
    tr.remove(old)
    tr.head = head
    tr.add(head)
    tr.dots.next_to(head, DOWN, buff=0.14, aligned_edge=LEFT)
    tr.xdots = None
    if key in EXTRA_ROWS:
        tr.xdots = _xdots(tr, extra)
        tr.add(tr.xdots)
    if step:
        tr.set_step(step)
    tr.remove(tr.caption)
    tr.caption = _caption(tr, step or 0, extra, note_)
    tr.extra, tr.note_ = extra, note_
    tr.add(tr.caption)
    return place_tracker(tr)


def _tracker_factory(key):
    def make(step=None, extra=False, note_=None):
        return tracker(key, step, extra, note_)
    make.__name__ = f"tracker_{key.lower()}"
    make.__doc__ = f"tracker('{key}', step, extra, note_): {' '.join(SECTIONS[key])}"
    return make


tracker_a, tracker_b, tracker_c, tracker_d, tracker_e, tracker_f, tracker_g = map(_tracker_factory, "ABCDEFG")
tracker_cleanup = _tracker_factory("cleanup")


def track(tr: ReadmeTracker, k: int | None = None, extra=False, note_: str | None = None,
          run_time: float = 0.5):
    """Animation: move the tracker to step k (None: stay) and set/clear the suffix (see
    tracker()). Use this, never tr.goto(). The caption cross-fades in place."""
    k = tr.k if k is None else k
    anims = []
    if k != tr.k:
        for i, d in enumerate(tr.dots, start=1):
            col = tr.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK)
            anims.append(d.animate.set_color(col).scale((1.5 if i == k else 1.0) / (d.width / 0.12)))
    if tr.xdots is not None and extra != tr.extra:
        anims.append(Transform(tr.xdots, _xdots(tr, extra)))
    old, new = tr.caption.copy(), _caption(tr, k, extra, note_)

    def fade_swap(m, a):
        src, f = (old if a < 0.5 else new), abs(1 - 2 * a)
        c = src.copy()
        for g, g0 in zip(c.family_members_with_points(), src.family_members_with_points()):
            g.set_fill(opacity=g0.get_fill_opacity() * f).set_stroke(opacity=g0.get_stroke_opacity() * f)
        m.become(c)

    anims.append(UpdateFromAlphaFunc(tr.caption, fade_swap))
    tr.k, tr.extra, tr.note_ = k, extra, note_
    return AnimationGroup(*anims, run_time=run_time)


def swap_tracker(scene, old: ReadmeTracker, new: ReadmeTracker, *anims, run_time: float = 0.6):
    """Plays: tracker `old` becomes `new` in place (section name and caption cross-fade, the dots
    regroup; the first word 'README' / 'Notebook A' stays put when both share it). `new` ends on the
    scene as one piece; `old` is gone."""
    same = old.head[0].original_text == new.head[0].original_text
    keep = VGroup(old.head[0], old.head[1]) if same else VGroup()
    scene.remove(old)
    olds = ([] if same else [old.head[0], old.head[1]]) + [old.head[2], old.dots, old.caption] + \
        ([old.xdots] if old.xdots is not None else [])
    scene.add(*keep, *olds)
    moves = [FadeTransform(old.head[2], new.head[2]), ReplacementTransform(old.dots, new.dots),
             FadeTransform(old.caption, new.caption)]
    if not same:
        moves += [FadeTransform(old.head[0], new.head[0]), FadeTransform(old.head[1], new.head[1])]
    if old.xdots is not None:
        moves.append(FadeOut(old.xdots))
    if new.xdots is not None:
        moves.append(FadeIn(new.xdots))
    scene.play(*moves, *anims, run_time=run_time)
    scene.remove(*keep, *new.head, new.dots, new.caption, *olds)
    if new.xdots is not None:
        scene.remove(new.xdots)
    scene.add(new)
    return new


def lref(slides: str, low: bool = False) -> VGroup:
    """The GREY 'Lecture 13 · slides 10–11' tag, top right (one per scene, BRIEF span). low=True
    sits it one row lower (centre y 3.0, beside the tracker's caption row): for a tracker whose
    heading reaches under it (F and G: measure with tr.get_right())."""
    g = lecture_ref(13, slides)
    if low:
        g.shift(DOWN * (g.get_center()[1] - 3.0))
    return g


# ---- line transforms (script.md conventions)
def cut(s: str, after: str, ellipsis: str = "…") -> str:
    """The line cut right after `after` (first occurrence), ending in '…'."""
    i = s.index(after) + len(after)
    return s[:i] + ellipsis


def from_(s: str, phrase: str, ellipsis: str = "…") -> str:
    """script.md's `from "…"`: the long line printed from `phrase` on, after a '…'."""
    return ellipsis + s[s.index(phrase):]


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


ID_COLUMNS = ("ID", "IMAGE ID", "CONTAINER ID")     # image/container ids: never shown (BRIEF crops)


def squeeze(lines: list[str], gutter: int = 2, drop=ID_COLUMNS) -> list[str]:
    """A docker table re-aligned with two-space gutters; columns empty in every row are dropped,
    and the id columns (ID_COLUMNS: 27, 91, 90) are dropped too (script: 'the ID column dropped by
    squeeze')."""
    names, rows, right = _table(lines)
    keep = [j for j in range(len(names)) if names[j] not in drop]
    if len(rows) > 1:
        keep = [j for j in keep if any(r[j] for r in rows[1:])]
    return _align([[r[j] for j in keep] for r in rows], [right[j] for j in keep], gutter)


def cols(lines: list[str], names: list[str], gutter: int = 2) -> list[str]:
    """Only the named columns of a docker table (header row first), re-aligned."""
    heads, rows, right = _table(lines)
    idx = [heads.index(n) for n in names]
    return _align([[r[j] for j in idx] for r in rows], [right[j] for j in idx], gutter)


def squash(s, gutter: int = 2):
    """Progress-line padding collapsed: every run of 3+ spaces inside the line becomes `gutter`
    spaces (BuildKit rows are padded to 110 columns: '[+] Building 314.2s (19/19) FINISHED <60
    spaces> docker:default'). Leading indentation is kept. A list maps over its items."""
    if isinstance(s, (list, tuple)):
        return [squash(x, gutter) for x in s]
    lead = len(s) - len(s.lstrip(" "))
    return s[:lead] + re.sub(r" {3,}", " " * gutter, s[lead:]).rstrip()


def soft(lines, n: int = 65) -> list:
    """Long lines broken at their last space that fits `n` characters (the text is unchanged, only
    the row break moves; a token longer than a row breaks at the edge). Items may be (text, colour)."""
    out_ = []
    for x in lines:
        s, c = (x, None) if isinstance(x, str) else x
        while len(s) > n:
            k = s.rfind(" ", 0, n + 1)
            if k > 0 and s[:k].strip():
                out_.append((s[:k].rstrip(), c))
                s = s[k + 1:]
            else:
                out_.append((s[:n], c))
                s = s[n:]
        out_.append((s, c))
    return [s if c is None else (s, c) for s, c in out_]


def at_commas(s: str, n: int = 65) -> list[str]:
    """A long comma-separated line (40:75 / 40:77's --args, 70:45, 80:70's package list) broken after
    its last comma that fits `n` characters (no space to break at). The rows join back to `s`."""
    rows, orig = [], s
    while len(s) > n:
        k = s.rfind(",", 0, n)
        if k <= 0:
            k = s.rfind(" ", 0, n)
        if k <= 0:
            k = n - 1
        rows.append(s[:k + 1])
        s = s[k + 1:]
    rows.append(s)
    assert "".join(rows) == orig, rows
    return rows


# ------------------------------------------------------------------ sources
_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".cfg": "ini", ".txt": "text", ".json": "json", ".lock": "toml", ".diff": "diff"}
# folder under assets/source -> header prefix (script.md: "history ·", "notebook A ·")
_REPOS = {"model-training": "model-training", "model-training-history": "history", "colab": "notebook"}
# W&B ids and the team in notebook B's stored output (BRIEF crops; coordinator: the team reads <team>)
_WB_MASKS = ((re.compile(r"ac215-harvard"), WB_TEAM),
             (re.compile(r"(/runs/)[a-z0-9]{8}"), r"\1…"),
             (re.compile(r"(offline-)?run-\d{8}_\d{6}-[a-z0-9]{8}"), "run-…"),
             (re.compile(r"(Syncing run )[a-z]+-[a-z]+-\d+"), r"\1…"))
_EMAIL_RE = re.compile(r"(?<![\w.+-])(?!git@)(?!noreply@)[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
README_NEVER = {96}          # README.md:96, an HTML comment holding a project-id-like string: never shown


def mask(s: str) -> str:
    """Source text with personal data replaced: e-mails -> student@example.com, the W&B team ->
    <team>, W&B run ids and auto run names -> '…', the instructor's name -> '‹instructor›'.
    source_text() / excerpt() / code() / nb_line() apply it."""
    for r, sub in _WB_MASKS:
        s = r.sub(sub, s)
    s = _EMAIL_RE.sub("student@example.com", s)
    return unname(s)


def _src(path: str) -> Path:
    p = SOURCE / path
    if p.exists() and p.is_file():
        return p
    raise FileNotFoundError(f"assets/source/{path} (folders: {', '.join(_REPOS)})")


def source_text(path: str) -> str:
    """An assets/source file, masked: 'model-training/cli.sh', 'model-training/package/trainer/task.py',
    'model-training-history/88f3374.diff', 'colab/notebook-B-1aAE5vR9.cells.txt'."""
    return mask(_src(path).read_text(encoding="utf-8"))


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of assets/source/<path>, masked. README.md:96 refused."""
    if path.endswith("model-training/README.md") and any(first <= n <= last for n in README_NEVER):
        raise ValueError("README.md:96 is an HTML comment with a project-id-like string: never shown")
    return "\n".join(source_text(path).split("\n")[first - 1:last])


def shown_path(path: str) -> str:
    """The header name of a source file: 'cli.sh', 'package/trainer/task.py', 'history · 88f3374.diff',
    'notebook A'. (The repo name is implied: the trackers name model-training.)"""
    rel = _src(path).relative_to(SOURCE).as_posix()
    top, _, rest = rel.partition("/")
    if top == "colab":
        return "notebook " + rest.split("-")[1]
    if top == "model-training":
        return rest
    return f"{_REPOS[top]} · {rest}"


def _lang(name: str) -> str:
    if name.startswith("Dockerfile"):
        return "docker"
    if name.startswith(".env") or name in (".gitignore",):
        return "bash"
    if name.endswith(".cells.txt"):
        return "python"
    if name == "PKG-INFO":
        return "text"
    return _LANG.get(Path(name).suffix, "text")


def _mt(path: str) -> str:
    """'cli.sh' -> 'model-training/cli.sh'; paths under another folder pass through."""
    top = path.split("/", 1)[0]
    return path if top in _REPOS else f"model-training/{path}"


def code(path: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, shown: str | None = None, max_lines: int = 12, cuts: dict | None = None,
         dedent: bool = False):
    """CODE(path: first–last) of script.md: a code_panel quoting assets/source/<path> (masked), header
    '<shown> · lines a–b'. path may omit 'model-training/' ('cli.sh', 'package/trainer/task.py';
    'model-training-history/88f3374.diff' for a diff). <= 12 lines. 22 pt fits <= 66 characters a
    line, 20 pt <= 73: a longer line raises; cut it with cuts={file_line: 'text it ends after'}
    (the house '…', recoloured GREY) or use font_size=20. .code .header; highlight with
    code_span(p.code, k, "sub"), line_bar(p.code, k, colour), k = file line - first. dedent=True
    removes the excerpt's common leading indentation, nothing else."""
    path = _mt(path)
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


def source_rows(path: str, n: int, size: float = 20, color=INK, width: int | None = None,
                indent: int = 4) -> VGroup:
    """Source line n of `path` (masked) as mono_line rows broken at the last space that fits
    (`width` characters; default 73 at 20 pt, 66 at 22 pt), continuation rows indented by `indent`
    spaces: the text is unchanged, only the row break moves. .rows .text"""
    path = _mt(path)
    s = excerpt(path, n, n)
    width = width or (66 if size >= 22 else 73)
    parts, first = [], True
    while len(s) > width - (0 if first else indent):
        k = s.rfind(" ", 0, width - (0 if first else indent) + 1)
        if k <= 0:
            break
        parts.append(s[:k])
        s = s[k + 1:]
        first = False
    parts.append(s)
    rows = VGroup(*[mono_line((" " * indent if i else "") + p, size, color) for i, p in enumerate(parts)])
    pitch = line_pitch(size)
    for i, r in enumerate(rows):
        r.shift(np.array([-r.strut.get_left()[0], -i * pitch - r.strut.get_center()[1], 0]))
    rows.rows, rows.text = list(rows), excerpt(path, n, n)
    return rows


def readme(n: int, last: int | None = None) -> str:
    """model-training/README.md line n (1-based; or lines n..last joined by newlines), masked
    (never line 96). A README command often sits in backticks or prose: compare with `in`, e.g.
    capture("26").cmd in readme(115)."""
    last = n if last is None else last
    return excerpt("model-training/README.md", n, last)


def readme_card(lines, body=None, quote: bool = False, card_w: float | None = None, size: float = 22,
                strip: bool = True) -> VGroup:
    """A GREY README card: header 'README.md · line n' (or 'lines a–b' for a tuple) and the README's
    own words. body None: the README lines themselves (stripped of markdown backticks and list
    marks when strip=True; long ones broken at a space); a str: '\\n' separates lines (label font);
    or any mobject. Never line 96. .frame .head .body"""
    where = f"line {lines}" if isinstance(lines, int) else f"lines {lines[0]}–{lines[1]}"
    head = VGroup(mono("README.md", CAPTION, S.GREY), label(f"· {where}", CAPTION, S.GREY)).arrange(RIGHT,
                                                                                                  buff=0.12)
    if body is None:
        a, b = (lines, lines) if isinstance(lines, int) else lines
        rows = [r for r in readme(a, b).split("\n") if r.strip()]
        if strip:
            rows = [re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", r).replace("`", "").strip() for r in rows]
        body = "\n".join(x for r in rows for x in soft([r], 60))
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


# ------------------------------------------------------------------ notebooks (the two Colab extracts)
NB_FILES = {"A": "colab/notebook-A-1h6xRhjI.cells.txt", "B": "colab/notebook-B-1aAE5vR9.cells.txt"}
NB_RUNS = {"A": "2025-10-20", "B": "2025-10-14"}      # the instructors' stored runs (Tesla T4)
_NB_MARKS = ("[HTML output, rendered as text]", "----- stored output")
_NB_CACHE: dict = {}


def _nb(which: str) -> list[str]:
    if which not in _NB_CACHE:
        _NB_CACHE[which] = source_text(NB_FILES[which]).split("\n")
    return _NB_CACHE[which]


def nb_line(which: str, n: int) -> str:
    """Extract line n (1-based) of notebook `which` ('A' / 'B'), masked (team <team>, run ids '…',
    the instructor ‹instructor›). Refuses the extract's own markers ('===== cell …', '----- stored
    output', '[HTML output, rendered as text]') and its header (line 1)."""
    ls = _nb(which)
    if not 2 <= n <= len(ls):
        raise IndexError(f"notebook {which} has {len(ls)} lines, not {n}")
    s = ls[n - 1]
    if s.startswith("===== cell") or s.strip() in _NB_MARKS:
        raise ValueError(f"notebook {which}:{n} is an extract marker ({s!r}): never printed")
    return s


def nb_lines(which: str, *spec) -> list[str]:
    """Lines by extract line numbers, as script.md's NB(A: …) writes them: ints, (a, b) ranges, '…'."""
    out_ = []
    for r in spec:
        if isinstance(r, str):
            out_.append(r)
            continue
        a, b = (r, r) if isinstance(r, int) else r
        out_ += [nb_line(which, n) for n in range(a, b + 1)]
    return out_


def nb_cell(which: str, n: int) -> int:
    """The cell number (the extracts' 0-based index) that holds extract line n."""
    ls = _nb(which)
    for k in range(n - 1, -1, -1):
        m = re.match(r"===== cell (\d+)", ls[k])
        if m:
            return int(m.group(1))
    raise ValueError(f"notebook {which}:{n}: no cell header above")


def nb_is_output(which: str, n: int) -> bool:
    """True when extract line n is a stored output line (after its cell's '----- stored output')."""
    ls = _nb(which)
    for k in range(n - 1, -1, -1):
        if ls[k].strip() == "----- stored output":
            return True
        if ls[k].startswith("===== cell"):
            return False
    return False


def nb_table(which: str, first: int, last: int) -> list[dict]:
    """A stored pandas table (pandas wraps wide tables into blocks with a trailing '\\'), parsed by
    column position: [{'idx': '1', 'trainable_parameters': '2,388,356', …, 'name':
    'mobilenetv2_train_base_True'}, …] in the table's own row order. nb_table('A', 1283, 1295) is
    cell 54's table; nb_table('B', 1703, 1715) cell 55's."""
    rows: dict = {}
    order: list = []
    block: list = []

    def take(bl):
        head = bl[0].rstrip().rstrip("\\").rstrip()
        spans = [(m.start(), m.end(), m.group()) for m in re.finditer(r"\S+", head)]
        for ln in bl[1:]:
            idx = ln[:spans[0][0]].split()[0]
            if idx not in rows:
                rows[idx] = {"idx": idx}
                order.append(idx)
            prev = len(idx)
            for a, b, name in spans:
                rows[idx][name] = ln[prev:b].strip().rstrip("\\").strip()
                prev = b

    for n in range(first, last + 1):
        s = nb_line(which, n)
        if not s.strip():
            if block:
                take(block)
            block = []
        else:
            block.append(s)
    if block:
        take(block)
    return [rows[i] for i in order]


def table_rows(which: str, first: int, last: int, columns=("name", "epochs", "accuracy")) -> list[tuple]:
    """The named columns of nb_table(), row by row: [('mobilenetv2_train_base_True', '15', '68.97%'), …]."""
    return [tuple(r[c] for c in columns) for r in nb_table(which, first, last)]


def sparkline(name: str = "accuracy", which: str = "B", first: int = 1010, last: int = 1014) -> list[int]:
    """notebook B's recorded W&B 'Run history' sparkline for `name` (nbB:1010-1014, the 2_block run,
    25 epochs) as levels 0..7 (▁ … █)."""
    bars = "▁▂▃▄▅▆▇█"
    for n in range(first, last + 1):
        k, _, v = nb_line(which, n).partition(" ")
        if k == name:
            return [bars.index(c) for c in v.strip()]
    raise KeyError(name)


def run_summary(name: str, which: str = "B", first: int = 1016, last: int = 1023) -> str:
    """A value of notebook B's recorded 'Run summary' (nbB:1016-1023): run_summary('accuracy') -> '0.72436'."""
    for n in range(first, last + 1):
        k, _, v = nb_line(which, n).partition(" ")
        if k == name:
            return v.strip()
    raise KeyError(name)


EXPERIMENT = nb_line("A", 1304).split("/")[0]                    # 'experiment_1760994796'
DATASET_SIZE = nb_line("A", 353).split(":")[1].strip()           # '1156'
SPLIT_COUNTS = tuple(nb_line("A", n).split(":")[1].strip() for n in (445, 446, 447))   # 936, 104, 116
TABLE_A = table_rows("A", 1283, 1295)      # S01's left table (name, epochs, accuracy)
TABLE_B = table_rows("B", 1703, 1715)      # S01's right table
RECORDED_A = f"recorded · notebook A, {NB_RUNS['A']}"
RECORDED_B = f"recorded · notebook B, {NB_RUNS['B']}"


def nb_recorded_tag(which: str, s: str | None = None) -> VGroup:
    """GREY 'recorded · notebook A, 2025-10-20' (B: 2025-10-14) — on every stored output."""
    return tag(s or (RECORDED_A if which == "A" else RECORDED_B), S.GREY)


def notebook_cell(which: str, *spec, cell: int | None = None, size: float = 22, card_w: float | None = None,
                  cuts: dict | None = None, wrap: bool = False, tag_: bool = True, ill: bool = True,
                  hi: dict | None = None) -> VGroup:
    """NB(A: …) of script.md: a schematic Colab cell (no product chrome, no logo), BLUE frame
    (the Colab runtime), header 'notebook A · cell n' (from the extract; cell= overrides), the code
    lines in WHITE mono, the stored-output lines (after the cell's '----- stored output') in a dark
    well tagged 'recorded · notebook A, 2025-10-20' (tag_=False: none) and the frame tagged
    `illustration` (ill=False: none). spec: extract line numbers / (a, b) ranges / '…' (a '…'
    joins the side of the line before it). A line longer than the frame raises (22 pt: 66
    characters, 20 pt: 73): cuts={n: 'text it ends after'} or wrap=True (broken at the last space that
    fits; code continuation rows indented 4 spaces, the text unchanged). hi={n: colour} colours whole
    lines. .frame .header .rows .code_rows .out_rows .well .tag .ill .line(n) (a VGroup of the rows
    of extract line n) .sub(n, 'text') (its glyphs, across folded rows)"""
    cuts, hi = cuts or {}, hi or {}
    limit = 66 if size >= 22 else 73
    items: list = []           # (n or None, text, is_output, row k of that line)
    last_out = False
    for r in spec:
        if isinstance(r, str):
            items.append((None, r, last_out, 0))
            continue
        a, b = (r, r) if isinstance(r, int) else r
        for n in range(a, b + 1):
            s = nb_line(which, n)
            last_out = nb_is_output(which, n)
            if n in cuts:
                s = cut(s, cuts[n])
            if wrap and len(s) > limit:
                parts = soft([s], limit) if last_out else _code_rows(s, limit)
            else:
                parts = [s]
            for k, p in enumerate(parts):
                if len(p) > limit:
                    raise ValueError(f"notebook {which}:{n} is {len(p)} characters; > {limit} at {size} pt: "
                                     f"cuts={{{n}: '…'}} or wrap=True")
                items.append((n, p, last_out, k))
    first_n = next(n for n, _, _, _ in items if n is not None)
    cell = nb_cell(which, first_n) if cell is None else cell
    pitch = line_pitch(size)
    rows, code_rows, out_rows, index = VGroup(), [], [], {}
    for i, (n, s, is_out, k) in enumerate(items):
        col = hi.get(n, OUTPUT if is_out else INK)
        r = mono_line(s, size, col)
        r.shift(np.array([-r.strut.get_left()[0], -i * pitch - r.strut.get_center()[1], 0]))
        r.n, r.is_output = n, is_out
        rows.add(r)
        (out_rows if is_out else code_rows).append(r)
        if n is not None:
            index.setdefault(n, VGroup()).add(r)
    head = label(f"notebook {which} · cell {cell}", CAPTION, S.GREY)
    w = card_w or max(rows.width + 0.8, head.width + 2.6)
    body_h = rows.height + 0.4
    fr = RoundedRectangle(width=w, height=body_h + 0.55, corner_radius=0.14, stroke_color=CLOUD,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    head.move_to(fr.get_corner(UL) + np.array([0.3 + head.width / 2, -0.3, 0]))
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.4).align_to(fr, DOWN).shift(UP * 0.2)
    g = VGroup(fr, head)
    well = None
    if out_rows:
        top = out_rows[0].strut.get_top()[1] + 0.08
        bot = out_rows[-1].strut.get_bottom()[1] - 0.08
        well = Rectangle(width=w - 0.3, height=top - bot, stroke_width=0).set_fill(TERM_BG, 1)
        well.move_to([fr.get_center()[0], (top + bot) / 2, 0])
        g.add(well)
    g.add(rows)
    g.frame, g.header, g.rows, g.code_rows, g.out_rows, g.well = fr, head, rows, code_rows, out_rows, well
    g.tag = g.ill = None
    if ill:
        it = illustration_tag().next_to(fr, UP, buff=0.08).align_to(fr, RIGHT)
        g.add(it)
        g.ill = it
    if tag_ and out_rows:
        tg = nb_recorded_tag(which)
        tg.next_to(fr, DOWN, buff=0.08).align_to(fr, RIGHT)
        g.add(tg)
        g.tag = tg
    g.line = lambda n: index[n]

    def sub(n, text, occurrence=0):
        """The glyphs of `text` on extract line n (searched row by row when the line folded)."""
        seen = 0
        for r in index[n]:
            i = -1
            while True:
                i = r.text.find(text, i + 1)
                if i < 0:
                    break
                if seen == occurrence:
                    return substring(r, text, r.text[:i].count(text))
                seen += 1
        raise ValueError(f"{text!r} not on notebook {which}:{n}")
    g.sub = sub
    return g


def _code_rows(s: str, limit: int, indent: int = 4) -> list[str]:
    """A long code line broken at its last space that fits, continuation rows indented (text unchanged)."""
    parts, first = [], True
    while len(s) > limit - (0 if first else indent):
        k = s.rfind(" ", 0, limit - (0 if first else indent) + 1)
        if k <= 0:
            break
        parts.append(("" if first else " " * indent) + s[:k])
        s = s[k + 1:]
        first = False
    parts.append(("" if first else " " * indent) + s)
    return parts


def notebook_menu(path, size: float = 22) -> VGroup:
    """A schematic Colab menu path ('File', 'Save a copy in Drive'): GREY chips joined by '→'
    (illustration; tag it). .items"""
    items = [grey_chip(s, size=size) for s in path]
    row = VGroup()
    for i, c in enumerate(items):
        row.add(c)
        if i < len(items) - 1:
            row.add(label("→", size, S.GREY))
    row.arrange(RIGHT, buff=0.14)
    row.items = items
    return row


# ------------------------------------------------------------------ terminals
def term(prompt: str = P_LAPTOP, rows: int = 10, title: str | None = T_LAPTOP, width: float = 12.6,
         size: float = 22, place: bool = True) -> Terminal:
    """The house terminal: 12.6 wide, 22 pt, 65 characters a row, centred, bottom edge at BOTTOM.
    Height = rows x 0.403 + 0.85. Full width, or a 3-row strip (rows=3) under a picture. size=20
    gives 72 characters a row (the long one-liners: 07, 08, 09, the sed edits, 80, 83-87, 70:45)."""
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)
    if place:
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def laptop_term(rows: int = 10, prompt: str = P_LAPTOP) -> Terminal:
    return term(prompt, rows, T_LAPTOP)


def new_term(rows: int = 3, prompt: str = P_LAPTOP) -> Terminal:
    """The second host shell: 'laptop · new terminal' (S07 ponder 4, S10's never-exported key)."""
    return term(prompt, rows, T_NEW)


def colab_term(rows: int = 3) -> Terminal:
    """The Colab stand-in strip: title 'colab stand-in · signed out', prompt '$' (tag it
    standin_tag())."""
    return term(P_COLAB, rows, T_COLAB)


def container_note(s: str = "our capture: a fresh cockpit for this step · stay in yours") -> VGroup:
    """The GREY chip at the first cockpit prompt of a new capture segment (script conventions)."""
    return grey_chip(s)


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


def _soft_fold(t: Terminal):
    def fold(text: str, first_prefix: int = 0) -> list[str]:
        n = t.max_chars
        return [text[i:i + n] for i in range(0, len(text), n)] or [text]
    return fold


def type_cmd(scene, t: Terminal, cmd: str, type_time: float | None = None, soft: bool = False):
    """Plays: type at the waiting prompt (replacing a bare prompt line if there is one; room is made
    first). Long commands fold at a space outside quotes with ' \\' (Terminal.fold). soft=True
    soft-wraps at the row edge instead, like a real terminal (no ' \\', rows join back to the exact
    command, asserted): for a quoted argument longer than a row (the sed edits 20/22/24, the
    python -c lines of 83-87). Returns the line, or a VGroup with .rows when it folded."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    p = t.prompt + " "
    if soft:
        t.fold = _soft_fold(t)
    try:
        room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
        ln = t.type(scene, cmd, type_time)
    finally:
        if soft:
            del t.fold
    if soft and hasattr(ln, "rows"):
        assert "".join(r.text for r in ln.rows) == p + cmd, "soft wrap must join back to the command"
    return ln


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
    """Plays: a typed line at the cockpit prompt, from its istep capture ('root@<id>:/app# sh cli.sh'):
    set the terminal's prompt to root@<id>:/app#, then type the rest."""
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
    l_, r, b, tp = mob.get_left()[0], mob.get_right()[0], mob.get_bottom()[1], mob.get_top()[1]
    return any(l_ < ch.get_right()[0] + 0.03 and r > ch.get_left()[0] - 0.03
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
                         "use a row_tag, put it on an output row, or on_bar()")
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
    """'extra' sized for a terminal row (GREY); kind 'local stand-in' / 'clean-up' -> 'extra · …'."""
    return row_tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def standin_row() -> VGroup:
    """'extra · local stand-in' sized for a terminal row (colab/C05, C05b, C38, C38b; laptop/80-87)."""
    return extra_row("local stand-in")


def time_row() -> VGroup:
    """'at the time of recording' sized for a terminal row (GREY)."""
    return row_tag("at the time of recording", S.GREY)


def editor_row(s: str = "our editor; use yours") -> VGroup:
    """The GREY row tag of the sed edits (20, 22, 24)."""
    return row_tag(s, S.GREY)


def cost_row(s: str) -> VGroup:
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
    """An outline box around `g` (hides nothing: fine over terminal text)."""
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
_AMOUNT_RE = re.compile(r"[$€£¢]|\d\s*(cents?|dollars?|USD)\b|\bcents?\b|per hour|/h\b|\bprice[ds]?\b", re.I)


def _no_amount(s: str) -> str:
    """Cost text never carries a money amount or a price (sizes like '10–104 MB' are fine; 'the
    pricing page' is fine; '$', cents, 'per hour', 'price' are not)."""
    if _AMOUNT_RE.search(s):
        raise ValueError(f"cost tag {s!r}: no money amounts or prices on screen (BRIEF: never a number)")
    return s


def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag (house size: beside a card or panel, not inside a terminal row)."""
    return tag("▶ your turn", TURN)


def extra_tag(kind: str | None = None) -> VGroup:
    """GREY 'extra' tag; kind 'local stand-in' / 'clean-up' / 'not captured' -> 'extra · …'."""
    return tag("extra" + (f" · {kind}" if kind else ""), S.GREY)


def standin_tag() -> VGroup:
    """'extra · local stand-in': colab/C05, C05b, C38, C38b and laptop/80-87 (the Vertex job's first
    step replayed in a plain Python 3.10 container; never Google's image)."""
    return extra_tag("local stand-in")


def stand_in_label() -> VGroup:
    """The plain GREY 'stand-in' tag (S07: the key file in 06)."""
    return tag("stand-in", S.GREY)


def illustration_tag(s: str = "illustration") -> VGroup:
    """On every console step, W&B page, notebook frame, the sidebar, the job-log shape (S12), the
    repo run's ledger row, the quota page, the GPU log line in S13 (schematic; no screenshots)."""
    return tag(s, S.GREY)


def recorded_tag(s: str = "recorded") -> VGroup:
    """On every success a student sees that this machine could not produce; name the source:
    recorded_tag('recorded · notebooks A/B'). Notebook outputs: nb_recorded_tag('A')."""
    return tag(s, S.GREY)


def recording_tag(s: str = "at the time of recording") -> VGroup:
    """Beside versions and image sizes when first shown (never on the tarball's 4016 bytes or the
    notebooks' counts: those are deterministic or stored)."""
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    """On every README/repo/notebook slip (the narration says 'a small slip')."""
    return tag(s, S.GREY)


def preview_tag(s: str = "preview") -> VGroup:
    return tag(s, S.GREY)


def plan_tag(s: str = "plan · drawn") -> VGroup:
    """S06's V4 step-4 miniature (no output panels)."""
    return tag(s, S.GREY)


def drawn_tag(s: str = "what Vertex does · drawn, not recorded") -> VGroup:
    """S11's full V4 step 4 (no output panels)."""
    return tag(s, S.GREY)


def editor_tag(s: str = "our editor; use yours") -> VGroup:
    """The sed edits of 20/22/24."""
    return tag(s, S.GREY)


def cost_tag(s: str = "billed while it runs · see the Vertex AI pricing page") -> VGroup:
    """The GOLD money tag: text only, never a number or a price (raises on '$', cents, 'per hour',
    'price'). S01 (checklist), S03 (experiment folder), S07 (bucket), S09 (tarball), S10 (the job's
    VM), S13 (a GPU), S14 (n1-standard-32 + 2 × T4), S15's card. Compute tags end 'see the Vertex AI
    pricing page'."""
    return tag(_no_amount(s), COST)


def grey_chip(s: str, size: float = 20, mono_font: bool = False, color=S.GREY) -> VGroup:
    """A GREY chip for a short note. .box .text"""
    return chip(s, color, size=size, font=MONO if mono_font else None)


def replace_chip(s: str = "replace this with yours") -> VGroup:
    """The GREY chip beside every instructors' resource name (cheese-app-trainer, ac215-project,
    cheese-app-models) inside quoted lines (coordinator decision)."""
    return grey_chip(s)


def dashed_chip(s: str, color=FUTURE, size: float = 20, mono_font: bool = False) -> VGroup:
    """A dashed chip: future/elsewhere/missing (L15, Multi Worker Mirrored, the unsaved model). .box .text"""
    t = mono(s, size, color) if mono_font else label(s, size, color)
    ob = outline_box(t.width + 0.48, mono("|", size).height + 0.24, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def tool_chip(s: str, size: float = 20) -> VGroup:
    """A tool as a PURPLE mono chip (never a logo): docker, gcloud, gsutil, uv, pip, tar, wandb …"""
    return chip(s, TOOL, size=size, font=MONO)


def err_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """A RED error chip: err_chip('404'), err_chip('two jobs, two bills', mono_font=False). .box .text"""
    return chip(s, ERR, size=size, font=MONO if mono_font else None, fill_opacity=0.14)


def differ_chip(s: str = "yours will differ") -> VGroup:
    """GREY chip for container ids, the job's hex, image ids (never read aloud)."""
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
    """The heading of an output-only strip: GREY mono text (place it on the strip's title bar or
    above it)."""
    return mono(call, 20, S.GREY)


def ponder(scene, question: str, seconds: float = 8, quick: bool = False, center=None,
           width: float = 9.5) -> VGroup:
    """Plays a PONDER card (timer drains over `seconds`); quick=True is the script's QUICK(4 s):
    the header says 'Quick predict'. center=(x, y) moves the card (default: the frame's centre).
    The frame is opaque, so the card may sit over a set piece.
    Returns the card (still on screen): FadeOut it at the start of the next block."""
    c = ponder_card(question, width=width)
    c[0].set_fill(S.BG, 1)        # opaque: at 0.96 the words of a set piece behind it ghost through (L10 S08)
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
    """A key (bow, shaft, two teeth), GREEN. Lies flat."""
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
    """A container as a small house (TEAL): hollow (nothing runs) or lit (running); dashed for the
    stand-in containers. The name sits inside the body (20 pt; keep it <= house_w - 0.25 wide).
    .body .roof .text ; base at y=0 of its own frame: place with .move_to(point, aligned_edge=DOWN)."""
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
    """A polyline route through `points` ending in an arrow tip. .path (for travel()) .line .tip_arrow"""
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
    """A bucket as a BLUE vault: a titled box with its drawers stacked. .frame .title .drawers .rows"""
    tt = mono(title, size, color) if mono_title else label(title, size, color)
    ds = [drawer(d, color, size) for d in drawers]
    dw = max([d.width for d in ds] + [tt.width])
    if vault_w:
        dw = max(dw, vault_w - 0.4)
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


def sticky(s: str, color=TURN, size: float = 20, mono_font: bool = True) -> VGroup:
    """A small sticky label (V3's YELLOW `wandb.config` name): a card with a folded corner. .frame .text"""
    t = mono(s, size, INK) if mono_font else label(s, size, INK)
    w, h = t.width + 0.36, t.height + 0.26
    fr = Polygon([-w / 2, h / 2, 0], [w / 2 - 0.12, h / 2, 0], [w / 2, h / 2 - 0.12, 0], [w / 2, -h / 2, 0],
                 [-w / 2, -h / 2, 0], stroke_color=color, stroke_width=2.5).set_fill(color, 0.22)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def window(url: str, win_w: float = 6.0, win_h: float = 3.6, size: float = 20) -> VGroup:
    """A schematic browser/console window (no logo, no screenshot): always tag it `illustration`.
    .frame .address .content — browser_window() at 20 pt; win_w grows to fit the address."""
    win_w = max(win_w, mono(url, size).width + 1.75)
    return browser_window(url, win_w, win_h, size)


def pipe(points, color=ROUTE, stroke: float = 4, glow: bool = True, dashed: bool = False) -> VGroup:
    """A tube through `points` (a polyline with a soft glow): GREY→TEAL for the cockpit's mounts,
    PINK for routes, PURPLE for the callback pipe. Create() draws it. .core .glow"""
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


def tag_on(mob, s: str, color=S.GREY, direction=UP, buff: float = 0.1) -> VGroup:
    """A house-size tag placed next to `mob` (not added)."""
    return tag(s, color).next_to(mob, direction, buff=buff)


# ------------------------------------------------------------------ L13 glyphs (all text >= 20 pt)
def meter(meter_w: float = 0.6, color=COST) -> VGroup:
    """A GOLD meter (a dial and a needle, NO numbers): money is being spent while it runs.
    .dial .needle ; meter_run(m) swings the needle, meter_stop(m) brings it back."""
    r = meter_w / 2
    dial = Arc(radius=r, start_angle=0, angle=PI, color=color, stroke_width=3)
    base = Line([-r, 0, 0], [r, 0, 0], color=color, stroke_width=3)
    needle = Line(ORIGIN, r * 0.8 * np.array([np.cos(PI * 0.85), np.sin(PI * 0.85), 0]), color=color,
                  stroke_width=3)
    g = VGroup(dial, base, needle)
    g.dial, g.needle = dial, needle
    g.center_pt = Dot(ORIGIN, radius=0.001).set_opacity(0)
    g.add(g.center_pt)
    g.running = False
    return g


def meter_run(m: VGroup, run_time: float = 1.0):
    """Animation: the meter's needle swings right (the machine bills). Idempotent per state."""
    ang = 0 if m.running else -0.7 * PI
    m.running = True
    return Rotate(m.needle, angle=ang, about_point=m.center_pt.get_center(), run_time=run_time)


def meter_stop(m: VGroup, run_time: float = 0.8):
    """Animation: the needle falls back (billing stops)."""
    ang = 0.7 * PI if m.running else 0
    m.running = False
    return Rotate(m.needle, angle=ang, about_point=m.center_pt.get_center(), run_time=run_time)


def badge(lines, color=KEY, size: float = 20, kind: str = "key", badge_w: float | None = None,
          mono_first: bool = True) -> VGroup:
    """An ID badge on a lanyard clip: `color` outline, a portrait glyph (kind 'key': a key; 'agent':
    a gear, Google-managed; 'wandb': a row of dots, the key never shown), then `lines` (first mono
    when mono_first). .frame .clip .portrait .text"""
    if isinstance(lines, str):
        lines = [lines]
    txt = VGroup(*[(mono if (i == 0 and mono_first) else label)(s, size, INK if i == 0 else S.GREY)
                   for i, s in enumerate(lines)]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    pf = RoundedRectangle(width=0.55, height=0.55, corner_radius=0.08, stroke_color=color,
                          stroke_width=2.5).set_fill(color, 0.15)
    if kind == "key":
        gl = key_glyph(0.42, color)
    elif kind == "agent":
        gl = VGroup(Circle(radius=0.13, stroke_color=color, stroke_width=3),
                    *[Line(ORIGIN, 0.2 * np.array([np.cos(a), np.sin(a), 0]), color=color, stroke_width=3)
                      .shift(0.13 * np.array([np.cos(a), np.sin(a), 0])) for a in np.linspace(0, 2 * PI, 6,
                                                                                                endpoint=False)])
    else:
        gl = VGroup(*[Dot(radius=0.035, color=color) for _ in range(5)]).arrange(RIGHT, buff=0.04)
    portrait = VGroup(pf, gl.move_to(pf))
    row = VGroup(portrait, txt).arrange(RIGHT, buff=0.22)
    w = badge_w or row.width + 0.5
    frame = RoundedRectangle(width=w, height=row.height + 0.45, corner_radius=0.12,
                             stroke_color=color, stroke_width=3).set_fill(S.GREY_DARKER, 1)
    row.move_to(frame)
    clip = RoundedRectangle(width=0.5, height=0.16, corner_radius=0.05, stroke_color=color,
                            stroke_width=2.5).set_fill(S.BG, 1).move_to(frame.get_top())
    g = VGroup(frame, row, clip)
    g.frame, g.clip, g.portrait, g.text = frame, clip, portrait, txt
    return g


def building(name: str = WB_HOST, bw: float = 2.4, bh: float = 2.4, size: float = 20, color=CLOUD) -> VGroup:
    """A BLUE building (no logo): pediment, columns, base, its name (wandb.ai: a separate building
    outside the GCP boundary). Base at y = 0 of its own frame. .frame .text"""
    ped_h = min(0.5, bh * 0.2)
    base = Rectangle(width=bw, height=0.12).move_to([0, 0.06, 0])
    hall = Rectangle(width=bw - 0.3, height=bh - ped_h - 0.12).next_to(base, UP, buff=0)
    ped = Polygon([-bw / 2, bh - ped_h, 0], [0, bh, 0], [bw / 2, bh - ped_h, 0])
    for m in (base, hall, ped):
        m.set_stroke(color, 3).set_fill(color, 0.08)
    t = mono(name, size, color).move_to([0, bh - ped_h - 0.3, 0])
    cols_ = VGroup()
    lo, hi = t.get_bottom()[1] - 0.1, t.get_top()[1] + 0.1
    for x in np.linspace(-bw / 2 + 0.4, bw / 2 - 0.4, 4):
        for a, b in ((0.2, min(hall.get_top()[1] - 0.1, lo)), (max(0.2, hi), hall.get_top()[1] - 0.1)):
            if b - a > 0.05:
                cols_.add(Line([x, a, 0], [x, b, 0], color=color, stroke_width=3, stroke_opacity=0.45))
    g = VGroup(base, hall, ped, cols_, t)
    g.frame, g.text = VGroup(base, hall, ped), t
    return g


def parcel(text: str | None = None, color=OWNED, size: float = 20, parcel_w: float = 0.7,
           parcel_h: float = 0.5) -> VGroup:
    """The tarball as a GREEN parcel (a box with a strap); `text` (mono) under it. .box .text"""
    b = RoundedRectangle(width=parcel_w, height=parcel_h, corner_radius=0.05, stroke_color=color,
                         stroke_width=3).set_fill(color, 0.3)
    strap = VGroup(Line(b.get_top(), b.get_bottom()), Line(b.get_left(), b.get_right())).set_stroke(color, 3)
    knot = Dot(b.get_center(), radius=0.06, color=color)
    g = VGroup(b, strap, knot)
    g.box, g.text = b, None
    if text:
        t = mono(text, size, INK).next_to(b, DOWN, buff=0.1)
        g.add(t)
        g.text = t
    return g


def t4_chip(lit: bool = False, size: float = 20, chip_w: float = 0.62) -> VGroup:
    """A GPU as a chip glyph with pins and 'T4' (lit: BLUE fill, WHITE text; dark: GREY, unused).
    .body .text"""
    col = CLOUD if lit else S.GREY
    body = RoundedRectangle(width=chip_w, height=chip_w, corner_radius=0.06, stroke_color=col,
                            stroke_width=3).set_fill(col, 0.35 if lit else 0.05)
    pins = VGroup()
    for k in range(3):
        d = (k - 1) * chip_w * 0.28
        for a, b in (([d, chip_w / 2, 0], [d, chip_w / 2 + 0.09, 0]), ([d, -chip_w / 2, 0], [d, -chip_w / 2 - 0.09, 0]),
                     ([chip_w / 2, d, 0], [chip_w / 2 + 0.09, d, 0]), ([-chip_w / 2, d, 0], [-chip_w / 2 - 0.09, d, 0])):
            pins.add(Line(a, b, color=col, stroke_width=2.5))
    t = label("T4", size, INK if lit else S.GREY).move_to(body)
    g = VGroup(pins, body, t)
    g.body, g.text, g.lit = body, t, lit
    return g


def job_tile(hw: str = "CPU, RAM", t4: bool = False, size: float = 20, tile_w: float = 1.3,
             tile_h: float = 1.5, meter_: bool = True, name: str | None = None) -> VGroup:
    """A Vertex AI job as a BLUE tile: its hardware words at the bottom (split at ', ' onto two lines
    when narrow), a T4 chip when t4=True (.chip), a GOLD meter top-right (.meter, no numbers), a
    slot for the job's TEAL container (.slot: a point). name: a mono line above the tile (the
    job's display name). .frame .hw .chip .meter .job_name"""
    fr = RoundedRectangle(width=tile_w, height=tile_h, corner_radius=0.12, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.12)
    words = hw.split(", ") if label(hw, size).width > tile_w - 0.2 else [hw]
    hwt = VGroup(*[label(w + ("," if i < len(words) - 1 else ""), size, INK) for i, w in enumerate(words)])
    hwt.arrange(DOWN, buff=0.05).move_to(fr).align_to(fr, DOWN).shift(UP * 0.12)
    g = VGroup(fr, hwt)
    g.frame, g.hw, g.chip, g.meter, g.job_name = fr, hwt, None, None, None
    if t4:
        c = t4_chip(True, size, 0.5).next_to(hwt, UP, buff=0.18)
        g.add(c)
        g.chip = c
    if meter_:
        m = meter(0.36).move_to(fr.get_corner(UR) + np.array([-0.3, -0.25, 0]))
        g.add(m)
        g.meter = m
    if name:
        n = mono(name, size, INK).next_to(fr, UP, buff=0.1)
        g.add(n)
        g.job_name = n
    g.slot = Dot(fr.get_center() + UP * 0.15, radius=0.001).set_opacity(0)
    g.add(g.slot)
    return g


def notebook_card(which: str = "A", size: float = 20, card_w: float = 1.9, card_h: float = 0.62,
                  color=CLOUD) -> VGroup:
    """'notebook A' as a small BLUE card (the Colab runtime is remote). .frame .text"""
    fr = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.1, stroke_color=color,
                          stroke_width=2.5).set_fill(color, 0.1)
    pg = file_glyph(0.3, color)
    t = label(f"notebook {which}", size, INK)
    row = VGroup(pg, t).arrange(RIGHT, buff=0.15).move_to(fr)
    g = VGroup(fr, row)
    g.frame, g.text = fr, t
    return g


def band(text: str, color=SYSTEM, band_w: float = 2.4, band_h: float = 0.36, size: float = 20,
         dashed: bool = False, mono_font: bool = False) -> VGroup:
    """A horizontal layer band (ORANGE: a Debian base, an apt layer, what the prebuilt image is
    assumed to hold; TEAL: an image name). .box .text"""
    b = outline_box(band_w, band_h, color, solid=not dashed, fill_opacity=0.2, radius=0.06)
    t = (mono if mono_font else label)(text, size, INK).move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def flag_chip(s: str, color=OWNED, size: float = 20) -> VGroup:
    """A flag or a config key as a mono chip (GREEN: yours). .box .text"""
    return chip(s, color, size=size, font=MONO)


def file_chip(s: str, color=INK, size: float = 20) -> VGroup:
    """A small file as a chip: file glyph + mono name. .box .text"""
    t = mono(s, size, color)
    g0 = file_glyph(0.26, color)
    row = VGroup(g0, t).arrange(RIGHT, buff=0.1)
    b = RoundedRectangle(width=row.width + 0.28, height=0.42, corner_radius=0.08, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.95)
    row.move_to(b)
    g = VGroup(b, row)
    g.box, g.text = b, t
    return g


def photo_grid(cols: int = 34, rows: int = 34, cell: float = 0.07, gap: float = 0.018, color=S.GREY) -> VGroup:
    """The dataset as a grid of tiny blank tiles (34 × 34 = 1,156, notebook A's 'Full size of the
    dataset'). No photos, no labels. .tiles (list, row-major)"""
    assert cols * rows == int(DATASET_SIZE) or (cols, rows) != (34, 34)
    g = VGroup(*[Rectangle(width=cell, height=cell, stroke_width=0).set_fill(color, 0.45)
                 for _ in range(cols * rows)])
    g.arrange_in_grid(rows=rows, cols=cols, buff=gap)
    g.tiles = list(g)
    return g


def test_pick(n_total: int = 1156, k: int = 116, seed: int = 0) -> list[int]:
    """k distinct tile indices for 'the test set' of one run (deterministic per seed; S03 reshuffles
    with seed 1, 2: 'no seed: a different 116 every run')."""
    rng = np.random.default_rng(seed)
    return sorted(int(i) for i in rng.choice(n_total, size=k, replace=False))


def console(path, win_w: float = 7.0, win_h: float = 3.2, size: float = 20) -> VGroup:
    """A schematic GCP/W&B console page (no logo, no screenshot): a GREY window whose top line is
    the breadcrumb `path` ('Vertex AI', 'Training', 'Custom jobs'); tag it illustration_tag().
    Content is the scene's (README words only). .frame .crumbs .content (rectangle)"""
    fr = RoundedRectangle(width=win_w, height=win_h, corner_radius=0.14, stroke_color=LAPTOP,
                          stroke_width=2.5).set_fill(PANEL, 1)
    items = []
    for i, s in enumerate(path):
        items.append(label(s, size, INK if i == len(path) - 1 else S.GREY))
        if i < len(path) - 1:
            items.append(label("→", size, S.GREY))
    crumbs = VGroup(*items).arrange(RIGHT, buff=0.12)
    crumbs.move_to(fr.get_corner(UL) + np.array([0.3 + crumbs.width / 2, -0.32, 0]))
    sep = Line(fr.get_corner(UL) + np.array([0, -0.62, 0]), fr.get_corner(UR) + np.array([0, -0.62, 0]),
               color=S.GREY_DARK, stroke_width=2)
    content = Rectangle(width=win_w - 0.4, height=win_h - 0.85, stroke_width=0).set_fill(opacity=0)
    content.move_to(fr).align_to(fr, DOWN).shift(UP * 0.1)
    g = VGroup(fr, sep, crumbs, content)
    g.frame, g.crumbs, g.content = fr, crumbs, content
    return g


# ================================================================== V1 · TrainingMap (slide 24 + the Colab lane)
MAP_KEYS = ("nbA", "folder", "laneA", "nbB", "laneB", "laptop", "cockpit", "secrets", "key", "gcp", "bucket",
            "tarball", "vertex", "cpu_tile", "gpu_tile", "wandb", "upload", "submit", "pull", "stream")
# parts not on the map until shown (reveal(k)): the key chip, the tarball, the tiles, the four routes
MAP_HIDDEN = ("key", "tarball", "cpu_tile", "gpu_tile", "upload", "submit", "pull", "stream")
_COLAB = ("nbA", "folder", "laneA", "nbB", "laneB", "wandb")
# the map at the START of each scene (script.md 'V1'; each scene lights its own pieces)
MAP_AT = {
    "S02": dict(),
    "S03": dict(),
    "S04": dict(lit=("nbA", "folder", "laneA", "bucket")),
    "S05": dict(lit=("nbA", "folder", "laneA", "bucket", "nbB", "laneB", "wandb")),
    "S06": dict(lit=_COLAB + ("bucket",)),
    "S07": dict(lit=_COLAB + ("bucket",)),
    "S08": dict(lit=_COLAB, shown=("key",), named=True),
    "S09": dict(lit=_COLAB + ("laptop", "cockpit", "secrets", "key"), shown=("key",), named=True, base="bookworm · Debian 12"),
    "S10": dict(lit=_COLAB + ("laptop", "cockpit", "secrets", "key", "gcp", "bucket", "tarball", "upload"),
                shown=("key", "tarball", "upload"), named=True, base="bookworm · Debian 12", stamped=True),
    "S11": dict(lit=_COLAB + ("laptop", "cockpit", "secrets", "key", "gcp", "bucket", "tarball", "upload", "vertex",
                              "submit"),
                shown=("key", "tarball", "upload", "submit"), named=True, base="bookworm · Debian 12", stamped=True),
    "S15": dict(lit=MAP_KEYS, shown=MAP_HIDDEN, named=True, base="bookworm · Debian 12", stamped=True),
}


class TrainingMap(Rig):
    """V1 · the lecture's map: slide 24's three layers left to right, plus the Colab lane on top.
    Built in place for the band above a 3-row strip (x -6.5 … 6.5, y -1.3 … 2.75); never scale it.
      Colab lane (y ≈ 2.3): .parts['nbA'] (BLUE card 'notebook A') → ['laneA'] → ['folder'] (GREY
      drawer 'experiment_<ts>/') → down into the bucket; ['nbB'] → ['laneB'] → the wandb.ai building.
      Repo lane: ['laptop'] GREY frame 'laptop' (x -6.5 … -3.75) with ['cockpit'] (TEAL house
      'model-training-cli', hollow until solid()), ['secrets'] (GREEN drawer), ['key'] (GREEN chip
      'W&B key', hidden); ['gcp'] BLUE dashed boundary 'your-gcp-project' (x -2.75 … 3.6) holding
      ['bucket'] (BLUE vault titled 'bucket' until name_bucket(); ['tarball'] parcel inside, hidden)
      and ['vertex'] ('Vertex AI' with ['cpu_tile'] 'CPU, RAM' and ['gpu_tile'] with a T4, hidden);
      ['wandb'] the separate BLUE building 'wandb.ai' (x 3.85 … 6.5).
      Routes (hidden): ['upload'] PINK cockpit → bucket ('package & upload'), ['submit'] GREY
      cockpit → Vertex AI ('create job'; the cockpit has exactly these two and none into a job),
      ['pull'] PINK bucket → CPU tile (--python-package-uris), ['stream'] PINK CPU tile → wandb.ai.
    Everything starts dark (greyed) unless lit; hidden parts are not on the map until reveal().
    TrainingMap.at('S09') = the map as S09 starts (MAP_AT; kw override).
      light(*keys) / unlight(*keys) / all_dark() -> Animation   keys of MAP_KEYS
      reveal(*keys) / conceal(*keys) -> Animation               hidden parts in (lit) / out
      name_bucket() -> Animation        the bucket's title becomes your-bucket-placeholder (S07)
      relabel_base(text) -> Animation       the cockpit's ORANGE base band appears / relabels (S08)
      crack() -> VGroup                 RED cracks over the cockpit (not added; S08's failed build)
      solid() -> Animation              the cockpit house fills TEAL (it built)
      stamp() -> VGroup                 the 'submits · never trains' chip on the cockpit (S09; .stamp)
      labels(k) -> VGroup               the route's words ('package & upload' / 'create job'), not added"""

    def __init__(self, lit=(), shown=(), named: bool = False, base: str | None = None, stamped: bool = False,
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        P = {}
        # ---- Colab lane
        P["nbA"] = notebook_card("A", size).move_to([-5.45, 2.3, 0])
        P["folder"] = drawer("experiment_<ts>/", LAPTOP, size).move_to([-0.95, 2.3, 0])
        P["nbB"] = notebook_card("B", size).move_to([1.95, 2.3, 0])
        # ---- repo lane frames
        self.laptop_frame = RoundedRectangle(width=2.95, height=2.75, corner_radius=0.16, stroke_color=LAPTOP,
                                             stroke_width=2.5).set_fill(LAPTOP, 0.04).move_to([-5.025, 0.075, 0])
        lt = label("laptop", size, LAPTOP).move_to(self.laptop_frame.get_corner(UL) + np.array([0.15, -0.22, 0]),
                                                   aligned_edge=LEFT)
        P["laptop"] = VGroup(self.laptop_frame, lt)
        P["cockpit"] = house(COCKPIT, 2.45, 0.95, IMAGE, size=size).move_to([-5.025, 0.0, 0], aligned_edge=DOWN)
        P["secrets"] = drawer("secrets/", KEY, size, drawer_w=1.5, glyph=False).move_to([-5.65, -0.85, 0])
        P["key"] = chip("W&B key", KEY, size=size, pad_x=0.12).move_to([-4.27, -0.85, 0])
        gfr = outline_box(6.2, 2.75, CLOUD, solid=False).move_to([0.5, 0.075, 0])
        gt = mono(PROJECT_ID, size, CLOUD).move_to(gfr.get_corner(UL) + np.array([0.15, -0.22, 0]), aligned_edge=LEFT)
        P["gcp"] = VGroup(gfr, gt)
        bfr = RoundedRectangle(width=3.0, height=1.3, corner_radius=0.14, stroke_color=CLOUD,
                               stroke_width=3).set_fill(CLOUD, 0.08).move_to([-0.95, 0.4, 0])
        self.bucket_title = steady("bucket", size, CLOUD).move_to(bfr.get_top() + DOWN * 0.25)
        P["bucket"] = VGroup(bfr, self.bucket_title)
        P["tarball"] = parcel(None, OWNED, size, 0.55, 0.4).move_to(bfr.get_center() + DOWN * 0.18)
        vfr = RoundedRectangle(width=2.8, height=2.3, corner_radius=0.14, stroke_color=CLOUD,
                               stroke_width=2.5).set_fill(CLOUD, 0.05).move_to([2.1, 0.0, 0])
        vt = label("Vertex AI", size, CLOUD).move_to(vfr.get_top() + DOWN * 0.24)
        P["vertex"] = VGroup(vfr, vt)
        P["cpu_tile"] = job_tile("CPU, RAM", False, size, 1.25, 1.55).move_to([1.42, -0.27, 0])
        P["gpu_tile"] = job_tile("GPU", True, size, 1.25, 1.55).move_to([2.78, -0.27, 0])
        wb = building(WB_HOST, 2.4, 2.45, size)
        P["wandb"] = wb.move_to([5.17, -1.3, 0], aligned_edge=DOWN)
        # ---- routes
        hr = P["cockpit"].body.get_right()[0]
        P["laneA"] = VGroup(arrow(P["nbA"].frame.get_right(), P["folder"].get_left(), LAPTOP, buff=0.1),
                            arrow(np.array([-0.95, P["folder"].get_bottom()[1], 0]),
                                  np.array([-0.95, bfr.get_top()[1] + 0.02, 0]), LAPTOP))
        bx = wb.get_center()[0]
        P["laneB"] = _poly([P["nbB"].frame.get_right() + RIGHT * 0.08, [bx, 2.3, 0], [bx, wb.get_top()[1] + 0.08, 0]],
                           ROUTE, 3)
        P["upload"] = _poly([[hr + 0.05, 0.42, 0], [bfr.get_left()[0] - 0.05, 0.42, 0]], ROUTE, 4)
        P["submit"] = _poly([[hr + 0.05, 0.15, 0], [-3.08, 0.15, 0], [-3.08, -0.95, 0], [vfr.get_left()[0] - 0.05, -0.95, 0]],
                            LAPTOP, 3)
        ct = P["cpu_tile"]
        P["pull"] = _poly([[bfr.get_right()[0] + 0.02, 0.4, 0], [ct.frame.get_left()[0] - 0.02, 0.4, 0]], ROUTE, 3)
        P["stream"] = _poly([[ct.frame.get_center()[0], ct.frame.get_bottom()[1] - 0.02, 0],
                             [ct.frame.get_center()[0], -1.18, 0], [wb.get_left()[0] + 0.1, -1.18, 0]], ROUTE, 3)
        self.parts = P
        self.base = band("", SYSTEM, 2.45, 0.34, size)
        self.base.move_to([-5.025, -0.24, 0])
        self.base_text = None
        self._lit = {k: P[k].copy() for k in MAP_KEYS}
        self.state = {k: False for k in MAP_KEYS}
        self.shown = {k: k not in MAP_HIDDEN or k in shown for k in MAP_KEYS}
        order = ("gcp", "laptop", "wandb", "vertex", "bucket", "nbA", "folder", "nbB", "laneA", "laneB", "cockpit",
                 "secrets", "key", "tarball", "cpu_tile", "gpu_tile", "upload", "submit", "pull", "stream")
        for k in order:
            if self.shown[k]:
                self.add(P[k])
        self.ride(*[P[k] for k in MAP_HIDDEN if not self.shown[k]], *self._lit.values(), self.base)
        if named:
            self._lit["bucket"] = self._named_bucket()
        for k in MAP_KEYS:
            self._apply(k, k in lit)
        self.cockpit_solid = False
        if base:
            self._set_base_now(base)
        self.stamp_ = None
        if stamped:
            self.stamp_ = self.stamp()
            self.add(self.stamp_)

    @classmethod
    def at(cls, scene_id: str, **kw) -> "TrainingMap":
        """The map as it stands when scene `scene_id` ('S09') starts (MAP_AT; kw overrides)."""
        return cls(**{**MAP_AT[scene_id], **kw})

    # ---- lit / dark
    def _version(self, k, on: bool):
        v = self._lit[k].copy().move_to(self.parts[k])
        if k == "cockpit":
            v = lit_house(v, getattr(self, "cockpit_solid", False))
        return v if on else greyed(v)

    def _apply(self, k, on: bool):
        self.state[k] = on
        self.parts[k].become(self._version(k, on))

    def light(self, *keys, run_time: float = 0.7):
        """Animation: pieces `keys` take their colours (BLUE remote, TEAL cockpit, GREEN yours, PINK routes)."""
        anims = []
        for k in keys:
            self.state[k] = True
            anims.append(Transform(self.parts[k], self._version(k, True)))
        return AnimationGroup(*anims, run_time=run_time)

    def unlight(self, *keys, run_time: float = 0.7):
        anims = []
        for k in keys:
            self.state[k] = False
            anims.append(Transform(self.parts[k], self._version(k, False)))
        return AnimationGroup(*anims, run_time=run_time)

    def all_dark(self, run_time: float = 1.0):
        return self.unlight(*[k for k in MAP_KEYS if self.state[k] and self.shown[k]], run_time=run_time)

    def reveal(self, *keys, run_time: float = 0.8):
        """Animation: hidden parts appear lit (routes draw, the rest fade in)."""
        anims = []
        for k in keys:
            if self.shown[k]:
                continue
            self.shown[k] = True
            self.state[k] = True
            m = self.parts[k]
            m.become(self._version(k, True))
            self.add(m)
            anims.append(Create(m) if k in ("upload", "submit", "pull", "stream") else FadeIn(m, scale=0.9))
        return AnimationGroup(*anims, run_time=run_time)

    def conceal(self, *keys, run_time: float = 0.6):
        """Animation: parts leave the map (a tile vanishing, a route gone)."""
        anims = []
        for k in keys:
            if not self.shown[k]:
                continue
            self.shown[k] = False
            m = self.parts[k]
            self.remove(m)
            anims.append(FadeOut(m))
        return AnimationGroup(*anims, run_time=run_time)

    # ---- the bucket, the cockpit
    def _named_bucket(self) -> VGroup:
        fr, t = self._lit["bucket"][0].copy(), self._lit["bucket"][1]
        return VGroup(fr, steady(BUCKET, self.size, CLOUD).move_to(t))

    def name_bucket(self, run_time: float = 0.7):
        """Animation: the bucket's title 'bucket' becomes your-bucket-placeholder (S07)."""
        self._lit["bucket"] = self._named_bucket()
        return Transform(self.parts["bucket"], self._version("bucket", self.state["bucket"]), run_time=run_time)

    def _set_base_now(self, text):
        b = band(text, SYSTEM, 2.45, 0.34, self.size).move_to(self.base)
        self.base.become(b)
        self.base.text = self.base[1]
        self.base_text = text
        if self.base not in self.submobjects:
            self.add(self.base)

    def relabel_base(self, text: str, run_time: float = 0.7):
        """Animation: the cockpit's ORANGE base band (Debian under the image) appears or relabels:
        'bullseye · Debian 11' → 'bookworm · Debian 12'."""
        new = band(text, SYSTEM, 2.45, 0.34, self.size).move_to(self.base)
        if self.base_text is None:
            self.base.become(new)
            self.base_text = text
            self.add(self.base)
            return FadeIn(self.base, shift=UP * 0.1, run_time=run_time)
        self.base_text = text
        return Transform(self.base, new, run_time=run_time)

    def crack(self) -> VGroup:
        """RED cracks over the cockpit house (not added): the failed builds."""
        h = self.parts["cockpit"].body
        c = h.get_center()
        pts1 = [c + np.array([-0.5, 0.33, 0]), c + np.array([-0.3, 0.05, 0]), c + np.array([-0.45, -0.1, 0]),
                c + np.array([-0.25, -0.31, 0])]
        pts2 = [c + np.array([0.75, 0.33, 0]), c + np.array([0.6, 0.1, 0]), c + np.array([0.78, -0.05, 0]),
                c + np.array([0.62, -0.31, 0])]
        return VGroup(*[VMobject(stroke_color=ERR, stroke_width=4).set_points_as_corners(p) for p in (pts1, pts2)])

    def solid(self, run_time: float = 0.8):
        """Animation: the cockpit house fills TEAL (the image built; S08's third run)."""
        self.cockpit_solid = True
        return Transform(self.parts["cockpit"], self._version("cockpit", self.state["cockpit"]), run_time=run_time)

    def stamp(self) -> VGroup:
        """The cockpit's stamp, 'submits · never trains' (two lines, GREY chip above the house; not
        added). Proved in S09 by No module named 'tensorflow'."""
        t = VGroup(label("submits ·", self.size, INK), label("never trains", self.size, INK)).arrange(DOWN, buff=0.04)
        b = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.2, corner_radius=0.1, stroke_color=S.GREY,
                             stroke_width=2).set_fill(S.GREY_DARKER, 1)
        t.move_to(b)
        g = VGroup(b, t)
        g.box, g.text = b, t
        return g.move_to([-4.3, 1.02, 0])

    def labels(self, k: str) -> VGroup:
        """The words of route k (not added): 'upload' → 'package & upload' (two lines in the gap
        above it), 'submit' → 'create job' (under the bucket)."""
        if k == "upload":
            return VGroup(note("package", INK), note("& upload", INK)).arrange(DOWN, buff=0.03).move_to([-3.08, 0.98, 0])
        if k == "submit":
            return note("create job", INK).move_to([-0.95, -0.95, 0])
        raise KeyError(k)


# ================================================================== V2 · RunLedger (runs as WHITE rows)
REPO_CONFIG = (("learning_rate", "task.py:274"), ("epochs", "--epochs"), ("batch_size", "--batch_size"),
               ("model_name", "model.name"), ("execution_time", "task.py:336"))


class RunLedger(Rig):
    """V2 · a stored notebook table as a ledger of WHITE rows (one row = one run), the columns of
    script.md (default name · epochs · accuracy), values verbatim from nb_table().
      RunLedger('A')  -> cell 54's table (nbA:1283-1295)   RunLedger('B') -> cell 55's (nbB:1703-1715)
    Built centred at the origin (move it); 20 pt, run names in the label font, numbers in mono
    (6.5 wide: two fit side by side with frame=False, S01); header 'notebook A · cell 54' and the
    GREY recorded tag under its right end (tag_=False: none). .rows (each a VGroup: .frame, .cells {column: Text},
    .name) .heads (column titles) .frame .header .tag
      find(name) -> int                 the row index of a run name
      ring_row(i, colour) -> VGroup     an outline around row i (not added)
      cell(i, column) -> Text           one cell
      slots(slot_w) -> VGroup           S04: one GREY-dashed curve slot right of every row + the
                                        shared epoch axis under them (not added; .boxes .axis)
      curves(box, keys) -> VGroup       notebook B's recorded 'Run history' sparklines (2_block,
                                        nbB:1010-1014) drawn inside a slot box (not added)
      callback_pipe(start, box) -> VGroup  the PURPLE callback pipe from a point to a slot (not added)
      collapse(i, j, text) -> (VGroup, Animation)  two rows' names fold under one label (S04's
                                        'mobilenetv2_train_base', nbB:1629)"""

    def __init__(self, which: str = "A", columns=("name", "epochs", "accuracy"), size: float = 20,
                 rows=None, tag_: bool = True, header: str | None = None, row_h: float = 0.46,
                 frame: bool = True, gap: float = 0.25):
        super().__init__()
        self.which, self.size, self.columns = which, size, columns
        first, last, cell_no = (1283, 1295, 54) if which == "A" else (1703, 1715, 55)
        rows = rows if rows is not None else table_rows(which, first, last, columns)

        def font(j, s, col=RUN):
            # run names and column titles in the label font (27-28 characters: mono would not fit two
            # tables side by side), numbers in mono; the text itself is verbatim
            return (mono if re.fullmatch(r"[\d.,%]+", s) else label)(s, size, col)

        widths = [max(font(j, c).width, *[font(j, r[j]).width for r in rows]) for j, c in enumerate(columns)]
        xs, x = [], 0.0
        for w in widths:
            xs.append(x)
            x += w + gap
        total = x - gap
        self.heads = VGroup(*[font(j, c, S.GREY) for j, c in enumerate(columns)])
        for j, (t, x0) in enumerate(zip(self.heads, xs)):
            if j > 0:
                t.move_to([x0 - total / 2 + widths[j] - t.width / 2, 0, 0])
            else:
                t.move_to([x0 - total / 2 + t.width / 2, 0, 0])
        self.rows = []
        for i, r in enumerate(rows):
            y = -(i + 1) * row_h
            cells = {}
            for j, (c, x0) in enumerate(zip(columns, xs)):
                t = font(j, r[j])
                if j > 0:                                   # values right-aligned under their head
                    t.move_to([x0 - total / 2 + widths[j] - t.width / 2, y, 0])
                else:
                    t.move_to([x0 - total / 2 + t.width / 2, y, 0])
                cells[c] = t
            fr = RoundedRectangle(width=total + 0.2, height=row_h - 0.08, corner_radius=0.06, stroke_color=RUN,
                                  stroke_width=1.5, stroke_opacity=0.55).move_to([0, y, 0])
            rg = VGroup(fr, *cells.values())
            rg.frame, rg.cells, rg.name = fr, cells, r[0]
            self.rows.append(rg)
        body = VGroup(self.heads, *self.rows)
        self.header = label(header or f"notebook {which} · cell {cell_no}", CAPTION, S.GREY)
        if frame:
            self.frame = RoundedRectangle(width=total + 0.7, height=body.height + 0.95, corner_radius=0.14,
                                          stroke_color=CLOUD, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
            self.frame.move_to(body).shift(UP * 0.2)
            self.header.move_to(self.frame.get_corner(UL) + np.array([0.25 + self.header.width / 2, -0.25, 0]))
            self.add(self.frame, self.header, body)
        else:                                               # compact: no outer frame (S01's two tables)
            self.frame = Rectangle(width=total + 0.2, height=body.height + 0.55, stroke_width=0).set_fill(opacity=0)
            self.frame.move_to(body).shift(UP * 0.25)
            self.header.next_to(self.heads, UP, buff=0.2).align_to(self.rows[0].frame, LEFT)
            self.add(self.frame, self.header, body)
        self.tag = None
        if tag_:
            self.tag = nb_recorded_tag(which).next_to(self.rows[-1].frame, DOWN, buff=0.15)
            self.tag.align_to(self.rows[-1].frame, RIGHT)
            self.add(self.tag)
        self.row_h, self.total = row_h, total

    def find(self, name: str) -> int:
        for i, r in enumerate(self.rows):
            if r.name == name:
                return i
        raise KeyError(name)

    def cell(self, i: int, column: str):
        return self.rows[i].cells[column]

    def ring_row(self, i: int, color=TURN, stroke: float = 3) -> VGroup:
        return ring(self.rows[i].frame, color, buff=0.03, stroke=stroke)

    def slots(self, slot_w: float = 3.0, epochs: int = 25) -> VGroup:
        """S04: a GREY-dashed curve slot right of every row (.boxes[i]) and one shared epoch axis
        under them (.axis: line + 'epoch' + '1' … '25', from the 2_block run's 25 epochs). Not added."""
        x0 = self.frame.get_right()[0] + 0.25
        boxes = []
        for r in self.rows:
            b = outline_box(slot_w, self.row_h - 0.08, S.GREY, solid=False, radius=0.05)
            b.move_to([x0 + slot_w / 2, r.frame.get_center()[1], 0])
            boxes.append(b)
        yb = self.rows[-1].frame.get_bottom()[1] - 0.2
        ax = Line([x0, yb, 0], [x0 + slot_w, yb, 0], color=S.GREY, stroke_width=2.5)
        t1 = mono("1", 20, S.GREY).next_to(ax.get_start(), DOWN, buff=0.08)
        t2 = mono(str(epochs), 20, S.GREY).next_to(ax.get_end(), DOWN, buff=0.08)
        tl = label("epoch · one shared axis", 20, S.GREY).next_to(ax, DOWN, buff=0.08)
        axis = VGroup(ax, t1, t2, tl)
        g = VGroup(*boxes, axis)
        g.boxes, g.axis = boxes, axis
        return g

    @staticmethod
    def curves(slot, keys=("accuracy", "loss"), colors=(INK, S.GREY)) -> VGroup:
        """The 2_block run's recorded sparklines (nbB:1010-1014, levels 0-7 over 25 epochs) drawn
        inside slot box `slot` (not added). .lines {key: VMobject}"""
        g = VGroup()
        g.lines = {}
        w, h = slot.width - 0.2, slot.height - 0.12
        c = slot.get_center()
        for k, col in zip(keys, colors):
            lv = sparkline(k)
            pts = [c + np.array([-w / 2 + w * i / (len(lv) - 1), -h / 2 + h * v / 7, 0]) for i, v in enumerate(lv)]
            ln = VMobject(stroke_color=col, stroke_width=3).set_points_as_corners(pts)
            g.add(ln)
            g.lines[k] = ln
        return g

    @staticmethod
    def callback_pipe(start, slot) -> VGroup:
        """The PURPLE callback pipe from point `start` (model.fit in a code panel) to slot `slot`."""
        s = np.array(start)
        e = slot.get_left() + LEFT * 0.04
        mid = [(s[0] + e[0]) / 2, s[1], 0]
        return pipe([s, mid, [mid[0], e[1], 0], e], TOOL, 4)

    def collapse(self, i: int, j: int, text: str):
        """Rows i and j (adjacent) share one display name: their name cells fold into one label
        between them. Returns (label, Animation)."""
        a, b = self.rows[i].cells["name"], self.rows[j].cells["name"]
        t = label(text, self.size, RUN)
        t.move_to([a.get_left()[0] + t.width / 2, (a.get_center()[1] + b.get_center()[1]) / 2, 0])
        br = Line([a.get_left()[0] - 0.12, a.get_top()[1], 0], [a.get_left()[0] - 0.12, b.get_bottom()[1], 0],
                  color=TURN, stroke_width=3)
        lab = VGroup(br, t)
        return lab, AnimationGroup(ReplacementTransform(VGroup(a.copy(), b.copy()), t), FadeOut(a), FadeOut(b),
                                   Create(br))


class ExperimentFolder(Rig):
    """V2's first build (S03): notebook A's home-made tracker, the folder `experiment_1760994796/`
    (name from nbA:1304) as a GREY card with five stacks (one per model) of five blank WHITE file
    glyphs, and a legend of the five suffixes (cell 12's code: .keras · .weights.h5 · .json ·
    _train_history.json · _model_metrics.json). Built empty; drop(i) fills stack i.
      drop(i) -> Animation      five files fall into stack i (i = 0..4)
      .card .title .legend .stacks (the 5×5 file glyphs, not added until dropped)"""

    def __init__(self, size: float = 20):
        super().__init__()
        title = mono(EXPERIMENT + "/", size + 2, INK)
        leg = VGroup(*[VGroup(file_glyph(0.26, INK), mono(s, size, INK)).arrange(RIGHT, buff=0.12)
                       for s in FIVE_FILES]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        self.stacks = []
        for i in range(5):
            st = VGroup(*[file_glyph(0.34, INK) for _ in FIVE_FILES]).arrange(DOWN, buff=0.06)
            self.stacks.append(st)
        sgrid = VGroup(*[outline_box(0.6, 2.4, S.GREY, solid=False, radius=0.06) for _ in range(5)]).arrange(RIGHT,
                                                                                                          buff=0.18)
        for st, b in zip(self.stacks, sgrid):
            st.move_to(b)
        inner = VGroup(sgrid, leg).arrange(RIGHT, buff=0.6)
        body = VGroup(title, inner).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fr = RoundedRectangle(width=body.width + 0.7, height=body.height + 0.6, corner_radius=0.16,
                              stroke_color=LAPTOP, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        body.move_to(fr)
        fg = folder_glyph(0.34, LAPTOP).next_to(title, LEFT, buff=0.15)
        self.add(fr, fg, title, sgrid, leg)
        self.card, self.title, self.legend, self.slots_ = fr, title, leg, sgrid
        self.ride(*self.stacks)

    def drop(self, i: int, run_time: float = 0.8):
        st = self.stacks[i]
        self.add(st)
        return LaggedStart(*[FadeIn(f, shift=DOWN * 0.35) for f in st], lag_ratio=0.12, run_time=run_time)


class RunRecord(Rig):
    """V2 in S12: the repo run's row as slide 9's seven columns (environment · code · data · model ·
    metrics · artifacts · notes), filled cells WHITE, empty cells GREY-dashed; tag illustration (no
    numbers, no dashboard chrome). Row label: run name + project from task.py (:263/:321, :314).
      mark(col, state, words=None) -> VGroup   'yes' (WHITE cell + GREEN check), 'partly' (half
                                    cell), 'no' (GREY-dashed cell + GREY cross); words: a GREY note
                                    under the cell (not added)
      .heads .cells (dict column -> box) .run_label .tag"""

    def __init__(self, name: str = "mobilenetv2_train_base_True", project: str = WB_PROJECT_REPO,
                 size: float = 20, cell_w: float = 1.68):
        super().__init__()
        self.size, self.cell_w = size, cell_w
        self.heads = VGroup(*[label(c, size, S.GREY) for c in SLIDE9])
        self.cells = {}
        boxes = VGroup()
        for j, c in enumerate(SLIDE9):
            b = outline_box(cell_w - 0.1, 0.62, S.GREY, solid=False, radius=0.06)
            b.move_to([(j - 3) * cell_w, 0, 0])
            self.cells[c] = b
            boxes.add(b)
            self.heads[j].next_to(b, UP, buff=0.12)
        self.run_label = VGroup(mono(name, size, RUN), label(f"· W&B project {project}", size, S.GREY))
        self.run_label.arrange(RIGHT, buff=0.15).next_to(self.heads, UP, buff=0.25).align_to(boxes, LEFT)
        self.tag = illustration_tag().next_to(boxes, DOWN, buff=0.12).align_to(boxes, RIGHT)
        self.add(self.run_label, self.heads, boxes, self.tag)
        self.boxes = boxes

    def mark(self, col: str, state: str = "yes", words: str | None = None) -> VGroup:
        b = self.cells[col]
        if state == "yes":
            fill = RoundedRectangle(width=b.width, height=b.height, corner_radius=0.06, stroke_color=RUN,
                                    stroke_width=2).set_fill(RUN, 0.12).move_to(b)
            gl = check_mark(0.3, PASS).move_to(b)
        elif state == "partly":
            fill = RoundedRectangle(width=b.width / 2, height=b.height, corner_radius=0.06, stroke_color=RUN,
                                    stroke_width=2).set_fill(RUN, 0.12).move_to(b).align_to(b, LEFT)
            gl = VGroup(Circle(radius=0.15, stroke_color=INK, stroke_width=3),
                        Arc(radius=0.15, start_angle=PI / 2, angle=PI, stroke_width=0).set_fill(INK, 1))
            gl.move_to(b)
        else:
            fill = VGroup()
            gl = cross_mark(0.26, S.GREY).move_to(b)
        g = VGroup(fill, gl)
        if words:
            ws = VGroup(*[note(w) for w in words.split("\n")]).arrange(DOWN, buff=0.04).next_to(b, DOWN, buff=0.12)
            g.add(ws)
            g.words = ws
        return g


def config_chips(size: float = 20) -> VGroup:
    """S12: the repo run's config keys as GREEN chips, each pointing to its source in GREY
    ('learning_rate ← task.py:274', 'epochs ← --epochs' …, REPO_CONFIG), stacked. No values."""
    rows = VGroup()
    for k, src in REPO_CONFIG:
        rows.add(VGroup(flag_chip(k, OWNED, size), label("←", size, S.GREY), mono(src, size, S.GREY))
                 .arrange(RIGHT, buff=0.15))
    return rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)


# ================================================================== V3 · ConfigBinding (the assignment that goes nowhere)
class ConfigBinding(Rig):
    """V3 (S05): a BLUE run box with a GREEN `Config` drawer inside; the name `wandb.config` is a
    YELLOW sticky label riding a PINK arrow that `wandb.init` (PURPLE chip) points at the drawer.
    Built in place, ~12.4 × 3.9 (x -6.2 … 6.2, y -1.3 … 2.6). Nothing but the run box is added.
      bind() -> Animation       init chip, arrow and label appear (the name points at the drawer)
      rebind() -> Animation     `wandb.config = {...}`: a loose WHITE dict (RED outline) appears
                                outside the run with the four keys (nbB:698-703); the label peels
                                off and sticks on it; the arrow re-points
      write_update() -> Animation  `.update({"execution_time": …})` writes into whatever the name holds
                                (the loose dict after rebind(); the drawer otherwise)
      finish() -> Animation     the run box closes (a lid) and its drawer is stamped: '{}' (RED,
                                C38:17) or, after fill(), GREEN 'Config · 5 keys' (C38b:16-17)
      fill() -> Animation       the fixed replay: config={...} inside init, the four keys drop
                                straight into the drawer
    Keys only, never values. .run .drawer .init .label .arrow .loose (not added) .rows"""

    def __init__(self, size: float = 22):
        super().__init__()
        self.size = size
        rf = RoundedRectangle(width=5.6, height=3.6, corner_radius=0.18, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.06).move_to([-3.4, 0.6, 0])
        rt = label("run", size, CLOUD).move_to(rf.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=LEFT)
        df = RoundedRectangle(width=4.4, height=2.5, corner_radius=0.12, stroke_color=OWNED,
                              stroke_width=3).set_fill(OWNED, 0.08).move_to([-3.4, 0.35, 0])
        dt = mono("Config", size, OWNED).move_to(df.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=LEFT)
        self.run = VGroup(rf, rt)
        self.drawer = VGroup(df, dt)
        self.add(self.run, self.drawer)
        self.init = chip("wandb.init(project=…)", TOOL, size=size, font=MONO).move_to([2.6, 2.3, 0])
        self.label = sticky("wandb.config", TURN, size)
        self.label.move_to([1.0, 1.25, 0])
        self.arrow = Arrow(self.label.get_left(), df.get_right(), buff=0.1, color=ROUTE, stroke_width=5,
                           tip_length=0.24)
        self.init_link = DashedLine(self.init.get_bottom(), self.label.get_top() + UP * 0.02, color=TOOL,
                                    stroke_width=3)
        # the loose dict outside the run (RED outline: config that went nowhere)
        lf = RoundedRectangle(width=4.3, height=2.6, corner_radius=0.12, stroke_color=ERR, stroke_width=3)
        lf.set_fill(S.GREY_DARKER, 1).move_to([3.7, -0.35, 0])
        lt = mono("dict", size, INK).move_to(lf.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=LEFT)
        self.loose = VGroup(lf, lt)
        self.loose_rows = self._rows(CONFIG_KEYS, lf)
        self.drawer_rows = self._rows(CONFIG_KEYS, df)
        self.extra_row_loose = self._rows(CONFIG_KEYS + ("execution_time",), lf)[-1]
        self.extra_row_drawer = self._rows(CONFIG_KEYS + ("execution_time",), df)[-1]
        self.lid = Line(rf.get_corner(UL) + RIGHT * 0.1, rf.get_corner(UR) + LEFT * 0.1, color=CLOUD, stroke_width=8)
        self.points_at = "drawer"
        self.filled = False
        self.ride(self.init, self.label, self.arrow, self.init_link, self.loose, *self.loose_rows,
                  *self.drawer_rows, self.extra_row_loose, self.extra_row_drawer, self.lid)

    def _rows(self, keys, fr):
        rows = []
        top = fr.get_top()[1] - 0.6
        for i, k in enumerate(keys):
            t = mono(f'"{k}": …', 20, INK)
            t.move_to([fr.get_left()[0] + 0.35 + t.width / 2, top - i * 0.36, 0])
            rows.append(t)
        return rows

    def bind(self, run_time: float = 1.2):
        self.add(self.init, self.init_link, self.arrow, self.label)
        return LaggedStart(FadeIn(self.init, shift=DOWN * 0.2), Create(self.init_link), GrowArrow(self.arrow),
                           FadeIn(self.label, scale=1.2), lag_ratio=0.35, run_time=run_time)

    def rebind(self, run_time: float = 1.6):
        lf = self.loose[0]
        spot = lf.get_top() + UP * (self.label.height / 2 + 0.12) + LEFT * 0.5
        new_arrow = Arrow(spot + DOWN * self.label.height / 2, lf.get_top() + LEFT * 0.5 + DOWN * 0.02, buff=0.05,
                          color=ROUTE, stroke_width=5, tip_length=0.24)
        self.add(self.loose, *self.loose_rows)
        self.points_at = "loose"
        return Succession(
            AnimationGroup(FadeIn(self.loose, shift=LEFT * 0.3), LaggedStart(*[FadeIn(r) for r in self.loose_rows],
                                                                             lag_ratio=0.15)),
            AnimationGroup(self.label.animate.move_to(spot), Transform(self.arrow, new_arrow),
                           self.init_link.animate.set_opacity(0.25)),
            run_time=run_time)

    def write_update(self, run_time: float = 0.8):
        r = self.extra_row_loose if self.points_at == "loose" else self.extra_row_drawer
        self.add(r)
        return FadeIn(r, shift=DOWN * 0.15, run_time=run_time)

    def fill(self, run_time: float = 1.2):
        """The fixed replay (config inside init): the label stays on the drawer, the four keys drop in."""
        self.filled = True
        self.add(*self.drawer_rows)
        return LaggedStart(*[FadeIn(r, shift=DOWN * 0.4) for r in self.drawer_rows], lag_ratio=0.2, run_time=run_time)

    def finish(self, run_time: float = 1.0) -> Animation:
        df = self.drawer[0]
        if self.filled:
            st = VGroup(check_mark(0.3, PASS), mono("Config · 5 keys", self.size, PASS)).arrange(RIGHT, buff=0.15)
            st.move_to(df.get_corner(DR) + np.array([-st.width / 2 - 0.2, 0.3, 0]))
        else:
            st = mono("{}", 44, ERR).move_to(df.get_center() + DOWN * 0.1)
        self.stamp_ = st
        self.add(self.lid, st)
        return Succession(Create(self.lid), FadeIn(st, scale=1.6), run_time=run_time)


# ================================================================== V4 · TarballTrip (what travels from laptop to Vertex)
NB_GLOBALS = ("epochs = 15", "batch_size = 32", "model = …")       # slide 23 with real names (notebook A's table)


class TarballTrip(Rig):
    """V4 · what travels: five stages, each a separate builder (a scene shows one at a time; all
    built in place for the band above a 3-row strip unless noted; text >= 20 pt).
      TarballTrip.flags()  step 1 (S06): .nb (BLUE notebook card: epochs = 15 · batch_size = 32 ·
          model = …) and .task (GREEN 'task.py' card with the five FLAGS rows, .rows, not added);
          .peel() -> Animation: the three values leave the notebook and become --epochs,
          --batch_size, --model_name; .more() -> Animation: --train_base, --wandb_key join.
      TarballTrip.pack()   step 2 (S09): GREEN .package box 'package/' with .trainer drawer; file
          chips .files ('task.py', '__init__.py', outside); .setup label ('setup.py · install_requires
          = wandb==0.15.11'), PURPLE .tar / .gzip chips, the .parcel ('4016 bytes', from laptop/30:54).
          .drop() / .clip() / .wrap() / .shrink() -> Animations (in that order);
          .upload(point, fail=True) -> (route, Animation): PINK gsutil cp to `point`, a RED '404'
          chip at its end when fail (our placeholder bucket) — .upload_fail holds the chip.
      TarballTrip.spec()   step 3 (S10): the job-spec card .card with .chips (name, machine,
          replicas, image, package, module, args — words from laptop/40:77, the hex cropped);
          .assemble(i) -> Animation; .redden() -> Animation (the W&B key inside --args turns RED);
          .fly(point) -> Animation.
      TarballTrip.vm(mini=False)  step 4 (S06 miniature with mini=True; S11 full): BLUE VM box with a
          GOLD meter, Google's TEAL image band 'tf-cpu.2-17.py310' with the ORANGE layer
          'TensorFlow · scikit-learn · expected' (.layer), the parcel landing and unwrapping to
          'trainer/', a GREEN 'wandb 0.15.11' chip (pip install), the argv tokens (gcloud splits
          --args at commas: python -m trainer.task + ARGV), PINK streams to 'logs' and 'wandb.ai'.
          .appear() .image_in() .unwrap() .pip() .run() .streams() .dissolve() -> Animations, in order;
          .dissolve() leaves .ghost: the trained weights as a GREY-dashed ghost (never saved).
      TarballTrip.standin()  S11: a dashed TEAL container 'plain python:3.10 · not Google's image'.
    Your Docker image never makes the trip: no builder here carries the cockpit."""

    # ---------------------------------------------------------------- step 1
    @classmethod
    def flags(cls, size: float = 22) -> "TarballTrip":
        g = cls()
        nb_rows = VGroup(*[mono(s, size, INK) for s in NB_GLOBALS]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        nfr = RoundedRectangle(width=nb_rows.width + 1.2, height=nb_rows.height + 1.0, corner_radius=0.14,
                               stroke_color=CLOUD, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        nt = label("notebook", 20, CLOUD).move_to(nfr.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=LEFT)
        nb_rows.move_to(nfr).shift(DOWN * 0.15)
        g.nb = VGroup(nfr, nt, nb_rows).move_to([-3.6, 0.7, 0])
        g.nb.rows = nb_rows
        trows = VGroup(*[mono(f, size, INK) for f in FLAGS]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        tfr = RoundedRectangle(width=trows.width + 1.4, height=trows.height + 1.0, corner_radius=0.14,
                               stroke_color=OWNED, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        tt = mono("task.py", 20, OWNED).move_to(tfr.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=LEFT)
        trows.move_to(tfr).shift(DOWN * 0.15)
        g.task = VGroup(tfr, tt).move_to([3.4, 0.7, 0])
        trows.move_to(tfr).shift(DOWN * 0.15)
        g.task.rows = list(trows)
        g.add(g.nb)
        g.ride(g.task, *trows)
        return g

    def peel(self, run_time: float = 1.6):
        """Animation: the task card appears; epochs/batch_size/model leave the notebook as flags."""
        self.add(self.task, *self.task.rows[:3])
        moves = [ReplacementTransform(self.nb.rows[i].copy(), self.task.rows[i]) for i in range(3)]   # FLAGS order
        return Succession(FadeIn(self.task, shift=UP * 0.3),
                          AnimationGroup(*moves, self.nb.rows.animate.set_opacity(0.35), lag_ratio=0.2),
                          run_time=run_time)

    def more(self, run_time: float = 0.8):
        self.add(*self.task.rows[3:])
        return LaggedStart(*[FadeIn(r, shift=UP * 0.3) for r in self.task.rows[3:]], lag_ratio=0.3, run_time=run_time)

    # ---------------------------------------------------------------- step 2
    @classmethod
    def pack(cls, size: float = 20) -> "TarballTrip":
        g = cls()
        pfr = RoundedRectangle(width=3.6, height=2.4, corner_radius=0.14, stroke_color=OWNED,
                               stroke_width=3).set_fill(OWNED, 0.06).move_to([-2.6, 0.55, 0])
        pt = mono("package/", size, OWNED).move_to(pfr.get_corner(UL) + np.array([0.2, -0.25, 0]), aligned_edge=LEFT)
        g.package = VGroup(pfr, pt)
        g.trainer = drawer("trainer/", OWNED, size, drawer_w=2.9).move_to(pfr.get_center() + DOWN * 0.05)
        g.files = [file_chip("task.py", INK, size).move_to([-5.4, 1.6, 0]),
                   file_chip("__init__.py", INK, size).move_to([-5.4, 0.9, 0])]
        g.slots_ = [g.trainer.get_center() + np.array([-0.15, -0.55, 0]), g.trainer.get_center() + np.array([1.0, -0.55, 0])]
        g.setup = sticky("setup.py · install_requires = wandb==0.15.11", OWNED, size)
        g.setup.next_to(pfr, DOWN, buff=0.18).align_to(pfr, LEFT)
        g.tar = tool_chip("tar", size).next_to(pfr, RIGHT, buff=0.45).shift(UP * 0.5)
        g.gzip = tool_chip("gzip", size).next_to(g.tar, DOWN, buff=0.35)
        g.parcel = parcel(f"{TARBALL_BYTES} bytes", OWNED, size, 0.9, 0.62).move_to([2.2, 0.55, 0])
        g.wrap_box = RoundedRectangle(width=3.8, height=2.6, corner_radius=0.05, stroke_color=TOOL,
                                      stroke_width=4).move_to(pfr)
        g.add(g.package, g.trainer)
        g.ride(*g.files, g.setup, g.tar, g.gzip, g.parcel, g.wrap_box)
        return g

    def drop(self, run_time: float = 1.0):
        self.add(*self.files)
        return Succession(LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in self.files], lag_ratio=0.3),
                          AnimationGroup(*[f.animate.move_to(p) for f, p in zip(self.files, self.slots_)]),
                          run_time=run_time)

    def clip(self, run_time: float = 0.7):
        self.add(self.setup)
        return FadeIn(self.setup, shift=UP * 0.2, run_time=run_time)

    def wrap(self, run_time: float = 0.9):
        self.add(self.tar, self.wrap_box)
        return Succession(FadeIn(self.tar, shift=LEFT * 0.2), Create(self.wrap_box), run_time=run_time)

    def shrink(self, run_time: float = 1.1):
        """gzip: the wrapped package collapses into the GREEN parcel ('4016 bytes')."""
        self.add(self.gzip)
        whole = VGroup(self.package, self.trainer, *self.files, self.wrap_box)
        return Succession(FadeIn(self.gzip, shift=LEFT * 0.2),
                          AnimationGroup(ReplacementTransform(whole, self.parcel[:3]), FadeIn(self.parcel[3])),
                          run_time=run_time)

    def upload(self, point, fail: bool = True, run_time: float = 1.0):
        """Returns (route, Animation): the PINK gsutil cp route from the parcel to `point`; with
        fail=True it stops short at a RED '404' chip (.upload_fail)."""
        p = np.array(point)
        s = self.parcel.box.get_right() + RIGHT * 0.1
        r = Arrow(s, p, buff=0, color=ROUTE, stroke_width=5, tip_length=0.22)
        lab = mono("gsutil cp", 20, ROUTE).next_to(r, UP, buff=0.08)
        anims = [GrowArrow(r), FadeIn(lab)]
        grp = VGroup(r, lab)
        self.upload_fail = None
        if fail:
            e = err_chip("404").move_to(p + RIGHT * 0.45)
            anims.append(FadeIn(e, scale=1.4))
            grp.add(e)
            self.upload_fail = e
        return grp, Succession(*anims, run_time=run_time)

    # ---------------------------------------------------------------- step 3
    @classmethod
    def spec(cls, size: float = 20) -> "TarballTrip":
        g = cls()
        machine, replicas, image, module = SPEC_CHIPS
        image_short = "executor-image-uri=…" + image.rsplit("/", 1)[1]
        words = [("display-name", JOB_NAME), ("machine", machine), ("replicas", replicas), ("image", image_short),
                 ("package", "--python-package-uris=…/" + TARBALL), ("module", module), ("args", "--args=…,--wandb_key=…")]
        chips_ = []
        for k, w in words:
            c = chip(w, KEY if k == "args" else (ROUTE if k == "package" else CLOUD), size=size, font=MONO)
            chips_.append(c)
        col = VGroup(*chips_).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fr = RoundedRectangle(width=col.width + 0.6, height=col.height + 0.85, corner_radius=0.14,
                              stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        hd = label("job spec · gcloud ai custom-jobs create", 20, S.GREY)
        hd.move_to(fr.get_corner(UL) + np.array([0.25 + hd.width / 2, -0.27, 0]))
        col.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3 + DOWN * 0.2)
        g.card = VGroup(fr, hd)
        g.chips = chips_
        g.key_chip = chips_[-1]
        g.add(g.card)
        g.ride(*chips_)
        return g

    def assemble(self, i: int, run_time: float = 0.5):
        self.add(self.chips[i])
        return FadeIn(self.chips[i], shift=RIGHT * 0.2, run_time=run_time)

    def redden(self, run_time: float = 0.7):
        c = self.key_chip
        new = chip(c.text.original_text, ERR, size=20, font=MONO, fill_opacity=0.18).move_to(c)
        return Transform(c, new, run_time=run_time)

    def fly(self, point, run_time: float = 1.2):
        whole = VGroup(self.card, *[c for c in self.chips if c in self.submobjects])
        return whole.animate(run_time=run_time).scale(0.25).move_to(point).set_opacity(0)

    # ---------------------------------------------------------------- step 4
    @classmethod
    def vm(cls, mini: bool = False, size: float = 20, center=(0.0, 0.7)) -> "TarballTrip":
        g = cls()
        g.mini = mini
        w, h = (3.4, 2.6) if mini else (7.2, 3.6)
        fr = RoundedRectangle(width=w, height=h, corner_radius=0.16, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.08).move_to([center[0], center[1], 0])
        ft = label("job VM" if mini else "job VM · Vertex AI", size, CLOUD)
        ft.move_to(fr.get_corner(UL) + np.array([0.2 + ft.width / 2, -0.25, 0]))
        g.meter = meter(0.5).move_to(fr.get_corner(UR) + np.array([-0.4, -0.32, 0]))
        g.box = VGroup(fr, ft)
        bw = w - 0.5
        g.image = band(CPU_IMAGE, IMAGE, bw, 0.4, size, mono_font=True)
        g.image.move_to(fr.get_bottom() + UP * (0.35 if mini else 0.4))
        g.layer = band("TensorFlow · scikit-learn · expected" if not mini else "TensorFlow · expected", SYSTEM,
                       bw, 0.4, size)
        g.layer.next_to(g.image, UP, buff=0.06)
        g.parcel = parcel(None, OWNED, size, 0.6, 0.42).move_to(fr.get_top() + UP * 0.6)
        g.trainer = drawer("trainer/", OWNED, size).next_to(g.layer, UP, buff=0.15).align_to(g.layer, LEFT)
        g.wandb_chip = chip("wandb 0.15.11", OWNED, size=size, font=MONO).next_to(g.trainer, RIGHT, buff=0.2)
        if mini:
            g.argv = VGroup(mono("python -m trainer.task", size, INK)).next_to(g.trainer, UP, buff=0.15).align_to(
                g.trainer, LEFT)
        else:
            toks = [mono("python -m trainer.task", size, INK)] + [chip(a if not a.startswith("--wandb_key")
                                                                       else "--wandb_key=…", KEY, size=size, font=MONO)
                                                                  for a in ARGV]
            row1 = VGroup(*toks[:3]).arrange(RIGHT, buff=0.12)
            row2 = VGroup(*toks[3:]).arrange(RIGHT, buff=0.12)
            g.argv = VGroup(row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            g.argv.next_to(g.trainer, UP, buff=0.15).align_to(g.trainer, LEFT)
            g.argv.tokens = toks
        out_y = fr.get_center()[1]
        g.logs = label("logs", size, ROUTE).move_to([fr.get_right()[0] + 0.75, out_y + 0.45, 0])
        g.wb = mono(WB_HOST, size, CLOUD).move_to([fr.get_right()[0] + 0.85, out_y - 0.45, 0])
        g.streams_ = VGroup(Arrow([fr.get_right()[0] - 0.1, out_y + 0.45, 0], g.logs.get_left(), buff=0.08,
                                  color=ROUTE, stroke_width=4, tip_length=0.18),
                            Arrow([fr.get_right()[0] - 0.1, out_y - 0.45, 0], g.wb.get_left(), buff=0.08,
                                  color=ROUTE, stroke_width=4, tip_length=0.18))
        g.ghost = VGroup(outline_box(1.6, 0.6, FUTURE, solid=False), label("trained weights", size, FUTURE))
        g.ghost[1].move_to(g.ghost[0])
        g.ghost.move_to(fr.get_center() + RIGHT * (w / 2 - 1.2) + UP * 0.1)
        g.ride(g.box, g.meter, g.image, g.layer, g.parcel, g.trainer, g.wandb_chip, g.argv, g.logs, g.wb,
               g.streams_, g.ghost)
        return g

    def appear(self, run_time: float = 1.0):
        """A machine materialises (BLUE) and the GOLD meter starts."""
        self.add(self.box, self.meter)
        return Succession(FadeIn(self.box, scale=0.9), FadeIn(self.meter), meter_run(self.meter), run_time=run_time)

    def image_in(self, run_time: float = 0.9):
        """Google's prebuilt image drops in (TEAL band) with its ORANGE 'expected' layer."""
        self.add(self.image, self.layer)
        return LaggedStart(FadeIn(self.image, shift=DOWN * 0.4), FadeIn(self.layer, shift=DOWN * 0.4),
                           lag_ratio=0.4, run_time=run_time)

    def unwrap(self, run_time: float = 1.0):
        """The GREEN tarball lands and unwraps into trainer/."""
        self.add(self.parcel)
        return Succession(FadeIn(self.parcel, shift=DOWN * 0.3),
                          ReplacementTransform(self.parcel, self.trainer), run_time=run_time)

    def pip(self, run_time: float = 0.7):
        self.add(self.wandb_chip)
        return FadeIn(self.wandb_chip, shift=LEFT * 0.2, run_time=run_time)

    def run(self, run_time: float = 1.2):
        """python -m trainer.task with the flags (full: --args split at its commas into argv tokens)."""
        self.add(self.argv)
        if self.mini:
            return FadeIn(self.argv, shift=UP * 0.2, run_time=run_time)
        return LaggedStart(*[FadeIn(t, shift=UP * 0.2) for t in self.argv.tokens], lag_ratio=0.15, run_time=run_time)

    def streams(self, run_time: float = 0.9):
        self.add(self.streams_, self.logs, self.wb)
        return AnimationGroup(*[GrowArrow(a) for a in self.streams_], FadeIn(self.logs), FadeIn(self.wb),
                              run_time=run_time)

    def dissolve(self, run_time: float = 1.4):
        """The script exits: the machine and everything on it fade, the meter stops, the trained
        weights are left as a GREY-dashed ghost (nothing calls model.save)."""
        inside = [m for m in (self.box, self.image, self.layer, self.trainer, self.wandb_chip, self.argv,
                              self.streams_, self.logs, self.wb) if m in self.submobjects]
        self.add(self.ghost)
        anim = Succession(FadeIn(self.ghost), AnimationGroup(meter_stop(self.meter),
                                                             *[FadeOut(m) for m in inside], FadeOut(self.meter)),
                          run_time=run_time)
        for m in inside + [self.meter]:
            self.remove(m)
        return anim

    # ---------------------------------------------------------------- the stand-in
    @staticmethod
    def standin(size: float = 20) -> VGroup:
        """S11: a dashed TEAL container labelled 'plain python:3.10 · not Google's image' (not added)."""
        h = house(None, 4.2, 1.5, IMAGE, dashed=True)
        t = VGroup(mono("python:3.10", size, IMAGE), label("plain · not Google's image", size, S.GREY))
        t.arrange(DOWN, buff=0.06).move_to(h.body)
        g = VGroup(h, t)
        g.house, g.text = h, t
        return g


# ================================================================== V5 · ThreeBadges (who submits, who runs)
class ThreeBadges(Rig):
    """V5 (S11; reprise S15): three badges on three lanyards, built in place (x -6.5 … 6.5,
    y -1.3 … 2.75). Nothing is added at first; hang(i) hangs badge i (0, 1, 2).
      0  GREEN key file: 'model-trainer' · 'key file · submits'; .roles (three GREEN role chips under
         it, README:62, not added)
      1  ORANGE, Google-managed: 'Vertex AI Custom Code' / 'Service Agent' /
         'service-…@gcp-sa-aiplatform-cc' (digest §3.5), 'runs the job, by default'; its lanyard can
         hang empty with a GREY '?' first: question()
      2  GREEN W&B key (dots, never the key): 'W&B key' · 'for wandb.ai · carried in --args'
      hang(i) -> Animation     lanyard + badge i appear
      lanyard(i) -> Animation  only the empty lanyard i
      question() -> VGroup     the GREY '?' on the middle lanyard (not added)
      turn_red() -> Animation  badge 2 turns RED (printed inside --args, S10)
      viewer() -> VGroup       a GREY viewer icon looking over badge 2's shoulder (not added)
    .badges .strings .roles"""

    XS = (-4.55, 0.0, 4.55)

    def __init__(self, size: float = 20, red: bool = False):
        super().__init__()
        self.size = size
        b0 = badge([SA_NAME, "key file · submits"], KEY, size, "key")
        b1 = self._agent(size)
        b2 = badge(["W&B key", "for wandb.ai", "carried in --args"], ERR if red else KEY, size, "wandb", mono_first=False)
        self.badges = [b0, b1, b2]
        self.strings = []
        for b, x in zip(self.badges, self.XS):
            b.move_to([x, 1.45, 0], aligned_edge=UP)
            s = VGroup(Line([x - 0.5, 2.75, 0], [x, b.get_top()[1] + 0.02, 0], color=S.GREY, stroke_width=3),
                       Line([x + 0.5, 2.75, 0], [x, b.get_top()[1] + 0.02, 0], color=S.GREY, stroke_width=3))
            self.strings.append(s)
        self.roles = VGroup(*[chip(r, KEY, size=size) for r in SA_ROLES]).arrange(DOWN, buff=0.1)
        self.roles.next_to(b0, DOWN, buff=0.25)
        self.ride(*self.badges, *self.strings, self.roles)
        self.red = red

    @staticmethod
    def _agent(size):
        col = SYSTEM
        gear = VGroup(Circle(radius=0.13, stroke_color=col, stroke_width=3),
                      *[Line(ORIGIN, 0.08 * np.array([np.cos(a), np.sin(a), 0]), color=col, stroke_width=3)
                        .shift(0.15 * np.array([np.cos(a), np.sin(a), 0])) for a in np.linspace(0, 2 * PI, 6,
                                                                                                endpoint=False)])
        pf = RoundedRectangle(width=0.55, height=0.55, corner_radius=0.08, stroke_color=col,
                              stroke_width=2.5).set_fill(col, 0.15)
        portrait = VGroup(pf, gear.move_to(pf))
        txt = VGroup(label(SERVICE_AGENT[0].rsplit(" ", 2)[0], size, INK), label("Service Agent", size, INK),
                     mono("service-…@", size, S.GREY), mono("gcp-sa-aiplatform-cc", size, S.GREY),
                     label("runs the job, by default", size, col)).arrange(DOWN, buff=0.06)
        body = VGroup(portrait, txt).arrange(DOWN, buff=0.15)
        fr = RoundedRectangle(width=body.width + 0.5, height=body.height + 0.4, corner_radius=0.12,
                              stroke_color=col, stroke_width=3).set_fill(S.GREY_DARKER, 1)
        body.move_to(fr)
        clip = RoundedRectangle(width=0.5, height=0.16, corner_radius=0.05, stroke_color=col,
                                stroke_width=2.5).set_fill(S.BG, 1).move_to(fr.get_top())
        g = VGroup(fr, body, clip)
        g.frame, g.clip, g.portrait, g.text = fr, clip, portrait, txt
        return g

    def lanyard(self, i: int, run_time: float = 0.5):
        self.add(self.strings[i])
        return Create(self.strings[i], run_time=run_time)

    def hang(self, i: int, run_time: float = 0.9):
        anims = []
        if self.strings[i] not in self.submobjects:
            self.add(self.strings[i])
            anims.append(Create(self.strings[i]))
        self.add(self.badges[i])
        anims.append(FadeIn(self.badges[i], shift=DOWN * 0.3))
        return Succession(*anims, run_time=run_time)

    def question(self) -> VGroup:
        return label("?", 48, S.GREY).move_to([self.XS[1], 0.9, 0])

    def turn_red(self, run_time: float = 0.8):
        b = self.badges[2]
        new = badge(["W&B key", "for wandb.ai", "carried in --args"], ERR, self.size, "wandb", mono_first=False)
        new.move_to(b)
        self.red = True
        return Transform(b, new, run_time=run_time)

    def viewer(self) -> VGroup:
        b = self.badges[2]
        p = person_icon(S.GREY, 0.8)
        return p.next_to(b, LEFT, buff=0.1).align_to(b, UP).shift(UP * 0.35)


# ================================================================== V6 · GpuSwitchboard (three switches, one GPU)
SWITCHES = ("accelerator", "image", "quota")
SWITCH_VALUES = {"accelerator": ("no accelerator", "T4 × 1"), "image": ("tf-cpu.*", "tf-gpu.* · CUDA"),
                 "quota": ("no T4 quota here", f"T4 quota · {REGION}")}


class GpuSwitchboard(Rig):
    """V6 (S13): a job tile (BLUE, 9 × 3.4, centred at (0, 0.75): the band above a 3-row strip) with
    three switches in a row — accelerator (worker pool: accelerator-type=NVIDIA_TESLA_T4,
    accelerator-count=1), image (tf-gpu.* with CUDA vs tf-cpu.*), quota (T4s for custom training in
    this region) — a T4 chip slot at the right and a GOLD meter. The chip lights only when all three
    are GREEN (on). Values are words, not numbers.
      toggle(k, on=True) -> Animation     switch k ('accelerator' | 'image' | 'quota') turns GREEN (on,
                                         its value becomes the 'on' words) or GREY (off)
      chip_on() -> Animation             the T4 in the slot lights (all three on)
      chip_dark() -> Animation           a T4 sits in the slot, dark, while the meter still runs
                                         (CPU image + accelerator: ponder 10)
      twin() -> VGroup                   a second tile with the same name + RED 'two jobs, two bills'
                                         (not added; both GPU and CPU blocks left live)
    .tile .switches {k: VGroup(.toggle .knob .title_ .value)} .slot .chip .meter .title"""

    def __init__(self, size: float = 20, on=()):
        super().__init__()
        self.size = size
        fr = RoundedRectangle(width=9.0, height=3.4, corner_radius=0.16, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.07).move_to([0, 0.75, 0])
        self.title = mono(JOB_NAME, size, INK).move_to(fr.get_corner(UL) + np.array([0.25, -0.28, 0]), aligned_edge=LEFT)
        self.meter = meter(0.5).move_to(fr.get_corner(UR) + np.array([-0.45, -0.35, 0]))
        self.tile = VGroup(fr, self.title)
        self.switches = {}
        self.state = {k: k in on for k in SWITCHES}
        for k, x in zip(SWITCHES, (-3.1, -0.9, 1.3)):
            self.switches[k] = self._switch(k, self.state[k]).move_to([x, 0.55, 0])
        self.slot = outline_box(1.1, 1.1, S.GREY, solid=False).move_to([3.4, 0.55, 0])
        sl = label("GPU slot", size, S.GREY).next_to(self.slot, DOWN, buff=0.12)
        self.chip = t4_chip(False, size, 0.7).move_to(self.slot)
        self.add(self.tile, self.meter, *self.switches.values(), self.slot, sl)
        self.ride(self.chip)

    def _switch(self, k, on):
        col = PASS if on else S.GREY
        tg = RoundedRectangle(width=1.0, height=0.46, corner_radius=0.23, stroke_color=col,
                              stroke_width=3).set_fill(col, 0.3 if on else 0.05)
        knob = Circle(radius=0.17, stroke_width=0).set_fill(col, 1).move_to(tg.get_center() + RIGHT * (0.27 if on else -0.27))
        nm = label(k, self.size + 2, INK).next_to(tg, UP, buff=0.18)
        v = label(SWITCH_VALUES[k][1 if on else 0], self.size, col).next_to(tg, DOWN, buff=0.18)
        g = VGroup(nm, tg, knob, v)
        g.toggle, g.knob, g.title_, g.value = tg, knob, nm, v
        return g

    def toggle(self, k: str, on: bool = True, run_time: float = 0.6):
        self.state[k] = on
        old = self.switches[k]
        new = self._switch(k, on)
        new.shift(old.toggle.get_center() - new.toggle.get_center())
        anims = [Transform(old.toggle, new.toggle), Transform(old.knob, new.knob), FadeOut(old.value),
                 FadeIn(new.value)]
        old.remove(old.value)
        old.add(new.value)
        old.value = new.value
        return AnimationGroup(*anims, run_time=run_time)

    def chip_on(self, run_time: float = 0.8):
        new = t4_chip(True, self.size, 0.7).move_to(self.slot)
        anims = [Transform(self.chip, new)] if self.chip in self.submobjects else [FadeIn(new, scale=1.3)]
        if self.chip not in self.submobjects:
            self.chip.become(new)
            self.add(self.chip)
            anims = [FadeIn(self.chip, scale=1.3)]
        return AnimationGroup(*anims, meter_run(self.meter), run_time=run_time)

    def chip_dark(self, run_time: float = 0.8):
        self.chip.become(t4_chip(False, self.size, 0.7).move_to(self.slot))
        self.add(self.chip)
        return AnimationGroup(FadeIn(self.chip, shift=DOWN * 0.2), meter_run(self.meter), run_time=run_time)

    def twin(self) -> VGroup:
        fr = RoundedRectangle(width=4.2, height=1.0, corner_radius=0.14, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.07)
        t = mono(JOB_NAME, self.size, INK).move_to(fr)
        a = VGroup(fr, t)
        b = a.copy()
        pair = VGroup(a, b).arrange(RIGHT, buff=0.3)
        e = err_chip("two jobs, two bills", mono_font=False).next_to(pair, DOWN, buff=0.15)
        g = VGroup(pair, e)
        g.tiles, g.chip = pair, e
        return g.move_to([0, -1.75 + g.height / 2 + 0.45, 0])


# ================================================================== V7 · MirroredReplicas (two GPUs, one model)
def network_glyph(fill=S.TEAL, layers=(3, 4, 2), net_w: float = 1.3, net_h: float = 1.0) -> VGroup:
    """A small network: nodes in layers joined by thin GREY edges; node fills = `fill` (the replica's
    weights). .nodes .edges"""
    nodes, cols_ = VGroup(), []
    for j, n in enumerate(layers):
        x = -net_w / 2 + net_w * j / (len(layers) - 1)
        col = []
        for i in range(n):
            y = net_h / 2 - net_h * (i + 0.5) / n
            d = Circle(radius=0.09, stroke_color=INK, stroke_width=2).set_fill(fill, 0.85).move_to([x, y, 0])
            nodes.add(d)
            col.append(d)
        cols_.append(col)
    edges = VGroup(*[Line(a.get_center(), b.get_center(), color=S.GREY_DARK, stroke_width=1.5)
                     for c1, c2 in zip(cols_, cols_[1:]) for a in c1 for b in c2])
    g = VGroup(edges, nodes)
    g.nodes, g.edges = nodes, edges
    return g


class MirroredReplicas(Rig):
    """V7 (S14): data-parallel training on one n1-standard-32 box with two T4s, built in place
    (x -6.5 … 4.0, y -1.3 … 2.0: the band above a 3-row strip). Picture before code.
      MirroredReplicas.ladder() -> VGroup   slide 27's three rows (One Device · Mirrored 'you are
                                            here' YELLOW · Multi Worker Mirrored GREY dashed); .rows .here
      split_batch() -> Animation  a global batch of 64 tiles (8 × 8, left) splits 32 + 32 onto the GPUs
      grads() -> Animation     each GPU's gradient arrow rises to the PINK all-reduce link
      allreduce() -> Animation the link lights, 'average' appears, the arrows return
      step() -> Animation      both replicas take the same step (same colour change): they stay identical
      MirroredReplicas.scope() -> Rig       'with strategy.scope():' as a frame around model ·
                                            optimizer · compile; .twins() -> Animation (the variables
                                            split into one synced copy per GPU); .outside (a model
                                            built outside, single, GREY chip 'not mirrored'; not added)
    .box .gpus [2] (.chip .net) .batch (64 tiles) .link .avg"""

    def __init__(self, size: float = 20):
        super().__init__()
        self.size = size
        fr = RoundedRectangle(width=7.6, height=3.3, corner_radius=0.16, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.05).move_to([0.25, 0.35, 0])
        ft = mono(MACHINE_MULTI, size, CLOUD).move_to(fr.get_corner(DL) + np.array([0.2, 0.25, 0]), aligned_edge=LEFT)
        self.box = VGroup(fr, ft)
        self.gpus = []
        for x in (-1.45, 1.95):
            cfr = RoundedRectangle(width=2.7, height=1.75, corner_radius=0.12, stroke_color=CLOUD,
                                   stroke_width=2.5).set_fill(S.GREY_DARKER, 1).move_to([x, 0.05, 0])
            ch = t4_chip(True, size, 0.5).move_to(cfr.get_corner(UL) + np.array([0.45, -0.45, 0]))
            net = network_glyph(S.TEAL).move_to(cfr.get_center() + RIGHT * 0.45 + DOWN * 0.05)
            rl = label("replica", size, S.GREY).next_to(ch, DOWN, buff=0.15)
            g = VGroup(cfr, ch, net, rl)
            g.frame, g.chip, g.net = cfr, ch, net
            self.gpus.append(g)
        tiles = VGroup(*[Rectangle(width=0.12, height=0.12, stroke_width=0).set_fill(INK, 0.8) for _ in range(64)])
        tiles.arrange_in_grid(rows=8, cols=8, buff=0.035).move_to([-5.3, 0.45, 0])
        self.batch = tiles
        self.batch_label = label("global batch · 64", size, INK).next_to(tiles, DOWN, buff=0.15)
        y_link = 1.55
        l0, l1 = self.gpus[0].frame.get_center()[0], self.gpus[1].frame.get_center()[0]
        self.link = Line([l0, y_link, 0], [l1, y_link, 0], color=ROUTE, stroke_width=6)
        self.link_label = label("all-reduce", size, ROUTE).next_to(self.link, UP, buff=0.08)
        self.up = [Arrow([x, self.gpus[0].frame.get_top()[1], 0], [x, y_link, 0], buff=0.04, color=ROUTE,
                         stroke_width=4, tip_length=0.16) for x in (l0, l1)]
        self.grad_labels = [label("gradients", size, INK).next_to(a, LEFT, buff=0.08) for a in self.up]
        self.avg = label("average", size, INK).next_to(self.link_label, RIGHT, buff=0.3)
        self.add(self.box, *self.gpus, self.batch, self.batch_label)
        self.ride(self.link, self.link_label, *self.up, *self.grad_labels, self.avg)

    def split_batch(self, run_time: float = 1.4):
        halves = (VGroup(*self.batch[:32]), VGroup(*self.batch[32:]))
        anims = []
        for h, g in zip(halves, self.gpus):
            tgt = h.copy().arrange_in_grid(rows=4, cols=8, buff=0.035)
            tgt.move_to(g.frame.get_corner(DL) + np.array([0.75, 0.32, 0]))
            anims.append(Transform(h, tgt))
        n32 = [label("32", self.size, INK).next_to(g.frame.get_corner(DL) + np.array([1.5, 0.32, 0]), RIGHT, buff=0.1)
               for g in self.gpus]
        self.n32 = n32
        self.add(*n32)
        return Succession(AnimationGroup(*anims, FadeOut(self.batch_label)), AnimationGroup(*[FadeIn(t) for t in n32]),
                          run_time=run_time)

    def grads(self, run_time: float = 1.0):
        self.add(*self.up, *self.grad_labels)
        return AnimationGroup(*[GrowArrow(a) for a in self.up], *[FadeIn(t) for t in self.grad_labels],
                              run_time=run_time)

    def allreduce(self, run_time: float = 1.2):
        self.add(self.link, self.link_label, self.avg)
        return Succession(AnimationGroup(Create(self.link), FadeIn(self.link_label)), FadeIn(self.avg, scale=1.2),
                          run_time=run_time)

    def step(self, color=S.YELLOW, run_time: float = 1.0):
        return AnimationGroup(*[g.net.nodes.animate.set_fill(color, 0.85) for g in self.gpus], run_time=run_time)

    @staticmethod
    def ladder(size: float = 22) -> VGroup:
        rows = VGroup()
        for i, (shape, name) in enumerate(LADDER):
            col = TURN if i == 1 else (FUTURE if i == 2 else INK)
            b = outline_box(9.0, 0.8, col, solid=i != 2, fill_opacity=0.06 if i != 1 else 0.12)
            t1 = label(shape, size, col).move_to(b).align_to(b, LEFT).shift(RIGHT * 0.3)
            t2 = label(name, size, col).move_to(b).align_to(b, RIGHT).shift(LEFT * 0.3)
            rows.add(VGroup(b, t1, t2))
        rows.arrange(DOWN, buff=0.25).move_to([-0.6, 0.75, 0])
        here = chip("you are here", TURN, size=20).next_to(rows[1], RIGHT, buff=0.2)
        g = VGroup(rows, here)
        g.rows, g.here = rows, here
        return g

    @staticmethod
    def scope(size: float = 22) -> Rig:
        g = Rig()
        chips_ = VGroup(*[chip(s, OWNED, size=size, font=MONO) for s in ("model", "optimizer", "compile")])
        chips_.arrange(RIGHT, buff=0.3)
        head = mono("with strategy.scope():", size, TOOL)
        body = VGroup(head, chips_).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        chips_.shift(RIGHT * 0.4)
        fr = RoundedRectangle(width=body.width + 0.8, height=body.height + 0.6, corner_radius=0.14,
                              stroke_color=TOOL, stroke_width=3).set_fill(TOOL, 0.05)
        body.move_to(fr)
        g.add(fr, body)
        g.frame, g.head, g.chips = fr, head, chips_
        g.move_to([-1.2, 0.9, 0])
        var = chip("variables", OWNED, size=size).next_to(fr, DOWN, buff=0.35).align_to(fr, LEFT).shift(RIGHT * 0.4)
        twins = VGroup(chip("variables · GPU 0", OWNED, size=20), chip("variables · GPU 1", OWNED, size=20))
        twins.arrange(RIGHT, buff=0.25).move_to(var).align_to(var, LEFT)
        link = Line(twins[0].get_right(), twins[1].get_left(), color=ROUTE, stroke_width=4)
        out_ = VGroup(chip("model", S.GREY, size=size, font=MONO), grey_chip("not mirrored"))
        out_.arrange(DOWN, buff=0.15).next_to(fr, RIGHT, buff=0.8)
        g.var, g.twin_chips, g.twin_link, g.outside = var, twins, link, out_
        g.add(var)
        g.ride(twins, link, out_)

        def twins_anim(run_time: float = 1.0):
            g.add(twins, link)
            return AnimationGroup(ReplacementTransform(var, twins), Create(link), run_time=run_time)
        g.twins = twins_anim
        return g
