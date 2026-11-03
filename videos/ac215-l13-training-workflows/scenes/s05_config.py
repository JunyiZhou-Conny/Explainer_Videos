"""S05 · Three lines, and an assignment that goes nowhere — tracker B4 (held), lecture_ref 14–15.

Beats (script.md, ## S05; one voiceover block each):
0. Tracker B4 + lref. Slide 14's baseline redrawn as plain code (training params, data, model,
   model.fit); three lines slide in, each with the slide's call-out (THREE_LINES): BLUE wandb.init,
   GREEN the callback inside model.fit, RED wandb.run.finish().
1. Notebook B's real cell 38 (nbB:696-705): line 698 `wandb.config = {` YELLOW, 704-705 GREY.
2. The cell grows by nbB:732 (`wandb.config.update(...)`, YELLOW). PONDER 8 s.
3. V3 ConfigBinding: bind → rebind (the name moves onto a loose dict) → write_update → finish ('{}').
4. The proof in the Colab stand-in (extra · local stand-in, 'W&B offline mode · today's wandb'):
   C38 (2-8, 9, …, 16-17; 16-17 RED), then C38b (3-4, …, 16-17; 17 GREEN). The strip shrinks to 3
   rows and V3 replays with config inside init: fill → write_update → finish ('Config · 5 keys').
5. nbB:705 `wandb.run.save("test")` + GREY chip "uploads files matching test · does not save the run".
6. The repo: task.py 312-322 and 335-338 (GREEN ticks), the 88f3374 diff (line 34 RED) + the commit
   chip, then the repo run's row (V2, illustration) with its curve slot a GREY ghost; exercise 1 chip.
   Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F403
from explainer import style as S

SAY = NARRATION["S05"]
PONDER_CONFIG = "After wandb.config = {…} and\nwandb.config.update(…), what does\nthe run's config hold?"
# slide 14's baseline (SLIDES.md, slides 14 → 15), redrawn as plain code: (text, is_comment)
BASELINE = (("# Training Params", True), ("learning_rate = 0.001", False), ("batch_size = 32", False),
            ("epochs = 10", False), ("# Data", True), ("train_data = …", False), ("# Model", True),
            ("model = …", False), ("# Train", True), ("training_results = model.fit(", False),
            ("    train_data, epochs=epochs,", False), (")", False))
# the three lines slide 15 adds: (insert at row index, text, call-out index in THREE_LINES)
INSERTS = ((8, "wandb.init(...)", 0), (12, "    callbacks=[WandbCallback()],", 1), (14, "wandb.run.finish()", 2))
COMMIT_NOTE = ("2025-10-15 · “removed ca;llback”",
               "51 min after 1c03dd5 moved the image to TF 2.17 · no reason given")


def listing_row(s: str, color=INK, size: float = 20) -> VGroup:
    """One row of the redrawn slide code (mono, fixed vertical extent)."""
    return mono_line(s, size, color)


def place_row(r: VGroup, x0: float, y: float) -> VGroup:
    r.shift(np.array([x0 - r.strut.get_left()[0], y - r.strut.get_center()[1], 0]))
    return r


def init_inside(cb, text: str) -> None:
    """Workaround (common.py's init chip overlaps the run box's top-right border): put the PURPLE
    init chip on the run box's top band, right of 'run', and re-run its dashed link to the label."""
    new = chip(text, TOOL, size=cb.size, font=MONO)
    df = cb.drawer[0]
    new.move_to([cb.run[0].get_right()[0] - 0.25 - new.width / 2, (cb.run[0].get_top()[1] + df.get_top()[1]) / 2, 0])
    cb.init = new
    cb.init_link = DashedLine(new.get_right() + RIGHT * 0.04, cb.label.get_top() + UP * 0.02, color=TOOL,
                              stroke_width=3)


class ThreeLines(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S05"] == 7, len(SAY)
        assert nb_cell("B", 696) == nb_cell("B", 732) == 38

        # ========================================================== 0. slide 14 → 15: three lines
        tr = tracker_b(4)
        ref = lref("14–15")
        pitch = line_pitch(20)
        x0, top_y = -6.15, 2.2
        rows = [place_row(listing_row(s, S.GREY if com else INK), x0, top_y - i * pitch)
                for i, (s, com) in enumerate(BASELINE)]

        def frame_for(n):
            h = n * pitch + 0.45
            fr = RoundedRectangle(width=6.3, height=h, corner_radius=0.14, stroke_color=S.GREY_DARK,
                                  stroke_width=2).set_fill(PANEL, 1)
            fr.move_to([x0 - 0.3 + 3.15, top_y + pitch / 2 + 0.22 - h / 2, 0])
            return fr

        frame = frame_for(len(rows))
        head = label("slide 14, redrawn", CAPTION, S.GREY).next_to(frame, UP, buff=0.1).align_to(frame, LEFT)
        head15 = label("slide 15, redrawn", CAPTION, S.GREY).move_to(head)
        attached = {}
        callouts = []

        def insert(at, text, k, color):
            nonlocal frame
            moving = [VGroup(r, *attached.get(id(r), [])) for r in rows[at:]]
            new_frame = frame_for(len(rows) + 1)
            self.play(*[m.animate.shift(DOWN * pitch) for m in moving], Transform(frame, new_frame), run_time=0.5)
            r = place_row(listing_row(text, INK), x0, top_y - at * pitch)
            bar = Rectangle(width=6.1, height=pitch, stroke_width=0).set_fill(color, 0.22)
            bar.move_to([frame.get_center()[0], r.strut.get_center()[1], 0])
            rows.insert(at, r)
            self.play(FadeIn(bar), FadeIn(r, shift=LEFT * 0.6), run_time=0.6)
            c = chip(THREE_LINES[k][0], color, size=22)
            c.move_to([0.6 + c.width / 2, r.strut.get_center()[1], 0])
            a = arrow(c.get_left(), np.array([r.get_right()[0] + 0.1, r.strut.get_center()[1], 0]), color, buff=0.08)
            self.play(FadeIn(c, shift=LEFT * 0.3), GrowArrow(a), run_time=0.6)
            attached[id(r)] = [bar, c, a]
            callouts.append(VGroup(bar, c, a))
            return r

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(frame), FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.08),
                      run_time=1.4)
            vo.wait_until("around unchanged training code")
            self.play(FadeOut(head), FadeIn(head15), run_time=0.5)
            vo.wait_until("Start the run")
            insert(*INSERTS[0][:2], INSERTS[0][2], THREE_LINES[0][1])
            vo.wait_until("Watch the model")
            insert(*INSERTS[1][:2], INSERTS[1][2], THREE_LINES[1][1])
            vo.wait_until("And finish the run")
            insert(*INSERTS[2][:2], INSERTS[2][2], THREE_LINES[2][1])

        # ========================================================== 1. notebook B's real cell 38
        cell = notebook_cell("B", (696, 705), "…", 732, hi={698: TURN, 704: S.GREY, 705: S.GREY, 732: TURN})
        cell.move_to([0, -0.4, 0])
        late = [cell.rows[-2], cell.rows[-1]]          # '…' and nbB:732, joining in block 2
        for m in late:
            cell.rows.remove(m)
        full_frame = cell.frame.copy()
        cell.frame.stretch_to_fit_height(full_frame.height - 2 * line_pitch(22)).align_to(full_frame, UP)
        assert cell.header.original_text.replace(" ", "") == "notebookB·cell38"

        with self.voiceover(SAY[1]) as vo:
            gone = VGroup(frame, head15, *rows, *callouts)
            self.play(FadeOut(gone, shift=UP * 0.2), run_time=0.6)
            self.remove(*gone)
            self.play(FadeIn(cell, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("It starts the run")
            self.play(Indicate(cell.line(697), color=CLOUD, scale_factor=1.06), run_time=0.8)
            vo.wait_until("then assigns a dictionary")
            hb = hl_bar(VGroup(*cell.line(698), *cell.line(703)), TURN, 0.14)
            self.play(FadeIn(hb), Indicate(cell.line(698), color=TURN, scale_factor=1.08), run_time=0.9)
            vo.wait_until("renames the run")
            self.play(Indicate(cell.line(704), color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("and calls run save")
            self.play(Indicate(cell.line(705), color=INK, scale_factor=1.06), run_time=0.7)

        # ========================================================== 2. the update joins; ponder
        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("and a later update")
            self.play(cell.frame.animate.become(full_frame), run_time=0.5)
            cell.rows.add(*late)
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in late], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("what does the run's config hold")
            self.play(Indicate(cell.line(732), color=TURN, scale_factor=1.06), run_time=0.8)
        pc = ponder(self, PONDER_CONFIG, seconds=8)

        # ========================================================== 3. V3: the name moves
        cb = ConfigBinding()
        init_inside(cb, "wandb.init(project=…)")

        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(pc, cell, hb)
            self.play(FadeOut(gone), run_time=0.6)
            self.remove(*gone)
            self.play(FadeIn(cb), run_time=0.7)
            vo.wait_until("The call wandb init points")
            self.play(cb.bind())
            vo.wait_until("The assignment does not fill")
            self.play(Indicate(cb.drawer[1], color=OWNED, scale_factor=1.15), run_time=0.7)
            vo.wait_until("it moves the name")
            self.play(cb.rebind())
            vo.wait_until("The update then writes")
            self.play(cb.write_update())
            vo.wait_until("and the run finishes")
            self.play(cb.finish())
            self.play(Indicate(cb.stamp_, color=ERR, scale_factor=1.2), run_time=0.7)

        # ========================================================== 4. the proof, then the replay
        t = colab_term(11)
        tags = VGroup(grey_chip("W&B offline mode · today's wandb"), standin_tag()).arrange(RIGHT, buff=0.2)
        on_bar(t, tags)
        c38, c38b = capture("C38"), capture("C38b")
        cb2 = ConfigBinding()
        init_inside(cb2, "wandb.init(config={…})")

        with self.voiceover(SAY[4]) as vo:
            old = Group(*[m for m in self.mobjects if m not in (tr, ref)])
            self.play(FadeOut(old), run_time=0.6)
            self.remove(*old)
            self.play(FadeIn(t), FadeIn(tags, shift=LEFT * 0.15), track(tr, 4, extra="local stand-in"),
                      run_time=0.7)
            assert tr.caption.get_right()[0] < ref.get_left()[0]
            type_cmd(self, t, c38.cmd)
            out(self, t, c38.at((2, 8), 9, "…"), wrap=True)
            vo.wait_until("The name points at a plain dict")
            o16 = out(self, t, [(c38.line(16), ERR)])
            r16 = ring(o16[-1], ERR, buff=0.05)
            self.play(Create(r16), run_time=0.5)
            vo.wait_until("and the run's config is empty")
            o17 = out(self, t, [(c38.line(17), ERR)])
            self.play(FadeOut(r16), Indicate(o17[-1], color=ERR, scale_factor=1.06), run_time=0.7)
            vo.wait_until("The fix passes the dictionary")
            type_cmd(self, t, c38b.cmd)
            out(self, t, c38b.at((3, 4), "…", 16), wrap=True)
            vo.wait_until("and the config holds all four keys")
            o17b = out(self, t, [(c38b.line(17), PASS)], wrap=True)
            self.play(each(list(o17b), PASS, scale=1.04, lag=0.15), run_time=0.8)
            dh = (11 - 3) * t.pitch
            resize(self, t, 3, keep=3, extra=[tags.animate.shift(DOWN * dh)])
            self.play(FadeIn(cb2), run_time=0.5)
            self.play(cb2.bind(run_time=1.0))
            self.play(cb2.fill())
            self.play(cb2.write_update())
            self.play(cb2.finish())

        # ========================================================== 5. run save saves files, not the run
        c705 = notebook_cell("B", 705).move_to([0, 0.9, 0])
        save_chip = grey_chip("uploads files matching test · does not save the run")
        save_chip.next_to(c705.frame, DOWN, buff=0.45)

        with self.voiceover(SAY[5]) as vo:
            old = Group(*[m for m in self.mobjects if m not in (tr, ref)])
            self.play(FadeOut(old), track(tr, 4), run_time=0.6)
            self.remove(*old)
            self.play(FadeIn(c705, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("uploads files matching test")
            rt = ring(c705.sub(705, '"test"'), TURN, buff=0.06)
            self.play(Create(rt), FadeIn(save_chip, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("it does not save the run")
            flash_tag(self, save_chip, INK)

        # ========================================================== 6. the repo: first and last right, middle gone
        pa = code("package/trainer/task.py", 312, 322).move_to([-0.6, 0.3, 0])
        ba = line_bar(pa.code, 315 - 312, PASS)
        ta = check_mark(0.5, PASS).next_to(pa, RIGHT, buff=0.35)
        pb = code("package/trainer/task.py", 335, 338).move_to([-0.4, 0.6, 0])
        bb = VGroup(line_bar(pb.code, 336 - 335, PASS), line_bar(pb.code, 338 - 335, PASS))
        tb = check_mark(0.5, PASS).next_to(pb, RIGHT, buff=0.3)
        pd = code("model-training-history/88f3374.diff", 30, 36).move_to([0, 0.9, 0])
        bd = line_bar(pd.code, 34 - 30, ERR, 0.3)
        note_c = card(list(COMMIT_NOTE), size=20).next_to(pd, DOWN, buff=0.35)

        led = RunLedger("B", columns=("run", "config", "system charts"),
                        rows=[(f"{WB_PROJECT_REPO} · repo run", "logged", "logged")], tag_=False,
                        header="W&B · the repo's runs")
        slot_w = 2.6
        span = led.width + 0.25 + slot_w
        led.move_to([-span / 2 + led.width / 2, 0.9, 0])
        sl = led.slots(slot_w)
        ghost = sl.boxes[0]
        curves_h = label("curves", 20, S.GREY).move_to([ghost.get_center()[0], led.heads[0].get_center()[1], 0])
        none_n = note("no callback · no curves", S.GREY).next_to(ghost, DOWN, buff=0.2)
        ill = illustration_tag().next_to(VGroup(led, ghost), UP, buff=0.12).align_to(ghost, RIGHT)
        ex1 = grey_chip("exercise 1 · add the callback again").next_to(VGroup(led, none_n), DOWN, buff=0.6)

        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(c705, save_chip, rt)
            self.play(FadeOut(gone, shift=UP * 0.2), run_time=0.5)
            self.remove(*gone)
            self.play(FadeIn(pa, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("config inside wandb init")
            self.play(FadeIn(ba), Create(ta), run_time=0.7)
            vo.wait_until("then update and finish")
            self.play(FadeOut(VGroup(pa, ba, ta), shift=UP * 0.3), run_time=0.5)
            self.remove(pa, ba, ta)
            self.play(FadeIn(pb, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(bb), Create(tb), run_time=0.6)
            vo.wait_until("But the middle line is gone")
            self.play(FadeOut(VGroup(pb, bb, tb), shift=UP * 0.3), run_time=0.5)
            self.remove(pb, bb, tb)
            self.play(FadeIn(pd, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(bd), Indicate(pd.code.code_lines[34 - 30], color=ERR, scale_factor=1.05), run_time=0.8)
            vo.wait_until("One commit in October 2025")
            self.play(FadeIn(note_c, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("So its runs get config")
            self.play(FadeOut(VGroup(pd, bd, note_c), shift=UP * 0.3), run_time=0.5)
            self.remove(pd, bd, note_c)
            self.play(FadeIn(led, shift=UP * 0.2), FadeIn(ill), run_time=0.7)
            self.play(each([led.cell(0, "config"), led.cell(0, "system charts")], PASS, scale=1.1), run_time=0.8)
            vo.wait_until("and no curves")
            self.play(Create(ghost), FadeIn(curves_h), run_time=0.7)
            self.play(FadeIn(none_n, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("exercise 1 adds the callback again")
            self.play(FadeIn(ex1, shift=UP * 0.15), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
