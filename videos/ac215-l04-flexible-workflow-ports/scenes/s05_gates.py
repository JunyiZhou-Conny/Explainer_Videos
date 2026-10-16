"""S05 · Three gates: account, role, API (README "Service Account & Secrets", steps 1-6).

Beats (script.md "## S05", one voiceover block each):
 0  TRACKER K/1. V3 builds at full width: the TEAL container with its dashed /secrets slot, the
    GREY secrets/ folder with the GOLD key outside its left edge, the PINK route between them. The
    route pulses once and the GOLD key outline appears in the slot at the same instant (nothing
    travels). GREY README card (top band) README.md · line 171: "an identity for your code, not
    for you".
 1  The google.auth stamp presses the outline into the GOLD token (GREY note "short-lived"). The
    five BLUE API doors appear (lock slot + switch each; Text-to-Speech: "no role"); the token
    flies right to the gates of the doors.
 2  "who?" writes over the slot, the slot glows; the token goes home; without the key (the
    laptop's key dims) the outline vanishes, the slot flashes RED, chip DefaultCredentialsError
    + "inside the container". The key comes back (pulse). "may?": the lock slots glow BLUE (a
    filled halo: they are BLUE already). "switched on?": the switches glow BLUE.
 3  V3 shrinks to the right third (the door column; the container side fades). Schematic console
    at left (illustration): IAM & Admin › Service accounts › Create service account, name
    mega-pipeline-sa typed. TRACKER K/2 + README chip lines 177–181: the name becomes the page head
    "› Grant roles"; four roles appear one by one in README order, each with its ID chip (tags
    "all five components", "generate_text · Gemini"); a BLUE padlock flies from each role onto its
    lock (Storage, Vertex AI, Speech-to-Text, Translation).
 4  Text-to-Speech's "no role" flashes, GREY note "no role needed · README.md line 185". The
    console goes; README card generate_text/README.md · line 46 "Vertex AI User" (erratum) is
    flashes YELLOW on "still says Vertex AI User" and is struck RED; README card README.md · line
    179 "Search the role picker for Agent Platform User" gets a GREEN check.
 5  TRACKER K/3. V3 and the cards go; the console's Keys page: Keys › Add Key › Create new key ›
    JSON builds up, Create flashes, a download chip <project>-<hex>.json with the GOLD key (GREY
    caption "the console picks a long name" under the window). TRACKER K/4: S04's tree slides in
    small at right;
    the chip renames itself mega-pipeline.json; the GOLD key drops out of the browser into
    secrets/, the dashed row turns solid (README chip line 183). Two GOLD tags: "whoever holds
    this file spends your project's money", "never commit it · never paste it".
 6  TRACKER K/5. README card lines 187–189 + a tiny console Library (illustration). The 8-row
    laptop terminal (~): `gcloud config set project <your-project-id>` -> gcloud-laptop/01 line 3
    RED; RED rings on < and >, GREY tag "the shell: redirection"; GREY chip "macOS zsh says: …".
    `gcloud config set project your-project-id` -> 02 line 2; YELLOW box + tag "your own ID".
 7  TRACKER K/6. The terminal clears and grows to 12 rows; the README's six rows of `gcloud
    services enable \\` are typed -> 03 lines 7 (folded, RED), 8–10, …; the message underlines
    YELLOW; GREY note "Tutorial 0: gcloud auth login" beside line 10. Chip `gcloud services list
    --enabled` (extra) "with your account: lists the five". The terminal shrinks to the strip; V3
    returns above it; the five switches flip on one by one (tag "illustration · with your
    account"); GOLD tag "calls now bill your project" lands under the doors.
 8  The strip and chips go; V3 moves up: white ticks at gate 1 and on the five switches; the
    Vertex AI padlock lifts off (its slot dashed and empty); a generate_text chip waits under the
    container; the container and the doors flash in turn as the two options are named.
    PONDER (8 s), card at the bottom right.
 9  The card goes; the token leaves the container, flies to the Vertex AI door and bounces RED off
    its empty lock: chip "permission error · from Google" + GREY note "said, not shown: nothing
    here reached Google". Caption "the key says who · the role says may"; GREY note "new roles
    and APIs: allow a few minutes". V3 shrinks to the right third (the padlock back in place); the
    static GREY your-turn card at left (console path, the two gcloud commands as written).
    ▶ your turn. Fade out to an empty frame.

Deviations from SHOW (and why):
- Beat 2: while gate 1 refuses, the laptop's key dims too (without the key there is nothing to
  see in /secrets), and the token leaves; both come back before gate 2.
- Beats 3-4, 9: "V3 shrinks to the right third" keeps the door column (locks, switches, the
  gate 2/3 labels) at 0.8 and fades the laptop and container side: the 20 pt door names do not
  fit a third-width copy of the whole piece.
- Beat 3: the console shows the role rows on two lines (name + tag, then its ID chip): name and
  ID chip side by side are wider than the console column.
- Beat 4: the console fades before the two README cards (no room for both at the left).
- Beat 5: V3 is off screen (the console and the tree need the frame); it returns in beat 7.
  The console spells "Add Key" as README.md line 182 does.
- Beat 7: line 7 is printed on two rows (it is 85 characters: cut at 65 it would lose "active
  account selected", the words the SAY points at), folded at the space before "active" rather
  than at column 65 (which splits "acti|ve"), so the output is lines 7–10 and "…" (12 rows: the
  six typed rows + six output rows). The strip keeps the two ERROR rows and line 10.
- V3: the door column (doors, padlocks, "may?", "switched on?") sits 0.32 further right and the
  token waits in the middle of the gap (widen_gap): at common.py's waiting point the token
  touched the container's wall and the lock column.
- Beat 6: the `<` and `>` circles are narrow upright rings inside their character cells (a
  round ring around one mono glyph touches its neighbours).
- Beats 7-9: the whole V3 returns at 0.9 so the strip (beat 7) and the ponder card (22 pt,
  beat 8) fit under it; the card sits at the bottom right, the generate_text chip under the
  container. On "inside your container" / "or at Google" the container and the doors flash in
  turn (same emphasis for both answers).
- Beat 9: the "allow a few minutes" note sits at the bottom right (it stays with the card); V3
  shrinks and the card arrives during that sentence, so the card is up when "Pause" is said; the
  Vertex AI padlock returns as V3 shrinks (the your-turn picture shows the full setup).
"""

from common import *
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    TAU,
    UP,
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    FadeTransform,
    Indicate,
    LaggedStart,
    Line,
    MoveToTarget,
    Restore,
    RoundedRectangle,
    ShowIncreasingSubsets,
    Succession,
    Transform,
    VGroup,
    Wiggle,
    Write,
    linear,
)

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import form_rows
from explainer.scene import VoiceScene

ThreeGatesPiece = ThreeGates          # V3 from common.py (this file's scene class takes the name)

SAY = NARRATION["S05"]
assert len(SAY) == 10, len(SAY)

README = "mega-pipeline/README.md"
GT_README = "mega-pipeline/generate_text/README.md"
GL = "gcloud-laptop"

# ------------------------------------------------------------------ sources (checked)
L171 = excerpt(README, 171, 171)
assert "an identity for your *code*, not for you" in L171
PH171 = "an identity for your code, not for you"
L175 = excerpt(README, 175, 175)
assert "**IAM & Admin → Service accounts**" in L175
L176 = excerpt(README, 176, 176)
SA_NAME = "mega-pipeline-sa"
assert f"`{SA_NAME}`" in L176
L177 = excerpt(README, 177, 177)
PH177 = "Grant it these roles"
assert PH177 in L177
ROLES = [  # (title, role id, tag, door index) in README order, README.md:178-181
    ("Storage Admin", "roles/storage.admin", "all five components", 0),
    ("Agent Platform User", "roles/aiplatform.user", "generate_text · Gemini", 2),
    ("Cloud Speech Client", "roles/speech.client", None, 1),
    ("Cloud Translation API User", "roles/cloudtranslate.user", None, 3),
]
for _k, (_t, _r, _g, _d) in enumerate(ROLES):
    _src = excerpt(README, 178 + _k, 178 + _k)
    assert f"**{_t}** (`{_r}`)" in _src, _src
assert API_DOORS[2] == "Vertex AI" and API_DOORS[4] == "Text-to-Speech"
L179 = excerpt(README, 179, 179)
assert 'Search the role picker for **"Agent Platform User"**' in L179
PH179 = "Search the role picker for Agent Platform User"
L46 = excerpt(GT_README, 46, 46)
assert "**Vertex AI User** role" in L46
L182 = excerpt(README, 182, 182)
assert "**Keys → Add Key → Create new key**" in L182 and "**JSON**" in L182
L183 = excerpt(README, 183, 183)
PH183 = "one level above this repo"
assert PH183 in L183 and "`mega-pipeline.json`" in L183
L185 = excerpt(README, 185, 185)
assert "**Text-to-Speech needs no role**" in L185
L189 = excerpt(README, 189, 189)
assert "go to **APIs & Services → Library**, search each name, and click **Enable**. Or do all five at once:" \
    in L189
README_CMDS = excerpt(README, 192, 198).split("\n")

# ------------------------------------------------------------------ captures
SET_BAD = capture("01", GL)                     # session: line 2 prompt + command, line 3 the error
assert SET_BAD.line(2).startswith(P_HOME + " ")
BAD_CMD = SET_BAD.typed(2)
assert BAD_CMD == README_CMDS[0] == "gcloud config set project <your-project-id>"
BAD_OUT = SET_BAD.line(3)
assert BAD_OUT.startswith("-bash: syntax error near unexpected token")
SET_OK = capture("02", GL)
assert SET_OK.cmd == "gcloud config set project your-project-id"
OK_OUT = SET_OK.line(2)
assert OK_OUT == "Updated property [core/project]."
ENABLE = capture("03", GL)
ENABLE_ROWS = [ENABLE.cmd] + ENABLE.at((2, 6))  # the README's six rows, as the capture typed them
assert ENABLE_ROWS == README_CMDS[1:7], ENABLE_ROWS
ERR7 = ENABLE.line(7)
assert ERR7.startswith("ERROR: (gcloud.services.enable) You do not currently have an active account")
assert len(ERR7) > 65                           # printed folded (see the docstring)
_k7 = ERR7.rfind(" ", 0, 66)
ERR7_ROWS = [ERR7[:_k7], ERR7[_k7 + 1:]]        # folded at the space before "active"
assert all(len(r) <= 65 for r in ERR7_ROWS) and ERR7_ROWS[1].startswith("active account selected")
REST7 = ENABLE.at(8, 9, 10, "…")
assert REST7[2] == "  $ gcloud auth login"
LIST_CMD = "gcloud services list --enabled"     # extra (ASSETS.md: a check, not a README step)

PONDER_Q = ("Key in place, every API enabled,\nbut you forgot the Agent Platform User role.\n"
            "Where does generate text fail:\ninside your container, or at Google?")

# ------------------------------------------------------------------ layout
X_L, X_R = -6.45, 6.42
Y_BAND = 3.21           # the top band, right of the tracker
TOP = 2.8               # top of the pictures under the tracker
K_THIRD = 0.8           # V3's scale as the door column in the right third (beats 3-4, 9)
K_FULL = 0.9            # V3's scale as the whole piece above the strip / the ponder card (7-9)
DOOR_DX = 0.32          # the door column moves right: room for the waiting token (widen_gap)


def at_left(m, x: float, y: float):
    return m.move_to([x + m.width / 2, y, 0])


def at_right(m, x: float, y: float):
    return m.move_to([x - m.width / 2, y, 0])


def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def glow(m, color: str = CLOUD, k: float = 1.3, run_time: float = 0.6):
    """m pulses and a filled `color` halo flashes on it: a BLUE glow on a BLUE outline (the lock
    slots), which Indicate alone cannot show."""
    h = box(m.width + 0.1, m.height + 0.1, color, fill_opacity=0.45, stroke=0, radius=0.08).move_to(m)
    return AnimationGroup(Indicate(m, color=color, scale_factor=k),
                          Succession(FadeIn(h, scale=0.7), FadeOut(h, scale=1.2)), run_time=run_time)


def pill(g, color: str = ERR, w: float = 0.17, h: float = 0.36, stroke: float = 2.5):
    """A narrow upright ring around one mono glyph (a circled `<`), inside its own character cell
    so it does not touch the neighbouring letters."""
    return RoundedRectangle(width=w, height=h, corner_radius=w / 2 - 0.005, stroke_color=color,
                            stroke_width=stroke).set_fill(opacity=0).move_to(g)


def widen_gap(v3, dx: float):
    """The door column (doors, padlocks, the may?/switched on? labels) moves right by dx and the
    token waits in the middle of the gap between the container and the lock column (common.py's
    waiting point leaves the token touching both, more so at 0.9, where the token keeps its size)."""
    for m in (v3.parts["doors"], v3.parts["gate2"], v3.parts["gate3"], *v3.locks.values()):
        m.shift(RIGHT * dx)
    x = (v3.container_frame.get_right()[0] + v3.doors[0].slot.get_left()[0]) / 2
    for d in v3.doors:
        d.stop.set_x(x)
    return v3


def crumb(*parts, size: float = TAG, colors=None):
    """A console breadcrumb: the parts joined by GREY '›'. .items (the parts, without the '›')."""
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


def id_chip(s: str):
    """A role's ID as a tight GREY mono chip (20 pt)."""
    t = mono(s, CAPTION, INK)
    b = box(t.width + 0.26, 0.4, S.GREY, fill_opacity=0.1, radius=0.12, stroke=2)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def role_item(title: str, rid: str, tag_s: str | None):
    """One granted role: the title (22 pt) and a GREY tag, its ID chip under it. .title .chip .tag"""
    tt = label(title, TAG, INK)
    head = VGroup(tt)
    tg = None
    if tag_s:
        tg = grey_tag(tag_s).next_to(tt, RIGHT, buff=0.25)
        head.add(tg)
    c = id_chip(rid).next_to(tt, DOWN, buff=0.1).align_to(tt, LEFT)
    g = VGroup(head, c)
    g.title, g.chip, g.tag = tt, c, tg
    return g


def sa_console():
    """Beats 3-4: the console's service-account pages (schematic, no logo).
    .win .ill .crumb (.items; the last, "Create service account", shown later) .form .value .btn
    .head (page 2: the name + "› Grant roles"; .name .rest) .items (four role_items)"""
    win = browser_window("console.cloud.google.com", width=8.0, height=6.1)
    win.move_to([X_L + 4.0, TOP - 3.05, 0])
    x0 = win.frame.get_left()[0] + 0.35
    y = win.frame.get_top()[1] - 0.55 - 0.42
    cr = crumb("IAM & Admin", "Service accounts", "Create service account", size=CAPTION,
               colors=[S.GREY, INK, INK])
    at_left(cr, x0, y)
    form = form_rows([("Service account name", "x")], width=7.2, size=CAPTION)
    at_left(form, x0, y - 0.75)
    fld = form.rows[0].field
    value = mono(SA_NAME, CAPTION, INK).move_to(fld).align_to(fld, LEFT).shift(RIGHT * 0.15)
    form.rows[0].remove(form.rows[0].value)
    btn = chip("Create and continue", CLOUD, size=CAPTION)
    at_left(btn, x0, y - 1.45)
    # page 2
    name2 = mono(SA_NAME, TAG, INK)
    rest = label("› Grant roles", TAG, INK)
    head = VGroup(name2, rest).arrange(RIGHT, buff=0.18)
    at_left(head, x0, y - 0.72)
    items = VGroup(*[role_item(t, r, g) for t, r, g, _ in ROLES])
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    items.move_to([x0 + items.width / 2, 0, 0])
    items.shift(UP * (head.get_bottom()[1] - 0.3 - items.get_top()[1]))
    ill = illustration_tag()
    ill.move_to(win.frame.get_corner(DOWN + RIGHT) + np.array([-ill.width / 2 - 0.3, 0, 0]))
    g = VGroup(win, cr, form, value, btn, head, items, ill)
    g.win, g.crumb, g.form, g.value, g.btn, g.head, g.items, g.ill = win, cr, form, value, btn, head, items, ill
    head.name, head.rest = name2, rest
    return g


def key_console():
    """Beat 5: the Keys page. .win .ill .ctx (IAM & Admin › Service accounts › mega-pipeline-sa)
    .path (Keys › Add Key › Create new key › JSON; .items) .btn .dl (download chip: .key .name)
    .dl_note"""
    win = browser_window("console.cloud.google.com", width=7.0, height=3.7)
    win.move_to([X_L + 3.5, 0.6, 0])
    x0 = win.frame.get_left()[0] + 0.35
    y = win.frame.get_top()[1] - 0.55 - 0.42
    ctx = crumb("Service accounts", mono(SA_NAME, CAPTION, INK), size=CAPTION, colors=[S.GREY, INK])
    at_left(ctx, x0, y)
    json_chip = chip("JSON", CLOUD, size=TAG)
    path = crumb("Keys", "Add Key", "Create new key", json_chip)
    at_left(path, x0, y - 0.68)
    btn = chip("Create", CLOUD, size=CAPTION)
    at_left(btn, x0, y - 1.38)
    k = key_glyph(0.3)
    nm = mono("<project>-<hex>.json", CAPTION, S.GREY)
    row = VGroup(k, nm).arrange(RIGHT, buff=0.2)
    fr = box(row.width + 0.5, 0.5, S.GREY, fill=S.BG, fill_opacity=1, radius=0.1)
    fr.move_to(row)
    dl = VGroup(fr, row)
    dl.key, dl.name, dl.frame = k, nm, fr
    at_left(dl, x0, win.frame.get_bottom()[1] + 0.6)          # clear of the illustration tag
    # under the window: beside the chip it would cross the window's right edge
    dl_note = note("the console picks a long name").next_to(win.frame, DOWN, buff=0.15).align_to(dl, LEFT)
    ill = illustration_tag()
    ill.move_to(win.frame.get_corner(DOWN + RIGHT) + np.array([-ill.width / 2 - 0.3, 0, 0]))
    g = VGroup(win, ctx, path, btn, ill)
    g.win, g.ctx, g.path, g.btn, g.dl, g.dl_note, g.ill = win, ctx, path, btn, dl, dl_note, ill
    return g


def small_tree():
    """S04's folder layout (README.md:107-117), small: <your-workspace>/, mega-pipeline/,
    secrets/, the dashed mega-pipeline.json. .header .ws .repo .sec .json .conns"""
    x0, pitch, ind = 1.15, 0.46, 0.5
    ws = file_row("<your-workspace>/", INK, LAPTOP)
    repo = file_row("mega-pipeline/", INK, LAPTOP)
    sec = file_row("secrets/", INK, LAPTOP)
    js = ghost_file("mega-pipeline.json")
    y0 = 1.75
    for i, (r, lvl) in enumerate([(ws, 0), (repo, 1), (sec, 1), (js, 2)]):
        r.shift(np.array([x0 + lvl * ind - r.glyph.get_left()[0], y0 - i * pitch - r.text.get_center()[1], 0]))
    conns = VGroup()
    for parent, kids in ((ws, (repo, sec)), (sec, (js,))):
        x = parent.glyph.get_center()[0]
        top = parent.glyph.get_bottom()[1] - 0.04
        bot = kids[-1].glyph.get_center()[1]
        conns.add(Line([x, top, 0], [x, bot, 0], color=S.GREY_DARK, stroke_width=2))
        for kd in kids:
            yk = kd.glyph.get_center()[1]
            conns.add(Line([x, yk, 0], [kd.glyph.get_left()[0] - 0.06, yk, 0], color=S.GREY_DARK,
                           stroke_width=2))
    header = VGroup(mono("README.md", CAPTION, S.GREY), label("· lines 107–117", CAPTION, S.GREY))
    header.arrange(RIGHT, buff=0.12)
    at_left(header, x0 - 0.05, y0 + 0.55)
    g = VGroup(header, conns, ws, repo, sec, js)
    g.header, g.ws, g.repo, g.sec, g.json, g.conns = header, ws, repo, sec, js, conns
    return g


def lib_console():
    """Beat 6: a tiny console Library page (illustration): APIs & Services › Library, a search
    field holding one of the five names, a BLUE Enable button. .win .ill"""
    win = browser_window("console.cloud.google.com", width=5.8, height=2.0)
    cr = crumb("APIs & Services", "Library", size=CAPTION)
    fld = box(2.35, 0.42, S.GREY_DARK, fill=TERM_BG, fill_opacity=1, radius=0.06, stroke=1.5)
    q = mono("Text-to-Speech", CAPTION, INK).move_to(fld).align_to(fld, LEFT).shift(RIGHT * 0.12)
    en = chip("Enable", CLOUD, size=CAPTION)
    row = VGroup(VGroup(fld, q), en).arrange(RIGHT, buff=0.3)
    body = VGroup(cr, row).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    body.move_to(win.content).align_to(win.content, LEFT).shift(RIGHT * 0.25)
    ill = illustration_tag()
    g = VGroup(win, body)
    ill.next_to(win.frame, DOWN, buff=0.08).align_to(win.frame, RIGHT)
    g.add(ill)
    g.win, g.ill, g.enable = win, ill, en
    return g


def zsh_chip():
    """The GREY caption chip: what macOS zsh prints instead (not a terminal line)."""
    a = label("macOS zsh says:", CAPTION, S.GREY)
    b = mono("zsh: parse error near `\\n'", CAPTION, INK)
    row = VGroup(a, b).arrange(RIGHT, buff=0.2)
    fr = box(row.width + 0.5, row.height + 0.3, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
    fr.move_to(row)
    return VGroup(fr, row)


def card_turn(rows, size: float = CAPTION):
    """The static GREY "your turn" card (common.turn_card's look) whose rows are mobjects
    (several lines each); the ▶ your turn tag on its top-right corner. .frame .rows .tag"""
    items = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    fr = box(items.width + 0.6, items.height + 0.6, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    items.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    h = note("your turn").next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
    tg = your_turn().move_to(fr.get_corner(UP + RIGHT)).shift(LEFT * 1.0)
    g = VGroup(fr, items, h, tg)
    g.frame, g.rows, g.tag = fr, items, tg
    return g


def mono_rows(lines, size: float = CAPTION, color: str = INK):
    """Mono lines one under the other, leading spaces kept (the README's continuation indent)."""
    rows = VGroup()
    pitch = line_pitch(size) * 0.9
    for i, s in enumerate(lines):
        ln = mono_line(s, size, color)
        ln.shift(np.array([-ln.strut.get_left()[0], -i * pitch - ln.strut.get_center()[1], 0]))
        rows.add(VGroup(*ln.glyphs))          # glyphs only: the group's left is the first letter
    return rows


def type_rows(scene, t, rows, type_time: float = 2.4):
    """Type a multi-line README command row by row at t's prompt, as the README writes it (each
    row but the last ends in ' \\'; continuation rows keep their two-space indent). Returns a
    VGroup of the rows (.rows)."""
    p = t.prompt + " "
    texts = [p + rows[0]] + list(rows[1:])
    assert all(len(s) <= t.max_chars for s in texts)
    t._make_room(scene, len(texts))
    lines = []
    for k, s in enumerate(texts):
        ln = mono_line(s, t.size, INK, t2c=t._prompt_colors(t.prompt) if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        lines.append(ln)
    scene.add(glyph_range(lines[0], 0, len(p)))
    typed = VGroup(*glyph_range(lines[0], len(p)), *[g for r in lines[1:] for g in glyph_range(r, 0)])
    scene.play(ShowIncreasingSubsets(typed, rate_func=linear), run_time=type_time)
    for r in lines:
        scene.add(r)
    g = VGroup(*lines)
    g.rows = lines
    return g


def fix_v3(tg):
    """After a rescale (shapes shrink, text keeps its size): the door names re-aligned inside
    their frames, the laptop's "secrets/" back beside its folder glyph and clear of the route."""
    for d in tg.doors:
        d.name.align_to(d.frame, LEFT).shift(RIGHT * 0.16)
    # the laptop's "secrets/" keeps its size while its folder glyph shrinks: put it back beside
    # the glyph, and keep it clear of the route's start
    (fg, fn), lap = tg.parts["laptop"][0], tg.parts["laptop"]
    fn.next_to(fg, RIGHT, buff=0.12)
    dx = tg.route.get_start()[0] - 0.12 - fn.get_right()[0]
    if dx < 0:
        lap.shift(RIGHT * dx)
    return tg


def small_v3_target(v3, k: float, right: float | None = None, center=None, top: float | None = None):
    """A target copy of V3 rescaled by k (fix_v3 applied), then moved: door frames' right edge at
    `right` and their column centred on center[1] (the right third), or the piece's centre at
    `center`, or its top at `top`."""
    tg = v3.generate_target()
    tg.rescale(k)
    fix_v3(tg)
    if right is not None:
        col = VGroup(*[d.frame for d in tg.doors])
        tg.shift(np.array([right - col.get_right()[0], center[1] - col.get_center()[1], 0]))
    elif center is not None:
        tg.move_to(center)
    if top is not None:
        tg.shift(UP * (top - tg.get_top()[1]))
    return tg


def door_tick(v3, i: int):
    """A white tick right of door i's switch (smaller than common's, for the 0.9 piece)."""
    return check_mark(0.22, INK).next_to(v3.doors[i].toggle, RIGHT, buff=0.06)


class ThreeGates(VoiceScene):
    def construct(self):
        tr = tracker("K", 1)

        v3 = ThreeGatesPiece(show=("container",))
        v3.parts["gate2"].shift(LEFT * 0.1)            # room between "may?" and "switched on?" at 0.8
        v3.parts["gate3"].shift(RIGHT * 0.15)
        widen_gap(v3, DOOR_DX)
        v3.shift(DOWN * 0.05)

        # ========================================================== 0 · identity: account + key
        card171 = readme_card("README.md · line 171", [f"“{PH171}”"])
        at_right(card171, X_R, 0)
        card171.shift(UP * (3.08 - card171.frame.get_top()[1]))
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(v3), run_time=0.8)
            self.wait(0.4)
            v3.reveal(self, "laptop", run_time=0.6)
            v3.reveal(self, "route", anim=Create, run_time=0.7)
            vo.wait_until("For code")
            self.play(FadeIn(card171, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("with one JSON key")
            self.play(flash(v3.key, KEY, 1.4, 0.6))
            self.play(v3.pulse(run_time=1.0))

        # ========================================================== 1 · token; five doors
        short = note("short-lived")
        with self.voiceover(SAY[1]) as vo:
            self.wait(0.3)
            self.play(*v3.mint(run_time=1.1))
            short.next_to(v3.container_frame, DOWN, buff=0.15).set_x(v3.token.get_center()[0])
            self.play(FadeIn(short, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("and every call")
            self.play(*v3.parts_in("doors"), FadeOut(card171), run_time=0.8)
            self.play(v3.fly(2, run_time=1.0), FadeOut(short), run_time=1.0)

        # ========================================================== 2 · gates 1, 2, 3
        v3.key.save_state()
        with self.voiceover(SAY[2]) as vo:
            self.play(*v3.parts_in("gate1", anim=Write), run_time=0.6)
            self.play(flash(v3.slot, TURN, 1.15, 0.8), v3.home(run_time=0.8))
            vo.wait_until("without the key")
            chips1, anims = v3.fail_gate1()
            self.play(v3.key.animate.set_opacity(0.15), *v3.parts_out("token"), run_time=0.5)
            self.play(*anims)
            vo.wait_until("Gate 2 asks")
            self.play(FadeOut(chips1), Restore(v3.key), run_time=0.5)
            self.play(v3.pulse(run_time=0.8), *v3.parts_in("gate2", anim=Write), run_time=0.8)
            vo.wait_until("the account needs a role")
            self.play(LaggedStart(*[glow(d.slot, CLOUD, 1.3, 0.6) for d in v3.doors if d.slot is not None],
                                  lag_ratio=0.2), run_time=1.1)
            vo.wait_until("Gate 3 asks")
            self.play(*v3.parts_in("gate3", anim=Write), run_time=0.6)
            vo.wait_until("if the API")
            self.play(LaggedStart(*[flash(d.toggle, CLOUD, 1.3, 0.6) for d in v3.doors], lag_ratio=0.2),
                      run_time=1.2)

        # ========================================================== 3 · console: account + four roles
        con = sa_console()
        crumb3 = con.crumb.items[2]
        crumb3_sep = con.crumb[3]                 # the '›' before it
        chip177 = readme_chip("README.md · lines 177–181", PH177)
        at_right(chip177, X_R, Y_BAND)
        y_doors = -0.15
        with self.voiceover(SAY[3]) as vo:
            self.play(*v3.parts_out("laptop", "route", "container", "ghost", "gate1"), run_time=0.5)
            small_v3_target(v3, K_THIRD, right=6.35, center=(0, y_doors))
            self.play(MoveToTarget(v3), run_time=0.9)
            self.play(FadeIn(con.win), FadeIn(con.ill),
                      *[FadeIn(m) for m in con.crumb if m not in (crumb3, crumb3_sep)], run_time=0.6)
            vo.wait_until("create a service account")
            self.play(FadeIn(VGroup(crumb3_sep, crumb3), shift=LEFT * 0.15), FadeIn(con.form), FadeIn(con.btn),
                      run_time=0.6)
            vo.wait_until("for example")
            self.play(ShowIncreasingSubsets(con.value, rate_func=linear), run_time=0.8)
            self.add(con.value)
            self.play(flash(con.btn, CLOUD, 1.1, 0.6))
            vo.wait_until("Grant it four roles")
            con.value.set_z_index(2)              # it travels above the fading form field
            self.play(tr.goto(2), FadeIn(chip177, shift=DOWN * 0.1),
                      FadeOut(VGroup(con.form, con.btn)),
                      con.value.animate.move_to(con.head.name).set_color(INK),
                      run_time=0.7)
            self.remove(con.value)
            self.add(con.head.name)
            self.play(FadeIn(con.head.rest, shift=LEFT * 0.15), run_time=0.4)
            for k, anchor in enumerate(("Storage Admin for every", "Agent Platform User for",
                                        "Cloud Speech Client", "and Cloud Translation")):
                vo.wait_until(anchor)
                it = con.items[k]
                door = ROLES[k][3]
                src = np.array([it.chip.get_right()[0] + 0.25, it.chip.get_center()[1], 0])
                self.play(FadeIn(it, shift=RIGHT * 0.15), run_time=0.5)
                self.play(v3.fill_lock(door, src=src, run_time=0.8))

        # ========================================================== 4 · no role for TTS; the slip
        tts = v3.doors[4]
        no185 = VGroup(note("no role needed"), note("README.md line 185")).arrange(DOWN, aligned_edge=RIGHT,
                                                                                  buff=0.08)
        card46 = readme_card("generate_text/README.md · line 46", ["“Vertex AI User”"])
        card179 = readme_card("README.md · line 179", [f"“{PH179}”"])
        err46 = erratum_tag()
        at_left(card46, X_L + 0.05, 0)
        card46.shift(UP * (0.95 - card46.frame.get_center()[1]))
        err46.next_to(card46.frame, RIGHT, buff=0.3)
        at_left(card179, X_L + 0.05, 0)
        card179.shift(UP * (-0.65 - card179.frame.get_center()[1]))
        ok179 = check_mark(0.34, VENV).next_to(card179.frame, RIGHT, buff=0.25)
        st46 = strike(card46.rows[0], ERR)
        with self.voiceover(SAY[4]) as vo:
            no185.next_to(VGroup(*[d.frame for d in v3.doors]), DOWN, buff=0.3)
            no185.align_to(tts.frame, RIGHT)
            self.play(flash(tts.slot if tts.slot is not None else tts[4], S.WHITE, 1.3, 0.7),
                      FadeIn(no185, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("A small slip")
            self.play(FadeOut(VGroup(con.win, con.ill, con.crumb, con.head, con.items), shift=LEFT * 0.3),
                      run_time=0.5)
            self.play(FadeIn(card46, shift=UP * 0.1), FadeIn(err46), run_time=0.6)
            vo.wait_until("still says Vertex AI User")
            self.play(flash(card46.rows[0], TURN, 1.08, 0.7))
            vo.wait_until("which finds nothing now")
            self.play(Create(st46), card46.rows[0].animate.set_color(ERR), run_time=0.5)
            self.play(FadeIn(card179, shift=UP * 0.1), run_time=0.5)
            self.play(Create(ok179), run_time=0.4)

        # ========================================================== 5 · JSON key -> secrets/
        kc = key_console()
        tree = small_tree()
        tree.shift(RIGHT * 9.0)
        tree_x = 9.0
        chip183 = readme_chip("README.md · line 183", PH183)
        at_right(chip183, X_R, Y_BAND)
        newname = mono("mega-pipeline.json", CAPTION, INK).move_to(kc.dl.name, aligned_edge=LEFT)
        pay1 = cost_tag("whoever holds this file spends your project's money")
        pay2 = cost_tag("never commit it · never paste it")
        pays = VGroup(pay1, pay2).arrange(DOWN, buff=0.2)
        pays.move_to([0, -2.35, 0])
        with self.voiceover(SAY[5]) as vo:
            self.play(tr.goto(3), FadeOut(VGroup(card46, err46, st46, card179, ok179, no185, chip177)),
                      FadeOut(v3), run_time=0.6)
            self.play(FadeIn(VGroup(kc.win, kc.ill, kc.ctx)), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(m, shift=LEFT * 0.1) for m in kc.path], lag_ratio=0.25),
                      run_time=1.2)
            vo.wait_until("it arrives with")
            self.play(FadeIn(kc.btn), run_time=0.3)
            self.play(flash(kc.btn, CLOUD, 1.1, 0.5))
            self.play(FadeIn(kc.dl, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(kc.dl_note), flash(kc.dl.name, S.WHITE, 1.08, 0.6), run_time=0.6)
            vo.wait_until("Rename it")
            self.play(tr.goto(4), tree.animate.shift(LEFT * tree_x), FadeOut(kc.dl_note), run_time=0.8)
            self.play(Transform(kc.dl.name, newname), run_time=0.7)
            vo.wait_until("in the secrets folder")
            solid = file_row("mega-pipeline.json", INK, LAPTOP)
            solid.shift(tree.json.glyph.get_center() - solid.glyph.get_center())
            key_end = key_glyph(0.3).next_to(solid.text, RIGHT, buff=0.25)
            flyer = kc.dl.key                     # the file leaves the browser (no copy)
            self.play(flyer.animate.move_to(key_end), FadeIn(chip183, shift=DOWN * 0.1), run_time=1.0)
            self.play(FadeTransform(tree.json, solid), flash(tree.sec, KEY, 1.1, 0.6), run_time=0.6)
            vo.wait_until("Whoever holds it")
            self.play(FadeIn(pay1, shift=UP * 0.15), flash(flyer, KEY, 1.4, 0.6), run_time=0.6)
            vo.wait_until("never commit or paste")
            self.play(FadeIn(pay2, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 6 · set project: the brackets
        card189 = readme_card("README.md · lines 187–189",
                              ["“go to APIs & Services → Library,", "search each name, and click Enable.",
                               "Or do all five at once:”"])
        at_left(card189, X_L + 0.05, 0)
        card189.shift(UP * (2.45 - card189.frame.get_top()[1]))
        lib = lib_console()
        at_right(lib, X_R, 0)
        lib.shift(UP * (3.45 - lib.win.frame.get_top()[1]))   # its tag clear of the 8-row terminal
        t = term(P_HOME, rows=8, title="laptop")
        zsh = zsh_chip()
        at_right(zsh, X_R, 0)
        zsh.shift(UP * (t.box.get_top()[1] + 0.35 + zsh.height / 2 - zsh.get_center()[1]))
        with self.voiceover(SAY[6]) as vo:
            self.play(tr.goto(5), FadeOut(VGroup(kc, kc.dl, tree.header, tree.conns, tree.ws, tree.repo, tree.sec, solid,
                                                  chip183, pays)),
                      run_time=0.6)
            self.play(FadeIn(card189, shift=DOWN * 0.1), FadeIn(lib), run_time=0.7)
            self.play(flash(lib.enable, CLOUD, 1.15, 0.6))
            vo.wait_until("or with gcloud")
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Typed exactly as written")
            self.play(FadeOut(card189), FadeOut(lib), run_time=0.4)
            bad = type_cmd(self, t, BAD_CMD, type_time=1.6)
            vo.wait_until("the set project command fails")
            err6 = t.print(self, [(BAD_OUT, ERR)], run_time=0.4)[0]
            vo.wait_until("the shell reads")
            lt, gt = substring(bad, "<"), substring(bad, ">")
            rings = VGroup(pill(lt), pill(gt))
            redir = grey_tag("the shell: redirection")
            redir.move_to([VGroup(lt, gt).get_center()[0], err6.strut.get_center()[1] - t.pitch, 0])
            self.play(Create(rings), lt.animate.set_color(ERR), gt.animate.set_color(ERR), run_time=0.6)
            self.play(FadeIn(redir, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("as redirections")
            self.play(FadeIn(zsh, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Type your own project ID")
            self.play(FadeOut(redir), run_time=0.2)
            ok = type_cmd(self, t, SET_OK.cmd, type_time=1.0)
            t.print(self, [OK_OUT], run_time=0.3)
            pid = substring(ok, VALUES["gcp_project"])
            pbox = ring(pid, TURN, buff=0.05)
            own = tag("your own ID", TURN)
            own.move_to([pid.get_center()[0], t.lines[-1].strut.get_center()[1] - 0.05, 0])
            self.play(Create(pbox), FadeIn(own, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 7 · services enable
        listc = cmd_chip(LIST_CMD, "with your account: lists the five")
        x_list = extra_tag().next_to(listc.chip, RIGHT, buff=0.25)
        list_grp = VGroup(listc, x_list)
        at_right(list_grp, X_R, 0)
        list_grp.shift(UP * (Y_BAND + 0.04 - listc.chip.get_center()[1]))
        with self.voiceover(SAY[7]) as vo:
            self.wait(0.6)                         # "your own ID" stays a moment into this block
            self.play(tr.goto(6), FadeOut(zsh), FadeOut(VGroup(rings, pbox, own)), run_time=0.4)
            t.clear(self, run_time=0.3)
            resize(self, t, 12, run_time=0.6)
            type_rows(self, t, ENABLE_ROWS, type_time=2.3)
            vo.wait_until("Our laptop had no Google account")
            e7 = t.print(self, [(r, ERR) for r in ERR7_ROWS], run_time=0.5)
            rest = t.print(self, REST7, run_time=0.5)
            vo.wait_until("so gcloud says")
            u1 = under(glyph_range(e7[0], e7[0].text.index("You")), TURN)
            u2 = under(glyph_range(e7[1], 0, e7[1].text.index("selected") + len("selected")), TURN)
            self.play(Create(u1), Create(u2), run_time=0.6)
            e7[0].add(u1)
            e7[1].add(u2)
            vo.wait_until("that's the login step")
            ln10 = rest[2]
            tut0 = note("Tutorial 0: gcloud auth login")
            beside(tut0, t, ln10, buff=0.5)
            pin(self, ln10, tut0, run_time=0.5)
            self.play(flash(substring(ln10, "gcloud auth login"), TURN, 1.1, 0.7))
            vo.wait_until("Logged in, it enables them")
            # V3 comes back full (at 0.8) above the strip, every part but the waiting token's place
            for name in ("laptop", "route", "container", "ghost", "token", "gate1"):
                v3.parts_in(name)                 # visible again when the piece fades in
            fix_v3(v3.rescale(K_FULL / K_THIRD))  # off screen: the whole piece at 0.9
            v3.move_to([0, 0.75, 0])
            v3.shift(UP * (2.42 - v3.get_top()[1]))
            ill7 = illustration_tag("with your account")
            resize(self, t, 3, keep=[e7[0], e7[1], ln10], run_time=0.6,
                   extra=(FadeIn(list_grp, shift=DOWN * 0.1),))
            ill7.move_to([v3.container_frame.get_center()[0], (v3.get_bottom()[1] + STRIP_TOP) / 2, 0])
            self.play(FadeIn(v3), FadeIn(ill7), run_time=0.5)
            self.play(LaggedStart(*[v3.switch(i, run_time=0.4) for i in range(5)], lag_ratio=0.5),
                      run_time=1.1)
            vo.wait_until("and calls bill your project")
            bill = cost_tag("calls now bill your project")
            col = VGroup(*[d.frame for d in v3.doors])
            bill.move_to([col.get_center()[0], (v3.get_bottom()[1] + STRIP_TOP) / 2, 0])
            bill.shift(LEFT * max(0.0, bill.get_right()[0] - X_R))
            self.play(FadeIn(bill, shift=DOWN * 0.3), run_time=0.6)

        # ========================================================== 8 · ponder: the forgotten role
        gt_chip = chip("generate_text", CTR, size=CAPTION, font=MONO, fill_opacity=0.1)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(t), FadeOut(VGroup(list_grp, ill7, bill)), run_time=0.5)
            self.play(v3.animate.shift(UP * (2.98 - v3.get_top()[1]) + RIGHT * (-6.4 - v3.get_left()[0])),
                      run_time=0.7)
            vo.wait_until("Your key is in place")
            tick1 = v3.tick("gate1")
            self.play(flash(v3.ghost, KEY, 1.3, 0.6), Create(tick1), run_time=0.6)
            vo.wait_until("and every API is enabled")
            ticks = VGroup(*[door_tick(v3, i) for i in range(5)])
            self.play(LaggedStart(*[Create(m) for m in ticks], lag_ratio=0.25), run_time=1.0)
            vo.wait_until("but you forgot")
            self.play(*v3.parts_out("lock2"), run_time=0.6)
            self.play(flash(v3.doors[2].slot, TURN, 1.3, 0.7))
            vo.wait_until("Where does generate text fail")
            gt_chip.next_to(v3.container_frame, DOWN, buff=0.3)
            self.play(FadeIn(gt_chip, shift=UP * 0.15), run_time=0.5)
            # the two options get the same emphasis (the picture must not answer)
            vo.wait_until("inside your container")
            self.play(flash(v3.container_frame, CTR, 1.03, 0.8))
            vo.wait_until("or at Google")
            self.play(flash(VGroup(*[d.frame for d in v3.doors]), CLOUD, 1.03, 0.8))

        q = ponder_card(PONDER_Q, width=X_R - (gt_chip.get_right()[0] + 0.3), size=22)
        q.move_to([X_R - q.width / 2, -3.45 + q.height / 2, 0])
        assert q.get_top()[1] < v3.get_bottom()[1] - 0.05, (q.get_top()[1], v3.get_bottom()[1])
        assert q[2].width >= ponder_card(PONDER_Q, width=30, size=22)[2].width * 20 / 22 - 1e-6   # >= 20 pt
        self.play(FadeIn(q, scale=0.95), run_time=0.6)
        bar = q[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 9 · at Google; your turn
        said = note("said, not shown: nothing here reached Google")
        cap9_s = "the key says who · the role says may"     # one Text: one baseline
        caption9 = label(cap9_s, TAG, INK, t2c={"who": KEY, "·": S.GREY, "may": CLOUD})
        assert len(caption9.submobjects) == len(cap9_s.replace(" ", ""))
        n9 = len("the key says who ·".replace(" ", ""))
        mins = VGroup(note("new roles and APIs:"), note("allow a few minutes")).arrange(DOWN, aligned_edge=RIGHT,
                                                                                     buff=0.08)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(q), run_time=0.4)
            self.play(flash(tick1, S.WHITE, 1.4, 0.5), v3.fly(2, run_time=0.9), run_time=0.9)
            perm, banims = v3.bounce(2)
            self.play(*banims)
            self.play(v3.home(run_time=0.6))
            said.next_to(perm, DOWN, buff=0.12).align_to(perm, RIGHT)
            self.play(FadeIn(said), run_time=0.4)
            vo.wait_until("The key proved who you are")
            at_left(caption9, -6.3, -2.0)
            self.play(FadeIn(caption9[:n9], shift=UP * 0.1), flash(v3.ghost, KEY, 1.3, 0.6), run_time=0.6)
            vo.wait_until("the role decides")
            self.play(FadeIn(caption9[n9:], shift=UP * 0.1),
                      flash(VGroup(*[v3.locks[i] for i in (0, 1, 3)]), CLOUD, 1.2, 0.6), run_time=0.6)
            vo.wait_until("New roles and APIs")
            at_right(mins, 6.35, -2.3)                # under the door column's place in the right third
            self.play(FadeIn(mins, shift=UP * 0.1), flash(VGroup(*[d.toggle for d in v3.doors]), CLOUD, 1.1, 0.6),
                      run_time=0.6)
            self.wait(0.5)
            # the picture makes room for the your-turn card before "Pause"
            self.play(FadeOut(VGroup(perm, said, caption9, gt_chip, tick1, ticks)),
                      *v3.parts_out("laptop", "route", "container", "ghost", "token", "gate1"), run_time=0.5)
            small_v3_target(v3, K_THIRD / K_FULL, right=6.35, center=(0, y_doors))
            self.play(MoveToTarget(v3), run_time=0.8)
            card = card_turn([
                label("IAM & Admin › Service accounts › Create · 4 roles", CAPTION, INK),
                label("Keys › Add Key › Create new key › JSON", CAPTION, INK),
                VGroup(label("save as", CAPTION, INK), mono("secrets/mega-pipeline.json", CAPTION, INK),
                       note("beside the repo")).arrange(RIGHT, buff=0.15),
                VGroup(mono(BAD_CMD, CAPTION, INK), note("your ID, no brackets")).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.08),
                mono_rows(ENABLE_ROWS),
            ])
            at_left(card, X_L + 0.05, 0)
            card.shift(UP * (y_doors - card.frame.get_center()[1]))
            assert card.get_right()[0] < v3.doors[4][4].get_left()[0] - 0.2      # clear of "no role"
            self.play(v3.fill_lock(2, run_time=0.6), FadeIn(card, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Pause, and set up")
            self.play(Wiggle(card.tag, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)
        self.wait(0.8)
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)

