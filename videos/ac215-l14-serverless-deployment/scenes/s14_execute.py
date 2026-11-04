"""S14 · Execute it and collect the files — tracker [4.4] 1 → 5 (+ extra at step 1, gcloud alternative
at step 1); lecture_ref 14 · slide 16 in blocks 0-5.

Beats (script.md "## S14"; one voiceover block each):
0. TRACKER [4.4] 1 appears; LECTURE 14 · 16. CONSOLE (README:828-830, illustration) "Cloud Run →
   Jobs · translation-audio": Execute pulses (GREY chip "narrow toolbar: More actions ⋮"). The
   History row: RECORDED(expected/part4-job-recorded.txt: 3) with a GREEN check, tag `recorded ·
   README:859`. V7's job strip (LifecycleStrips, job only) runs its four segments to "exit 0".
1. [4.4] 1 · extra. The strip rises; a 7-row `laptop` terminal types laptop/42 lines 1-4 (extra; the
   image's own examples/passage.txt, no speech flag) → TERM(laptop/42: 5, wrap) RED, row tag
   "exit 1"; the strip fails at "speak" and its edge reads RED "exit 1". CODE(__main__.py: 59–61)
   between them, line 59 YELLOW. The edge goes back to "exit 0" (History tells the truth).
2. [4.4] 2: CONSOLE "Tasks" with View logs (README:830-833). README card (README.md · line 833) "The
   job exits; it does not provide a web URL."; the strip's instance has no ear (GREY "no URL").
   Then the log panel (illustration): the JSON shape of expected/part4-task-log-shape.txt lines
   2-12 (two long URI lines cut with '…'), chip "the shape · keys from storage.py:48-56";
   output/manifest URIs PINK, status complete GREEN, the files' lines lit.
3. [4.4] 3: V8 AttemptFolders: the BLUE output bucket, PINK prefix tab run-001/ (chip "yours, from
   the arguments"); the folder `de2f41…/` drops in (tag `recorded · README:860`, GREY chip "a random
   name"). [4.4] 4: the three files land; the README's table (README.md · lines 838–842) gives each
   its description.
4. The order: the bucket gives way to CODE(storage.py: 45–55) (20 pt, cut lines), line 46 and
   `if_generation_match=0` GREEN; translated.txt and speech.wav land beside it with a GREEN "create
   only" stamp; the manifest's lines 48–55 light and manifest.json lands LAST with the receipt.
5. The bucket returns; the where-to-look card (slots 1-2 as in S10) fills slot 3 "the job's logs and
   manifest"; a GREEN check "exit 0" vs the receipt: chip "exit 0 ≠ work complete". V8 replay with a
   failure after the audio: two files, no receipt, folder RED "not a success"; README card
   (README.md · lines 893–895). The lecture tag leaves.
6. The bucket with one complete attempt folder. PONDER (6 s) on the right.
7. A second folder `<attempt>/` lands beside the first with all three files; GREY chip "a random UUID
   per attempt · storage.py · lines 37–38"; a GREEN shield on the first ("create only"); GOLD cost
   tag "a retry = paid work again · retries 0" (README:895-897).
8. [4.4] 5: CONSOLE object list (README:844-848, illustration) with download icons; the text opens in
   a tab: RECORDED(expected/part4-job-recorded.txt: 10), tag `recorded · results GIF`; GREY chip for
   the WAV "media tab · ⋮ → Download". ▶ your turn. GOLD cost tag "one execution = its task's running
   time + one TTS call · check the pricing page".
9. [4.4] 1 · gcloud alternative: terminal `laptop · gcloud` (20 pt) types README:872-876 verbatim, no
   output panel (GREY chip); `--wait` ringed, GREY chip "--wait waits · does not stream app logs"
   (README:879-880).
10. [4.4] 5: README card (README.md · lines 850–851, Checkpoint) on top; V7's job strip ends at its
    edge, its instance goes (the process stopped); V8's bucket with both folders takes its place.
    Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S14"]

FORM_UL = np.array([-6.45, 2.72, 0])                 # forms hang from here, under the tracker
MAIN_PY = "tutorial/app/translation_demo/__main__.py"
STORAGE_PY = "tutorial/app/translation_demo/storage.py"
PONDER_Q = "Execute the same job again,\nsame arguments. Is the first\nresult overwritten?"
TABLE = ("The complete translated passage", "Its generated audio", "Completion status and output locations")


def ill_for(f: VGroup) -> VGroup:
    """The illustration tag on a form's top edge, right end."""
    tg = illustration_tag()
    return tg.move_to(f.frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))


def dl_glyph(h: float = 0.32, color=INK) -> VGroup:
    """A small download icon (an arrow onto a tray), text-free."""
    a = Arrow([0, h / 2, 0], [0, -h / 4, 0], buff=0, color=color, stroke_width=3, tip_length=0.12,
              max_tip_length_to_length_ratio=0.5)
    tray = Line([-h * 0.4, -h / 2, 0], [h * 0.4, -h / 2, 0], color=color, stroke_width=3)
    return VGroup(a, tray)


def object_list(path: str, title: str, names) -> VGroup:
    """A schematic console object list (illustration): breadcrumb, title, one row per object with its
    download icon at the right. .frame .rows (each .icon .dl)"""
    rows = VGroup()
    for n in names:
        fi = file_icon(n)
        rows.add(fi)
    rows.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    pt = label(path, 20, S.GREY)
    tt = label(title, 24, INK)
    head = VGroup(pt, tt).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    w = max(body.width + 1.4, 5.6)
    frame = RoundedRectangle(width=w, height=body.height + 0.6, corner_radius=0.14, stroke_color=S.GREY_DARK,
                             stroke_width=2).set_fill(PANEL, 1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    sep = Line(frame.get_left() + RIGHT * 0.15, frame.get_right() + LEFT * 0.15, color=S.GREY_DARK,
               stroke_width=1.5).move_to([frame.get_center()[0], head.get_bottom()[1] - 0.15, 0])
    dls = VGroup()
    for r in rows:
        d = dl_glyph().move_to([frame.get_right()[0] - 0.5, r.get_center()[1], 0])
        r.dl = d
        dls.add(d)
    g = VGroup(frame, sep, head, rows, dls)
    g.frame, g.rows, g.dls = frame, rows, dls
    return g


def log_panel() -> VGroup:
    """The task log's last output: the JSON shape of expected/part4-task-log-shape.txt (an
    illustration; the two longest URI lines cut with the house '…' to fit 20 pt)."""
    lines = task_log_lines()
    shown = []
    for s in lines:
        if len(s) > 70:
            s = cut(s, "<attempt>/")
        shown.append(s)
    p = code_panel("\n".join(shown), "task logs · the shape", 1, "json", font_size=20)
    p.header.submobjects[1].set_opacity(0)          # no 'lines a–b': this is a shape, not a file
    for k, s in enumerate(shown):
        if s.endswith("…"):
            code_span(p.code, k, "…").set_color(S.GREY)
    return p


class ExecuteAndCollect(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S14"] == 11, len(SAY)
        assert "**Execute**" in readme(828) and "More actions" in readme(829)
        assert "**View logs**" in readme(831) and readme(833).endswith("it does not provide a web URL.")
        assert all(f"`{n}`" in readme(840 + k) and TABLE[k] in readme(840 + k)
                   for k, n in enumerate(AttemptFolders.FILES))
        assert readme(850).startswith("**Checkpoint:** the task finished") and readme(851).startswith("Storage.")
        assert "`translation-audio-hq9f5`" in readme(859) and "`run-001/de2f41…/`" in readme(860)
        assert readme(893).startswith("Each upload uses a create-only") and "do not establish success" in readme(895)
        assert "duplicate" in readme(895) and "Keep retries at zero" in readme(897)
        assert readme(879).startswith("`--wait` waits for completion; it does not stream application logs")
        assert "A failing job must exit unsuccessfully" in excerpt(MAIN_PY, 59, 59)
        assert "if_generation_match=0" in excerpt(STORAGE_PY, 46, 46) and "'status': 'complete'" in excerpt(STORAGE_PY, 49, 49)
        assert "uuid.uuid4().hex" in excerpt(STORAGE_PY, 37, 37)
        c42 = capture("laptop/42")
        assert c42.k == 4 and c42.exit == 1 and "--text-file examples/passage.txt" in c42.cmd
        assert c42.line(5).startswith("Batch failed: Speech is disabled.")
        rows_g = readme_rows(872, 876)
        assert len(rows_g) == 5 and rows_g[0].startswith("gcloud run jobs execute") and rows_g[2] == "mkdir -p results"

        # ========================================================== 0. Execute; History shows success
        tr = tracker_44(1)
        ref = lref("16")
        f0 = console_form(JOB, [("button", "Execute")], form_w=6.2, path="Cloud Run → Jobs")
        f0.move_to(FORM_UL, aligned_edge=UL)
        ill0 = ill_for(f0)
        nar = grey_chip("narrow toolbar: More actions ⋮").next_to(f0.frame, RIGHT, buff=0.35)
        nar.align_to(f0.rows[0], DOWN)
        assert nar.get_right()[0] < 6.55, nar.get_right()
        rec = recorded_card("part4-job-recorded", 3, "README:859")
        ok = check_glyph(0.36, OWN, 6)
        hist = label("History", 22, S.GREY)
        hrow = VGroup(hist, ok, rec).arrange(RIGHT, buff=0.3)
        hrow.move_to([0, 0.05, 0])
        ls = LifecycleStrips(show=("job",))
        ls.remove(ls.image, ls.cmds, ls.hang)          # the job strip alone in this scene
        ls.job_strip.exit_label.next_to(ls.job_strip.edge, RIGHT, buff=0.15)
        ls.shift(np.array([-0.55, -1.15, 0]))
        js = ls.job_strip                              # (ls itself also holds its anchor dot)
        assert js.get_right()[0] < 6.55 and js.get_bottom()[1] > -3.55, js.get_corner(DR)
        assert hrow.get_bottom()[1] > js.get_top()[1] + 0.3 and hrow.get_top()[1] < f0.frame.get_bottom()[1] - 0.2
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("open the job")
            self.play(FadeIn(f0, shift=UP * 0.1), FadeIn(ill0), run_time=0.5)
            vo.wait_until("and select Execute")
            self.play(f0.press(0), FadeIn(nar, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("The recording shows it succeeding")
            self.play(FadeIn(rec, shift=UP * 0.1), FadeIn(hist), run_time=0.5)
            self.play(FadeIn(ls), run_time=0.4)
            ls.run_job(self, run_time=1.6)
            vo.wait_until("with a green check in History")
            self.play(Create(ok), run_time=0.5)
            self.play(Indicate(ok, color=OWN, scale_factor=1.4), Indicate(ls.job_strip.exit_label, color=OWN),
                      run_time=0.7)

        # ========================================================== 1. what a red mark would mean: an honest exit 1
        t1 = term(P_REPO, 8, T_LAPTOP, size=20)
        ex1 = on_bar(t1, extra_row())
        up1 = 2.15 - ls.job_strip.segs.get_center()[1]
        cp = code(MAIN_PY, 59, 61, font_size=20, dedent=True)
        cp.move_to([0, 0, 0])
        bar59 = line_bar(cp.code, 0, TURN, opacity=0.3)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(f0, ill0, nar, hrow)), track(tr, 1, True), ls.animate.shift(UP * up1),
                      run_time=0.7)
            ls.reset_job(self, run_time=0.4)
            assert js.get_top()[1] < TRACK_BOTTOM - 0.05 and js.get_bottom()[1] > 1.45, (js.get_top(), js.get_bottom())
            cp.move_to([0, (js.get_bottom()[1] + BOTTOM) / 2, 0])
            bar59.move_to([cp.code.background.get_center()[0], cp.code.code_lines[0].get_center()[1], 0])
            assert t1.box.get_top()[1] < js.get_bottom()[1] - 0.3, (t1.box.get_top(), js.get_bottom())
            vo.wait_until("Our extra laptop run")
            self.play(FadeIn(t1, shift=UP * 0.15), FadeIn(ex1), run_time=0.4)
            type_capture(self, t1, c42, type_time=0.4)
            vo.wait_until("exits with status 1")
            e1 = out(self, t1, [c42.line(5)], wrap=True, color=ERR, run_time=0.4)
            pin(self, e1[-1], beside(row_tag("exit 1", ERR), e1[-1]))
            ls.run_job(self, fail_at=2, run_time=1.0)
            vo.wait_until("an honest failure")
            self.play(FadeOut(VGroup(t1, ex1)), FadeIn(cp, shift=UP * 0.1), run_time=0.5)
            self.remove(t1)
            self.play(FadeIn(bar59), Indicate(cp.code.code_lines[0], color=TURN, scale_factor=1.02), run_time=0.6)
            vo.wait_until("so History tells the truth")
            ls.reset_job(self, run_time=0.3)
            ls.run_job(self, run_time=1.0)

        # ========================================================== 2. View logs: no URL; the JSON summary
        tasks = console_form("Tasks", [("button", "View logs")], form_w=6.2,
                             path="Jobs → translation-audio → execution")
        tasks.move_to([-6.45, js.get_bottom()[1] - 0.35, 0], aligned_edge=UL)
        ill2 = ill_for(tasks)
        rc2 = readme_card(833, "The job exits; it does not provide a web URL.", size=22)
        rc2.next_to(tasks, DOWN, buff=0.35).align_to(tasks, LEFT)
        nourl = label("no ear · no URL", 20, S.GREY).next_to(ls.job_strip.inst, LEFT, buff=0.25)
        assert rc2.get_bottom()[1] > -3.55 and nourl.get_left()[0] > -6.55, (rc2.get_bottom(), nourl.get_left())
        lp = log_panel()
        lp.move_to([0, 2.25 - lp.height / 2, 0])
        lill = illustration_tag().next_to(lp.code, UP, buff=0.1).align_to(lp.code, RIGHT)
        shape = grey_chip("the shape · keys from storage.py:48-56").next_to(lp, DOWN, buff=0.25)
        assert lill.get_top()[1] < TRACK_BOTTOM - 0.05 and lp.get_left()[0] > -6.55, (lill.get_top(), lp.get_left())
        assert shape.get_bottom()[1] > -3.55 and lill.get_right()[0] < 6.55, (shape.get_bottom(), lill.get_right())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(cp, bar59)), track(tr, 2), run_time=0.5)
            vo.wait_until("open the execution")
            self.play(FadeIn(tasks, shift=UP * 0.1), FadeIn(ill2), run_time=0.5)
            vo.wait_until("View logs")
            self.play(tasks.press(0), run_time=0.6)
            vo.wait_until("The job exits")
            self.play(FadeIn(rc2, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("it has no web URL")
            self.play(Indicate(ls.job_strip.inst, color=S.GREY, scale_factor=1.15), FadeIn(nourl, shift=UP * 0.1),
                      run_time=0.7)
            vo.wait_until("Its last output")
            self.play(FadeOut(VGroup(tasks, ill2, rc2, nourl, ls)), FadeIn(lp, shift=UP * 0.1), FadeIn(lill),
                      run_time=0.7)
            self.remove(ls)
            self.play(FadeIn(shape, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("with the output and manifest locations")
            b_uri = VGroup(line_bar(lp.code, 1, ROUTE, 0.3), line_bar(lp.code, 2, ROUTE, 0.3))
            self.play(FadeIn(b_uri), run_time=0.5)
            vo.wait_until("status complete")
            b_ok = line_bar(lp.code, 3, OWN, 0.35)
            self.play(FadeIn(b_ok), Indicate(code_span(lp.code, 3, '"complete"'), color=OWN), run_time=0.6)
            self.add(lp, b_uri, b_ok)
            vo.wait_until("and the files")
            b_f = VGroup(line_bar(lp.code, 5, TURN, 0.25), line_bar(lp.code, 6, TURN, 0.25))
            self.play(FadeIn(b_f), run_time=0.5)

        # ========================================================== 3. the bucket, run-001, a random folder; three files
        af = AttemptFolders()
        af.move_to([0, -0.4, 0])
        tab = af.tabs[0]
        yours = grey_chip("yours, from the arguments").next_to(tab, RIGHT, buff=0.3)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(lp, lill, shape, b_uri, b_ok, b_f)), track(tr, 3), run_time=0.5)
            self.play(FadeIn(af, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("then run zero zero one")
            self.play(Indicate(tab, color=ROUTE, scale_factor=1.15), run_time=0.5)
            af.show(self, yours, anims=[FadeIn(yours, shift=LEFT * 0.1)], run_time=0.4)
            vo.wait_until("Inside is a folder")
            col = af.attempt(self, ATTEMPT + "/", run_time=0.7)
            col.add(col.files)      # workaround: files() parks rows in col.files before col holds it
            rt = recorded_tag("README:860").next_to(col.name, RIGHT, buff=0.3)
            rnd = grey_chip("a random name").next_to(rt, RIGHT, buff=0.25)
            assert rnd.get_right()[0] < af.frame.get_right()[0] - 0.15, rnd.get_right()
            af.show(self, rt, rnd, run_time=0.5)
            vo.wait_until("Step 4")
            af.drop(self, yours, rnd, extra=[track(tr, 4)], run_time=0.4)
            af.files(self, 0, run_time=2.4)
            tb_head = label("README.md · lines 838–842", 20, S.GREY)
            descs = VGroup()
            for row, d in zip(col.files, TABLE):
                descs.add(label(d, 20, S.GREY).move_to([0, row.get_center()[1], 0]))
            x0 = col.files.get_right()[0] + 0.5
            for d in descs:
                d.shift(np.array([x0 - d.get_left()[0], 0, 0]))
            tb_head.next_to(descs, UP, buff=0.2).align_to(descs, LEFT)
            if tb_head.get_bottom()[1] < col.folder.get_top()[1] + 0.02 and tb_head.get_left()[0] < rt.get_right()[0]:
                tb_head.next_to(descs, DOWN, buff=0.2).align_to(descs, LEFT)
            assert descs.get_right()[0] < af.frame.get_right()[0] - 0.15, descs.get_right()
            af.show(self, tb_head, *descs, anims=[FadeIn(tb_head), LaggedStart(*[FadeIn(d, shift=LEFT * 0.1)
                                                                                for d in descs], lag_ratio=0.3)],
                    run_time=0.9)

        # ========================================================== 4. the order: create-only uploads, manifest last
        sp = code(STORAGE_PY, 45, 55, font_size=20, dedent=True,
                  cuts={46: "content,", 50: "os.environ.get(", 51: "os.environ.get(", 54: "json.dumps("})
        sp.move_to([-6.45, 2.75, 0], aligned_edge=UL)
        assert sp.get_bottom()[1] > -3.5, sp.get_corner(DR)
        f_txt, f_wav, f_man = [file_icon(n, OWN if n == "manifest.json" else INK) for n in AttemptFolders.FILES]
        order = VGroup(f_txt, f_wav, f_man).arrange(RIGHT, buff=0.9)
        order.move_to([0, (sp.get_bottom()[1] + BOTTOM) / 2 + 0.3, 0])
        stamp = ok_chip("create only").next_to(VGroup(f_txt, f_wav), DOWN, buff=0.2)
        rcpt = receipt().next_to(f_man, DOWN, buff=0.2)
        assert order.get_right()[0] < 6.55 and stamp.get_bottom()[1] > -3.55 and rcpt.get_bottom()[1] > -3.55, \
            (order.get_right(), stamp.get_bottom())
        assert order.get_top()[1] < sp.get_bottom()[1] - 0.1, (order.get_top(), sp.get_bottom())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(af), FadeIn(sp, shift=UP * 0.1), run_time=0.6)
            self.remove(af)
            vo.wait_until("Each upload is create-only")
            b46 = line_bar(sp.code, 1, OWN, 0.3)
            gm = code_span(sp.code, 10, "if_generation_match=0")
            self.play(FadeIn(b46), gm.animate.set_color(OWN), run_time=0.5)
            self.add(sp, b46)
            self.play(LaggedStart(FadeIn(f_txt, shift=DOWN * 0.3), FadeIn(f_wav, shift=DOWN * 0.3), lag_ratio=0.5),
                      run_time=0.8)
            self.play(FadeIn(stamp, scale=1.2), run_time=0.4)
            vo.wait_until("and the manifest, saying complete")
            b48 = VGroup(*[line_bar(sp.code, k, OWN, 0.22) for k in range(3, 11)])
            self.play(FadeOut(b46), FadeIn(b48), run_time=0.5)
            self.play(Indicate(code_span(sp.code, 4, "'complete'"), color=OWN), run_time=0.5)
            self.add(sp, b48)
            vo.wait_until("is written last")
            self.play(FadeIn(f_man, shift=DOWN * 0.3), run_time=0.5)
            vo.wait_until("It is the receipt")
            self.play(FadeIn(rcpt, scale=1.3), run_time=0.4)
            flash_tag(self, rcpt, OWN)

        # ========================================================== 5. the third place to look; exit 0 vs complete; partial
        wl = WhereToLook(card_w=5.4)
        w0 = label("the build and start-up logs", 20, INK).move_to(wl.slots[0]).align_to(wl.slots[0], LEFT).shift(RIGHT * 0.2)
        w1 = label("the service logs", 20, INK).move_to(wl.slots[1]).align_to(wl.slots[1], LEFT).shift(RIGHT * 0.2)
        wl.slots[0].frame.set_stroke(TURN)
        wl.slots[1].frame.set_stroke(TURN)
        wl.add(w0, w1)
        wl.move_to([af.frame.get_right()[0] - 0.25 - wl.width / 2 + 0.6, af.frame.get_center()[1] - 0.15, 0])
        assert wl.get_right()[0] < 6.55
        ex0 = VGroup(check_glyph(0.4, OWN, 6), mono("exit 0", 22, INK)).arrange(RIGHT, buff=0.2)
        ex0.move_to([2.4, af.frame.get_center()[1] + 0.6, 0])
        neq = grey_chip("exit 0 ≠ work complete").next_to(ex0, DOWN, buff=0.35)
        rc5 = readme_card((894, 895), "Partial text/audio files\nwithout a completion manifest\n"
                                      "do not establish success.", size=22)
        rc5.move_to([2.55, af.frame.get_center()[1] - 0.3, 0])
        assert rc5.get_right()[0] < 6.55 and neq.get_right()[0] < af.frame.get_right()[0] - 0.1
        with self.voiceover(SAY[5]) as vo:
            for m in (tb_head, *descs, rt):
                af._detach(m)
            self.play(FadeOut(VGroup(sp, b48, f_txt, f_wav, stamp, f_man, rcpt)), FadeIn(af), run_time=0.6)
            vo.wait_until("the third place to look")
            self.play(FadeIn(wl, shift=LEFT * 0.15), run_time=0.5)
            wl.fill(self, 2, "the job's logs and manifest", run_time=0.6)
            self.play(wl.glow(2), run_time=0.6)
            vo.wait_until("A green check says")
            self.play(FadeOut(wl), run_time=0.4)
            self.play(FadeIn(ex0, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the manifest says the work is complete")
            af.flash_receipt(self, 0, run_time=0.8)
            self.play(FadeIn(neq, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Files without a manifest")
            self.play(FadeOut(VGroup(ex0, neq)), FadeOut(ref), run_time=0.3)
            af.clear(self, 0, run_time=0.3)
            af.files(self, 0, fail_after=2, run_time=1.2)
            self.play(FadeIn(rc5, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 6. PONDER: run it again — overwritten?
        with self.voiceover(SAY[6]) as vo:
            vo.wait_until("with the same arguments")
            self.play(FadeOut(rc5), run_time=0.3)
            af.clear(self, 0, run_time=0.3)
            af.files(self, 0, run_time=1.2)
            vo.wait_until("Is the first result overwritten")
            self.play(Indicate(af.attempts[0], color=TURN, scale_factor=1.04), run_time=0.6)
        pc = ponder(self, PONDER_Q, 6, center=(2.75, af.frame.get_center()[1] - 0.2), width=7.0)
        assert pc.get_left()[0] > af.attempts[0].get_right()[0] + 0.1 and pc.get_right()[0] < 6.55, \
            (pc.get_left(), af.attempts[0].get_right())

        # ========================================================== 7. a new folder beside the first; not exactly once
        uu = grey_chip("a random UUID per attempt · storage.py · lines 37–38")
        uu.move_to([6.45 - uu.width / 2, (af.frame.get_top()[1] + TRACK_BOTTOM) / 2 - 0.05, 0])
        assert uu.get_left()[0] > tr.get_right()[0] + 0.1 and uu.get_bottom()[1] > af.frame.get_top()[1] + 0.03, \
            (uu.get_left(), tr.get_right(), uu.get_bottom())
        retry = cost_tag("a retry = paid work again · retries 0")
        retry.move_to([af.frame.get_right()[0] - retry.width / 2, (af.frame.get_bottom()[1] + BOTTOM) / 2, 0])
        shield = Polygon([0, 0.25, 0], [0.22, 0.15, 0], [0.18, -0.15, 0], [0, -0.28, 0], [-0.18, -0.15, 0],
                         [-0.22, 0.15, 0], stroke_color=OWN, stroke_width=3).set_fill(OWN, 0.25)
        sh_chip = ok_chip("create only")
        sh_row = VGroup(shield, sh_chip).arrange(RIGHT, buff=0.15)
        sh_row.move_to([0, retry.get_center()[1], 0]).align_to(af.attempts[0].folder, LEFT)
        assert sh_row.get_right()[0] < retry.get_left()[0] - 0.3 and sh_row.get_bottom()[1] > -3.55, \
            (sh_row.get_right(), retry.get_left())
        assert sh_row.get_top()[1] < af.frame.get_bottom()[1] - 0.05, (sh_row.get_top(), af.frame.get_bottom())
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            vo.wait_until("A new attempt folder lands beside the first")
            c2 = af.attempt(self, "<attempt>/", run_time=0.7)
            c2.add(c2.files)        # (same workaround as above)
            self.play(FadeIn(uu, shift=DOWN * 0.1), run_time=0.4)
            af.files(self, 1, run_time=1.6)
            vo.wait_until("and create-only uploads cannot overwrite")
            files0 = af.attempts[0].files
            lock = Line(files0.get_corner(UL) + LEFT * 0.12, files0.get_corner(DL) + LEFT * 0.12, color=OWN, stroke_width=5)
            af.show(self, lock, sh_row, anims=[Create(lock), FadeIn(sh_row, shift=UP * 0.1)], run_time=0.6)
            self.play(Indicate(files0, color=OWN, scale_factor=1.04), run_time=0.6)
            vo.wait_until("But it is not exactly once")
            self.play(Indicate(VGroup(af.attempts[0].name, c2.name), color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("a retry repeats paid work")
            self.play(FadeIn(retry, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("which is why retries are 0")
            flash_tag(self, retry, COST)

        # ========================================================== 8. step 5: download; your turn; what one execution bills
        ol = object_list(f"Buckets → {OUT_BUCKET} → run-001", ATTEMPT + "/", AttemptFolders.FILES)
        ol.move_to(FORM_UL, aligned_edge=UL)
        ill8 = ill_for(ol)
        rec10 = recorded_card("part4-job-recorded", 10, "results GIF", size=20)
        rec10.next_to(ol, DOWN, buff=0.35).align_to(ol, LEFT)
        media = grey_chip("speech.wav · media tab · ⋮ → Download")
        media.next_to(rec10, DOWN, buff=0.3).align_to(rec10, LEFT)
        yt = your_turn().next_to(rec10, RIGHT, buff=0.4)
        cost = cost_tag("one execution = its task's running time + one TTS call · check the pricing page")
        cost.move_to([0, -3.1, 0])
        assert media.get_right()[0] < 6.55 and yt.get_right()[0] < 6.55, (media.get_right(), yt.get_right())
        assert cost.get_top()[1] < media.get_bottom()[1] - 0.15, (cost.get_top(), media.get_bottom())
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(af, uu, retry)), track(tr, 5), run_time=0.5)
            self.remove(af)
            af._detach(sh_row)                         # the chip under the bucket stays behind
            self.play(FadeIn(ol, shift=UP * 0.1), FadeIn(ill8), run_time=0.5)
            vo.wait_until("download the text and the audio")
            self.play(Indicate(ol.rows[0].dl, color=TURN, scale_factor=1.4), run_time=0.5)
            self.play(FadeIn(rec10, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(ol.rows[1].dl, color=TURN, scale_factor=1.4), FadeIn(media, shift=LEFT * 0.1),
                      run_time=0.6)
            vo.wait_until("Pause and run your job")
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)
            vo.wait_until("A gold tag")
            self.play(FadeIn(cost, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("plus one speech call")
            flash_tag(self, cost, COST)

        # ========================================================== 9. the gcloud alternative (README:872-876)
        gt = term(P_REPO, 8, T_GCLOUD, size=20)
        npc = no_panel_chip()
        wchip = grey_chip("waits · does not stream app logs")
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(ol, ill8, rec10, media, yt, cost)), track(tr, 1, "gcloud"), run_time=0.5)
            self.play(FadeIn(gt, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("executes with wait")
            typed = type_lines(self, gt, rows_g[:2], type_time=0.5)
            vo.wait_until("makes a results folder")
            typed += type_lines(self, gt, rows_g[2:3], type_time=0.3)
            vo.wait_until("and copies the output down")
            typed += type_lines(self, gt, rows_g[3:], type_time=0.5)
            under_term(gt, npc)
            self.play(FadeIn(npc, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("The wait flag")
            wrow = [r for r in rows_of(typed[1]) if "--wait" in r.text][0]
            rw = ring(substring(wrow, "--wait"), TURN, buff=0.05)
            wchip.next_to(gt.box, UP, buff=0.12).align_to(gt.box, LEFT)
            assert wchip.get_right()[0] < npc.get_left()[0] - 0.2 and wchip.get_top()[1] < TRACK_BOTTOM - 0.05
            self.play(Create(rw), FadeIn(wchip, shift=DOWN * 0.1), run_time=0.6)
            self.add(gt, rw)

        # ========================================================== 10. the README's checkpoint; files remain
        rc10 = readme_card((850, 851), "Checkpoint: the task finished, the process stopped,\n"
                                       "and its files remain in Storage.", size=22)
        rc10.move_to([6.45 - rc10.width / 2, 2.78 - rc10.height / 2, 0])
        assert rc10.get_left()[0] > tracker_44(5).get_right()[0] + 0.15, rc10.get_left()
        ls.shift(np.array([-js.get_center()[0], rc10.get_bottom()[1] - 0.5 - js.get_top()[1], 0]))
        af.move_to([0, BOTTOM + 0.05 + af.height / 2, 0])
        assert af.get_top()[1] < rc10.get_bottom()[1] - 0.1, (af.get_top(), rc10.get_bottom())
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(gt, npc, wchip, rw)), track(tr, 5), run_time=0.5)
            self.remove(gt)
            self.play(FadeIn(rc10, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("the task finished")
            self.play(FadeIn(ls), run_time=0.4)
            self.play(Indicate(ls.job_strip.edge, color=INK, scale_factor=1.3), run_time=0.5)
            vo.wait_until("the process stopped")
            ls.drop(self, ls.job_strip.inst, ls.job_strip.disk, run_time=0.5)
            vo.wait_until("and its files remain in Storage")
            self.play(FadeOut(ls), FadeIn(af, shift=UP * 0.2), run_time=0.7)
            self.remove(ls)
            self.play(Indicate(VGroup(*af.attempts), color=CLOUD, scale_factor=1.03), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
