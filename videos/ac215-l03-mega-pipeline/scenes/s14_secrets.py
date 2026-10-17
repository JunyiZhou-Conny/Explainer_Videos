r"""S14 · Keep the key out of the image (extras with an 82-byte stand-in; V6 Two filters; V3; the
optional Docker Hub push; the solution branch's coda).

V6 (common.TwoFilters) is laid out so it fits above the 4-row strip ("HOME": the folder left, the
image box bottom centre-left with a small layer stack inside its front, the Git book top right;
the Docker Hub shelf only in beat 0). When an output needs more rows, the terminal grows to 7 rows
and the image box "parks" top right (with its sieve) while the folder and the book fade; it glides
back when the terminal shrinks to the strip again. When a beat's commands need 10 rows (beat 1's
four extras, beat 5's build and run), V6 fades altogether and comes back with the strip. Terminal titles: "laptop", and "laptop · the
same build, full log" while a G1 build's plain log is on screen.

Beats (script.md "## S14", one voiceover block each):
 0  No tracker. V6: the GREY transcribe_audio/ folder with the GOLD key in secrets/, the GREY book
    "Git history", the TEAL box "image" (inside its front a small stack: ORANGE base, the GREY COPY
    slab, GREEN venv), the Docker Hub shelf. The key, the book, the box and the shelf pulse as named;
    a YELLOW "?" in the box. PONDER (8 s) under the picture.
 1  The card goes, the shelf fades, V6 settles above the strip; TRACKER A13 · extra. A 4-row strip
    (prompt .../synthesis_audio$). GREY tag "stand-in file · not a real key" under the folder;
    `cd ../transcribe_audio` (extra) -> (no output). Then V6 fades and the terminal grows to 10
    rows, so every extra stays in view with its output: `ls secrets`, `git status --short`,
    `git check-ignore -v secrets/mega-pipeline.json` (extras) -> 20-g1 lines 2, 3, 4 (the tab of
    line 4 shown as one space, so it fits the 65-character row). `.gitignore:3:/secrets`
    underlines YELLOW; CODE(transcribe_audio/.gitignore: 3) top right. The terminal shrinks to the
    strip (the check-ignore rows stay) as V6 returns; the .gitignore sieve lowers over the book; the
    folder pours into the book and the key stays on the sieve.
 2  The strip clears (the check-ignore rows go together, so no continuation row is left alone);
    `docker build -t transcribe_audio .` (extra here; title "laptop · the same build, full log")
    -> 21-g1 lines 30-31, COPY underlined TEAL. The folder pours into the box with no sieve: the key
    lands in the COPY slab, which turns RED. The box parks top right, the terminal grows to 7 rows:
    `docker run --rm --entrypoint ls transcribe_audio -la /app/secrets` (extra) -> 22-g1 lines 2-6,
    with a GREY note top left "--entrypoint ls runs ls instead of the image's /bin/bash / -la
    /app/secrets are the arguments to ls" (Dockerfile line 29); the listing scrolls the build log
    out and the title back to "laptop". Line 6's name RED + underline; GREY caption "stand-in: 82
    bytes · yours shows your key's real size" above the terminal ("82" underlined GREY). RED tag
    "every image you built today" beside the box (the note goes); on "step 2 came before step 5"
    the tracker's dots 2 and 5 flash and its caption reads "step 2: Key in secrets · before step
    5: Build image", then returns.
 3  The terminal shrinks to the strip (line 6 + the prompt) as the box glides home; the folder and
    the book return. Caption "Docker doesn't read .gitignore" (the .gitignore sieve pulses GREY).
    Lecture 2's parcel replays small: the folder's files, then the key ("key included"), pack into a
    "build context" parcel. On "the copy line unpacks": PANEL transcribe_audio/Dockerfile line 26
    (`COPY --chown=app:app . ./`, TEAL bar; "from transcribe_audio/README.md / lines 41–90" on two
    rows under the panel's right end) top right, the parcel moves into the box and unpacks into the COPY slab, and a RED arrow runs from
    the panel to `mega-pipeline.json` (RED flash). Then the panel goes: a GREY README card
    `README.md · lines 103–106` + `erratum`: "we’ve already added a .gitignore entry / so the file
    won’t be pushed accidentally" -> caption "about Git only · says nothing about the image" (the
    book pulses, the box flashes RED).
 4  The fix. `cat .dockerignore` (tag "extra · recommended") -> 23-g1 line 2. The .dockerignore sieve
    lowers over the box; a GREY note bottom right "create it in VS Code: a file named .dockerignore /
    one line secrets/ · in all five component folders"; `secrets/` pulses; ▶ your turn, "in all
    five component folders" underlines YELLOW. At the end the box parks and the terminal grows to 7
    rows (cleared) for the rebuild.
 5  The COPY slab clears (the rebuild). `docker build -t transcribe_audio .` (full log) ->
    24-g1 lines 12-13, …, 30-31; `49B` gets a GREEN bar and the GREY tag ".dockerignore: was 2B,
    now a file". The box fades and the terminal grows to 10 rows (the build and its log stay):
    `docker run --rm --entrypoint ls transcribe_audio -la /app/secrets` (extra) -> 25-g1 line 2,
    GREEN. The log leaves (title back to "laptop"), the terminal shrinks to the strip as V6 returns
    with the box at home; on "The key stayed out" the folder pours in again: the key stays on the
    .dockerignore sieve; GREEN check beside the clean COPY slab.
 6  V3 (common.Window, key=True; the image's /app holds cli.py, Dockerfile, pyproject.toml, no
    secrets/): the command shown in a chip, `docker run --rm -ti -v "$(pwd):/app" transcribe_audio`;
    the mount brings the laptop sheet (secrets/ with its GOLD key) over /app; the PINK signpost
    GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json at /app finds the key (PINK arrow).
 7  The tracker switches: "README › Push to Docker Hub" + tag "optional"; a GREY README card
    `transcribe_audio/README.md · lines 136–140` (heading, first bullet highlighted on "create an
    access token") holding three command chips (shown, not typed), each appearing with H1, H2, H3.
    Under it the image box (key inside, RED slab) slides toward the Docker Hub shelf and stops under
    a RED stamp "without .dockerignore: would publish the key"; beside it a GREEN tag "only after
    the .dockerignore fix".
 8  The box, shelf and stamp go. A GREEN chip `docker login -u <USER NAME>` + "paste the token at
    the prompt"; `-p <ACCESS TOKEN>` in the login chip underlines YELLOW with the GREY note "stays in
    your shell history"; a RED card "pushed one with the key? delete it · tell the staff".
 9  Coda (the tracker leaves: not a README step). CODE(solution-branch/transcribe_audio/
    docker-shell.sh: 8–10) top, caption "last year's solution branch: not today's steps"; below, a
    small picture: the laptop (the transcribe_audio/ folder with secrets/ and the key) and a TEAL
    container (/app, /secrets), one PINK route folder -> /app. Line 9 highlights and secrets/ slides
    out of the repo folder, below it ("outside the repo"); the panel becomes lines 95–100, line 98
    highlights and a second PINK route runs from secrets/ to /secrets. GREEN "image: no key" with a
    check. Fade out: empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import box, cell_width, check_mark, label, line_bar, mono, substring, tag
from explainer.scene import VoiceScene

from common import (CTR, ERR, INK, KEY, LAPTOP, LOOKUP, NARRATION, P_A, SYSTEM, TURN, VENV, Window,
                    TwoFilters, _save_op, _set_op, asset_lines, beside, capture, caption_extra, cmd_chip, erratum_tag,
                    file_panel, file_row, hub_shelf, key_glyph, optional_tag, p_comp, parcel_glyph, pin, resize,
                    sans, ship_box, signpost, source_text, src_panel, standin_tag, stamp, strip_top,
                    switch_section, term, tracker, your_turn)

SAY = NARRATION["S14"]

# ------------------------------------------------------------------ commands and real outputs
P_SYN = p_comp("synthesis_audio")
CD = "cd ../transcribe_audio"

G1 = capture("20-g1-git-ignores-key")
assert G1.cmd == "ls secrets; git status --short; git check-ignore -v secrets/mega-pipeline.json", G1.cmd
LS_S, GST, GCI = G1.cmd.split("; ")                    # typed as three commands (script conventions)
LS_OUT, GST_OUT = G1.at(2), G1.at(3)
assert LS_OUT == ["mega-pipeline.json"] and GST_OUT == [" M cli.py"], (LS_OUT, GST_OUT)
_gci = G1.line(4)
assert _gci == "transcribe_audio/.gitignore:3:/secrets\tsecrets/mega-pipeline.json", _gci
GCI_OUT = [_gci.replace("\t", " ")]                    # the tab as one space: 65 characters, one row
assert len(GCI_OUT[0]) == 65

BUILD = "docker build -t transcribe_audio ."           # README :95 names the image; never --network host
B1 = capture("21-g1-rebuild-with-key")
assert B1.cmd == "docker build --network host -t transcribe_audio .", B1.cmd
B1_OUT = B1.at((30, 31))
assert B1_OUT == ["#8 [4/5] COPY --chown=app:app . ./", "#8 DONE 0.0s"], B1_OUT

KIN = capture("22-g1-key-in-image")
RUN_LS = KIN.cmd
assert RUN_LS == "docker run --rm --entrypoint ls transcribe_audio -la /app/secrets", RUN_LS
KIN_OUT = KIN.at((2, 6))
assert KIN_OUT[0] == "total 12" and KIN_OUT[-1].endswith(" 82 Oct 13 01:47 mega-pipeline.json"), KIN_OUT

DI = capture("23-g1-dockerignore")
CAT = DI.cmd
assert CAT == "cat .dockerignore" and DI.at(2) == ["secrets/"], (CAT, DI.lines)
DI_OUT = DI.at(2)

B2 = capture("24-g1-rebuild-dockerignore")
assert B2.cmd == B1.cmd, B2.cmd
B2_OUT = B2.at((12, 13), "…", (30, 31))
assert B2_OUT[1] == "#3 transferring context: 49B done" and B2_OUT[3] == B1_OUT[0], B2_OUT
assert B1.line(13) == "#3 transferring context: 2B done"          # "was 2B"

NOK = capture("25-g1-key-not-in-image")
assert NOK.cmd == RUN_LS, NOK.cmd
NOK_OUT = NOK.at(2)
assert NOK_OUT == ["ls: cannot access '/app/secrets': No such file or directory"], NOK_OUT

# the student's Dockerfile, line 26 (the README's piece, lines 41-90)
DF = "files/transcribe_audio.Dockerfile"
assert asset_lines(DF, 26, 26) == "COPY --chown=app:app . ./"

# README.md:103-106 (the secrets note) and transcribe_audio/README.md:136-140 (the optional push)
_R = source_text("README.md").split("\n")
assert _R[102].startswith("### ") and "Important Note on Secrets" in _R[102], _R[102]
NOTE_Q = ["we’ve already added a .gitignore entry", "so the file won’t be pushed accidentally"]
assert "we’ve already added a `.gitignore` entry so the file won’t be pushed accidentally" in _R[105], _R[105]
_RA = source_text("transcribe_audio/README.md").split("\n")
HUB_HEAD = _RA[135].lstrip("# ")
assert HUB_HEAD == "OPTIONAL: Push Container to Docker Hub", _RA[135]
HUB_B1 = "Sign up in Docker Hub and create an Access Token"
assert _RA[136].startswith("* " + HUB_B1.replace("an Access Token", "an [Access Token]")), _RA[136]
LOGIN = "docker login -u <USER NAME> -p <ACCESS TOKEN>"
TAGC = "docker tag transcribe_audio <USER NAME>/transcribe_audio"
PUSH = "docker push <USER NAME>/transcribe_audio"
for _n, _c in ((137, LOGIN), (138, TAGC), (139, PUSH)):
    assert f"`{_c}`" in _RA[_n], _RA[_n]
LOGIN_U = "docker login -u <USER NAME>"

RUN_V = 'docker run --rm -ti -v "$(pwd):/app" transcribe_audio'
assert RUN_V == capture("01-docker-run-tty", "transcribe_audio").cmd and _RA[98] == RUN_V

SOL = "solution-branch/transcribe_audio/docker-shell.sh"
_SOL = source_text(SOL).split("\n")
assert _SOL[8] == "export SECRETS_DIR=$(pwd)/../../secrets/" and '-v "$SECRETS_DIR":/secrets' in _SOL[97], _SOL[97]

assert source_text("transcribe_audio/.gitignore").split("\n")[2] == "/secrets"

PONDER_Q = "Your key is git-ignored.\nYou build the image and push it to Docker Hub.\nIs the key inside?"

# ------------------------------------------------------------------ layout
EDGE = 6.45
TRACK_BOTTOM = 2.917               # the tracker band is y 2.92..3.5
STRIP, PARKED = 4, 7               # terminal rows: the strip under V6; 7 rows with the box parked
TALL = 10                          # beat 1's four extras, beat 5's build + run: V6 steps aside
ST4, ST7, ST10 = strip_top(STRIP), strip_top(PARKED), strip_top(TALL)
FOLDER_L, FOLDER_T = -6.45, 2.3    # V6 HOME: the folder frame's left and top (frame 3.3 x 2.3)
FOLDER_W, FOLDER_H = 3.3, 2.3
BOOK_X, BOOK_T = -1.3, 2.3         # the book's centre x and top (its sieve's name ends over the folder)
CRATE_FX, CRATE_B = 3.1, ST4 + 0.14  # the box's front centre x and its bottom (caption) y
PARK_FX, PARK_B = 4.35, ST7 + 0.16  # the parked box: front centre x, bottom y
PONDER_UP = 0.4                    # beat 0: V6 sits this much higher (no tracker, the card under it)
PANEL_TOP = 2.78                   # panels and cards go top right: x up to EDGE, y down to ~1.0


# ------------------------------------------------------------------ small helpers
def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cx is not None:
        m.set_x(cx)
    if cy is not None:
        m.set_y(cy)
    return m


def make_room(scene, t, n: int, extra=()):
    """Room for n new rows: the oldest rows fade where they are, then the rest move up (Terminal's own
    scroll slides them over the title bar). `extra`: animations played as the old rows fade."""
    over = min(max(len(t.lines) + n - t.rows, 0), len(t.lines))
    if over <= 0:
        if extra:
            scene.play(*extra, run_time=0.25)
        return
    gone = t.lines.submobjects[:over]
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(VGroup(*gone)), *extra, run_time=0.25 if extra else 0.2)
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=0.25)


def n_rows(t, cmd: str) -> int:
    p = t.prompt + ("" if t.prompt.endswith(" ") else " ")
    return len(t.fold(p + cmd, first_prefix=len(p)))


def type_in(scene, t, cmd: str, type_time: float):
    """Type at the prompt (replacing a waiting bare prompt), scrolling the house way first."""
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    make_room(scene, t, n_rows(t, cmd))
    return t.type(scene, cmd, type_time)


def print_in(scene, t, lines, run_time: float = 0.3, color=None, extra=()):
    make_room(scene, t, len(lines), extra=extra)
    kw = {} if color is None else {"color": color}
    return t.print(scene, lines, run_time=run_time, lag=0.12, **kw)


def bare(scene, t):
    """The prompt returns (no output)."""
    make_room(scene, t, 1)
    ln = t.type(scene, "", type_time=0)
    ln.bare = True
    return ln


def seed(t, text: str):
    """A bare prompt line on t, without animation (the terminal fades in with it)."""
    from explainer.devops import mono_line
    ln = mono_line(text, t.size, INK, t2c=t._prompt_colors(t.prompt))
    t._place(ln, len(t.lines))
    t.lines.add(ln)
    ln.bare = True
    return ln


def last_row(line):
    return line.rows[-1] if hasattr(line, "rows") else line


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded)."""
    row = last_row(line)
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def uline(line, sub, color, stroke=3.5, pad=0.02) -> Line:
    """A Line under substring `sub` of terminal row `line`, in the gap under the row."""
    g = substring(line, sub)
    y = line.strut.get_bottom()[1] + 0.01
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color, stroke_width=stroke)


def sbar(line, sub, color, opacity=0.3) -> Rectangle:
    """A translucent bar over substring `sub` of a terminal row."""
    g = substring(line, sub)
    return Rectangle(width=g.width + 0.14, height=line.strut.height * 0.95, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def xtag(t, line, text: str = "extra"):
    """The GREY tag beside a typed command (its last row when folded)."""
    return beside(tag(text, S.GREY, size=20), t, line)


def retitle(t, s: str):
    return Transform(t.title, mono(s, 20, S.GREY).move_to(t.box.get_top() + DOWN * t.bar_h / 2))


def gray_line(*parts, size: float = 20, color=S.GREY) -> VGroup:
    """A caption row: plain strings in serif, 1-tuples in mono (same colour)."""
    ms = [mono(p[0], size, color) if isinstance(p, tuple) else label(p, size, color) for p in parts]
    g = VGroup(*ms).arrange(RIGHT, buff=0.12)
    for m in ms[1:]:
        m.align_to(ms[0], DOWN)
    return g


def compact_ponder(question: str, width: float = 11.0, size: float = 24) -> VGroup:
    """pause_and_ponder's card (frame, header, question, timer bar) with less padding."""
    card = ponder_card(question, width=width, size=size)
    fr, head, q, bar = card
    body = VGroup(head, q).arrange(DOWN, buff=0.14)
    fr.become(RoundedRectangle(width=width, height=body.height + 0.55, corner_radius=0.2,
                               stroke_color=TURN, stroke_width=3).set_fill(S.BG, 0.96))
    body.move_to(fr).shift(UP * 0.09)
    bar.become(Line(fr.get_corner(DL) + RIGHT * 0.3 + UP * 0.17, fr.get_corner(DR) + LEFT * 0.3 + UP * 0.17,
                    color=TURN, stroke_width=4))
    return card


def scale_opacity(m, k: float):
    """Every member's fill and stroke opacity times k (a chip shown dimmed before it is named)."""
    for f in m.get_family():
        if isinstance(f, VMobject):
            f.set_fill(opacity=f.get_fill_opacity() * k, family=False)
            f.set_stroke(opacity=f.get_stroke_opacity() * k, family=False)
    return m


def chip_span(c, s: str, sub: str) -> tuple[float, float]:
    """x range of `sub` inside cmd_chip c (mono text `s`)."""
    cw = cell_width(20)
    i = s.index(sub)
    x0 = c.text.get_left()[0] + (c.text.width - len(s) * cw) / 2
    return x0 + i * cw, x0 + (i + len(sub)) * cw


# ------------------------------------------------------------------ V6, laid out for this scene
def make_v6() -> TwoFilters:
    """V6 at HOME (above the 3-row strip) with a small layer stack inside the box's front (ORANGE base,
    the GREY COPY slab, GREEN venv) and the folder, book, box and shelf registered as parts."""
    v6 = TwoFilters()
    f = v6.folder                          # a lower folder frame (3.3 x 2.3) so V6 fits above the strip
    fr0, title, rows, key, cap = f.submobjects
    fr0.become(box(FOLDER_W, FOLDER_H, LAPTOP, fill_opacity=0.05).move_to(fr0, aligned_edge=UL))
    title.move_to(fr0.get_corner(UL) + np.array([0.15, -0.26, 0]), aligned_edge=LEFT)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.09)
    rows.next_to(title, DOWN, buff=0.17, aligned_edge=LEFT).shift(RIGHT * 0.05)
    key.next_to([r for r in rows if r.name == "secrets/"][0], RIGHT, buff=0.15)
    cap.next_to(fr0, DOWN, buff=0.1)
    f.shift(np.array([FOLDER_L - f.frame.get_left()[0], FOLDER_T - f.frame.get_top()[1], 0]))
    bk = VGroup(*v6.book[:3])
    v6.book.shift(np.array([BOOK_X - bk.get_center()[0], BOOK_T - v6.book.get_top()[1], 0]))
    v6.crate.shift(np.array([CRATE_FX - v6.crate.front.get_center()[0], CRATE_B - v6.crate.get_bottom()[1], 0]))
    v6.hub.shift(np.array([EDGE - v6.hub.get_right()[0], CRATE_B - v6.hub.get_bottom()[1], 0]))
    v6._place_sieve("git")
    v6._place_sieve("image")
    fr = v6.crate.front
    w = fr.width - 0.16
    base = box(w, 0.24, SYSTEM, fill_opacity=0.25, radius=0.04, stroke=2)
    copy = box(w, 0.34, LAPTOP, fill_opacity=0.18, radius=0.05, stroke=2)
    sync = box(w, 0.16, VENV, fill_opacity=0.25, radius=0.04, stroke=2)
    stack = VGroup(base, copy, sync).arrange(UP, buff=0.05)
    stack.move_to(fr).align_to(fr, DOWN).shift(UP * 0.08)
    lab = sans("COPY", 20, INK).move_to(copy).align_to(copy, LEFT).shift(RIGHT * 0.1)
    v6.crate.add(stack, lab)
    v6.slab, v6.slab_label = copy, lab
    v6.key_spot = np.array([copy.get_right()[0] - 0.3, copy.get_center()[1], 0])
    for name, m in (("folder", v6.folder), ("book", v6.book), ("hub", v6.hub), ("crate", v6.crate)):
        v6.parts[name] = m
        m.hidden = False
    return v6


def crate_group(v6) -> list:
    """What moves when the box moves: the box and its sieve (hidden or not)."""
    return [v6.crate, v6.sieves["image"]]


def park_shift(v6):
    return np.array([PARK_FX - v6.crate.front.get_center()[0], PARK_B - v6.crate.get_bottom()[1], 0])


def home_shift(v6):
    return np.array([CRATE_FX - v6.crate.front.get_center()[0], CRATE_B - v6.crate.get_bottom()[1], 0])


def hide_anims(v6, *names) -> list:
    """Piece.hide's fades, unplayed, so they go with the terminal's resize (parts flagged hidden)."""
    mobs = [v6.parts[n] for n in names if not getattr(v6.parts[n], "hidden", False)]
    for m in mobs:
        _save_op(m)
        v6._flag(m, True)
    return [m.animate.set_opacity(0) for m in mobs]


def reveal_anims(v6, *names) -> list:
    """Piece.reveal's fade-ins, unplayed. The parts get their opacity back at once: play these in
    the very next play() (resize() with no line left to fade first)."""
    mobs = [v6.parts[n] for n in names]
    for m in mobs:
        if getattr(m, "hidden", False):
            _set_op(m)
        v6._flag(m, False)
    return [FadeIn(m) for m in mobs]


def shrink_home(scene, t, v6, keep: list, names, extra=(), pre=(), run_time: float = 0.5):
    """Back to HOME in one move: the lines not in `keep` fade (with `pre`, e.g. the retitle), then
    the terminal shrinks to the strip while the named V6 parts fade in (with `extra`)."""
    gone = [ln for ln in t.lines.submobjects if ln not in keep]
    if gone or pre:
        scene.play(*([FadeOut(VGroup(*gone))] if gone else []), *pre, run_time=0.3)
        for ln in gone:
            t.lines.remove(ln)
            scene.remove(ln)
    resize(scene, t, STRIP, keep=list(keep), run_time=run_time, extra=[*extra, *reveal_anims(v6, *names)])


def pour_image(scene, v6, caught: bool, run_time: float = 1.3, extra=()):
    """The build context pours into the box: copies of the folder's files fly into the COPY slab and
    vanish into it; the key lands in the slab (it stays: returns it) or, with the .dockerignore sieve
    lowered, on the sieve (it becomes part of the sieve). `extra`: animations played with it."""
    files = VGroup(*[r.glyph.copy() for r in v6.folder.rows])
    k = v6.key.copy()
    dest = v6.slab.get_center()
    scene.add(files, k)
    lag = LaggedStart(*[f.animate.move_to(dest).scale(0.5).set_opacity(0) for f in files], lag_ratio=0.12)
    if caught:
        k_dest = v6.sieves["image"].bowl.get_center() + UP * 0.12
        scene.play(lag, k.animate.move_to(k_dest), *extra, run_time=run_time)
    else:
        k_tgt = k.copy().scale_to_fit_height(0.2).move_to(v6.key_spot)
        scene.play(lag, Transform(k, k_tgt), *extra, run_time=run_time)
    scene.remove(files)
    for a in (lag,):
        if a.group in scene.mobjects:
            scene.remove(a.group)
    scene.remove(k)
    (v6.sieves["image"] if caught else v6.crate).add(k)
    return k


# ------------------------------------------------------------------ the coda picture
def coda_picture() -> VGroup:
    """The laptop (transcribe_audio/ with cli.py, Dockerfile, secrets/ + key; below it an empty
    "outside the repo" folder for the moved secrets/) and a TEAL container with /app and a dashed
    /secrets; route 1 laptop -> /app. .rows .sec_row .key .out (frame + caption) .slot (where the row
    lands) .secs .r2 .img (GREEN "image: no key", top right of the container)"""
    lap = box(5.3, 2.75, LAPTOP, fill_opacity=0.04)
    place(lap, left=-6.4, top=-0.3)
    lap_cap = label("your laptop", 20, LAPTOP).next_to(lap, DOWN, buff=0.08)
    repo = box(3.3, 1.45, LAPTOP, fill_opacity=0.08)
    place(repo, left=lap.get_left()[0] + 0.2, top=lap.get_top()[1] - 0.15)
    rt = mono("transcribe_audio/", 20, LAPTOP)
    place(rt, left=repo.get_left()[0] + 0.15, top=repo.get_top()[1] - 0.1)
    rows = VGroup(file_row("cli.py"), file_row("Dockerfile"), file_row("secrets/"))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    place(rows, left=repo.get_left()[0] + 0.25, top=rt.get_bottom()[1] - 0.1)
    sec = rows[2]
    k = key_glyph(0.2).next_to(sec, RIGHT, buff=0.15)
    sec_row = VGroup(sec, k)
    out = box(3.3, 0.92, LAPTOP, fill_opacity=0.08)
    place(out, left=repo.get_left()[0], top=repo.get_bottom()[1] - 0.18)
    out_cap = label("outside the repo", 20, S.GREY)
    place(out_cap, left=out.get_left()[0] + 0.15, top=out.get_top()[1] - 0.08)
    slot = np.array([out.get_left()[0] + 0.25, out.get_bottom()[1] + 0.25, 0])
    ctr = box(4.9, 2.75, CTR, fill_opacity=0.06)
    place(ctr, right=6.4, top=-0.3)
    ctr_t = sans("container", 20, CTR)
    place(ctr_t, left=ctr.get_left()[0] + 0.15, top=ctr.get_top()[1] - 0.1)
    app = box(2.6, 0.6, LAPTOP, fill=S.BG, fill_opacity=1)
    place(app, left=ctr.get_left()[0] + 0.3, cy=repo.get_center()[1] - 0.05)
    app_t = mono("/app", 20, INK).move_to(app)
    secs = box(2.6, 0.6, LAPTOP, fill=S.BG, fill_opacity=1, dashed=True)
    place(secs, left=app.get_left()[0], cy=slot[1])
    secs_t = mono("/secrets", 20, INK).move_to(secs)
    img = VGroup(label("image: no key", 20, VENV), check_mark(0.22, VENV)).arrange(RIGHT, buff=0.12)
    place(img, right=ctr.get_right()[0] - 0.2, top=ctr.get_top()[1] - 0.12)
    r1 = Line(repo.get_right() + RIGHT * 0.1, app.get_left() + LEFT * 0.1, color=LOOKUP, stroke_width=5)
    r2 = Line(np.array([out.get_right()[0] + 0.1, slot[1], 0]), secs.get_left() + LEFT * 0.1,
              color=LOOKUP, stroke_width=5)
    g = VGroup(lap, lap_cap, repo, rt, rows[0], rows[1], sec_row, ctr, ctr_t, app, app_t, secs, secs_t, r1)
    g.rows, g.sec_row, g.key, g.slot = rows, sec_row, k, slot
    g.out, g.out_cap, g.secs, g.r2, g.img = VGroup(out, out_cap), out_cap, VGroup(secs, secs_t), r2, img
    return g


# ------------------------------------------------------------------ the scene
class KeepTheKeyOut(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, f"S14 has {len(SAY)} SAY lines; this scene times 10"

        v6 = make_v6()
        self._check_home(v6)

        # ========================================================== 0 · the question (no tracker)
        v6.shift(UP * PONDER_UP)
        card = compact_ponder(PONDER_Q)
        place(card, cx=0, bottom=-3.5)
        assert card.get_top()[1] < CRATE_B + PONDER_UP - 0.1, card.get_top()
        qm = sans("?", 34, TURN, weight="BOLD").move_to(v6.key_spot + UP * PONDER_UP)   # key_spot is HOME
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(v6, shift=UP * 0.1), run_time=0.8)
            self.play(Indicate(v6.key, color=KEY, scale_factor=1.5), run_time=0.9)
            vo.wait_until("It's git-ignored")
            self.play(Indicate(v6.book, color=INK, scale_factor=1.1), run_time=0.9)
            vo.wait_until("But you build the image")
            self.play(Indicate(v6.crate, color=CTR, scale_factor=1.08), run_time=0.9)
            vo.wait_until("and push it to Docker Hub")
            self.play(Indicate(v6.hub, color=INK, scale_factor=1.08), run_time=0.8)
            vo.wait_until("is the key inside")
            self.play(FadeIn(qm, scale=1.6), run_time=0.5)
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 1 · Git ignores it (extras)
        tr = tracker("A", 13)
        t = term(P_SYN, STRIP)
        seed(t, P_SYN + " ")
        st = standin_tag()             # under "your laptop" at HOME (V6 is still raised for the ponder here)
        place(st, left=FOLDER_L, top=v6.folder.get_bottom()[1] - PONDER_UP - 0.08)
        assert st.get_bottom()[1] > ST4 + 0.08, st.get_bottom()
        gi = src_panel("transcribe_audio/.gitignore", 3, 3)
        place(gi, right=EDGE, top=PANEL_TOP + 0.05)       # it appears over the 10-row terminal
        assert gi.get_left()[0] > v6.sieves["git"].get_right()[0] + 0.1 and gi.get_bottom()[1] > v6.crate.get_top()[1] - PONDER_UP + 0.3
        assert gi.get_bottom()[1] > ST10 + 0.15 and gi.get_top()[1] < TRACK_BOTTOM - 0.05, gi.get_corner(DL)
        with self.voiceover(SAY[1]) as vo:
            v6.hide(self, "hub", run_time=0.4, extra=[FadeOut(card), FadeOut(qm)])
            self.play(v6.animate.shift(DOWN * PONDER_UP), FadeIn(tr, shift=DOWN * 0.1), FadeIn(t, shift=UP * 0.1),
                      run_time=0.7)
            self.play(caption_extra(tr), run_time=0.3)
            vo.wait_until("with an 82 byte stand-in")
            v6.attach(self, st, anims=[FadeIn(st, shift=DOWN * 0.1)], run_time=0.4, into=v6.folder,
                      extra=[Indicate(v6.key, color=KEY, scale_factor=1.4)])
            c_cd = type_in(self, t, CD, 0.7)
            pin(self, c_cd, xtag(t, c_cd), run_time=0.25)
            t.set_prompt(P_A)
            bare(self, t)
            # four extras with their outputs take 10 rows: V6 steps aside so all of them stay in view
            resize(self, t, TALL, run_time=0.5, extra=hide_anims(v6, "folder", "book", "crate"))
            c_ls = type_in(self, t, LS_S, 0.35)
            print_in(self, t, LS_OUT, 0.2)
            pin(self, c_ls, xtag(t, c_ls), run_time=0.2)
            vo.wait_until("These extra Git commands")
            c_gs = type_in(self, t, GST, 0.45)
            print_in(self, t, GST_OUT, 0.2)
            pin(self, c_gs, xtag(t, c_gs), run_time=0.2)
            c_ci = type_in(self, t, GCI, 0.9)
            o_ci = print_in(self, t, GCI_OUT, 0.2)
            pin(self, c_ci, xtag(t, c_ci), run_time=0.2)
            assert len(t.lines) == TALL, len(t.lines)          # nothing scrolled: the cd is still on screen
            vo.wait_until("by line 3 of dot gitignore")
            u_ci = uline(o_ci[0], ".gitignore:3:/secrets", TURN)
            self.play(Create(u_ci), FadeIn(gi, shift=UP * 0.1), run_time=0.4)
            stick(self, o_ci[0], u_ci)
            # back to the strip (the check-ignore rows stay) as V6 returns for the payoff
            shrink_home(self, t, v6, [*c_ci.rows, o_ci[0]], ("folder", "book", "crate"))
            v6.lower(self, "git", run_time=0.5)
            v6.pour(self, "git", run_time=1.3)
            # the panel goes with the payoff, so beat 2 starts on the build
            self.play(Indicate(v6.sieves["git"], color=INK, scale_factor=1.06), FadeOut(gi), run_time=0.6)

        # ========================================================== 2 · the key is in the image
        cap82 = gray_line("stand-in: 82 bytes · yours shows your key's real size")
        place(cap82, left=-6.3, bottom=ST7 + 0.12)
        # why --entrypoint: the image's ENTRYPOINT is /bin/bash (a plain `... transcribe_audio ls` fails)
        ep = VGroup(gray_line(("--entrypoint ls",), "runs ls instead of the image's", ("/bin/bash",)),
                    gray_line(("-la /app/secrets",), "are the arguments to ls"))
        ep.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        place(ep, left=-6.3, top=TRACK_BOTTOM - 0.3)
        assert asset_lines("files/transcribe_audio.Dockerfile", 29, 29) == 'ENTRYPOINT ["/bin/bash"]'
        with self.voiceover(SAY[2]) as vo:
            # the check-ignore rows leave together: a one-row scroll would leave its continuation
            # row ("check-ignore -v ...") on top without the prompt row that starts it
            t.clear(self, run_time=0.25)
            c_b = type_in(self, t, BUILD, 0.6)
            x_b = xtag(t, c_b, "extra here")
            pin(self, c_b, x_b, run_time=0.3,
                anim=AnimationGroup(FadeIn(x_b, shift=LEFT * 0.1), retitle(t, "laptop · the same build, full log")))
            o_b = print_in(self, t, B1_OUT, 0.3)
            # COPY underlines TEAL as the build context pours into the box (no sieve: the key lands)
            u_cp = uline(o_b[0], "COPY --chown=app:app . ./", CTR)
            k_in = pour_image(self, v6, caught=False, run_time=1.1,
                              extra=[Create(u_cp, rate_func=lambda a: smooth(min(1.0, 3 * a)))])
            stick(self, o_b[0], u_cp)
            self.play(v6.slab.animate.set_stroke(ERR, 3), Indicate(k_in, color=ERR, scale_factor=1.6), run_time=0.5)
            # the box parks top right; the terminal grows to 7 rows (the build log stays: so does the title)
            v6.hide(self, "folder", "book", "sieve_git", run_time=0.5,
                    extra=[m.animate.shift(park_shift(v6)) for m in crate_group(v6)])
            resize(self, t, PARKED, run_time=0.5)
            c_r = type_in(self, t, RUN_LS, 0.7)
            x_r = xtag(t, c_r)
            assert ep.get_right()[0] < v6.crate.get_left()[0] - 0.3 and ep.get_bottom()[1] > ST7 + 0.6, ep.get_corner(DR)
            pin(self, c_r, x_r, run_time=0.4, anim=AnimationGroup(FadeIn(x_r, shift=LEFT * 0.1),
                                                                   FadeIn(ep, shift=DOWN * 0.1)))
            vo.wait_until("There it is")
            # the listing pushes the build log out: the title goes back to "laptop" with it
            o_r = print_in(self, t, KIN_OUT, 0.4, extra=[retitle(t, "laptop")])
            l6 = o_r[-1]
            nm = substring(l6, "mega-pipeline.json")
            u6 = uline(l6, "mega-pipeline.json", ERR, stroke=4)
            self.play(nm.animate.set_color(ERR), Create(u6), run_time=0.4)
            stick(self, l6, u6)
            u82 = uline(l6, "82", S.GREY)
            self.play(FadeIn(cap82, shift=UP * 0.1), Create(u82), run_time=0.5)
            stick(self, l6, u82)
            self.play(Indicate(nm, color=ERR, scale_factor=1.15), Indicate(k_in, color=ERR, scale_factor=1.6),
                      run_time=0.8)
            vo.wait_until("Your real key is in every image")
            every = tag("every image you built today", ERR, size=20)
            place(every, right=v6.crate.get_left()[0] - 0.25, cy=v6.crate.front.get_center()[1])
            assert every.get_top()[1] < ep.get_bottom()[1] - 0.2, (every.get_top(), ep.get_bottom())
            self.play(FadeIn(every, shift=RIGHT * 0.15), v6.slab.animate.set_fill(ERR, 0.25), FadeOut(ep),
                      run_time=0.5)
            vo.wait_until("because step 2 came before")
            alt = label("step 2: Key in secrets · before step 5: Build image", tr.size, TURN)
            alt.next_to(tr.dots, RIGHT, buff=0.25)
            self.play(Transform(tr.caption, alt), Indicate(tr.dots[1], color=TURN, scale_factor=2.2),
                      run_time=0.6)
            self.play(Indicate(tr.dots[4], color=TURN, scale_factor=2.2), run_time=0.6)

        # ========================================================== 3 · Docker doesn't read .gitignore
        p26 = file_panel(DF, 26, 26, "transcribe_audio/Dockerfile")
        place(p26, right=EDGE, top=PANEL_TOP)
        # the provenance on two short rows under the panel's right end, well clear of "Git history"
        src26 = VGroup(gray_line("from", ("transcribe_audio/README.md",)), label("lines 41–90", 20, S.GREY))
        src26.arrange(DOWN, aligned_edge=RIGHT, buff=0.08)
        place(src26, right=EDGE - 0.05, top=p26.get_bottom()[1] - 0.08)
        assert src26.get_left()[0] > v6.book.get_right()[0] + 0.6, src26.get_left()      # the book with its caption
        assert src26.get_bottom()[1] > v6.crate.get_top()[1] + home_shift(v6)[1] + 0.05, src26.get_bottom()
        nogit = sans("Docker doesn't read .gitignore", 22, INK)
        place(nogit, left=v6.folder.frame.get_right()[0] + 0.25, top=v6.book.get_bottom()[1] - 0.12)
        parcel = parcel_glyph(0.62)
        place(parcel, cx=-1.1, bottom=ST4 + 0.14)
        assert parcel.get_top()[1] < nogit.get_bottom()[1] - 0.1, (parcel.get_top(), nogit.get_bottom())
        hs = home_shift(v6)                # the box is parked now: check against its home place
        assert parcel.get_bottom()[1] > ST4 + 0.1 and parcel.get_right()[0] < v6.crate.get_left()[0] + hs[0] - 0.3
        rc = self._note_card()
        place(rc, right=EDGE, top=PANEL_TOP + 0.06)    # its erratum pill sits right of the tracker band
        assert rc.get_left()[0] > tr.get_right()[0] + 0.3 or rc.get_top()[1] < TRACK_BOTTOM, rc.get_left()
        git_only = label("about Git only · says nothing about the image", 20, S.GREY)
        place(git_only, right=EDGE, top=rc.get_bottom()[1] - 0.12)
        assert git_only.get_bottom()[1] > v6.crate.get_top()[1] + hs[1] + 0.1, git_only.get_bottom()   # its sieve is hidden here
        bar26 = line_bar(p26.code, 0, CTR, 0.22)
        with self.voiceover(SAY[3]) as vo:
            # one move back to HOME: the strip (line 6 + the prompt), the box glides home, V6 returns
            self.play(FadeOut(VGroup(cap82, every)), run_time=0.3)
            resize(self, t, STRIP, keep=[l6], run_time=0.5,
                   extra=[caption_extra(tr), *[m.animate.shift(home_shift(v6)) for m in crate_group(v6)]])
            bare(self, t)
            v6.reveal(self, "folder", "book", "sieve_git", run_time=0.5)
            assert nogit.get_top()[1] < v6.book.get_bottom()[1] - 0.05, (nogit.get_top(), v6.book.get_bottom())
            # "Docker doesn't read dot gitignore": the caption, the .gitignore sieve pulses GREY
            self.play(Write(nogit), Indicate(v6.sieves["git"], color=S.GREY, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Remember lecture 2's parcel")
            self.play(FadeIn(parcel, scale=0.8), run_time=0.5)
            vo.wait_until("the build context is the whole folder")
            files = VGroup(*[r.glyph.copy() for r in v6.folder.rows])
            self.add(files)
            self.play(LaggedStart(*[f.animate.move_to(parcel.frame).scale(0.4).set_opacity(0) for f in files],
                                  lag_ratio=0.15), run_time=1.2)
            self.remove(files)
            vo.wait_until("key included")
            kc = v6.key.copy()
            self.add(kc)
            self.play(kc.animate.scale(0.6).move_to(parcel.frame), Indicate(v6.key, color=KEY, scale_factor=1.4),
                      run_time=0.7)
            self.remove(kc)
            parcel.add(kc)                 # the key rides in the parcel
            vo.wait_until("and the copy line unpacks")
            nm6 = substring(l6, "mega-pipeline.json")
            ax = nm6.get_left()[0] + 0.3
            assert p26.get_left()[0] < ax - 0.2 and ax < v6.crate.get_left()[0] - 0.3, (ax, p26.get_left())
            assert src26[0].get_left()[0] < ax < src26[1].get_left()[0] - 0.3, ax     # it starts under row 1
            assert ax > nogit.get_right()[0] + 0.3, (ax, nogit.get_right())
            arr = Arrow([ax, src26[0].get_bottom()[1] - 0.06, 0], [ax, l6.strut.get_top()[1] + 0.02, 0], buff=0,
                        color=ERR, stroke_width=5, max_tip_length_to_length_ratio=0.12)
            self.play(FadeIn(p26, shift=UP * 0.1), FadeIn(src26), run_time=0.4)
            self.play(FadeIn(bar26), run_time=0.25)
            self.play(parcel.animate.move_to(v6.slab).scale(0.35).set_opacity(0), run_time=0.8)
            self.remove(parcel)
            # the COPY line put mega-pipeline.json into the image
            self.play(GrowArrow(arr), Indicate(nm6, color=ERR, scale_factor=1.15),
                      Indicate(v6.slab, color=ERR, scale_factor=1.15), Indicate(k_in, color=ERR, scale_factor=1.6),
                      run_time=0.7)
            vo.wait_until("The README's secrets note")
            self.play(FadeOut(VGroup(p26, bar26, src26, nogit, arr)), run_time=0.4)
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(git_only, shift=UP * 0.1), Indicate(v6.book, color=INK, scale_factor=1.08), run_time=0.6)
            self.play(Indicate(v6.slab, color=ERR, scale_factor=1.15), run_time=0.6)

        # ========================================================== 4 · the fix: .dockerignore
        note = VGroup(gray_line("create it in VS Code: a file named", (".dockerignore",)),
                      gray_line("one line", ("secrets/",), "· in all five component folders"))
        note.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        place(note, right=EDGE, top=PANEL_TOP - 0.2)
        five = note[1][-1]
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(rc, git_only)), run_time=0.4)
            c_cat = type_in(self, t, CAT, 0.5)
            x_cat = xtag(t, c_cat, "extra · recommended")
            pin(self, c_cat, x_cat, run_time=0.3)
            o_cat = print_in(self, t, DI_OUT, 0.25)
            vo.wait_until("a file named dot dockerignore")
            v6.lower(self, "image", run_time=0.6)
            self.play(FadeIn(note[0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("with one line, secrets, slash")
            self.play(FadeIn(note[1], shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(o_cat[0].glyphs, color=INK, scale_factor=1.2),
                      Indicate(note[1][1], color=INK, scale_factor=1.2), run_time=0.7)
            vo.wait_until("All five images copied the key")
            self.play(Indicate(v6.slab, color=ERR, scale_factor=1.15), Indicate(k_in, color=ERR, scale_factor=1.6),
                      run_time=0.7)
            vo.wait_until("so pause and add it")
            yt = your_turn()
            yt.next_to(x_cat, RIGHT, buff=0.2).set_y(x_cat.get_center()[1])
            pin(self, c_cat, yt, run_time=0.3)
            u5 = Line(five.get_corner(DL) + DOWN * 0.06, five.get_corner(DR) + DOWN * 0.06, color=TURN, stroke_width=4)
            self.play(Create(u5), Wiggle(yt, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.8)
            self.wait(1.5)
            # ready for the rebuild: the box parks, the terminal grows to 7 rows (cleared)
            self.play(FadeOut(VGroup(note, u5)), run_time=0.3)
            v6.hide(self, "folder", "book", "sieve_git", run_time=0.5,
                    extra=[m.animate.shift(park_shift(v6)) for m in crate_group(v6)])
            t.clear(self, run_time=0.25)
            resize(self, t, PARKED, run_time=0.5)

        # ========================================================== 5 · rebuild: the key stays out
        tag49 = tag(".dockerignore: was 2B, now a file", S.GREY, size=20)
        chk = check_mark(0.26, VENV)
        with self.voiceover(SAY[5]) as vo:
            # the rebuild: the COPY slab clears; a G1 build's plain log, so the title says so
            self.play(FadeOut(k_in), v6.slab.animate.set_stroke(LAPTOP, 2).set_fill(LAPTOP, 0.18),
                      retitle(t, "laptop · the same build, full log"), run_time=0.3)
            v6.crate.remove(k_in)
            type_in(self, t, BUILD, 0.45)
            o_b2 = print_in(self, t, B2_OUT, 0.3)
            l13 = o_b2[1]
            assert l13.text == "#3 transferring context: 49B done" and o_b2[0].text == "#3 [internal] load .dockerignore"
            b49 = sbar(l13, "49B", VENV, 0.35)
            place(tag49, left=substring(l13, "done").get_right()[0] + 0.4, cy=l13.strut.get_center()[1])
            assert tag49.get_right()[0] < t.box.get_right()[0] - 0.12, tag49.get_right()
            self.play(FadeIn(b49), substring(l13, "49B").animate.set_color(VENV), FadeIn(tag49, shift=LEFT * 0.1),
                      run_time=0.45)
            stick(self, l13, b49, tag49)
            # "and list again": the box steps aside and the terminal grows to 10 rows, so the build, its
            # log (line 12 names the .dockerignore) and the run with its answer are all in view
            resize(self, t, TALL, run_time=0.45, extra=hide_anims(v6, "crate", "sieve_image"))
            c_r2 = type_in(self, t, RUN_LS, 0.5)
            o_n = print_in(self, t, NOK_OUT, 0.25, color=VENV)
            assert len(t.lines) == TALL, len(t.lines)          # nothing scrolled
            x_r2 = xtag(t, c_r2)
            pin(self, c_r2, x_r2, run_time=0.6,
                anim=AnimationGroup(FadeIn(x_r2, shift=LEFT * 0.1),
                                    Indicate(o_n[0].glyphs, color=VENV, scale_factor=1.05)))
            # the 10 rows hold until "The key stayed out": then back to HOME, the log leaves (the title
            # says "laptop" again), the strip keeps the run, V6 returns with the box at home, and the
            # folder pours in: the key stays on the .dockerignore sieve
            vo.wait_until("The key stayed out of the image")
            hs = home_shift(v6)
            for m in crate_group(v6):
                m.shift(hs)
            shrink_home(self, t, v6, [*c_r2.rows, o_n[0]], ("folder", "book", "sieve_git", "crate", "sieve_image"),
                        pre=[retitle(t, "laptop")])
            k_out = pour_image(self, v6, caught=True, run_time=1.0)
            chk.next_to(v6.crate.get_right(), RIGHT, buff=0.15).set_y(v6.slab.get_center()[1])
            self.play(Create(chk), v6.slab.animate.set_stroke(VENV, 3), Indicate(k_out, color=KEY, scale_factor=1.4),
                      run_time=0.6)

        # ========================================================== 6 · the run still works (V3)
        win = Window(files=("cli.py", "Dockerfile", "pyproject.toml", "secrets/"),
                     copied=("cli.py", "Dockerfile", "pyproject.toml"), key=True, sheet=False)
        place(win, cx=0, bottom=-1.95)
        run_c = cmd_chip(RUN_V)
        place(run_c, cx=0, top=win.get_bottom()[1] - 0.25)
        post = signpost(["GOOGLE_APPLICATION_CREDENTIALS=", "secrets/mega-pipeline.json"], post_h=0.45)
        app_lbl = win.image.app
        post.shift(np.array([app_lbl.get_center()[0], app_lbl.get_top()[1] + 0.05, 0]) - post.root())
        assert post.get_top()[1] < TRACK_BOTTOM - 0.05 and post.get_right()[0] < EDGE, (post.get_top(), post.get_right())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(t), FadeOut(v6), FadeOut(chk), run_time=0.5)
            self.play(FadeIn(win), FadeIn(run_c, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("because the mount brings")
            win.mount(self, run_time=1.5)
            key_c = win.row("secrets/", "cover")[-1]
            self.play(FadeIn(post, shift=DOWN * 0.15), run_time=0.5)
            # the lookup: from the board down the free strip right of /app, then left to the key
            xr = win.image.cavity.get_right()[0] + 0.1
            ky = key_c.get_center()[1]
            leg = Line([xr, post.board.get_bottom()[1], 0], [xr, ky, 0], color=LOOKUP, stroke_width=4)
            tip = Arrow([xr, ky, 0], [key_c.get_right()[0] + 0.06, ky, 0], buff=0, color=LOOKUP, stroke_width=4,
                        max_tip_length_to_length_ratio=0.25)
            look = VGroup(leg, tip)
            self.play(Create(leg), run_time=0.4)
            self.play(GrowArrow(tip), run_time=0.3)
            self.play(Indicate(key_c, color=KEY, scale_factor=1.8), Indicate(win.row("secrets/", "laptop"), color=KEY),
                      run_time=0.8)

        # ========================================================== 7 · the optional push to Docker Hub
        hub_card = self._hub_card()
        place(hub_card, left=-6.3, top=TRACK_BOTTOM - 0.12)
        chips = hub_card.chips
        crate7 = self._box7()
        place(crate7, left=-3.6, bottom=-3.45)
        shelf = hub_shelf()
        place(shelf, right=6.2, bottom=-3.45)
        warn = stamp("without .dockerignore: would publish the key", ERR, angle=0.03)
        green = tag("only after the .dockerignore fix", VENV, size=20)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(win, run_c, post, look)), run_time=0.5)
            tr = switch_section(self, tr, "H", None, run_time=0.6)
            opt = optional_tag()
            place(opt, left=tr.head.get_right()[0] + 0.3, top=3.54)
            full = [c.copy() for c in chips]
            for c in chips:
                scale_opacity(c, 0.3)
            self.play(FadeIn(opt, shift=LEFT * 0.1), FadeIn(hub_card.base, shift=UP * 0.1), FadeIn(chips),
                      run_time=0.5)
            vo.wait_until("create an access token there")
            self.play(FadeIn(hub_card.hl), run_time=0.4)
            vo.wait_until("then log in")
            self.play(tr.goto(1), Transform(chips[0], full[0]), run_time=0.5)
            vo.wait_until("tag and push")
            self.play(tr.goto(2), Transform(chips[1], full[1]), run_time=0.5)
            self.play(tr.goto(3), Transform(chips[2], full[2]), run_time=0.5)
            self.play(FadeIn(crate7, shift=UP * 0.1), FadeIn(shelf, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Only push an image")
            dx = shelf.get_left()[0] - 0.35 - crate7.get_right()[0]
            self.play(crate7.animate.shift(RIGHT * dx), run_time=1.0, rate_func=smooth)
            place(warn, cx=crate7.get_center()[0] - 0.4, bottom=crate7.get_top()[1] + 0.2)
            place(green, right=warn.get_left()[0] - 0.3, cy=warn.get_center()[1])
            assert warn.get_top()[1] < hub_card.get_bottom()[1] - 0.05 and green.get_left()[0] > -EDGE
            self.play(FadeIn(warn, scale=1.3), Indicate(crate7.key, color=ERR, scale_factor=1.5), run_time=0.5)
            vo.wait_until("built with that dot dockerignore")
            self.play(FadeIn(green, shift=RIGHT * 0.1), run_time=0.5)

        # ========================================================== 8 · log in without -p; if you pushed the key
        gl = cmd_chip(LOGIN_U, color=VENV)
        gl_note = label("paste the token at the prompt", 20, S.GREY)
        gl_row = VGroup(gl, gl_note).arrange(RIGHT, buff=0.3)
        place(gl_row, left=-6.3, top=hub_card.get_bottom()[1] - 0.35)
        x0, x1 = chip_span(chips[0], LOGIN, "-p <ACCESS TOKEN>")
        y_u = chips[0].get_bottom()[1] - 0.06
        u_p = Line([x0, y_u, 0], [x1, y_u, 0], color=TURN, stroke_width=4)
        hist = label("stays in your shell history", 20, S.GREY)
        place(hist, left=chips[0].get_right()[0] + 0.3, cy=chips[0].get_center()[1])
        assert hist.get_right()[0] < hub_card.frame.get_right()[0] - 0.1, hist.get_right()
        redc = self._red_card()
        place(redc, left=-6.3, top=gl_row.get_bottom()[1] - 0.45)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(crate7, shelf, warn, green)), run_time=0.4)
            self.play(FadeIn(gl, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and paste the token")
            self.play(FadeIn(gl_note, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("after dash p")
            self.play(Create(u_p), FadeIn(hist, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("If you ever pushed an image")
            self.play(FadeIn(redc, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("delete it and tell the staff")
            self.play(Indicate(redc, color=ERR, scale_factor=1.04), run_time=0.7)

        # ========================================================== 9 · coda: the solution branch
        p8 = src_panel(SOL, 8, 10, size=20, shown_path="transcribe_audio/docker-shell.sh", suffix="solution branch")
        p95 = src_panel(SOL, 95, 100, size=20, shown_path="transcribe_audio/docker-shell.sh", suffix="solution branch")
        place(p95, cx=0, top=3.45)
        place(p8, left=p95.get_left()[0], top=3.45)
        sol_cap = label("last year's solution branch: not today's steps", 20, S.GREY)
        place(sol_cap, left=p95.get_left()[0] + 0.12, top=p8.get_bottom()[1] - 0.08)
        cap_y95 = p95.get_bottom()[1] - 0.08 - sol_cap.height / 2
        pic = coda_picture()
        assert pic.get_top()[1] < cap_y95 - sol_cap.height / 2 - 0.05, (pic.get_top(), cap_y95)

        bar9 = line_bar(p8.code, 1, TURN, 0.2)
        bar98 = line_bar(p95.code, 3, LOOKUP, 0.22)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(hub_card, u_p, hist, gl_row, redc, tr, opt)), run_time=0.5)
            self.play(FadeIn(p8, shift=DOWN * 0.1), FadeIn(sol_cap), run_time=0.5)
            self.play(FadeIn(pic), run_time=0.6)
            vo.wait_until("kept the secrets folder outside")
            self.play(FadeIn(bar9), run_time=0.3)
            self.play(FadeIn(pic.out), run_time=0.4)
            dest = pic.slot - np.array([pic.sec_row.get_left()[0], pic.sec_row.get_center()[1], 0])
            self.play(pic.sec_row.animate.shift(dest), run_time=0.9)
            self.play(Indicate(pic.out_cap, color=INK, scale_factor=1.1), run_time=0.5)
            vo.wait_until("and mounted it at slash secrets")
            # different lines of the same file: a cross-fade (a glyph morph would scramble the code)
            self.play(FadeOut(VGroup(p8, bar9)), FadeIn(p95), sol_cap.animate.set_y(cap_y95), run_time=0.6)
            self.play(FadeIn(bar98), run_time=0.3)
            self.play(Create(pic.r2), Indicate(pic.secs, color=LOOKUP, scale_factor=1.08), run_time=0.8)
            vo.wait_until("No key ever enters the image")
            self.play(FadeIn(pic.img, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(pic.key, color=KEY, scale_factor=1.6), run_time=0.7)
        self.play(FadeOut(VGroup(p95, bar98, sol_cap, pic, pic.out, pic.r2, pic.img)), run_time=0.8)
        self.wait(0.3)

    # ------------------------------------------------------------------ pieces made for this scene
    def _check_home(self, v6):
        """V6 at HOME fits above the strip, under the tracker band, inside the frame."""
        assert v6.get_bottom()[1] > ST4 + 0.1, v6.get_bottom()
        vis = VGroup(v6.folder, v6.book, v6.crate, v6.sieves["git"], v6.sieves["image"])
        assert vis.get_top()[1] < TRACK_BOTTOM - 0.1, vis.get_top()
        assert v6.sieves["image"].name.get_left()[0] > v6.folder.frame.get_right()[0] + 0.1
        assert v6.get_left()[0] > -6.6 and v6.get_right()[0] < 6.6

    def _note_card(self) -> VGroup:
        """README.md:103-106 as a GREY card (header + erratum tag)."""
        rows = VGroup(*[label(s, 20, INK) for s in NOTE_Q]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        fr = box(rows.width + 0.5, rows.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
        rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
        head = gray_line(("README.md",), "· lines 103–106")
        head.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        er = erratum_tag()
        er.next_to(head, RIGHT, buff=0.25)
        er.align_to(fr, RIGHT) if er.get_right()[0] > fr.get_right()[0] else None
        er.shift(UP * max(0.0, fr.get_top()[1] + 0.03 - er.get_bottom()[1]))   # the pill clears the frame
        return VGroup(fr, rows, head, er)

    def _hub_card(self) -> VGroup:
        """transcribe_audio/README.md:136-140 as a GREY card: the heading, the first bullet, and the
        three commands as chips (shown, not typed). .base (frame, header, text rows) .hl .chips .frame"""
        h = label(HUB_HEAD, 20, INK)
        b1 = label("• " + HUB_B1, 20, INK)
        cs = VGroup(cmd_chip(LOGIN), cmd_chip(TAGC), cmd_chip(PUSH))
        col = VGroup(h, b1, *cs).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        for c in cs:
            c.shift(RIGHT * 0.3)
        fr = box(12.6, col.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
        col.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25)
        head = gray_line(("transcribe_audio/README.md",), "· lines 136–140")
        head.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        hl = Rectangle(width=b1.width + 0.2, height=b1.height + 0.14, stroke_width=0).set_fill(TURN, 0.22)
        hl.move_to(b1)
        g = VGroup(fr, head, h, b1, hl, *cs)
        g.base, g.hl, g.chips, g.frame = VGroup(fr, head, h, b1), hl, cs, fr
        return g

    def _box7(self) -> VGroup:
        """The image box of beat 7: built before the fix, the key in its RED COPY slab. .key"""
        b = ship_box()
        fr = b.front
        w = fr.width - 0.16
        base = box(w, 0.24, SYSTEM, fill_opacity=0.25, radius=0.04, stroke=2)
        copy = box(w, 0.34, ERR, fill=ERR, fill_opacity=0.2, radius=0.05, stroke=3)
        sync = box(w, 0.16, VENV, fill_opacity=0.25, radius=0.04, stroke=2)
        stack = VGroup(base, copy, sync).arrange(UP, buff=0.05)
        stack.move_to(fr).align_to(fr, DOWN).shift(UP * 0.08)
        lab = sans("COPY", 20, INK).move_to(copy).align_to(copy, LEFT).shift(RIGHT * 0.1)
        k = key_glyph(0.2).move_to([copy.get_right()[0] - 0.3, copy.get_center()[1], 0])
        b.add(stack, lab, k)
        b.key = k
        return b

    def _red_card(self) -> VGroup:
        t = label("pushed one with the key? delete it · tell the staff", 22, INK)
        fr = box(t.width + 0.5, t.height + 0.36, ERR, fill_opacity=0.1, radius=0.1, stroke=3)
        t.move_to(fr)
        return VGroup(fr, t)
