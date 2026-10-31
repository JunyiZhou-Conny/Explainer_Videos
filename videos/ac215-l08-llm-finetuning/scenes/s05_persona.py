"""S05 · Manufacturing a persona (README "Dataset › Generate Text", steps 1-4, and "Dataset › Samples").
Lecture: 4–5 (the tag shows in beats 0-1, the instruction-dataset and teacher idea).

Beats (script.md "## S05", one voiceover block each):
 0  LECTURE 4–5. No terminal. The lecture's three-part card (instruction / context / output, our
    redrawing of slide 5) writes in, each row lit as named; on "drops the context" the context row
    fades and the card closes into a GREEN-outlined two-field brick (question / answer). A stack of
    empty brick outlines grows behind it with the counter "≈ 100"; on "a teacher" a BLUE teacher box
    appears with an arrow into the stack.
 1  V3: the teacher box grows into the Teacher piece's BLUE box (gemini-3.1-flash-lite, location =
    global; GOLD "billed · cents"); excerpt chips cli.py line 19 (GENERATIVE_MODEL) and line 18
    (GCP_LOCATION) at the bottom. The system-instruction card and the input-prompt card slide in as
    named; the PINK-outlined mould "response_schema" (cli.py · lines 146–160) and the pile appear;
    five BLUE Q·A bricks drop through the mould onto slots "batch 0 … 4".
 2  TRACKER DsGen 1. The picture shrinks to a strip along the top (the teacher box + five empty
    brick slots). Full-width TEAL container terminal (title bar: `no key`, GOLD `billed`):
    `python cli.py --generate`; a GOLD two-row chip "≈ $2 / 1,000 iterations · README.md:151" beside
    it. dataset-creator/05 lines 4, 5 (wrapped once, so "was not found." shows), 6–9, …, 12–13; the
    error lines RED (cut at 65 characters); one slot of the strip goes dark per batch (the … row
    darkens the fourth). The prompt returns: GREY caption "exit status 0", YELLOW ring.
 3  TRACKER DsGen 2. The strip at the top fades; the terminal shrinks to a 3-row strip (line 12, line
    13 and the prompt with the circled "exit status 0"). Above it CODE(dataset-creator/cli.py: 84–89,
    96, folded, 20 pt, persona masked); line 84 lights, then the openers 85–89 one by one, then 96.
 4  TRACKER DsGen 3: a two-row excerpt chip of cli.py line 169 ("Generate 20 diverse, informative,
    and engaging question-answer pairs about cheese") with the GREY note "= README.md · line 144".
    TRACKER DsGen 4: CODE(dataset-creator/cli.py: 170, 173–174, 179–181, folded): line 170 YELLOW
    with the erratum tag under the panel; line 174 lights; 179–180 PINK and a small PINK mould
    appears beside them and pulses.
 5  TRACKER DsSamples 1. The panel and the strip fade. QUOTE(expected/readme-generate-sample-qa:
    4–5, 6 cut after "‹instructor›,", 7, 8, 9–10 cut after "cheese monker,", 11), tag `expected`;
    the two answer openers light BLUE. A GREY erratum chip under it (line numbers only).
 6  The quote card fades. A two-row excerpt chip of cli.py line 45 ("Include specific data such as
    optimal pH levels, aging temperatures, and humidity percentages"); "optimal pH levels" lights.
    PONDER (8 s).
 7  The ponder card leaves. A BLUE brick with a RED-ringed "pH ✗" travels from a BLUE teacher box
    into a GREEN dataset stack, then into a GREY student-model box, which says the same "pH ✗" in a
    speech bubble with the ‹instructor› chip. Caption "synthetic data carries the teacher's
    mistakes"; the teacher is ringed YELLOW. Everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Polygon,
    ReplacementTransform,
    TransformFromCopy,
    VGroup,
)

from common import *  # noqa: F401,F403
from common import _Reveal, _set_op, _with_header
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real captures and sources
GEN = capture("dataset-creator/05")
assert GEN.cmd == "python cli.py --generate" and GEN.exit == 0, (GEN.cmd, GEN.exit)
assert GEN.line(4) == "Generating batch: 0" and GEN.line(12) == "Generating batch: 4", GEN.lines
assert all("was not found." in GEN.line(n) for n in (5, 7, 9, 11, 13)), GEN.lines
CLI = "dataset-creator/cli.py"
L18, L19, L45, L169 = (source_line(CLI, n) for n in (18, 19, 45, 169))
assert 'GCP_LOCATION = "global"' in L18 and 'GENERATIVE_MODEL = "gemini-3.1-flash-lite"' in L19
assert source_line(CLI, 170).strip().startswith("NUM_ITERATIONS = 5")
assert "temperature=0.9" in source_line(CLI, 174)
assert "response_schema=response_schema" in source_line(CLI, 180)
assert source_line(CLI, 146).startswith("response_schema = {") and source_line(CLI, 160) == "}"
R144, R151, R106 = source_line("README.md", 144), source_line("README.md", 151), source_line("README.md", 106)
assert "$2.0 for 1000 iterations" in R151 and "default parameters" in R106
P169 = ["Generate 20 diverse, informative, and engaging", "question-answer pairs about cheese"]
assert " ".join(P169) in L169 and " ".join(P169) in R144
P45 = ["Include specific data such as optimal pH levels,", "aging temperatures, and humidity percentages"]
assert " ".join(P45) in L45
QA = capture("expected/readme-generate-sample-qa")
QA6, QA10 = QA.cut(6, f"{PERSONA},"), QA.cut(10, "cheese monker,")
assert "Welcome welcome welcome" in QA6 and QA10.lstrip().startswith('"answer": "Yello - this is'), (QA6, QA10)

# ------------------------------------------------------------------ layout
TOP_Y = 2.87                     # top of a full-width panel (just under the tracker)


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


def text_part(t, sub: str) -> VGroup:
    """The glyphs of `sub` in a serif/mono Text (Text keeps no glyphs for spaces)."""
    s, needle = t.text, sub.replace(" ", "")
    i = s.find(needle)
    if i < 0:
        raise ValueError(f"{sub!r} not in {s!r}")
    assert len(t.submobjects) == len(s), (len(t.submobjects), len(s))
    return VGroup(*t.submobjects[i:i + len(needle)])


def excerpt_rows(rows, header: str, line: str) -> VGroup:
    """An excerpt chip over two rows: the rows joined by one space are an exact sub-string of
    `line` (checked). .rows .header .frame"""
    assert " ".join(rows) in line, rows
    body = VGroup(*[mtext(r, CAPTION, INK) for r in rows]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    fr = box(body.width + 0.5, body.height + 0.36, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
    body.move_to(fr)
    head = label(header, CAPTION, S.GREY).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.08)
    g = VGroup(fr, body, head)
    g.frame, g.rows, g.header = fr, body, head
    return g


def note_card(rows, color: str = S.GREY) -> VGroup:
    """A GREY card of serif rows (erratum notes). .rows .frame"""
    body = VGroup(*[label(r, CAPTION, c) for r, c in rows]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    fr = box(body.width + 0.5, body.height + 0.32, color, fill=S.BG, fill_opacity=0.95, radius=0.12)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.rows = fr, body
    return g


def ph_mark(size: float = CAPTION) -> VGroup:
    """'pH ✗' in a RED ring: a wrong number (we never write a value)."""
    t = label("pH", size + 4, INK)
    x = x_mark(0.24).next_to(t, RIGHT, buff=0.12)
    g = VGroup(t, x)
    r = ring(g, ERR, buff=0.1, stroke=3)
    out = VGroup(g, r)
    out.ring = r
    return out


class Persona(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        # ========================================================== 0 · the lecture's instruction dataset
        lr = lref("4–5")
        ic = InstructionCard().move_to([0.0, 0.5, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(lr), Create(ic.frame), run_time=1.0)
            vo.wait_until("three parts")
            self.play(LaggedStart(*[Create(sp) for sp in ic.seps], lag_ratio=0.4), run_time=0.8)
            vo.wait_until("an instruction")
            self.play(FadeIn(ic.rows[0], shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("optional context")
            self.play(FadeIn(ic.rows[1], shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("and the output")
            self.play(FadeIn(ic.rows[2], shift=RIGHT * 0.15), run_time=0.4)
            self.remove(ic.frame, ic.seps, *ic.rows)
            self.add(ic)
            vo.wait_until("The tutorial drops")
            self.play(flash(ic.rows[1], ERR, 1.1), run_time=0.6)
            ic.to_pair(self, run_time=1.2)
            self.play(ic.frame.animate.set_stroke(OWN), run_time=0.5)
            # the stack of empty bricks behind it, and the counter
            fw, fh = ic.frame.width, ic.frame.height
            stack = VGroup(*[box(fw, fh, S.GREY, fill=S.BG, fill_opacity=1.0, radius=0.14)
                             .move_to(ic.frame).shift(np.array([0.16 * k, 0.16 * k, 0]))
                             for k in range(6, 0, -1)])
            for k, b in enumerate(stack):
                b.set_stroke(S.GREY, opacity=0.35 + 0.08 * k)
                b.set_z_index(-1)
            count = label("≈ 100", 30, INK).next_to(stack, RIGHT, buff=0.45)
            vo.wait_until("Who writes")
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.08 + RIGHT * 0.08) for b in reversed(stack)],
                                  lag_ratio=0.2), FadeIn(count, shift=LEFT * 0.1), run_time=1.2)
            vo.wait_until("Another model")
            hint = model_box("teacher", w=2.2, h=0.9).move_to([-4.6, 0.5 + 0.48, 0])
            ha = Arrow(hint.get_right() + RIGHT * 0.05, ic.frame.get_left() + LEFT * 0.08, buff=0,
                       color=MODEL, stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.3)
            self.play(FadeIn(hint, shift=RIGHT * 0.2), run_time=0.5)
            self.play(GrowArrow(ha), run_time=0.4)

        # ========================================================== 1 · V3: teacher, cards, mould, bricks
        td = Teacher(show=())
        tb = td.teacher_box
        gl, arrows = td.teacher[1], td.teacher[2]
        c1, c2 = td.cards[0], td.cards[1]
        mould = td.parts["mould"]
        mould[0].set_stroke(LOOKUP)
        mnote = label("cli.py · lines 146–160", CAPTION, S.GREY).next_to(mould[1], DOWN, buff=0.1) \
            .align_to(mould[1], LEFT)
        pile = td.parts["pile"]
        nums = pile[2]
        batch = label("batch", CAPTION, S.GREY).next_to(nums, LEFT, buff=0.3)
        bill = billed_tag("billed · cents").next_to(tb.frame, RIGHT, buff=0.3)
        e19 = excerpt_chip('GENERATIVE_MODEL = "gemini-3.1-flash-lite"', f"{CLI} · line 19 (excerpt)", line=L19)
        e18 = excerpt_chip('GCP_LOCATION = "global"', f"{CLI} · line 18 (excerpt)", line=L18)
        place(e19, left=-6.3, top=-2.0)
        place(e18, left=e19.get_right()[0] + 0.3, top=-2.0)
        if e18.get_right()[0] > 6.4:                   # too wide side by side: stack them
            place(e19, top=-1.66)
            place(e18, left=-6.3, top=e19.get_bottom()[1] - 0.1)
        assert e18.get_bottom()[1] > -3.56 and e18.get_right()[0] < 6.45, e18.get_corner(DOWN + RIGHT)
        assert e19.get_right()[0] < batch.get_left()[0] - 0.2 or e19.get_top()[1] < nums.get_bottom()[1] - 0.05
        target = tb.copy()
        _set_op(target)                       # the copy at its real opacity (the piece hides it)
        with self.voiceover(SAY[1]) as vo:
            self.add(td)
            self.play(FadeOut(VGroup(ic, stack, count, ha)), ReplacementTransform(hint, target), run_time=0.8)
            self.remove(target)
            _set_op(tb)
            self.play(_Reveal(gl), FadeIn(bill, shift=LEFT * 0.1), run_time=0.5)
            self.play(FadeIn(e19, shift=UP * 0.1), run_time=0.4)
            self.play(flash(tb.sub, MODEL, 1.08), run_time=0.6)
            vo.wait_until("called in the global")
            self.play(FadeIn(e18, shift=UP * 0.1), flash(gl, MODEL, 1.15), run_time=0.6)
            vo.wait_until("It gets a system")
            self.play(_Reveal(c1, shift=RIGHT * 0.4), run_time=0.5)
            self.play(_Reveal(arrows[0]), run_time=0.3)
            vo.wait_until("an input prompt")
            self.play(_Reveal(c2, shift=RIGHT * 0.4), run_time=0.5)
            self.play(_Reveal(arrows[1]), run_time=0.3)
            vo.wait_until("and a JSON schema")
            self.play(_Reveal(mould), FadeIn(mnote), _Reveal(pile), FadeIn(batch), run_time=0.6)
            vo.wait_until("question and answer objects")
            for i in range(5):
                td.pour(self, i, run_time=0.6)

        # ========================================================== 2 · step 1: python cli.py --generate
        tr = tracker("DsGen", 1)
        t = term(P_CTR_DC, rows=12, container="dc")
        tags = frame_tags(t, nokey_tag(), billed_tag())
        st_tb = VGroup(box(mono(TEACHER, CAPTION).width + 0.4, 0.55, MODEL, fill_opacity=0.14, radius=0.1, stroke=3),
                       mono(TEACHER, CAPTION, INK))
        st_tb[1].move_to(st_tb[0])
        slots = VGroup(*[box(0.55, 0.42, MODEL, fill_opacity=0.0, radius=0.06, stroke=2) for _ in range(5)])
        slots.arrange(RIGHT, buff=0.1)
        st_ar = Arrow(ORIGIN_L, ORIGIN_L + RIGHT * 0.45, buff=0, color=S.GREY, stroke_width=3, tip_length=0.14,
                      max_tip_length_to_length_ratio=0.4)
        strip = VGroup(st_tb, st_ar, slots).arrange(RIGHT, buff=0.15)
        place(strip, left=-1.7, cy=2.62)
        assert strip.get_right()[0] < 6.45 and strip.get_bottom()[1] > t.box.get_top()[1] + 0.08, strip.get_corner(DOWN + RIGHT)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(td, mnote, batch, bill, e18, e19, lr)), TransformFromCopy(tb, st_tb),
                      TransformFromCopy(td.bricks, slots), FadeIn(st_ar), run_time=0.9)
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.2), FadeIn(tags), run_time=0.6)
            bare_prompt(self, t)
            cmd = type_cmd(self, t, GEN.cmd, 0.7)
            # the cost chip: two rows beside the command (the rows under it are short)
            cost = VGroup(label("≈ $2 / 1,000 iterations", CAPTION, COST),
                          label("README.md:151", CAPTION, S.GREY)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
            cfr = box(cost.width + 0.36, cost.height + 0.2, COST, fill=S.BG, fill_opacity=0.95, radius=0.1)
            cost.move_to(cfr)
            costc = VGroup(cfr, cost)
            vo.wait_until("With a key")
            row0_y = cmd.strut.get_center()[1]
            place(costc, right=t.box.get_right()[0] - 0.15, cy=row0_y - t.pitch / 2)
            assert costc.get_left()[0] > cmd.glyphs.get_right()[0] + 0.3, costc.get_left()
            self.play(FadeIn(costc, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("the README estimates")
            self.play(flash(cost[0], COST, 1.08), run_time=0.6)
            vo.wait_until("Without one")
            o4 = show(self, t, GEN, 4, run_time=0.3)
            assert costc.get_left()[0] > o4[0].glyphs.get_right()[0] + 0.3
            o5 = t.print(self, [(GEN.line(5), ERR)], wrap=True, run_time=0.4)
            assert len(o5) == 2, [r.text for r in o5]
            self.play(_dark(slots[0]), run_time=0.3)
            for k, n in enumerate((6, 8)):
                show(self, t, GEN, n, run_time=0.25)
                t.print(self, [(GEN.line(n + 1), ERR)], run_time=0.3)
                self.play(_dark(slots[k + 1]), run_time=0.3)
            t.print(self, [("…", S.GREY)], run_time=0.25)
            self.play(_dark(slots[3]), run_time=0.3)
            r12 = show(self, t, GEN, 12, run_time=0.25)[0]
            r13 = t.print(self, [(GEN.line(13), ERR)], run_time=0.3)[0]
            self.play(_dark(slots[4]), run_time=0.3)
            vo.wait_until("the key file was not found")
            nf = wrapped_glyphs(o5, "was not found.")
            self.play(flash(nf, ERR, 1.12), run_time=0.7)
            vo.wait_until("And yet the exit")
            pr = bare_prompt(self, t)
            assert len(t.lines) <= 12
            ex = note("exit status 0").next_to(pr.glyphs, RIGHT, buff=0.5).set_y(pr.strut.get_center()[1])
            pin(self, pr, ex, run_time=0.4)
            exr = ring(ex, TURN, buff=0.1, stroke=3)
            pin(self, pr, exr, run_time=0.5, anim=Create(exr))
            vo.wait_until("Remember that zero")
            self.play(flash(VGroup(ex, exr), TURN, 1.15), run_time=0.8)

        # ========================================================== 3 · step 2: the system prompt
        p3 = src_panel(CLI, [(84, 89), 96], size=20, wrap={84: ["sets the scene"], 96: ["to enhance"]})
        _with_header(p3, f"{CLI} · lines 84–96 (folded)")
        place(p3, cx=0, top=TOP_Y)
        assert p3.get_bottom()[1] > STRIP_TOP + 0.08, p3.get_bottom()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(strip, costc)), tr.goto(2), run_time=0.5)
            resize(self, t, 3, keep=[r12, r13, pr], run_time=0.6,
                   extra=[tags.animate.set_y(STRIP_TOP - t.bar_h / 2)])
            vo.wait_until("which lives in cli.py")
            self.play(FadeIn(p3, shift=UP * 0.15), run_time=0.6)
            self.play(flash(p3.header, TURN, 1.06), run_time=0.6)
            vo.wait_until("It tells the teacher")
            b84 = p3.bar(84, TURN)
            self.play(FadeIn(b84), run_time=0.4)
            vo.wait_until("to open each answer")
            self.play(flash(p3.span(84, "engaging introduction"), TURN, 1.08), run_time=0.6)
            vo.wait_until("one of the instructor's")
            self.play(flash(p3.span(84, PERSONA), TURN, 1.12), run_time=0.6)
            vo.wait_until("such as good question")
            bars = [p3.bar(n, TURN) for n in range(85, 90)]
            for b in bars:
                self.play(FadeIn(b), run_time=0.35)
            vo.wait_until("And it asks for")
            b96 = p3.bar(96, TURN)
            self.play(FadeOut(VGroup(b84, *bars)), FadeIn(b96), run_time=0.5)
            self.play(flash(p3.span(96, "enthusiastic exclamations"), TURN, 1.08), run_time=0.7)

        # ========================================================== 4 · steps 3-4: input prompt, iterations, config
        e169 = excerpt_rows(P169, f"{CLI} · line 169 (excerpt)", L169)
        n144 = note("= README.md · line 144").next_to(e169.frame, DOWN, buff=0.15).align_to(e169.frame, RIGHT)
        g169 = VGroup(e169, n144).move_to([0, 1.0, 0])
        p4 = src_panel(CLI, [170, (173, 174), (179, 181)])
        place(p4, cx=0, top=TOP_Y)
        err4 = erratum_tag('a constant you edit · README.md:106 says "default parameters"')
        place(err4, right=p4.get_right()[0], cy=(p4.get_bottom()[1] + STRIP_TOP) / 2)
        assert err4.get_top()[1] < p4.get_bottom()[1] - 0.03 and err4.get_bottom()[1] > STRIP_TOP + 0.03, err4.get_center()
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p3, b96)), tr.goto(3), run_time=0.5)
            self.play(FadeIn(e169, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(n144), run_time=0.4)
            vo.wait_until("asking for 20 diverse")
            self.play(flash(text_part(e169.rows[0], "Generate 20 diverse"), TURN, 1.1), run_time=0.7)
            vo.wait_until("Step 4")
            self.play(FadeOut(g169), tr.goto(4), run_time=0.5)
            self.play(FadeIn(p4, shift=UP * 0.15), run_time=0.5)
            b170 = p4.bar(170, TURN)
            self.play(FadeIn(b170), p4.span(170, "NUM_ITERATIONS").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("not a flag")
            self.play(FadeIn(err4, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Temperature 0.9")
            b174 = p4.bar(174, TURN)
            self.play(FadeIn(b174), run_time=0.4)
            self.play(flash(p4.span(174, "temperature=0.9"), TURN, 1.1), run_time=0.6)
            vo.wait_until("and the response schema")
            b179, b180 = p4.bar(179, LOOKUP), p4.bar(180, LOOKUP)
            row179 = p4.code.code_lines[p4.rows_of(179)[0]]
            row180 = p4.code.code_lines[p4.rows_of(180)[0]]
            mx = p4.get_right()[0] - 1.1
            my = (row179.get_center()[1] + row180.get_center()[1]) / 2
            mini = Polygon([-0.5, 0.3, 0], [0.5, 0.3, 0], [0.2, -0.3, 0], [-0.2, -0.3, 0],
                           stroke_color=LOOKUP, stroke_width=3).set_fill(LOOKUP, 0.12).move_to([mx, my, 0])
            assert mini.get_left()[0] > max(row179.get_right()[0], row180.get_right()[0]) + 0.3
            self.play(FadeIn(b179), FadeIn(b180), run_time=0.4)
            self.play(TransformFromCopy(p4.span(180, "response_schema", 1), mini), run_time=0.7)
            self.play(flash(mini, LOOKUP, 1.25), run_time=0.7)

        # ========================================================== 5 · samples (expected) and the openers erratum
        q = quote_card("readme-generate-sample-qa", 4, 5, QA6, 7, 8, 9, QA10, 11)
        e5 = note_card([("erratum · README.md:114–135 lists older openers than cli.py:83–101", S.GREY),
                        ("cli.py's own sample answers (lines 127–141) still open with Yello / Welcome", S.GREY)])
        e5.next_to(q, DOWN, buff=0.3)
        VGroup(q, e5).move_to([0, 0.15, 0])
        assert q.get_top()[1] < 2.9
        assert e5.get_bottom()[1] > -3.5 and e5.width < 12.9, (e5.get_bottom(), e5.width)
        rows = q.rows
        r_w = next(r for r in rows if "Welcomewelcomewelcome" in r.text)
        r_y = next(r for r in rows if "Yello-thisis" in r.text)
        op_w = text_part(r_w, "Welcome welcome welcome,")
        op_y = VGroup(text_part(r_y, "Yello - this is"), text_part(r_y, "your cheese monker,"))
        strip_out = VGroup(t, tags)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p4, b170, b174, b179, b180, mini, err4)), FadeOut(strip_out), run_time=0.45)
            self.play(FadeIn(q, shift=UP * 0.15), run_time=0.5)
            tr = switch_section(self, tr, "DsSamples", 1)
            vo.wait_until("Yello, this is")
            self.play(op_y.animate.set_color(MODEL), run_time=0.5)
            self.play(flash(op_y, MODEL, 1.06), run_time=0.6)
            vo.wait_until("A small slip")
            self.play(FadeIn(e5, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("lists older openers")
            self.play(flash(e5.rows[0], TURN, 1.04), run_time=0.6)
            vo.wait_until("but cli.py")
            self.play(op_w.animate.set_color(MODEL), run_time=0.5)
            self.play(flash(op_w, MODEL, 1.06), flash(op_y, MODEL, 1.06), run_time=0.7)
            vo.wait_until("Expect a mix")
            self.play(flash(e5.rows[1], TURN, 1.04), run_time=0.6)

        # ========================================================== 6 · the pH request; PONDER
        e45 = excerpt_rows(P45, f"{CLI} · line 45 (excerpt)", L45).move_to([0, 1.1, 0])
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(q, e5)), run_time=0.5)
            self.play(FadeIn(e45, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("The prompt asks")
            self.play(flash(e45.header, TURN, 1.06), run_time=0.6)
            vo.wait_until("such as optimal")
            ph = text_part(e45.rows[0], "optimal pH levels,")
            self.play(ph.animate.set_color(TURN), run_time=0.4)
            self.play(flash(ph, TURN, 1.1), run_time=0.6)
        card = ponder_at(self, "If the teacher gets a pH value wrong,\nwhat happens to it after fine-tuning?", 8)

        # ========================================================== 7 · synthetic data carries the teacher's mistakes
        y0 = 0.1
        teach = model_box("teacher", w=2.6, h=1.1, sub=TEACHER).move_to([-4.3, y0, 0])
        data = VGroup(*[box(2.1, 0.72, OWN, fill=S.BG, fill_opacity=1.0, radius=0.06) for _ in range(3)])
        data.arrange(DOWN, buff=0.1).move_to([0, y0 - 0.25, 0])
        dlab = label("dataset", CAPTION, OWN).next_to(data, DOWN, buff=0.15)
        stud = model_box("student model", w=2.6, h=1.1, color=S.GREY).move_to([4.3, y0, 0])
        pb = VGroup(box(1.8, 0.62, MODEL, fill_opacity=0.25, radius=0.08), ph_mark())
        pb[1].move_to(pb[0])
        pb.next_to(teach, RIGHT, buff=0.05)
        slot_top = data[0].get_top() + UP * 0.45
        bub = VGroup(persona_chip(), ph_mark()).arrange(RIGHT, buff=0.3)
        bfr = box(bub.width + 0.5, bub.height + 0.36, S.GREY, fill=S.BG, fill_opacity=1.0, radius=0.2)
        bub.move_to(bfr)
        tail = Polygon([-0.15, 0, 0], [0.15, 0, 0], [0.05, -0.3, 0], stroke_color=S.GREY, stroke_width=2.5) \
            .set_fill(S.BG, 1)
        bubble = VGroup(tail, bfr, bub)
        bubble.next_to(stud, UP, buff=0.4)
        if bubble.get_right()[0] > 6.4:
            bubble.shift(LEFT * (bubble.get_right()[0] - 6.4))
        tail.next_to(bfr, DOWN, buff=-0.04).set_x(stud.get_center()[0])
        cap7 = label("synthetic data carries the teacher's mistakes", 28, INK).move_to([0, -2.4, 0])
        assert bubble.get_top()[1] < 2.85, bubble.get_top()
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(card), FadeOut(e45), run_time=0.5)
            self.play(FadeIn(teach, shift=RIGHT * 0.2), FadeIn(data), FadeIn(dlab), FadeIn(stud, shift=LEFT * 0.2),
                      run_time=0.7)
            self.play(FadeIn(pb, scale=0.8), run_time=0.4)
            self.play(pb.animate.move_to(slot_top), run_time=0.9)
            self.play(pb.animate.move_to(data[0]), run_time=0.4)
            vo.wait_until("The student learns")
            pb2 = pb.copy()
            self.add(pb2)
            self.play(pb2.animate.move_to(stud.get_center()), run_time=1.0)
            self.play(FadeOut(pb2, scale=0.4), flash(stud.frame, S.GREY, 1.06), run_time=0.6)
            said = ph_mark().move_to(stud.get_center())
            self.play(FadeIn(tail), FadeIn(bfr), FadeIn(bub[0]), said.animate.move_to(bub[1]), run_time=0.8)
            self.remove(said)
            self.add(bub[1])
            vo.wait_until("in the instructor")
            self.play(flash(bub[0], TURN, 1.12), run_time=0.6)
            vo.wait_until("Synthetic data carries")
            self.play(FadeIn(cap7, shift=UP * 0.1), run_time=0.6)
            self.play(flash(VGroup(pb[1].ring, bub[1].ring), ERR, 1.15), run_time=0.7)
            vo.wait_until("so check what")
            tr7 = ring(teach, TURN, buff=0.12, stroke=4)
            self.play(Create(tr7), run_time=0.6)
        self.play(FadeOut(VGroup(teach, data, dlab, stud, pb, bubble, cap7, tr7, tr)), run_time=0.8)
        self.wait(0.3)


ORIGIN_L = np.array([0.0, 0.0, 0.0])


def _dark(slot):
    """A brick slot of the strip goes dark (its batch failed)."""
    return slot.animate.set_stroke(S.GREY_DARK, opacity=1.0).set_fill(S.GREY_DARK, 0.7)
