"""S09 · What goes in the tarball — tracker E1 → E3, lecture_ref 23–24.

Beats (script.md, ## S09; one voiceover block each):
0. E1 · extra. The cockpit (same as S08, laptop/26) types five extras: ls -la /secrets (43–45), the
   echo (47, `40` YELLOW, ▶ your turn, "0? exit · …" chip), which (49–52), gcloud --version (54, …,
   61), the aiplatform version (64; soft wrap), both versions `at the time of recording`; then
   python -c "import tensorflow" (66, …, 69 RED). The terminal shrinks to a strip under V1; the
   cockpit gets its stamp "submits · never trains". A host strip: docker image ls (27:2–3, squeezed,
   2.59GB with `at the time of recording`).
1. E1. CODE(package/setup.py: 5–13): line 5 GREEN, "requests: via wandb" beside it; line 11 YELLOW →
   V4's GREEN trainer/ with __init__.py lit ("this file makes it a package") and python -m
   trainer.task. The ORANGE layer "TensorFlow · scikit-learn — assumed from Google's image", erratum,
   "expected in tf-cpu.2-17 · not verified here"; "uv.lock pins the cockpit, not the trainer".
2. E2. CODE(task.py: 45–54), line 52 YELLOW + "scene 11"; then CODE(task.py: 96–100) ("from a GitHub
   release · the job can't see your laptop") and CODE(task.py: 152–153) ("after the download").
3. E3. V4 step 2 (drop, clip, wrap, shrink) over a cockpit strip with the fresh-cockpit chip; sh
   package-trainer.sh, ▶ your turn; the terminal grows: laptop/30: 43–50, 51 cut (GREY, "new notice ·
   harmless"), 52 RED. Strip again: the parcel's gsutil cp stops at a RED 404 at the bucket. Then
   CODE(package-trainer.sh: 1–4), line 4 YELLOW + "fixed name · …", README card 128–129 and the
   "with your bucket: gsutil ls …" chip (no panel).
4. E3 · extra. ls -l (30:54, 4016 YELLOW), tar tzvf (30:56–63 as mode · owner · size · name, 10253
   YELLOW). Host terminal: laptop/31: 2–5, root and .gitignore:4 YELLOW, chip on root.
5. V1: cockpit (stamped), the /app mount pipe, the bucket holding the tarball, a job tile. PONDER 6 s.
6. Only `sh package-trainer.sh` lights; the GREEN tarball crosses to BLUE on the upload route, the
   cockpit stays, the /app pipe glows ("already sees your edit"); GOLD cost tag. Fade out.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F403
from explainer import style as S

SAY = NARRATION["S09"]
PONDER_TYPO = "You fix a typo in task.py.\nRebuild the image, re-run\npackage-trainer.sh, or both?"
MAP_S09 = MAP_AT["S09"]


def solid_map(**kw) -> TrainingMap:
    """V1 as S09 starts, with the cockpit solid (S08 ended on solid(); MAP_AT has no 'solid' flag)."""
    m = TrainingMap.at("S09", **kw)
    m.cockpit_solid = True
    m._apply("cockpit", m.state["cockpit"])
    return m


def tar_cols(lines):
    """`tar tzvf` rows as mode · owner · size · name (date and time dropped: the rows are 64–81
    characters, the frame holds 65); each kept field's text unchanged, sizes right-aligned."""
    rows = [ln.split(None, 5) for ln in lines]
    w = max(len(r[2]) for r in rows)
    return [f"{r[0]}  {r[1]}  {r[2].rjust(w)}  {r[5]}" for r in rows]


def notes2(a, b, color=S.GREY, size=20):
    """Two GREY caption lines, left-aligned."""
    return VGroup(note(a, color, size), note(b, color, size)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)


def put_top_left(m, x=-6.3, y=2.65):
    m.shift(np.array([x - m.get_left()[0], y - m.get_top()[1], 0]))
    return m


class InsideTheTarball(VoiceScene):
    def keep_only(self, *keep, run_time=0.5, shift=UP * 0.2):
        fam = {id(x) for k in keep for x in k.get_family()}
        gone = [m for m in self.mobjects if not any(id(x) in fam for x in m.get_family())]
        if gone:
            self.play(FadeOut(Group(*gone), shift=shift), run_time=run_time)
            self.remove(*gone)

    def construct(self):
        assert len(SAY) == SAY_COUNT["S09"] == 7, len(SAY)
        c26, c27, c30, c31 = capture("26"), capture("27"), capture("30"), capture("31")

        # ========================================================== 0. the cockpit's extras (E1 · extra)
        tr = tracker_e(1, extra=True)
        ref = lref("23–24")
        t = term(P_COCKPIT, rows=12)
        ex0 = on_bar(t, extra_row())
        zero = grey_chip("0? exit · export WANDB_KEY=… · sh docker-shell.sh")
        zero.next_to(t.box, UP, buff=0.12).align_to(t.box, RIGHT)
        mp = solid_map()
        assert tr.caption.get_right()[0] < ref.get_left()[0]

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(t), run_time=0.6)
            self.play(FadeIn(ex0), run_time=0.3)
            istep(self, t, c26.line(42), type_time=0.6)
            vo.wait_until("Slash secrets is empty")
            o1 = out(self, t, c26.at((43, 45)), run_time=0.4)
            self.play(Indicate(o1[1], color=INK, scale_factor=1.03), Indicate(o1[2], color=INK, scale_factor=1.03),
                      run_time=0.6)
            vo.wait_until("Project, bucket and key came through")
            istep(self, t, c26.line(46), type_time=0.8)
            o2 = out(self, t, c26.at(47), run_time=0.3)
            forty = substring(o2[0], "40")
            self.play(forty.animate.set_color(TURN), run_time=0.4)
            yt = beside(turn_row(), o2[0])
            pin(self, o2[0], yt, run_time=0.3)
            vo.wait_until("gcloud, gsutil and uv are here")
            istep(self, t, c26.line(48), type_time=0.5)
            out(self, t, c26.at((49, 52)), run_time=0.4)
            vo.wait_until("Pause and check yours")
            flash_tag(self, yt, TURN, run_time=0.5)
            vo.wait_until("the last number must be 40")
            r40 = ring(forty, TURN, buff=0.06)
            self.play(Create(r40), FadeIn(zero, shift=UP * 0.1), run_time=0.5)
            istep(self, t, c26.line(53), type_time=0.4)
            self.play(FadeOut(r40), run_time=0.2)
            self.remove(r40)
            o4 = out(self, t, [c26.line(54), "…", c26.line(61)], run_time=0.3)
            pin(self, o4[0], beside(time_row(), o4[0]), run_time=0.2)
            prompt_, typed = c26.istep(63)
            t.set_prompt(prompt_)
            type_cmd(self, t, typed, type_time=0.8, soft=True)
            o5 = out(self, t, c26.at(64), run_time=0.2)
            pin(self, o5[0], beside(time_row(), o5[0]), run_time=0.2)
            vo.wait_until("But importing TensorFlow fails")
            self.play(FadeOut(zero), run_time=0.2)
            self.remove(zero)
            istep(self, t, c26.line(65), type_time=0.5)
            o6 = out(self, t, [c26.line(66), "…", (c26.line(69), ERR)], run_time=0.4)
            self.play(Indicate(o6[-1], color=ERR, scale_factor=1.04), run_time=0.5)
            vo.wait_until("this container submits jobs")
            resize(self, t, 3, run_time=0.5, extra=[ex0.animate.shift(DOWN * 9 * t.pitch)])
            self.play(FadeIn(mp), run_time=0.5)
            self.play(mp.stamp_on(), run_time=0.6)
            self.play(Indicate(mp.stamp_.text, color=INK, scale_factor=1.08), run_time=0.6)
            h = term(P_REPO, rows=3, size=20)     # 72 characters a row: the command fits on one
            exh = on_bar(h, extra_row())
            tmh = on_bar(h, time_row()).next_to(exh, LEFT, buff=0.15)
            self.play(FadeOut(VGroup(t, ex0, *t.lines)), FadeIn(h), run_time=0.4)
            self.remove(t, ex0, *t.lines)
            type_cmd(self, h, c27.cmd, type_time=0.6)
            self.play(FadeIn(exh), run_time=0.2)
            o7 = out(self, h, squeeze(c27.at(2, 3)), run_time=0.3)
            gb = substring(o7[-1], "2.59GB")
            self.play(gb.animate.set_color(TURN), FadeIn(tmh), run_time=0.4)
        self.wait(1.3)      # the docker image ls row stays readable after the narration ends

        # ========================================================== 1. setup.py (E1)
        p1 = put_top_left(code("package/setup.py", 5, 13))
        yt1 = your_turn().next_to(p1, RIGHT, buff=0.3).align_to(p1, UP)
        req = grey_chip("requests: via wandb")
        bar5, bar11 = line_bar(p1.code, 0, OWNED), line_bar(p1.code, 6, TURN)
        req.next_to(p1, RIGHT, buff=0.3).set_y(p1.code.code_lines[0].get_center()[1])   # beside the pin
        tdr = drawer("trainer/", OWNED, 20, drawer_w=2.75)
        ini = file_chip("__init__.py", OWNED, 20)
        mk = notes2("this file makes", "it a package")
        col = VGroup(tdr, ini, mk).arrange(DOWN, buff=0.22)
        col.next_to(p1, RIGHT, buff=0.3).set_y(-0.35)
        run_ok = VGroup(check_mark(0.26, PASS), mono("python -m trainer.task", 22, INK)).arrange(RIGHT, buff=0.15)
        run_ok.next_to(p1, DOWN, buff=0.3).align_to(p1, LEFT)
        layer = band("TensorFlow · scikit-learn — assumed from Google's image", SYSTEM, 7.7, 0.42, 20)
        layer.next_to(run_ok, DOWN, buff=0.28).align_to(p1, LEFT)
        err1 = erratum_tag().next_to(layer, RIGHT, buff=0.25)
        exp_ = grey_chip("expected in tf-cpu.2-17 · not verified here")
        exp_.next_to(layer, DOWN, buff=0.22).align_to(layer, LEFT)
        uvl = grey_chip("uv.lock pins the cockpit, not the trainer").next_to(exp_, RIGHT, buff=0.3)

        with self.voiceover(SAY[1]) as vo:
            self.keep_only(tr, ref)
            self.play(track(tr, 1), FadeIn(p1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("pause and open it")
            self.play(FadeIn(yt1, shift=LEFT * 0.15), run_time=0.3)
            flash_tag(self, yt1, TURN, run_time=0.5)
            vo.wait_until("It is the label pip uses")
            self.play(Indicate(p1.code.code_lines[2], color=INK, scale_factor=1.04), run_time=0.7)
            vo.wait_until("The only declared dependency is wandb")
            self.play(FadeIn(bar5), code_span(p1.code, 0, '"wandb==0.15.11"').animate.set_color(OWNED), run_time=0.5)
            vo.wait_until("Its find packages call")
            self.play(FadeOut(yt1), FadeIn(bar11), run_time=0.4)
            self.remove(yt1)
            vo.wait_until("because the folder has its own init file")
            self.play(FadeIn(tdr, shift=LEFT * 0.2), run_time=0.4)
            self.play(FadeIn(ini, shift=DOWN * 0.15), run_time=0.4)
            self.play(Indicate(ini.text, color=OWNED, scale_factor=1.1), FadeIn(mk), run_time=0.6)
            vo.wait_until("so once installed")
            self.play(FadeIn(run_ok, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("TensorFlow and scikit-learn are not declared")
            self.play(FadeIn(layer, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("they are assumed to come")
            self.play(FadeIn(err1, shift=LEFT * 0.1), FadeIn(exp_, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and scene 11 shows")
            flash_tag(self, err1, SYSTEM, run_time=0.5)
            self.play(FadeIn(uvl, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Requests only arrives")
            self.play(FadeIn(req, shift=LEFT * 0.15), run_time=0.4)
            self.play(Indicate(req.text, color=INK, scale_factor=1.06), run_time=0.6)

        # ========================================================== 2. task.py (E2)
        p2 = put_top_left(code("package/trainer/task.py", 45, 54, font_size=20,
                               cuts={46: "default=10,", 49: "default=16,", 52: 'default="16",'}))
        yt2 = your_turn().next_to(p2, RIGHT, buff=0.3).align_to(p2, UP)
        bar52 = line_bar(p2.code, 7, TURN)
        s11 = row_tag("scene 11", S.GREY).next_to(p2, RIGHT, buff=0.3).set_y(p2.code.code_lines[7].get_center()[1])
        flags_ = [code_span(p2.code, k, s) for k, s in ((1, '"--epochs"'), (4, '"--batch_size"'), (7, '"--wandb_key"'))]
        p3 = code("package/trainer/task.py", 96, 100, font_size=20, cuts={97: ("releases/", "cheese_4")})
        p3.move_to([0, 0, 0])
        put_top_left(p3, -p3.width / 2, 2.65)
        gh = grey_chip("from a GitHub release · the job can't see your laptop")
        gh.next_to(p3, DOWN, buff=0.2).align_to(p3, RIGHT)
        p4 = code("package/trainer/task.py", 152, 153)
        p4.next_to(gh, DOWN, buff=0.35).align_to(p3, LEFT)
        aft = grey_chip("after the download").next_to(p4, RIGHT, buff=0.35)
        yt3 = your_turn().next_to(aft, DOWN, buff=0.35).align_to(aft, LEFT)

        with self.voiceover(SAY[2]) as vo:
            self.keep_only(tr, ref)
            self.play(track(tr, 2), FadeIn(p2, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("pause and open it")
            self.play(FadeIn(yt2, shift=LEFT * 0.15), run_time=0.3)
            flash_tag(self, yt2, TURN, run_time=0.5)
            vo.wait_until("The notebook choices are flags now")
            self.play(each(flags_, INK, scale=1.1, lag=0.25), run_time=1.0)
            vo.wait_until("and the key flag defaults to the text 16")
            self.play(FadeIn(bar52), code_span(p2.code, 7, '"16"').animate.set_color(TURN), run_time=0.5)
            self.play(FadeIn(s11, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("remember that")
            flash_tag(self, s11, S.GREY, run_time=0.5)
            vo.wait_until("The data comes from one GitHub release")
            self.play(FadeOut(VGroup(p2, bar52, s11, yt2), shift=UP * 0.2), run_time=0.4)
            self.remove(p2, bar52, s11, yt2)
            self.play(FadeIn(p3, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(code_span(p3.code, 1, "github.com/dlops-io/datasets/releases/"), color=INK,
                               scale_factor=1.04), run_time=0.6)
            vo.wait_until("since the job cannot see your laptop")
            self.play(FadeIn(gh, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and the W and B login runs after that download")
            self.play(FadeIn(p4, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(line_bar(p4.code, 1, TURN)), FadeIn(aft, shift=LEFT * 0.1), run_time=0.4)
            self.play(FadeIn(yt3), run_time=0.3)

        # ========================================================== 3. pack it (E3)
        pk = TarballTrip.pack()
        pk.shift(UP * 0.5)          # the setup.py label clears the fresh-cockpit chip above the strip
        s3 = term(P_COCKPIT, rows=3)
        fresh = container_note()
        fresh.move_to([6.55 - fresh.width / 2, 2.45, 0])     # clear of the setup.py label
        notice = grey_chip("new notice · harmless")
        bk_box = RoundedRectangle(width=4.4, height=1.6, corner_radius=0.14, stroke_color=CLOUD,
                                  stroke_width=3).set_fill(CLOUD, 0.08).move_to([4.0, 0.55, 0])
        bk_t = mono(BUCKET, 20, CLOUD).move_to(bk_box.get_top() + DOWN * 0.3)
        bk_k = label("bucket", 20, CLOUD).next_to(bk_box, DOWN, buff=0.1)
        bkt = VGroup(bk_box, bk_t, bk_k)
        p5 = code("package-trainer.sh", 1, 4)
        p5.move_to([0, 0, 0])
        put_top_left(p5, -p5.width / 2, 2.75)
        fixed = grey_chip("fixed name · a new upload overwrites the old one")
        fixed.next_to(p5, DOWN, buff=0.16).align_to(p5, RIGHT)
        rc = readme_card((128, 129)).next_to(fixed, DOWN, buff=0.16).align_to(p5, LEFT)
        yb = VGroup(label("with your bucket:", 20, S.GREY), mono("gsutil ls $GCS_BUCKET_URI", 20, INK),
                    label("lists", 20, S.GREY), mono(TARBALL, 20, INK)).arrange(RIGHT, buff=0.15)
        yb_box = RoundedRectangle(width=yb.width + 0.5, height=0.52, corner_radius=0.2, stroke_color=S.GREY,
                                  stroke_width=2.5).set_fill(S.GREY, 0.16)
        yb.move_to(yb_box)
        ybc = VGroup(yb_box, yb).next_to(rc, DOWN, buff=0.16).align_to(p5, LEFT)
        assert ybc.get_bottom()[1] > -3.6, ybc.get_bottom()

        with self.voiceover(SAY[3]) as vo:
            self.keep_only(tr, ref)
            self.play(track(tr, 3), FadeIn(pk), FadeIn(s3), FadeIn(fresh, shift=UP * 0.1), run_time=0.6)
            self.play(pk.drop(run_time=0.8))
            self.play(pk.clip(run_time=0.4))
            vo.wait_until("run sh package-trainer.sh")
            pl = istep(self, s3, c30.line(42), type_time=0.6)
            self.play(pk.wrap(run_time=0.6))
            self.play(pk.shrink(run_time=0.8))
            vo.wait_until("pause and run it")
            yt4 = beside(turn_row(), pl)
            pin(self, pl, yt4, run_time=0.3)
            flash_tag(self, yt4, TURN, run_time=0.5)
            vo.wait_until("Tar lists eight entries")
            pic = VGroup(pk.parcel, pk.setup, pk.tar, pk.gzip)
            self.play(FadeOut(pic), FadeOut(fresh), run_time=0.3)
            self.remove(pic, *pic, fresh)
            resize(self, s3, 12, run_time=0.5)
            s51 = c30.line(51)
            o8 = out(self, s3, [*c30.at((43, 50)), (s51[:s3.max_chars - 1] + "…", S.GREY)], run_time=0.6, lag=0.05)
            notice.next_to(s3.box, UP, buff=0.12).align_to(s3.box, RIGHT)
            self.play(FadeIn(notice, shift=UP * 0.1), Indicate(o8[-1], color=S.GREY, scale_factor=1.02), run_time=0.5)
            vo.wait_until("and the upload fails")
            o9 = out(self, s3, [c30.line(52)], wrap=True, run_time=0.3, color=ERR)
            r404 = ring(VGroup(*o9), ERR, buff=0.06)
            self.play(Create(r404), run_time=0.4)
            vo.wait_until("our placeholder bucket does not exist")
            self.play(FadeOut(VGroup(notice, r404)), run_time=0.2)
            self.remove(notice, r404)
            resize(self, s3, 3, run_time=0.5)
            pk.parcel.move_to([-2.4, 0.55, 0])
            self.play(FadeIn(pk.parcel), FadeIn(bkt), run_time=0.4)
            up, anim = pk.upload([bk_box.get_left()[0] - 0.9, 0.55, 0])
            self.play(anim)
            vo.wait_until("Line 4 uses a fixed name")
            self.keep_only(tr, ref, run_time=0.4)
            self.play(FadeIn(p5, shift=UP * 0.15), run_time=0.4)
            self.play(FadeIn(line_bar(p5.code, 3, TURN)), code_span(p5.code, 3, TARBALL).animate.set_color(TURN),
                      run_time=0.4)
            vo.wait_until("so each upload overwrites the last")
            self.play(FadeIn(fixed, shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(rc, shift=UP * 0.15), run_time=0.4)
            self.play(FadeIn(ybc, shift=UP * 0.1), run_time=0.4)
        self.wait(0.6)

        # ========================================================== 4. extras: size, contents, owner (E3 · extra)
        t4 = term(P_COCKPIT, rows=11)
        ex4 = on_bar(t4, extra_row())
        h4 = term(P_REPO, rows=6)
        exh4 = on_bar(h4, extra_row())
        own = grey_chip("Linux engine · Docker Desktop: your user")

        with self.voiceover(SAY[4]) as vo:
            self.keep_only(tr, ref, run_time=0.4)
            self.play(track(tr, 3, extra=True), FadeIn(t4), FadeIn(ex4), run_time=0.5)
            istep(self, t4, c30.line(53), type_time=0.4)
            o10 = out(self, t4, c30.at(54), run_time=0.3)
            vo.wait_until("the tarball is 4,016 bytes")
            b4016 = substring(o10[0], TARBALL_BYTES)
            self.play(b4016.animate.set_color(TURN), run_time=0.3)
            istep(self, t4, c30.line(55), type_time=0.4)
            o11 = out(self, t4, tar_cols(c30.at((56, 63))), run_time=0.5, lag=0.05)
            self.play(substring(o11[2], "10253").animate.set_color(TURN), run_time=0.4)
            self.wait(1.0)      # the listing stays readable before the host strip replaces it
            vo.wait_until("On our Linux engine it belongs to root")
            self.play(FadeOut(VGroup(t4, ex4, *t4.lines)), FadeIn(h4), run_time=0.4)
            self.remove(t4, ex4, *t4.lines)
            type_cmd(self, h4, c31.cmd, type_time=0.9, soft=True)
            self.play(FadeIn(exh4), run_time=0.2)
            o12 = out(self, h4, [squash(s) for s in c31.at((2, 5))], run_time=0.4)
            root = substring(o12[0], "root")
            self.play(root.animate.set_color(TURN), run_time=0.3)
            own.next_to(h4.box, UP, buff=0.15).align_to(h4.box, LEFT)
            vo.wait_until("because the container wrote it")
            self.play(FadeIn(own, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("on Docker Desktop, to you")
            self.play(Indicate(own.text, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Git ignores it either way")
            self.play(substring(o12[-1], ".gitignore:4").animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(substring(o12[-1], ".gitignore:4"), color=TURN, scale_factor=1.1), run_time=0.6)

        # ========================================================== 5. V1 · the ponder
        m2 = solid_map(stamped=True, lit=MAP_S09["lit"] + ("gcp", "bucket", "vertex", "tarball", "cpu_tile"),
                       shown=("key", "tarball", "cpu_tile"))
        ck = m2.parts["cockpit"]
        px = -4.98
        code_c = chip("your code → /app", LAPTOP, size=20).move_to([-5.0, -1.9, 0])
        mount = pipe([[px, code_c.get_top()[1] + 0.02, 0], [px, m2.base.get_bottom()[1] - 0.02, 0]], IMAGE)

        with self.voiceover(SAY[5]) as vo:
            self.keep_only(tr, ref, run_time=0.4)
            self.play(track(tr, 3), FadeIn(m2), run_time=0.7)
            self.play(FadeIn(code_c, shift=UP * 0.1), Create(mount), run_time=0.6)
            vo.wait_until("You fix a typo in task.py")
            self.play(Indicate(code_c.text, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Do you rebuild the image")
            self.play(Indicate(ck, color=IMAGE, scale_factor=1.04), run_time=0.6)
        pc = ponder(self, PONDER_TYPO, seconds=6, center=(1.9, -1.72), width=8.0)

        # ========================================================== 6. the answer
        opts = VGroup(grey_chip("rebuild the image"), grey_chip("sh package-trainer.sh", mono_font=True),
                      grey_chip("both")).arrange(RIGHT, buff=0.35)
        opts.move_to([2.4, -2.55, 0])
        hit = chip("sh package-trainer.sh", TURN, size=20, font=MONO).move_to(opts[1])
        seen = note("already sees your edit", INK).next_to(code_c, RIGHT, buff=0.3)
        stays = grey_chip("your image never travels").move_to([-4.65, -2.62, 0])
        gold = cost_tag("the tarball is stored in your bucket · tiny").move_to([2.4, -3.25, 0])
        new_p = parcel(None, OWNED, 20, 0.55, 0.4).move_to(ck.body.get_center())
        tb = m2.parts["tarball"]
        words = m2.labels("upload")

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            self.play(FadeIn(opts, shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(hit), opts[0].animate.set_opacity(0.35), opts[2].animate.set_opacity(0.35),
                      run_time=0.5)
            vo.wait_until("Vertex AI runs the tarball in your bucket")
            self.play(m2.reveal("upload"), FadeIn(words), FadeIn(new_p, scale=0.8), run_time=0.6)
            self.play(new_p.animate.move_to(tb), m2.conceal("tarball", run_time=0.9), run_time=0.9)
            self.play(m2.reveal("pull"), Indicate(new_p, color=OWNED, scale_factor=1.15), run_time=0.7)
            vo.wait_until("and your image never travels")
            self.play(FadeIn(stays, shift=UP * 0.1), Indicate(ck.body, color=INK, scale_factor=1.03), run_time=0.6)
            vo.wait_until("The cockpit mounts your code folder")
            self.play(mount.core.animate.set_stroke(width=8), Indicate(code_c.text, color=INK), run_time=0.6)
            vo.wait_until("so it already sees the edit")
            self.play(FadeIn(seen, shift=LEFT * 0.1), mount.core.animate.set_stroke(width=4), run_time=0.5)
            vo.wait_until("A gold tag")
            self.play(FadeIn(gold, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and it is tiny")
            flash_tag(self, gold, COST, run_time=0.7)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
