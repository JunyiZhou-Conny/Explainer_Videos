r"""S11 · Exit, and bake it in (README › transcribe_audio step 13; V3 + V4, then V2).

The house terminal changes height with the beat: a 2-row strip under the 7-row window (beat 0:
the window needs 4.7 of the frame), 13 rows for the laptop checks (beats 1-2), 7 rows under a
picture (beats 3-5, 8), a 4-row strip under V2 (beat 7). V2 stands top right (floor y 0.8)
from beat 5 to beat 8, so the full logs and panels can take the bottom of the frame.

Beats (script.md "## S11", one voiceover block each):
 0  TRACKER A12 -> A13. V3 + V4 as S08-S10 left them, mounted: the laptop folder holds cli.py,
    Dockerfile, pyproject.toml and uv.lock (GREEN), secrets/, input_audios/, text_prompts/; the
    dashed TEAL writable layer carries 26 GREEN chips on its shelf. Under it a 2-row strip (TEAL,
    container prompt). It types `exit`: the frame turns GREY, the title `laptop`, the prompt
    `student@laptop:~/mega-pipeline/transcribe_audio$`; the laptop sheet slides back along the PINK
    route and the route fades (no container, no window). On "the container is removed" the
    writable layer floats up and vanishes; on "the 26 packages" its chips scatter after it. The
    laptop's survivors blink GREEN.
 1  TRACKER A13 · extra. The window goes, the terminal grows to 13 rows. Typed in the order the
    SAY names them (extras, each with a GREY `extra` tag): `cat pyproject.toml` ->
    TERM(14-host-after-uv-add.txt: …, 17–21), the three dependencies GREEN with a bar;
    `wc -c uv.lock` -> TERM(…: 35), GREEN bar; `ls -a` -> TERM(…: …, 8–12): input_audios and
    text_prompts GREEN, then on "all survived" all four survivors GREEN; the four pulse on "in the
    window".
 2  `git status --short` (extra) -> TERM(…: 36); ` M cli.py` underlines YELLOW; GREY tag "the rest
    is hidden from Git · S15" beside it; the survivor rows pulse GREY.
 3  The trap. The terminal clears and shrinks to 7 rows. Above it, V4's image alone: the TEAL image
    `transcribe_audio` "built before uv add" (the /app cavity with the mounted cli.py, the GREEN
    /home/app/.venv box). It types `docker run --rm -ti -v "$(pwd):/app" transcribe_audio` (extra,
    folds after `run`): the frame turns TEAL and a new dashed writable layer settles on the image,
    its GREEN shelf empty. `python cli.py --help` (extra) -> TERM(11-g10-new-container.txt: 2–5),
    line 5 RED and underlined; a dashed RED line runs from cli.py to a RED "?" at the empty venv;
    on "lived only in the old container" the empty shelf flashes RED with a GREY tag "empty".
 4  It types `exit` (frame GREY); the layer evaporates and the picture goes; TRACKER A13; the
    README chip `transcribe_audio/README.md · line 110` "re-build the image" above the terminal.
    It types `docker build -t transcribe_audio .` (folds after `build`) -> TERM(15-rebuild.txt: 3,
    14–17): live-view rows cut at 58 characters, each row's last field in a GREY tag at its right
    end. ▶ your turn.
 5  The chip goes; V2 (old state: GREY COPY slab, empty uv sync slab) rises top right; GREY tag
    "ponder 2". On "build steps 2 and 3" `CACHED` turns GREEN and boxed on lines 14–15, and the apt
    and WORKDIR slabs get GREEN "CACHED" stamps (fanned, with leaders; the base slab stays as is).
    On "build step 4" line 16 gets a TEAL "build step 4" badge and the COPY slab dissolves and
    re-forms, now holding a GREEN pyproject.toml and a GREEN uv.lock; on "build step 5" line 17's
    badge, its `2.9s` tag pulses, the uv sync slab dissolves and re-forms. `Building 9.9s`
    underlines YELLOW on "The build took".
 6  The terminal gives way to PANEL(15-rebuild.plain.txt: 30–33, …, 38–39, "the same build, full
    log · lines 30–39"). On "the copy brought in" the GREEN uv.lock in the COPY slab pulses and
    `Resolved 27 packages` turns GREEN; on "and uv installed" `Installed 26 packages` turns GREEN,
    the uv sync slab grows and 26 GREEN chips stream into it from uv.lock; the slab pulses on
    "into the image".
 7  TRACKER A13 · extra. The panel goes; a 4-row strip: `docker images transcribe_audio` (extra)
    -> TERM(16-images-after.txt: 2–3); `1.48GB` gets a YELLOW bar, and V2 a GREY brace on its left
    "≈ 1.1 GB of layers" + "+ 388 MB compressed copy" / "= 1.48 GB disk usage · this machine".
    `docker history transcribe_audio` (extra); the brace and the strip give way to
    PANEL(17-history.txt: 2–9, …, 16, "docker history · CREATED BY and SIZE"), rows sliced to
    line[32:90], bottom left. The rows pulse in turn; on "card-only lines" the four 0B rows' "0B"
    turn TEAL and their instruction words flick onto a small TEAL config card (bottom right). On
    "The uv sync layer" the sizes lift out of rows 5, 6, 9 onto their slabs: `105MB` GREEN, then
    `193kB` GREY and `842MB` ORANGE; on "the packages plus" the GREEN label is split: "= venv ≈ 50 MB
    + uv cache ≈ 58 MB".
 8  The panel, card and labels go; a 7-row terminal: `docker run --rm -ti -v "$(pwd):/app"
    transcribe_audio` (extra): TEAL frame, and a dashed "new container" layer settles on V2;
    `python -c "import google.cloud.storage, google.cloud.speech, ffmpeg; print(\"imports ok\")"`
    (extra, 3 rows) -> TERM(12-after-rebuild.txt: 2) GREEN; the 26 chips in the uv sync slab pulse
    GREEN on "they're baked in". `exit`: the layer evaporates.
 9  TRACKER A13. V2 alone, centred. The COPY and uv sync slabs pulse in build order; a GREY chip
    "edit: group_name" drops into the COPY slab (YELLOW flash); the uv sync slab tips over and
    falls off like a domino; it re-forms and its 26 chips rain in again. A GREY note: "later
    tutorials: COPY pyproject.toml uv.lock first, / then uv sync, then the rest"; its first part
    underlines YELLOW. Fade out: empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (MONO, box, chip, file_glyph, folder_glyph, label, mono, mono_line, step_badge,
                              substring, tag)
from explainer.scene import VoiceScene

from common import (CTR, ERR, INK, LAPTOP, LOOKUP, NARRATION, P_A, P_CTR, PANEL, SYSTEM, TOOL, TURN, VENV,
                    ConfigCard, LayerStack, Window, bare_prompt, beside, cached_stamp, capture, caption_extra,
                    enter_container, extra_tag, history_row, key_glyph, leave_container, live_split, log_panel,
                    pin, pkg_dots, readme_chip, resize, sans, source_text, strip_top, term, time_tag, tracker,
                    type_cmd, your_turn)

SAY = NARRATION["S11"]

# ------------------------------------------------------------------ commands and real outputs
HOST = capture("14-host-after-uv-add")
assert HOST.cmd.split("; ") == ["ls -a", "cat pyproject.toml", "head -c 300 uv.lock", "echo",
                                "wc -c uv.lock", "git status --short"], HOST.cmd
LS_CMD, CAT_CMD, WC_CMD, GIT_CMD = "ls -a", "cat pyproject.toml", "wc -c uv.lock", "git status --short"
CAT_OUT = HOST.at("…", (17, 21))
assert CAT_OUT[1] == "dependencies = [" and CAT_OUT[-1] == "]", CAT_OUT
assert [s.strip() for s in CAT_OUT[2:5]] == ['"ffmpeg-python>=0.2.0",', '"google-cloud-speech>=2.41.0",',
                                             '"google-cloud-storage>=3.17.0",'], CAT_OUT
WC_OUT = HOST.at(35)
assert WC_OUT == ["138445 uv.lock"], WC_OUT
LS_OUT = HOST.at("…", (8, 12))
assert LS_OUT[1:] == ["input_audios", "pyproject.toml", "secrets", "text_prompts", "uv.lock"], LS_OUT
SURVIVORS = ["input_audios", "pyproject.toml", "text_prompts", "uv.lock"]
GIT_OUT = HOST.at(36)
assert GIT_OUT == [" M cli.py"], GIT_OUT

RUN = capture("01-docker-run-tty", "transcribe_audio").cmd
_RA = source_text("transcribe_audio/README.md").split("\n")
assert RUN == 'docker run --rm -ti -v "$(pwd):/app" transcribe_audio' and _RA[98] == RUN, RUN   # README :99
assert "re-build the image" in _RA[109], _RA[109]                                                # README :110

TRAP = capture("11-g10-new-container", "transcribe_audio")
assert TRAP.cmd == "python cli.py --help", TRAP.cmd
TRAP_OUT = TRAP.at((2, 5))
assert TRAP_OUT[-1] == "ModuleNotFoundError: No module named 'google'", TRAP_OUT

BUILD = "docker build -t transcribe_audio ."           # README :95 names the image; never --network host
_RB = capture("15-rebuild")
assert _RB.cmd == "docker build --network host -t transcribe_audio .", _RB.cmd
LIVE = [live_split(_RB.line(n), 58) for n in (3, 14, 15, 16, 17)]
assert LIVE[0] == ("[+] Building 9.9s (10/10) FINISHED", "docker:default"), LIVE[0]
assert LIVE[1][0].startswith(" => CACHED [2/5] RUN apt-get update") and LIVE[2][0] == " => CACHED [3/5] WORKDIR /app"
assert LIVE[3] == (" => [4/5] COPY --chown=app:app . ./", "0.0s") and LIVE[4] == (" => [5/5] RUN uv sync", "2.9s")

PLAIN = capture("15-rebuild.plain")
PLAIN_OUT = PLAIN.at((30, 33), "…", (38, 39))
assert PLAIN_OUT[0] == "#9 [5/5] RUN uv sync" and "Resolved 27 packages" in PLAIN_OUT[3], PLAIN_OUT
assert "Installed 26 packages" in PLAIN_OUT[6], PLAIN_OUT

IMG = capture("16-images-after")
assert IMG.cmd == "docker images transcribe_audio", IMG.cmd
IMG_OUT = IMG.at((2, 3))
assert "1.48GB" in IMG_OUT[1] and "388MB" in IMG_OUT[1], IMG_OUT

HIST = capture("17-history")
assert HIST.cmd == "docker history transcribe_audio", HIST.cmd
HIST_ROWS = [history_row(HIST.line(n)) for n in range(2, 10)] + ["…", history_row(HIST.line(16))]
assert HIST_ROWS[3].startswith("RUN |1") and HIST_ROWS[3].endswith("105MB"), HIST_ROWS[3]    # line 5
assert HIST_ROWS[4].startswith("COPY") and HIST_ROWS[4].endswith("193kB"), HIST_ROWS[4]      # line 6
assert HIST_ROWS[7].startswith("RUN |1") and HIST_ROWS[7].endswith("842MB"), HIST_ROWS[7]    # line 9
ZERO = {1: "CMD", 2: "ENTRYPOINT", 6: "USER app", 9: "ARG"}         # panel row -> card line (0B rows)
for _i, _w in ZERO.items():
    assert HIST_ROWS[_i].startswith(_w) and HIST_ROWS[_i].endswith("0B"), HIST_ROWS[_i]

_AR = capture("12-after-rebuild", "transcribe_audio")
IMP_CMD = _AR.cmd.split("; uv --version")[0]          # the `;`-joined capture: only this one is typed
assert IMP_CMD == 'python -c "import google.cloud.storage, google.cloud.speech, ffmpeg; print(\\"imports ok\\")"'
IMP_OUT = _AR.at(2)
assert IMP_OUT == ["imports ok"], IMP_OUT

# ------------------------------------------------------------------ layout
EDGE = 6.45
TRACK_BOTTOM = 2.917               # the tracker band is y 2.92..3.5
BIG, MID, STRIP0, STRIP7 = 13, 7, 2, 4
WIN_DX = 0.25                      # the window sits 0.25 right: its writable layer clears the tracker
SLAB_W, SX, FLOOR_Y = 4.2, 4.15, 0.8         # V2 top right (beats 5-8), above the history panel
H0 = {"base": 0.36, "apt": 0.5, "workdir": 0.07, "copy": 0.3, "sync": 0.36}
SYNC_FULL = 0.66
CENTRE = np.array([0.0, -1.25, 0])           # beat 9: V2's floor, centred


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


def make_room(scene, t, n: int, at_least: int = 0):
    """Room for n new rows before typing/printing: the oldest rows fade where they are, then the
    rest move up (Terminal's own scroll would slide them over the title bar)."""
    over = max(len(t.lines) + n - t.rows, at_least)
    over = min(over, len(t.lines))
    if over <= 0:
        return
    gone = t.lines.submobjects[:over]
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(VGroup(*gone)), run_time=0.25)
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=0.3)


def seed(t, text: str, color=INK, prompt: bool = False, bare: bool = False):
    """Put a line on terminal t without animation (the terminal fades in with it)."""
    ln = mono_line(text, t.size, color, t2c=t._prompt_colors(t.prompt) if prompt else None)
    t._place(ln, len(t.lines))
    t.lines.add(ln)
    if bare:
        ln.bare = True
    return ln


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded), so
    they scroll and fade with it."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def rbar(lines, color, opacity=0.2, pad=0.08) -> Rectangle:
    """A translucent bar behind whole terminal rows (first glyph to last)."""
    lines = lines if isinstance(lines, (list, tuple)) else [lines]
    left = min(ln.glyphs.get_left()[0] for ln in lines) - pad
    rx = max(ln.glyphs.get_right()[0] for ln in lines) + pad
    top = lines[0].strut.get_top()[1] + 0.02
    bot = lines[-1].strut.get_bottom()[1] - 0.02
    return Rectangle(width=rx - left, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([(left + rx) / 2, (top + bot) / 2, 0])


def sbar(line, sub, color, opacity=0.3) -> Rectangle:
    """A translucent bar over substring `sub` of a terminal row."""
    g = substring(line, sub)
    return Rectangle(width=g.width + 0.14, height=line.strut.height * 0.95, stroke_width=0) \
        .set_fill(color, opacity).move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def uline(line, sub, color, stroke=3.5, pad=0.02) -> Line:
    """A Line under substring `sub` of terminal row `line`, in the gap under the row."""
    g = substring(line, sub)
    y = line.strut.get_bottom()[1] + 0.01
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def row_badge(k: int) -> VGroup:
    """TEAL 'build step k' badge that fits inside one terminal row."""
    b = step_badge(k, CTR, size=20, radius=0.17)
    return VGroup(b, sans(f"build step {k}", 20, CTR)).arrange(RIGHT, buff=0.1)


def note_tag(s: str) -> VGroup:
    return tag(s, S.GREY, size=20)


# ------------------------------------------------------------------ pictures
WIN_FILES = ("cli.py", "Dockerfile", ("pyproject.toml", VENV), "secrets/", ("uv.lock", VENV), "input_audios/",
             "text_prompts/")
WIN_COPIED = ("cli.py", "Dockerfile", "pyproject.toml", "secrets/")      # what the step-5 image copied


def make_window() -> Window:
    """V3 + V4 as S08-S10 leave them: mounted, the laptop folder with the files uv add and the
    download wrote, 26 GREEN chips on the writable layer's shelf. Bottom just above the 2-row
    strip, 0.25 right of centre."""
    win = Window(files=WIN_FILES, copied=WIN_COPIED, mounted=True)
    sheet = win.sheet
    cap = sheet.caption
    new_cap = sans("writable layer · throwaway", 20, CTR).move_to(cap, aligned_edge=LEFT)
    sheet.remove(cap)
    sheet.add(new_cap)
    sheet.caption = new_cap
    sh = sheet.shelf
    d = pkg_dots(26, cols=13)
    if d.width > sh.get_length() - 0.1:
        d.scale_to_fit_width(sh.get_length() - 0.1)
    d.next_to(sh, UP, buff=0.03)
    sheet.add(d)
    sheet.chips = d
    place(win, bottom=strip_top(STRIP0) + 0.1)
    win.shift(RIGHT * WIN_DX)
    return win


def trap_image() -> VGroup:
    """V4's image alone, as the step-5 build made it (beat 3): TEAL frame, the /app cavity with the
    mounted laptop folder (cli.py), the GREEN /home/app/.venv box (just the project: empty).
    .frame .cavity .cover .cli .venv .vlabel .caption"""
    fr = box(6.3, 1.3, CTR, fill_opacity=0.06)
    cav = RoundedRectangle(width=3.0, height=0.62, corner_radius=0.1, stroke_color=CTR,
                           stroke_width=2).set_fill(S.BG, 1)
    cav.move_to(fr.get_corner(DL) + np.array([0.2 + 1.5, 0.17 + 0.31, 0]))
    app = mono("/app", 20, INK).next_to(cav, UP, buff=0.1).align_to(cav, LEFT)
    cover = RoundedRectangle(width=2.8, height=0.46, corner_radius=0.08, stroke_color=LAPTOP,
                             stroke_width=2).set_fill(PANEL, 1).move_to(cav)
    cli = VGroup(file_glyph(0.28, LAPTOP), mono("cli.py", 20, INK)).arrange(RIGHT, buff=0.12)
    cli.move_to(cover).align_to(cover, LEFT).shift(RIGHT * 0.15)
    vbox = box(2.6, 0.62, VENV, fill_opacity=0.12)
    vbox.move_to([cav.get_right()[0] + 0.2 + 1.3, cav.get_center()[1], 0])
    vlab = mono("/home/app/.venv", 20, VENV).next_to(vbox, UP, buff=0.1)
    cap = sans("image · transcribe_audio · built before uv add", 20, CTR).next_to(fr, DOWN, buff=0.12)
    g = VGroup(fr, cav, app, cover, cli, vbox, vlab, cap)
    g.frame, g.cavity, g.cover, g.cli, g.venv, g.vlabel, g.caption = fr, cav, cover, cli, vbox, vlab, cap
    return g


def new_layer(over, caption: str, width: float | None = None, h: float = 0.5, shelf_under=None) -> VGroup:
    """A dashed TEAL writable layer settling on `over` (its top edge), with a caption at its left
    and, if `shelf_under` is given, an empty GREEN shelf above that box. .frame .caption .shelf"""
    w = width or over.width
    fr = box(w, h, CTR, dashed=True).next_to(over, UP, buff=0.06)
    cap = sans(caption, 20, CTR).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
    g = VGroup(fr, cap)
    g.frame, g.caption, g.shelf = fr, cap, None
    if shelf_under is not None:
        vx = shelf_under
        sh = Line([vx.get_left()[0] + 0.1, fr.get_bottom()[1] + 0.1, 0],
                  [vx.get_right()[0] - 0.1, fr.get_bottom()[1] + 0.1, 0], color=VENV, stroke_width=3)
        g.add(sh)
        g.shelf = sh
    return g


def copy_glyphs(st: LayerStack, new: bool) -> VGroup:
    """The files inside the COPY slab: before the rebuild five GREY files and the tiny GOLD key;
    after it the folder as uv add left it: four GREY files, a GREEN pyproject.toml and a GREEN
    uv.lock, the two new folders and the key. .lock (the uv.lock glyph when new)"""
    sb = st.slabs["copy"].box
    h = sb.height - 0.12
    if new:
        items = [file_glyph(h, LAPTOP) for _ in range(4)] + [file_glyph(h, VENV), file_glyph(h, VENV),
                                                           folder_glyph(h * 0.85, LAPTOP),
                                                           folder_glyph(h * 0.85, LAPTOP), key_glyph(h * 0.6)]
    else:
        items = [file_glyph(h, LAPTOP) for _ in range(5)] + [key_glyph(h * 0.6)]
    g = VGroup(*items).arrange(RIGHT, buff=0.14).move_to(sb)
    g.lock = items[5] if new else None
    return g


def make_stack() -> LayerStack:
    """V2 as the step-5 build left it: five slabs (base, apt, WORKDIR hairline, the GREY COPY
    slab with its files, the empty GREEN uv sync slab), floor at (SX, FLOOR_Y)."""
    st = LayerStack(slab_w=SLAB_W)
    for name in ("base", "apt", "workdir", "copy", "sync"):
        s = st.make(name, h=H0[name])
        st.slabs[name] = s
        st.order.append(name)
        st.add(s)
    st.copy_files = copy_glyphs(st, new=False)
    st.add(st.copy_files)
    st.move_to([SX, FLOOR_Y, 0], aligned_edge=DOWN)
    return st


def stack_brace(st: LayerStack) -> VGroup:
    """GREY brace on V2's left with "≈ 1.1 GB of layers" and the disk-usage note (right-aligned)."""
    boxes = VGroup(*[st.slabs[n].box for n in st.order])
    br = Brace(boxes, LEFT, color=S.GREY, buff=0.12)
    txt = VGroup(sans("≈ 1.1 GB of layers", 20, INK), label("+ 388 MB compressed copy", 20, S.GREY),
                 label("= 1.48 GB disk usage · this machine", 20, S.GREY))
    txt.arrange(DOWN, aligned_edge=RIGHT, buff=0.1).next_to(br, LEFT, buff=0.15)
    g = VGroup(br, txt)
    g.brace, g.text = br, txt
    return g


def edit_chip() -> VGroup:
    t = mono("edit: group_name", 20, INK)
    fr = RoundedRectangle(width=t.width + 0.44, height=0.5, corner_radius=0.18, stroke_color=S.GREY,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def history_panel() -> VGroup:
    return log_panel(HIST_ROWS, "docker history · CREATED BY and SIZE", width=9.6, size=20)


def plain_panel() -> VGroup:
    """The rebuild's full log, lines 30-39 (with a '…' between 33 and 38), header in serif."""
    p = log_panel(PLAIN_OUT, "x", width=12.6, size=20)
    head = label("the same build, full log · lines 30–39", 20, S.GREY)
    head.next_to(p.frame, UP, buff=0.1).align_to(p.frame, LEFT).shift(RIGHT * 0.12)
    p.remove(p.header)
    p.header = head
    p.add(head)
    return p


# ------------------------------------------------------------------ the scene
class BakeItIn(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, f"S11 has {len(SAY)} SAY lines; this scene times 10"

        tr = tracker("A", 12)

        # ========================================================== 0 · exit: the layer evaporates
        t = term(P_CTR, STRIP0, component="transcribe_audio")
        seed(t, P_CTR + " ", prompt=True, bare=True)
        win = make_window()
        assert win.get_bottom()[1] > strip_top(STRIP0) + 0.05 and win.get_top()[1] < 3.0
        assert win.sheet.frame.get_left()[0] > tr.get_right()[0] + 0.05
        lap_survivors = VGroup(*[win.row(n, "laptop") for n in ("pyproject.toml", "uv.lock", "input_audios/",
                                                                 "text_prompts/")])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), FadeIn(win), run_time=0.8)
            self.play(tr.goto(13), run_time=0.5)
            self.play(Indicate(win.sheet.chips, color=VENV, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Type exit")
            type_cmd(self, t, "exit", 0.4)
            self.play(*leave_container(t, P_A), win.cover_to(0), win.copied.animate.set_opacity(1),
                      run_time=0.8)
            win.hide(self, "cover", "route", "route_label", run_time=0.4)
            bare_prompt(self, t)
            vo.wait_until("and the container is removed")
            chips = win.sheet.chips
            win.sheet.remove(chips)                  # the packages linger a moment after their layer
            win.add(chips)
            win.evaporate(self, run_time=0.9)
            vo.wait_until("and the 26 packages")
            win.detach(self, chips, anims=[FadeOut(chips, shift=UP * 0.6, lag_ratio=0.05)], run_time=1.3)
            self.play(Indicate(lap_survivors, color=VENV, scale_factor=1.1), run_time=0.8)

        # ========================================================== 1 · back on the laptop (extras)
        with self.voiceover(SAY[1]) as vo:
            resize(self, t, BIG, run_time=0.7, extra=[FadeOut(win), caption_extra(tr)])
            vo.wait_until("the pyproject.toml with")
            make_room(self, t, 1 + len(CAT_OUT))
            c1 = type_cmd(self, t, CAT_CMD, 0.6)
            out1 = t.print(self, CAT_OUT, run_time=0.4, lag=0.08)
            deps = list(out1[2:5])
            x1, b1 = beside(extra_tag(), t, c1), rbar(deps, VENV, 0.2)
            self.play(FadeIn(x1), FadeIn(b1), *[ln.glyphs.animate.set_color(VENV) for ln in deps], run_time=0.4)
            stick(self, c1, x1)
            stick(self, deps[0], b1)

            vo.wait_until("the lock file")
            make_room(self, t, 1 + len(WC_OUT))
            c2 = type_cmd(self, t, WC_CMD, 0.5)
            out2 = t.print(self, WC_OUT, run_time=0.3)
            x2, b2 = beside(extra_tag(), t, c2), rbar(out2[0], VENV, 0.2)
            self.play(FadeIn(x2), FadeIn(b2), out2[0].glyphs.animate.set_color(VENV), run_time=0.4)
            stick(self, c2, x2)
            stick(self, out2[0], b2)

            vo.wait_until("and the two new folders")
            make_room(self, t, 1 + len(LS_OUT))
            c3 = type_cmd(self, t, LS_CMD, 0.3)
            out3 = t.print(self, LS_OUT, run_time=0.5, lag=0.08)
            rows3 = {ln.text: ln for ln in out3}
            x3 = beside(extra_tag(), t, c3)
            folders = [rows3["input_audios"], rows3["text_prompts"]]
            self.play(FadeIn(x3), *[ln.glyphs.animate.set_color(VENV) for ln in folders], run_time=0.4)
            stick(self, c3, x3)
            vo.wait_until("all survived")
            surv = [rows3[n] for n in SURVIVORS]
            bars = [rbar(ln, VENV, 0.2) for ln in surv]
            self.play(*[ln.glyphs.animate.set_color(VENV) for ln in surv], *[FadeIn(b) for b in bars], run_time=0.5)
            for ln, b in zip(surv, bars):
                stick(self, ln, b)
            vo.wait_until("because they were")
            self.play(LaggedStart(*[Indicate(ln.glyphs, color=VENV, scale_factor=1.15) for ln in surv],
                                  lag_ratio=0.2), run_time=1.2)

        # ========================================================== 2 · git status --short (extra)
        with self.voiceover(SAY[2]) as vo:
            make_room(self, t, 1 + len(GIT_OUT))
            c4 = type_cmd(self, t, GIT_CMD, 0.6)
            out4 = t.print(self, GIT_OUT, run_time=0.3)
            x4 = beside(extra_tag(), t, c4)
            self.play(FadeIn(x4), run_time=0.3)
            stick(self, c4, x4)
            vo.wait_until("as changed")
            u4 = uline(out4[0], "M cli.py", TURN, stroke=4)
            self.play(Create(u4), Indicate(substring(out4[0], "M cli.py"), color=TURN, scale_factor=1.2),
                      run_time=0.7)
            stick(self, out4[0], u4)
            vo.wait_until("we'll see why")
            hid = note_tag("the rest is hidden from Git · S15")
            place(hid, left=substring(out4[0], "M cli.py").get_right()[0] + 0.5,
                  cy=out4[0].strut.get_center()[1])
            self.play(FadeIn(hid, shift=LEFT * 0.15), run_time=0.5)
            stick(self, out4[0], hid)
            self.play(LaggedStart(*[Indicate(ln.glyphs, color=S.GREY, scale_factor=1.1) for ln in surv],
                                  lag_ratio=0.15), run_time=1.1)

        # ========================================================== 3 · the trap (extra)
        img = trap_image()
        place(img, cx=0, bottom=strip_top(MID) + 0.12)
        layer3 = new_layer(img.frame, "writable layer · new container", shelf_under=img.venv)
        assert layer3.get_top()[1] < TRACK_BOTTOM - 0.08, layer3.get_top()[1]
        with self.voiceover(SAY[3]) as vo:
            resize(self, t, MID, keep=0, run_time=0.7)
            self.play(FadeIn(img, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(img.caption, color=CTR, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Start a new container")
            c5 = type_cmd(self, t, RUN, 1.3)
            assert c5.rows[0].text.endswith("docker run \\"), c5.rows[0].text
            x5 = beside(extra_tag(), t, c5)
            self.play(*enter_container(t), FadeIn(x5), FadeIn(layer3, shift=DOWN * 0.3), run_time=0.7)
            stick(self, c5, x5)
            self.play(Indicate(layer3.shelf, color=VENV, scale_factor=1.0), run_time=0.6)
            vo.wait_until("and ask for help")
            c6 = type_cmd(self, t, TRAP.cmd, 0.6)
            x6 = beside(extra_tag(), t, c6)
            self.play(FadeIn(x6), Indicate(img.cli, color=TURN, scale_factor=1.15), run_time=0.5)
            stick(self, c6, x6)
            vo.wait_until("It's module not found")
            out6 = t.print(self, TRAP_OUT[:-1] + [(TRAP_OUT[-1], ERR)], run_time=0.5, lag=0.1)
            u6 = uline(out6[-1], "ModuleNotFoundError", ERR, stroke=4)
            q = sans("?", 40, ERR, weight="BOLD").move_to(img.venv)
            link = DashedLine(img.cli.get_right() + RIGHT * 0.12, q.get_left() + LEFT * 0.08, color=ERR,
                              stroke_width=2.5, dash_length=0.08)
            self.play(Create(u6), Create(link), FadeIn(q, scale=1.4), run_time=0.7)
            stick(self, out6[-1], u6)
            vo.wait_until("the packages lived only")
            empty = note_tag("empty")
            place(empty, left=layer3.shelf.get_right()[0] - empty.width, cy=layer3.frame.get_center()[1])
            empty.align_to(layer3.shelf, RIGHT)
            self.play(Indicate(layer3.shelf, color=ERR, scale_factor=1.0), FadeIn(empty, shift=DOWN * 0.1),
                      run_time=0.8)
            self.play(Indicate(q, color=ERR, scale_factor=1.3), run_time=0.7)

        # ========================================================== 4 · the README's fix: rebuild
        rchip = readme_chip("transcribe_audio/README.md · line 110", "re-build the image")
        place(rchip, cx=0, cy=(strip_top(MID) + TRACK_BOTTOM) / 2 - 0.2)
        with self.voiceover(SAY[4]) as vo:
            make_room(self, t, 1)
            type_cmd(self, t, "exit", 0.3)
            self.play(*leave_container(t, P_A), FadeOut(layer3, shift=UP * 0.4), FadeOut(empty),
                      FadeOut(q), FadeOut(link), run_time=0.6)
            self.play(FadeOut(img, shift=UP * 0.1), FadeIn(rchip, shift=DOWN * 0.1), caption_extra(tr, False),
                      run_time=0.6)
            vo.wait_until("and rebuild the image")
            self.play(rchip.phrase.animate.set_color(TURN), Indicate(tr.dots, color=TURN, scale_factor=1.1),
                      run_time=0.5)
            make_room(self, t, 2 + len(LIVE), at_least=len(t.lines))
            c7 = type_cmd(self, t, BUILD, 1.1)
            assert c7.rows[0].text.endswith("docker build \\"), c7.rows[0].text
            out7 = t.print(self, [s for s, _ in LIVE], run_time=0.6, lag=0.1)
            times = [place_tag(time_tag(tm), t, ln) for (_, tm), ln in zip(LIVE, out7)]
            self.play(*[FadeIn(g) for g in times], run_time=0.4)
            for ln, g in zip(out7, times):
                stick(self, ln, g)
            vo.wait_until("Pause and run it")
            yt = beside(your_turn(), t, c7)
            pin(self, c7, yt, run_time=0.4)
            self.play(Wiggle(yt, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)
        r3, r14, r15, r16, r17 = out7

        # ========================================================== 5 · the ponder's answer, for real
        st = make_stack()
        stamps, leads = VGroup(), VGroup()
        x_edge = st.slabs["apt"].box.get_left()[0]
        for n, dy in (("apt", -0.14), ("workdir", 0.34)):
            b = st.slabs[n].box
            s_ = cached_stamp()
            s_.move_to([x_edge - 0.45 - s_.width / 2, b.get_center()[1] + dy, 0])
            leads.add(Line(s_.get_right(), [x_edge - 0.03, b.get_center()[1], 0], color=VENV, stroke_width=2.5))
            stamps.add(s_)
        ptag = note_tag("ponder 2")
        place(ptag, right=stamps.get_left()[0] - 0.35, cy=stamps[1].get_center()[1])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(rchip), FadeIn(st, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(ptag, shift=DOWN * 0.1), run_time=0.4)

            vo.wait_until("build steps 2 and 3")
            cached = [substring(r, "CACHED") for r in (r14, r15)]
            boxes = [SurroundingRectangle(c, color=VENV, buff=0.04, stroke_width=2.5, corner_radius=0.05)
                     for c in cached]
            self.play(*[c.animate.set_color(VENV) for c in cached], *[Create(b) for b in boxes], run_time=0.5)
            for r, b in zip((r14, r15), boxes):
                stick(self, r, b)
            st.attach(self, *leads, *stamps,
                      anims=[LaggedStart(*[AnimationGroup(Create(ln), FadeIn(s_, scale=1.4))
                                           for ln, s_ in zip(leads, stamps)], lag_ratio=0.4)], run_time=0.9)

            vo.wait_until("while build step 4")
            cp = st.slabs["copy"]
            bd4 = row_badge(4)
            place(bd4, left=r16.glyphs.get_right()[0] + 0.45, cy=r16.strut.get_center()[1])
            saved_cp = cp.box.copy()
            old_files, new_files = st.copy_files, copy_glyphs(st, new=True)
            st.detach(self, old_files, anims=[FadeOut(old_files, scale=1.1)], run_time=0.6,
                      extra=[FadeIn(bd4, shift=LEFT * 0.1), cp.box.animate.set_opacity(0).scale(1.04)])
            stick(self, r16, bd4)
            st.attach(self, new_files, anims=[FadeIn(new_files, shift=DOWN * 0.15)], run_time=0.8,
                      extra=[Transform(cp.box, saved_cp)])
            st.copy_files = new_files
            lock = new_files.lock
            self.play(Indicate(VGroup(new_files[4], lock), color=VENV, scale_factor=1.3), run_time=0.7)

            vo.wait_until("and build step 5")
            sync = st.slabs["sync"]
            bd5 = row_badge(5)
            place(bd5, left=r17.glyphs.get_right()[0] + 0.45, cy=r17.strut.get_center()[1])
            saved_sync = VGroup(sync.box.copy(), sync.label.copy())
            self.play(FadeIn(bd5, shift=LEFT * 0.1), sync.box.animate.set_opacity(0).scale(1.04),
                      sync.label.animate.set_opacity(0), run_time=0.5)
            stick(self, r17, bd5)
            self.play(Transform(sync.box, saved_sync[0]), Transform(sync.label, saved_sync[1]),
                      Indicate(times[4], color=INK, scale_factor=1.35), run_time=0.8)

            vo.wait_until("The build took")
            u3 = uline(r3, "Building 9.9s", TURN, stroke=4)
            self.play(Create(u3), Indicate(substring(r3, "Building 9.9s"), color=TURN, scale_factor=1.15),
                      run_time=0.8)
            stick(self, r3, u3)

        # ========================================================== 6 · the full log: 26 packages, into the image
        plog = plain_panel()
        place(plog, cx=0, bottom=-3.5)
        assert plog.get_top()[1] < FLOOR_Y - 0.1, plog.get_top()[1]
        with self.voiceover(SAY[6]) as vo:
            st.detach(self, *leads, *stamps, run_time=0.4)
            self.play(FadeOut(t), FadeOut(ptag), FadeIn(plog, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("the copy brought in")
            rr = plog.rows[3]
            self.play(Indicate(lock, color=VENV, scale_factor=1.6),
                      substring(rr, "Resolved 27 packages").animate.set_color(VENV), run_time=0.8)
            vo.wait_until("and uv installed")
            ri = plog.rows[6]
            self.play(substring(ri, "Installed 26 packages").animate.set_color(VENV), *st.grow("sync", SYNC_FULL,
                                                                                               label_top=True),
                      run_time=0.7)
            target = st.chips("sync", 26)
            start = target.copy()
            for c in start:
                c.move_to(lock.get_center()).scale(0.5)
            st.attach(self, start, anims=[Transform(start, target, lag_ratio=0.04, path_arc=-0.6)], run_time=1.6)
            st.sync_chips = start
            vo.wait_until("into the image")
            self.play(Indicate(VGroup(sync.box, start), color=VENV, scale_factor=1.05), run_time=0.9)

        # ========================================================== 7 · docker images, docker history (extras)
        t7 = term(P_A, STRIP7)
        hpan = history_panel()
        place(hpan, left=-EDGE, bottom=-3.5)
        assert hpan.frame.get_top()[1] < FLOOR_Y - 0.1 and hpan.get_right()[0] < 3.2, hpan.get_corner(UR)
        card = ConfigCard(width=3.15, rows=2)
        place(card, right=EDGE, bottom=-3.5)
        brace = stack_brace(st)
        assert brace.get_left()[0] > -EDGE and brace.get_bottom()[1] > strip_top(STRIP7) + 0.1, brace.get_corner(DL)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(plog), FadeIn(t7), caption_extra(tr), run_time=0.6)
            c8 = type_cmd(self, t7, IMG.cmd, 0.8)
            out8 = t7.print(self, IMG_OUT, run_time=0.4)
            x8 = beside(extra_tag(), t7, c8)
            self.play(FadeIn(x8), run_time=0.3)
            stick(self, c8, x8)
            vo.wait_until("The image grew")
            b148 = sbar(out8[1], "1.48GB", TURN, 0.3)
            self.play(FadeIn(b148), Indicate(substring(out8[1], "1.48GB"), color=TURN, scale_factor=1.2), run_time=0.6)
            stick(self, out8[1], b148)
            self.play(GrowFromCenter(brace.brace), FadeIn(brace.text, shift=RIGHT * 0.1), run_time=0.7)

            vo.wait_until("and docker history")
            make_room(self, t7, 2)
            c9 = type_cmd(self, t7, HIST.cmd, 0.8)
            x9 = beside(extra_tag(), t7, c9)
            self.play(FadeIn(x9), run_time=0.3)
            stick(self, c9, x9)
            self.play(FadeOut(t7), FadeOut(brace), FadeIn(hpan, shift=UP * 0.2), run_time=0.7)
            hrows = hpan.rows
            self.play(LaggedStart(*[Indicate(hrows[i].glyphs, color=INK, scale_factor=1.04)
                                    for i in range(1, len(hrows)) if HIST_ROWS[i] != "…"], lag_ratio=0.15),
                      run_time=1.4)

            vo.wait_until("card-only lines")
            self.play(FadeIn(card, shift=UP * 0.1),
                      *[substring(hrows[i], "0B").animate.set_color(CTR) for i in ZERO], run_time=0.5)
            srcs, lines = [], []
            for i, word in ZERO.items():
                src = substring(hrows[i], word).copy()
                srcs.append(src)
                lines.append(card.line(word, INK, key=word, font="mono"))
            self.play(LaggedStart(*[Transform(s, ln) for s, ln in zip(srcs, lines)], lag_ratio=0.2), run_time=1.0)
            self.remove(*srcs)
            card.add(*lines)

            vo.wait_until("The uv sync layer")
            sizes = {}
            for i, name, txt, col in ((3, "sync", "105MB", VENV), (4, "copy", "193kB", LAPTOP),
                                      (7, "apt", "842MB", SYSTEM)):
                lab = mono(txt, 22, col)
                b = st.slabs[name].box
                place(lab, right=b.get_left()[0] - 0.2, cy=b.get_center()[1])
                sizes[name] = (substring(hrows[i], txt), lab)
            g, lab = sizes["sync"]
            st.attach(self, lab, anims=[ReplacementTransform(g.copy(), lab, path_arc=0.4)], run_time=0.9)
            self.play(Indicate(lab, color=VENV, scale_factor=1.25), run_time=0.6)
            st.attach(self, sizes["copy"][1], sizes["apt"][1],
                      anims=[ReplacementTransform(sizes["copy"][0].copy(), sizes["copy"][1], path_arc=0.4),
                             ReplacementTransform(sizes["apt"][0].copy(), sizes["apt"][1], path_arc=0.4)],
                      run_time=0.9)
            vo.wait_until("the packages plus")
            split = sans("= venv ≈ 50 MB + uv cache ≈ 58 MB", 20, INK, t2c={"venv ≈ 50 MB": VENV,
                                                                           "uv cache ≈ 58 MB": TOOL})
            place(split, right=lab.get_left()[0] - 0.25, cy=lab.get_center()[1])
            assert split.get_left()[0] > -EDGE and split.get_top()[1] < TRACK_BOTTOM - 0.05, split.get_corner(UL)
            st.attach(self, split, anims=[FadeIn(split, shift=RIGHT * 0.2)], run_time=0.6)
            self.play(Indicate(VGroup(sync.box, st.sync_chips), color=VENV, scale_factor=1.04), run_time=0.9)

        # ========================================================== 8 · a fresh container imports them
        t8 = term(P_A, MID)
        with self.voiceover(SAY[8]) as vo:
            st.detach(self, split, *[v[1] for v in sizes.values()], run_time=0.4,
                      extra=[FadeOut(hpan), FadeOut(card)])
            self.play(FadeIn(t8), run_time=0.4)
            c10 = type_cmd(self, t8, RUN, 1.1)
            x10 = beside(extra_tag(), t8, c10)
            top = st.slabs["sync"].box
            layer8 = new_layer(top, "new container", width=SLAB_W, h=0.42)
            assert layer8.get_top()[1] < 3.4 and layer8.get_left()[0] > tr.get_right()[0] + 0.3
            self.play(*enter_container(t8), FadeIn(x10), FadeIn(layer8, shift=DOWN * 0.3), run_time=0.6)
            stick(self, c10, x10)
            vo.wait_until("imports all three")
            c11 = type_cmd(self, t8, IMP_CMD, 1.5)
            x11 = beside(extra_tag(), t8, c11)
            out11 = t8.print(self, [(IMP_OUT[0], VENV)], run_time=0.3)
            self.play(FadeIn(x11), Indicate(out11[0], color=VENV, scale_factor=1.2), run_time=0.5)
            stick(self, c11, x11)
            vo.wait_until("they're baked in")
            self.play(Indicate(st.sync_chips, color=VENV, scale_factor=1.25),
                      Indicate(sync.label, color=VENV, scale_factor=1.1), run_time=0.9)
            make_room(self, t8, 1)
            type_cmd(self, t8, "exit", 0.3)
            self.play(*leave_container(t8, P_A), FadeOut(layer8, shift=UP * 0.4), run_time=0.6)

        # ========================================================== 9 · dominoes: any edit re-runs uv sync
        chip9 = edit_chip()
        note = VGroup(label("later tutorials: COPY pyproject.toml uv.lock first,", 22, S.GREY),
                      label("then uv sync, then the rest", 22, S.GREY)).arrange(DOWN, buff=0.12)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(t8), caption_extra(tr, False), run_time=0.5)
            self.play(st.animate.move_to(CENTRE, aligned_edge=DOWN), run_time=0.8)
            place(note, cx=0, top=st.floor.get_center()[1] - 0.35)
            cp, sync = st.slabs["copy"], st.slabs["sync"]
            place(chip9, left=cp.box.get_right()[0] + 0.5, cy=cp.box.get_center()[1] + 0.9)
            vo.wait_until("because the copy comes")
            self.play(Indicate(VGroup(cp.box, st.copy_files), color=INK, scale_factor=1.06), run_time=0.7)
            self.play(Indicate(VGroup(sync.box, sync.label, st.sync_chips), color=VENV, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("any edit")
            self.play(FadeIn(chip9, shift=LEFT * 0.2), run_time=0.5)
            saved_cp = cp.box.copy()
            self.play(chip9.animate.move_to(cp.box).scale(0.4).set_opacity(0),
                      cp.box.animate.set_stroke(TURN, 3).set_fill(TURN, 0.35), run_time=0.7)
            self.remove(chip9)
            self.play(Transform(cp.box, saved_cp), run_time=0.4)

            vo.wait_until("knocks over")
            sv_box, sv_lab = sync.box.copy(), sync.label.copy()
            sv_chips = st.sync_chips.copy()
            pivot = sync.box.get_center()            # knocked off: it slides right, its right end dipping
            fall = [m.animate.rotate(-0.45, about_point=pivot).shift(RIGHT * 1.5 + DOWN * 1.1).set_opacity(0)
                    for m in (sync.box, sync.label, st.sync_chips)]
            self.play(*fall, run_time=0.9, rate_func=rush_into)
            vo.wait_until("like lecture 2's")
            self.play(Transform(sync.box, sv_box), Transform(sync.label, sv_lab), run_time=0.6)
            st.sync_chips.become(sv_chips.copy().shift(UP * 1.4).set_opacity(0))
            self.play(Transform(st.sync_chips, sv_chips, lag_ratio=0.05), run_time=1.6)

            vo.wait_until("Later tutorials")
            self.play(FadeIn(note, shift=UP * 0.15), run_time=0.7)
            first = note[0]
            u9 = Line(first.get_corner(DL) + DOWN * 0.06, first.get_corner(DR) + DOWN * 0.06, color=TURN,
                      stroke_width=3.5)
            self.play(Create(u9), run_time=0.7)
            self.play(Indicate(VGroup(cp.box, st.copy_files), color=TURN, scale_factor=1.05), run_time=0.8)
        self.wait(0.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


def place_tag(tg, t, line) -> VGroup:
    """A live-view row's time tag at the row's right end, inside the frame."""
    return tg.move_to(line.strut).align_to(t.box, RIGHT).shift(LEFT * 0.12)
