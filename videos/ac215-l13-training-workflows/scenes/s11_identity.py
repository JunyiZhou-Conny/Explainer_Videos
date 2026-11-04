"""S11 · Who submits, who runs — no tracker for the badges, then F2 · extra · local stand-in;
lecture_ref 24.

Beats (script.md, ## S11; one voiceover block each):
0. No tracker. V5 ThreeBadges (badge 2 already RED from S10): badge 0 (GREEN key file,
   model-trainer, "key file · submits") hangs, its three role chips (README:62) settle under it. A
   flat strip of the map below: the GREY laptop (TEAL cockpit, GREEN key), the BLUE dashed
   your-gcp-project (bucket, Vertex AI), the separate BLUE wandb.ai building. Two GREY arrows from
   the cockpit: "write" to the bucket, "create job" to Vertex AI.
1. Badge 2 (RED W&B key) hangs; a RED "--args · W&B key" chip is carried along the create-job arrow
   through Vertex AI to wandb.ai. The middle lanyard hangs empty with a GREY "?".
2. The bucket glows, the key on the laptop flashes. PONDER 8 s.
3. The answer: the ORANGE service-agent badge settles on the middle lanyard; a job appears in
   Vertex AI with a small ORANGE badge riding it; an ORANGE arrow from the job opens the bucket;
   the key stays GREY-side, only the create-job arrow is its work. GREY chip "a 403 …".
4. V4 step 4, drawn once (tag "what Vertex does · drawn, not recorded", no output panel): VM + GOLD
   meter, Google's TEAL image with the ORANGE "expected" layer, the tarball unwraps, pip adds wandb,
   python -m trainer.task with --args split at its commas. Then the dashed TEAL stand-in replaces
   the VM; tracker F2 · extra · local stand-in; laptop strip types 80; the tarball unwraps in the
   stand-in; the terminal grows: 80: 2, …, 68, 70 wrap (cheese-app-trainer-0.0.1, wandb-0.15.11
   YELLOW).
5. 81 (commit) → 81:2; 82 pip list (squeezed: 2–3, …, 7, …, 19, …, 26), chip "no tensorflow · no
   scikit-learn"; 09 (plain extra, live manifest check) → 09:2–3, at the time of recording; strip
   under a picture: the stand-in's ORANGE slot empty (dashed), Google's tf-cpu band with the ORANGE
   layer, "expected in tf-cpu.2-17 · not verified here". 83 → 83: 2, …, 7–9, line 9 RED.
6. CODE(task.py: 152–153); one terminal, three keys: 85:2 RED (chip: the empty key from scene 10 …),
   84: …, 14 RED (chip: the default "16"), 86:4 YELLOW (chip: length check only …).
7. 87: …, 14, "yours was 47" RED; GREY card on the pin. Fade out.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F403
from explainer import style as S

SAY = NARRATION["S11"]
PONDER_HOW = ("The job installs your package from your\nprivate bucket, but your key never left\n"
              "your laptop. How?")
LOW_Y = -2.7          # centre line of the flat map strip under the badges (y -3.45 … -1.95)


def lines_chip(*lines: str, color=S.GREY, size: float = 20) -> VGroup:
    """A GREY note of a few label lines in a rounded box (the chips too long for one line). .box .text"""
    t = VGroup(*[label(x, size, INK) for x in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    b_ = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.3, corner_radius=0.16, stroke_color=color,
                          stroke_width=2.5).set_fill(color, 0.16)
    t.move_to(b_)
    g = VGroup(b_, t)
    g.box, g.text = b_, t
    return g


def agent_pin(size: float = 20) -> VGroup:
    """A small ORANGE badge that rides the job (the service agent's)."""
    fr = RoundedRectangle(width=0.42, height=0.5, corner_radius=0.07, stroke_color=SYSTEM,
                          stroke_width=2.5).set_fill(SYSTEM, 0.25)
    gear = Circle(radius=0.1, stroke_color=SYSTEM, stroke_width=3).move_to(fr)
    clip = RoundedRectangle(width=0.22, height=0.08, corner_radius=0.03, stroke_color=SYSTEM,
                            stroke_width=2).set_fill(S.BG, 1).move_to(fr.get_top())
    return VGroup(fr, gear, clip)


def flat_map() -> VGroup:
    """The map as a flat strip under the badges: laptop (cockpit, key), your-gcp-project (bucket,
    Vertex AI), wandb.ai. .laptop .cockpit .key .gcp .bucket .vertex .wb"""
    top, bot = -1.95, -3.45
    lp = RoundedRectangle(width=2.75, height=top - bot, corner_radius=0.14, stroke_color=LAPTOP,
                          stroke_width=2.5).set_fill(LAPTOP, 0.06).move_to([-5.125, (top + bot) / 2, 0])
    lpt = label("laptop", 20, LAPTOP).move_to(lp.get_corner(UL) + np.array([0.15, -0.22, 0]), aligned_edge=LEFT)
    ck = house("cockpit", 1.2, 0.85, IMAGE, lit=True).move_to([-4.65, bot + 0.18, 0], aligned_edge=DOWN)
    kg = key_glyph(0.55, KEY)
    kl = label("key file", 20, KEY)
    key = VGroup(kg, kl).arrange(DOWN, buff=0.08).move_to([-6.0, -2.95, 0])
    gcp = outline_box(6.05, top - bot, CLOUD, solid=False, fill_opacity=0.0).move_to([-0.225, (top + bot) / 2, 0])
    gct = mono(PROJECT_ID, 20, CLOUD).move_to([1.45, -2.18, 0])
    bk = RoundedRectangle(width=1.7, height=0.5, corner_radius=0.1, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.12).move_to([-1.5, -2.45, 0])
    bkt = label("your bucket", 20, INK).move_to(bk)
    vx = RoundedRectangle(width=3.3, height=0.62, corner_radius=0.1, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.12).move_to([1.05, -3.05, 0])
    vxt = label("Vertex AI", 20, INK).move_to(vx.get_left() + RIGHT * 0.2, aligned_edge=LEFT)
    wb = building(WB_HOST, 2.4, 1.45).move_to([4.75, bot, 0], aligned_edge=DOWN)
    g = VGroup(lp, lpt, ck, key, gcp, gct, bk, bkt, vx, vxt, wb)
    g.laptop, g.cockpit, g.key, g.gcp = VGroup(lp, lpt), ck, key, VGroup(gcp, gct)
    g.bucket, g.vertex, g.wb = VGroup(bk, bkt), VGroup(vx, vxt), wb
    return g


def rows_with(rows, sub):
    """The printed terminal row whose text contains `sub`."""
    for r in rows:
        if sub in getattr(r, "text", ""):
            return r
    raise ValueError(sub)


class WhoRunsIt(VoiceScene):
    def keep_only(self, *keep, run_time=0.5, shift=UP * 0.2):
        fam = {id(x) for k in keep for x in k.get_family()}
        gone = [m for m in self.mobjects if not any(id(x) in fam for x in m.get_family())]
        if gone:
            self.play(FadeOut(Group(*gone), shift=shift), run_time=run_time)
            self.remove(*gone)

    def clear(self, t, *extra, run_time=0.3):
        """Fade every printed row of terminal t (and `extra`), then drop them from t.lines."""
        rows = list(t.lines)
        self.play(FadeOut(VGroup(*rows, *extra)), run_time=run_time)
        self.remove(*rows, *extra)
        if rows:
            t.lines.remove(*rows)

    def construct(self):
        assert len(SAY) == SAY_COUNT["S11"] == 8, len(SAY)
        c80, c81, c82, c83 = capture("80"), capture("81"), capture("82"), capture("83")
        c84, c85, c86, c87, c09 = capture("84"), capture("85"), capture("86"), capture("87"), capture("09")

        # ========================================================== 0. badge 1: the submitter
        ref = lref("24")
        tb = ThreeBadges(red=True)
        fm = flat_map()
        ck, bk, vx = fm.cockpit, fm.bucket, fm.vertex
        y_w = bk.get_center()[1]
        a_write = arrow(np.array([ck.get_right()[0] + 0.02, -2.75, 0]), np.array([bk.get_left()[0], y_w, 0]), S.GREY, buff=0.08)
        l_write = label("write", 20, S.GREY).move_to([-2.85, -2.2, 0])
        y_c = vx.get_center()[1]
        a_job = arrow(np.array([ck.get_right()[0] + 0.02, y_c, 0]), np.array([vx.get_left()[0], y_c, 0]), S.GREY, buff=0.08)
        l_job = label("create job", 20, S.GREY).move_to([-1.9, -3.27, 0])
        assert l_write.get_bottom()[1] > a_write.get_top()[1]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(fm.laptop), FadeIn(ck), FadeIn(fm.gcp), FadeIn(bk), FadeIn(vx),
                      run_time=0.7)
            self.play(tb.hang(0), run_time=0.9)
            vo.wait_until("The first is your key file")
            self.play(FadeIn(fm.key, shift=UP * 0.15), Indicate(tb.badges[0].text, color=INK, scale_factor=1.05),
                      run_time=0.7)
            vo.wait_until("Its three roles")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.15) for r in tb.roles], lag_ratio=0.3), run_time=0.9)
            self.add(tb.roles)
            vo.wait_until("write to your bucket")
            self.play(GrowArrow(a_write), FadeIn(l_write), run_time=0.6)
            vo.wait_until("and create jobs")
            self.play(GrowArrow(a_job), FadeIn(l_job), run_time=0.6)
            vo.wait_until("it submits")
            self.play(Indicate(tb.badges[0].text[1], color=KEY, scale_factor=1.1), run_time=0.6)

        # ========================================================== 1. badge 3: W&B key, by hand
        args_c = chip("--args · W&B key", ERR, size=20, font=MONO, fill_opacity=0.14)
        args_y = -1.74
        q = tb.question()

        with self.voiceover(SAY[1]) as vo:
            self.play(tb.hang(2), FadeIn(fm.wb, shift=UP * 0.15), run_time=0.9)
            vo.wait_until("for a different building altogether")
            self.play(Indicate(fm.wb.text, color=CLOUD, scale_factor=1.1), run_time=0.6)
            vo.wait_until("carried by hand")
            args_c.move_to([-0.8, args_y, 0])
            self.play(FadeIn(args_c, shift=UP * 0.1), Indicate(a_job, color=ERR), run_time=0.5)
            self.play(args_c.animate.move_to([vx.get_center()[0], args_y, 0]), run_time=0.9)
            self.play(args_c.animate.move_to([fm.wb.get_center()[0] - 0.2, args_y, 0]), run_time=0.8)
            vo.wait_until("The middle lanyard is still empty")
            self.play(tb.lanyard(1), run_time=0.5)
            self.play(FadeIn(q, scale=0.8), run_time=0.4)

        # ========================================================== 2. the ponder
        with self.voiceover(SAY[2]) as vo:
            self.play(Indicate(q, color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("from your private bucket")
            self.play(bk[0].animate.set_stroke(width=6).set_fill(CLOUD, 0.35), run_time=0.6)
            vo.wait_until("but your key file never left your laptop")
            self.play(Indicate(fm.key, color=KEY, scale_factor=1.2), run_time=0.8)
        pc = ponder(self, PONDER_HOW, seconds=8, center=(0, 1.15), width=9.0)

        # ========================================================== 3. badge 2: the runner
        job = chip("job", CLOUD, size=20, font=MONO).move_to([2.2, y_c, 0])
        ap = agent_pin().next_to(job, LEFT, buff=0.1)
        a_open = Arrow(job.get_top() + LEFT * 0.1, bk[0].get_right() + DOWN * 0.05, buff=0.08, color=SYSTEM,
                       stroke_width=4, tip_length=0.18)
        c403 = grey_chip("a 403 on your bucket → grant this identity access").move_to([0.75, -1.6, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(pc), FadeOut(q), FadeOut(args_c), run_time=0.4)
            self.remove(pc, q, args_c)
            self.play(tb.hang(1), run_time=0.9)
            vo.wait_until("a service account Google manages")
            self.play(Indicate(tb.badges[1].portrait, color=SYSTEM, scale_factor=1.2), run_time=0.6)
            vo.wait_until("By default the job runs as it")
            self.play(FadeIn(job, scale=0.8), run_time=0.4)
            self.play(Indicate(tb.badges[1].portrait, color=SYSTEM, scale_factor=1.15), FadeIn(ap, scale=1.6),
                      run_time=0.8)
            vo.wait_until("and it can open buckets in the same project")
            self.play(GrowArrow(a_open), bk[0].animate.set_stroke(width=3).set_fill(CLOUD, 0.12), run_time=0.7)
            self.play(Indicate(bk[1], color=SYSTEM, scale_factor=1.1), run_time=0.5)
            vo.wait_until("Your key only proved who submitted")
            self.play(Indicate(fm.key, color=KEY, scale_factor=1.15), a_job.animate.set_color(KEY),
                      l_job.animate.set_color(KEY), run_time=0.8)
            vo.wait_until("If a job ever gets a 403")
            self.play(FadeIn(c403, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("that is the identity to grant access")
            self.play(Indicate(tb.badges[1].text, color=SYSTEM, scale_factor=1.05), run_time=0.7)
        self.wait(0.4)

        # ========================================================== 4. V4 step 4, then the stand-in
        dt = drawn_tag().move_to([-6.5, 3.25, 0], aligned_edge=LEFT)
        vm = TarballTrip.vm()
        vm_t = vm.box[1]           # its title would sit under the argv's first row: put it under the frame
        vm_t.next_to(vm.box[0], DOWN, buff=0.12).align_to(vm.box[0], LEFT)
        exp_ = grey_chip("expected · not verified here").move_to([2.4, -2.25, 0])
        split_ = grey_chip("--args, split at its commas").move_to([-2.0, -2.25, 0])
        sd = TarballTrip.standin().move_to([-1.6, 0.9, 0])
        tr = tracker_f(2, extra="local stand-in")
        assert tr.caption.get_right()[0] < ref.get_left()[0]
        h = term(P_REPO, rows=3, size=20)
        sr = on_bar(h, standin_row())
        p2 = parcel(None, OWNED, 20, 0.6, 0.42).move_to([-1.6, 2.4, 0])
        tdr = drawer("trainer/", OWNED, 20)
        wch = chip("wandb 0.15.11", OWNED, size=20, font=MONO)
        inst = VGroup(tdr, wch).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(sd, RIGHT, buff=0.6)

        with self.voiceover(SAY[4]) as vo:
            self.keep_only(ref, run_time=0.5)
            self.play(FadeIn(dt, shift=DOWN * 0.1), run_time=0.3)
            self.play(vm.appear(run_time=0.7))
            self.play(vm.image_in(run_time=0.6))
            self.play(FadeIn(exp_, shift=UP * 0.1), run_time=0.3)
            vo.wait_until("installs your tarball")
            self.play(vm.unwrap(run_time=0.7))
            self.play(vm.pip(run_time=0.4))
            self.play(vm.run(run_time=0.9), FadeIn(split_, shift=UP * 0.1))
            vo.wait_until("We can't run Vertex here")
            inside = [m for m in (vm.meter, vm.image, vm.layer, vm.trainer, vm.wandb_chip, vm.argv)
                      if m in vm.submobjects]
            self.play(*[FadeOut(m) for m in inside], FadeOut(vm_t), FadeOut(exp_), FadeOut(split_), FadeOut(dt),
                      run_time=0.5)
            vm.box.remove(vm_t)
            self.remove(*inside, vm_t, exp_, split_, dt)
            # a cross-fade: ReplacementTransform of the VM frame into the dashed house flashed a solid TEAL block
            self.play(FadeOut(vm.box[0], scale=0.6), FadeIn(sd, scale=1.3), run_time=0.9)
            self.remove(vm)
            self.add(sd)
            vo.wait_until("tagged as a stand-in")
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(h), FadeIn(sr), run_time=0.5)
            ln80 = type_cmd(self, h, c80.cmd, type_time=1.0)
            vo.wait_until("In a plain Python 3.10 container")
            self.play(Indicate(sd.text[0], color=IMAGE, scale_factor=1.1), run_time=0.5)
            self.play(FadeIn(p2, shift=DOWN * 0.3), run_time=0.4)
            self.play(p2.animate.move_to(sd.get_center()), run_time=0.5)
            self.play(FadeOut(p2, scale=1.4), FadeIn(tdr, shift=RIGHT * 0.2), run_time=0.5)
            self.remove(p2)
            vo.wait_until("pip installs the tarball")
            self.play(FadeIn(wch, shift=RIGHT * 0.2), run_time=0.4)
            self.play(FadeOut(VGroup(sd, tdr, wch)), run_time=0.4)
            self.remove(sd, tdr, wch)
            resize(self, h, 12, run_time=0.5, extra=[sr.animate.shift(UP * 9 * h.pitch)])
            o80 = out(self, h, [c80.line(2), "…", c80.line(68), c80.line(70)], wrap=True, run_time=0.6)
            vo.wait_until("your package")
            pk = rows_with(o80, "cheese-app-trainer-0.0.1")
            self.play(substring(pk, "cheese-app-trainer-0.0.1").animate.set_color(TURN), run_time=0.4)
            vo.wait_until("plus wandb 0.15.11")
            wr = rows_with(o80, "wandb-0.15.11")
            self.play(substring(wr, "wandb-0.15.11").animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(substring(wr, "wandb-0.15.11"), color=TURN, scale_factor=1.1), run_time=0.5)

        # ========================================================== 5. what the stand-in lacks
        nott = grey_chip("no tensorflow · no scikit-learn")
        sq = squeeze(c82.at((2, 26)))           # file lines 2..26 → sq[0..24]
        pl = [sq[0], sq[1], "…", sq[5], "…", sq[17], "…", sq[24]]
        assert sq[5].startswith("cheese-app-trainer") and sq[17].startswith("requests") and sq[24].startswith("wandb")
        sd2 = TarballTrip.standin().move_to([-3.3, -0.1, 0])
        slot = dashed_chip("TensorFlow · scikit-learn", SYSTEM).next_to(sd2, UP, buff=0.15)
        mt = label("stand-in: slot empty", 20, S.GREY).next_to(slot, UP, buff=0.15)
        gimg = band(CPU_IMAGE, IMAGE, 4.6, 0.42, 20, mono_font=True).move_to([3.3, -0.65, 0])
        glay = band("TensorFlow · scikit-learn", SYSTEM, 4.6, 0.42, 20).next_to(gimg, UP, buff=0.06)
        gt = label("Google's prebuilt image", 20, IMAGE).next_to(glay, UP, buff=0.15)
        gexp = grey_chip("expected in tf-cpu.2-17 · not verified here").next_to(gimg, DOWN, buff=0.25)

        with self.voiceover(SAY[5]) as vo:
            self.clear(h)
            type_cmd(self, h, c81.cmd, type_time=0.6)
            out(self, h, c81.at(2), run_time=0.3)
            self.wait(0.4)
            self.clear(h)
            type_cmd(self, h, c82.cmd, type_time=0.5)
            vo.wait_until("An extra pip list")
            o82 = out(self, h, pl, run_time=0.6, lag=0.05)
            vo.wait_until("shows wandb, requests and their helpers")
            self.play(each([o82[7], o82[5]], TURN, scale=1.05, lag=0.2), run_time=0.8)   # wandb, requests (as said)
            vo.wait_until("but no TensorFlow")
            nott.next_to(h.box, UP, buff=0.15).align_to(h.box, RIGHT)
            self.play(FadeIn(nott, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("The trainer counts on the prebuilt image")
            # 09 checks Google's real image: plain `extra`, not a stand-in — the bar tag says so too
            sr_x = on_bar(h, extra_row())
            self.play(track(tr, 2, extra=True), FadeTransform(sr, sr_x), run_time=0.4)
            sr = sr_x
            self.clear(h, nott)
            type_cmd(self, h, c09.cmd, type_time=0.9, soft=True)
            o09 = out(self, h, c09.at(2, 3), run_time=0.3)
            self.play(substring(o09[1], "4.31 GB compressed").animate.set_color(TURN), run_time=0.3)
            pin(self, o09[1], beside(time_row(), o09[1]), run_time=0.3)
            # the picture goes up straight after the manifest line (it was on screen for ~1 s before)
            resize(self, h, 3, keep=[o09[0], o09[1]], run_time=0.4, extra=[sr.animate.shift(DOWN * 9 * h.pitch)])
            self.play(FadeIn(sd2), FadeIn(slot), FadeIn(mt), FadeIn(gimg, shift=DOWN * 0.2), FadeIn(gt), run_time=0.5)
            self.play(FadeIn(glay, shift=DOWN * 0.3), run_time=0.4)
            vo.wait_until("which we did not pull to check")
            self.play(FadeIn(gexp, shift=UP * 0.1), Indicate(slot, color=SYSTEM, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Without it")
            pic = VGroup(sd2, slot, mt, gimg, glay, gt, gexp)
            sr_s = on_bar(h, standin_row())
            self.play(track(tr, 2, extra="local stand-in"), FadeTransform(sr, sr_s), FadeOut(pic), run_time=0.4)
            sr = sr_s
            self.remove(*pic)
            self.clear(h)
            resize(self, h, 8, run_time=0.4, extra=[sr.animate.shift(UP * 5 * h.pitch)])
            type_cmd(self, h, c83.cmd, type_time=0.6)
            o83 = out(self, h, [c83.line(2), "…", *c83.at((7, 8)), (c83.line(9), ERR)], wrap=True, run_time=0.5)
            vo.wait_until("cannot even print its help")
            self.play(Indicate(o83[-1], color=ERR, scale_factor=1.04), run_time=0.6)
        self.wait(1.5)          # the traceback stays readable before beat 6 clears the terminal

        # ========================================================== 6. three keys at line 153
        p153 = code("package/trainer/task.py", 152, 153)
        p153.move_to([-6.4 + p153.width / 2, 2.6 - p153.height / 2, 0])
        bar153 = line_bar(p153.code, 1, TURN)
        ch_empty = lines_chip("the empty key from scene 10 ·", "on Vertex: after the download,", "on billed machine time")
        ch_16 = grey_chip('the default "16"')
        ch_ph = lines_chip("length check only · offline ·", "nothing asked W&B")
        for c_ in (ch_empty, ch_16, ch_ph):
            c_.move_to([p153.get_right()[0] + 0.3 + c_.width / 2, p153.get_center()[1], 0])
            assert c_.get_right()[0] < 6.6, c_.get_right()

        with self.voiceover(SAY[6]) as vo:
            self.clear(h)
            self.play(FadeIn(p153, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("line 153")
            self.play(FadeIn(bar153), run_time=0.4)
            vo.wait_until("The empty key from the last chapter")
            type_cmd(self, h, c85.cmd, type_time=0.7, soft=True)
            o85 = out(self, h, [(c85.line(2), ERR)], wrap=True, run_time=0.3)
            self.play(FadeIn(ch_empty, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("on Vertex that comes after the data download")
            self.play(Indicate(ch_empty.text[1], color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("The default of 16 fails")
            self.play(FadeOut(ch_empty), run_time=0.3)
            self.remove(ch_empty)
            type_cmd(self, h, c84.cmd, type_time=0.7, soft=True)
            o84 = out(self, h, ["…", (c84.line(14), ERR)], run_time=0.3)
            self.play(FadeIn(ch_16, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("yours was 2")
            self.play(Indicate(substring(o84[-1], "yours was 2"), color=ERR, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Our 40 character placeholder")
            self.play(FadeOut(ch_16), run_time=0.3)
            self.remove(ch_16)
            type_cmd(self, h, c86.cmd, type_time=0.8, soft=True)
            o86 = out(self, h, [(c86.line(4), TURN)], wrap=True, run_time=0.3)
            vo.wait_until("and nothing more")
            self.play(FadeIn(ch_ph, shift=UP * 0.1), run_time=0.4)
        self.wait(0.3)

        # ========================================================== 7. this pin: exactly 40
        pin_card = card(["wandb 0.15.11 accepts exactly 40 characters", "today's key format: not checked",
                         "a different length: this pin refuses it", "check before you submit"], size=22)

        with self.voiceover(SAY[7]) as vo:
            self.clear(h, ch_ph)
            type_cmd(self, h, c87.cmd, type_time=0.8, soft=True)
            o87 = out(self, h, ["…", c87.line(14)], run_time=0.3)
            vo.wait_until("and 47 fails")
            self.play(substring(o87[-1], "yours was 47").animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(substring(o87[-1], "yours was 47"), color=ERR, scale_factor=1.1), run_time=0.5)
            vo.wait_until("We could not check")
            pin_card.move_to([0, (h.box.get_top()[1] + 2.8) / 2, 0])
            self.play(FadeOut(VGroup(p153, bar153)), FadeIn(pin_card, shift=UP * 0.15), run_time=0.6)
            self.remove(p153, bar153)
            vo.wait_until("If yours differs")
            self.play(Indicate(pin_card.body[2], color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("so check before you submit")
            self.play(pin_card.body[3].animate.set_color(TURN), run_time=0.5)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
