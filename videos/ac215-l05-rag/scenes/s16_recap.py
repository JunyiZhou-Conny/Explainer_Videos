"""S16 · Tear down, a stale index, recap (the end of part 2: README "Run Container" step 3 with extras,
then "Agents (L06)" as a preview; the four questions; five test-yourself questions). Lecture:
B74–B76, A63 (script: B68–B76, A63).

Beats (script.md "## S16", one voiceover block each):
 0  No lecture tag. TRACKER Run 3 · extra. V2 above the strip (fit_top), as the restart of S10 left
    it: laptop zone (llm-rag/, secrets/ + GOLD key, docker-volumes/chromadb/, the :8000 door), the CLI
    box (/app, /secrets, /.venv), the Chroma box (/data, the cylinder, :8000, its name), the rail,
    the PINK routes. The TEAL 3-row strip (container · llm-rag-cli, app@390fe47a277a:/app$) types
    `exit` (extra) -> laptop/23 line 14 (session); the CLI box, its routes and plug dissolve while
    the frame turns GREY (title laptop, prompt student@laptop:~/AC215/llm-rag$). `docker compose
    down` (extra) -> laptop/25 lines 2–3 joined and 4 (GREY, cut at 65 with …; a GREY "harmless"
    tag in the strip's title bar), then 5–7 (Compose rows, times as GREY tags): with line 6 the
    Chroma box, its name, port, /data and :8000 routes dissolve; with line 7 the rail. The GREY
    laptop zone stays; it re-lays itself as a band along the top while the strip grows to 7 rows.
 1  `docker images` (extra) -> laptop/26 lines 2–5 as the column view (IMAGE, DISK USAGE; GREY header
    "docker images · IMAGE and DISK USAGE" just above the terminal). `2.11GB` boxed YELLOW as said,
    GREY tag "already inside the 2.11 GB" on the python:3.12-slim-bookworm row, `826MB` boxed
    YELLOW. GREY chip "need the space? docker image rm llm-rag-cli chromadb/chroma:latest" between
    the band and the terminal.
 2  The terminal clears. `git status; git status --short --ignored` (extra; folded after
    "git status;") -> laptop/27 lines 8, 11–14. ` M docker-shell.sh` boxed GREY + GREY tag "your
    edit"; `!! docker-volumes/` and `!! outputs/` GREEN + GREEN tag "ignored · stays on your disk";
    in the band outputs/ appears and both folders get a GREEN tick. The chip becomes "Linux: sudo rm
    -rf docker-volumes".
 3  The terminal leaves. A BLUE cloud "Google Cloud" with the GREY note "no VM · no bucket · no
    endpoint", then the GOLD tag "nothing runs in Google Cloud · you paid only for what you sent".
    The cloud goes and the GOLD tag moves up; the GOLD key in the band's secrets/ (beside llm-rag/)
    pulses. A RED "what if · just watch" frame
    (tag illustration): a copy of the key flies into an llm-rag/ folder card (Dockerfile, cli.py, the
    key file); RED tag "not in .gitignore"; a TEAL arrow labelled `COPY --chown=app:app . ./`
    (Dockerfile · line 48) carries the key into the COPY layer ("your files") of an "llm-rag-cli
    image" (three layers), RED cross. The frame clears; the GOLD tag becomes the GOLD row of the static GREY card
    "tear down" (checkboxes): `exit` (in the container) · `docker compose down` (laptop, in
    ~/AC215/llm-rag) · `docker image rm llm-rag-cli chromadb/chroma:latest` (optional) · keep
    docker-volumes/ and outputs/: your index · course over: IAM › Service accounts › KEYS › delete ·
    GOLD "nothing to delete in Google Cloud". The course-over row ticks as it is named; ▶ your turn
    on "Pause", the other rows tick; on "port 8000" the band's door and the compose-down row flash.
    Hold 2 s.
 4  The stale index. TRACKER Run 3 (no extra). PANEL expected/out-txt-agent-run.txt line 74 cut after
    "economic life" (header `out.txt · line 73 (excerpt)`, tag "recorded · the staff's agent run,
    September 22, 2026", flashing on "recorded run"), "transhumance" YELLOW; under it the excerpt
    chip `…known as transhumance, shaped not just the economic life…` (`96d5fd7 · Tolminc Cheese.txt
    · line 102 (excerpt)`), its "transhumance" YELLOW; today's file `Tolminc Cheese.txt` ("today")
    with the GREY chip "line 4: A fictional tale…" and the RED tag "not in today's book". A TEAL
    cylinder holding RED-edged cards; the old chip's frame shrinks into one more card that drops in
    (RED tag "stale"). On "rebuild the index" a GREEN arrow "books changed → chunk, embed, load
    again" runs into the cylinder, the cards turn GREEN and "stale" goes.
 5  TRACKER Agents 1. Static GREY card "next lecture · inside the container:" with `python cli.py
    --agent --chunk_type char-split` (tag preview · L06; not typed, no output). PANEL
    expected/out-txt-agent-run.txt line 65 (header `out.txt · line 64`, tag recorded) `Function:
    get_book_by_author`, the tool name YELLOW; GREY note "must call a tool: which one is its choice"
    with the excerpt chip `mode="any"` (cli.py · line 449 (excerpt)). LECTURE B74–B76: card and panel
    dim; a GREY dashed "Retrieve?" diamond (tag concept), caption "a related idea, further: whether
    to retrieve"; its No branch to "answer", its Yes branch to "retrieve", then "check what it found".
 6  LECTURE A63. S01's blurred map returns (dimmed, tag "illustration · our redrawing") with its four
    questions dim; each lights up YELLOW as answered, with a tiny glyph-only thumbnail (above the top
    two, below the bottom two) and a GREEN tick beside it: V4's arrows (S08's angles), V5's
    cylinder, V6's beam, V7's prompt card.
 7  No lecture tag, no tracker. "Test yourself" (YELLOW underline). Q1 with V1 under it, full size
    (both lanes, the five flags; each flag gets a GREEN tick; "flags" and "share" turn YELLOW, the
    embedding box and the cylinder light YELLOW and both lanes pulse on "what must both lanes
    share"). Q2 writes in below as Q1 turns small and GREY (V1 leaves); its code and
    "published port 8000" turn YELLOW as said.
 8  Q3, Q4, Q5 the same way, their key words YELLOW as said.
 9  Q5 turns small; the five questions sit at the top; the footer cards "Answers: exercises.md" and
    "Study guide + every command: github.com/JunyiZhou-Conny/MLOps_Learning · guides/L05-rag.md"
    (MLOps_Learning underlined YELLOW) under them; a GREY dashed "next: agents · L06" top right.
    Everything fades: empty frame (end of part 2).

Deviations from SHOW (see the scene report): laptop/25's WARN lines are cut at 65 with … (the script's
rule without `wrap`; S10 word-folded them), and the "harmless" tag sits in the strip's title bar (a
cut row has no room for a tag). The column view's header sits above the terminal like a panel
header (no row has room for it). V2's laptop zone stays as a band along the top for beats 1–3 (the
terminal grows to 7 rows for docker images and git status), which is also where the key "beside the
repo" is shown. Beat 3 opens on a Google Cloud picture (BRIEF.md: no VM, no bucket, no endpoint) and
follows the SAY's order (the GOLD tag first). The git command folds after "git status;" (one valid
line when joined). The COPY arrow carries the Dockerfile's real line 48, `COPY --chown=app:app .
./`, not the shorthand `COPY . ./`. The tear-down card's GOLD row has a coin instead of a checkbox.
The "check what it found" box after the Yes branch illustrates the SAY's last clause (critique
tokens, B78, under the B74–B76 tag). "Test yourself" is a title, not a card; V1 is shown full size
(scaled down, its flags collide). The "next" box sits top right (the footer row has no room).
"""

from types import SimpleNamespace

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Group,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Transform,
    VGroup,
    there_and_back,
)

from common import (
    CLOUD,
    COST,
    CTR,
    DATA,
    ERR,
    INK,
    KEY_FILE,
    LAPTOP,
    LOOKUP,
    MONO,
    NARRATION,
    P_CTR2,
    P_REPO,
    STORY_PATH,
    SYSTEM,
    TURN,
    ComposeView,
    RagMap,
    VectorSketch,
    _keep,
    _type_rows,
    bare_prompt,
    beside,
    capture,
    caption_extra,
    chunk_card,
    cloud,
    coin_glyph,
    col_box,
    column_view,
    concept_tag,
    cost_tag,
    cylinder,
    door,
    excerpt,
    excerpt_chip,
    extra_tag,
    file_row,
    grey_tag,
    harmless_tag,
    illustration_tag,
    key_glyph,
    leave_container,
    log_panel,
    lref,
    note,
    pin,
    preview_tag,
    print_build,
    prompt_card,
    recorded_tag,
    resize,
    sans,
    session,
    source_text,
    split_prompt,
    switch_section,
    term,
    tracker,
    type_cmd,
    under,
    what_if_frame,
)
from explainer import style as S
from explainer.devops import box, check_mark, chip, cross_mark, label, mono, step_badge, substring, tag
from explainer.scene import VoiceScene
from s01_hook import blur_map  # the lecture's map as S01 drew it (the recap returns to it)

SAY = NARRATION["S16"]

# ------------------------------------------------------------------ the real sources
AGAIN = capture("23", "laptop")                     # 23-x-docker-shell-again.txt: S10's restart
assert split_prompt(AGAIN.line(13)) == (P_CTR2, "exit") and AGAIN.line(14) == "exit", AGAIN.lines[-2:]

DOWN_ = capture("25", "laptop")                     # 25-x-compose-down-final.txt (extra)
assert DOWN_.cmd == "docker compose down" and DOWN_.exit == 0
# lines 2–3: one WARN line the 80-column terminal wrapped at a space (the space itself was lost)
assert DOWN_.line(2).endswith("Defaulting") and DOWN_.line(3) == "to a blank string.", DOWN_.lines[:2]
WARN_CREDS = DOWN_.line(2) + " " + DOWN_.line(3)
WARN_PROJ = DOWN_.line(4)
assert '"GCP_PROJECT" variable is not set' in WARN_PROJ, WARN_PROJ
assert DOWN_.line(5) == "[+] down 2/2" and "llm-rag-chromadb Removed" in DOWN_.line(6)
assert "llm-rag-network    Removed" in DOWN_.line(7)

IMG = capture("26", "laptop")                       # 26-x-images.txt (extra)
assert IMG.cmd == "docker images" and IMG.exit == 0
IMG_ROWS = column_view(IMG.at((2, 5)), ("IMAGE", "DISK USAGE"))
assert IMG_ROWS[2].split() == ["llm-rag-cli:latest", "2.11GB"] and IMG_ROWS[1].endswith("826MB"), IMG_ROWS
assert IMG_ROWS[3].split() == ["python:3.12-slim-bookworm", "198MB"], IMG_ROWS

GIT = capture("27", "laptop")                       # 27-x-git-status.txt (extra)
assert GIT.cmd == "git status; git status --short --ignored" and GIT.exit == 0
GIT_ROWS = GIT.at(8, (11, 14))
assert GIT_ROWS[1] == " M docker-shell.sh" and GIT_ROWS[3:] == ["!! docker-volumes/", "!! outputs/"], GIT_ROWS
_g = GIT.cmd.split("; ", 1)                         # folded after "git status;" (one valid line when joined)
GIT_TYPED = [f"{P_REPO} {_g[0]}; \\", f"    {_g[1]}"]
assert all(len(r) <= 65 for r in GIT_TYPED), GIT_TYPED
assert " ".join("\n".join(GIT_TYPED)[len(P_REPO) + 1:].replace("\\\n", "").split()) == GIT.cmd

AGENT = capture("out-txt-agent-run", "expected")    # the staff's L06 run (out.txt, recorded)
FUNC = AGENT.line(65)                               # = out.txt line 64
assert FUNC == "Function: get_book_by_author", FUNC
STALE = AGENT.cut(74, "economic life")              # = out.txt line 73, cut
assert STALE == "s, known as transhumance, shaped not just the economic life", STALE

OLD_BOOK = "tolminc-before-85bba32/input-datasets/books/Tolminc Cheese.txt"
OLD_SUB = "known as transhumance, shaped not just the economic life"
assert OLD_SUB in excerpt(OLD_BOOK, 102, 102)
LINE4 = excerpt(STORY_PATH, 4, 4)
assert LINE4.startswith("*A fictional tale"), LINE4
assert "transhumance" not in source_text(STORY_PATH)
AGENT_CMD = excerpt("README.md", 258, 258)
assert AGENT_CMD == "python cli.py --agent --chunk_type char-split", AGENT_CMD
MODE = 'mode="any"'
assert excerpt("cli.py", 449, 449).strip() == MODE
COPY_LINE = excerpt("Dockerfile", 48, 48)
assert COPY_LINE == "COPY --chown=app:app . ./", COPY_LINE
_ignore = source_text(".gitignore")
assert "secrets" not in _ignore and "json" not in _ignore      # the key inside llm-rag/ is not ignored

GUIDE_REPO = "github.com/JunyiZhou-Conny/MLOps_Learning"
GUIDE_PATH = "guides/L05-rag.md"
MAP_QUESTIONS = ["What is an embedding?", "a vector database?", "a query?", "the context?"]   # S01's

QUESTIONS = [   # (text, code spans) — script.md S16
    ("Which cli.py flags belong to each lane, and what must both lanes share?", ("cli.py",)),
    ("Why does the CLI reach the database at llm-rag-chromadb:8000, and who uses the published "
     "port 8000?", ("llm-rag-chromadb:8000",)),
    ("What does chunk_overlap buy and cost, and why did recursive-split make 14,228 chunks?",
     ("chunk_overlap", "recursive-split")),
    ("Why did the README's --query return no Tolminc text?", ("--query",)),
    ("What is the tutorial's prompt missing compared with the lecture's final prompt, and what is "
     "the one-line fix?", ()),
]

# ------------------------------------------------------------------ layout
SHOW_V2 = ("zone", "row_repo", "row_secrets", "row_volumes", "key", "door", "cli", "venv", "chroma",
           "name", "port_chip", "rail", "plug_cli", "plug_chroma", "route_app", "route_secrets",
           "route_data", "route_port")
BAND_Y = 2.125                  # the laptop band (beats 1–3): y 1.45..2.8, under the tracker
ROW_Y = 2.0                     # its folder rows
CHIP_Y = 0.98                   # chips between the band and the 7-row terminal (top 0.17)
Q_BIG, Q_SMALL = 26, 22         # the current question, the earlier ones
Q_X, Q_W = -5.75, 12.1          # left edge of the question text, wrap width
Q_TOP = 2.55
NBSP = "\u00a0"
NOBREAK = ("port 8000?", "14,228 chunks?", "no Tolminc text?", "one-line fix?")   # highlighted as one span


# ------------------------------------------------------------------ small helpers
def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.shift(RIGHT * (cx - m.get_center()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.shift(UP * (cy - m.get_center()[1]))
    return m


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded): they
    scroll and fade with it."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def in_title_bar(mob, t):
    """A tag at the right end of the terminal's title bar (a row too full for a tag beside it)."""
    return place(mob, right=t.box.get_right()[0] - 0.18, cy=t.box.get_top()[1] - t.bar_h / 2)


def clear_stage(scene, keep=(), extra=(), run_time: float = 0.6):
    """Fade out everything on screen except `keep` (and their families), then drop it."""
    fam = set()
    for k in keep:
        fam |= set(k.get_family())
    old = [m for m in scene.mobjects if m not in fam]
    if old:
        scene.play(FadeOut(Group(*old)), *extra, run_time=run_time)
        scene.remove(*old)
    elif extra:
        scene.play(*extra, run_time=run_time)


def mixed(parts, size: float = 22, color: str = INK):
    """One line of serif and mono pieces: parts = [(text, "mono"|"serif"), …] joined by spaces."""
    s = " ".join(txt for txt, _ in parts)
    t2f = {txt: MONO for txt, kind in parts if kind == "mono"}
    return _keep(S.text(s, size, color, t2f=t2f))


def grey_chip(parts, size: float = 20) -> VGroup:
    """A GREY chip holding a mixed caption (GREY serif + white mono). .box .text"""
    t = mixed(parts, size, INK)
    for txt, kind in parts:
        if kind == "serif":
            text_span(t, txt).set_color(S.GREY)
    h = mono("|", size).height + 0.26
    b = box(t.width + 0.5, h, S.GREY, fill=S.BG, fill_opacity=0.95, radius=h / 2.6)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return _keep(g)


def text_span(t, sub: str) -> VGroup:
    """The glyphs of `sub` in a one-line Text (spaces have no glyphs; no ligatures in mono)."""
    src = t.original_text                      # Text.text has its spaces removed
    i = src.find(sub)
    assert i >= 0, (sub, src)
    a = len("".join(src[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t[a:a + n])


def checkbox(s: float = 0.32) -> RoundedRectangle:
    return RoundedRectangle(width=s, height=s, corner_radius=0.06, stroke_color=S.GREY,
                            stroke_width=2.5).set_fill(S.BG, 1)


# ------------------------------------------------------------------ beat 0–3: the laptop band
def band_targets() -> SimpleNamespace:
    """V2's laptop zone laid out as a band along the top (y 1.45..2.8), part for part, so each zone
    part Transforms into its band twin."""
    b = SimpleNamespace()
    zf = box(12.8, 1.35, LAPTOP, fill_opacity=0.05, radius=0.16).move_to([0, BAND_Y, 0])
    zt = place(sans("laptop · ~/AC215", 20, LAPTOP), left=-6.2, cy=2.6)
    b.zone = VGroup(zf, zt)
    b.repo = place(file_row("llm-rag/"), left=-6.2, cy=ROW_Y)
    b.secrets = place(file_row("secrets/"), left=-4.05, cy=ROW_Y)
    b.key = place(key_glyph(0.28), left=b.secrets.get_right()[0] + 0.25, cy=ROW_Y)
    r3a = place(file_row("docker-volumes/"), left=-1.2, cy=2.12)
    r3b = place(file_row("chromadb/"), left=-0.78, cy=1.72)
    b.volumes = VGroup(r3a, r3b)
    b.outputs = place(file_row("outputs/"), left=2.45, cy=ROW_Y)
    dr = door(0.34, 0.56, LAPTOP)
    dl = mono(":8000", 20, LAPTOP)
    place(dr, right=6.15, cy=ROW_Y - 0.05)
    place(dl, right=dr.get_left()[0] - 0.12, cy=ROW_Y - 0.05)
    b.door = VGroup(dr, dl)
    return b


def need_chip() -> VGroup:
    return grey_chip([("need the space?", "serif"), ("docker image rm llm-rag-cli chromadb/chroma:latest", "mono")])


def linux_chip() -> VGroup:
    return grey_chip([("Linux:", "serif"), ("sudo rm -rf docker-volumes", "mono")])


def what_if_inset() -> SimpleNamespace:
    """Beat 3's RED dashed "what if" frame: the key inside llm-rag/ (not ignored), COPY into a layer."""
    w = SimpleNamespace()
    w.frame = what_if_frame(width=12.9, top=0.4, bottom=-3.5, note_="illustration")
    card = box(4.5, 3.0, LAPTOP, fill_opacity=0.05, radius=0.14).move_to([-3.95, -1.6, 0])
    head = place(file_row("llm-rag/"), left=card.get_left()[0] + 0.25, cy=-0.45)
    files = place(mono("Dockerfile  cli.py  …", 20, S.GREY), left=card.get_left()[0] + 0.6, cy=-0.95)
    k = key_glyph(0.3)
    place(k, left=card.get_left()[0] + 0.6, cy=-1.5)
    kn = place(mono(KEY_FILE, 20, COST), left=card.get_left()[0] + 0.25, cy=-1.95)
    nig = place(_keep(tag("not in .gitignore", ERR)), left=card.get_left()[0] + 0.25, cy=-2.6)
    w.card, w.head, w.files, w.key, w.key_name, w.not_ignored = card, head, files, k, kn, nig
    # the image: three layers, the top one is COPY's
    x_img = 4.8
    title = place(sans("llm-rag-cli image", 20, CTR), cx=x_img, cy=-0.45)
    specs = (("your files", CTR), ("/.venv (uv sync)", DATA), ("python base", SYSTEM))
    layers = VGroup()
    for k_, (s, col) in enumerate(specs):
        fr = box(2.95, 0.5, col, fill_opacity=0.12, radius=0.08, stroke=2.5).move_to([x_img, -1.05 - k_ * 0.62, 0])
        lab = place(sans(s, 20, col), left=fr.get_left()[0] + 0.18, cy=fr.get_center()[1])
        layers.add(VGroup(fr, lab))
    w.image = VGroup(title, layers)
    w.top_layer = layers[0]
    y_arr = layers[0].get_center()[1]            # into the COPY layer
    w.arrow = Arrow([card.get_right()[0] + 0.12, y_arr, 0], [layers.get_left()[0] - 0.12, y_arr, 0], buff=0,
                    color=CTR, stroke_width=5, max_tip_length_to_length_ratio=0.08, tip_length=0.22)
    w.copy_label = place(mono(COPY_LINE, 20, INK), cx=w.arrow.get_center()[0], bottom=y_arr + 0.16)
    w.copy_where = VGroup(mono("Dockerfile", 20, S.GREY), label("· line 48", 20, S.GREY)).arrange(RIGHT, buff=0.12)
    place(w.copy_where, cx=w.arrow.get_center()[0], top=y_arr - 0.18)
    w.landing = np.array([w.top_layer.get_right()[0] - 0.38, w.top_layer.get_center()[1], 0])
    return w


def teardown_card() -> SimpleNamespace:
    """The static GREY "tear down" card (beat 3): a checkbox per row, a GOLD row, ▶ your turn on its
    top-right corner. .frame .rows .boxes .ticks .gold .header .tag"""
    c = SimpleNamespace()
    rows = [
        VGroup(mono("exit", 22, INK), note("in the container", size=22)),
        VGroup(mono("docker compose down", 22, INK), note("on the laptop, in ~/AC215/llm-rag", size=22)),
        VGroup(mono("docker image rm llm-rag-cli chromadb/chroma:latest", 22, INK), note("optional", size=22)),
        VGroup(mixed([("keep", "serif"), ("docker-volumes/", "mono"), ("and", "serif"), ("outputs/:", "mono"),
                      ("your index", "serif")])),
        VGroup(label("course over: IAM › Service accounts › KEYS › delete", 22, INK)),
    ]
    items, boxes = VGroup(), []
    for r in rows:
        r.arrange(RIGHT, buff=0.3)
        cb = checkbox()
        it = VGroup(cb, r).arrange(RIGHT, buff=0.25)
        boxes.append(cb)
        items.add(it)
    gold = VGroup(coin_glyph(0.15), label("nothing to delete in Google Cloud", 22, COST)).arrange(RIGHT, buff=0.24)
    items.add(gold)
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    gold.shift(RIGHT * (boxes[0].get_center()[0] - gold[0].get_center()[0]))
    fr = box(items.width + 0.8, items.height + 0.62, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    items.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.4)
    head = note("tear down").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(fr, items, head)
    place(g, cx=0, top=1.32)
    yt = _keep(tag("▶ your turn", TURN))
    yt.move_to(fr.get_corner(UP + RIGHT)).shift(LEFT * 1.1)
    c.frame, c.items, c.header, c.tag, c.gold, c.group = fr, items, head, yt, gold, g
    c.boxes = boxes
    c.ticks = [check_mark(0.3, DATA, 5).move_to(b) for b in boxes]
    c.rows = rows
    return c


# ------------------------------------------------------------------ beat 4: the stale index
def stale_cards(n: int = 4) -> VGroup:
    cards = VGroup(*[chunk_card(0.42, 0.24) for _ in range(n)])
    for c in cards:
        c.frame.set_stroke(ERR, 3)
    return cards.arrange_in_grid(rows=2, cols=2, buff=(0.12, 0.1))


# ------------------------------------------------------------------ beat 5: Self-RAG's Retrieve token
def dashed_box(s: str, w: float | None = None) -> VGroup:
    t = sans(s, 20, S.GREY)
    b = box(w or t.width + 0.5, t.height + 0.36, S.GREY, dashed=True, stroke=2.5, radius=0.1)
    return VGroup(b, t.move_to(b))


def retrieve_diamond() -> SimpleNamespace:
    """B74–B76 in the series style: a GREY dashed "Retrieve?" diamond, No -> "answer", Yes ->
    "retrieve" -> "check what it found" (all dashed: a concept with no code here)."""
    d = SimpleNamespace()
    cx, cy = -2.3, -1.8
    poly = Polygon([cx, cy + 0.5, 0], [cx + 1.35, cy, 0], [cx, cy - 0.5, 0], [cx - 1.35, cy, 0])
    dia = DashedVMobject(poly, num_dashes=36, dashed_ratio=0.55).set_stroke(S.GREY, 2.5)
    d.diamond = VGroup(dia, sans("Retrieve?", 22, INK).move_to([cx, cy, 0]))
    y_b = -3.05
    d.answer = dashed_box("answer").move_to([cx - 2.9, y_b, 0])
    d.retrieve = dashed_box("retrieve").move_to([cx + 2.5, y_b, 0])
    d.check = dashed_box("check what it found").move_to([d.retrieve.get_right()[0] + 2.15, y_b, 0])

    def branch(a, b, word, side):
        ln = Arrow(a, b, buff=0.06, color=S.GREY, stroke_width=3, tip_length=0.16,
                   max_tip_length_to_length_ratio=0.2)
        w = sans(word, 20, S.GREY).next_to(ln.get_center(), side, buff=0.12)
        return VGroup(ln, w)

    d.no = branch([cx - 1.35, cy, 0], d.answer.get_top(), "No", LEFT + UP * 0.3)
    d.yes = branch([cx + 1.35, cy, 0], d.retrieve.get_top(), "Yes", RIGHT + UP * 0.3)
    d.then = Arrow(d.retrieve.get_right(), d.check.get_left(), buff=0.08, color=S.GREY, stroke_width=3,
                   tip_length=0.16, max_tip_length_to_length_ratio=0.25)
    d.caption = place(note("a related idea, further: whether to retrieve", size=22), left=cx - 1.5, cy=-0.95)
    d.tag = place(concept_tag(), left=1.2, cy=cy + 0.05)
    return d


# ------------------------------------------------------------------ beat 6: thumbnails (glyph-only)
def thumb(content: VGroup, w: float = 1.6, h: float = 1.05) -> VGroup:
    fr = box(w, h, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    k = min((w - 0.3) / content.width, (h - 0.24) / content.height, 1.0)
    content.scale(k).move_to(fr)
    g = VGroup(fr, content)
    g.frame, g.content = fr, content
    return g


def icon_vectors() -> VGroup:
    """V4 as S08 drew it: the sphere drawing, four GREEN arrows close together, two far off."""
    vs = VectorSketch(r=0.62)
    angles = ((42, 0.86), (55, 0.80), (48, 0.90), (61, 0.82), (203, 0.84), (216, 0.78))   # S08's ANGLES0
    arrows = VGroup(*[vs.arrow(d, ln, DATA, stroke=4) for d, ln in angles])
    return VGroup(vs.glyph_only(), arrows)


def icon_db() -> VGroup:
    """V5: the TEAL cylinder with three GREEN records beside it."""
    c = cylinder(0.62, 0.7)
    recs = VGroup(*[RoundedRectangle(width=0.6, height=0.13, corner_radius=0.05, stroke_width=0)
                    .set_fill(DATA, 0.75) for _ in range(3)]).arrange(DOWN, buff=0.08)
    recs.next_to(c, RIGHT, buff=0.18)
    return VGroup(c, recs)


def icon_beam() -> VGroup:
    """V6: GREEN dots, the PINK query point, its beam to the nearest five."""
    rng = np.random.default_rng(16)
    pts = rng.uniform(-1, 1, (30, 2)) * np.array([0.95, 0.45])
    dots = VGroup(*[Dot([x, y, 0], radius=0.035, color=DATA) for x, y in pts])
    q = np.array([-0.35, 0.12, 0])
    near = sorted(dots, key=lambda d: float(np.linalg.norm(d.get_center() - q)))[:5]
    beam = VGroup(*[Line(q, d.get_center(), color=LOOKUP, stroke_width=2) for d in near])
    for d in near:
        d.set_color(TURN)
    return VGroup(dots, beam, Dot(q, radius=0.075, color=LOOKUP))


def icon_prompt() -> VGroup:
    """V7: one prompt card (the PINK question row, then GREEN chunk rows)."""
    return prompt_card(n=5, w=1.2)


# ------------------------------------------------------------------ beats 7–9: question text (L04's helpers)
def text_line(s: str, size: float, color: str, code=()) -> VGroup:
    """One line of house-font text whose code spans use the code font, with a FIXED vertical extent
    (a leading '|' dropped after layout). Ligatures off, so glyph i is non-space character i.
    .glyphs .strut"""
    spans: list[tuple[int, int]] = []
    for c in sorted(code, key=len, reverse=True):
        i = s.find(c)
        while i >= 0:
            if all(i + len(c) <= a or i >= b for a, b in spans):
                spans.append((i, i + len(c)))
            i = s.find(c, i + 1)
    t2f = {f"[{a + 1}:{b + 1}]": MONO for a, b in spans}
    t = S.text("|" + s, size, color, t2f=t2f, disable_ligatures=True)
    pipe = t.submobjects[0]
    strut = Rectangle(width=max(0.01, t.width), height=pipe.height, stroke_width=0, fill_opacity=0)
    strut.move_to(pipe.get_center()).align_to(t, LEFT)
    subs = t.submobjects[1:]
    assert len(subs) == len(s), (s, len(subs))       # ligatures off: one submobject per character
    gl = VGroup(*[m for ch, m in zip(s, subs) if not ch.isspace()])
    strut.stretch_to_fit_width(max(0.01, gl.width)).align_to(gl, LEFT)
    g = VGroup(strut, *gl.submobjects)
    g.glyphs, g.strut = VGroup(*gl.submobjects), strut
    return g


_WIDTHS: dict = {}


def _line_width(s: str, size: float, code: tuple) -> float:
    key = (s, size, code)
    if key not in _WIDTHS:
        _WIDTHS[key] = text_line(s, size, INK, code).glyphs.width
    return _WIDTHS[key]


def wrap_lines(s: str, size: float, width: float, code=()) -> list:
    """Greedy wrap at spaces; a code span is never split."""
    code = tuple(code)
    for c in code + NOBREAK:
        s = s.replace(c, c.replace(" ", NBSP))
    lines, cur = [], ""
    for w in s.split(" "):
        trial = f"{cur} {w}" if cur else w
        if cur and _line_width(trial.replace(NBSP, " "), size, code) > width:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    return [ln.replace(NBSP, " ") for ln in lines + [cur]]


def question(i: int, size: float, color: str, badge_color: str) -> VGroup:
    """Question i (1-based): wrapped rows, a numbered badge left of the first row; the text's
    top-left at (Q_X, 0). .badge .lines .strs .flat (badge + glyphs, for glyph-to-glyph transforms)"""
    s, code = QUESTIONS[i - 1]
    strs = wrap_lines(s, size, Q_W, code)
    assert " ".join(strs) == s, (strs, s)
    rows = [text_line(ln, size, color, code) for ln in strs]
    pitch = rows[0].strut.height * 1.22
    for k, r in enumerate(rows):
        r.shift(np.array([Q_X - r.strut.get_left()[0], -k * pitch - r.strut.get_top()[1], 0]))
    big = size >= Q_BIG
    rad = 0.24 if big else 0.2
    b = step_badge(i, badge_color, size=22 if big else 20, radius=rad)
    b.move_to([Q_X - 0.22 - rad, rows[0].strut.get_center()[1], 0])
    g = VGroup(b, *rows)
    g.badge, g.lines, g.strs = b, rows, strs
    g.flat = VGroup(b, *[gl for r in rows for gl in r.glyphs])
    return g


def q_at(q: VGroup, top: float) -> VGroup:
    return q.shift(UP * (top - q.lines[0].strut.get_top()[1]))


def q_bottom(q: VGroup) -> float:
    return q.lines[-1].strut.get_bottom()[1]


def q_span(q: VGroup, sub: str) -> VGroup:
    """The glyphs of `sub` in question q (a span never crosses a line break)."""
    key = "".join(sub.split())
    for r, s in zip(q.lines, q.strs):
        flat = "".join(s.split())
        i = flat.find(key)
        if i >= 0:
            return VGroup(*r.glyphs[i:i + len(key)])
    raise AssertionError((sub, q.strs))


def footer_cards() -> VGroup:
    """Beat 9: "Answers: exercises.md" and "Study guide + every command:" (the link and the guide's
    path), side by side. .answers .guide .repo"""
    a_body = VGroup(label("Answers:", 24, INK), mono("exercises.md", 22, INK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.14)
    g_url = mono(GUIDE_REPO, 20, INK)
    g_body = VGroup(label("Study guide + every command:", 24, INK), g_url,
                    mono(GUIDE_PATH, 20, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    h = max(a_body.height, g_body.height) + 0.5
    a_box = box(a_body.width + 0.7, h, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    g_box = box(g_body.width + 0.7, h, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    a_body.move_to(a_box).align_to(a_box, LEFT).shift(RIGHT * 0.35)
    g_body.move_to(g_box).align_to(g_box, LEFT).shift(RIGHT * 0.35)
    row = VGroup(VGroup(a_box, a_body), VGroup(g_box, g_body)).arrange(RIGHT, buff=0.3)
    row.answers, row.guide = row[0], row[1]
    row.repo = text_span(g_url, "MLOps_Learning")
    return row


# ------------------------------------------------------------------ the scene
class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, f"S16 has {len(SAY)} SAY lines; this scene times 10"

        # ========================================================== 0 · exit, docker compose down
        tr = tracker("Run", 3)
        cv = ComposeView(show=SHOW_V2).fit_top()
        t = term(P_CTR2, rows=3, container=True)
        harm = harmless_tag()

        self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(cv), FadeIn(t, shift=UP * 0.2), run_time=0.8)
        bare_prompt(self, t)
        self.play(caption_extra(tr, True), run_time=0.3)

        with self.voiceover(SAY[0]) as vo:
            vo.wait_until("Type exit")
            out = session(self, t, AGAIN, 13, 14, type_time=0.35, out_time=0.2)
            pin(self, out[13], beside(extra_tag(), t, out[13]), run_time=0.2)
            self.play(*cv.remove_cli(), *leave_container(t, P_REPO), run_time=0.7)
            bare_prompt(self, t)
            vo.wait_until("then docker compose down")
            dn = type_cmd(self, t, DOWN_.cmd, 0.6)
            pin(self, dn, beside(extra_tag(), t, dn), run_time=0.25)
            vo.wait_until("the same harmless warnings")
            t.print(self, [(WARN_CREDS, S.GREY), (WARN_PROJ, S.GREY)], run_time=0.5)
            in_title_bar(harm, t)
            self.play(FadeIn(harm, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("then Chroma and the network")
            print_build(self, t, [DOWN_.line(5)], run_time=0.3)
            print_build(self, t, [DOWN_.line(6)], run_time=0.3)
            self.play(*cv.parts_out("chroma", "name", "port_chip", "plug_chroma", "route_data", "route_port"),
                      run_time=0.7)
            print_build(self, t, [DOWN_.line(7)], run_time=0.3)
            self.play(*cv.parts_out("rail"), FadeOut(harm), run_time=0.6)
            # the laptop zone stays: it re-lays itself as a band along the top; the terminal grows
            b = band_targets()
            P = cv.parts
            resize(self, t, 7, run_time=0.9,
                   extra=[Transform(P["zone"], b.zone), Transform(P["row_repo"], b.repo),
                          Transform(P["row_secrets"], b.secrets), Transform(P["key"], b.key),
                          Transform(P["row_volumes"], b.volumes), Transform(P["door"], b.door)])

        # ========================================================== 1 · docker images: the images stay
        hdr = VGroup(mono("docker images", 20, S.GREY), label("· IMAGE and DISK USAGE", 20, S.GREY))
        hdr.arrange(RIGHT, buff=0.12)
        base_tag = grey_tag("already inside the 2.11 GB")
        need = need_chip().move_to([0, CHIP_Y, 0])

        with self.voiceover(SAY[1]) as vo:
            im = type_cmd(self, t, IMG.cmd, 0.45)
            pin(self, im, beside(extra_tag(), t, im), run_time=0.25)
            head, r_chroma, r_cli, r_base = t.print(self, IMG_ROWS, run_time=0.4)
            place(hdr, right=t.box.get_right()[0] - 0.15, bottom=t.box.get_top()[1] + 0.1)   # the view's header
            self.play(FadeIn(hdr, shift=DOWN * 0.1), run_time=0.3)
            vo.wait_until("2.11 gigabytes")
            i = r_cli.text.index("2.11GB")
            b211 = col_box(r_cli, i, i + 6, TURN)
            self.play(Create(b211), substring(r_cli, "2.11GB").animate.set_color(TURN), run_time=0.6)
            stick(self, r_cli, b211)
            vo.wait_until("its Python base included")
            beside(base_tag, t, r_base, buff=0.5)
            self.play(FadeIn(base_tag, shift=LEFT * 0.1), Indicate(substring(r_base, "python:3.12-slim-bookworm"),
                                                                   color=INK, scale_factor=1.04), run_time=0.7)
            stick(self, r_base, base_tag)
            vo.wait_until("and 826 megabytes")
            i = r_chroma.text.index("826MB")
            b826 = col_box(r_chroma, i, i + 5, TURN)
            self.play(Create(b826), substring(r_chroma, "826MB").animate.set_color(TURN), run_time=0.6)
            stick(self, r_chroma, b826)
            self.wait(0.4)
            self.play(FadeIn(need, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 2 · git status: ignored, on your disk
        your_edit = grey_tag("your edit")
        ignored = _keep(tag("ignored · stays on your disk", DATA))
        outs = b.outputs
        ticks = VGroup(check_mark(0.24, DATA, 4).next_to(P["row_volumes"][0], RIGHT, buff=0.18),
                       check_mark(0.24, DATA, 4).next_to(outs, RIGHT, buff=0.18))
        lin = linux_chip().move_to([0, CHIP_Y, 0])

        with self.voiceover(SAY[2]) as vo:
            t.clear(self, run_time=0.3)
            self.play(FadeOut(hdr), run_time=0.2)
            gs = _type_rows(self, t, GIT_TYPED, len(P_REPO) + 1, 0.9, len(GIT.cmd))
            pin(self, gs, beside(extra_tag(), t, gs), run_time=0.25)
            mod, m_row, pyc, vol, out_row = t.print(self, GIT_ROWS, run_time=0.5)
            vo.wait_until("shows only your edit")
            eb = col_box(m_row, 1, len(m_row.text), S.GREY)
            beside(your_edit, t, m_row, buff=0.45)
            self.play(Create(eb), FadeIn(your_edit, shift=LEFT * 0.1), run_time=0.6)
            stick(self, m_row, eb, your_edit)
            vo.wait_until("The outputs and docker volumes folders")
            beside(ignored, t, vol, buff=0.6)
            ignored.set_y((vol.strut.get_center()[1] + out_row.strut.get_center()[1]) / 2)
            self.play(vol.animate.set_color(DATA), out_row.animate.set_color(DATA), FadeIn(ignored, shift=LEFT * 0.1),
                      FadeIn(outs, shift=DOWN * 0.15), run_time=0.7)
            self.play(Create(ticks[0]), Create(ticks[1]),
                      Indicate(P["row_volumes"][0], color=DATA, scale_factor=1.06),
                      Indicate(outs, color=DATA, scale_factor=1.06), run_time=0.8)
            vo.wait_until("and stay on your disk")
            self.play(FadeOut(need, shift=DOWN * 0.1), FadeIn(lin, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 3 · nothing in the cloud; the key; ▶ tear down
        gold = _keep(cost_tag("nothing runs in Google Cloud · you paid only for what you sent"))
        gold.move_to([0, -2.15, 0])
        gc = cloud(2.6, CLOUD).move_to([0, -0.35, 0])
        gc_t = sans("Google Cloud", 24, INK).move_to(gc)
        none_ = note("no VM · no bucket · no endpoint", size=22).next_to(gc, DOWN, buff=0.22)
        w = what_if_inset()
        card = teardown_card()
        key = P["key"]

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(t), FadeOut(ignored), FadeOut(lin), FadeOut(ticks), run_time=0.6)
            self.play(FadeIn(gc), FadeIn(gc_t), run_time=0.6)
            self.play(FadeIn(none_, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("you paid only for what you sent")
            self.play(FadeIn(gold, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Keep the key beside the repo")
            self.play(FadeOut(VGroup(gc, gc_t, none_)), gold.animate.move_to([0, CHIP_Y, 0]), run_time=0.6)
            self.play(Indicate(key, color=COST, scale_factor=1.6),
                      Indicate(P["row_secrets"], color=COST, scale_factor=1.08),
                      Indicate(P["row_repo"], color=INK, scale_factor=1.08), run_time=0.9)
            vo.wait_until("inside it")
            self.play(FadeIn(w.frame), FadeIn(w.card), FadeIn(w.head), FadeIn(w.files), run_time=0.5)
            kc = key.copy()
            self.add(kc)
            self.play(ReplacementTransform(kc, w.key), FadeIn(w.key_name, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("git wouldn't ignore the key")
            self.play(FadeIn(w.not_ignored, shift=UP * 0.1), Indicate(w.key_name, color=ERR, scale_factor=1.05),
                      run_time=0.6)
            vo.wait_until("and the image would copy it")
            self.play(FadeIn(w.image, shift=LEFT * 0.15), FadeIn(w.copy_label), FadeIn(w.copy_where), run_time=0.5)
            rider = w.key.copy()
            self.add(rider)
            self.play(GrowArrow(w.arrow), rider.animate.move_to(w.landing), run_time=1.0)
            x_ = cross_mark(0.5, ERR, 6).move_to(w.landing)
            self.play(Create(x_), Indicate(w.top_layer, color=ERR, scale_factor=1.04), run_time=0.5)
            vo.wait_until("Delete it when the course ends")
            inset = VGroup(w.frame, w.card, w.head, w.files, w.key, w.key_name, w.not_ignored, w.image,
                           w.copy_label, w.copy_where, w.arrow, rider, x_)
            self.play(FadeOut(inset), run_time=0.45)
            self.play(FadeIn(card.frame), FadeIn(card.header), FadeIn(VGroup(*card.items[:-1])),
                      FadeTransform(gold, card.gold), run_time=0.7)
            self.play(card.rows[4].animate.set_color(TURN), Create(card.ticks[4]),
                      Indicate(key, color=COST, scale_factor=1.5), run_time=0.6)
            vo.wait_until("Pause and tear down now")
            self.play(FadeIn(card.tag, scale=1.2), card.rows[4].animate.set_color(INK), run_time=0.4)
            self.play(LaggedStart(*[Create(card.ticks[k]) for k in range(4)], lag_ratio=0.35), run_time=1.2)
            vo.wait_until("so port 8000 is free")
            door_ = P["door"]
            self.play(Indicate(door_, color=LOOKUP, scale_factor=1.15),
                      Indicate(card.rows[1][0], color=TURN, scale_factor=1.05), run_time=0.9)
        self.wait(2)                                   # ▶ beat: hold the frame

        # ========================================================== 4 · a stale index
        cw_ = mono("M" * 40, 20).width / 40
        panel = log_panel([STALE], "out.txt · line 73 (excerpt)", width=12.2)
        place(panel, left=-6.1, top=2.72)
        rec = recorded_tag("recorded · the staff's agent run, September 22, 2026")
        place(rec, right=panel.frame.get_right()[0], cy=panel.header.get_center()[1])
        p_word = substring(panel.rows[0], "transhumance")
        old = excerpt_chip(f"…{OLD_SUB}…", "96d5fd7 · Tolminc Cheese.txt · line 102 (excerpt)")
        place(old, left=-6.1, top=panel.frame.get_bottom()[1] - 0.3)
        o_word = text_span(old.text, "transhumance")
        today = file_row("Tolminc Cheese.txt")
        today_lab = note("today", size=22)
        line4 = _keep(chip("line 4: A fictional tale…", S.GREY, size=20, fill_opacity=0.1))
        not_in = _keep(tag("not in today's book", ERR))
        today_row = VGroup(today, today_lab, line4, not_in).arrange(RIGHT, buff=0.3)
        place(today_row, left=-6.0, cy=-0.75)
        cyl = cylinder(1.25, 1.15).move_to([-4.7, -2.6, 0])
        cards = stale_cards().move_to(cyl.body.get_center() + DOWN * 0.05)
        stale = _keep(tag("stale", ERR)).next_to(cyl, RIGHT, buff=0.3).shift(UP * 0.4)
        newcard = chunk_card(0.42, 0.24)
        newcard.frame.set_stroke(ERR, 3)
        rb_text = VGroup(sans("books changed", 22, INK), label("→", 22, INK),
                         sans("chunk, embed, load again", 22, DATA)).arrange(RIGHT, buff=0.18)
        place(rb_text, left=0.2, cy=-2.75)
        rb_arrow = Arrow([rb_text.get_left()[0] - 0.12, -2.75, 0], [cyl.get_right()[0] + 0.12, -2.75, 0], buff=0,
                         color=DATA, stroke_width=5, tip_length=0.2, max_tip_length_to_length_ratio=0.12)

        with self.voiceover(SAY[4]) as vo:
            clear_stage(self, keep=[tr], extra=[caption_extra(tr, False)], run_time=0.6)
            self.play(FadeIn(panel, shift=DOWN * 0.1), FadeIn(rec), run_time=0.7)
            vo.wait_until("recorded run")
            self.play(Indicate(rec.text, color=INK, scale_factor=1.06),
                      rec.box.animate(rate_func=there_and_back).set_stroke(INK, 4), run_time=0.7)
            vo.wait_until("transhumance")
            self.play(p_word.animate.set_color(TURN), Create(under(p_word, TURN, 3)), run_time=0.6)
            vo.wait_until("from an older Tolminc book")
            self.play(FadeIn(old, shift=DOWN * 0.1), run_time=0.6)
            self.play(o_word.animate.set_color(TURN), Create(under(o_word, TURN, 3)), run_time=0.5)
            vo.wait_until("replaced that same day")
            self.play(FadeIn(VGroup(today, today_lab, line4), shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(not_in, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("The database answers from what was loaded")
            self.play(FadeIn(cyl), FadeIn(cards), run_time=0.6)
            ghost = old.chip[0].copy()                 # the chip's frame shrinks into a card
            self.add(ghost)
            self.play(Transform(ghost, newcard.move_to(cyl.top.get_center() + UP * 0.05)), run_time=0.8)
            self.play(ghost.animate.move_to(cards.get_center()).set_opacity(0), FadeIn(stale, shift=LEFT * 0.1),
                      Indicate(cards, color=ERR, scale_factor=1.08), run_time=0.7)
            self.remove(ghost)
            vo.wait_until("when the books change")
            self.play(FadeIn(rb_text, shift=LEFT * 0.1), run_time=0.5)
            self.play(GrowArrow(rb_arrow), run_time=0.6)
            self.play(*[c.frame.animate.set_stroke(DATA, 2) for c in cards], FadeOut(stale),
                      cyl.animate(rate_func=there_and_back).set_stroke(DATA), run_time=0.8)

        # ========================================================== 5 · next lecture: an agent; Self-RAG
        agent_card = VGroup(mono(AGENT_CMD, 22, INK))
        a_fr = box(agent_card.width + 0.7, agent_card.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95)
        agent_card.move_to(a_fr)
        a_head = note("next lecture · inside the container:", size=22).next_to(a_fr, UP, buff=0.08)
        a_head.align_to(a_fr, LEFT).shift(RIGHT * 0.12)
        pv = preview_tag()
        card5 = VGroup(a_fr, agent_card, a_head)
        place(card5, left=-6.1, top=2.72)
        place(pv, left=a_fr.get_right()[0] + 0.3, cy=a_fr.get_center()[1])
        fpanel = log_panel([FUNC], "out.txt · line 64", width=len(FUNC) * cw_ + 0.8)
        place(fpanel, left=-6.1, top=a_fr.get_bottom()[1] - 0.45)
        frec = recorded_tag()
        place(frec, left=fpanel.header.get_right()[0] + 0.35, cy=fpanel.header.get_center()[1])
        tool = substring(fpanel.rows[0], "get_book_by_author")
        n1 = note("must call a tool: which one is its choice", size=22)
        mode_g = excerpt_chip(MODE, "cli.py · line 449 (excerpt)", line=excerpt("cli.py", 449, 449))
        note5 = VGroup(n1, mode_g).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        place(note5, left=fpanel.frame.get_right()[0] + 0.45, cy=fpanel.frame.get_center()[1] + 0.1)
        d = retrieve_diamond()

        with self.voiceover(SAY[5]) as vo:
            clear_stage(self, keep=[tr], run_time=0.5)
            tr = switch_section(self, tr, "Agents", 1, run_time=0.6)
            self.play(FadeIn(card5, shift=DOWN * 0.1), run_time=0.6)
            self.play(FadeIn(pv, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("In the staff's run")
            self.play(FadeIn(fpanel, shift=DOWN * 0.1), FadeIn(frec), run_time=0.6)
            vo.wait_until("the model chose which retrieval tool")
            self.play(tool.animate.set_color(TURN), run_time=0.5)
            self.play(FadeIn(note5, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("The lecture's Self-RAG goes further")
            lr = lref("B74–B76")
            self.play(FadeIn(lr), *[m.animate.fade(0.55) for m in (card5, pv, fpanel, frec, note5)],
                      FadeIn(d.caption, shift=UP * 0.1), run_time=0.6)
            self.play(Create(d.diamond[0]), FadeIn(d.diamond[1]), FadeIn(d.tag), run_time=0.8)
            vo.wait_until("the model decides whether to retrieve")
            self.play(Indicate(d.diamond, color=INK, scale_factor=1.08), run_time=0.6)
            self.play(GrowArrow(d.no[0]), FadeIn(d.no[1]), FadeIn(d.answer), run_time=0.5)
            self.play(GrowArrow(d.yes[0]), FadeIn(d.yes[1]), FadeIn(d.retrieve), run_time=0.5)
            vo.wait_until("then checks what it found")
            self.play(GrowArrow(d.then), FadeIn(d.check, shift=LEFT * 0.1), run_time=0.7)

        # ========================================================== 6 · the four questions, answered
        mp = blur_map()
        mp.fade(0.5)
        ill = illustration_tag("our redrawing")
        place(ill, right=6.5, cy=-3.32)
        nd = mp.nodes
        targets = [nd[1].get_top() + UP * 0.08, nd[3].get_top() + UP * 0.08,
                   nd[0].get_bottom() + DOWN * 0.08, nd[4].get_bottom() + DOWN * 0.08]
        spots = [(-4.3, 1.98), (0.0, 1.98), (-4.9, -1.98), (0.45, -1.98)]
        qs, arrows = VGroup(), VGroup()
        for s, (x, y), t_pt in zip(MAP_QUESTIONS, spots, targets):
            c = chip(s, TURN, size=26, text_color=TURN, fill_opacity=0.0)
            c.box.set_fill(S.BG, 0.95)
            c.move_to([x, y, 0])
            qs.add(c)
            start = (c.get_bottom() if y > 0 else c.get_top()) + (UP if y < 0 else DOWN) * 0.05
            arrows.add(Arrow(start, t_pt, buff=0.04, color=TURN, stroke_width=5, max_tip_length_to_length_ratio=0.3))
        thumbs = []
        for k, fn in enumerate((icon_vectors, icon_db, icon_beam, icon_prompt)):
            th = thumb(fn())
            c = qs[k]
            if spots[k][1] > 0:
                place(th, cx=c.get_center()[0], bottom=c.get_top()[1] + 0.14)
            else:
                place(th, cx=c.get_center()[0], top=c.get_bottom()[1] - 0.14)
            thumbs.append(th)
        qticks = [check_mark(0.3, DATA, 5).next_to(thumbs[k], RIGHT, buff=0.15) for k in range(4)]
        for q_, a_ in zip(qs, arrows):
            q_.set_opacity(0.3)
            q_.box.set_fill(S.BG, 0.95)
            a_.set_opacity(0.3)
        anchors = ["An embedding is a direction", "A vector database stores records", "A query finds",
                   "The context is the chunks"]

        with self.voiceover(SAY[6]) as vo:
            clear_stage(self, run_time=0.6)
            lr = lref("A63")
            self.play(FadeIn(lr), FadeIn(mp, lag_ratio=0.01), FadeIn(ill), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(VGroup(q_, a_)) for q_, a_ in zip(qs, arrows)], lag_ratio=0.15),
                      run_time=0.8)
            for k in range(4):
                vo.wait_until(anchors[k])
                self.play(qs[k].animate.set_opacity(1), arrows[k].animate.set_opacity(1),
                          FadeIn(thumbs[k], shift=(DOWN if spots[k][1] > 0 else UP) * 0.15), run_time=0.6)
                qs[k].box.set_fill(S.BG, 0.95)
                self.play(Create(qticks[k]), qs[k].animate(rate_func=there_and_back).scale(1.1), run_time=0.6)

        # ========================================================== 7 · test yourself: Q1, Q2
        title = label("Test yourself", 34, INK)
        place(title, left=-6.2, top=3.5)
        t_ul = Line(title.get_corner(DOWN + LEFT) + DOWN * 0.08, title.get_corner(DOWN + RIGHT) + DOWN * 0.08,
                    color=TURN, stroke_width=3)
        q1 = q_at(question(1, Q_BIG, INK, TURN), Q_TOP)
        rm = RagMap(show=RagMap.TOP + RagMap.BOTTOM + RagMap.FLAGS)
        vis = VGroup(*[rm.parts[n] for n in RagMap.TOP + RagMap.BOTTOM + RagMap.FLAGS])
        rm.shift(np.array([-vis.get_center()[0], q_bottom(q1) - 0.5 - vis.get_top()[1], 0]))
        fticks = [rm.tick(n) for n in RagMap.FLAGS]

        with self.voiceover(SAY[7]) as vo:
            clear_stage(self, run_time=0.6)
            self.play(FadeIn(title, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Five questions")
            self.play(Create(t_ul), run_time=0.5)
            vo.wait_until("One:")
            self.play(FadeIn(q1, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(rm), run_time=0.7)
            vo.wait_until("which flags belong")
            self.play(q_span(q1, "flags").animate.set_color(TURN), run_time=0.3)
            self.play(LaggedStart(*[Create(tk) for tk in fticks], lag_ratio=0.3), run_time=1.3)
            vo.wait_until("what must both lanes share")
            # the cylinder's strokes one by one: RagMap.light("database") animates the helper group
            # cylinder.frame, which the scene would add on top of the flags
            db_strokes = list(rm.item("database").frame.submobjects)
            self.play(q_span(q1, "share").animate.set_color(TURN), rm.light("embedding"),
                      *[m.animate.set_stroke(TURN, 5) for m in db_strokes], run_time=0.6)
            self.play(rm.pulse_lane("top", DATA), rm.pulse_lane("bottom", LOOKUP), run_time=1.0)
            vo.wait_until("Two:")
            small1 = q_at(question(1, Q_SMALL, S.GREY, S.GREY), Q_TOP)
            top2 = q_bottom(small1) - 0.34
            q2 = q_at(question(2, Q_BIG, INK, TURN), top2)
            self.play(Transform(q1.flat, small1.flat), FadeOut(rm), *[FadeOut(tk) for tk in fticks], run_time=0.6)
            self.remove(q1, q1.flat)
            self.add(small1)
            self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("by name")
            self.play(q_span(q2, "llm-rag-chromadb:8000").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("who uses port 8000")
            self.play(q_span(q2, "published").animate.set_color(TURN),
                      q_span(q2, "port 8000?").animate.set_color(TURN), run_time=0.5)

        # ========================================================== 8 · Q3, Q4, Q5
        smalls = [small1]

        def step(q_cur, i_cur, top_cur):
            """Demote question i_cur (it turns small and GREY at top_cur); question i_cur + 1 writes in
            under it. Returns (small, new question, its top)."""
            small = q_at(question(i_cur, Q_SMALL, S.GREY, S.GREY), top_cur)
            top_new = q_bottom(small) - 0.34
            q_new = q_at(question(i_cur + 1, Q_BIG, INK, TURN), top_new)
            self.play(Transform(q_cur.flat, small.flat), run_time=0.5)
            self.remove(q_cur, q_cur.flat)
            self.add(small)
            smalls.append(small)
            self.play(FadeIn(q_new, shift=UP * 0.15), run_time=0.5)
            return q_new, top_new

        with self.voiceover(SAY[8]) as vo:
            q3, top3 = step(q2, 2, top2)
            self.play(q_span(q3, "chunk_overlap").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("And why did the recursive splitter")
            self.play(q_span(q3, "recursive-split").animate.set_color(TURN),
                      q_span(q3, "14,228 chunks?").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("Four:")
            q4, top4 = step(q3, 3, top3)
            vo.wait_until("query return")
            self.play(q_span(q4, "--query").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("no Tolminc text")
            self.play(q_span(q4, "no Tolminc text?").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("Five:")
            q5, top5 = step(q4, 4, top4)
            vo.wait_until("what is the prompt missing")
            self.play(q_span(q5, "missing").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("and what's the fix")
            self.play(q_span(q5, "one-line fix?").animate.set_color(TURN), run_time=0.4)

        # ========================================================== 9 · answers, the guide, next time
        small5 = q_at(question(5, Q_SMALL, S.GREY, S.GREY), top5)
        foot = footer_cards()
        nxt = VGroup(label("next:", 24, S.GREY), label("agents · L06", 24, INK)).arrange(RIGHT, buff=0.15)
        nxt_box = box(nxt.width + 0.6, nxt.height + 0.28, S.GREY, dashed=True)
        nxt.move_to(nxt_box)
        nxt_g = VGroup(nxt_box, nxt)

        with self.voiceover(SAY[9]) as vo:
            self.play(Transform(q5.flat, small5.flat), run_time=0.5)
            self.remove(q5, q5.flat)
            self.add(small5)
            smalls.append(small5)
            place(foot, left=-6.2, top=q_bottom(small5) - 0.45)
            place(nxt_g, right=6.3, top=3.5)
            vo.wait_until("in the exercises")
            self.play(FadeIn(foot.answers, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("every command is in the study guide")
            self.play(FadeIn(foot.guide, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("in the MLOps Learning repo")
            self.play(Create(under(foot.repo, TURN, 3)), foot.repo.animate.set_color(TURN), run_time=0.6)
            vo.wait_until("Next time")
            self.play(FadeIn(nxt_g, shift=LEFT * 0.2), run_time=0.6)

        self.wait(0.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.9)
        self.wait(0.2)
