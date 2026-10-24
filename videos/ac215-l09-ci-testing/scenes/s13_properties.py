"""S13 · Properties, not examples (guest lecture, step-05a; tracker E7).

Beats (script.md, ## S13; one voiceover block each):
0. TRACKER E6 -> E7, `Lecture 9 · slides 78–84` (top right, whole scene). A 14-row `laptop ·
   babykev` terminal (20 pt): `git switch --detach step-05a` -> s05a-01: …, 3 (cut); `just setup` (small:
   s05a-02: 2, …); `just test` -> s05a-03: …, 11–17 (cut after their progress marks), …, 66 (cut),
   67 (cut after the timing). `▶ your turn` on `just test`. The F of test_model.py, line 66 and
   `1 failed` RED, `102 passed` GREEN: the live result, printed honestly. The terminal shrinks to a
   4-row strip (command, …, 66, 67). Above it, the two-dot picture: before[2] and after[2] on top of
   each other over the capture's own tensor (s05a-03:48, identical to 4 decimals), GREEN "same to 4
   decimals"; a lens opens and the dots part, RED "last bits differ". Beside it a GREY card, tag
   `recorded · walk.md`: "the author's Mac: 103 passed" (walk.md:621), and a GREY note "bit-exact
   across machines: a stronger promise". Line 67 is ringed on "this machine measured it".
1. TRACKER E7. The strip is cleared and grows to 6 rows; the walk's wrong-fix perl (walk.md:627 = s05a-04) is typed at
   20 pt and soft-wraps at the terminal's edge -> no output. As it is spoken, V6's 4×4 grid (the
   wrong fix's mask for state 1 · questions 1, 1, 1) appears; the adjacent-question cells it correctly
   blocks get RED boxes, the two-back cell it wrongly leaves open a pulsing YELLOW box. The six-token
   checker `uv run python - <<'EOF'` + `…` (walk.md:628–634; a GREY row tag "full script: study guide"
   beside the `…` row) -> s05a-05: 8–13 in two chunks, `ok` GREEN, while a 6×6 grid fills row by
   row; a GREY shrug glyph. The four-token checker (walk.md:635–641) -> s05a-06: 8–11; row 4 `WRONG`
   RED, the 4×4 grid's row 4 boxed RED; the 4×4 card's caption "state 1 · questions 1, 1, 1".
2. CODE(babykev/tests/unit/test_mask.py: 58–65) at 20 pt (lines 60 and 64 get the house cut). A
   PURPLE die beside `@given(shapes)` rolls ("hypothesis draws"). The chip "a state of 1 to 6
   tokens · up to 4 questions of 1 to 5" (line 9's comment on line 10's `shapes`) lands above the
   code; beside it the counter spins up: "shapes to cover with pictures: 4,686" (walk.md:625). The
   assert line (65) bars GREEN; `allowed(` and `siblings` on it flash. PONDER 5 (8 s).
3. The ponder's answer drawn: the 4×4 wrong-fix grid returns with its YELLOW two-back cell and the
   caption "state 1 · questions 1, 1, 1". TRACKER E7, a 14-row terminal: `just test -k
   no_question_sees_another` (walk.md:653) -> s05a-08: …, 9, …, 11 (cut), …, 25, …, 41–45, …; the F RED,
   line 25 `shape = (1, [1, 1, 1])` YELLOW. The terminal shrinks to a 3-row strip (command, …, 25);
   above it a PURPLE die rolls while a RED-framed counter-example grid shrinks 9×9 -> 6×6 -> 4×4 (GREY
   tag `illustration` on the two intermediate shapes, SHRINK_PATH; they carry no numbers); the
   final 4×4 is the captured shape (the tag leaves, the caption returns). `▶ your turn` on the
   command. The siblings grid (GREY) slides over the allowed grid; the one overlapping cell (row 4,
   column 2) lights RED.
4. TRACKER E7. A 14-row terminal: `git restore src/babykev/model.py` (walk.md:654), the mask-back
   perl (walk.md:667 = s05a-10, soft-wrapped) -> no output, `just test` (walk.md:668) -> s05a-11: …,
   14–17 (cut), …, 306 (cut), 307 (cut); `▶ your turn`; `8 failed, 95 passed` RED and every F RED.
   `git restore src/babykev/model.py` (walk.md:669), `sed -n '151p' src/babykev/model.py`
   (walk.md:670) -> s05a-13: 2, GREEN; its `s[None, :] == s[:, None]` flashes.
5. TRACKER E7. `just types` (walk.md:679) -> s05a-14: 2–3, `All checks passed!` GREEN; `just --show
   check` (walk.md:683) -> s05a-15: …, 9–14, `    just types` YELLOW. V1: the gate table (all six
   rows; config's tools as in S11) and the types row fills and settles. Then `just smoke local`
   (walk.md:674) -> s05a-17: 2, …, 4, …, 31–32; `▶ your turn`; `4 of 15 right` YELLOW, line 32
   GREY. Fade to an empty frame.

Deviations (reported to the coordinator):
- The two perl lines (211 and 179 characters, one single-quoted argument with spaces inside the
  quotes) cannot fold at a space outside quotes with a backslash: they soft-wrap at the terminal's edge,
  exactly as a terminal shows a long typed line (the rows join back to the command; asserted).
- The checker heredocs are walk.md:628–634 and 635–641 (the script cites 628–635 / 636–641).
- Over-wide lines get the house "…" cut (s05a-01:3, s05a-03:11–17/66/67, s05a-08:11, s05a-11:14–17/
  306/307, test_mask.py:60/64); every skipped range gets a "…" row (s05a-01 before 3, s05a-02 after 2, s05a-03 before 11
  and 17/66, s05a-08 before 9, 9/11, 11/25, 25/41, after 45, s05a-11 before 14 and 17/306, s05a-15 before 9, s05a-17
  2/4, 4/31). `just setup` is shown small: its first output line and a "…".
- The two-dot picture's tensor text is s05a-03:48's own (both tensors print identically there);
  the dot names `before[2]` / `after[2]` are the failing assert's (s05a-03:46).
- "bit-exact across machines: a stronger promise" (GREY note) and "shapes to cover with pictures"
  are the narration's / the script's own words. The die's pips are a picture, not data.
- SHRINK_PATH's two intermediate shapes are drawn as bare grids (no token numbers, no shape text)
  under an `illustration` tag; only the final 4×4 carries numbers, and it is the captured shape.
"""

import re

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer.scene import VoiceScene
from explainer import style as S

from common import (ERR, INK, NARRATION, P_BABYKEV, PASS, SEG_FOUR, SEG_SIX, SHRINK_PATH, TOOL, TURN,
                    T_BABYKEV, Dice, GateTable, MaskGrid, attach, beside, capture, code_panel, code_span,
                    cut, excerpt, glyph_range, illustration_tag, label, line_bar, lref, mask_rows, mono,
                    note, pause_and_ponder, pin, recorded_tag, resize, ring, row_tag, segment_ids,
                    shape_caption, shape_text, steady, strip_top, substring, term, track, tracker, turn_row,
                    type_cmd, walk, your_turn)

SAY = NARRATION["S13"]
PT = 20                                  # terminal size: 72 characters a row
COLS = 72
MASK_SRC = "babykev/tests/unit/test_mask.py"
FIRST, LAST = 58, 65                     # the rule test
CONFIG_ROW = {"config": ("config files", "yamllint, uv, just", "just lint-config", "yes", True)}   # S11's


# ---------------------------------------------------------------- terminal helpers (S12's)
def fit(lines):
    """Capture lines ready to print: every row must already fit (cuts are made explicitly)."""
    for x in lines:
        s = x if isinstance(x, str) else x[0]
        assert len(s) <= COLS, (len(s), s)
    return list(lines)


def room(scene, t, n: int, run_time: float = 0.3) -> None:
    """Make room for n new rows: the oldest rows fade where they are, then the rest slide up."""
    over = len(t.lines) + n - t.rows
    if over <= 0:
        return
    gone = VGroup(*t.lines.submobjects[:over])
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(gone), run_time=run_time * 0.4)
    for m in gone:
        t.lines.remove(m)
    scene.remove(gone, *gone.get_family())
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=run_time * 0.6)


def out(scene, t, lines, run_time: float = 0.6, lag: float = 0.08) -> VGroup:
    """Print capture lines ((text, colour) or text) at once (they must fit the box)."""
    items = fit(lines)
    assert len(items) <= t.rows, (len(items), t.rows)
    room(scene, t, len(items))
    return t.print(scene, items, run_time=run_time, lag=lag)


def typ(scene, t, cmd: str, type_time: float | None = None, soft: bool = False):
    """type_cmd with room made first. soft=True: a command whose long quoted argument cannot fold
    at a space outside quotes soft-wraps at the terminal's edge, as a terminal shows it (the rows
    join back to exactly the prompt and the command)."""
    p = t.prompt + " "
    if not soft:
        room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
        return type_cmd(scene, t, cmd, type_time)
    full = p + cmd
    rows = [full[i:i + COLS] for i in range(0, len(full), COLS)]
    assert "".join(rows) == full and all(len(r) <= COLS for r in rows)
    room(scene, t, len(rows))
    t.fold = lambda text, first_prefix=0: list(rows)
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


def rows_of(line) -> list:
    return list(line.rows) if hasattr(line, "rows") else [line]


def flash(tg, color, scale: float = 1.15, run_time: float = 0.7) -> list:
    """Flash a filled tag: its word and its outline (Indicate on the whole tag hides the word)."""
    return [Indicate(tg.text, color=color, scale_factor=scale, run_time=run_time),
            tg.box.animate(rate_func=there_and_back, run_time=run_time).set_stroke(width=4)]


def tag_on(scene, line, mk, buff: float = 0.45):
    """Pin a row tag beside a typed command (its last row); returns (row, tag)."""
    r = rows_of(line)[-1]
    tg = beside(mk(), r, buff=buff)
    assert tg.get_right()[0] <= 6.55, tg.get_right()
    pin(scene, r, tg)
    return r, tg


def wipe(scene, t, *extra, run_time: float = 0.4):
    """Clear the terminal's rows (and their pinned marks) together with `extra` overlays."""
    gone = VGroup(*t.lines.submobjects, *extra)
    if len(gone):
        scene.play(FadeOut(gone), run_time=run_time)
    scene.remove(gone, *gone.get_family())
    for m in list(t.lines):
        t.lines.remove(m)


def drop(scene, *mobs, run_time: float = 0.5):
    """Fade mobjects (and their families) off the scene for good."""
    g = VGroup(*mobs)
    scene.play(FadeOut(g), run_time=run_time)
    scene.remove(g, *g.get_family())


def marks_cut(s: str) -> str:
    """A pytest progress row cut after its progress marks (the padding and `[ nn%]` dropped)."""
    m = re.match(r"^(\S+ [.F]+)\s+\[", s)
    assert m, s
    return cut(s, m.group(1))


def f_glyphs(row) -> VGroup:
    """Every F in a progress row's marks."""
    head = row.text.index(" ") + 1
    return VGroup(*[g for k, ch in enumerate(row.text) if k >= head and ch == "F"
                    for g in glyph_range(row, k, k + 1)])


def study_tag() -> VGroup:
    """'full script: study guide', row-sized: pinned beside the '…' that stands for the heredoc."""
    return row_tag("full script: study guide", S.GREY)


def pulse(mobs, color, width: float = 6, run_time: float = 0.7):
    """Outlines flash (Indicate floods a filled shape with its colour)."""
    return AnimationGroup(*[m.animate(rate_func=there_and_back).set_stroke(color, width=width) for m in mobs],
                          run_time=run_time)


# ---------------------------------------------------------------- pictures
def shrug(color=S.GREY) -> VGroup:
    """A shrug drawn in lines (a kaomoji needs glyphs the house font lacks): head, raised arms."""
    head = Circle(radius=0.2, stroke_color=color, stroke_width=4)
    body = Line(head.get_bottom(), head.get_bottom() + DOWN * 0.5, color=color, stroke_width=4)
    sh = head.get_bottom() + DOWN * 0.12
    arms = VGroup(*[VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
        [sh, sh + np.array([0.38 * s, -0.05, 0]), sh + np.array([0.55 * s, 0.28, 0])]) for s in (-1, 1)])
    hands = VGroup(*[Line(sh + np.array([0.55 * s, 0.28, 0]), sh + np.array([0.72 * s, 0.34, 0]), color=color,
                          stroke_width=4) for s in (-1, 1)])
    return VGroup(head, body, arms, hands)


def shrink_grid(state: int, questions, side: float = 2.6) -> VGroup:
    """An intermediate counter-example (no numbers): the wrong fix's mask for this shape, the cells
    that break the rule RED, in a RED frame."""
    seg = segment_ids(state, questions)
    g = MaskGrid(seg, "wrong_fix", cell=side / len(seg), numbers=False, band=False)
    sib = MaskGrid(seg, "siblings", cell=side / len(seg), numbers=False, band=False)
    bad = g.overlap(sib)
    assert bad, (state, questions)
    for i, j in bad:
        g.cells[i][j].set_fill(ERR, 0.9).set_stroke(ERR, 2)
    frame = Rectangle(width=g.grid.width + 0.18, height=g.grid.height + 0.18, stroke_color=ERR,
                      stroke_width=4).move_to(g.grid)
    return VGroup(g, frame)


class PropertyTests(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)

        sw, setup, test = capture("babykev/s05a-01"), capture("babykev/s05a-02"), capture("babykev/s05a-03")
        wrong, six, four = capture("babykev/s05a-04"), capture("babykev/s05a-05"), capture("babykev/s05a-06")
        rule, hyp = capture("babykev/s05a-07"), capture("babykev/s05a-08")
        rst1, back, again = capture("babykev/s05a-09"), capture("babykev/s05a-10"), capture("babykev/s05a-11")
        rst2, fixl = capture("babykev/s05a-12"), capture("babykev/s05a-13")
        types, show, smoke = capture("babykev/s05a-14"), capture("babykev/s05a-15"), capture("babykev/s05a-17")
        assert sw.cmd == "git switch --detach step-05a" and setup.cmd == walk(610)[2:] and test.cmd == walk(623)[2:]
        assert wrong.cmd == walk(627)[2:] == walk(651)[2:]
        assert six.cmd == walk(628)[2:] == "uv run python - <<'EOF'" and walk(634) == "$ EOF"
        assert four.cmd == walk(635)[2:] and walk(641) == "$ EOF"
        assert [r[2:] for r in (walk(n) for n in range(629, 634))] == six.at((2, 6))
        assert [r[2:] for r in (walk(n) for n in range(636, 641))] == four.at((2, 6))
        assert hyp.cmd == walk(653)[2:] and rst1.cmd == walk(654)[2:] and back.cmd == walk(667)[2:]
        assert again.cmd == walk(668)[2:] and rst2.cmd == walk(669)[2:] and fixl.cmd == walk(670)[2:]
        assert smoke.cmd == walk(674)[2:] and types.cmd == walk(679)[2:] and show.cmd == walk(683)[2:]
        assert wrong.lines == [] and back.lines == [] and rst1.lines == [] and rst2.lines == []
        assert "103 passed" in walk(621) and "4,686 shapes" in walk(625)
        six_rows, four_rows = six.at((8, 13)), four.at((8, 11))
        assert [r.split()[0] for r in six_rows] == mask_rows(SEG_SIX, "want")
        assert [r.split()[1] for r in six_rows] == mask_rows(SEG_SIX, "wrong_fix")
        assert [r.split()[0] for r in four_rows] == mask_rows(SEG_FOUR, "want")
        assert [r.split()[1] for r in four_rows] == mask_rows(SEG_FOUR, "wrong_fix")
        assert hyp.line(25) == shape_text(1, [1, 1, 1]) and SHRINK_PATH[-1] == (1, [1, 1, 1])
        assert rule.at((2, 9)) == excerpt(MASK_SRC, FIRST, LAST).split("\n")
        assert fixl.line(2) == excerpt("babykev/src/babykev/model.py", 151, 151)

        # ========================================================== 0. step-05a: the honest result
        tr = tracker("E", 6)
        ref = lref("78–84")
        t = term(P_BABYKEV, rows=14, title=T_BABYKEV, size=PT)
        assert t.max_chars == COLS, t.max_chars
        test_lines = ["…"] + [marks_cut(test.line(n)) for n in range(11, 18)] + \
            ["…", cut(test.line(66), "test_a_question_cannot_see_its_sibling"), cut(test.line(67), "4.53s")]
        top4 = strip_top(4, PT)

        # the two-dot picture (left) and the recorded card (right), over the 4-row strip
        c0 = np.array([-3.35, 1.95, 0])
        d_b = Dot(c0, radius=0.15, color=INK)
        d_a = Circle(radius=0.15, stroke_color=INK, stroke_width=4).move_to(c0)
        n_b = mono("before[2]", 22, INK)
        n_a = mono("after[2]", 22, INK)
        n_b.next_to(c0, LEFT, buff=0.95)
        n_a.next_to(c0, RIGHT, buff=0.95)
        pair = re.findall(r"tensor\(\[[^\]]*\]\)", test.line(48))
        assert len(pair) == 2 and pair[0] == pair[1], pair        # before[2] and after[2] print the same
        tens = mono(pair[0], PT, S.GREY)
        tens.move_to([c0[0], 1.05, 0])
        same = label("same to 4 decimals", 24, PASS).move_to([c0[0], 0.45, 0])
        differ = label("last bits differ", 24, ERR).move_to([c0[0], -0.2, 0])
        lens = Circle(radius=0.62, stroke_color=INK, stroke_width=3).move_to(c0)
        handle = Line(lens.point_at_angle(-PI / 4), lens.point_at_angle(-PI / 4) + np.array([0.3, -0.3, 0]),
                      color=INK, stroke_width=5)
        card_txt = VGroup(label("the author's Mac:", 26, INK), mono("103 passed", 26, INK)).arrange(DOWN, buff=0.22)
        card_box = RoundedRectangle(width=card_txt.width + 1.0, height=card_txt.height + 0.7, corner_radius=0.16,
                                    stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        card = VGroup(card_box, card_txt)
        card.move_to([3.55, 1.15, 0])
        card_txt.move_to(card_box)
        rec = recorded_tag()
        rec.next_to(card_box, UP, buff=0.15).align_to(card_box, LEFT)
        promise = VGroup(note("bit-exact across machines:", S.GREY, 24),
                         note("a stronger promise", S.GREY, 24)).arrange(DOWN, buff=0.1)
        promise.next_to(card_box, DOWN, buff=0.35)
        assert tens.get_left()[0] > -6.6 and tens.get_right()[0] < card_box.get_left()[0] - 0.3
        assert differ.get_bottom()[1] > top4 + 0.1 and promise.get_bottom()[1] > top4 + 0.1
        assert rec.get_top()[1] < 2.85 and n_b.get_left()[0] > -6.6

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            self.play(track(tr, 7), run_time=0.4)
            typ(self, t, sw.cmd, type_time=0.5)
            out(self, t, ["…", cut(sw.line(3), "the tests that see the mask")], run_time=0.25)
            typ(self, t, setup.cmd, type_time=0.3)
            out(self, t, [setup.line(2), "…"], run_time=0.3)
            vo.wait_until("First, honesty")
            j_ln = typ(self, t, test.cmd, type_time=0.3)
            _, yj = tag_on(self, j_ln, turn_row)
            vo.wait_until("on this machine just test says")
            j_out = out(self, t, test_lines, run_time=0.8, lag=0.05)
            model_row, l66, l67 = j_out[5], j_out[9], j_out[10]
            assert model_row.text.startswith("tests/unit/test_model.py") and l67.text.startswith("=")
            vo.wait_until("1 failed, 102 passed")
            one, ok102 = substring(l67, "1 failed"), substring(l67, "102 passed")
            self.play(one.animate.set_color(ERR), ok102.animate.set_color(PASS), run_time=0.3)
            self.play(Indicate(one, color=ERR, scale_factor=1.2), Indicate(ok102, color=PASS, scale_factor=1.15),
                      run_time=0.7)
            vo.wait_until("The failing test")
            fm = f_glyphs(model_row)
            self.play(fm.animate.set_color(ERR), l66.animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(fm, color=ERR, scale_factor=1.6),
                      Indicate(substring(l66, "test_a_question_cannot_see_its_sibling"), color=ERR,
                               scale_factor=1.08), run_time=0.8)
            vo.wait_until("bit for bit")
            resize(self, t, 4, keep=[j_ln, j_out[8], l66, l67], run_time=0.6)
            self.play(FadeIn(d_b, scale=0.5), FadeIn(d_a, scale=0.5), FadeIn(n_b, shift=RIGHT * 0.15),
                      FadeIn(n_a, shift=LEFT * 0.15), FadeIn(tens, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(same, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("torch sums in a different order")
            self.play(Create(lens), Create(handle), run_time=0.6)
            self.play(d_b.animate.shift(LEFT * 0.3), d_a.animate.shift(RIGHT * 0.3).set_stroke(ERR),
                      FadeIn(differ, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("there all 103 pass")
            self.play(FadeIn(card_box, scale=0.96), FadeIn(card_txt, shift=UP * 0.1), FadeIn(rec, shift=DOWN * 0.1),
                      run_time=0.6)
            vo.wait_until("as the walk records")
            self.play(*flash(rec, S.GREY), run_time=0.7)
            vo.wait_until("Hermetic means")
            # (fm left the screen with the resize: indicating it again would bring a stray F back)
            self.play(Indicate(substring(l66, "test_a_question_cannot_see_its_sibling"), color=ERR,
                               scale_factor=1.06), d_a.animate(rate_func=there_and_back).set_stroke(width=8),
                      run_time=0.8)
            vo.wait_until("bit exactness across machines")
            self.play(FadeIn(promise[0], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a stronger promise")
            self.play(FadeIn(promise[1], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("this machine measured it")
            r67 = ring(substring(l67, "1 failed, 102 passed"), INK, buff=0.05)
            self.play(Create(r67), run_time=0.5)
            attach(self, l67, r67)

        # ========================================================== 1. a wrong fix; two pictures
        top6 = strip_top(6, PT)
        g4 = MaskGrid(SEG_FOUR, "wrong_fix", cell=0.52)       # (smaller cells crowd the band names)
        g4.move_to([2.7, 0, 0]).align_to([0, 2.9, 0], UP)    # clear of the lecture tag (bottom 3.13)
        blocked, opened = g4.wrong_fix_marks()
        cap4 = label(shape_caption(1, [1, 1, 1]), 22, INK).next_to(g4, DOWN, buff=0.15)
        g6 = MaskGrid(SEG_SIX, "wrong_fix", cell=0.38)
        g6.move_to([-3.5, 0, 0]).align_to([0, 2.72, 0], UP)
        sh = shrug().move_to([-0.55, 0.9, 0])
        assert cap4.get_bottom()[1] > top6 + 0.1 and g6.get_bottom()[1] > top6 + 0.1, (cap4.get_bottom(), top6)
        assert g6.get_right()[0] < sh.get_left()[0] - 0.2 and sh.get_right()[0] < g4.get_left()[0] - 0.2
        assert len(opened) == 1 and len(blocked) == 2 and g4.get_top()[1] < ref.get_bottom()[1] - 0.15

        with self.voiceover(SAY[1]) as vo:
            pic = VGroup(d_b, d_a, n_b, n_a, tens, same, differ, lens, handle, card, rec, promise)
            wipe(self, t, pic, run_time=0.5)
            resize(self, t, 6, run_time=0.4)
            vo.wait_until("A deliberately wrong fix goes in")
            typ(self, t, wrong.cmd, type_time=1.3, soft=True)
            self.play(FadeIn(g4), run_time=0.6)
            vo.wait_until("blocks only the question just before")
            self.play(LaggedStart(*[Create(b) for b in blocked], lag_ratio=0.3), run_time=0.6)
            self.play(Create(opened), run_time=0.4)
            self.play(pulse(opened, TURN, width=9), run_time=0.6)
            vo.wait_until("The six token picture")
            wipe(self, t, run_time=0.25)
            typ(self, t, six.cmd, type_time=0.35)
            dots6 = out(self, t, ["…"], run_time=0.15)[0]
            st6 = beside(study_tag(), dots6, buff=0.35)
            pin(self, dots6, st6, anim=AnimationGroup(FadeIn(st6, shift=LEFT * 0.1),
                                                      FadeIn(VGroup(g6.col_labels, g6.row_labels, g6.band))),
                run_time=0.3)
            p1 = out(self, t, six_rows[:3], run_time=0.25, lag=0.05)
            self.play(LaggedStart(*[FadeIn(VGroup(*g6.cells[i])) for i in range(3)], lag_ratio=0.3),
                      *[substring(r, "ok").animate.set_color(PASS) for r in p1], run_time=0.3)
            p2 = out(self, t, six_rows[3:], run_time=0.25, lag=0.05)
            self.play(LaggedStart(*[FadeIn(VGroup(*g6.cells[i])) for i in range(3, 6)], lag_ratio=0.3),
                      *[substring(r, "ok").animate.set_color(PASS) for r in p2], run_time=0.3)
            self.remove(*[c for row in g6.cells for c in row], g6.col_labels, g6.row_labels, g6.band)
            self.add(g6)
            vo.wait_until("it cannot tell")
            self.play(FadeIn(sh, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("A four token picture can")
            wipe(self, t, run_time=0.2)
            typ(self, t, four.cmd, type_time=0.3)
            dots4 = out(self, t, ["…"], run_time=0.15)[0]
            pin(self, dots4, beside(study_tag(), dots4, buff=0.35), run_time=0.2)
            out(self, t, four_rows[:2], run_time=0.25, lag=0.05)
            q2 = out(self, t, four_rows[2:], run_time=0.25, lag=0.05)
            w = substring(q2[1], "WRONG")
            box4 = g4.row_box(3, ERR)
            self.play(w.animate.set_color(ERR), Create(box4), FadeIn(cap4, shift=UP * 0.1),
                      *[substring(r, "ok").animate.set_color(PASS) for r in t.lines if r.text.endswith(" ok")],
                      run_time=0.4)
            self.play(Indicate(w, color=ERR, scale_factor=1.25), g4.flash_rows([3]), run_time=0.7)
            self.add(blocked, opened, box4)          # flash_rows re-added row 4's cells over the boxes

        # ========================================================== 2. state the rule once; ponder
        lines = excerpt(MASK_SRC, FIRST, LAST).split("\n")
        lines[60 - FIRST] = cut(lines[60 - FIRST], "# The lengths of a state")
        lines[64 - FIRST] = cut(lines[64 - FIRST], "& (seg[:, None] > 0)")
        assert all(len(s) <= COLS for s in lines), [len(s) for s in lines]
        panel = code_panel("\n".join(lines), "tests/unit/test_mask.py", FIRST, "python", font_size=PT)
        panel.move_to([0, 0, 0]).align_to([0, 1.75, 0], UP)
        for k in (60 - FIRST, 64 - FIRST):           # the house cut: pygments paints it as an error token
            code_span(panel.code, k, "…").set_color(S.GREY)
        assert panel.width <= 13.1 and panel.get_bottom()[1] > -3.5, (panel.width, panel.get_bottom())
        given = code_span(panel.code, 0, "@given(shapes)")
        l59 = panel.code.code_lines[59 - FIRST]
        die = Dice(3, side=0.5).move_to([l59.get_right()[0] + 1.0, given.get_center()[1], 0])   # clear of line 59
        chp = VGroup(label("a state of 1 to 6 tokens · up to 4 questions of 1 to 5", 22, INK))
        chp_box = RoundedRectangle(width=chp.width + 0.48, height=0.56, corner_radius=0.2, stroke_color=TOOL,
                                   stroke_width=2.5).set_fill(TOOL, 0.14)
        chp.move_to(chp_box)
        chip_g = VGroup(chp_box, chp)
        chip_g.move_to([0, 2.38, 0]).align_to([-6.45, 0, 0], LEFT)
        cnt_l = label("shapes to cover with pictures:", 22, S.GREY)
        num = steady("0", 26, INK)
        cnt = VGroup(cnt_l, num)
        cnt_l.next_to(chip_g, RIGHT, buff=0.35)
        num.next_to(cnt_l, RIGHT, buff=0.15).align_to(cnt_l, DOWN)
        val = ValueTracker(0)
        assert cnt_l.get_right()[0] + steady("4,686", 26).width + 0.15 < 6.55, cnt_l.get_right()
        assert chip_g.get_top()[1] < 2.85 and panel.get_top()[1] < chip_g.get_bottom()[1] - 0.1

        with self.voiceover(SAY[2]) as vo:
            drop(self, t, g4, blocked, opened, box4, cap4, g6, sh, run_time=0.5)
            for m in list(t.lines):
                t.lines.remove(m)
            vo.wait_until("State the rule once instead")
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("lets hypothesis draw any request shape")
            rg = ring(given, TOOL, buff=0.06)
            self.play(Create(rg), FadeIn(die, scale=0.6), run_time=0.5)
            self.play(die.roll(5), run_time=0.4)
            self.play(die.roll(2), run_time=0.4)
            vo.wait_until("a state of 1 to 6 tokens")
            self.play(FadeIn(chip_g, shift=DOWN * 0.2), Indicate(code_span(panel.code, 0, "shapes"), color=TOOL,
                                                                  scale_factor=1.2), run_time=0.7)
            self.play(die.roll(6), run_time=0.4)
            vo.wait_until("Those sizes allow")
            self.play(FadeIn(cnt_l, shift=LEFT * 0.1), FadeIn(num), run_time=0.4)
            left = num.get_left()

            def spin(m):
                m.become(steady(f"{int(round(val.get_value())):,}", 26, INK))
                m.shift(left - m.get_left())

            num.add_updater(spin)
            self.play(val.animate.set_value(4686), run_time=1.3, rate_func=rate_functions.ease_out_cubic)
            num.clear_updaters()
            vo.wait_until("too many for pictures")
            self.play(Indicate(num, color=TURN, scale_factor=1.25), run_time=0.7)
            vo.wait_until("It asserts")
            bar65 = line_bar(panel.code, 65 - FIRST, PASS, 0.22)
            self.play(FadeIn(bar65), run_time=0.4)
            vo.wait_until("no allowed pair")
            self.play(Indicate(code_span(panel.code, 65 - FIRST, "allowed("), color=PASS, scale_factor=1.15),
                      run_time=0.6)
            vo.wait_until("a sibling pair")
            self.play(Indicate(code_span(panel.code, 65 - FIRST, "siblings"), color=PASS, scale_factor=1.15),
                      Indicate(code_span(panel.code, 64 - FIRST, "siblings"), color=INK, scale_factor=1.12),
                      run_time=0.7)
            vo.wait_until("Something to ponder")
            self.play(die.roll(4), run_time=0.4)
        ponder = pause_and_ponder(self, "The wrong fix blocks only the question just before.\n"
                                        "What is the smallest request shape\nthat still breaks the rule?", seconds=8)

        # ========================================================== 3. hypothesis finds and shrinks it
        a4 = MaskGrid(SEG_FOUR, "wrong_fix", cell=0.7).move_to([0, 0.45, 0])
        _, a_open = a4.wrong_fix_marks()
        a_cap = label(shape_caption(1, [1, 1, 1]), 24, INK).next_to(a4, DOWN, buff=0.25)
        t3 = term(P_BABYKEV, rows=14, title=T_BABYKEV, size=PT)
        h_lines = hyp.at("…", 9, "…") + [cut(hyp.line(11), "test_mask.py F")] + hyp.at("…", 25, "…", (41, 45), "…")
        top3 = strip_top(3, PT)
        gx, gy = -1.2, 0.85
        steps = [shrink_grid(*s).move_to([gx, gy, 0]) for s in SHRINK_PATH[:-1]]
        fin = MaskGrid(SEG_FOUR, "wrong_fix", cell=0.6).move_to([gx, gy, 0])
        fin_frame = Rectangle(width=fin.grid.width + 0.18, height=fin.grid.height + 0.18, stroke_color=ERR,
                              stroke_width=4).move_to(fin.grid)
        fin_cap = label(shape_caption(1, [1, 1, 1]), 22, INK).next_to(fin, DOWN, buff=0.15)
        sib = MaskGrid(SEG_FOUR, "siblings", cell=0.6, numbers=False, band=False)
        sib.move_to([3.9, 0, 0]).align_to(fin.grid, UP)
        sib_l = mono("siblings", 22, S.GREY).next_to(sib, DOWN, buff=0.25)
        all_l = mono("allowed", 22, INK).next_to(fin.row_labels, LEFT, buff=0.3)
        hit = fin.overlap(sib)
        assert hit == [(3, 1)], hit
        die3 = Dice(2, side=0.7).move_to([-5.6, gy, 0])
        ill = illustration_tag().move_to([-5.6, gy + 0.85, 0])
        assert fin_cap.get_bottom()[1] > top3 + 0.1 and sib_l.get_bottom()[1] > top3 + 0.1, (fin_cap.get_bottom(), top3)
        assert all(s.get_top()[1] < 2.8 and s.get_bottom()[1] > top3 + 0.1 for s in steps)
        assert fin.get_top()[1] < 2.8 and all_l.get_left()[0] > die3.get_right()[0] + 0.15

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(ponder, panel, rg, die, chip_g, cnt, bar65)
            self.play(FadeOut(gone), FadeIn(a4), run_time=0.6)
            self.remove(gone, *gone.get_family())
            vo.wait_until("a question two steps back")
            self.play(Create(a_open), run_time=0.4)
            self.play(pulse(a_open, TURN, width=10), run_time=0.8)
            self.add(a_open)
            vo.wait_until("so one state token")
            self.play(FadeIn(a_cap, shift=UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[Indicate(b, color=INK, scale_factor=1.1) for b in a4.band], lag_ratio=0.25),
                      run_time=0.9)
            vo.wait_until("And hypothesis finds it")
            drop(self, a4, a_open, a_cap, run_time=0.4)
            self.play(FadeIn(t3, shift=UP * 0.2), run_time=0.4)
            h_ln = typ(self, t3, hyp.cmd, type_time=0.5)
            h_out = out(self, t3, h_lines, run_time=0.7, lag=0.04)
            f_row, l25 = h_out[3], h_out[5]
            assert l25.text == shape_text(1, [1, 1, 1])
            vo.wait_until("the one test fails")
            ff = substring(f_row, "F")
            self.play(ff.animate.set_color(ERR), run_time=0.25)
            self.play(Indicate(ff, color=ERR, scale_factor=1.8), run_time=0.6)
            vo.wait_until("then shrinks the counter example")
            resize(self, t3, 3, keep=[h_ln, h_out[4], l25], run_time=0.5)
            self.play(FadeIn(die3, scale=0.6), FadeIn(ill, shift=DOWN * 0.1), FadeIn(steps[0], scale=1.08),
                      run_time=0.5)
            self.play(die3.roll(5), run_time=0.35)
            self.play(ReplacementTransform(steps[0], steps[1]), die3.roll(3), run_time=0.6)
            vo.wait_until("to exactly that shape")
            self.play(ReplacementTransform(steps[1], VGroup(fin.grid, fin_frame)), die3.roll(1), FadeOut(ill),
                      run_time=0.6)
            self.remove(ill)
            self.play(FadeIn(VGroup(fin.col_labels, fin.row_labels, fin.band)), FadeIn(fin_cap, shift=UP * 0.1),
                      l25.animate.set_color(TURN), run_time=0.5)
            self.remove(fin.grid, fin.col_labels, fin.row_labels, fin.band)
            self.add(fin)
            self.play(Indicate(l25, color=TURN, scale_factor=1.12), run_time=0.5)
            vo.wait_until("Pause and run it.")
            # the command row is too long for a row tag beside it: the house tag stands on the strip
            y3 = your_turn()
            y3.move_to([6.45 - y3.width / 2, t3.box.get_top()[1] + 0.1 + y3.height / 2, 0])
            self.play(FadeIn(y3, shift=DOWN * 0.1), run_time=0.3)
            self.play(*flash(y3, TURN), run_time=0.7)
            vo.wait_until("does not only say no")
            self.play(FadeIn(sib, shift=LEFT * 0.2), FadeIn(sib_l), FadeIn(all_l), run_time=0.5)
            off = [sib.cells[a][b] for a in range(4) for b in range(4) if not sib.allowed[a][b]]
            delta = fin.cells[0][0].get_center() - sib.cells[0][0].get_center()   # cell onto cell
            self.play(FadeOut(VGroup(*off)), run_time=0.3)
            for c in off:
                sib.grid.remove(c)
            self.remove(*off)
            sib_to = sib_l.copy().next_to(fin.grid, RIGHT, buff=0.45)
            self.play(sib.grid.animate.shift(delta).set_fill(opacity=0.3), sib_l.animate.move_to(sib_to),
                      run_time=0.9)
            i, j = hit[0]
            vo.wait_until("the smallest witness")
            self.add(fin.cells[i][j])                    # above the siblings overlay: the lit cell reads RED
            self.play(fin.light(hit), run_time=0.5)
            spot = fin.cell_box(i, j, ERR, stroke=6)
            self.play(Create(spot), run_time=0.3)
            self.play(spot.animate(rate_func=there_and_back).scale(1.3), run_time=0.6)

        # ========================================================== 4. the gate grew teeth; the real fix
        t4 = term(P_BABYKEV, rows=14, title=T_BABYKEV, size=PT)
        a_lines = ["…"] + [marks_cut(again.line(n)) for n in range(14, 18)] + \
            ["…", cut(again.line(306), "test_notebook_prints_what_its"), cut(again.line(307), "34.19s")]

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(t3, y3, fin, fin_frame, fin_cap, sib, sib_l, all_l, die3, spot)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            for m in list(t3.lines):
                t3.lines.remove(m)
            self.play(FadeIn(t4, shift=UP * 0.2), run_time=0.4)
            typ(self, t4, rst1.cmd, type_time=0.4)
            vo.wait_until("put step 5's wrong mask line back")
            typ(self, t4, back.cmd, type_time=1.2, soft=True)
            vo.wait_until("and run just test")
            a_ln = typ(self, t4, again.cmd, type_time=0.3)
            vo.wait_until("pause and try it")
            _, y4 = tag_on(self, a_ln, turn_row)
            self.play(*flash(y4, TURN), run_time=0.45)
            a_out = out(self, t4, a_lines, run_time=0.6, lag=0.04)
            l307 = a_out[7]
            assert l307.text.startswith("=") and "8 failed, 95 passed" in l307.text
            vo.wait_until("8 failed, 95 passed")
            eight = substring(l307, "8 failed, 95 passed")
            self.play(eight.animate.set_color(ERR), a_out[6].animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(eight, color=ERR, scale_factor=1.15), run_time=0.6)
            vo.wait_until("code that sailed through before is refused")
            fs = VGroup(*[f_glyphs(a_out[k]) for k in range(1, 5)])
            self.play(fs.animate.set_color(ERR), run_time=0.3)
            self.play(LaggedStart(*[Indicate(f, color=ERR, scale_factor=1.7) for f in fs], lag_ratio=0.1),
                      run_time=0.9)
            vo.wait_until("A gate refuses only what its tests can see")
            mask_row, model_r = a_out[1], a_out[2]
            assert mask_row.text.startswith("tests/unit/test_mask.py") and model_r.text.startswith("tests/unit/test_model")
            r_m = ring(VGroup(mask_row.glyphs, model_r.glyphs), INK, buff=0.07)
            self.play(Create(r_m), run_time=0.5)
            attach(self, model_r, r_m)
            vo.wait_until("The real fix is one line")
            k = list(t4.lines).index(a_ln)                # rows above `just test`: restore + perl
            room(self, t4, t4.rows - len(t4.lines) + k)
            typ(self, t4, rst2.cmd, type_time=0.35)
            typ(self, t4, fixl.cmd, type_time=0.35)
            f_out = out(self, t4, [fixl.line(2)], run_time=0.3)[0]
            self.play(f_out.animate.set_color(PASS), run_time=0.3)
            vo.wait_until("same question means same segment ID")
            ss = substring(f_out, "s[None, :] == s[:, None]")
            self.play(Indicate(ss, color=PASS, scale_factor=1.15), run_time=0.8)
            u = Line(ss.get_corner(DL) + DOWN * 0.06, ss.get_corner(DR) + DOWN * 0.06, color=PASS, stroke_width=4)
            self.play(Create(u), run_time=0.4)
            attach(self, f_out, u)

        # ========================================================== 5. types join the gate; the smoke
        gt = GateTable(keys=("tests", "format", "docs", "config", "types", "system"),
                       filled=("tests", "format", "docs", "config", "system"), rows=CONFIG_ROW)
        gt.move_to([0, 0.25, 0])
        assert gt.get_top()[1] < 2.85 and gt.get_bottom()[1] > -3.5 and gt.width < 13.2, (gt.get_top(), gt.width)
        smoke_lines = smoke.at(2, "…", 4, "…", (31, 32))

        with self.voiceover(SAY[5]) as vo:
            wipe(self, t4, run_time=0.4)
            vo.wait_until("the new recipe, just types")
            typ(self, t4, types.cmd, type_time=0.3)
            y_out = out(self, t4, types.at((2, 3)), run_time=0.4)
            typ(self, t4, show.cmd, type_time=0.3)
            vo.wait_until("passes")
            self.play(y_out[1].animate.set_color(PASS), run_time=0.3)
            self.play(Indicate(y_out[1], color=PASS, scale_factor=1.12), run_time=0.4)
            vo.wait_until("check has six lines")
            s_out = out(self, t4, show.at("…", (9, 14)), run_time=0.4, lag=0.04)
            jt = s_out[3]
            assert jt.text == "    just types", jt.text
            self.play(jt.animate.set_color(TURN), Indicate(VGroup(*[r.glyphs for r in s_out[1:] if r is not jt]),
                                                           color=INK, scale_factor=1.04), run_time=0.45)
            self.play(FadeOut(t4), FadeIn(gt), run_time=0.35)
            self.remove(t4, *t4.get_family())
            for m in list(t4.lines):
                t4.lines.remove(m)
            gt.fill(self, "types", run_time=0.4)
            gt.settle(self, "types", run_time=0.3)
            self.wait(0.35)
            vo.wait_until("And the smoke")
            t5 = term(P_BABYKEV, rows=14, title=T_BABYKEV, size=PT)
            self.play(FadeOut(gt), FadeIn(t5, shift=UP * 0.2), run_time=0.35)
            self.remove(gt, *gt.get_family())
            m_ln = typ(self, t5, smoke.cmd, type_time=0.3)
            m_out = out(self, t5, smoke_lines, run_time=0.5, lag=0.05)
            l31, l32 = m_out[4], m_out[5]
            vo.wait_until("4 of 15")
            right = substring(l31, "4 of 15 right")
            self.play(right.animate.set_color(TURN), run_time=0.25)
            self.play(Indicate(right, color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("Pause and run the smoke")
            _, y5 = tag_on(self, m_ln, turn_row)
            self.play(*flash(y5, TURN), run_time=0.6)
            vo.wait_until("The 6 was luck")
            self.play(l32.animate.set_color(S.GREY), run_time=0.3)
            self.play(Indicate(l32, color=S.GREY, scale_factor=1.06), run_time=0.7)
            vo.wait_until("an untrained score means nothing")
            r31 = ring(right, TURN, buff=0.06)
            self.play(Create(r31), run_time=0.5)
            attach(self, l31, r31)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
