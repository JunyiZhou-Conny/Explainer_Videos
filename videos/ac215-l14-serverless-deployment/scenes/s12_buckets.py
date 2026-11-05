"""S12 · Finite work: a job and two buckets — no tracker in blocks 0-3, then tracker [4.1] 1 → 6
(+ extra at step 5, gcloud alternative at step 4); lecture_ref 14 (blocks 0-1) and 9 (block 2).

Beats (script.md "## S12"; one voiceover block each):
0. No tracker. LECTURE 14 · 14. A README card (README.md · lines 582–585): "… The program should
   read its input, translate it, generate speech, save the files, and exit. That is a job …"
   ("job" BLUE). A GREY person waiting at a browser on the left (dots pulse "waiting"); a sealed
   GREY envelope "audio edition · collect later" on the right.
1. V1 (no sketch) returns centred; at "a service or as a job" the container · serverless cell lights
   and splits into "service | job". At "Same image, two programs" the grid gives way to V7
   LifecycleStrips: the TEAL image block with `serve` and `batch` hanging under it, and
   CODE(tutorial/app/translation_demo/__main__.py: 12–13) (cut, small) top right. The service strip
   (dashed instance, PINK ear, pulses, no right edge) while "serve" is said; the job strip (four
   segments take input → translate → speak → save, `__main__.py:52-57`, hard edge "exit 0") runs
   while "batch" is said.
2. LECTURE 14 · 9. A GREY-dashed chip "LAST WEEK · Vertex AI training job (L13)" drops under the job
   strip with its own dashed strip start → train → save | exit; the segments of both strips pulse
   in step.
3. The L13 strip and the code panel leave. Under the job instance: GREY chip "no URL" (the service's
   PINK ear flashes for contrast); the disk icon vanishes, chip "no URL · local disk gone". The
   service strip leaves; the two BLUE buckets arrive (PINK gs://… arrow in, files out). A GREY
   laptop with passage.txt tries to hand it straight in: its arrow stops at a RED cross; README card
   (README.md · lines 918–919) "… a remote container cannot read a filename on your laptop."
4. TRACKER [4.1] 1 appears with the two blank worksheet bucket cards on the right ("input bucket" /
   "output bucket", dashed). CONSOLE (README:595-613, illustration): "Cloud Storage → Buckets ·
   Create". [4.1] 2: "Get started", Name YOUR_GLOBALLY_UNIQUE_INPUT_BUCKET, hint "e.g. your project
   ID + -translation-input". [4.1] 3: the wizard's rows fill one per phrase (Region
   northamerica-northeast2 (Toronto), Standard, Enforce public access prevention ✓, Uniform, Soft
   delete · default retention ✓, Object versioning unchecked); Create → a veiled form under the
   dialog "Public access will be prevented · Confirm" → the input card fills (YOUR_INPUT_BUCKET)
   with a BLUE bucket "Public access: Not public". ▶ your turn.
5. [4.1] 4: the name swaps to YOUR_GLOBALLY_UNIQUE_OUTPUT_BUCKET, the settings rows pulse, Create;
   the output card fills. The form leaves, the two cards move to the centre; GOLD cost tags "two
   buckets · storage bills while files exist" / "soft delete keeps deleted files for a while · check
   the pricing page".
6. [4.1] 5: CONSOLE "YOUR_INPUT_BUCKET · Objects": Create folder → run-001 → Create. Then the form
   becomes "Upload" (README:615-618) and [4.1] 5 · extra: a 6-row `laptop` terminal types
   `cat tutorial/app/examples/passage.txt` (extra tag beside it) → TERM(laptop/40: 2–5); a
   passage.txt file icon rises from the terminal to "Upload → Upload files". [4.1] 6: "Object
   details · Live object · Cloud Storage URI" with a copy icon: gs://YOUR_INPUT_BUCKET/run-001/
   passage.txt in PINK (README:619-621). ▶ your turn.
7. The URI splits into PINK segments; run-001/ rings, GREY chip "a prefix you chose · not a
   directory" (README:887-891). [4.1] 4 · gcloud alternative: terminal `laptop · gcloud` (20 pt)
   types README:661-672 verbatim, no output panel. Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.devops import laptop
from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S12"]

FORM_UL = np.array([-6.45, 2.72, 0])                 # forms hang from here, under the tracker
URI = f"gs://{IN_BUCKET}/run-001/passage.txt"        # README:621
IN_NAME, OUT_NAME = "YOUR_GLOBALLY_UNIQUE_INPUT_BUCKET", "YOUR_GLOBALLY_UNIQUE_OUTPUT_BUCKET"


def form_at(f: VGroup) -> VGroup:
    return f.move_to(FORM_UL, aligned_edge=UL)


def ill_for(f: VGroup) -> VGroup:
    """The illustration tag on the form's top edge, right end."""
    tg = illustration_tag()
    return tg.move_to(f.frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))


def sealed_envelope(text: str = "audio edition · collect later") -> VGroup:
    """A sealed GREY envelope with a label-font line under the flap (beat 0)."""
    t = label(text, 20, INK)
    w, h = t.width + 0.6, 1.1
    body = Rectangle(width=w, height=h, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1)
    flap = VMobject(stroke_color=S.GREY, stroke_width=2.5).set_points_as_corners(
        [body.get_corner(UL), body.get_center() + UP * 0.12, body.get_corner(UR)])
    seal = Circle(radius=0.1, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.6).move_to(
        body.get_center() + UP * 0.12)
    t.move_to(body).shift(DOWN * 0.28)
    g = VGroup(body, flap, seal, t)
    g.text = t
    return g


def copy_icon(h: float = 0.3, color=S.GREY) -> VGroup:
    a = RoundedRectangle(width=h * 0.8, height=h, corner_radius=0.04, stroke_color=color, stroke_width=2)
    b = a.copy().shift(np.array([h * 0.25, h * 0.25, 0])).set_fill(PANEL, 1)
    return VGroup(b, a.set_fill(PANEL, 1))


def gcloud_rows():
    """README:661-672 as command groups: each a list of rows (a row after a trailing '\\' continues)."""
    rows = readme_rows(661, 672)
    groups, cur = [], []
    for r in rows:
        cur.append(r)
        if not r.rstrip().endswith("\\"):
            groups.append(cur)
            cur = []
    assert not cur and len(groups) == 6, groups
    return groups


class JobAndBuckets(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S12"] == 8, len(SAY)
        assert "should read its input, translate it, generate speech, save the files, and exit." in readme(584)
        assert readme(585).startswith("That is a **job**")
        assert readme(918).endswith("a remote container cannot read") and readme(919) == "a filename on your laptop."
        assert "northamerica-northeast2 (Toronto)" in readme(600) + readme(601)
        assert f"`{URI}`" in readme(621), readme(621)
        assert "`run-001` is a prefix you selected" in readme(887)
        c40 = capture("laptop/40")
        assert c40.cmd == "cat tutorial/app/examples/passage.txt" and len(c40.at((2, 5))) == 4
        groups = gcloud_rows()

        # ========================================================== 0. a person waits; an edition is collected later
        ref14 = lref("14")
        r1 = label("… The program should read its input, translate it,", 22, INK)
        r2 = label("generate speech, save the files, and exit.", 22, INK)
        r3a = label("That is a", 22, INK)
        r3b = label("job", 22, CLOUD, weight=BOLD)
        r3c = label("…", 22, INK)
        r3 = VGroup(r3a, r3b, r3c).arrange(RIGHT, buff=0.12)
        r3b.align_to(r3a, DOWN)
        body0 = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        card0 = readme_card((582, 585), body0, quote=True).move_to([0, 1.55, 0])
        person = you("a person").move_to([-5.4, -1.7, 0])
        brw = browser_icon(1.4, name=None)
        brw.next_to(person.figure, RIGHT, buff=0.35).align_to(person.figure, DOWN)
        dots = VGroup(*[Dot(radius=0.07, color=S.GREY) for _ in range(3)]).arrange(RIGHT, buff=0.14)
        dots.move_to(brw.window[0].get_center() + DOWN * 0.08)
        wait_t = label("waits for the response", 20, S.GREY).next_to(VGroup(person, brw), DOWN, buff=0.25)
        wait_t.align_to(person, LEFT)
        env = sealed_envelope().move_to([3.6, -1.6, 0])
        assert card0.get_top()[1] < PIC_TOP and env.get_right()[0] < 6.5 and wait_t.get_bottom()[1] > -3.5
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref14, shift=LEFT * 0.1), FadeIn(card0, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("A web request has a person waiting")
            self.play(FadeIn(person, shift=UP * 0.1), FadeIn(brw), FadeIn(dots), run_time=0.6)
            self.play(FadeIn(wait_t, shift=UP * 0.1),
                      LaggedStart(*[Indicate(d, color=INK, scale_factor=1.6) for d in dots], lag_ratio=0.3),
                      run_time=1.0)
            vo.wait_until("but a translated audio edition")
            self.play(FadeIn(env, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("should take its input")
            self.play(Indicate(r1, color=TURN, scale_factor=1.03), run_time=0.8)
            vo.wait_until("save the files and exit")
            self.play(Indicate(r2, color=TURN, scale_factor=1.03), run_time=0.8)
            vo.wait_until("That is a job")
            self.play(Indicate(r3b, color=CLOUD, scale_factor=1.3),
                      Indicate(env, color=CLOUD, scale_factor=1.05), run_time=0.8)

        # ========================================================== 1. service | job; one image, two programs
        grid = DeployGrid(built=True, sketch=False)
        seen = VGroup(*[grid.cells[r][c].frame for r in range(2) for c in range(2)], grid.cols, grid.rows_)
        grid.shift(np.array([0, 0.3, 0]) - seen.get_center())
        strips = LifecycleStrips(show=())
        cp = code("tutorial/app/translation_demo/__main__.py", 12, 13, font_size=20, dedent=True,
                  cuts={12: '"serve",', 13: '"batch",'})
        cp.move_to([6.5 - cp.width / 2, 2.75 - cp.height / 2, 0])
        assert cp.get_left()[0] > strips.image.get_right()[0] + 0.3, cp.get_left()
        bar_s, bar_b = line_bar(cp.code, 0, TURN), line_bar(cp.code, 1, TURN)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(card0, person, brw, dots, wait_t, env)), run_time=0.5)
            self.play(FadeIn(grid), run_time=0.7)
            vo.wait_until("a service or as a job")
            self.play(grid.light(1, 1), run_time=0.4)
            grid.split_job(self, run_time=1.0)
            self.play(Indicate(grid.split.job, color=CLOUD, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Same image, two programs")
            self.play(FadeOut(grid), run_time=0.4)
            self.play(FadeIn(strips, shift=DOWN * 0.1), FadeIn(cp, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("serve keeps listening")
            self.play(FadeIn(bar_s), Indicate(strips.cmds[0], color=TURN, scale_factor=1.15), run_time=0.5)
            strips.show_strip(self, "service", run_time=0.5)
            strips.serve(self, n=4, run_time=1.6)
            vo.wait_until("batch walks four steps")
            self.play(FadeOut(bar_s), FadeIn(bar_b), Indicate(strips.cmds[1], color=TURN, scale_factor=1.15),
                      run_time=0.5)
            strips.show_strip(self, "job", run_time=0.4)
            strips.run_job(self, run_time=2.0)

        # ========================================================== 2. last week's training job: the same shape
        ref9 = lref("9")
        js = strips.job_strip
        segs = js.segs
        y13 = -2.85
        l13 = VGroup()
        # start ↔ take input, train ↔ translate + speak, save ↔ save, exit ↔ exit (the pairs pulse together)
        for (a, b), s in zip(((0, 0), (1, 2), (3, 3)), ("start", "train", "save")):
            x0, x1 = segs[a].frame.get_left()[0], segs[b].frame.get_right()[0]
            r = DashedVMobject(RoundedRectangle(width=x1 - x0, height=0.55, corner_radius=0.08),
                               num_dashes=30 if a == b else 50).set_stroke(PAST, 2)
            r.move_to([(x0 + x1) / 2, y13, 0])
            t = label(s, 20, PAST).move_to(r)
            l13.add(VGroup(r, t))
        e13 = DashedLine([js.edge.get_center()[0], y13 + 0.4, 0], [js.edge.get_center()[0], y13 - 0.4, 0],
                         color=PAST, stroke_width=5)
        x13 = label("exit", 20, PAST).next_to(e13, RIGHT, buff=0.12)
        assert x13.get_right()[0] < 6.55, x13.get_right()
        last = dashed_chip("LAST WEEK · Vertex AI training job (L13)").move_to([0, -2.1, 0])
        last.align_to(segs[0].frame, LEFT)
        strip13 = VGroup(l13, e13, x13)
        assert last.get_bottom()[1] > l13.get_top()[1] + 0.05 and last.get_top()[1] < js.exit_label.get_bottom()[1] \
            or last.get_right()[0] < js.exit_label.get_left()[0]
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(bar_b), ReplacementTransform(ref14, ref9), run_time=0.5)
            vo.wait_until("You have seen this shape before")
            self.play(FadeIn(last, shift=DOWN * 0.2), FadeIn(strip13, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("last week's Vertex AI training job")
            self.play(Indicate(last, color=S.GREY, scale_factor=1.06), run_time=0.7)
            vo.wait_until("start, train, save, exit")
            for k, mine in enumerate((segs[0], VGroup(segs[1], segs[2]), segs[3])):
                self.play(Indicate(l13[k], color=INK, scale_factor=1.06),
                          Indicate(mine, color=IMAGE, scale_factor=1.04), run_time=0.45)
            self.play(Indicate(VGroup(e13, x13), color=INK, scale_factor=1.1),
                      Indicate(VGroup(js.edge, js.exit_label), color=INK, scale_factor=1.1), run_time=0.5)
            strips.heal(self)

        # ========================================================== 3. no URL, no disk: buckets; not your laptop
        nourl = grey_chip("no URL")
        nourl.next_to(js.inst, UP, buff=0.12)
        gone = grey_chip("no URL · local disk gone")
        gone.next_to(js.inst, UP, buff=0.12)
        lap = laptop(1.3).move_to([-0.6, 0.75, 0])
        pfile = file_icon("passage.txt", INK, 0.32).next_to(lap, RIGHT, buff=0.25)
        tgt = segs[0].frame.get_top() + np.array([0.6, 0.05, 0])
        hand = Arrow(lap.get_bottom() + DOWN * 0.05, tgt, buff=0.05, color=S.GREY, stroke_width=4, tip_length=0.18)
        mid = hand.point_from_proportion(0.55)
        stop = cross_glyph(0.36).move_to(mid)
        rc = readme_card((918, 919), "… a remote container cannot read\na filename on your laptop.")
        rc.move_to([6.5 - rc.width / 2, 2.75 - rc.height / 2, 0])
        assert rc.get_left()[0] > strips.image.get_right()[0] + 0.2 and rc.get_bottom()[1] > lap.get_top()[1] - 0.6
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(last, strip13, ref9, cp)), run_time=0.5)
            vo.wait_until("A job has no URL")
            self.play(Indicate(strips.serve_strip.ear, color=ROUTE, scale_factor=1.4), run_time=0.6)
            strips.show(self, nourl, run_time=0.4)
            vo.wait_until("and its disk vanishes")
            strips.drop(self, js.disk, run_time=0.5)
            strips.swap(self, nourl, gone, run_time=0.5)
            vo.wait_until("So input comes from Storage")
            strips.drop(self, strips.serve_strip, run_time=0.4)
            strips.buckets(self, run_time=1.4)
            vo.wait_until("a remote container cannot see")
            self.play(FadeIn(lap), FadeIn(pfile, shift=LEFT * 0.1), run_time=0.5)
            self.play(GrowArrow(hand), run_time=0.6)
            self.play(hand.animate.set_color(ERR), FadeIn(stop, scale=0.6), run_time=0.4)
            self.play(FadeIn(rc, shift=LEFT * 0.1), run_time=0.5)
            self.wait(0.6)

        # ========================================================== 4. steps 1-3: create the input bucket
        tr = tracker_41(1)
        f1 = form_at(console_form("Buckets", [("button", "Create")], form_w=8.4, path="Cloud Storage → Buckets"))
        ill1 = ill_for(f1)
        f2 = form_at(console_form("Get started", [("Name", ""), ("note", "e.g. your project ID + -translation-input"),
                                                  ("button", "Continue")], form_w=8.4,
                                  path="Cloud Storage → Buckets → Create a bucket"))
        ill2 = ill_for(f2)
        wiz = form_at(console_form("Create a bucket", [
            ("Name", IN_NAME), ("Region", ""), ("Default class", ""),
            ("check", "Enforce public access prevention", False), ("radio", "Uniform", False),
            ("check", "Soft delete · default retention", False), ("check", "Object versioning", False),
            ("button", "Create")], form_w=8.4))
        ill3 = ill_for(wiz)
        veil = wiz.frame.copy().set_stroke(width=0).set_fill(S.BG, 0.75)
        modal = console_form("Public access will be prevented",
                             [("check", "Enforce public access prevention on this bucket", True),
                              ("button", "Confirm")], form_w=7.0)
        modal.move_to(wiz.frame)
        assert wiz.frame.get_right()[0] < 2.3 and wiz.frame.get_bottom()[1] > -3.5, wiz.frame.get_corner(DR)
        w_in, w_out = worksheet_card(None, "input bucket"), worksheet_card(None, "output bucket")
        f_in, f_out = worksheet_card(IN_BUCKET, "input bucket"), worksheet_card(OUT_BUCKET, "output bucket")

        def not_public():
            return VGroup(bucket(None, 0.5), label("Public access: Not public", 20, OWN)).arrange(RIGHT, buff=0.2)
        np_in, np_out = not_public(), not_public()
        col = VGroup(VGroup(f_in, np_in).arrange(DOWN, buff=0.2), VGroup(f_out, np_out).arrange(DOWN, buff=0.2))
        col.arrange(DOWN, buff=0.6).move_to([4.45, 0.5, 0])
        w_in.move_to(f_in)
        w_out.move_to(f_out)
        assert col.get_left()[0] > wiz.frame.get_right()[0] + 0.1 and col.get_right()[0] < 6.55, col.get_left()
        turn4 = your_turn().next_to(wiz, DOWN, buff=0.3).align_to(wiz, LEFT)
        assert turn4.get_bottom()[1] > -3.55
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(Group(*[m for m in self.mobjects])), run_time=0.6)
            self.remove(*self.mobjects)
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(f1, shift=UP * 0.1), FadeIn(ill1), run_time=0.6)
            self.play(FadeIn(w_in, shift=LEFT * 0.1), FadeIn(w_out, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Buckets, Create")
            self.play(f1.press(0), run_time=0.6)
            vo.wait_until("Step 2")
            self.play(track(tr, 2), FadeOut(f1), FadeOut(ill1), run_time=0.4)
            self.play(FadeIn(f2, shift=UP * 0.1), FadeIn(ill2), run_time=0.4)
            vo.wait_until("a globally unique name")
            self.play(f2.fill(0, IN_NAME), run_time=0.9)
            vo.wait_until("such as your project ID")
            self.play(Indicate(f2.rows[1].text, color=TURN, scale_factor=1.05), run_time=0.7)
            self.play(f2.press(2), run_time=0.4)
            vo.wait_until("Step 3")
            self.play(track(tr, 3), FadeOut(f2), FadeOut(ill2), run_time=0.4)
            self.play(FadeIn(wiz, shift=UP * 0.1), FadeIn(ill3), run_time=0.4)
            vo.wait_until("region Toronto")
            self.play(wiz.fill(1, f"{REGION} ({REGION_CITY})"), run_time=0.8)
            vo.wait_until("class Standard")
            self.play(wiz.fill(2, "Standard"), run_time=0.4)
            for i, phrase in ((3, "public access prevention"), (4, "uniform access"), (5, "default soft delete")):
                vo.wait_until(phrase)
                self.play(wiz.rows[i].tick.animate.set_opacity(1), Indicate(wiz.rows[i].text, color=TURN,
                                                                            scale_factor=1.04), run_time=0.5)
            vo.wait_until("then Create and Confirm")
            self.play(wiz.press(7), run_time=0.5)
            self.play(FadeIn(veil), FadeIn(modal, scale=0.95), run_time=0.4)
            self.play(modal.press(1), run_time=0.5)
            self.play(FadeOut(modal), FadeOut(veil), ReplacementTransform(w_in, f_in),
                      FadeIn(np_in, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Pause and create it")
            self.play(FadeIn(turn4, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 5. step 4: the output bucket; what bills
        c1 = cost_tag("two buckets · storage bills while files exist")
        c2 = cost_tag("soft delete keeps deleted files for a while · check the pricing page")
        costs = VGroup(c1, c2).arrange(DOWN, buff=0.2).move_to([0, -2.3, 0])
        pair = col.copy()
        pair[0].move_to([-2.4, 0.9, 0])
        pair[1].move_to([2.4, 0.9, 0])
        assert costs.width < 13
        with self.voiceover(SAY[5]) as vo:
            vo.wait_until("Step 4")
            self.play(track(tr, 4), FadeOut(turn4), run_time=0.4)
            new_name = mono(OUT_NAME, 20, INK).move_to(wiz.rows[0].value, aligned_edge=LEFT)
            self.play(Transform(wiz.rows[0].value, new_name), Indicate(w_out, color=CLOUD, scale_factor=1.05),
                      run_time=0.7)
            self.play(*[Indicate(wiz.rows[i], color=OWN, scale_factor=1.02) for i in range(1, 6)], run_time=0.6)
            self.play(wiz.press(7), run_time=0.4)
            self.play(ReplacementTransform(w_out, f_out), FadeIn(np_out, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("A gold tag")
            self.play(FadeOut(VGroup(wiz, ill3)), run_time=0.4)
            self.play(VGroup(f_in, np_in).animate.move_to(pair[0]), VGroup(f_out, np_out).animate.move_to(pair[1]),
                      FadeIn(c1, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("soft delete keeps deleted ones")
            self.play(FadeIn(c2, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(c2, color=COST, scale_factor=1.04), run_time=0.7)

        # ========================================================== 6. steps 5-6: folder, upload, copy the URI
        f5 = form_at(console_form(f"{IN_BUCKET} · Objects", [("button", "Create folder"), ("Folder name", ""),
                                                            ("button", "Create")], form_w=8.4))
        ill5 = ill_for(f5)
        f5b = form_at(console_form("Upload", [("button", "Upload → Upload files")], form_w=8.4,
                                   path=f"{IN_BUCKET} → run-001"))
        ill5b = ill_for(f5b)
        lt = term(P_REPO, 6, T_LAPTOP, size=20)
        assert lt.box.get_top()[1] < f5b.frame.get_bottom()[1] - 0.2, (lt.box.get_top(), f5b.frame.get_bottom())
        f6 = form_at(console_form("Object details · Live object",
                                  [("Cloud Storage URI", "")], form_w=11.0,
                                  path=f"Cloud Storage → Buckets → {IN_BUCKET} → run-001 → passage.txt"))
        ill6 = ill_for(f6)
        cpy = copy_icon().next_to(f6.rows[0].field, RIGHT, buff=0.25)
        assert cpy.get_right()[0] < 6.55, cpy.get_right()
        assert mono(URI, 20).width < f6.rows[0].field.width - 0.3
        turn6 = your_turn().next_to(f6, DOWN, buff=0.3).align_to(f6, LEFT)
        with self.voiceover(SAY[6]) as vo:
            vo.wait_until("Step 5")
            self.play(track(tr, 5), FadeOut(VGroup(f_in, f_out, np_in, np_out, c1, c2)), run_time=0.5)
            self.play(FadeIn(f5, shift=UP * 0.1), FadeIn(ill5), run_time=0.4)
            vo.wait_until("create a folder named")
            self.play(f5.press(0), run_time=0.5)
            self.play(f5.fill(1, "run-001"), run_time=0.6)
            self.play(f5.press(2), run_time=0.4)
            vo.wait_until("and upload the sample passage")
            self.play(FadeOut(VGroup(f5, ill5)), FadeIn(f5b, shift=UP * 0.1), FadeIn(ill5b),
                      track(tr, 5, True), FadeIn(lt, shift=UP * 0.15), run_time=0.6)
            typed = type_capture(self, lt, c40, type_time=0.8)
            pin(self, typed[0], beside(extra_row(), typed[0]))
            vo.wait_until("four short lines")
            out(self, lt, c40.at((2, 5)), run_time=0.8)
            up = file_icon("passage.txt", INK, 0.32).move_to(lt.box.get_center() + RIGHT * 3.5)
            self.play(FadeIn(up, scale=0.7), track(tr, 5), run_time=0.4)
            self.play(up.animate.next_to(f5b.rows[0], RIGHT, buff=0.35), f5b.press(0), run_time=0.9)
            vo.wait_until("Step 6")
            self.play(track(tr, 6), FadeOut(VGroup(lt, f5b, ill5b, up)), run_time=0.5)
            self.play(FadeIn(f6, shift=UP * 0.1), FadeIn(ill6), run_time=0.4)
            vo.wait_until("copy its Storage URI")
            self.play(f6.fill(0, URI, color=ROUTE), run_time=0.9)
            self.play(FadeIn(cpy, scale=0.7), run_time=0.3)
            vo.wait_until("Pause, upload and copy")
            self.play(FadeIn(turn6, shift=UP * 0.1), Indicate(cpy, color=TURN, scale_factor=1.4), run_time=0.6)

        # ========================================================== 7. a prefix, not a directory; the gcloud box
        u = mono(URI, 24, ROUTE).move_to([0, 1.0, 0])
        cuts_ = [0, len("gs://"), len(f"gs://{IN_BUCKET}/"), len(f"gs://{IN_BUCKET}/run-001/"), len(URI)]
        useg = [VGroup(*u[a:b]) for a, b in zip(cuts_, cuts_[1:])]
        spread = [-0.45, -0.15, 0.15, 0.45]
        pre = grey_chip("a prefix you chose · not a directory")
        gt = term(P_REPO, 13, T_GCLOUD, size=20)
        npc = no_panel_chip()
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(f6, ill6, cpy, turn6)), FadeIn(u), run_time=0.6)
            self.remove(u)
            self.add(*useg)
            self.play(*[s.animate.shift(RIGHT * d) for s, d in zip(useg, spread)], run_time=0.7)
            vo.wait_until("a prefix you chose")
            rg = ring(useg[2], TURN)
            pre.next_to(useg[2], DOWN, buff=0.45)
            self.play(Create(rg), run_time=0.4)
            self.play(FadeIn(pre, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("The gcloud alternative")
            self.play(FadeOut(VGroup(*useg, rg, pre)), track(tr, 4, "gcloud"), run_time=0.5)
            self.play(FadeIn(gt, shift=UP * 0.15), run_time=0.4)
            for g in groups:
                type_lines(self, gt, g, type_time=0.8 / len(g) if len(g) > 1 else 0.8)
            under_term(gt, npc)
            assert npc.get_top()[1] < TRACK_BOTTOM - 0.05
            self.play(FadeIn(npc, shift=DOWN * 0.1), run_time=0.4)
            self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
