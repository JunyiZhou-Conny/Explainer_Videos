"""S03 · A tracker made of folders (notebook A) — tracker A1 → A6, lecture_ref 10–11.

Beats (script.md, ## S03; one voiceover block each):
0. Tracker A1 + lref. Colab menu illustration ("File → Save a copy in Drive", "Runtime → Change
   runtime type → GPU"), the study-guide chip, ▶ your turn. Cell 8 (nbA:101, 106, 112 → 115, 117, 120,
   the last cut at the frame), then cell 10 cropped to nbA:137 with `Tesla T4` YELLOW.
1. A2: cell 15's download line (nbA:318, cut after the release path), cell 17's output (nbA:352–353)
   with a YELLOW "remember this order" sticky. A3: cell 26 (nbA:432–433, 436, 439 → 445–447), the three
   counts light in turn, ▶ your turn.
2. The code stays; line 433 and the three counts glow. PONDER 8 s.
3. Both `test_size=test_percent` turn RED; a bar of 1,156 tiles splits 116 (test) off, then 104
   (validation) off the remaining 1,040, 936 left; `erratum` + "same lines in task.py:134–146".
4. A4: cell 31 (nbA:527–528) makes the ExperimentFolder; cell 12's five save/open lines (nbA:242, 245,
   249, 289, 307, elided around the path) light one by one with the legend; five files drop per model.
5. A5: the five metric files fly out and become notebook A's table (cell 54, six columns), cell 56's
   pick (nbA:1304) YELLOW, the "cells 54–59" chip + ▶ your turn; the erratum: the table narrows to
   name · accuracy, nbA:1272/1280 below, the strings card.
6. The first answer: 1,156 tiles, 116 light as "test", reshuffle twice ("no seed"); A's top two rows
   with a ruler "1 photo = 0.86 points (1/116)" and "2 photos" YELLOW.
7. A6: cell 62, cell 63 (names ringed YELLOW, "replace this with yours"), cell 66's upload output,
   the bucket chip, ▶ your turn; V1's Colab lane lights (notebook A → folder → bucket) and the GOLD
   cost tag. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F403
from explainer import style as S

SAY = NARRATION["S03"]
PONDER_SPLIT = ("The cell sets validation_percent = 0.2.\nYet validation is 104 of 1,156.\n"
                "What did the code actually do?")
TOP = 2.75                     # pictures stay under the tracker / lecture tag
LEFT_X = -6.35
HELPER_LINES = (242, 245, 249, 289, 307)      # cell 12: the five save / open lines, one per suffix
SIX = ("name", "epochs", "accuracy", "loss", "execution_time", "model_size")


def top_left(m, x=LEFT_X, y=TOP):
    """Place m with its top-left corner at (x, y)."""
    m.shift(np.array([x - m.get_left()[0], y - m.get_top()[1], 0]))
    return m


def helper_cell(size: float = 20) -> VGroup:
    """Cell 12's five save/open lines (extract text, masked by nb_line), each elided around the path
    so only the call and its suffix remain; drawn like notebook_cell (which cannot elide a line's
    middle). .rows .frame .header .ill"""
    texts = [elide(nb_line("A", n).strip(), ("(", '+"', suf + '"')) for n, suf in zip(HELPER_LINES, FIVE_FILES)]
    pitch = line_pitch(size)
    rows = VGroup()
    for i, s in enumerate(texts):
        r = mono_line(s, size, INK)
        r.shift(np.array([-r.strut.get_left()[0], -i * pitch - r.strut.get_center()[1], 0]))
        rows.add(r)
    for r in rows:
        k = r.text.index("…")
        glyph_range(r, k, k + 1).set_color(S.GREY)
    head = label(f"notebook A · cell {nb_cell('A', HELPER_LINES[0])}", CAPTION, S.GREY)
    w = max(rows.width + 0.8, head.width + 2.9 + 1.4)
    fr = RoundedRectangle(width=w, height=rows.height + 0.85, corner_radius=0.14, stroke_color=CLOUD,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    head.move_to(fr.get_corner(UL) + np.array([0.3 + head.width / 2, -0.3, 0]))
    rows.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.4).align_to(fr, DOWN).shift(UP * 0.15)
    ill = illustration_tag()      # in the header row (inside the frame): saves a row for the folder below
    ill.move_to(fr.get_corner(UR) + np.array([-0.2 - ill.width / 2, -0.32, 0]))
    g = VGroup(fr, head, rows, ill)
    g.frame, g.header, g.rows, g.ill = fr, head, rows, ill
    return g


class FolderTracker(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 8, len(SAY)
        assert nb_cell("A", 242) == 12 and nb_cell("A", 527) == 31 and nb_cell("A", 1304) == 56

        # ========================================================== 0. set up notebook A; one Tesla T4
        tr = tracker_a(1)
        ref = lref("10–11")
        m1 = notebook_menu(("File", "Save a copy in Drive"))
        m2 = notebook_menu(("Runtime", "Change runtime type", "GPU"))
        menus = VGroup(m1, m2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-0.6, 1.25, 0])
        m_ill = illustration_tag().next_to(menus, UP, buff=0.25).align_to(m2, RIGHT)
        guide = grey_chip("the study guide links notebooks A and B · the badges inside them open older copies")
        guide.next_to(menus, DOWN, buff=0.55).set_x(0)
        yt0 = your_turn().next_to(m2, RIGHT, buff=0.35)
        c8 = notebook_cell("A", 101, 106, 112, 115, 117, 120, size=20, cuts={120: "GPU:0'"})
        top_left(c8, -c8.width / 2)
        c10 = notebook_cell("A", 127, 137, size=20, cuts={137: "Tesla T4"})
        c10.move_to([0, 0.3, 0])
        t4 = c10.sub(137, "Tesla T4")

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("from the course page")
            self.play(FadeIn(guide, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("save a copy")
            self.play(FadeIn(m_ill), LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in m1], lag_ratio=0.3),
                      run_time=0.8)
            vo.wait_until("switch the runtime to a GPU")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.2) for x in m2], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("pause and set it up")
            self.play(FadeIn(yt0, shift=LEFT * 0.2), run_time=0.5)
            flash_tag(self, yt0, TURN)
            vo.wait_until("Its stored outputs")
            gone = VGroup(menus, m_ill, guide, yt0)
            self.play(FadeOut(gone, shift=UP * 0.2), FadeIn(c8, shift=UP * 0.2), run_time=0.8)
            self.remove(gone)
            vo.wait_until("the instructors' run")
            flash_tag(self, c8.tag, INK)
            vo.wait_until("one Tesla T4")
            gpu = c8.line(120)
            self.play(Indicate(gpu, color=TURN, scale_factor=1.05), run_time=0.6)
            self.play(FadeOut(c8, shift=UP * 0.2), FadeIn(c10, shift=UP * 0.2), run_time=0.7)
            self.remove(c8)
            self.play(t4.animate.set_color(TURN), run_time=0.5)
            t4r = ring(t4, TURN, buff=0.07)
            self.play(Create(t4r), run_time=0.5)

        # ========================================================== 1. dataset (A2), split (A3)
        c15 = notebook_cell("A", 318, size=20, cuts={318: "datasets/releases/"})
        top_left(c15)
        c17 = notebook_cell("A", 352, 353, size=20)
        top_left(c17, y=c15.get_bottom()[1] - 0.25)
        pin_ = sticky("remember this order", mono_font=False).next_to(c17.frame, RIGHT, buff=0.25)
        pin_.set_y(c17.line(352).get_center()[1])
        c26 = notebook_cell("A", (432, 433), "…", 436, 439, (445, 447), wrap=True, size=20)
        top_left(c26, -c26.width / 2)
        yt1 = your_turn().next_to(c26.frame, DOWN, buff=0.1).align_to(c26.frame, LEFT)
        counts = [c26.line(n) for n in (445, 446, 447)]

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(c10, t4r), shift=UP * 0.2), track(tr, 2), run_time=0.7)
            self.remove(c10, t4r)
            self.play(FadeIn(c15, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("1,156 photos")
            self.play(FadeIn(c17, shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(c17.sub(353, "1156"), color=TURN), run_time=0.5)
            vo.wait_until("from one GitHub release")
            self.play(Indicate(c15.sub(318, "github.com/dlops-io/datasets/releases/"), color=TURN,
                               scale_factor=1.04), run_time=0.8)
            vo.wait_until("with four cheese labels")
            self.play(Indicate(c17.line(352), color=INK, scale_factor=1.03), run_time=0.7)
            vo.wait_until("Remember their order")
            self.play(FadeIn(pin_, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("Then the split")
            old = VGroup(c15, c17, pin_)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 3), run_time=0.7)
            self.remove(old)
            self.play(FadeIn(c26, shift=UP * 0.2), run_time=0.7)
            for n, a in zip(counts, ("936 to train", "104 to validate", "116 to test")):
                vo.wait_until(a)
                self.play(Indicate(n, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Pause and run them")
            self.play(FadeIn(yt1, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, yt1, TURN)

        # ========================================================== 2. ponder: 0.2, yet 104 of 1,156
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(yt1), run_time=0.4)
            self.remove(yt1)
            vo.wait_until("The cell sets the validation percent")
            r433 = ring(c26.line(433), TURN, buff=0.07)
            self.play(Create(r433), run_time=0.7)
            vo.wait_until("to 0.2")
            self.play(Indicate(c26.sub(433, "0.2"), color=TURN, scale_factor=1.2), run_time=0.7)
            vo.wait_until("yet validation is 104")
            r446 = ring(c26.line(446), TURN, buff=0.06)
            self.play(Create(r446), run_time=0.6)
            vo.wait_until("What did the code actually do")
            self.play(each(counts, TURN, scale=1.06, lag=0.25), run_time=1.2)
        pc = ponder(self, PONDER_SPLIT, seconds=8)

        # ========================================================== 3. both splits use test_percent
        reds = [c26.sub(n, "test_size=test_percent") for n in (436, 439)]
        cols = 289                        # 289 × 4 = 1,156 tiles, split by whole columns
        bar = VGroup(*[Rectangle(width=0.03, height=0.11, stroke_width=0).set_fill(S.GREY, 0.45)
                       for _ in range(4 * cols)]).arrange_in_grid(rows=4, cols=cols, buff=0.008)
        bar.tiles = list(bar)
        bar.move_to([0, -1.55, 0])

        def columns(a, b):
            return VGroup(*[bar.tiles[r * cols + c] for r in range(4) for c in range(a, b)])

        test = columns(260, 289)          # 29 columns × 4 = 116
        val = columns(234, 260)           # 26 × 4 = 104
        train = columns(0, 234)           # 234 × 4 = 936
        whole = label("1,156 photos", 22, INK).next_to(bar, UP, buff=0.18)
        e_tag = erratum_tag()
        e_chip = grey_chip("same lines in task.py:134–146")
        e_row = VGroup(e_tag, e_chip).arrange(RIGHT, buff=0.25).move_to([0, -3.05, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(pc), FadeOut(VGroup(r433, r446)), run_time=0.5)
            self.remove(pc, r433, r446)
            vo.wait_until("Both splits use the test percent")
            self.play(*[g.animate.set_color(ERR) for g in reds], run_time=0.7)
            self.play(each(reds, ERR, scale=1.05, lag=0.3), run_time=0.9)
            vo.wait_until("10 percent of 1,156")
            small = notebook_cell("A", 436, 439, wrap=True, size=20)
            top_left(small, -small.width / 2)
            for n in (436, 439):
                small.sub(n, "test_size=test_percent").set_color(ERR)
            self.play(FadeOut(c26, shift=UP * 0.2), run_time=0.5)
            self.remove(c26)
            self.play(FadeIn(small, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(bar, lag_ratio=0.002), FadeIn(whole), run_time=0.8)
            vo.wait_until("is 116 for testing")
            self.play(test.animate.set_fill(TURN, 1).shift(RIGHT * 0.35), run_time=0.8)
            lt = label("116 · test", 22, TURN).next_to(test, DOWN, buff=0.2)
            rest = label("1,040", 22, INK).next_to(VGroup(*columns(0, 260)), DOWN, buff=0.2)
            self.play(FadeIn(lt, shift=UP * 0.1), FadeOut(whole), FadeIn(rest, shift=UP * 0.1), run_time=0.6)
            self.remove(whole)
            vo.wait_until("then 10 percent of the remaining 1,040")
            self.play(Indicate(rest, color=INK), run_time=0.7)
            vo.wait_until("is 104")
            self.play(val.animate.set_fill(INK, 0.9).shift(RIGHT * 0.17), run_time=0.8)
            lv = label("104 · validation", 22, INK).next_to(val, UP, buff=0.2)
            ltr = label("936 · train", 22, S.GREY).next_to(train, DOWN, buff=0.2)
            self.play(FadeIn(lv, shift=DOWN * 0.1), FadeOut(rest), FadeIn(ltr, shift=UP * 0.1), run_time=0.6)
            self.remove(rest)
            vo.wait_until("A small slip")
            self.play(FadeIn(e_row, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("copied into the repo trainer")
            flash_tag(self, e_tag, INK)

        # ========================================================== 4. the home-made tracker (A4)
        c31 = notebook_cell("A", 527, 528, size=20)
        hc = helper_cell()
        top_left(hc)
        top_left(c31, x=6.35 - c31.width)
        fold = ExperimentFolder()
        fold.move_to([-0.6, -3.57 + fold.height / 2, 0])
        mk = arrow(c31.frame.get_bottom(), np.array([c31.frame.get_center()[0], fold.card.get_top()[1], 0]), S.GREY)
        yt4 = your_turn().next_to(fold.card, RIGHT, buff=0.25)

        with self.voiceover(SAY[4]) as vo:
            old = VGroup(small, bar, lt, lv, ltr, e_row)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 4), run_time=0.7)
            self.remove(old)
            vo.wait_until("Cell 31 makes a folder")
            self.play(FadeIn(c31, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("named after the current Unix time")
            self.play(GrowArrow(mk), FadeIn(fold, shift=DOWN * 0.2), run_time=0.8)
            self.play(Indicate(fold.title[1], color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("the helper from cell 12")
            self.play(FadeIn(hc, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("drops five files into it")
            self.play(fold.drop(0), run_time=0.9)
            for k, a in enumerate(("the model,", "its weights,", "its structure,", "its history", "its metrics")):
                vo.wait_until(a)
                suf = substring(hc.rows[k], FIVE_FILES[k])
                self.play(Indicate(suf, color=TURN, scale_factor=1.06),
                          Indicate(fold.legend[k], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Pause and train the five models")
            self.play(FadeIn(yt4, shift=LEFT * 0.2), run_time=0.4)
            for i in range(1, 5):
                self.play(fold.drop(i), run_time=0.6)

        # ========================================================== 5. the table (A5), cell 56's pick, the erratum
        led = RunLedger("A", columns=SIX)
        top_left(led, -led.width / 2)
        idx = [r["idx"] for r in nb_table("A", 1283, 1295)]
        c56 = notebook_cell("A", 1304, size=20, hi={1304: TURN})
        top_left(c56, -c56.width / 2, led.get_bottom()[1] - 0.1)
        cells_chip = grey_chip("cells 54–59, through the predictions")
        yt5 = your_turn()
        turn5 = VGroup(cells_chip, yt5).arrange(RIGHT, buff=0.3).move_to([0, -2.6, 0])
        rr = led.ring_row(0, TURN)

        with self.voiceover(SAY[5]) as vo:
            metric = [fold.stacks[i][4] for i in range(5)]
            self.play(track(tr, 5), FadeOut(VGroup(hc, c31, mk, yt4)), run_time=0.6)
            self.remove(hc, c31, mk, yt4)
            self.play(*[f.animate.set_color(TURN).shift(UP * 0.25) for f in metric], run_time=0.5)
            fly = [f.copy() for f in metric]
            self.add(*fly)
            self.play(FadeOut(fold), run_time=0.5)
            self.remove(fold)
            vo.wait_until("into one table")
            shell = VGroup(led.frame, led.header, led.heads)
            self.play(FadeIn(shell), *[fly[int(idx[j])].animate.move_to(led.rows[j].frame.get_left() + RIGHT * 0.2)
                                       for j in range(5)], run_time=0.6)
            self.play(*[ReplacementTransform(fly[int(idx[j])], led.rows[j].frame) for j in range(5)],
                      run_time=0.5)
            self.play(LaggedStart(*[FadeIn(VGroup(*led.rows[j].cells.values()), shift=RIGHT * 0.15)
                                    for j in range(5)], lag_ratio=0.15), FadeIn(led.tag), run_time=0.7)
            vo.wait_until("and cell 56 picks its top row")
            self.play(Create(rr), run_time=0.6)
            self.play(FadeIn(c56, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("pause and run through the predictions")
            self.play(FadeOut(c56, shift=DOWN * 0.2), FadeIn(turn5, shift=UP * 0.15), run_time=0.6)
            self.remove(c56)
            flash_tag(self, yt5, TURN)
            # the erratum: the ledger narrows to name · accuracy; the two lines and a card beside it
            vo.wait_until("A small slip")
            led2 = RunLedger("A", columns=("name", "accuracy"))
            top_left(led2)
            card_e = card(["accuracy turned into text before sorting", "9.50% would rank above 68.97%"],
                          size=22)
            card_e.next_to(led2.frame, RIGHT, buff=0.4).align_to(led2.frame, DOWN)
            et = erratum_tag().next_to(card_e, UP, buff=0.12).align_to(card_e, LEFT)
            c54 = notebook_cell("A", 1272, 1280, size=20, cuts={1272: "map('{:,.2f}%'"})
            top_left(c54, -c54.width / 2, led2.get_bottom()[1] - 0.12)
            moves = [ReplacementTransform(led.rows[j].cells[c], led2.rows[j].cells[c])
                     for j in range(5) for c in ("name", "accuracy")]
            moves += [ReplacementTransform(led.rows[j].frame, led2.rows[j].frame) for j in range(5)]
            moves += [ReplacementTransform(led.heads[k], led2.heads[j]) for j, k in ((0, 0), (1, 2))]
            moves += [ReplacementTransform(m, n) for m, n in ((led.frame, led2.frame), (led.header, led2.header),
                                                             (led.tag, led2.tag))]
            moves_targets = [a.target_mobject for a in moves]
            fades = [FadeOut(led.rows[j].cells[c]) for j in range(5) for c in SIX if c not in ("name", "accuracy")]
            fades += [FadeOut(led.heads[k]) for k in (1, 3, 4, 5)]
            self.play(*moves, *fades, FadeOut(rr), FadeOut(turn5), run_time=1.0)
            self.remove(rr, turn5, led, *[m for m in moves_targets])
            self.add(led2)
            self.play(FadeIn(c54, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("accuracy becomes text before sorting")
            fmt = c54.sub(1272, "'{:,.2f}%'")
            srt = c54.sub(1280, "sort_values(by=['accuracy']")
            self.play(fmt.animate.set_color(ERR), FadeIn(card_e, shift=LEFT * 0.2), FadeIn(et), run_time=0.7)
            vo.wait_until("so it sorts strings")
            self.play(srt.animate.set_color(ERR), run_time=0.6)
            self.play(each([led2.cell(j, "accuracy") for j in range(5)], ERR, scale=1.08, lag=0.15), run_time=1.0)
            vo.wait_until("9.5 percent would rank above 68 percent")
            self.play(Indicate(card_e.body[1], color=INK, scale_factor=1.04), run_time=0.8)
            flash_tag(self, et, INK)

        # ========================================================== 6. the first answer: the test set
        grid = photo_grid(cols=68, rows=17, cell=0.085, gap=0.02)
        top_left(grid, y=TOP - 0.05)
        picks = [test_pick(seed=s) for s in (0, 1, 2)]
        t_lab = label("116 test photos", 24, TURN).next_to(grid, RIGHT, buff=0.45).align_to(grid, UP).shift(DOWN * 0.1)
        seed_chip = grey_chip("no seed: a different 116 every run")
        seed_chip.next_to(t_lab, DOWN, buff=0.35).align_to(t_lab, LEFT)
        two = RunLedger("A", rows=TABLE_A[:2], header="notebook A · cell 54 · top two rows")
        top_left(two, y=-0.65)
        a1, a2 = two.cell(0, "accuracy"), two.cell(1, "accuracy")
        assert (a1.original_text, a2.original_text) == ("68.97%", "67.24%")
        # the ruler: 67.24 → 68.97 in two steps of one test photo (100 / 116 = 0.86 points)
        rx0, rx1, ry = 1.6, 6.0, -2.35
        rl = Line([rx0, ry, 0], [rx1, ry, 0], color=S.GREY, stroke_width=3)
        ticks = VGroup(*[Line([x, ry - 0.12, 0], [x, ry + 0.12, 0], color=S.GREY, stroke_width=3)
                         for x in (rx0, (rx0 + rx1) / 2, rx1)])
        lo = mono("67.24%", 20, INK).next_to([rx0, ry, 0], UP, buff=0.22)
        hi = mono("68.97%", 20, INK).next_to([rx1, ry, 0], UP, buff=0.22)
        steps = VGroup(*[Rectangle(width=0.16, height=0.16, stroke_width=0).set_fill(TURN, 1)
                         .move_to([(rx0 + rx1) / 2 + d * (rx1 - rx0) / 4, ry + 0.34, 0]) for d in (-1, 1)])
        unit = VGroup(label("1 photo = 0.86 points", 24, INK), mono("(1/116)", 20, S.GREY)).arrange(RIGHT, buff=0.2)
        unit.move_to([(rx0 + rx1) / 2, -1.05, 0])
        brace = BraceBetweenPoints([rx0, ry - 0.2, 0], [rx1, ry - 0.2, 0], DOWN, color=TURN)
        twop = label("2 photos", 24, TURN).next_to(brace, DOWN, buff=0.08)

        with self.voiceover(SAY[6]) as vo:
            old = VGroup(led2, c54, card_e, et)
            self.play(FadeOut(old, shift=UP * 0.2), run_time=0.6)
            self.remove(old)
            self.play(FadeIn(grid, lag_ratio=0.001), run_time=0.9)
            vo.wait_until("The folder keeps settings and scores")
            self.play(ApplyWave(grid, amplitude=0.08), run_time=0.9)
            vo.wait_until("not which 116 photos")
            self.play(*[grid.tiles[i].animate.set_fill(TURN, 1) for i in picks[0]], FadeIn(t_lab), run_time=0.8)
            vo.wait_until("The split has no seed")
            self.play(FadeIn(seed_chip, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("graded on a different 116")
            for a, b in ((picks[0], picks[1]), (picks[1], picks[2])):
                off = [i for i in a if i not in b]
                on = [i for i in b if i not in a]
                self.play(*[grid.tiles[i].animate.set_fill(S.GREY, 0.45) for i in off],
                          *[grid.tiles[i].animate.set_fill(TURN, 1) for i in on], run_time=0.7)
            vo.wait_until("One photo is worth 0.86 points")
            self.play(FadeIn(two, shift=UP * 0.2), FadeIn(unit, shift=UP * 0.15), run_time=0.7)
            self.play(Create(rl), Create(ticks), TransformFromCopy(a2, lo), TransformFromCopy(a1, hi), run_time=0.9)
            vo.wait_until("the winner in notebook A leads by two photos")
            r0 = two.ring_row(0, TURN)
            self.play(Create(r0), LaggedStart(*[FadeIn(s, shift=DOWN * 0.2) for s in steps],
                                                                 lag_ratio=0.4), run_time=0.8)
            self.play(GrowFromCenter(brace), FadeIn(twop, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 7. upload the folder (A6), the cost tag
        c62 = notebook_cell("A", 1396, 1397, size=20)
        top_left(c62)
        c63 = notebook_cell("A", (1400, 1402), size=20, cuts={1401: '"ac215-project"', 1402: '"cheese-app-models"'})
        top_left(c63, y=c62.get_bottom()[1] - 0.15)
        names = [c63.sub(1401, '"ac215-project"'), c63.sub(1402, '"cheese-app-models"')]
        nrings = [ring(nm, TURN, buff=0.04, stroke=2.5) for nm in names]
        rtags = [row_tag("replace this with yours").next_to(c63.frame, RIGHT, buff=0.3).set_y(nm.get_center()[1])
                 for nm in names]
        assert rtags[0].get_bottom()[1] > rtags[1].get_top()[1] - 0.02, "replace tags overlap"
        c66 = notebook_cell("A", 1437, (1439, 1442), "…", size=20)
        top_left(c66, -c66.width / 2)
        b_chip = grey_chip("your bucket: one from lecture 11, or create it now · scene 7 shows how")
        b_chip.next_to(c66, DOWN, buff=0.3).align_to(c66.frame, LEFT)
        yt7 = your_turn().next_to(b_chip, DOWN, buff=0.25).align_to(b_chip, LEFT)
        mp = TrainingMap.at("S03")
        ctag = cost_tag("stored in your bucket · weights of 10–104 MB per model (the table's model_size),\n"
                        "plus a .keras copy of each")
        ctag.move_to([0, -2.55, 0])

        with self.voiceover(SAY[7]) as vo:
            old = VGroup(grid, t_lab, seed_chip, two, r0, rl, ticks, lo, hi, steps, unit, brace, twop)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 6), run_time=0.7)
            self.remove(old)
            self.play(FadeIn(c62, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("put your own project and bucket")
            self.play(FadeIn(c63, shift=UP * 0.2), run_time=0.6)
            self.play(*[Create(r) for r in nrings], *[FadeIn(t, shift=LEFT * 0.15) for t in rtags], run_time=0.7)
            vo.wait_until("and run cell 66")
            old = VGroup(c62, c63, *nrings, *rtags)
            self.play(FadeOut(old, shift=UP * 0.2), FadeIn(c66, shift=UP * 0.2), run_time=0.8)
            self.remove(old)
            self.play(Indicate(c66.sub(1437, EXPERIMENT), color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("Any bucket of yours works")
            self.play(FadeIn(b_chip, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Pause and run it")
            self.play(FadeIn(yt7, shift=UP * 0.15), run_time=0.4)
            flash_tag(self, yt7, TURN)
            vo.wait_until("A gold tag")
            old = VGroup(c66, b_chip, yt7)
            self.play(FadeOut(old, shift=UP * 0.2), FadeIn(mp), run_time=0.6)
            self.remove(old)
            self.play(mp.light("nbA"), run_time=0.3)
            self.play(mp.light("laneA", "folder"), run_time=0.4)
            self.play(mp.light("bucket"), run_time=0.4)
            vo.wait_until("those files now sit in your bucket")
            self.play(FadeIn(ctag, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("10 to 104 megabytes")
            flash_tag(self, ctag, COST)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
