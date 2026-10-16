"""S12 · Tag and push (README B1-B4; V6 names and the registry; the local-registry stand-in).

Beats (script.md "## S12", one voiceover block each):
 0  S11 ended on an empty frame: TRACKER A16 fades in, then the README card `README.md · line 186` with the
    section heading (34 pt, as S14's line 203); "Pushing Docker Image to Docker Hub": the heading becomes the
    new tracker's section name (4 dots) and pulses; "First, sign up": B1 and the README card (`README.md · line 188`, "Sign up in
    Docker Hub and create an Access Token", the link underlined). A schematic browser window (tag
    `illustration`, address = the README's link): "Docker Hub · account settings", "Personal access
    tokens" with a BLUE button "Generate new token" (pulses); "with read and write": the row "Access
    permissions:" with a YELLOW "Repo Read & Write"; "not the default": GREY note "default: Repo Public
    Read-only · can't push". "Copy it right away": the token field `<ACCESS TOKEN>` with a lock glyph
    and the GREY note "copy it now: shown only once"; "it works like a password": the lock pulses and
    a GREY note "a token is a password: / never in a file, never in a repo" sits right of the card.
    "Pause": ▶ your turn beside the token field.
 1  TRACKER B2. The page goes; the README card becomes line 189 ("Login to the Hub:" / the command in
    mono, 24 pt; CODE(README.md: 189) at >= 20 pt is the card: line 190 would be 16 units wide).
    "dash u": `<USER NAME>` boxed YELLOW, "dash p": `<ACCESS TOKEN>` boxed YELLOW, "yours" under each.
    "We have no account": GREY note "no Docker Hub account in our recording · not run here".
 2  TRACKER B2 · extra. The card moves to the top; an 8-row laptop terminal fades in with
    `stand_in_tag()` on its frame and its prompt waiting (the tag's "watch only" line pulses on "just
    watch those"). "Logging in to
    it": `docker login localhost:5000 -u student -p not-a-real-token` (laptop-push/05's own command;
    folds) -> laptop-push/05: 2 (wrapped: it is 72 characters), 8. Line 2 gets a YELLOW bar on "warns",
    `Login Succeeded` turns GREEN.
 3  TRACKER B2. The terminal goes. A GREY card `~/.bash_history` (tag `illustration`) with two earlier
    commands; the card's command flies down into it as its third line; "with dash p": `-p <ACCESS
    TOKEN>` turns RED, tag `erratum` beside it. "Instead": a GREEN chip `docker login -u <USER NAME>`;
    "then paste": a GREY prompt row `Password:` with a clipboard glyph that drops into the empty field
    (its outline flashes; "paste your token · nothing shows"). "Pause and log in": ▶ your turn beside the chip, GREY note "or the
    README's form".
 4  TRACKER B3. The card becomes line 190 (top) with the YELLOW caption "<USER NAME> = your Docker Hub
    username (here: student)". A 7-row laptop terminal types `docker tag simple-translate
    student/simple-translate-ac215` (laptop/43; folds) -> no output; `student` lights YELLOW with the
    caption. "Pause": ▶ your turn. "An extra image ls": B3 · extra, `docker image ls` (row tag `extra`)
    -> laptop/44: 2, 4–5 with cols IMAGE, ID, DISK USAGE (squeezed it is 77 characters: too wide even
    for the wide terminal; GREY caption "columns: IMAGE · ID · DISK USAGE" on the frame; row 3 never
    printed). "two names": both names underline TEAL; "one ID": both `b5c531a6b555` turn TEAL in TEAL
    boxes; "a second name": TEAL row tag "same ID · a second name, not a copy" on the returned prompt
    row, under the IDs (no room for a bracket: DISK USAGE sits right of the IDs).
 5  TRACKER B3. V6: the two names fly up out of the terminal into two TEAL sticky notes, the ID into
    the TEAL label under a TEAL stack (7 unlabelled slabs, fills as V2) that fades in where the card was
    (the card goes first; the terminal fades as the names leave it). "Read the long name": the long
    note's letters fly down into the unfolded name while the notes link to the stack (24 pt TEAL, separators GREY); "the registry": `docker.io` slides in with its
    caption "registry · the default"; then "account", "repository", "tag" as said, each part pulsing.
    "Names without an account": a GREY chip `docker.io/library/simple-translate:latest` grows out of
    the short note (letter by letter), GREY "as in the build log · no account → library";
    `library` turns YELLOW on "fall under library".
 6  TRACKER B4. The parts and the chip go; the long note's repository name flies into the title of a
    BLUE shelf "Docker Hub" / `student/simple-translate-ac215` (door on its left) at the right, a PINK
    route from the stack. README card line 191 at the bottom; "Pause and run it": ▶ your turn. "Yours
    should upload each layer": GREY "missing? → upload" at the door; the seven slabs lift off one by
    one along the route and queue at the door; "and end with a digest line": GREEN note "logged in:
    Pushed … latest: digest: … (next)". "Without an account": the card and notes go, the picture parks
    in the top-right corner (no text), a 12-row laptop terminal types `docker push
    student/simple-translate-ac215` -> laptop-push/03: 2–8 (wrap), line 8 RED; "push access denied":
    line 8 pulses RED and the corner shelf's door shuts RED; row tags "real capture · 2026-10-13" and
    "what we got · no Docker Hub account" beside line 8. "If you see it": the terminal shrinks to the
    strip (line 8's three rows) while the picture grows back (door shut, RED cross); "log in": GREY
    "if you see this:" + YELLOW chip "log in", and the GREEN note returns under the shelf; "and check
    your token": chip "a token that can write" while the queue slides back into the stack; "and the
    name starts": chip "the name must start with YOUR username".
 7  TRACKER B4 · extra. The strip clears while the Docker Hub shelf gives way to a dashed BLUE shelf
    "stand-in registry" / `localhost:5000`, then grows to 6 rows (the folded push command and its four
    output lines fit together) with `stand_in_tag()` on its frame. Types `docker tag simple-translate
    localhost:5000/student/simple-translate-ac215` (laptop-push/06; folds) -> no output, `docker push
    localhost:5000/student/simple-translate-ac215` (laptop-push/07; folds) -> laptop-push/07: 3–4, …, 15
    (hash12; line 3 is cut at the terminal edge); the tag's rows scroll off fading in place (local
    scroll(): no drift over the picture). The seven slabs travel the route through the open door onto
    the shelf while the output prints and the digest underlines TEAL (one play: the push goes through as
    it is said); "a fingerprint": a TEAL fingerprint badge "digest" appears on the shelf (it stays through
    beat 8: same digest). (The narration is 5.7 s; the typing is quick so that the digest line is printed
    as "digest" is said.)
 8  The strip clears ("Push again"); the same push -> laptop-push/08: 4, …, 14–15 (hash12). "every layer
    already exists": each
    slab rides to the door and bounces back; GREY "already exists" by the door, the two rows underline
    TEAL, GREY note "only missing layers travel" (pulses as said). "On Docker Hub": the strip shrinks
    to 3 rows; the
    stand-in shelf gives way to a BLUE "Docker Hub" shelf with an ORANGE `python` stack on its board
    (tag `illustration`); the four ORANGE base slabs get GREY links to it; GREY caption "already on
    Docker Hub · from the official python image" (the message itself is said, never printed);
    "it already has them": the python stack pulses.
 9  TRACKER B4. Everything else goes. A schematic repository card (tag `illustration`) `student/
    simple-translate-ac215`; the image moves down, then into it (never across its text); "is public
    by default": a BLUE badge "public", and a `.git/` glyph appears on a lead from the COPY slab;
    "Anyone can pull it": three GREY figures pull it along PINK routes; "git folder and all": `.git/`
    and the COPY slab's outline turn RED and pulse, and S10's `.dockerignore` card (`.git`, `.venv`,
    `secrets/`, tag "illustration · a file you'd add" above it, as in S10 and S11) fades in where the image
    stood (raised: the tag runs over the repository card's x-range, so it sits clear above that card's
    top), its `.git` line flashing GREEN.
    Fade to an empty frame.
"""

import re  # noqa: I001  (manim first, then common: common must win)

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.devops import MONO, OUTPUT, browser_window, cross_mark, folder_glyph
from explainer.scene import VoiceScene

from common import (CLOUD, DOCKER_PUSH, DOCKER_TAG, ERR, IMAGE, IMAGE_LS, INK, LAPTOP, LAPTOP_DIR,
                    LOGIN_README, NARRATION, PUSH_DIR, PUSH_README, SECTION_B, STRIP_ROWS, SYSTEM, TAG_README, TURN,
                    VENV, LayerStack, RegistryShelf, attach, bare_prompt, beside, box, capture, chip, cols,
                    erratum_tag, excerpt, fingerprint, hash12, illustration_tag, label, laptop_term,
                    lock_glyph, mono, mono_line, name_parts, pin, readme_card, resize, route, row_tag,
                    stand_in_tag, sticky, substring, track, tracker_a, tracker_b, type_cmd, under,
                    user_caption, your_turn)

SAY = NARRATION["S12"]

# ------------------------------------------------------------------ the README lines (assets/source/README.md)
_BULLET = re.compile(r"^\* (.*?:) `(.*)`$")


def _bullet(n: int) -> tuple[str, str]:
    m = _BULLET.match(excerpt("README.md", n, n))
    assert m, excerpt("README.md", n, n)
    return m.group(1), m.group(2)


assert excerpt("README.md", 186, 186).endswith(SECTION_B), excerpt("README.md", 186, 186)   # the section heading
L188 = excerpt("README.md", 188, 188)
assert L188.startswith("* Sign up in Docker Hub and create an [Access Token](https://"), L188
TOKEN_URL = re.search(r"\]\(https://([^)]+)\)", L188).group(1)          # hub.docker.com/settings/security
LOGIN_WORDS, _c = _bullet(189)
assert (LOGIN_WORDS, _c) == ("Login to the Hub:", LOGIN_README), _c
TAG_WORDS, _c = _bullet(190)
assert (TAG_WORDS, _c) == ("Tag the Docker Image:", TAG_README), _c
PUSH_WORDS, _c = _bullet(191)
assert (PUSH_WORDS, _c) == ("Push to Docker Hub:", PUSH_README), _c

# ------------------------------------------------------------------ real outputs (file line numbers)
C05 = capture("05", PUSH_DIR)                         # laptop-push/05-login-local.txt
LOGIN_LOCAL = C05.cmd
assert LOGIN_LOCAL == "docker login localhost:5000 -u student -p not-a-real-token", LOGIN_LOCAL
OUT05 = C05.at(2, 8)
assert OUT05[0].startswith("WARNING! Using --password via the CLI is insecure") and OUT05[1] == "Login Succeeded"

C43 = capture("43", LAPTOP_DIR)                       # laptop/43-tag.txt: no output
assert C43.cmd == DOCKER_TAG and C43.lines == [] and C43.exit == 0, C43.raw

C44 = capture("44", LAPTOP_DIR)                       # laptop/44-image-ls-tagged.txt
assert C44.cmd == IMAGE_LS, C44.cmd
LS44 = cols(C44.at(2, 4, 5), ["IMAGE", "ID", "DISK USAGE"])          # row 3 never printed
assert LS44[1].startswith("simple-translate:latest") and LS44[2].startswith("student/simple-translate-ac215:latest")
ID = "b5c531a6b555"
assert all(ID in s for s in LS44[1:]) and max(len(s) for s in LS44) <= 65, LS44

C03 = capture("03", PUSH_DIR)                         # laptop-push/03-push-no-login.txt
assert C03.cmd == DOCKER_PUSH and C03.exit == 1, C03.cmd
OUT03 = C03.at((2, 8))
assert OUT03[-1].startswith("push access denied") and OUT03[2].endswith(": Waiting"), OUT03

C06 = capture("06", PUSH_DIR)                         # laptop-push/06-tag-local.txt: no output
TAG_LOCAL = C06.cmd
assert TAG_LOCAL == "docker tag simple-translate localhost:5000/student/simple-translate-ac215" and C06.lines == []

C07 = capture("07", PUSH_DIR)                         # laptop-push/07-push-local.txt
PUSH_LOCAL = C07.cmd
assert PUSH_LOCAL == "docker push localhost:5000/student/simple-translate-ac215", PUSH_LOCAL
OUT07 = [hash12(s) for s in C07.at(3, 4, "…", 15)]
assert OUT07[1].endswith(": Pushed") and OUT07[3].startswith("latest: digest: sha256:2c302ec4c536…"), OUT07

C08 = capture("08", PUSH_DIR)                         # laptop-push/08-push-local-again.txt
assert C08.cmd == PUSH_LOCAL, C08.cmd
OUT08 = [hash12(s) for s in C08.at(4, "…", (14, 15))]
assert OUT08[0].endswith("Layer already exists") and OUT08[3] == OUT07[3], OUT08

LIBRARY = "docker.io/library/simple-translate:latest"   # every build log: laptop/29 line 22
assert f"naming to {LIBRARY}" in capture("29", LAPTOP_DIR).line(22)
LONG = "student/simple-translate-ac215:latest"
SHORT = "simple-translate:latest"
REPO = "student/simple-translate-ac215"
HISTORY = ["docker build -t simple-translate -f Dockerfile .", "docker run --rm -ti simple-translate"]

# ------------------------------------------------------------------ layout
STACK_X, FLOOR = -4.9, 0.35         # V6: the image (beats 5-8), floor of its lowest slab
STACK_W = 2.2
H_STACK = [0.1] * 4 + [0.3, 0.3, 0.5]
FILLS = [SYSTEM] * 5 + [LAPTOP, VENV]
SHELF_C = np.array([3.2, 1.08, 0])  # the registry shelf's frame centre (beats 6-8)
SHELF_W, SHELF_H = 4.4, 1.46
THUMB_C, THUMB_W = np.array([4.35, 3.05, 0]), 3.8    # the parked picture (beat 6, over a 12-row terminal)
PARCEL_W = 0.8
STAND_ROWS = 6                      # the stand-in strip (beats 7-8): a folded push command + its 4 output lines


# ------------------------------------------------------------------ builders
def card_line(n: int, words: str, cmd: str, size: float = 22, cmd_size: float = 24) -> VGroup:
    """README card for a bullet 'words `cmd`' (README.md line n): the words, then the command (mono) on
    its own line. .cmd (a mono_line)."""
    cmd_line = mono_line(cmd, cmd_size, INK)
    body = VGroup(label(words, size, INK), cmd_line).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    c = readme_card(n, body)
    c.cmd = cmd_line
    return c


def card_188() -> VGroup:
    """README card line 188 as it renders: 'Sign up in Docker Hub and create an Access Token' (a link)."""
    a = label("Sign up in Docker Hub and create an", 22, INK)
    b = label("Access Token", 22, INK)
    VGroup(a, b).arrange(RIGHT, buff=0.13, aligned_edge=DOWN)
    u = Line(b.get_corner(DL) + DOWN * 0.07, b.get_corner(DR) + DOWN * 0.07, color=INK, stroke_width=2)
    c = readme_card(188, VGroup(a, b, u))
    return c


def button(s: str, color=CLOUD, size: float = 20) -> VGroup:
    t = label(s, size, INK)
    b = RoundedRectangle(width=t.width + 0.5, height=0.46, corner_radius=0.1, stroke_color=color,
                         stroke_width=2).set_fill(color, 0.45)
    t.move_to(b)
    return VGroup(b, t)


def token_page() -> VGroup:
    """The schematic Docker Hub token page (no logo, no screenshot). .win .title .row1 .btn .perm .val
    .note_perm .field .lock .tok .note_tok (all positioned; .win is the window itself)."""
    win = browser_window(TOKEN_URL, width=9.4, height=4.3, size=20)
    win.shift(np.array([-6.3 - win.frame.get_left()[0], 1.22 - win.frame.get_top()[1], 0]))
    x0 = win.frame.get_left()[0] + 0.45
    y0 = win.frame.get_top()[1] - 0.55 - 0.42
    xr = win.frame.get_right()[0] - 0.45
    xv = x0 + 2.75                                                     # the value column

    def left(m, y):
        return m.move_to([x0 + m.width / 2, y, 0])

    title = left(label("Docker Hub · account settings", 24, INK), y0)
    row1 = left(label("Personal access tokens", 22, INK), y0 - 0.72)
    btn = button("Generate new token")
    btn.move_to([xr - btn.width / 2, row1.get_y(), 0])
    perm = left(label("Access permissions:", 22, S.GREY), y0 - 1.42)
    val = chip("Repo Read & Write", TURN, size=22)
    val.move_to([xv + val.width / 2, perm.get_y(), 0])
    note_perm = label("default: Repo Public Read-only · can't push", 20, S.GREY)
    note_perm.next_to(val, DOWN, buff=0.12).align_to(val, LEFT)
    tok_l = left(label("Access token", 22, S.GREY), y0 - 2.42)
    field = RoundedRectangle(width=xr - xv, height=0.5, corner_radius=0.08, stroke_color=S.GREY,
                             stroke_width=2).set_fill("#090A0D", 1)
    field.move_to([xv + field.width / 2, tok_l.get_y(), 0])
    tok = mono("<ACCESS TOKEN>", 22, INK)
    tok.move_to(field).align_to(field, LEFT).shift(RIGHT * 0.2)
    lock = lock_glyph(0.34, S.GREY).move_to([field.get_right()[0] - 0.32, field.get_y(), 0])
    note_tok = label("copy it now: shown only once", 20, S.GREY)
    note_tok.next_to(field, DOWN, buff=0.12).align_to(field, LEFT)
    g = VGroup(win, title, row1, btn, perm, val, note_perm, tok_l, field, tok, lock, note_tok)
    g.win, g.title, g.row1, g.btn, g.perm, g.val, g.note_perm = win, title, row1, btn, perm, val, note_perm
    g.tok_l, g.field, g.tok, g.lock, g.note_tok = tok_l, field, tok, lock, note_tok
    return g


def image_stack() -> LayerStack:
    """V6 · the image: seven unlabelled slabs (V2 fills: four thin ORANGE base slabs, the ORANGE apt/pip
    slab, the GREY COPY slab, the GREEN uv sync slab), floor at (STACK_X, FLOOR). Not added."""
    st = LayerStack(stack_w=STACK_W)
    st.floor.move_to([STACK_X, FLOOR, 0])
    for f, h in zip(FILLS, H_STACK):
        st.slabs.add(st.make(None, f, h))
    st._pending.clear()
    return st


def parcel_of(slab) -> RoundedRectangle:
    """A small copy of a slab (what travels to a registry): same fill, TEAL outline."""
    h = max(0.1, slab.slab_h * 0.5)
    r = RoundedRectangle(width=PARCEL_W, height=h, corner_radius=min(0.04, h / 2.5), stroke_color=IMAGE,
                         stroke_width=2).set_fill(slab.fill_hex, 0.5)
    return r.move_to(slab.box)


def pile(parcels, x: float, bottom: float, gap: float = 0.03) -> list:
    """Centres of the parcels stacked bottom-up from `bottom` at x."""
    out, y = [], bottom
    for p in parcels:
        out.append(np.array([x, y + p.height / 2, 0]))
        y += p.height + gap
    return out


def shelf(lines, dashed: bool = False) -> RegistryShelf:
    """A registry shelf at SHELF_C, its title replaced by `lines` (mobjects, stacked, BLUE) above the
    frame's left edge. .title"""
    sh = RegistryShelf("x", shelf_w=SHELF_W, shelf_h=SHELF_H, boards=1, dashed=dashed)
    sh.remove(sh.title)
    sh.shift(SHELF_C - sh.frame.get_center())
    t = VGroup(*lines).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    t.next_to(sh.frame, UP, buff=0.12).align_to(sh.frame, LEFT)
    sh.title = t
    sh.add(t)
    return sh


def level_parts(name: str = "docker.io/" + LONG) -> VGroup:
    """common.name_parts() with its letters on one baseline: it arranges the parts by their bottom edges,
    so `simple-translate-ac215` (descender p) sits higher than `docker.io`. Every glyph is moved onto the
    same glyph of one mono_line of the whole name; ticks and captions follow their parts."""
    g = name_parts(name)
    words = g[0]
    full = mono_line(name, 24)
    full.move_to(words)
    glyphs = [gl for w in words for gl in w]
    assert len(glyphs) == len(full.glyphs) == len(name)
    for gl, ref in zip(glyphs, full.glyphs):
        gl.move_to(ref)
    top, bot = full.strut.get_top()[1], full.strut.get_bottom()[1]
    for i, (part, cap, tick) in enumerate(zip(g.parts, g.captions, g.ticks)):
        below = i % 2 == 0
        edge = bot - 0.06 if below else top + 0.06
        cy = edge - 0.39 - cap.height / 2 if below else edge + 0.39 + cap.height / 2
        cap.move_to([part.get_x(), cy, 0])
        end = cap.get_top()[1] + 0.06 if below else cap.get_bottom()[1] - 0.06
        tick.put_start_and_end_on(np.array([part.get_x(), edge, 0]), np.array([part.get_x(), end, 0]))
    return g


def clipboard(h: float = 0.42, color=S.GREY) -> VGroup:
    """A paste glyph: a clipboard with two text lines."""
    w = h * 0.78
    board = RoundedRectangle(width=w, height=h, corner_radius=0.05, stroke_color=color,
                             stroke_width=2.5).set_fill(color, 0.15)
    clip = RoundedRectangle(width=w * 0.45, height=h * 0.16, corner_radius=0.03, stroke_color=color,
                            stroke_width=2.5).set_fill(S.BG, 1).move_to(board.get_top())
    lines = VGroup(*[Line(LEFT * w * 0.28, RIGHT * w * 0.28, color=color, stroke_width=2) for _ in range(2)])
    lines.arrange(DOWN, buff=h * 0.16).move_to(board).shift(DOWN * h * 0.06)
    return VGroup(board, clip, lines)


def dockerignore_card(lines=(".git", ".venv", "secrets/"), size: float = 22) -> VGroup:
    """S10's .dockerignore card: mono GREY header, GREEN lines. .frame .head .rows"""
    head = mono(".dockerignore", 20, S.GREY)
    rows = VGroup(*[mono(s, size, VENV) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    inner = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    fr = box(2.8, inner.height + 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, inner)
    g.frame, g.head, g.rows = fr, head, rows
    return g


def row_bar(row, color, opacity: float = 0.24) -> Rectangle:
    """A translucent bar the height of terminal row `row`, behind its glyphs."""
    g = row.glyphs
    return Rectangle(width=g.width + 0.16, height=row.strut.height * 0.92, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], row.strut.get_center()[1], 0])


def attach_back(scene, line, mob):
    """attach(), drawn behind the row's glyphs."""
    scene.remove(mob)
    line.add_to_back(mob)
    scene.add(line)
    return mob


def on_frame(t, mob, right: float = 0.3, rows: int | None = None):
    """Put `mob` on terminal t's top edge, right-aligned `right` inside its right edge (rows: where the top
    edge will be once common.resize() has given t that many rows; its bottom edge stays put)."""
    top = t.box.get_top()[1] if rows is None else t.box.get_bottom()[1] + rows * t.pitch + 0.45 + t.bar_h
    return mob.move_to([t.box.get_right()[0] - right - mob.width / 2, top, 0])


def scroll(scene, t, n_new: int, run_time: float = 0.35) -> None:
    """Make room for n_new rows like Terminal._make_room, but the rows that scroll off fade where they are
    (inside the strip) instead of drifting up over the picture above it."""
    over = len(t.lines) + n_new - t.rows
    if over <= 0:
        return
    gone = VGroup(*t.lines.submobjects[:over])
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(gone), run_time=run_time * 0.45)
    for m in gone:
        t.lines.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=run_time * 0.55)


def quick(t: float) -> float:
    """Rate function: a fade that is done in the first third of a longer move (S14's own)."""
    return min(1.0, 3.0 * t)


def lead(vo, phrase: str, early: float) -> None:
    """Wait until `early` seconds before `phrase` is spoken."""
    dt = vo.time_until(phrase) - early
    if dt > 1 / 60:
        vo.scene.wait(dt)


def go(p, point, run_time: float, fade: bool = False, rate_func=smooth) -> ApplyFunction:
    """Animation: `p` moves to `point` (and fades out). Its target is made when it starts, so several of these
    can follow each other in one Succession: `p.animate` builders all share p.target (the last one made), so in
    a Succession every `.animate` step would head for the final step's target."""
    point = np.array(point, dtype=float)

    def f(m):
        m.move_to(point)
        return m.set_opacity(0) if fade else m
    return ApplyFunction(f, p, run_time=run_time, rate_func=rate_func)


def rows_of(t, lines) -> VGroup:
    """Terminal.print's rows (no wrap), placed under t's last row and put in t.lines, for a FadeIn played with
    other animations (Terminal.print plays its own). Play their FadeIn before anything is rendered."""
    new = VGroup()
    for s in lines:
        ln = mono_line(t._cut(s), t.size, OUTPUT)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        new.add(ln)
    return new


# ------------------------------------------------------------------ the scene
class TagAndPush(VoiceScene):
    def stamp_parcels(self, parcels, slots, path, through=None, lag: float = 0.22, run_time: float = 2.4,
                      extra=()):
        """The slabs' parcels lift off one by one, ride `path` and settle at `slots` (via `through`)."""
        anims = []
        for p, s in zip(parcels, slots):
            steps = [FadeIn(p, scale=0.6, run_time=0.2), go(p, path.get_start(), 0.2),
                     MoveAlongPath(p, path, run_time=0.55)]
            if through is not None:
                steps.append(go(p, through, 0.15))
            steps.append(go(p, s, 0.2))
            anims.append(Succession(*steps))
        self.play(LaggedStart(*anims, lag_ratio=lag), *extra, run_time=run_time)

    def construct(self):
        assert len(SAY) == 10, f"S12 has {len(SAY)} SAY lines; this scene times 10"

        # ========================================================== 0 · B1: the access token
        tr_a = tracker_a(16)
        tr = tracker_b()
        c188 = card_188()
        c188.shift(np.array([-6.5 - c188.get_left()[0], 2.7 - c188.get_top()[1], 0]))
        page = token_page()
        ill0 = illustration_tag().next_to(page.win.frame, RIGHT, buff=0.25).align_to(page.win.frame, UP)
        pw = VGroup(label("a token is a password:", 22, S.GREY), label("never in a file, never in a repo", 22, S.GREY))
        pw.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        pw.move_to([c188.get_right()[0] + 0.45 + pw.width / 2, c188.get_y(), 0])
        yt0 = your_turn().next_to(page.field, RIGHT, buff=0.75)
        frame_bits = VGroup(page.win, page.title)
        sec = readme_card(186, label(SECTION_B, 34, INK)).move_to([0, 0.5, 0])    # as S14's line 203
        tr_rest = VGroup(tr.head[0], tr.head[1], tr.dots, tr.caption)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr_a, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(sec, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Pushing Docker Image to Docker Hub")
            # the README's heading becomes the new tracker's section name (what became what)
            self.play(FadeOut(tr_a, shift=UP * 0.25), FadeIn(tr_rest, shift=UP * 0.25),
                      ReplacementTransform(sec.body, tr.head[2]), FadeOut(VGroup(sec.frame, sec.head), rate_func=quick),
                      run_time=1.0)
            self.remove(tr_rest, tr.head[2])
            self.add(tr)
            self.play(Indicate(tr.head[2], color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("First, sign up")
            self.play(track(tr, 1), FadeIn(c188, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(frame_bits, shift=UP * 0.15), FadeIn(ill0), run_time=0.6)
            vo.wait_until("and create an access token")
            self.play(FadeIn(page.row1, shift=RIGHT * 0.1), FadeIn(page.btn, scale=1.1), run_time=0.5)
            self.play(Indicate(page.btn[0], color=CLOUD, scale_factor=1.1),     # the label stays INK on the fill
                      Indicate(page.btn[1], color=INK, scale_factor=1.1), run_time=0.7)
            vo.wait_until("with read and write access")
            self.play(FadeIn(page.perm, shift=RIGHT * 0.1), FadeIn(page.val, scale=1.15), run_time=0.5)
            vo.wait_until("not the default")
            self.play(FadeIn(page.note_perm, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Copy it right away")
            self.play(FadeIn(VGroup(page.tok_l, page.field, page.tok, page.lock), shift=RIGHT * 0.1), run_time=0.5)
            self.play(Indicate(page.tok, color=TURN, scale_factor=1.08), FadeIn(page.note_tok, shift=UP * 0.1),
                      run_time=0.7)
            vo.wait_until("and it works like a password")
            self.play(page.lock.animate.set_color(TURN), FadeIn(pw, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(page.lock, color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("Pause and make yours")
            self.play(FadeIn(yt0, shift=LEFT * 0.15), run_time=0.4)

        # ========================================================== 1 · B2: the README's login (not run here)
        c189 = card_line(189, LOGIN_WORDS, LOGIN_README)
        c189.move_to([0, 1.25, 0])
        u_name = substring(c189.cmd, "<USER NAME>")
        u_tok = substring(c189.cmd, "<ACCESS TOKEN>")
        bx_name = SurroundingRectangle(u_name, color=TURN, buff=0.07, stroke_width=3, corner_radius=0.05)
        bx_tok = SurroundingRectangle(u_tok, color=TURN, buff=0.07, stroke_width=3, corner_radius=0.05)
        y_low = c189.frame.get_bottom()[1] - 0.32
        yours1 = label("yours", 22, TURN).move_to([bx_name.get_x(), y_low, 0])
        yours2 = label("yours", 22, TURN).move_to([bx_tok.get_x(), y_low, 0])
        not_run = label("no Docker Hub account in our recording · not run here", 22, S.GREY)
        not_run.move_to([0, y_low - 0.75, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(page, ill0, pw, yt0), shift=DOWN * 0.2), FadeOut(c188, shift=UP * 0.2),
                      track(tr, 2), run_time=0.6)
            self.play(FadeIn(c189, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("docker login")
            self.play(Indicate(c189.cmd, color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("dash u with your user name")
            self.play(Create(bx_name), u_name.animate.set_color(TURN), FadeIn(yours1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("dash p with your token")
            self.play(Create(bx_tok), u_tok.animate.set_color(TURN), FadeIn(yours2, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("We have no account")
            self.play(FadeIn(not_run, shift=UP * 0.1), run_time=0.5)
        c189.add(bx_name, bx_tok)
        self.add(c189)                                   # the boxes now move and fade with the card

        # ========================================================== 2 · B2 · extra: the stand-in login
        t = laptop_term(8)
        sit = on_frame(t, stand_in_tag(size=20))

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(yours1, yours2, not_run)), c189.animate.move_to([0, 1.95, 0]),
                      track(tr, 2, extra=True), run_time=0.6)
            self.play(FadeIn(t), run_time=0.5)
            bare_prompt(self, t)                         # the prompt waits (no empty box for 4 s)
            vo.wait_until("a small registry")
            self.play(FadeIn(sit, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("just watch those")
            self.play(Indicate(sit.lines[1], color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Logging in to it")
            cmd2 = type_cmd(self, t, LOGIN_LOCAL, 1.2)
            out2 = t.print(self, OUT05, run_time=0.5, wrap=True)
            warn_rows = [r for r in out2 if r.text != OUT05[1]]
            ok_row = out2[-1]
            vo.wait_until("warns that")
            bars = [row_bar(r, TURN, 0.26) for r in warn_rows]
            self.play(*[FadeIn(b) for b in bars], *[r.glyphs.animate.set_color(TURN) for r in warn_rows],
                      run_time=0.5)
            for r, b in zip(warn_rows, bars):
                attach_back(self, r, b)
            p_part = substring(cmd2.rows[-1], "-p not-a-real-token")
            self.play(ok_row.glyphs.animate.set_color(VENV), Indicate(p_part, color=TURN, scale_factor=1.05),
                      run_time=0.7)
            self.add(cmd2.rows[-1], ok_row)
            bare_prompt(self, t)

        # ========================================================== 3 · the slip: -p lands in the history
        hist_rows = [mono_line(s, 22, S.GREY) for s in HISTORY] + [mono_line(LOGIN_README, 22, INK)]
        hist_head = mono("~/.bash_history", 20, S.GREY)
        hist_body = VGroup(*hist_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        hist_in = VGroup(hist_head, hist_body).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        hist_fr = box(hist_in.width + 0.7, hist_in.height + 0.5, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        hist_in.move_to(hist_fr)
        hist = VGroup(hist_fr, hist_in)
        hist.shift(np.array([-6.3 - hist_fr.get_left()[0], 0.78 - hist_fr.get_top()[1], 0]))
        ill3 = illustration_tag().next_to(hist_fr, RIGHT, buff=0.3).align_to(hist_fr, UP)
        new_row = hist_rows[-1]
        red_part = substring(new_row, "-p <ACCESS TOKEN>")
        err3 = erratum_tag().next_to(hist_fr, RIGHT, buff=0.3).match_y(new_row.strut)
        safe = chip("docker login -u <USER NAME>", VENV, size=24, font=MONO)
        safe.move_to([-6.3 + safe.width / 2, hist_fr.get_bottom()[1] - 0.62, 0])
        pw_row = mono("Password:", 22, S.GREY)
        pw_row.move_to([safe.get_left()[0] + 0.3 + pw_row.width / 2, safe.get_y() - 0.78, 0])
        pw_field = RoundedRectangle(width=1.5, height=0.42, corner_radius=0.06, stroke_color=S.GREY,
                                    stroke_width=2).set_fill("#090A0D", 1)
        pw_field.next_to(pw_row, RIGHT, buff=0.2)
        clip = clipboard().next_to(pw_field, RIGHT, buff=0.9)
        pw_note = label("paste your token · nothing shows", 20, S.GREY).next_to(pw_field, RIGHT, buff=0.35)
        yt3 = your_turn().next_to(safe, RIGHT, buff=0.4)
        alt3 = label("or the README's form", 20, S.GREY).next_to(yt3, RIGHT, buff=0.3)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(t), FadeOut(sit), track(tr, 2, extra=False), run_time=0.5)
            self.remove(*t.get_family())
            self.play(FadeIn(hist_fr), FadeIn(hist_head), FadeIn(VGroup(*hist_rows[:2])), FadeIn(ill3),
                      run_time=0.6)
            self.play(TransformFromCopy(c189.cmd.glyphs, new_row.glyphs, path_arc=-0.4), run_time=1.0)
            self.add(new_row)
            vo.wait_until("with dash p")
            self.play(red_part.animate.set_color(ERR), Indicate(substring(c189.cmd, "-p"), color=ERR), run_time=0.5)
            vo.wait_until("your token stays")
            hl = under(red_part, ERR)
            self.play(Create(hl), FadeIn(err3, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(red_part, color=ERR, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Instead")
            self.play(FadeIn(safe, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("then paste the token")
            self.play(FadeIn(pw_row, shift=RIGHT * 0.1), FadeIn(pw_field), FadeIn(clip, shift=LEFT * 0.2),
                      run_time=0.5)
            self.play(clip.animate.move_to(pw_field).scale(0.8), run_time=0.6)
            self.play(FadeOut(clip, scale=0.6), pw_field.animate(rate_func=there_and_back).set_stroke(INK, 4),
                      FadeIn(pw_note, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Pause and log in")
            self.play(FadeIn(yt3, shift=LEFT * 0.15), run_time=0.4)
            self.play(FadeIn(alt3), run_time=0.3)

        # ========================================================== 4 · B3: tag (laptop/43), image ls (laptop/44)
        c190 = card_line(190, TAG_WORDS, TAG_README, cmd_size=22)
        c190.move_to([0, 2.0, 0])
        cap4 = user_caption().move_to([0, c190.get_bottom()[1] - 0.42, 0])
        t4 = laptop_term(7)
        colcap = on_frame(t4, row_tag("columns: IMAGE · ID · DISK USAGE"))

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(hist, ill3, err3, hl, safe, pw_row, pw_field, pw_note, yt3, alt3)),
                      FadeOut(c189, shift=UP * 0.2), track(tr, 3), run_time=0.6)
            self.play(FadeIn(c190, shift=UP * 0.2), FadeIn(t4), run_time=0.6)
            bare_prompt(self, t4)
            cmd4 = type_cmd(self, t4, DOCKER_TAG, 1.4)
            r4 = cmd4.rows[-1]
            vo.wait_until("then your user name")
            stu = substring(r4, "student")
            self.play(FadeIn(cap4, shift=DOWN * 0.1), stu.animate.set_color(TURN),
                      substring(c190.cmd, "<USER NAME>").animate.set_color(TURN), run_time=0.6)
            self.add(r4)
            self.play(Indicate(stu, color=TURN, scale_factor=1.2), run_time=0.6)
            self.add(r4)
            bare_prompt(self, t4)
            vo.wait_until("Pause and run it")
            pin(self, r4, beside(row_tag("▶ your turn", TURN), r4), run_time=0.4)
            vo.wait_until("An extra image ls")
            self.play(track(tr, 3, extra=True), run_time=0.4)
            c4b = type_cmd(self, t4, IMAGE_LS, 0.6)
            pin(self, c4b, beside(row_tag("extra"), c4b), run_time=0.3)
            out4 = t4.print(self, LS44, run_time=0.5)
            self.play(FadeIn(colcap, shift=DOWN * 0.1), run_time=0.3)
            pr4 = bare_prompt(self, t4)
            n1, n2 = substring(out4[1], SHORT), substring(out4[2], LONG)
            i1, i2 = substring(out4[1], ID), substring(out4[2], ID)
            vo.wait_until("shows two names")
            u1, u2 = under(n1, IMAGE), under(n2, IMAGE)
            self.play(Create(u1), Create(u2), n1.animate.set_color(IMAGE), n2.animate.set_color(IMAGE), run_time=0.5)
            vo.wait_until("one ID")
            b1 = SurroundingRectangle(i1, color=IMAGE, buff=0.06, stroke_width=2.5)
            b2 = SurroundingRectangle(i2, color=IMAGE, buff=0.06, stroke_width=2.5)
            self.play(i1.animate.set_color(IMAGE), i2.animate.set_color(IMAGE), Create(b1), Create(b2), run_time=0.5)
            vo.wait_until("a second name")
            same = row_tag("same ID · a second name, not a copy", IMAGE)
            pin(self, pr4, beside(same, pr4, min_x=b1.get_left()[0]), run_time=0.4)
            self.play(Indicate(VGroup(b1, b2), color=IMAGE, scale_factor=1.12), run_time=0.6)
            for row, ms in ((out4[1], (u1, b1)), (out4[2], (u2, b2))):
                for m in ms:
                    attach(self, row, m)

        # ========================================================== 5 · V6: two names, one image; the long name
        st = image_stack()
        id_lbl = mono(ID, 22, IMAGE).next_to(st.slabs, DOWN, buff=0.2)
        notes = VGroup(sticky(SHORT), sticky(LONG)).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        notes.next_to(st.slabs, RIGHT, buff=0.9)
        links = VGroup(*[Line(n.get_left(), [st.slabs.get_right()[0], n.get_y(), 0], color=IMAGE, stroke_width=2.5)
                         for n in notes])
        parts = level_parts()
        parts.move_to([0, -1.4, 0])
        words = parts[0]
        tail = VGroup(*[g for w in words[2:] for g in w])                     # student/…:latest, glyph by glyph
        assert len(tail) == len(notes[1].text) == len(LONG)
        lib_chip = chip(LIBRARY, S.GREY, size=22, font=MONO, fill_opacity=0.1)
        assert len(lib_chip.text) == len(LIBRARY)
        lib_note = VGroup(label("as in the build log:", 20, S.GREY), label("no account → library", 20, S.GREY))
        lib_note.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        VGroup(lib_chip, lib_note).arrange(RIGHT, buff=0.3).move_to([0, -2.95, 0])

        with self.voiceover(SAY[5]) as vo:
            # the card goes first (the stack stands where it was), then the names and the ID lift out of the
            # terminal as it fades (the ID label lands on its title bar)
            self.play(track(tr, 3, extra=False), FadeOut(VGroup(c190, cap4), shift=UP * 0.2), FadeOut(colcap),
                      run_time=0.4)
            self.play(FadeIn(st, shift=UP * 0.15), FadeIn(VGroup(notes[0].note, notes[1].note)),
                      TransformFromCopy(n1, notes[0].text), TransformFromCopy(n2, notes[1].text),
                      TransformFromCopy(i1, id_lbl), FadeOut(t4, rate_func=lambda a: smooth(min(1, a * 1.6))),
                      run_time=1.1)
            self.remove(*t4.get_family())
            self.add(notes)
            vo.wait_until("in four parts")
            self.play(TransformFromCopy(notes[1].text, tail, path_arc=0.3), Create(links), run_time=1.0)
            vo.wait_until("the registry")
            self.play(FadeIn(VGroup(words[0], words[1]), shift=RIGHT * 0.3), run_time=0.5)
            self.play(Create(parts.ticks[0]), FadeIn(parts.captions[0], shift=UP * 0.1),
                      Indicate(words[0], color=TURN, scale_factor=1.12), run_time=0.6)
            for k, phrase in ((1, "your account"), (2, "the repository"), (3, "and the tag")):
                vo.wait_until(phrase)
                w = words[2 * k]
                self.play(Create(parts.ticks[k]), FadeIn(parts.captions[k], shift=(UP if k % 2 == 0 else DOWN) * 0.1),
                          Indicate(w, color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(parts)                              # (takes the wrapper `tail` off the list)
            vo.wait_until("Names without an account")
            self.play(Indicate(notes[0], color=IMAGE, scale_factor=1.06), run_time=0.5)
            # the chip grows out of the short note: its letters fly into the chip's tail
            chip_txt = lib_chip.text
            k0 = len(LIBRARY) - len(SHORT)
            chip_tail = VGroup(*chip_txt[k0:])
            chip_head = VGroup(*chip_txt[:k0])
            self.play(FadeIn(lib_chip.box), TransformFromCopy(notes[0].text, chip_tail), run_time=0.8)
            self.play(FadeIn(chip_head, shift=RIGHT * 0.2), FadeIn(lib_note, shift=LEFT * 0.1), run_time=0.5)
            self.add(lib_chip)
            vo.wait_until("fall under library")
            lib_w = VGroup(*chip_txt[len("docker.io/"):len("docker.io/library")])
            self.play(lib_w.animate.set_color(TURN), run_time=0.3)                # it stays YELLOW
            self.play(Indicate(lib_w, color=TURN, scale_factor=1.15), run_time=0.6)

        # ========================================================== 6 · B4: push to Docker Hub (denied)
        hub = shelf([label("Docker Hub", 22, CLOUD), mono(REPO, 20, CLOUD)])
        door = hub.door
        parcels = [parcel_of(s) for s in st.slabs]
        q_x = door.get_left()[0] - 0.65                                     # the queue at the door (clear of its cross)
        q_slots = pile(parcels, q_x, hub.frame.get_bottom()[1] + 0.06)
        q_top = q_slots[-1][1] + parcels[-1].height / 2
        path = route(np.array([st.slabs.get_right()[0] + 0.15, 1.25, 0]), np.array([q_x, q_top + 0.3, 0]),
                     arc=-0.45)
        check_lbl = label("missing? → upload", 20, S.GREY)
        check_lbl.move_to([q_x - PARCEL_W / 2 - 0.3 - check_lbl.width / 2, 0.85, 0])
        c191 = card_line(191, PUSH_WORDS, PUSH_README)
        yt6 = your_turn()
        VGroup(c191, yt6).arrange(RIGHT, buff=0.4).move_to([0, -2.55, 0])
        ok_note = VGroup(label("logged in:", 22, VENV), mono("Pushed … latest: digest: …", 22, VENV),
                         label("(next)", 22, VENV)).arrange(RIGHT, buff=0.18)
        ok_note.move_to([SHELF_C[0] - 0.4, 0.0, 0])
        assert len(hub.title[1]) == len(REPO)
        note_repo = VGroup(*notes[1].text[:len(REPO)])

        with self.voiceover(SAY[6]) as vo:
            self.play(track(tr, 4), FadeOut(VGroup(parts, lib_chip, lib_note)), FadeOut(notes[0]),
                      FadeOut(links[0]), run_time=0.5)
            self.play(FadeIn(VGroup(hub.frame, hub.boards, hub.door, hub.title[0])), FadeOut(links[1]),
                      TransformFromCopy(note_repo, hub.title[1]), FadeOut(notes[1]), run_time=0.9)
            self.add(hub)
            self.play(Create(path), FadeIn(c191, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Pause and run it")
            self.play(FadeIn(yt6, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("Yours should upload")
            self.play(FadeIn(check_lbl, shift=DOWN * 0.1), run_time=0.3)
            self.stamp_parcels(parcels, q_slots, path, run_time=2.4)
            vo.wait_until("and end with a digest line")
            self.play(FadeIn(ok_note, shift=UP * 0.1), run_time=0.5)

            # ---- the real answer: a 12-row terminal; the picture parks in the corner (no text)
            vo.wait_until("Without an account")
            texts = VGroup(hub.title, check_lbl, id_lbl)
            body = VGroup(*[s.box for s in st.slabs], path, hub.frame, hub.boards, hub.door, *parcels)
            ghost = body.copy()
            k = THUMB_W / ghost.width
            home = ghost.get_center().copy()
            t6 = laptop_term(12)
            self.remove(*body, *st.get_family(), hub, *parcels)
            self.add(ghost)
            self.play(ghost.animate.scale(k).move_to(THUMB_C), FadeOut(texts), FadeOut(VGroup(c191, yt6, ok_note)),
                      run_time=0.7)
            self.play(FadeIn(t6), run_time=0.4)
            bare_prompt(self, t6)
            type_cmd(self, t6, DOCKER_PUSH, 0.9)
            out6 = t6.print(self, [*OUT03[:-1], (OUT03[-1], ERR)], run_time=0.6, wrap=True, lag=0.08)
            deny = list(out6[-3:])
            vo.wait_until("push access denied")
            g_door = ghost[len(st.slabs) + 3]
            x_small = cross_mark(0.35 * k, ERR, stroke=3).move_to(g_door)
            self.play(*[Indicate(r.glyphs, color=ERR, scale_factor=1.04) for r in deny],
                      g_door.animate.set_stroke(ERR).set_fill(ERR, 0.45), FadeIn(x_small, scale=1.5), run_time=0.8)
            rc = row_tag("real capture · 2026-10-13")
            wg = row_tag("what we got · no Docker Hub account")
            VGroup(rc, wg).arrange(RIGHT, buff=0.25)
            beside(VGroup(rc, wg), deny[-1], buff=0.5)
            pin(self, deny[-1], VGroup(rc, wg), run_time=0.4)

            # ---- if you see this: the strip keeps line 8, the picture comes back with its door shut
            fix = VGroup(row_tag("if you see this:"), row_tag("log in", TURN), row_tag("a token that can write", TURN),
                         row_tag("the name must start with YOUR username", TURN))
            fix.arrange(RIGHT, buff=0.18).move_to([0, -0.88, 0])
            assert fix.width < 13.0, fix.width
            vo.wait_until("If you see it")
            resize(self, t6, STRIP_ROWS, keep=deny, run_time=0.7,
                   extra=[ghost.animate.scale(1 / k).move_to(home),
                          x_small.animate.scale(1 / k).move_to(home + (x_small.get_center() - THUMB_C) / k)])
            door.set_stroke(ERR).set_fill(ERR, 0.45)
            x_big = cross_mark(0.35, ERR).move_to(door)
            self.remove(ghost, x_small)
            self.add(st, path, hub, x_big, *parcels)
            self.play(FadeIn(hub.title), FadeIn(id_lbl), FadeIn(fix[0]), FadeIn(fix[1], shift=UP * 0.1),
                      FadeIn(ok_note, shift=UP * 0.1), run_time=0.4)
            self.add(hub)
            back = [Succession(go(p, path.get_start(), 0.5), go(p, s.box.get_center(), 0.3, fade=True))
                    for p, s in zip(reversed(parcels), reversed(list(st.slabs)))]
            vo.wait_until("and check your token can write")
            self.play(LaggedStart(*back, lag_ratio=0.15), FadeIn(fix[2], shift=UP * 0.1), run_time=1.2)
            self.remove(*parcels)
            vo.wait_until("and the name starts")
            self.play(FadeIn(fix[3], shift=UP * 0.1), run_time=0.4)

        # ========================================================== 7 · B4 · extra: the stand-in push goes through
        sin = shelf([label("stand-in registry", 22, CLOUD), mono("localhost:5000", 20, CLOUD)], dashed=True)
        land = pile(parcels, sin.spot(0, 1, 3)[0], sin.boards[0].get_y() + 0.04)
        sit7 = stand_in_tag(size=20)

        with self.voiceover(SAY[7]) as vo:
            # the narration is 5.7 s: "On the stand-in", the shelves swap while the strip clears and grows (its
            # tag comes with it); the two commands type quickly; "the push goes through": the slabs travel while
            # the output prints, and the digest underlines as it is said
            self.play(track(tr, 4, extra=True), FadeOut(fix), FadeOut(ok_note), FadeOut(VGroup(hub, x_big)),
                      FadeIn(sin, shift=DOWN * 0.1), FadeOut(t6.lines), run_time=0.5)
            for m in list(t6.lines):
                t6.lines.remove(m)
            on_frame(t6, sit7, rows=STAND_ROWS)
            resize(self, t6, STAND_ROWS, run_time=0.4, extra=[FadeIn(sit7, shift=DOWN * 0.1)])
            bare_prompt(self, t6)
            type_cmd(self, t6, TAG_LOCAL, 0.5)
            bare_prompt(self, t6)
            type_cmd(self, t6, PUSH_LOCAL, 0.5)
            scroll(self, t6, len(OUT07), run_time=0.3)   # the tag's two rows fade in place
            out7 = rows_of(t6, OUT07)                     # laptop-push/07: 3-4, …, 15 (shown below)
            parcels = [parcel_of(s) for s in st.slabs]
            door_in = np.array([sin.door.get_right()[0] + 0.25, sin.door.get_y(), 0])
            dig = substring(out7[-1], "sha256:2c302ec4c536…")
            u7 = under(dig, IMAGE)
            printed = Succession(LaggedStart(*[FadeIn(r) for r in out7], lag_ratio=0.3, run_time=0.9),
                                 AnimationGroup(Create(u7), dig.animate.set_color(IMAGE), run_time=0.45),
                                 Wait(0.25))
            self.stamp_parcels(parcels, land, path, through=door_in, lag=0.14, run_time=1.6, extra=[printed])
            attach(self, out7[-1], u7)
            fp = fingerprint(0.24, IMAGE)
            fp.move_to([sin.frame.get_right()[0] - 0.55, sin.frame.get_y() + 0.15, 0])
            fp_l = label("digest", 20, IMAGE).next_to(fp, DOWN, buff=0.1)
            vo.wait_until("a fingerprint")
            self.play(FadeIn(fp, scale=0.4), FadeIn(fp_l), run_time=0.4)
            self.play(fp.animate(rate_func=there_and_back).scale(1.3), run_time=0.5)   # (Indicate would fill the disc)

        # ========================================================== 8 · again: already exists; Docker Hub has python
        dh = shelf([label("Docker Hub", 22, CLOUD)])
        py = VGroup(*[RoundedRectangle(width=1.0, height=0.12, corner_radius=0.04, stroke_color=IMAGE, stroke_width=2)
                      .set_fill(SYSTEM, 0.5) for _ in range(4)]).arrange(UP, buff=0.04)
        py.move_to(dh.spot(0, 1, 3), aligned_edge=DOWN)
        py_l = mono("python", 22, SYSTEM).next_to(py, RIGHT, buff=0.25)
        ill8 = illustration_tag().next_to(dh.frame, UP, buff=0.12).align_to(dh.frame, RIGHT)
        cap8 = label("already on Docker Hub · from the official python image", 20, S.GREY)
        cap8.next_to(dh.frame, DOWN, buff=0.2).align_to(dh.frame, RIGHT)
        base = list(st.slabs)[:4]
        ties = VGroup(*[Line(s.box.get_right() + RIGHT * 0.06, p.get_left() + LEFT * 0.06, color=S.GREY, stroke_width=2)
                        for s, p in zip(base, py)])

        with self.voiceover(SAY[8]) as vo:
            t6.clear(self, run_time=0.25)                # the command stays on screen with its output, no scroll
            bare_prompt(self, t6)
            type_cmd(self, t6, PUSH_LOCAL, 0.6)
            out8 = t6.print(self, OUT08, run_time=0.3, lag=0.1)
            vo.wait_until("every layer already exists")
            bouncers = [parcel_of(s) for s in st.slabs]
            ex_l = label("already exists", 20, S.GREY)
            ex_l.move_to([q_x - PARCEL_W / 2 - 0.3 - ex_l.width / 2, 0.85, 0])
            hit = path.get_end()
            anims = []
            for p in bouncers:
                anims.append(Succession(FadeIn(p, scale=0.6, run_time=0.15), go(p, path.get_start(), 0.2),
                                        MoveAlongPath(p, path, run_time=0.45),
                                        go(p, hit + LEFT * 0.7 + DOWN * 0.25, 0.3, fade=True, rate_func=rush_from)))
            rows8 = [r for r in out8 if "already exists" in r.text]
            us8 = [under(substring(r, "Layer already exists"), IMAGE) for r in rows8]
            only = label("only missing layers travel", 22, S.GREY)
            only.move_to([(st.slabs.get_right()[0] + sin.frame.get_left()[0]) / 2, 0.3, 0])   # clear of the strip's top
            self.play(LaggedStart(*anims, lag_ratio=0.16), FadeIn(ex_l, shift=DOWN * 0.1),
                      *[Create(u) for u in us8], Succession(Wait(0.7), FadeIn(only, shift=UP * 0.1, run_time=0.5)),
                      run_time=1.6)
            self.remove(*bouncers)
            for r, u in zip(rows8, us8):
                attach(self, r, u)
            vo.wait_until("and only missing layers travel")
            self.play(Indicate(only, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("On Docker Hub")
            self.play(FadeOut(VGroup(only, ex_l, path, fp, fp_l)), FadeOut(sin), FadeOut(VGroup(*parcels)), run_time=0.4)
            resize(self, t6, STRIP_ROWS, run_time=0.5, extra=[sit7.animate.shift(DOWN * (STAND_ROWS - STRIP_ROWS) * t6.pitch)])
            self.play(FadeIn(VGroup(dh.frame, dh.boards, dh.door, dh.title)), FadeIn(ill8, shift=DOWN * 0.1),
                      FadeIn(py, shift=DOWN * 0.3), FadeIn(py_l), run_time=0.6)
            vo.wait_until("even the base layers")
            self.play(*[s.box.animate.set_stroke(SYSTEM) for s in base], run_time=0.3)
            self.play(LaggedStart(*[Create(x) for x in ties], lag_ratio=0.15), FadeIn(cap8, shift=UP * 0.1),
                      run_time=0.8)
            self.play(*[s.box.animate.set_stroke(IMAGE) for s in base], run_time=0.3)
            vo.wait_until("it already has them")
            self.play(Indicate(VGroup(py, py_l), color=SYSTEM, scale_factor=1.12), run_time=0.7)

        # ========================================================== 9 · public by default
        repo_fr = box(7.0, 3.9, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        repo_fr.move_to([0.55, -0.45, 0])
        r_title = mono(REPO, 24, INK)
        r_title.move_to(repo_fr.get_corner(UL) + np.array([0.35 + r_title.width / 2, -0.45, 0]))
        pub = chip("public", CLOUD, size=22, fill_opacity=0.45)
        pub.next_to(r_title, DOWN, buff=0.25).align_to(r_title, LEFT)
        ill9 = illustration_tag().next_to(repo_fr, UP, buff=0.15).align_to(repo_fr, RIGHT)
        dx = repo_fr.get_left()[0] + 0.45 - st.slabs.get_left()[0]           # the image goes down, then in
        dy = repo_fr.get_bottom()[1] + 0.3 - st.slabs.get_bottom()[1]
        copy_slab = st.slabs[5]
        git_g = VGroup(folder_glyph(0.3, S.GREY), mono(".git/", 22, INK)).arrange(RIGHT, buff=0.12)
        git_g.move_to([st.slabs.get_right()[0] + dx + 0.7 + git_g.width / 2, copy_slab.box.get_y() + dy, 0])
        git_lead = Line(copy_slab.box.get_right() + np.array([dx + 0.05, dy, 0]), git_g.get_left() + LEFT * 0.08,
                        color=S.GREY, stroke_width=2)
        folks = VGroup(*[person_icon(S.GREY, 0.42) for _ in range(3)]).arrange(DOWN, buff=0.35)
        folks.move_to([5.6, -0.45, 0])
        pulls = VGroup(*[route(repo_fr.get_right() + RIGHT * 0.1 + UP * dy, f.get_left() + LEFT * 0.1, arc=0)
                         for f, dy in zip(folks, (0.6, 0, -0.6))])
        dig9 = dockerignore_card()
        dig_t = illustration_tag("illustration · a file you'd add")      # S10's and S11's tag for this card
        # where the image stood; the tag (wider than the card, left-aligned) runs over repo_fr's x-range, so
        # card and tag sit high enough for the tag to clear repo_fr's top by more than ill9 does
        dig_t.move_to([-6.3 + dig_t.width / 2, repo_fr.get_top()[1] + 0.8, 0])
        dig9.next_to(dig_t, DOWN, buff=0.2).align_to(dig_t, LEFT)

        with self.voiceover(SAY[9]) as vo:
            self.play(track(tr, 4, extra=False), FadeOut(t6), FadeOut(sit7),
                      FadeOut(VGroup(dh, ill8, py, py_l, cap8, ties)), run_time=0.5)
            self.remove(*t6.get_family())
            self.play(FadeOut(id_lbl), FadeIn(repo_fr), FadeIn(r_title), FadeIn(ill9), run_time=0.5)
            self.bring_to_front(st)                      # drawn over the card's opaque fill
            self.play(st.animate.shift(UP * dy), run_time=0.5)
            self.play(st.animate.shift(RIGHT * dx), run_time=0.6)
            vo.wait_until("is public by default")
            self.play(FadeIn(pub, scale=1.3), run_time=0.4)
            self.play(Indicate(pub.box, color=CLOUD, scale_factor=1.15), Indicate(pub.text, color=INK, scale_factor=1.15),
                      Create(git_lead), FadeIn(git_g, shift=LEFT * 0.1),
                      run_time=0.6)
            vo.wait_until("Anyone can pull it")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(f, shift=LEFT * 0.2)) for a, f in zip(pulls, folks)],
                                  lag_ratio=0.3), run_time=1.0)
            vo.wait_until("git folder and all")
            self.play(git_g.animate.set_color(ERR), copy_slab.box.animate.set_stroke(ERR), run_time=0.3)
            self.play(Indicate(git_g, color=ERR, scale_factor=1.25), FadeOut(VGroup(pulls, folks)), run_time=0.7)
            self.play(FadeIn(dig9, shift=LEFT * 0.2), FadeIn(dig_t), run_time=0.5)
            self.play(Indicate(dig9.rows[0], color=VENV, scale_factor=1.3), run_time=0.6)

        self.wait(0.6)                                   # time to read the card's three lines
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
