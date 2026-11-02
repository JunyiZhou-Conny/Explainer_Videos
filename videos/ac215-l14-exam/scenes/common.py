"""Shared code for AC215 L14 · Serverless Deployment, EXAM EDITION (videos/ac215-l14-exam): paths,
narration, the semantic colours of BRIEF.md, source loaders for the code panels (assets/source/
serverless-deployment @ 46cc62f and model-deployment @ cf0b7c7), the generic panel / card / tag /
Piece helpers ported unchanged from L08's tested common.py (guard() included), and this video's
exam scaffolding (exam map, rule cards, multiple-choice ponders) and set pieces V1-V6 of BRIEF.md.
No captures, terminals or README trackers: this edition has none (script.md "No live runs").
Tested on screen by build/common_test.py (CommonTest, StripTest, MeterTest, HandTest, DoorTest,
ClientTest: explainer.check OK, preview sheets read).

Notes for scene authors
=======================

    from common import ...     # every scene: SAY = NARRATION["S03"]; assert len(SAY) == n;
                               # one `with self.voiceover(SAY[i]) as vo:` per SAY line, in order
    from common import ThinClients as ClientsPiece    # S06's scene class has the same name

All text here is 20-34 pt. Never .scale() a group that holds text below 1.0 (Piece.rescale(k)
shrinks shapes and keeps text). Methods return ANIMATIONS (play them right away: new members are
added to the piece when the method is called) unless they say "plays". Set pieces marked "in
place" already sit where the script wants them; do not move those (their methods use absolute
coordinates); the others are built centred at ORIGIN and may be moved.

Frame budget. Exam map: top strip x -6.6..2.3, centre y 3.3 (MAP_Y), its active label under it
(y ~2.75). lecture_ref top right, left of it >= REF_LEFT 2.45 (lref() guards it: the widest tag,
"Lecture 14 · slides 8, 11, 14", is 4.04 wide, so the map ends at 2.3, not at script.md's 3.2).
Keep content below y 2.55 when the map shows its label. Rule card: bottom third (bottom -3.45).
Ponder card: bottom -3.55, top <= 2.58 (guarded). Safe frame x +-6.6, y +-3.6 (SAFE_X, SAFE_Y).

Data and sources
    NARRATION["S01"] … ["S08"] (SAY lines of script.md)   TITLES[cls]   SPEC (video.yaml)
    src_path / source_text / excerpt(name, a, b) / source_line(name, n) / readme(a, b, repo=…)
        names: "README.md" (= serverless-deployment/README.md), "tutorial/app/Dockerfile",
        "tutorial/app/translation_demo/__main__.py", "tutorial/function/main.py", "cli.py"
        (= model-deployment/cli.py), "model-deployment/README.md". README lines lose their "**".
    shown_path(name): header path (serverless-deployment/ dropped, model-deployment/ kept)
    Names (no real person: guard_names() raises on the instructor's first name; model-deployment/
        README.md line 136 is never quoted): IMAGE, RUNTIME_SA, RUNTIME_SA_EMAIL (exactly as the
        README writes it, YOUR_PROJECT_ID), JOB_SA, JOB_NAME, SERVICE_NAME, IN_BUCKET, OUT_BUCKET,
        ENTRY "hello_http", BASE_IMAGE, PORT 8080, JOB_STEPS, CHEESES, PREP_STEPS, GUIDE

Colours (BRIEF.md "Colours", binding)
    CLIENT (= LAPTOP = YOU) GREY · CLOUD (= IDENTITY: Cloud Run, VM, endpoint, buckets, Scheduler,
    badges) BLUE · CTR TEAL · SYSTEM ORANGE (base image, S04) · OWN GREEN · TOOL PURPLE · ERR RED ·
    TURN (= PULSE) YELLOW · COST (= KEY) GOLD · ROUTE (= LOOKUP: requests, URLs, triggers, gs://,
    b64) PINK · INK white. VMs: solid racks; serverless instances: DASHED outlines.

Lecture tag
    lref(14, "14") / lref(15, "13") / lref(14, "8, 11, 14")   lr = lref_swap(self, lr, 15, "11")
    (plays; old may be None)

Code panels and cards (20-22 pt)
    src_panel(name, a, b=None, focus=, wrap=None, wrap_at=65, join=, cut_comments=, subtitle=,
        max_rows=12) CODE(): header "path · lines a–b" (+ " · long lines wrapped"); a list
        [1, 2, 11, 12] folds (GREY "…" rows); wrap=None wraps every line > wrap_at at spaces
        (GREY ↪); raises when > 12 rows or > 12.9 wide. .bar(n, colour) .span(n, "sub")
        .rows_of(n). README tables are long: wrap_at=88 fills the frame width.
    excerpt_chip(sub, "README.md · line 833 (excerpt)", line=source_line(...)) (checks sub)
    readme_chip(where, phrase) one-line chip   readme_card(where, lines)   log_panel(lines, header)
    card_rows(items, header=)  table_card(headers, rows)  question_card(text)  answer_card(rows)
    card_glyph(title, sub)  concept_box(text)  cmd_chip(cmd, note_)  json_card(lines)
    fit_rows(text, width, size) rows that fit (`code` mono)   swap_text(parent, old, new) -> anims
    ponder_at(scene, "q", seconds) the one-line ponder (S06; plays)   Counter(text, value)
Tags / marks: grey_tag(s) illustration_tag(note_) concept_tag(s) stamp(text, colour)
    fix_chip(text) url_chip(text) (PINK mono) x_mark() tick_mark() under(m) strike(m) ring(m)
Opacity helpers: dim(m, 0.2) / undim(m) -> anims (a ponder is up: everything else <= 20 %);
    keep_size(m) (Piece.rescale leaves it)

Small glyphs (no text unless said): instance_box(w, h, inner=True) (dashed BLUE + TEAL inner)
    vm_rack(h) ear_glyph() ear_chip("listening on :8080") gear(r) puff() bucket_glyph()
    phone_glyph() webpage_glyph() token_glyph() no_key() (dashed GOLD key, crossed)
    entry_tag(name="hello_http") (GREEN luggage tag, .name) badge(name) (BLUE, .name .frame)
    role_chip(text, colour) log_window(title) (.light(colour) -> anims) image_glyph() (224×224×3)
    ProbBars(CHEESES) (.rise(values, hi=2) -> anims) Clock(counter=True) (.run_to(min, t) -> anims;
    .freeze()) scheduler_clock() execute_button() (.press() -> anim) Slider() (.to(v) -> anim)
    VersionDial() (.set("v2", bad=True) -> anims) door() plug(text, letter=) socket(text)
    toggle(text, on) (.flip(on) -> anims; tag it illustration_tag()) service_box(title)
    container_glyph() answer_bubble(colour) hbracket(mobs, text, UP|DOWN)
    file_row(name) ghost_file(name) key_glyph() key_outline() model_box(name) container_box(title)

Exam scaffolding
    ExamMap(filled=(1, 2), half=(5,))  (= exam_map) top strip, slots 1..5 (EXAM_SLOTS), icon +
        number. .write_in() / .slot_in(i) -> anim; .activate(i) -> anims (others 35 %, slot i
        YELLOW + its label under it); .deactivate() .pulse(i) .fill(i, frac=1.0) -> anims;
        .slot_frame(i); .slots[i-1] (.frame .num .icon). Rebuild it per scene with what is done.
    RuleCard(top, bottom)  (= rule_card) GREEN "exam rule" card, bottom third. .write_in() /
        .frame_in() / .line_in(0|1) -> anims; .shrink_into(scene, map, i, frac=1.0) (plays: into
        slot i, then the slot fills). .rows[0] / .rows[1]
    mcq_ponder(scene, question, [A, B, C, D], seconds=10, dim=[...], hide=[...]) (plays: dims,
        card in, timer) -> MCQCard: .right(k, note) / .wrong(k, reason) -> anims (k 0-based; a
        reason must fit its reserved row: guarded). MCQCard(None, options, width=7.6,
        reason_rows=2, header="P3") is the compact docked card (S07): build it and FadeIn it.
    recap_icon(k) (S08 rules 1..7: strips, meters, puff, grid, doors, gear, plug), icon_*()

Set pieces (Piece: named parts; piece.parts_in("a") / parts_out / reveal(scene, …) / hide;
    late_in(piece, "a") = parts_in that waits for its turn inside a Succession; never FadeOut a
    part, FadeOut the whole piece; dim with dim(piece))
    V1 ImageBlock(name=IMAGE, commands=("serve", "batch"))  ~7.7 x 1.3: TEAL image + GREEN
       command tags; .cmds["serve"] .anchor(cmd)
       ServiceStrip(10.0)  10.8 x 3.3 (y -1.75..1.6): .start(t) .grow(t) .request(t, lane)
       .split(t) .stop(t) -> anims (t: 0..1 of the time span); parts url ear max_chip zero_chip
       JobStrip(10.0, steps=JOB_STEPS, code=0)  ~10 x 1.6: .run(i) .run_all() .finish() -> anims;
       .span(). code=1: RED "exit 1" (the short failed run: steps=("read", "translate"))
       EndlessStrip(10.0)  ~10 x 2.4: .grow_to(t, run_time) .hit_wall() .cut_into(job) -> anims;
       .clock (freeze() before it leaves). LifecycleStrip(kind) factory.
    V2 TwoMeters()  in place, x -6.5..6.4, y -2.4..2.0: .sweep() .blink_all() .stretch()
       .unstretch() .double() .cold_start() .min_instances(1) .lift_always_on() -> anims;
       .always_on_slot() (the endpoint card's centre, card <= 0.5 tall)
    V3 HandoverGrid()  in place, ~12 wide, y -1.9..1.25: .tick(r, c, "Lecture 1") .light(r, c)
       -> anims; .cell(r, c)
       BuildLine(show=("items",))  in place, x -6.5..6.4, y -1.6..1.2: .build() .publish() .run()
       .set_entry("main"|"hello_http") -> anims; .tag .call_arrow .fn_chip
    V4 TwoDoors()  in place, x -6.5..6.5, y -3.2..1.75: .set_public(on) .call(allowed)
       .clear_calls() .pin_badge() .add_roles(*names) .no_key() .token() .call_out() .you_arrow()
       -> anims. Job badge: service_box("translation-audio (job)") + badge(JOB_SA) + role_chip(…)
    V5 ThinClients()  in place, x -6.5..6.4, y -1.9..2.5: parts gear0/1 chip0/1 ans0/1 dial;
       .recipe() .answers(colour) .drift(1) .to_endpoint() .set_version("v2", bad=True)
       .to_clients() -> anims (show the dial first: parts_in("dial"))
    V6 ServingPlug(show=(...))  in place, x -6.5..6.4, y -2.4..2.3: .write_block(i) (0..5; needs
       the pipeline hidden) .bracket("pre"|"serve") .plug("preprocess"|"raw"|"serve", letter)
       .unplug() -> anims; .bars .out_bars .sock
"""

from __future__ import annotations

import os
import re
import subprocess
import warnings
from functools import lru_cache
from pathlib import Path

import numpy as np
import yaml
from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    PI,
    RIGHT,
    TAU,
    UP,
    AnimationGroup,
    Arc,
    Arrow,
    Circle,
    Create,
    DashedLine,
    DashedVMobject,
    DecimalNumber,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    ManimColor,
    Polygon,
    Rectangle,
    Rotate,
    RoundedRectangle,
    Succession,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    UpdateFromAlphaFunc,
    VMobject,
    Wait,
    linear,
    smooth,
    there_and_back,
)

from explainer import style as S


def guard(ok, msg=""):
    """Layout guard for positions and sizes. Raises locally like an assert; on the GitHub release
    runner, whose fonts set text up to ~1% wider, a miss is only warned about, so a sub-pixel
    difference cannot stop the release render of an already reviewed layout. Content checks
    (captures, narration, arithmetic) stay plain asserts and fail everywhere."""
    if ok:
        return
    if os.environ.get("GITHUB_ACTIONS") == "true":
        warnings.warn(f"layout guard tolerated on CI: {msg}", stacklevel=2)
        return
    raise AssertionError(msg)
from explainer.components import person_icon, ponder_card, timeline  # noqa: F401,E402  (re-exported)
from explainer.devops import (  # noqa: F401,E402  (re-exported for the scenes)
    CAPTION,
    LABEL,
    MONO,
    OUTPUT,
    PANEL,
    SANS,
    SMALL,
    TAG,
    TERM_BG,
    box,
    browser_window,
    cell_width,
    check_mark,
    chip,
    cloud,
    code_block,
    code_panel,
    code_span,
    cross_mark,
    file_glyph,
    folder_glyph,
    glyph_range,
    label,
    laptop,
    lecture_ref,
    line_bar,
    line_pitch,
    mono,
    mono_line,
    server,
    step_badge,
    substring,
    tag,
    warning_sign,
)
from explainer.script import load_narration  # noqa: E402

# ------------------------------------------------------------------ paths and data
HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
SOURCE = ASSETS / "source"

SPEC = yaml.safe_load((PROJECT / "video.yaml").read_text())
TITLES = {s["cls"]: s["title"] for s in SPEC["scenes"]}
_script = PROJECT / "script.md"
NARRATION = load_narration(_script) if _script.exists() else {}

# ------------------------------------------------------------------ semantic colours (BRIEF.md "Colours")
CLIENT = S.GREY          # your laptop, the clients (browser, phone app, web page), "you" the deployer
LAPTOP = CLIENT
YOU = CLIENT
CLOUD = S.BLUE           # Cloud Run (services, jobs, functions), the VM, the Vertex AI endpoint, buckets,
                         # Cloud Scheduler, Artifact Registry; runtime identities (the service-account badge)
IDENTITY = CLOUD
CTR = S.TEAL             # the image and its containers; a running instance's inner box
SYSTEM = S.ORANGE        # the base image's own Python (python:3.12-slim-bookworm, S04 only)
OWN = S.GREEN            # what you own and ship: main.py, requirements.txt, hello_http, serve/batch, the
                         # SavedModel, serving_function, the preprocessing gear
TOOL = S.PURPLE          # functions-framework, gunicorn, Cloud Build, the TensorFlow model server
ERR = S.RED              # errors and wrong answers: the endless job, entry-point mismatch, 403, the ✗
TURN = S.YELLOW          # look here now: request pulses, timers, the right option
PULSE = TURN
COST = S.GOLD            # money: meters, idle shading, the min-instances drip, the always-on endpoint;
KEY = COST               # the (absent) key glyph, dashed and crossed
ROUTE = S.PINK           # HTTP requests and URLs, query strings, the Scheduler trigger, gs:// paths, b64 bodies
LOOKUP = ROUTE
INK = S.WHITE
DIMMED = S.GREY

# ------------------------------------------------------------------ names on screen (script.md "Names")
# No real person's name anywhere. The only one in the copied sources is the instructor's first name
# in model-deployment/README.md line 136 (never quoted: NEVER_SOURCE); every line that goes on screen
# through these helpers is checked (guard_names). There are no masks in this video (MASKS is empty:
# the README's own placeholders YOUR_PROJECT_ID / YOUR_INPUT_BUCKET are shown as written).
MASKS: tuple[str, ...] = ()
_NAME_RE = re.compile(r"\bpavlos\b", re.IGNORECASE)
NEVER_SOURCE = {      # file lines never quoted (they hold a person's name)
    "model-deployment/README.md": {136},
}


def guard_names(s: str) -> str:
    """Raise ValueError if s holds a person's name (never on screen). Returns s."""
    if _NAME_RE.search(s):
        raise ValueError("this line holds a person's name: it is never shown (script.md 'Names')")
    return s


unname = guard_names     # the generic helpers call unname(): here it only checks


# ------------------------------------------------------------------ the running example (from assets/source)
IMAGE = "cgumb/ac215-translation-demo:lecture14-agent-platform-20261022"   # README.md (the image URL)
RUNTIME_SA = "translation-demo-runtime"
RUNTIME_SA_EMAIL = "translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com"   # as the README writes it
JOB_SA = "translation-audio-job"
JOB_NAME = "translation-audio"
SERVICE_NAME = "translation-demo"
IN_BUCKET = "gs://YOUR_INPUT_BUCKET/…"
OUT_BUCKET = "gs://YOUR_OUTPUT_BUCKET/…"
ENTRY = "hello_http"                     # function/main.py line 8; README.md line 150
BASE_IMAGE = "python:3.12-slim-bookworm"  # Dockerfile line 1
PORT = 8080                              # Dockerfile line 2; __main__.py line 23
JOB_STEPS = ("read", "translate", "speak", "save")      # __main__.py lines 53-57
CHEESES = ("parmigiano", "gruyere", "brie", "gouda")    # model-deployment/README.md line 187
PREP_STEPS = ("decode", "to float", "resize")           # model-deployment/cli.py lines 102-104
GUIDE = "MLOps_Learning · guides/L14-serverless-deployment.md"

# ------------------------------------------------------------------ layout
BOTTOM = -3.5                    # the lowest edge anything sits on
SAFE_X, SAFE_Y = 6.6, 3.6
MAP_Y = 3.3                      # the exam map's centre y (top strip)
MAP_LEFT, MAP_RIGHT = -6.6, 2.3  # the exam map's span; lecture_ref stays right of x = REF_LEFT
REF_LEFT = 2.45                  # (script.md said 3.2 / 3.4: the widest tag, "Lecture 14 · slides 8, 11, 14", is 4.04)
TERM_W = 12.6                    # the widest panel (log_panel default)


def lref(lecture: int, slides: str) -> VGroup:
    """The GREY "Lecture 14 · slide 14" tag, top right: lref(14, "14"), lref(15, "13"),
    lref(14, "8, 11, 14"). Guards that it stays right of x = REF_LEFT (2.45; the map ends at 2.3)."""
    g = lecture_ref(lecture, slides)
    guard(g.get_left()[0] >= REF_LEFT - 1e-6,
          f"lecture tag {slides!r} is {g.width:.2f} wide: it would reach the exam map (left {g.get_left()[0]:.2f})")
    return g


def lref_swap(scene, old, lecture: int, slides: str, run_time: float = 0.5) -> VGroup:
    """Replace the lecture tag (old may be None): the old tag fades out, then the new one fades in,
    in the same run_time (plays). Returns the new tag (on screen)."""
    new = lref(lecture, slides)
    if old is None:
        scene.play(FadeIn(new), run_time=run_time)
    else:
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=run_time)
    return new


# ------------------------------------------------------------------ sources (assets/source/<repo>/<path>)
REPOS = ("serverless-deployment", "model-deployment")
README_SD = "serverless-deployment/README.md"
README_MD = "model-deployment/README.md"


def src_path(name: str) -> str:
    """Resolve a source name under assets/source. Names start with the repo: "serverless-deployment/
    tutorial/function/main.py", "model-deployment/cli.py". Short forms: "README.md" (the
    serverless-deployment README), "cli.py" (model-deployment/cli.py), and any path under
    serverless-deployment/ without the repo prefix ("tutorial/app/Dockerfile")."""
    if not name.startswith(REPOS):
        if name == "cli.py":
            name = "model-deployment/cli.py"
        else:
            name = "serverless-deployment/" + name
    if not (SOURCE / name).is_file():
        raise FileNotFoundError(f"assets/source/{name} not found")
    return name


def source_text(name: str) -> str:
    """A tutorial file as text (do not print it whole: excerpt()/src_panel() check every line)."""
    return (SOURCE / src_path(name)).read_text(encoding="utf-8")


def _source_lines(name: str, nums, strip_emoji_: bool = False) -> dict[int, str]:
    path = src_path(name)
    lines = source_text(name).split("\n")
    bad = NEVER_SOURCE.get(path, set()) & set(nums)
    if bad:
        raise ValueError(f"{path}: lines {sorted(bad)} are never shown (they hold a person's name)")
    out = {}
    for n in nums:
        if not 1 <= n <= len(lines):
            raise IndexError(f"{path} has {len(lines)} lines (asked for {n})")
        s = lines[n - 1].expandtabs(4)
        if path.endswith(".md"):
            s = s.replace("**", "")            # script.md: README excerpts drop the bold marks
        guard_names(s)
        out[n] = _emoji_guard(s, f"{path} line {n}", strip_emoji_)
    return out


def shown_path(name: str) -> str:
    """The path in a panel header (script.md "CODE"): the serverless-deployment/ prefix is dropped
    ("README.md", "tutorial/app/Dockerfile"); model-deployment/ is kept ("model-deployment/cli.py")."""
    p = src_path(name)
    return p[len("serverless-deployment/"):] if p.startswith("serverless-deployment/") else p


def readme(a: int, b: int | None = None, repo: str = "serverless-deployment") -> list[str]:
    """README.md lines a..b (1-based, inclusive; bold marks dropped) as a list, stripped of
    Markdown list/quote marks only where they lead ('- ', '> '): the words of a README card.
    repo="model-deployment" for the other README."""
    rows = excerpt(f"{repo}/README.md", a, a if b is None else b).split("\n")
    return [re.sub(r"^\s*(?:[-*>]\s+)", "", r).rstrip() for r in rows]


# ================================================================== generic helpers (from L08, tested there)
EMOJI = frozenset("📊📝🔵🟢✅✓❌⚠🧀🤖" + chr(0xFE0F))
# a captured line's leading emoji becomes its colour: 🔵 Base Model GREY, 🟢 Fine-Tuned GREEN
EMOJI_COLORS = (("❌", ERR), ("⚠", ERR), ("🟢", OWN), ("✅", OWN), ("🔵", S.GREY))


# ================================================================== generic helpers (from L07, tested there)
@lru_cache(maxsize=None)
def _mono_has(ch: str) -> bool:
    """True when the house mono font (or, failing that check, the system) has a glyph for ch."""
    try:
        out = subprocess.run(["fc-list", f":charset={ord(ch):x}", "family"], capture_output=True,
                             text=True, timeout=5).stdout
    except (OSError, subprocess.SubprocessError):
        return True
    return any("DejaVu Sans Mono" in f for f in out.splitlines())


def dropped_chars(s: str) -> list[str]:
    """Characters of s the house mono font cannot draw (emoji): they would vanish silently."""
    return sorted({ch for ch in s if ord(ch) > 0x2000 and not _mono_has(ch)})


def strip_emoji(s: str) -> str:
    """s without its emoji (EMOJI, and any other character the mono font drops) and the space they
    leave; the words stay exactly as captured (script.md "Emoji")."""
    bad = set(dropped_chars(s)) | {ch for ch in s if ch in EMOJI}
    if not bad:
        return s
    lead = len(s) - len(s.lstrip(" "))
    out = "".join(ch for ch in s if ch not in bad)
    body = re.sub(r"(?<=\S) {2,}(?=\S)", " ", out).lstrip()
    return (" " * lead + body) if body.strip() else out


def _emoji_guard(s: str, where: str, strip: bool) -> str:
    if strip:
        return strip_emoji(s)
    bad = dropped_chars(s)
    if bad:
        raise ValueError(f"{where}: {bad!r} would vanish (the mono font has no glyph): leave the line "
                         "out, or pass strip_emoji=True (script.md: print it without its emoji)")
    return s


def emoji_color(raw: str, default: str = OUTPUT) -> str:
    """The colour a captured line prints in, from the emoji it starts with: ❌ / ⚠️ RED, ✅ GREEN,
    🤖 (a model call) BLUE, anything else `default` (output grey)."""
    head = raw.lstrip()
    for e, col in EMOJI_COLORS:
        if head.startswith(e):
            return col
    return default


def _looks_code(s: str) -> bool:
    return " " not in s and bool(re.search(r"[-_.]", s))




def _out_early(t: float) -> float:
    """rate_func: done in the first 45% of the run (the old text of a swap leaves first)."""
    return smooth(min(1.0, t / 0.45))


def _in_late(t: float) -> float:
    """rate_func: starts at 55% of the run (the new text of a swap, after a short gap)."""
    return smooth(max(0.0, (t - 0.55) / 0.45))


def _in_first_half(t: float) -> float:
    return smooth(min(1.0, 2 * t))


def _out_second_half(t: float) -> float:
    return smooth(max(0.0, 2 * t - 1))


class _SwapOut(FadeOut):
    """The FadeOut of a text a swap replaces: the text stays a member of `parent` (and visible)
    until this fade is over, then leaves it for good (a member left behind at full opacity would
    snap back when the parent is next added or animated)."""

    def __init__(self, mob, parent, **kw):
        super().__init__(mob, **kw)
        self.swap_parent = parent

    def clean_up_from_scene(self, scene) -> None:
        super().clean_up_from_scene(scene)
        if self.mobject in self.swap_parent.submobjects:
            self.swap_parent.remove(self.mobject)


class _SwapIn(FadeIn):
    """The FadeIn of the text a swap brings: a member from the moment the swap is built, but at
    opacity 0 until this animation begins (a swap built early, e.g. passed as resize(extra=...),
    whose caller plays something else first, showed the new text in that play: S10 at 28.4 s)."""

    def begin(self) -> None:
        _set_op(self.mobject, attr="_swop")
        super().begin()


def _stage_swap(parent, old, new) -> None:
    """`new` joins `parent` right after `old` (so it takes old's slot once old leaves), invisible
    until its _SwapIn begins; `old` stays until its _SwapOut is over."""
    _save_op(new, "_swop")
    _set_op(new, 0, "_swop")
    if old in parent.submobjects:
        parent.insert(parent.submobjects.index(old) + 1, new)
    else:
        parent.add(new)


def _swap_text(parent, old, new) -> list:
    """Sequential text swap in ONE play (L05 final review: faded at once, both texts were
    half-readable mid-swap; a Transform between different strings scrambled the letters): `old`
    fades out in the first 45% of the run, `new` fades in from 55% (rate_funcs inside the same
    run_time, so the caller's timing is unchanged). `new` joins `parent` now (invisible until the
    swap plays) and `old` leaves it when its fade is over. Returns the two animations."""
    _stage_swap(parent, old, new)
    return [_SwapOut(old, parent, rate_func=_out_early), _SwapIn(new, rate_func=_in_late)]


def swap_text(parent, old, new) -> list:
    """Public: the sequential swap of two texts at one place (old fades out in the first 45% of the
    play, new fades in from 55%); `new` joins `parent` at once (invisible until the play), `old`
    leaves it after its fade. self.play(*swap_text(card, card.text, new_text)). Never Transform one
    string into another (the letters scramble)."""
    return _swap_text(parent, old, new)


def _comment_at(line: str) -> int:
    """Index of the '#' that starts a comment (outside quotes, not inside a word), or -1."""
    quote = None
    for i, ch in enumerate(line):
        if quote:
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch
        elif ch == "#" and (i == 0 or line[i - 1] in " \t"):
            return i
    return -1


def cut_comment(line: str, limit: int = 65) -> str:
    """A line longer than `limit` loses its trailing comment, shown as '# …'."""
    if len(line) <= limit:
        return line
    i = _comment_at(line)
    if i < 0:
        return line
    code = line[:i]
    return code.rstrip() + "  # …" if code.strip() else code + "# …"


def excerpt(name: str, first: int, last: int, cut_comments: bool = False,
            strip_emoji: bool = False) -> str:
    """Lines first..last (1-based, inclusive) of a tutorial file in assets/source (IDs masked).
    Never-shown lines raise."""
    d = _source_lines(name, range(first, last + 1), strip_emoji)
    res = [d[n] for n in range(first, last + 1)]
    if cut_comments:
        res = [cut_comment(s) for s in res]
    return "\n".join(res)


def source_line(name: str, n: int, strip_emoji: bool = False) -> str:
    """One line of a tutorial file (for excerpt_chip(..., line=...))."""
    return _source_lines(name, [n], strip_emoji)[n]


def sans(s: str, size: float = CAPTION, color: str = INK, **kw) -> Text:
    """CMU Sans Serif text (box labels, card lines)."""
    return label(s, size, color, font=SANS, **kw)


def note(s: str, color: str = S.GREY, size: float = CAPTION) -> Text:
    """A GREY caption (serif, 20 pt)."""
    return label(s, size, color)


def mtext(s: str, size: float = CAPTION, color: str = INK, font: str = MONO) -> Text:
    """Text through unname(), the masks drawn GREY (mono by default; font=SANS or S.FONT)."""
    s = unname(s)
    t2c = {m: S.GREY for m in MASKS if m in s}
    return S.text(s, size, color, font=font, t2c=t2c)


def grey_masks(line, ellipses: bool = True, color: str = S.GREY):
    """Colour every customer mask (and every '…', the sign of something left out) in a mono_line
    GREY; a folded command (a VGroup with .rows) is handled row by row. Returns line."""
    rows = line.rows if hasattr(line, "rows") else [line]
    for r in rows:
        s = getattr(r, "text", None)
        if not s or not hasattr(r, "glyphs"):
            continue
        for sub in ([*MASKS, "…"] if ellipses else list(MASKS)):
            i = s.find(sub)
            while i >= 0:
                glyph_range(r, i, i + len(sub)).set_color(color)
                i = s.find(sub, i + len(sub))
    return line


def _keep(m):
    """Mark a group (chip, tag, labelled glyph) to keep its size in Piece.rescale()."""
    m.keep_size = True
    return m


def keep_size(m):
    """Public: mark a group you built (a chip, a tag, a labelled glyph) to keep its size when a set
    piece it joins is rescaled (Piece.rescale shrinks shapes, never text). Returns m."""
    return _keep(m)


def _mix(color, k: float) -> ManimColor:
    """An opaque colour k of the way from the background to `color`."""
    return ManimColor(S.BG).interpolate(ManimColor(color), k)


def _poly(points, color: str = LOOKUP, stroke: float = 4) -> VMobject:
    """A polyline through `points` (elbow routes)."""
    m = VMobject(stroke_color=color, stroke_width=stroke)
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in points])
    return m


def under(mob, color: str = TURN, stroke: float = 4, buff: float = 0.05) -> Line:
    """A Line under `mob` (a terminal line, a substring of one, a code span)."""
    return Line(mob.get_corner(DOWN + LEFT) + DOWN * buff, mob.get_corner(DOWN + RIGHT) + DOWN * buff,
                color=color, stroke_width=stroke)


def strike(mob, color: str = ERR, stroke: float = 4) -> Line:
    """A Line through the middle of `mob` (a struck-through name or chip)."""
    return Line(mob.get_left() + LEFT * 0.06, mob.get_right() + RIGHT * 0.06, color=color,
                stroke_width=stroke)


def ring(mob, color: str = ERR, buff: float = 0.08, stroke: float = 3) -> VMobject:
    """A rounded outline around `mob`."""
    r = RoundedRectangle(width=mob.width + 2 * buff, height=mob.height + 2 * buff,
                         corner_radius=min(0.12, (mob.height + 2 * buff) / 2), stroke_color=color,
                         stroke_width=stroke).set_fill(opacity=0)
    return r.move_to(mob)


def at_bottom(mob, y: float = BOTTOM, x: float = 0.0):
    """Put mob's bottom edge on y (the terminal line) and centre it at x (a code strip)."""
    return mob.shift(np.array([x - mob.get_center()[0], y - mob.get_bottom()[1], 0]))


def grey_tag(s: str) -> VGroup:
    return _keep(tag(s, S.GREY))


def illustration_tag(note_: str | None = None) -> VGroup:
    """GREY 'illustration' (every schematic: Colab, the browser, the editor, the rings, the
    turnstile, the jar, the shelf, the "what if" variants); note_="what if" -> 'illustration · what if'."""
    return grey_tag("illustration" + (f" · {note_}" if note_ else ""))


def concept_tag(s: str = "concept · lecture only") -> VGroup:
    """The GREY dashed tag of a lecture idea with no code here (LLM as judge, MCP, peer handoffs,
    skill scripts/, Think and Reason inside the model)."""
    g = tag(s, S.GREY)
    dashed = DashedVMobject(g.box, num_dashes=int(g.box.width * 9), dashed_ratio=0.55)
    dashed.set_stroke(S.GREY, 2)
    fill = g.box.copy().set_stroke(width=0)
    res = VGroup(fill, dashed, g.text)
    res.box, res.text = fill, g.text
    return _keep(res)


def stamp(text: str, color: str = ERR, size: float = TAG, angle: float = 0.08) -> VGroup:
    """An outlined, slightly rotated stamp (BLOCKED, data, not instructions …). Opaque dark fill:
    put it where it covers nothing you need to read. .frame .text"""
    t = sans(text, size, color, weight="BOLD")
    r = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.22, corner_radius=0.06,
                         stroke_color=color, stroke_width=3).set_fill(S.BG, 0.85)
    t.move_to(r)
    g = VGroup(r, t).rotate(angle)
    g.frame, g.text = r, t
    return _keep(g)


def fix_chip(text: str, color: str = OWN, font: str | None = None) -> VGroup:
    """A GREEN "the fix" chip (serif text; font=MONO for code)."""
    return _keep(chip(text, color, size=CAPTION, font=font))


def concept_box(text: str, size: float = CAPTION, color: str = S.GREY, min_w: float = 0.0,
                text_color: str = INK, h: float | None = None) -> VGroup:
    """A GREY dashed box holding a lecture concept (MCP, LLM as judge, handoffs …). .box .text"""
    t = label(text, size, text_color)
    h = h or mono("|", size).height + 0.26
    b = box(max(min_w, t.width + 0.5), h, color, dashed=True, radius=h / 2.6)
    bg = RoundedRectangle(width=b.width, height=h, corner_radius=h / 2.6, stroke_width=0).set_fill(S.BG, 0.9)
    t.move_to(b)
    g = VGroup(bg, b, t)
    g.box, g.text = b, t
    return _keep(g)


_LANG = {".py": "python", ".toml": "toml", ".sh": "bash", ".md": "markdown", ".yaml": "yaml",
         ".yml": "yaml", ".json": "json", ".html": "html", ".txt": "text", ".lock": "toml"}


def _lang(path: str) -> str:
    p = Path(path)
    if p.name == "Dockerfile":
        return "docker"
    if p.name in (".gitignore", ".dockerignore") or p.name.startswith(".env"):
        return "text"
    return _LANG.get(p.suffix, "text")


def _looks_path(p: str) -> bool:
    return bool(re.search(r"\.[A-Za-z]\w*$", p)) or ("/" in p and " " not in p)


def _header_text(text: str, size: float = CAPTION) -> VGroup:
    """'cli.py · lines 183–194' -> mono path + serif rest; 'Agent Harness · cell 10 · lines 3–6' all
    serif."""
    parts = text.split(" · ")
    mobs = []
    path_done = False
    for i, p in enumerate(parts):
        s = p if i == 0 else f"· {p}"
        if _looks_path(p) and not path_done:
            mobs.append(mono(s, size, S.GREY))
            path_done = True
        else:
            mobs.append(label(s, size, S.GREY))
    return VGroup(*mobs).arrange(RIGHT, buff=0.12)


def _with_header(panel: VGroup, text: str, size: float = CAPTION, subtitle: str | None = None) -> VGroup:
    """Replace a code_panel's header with `text` (+ a GREY quoted subtitle after it)."""
    header = _header_text(text, size)
    if subtitle:
        header.add(label(f"“{subtitle}”" if not subtitle.startswith("your copy") else subtitle,
                         size, S.GREY))
        header.arrange(RIGHT, buff=0.12)
        header[-1].shift(RIGHT * 0.15)
    header.next_to(panel.code, UP, buff=0.1).align_to(panel.code, LEFT).shift(RIGHT * 0.12)
    panel.remove(panel.header)
    panel.header = header
    panel.add(header)
    return panel


def _wrap_line(line: str, breaks: list[str]) -> list[str]:
    """Break a code line before each substring in `breaks` (in order); continuation rows keep
    the line's indent plus '  ↪ '."""
    indent = line[:len(line) - len(line.lstrip())]
    rows, rest = [], line
    for b in breaks:
        i = rest.find(b, 1)
        if i < 0:
            raise ValueError(f"{b!r} not in {rest!r}")
        rows.append(rest[:i].rstrip())
        rest = rest[i:]
    rows.append(rest)
    return [rows[0]] + [f"{indent}  ↪ {r.strip()}" for r in rows[1:]]


def _auto_wrap(line: str, limit: int = 65) -> list[str]:
    """Break a line longer than `limit` at spaces; continuation rows: indent + '  ↪ '."""
    if len(line) <= limit:
        return [line]
    indent = line[:len(line) - len(line.lstrip())]
    pre = indent + "  ↪ "
    rows, rest, first = [], line, True
    while len(rest) > (limit if first else limit - len(pre)):
        lim = limit if first else limit - len(pre)
        i = rest.rfind(" ", len(indent) + 1 if first else 1, lim)
        if i <= 0:
            i = lim
        rows.append(rest[:i].rstrip() if first else pre + rest[:i].strip())
        rest = rest[i:].lstrip()
        first = False
    rows.append(rest if first else pre + rest.strip())
    return rows


def _lex_whole(code, code_rows, whole, spots, language: str, size: float) -> None:
    """Colour the rows of each wrapped line as the lexer colours the WHOLE line (S03, S11, S13
    critics: src_panel wrapped before lexing, so a wrapped string's continuation row was lexed as
    code and came out half-coloured). `whole` is the panel's rows with every wrapped line in one
    piece; spots = {file line: (its row in `whole`, its rows in the panel)}. A reference
    code_block of `whole` (same language and style, lexed in context) lends its glyph colours to
    the wrapped rows, the ↪ marks skipped (they turn GREY afterwards). A line whose glyphs don't
    pair up one to one is left as it was."""
    ref = code_block("\n".join(whole), language, size)
    for r, ks in spots.values():
        src = [g for g in ref.code_lines[r]]
        dst = []
        for k in ks:
            txt = "".join(code_rows[k].split())
            glyphs = list(code.code_lines[k]) if k < len(code.code_lines) else []
            if len(glyphs) != len(txt):
                dst = None
                break
            dst += [g for c, g in zip(txt, glyphs) if not (c == "↪" and k != ks[0])]
        if dst is None or len(dst) != len(src):
            continue
        for d, g in zip(dst, src):
            d.set_color(g.get_color())


def _line_bars(code, ks, color, opacity) -> VGroup:
    """src_panel's .bar(n): a VGroup of line bars over rows ks; the rows of ONE wrapped line get a
    single bar from the first row's top to the last row's bottom (one bar per row overlapped in a
    brighter seam: S12 critic)."""
    bars = [line_bar(code, k, color, opacity) for k in ks]
    if len(bars) < 2:
        return VGroup(*bars)
    top = max(b.get_top()[1] for b in bars)
    bot = min(b.get_bottom()[1] for b in bars)
    one = Rectangle(width=bars[0].width, height=top - bot, stroke_width=0).set_fill(color, opacity)
    return VGroup(one.move_to([bars[0].get_center()[0], (top + bot) / 2, 0]))


def _spec_lines(spec) -> list[int]:
    out: list[int] = []
    for s in spec:
        if isinstance(s, int):
            out.append(s)
        else:
            out += list(range(s[0], s[1] + 1))
    if out != sorted(set(out)):
        raise ValueError(f"folded lines must increase: {spec}")
    return out


def src_panel(name: str, first, last: int | None = None, cut_comments: bool = False,
              focus=None, size: float = 22, width: float | None = None,
              shown: str | None = None, suffix: str | None = None, wrap=None, join=None,
              subtitle=None, language: str | None = None, strip_emoji: bool = False,
              max_rows: int = 12, wrap_at: int = 65) -> VGroup:
    """code_panel quoting assets/source/<name> (name masked), header "shown · lines a–b" (+ " ·
    comment cut", " · line N wrapped", " · suffix"). `first` may be a list (folded: only those file
    lines, a GREY '…' row at each gap, header "lines a–b (folded)"). join=[(a, b)]: lines a..b as
    one row. wrap=None (default): every line > wrap_at (65) characters wraps; wrap=True / {n: ["sub", …]} as in L05. subtitle: a GREY
    quotes; a str: that text. focus: file line(s) kept bright, the rest dimmed.
    .rows_of(file_line) -> code row indices; .bar(file_line, colour) -> VGroup of line bars (not
    added); .span(file_line, sub) -> glyphs; .source_name .first"""
    folded = isinstance(first, (list, tuple))
    nums = _spec_lines(first) if folded else list(range(first, (first if last is None else last) + 1))
    lo, hi = nums[0], nums[-1]
    lines = _source_lines(name, nums, strip_emoji)
    if cut_comments:
        lines = {n: cut_comment(s) for n, s in lines.items()}
    joined_into: dict[int, int] = {}
    for a, b in (join or []):
        if not all(n in lines for n in range(a, b + 1)):
            raise ValueError(f"join {a}-{b}: every line must be shown")
        lines[a] = lines[a].rstrip() + "".join(lines[n].strip() for n in range(a + 1, b + 1))
        for n in range(a + 1, b + 1):
            joined_into[n] = a
    if wrap is None:                   # auto: wrap every line longer than 65 characters
        wrap = any(len(s) > wrap_at for s in lines.values())
    rows, rows_of, wrapped, gap_rows = [], {}, [], []
    whole, whole_row = [], {}          # the same rows with each wrapped line whole (lexed in context)
    prev = None
    for n in nums:
        if n in joined_into:
            rows_of[n] = rows_of[joined_into[n]]
            prev = n
            continue
        ln = lines[n]
        if prev is not None and n > prev + 1:
            indent = ln[:len(ln) - len(ln.lstrip())]
            gap_rows.append(len(rows))
            rows.append(indent + "…")
            whole.append(indent + "…")
        if isinstance(wrap, dict) and n in wrap:
            parts = _wrap_line(ln, wrap[n])
        elif wrap is True:
            parts = _auto_wrap(ln, wrap_at)
        else:
            parts = [ln]
        if len(parts) > 1:
            wrapped.append(n)
        rows_of[n] = list(range(len(rows), len(rows) + len(parts)))
        rows += parts
        whole_row[n] = len(whole)
        whole.append(ln)
        prev = n
    if len(rows) > max_rows:
        raise ValueError(f"{name} {lo}-{hi}: {len(rows)} rows (at most {max_rows} on screen): "
                         "show it in windows, or fold it")
    shown = shown or shown_path(name)
    p = code_panel("\n".join(rows), shown, lo, language or _lang(src_path(name)), font_size=size,
                   width=width)
    if p.code.width > 12.95:
        raise ValueError(f"{name} {lo}-{hi}: the panel is {p.code.width:.1f} wide (> 12.9): "
                         "wrap=True, or wrap={line: [break before …]}")
    where = f"line {lo}" if lo == hi else f"lines {lo}–{hi}"
    if folded:
        where += " (folded)"
    extra = []
    if cut_comments and any(cut_comment(s) != s for s in _source_lines(name, nums, strip_emoji).values()):
        extra.append("comment cut")
    if wrapped:
        extra.append("long lines wrapped")
    if suffix:
        extra.append(suffix)
    if subtitle is True:
        raise ValueError("subtitle=True was the Colab cell title (L08): pass the text")
    _with_header(p, " · ".join([shown, where, *extra]), subtitle=subtitle or None)
    code_rows = p.code.source.split("\n")
    if wrapped:
        _lex_whole(p.code, code_rows, whole, {n: (whole_row[n], rows_of[n]) for n in wrapped},
                   language or _lang(src_path(name)), size)
    for k in range(len(code_rows)):                 # GREY ↪ marks, '…' gap rows and the mask
        for sub in ("↪", "…", *MASKS):
            if sub == "↪" and k not in [r for ks in rows_of.values() for r in ks[1:]]:
                continue
            if sub == "…" and k not in gap_rows:
                continue
            occ = 0
            while True:
                try:
                    code_span(p.code, k, sub, occ).set_color(S.GREY)
                except (ValueError, IndexError):
                    break
                occ += 1
    if focus is not None:
        keep = {focus} if isinstance(focus, int) else set(focus)
        for n, ks in rows_of.items():
            if n not in keep:
                for k in ks:
                    if k < len(p.code.code_lines):
                        p.code.code_lines[k].set_opacity(0.3)
    p.source_name, p.first, p.rows_map = name, lo, rows_of
    p.rows_of = lambda n: rows_of[n]
    p.bar = lambda n, color=TURN, opacity=0.18: _line_bars(p.code, rows_of[n], color, opacity)

    def span(n, sub, occurrence=0):
        for k in rows_of[n]:
            try:
                return code_span(p.code, k, sub, occurrence)
            except ValueError:
                continue
        raise ValueError(f"{sub!r} not in line {n} of {name}")
    p.span = span
    return p


def _mono_rows(lines, size: float, color: str, max_chars: int | None = None) -> VGroup:
    rows = VGroup()
    pitch = line_pitch(size)
    for i, s in enumerate(lines):
        s, col = (s, color) if isinstance(s, str) else s
        s = strip_emoji(unname(s))
        if max_chars and len(s) > max_chars:
            s = s[:max_chars - 1] + "…"
        ln = mono_line(s, size, col)
        grey_masks(ln)
        ln.shift(np.array([0, -i * pitch, 0]) - ln.strut.get_corner(UP + LEFT))
        rows.add(ln)
    return rows


def log_panel(lines: list[str], header: str, width: float = TERM_W, size: float = CAPTION,
              color: str = OUTPUT) -> VGroup:
    """PANEL: plain mono rows (a recorded line, a diff, out.txt) on a dark rounded panel with a GREY
    header above. Rows longer than the panel are cut with '…'; masks and '…' GREY. .rows .frame
    .header"""
    max_chars = int((width - 0.5) / cell_width(size))
    rows = _mono_rows(lines, size, color, max_chars)
    h = len(lines) * line_pitch(size) + 0.4
    frame = RoundedRectangle(width=width, height=h, corner_radius=0.15, stroke_color=S.GREY_DARK,
                             stroke_width=2).set_fill(PANEL, 1)
    frame.move_to(rows.get_center()).align_to(rows, LEFT).shift(LEFT * 0.25)
    frame.shift(UP * (rows.get_top()[1] + 0.2 - frame.get_top()[1]))
    head = _header_text(header).next_to(frame, UP, buff=0.1).align_to(frame, LEFT).shift(RIGHT * 0.12)
    g = VGroup(frame, rows, head)
    g.frame, g.rows, g.header = frame, rows, head
    return g.move_to(ORIGIN)


def output_box(lines: list[str], header: str | None = None, width: float | None = None,
               size: float = CAPTION, color: str = OUTPUT) -> VGroup:
    """RECORDED: a notebook cell's saved output, drawn as an output area under a cell (never a
    terminal frame): mono rows on a dark panel with a GREY rule at the left; an optional GREY
    header above. Width fits the longest row (or `width`, rows cut with '…'). .rows .frame .rule
    .header (None)"""
    max_chars = int((width - 0.6) / cell_width(size)) if width else None
    rows = _mono_rows(lines, size, color, max_chars)
    w = width or rows.width + 0.6
    h = len(lines) * line_pitch(size) + 0.36
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=S.GREY_DARK,
                             stroke_width=1.5).set_fill(TERM_BG, 1)
    frame.move_to(rows.get_center()).align_to(rows, LEFT).shift(LEFT * 0.35)
    frame.shift(UP * (rows.get_top()[1] + 0.18 - frame.get_top()[1]))
    rule = Line(frame.get_corner(UP + LEFT) + np.array([0.14, -0.12, 0]),
                frame.get_corner(DOWN + LEFT) + np.array([0.14, 0.12, 0]), color=S.GREY, stroke_width=4)
    g = VGroup(frame, rule, rows)
    g.frame, g.rule, g.rows, g.header = frame, rule, rows, None
    if header:
        hd = _header_text(header).next_to(frame, UP, buff=0.1).align_to(frame, LEFT).shift(RIGHT * 0.12)
        g.add(hd)
        g.header = hd
    return g.move_to(ORIGIN)


def readme_chip(where: str, phrase: str | None = None, size: float = CAPTION,
                max_w: float = 12.4, expected: bool = False) -> VGroup:
    """A one-line README chip: GREY `where` ("README.md · line 244 (excerpt)") and the quoted
    phrase in white (expected=True adds the GREY `expected` tag after it). Fails if wider than
    max_w: in the top band right of the tracker pass max_w=6.4 (shorten the phrase). .frame
    .where .phrase .tag"""
    w = _header_text(where, size)
    parts = [w]
    ph = None
    if phrase:
        ph = mtext(f"“{phrase}”", size, INK, font=S.FONT)
        parts.append(ph)
    row = VGroup(*parts).arrange(RIGHT, buff=0.25)
    fr = box(row.width + 0.4, row.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    fr.move_to(row)
    g = VGroup(fr, row)
    g.tag = None
    if expected:
        raise ValueError("no expected output in this video (script.md 'No live runs')")
    if g.width > max_w:
        raise ValueError(f"README chip {g.width:.1f} wide (> {max_w}): shorten {phrase!r}")
    g.frame, g.where, g.phrase = fr, w, ph
    return _keep(g)


class Prose(str):
    """A prose row for turn_card / card_rows (serif, not a command)."""


def _cell(s, size: float = CAPTION, color: str = INK):
    """A card cell: "`code`" -> mono (without backticks), Prose / str -> serif, a mobject as is."""
    if not isinstance(s, str):
        return s
    if len(s) > 1 and s.startswith("`") and s.endswith("`"):
        return mtext(s[1:-1], size, color)
    return mtext(str(s), size, color, font=S.FONT)


def readme_card(where: str, lines: list[str], width: float | None = None,
                size: float = CAPTION) -> VGroup:
    """A multi-line GREY README card: header `where` above, the README's words inside (a line in
    backticks is mono). .frame .rows .header"""
    rows = VGroup(*[_cell(s, size) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    w = max(width or 0, rows.width + 0.5)
    fr = box(w, rows.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    head = _header_text(where, size).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head
    return g


def _md_text(s: str, size: float = CAPTION, color: str = INK) -> Text:
    """One README line as ONE Text: inline `code` in mono (backticks dropped, spacing kept), the rest
    serif; masks GREY."""
    s = unname(s)
    parts = s.split("`")
    plain, spans, pos = "", [], 0
    for k, p in enumerate(parts):
        if k % 2:
            spans.append((len(plain), len(plain) + len(p)))
        plain += p
    t2c = {m: S.GREY for m in MASKS if m in plain}
    return S.text(plain, size, color, t2f={f"[{a}:{b}]": MONO for a, b in spans if b > a}, t2c=t2c)


def _wrap_words(s: str, limit: int) -> list[str]:
    """Break prose at spaces into rows of at most `limit` characters (a long word stays whole)."""
    rows, cur = [], ""
    for w in s.split(" "):
        if cur and len(cur) + 1 + len(w) > limit:
            rows.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    rows.append(cur)
    return rows


def excerpt_chip(sub: str, header: str, color: str = INK, frame: str = S.GREY,
                 line: str | None = None, size: float = CAPTION) -> VGroup:
    """An excerpt chip: a mono chip holding the exact sub-string `sub` of one source or capture
    line, headed `header` ("cli.py · line 459 (excerpt)"). Pass the full `line` (excerpt(...) or
    cap.line(n)) to check the sub-string. .chip .text .header"""
    sub = unname(sub)
    if line is not None and sub not in unname(line):
        raise ValueError(f"{sub!r} is not in {line!r}")
    c = chip(sub, frame, size=size, text_color=color, font=MONO, fill_opacity=0.1)
    if any(m in sub for m in MASKS):
        new = mtext(sub, size, color).move_to(c.text)
        c.remove(c.text)
        c.add(new)
        c.text = new
    h = _header_text(header, size).next_to(c, UP, buff=0.08).align_to(c, LEFT).shift(RIGHT * 0.08)
    g = VGroup(c, h)
    g.chip, g.text, g.header = c, c.text, h
    return _keep(g)


def cmd_chip(cmd: str, note_: str | None = None, color: str = S.GREY, size: float = CAPTION,
             note_color: str = S.GREY) -> VGroup:
    """A command shown, not typed: a mono chip, and an optional note under it. .chip .note"""
    c = chip(cmd, color, size=size, font=MONO)
    if not note_:
        c.chip, c.note = c, None
        return _keep(c)
    n = label(note_, size, note_color).next_to(c, DOWN, buff=0.1).align_to(c, LEFT)
    g = VGroup(c, n)
    g.chip, g.note = c, n
    return _keep(g)


def _mixed_row(parts, size: float = CAPTION, color: str = INK) -> Text:
    """One row mixing mono ("`code`") and serif pieces as ONE Text (one baseline), pieces joined
    by a space (none before a piece that starts with , . : ? ; or ·…)."""
    s, spans = "", []
    for p in parts:
        code = len(p) > 1 and p.startswith("`") and p.endswith("`")
        txt = unname(p[1:-1] if code else p)
        if s and (code or txt[0] not in ",.:?;"):
            s += " "
        if code:
            spans.append((len(s), len(s) + len(txt)))
        s += txt
    t2c = {m: S.GREY for m in MASKS if m in s}
    return S.text(s, size, color, t2f={f"[{a}:{b}]": MONO for a, b in spans}, t2c=t2c)


def card_rows(items, width: float | None = None, header: str | None = None,
              size: float = CAPTION, frame_color: str = S.GREY, buff: float = 0.16) -> VGroup:
    """A GREY card of rows (fix cards, checklists): each item is a str (serif; "`mono`" in
    backticks), (str, colour), or a mobject. .frame .rows .header; rows write in with
    self.play(FadeIn(card.rows[i]))."""
    rows = VGroup()
    for it in items:
        if isinstance(it, tuple):
            rows.add(_cell(it[0], size, it[1]))
        else:
            rows.add(_cell(it, size, INK))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    w = max(width or 0, rows.width + 0.6)
    fr = box(w, rows.height + 0.5, frame_color, fill=S.BG, fill_opacity=0.95, radius=0.14)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, rows)
    g.header = None
    if header:
        h = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
        g.add(h)
        g.header = h
    g.frame, g.rows = fr, rows
    return g


def table_card(headers, rows, col_w=None, size: float = CAPTION, header_colors=None,
               buff: float = 0.16) -> VGroup:
    """A two- or three-column card. headers: column titles; rows: lists of cells (str, "`mono`",
    or a mobject). .cells[r][c] .heads .frame. Not added; write rows in with
    FadeIn(VGroup(*card.cells[r]))."""
    ncol = len(headers)
    header_colors = header_colors or [S.GREY] * ncol
    heads = [label(h, size, c) for h, c in zip(headers, header_colors)]
    cells = [[_cell(c, size) for c in r] for r in rows]
    widths = col_w or [max([heads[c].width] + [r[c].width for r in cells]) + 0.4 for c in range(ncol)]
    pitch_rows = [max(m.height for m in r) for r in cells]
    hh = max(h.height for h in heads)
    total_h = hh + sum(pitch_rows) + buff * (len(rows) + 1) + 0.5
    total_w = sum(widths) + 0.4
    fr = box(total_w, total_h, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    x0, y = fr.get_left()[0] + 0.2, fr.get_top()[1] - 0.25
    xs = [x0 + sum(widths[:c]) for c in range(ncol)]
    for c, h in enumerate(heads):
        h.move_to([xs[c], y - hh / 2, 0], aligned_edge=LEFT)
    y -= hh + buff
    sep = Line([fr.get_left()[0] + 0.15, y + buff / 2, 0], [fr.get_right()[0] - 0.15, y + buff / 2, 0],
               color=S.GREY_DARK, stroke_width=2)
    for r, row in enumerate(cells):
        for c, m in enumerate(row):
            m.move_to([xs[c], y - pitch_rows[r] / 2, 0], aligned_edge=LEFT)
        y -= pitch_rows[r] + buff
    g = VGroup(fr, sep, *heads, *[m for r in cells for m in r])
    g.frame, g.heads, g.cells = fr, heads, cells
    return g


def ponder_at(scene, question: str, seconds: float = 8.0, y: float = -2.2,
              width: float = 10.2, hide=()) -> VGroup:
    """The ponder card (pause_and_ponder's look) in the lower third, opaque, its timer draining
    over `seconds`; its bottom never goes below -3.55. `hide` (e.g. a 3-row strip) fades out as
    the card arrives (bring it back yourself). Returns the card (FadeOut it at the start of the
    next SAY block)."""
    card = ponder_card(question, width=width).move_to([0, y, 0])
    card[0].set_fill(S.BG, 1)
    if card.get_bottom()[1] < -3.55:
        card.shift(UP * (-3.55 - card.get_bottom()[1]))
    scene.play(FadeIn(card, scale=0.95), *[FadeOut(m) for m in hide], run_time=0.6)
    bar = card[3]
    scene.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
               run_time=seconds)
    return card


class Counter(VGroup):
    """A counter "chunks: 8,248": a label and a number (with thousands commas) driven by a
    ValueTracker. .count_to(n, run_time) -> animation; .freeze() before it leaves. .num .label"""

    def __init__(self, text: str | None = "chunks", value: float = 0, color: str = INK,
                 size: float = 26, **kw):
        super().__init__(**kw)
        self.tracker = ValueTracker(value)
        self.num = DecimalNumber(value, num_decimal_places=0, group_with_commas=True,
                                 font_size=size * 1.3, color=color)
        self.num.add_updater(lambda m: m.set_value(self.tracker.get_value()))
        self.label = None
        if text:
            self.label = label(f"{text}:", size, color)
            self.num.next_to(self.label, RIGHT, buff=0.15).align_to(self.label, DOWN)
            self.add(self.label)
        self.add(self.num)
        _keep(self)

    def count_to(self, n: float, run_time: float = 1.0):
        return self.tracker.animate(rate_func=linear, run_time=run_time).set_value(n)

    def freeze(self):
        self.num.clear_updaters()
        return self


def key_glyph(h: float = 0.3, color: str = KEY, name: str | None = None) -> VGroup:
    """A GOLD key (its content is never drawn). name adds a GOLD mono name to its right. .key .name"""
    bow = Circle(radius=h * 0.42, stroke_color=color, stroke_width=3).set_fill(color, 0.3)
    hole = Circle(radius=h * 0.12, stroke_color=color, stroke_width=2).set_fill(S.BG, 1).move_to(bow)
    a = bow.get_right()
    shaft = Line(a, a + RIGHT * h * 1.25, color=color, stroke_width=4)
    t1 = Line(a + RIGHT * h * 0.8, a + RIGHT * h * 0.8 + DOWN * h * 0.3, color=color, stroke_width=4)
    t2 = Line(a + RIGHT * h * 1.12, a + RIGHT * h * 1.12 + DOWN * h * 0.3, color=color, stroke_width=4)
    k = VGroup(bow, hole, shaft, t1, t2)
    if not name:
        k.key, k.name = k, None
        return _keep(k)
    n = mono(name, CAPTION, color).next_to(k, RIGHT, buff=0.14)
    g = VGroup(k, n)
    g.key, g.name = k, n
    return _keep(g)


def key_outline(h: float = 0.3, color: str = KEY) -> VGroup:
    """A dashed GOLD key outline: where your key would be."""
    k = key_glyph(h, color)
    out = VGroup(*[DashedVMobject(m, num_dashes=10, dashed_ratio=0.6).set_stroke(color, 2.5)
                   for m in (k[0], k[2], k[3], k[4])])
    return _keep(out)


def file_row(name: str, color: str = INK, glyph_color: str = S.GREY, size: float = CAPTION) -> VGroup:
    """A file (or folder, name ending in '/') glyph + its mono name. .glyph .text .fname"""
    g = folder_glyph(0.22, glyph_color) if name.endswith("/") else file_glyph(0.28, glyph_color)
    t = mono(name, size, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.fname = g, t, name
    return _keep(row)


def ghost_file(name: str, color: str = S.GREY) -> VGroup:
    """A dashed GREY file that doesn't exist (uv.lock, a missing systemInstruction …)."""
    g = DashedVMobject(file_glyph(0.28, color)[0], num_dashes=18).set_stroke(color, 2)
    t = mono(name, CAPTION, color).next_to(g, RIGHT, buff=0.12)
    row = VGroup(g, t)
    row.glyph, row.text, row.fname = g, t, name
    return _keep(row)


def model_box(name: str = "LLM", w: float = 1.3, h: float = 0.9, color: str = CLOUD,
              sub: str | None = None, size: float = CAPTION) -> VGroup:
    """A model box: BLUE rounded box, sans name ("\\n" splits rows), optional mono sub-label
    inside under it. .frame .title .sub"""
    nm = VGroup(*[sans(s, size, INK) for s in name.split("\n")]).arrange(DOWN, buff=0.06)
    sb = mono(sub, size, color).next_to(nm, DOWN, buff=0.1) if sub else None
    content = VGroup(nm, sb) if sb is not None else nm
    fr = box(max(w, content.width + 0.3), max(h, content.height + 0.24), color, fill_opacity=0.14,
             radius=0.12, stroke=3)
    content.move_to(fr)
    g = VGroup(fr, nm)
    g.sub = None
    if sb is not None:
        g.add(sb)
        g.sub = sb
    g.frame, g.title = fr, nm
    return g


def container_box(title: str, w: float = 3.0, h: float = 2.0, color: str = CTR,
                  size: float = CAPTION) -> VGroup:
    """A container: TEAL rounded box with its mono name at the top. .frame .title .body_top()"""
    fr = box(w, h, color, fill=S.BG, fill_opacity=1.0, radius=0.14, stroke=3)
    tint = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_width=0).set_fill(color, 0.06)
    t = mono(title, size, color).move_to(fr.get_top() + DOWN * 0.28)
    g = VGroup(fr, tint, t)
    g.frame, g.title = fr, t
    g.body_top = lambda: t.get_bottom()[1] - 0.12
    return g


def laptop_zone(w: float = 7.0, h: float = 3.8, caption: str | None = "your laptop",
                color: str = LAPTOP, size: float = CAPTION, corner=DOWN + LEFT) -> VGroup:
    """The GREY laptop as a zone (things inside it run on your machine); the caption sits in
    `corner` (DOWN + LEFT or DOWN + RIGHT). .frame .caption"""
    fr = box(w, h, color, fill_opacity=0.04, radius=0.2, stroke=2.5)
    g = VGroup(fr)
    g.frame, g.caption = fr, None
    if caption:
        c = label(caption, size, color).move_to(fr.get_corner(corner), aligned_edge=corner) \
            .shift(np.array([0.2 if corner[0] < 0 else -0.2, 0.12, 0]))
        g.add(c)
        g.caption = c
    return g


def cost_tick(r: float = 0.1, color: str = COST) -> VGroup:
    """A GOLD tick per paid call: a small coin."""
    c = Circle(radius=r, stroke_color=color, stroke_width=2.5).set_fill(color, 0.45)
    inner = Circle(radius=r * 0.55, stroke_color=color, stroke_width=1.5)
    return _keep(VGroup(c, inner))


def json_card(lines, color: str = OWN, size: float = CAPTION, header: str | None = None) -> VGroup:
    """A card of mono rows (masked, emoji stripped) in `color` (a BLUE tool request, a GREEN
    result, a GREEN capsule): .frame .rows .header"""
    rows = _mono_rows(lines, size, INK)
    fr = box(rows.width + 0.5, rows.height + 0.4, color, fill=S.BG, fill_opacity=0.95, radius=0.12, stroke=2.5)
    tint = RoundedRectangle(width=fr.width, height=fr.height, corner_radius=0.12, stroke_width=0) \
        .set_fill(color, 0.08).move_to(fr)
    rows.move_to(fr)
    g = VGroup(fr, tint, rows)
    g.frame, g.rows, g.header = fr, rows, None
    if header:
        h = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        g.add(h)
        g.header = h
    return g


def _save_op(m, attr: str = "_hop"):
    """Remember the fill/stroke opacity of every member of m ("_hop" for hide/reveal, "_dop"
    for dim/undim)."""
    for f in m.get_family():
        if isinstance(f, VMobject):
            setattr(f, attr, (f.get_fill_opacity(), f.get_stroke_opacity()))


def _set_op(m, k: float | None = None, attr: str = "_hop"):
    """Opacity of every member: k * saved (k=None: back to the saved opacities)."""
    for f in m.get_family():
        op = getattr(f, attr, None)
        if isinstance(f, VMobject) and op is not None:
            a = 1.0 if k is None else k
            f.set_fill(opacity=op[0] * a, family=False)
            f.set_stroke(opacity=op[1] * a, family=False)


def _drop_groups(scene, anims):
    """Remove the wrapper group an AnimationGroup / LaggedStart adds to the scene."""
    for a in anims:
        if isinstance(a, AnimationGroup) and a.group in scene.mobjects:
            scene.remove(a.group)


def _ref(point) -> Dot:
    """An invisible reference point (geometry that follows moves and rescales)."""
    return Dot(point, radius=0.01).set_fill(opacity=0).set_stroke(width=0, opacity=0)


class Piece(VGroup):
    """A set piece: a VGroup with named parts (self.parts) and helpers that keep the scene clean.

    A part that is not shown yet is a member at opacity 0, so it moves and scales with the piece
    and the piece's size never jumps; parts_in() / reveal() fade it in, parts_out() / hide() fade it
    back to 0. Never FadeOut a part (a FadeOut removes it from the scene and splits the piece);
    never set_opacity on the whole piece (it would show hidden parts): use dim_to()/undim()."""

    def __init__(self, **kw):
        super().__init__(**kw)
        self.parts: dict[str, object] = {}

    # -- parts
    def part(self, name: str, mob, shown: bool = True, into=None):
        """Register and add a named part (invisible until shown when shown=False)."""
        self.parts[name] = mob
        if not shown:
            _save_op(mob)
            _set_op(mob, 0)
        mob.hidden = not shown
        (into if into is not None else self).add(mob)
        return mob

    def _show_set(self, show, names):
        """show=None -> every name; a tuple -> those names."""
        return set(names) if show is None else set(show)

    def parts_in(self, *names, anim=None) -> list:
        """Animations that fade in (or anim(mob): Create, Write, GrowArrow …) the named hidden
        parts. Use inside self.play(*piece.parts_in("a", "b"))."""
        out = []
        for n in names:
            m = self.parts[n]
            if getattr(m, "hidden", False):
                _set_op(m)
            self._flag(m, False)
            out.append((anim or FadeIn)(m))
        return out

    def parts_out(self, *names) -> list:
        """Animations that fade the named parts to opacity 0 (they stay members)."""
        out = []
        for n in names:
            m = self.parts[n]
            if getattr(m, "hidden", False):
                continue
            _save_op(m)
            out.append(m.animate.set_opacity(0))
            self._flag(m, True)
        return out

    def reveal(self, scene, *names, run_time: float = 0.6, anim=None, extra=()):
        """parts_in() with its own play. Returns the part (or a list of them)."""
        self._ensure(scene)
        scene.play(*self.parts_in(*names, anim=anim), *extra, run_time=run_time)
        mobs = [self.parts[n] for n in names]
        return mobs[0] if len(mobs) == 1 else mobs

    def hide(self, scene, *names, run_time: float = 0.4, extra=()):
        anims = self.parts_out(*names) + list(extra)
        if anims:
            scene.play(*anims, run_time=run_time)

    def is_shown(self, name: str) -> bool:
        return not getattr(self.parts[name], "hidden", False)

    def _flag(self, m, hidden: bool):
        fam = set(m.get_family())
        for p in self.parts.values():
            if p is m or p in fam:
                p.hidden = hidden

    def dim_to(self, k: float = 0.3) -> Transform:
        """Animation: everything shown fades to k of its opacity (hidden parts stay hidden)."""
        _save_op(self, "_dop")
        target = self.copy()
        _set_op(target, k, "_dop")
        return Transform(self, target)

    def undim(self) -> Transform:
        target = self.copy()
        _set_op(target, None, "_dop")
        return Transform(self, target)

    # -- adding and removing mobjects
    def _ensure(self, scene):
        if self not in scene.get_mobject_family_members():
            scene.add(self)

    def _unparent(self, m):
        for f in self.get_family():
            if m in f.submobjects:
                f.remove(m)

    def attach(self, scene, *mobs, anims=None, run_time: float = 0.5, extra=(), into=None):
        """Play `anims` (default: FadeIn of each mob), then make the mobs members of this piece
        (or of `into`), so moving the piece moves them. Returns the first mob (or a list)."""
        anims = list(anims) if anims is not None else [FadeIn(m) for m in mobs]
        scene.play(*anims, *extra, run_time=run_time)
        _drop_groups(scene, anims)
        fam = set(self.get_family())
        for m in mobs:
            if m in scene.mobjects:
                scene.remove(m)
            if m not in fam:
                (into if into is not None else self).add(m)
        self._ensure(scene)
        return mobs[0] if len(mobs) == 1 else list(mobs)

    def detach(self, scene, *mobs, anims=None, run_time: float = 0.5, extra=()):
        """Take the mobs out of the piece and play `anims` (default: FadeOut of each)."""
        for m in mobs:
            self._unparent(m)
        scene.add(*mobs)
        scene.play(*(list(anims) if anims is not None else [FadeOut(m) for m in mobs]), *extra,
                   run_time=run_time)
        fam = scene.get_mobject_family_members()
        for m in mobs:
            if m in fam:
                scene.remove(m)

    def rescale(self, k: float, about_point=None):
        """Scale every shape by k but keep every text (and every chip, tag, labelled glyph) at
        its own size, so text stays >= 20 pt. Use via self.play(piece.animate.rescale(k))."""
        units: list = []

        def walk(m):
            if getattr(m, "keep_size", False) or isinstance(m, Text) or hasattr(m, "pt"):
                units.append(m)
                return
            for s in m.submobjects:
                walk(s)

        for s in self.submobjects:
            walk(s)
        self.scale(k, about_point=self.get_center() if about_point is None else about_point)
        for u in units:
            u.scale(1 / k)
        return self

    def glyph_only(self) -> VGroup:
        """A copy without any text (a thumbnail: shapes, colours; scale freely)."""
        c = self.copy()

        def strip(m):
            for s in list(m.submobjects):
                if isinstance(s, Text) or hasattr(s, "pt") or isinstance(s, DecimalNumber):
                    m.remove(s)
                else:
                    strip(s)
        strip(c)
        return c


def _restroke(mobs, color, width=None) -> list:
    """Animations recolouring the strokes of `mobs` (lighting a box)."""
    out = []
    for m in mobs:
        out.append(m.animate.set_stroke(color, width) if width else m.animate.set_stroke(color))
    return out


def _arrow(a, b, color: str = S.GREY, stroke: float = 3, buff: float = 0.06) -> Arrow:
    return Arrow(a, b, buff=buff, color=color, stroke_width=stroke, max_tip_length_to_length_ratio=0.3,
                 tip_length=0.16)


class _Reveal(FadeIn):
    """FadeIn of a member kept at opacity 0 (Piece.part(shown=False), or staged): its saved
    opacities come back when the animation BEGINS, not when it is built (a reveal built early and
    played later must not show the member in between)."""

    def __init__(self, mob, attr: str = "_hop", **kw):
        self._attr = attr
        super().__init__(mob, **kw)

    def begin(self) -> None:
        _set_op(self.mobject, attr=self._attr)
        super().begin()


def _stage_hidden(parent, mob, attr: str = "_swop"):
    """Add `mob` to `parent` at opacity 0 (its opacities saved under `attr`) for a _Reveal."""
    parent.add(mob)
    _save_op(mob, attr)
    _set_op(mob, 0, attr)
    return mob


def _rich(s: str, size: float = CAPTION, color: str = INK) -> Text:
    """Serif text with `code` spans in mono (backticks dropped); masks GREY."""
    return _md_text(s, size, color)


def fit_rows(text: str, width: float, size: float = CAPTION, color: str = INK, buff: float = 0.08,
             align=LEFT) -> VGroup:
    """`text` as rows that fit `width`: it breaks at " · " first (the separator stays at a row's
    end), then at spaces; a lone word wider than `width` raises. Rows are serif with `code` mono.
    Returns a VGroup of rows (arranged, aligned)."""
    segs = text.split(" · ")
    rows: list[str] = []
    cur = ""
    for k, seg in enumerate(segs):
        piece = seg + (" ·" if k < len(segs) - 1 else "")
        trial = f"{cur} {piece}" if cur else piece
        if cur and _rich(trial, size).width > width:
            rows.append(cur)
            cur = piece
        else:
            cur = trial
    rows.append(cur)
    out: list[str] = []
    for r in rows:                                   # a segment still too wide: break at spaces
        if _rich(r, size).width <= width:
            out.append(r)
            continue
        line = ""
        for w in r.split(" "):
            t = f"{line} {w}" if line else w
            if line and _rich(t, size).width > width:
                out.append(line)
                line = w
            else:
                line = t
        out.append(line)
    g = VGroup(*[_rich(r, size, color) for r in out]).arrange(DOWN, aligned_edge=align, buff=buff)
    if g.width > width + 0.01:
        raise ValueError(f"fit_rows: {text!r} does not fit {width:.2f} at {size} pt")
    g.row_texts = out
    return g


def x_mark(h: float = 0.3) -> VGroup:
    """The RED ✗ on a wrong physics claim."""
    return _keep(cross_mark(h, ERR))


def tick_mark(h: float = 0.3) -> VMobject:
    """The GREEN tick on the voice (S01)."""
    return _keep(check_mark(h, OWN))


def answer_card(rows: list[str], color: str = CLOUD, title: str | None = None, width: float = 5.6,
                size: float = CAPTION, dashed: bool = False) -> VGroup:
    """An answer card (S01, S15: what a model wrote): rows of serif text (`code` mono, the persona
    GREY) in a box of `color` (BLUE: a model wrote it); rows longer than the box are broken at spaces
    (fit_rows). title: a GREY line above ("base Qwen3-0.6B"). .frame .rows .title"""
    body = VGroup(*[fit_rows(unname(r), width - 0.5, size) for r in rows]).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.14)
    fr = box(width, body.height + 0.45, color, fill=S.BG, fill_opacity=0.95, radius=0.14, dashed=dashed)
    tint = RoundedRectangle(width=width, height=fr.height, corner_radius=0.14, stroke_width=0) \
        .set_fill(color, 0.07).move_to(fr)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
    g = VGroup(tint, fr, body)
    g.frame, g.rows, g.title = fr, body, None
    if title:
        t = note(title).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        g.add(t)
        g.title = t
    return g


def question_card(text: str, size: float = 26, color: str = INK) -> VGroup:
    """A question card (S01's "Why is the sky blue?"): GREY frame, larger serif text. .frame .text"""
    t = label(text, size, color)
    fr = box(t.width + 0.7, t.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.16)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def card_glyph(title: str, sub: str | None = None, color: str = S.GREY, w: float = 3.2,
               size: float = CAPTION, dashed: bool = False) -> VGroup:
    """A small card: serif title, optional GREY mono sub-line ("cli.py · lines 36–145"). .frame
    .title .sub"""
    t = label(title, size, INK)
    parts = [t]
    s = None
    if sub:
        s = _header_text(sub, size)
        parts.append(s)
    body = VGroup(*parts).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    fr = box(max(w, body.width + 0.4), body.height + 0.36, color, fill=S.BG, fill_opacity=0.95,
             radius=0.12, dashed=dashed)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
    g = VGroup(fr, body)
    g.frame, g.title, g.sub = fr, t, s
    return g



# ================================================================== L14: opacity helpers
def _op_to(m, k: float | None, attr: str = "_hop") -> Transform:
    """Animation: every member of m to k x its saved opacity (k=None: back to the saved values).
    m's opacities must have been saved under `attr` (_save_op) while it was fully shown."""
    target = m.copy()
    _set_op(target, k, attr)
    return Transform(m, target)


def dim(m, k: float = 0.2) -> Transform:
    """Animation: m (any group, a set piece, a panel) fades to k of its own opacities (a ponder card
    is up: everything else <= 20 %). Undo with undim(m). Never set_opacity on a group: it would
    flatten faint fills and show hidden members."""
    if isinstance(m, Piece):
        return m.dim_to(k)
    _save_op(m, "_dop")
    return _op_to(m, k, "_dop")


def undim(m) -> Transform:
    """Animation: back to the opacities dim(m) saved."""
    if isinstance(m, Piece):
        return m.undim()
    return _op_to(m, None, "_dop")


def _hidden(m):
    """Save m's opacities (as shown) and set it to 0: a member that appears later (_late, _Reveal,
    _op_to(m, None))."""
    _save_op(m)
    _set_op(m, 0)
    return m


class _Late(AnimationGroup):
    """Run `anim` on the hidden member `mob`, restoring its saved opacities only when this animation
    BEGINS (inside a Succession, a later step stays invisible until its turn)."""

    def __init__(self, mob, anim, attr: str = "_hop", **kw):
        self._late_mob, self._late_attr = mob, attr
        super().__init__(anim, **kw)

    def begin(self) -> None:
        _set_op(self._late_mob, attr=self._late_attr)
        super().begin()


def _fade_to(m, k: float = 0.0, attr: str = "_hop", **kw) -> UpdateFromAlphaFunc:
    """Opacity-only fade of m (and its family) from its current opacities to k x those, computed
    as it runs: a move or stretch played before it in a Succession stays. The opacities are saved
    under `attr` now (as shown), so a later _appear(m) / piece.parts_in() brings them back."""
    _save_op(m, attr)
    return UpdateFromAlphaFunc(m, lambda mob, a: _set_op(mob, 1 + (k - 1) * a, attr), **kw)


def _appear(m, attr: str = "_hop", **kw) -> UpdateFromAlphaFunc:
    """Opacity-only fade-in of a member hidden with _hidden(m) / part(shown=False): 0 -> its saved
    opacities, as it runs (safe anywhere in a Succession; no geometry snapshot)."""
    return UpdateFromAlphaFunc(m, lambda mob, a: _set_op(mob, a, attr), **kw)


def late_in(piece, *names, anim=None) -> list:
    """Like piece.parts_in(...), but each hidden part's opacity comes back when its animation
    begins: safe as a later step of a Succession. anim(mob): Create, GrowArrow, … (default FadeIn)."""
    out = []
    for n in names:
        m = piece.parts[n]
        piece._flag(m, False)
        out.append(_Late(m, (anim or FadeIn)(m)))
    return out


# ================================================================== L14: small glyphs
def instance_box(w: float = 1.2, h: float = 0.7, color: str = CLOUD, inner: bool = True,
                 inner_color: str = CTR) -> VGroup:
    """A serverless instance: a DASHED BLUE outline (it exists only while called) with a faint
    fill and, by default, a small TEAL container inside. .frame .fill .inner (None)"""
    fill = RoundedRectangle(width=w, height=h, corner_radius=min(0.12, h / 3), stroke_width=0) \
        .set_fill(color, 0.1)
    fr = box(w, h, color, dashed=True, radius=min(0.12, h / 3), stroke=3)
    g = VGroup(fill, fr)
    g.frame, g.fill, g.inner = fr, fill, None
    if inner:
        ib = RoundedRectangle(width=w * 0.5, height=h * 0.45, corner_radius=0.05, stroke_color=inner_color,
                              stroke_width=2).set_fill(inner_color, 0.25)
        g.add(ib)
        g.inner = ib
    return g


def vm_rack(h: float = 1.0, color: str = CLOUD) -> VGroup:
    """A VM: a SOLID BLUE rack (always there, booted or idle)."""
    return server(height=h, units=3, color=color)


def ear_glyph(h: float = 0.34, color: str = CLOUD) -> VGroup:
    """The "listening" ear: an outer arc and a small inner curl."""
    outer = Arc(radius=h * 0.5, start_angle=-0.35 * PI, angle=1.45 * PI, stroke_color=color, stroke_width=3)
    inner = Arc(radius=h * 0.22, start_angle=0.1 * PI, angle=1.1 * PI, stroke_color=color, stroke_width=2.5) \
        .shift(UP * h * 0.06)
    lobe = Line(outer.get_end(), outer.get_end() + DOWN * h * 0.22 + RIGHT * h * 0.1, color=color, stroke_width=3)
    return _keep(VGroup(outer, inner, lobe))


def ear_chip(text: str = f"listening on :{PORT}", color: str = CLOUD) -> VGroup:
    """Ear + a 20 pt caption ("listening on :8080"). .ear .text"""
    e = ear_glyph(color=color)
    t = label(text, CAPTION, color).next_to(e, RIGHT, buff=0.12)
    g = VGroup(e, t)
    g.ear, g.text = e, t
    return _keep(g)


def gear(r: float = 0.3, teeth: int = 8, color: str = OWN, fill: float = 0.25) -> VGroup:
    """A preprocessing gear (no text). .body .hole"""
    pts = []
    for k in range(teeth * 4):
        a = TAU * k / (teeth * 4)
        rr = r if (k % 4) in (1, 2) else r * 0.78
        pts.append([rr * np.cos(a), rr * np.sin(a), 0])
    body = Polygon(*pts, stroke_color=color, stroke_width=2.5).set_fill(color, fill)
    hole = Circle(radius=r * 0.28, stroke_color=color, stroke_width=2).set_fill(S.BG, 1)
    g = VGroup(body, hole)
    g.body, g.hole = body, hole
    return _keep(g)


def puff(r: float = 0.2, color: str = S.GREY) -> VGroup:
    """A small GREY puff (a cold start): three overlapping circles, no text."""
    cs = [Circle(radius=r * k, stroke_color=color, stroke_width=2).set_fill(color, 0.35).shift(np.array(d) * r)
          for k, d in ((0.6, (-0.55, -0.1, 0)), (0.75, (0.1, 0.2, 0)), (0.55, (0.65, -0.12, 0)))]
    return _keep(VGroup(*cs))


def bucket_glyph(h: float = 0.5, color: str = CLOUD) -> VGroup:
    """A storage bucket: a trapezoid with a rim."""
    w = h * 1.1
    body = Polygon([-w / 2, h / 2, 0], [w / 2, h / 2, 0], [w * 0.38, -h / 2, 0], [-w * 0.38, -h / 2, 0],
                   stroke_color=color, stroke_width=2.5).set_fill(color, 0.2)
    rim = Line([-w / 2 - 0.04, h / 2, 0], [w / 2 + 0.04, h / 2, 0], color=color, stroke_width=4)
    return _keep(VGroup(body, rim))


def phone_glyph(h: float = 0.9, color: str = CLIENT) -> VGroup:
    """A phone (the phone-app client): a tall rounded slab with a screen."""
    w = h * 0.52
    body = RoundedRectangle(width=w, height=h, corner_radius=w * 0.18, stroke_color=color,
                            stroke_width=3).set_fill(PANEL, 1)
    screen = RoundedRectangle(width=w * 0.76, height=h * 0.7, corner_radius=0.04, stroke_width=0) \
        .set_fill(color, 0.25)
    btn = Dot(body.get_bottom() + UP * h * 0.08, radius=h * 0.035, color=color)
    return _keep(VGroup(body, screen, btn))


def webpage_glyph(w: float = 1.2, color: str = CLIENT) -> VGroup:
    """A web page (the web client): a small browser frame with a bar and three text lines."""
    h = w * 0.72
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=3) \
        .set_fill(PANEL, 1)
    bar = Line(fr.get_corner(UP + LEFT) + DOWN * h * 0.22, fr.get_corner(UP + RIGHT) + DOWN * h * 0.22,
               color=color, stroke_width=2)
    lines = VGroup(*[Line(LEFT * w * 0.32, RIGHT * w * (0.32 - 0.12 * k), color=color, stroke_width=2)
                     for k in range(3)]).arrange(DOWN, buff=h * 0.12, aligned_edge=LEFT)
    lines.move_to(fr).shift(DOWN * h * 0.1)
    return _keep(VGroup(fr, bar, lines))


def token_glyph(r: float = 0.13, color: str = IDENTITY) -> VGroup:
    """A short-lived token the platform hands the badge: a small hexagon coin (no text)."""
    hexa = Polygon(*[[r * np.cos(a), r * np.sin(a), 0] for a in np.linspace(0, TAU, 7)[:-1]],
                   stroke_color=color, stroke_width=2.5).set_fill(color, 0.45)
    return _keep(VGroup(hexa, Dot(radius=r * 0.25, color=S.BG)))


def no_key(h: float = 0.32) -> VGroup:
    """The absent key: a dashed GOLD key outline, crossed out (GOLD). .key .cross"""
    k = key_outline(h)
    c = Line(k.get_corner(DOWN + LEFT) + np.array([-0.06, -0.06, 0]),
             k.get_corner(UP + RIGHT) + np.array([0.06, 0.06, 0]), color=COST, stroke_width=4)
    g = VGroup(k, c)
    g.key, g.cross = k, c
    return _keep(g)


def url_chip(text: str, size: float = CAPTION, color: str = ROUTE) -> VGroup:
    """A PINK mono chip: a URL, a query string, a gs:// path, a request body. .box .text"""
    return _keep(chip(text, color, size=size, font=MONO))


def entry_tag(name: str = ENTRY, color: str = OWN) -> VGroup:
    """V3's name tag "entry point: hello_http": a GREEN luggage tag (serif "entry point:" + mono name).
    .frame .name .hole; entry_tag("main") for the mismatch."""
    a = label("entry point:", CAPTION + 2, INK)
    b = mono(name, CAPTION + 2, color)
    row = VGroup(a, b).arrange(RIGHT, buff=0.14)
    h = row.height + 0.3
    w = row.width + 0.75
    pts = [[-w / 2, 0, 0], [-w / 2 + 0.3, h / 2, 0], [w / 2, h / 2, 0], [w / 2, -h / 2, 0], [-w / 2 + 0.3, -h / 2, 0]]
    fr = Polygon(*pts, stroke_color=color, stroke_width=2.5).set_fill(color, 0.12)
    hole = Circle(radius=0.06, stroke_color=color, stroke_width=2).move_to([-w / 2 + 0.28, 0, 0])
    row.move_to(fr).shift(RIGHT * 0.15)
    g = VGroup(fr, hole, row)
    g.frame, g.name, g.hole, g.row = fr, b, hole, row
    return _keep(g)


def badge(name: str = RUNTIME_SA, color: str = IDENTITY, size: float = CAPTION) -> VGroup:
    """A service-account badge: a BLUE card with a clip and a small person, the account name in
    mono. .frame .name .clip"""
    who = person_icon(color, height=0.32)
    t = mono(name, size, INK)
    row = VGroup(who, t).arrange(RIGHT, buff=0.15)
    fr = RoundedRectangle(width=row.width + 0.4, height=row.height + 0.3, corner_radius=0.1,
                          stroke_color=color, stroke_width=3).set_fill(S.BG, 0.95)
    tint = fr.copy().set_stroke(width=0).set_fill(color, 0.12)
    row.move_to(fr)
    clip = RoundedRectangle(width=0.32, height=0.12, corner_radius=0.05, stroke_color=color,
                            stroke_width=2).set_fill(color, 0.5).next_to(fr, UP, buff=-0.06)
    g = VGroup(fr, tint, row, clip)
    g.frame, g.name, g.clip = fr, t, clip
    return _keep(g)


def role_chip(text: str, color: str = IDENTITY) -> VGroup:
    """A role on a badge ("Agent Platform User"; PINK for bucket roles)."""
    return _keep(chip(text, color, size=CAPTION))


def log_window(title: str, w: float = 2.6, color: str = S.GREY) -> VGroup:
    """A schematic log window: title bar with the title (20 pt), three GREY log lines. .frame
    .title .lines; .light(colour) -> anims"""
    t = label(title, CAPTION, INK)
    w = max(w, t.width + 0.4)
    h = 1.2
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.1, stroke_color=color, stroke_width=2.5) \
        .set_fill(TERM_BG, 1)
    t.move_to(fr.get_top() + DOWN * 0.24)
    sep = Line(fr.get_corner(UP + LEFT) + DOWN * 0.46, fr.get_corner(UP + RIGHT) + DOWN * 0.46, color=color,
               stroke_width=1.5)
    lines = VGroup(*[Line(LEFT * (w / 2 - 0.25), RIGHT * (w / 2 - 0.25 - 0.4 * k), color=S.GREY_DARK,
                          stroke_width=3) for k in range(3)]).arrange(DOWN, buff=0.13, aligned_edge=LEFT)
    lines.next_to(sep, DOWN, buff=0.14).align_to(fr, LEFT).shift(RIGHT * 0.25)
    g = VGroup(fr, sep, t, lines)
    g.frame, g.title, g.lines = fr, t, lines

    def light(c=TURN):
        return [fr.animate.set_stroke(c, 3.5), t.animate.set_color(c), lines.animate.set_stroke(c)]
    g.light = light
    return g


def image_glyph(side: float = 0.6, text: str | None = "224×224×3", color: str = OWN) -> VGroup:
    """A preprocessed image: three stacked squares (R, G, B planes) and an optional 20 pt label
    under them. .stack .label"""
    sq = VGroup(*[Rectangle(width=side, height=side, stroke_color=c, stroke_width=2.5).set_fill(c, 0.15)
                  .shift(np.array([0.09 * k, 0.09 * k, 0])) for k, c in enumerate((S.RED, S.GREEN, S.BLUE))])
    g = VGroup(sq)
    g.stack, g.label = sq, None
    if text:
        t = mono(text, CAPTION, color).next_to(sq, DOWN, buff=0.12)
        g.add(t)
        g.label = t
    return _keep(g)


class ProbBars(VGroup):
    """The four class probabilities: one row per label (20 pt serif) with a bar. Built empty.
    .rise(values, hi=index) -> anims (bars grow; the hi row YELLOW); .bars .labels"""

    def __init__(self, labels=CHEESES, bar_w: float = 1.2, color: str = CLOUD, **kw):
        super().__init__(**kw)
        self.bar_w, self.hi_color = bar_w, color
        self.labels = VGroup(*[label(s, CAPTION, INK) for s in labels]).arrange(DOWN, buff=0.12, aligned_edge=RIGHT)
        x0 = self.labels.get_right()[0] + 0.15
        self.bars = VGroup()
        self.tracks = VGroup()
        for t in self.labels:
            tr = Rectangle(width=bar_w, height=0.2, stroke_color=S.GREY_DARK, stroke_width=1.5) \
                .set_fill(opacity=0).move_to([x0 + bar_w / 2, t.get_center()[1], 0])
            b = Rectangle(width=0.01, height=0.2, stroke_width=0).set_fill(color, 0.8)
            b.move_to([x0 + 0.005, t.get_center()[1], 0])
            self.tracks.add(tr)
            self.bars.add(b)
        self.x0 = x0
        self.add(self.labels, self.tracks, self.bars)

    def rise(self, values=(0.08, 0.12, 0.7, 0.1), hi: int | None = 2) -> list:
        out = []
        for k, (b, v) in enumerate(zip(self.bars, values)):
            col = TURN if k == hi else self.hi_color
            x0 = self.tracks[k].get_left()[0]          # (the bars follow the group when it moves)
            out.append(b.animate.stretch_to_fit_width(max(0.01, v * self.bar_w))
                       .move_to([x0 + max(0.01, v * self.bar_w) / 2, b.get_center()[1], 0])
                       .set_fill(col, 0.85))
        if hi is not None:
            out.append(self.labels[hi].animate.set_fill(TURN, opacity=1))
        return out


class Clock(VGroup):
    """A clock face with one hand (one turn per minute) and, with counter=True, a "0 min" readout
    to its right (20 pt+). .run_to(minutes, run_time) -> anims (hand + readout); .freeze() before it
    leaves (clears the readout's updater). .face .hand .num"""

    def __init__(self, r: float = 0.32, color: str = S.GREY, counter: bool = True, caption: str | None = None,
                 **kw):
        super().__init__(**kw)
        self.face = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
        ticks = VGroup(*[Line(UP * r * 0.78, UP * r * 0.95, color=color, stroke_width=2)
                         .rotate(-k * TAU / 12, about_point=ORIGIN) for k in range(12)])
        self.hand = Line(ORIGIN, UP * r * 0.72, color=INK, stroke_width=3.5)
        self.add(self.face, ticks, self.hand, Dot(radius=0.04, color=INK))
        self.minutes = 0.0
        self.tracker, self.num, self.caption = None, None, None
        if counter:
            self.tracker = ValueTracker(0)
            self.num = DecimalNumber(0, num_decimal_places=0, font_size=26, color=INK)
            unit = label("min", CAPTION + 2, S.GREY)
            row = VGroup(self.num, unit).arrange(RIGHT, buff=0.1, aligned_edge=DOWN).next_to(self.face, RIGHT,
                                                                                            buff=0.18)
            self.num.add_updater(lambda m: m.set_value(self.tracker.get_value()))
            self.unit = unit
            self.add(row)
        if caption:
            self.caption = label(caption, CAPTION, color).next_to(self.face, DOWN, buff=0.12)
            self.add(self.caption)
        _keep(self)

    def run_to(self, minutes: float, run_time: float = 2.0) -> list:
        turns = minutes - self.minutes
        self.minutes = minutes
        out = [Rotate(self.hand, angle=-TAU * turns, about_point=self.face.get_center(), rate_func=linear,
                      run_time=run_time)]
        if self.tracker is not None:
            out.append(self.tracker.animate(rate_func=linear, run_time=run_time).set_value(minutes))
        return out

    def freeze(self):
        if self.num is not None:
            self.num.clear_updaters()
        return self


def scheduler_clock(caption: str = "Cloud Scheduler") -> Clock:
    """The BLUE Cloud Scheduler clock (no logo), caption under it. .run_to(…) turns its hand."""
    return Clock(r=0.36, color=CLOUD, counter=False, caption=caption)


def execute_button(text: str = "Execute") -> VGroup:
    """The schematic GREY console button (tag it illustration_tag()). .press() -> anim"""
    t = sans(text, CAPTION + 2, INK)
    b = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.3, corner_radius=0.08,
                         stroke_color=CLIENT, stroke_width=2.5).set_fill(CLIENT, 0.25)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    g.press = lambda: Succession(b.animate(run_time=0.15).set_fill(TURN, 0.45),
                                 b.animate(run_time=0.3).set_fill(CLIENT, 0.25))
    return _keep(g)


class Slider(VGroup):
    """A GOLD slider "minimum instances" with values under the track (0, 1). .to(v) -> anim (the
    knob moves; the value under it lights). .track .knob .ticks"""

    def __init__(self, text: str = "minimum instances", values=(0, 1), w: float = 1.6, color: str = COST, **kw):
        super().__init__(**kw)
        self.values = list(values)
        self.caption = label(text, CAPTION, color)
        self.track = Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=4)
        self.track.next_to(self.caption, RIGHT, buff=0.3)
        self.ticks = VGroup()
        for k, v in enumerate(self.values):
            x = self.track.get_left()[0] + w * k / max(1, len(self.values) - 1)
            self.ticks.add(mono(str(v), CAPTION, S.GREY).move_to([x, self.track.get_y() - 0.3, 0]))
        self.knob = Circle(radius=0.12, stroke_color=color, stroke_width=3).set_fill(color, 0.9) \
            .move_to(self.track.get_left())
        self.ticks[0].set_color(color)
        self.add(self.caption, self.track, self.ticks, self.knob)
        _keep(self)

    def to(self, v, run_time: float = 0.8) -> AnimationGroup:
        k = self.values.index(v)
        x = self.ticks[k].get_x()
        return AnimationGroup(self.knob.animate.move_to([x, self.track.get_y(), 0]),
                              *[t.animate.set_color(COST if j == k else S.GREY) for j, t in enumerate(self.ticks)],
                              run_time=run_time)


class VersionDial(VGroup):
    """The endpoint's version dial: a knob with "v1" / "v2" marks (20 pt). .set(v) -> anims (needle
    turns; the mark lights YELLOW, RED with bad=True). .face .needle .marks"""

    def __init__(self, versions=("v1", "v2"), r: float = 0.3, color: str = CLOUD, **kw):
        super().__init__(**kw)
        self.face = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
        self.angles = {v: a for v, a in zip(versions, np.linspace(0.6, -0.6, len(versions)))}
        self.needle = Line(ORIGIN, UP * r * 0.8, color=INK, stroke_width=4).rotate(self.angles[versions[0]],
                                                                                 about_point=ORIGIN)
        self.marks = VGroup()
        for v, a in self.angles.items():
            d = np.array([-np.sin(a), np.cos(a), 0])
            self.marks.add(mono(v, CAPTION, S.GREY).move_to(d * (r + 0.28)))
        self.marks[0].set_color(TURN)
        self.cur = versions[0]
        self.add(self.face, self.needle, Dot(radius=0.04, color=INK), self.marks)
        _keep(self)

    def set(self, v: str, bad: bool = False, run_time: float = 0.7) -> list:
        da = self.angles[v] - self.angles[self.cur]
        self.cur = v
        out = [Rotate(self.needle, angle=da, about_point=self.face.get_center(), run_time=run_time)]
        for (name, _), m in zip(self.angles.items(), self.marks):
            out.append(m.animate.set_color((ERR if bad else TURN) if name == v else S.GREY))
        return out


def door(h: float = 1.0, color: str = CLOUD) -> VGroup:
    """A door in a wall: a frame and a leaf with a knob. .leaf .frame; .open_() / .close_() -> anims"""
    w = h * 0.5
    fr = Rectangle(width=w, height=h, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    leaf = Rectangle(width=w * 0.86, height=h * 0.92, stroke_color=color, stroke_width=2).set_fill(color, 0.25)
    leaf.move_to(fr).align_to(fr, DOWN)
    knob = Dot(radius=0.04, color=color).move_to(leaf.get_right() + LEFT * w * 0.15)
    lf = VGroup(leaf, knob)
    g = VGroup(fr, lf)
    g.frame, g.leaf = fr, lf
    g.open_ = lambda: lf.animate.stretch(0.2, 0, about_edge=LEFT)
    g.close_ = lambda: lf.animate.stretch(5.0, 0, about_edge=LEFT)
    return g


def plug(text: str, color: str = OWN, letter: str | None = None) -> VGroup:
    """V6's plug: a body with the registered function's mono name (20 pt+) and two prongs at the
    right; an optional option-letter badge on its left (YELLOW circle). .body .name .prongs .tip
    (the prongs' end point) .badge"""
    t = mono(text, CAPTION + 2, INK)
    body = RoundedRectangle(width=t.width + 0.5, height=0.62, corner_radius=0.12, stroke_color=color,
                            stroke_width=3).set_fill(color, 0.15)
    t.move_to(body)
    prongs = VGroup(*[Rectangle(width=0.34, height=0.08, stroke_width=0).set_fill(color, 1)
                      .next_to(body, RIGHT, buff=0).shift(UP * dy) for dy in (0.13, -0.13)])
    g = VGroup(body, t, prongs)
    g.body, g.name, g.prongs, g.badge = body, t, prongs, None
    if letter:
        b = step_badge(letter, TURN).next_to(body, LEFT, buff=0.12)
        g.add(b)
        g.badge = b
    g.tip = lambda: prongs.get_right()
    return _keep(g)


def socket(text: str = "serving_default", color: str = OWN) -> VGroup:
    """V6's export socket: a recessed square with two slots, its mono label above (20 pt+).
    .frame .slots .label .mouth() (the point a plug's tip goes to)"""
    fr = RoundedRectangle(width=0.62, height=0.9, corner_radius=0.08, stroke_color=color, stroke_width=3) \
        .set_fill(S.BG, 1)
    slots = VGroup(*[Rectangle(width=0.2, height=0.08, stroke_width=0).set_fill(color, 0.9)
                     .move_to(fr.get_left() + RIGHT * 0.16 + UP * dy) for dy in (0.13, -0.13)])
    t = mono(text, CAPTION + 2, color).next_to(fr, UP, buff=0.14)
    g = VGroup(fr, slots, t)
    g.frame, g.slots, g.label = fr, slots, t
    g.mouth = lambda: fr.get_left()
    return g


# ================================================================== exam map (S01 builds it, S02-S08 reuse it)
EXAM_SLOTS = ("service or job", "who pays for idle", "what you hand over", "who calls, who it runs as",
              "the model endpoint")


def icon_strips(h: float = 0.36) -> VGroup:
    """Slot icon 1 (V1): a service bar with a request tick over a job bar with an end edge."""
    a = Rectangle(width=h * 1.6, height=h * 0.3, stroke_color=CLOUD, stroke_width=2).set_fill(CLOUD, 0.25)
    tick = Line(UP * h * 0.3, ORIGIN, color=TURN, stroke_width=3).next_to(a, UP, buff=0.02)
    b = Rectangle(width=h * 1.1, height=h * 0.3, stroke_width=0).set_fill(CTR, 0.6)
    b.next_to(a, DOWN, buff=h * 0.18).align_to(a, LEFT)
    edge = Line(UP * h * 0.2, DOWN * h * 0.2, color=OWN, stroke_width=3).next_to(b, RIGHT, buff=0)
    return _keep(VGroup(a, tick, b, edge))


def icon_meters(h: float = 0.36) -> VGroup:
    """Slot icon 2 (V2): two GOLD meter bars, one full, one short."""
    g = VGroup()
    for k, f in enumerate((0.9, 0.35)):
        tr = Rectangle(width=h * 1.6, height=h * 0.32, stroke_color=COST, stroke_width=2).set_fill(opacity=0)
        fl = Rectangle(width=h * 1.6 * f, height=h * 0.32, stroke_width=0).set_fill(COST, 0.7) \
            .align_to(tr, LEFT)
        g.add(VGroup(tr, fl).shift(DOWN * k * h * 0.55))
    return _keep(g)


def icon_grid(h: float = 0.36) -> VGroup:
    """Slot icon 3 (V3): a 2x2 grid, the bottom row YELLOW."""
    s = h * 0.48
    cells = VGroup(*[Square(s, CLOUD if r == 0 else TURN) for r in range(2) for _ in range(2)])
    cells.arrange_in_grid(2, 2, buff=0.04)
    return _keep(cells)


def Square(s: float, color: str):  # noqa: N802  (a tiny filled square; not manim's Square)
    return Rectangle(width=s, height=s, stroke_color=color, stroke_width=2).set_fill(color, 0.25)


def icon_doors(h: float = 0.36) -> VGroup:
    """Slot icon 4 (V4): a box with a door on each side."""
    b = Rectangle(width=h * 1.4, height=h, stroke_color=CLOUD, stroke_width=2).set_fill(CLOUD, 0.12)
    d1 = Rectangle(width=h * 0.22, height=h * 0.55, stroke_width=0).set_fill(ROUTE, 0.8) \
        .move_to(b.get_left()).align_to(b, DOWN)
    d2 = d1.copy().set_fill(CLOUD, 0.9).move_to(b.get_right()).align_to(b, DOWN)
    return _keep(VGroup(b, d1, d2))


def icon_gear_plug(h: float = 0.36) -> VGroup:
    """Slot icon 5 (V5 + V6): a gear and a plug."""
    gr = gear(h * 0.45)
    p = Rectangle(width=h * 0.6, height=h * 0.4, stroke_color=OWN, stroke_width=2).set_fill(OWN, 0.2)
    pr = VGroup(*[Rectangle(width=h * 0.25, height=h * 0.07, stroke_width=0).set_fill(OWN, 1)
                  .next_to(p, RIGHT, buff=0).shift(UP * dy * h) for dy in (0.1, -0.1)])
    return _keep(VGroup(gr, VGroup(p, pr)).arrange(RIGHT, buff=0.08))


def icon_gear(h: float = 0.36) -> VGroup:
    """Recap icon 6 (V5's single gear inside a BLUE endpoint box)."""
    b = Rectangle(width=h * 1.3, height=h, stroke_color=CLOUD, stroke_width=2).set_fill(CLOUD, 0.12)
    return _keep(VGroup(b, gear(h * 0.38).move_to(b)))


def icon_plug(h: float = 0.36) -> VGroup:
    """Recap icon 7 (V6's plug in a socket)."""
    p = icon_gear_plug(h)[1]
    s = Rectangle(width=h * 0.3, height=h * 0.7, stroke_color=OWN, stroke_width=2).set_fill(S.BG, 1)
    s.next_to(p, RIGHT, buff=0.0)
    return _keep(VGroup(p, s))


def icon_puff(h: float = 0.36) -> VGroup:
    """Recap icon 3 (a cold-start puff before a dashed instance)."""
    inst = instance_box(h * 1.1, h * 0.75, inner=False)
    return _keep(VGroup(puff(h * 0.35), inst).arrange(RIGHT, buff=0.05))


SLOT_ICONS = (icon_strips, icon_meters, icon_grid, icon_doors, icon_gear_plug)
RECAP_ICONS = (icon_strips, icon_meters, icon_puff, icon_grid, icon_doors, icon_gear, icon_plug)


def recap_icon(k: int, h: float = 0.42) -> VGroup:
    """S08: the icon of rule k (1..7): strips, meters, puff, grid, doors, gear, plug."""
    return RECAP_ICONS[k - 1](h)


class ExamMap(VGroup):
    """The exam map in the top strip (x -6.6..3.2, centre y MAP_Y = 3.3): five GREY-outlined slots
    1..5 (EXAM_SLOTS), each a number and an icon (no label). Rebuild it in every scene with what
    earlier scenes filled: ExamMap(filled=(1, 2), half=(5,)).

        m = ExamMap(filled=(1,))           # S03 starts with slot 1 done
        self.play(FadeIn(m))               # or self.play(m.write_in()) (S01: slots one by one)
        self.play(*m.activate(2))          # others dim to 35 %; slot 2 YELLOW + its label under it
        self.play(m.pulse(2))
        rule.shrink_into(self, m, 2)       # (RuleCard) plays the card into the slot, then m.fill(2)
        self.play(*m.fill(5, frac=0.5))    # S06: half-filled (the gear); frac=1 adds the GREEN tick

    .slots[i-1] (VGroup: .frame .num .icon), .caption (the active slot's label, or None).
    Methods return animations. The slot index is 1-based everywhere."""

    def __init__(self, filled=(), half=(), dim: float = 0.35, **kw):
        super().__init__(**kw)
        n = len(EXAM_SLOTS)
        gap = 0.16
        w = (MAP_RIGHT - MAP_LEFT - gap * (n - 1)) / n
        self.dim_k, self.active, self.caption = dim, None, None
        self.slots = []
        for i in range(n):
            fr = RoundedRectangle(width=w, height=0.56, corner_radius=0.1, stroke_color=S.GREY,
                                  stroke_width=2).set_fill(S.BG, 0.9)
            num = S.text(str(i + 1), CAPTION + 2, INK, font=SANS, weight="BOLD")
            ic = SLOT_ICONS[i]()
            row = VGroup(num, ic).arrange(RIGHT, buff=0.22).move_to(fr)
            fill = RoundedRectangle(width=w, height=0.56, corner_radius=0.1, stroke_width=0).set_fill(OWN, 0.22)
            fill.stretch(0.001, 0, about_edge=LEFT).move_to(fr, aligned_edge=LEFT)
            tick = _keep(check_mark(0.22, OWN)).move_to(fr.get_corner(UP + RIGHT) + np.array([-0.2, -0.17, 0]))
            s = VGroup(fill, fr, row, tick)
            s.frame, s.num, s.icon, s.fillbar, s.tick, s.frac = fr, num, ic, fill, tick, 0.0
            s.move_to([MAP_LEFT + w / 2 + i * (w + gap), MAP_Y, 0])
            tick.set_stroke(opacity=0)
            self.slots.append(s)
            self.add(s)
        for i in filled:
            self._set_fill(i, 1.0)
        for i in half:
            self._set_fill(i, 0.5)
        for s in self.slots:
            _save_op(s, "_mop")
        guard(self.get_left()[0] >= -SAFE_X - 1e-6 and self.get_right()[0] <= MAP_RIGHT + 1e-6, "exam map span")

    def _set_fill(self, i: int, frac: float):
        s = self.slots[i - 1]
        w = s.frame.width * frac
        s.fillbar.stretch_to_fit_width(max(0.001, w)).move_to(s.frame, aligned_edge=LEFT)
        s.frac = frac
        if frac >= 1:
            s.frame.set_stroke(OWN)
            s.tick.set_stroke(opacity=1)

    def write_in(self, lag: float = 0.25, run_time: float = 2.0) -> LaggedStart:
        """S01: the five slots write in left to right (the whole map at once: use slot_in(i) to
        time each slot to its words)."""
        return LaggedStart(*[FadeIn(s, shift=DOWN * 0.15) for s in self.slots], lag_ratio=lag, run_time=run_time)

    def slot_in(self, i: int) -> FadeIn:
        """One slot writes in (the map must not be on screen yet as a whole: add slots one by one)."""
        return FadeIn(self.slots[i - 1], shift=DOWN * 0.15)

    def label_of(self, i: int, color: str = TURN) -> Text:
        """The slot's label ("1 · service or job"), 20 pt, centred under the slot, kept in x <= 3.2."""
        t = label(f"{i} · {EXAM_SLOTS[i - 1]}", CAPTION, color)
        s = self.slots[i - 1]
        t.next_to(s, DOWN, buff=0.12)
        x = min(max(t.get_center()[0], MAP_LEFT + t.width / 2), MAP_RIGHT - t.width / 2)
        t.set_x(x)
        return t

    def activate(self, i: int) -> list:
        """Slot i bright with a YELLOW outline and its label under it; the other slots at `dim`
        (35 %). The label replaces the previous one."""
        out = []
        for k, s in enumerate(self.slots, start=1):
            tgt = s.copy()
            _set_op(tgt, None if k == i else self.dim_k, "_mop")
            tgt.frame.set_stroke(TURN if k == i else (OWN if s.frac >= 1 else S.GREY), 3 if k == i else 2)
            out.append(Transform(s, tgt))
        new = self.label_of(i)
        if self.caption is not None:
            old = self.caption
            out += _swap_text(self, old, new)
        else:
            self.add(new)
            _save_op(new, "_swop")
            _set_op(new, 0, "_swop")
            out.append(_SwapIn(new))
        self.caption, self.active = new, i
        return out

    def deactivate(self) -> list:
        """All slots back to full opacity, outlines GREY (GREEN when filled), the label gone (it
        stays a member at opacity 0)."""
        out = []
        for s in self.slots:
            tgt = s.copy()
            _set_op(tgt, None, "_mop")
            tgt.frame.set_stroke(OWN if s.frac >= 1 else S.GREY, 2)
            out.append(Transform(s, tgt))
        if self.caption is not None:
            out.append(_fade_to(self.caption, 0.0, "_cop"))
            self.caption = None
        self.active = None
        return out

    def pulse(self, i: int) -> Indicate:
        return Indicate(self.slots[i - 1].frame, color=TURN, scale_factor=1.08)

    def fill(self, i: int, frac: float = 1.0) -> list:
        """Slot i fills GREEN to frac (0.5: half, the S06 gear); frac 1 adds the GREEN tick and a
        GREEN outline."""
        s = self.slots[i - 1]
        w = max(0.001, s.frame.width * frac)
        target = s.fillbar.copy().stretch_to_fit_width(w).move_to(s.frame, aligned_edge=LEFT)
        out = [Transform(s.fillbar, target)]
        s.frac = frac
        if frac >= 1:
            out.append(s.frame.animate.set_stroke(OWN, 2.5))
            out.append(s.tick.animate.set_stroke(opacity=1))
            s.tick._mop = (0.0, 1.0)
            s.fillbar._mop = (0.22, 0.0)
        return out

    def slot_frame(self, i: int):
        """The slot's frame (where a RuleCard shrinks to)."""
        return self.slots[i - 1].frame


exam_map = ExamMap


class RuleCard(VGroup):
    """The scene's exam-rule card (script.md "RULE"): a GREEN-outlined card in the bottom third, the
    GREEN title "exam rule", the rule's two lines (`top`, `bottom`; serif 22 pt, `code` in
    backticks mono, broken to fit). Bottom edge at y (default -3.45).

        rule = RuleCard("runs, writes output, exits · 'every night' → job (+ Cloud Scheduler)",
                        "answers requests · URL · port → service")
        self.play(*rule.write_in())                # frame + title, then both lines
        # or: self.play(rule.frame_in()); self.play(rule.line_in(0)); ...; self.play(rule.line_in(1))
        rule.shrink_into(self, exam_map, 1)        # plays: text out, the frame flies into slot 1,
                                                   # then the slot fills (frac=1 by default)
    .frame .title .rows (two VGroups of rows)"""

    def __init__(self, top: str, bottom: str, width: float = 12.4, size: float = 22, y: float = -3.45, **kw):
        super().__init__(**kw)
        ttl = sans("exam rule", CAPTION, OWN, weight="BOLD")
        r0 = fit_rows(top, width - 0.8, size)
        r1 = fit_rows(bottom, width - 0.8, size)
        body = VGroup(r0, r1).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        h = ttl.height + body.height + 0.75
        fr = RoundedRectangle(width=width, height=h, corner_radius=0.16, stroke_color=OWN, stroke_width=3) \
            .set_fill(S.BG, 0.96)
        ttl.move_to(fr.get_corner(UP + LEFT) + np.array([0.4 + ttl.width / 2, -0.22 - ttl.height / 2, 0]))
        body.next_to(ttl, DOWN, buff=0.18, aligned_edge=LEFT)
        self.frame, self.title, self.rows = fr, ttl, VGroup(r0, r1)
        self.add(fr, ttl, self.rows)
        self.move_to([0, y + h / 2, 0])
        guard(self.get_bottom()[1] >= -SAFE_Y - 0.01 and self.width <= 2 * SAFE_X + 0.01,
              f"rule card out of frame (bottom {self.get_bottom()[1]:.2f}, width {self.width:.2f})")

    def frame_in(self) -> AnimationGroup:
        return AnimationGroup(FadeIn(self.frame), FadeIn(self.title))

    def line_in(self, k: int) -> FadeIn:
        return FadeIn(self.rows[k], shift=RIGHT * 0.15)

    def write_in(self) -> list:
        return [Succession(self.frame_in(), self.line_in(0), self.line_in(1), run_time=1.6)]

    def shrink_into(self, scene, emap: ExamMap, i: int, frac: float = 1.0, run_time: float = 1.0):
        """Plays: the text fades (first 40 %), the frame flies into slot i and takes its shape, then
        the card leaves the scene and the slot fills GREEN (emap.fill(i, frac))."""
        tgt = emap.slot_frame(i).copy().set_stroke(OWN, 3).set_fill(OWN, 0.22)
        scene.play(FadeOut(VGroup(self.title, self.rows), rate_func=_out_early),
                   Transform(self.frame, tgt), run_time=run_time)
        scene.remove(self)
        scene.play(*emap.fill(i, frac), run_time=0.4)


rule_card = RuleCard


# ================================================================== multiple-choice ponder (P1-P3)
class MCQCard(VGroup):
    """The multiple-choice ponder card (script.md "PONDER"): YELLOW outline, header "Pause and
    ponder", the question (serif 24 pt, broken to fit; question=None leaves it out), four options
    A-D (a YELLOW letter badge + serif 22 pt), a reserved slot of `reason_rows` rows under each
    option for its reason (so the card never changes size), a YELLOW timer bar at the bottom.
    Width 12.4 by default (compact: width=5.8, question=None, reason_rows=2 for S07's docked card).

        card = mcq_ponder(self, Q, OPTS, seconds=10, dim=[piece])   # plays in + the timer
        self.play(*card.right(1, "finite work · runs to completion"))   # B: YELLOW row, ✓, GREEN note
        self.play(*card.wrong(0, "pays for an always-on instance …"))   # A: RED ✗ + RED reason
        self.play(FadeOut(card), *[undim(m) for m in dimmed])

    .frame .header .question .rows[k] (VGroup badge, text) .badges .bar; .reason_at(k) (left point)"""

    def __init__(self, question: str | None, options, width: float = 12.4, size: float = 22,
                 q_size: float = 24, reason_rows: int = 1, header: str = "Pause and ponder", **kw):
        super().__init__(**kw)
        self.width_, self.size, self.reason_rows = width, size, reason_rows
        hd = S.text(header, CAPTION + 2, TURN, weight="BOLD")
        parts = [hd]
        q = None
        if question:
            q = fit_rows(question, width - 0.8, q_size)
            parts.append(q)
        self.rows, self.badges, self.slots = VGroup(), VGroup(), []
        self.text_w = width - 1.5
        rpitch = _rich("Ag", CAPTION).height + 0.08
        opts = VGroup()
        for k, o in enumerate(options):
            b = step_badge("ABCD"[k], TURN)
            t = fit_rows(o, self.text_w, size)
            row = VGroup(b, t).arrange(RIGHT, buff=0.25, aligned_edge=UP)
            b.align_to(t, UP).shift(UP * 0.04)
            slot = Rectangle(width=self.text_w, height=rpitch * reason_rows, stroke_width=0, fill_opacity=0)
            slot.next_to(t, DOWN, buff=0.08, aligned_edge=LEFT)
            grp = VGroup(row, slot)
            self.rows.add(row)
            self.badges.add(b)
            self.slots.append(slot)
            opts.add(grp)
        opts.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        parts.append(opts)
        body = VGroup(*parts).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        fr = RoundedRectangle(width=width, height=body.height + 0.75, corner_radius=0.2, stroke_color=TURN,
                              stroke_width=3).set_fill(S.BG, 1)
        body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.4 + UP * 0.1)
        bar = Line(fr.get_corner(DOWN + LEFT) + RIGHT * 0.3 + UP * 0.2,
                   fr.get_corner(DOWN + RIGHT) + LEFT * 0.3 + UP * 0.2, color=TURN, stroke_width=4)
        self.frame, self.header, self.question, self.bar, self.opts = fr, hd, q, bar, opts
        self.add(fr, body, bar)
        self.marks = VGroup()
        self.add(self.marks)

    def reason_at(self, k: int):
        return self.slots[k].get_corner(UP + LEFT)

    def run_timer(self, scene, seconds: float = 10.0):
        """Plays: the timer bar drains over `seconds` (nothing else moves: a ponder pause)."""
        bar = self.bar
        scene.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                   run_time=seconds)

    def _note(self, k: int, text: str, color: str) -> VGroup:
        rows = fit_rows(text, self.text_w, CAPTION, color)
        guard(len(rows) <= self.reason_rows,
              f"option {'ABCD'[k]} reason {text!r} needs {len(rows)} rows (reserved {self.reason_rows})")
        rows.move_to(self.reason_at(k), aligned_edge=UP + LEFT)
        return rows

    def right(self, k: int, note_: str | None = None) -> list:
        """Option k (0-based) is right: its row gets a YELLOW fill, a GREEN ✓ at the frame's right,
        and the GREEN note in its reason slot."""
        row = self.rows[k]
        hl = RoundedRectangle(width=self.width_ - 0.4, height=row.height + 0.14, corner_radius=0.08,
                              stroke_color=TURN, stroke_width=2).set_fill(TURN, 0.16)
        hl.move_to([self.frame.get_center()[0], row.get_center()[1], 0])
        tk = _keep(check_mark(0.3, OWN)).move_to([self.frame.get_right()[0] - 0.5, row.get_center()[1], 0])
        mobs = [hl, tk]
        if note_:
            mobs.append(self._note(k, note_, OWN))
        self.marks.add(*mobs)
        self.rows[k][0][0].set_fill(TURN, 0.3)
        return [FadeIn(m) for m in mobs]

    def wrong(self, k: int, reason: str | None = None) -> list:
        """Option k is wrong: a RED ✗ at the frame's right and the RED reason in its slot."""
        row = self.rows[k]
        x = _keep(cross_mark(0.26, ERR)).move_to([self.frame.get_right()[0] - 0.5, row.get_center()[1], 0])
        mobs = [x]
        if reason:
            mobs.append(self._note(k, reason, ERR))
        self.marks.add(*mobs)
        return [FadeIn(m, shift=RIGHT * 0.1) for m in mobs]


def mcq_ponder(scene, question: str | None, options, seconds: float = 10.0, bottom: float = -3.55,
               dim=(), hide=(), **kw) -> MCQCard:
    """Plays the multiple-choice ponder: everything in `dim` fades to 20 % (dim()), `hide` fades
    out, the card fades in with its bottom at `bottom`, then its timer drains over `seconds`.
    Returns the card (on screen). Undo with undim(m) for m in dim. kw go to MCQCard."""
    card = MCQCard(question, options, **kw)
    card.move_to([0, bottom + card.frame.height / 2, 0])
    guard(card.get_top()[1] <= 2.58, f"ponder card top {card.get_top()[1]:.2f} reaches the exam map's label")
    scene.play(FadeIn(card, scale=0.97), *[dim(m) for m in dim], *[FadeOut(m) for m in hide], run_time=0.6)
    card.run_timer(scene, seconds)
    return card


# ================================================================== V1 · lifecycle strips (S01, S02, S08)
class ImageBlock(VGroup):
    """V1's TEAL image block: the image name (mono 20 pt; name=None: "image") and one GREEN command
    tag per startup command hanging under it (serve, batch). .frame .name .cmds[cmd] (the tag)
    .anchor(cmd) (the tag's bottom: where its strip starts)."""

    def __init__(self, name: str | None = IMAGE, commands=("serve", "batch"), w: float | None = None,
                 gap: float = 2.6, **kw):
        super().__init__(**kw)
        t = mono(name or "image", CAPTION, INK)
        fw = max(w or 0, t.width + 0.5)
        fr = RoundedRectangle(width=fw, height=0.62, corner_radius=0.1, stroke_color=CTR, stroke_width=3) \
            .set_fill(CTR, 0.15)
        t.move_to(fr)
        self.frame, self.name = fr, t
        self.add(fr, t)
        self.cmds = {}
        n = len(commands)
        for k, c in enumerate(commands):
            tg = _keep(chip(c, OWN, size=CAPTION + 2, font=MONO))
            x = (k - (n - 1) / 2) * gap
            tg.move_to([x, fr.get_bottom()[1] - 0.55, 0])
            wire = Line([x, fr.get_bottom()[1], 0], tg.get_top(), color=OWN, stroke_width=2)
            self.cmds[c] = tg
            self.add(wire, tg)

    def anchor(self, cmd: str):
        return self.cmds[cmd].get_bottom()


class ServiceStrip(Piece):
    """V1 service strip (S02): time runs left to right along a GREY axis (`width` wide, "time"
    after its end); a dashed BLUE instance bar appears when the first request arrives, grows with
    time, answers every PINK request arrow (from above; lane 1's from below) with a short YELLOW
    return arrow, a second bar splits off in a burst (max 2), and both dissolve when traffic stops
    (scale to zero). Built centred at ORIGIN: width + 0.8 wide, 3.3 tall (y -1.75..1.6).
    t is a fraction of the time span (0..1).

        sv = ServiceStrip(10.0)
        self.play(FadeIn(sv))                        # axis, "time", url chip
        self.play(*sv.start(0.05))                   # bar 0 + ear + "listening on :8080" (under the axis)
        self.play(*sv.request(0.12))                 # one request and its answer
        self.play(*sv.grow(0.4), *sv.request(0.3))
        self.play(*sv.split(0.45))                   # bar 1 + GREY chip "max instances 2"
        self.play(*sv.stop(0.8))                     # bars end and dissolve; chip "scale to zero"
    Parts: axis, time, url, ear, max_chip, zero_chip, bar0, bar1. Every method returns animations
    (play them at once: new members are added to the piece when the method is called)."""

    LANE_Y = (0.3, -0.3)
    BAR_H = 0.4

    def __init__(self, width: float = 10.0, url: str | None = "https://…run.app", **kw):
        super().__init__(**kw)
        self.W, self.x0 = width, -width / 2
        ax_y = -1.0
        self.part("axis", Arrow([self.x0, ax_y, 0], [self.x0 + width + 0.15, ax_y, 0], buff=0, color=S.GREY,
                                stroke_width=2.5, tip_length=0.16, max_tip_length_to_length_ratio=0.05))
        self.part("time", label("time", CAPTION, S.GREY).next_to(self.parts["axis"], RIGHT, buff=0.12))
        if url:
            self.part("url", url_chip(url).move_to([self.x0, 1.42, 0], aligned_edge=LEFT))
        self.part("ear", ear_chip().move_to([self.x0, ax_y - 0.42, 0], aligned_edge=LEFT), shown=False)
        self.part("max_chip", _keep(chip("max instances 2", S.GREY, size=CAPTION))
                  .move_to([self.x0 + width, ax_y - 0.42, 0], aligned_edge=RIGHT), shown=False)
        self.part("zero_chip", _keep(chip("scale to zero", CLOUD, size=CAPTION))
                  .move_to([self.x0 + width * 0.55, ax_y - 0.42, 0]), shown=False)
        self.ref = _ref(ORIGIN)            # follows the piece when it moves
        self.add(self.ref)
        self.bars = [None, None]
        self.t0 = [0.0, 0.0]
        self.arrows = VGroup()
        self.add(self.arrows)

    def x(self, t: float) -> float:
        """Screen x of time t (follows the piece)."""
        return self.ref.get_center()[0] + self.x0 + t * self.W

    def lane_y(self, lane: int) -> float:
        return self.ref.get_center()[1] + self.LANE_Y[lane]

    def start(self, t: float, lane: int = 0) -> list:
        """An instance bar appears on `lane` at time t (lane 0 also gets the ear and its caption)."""
        b = instance_box(0.3, self.BAR_H, inner=False)
        b.move_to([self.x(t), self.lane_y(lane), 0], aligned_edge=LEFT)
        self.bars[lane], self.t0[lane] = b, t
        self.part(f"bar{lane}", b)
        out = [FadeIn(b, scale=0.6)]
        if lane == 0 and not self.is_shown("ear"):
            mark = ear_glyph().next_to(b, LEFT, buff=0.06)
            self.part("ear_mark", mark)
            out += self.parts_in("ear") + [FadeIn(mark)]
        return out

    def grow(self, t: float, lanes=(0, 1)) -> list:
        """The live bars extend to time t."""
        out = []
        for lane in lanes:
            b = self.bars[lane]
            if b is None or getattr(b, "ended", False):
                continue
            w = max(0.3, (t - self.t0[lane]) * self.W)
            tgt = instance_box(w, self.BAR_H, inner=False).move_to(b.get_left(), aligned_edge=LEFT)
            out.append(Transform(b, tgt))           # rebuilt, not stretched (the dashes keep their size)
        return out

    def request(self, t: float, lane: int = 0) -> list:
        """A PINK request arrow onto bar `lane` at time t, then a YELLOW return arrow beside it
        (both stay as the traffic's trace; stop() fades them to 35 %)."""
        b = self.bars[lane]
        x = self.x(t)
        if lane == 0:
            top = b.get_top()[1]
            a = Arrow([x, top + 0.62, 0], [x, top + 0.02, 0], buff=0, color=ROUTE, stroke_width=3, tip_length=0.14)
            r = Arrow([x + 0.13, top + 0.02, 0], [x + 0.13, top + 0.5, 0], buff=0, color=TURN, stroke_width=3,
                      tip_length=0.12)
        else:
            bot = b.get_bottom()[1]
            a = Arrow([x, bot - 0.5, 0], [x, bot - 0.02, 0], buff=0, color=ROUTE, stroke_width=3, tip_length=0.14)
            r = Arrow([x + 0.13, bot - 0.02, 0], [x + 0.13, bot - 0.42, 0], buff=0, color=TURN, stroke_width=3,
                      tip_length=0.12)
        _hidden(r)
        self.arrows.add(a, r)
        return [Succession(Create(a, run_time=0.35), _Reveal(r, run_time=0.3))]

    def split(self, t: float) -> list:
        out = self.start(t, 1)
        return out + self.parts_in("max_chip")

    def stop(self, t: float) -> list:
        """The bars grow to t, then dissolve (to opacity 0: they stay members), the ear mark goes,
        the arrows fade to 35 %, and "scale to zero" appears under the axis at t."""
        grow = self.grow(t)
        out = []
        steps = [AnimationGroup(*grow, run_time=0.6)] if grow else []
        fade = []
        for lane in (0, 1):
            b = self.bars[lane]
            if b is not None:
                b.ended = True
                fade.append(_fade_to(b, 0.0))
                self._flag(b, True)
        if "ear_mark" in self.parts:
            fade.append(_fade_to(self.parts["ear_mark"], 0.0))
            self._flag(self.parts["ear_mark"], True)
        fade.append(_fade_to(self.arrows, 0.35, "_aop"))
        zc = self.parts["zero_chip"]
        zc.set_x(min(self.x(t) + 0.3 + zc.width / 2, self.x(1.0) - zc.width / 2 - self.parts["max_chip"].width - 0.2))
        out.append(Succession(*steps, AnimationGroup(*fade, run_time=0.8), AnimationGroup(*late_in(self, "zero_chip"))))
        return out


class JobStrip(Piece):
    """V1 job strip (S02, S08): one TEAL block running through GREEN-labelled segments (JOB_STEPS:
    read, translate, speak, save; 20 pt), then a hard right edge "exit 0" (GREEN; code=1: RED
    "exit 1"). No ear, no URL. Built centred at ORIGIN: `width` wide, ~1.6 tall; each segment is
    seg_w wide (default 0.17 x width), the strip starts at x = -width/2.

        jb = JobStrip(10.0)
        self.play(FadeIn(jb))                 # the axis only (segments hidden)
        for i in range(4): self.play(*jb.run(i))
        self.play(*jb.finish())               # edge + "exit 0"
        JobStrip(10.0, steps=("read", "translate"), code=1)   # the short failed run
    .span() -> (x_left, x_right) of all segments (the EndlessStrip cuts into this). Parts: axis,
    seg0.., lab0.., edge, exit."""

    def __init__(self, width: float = 10.0, steps=JOB_STEPS, seg_w: float | None = None, code: int = 0,
                 axis: bool = True, **kw):
        super().__init__(**kw)
        self.W, self.x0 = width, -width / 2
        sw = seg_w or 0.17 * width
        self.seg_w, self.n = sw, len(steps)
        if axis:
            self.part("axis", Arrow([self.x0, -0.55, 0], [self.x0 + width + 0.15, -0.55, 0], buff=0,
                                    color=S.GREY, stroke_width=2.5, tip_length=0.16,
                                    max_tip_length_to_length_ratio=0.05))
        for i, s in enumerate(steps):
            r = Rectangle(width=sw, height=0.5, stroke_color=CTR, stroke_width=2).set_fill(CTR, 0.25)
            r.move_to([self.x0 + sw * (i + 0.5), 0, 0])
            lab = label(s, CAPTION, OWN).move_to(r)
            guard(lab.width <= sw - 0.1, f"job step {s!r} wider than its segment ({sw:.2f})")
            self.part(f"seg{i}", r, shown=False)
            self.part(f"lab{i}", lab, shown=False)
        xe = self.x0 + sw * self.n
        col = OWN if code == 0 else ERR
        self.part("edge", Line([xe, -0.42, 0], [xe, 0.42, 0], color=col, stroke_width=7), shown=False)
        self.part("exit", label(f"exit {code}", CAPTION + 2, col).next_to([xe, 0.42, 0], UP, buff=0.1),
                  shown=False)
        self.code = code

    def run(self, i: int, run_time: float = 0.6) -> list:
        """Segment i grows from its left edge and its label appears (safe inside a Succession)."""
        seg, lab = self.parts[f"seg{i}"], self.parts[f"lab{i}"]
        self._flag(seg, False)
        self._flag(lab, False)
        return [_Late(seg, GrowFromEdge(seg, LEFT), run_time=run_time), _appear(lab, run_time=run_time)]

    def run_all(self, run_time: float = 2.0) -> Succession:
        """All segments one after another, then the edge and "exit N"."""
        return Succession(*[AnimationGroup(*self.run(i, run_time / self.n)) for i in range(self.n)],
                          AnimationGroup(*late_in(self, "edge", "exit")))

    def finish(self) -> list:
        return self.parts_in("edge", "exit")

    def span(self):
        return self.parts["seg0"].get_left()[0], self.parts[f"seg{self.n - 1}"].get_right()[0]


class EndlessStrip(Piece):
    """V1's broken job (S01, S02): the image's default command `serve` started a server, so the
    TEAL bar grows and never reaches an edge; a GREY clock above its start counts minutes; at
    `wall_at` a RED wall "task timeout · 5 min" slams down and the bar's end turns RED with a RED
    chip "execution failed". Built centred at ORIGIN: width wide, ~2.4 tall (y -0.9..1.5).

        en = EndlessStrip(10.0)
        self.play(FadeIn(en))                       # the clock and the axis
        self.play(*en.grow_to(0.5, run_time=3))     # bar + clock ("2 min" at half the wall)
        self.play(*en.grow_to(en.wall_at, 3))
        self.play(*en.hit_wall())                   # wall + RED end + "execution failed"
        self.play(*en.cut_into(job))                # S02: bar -> the job's segment span; wall, chips out
    .clock (Clock: call en.clock.freeze() before it leaves). Parts: axis, clock, bar, wall,
    wall_label, fail."""

    def __init__(self, width: float = 10.0, wall_at: float = 0.86, minutes: float = 5.0, **kw):
        super().__init__(**kw)
        self.W, self.x0, self.wall_at, self.minutes = width, -width / 2, wall_at, minutes
        self.part("axis", Arrow([self.x0, -0.55, 0], [self.x0 + width + 0.15, -0.55, 0], buff=0, color=S.GREY,
                                stroke_width=2.5, tip_length=0.16, max_tip_length_to_length_ratio=0.05))
        self.clock = Clock(r=0.3)
        self.clock.move_to([self.x0 + 0.3, 0.95, 0], aligned_edge=LEFT)
        self.part("clock", self.clock)
        bar = Rectangle(width=0.05, height=0.5, stroke_color=CTR, stroke_width=2).set_fill(CTR, 0.3)
        bar.move_to([self.x0, 0, 0], aligned_edge=LEFT)
        self.part("bar", bar)
        xw = self.x0 + width * wall_at
        self.part("wall", Rectangle(width=0.16, height=1.5, stroke_width=0).set_fill(ERR, 0.9)
                  .move_to([xw + 0.08, 0.2, 0]), shown=False)
        self.part("wall_label", label("task timeout · 5 min", CAPTION, ERR)
                  .next_to([xw + 0.08, 0.95, 0], UP, buff=0.08).shift(LEFT * 0.4), shown=False)
        self.part("fail", _keep(chip("execution failed", ERR, size=CAPTION))
                  .move_to([xw - 1.1, -0.95, 0]), shown=False)
        self.t = 0.0

    def x(self, t: float) -> float:
        return self.parts["axis"].get_left()[0] + t * self.W

    def grow_to(self, t: float, run_time: float = 2.0) -> list:
        bar = self.parts["bar"]
        w = max(0.05, t * self.W)
        self.t = t
        return [bar.animate(rate_func=linear, run_time=run_time).stretch_to_fit_width(w).align_to(bar, LEFT),
                *self.clock.run_to(self.minutes * t / self.wall_at, run_time=run_time)]

    def hit_wall(self) -> list:
        bar = self.parts["bar"]
        return [*self.parts_in("wall", anim=lambda m: FadeIn(m, shift=DOWN * 0.6)), *self.parts_in("wall_label"),
                bar.animate.set_stroke(ERR, 3), *self.parts_in("fail")]

    def cut_into(self, job: JobStrip) -> list:
        """The bar becomes the job's segment span (same y as the job's segments); wall, labels and
        clock fade to 0 (members). Then reveal the job: self.play(*job.run(i)) / job.finish();
        afterwards fade this piece out."""
        a, b = job.span()
        y = job.parts["seg0"].get_center()[1]
        bar = self.parts["bar"]
        tgt = bar.copy().stretch_to_fit_width(b - a).move_to([(a + b) / 2, y, 0]).set_stroke(CTR, 2)
        hide = [n for n in ("wall", "wall_label", "fail", "clock") if self.is_shown(n)]
        return [Transform(bar, tgt), *self.parts_out(*hide)]


def LifecycleStrip(kind: str = "service", width: float = 10.0, **kw):  # noqa: N802
    """V1 factory (script.md's name): "service" -> ServiceStrip, "job" -> JobStrip, "endless" ->
    EndlessStrip."""
    return {"service": ServiceStrip, "job": JobStrip, "endless": EndlessStrip}[kind](width, **kw)


# ================================================================== V2 · two meters on one day (S03, S08)
class TwoMeters(Piece):
    """V2 (S03): a 24-hour axis with nine YELLOW request ticks in two clusters; the top row a SOLID
    BLUE VM rack whose GOLD meter fills at a constant rate (idle shading GOLD across the whole
    row), the bottom row a dashed function instance that blinks at each tick and whose GOLD meter
    steps up one block per invocation. Meters on the right (x 4.0..6.4). Built in place: x
    -6.5..6.4, y -2.4..2.0 (axis y -1.4, VM row y 1.25, function row y -0.45; slider at y -2.0).
    Do not move it (its methods use these coordinates).

        tm = TwoMeters()
        self.play(FadeIn(tm))                    # racks, empty meters, axis "0 h"/"24 h", ticks
        self.play(*tm.sweep(run_time=4))         # cursor sweeps (then fades); VM meter fills; idle shading
        self.play(tm.blink_all(run_time=3))      # instances blink, function meter steps up
        self.play(*tm.stretch())                 # transform 1: gaps widen (axis "36 h"); VM grows, "+0"
        self.play(*tm.cold_start())              # puff + delayed first tick of cluster 2 + RED "cold start"
        self.play(*tm.min_instances(1))          # GOLD slider 0 -> 1, always-on band + drip; puff goes
        self.play(*tm.lift_always_on())          # the band rises into the VM row; "always on" chip
        self.play(*tm.unstretch())               # back to one day (P2 reveal)
        self.play(*tm.double())                  # transform 2: every tick splits; function meter x2; "flat"
    .always_on_slot() -> a point under the lifted band (a card <= 0.5 tall fits) for S03's endpoint card. Parts: rack, inst_icon,
    axis, t0, t_end, ticks, vm_meter, fn_meter, vm_fill, idle, cursor, plus0, flat, puff, cold,
    slider, band, drip, always."""

    AX0, L0 = -4.6, 5.4
    VM_Y, FN_Y, AX_Y = 1.25, -0.45, -1.4
    HOURS = (8.0, 9.0, 9.5, 10.5, 11.0, 17.0, 18.0, 19.0, 20.0)
    METER_X, METER_W = 4.0, 2.4
    BLOCK = 0.11

    def __init__(self, **kw):
        super().__init__(**kw)
        self.stretched = False
        self.part("rack", vm_rack(0.8).move_to([-5.85, self.VM_Y, 0]))
        self.part("inst_icon", instance_box(0.85, 0.55).move_to([-5.85, self.FN_Y, 0]))
        self.part("axis", Line([self.AX0, self.AX_Y, 0], [self.AX0 + self.L0, self.AX_Y, 0], color=S.GREY,
                               stroke_width=2.5))
        self.part("t0", label("0 h", CAPTION, S.GREY).next_to([self.AX0, self.AX_Y, 0], DOWN, buff=0.15))
        self.part("t_end", label("24 h", CAPTION, S.GREY).next_to([self.AX0 + self.L0, self.AX_Y, 0], DOWN,
                                                                     buff=0.15))
        ticks = VGroup(*[Line([self.hx(h), self.AX_Y - 0.08, 0], [self.hx(h), self.FN_Y + 0.35, 0], color=TURN,
                              stroke_width=3) for h in self.HOURS])
        self.part("ticks", ticks)
        for name, y in (("vm_meter", self.VM_Y), ("fn_meter", self.FN_Y)):
            fr = Rectangle(width=self.METER_W, height=0.4, stroke_color=COST, stroke_width=2.5).set_fill(opacity=0)
            fr.move_to([self.METER_X + self.METER_W / 2, y, 0])
            self.part(name, fr)
        self.part("vm_fill", Rectangle(width=self.vm_level(), height=0.4, stroke_width=0).set_fill(COST, 0.75)
                  .move_to([self.METER_X, self.VM_Y, 0], aligned_edge=LEFT), shown=False)
        self.part("idle", Rectangle(width=self.L0, height=0.46, stroke_width=0).set_fill(COST, 0.2)
                  .move_to([self.AX0, self.VM_Y, 0], aligned_edge=LEFT), shown=False)
        self.part("idle_lab", label("idle · billed", CAPTION, COST)
                  .move_to([self.hx(14.0), self.VM_Y + 0.5, 0]), shown=False)
        self.part("vm_on", Line([self.AX0, self.VM_Y - 0.28, 0], [self.AX0 + self.L0, self.VM_Y - 0.28, 0],
                                color=CLOUD, stroke_width=4), shown=False)
        self.part("cursor", Line([self.AX0, self.AX_Y, 0], [self.AX0, self.VM_Y + 0.35, 0], color=TURN,
                                 stroke_width=2.5), shown=False)
        self.blinks = VGroup()
        self.blocks = VGroup()
        for k, h in enumerate(self.HOURS + self.HOURS):
            if k < len(self.HOURS):
                b = instance_box(0.36, 0.5, inner=False).move_to([self.hx(h), self.FN_Y, 0])
                self.blinks.add(_hidden(b))
            blk = Rectangle(width=self.BLOCK - 0.02, height=0.34, stroke_width=0).set_fill(COST, 0.75)
            blk.move_to([self.METER_X + 0.04 + self.BLOCK * k, self.FN_Y, 0], aligned_edge=LEFT)
            self.blocks.add(_hidden(blk))
        self.add(self.blinks, self.blocks)
        self.part("plus0", _keep(chip("+0", S.GREY, size=CAPTION))
                  .next_to(self.parts["fn_meter"], DOWN, buff=0.12), shown=False)
        self.part("flat", _keep(chip("flat", S.GREY, size=CAPTION))
                  .next_to(self.parts["vm_meter"], UP, buff=0.12), shown=False)
        self.part("puff", puff().move_to([self.hx(17.0) - 0.42, self.FN_Y + 0.05, 0]), shown=False)
        self.part("cold", _keep(chip("cold start", ERR, size=CAPTION))
                  .move_to([self.hx(17.0), self.FN_Y + 0.75, 0]), shown=False)
        self.part("slider", Slider().move_to([2.6, -2.25, 0]), shown=False)
        self.part("band", self._band(self.FN_Y - 0.36), shown=False)
        self.part("always", _keep(chip("always on", S.GREY, size=CAPTION))
                  .move_to([self.AX0 + 0.9, self.VM_Y - 0.45 - 0.42, 0]), shown=False)
        self.extra_ticks = VGroup()
        self.add(self.extra_ticks)
        guard(self.get_right()[0] <= SAFE_X and self.get_left()[0] >= -SAFE_X, "TwoMeters width")

    def _band(self, y: float) -> VGroup:
        bd = DashedLine([self.AX0, y, 0], [self.AX0 + self.L0, y, 0], color=CLOUD, stroke_width=3,
                        dash_length=0.12)
        drip = VGroup(*[cost_tick(0.06).move_to([x, y - 0.17, 0])
                        for x in np.arange(self.AX0 + 0.3, self.AX0 + self.L0, 0.6)])
        g = VGroup(bd, drip)
        g.line, g.drip = bd, drip
        return g

    def hx(self, h: float, stretched: bool | None = None) -> float:
        """x of hour h on the axis (stretched: the quiet gaps widened, the day 36 h)."""
        s = self.stretched if stretched is None else stretched
        if s:
            h = h + (6.0 if h > 12 else 0.0)
            return self.AX0 + self.L0 * h / 24.0
        return self.AX0 + self.L0 * h / 24.0

    def length(self) -> float:
        return self.L0 * (1.5 if self.stretched else 1.0)

    def vm_level(self) -> float:
        return 1.4 * self.length() / self.L0

    def sweep(self, run_time: float = 4.0) -> list:
        """The cursor sweeps the day; the VM meter fills linearly; the idle shading grows behind
        the cursor; "idle · billed" appears."""
        cur, fill, idle = self.parts["cursor"], self.parts["vm_fill"], self.parts["idle"]
        for m in (cur, fill, idle):
            _set_op(m)
            self._flag(m, False)
        return [cur.animate(rate_func=linear, run_time=run_time).shift(RIGHT * self.length()),
                GrowFromEdge(fill, LEFT, rate_func=linear, run_time=run_time),
                GrowFromEdge(idle, LEFT, rate_func=linear, run_time=run_time),
                Succession(Wait(run_time * 0.6), AnimationGroup(*late_in(self, "idle_lab", "vm_on"))),
                Succession(Wait(run_time), _fade_to(cur, 0.0, run_time=0.3))]

    def blink_all(self, run_time: float = 3.0) -> LaggedStart:
        """At each tick a dashed instance blinks on and off; the function meter gains one block."""
        steps = []
        for k, b in enumerate(self.blinks):
            steps.append(Succession(AnimationGroup(_op_to(b, None), _op_to(self.blocks[k], None), run_time=0.2),
                                    _op_to(b, 0, "_hop"), run_time=0.5))
        return LaggedStart(*steps, lag_ratio=0.6, run_time=run_time)

    def _moves(self, stretched: bool) -> list:
        old = self.stretched
        self.stretched = stretched
        out = []
        ax = self.parts["axis"]
        out.append(ax.animate.put_start_and_end_on(np.array([self.AX0, self.AX_Y, 0]),
                                                   np.array([self.AX0 + self.length(), self.AX_Y, 0])))
        new_lab = label("36 h" if stretched else "24 h", CAPTION, S.GREY) \
            .next_to([self.AX0 + self.length(), self.AX_Y, 0], DOWN, buff=0.15)
        out += _swap_text(self, self.parts["t_end"], new_lab)
        self.parts["t_end"] = new_lab
        for k, h in enumerate(self.HOURS):
            dx = self.hx(h) - self.hx(h, old)
            if dx:
                out.append(self.parts["ticks"][k].animate.shift(RIGHT * dx))
                self.blinks[k].shift(RIGHT * dx)
        for name in ("puff", "cold"):
            self.parts[name].shift(RIGHT * (self.hx(17.0) - self.hx(17.0, old)))
        k = self.length() / (self.L0 * (1.5 if old else 1.0))
        for name in ("idle", "vm_on"):
            m = self.parts[name]
            out.append(m.animate.stretch(k, 0, about_point=np.array([self.AX0, m.get_center()[1], 0])))
        out.append(self.parts["idle_lab"].animate.move_to([self.hx(14.0), self.VM_Y + 0.5, 0]))
        fill = self.parts["vm_fill"]
        out.append(fill.animate.stretch_to_fit_width(self.vm_level()).align_to(fill, LEFT))
        band = self.parts["band"]
        out.append(band.line.animate.stretch(k, 0, about_point=np.array([self.AX0, band.line.get_center()[1], 0])))
        for d in band.drip:
            out.append(d.animate.set_x(self.AX0 + (d.get_center()[0] - self.AX0) * k))
        return out

    def stretch(self) -> list:
        """Transform 1: the quiet gaps widen (cluster 2 moves right, the day reads "36 h"); the VM
        meter grows with the added idle; the function meter does not move ("+0" chip)."""
        return self._moves(True) + self.parts_in("plus0")

    def unstretch(self) -> list:
        """Back to one 24-hour day (the "+0" chip goes)."""
        return self._moves(False) + self.parts_out("plus0")

    def double(self) -> list:
        """Transform 2: every tick splits in two (18 ticks), the function meter climbs to 18 blocks,
        the VM meter stays where it is ("flat" chip)."""
        out = []
        for t in self.parts["ticks"]:
            twin = _hidden(t.copy().shift(RIGHT * 0.1))
            self.extra_ticks.add(twin)
            out.append(_Reveal(twin, shift=RIGHT * 0.1))
        out.append(LaggedStart(*[_op_to(b, None) for b in self.blocks[len(self.HOURS):]], lag_ratio=0.3,
                               run_time=1.5))
        out += self.parts_in("flat")
        return out

    def cold_start(self) -> list:
        """After the longest gap: a GREY puff before the first tick of cluster 2, that tick delayed
        (shifted right 0.15), RED chip "cold start" above."""
        tick = self.parts["ticks"][5]
        return [*self.parts_in("puff", "cold"), tick.animate.shift(RIGHT * 0.15)]

    def min_instances(self, v: int = 1) -> list:
        """The GOLD slider (bottom right) to v. v=1: an always-on dashed band with its GOLD drip
        along the function row; the puff and "cold start" go and the delayed tick returns. v=0:
        the band goes."""
        sl = self.parts["slider"]
        out = []
        if not self.is_shown("slider"):
            out.append(Succession(AnimationGroup(*self.parts_in("slider")), sl.to(v)))
        else:
            out.append(sl.to(v))
        tick = self.parts["ticks"][5]
        if v:
            out += self.parts_in("band")
            if self.is_shown("puff"):
                out += self.parts_out("puff", "cold")
                out.append(tick.animate.shift(LEFT * 0.15))
        else:
            out += self.parts_out("band")
        return out

    def lift_always_on(self) -> list:
        """The always-on band and its drip rise into the VM row (under the rack's line); GREY chip
        "always on" at its left."""
        band = self.parts["band"]
        return [band.animate.shift(UP * (self.VM_Y - 0.45 - band.line.get_center()[1])), *self.parts_in("always")]

    def always_on_slot(self):
        """A point in the VM row, right half, below the shading (for the endpoint card)."""
        return np.array([self.AX0 + self.length() * 0.62, self.VM_Y - 0.95, 0])


# ================================================================== V3 · what you hand over (S04)
class HandoverGrid(Piece):
    """V3 (S04): slide 10's four deployment options redrawn as a 2x2 grid: rows "virtual machine"
    (solid BLUE rack) / "serverless" (dashed BLUE instance; row labels on the grid's RIGHT), columns
    "a code file" (a page) / "a container" (TEAL box); a GREEN "Simple Translate App" code block on
    the left with four GREEN arrows to the cells (column 2's arrows run over the top / under the
    bottom). Built in place: ~12.0 wide, y -1.9..1.25 (centre y -0.35).

        hg = HandoverGrid()
        self.play(FadeIn(hg))                           # everything but ticks / lights
        self.play(*hg.tick(0, 0, "Lecture 1"), *hg.tick(0, 1, "Lecture 2"))
        self.play(*hg.light(1, 0), *hg.light(1, 1))     # today's two cells YELLOW
    .cell(r, c) -> the cell frame (r 0 = VM, 1 = serverless; c 0 = file, 1 = container).
    Parts: app, arrows, heads, cells, tick_r_c, chip_r_c."""

    CELL_W, CELL_H = 3.1, 1.2

    def __init__(self, app: bool = True, **kw):
        super().__init__(**kw)
        gx, gy = 0.0, -0.35          # grid centre (cells only)
        cw, ch = self.CELL_W, self.CELL_H
        self._cells = {}
        cells = VGroup()
        for r in range(2):
            for c in range(2):
                fr = RoundedRectangle(width=cw, height=ch, corner_radius=0.1, stroke_color=S.GREY,
                                      stroke_width=2).set_fill(S.BG, 0.9)
                fr.move_to([gx + (c - 0.5) * (cw + 0.12), gy - (r - 0.5) * (ch + 0.12), 0])
                host = vm_rack(0.55) if r == 0 else instance_box(0.75, 0.5, inner=False)
                what = file_glyph(0.42, OWN) if c == 0 else container_glyph(0.4)
                icon = VGroup(what, host).arrange(RIGHT, buff=0.2).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.22)
                self._cells[(r, c)] = fr
                cells.add(VGroup(fr, icon))
        self.part("cells", cells)
        heads = VGroup()
        for c, t in enumerate(("a code file", "a container")):
            heads.add(label(t, CAPTION + 2, INK).next_to(self._cells[(0, c)], UP, buff=0.14))
        for r, t in enumerate(("virtual machine", "serverless")):
            heads.add(label(t, CAPTION + 2, CLOUD).next_to(self._cells[(r, 1)], RIGHT, buff=0.25))
        self.part("heads", heads)
        if app:
            lines = ["# translate text", "# from a request", "# return the result"]
            body = VGroup(*[mono(s, CAPTION, OWN) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            ttl = label("Simple Translate App", CAPTION, INK)
            inner = VGroup(ttl, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            fr = RoundedRectangle(width=inner.width + 0.4, height=inner.height + 0.4, corner_radius=0.12,
                                  stroke_color=OWN, stroke_width=2.5).set_fill(OWN, 0.08)
            inner.move_to(fr)
            appg = VGroup(fr, inner)
            appg.move_to([self._cells[(0, 0)].get_left()[0] - 0.7 - fr.width / 2, gy, 0])
            self.part("app", appg)
            top_y = self._cells[(0, 0)].get_top()[1] + 0.6      # above the column heads
            bot_y = self._cells[(1, 0)].get_bottom()[1] - 0.25
            arrows = VGroup()
            for r in range(2):
                cell = self._cells[(r, 0)]
                start = fr.get_right() + np.array([0.02, 0.15 if r == 0 else -0.15, 0])
                arrows.add(_arrow(start, cell.get_left() + UP * 0.1 * (1 if r == 0 else -1), OWN, 2.0, buff=0.02))
            for r, y in ((0, top_y), (1, bot_y)):
                cell = self._cells[(r, 1)]
                start = fr.get_corner(UP + RIGHT if r == 0 else DOWN + RIGHT) + LEFT * 0.4
                edge = (cell.get_top() if r == 0 else cell.get_bottom()) + RIGHT * (cw / 2 - 0.35)
                path = _poly([start, [start[0], y, 0], [edge[0], y, 0]], OWN, 2.0)
                arrows.add(VGroup(path, _arrow(np.array([edge[0], y, 0]), edge, OWN, 2.0, buff=0.0)))
            self.part("arrows", arrows)
        self.shift(RIGHT * -self.get_center()[0])           # centred in x
        guard(self.get_left()[0] >= -SAFE_X - 1e-6 and self.get_right()[0] <= SAFE_X + 1e-6,
              f"HandoverGrid spans {self.get_left()[0]:.2f}..{self.get_right()[0]:.2f}")

    def cell(self, r: int, c: int):
        return self._cells[(r, c)]

    def tick(self, r: int, c: int, text: str | None = None) -> list:
        fr = self._cells[(r, c)]
        tk = _keep(check_mark(0.28, S.GREY)).move_to(fr.get_corner(UP + RIGHT) + np.array([-0.25, -0.22, 0]))
        self.part(f"tick_{r}_{c}", tk, shown=False)
        names = [f"tick_{r}_{c}"]
        if text:
            ch = _keep(chip(text, S.GREY, size=CAPTION)).move_to(fr.get_corner(DOWN + RIGHT) +
                                                                  np.array([-0.12, 0.07, 0]), aligned_edge=DOWN + RIGHT)
            self.part(f"chip_{r}_{c}", ch, shown=False)
            names.append(f"chip_{r}_{c}")
        return self.parts_in(*names)

    def light(self, r: int, c: int, color: str = TURN) -> list:
        return [self._cells[(r, c)].animate.set_stroke(color, 3.5)]


def container_glyph(h: float = 0.5, color: str = CTR) -> VGroup:
    """A small TEAL container (a box with two ribs)."""
    b = RoundedRectangle(width=h * 1.3, height=h, corner_radius=0.05, stroke_color=color, stroke_width=2.5) \
        .set_fill(color, 0.2)
    ribs = VGroup(*[Line(UP * h * 0.32, DOWN * h * 0.32, color=color, stroke_width=2).shift(RIGHT * dx * h)
                    for dx in (-0.2, 0.2)])
    return _keep(VGroup(b, ribs))


class BuildLine(Piece):
    """V3's function cell, opened (S04): three GREEN items (main.py, requirements.txt, the entry
    tag "entry point: hello_http") -> a PURPLE "Cloud Build" box -> a TEAL image on a BLUE
    "Artifact Registry" shelf -> a dashed BLUE instance whose PURPLE "functions-framework" layer
    calls the GREEN `def hello_http` by name (GREEN arrow). Built in place: x -6.5..6.4, y
    -1.6..1.2 (above a code panel's space? no: put panels above or below as the scene needs).

        bl = BuildLine(show=("items",))
        self.play(*bl.parts_in("items"))
        self.play(*bl.build())                    # items flow into Cloud Build; image appears
        self.play(*bl.publish())                  # the image drops onto the registry shelf
        self.play(*bl.run())                      # the instance; framework -> hello_http GREEN
        self.play(*bl.set_entry("main"))          # the tag flips; the arrow snaps RED; RED chip
        self.play(*bl.set_entry("hello_http"))    # back to GREEN
    .tag (the current entry tag) .call_arrow .instance. Parts: items, build, image, shelf,
    instance, framework, fn, call, fail."""

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        vis = self._show_set(show, ("items", "build", "image", "shelf", "instance", "framework", "fn", "call"))
        f1 = file_row("main.py", OWN, OWN)
        f2 = file_row("requirements.txt", OWN, OWN)
        self.tag = entry_tag()
        items = VGroup(f1, f2, self.tag).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        items.move_to([-6.45 + items.width / 2, 0.0, 0])
        self.part("items", items, shown="items" in vis)
        bx = RoundedRectangle(width=1.9, height=0.8, corner_radius=0.12, stroke_color=TOOL, stroke_width=3) \
            .set_fill(TOOL, 0.15)
        bt = sans("Cloud Build", CAPTION + 2, INK).move_to(bx)
        build = VGroup(bx, bt).move_to([-1.75, 0.35, 0])
        self.part("build", build, shown="build" in vis)
        img = container_glyph(0.5).move_to([0.55, 0.35, 0])
        imgl = label("image", CAPTION, CTR).next_to(img, UP, buff=0.1)
        self.part("image", VGroup(img, imgl), shown="image" in vis)
        shelf_line = Line([-0.55, -0.75, 0], [1.65, -0.75, 0], color=CLOUD, stroke_width=4)
        shelf_lab = label("Artifact Registry", CAPTION, CLOUD).next_to(shelf_line, DOWN, buff=0.12)
        self.part("shelf", VGroup(shelf_line, shelf_lab), shown="shelf" in vis)
        inst = instance_box(3.6, 2.2, inner=False).move_to([4.6, 0.0, 0])
        self.instance = inst
        self.part("instance", inst, shown="instance" in vis)
        fw = RoundedRectangle(width=3.1, height=0.55, corner_radius=0.08, stroke_color=TOOL, stroke_width=2.5) \
            .set_fill(TOOL, 0.15).move_to([4.6, 0.55, 0])
        fwl = mono("functions-framework", CAPTION, INK).move_to(fw)
        self.part("framework", VGroup(fw, fwl), shown="framework" in vis)
        fn = _keep(chip(f"def {ENTRY}", OWN, size=CAPTION + 2, font=MONO)).move_to([4.6, -0.55, 0])
        self.fn_chip = fn
        self.part("fn", fn, shown="fn" in vis)
        self.call_arrow = Arrow(fw.get_bottom(), fn.get_top(), buff=0.04, color=OWN, stroke_width=4,
                                tip_length=0.16)
        self.part("call", self.call_arrow, shown="call" in vis)
        self.part("fail", _keep(chip("function build failed", ERR, size=CAPTION))
                  .move_to([4.6, -1.45, 0]), shown=False)
        guard(self.get_left()[0] >= -SAFE_X - 1e-6 and self.get_right()[0] <= SAFE_X + 1e-6, "BuildLine width")

    def build(self) -> list:
        """Copies of the three items fly into Cloud Build and vanish; the image appears beside it."""
        out = []
        if not self.is_shown("build"):
            out += self.parts_in("build")
        flyers = VGroup(*[m.copy() for m in self.parts["items"]])
        self.add(flyers)
        tgt = self.parts["build"].get_center()
        fly = flyers.animate.move_to(tgt).set_opacity(0)      # (no shrinking: the text fades as it flies)
        self._flyers = flyers
        img = [] if self.is_shown("image") else late_in(self, "image")
        return [Succession(AnimationGroup(*out), fly, AnimationGroup(*img))]

    def publish(self) -> list:
        """The image drops onto the BLUE Artifact Registry shelf."""
        img = self.parts["image"]
        out = self.parts_in("shelf") if not self.is_shown("shelf") else []
        return out + [img.animate.move_to([0.55, -0.75 + img.height / 2 + 0.06, 0])]

    def run(self) -> list:
        names = [n for n in ("instance", "framework", "fn") if not self.is_shown(n)]
        call = [] if self.is_shown("call") else late_in(self, "call", anim=Create)
        return [Succession(AnimationGroup(*self.parts_in(*names)), AnimationGroup(*call))]

    def set_entry(self, name: str) -> list:
        """The tag's name flips to `name`. name != hello_http: the call arrow turns RED and a RED
        "function build failed" chip appears; hello_http: GREEN again, the chip goes."""
        new = mono(name, CAPTION + 2, OWN if name == ENTRY else ERR).move_to(self.tag.name, aligned_edge=LEFT)
        out = _swap_text(self.tag.row, self.tag.name, new)
        self.tag.name = new
        bad = name != ENTRY
        out.append(self.call_arrow.animate.set_color(ERR if bad else OWN))
        out.append(self.tag.frame.animate.set_stroke(ERR if bad else OWN))
        out += self.parts_in("fail") if bad else self.parts_out("fail")
        return out


# ================================================================== V4 · two doors and a badge (S05)
class TwoDoors(Piece):
    """V4 (S05): a BLUE service box "translation-demo" (4.0 x 2.4) with a door on each side and a
    TEAL "your code" box inside. Left door "who may call it": a GREY browser sends a PINK request
    that passes (public access on) or bounces RED with "403". Right door "who it is when it calls
    out": a BLUE badge on the box, role chips under it, a token from a BLUE "Cloud Run" block,
    a PINK request to a BLUE "Agent Platform" block, the dashed GOLD key crossed out (inside the
    box, bottom right: no key file in the container), and a GREY "you" with an arrow "Service Account User". Built in place: x -6.5..6.5,
    y -3.2..1.75 (the box at (0, 0.1), the badge under it at x 1.2, roles under the badge, Cloud Run
    right of the badge); leave the top band for a README panel (y >= 1.8).

        td = TwoDoors()
        self.play(FadeIn(td))                     # box, doors, captions, browser
        self.play(*td.set_public(True)); self.play(*td.call(True))
        self.play(*td.set_public(False)); self.play(*td.call(False))   # RED bounce + "403"
        self.play(*td.pin_badge()); self.play(*td.add_roles("Agent Platform User", "Service Usage Consumer"))
        self.play(*td.no_key()); self.play(*td.token()); self.play(*td.call_out())
        self.play(*td.you_arrow())
    Parts: box, door_l, door_r, cap_l, cap_r, code, browser, toggle, badge, roles, key, platform,
    tok, agent, out_arrow, you, you_arrow, sau."""

    def __init__(self, name: str = SERVICE_NAME, **kw):
        super().__init__(**kw)
        bx = RoundedRectangle(width=4.0, height=2.4, corner_radius=0.16, stroke_color=CLOUD, stroke_width=3) \
            .set_fill(CLOUD, 0.08).move_to([0, 0.1, 0])
        bt = mono(name, CAPTION + 2, INK).move_to(bx.get_top() + DOWN * 0.3)
        self.part("box", VGroup(bx, bt))
        self.boxf = bx
        dl = door(1.0).move_to(bx.get_left()).align_to(bx, DOWN).shift(UP * 0.25)
        dr = door(1.0).move_to(bx.get_right()).align_to(bx, DOWN).shift(UP * 0.25)
        self.part("door_l", dl)
        self.part("door_r", dr)
        cy = dl.get_top()[1] + 0.45
        self.part("cap_l", label("who may call it", CAPTION + 2, ROUTE)
                  .next_to(bx, LEFT, buff=0.2).set_y(cy))
        self.part("cap_r", label("who it is when it calls out", CAPTION + 2, CLOUD)
                  .next_to(bx, RIGHT, buff=0.2).set_y(cy))
        code = RoundedRectangle(width=1.7, height=0.75, corner_radius=0.08, stroke_color=CTR, stroke_width=2.5) \
            .set_fill(CTR, 0.15).move_to(bx.get_center() + DOWN * 0.15)
        self.part("code", VGroup(code, label("your code", CAPTION, INK).move_to(code)))
        self.codef = code
        br = webpage_glyph(1.1).move_to([-5.7, dl.get_center()[1], 0])
        self.part("browser", br)
        tg = toggle("Allow public access", True).next_to(br, DOWN, buff=0.35).align_to(br, LEFT)
        self.part("toggle", tg, shown=False)
        self.toggle_ = tg
        b = badge().next_to(bx, DOWN, buff=0.3).set_x(1.2)
        self.part("badge", b, shown=False)
        self.badge_ = b
        self.part("roles", VGroup(), shown=True)
        self.part("key", no_key().move_to([1.25, bx.get_bottom()[1] + 0.3, 0]), shown=False)   # no key file inside
        plat = model_box("Cloud Run", w=1.8, h=0.6).move_to([5.45, b.get_center()[1], 0])
        self.part("platform", plat, shown=False)
        agent = model_box("Agent Platform", w=2.0, h=0.7).move_to([5.45, dr.get_center()[1], 0])
        self.part("agent", agent, shown=False)
        you = VGroup(person_icon(YOU, 0.5), label("you", CAPTION, YOU)).arrange(DOWN, buff=0.08)
        you.move_to([-2.6, -2.75, 0])
        self.part("you", you, shown=False)
        self.part("sau", label("Service Account User", CAPTION, YOU), shown=False)
        self.doorl, self.doorr = dl, dr
        guard(self.get_left()[0] >= -SAFE_X - 1e-6 and self.get_right()[0] <= SAFE_X + 1e-6 and
              self.get_bottom()[1] >= -SAFE_Y, f"TwoDoors out of frame ({self.get_left()[0]:.2f}, "
              f"{self.get_right()[0]:.2f}, {self.get_bottom()[1]:.2f})")

    def set_public(self, on: bool) -> list:
        out = self.parts_in("toggle") if not self.is_shown("toggle") else []
        return out + self.toggle_.flip(on)

    def call(self, allowed: bool = True) -> list:
        """A PINK request from the browser to the left door: allowed -> it passes, the code box
        flashes YELLOW; refused -> it bounces back RED and a RED "403" chip sits at the door (the
        code stays dark)."""
        br = self.parts["browser"]
        y = self.doorl.get_center()[1]
        a = Arrow(br.get_right(), self.doorl.get_left() + RIGHT * (0.5 if allowed else 0.0), buff=0.08,
                  color=ROUTE, stroke_width=4, tip_length=0.16)
        a.set_y(y)
        self.add(a)
        if allowed:
            through = _hidden(Arrow(self.doorl.get_right(), self.codef.get_left(), buff=0.05, color=ROUTE,
                                    stroke_width=4, tip_length=0.16))
            self.add(through)
            self._last = VGroup(a, through)
            return [Succession(Create(a, run_time=0.5), _Reveal(through, run_time=0.3),
                               Indicate(self.codef, color=TURN, scale_factor=1.05))]
        back = _hidden(Arrow(self.doorl.get_left() + LEFT * 0.05, br.get_right() + RIGHT * 0.3, buff=0.05,
                             color=ERR, stroke_width=4, tip_length=0.16).shift(DOWN * 0.3))
        c403 = _hidden(_keep(chip("403", ERR, size=CAPTION + 2)).next_to(self.doorl, LEFT, buff=0.25)
                       .shift(UP * 0.5))
        self.add(back, c403)
        self._last = VGroup(a, back, c403)
        return [Succession(Create(a, run_time=0.5), AnimationGroup(_Reveal(back), _Reveal(c403), run_time=0.5))]

    def clear_calls(self) -> list:
        """The last call's arrows (and 403) fade to 0 (they stay members)."""
        m = getattr(self, "_last", None)
        if m is None:
            return []
        self._last = None
        return [m.animate.set_opacity(0)]

    def pin_badge(self) -> list:
        return self.parts_in("badge", anim=lambda m: FadeIn(m, shift=UP * 0.2))

    def add_roles(self, *names, color: str = IDENTITY) -> list:
        """Role chips attach in a row under the badge (or a second row when too wide)."""
        roles = self.parts["roles"]
        out = []
        for n in names:
            c = role_chip(n, color)
            if len(roles):
                c.next_to(roles[-1], RIGHT, buff=0.15)
                if c.get_right()[0] > SAFE_X:
                    c.next_to(roles[0], DOWN, buff=0.1, aligned_edge=LEFT)
            else:
                c.next_to(self.badge_, DOWN, buff=0.15).align_to(self.badge_, LEFT)
            roles.add(c)
            out.append(FadeIn(c, shift=UP * 0.1))
        guard(roles.get_right()[0] <= SAFE_X + 1e-6, "role chips run off the right edge")
        return out

    def no_key(self) -> list:
        return self.parts_in("key")

    def token(self) -> list:
        """The BLUE "Cloud Run" platform block appears right of the badge; a token flies from it into
        the badge."""
        out = self.parts_in("platform") if not self.is_shown("platform") else []
        t = _hidden(token_glyph().move_to(self.parts["platform"].get_left()))
        self.add(t)
        self._tok = t
        return [Succession(AnimationGroup(*out), _Reveal(t, scale=0.5),
                           t.animate.move_to(self.badge_.frame.get_right() + LEFT * 0.25))]

    def call_out(self) -> list:
        """A PINK request leaves the right door for the BLUE Agent Platform block."""
        out = self.parts_in("agent") if not self.is_shown("agent") else []
        a = Arrow(self.doorr.get_right(), self.parts["agent"].get_left(), buff=0.08, color=ROUTE, stroke_width=4,
                  tip_length=0.16)
        self.part("out_arrow", a, shown=False)
        return [Succession(AnimationGroup(*out), *late_in(self, "out_arrow", anim=Create))]

    def you_arrow(self) -> list:
        """GREY "you" bottom left; an arrow to the badge; "Service Account User" beside "you"."""
        you = self.parts["you"]
        a = Arrow(you.get_right(), self.badge_.frame.get_left(), buff=0.12, color=YOU, stroke_width=3,
                  tip_length=0.14)
        self.part("you_arrow", a, shown=False)
        sau = self.parts["sau"]
        sau.next_to(you, RIGHT, buff=0.25).align_to(you, DOWN)
        return [Succession(AnimationGroup(*self.parts_in("you")), *late_in(self, "you_arrow", anim=Create),
                           AnimationGroup(*late_in(self, "sau")))]


def toggle(text: str, on: bool = True, size: float = CAPTION) -> VGroup:
    """A schematic console toggle (tag it illustration_tag()): a pill switch + its label. .flip(on)
    -> anims. .pill .knob .text"""
    pill = RoundedRectangle(width=0.7, height=0.34, corner_radius=0.17, stroke_color=S.GREY, stroke_width=2) \
        .set_fill(OWN if on else S.GREY_DARK, 0.6)
    knob = Circle(radius=0.13, stroke_width=0).set_fill(INK, 1).move_to(pill.get_center() + RIGHT * (0.18 if on else -0.18))
    t = label(text, size, INK).next_to(pill, RIGHT, buff=0.16)
    g = VGroup(pill, knob, t)
    g.pill, g.knob, g.text = pill, knob, t

    def flip(v: bool):
        return [pill.animate.set_fill(OWN if v else S.GREY_DARK, 0.6),
                knob.animate.move_to(pill.get_center() + RIGHT * (0.18 if v else -0.18))]
    g.flip = flip
    return _keep(g)


def service_box(title: str, w: float = 3.0, h: float = 1.6, color: str = CLOUD) -> VGroup:
    """A BLUE workload box with a mono title at its top ("translation-audio (job)"); at least as
    wide as its title + 0.4. .frame .title"""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=color, stroke_width=3) \
        .set_fill(color, 0.08)
    t = mono(title, CAPTION, INK)
    if t.width > w - 0.3:                      # the box grows to its title
        fr.stretch_to_fit_width(t.width + 0.4)
    t.move_to(fr.get_top() + DOWN * 0.28)
    g = VGroup(fr, t)
    g.frame, g.title = fr, t
    return g


# ================================================================== V5 · thin clients, one door (S06, S07)
class ThinClients(Piece):
    """V5 (S06; rewound in S07). NOTE: S06's scene class has the same name: import this one as
    `from common import ThinClients as ClientsPiece`.

    Two GREY clients on the left (a phone app at y 0.9, a web page at y -1.3), each with a GREEN
    preprocessing gear and a PINK arrow to a BLUE "Vertex AI endpoint" box on the right (with a
    version dial). Each arrow carries a chip ("float tensor"; after the move, `{"b64": …}`).
    Each client has a small answer bubble (GREEN healthy / RED wrong). Built in place: x -6.5..6.5,
    y -1.9..2.5 (the recipe row of three chips sits at y 2.1, from x -4.5).

        tc = ThinClients()
        self.play(FadeIn(tc))                         # clients, endpoint, arrows (no gears yet)
        self.play(*tc.parts_in("gear0", "gear1", "chip0", "chip1"))
        self.play(*tc.recipe())                       # three GREEN chips beside the phone's gear
        self.play(*tc.drift(1))                       # web gear goes RED; its chip RED; its answer RED
        self.play(*tc.to_endpoint())                  # gears merge into one inside the endpoint; b64 chips
        self.play(*tc.set_version("v2", bad=True))    # both answers RED at once
        self.play(*tc.set_version("v1"))              # both healthy at once
        self.play(*tc.to_clients())                   # replay: gears back on the clients; dial greys
    Parts: phone, web, endpoint, dial, arrow0, arrow1, chip0, chip1, gear0, gear1, egear, ans0,
    ans1, recipe, b64_0, b64_1."""

    def __init__(self, **kw):
        super().__init__(**kw)
        ys = (0.9, -1.3)
        ph = VGroup(phone_glyph(0.85), label("phone app", CAPTION, CLIENT)).arrange(DOWN, buff=0.1)
        wb = VGroup(webpage_glyph(1.1), label("web page", CAPTION, CLIENT)).arrange(DOWN, buff=0.1)
        ph.move_to([-5.7, ys[0], 0])
        wb.move_to([-5.7, ys[1], 0])
        self.part("phone", ph)
        self.part("web", wb)
        ep = RoundedRectangle(width=3.0, height=3.4, corner_radius=0.16, stroke_color=CLOUD, stroke_width=3) \
            .set_fill(CLOUD, 0.08).move_to([4.9, -0.2, 0])
        et = VGroup(*[sans(s, CAPTION + 2, INK) for s in ("Vertex AI", "endpoint")]).arrange(DOWN, buff=0.05)
        et.move_to(ep.get_top() + DOWN * 0.5)
        mdl = model_box("model", w=1.3, h=0.6).move_to(ep.get_center() + DOWN * 0.1 + RIGHT * 0.6)
        self.part("endpoint", VGroup(ep, et, mdl))
        self.ep, self.mdl = ep, mdl
        dial = VersionDial().move_to(ep.get_center() + DOWN * 1.25)
        self.part("dial", dial, shown=False)
        self.dial = dial
        self.gx = -4.3
        for k, y in enumerate(ys):
            g = gear(0.32).move_to([self.gx, y, 0])
            self.part(f"gear{k}", g, shown=False)
            a = Arrow([self.gx + 0.4, y, 0], [ep.get_left()[0], ep.get_center()[1] + (0.6 if k == 0 else -1.0), 0],
                      buff=0.05, color=ROUTE, stroke_width=3.5, tip_length=0.16)
            self.part(f"arrow{k}", a)
            c = _keep(chip("float tensor", ROUTE, size=CAPTION)).move_to(a.point_from_proportion(0.45) + UP * 0.32)
            self.part(f"chip{k}", c, shown=False)
            b = _keep(chip('{"b64": "…"}', ROUTE, size=CAPTION, font=MONO)).move_to(a.point_from_proportion(0.45) +
                                                                                   UP * 0.32)
            self.part(f"b64_{k}", b, shown=False)
            ans = answer_bubble(OWN).next_to(self.parts["phone" if k == 0 else "web"], UP, buff=0.08) \
                .shift(RIGHT * 0.55)
            self.part(f"ans{k}", ans, shown=False)
        eg = gear(0.36).move_to(ep.get_center() + DOWN * 0.1 + LEFT * 0.7)
        self.part("egear", eg, shown=False)
        rec = VGroup(*[_keep(chip(s, OWN, size=CAPTION)) for s in ("decode JPEG", "scale to 0–1", "resize 224×224")])
        rec.arrange(RIGHT, buff=0.2).move_to([-4.5, 2.1, 0], aligned_edge=LEFT)
        self.part("recipe", rec, shown=False)
        guard(self.get_left()[0] >= -SAFE_X - 1e-6 and self.get_right()[0] <= SAFE_X + 1e-6 and
              self.get_top()[1] <= 2.55, f"ThinClients out of its band (top {self.get_top()[1]:.2f})")

    def recipe(self) -> list:
        rec = self.parts["recipe"]
        self._flag(rec, False)
        return [LaggedStart(*[_appear(r) for r in rec], lag_ratio=0.7, run_time=1.5)]

    def answers(self, color: str = OWN, which=(0, 1)) -> list:
        """The answer bubbles of `which` clients turn `color` (shown first if hidden)."""
        out = []
        for k in which:
            n = f"ans{k}"
            m = self.parts[n]
            if not self.is_shown(n):
                m.set_stroke(color)
                for f in m.get_family():
                    if hasattr(f, "_hop"):
                        f._hop = (0.3, 1.0)
                    f.set_fill(color)
                out += late_in(self, n)
            else:
                out.append(m.animate.set_stroke(color).set_fill(color, 0.3))
        return out

    def drift(self, k: int = 1) -> list:
        """Client k's gear quietly changes a step: RED outline; its chip RED; its answer RED."""
        g, c = self.parts[f"gear{k}"], self.parts[f"chip{k}"]
        return [g.animate.set_stroke(ERR), c.box.animate.set_stroke(ERR), *self.answers(ERR, (k,))]

    def to_endpoint(self) -> list:
        """Both gears fly into the endpoint and become one (egear); the arrows' chips swap to the
        `{"b64": "…"}` chips; both answers GREEN."""
        eg = self.parts["egear"]
        out = []
        for k in (0, 1):
            g = self.parts[f"gear{k}"]
            out.append(g.animate.move_to(eg).set_stroke(OWN))
        out2 = [*late_in(self, "egear")]
        for k in (0, 1):
            out2 += self.parts_out(f"gear{k}", f"chip{k}") + late_in(self, f"b64_{k}")
        out2 += self.answers(OWN)
        return [Succession(AnimationGroup(*out, run_time=0.9), AnimationGroup(*out2, run_time=0.6))]

    def set_version(self, v: str, bad: bool = False) -> list:
        """The endpoint's dial turns to v; bad=True: the endpoint gear gets a RED outline and both
        answers turn RED at the same instant; otherwise both GREEN with a YELLOW flash."""
        guard(self.is_shown("dial"), "show the dial first: self.play(*tc.parts_in('dial'))")
        out = self.dial.set(v, bad)
        eg = self.parts["egear"]
        out.append(eg.animate.set_stroke(ERR if bad else OWN))
        col = self.answers(ERR if bad else OWN)
        if bad:
            return out + col
        flash = [Indicate(self.parts[f"ans{k}"], color=TURN) for k in (0, 1)]
        return out + [Succession(AnimationGroup(*col), AnimationGroup(*flash))]

    def to_clients(self) -> list:
        """Replay: the gears go back onto the clients (GREEN), the endpoint gear goes, the dial
        greys, the b64 chips swap back to "float tensor"."""
        out = []
        for k, y in enumerate((0.9, -1.3)):
            g = self.parts[f"gear{k}"]
            g.move_to([self.gx, y, 0]).set_stroke(OWN)
            self.parts[f"chip{k}"].box.set_stroke(ROUTE)
            out += self.parts_in(f"gear{k}", f"chip{k}") + self.parts_out(f"b64_{k}")
        out += self.parts_out("egear")
        if self.is_shown("dial"):
            out.append(self.dial.animate.set_opacity(0.3))
        return out


def answer_bubble(color: str = OWN) -> VGroup:
    """A small speech bubble (a client's answer): rounded box + tail, tinted `color`, no text."""
    b = RoundedRectangle(width=0.55, height=0.36, corner_radius=0.12, stroke_color=color, stroke_width=2.5) \
        .set_fill(color, 0.3)
    tail = Polygon(b.get_bottom() + LEFT * 0.12, b.get_bottom() + LEFT * 0.02, b.get_bottom() + LEFT * 0.2 + DOWN * 0.14,
                   stroke_color=color, stroke_width=2.5).set_fill(color, 0.3)
    return _keep(VGroup(b, tail))


# ================================================================== V6 · the serving plug (S07)
class ServingPlug(Piece):
    """V6 (S07): the pipeline PINK "JPEG bytes" -> GREEN "decode" -> "to float" -> "resize" ->
    "model" -> four probability bars (CHEESES), at y 1.3; brackets "preprocess_image" (over the
    three preprocessing blocks, label above) and "serving_function" (under all five, with a GREY
    chip "a.k.a. serve"); below, a GREEN "SavedModel" block with the export socket
    `serving_default` on its left and a PURPLE "model server" to its right, the output spot right
    of the server. Plugs come from the left (x -4.6) into the socket. Built in place: x -6.5..6.5,
    y -2.6..2.3.

        sp = ServingPlug(show=("blocks",))
        self.play(*sp.write_block(0)) …               # or sp.parts_in("blocks") at once
        self.play(*sp.bracket("pre")); self.play(*sp.bracket("serve"))
        self.play(*sp.parts_in("saved", "socket", "server"))
        self.play(*sp.plug("preprocess", letter="B"))  # 224×224×3 image out + RED ✗ "no prediction"
        self.play(*sp.unplug())
        self.play(*sp.plug("raw", letter="A"))         # socket label -> "expects float tensors"; RED bounce
        self.play(*sp.unplug())
        self.play(*sp.plug("serve", letter="C"))       # probability bars rise, brie YELLOW
    .blocks (VGroup of the 5 blocks + bars), .bars (ProbBars, top), .out_bars (ProbBars at the
    output spot). Parts: blocks, arrows, bars, pre, serve, alias, saved, socket, server, wire."""

    TOP_Y, LOW_Y = 1.3, -1.55

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        vis = self._show_set(show, ("blocks", "arrows", "bars", "pre", "serve", "alias", "saved", "socket",
                                    "server", "wire"))
        names = [("JPEG bytes", ROUTE), ("decode", OWN), ("to float", OWN), ("resize", OWN), ("model", OWN)]
        blocks = VGroup()
        for t, c in names:
            tx = sans(t, CAPTION + 2, INK)
            fr = RoundedRectangle(width=max(1.35, tx.width + 0.35), height=0.7, corner_radius=0.1, stroke_color=c,
                                  stroke_width=3).set_fill(c, 0.14)
            tx.move_to(fr)
            blocks.add(VGroup(fr, tx))
        blocks.arrange(RIGHT, buff=0.42).move_to([-1.7, self.TOP_Y, 0])
        blocks.shift(RIGHT * (-6.45 - blocks.get_left()[0]))
        self.blocks = blocks
        self.part("blocks", blocks, shown="blocks" in vis)
        self._whole_blocks = "blocks" in vis
        arrows = VGroup(*[_arrow(blocks[i].get_right(), blocks[i + 1].get_left(), S.GREY, 2.5) for i in range(4)])
        bars = ProbBars(bar_w=1.0)
        bars.next_to(blocks, RIGHT, buff=0.55)
        arrows.add(_arrow(blocks[-1].get_right(), bars.get_left(), S.GREY, 2.5))
        self.part("arrows", arrows, shown="arrows" in vis)
        self.bars = bars
        self.part("bars", bars, shown="bars" in vis)
        pre = _hbracket(VGroup(*blocks[1:4]), "preprocess_image", UP, OWN)
        self.part("pre", pre, shown="pre" in vis)
        srv = _hbracket(VGroup(*blocks), "serving_function", DOWN, OWN)
        self.part("serve", srv, shown="serve" in vis)
        alias = _keep(chip("a.k.a. serve", S.GREY, size=CAPTION)).next_to(srv.text, RIGHT, buff=0.3)
        self.part("alias", alias, shown="alias" in vis)
        sm = RoundedRectangle(width=2.4, height=1.1, corner_radius=0.12, stroke_color=OWN, stroke_width=3) \
            .set_fill(OWN, 0.12).move_to([0.1, self.LOW_Y, 0])
        smt = sans("SavedModel", CAPTION + 2, INK).move_to(sm)
        self.part("saved", VGroup(sm, smt), shown="saved" in vis)
        so = socket().move_to(sm.get_left() + LEFT * 0.31)
        so.label.next_to(so.frame, DOWN, buff=0.14)
        self.sock = so
        self.part("socket", so, shown="socket" in vis)
        sv = RoundedRectangle(width=1.9, height=1.0, corner_radius=0.12, stroke_color=TOOL, stroke_width=3) \
            .set_fill(TOOL, 0.14).move_to([2.95, self.LOW_Y, 0])
        svt = VGroup(*[sans(s, CAPTION, INK) for s in ("model", "server")]).arrange(DOWN, buff=0.04).move_to(sv)
        self.part("server", VGroup(sv, svt), shown="server" in vis)
        self.part("wire", _arrow(sm.get_right(), sv.get_left(), TOOL, 3), shown="wire" in vis)
        self.out_x = 5.35
        self.out_bars = ProbBars(bar_w=0.9)
        self.out_bars.move_to([self.out_x + 0.05, self.LOW_Y, 0])
        self.part("out_bars", self.out_bars, shown=False)
        self.part("out_arrow", _arrow(sv.get_right(), [self.out_x - 1.1, self.LOW_Y, 0], S.GREY, 2.5), shown=False)
        self.cur = None
        guard(self.get_left()[0] >= -SAFE_X - 1e-6 and self.get_right()[0] <= SAFE_X + 1e-6,
              f"ServingPlug spans {self.get_left()[0]:.2f}..{self.get_right()[0]:.2f}")

    def write_block(self, i: int) -> list:
        """Block i (0..4) of the pipeline writes in, with the arrow before it (i = 5: the bars)."""
        bl, ar = self.parts["blocks"], self.parts["arrows"]
        guard(not getattr(self, "_whole_blocks", False),
              "write_block needs the pipeline hidden: ServingPlug(show=(...)) without 'blocks', 'arrows', 'bars'")
        out = []
        if i < 5:
            self._flag(bl, False)
            out.append(_appear(bl[i]))
        if i >= 1:
            self._flag(ar, False)
            out.append(_appear(ar[i - 1]))
        if i == 5:
            out += late_in(self, "bars")
        return out

    def bracket(self, which: str = "pre") -> list:
        """"pre": the preprocess_image bracket over decode..resize; "serve": the serving_function
        bracket under all five + the alias chip."""
        return self.parts_in("pre") if which == "pre" else self.parts_in("serve", "alias")

    def plug(self, kind: str, letter: str | None = None) -> list:
        """kind "preprocess" (option B: out comes a 224×224×3 image, RED ✗ "no prediction"), "raw"
        (A/D: the socket's label becomes "expects float tensors", the PINK bytes chip bounces RED),
        "serve" (C: the four probabilities rise, brie YELLOW). Returns the animations (plug slides in,
        then the outcome)."""
        text = {"preprocess": "preprocess_image", "raw": "raw model", "serve": "serving_function"}[kind]
        p = plug(text, OWN, letter)
        y = self.sock.frame.get_center()[1]
        p.move_to([0, y, 0])
        p.shift(RIGHT * (self.sock.mouth()[0] - 0.55 - p.prongs.get_right()[0]))
        dx = self.sock.mouth()[0] + 0.18 - p.prongs.get_right()[0]
        guard(p.get_left()[0] >= -SAFE_X - 1e-6, f"plug {text!r} starts off the left edge")
        self.add(p)
        self.cur = VGroup(p)
        ins = AnimationGroup(FadeIn(p, shift=RIGHT * 0.3), run_time=0.4)
        push = p.animate(run_time=0.6).shift(RIGHT * dx)
        bytes_chip = _keep(chip("JPEG bytes", ROUTE, size=CAPTION)).next_to(p, UP, buff=0.35)
        bytes_chip.shift(RIGHT * dx)
        _hidden(bytes_chip)
        self.add(bytes_chip)
        self.cur.add(bytes_chip)
        outcome = []
        if kind == "preprocess":
            img = image_glyph(0.45).move_to([self.out_x, self.LOW_Y + 0.15, 0])
            x = _keep(cross_mark(0.3, ERR)).next_to(img.stack, RIGHT, buff=0.15)
            nop = label("no prediction", CAPTION, ERR).next_to(img, DOWN, buff=0.12)
            for m in (img, x, nop):
                _hidden(m)
            self.add(img, x, nop)
            self.cur.add(img, x, nop)
            outcome = [*late_in(self, "out_arrow"), _Reveal(img, shift=RIGHT * 0.2), _Reveal(x), _Reveal(nop)]
        elif kind == "raw":
            new = mono("expects float tensors", CAPTION + 2, ERR).move_to(self.sock.label)
            self._old_label = self.sock.label
            outcome = _swap_text(self.sock, self.sock.label, new) + \
                [Succession(bytes_chip.animate(run_time=0.3).set_color(ERR),
                            bytes_chip.animate(run_time=0.4, rate_func=there_and_back).shift(LEFT * 0.4))]
            self.sock.label = new
        else:
            outcome = [*late_in(self, "out_arrow", "out_bars"), *self.out_bars.rise()]
        return [Succession(ins, push, _Reveal(bytes_chip, run_time=0.3), AnimationGroup(*outcome, run_time=0.8))]

    def unplug(self) -> list:
        """The current plug, its chip and its outcome fade to 0; the socket's label returns; the
        output arrow and bars hide."""
        out = []
        if self.cur is not None:
            out.append(self.cur.animate.set_opacity(0))
            self.cur = None
        if getattr(self, "_old_label", None) is not None:
            old = mono("serving_default", CAPTION + 2, OWN).move_to(self.sock.label)
            out += _swap_text(self.sock, self.sock.label, old)
            self.sock.label = old
            self._old_label = None
        names = [n for n in ("out_arrow", "out_bars") if self.is_shown(n)]
        out += self.parts_out(*names)
        return out


def _hbracket(mobs, text: str, side=UP, color: str = OWN) -> VGroup:
    """A square bracket over (side=UP) or under (DOWN) `mobs` with a mono label (22 pt) beyond it.
    .line .text"""
    l, r = mobs.get_left()[0] - 0.08, mobs.get_right()[0] + 0.08
    s = 1 if np.array_equal(side, UP) else -1
    y = (mobs.get_top()[1] + 0.14) if s > 0 else (mobs.get_bottom()[1] - 0.14)
    ln = VMobject(stroke_color=color, stroke_width=3)
    ln.set_points_as_corners([[l, y - 0.1 * s, 0], [l, y, 0], [r, y, 0], [r, y - 0.1 * s, 0]])
    t = mono(text, CAPTION + 2, color).next_to([(l + r) / 2, y, 0], side, buff=0.1)
    g = VGroup(ln, t)
    g.line, g.text = ln, t
    return g


hbracket = _hbracket
