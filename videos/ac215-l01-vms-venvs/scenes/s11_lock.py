"""S11 · uv sync: resolve, lock, install (part 2: the rest of the uv sync output, V5 wish list ->
receipt, why 11 here and 12 elsewhere, the uv.lock erratum).

Beats (script.md "## S11", one voiceover block each):
 0  TRACKER B9. The `uv sync` terminal of S10 returns (7 rows, full width) with 08-uv-sync.txt
    lines 2-5 and a GREY curtain over the rest; above, CODE(pyproject.toml: 7-10) with a GREEN
    brace and "2" badge; an ORANGE chip "part 1: pip installed 12". PONDER(6 s) over the terminal.
 1  The curtain lifts (the terminal grows to 8 rows); lines 6-8 print, `Installed 11 packages`
    gets a YELLOW bar and its "11" lifts into a GREEN counter chip at left; lines 9-19 print in two
    batches and every `+` line is copied as a GREEN chip into two rows above the terminal (the
    deviation from "a column at left": a full-width terminal leaves no column beside it).
    art/googletrans circled YELLOW, the other 9 wave, a GREY dashed "?" chip for the missing one.
 2  V5. The terminal shrinks to a 3-row strip; the 11 chips move to their places in the tree as
    dim ghosts, art and googletrans become the two wishes `art>=6.5` / `googletrans==4.0.2`; the
    counter goes top right ("11 packages"). TRACKER B9 · extra. `uv tree` (extra) ->
    17-tree.txt lines 2-16, printed group by group with the narration: each line's name flies to
    its node, which lights up, and its edge grows from the parent. The repeated certifi and idna
    rows add a second incoming edge to the existing node.
 3  The strip goes; the tree opens up and every package gets its exact version tag (17-tree.txt);
    the edges flash GREEN ("fit together"); the tree rolls up into a GREEN `uv.lock` scroll with
    two real snippets of 18-lock-head.txt line 14 (url, hash); then CODE(pyproject.toml: 7-10)
    "wish list" beside the scroll "receipt".
 4  The scroll unrolls into a compact tree; a tally top right: "11 + app = 12" ... ; the app gets a
    GREY tag "the project itself · not downloaded"; PANEL(18-lock-head.txt: 6-13, "uv.lock · lines
    5-12 (generated on your VM)") at 20 pt under the tree; capture line 4 flashes as a chip "one
    lock for every allowed Python"; uv.lock line 11 YELLOW; a hollow dashed GREEN node
    typing-extensions hangs off anyio, edge "python < 3.15"; the tally completes
    "11 + app + typing-extensions = 13 resolved".
 5  The panel fades; "11 on 3.15" under the dashed node; two cards fill it in: a part-1 shelf
    (08-pip-break.txt line 35, `typing_extensions-4.16.0` named) "12 on 3.11", and a GREY "Debian 13"
    card (debian13-part-b/08-uv-sync.txt lines 6, …, 18) "12 on 3.13".
 6  Illustration: two GREY students a week apart ("Monday", "next Monday") with a copy of the tree;
    without a shared lock two of the second student's leaf tags flip to GREY dashed "newer?"; the
    GREEN uv.lock scroll is handed over and every tag snaps back, GREEN check.
 7  TRACKER B9 · extra. Terminal (13 rows): `ls -a` (extra) -> 09-ls-after.txt lines 2-14 (the
    command row scrolls off: 14 rows don't fit under the tracker), `.venv` and `uv.lock` GREEN +
    "new"; `git status` (extra) -> 19-git-status.txt lines 2-9, the untracked `uv.lock` YELLOW.
 8  README card (README.md · line 70), YELLOW note "the repo has no uv.lock yet", GREY "erratum";
    GREEN fixes "commit uv.lock" (the scroll flies into a `simple-translate/` folder,
    `git add uv.lock`) and "in CI: uv sync --locked" (a CI box: matching lock -> GREEN check,
    missing lock -> RED stop).
 9  `uv sync` again (extra) -> 23-resync.txt lines 2-3, `Checked 11 packages in 0.14ms` GREEN;
    fade out.
"""

import re

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon, ponder_card
from explainer.devops import (CAPTION, HOUSE_CODE_STYLE, MONO, OUTPUT, PANEL, box, check_mark, chip,
                              code_panel, code_span, folder_glyph, label, line_bar, mono, mono_line,
                              substring, tag)
from explainer.scene import VoiceScene

from common import (ERR, INK, NARRATION, P_REPO, SYSTEM, TURN, UV, VENV, capture, excerpt,
                    illustration_tag, jar, term, tracker_b)

SAY = NARRATION["S11"]
PA, PB, PB13 = "debian12-part-a", "debian12-part-b", "debian13-part-b"

# ------------------------------------------------------------------ real sources and outputs
TOML_DEPS = excerpt("pyproject.toml", 7, 10)
assert TOML_DEPS.split("\n")[1].strip() == '"art>=6.5",'

_sync = capture("08-uv-sync", PB)
assert _sync.cmd == "uv sync"
SYNC_HEAD = _sync.pick((1, 4))                      # file lines 2-5 (S10 showed them)
SYNC_RES = _sync.pick((5, 7))                       # file lines 6-8
SYNC_PLUS = _sync.pick((8, 18))                     # file lines 9-19
assert SYNC_RES[0].startswith("Resolved 13 packages") and SYNC_RES[2].startswith("Installed 11 packages")
assert len(SYNC_PLUS) == 11 and all(s.startswith(" + ") for s in SYNC_PLUS)
PKGS = [s[3:].split("==")[0] for s in SYNC_PLUS]   # in uv's (alphabetical) order

_tree = capture("17-tree", PB)
assert _tree.cmd == "uv tree"
TREE_OUT = _tree.pick((1, 15))                      # file lines 2-16


def parse_tree(lines):
    """(name, parent, version) for each row of `uv tree` (4 characters per level)."""
    rows, stack = [], []
    for s in lines:
        m = re.search(r"[a-z]", s)
        depth = m.start() // 4
        full, ver = s[m.start():].split()[:2]
        name = full.split("[")[0]
        stack = stack[:depth] + [name]
        rows.append((name, stack[depth - 1] if depth else None, ver))
    return rows


TREE = parse_tree(TREE_OUT[1:])                     # file lines 3-16
VERS = {n: v for n, _, v in TREE}
assert set(VERS) - {"app"} == set(PKGS) and len(TREE) == 14

_lock = capture("18-lock-head", PB)
LOCK = _lock.pick((5, 12))                          # file lines 6-13 = uv.lock lines 5-12
assert LOCK[6].strip().startswith('{ name = "typing-extensions", marker')
LOCK_RP = _lock.pick(3)[0]                          # file line 4 = uv.lock line 3
assert LOCK_RP == 'requires-python = ">=3.13"'
_sdist = _lock.pick(13)[0]                          # file line 14: the sdist entry
URL_SNIP = 'url = "' + re.search(r'url = "(https://[^/]+/)', _sdist).group(1) + '…"'
HASH_SNIP = 'hash = "' + re.search(r'hash = "(sha256:[0-9a-f]{10})', _sdist).group(1) + '…"'

_pip = capture("08-pip-break", PA).pick(34)[0]      # file line 35
assert _pip.startswith("Successfully installed") and len(_pip.split()) == 14
TE_PIP = _pip.split()[-1]
assert TE_PIP == "typing_extensions-4.16.0"

D13 = capture("08-uv-sync", PB13).pick(5, 17)       # file lines 6, …, 18
assert D13[0].startswith("Installed 12 packages") and D13[2] == " + typing-extensions==4.16.0"

_ls = capture("09-ls-after", PB)
assert _ls.cmd == "ls -a"
LS_OUT = _ls.pick((1, 13))                          # file lines 2-14
_gs = capture("19-git-status", PB)
assert _gs.cmd == "git status"
GS_OUT = [s.expandtabs(8) for s in _gs.pick((1, 8))]   # file lines 2-9 (a tab shows as 8 columns)
_re = capture("23-resync", PB)
assert _re.cmd == "uv sync"
RE_OUT = _re.pick((1, 2))                           # file lines 2-3
assert RE_OUT[1].startswith("Checked 11 packages")

README70 = excerpt("README.md", 70, 70)
assert "`uv.lock` pins exact versions so the next person gets the same setup" in README70

# ------------------------------------------------------------------ layout
TRACK_LEFT, TRACK_TOP = -6.5, 3.5
BOTTOM = -3.5                    # terminal bottom edge
# V5: x of every node, its row (0 = top), and three sets of row heights
XPOS = {"app": 1.3,
        "googletrans": -4.4, "httpx": -1.7, "art": 1.0,
        "anyio": -3.4, "httpcore": -0.3, "certifi": 2.2, "h2": 4.3,
        "typing-extensions": -4.7, "idna": -1.9, "h11": 0.1, "hpack": 3.2, "hyperframe": 5.4}
ROW = {"app": 0, "googletrans": 1, "httpx": 1, "art": 1, "anyio": 2, "httpcore": 2, "certifi": 2,
       "h2": 2, "typing-extensions": 3, "idna": 3, "h11": 3, "hpack": 3, "hyperframe": 3}
ROWS_BIG = [3.1, 1.75, 0.4, -0.95]          # above the 3-row strip (beat 2)
ROWS_TALL = [3.1, 1.6, 0.05, -1.5]          # room for a version tag under each chip (beat 3)
ROWS_COMPACT = [3.2, 2.22, 1.24, 0.28]      # above the uv.lock panel (beats 4-5)
TAG_ROOM = 0.47                             # a version tag's height + gap


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


def short_extra():
    return tag("extra", S.GREY)


def mchip(name: str, color: str, size: float = 22) -> VGroup:
    """chip(..., font=MONO) with its text on a common baseline: chip() centres the glyphs' bounding
    box, so 'idna' or 'h11' (no descender) sat lower than 'anyio'. Centre the full-height line
    instead (the same strut mono_line uses), so every chip in a row reads on one line."""
    c = chip(name, color, size=size, font=MONO)
    ref = mono_line(name, size)
    c.text.move_to(c.box).shift(UP * (ref.glyphs.get_center()[1] - ref.strut.get_center()[1]))
    return c


def vpkg(name: str) -> VGroup:
    """A package chip in the venv (GREEN), like common.pkg(name, 'venv', 22), baseline-levelled."""
    return mchip(name, VENV, 22)


def node_chip(name: str) -> VGroup:
    """A node of V5: the project itself GREY, a package GREEN (it lives in the venv)."""
    if name == "app":
        return mchip("app", S.GREY, 22)
    return vpkg(name)


def vtag(v: str) -> VGroup:
    """An exact-version tag that clicks in under a node."""
    t = mono(v, 20, VENV)
    h = mono("|", 20).height + 0.12
    b = RoundedRectangle(width=t.width + 0.26, height=h, corner_radius=0.1, stroke_color=VENV,
                         stroke_width=2).set_fill(S.BG, 0.95)
    t.move_to(b)
    return VGroup(b, t)


def node_pos(name: str, rows) -> np.ndarray:
    return np.array([XPOS[name], rows[ROW[name]], 0])


def edge(a: VGroup, b: VGroup, room: float = 0.0, color: str = S.GREY, bow: bool = True):
    """Dependency arrow from node a to node b (VGroups whose [0] is the chip). Same row: side to
    side at the chips' height; otherwise from below a (leaving `room` for its version tag) to the
    top of b. A long fan-out edge leaves from the side of a's bottom that faces b and bows upward a
    little, so it clears the tops of the nodes it passes over."""
    ca, cb = a[0], b[0]
    if abs(ca.get_center()[1] - cb.get_center()[1]) < 0.2:
        if cb.get_center()[0] > ca.get_center()[0]:
            s, e = ca.get_right(), cb.get_left()
        else:
            s, e = ca.get_left(), cb.get_right()
    else:
        dx = cb.get_center()[0] - ca.get_center()[0]
        if bow and abs(dx) > 3.0:
            sx = ca.get_center()[0] + np.sign(dx) * (ca.width / 2 - 0.22)
            s = np.array([sx, ca.get_bottom()[1] - room - 0.06, 0])
            e = cb.get_top() + UP * 0.06
            arc = ArcBetweenPoints(s, e, angle=-0.16 * np.sign(dx), color=color, stroke_width=2.5)
            arc.add_tip(tip_length=0.14, tip_width=0.14)
            return arc
        s, e = ca.get_bottom() + DOWN * room, cb.get_top()
    return Arrow(s, e, buff=0.06, color=color, stroke_width=2.5, tip_length=0.14,
                 max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=12)


def lock_scroll(w: float = 1.5, h: float = 1.8, name_size: float = 26, named: bool = True) -> VGroup:
    """The GREEN uv.lock scroll (V5's receipt). .paper .name"""
    paper = Rectangle(width=w, height=h, stroke_color=VENV, stroke_width=3).set_fill(VENV, 0.12)
    rh = max(0.07, h * 0.12)
    rods = VGroup(*[RoundedRectangle(width=w * 1.23, height=rh, corner_radius=rh / 2, stroke_color=VENV,
                                     stroke_width=3 if w > 0.6 else 2).set_fill(VENV, 0.55).move_to(p)
                    for p in (paper.get_top(), paper.get_bottom())])
    lines = VGroup(*[Line(LEFT * w * 0.32, RIGHT * w * (0.32 if k % 2 == 0 else 0.1), color=VENV,
                          stroke_width=3 if w > 0.6 else 1.5) for k in range(5)])
    lines.arrange(DOWN, buff=h * 0.11, aligned_edge=LEFT)
    lines.move_to(paper)
    name = mono("uv.lock", name_size, VENV).next_to(rods[1], DOWN, buff=0.15)
    g = VGroup(paper, lines, rods, name) if named else VGroup(paper, lines, rods)
    g.paper, g.name = paper, name
    return g


def hollow_node(name: str) -> VGroup:
    """A package that is in the lock but not installed here: hollow, dashed GREEN."""
    t = mono(name, 22, VENV)
    h = mono("|", 22).height + 0.24
    r = RoundedRectangle(width=t.width + 0.48, height=h, corner_radius=h / 2.6, stroke_color=VENV,
                         stroke_width=2.5).set_fill(S.BG, 0)
    d = DashedVMobject(r, num_dashes=34, dashed_ratio=0.55).set_stroke(VENV, 2.5)
    t.move_to(r)
    return VGroup(d, t)


def readme_card(line_no: int, body: VGroup, width: float | None = None) -> VGroup:
    head = VGroup(mono("README.md", CAPTION, S.GREY), label(f"· line {line_no}", CAPTION, S.GREY))
    head.arrange(RIGHT, buff=0.12)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    frame = box(width or inner.width + 0.5, inner.height + 0.4, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.25)
    g = VGroup(frame, inner)
    g.frame, g.body = frame, body
    return g


def panel(lines, header_parts, size: float = 20) -> VGroup:
    """A captured file shown like a code panel, its header naming the real file and lines. Built
    like devops.code_block but with a 0.22 padding instead of Code's 0.3, so the 77-character
    line 11 of uv.lock fits the safe width at 20 pt."""
    c = Code(code_string="\n".join(lines), language="text", formatter_style=HOUSE_CODE_STYLE,
             add_line_numbers=False, background="rectangle",
             background_config={"fill_color": PANEL, "stroke_color": S.GREY_DARK, "stroke_width": 2,
                                "corner_radius": 0.15, "buff": 0.22},
             paragraph_config={"font_size": size, "font": MONO})
    c.source = "\n".join(lines)
    hs = [mono(p, CAPTION, S.GREY) if p.endswith(".lock") else label(p, CAPTION, S.GREY) for p in header_parts]
    h = VGroup(*hs).arrange(RIGHT, buff=0.14)
    h.next_to(c, UP, buff=0.1).align_to(c, LEFT).shift(RIGHT * 0.12)
    g = VGroup(c, h)
    g.code, g.header = c, h
    return g


def under(m, color, buff=0.06, stroke=3):
    return Line(m.get_corner(DL) + DOWN * buff, m.get_corner(DR) + DOWN * buff, color=color, stroke_width=stroke)


def stop_sign(r: float = 0.34) -> VGroup:
    o = RegularPolygon(8, radius=r, stroke_color=ERR, stroke_width=3).set_fill(ERR, 0.25).rotate(PI / 8)
    t = label("stop", 20, ERR).move_to(o)
    return VGroup(o, t)


class ResolveLock(VoiceScene):
    # ------------------------------------------------------------- terminal helpers
    def prefill(self, t, cmd, lines):
        """Put a command and its output into a terminal without animating (it returns from S10)."""
        p = t.prompt + " "
        ln = mono_line(p + cmd, t.size, INK, t2c=t._prompt_colors(t.prompt))
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        for s in lines:
            o = mono_line(t._cut(s), t.size, OUTPUT)
            t._place(o, len(t.lines))
            t.lines.add(o)

    def fast_print(self, t, lines, run_time=0.3, scroll=0.2):
        t._make_room(self, len(lines), run_time=scroll)
        return t.print(self, lines, run_time=run_time)

    def pin(self, line, mob, run_time=0.4, anim=None, behind=False):
        """Show `mob` beside/behind a terminal line and make it part of that line (it scrolls with
        it). The line is re-added whole (an Indicate on some of its glyphs splits it)."""
        self.play(anim or FadeIn(mob, shift=LEFT * 0.1), run_time=run_time)
        self.remove(mob)
        if behind:
            line.submobjects.insert(0, mob)
        else:
            line.add(mob)
        self.add(line)
        return mob

    def resize(self, t, rows, run_time=0.8, extra=()):
        """Grow or shrink the terminal to `rows` (bottom edge fixed); it keeps its last lines."""
        ref = term(prompt=t.prompt, rows=rows)
        ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                            BOTTOM - ref.box.get_bottom()[1], 0]))
        n_keep = min(len(t.lines), rows)
        kept = t.lines.submobjects[len(t.lines) - n_keep:]
        gone = t.lines.submobjects[:len(t.lines) - n_keep]
        anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar),
                 t.dots.animate.move_to(ref.dots), t.title.animate.move_to(ref.title)]
        for i, ln in enumerate(kept):
            anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
        if gone:
            anims.append(FadeOut(VGroup(*gone)))
        self.play(*anims, *extra, run_time=run_time)
        for ln in gone:
            t.lines.remove(ln)
        t.rows = rows
        return t

    def hl(self, line, color, opacity=0.22, sub=None, extra=(), run_time=0.3):
        """A translucent bar behind a terminal line (or one part of it), pinned to the line.
        `extra` animations play together with it."""
        tgt = sub if sub is not None else line.glyphs
        bar = Rectangle(width=tgt.width + 0.2, height=line.strut.height * 1.08, stroke_width=0) \
            .set_fill(color, opacity).move_to([tgt.get_center()[0], line.strut.get_center()[1], 0])
        return self.pin(line, bar, behind=True, run_time=run_time, anim=AnimationGroup(FadeIn(bar), *extra))

    def ponder_over(self, question, seconds, center):
        """pause_and_ponder's card and draining timer, placed over the terminal (so the
        pyproject.toml panel and the part-1 chip above stay readable)."""
        card = ponder_card(question).move_to(center)
        card[0].set_fill(S.BG, 1)                     # fully opaque over the terminal text
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=seconds)
        return card

    def regroup(self, g):
        """Make `g` one top-level mobject again after its parts were animated separately."""
        self.remove(*g.submobjects)
        self.add(g)
        return g

    # ------------------------------------------------------------- the scene
    def construct(self):
        assert len(SAY) == 10, f"S11 has {len(SAY)} SAY lines; this scene times 10"

        tr = place_tracker(tracker_b(9))

        # ========================================================== 0 · how many? (ponder)
        t = term(prompt=P_REPO, rows=7)
        t.shift(np.array([0 - t.box.get_center()[0], BOTTOM - t.box.get_bottom()[1], 0]))
        self.prefill(t, "uv sync", SYNC_HEAD)
        c_top = t._slot(len(t.lines))[1] + 0.02
        c_bot = t.box.get_bottom()[1] + 0.14
        curtain = Rectangle(width=t.box.width - 0.4, height=c_top - c_bot, stroke_color=S.GREY,
                            stroke_width=2).set_fill(S.GREY_DARK, 1)
        curtain.move_to([t.box.get_center()[0], (c_top + c_bot) / 2, 0])
        folds = VGroup(*[Line(UP, DOWN, color=S.GREY, stroke_width=1.5, stroke_opacity=0.5)
                         .stretch_to_fit_height(curtain.height - 0.1).move_to(curtain).shift(RIGHT * x)
                         for x in np.linspace(-5.4, 5.4, 10)])
        qm = label("?", 34, S.GREY).move_to(curtain)
        qm_bg = Circle(radius=0.32, stroke_width=0).set_fill(S.GREY_DARK, 1).move_to(qm)
        cur = VGroup(curtain, folds, qm_bg, qm)

        toml = code_panel(TOML_DEPS, "pyproject.toml", 7, language="toml", font_size=24)
        toml.shift(np.array([-6.3 - toml.get_left()[0], 2.72 - toml.get_top()[1], 0]))
        code = toml.code
        L = lambda n: code.code_lines[n - 7]                           # file line n
        deps = VGroup(L(8), L(9))
        bx = code.background.get_right()[0]
        brace = Brace(Line([bx, deps.get_top()[1], 0], [bx, deps.get_bottom()[1], 0]), RIGHT,
                      color=VENV, buff=0.14)
        badge = VGroup(Circle(radius=0.3, stroke_color=VENV, stroke_width=3).set_fill(VENV, 0.18),
                       label("2", 30, VENV))
        badge[1].move_to(badge[0])
        badge.next_to(brace, RIGHT, buff=0.14)
        bars = VGroup(line_bar(code, 1, VENV, 0.14), line_bar(code, 2, VENV, 0.14))
        part1 = chip("part 1: pip installed 12", SYSTEM, size=24)
        part1.move_to([0, deps.get_center()[1], 0]).align_to([6.3, 0, 0], RIGHT)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(VGroup(t, cur), shift=UP * 0.2), run_time=0.9)
            vo.wait_until("pyproject.toml lists")
            self.play(FadeIn(toml, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("2 dependencies")
            self.play(FadeIn(bars), GrowFromCenter(brace), FadeIn(badge, scale=0.6), run_time=0.7)
            vo.wait_until("in part 1")
            self.play(FadeIn(part1, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("12 packages")
            self.play(Indicate(part1.text, color=SYSTEM, scale_factor=1.08), run_time=0.8)
            vo.wait_until("How many")
            self.play(Indicate(qm, color=TURN, scale_factor=1.5), run_time=0.9)

        card = self.ponder_over("pyproject.toml lists 2 dependencies.\nHow many packages will be installed?",
                                6, center=t.box.get_center() + DOWN * 0.1)

        # ========================================================== 1 · it's 11
        ROW_A, ROW_B = 2.3, 1.42
        counter = chip("11", VENV, size=30)
        counter.move_to([0, ROW_A, 0]).align_to([-6.3, 0, 0], LEFT)
        p1s = chip("part 1: 12", SYSTEM, size=24)
        p1s.move_to([0, ROW_B, 0]).align_to([-6.3, 0, 0], LEFT)
        G = {n: vpkg(n) for n in PKGS}
        rowa, rowb = VGroup(*[G[n] for n in PKGS[:6]]), VGroup(*[G[n] for n in PKGS[6:]])
        for r, y in ((rowa, ROW_A), (rowb, ROW_B)):
            r.arrange(RIGHT, buff=0.2).move_to([0, y, 0]).align_to([-3.75, 0, 0], LEFT)
        missing = VGroup(box(0.62, G["art"].height, S.GREY, dashed=True), label("?", 26, S.GREY))
        missing[1].move_to(missing[0])
        missing.next_to(rowb, RIGHT, buff=0.2)

        def to_chips(lines):
            anims = []
            for ln in lines:
                n = ln.text[3:].split("==")[0]
                anims.append(AnimationGroup(ReplacementTransform(substring(ln, n).copy(), G[n].text),
                                            FadeIn(G[n].box)))
            return anims

        with self.voiceover(SAY[1]) as vo:
            # "It's 11" is the first word: lift the curtain, print and lift the 11 without delay
            self.resize(t, 8, run_time=0.45, extra=[FadeOut(card), FadeOut(VGroup(toml, bars, brace, badge)),
                                                     cur.animate.stretch(0.02, 1, about_edge=UP).set_opacity(0)])
            self.remove(cur)
            res = self.fast_print(t, SYNC_RES, run_time=0.3)
            inst = res[2]
            self.hl(inst, TURN, run_time=0.6,
                    extra=[ReplacementTransform(substring(inst, "11").copy(), counter.text), FadeIn(counter.box)])
            self.regroup(counter)
            vo.wait_until("one fewer")
            self.play(ReplacementTransform(part1, p1s), run_time=0.6)
            self.play(Indicate(counter, color=VENV, scale_factor=1.15), Indicate(p1s, color=SYSTEM, scale_factor=1.08),
                      run_time=0.7)
            vo.wait_until("It resolved 13")
            self.play(Indicate(substring(res[0], "Resolved 13 packages"), color=S.WHITE, scale_factor=1.06),
                      run_time=0.7)
            self.add(res[0])
            vo.wait_until("installed 11,")
            self.play(Indicate(substring(inst, "Installed 11 packages"), color=TURN, scale_factor=1.06), run_time=0.6)
            self.add(inst)
            vo.wait_until("each with a plus")
            b1 = self.fast_print(t, SYNC_PLUS[:6], run_time=0.3)
            self.play(LaggedStart(*to_chips(b1), lag_ratio=0.12), run_time=1.0)
            b2 = self.fast_print(t, SYNC_PLUS[6:], run_time=0.3)
            self.play(LaggedStart(*to_chips(b2), lag_ratio=0.12), run_time=0.9)
            for n in PKGS:
                self.regroup(G[n])
            vo.wait_until("an exact version")
            vers = [substring(ln, ln.text.split("==")[1]) for ln in b2]
            self.play(*[Indicate(v, color=VENV, scale_factor=1.12) for v in vers], run_time=0.7)
            self.add(*b2)
            vo.wait_until("So where")
            rings = VGroup(*[SurroundingRectangle(G[n], buff=0.06, color=TURN, stroke_width=3, corner_radius=0.2)
                             for n in ("art", "googletrans")])
            self.play(Create(rings), run_time=0.5)
            others = [G[n] for n in PKGS if n not in ("art", "googletrans")]
            self.play(LaggedStart(*[Indicate(g, color=S.WHITE, scale_factor=1.12) for g in others], lag_ratio=0.12),
                      run_time=1.2)
            vo.wait_until("which one")
            self.play(FadeIn(missing, scale=0.6), run_time=0.5)
            self.play(Indicate(p1s, color=SYSTEM, scale_factor=1.1), run_time=0.7)

        # ========================================================== 2 · uv tree
        N = {}
        wish = {"art": mchip("art>=6.5", VENV), "googletrans": mchip("googletrans==4.0.2", VENV)}
        anims = []
        for n in PKGS:
            if n in wish:
                wish[n].move_to(node_pos(n, ROWS_BIG))
                anims.append(ReplacementTransform(G[n], wish[n]))
            else:
                anims.append(G[n].animate.move_to(node_pos(n, ROWS_BIG)).fade(0.72))
        counter2 = chip("11 packages", VENV, size=24).move_to([0, ROWS_BIG[0], 0]).align_to([6.4, 0, 0], RIGHT)
        nodes_lit = {n: node_chip(n).move_to(node_pos(n, ROWS_BIG)) for n in list(PKGS) + ["app"]}
        E = {}

        def grow(i0, i1, firsts):
            """Print rows i0..i1-1 of the uv tree output in the strip; each name flies to its node,
            which lights up, and its edge grows from the parent (a repeated row: only the edge)."""
            new = self.fast_print(t, TREE_OUT[i0:i1], run_time=0.2, scroll=0.12)
            anims, flies = [], []
            for k, ln in zip(range(i0, i1), new):
                if k == 0:                                     # "Resolved 13 packages in 1ms"
                    continue
                name, parent, _ = TREE[k - 1]
                fly = substring(ln, name).copy()
                flies.append(fly)
                anims.append(fly.animate.move_to(nodes_lit[name]).set_opacity(0))
                if name in firsts:
                    if name == "app":
                        N[name] = nodes_lit[name]
                        anims.append(FadeIn(N[name], scale=0.7))
                    elif name in wish:
                        N[name] = nodes_lit[name]
                        anims.append(ReplacementTransform(wish[name], N[name]))
                    else:
                        N[name] = G[name]
                        anims.append(Transform(G[name], nodes_lit[name]))
                if parent is not None:
                    E[(parent, name)] = edge(VGroup(nodes_lit[parent]), VGroup(nodes_lit[name]), bow=parent != "app")
                    e_ = E[(parent, name)]
                    anims.append(GrowArrow(e_) if isinstance(e_, Arrow) else Create(e_))
            self.play(*anims, run_time=0.45)        # quick: the names come about 0.8 s apart
            self.remove(*flies)
            return new

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(rings, missing, p1s)), run_time=0.3)
            self.resize(t, 3, run_time=0.8, extra=[*anims, Transform(counter, counter2)])
            vo.wait_until("this extra command")
            self.play(caption_extra(tr), run_time=0.4)
            cmd = t.type(self, "uv tree", type_time=0.5)
            self.pin(cmd, short_extra().next_to(cmd.strut, RIGHT, buff=0.35), run_time=0.3)
            vo.wait_until("draws them")
            grow(0, 2, {"app"})
            grow(2, 4, {"art", "googletrans"})
            vo.wait_until("Our googletrans")
            self.play(Indicate(N["googletrans"], color=S.WHITE, scale_factor=1.1), run_time=0.6)
            grow(4, 5, {"httpx"})
            vo.wait_until("an HTTP library")
            self.play(Indicate(N["httpx"], color=VENV, scale_factor=1.15), run_time=0.7)
            vo.wait_until("anyio")
            grow(5, 7, {"anyio", "idna"})
            vo.wait_until("certifi")
            grow(7, 8, {"certifi"})
            vo.wait_until("httpcore")
            grow(8, 11, {"httpcore", "h11"})
            vo.wait_until("h2")
            grow(11, 13, {"h2"})
            vo.wait_until("and more")
            grow(13, 15, {"hpack", "hyperframe"})
            vo.wait_until("Two wishes")
            self.play(Indicate(N["art"], color=TURN, scale_factor=1.2),
                      Indicate(N["googletrans"], color=TURN, scale_factor=1.12), run_time=0.8)
            self.play(Indicate(counter, color=VENV, scale_factor=1.1), run_time=0.7)

        # ========================================================== 3 · versions, then the receipt
        names = list(N)                                        # app first, then tree order
        tall = {n: N[n].copy().move_to(node_pos(n, ROWS_TALL)) for n in names}
        # edges first leave from the chips themselves, and stretch below each version tag only as
        # that tag clicks in (an edge never starts in mid-air)
        tall_E0 = {k: edge(VGroup(tall[k[0]]), VGroup(tall[k[1]]), bow=k[0] != "app") for k in E}
        tall_E = {k: edge(VGroup(tall[k[0]]), VGroup(tall[k[1]]), room=0 if k[0] == "app" else TAG_ROOM,
                          bow=k[0] != "app") for k in E}
        tags = {n: vtag(VERS[n]).next_to(tall[n], DOWN, buff=0.05) for n in names if n != "app"}
        counter3 = counter.copy().move_to([0, -2.95, 0])
        frame = VGroup(t.box, t.bar, t.dots, t.title)
        scroll = lock_scroll().move_to([0, 0.75, 0])
        url = mono(URL_SNIP, 20, S.GREY)
        hsh = mono(HASH_SNIP, 20, S.GREY)
        snips = VGroup(url, hsh).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(scroll, DOWN, buff=0.4)
        wl = code_panel(TOML_DEPS, "pyproject.toml", 7, language="toml", font_size=24)
        wl.move_to([-3.3, 0.6, 0])
        wl_cap = label("wish list", 34, INK).next_to(wl, DOWN, buff=0.35)
        rc_spot = np.array([3.3, 0.8, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(frame, t.lines), shift=DOWN * 0.4), caption_extra(tr, False),
                      *[Transform(N[n], tall[n]) for n in names], *[Transform(E[k], tall_E0[k]) for k in E],
                      counter.animate.move_to(counter3), run_time=0.9)
            vo.wait_until("one exact version")
            order = [n for n, _, _ in TREE if n != "app"]
            seen = []
            for n in order:
                if n not in seen:
                    seen.append(n)
            def click(n):
                return AnimationGroup(FadeIn(tags[n], shift=UP * 0.25, scale=1.25),
                                      *[Transform(E[k], tall_E[k]) for k in E if k[0] == n])
            self.play(LaggedStart(*[click(n) for n in seen], lag_ratio=0.25), run_time=2.6)
            for n in seen:
                N[n].add(tags[n])
            vo.wait_until("versions that all")
            flashes = [ShowPassingFlash(e.copy().set_color(VENV).set_stroke(width=6), time_width=0.6)
                       for e in E.values()]
            self.play(LaggedStart(*flashes, lag_ratio=0.06), run_time=1.4)
            vo.wait_until("Then uv writes")
            tree_all = VGroup(*N.values(), *E.values(), counter)
            self.play(FadeOut(tree_all, target_position=scroll.paper.get_center(), scale=0.1),
                      FadeIn(VGroup(scroll[0], scroll[1], scroll[2]), scale=0.4), run_time=1.3)
            vo.wait_until("uv.lock,")
            self.play(Write(scroll.name), run_time=0.6)
            vo.wait_until("with download")
            self.play(FadeIn(url, shift=UP * 0.1), run_time=0.5)
            self.wait(0.4)
            self.play(FadeIn(hsh, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("checksums")
            self.play(Indicate(hsh, color=S.WHITE, scale_factor=1.05), run_time=0.7)
            vo.wait_until("The pyproject.toml file")
            self.play(FadeOut(snips), scroll.animate.move_to(rc_spot), run_time=0.7)
            self.play(FadeIn(wl, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("wish list")
            self.play(Write(wl_cap), run_time=0.7)
            vo.wait_until("The uv.lock file")
            rc_cap = label("receipt", 34, VENV).move_to([rc_spot[0], wl_cap.get_center()[1], 0])
            self.play(Indicate(scroll.name, color=VENV, scale_factor=1.15), run_time=0.6)
            self.play(Write(rc_cap), run_time=0.7)

        # ========================================================== 4 · why 13?
        C = {n: node_chip(n).move_to(node_pos(n, ROWS_COMPACT)) for n in names}
        CE = {k: edge(VGroup(C[k[0]]), VGroup(C[k[1]]), bow=k[0] != "app") for k in E}
        ctree = VGroup(*CE.values(), *C.values())
        app_tag = tag("the project itself · not downloaded", S.GREY, size=20).next_to(C["app"], RIGHT, buff=0.2)
        lock_p = panel(LOCK, ["uv.lock", "· lines 5–12 (generated on your VM)"], size=20)
        lock_p.shift(np.array([0 - lock_p.code.get_center()[0], -3.58 - lock_p.code.get_bottom()[1], 0]))
        lc = lock_p.code
        bar11 = line_bar(lc, 6, TURN, 0.22)
        TX = 1.75                                              # tally block (top right)
        t_11 = label("11", 24, VENV)
        t_app = VGroup(label("+", 24, INK), mono("app", 20, INK)).arrange(RIGHT, buff=0.1)
        t_te = VGroup(label("+", 24, INK), mono("typing-extensions", 20, VENV)).arrange(RIGHT, buff=0.1)
        line_a = VGroup(t_11, t_app, t_te).arrange(RIGHT, buff=0.13)
        line_a.move_to([0, 2.66, 0]).align_to([TX, 0, 0], LEFT)
        t_eq = label("= 12", 24, INK)
        t_eq13 = label("= 13 resolved", 24, VENV)
        t_q = label("13 resolved?", 24, TURN)
        for m in (t_eq, t_eq13, t_q):
            m.move_to([0, 2.16, 0]).align_to([TX, 0, 0], LEFT)
        rp_line = VGroup(mono(LOCK_RP, 20, INK), label("· line 3", 20, S.GREY)).arrange(RIGHT, buff=0.18)
        rp = VGroup(rp_line, label("one lock for every allowed Python", 22, S.GREY))
        rp.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rp_in = rp
        rp_box = box(rp_in.width + 0.4, rp_in.height + 0.3, S.GREY, fill=S.GREY_DARKER, fill_opacity=1).move_to(rp_in)
        rpc = VGroup(rp_box, rp_in).move_to([0, -1.08, 0]).align_to([6.35, 0, 0], RIGHT)
        te = hollow_node("typing-extensions").move_to(node_pos("typing-extensions", ROWS_COMPACT))
        te_edge = DashedLine(C["anyio"].get_bottom() + DOWN * 0.04 + LEFT * 0.2, te.get_top() + UP * 0.04,
                             color=VENV, stroke_width=2.5, dash_length=0.08)
        te_lab = mono("python < 3.15", 20, VENV)
        te_lab.move_to([0, ROWS_COMPACT[2], 0]).align_to([C["anyio"].get_left()[0] - 0.22, 0, 0], RIGHT)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(wl, wl_cap, rc_cap)),
                      FadeIn(ctree, target_position=scroll.paper.get_center(), scale=0.12),
                      FadeOut(scroll, scale=0.3), run_time=1.0)
            self.play(FadeIn(t_q, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("It's 11 packages")
            pk = [C[n] for n in names if n != "app"]
            self.play(FadeIn(t_11, shift=DOWN * 0.1),
                      LaggedStart(*[Indicate(c, color=VENV, scale_factor=1.12) for c in pk], lag_ratio=0.08),
                      run_time=1.2)
            vo.wait_until("plus the app")
            self.play(FadeIn(t_app, shift=DOWN * 0.1), Indicate(C["app"], color=S.WHITE, scale_factor=1.2),
                      run_time=0.7)
            vo.wait_until("which uv doesn't")
            self.play(FadeIn(app_tag, shift=LEFT * 0.15), FadeOut(t_q), FadeIn(t_eq), run_time=0.6)
            vo.wait_until("The 13th")
            self.play(FadeOut(app_tag), t_eq.animate.set_color(S.GREY),
                      FadeIn(lock_p, shift=UP * 0.3), run_time=0.8)
            vo.wait_until("which covers")
            self.play(FadeIn(rpc, scale=0.9), run_time=0.5)
            vo.wait_until("not just ours")
            self.play(Indicate(rp_line[0], color=S.WHITE, scale_factor=1.08), run_time=0.8)
            vo.wait_until("In it, anyio")
            self.play(FadeOut(rpc), run_time=0.3)
            self.play(FadeIn(bar11), Indicate(C["anyio"], color=VENV, scale_factor=1.2), run_time=0.7)
            vo.wait_until("needs typing")
            self.play(Create(te_edge), FadeIn(te, shift=DOWN * 0.15), run_time=0.8)
            self.play(FadeIn(t_te, shift=DOWN * 0.1), FadeOut(t_eq), FadeIn(t_eq13), run_time=0.6)
            vo.wait_until("but only")
            mk = code_span(lc, 6, "python_full_version < '3.15'")
            self.play(Indicate(mk, color=TURN, scale_factor=1.06), FadeIn(te_lab, shift=RIGHT * 0.15),
                      run_time=0.8)
            vo.wait_until("older than")
            self.play(Indicate(te_lab, color=VENV, scale_factor=1.15), run_time=0.7)
            self.play(Indicate(t_eq13, color=VENV, scale_factor=1.12), run_time=0.7)

        # ========================================================== 5 · 11 here, 12 elsewhere
        cap15 = VGroup(label("11", 26, VENV), label("on 3.15", 24, INK)).arrange(RIGHT, buff=0.12)
        cap15.next_to(te, DOWN, buff=0.22)
        # left card: the part-1 shelf
        lcard = box(6.2, 2.7, SYSTEM, fill_opacity=0.05).move_to([-3.3, -2.16, 0])
        lhead = label("part 1 · Python 3.11 · pip", 22, S.GREY)
        lhead.move_to(lcard.get_corner(UL) + np.array([0.25, -0.3, 0]), aligned_edge=UL)
        board_y = lcard.get_bottom()[1] + 1.05
        board = Line([lcard.get_left()[0] + 0.3, board_y, 0], [lcard.get_right()[0] - 0.3, board_y, 0],
                     color=SYSTEM, stroke_width=5)
        shelf_jars = VGroup(*[jar(SYSTEM, 0.36) for _ in range(12)]).arrange(RIGHT, buff=0.08)
        shelf_jars.next_to(board, UP, buff=0.03).align_to(board, RIGHT)
        path_t = mono("/usr/local/… (pip's)", 20, SYSTEM).next_to(board, DOWN, buff=0.12).align_to(board, LEFT)
        te_name = mono(TE_PIP, 20, INK).next_to(shelf_jars[-1], UP, buff=0.14).align_to(board, RIGHT)
        cap11 = VGroup(label("12", 26, SYSTEM), label("on 3.11", 24, INK)).arrange(RIGHT, buff=0.12)
        cap11.move_to([0, -3.18, 0]).align_to(board, RIGHT)
        left_card = VGroup(lcard, lhead, board, VGroup(*shelf_jars[:-1]), path_t)
        # right card: Debian 13
        rcard = box(6.2, 2.7, S.GREY, fill_opacity=0.05).move_to([3.3, -2.16, 0])
        rhead = VGroup(tag("Debian 13", S.GREY), label("Python 3.13 · uv", 22, S.GREY)).arrange(RIGHT, buff=0.25)
        rhead.move_to(rcard.get_corner(UL) + np.array([0.25, -0.22, 0]), aligned_edge=UL)
        d13 = VGroup(*[mono_line(s, 22, OUTPUT) for s in D13]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        d13.next_to(rhead, DOWN, buff=0.22).align_to(rhead, LEFT)
        cap13 = VGroup(label("12", 26, VENV), label("on 3.13", 24, INK)).arrange(RIGHT, buff=0.12)
        cap13.move_to([0, -3.18, 0]).align_to([rcard.get_right()[0] - 0.3, 0, 0], RIGHT)
        right_card = VGroup(rcard, rhead, d13[0], d13[1])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(lock_p, bar11)), run_time=0.5)
            vo.wait_until("it's skipped")
            self.play(Wiggle(te, scale_value=1.08, rotation_angle=0.02 * TAU), run_time=0.8)
            vo.wait_until("so 11")
            self.play(FadeIn(cap15, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Part 1 ran")
            self.play(FadeOut(VGroup(line_a, t_eq13)), FadeIn(left_card, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("so pip installed it")
            self.play(FadeTransform(te.copy(), shelf_jars[-1]), run_time=0.8)
            self.play(FadeIn(te_name, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until(": 12")
            self.play(FadeIn(cap11, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("And on Debian 13")
            self.play(FadeIn(right_card, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("uv installs")
            self.play(FadeTransform(te.copy(), d13[2]), run_time=0.8)
            self.play(d13[2].animate.set_color(VENV), run_time=0.4)
            vo.wait_until("12 too")
            self.play(FadeIn(cap13, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 6 · why the receipt matters
        def mini_tree():
            """A schematic copy of the tree: GREEN nodes, GREEN version tags on the four leaves."""
            pts = {"r": [0, 0.9], "a": [-0.95, 0.0], "b": [0.95, 0.0],
                   "l0": [-1.65, -1.0], "l1": [-0.45, -1.0], "l2": [0.6, -1.0], "l3": [1.75, -1.0]}
            dots = {k: RoundedRectangle(width=0.42, height=0.3, corner_radius=0.08, stroke_color=VENV,
                                        stroke_width=2.5).set_fill(VENV, 0.25).move_to([x, y, 0])
                    for k, (x, y) in pts.items()}
            es = VGroup(*[Line(dots[a].get_bottom(), dots[b].get_top(), color=S.GREY, stroke_width=2.5, buff=0.04)
                          for a, b in [("r", "a"), ("r", "b"), ("a", "l0"), ("a", "l1"), ("b", "l2"), ("b", "l3")]])
            pills = VGroup(*[RoundedRectangle(width=0.62, height=0.22, corner_radius=0.11, stroke_width=0)
                             .set_fill(VENV, 0.85).next_to(dots[f"l{i}"], DOWN, buff=0.12) for i in range(4)])
            g = VGroup(es, VGroup(*dots.values()), pills)
            g.pills = pills
            return g

        def student(day, x):
            p = person_icon(S.GREY, 0.95)
            d = label(day, 26, INK).next_to(p, DOWN, buff=0.15)
            run = mchip("uv sync", UV)
            g = VGroup(p, d)
            g.move_to([x, 1.75, 0])
            run.next_to(p, RIGHT, buff=0.35)
            return g, run

        sA, runA = student("Monday", -5.2)
        sB, runB = student("next Monday", 1.6)
        tA = mini_tree().move_to([-3.1, -1.05, 0])
        tB = mini_tree().move_to([3.6, -1.05, 0])
        ill = illustration_tag().move_to([0, 3.2, 0]).align_to([6.4, 0, 0], RIGHT)
        divider = DashedLine([0.25, 2.6, 0], [0.25, -2.75, 0], color=S.GREY_DARK, stroke_width=2)
        newer = {}
        for i in (1, 3):
            nb = VGroup(box(1.2, 0.46, S.GREY, dashed=True), label("newer?", 22, INK))
            nb[1].move_to(nb[0])
            nb.move_to(tB.pills[i])
            newer[i] = nb
        no_lock = label("no shared lock: each run resolves fresh", 24, S.GREY).move_to([0, -3.25, 0])
        handoff = lock_scroll(w=0.5, h=0.6, name_size=20)
        handoff.next_to(runA, RIGHT, buff=0.3)
        ok = check_mark(0.45, VENV, stroke=7).next_to(tB, RIGHT, buff=0.25)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(*C.values(), *CE.values(), te, te_edge, te_lab, cap15, left_card, shelf_jars[-1],
                                     te_name, cap11, right_card, d13[2], cap13)), run_time=0.7)
            self.play(FadeIn(ill), run_time=0.4)
            vo.wait_until("Two students")
            self.play(FadeIn(sA, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Create(divider), FadeIn(sB, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("run uv sync")
            self.play(FadeIn(runA, scale=0.8), FadeIn(runB, scale=0.8), run_time=0.5)
            vo.wait_until("Without a shared")
            self.play(FadeIn(no_lock, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("each resolves")
            self.play(LaggedStart(Create(tA[0]), FadeIn(tA[1]), FadeIn(tA[2]), lag_ratio=0.3),
                      LaggedStart(Create(tB[0]), FadeIn(tB[1]), FadeIn(tB[2]), lag_ratio=0.3), run_time=1.2)
            vo.wait_until("different versions")
            self.play(*[FadeOut(tB.pills[i], scale=0.5) for i in newer],
                      *[FadeIn(newer[i], scale=1.3) for i in newer], run_time=0.6)
            vo.wait_until("deep in the tree")
            self.play(*[Indicate(newer[i], color=S.WHITE, scale_factor=1.15) for i in newer], run_time=0.8)
            vo.wait_until("With the same")
            self.play(FadeOut(no_lock), FadeIn(handoff, scale=0.5), run_time=0.5)
            # an arc over the second student (a straight move would slide across the icon and its chip)
            self.play(handoff.animate(path_arc=-PI / 3).next_to(runB, RIGHT, buff=0.3), run_time=1.0)
            vo.wait_until("they get exactly")
            self.play(*[FadeOut(newer[i], scale=0.6) for i in newer],
                      *[FadeIn(tB.pills[i], scale=1.4) for i in newer], run_time=0.6)
            self.play(Create(ok), Indicate(tB[2], color=VENV, scale_factor=1.15), run_time=0.7)

        # ========================================================== 7 · ls -a, git status
        t7 = term(prompt=P_REPO, rows=13)
        t7.shift(np.array([0 - t7.box.get_center()[0], -3.55 - t7.box.get_bottom()[1], 0]))

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(ill, sA, sB, runA, runB, tA, tB, divider, handoff, ok)), run_time=0.5)
            self.play(FadeIn(t7, shift=UP * 0.3), caption_extra(tr), run_time=0.6)
            vo.wait_until("First, ls")
            c1 = t7.type(self, "ls -a", type_time=0.4)
            self.pin(c1, short_extra().next_to(c1.strut, RIGHT, buff=0.35), run_time=0.3)
            vo.wait_until("shows two")              # the command row scrolls off when 13 lines print
            self.fast_print(t7, LS_OUT, run_time=0.6)
            vo.wait_until("the dot venv")
            venv_ln, lock_ln = t7.find(".venv"), t7.find("uv.lock")
            self.play(venv_ln.glyphs.animate.set_color(VENV), run_time=0.4)
            self.pin(venv_ln, tag("new", VENV).next_to(venv_ln.strut, RIGHT, buff=0.4), run_time=0.4)
            vo.wait_until("and uv.lock")
            self.play(lock_ln.glyphs.animate.set_color(VENV), run_time=0.4)
            self.pin(lock_ln, tag("new", VENV).next_to(lock_ln.strut, RIGHT, buff=0.4), run_time=0.4)
            vo.wait_until("And git status")
            c2 = t7.type(self, "git status", type_time=0.5)
            self.pin(c2, short_extra().next_to(c2.strut, RIGHT, buff=0.35), run_time=0.3)
            self.fast_print(t7, GS_OUT, run_time=0.5)
            vo.wait_until("is untracked")
            ut = t7.find("Untracked files")
            self.play(Indicate(ut.glyphs, color=TURN, scale_factor=1.05), run_time=0.6)
            self.add(ut)
            gl = t7.find("uv.lock")
            assert gl.text.strip() == "uv.lock" and gl is not lock_ln
            self.hl(gl, TURN, sub=gl.glyphs)
            vo.wait_until("It was made here")
            self.play(Indicate(gl.glyphs, color=TURN, scale_factor=1.2), run_time=0.8)
            self.add(gl)
            vo.wait_until("didn't come")
            self.play(Indicate(lock_ln.glyphs, color=VENV, scale_factor=1.15), run_time=0.8)
            self.add(lock_ln)

        # ========================================================== 8 · erratum and the fix
        body = VGroup(label("…and", 24, INK), mono("uv.lock", 22, VENV),
                      label("pins exact versions so the next person gets the same setup.", 24, INK))
        body.arrange(RIGHT, buff=0.12)
        body[1].align_to(body[0], DOWN)
        card8 = readme_card(70, body)
        CARD_Y0, CARD_Y1 = 0.9, 2.15                       # centre while it is read, then top
        card8.move_to([0, CARD_Y0, 0])
        err = tag("erratum", S.GREY).next_to(card8[1][0], RIGHT, buff=0.35)
        note = VGroup(label("the repo has no", 24, TURN), mono("uv.lock", 22, TURN), label("yet", 24, TURN))
        note.arrange(RIGHT, buff=0.12)
        note.next_to(card8, DOWN, buff=0.25).align_to(card8, LEFT).shift(RIGHT * 0.25)
        def fix_chip(*parts):
            row = VGroup(*parts).arrange(RIGHT, buff=0.14)
            h = mono("|", 24).height + 0.26
            return VGroup(box(row.width + 0.5, h, VENV, fill_opacity=0.16, radius=h / 2.6).move_to(row), row)

        fix1 = fix_chip(label("commit", 24, INK), mono("uv.lock", 22, INK))
        fix2 = fix_chip(label("in CI:", 24, INK), mono("uv sync --locked", 22, INK))
        fix1.move_to([-3.3, 0.2, 0])
        fix2.move_to([3.3, 0.2, 0])
        # left: the repo folder
        folder = folder_glyph(1.1, S.GREY).move_to([-4.6, -1.95, 0])
        fname = mono("simple-translate/", 22, INK).next_to(folder, DOWN, buff=0.15)
        gadd = mono("git add uv.lock", 22, INK).next_to(folder, RIGHT, buff=0.5)
        flying = lock_scroll(w=0.5, h=0.6, name_size=20).move_to([-3.3, -0.8, 0])
        # right: CI
        ci_box = box(5.6, 2.35, S.GREY, fill_opacity=0.05).move_to([3.3, -2.0, 0])
        ci_head = VGroup(label("CI", 26, S.GREY), mono("$ uv sync --locked", 22, INK)).arrange(RIGHT, buff=0.35)
        ci_head.move_to(ci_box.get_top() + DOWN * 0.38).align_to(ci_box, LEFT).shift(RIGHT * 0.3)
        good = lock_scroll(w=0.36, h=0.42, name_size=20).move_to([2.0, -2.4, 0])
        bad = VGroup(box(0.62, 0.62, S.GREY, dashed=True), label("?", 24, S.GREY)).move_to([4.6, -2.3, 0])
        bad[1].move_to(bad[0])
        bad_l = label("no lock", 20, S.GREY).next_to(bad, DOWN, buff=0.12)
        g_ok = check_mark(0.4, VENV, stroke=7).next_to(good, RIGHT, buff=0.3).shift(UP * 0.15)
        b_stop = stop_sign(0.34).next_to(bad, RIGHT, buff=0.3)

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(t7.box, t7.bar, t7.dots, t7.title, t7.lines)), caption_extra(tr, False),
                      run_time=0.5)
            self.play(FadeIn(card8, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("a small mistake")
            self.play(FadeIn(err, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("It says")
            ul = under(VGroup(body[1], body[2]), S.GREY)
            self.play(Create(ul), run_time=0.6)
            vo.wait_until("the same versions")
            self.play(Indicate(body[2], color=S.WHITE, scale_factor=1.03), run_time=0.8)
            vo.wait_until("But the repo")
            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("resolves fresh")
            self.play(Indicate(note, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("In your own")
            top = VGroup(card8, err, ul, note)
            self.play(top.animate.shift(np.array([-6.3 - card8.get_left()[0], CARD_Y1 - CARD_Y0, 0])), run_time=0.7)
            self.play(FadeIn(fix1, shift=UP * 0.15), FadeIn(VGroup(folder, fname), shift=UP * 0.15), run_time=0.6)
            vo.wait_until("commit uv.lock")
            self.play(FadeIn(flying, scale=0.6), run_time=0.3)
            inside = lock_scroll(w=0.3, h=0.36, named=False).move_to(folder[1].get_center() + DOWN * 0.02)
            self.play(ReplacementTransform(flying[:3], inside), FadeOut(flying[3], scale=0.5), run_time=0.8)
            self.play(Write(gadd), Indicate(folder, color=VENV, scale_factor=1.1), run_time=0.7)
            vo.wait_until("In automated")
            self.play(FadeIn(fix2, shift=UP * 0.15), FadeIn(VGroup(ci_box, ci_head), shift=UP * 0.15), run_time=0.7)
            vo.wait_until("locked flag")
            self.play(Indicate(ci_head[1], color=S.WHITE, scale_factor=1.06), run_time=0.7)
            self.play(FadeIn(good, shift=RIGHT * 0.2), run_time=0.4)
            self.play(Create(g_ok), run_time=0.4)
            vo.wait_until("which refuses")
            self.play(FadeIn(VGroup(bad, bad_l), shift=RIGHT * 0.2), run_time=0.4)
            self.play(FadeIn(b_stop, scale=0.5), run_time=0.4)
            vo.wait_until("or stale")
            self.play(Indicate(b_stop, color=ERR, scale_factor=1.2), run_time=0.8)

        # ========================================================== 9 · re-run, nothing changes
        t9 = term(prompt=P_REPO, rows=3)
        t9.move_to([0, 0.35, 0])
        safe = VGroup(check_mark(0.4, VENV, stroke=7), label("changes nothing · safe to re-run", 28, VENV))
        safe.arrange(RIGHT, buff=0.25).next_to(t9, DOWN, buff=0.45)

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(card8, err, ul, note, fix1, fix2, folder, fname, inside, gadd, ci_box, ci_head,
                                     good, g_ok, bad, bad_l, b_stop)), run_time=0.6)
            self.play(FadeIn(t9, shift=UP * 0.2), caption_extra(tr), run_time=0.5)
            c9 = t9.type(self, "uv sync", type_time=0.4)
            self.pin(c9, short_extra().next_to(c9.strut, RIGHT, buff=0.35), run_time=0.3)
            out9 = t9.print(self, RE_OUT, run_time=0.4)
            vo.wait_until("It checks")
            self.hl(out9[1], VENV)
            vo.wait_until("11 here")
            self.play(Indicate(substring(out9[1], "11"), color=VENV, scale_factor=1.4), run_time=0.7)
            self.add(out9[1])
            vo.wait_until("a fraction")
            ms = substring(out9[1], "0.14ms")
            ulm = under(ms, VENV)
            self.play(Create(ulm), Indicate(ms, color=VENV, scale_factor=1.2), run_time=0.8)
            self.add(out9[1])
            vo.wait_until("and changes nothing")
            self.play(FadeIn(safe, shift=UP * 0.15), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
