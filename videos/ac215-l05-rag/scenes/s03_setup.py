"""S03 · Your key, your folders, your project (README "Prerequisites", "Service Account",
"Run Container" steps 1-2). Lecture: none (no lecture tag).

Beats (script.md "## S03", one voiceover block each):
 0  TRACKER Prereq 1 · extra. The house terminal (10 rows, `laptop`, prompt ~/AC215) types
    `docker --version; docker compose version` (extra) -> laptop/01 lines 2-3; the command row is
    64 of the 65 columns (beside() would clamp the tag over "version"), so its extra tag sits at
    the right end of the output row below (the pilot's under_row; QA_FOLLOWUPS S03). 29.8.2 and
    v5.6.0 underline GREY under one bracket + tag "at the time of recording"; the space in
    `docker compose` flashes YELLOW (a block in the gap between the glyphs, clear of both
    words). GREY note under the terminal, in two halves as named:
    "Mac: zsh, prompt ends in %" · "Windows: WSL or Git Bash".
 1  TRACKER Prereq 2. The terminal settles on the bottom edge; README chip (top band)
    README.md · line 48 "Cloned this repository". `git clone https://github.com/dlops-io/llm-rag.git`
    (folds) -> laptop/02 line 2. TRACKER Prereq 2 · extra: `mkdir secrets; ls` (extra) ->
    laptop/03 line 2. The terminal shrinks to the 3-row strip. Right: GREY folders llm-rag/ and
    secrets/ side by side under a GREY ~/AC215 bracket; llm-rag/ underlines YELLOW + tag "exactly
    this name"; README card README.md · lines 66–69 (|-llm-rag, |-secrets). Left: static GREY
    your-turn card "in your course folder (~/AC215)" with both commands (▶ your turn). Hold 2 s.
 2  TRACKER Account 1→6. Strip, cards and tags leave; the folders stay at right. A schematic
    console in a GREY browser frame (tag illustration, no logo), one screen per step as named:
    IAM & Admin › Service accounts → Create service account (name llm-service-account typed) →
    "Grant this service account access to project": BLUE role chips Storage Admin, Gemini
    Enterprise Agent Platform User (+ GREY note "Vertex AI User in older projects") → the
    account's KEYS tab → Add key › Create new key › JSON, a download chip with the GOLD key, and
    a GREY card under the browser "key creation blocked by an org policy? / use a personal
    project, …". The GOLD key drops into secrets/; its label becomes llm-service-account.json.
 3  The console leaves; the folders move to the top left; GOLD tag "this file spends your
    project's money" under the key. .gitignore · lines 1–5 slides in at right; a GREY dashed ghost
    row "secrets" under line 5 with tag "not here". Both folders pulse ("beside"). Then L04's three
    gates in miniature along the bottom, BLUE, each label and item as named: "who?" + GOLD key,
    "may?" + the two role chips, "switched on?" + an API switch (off).
 4  The top half clears and the gates rise to the middle (they go back down when the Vertex AI
    screen arrives above them). An erratum tag on the Storage Admin row (the README's slip: beside the
    other chip it read as "this role is the mistake"); Storage Admin dims to GREY with a note "no
    storage call in this code" after the tag; the Agent Platform chip flashes and gets a GREEN
    "✓ needed". The third gate sits far right so that row clears the switch. TRACKER Account 6 ·
    extra: a schematic "APIs & Services › Vertex AI API" screen (aiplatform.googleapis.com, a BLUE
    Enable button; tag illustration); Enable pulses, the switch flips on, the third gate opens with
    a white tick. A dimmed RED chip under the screen: "without it: SERVICE_DISABLED on the first
    embed, after 5 retries". Then everything leaves; all 6 tracker dots light; a static GREY
    "your turn · in the console" card (tag illustration) with the five console rows and a GREY
    look-for line "check: ls secrets → llm-service-account.json"; its rows light one by one as
    "account, roles, key, and API" are named. Hold 2 s.
 5  TRACKER Run 1. A 10-row terminal (9 rows of output + a row for the commit tag) at ~/AC215 types `cd llm-rag` (no output); the prompt becomes
    ~/AC215/llm-rag, the new path part flashing GREY. TRACKER Run 1 · extra: `ls -a; git log
    --oneline -1` (extra) -> laptop/05 lines 2-5 (captured 80 wide: the two long rows wrap at their
    last column gap, so no name splits), line 6 cut after "origin/HEAD)".
    docker-shell.sh, docker-compose.yml and cli.py box GREEN one by one as named; e17a39f gets a
    GREY box and the GREY tag "↑ the commit this video was recorded on" on the empty row under
    it (the commit row is full; on the row above, the tag would touch the cli.py box).
 6  TRACKER Run 2. The ls output leaves as, above the terminal, a GREY pencil edits a GREY file
    card docker-shell.sh ("in your editor"). Then `git diff docker-shell.sh` (extra) -> laptop/06 lines
    6-13: line 10 RED, line 11 GREEN; a YELLOW box on your-project-id and, two rows up (the only
    free row space near it), a YELLOW tag "your Project ID · not the name" starting at the blank
    column after line 10's closing quote, with a short arrow down through it (so nothing frames
    the old value); line 12's path underlined GREY + tag on line 13's row "↑ leave this: a path
    inside the container". GREY note "skip it → calls go to the course's project → permission
    error" low on the left. The card sits top right (the tracker owns the top left); the pencil
    rests to its left, where ▶ your turn replaces it; hold 2 s; fade to empty.
"""

import re

import numpy as np
from common import (
    CLOUD,
    COST,
    DATA,
    ERR,
    INK,
    KEY_FILE,
    LAPTOP,
    NARRATION,
    P_REPO,
    P_WS,
    TURN,
    BOTTOM,
    Prose,
    beside,
    caption_extra,
    capture,
    card_rows,
    cd_prompt,
    erratum_tag,
    extra_tag,
    grey_tag,
    illustration_tag,
    key_glyph,
    note,
    pencil,
    pin,
    readme_card,
    readme_chip,
    recording_tag,
    resize,
    source_text,
    src_panel,
    switch_section,
    term,
    toggle,
    tracker,
    turn_card,
    type_cmd,
    under,
    your_turn,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    RoundedRectangle,
    ShowIncreasingSubsets,
    Transform,
    VGroup,
    VMobject,
    linear,
    smooth,
    there_and_back,
)

from explainer import style as S
from explainer.devops import (
    CAPTION,
    OUTPUT,
    TAG,
    box,
    browser_window,
    cell_width,
    check_mark,
    chip,
    file_glyph,
    folder_glyph,
    TERM_BG,
    glyph_range,
    label,
    mono,
    substring,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ commands (README / capture spelling)
DOCKER_CHECK = "docker --version; docker compose version"
CLONE = "git clone https://github.com/dlops-io/llm-rag.git"
MKDIR = "mkdir secrets; ls"
CD = "cd llm-rag"
LS = "ls -a; git log --oneline -1"
DIFF = "git diff docker-shell.sh"

# ------------------------------------------------------------------ real outputs (file line numbers)
_ver = capture("01", "laptop")
assert _ver.cmd == DOCKER_CHECK, _ver.cmd
VER_OUT = _ver.at((2, 3))                               # Docker version 29.8.2 … / Compose v5.6.0
assert "29.8.2" in VER_OUT[0] and "v5.6.0" in VER_OUT[1], VER_OUT

_clone = capture("02", "laptop")
assert _clone.cmd == CLONE, _clone.cmd
CLONE_OUT = _clone.at(2)                                # Cloning into 'llm-rag'...

_mk = capture("03", "laptop")
assert _mk.cmd == MKDIR, _mk.cmd
MK_OUT = _mk.at(2)                                      # llm-rag  secrets

_cd = capture("04", "laptop")
assert _cd.cmd == CD and _cd.exit == 0, _cd.cmd         # no output

_ls = capture("05", "laptop")
assert _ls.cmd == LS, _ls.cmd
LS_OUT = _ls.at((2, 5))                                 # the ls -a columns (80 wide: see gap_wrap)
LOG = _ls.cut(6, "origin/HEAD)")                        # e17a39f (HEAD -> main, origin/main, origin/HEAD)
assert LOG.startswith("e17a39f "), LOG

_diff = capture("06", "laptop")
assert _diff.cmd == DIFF, _diff.cmd
DIFF_OUT = _diff.at((6, 13))                            # @@ … through export IMAGE_NAME=…
assert DIFF_OUT[4].startswith("-export GCP_PROJECT=") and DIFF_OUT[5].startswith("+export GCP_PROJECT=")
assert "your-project-id" in DIFF_OUT[5] and "/secrets/" in DIFF_OUT[6], DIFF_OUT

# README.md (dlops-io/llm-rag @ e17a39f): line 48 and the folder layout of lines 66-69
_readme = source_text("README.md").split("\n")
assert "Cloned this repository" in _readme[47], _readme[47]
assert _readme[66:68] == ["|-llm-rag", "|-secrets"], _readme[65:69]
assert "Gemini Enterprise Agent Platform User" in _readme[57] and "Storage Admin" in _readme[56]
GRANT_HEAD = "Grant this service account access to project"
assert GRANT_HEAD in _readme[55], _readme[55]
# docker-shell.sh: line 7 is GCP_PROJECT, line 8 the credentials path (the SAY's line numbers)
_shell = source_text("docker-shell.sh").split("\n")
assert _shell[6].startswith("export GCP_PROJECT=") and _shell[7].startswith("export GOOGLE_APPLICATION")

ROLE_STORAGE = "Storage Admin"
ROLE_VERTEX = "Gemini Enterprise Agent Platform User"
SA_NAME = "llm-service-account"
URL = "console.cloud.google.com"

# ------------------------------------------------------------------ layout
TERM0_BOTTOM = -2.95          # beat 0: room for the GREY note under the terminal
RX = 4.68                     # centre of the right column (folders) in beats 1-2
GATE_Y = -1.55                # centre of the three gates (beats 3-4)
GATE_X = (-5.0, -1.6, 5.0)   # the third far right: beat 4's Storage Admin row runs to x ~ 4


# ------------------------------------------------------------------ small helpers
def first_half(t: float) -> float:
    return smooth(min(1.0, 2 * t))


def second_half(t: float) -> float:
    return smooth(max(0.0, 2 * t - 1))


def at_left(m, x: float, y: float):
    """Put m's left edge at x and its centre at height y."""
    return m.shift(np.array([x - m.get_left()[0], y - m.get_center()[1], 0]))


def attach(scene, row, *mobs):
    """Make mobs (already on screen) part of terminal row `row`, as pin() does: they scroll,
    clear and fade with it."""
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def under_row(mob, t, line):
    """A tag for a command row too long to have one beside it: at the right end of the row
    below (whose output is short), as the pilot does. Returns mob (not added)."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    mob.set_y(row.strut.get_center()[1] - t.pitch)
    return mob.align_to(t.box, RIGHT).shift(LEFT * 0.12)


def col_x(line, j: float) -> float:
    """x of the left edge of character cell j of a mono_line, measured from its glyphs (the
    strut's left edge sits about 2/3 of a cell left of cell 0, so common.col_box drifts)."""
    cw = cell_width(line.pt)
    offs, gi = [], 0
    for k, ch in enumerate(line.text):
        if ch.isspace():
            continue
        offs.append(line.glyphs[gi].get_center()[0] - (k + 0.5) * cw)
        gi += 1
    x0 = float(np.median(offs)) if offs else line.strut.get_left()[0]
    return x0 + j * cw


def gap_wrap(rows: list[str], limit: int) -> list[str]:
    """Captured `ls` rows wider than the terminal, each broken at its last column gap (two or
    more spaces) that fits, the rest on its own row from column 0: a hard fold at the edge split
    'semantic_splitter.py' into 'semantic_splitt' / 'er.py'. Every name is the capture's text."""
    out = []
    for s in rows:
        s = s.rstrip()
        while len(s) > limit:
            cuts = [m.start() for m in re.finditer(r" {2,}", s) if m.start() <= limit]
            if not cuts:
                raise ValueError(f"no column gap within {limit} columns: {s!r}")
            out.append(s[:cuts[-1]])
            s = s[cuts[-1]:].lstrip()
        out.append(s)
    return out


def cbox(line, a: int, b: int, color: str = TURN, pad: float = 0.04) -> VMobject:
    """common.col_box on the glyph-measured grid: a box over character cells a..b (exclusive)."""
    cw = cell_width(line.pt)
    r = box((b - a) * cw + 2 * pad, line.strut.height + 2 * pad, color, fill_opacity=0.0,
            radius=0.06, stroke=3)
    r.move_to([col_x(line, a) + (b - a) * cw / 2, line.strut.get_center()[1], 0])
    return r


def crumb(*parts, size: float = TAG, colors=None) -> VGroup:
    """A console breadcrumb: the parts joined by GREY '›' (as L04 S05). .items"""
    colors = colors or [INK] * len(parts)
    row, items = VGroup(), []
    for i, (p, c) in enumerate(zip(parts, colors)):
        if i:
            row.add(label("›", size, S.GREY))
        m = p if not isinstance(p, str) else label(p, size, c)
        row.add(m)
        items.append(m)
    row.arrange(RIGHT, buff=0.14)
    row.items = items
    return row


def folders() -> VGroup:
    """~/AC215 holding llm-rag/ and secrets/ side by side (GREY glyphs, white mono names), a
    GREY bracket over both. Centred at x = 0. .repo .sec (glyphs) .repo_name .sec_name .ws .bar"""
    gr = folder_glyph(0.78, LAPTOP).move_to([-0.85, 0, 0])
    gs = folder_glyph(0.78, LAPTOP).move_to([0.85, 0, 0])
    nr = mono("llm-rag/", TAG, INK).next_to(gr, DOWN, buff=0.14)
    ns = mono("secrets/", TAG, INK).next_to(gs, DOWN, buff=0.14)
    y = gr.get_top()[1] + 0.22
    bar = VMobject(stroke_color=S.GREY, stroke_width=3)
    bar.set_points_as_corners([[-1.55, y - 0.13, 0], [-1.55, y, 0], [1.55, y, 0], [1.55, y - 0.13, 0]])
    ws = mono("~/AC215", TAG, S.GREY).next_to(bar, UP, buff=0.1)
    g = VGroup(ws, bar, gr, gs, nr, ns)
    g.repo, g.sec, g.repo_name, g.sec_name, g.ws, g.bar = gr, gs, nr, ns, ws, bar
    return g


def gate(text: str, w: float = 1.2, h: float = 1.0) -> VGroup:
    """A small BLUE gate (L04's V3 in miniature): two posts, a lintel, a barrier across the
    opening (it opens by retracting into the left post: .open()), the question above.
    .barrier .label .posts"""
    l_post = Line([-w / 2, -h / 2, 0], [-w / 2, h / 2, 0], color=CLOUD, stroke_width=6)
    r_post = Line([w / 2, -h / 2, 0], [w / 2, h / 2, 0], color=CLOUD, stroke_width=6)
    lintel = Line([-w / 2 - 0.08, h / 2, 0], [w / 2 + 0.08, h / 2, 0], color=CLOUD, stroke_width=6)
    barrier = Rectangle(width=w - 0.08, height=0.13, stroke_color=CLOUD, stroke_width=2)
    barrier.set_fill(CLOUD, 0.6).move_to([0, -0.05, 0])
    # the question on a common baseline (a bare next_to lifts "may?" by its descender): laid out
    # as "|" + text, the pipe's foot set just above the lintel, then the pipe dropped
    full = label("|" + text, TAG, INK)
    q = VGroup(*full.submobjects[1:])
    q.shift(np.array([-q.get_center()[0], h / 2 + 0.08 - full[0].get_bottom()[1], 0]))
    g = VGroup(l_post, r_post, lintel, barrier, q)
    g.barrier, g.label, g.posts = barrier, q, VGroup(l_post, r_post, lintel)
    g.open = lambda: barrier.animate.stretch(0.06, 0, about_edge=LEFT)
    return g


def course_row() -> VGroup:
    """The turn card's first row, "in your course folder (~/AC215)", with the path in mono (the
    serif font draws '~' as a raised accent). Baselines matched glyph to glyph."""
    a = label("in your course folder (", CAPTION, INK)
    m = mono("~/AC215", CAPTION, INK).next_to(a, RIGHT, buff=0.05)
    m.shift(UP * (a[0].get_bottom()[1] - m[2].get_bottom()[1]))           # "i" and "A" on one line
    c = label(")", CAPTION, INK).next_to(m, RIGHT, buff=0.05)
    c.shift(UP * (a[-1].get_bottom()[1] - c.get_bottom()[1]))              # ")" level with "("
    return VGroup(a, m, c)


def error_chip() -> VGroup:
    """The dimmed RED 'without it' chip (SERVICE_DISABLED in mono)."""
    row = VGroup(label("without it:", CAPTION, ERR), mono("SERVICE_DISABLED", CAPTION, ERR),
                 label("on the first embed, after 5 retries", CAPTION, ERR)).arrange(RIGHT, buff=0.14)
    fr = box(row.width + 0.5, row.height + 0.26, ERR, fill=S.BG, fill_opacity=0.95, radius=0.12)
    fr.move_to(row)
    g = VGroup(fr, row)
    g.frame, g.row = fr, row
    return g


def file_card() -> VGroup:
    """A GREY file card 'docker-shell.sh' with the caption 'in your editor' above it, and two
    blank rows (the file's text is the diff's job). .frame .name .rows .caption"""
    fg = file_glyph(0.42, S.GREY)
    nm = mono("docker-shell.sh", TAG, INK).next_to(fg, RIGHT, buff=0.18)
    head = VGroup(fg, nm)
    rows = VGroup(Line(LEFT * 0, RIGHT * 2.9, color=S.GREY_DARK, stroke_width=5))
    rows.next_to(head, DOWN, buff=0.22).align_to(head, LEFT)
    body = VGroup(head, rows)
    fr = box(body.width + 0.6, body.height + 0.36, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    body.move_to(fr)
    cap = note("in your editor").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(fr, body, cap)
    g.frame, g.name, g.rows, g.caption = fr, nm, rows, cap
    return g


# ------------------------------------------------------------------ console screens (schematic)
def console(width: float, height: float, center) -> VGroup:
    """A GREY browser frame on the console address (no logo) with the illustration tag at its
    bottom-right corner, inside. .win .ill .x0 .y0 (left edge and first row of the page)"""
    win = browser_window(URL, width=width, height=height).move_to(center)
    ill = illustration_tag()
    ill.move_to(win.frame.get_corner(DOWN + RIGHT) + np.array([-ill.width / 2 - 0.2, ill.height / 2 + 0.16, 0]))
    g = VGroup(win, ill)
    g.win, g.ill = win, ill
    g.x0 = win.frame.get_left()[0] + 0.4
    g.y0 = win.frame.get_top()[1] - 0.55 - 0.45
    return g


def screens(con) -> list:
    """The service-account pages, each a VGroup placed in `con`; the crumb is part [0].
    1 Service accounts · 2 Create (form, value typed later: .value) · 3 Grant access (.chips .note)
    · 4 the account's tabs (.keys) · 5 Add key › Create new key › JSON (.dl: download chip,
    .dl.key .dl.name)."""
    x0, y0 = con.x0, con.y0
    out = []
    # 1 · IAM & Admin › Service accounts
    c1 = at_left(crumb("IAM & Admin", "Service accounts", colors=[S.GREY, INK]), x0, y0)
    b1 = at_left(chip("+ Create service account", CLOUD, size=CAPTION), x0, y0 - 0.8)
    rows1 = VGroup(*[Line(LEFT * 0, RIGHT * 6.6, color=S.GREY_DARKER, stroke_width=10) for _ in range(3)])
    rows1.arrange(DOWN, buff=0.32)
    at_left(rows1, x0, y0 - 1.95)
    s1 = VGroup(c1, b1, rows1)
    s1.button = b1
    out.append(s1)
    # 2 · Create service account (name typed)
    c2 = at_left(crumb("IAM & Admin", "Service accounts", "Create service account",
                       colors=[S.GREY, S.GREY, INK]), x0, y0)
    lab = label("Service account name", TAG, S.GREY)
    fld = RoundedRectangle(width=4.0, height=0.48, corner_radius=0.06, stroke_color=S.GREY_DARK,
                           stroke_width=1.5).set_fill(TERM_BG, 1)
    fld.next_to(lab, RIGHT, buff=0.3)
    form = at_left(VGroup(lab, fld), x0, y0 - 0.85)
    value = mono(SA_NAME, CAPTION, INK).move_to(fld).align_to(fld, LEFT).shift(RIGHT * 0.15)
    btn = at_left(chip("Create and continue", CLOUD, size=CAPTION), x0, y0 - 1.65)
    s2 = VGroup(c2, form, btn)
    s2.value, s2.button = value, btn
    out.append(s2)
    # 3 · Grant this service account access to project (README.md line 56)
    c3 = at_left(crumb("Service accounts", "Create service account", colors=[S.GREY, INK]), x0, y0)
    hd = at_left(label(GRANT_HEAD, TAG, INK), x0, y0 - 0.62)
    ch_s = at_left(chip(ROLE_STORAGE, CLOUD, size=TAG), x0, y0 - 1.3)
    ch_v = at_left(chip(ROLE_VERTEX, CLOUD, size=TAG), x0, y0 - 1.95)
    nt = note("Vertex AI User in older projects").next_to(ch_v, DOWN, buff=0.16).align_to(ch_v, LEFT).shift(RIGHT * 0.1)
    s3 = VGroup(c3)
    s3.head, s3.chips, s3.note = hd, VGroup(ch_s, ch_v), nt
    out.append(s3)
    # 4 · the account's tabs: KEYS
    c4 = at_left(crumb("Service accounts", mono(SA_NAME, CAPTION, INK), colors=[S.GREY, INK]), x0, y0)
    tabs = VGroup(*[box(1.3, 0.16, S.GREY_DARK, fill_opacity=0.6, radius=0.05) for _ in range(2)])
    keys = label("KEYS", TAG, INK)
    tabs.add(keys).arrange(RIGHT, buff=0.45)
    at_left(tabs, x0, y0 - 0.8)
    rule = Line([x0, y0 - 1.1, 0], [x0 + 7.0, y0 - 1.1, 0], color=S.GREY_DARK, stroke_width=2)
    s4 = VGroup(c4, tabs, rule)
    s4.keys = keys
    out.append(s4)
    # 5 · Add key › Create new key › JSON, and the download
    path = at_left(crumb(chip("Add key", CLOUD, size=CAPTION), "Create new key",
                         chip("JSON", CLOUD, size=CAPTION)), x0, y0 - 1.55)
    k = key_glyph(0.34)
    nm = mono("<project>-<hex>.json", CAPTION, S.GREY)
    row = VGroup(k, nm).arrange(RIGHT, buff=0.22)
    fr = box(row.width + 0.5, 0.52, S.GREY, fill=S.BG, fill_opacity=1, radius=0.1).move_to(row)
    dl = VGroup(fr, row)
    at_left(dl, x0, y0 - 2.35)
    dl.key, dl.name, dl.frame = k, nm, fr
    s5 = VGroup(path)
    s5.dl = dl
    out.append(s5)
    return out


def vertex_console(center) -> VGroup:
    """Beat 4: APIs & Services › Vertex AI API · aiplatform.googleapis.com › Enable."""
    con = console(8.9, 2.35, center)
    x0, y0 = con.x0, con.y0
    cr = at_left(crumb("APIs & Services", "Vertex AI API", colors=[S.GREY, INK]), x0, y0)
    svc = at_left(mono("aiplatform.googleapis.com", CAPTION, S.GREY), x0, y0 - 0.62)
    en = chip("Enable", CLOUD, size=CAPTION).next_to(svc, RIGHT, buff=0.5)
    g = VGroup(con, cr, svc, en)
    g.con, g.enable = con, en
    return g


# ------------------------------------------------------------------ the scene
class KeyAndProject(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, f"S03 has {len(SAY)} SAY lines; this scene times 7"

        # ========================================================== 0 · Docker (extra check)
        tr = tracker("Prereq", 1)
        t = term(P_WS, rows=10)
        t.shift(UP * (TERM0_BOTTOM - t.box.get_bottom()[1]))
        mac = note("Mac: zsh, prompt ends in %")
        win_ = note("· Windows: WSL or Git Bash")
        os_note = VGroup(mac, win_).arrange(RIGHT, buff=0.2).move_to([0, -3.27, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.7)
            self.play(Indicate(tr.dots[0], color=TURN, scale_factor=1.6), run_time=0.7)
            vo.wait_until("This extra check")
            self.play(caption_extra(tr, True), run_time=0.4)
            cmd0 = type_cmd(self, t, DOCKER_CHECK, 1.3)
            out0 = t.print(self, VER_OUT, run_time=0.5)
            # a 64-of-65-column row: the extra tag sits at the right end of the output row below
            xt0 = under_row(extra_tag(), t, cmd0)
            pin(self, out0[0], xt0, run_time=0.3)
            # the two versions: GREY underlines, one bracket, one tag (attached to the first row)
            u1 = under(substring(out0[0], "29.8.2"), S.GREY, stroke=3)
            u2 = under(substring(out0[1], "v5.6.0"), S.GREY, stroke=3)
            xb = out0[0].glyphs.get_right()[0] + 0.25
            yt, yb = out0[0].strut.get_top()[1], out0[1].strut.get_bottom()[1]
            brk = VMobject(stroke_color=S.GREY, stroke_width=3)
            brk.set_points_as_corners([[xb - 0.12, yt, 0], [xb, yt, 0], [xb, yb, 0], [xb - 0.12, yb, 0]])
            rec = recording_tag()
            rec.move_to([xb + 0.2 + rec.width / 2, (yt + yb) / 2, 0])
            self.play(Create(u1), Create(u2), run_time=0.5)
            self.play(Create(brk), FadeIn(rec, shift=LEFT * 0.1), run_time=0.5)
            attach(self, out0[0], u1, brk, rec)
            attach(self, out0[1], u2)

            vo.wait_until("the script needs docker compose")
            line = cmd0
            sp = len(P_WS) + 1 + DOCKER_CHECK.index("docker compose") + len("docker")
            # a filled block in the space itself, between the glyphs of "docker" and "compose"
            # (a whole-cell box covered the arm of the "r", and a 1.35 pulse ate into both
            # words): 0.045 clear of each glyph, so the 1.2 pulse stays inside the gap
            x_r = glyph_range(line, sp - 1, sp).get_right()[0]
            x_c = glyph_range(line, sp + 1, sp + 2).get_left()[0]
            gap = box(x_c - x_r - 0.09, 0.3, TURN, fill_opacity=0.75, radius=0.05, stroke=3)
            gap.move_to([(x_r + x_c) / 2, line.strut.get_center()[1], 0])
            words = glyph_range(line, sp - len("docker"), sp + len(" compose"))
            self.play(FadeIn(gap, scale=1.2), words.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(gap, color=TURN, scale_factor=1.2), run_time=0.6)
            self.play(Indicate(gap, color=TURN, scale_factor=1.2), run_time=0.6)
            self.play(FadeOut(gap), words.animate.set_color(INK), run_time=0.4)

            vo.wait_until("On a Mac")
            self.play(FadeIn(mac, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("on Windows")
            self.play(FadeIn(win_, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 1 · clone, secrets, the layout
        chip48 = readme_chip("README.md · line 48", "Cloned this repository")
        chip48.move_to([6.45 - chip48.width / 2, 3.2, 0])
        fo = folders().move_to([RX, 1.95, 0])
        u_repo = under(fo.repo_name, TURN, stroke=4)
        exact = tag("exactly this name", TURN).next_to(u_repo, DOWN, buff=0.14)
        exact.set_x(fo.repo_name.get_center()[0])
        if exact.get_left()[0] < 2.75:
            exact.shift(RIGHT * (2.75 - exact.get_left()[0]))
        card66 = readme_card("README.md · lines 66–69", ["`|-llm-rag`", "`|-secrets`"])
        card66.move_to([RX, -0.6, 0])
        tcard = turn_card([Prose("in your course folder (~/AC215)"), CLONE, (MKDIR, "extra")])
        row0 = tcard.rows[0]
        tcard.rows.submobjects[0] = course_row().move_to(row0).align_to(row0, LEFT)
        at_left(tcard, -6.4, 0.55)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(os_note), t.animate.shift(DOWN * (t.box.get_bottom()[1] - BOTTOM)),
                      caption_extra(tr, False), run_time=0.6)
            self.play(tr.goto(2), FadeIn(chip48, shift=DOWN * 0.1), run_time=0.6)
            self.play(Indicate(chip48.phrase, color=TURN, scale_factor=1.06), run_time=0.7)
            type_cmd(self, t, CLONE, 1.6)
            t.print(self, CLONE_OUT, run_time=0.4)

            vo.wait_until("Then, as an extra")
            self.play(caption_extra(tr, True), FadeOut(chip48), run_time=0.4)
            cmd2 = type_cmd(self, t, MKDIR, 0.8)
            pin(self, cmd2, beside(extra_tag(), t, cmd2), run_time=0.3)
            out2 = t.print(self, MK_OUT, run_time=0.4)[0]
            vo.wait_until("make a secrets folder")
            resize(self, t, 3, keep=[cmd2, out2])
            self.play(FadeIn(fo.ws), Create(fo.bar), FadeIn(fo.repo, shift=DOWN * 0.15),
                      FadeIn(fo.repo_name), run_time=0.6)
            self.play(FadeIn(fo.sec, shift=DOWN * 0.15), FadeIn(fo.sec_name),
                      Indicate(substring(out2, "secrets"), color=TURN, scale_factor=1.15), run_time=0.6)

            vo.wait_until("and keep the clone's name")
            self.play(Create(u_repo), FadeIn(exact, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(card66, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(card66.rows[0], color=TURN, scale_factor=1.1),
                      Indicate(fo.repo_name, color=TURN, scale_factor=1.1), run_time=0.8)

            vo.wait_until("Pause and do both")
            self.play(FadeIn(tcard, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(2)                                   # ▶ beat: hold the frame

        # ========================================================== 2 · the console, the key
        con = console(8.35, 4.35, [-2.17, 0.5, 0])
        pages = screens(con)
        org = card_rows(["key creation blocked by an org policy?",
                         "use a personal project, not one under the university's organization"])
        org.move_to([con.win.frame.get_left()[0] + org.width / 2, -2.55, 0])
        key_name = mono(KEY_FILE, CAPTION, COST)
        key_name.move_to([6.45 - key_name.width / 2, fo.sec_name.get_bottom()[1] - 0.38, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(t, tcard, card66, exact, u_repo)), run_time=0.5)
            tr = switch_section(self, tr, "Account", 1)
            self.play(FadeIn(con), FadeIn(pages[0]), run_time=0.6)
            cr = pages[0][0]
            self.play(Indicate(cr.items[1], color=TURN, scale_factor=1.1), run_time=0.7)
            self.play(Indicate(pages[0].button, color=TURN, scale_factor=1.08), run_time=0.7)

            def page_to(k, old, new, *extra):
                """The crumb slides to page k's, `old` parts leave and `new` parts arrive: old out in the
                first half, new in the second (faded at once, both pages' crumbs and fields read on top
                of each other)."""
                nonlocal cr
                anims = [tr.goto(k), FadeOut(cr, shift=LEFT * 0.25, rate_func=first_half),
                         FadeIn(pages[k - 1][0], shift=LEFT * 0.25, rate_func=second_half)]
                if old:
                    anims.append(FadeOut(VGroup(*old), rate_func=first_half))
                if new:
                    anims.append(FadeIn(VGroup(*new), shift=UP * 0.1, rate_func=second_half))
                self.play(*anims, *extra, run_time=0.6)
                cr = pages[k - 1][0]

            vo.wait_until("Create one called")
            page_to(2, [pages[0].button, pages[0][2]], [pages[1][1], pages[1][2]])
            self.play(ShowIncreasingSubsets(pages[1].value, rate_func=linear), run_time=1.0)

            vo.wait_until("and grant it two roles")
            page_to(3, [pages[1][1], pages[1][2], pages[1].value], [pages[2].head])
            vo.wait_until("Storage Admin")
            self.play(FadeIn(pages[2].chips[0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and Gemini Enterprise")
            self.play(FadeIn(pages[2].chips[1], shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(pages[2].note), run_time=0.5)

            vo.wait_until("Open its keys tab")
            page_to(4, [pages[2].head, pages[2].chips, pages[2].note], [pages[3][1], pages[3][2]])
            ukeys = under(pages[3].keys, TURN, stroke=5)
            self.play(Create(ukeys), Indicate(pages[3].keys, color=TURN), run_time=0.6)

            vo.wait_until("add a JSON key")
            self.play(tr.goto(5), FadeIn(pages[4][0], shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(pages[4][0].items[2], color=TURN, scale_factor=1.15), run_time=0.5)
            self.play(FadeIn(pages[4].dl, shift=UP * 0.1), FadeIn(org, shift=UP * 0.1), run_time=0.6)

            vo.wait_until("and save it in secrets")
            dl = pages[4].dl
            self.play(tr.goto(6), run_time=0.4)
            # the key flies; the old name fades in place and the new one fades in under secrets/ (the
            # name morphing along the key's path ran garbled across the JSON chip)
            self.play(dl.key.animate(path_arc=-0.9).move_to(fo.sec.get_center() + DOWN * 0.06),
                      FadeOut(dl.name), FadeIn(key_name), FadeOut(dl.frame), run_time=1.2)
            self.remove(dl)
            self.add(dl.key, key_name)
            self.play(Indicate(fo.sec, color=COST, scale_factor=1.1), run_time=0.6)

        # ========================================================== 3 · money, .gitignore, three gates
        key, key_lbl = dl.key, key_name
        drop = VGroup(fo, key, key_lbl)
        gi = src_panel(".gitignore", 1, 5)
        gi.move_to([3.6, 1.55, 0])
        ghost_txt = mono("secrets", TAG, S.GREY)
        ghost_box = box(ghost_txt.width + 0.6, ghost_txt.height + 0.3, S.GREY, dashed=True, stroke=2)
        ghost = VGroup(ghost_box, ghost_txt)
        ghost.next_to(gi, DOWN, buff=0.2).align_to(gi.code, LEFT).shift(RIGHT * 0.25)
        ghost_txt.move_to(ghost_box)
        not_here = grey_tag("not here").next_to(ghost, RIGHT, buff=0.25)
        gates = [gate("who?"), gate("may?"), gate("switched on?")]
        for g, x in zip(gates, GATE_X):
            g.shift(np.array([x, GATE_Y, 0]) - g.posts.get_center())
        g_key = key_glyph(0.34).next_to(gates[0].posts, DOWN, buff=0.35)
        c_store = chip(ROLE_STORAGE, CLOUD, size=CAPTION)
        c_vert = chip(ROLE_VERTEX, CLOUD, size=CAPTION)
        roles = VGroup(c_store, c_vert).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        at_left(roles, gates[1].posts.get_left()[0] - 1.25, 0).align_to(g_key, UP).shift(UP * 0.05)
        sw = toggle(False, CLOUD, w=0.62).next_to(gates[2].posts, DOWN, buff=0.38)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(con, cr, pages[3][1], pages[3][2], ukeys,
                                     pages[4][0], org)), run_time=0.5)
            self.play(drop.animate.shift(np.array([-6.35 - key_lbl.get_left()[0],
                                                   2.62 - fo.ws.get_top()[1], 0])), run_time=0.8)
            money = tag("this file spends your project's money", COST)
            money.next_to(key_lbl, DOWN, buff=0.2).align_to(key_lbl, LEFT)
            if money.get_left()[0] < -6.45:
                money.shift(RIGHT * (-6.45 - money.get_left()[0]))
            self.play(FadeIn(money, shift=UP * 0.1), Indicate(key, color=COST, scale_factor=1.3), run_time=0.7)

            vo.wait_until("the git ignore file")
            self.play(FadeIn(gi, shift=LEFT * 0.4), run_time=0.7)
            vo.wait_until("has no secrets line")
            self.play(Create(ghost_box), FadeIn(ghost_txt), FadeIn(not_here, shift=LEFT * 0.1), run_time=0.6)

            vo.wait_until("so it's safe only beside the repo")
            self.play(Indicate(fo.repo, color=TURN, scale_factor=1.15),
                      Indicate(fo.repo_name, color=TURN, scale_factor=1.1), run_time=0.7)
            self.play(Indicate(fo.sec, color=TURN, scale_factor=1.15),
                      Indicate(fo.sec_name, color=TURN, scale_factor=1.1), run_time=0.7)

            vo.wait_until("Remember the three gates")
            self.play(LaggedStart(*[Create(g.posts) for g in gates], lag_ratio=0.25), run_time=0.9)
            self.play(*[FadeIn(g.barrier) for g in gates], run_time=0.4)
            vo.wait_until("the key says who you are")
            self.play(FadeIn(gates[0].label, shift=DOWN * 0.1),
                      FadeIn(g_key, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("the role what you may do")
            self.play(FadeIn(gates[1].label, shift=DOWN * 0.1),
                      LaggedStart(FadeIn(c_store, shift=UP * 0.15), FadeIn(c_vert, shift=UP * 0.15),
                                  lag_ratio=0.4), run_time=0.8)
            vo.wait_until("and the API must be switched on")
            self.play(FadeIn(gates[2].label, shift=DOWN * 0.1), FadeIn(sw, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(sw, color=TURN, scale_factor=1.25), run_time=0.7)

        # ========================================================== 4 · two slips, the API, your turn
        # while the slips are named, the gates rise to the middle of the emptied frame; they go
        # back down when the Vertex AI screen arrives above them
        LIFT = UP * 1.75
        gate_row = VGroup(*gates, g_key, roles, sw)
        # the erratum is the Storage Admin line (QA: beside the Agent Platform chip it read as
        # "this role is the mistake"); that chip gets a GREEN "✓ needed" instead
        err_tag = erratum_tag().next_to(c_store, RIGHT, buff=0.25).shift(LIFT)
        no_store = note("no storage call in this code").next_to(err_tag, RIGHT, buff=0.25)
        need = VGroup(check_mark(0.3, DATA), label("needed", TAG, DATA)).arrange(RIGHT, buff=0.12)
        need.next_to(c_vert, RIGHT, buff=0.3).shift(LIFT)
        vx = vertex_console([-0.75, 1.55, 0])
        sw_on = toggle(True, CLOUD, w=0.62).move_to(sw)
        tick = check_mark(0.42, INK).move_to(gates[2].posts.get_center() + DOWN * 0.05)
        red = error_chip()
        red.move_to([vx.con.win.frame.get_right()[0] - red.width / 2, -0.05, 0])
        red.set_opacity(0.5)
        rows = [Prose(f"IAM & Admin › Service accounts › Create: {SA_NAME}"),
                Prose(f"roles: {ROLE_VERTEX} (Vertex AI User) · {ROLE_STORAGE}"),
                Prose("KEYS › Add key › Create new key › JSON"),
                Prose(f"rename it {KEY_FILE}, into secrets/ beside llm-rag/"),
                Prose("APIs & Services › Vertex AI API › Enable"),
                (Prose(f"check: ls secrets → {KEY_FILE}"), S.GREY)]
        card4 = turn_card(rows, header="your turn · in the console")
        xt4 = extra_tag().next_to(card4.rows[4], RIGHT, buff=0.3)
        card4.add(xt4)
        ill4 = illustration_tag()
        ill4.move_to(card4.frame.get_corner(DOWN + RIGHT) + np.array([-ill4.width / 2 - 0.2, 0, 0]))
        card4.add(ill4)
        card4.move_to([0, -0.15, 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(drop, money, gi, ghost, not_here)), run_time=0.45)
            self.play(gate_row.animate.shift(LIFT), run_time=0.6)
            self.play(FadeIn(err_tag, shift=LEFT * 0.1),
                      Indicate(c_store, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Nothing here uses Cloud Storage")
            self.play(c_store.box.animate.set_stroke(S.GREY), c_store.text.animate.set_color(S.GREY),
                      FadeIn(no_store, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("so the Agent Platform role")
            self.play(Indicate(c_vert, color=TURN, scale_factor=1.08),
                      FadeIn(need, shift=LEFT * 0.1), run_time=0.8)

            vo.wait_until("And the README never says")
            self.play(caption_extra(tr, True), VGroup(gate_row, err_tag, no_store, need).animate.shift(-LIFT),
                      FadeIn(vx, shift=DOWN * 0.15), run_time=0.8)
            vo.wait_until("to enable the Vertex AI API")
            self.play(Indicate(vx.enable, color=TURN, scale_factor=1.2), run_time=0.6)
            self.play(Transform(sw, sw_on), run_time=0.5)
            self.play(gates[2].open(), run_time=0.5)
            self.play(Create(tick), run_time=0.4)
            vo.wait_until("without it")
            self.play(FadeIn(red, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("fails with service disabled")
            self.play(red.animate.set_opacity(1.0), run_time=0.4)        # brightens, then dims again
            self.play(red.animate.set_opacity(0.5), run_time=0.6)

            vo.wait_until("Pause and do it all now")
            self.play(FadeOut(VGroup(vx, red, *gates, g_key, roles, sw, tick, err_tag, no_store, need)),
                      run_time=0.5)
            self.play(*[d.animate.set_color(TURN) for d in tr.dots], FadeIn(card4, shift=UP * 0.15),
                      run_time=0.7)
            vo.wait_until("account, roles")              # the rows light as they are named
            self.play(LaggedStart(*[Indicate(r, color=TURN, scale_factor=1.0) for r in card4.rows[:5]],
                                  lag_ratio=0.45), run_time=2.2)
        self.wait(2)                                   # ▶ beat: hold the frame

        # ========================================================== 5 · cd llm-rag, an extra look
        t5 = term(P_WS, rows=10)      # 9 rows of output + one empty row for the commit tag
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(card4), run_time=0.4)
            tr = switch_section(self, tr, "Run", 1)
            self.play(FadeIn(t5), run_time=0.4)
            type_cmd(self, t5, CD, 0.6)
            cd_prompt(self, t5, P_REPO)

            vo.wait_until("An extra look")
            self.play(caption_extra(tr, True), run_time=0.3)
            cmd5 = type_cmd(self, t5, LS, 0.7)
            # 59 of 65 columns: beside() clamps the tag to the terminal's right end, still ~0.17
            # clear of "-1" (pin() would refuse a cover); the row below is full ls output
            pin(self, cmd5, beside(extra_tag(), t5, cmd5), run_time=0.25)
            ls_rows = gap_wrap(LS_OUT, t5.max_chars)              # 4 rows -> 6, no name split
            assert len(ls_rows) == 6 and "semantic_splitter.py" in ls_rows and "uv.lock" in ls_rows, ls_rows
            log = t5.print(self, ls_rows + [LOG], run_time=0.5)[-1]                 # LOG fits a row
            assert log.text == LOG, log.text
            hl = []
            for name, anchor in (("docker-shell.sh", "the scripts"), ("docker-compose.yml", "the compose file"),
                                 ("cli.py", "cli.py, and")):
                vo.wait_until(anchor)
                ln = t5.find(name)
                i = ln.text.index(name)
                b = cbox(ln, i, i + len(name), DATA)
                self.play(Create(b), substring(ln, name).animate.set_color(DATA), run_time=0.45)
                attach(self, ln, b)
                hl.append(b)
            vo.wait_until("and the commit")
            ring_ = cbox(log, 0, 7, S.GREY)
            # the commit row has no room left for the tag (and a tag on the row above would
            # touch the cli.py box): it sits on the empty last row, under the hash
            cm = grey_tag("↑ the commit this video was recorded on")
            at_left(cm, ring_.get_left()[0], log.strut.get_center()[1] - t5.pitch)
            self.play(Create(ring_), run_time=0.4)
            attach(self, log, ring_)
            pin(self, log, cm, run_time=0.4)

        # ========================================================== 6 · GCP_PROJECT in docker-shell.sh
        # the band above the 10-row terminal: the editor card top right (the tracker owns the top
        # left), the pencil and later ▶ your turn to its left, the skip note low on the left
        fc = file_card()
        fc.move_to([6.45 - fc.width / 2, (t5.box.get_top()[1] + 3.4) / 2, 0])
        pen = pencil(0.6, S.GREY)
        pen.move_to(fc.frame.get_left() + np.array([-0.7, 0.25, 0]))
        skip = note("skip it → calls go to the course's project → permission error")
        at_left(skip, -6.4, t5.box.get_top()[1] + 0.3)

        with self.voiceover(SAY[6]) as vo:
            # the ls output leaves as the editor card arrives: the edit happens there first
            self.play(tr.goto(2), FadeIn(fc, shift=DOWN * 0.1), FadeOut(t5.lines), run_time=0.6)
            for m in list(t5.lines):
                t5.lines.remove(m)
            self.play(FadeIn(pen, shift=RIGHT * 0.2), run_time=0.3)
            r0 = fc.rows[0]
            tip = pen.tip_point()
            a = r0.get_left() + RIGHT * 0.3
            self.play(pen.animate.shift(a - tip), run_time=0.4)
            self.play(pen.animate.shift(RIGHT * 2.0), r0.animate.set_color(TURN), run_time=0.7)
            self.play(pen.animate.shift(fc.frame.get_left() + LEFT * 0.3 - pen.get_right()
                                        + DOWN * (pen.get_center()[1] - fc.frame.get_center()[1])),
                      caption_extra(tr, True), run_time=0.4)
            cmd6 = type_cmd(self, t5, DIFF, 0.9)
            pin(self, cmd6, beside(extra_tag(), t5, cmd6), run_time=0.3)
            cols = {4: ERR, 5: DATA}
            out6 = t5.print(self, [(s, cols.get(k, OUTPUT)) for k, s in enumerate(DIFF_OUT)], run_time=0.6)

            vo.wait_until("to your own Project ID")
            l11 = out6[5]
            i = l11.text.index("your-project-id")
            pid = cbox(l11, i, i + len("your-project-id"), TURN)
            l10 = out6[4]
            j = l10.text.index('" #') + 1                 # the blank column after the old value
            xg = col_x(l10, j + 0.5)
            yt = tag("your Project ID · not the name", TURN)
            at_left(yt, xg - 0.18, out6[3].strut.get_center()[1])
            arr = Line([xg, yt.get_bottom()[1] - 0.02, 0], [xg, pid.get_top()[1] + 0.01, 0],
                       color=TURN, stroke_width=3)
            self.play(Create(pid), run_time=0.4)
            self.play(FadeIn(yt, shift=DOWN * 0.1), Create(arr), run_time=0.5)
            attach(self, l11, pid, arr, yt)
            vo.wait_until("the ID, not the name")
            # the tag's outline and text flash (Indicate on the whole tag filled it YELLOW: text unreadable);
            # 1.04: the outline no longer grows with the text, and at 1.08 the "y" and "e" met its round ends
            self.play(yt.box.animate(rate_func=there_and_back).set_stroke(TURN, 4),
                      Indicate(yt.text, color=TURN, scale_factor=1.04), run_time=0.7)

            vo.wait_until("Leave line 8 alone")
            l12, l13 = out6[6], out6[7]
            k = l12.text.index('"/secrets')
            yb = l12.strut.get_bottom()[1] + 0.01
            u12 = Line([col_x(l12, k), yb, 0], [col_x(l12, len(l12.text)), yb, 0],
                       color=S.GREY, stroke_width=3)
            leave = grey_tag("↑ leave this: a path inside the container")
            beside(leave, t5, l13, buff=0.45)
            self.play(Create(u12), run_time=0.4)
            attach(self, l12, u12)
            pin(self, l13, leave, run_time=0.4)

            vo.wait_until("Skip this")
            self.play(FadeIn(skip, shift=LEFT * 0.15), run_time=0.6)

            vo.wait_until("Pause and edit")
            yt6 = your_turn()                             # where the pencil rested
            yt6.move_to(fc.frame.get_left() + LEFT * (0.3 + yt6.width / 2))
            self.play(FadeIn(yt6, scale=1.2), FadeOut(pen), run_time=0.5)
        self.wait(2)                                   # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tr, t5, fc, yt6, skip)), run_time=0.8)
        self.wait(0.3)
