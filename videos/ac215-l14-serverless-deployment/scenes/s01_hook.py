"""S01 · It works on localhost (cold open of AC215 L14, the full follow-along). Lecture: 14 · 8.

Beats (script.md "## S01", one voiceover block each; no tracker until the sample in beat 6):
0. Black frame. A GREY laptop slides in; on its screen the drawn translation page (TranslatePage,
   tag `illustration`, from laptop/11: title "Translate · AC215", two boxes, en / es selectors,
   Translate, the grey disabled "Play audio · enable in part 3"), address bar `localhost:8086` in
   PINK. "Good afternoon everyone" types into the left box, the right selector flips to `fr`,
   Translate pulses, and on "Bonjour à tous" the right box fills with the real answer of laptop/21.
1. The big laptop folds into a compact one on the left ("your laptop": PINK address bar, a TEAL
   "app on :8086" box it reaches, GREEN tick). A second GREY laptop slides in on the right,
   "a classmate" (tag `illustration`). The address flies across and types into its bar; a PINK
   request arrow leaves the bar, curls back into the same laptop and finds an empty, dashed socket:
   RED "nothing here". README card `README.md · lines 238–240` (quote): "Sharing localhost does not
   make it available on another person's computer."
2. The classmate laptop shrinks away, the rest fades. V2 InstanceStrip's top row builds: a solid
   BLUE rack "VM · lecture 1" (GREY-dashed "L1" chip), the axis "evening → night → morning", a few
   PINK pulses near the start, the solid life and the GOLD meter rising at a constant rate, then the
   long empty stretch shaded GOLD "idle, still billed".
3. The strip dims. The YELLOW question card settles centre: "Can this page have a public URL — /
   and cost nothing while nobody is using it?" (each row pulses as it is spoken).
4. lecture_ref(14, "8") fades in top right. The card fades out upward (gone, not parked); the strip
   comes back. V2's bottom row builds under the rack row (the time labels move down under it): at
   the first PINK pulse a dashed BLUE outline with a TEAL box blinks on (cold-start puff), answers,
   and dissolves after the pulses; its GOLD meter moves only under the pulses. On "By the end" the
   strip's words fade and its text-free drawing shrinks left (text is never scaled below 1.0); on
   the right a GREY-dashed preview builds: a BLUE input bucket → a TEAL "job" box with no ear → an
   output bucket that receives three file icons and a GREEN receipt; a hard right edge "exit".
5. Clear (the lecture tag goes with the idea) to a checklist of four GREY chips, one per phrase:
   "your clone", "Docker", "gcloud", "your project + billing".
6. The chips fade. A sample YELLOW tracker (Before you begin · step 4 of 5: Clone repo) fades in
   top-left; a 3-row laptop strip (GREY tag "preview") types laptop/01's `git clone …` exactly as
   captured, and a YELLOW `▶ your turn` row tag pulses beside it. On "Follow the console steps
   first" a GREY README card `README.md · lines 19–21`: "console first · gcloud boxes =
   alternatives". Everything fades; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources (checked)
ANSWER = "Bonjour à tous"
assert '"text":"Bonjour \\u00e0 tous"' in capture("laptop/21").line(2), capture("laptop/21").line(2)
assert "<title>Translate · AC215</title>" in capture("laptop/11").line(5)
assert "Play audio · enable in part 3" in capture("laptop/11").line(6)
assert "Sharing" in readme(238) and "`localhost` does not make it available on another person's computer." \
    in readme(239)
assert readme(19).startswith("**Follow the console steps first.**")
assert "alternative ways to perform the same actions" in readme(20)
CLONE = capture("laptop/01")
assert CLONE.cmd == "git clone https://github.com/dlops-io/serverless-deployment.git", CLONE.cmd
QUESTION = "Can this page have a public URL —\nand cost nothing while nobody is using it?"
CHECKLIST = ("your clone", "Docker", "gcloud", "your project + billing")
CHIP_CUES = ("have your clone", "Docker", "the gcloud tool", "your own project")


def laptop_frame(screen_w: float, screen_h: float, name: str | None = None, color=LAPTOP) -> VGroup:
    """A GREY laptop drawn around a screen of screen_w x screen_h (centred at ORIGIN). .screen .base .name"""
    scr = RoundedRectangle(width=screen_w, height=screen_h, corner_radius=0.16, stroke_color=color,
                           stroke_width=3).set_fill(S.BG, 1)
    bw = screen_w * 1.1
    base = Polygon([-bw / 2, 0, 0], [bw / 2, 0, 0], [bw / 2 - 0.12, 0.22, 0], [-bw / 2 + 0.12, 0.22, 0],
                   stroke_color=color, stroke_width=3).set_fill(color, 0.3)
    base.next_to(scr, DOWN, buff=0.04)
    g = VGroup(scr, base)
    g.screen, g.base, g.name = scr, base, None
    if name:
        t = label(name, 20, color).next_to(base, DOWN, buff=0.14)
        g.add(t)
        g.name = t
    return g


def address_bar(bar_w: float, url: str | None) -> VGroup:
    """A browser address bar (dark field) with an optional PINK mono address. .field .url"""
    f = RoundedRectangle(width=bar_w, height=0.5, corner_radius=0.08, stroke_color=S.GREY_DARK,
                         stroke_width=2).set_fill(TERM_BG, 1)
    g = VGroup(f)
    g.field, g.url = f, None
    if url:
        u = mono(url, 20, ROUTE).move_to(f).align_to(f, LEFT).shift(RIGHT * 0.2)
        g.add(u)
        g.url = u
    return g


def socket_box(running: bool) -> VGroup:
    """What answers on port 8086: the TEAL running app, or an empty dashed GREY socket. .frame .text"""
    if running:
        fr = RoundedRectangle(width=3.0, height=0.7, corner_radius=0.1, stroke_color=IMAGE,
                              stroke_width=3).set_fill(IMAGE, 0.22)
        t = VGroup(label("app on", 20, INK), mono(":8086", 20, ROUTE)).arrange(RIGHT, buff=0.12)
    else:
        fr = outline_box(3.0, 0.7, S.GREY, solid=False)
        t = VGroup(mono(":8086", 20, S.GREY), label("· empty", 20, S.GREY)).arrange(RIGHT, buff=0.12)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 7, len(SAY)

        # ========================================================== 0. it works on localhost
        pg = TranslatePage()                                   # 8.0 x 4.0, address localhost:8086 (PINK)
        pg.move_to([0, 0.45, 0])
        big = laptop_frame(8.5, 4.5, "your laptop").shift(pg.frame.get_center() - ORIGIN)
        ill0 = illustration_tag().next_to(big.screen, UP, buff=0.1).align_to(big.screen, RIGHT)
        whole0 = VGroup(big, pg, ill0)
        assert whole0.get_top()[1] <= 3.55 and whole0.get_bottom()[1] >= -3.55, whole0.get_bottom()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(big, shift=RIGHT * 1.2), FadeIn(pg, shift=RIGHT * 1.2), run_time=1.0)
            self.play(FadeIn(ill0), Indicate(pg.url, color=ROUTE, scale_factor=1.1), run_time=0.8)
            vo.wait_until("Type good afternoon")
            pg.type_in(self, "Good afternoon everyone", run_time=1.4)
            vo.wait_until("choose French")
            pg.set_dest(self, "fr", run_time=0.5)
            vo.wait_until("press Translate")
            self.play(pg.press("translate"), run_time=0.7)
            vo.wait_until("and it answers")
            pg.translate(self, ANSWER, run_time=1.0)
            self.play(Indicate(pg.right_text, color=OWN, scale_factor=1.08), run_time=0.8)

        # ========================================================== 1. send the address to a classmate
        SW, SH = 4.6, 2.9
        me = laptop_frame(SW, SH, "your laptop")
        me.shift([-3.55 - me.screen.get_center()[0], 1.0 - me.screen.get_center()[1], 0])
        me_bar = address_bar(SW - 0.6, LOCAL_URL).move_to(me.screen.get_top() + DOWN * 0.5)
        me_app = socket_box(True).move_to(me.screen.get_center() + DOWN * 0.2)
        me_go = route(me_bar.get_bottom() + LEFT * 0.6, me_app.get_top() + LEFT * 0.6, stroke=4)
        me_ok = check_glyph(0.3).next_to(me_app, RIGHT, buff=0.12)
        ill_me = illustration_tag().next_to(me.screen, UP, buff=0.1).align_to(me.screen, RIGHT)

        mate = laptop_frame(SW, SH, "a classmate")
        mate.shift([3.55 - mate.screen.get_center()[0], 1.0 - mate.screen.get_center()[1], 0])
        mate_bar = address_bar(SW - 0.6, None).move_to(mate.screen.get_top() + DOWN * 0.5)
        mate_url = mono(LOCAL_URL, 20, ROUTE).move_to(mate_bar).align_to(mate_bar, LEFT).shift(RIGHT * 0.2)
        mate_sock = socket_box(False).move_to(mate.screen.get_center() + DOWN * 0.2)
        ill_mate = illustration_tag().next_to(mate.screen, UP, buff=0.1).align_to(mate.screen, RIGHT)
        start = mate_bar.get_right() + LEFT * 0.15
        end = mate_sock.get_right() + RIGHT * 0.02
        curl = Arrow(start, end, buff=0, path_arc=-2.6, color=ROUTE, stroke_width=4, tip_length=0.2,
                     max_tip_length_to_length_ratio=0.3)
        nothing = err_chip("nothing here", mono_font=False).next_to(mate_sock, DOWN, buff=0.15)
        body = VGroup(
            VGroup(label("Sharing", 22, INK), mono("localhost", 22, ROUTE),
                   label("does not make it available", 22, INK)).arrange(RIGHT, buff=0.14, aligned_edge=DOWN),
            label("on another person's computer.", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rc = readme_card((238, 240), body, quote=True).move_to([0, -2.6, 0])
        for m in (me, mate, rc, ill_me, ill_mate, curl, nothing):
            assert -6.6 <= m.get_left()[0] and m.get_right()[0] <= 6.6, (m, m.get_left(), m.get_right())
            assert -3.6 <= m.get_bottom()[1] and m.get_top()[1] <= 3.6, (m, m.get_bottom(), m.get_top())
        assert nothing.get_bottom()[1] > mate.screen.get_bottom()[1] - 0.01
        assert rc.get_top()[1] < mate.name.get_bottom()[1] - 0.1, (rc.get_top(), mate.name.get_bottom())

        with self.voiceover(SAY[1]) as vo:
            url0 = pg.url
            pg.remove(url0)
            self.play(ReplacementTransform(big.screen, me.screen), ReplacementTransform(big.base, me.base),
                      ReplacementTransform(big.name, me.name), FadeOut(pg, scale=0.5), FadeIn(me_bar.field),
                      ReplacementTransform(url0, me_bar.url), ReplacementTransform(ill0, ill_me), run_time=1.0)
            self.add(me_bar.field, me_bar.url)                 # above the (opaque) screen
            self.play(FadeIn(me_app, shift=UP * 0.1), GrowArrow(me_go), FadeIn(me_ok, scale=1.4), run_time=0.7)
            self.play(FadeIn(mate, shift=LEFT * 1.0), FadeIn(mate_bar), FadeIn(ill_mate), run_time=0.8)
            vo.wait_until("On their laptop")
            fly = me_bar.url.copy()
            self.play(fly.animate(path_arc=-0.8).move_to(mate_url), run_time=0.9)
            self.remove(fly)
            self.play(ShowIncreasingSubsets(mate_url, rate_func=linear), run_time=0.6)
            self.play(FadeIn(mate_sock), run_time=0.4)
            self.play(Create(curl), run_time=1.0)
            self.play(FadeIn(nothing, scale=1.2), Indicate(mate_sock.frame, color=ERR, scale_factor=1.05),
                      run_time=0.6)
            vo.wait_until("because localhost always means")
            self.play(FadeIn(rc, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(body[0][1], color=ROUTE, scale_factor=1.1), run_time=0.8)
            self.play(Indicate(mate.screen, color=INK, scale_factor=1.02), run_time=0.8)
            vo.wait_until("and nothing runs on theirs")
            self.play(Indicate(nothing, color=ERR, scale_factor=1.12), run_time=0.8)

        # ========================================================== 2. lecture 1's fix: rent a VM
        strip = InstanceStrip()                                # vm row y 1.1, serverless y -1.1
        sv_axis, sv_label = strip.axis["serverless"], strip.label_["serverless"]
        strip.remove(sv_axis, sv_label)                        # the bottom row builds in beat 4
        times_home = strip.times.get_center().copy()
        strip.times.shift(UP * (strip.p(0, 1.1 - 0.75)[1] - strip.times.get_center()[1]))
        left_part = VGroup(me, me_bar, me_app, me_go, me_ok, ill_me)
        right_part = VGroup(mate, mate_bar, mate_url, mate_sock, ill_mate, curl, nothing)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(right_part, scale=0.3), run_time=0.7)
            self.play(FadeOut(left_part), FadeOut(rc), run_time=0.5)
            self.play(FadeIn(strip, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("The page gets a public address")
            strip.pulses(self, "vm", (0.04, 0.09, 0.15), run_time=0.8)
            vo.wait_until("but the machine is billed")
            strip.vm_run(self, run_time=3.0)
            vo.wait_until("while nobody translates")
            strip.idle(self, [(0.2, 0.97)], run_time=0.9)

        # ========================================================== 3. today's question
        qc = question_card(QUESTION).move_to([0, 0.1, 0])
        strip.save_state()

        with self.voiceover(SAY[3]) as vo:
            self.play(strip.animate.fade(0.75), run_time=0.6)
            self.play(FadeIn(qc, shift=DOWN * 0.3), run_time=0.8)
            vo.wait_until("Can this page have")
            self.play(Indicate(qc.body[0], color=TURN, scale_factor=1.06), run_time=1.0)
            vo.wait_until("and cost nothing")
            self.play(Indicate(qc.body[1], color=TURN, scale_factor=1.06), run_time=1.0)

        # ========================================================== 4. serverless: appears, answers, goes
        ref = lref("8")
        pv_in = bucket(None, 0.8).move_to([1.1, -0.1, 0])
        pv_in_l = label("private", 20, S.GREY).next_to(pv_in, DOWN, buff=0.12)
        pv_job = image_block("job", 1.3, 0.7).move_to([2.95, -0.1, 0])
        pv_out = bucket(None, 0.8).move_to([4.8, -0.1, 0])
        pv_out_l = label("files", 20, S.GREY).next_to(pv_out, DOWN, buff=0.12)
        a1 = arrow(pv_in.get_right() + RIGHT * 0.1, pv_job.get_left() + LEFT * 0.08, color=S.GREY)
        a2 = arrow(pv_job.get_right() + RIGHT * 0.08, pv_out.get_left() + LEFT * 0.1, color=S.GREY)
        files = VGroup(*[file_icon(None, h=0.34) for _ in range(3)]).arrange(RIGHT, buff=0.12)
        files.next_to(pv_out, UP, buff=0.35)
        rcpt = receipt("complete").next_to(pv_out_l, DOWN, buff=0.2)
        edge = Line([5.95, -1.3, 0], [5.95, 1.1, 0], color=INK, stroke_width=7)
        edge_l = label("exit", 20, INK).next_to(edge, UP, buff=0.12)
        pv_frame = outline_box(6.3, 4.0, S.GREY, solid=False).move_to([3.4, -0.05, 0])
        pv_title = label("by the end · a job", 20, S.GREY).move_to(pv_frame.get_corner(UL) + np.array([0.25, -0.3, 0]),
                                                                    aligned_edge=UL)
        for m in (pv_frame, rcpt, edge_l, files):
            assert pv_frame.get_left()[0] - 0.01 <= m.get_left()[0] and m.get_right()[0] <= pv_frame.get_right()[0] + 0.01
            assert pv_frame.get_bottom()[1] - 0.01 <= m.get_bottom()[1] and m.get_top()[1] <= pv_frame.get_top()[1] + 0.01
        assert pv_frame.get_right()[0] <= 6.6 and pv_frame.get_bottom()[1] >= -3.6

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(qc, shift=UP * 0.6), FadeIn(ref), Restore(strip), run_time=0.8)
            strip.show(self, sv_axis, sv_label, anims=[Create(sv_axis), FadeIn(sv_label),
                                                       strip.times.animate.move_to(times_home)], run_time=0.9)
            vo.wait_until("A copy of your app appears")
            before = list(strip.submobjects)
            strip.serve(self, 0.02, 0.22, pulses=(0.04, 0.09, 0.15), run_time=1.6)
            life = [m for m in strip.submobjects if m not in before and not isinstance(m, (Dot, Rectangle))]
            assert len(life) == 1, life
            vo.wait_until("and disappears when")
            self.play(life[0].animate.set_opacity(0.1), run_time=0.9)
            self.play(Indicate(strip.meters["serverless"][0], color=COST, scale_factor=1.3),
                      Indicate(strip.meters["serverless"][1], color=COST, scale_factor=1.3),
                      Indicate(strip.meters["serverless"][2], color=COST, scale_factor=1.3), run_time=0.9)
            vo.wait_until("By the end")
            texts = [strip.label_["vm"][1], sv_label[1], strip.times]
            strip.drop(self, *texts, run_time=0.5)
            rest = [m for m in strip.get_family() if isinstance(m, Text)]
            if rest:
                strip.drop(self, *rest, run_time=0.3)
            assert not [m for m in strip.get_family() if isinstance(m, Text)]
            self.play(strip.animate.scale(0.5).move_to([-3.45, 0.0, 0]), run_time=0.9)
            self.play(Create(pv_frame), FadeIn(pv_title), FadeIn(pv_job, scale=0.8), run_time=0.8)
            vo.wait_until("It takes a passage")
            self.play(FadeIn(pv_in), FadeIn(pv_in_l), GrowArrow(a1), run_time=0.7)
            vo.wait_until("speaks it in French")
            self.play(Indicate(pv_job, color=IMAGE, scale_factor=1.12), run_time=0.8)
            vo.wait_until("saves its files")
            self.play(FadeIn(pv_out), FadeIn(pv_out_l), GrowArrow(a2), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(f, shift=DOWN * 0.3) for f in files], lag_ratio=0.3), run_time=0.8)
            self.play(LaggedStart(*[f.animate.move_to(pv_out.get_center() + UP * 0.05).set_opacity(0)
                                    for f in files], lag_ratio=0.2), FadeIn(rcpt, shift=UP * 0.1), run_time=0.9)
            self.remove(files)
            vo.wait_until("and exits")
            self.play(Create(edge), FadeIn(edge_l), pv_job.animate.set_opacity(0.35), run_time=0.7)
        self.play(Indicate(edge_l, color=INK, scale_factor=1.15), run_time=0.8)   # a breath on the exit

        # ========================================================== 5. what you need
        chips = VGroup(*[grey_chip(s, size=24) for s in CHECKLIST]).arrange(RIGHT, buff=0.4).move_to([0, 0.2, 0])
        ticks = VGroup(*[check_glyph(0.28).next_to(c, UP, buff=0.18) for c in chips])
        pv = VGroup(pv_frame, pv_title, pv_in, pv_in_l, pv_job, pv_out, pv_out_l, a1, a2, rcpt, edge, edge_l)
        assert chips.width <= 12.6

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(strip), FadeOut(pv), FadeOut(ref), run_time=0.6)
            for c, t, cue in zip(chips, ticks, CHIP_CUES):
                vo.wait_until(cue)
                self.play(FadeIn(c, shift=UP * 0.2), FadeIn(t, scale=1.4), run_time=0.45)

        # ========================================================== 6. how to read the screen
        tr = tracker_bb(4)
        t = laptop_term(rows=3, prompt=P_HOME)
        prev = tag("preview", S.GREY)
        on_bar(t, prev)
        cons = readme_card((19, 21), "console first · gcloud boxes = alternatives", size=24).move_to([0, 0.6, 0])
        assert cons.get_bottom()[1] > t.box.get_top()[1] + 0.3 and cons.get_top()[1] < TRACK_BOTTOM - 0.2

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(chips), FadeOut(ticks), run_time=0.5)
            self.play(FadeIn(tr, shift=RIGHT * 0.3), run_time=0.7)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("and a yellow tag")
            self.play(FadeIn(t), FadeIn(prev), run_time=0.5)
            type_capture(self, t, CLONE, type_time=0.9)
            got = out(self, t, CLONE.at(2), run_time=0.4)
            yt = beside(turn_row(), got[-1])
            pin(self, got[-1], yt)
            vo.wait_until("means pause")
            flash_tag(self, yt)
            vo.wait_until("Follow the console steps")
            self.play(FadeIn(cons, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("the gcloud boxes")
            self.play(Indicate(cons.body, color=INK, scale_factor=1.05), run_time=0.9)

        self.play(FadeOut(tr), FadeOut(t), FadeOut(prev), FadeOut(cons), run_time=0.8)
        self.wait(0.5)
