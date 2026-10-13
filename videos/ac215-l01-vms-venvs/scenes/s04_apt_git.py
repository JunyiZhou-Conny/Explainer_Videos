"""S04 · apt, git and the repo (README steps 3-6, then an extra `ls`).

Beats (script.md "## S04", one voiceover block each):
 0  TRACKER A3. The house terminal (10 rows) types `sudo apt-get update`; `apt-get` and `sudo` get
    a short label each as they are named; then the real output (01-apt-update.txt lines 2-9, +Done)
    prints while an ORANGE "package catalog" book above the terminal flips a page per Get: line.
    Beside it a GREY "installed" shelf stays unchanged ("nothing new"). A GREY note: "on a Google
    VM: a few more lines (Google's package sources)". ▶ your turn.
 1  The terminal shrinks to the 3-row strip (the command, Fetched…, Reading… Done), the book and
    shelf shrink into the top-right corner.
    A GREY README quote card (README.md · line 48, the tip after step 4) appears; its phrases light
    up as they are spoken and condense into two ORANGE chips: `apt-get` "scripts · Dockerfiles · CI"
    and `apt` "humans at a terminal".
 2  TRACKER A4. The strip clears, the terminal grows to 12 rows and types `sudo apt install git` (02-git.txt lines
    4-6 +Done, …, 25-28 with [Y/n] Y, …, 160-161); the `Y` flashes YELLOW; a `git` box lands on
    the small "installed" shelf; GREY tag "package list varies by VM" on the elided list. ▶ your turn.
 3  TRACKER A5. A small GREY README card (line 50) with the clone command, which flashes YELLOW
    ("copy it from here"); `git clone https://github.com/dlops-io/simple-translate.git` folds onto
    two rows; "Cloning into 'simple-translate'..."; a BLUE folder drops into a "home" box.
 4  TRACKER A6. `cd simple-translate`; the next prompt shows ~/simple-translate (the new part
    flashes BLUE, the folder in the home box answers); GREY tag "~ = your home folder". ▶ your turn.
 5  TRACKER A6 · extra. `ls` (extra) -> 04-ls.txt lines 2-7; each file is pointed at as it is named
    (Dockerfile.txt: "L2 solution file"; pyproject.toml GREEN: "what the app needs"); two GREY
    dashed ghost chips `requirements.txt` and `uv.lock`, "not in the repo". Fade out.
"""

import re

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (CAPTION, MONO, OUTPUT, box, chip, folder_glyph, label, mono,
                              mono_line, substring, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, INK, NARRATION, P_HOME, P_REPO, SYSTEM, TURN, VENV, capture,
                    excerpt, extra_tag, term, tracker_a, your_turn)

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ commands (README spelling)
APT_UPDATE = "sudo apt-get update"
APT_GIT = "sudo apt install git"
CLONE = "git clone https://github.com/dlops-io/simple-translate.git"
CD = "cd simple-translate"
LS = "ls"

# ------------------------------------------------------------------ real outputs
_DONE = ("Reading package lists...", "Building dependency tree...", "Reading state information...")


def plus_done(lines):
    """apt prints ' Done' after its progress lines on a terminal (lost in the capture: ASSETS.md)."""
    return [s + " Done" if s in _DONE else s for s in lines]


_upd = capture("01-apt-update")
assert _upd.cmd == APT_UPDATE
UPDATE_OUT = plus_done(_upd.pick((1, 8)))                       # file lines 2-9
assert UPDATE_OUT[-1] == "Reading package lists... Done"
_git = capture("02-git")
assert _git.cmd.endswith(APT_GIT)                               # captured as `yes | sudo apt install git`
GIT_READ = plus_done(_git.pick((3, 5)))                         # file lines 4-6
GIT_SUM = _git.pick((24, 26))                                   # file lines 25-27
GIT_ASK = _git.pick(27)[0]                                      # file line 28
GIT_ASK = GIT_ASK[:GIT_ASK.index("[Y/n]") + len("[Y/n]")]       # cut after [Y/n]
# capture() reads with universal newlines, so apt's mid-line \r progress rows split into extra
# lines: file lines 160-161 are the last two body lines (checked here).
GIT_TAIL = _git.pick((-2, -1))
assert GIT_TAIL[0].startswith("Setting up git (") and GIT_TAIL[1].startswith("Processing triggers")
_clone = capture("03-clone")
assert _clone.cmd == CLONE
CLONE_OUT = _clone.pick(1)                                      # file line 2
_ls = capture("04-ls")
assert _ls.cmd == LS
LS_OUT = _ls.pick((1, 6))                                       # file lines 2-7

# README.md line 48 (the tip after step 4), as the README words it, broken into card rows
TIP48 = ["apt-get vs apt: Both manage Debian packages.",
         "apt-get is the older, stable, scriptable interface —",
         "predictable output, used in Dockerfiles and CI",
         "(we'll cover CI in a later lecture).",
         "apt is a friendlier wrapper for interactive use",
         "(progress bars, colors). Prefer apt-get in scripts;",
         "either is fine on a VM shell like this one."]


def _md_plain(s: str) -> str:
    """A README line as rendered text: no quote marker, bold or code backticks."""
    return s.lstrip("> ").replace("**", "").replace("`", "").lstrip("* ").strip()


# the card rows are the README's own words (checked against assets/source/README.md)
assert " ".join(TIP48) == _md_plain(excerpt("README.md", 48, 48)), "README line 48 changed"
CLONE_HEAD = "Clone App Repo:"
assert _md_plain(excerpt("README.md", 50, 50)) == f"{CLONE_HEAD} {CLONE}", "README line 50 changed"

# ------------------------------------------------------------------ layout
BOTTOM = -3.5            # terminal bottom edge (kept fixed when it grows or shrinks)
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
SMALL_K = 0.7            # the book and shelf in the corner (their 29 pt labels stay >= 20 pt)


def place_tracker(tr):
    tr.shift(np.array([TRACK_LEFT - tr.get_left()[0], TRACK_TOP - tr.get_top()[1], 0]))
    return tr


def caption_extra(tr, on: bool = True):
    """The tracker caption with (or without) ' · extra' while a non-README command is on screen."""
    k = tr.k
    s = f"step {k} of {len(tr.steps)}: {tr.steps[k - 1]}"
    new = label(s + " · extra", tr.size, tr.hi_color, t2c={"· extra": S.GREY}) if on else \
        label(s, tr.size, tr.hi_color)
    new.next_to(tr.dots, RIGHT, buff=0.25)
    return Transform(tr.caption, new)


def span(t: Text, sub: str) -> VGroup:
    """Glyphs of `sub` in a plain Text (Text.text holds the string without whitespace). Falls back
    to the whole text when `sub` isn't there (e.g. a translated label)."""
    k = "".join(sub.split())
    i = t.text.find(k)
    if i < 0:
        return VGroup(t)
    return VGroup(*t.submobjects[i:i + len(k)])


def tip_row(s: str) -> Text:
    """One row of a README quote; the commands apt-get and apt in ORANGE (apt, the OS's tool)."""
    t = label(s, 22, INK)
    for m in re.finditer(r"apt-get|\bapt\b", s):
        a = len("".join(s[:m.start()].split()))
        n = len("".join(m.group().split()))
        if t.text[a:a + n] == m.group():
            VGroup(*t.submobjects[a:a + n]).set_color(SYSTEM)
    return t


def under(g, color, y=None, stroke=4, pad=0.03) -> Line:
    """A line under glyphs `g` (at height y, default just under them)."""
    y = g.get_bottom()[1] - 0.06 if y is None else y
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def line_under(line, sub, color):
    """Underline the substring `sub` of a terminal row, under the row's descenders."""
    return under(substring(line, sub), color, y=line.strut.get_bottom()[1] - 0.01)


def condense(scene, src, target, chip_mob, run_time=1.0):
    """The highlighted words lift off the card (a copy) and fly, still crisp, to the caption's
    place; only there do they cross-fade into the short caption while the chip forms above it, so
    nothing blends over the card's own text."""
    fly = VGroup(*[m.copy() for m in src])
    w = min(fly.width, target.width)
    scene.play(fly.animate(path_arc=-0.35).scale_to_fit_width(w).move_to(target), run_time=0.55 * run_time)
    scene.play(FadeTransform(fly, target, stretch=False, dim_to_match=0),
               FadeIn(chip_mob, shift=UP * 0.2), run_time=0.45 * run_time)


def hl_bar(g, color=TURN, opacity=0.25, buff=0.05) -> Rectangle:
    """A translucent highlight bar behind glyphs `g`."""
    return Rectangle(width=g.width + 2 * buff, height=g.height + 2 * buff, stroke_width=0) \
        .set_fill(color, opacity).move_to(g)


# ------------------------------------------------------------------ pictures
def catalog_book(h: float = 1.0, color=SYSTEM) -> VGroup:
    """An open ORANGE book (apt's package catalog). .right_page flips over the spine (.spine)."""
    w = h * 0.8
    cover = RoundedRectangle(width=2 * w + 0.2, height=h + 0.16, corner_radius=0.07,
                             stroke_color=color, stroke_width=3).set_fill(color, 0.3)

    def page(sign):
        p = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2).set_fill(S.BG, 1)
        p.move_to([sign * w / 2, 0, 0])
        rows = VGroup()
        for k, f in enumerate((0.75, 0.55, 0.7, 0.45, 0.65)):
            y = h / 2 - 0.2 - k * (h - 0.35) / 4.5
            x0 = sign * 0.12 if sign > 0 else -w + 0.12
            rows.add(Line([x0, y, 0], [x0 + f * (w - 0.24), y, 0], color=color, stroke_width=2.5,
                          stroke_opacity=0.75))
        return VGroup(p, rows)

    left, right = page(-1), page(1)
    spine = Line([0, h / 2, 0], [0, -h / 2, 0], color=color, stroke_width=3)
    g = VGroup(cover, left, right, spine)
    g.left_page, g.right_page, g.spine = left, right, spine
    return g


def parcel(s: float = 0.34, color=S.GREY) -> VGroup:
    """A small package box (an installed Debian package)."""
    b = Square(side_length=s, stroke_color=color, stroke_width=2.5).set_fill(color, 0.2)
    tape = Line(b.get_top(), b.get_bottom(), color=color, stroke_width=2)
    return VGroup(b, tape)


def installed_shelf(w: float = 2.9) -> VGroup:
    """A GREY shelf of what is installed on the VM: a board, a few package boxes, a label."""
    board = Line(LEFT * w / 2, RIGHT * w / 2, color=S.GREY, stroke_width=5)
    boxes = VGroup(*[parcel() for _ in range(3)]).arrange(RIGHT, buff=0.1)
    boxes.next_to(board, UP, buff=0.04).align_to(board, LEFT).shift(RIGHT * 0.15)
    g = VGroup(board, boxes)
    g.board, g.boxes = board, boxes
    return g


def readme_card(line_no: int, body: VGroup, extra: str = "", quote: bool = False,
                width: float | None = None) -> VGroup:
    """A GREY README card: header 'README.md · line n' and the README's own words.
    quote=True draws a markdown-style quote bar at the left of the body."""
    head = VGroup(mono("README.md", CAPTION, S.GREY), label(f"· line {line_no}{extra}", CAPTION, S.GREY))
    head.arrange(RIGHT, buff=0.12)
    if quote:
        bar = Line(body.get_corner(UL) + np.array([-0.22, 0.04, 0]),
                   body.get_corner(DL) + np.array([-0.22, -0.04, 0]), color=S.GREY, stroke_width=4)
        body = VGroup(bar, body)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    frame = box(width or inner.width + 0.55, inner.height + 0.4, S.GREY, fill=S.GREY_DARKER,
                fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.28)
    g = VGroup(frame, inner)
    g.frame, g.head = frame, head
    return g


def row_tag(parts, color=S.GREY, size: float = 22) -> VGroup:
    """A tag that fits inside one terminal row (the house tag is taller than a row and would
    touch the rows above and below). parts: a string, or (text, 'mono'|'label') pairs."""
    if isinstance(parts, str):
        parts = [(parts, "label")]
    t = VGroup(*[mono(x, size, color) if k == "mono" else label(x, size, color) for x, k in parts])
    t.arrange(RIGHT, buff=0.12)
    h = 0.37
    b = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=h / 2, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def beside(mob, line, buff=0.45, min_x=None):
    """Put `mob` right of terminal row `line`, centred on the row (left edge at least min_x)."""
    x = line.strut.get_right()[0] + buff
    if min_x is not None:
        x = max(x, min_x)
    return mob.move_to([x + mob.width / 2, line.strut.get_center()[1], 0])


def ghost_chip(s: str) -> VGroup:
    """Something that is merely absent: a GREY dashed chip."""
    t = mono(s, 24, S.GREY)
    h = mono("|", 24).height + 0.26
    b = box(t.width + 0.5, h, S.GREY, dashed=True, radius=h / 2.6)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


class AptAndGit(VoiceScene):
    # ------------------------------------------------------------- terminal helpers (as in S09)
    def bare_prompt(self, t):
        """The prompt returns (no output): a prompt line with nothing typed yet."""
        ln = t.type(self, "", type_time=0)
        ln.bare = True
        return ln

    def type_cmd(self, t, cmd, type_time=None):
        """Type at the waiting prompt (replacing a bare prompt line if there is one)."""
        if len(t.lines) and getattr(t.lines[-1], "bare", False):
            last = t.lines[-1]
            self.remove(last, *last.submobjects)
            t.lines.remove(last)
        return t.type(self, cmd, type_time)

    def pin(self, line, mob, run_time=0.4, anim=None):
        """Show `mob` beside a terminal line and make it part of that line (it scrolls with it)."""
        self.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
        return self.attach(line, mob)

    def attach(self, line, mob):
        """Make `mob` part of terminal row `line`. Animating a substring of a row (a new VGroup of
        its glyphs) makes Scene.add split the row out of the scene's list, so re-add the row:
        otherwise a mark added to it would not be drawn."""
        self.remove(mob)
        line.add(mob)
        self.add(line)
        return mob

    def unpin(self, pairs, run_time=0.3, *extra):
        """Fade out pinned marks and take them off their lines."""
        self.play(*[FadeOut(m) for _, m in pairs], *extra, run_time=run_time)
        for line, m in pairs:
            if m in line.submobjects:
                line.remove(m)

    def type_yes(self, t, ln, text, asked_at, pause=0.6):
        """The `Y` keystroke after apt's question `ln` (printed at time `asked_at`): at least
        `pause` s after the question (script.md: [Y/n] Y), then it flashes YELLOW. Returns Y."""
        left = asked_at + pause - self.renderer.time
        if left > 1 / 60:
            self.wait(left)
        y = mono_line(text + " Y", t.size, OUTPUT)
        y.shift(ln.strut.get_corner(UL) - y.strut.get_corner(UL))
        yg = y.glyphs[-1].set_color(TURN)
        self.play(FadeIn(yg, scale=1.6), run_time=0.2)
        self.play(Indicate(yg, color=TURN, scale_factor=1.8), run_time=0.5)
        self.play(yg.animate.set_color(INK), run_time=0.2)
        self.attach(ln, yg)
        return yg

    def resize(self, t, rows, run_time=0.8, extra=(), keep=None):
        """Grow or shrink the terminal to `rows` (bottom edge fixed). It keeps its last lines (at
        most `keep` of them), or, when `keep` is a list of line mobjects, exactly those lines."""
        ref = term(prompt=t.prompt, rows=rows)
        ref.shift(np.array([-ref.box.get_center()[0], BOTTOM - ref.box.get_bottom()[1], 0]))
        if isinstance(keep, (list, tuple)):
            assert len(keep) <= rows
            kept = [ln for ln in t.lines.submobjects if ln in keep]
        else:
            n_keep = min(len(t.lines), rows, len(t.lines) if keep is None else keep)
            kept = t.lines.submobjects[len(t.lines) - n_keep:]
        gone = [ln for ln in t.lines.submobjects if ln not in kept]
        if gone:                       # first the lines that go (nothing slides through them)
            self.play(FadeOut(VGroup(*gone)), run_time=0.25)
            for ln in gone:
                t.lines.remove(ln)
                self.remove(ln)
        anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar),
                 t.dots.animate.move_to(ref.dots), t.title.animate.move_to(ref.title)]
        for i, ln in enumerate(kept):
            anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
        self.play(*anims, *extra, run_time=run_time)
        t.rows = rows
        return t

    def flip(self, book, run_time=0.4):
        """Turn one page of the book (the right page swings over the spine)."""
        pg = book.right_page.copy()
        self.add(pg)
        self.play(pg.animate.stretch(-1, 0, about_point=book.spine.get_center()), run_time=run_time,
                  rate_func=smooth)
        self.remove(pg)

    # ------------------------------------------------------------- the scene
    def construct(self):
        assert len(SAY) == 6, f"S04 has {len(SAY)} SAY lines; this scene times 6"

        tr = place_tracker(tracker_a(2))

        # ========================================================== 0 · sudo apt-get update
        t = term(prompt=P_HOME, rows=10)
        t.shift(np.array([-t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))

        book = catalog_book()
        book_lbl = label("package catalog", 29, SYSTEM).next_to(book, DOWN, buff=0.16)
        book_g = VGroup(book, book_lbl)
        shelf = installed_shelf()
        shelf_lbl = label("installed", 29, S.GREY).next_to(shelf.board, DOWN, buff=0.16)
        shelf_g = VGroup(shelf, shelf_lbl)
        shelf_g.next_to(book_g, RIGHT, buff=1.0).align_to(book_g, DOWN)
        pic = VGroup(book_g, shelf_g)
        pic.move_to([3.05, 0, 0]).align_to(t.box, UP).shift(UP * (pic.height + 0.3))
        nothing = tag("nothing new", S.GREY).next_to(shelf.boxes, UP, buff=0.18)
        nothing.align_to(shelf.board, LEFT)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            self.play(tr.goto(3), run_time=0.5)
            cmd0 = self.type_cmd(t, APT_UPDATE, 0.9)

            vo.wait_until("Debian's package manager")
            apt_g = substring(cmd0, "apt-get")
            ul_apt = line_under(cmd0, "apt-get", SYSTEM)
            lab_apt = label("Debian's package manager", 22, SYSTEM)
            lab_apt.move_to([apt_g.get_left()[0] - 0.03, t._slot(1)[1] - 0.17, 0], aligned_edge=LEFT)
            self.play(Create(ul_apt), apt_g.animate.set_color(SYSTEM), FadeIn(lab_apt, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("and sudo runs it")
            sudo_g = substring(cmd0, "sudo")
            ul_sudo = line_under(cmd0, "sudo", INK)
            lab_sudo = label("runs it as the administrator", 22, S.GREY)
            lab_sudo.move_to([sudo_g.get_left()[0] - 0.03, t._slot(1)[1] - 0.17, 0], aligned_edge=LEFT)
            self.play(FadeOut(VGroup(ul_apt, lab_apt)), apt_g.animate.set_color(INK), run_time=0.3)
            self.play(Create(ul_sudo), FadeIn(lab_sudo, shift=UP * 0.1), run_time=0.5)

            vo.wait_until("Update downloads")
            upd_g = substring(cmd0, "update")
            self.play(FadeOut(VGroup(ul_sudo, lab_sudo)), FadeIn(pic, shift=DOWN * 0.15),
                      Indicate(upd_g, color=SYSTEM, scale_factor=1.15), run_time=0.6)
            # one page turns for every Get: line apt downloads
            gets = [s for s in UPDATE_OUT if s.startswith("Get:")]
            rest = UPDATE_OUT[len(gets):]
            for s in gets:
                t.print(self, [s], run_time=0.18)
                self.flip(book, 0.32)
            t.print(self, rest, run_time=0.4)
            p_after = self.bare_prompt(t)
            vo.wait_until("and their latest versions")
            self.play(Indicate(book_g, color=SYSTEM, scale_factor=1.06), run_time=0.8)

            vo.wait_until("Nothing is installed yet")
            self.play(Indicate(shelf, color=S.WHITE, scale_factor=1.06), FadeIn(nothing, shift=DOWN * 0.1),
                      run_time=0.7)

            vo.wait_until("On a Google VM")
            note = VGroup(label("on a Google VM: a few more lines", 22, S.GREY),
                          label("(Google's package sources)", 22, S.GREY)).arrange(DOWN, aligned_edge=LEFT,
                                                                                   buff=0.1)
            note.arrange(DOWN, aligned_edge=LEFT, buff=0.06)
            nbox = box(note.width + 0.4, note.height + 0.14, S.GREY, fill=S.BG, fill_opacity=0.95)
            note.move_to(nbox)
            note_g = VGroup(nbox, note)
            l_fetch, l_read = t.find("Fetched"), t.find("Reading package lists")
            # beside the short rows at the bottom (clear of the long Get:6 row above them)
            note_g.move_to([5.9 - note_g.width / 2, l_read.strut.get_center()[1], 0])
            self.play(FadeIn(note_g, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("for Google's own")
            get_rows = VGroup(*[ln for ln in t.lines if ln.text.startswith("Get:")])
            self.play(Indicate(get_rows, color=S.WHITE, scale_factor=1.02), run_time=1.0)

            vo.wait_until("Pause and run it")
            yt0 = beside(your_turn(), cmd0).shift(UP * 0.04)       # the Get: row below is long
            self.pin(cmd0, yt0, run_time=0.4)

        # ========================================================== 1 · the README tip: apt-get vs apt
        rows = VGroup(*[tip_row(s) for s in TIP48]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card48 = readme_card(48, rows, " (tip after step 4)", quote=True)
        card48.move_to([TRACK_LEFT + card48.width / 2, 2.72 - card48.height / 2, 0])
        hl_same = span(rows[0], "Both manage Debian packages.")
        hl_stable = span(rows[1], "stable, scriptable interface")
        hl_ci = span(rows[2], "used in Dockerfiles and CI")
        hl_human = span(rows[4], "friendlier wrapper for interactive use")
        hl_either = span(rows[6], "either is fine on a VM shell like this one.")

        c_get = chip("apt-get", SYSTEM, size=28, font=MONO)
        cap_get = label("scripts · Dockerfiles · CI", 24, INK)
        g_get = VGroup(c_get, cap_get).arrange(DOWN, buff=0.14)
        c_apt = chip("apt", SYSTEM, size=28, font=MONO)
        cap_apt = label("humans at a terminal", 24, INK)
        g_apt = VGroup(c_apt, cap_apt).arrange(DOWN, buff=0.14)
        chips = VGroup(g_get, g_apt).arrange(DOWN, buff=0.5)
        strip_top = BOTTOM + term(rows=3).box.height
        small_h = pic.height * SMALL_K
        corner = np.array([6.5 - pic.width * SMALL_K / 2, 3.52 - small_h / 2, 0])
        chips.move_to([4.5, (3.52 - small_h + strip_top) / 2, 0])

        with self.voiceover(SAY[1]) as vo:
            self.unpin([(cmd0, yt0)], 0.3, FadeOut(note_g), FadeOut(nothing))
            # the strip keeps the command and its key output lines (script.md: terminal width)
            self.resize(t, 3, run_time=0.8, keep=[cmd0, l_fetch, l_read],
                        extra=[pic.animate.scale(SMALL_K).move_to(corner)])
            self.play(FadeIn(card48, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("do the same job")
            bars = {}

            def light(key, g, rt=0.5):
                bars[key] = hl_bar(g)
                self.play(FadeIn(bars[key]), run_time=rt)

            light("same", hl_same)
            vo.wait_until("the stable, scriptable one")
            light("stable", hl_stable)
            vo.wait_until("for Dockerfiles")
            light("ci", hl_ci)
            # the highlighted words travel to the chip and become its caption
            condense(self, VGroup(*hl_stable, *hl_ci), cap_get, c_get)

            vo.wait_until("The shorter apt")
            light("human", hl_human)
            condense(self, hl_human, cap_apt, c_apt)

            vo.wait_until("Either is fine")
            light("either", hl_either, 0.3)
            self.play(FadeOut(VGroup(card48, *bars.values()), scale=0.3, target_position=chips.get_center()),
                      Indicate(chips, color=S.WHITE, scale_factor=1.06), run_time=0.8)

        # ========================================================== 2 · sudo apt install git
        git_box = VGroup(parcel(color=S.WHITE).scale(SMALL_K), mono("git", 20, INK)).arrange(RIGHT, buff=0.1)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(chips), tr.goto(4), run_time=0.4)
            self.resize(t, 12, run_time=0.7, keep=0)
            cmd2 = self.type_cmd(t, APT_GIT, 0.9)

            vo.wait_until("This time apt")
            t.print(self, GIT_READ, run_time=0.5)
            dots1 = t.print(self, ["…"], run_time=0.2)[0]
            self.play(Indicate(shelf, color=S.WHITE, scale_factor=1.1), run_time=0.6)

            vo.wait_until("It lists what")
            summ = t.print(self, GIT_SUM, run_time=0.5)
            ul_sum = line_under(summ[0], "1 upgraded, 25 newly installed", TURN)
            self.play(Create(ul_sum), run_time=0.5)
            vo.wait_until("do you want to continue")
            self.play(FadeOut(ul_sum), run_time=0.2)
            ask = t.print(self, [GIT_ASK], run_time=0.3)[0]
            asked_at = self.renderer.time
            vo.wait_until("Type Y")
            self.type_yes(t, ask, GIT_ASK, asked_at, pause=0.6)
            vo.wait_until("press enter")
            tail = t.print(self, ["…", *GIT_TAIL], run_time=0.5)
            # git joins the installed packages on the shelf
            git_box.next_to(shelf.boxes, RIGHT, buff=0.1 * SMALL_K)
            board_y = shelf.board.get_center()[1]          # the box and its name both stand on the
            git_box[0].shift(UP * (board_y + 0.03 - git_box[0].get_bottom()[1]))   # board ("g" clears it)
            git_box[1].shift(UP * (board_y + 0.07 - git_box[1].get_bottom()[1]))
            land = git_box.get_center()
            git_box.shift(substring(tail[1], "git").get_center() - git_box[1].get_center())
            self.play(git_box.animate.move_to(land), path_arc=-0.5, run_time=0.8)
            self.play(git_box[0].animate.set_stroke(S.GREY).set_fill(S.GREY, 0.2), run_time=0.3)

            vo.wait_until("The list depends")
            vary = beside(row_tag("package list varies by VM"), dots1)
            self.pin(dots1, vary, run_time=0.5)
            vo.wait_until("if git is already there")
            self.play(Indicate(git_box, color=S.WHITE, scale_factor=1.4), run_time=0.8)

            vo.wait_until("Pause and run it")
            yt2 = beside(your_turn(), cmd2)
            self.pin(cmd2, yt2, run_time=0.4)

        # ========================================================== 3 · git clone
        home_box = box(3.3, 2.25, CLOUD, fill_opacity=0.06)
        home_lbl = label("home", 26, CLOUD)
        home_head = VGroup(home_lbl).move_to(home_box.get_top() + DOWN * 0.3)
        home = VGroup(home_box, home_head).move_to([6.5 - 1.65, 1.95, 0])
        folder = folder_glyph(0.85, CLOUD)
        folder_name = mono("simple-translate", 22, INK).next_to(folder, DOWN, buff=0.12)
        repo = VGroup(folder, folder_name).move_to(home_box.get_center() + DOWN * 0.28)

        url = CLONE.split()[-1]                                   # README line 50, as checked above
        r1 = VGroup(label(CLONE_HEAD, 22, INK), mono(CLONE[:-len(url)].strip(), 22, INK)) \
            .arrange(RIGHT, buff=0.18)
        r2 = mono(url, 22, INK)
        body50 = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card50 = readme_card(50, body50)
        card50.move_to([TRACK_LEFT + card50.width / 2, 2.72 - card50.height / 2, 0])
        cmd50 = VGroup(r1[1], r2)
        copy_tag = tag("copy it from here", TURN)
        copy_tag.move_to([card50.frame.get_right()[0] - 0.25 - copy_tag.width / 2, r1.get_center()[1], 0])

        with self.voiceover(SAY[3]) as vo:
            self.unpin([(cmd2, yt2), (dots1, vary)], 0.3, FadeOut(VGroup(pic, git_box)), tr.goto(5))
            t.clear(self, run_time=0.3)
            self.resize(t, 8, run_time=0.6)

            vo.wait_until("Type git clone")
            self.play(FadeIn(card50, shift=DOWN * 0.1), run_time=0.5)
            bar50 = VGroup(hl_bar(r1[1], TURN, 0.22), hl_bar(r2, TURN, 0.22))
            self.play(FadeIn(bar50), Indicate(cmd50, color=TURN, scale_factor=1.04), run_time=0.7)
            clone_cmd = self.type_cmd(t, CLONE, 1.4)

            vo.wait_until("copy it from the README")
            self.play(FadeIn(copy_tag, shift=UP * 0.1), Indicate(cmd50, color=TURN, scale_factor=1.04),
                      run_time=0.7)

            vo.wait_until("Git copies the whole repo")
            cl_out = t.print(self, CLONE_OUT, run_time=0.4)[0]
            self.play(Indicate(substring(cl_out, "'simple-translate'"), color=CLOUD, scale_factor=1.1),
                      FadeIn(home, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("into a new folder")
            repo.shift(UP * 1.6)
            repo.set_opacity(0)
            self.play(repo.animate.shift(DOWN * 1.6).set_opacity(1), run_time=0.8, rate_func=rush_from)
            vo.wait_until("in your home directory")
            self.play(Indicate(home_lbl, color=S.WHITE, scale_factor=1.25),
                      home_box.animate.set_stroke(width=4), run_time=0.7)

        # ========================================================== 4 · cd simple-translate
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(card50, bar50, copy_tag)), tr.goto(6),
                      home_box.animate.set_stroke(width=2.5), run_time=0.5)
            cd_line = self.type_cmd(t, CD, 0.7)
            t.set_prompt(P_REPO)
            p_repo = self.bare_prompt(t)

            vo.wait_until("Watch the prompt")
            self.play(Indicate(p_repo, color=S.WHITE, scale_factor=1.04), run_time=0.7)
            vo.wait_until("after the colon")
            colon = substring(p_repo, ":")
            self.play(Indicate(colon, color=TURN, scale_factor=2.0), run_time=0.6)
            vo.wait_until("it now shows the folder")
            new_part = substring(p_repo, "/simple-translate")
            ul_new = line_under(p_repo, "/simple-translate", CLOUD)
            self.play(Indicate(new_part, color=CLOUD, scale_factor=1.2), Create(ul_new),
                      Indicate(repo, color=CLOUD, scale_factor=1.12), run_time=0.9)
            self.attach(p_repo, ul_new)

            vo.wait_until("The wavy tilde")
            tilde = substring(p_repo, "~")
            ttag = row_tag([("~", "mono"), ("= your home folder", "label")])
            row_below = t._slot(len(t.lines))[1] - t.pitch / 2 + 0.04
            ttag.shift(np.array([tilde.get_center()[0] - ttag.text[0].get_center()[0],
                                 row_below - ttag.get_center()[1], 0]))
            self.play(Indicate(tilde, color=S.WHITE, scale_factor=1.8), run_time=0.6)
            self.play(FadeIn(ttag, shift=UP * 0.1), Indicate(home_head, color=S.WHITE, scale_factor=1.12),
                      run_time=0.7)

            vo.wait_until("Pause, and catch up")
            yt4 = beside(your_turn(), p_repo, min_x=cd_line.strut.get_right()[0] + 0.35)
            self.pin(p_repo, yt4, run_time=0.4)

        # ========================================================== 5 · ls (extra)
        with self.voiceover(SAY[5]) as vo:
            self.unpin([(p_repo, yt4), (p_repo, ul_new)], 0.4, FadeOut(ttag),
                       FadeOut(VGroup(home, repo)), caption_extra(tr))
            self.resize(t, 11, run_time=0.5)
            ls_line = self.type_cmd(t, LS, 0.3)
            xt = beside(extra_tag(), ls_line, buff=0.4)
            self.pin(ls_line, xt, run_time=0.4)

            vo.wait_until("lists the files")                 # the output follows the command
            files = t.print(self, LS_OUT, run_time=0.6)
            row = {ln.text: ln for ln in files}
            vo.wait_until("There's cli.py")

            def point(name, color=S.WHITE):
                self.play(Indicate(row[name].glyphs, color=color, scale_factor=1.15), run_time=0.6)

            point("cli.py")
            vo.wait_until("the README")
            point("README.md")
            vo.wait_until("a Dockerfile saved")
            l2 = beside(row_tag("L2 solution file"), row["Dockerfile.txt"])
            self.play(Indicate(row["Dockerfile.txt"].glyphs, color=S.WHITE, scale_factor=1.15),
                      FadeIn(l2, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("two scripts")
            s1, s2 = row["docker-build-push.sh"], row["docker-shell.sh"]
            bx = s1.strut.get_right()[0] + 0.3
            brk = VMobject(stroke_color=S.GREY, stroke_width=2.5).set_points_as_corners([
                [bx, s1.strut.get_top()[1] - 0.04, 0], [bx + 0.15, s1.strut.get_top()[1] - 0.04, 0],
                [bx + 0.15, s2.strut.get_bottom()[1] + 0.04, 0], [bx, s2.strut.get_bottom()[1] + 0.04, 0]])
            nl = label("next lecture", 22, S.GREY).next_to(brk, RIGHT, buff=0.2)
            self.play(Indicate(VGroup(s1.glyphs, s2.glyphs), color=S.WHITE, scale_factor=1.08),
                      Create(brk), FadeIn(nl), run_time=0.8)
            vo.wait_until("and pyproject.toml")
            pp = row["pyproject.toml"]
            # the row's full height, the name's width (the strut starts a little left of the name)
            pbar = Rectangle(width=pp.glyphs.width + 0.12, height=pp.strut.height + 0.06, stroke_width=0) \
                .set_fill(VENV, 0.22).move_to([pp.glyphs.get_center()[0], pp.strut.get_center()[1], 0])
            need = beside(row_tag("what the app needs", VENV), pp)
            self.play(FadeIn(pbar), pp.glyphs.animate.set_color(VENV), run_time=0.5)
            self.play(FadeIn(need, shift=LEFT * 0.1), Indicate(pp.glyphs, color=VENV, scale_factor=1.15),
                      run_time=0.7)

            vo.wait_until("Notice what's missing")
            req, lock = ghost_chip("requirements.txt"), ghost_chip("uv.lock")
            ghosts = VGroup(req, lock).arrange(DOWN, buff=0.3)
            missing = label("not in the repo", 24, S.GREY)
            gg = VGroup(ghosts, missing).arrange(DOWN, buff=0.25)
            gg.move_to([4.0, 0, 0]).align_to(row["README.md"].strut, UP)
            self.play(Indicate(VGroup(*[ln.glyphs for ln in files]), color=S.WHITE, scale_factor=1.03),
                      run_time=0.8)
            vo.wait_until("no requirements file")
            self.play(FadeIn(req, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("and no lock file")
            self.play(FadeIn(lock, shift=LEFT * 0.15), run_time=0.6)
            self.play(FadeIn(missing, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Hold on to that")
            self.play(Indicate(ghosts, color=S.WHITE, scale_factor=1.08),
                      Indicate(pp.glyphs, color=VENV, scale_factor=1.12), run_time=0.9)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
