"""S14 · The older way: pipenv (concept scene: no tracker, no terminal).

Beats (script.md "## S14", one voiceover block each):
 0  "pipenv" (GREY) at the top, "an older way to do the same job". At left the repo card
    dlops-io/simple-translate with its two branches drawn as two separate lanes (the pipenv branch
    is its own root commit, digest.md §0): `main` (GREEN) and `pipenv` (GREY), a small `Pipfile`
    chip on the pipenv lane and the note "older version of this tutorial". At right, "also using
    pipenv": GREY repo chips `simple-translate-aws` ("AWS track") and `cheese-app-v0 · api-service`
    ("later in the course").
 1  Two columns, uv (PURPLE header; GREEN/PURPLE items) and pipenv (GREY): the title becomes the
    pipenv header; GREY tag "just read: no pipenv on this VM". Five rows, each built as it is said:
    the uv item appears, a copy morphs across into the pipenv name; earlier rows dim.
    pyproject.toml ↔ Pipfile · uv.lock ↔ Pipfile.lock · .venv/ "in the project" ↔
    ~/.local/share/virtualenvs/<name>-<hash> "in your home" · uv sync ↔ pipenv install / pipenv sync
    · source .venv/bin/activate ↔ pipenv shell, tag "a subshell" -> "a subshell · type exit to leave".
 2  S05's puzzle chips "httpx 0.13" / "httpx 0.28" return, then become real: left the pipenv
    branch's Pipfile.lock (lines 88 and 94, `"version": "==0.13.3"`) -> httpx 0.13.3; right our uv
    sync (debian12-part-b/08-uv-sync.txt lines 16-18, line 17 ` + httpx==0.28.1`) -> httpx 0.28.1,
    tag "at the time of recording". "≠" between. Then S05's picture (tag illustration): one ORANGE
    `/usr/local/… (pip's)` shelf, both versions fly to its one httpx slot as ORANGE jars, 0.13.3
    knocks 0.28.1 off, RED cross; the shelf splits into two GREEN toolboxes (pipenv's venv, uv's
    .venv/), one jar each, GREEN check. Fade out to an empty frame.
"""

import textwrap

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (MONO, OUTPUT, PANEL, TERM_BG, box, check_mark, chip, cross_mark,
                              folder_glyph, label, line_pitch, mono, mono_line, substring, tag)
from explainer.scene import VoiceScene

from common import (ERR, INK, NARRATION, SYSTEM, TURN, UV, VENV, capture, excerpt, illustration_tag,
                    jar, recorded_tag)

SAY = NARRATION["S14"]
PIPENV = S.GREY                      # the pipenv column / branch (script.md: GREY)

# ------------------------------------------------------------------ real lines
LOCK = "pipenv-branch/Pipfile.lock"
_key_raw, _ver_raw = excerpt(LOCK, 88, 88), excerpt(LOCK, 94, 94)
assert _key_raw.strip() == '"httpx": {', _key_raw
assert _ver_raw.strip() == '"version": "==0.13.3"', _ver_raw
LOCK_KEY, _, LOCK_VER = textwrap.dedent(_key_raw + "\n\n" + _ver_raw).split("\n")
OLD = LOCK_VER.split("==")[1].rstrip('"')                                    # 0.13.3

_sync = capture("08-uv-sync", "debian12-part-b")
assert _sync.cmd == "uv sync", _sync.cmd
SYNC_ROWS = _sync.pick((15, 17))                                             # file lines 16-18
assert SYNC_ROWS[1] == " + httpx==0.28.1", SYNC_ROWS
NEW = SYNC_ROWS[1].split("==")[1]                                            # 0.28.1

# ------------------------------------------------------------------ layout
# beat 1: the table hugs the centre like a dictionary: uv items end at XL, pipenv items start at XR
XL, XR = -1.75, -0.85
HEAD_Y = 2.75
ROW_Y = [1.6, 0.65, -0.3, -1.5, -2.45]
ITEM = 24
# beat 2
CARD_X = 3.3
CHIP_Y = 0.3
SHELF_Y, SHELF_HALF = -2.25, 3.0
SLOT_X, CROSS_X = 2.3, 1.3
BOX_X, BOX_Y = 2.05, -2.5


# ------------------------------------------------------------------ helpers
def item(s: str, color: str, size: float = ITEM) -> VGroup:
    return mono_line(s, size, color)


def at_left(m: VGroup, y: float) -> VGroup:
    """uv item: right edge at XL, centred on row y."""
    return m.shift([XL - m.glyphs.get_right()[0], y - m.strut.get_center()[1], 0])


def at_right(m: VGroup, y: float) -> VGroup:
    """pipenv item: left edge at XR, centred on row y."""
    return m.shift([XR - m.glyphs.get_left()[0], y - m.strut.get_center()[1], 0])


def row_arrow(y: float) -> Arrow:
    return Arrow([XL + 0.14, y, 0], [XR - 0.14, y, 0], buff=0, color=S.GREY, stroke_width=3,
                 tip_length=0.15, max_tip_length_to_length_ratio=0.4)


def lane(y: float, x0: float, x1: float, n: int, color: str, name: str, size: float = 26) -> VGroup:
    """A branch drawn git-graph style: a line of commits ending in its name chip."""
    ln = Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4)
    dots = VGroup(*[Dot([x, y, 0], radius=0.09, color=color) for x in np.linspace(x0 + 0.3, x1 - 0.25, n)])
    c = chip(name, color, size, font=MONO).next_to(ln, RIGHT, buff=0.15)
    g = VGroup(ln, dots, c)
    g.line, g.dots, g.chip = ln, dots, c
    return g


def mini_panel(rows, bg_color: str, width: float | None = None, size: float = 22, pad: float = 0.22) -> VGroup:
    """Rows of real text (mono_line, (text, colour, t2c)) on a dark rounded panel (as wide as the
    text plus 0.3 a side, unless `width`). .rows .bg"""
    lines = VGroup(*[mono_line(s, size, col, t2c=t2c) for s, col, t2c in rows])
    p = line_pitch(size)
    for i, ln in enumerate(lines):
        ln.shift(np.array([0, -i * p, 0]) - ln.strut.get_corner(UL))
    width = width or lines.width + 0.6
    bg = RoundedRectangle(width=width, height=lines.height + 2 * pad, corner_radius=0.14,
                          stroke_color=S.GREY_DARK, stroke_width=2).set_fill(bg_color, 1)
    lines.move_to(bg).align_to(bg, LEFT).shift(RIGHT * 0.3)
    g = VGroup(bg, lines)
    g.bg, g.rows = bg, lines
    return g


def text_span(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` in a Text (Text keeps no glyphs for spaces); the whole Text when `sub`
    isn't in it (e.g. in a translated version)."""
    i = t.text.find(sub)
    if i < 0 or len(t) != len("".join(t.text.split())):
        return VGroup(t)
    a, n = len("".join(t.text[:i].split())), len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def underline(glyphs, color: str = TURN, stroke: float = 3.5) -> Line:
    return Line(glyphs.get_corner(DL) + DOWN * 0.05, glyphs.get_corner(DR) + DOWN * 0.05,
                color=color, stroke_width=stroke)


def rich_tag(s: str, color: str = S.GREY, size: float = 22, **kw) -> VGroup:
    """tag() with t2c / t2f for one word (e.g. a command in mono, in white). .box .text"""
    t = label(s, size, color, **kw)
    h = mono("|", size).height + 0.16
    b = RoundedRectangle(width=t.width + 0.4, height=h, corner_radius=h / 2,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def extend_chip(scene, q: VGroup, v: VGroup, run_time: float = 0.7) -> None:
    """Morph chip q into chip v when v's text extends q's ("httpx 0.13" -> "httpx 0.13.3"): the box
    stretches, the shared glyphs slide into place one-to-one and only the new ones appear. (A plain
    Transform pads the shorter glyph list with duplicates spread through it, so the letters scramble
    mid-morph.) Falls back to a ReplacementTransform when v doesn't extend q (e.g. translated)."""
    n = len(q.text)
    if v.text.text.startswith(q.text.text) and n == len("".join(q.text.text.split())) \
            and len(v.text) == len("".join(v.text.text.split())):
        rest = VGroup(*v.text[n:])
        scene.play(Transform(q.box, v.box), Transform(q.text, VGroup(*v.text[:n])),
                   FadeIn(rest, shift=LEFT * 0.1), run_time=run_time)
        scene.remove(q, rest)
        scene.add(v)
    else:
        scene.play(ReplacementTransform(q, v), run_time=run_time)


def toolbox(w: float, h: float, color: str, fill: float = 0.1) -> VGroup:
    """A toolbox (as in S08): a rounded body with a handle on top. .body .handle"""
    body = box(w, h, color, fill_opacity=fill, radius=0.12, stroke=3)
    hw, hh = min(1.0, w * 0.3), 0.24
    handle = VMobject(stroke_color=color, stroke_width=4)
    handle.set_points_as_corners([[-hw / 2, 0, 0], [-hw / 2, hh, 0], [hw / 2, hh, 0], [hw / 2, 0, 0]])
    handle.next_to(body, UP, buff=0)
    g = VGroup(body, handle)
    g.body, g.handle = body, handle
    return g


class Pipenv(VoiceScene):
    def construct(self):
        assert len(SAY) == 3, len(SAY)

        # ========================================================== 0 · pipenv, and where you'll meet it
        title = mono("pipenv", 48, PIPENV).move_to([0, 2.9, 0])
        sub = label("an older way to do the same job", 26, S.GREY).next_to(title, DOWN, buff=0.18)

        card = box(6.2, 3.5, S.GREY_DARK, fill_opacity=0.05).move_to([-3.2, -0.7, 0])
        repo = VGroup(folder_glyph(0.32, S.GREY), mono("dlops-io/simple-translate", 24, INK)) \
            .arrange(RIGHT, buff=0.2)
        repo.align_to(card, LEFT).align_to(card, UP).shift(RIGHT * 0.3 + DOWN * 0.3)
        main_lane = lane(-0.05, -5.95, -3.0, 3, VENV, "main")
        old_lane = lane(-1.15, -5.95, -4.15, 2, PIPENV, "pipenv")
        pipfile = chip("Pipfile", PIPENV, 22, font=MONO).next_to(old_lane.chip, RIGHT, buff=0.2)
        old_note = label("older version of this tutorial", 24, S.GREY)
        old_note.next_to(old_lane.line, DOWN, buff=0.5).align_to(old_lane.line, LEFT)

        also = label("also using pipenv", 26, S.GREY).move_to([0, 0.75, 0]).align_to([0.45, 0, 0], LEFT)
        aws = chip("simple-translate-aws", PIPENV, 24, font=MONO).next_to(also, DOWN, buff=0.4, aligned_edge=LEFT)
        aws_note = label("AWS track", 22, S.GREY).next_to(aws, DOWN, buff=0.12, aligned_edge=LEFT).shift(RIGHT * 0.2)
        cheese = chip("cheese-app-v0 · api-service", PIPENV, 24, font=MONO)
        cheese.next_to(aws_note, DOWN, buff=0.4).align_to(aws, LEFT)
        cheese_note = label("later in the course", 22, S.GREY).next_to(cheese, DOWN, buff=0.12, aligned_edge=LEFT) \
            .shift(RIGHT * 0.2)
        others = VGroup(also, aws, aws_note, cheese, cheese_note)
        others.shift(UP * (card.get_center()[1] - others.get_center()[1]))

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(title, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("an older way")
            self.play(FadeIn(sub, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("This repo's pipenv branch")
            # the repo and its main branch come in together, so the pipenv lane lands on "pipenv branch"
            self.play(Create(card), FadeIn(repo, shift=RIGHT * 0.15), Create(main_lane.line),
                      LaggedStart(*[GrowFromCenter(d) for d in main_lane.dots], lag_ratio=0.3),
                      FadeIn(main_lane.chip, shift=LEFT * 0.15), run_time=0.8)
            self.play(Create(old_lane.line), LaggedStart(*[GrowFromCenter(d) for d in old_lane.dots], lag_ratio=0.3),
                      FadeIn(old_lane.chip, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("an older version of this tutorial")
            self.play(FadeIn(old_note, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("uses it")
            self.play(FadeIn(pipfile, shift=LEFT * 0.15), Indicate(old_lane.chip, color=PIPENV, scale_factor=1.15),
                      run_time=0.8)
            vo.wait_until("So do the separate")
            self.play(FadeIn(also, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("AWS version")
            self.play(FadeIn(aws, shift=LEFT * 0.2), FadeIn(aws_note), run_time=0.7)
            vo.wait_until("later, the cheese")
            self.play(FadeIn(cheese, shift=LEFT * 0.2), FadeIn(cheese_note), run_time=0.7)

        # ========================================================== 1 · same ideas, different names
        head_uv = at_left(item("uv", UV, 36), HEAD_Y)            # mono_line: the two share a baseline
        head_pe = at_right(item("pipenv", PIPENV, 36), HEAD_Y)
        just_read = tag("just read: no pipenv on this VM", S.GREY).next_to(head_pe.glyphs, RIGHT, buff=0.4)
        rule = Line([-6.3, HEAD_Y - 0.45, 0], [6.3, HEAD_Y - 0.45, 0], color=S.GREY_DARK, stroke_width=2)

        pairs = [("pyproject.toml", VENV, "Pipfile"),
                 ("uv.lock", VENV, "Pipfile.lock"),
                 (".venv/", VENV, "~/.local/share/virtualenvs/<name>-<hash>"),
                 ("uv sync", UV, "pipenv install / pipenv sync"),
                 ("source .venv/bin/activate", VENV, "pipenv shell")]
        lefts, rights, arrows = [], [], []
        for (l, col, r), y in zip(pairs, ROW_Y):
            lefts.append(at_left(item(l, col, 22 if len(l) > 20 else ITEM), y))
            rights.append(at_right(item(r, PIPENV, 22 if len(r) > 30 else ITEM), y))
            arrows.append(row_arrow(y))
        r3_note_l = label("in the project", 22, S.GREY)
        r3_note_l.next_to(lefts[2], DOWN, buff=0.14).align_to(lefts[2].glyphs, RIGHT)
        r3_note_r = label("in your home", 22, S.GREY)
        r3_note_r.next_to(rights[2], DOWN, buff=0.14).align_to(rights[2].glyphs, LEFT)
        r4 = rights[3]
        r4_first = substring(r4, "pipenv install")
        r4_rest = VGroup(*[g for g in r4.glyphs if g not in r4_first.submobjects])
        sub_tag = tag("a subshell", S.GREY)
        sub_tag.next_to(rights[4], DOWN, buff=0.18).align_to(rights[4].glyphs, LEFT)
        exit_tag = rich_tag("a subshell · type exit to leave", S.GREY, t2c={"exit": INK}, t2f={"exit": MONO})
        exit_tag.move_to(sub_tag, aligned_edge=LEFT)
        # the short tag grows into the long one when the long one starts with it (else a cross-fade)
        grows = exit_tag.text.text.startswith(sub_tag.text.text) and \
            len(exit_tag.text) == len("".join(exit_tag.text.text.split()))
        n_sub = len(sub_tag.text)
        exit_rest = VGroup(*exit_tag.text[n_sub:])

        dimmed = []

        def dim_rows():
            anims = [m.animate.set_opacity(0.4) for m in dimmed]
            dimmed.clear()
            return anims

        def morph(k, glyphs=None):
            target = rights[k].glyphs if glyphs is None else glyphs
            # a copy of the uv item travels across and becomes the pipenv item (ReplacementTransform keeps
            # the target's own glyphs; TransformFromCopy would pad them with hidden duplicates that a
            # later set_opacity makes visible)
            return [ReplacementTransform(lefts[k].glyphs.copy(), target, path_arc=-0.35), GrowArrow(arrows[k])]

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(card, repo, main_lane, old_lane, pipfile, old_note, also, aws, aws_note,
                                     cheese, cheese_note, sub)), run_time=0.5)
            self.play(Transform(title, head_pe.glyphs), FadeIn(head_uv.glyphs, shift=RIGHT * 0.2), Create(rule),
                      run_time=0.8)
            self.play(FadeIn(just_read, shift=LEFT * 0.15), run_time=0.5)
            # row 1
            vo.wait_until("The pyproject.toml")
            self.play(FadeIn(lefts[0].glyphs, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("becomes the Pipfile")
            self.play(*morph(0), run_time=0.9)
            dimmed += [lefts[0].glyphs, rights[0].glyphs, arrows[0]]
            # row 2
            vo.wait_until("and uv.lock")
            self.play(FadeIn(lefts[1].glyphs, shift=RIGHT * 0.2), *dim_rows(), run_time=0.5)
            vo.wait_until("becomes Pipfile.lock")
            self.play(*morph(1), run_time=0.9)
            dimmed += [lefts[1].glyphs, rights[1].glyphs, arrows[1]]
            # row 3
            vo.wait_until("The venv lives")
            self.play(FadeIn(lefts[2].glyphs, shift=RIGHT * 0.2), *dim_rows(), run_time=0.5)
            vo.wait_until("in a folder in your home")
            self.play(*morph(2), run_time=1.0)
            self.play(FadeIn(r3_note_r, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("instead of in the project")
            self.play(FadeIn(r3_note_l, shift=UP * 0.1), run_time=0.5)
            dimmed += [lefts[2].glyphs, rights[2].glyphs, arrows[2], r3_note_l, r3_note_r]
            # row 4
            vo.wait_until("The command uv sync")
            self.play(FadeIn(lefts[3].glyphs, shift=RIGHT * 0.2), *dim_rows(), run_time=0.5)
            vo.wait_until("becomes pipenv install")
            self.play(*morph(3, r4_first), run_time=0.9)
            vo.wait_until("or pipenv sync")
            self.play(FadeIn(r4_rest, shift=LEFT * 0.15), run_time=0.6)
            dimmed += [lefts[3].glyphs, r4_first, r4_rest, arrows[3]]
            # row 5
            vo.wait_until("And instead of activating")
            self.play(FadeIn(lefts[4].glyphs, shift=RIGHT * 0.2), *dim_rows(), run_time=0.5)
            vo.wait_until("pipenv shell opens")
            self.play(*morph(4), run_time=0.9)
            vo.wait_until("a new shell inside")
            self.play(FadeIn(sub_tag, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Type exit")
            if grows:
                self.play(Transform(sub_tag.box, exit_tag.box), Transform(sub_tag.text, VGroup(*exit_tag.text[:n_sub])),
                          FadeIn(exit_rest, shift=LEFT * 0.15), run_time=0.6)
                self.remove(sub_tag, exit_rest)
                self.add(exit_tag)
            else:
                self.play(FadeOut(sub_tag), FadeIn(exit_tag), run_time=0.6)
            self.play(Indicate(text_span(exit_tag.text, "exit"), color=INK, scale_factor=1.25), run_time=0.7)

        table = VGroup(title, head_uv.glyphs, just_read, rule, *[m.glyphs for m in lefts], *[m.glyphs for m in rights],
                       *arrows, r3_note_l, r3_note_r, exit_tag)

        # ========================================================== 2 · the puzzle, for real
        # the S05 puzzle chips, then the real versions
        q_old = chip("httpx 0.13", S.GREY, 24, font=MONO).move_to([-CARD_X, CHIP_Y, 0])
        q_new = chip("httpx 0.28", S.GREY, 24, font=MONO).move_to([CARD_X, CHIP_Y, 0])
        v_old = chip(f"httpx {OLD}", PIPENV, 28, font=MONO).move_to(q_old)
        v_new = chip(f"httpx {NEW}", VENV, 28, font=MONO).move_to(q_new)
        when = recorded_tag().next_to(v_new, DOWN, buff=0.2)
        neq = label("≠", 44, INK).move_to([0, CHIP_Y, 0])

        lock = mini_panel([(f"88  {LOCK_KEY}", OUTPUT, {"[0:2]": S.GREY}),
                           ("      …", S.GREY, None),
                           (f"94  {LOCK_VER}", OUTPUT, {"[0:2]": S.GREY})], PANEL)
        sync = mini_panel([(s, OUTPUT, None) for s in SYNC_ROWS], TERM_BG, width=lock.bg.width)
        lock.move_to([-CARD_X, 1.75, 0])
        lock_head = VGroup(chip("pipenv", PIPENV, 22, font=MONO), mono("Pipfile.lock", 20, S.GREY),
                           label("· lines 88–94", 20, S.GREY)).arrange(RIGHT, buff=0.16)
        lock_head.next_to(lock, UP, buff=0.14).align_to(lock, LEFT)
        sync.move_to([CARD_X, 1.75, 0])
        sync_head = VGroup(chip("main", VENV, 22, font=MONO), mono("uv sync", 20, S.GREY),
                           label("· our output", 20, S.GREY)).arrange(RIGHT, buff=0.16)
        sync_head.next_to(sync, UP, buff=0.14).align_to(sync, LEFT)
        ul_key = underline(substring(lock.rows[0], '"httpx"'))
        ul_ver = underline(substring(lock.rows[2], OLD))
        ul_new = underline(substring(sync.rows[1], f"httpx=={NEW}"))

        # S05's picture: one shared shelf, one httpx slot
        board = Line([-SHELF_HALF, SHELF_Y, 0], [SHELF_HALF, SHELF_Y, 0], color=SYSTEM, stroke_width=6)
        board_label = mono("/usr/local/… (pip's)", 22, SYSTEM)
        board_label.next_to(board, UP, buff=0.1).align_to(board, LEFT)
        ill = illustration_tag()
        ill.move_to([6.35 - ill.width / 2, -3.2, 0])
        slot = np.array([SLOT_X, SHELF_Y + 0.33, 0])
        j_new, j_old = jar(SYSTEM, 0.6), jar(SYSTEM, 0.6)
        j_new.move_to(slot)
        j_old.move_to(slot)
        t_new, t_old = mono(NEW, 22, INK), mono(OLD, 22, INK)
        t_new.move_to(slot + UP * 0.58)
        t_old.move_to(slot + UP * 0.58)
        cross = cross_mark(0.6, ERR, 8).move_to([CROSS_X, slot[1] + 0.05, 0])

        tb_l = toolbox(3.0, 1.1, VENV).move_to([-BOX_X, BOX_Y, 0])
        tb_r = toolbox(3.0, 1.1, VENV).move_to([BOX_X, BOX_Y, 0])
        name_l = label("pipenv's venv", 22, S.GREY).next_to(tb_l.body, DOWN, buff=0.14)
        name_r = label("uv's .venv", 22, S.GREY).next_to(tb_r.body, DOWN, buff=0.14)
        ok = check_mark(0.5, VENV, 7).move_to([0, BOX_Y, 0])

        def in_box(tb, version):
            """Targets for a jar and its version inside a toolbox: GREEN jar at left, version beside it."""
            g = VGroup(jar(VENV, 0.6), mono(version, 22, INK)).arrange(RIGHT, buff=0.2)
            g.move_to(tb.body)
            return g[0], g[1]

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(table), run_time=0.6)
            self.play(LaggedStart(FadeIn(q_old, shift=DOWN * 0.15), FadeIn(q_new, shift=DOWN * 0.15), lag_ratio=0.4),
                      run_time=0.8)
            vo.wait_until("That branch's lock file")
            self.play(FadeIn(lock_head, shift=DOWN * 0.1), FadeIn(lock, shift=DOWN * 0.1), run_time=0.8)
            vo.wait_until("pins httpx")
            self.play(Create(ul_key), Create(ul_ver), run_time=0.6)
            extend_chip(self, q_old, v_old)
            vo.wait_until("while our uv sync")
            self.play(FadeIn(sync_head, shift=DOWN * 0.1), FadeIn(sync, shift=DOWN * 0.1), run_time=0.8)
            vo.wait_until("installed 0.28.1")
            self.play(Create(ul_new), run_time=0.5)
            extend_chip(self, q_new, v_new)
            vo.wait_until("at the time of recording")
            self.play(FadeIn(when, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Two versions of the same app")
            self.play(Indicate(lock_head[0], color=PIPENV, scale_factor=1.2),
                      Indicate(sync_head[0], color=VENV, scale_factor=1.2), run_time=0.9)
            vo.wait_until("two versions of httpx")
            self.play(FadeIn(neq, scale=0.6), Indicate(v_old, color=INK, scale_factor=1.08),
                      Indicate(v_new, color=VENV, scale_factor=1.08), run_time=0.9)

            # one shared system Python: the last install wins
            vo.wait_until("On one shared system Python")
            # the evidence has done its job: it steps back so the picture (and the two chips feeding it)
            # carry the sentence. Only visible parts dim (a mono_line's strut must stay invisible).
            evidence = VGroup(lock.bg, sync.bg, *[r.glyphs for r in (*lock.rows, *sync.rows)],
                              lock_head, sync_head, ul_key, ul_ver, ul_new)
            self.play(Create(board), FadeIn(board_label, shift=UP * 0.1), FadeIn(ill),
                      evidence.animate.set_opacity(0.3), run_time=0.5)
            self.play(GrowFromPoint(j_new, v_new.get_center()), GrowFromPoint(t_new, v_new.get_center()),
                      run_time=0.6)
            self.play(GrowFromPoint(j_old, v_old.get_center()), GrowFromPoint(t_old, v_old.get_center()),
                      j_new.animate.move_to([SHELF_HALF + 0.6, SHELF_Y - 0.75, 0]).rotate(-1.4).set_color(ERR),
                      t_new.animate.move_to([SHELF_HALF + 0.75, SHELF_Y - 0.15, 0]).set_color(ERR),
                      run_time=0.7)
            self.play(Create(cross), run_time=0.35)

            # two venvs: they can
            vo.wait_until("In two venvs")
            jl, tl = in_box(tb_l, OLD)
            jr, tr = in_box(tb_r, NEW)
            half_l = Line(board.get_start(), board.get_center(), color=SYSTEM, stroke_width=6)
            half_r = Line(board.get_center(), board.get_end(), color=SYSTEM, stroke_width=6)
            self.remove(board)
            self.add(half_l, half_r)
            self.play(FadeOut(VGroup(cross, board_label)),
                      ReplacementTransform(half_l, tb_l), ReplacementTransform(half_r, tb_r),
                      ReplacementTransform(j_old, jl), ReplacementTransform(t_old, tl),
                      ReplacementTransform(j_new, jr), ReplacementTransform(t_new, tr),
                      run_time=0.9)
            self.play(Create(ok), FadeIn(name_l, shift=UP * 0.1), FadeIn(name_r, shift=UP * 0.1), run_time=0.5)

        self.wait(1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
