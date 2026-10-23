"""Shared scene code for AC215 L10 (connecting to the cloud: who checks that it's you, and how does a
page find a database?).

Paths, narration (SAY lines straight from script.md), the semantic colours of BRIEF.md, the running
example, the six trackers A-F, loaders for the real captures in assets/, terminal helpers, tags,
small glyphs, and the video's set pieces V1-V6.  The scene authors' contract is build/SCENE-NOTES.md;
the reference scene is s01_hook.py; build/common_test.py (Bench) plays every set piece once.

    from manim import *          # first
    from common import *         # second (common's names win), then:
    SAY = NARRATION["S07"]; assert len(SAY) == n   # one `with self.voiceover(SAY[i]) as vo:` each

Every text here is >= 20 pt.  Never .scale() a group that holds text below 1.0; set pieces take
size parameters instead (house_w, cell_h ...).  Never set width/height/color/depth on a VGroup
subclass (Manim properties): these classes use house_w, slot_w, card_w ...
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
                   ReplacementTransform, RoundedRectangle, ShowIncreasingSubsets, Succession, Text,
                   Transform, UpdateFromAlphaFunc, VGroup, VMobject, linear, there_and_back)

from explainer import style as S
from explainer.components import pause_and_ponder, person_icon, ponder_card  # noqa: F401 (re-export)
from explainer.devops import (CAPTION, LABEL, MONO, OUTPUT, PANEL, SMALL, TAG, TERM_BG,  # noqa: F401
                              ReadmeTracker, Terminal, box, cell_width, check_mark, chip, code_block,
                              code_panel, code_span, cross_mark, file_glyph, file_tree, folder_glyph,
                              glyph_range, label, lecture_ref, line_bar, line_pitch, mono, mono_line,
                              step_badge, substring, tag, warning_sign)
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
SAY_COUNT = {"S01": 4, "S02": 5, "S03": 5, "S04": 7, "S05": 6, "S06": 7, "S07": 6, "S08": 6, "S09": 8,
             "S10": 6, "S11": 6, "S12": 9, "S13": 4, "S14": 5, "S15": 6}

# ------------------------------------------------------------------ semantic colours (BRIEF.md)
LAPTOP = S.GREY          # your laptop: the host shell, the host filesystem, the browser's home
CLOUD = S.BLUE           # Google's building, Vertex AI, GCS, the token desk, the bearer ticket
IMAGE = S.TEAL           # containers and images: llm-rag-cli, llm-rag-chromadb, api-service, frontend
CONTAINER = IMAGE
SYSTEM = S.ORANGE        # system-wide / host-owned: Docker Desktop itself (little this lecture)
SECRET = S.GREEN         # project-owned, protected: secrets/, the JSON key, the mounted /secrets
KEY = SECRET
PASS = S.GREEN           # an allowed cell, a pass, a 200
TOOL = S.PURPLE          # docker, compose, gcloud, uv, pipenv, npm, uvicorn, next
ERR = S.RED              # DefaultCredentialsError, 403, 500, the aborted script, CORS "no header"
TURN = S.YELLOW          # your turn, the tracker, the current step, "look here"
COST = S.GOLD            # money: every Vertex AI call the student's run makes
ROUTE = S.PINK           # Docker networks (streets), Docker DNS, ADC's lookup walk, tunnels, browser calls
FUTURE = S.GREY          # future / elsewhere: deleted hosted deployment, L11 buckets, metadata server: dashed
DOOR = S.GREY            # an open (unprefixed) published port: neutral, never GREEN
INK = S.WHITE
DIMMED = S.GREY

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
TRACK_BOTTOM = 2.9           # the tracker's lowest point
BOTTOM = -3.5                # a terminal's bottom edge (kept when it grows or shrinks)


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


# ------------------------------------------------------------------ running example
USER = "student"
P_LAPTOP_HOME = "student@laptop:~$"
P_REPO = "student@laptop:~/cheese-app-v0$"
P_LLMRAG = "student@laptop:~/cheese-app-v0/llm-rag$"
P_API = "student@laptop:~/cheese-app-v0/api-service$"
P_FRONTEND = "student@laptop:~/cheese-app-v0/frontend-ai-chatbot$"
P_LAPTOP = P_LAPTOP_HOME
T_LAPTOP = "laptop"
T_SECOND = "laptop · second terminal"
PROJECT_ID = "your-gcp-project"            # the only project id ever shown as ours
SA_NAME = "llm-service-account"
SA_EMAIL = "llm-service-account@your-gcp-project.iam.gserviceaccount.com"
KEY_PATH = "/secrets/llm-service-account.json"
ENV_VAR = "GOOGLE_APPLICATION_CREDENTIALS"
TOKEN_URI = "https://oauth2.googleapis.com/token"
TOKEN_DESK = "oauth2.googleapis.com/token"
QUESTION = "How is tolminc cheese made?"   # README.md line 215, quoted as written
CHROMA_DNS = "llm-rag-chromadb:8000"
STREETS = {"llm-rag": "llm-rag-network", "cheese-app": "cheese-app-network"}
# (host port, container port) of every published door; container name of each house
PORTS = {"8000": ("8000", "8000"), "9000": ("9000", "9000"), "3200": ("3200", "3000")}
CONTAINERS = {"loader": "llm-rag-cli", "chroma": "llm-rag-chromadb",
              "api": "llm-rag-analysis-api-service", "frontend": "llm-rag-analysis-frontend-ai-chatbot"}
# the zeroed key card (digest §3.1, the placeholder's field names); never a real-looking value
KEY_FIELDS = (("type", "service_account"), ("project_id", PROJECT_ID),
              ("private_key_id", "0000…"), ("private_key", "PLACEHOLDER"),
              ("client_email", "llm-service-account@…"), ("client_id", "0000…"),
              ("token_uri", TOKEN_URI))
# S01's riddles (slide 4's trick on this app) and slide 11's flip; S15 brings the labels back
RIDDLES = (("-p 3200:3000", "two numbers: why?"), ("localhost:9000", "which machine is that?"),
           ("llm-rag-chromadb", "a name: where is the address?"))
KNOCK = "once anything can knock: who's allowed in?"


def readme(n: int) -> str:
    """cheese-app-v0/README.md line n (1-based), stripped: assert cap.cmd == readme(88)."""
    return excerpt("cheese-app-v0/README.md", n, n).strip()


# ------------------------------------------------------------------ trackers (BRIEF.md, six)
SECTIONS = {
    "A": "Prerequisites & Service Account",
    "B": "Build the Vector DB",
    "C": "Run API Service Container",
    "D": "Run Frontend Container",
    "E": "The five UI steps",
    "F": "Shut down",
}
STEPS = {
    "A": ["Docker + clone", "Create llm-service-account + roles", "JSON key → secrets/",
          "Folder tree check", "Create the network"],
    "B": ["Edit GCP_PROJECT", "docker-shell", "cli char-split", "cli recursive-split",
          "Exit (Chroma stays up)"],
    "C": ["Edit GCP_PROJECT", "docker-shell", "uvicorn_server", "/docs"],
    "D": ["docker-shell", "npm install", "npm run dev", "Open :3200"],
    "E": ["Text Chunking", "Vector DB UI", "Chat", "Cheese Expert Agent", "Pavlos Cheese Model"],
    "F": ["Ctrl-C + exit each", "docker compose down"],
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
    """Tracker `key` ("A".."F") at `step` (1-based; None = no step lit yet), placed top-left:
    'README › <section>', one dot per step, 'step k of N: <step>' (+ ' · extra')."""
    tr = ReadmeTracker(SECTIONS[key], STEPS[key])
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
    Use this, never tr.goto(). The caption cross-fades in place (never a glyph-by-glyph morph)."""
    k = tr.k if k is None else k
    anims = []
    if k != tr.k:
        for i, d in enumerate(tr.dots, start=1):
            col = tr.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK)
            anims.append(d.animate.set_color(col).scale((1.5 if i == k else 1.0) / (d.width / 0.12)))
    old, new = tr.caption.copy(), _caption(tr, k, extra)

    def fade_swap(m, a):
        src, f = (old if a < 0.5 else new), abs(1 - 2 * a)
        c = src.copy()
        for g, g0 in zip(c.family_members_with_points(), src.family_members_with_points()):
            g.set_fill(opacity=g0.get_fill_opacity() * f).set_stroke(opacity=g0.get_stroke_opacity() * f)
        m.become(c)

    anims.append(UpdateFromAlphaFunc(tr.caption, fade_swap))
    tr.k = k
    return AnimationGroup(*anims, run_time=run_time)


def swap_tracker(scene, old: ReadmeTracker, new: ReadmeTracker, *anims, run_time: float = 0.6):
    """Plays: tracker `old` becomes `new` in place (section name and caption cross-fade, the dots
    regroup). `new` ends on the scene as one piece; `old` is gone."""
    keep = VGroup(old.head[0], old.head[1])          # 'README ›' stays put
    scene.remove(old)
    scene.add(*keep, old.head[2], old.dots, old.caption)
    moves = [FadeTransform(old.head[2], new.head[2]), ReplacementTransform(old.dots, new.dots),
             FadeTransform(old.caption, new.caption)]
    scene.play(*moves, *anims, run_time=run_time)
    scene.remove(*keep, *new.head, new.dots, new.caption)
    scene.add(new)
    return new


def lref(slides: str) -> VGroup:
    """The GREY 'Lecture 10 · slides 4, 11–13' tag, top right (one per scene, BRIEF)."""
    return lecture_ref(10, slides)


# ------------------------------------------------------------------ captures
LAPTOP_DIR = "laptop"
# file lines never to print (capture-only, ASSETS.md / script.md crops): checked by Capture.line()
NEVER = {("laptop", "33-docker-shell.txt"): {42, 164},      # readiness GET /, GET /capture-done 404
         ("laptop", "51-npm-run-dev.txt"): {54, 55}}        # /_not-found compile, /capture-done 404

_PROMPT_RE = re.compile(r"^((?:\([^)]*\) )?(?:[\w.-]+@)?[\w.-]+:[^#$\s]*[#$])(?: (.*))?$")


def split_prompt(s: str) -> tuple[str, str]:
    """'app@3c41bc0606ad:/app$ ls -la /secrets' -> ('app@3c41bc0606ad:/app$', 'ls -la /secrets');
    '(app) app@ed21…:/app$ uvicorn_server' and the root '6c23fe52ca92:/app# npm run dev' too.
    A line without a prompt -> ('', s)."""
    m = _PROMPT_RE.match(s)
    if not m:
        return "", s
    return m.group(1), m.group(2) or ""


class Capture:
    """One captured command (assets/terminal/laptop/<file>). .cmd (as typed) .lines (output body,
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

    def istep(self, n: int) -> tuple[str, str]:
        """File line n split into (prompt, typed): the istep captures 21, 24, 25, 29, 33, 50, 51, 73."""
        return split_prompt(self.line(n))


def capture(name: str) -> Capture:
    """capture("21") or capture("21-docker-shell") or capture("laptop/21"): the one file
    assets/terminal/laptop/NN-*.txt. Fails loudly when missing: never show an uncaptured output.
    A trailing inline '[exit N]' (23:2, 34:2, 37:8, 63:2, 74:2) is split off the last line, so
    .at(2) of capture("23") is '"1.0.0"'."""
    folder, name = name.split("/", 1) if "/" in name else (LAPTOP_DIR, name)
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
    with open(p, encoding="utf-8", newline="") as f:
        text = f.read()
    raw = [s.rstrip("\r").expandtabs(8) for s in text.rstrip("\n").split("\n")]
    m = re.fullmatch(r"(.*\S)\[exit (-?\d+)\]", raw[-1]) if len(raw) > 1 else None
    if m:                                   # '"1.0.0"[exit 0]': output and status on one line
        raw = raw[:-1] + [m.group(1), f"[exit {m.group(2)}]"]
    cmd = raw[0][2:] if raw[0].startswith("$ ") else ""
    body = raw[1:]
    code_ = 0
    if body and re.fullmatch(r"\[exit -?\d+\]", body[-1]):
        code_ = int(body[-1][6:-1])
        body = body[:-1]
    return Capture(cmd, body, code_, raw, p, NEVER.get((folder, p.name), ()))


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
         ".yml": "yaml", ".ini": "ini", ".txt": "text", ".json": "json", ".js": "javascript",
         ".jsx": "jsx", ".lock": "json"}
_NEIGHBOURS = ("llm-finetuning", "mega-pipeline", "llm-rag")


def _src(path: str) -> Path:
    p = SOURCE / path
    if p.exists():
        return p
    q = SOURCE / "cheese-app-v0" / path
    if q.exists():
        return q
    raise FileNotFoundError(f"assets/source/{path} (nor cheese-app-v0/{path})")


def source_text(path: str) -> str:
    """An assets/source file: 'cheese-app-v0/api-service/docker-shell.sh' (the 'cheese-app-v0/'
    prefix may be left out) or a neighbour repo 'llm-finetuning/dataset-creator/cli.py'."""
    return _src(path).read_text(encoding="utf-8")


def excerpt(path: str, first: int, last: int) -> str:
    """Lines first..last (1-based, inclusive) of assets/source/<path>."""
    return "\n".join(source_text(path).split("\n")[first - 1:last])


def shown_path(path: str) -> str:
    """The header name of a source file: repo-relative for cheese-app-v0
    ('api-service/docker-shell.sh'); 'llm-finetuning · gemini-finetuner/cli.py' for a neighbour."""
    rel = _src(path).relative_to(SOURCE).as_posix()
    top, _, rest = rel.partition("/")
    if top == "cheese-app-v0":
        return rest
    if top in _NEIGHBOURS:
        return f"{top} · {rest}"
    return rel


def _lang(name: str) -> str:
    if name.startswith("Dockerfile"):
        return "docker"
    if name.startswith(".env") or name == ".gitignore":
        return "bash"
    if name == "Pipfile":
        return "toml"
    return _LANG.get(Path(name).suffix, "text")


def code(path: str, first: int, last: int | None = None, language: str | None = None, focus=None,
         font_size: float = 22, shown: str | None = None, max_lines: int = 12, cuts: dict | None = None):
    """CODE(path: first–last) of script.md: a code_panel quoting assets/source/<path>, header
    '<shown> · lines a–b' (shown_path()). <= 12 lines. 22 pt fits <= 66 characters a line, 20 pt
    <= 73: a longer line raises; cut it with cuts={file_line: 'text it ends after'} (the house '…',
    recoloured GREY; pygments would paint it pink-red) or use font_size=20 (<= 73).
    .code .header; highlight with code_span(p.code, k, "x"), line_bar(p.code, k, colour), k = file
    line - first."""
    last = first if last is None else last
    if last - first + 1 > max_lines:
        raise ValueError(f"CODE {path}: {last - first + 1} lines; never more than {max_lines} lines "
                         f"on screen (show a long file as successive windows of <= {max_lines} lines)")
    lines = excerpt(path, first, last).split("\n")
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
def term(prompt: str = P_LAPTOP_HOME, rows: int = 10, title: str | None = T_LAPTOP, width: float = 12.6,
         size: float = 22, place: bool = True) -> Terminal:
    """The house terminal: 12.6 wide, 22 pt, 65 characters a row, centred, bottom edge at BOTTOM.
    Height = rows x 0.403 + 0.85. Full width, or a 3-row strip (rows=3) under a picture."""
    t = Terminal(prompt=prompt, width=width, rows=rows, size=size, title=title)
    if place:
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
    return t


def laptop_term(rows: int = 10, prompt: str = P_LAPTOP_HOME) -> Terminal:
    return term(prompt, rows, T_LAPTOP)


def second_term(rows: int = 10, prompt: str = P_API) -> Terminal:
    """The second shell of S09/S11 ('laptop · second terminal'; P_API or P_FRONTEND)."""
    return term(prompt, rows, T_SECOND)


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


def extra_row() -> VGroup:
    """'extra' sized for a terminal row (GREY)."""
    return row_tag("extra", S.GREY)


def time_row() -> VGroup:
    """'at the time of recording' sized for a terminal row (GREY)."""
    return row_tag("at the time of recording", S.GREY)


def editor_row(s: str = "our editor; use yours") -> VGroup:
    """The GREY row tag of the sed edits (20, 30: 'our editor'; 32: use extra_row())."""
    return row_tag(s, S.GREY)


def cost_row(s: str = "this bills your project") -> VGroup:
    """The GOLD cost tag sized for a terminal row (S06's --embed line, S09's curl)."""
    return row_tag(s, COST)


def flash_tag(tg, color=None, scale: float = 1.15, run_time: float = 0.8):
    """Animation: flash a tag's words and pulse its outline. Never Indicate a whole tag: its dark
    fill floods with the text colour and the word vanishes (L09 trap)."""
    color = color or tg.text.get_color()
    return AnimationGroup(Indicate(tg.text, color=color, scale_factor=scale),
                          tg.box.animate(rate_func=there_and_back).set_stroke(width=4), run_time=run_time)


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
def your_turn() -> VGroup:
    """YELLOW '▶ your turn' tag (house size: beside a card or panel, not inside a terminal row)."""
    return tag("▶ your turn", TURN)


def extra_tag(s: str = "extra") -> VGroup:
    return tag(s, S.GREY)


def illustration_tag(s: str = "illustration") -> VGroup:
    """On every console step, browser page, key card, Swagger page (schematic; no screenshots)."""
    return tag(s, S.GREY)


def recorded_tag(s: str = "recorded") -> VGroup:
    """On every success a student sees that this machine could not produce; name the source:
    recorded_tag('recorded · rag.py:218–223')."""
    return tag(s, S.GREY)


def recording_tag(s: str = "at the time of recording") -> VGroup:
    """Beside versions, package counts, build times, chunk counts and "1.0.0" when first shown."""
    return tag(s, S.GREY)


def erratum_tag(s: str = "erratum") -> VGroup:
    """On every README/repo slip (the narration says 'a small slip' or 'a small gap')."""
    return tag(s, S.GREY)


def preview_tag(s: str = "preview") -> VGroup:
    return tag(s, S.GREY)


def editor_tag(s: str = "our editor; use yours") -> VGroup:
    """The sed edits of 20/30 (32 is extra: our fix)."""
    return tag(s, S.GREY)


def cost_tag(s: str = "this bills your project") -> VGroup:
    """The GOLD money tag: S01 (checklist), S06 (--embed), S12 (chat), S13 (agent, tuned endpoint)."""
    return tag(s, COST)


def future_cost_tag(s: str = "storage and egress bill") -> VGroup:
    """GOLD text on a GREY dashed outline: S14's future (L11) storage rule."""
    t = label(s, TAG, COST)
    ob = outline_box(t.width + 0.48, mono("|", TAG).height + 0.26, FUTURE, solid=False, fill_opacity=0)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def grey_chip(s: str, size: float = 20, mono_font: bool = False, color=S.GREY) -> VGroup:
    """A GREY chip for a short note ("not on Docker Hub → built locally"). .box .text"""
    return chip(s, color, size=size, font=MONO if mono_font else None)


def dashed_chip(s: str, color=FUTURE, size: float = 20, mono_font: bool = False) -> VGroup:
    """A dashed chip: future/elsewhere things (L11, L13–L15, the hosted deployment). .box .text"""
    t = mono(s, size, color) if mono_font else label(s, size, color)
    ob = outline_box(t.width + 0.48, mono("|", size).height + 0.24, color, solid=False)
    t.move_to(ob)
    g = VGroup(ob, t)
    g.box, g.text = ob, t
    return g


def tool_chip(s: str, size: float = 20) -> VGroup:
    """A tool as a PURPLE mono chip (never a logo): docker, gcloud, uv, pipenv, npm, uvicorn …"""
    return chip(s, TOOL, size=size, font=MONO)


def err_chip(s: str, size: float = 20, mono_font: bool = True) -> VGroup:
    """A RED error chip: err_chip('DefaultCredentialsError'), err_chip('403'). .box .text"""
    return chip(s, ERR, size=size, font=MONO if mono_font else None, fill_opacity=0.14)


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


def magnifier(glass_r: float = 0.28, color=ROUTE) -> VGroup:
    """ADC's magnifying glass (PINK: a lookup). .lens .handle"""
    lens = Circle(radius=glass_r, stroke_color=color, stroke_width=5).set_fill(color, 0.08)
    h = Line(lens.point_at_angle(-PI / 4), lens.point_at_angle(-PI / 4) + glass_r * 1.1 * np.array([1, -1, 0]),
             color=color, stroke_width=7)
    g = VGroup(lens, h)
    g.lens, g.handle = lens, h
    return g


def envelope(text: str = "JWT", env_w: float = 1.1, env_h: float = 0.7, color=LAPTOP,
             size: float = 20, sealed: bool = False) -> VGroup:
    """A small envelope (the signed JWT): opaque, flap, its name inside; .seal (a GREEN wax dot,
    in the group only when sealed=True; add_seal() puts it on). .body .flap .text .seal"""
    body = RoundedRectangle(width=env_w, height=env_h, corner_radius=0.05, stroke_color=color,
                            stroke_width=3).set_fill(S.BG, 1)
    flap = VMobject(stroke_color=color, stroke_width=3)
    flap.set_points_as_corners([[-env_w / 2 + 0.03, env_h / 2 - 0.03, 0], [0, env_h / 2 - env_h * 0.42, 0],
                                [env_w / 2 - 0.03, env_h / 2 - 0.03, 0]])
    t = label(text, size, INK).move_to([0, -env_h / 2 + 0.2, 0])
    seal = Circle(radius=0.09, stroke_width=0).set_fill(KEY, 1).move_to([0, env_h / 2 - env_h * 0.42, 0])
    g = VGroup(body, flap, t)
    if sealed:
        g.add(seal)
    g.body, g.flap, g.text, g.seal = body, flap, t, seal
    return g


def badge(email: str = SA_EMAIL, size: float = 20, color=KEY) -> VGroup:
    """The service account's ID badge: GREEN outline, a clip on top, a person-less portrait, the
    email (two lines when long). .frame .clip .text"""
    if len(email) > 30 and "@" in email:
        a, b = email.split("@", 1)
        txt = VGroup(mono(a, size, INK), mono("@" + b, size, S.GREY)).arrange(DOWN, buff=0.08)
    else:
        txt = mono(email, size, INK)
    portrait = RoundedRectangle(width=0.5, height=0.5, corner_radius=0.08, stroke_color=color,
                                stroke_width=2.5).set_fill(color, 0.15)
    gear = Circle(radius=0.12, stroke_color=color, stroke_width=3)
    portrait = VGroup(portrait, gear.move_to(portrait))
    row = VGroup(portrait, txt).arrange(RIGHT, buff=0.25)
    frame = RoundedRectangle(width=row.width + 0.5, height=row.height + 0.45, corner_radius=0.12,
                             stroke_color=color, stroke_width=3).set_fill(S.GREY_DARKER, 1)
    row.move_to(frame)
    clip = RoundedRectangle(width=0.5, height=0.16, corner_radius=0.05, stroke_color=color,
                            stroke_width=2.5).set_fill(S.BG, 1).move_to(frame.get_top())
    g = VGroup(frame, row, clip)
    g.frame, g.clip, g.text = frame, clip, txt
    return g


def key_card(fields=KEY_FIELDS, size: float = 20, color=KEY, glow: bool = False) -> VGroup:
    """The JSON key file as a card (always an `illustration`): '{', one mono row per (field, value)
    from KEY_FIELDS (zeroed ids, PLACEHOLDER), '}'. .frame .rows (dict field -> row) .private_key"""
    rows, by = VGroup(), {}
    for f, v in fields:
        r = mono(f'"{f}": "{v}",', size, INK, t2c={f'"{f}"': S.GREY})
        rows.add(r)
        by[f] = r
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    body = VGroup(mono("{", size, S.GREY), rows, mono("}", size, S.GREY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.1)
    rows.shift(RIGHT * 0.3)
    frame = RoundedRectangle(width=body.width + 0.6, height=body.height + 0.45, corner_radius=0.14,
                             stroke_color=color, stroke_width=3).set_fill(S.GREY_DARKER, 1)
    body.move_to(frame)
    g = VGroup(frame, body)
    g.frame, g.rows, g.private_key = frame, by, by.get("private_key")
    return g


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


def _columns(bw, y0, y1, t, n: int = 4) -> VGroup:
    """The building's columns, interrupted where its name sits (so no line runs through text)."""
    out_ = VGroup()
    lo, hi = t.get_bottom()[1] - 0.1, t.get_top()[1] + 0.1
    for x in np.linspace(-bw / 2 + 0.45, bw / 2 - 0.45, n):
        for a, b in ((y0, min(y1, lo)), (max(y0, hi), y1)):
            if b - a > 0.05:
                out_.add(Line([x, a, 0], [x, b, 0], color=CLOUD, stroke_width=3, stroke_opacity=0.55))
    return out_


def google_building(bw: float = 2.4, bh: float = 3.0, size: float = 20, door: bool = True,
                    meter_: bool = True, name: str = "Google Cloud", text_y: float | None = None) -> VGroup:
    """The BLUE Google building (no logo): pediment, columns, base, its name; an IAM-guarded door on
    its left wall (.door, .guard = a padlock 'IAM') and a GOLD meter (.meter). Base at y = 0 of its
    own frame. .frame .text .door .guard .meter"""
    ped_h = bh * 0.2
    base = Rectangle(width=bw, height=0.14).move_to([0, 0.07, 0])
    hall = Rectangle(width=bw - 0.3, height=bh - ped_h - 0.14).next_to(base, UP, buff=0)
    ped = Polygon([-bw / 2, bh - ped_h, 0], [0, bh, 0], [bw / 2, bh - ped_h, 0])
    for m in (base, hall, ped):
        m.set_stroke(CLOUD, 3).set_fill(CLOUD, 0.1)
    t = label(name, size, CLOUD).move_to([0, bh - ped_h - 0.3 if text_y is None else text_y, 0])
    cols_ = _columns(bw, 0.2, hall.get_top()[1] - 0.12, t)
    g = VGroup(base, hall, ped, cols_, t)
    g.frame, g.text, g.door, g.guard, g.meter = VGroup(base, hall, ped), t, None, None, None
    g.columns = cols_
    if door:
        d = door_glyph(0.36, 0.56, CLOUD).move_to([-bw / 2 + 0.15 + 0.18, 0.14 + 0.28, 0])
        lk = lock_glyph(0.26, CLOUD).next_to(d, UP, buff=0.08)
        iam = label("IAM", size, CLOUD).next_to(lk, RIGHT, buff=0.08)
        g.add(d, lk, iam)
        g.door, g.guard = d, VGroup(lk, iam)
    if meter_:
        m_ = meter().move_to([bw / 2 - 0.55, 0.55, 0])
        g.add(m_)
        g.meter = m_
    return g


def meter(meter_w: float = 0.6, color=COST) -> VGroup:
    """A GOLD meter (a dial and a needle): money. .dial .needle ; tick(scene) plays a swing."""
    r = meter_w / 2
    dial = Arc(radius=r, start_angle=0, angle=PI, color=color, stroke_width=3)
    base = Line([-r, 0, 0], [r, 0, 0], color=color, stroke_width=3)
    needle = Line(ORIGIN, r * 0.8 * np.array([np.cos(PI * 0.7), np.sin(PI * 0.7), 0]), color=color,
                  stroke_width=3)
    g = VGroup(dial, base, needle)
    g.dial, g.needle = dial, needle
    g.center_pt = Dot(ORIGIN, radius=0.001).set_opacity(0)
    g.add(g.center_pt)
    return g


def meter_tick(m: VGroup, angle: float = -0.9, run_time: float = 0.8):
    """Animation: the meter's needle swings (and stays): money is being spent."""
    from manim import Rotate
    return Rotate(m.needle, angle=angle, about_point=m.center_pt.get_center(), run_time=run_time)


class EmbeddingBars(VGroup):
    """An embedding as n thin BLUE bars of EQUAL height (256 by default: EMBEDDING_DIMENSION, rag.py:17
    and cli.py:26). Never show values: the bars carry no data. .bars"""

    def __init__(self, n: int = 256, bars_w: float = 4.0, bar_h: float = 0.5, color=CLOUD,
                 rows: int = 1, **kw):
        super().__init__(**kw)
        per = int(np.ceil(n / rows))
        dx = bars_w / per
        self.bars = VGroup()
        for i in range(n):
            r, c = divmod(i, per)
            x = -bars_w / 2 + dx * (c + 0.5)
            y = -r * (bar_h + 0.08)
            self.bars.add(Line([x, y - bar_h / 2, 0], [x, y + bar_h / 2, 0], color=color,
                               stroke_width=max(0.6, min(2.5, dx * 60))))
        self.add(self.bars)
        self.move_to(ORIGIN)

    def grow(self, run_time: float = 1.0):
        return LaggedStart(*[GrowFromEdge(b, DOWN) for b in self.bars], lag_ratio=0.004, run_time=run_time)


def riddle_card(i: int, size: float = 26) -> VGroup:
    """S01's riddle i (0-2) as a card: the code (mono, WHITE) and its question (GREY).
    .code .question .frame"""
    c, q = RIDDLES[i]
    ct = mono(c, size, INK)
    qt = label(q, size, S.GREY)
    row = VGroup(ct, qt).arrange(RIGHT, buff=0.4)
    fr = RoundedRectangle(width=row.width + 0.7, height=row.height + 0.45, corner_radius=0.14,
                          stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    row.move_to(fr)
    g = VGroup(fr, row)
    g.frame, g.code, g.question = fr, ct, qt
    return g


def riddle_label(i: int, size: float = 22) -> VGroup:
    """The small label a riddle card fades into (kept for S15's recap): the code and a '?'."""
    c, _ = RIDDLES[i]
    g = VGroup(mono(c, size, INK), label("?", size, TURN)).arrange(RIGHT, buff=0.1)
    g.code = g[0]
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


# ================================================================== V1 · the auth chain
class Ticket(VGroup):
    """The bearer token: a small BLUE ticket with a timer (it belongs to the cloud conversation).
    .frame .text .clock .life (the remaining-time arc) .minutes ('≈ 60 min', when timer=True)
    run_out(run_time) -> Animation (the arc drains); expire() -> Animation (the ticket greys)."""

    def __init__(self, ticket_w: float = 1.5, text: str = "token", size: float = 20, timer: bool = True,
                 color=CLOUD, **kw):
        super().__init__(**kw)
        h = 0.6
        fr = RoundedRectangle(width=ticket_w, height=h, corner_radius=0.08, stroke_color=color,
                              stroke_width=3).set_fill(color, 0.2)
        notches = VGroup(*[Dot(fr.get_edge_center(d), radius=0.08, color=S.BG) for d in (LEFT, RIGHT)])
        self.r = 0.16
        clock = Circle(radius=self.r, stroke_color=color, stroke_width=2.5).move_to(
            fr.get_left() + RIGHT * (0.2 + self.r))
        life = self._life(1.0, clock.get_center(), color)
        t = label(text, size, INK).next_to(clock, RIGHT, buff=0.14)
        if t.get_right()[0] > fr.get_right()[0] - 0.12:
            raise ValueError("Ticket: text too wide for ticket_w")
        self.frame, self.text, self.clock, self.life, self.color_ = fr, t, clock, life, color
        self.add(fr, notches, clock, life, t)
        self.minutes = None
        if timer:
            self.minutes = label("≈ 60 min", size, color).next_to(fr, DOWN, buff=0.1)
            self.add(self.minutes)

    def _life(self, frac, center, color):
        a = Arc(radius=self.r * 0.62, start_angle=PI / 2, angle=-2 * PI * max(frac, 0.002),
                arc_center=center, color=color, stroke_width=5)
        return a

    def run_out(self, run_time: float = 1.5):
        c, col = self.clock.get_center(), self.color_
        return UpdateFromAlphaFunc(self.life, lambda m, a: m.become(self._life(1 - a, c, col)),
                                   run_time=run_time, rate_func=linear)

    def expire(self, run_time: float = 0.5):
        return Transform(self, greyed(self), run_time=run_time)


def desk_glyph(desk_w: float = 1.3, color=CLOUD) -> VGroup:
    """Google's token desk: a counter with a little bell. .top .front"""
    top = Line([-desk_w / 2, 0, 0], [desk_w / 2, 0, 0], color=color, stroke_width=5)
    front = Rectangle(width=desk_w * 0.86, height=0.45, stroke_color=color, stroke_width=3) \
        .set_fill(color, 0.15).next_to(top, DOWN, buff=0)
    bell = VGroup(Arc(radius=0.13, start_angle=0, angle=PI, color=color, stroke_width=3),
                  Dot([0, 0.17, 0], radius=0.03, color=color)).move_to([desk_w * 0.25, 0.09, 0])
    g = VGroup(top, front, bell)
    g.top, g.front = top, front
    return g


AUTH_LINKS = ("key file", "ADC", "signed JWT", "token desk", "bearer token")
AUTH_COLORS = (KEY, ROUTE, LAPTOP, CLOUD, CLOUD)


class AuthChain(Rig):
    """V1 · the auth chain, five links left to right: GREEN key file → ADC's PINK magnifying glass →
    the signed JWT envelope (GREEN seal) → the BLUE token desk → the BLUE bearer ticket (≈ 60 min).
    12.5 × 1.85 (slot_w 2.1, gap 0.5): centre it at x = 0; never scale it.
        ch = AuthChain(teaser=True)       # S06/S09: the key slot, then four hollow unlabelled slots
        ch.break_at(scene)                # plays: the glass finds nothing at slot 0; RED cross; greys
        self.play(ch.reveal(3))           # S07: slot 3 lights (with the arrow into it)
        self.play(ch.light_all())         # S09: the whole chain lit at once
        ch.mint(scene)                    # plays: the timer runs out, a fresh ticket mints itself
    Slot states: 'lit' | 'hollow' (dashed GREY_DARK, empty) | 'grey'. .slots[i] (each .frame .glyph
    .text) .arrows[j] (slot j -> j+1) .key .glass .jwt .desk .ticket (the lit glyphs) .url (the
    desk's 'oauth2.googleapis.com/token' caption, built, not added: place it above slot 3)"""

    def __init__(self, teaser: bool = False, slot_w: float = 2.1, slot_h: float = 1.35, gap: float = 0.5,
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.slot_w, self.slot_h, self.gap, self.size = slot_w, slot_h, gap, size
        self.xs = [(i - 2) * (slot_w + gap) for i in range(5)]
        self.state = ["lit" if (i == 0 or not teaser) else "hollow" for i in range(5)]
        self.slots = VGroup(*[self._slot(i, s) for i, s in enumerate(self.state)])
        self.arrows = VGroup(*[self._arrow(j, "lit" if not teaser else "hollow") for j in range(4)])
        self.add(self.arrows, self.slots)
        self.key, self.glass, self.jwt, self.desk, self.ticket = [s.glyph for s in self.slots]
        self.url = mono(TOKEN_DESK, size, CLOUD).next_to(self.slots[3], UP, buff=0.15)
        self.ride(self.url)

    def _glyph(self, i):
        if i == 0:
            return key_glyph(1.0)
        if i == 1:
            return magnifier(0.3)
        if i == 2:
            return envelope("JWT", sealed=True)
        if i == 3:
            return desk_glyph(1.3)
        return Ticket(1.5, timer=True, size=self.size)

    def _slot(self, i, state):
        col = AUTH_COLORS[i]
        x = self.xs[i]
        if state == "hollow":
            fr = outline_box(self.slot_w, self.slot_h, S.GREY_DARK, solid=False)
        else:
            fr = outline_box(self.slot_w, self.slot_h, col if state == "lit" else S.GREY_DARK, solid=True,
                             fill_opacity=0.06 if state == "lit" else 0.0)
        fr.move_to([x, 0, 0])
        gl = self._glyph(i).move_to([x, 0.05 if i != 4 else 0.12, 0])
        tx = label(AUTH_LINKS[i], self.size, INK if state == "lit" else S.GREY)
        tx.next_to(fr, DOWN, buff=0.12)
        if state == "grey":
            gl = greyed(gl)
        if state == "hollow":
            gl.set_opacity(0)
            tx.set_opacity(0)
        g = VGroup(fr, gl, tx)
        g.frame, g.glyph, g.text = fr, gl, tx
        return g

    def _arrow(self, j, state):
        a = [self.xs[j] + self.slot_w / 2 + 0.06, 0, 0]
        b = [self.xs[j + 1] - self.slot_w / 2 - 0.06, 0, 0]
        col = {"lit": S.GREY, "hollow": S.GREY_DARK, "grey": S.GREY_DARK}[state]
        return Arrow(a, b, buff=0, color=col, stroke_width=3, tip_length=0.16,
                     max_tip_length_to_length_ratio=0.5)

    def _shift(self, m):
        """A freshly built part moved to wherever the chain now is."""
        return m.shift(self._origin())

    def _origin(self):
        return self.slots[0].frame.get_center() - np.array([self.xs[0], 0, 0])

    def to(self, i: int, state: str, run_time: float = 0.5):
        """Animation: slot i takes `state` ('lit', 'hollow', 'grey')."""
        self.state[i] = state
        return Transform(self.slots[i], self._shift(self._slot(i, state)), run_time=run_time)

    def arrow_to(self, j: int, state: str, run_time: float = 0.4):
        return Transform(self.arrows[j], self._shift(self._arrow(j, state)), run_time=run_time)

    def reveal(self, i: int, run_time: float = 0.7):
        """Animation: slot i lights, with the arrow that leads into it."""
        anims = [self.to(i, "lit", run_time)]
        if i > 0:
            anims.append(self.arrow_to(i - 1, "lit", run_time))
        return AnimationGroup(*anims)

    def light_all(self, run_time: float = 1.2):
        """Animation: every link lit, left to right."""
        anims = []
        for i in range(5):
            anims.append(AnimationGroup(self.to(i, "lit"), *([self.arrow_to(i - 1, "lit")] if i else [])))
        return LaggedStart(*anims, lag_ratio=0.25, run_time=run_time)

    def grey_out(self, run_time: float = 0.8):
        """Animation: the whole chain greys out (slots that were hollow stay hollow)."""
        anims = [self.to(i, "grey" if s != "hollow" else "hollow") for i, s in enumerate(list(self.state))]
        anims += [self.arrow_to(j, "grey") for j in range(4)]
        return AnimationGroup(*anims, run_time=run_time)

    def break_at(self, scene, i: int = 0, run_time: float = 0.6):
        """Plays: the glass looks into slot i and finds nothing: the slot's glyph fades, a RED cross
        lands on it, the whole chain greys out. Returns the cross (on the scene; fade it yourself)."""
        fr = self.slots[i].frame
        glass = magnifier(0.3).move_to(fr.get_corner(UR) + np.array([0.45, 0.35, 0]))
        scene.play(FadeIn(glass, shift=LEFT * 0.2), run_time=0.4)
        scene.play(glass.animate.move_to(fr.get_center() + np.array([0.15, 0.1, 0])), run_time=run_time)
        cross = cross_mark(0.55, ERR).move_to(fr)
        scene.play(self.slots[i].glyph.animate.set_opacity(0.15), Create(cross), run_time=0.5)
        scene.play(self.grey_out(), FadeOut(glass), run_time=0.8)
        scene.remove(glass)
        return cross

    def mint(self, scene, run_time: float = 1.6):
        """Plays: the ticket's timer runs out and it greys; a fresh ticket mints itself at the desk and
        slides into slot 4 (the chain must be lit)."""
        old = self.slots[4].glyph
        scene.play(old.run_out(run_time), run_time=run_time)
        scene.play(old.expire(), run_time=0.4)
        new = Ticket(1.5, timer=True, size=self.size).move_to(self.slots[3].frame)
        scene.play(FadeOut(old), FadeIn(new, scale=0.6), run_time=0.5)
        scene.play(new.animate.move_to(old.get_center()), run_time=0.7)
        self.slots[4].remove(old)
        scene.remove(old)
        self.slots[4].add(new)
        self.slots[4].glyph = new
        self.ticket = new

    def staple(self, n: int = 3, size: float = 20) -> VGroup:
        """n HTTPS requests, each with a small ticket stapled on and the header text (not added):
        a column, centred at the origin; place it under the chain. .rows (each .pill .ticket)"""
        rows = VGroup()
        for _ in range(n):
            t = mono("HTTPS · Authorization: Bearer …", size, INK)
            pill = RoundedRectangle(width=t.width + 0.5, height=0.5, corner_radius=0.25, stroke_color=ROUTE,
                                    stroke_width=3).set_fill(ROUTE, 0.1)
            t.move_to(pill)
            tk = Ticket(1.45, timer=False, size=size).next_to(pill, LEFT, buff=0.15)
            r = VGroup(tk, pill, t)
            r.pill, r.ticket, r.text = pill, tk, t
            rows.add(r)
        rows.arrange(DOWN, buff=0.18)
        rows.rows = rows
        return rows


ADC_PLACES = (
    (("the file named by ", "label"), (ENV_VAR, "mono"), "a service-account key · this tutorial"),
    (("gcloud auth application-default login", "mono"), None, "you, through a consent screen"),
    (("the metadata server", "label"), None, "the account attached to a VM, a Cloud Run service, a pod"),
)


class AdcPlaces(Rig):
    """V1 (S07) · the three places ADC looks, in order, as three stacked rows: (1) the file named by
    GOOGLE_APPLICATION_CREDENTIALS (GREEN) · (2) the gcloud user login (GREY) · (3) the metadata
    server (GREY dashed, chip 'L13–L15'). ~ 9.3 × 3.4 with the glass at the left.
        ap = AdcPlaces(); self.play(FadeIn(ap)); self.play(FadeIn(ap.glass))
        self.play(ap.visit(1))              # the glass walks to row 1 (0-based)
        ap.stop(scene, 0)                   # plays: the glass flashes RED on row 0
        box, anim = ap.enclose(); self.play(anim)   # a TEAL container outline closes around them
        self.play(ap.empty((1, 2)))         # rows 1 and 2 become empty boxes inside the container
    .rows[i] (each .frame .badge .title .sub) .glass .chip (the L13–L15 chip, part of row 2)"""

    def __init__(self, size: float = 20, row_h: float = 0.95, gap: float = 0.2, **kw):
        super().__init__(**kw)
        self.rows = VGroup()
        contents = []
        for i, (a, b, sub) in enumerate(ADC_PLACES):
            parts = [label(a[0], size, INK) if a[1] == "label" else mono(a[0], size, INK)]
            if b:
                parts.append(mono(b[0], size, INK))
            title = VGroup(*parts).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
            st = label(sub, size, S.GREY)
            txt = VGroup(title, st).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            contents.append(txt)
        w = max(c.width for c in contents) + 1.3
        for i, txt in enumerate(contents):
            col = KEY if i == 0 else S.GREY
            fr = outline_box(w, row_h, col, solid=i != 2, fill_opacity=0.06)
            bd = step_badge(i + 1, ROUTE)
            fr.move_to([0, -i * (row_h + gap), 0])
            bd.move_to(fr.get_left() + RIGHT * 0.42)
            txt.next_to(bd, RIGHT, buff=0.3)
            r = VGroup(fr, bd, txt)
            r.frame, r.badge, r.title, r.sub = fr, bd, txt[0], txt[1]
            self.rows.add(r)
        self.chip = dashed_chip("L13–L15").next_to(self.rows[2].frame, RIGHT, buff=0.2)
        self.rows[2].add(self.chip)
        self.add(self.rows)
        self.move_to(ORIGIN)
        self.glass = magnifier(0.3).next_to(self.rows[0].frame, LEFT, buff=0.25)
        self.ride(self.glass)

    def visit(self, i: int, run_time: float = 0.7):
        """Animation: the glass walks to row i."""
        tgt = self.glass.copy().next_to(self.rows[i].frame, LEFT, buff=0.25)
        return self.glass.animate(run_time=run_time).move_to(tgt)

    def stop(self, scene, i: int = 0, run_time: float = 0.8):
        """Plays: the glass stops at row i and flashes RED; the row's frame flashes RED."""
        scene.play(Indicate(self.glass, color=ERR, scale_factor=1.25),
                   self.rows[i].frame.frame.animate(rate_func=there_and_back).set_stroke(ERR, 5),
                   run_time=run_time)

    def enclose(self, label_text: str = "inside a container", size: float = 20):
        """(outline, Animation): a TEAL container outline closes around the rows (and the glass),
        with its label at the top-left. The outline is not added until the animation plays."""
        body = VGroup(self.rows, self.glass)
        ob = outline_box(body.width + 0.6, body.height + 0.95, IMAGE, solid=True, fill_opacity=0.04)
        ob.move_to(body).shift(UP * 0.18)
        t = label(label_text, size, IMAGE).move_to(ob.get_corner(UL) + np.array([0.2, -0.25, 0]),
                                                   aligned_edge=LEFT)
        g = VGroup(ob, t)
        return g, AnimationGroup(Create(ob.frame), FadeIn(ob.fill), FadeIn(t, shift=DOWN * 0.1))

    def empty(self, rows=(1, 2), run_time: float = 0.7):
        """Animation: rows' texts fade, leaving empty GREY boxes (nothing there in a container)."""
        anims = []
        for i in rows:
            r = self.rows[i]
            anims.append(VGroup(r.title, r.sub).animate.set_opacity(0.12))
        return AnimationGroup(*anims, run_time=run_time)


# ================================================================== V2 · the IAM grid
PRINCIPALS = ("you", SA_NAME)
RESOURCES = (PROJECT_ID, "ac215-project", "129349313346")


class IamGridRig(Rig):
    """V2 · IAM as a grid: rows = principals ('you', 'llm-service-account'), columns = resources
    ('your-gcp-project', 'ac215-project', 'project 129349313346'). ~12.9 × 3.5: centre at x = 0.
        g = IamGridRig(); self.play(FadeIn(g))
        tok = g.token("roles/aiplatform.user", PASS)                   # a role token (not added)
        self.play(g.drop(tok, 1, 0, slot=0, of=2))                     # into (SA, your project)
        self.play(g.drop(g.token("Storage Admin", S.GREY, mono_font=False), 1, 0, slot=1, of=2))
        req, mark = g.fire(scene, 1, 1, ok=False, text="embed")        # plays: request ② → 403
        self.play(g.pulse_col(2))
    A request comes from a PINK chip under its column (the resource path picks the column) and
    points up into the cell; the verdict (GREEN check, RED '403') lands in the cell's top-right.
    .heads[c] .names[r] .cells[r][c] .caps (the 'principals' / 'resources' captions)"""

    def __init__(self, principals=PRINCIPALS, resources=RESOURCES, row_h=(0.9, 1.55), size: float = 20,
                 **kw):
        super().__init__(**kw)
        self.size = size
        heads = []
        for r in resources:
            if r.isdigit():
                heads.append(VGroup(label("project", size, INK), mono(r, size, INK)).arrange(RIGHT, buff=0.1,
                                                                                         aligned_edge=DOWN))
            else:
                heads.append(mono(r, size, INK))
        names = [label(p, size, INK) if p == "you" else mono(p, size, INK) for p in principals]
        tok_w = mono("roles/aiplatform.user", size).width + 0.48
        name_w = max(n.width for n in names) + 0.25
        col_w = [max(h.width + 0.3, tok_w + 0.2 if c == 0 else 0) for c, h in enumerate(heads)]
        head_h = 0.55
        total_w = name_w + sum(col_w)
        x0 = -total_w / 2
        xs = [x0 + name_w + sum(col_w[:c]) for c in range(len(col_w))]          # left edge of each column
        y = 0.0
        self.heads = VGroup()
        for c, h in enumerate(heads):
            h.move_to([xs[c] + col_w[c] / 2, y - head_h / 2, 0])
            self.heads.add(h)
        y -= head_h
        self.cells, self.names = [], VGroup()
        for r, n in enumerate(names):
            hgt = row_h[r] if r < len(row_h) else row_h[-1]
            n.move_to([x0 + 0.1 + n.width / 2, y - hgt / 2, 0])
            self.names.add(n)
            row = []
            for c in range(len(heads)):
                cell = Rectangle(width=col_w[c], height=hgt, stroke_color=S.GREY_DARK, stroke_width=2)
                cell.move_to([xs[c] + col_w[c] / 2, y - hgt / 2, 0])
                row.append(cell)
            self.cells.append(row)
            y -= hgt
        cap_p = label("principals", size, S.GREY).move_to([x0 + 0.1, head_h / 2 + 0.05, 0], aligned_edge=LEFT)
        cap_r = label("resources", size, S.GREY).move_to([xs[0] + 0.1, head_h / 2 + 0.05, 0], aligned_edge=LEFT)
        self.caps = VGroup(cap_p, cap_r)
        self.add(self.caps, self.heads, self.names, *[c for row in self.cells for c in row])
        self.move_to(ORIGIN)

    def cell(self, r: int, c: int) -> Rectangle:
        return self.cells[r][c]

    def token(self, text: str, color=PASS, dashed: bool = False, mono_font: bool = True) -> VGroup:
        """A role token (chip; not added): token('roles/aiplatform.user'), token('Owner', S.GREY,
        mono_font=False), token('Storage Admin', S.GREY, mono_font=False)."""
        if dashed:
            return dashed_chip(text, color, self.size, mono_font)
        return chip(text, color, size=self.size, font=MONO if mono_font else None, fill_opacity=0.18)

    def slot_point(self, r: int, c: int, slot: int = 0, of: int = 1) -> np.ndarray:
        """Where token `slot` of `of` sits in cell (r, c): stacked, a little below the centre (the
        top-right corner stays free for a verdict)."""
        cell = self.cells[r][c]
        h = 0.5
        top = cell.get_center()[1] + (of * h + (of - 1) * 0.1) / 2 - 0.12
        return np.array([cell.get_center()[0], top - h / 2 - slot * (h + 0.1), 0])

    def drop(self, tok, r: int, c: int, slot: int = 0, of: int = 1, run_time: float = 0.6):
        """Animation: role token `tok` drops into cell (r, c)."""
        tok.move_to(self.slot_point(r, c, slot, of))
        return FadeIn(tok, shift=DOWN * 0.35, run_time=run_time)

    def verdict(self, r: int, c: int, ok: bool) -> VGroup:
        """The verdict mark for cell (r, c) (not added): a GREEN check or a RED '403' pill."""
        cell = self.cells[r][c]
        if ok:
            m = VGroup(check_mark(0.32, PASS))
        else:
            t = mono("403", self.size, ERR)
            b = RoundedRectangle(width=t.width + 0.3, height=0.38, corner_radius=0.19, stroke_color=ERR,
                                 stroke_width=2.5).set_fill(S.BG, 0.95)
            t.move_to(b)
            m = VGroup(b, t)
        return m.move_to(cell.get_corner(UR) + np.array([-m.width / 2 - 0.1, -m.height / 2 - 0.08, 0]))

    def fire(self, scene, r: int, c: int, ok: bool, text: str = "request", run_time: float = 0.8):
        """Plays: a PINK request chip appears under column c, its arrow points up into cell (r, c),
        the verdict lands. Returns (VGroup(chip, arrow), mark), both on the scene."""
        cell = self.cells[r][c]
        bottom = self.cells[-1][c].get_bottom()[1]
        req = chip(text, ROUTE, size=self.size, font=MONO, fill_opacity=0.15)
        req.move_to([cell.get_center()[0], bottom - 0.5, 0])
        ar = Arrow(req.get_top(), [cell.get_center()[0], cell.get_bottom()[1] + 0.12, 0], buff=0.05,
                   color=ROUTE, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=0.5)
        mark = self.verdict(r, c, ok)
        scene.play(FadeIn(req, shift=UP * 0.2), run_time=0.4)
        scene.play(Create(ar), run_time=run_time)
        flash = cell.copy().set_stroke(PASS if ok else ERR, 5)
        scene.play(FadeIn(mark, scale=1.3), FadeIn(flash), run_time=0.45)
        scene.play(FadeOut(flash), run_time=0.3)
        scene.remove(flash)
        return VGroup(req, ar), mark

    def pulse_col(self, c: int, color=TURN, run_time: float = 0.8):
        """Animation: column c's header lights and its cells' outlines pulse."""
        cells = VGroup(*[row[c] for row in self.cells])
        return AnimationGroup(Indicate(self.heads[c], color=color, scale_factor=1.1),
                              cells.animate(rate_func=there_and_back).set_stroke(color, 4), run_time=run_time)


# ================================================================== V3 · the secrets portal
def _tree(entries, size: float = 20, indent: float = 0.36, buff: float = 0.1) -> VGroup:
    """A small file tree: entries (text, colour) with two spaces of indent per level; folders end in
    '/'. Folder glyphs take the entry's colour; names are WHITE unless the colour is not GREY.
    Each row: .glyph .name_text .name .level ; the tree: .rows .row(name)"""
    rows = VGroup()
    for e, col in entries:
        depth = (len(e) - len(e.lstrip(" "))) // 2
        name = e.strip()
        is_dir = name.endswith("/")
        g = folder_glyph(0.24, col) if is_dir else file_glyph(0.3, col)
        t = mono_line(name, size, INK if col == LAPTOP else col)
        t.next_to(g, RIGHT, buff=0.14)
        g.match_y(t.strut)
        r = VGroup(g, t)
        r.glyph, r.name_text, r.name, r.level = g, t, name, depth
        rows.add(r)
    pitch = line_pitch(size) + buff
    for i, r in enumerate(rows):
        r.shift(np.array([r.level * indent - r.glyph.get_left()[0], -i * pitch - r.name_text.strut.get_top()[1], 0]))

    def row(name):
        for r in rows:
            if r.name == name:
                return r
        raise KeyError(name)
    tree = VGroup(*rows)
    tree.rows, tree.row = rows, row
    return tree


class SecretsPortalRig(Rig):
    """V3 · two filesystems, one folder. Left: the host tree AC215/ (caption 'your course folder ·
    here: ~') holding cheese-app-v0/ (llm-rag/, api-service/, frontend-ai-chatbot/) and, beside the
    repo, secrets/ (GREEN) with the key. Right: a TEAL container silhouette with /secrets/ (and the
    key file inside when it is there) and a GREY 'Google library' chip. ~12.6 × 3.6.
        sp = SecretsPortalRig(); self.play(FadeIn(sp.tree), FadeIn(sp.caption))
        ring_ = sp.climb(self)                     # plays: $(pwd) at api-service/, '..', '..', secrets/
        self.play(FadeIn(sp.box)); self.play(sp.connect())       # the GREEN tube
        sp.snap(self)                              # plays: the key flows, the env var points at the file
    key_inside=True (Ponder 1): the key sits in cheese-app-v0/secrets/ (RED), AC215/secrets/ is
    absent; climb() ends on AC215/, pop_empty(scene) plays the empty GREEN folder Docker creates,
    and the box's /secrets stays empty.
    .tree (.row(name)) .caption .box (.frame .title .mount .file .lib) .host_cap .cont_cap (GREY
    'host path' / TEAL 'container path', not added) .ghost (the popped folder, key_inside only)
    Move .tree / .box freely before connect(): the tube is built from where they are."""

    def __init__(self, key_inside: bool = False, size: float = 20, box_w: float = 5.9, **kw):
        super().__init__(**kw)
        self.size, self.key_inside = size, key_inside
        ent = [("AC215/", LAPTOP), ("  cheese-app-v0/", LAPTOP), ("    llm-rag/", LAPTOP),
               ("    api-service/", LAPTOP), ("    frontend-ai-chatbot/", LAPTOP)]
        if key_inside:
            ent += [("    secrets/", ERR), ("      llm-service-account.json", ERR), ("  secrets/", KEY)]
        else:
            ent += [("  secrets/", KEY), ("    llm-service-account.json", KEY)]
        self.tree = _tree(ent, size)
        self.tree.move_to([-6.4 + self.tree.width / 2, 0.15, 0])
        self.caption = note("your course folder · here: ~").next_to(self.tree, DOWN, buff=0.25)
        self.caption.align_to(self.tree, LEFT)
        self.ghost = self.ghost_chip = None
        if key_inside:                      # the slot where Docker will create the empty folder
            self.ghost = self.tree.rows[-1]
            self.tree.remove(self.ghost)
            self.tree.rows = VGroup(*self.tree.rows[:-1])
            self.ghost_chip = grey_chip("created by Docker, empty").next_to(self.ghost, RIGHT, buff=0.3)
        # the container silhouette
        fr = outline_box(box_w, 3.4, IMAGE, solid=True, fill_opacity=0.05)
        title = label("container", size, IMAGE)
        mount = VGroup(folder_glyph(0.24, KEY), mono_line("/secrets/", size, KEY)).arrange(RIGHT, buff=0.14)
        file_ = VGroup(file_glyph(0.3, KEY), mono_line("llm-service-account.json", size, INK)).arrange(RIGHT,
                                                                                                    buff=0.14)
        lib = grey_chip("Google library")
        fr.move_to([6.4 - box_w / 2, 0.2, 0])
        title.move_to(fr.get_corner(UL) + np.array([0.25, -0.28, 0]), aligned_edge=LEFT)
        mount.move_to(fr.get_corner(UL) + np.array([0.3, -0.85, 0]), aligned_edge=LEFT)
        file_.next_to(mount, DOWN, buff=0.15, aligned_edge=LEFT).shift(RIGHT * 0.36)
        lib.move_to(fr.get_corner(DR) + np.array([-0.25 - 0, 0.38, 0]), aligned_edge=RIGHT)
        self.box = VGroup(fr, title, mount)
        if not key_inside:
            self.box.add(file_)
        self.box.add(lib)
        self.box.frame, self.box.title, self.box.mount, self.box.file, self.box.lib = fr, title, mount, file_, lib
        self.host_cap = note("host path")
        self.cont_cap = note("container path", IMAGE)
        self.add(self.tree, self.caption, self.box)
        self.tube_mob = None
        self.ride(self.ghost, self.ghost_chip, self.host_cap, self.cont_cap,
                  self.box.file if key_inside else None)

    def cursor_on(self, name: str, color=ROUTE) -> VGroup:
        """A PINK ring around tree row `name` (not added)."""
        r = self.tree.row(name) if name != "ghost" else self.ghost
        return ring(r, color, buff=0.07)

    def climb(self, scene, start: str = "api-service/", end: str | None = None, hop_time: float = 0.6):
        """Plays: the cursor rings `start` with a PINK '$(pwd)' label, hops '..' to cheese-app-v0/,
        '..' to AC215/, then lands on `end` (default: secrets/ beside the repo, which turns GREEN; with
        key_inside, it stays on AC215/: call pop_empty()). Returns the ring (on the scene)."""
        cur = self.cursor_on(start)
        pwd = mono("$(pwd)", self.size, ROUTE).next_to(cur, RIGHT, buff=0.2)
        scene.play(Create(cur), FadeIn(pwd, shift=LEFT * 0.1), run_time=0.6)
        hops = VGroup()
        for name in ("cheese-app-v0/", "AC215/"):
            tgt = self.cursor_on(name)
            dots = mono("..", self.size, ROUTE).next_to(tgt, RIGHT, buff=0.2)
            scene.play(Transform(cur, tgt), FadeIn(dots, shift=UP * 0.15), run_time=hop_time)
            hops.add(dots)
        scene.play(FadeOut(pwd), run_time=0.3)
        scene.remove(pwd)
        end = end or (None if self.key_inside else "secrets/")
        if end:
            row = self.tree.rows[-2] if (end == "secrets/" and not self.key_inside) else self.tree.row(end)
            tgt = ring(row, ROUTE, buff=0.07)
            scene.play(Transform(cur, tgt), FadeOut(hops), run_time=hop_time)
            scene.play(cur.animate.set_stroke(KEY), Indicate(row.name_text, color=KEY, scale_factor=1.08),
                       run_time=0.6)
        else:
            scene.play(FadeOut(hops), run_time=0.3)
        scene.remove(hops)
        return cur

    def pop_empty(self, scene, run_time: float = 0.6):
        """Plays (key_inside only): the empty GREEN AC215/secrets/ folder pops into existence, with
        the GREY chip 'created by Docker, empty'. It joins .tree (row 'ghost')."""
        scene.play(FadeIn(self.ghost, scale=0.5), run_time=run_time)
        scene.play(FadeIn(self.ghost_chip, shift=LEFT * 0.15), run_time=0.4)
        self.tree.add(self.ghost)

    def tube(self, run_time: float = 0.9):
        """The GREEN glowing tube (not added) from the host secrets/ row (the popped folder with
        key_inside) to the container's /secrets/ row, built from where they are now."""
        src = self.ghost if self.key_inside else self.tree.rows[-2]
        a = src.name_text.strut.get_right() + RIGHT * 0.15
        if self.key_inside and self.ghost_chip is not None:
            a = np.array([self.ghost_chip.get_right()[0] + 0.15, a[1], 0])
        b = self.box.mount.get_left() + LEFT * 0.12
        xm = max(a[0] + 0.2, (max(r.get_right()[0] for r in self.tree.rows) + self.box.frame.get_left()[0]) / 2)
        pts = [a, np.array([xm, a[1], 0]), np.array([xm, b[1], 0]), b]
        core = VMobject(stroke_color=KEY, stroke_width=5).set_points_as_corners(pts)
        glow = core.copy().set_stroke(KEY, 16, opacity=0.18)
        g = VGroup(glow, core)
        g.core = core
        return g

    def connect(self, run_time: float = 0.9):
        """Animation: the tube draws (stored as .tube_mob)."""
        self.tube_mob = self.tube()
        return Create(self.tube_mob, run_time=run_time)

    def env_label(self) -> VGroup:
        """GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json, two mono rows (not
        added), placed inside the box under its file row."""
        g = VGroup(mono(ENV_VAR + "=", self.size, ROUTE), mono(KEY_PATH, self.size, ROUTE))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        g.move_to(self.box.frame.get_left() + RIGHT * (0.2 + g.width / 2)).set_y(
            self.box.file.get_y() - 0.85)
        return g

    def snap(self, scene, run_time: float = 0.8):
        """Plays: a GREEN dot runs through the tube (the folder is shared), the env var appears in
        the box and a PINK pointer snaps from it onto the key file (or the empty /secrets/), and the
        Google library chip reads it. Returns VGroup(label, pointer) on the scene."""
        if getattr(self, "tube_mob", None) is None:
            scene.play(self.connect())
        dot = Dot(self.tube_mob.core.get_start(), radius=0.09, color=KEY)
        scene.play(FadeIn(dot), run_time=0.2)
        scene.play(MoveAlongPath(dot, self.tube_mob.core), run_time=run_time)
        scene.play(FadeOut(dot), run_time=0.2)
        scene.remove(dot)
        lab = self.env_label()
        scene.play(FadeIn(lab, shift=RIGHT * 0.3), run_time=0.6)
        tgt = self.box.file if not self.key_inside else self.box.mount
        ptr = Arrow(lab[1].get_right() + RIGHT * 0.05, tgt.get_right() + RIGHT * 0.15, buff=0.05, color=ROUTE,
                    stroke_width=3, tip_length=0.16, path_arc=1.2, max_tip_length_to_length_ratio=0.3)
        scene.play(Create(ptr), run_time=0.6)
        scene.play(Indicate(self.box.lib.text, color=INK, scale_factor=1.15),
                   self.box.lib.box.animate(rate_func=there_and_back).set_stroke(width=4), run_time=0.7)
        return VGroup(lab, ptr)


# ================================================================== V4 · one server, two addresses
class TwoArrows(Rig):
    """V4 (S10) · one Chroma box, two arrows in. Above: the PINK llm-rag-network street with the
    loader and chroma houses; the loader dials `llm-rag-chromadb:8000` along the street (PINK).
    Below: the laptop floor with your browser; it rings `localhost:8000` (GREY) through the wall
    door '8000→8000'. ~7.6 × 3.9 (pair it with a CODE panel above/below or beside a 3-row strip).
        ta = TwoArrows(); self.play(FadeIn(ta))
        self.play(ta.dial())               # the PINK arrow + its label
        self.play(ta.ring_())              # the GREY arrow through the door + its label
    .street .loader .chroma .wall .door .browser .pink (+ .pink_text) .grey (+ .grey_text): the two
    arrows and their labels are built, not added (dial() / ring_() draw them)."""

    def __init__(self, size: float = 20, **kw):
        super().__init__(**kw)
        band = outline_box(6.6, 0.36, ROUTE, solid=True, fill_opacity=0.15).move_to([0, 0.13, 0])
        sname = mono(STREETS["llm-rag"], size, ROUTE).move_to(band)
        mask = RoundedRectangle(width=sname.width + 0.2, height=0.3, corner_radius=0.08, stroke_width=0) \
            .set_fill(S.BG, 0.85).move_to(sname)
        self.street = VGroup(band, mask, sname)
        self.loader = house("loader", 1.4, lit=True).move_to([-2.2, 0.31, 0], aligned_edge=DOWN)
        self.chroma = house("chroma", 1.4, lit=True).move_to([1.8, 0.31, 0], aligned_edge=DOWN)
        wall_y = -0.5
        gap = 0.4
        self.wall = VGroup(Line([-3.6, wall_y, 0], [1.8 - gap / 2, wall_y, 0], color=S.GREY, stroke_width=3),
                           Line([1.8 + gap / 2, wall_y, 0], [3.6, wall_y, 0], color=S.GREY, stroke_width=3))
        d = door_glyph().move_to([1.8, wall_y, 0])
        dl = mono("8000→8000", size, DOOR).next_to(d, RIGHT, buff=0.15).shift(DOWN * 0.38)
        self.door = VGroup(d, dl)
        self.door.glyph, self.door.text = d, dl
        self.browser = browser_glyph().move_to([-2.2, -1.45, 0])
        floor = note("your laptop").move_to([-3.6, -0.8, 0], aligned_edge=LEFT)
        self.floor_text = floor
        self.add(self.street, self.loader, self.chroma, self.wall, self.door, self.browser, floor)
        y = 0.31 + 0.27
        self.pink = Arrow([-1.45, y, 0], [1.05, y, 0], buff=0, color=ROUTE, stroke_width=4, tip_length=0.2)
        self.pink_text = mono(CHROMA_DNS, size, ROUTE).move_to([-0.2, 1.45, 0])
        win = self.browser.window
        self.grey = _poly([win.get_right() + RIGHT * 0.05, [1.8, -1.2, 0], [1.8, 0.28, 0]], S.GREY, 4)
        self.grey_text = mono("localhost:8000", size, S.GREY).move_to([0.1, -1.75, 0])
        self.ride(self.pink, self.pink_text, self.grey, self.grey_text)
        self.move_to(ORIGIN)

    def dial(self, run_time: float = 0.9):
        """Animation: the loader's PINK arrow along the street + 'llm-rag-chromadb:8000'."""
        return AnimationGroup(Create(self.pink), FadeIn(self.pink_text, shift=DOWN * 0.1), run_time=run_time)

    def ring_(self, run_time: float = 1.0):
        """Animation: the browser's GREY arrow through the door + 'localhost:8000'."""
        return AnimationGroup(Create(self.grey), FadeIn(self.grey_text, shift=UP * 0.1), run_time=run_time)


class PortDoor(Rig):
    """V4 (S11) · slide 9's tunnel with this app's numbers: a wall with a door labelled
    '3200→3000'; left, the laptop side with your browser; right, a TEAL container with its Next
    server listening on 3000. ~10.4 × 2.6.
        pd = PortDoor("3200", "3000", "frontend"); self.play(FadeIn(pd))
        pd.tunnel(self)                    # plays: a '3200' chip rides in, becomes '3000' at the door
        self.play(pd.brick())              # the 127.0.0.1: narrowing bricks the door up
    .wall .door (.glyph .text) .left_text .browser .house .ear (the server's '3000' sign)"""

    def __init__(self, host: str = "3200", cont: str = "3000", name: str = "frontend", size: float = 22, **kw):
        super().__init__(**kw)
        self.host, self.cont, self.size = host, cont, size
        gap = 0.6
        self.wall = VGroup(Line([0, -1.3, 0], [0, -gap / 2, 0], color=S.GREY, stroke_width=5),
                           Line([0, gap / 2, 0], [0, 1.3, 0], color=S.GREY, stroke_width=5))
        d = door_glyph(0.44, gap).move_to(ORIGIN)
        dt = mono(f"{host}→{cont}", size, DOOR).next_to(self.wall, UP, buff=0.15)
        self.door = VGroup(d, dt)
        self.door.glyph, self.door.text = d, dt
        self.left_text = label("your laptop", 20, S.GREY).move_to([-3.0, 1.1, 0])
        self.right_text = label("container", 20, IMAGE).move_to([3.0, 1.1, 0])
        self.browser = browser_glyph().move_to([-4.3, -0.2, 0])
        self.house = house(name, 1.6, lit=True).move_to([3.9, -0.6, 0], aligned_edge=DOWN)
        self.ear = chip(f"listens on {cont}", IMAGE, size=20).next_to(self.house, DOWN, buff=0.15)
        self.add(self.wall, self.door, self.left_text, self.right_text, self.browser, self.house, self.ear)
        self.move_to(ORIGIN)

    def tunnel(self, scene, run_time: float = 2.2):
        """Plays: a GREY '<host>' chip leaves the browser, rides to the door, morphs into a TEAL
        '<cont>' chip as it passes, and reaches the house. Returns the chip (on the scene)."""
        start = self.browser.get_right() + RIGHT * 0.6
        a = chip(self.host, S.GREY, size=self.size, font=MONO).move_to(start)
        b = chip(self.cont, IMAGE, size=self.size, font=MONO).move_to(self.door.glyph.get_center() + RIGHT * 0.9)
        path = Line(start, self.door.glyph.get_center() + LEFT * 0.7)
        trail = DashedLine(start, self.house.get_left() + LEFT * 0.1, color=ROUTE, stroke_width=3)
        scene.play(FadeIn(a, scale=0.8), Create(trail), run_time=0.5)
        scene.play(MoveAlongPath(a, path), run_time=run_time * 0.4, rate_func=linear)
        scene.play(ReplacementTransform(a, b), run_time=run_time * 0.3)
        scene.play(b.animate.move_to(self.house.get_left() + LEFT * (b.width / 2 + 0.2)),
                   run_time=run_time * 0.3)
        self.trail = trail
        return b

    def brick(self, run_time: float = 0.6):
        """Animation: bricks fill the door (the 127.0.0.1: prefix closes this side)."""
        br = bricks(0.44, 0.6).move_to(self.door.glyph)
        self.bricks = br
        return LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in br], lag_ratio=0.05, run_time=run_time)


PORT_BANDS = (("0–1023", "system", ("22", "80", "443")),
              ("1024–49151", "registered · pick yours here", ("3000", "3200", "8000", "9000")),
              ("49152–65535", "dynamic", ()))


class PortLine(Rig):
    """V4 (S11) · the 0–65535 number line in three bands (schematic widths, not to scale): system
    (22, 80, 443) · registered, pick yours here (3000, 3200, 8000, 9000) · dynamic (a throw-away port
    the OS picks for each outgoing call). ~12.4 × 2.4.
        pl = PortLine(); self.play(FadeIn(pl))
        self.play(pl.drop(1))                # the band's port chips drop in (band 0, 1)
        self.play(FadeIn(pl.dynamic_note))
    .bands[i] (each .bar .range .name) .chips[i] (port chips, not added) .dynamic_note (not added)"""

    def __init__(self, line_w: float = 12.4, size: float = 20, **kw):
        super().__init__(**kw)
        widths = (2.6, 5.8, 4.0)
        x = -line_w / 2
        unit = line_w / sum(widths)
        self.bands, self.chips = VGroup(), []
        cols_ = (S.GREY, TURN, S.GREY)
        for (rng, name, ports), w, col in zip(PORT_BANDS, widths, cols_):
            bw = w * unit
            bar = Rectangle(width=bw - 0.06, height=0.3, stroke_color=col, stroke_width=2.5) \
                .set_fill(col, 0.18).move_to([x + bw / 2, 0, 0])
            r = mono(rng, size, INK).next_to(bar, UP, buff=0.15)
            n = label(name, size, col if col != S.GREY else S.GREY).next_to(r, UP, buff=0.1)
            band = VGroup(bar, r, n)
            band.bar, band.range, band.name = bar, r, n
            self.bands.add(band)
            ch = VGroup(*[chip(p, col if col != S.GREY else S.GREY, size=size, font=MONO) for p in ports])
            if len(ch):
                ch.arrange(RIGHT, buff=0.15).next_to(bar, DOWN, buff=0.25)
            self.chips.append(ch)
            x += bw
        self.ends = VGroup(mono("0", size, S.GREY).next_to(self.bands[0].bar, LEFT, buff=0.1),
                           mono("65535", size, S.GREY).next_to(self.bands[2].bar.get_corner(DR), DOWN, buff=0.1))
        self.ends[1].align_to(self.bands[2].bar, RIGHT)
        self.dynamic_note = VGroup(label("a throw-away port the OS picks", size, S.GREY),
                                   label("for each outgoing call", size, S.GREY)).arrange(DOWN, buff=0.08)
        self.dynamic_note.next_to(self.bands[2].bar, DOWN, buff=0.25)
        self.add(self.bands, self.ends[0])
        self.ride(*[c for c in self.chips if len(c)], self.dynamic_note, self.ends[1])
        self.move_to(ORIGIN)

    def drop(self, i: int, run_time: float = 0.8):
        """Animation: band i's port chips drop in (LaggedStart)."""
        return LaggedStart(*[FadeIn(c, shift=DOWN * 0.3) for c in self.chips[i]], lag_ratio=0.2,
                           run_time=run_time)

    def note_in(self, run_time: float = 0.6):
        """Animation: the dynamic band's note and the '65535' end label appear."""
        return AnimationGroup(FadeIn(self.dynamic_note, shift=UP * 0.1), FadeIn(self.ends[1]), run_time=run_time)


# ================================================================== V5 · the browser integrates; the CORS bouncer
GUEST_LIST = (("the course's hosted site", "label"), ("http://localhost:3200", "mono"))   # compose :26
CALLS = {1: "GET :9000/rag/embedding", 2: "POST :8000/…/query", 3: "POST :9000/rag/llm-response"}


class CorsBouncer(Rig):
    """V5 (S12; S01 teaser) · one chat question as three PINK calls from your browser. Left: the
    page (address localhost:3200) and the bouncer at the browser's edge (CORS is enforced by the
    browser). Right: the API's door :9000 (guest list '*') and Chroma's door :8000 with its two-line
    guest list, which never travels; top right, Google's building for call ①. ~12.8 × 4.0.
        cb = CorsBouncer(); self.play(FadeIn(cb))
        cb.send(self, 1); cb.cloud(self)                 # ① to :9000, ticket to Google, 256 bars back
        ok = cb.preflight(self)                          # OPTIONS + Origin stamp; a pass, or nothing
        cb.admit(self) if ok else cb.refuse(self)        # ② through (10 chunks back) / stopped RED
        cb.send(self, 3)                                 # ③ question + chunks to :9000
        cb.never_sent(self); cb.curl_walk(self)          # the :3300 replay pieces
    .page (.url) .bouncer .api .chroma .doors{9000, 8000} .guest (the card) .api_list ('*') .google
    .routes{k} .captions{k} (built, not added) .pass_ (the last pass, after preflight)"""

    def __init__(self, origin: str = "3200", size: float = 20, **kw):
        super().__init__(**kw)
        self.size, self.origin = size, origin
        self.page = browser_glyph(f"localhost:{origin}", glyph_w=2.6, name="your browser", glyph_h=1.9)
        self.page.move_to([-5.05, 0.15, 0])
        self.bouncer = VGroup(person_icon(S.GREY, 0.7), label("bouncer", size, S.GREY))
        self.bouncer.arrange(DOWN, buff=0.1).move_to([-3.05, -1.25, 0])
        self.api = house("API", 1.4, lit=True).move_to([1.4, 0.75, 0], aligned_edge=DOWN)
        self.chroma = house("chroma", 1.4, lit=True).move_to([1.4, -1.55, 0], aligned_edge=DOWN)
        d9 = door_glyph().next_to(self.api, LEFT, buff=0.12).align_to(self.api, DOWN)
        d8 = door_glyph().next_to(self.chroma, LEFT, buff=0.12).align_to(self.chroma, DOWN)
        self.doors = {"9000": VGroup(d9, mono(":9000", size, DOOR).next_to(d9, DOWN, buff=0.1)),
                      "8000": VGroup(d8, mono(":8000", size, DOOR).next_to(d8, DOWN, buff=0.1))}
        rows = VGroup(*[label(s, size, INK) if k == "label" else mono(s, size, INK) for s, k in GUEST_LIST])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fr = RoundedRectangle(width=rows.width + 0.45, height=rows.height + 0.35, corner_radius=0.1,
                              stroke_color=IMAGE, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        rows.move_to(fr)
        self.guest = VGroup(fr, rows).next_to(self.chroma, RIGHT, buff=0.2)
        self.guest.rows = rows
        star = mono("*", 26, INK)
        sfr = RoundedRectangle(width=0.6, height=0.5, corner_radius=0.1, stroke_color=IMAGE,
                               stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        self.api_list = VGroup(sfr, star.move_to(sfr)).next_to(self.api, RIGHT, buff=0.2)
        self.google = google_building(2.1, 1.3, door=False, meter_=False).move_to([5.15, 0.75, 0],
                                                                                  aligned_edge=DOWN)
        self.add(self.page, self.bouncer, self.api, self.chroma, *self.doors.values(), self.guest,
                 self.api_list, self.google)
        self.routes, self.captions = {}, {}
        for k in (1, 2, 3):
            self._build_route(k)
        self.ride(*self.routes.values(), *self.captions.values())
        self.pass_ = None

    @property
    def _starts(self):
        edge = self.page.window.get_right()
        return {"up": edge + np.array([0.05, 0.25, 0]), "down": edge + np.array([0.05, -0.3, 0])}

    def _build_route(self, k, dashed: bool = False, color=ROUTE):
        if k == 2:
            a, b = self._starts["down"], self.doors["8000"][0].get_left() + LEFT * 0.05
            r = _poly([a, [a[0] + 0.9, b[1], 0], b], color, 4, dashed=dashed)
            cap = mono(CALLS[2], self.size, color).move_to([(a[0] + b[0]) / 2 + 0.75, b[1] - 0.62, 0])
        else:
            a, b = self._starts["up"], self.doors["9000"][0].get_left() + LEFT * 0.05
            if k == 3:                                   # beside route 1, not on top of it
                a = a + DOWN * 0.22
            r = _poly([a, b], color, 4, dashed=dashed)
            cap = mono(CALLS[k], self.size, color).move_to([(a[0] + b[0]) / 2, b[1] + 0.85, 0])
        self.routes[k], self.captions[k] = r, cap
        return r

    def landing(self) -> np.ndarray:
        """Where replies land in the page (under its address)."""
        w = self.page.window
        return w.get_center() + DOWN * 0.3

    def packet(self, k: int) -> VGroup:
        """The numbered PINK packet of call k (a badge; not added)."""
        return step_badge(k, ROUTE)

    def send(self, scene, k: int, run_time: float = 1.0):
        """Plays: route k draws with its caption; packet k rides to its door; the house flashes.
        Returns the packet (on the scene, at the door)."""
        r, cap = self.routes[k], self.captions[k]
        if k == 3 and self.captions.get(1) in scene.mobjects:
            scene.play(FadeOut(self.captions[1]), run_time=0.3)
        p = self.packet(k).move_to(r.path.get_start())
        drawn = r in scene.mobjects                     # preflight() may have drawn route 2 already
        anims = [] if drawn else [Create(r)]
        if cap not in scene.mobjects:
            anims.append(FadeIn(cap, shift=DOWN * 0.1))
        scene.play(*anims, FadeIn(p, scale=0.6), run_time=0.6)
        scene.play(MoveAlongPath(p, r.path), run_time=run_time)
        tgt = self.api if k != 2 else self.chroma
        scene.play(Indicate(tgt.text, color=INK, scale_factor=1.2), run_time=0.5)
        return p

    def cloud(self, scene, run_time: float = 1.0):
        """Plays (after send 1): a BLUE ticket rides from the API to Google; 256 equal BLUE bars come
        back to the API and on to the browser. Returns the bars (on the scene, at the browser)."""
        tk = Ticket(1.45, timer=False).move_to(self.api.get_top() + UP * 0.3)
        to = self.google.frame.get_left() + RIGHT * 0.2
        scene.play(FadeIn(tk, shift=UP * 0.1), run_time=0.3)
        scene.play(tk.animate.move_to(to + UP * 0.35), run_time=run_time * 0.6)
        scene.play(FadeOut(tk), run_time=0.2)
        scene.remove(tk)
        bars = EmbeddingBars(256, 1.6, 0.35).move_to(to + UP * 0.35)
        scene.play(bars.grow(0.6))
        scene.play(bars.animate.move_to(self.api.get_top() + UP * 0.35), run_time=run_time * 0.5)
        scene.play(bars.animate.move_to(self.landing()), run_time=run_time * 0.7)
        return bars

    def preflight(self, scene, origin: str | None = None, run_time: float = 1.0) -> bool:
        """Plays: an OPTIONS knock carrying the page's Origin stamp rides route 2 to door 8000;
        Chroma checks the stamp against its guest list (a line lights GREEN, or the card flashes
        RED) and sends back a one-origin pass (GREEN pill, to the bouncer) or nothing (a RED
        dashed ring at the bouncer). Returns True when a pass came back (.pass_ holds it)."""
        origin = origin or self.origin
        allowed = f"http://localhost:{origin}" == GUEST_LIST[1][0]
        r = self.routes[2]
        if r not in scene.mobjects:
            scene.play(Create(r), run_time=0.5)
        knock = VGroup(mono("OPTIONS", self.size, ROUTE), mono(f"Origin: :{origin}", self.size, INK))
        knock.arrange(DOWN, buff=0.06)
        kfr = RoundedRectangle(width=knock.width + 0.3, height=knock.height + 0.2, corner_radius=0.1,
                               stroke_color=ROUTE, stroke_width=2.5).set_fill(S.BG, 0.95)
        kn = VGroup(kfr, knock.move_to(kfr)).move_to(r.path.get_start() + RIGHT * 0.9 + DOWN * 0.1)
        scene.play(FadeIn(kn, shift=RIGHT * 0.2), run_time=0.4)
        end = self.doors["8000"][0].get_left() + LEFT * (kn.width / 2 + 0.1)
        scene.play(kn.animate.move_to(end), run_time=run_time)
        line = self.guest.rows[1]
        if allowed:
            scene.play(Indicate(line, color=PASS, scale_factor=1.1), run_time=0.6)
            ps = chip(f"localhost:{origin}", PASS, size=self.size, font=MONO, fill_opacity=0.2).move_to(end)
            scene.play(FadeOut(kn), FadeIn(ps), run_time=0.4)
            scene.play(ps.animate.next_to(self.bouncer, RIGHT, buff=0.15), run_time=run_time)
            self.pass_ = ps
        else:
            scene.play(self.guest[0].animate(rate_func=there_and_back).set_stroke(ERR, 5), run_time=0.6)
            scene.play(FadeOut(kn), run_time=0.4)
            nothing = ring(VGroup(Dot(radius=0.2)).next_to(self.bouncer, RIGHT, buff=0.3), ERR, buff=0.15,
                           dashed=True)
            scene.play(Create(nothing), run_time=0.5)
            self.pass_ = nothing
        scene.remove(kn)
        return allowed

    def admit(self, scene, run_time: float = 1.0):
        """Plays (after a pass): the bouncer compares pass and stamp (GREEN check) and waves packet ②
        through route 2; ten chunk cards come back to the browser. Returns the chunks (on the scene)."""
        ok = check_mark(0.35, PASS).next_to(self.bouncer[0], UP, buff=0.1)
        scene.play(Create(ok), run_time=0.4)
        p = self.send(scene, 2, run_time)
        chunks = VGroup(*[RoundedRectangle(width=0.36, height=0.22, corner_radius=0.04, stroke_color=S.GREY,
                                           stroke_width=2).set_fill(S.GREY, 0.35) for _ in range(10)])
        chunks.arrange_in_grid(rows=2, buff=0.06).move_to(self.chroma.get_left() + LEFT * 1.0)
        scene.play(FadeOut(p), FadeIn(chunks), run_time=0.4)
        scene.remove(p)
        scene.play(chunks.animate.move_to(self.landing()), FadeOut(ok),
                   *([FadeOut(self.pass_)] if self.pass_ is not None else []), run_time=run_time)
        scene.remove(ok)
        return chunks

    def refuse(self, scene, run_time: float = 0.8):
        """Plays (no pass): packet ② turns RED at the bouncer and goes nowhere (a RED cross)."""
        p = self.packet(2).move_to(self._starts["down"] + RIGHT * 0.3)
        scene.play(FadeIn(p, scale=0.6), run_time=0.3)
        x = cross_mark(0.4, ERR).next_to(self.bouncer[0], UP, buff=0.1)
        scene.play(p.animate.set_color(ERR), Create(x), run_time=run_time)
        self.stopped = VGroup(p, x)
        return self.stopped

    def never_sent(self, scene, run_time: float = 0.8):
        """Plays: route ③ drawn GREY dashed with the caption 'awaits call 2 · ChatComponent.jsx:163–171'."""
        r = self._build_route(3, dashed=True, color=S.GREY)
        cap = note("awaits call 2 · ChatComponent.jsx:163–171").move_to(self.captions[3])
        self.captions[3] = cap
        old = [self.captions[1]] if self.captions[1] in scene.mobjects else []
        if old:
            scene.play(FadeOut(*old), run_time=0.3)
            scene.remove(*old)
        scene.play(Create(r), FadeIn(cap), run_time=run_time)
        return VGroup(r, cap)

    def curl_walk(self, scene, run_time: float = 1.4):
        """Plays: a curl figure walks straight to door 8000 along the bottom, past no bouncer, and an
        answer comes back. Returns the figure (on the scene)."""
        fig = VGroup(person_icon(S.GREY, 0.55), mono("curl", self.size, TOOL)).arrange(RIGHT, buff=0.12)
        y = self.chroma.get_bottom()[1] - 0.6
        fig.move_to([self.bouncer.get_right()[0] + 1.2, y, 0])
        scene.play(FadeIn(fig, shift=RIGHT * 0.2), run_time=0.4)
        door = self.doors["8000"][0]
        scene.play(fig.animate.move_to([door.get_left()[0] - fig.width / 2 - 0.5, y, 0]),
                   run_time=run_time)
        ans = Dot(door.get_center(), radius=0.09, color=INK)
        scene.play(FadeIn(ans), run_time=0.2)
        scene.play(ans.animate.move_to(fig.get_right() + RIGHT * 0.15), run_time=0.6)
        self.curl_fig = VGroup(fig, ans)
        return self.curl_fig

    def restamp(self, origin: str, run_time: float = 0.6):
        """Animation: the page is now served from localhost:<origin>: the address cross-fades in
        place (old out, new in; the URL stays the same mobject inside .page)."""
        self.origin = origin
        url = self.page.url
        old = url.copy()
        new = mono(f"localhost:{origin}", self.size, S.GREY).move_to(url)

        def swap(m, a):
            src, f = (old if a < 0.5 else new), abs(1 - 2 * a)
            c = src.copy()
            for g, g0 in zip(c.family_members_with_points(), src.family_members_with_points()):
                g.set_fill(opacity=g0.get_fill_opacity() * f).set_stroke(opacity=g0.get_stroke_opacity() * f)
            m.become(c)
        return UpdateFromAlphaFunc(url, swap, run_time=run_time)


class PacketReplay(CorsBouncer):
    """V5 (S12 ponder answer) · the CorsBouncer replayed from another origin (default :3300):
        pr = PacketReplay("3300"); self.play(FadeIn(pr)); pr.replay(self)
    replay() plays: ① to :9000 with a GREEN check (the API's list is '*'), the OPTIONS knock to
    :8000 comes back with no pass, the bouncer stops ② (RED), ③ is never sent (GREY dashed), and a
    curl figure walks straight to door 8000. Each step is also a CorsBouncer method."""

    def __init__(self, origin: str = "3300", size: float = 20, **kw):
        super().__init__(origin, size, **kw)

    def replay(self, scene):
        p = self.send(scene, 1, run_time=0.8)
        ok = check_mark(0.32, PASS).next_to(self.api_list, UP, buff=0.1)
        scene.play(Create(ok), Indicate(self.api_list[1], color=PASS), run_time=0.6)
        self.preflight(scene)
        self.refuse(scene)
        self.never_sent(scene)
        self.curl_walk(scene)
        return VGroup(p, ok)


# ================================================================== V6 · the running map
HOUSE_STREET = {"chroma": "llm-rag", "loader": "llm-rag", "frontend": "cheese-app", "api": "cheese-app"}
HOUSE_NAMES = {"chroma": "chroma", "loader": "loader", "frontend": "frontend", "api": "API"}
DOOR_HOUSE = {"8000": "chroma", "3200": "frontend", "9000": "api"}
# the map at the START of each scene (script.md 'V6, the running map'; scenes add their own piece)
MAP_AT = {
    "S01": {}, "S02": {}, "S03": {}, "S04": {},
    "S05": dict(drawer=True),
    "S06": dict(drawer=True, tubes=("loader",), laid=("llm-rag", "cheese-app"), lit=("chroma",)),
    "S07": dict(drawer=True, tubes=("loader",), laid=("llm-rag", "cheese-app"), lit=("chroma",), doors=("8000",)),
    "S08": dict(drawer=True, tubes=("loader",), laid=("llm-rag", "cheese-app"), lit=("chroma",), doors=("8000",)),
    "S09": dict(drawer=True, tubes=("loader",), laid=("llm-rag", "cheese-app"), lit=("chroma",), doors=("8000",)),
    "S10": dict(drawer=True, tubes=("loader", "api"), laid=("llm-rag", "cheese-app"), lit=("chroma", "api"),
                doors=("8000", "9000")),
    "S11": dict(drawer=True, tubes=("loader", "api"), laid=("llm-rag", "cheese-app"), lit=("chroma", "api"),
                doors=("8000", "9000")),
    "S12": dict(drawer=True, tubes=("loader", "api"), laid=("llm-rag", "cheese-app"),
                lit=("chroma", "api", "frontend"), doors=("8000", "9000", "3200")),
    "S13": dict(drawer=True, tubes=("loader", "api"), laid=("llm-rag", "cheese-app"),
                lit=("chroma", "api", "frontend"), doors=("8000", "9000", "3200")),
    "S14": dict(drawer=True, tubes=("loader", "api"), laid=("llm-rag", "cheese-app"),
                lit=("chroma", "api", "frontend"), doors=("8000", "9000", "3200")),
    "S15": dict(drawer=True, tubes=("api",), laid=("cheese-app",), gone=("chroma", "loader"), folder=True),
}


class AppMap(Rig):
    """V6 · the running map (this episode's gate table). A GREY laptop frame ('your laptop'); inside
    it two streets (llm-rag-network, cheese-app-network: GREY dashed 'planned', solid PINK once
    created) with four TEAL houses (chroma + loader | frontend + API: hollow until their container
    runs); the inner wall with the published doors (8000→8000, 3200→3000, 9000→9000, neutral GREY);
    the laptop floor with your browser and the laptop's own loopback ('localhost · 127.0.0.1'); the
    GREEN secrets/ drawer (top) with tubes into the loader and API; across the public street, the
    BLUE Google building with its IAM-guarded door and a GOLD meter. 12.75 × 4.05: centre it at
    (0, 0.75) above a 3-row strip, never scale it.
        m = AppMap.at("S05")                       # the map as it stands when S05 starts
        self.play(FadeIn(m)); self.play(m.lay("cheese-app")); self.play(m.light("chroma"))
        self.play(m.open_door("8000")); self.play(Create(m.call("browser", "api")))
    Flags: laid=(streets), lit=(houses), doors=(ports), drawer, tubes=(houses), gone=(houses not on
    the map), folder (the GREEN docker-volumes folder where chroma stood). Parts not shown yet are
    built anyway (FadeIn them, or use the methods). Move the map before it plays: the unshown parts
    follow shift/move_to/next_to.
    .frame .header .streets{k} (.band .mask .text) .houses{k} .wall .doors{port} (.glyph .text)
    .browser .loop .drawer .tubes{k} .public .google (.door .guard .meter) .folder"""

    def __init__(self, laid=(), lit=(), doors=(), drawer: bool = False, tubes=(), gone=(), folder: bool = False,
                 size: float = 20, **kw):
        super().__init__(**kw)
        self.size = size
        L, R, B, T = -6.4, 2.6, -2.0, 2.05
        self.frame = RoundedRectangle(width=R - L, height=T - B, corner_radius=0.2, stroke_color=LAPTOP,
                                      stroke_width=3).set_fill(LAPTOP, 0.04).move_to([(L + R) / 2, (B + T) / 2, 0])
        self.header = label("your laptop", size, LAPTOP).move_to([L + 0.2, 1.77, 0], aligned_edge=LEFT)
        # streets and houses
        self.street_state = {}
        self.streets = {}
        spans = {"llm-rag": (-6.1, -2.35), "cheese-app": (-2.05, 2.3)}
        for k, (a, b) in spans.items():
            self.streets[k] = self._street(k, a, b, k in laid)
            self.street_state[k] = "laid" if k in laid else "planned"
        xs = {"chroma": -5.1, "loader": -3.25, "frontend": -1.0, "api": 1.25}
        self.house_x = xs
        self.houses = {k: house(HOUSE_NAMES[k], 1.25 if HOUSE_STREET[k] == "llm-rag" else 1.3, lit=k in lit)
                       .move_to([x, 0.31, 0], aligned_edge=DOWN) for k, x in xs.items()}
        # the inner wall with door gaps under chroma, frontend, api
        wy, gap = -0.45, 0.42
        gaps = sorted(xs[DOOR_HOUSE[p]] for p in DOOR_HOUSE)
        segs, x0 = [], L
        for gx in gaps:
            segs.append(Line([x0, wy, 0], [gx - gap / 2, wy, 0], color=S.GREY_DARK, stroke_width=3))
            x0 = gx + gap / 2
        segs.append(Line([x0, wy, 0], [R, wy, 0], color=S.GREY_DARK, stroke_width=3))
        self.wall = VGroup(*segs)
        self.doors = {}
        for p, h in DOOR_HOUSE.items():
            d = door_glyph().move_to([xs[h], wy, 0])
            hp, cp = PORTS[p]
            t = mono(f"{hp}→{cp}", size, DOOR).next_to(d, DOWN, buff=0.12)
            g = VGroup(d, t)
            g.glyph, g.text = d, t
            self.doors[p] = g
        # the floor
        self.browser = browser_glyph().move_to([-3.0, -1.4, 0])
        lp = Arc(radius=0.17, start_angle=-PI / 2 + 0.5, angle=2 * PI - 1.0, color=LAPTOP, stroke_width=3)
        lp.add_tip(tip_length=0.12, tip_width=0.12)
        lt = label("localhost · 127.0.0.1", size, LAPTOP).next_to(lp, RIGHT, buff=0.12)
        self.loop = VGroup(lp, lt).move_to([0.95, -1.62, 0])
        # the drawer and its tubes
        dr = outline_box(1.25, 0.42, KEY, solid=True, fill_opacity=0.15)
        dt = mono("secrets/", size, KEY)
        self.drawer = VGroup(dr, dt.move_to(dr)).move_to([0.2, 1.77, 0])
        self.drawer.box, self.drawer.text = dr, dt
        self.tubes = {}
        for k, dx in (("loader", -0.25), ("api", 0.25)):
            hx = xs[k] - 0.22
            top = self.houses[k].roof.get_top()[1]
            roof_y = top - 0.22 * (self.houses[k].roof.height / (self.houses[k].roof.width / 2))
            sx = self.drawer.get_center()[0] + dx
            pts = [[sx, self.drawer.get_bottom()[1], 0], [sx, 1.43, 0], [hx, 1.43, 0], [hx, roof_y, 0]]
            core = VMobject(stroke_color=KEY, stroke_width=4).set_points_as_corners([np.array(p) for p in pts])
            glow = core.copy().set_stroke(KEY, 12, opacity=0.18)
            self.tubes[k] = VGroup(glow, core)
        # the public street and Google
        ps = outline_box(0.7, T - B, S.GREY, solid=False).move_to([3.2, (B + T) / 2, 0])
        pt = label("public street", size, S.GREY).rotate(PI / 2).move_to(ps)
        self.public = VGroup(ps, pt)
        self.google = self._building(B, T)
        # the docker-volumes folder (S14/S15)
        fd = VGroup(folder_glyph(0.34, KEY), mono("docker-volumes/", size, KEY)).arrange(RIGHT, buff=0.12)
        self.folder = fd.move_to([xs["chroma"] + 0.35, 0.6, 0])
        # assemble what is shown
        self.add(self.frame, self.header, *[self.streets[k] for k in spans], self.wall)
        for k, h in self.houses.items():
            if k not in gone:
                self.add(h)
        for p in doors:
            self.add(self.doors[p])
        self.add(self.browser, self.loop, self.public, self.google)
        if drawer:
            self.add(self.drawer)
        for k in tubes:
            self.add(self.tubes[k])
        if folder:
            self.add(self.folder)
        self.ride(*self.doors.values(), self.drawer, *self.tubes.values(), self.folder, *self.houses.values())
        self.shift(np.array([0, 0.75 - self.frame.get_center()[1], 0]))

    @classmethod
    def at(cls, scene_id: str, **kw) -> "AppMap":
        """The map as it stands when scene `scene_id` ('S05') starts (MAP_AT); kw overrides."""
        return cls(**{**MAP_AT[scene_id], **kw})

    def _street(self, k, a, b, laid):
        w = b - a
        band = (outline_box(w, 0.36, ROUTE, solid=True, fill_opacity=0.15) if laid
                else outline_box(w, 0.36, S.GREY, solid=False)).move_to([(a + b) / 2, 0.13, 0])
        t = mono(STREETS[k], self.size, ROUTE if laid else S.GREY).move_to(band)
        mask = RoundedRectangle(width=t.width + 0.2, height=0.3, corner_radius=0.08, stroke_width=0) \
            .set_fill(S.BG, 0.85).move_to(t)
        g = VGroup(band, mask, t)
        g.band, g.mask, g.text = band, mask, t
        return g

    def _building(self, B, T):
        g = google_building(2.55, T - B, door=False, meter_=False, text_y=0.35 - B).move_to([5.1, B, 0],
                                                                                           aligned_edge=DOWN)
        d = door_glyph(0.36, 0.5, CLOUD).move_to([g.frame.get_left()[0] + 0.15 + 0.2, 1.28, 0])
        lk = lock_glyph(0.26, CLOUD).next_to(d, RIGHT, buff=0.15)
        iam = label("IAM", self.size, CLOUD).next_to(lk, RIGHT, buff=0.08)
        m = meter().move_to([g.frame.get_right()[0] - 0.55, B + 0.55, 0])
        g.add(d, lk, iam, m)
        g.door, g.guard, g.meter = d, VGroup(lk, iam), m
        return g

    # ---- pieces changing state (Animations)
    def lay(self, k: str, run_time: float = 0.8):
        """Animation: street k turns from a GREY dashed plan into a solid PINK street."""
        st = self.streets[k]
        new = self._street(k, st.band.get_left()[0], st.band.get_right()[0], True)
        new.shift(st.band.get_center() - new.band.get_center())
        self.street_state[k] = "laid"
        return AnimationGroup(Transform(st.band, new.band), Transform(st.text, new.text), run_time=run_time)

    def unlay(self, k: str, run_time: float = 0.6):
        """Animation: street k disappears (network removed)."""
        self.street_state[k] = "gone"
        return FadeOut(self.streets[k], run_time=run_time)

    def light(self, k: str, run_time: float = 0.6):
        """Animation: house k lights TEAL (its container runs)."""
        return Transform(self.houses[k], lit_house(self.houses[k], True), run_time=run_time)

    def darken(self, k: str, run_time: float = 0.6):
        """Animation: house k goes hollow again (its container stopped)."""
        return Transform(self.houses[k], lit_house(self.houses[k], False), run_time=run_time)

    def open_door(self, p: str, run_time: float = 0.6):
        """Animation: published port p's door appears with its 'host→container' label."""
        d = self.doors[p]
        return AnimationGroup(FadeIn(d.glyph, scale=0.6), FadeIn(d.text, shift=UP * 0.1), run_time=run_time)

    def brick(self, p: str, run_time: float = 0.6):
        """Animation: door p bricks up (the container stopped; or a side narrowed). Returns the
        animation; the bricks are kept as .bricked[p]."""
        br = bricks(0.42, 0.46).move_to(self.doors[p].glyph)
        self.bricked = getattr(self, "bricked", {})
        self.bricked[p] = br
        return LaggedStart(*[FadeIn(b) for b in br], lag_ratio=0.05, run_time=run_time)

    def tube_on(self, k: str, run_time: float = 0.8):
        """Animation: the GREEN tube from the drawer into house k ('loader' or 'api') draws."""
        return Create(self.tubes[k], run_time=run_time)

    def call(self, src: str, dst: str, color=None, lane: float = 1.28) -> VGroup:
        """A call as an arrow (not added; .path for travel()): 'browser' -> a house goes to its door
        (PINK); 'loader' -> 'chroma' along their street (PINK); a house -> 'google' up to the lane
        over the roofs and across the public street to the IAM door (thin BLUE)."""
        if src == "browser":
            port = {v: k for k, v in DOOR_HOUSE.items()}[dst]
            d = self.doors[port].glyph
            a = self.browser.window.get_top() + UP * 0.05
            return _poly([a, d.get_bottom() + DOWN * 0.08], color or ROUTE, 4)
        if dst == "google":
            h = self.houses[src]
            ax = h.get_center()[0] + 0.25
            roof_y = h.roof.get_top()[1] - 0.25 * (h.roof.height / (h.roof.width / 2))
            door = self.google.door
            pts = [[ax, roof_y, 0], [ax, lane + self._dy(), 0], [door.get_left()[0] - 0.05, lane + self._dy(), 0]]
            return _poly(pts, color or CLOUD, 3)
        a, b = self.houses[src], self.houses[dst]
        y = a.body.get_center()[1]
        if a.get_center()[0] > b.get_center()[0]:
            pa, pb = [a.body.get_left()[0] - 0.05, y, 0], [b.body.get_right()[0] + 0.05, y, 0]
        else:
            pa, pb = [a.body.get_right()[0] + 0.05, y, 0], [b.body.get_left()[0] - 0.05, y, 0]
        return _poly([pa, pb], color or ROUTE, 4)

    def _dy(self):
        return self.frame.get_center()[1] - 0.025         # the lane's offset from the local frame

    def house_loop(self, k: str, with_label: bool = True) -> VGroup:
        """A small GREY loop arrow 'localhost' at house k's top-left (S10: every house has its own)."""
        h = self.houses[k]
        lp = Arc(radius=0.13, start_angle=-PI / 2 + 0.5, angle=2 * PI - 1.0, color=IMAGE, stroke_width=3)
        lp.add_tip(tip_length=0.1, tip_width=0.1)
        lp.move_to(h.body.get_corner(UL) + np.array([-0.05, 0.28, 0]))
        g = VGroup(lp)
        if with_label:
            g.add(label("localhost", self.size, IMAGE).next_to(lp, UP, buff=0.05))
        return g

    def phone_book(self, k: str, names) -> VGroup:
        """Street k's phone book (Docker DNS) as a small card listing `names` (not added), placed
        on the street's band, right end (for the S10 beat; move it as you need)."""
        rows = VGroup(*[mono(n, self.size, INK) for n in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        head = label("phone book", self.size, ROUTE)
        body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        fr = RoundedRectangle(width=body.width + 0.3, height=body.height + 0.25, corner_radius=0.08,
                              stroke_color=ROUTE, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        body.move_to(fr)
        g = VGroup(fr, body)
        st = self.streets[k].band
        g.next_to(st, DOWN, buff=0.1).align_to(st, RIGHT)
        g.head, g.rows = head, rows
        return g

    def wifi(self, size: float = 20) -> VGroup:
        """S11's honest beat (not added): a GREY dashed 'Wi-Fi' street below the laptop and, for each
        door, a dashed GREY reach line down through the floor to it (.reach{port}): an unprefixed
        door faces every street the laptop is on. Needs ~0.7 below the map."""
        b = self.frame.get_bottom()[1]
        st = outline_box(self.frame.width, 0.36, S.GREY, solid=False).move_to([self.frame.get_center()[0],
                                                                                b - 0.35, 0])
        t = label("Wi-Fi", size, S.GREY).move_to(st).align_to(st, LEFT).shift(RIGHT * 0.25)
        g = VGroup(st, t)
        g.reach = {}
        for p, d in self.doors.items():
            x = d.glyph.get_center()[0]
            g.reach[p] = DashedLine([x, d.text.get_bottom()[1] - 0.05, 0], [x, b - 0.17, 0], color=S.GREY,
                                    stroke_width=2.5)
        return g


# ================================================================== the chat page (illustration)
class ChatWireframe(Rig):
    """The schematic /chat page (always tagged `illustration`; NO answer text anywhere): address
    bar, an optional collection picker, the question bubble (README's example, quoted), an answer
    frame, and a collapsed 'References · 10 chunks' drawer.
        cw = ChatWireframe(); self.play(FadeIn(cw.shell))
        self.play(cw.type_question())                # the question's glyphs type in
        self.play(cw.grow_bars())                    # 5 GREY skeleton bars, no glyphs
        self.play(cw.open_drawer())                  # 10 empty GREY rows
    picker='char-split-collection ▾' (S12/S13); row_head='book · author · dist' (S12's drawer header);
    fun_fact=True (S13): the answer's last bar is a YELLOW box 'Pavlos' fun fact' (.fun, not added).
    .window .shell (everything shown before typing) .picker .bubble .question .answer .bars (not
    added) .drawer .rows (not added) .row_head (not added) .fun (not added)"""

    def __init__(self, url: str = "localhost:3200/chat", question: str = QUESTION, picker: str | None = None,
                 row_head: str | None = None, fun_fact: bool = False, win_w: float = 9.6, win_h: float = 6.0,
                 size: float = 22, **kw):
        super().__init__(**kw)
        from explainer.devops import browser_window
        self.window = browser_window(url, win_w, win_h)
        c = self.window.content
        x0, x1, top = c.get_left()[0] + 0.3, c.get_right()[0] - 0.3, c.get_top()[1] - 0.25
        y = top
        self.picker = None
        if picker:
            self.picker = chip(picker, S.GREY, size=20, font=MONO).move_to([x0, y, 0], aligned_edge=UL)
            y -= self.picker.height + 0.2
        q = label(question, size, INK)
        bub = RoundedRectangle(width=q.width + 0.6, height=q.height + 0.4, corner_radius=0.18, stroke_color=S.GREY,
                               stroke_width=2).set_fill(S.GREY_DARK, 1)
        bub.move_to([x1 - bub.width / 2, y - bub.height / 2, 0])
        q.move_to(bub)
        self.bubble, self.question = bub, q
        y -= bub.height + 0.25
        ans_h = 1.45
        self.answer = RoundedRectangle(width=x1 - x0, height=ans_h, corner_radius=0.12, stroke_color=S.GREY_DARK,
                                       stroke_width=2).set_fill(S.BG, 1).move_to([(x0 + x1) / 2, y - ans_h / 2, 0])
        widths = (0.92, 0.85, 0.95, 0.7, 0.5)
        aw = self.answer.width - 0.6
        self.bars = VGroup(*[RoundedRectangle(width=aw * f, height=0.13, corner_radius=0.06, stroke_width=0)
                             .set_fill(S.GREY, 0.45) for f in widths])
        self.bars.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(self.answer).align_to(self.answer, LEFT) \
            .shift(RIGHT * 0.3)
        self.fun = None
        if fun_fact:
            ft = label("Pavlos' fun fact", 20, TURN)
            fb = RoundedRectangle(width=aw * 0.7, height=0.42, corner_radius=0.08, stroke_color=TURN,
                                  stroke_width=2.5).set_fill(TURN, 0.12)
            ft.move_to(fb).align_to(fb, LEFT).shift(RIGHT * 0.15)
            self.fun = VGroup(fb, ft).move_to(self.bars[-1], aligned_edge=LEFT)
            self.bars.remove(self.bars[-1])
        y -= ans_h + 0.25
        dh = 0.48
        dfr = RoundedRectangle(width=x1 - x0, height=dh, corner_radius=0.1, stroke_color=S.GREY, stroke_width=2) \
            .set_fill(S.GREY_DARKER, 1).move_to([(x0 + x1) / 2, y - dh / 2, 0])
        dtx = label("References · 10 chunks", 20, S.GREY).move_to(dfr).align_to(dfr, LEFT).shift(RIGHT * 0.25)
        chev = label("▸", 20, S.GREY).move_to(dfr).align_to(dfr, RIGHT).shift(LEFT * 0.25)
        self.drawer = VGroup(dfr, dtx, chev)
        self.drawer.text, self.drawer.chev = dtx, chev
        y -= dh + 0.12
        self.row_head = None
        if row_head:
            self.row_head = label(row_head, 20, S.GREY).move_to([x0 + 0.25, y - 0.15, 0], aligned_edge=LEFT)
            y -= 0.4
        avail = y - (c.get_bottom()[1] + 0.15)
        rh = min(0.16, (avail - 9 * 0.06) / 10)
        self.rows = VGroup(*[RoundedRectangle(width=x1 - x0 - 0.3, height=rh, corner_radius=min(0.05, rh / 2),
                                              stroke_width=0).set_fill(S.GREY, 0.3) for _ in range(10)])
        self.rows.arrange(DOWN, buff=0.06).move_to([(x0 + x1) / 2, y - self.rows.height / 2, 0])
        self.shell = VGroup(self.window, *([self.picker] if self.picker else []), self.bubble, self.answer,
                            self.drawer)
        self.add(self.shell)
        self.ride(self.question, self.bars, self.rows, self.fun, self.row_head)

    def type_question(self, run_time: float = 1.4):
        """Animation: the question types into its bubble (glyph by glyph)."""
        self.add(self.question)
        return ShowIncreasingSubsets(self.question, rate_func=linear, run_time=run_time)

    def grow_bars(self, run_time: float = 1.0):
        """Animation: the answer's GREY skeleton bars grow in from the left (no glyphs)."""
        bars = list(self.bars) + ([self.fun] if self.fun is not None else [])
        self.add(*bars)
        return LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.2, run_time=run_time)

    def open_drawer(self, run_time: float = 1.0):
        """Animation: the drawer's chevron turns and ten empty GREY rows slide open."""
        from manim import Rotate
        self.add(self.rows, *([self.row_head] if self.row_head is not None else []))
        anims = [Rotate(self.drawer.chev, angle=-PI / 2),
                 LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in self.rows], lag_ratio=0.08)]
        if self.row_head is not None:
            anims.append(FadeIn(self.row_head))
        return AnimationGroup(*anims, run_time=run_time)
