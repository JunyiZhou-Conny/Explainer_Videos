"""S08 · Deploy the same image — tracker [2.2] 1 → 10; lecture slides 14–15, 11 and 14.

Beats (script.md "## S08"; one voiceover block each):
0. No tracker. LECTURE 14 · 14–15. Slide 14 in one line (GREY card): "Cloud Run: a whole container ·
   as a service or a job · no server to manage", with a small dashed BLUE instance holding a TEAL
   container and the two words service | job; slide 15's three steps as a GREY checklist ("open
   Cloud Run", "enable the APIs", "deploy an image"), each ticked as it is spoken.
1. TRACKER [2.2] 1 (appears). CONSOLE (README:272-280, illustration): Cloud Run → Services → Deploy
   container, then "Create service" with the radio "Deploy one revision from an existing container
   image" selected. [2.2] 2: "Container image URL" fills with the image; a PINK thread links it to
   the same string in a GREY ghost of S07's `docker run` (laptop/10:1–2). [2.2] 3: the worksheet card
   `translation-demo` flies into "Service name"; the region fills (Toronto).
2. [2.2] 4: "Authentication" → Allow public access, "Billing" → Request-based. [2.2] 5: "Service
   scaling" Auto scaling, minimum 0, maximum 2 (README:281-283).
3. [2.2] 6: "Containers, Networking, Security → Edit Container → Settings": port 8080, 512 MiB,
   CPU 1, the GREY note "leave the image's command and arguments unchanged". On "knocks on it", V5's
   envelope returns small beside the form: a BLUE Cloud Run envelope PORT=8080 opens over a TEAL
   container, and a BLUE knock reaches the PINK ear 0.0.0.0:8080. [2.2] 7: "Requests": timeout 120,
   max concurrent requests per instance 4 (README:288-290).
4. V2 SlotPool: one dashed BLUE instance with a TEAL box of four slots, labelled "4 threads
   (__main__.py:25) = concurrency 4" + GREY chip "--threads 4 in the process list"; PINK pulses fill
   the slots, a second instance splits off, YELLOW ceiling "max = 2" (no in-flight counter yet).
5. The instances dissolve (chip "scale to zero"). V2's strip: the GOLD meter moves only under the
   pulses; slider min instances 0 → 1 (a faint instance with its own GOLD drip); switch Request-based
   → Instance-based (the meter covers whole lives); both reset. LECTURE 14 · 11, 14 + GREY quote
   "pay only when your code runs" (erratum) + GREEN "with these two settings". GOLD cost tags.
6. Ten PINK request dots line up, YELLOW "Translate ×10". PONDER (8 s).
7. The dots flow: two instances, 4 + 4 slots, the ceiling glows, "8 in flight, at most"; two dots wait
   in a GREY queue, one flashes RED "may be refused". Three fix chips: raise max instances (GREEN
   tick), raise concurrency + threads together (GREEN tick), raise min instances (RED cross, chip
   "warmth, not capacity").
8. [2.2] 8: Create; RECORDED panels (expected/part2-service-recorded.txt: 3, then 4 at [2.2] 9, then
   5–6 at [2.2] 10), each replacing the last, tag "recorded · container GIF". On "A revision is", a
   card "rev 1 · image + settings" under a dashed instance + README card (lines 295–296).
   `▶ your turn`.
9. A small V1 grid icon: the container · serverless cell lights YELLOW; a PURPLE Cloud Build box
   turns GREY-dashed with a GREY cross, "no build this time"; README card (lines 314–315).
10. A TEAL image with a movable sticky note `:lecture14-agent-platform-20261022` ("tag") and an
   engraved GREEN `@sha256:c17b…dbe72e` ("digest"); [2.2] 10 · extra: strip types laptop/15 →
   TERM(laptop/15: 2), GREEN; the digest goes into a dashed revision; erratum chip "a tag in the
   click path · deploy by digest to reproduce".
11. [2.2] 8 · gcloud alternative. Terminal `laptop · gcloud` types README:321-324 (no output panel);
   the flags light in four groups (image · access · scaling · resources); GREY chip "needs your
   project · no output shown".
12. The drawn public page (illustration) at `https://translation-demo-…run.app` (BLUE); "Play audio ·
   enable in part 3" pulses YELLOW; YELLOW parked-question card. Fade out; empty frame (end of part 1).
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S08"]

REGION_VALUE = f"{REGION} ({REGION_CITY})"         # as S04 fills it
FORM_UL = np.array([-6.45, 2.72, 0])                 # forms hang from here, under the tracker
PONDER_Q = ("Concurrency 4, max instances 2.\nTen people press Translate at once.\n"
            "How many instances — and the last two?")


def field_box(w: float, size: float = 20) -> RoundedRectangle:
    """A console field box, the way console_form draws one."""
    return RoundedRectangle(width=w, height=mono("|", size).height + 0.2, corner_radius=0.06,
                            stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(TERM_BG, 1)


def image_form() -> VGroup:
    """'Create service' with the image URL field on its own row under its label (the 62-character
    image does not fit beside a label column). fill(1, IMAGE_REF) types it like any field."""
    f = console_form("Create service",
                     [("radio", "Deploy one revision from an existing container image", True),
                      ("Service name", ""), ("Region", "")], form_w=11.4, path="Cloud Run → Services")
    items = f.rows
    lt = label("Container image URL", 20, S.GREY)
    fb = field_box(mono(IMAGE_REF, 20).width + 0.4)
    vt = mono("|", 20).set_opacity(0)
    fb.next_to(lt, DOWN, buff=0.12, aligned_edge=LEFT)
    vt.move_to(fb).align_to(fb, LEFT).shift(RIGHT * 0.15)
    row = VGroup(lt, fb, vt)
    row.label, row.field, row.value, row.kind = lt, fb, vt, "field"
    items.submobjects.insert(1, row)
    items.arrange(DOWN, buff=0.2, aligned_edge=LEFT)
    frame, sep, head = f.frame, f[1], f[2]
    body = VGroup(head, items).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    frame.stretch_to_fit_height(body.height + 0.6)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    sep.move_to([frame.get_center()[0], head.get_bottom()[1] - 0.15, 0])
    return f


def form_at(f: VGroup) -> VGroup:
    return f.move_to(FORM_UL, aligned_edge=UL)


def ill_on(f: VGroup) -> VGroup:
    """The illustration tag right of a form's top (or on its top edge, right, for a wide form): never
    under the tracker's caption."""
    tg = illustration_tag()
    if f.frame.get_right()[0] + 0.2 + tg.width <= 6.5:
        return tg.next_to(f.frame, RIGHT, buff=0.2).align_to(f.frame, UP)
    return tg.move_to(f.frame.get_corner(UR) + np.array([-0.95, 0, 0]))


def row_with(rows, sub):
    """The first terminal row among `rows` whose text contains `sub`."""
    for r in rows:
        if sub in getattr(r, "text", ""):
            return r
    raise KeyError(f"{sub!r} not in {[getattr(r, 'text', '') for r in rows]}")


def all_rows(lines) -> list:
    out_ = []
    for ln in lines:
        out_ += rows_of(ln)
    return out_


def check_row(text: str) -> VGroup:
    """A checklist row: an empty GREY box and its words. .mark .text"""
    mk = Rectangle(width=0.3, height=0.3, stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 1)
    t = label(text, 22, INK).next_to(mk, RIGHT, buff=0.2)
    g = VGroup(mk, t)
    g.mark, g.text = mk, t
    return g


def sticky(text: str) -> VGroup:
    """A movable sticky note (GREY, slightly tilted) holding the image tag. .note .text"""
    t = mono(text, 20, INK)
    b = Rectangle(width=t.width + 0.4, height=t.height + 0.32, stroke_color=S.GREY,
                  stroke_width=2).set_fill(S.GREY_DARKER, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.note, g.text = b, t
    return g


class DeployTheImage(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S08"] == 13, len(SAY)
        c10, c15 = capture("laptop/10"), capture("laptop/15")
        assert c10.cmd_lines[1].strip() == IMAGE_REF and c15.cmd_lines[0].endswith(IMAGE_REF)
        gc_rows = readme_rows(321, 324)
        assert gc_rows[0].startswith("gcloud run deploy") and gc_rows[-1].endswith("--timeout=120")

        # ========================================================== 0. the lecture's Cloud Run (slides 14-15)
        ref = lref("14–15")
        s14 = card(["Cloud Run: a whole container · as a service or a job · no server to manage"], S.GREY,
                   size=22).move_to([0, 1.9, 0])
        inst = instance(2.4, 1.4, inner=False)
        box_in = image_block("container", 1.9, 0.75).move_to(inst)
        svc_w = chip("service", CLOUD, size=20)
        job_w = chip("job", CLOUD, size=20)
        VGroup(svc_w, job_w).arrange(DOWN, buff=0.2).next_to(inst, RIGHT, buff=0.35)
        pic = VGroup(inst, box_in, svc_w, job_w).move_to([-3.4, -0.9, 0])
        steps = VGroup(*[check_row(s) for s in ("open Cloud Run", "enable the APIs", "deploy an image")])
        steps.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        chk = card([steps], S.GREY, head="lecture's three steps").move_to([3.2, -0.9, 0])
        ticks = [check_glyph(0.3, TURN).move_to(r.mark) for r in steps]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(s14, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("runs a whole container")
            self.play(FadeIn(inst, scale=0.9), FadeIn(box_in, scale=0.8), run_time=0.6)
            vo.wait_until("as a service or a job")
            self.play(LaggedStart(FadeIn(svc_w, shift=LEFT * 0.15), FadeIn(job_w, shift=LEFT * 0.15),
                                  lag_ratio=0.4), run_time=0.7)
            vo.wait_until("Its steps")
            self.play(FadeIn(chk, shift=UP * 0.15), run_time=0.6)
            for k, phrase in enumerate(("open Cloud Run", "enable the APIs", "deploy an image")):
                vo.wait_until(phrase)
                self.play(Create(ticks[k]), Indicate(steps[k].text, color=TURN, scale_factor=1.06),
                          run_time=0.6)
            self.play(Indicate(box_in, color=IMAGE, scale_factor=1.08), run_time=0.6)

        # ========================================================== 1. Deploy container: image, name, region
        tr = tracker_22(1)
        svc = form_at(console_form("Services", [("button", "Deploy container")], path="Cloud Run", form_w=8.2))
        ill_s = ill_on(svc)
        fa = form_at(image_form())
        ill_a = ill_on(fa)
        img_row = fa.rows[1]
        ghost_rows = VGroup(*[mono(("$ " if i == 0 else "") + s, 20, S.GREY)
                              for i, s in enumerate(c10.cmd_lines)]).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        ghost_frame = outline_box(ghost_rows.width + 0.5, ghost_rows.height + 0.4, S.GREY, solid=False)
        ghost_rows.move_to(ghost_frame)
        ghost_head = label("S07 · laptop", 20, S.GREY).next_to(ghost_frame, UP, buff=0.08).align_to(ghost_frame, LEFT)
        ghost = VGroup(ghost_frame, ghost_rows, ghost_head).move_to([0, -2.75, 0])
        ws = worksheet_card(SERVICE, "web service").move_to([0, -2.75, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(s14, pic, chk, *ticks)), FadeOut(ref), FadeIn(tr, shift=DOWN * 0.15),
                      run_time=0.7)
            self.play(FadeIn(svc, shift=UP * 0.1), FadeIn(ill_s), run_time=0.5)
            vo.wait_until("Deploy container")
            self.play(svc.press(0), run_time=0.8)
            vo.wait_until("and choose Deploy one revision")
            self.play(ReplacementTransform(svc, fa), ReplacementTransform(ill_s, ill_a), run_time=0.7)
            self.play(Indicate(fa.rows[0].text, color=TURN, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Paste the same image")
            self.play(track(tr, 2), FadeIn(ghost, shift=UP * 0.15), run_time=0.5)
            self.play(fa.fill(1, IMAGE_REF), run_time=0.8)
            img_val = img_row.value
            src = ghost_rows[1]
            thread = CubicBezier(src.get_right() + RIGHT * 0.12, src.get_right() + np.array([1.0, 1.2, 0]),
                                 img_val.get_right() + np.array([1.3, -0.6, 0]), img_val.get_right() + RIGHT * 0.12)
            thread.set_stroke(ROUTE, 3)
            self.play(Create(thread), run_time=0.6)
            self.play(Indicate(img_val, color=ROUTE, scale_factor=1.03),
                      Indicate(src, color=ROUTE, scale_factor=1.03), run_time=0.8)
            vo.wait_until("name it translation-demo")
            self.play(track(tr, 3), FadeOut(thread), FadeOut(ghost), run_time=0.4)
            self.play(FadeIn(ws, shift=UP * 0.2), run_time=0.4)
            self.play(ws.animate.move_to(fa.rows[2].field).set_opacity(0), fa.fill(2, SERVICE), run_time=0.9)
            self.remove(ws)
            vo.wait_until("and choose your region")
            self.play(fa.fill(3, REGION_VALUE), run_time=0.9)

        # ========================================================== 2. public access, request-based, scaling
        fb = form_at(console_form("Create service",
                                  [("note", "Authentication"), ("radio", "Allow public access", False),
                                   ("note", "Billing"), ("radio", "Request-based", False),
                                   ("Service scaling", ""), ("Minimum number of instances", ""),
                                   ("Maximum number of instances", "")], form_w=8.6))
        ill_b = ill_on(fb)
        with self.voiceover(SAY[2]) as vo:
            self.play(ReplacementTransform(fa, fb), ReplacementTransform(ill_a, ill_b),
                      run_time=0.8)
            vo.wait_until("Select Allow public access")
            self.play(track(tr, 4), fb.rows[1].tick.animate.set_opacity(1),
                      Indicate(fb.rows[1].text, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("and Request-based billing")
            self.play(fb.rows[3].tick.animate.set_opacity(1),
                      Indicate(fb.rows[3].text, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Under scaling")
            self.play(track(tr, 5), fb.fill(4, "Auto scaling"), run_time=0.8)
            vo.wait_until("minimum 0 instances")
            self.play(fb.fill(5, "0", TURN), run_time=0.5)
            vo.wait_until("and maximum 2")
            self.play(fb.fill(6, "2", TURN), run_time=0.5)

        # ========================================================== 3. container settings, requests; PORT
        fc = form_at(console_form("Settings",
                                  [("Container port", ""), ("Memory", ""), ("CPU", ""),
                                   ("note", "leave the image's command and arguments unchanged"),
                                   ("button", "Done")],
                                  path="Containers, Networking, Security → Edit Container", form_w=7.6))
        ill_c = ill_on(fc)
        fd = form_at(console_form("Requests", [("Request timeout", ""),
                                               ("Maximum concurrent requests per instance", "")],
                                  path="Containers, Networking, Security", form_w=7.6))
        ill_d = ill_on(fd)
        # V5's envelope, small: a TEAL container with its PINK ear; Cloud Run writes PORT and knocks
        cbox = RoundedRectangle(width=3.3, height=2.4, corner_radius=0.12, stroke_color=IMAGE,
                                stroke_width=3).set_fill(IMAGE, 0.08).move_to([4.75, 0.3, 0])
        clab = label("container", 20, IMAGE).move_to(cbox.get_corner(DR) + np.array([-0.85, 0.25, 0]))
        e = ear("0.0.0.0:8080")
        e.glyph.move_to([cbox.get_left()[0] + 0.12, cbox.get_center()[1] - 0.2, 0])
        e.text.next_to(cbox, DOWN, buff=0.15).align_to(cbox, LEFT)
        gun = tool_chip("gunicorn").move_to(cbox.get_center() + RIGHT * 0.35 + DOWN * 0.1)
        wire = Line(e.glyph.get_right(), gun.get_left(), color=ROUTE, stroke_width=3)
        env = envelope("PORT=8080", CLOUD).move_to([4.85, 1.95, 0])
        who = label("Cloud Run", 20, CLOUD).next_to(env, UP, buff=0.12)
        knock = pulse_dot(CLOUD, 0.11).move_to([2.35, e.glyph.get_center()[1], 0])
        port_pic = VGroup(cbox, clab, gun, e, wire)

        with self.voiceover(SAY[3]) as vo:
            self.play(track(tr, 6), ReplacementTransform(fb, fc), ReplacementTransform(ill_b, ill_c),
                      run_time=0.8)
            vo.wait_until("port 8080")
            self.play(fc.fill(0, "8080", ROUTE), run_time=0.5)
            vo.wait_until("512 mebibytes")
            self.play(fc.fill(1, "512 MiB"), run_time=0.5)
            vo.wait_until("1 CPU")
            self.play(fc.fill(2, "1"), run_time=0.4)
            vo.wait_until("and the command left alone")
            self.play(Indicate(fc.rows[3].text, color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("Cloud Run sets PORT")
            self.play(FadeIn(port_pic, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeIn(env, shift=DOWN * 0.3), FadeIn(who), run_time=0.5)
            self.play(env.animate.next_to(gun, UP, buff=0.12), FadeOut(who), run_time=0.5)
            vo.wait_until("and knocks on it")
            self.add(knock)
            self.play(FadeIn(knock, scale=0.5), run_time=0.2)
            self.play(knock.animate.move_to(e.glyph), run_time=0.6)
            self.play(Indicate(e.text, color=ROUTE, scale_factor=1.12), FadeOut(knock), run_time=0.6)
            vo.wait_until("Then a 120 second timeout")
            self.play(track(tr, 7), ReplacementTransform(fc, fd), ReplacementTransform(ill_c, ill_d),
                      run_time=0.7)
            self.play(fd.fill(0, "120"), run_time=0.5)
            vo.wait_until("and 4 concurrent requests")
            self.play(fd.fill(1, "4", TURN), run_time=0.5)
            self.play(Indicate(fd.rows[1].value, color=TURN, scale_factor=1.4), run_time=0.6)

        # ========================================================== 4. why 4: four threads, two instances
        pool = SlotPool().shift(UP * 0.1)
        th = VGroup(mono("4 threads", 22, OWN), label("(__main__.py:25)", 20, S.GREY),
                    label("= concurrency 4", 22, INK)).arrange(RIGHT, buff=0.15)
        th.move_to([pool.p(0, 0)[0] + 1.65, -1.25, 0])
        ps = grey_chip("--threads 4 in the process list", mono_font=False).next_to(th, DOWN, buff=0.2)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(fd, ill_d, port_pic, env)), run_time=0.5)
            pool.spawn(self, run_time=0.5)
            vo.wait_until("Each instance runs gunicorn")
            self.play(FadeIn(th, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(ps, shift=UP * 0.1), run_time=0.4)
            dots = pool.line_up(self, 4, text=None, run_time=0.4)
            vo.wait_until("so it never gets more")
            pool.fill(self, list(dots), run_time=1.0)
            pool.spawn(self, run_time=0.5)
            pool.ceiling(self, run_time=0.5)

        # ========================================================== 5. scale to zero, the meter, the promise
        strip = InstanceStrip(rows=("serverless",), times=None).shift(UP * 1.2)
        zero = grey_chip("scale to zero").move_to([strip.x(0.42), 1.55, 0])
        sl = Slider("min instances", (0, 1)).move_to([-3.4, -0.55, 0])
        sw = Switch("Request-based", off_text="Instance-based").move_to([2.6, -0.55, 0])
        ref2 = lref("11, 14")
        quote = label("“pay only when your code runs”", 22, INK)
        q_card = card([quote], S.GREY)
        er = erratum_tag()
        green = ok_chip("with these two settings")
        promise = VGroup(er, q_card, green).arrange(RIGHT, buff=0.25).move_to([0, -1.75, 0])
        cost1 = cost_tag("request-based + min 0: billed while serving")
        cost2 = cost_tag("min ≥ 1 or instance-based: idle time billed · check the pricing page")
        costs = VGroup(cost1, cost2).arrange(DOWN, buff=0.12).move_to([0, -2.95, 0])
        assert promise.width < 13.0 and costs.width < 13.0

        with self.voiceover(SAY[5]) as vo:
            pool.dissolve(self, run_time=0.6)
            self.play(FadeOut(pool), FadeOut(VGroup(th, ps)), run_time=0.4)
            self.remove(pool)
            self.play(FadeIn(strip), FadeIn(sl), FadeIn(sw), run_time=0.5)
            vo.wait_until("the meter moves only")
            strip.serve(self, 0.04, 0.24, pulses=(0.07, 0.13, 0.2), run_time=1.0)
            strip.show(self, zero, anims=[FadeIn(zero, scale=0.9)], run_time=0.3)
            strip.serve(self, 0.6, 0.8, pulses=(0.63, 0.7, 0.76), run_time=1.0)
            vo.wait_until("That is the lecture's promise")
            self.play(FadeIn(ref2), FadeIn(q_card, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("pay only when your code runs")
            self.play(Indicate(quote, color=TURN, scale_factor=1.05), FadeIn(er), run_time=0.6)
            self.play(FadeIn(green, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("A minimum of 1")
            self.play(sl.to(1), run_time=0.5)
            life, drip = strip.always_on(self, run_time=1.2)
            vo.wait_until("or instance-based billing")
            self.play(sw.flip(False), run_time=0.5)
            strip.instance_billing(self, True, run_time=0.6)
            vo.wait_until("bills idle time too")
            self.play(FadeIn(cost1, shift=UP * 0.1), FadeIn(cost2, shift=UP * 0.1), run_time=0.5)
            self.play(sl.to(0), sw.flip(True), run_time=0.6)
            strip.drop(self, life, drip, run_time=0.4)
            strip.instance_billing(self, False, run_time=0.6)

        # ========================================================== 6. ten at once (PONDER)
        pool2 = SlotPool().shift(UP * 0.1)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(strip, sl, sw, promise, costs)), FadeOut(ref2), run_time=0.6)
            self.remove(strip)
            pool2.line_up(self, 10, run_time=0.8)
            vo.wait_until("Ten people press Translate")
            self.play(Indicate(pool2.req_label, color=TURN, scale_factor=1.1),
                      LaggedStart(*[Indicate(d, color=ROUTE, scale_factor=1.4) for d in pool2.waiting],
                                  lag_ratio=0.08), run_time=1.0)
            pool2.heal(self)
        pc = ponder(self, PONDER_Q, seconds=8, center=(0.9, 0.2))

        # ========================================================== 7. the answer: two instances, eight slots
        fix1 = VGroup(chip("raise max instances", S.GREY, size=20), check_glyph(0.28, OWN)).arrange(RIGHT, buff=0.2)
        fix2 = VGroup(chip("raise concurrency + threads together", S.GREY, size=20),
                      check_glyph(0.28, OWN)).arrange(RIGHT, buff=0.2)
        fix3 = VGroup(chip("raise min instances", S.GREY, size=20), cross_glyph(0.26),
                      err_chip("warmth, not capacity", mono_font=False)).arrange(RIGHT, buff=0.2)
        fixes = VGroup(fix1, fix2, fix3).arrange(DOWN, buff=0.15, aligned_edge=LEFT).move_to([2.2, -2.55, 0])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            pool2.spawn(self, run_time=0.4)
            pool2.spawn(self, run_time=0.4)
            waiting = list(pool2.waiting)            # dots in front of the slot squares
            pool2.remove(*waiting)
            pool2.add(*waiting)
            left = pool2.fill(self, run_time=1.4)
            assert len(left) == 2
            vo.wait_until("the ceiling")
            pool2.ceiling(self, run_time=0.5)
            vo.wait_until("with 8 slots")
            pool2.counter(self, run_time=0.4)
            self.play(Indicate(pool2.ceiling_line, color=TURN, scale_factor=1.04), run_time=0.6)
            pool2.heal(self)
            vo.wait_until("The other two wait")
            pool2.queue(self, left, run_time=0.6)
            vo.wait_until("and can be refused")
            pool2.refuse(self, left[-1], run_time=0.6)
            vo.wait_until("Raise the maximum")
            self.play(FadeIn(fix1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("or raise concurrency")
            self.play(FadeIn(fix2, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a higher minimum")
            self.play(FadeIn(fix3[0], shift=UP * 0.1), run_time=0.4)
            self.play(Create(fix3[1]), FadeIn(fix3[2], shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 8. Create; the recording; revisions
        fcr = console_form("Create service", [("button", "Create")], form_w=4.2).move_to([0, 1.85, 0])
        r3 = recorded_card("part2-service-recorded", 3, "container GIF").move_to([0, 1.85, 0])
        r4 = recorded_card("part2-service-recorded", 4, "container GIF").move_to([0, 1.85, 0])
        r56 = recorded_card("part2-service-recorded", (5, 6), "container GIF").move_to([0, 1.85, 0])
        rev = instance(2.0, 1.1, inner=True).move_to([-4.3, -1.2, 0])
        rev_card = card(["rev 1 · image + settings"], CLOUD, size=20).next_to(rev, DOWN, buff=0.2)
        rmc = readme_card((295, 296), "A revision is a deployed version of the service’s\nimage and configuration.")
        rmc.move_to([2.6, -1.9, 0])
        yt = your_turn()
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(pool2), FadeOut(fixes), track(tr, 8), run_time=0.6)
            self.remove(pool2)
            self.play(FadeIn(fcr, shift=UP * 0.1), run_time=0.4)
            self.play(fcr.press(0), run_time=0.7)
            self.play(ReplacementTransform(fcr, r3), run_time=0.7)
            vo.wait_until("the recording shows")
            self.play(track(tr, 9), ReplacementTransform(r3, r4), run_time=0.7)
            vo.wait_until("Bonjour à tous")
            self.play(Indicate(r4.body, color=TURN, scale_factor=1.03), run_time=0.7)
            vo.wait_until("Then check Revision History")
            self.play(track(tr, 10), ReplacementTransform(r4, r56), run_time=0.7)
            vo.wait_until("A revision is")
            self.play(FadeIn(rev, scale=0.9), FadeIn(rev_card, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(rmc, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("Pause and deploy yours")
            yt.next_to(r56, DOWN, buff=0.2).align_to(r56, RIGHT)
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)

        # ========================================================== 9. no build this time
        icon = grid_icon(0.7).move_to([-4.6, 0.7, 0])
        cell = icon.cells[1][1]
        cb_box = RoundedRectangle(width=2.8, height=1.5, corner_radius=0.14, stroke_color=TOOL,
                                  stroke_width=3).set_fill(TOOL, 0.12)
        cb_text = label("Cloud Build", 22, INK).move_to(cb_box)
        cb = VGroup(cb_box, cb_text).move_to([0.6, 0.7, 0])
        cb_dash = outline_box(2.8, 1.5, S.GREY, solid=False).move_to(cb_box)
        cb_x = cross_glyph(0.9, S.GREY, 5).move_to(cb_box)
        cb_lab = label("no build this time", 20, S.GREY).next_to(cb_box, DOWN, buff=0.2)
        rm314 = readme_card((314, 315), "We supplied an already-built image, so this deployment\n"
                                        "did not need to build our source.").move_to([0, -2.1, 0])
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(r56, rev, rev_card, rmc, yt)), run_time=0.5)
            self.play(FadeIn(icon, scale=0.8), FadeIn(cb, scale=0.95), run_time=0.5)
            self.play(cell.frame.animate.set_stroke(TURN, 4), cell.fill.animate.set_fill(TURN, 0.25), run_time=0.5)
            self.play(FadeOut(cb_box), FadeIn(cb_dash), cb_text.animate.set_color(S.GREY).set_opacity(0.5),
                      Create(cb_x), FadeIn(cb_lab), run_time=0.7)
            self.play(FadeIn(rm314, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(rm314.body, color=TURN, scale_factor=1.03), run_time=0.9)
            self.wait(0.6)

        # ========================================================== 10. tag vs digest (extra: laptop/15)
        blk = RoundedRectangle(width=4.4, height=1.15, corner_radius=0.12, stroke_color=IMAGE,
                               stroke_width=3).set_fill(IMAGE, 0.2).move_to([-1.6, 1.15, 0])
        serial = mono("@" + digest_short(4, 6), 22, OWN).move_to(blk).shift(DOWN * 0.15)
        blk_lab = label("image", 20, IMAGE).move_to(blk.get_corner(UL) + np.array([0.55, -0.22, 0]))
        dig_lab = label("digest", 20, OWN).next_to(blk, RIGHT, buff=0.2).align_to(serial, DOWN)
        note = sticky(IMAGE_TAG).rotate(0.04).move_to([-1.6, 2.32, 0])
        tag_lab = label("tag", 20, S.GREY).next_to(note, RIGHT, buff=0.2)
        rv = instance(3.9, 1.15, inner=False).move_to([4.55, 1.15, 0])
        rv_lab = label("revision", 20, CLOUD).next_to(rv, UP, buff=0.12)
        er2 = VGroup(erratum_tag(), grey_chip("a tag in the click path · deploy by digest to reproduce"))
        er2.arrange(RIGHT, buff=0.2).move_to([0, -0.05, 0])
        tab = tab_term(5)
        tab.shift(UP * 0.0)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(icon, cb, cb_dash, cb_x, cb_lab, rm314)), run_time=0.4)
            self.play(FadeIn(blk), FadeIn(blk_lab), FadeIn(note, shift=DOWN * 0.1), FadeIn(tag_lab),
                      track(tr, 10, True), FadeIn(tab, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("a movable label")
            self.play(note.animate.shift(RIGHT * 0.5).rotate(-0.08), run_time=0.4)
            self.play(note.animate.shift(LEFT * 0.5).rotate(0.08), run_time=0.4)
            typed = type_capture(self, tab, c15, type_time=1.0)
            vo.wait_until("the revision keeps the digest")
            r15 = out(self, tab, c15.at(2), wrap=True, run_time=0.4, color=OWN)
            self.play(*[Indicate(r, color=OWN, scale_factor=1.03) for r in r15],
                      FadeIn(serial, shift=UP * 0.3), FadeIn(dig_lab), run_time=0.8)
            self.add(tab)
            self.play(FadeIn(rv, scale=0.9), FadeIn(rv_lab), run_time=0.4)
            sc = serial.copy()
            self.play(sc.animate.move_to(rv), run_time=0.7)
            vo.wait_until("To reproduce a deployment")
            self.play(FadeIn(er2, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("deploy by digest")
            self.play(Indicate(serial, color=OWN, scale_factor=1.12), Indicate(sc, color=OWN, scale_factor=1.12),
                      run_time=0.8)
            del typed

        # ========================================================== 11. the gcloud alternative (README:321-324)
        gt = gcloud_term(6)
        groups = [("image", '--image="$IMAGE"'), ("access", "--no-invoker-iam-check"),
                  ("scaling", "--min-instances=0 --max-instances=2"),
                  ("resources", "--cpu=1 --memory=512Mi --concurrency=4 --timeout=120")]
        gchips = VGroup(*[chip(n, S.GREY, size=20) for n, _ in groups]).arrange(RIGHT, buff=0.35)
        gchips.move_to([0, 1.0, 0])
        npc = no_panel_chip()
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(blk, blk_lab, serial, dig_lab, note, tag_lab, rv, rv_lab, sc, er2, tab)),
                      track(tr, 8, "gcloud"), run_time=0.5)
            self.play(FadeIn(gt, shift=UP * 0.15), FadeIn(gchips), run_time=0.4)
            lines = type_lines(self, gt, gc_rows, type_time=0.45)
            rows = all_rows(lines)
            rings = []
            for (name, sub), gc in zip(groups, gchips):
                r = row_with(rows, sub)
                rg = ring(substring(r, sub), TURN)
                rings.append(rg)
                self.play(Create(rg), gc.box.animate.set_stroke(TURN), gc.text.animate.set_color(TURN),
                          run_time=0.35)
                self.add(gt, rg)
            under_term(gt, npc)
            self.play(FadeIn(npc, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 12. a public URL; the parked question
        page = TranslatePage(SERVICE_URL, CLOUD).move_to([0, 0.75, 0])
        q = _Quiet()
        page.set_dest(q, "fr")
        page.left_text = page._boxtext(page.left, "Good afternoon everyone")
        page.add(page.left_text)
        page.right_text = page._boxtext(page.right, "Bonjour à tous")
        page.add(page.right_text)
        ill_p = illustration_tag().next_to(page.frame, RIGHT, buff=0.2).align_to(page.frame, UP)
        qc = question_card("To speak, the app must call an API that asks who is calling.\nWho is it?",
                           size=24).move_to([0, -2.55, 0])
        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(VGroup(gt, gchips, npc, *rings)), track(tr, 10, False), run_time=0.6)
            self.remove(*self.mobjects)
            self.add(tr)
            self.play(FadeIn(page, shift=UP * 0.15), FadeIn(ill_p), run_time=0.6)
            vo.wait_until("at a public URL")
            self.play(Indicate(page.url, color=CLOUD, scale_factor=1.06), run_time=0.7)
            vo.wait_until("But Play audio still waits")
            self.play(page.press("audio", TURN), run_time=0.8)
            page.heal(self)
            vo.wait_until("to speak, the app")
            self.play(FadeIn(qc, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Who is it?")
            self.play(Indicate(qc.body[1], color=TURN, scale_factor=1.1), page.press("audio", TURN), run_time=0.9)
            page.heal(self)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)


class _Quiet:
    """A stand-in 'scene' for assembling a set piece's state without playing it."""

    mobjects: list = []

    def play(self, *a, **k):
        pass

    def add(self, *m):
        pass

    def remove(self, *m):
        pass
