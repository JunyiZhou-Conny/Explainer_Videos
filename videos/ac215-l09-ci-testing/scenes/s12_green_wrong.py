"""S12 · All green, and the mask is wrong (guest lecture, step-05; tracker E6).

Beats (script.md, ## S12; one voiceover block each):
0. TRACKER E5 -> E6, `Lecture 9 · slides 53–55, 72–75` (top right, whole scene). A 14-row `laptop ·
   babykev` terminal (20 pt): `git switch --detach step-05` -> s05-01: 3 (cut); `just setup` ->
   s05-02: 2, …, 4 (cut), …, 8, …, 44, …, 46–47, …, 49. `Installed 38 packages` and
   `torch==2.14.1+cpu` ringed; `at the time of recording` beside line 44 and beside the uv-build
   warning (its tag from S10). The terminal keeps the setup command and line 44; `just test` ->
   s05-03: …, 11–15 (cut after the dots), …, 29, 30 (cut): the dots, `TOTAL … 94%` and `92 passed`
   GREEN. `▶ your turn` on both commands.
1. The model in one picture (slides 54–55 redrawn): a packed sequence bar (state GREEN, three TEAL
   questions) and V6's 6×6 grid beside it, assembling; the rule as one GREY sentence under the
   grid. Attention arrows from question 2's token to the state and to itself (and the grid's row 6
   lights the same cells); a GREY dashed arrow sneaks toward question 1 and is crossed out RED. The
   question-2 × question-1 block of the grid gets a YELLOW box: "this cell is the whole
   difference"; on "from a causal mask" the block fills (a causal mask, GREY note) and empties again.
2. TRACKER E6. The picture clears; the grid empties and shrinks over a 4-row strip. The walk's
   one-liner (walk.md:589) folds over four rows at 20 pt; `[0, 0, 1, 1, 2, 2]` ringed with the grid's
   segment band; `▶ your turn`. s05-04: 2–7 print in two chunks and each printed row flies into the
   grid (the cells light as the glyphs land). Rows 5–6 flash RED, in the strip and the grid, and the
   four question-1 cells of rows 5–6 get RED boxes. `sed -n '140p' src/babykev/model.py` -> s05-05: 2,
   `torch.ones_like` RED.
3. The strip shrinks to 3 rows; the built grid moves right ("built"), an empty one appears left ("we
   meant"). `uv run python - <<'EOF'` plus one `…` row (walk.md:594–600 collapsed), a GREY tag "full
   script: study guide" at the strip's corner. s05-06: 8–13 print in two chunks; each row's first
   field flies into the left grid. `WRONG` RED (rows 12–13) and the built grid's rows 5–6 flash RED.
   GREY caption "nothing in just check runs this". PONDER (8 s).
4. CODE(babykev-history/step-05-model.py: 137–143) at 20 pt (lines 139 and 143 get the house cut);
   the coverage highlighter sweeps every line GREEN ("lines that ran"); beside it the built grid's
   RED boxes pulse ("what they produced", RED). "necessary · never sufficient" under both.
5. TRACKER E6. 14-row terminal: `uv run ty check` -> s05-07: 2–3, …, 55, `Found 6 diagnostics`
   RED; `just check` -> s05-11: 2–6, …, 22–23, `92 passed` and `Required test coverage of 90%
   reached` GREEN; a YELLOW bracket pairs the two.
6. TRACKER E6. `just smoke local` -> s05-12: 2, …, 5, …, 22–23, 24–25 (cut after the answer), …,
   32–33. `▶ your turn`. `503M parameters` ringed, the model name ringed BLUE (the Hub), `6 of 15
   right` YELLOW, line 33 GREY. The ms figures are not highlighted. Fade to an empty frame.

Deviations (reported to the coordinator):
- s05-02:4 (111 columns): the script says "wrap"; the house rule for this batch is "never re-wrap,
  over-wide lines get the house cut", so it is cut after `uv-build>=0.12.13` (short enough that
  its `at the time of recording` tag fits beside it). s05-03:11–15 (79) are cut after their dots
  (the `[ nn%]` column dropped), s05-03:30 after `4.18s`, s05-01:3 after `with its tests`,
  s05-12:24–25 after their answers (`(0.47)`, `(score 3.00)`); line 23 shows the label column whole.
- Skipped lines between two shown ranges always get a "…" row (house picker rule), also where the
  script runs them together (s05-02 2/4, 4/8, 8/44, 44/46, 47/49; s05-03 before 11 and 15/29;
  s05-07 3/55; s05-11 6/22; s05-12 2/5, 5/22, 25/32).
- The one-liner is hand-folded at spaces inside its double quotes (bash drops a backslash-newline
  there; Python ignores the extra spaces), because the house fold would break it mid-token; the rows
  paste back as exactly walk.md:589 (asserted).
- The sequence bar packs a state of 2 tokens and three questions of 2 (no numbers on it); the grid is
  slide 72's six tokens. The "causal" fill of the forbidden block is an added beat for "the whole
  difference from a causal mask" (GREY note "causal mask").
- The want/built labels ("we meant", "built") and the beat-4 captions ("lines that ran", "what they
  produced", "necessary · never sufficient") are the narration's own words.
"""

import re

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer.scene import VoiceScene
from explainer import style as S

from explainer.devops import tag

from common import (CLOUD, ERR, INK, NARRATION, P_BABYKEV, PASS, SEG_SIX, TURN, T_BABYKEV, MaskGrid, attach,
                    beside, capture, code_panel, coverage_sweep, cut, excerpt, glyph_range, label, lref,
                    mask_rows, note, pause_and_ponder, pin, resize, ring, segment_ids, sequence_bar, shown_path,
                    substring, term, time_row, track, tracker, turn_row, type_cmd, walk)

SAY = NARRATION["S12"]
PT = 20                                  # terminal size: 72 characters a row
COLS = 72
SRC = "babykev-history/step-05-model.py"
FIRST, LAST = 137, 143                   # branch_mask's body
ONE_LINER_ROWS = [                       # walk.md:589, folded inside its double quotes
    P_BABYKEV + ' uv run python -c "from babykev.model import \\',
    "    branch_mask; m = branch_mask([0, 0, 1, 1, 2, 2], 'cpu')[0, 0] \\",
    "    == 0; print('\\n'.join(''.join('#' if x else '.' for x in r) \\",
    '    for r in m))"',
]


# ---------------------------------------------------------------- terminal helpers (S09/S11's)
def fit(lines):
    """Capture lines ready to print: every row must already fit (cuts are made explicitly)."""
    for x in lines:
        s = x if isinstance(x, str) else x[0]
        assert len(s) <= COLS, (len(s), s)
    return list(lines)


def room(scene, t, n: int, run_time: float = 0.3) -> None:
    """Make room for n new rows: the oldest rows fade where they are, then the rest slide up (the
    toolkit's scroll sails the old rows over the tracker)."""
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


def typ(scene, t, cmd: str, type_time: float | None = None, rows: list[str] | None = None):
    """type_cmd with room made first. `rows`: a hand fold (asserted to paste back as `cmd`)."""
    p = t.prompt + " "
    if rows is None:
        room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
        return type_cmd(scene, t, cmd, type_time)
    parts = [r[:-2] if r.endswith(" \\") else r for r in rows]
    assert all(r.endswith(" \\") for r in rows[:-1]) and all(len(r) <= COLS for r in rows), rows
    assert " ".join([parts[0]] + [q.lstrip(" ") for q in parts[1:]]) == p + cmd, rows
    room(scene, t, len(rows))
    t.fold = lambda text, first_prefix=0: list(rows)
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


def rows_of(line) -> list:
    return list(line.rows) if hasattr(line, "rows") else [line]


def find_in(line, sub: str) -> VGroup:
    """The glyphs of `sub` in a typed command, on whichever of its folded rows holds it."""
    for r in rows_of(line):
        if sub in r.text:
            return substring(r, sub)
    raise KeyError(f"{sub!r} is not on one row of {[r.text for r in rows_of(line)]}")


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


def dots_cut(s: str) -> str:
    """A pytest progress row cut after its dots (the padding and the `[ nn%]` column dropped)."""
    m = re.match(r"^(\S+ \.+)\s+\[", s)
    assert m, s
    return cut(s, m.group(1))


# ---------------------------------------------------------------- mask helpers
def empty_grid(cell: float = 0.45) -> MaskGrid:
    return MaskGrid(SEG_SIX, rows=["......"] * 6, cell=cell)


def lit(grid: MaskGrid, i: int, j: int, on: bool):
    """A painted copy of cell (i, j): what it becomes when row i prints '#' (on) or '.'."""
    return grid._paint(grid.cells[i][j].copy(), i, j, on)


def land(scene, grid: MaskGrid, printed, texts, start: int, run_time: float = 0.9):
    """The glyphs of printed rows fly into rows start.. of `grid`, whose cells light as they land.
    printed: terminal rows; texts: the six '#'/'.' characters of each (the glyphs, in order)."""
    flies, anims = VGroup(), []
    for k, (row, s) in enumerate(zip(printed, texts)):
        i = start + k
        assert len(s) == 6 and set(s) <= {"#", "."}, s
        gl = glyph_range(row, row.text.index(s), row.text.index(s) + 6)
        for j, ch in enumerate(s):
            f = gl[j].copy()
            flies.add(f)
            anims.append(Succession(f.animate(run_time=0.5).move_to(grid.cells[i][j]),
                                    AnimationGroup(FadeOut(f, run_time=0.2),
                                                   Transform(grid.cells[i][j], lit(grid, i, j, ch == "#"),
                                                             run_time=0.2))))
    scene.play(LaggedStart(*anims, lag_ratio=0.03), run_time=run_time)
    scene.remove(flies)
    for i in range(start, start + len(texts)):
        grid.allowed[i] = [ch == "#" for ch in texts[i - start]]


def attn(a, b, color=INK, angle: float = PI / 2, dashed: bool = False):
    """An attention arrow over the bar, from token a back to token b (curving up)."""
    arr = CurvedArrow(a.get_top() + UP * 0.08, b.get_top() + UP * 0.08, angle=angle, color=color,
                      stroke_width=3, tip_length=0.16)
    mid = arr.point_from_proportion(0.5)
    if dashed:
        body = DashedVMobject(VMobject().set_points(arr.get_points()), num_dashes=10, dashed_ratio=0.55)
        body.set_stroke(color, 3)
        arr = VGroup(body, arr.tip.copy())
    arr.mid = mid
    return arr


def bracket(a_row, b_row, x: float, color=TURN) -> VMobject:
    """A YELLOW bracket from the end of row a to the end of row b, standing at x."""
    ya, yb = a_row.strut.get_center()[1], b_row.strut.get_center()[1]
    xa, xb = a_row.glyphs.get_right()[0] + 0.15, b_row.glyphs.get_right()[0] + 0.15
    p = VMobject().set_points_as_corners([[xa, ya, 0], [x, ya, 0], [x, yb, 0], [xb, yb, 0]])
    return p.set_stroke(color, 3)


class GreenButWrong(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        sw, setup, test = capture("babykev/s05-01"), capture("babykev/s05-02"), capture("babykev/s05-03")
        mask, line140, cmp_ = capture("babykev/s05-04"), capture("babykev/s05-05"), capture("babykev/s05-06")
        ty, check, smoke = capture("babykev/s05-07"), capture("babykev/s05-11"), capture("babykev/s05-12")
        assert sw.cmd == "git switch --detach step-05" and setup.cmd == walk(462)[2:] and test.cmd == walk(530)[2:]
        assert mask.cmd == walk(589)[2:] and line140.cmd == walk(590)[2:] and cmp_.cmd == walk(594)[2:]
        assert ty.cmd == walk(565)[2:] and check.cmd == walk(550)[2:] and smoke.cmd == walk(561)[2:]
        built_rows = mask.at((2, 7))
        assert built_rows == mask_rows(SEG_SIX, "ones"), built_rows
        assert [r.split()[0] for r in cmp_.at((8, 13))] == mask_rows(SEG_SIX, "want")
        assert [r.split()[1] for r in cmp_.at((8, 13))] == built_rows
        assert line140.line(2) == excerpt(SRC, 140, 140)

        # ========================================================== 0. step-05: setup, then all green
        tr = tracker("E", 5)
        ref = lref("53–55, 72–75")
        t = term(P_BABYKEV, rows=14, title=T_BABYKEV, size=PT)
        warn = cut(setup.line(4), "uv-build>=0.12.13")
        setup_lines = setup.at(2, "…") + [warn] + setup.at("…", 8, "…", 44, "…", (46, 47), "…", 49)
        test_lines = ["…"] + [dots_cut(test.line(n)) for n in range(11, 16)] + \
            ["…", test.line(29), cut(test.line(30), "4.18s")]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(t, shift=UP * 0.2), run_time=0.7)
            self.play(track(tr, 6), run_time=0.5)
            typ(self, t, sw.cmd, type_time=0.6)
            out(self, t, [cut(sw.line(3), "with its tests")], run_time=0.3)
            vo.wait_until("the setup recipe")
            s_ln = typ(self, t, setup.cmd, type_time=0.4)
            s_out = out(self, t, setup_lines, run_time=0.9, lag=0.05)
            l4, l8, l44 = s_out[2], s_out[4], s_out[6]
            assert l8.text.startswith("Installed 38") and "torch==" in l44.text, (l8.text, l44.text)
            vo.wait_until("38 packages")
            r38 = ring(substring(l8, "Installed 38 packages"), INK, buff=0.05)
            self.play(Create(r38), Indicate(substring(l8, "38"), color=INK, scale_factor=1.3), run_time=0.6)
            attach(self, l8, r38)
            vo.wait_until("including torch 2.14.1")
            torch = substring(l44, "torch==2.14.1+cpu")
            r44 = ring(torch, INK, buff=0.05)
            self.play(Create(r44), Indicate(torch, color=INK, scale_factor=1.12), run_time=0.6)
            attach(self, l44, r44)
            vo.wait_until("for the CPU")
            self.play(Indicate(substring(l44, "+cpu"), color=INK, scale_factor=1.3), run_time=0.5)
            vo.wait_until("at the time of recording")
            t44, t4 = beside(time_row(), l44), beside(time_row(), l4, buff=0.2)
            assert t4.get_right()[0] <= 6.55, t4.get_right()
            self.play(FadeIn(t44, shift=LEFT * 0.1), FadeIn(t4, shift=LEFT * 0.1), run_time=0.5)
            attach(self, l44, t44)
            attach(self, l4, t4)
            vo.wait_until("Then just test")
            resize(self, t, 14, keep=[s_ln, l44], run_time=0.5)
            j_ln = typ(self, t, test.cmd, type_time=0.4)
            j_out = out(self, t, test_lines, run_time=0.8, lag=0.05)
            dots = [substring(j_out[k], j_out[k].text.split()[1].rstrip("…")) for k in range(1, 6)]
            total, passed = j_out[7], j_out[8]
            vo.wait_until("92 passed")
            self.play(substring(passed, "92 passed").animate.set_color(PASS), run_time=0.3)
            self.play(Indicate(substring(passed, "92 passed"), color=PASS, scale_factor=1.15), run_time=0.6)
            vo.wait_until("coverage 94 percent")
            self.play(total.animate.set_color(PASS), run_time=0.3)
            self.play(Indicate(substring(total, "94%"), color=PASS, scale_factor=1.25), run_time=0.6)
            vo.wait_until("all green")
            self.play(LaggedStart(*[d.animate.set_color(PASS) for d in dots], lag_ratio=0.15), run_time=0.7)
            vo.wait_until("Pause and run both.")
            k1, y1 = tag_on(self, s_ln, turn_row)
            k2, y2 = tag_on(self, j_ln, turn_row)
            self.play(*flash(y1, TURN), *flash(y2, TURN), run_time=0.8)

        # ========================================================== 1. the model in one picture
        seg8 = segment_ids(2, [2, 2, 2])
        bar = sequence_bar(seg8, cell=0.7)
        bar.move_to([-3.35, 0.55, 0])
        toks = bar.tokens
        grid = MaskGrid(SEG_SIX, "want", cell=0.5).move_to([3.55, 0.75, 0])
        rule = VGroup(label("a question sees the state and itself —", 22, S.GREY),
                      label("never a sibling", 22, S.GREY)).arrange(DOWN, buff=0.12)
        rule.next_to(grid, DOWN, buff=0.3)
        to_state = attn(toks[5], toks[0], INK, angle=PI / 2)
        to_self = attn(toks[5], toks[4], INK, angle=PI / 1.4)
        sneak = attn(toks[5], toks[3], S.GREY, angle=PI / 1.6, dashed=True)
        block = VGroup(*[grid.cells[i][j] for i in (4, 5) for j in (2, 3)])
        ybox = Rectangle(width=block.width + 0.1, height=block.height + 0.1, stroke_color=TURN,
                         stroke_width=4).move_to(block)
        diff_cap = label("this cell is the whole difference", 22, TURN)
        diff_cap.move_to([grid.get_left()[0] - 0.25 - diff_cap.width / 2, block.get_center()[1] - 0.95, 0])
        causal = note("causal mask", S.GREY, 22).next_to(diff_cap, DOWN, buff=0.2).align_to(diff_cap, RIGHT)

        with self.voiceover(SAY[1]) as vo:
            gone = VGroup(t, y1, y2)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            for m in list(t.lines):
                t.lines.remove(m)
            vo.wait_until("A request packs")
            self.play(LaggedStart(*[FadeIn(k, shift=DOWN * 0.3) for k in toks], lag_ratio=0.12), run_time=1.0)
            vo.wait_until("several questions")
            self.play(LaggedStart(*[FadeIn(lb, shift=UP * 0.1) for lb in bar.labels], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("A mask enforces one rule")
            self.play(FadeIn(VGroup(grid.col_labels, grid.row_labels, grid.band)),
                      LaggedStart(*[FadeIn(c, scale=0.6) for c in grid.grid], lag_ratio=0.02), run_time=1.2)
            self.remove(grid.col_labels, grid.row_labels, grid.band, *grid.grid)
            self.add(grid)                       # one piece from now on (it is transformed later)
            vo.wait_until("a question may see the state and itself")
            row6 = VGroup(*[grid.cells[5][j] for j in (0, 1, 4, 5)])
            self.play(Create(to_state), Create(to_self), FadeIn(rule[0], shift=UP * 0.1), run_time=0.8)
            self.play(Indicate(row6, color=INK, scale_factor=1.08),
                      Indicate(VGroup(toks[0], toks[1], toks[4], toks[5]), color=INK, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("never a sibling question")
            self.play(FadeIn(rule[1], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Questions must be answered independently")
            self.play(FadeOut(VGroup(to_state, to_self)), run_time=0.3)
            self.remove(to_state, to_self)
            self.play(Create(sneak), run_time=0.8)
            vo.wait_until("a peek would leak")
            xmark = VGroup(Line(UL, DR), Line(DL, UR)).scale(0.22).set_stroke(ERR, 6)
            xmark.move_to(sneak.mid)
            self.play(Create(xmark), sneak.animate.set_color(ERR), run_time=0.5)
            self.play(Indicate(VGroup(toks[2], toks[3]), color=ERR, scale_factor=1.06), run_time=0.6)
            vo.wait_until("That one forbidden cell")
            self.play(Create(ybox), FadeIn(diff_cap, shift=RIGHT * 0.2), run_time=0.7)
            self.play(ybox.animate(rate_func=there_and_back).set_stroke(width=8), run_time=0.6)
            vo.wait_until("from a causal mask")
            self.play(grid.retarget("ones", run_time=0.5), FadeIn(causal, shift=UP * 0.1))
            self.wait(0.6)
            self.play(grid.retarget("want", run_time=0.5), FadeOut(causal))
            self.remove(causal)

        # ========================================================== 2. the mask the code builds
        s = term(P_BABYKEV, rows=4, title=T_BABYKEV, size=PT)
        g2 = empty_grid().move_to([0, 0.95, 0])
        assert g2.get_bottom()[1] > s.box.get_top()[1] + 0.15, (g2.get_bottom(), s.box.get_top())

        with self.voiceover(SAY[2]) as vo:
            pic = VGroup(bar, sneak, xmark, rule, diff_cap, ybox)
            self.play(FadeOut(pic), run_time=0.5)
            self.remove(pic, *pic.get_family())
            self.play(ReplacementTransform(grid, g2), FadeIn(s, shift=UP * 0.2), run_time=0.8)
            grid = g2
            vo.wait_until("The walk prints the mask")
            o_ln = typ(self, s, mask.cmd, type_time=2.0, rows=ONE_LINER_ROWS)
            vo.wait_until("for two state tokens")
            seg_glyphs = find_in(o_ln, "[0, 0, 1, 1, 2, 2]")
            r_seg = ring(seg_glyphs, INK, buff=0.05)
            self.play(Create(r_seg), run_time=0.4)
            self.play(Indicate(seg_glyphs, color=INK, scale_factor=1.1),
                      LaggedStart(*[Indicate(b, color=INK, scale_factor=1.12) for b in grid.band], lag_ratio=0.3),
                      run_time=0.9)
            attach(self, rows_of(o_ln)[1], r_seg)
            vo.wait_until("pause and print yours")
            ky, yy = tag_on(self, o_ln, turn_row)
            self.play(*flash(yy, TURN), run_time=0.7)
            p1 = out(self, s, built_rows[:3], run_time=0.4)
            land(self, grid, p1, built_rows[:3], 0)
            p2 = out(self, s, built_rows[3:], run_time=0.4)
            land(self, grid, p2, built_rows[3:], 3)
            vo.wait_until("Rows 5 and 6")
            self.play(p2[1].animate.set_color(ERR), p2[2].animate.set_color(ERR), grid.flash_rows([4, 5]),
                      run_time=0.8)
            vo.wait_until("including question 1")
            wrong = [(i, j) for i in (4, 5) for j in (2, 3)]
            assert sorted(wrong) == sorted(MaskGrid(SEG_SIX, rows=built_rows).diff("want")), wrong
            boxes = VGroup(*[grid.cell_box(i, j, ERR) for i, j in wrong])
            self.play(LaggedStart(*[Create(b) for b in boxes], lag_ratio=0.15), run_time=0.7)
            vo.wait_until("The cause is one line")
            typ(self, s, line140.cmd, type_time=0.6)
            c_row = out(self, s, [line140.line(2)], run_time=0.3)[0]
            vo.wait_until("torch dot ones like")
            ones = substring(c_row, "torch.ones_like")
            self.play(ones.animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(ones, color=ERR, scale_factor=1.15), run_time=0.6)
            vo.wait_until("marks every pair of tokens")
            lower = VGroup(*[grid.cells[i][j] for i in range(6) for j in range(i + 1)])
            self.play(Indicate(substring(c_row, "same"), color=INK, scale_factor=1.2),
                      Indicate(lower, color=INK, scale_factor=1.04), run_time=0.8)

        # ========================================================== 3. a checker prints WRONG; ponder
        built = VGroup(grid, boxes)
        want = empty_grid().move_to([-2.45, 0.95, 0])
        meant_l = label("we meant", 24, INK).next_to(want, LEFT, buff=0.45)
        built_l = label("built", 24, INK)
        study = tag("full script: study guide", S.GREY)
        nothing = note("nothing in just check runs this", S.GREY, 22)
        cmp_rows = cmp_.at((8, 13))

        with self.voiceover(SAY[3]) as vo:
            wipe(self, s)
            resize(self, s, 3, keep=0, run_time=0.5)
            study.move_to([6.5 - study.width / 2, s.box.get_top()[1] + 0.08 + study.height / 2, 0])
            nothing.move_to([-6.5 + nothing.width / 2, study.get_center()[1], 0])
            self.play(built.animate.move_to([2.45, 0.95, 0]), FadeIn(want), run_time=0.7)
            built_l.next_to(built, RIGHT, buff=0.45)
            self.play(FadeIn(meant_l, shift=RIGHT * 0.15), FadeIn(built_l, shift=LEFT * 0.15), run_time=0.5)
            assert want.get_bottom()[1] > study.get_top()[1] + 0.05, (want.get_bottom(), study.get_top())
            assert nothing.get_right()[0] < study.get_left()[0] - 0.3
            vo.wait_until("A checker script compares")
            typ(self, s, cmp_.cmd, type_time=0.6)
            out(self, s, ["…"], run_time=0.2)
            self.play(FadeIn(study, shift=UP * 0.1), run_time=0.4)
            q1 = out(self, s, cmp_rows[:3], run_time=0.4)
            land(self, want, q1, [r.split()[0] for r in cmp_rows[:3]], 0)
            q2 = out(self, s, cmp_rows[3:], run_time=0.4)
            land(self, want, q2, [r.split()[0] for r in cmp_rows[3:]], 3)
            vo.wait_until("prints WRONG")
            w12, w13 = substring(q2[1], "WRONG"), substring(q2[2], "WRONG")
            self.play(w12.animate.set_color(ERR), w13.animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(w12, color=ERR, scale_factor=1.2), Indicate(w13, color=ERR, scale_factor=1.2),
                      grid.flash_rows([4, 5]), run_time=0.8)
            vo.wait_until("But nothing in just check runs it")
            self.play(FadeIn(nothing, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a printout you read by eye")
            self.play(Indicate(VGroup(*q2), color=INK, scale_factor=1.04), run_time=0.8)
            vo.wait_until("Something to ponder")
            self.play(Indicate(nothing, color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Can any coverage number")
            self.play(LaggedStart(*[b.animate(rate_func=there_and_back).set_stroke(width=8) for b in boxes],
                                  lag_ratio=0.1), run_time=0.9)
        ponder = pause_and_ponder(self, "Every line of branch_mask ran.\nCoverage reads 94%.\n"
                                        "Can any coverage number catch this bug?", seconds=8)

        # ========================================================== 4. coverage counts lines that ran
        lines = excerpt(SRC, FIRST, LAST).split("\n")
        lines[139 - FIRST] = cut(lines[139 - FIRST], "torch.ones(n, n,")
        lines[143 - FIRST] = cut(lines[143 - FIRST], "device=device)")
        panel = code_panel("\n".join(lines), shown_path(SRC), FIRST, "python", font_size=PT)
        panel.move_to([0, 0, 0]).align_to([-6.5, 0, 0], LEFT).align_to([0, 2.75, 0], UP)
        g_at = [4.95, 0.95, 0]
        ran = label("lines that ran", 24, PASS)
        made = label("what they produced", 24, ERR)
        verdict = label("necessary · never sufficient", 26, INK)

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(ponder, s, want, meant_l, built_l, study, nothing)
            self.play(FadeOut(gone), run_time=0.6)
            self.remove(gone, *gone.get_family())
            for m in list(s.lines):
                s.lines.remove(m)
            self.play(built.animate.move_to(g_at), FadeIn(panel, shift=RIGHT * 0.2), run_time=0.7)
            assert panel.get_right()[0] < built.get_left()[0] - 0.2, (panel.get_right(), built.get_left())
            ran.next_to(panel, DOWN, buff=0.35)
            made.next_to(built, DOWN, buff=0.35)
            verdict.move_to([0, min(ran.get_bottom()[1], made.get_bottom()[1]) - 0.75, 0])
            vo.wait_until("Coverage counts lines that ran")
            bars, sweep = coverage_sweep(panel, run_time=1.6)
            self.play(sweep, FadeIn(ran, shift=UP * 0.15))
            vo.wait_until("never whether anyone checked")
            self.play(FadeIn(made, shift=UP * 0.15),
                      LaggedStart(*[b.animate(rate_func=there_and_back).set_stroke(width=8) for b in boxes],
                                  lag_ratio=0.1), run_time=0.9)
            self.play(grid.flash_rows([4, 5]), run_time=0.8)
            vo.wait_until("Necessary, and never sufficient.")
            self.play(FadeIn(verdict, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(verdict, color=INK, scale_factor=1.08), run_time=0.8)

        # ========================================================== 5. ty: green and blind
        t = term(P_BABYKEV, rows=14, title=T_BABYKEV, size=PT)

        with self.voiceover(SAY[5]) as vo:
            gone = VGroup(panel, bars, built, ran, made, verdict)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("the type checker")
            typ(self, t, ty.cmd, type_time=0.5)
            vo.wait_until("Running ty finds 6 diagnostics")
            y_out = out(self, t, ty.at((2, 3), "…", 55), run_time=0.6)
            found = y_out[3]
            self.play(found.animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(found, color=ERR, scale_factor=1.12), run_time=0.6)
            vo.wait_until("yet just check is green")
            typ(self, t, check.cmd, type_time=0.4)
            c_out = out(self, t, check.at((2, 6), "…", 22, 23), run_time=0.8, lag=0.06)
            req, p92 = c_out[6], c_out[7]
            self.play(substring(req, "Required test coverage of 90% reached").animate.set_color(PASS),
                      substring(p92, "92 passed").animate.set_color(PASS), run_time=0.5)
            vo.wait_until("types are not in the gate yet")
            br = bracket(found, p92, max(r.glyphs.get_right()[0] for r in c_out) + 0.4)
            self.play(Create(br), run_time=0.7)
            self.play(Indicate(found, color=ERR, scale_factor=1.1),
                      Indicate(substring(p92, "92 passed"), color=PASS, scale_factor=1.15), run_time=0.7)
            vo.wait_until("a check outside the gate protects nobody")
            self.play(br.animate(rate_func=there_and_back).set_stroke(width=7), run_time=0.8)

        # ========================================================== 6. the smoke on the real model
        smoke_lines = smoke.at(2, "…", 5, "…", (22, 23)) + \
            [cut(smoke.line(24), "(0.47)"), cut(smoke.line(25), "(score 3.00)"), "…", smoke.line(32),
             (smoke.line(33), S.GREY)]

        with self.voiceover(SAY[6]) as vo:
            wipe(self, t, br)
            vo.wait_until("the smoke on the real model")
            m_ln = typ(self, t, smoke.cmd, type_time=0.5)
            m_out = out(self, t, smoke_lines, run_time=0.9, lag=0.06)
            l2, l5, l32, l33 = m_out[0], m_out[2], m_out[9], m_out[10]
            vo.wait_until("half a billion parameters")
            r5 = ring(substring(l5, "503M parameters"), INK, buff=0.05)
            self.play(Create(r5), Indicate(substring(l5, "503M"), color=INK, scale_factor=1.25), run_time=0.7)
            attach(self, l5, r5)
            vo.wait_until("downloaded once from the Hugging Face Hub")
            hub = substring(l2, "Qwen/Qwen2.5-0.5B")
            r2 = ring(hub, CLOUD, buff=0.05)
            self.play(Create(r2), Indicate(hub, color=CLOUD, scale_factor=1.1), run_time=0.7)
            attach(self, l2, r2)
            vo.wait_until("answering 15 cheese questions on CPU")
            self.play(LaggedStart(*[Indicate(m_out[k], color=INK, scale_factor=1.04) for k in (4, 5, 6, 7)],
                                  lag_ratio=0.2),
                      Indicate(substring(l2, "on cpu"), color=INK, scale_factor=1.2), run_time=1.0)
            vo.wait_until("pause and run it")
            km, ym = tag_on(self, m_ln, turn_row)
            self.play(*flash(ym, TURN), run_time=0.7)
            vo.wait_until("6 of 15 right.")
            right = substring(l32, "6 of 15 right")
            self.play(right.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(right, color=TURN, scale_factor=1.2), run_time=0.7)
            vo.wait_until("Nothing is trained")
            self.play(Indicate(l33, color=S.GREY, scale_factor=1.06), run_time=0.8)
            vo.wait_until("hold that number")
            r32 = ring(right, TURN, buff=0.06)
            self.play(Create(r32), run_time=0.5)
            self.play(Indicate(right, color=TURN, scale_factor=1.15), run_time=0.7)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
