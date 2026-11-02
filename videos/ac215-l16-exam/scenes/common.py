"""Shared code for AC215 L16 exam edition (System Tradeoffs: networking, runtime config and capacity,
with L10 as the opener): paths, narration, the semantic colours of BRIEF.md, source panels quoting
assets/source/<repo>/<path> (cheese-app-v0 @ cb6fb94, cheese-app-v2 @ 14f2a14), tags, lecture refs,
the multiple-choice ponder card, the takeaway card, and this video's set pieces V1-V6 of BRIEF.md.
The generic helpers (guard, swap_text, src_panel, cards, Piece …) are ported unchanged from L08's
tested common.py. Tested on screen by build/common_test.py (CommonTest, PieceTest).

Notes for scene authors
=======================

    from common import *      # every scene: SAY = NARRATION["S03"]; assert len(SAY) == n;
                              # one `with self.voiceover(SAY[i]) as vo:` per SAY line, in order
All text here is 20-26 pt (never below CAPTION = 20). Never .scale() a group that holds text below
1.0: Piece set pieces have .rescale(k) (shapes shrink, text keeps its size). Methods return
ANIMATIONS (play them) or MOBJECTS (placed, not added: FadeIn them) unless they say "plays". Set
pieces are built centred at ORIGIN unless they say "in place" (then they already sit where the
script wants them). This edition has NO terminals, NO captures, NO README tracker, NO your-turn tags.

Frame budget. Safe frame x -6.6..6.6, y -3.6..3.6. lecture_ref / lref top right (y 3.13..3.6,
right edge 6.6): keep the top-right corner free while a tag is up. An "in place" piece spans
y -3.3..2.95 at most. Layout asserts use guard() (raises locally, only warns when
GITHUB_ACTIONS=true); content checks (sources, numbers, never-shown lines) are plain raises.

Glyph fonts. CMU (serif / sans) lacks ⌊ ⌋ ↔ ≤ ≠ ✓ ✗ ▸ and superscripts other than ¹ (Pango falls
back to another font, which looks foreign): put formulas and those signs in mono (formula(),
mono()). "→", "−", "÷", "×", "…" are fine everywhere. In card text, `code` is mono and **word** bold.

Names. The cheese-app-v0 README names the instructor (first name) on lines 20, 21, 36, 232-249:
NEVER_SOURCE refuses them (excerpt, src_panel, readme_panel raise), and unname(s) / guard_names(s)
refuse any line holding the name. Say "the course staff". Secrets are key_glyph() (GOLD), never a
value; "…" stands for any value left out.

Data and sources
    NARRATION["S01"] … ["S08"]   SAY lines from script.md      TITLES[cls], SPEC (video.yaml)
    Source names are repo-relative WITH the repo as the first segment, exactly as stored:
        "cheese-app-v0/api-service/docker-entrypoint.sh", "cheese-app-v0/frontend-ai-chatbot/
        env.development" (stored without the dot; shown_path() -> ".env.development"),
        "cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py", "cheese-app-v2/README.md" …
    source_text(name)  excerpt(name, a, b)  source_line(name, n)  shown_path(name)
    src_panel(name, a, b=None, wrap=True|{n: [...]}, focus=, join=, cut_comments=, max_rows=12,
        size=22, width=) CODE(): header "path · lines a–b"; folded: src_panel(name, [23, 25, 27,
        (29, 33)]) -> "lines 23–33 (folded)"; raises when > 12 rows or > 12.9 wide.
        .bar(n, colour) -> VGroup (not added) .span(n, sub) -> glyphs .rows_of(n) .code .header
    readme_panel(repo, a, b=None, width_chars=60, focus=None) PANEL(repo/README.md: a–b): the README's
        words as plain text in the code-panel frame (** and backticks stripped, link targets
        dropped), long lines folded at word boundaries (GREY ↪ rows), header "repo/README.md ·
        lines a–b" (+ " · wrapped"). .clause(n, sub) -> the glyphs of `sub` in line n across its rows;
        .bar(n) as src_panel.
    excerpt_chip(sub, header, line=source_line(...)) the exact sub-string of one line, headed
    max_replicas(limit, other, per) -> int (floor)   formula_text(limit, other, per) -> str

Colours (BRIEF.md "Colours", binding)
    LAPTOP (= BROWSER, the visitor's machine) GREY · CLOUD (VPC, subnets, IGW, NAT, ALB, Route 53,
    managed DB, secret manager) BLUE · CTR (images, FastAPI tasks / replicas, ChromaDB) TEAL ·
    SHARED (= INTERNET: the internet, the public resolver, ephemeral ports, other DB clients) ORANGE
    · OWN (= VALUES: runtime values, schema, the replica's pool) GREEN · TOOL (Docker, uvicorn,
    Nginx, autoscaler, pgvector) PURPLE · ERR RED · TURN (packet in flight, matched row, ponder,
    takeaway) YELLOW · KEY (= COST: the key glyph, the price tag) GOLD · ROUTE (= LOOKUP: route
    rows, DNS arrows, request paths, NAT table, connection pipes) PINK · FUTURE (outside this
    lecture: dashed) GREY · INK white.
Running example (BRIEF.md "Running example"; the lecture's own placeholders)
    VPC_CIDR "10.0.0.0/16"  PUB_CIDR "10.0.1.0/24"  APP_CIDR "10.0.2.0/24"  DATA_CIDR "10.0.3.0/24"
    TASK_IP "10.0.2.5"  DB_IP "10.0.3.7"  PUBLIC_IP "34.120.45.67"  API_HOST "api.example.com"
    APP_HOST "app.example.com"  ALB_NAME "api-alb"  TG_NAME "fastapi-tg"  IMAGE "myapp:v1.4"
    LLM_DST "34.x:443"  EPHEMERAL "52134"  NAT_PORT "61001"  RESOLVER "1.1.1.1"
    PRIVATE_RANGES (RFC 1918)  PORT_REPO 9000  PORT_LECTURE 8000

Tags and chips (GREY unless said; all _keep: they keep their size in Piece.rescale)
    lref(16, "13") / lref(10, "11") = lecture_ref(n, slides), top right
    lr = lref_swap(self, lr, 10, "42") (plays; old may be None; old out, then new in)
    swap_text(parent, old, new) -> anims: the house sequential text swap (never Transform text)
    illustration_tag(note_=None)  lecture_pic_tag() "lecture's picture"  aws_chip() "the lecture's
    picture (AWS names)"  concept_tag(s) (dashed)  grey_chip(text)  stamp(text, colour)
    fix_chip(text) (GREEN)  concept_box(text)  price_tag(text="$$") (GOLD)  down_chip() (RED "down")
Cards
    takeaway(text, width=12.2, y=-1.4) the YELLOW takeaway card: " · " splits it into rows (each
        row fit to width; `code` mono); .frame .head .rows; write it in with takeaway_in(card)
        (-> anims, head first, rows lagged) and leave with FadeOut(card).
    McqCard(stem, options, answer, seconds=10) the multiple-choice ponder (script PONDER): YELLOW
        card, 22 pt stem (**word** bold, `code` mono), four rows A-D (letter in a circle), a reserved
        one-row reason slot (20 pt) under each, timer bar, `illustration` tag on its top edge.
        11.8 x 6.3 for a 3-row stem and one-row options, top at y 2.95 (guard raises when it
        would reach below -3.6: shorten the stem or an option).
        mcq_ponder(scene, card) plays: card in, timer drains (seconds). Then (next SAY):
        self.play(*card.right(note="…")) (row fills YELLOW, ✓, GREEN note in its slot);
        self.play(*card.wrong("A", "reason")) (RED reason in A's slot); FadeOut(card).
    ponder_at(scene, question) the plain ponder card (L08)   question_card(text)
    card_rows(items, header=)  table_card(headers, rows)  mono_card(lines, colour, header=)
    illustration_card(lines, header=None, mono=True) GREY-outlined card + `illustration` tag:
        every invented code line (S05's Dockerfile line, S07's SQL); never a repo panel.
    value_card(lines) GREEN mono card (runtime values: "APP_ENV=prod", …)
    rule_row(n, text, thumb=None, width=11.6) S08's numbered rule row (YELLOW badge, a ≤1.3 x 0.8
        thumbnail slot, fit text). .badge .thumb .text
    Counter(text, value)  card_glyph(title, sub)  fit_rows(text, width)
Glyphs
    key_glyph(name=) key_outline() padlock() bell(colour) door(port, colour) house(text)
    cylinder(name, sub, colour) gear() cpu_gauge(level) browser_glyph() internet_cloud()
    image_glyph(name, digest) secret_manager() spark() x_mark() tick_mark() file_row(name)
    container_box(title) laptop_zone() tunnel(a, b, text=None) (PINK, not added) formula(s) (mono)
    arrow_(a, b, colour) a house arrow  path_points(*mobs_or_points) -> list of points

Set pieces (Piece = VGroup with named parts: piece.reveal(scene, *names) / .hide plays;
    self.play(*piece.parts_in("a")); a part not shown yet is a member at opacity 0 (never FadeOut a
    part, FadeOut the whole piece); Piece(show=(...)) starts with only those parts visible)
    Packet(src, dst, colour=TURN, slot=None)  (chars x 0.167 + 0.7) x 0.48, centred at ORIGIN: an
       envelope icon and "src → dst" in 20 pt mono (src="" draws "→ dst"). .set_src(text) (no
       longer than the first src; it ends at the arrow) / .set_dst(text) (≤ slot chars, default
       len(dst)) -> anims (the field swaps, new text YELLOW); .settle() -> anims (white again);
       .travel(points, run_time=1.2, lead="center"|"icon", clamp=True) -> anim (jumps to the first
       point now: build it before FadeIn; clamp keeps it inside the frame); .recolor(c) -> anims;
       .drop() -> anim (RED, shrinks away: it leaves the scene); .spark_at() / .ok() -> mobjects
       (not added). .src .dst .arrow .icon .frame
    V1 LaptopHost(show=None)  6.2 x 3.9: GREY laptop zone, browser glyph, host door "laptop :9000",
       TEAL container (uvicorn chip PURPLE, FastAPI box with door :9000), three interface sockets
       on the container wall (the top one is 127.0.0.1), PINK tunnel host door -> FastAPI door.
       Parts: zone browser host_door ctr uvicorn api sockets tunnel (show=(...) starts with those).
       .bind_all() -> mobject
       (YELLOW bracket around every socket + "0.0.0.0 · every interface") .bind_loopback() ->
       mobject (RED bracket around 127.0.0.1 + chip "loopback · only this container")
       .request_points() -> browser -> host door -> tunnel -> FastAPI door (travel it with
       lead="icon": the label trails right). .host_door .api_door .sockets
       Street(numbers=5 IPs)  9.1 x 2.6: BLUE houses with numbers (addresses); .houses[i]; house 2 has the
       doors :8000 and :5432 (.doors)
       ReachTable()  12.0 x 2.8 (L10 slide 11): rows address · who can reach it · getting traffic
       in; laptop column; .to_cloud(r) -> anims (cell r swaps to the cloud value); .cells[r]
       DnsPath()  12.8 x 3.6 (L16 slide 27): browser (api.example.com), public resolver 1.1.1.1
       (ORANGE), Route 53 (BLUE), ALB api-alb (BLUE, public subnet 10.0.1.0/24); .step(k) -> anims
       (arrow k + its badge; 1 ask, 2 ask Route 53, 3 ALB IP back, 4 to the browser, 5 HTTPS to
       the ALB) .node(name) name in browser resolver route53 alb
       Gate(rule="allow · TCP 8000 · source: ALB")  4.4 x 1.6: a GREY gate bar + rule card;
       .point() the gate's centre .flash(ok=True) -> anims (GREEN / RED)
    V2 VpcMap(show=None)  in place, 12.8 x 6.05 (x -6.35..6.45, y -3.2..2.85): ORANGE internet (left),
       Internet Gateway on the VPC edge, BLUE VPC 10.0.0.0/16 with three subnets: public
       10.0.1.0/24 (ALB, NAT Gateway), private app 10.0.2.0/24 (padlock, two TEAL FastAPI tasks,
       10.0.2.5), private data 10.0.3.0/24 (padlock, PostgreSQL 10.0.3.7). Parts: internet igw vpc
       public app data alb nat tasks db. .anchor(name) -> point: internet igw alb nat task task2
       db edge (outside the IGW) .path(*names) -> points .nat_down() -> anims (NAT RED + "down")
       .nat_up() -> anims .route_spot() -> where the compact RouteTable (≤ 4.2 wide) sits: above
       the first task, under the app subnet's header. .boxes[name] (the shapes)
       CidrRuler(prefix=16)  11.4 x 0.7: 32 bit cells (prefix BLUE "fixed", rest white "vary"),
       mono counter "2¹⁶ = 65,536"; .set_prefix(24) -> anims
       RouteTable(rows, title=None, compact=False)  rows [(destination, gateway)], PINK rows,
       header Destination / Gateway; full 4.7 x 2.1 with title, compact ~4.1 x 1.15 (no title,
       no header, PINK frame).
       .light(i) -> anims (row YELLOW) .unlight(i) .bar(i, text=None, thick=False, side=RIGHT|DOWN)
       -> mobject (YELLOW bar over row i + .label beside or under the table; not added: in VpcMap
       move .label where it covers nothing) .flash_gateway(i) -> anims
       .rows[i] .dst[i] .gw[i]
       NatNotebook(slots=2)  6.3 x 1.8 (+ 0.42 per extra slot): PINK card "NAT table · inside ↔
       outside"; .add_line(inside, outside) -> anims (next slot) .glow(i) -> anims .miss_note()
       -> mobject (RED "no line → dropped", under it; not added) .lines[i]
    V3 TwoPaths(show=None)  in place, 12.9 x 6.0: visitor's laptop with browser (top left, GREY,
       outside the VPC), static host / CDN app.example.com (bottom left, BLUE), the VPC (right:
       public subnet with ALB and NAT Gateway, private app subnet "FastAPI tasks ×3").
       Parts: visitor static vpc alb tasks (shown); files gear nat nat_out door (hidden).
       .deliver() -> anims (HTML CSS JS appear on the static host and fly into the browser)
       .unpack() -> anims (the files fade, the JS gear appears) .spin() -> anim .outline() ->
       anims (YELLOW traces of the VPC border and the visitor's laptop) .door_in() -> anims (the
       visitor's own ":9000 · nothing listens" door) .nat_one_way() -> anims (NAT Gateway + a
       PINK "out only" arrow) .anchor(name): browser visitor_door edge internet alb task static nat
       FrontDoor()  8.5 x 2.8 (slide 32 layout B): browser -> public front door app.example.com ->
       "/" Next.js server, "/api/*" FastAPI 10.0.2.5:8000 (private app subnet). .arrows .door
       RuleCards()  9.1 x 2.8 (slide 24): GREEN-outlined Nginx `location /api/ { proxy_pass
       http://10.0.2.5:8000; }` "=" BLUE-outlined ALB rule; .ip (the 10.0.2.5 glyphs) .eq
    V4 ImageConveyor(stops=("dev", "staging", "prod"), width=11.6)  11.6 x 0.85: belt + stop labels (belt at y 0
       before moving). .stop_point(i) .carry(mob, i) -> anim .check(i) -> mobject (YELLOW ✓)
       LayerStack(layers=None, key_line="ENV LLM_API_KEY=…")  4.0 x 3.1: TEAL image layers bottom to top, a
       config card on top (ENV LLM_API_KEY=… with a GOLD key). .xray() -> anims (layers ghost,
       the key glows RED) .layers .config .key
       secret_manager()  BLUE box with a GOLD key   value_card(lines)   tunnel(a, b, "-v")
    V5 SlotGrid(n=100, cols=10)  3.9 x 4.2 (title included): BLUE panel of socket slots; .fill(k, colour) ->
       (slot indices, anims) the next k free slots plugged; .free() count; .slot(i) .slots
       .pipes(point, idx, colour=ROUTE) -> VGroup of PINK lines (not added)
       Autoscaler(count=3, max_="?")  12.3 x 1.45 (slide 52): Signal -> Policy (target · min · max, PURPLE) ->
       Desired count -> Capacity, caption slot under it. .set_count(n) -> anims .set_max(n) ->
       anims .boxes[name] (signal policy count capacity) .caption() -> mobject (YELLOW
       "Downstream limits still bound the result.")
       Replica(i, pool=20)  1.9 x 1.4: TEAL box "replica i", GREEN pool bar "pool 20"; .pool_point()
       .cpu (a cpu_gauge, low)
    V6 req_table(name, cols)  GREEN mini table (header + column rows); fk_line(a, b) PINK
       txn_bracket(mob, text) GREEN; vector_chip(text) PINK chip with distance rays
       ChipSorter(names=(...))  ~12.4 x 2.7: three candidate boxes (TEAL "ChromaDB on a VM", BLUE
       "PostgreSQL service + pgvector", BLUE "vector search service"), each with a GREY note;
       three chip slots per box (k = 0 bottom … 2). .box(i) .slot(i, k) -> point .land(chip, i,
       k=0) -> anim .bounce(chip, i) -> anims (dips into box i, it flashes RED, chip returns)
       DbTable(name, cols)  8.4 x 1.3, GREEN table card with room for one more column; .add_column("embedding
       vector(256)", colour=TOOL) -> anims .new_col
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
    DashedVMobject,
    DecimalNumber,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    ManimColor,
    MoveAlongPath,
    Polygon,
    Rectangle,
    Rotate,
    RoundedRectangle,
    ShowPassingFlash,
    Square,
    Succession,
    Text,
    Transform,
    ValueTracker,
    VGroup,
    VMobject,
    linear,
    rush_into,
    smooth,
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
from explainer.components import ponder_card  # noqa: F401  (re-exported for the scenes)
from explainer.devops import (  # noqa: F401  (re-exported for the scenes)
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
    layer_bar,
    lecture_ref,
    line_bar,
    line_pitch,
    machine_box,
    mono,
    mono_line,
    server,
    step_badge,
    substring,
    tag,
    warning_sign,
)
from explainer.script import load_narration

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
LAPTOP = S.GREY          # your laptop and the visitor's machine: the browser, localhost, secrets/ on the host
BROWSER = LAPTOP
CLOUD = S.BLUE           # VPC, subnets, IGW, NAT Gateway, ALB, Route 53, managed PostgreSQL, secret manager
CTR = S.TEAL             # images (myapp:v1.4), FastAPI tasks / replicas, ChromaDB, the registry shelf
SHARED = S.ORANGE        # the public internet, the public resolver, ephemeral ports, other DB clients
INTERNET = SHARED
OWN = S.GREEN            # runtime values per environment, the app's schema, the replica's own pool
VALUES = OWN
TOOL = S.PURPLE          # Docker, uvicorn, Nginx, the autoscaler, the pgvector extension
ERR = S.RED              # a dropped packet, too many connections, a baked key, localhost/10.x in browser code
TURN = S.YELLOW          # look here now: the packet in flight, the matched row, ponder, takeaway
KEY = S.GOLD             # the secret's key glyph (never a value), the DB tier's price tag
COST = KEY
ROUTE = S.PINK           # route rows, DNS arrows, request paths, the NAT table, connection pipes
LOOKUP = ROUTE
FUTURE = S.GREY          # outside this lecture (dashed)
INK = S.WHITE
DIMMED = S.GREY

# ------------------------------------------------------------------ names on screen (BRIEF.md "Things never to do")
# The cheese-app-v0 README names the instructor (first name) on the lines below: never quoted. Every
# other line that goes on screen is checked for the name (guard_names), so a slip raises.
MASKS: tuple = ()                    # nothing is masked in this edition: a named line is refused
_NAME_RE = re.compile(r"pavlos", re.IGNORECASE)
NEVER_SOURCE = {
    "cheese-app-v0/README.md": {20, 21, 36, *range(232, 250)},
}
NEVER_FILES = {   # BRIEF.md: never quoted (not in assets/source on purpose; refused if they ever appear)
    "cheese-app-v0/api-service/api/routers/rag.py",
    "cheese-app-v2/src/frontend-react/.env.development",
    "cheese-app-v2/src/frontend-react/.env.production",
}


def guard_names(s: str) -> str:
    """Raise ValueError if s names the instructor (never on screen: say "the course staff")."""
    if _NAME_RE.search(s):
        raise ValueError("this line names a person: it is never shown (BRIEF.md 'Things never to do')")
    return s


unname = guard_names     # the generic helpers below call unname() on every shown line

# ------------------------------------------------------------------ the running example (the lecture's placeholders)
VPC_CIDR, PUB_CIDR, APP_CIDR, DATA_CIDR = "10.0.0.0/16", "10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"
TASK_IP, DB_IP = "10.0.2.5", "10.0.3.7"
PUBLIC_IP = "34.120.45.67"                   # L16 slide 4
API_HOST, APP_HOST = "api.example.com", "app.example.com"
ALB_NAME, TG_NAME = "api-alb", "fastapi-tg"
IMAGE = "myapp:v1.4"
LLM_DST = "34.x:443"
EPHEMERAL, NAT_PORT = "52134", "61001"
RESOLVER = "1.1.1.1"
PRIVATE_RANGES = ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16")   # L16 slide 8 (RFC 1918)
PORT_REPO, PORT_LECTURE = 9000, 8000
BOTTOM = -3.5


def max_replicas(limit: int, other: int, per: int) -> int:
    """⌊(limit − other) ÷ per⌋ (BRIEF.md rule 6): the largest replica count whose pools all open."""
    assert limit > other >= 0 and per > 0
    return (limit - other) // per


def formula_text(limit: int, other: int, per: int) -> str:
    """'⌊(100 − 10) ÷ 20⌋ = ⌊4.5⌋ = 4' (mono only: the serif has no ⌊ ⌋)."""
    q = (limit - other) / per
    qs = f"{q:.1f}".rstrip("0").rstrip(".") if q != int(q) else str(int(q))
    return f"⌊({limit} − {other}) ÷ {per}⌋ = ⌊{qs}⌋ = {max_replicas(limit, other, per)}"


# ------------------------------------------------------------------ lecture refs
def lref(lecture: int, slides: str) -> VGroup:
    """The GREY "Lecture 16 · slides 13–14" tag, top right (lecture_ref(lecture, slides)). Only
    lectures 16 and 10 are cited in this video."""
    if int(lecture) not in (10, 16):
        raise ValueError("this video cites Lecture 16 (primary) and Lecture 10 (the opener) only")
    return lecture_ref(int(lecture), slides)


# ------------------------------------------------------------------ sources
def src_path(name: str) -> str:
    """Resolve a source name under assets/source ("cheese-app-v0/api-service/docker-shell.sh"; the
    two frontend env files are stored as env.development / env.production). Raises for files never
    shown and for missing files."""
    if name in NEVER_FILES:
        raise ValueError(f"{name} is never shown (BRIEF.md 'Things never to do')")
    if not (SOURCE / name).is_file():
        raise FileNotFoundError(f"assets/source/{name} not found")
    return name


def source_text(name: str) -> str:
    """A tutorial file as stored (never print it whole: excerpt / src_panel refuse the
    never-shown lines line by line)."""
    return (SOURCE / src_path(name)).read_text(encoding="utf-8")


def _source_lines(name: str, nums, strip_emoji_: bool = False) -> dict[int, str]:
    path = src_path(name)
    lines = source_text(name).split("\n")
    bad = NEVER_SOURCE.get(path, set()) & set(nums)
    if bad:
        raise ValueError(f"{path}: lines {sorted(bad)} are never shown (they name a person)")
    out = {}
    for n in nums:
        if not 1 <= n <= len(lines):
            raise IndexError(f"{path} has {len(lines)} lines (asked for {n})")
        s = lines[n - 1].expandtabs(4)
        guard_names(s)
        out[n] = _emoji_guard(s, f"{path} line {n}", strip_emoji_)
    return out


def shown_path(name: str) -> str:
    """The path as the viewer sees it: the stored path, the frontend env files with their real
    leading dot ("cheese-app-v0/frontend-ai-chatbot/.env.development")."""
    p = src_path(name)
    head, _, base = p.rpartition("/")
    if base in ("env.development", "env.production"):
        base = "." + base
    return f"{head}/{base}" if head else base


# ================================================================== generic helpers (from L07, tested there)
EMOJI = frozenset("📊📝🔵🟢✅❌⚠🧀🤖" + chr(0xFE0F))   # README emoji: stripped from shown rows


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


WRAP_REACH = 20          # wrap_output: a break may come up to this many characters before the column


WRAP_HANG = 2            # wrap_output: continuation rows hang this far under the line's own indent


def wrap_output(s: str, width: int, reach: int = WRAP_REACH, hang: int = WRAP_HANG) -> list:
    """Fold one output line for a `width`-column terminal at a word boundary (QA: the fixed-column
    fold cut words and identifiers, "ad|k telemetry disable", "H|TTP/1.1", "itine|rary_validation"):
    at the last space within `reach` characters of the column, else after the last ',' there, else
    after the last '/', else after the last '_', '-' or '.', and at the column only when none is
    in reach. Continuation rows hang `hang` spaces under the line's own indent. Returns
    [(row, a, b, indent)] with row == " " * indent + s[a:b] (the spaces at a break are dropped)."""
    if len(s) <= width:
        return [(s, 0, len(s), 0)]
    lead = len(s) - len(s.lstrip(" "))
    ind = min(lead + hang, width // 3)
    out, pos, indent = [], 0, 0
    while len(s) - pos + indent > width:
        room = width - indent
        lo = pos + max(1, room - reach)                 # the earliest row end allowed
        hi = pos + room                                 # the latest: a full row
        cut = nxt = None
        spaces = [j for j in range(lo, min(hi, len(s) - 1) + 1) if s[j] == " " and s[j - 1] != " "]
        if spaces:
            cut = nxt = spaces[-1]
            while nxt < len(s) and s[nxt] == " ":
                nxt += 1
        else:
            for seps in (",", "/", "_-."):
                after = [j + 1 for j in range(lo - 1, hi) if s[j] in seps and j + 1 < len(s)]
                if after:
                    cut = nxt = after[-1]
                    break
        if cut is None:                                 # nothing in reach: at the column
            cut = nxt = hi
        out.append((" " * indent + s[pos:cut], pos, cut, indent))
        pos, indent = nxt, ind
    out.append((" " * indent + s[pos:], pos, len(s), indent))
    return out


def grid_x0(line) -> float:
    """The x of column 0's left edge in a mono_line, measured from its glyphs (the median over
    non-space characters of glyph centre − (k + 0.5) · cell width). Falls back to the strut."""
    cw = cell_width(line.pt)
    offs, gi = [], 0
    for k, ch in enumerate(line.text):
        if ch.isspace():
            continue
        if gi >= len(line.glyphs):
            break
        offs.append(line.glyphs[gi].get_center()[0] - (k + 0.5) * cw)
        gi += 1
    return float(np.median(offs)) if offs else line.strut.get_left()[0]


def col_box(line, a: int, b: int, color: str = TURN, dashed: bool = False, pad: float = 0.04):
    """A box over character columns a..b (exclusive) of a mono_line, blank cells included. Not
    added."""
    cw = cell_width(line.pt)
    x0 = grid_x0(line) + a * cw
    r = box((b - a) * cw + 2 * pad, line.strut.height + 2 * pad, color, fill_opacity=0.0,
            radius=0.06, dashed=dashed, stroke=3)
    r.move_to([x0 + (b - a) * cw / 2, line.strut.get_center()[1], 0])
    return r


def bracket(mobs, text: str, color: str = ERR, x: float | None = None) -> VGroup:
    """A vertical bracket spanning `mobs` (terminal lines) at their left margin (or at x), with a
    numbered badge centred on it. Not added. .line .badge"""
    g = VGroup(*mobs) if isinstance(mobs, (list, tuple)) else mobs
    top, bot = g.get_top()[1] + 0.02, g.get_bottom()[1] - 0.02
    x = g.get_left()[0] - 0.16 if x is None else x
    ln = VMobject(stroke_color=color, stroke_width=4)
    ln.set_points_as_corners([[x + 0.08, top, 0], [x, top, 0], [x, bot, 0], [x + 0.08, bot, 0]])
    b = step_badge(text, color, radius=0.19).move_to([x - 0.04, (top + bot) / 2, 0])
    out = VGroup(ln, b)
    out.line, out.badge = ln, b
    return _keep(out)


def grey_tag(s: str) -> VGroup:
    return _keep(tag(s, S.GREY))


def illustration_tag(note_: str | None = None) -> VGroup:
    """GREY 'illustration' (every invented example: the hook's alarms, the ponders, S06's slots,
    S07's tables and SQL, the baked Dockerfile line); note_="x" -> 'illustration · x'."""
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
         ".yml": "yaml", ".json": "json", ".html": "html", ".txt": "text", ".lock": "toml",
         ".js": "javascript"}


def _lang(path: str) -> str:
    p = Path(path)
    if p.name == "Dockerfile":
        return "docker"
    if p.name in (".gitignore", ".dockerignore") or p.name.startswith((".env", "env.")):
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
              max_rows: int = 12) -> VGroup:
    """code_panel quoting assets/source/<name> (name masked), header "shown · lines a–b" (+ " ·
    comment cut", " · line N wrapped", " · suffix"). `first` may be a list (folded: only those file
    lines, a GREY '…' row at each gap, header "lines a–b (folded)"). join=[(a, b)]: lines a..b as
    one row. wrap=True / {n: ["sub", …]} as in L05. subtitle=True: the Colab cell's @title in GREY
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
            parts = _auto_wrap(ln)
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
    if wrapped:   # one note for every wrapped line (one note per line made the header too wide)
        extra.append(f"line {wrapped[0]} wrapped" if len(wrapped) == 1 else
                     f"lines {', '.join(str(n) for n in wrapped)} wrapped")
    if suffix:
        extra.append(suffix)
    if subtitle is True:
        subtitle = None
    _with_header(p, " · ".join([shown, where, *extra]), subtitle=subtitle or None)
    if p.header.width > 12.9 and wrapped:
        extra = [e for e in extra if not e.endswith(" wrapped")] + ["wrapped"]
        _with_header(p, " · ".join([shown, where, *extra]), subtitle=subtitle or None)
    guard(p.header.width <= 12.9, f"{name} {lo}-{hi}: the header is {p.header.width:.1f} wide (> 12.9)")
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


class Prose(str):
    """A prose row for turn_card / card_rows (serif, not a command)."""


def _cell(s, size: float = CAPTION, color: str = INK):
    """A card cell: "`code`" -> mono (without backticks), Prose / str -> serif, a mobject as is."""
    if not isinstance(s, str):
        return s
    if len(s) > 1 and s.startswith("`") and s.endswith("`"):
        return mtext(s[1:-1], size, color)
    return mtext(str(s), size, color, font=S.FONT)



def _md_text(s: str, size: float = CAPTION, color: str = INK) -> Text:
    """One line as ONE Text: inline `code` in mono (backticks dropped, spacing kept), **word** in
    bold (markers dropped; keep a bold phrase on one row), the rest serif; masks GREY. An unpaired
    marker is dropped."""
    s = unname(s)
    if s.count("**") % 2:
        s = s.replace("**", "")
    plain, spans, bold = "", [], []
    in_code = in_bold = False
    start_c = start_b = 0
    i = 0
    while i < len(s):
        if s.startswith("**", i) and not in_code:
            if in_bold:
                bold.append((start_b, len(plain)))
            else:
                start_b = len(plain)
            in_bold = not in_bold
            i += 2
            continue
        if s[i] == "`":
            if in_code:
                spans.append((start_c, len(plain)))
            else:
                start_c = len(plain)
            in_code = not in_code
            i += 1
            continue
        plain += s[i]
        i += 1
    t2c = {m: S.GREY for m in MASKS if m in plain}
    kw = {"t2w": {f"[{a}:{b}]": "BOLD" for a, b in bold if b > a}} if bold else {}
    return S.text(plain, size, color, t2f={f"[{a}:{b}]": MONO for a, b in spans if b > a}, t2c=t2c, **kw)


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


def spark(r: float = 0.14, color: str = ERR) -> VGroup:
    """A small RED spark (an error flying)."""
    g = VGroup(*[Line(ORIGIN, UP * r, color=color, stroke_width=3).rotate(k * TAU / 8, about_point=ORIGIN)
                 for k in range(8)])
    g.add(Dot(radius=r * 0.3, color=color))
    return _keep(g)


def x_mark(h: float = 0.3) -> VGroup:
    """The RED ✗ on a wrong physics claim."""
    return _keep(cross_mark(h, ERR))


def tick_mark(h: float = 0.3) -> VMobject:
    """The GREEN tick on the voice (S01)."""
    return _keep(check_mark(h, OWN))


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


# ================================================================== L16: lecture tags, README panel
def lref_swap(scene, old, lecture: int, slides: str, run_time: float = 0.5) -> VGroup:
    """Replace the lecture tag (old may be None): old fades out, then the new one fades in, in the
    same run_time (faded at once, the two texts overlapped mid-swap: L05 final review). Returns
    the new tag (on screen)."""
    new = lref(lecture, slides)
    if old is None:
        scene.play(FadeIn(new), run_time=run_time)
    else:
        scene.play(Succession(FadeOut(old), FadeIn(new)), run_time=run_time)
    return new


_MD_LINK = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def md_plain(s: str) -> str:
    """A README line as plain text: [text](url) -> text, ** and backticks dropped, trailing
    spaces trimmed (README panels show the words, not the markup)."""
    s = _MD_LINK.sub(r"\1", s)
    return s.replace("**", "").replace("`", "").rstrip()


def readme_lines(repo: str, a: int, b: int | None = None) -> list[str]:
    """README.md lines a..b of `repo` ("cheese-app-v0" / "cheese-app-v2") as plain text (md_plain).
    Never-shown lines raise."""
    b = a if b is None else b
    d = _source_lines(f"{repo}/README.md", range(a, b + 1))
    return [md_plain(d[n]) for n in range(a, b + 1)]


def _nonspace(s: str) -> int:
    return len("".join(s.split()))


def readme_panel(repo: str, a: int, b: int | None = None, width_chars: int = 60, focus=None,
                 size: float = 22) -> VGroup:
    """PANEL(repo/README.md: a–b): the README's words (md_plain) in the code-panel frame, long lines
    folded at word boundaries (wrap_output), continuation rows start with a GREY '↪ '. Header
    "repo/README.md · lines a–b" (" · line N wrapped" when folded). focus: file line(s) kept bright.
    .clause(n, sub) -> glyphs of `sub` in file line n across its rows; .bar(n, colour) -> VGroup
    (not added); .rows_of(n) -> row indices; .code .header"""
    b = a if b is None else b
    plain = dict(zip(range(a, b + 1), readme_lines(repo, a, b)))
    rows, spans, rows_of, wrapped = [], [], {}, []
    for n in range(a, b + 1):
        s = plain[n]
        parts = wrap_output(s, width_chars - 2, hang=0) if len(s) > width_chars else [(s, 0, len(s), 0)]
        if len(parts) > 1:
            wrapped.append(n)
        rows_of[n] = []
        for k, (_row, i, j, _ind) in enumerate(parts):
            pre = "" if k == 0 else "↪ "
            rows_of[n].append(len(rows))
            rows.append(pre + s[i:j].strip() if k else s[i:j])
            spans.append((n, i, j, pre, len(s[i:j]) - len(s[i:j].lstrip()) if k else 0))
    if len(rows) > 12:
        raise ValueError(f"{repo}/README.md {a}-{b}: {len(rows)} rows (at most 12 on screen)")
    p = code_panel("\n".join(rows), f"{repo}/README.md", a, "text", font_size=size)
    where = f"line {a}" if a == b else f"lines {a}–{b}"
    _with_header(p, " · ".join([f"{repo}/README.md", where, *(["wrapped"] if wrapped else [])]))
    guard(p.width <= 12.95, f"README panel {p.width:.2f} wide (> 12.9): lower width_chars")
    for k, r in enumerate(rows):
        if r.startswith("↪ "):
            code_span(p.code, k, "↪").set_color(S.GREY)
    if focus is not None:
        keep = {focus} if isinstance(focus, int) else set(focus)
        for n, ks in rows_of.items():
            if n not in keep:
                for k in ks:
                    p.code.code_lines[k].set_opacity(0.3)

    def clause(n, sub, occurrence=0):
        s = plain[n]
        i = -1
        for _ in range(occurrence + 1):
            i = s.find(sub, i + 1)
        if i < 0:
            raise ValueError(f"{sub!r} not in {repo}/README.md line {n}")
        j = i + len(sub)
        out = VGroup()
        for k in rows_of[n]:
            _n, ra, rb, pre, lead = spans[k]
            lo, hi = max(i, ra + lead), min(j, rb)
            if lo >= hi:
                continue
            row_text = rows[k]
            col0 = len(pre) - (ra + lead)              # column of s-index x in this row: x + col0
            start = _nonspace(row_text[:lo + col0])
            cnt = _nonspace(s[lo:hi])
            out.add(*p.code.code_lines[k][start:start + cnt])
        return out

    p.clause = clause
    p.rows_of = lambda n: rows_of[n]
    p.bar = lambda n, color=TURN, opacity=0.18: _line_bars(p.code, rows_of[n], color, opacity)
    p.first, p.plain = a, plain
    return p


# ================================================================== L16: tags and chips
def lecture_pic_tag(s: str = "lecture's picture") -> VGroup:
    """GREY tag on a redrawn lecture diagram that is not in the repo (slide 24's rule, slide 32)."""
    return grey_tag(s)


def aws_chip(s: str = "the lecture's picture (AWS names)") -> VGroup:
    """GREY chip, the first time each AWS-named diagram appears (script.md conventions)."""
    return _keep(chip(s, S.GREY, size=CAPTION))


def grey_chip(s: str, size: float = CAPTION, font: str | None = None) -> VGroup:
    """A GREY chip (captions such as "TLS ends here", "no live runs · concepts, not clicks")."""
    return _keep(chip(s, S.GREY, size=size, font=font))


def price_tag(s: str = "$$") -> VGroup:
    """GOLD price tag (the DB tier's cost)."""
    return _keep(tag(s, COST))


def down_chip(s: str = "down") -> VGroup:
    """RED chip on a failed hop (the NAT Gateway outage)."""
    return _keep(tag(s, ERR))


def formula(s: str, size: float = 24, color: str = INK) -> Text:
    """A formula in mono (DejaVu has ⌊ ⌋ ≤ ↔ ⁶ ⁸ the serif lacks): formula(formula_text(100, 10, 20))."""
    return mono(s, size, color)


# ================================================================== L16: cards
def mono_card(lines, color: str = S.GREY, size: float = CAPTION, header: str | None = None,
              tint: float = 0.08) -> VGroup:
    """A card of mono rows in a `color` frame (GREEN value cards, GREY illustration code). Names are
    checked. .frame .rows .header"""
    rows = _mono_rows(lines, size, INK)
    fr = box(rows.width + 0.5, rows.height + 0.4, color, fill=S.BG, fill_opacity=0.95, radius=0.12, stroke=2.5)
    tn = RoundedRectangle(width=fr.width, height=fr.height, corner_radius=0.12, stroke_width=0) \
        .set_fill(color, tint).move_to(fr)
    rows.move_to(fr)
    g = VGroup(fr, tn, rows)
    g.frame, g.rows, g.header = fr, rows, None
    if header:
        h = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        g.add(h)
        g.header = h
    return g


def value_card(lines, size: float = CAPTION) -> VGroup:
    """GREEN runtime-value card ("APP_ENV=prod", "LOG_LEVEL=info", …): what the project sets."""
    return mono_card(lines, OWN, size)


def illustration_card(lines, header: str | None = None, mono_: bool = True, size: float = CAPTION) -> VGroup:
    """Invented code or text (S05's Dockerfile line, S07's SQL, the hook's alarms) on a GREY-outlined
    card with the `illustration` tag above its top-right corner (below it when a header is in the
    way); never a repo panel (no path header).
    mono_=False: serif rows ("`code`" spans mono). .frame .rows .tag .header"""
    if mono_:
        g = mono_card(lines, S.GREY, size, header=header, tint=0.04)
    else:
        g = card_rows(list(lines), header=header, size=size)
    tg = illustration_tag()
    tg.next_to(g.frame, UP, buff=0.06).align_to(g.frame, RIGHT)
    if header and g.header is not None and tg.get_left()[0] < g.header.get_right()[0] + 0.15:
        tg.next_to(g.frame, DOWN, buff=0.08).align_to(g.frame, RIGHT)
    g.add(tg)
    g.tag = tg
    return g


def question_card(text: str, size: float = 26, color: str = INK) -> VGroup:
    """A question card: GREY frame, larger serif text. .frame .text"""
    t = label(text, size, color)
    fr = box(t.width + 0.7, t.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.16)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def takeaway(text: str, width: float = 12.2, y: float = -1.4, size: float = 24,
             head: str = "takeaway") -> VGroup:
    """The YELLOW takeaway card (script TAKEAWAY): " · " splits `text` into rows, each fitted to the
    card (fit_rows; `code` in backticks mono), a "▸" in front of each; a YELLOW head word on the top
    edge. Centred at (0, y), bottom never below -3.5. Write it in with takeaway_in(card). .frame
    .head .rows"""
    inner = width - 1.0
    rows = VGroup()
    for seg in [s.strip() for s in text.split(" · ") if s.strip()]:
        body = fit_rows(seg, inner - 0.45, size)
        mark = mono("▸", size, TURN).next_to(body[0], LEFT, buff=0.18)
        rows.add(VGroup(mark, body))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    fr = box(width, rows.height + 0.8, TURN, fill=S.BG, fill_opacity=0.96, radius=0.18, stroke=3)
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.5 + DOWN * 0.08)
    hd = tag(head, TURN, size=CAPTION)
    hd.move_to(fr.get_corner(UP + LEFT) + np.array([0.4 + hd.width / 2, 0, 0]))
    g = VGroup(fr, rows, hd)
    g.frame, g.rows, g.head = fr, rows, hd
    g.move_to([0, y, 0])
    if g.get_bottom()[1] < -3.5:
        g.shift(UP * (-3.5 - g.get_bottom()[1]))
    guard(g.get_top()[1] <= 3.05, f"takeaway card too tall ({g.height:.2f}): shorten it")
    return g


def takeaway_in(card: VGroup, lag: float = 0.6) -> list:
    """Animations writing the takeaway card in: frame and head, then the rows one after another."""
    return [FadeIn(VGroup(card.frame, card.head)),
            LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows], lag_ratio=lag)]


def rule_row(n: int, text: str, thumb=None, width: float = 11.6, size: float = 22) -> VGroup:
    """S08's rule row: a YELLOW numbered badge, a thumbnail slot (≤ 1.3 x 0.8: a glyph_only() copy
    of a set piece, scaled to fit; None leaves the slot empty), the rule as fit rows. .badge .thumb
    .text .slot"""
    badge = step_badge(n, TURN, radius=0.24)
    slot = Rectangle(width=1.3, height=0.8, stroke_width=0).set_fill(opacity=0).next_to(badge, RIGHT, buff=0.2)
    th = None
    if thumb is not None:
        th = thumb
        if th.width > 1.3 or th.height > 0.8:
            th.scale(min(1.3 / th.width, 0.8 / th.height))
        th.move_to(slot)
    body = fit_rows(text, width - 2.2, size).next_to(slot, RIGHT, buff=0.25)
    if body.height < slot.height:
        body.match_y(slot)
    g = VGroup(badge, slot, body) if th is None else VGroup(badge, slot, th, body)
    g.badge, g.thumb, g.text, g.slot = badge, th, body, slot
    return g


class McqCard(VGroup):
    """The multiple-choice ponder card (script PONDER): YELLOW frame, "Pause and ponder" head, the
    stem (22 pt, fit rows; `code` mono), four option rows A-D (letter in a circle, 22 pt), a
    reserved reason slot under each row (empty until right()/wrong()), the timer bar at the bottom,
    the `illustration` tag on the top edge. Width 11.8; top at y <= 2.95 (clear of the lecture tag).

        card = McqCard(stem, ["the Internet Gateway, …", "the local route", …], answer="C")
        mcq_ponder(self, card)                 # plays: in, then the 10 s timer
        self.play(*card.right("out + replies back · nothing uninvited in"))
        self.play(*card.wrong("A", "makes the subnet public · …"))
        self.play(FadeOut(card))
    .frame .stem .rows[letter] (VGroup(circle-letter, text)) .reasons {letter: Text or None} .bar"""

    LETTERS = "ABCD"

    def __init__(self, stem: str, options, answer: str, seconds: float = 10.0, width: float = 11.8,
                 size: float = 22, top: float = 2.95, **kw):
        super().__init__(**kw)
        if len(options) != 4 or answer not in self.LETTERS:
            raise ValueError("McqCard: four options, answer one of A-D")
        self.answer, self.seconds, self.size = answer, seconds, size
        inner = width - 0.8
        head = label("Pause and ponder", CAPTION + 2, TURN, weight="BOLD")
        stem_m = fit_rows(stem, inner, size)
        rows, slots = {}, {}
        col = VGroup()
        for L, opt in zip(self.LETTERS, options):
            badge = step_badge(L, S.GREY, size=CAPTION, radius=0.21)
            txt = fit_rows(opt, inner - 0.7, size).next_to(badge, RIGHT, buff=0.2)
            if len(txt) > 1:
                txt.align_to(badge, UP).shift(UP * 0.03)
            else:
                txt.match_y(badge)
            r = VGroup(badge, txt)
            slot = Rectangle(width=inner - 0.7, height=0.34, stroke_width=0).set_fill(opacity=0)
            slot.next_to(r, DOWN, buff=0.04).align_to(txt, LEFT)
            rows[L], slots[L] = r, slot
            col.add(VGroup(r, slot))
        col.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        body = VGroup(head, stem_m, col).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        fr = RoundedRectangle(width=width, height=body.height + 0.95, corner_radius=0.2,
                              stroke_color=TURN, stroke_width=3).set_fill(S.BG, 1)
        body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.4 + UP * 0.12)
        bar = Line(fr.get_corner(DOWN + LEFT) + RIGHT * 0.3 + UP * 0.22,
                   fr.get_corner(DOWN + RIGHT) + LEFT * 0.3 + UP * 0.22, color=TURN, stroke_width=4)
        tg = illustration_tag()
        tg.move_to(fr.get_corner(UP + RIGHT) + np.array([-0.35 - tg.width / 2, 0, 0]))
        self.add(fr, body, bar, tg)
        self.frame, self.head, self.stem, self.bar, self.tag = fr, head, stem_m, bar, tg
        self.rows, self.slots = rows, slots
        self.reasons = {L: None for L in self.LETTERS}
        self.shift(np.array([-self.get_center()[0], top - self.get_top()[1], 0]))
        if self.get_bottom()[1] < -3.55:
            self.shift(UP * (-3.55 - self.get_bottom()[1]))
        guard(self.get_top()[1] <= 3.0 and self.get_bottom()[1] >= -3.6,
              f"McqCard {self.height:.2f} tall does not fit under the lecture tag: shorten the stem")

    def _reason(self, L: str, text: str, color: str) -> Text:
        slot = self.slots[L]
        t = fit_rows(text, slot.width, CAPTION, color)
        guard(len(t) == 1, f"reason for {L} must fit one row: {text!r}")
        t.move_to(slot).align_to(slot, LEFT)
        self.reasons[L] = t
        self.add(t)
        _save_op(t, "_swop")
        _set_op(t, 0, "_swop")
        return t

    def right(self, note_: str | None = None) -> list:
        """Animations: the answer row fills YELLOW (letter circle filled, text YELLOW) with a ✓ at
        its right end; `note_` writes in GREEN in its reason slot."""
        L = self.answer
        r = self.rows[L]
        badge, txt = r[0], r[1]
        tick = mono("✓", 26, TURN).next_to(txt, RIGHT, buff=0.2)
        self.add(tick)
        _save_op(tick, "_swop")
        _set_op(tick, 0, "_swop")
        out = [badge[0].animate.set_fill(TURN, 0.9).set_stroke(TURN), badge[1].animate.set_color(S.BG),
               txt.animate.set_color(TURN), _Reveal(tick, "_swop")]
        if note_:
            out.append(_Reveal(self._reason(L, note_, OWN), "_swop", shift=RIGHT * 0.1))
        return out

    def wrong(self, L: str, reason: str) -> list:
        """Animations: the RED one-line reason under option L writes in; L's letter turns RED."""
        if L == self.answer:
            raise ValueError("wrong(): that is the answer")
        t = self._reason(L, reason, ERR)
        return [_Reveal(t, "_swop", shift=RIGHT * 0.1), self.rows[L][0][1].animate.set_color(ERR)]


def mcq_ponder(scene, card: McqCard, run_time: float = 0.6) -> McqCard:
    """Plays: the McqCard fades in, then its timer bar drains over card.seconds. Returns the card
    (still on screen; reveal with card.right()/card.wrong() in the next SAY block)."""
    scene.play(FadeIn(card, scale=0.97), run_time=run_time)
    bar = card.bar
    scene.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
               run_time=card.seconds)
    bar.set_stroke(opacity=0)            # the drained bar leaves no dot behind
    return card


# ================================================================== L16: small glyphs
def arrow_(a, b, color: str = ROUTE, stroke: float = 4, buff: float = 0.08) -> Arrow:
    """The house arrow between two points (or mobjects' centres)."""
    a = a.get_center() if hasattr(a, "get_center") else np.array(a, dtype=float)
    b = b.get_center() if hasattr(b, "get_center") else np.array(b, dtype=float)
    return Arrow(a, b, buff=buff, color=color, stroke_width=stroke, max_tip_length_to_length_ratio=0.25,
                 tip_length=0.2)


def path_points(*items) -> list:
    """Points for Packet.travel: each item a point or a mobject (its centre)."""
    out = []
    for it in items:
        p = it.get_center() if hasattr(it, "get_center") else np.array(it, dtype=float)
        out.append(np.array([p[0], p[1], 0.0]))
    return out


def padlock(h: float = 0.28, color: str = CLOUD) -> VGroup:
    """A small padlock (a private subnet)."""
    body = RoundedRectangle(width=h * 0.9, height=h * 0.62, corner_radius=h * 0.08, stroke_color=color,
                            stroke_width=2).set_fill(color, 0.35)
    shackle = Arc(radius=h * 0.27, start_angle=0, angle=PI, stroke_color=color, stroke_width=2.5)
    shackle.next_to(body, UP, buff=-0.02)
    return _keep(VGroup(shackle, body))


def bell(h: float = 0.45, color: str = ERR) -> VGroup:
    """An alarm bell (S01)."""
    dome = Arc(radius=h * 0.38, start_angle=0, angle=PI, stroke_color=color, stroke_width=3)
    left = Line(dome.get_start(), dome.get_start() + np.array([0.08 * h, -0.42 * h, 0]))
    right = Line(dome.get_end(), dome.get_end() + np.array([-0.08 * h, -0.42 * h, 0]))
    rim = Line(right.get_end() + LEFT * 0.12 * h, left.get_end() + RIGHT * 0.12 * h)
    clap = Dot(rim.get_center() + DOWN * 0.1 * h, radius=0.06 * h * 1.4)
    g = VGroup(dome, left, right, rim).set_stroke(color, 3)
    g.add(clap.set_color(color))
    shape = Polygon(dome.get_start(), left.get_end(), right.get_end(), dome.get_end(), stroke_width=0)
    shape.set_fill(color, 0.25)
    return _keep(VGroup(shape, g))


def door(port: str, color: str = CTR, h: float = 0.55, size: float = CAPTION, label_side=RIGHT) -> VGroup:
    """A door with its mono port label (":9000"): port = door, picks the service. .frame .label"""
    fr = RoundedRectangle(width=h * 0.6, height=h, corner_radius=0.04, stroke_color=color, stroke_width=3) \
        .set_fill(S.BG, 1)
    knob = Dot(fr.get_center() + RIGHT * h * 0.17, radius=0.035, color=color)
    lb = mono(port, size, color).next_to(fr, label_side, buff=0.1)
    g = VGroup(fr, knob, lb)
    g.frame, g.label = fr, lb
    return _keep(g)


def house(text: str, color: str = CLOUD, w: float = 1.0, size: float = CAPTION) -> VGroup:
    """A house outline (an IP = a street address) with its mono number under it. .shape .label"""
    body = Rectangle(width=w, height=w * 0.62, stroke_color=color, stroke_width=3).set_fill(color, 0.08)
    roof = Polygon(body.get_corner(UP + LEFT) + LEFT * 0.08, body.get_corner(UP + RIGHT) + RIGHT * 0.08,
                   body.get_top() + UP * w * 0.38, stroke_color=color, stroke_width=3).set_fill(color, 0.08)
    shape = VGroup(body, roof)
    lb = mono(text, size, INK).next_to(shape, DOWN, buff=0.1)
    g = VGroup(shape, lb)
    g.shape, g.label, g.body = shape, lb, body
    return g


def cylinder(name: str | None = "PostgreSQL", sub: str | None = None, color: str = CLOUD, w: float = 1.5,
             h: float = 1.1, size: float = CAPTION) -> VGroup:
    """A database cylinder; name (serif) under it, sub (mono, e.g. the IP) under that. .body .title .sub"""
    ry = w * 0.14
    top = Ellipse(width=w, height=2 * ry, stroke_color=color, stroke_width=3).set_fill(color, 0.25)
    top.move_to(UP * h / 2)
    side = Line(top.get_left(), [top.get_left()[0], -h / 2, 0], stroke_width=3, color=color)
    side2 = Line(top.get_right(), [top.get_right()[0], -h / 2, 0], stroke_width=3, color=color)
    bottom = Arc(radius=w / 2, start_angle=PI, angle=PI, stroke_color=color, stroke_width=3)
    bottom.stretch_to_fit_height(ry).move_to([0, -h / 2 - ry / 2, 0])
    fill = Rectangle(width=w, height=h, stroke_width=0).set_fill(color, 0.1)
    body = VGroup(fill, side, side2, bottom, top)
    g = VGroup(body)
    g.body, g.title, g.sub = body, None, None
    last = body
    if name:
        t = label(name, size, INK).next_to(body, DOWN, buff=0.1)
        g.add(t)
        g.title, last = t, t
    if sub:
        s = mono(sub, size, color).next_to(last, DOWN, buff=0.06)
        g.add(s)
        g.sub = s
    return g


def gear(r: float = 0.24, color: str = TOOL, teeth: int = 8) -> VGroup:
    """A gear (the JS running in the browser). Spin it with Rotate(g, TAU, about_point=g.get_center())."""
    ring_ = Circle(radius=r * 0.72, stroke_color=color, stroke_width=3).set_fill(color, 0.25)
    hole = Circle(radius=r * 0.25, stroke_color=color, stroke_width=2).set_fill(S.BG, 1)
    ts = VGroup(*[Square(r * 0.32, stroke_width=0).set_fill(color, 1).move_to(UP * r * 0.82)
                  .rotate(k * TAU / teeth, about_point=ORIGIN) for k in range(teeth)])
    return _keep(VGroup(ts, ring_, hole))


def cpu_gauge(level: float = 0.2, text: str = "CPU", w: float = 1.2, color: str = S.GREY) -> VGroup:
    """A small horizontal meter "CPU ▭▭▭" filled to `level` (0..1). .track .fill .label
    .set_level(k) -> anim"""
    lb = label(text, CAPTION, color)
    track = RoundedRectangle(width=w, height=0.22, corner_radius=0.08, stroke_color=color, stroke_width=2)
    track.next_to(lb, RIGHT, buff=0.12)
    fill = Rectangle(width=max(0.02, w * level), height=0.16, stroke_width=0).set_fill(color, 0.8)
    fill.align_to(track, LEFT).shift(RIGHT * 0.03).match_y(track)
    g = VGroup(lb, track, fill)
    g.track, g.fill, g.label = track, fill, lb

    def set_level(k: float):
        tgt = Rectangle(width=max(0.02, w * k), height=0.16, stroke_width=0).set_fill(color, 0.8)
        tgt.align_to(track, LEFT).shift(RIGHT * 0.03).match_y(track)
        return Transform(fill, tgt)
    g.set_level = set_level
    return _keep(g)


def browser_glyph(w: float = 1.5, color: str = BROWSER) -> VGroup:
    """A small browser window without text (put a mono URL next to it). .frame .page"""
    h = w * 0.68
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=color, stroke_width=2.5) \
        .set_fill(PANEL, 1)
    bar = Line(fr.get_corner(UP + LEFT) + DOWN * 0.2, fr.get_corner(UP + RIGHT) + DOWN * 0.2,
               color=color, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.03, color=color) for _ in range(3)]).arrange(RIGHT, buff=0.05)
    dots.move_to(fr.get_corner(UP + LEFT) + np.array([0.2, -0.1, 0]))
    page = Rectangle(width=w - 0.2, height=h - 0.35, stroke_width=0).set_fill(opacity=0)
    page.move_to(fr.get_bottom() + UP * (h - 0.2) / 2)
    g = VGroup(fr, bar, dots, page)
    g.frame, g.page = fr, page
    return g


def internet_cloud(w: float = 2.0, text: str | None = "internet", color: str = INTERNET) -> VGroup:
    """The ORANGE public internet (a cloud outline) with its label under it. .shape .label"""
    sh = cloud(w, color, 0.1)
    g = VGroup(sh)
    g.shape, g.label = sh, None
    if text:
        lb = label(text, CAPTION, color).next_to(sh, DOWN, buff=0.08)
        g.add(lb)
        g.label = lb
    return g


def image_glyph(name: str = IMAGE, digest: str = "sha256:…", w: float = 2.3, size: float = CAPTION) -> VGroup:
    """A TEAL container image: stacked slabs, mono name, GREY digest stamp under it (the digest never
    changes when the image is promoted). .slabs .name .stamp"""
    slabs = VGroup(*[RoundedRectangle(width=w, height=0.2, corner_radius=0.05, stroke_color=CTR, stroke_width=2)
                     .set_fill(CTR, 0.15 + 0.1 * k) for k in range(3)]).arrange(DOWN, buff=0.05)
    nm = mono(name, size, CTR).next_to(slabs, UP, buff=0.1)
    st = tag(digest, S.GREY, size=CAPTION).next_to(slabs, DOWN, buff=0.1)
    g = VGroup(slabs, nm, st)
    g.slabs, g.name, g.stamp = slabs, nm, st
    return g


def secret_manager(text: str = "secret manager", w: float = 2.6) -> VGroup:
    """BLUE box "secret manager" holding a GOLD key glyph. .frame .title .key"""
    t = label(text, CAPTION, INK)
    k = key_glyph(0.3)
    body = VGroup(k, t).arrange(RIGHT, buff=0.2)
    fr = box(max(w, body.width + 0.4), body.height + 0.36, CLOUD, fill_opacity=0.12, stroke=3)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.title, g.key = fr, t, k
    return g


def tunnel(a, b, text: str | None = None, color: str = ROUTE, size: float = CAPTION) -> VGroup:
    """A PINK tunnel between two points (a port publish -p, a bind mount -v): a thick line with a
    dark core and an optional mono label above its middle. Not added. .line .label"""
    a, b = path_points(a, b)
    outer = Line(a, b, color=color, stroke_width=12, stroke_opacity=0.55)
    core = Line(a, b, color=S.BG, stroke_width=4)
    g = VGroup(outer, core)
    g.line, g.label = outer, None
    if text:
        lb = mono(text, size, color).next_to(outer, UP, buff=0.08)
        g.add(lb)
        g.label = lb
    return g


# ================================================================== the packet (everywhere)
class Packet(VGroup):
    """The packet glyph: a small envelope icon and "src → dst" in mono, in a rounded frame of
    `color` (YELLOW in flight, ORANGE a stranger, GREY the browser). Centred at ORIGIN.

        p = Packet("10.0.2.5:52134", "34.x:443").move_to(...)
        self.play(p.travel(path_points(a, b, c)))
        self.play(*p.set_src("NAT-IP:61001")); self.play(*p.settle())
        self.play(p.drop())                       # RED, shrinks away (gone from the scene)
    .src .dst .arrow .icon .frame .slot (chars per field)"""

    def __init__(self, src: str, dst: str, color: str = TURN, size: float = CAPTION, slot: int | None = None,
                 **kw):
        super().__init__(**kw)
        self.size, self.color_ = size, color
        self.slot = slot or len(dst)
        cw = cell_width(size)
        icon_body = Rectangle(width=0.34, height=0.24, stroke_color=color, stroke_width=2).set_fill(color, 0.2)
        flap = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(
            [icon_body.get_corner(UP + LEFT), icon_body.get_center() + DOWN * 0.03, icon_body.get_corner(UP + RIGHT)])
        self.icon = VGroup(icon_body, flap)
        self.src = mono(src, size, INK) if src else _ref(ORIGIN)       # src="": "→ dst" only
        self.arrow = mono("→", size, S.GREY)
        self.dst = mono(dst, size, INK)
        x = 0.0
        self.icon.move_to([x + 0.17, 0, 0])
        x0 = x + 0.5
        ax = x0 + len(src) * cw + 0.12 if src else x0
        self.src.move_to([ax - 0.12, 0, 0], aligned_edge=RIGHT)
        self.arrow.move_to([ax, 0, 0], aligned_edge=LEFT)
        self._dst_x = ax + self.arrow.width + 0.12
        self.dst.move_to([self._dst_x, 0, 0], aligned_edge=LEFT)
        right = self._dst_x + self.slot * cw
        h = mono("|", size).height + 0.2
        self.frame = RoundedRectangle(width=right + 0.2 - (x - 0.08), height=h, corner_radius=0.1,
                                      stroke_color=color, stroke_width=2.5).set_fill(S.BG, 0.95)
        self.frame.move_to([(right + 0.2 + x - 0.08) / 2, 0, 0])
        for m in (self.arrow, self.dst) if not src else (self.src, self.arrow, self.dst):
            m.set_y(0)
        self.add(self.frame, self.icon, self.src, self.arrow, self.dst)
        self.move_to(ORIGIN)
        _keep(self)

    def _swap_field(self, which: str, text: str, color: str) -> list:
        old = getattr(self, which)
        new = mono(text, self.size, color)
        if which == "src":            # the source field ends at the arrow
            new.move_to(old, aligned_edge=RIGHT).set_y(old.get_center()[1])
            guard(new.get_left()[0] >= self.icon.get_right()[0] + 0.05,
                  f"Packet: {text!r} is longer than the source field (build the packet with the longer one)")
        else:
            new.move_to(old, aligned_edge=LEFT).set_y(old.get_center()[1])
            guard(new.get_right()[0] <= self.frame.get_right()[0] - 0.05,
                  f"Packet: {text!r} is longer than the field (pass slot= at construction)")
        setattr(self, which, new)
        return _swap_text(self, old, new)

    def set_src(self, text: str, color: str = TURN) -> list:
        """Animations: the source field swaps to `text` (YELLOW: the field that changed)."""
        return self._swap_field("src", text, color)

    def set_dst(self, text: str, color: str = TURN) -> list:
        """Animations: the destination field swaps to `text` (YELLOW)."""
        return self._swap_field("dst", text, color)

    def settle(self) -> list:
        """Animations: both fields back to white (after a YELLOW flash)."""
        return [self.src.animate.set_color(INK), self.dst.animate.set_color(INK)]

    def recolor(self, color: str) -> list:
        """Animations: the frame and icon take `color` (ORANGE stranger, RED failure)."""
        return [self.frame.animate.set_stroke(color), self.icon.animate.set_stroke(color)]

    def travel(self, points, run_time: float = 1.2, rate_func=smooth, lead: str = "center",
               clamp: bool = True):
        """Animation: the packet moves along the polyline through `points` (it jumps to the first
        point now). lead="center": its centre follows the path; lead="icon": the envelope icon
        does (the label trails to the right: use it near the left edge). clamp=True shifts every
        point so the whole packet stays inside the safe frame (|x| <= 6.55, |y| <= 3.55)."""
        pts = path_points(*points)
        off = self.icon.get_center() - self.get_center() if lead == "icon" else np.zeros(3)
        hw, hh = self.width / 2, self.height / 2
        out = []
        for p in pts:
            c = p - off
            if clamp:
                c = np.array([min(max(c[0], -6.55 + hw), 6.55 - hw), min(max(c[1], -3.55 + hh), 3.55 - hh), 0])
            out.append(c)
        path = _poly([p[:2] for p in out], S.BG, 1)
        self.move_to(out[0])
        return MoveAlongPath(self, path, run_time=run_time, rate_func=rate_func)

    def drop(self, run_time: float = 0.8):
        """Animation: the packet turns RED, then shrinks and fades away (it leaves the scene)."""
        red = AnimationGroup(self.frame.animate.set_stroke(ERR), self.icon.animate.set_stroke(ERR),
                             self.src.animate.set_color(ERR), self.dst.animate.set_color(ERR),
                             self.arrow.animate.set_color(ERR), run_time=run_time * 0.4)
        return Succession(red, FadeOut(self, scale=0.3, run_time=run_time * 0.6))

    def spark_at(self) -> VGroup:
        """A RED spark at the packet's front edge (not added)."""
        return spark(0.18).move_to(self.frame.get_right())

    def ok(self) -> VMobject:
        """A GREEN tick right of the packet (not added)."""
        return tick_mark(0.32).next_to(self.frame, RIGHT, buff=0.12)


# ================================================================== V1 · same container, different street (S02)
class LaptopHost(Piece):
    """V1 laptop half (S02): GREY laptop zone 6.2 x 3.9 with a browser glyph (top left), the host
    door "laptop :9000", a TEAL container "api-service container" holding a PURPLE uvicorn chip and
    a TEAL FastAPI box with its door :9000, three interface sockets on the container's left wall
    (the top one labelled 127.0.0.1), and the PINK -p tunnel from the host door to FastAPI's door.
    Built centred at ORIGIN. Parts: zone browser host_door ctr uvicorn api sockets tunnel.
    .bind_all() / .bind_loopback() -> mobjects (not added) .request_points() -> points"""

    def __init__(self, show=None, port: int = PORT_REPO, **kw):
        super().__init__(**kw)
        names = ("zone", "browser", "host_door", "ctr", "uvicorn", "api", "sockets", "tunnel")
        sh = self._show_set(show, names)
        zone = laptop_zone(6.2, 3.9, "your laptop")
        self.part("zone", zone, "zone" in sh)
        br = browser_glyph(1.3).move_to([-2.25, 1.05, 0])
        self.part("browser", br, "browser" in sh)
        ctr = container_box("api-service container", w=3.7, h=2.7).move_to([1.05, 0.25, 0])
        self.part("ctr", ctr, "ctr" in sh)
        uv = _keep(chip("uvicorn", TOOL, size=CAPTION)).move_to([2.25, 0.45, 0])
        self.part("uvicorn", uv, "uvicorn" in sh)
        api = box(1.9, 0.75, CTR, fill_opacity=0.15, stroke=2.5).move_to([1.75, -0.55, 0])
        api_t = label("FastAPI", CAPTION, INK).move_to(api)
        dr = door(f":{port}", CTR, h=0.5, label_side=DOWN).move_to([0.25, -0.62, 0])
        self.api_door = dr
        self.part("api", VGroup(api, api_t, dr), "api" in sh)
        x_wall = ctr.frame.get_left()[0]
        socks = VGroup(*[Circle(radius=0.09, stroke_color=CTR, stroke_width=2.5).set_fill(S.BG, 1)
                         .move_to([x_wall, y, 0]) for y in (0.9, 0.35, -0.2)])
        lo = mono("127.0.0.1", CAPTION, S.GREY).next_to(socks[0], RIGHT, buff=0.15)
        lo.align_to(socks[0], DOWN).shift(DOWN * 0.02)
        self.sockets = socks
        self.loopback_label = lo
        self.part("sockets", VGroup(socks, lo), "sockets" in sh)
        hd = door(f"laptop :{port}", LAPTOP, h=0.5, label_side=DOWN).move_to([-2.05, -0.75, 0])
        self.host_door = hd
        self.part("host_door", hd, "host_door" in sh)
        tn = tunnel(hd.frame.get_right() + RIGHT * 0.05, dr.frame.get_left() + LEFT * 0.05, "-p")
        self.part("tunnel", tn, "tunnel" in sh)
        self.move_to(ORIGIN)

    def bind_all(self) -> VGroup:
        """A YELLOW bracket around every socket + mono "0.0.0.0 · every interface" left of it
        (not added)."""
        s = self.sockets
        x = s.get_left()[0] - 0.14
        top, bot = s.get_top()[1] + 0.08, s.get_bottom()[1] - 0.08
        br = VMobject(stroke_color=TURN, stroke_width=4).set_points_as_corners(
            [[x + 0.1, top, 0], [x, top, 0], [x, bot, 0], [x + 0.1, bot, 0]])
        t = VGroup(mono("0.0.0.0", CAPTION, TURN), label("every interface", CAPTION, TURN)) \
            .arrange(DOWN, buff=0.06, aligned_edge=RIGHT).next_to(br, LEFT, buff=0.12)
        g = VGroup(br, t)
        g.bracket, g.text = br, t
        return _keep(g)

    def bind_loopback(self) -> VGroup:
        """A RED ring around the 127.0.0.1 socket + chip "loopback · only this container" (not
        added)."""
        r = Circle(radius=0.2, stroke_color=ERR, stroke_width=4).move_to(self.sockets[0])
        c = _keep(tag("loopback · only this container", ERR))
        c.next_to(self.parts["ctr"].frame, DOWN, buff=0.12).align_to(self.parts["ctr"].frame, RIGHT)
        g = VGroup(r, c)
        g.ring, g.chip = r, c
        return _keep(g)

    def request_points(self) -> list:
        """browser -> host door -> (tunnel) -> FastAPI's door: the localhost:9000 request's path."""
        br = self.parts["browser"]
        return path_points(br.get_bottom() + DOWN * 0.3, self.host_door.frame,
                           self.api_door.frame.get_left() + LEFT * 0.25, self.api_door.frame)


class Street(VGroup):
    """V1 (S02): a street of BLUE houses with mono numbers (IP = street address); house 2 shows two
    doors :8000 and :5432 (port = door). ~9.6 x 1.9, centred. .houses .doors .road"""

    def __init__(self, numbers=("10.0.2.3", "10.0.2.4", "10.0.2.5", "10.0.2.6", "10.0.2.7"),
                 big: int = 2, **kw):
        super().__init__(**kw)
        hs = VGroup(*[house(n, CLOUD, w=1.0 if i != big else 2.0) for i, n in enumerate(numbers)])
        hs.arrange(RIGHT, buff=0.35, aligned_edge=DOWN)
        hb = hs[big]
        d1 = door(":8000", CTR, h=0.42, label_side=UP)
        d2 = door(":5432", CLOUD, h=0.42, label_side=UP)
        for d, dx in ((d1, -0.5), (d2, 0.5)):
            d.frame.move_to(hb.body.get_bottom() + np.array([dx, 0.23, 0]))
            d[1].move_to(d.frame.get_center() + RIGHT * 0.1)
            d.label.next_to(hb.shape, UP, buff=0.08).match_x(d.frame)
        road = Line(hs.get_corner(DOWN + LEFT) + np.array([-0.2, 0.42, 0]),
                    hs.get_corner(DOWN + RIGHT) + np.array([0.2, 0.42, 0]), color=S.GREY_DARK, stroke_width=3)
        road.set_y(hs[0].shape.get_bottom()[1] - 0.02)
        self.add(road, hs, d1, d2)
        self.houses, self.doors, self.road = hs, VGroup(d1, d2), road
        self.move_to(ORIGIN)


class ReachTable(Piece):
    """L10 slide 11 redrawn (S02): rows address · who can reach it · getting traffic in; a header
    with the laptop and the cloud; one value column that starts as the laptop's and swaps cell by
    cell to the cloud's (.to_cloud(r) -> anims). 12.0 x 2.6, centred. .cells[r] .heads"""

    ROWS = ("address", "who can reach it", "getting traffic in")
    LAPTOP_VALS = ("localhost / private IP", "not on the internet · your router keeps the world out",
                   "publish the port (-p)")
    CLOUD_VALS = ("public IP and DNS name", "on the internet · firewall closed by default",
                  "load balancer out front")

    def __init__(self, **kw):
        super().__init__(**kw)
        heads = [label(r, CAPTION + 2, S.GREY) for r in self.ROWS]
        cells = [label(v, CAPTION + 2, INK) for v in self.LAPTOP_VALS]
        col_x = max(h.width for h in heads) + 0.6
        y = 0.0
        for h, c in zip(heads, cells):
            h.move_to([0, y, 0], aligned_edge=LEFT)
            c.move_to([col_x, y, 0], aligned_edge=LEFT)
            y -= 0.62
        self.col_title = label("your laptop", CAPTION + 2, LAPTOP).move_to([col_x, 0.7, 0], aligned_edge=LEFT)
        rows = VGroup(*heads, *cells)
        self.part("heads", VGroup(*heads))
        self.part("cells", VGroup(*cells))
        self.part("title", self.col_title)
        fr = box(12.0, rows.height + 1.3, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        fr.move_to(VGroup(rows, self.col_title)).set_x(0)
        VGroup(*self.submobjects).shift(np.array([fr.get_left()[0] + 0.35 - heads[0].get_left()[0], 0, 0]))
        self.add_to_back(fr)
        self.frame, self.heads, self.cells = fr, heads, cells
        self.move_to(ORIGIN)
        guard(all(c.get_right()[0] <= fr.get_right()[0] - 0.2 for c in cells), "ReachTable: a value is too wide")

    def to_cloud(self, r: int) -> list:
        """Animations: value r swaps to the cloud's (and the column title to "the cloud" on r=0)."""
        old = self.cells[r]
        new = label(self.CLOUD_VALS[r], CAPTION + 2, CLOUD).move_to(old, aligned_edge=LEFT)
        guard(new.get_right()[0] <= self.frame.get_right()[0] - 0.2, "ReachTable: cloud value too wide")
        self.cells[r] = new
        out = _swap_text(self.parts["cells"], old, new)
        if r == 0:
            t = label("the cloud", CAPTION + 2, CLOUD).move_to(self.col_title, aligned_edge=LEFT)
            out += _swap_text(self, self.col_title, t)
            self.col_title = t
        return out


class DnsPath(Piece):
    """L16 slide 27 redrawn (S02, S04): the numbered path. GREY browser "api.example.com" (left),
    ORANGE public resolver 1.1.1.1, BLUE Route 53 (authoritative), BLUE ALB api-alb in the public
    subnet 10.0.1.0/24 (right). Steps: 1 browser -> resolver, 2 resolver -> Route 53, 3 Route 53 ->
    resolver (the ALB's IP), 4 resolver -> browser, 5 browser -> ALB (PINK HTTPS :443). 12.4 x 3.3,
    centred; every arrow hidden until .step(k). .node(name) .arrows[k] .badges[k]"""

    def __init__(self, show=("nodes",), **kw):
        super().__init__(**kw)
        br = browser_glyph(1.3).move_to([-5.3, 0.55, 0])
        bt = mono(API_HOST, CAPTION, LAPTOP).next_to(br, DOWN, buff=0.1)
        res = box(2.3, 0.85, SHARED, fill_opacity=0.12, stroke=3).move_to([-1.3, 1.0, 0])
        rt = VGroup(label("public resolver", CAPTION, INK), mono(RESOLVER, CAPTION, SHARED)).arrange(DOWN, buff=0.04)
        rt.move_to(res)
        r53 = box(2.3, 0.85, CLOUD, fill_opacity=0.12, stroke=3).move_to([3.0, 1.0, 0])
        r53t = VGroup(label("Route 53", CAPTION, INK), label("authoritative", CAPTION, S.GREY)).arrange(DOWN, buff=0.04)
        r53t.move_to(r53)
        alb = box(2.0, 0.85, CLOUD, fill_opacity=0.12, stroke=3).move_to([4.7, -1.1, 0])
        albt = VGroup(label("ALB", CAPTION, INK), mono(ALB_NAME, CAPTION, CLOUD)).arrange(DOWN, buff=0.04).move_to(alb)
        sub = label(f"public subnet {PUB_CIDR}", CAPTION, S.GREY).next_to(alb, DOWN, buff=0.1)
        self._nodes = {"browser": br, "resolver": res, "route53": r53, "alb": alb}
        self.part("nodes", VGroup(br, bt, res, rt, r53, r53t, alb, albt, sub), "nodes" in (show or ()))
        specs = [
            (br.get_right() + UP * 0.25, res.get_left() + UP * 0.15, ROUTE, "1"),
            (res.get_right() + UP * 0.15, r53.get_left() + UP * 0.15, ROUTE, "2"),
            (r53.get_left() + DOWN * 0.2, res.get_right() + DOWN * 0.2, ROUTE, "3"),
            (res.get_left() + DOWN * 0.2, br.get_right() + DOWN * 0.1, ROUTE, "4"),
            (br.get_bottom() + DOWN * 0.45 + RIGHT * 0.4, alb.get_left(), ROUTE, "5"),
        ]
        self.arrows, self.badges = [], []
        for k, (a, b, col, n) in enumerate(specs):
            ar = arrow_(a, b, col, stroke=4)
            bd = step_badge(n, TURN, size=CAPTION, radius=0.2)
            mid = ar.get_center()
            off = UP * 0.32 if k in (0, 1) else DOWN * 0.32
            if k == 4:
                off = DOWN * 0.3
            bd.move_to(mid + off)
            self.arrows.append(ar)
            self.badges.append(bd)
            self.part(f"a{k + 1}", VGroup(ar, bd), False)
        lbl3 = mono("ALB-IP", CAPTION, TURN).next_to(self.badges[2], RIGHT, buff=0.15)
        self.part("ip", lbl3, False)
        lbl5 = mono("HTTPS → ALB-IP:443", CAPTION, ROUTE).next_to(self.arrows[4], DOWN, buff=0.1)
        lbl5.shift(RIGHT * 0.6)
        self.part("https", lbl5, False)
        self.move_to(ORIGIN)

    def node(self, name: str):
        return self._nodes[name]

    def step(self, k: int) -> list:
        """Animations: arrow k (1-5) grows and its badge appears (3 adds "ALB-IP", 5 the HTTPS
        label)."""
        out = self.parts_in(f"a{k}")
        if k == 3:
            out += self.parts_in("ip")
        if k == 5:
            out += self.parts_in("https")
        return out


class Gate(VGroup):
    """A security-group gate (S02, slide 11): a GREY vertical bar with a rule card above it
    ("allow · TCP 8000 · source: ALB"). ~2.9 x 1.6, centred. .bar .rule .point() .flash(ok)"""

    def __init__(self, rule: str = "allow · TCP 8000 · source: ALB", **kw):
        super().__init__(**kw)
        self.bar = VGroup(Line(UP * 0.45, DOWN * 0.45, color=S.GREY, stroke_width=6),
                          *[Line(LEFT * 0.12, RIGHT * 0.12, color=S.GREY, stroke_width=3).shift(UP * y)
                            for y in (0.3, 0.0, -0.3)])
        self.rule = _keep(chip(rule, S.GREY, size=CAPTION)).next_to(self.bar, UP, buff=0.15)
        self.add(self.bar, self.rule)
        self.move_to(ORIGIN)

    def point(self):
        return self.bar.get_center()

    def flash(self, ok: bool = True) -> list:
        col = OWN if ok else ERR
        return [Indicate(self.bar, color=col, scale_factor=1.15)]


# ================================================================== V2 · the VPC map, routes and NAT (S01, S03, S08)
class VpcMap(Piece):
    """V2 (S03; S01 and S08 reuse it): in place, x -6.45..6.45, y -3.2..2.9. ORANGE internet (left),
    the Internet Gateway on the VPC's left edge, the BLUE VPC 10.0.0.0/16 cut into three subnets:
    public 10.0.1.0/24 (ALB, NAT Gateway), private app 10.0.2.0/24 (padlock, two TEAL FastAPI
    tasks, the first at 10.0.2.5), private data 10.0.3.0/24 (padlock, PostgreSQL at 10.0.3.7).
    Parts: internet igw vpc public app data alb nat tasks db. Packets travel between
    .anchor(name) points (internet igw edge alb nat task task2 db); .path(*names) -> points.
    .nat_down() / .nat_up() -> anims. .route_spot() -> the point above the first task where a
    compact RouteTable sits. .boxes[name] the shapes"""

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        names = ("internet", "igw", "vpc", "public", "app", "data", "alb", "nat", "tasks", "db")
        sh = self._show_set(show, names)
        b = {}
        inet = internet_cloud(1.55, "internet").move_to([-5.65, 0.5, 0])
        self.part("internet", inet, "internet" in sh)
        vpc = box(10.45, 6.05, CLOUD, fill_opacity=0.03, stroke=3, radius=0.2).move_to([1.2, -0.17, 0])
        vt = VGroup(label("VPC", CAPTION + 2, CLOUD), mono(VPC_CIDR, CAPTION, CLOUD)).arrange(RIGHT, buff=0.2)
        vt.move_to(vpc.get_corner(UP + LEFT) + np.array([0.3 + vt.width / 2, -0.32, 0]))
        self.part("vpc", VGroup(vpc, vt), "vpc" in sh)
        b["vpc"] = vpc
        x_edge = vpc.get_left()[0]
        igw = box(1.25, 0.95, CLOUD, fill=S.BG, fill_opacity=1, stroke=3).move_to([x_edge, 0.5, 0])
        igwt = VGroup(label("Internet", CAPTION, INK), label("Gateway", CAPTION, INK)).arrange(DOWN, buff=0.02).move_to(igw)
        self.part("igw", VGroup(igw, igwt), "igw" in sh)
        b["igw"] = igw
        top, bot = 2.25, -2.95
        cols = {"public": (-3.25, -0.75), "app": (-0.55, 3.75), "data": (3.95, 6.2)}
        heads = {"public": ("public", PUB_CIDR, False), "app": ("private app", APP_CIDR, True),
                 "data": ("private data", DATA_CIDR, True)}
        for k, (x0, x1) in cols.items():
            sb = box(x1 - x0, top - bot, CLOUD, fill_opacity=0.05 if k == "public" else 0.02,
                     stroke=2.5, radius=0.14).move_to([(x0 + x1) / 2, (top + bot) / 2, 0])
            nm, cidr, lock = heads[k]
            ht = VGroup(label(nm, CAPTION, CLOUD), mono(cidr, CAPTION, S.GREY)).arrange(DOWN, buff=0.04)
            ht.move_to([(x0 + x1) / 2, top - 0.45, 0])
            g = VGroup(sb, ht)
            if lock:
                pl = padlock(0.3).next_to(ht[0], RIGHT, buff=0.15)
                g.add(pl)
            self.part(k, g, k in sh)
            b[k] = sb
        alb = box(2.2, 0.85, CLOUD, fill_opacity=0.15, stroke=3).move_to([-2.0, 0.65, 0])
        albt = VGroup(label("ALB", CAPTION, INK), mono(ALB_NAME, CAPTION, CLOUD)).arrange(DOWN, buff=0.03).move_to(alb)
        self.part("alb", VGroup(alb, albt), "alb" in sh)
        b["alb"] = alb
        nat = box(2.2, 0.85, CLOUD, fill_opacity=0.15, stroke=3).move_to([-2.0, -1.55, 0])
        natt = VGroup(label("NAT", CAPTION, INK), label("Gateway", CAPTION, INK)).arrange(DOWN, buff=0.03).move_to(nat)
        self.part("nat", VGroup(nat, natt), "nat" in sh)
        b["nat"] = nat
        self._nat_text = natt
        t1 = box(1.9, 0.75, CTR, fill_opacity=0.15, stroke=3).move_to([1.6, -0.15, 0])
        t1t = label("FastAPI", CAPTION, INK).move_to(t1)
        ip1 = mono(TASK_IP, CAPTION, S.GREY).next_to(t1, DOWN, buff=0.08)
        t2 = box(1.9, 0.75, CTR, fill_opacity=0.15, stroke=3).move_to([1.6, -1.95, 0])
        t2t = label("FastAPI", CAPTION, INK).move_to(t2)
        self.part("tasks", VGroup(t1, t1t, ip1, t2, t2t), "tasks" in sh)
        b["task"], b["task2"] = t1, t2
        db = cylinder("PostgreSQL", DB_IP, CLOUD, w=1.4, h=0.9).move_to([5.07, -0.6, 0])
        self.part("db", db, "db" in sh)
        b["db"] = db.body
        dn = down_chip().next_to(nat, DOWN, buff=0.1)
        self.part("down", dn, False)
        self.boxes = b
        self._anchors = {
            "internet": inet.shape.get_center(), "edge": np.array([x_edge - 1.0, 0.5, 0]),
            "igw": igw.get_center(), "alb": alb.get_center(), "nat": nat.get_center(),
            "task": t1.get_center(), "task2": t2.get_center(), "db": db.body.get_center(),
        }
        self._anchor_mobs = {"internet": inet.shape, "igw": igw, "alb": alb, "nat": nat, "task": t1,
                             "task2": t2, "db": db.body}
        guard(self.get_left()[0] >= -6.6 and self.get_right()[0] <= 6.6 and self.get_top()[1] <= 2.95
              and self.get_bottom()[1] >= -3.6, "VpcMap out of its frame")

    def anchor(self, name: str):
        """Current centre of a node (follows moves): internet igw alb nat task task2 db; "edge" is
        just outside the Internet Gateway."""
        if name == "edge":
            return self.boxes["igw"].get_center() + LEFT * 1.0
        return self._anchor_mobs[name].get_center()

    def path(self, *names) -> list:
        return [self.anchor(n) for n in names]

    def route_spot(self):
        """Where a compact RouteTable (≤ 4.2 wide) sits: centred above the first FastAPI task,
        under the app subnet's header."""
        return self.boxes["task"].get_top() + UP * 0.66

    def nat_down(self) -> list:
        """Animations: the NAT Gateway turns RED and a RED "down" chip appears under it."""
        return [self.boxes["nat"].animate.set_stroke(ERR).set_fill(ERR, 0.15),
                self._nat_text.animate.set_color(ERR), *self.parts_in("down")]

    def nat_up(self) -> list:
        return [self.boxes["nat"].animate.set_stroke(CLOUD).set_fill(CLOUD, 0.15),
                self._nat_text.animate.set_color(INK), *self.parts_out("down")]


class CidrRuler(VGroup):
    """S03's CIDR ruler (slides 5, 7): 32 bit cells, the first `prefix` BLUE ("fixed"), the rest
    white outlines ("vary"), a mono counter "2¹⁶ = 65,536". ~10.6 x 1.5, centred.
    .set_prefix(24) -> anims (cells recolour, counter swaps). .cells .counter .fixed .vary"""

    SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

    def __init__(self, prefix: int = 16, **kw):
        super().__init__(**kw)
        self.prefix = prefix
        self.cells = VGroup(*[Rectangle(width=0.22, height=0.38, stroke_width=1.5) for _ in range(32)])
        self.cells.arrange(RIGHT, buff=0.04)
        for k in range(4):                      # small gaps between the four octets
            for c in self.cells[8 * k:]:
                c.shift(RIGHT * (0.14 if k else 0))
        self._paint(self.cells, prefix)
        self.counter = self._count(prefix).next_to(self.cells, RIGHT, buff=0.35)
        self.fixed = label("fixed", CAPTION, CLOUD)
        self.vary = label("vary", CAPTION, INK)
        self._place_labels(prefix)
        self.add(self.cells, self.counter, self.fixed, self.vary)
        self.move_to(ORIGIN)
        _keep(self)

    def _count(self, prefix):
        n = 32 - prefix
        return mono(f"2{str(n).translate(self.SUP)} = {2 ** n:,}", 24, INK)

    @staticmethod
    def _paint(cells, prefix):
        for i, c in enumerate(cells):
            if i < prefix:
                c.set_stroke(CLOUD, 1.5).set_fill(CLOUD, 0.7)
            else:
                c.set_stroke(INK, 1.5).set_fill(INK, 0.0)

    def _place_labels(self, prefix):
        self.fixed.next_to(VGroup(*self.cells[:prefix]), DOWN, buff=0.12)
        self.vary.next_to(VGroup(*self.cells[prefix:]), DOWN, buff=0.12)

    def set_prefix(self, prefix: int) -> list:
        tgt = self.cells.copy()
        self._paint(tgt, prefix)
        new = self._count(prefix).move_to(self.counter, aligned_edge=LEFT)
        old = self.counter
        self.counter = new
        f2 = label("fixed", CAPTION, CLOUD).next_to(VGroup(*self.cells[:prefix]), DOWN, buff=0.12)
        v2 = label("vary", CAPTION, INK).next_to(VGroup(*self.cells[prefix:]), DOWN, buff=0.12)
        self.prefix = prefix
        return [Transform(self.cells, tgt), *_swap_text(self, old, new),
                self.fixed.animate.move_to(f2), self.vary.animate.move_to(v2)]


class RouteTable(Piece):
    """A route table (slide 13): optional GREY title, header Destination / Gateway, PINK-outlined
    rows of mono destination and serif gateway. Full ~5.4 x 2.0; compact=True (no title, no header,
    ~4.3 x 0.95) is the little route card on a task. Centred at ORIGIN.
    .light(i) -> anims (row YELLOW) .unlight(i) -> anims .bar(i, text=None, thick=False) -> mobject
    (YELLOW bar behind row i, label right of the table; not added) .flash_gateway(i) -> anims
    .rows[i] .dst[i] .gw[i]"""

    def __init__(self, rows=((VPC_CIDR, "local route"), ("0.0.0.0/0", "NAT Gateway")), title: str | None = None,
                 compact: bool = False, width: float | None = None, **kw):
        super().__init__(**kw)
        self.compact = compact
        dsts = [mono(d, CAPTION, INK) for d, _ in rows]
        gws = [label(g, CAPTION, INK) for _, g in rows]
        pad = 0.12 if compact else 0.3
        cw = max(m.width for m in dsts) + (0.22 if compact else 0.45)
        gw_w = max(m.width for m in gws)
        w = width or (pad + cw + gw_w + pad + 0.05)
        pitch = 0.46 if compact else 0.5
        y = 0.0
        self.rows, self.dst, self.gw, self.row_boxes = [], dsts, gws, []
        heads = None
        if not compact:
            heads = VGroup(label("Destination", CAPTION, S.GREY), label("Gateway", CAPTION, S.GREY))
            heads[0].move_to([pad, y, 0], aligned_edge=LEFT)
            heads[1].move_to([pad + cw, y, 0], aligned_edge=LEFT)
            self.part("heads", heads)
            y -= pitch
        for d, g in zip(dsts, gws):
            rb = RoundedRectangle(width=w - 0.1, height=pitch - 0.06, corner_radius=0.06, stroke_color=ROUTE,
                                  stroke_width=2).set_fill(ROUTE, 0.06)
            rb.move_to([0.05 + w / 2 - 0.05, y, 0])
            d.move_to([pad, y, 0], aligned_edge=LEFT)
            g.move_to([pad + cw, y, 0], aligned_edge=LEFT)
            row = VGroup(rb, d, g)
            self.rows.append(row)
            self.row_boxes.append(rb)
            self.part(f"row{len(self.rows) - 1}", row)
            y -= pitch
        body = VGroup(*self.rows) if heads is None else VGroup(heads, *self.rows)
        fr = box(w + 0.1, body.height + (0.3 if compact else 0.4), ROUTE if compact else S.GREY,
                 fill=S.BG, fill_opacity=0.96, radius=0.12, stroke=2 if compact else 2.5)
        fr.move_to(body)
        self.add_to_back(fr)
        self.frame = fr
        self.title = None
        if title:
            t = label(title, CAPTION, S.GREY).next_to(fr, UP, buff=0.08).align_to(fr, LEFT)
            self.part("title", t)
            self.title = t
        self.move_to(ORIGIN)

    def light(self, i: int, color: str = TURN) -> list:
        rb = self.row_boxes[i]
        return [rb.animate.set_stroke(color, 3).set_fill(color, 0.18)]

    def unlight(self, i: int) -> list:
        rb = self.row_boxes[i]
        return [rb.animate.set_stroke(ROUTE, 2).set_fill(ROUTE, 0.06)]

    def bar(self, i: int, text: str | None = None, thick: bool = False, side=RIGHT) -> VGroup:
        """A YELLOW bar over row i (thick=True: a heavier outline) and an optional YELLOW label
        beside the table (side RIGHT, or DOWN under it). Not added. .bar .label"""
        rb = self.row_boxes[i]
        bar_ = RoundedRectangle(width=rb.width + 0.08, height=rb.height + 0.08, corner_radius=0.08,
                                stroke_color=TURN, stroke_width=6 if thick else 3).set_fill(TURN, 0.12)
        bar_.move_to(rb)
        g = VGroup(bar_)
        g.bar, g.label = bar_, None
        if text:
            lb = label(text, CAPTION, TURN)
            if side is DOWN or (isinstance(side, np.ndarray) and side[1] < 0):
                lb.next_to(self.frame, DOWN, buff=0.12)
            else:
                lb.next_to(self.frame, RIGHT, buff=0.2).match_y(rb)
            g.add(lb)
            g.label = lb
        return _keep(g)

    def flash_gateway(self, i: int, color: str = TURN) -> list:
        return [Indicate(self.gw[i], color=color, scale_factor=1.15)]


class NatNotebook(Piece):
    """The NAT notebook (S03, slide 14): a PINK card "NAT table" with the head "inside ↔ outside"
    and `slots` empty line slots. .add_line(inside, outside) -> anims (the next slot writes in)
    .glow(i) -> anims .miss_note() -> mobject (RED "no line → dropped" under the card; not added)
    .lines[i]. ~6.3 x (0.95 + 0.42 per slot), centred."""

    def __init__(self, slots: int = 2, width: float = 6.3, **kw):
        super().__init__(**kw)
        hd = VGroup(label("NAT table", CAPTION, ROUTE), mono("inside ↔ outside", CAPTION, S.GREY)).arrange(RIGHT, buff=0.3)
        pitch = 0.42
        h = 0.95 + pitch * slots
        fr = box(width, h, ROUTE, fill=S.BG, fill_opacity=0.96, radius=0.12, stroke=2.5)
        hd.move_to(fr.get_corner(UP + LEFT) + np.array([0.25 + hd.width / 2, -0.32, 0]))
        sep = Line(fr.get_left() + RIGHT * 0.15, fr.get_right() + LEFT * 0.15, color=S.GREY_DARK, stroke_width=1.5)
        sep.set_y(hd.get_bottom()[1] - 0.1)
        self.add(fr, sep)
        self.part("head", hd)
        self.frame, self.sep, self.width_ = fr, sep, width
        self._pitch = pitch
        self._slots = slots
        self.lines = []
        self.move_to(ORIGIN)

    def add_line(self, inside: str, outside: str) -> list:
        if len(self.lines) >= self._slots:
            raise ValueError("NatNotebook: no free slot (pass slots=)")
        y = self.sep.get_y() - 0.3 - len(self.lines) * self._pitch
        t = mono(f"{inside} ↔ {outside}", CAPTION, INK)
        t.move_to([self.frame.get_left()[0] + 0.25 + t.width / 2, y, 0])
        guard(t.get_right()[0] <= self.frame.get_right()[0] - 0.15, "NatNotebook: the line is too wide")
        self.lines.append(t)
        _stage_hidden(self, t, "_hop")
        return [_Reveal(t, "_hop", shift=RIGHT * 0.1)]

    def glow(self, i: int) -> list:
        return [Indicate(self.lines[i], color=TURN, scale_factor=1.08)]

    def miss_note(self, text: str = "no line → dropped") -> Text:
        return mono(text, CAPTION, ERR).next_to(self.frame, DOWN, buff=0.12)


# ================================================================== V3 · two request paths (S04)
class TwoPaths(Piece):
    """V3 (S04, slide 64): in place, x -6.45..6.45, y -3.2..2.8. Top left: the visitor's laptop
    (GREY zone) with a browser; bottom left: the BLUE static host / CDN app.example.com; right: the
    BLUE VPC with the public subnet (ALB, NAT Gateway hidden until .nat_one_way()) and the private
    app subnet ("FastAPI tasks ×3"). Parts: visitor static vpc alb nat tasks files gear.
    .deliver() -> anims (HTML CSS JS fly from the static host into the browser) .unpack() ->
    anims (the files fade, the JS gear appears) .spin(turns=1) -> anim .outline() -> anims (YELLOW
    traces of the VPC border and the visitor's laptop) .nat_one_way() -> anims (NAT + a PINK arrow
    out) .anchor(name): browser visitor_door edge internet alb task static nat"""

    def __init__(self, show=None, **kw):
        super().__init__(**kw)
        names = ("visitor", "static", "vpc", "alb", "tasks", "files", "gear", "nat")
        sh = self._show_set(show, names) - {"files", "gear", "nat"} if show is None else set(show)
        zone = laptop_zone(4.9, 2.6, "visitor's laptop").move_to([-4.05, 1.45, 0])
        br = browser_glyph(1.6).move_to([-5.4, 1.75, 0])
        url = mono(APP_HOST, CAPTION, LAPTOP).next_to(br, RIGHT, buff=0.15).align_to(br, UP)
        dr = door(":9000", LAPTOP, h=0.4, label_side=RIGHT).move_to([-3.05, 0.95, 0])
        dr_note = label("nothing listens", CAPTION, S.GREY).next_to(dr, DOWN, buff=0.06).align_to(dr, LEFT)
        self.part("visitor", VGroup(zone, br, url), "visitor" in sh)
        self.part("door", VGroup(dr, dr_note), False)
        self.browser, self.vzone, self.vdoor = br, zone, dr
        st = box(3.4, 1.0, CLOUD, fill_opacity=0.12, stroke=3).move_to([-4.6, -2.3, 0])
        stt = VGroup(label("static host / CDN", CAPTION, INK), mono(APP_HOST, CAPTION, CLOUD)).arrange(DOWN, buff=0.03)
        stt.move_to(st)
        self.part("static", VGroup(st, stt), "static" in sh)
        self.static = st
        vpc = box(6.1, 6.0, CLOUD, fill_opacity=0.03, stroke=3, radius=0.2).move_to([3.35, -0.2, 0])
        vt = VGroup(label("VPC", CAPTION + 2, CLOUD), mono(VPC_CIDR, CAPTION, CLOUD)).arrange(RIGHT, buff=0.2)
        vt.move_to(vpc.get_corner(UP + LEFT) + np.array([0.3 + vt.width / 2, -0.32, 0]))
        pub = box(2.6, 4.8, CLOUD, fill_opacity=0.05, stroke=2.5).move_to([1.85, -0.5, 0])
        pubt = VGroup(label("public", CAPTION, CLOUD), mono(PUB_CIDR, CAPTION, S.GREY)).arrange(DOWN, buff=0.03)
        pubt.move_to([pub.get_x(), pub.get_top()[1] - 0.45, 0])
        app = box(2.6, 4.8, CLOUD, fill_opacity=0.02, stroke=2.5).move_to([4.75, -0.5, 0])
        appt = VGroup(label("private app", CAPTION, CLOUD), mono(APP_CIDR, CAPTION, S.GREY)).arrange(DOWN, buff=0.03)
        appt.move_to([app.get_x(), app.get_top()[1] - 0.45, 0])
        lk = padlock(0.28).next_to(appt[0], RIGHT, buff=0.1)
        self.part("vpc", VGroup(vpc, vt, pub, pubt, app, appt, lk), "vpc" in sh)
        self.vpc_box = vpc
        alb = box(2.0, 0.85, CLOUD, fill_opacity=0.15, stroke=3).move_to([1.85, 0.6, 0])
        albt = VGroup(label("ALB", CAPTION, INK), mono(ALB_NAME, CAPTION, CLOUD)).arrange(DOWN, buff=0.03).move_to(alb)
        self.part("alb", VGroup(alb, albt), "alb" in sh)
        self.alb = alb
        tk = VGroup(*[box(1.9, 0.6, CTR, fill_opacity=0.15, stroke=2.5) for _ in range(3)]).arrange(DOWN, buff=0.12)
        tk.move_to([4.75, -0.15, 0])
        tkt = label("FastAPI tasks ×3", CAPTION, INK).next_to(tk, DOWN, buff=0.12)
        self.part("tasks", VGroup(tk, tkt), "tasks" in sh)
        self.tasks = tk
        nat = box(2.0, 0.85, CLOUD, fill_opacity=0.15, stroke=3).move_to([1.85, -1.75, 0])
        natt = VGroup(label("NAT", CAPTION, INK), label("Gateway", CAPTION, INK)).arrange(DOWN, buff=0.03).move_to(nat)
        out_ar = arrow_(nat.get_left(), nat.get_left() + LEFT * 1.3, ROUTE)
        out_l = label("out only", CAPTION, ROUTE).next_to(out_ar, LEFT, buff=0.12)
        self.part("nat", VGroup(nat, natt), "nat" in sh)
        self.part("nat_out", VGroup(out_ar, out_l), False)
        self.nat = nat
        files = VGroup(*[VGroup(file_glyph(0.42, c), mono(n, CAPTION, c)).arrange(DOWN, buff=0.04)
                         for n, c in (("HTML", INK), ("CSS", INK), ("JS", TURN))]).arrange(RIGHT, buff=0.25)
        files.next_to(st, UP, buff=0.2)
        self.part("files", files, "files" in sh)
        self.files = files
        gr = gear(0.26).next_to(url, DOWN, buff=0.3).align_to(url, LEFT).shift(RIGHT * 0.1)
        gl = mono("JS", CAPTION, TURN).next_to(gr, RIGHT, buff=0.12)
        self.part("gear", VGroup(gr, gl), "gear" in sh)
        self.gear_ = gr
        guard(self.get_left()[0] >= -6.6 and self.get_right()[0] <= 6.6 and self.get_top()[1] <= 2.95
              and self.get_bottom()[1] >= -3.6, "TwoPaths out of its frame")

    def anchor(self, name: str):
        pts = {"browser": self.browser.get_center(), "visitor_door": self.vdoor.frame.get_center(),
               "edge": self.vpc_box.get_left() + LEFT * 0.35 + UP * 0.8,
               "internet": np.array([-1.3, 0.2, 0]), "alb": self.alb.get_center(),
               "task": self.tasks[0].get_center(), "static": self.static.get_center(),
               "nat": self.nat.get_center()}
        return pts[name]

    def deliver(self, run_time: float = 1.4) -> list:
        """Animations: the HTML / CSS / JS files appear on the static host and fly into the browser
        (they end over the browser page)."""
        out = []
        if getattr(self.files, "hidden", False):
            out += self.parts_in("files")
        return out + [self.files.animate(run_time=run_time, rate_func=rush_into).move_to(self.browser.page)]

    def unpack(self) -> list:
        """Animations: the delivered files fade into the page and the JS gear appears."""
        return self.parts_out("files") + self.parts_in("gear")

    def spin(self, turns: float = 1.0, run_time: float = 1.5):
        return Rotate(self.gear_, angle=-TAU * turns, about_point=self.gear_.get_center(), run_time=run_time,
                      rate_func=linear)

    def outline(self) -> list:
        """Animations: YELLOW traces run round the VPC's border and the visitor's laptop."""
        return [ShowPassingFlash(self.vpc_box.copy().set_stroke(TURN, 6).set_fill(opacity=0), time_width=0.6),
                ShowPassingFlash(self.vzone.frame.copy().set_stroke(TURN, 6).set_fill(opacity=0), time_width=0.6)]

    def nat_one_way(self) -> list:
        return self.parts_in("nat", "nat_out")

    def door_in(self) -> list:
        """Animations: the visitor's empty door ":9000 · nothing listens" appears."""
        return self.parts_in("door")


class FrontDoor(VGroup):
    """Slide 32 layout B (S04): GREY browser -> one BLUE public front door app.example.com (ALB or
    Nginx) in the public subnet; PINK arrows "/" -> TEAL Next.js server and "/api/*" -> TEAL FastAPI
    10.0.2.5:8000 in the private app subnet. ~8.4 x 3.0, centred. .browser .door .next .api
    .arrows (in, root, api) — FadeIn parts in order; add lecture_pic_tag()."""

    def __init__(self, **kw):
        super().__init__(**kw)
        br = browser_glyph(1.2).move_to([-3.6, 0, 0])
        drt = VGroup(label("front door", CAPTION, INK), mono(APP_HOST, CAPTION, CLOUD)).arrange(DOWN, buff=0.03)
        dr = box(drt.width + 0.4, 0.95, CLOUD, fill_opacity=0.14, stroke=3).move_to([-0.6, 0, 0])
        drt.move_to(dr)
        nx = box(2.3, 0.7, CTR, fill_opacity=0.14, stroke=2.5).move_to([3.0, 1.0, 0])
        nxt = label("Next.js server", CAPTION, INK).move_to(nx)
        apt = VGroup(label("FastAPI", CAPTION, INK), mono(f"{TASK_IP}:8000", CAPTION, CTR)).arrange(DOWN, buff=0.03)
        ap = box(apt.width + 0.4, 0.95, CTR, fill_opacity=0.14, stroke=2.5).move_to([3.0, -1.0, 0])
        apt.move_to(ap)
        nx.match_width(ap, stretch=True).match_x(ap)
        nxt.move_to(nx)
        a_in = arrow_(br.get_right(), dr.get_left())
        a_root = arrow_(dr.get_right(), nx.get_left())
        a_api = arrow_(dr.get_right(), ap.get_left())
        l_root = mono("/", CAPTION, ROUTE).next_to(a_root.get_center(), UP + LEFT, buff=0.08)
        l_api = mono("/api/*", CAPTION, ROUTE).next_to(a_api.get_center(), DOWN + LEFT, buff=0.08)
        self.browser, self.door, self.next, self.api = br, VGroup(dr, drt), VGroup(nx, nxt), VGroup(ap, apt)
        self.arrows = VGroup(a_in, VGroup(a_root, l_root), VGroup(a_api, l_api))
        self.add(br, self.door, self.next, self.api, self.arrows)
        self.move_to(ORIGIN)


class RuleCards(VGroup):
    """Slide 24's two cards (S04): the GREEN-outlined Nginx rule "location /api/ { proxy_pass
    http://10.0.2.5:8000; }" = the BLUE-outlined ALB rule "listener :443 · path /api/* ->
    fastapi-tg · fastapi-tg -> targets :8000". Stacked, ~11.4 x 2.6, centred. .nginx .alb .eq .ip
    (the 10.0.2.5 glyphs in the Nginx card) .vpc (a small BLUE outline round the IP)"""

    def __init__(self, **kw):
        super().__init__(**kw)
        ng_line = f"location /api/ {{ proxy_pass http://{TASK_IP}:8000; }}"
        self.nginx = mono_card([ng_line], OWN, header="Nginx")
        self.alb = mono_card([f"listener :443 · path /api/* -> {TG_NAME}", f"{TG_NAME} -> targets :8000"],
                             CLOUD, header="ALB rule")
        self.eq = mono("=", 30, TURN)
        VGroup(self.nginx, self.eq, self.alb).arrange(DOWN, buff=0.15)
        row = self.nginx.rows[0]
        i = ng_line.index(TASK_IP)
        self.ip = glyph_range(row, i, i + len(TASK_IP))
        self.vpc = RoundedRectangle(width=self.ip.width + 0.12, height=self.ip.height + 0.22, corner_radius=0.06,
                                    stroke_color=CLOUD, stroke_width=2.5).move_to(self.ip)
        self.add(self.nginx, self.eq, self.alb, self.vpc)
        self.move_to(ORIGIN)


# ================================================================== V4 · one image, many startups (S05)
class ImageConveyor(VGroup):
    """V4 (S05, slide 21): a belt with stops (dev, staging, prod), stop labels under it. Belt at
    y 0 before you move it; width 11.6. .stop_point(i) (on the belt, where an image sits)
    .carry(mob, i, run_time=1.0) -> anim (mob slides so its bottom sits on stop i) .check(i) ->
    YELLOW ✓ under the stop label (not added) .belt .labels"""

    def __init__(self, stops=("dev", "staging", "prod"), width: float = 11.6, **kw):
        super().__init__(**kw)
        self.belt = VGroup(Line(LEFT * width / 2, RIGHT * width / 2, color=S.GREY, stroke_width=4),
                           *[Circle(radius=0.12, stroke_color=S.GREY, stroke_width=2).move_to([x, -0.14, 0])
                             for x in np.linspace(-width / 2 + 0.3, width / 2 - 0.3, 12)])
        xs = np.linspace(-width / 2 + width / (2 * len(stops)), width / 2 - width / (2 * len(stops)), len(stops))
        self.xs = list(xs)
        self.labels = VGroup(*[label(s, CAPTION + 2, INK).move_to([x, -0.6, 0]) for s, x in zip(stops, xs)])
        self.ticks = VGroup(*[Line([x, 0.1, 0], [x, -0.1, 0], color=S.GREY, stroke_width=3) for x in xs])
        self.add(self.belt, self.ticks, self.labels)

    def stop_point(self, i: int):
        return np.array([self.ticks[i].get_x(), self.belt[0].get_y(), 0])

    def carry(self, mob, i: int, run_time: float = 1.0):
        p = self.stop_point(i)
        return mob.animate(run_time=run_time).shift(
            np.array([p[0] - mob.get_center()[0], p[1] + 0.08 - mob.get_bottom()[1], 0]))

    def check(self, i: int) -> VMobject:
        return mono("✓", 24, TURN).next_to(self.labels[i], DOWN, buff=0.08)


class LayerStack(VGroup):
    """V4 contrast (S05): an image's layer stack (TEAL slabs, bottom to top) and its config card on
    top holding "ENV LLM_API_KEY=…" with a GOLD key glyph. 4.0 wide. .xray() -> anims (the layers
    ghost to outlines, the key glyph glows RED with a RED ring round the config card) .layers
    .config .key"""

    def __init__(self, layers=None, key_line: str = "ENV LLM_API_KEY=…", width: float = 4.0, **kw):
        super().__init__(**kw)
        layers = layers or ["base OS", "Python + uv", "dependencies", "app code"]
        self.layers = VGroup(*[layer_bar(t, width, 0.48, CTR, size=CAPTION) for t in reversed(layers)])
        self.layers.arrange(DOWN, buff=0.06)
        k = key_glyph(0.26)
        t = mono(key_line, CAPTION, INK)
        body = VGroup(k, t).arrange(RIGHT, buff=0.15)
        fr = box(width, body.height + 0.3, CTR, fill=S.BG, fill_opacity=1, stroke=2.5, radius=0.08)
        body.move_to(fr)
        cap = label("image config", CAPTION, S.GREY).next_to(fr, UP, buff=0.06).align_to(fr, LEFT)
        self.config = VGroup(fr, body, cap)
        self.key, self.key_text = k, t
        self.config.next_to(self.layers, UP, buff=0.12)
        self.add(self.layers, self.config)
        self.move_to(ORIGIN)
        guard(body.width <= width - 0.3, "LayerStack: the key line is too wide")

    def xray(self) -> list:
        out = [L.box.animate.set_fill(CTR, 0.04) for L in self.layers]
        out += [self.key.animate.set_stroke(ERR).set_fill(ERR, 0.5),
                self.config[0].animate.set_stroke(ERR, 3), self.key_text.animate.set_color(ERR)]
        return out


# ================================================================== V5 · the connection budget (S06)
class SlotGrid(VGroup):
    """V5 (S06): the database as a BLUE panel of `n` socket slots (cols per row), title above.
    ~4.6 x 4.6 for 100. .fill(k, colour) -> (slot indices, anims): the next k free slots get plugs
    of `colour` .free() -> number of free slots .slot(i) .slots .pipes(point, idx, colour=ROUTE) ->
    VGroup of lines from `point` to those slots (not added) .used"""

    def __init__(self, n: int = 100, cols: int = 10, cell: float = 0.36, title: str = "database · 100 connections", **kw):
        super().__init__(**kw)
        self.slots = VGroup(*[RoundedRectangle(width=cell * 0.78, height=cell * 0.78, corner_radius=0.04,
                                               stroke_color=CLOUD, stroke_width=1.5).set_fill(S.BG, 1)
                              for _ in range(n)])
        self.slots.arrange_in_grid(n // cols, cols, buff=cell * 0.22)
        fr = box(self.slots.width + 0.4, self.slots.height + 0.4, CLOUD, fill_opacity=0.08, stroke=3)
        fr.move_to(self.slots)
        self.title = label(title, CAPTION, CLOUD).next_to(fr, UP, buff=0.1)
        self.frame = fr
        self.used = 0
        self.plugs = VGroup()
        self.add(fr, self.slots, self.title, self.plugs)
        self.move_to(ORIGIN)

    def slot(self, i: int):
        return self.slots[i]

    def free(self) -> int:
        return len(self.slots) - self.used

    def fill(self, k: int, color: str = SHARED, lag: float = 0.02):
        """(indices, anims): the next min(k, free) slots plug in `color`; indices beyond the free
        ones are not returned (the caller sparks the rest RED)."""
        k2 = min(k, self.free())
        idx = list(range(self.used, self.used + k2))
        self.used += k2
        plugs = [Square(self.slots[i].width * 0.62, stroke_width=0).set_fill(color, 0.95).move_to(self.slots[i])
                 for i in idx]
        for p in plugs:
            self.plugs.add(p)
            _save_op(p, "_swop")
            _set_op(p, 0, "_swop")
        anims = [LaggedStart(*[_Reveal(p, "_swop", scale=1.4) for p in plugs], lag_ratio=lag)] if plugs else []
        return idx, anims

    def pipes(self, point, idx, color: str = ROUTE, stroke: float = 1.5) -> VGroup:
        p = path_points(point)[0]
        return VGroup(*[Line(p, self.slots[i].get_center(), color=color, stroke_width=stroke, stroke_opacity=0.7)
                        for i in idx])


class Autoscaler(Piece):
    """V5 (S06, slide 52): four boxes in a row — Signal (measure CPU, concurrent requests or queue
    depth) -> Policy (PURPLE: target · min · max) -> Desired count (a mono number) -> Capacity
    (enough places to run). ~12.4 x 1.9, centred. .set_count(n) -> anims .set_max(n) -> anims
    (the policy's "max" value swaps) .caption() -> YELLOW "Downstream limits still bound the
    result." under the row (not added) .boxes[name] (signal policy count capacity)"""

    def __init__(self, count: int = 3, max_: str = "?", **kw):
        super().__init__(**kw)
        specs = [("signal", "Signal", ["CPU · requests", "queue depth"], S.GREY),
                 ("policy", "Policy", ["target · min", f"max = {max_}"], TOOL),
                 ("count", "Desired count", [str(count)], S.GREY),
                 ("capacity", "Capacity", ["places to run"], S.GREY)]
        self.boxes, self.texts = {}, {}
        cards = []
        for key, head, lines, col in specs:
            h = label(head, CAPTION + 2, col if key == "policy" else INK)
            body = VGroup(*[(mono(s, 26, TURN) if key == "count" else label(s, CAPTION, S.GREY)) for s in lines])
            body.arrange(DOWN, buff=0.04)
            g = VGroup(h, body).arrange(DOWN, buff=0.1)
            fr = box(2.55, 1.45, col, fill_opacity=0.1 if key == "policy" else 0.05, stroke=3 if key == "policy" else 2.5)
            g.move_to(fr)
            card = VGroup(fr, g)
            cards.append(card)
            self.boxes[key] = fr
            self.texts[key] = body
        VGroup(*cards).arrange(RIGHT, buff=0.7)
        for a, b in zip(cards, cards[1:]):
            self.add(arrow_(a.get_right(), b.get_left(), S.GREY, stroke=3))
        for key, c in zip(("signal", "policy", "count", "capacity"), cards):
            self.part(key, c)
        self.count = count
        self.move_to(ORIGIN)
        guard(self.width <= 12.9, f"Autoscaler {self.width:.2f} wide")

    def set_count(self, n: int) -> list:
        old = self.texts["count"][0]
        new = mono(str(n), 26, TURN).move_to(old)
        self.count = n
        out = _swap_text(self.texts["count"], old, new)
        return out

    def set_max(self, n) -> list:
        old = self.texts["policy"][1]
        new = label(f"max = {n}", CAPTION, TURN).move_to(old)
        return _swap_text(self.texts["policy"], old, new)

    def caption(self, text: str = "Downstream limits still bound the result.") -> Text:
        return label(text, CAPTION + 2, TURN).next_to(self, DOWN, buff=0.25)


class Replica(VGroup):
    """V5 (S06): a TEAL replica box "replica i" with a GREEN pool bar "pool 20" under the title and a
    low GREY cpu gauge. 1.9 x 1.4, centred. .frame .pool .cpu .pool_point() (where its pipes start)"""

    def __init__(self, i: int, pool: int = 20, **kw):
        super().__init__(**kw)
        fr = box(1.9, 1.4, CTR, fill_opacity=0.12, stroke=3)
        t = label(f"replica {i}", CAPTION, INK).move_to(fr.get_top() + DOWN * 0.27)
        pb = RoundedRectangle(width=1.5, height=0.32, corner_radius=0.08, stroke_color=OWN, stroke_width=2) \
            .set_fill(OWN, 0.25).next_to(t, DOWN, buff=0.08)
        pt = label(f"pool {pool}", CAPTION, OWN).move_to(pb)
        cpu = cpu_gauge(0.15, w=0.7).next_to(pb, DOWN, buff=0.08)
        self.frame, self.pool, self.cpu = fr, VGroup(pb, pt), cpu
        self.add(fr, t, self.pool, cpu)
        self.move_to(ORIGIN)

    def pool_point(self):
        return self.frame.get_right()


# ================================================================== V6 · two shapes of data, one engine (S07)
def req_table(name: str, cols=("id", "…"), color: str = OWN, w: float = 1.7) -> VGroup:
    """A GREEN mini table chip: the table name (mono) over its column rows. .head .cols .frame"""
    hd = mono(name, CAPTION, color)
    cs = VGroup(*[mono(c, CAPTION, INK) for c in cols]).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
    body = VGroup(hd, cs).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    fr = box(max(w, body.width + 0.35), body.height + 0.3, color, fill=S.BG, fill_opacity=0.96, stroke=2.5, radius=0.1)
    body.move_to(fr)
    sep = Line(fr.get_left() + RIGHT * 0.08, fr.get_right() + LEFT * 0.08, color=color, stroke_width=1.5)
    sep.set_y((hd.get_bottom()[1] + cs.get_top()[1]) / 2)
    g = VGroup(fr, sep, body)
    g.head, g.cols, g.frame = hd, cs, fr
    return _keep(g)


def fk_line(a, b, color: str = ROUTE) -> VGroup:
    """The PINK foreign-key line between two req_tables (a's right edge to b's left) with "FK"."""
    p, q = a.get_right(), b.get_left()
    ln = Line(p, q, color=color, stroke_width=3)
    t = mono("FK", CAPTION, color).next_to(ln, UP, buff=0.06)
    return _keep(VGroup(ln, t))


def txn_bracket(mob, text: str = "transaction: all or nothing", color: str = OWN) -> VGroup:
    """A GREEN bracket under `mob` with its label (the transaction requirement). .bracket .label"""
    l, r = mob.get_left()[0] - 0.1, mob.get_right()[0] + 0.1
    y = mob.get_bottom()[1] - 0.15
    br = VMobject(stroke_color=color, stroke_width=3).set_points_as_corners(
        [[l, y + 0.12, 0], [l, y, 0], [r, y, 0], [r, y + 0.12, 0]])
    t = label(text, CAPTION, color).next_to(br, DOWN, buff=0.08)
    g = VGroup(br, t)
    g.bracket, g.label = br, t
    return _keep(g)


def vector_chip(text: str = "find the 5 most similar cheeses", color: str = ROUTE) -> VGroup:
    """A PINK vector requirement chip: a dot with distance rays to five neighbours, then the text.
    .chip .rays"""
    c = chip(text, color, size=CAPTION)
    rng = np.random.default_rng(16)
    q = Dot(radius=0.06, color=TURN)
    pts = [np.array([np.cos(a), np.sin(a), 0]) * r for a, r in zip(np.linspace(0, TAU, 6)[:5] + 0.4,
                                                                    rng.uniform(0.22, 0.38, 5))]
    rays = VGroup(*[Line(ORIGIN, p, color=color, stroke_width=2) for p in pts],
                  *[Dot(p, radius=0.045, color=color) for p in pts], q)
    rays.next_to(c, LEFT, buff=0.15)
    g = VGroup(rays, c)
    g.chip, g.rays = c, rays
    return _keep(g)


class ChipSorter(Piece):
    """V6 (S07, slides 65-66): three candidate boxes in a row — TEAL "ChromaDB on a VM", BLUE
    "PostgreSQL service + pgvector", BLUE "vector search service" — each with a GREY note line and
    room for three chips. ~12.4 x 2.6, centred. .box(i) .slot(i, k) -> point .land(mob, i, k=0) ->
    anim (mob moves into slot k of box i) .bounce(mob, i) -> anims (dips into box i, the box
    flashes RED, mob returns) .names"""

    NAMES = (("ChromaDB on a VM", CTR, "team patches + backs up"),
             ("PostgreSQL service\n+ pgvector", CLOUD, "relational + vector"),
             ("vector search service", CLOUD, "vectors only"))

    def __init__(self, names=None, w: float = 3.9, h: float = 2.7, **kw):
        super().__init__(**kw)
        names = names or self.NAMES
        self._boxes = []
        for k, (nm, col, sub) in enumerate(names):
            fr = box(w, h, col, fill_opacity=0.06, stroke=3)
            t = VGroup(*[label(r, CAPTION, INK) for r in nm.split("\n")]).arrange(DOWN, buff=0.04)
            t.next_to(fr.get_top(), DOWN, buff=0.14)
            s = label(sub, CAPTION, S.GREY).next_to(t, DOWN, buff=0.05)
            guard(max(t.width, s.width) <= w - 0.2, f"ChipSorter: {nm!r} wider than its box")
            g = VGroup(fr, t, s)
            self._boxes.append(fr)
            self.part(f"b{k}", g)
        VGroup(*[self.parts[f"b{k}"] for k in range(len(names))]).arrange(RIGHT, buff=0.35)
        self.names = [n.replace("\n", " ") for n, _, _ in names]
        self.move_to(ORIGIN)
        guard(self.width <= 12.9, f"ChipSorter {self.width:.2f} wide")

    def box(self, i: int):
        return self._boxes[i]

    def slot(self, i: int, k: int = 0):
        fr = self._boxes[i]
        return fr.get_bottom() + UP * (0.35 + 0.42 * k)

    def land(self, mob, i: int, k: int = 0, run_time: float = 0.7):
        return mob.animate(run_time=run_time).move_to(self.slot(i, k))

    def bounce(self, mob, i: int, run_time: float = 0.9) -> list:
        start = mob.get_center()
        dip = self._boxes[i].get_top() + DOWN * 0.15
        fr = self._boxes[i]
        return [Succession(mob.animate(run_time=run_time * 0.45).move_to(dip),
                           mob.animate(run_time=run_time * 0.55).move_to(start)),
                Succession(Indicate(fr, color=ERR, scale_factor=1.03, run_time=run_time))]


class DbTable(VGroup):
    """S07: the `cheeses` table of the PostgreSQL box: GREEN relational columns (mono) in a card;
    .add_column(text, colour=TOOL) -> anims (a PURPLE `embedding vector(256)` column writes in
    beside them). .frame .cols .head"""

    def __init__(self, name: str = "cheeses", cols=("id", "name", "in_stock"),
                 room_for: str = "embedding vector(256)", **kw):
        super().__init__(**kw)
        self.head = mono(name, CAPTION, OWN)
        self.cols = VGroup(*[chip(c, OWN, size=CAPTION, font=MONO) for c in cols]).arrange(RIGHT, buff=0.12)
        self.cols.next_to(self.head, DOWN, buff=0.12, aligned_edge=LEFT)
        extra = chip(room_for, TOOL, size=CAPTION, font=MONO).width + 0.6
        self.frame = box(self.cols.width + extra, self.cols.height + self.head.height + 0.55, OWN,
                         fill=S.BG, fill_opacity=0.96, stroke=2.5)
        body = VGroup(self.head, self.cols)
        self.frame.move_to(body).align_to(body, LEFT).shift(LEFT * 0.25)
        self.add(self.frame, self.head, self.cols)
        self.move_to(ORIGIN)

    def add_column(self, text: str = "embedding vector(256)", color: str = TOOL) -> list:
        c = chip(text, color, size=CAPTION, font=MONO).next_to(self.cols, RIGHT, buff=0.12)
        guard(c.get_right()[0] <= self.frame.get_right()[0] - 0.1, "DbTable: the new column does not fit")
        self.add(c)
        _save_op(c, "_swop")
        _set_op(c, 0, "_swop")
        self.new_col = c
        return [_Reveal(c, "_swop", shift=RIGHT * 0.2)]
