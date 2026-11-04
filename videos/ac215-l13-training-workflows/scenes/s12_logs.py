"""S12 · What the job prints, what W&B can show — tracker F4 → F5; lecture_ref 9–10, 15–16, 25.

Beats (script.md, ## S12; one voiceover block each):
0. TRACKER F4. README card (README.md · lines 157–158, the link's markdown dropped). A console
   illustration "Vertex AI → Training → Custom jobs" with one row `cheese_training_job_<12 hex>`
   (no status, no durations); GREY chip "a custom job · not a training pipeline"; ▶ your turn. The
   row opens to a job-page wireframe with a PINK "logs" link; the line to wait for,
   `Training Job Complete`, appears beside it.
1. The log shape (illustration · built from task.py's print lines): ten rows, each with its
   task.py line in a GREY gutter; the four counts get `recorded · notebooks A/B` (their cells).
2. The Labels row splits into notebook A's and notebook B's recorded orders (NB(A: 352),
   NB(B: 409)); chip "os.listdir has no order · no label map is saved" + erratum; YELLOW chip
   "class 0: brie in A · gruyere in B"; S03's sticky "remember this order" returns. The panel comes
   back further down: Train model (:269), the summary block ending in a stray None (:308, chip
   "print(model.summary())"), the GREY-dashed gap "no recording of this part", the training time
   (:333) and Training Job Complete (:341).
3. TRACKER F5. README card (lines 161–163) + erratum + chip "not with this code · no callback".
   The repo run's row (illustration, no numbers): run name + project, the five config chips with
   their sources, "system charts · CPU · GPU · memory", ghost curve slots and CODE(task.py:
   326–331) at 20 pt with no callbacks=. ▶ your turn.
4. The row becomes slide 9's seven columns (RunRecord), all unticked. PONDER 8 s.
5. The answer ticked column by column; then the folder from notebook A with its three gaps; then
   the hook's two tables and S01's question card, whose "?" resolves to "can't tell · yet";
   exercise chips. Fade out.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F403
from explainer import style as S

SAY = NARRATION["S12"]
PONDER_SEVEN = "Of the seven things a run record\nshould hold, which does this run record?"
HOOK_LINES = ("Which recipe is better — and from these two tables,", "can you even tell what was different?")
LOG_TAG = "illustration · built from task.py's print lines"
ROW_H = 0.42
GUTTER_X = -5.3           # right edge of the gutter (:NN, under a "task.py" heading)
TEXT_X = -5.05            # left edge of the log text

# the job log's shape: (task.py line, printed text); values only where both notebooks recorded them
COUNTS_A = (353, 445, 446, 447)
COUNTS_B = (410, 502, 503, 504)


def log_row(src: str, text: str, y: float, color=INK) -> VGroup:
    """One log line: the task.py line in a GREY gutter, the printed text in mono. .src .text"""
    g = mono(src, 20, S.GREY)
    g.move_to([GUTTER_X - g.width / 2, y, 0])
    t = mono(text, 20, color)
    t.move_to([TEXT_X + t.width / 2, y, 0])
    r = VGroup(g, t)
    r.src, r.text = g, t
    return r


def hook_card(lines, size: float = 22) -> VGroup:
    """S01's YELLOW question card, back small. .frame .text"""
    t = VGroup(*[label(s, size, INK) for s in lines]).arrange(DOWN, buff=0.1)
    fr = RoundedRectangle(width=t.width + 0.7, height=t.height + 0.4, corner_radius=0.14, stroke_color=TURN,
                          stroke_width=3).set_fill(S.BG, 1)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


class WhatTheJobSays(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S12"] == 6, len(SAY)
        tr = tracker_f(4)
        ref = lref("9–10, 15–16, 25")
        assert tr.caption.get_right()[0] < ref.get_left()[0]

        # ========================================================== 0. view jobs (F4)
        rc = readme_card((157, 158), body="Go to Vertex AI Custom Jobs\n"
                                          "You will see the newly created job ready to be provisioned to run.")
        rc.move_to([0, 0, 0]).align_to([-6.3, 0, 0], LEFT).align_to([0, 2.6, 0], UP)
        assert "Custom Jobs" in readme(157) and "ready to be provisioned to run" in readme(158)
        con = console(("Vertex AI", "Training", "Custom jobs"), win_w=7.0, win_h=2.7)
        con.move_to([-2.8, -1.55, 0])
        con_ill = illustration_tag("illustration · console labels not captured")
        con_ill.next_to(con.frame, UP, buff=0.1).align_to(con.frame, RIGHT)
        jn = mono(JOB_NAME, 20, INK)
        jrow = RoundedRectangle(width=con.frame.width - 0.6, height=0.5, corner_radius=0.06, stroke_color=S.GREY,
                                stroke_width=1.5).move_to(con.content.get_top() + DOWN * 0.45)
        jn.move_to(jrow).align_to(jrow, LEFT).shift(RIGHT * 0.2)
        cj = grey_chip("a custom job · not a training pipeline").next_to(con.frame, RIGHT, buff=0.3)
        cj.align_to(con.frame, UP).shift(DOWN * 0.2)
        yt0 = your_turn().next_to(cj, DOWN, buff=0.25).align_to(cj, LEFT)
        # the job page (wireframe): same window, new breadcrumb, the job name as title, a logs link
        crumbs2 = VGroup(label("Custom jobs", 20, S.GREY), label("→", 20, S.GREY), label("your job", 20, INK))
        crumbs2.arrange(RIGHT, buff=0.12).move_to(con.crumbs, aligned_edge=LEFT)
        title_pos = con.content.get_corner(UL) + np.array([0.25, -0.35, 0])
        bars = VGroup(*[RoundedRectangle(width=w, height=0.16, corner_radius=0.05, stroke_width=0)
                        .set_fill(S.GREY_DARK, 1) for w in (4.2, 3.4, 3.8)]).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.2)
        bars.move_to(title_pos + np.array([bars.width / 2, -0.75, 0]))
        logs = label("logs", 22, ROUTE)
        logs.next_to(bars, RIGHT, buff=0.7).align_to(bars, DOWN)
        logs_u = under(logs, ROUTE, stroke=2)
        done_chip = mono("Training Job Complete", 20, INK)
        done_box = RoundedRectangle(width=done_chip.width + 0.4, height=0.5, corner_radius=0.08, stroke_color=TURN,
                                    stroke_width=2.5).set_fill(S.BG, 1)
        done_w = note("wait for this line")
        done = VGroup(done_box, done_chip.move_to(done_box))
        done_w.next_to(done, UP, buff=0.1).align_to(done, LEFT)
        done.add(done_w)
        done.next_to(cj, DOWN, buff=0.7).align_to(cj, LEFT)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(rc, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("open Vertex AI")
            self.play(FadeIn(con.frame), FadeIn(con[1]), FadeIn(con_ill), run_time=0.5)
            for i, anchor in ((0, "open Vertex AI"), (2, "then Training"), (4, "then Custom jobs")):
                if i:
                    vo.wait_until(anchor)
                    self.play(FadeIn(con.crumbs[i - 1]), run_time=0.2)
                self.play(FadeIn(con.crumbs[i], shift=RIGHT * 0.15), run_time=0.35)
            self.play(FadeIn(jrow), FadeIn(jn, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("pause and look for yours")
            self.play(Indicate(jn, color=TURN, scale_factor=1.04), FadeIn(yt0, shift=LEFT * 0.2), run_time=0.7)
            flash_tag(self, yt0, TURN)
            vo.wait_until("It is a custom job")
            self.play(FadeIn(cj, shift=LEFT * 0.2), run_time=0.5)
            self.play(Indicate(con.crumbs[4], color=TURN), run_time=0.7)
            vo.wait_until("Open your job")
            self.play(FadeOut(VGroup(rc, yt0), shift=UP * 0.15), FadeOut(jrow), FadeOut(con.crumbs),
                      FadeIn(crumbs2), jn.animate.move_to(title_pos + RIGHT * jn.width / 2), run_time=0.8)
            self.remove(rc, yt0, jrow, con.crumbs)
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.2), run_time=0.7)
            vo.wait_until("follow its logs link")
            self.play(FadeIn(logs, shift=UP * 0.1), Create(logs_u), run_time=0.6)
            self.play(Indicate(logs, color=ROUTE, scale_factor=1.15), run_time=0.6)
            vo.wait_until("wait for the line training job complete")
            lk = route(logs.get_right() + RIGHT * 0.08, done[0].get_left() + LEFT * 0.08)
            self.play(Create(lk), FadeIn(done, shift=UP * 0.15), run_time=0.8)

        # ========================================================== 1. the log's shape
        page1 = ((":57", "tensorflow version …"), (":61", "Number of replicas: …"),
                 (":67", "GPU Available:  …"), (":94", "Downloading data..."),
                 (":102", "Download execution time (mins) …"), (":107", "Labels: […]"),
                 (":122", nb_line("A", 353)), (":148", nb_line("A", 445)),
                 (":149", nb_line("A", 446)), (":150", nb_line("A", 447)))
        for a, b in zip(COUNTS_A, COUNTS_B):
            assert nb_line("A", a) == nb_line("B", b), (a, b)
        y0 = 1.85
        rows1 = [log_row(s, t, y0 - i * ROW_H) for i, (s, t) in enumerate(page1)]
        pan = RoundedRectangle(width=12.7, height=6.0, corner_radius=0.16, stroke_color=CLOUD,
                               stroke_width=2.5).set_fill(S.GREY_DARKER, 1).move_to([0, -0.55, 0])
        pan.set_z_index(-1)          # the Labels row slides back over it
        gut_h = mono("task.py", 20, S.GREY)
        gut_h.move_to([0, y0 + 0.36, 0]).align_to(pan, LEFT).shift(RIGHT * 0.25)
        pan_t = label("job log · its shape", CAPTION, S.GREY).next_to(gut_h, RIGHT, buff=0.6)
        pan_h = VGroup(gut_h, pan_t)
        log_ill = illustration_tag(LOG_TAG).next_to(pan, UP, buff=0.1).align_to(pan, RIGHT)
        vals = VGroup(*rows1[6:])
        brk = Line(vals.get_corner(UR) + np.array([0.45, 0.05, 0]), vals.get_corner(DR) + np.array([0.45, -0.05, 0]),
                   color=S.GREY, stroke_width=3)
        rec = recorded_tag("recorded · notebooks A/B").next_to(brk, RIGHT, buff=0.25)
        rec.align_to(brk, UP)
        cells = VGroup(note(f"notebook A · cells {nb_cell('A', 353)}, {nb_cell('A', 445)}"),
                       note(f"notebook B · cells {nb_cell('B', 410)}, {nb_cell('B', 502)}")).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(rec, DOWN, buff=0.15).align_to(rec, LEFT)
        gutters = [r.src for r in rows1]

        with self.voiceover(SAY[1]) as vo:
            old = VGroup(con.frame, con[1], crumbs2, con_ill, jn, bars, logs, logs_u, cj, lk)
            self.play(FadeOut(old, shift=DOWN * 0.15), done.animate.move_to([0, 0.4, 0]), run_time=0.8)
            self.remove(*old)
            self.play(FadeOut(done, scale=0.9), FadeIn(pan), FadeIn(pan_h), run_time=0.6)
            self.remove(done)
            vo.wait_until("No job log exists for this video")
            self.play(FadeIn(log_ill, shift=LEFT * 0.15), run_time=0.5)
            flash_tag(self, log_ill, INK)
            vo.wait_until("so here is its shape")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows1[:6]], lag_ratio=0.25), run_time=1.6)
            vo.wait_until("built from the code's own print lines")
            self.play(each(gutters[:6], INK, scale=1.08, lag=0.1), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows1[6:]], lag_ratio=0.25), run_time=1.0)
            vo.wait_until("The counts are the ones")
            self.play(Create(brk), FadeIn(rec, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("both notebooks printed")
            self.play(FadeIn(cells, shift=UP * 0.1), run_time=0.5)
            self.play(each([r.text for r in rows1[6:]], TURN, scale=1.05, lag=0.12), run_time=1.0)

        # ========================================================== 2. labels, summary, the gap, the end
        lab_row = rows1[5]
        lab_home = lab_row.get_center().copy()
        lab_top = [0, 2.55, 0]
        c_a = notebook_cell("A", 352, size=20)
        c_b = notebook_cell("B", 409, size=20)
        c_a.move_to([0, 0, 0]).align_to([-6.3, 0, 0], LEFT).align_to([0, 2.2, 0], UP)
        c_b.next_to(c_a, DOWN, buff=0.15).align_to(c_a, LEFT)
        pin_ = sticky("remember this order", mono_font=False).next_to(c_a.frame, RIGHT, buff=0.3)
        pin_.set_y(c_a.line(352).get_center()[1])
        r_a = ring(c_a.sub(352, "'brie'"), TURN, buff=0.05)
        r_b = ring(c_b.sub(409, "'gruyere'"), TURN, buff=0.05)
        c0 = card(["class 0:", "brie in A · gruyere in B"], color=TURN, size=20).next_to(c_b.frame, RIGHT, buff=0.15)
        c0.set_y(c_b.frame.get_center()[1])
        osl = grey_chip("os.listdir has no order · no label map is saved")
        err1 = erratum_tag()
        osl_g = VGroup(osl, err1).arrange(RIGHT, buff=0.25).next_to(c_b, DOWN, buff=0.2).align_to(c_b, LEFT)
        # page 2 of the panel
        y1 = 1.85
        keep = [rows1[i] for i in (5, 6, 7, 8, 9)]
        targets2 = [y1 - i * ROW_H for i in range(5)]
        r269 = log_row(":269", "Train model", y1 - 5 * ROW_H)
        yb = y1 - 6 * ROW_H
        blk = RoundedRectangle(width=6.2, height=0.62, corner_radius=0.06, stroke_width=0).set_fill(S.GREY_DARK, 1)
        blk.move_to([TEXT_X + 3.1, yb - 0.1, 0])
        blk_t = label("the model summary table", 20, S.GREY).move_to(blk)
        blk_src = mono(":308", 20, S.GREY)
        blk_src.move_to([GUTTER_X - blk_src.width / 2, blk.get_center()[1], 0])
        block = VGroup(blk, blk_t, blk_src)
        r308 = log_row("", "None", blk.get_bottom()[1] - 0.3)
        none_c = grey_chip("print(model.summary())", mono_font=True).next_to(r308.text, RIGHT, buff=0.4)
        none_r = ring(r308.text, TURN, buff=0.06)
        yg = r308.text.get_center()[1] - 0.72
        gap = outline_box(8.4, 0.75, FUTURE, solid=False, radius=0.08).move_to([TEXT_X + 4.2, yg, 0])
        gap_t = label("no recording of this part", 20, S.GREY).move_to(gap)
        gap_src = mono("model.fit", 20, S.GREY)
        gap_t.move_to(gap).shift(RIGHT * 0.9)
        gap_src.move_to(gap).align_to(gap, LEFT).shift(RIGHT * 0.3)
        r333 = log_row(":333", "Training execution time (mins) …", yg - 0.72)
        r341 = log_row(":341", "Training Job Complete", yg - 0.72 - ROW_H)
        end_r = ring(r341.text, TURN, buff=0.07)

        with self.voiceover(SAY[2]) as vo:
            others = VGroup(*rows1[:5], *rows1[6:], brk, rec, cells, pan, pan_h, log_ill)
            self.play(FadeOut(others), lab_row.animate.move_to(lab_top).align_to([-6.3, 0, 0], LEFT), run_time=0.8)
            self.remove(*others)
            self.play(FadeIn(c_a, shift=DOWN * 0.3), FadeIn(c_b, shift=DOWN * 0.3), run_time=0.8)
            vo.wait_until("as the two notebooks show")
            self.play(Create(r_a), Create(r_b), run_time=0.6)
            self.play(FadeIn(c0, shift=LEFT * 0.2), FadeIn(pin_, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("and no label map is saved")
            self.play(FadeIn(osl_g, shift=UP * 0.15), run_time=0.6)
            flash_tag(self, err1, INK)
            vo.wait_until("The summary ends with a stray None")
            gone = VGroup(c_a, c_b, r_a, r_b, c0, pin_, osl_g)
            self.play(FadeOut(gone, shift=DOWN * 0.2), run_time=0.6)
            self.remove(*gone)
            self.play(FadeIn(pan), FadeIn(pan_h), FadeIn(log_ill), lab_row.animate.move_to([lab_home[0], y1, 0]),
                      run_time=0.7)
            for r, y in zip(keep[1:], targets2[1:]):
                r.shift([0, y - r.get_center()[1], 0])
            self.play(LaggedStart(*[FadeIn(r) for r in keep[1:]], FadeIn(r269, shift=RIGHT * 0.15),
                                  lag_ratio=0.15), run_time=1.0)
            self.play(FadeIn(block, shift=RIGHT * 0.15), FadeIn(r308, shift=RIGHT * 0.15), run_time=0.6)
            self.play(Create(none_r), run_time=0.4)
            vo.wait_until("because the code prints what summary returns")
            self.play(FadeIn(none_c, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("Training itself is a gap here")
            self.play(Create(gap), FadeIn(gap_src), run_time=0.8)
            self.play(FadeIn(gap_t), run_time=0.5)
            vo.wait_until("then the line training job complete")
            self.play(FadeIn(r333, shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(r341, shift=RIGHT * 0.15), run_time=0.5)
            self.play(Create(end_r), run_time=0.5)

        # ========================================================== 3. view training metrics (F5): the repo run
        rc2 = readme_card((161, 163), body="Go to WandB\nSelect the project cheese-training-vertex-ai\n"
                                           "You will view the training metrics tracked and automatically updated")
        assert "cheese-training-vertex-ai" in readme(162) and \
            "You will view the training metrics tracked and automatically updated" in readme(163)
        rc2.move_to([0, 1.2, 0])
        prj = rc2.body[1]
        promise = rc2.body[2]
        err2 = erratum_tag().next_to(rc2.frame, DOWN, buff=0.3).align_to(rc2.frame, LEFT)
        nwc = grey_chip("not with this code · no callback").next_to(err2, RIGHT, buff=0.25)
        # the repo run's row
        rname = mono("mobilenetv2_train_base_True", 22, RUN)
        rproj = label(f"· W&B project {WB_PROJECT_REPO}", 20, S.GREY)
        rl = VGroup(rname, rproj).arrange(RIGHT, buff=0.18)
        rrow = RoundedRectangle(width=12.4, height=0.6, corner_radius=0.08, stroke_color=RUN, stroke_width=2.5)
        rrow.move_to([0, 2.3, 0])
        rl.move_to(rrow).align_to(rrow, LEFT).shift(RIGHT * 0.25)
        row_ill = illustration_tag().next_to(rrow, DOWN, buff=0.12).align_to(rrow, RIGHT)
        src_n = VGroup(note("run name ← task.py:263, :321"), note("project ← task.py:314"))
        src_n.arrange(RIGHT, buff=0.5).next_to(rrow, DOWN, buff=0.15).align_to(rrow, LEFT).shift(RIGHT * 0.2)
        cfg_h = label("config", 20, OWNED)
        chips_ = config_chips()
        cfg = VGroup(cfg_h, chips_).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        cfg.move_to([0, 0, 0]).align_to([-6.2, 0, 0], LEFT).align_to([0, 1.25, 0], UP)
        exe = chips_[4]
        sysc = grey_chip("system charts · CPU · GPU · memory").next_to(cfg, DOWN, buff=0.35).align_to(cfg, LEFT)
        slots_ = VGroup(*[outline_box(2.5, 0.8, FUTURE, solid=False, radius=0.06) for _ in range(2)])
        slots_.arrange(RIGHT, buff=0.3).move_to([3.4, 0.75, 0])
        slot_t = label("curve slots · empty", 20, S.GREY).next_to(slots_, UP, buff=0.12).align_to(slots_, LEFT)
        cp = code("package/trainer/task.py", 326, 331, font_size=20)
        nocb = grey_chip("no callbacks=", mono_font=True).next_to(slots_, DOWN, buff=0.15).align_to(slots_, RIGHT)
        cp.next_to(nocb, DOWN, buff=0.15).align_to(slots_, RIGHT)
        yt3 = your_turn().next_to(nocb, LEFT, buff=0.3)
        prj_r = ring(prj, TURN, buff=0.06)
        promise_u = under(promise, INK, stroke=2)

        with self.voiceover(SAY[3]) as vo:
            old = VGroup(pan, pan_h, log_ill, *keep, r269, block, r308, none_c, none_r, gap, gap_t, gap_src, r333, r341,
                         end_r)
            self.play(FadeOut(old, shift=UP * 0.2), track(tr, 5), run_time=0.8)
            self.remove(*old)
            self.play(FadeIn(rc2, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the W and B project")
            self.play(Create(prj_r), run_time=0.6)
            vo.wait_until("It promises training metrics")
            self.play(Create(promise_u), run_time=0.8)
            vo.wait_until("To put it kindly")
            self.play(FadeIn(err2, shift=UP * 0.15), FadeIn(nwc, shift=UP * 0.15), run_time=0.6)
            flash_tag(self, err2, INK)
            vo.wait_until("From task.py")
            self.play(FadeOut(VGroup(rc2, err2, nwc, prj_r, promise_u), shift=UP * 0.2), Create(rrow),
                      FadeIn(rl, shift=RIGHT * 0.15), FadeIn(row_ill), run_time=0.8)
            self.remove(rc2, err2, nwc, prj_r, promise_u)
            vo.wait_until("the run named after the model")
            self.play(Indicate(rname, color=TURN, scale_factor=1.04), run_time=0.6)
            self.play(FadeIn(src_n, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("gets its config")
            self.play(FadeIn(cfg_h), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in chips_], lag_ratio=0.2),
                      run_time=1.2)
            vo.wait_until("including the execution time")
            self.play(Indicate(exe, color=OWNED, scale_factor=1.06), run_time=0.7)
            vo.wait_until("and system charts")
            self.play(FadeIn(sysc, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("its curve slots stay empty")
            self.play(Create(slots_), FadeIn(slot_t), run_time=0.8)
            self.play(FadeIn(cp, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(nocb, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("Pause and open your project")
            self.play(FadeIn(yt3, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt3, TURN)

        # ========================================================== 4. slide 9's seven items (PONDER 9)
        rr = RunRecord(cell_w=1.8)
        rr.move_to([0, 0, 0])
        rr.shift(UP * (2.7 - rr.get_top()[1]))
        heads = list(rr.heads)
        boxes = list(rr.boxes)

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(cfg, sysc, slots_, slot_t, cp, nocb, yt3, src_n, row_ill)
            self.play(FadeOut(gone, shift=DOWN * 0.2), run_time=0.6)
            self.remove(*gone)
            self.play(ReplacementTransform(rname, rr.run_label[0]), ReplacementTransform(rproj, rr.run_label[1]),
                      FadeOut(rrow), FadeIn(rr.tag), run_time=0.8)
            vo.wait_until("the lecture's list of seven")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(h, shift=DOWN * 0.1), Create(b))
                                    for h, b in zip(heads, boxes)], lag_ratio=0.2), run_time=1.6)
            self.remove(rr.run_label, rr.tag, *heads, *boxes)
            self.add(rr)
            vo.wait_until("Which of them")
            self.play(each(heads, INK, scale=1.08, lag=0.08), run_time=1.0)
        pc = ponder(self, PONDER_SEVEN, seconds=8, center=(0, -1.5))

        # ========================================================== 5. the answer, the folder, the verdict
        m_model = rr.mark("model", "yes", "hyper-\nparameters")
        m_env = rr.mark("environment", "partly", "system charts\nrun metadata\nnot the image tag\n(cli.sh)")
        m_met = rr.mark("metrics", "no", "execution_time\nin config ·\nno metric\nlogged")
        m_art = rr.mark("artifacts", "partly", "logs ✓ ·\nweights ✗")
        ab = rr.cells["artifacts"]
        hole = outline_box(ab.width / 2 - 0.16, ab.height - 0.16, FUTURE, solid=False, radius=0.05)
        hole.move_to(ab).align_to(ab, RIGHT).shift(LEFT * 0.08)
        m_code = rr.mark("code", "no", "no commit")
        m_data = rr.mark("data", "no", "a fixed\nrelease zip ·\nan unseeded\nsplit")
        m_notes = rr.mark("notes", "no")
        marks = VGroup(m_model, m_env, m_met, m_art, hole, m_code, m_data, m_notes)
        # the folder from notebook A
        fold = VGroup(folder_glyph(0.34, LAPTOP), mono(EXPERIMENT + "/", 22, INK)).arrange(RIGHT, buff=0.15)
        fold_h = label("the folder from notebook A", 20, S.GREY)
        fold_in = VGroup(fold_h, fold).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        fold_fr = RoundedRectangle(width=fold_in.width + 0.6, height=fold_in.height + 0.45, corner_radius=0.14,
                                   stroke_color=LAPTOP, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        fold_in.move_to(fold_fr)
        fcard = VGroup(fold_fr, fold_in).move_to([0, -2.2, 0]).align_to([-6.2, 0, 0], LEFT)
        fnotes = card(["no commit", f"no split · it keeps sizes and the label map (cell {nb_cell('A', 1412)})",
                       "no notes"], size=20)
        fnotes.next_to(fcard, RIGHT, buff=0.35)
        # the verdict: the hook's two tables, the question card
        ta = RunLedger("A", frame=False)
        tb = RunLedger("B", frame=False)
        ta.move_to([-3.35, 0, 0])
        tb.move_to([3.35, 0, 0])
        dy = 2.7 - max(ta.get_top()[1], tb.get_top()[1])
        ta.shift(UP * dy)
        tb.shift(UP * dy)
        ga = ring(ta.heads[1], S.GREY, buff=0.06)
        gb = ring(tb.heads[1], S.GREY, buff=0.06)
        qc = hook_card(HOOK_LINES)
        qmark = label("?", 40, TURN)
        verdict = label("can't tell · yet", 26, TURN)
        qrow = VGroup(qc, qmark).arrange(RIGHT, buff=0.4)
        qrow.next_to(VGroup(ta, tb), DOWN, buff=0.35)
        qrow.set_x(0)
        verdict.move_to(qmark).align_to(qmark, LEFT)
        ex = VGroup(grey_chip("exercise 1: a LambdaCallback"), grey_chip("exercise 3: seed the split"))
        ex.arrange(RIGHT, buff=0.4).next_to(qrow, DOWN, buff=0.3).set_x(0)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            self.play(FadeIn(m_model), run_time=0.6)
            vo.wait_until("The environment only partly")
            self.play(FadeIn(m_env), run_time=0.6)
            vo.wait_until("while the image tag sits in cli.sh")
            self.play(Indicate(m_env.words[2], color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Metrics, none")
            self.play(FadeIn(m_met), run_time=0.6)
            vo.wait_until("Logs yes, weights no")
            self.play(FadeIn(m_art), Create(hole), run_time=0.7)
            vo.wait_until("Code, data and notes, no")
            self.play(LaggedStart(FadeIn(m_code), FadeIn(m_data), FadeIn(m_notes), lag_ratio=0.3), run_time=1.0)
            vo.wait_until("The folder from notebook A")
            self.play(FadeIn(fcard, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(fnotes.frame), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in fnotes.body],
                                                        lag_ratio=0.3), run_time=1.0)
            self.remove(fnotes.frame, *fnotes.body)
            self.add(fnotes)
            vo.wait_until("So the verdict")
            gone = VGroup(rr, marks, fcard, fnotes)
            self.play(FadeOut(gone, shift=DOWN * 0.2), run_time=0.6)
            self.remove(*gone)
            self.play(FadeIn(ta, shift=RIGHT * 0.5), FadeIn(tb, shift=LEFT * 0.5), run_time=0.8)
            vo.wait_until("these tables cannot crown a recipe")
            self.play(FadeIn(qrow, shift=UP * 0.2), run_time=0.6)
            self.play(Wiggle(qmark, scale_value=1.2), run_time=0.6)
            self.play(FadeOut(qmark), FadeIn(verdict, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("match the epochs")
            self.play(Create(ga), Create(gb), run_time=0.6)
            vo.wait_until("keep the code version, then compare")
            self.play(Indicate(qc.text, color=TURN, scale_factor=1.03), run_time=0.7)
            vo.wait_until("Exercise 1 adds a small callback")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in ex], lag_ratio=0.3), run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
