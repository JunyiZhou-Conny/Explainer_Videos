"""S14 · Two GPUs, one model (AC215 L13) — the optional multi-GPU step, picture before code.

Beats (script.md, ## S14; one voiceover block each):
0. No tracker; lref 26–30 for the whole scene. V7 opens with slide 27's ladder (One Device · Mirrored
   'you are here' · Multi Worker Mirrored GREY dashed), row by row. CODE(package/trainer/task.py: 60)
   under it, tied to the first row, with the kind GREY chip "only counts replicas · the model is built
   outside any scope".
1. Still no tracker. V7 MirroredReplicas: the n1-standard-32 box, two T4 cards with identical replicas;
   the global batch of 64 splits 32 + 32; gradients rise, all-reduce averages, both replicas take the
   same step. Then `with strategy.scope():` around model · optimizer · compile; the variables split
   into one synced copy per GPU; a model built outside stays single, GREY 'not mirrored'.
2. Tracker G1. CODE(cli-multi-gpu.sh: 4–16) as two 12-line windows at 20 pt: line 6 n1-standard-32,
   lines 11–12 T4 × 2, line 10 trainer.task_multi_gpu, line 16 --epochs=5, line 8 tf-gpu.2-14 with a
   kind chip + `erratum` tag; ▶ your turn.
3. Tracker G2. CODE(task_multi_gpu.py: 286–301) then (: 303–321) as 12-line windows, the slide's three
   call-outs (BLUE create strategy 287–289 · GREEN batch size 293 (+300) with the num_workers chip · RED
   build and compile in the scope 304–321), one per sentence; a text-free V7 thumbnail beside the code;
   CODE(: 338–343) with GREY 'unchanged'; ▶ your turn.
4. The two GPUs, --batch_size=32 and a stack of 936 training tiles; PONDER 8 s.
5. The answer: CODE(: 293) and '= 32 × 2 = 64'; the 936 tiles fall into 15 batches of 64 (14 full + 40);
   the first batch splits 32 + 32; the two config chips of 324–334 (no values); two caveat cards.
6. G3: GREY quota card over the quota page (illustration); the GOLD cost tag on the n1-standard-32
   two-T4 box (no amounts). G4: README card (line 170), cockpit prompt with the fresh-cockpit chip,
   sh cli-multi-gpu.sh → laptop/50: 43–44, 44 RED; ▶ your turn + 'optional · only with GPU quota';
   slide 30 as one GREY line, not spoken. Fade out.

Deviation: the V7 thumbnail in beat 3 is a text-free redraw (two replica cards and the PINK link), not
the full set piece scaled down (scaling text below 1.0 trips SMALL). The twin variables of beat 1 are
animated locally (the set piece's ReplacementTransform smears 'variables' across both chips).
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, FUTURE, INK, MACHINE_MULTI, MULTI_EDITS, NARRATION, OWNED, P_COCKPIT,
                    ROUTE, SAY_COUNT, SPLIT_COUNTS, TOOL, TURN, MirroredReplicas, arrow, beside, capture, card,
                    chip, code, code_span, console, container_note, cost_tag, each, erratum_tag, flag_chip,
                    flash_tag, grey_chip, illustration_tag, istep, label, line_bar, lref, mono, network_glyph,
                    note, out, pin, ponder, readme_card, ring, t4_chip, tag, term, track, tracker_g, turn_row,
                    your_turn)
from explainer import style as S

SAY = NARRATION["S14"]
PONDER_STEPS = "Two GPUs, --batch_size=32, 936 training\nimages. Steps per epoch? Images per GPU\nper step?"
MG = "cli-multi-gpu.sh"
TMG = "package/trainer/task_multi_gpu.py"
CUTS_MG = {8: ('"', "tf-gpu"), 13: '"us-central1"', 15: "mobilenetv2,"}
CUTS_MG2 = {**CUTS_MG, 16: ("mobilenetv2,", "--epochs", "--epochs=5,")}
N_TRAIN = int(SPLIT_COUNTS[0])            # 936 (notebook split counts, ASSETS)
GLOBAL = 64                               # task_multi_gpu.py:293 with --batch_size=32 and two replicas


def put_top(m, y: float = 2.6, x: float = 0.0):
    """Centre m at x with its top at y."""
    return m.shift(np.array([x - m.get_center()[0], y - m.get_top()[1], 0]))


def mini_replicas() -> VGroup:
    """V7 as a text-free thumbnail: two replica cards (same network, same colours) and the PINK link."""
    cards = VGroup()
    for _ in range(2):
        fr = RoundedRectangle(width=0.95, height=0.62, corner_radius=0.08, stroke_color=CLOUD,
                              stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        net = network_glyph(S.TEAL, net_w=0.6, net_h=0.45).move_to(fr)
        cards.add(VGroup(fr, net))
    cards.arrange(RIGHT, buff=0.35)
    y = cards.get_top()[1] + 0.18
    link = Line([cards[0].get_center()[0], y, 0], [cards[1].get_center()[0], y, 0], color=ROUTE, stroke_width=5)
    ups = VGroup(*[Line([c.get_center()[0], c.get_top()[1], 0], [c.get_center()[0], y, 0], color=ROUTE,
                        stroke_width=3) for c in cards])
    box_ = RoundedRectangle(width=cards.width + 0.4, height=cards.height + 0.6, corner_radius=0.12,
                            stroke_color=CLOUD, stroke_width=2.5).set_fill(CLOUD, 0.05)
    box_.move_to(VGroup(cards, link)).shift(DOWN * 0.02)
    return VGroup(box_, cards, ups, link)


def tile_stack(n: int, cols: int = 36, side: float = 0.07, buff: float = 0.02) -> VGroup:
    """n blank WHITE tiles in a block (the training images; no pictures)."""
    tiles = VGroup(*[Rectangle(width=side, height=side, stroke_width=0).set_fill(INK, 0.8) for _ in range(n)])
    tiles.arrange_in_grid(rows=(n + cols - 1) // cols, cols=cols, buff=buff)
    return tiles


def batch_targets(n: int, per: int = GLOBAL, cols: int = 8, side: float = 0.07, buff: float = 0.02,
                  gap: float = 0.12, y: float = 0.45):
    """Where tile i lands when n tiles are cut into batches of `per` (8 × 8 blocks in one row, the last
    one partial, top-aligned). Returns (points, block frames)."""
    nb = (n + per - 1) // per
    pitch = side + buff
    bw = cols * pitch - buff
    total = nb * bw + (nb - 1) * gap
    x0 = -total / 2
    top = y + bw / 2
    pts = []
    for i in range(n):
        b, r, c = i // per, (i % per) // cols, i % cols
        pts.append(np.array([x0 + b * (bw + gap) + c * pitch + side / 2, top - r * pitch - side / 2, 0]))
    frames = VGroup(*[Rectangle(width=bw + 0.08, height=bw + 0.08, stroke_color=S.GREY, stroke_width=1.5)
                      .move_to([x0 + b * (bw + gap) + bw / 2, y, 0]) for b in range(nb)])
    return pts, frames


def bars(p, ks, color, opacity: float = 0.22) -> VGroup:
    return VGroup(*[line_bar(p.code, k, color, opacity) for k in ks])


class TwoGpusOneModel(VoiceScene):
    def keep_only(self, *keep, run_time=0.6, shift=UP * 0.2):
        fam = {id(x) for k in keep for x in k.get_family()}
        gone = [m for m in self.mobjects if not any(id(x) in fam for x in m.get_family())]
        if gone:
            self.play(FadeOut(Group(*gone), shift=shift), run_time=run_time)
            self.remove(*gone)

    def construct(self):
        assert len(SAY) == SAY_COUNT["S14"] == 7, len(SAY)
        c50 = capture("50")
        ref = lref("26–30")

        # ========================================================== 0. slide 27's ladder; task.py only counts
        ld = MirroredReplicas.ladder()
        ld.shift(UP * (2.6 - ld.get_top()[1]))
        rows = ld.rows
        p60 = code("package/trainer/task.py", 60)
        p60.shift(np.array([rows.get_left()[0] - p60.get_left()[0], -0.75 - p60.get_top()[1], 0]))
        only = grey_chip("only counts replicas · the model is built outside any scope")
        only.next_to(p60, DOWN, buff=0.25).align_to(p60, LEFT)
        tie = arrow(np.array([rows.get_left()[0] - 0.1, p60.get_center()[1], 0]),
                    np.array([rows.get_left()[0] - 0.1, rows[0].get_center()[1], 0]), S.GREY, arc=-1.2)
        assert ld.get_right()[0] < 6.5 and only.get_bottom()[1] > -3.5 and tie.get_left()[0] > -6.5, \
            (ld.get_right(), only.get_bottom(), tie.get_left())

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), run_time=0.5)
            vo.wait_until("one machine with one GPU")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("one machine with several")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("and several machines")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("Today is the middle one")
            self.play(FadeIn(ld.here, shift=LEFT * 0.2), run_time=0.5)
            flash_tag(self, ld.here, TURN)
            self.play(Indicate(rows[1][2], color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("The single-GPU trainer also creates one")
            self.play(FadeIn(p60, shift=UP * 0.15), run_time=0.6)
            self.play(Create(tie), Indicate(rows[0][2], color=INK, scale_factor=1.1), run_time=0.8)
            self.play(Indicate(code_span(p60.code, 0, "MirroredStrategy"), color=TOOL, scale_factor=1.1), run_time=0.6)
            vo.wait_until("but only to count GPUs")
            self.play(FadeIn(only, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(only.text, color=INK, scale_factor=1.05), run_time=0.7)

        # ========================================================== 1. the picture: split, gradients, all-reduce, step
        mr = MirroredReplicas()
        g0, g1 = mr.gpus
        sc = MirroredReplicas.scope()
        twins, tlink = sc.twin_chips, sc.twin_link
        tpos = [twins[0].get_center().copy(), twins[1].get_center().copy()]

        with self.voiceover(SAY[1]) as vo:
            self.keep_only(ref)
            vo.wait_until("Each GPU holds")
            self.play(FadeIn(mr.box), FadeIn(g0, shift=UP * 0.15), FadeIn(g1, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("called a replica")
            self.play(each([g0.net, g1.net], INK, scale=1.12, lag=0.3), run_time=0.9)
            vo.wait_until("A global batch of 64")
            self.play(FadeIn(mr.batch, shift=RIGHT * 0.2), FadeIn(mr.batch_label), run_time=0.7)
            self.add(mr)
            vo.wait_until("splits into two halves")
            self.play(mr.split_batch(run_time=1.4))
            vo.wait_until("Each GPU computes gradients")
            self.play(mr.grads(run_time=1.0))
            vo.wait_until("The two are averaged")
            self.play(mr.allreduce(run_time=1.2))
            vo.wait_until("and both copies take the same step")
            self.play(*[a.animate.set_color(S.YELLOW) for a in mr.up], run_time=0.4)
            self.play(mr.step(S.YELLOW, run_time=1.0))
            vo.wait_until("Variables created inside the scope")
            self.play(FadeOut(mr, shift=DOWN * 0.2), run_time=0.5)
            self.remove(mr)
            self.play(FadeIn(sc, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("are mirrored")
            for t_, p_ in zip(twins, tpos):
                t_.move_to(sc.var)
            self.play(FadeOut(sc.var), FadeIn(twins[0]), FadeIn(twins[1]), run_time=0.4)
            sc.remove(sc.var)
            self.play(twins[0].animate.move_to(tpos[0]), twins[1].animate.move_to(tpos[1]), run_time=0.7)
            self.play(Create(tlink), run_time=0.4)
            vo.wait_until("a model built outside")
            self.play(FadeIn(sc.outside, shift=LEFT * 0.2), run_time=0.6)
            self.play(Indicate(sc.outside[1].text, color=INK, scale_factor=1.08), run_time=0.6)

        # ========================================================== 2. G1: review cli-multi-gpu.sh
        tr = tracker_g(1)
        assert tr.get_right()[0] < ref.get_left()[0] - 0.2, (tr.get_right(), ref.get_left())
        w1 = put_top(code(MG, 4, 15, font_size=20, cuts=CUTS_MG))
        w2 = put_top(code(MG, 5, 16, font_size=20, cuts=CUTS_MG2))
        yt2 = your_turn()
        yt2.move_to([w1.get_right()[0] - yt2.width / 2, w1.get_bottom()[1] - 0.45, 0])
        slip = grey_chip("older than cli.sh's tf-cpu.2-17")
        er = erratum_tag()
        slip_row = VGroup(slip, er).arrange(RIGHT, buff=0.25)
        slip_row.move_to([w2.get_left()[0] + slip_row.width / 2, w2.get_bottom()[1] - 0.45, 0])
        assert slip_row.get_right()[0] < yt2.get_left()[0] - 0.2 and yt2.get_bottom()[1] > -3.5

        with self.voiceover(SAY[2]) as vo:
            self.keep_only(ref, run_time=0.5)
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(w1, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("pause and open it")
            self.play(FadeIn(yt2, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt2, TURN)
            vo.wait_until("It asks for one n1-standard-32")
            b6 = bars(w1, [2], TURN)
            self.play(FadeIn(b6), Indicate(code_span(w1.code, 2, MACHINE_MULTI), color=TURN, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("with two T4s")
            b11 = bars(w1, [7, 8], TURN)
            self.play(FadeOut(b6), FadeIn(b11), run_time=0.4)
            self.play(each([code_span(w1.code, 7, "NVIDIA_TESLA_T4"), code_span(w1.code, 8, "2")], TURN,
                           scale=1.15, lag=0.3), run_time=0.8)
            b10 = bars(w1, [6], TOOL)
            self.play(FadeOut(b11), FadeIn(b10), Indicate(code_span(w1.code, 6, "trainer.task_multi_gpu"), color=TOOL,
                                                          scale_factor=1.08), run_time=0.7)
            vo.wait_until("for 5 epochs")
            self.play(FadeOut(VGroup(w1, b10), shift=UP * 0.2), FadeIn(w2, shift=UP * 0.2), run_time=0.5)
            self.remove(w1, b10)
            b16 = bars(w2, [11], TURN)
            self.play(FadeIn(b16), Indicate(code_span(w2.code, 11, "--epochs=5"), color=TURN, scale_factor=1.15),
                      run_time=0.7)
            vo.wait_until("A small slip")
            b8 = bars(w2, [3], S.GREY, 0.3)
            self.play(FadeOut(b16), FadeIn(b8), run_time=0.4)
            self.play(Indicate(code_span(w2.code, 3, "tf-gpu.2-14.py310"), color=INK, scale_factor=1.1),
                      FadeIn(slip_row, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("where cli.sh uses 2.17")
            self.play(Indicate(slip.text, color=INK, scale_factor=1.06), run_time=0.7)

        # ========================================================== 3. G2: task_multi_gpu.py, the three edits
        top_ = 1.25
        u1 = put_top(code(TMG, 286, 297, font_size=20), top_)
        u2 = put_top(code(TMG, 290, 301, font_size=20), top_)
        u3 = put_top(code(TMG, 303, 314, font_size=20), top_)
        u4 = put_top(code(TMG, 310, 321, font_size=20), top_)
        fit = put_top(code(TMG, 338, 343, font_size=20), 0.6, -1.0)
        same = grey_chip("unchanged").next_to(fit, RIGHT, buff=0.35)
        thumb = mini_replicas().move_to([4.95, 2.05, 0])
        calls = [tag(s, c) for s, c in MULTI_EDITS]
        for c_ in calls:
            c_.move_to([-6.3 + c_.width / 2, 2.25, 0])
        yt3 = your_turn().move_to([-6.3 + your_turn().width / 2, 2.25, 0])
        nw = grey_chip("num_workers counts GPU replicas here, not machines")
        nw.move_to([-6.3 + nw.width / 2, 1.62, 0])
        for m_ in (u1, u2, u3, u4):
            assert m_.get_bottom()[1] > -3.5 and m_.get_right()[0] < 6.5, (m_.get_bottom(), m_.get_right())
        assert nw.get_bottom()[1] > top_ + 0.03 and nw.get_right()[0] < thumb.get_left()[0] - 0.2, \
            (nw.get_bottom(), nw.get_right(), thumb.get_left())
        assert thumb.get_top()[1] < 2.8 and thumb.get_right()[0] < 6.5, (thumb.get_top(), thumb.get_right())
        assert calls[2].get_right()[0] < thumb.get_left()[0] - 0.2
        assert same.get_right()[0] < 6.5

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(w2, b8, slip_row, yt2), shift=UP * 0.2), track(tr, 2), run_time=0.6)
            self.remove(w2, b8, slip_row, yt2)
            self.play(FadeIn(u1, shift=UP * 0.15), FadeIn(thumb, scale=1.6), run_time=0.7)
            vo.wait_until("pause and open it")
            self.play(FadeIn(yt3, shift=RIGHT * 0.15), run_time=0.4)
            flash_tag(self, yt3, TURN)
            vo.wait_until("These are the lecture's three changes")
            self.play(FadeOut(yt3), run_time=0.3)
            self.remove(yt3)
            self.play(Indicate(thumb[3], color=ROUTE, scale_factor=1.1), run_time=0.6)
            vo.wait_until("It creates the mirrored strategy")
            bb = bars(u1, [1, 2, 3], CLOUD)
            self.play(FadeIn(calls[0], shift=RIGHT * 0.15), FadeIn(bb), run_time=0.5)
            self.play(Indicate(code_span(u1.code, 1, "tf.distribute.MirroredStrategy()"), color=CLOUD,
                               scale_factor=1.06), run_time=0.7)
            vo.wait_until("It multiplies the batch size")
            bg = bars(u1, [7], OWNED)
            self.play(FadeOut(calls[0]), FadeOut(bb), FadeIn(calls[1], shift=RIGHT * 0.15), FadeIn(bg), run_time=0.5)
            self.remove(calls[0], bb)
            self.play(Indicate(code_span(u1.code, 7, "args.batch_size * num_workers"), color=OWNED, scale_factor=1.06),
                      FadeIn(nw, shift=UP * 0.1), run_time=0.8)
            self.play(FadeOut(VGroup(u1, bg)), FadeIn(u2), run_time=0.5)
            self.remove(u1, bg)
            bg2 = bars(u2, [3, 10], OWNED)
            self.play(FadeIn(bg2), Indicate(code_span(u2.code, 10, "global_batch_size"), color=OWNED,
                                            scale_factor=1.08), run_time=0.7)
            vo.wait_until("And it builds and compiles")
            self.play(FadeOut(VGroup(u2, bg2, nw, calls[1])), FadeIn(u3), FadeIn(calls[2], shift=RIGHT * 0.15),
                      run_time=0.6)
            self.remove(u2, bg2, nw, calls[1])
            br = bars(u3, range(1, 12), ERR, 0.14)
            self.play(FadeIn(br), Indicate(code_span(u3.code, 1, "with strategy.scope():"), color=ERR,
                                           scale_factor=1.06), run_time=0.7)
            self.play(Indicate(code_span(u3.code, 3, "build_mobilenet_model"), color=INK, scale_factor=1.06),
                      run_time=0.5)
            self.play(FadeOut(VGroup(u3, br)), FadeIn(u4), run_time=0.5)
            self.remove(u3, br)
            br2 = bars(u4, range(0, 12), ERR, 0.14)
            self.play(FadeIn(br2), run_time=0.3)
            self.play(each([code_span(u4.code, 5, "optimizer"), code_span(u4.code, 11, "model.compile")], INK,
                           scale=1.08, lag=0.3), run_time=0.8)
            vo.wait_until("Model fit is unchanged")
            self.play(FadeOut(VGroup(u4, br2, calls[2])), FadeIn(fit, shift=UP * 0.15), run_time=0.5)
            self.remove(u4, br2, calls[2])
            self.play(FadeIn(same, shift=LEFT * 0.15), Indicate(code_span(fit.code, 0, "model.fit("), color=INK,
                                                                scale_factor=1.1), run_time=0.7)

        # ========================================================== 4. PONDER: steps and images per GPU
        mr4 = MirroredReplicas()
        gpus = VGroup(*mr4.gpus).copy()
        gpus.move_to([3.2, 0.5, 0])
        stack = tile_stack(N_TRAIN).move_to([-3.9, 0.7, 0])
        n_lbl = note(f"{N_TRAIN} training images", INK, 22).next_to(stack, DOWN, buff=0.2)
        bs = flag_chip("--batch_size=32").next_to(gpus, DOWN, buff=0.3)
        assert gpus.get_right()[0] < 6.5 and stack.get_left()[0] > -6.5 and n_lbl.get_bottom()[1] > -3.5

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(fit, same, thumb)), run_time=0.5)
            self.remove(fit, same, thumb)
            vo.wait_until("Two GPUs")
            self.play(FadeIn(gpus, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("a batch size flag of 32")
            self.play(FadeIn(bs, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("and 936 training images")
            self.play(FadeIn(stack, lag_ratio=0.002), FadeIn(n_lbl), run_time=1.0)
        pc = ponder(self, PONDER_STEPS, seconds=8)

        # ========================================================== 5. the answer; two caveats
        p293 = code(TMG, 293, font_size=20)
        p293.shift(np.array([-6.3 - p293.get_left()[0], 2.7 - p293.get_top()[1], 0]))
        eq = mono(f"= 32 × 2 = {GLOBAL}", 22, TURN)
        eq.move_to([p293.get_right()[0] + 0.3 + eq.width / 2, p293.code.code_lines[0].get_center()[1], 0])
        pts, frames = batch_targets(N_TRAIN, y=0.3)
        n_full, rest = divmod(N_TRAIN, GLOBAL)
        assert (n_full, rest) == (14, 40)
        steps_b = Brace(frames, DOWN, buff=0.12, color=S.GREY)
        steps_l = note(f"{n_full + 1} steps · {n_full} full + the last one partial ({rest})", INK, 22)
        steps_l.next_to(steps_b, DOWN, buff=0.12)
        per_gpu = chip("32 per GPU per full step", TURN, size=20)
        cfg_head = note("wandb.init config · task_multi_gpu.py lines 324–334", S.GREY, 20)
        cfg = VGroup(cfg_head, flag_chip("batch_size"), flag_chip("global_batch_size")).arrange(RIGHT, buff=0.3)
        cfg.move_to([0, -2.85, 0])
        assert eq.get_right()[0] < 6.5 and frames.get_left()[0] > -6.5 and frames.get_right()[0] < 6.5, \
            (eq.get_right(), frames.get_left(), frames.get_right())
        assert cfg.get_left()[0] > -6.5 and cfg.get_right()[0] < 6.5, cfg.width
        cav1 = card(["learning_rate = 0.001 (:275) while the batch doubles"], size=26)
        cav2 = card(["2 GPUs ≠ 2× faster: start-up, image pull and download don't shrink"], size=26)
        cavs = VGroup(cav1, cav2).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([0, 0.4, 0])
        assert cavs.get_left()[0] > -6.5 and cavs.get_right()[0] < 6.5, cavs.width

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pc), FadeOut(VGroup(gpus, bs)), run_time=0.5)
            self.remove(pc, gpus, bs)
            self.play(FadeIn(p293, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("The global batch is 64")
            self.play(Write(eq), run_time=0.8)
            self.play(Indicate(code_span(p293.code, 0, "global_batch_size"), color=TURN, scale_factor=1.08), run_time=0.5)
            vo.wait_until("so 15 steps")
            self.play(FadeOut(n_lbl), *[t_.animate.move_to(pt) for t_, pt in zip(stack, pts)], run_time=1.4)
            self.remove(n_lbl)
            self.play(FadeIn(frames), GrowFromCenter(steps_b), FadeIn(steps_l, shift=UP * 0.1), run_time=0.7)
            self.play(Indicate(frames[-1], color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("and 32 images per GPU")
            first = VGroup(*stack[:GLOBAL])
            top32, bot32 = VGroup(*stack[:32]), VGroup(*stack[32:GLOBAL])
            self.play(top32.animate.set_fill(CLOUD, 1), bot32.animate.set_fill(S.TEAL, 1), run_time=0.6)
            per_gpu.next_to(first, UP, buff=0.3).align_to(frames[0], LEFT)
            self.play(FadeIn(per_gpu, shift=DOWN * 0.1), Create(ring(frames[0], TURN, buff=0.04)), run_time=0.6)
            self.play(FadeIn(cfg, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Two caveats")
            self.keep_only(tr, ref, run_time=0.5)
            self.play(FadeIn(cav1, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("The learning rate stays")
            self.play(Indicate(cav1.body[0], color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("And two GPUs are not twice as fast")
            self.play(FadeIn(cav2, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("because start-up")
            self.play(Indicate(cav2.body[0], color=INK, scale_factor=1.04), run_time=0.8)

        # ========================================================== 6. G3 quota + GOLD; G4 sh cli-multi-gpu.sh
        qp = console(("IAM & Admin", "Quotas"), 11.0, 3.0)
        qp.move_to([0, 0.6, 0])
        q_ill = illustration_tag().move_to(qp.frame.get_corner(UR) + np.array([-0.9, -0.32, 0]))
        q_ill.shift(LEFT * (q_ill.width / 2 - 0.6))
        qcard = card(["quota: 2 × T4 and 32 vCPUs of custom training, in your region"], size=24)
        qcard.move_to(qp.content)
        assert q_ill.get_left()[0] > qp.crumbs.get_right()[0] + 0.2 and qcard.width < qp.frame.width - 0.2, \
            (q_ill.get_left(), qp.crumbs.get_right(), qcard.width)

        bx_fr = RoundedRectangle(width=5.0, height=2.0, corner_radius=0.16, stroke_color=CLOUD,
                                 stroke_width=3).set_fill(CLOUD, 0.05).move_to([0, 1.3, 0])
        bx_t = mono(MACHINE_MULTI, 22, CLOUD).move_to(bx_fr.get_corner(DL) + np.array([0.2, 0.3, 0]), aligned_edge=LEFT)
        bx_v = note("32 vCPUs", INK, 22).next_to(bx_t, RIGHT, buff=0.5)
        chips2 = VGroup(t4_chip(True, 20, 0.6), t4_chip(True, 20, 0.6)).arrange(RIGHT, buff=0.6)
        chips2.move_to(bx_fr.get_center() + UP * 0.25)
        bigbox = VGroup(bx_fr, bx_t, bx_v, chips2)
        gold = cost_tag("the biggest machine of the lecture\n"
                        "check the Vertex AI pricing page before you press enter")
        gold.next_to(bx_fr, DOWN, buff=0.45)
        assert gold.get_bottom()[1] > -3.5 and gold.get_right()[0] < 6.5

        t = term(P_COCKPIT, rows=5)
        r170 = readme_card(170)
        r170.move_to([6.5 - r170.width / 2, 2.3, 0])
        fresh = container_note()
        fresh.next_to(r170, DOWN, buff=0.2).align_to(r170, RIGHT)
        opt = grey_chip("optional · only with GPU quota")
        opt.move_to([6.5 - opt.width / 2, t.box.get_top()[1] + 0.35, 0])
        s30 = note("bucket, key and package: already done · only the launch script changes", S.GREY, 20)
        s30.move_to([-6.4 + s30.width / 2, t.box.get_top()[1] + 0.35, 0])
        assert s30.get_right()[0] < opt.get_left()[0] - 0.2, (s30.get_right(), opt.get_left())
        assert fresh.get_bottom()[1] > opt.get_top()[1] + 0.1 and r170.get_top()[1] < 2.8, \
            (fresh.get_bottom(), opt.get_top(), r170.get_top())

        with self.voiceover(SAY[6]) as vo:
            self.keep_only(tr, ref, run_time=0.5)
            self.play(track(tr, 3), FadeIn(qp, shift=UP * 0.15), FadeIn(q_ill), run_time=0.6)
            self.play(FadeIn(qcard, scale=0.96), run_time=0.5)
            vo.wait_until("and 32 virtual CPUs")
            self.play(Indicate(qcard.body[0], color=INK, scale_factor=1.04), run_time=0.7)
            vo.wait_until("A gold tag")
            self.play(FadeOut(VGroup(qp, q_ill, qcard), shift=UP * 0.2), FadeIn(bigbox, shift=UP * 0.15), run_time=0.6)
            self.remove(qp, q_ill, qcard)
            self.play(FadeIn(gold, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("this is the biggest machine")
            flash_tag(self, gold, COST)
            vo.wait_until("If your quota came through")
            self.play(FadeOut(VGroup(bigbox, gold), shift=UP * 0.2), track(tr, 4), run_time=0.5)
            self.remove(bigbox, gold)
            self.play(FadeIn(t), FadeIn(r170, shift=LEFT * 0.15), FadeIn(fresh, shift=UP * 0.1),
                      FadeIn(s30), run_time=0.6)
            vo.wait_until("pause and run")
            pl = istep(self, t, c50.line(42), type_time=0.6)
            yt = beside(turn_row(), pl)
            pin(self, pl, yt, run_time=0.3)
            self.play(FadeIn(opt, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt, TURN, run_time=0.5)
            vo.wait_until("Here it fails like cli.sh")
            out(self, t, [c50.line(43)], run_time=0.4)
            vo.wait_until("with no active account")
            o2 = out(self, t, [c50.line(44)], wrap=True, color=ERR, run_time=0.4)
            self.play(Indicate(VGroup(*o2), color=ERR, scale_factor=1.02), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
