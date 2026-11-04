"""S13 · Three switches for one GPU (AC215 L13) — the optional CPU step read in reverse.

Beats (script.md, ## S13; one voiceover block each):
0. Tracker F3 (note "read in reverse"), lref 22, 24. CODE(cli.sh: 9-14) along the bottom; V6
   GpuSwitchboard above it, all three switches off. Each switch is named while its source line is
   barred (accelerator: lines 12-13; image: line 9; quota: the region, line 14). On "all three" the
   switches flip GREEN one by one and the T4 chip lights.
1. The quota page from S07 (schematic, `illustration`) flashes under the quota switch; then a laptop
   strip, tracker F3 · extra: the manifest loop of laptop/09 (typed, soft-wrapped) and 09:2-7, the
   sizes tagged `at the time of recording` (on screen, not spoken).
2. CODE(cli.sh: 21-37) as two 12-line windows: 22-27 uncomment (YELLOW, the '#' fade), 30-37 comment
   out (GREY). Then the V6 replay with both blocks live: two tiles with the same name, RED chip.
3. A GREY honest card: no GPU quota, no account here; the GPU block runs the same create command
   that failed in scene 10; nothing new to show, nothing faked.
4. The board, all three on, chip lit; the GOLD cost tag on the T4 chip (no amounts).
5. CODE(cli.sh: 30-37) with accelerator-type drawn into line 36 (GREY dashed, "a thought
   experiment"); PONDER 6 s.
6. The answer: CODE(cli.sh: 31) YELLOW; V6 replay with the image switch on tf-cpu: the T4 sits dark
   in the slot while the GOLD meter runs; the log line `GPU Available:  []` (task.py:67,
   `illustration`); chip "exercise 5". Fade out.

Deviation: CODE(cli.sh: 21-27) and CODE(cli.sh: 30-37) cannot stand side by side (10.6 and 9.4
units wide at 20 pt) nor stacked under the board; beat 0 shows CODE(cli.sh: 9-14) under the board,
and the GPU block against the CPU block is the scrolling CODE(cli.sh: 21-37) of beat 2.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, JOB_NAME, err_chip, IMAGE, INK, NARRATION, P_LAPTOP, REGION, SAY_COUNT, SWITCHES,
                    TURN, GpuSwitchboard, capture, card, chip, check_mark, code, code_span, console, cost_tag,
                    dashed_chip, each, extra_row, flash_tag, grey_chip, illustration_tag, label, line_bar, lref,
                    mono, on_bar, out, ponder, ring, term, time_row, track, tracker_f, type_cmd)
from explainer import style as S

SAY = NARRATION["S13"]
PONDER_CPU_T4 = "You add accelerator-type to the CPU block.\nThe job runs; its log says\nGPU Available:  []. Why?"
C26 = ("--worker-pool-spec=", "accelerator-type", "$ACCELERATOR_TYPE,")
CUT31 = ('"', "tf-cpu")
CUT36 = "machine-type=$MACHINE_TYPE,"
ADDED = "accelerator-type=$ACCELERATOR_TYPE,accelerator-count=$ACCELERATOR_COUNT,"   # cli.sh:26's words


def raised_board(on=()) -> GpuSwitchboard:
    """V6 placed 0.3 higher (before it plays: riders follow) so a panel or strip fits beneath."""
    sb = GpuSwitchboard(on=on)
    sb.shift(UP * 0.3)
    return sb


def put_top(m, y: float = 2.75):
    return m.shift(np.array([-m.get_center()[0], y - m.get_top()[1], 0]))


def hashes(p, ks):
    """The '#' glyph that comments out each line k of code panel p."""
    return [code_span(p.code, k, "#") for k in ks]


def two_tiles() -> VGroup:
    """V6's twin replay, built locally: GpuSwitchboard.twin()'s 4.2-wide tiles are narrower than the
    job name at 20 pt (the name overhangs both frames). Same parts: .tiles (two BLUE tiles with the
    same name) .chip (RED 'two jobs, two bills')."""
    tiles = VGroup()
    for _ in range(2):
        t = mono(JOB_NAME, 20, INK)
        fr = RoundedRectangle(width=t.width + 0.5, height=1.0, corner_radius=0.14, stroke_color=CLOUD,
                              stroke_width=3).set_fill(CLOUD, 0.07)
        tiles.add(VGroup(fr, t.move_to(fr)))
    tiles.arrange(RIGHT, buff=0.35)
    e = err_chip("two jobs, two bills", mono_font=False).next_to(tiles, DOWN, buff=0.2)
    g = VGroup(tiles, e)
    g.tiles, g.chip = tiles, e
    return g


class ThreeSwitches(VoiceScene):
    def keep_only(self, *keep, run_time=0.6, shift=UP * 0.2):
        fam = {id(x) for k in keep for x in k.get_family()}
        gone = [m for m in self.mobjects if not any(id(x) in fam for x in m.get_family())]
        if gone:
            self.play(FadeOut(Group(*gone), shift=shift), run_time=run_time)
            self.remove(*gone)

    def construct(self):
        assert len(SAY) == SAY_COUNT["S13"] == 7, len(SAY)
        c09 = capture("09")

        # ========================================================== 0. three switches must agree
        tr = tracker_f(3, note_="read in reverse")
        ref = lref("22, 24")
        assert tr.caption.get_right()[0] < ref.get_left()[0]
        assert tracker_f(3, extra=True, note_="read in reverse").caption.get_right()[0] < ref.get_left()[0]
        sb = raised_board()
        p9 = code("cli.sh", 9, 14, font_size=20, cuts={9: ('"', "tf-gpu"), 14: '"us-central1"'})
        p9.shift(np.array([-p9.get_center()[0], -0.73 - p9.get_top()[1], 0]))
        assert p9.get_bottom()[1] > -3.6 and sb.get_bottom()[1] > p9.get_top()[1] + 0.05, (p9.get_bottom(), sb.get_bottom())
        acc_bars = VGroup(line_bar(p9.code, 3, TURN, 0.22), line_bar(p9.code, 4, TURN, 0.22))
        img_bar = line_bar(p9.code, 0, TURN, 0.22)
        reg_bar = line_bar(p9.code, 5, TURN, 0.22)
        sw = sb.switches

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(p9, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("what would it take")
            self.play(FadeIn(sb, shift=DOWN * 0.15), run_time=0.8)
            vo.wait_until("Three switches must agree")
            self.play(each([sw[k].title_ for k in SWITCHES], INK, scale=1.15, lag=0.25), run_time=1.2)
            vo.wait_until("The accelerator")
            self.play(FadeIn(acc_bars), Indicate(sw["accelerator"].title_, color=TURN, scale_factor=1.15), run_time=0.6)
            self.play(Indicate(p9.code.code_lines[3], color=TURN, scale_factor=1.04), run_time=0.6)
            vo.wait_until("The image")
            self.play(FadeOut(acc_bars), FadeIn(img_bar), Indicate(sw["image"].title_, color=TURN, scale_factor=1.15),
                      run_time=0.6)
            vo.wait_until("with CUDA")
            self.play(Indicate(code_span(p9.code, 0, "tf-gpu"), color=IMAGE, scale_factor=1.15), run_time=0.6)
            vo.wait_until("And the quota")
            self.play(FadeOut(img_bar), FadeIn(reg_bar), Indicate(sw["quota"].title_, color=TURN, scale_factor=1.15),
                      run_time=0.6)
            vo.wait_until("in this region")
            self.play(Indicate(code_span(p9.code, 5, '"us-central1"'), color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("only when all three")
            self.play(FadeOut(reg_bar), run_time=0.3)
            for k in SWITCHES:
                self.play(sb.toggle(k, run_time=0.45))
            self.play(sb.chip_on())

        # ========================================================== 1. the quota page; the images are still served
        qp = console(("IAM & Admin", "Quotas"), 7.4, 2.1)
        qp.move_to([1.4 + 0.6, -2.0, 0])
        q_ill = illustration_tag().move_to(qp.frame.get_corner(UR) + np.array([-1.2, -0.32, 0]))
        q_ill.shift(LEFT * (q_ill.width / 2 - 1.0))
        t4 = label("Custom model training Nvidia T4 GPUs per region", 20, INK)
        reg = VGroup(Square(0.26, stroke_color=TURN, stroke_width=2.5), mono(REGION, 20, TURN)).arrange(RIGHT, buff=0.2)
        reg[0].add(check_mark(0.22, TURN, 4).move_to(reg[0]))
        qcol = VGroup(t4, reg).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        qcol.move_to(qp.content).align_to(qp.content, LEFT).shift(RIGHT * 0.25)
        from7 = grey_chip("scene 7's request").next_to(qp.frame, LEFT, buff=0.3)
        quota_page = VGroup(qp, q_ill, qcol)
        link = Line(sw["quota"].value.get_bottom() + DOWN * 0.08, qp.frame.get_top(), color=TURN, stroke_width=3)
        assert qp.get_bottom()[1] > -3.5 and qp.get_right()[0] < 6.5 and from7.get_left()[0] > -6.5
        assert q_ill.get_left()[0] > qp.crumbs.get_right()[0] + 0.2, (q_ill.get_left(), qp.crumbs.get_right())

        t = term(P_LAPTOP, rows=12, size=20)   # the one-liner folds into 6 rows: no strip holds it
        assert t.box.get_top()[1] < 2.75, t.box.get_top()
        ex = on_bar(t, extra_row())
        tm = time_row()
        tm.move_to([ex.get_left()[0] - 0.2 - tm.width / 2, ex.get_center()[1], 0])
        o09 = [c09.line(2), (c09.line(3), S.GREY), (c09.line(4), IMAGE), (c09.line(5), S.GREY),
               (c09.line(6), IMAGE), (c09.line(7), S.GREY)]

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(p9, shift=DOWN * 0.2), run_time=0.5)
            self.remove(p9)
            self.play(Create(link), FadeIn(quota_page, shift=UP * 0.15), run_time=0.7)
            self.play(FadeIn(from7, shift=RIGHT * 0.15), Indicate(qcol[0], color=TURN, scale_factor=1.05), run_time=0.7)
            self.play(Indicate(reg[1], color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("An extra check")
            self.play(FadeOut(VGroup(link, quota_page, from7, sb, sb.chip), shift=UP * 0.2),
                      track(tr, 3, extra=True, note_="read in reverse"), run_time=0.5)
            self.remove(link, quota_page, from7, sb, sb.chip)
            self.play(FadeIn(t), FadeIn(ex), run_time=0.5)
            type_cmd(self, t, c09.cmd, type_time=1.8, soft=True)
            vo.wait_until("still serves both GPU images")
            rows09 = out(self, t, o09, run_time=1.0, lag=0.1)
            self.play(FadeIn(tm, shift=LEFT * 0.15), run_time=0.4)
            self.play(each([rows09[2], rows09[4]], IMAGE, scale=1.04, lag=0.3), run_time=1.0)

        # ========================================================== 2. uncomment the GPU block, comment out the CPU block
        w1 = put_top(code("cli.sh", 21, 32, font_size=20, cuts={26: C26, 31: CUT31}), 2.4)
        w2 = put_top(code("cli.sh", 26, 37, font_size=20, cuts={26: C26, 31: CUT31, 36: CUT36}), 2.4)
        y1 = VGroup(*[line_bar(w1.code, k, TURN, 0.22) for k in range(1, 7)])
        h1 = hashes(w1, range(1, 7))
        un = chip("uncomment · lines 22–27", TURN, size=20)
        un.next_to(w1, UP, buff=0.08).align_to(w1, RIGHT)
        y2 = VGroup(*[line_bar(w2.code, k, TURN, 0.22) for k in (0, 1)])
        h2 = hashes(w2, (0, 1))
        g2 = VGroup(*[line_bar(w2.code, k, S.GREY, 0.22) for k in range(4, 12)])
        co = grey_chip("comment out · lines 30–37")
        co.next_to(w2, UP, buff=0.08).align_to(w2, RIGHT)
        for m_ in (un, co):
            assert m_.get_top()[1] < ref.get_bottom()[1] - 0.05, (m_.get_top(), ref.get_bottom())
        tw = two_tiles()
        tw.move_to([0, 0.6, 0])
        assert tw.get_left()[0] > -6.5 and tw.get_right()[0] < 6.5, tw.width

        with self.voiceover(SAY[2]) as vo:
            self.play(track(tr, 3, note_="read in reverse"),
                      FadeOut(VGroup(t, *t.lines, ex, tm), shift=DOWN * 0.2), run_time=0.6)
            self.remove(t, *t.lines, ex, tm)
            self.play(FadeIn(w1, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("uncomment the GPU block")
            self.play(FadeIn(y1), FadeIn(un, shift=LEFT * 0.15), run_time=0.5)
            self.play(*[h.animate.set_opacity(0.15) for h in h1], run_time=0.7)
            vo.wait_until("comment out the CPU block")
            self.play(FadeOut(VGroup(w1, y1, un), shift=UP * 0.3), run_time=0.4)
            self.remove(w1, y1, un)
            self.play(FadeIn(w2, shift=UP * 0.3), run_time=0.4)
            for h in h2:
                h.set_opacity(0.15)
            self.play(FadeIn(y2), FadeIn(g2), FadeIn(co, shift=LEFT * 0.15), run_time=0.5)
            self.play(*[w2.code.code_lines[k].animate.set_opacity(0.4) for k in range(4, 12)], run_time=0.7)
            vo.wait_until("Leave both active")
            self.play(FadeOut(VGroup(w2, y2, g2, co), shift=UP * 0.2), run_time=0.5)
            self.remove(w2, y2, g2, co)
            self.play(FadeIn(tw.tiles[0], shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("two jobs with the same name")
            self.play(FadeIn(tw.tiles[1], shift=LEFT * 0.3), run_time=0.7)   # a sliding copy garbled both names
            self.play(FadeIn(tw.chip, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(tw.chip.text, color=ERR, scale_factor=1.1), run_time=0.6)

        # ========================================================== 3. the honest card
        honest = card(["no GPU quota, no account here",
                       "the GPU block runs the same gcloud ai custom-jobs create",
                       "that failed in scene 10",
                       "nothing new to show, nothing faked"], size=24)
        honest.move_to([0, 0.4, 0])
        cmd_glyphs = honest.body[1]

        with self.voiceover(SAY[3]) as vo:
            self.keep_only(tr, ref)
            self.play(FadeIn(honest, scale=0.97), run_time=0.6)
            vo.wait_until("the same way as our CPU submit did")
            self.play(Indicate(VGroup(cmd_glyphs, honest.body[2]), color=INK, scale_factor=1.04), run_time=0.8)
            vo.wait_until("with no active account")
            self.play(Indicate(honest.body[0], color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("nothing new to show")
            self.play(Indicate(honest.body[3], color=INK, scale_factor=1.06), run_time=0.8)

        # ========================================================== 4. GOLD: a GPU adds to the bill
        sb4 = GpuSwitchboard(on=SWITCHES)
        bill = cost_tag("a GPU adds to the bill while it is attached, used or not\nsee the Vertex AI pricing page")
        sx = sb4.slot.get_center()[0]
        bill.move_to([sx + 1.05 - bill.width / 2, -2.0, 0])
        lead = Line([sx, bill.get_top()[1], 0], [sx, sb4.slot.get_bottom()[1] - 0.45, 0], color=COST, stroke_width=3)
        assert bill.get_right()[0] < 6.5 and bill.get_left()[0] > -6.5, (bill.get_left(), bill.get_right())

        with self.voiceover(SAY[4]) as vo:
            self.keep_only(tr, ref)
            self.play(FadeIn(sb4, shift=DOWN * 0.15), run_time=0.6)
            self.play(sb4.chip_on())
            vo.wait_until("a GPU adds to the bill")
            self.play(Create(lead), FadeIn(bill, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("for as long as it is attached")
            flash_tag(self, bill, COST)

        # ========================================================== 5. a thought experiment; PONDER
        p30 = put_top(code("cli.sh", 30, 37, font_size=20, cuts={31: CUT31, 36: CUT36}))
        b36 = line_bar(p30.code, 6, TURN, 0.22)
        add = dashed_chip(ADDED, S.GREY, mono_font=True)
        add.move_to([0, p30.get_bottom()[1] - 0.75, 0])
        caret = Arrow(add.get_top(), [code_span(p30.code, 6, CUT36).get_right()[0], p30.code.code_lines[6].get_bottom()[1], 0],
                      buff=0.08, color=S.GREY, stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.3)
        thought = grey_chip("a thought experiment").next_to(add, DOWN, buff=0.25)
        assert add.get_left()[0] > -6.55 and add.get_right()[0] < 6.55, add.width
        assert thought.get_bottom()[1] > -3.5

        with self.voiceover(SAY[5]) as vo:
            self.keep_only(tr, ref)
            self.play(FadeIn(p30, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("You add the accelerator")
            self.play(FadeIn(b36), run_time=0.3)
            self.play(FadeIn(add, shift=UP * 0.2), GrowArrow(caret), FadeIn(thought, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("The job runs")
            self.play(Indicate(add.text, color=INK, scale_factor=1.05), run_time=0.7)
        pc = ponder(self, PONDER_CPU_T4, seconds=6)

        # ========================================================== 6. the answer: a dark T4, still billed
        sb6 = raised_board(on=("accelerator", "quota"))
        p31 = code("cli.sh", 31, font_size=20, cuts={31: CUT31})
        p31.shift(np.array([-4.5 - p31.get_left()[0] + 0.0, -0.8 - p31.get_top()[1], 0]))
        b31 = line_bar(p31.code, 0, TURN, 0.22)
        log_lbl = label("task.py · line 67 prints", 20, S.GREY)
        log_txt = mono("GPU Available:  []", 22, INK)
        log_box = RoundedRectangle(width=log_txt.width + 0.5, height=0.55, corner_radius=0.08, stroke_color=S.GREY,
                                   stroke_width=2).set_fill(S.GREY_DARKER, 1)
        log_txt.move_to(log_box)
        log_row = VGroup(log_lbl, VGroup(log_box, log_txt)).arrange(RIGHT, buff=0.3)
        log_row.next_to(p31, DOWN, buff=0.35).align_to(p31, LEFT)
        log_ill = illustration_tag().next_to(log_row, RIGHT, buff=0.3)
        ex5 = chip("exercise 5", TURN, size=20).next_to(log_ill, RIGHT, buff=0.4)
        assert ex5.get_right()[0] < 6.5 and log_row.get_bottom()[1] > -3.5, (ex5.get_right(), log_row.get_bottom())
        assert p31.get_right()[0] < 6.5
        img = sb6.switches["image"]

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(pc, p30, b36, add, caret, thought)), run_time=0.5)
            self.remove(pc, p30, b36, add, caret, thought)
            self.play(FadeIn(sb6, shift=DOWN * 0.15), FadeIn(p31, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(b31), run_time=0.3)
            vo.wait_until("which has no CUDA")
            img_ring = ring(img.value, TURN, buff=0.1)
            self.play(Create(img_ring), Indicate(code_span(p31.code, 0, "tf-cpu"), color=IMAGE, scale_factor=1.15),
                      run_time=0.7)
            vo.wait_until("The T4 is attached")
            self.play(sb6.chip_dark())
            vo.wait_until("idle")
            self.play(FadeIn(log_row, shift=UP * 0.15), FadeIn(log_ill), run_time=0.6)
            vo.wait_until("and still billed")
            self.play(Circumscribe(sb6.meter, color=COST, buff=0.08), run_time=0.8)
            vo.wait_until("Exercise 5")
            self.play(FadeIn(ex5, shift=LEFT * 0.15), run_time=0.5)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
