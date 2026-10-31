"""S06 · Prepare: a failure that surfaces late (README "Dataset › Prepare", step 1, and one extra).
Lecture: 5 (the tag shows in beat 6, with the lecture's term in the file name).

Beats (script.md "## S06", one voiceover block each):
 0  TRACKER DsPrep 1. Full-width TEAL container terminal (12 rows, app@6f5113cdb660:/app$); GREY chip
    in the top band "right after the failed generate, as a student would". `python cli.py --prepare`
    -> dataset-creator/07 lines 2–6, …, 15–17, …, 23 (11 rows; line 2 cut with …): "Number of
    errors: 0" flashes, `Shape: (0, 0)` lights YELLOW, line 15 (`line 243, in prepare`) and line 23
    `KeyError: 'question'` print RED; "line 243" flashes.
 1  The terminal shrinks to a 3-row strip (line 15, the …, the KeyError). Above it
    CODE(dataset-creator/cli.py: 184–186, 188, 198–201, folded, 20 pt). Line 184 (the loop), the
    try and the call (186, 188) light; on "the except on line 200" `except Exception` lights and a
    GREY net is drawn under the call, beside line 200 (linked to it). Five RED sparks (one per
    batch) fly out of line 188's call and drop into the net; line 201's print pulses RED as each one
    lands. In the right margin the pile (data/ · five dashed batch slots) stays empty: "0 files";
    a calm GREY "exit 0".
 2  The strip and the code fade; the net (its `except Exception` label pulled out of line 200) and
    the empty pile move small to the lower left. CODE(dataset-creator/cli.py: 232–233, 235,
    241–243, folded, 20 pt) at the top: a GREY table chip "0 rows · 0 columns" slides out of the
    empty pile to line 235 while 232's `output_pairs_df` lights; on line 243
    `output_pairs_df["question"]` lights RED and a RED `KeyError: 'question'` stamp lands beside it.
    A GREY arrow from the net to the stamp: "the error was there all along · the net moved it".
    YELLOW caption "read the lines, not the exit code".
 3  The panels fade. V2's laptop (~/AC215 … secrets/ with the dashed GOLD key outline), tag
    `illustration`; a GREEN fix card under it: "key → `~/AC215/secrets/llm-service-account.json`
    (exact name)" and "check: `ls -la /secrets`". The outline turns into the solid GOLD key; on
    "check" the dataset-creator container and its mounts appear and the key's mount into /secrets
    lights.
 4  TRACKER DsPrep 1 · extra. The second laptop terminal slides in (laptop · second terminal,
    9 rows, …/dataset-creator$; GREY `extra` and `scripted` on its title bar). It types
    `cp ~/scripted/cheese_qa_*.txt data/; ls -la data` -> laptop/13 line 2 and lines 5–10
    (names + sizes); the five cheese_qa_ rows inside a BLUE dashed outline; line 10's
    `1  instruct-dataset.csv` RED-ringed with the GREY note "left by the failed run". Under the
    terminal a GREY card "hand-written in the shape Gemini returns · 20 pairs (Gemini: ≈ 100)" and
    a GREY chip "not in the repo · with a key, generate writes these files for you".
 5  The second terminal slides away; the container terminal returns (13 rows, GREY `scripted` on
    its title bar) and types `python cli.py --prepare` again -> dataset-creator/09 lines 4–9, 11,
    13–17 (12 rows; 13–17 cut at 65 characters); `Shape: (19, 2)` lights YELLOW. The terminal
    shrinks to 7 rows (line 11 and the five rows). Above: the excerpt chip
    `dataset-creator/cli.py · line 233 (excerpt)` and a row of 20 BLUE dashed bricks numbered by
    question (1 … 19, 1): a YELLOW arc joins the last to the first, the last drops out with a RED ✗,
    "20 scripted pairs" ->
    "19 rows". The openers in lines 13–17 light BLUE.
 6  V4 station 1: a conveyor (only station 1 labelled, `instruct-dataset.csv` GREEN); the first
    brick rides onto it and becomes a GREEN CSV-row card `question,answer`; "instruct" lights;
    lecture tag "Lecture 8 · slide 5" top right and a GREY chip "instruction dataset · slide 5".
    Then the GREY "your turn" card with ▶: `python cli.py --generate` · `python cli.py --prepare`,
    GOLD "generate: billed · cents", GREEN "prepare: free". 2 s hold. Everything fades to an
    empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    ArcBetweenPoints,
    Create,
    CurvedArrow,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    ReplacementTransform,
    TransformFromCopy,
    VGroup,
)

from common import *  # noqa: F401,F403
from common import _mixed_row
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ the real captures and sources
CLI = "dataset-creator/cli.py"
NODATA = capture("dataset-creator/07")
assert NODATA.cmd == "python cli.py --prepare" and NODATA.exit == 1, (NODATA.cmd, NODATA.exit)
assert NODATA.line(4) == "Number of errors: 0" and NODATA.line(6) == "Shape: (0, 0)", NODATA.lines
assert "line 243, in prepare" in NODATA.line(15) and NODATA.line(23) == "KeyError: 'question'"
CP = capture("laptop/13")
assert CP.cmd == "cp ~/scripted/cheese_qa_*.txt data/; ls -la data" and CP.line(2) == "total 24"
CP_ROWS = CP.names_sizes((5, 10))
assert CP_ROWS[-1] == "1  instruct-dataset.csv" and all("cheese_qa_" in r for r in CP_ROWS[:5]), CP_ROWS
PREP = capture("dataset-creator/09")
assert PREP.cmd == NODATA.cmd and PREP.exit == 0 and PREP.line(11) == "Shape: (19, 2)", PREP.lines
assert all(PREP.line(n).startswith("Processing file: data/cheese_qa_") for n in range(4, 9))
assert PREP.line(9) == "Number of errors: 0"
ANS_COL = 54                                  # the answer column of pandas' head table (lines 13–17)
assert all(PREP.line(n)[ANS_COL - 2:ANS_COL] == "  " and PREP.line(n)[ANS_COL] != " " for n in range(13, 18))
GEN_CMD = capture("dataset-creator/05").cmd
assert GEN_CMD == "python cli.py --generate"
L233 = source_line(CLI, 233)
DEDUP = 'output_pairs_df.drop_duplicates(subset=["question"], inplace=True)'
assert DEDUP in L233
assert "except Exception" in source_line(CLI, 200) and "Error occurred" in source_line(CLI, 201)
assert "generate_content(" in source_line(CLI, 188) and source_line(CLI, 186).strip() == "try:"
assert 'output_pairs_df["question"]' in source_line(CLI, 243)
assert "output_pairs_df = pd.DataFrame(output_pairs)" in source_line(CLI, 232)
PAIRS = scripted_pairs()
assert len(PAIRS) == 20 and PAIRS[-1]["question"] == PAIRS[0]["question"], len(PAIRS)
assert len({p["question"] for p in PAIRS}) == 19

# ------------------------------------------------------------------ layout
TOP_Y = 2.87                     # top of a panel under the tracker


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


def inside(m):
    assert m.get_left()[0] > -6.6 and m.get_right()[0] < 6.6, (m.get_left(), m.get_right())
    assert m.get_bottom()[1] > -3.6 and m.get_top()[1] < 3.6, (m.get_bottom(), m.get_top())


def text_part(t, sub: str) -> VGroup:
    """The glyphs of `sub` in a Text (Text keeps no glyphs for spaces)."""
    s, needle = t.text, sub.replace(" ", "")
    i = s.find(needle)
    if i < 0:
        raise ValueError(f"{sub!r} not in {s!r}")
    return VGroup(*t.submobjects[i:i + len(needle)])


def code_row(p, n: int, k: int = 0):
    return p.code.code_lines[p.rows_of(n)[k]]


def make_net(w: float = 2.2, h: float = 0.3) -> VGroup:
    """V3's net: a GREY mesh under a rim (catches whatever falls in). .rim .mesh"""
    mesh = VGroup()
    n = max(4, int(round(w / 0.4)))
    step = w / n
    for k in range(n):
        x = -w / 2 + k * step
        mesh.add(Line([x, h / 2, 0], [x + step, -h / 2, 0], color=S.GREY, stroke_width=1.8))
        mesh.add(Line([x + step, h / 2, 0], [x, -h / 2, 0], color=S.GREY, stroke_width=1.8))
    rim = Line([-w / 2 - 0.08, h / 2 + 0.02, 0], [w / 2 + 0.08, h / 2 + 0.02, 0], color=S.GREY, stroke_width=3)
    g = VGroup(mesh, rim)
    g.mesh, g.rim = mesh, rim
    return g


def pile_slots(n: int = 5, w: float = 1.3, h: float = 0.3, direction=DOWN, buff: float = 0.1) -> VGroup:
    """The five empty batch slots (GREY dashed: nothing was written), numbered 0-4."""
    g = VGroup()
    for k in range(n):
        g.add(box(w, h, S.GREY, fill_opacity=0.0, radius=0.06, dashed=True))
    g.arrange(direction, buff=buff)
    return g


class LateFailure(VoiceScene):
    def construct(self):
        assert len(SAY) == 7, len(SAY)

        # ========================================================== 0 · python cli.py --prepare, right after
        tr = tracker("DsPrep", 1)
        t = term(P_CTR_DC, rows=12, container="dc")
        chip0 = top_chip("right after the failed generate, as a student would", color=S.GREY)
        assert chip0.get_left()[0] > tr.get_right()[0] + 0.2 and chip0.get_bottom()[1] > t.box.get_top()[1] + 0.05
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.2), run_time=0.7)
            self.play(flash(tr.caption, TURN, 1.12), run_time=0.6)      # "step 1 of the prepare section"
            bare_prompt(self, t)
            self.play(FadeIn(chip0, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("as a student would")
            self.play(flash(chip0, S.GREY, 1.06), run_time=0.7)
            vo.wait_until("python cli.py dash dash prepare")
            type_cmd(self, t, NODATA.cmd, 0.7)
            vo.wait_until("Zero errors")
            o0 = show(self, t, NODATA, (2, 6), run_time=0.5)
            r4, r6 = o0[2], o0[4]
            self.play(flash(r4, TURN, 1.08), run_time=0.6)
            vo.wait_until("a shape of zero")
            self.play(r6.animate.set_color(TURN), run_time=0.3)
            self.play(flash(r6, TURN, 1.15), run_time=0.6)
            vo.wait_until("and then a crash")
            o1 = t.print(self, NODATA.out("…", (15, 17), "…") + [(NODATA.line(23), ERR)], run_time=0.6)
            r15, rdots, r23 = o1[1], o1[4], o1[5]
            self.play(r15.animate.set_color(ERR), run_time=0.3)
            vo.wait_until("key error, question")
            self.play(flash(r23, ERR, 1.12), run_time=0.6)
            vo.wait_until("from line 243")
            self.play(flash(substring(r15, "line 243"), TURN, 1.25), run_time=0.7)
        assert len(t.lines) == 12, len(t.lines)

        # ========================================================== 1 · the net: generate swallowed every error
        p1 = src_panel(CLI, [(184, 186), 188, (198, 201)], size=20)
        place(p1, left=-6.45, top=TOP_Y)
        assert p1.get_bottom()[1] > STRIP_TOP + 0.08, p1.get_bottom()
        row188, row200, row201 = code_row(p1, 188), code_row(p1, 200), code_row(p1, 201)
        call = p1.span(188, "generate_content")
        exc = p1.span(200, "except Exception")
        net_cx = max(code_row(p1, 198).get_right()[0] + 1.35, call.get_center()[0])
        net = make_net(2.2, 0.28).move_to([net_cx, row200.get_center()[1] + 0.03, 0])
        assert net.get_left()[0] > row200.get_right()[0] + 0.6, (net.get_left(), row200.get_right())
        assert net.get_right()[0] < p1.get_right()[0] - 0.08
        for n in (198, 199):
            assert code_row(p1, n).get_right()[0] < net.get_left()[0] - 0.1, n
        link = Line(row200.get_right() + RIGHT * 0.15, net.get_left() + LEFT * 0.12, color=S.GREY, stroke_width=2)
        # the pile in the right margin: data/ and five empty batch slots
        mx = (p1.get_right()[0] + 6.45) / 2
        dlab = mono("data/", CAPTION, OWN)
        slots = pile_slots(5, w=1.25, h=0.3)
        zero = label("0 files", CAPTION, S.GREY)
        pile = VGroup(dlab, slots, zero).arrange(DOWN, buff=0.18)
        place(pile, cx=mx, top=TOP_Y - 0.15)
        ex0 = label("exit 0", CAPTION, S.GREY).next_to(pile, DOWN, buff=0.35)
        assert pile.get_left()[0] > p1.get_right()[0] + 0.08 and pile.get_right()[0] < 6.45, pile.get_left()
        assert ex0.get_bottom()[1] > STRIP_TOP + 0.1
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(chip0), run_time=0.3)
            resize(self, t, 3, keep=[r15, rdots, r23], run_time=0.6)
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("In generate")
            b184 = p1.bar(184, TURN)
            self.play(FadeIn(b184), run_time=0.4)
            vo.wait_until("each batch runs inside")
            b186, b188 = p1.bar(186, TURN), p1.bar(188, TURN)
            self.play(FadeIn(b186), FadeIn(b188), run_time=0.4)
            self.play(FadeIn(pile, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and the except on line 200")
            b200 = p1.bar(200, S.GREY, 0.22)
            self.play(FadeIn(b200), exc.animate.set_color(INK), run_time=0.4)
            self.play(Create(net.rim), Create(net.mesh), Create(link), run_time=0.6)
            vo.wait_until("catches any exception")
            b201 = p1.bar(201, ERR, 0.25)
            caught = VGroup()
            for i in range(5):
                s = spark().move_to(call.get_bottom() + DOWN * 0.08 + RIGHT * (i - 2) * 0.12)
                tgt = net.get_center() + RIGHT * (i - 2) * 0.42 + UP * 0.02
                self.play(FadeIn(s, scale=0.5), run_time=0.12)
                self.play(s.animate.move_to(tgt), run_time=0.32)
                caught.add(s)
                self.play(FadeIn(b201, rate_func=lambda x: 1 - abs(2 * x - 1)), run_time=0.22)
            self.remove(b201)
            vo.wait_until("So no file was written")
            self.play(flash(slots, S.GREY, 1.06), run_time=0.6)
            self.play(flash(zero, TURN, 1.15), run_time=0.6)
            vo.wait_until("and the command still exited")
            self.play(FadeIn(ex0, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 2 · prepare met the empty table one command later
        p2 = src_panel(CLI, [(232, 233), 235, (241, 243)], size=20)
        place(p2, cx=0, top=TOP_Y)
        r232, r235, r243 = code_row(p2, 232), code_row(p2, 235), code_row(p2, 243)
        # the net (with its label pulled out of line 200) and the empty pile, small at the lower left
        net2 = make_net(2.2, 0.28)
        nlab = mono("except Exception", CAPTION, S.GREY)
        netg = VGroup(nlab, net2).arrange(DOWN, buff=0.16)
        place(netg, left=-6.3, top=p2.get_bottom()[1] - 0.3)
        caught2 = VGroup(*[s.copy().move_to(net2.get_center() + RIGHT * (i - 2) * 0.42) for i, s in enumerate(caught)])
        slots2 = pile_slots(5, w=0.42, h=0.26, direction=RIGHT, buff=0.08)
        dlab2 = mono("data/", CAPTION, OWN)
        zero2 = label("0 files", CAPTION, S.GREY)
        pile2 = VGroup(dlab2, slots2, zero2).arrange(RIGHT, buff=0.2)
        place(pile2, left=-6.3, top=netg.get_bottom()[1] - 0.35)
        ex2 = label("exit 0", CAPTION, S.GREY).next_to(pile2, RIGHT, buff=0.4)
        tbl = VGroup(box(0.5, 0.36, S.GREY, fill_opacity=0.0, radius=0.04, dashed=True),
                     label("0 rows · 0 columns", CAPTION, S.GREY)).arrange(RIGHT, buff=0.15)
        place(tbl, left=r235.get_right()[0] + 0.5, cy=r235.get_center()[1])
        assert tbl.get_right()[0] < p2.get_right()[0] - 0.1, tbl.get_right()
        st = stamp("KeyError: 'question'", ERR, angle=0.05)
        place(st, left=r243.get_right()[0] + 0.5, cy=r243.get_center()[1] + 0.05)
        assert st.get_right()[0] < 6.45 and st.get_bottom()[1] > p2.get_bottom()[1] - 0.3, st.get_corner(DOWN + RIGHT)
        arr = Arrow_(net2.get_right() + RIGHT * 0.15, st.get_bottom() + DOWN * 0.08)
        alab = note("the error was there all along · the net moved it")
        place(alab, left=ex2.get_right()[0] + 0.5, cy=pile2.get_center()[1])
        if alab.get_right()[0] > 6.4:
            place(alab, right=6.4, cy=pile2.get_center()[1] - 0.6)
        lesson = label("read the lines, not the exit code", 30, TURN)
        place(lesson, cx=0.9, bottom=-3.4)
        for m in (netg, pile2, ex2, alab, lesson, st, tbl):
            inside(m)
        assert lesson.get_top()[1] < alab.get_bottom()[1] - 0.15, (lesson.get_top(), alab.get_bottom())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(t, b184, b186, b188, b200, link)), run_time=0.4)
            self.play(FadeOut(p1), TransformFromCopy(exc, nlab), ReplacementTransform(net, net2),
                      ReplacementTransform(caught, caught2),
                      ReplacementTransform(dlab, dlab2), ReplacementTransform(slots, slots2),
                      ReplacementTransform(zero, zero2),
                      ReplacementTransform(ex0, ex2), run_time=0.9)
            self.play(FadeIn(p2, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Prepare found no files")
            self.play(flash(VGroup(slots2, zero2), TURN, 1.08), run_time=0.6)
            vo.wait_until("built an empty table")
            b232 = p2.bar(232, S.GREY, 0.22)
            tbl.move_to(slots2.get_center())
            self.play(FadeIn(tbl, scale=0.6), FadeIn(b232), run_time=0.4)
            self.play(tbl.animate.move_to(place(tbl.copy(), left=r235.get_right()[0] + 0.5,
                                                cy=r235.get_center()[1]).get_center()),
                      flash(p2.span(232, "output_pairs_df"), S.GREY, 1.1), run_time=0.9)
            vo.wait_until("and failed the first time")
            b243 = p2.bar(243, ERR, 0.22)
            q = p2.span(243, 'output_pairs_df["question"]')
            self.play(FadeIn(b243), q.animate.set_color(ERR), run_time=0.4)
            self.play(FadeIn(st, scale=1.3), run_time=0.4)
            vo.wait_until("The error was there")
            self.play(GrowArrow(arr), run_time=0.6)
            self.play(FadeIn(alab, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("the catch-all only moved")
            self.play(flash(VGroup(net2, nlab), S.GREY, 1.08), flash(st, ERR, 1.08), run_time=0.8)
            vo.wait_until("Read the lines")
            self.play(FadeIn(lesson, shift=UP * 0.1), run_time=0.5)
            self.play(flash(lesson, TURN, 1.06), run_time=0.6)

        # ========================================================== 3 · the fix: the key, exact name
        stage = Stage(show=("laptop", "key"))
        ill = illustration_tag()
        place(ill, right=6.4, top=2.75)
        fix = card_rows([_mixed_row(["key →", "`~/AC215/secrets/llm-service-account.json`", "(exact name)"]),
                         _mixed_row(["check:", "`ls -la /secrets`"])], frame_color=OWN, header="the fix")
        place(fix, cx=0, top=-1.6)
        inside(fix)
        sec = stage.row("secrets")
        # the stage's straight key -> /secrets mount crosses the end of "gemini-finetuner/": keep it
        # hidden (its saved opacity is 0, so parts_in leaves it invisible) and draw a bent one instead
        m_old = stage.parts["mounts_dc"][1]
        for f in m_old.get_family():
            f._hop = (0.0, 0.0)
        m_key = CurvedArrow(stage.key_out.get_right() + RIGHT * 0.08,
                            stage.boxes["dc"].secrets.get_left() + LEFT * 0.08, angle=0.9, color=LOOKUP,
                            stroke_width=2.5, tip_length=0.16)
        gfr = stage.row("gf")
        near = [pt for pt in m_key.get_all_points() if pt[0] < gfr.get_right()[0] + 0.1]
        assert all(pt[1] < gfr.get_bottom()[1] - 0.05 for pt in near), "the key's mount still crosses gf/"
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p2, b232, b243, tbl, st, arr, alab, lesson, netg, caught2, pile2, ex2)),
                      run_time=0.5)
            self.add(stage)
            self.play(*stage.parts_in("laptop", "key"), FadeIn(ill), run_time=0.7)
            vo.wait_until("The fix is the key")
            self.play(FadeIn(fix.frame), FadeIn(fix.header), FadeIn(fix.rows[0], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("put it in the secrets folder")
            self.play(flash(sec, KEY, 1.1), run_time=0.5)
            self.play(*stage.key_in(), run_time=0.7)
            vo.wait_until("with the exact name")
            self.play(flash(fix.rows[0], OWN, 1.04), flash(stage.key_solid, KEY, 1.3), run_time=0.7)
            vo.wait_until("and check with")
            self.play(FadeIn(fix.rows[1], shift=UP * 0.1), run_time=0.4)
            self.play(*stage.parts_in("dc", "mounts_dc"), FadeIn(m_key), run_time=0.6)
            self.play(flash(m_key, LOOKUP, 1.05), flash(stage.boxes["dc"].secrets, TURN, 1.2), run_time=0.8)

        # ========================================================== 4 · extra: the scripted stand-in data
        t2 = term(P_DC, rows=9, title=SECOND, top=2.75)
        ft2 = frame_tags(t2, scripted_tag(), extra_tag())
        card4 = card_rows(["hand-written in the shape Gemini returns · 20 pairs (Gemini: ≈ 100)"])
        place(card4, cx=0, top=t2.box.get_bottom()[1] - 0.2)
        chip4 = chip("not in the repo · with a key, generate writes these files for you", S.GREY, size=CAPTION)
        place(chip4, cx=0, top=card4.get_bottom()[1] - 0.18)
        inside(chip4)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(stage, ill, fix, stage.key_solid, m_key)), run_time=0.5)
            self.play(FadeIn(t2, shift=DOWN * 0.3), FadeIn(ft2), caption_extra(tr, True), run_time=0.6)
            bare_prompt(self, t2)
            type_cmd(self, t2, CP.cmd, 0.8)
            o4 = show(self, t2, CP, 2, *CP_ROWS, run_time=0.6)
            files = VGroup(*o4[1:6])
            vo.wait_until("five hand-written files")
            o_top = (o4[0].get_bottom()[1] + files.get_top()[1]) / 2
            o_bot = (files.get_bottom()[1] + o4[6].get_top()[1]) / 2
            outline = box(files.width + 0.3, o_top - o_bot, MODEL, fill_opacity=0.0, radius=0.06,
                          dashed=True).move_to([files.get_center()[0], (o_top + o_bot) / 2, 0])
            self.play(Create(outline), run_time=0.6)
            vo.wait_until("tagged scripted")
            self.play(flash(ft2[0], S.GREY, 1.15), run_time=0.6)
            vo.wait_until("in exactly the shape")
            self.play(FadeIn(card4, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("They hold 20 pairs")
            self.play(flash(card4.rows[0], TURN, 1.04), run_time=0.6)
            vo.wait_until("your generate writes")
            self.play(FadeIn(chip4, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Note the 1-byte CSV")
            r10 = o4[6]
            rg = ring(r10.glyphs, ERR, buff=0.08, stroke=3)
            self.play(Create(rg), run_time=0.5)
            left_by = note("left by the failed run")
            beside(left_by, t2, r10, buff=0.5)
            pin(self, r10, left_by, run_time=0.4)
            self.play(flash(substring(r10, "1"), ERR, 1.4), run_time=0.6)

        # ========================================================== 5 · prepare again: 19 by 2
        t3 = term(P_CTR_DC, rows=13, container="dc")
        ft3 = frame_tags(t3, scripted_tag())
        dd = excerpt_chip(DEDUP, f"{CLI} · line 233 (excerpt)", line=L233)
        place(dd, cx=0, top=TOP_Y - 0.12)
        inside(dd)
        names = [str(k + 1) for k in range(19)] + ["1"]       # the 20th repeats question 1
        bricks = VGroup(*[brick(True, w=0.52, text=s) for s in names]).arrange(RIGHT, buff=0.06)
        place(bricks, cx=0, top=dd.get_bottom()[1] - 0.7)
        inside(bricks)
        cnt_a = label("20 scripted pairs · numbered by question", CAPTION, S.GREY)
        cnt_b = label("19 rows", CAPTION, TURN)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(t2, ft2, outline, rg, card4, chip4), shift=UP * 0.3),
                      caption_extra(tr, False), run_time=0.6)
            self.play(FadeIn(t3, shift=UP * 0.2), FadeIn(ft3), run_time=0.5)
            bare_prompt(self, t3)
            type_cmd(self, t3, PREP.cmd, 0.6)
            vo.wait_until("Five files processed")
            o5 = show(self, t3, PREP, (4, 8), run_time=0.6)
            vo.wait_until("zero errors")
            o5b = show(self, t3, PREP, 9, 11, run_time=0.3)
            self.play(flash(o5b[0], TURN, 1.06), run_time=0.4)
            o5c = t3.print(self, [(PREP.line(n), OUTPUT) for n in range(13, 18)], run_time=0.5)
            r11 = o5b[1]
            vo.wait_until("and a shape of 19 by 2")
            self.play(r11.animate.set_color(TURN), run_time=0.3)
            self.play(flash(r11, TURN, 1.2), run_time=0.6)
            assert len(t3.lines) == 13, len(t3.lines)
            vo.wait_until("The last scripted pair")
            ref7 = term(P_CTR_DC, rows=7, container="dc")
            resize(self, t3, 7, keep=[r11, *o5c], run_time=0.7,
                   extra=[ft3.animate.set_y(ref7.box.get_top()[1] - ref7.bar_h / 2)])
            place(cnt_a, cx=0, top=bricks.get_bottom()[1] - 0.12)
            assert cnt_a.get_bottom()[1] > t3.box.get_top()[1] + 0.08, (cnt_a.get_bottom(), t3.box.get_top())
            cnt_b.move_to(cnt_a)
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in bricks], lag_ratio=0.08),
                      FadeIn(cnt_a), run_time=1.2)
            arc = ArcBetweenPoints(bricks[-1].get_top() + UP * 0.05, bricks[0].get_top() + UP * 0.05,
                                   angle=0.36, color=TURN, stroke_width=3)
            assert arc.get_top()[1] < dd.get_bottom()[1] - 0.05, (arc.get_top(), dd.get_bottom())
            self.play(Create(arc), bricks[0].frame.animate.set_stroke(TURN),
                      bricks[-1].frame.animate.set_stroke(TURN), run_time=0.7)
            vo.wait_until("and drop duplicates")
            self.play(FadeIn(dd, shift=DOWN * 0.1), run_time=0.5)
            self.play(flash(dd.chip, TURN, 1.04), run_time=0.5)
            vo.wait_until("removed it")
            xm = x_mark(0.3).move_to(bricks[-1])
            self.play(FadeIn(xm, scale=1.4), run_time=0.3)
            self.play(FadeOut(VGroup(bricks[-1], xm), shift=DOWN * 0.4), FadeOut(arc),
                      bricks[0].frame.animate.set_stroke(MODEL), run_time=0.6)
            self.play(VGroup(*bricks[:-1]).animate.set_x(0), run_time=0.4)
            self.play(FadeOut(cnt_a, shift=UP * 0.1), run_time=0.25)
            self.play(FadeIn(cnt_b, shift=UP * 0.1), run_time=0.3)
            vo.wait_until("Every answer opens")
            ops = VGroup(*[glyph_range(r, ANS_COL, len(r.text) - 1) for r in o5c])
            self.play(ops.animate.set_color(MODEL), run_time=0.5)
            self.play(flash(ops, MODEL, 1.08), run_time=0.7)

        # ========================================================== 6 · station 1: instruct-dataset.csv; your turn
        cv = Conveyor(STATIONS[:3])
        cv.move_to([0, 0.35, 0])
        for k in (1, 2):                           # only station 1 here; S07 builds the others
            cv.labels[k].set_opacity(0)
            cv.marks[k].set_opacity(0)
        csv = shape_card(["question,answer"], OWN)
        cv.put(0, csv)
        st_lab = cv.labels[0]
        inst = text_part(st_lab, "instruct")
        lchip = chip("instruction dataset · slide 5", S.GREY, size=CAPTION)
        place(lchip, left=st_lab.get_left()[0], top=st_lab.get_bottom()[1] - 0.2)
        lr = lref("5")
        tc = turn_card([GEN_CMD, PREP.cmd, (Prose("generate: billed · cents"), COST),
                        (Prose("prepare: free"), OWN)])
        place(tc, cx=0, bottom=-3.4)
        for m in (csv, lchip, tc):
            inside(m)
        assert tc.get_top()[1] < lchip.get_bottom()[1] - 0.1 or tc.get_left()[0] > lchip.get_right()[0] + 0.2
        b0 = bricks[0]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(t3, ft3, dd, cnt_b, *bricks[1:-1])), run_time=0.6)
            self.play(FadeIn(cv), run_time=0.5)
            self.play(b0.animate.move_to(csv.get_center()), run_time=0.7)
            self.play(ReplacementTransform(b0, csv), run_time=0.6)
            vo.wait_until("the lecture's term")
            self.play(inst.animate.set_color(TURN), FadeIn(lr), run_time=0.4)
            self.play(flash(inst, TURN, 1.2), FadeIn(lchip, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("Pause, and run")
            self.play(FadeIn(tc, shift=UP * 0.1), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(cv, csv, lchip, lr, tc, tr)), run_time=0.8)
        self.wait(0.3)


def Arrow_(a, b):
    """A GREY arrow (the net -> the stamp)."""
    from manim import Arrow
    return Arrow(a, b, buff=0, color=S.GREY, stroke_width=3, tip_length=0.18, max_tip_length_to_length_ratio=0.2)
