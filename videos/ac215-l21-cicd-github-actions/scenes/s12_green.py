"""S12 · Fix, push, green: one turn of the loop (AC215 L21). TRACKER P5 8 → 8 · Part 4 · L09 → 8,
STRIP Lint and Format. Lecture: 21 · slide 21 (beat 0 only). Set pieces V2 CiLoop, V4 JobGraph.

Beats (script.md "## S12", one voiceover block each):
0. TRACKER P5 8; the Part 2 strip moves on from `Summary` back to `Lint and Format` (YELLOW).
   LECTURE 21 · 21. V2 CiLoop at full size; run 1's six marks land on the "Notifications" bar (the
   RED ✗ on lint pulses); the bar's way back to "Developers" lights PINK, the developers light up
   and a GREY "fix" chip appears beside them; the PINK Commits arrow flashes; Codebase → Build →
   Test light in turn ("goes around once more").
1. LECTURE off. The loop's words fade and its outline shrinks into a text-free copy in the top-right
   corner (no text is ever scaled). TRACKER P5 8 · Part 4 · L09 (the caption flashes on "extras").
   An 11-row `laptop` terminal: `pip install pre-commit` → TERM(laptop/30: 2, …, 39 wrap) with
   `pre-commit-4.7.0` YELLOW and "at the time of recording" on the title bar; `pre-commit install`
   → TERM(laptop/31: 2), `.git/hooks/pre-commit` ringed.
2. The terminal clears: `pre-commit run --all-files` (README.md:262) → TERM(laptop/32: …, 15–22,
   24, 26, 29, 31): the `[INFO]`/`[WARNING]` lines 2–14 as one `…` row with the GREY chip "first
   run: a few minutes (downloads the hook environments)"; the hygiene lines GREEN (19 `Skipped`
   GREY), 22 Black `Failed` RED, 24, 26 `reformatted src/api-service/api/utils.py` YELLOW, 29, 31
   Flake8 `Passed` GREEN. `▶ your turn` on the title bar (the command row has scrolled away).
3. The terminal clears and shrinks to 10 rows: `git diff` → TERM(laptop/33: 6, 10–17): 10 RED, 11
   GREEN, 16 RED. Under the strip `def power(base,exponent):` → TransformMatchingShapes → `def
   power(base, exponent):` (the new space glows GREEN), and three GREY "blank line" bars become two
   (the third fades RED).
4. The terminal clears: `pre-commit run --all-files` → TERM(laptop/34: 2–10): every row GREEN,
   `Skipped` GREY; the `Passed` words flash in turn; a GREEN outline around the block.
5. The terminal clears: `git add .` → (no output); `git commit -m "Format utils.py with Black"`
   (folds; GREY chip "our message · the README has none" above the terminal) → TERM(laptop/36:
   9–12), the hook rows GREEN, `[main 2289d89] …` with "your commit ID will differ"; `git push` →
   TERM(laptop/37: 3) GREEN; `▶ your turn` beside `git push`.
6. TRACKER P5 8. The terminal leaves. GRAPH(run2) (short labels) at its start state, all six turn
   GREEN one after another, the run badge GREEN. The lint node is ringed, the graph gives way to
   STEPS(run2/lint-and-format: 5–6) (top left; Flake8's mark starts as run 1's GREY dashed
   "skipped" and turns into a GREEN ✓) and LOG(run2/lint-and-format/04: 4–5) along the bottom
   (`All done! ✨ 🍰 ✨`, `3 files would be left unchanged.` GREEN). GREY chips "run 1: skipped"
   beside Flake8 and "on a fork: your first run" (with a GREEN ✓) on the right.
7. Steps and log go. GRAPH(run2) left, RECORDED(screenshot) slides in on the right; their nodes
   pulse GREEN pair by pair. Both go; the corner copy of the loop grows back into the full CiLoop,
   its return lines solid (no "?" any more); on its phrases: run 1's marks (a red notification),
   the "fix" chip, a GREEN commit dot goes around (Commits → Codebase → Build → Test, a ✓ back along
   the returns to the developers), six GREEN marks on the bar. Fade; empty frame.

Deviation from SHOW (beat 6): GRAPH(run2), STEPS and LOG do not fit the Part 2 frame together at
>= 20 pt (graph ~7.0 x 4.0, log 12.6 x 2.6), so the steps list and the log take the graph's place
after its reveal (the lint node is ringed first); the graph comes back for the screenshot (beat 7).
The pre-commit hook rows (73 columns) have their dot leaders shortened to fit the 65-column
terminal (the words are the capture's, as in L09's S09).
"""

import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S12"]

# ------------------------------------------------------------------ the real sources (checked)
C30 = capture("laptop/30")
C31 = capture("laptop/31")
C32 = capture("laptop/32")
C33 = capture("laptop/33")
C34 = capture("laptop/34")
C35 = capture("laptop/35")
C36 = capture("laptop/36")
C37 = capture("laptop/37")
assert C30.cmd_lines == ["pip install pre-commit"], C30.cmd_lines
assert "pre-commit-4.7.0" in C30.line(39), C30.line(39)
assert C31.cmd_lines == ["pre-commit install"] and C31.line(2) == "pre-commit installed at .git/hooks/pre-commit"
assert C32.cmd_lines == ["pre-commit run --all-files"], C32.cmd_lines
assert readme(262) == "pre-commit run --all-files", readme(262)
assert C32.line(2).startswith("[INFO]") and C32.line(14).startswith("[INFO]")
assert C32.line(19).endswith("(no files to check)Skipped"), C32.line(19)
assert C32.line(22).startswith("Format Python code with Black") and C32.line(22).endswith("Failed")
assert C32.line(24) == "- files were modified by this hook", C32.line(24)
assert C32.line(26) == "reformatted src/api-service/api/utils.py", C32.line(26)
assert C32.line(29) == "1 file reformatted, 2 files left unchanged.", C32.line(29)
assert C32.line(31).startswith("Check Python code with Flake8") and C32.line(31).endswith("Passed")
assert C33.cmd_lines == ["git diff"]
assert C33.line(10) == "-def power(base,exponent):" and C33.line(11) == "+def power(base, exponent):"
assert C33.line(16) == "-", C33.line(16)
assert C34.cmd_lines == ["pre-commit run --all-files"] and C34.exit == 0
assert C35.cmd_lines == ["git add ."]
assert C36.cmd_lines == ['git commit -m "Format utils.py with Black"'], C36.cmd_lines
assert C36.line(11) == "[main 2289d89] Format utils.py with Black", C36.line(11)
assert C37.cmd_lines == ["git push"] and C37.line(3).strip() == "b8458ff..2289d89  main -> main"
RUN1 = results("run1")
RUN2 = results("run2")
assert RUN1["lint-and-format"] == "failure" and all(RUN2[j] == "success" for j in JOB_IDS), RUN2
assert [(s.name, s.state) for s in steps("run2", "lint-and-format")][3:5] == [
    ("Run Black formatter check", "success"), ("Run Flake8 linter", "success")]
assert [s.state for s in steps("run1", "lint-and-format")][3:5] == ["failure", "skipped"]
LINT2 = capture("run2/lint-and-format/04")
assert LINT2.at((4, 5)) == ["All done! ✨ 🍰 ✨", "3 files would be left unchanged."], LINT2.at((4, 5))

# ------------------------------------------------------------------ layout
TOP = 2.05                       # Part 2 pictures stay below PIC_TOP2 (2.15)
LEFT_X, RIGHT_X = -6.45, 6.45
LOOP_C = np.array([0.0, -0.25, 0])
ICON_C = np.array([5.05, 2.86, 0])
ICON_LOW = np.array([4.65, 1.35, 0])   # the corner copy's stop under the strip (it never crosses it)
ICON_K = 0.28                    # the corner copy of the loop: outlines only, so scaling is fine
COLS = 65                        # the house terminal at 22 pt

_HOOK = re.compile(r"^(.*?[^.])(\.{3,})((?:\(no files to check\))?(?:Passed|Failed|Skipped))$")


def hook_row(s: str, n: int = COLS) -> str:
    """A pre-commit row with its dot leader shortened to fit `n` columns (words unchanged)."""
    m = _HOOK.match(s)
    if not m:
        return s
    name, _, tail = m.groups()
    dots = n - len(name) - len(tail)
    assert dots >= 3, s
    return name + "." * dots + tail


def hook_color(s: str):
    return S.GREY if s.endswith("Skipped") else ERR if s.endswith("Failed") else PASS if s.endswith("Passed") \
        else OUTPUT


def loop_texts(loop: CiLoop) -> VGroup:
    """Every word (and the marks) of the loop: they fade, never scale."""
    return VGroup(*[b.text for b in loop.boxes.values()], loop.devs[1], loop.notify.text, loop.commits[2],
                  loop.mark_row)


def loop_lines(loop: CiLoop) -> list:
    """The loop's text-free outlines, in a fixed order (pairs up with a corner copy)."""
    return [loop.row_frame, loop.row_arrows, *[b.frame for b in loop.boxes.values()], loop.devs[0],
            loop.notify.bar, loop.commits[0], loop.commits[1], loop.returns, loop.back]


def corner_copy(loop: CiLoop) -> list:
    """Copies of the loop's outlines, shrunk about the loop's centre and moved to the corner."""
    parts = [m.copy() for m in loop_lines(loop)]
    g = VGroup(*parts)
    g.scale(ICON_K, about_point=loop.get_center())
    g.shift(ICON_C - g.get_center())
    return parts


def fix_chip(loop: CiLoop) -> VGroup:
    return grey_chip("fix", size=22).next_to(loop.devs, LEFT, buff=0.3)


class RedToGreen(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S12"] == 8, len(SAY)

        # ========================================================== 0. back to slide 21's loop
        tr = tracker_p5(8)
        strip = pipeline_strip("Summary")
        ref = lref("21")
        loop = CiLoop().move_to(LOOP_C)
        fix = fix_chip(loop)
        run1_marks = [RUN1[j] for j in JOB_IDS]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(strip, shift=RIGHT * 0.3), run_time=0.6)
            self.play(strip.set_current("Lint and Format"), run_time=0.6)
            self.add(strip)
            vo.wait_until("and the lecture's loop")
            self.play(FadeIn(ref), FadeIn(loop, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("The notification came back red")
            ms = loop.marks(self, run1_marks, run_time=0.7)
            red = ms[JOB_IDS.index("lint-and-format")]
            self.play(Indicate(red, color=ERR, scale_factor=1.5), run_time=0.7)
            vo.wait_until("so now the developer fixes")
            lit = Line(loop.back.get_start(), loop.back.get_end(), color=ROUTE, stroke_width=7)
            self.play(Create(lit), run_time=0.6)
            self.play(FadeOut(lit), loop.light("devs", ROUTE), FadeIn(fix, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("and commits again")
            flash = VGroup(loop.commits[0].copy().set_stroke(ROUTE, 8))
            self.play(Create(flash), Indicate(loop.commits[2], color=ROUTE, scale_factor=1.15), run_time=0.6)
            self.play(FadeOut(flash), run_time=0.3)
            vo.wait_until("and the loop goes around")
            self.play(LaggedStart(*[loop.light(k, ROUTE) for k in ("codebase", "build", "test")], lag_ratio=0.5),
                      run_time=1.6)

        # ========================================================== 1. the fix is L09's tool (extras)
        t = laptop_term(11)
        assert t.box.get_top()[1] < PIC_TOP2, t.box.get_top()
        icon = corner_copy(loop)
        rec_tag = on_bar(t, time_row())
        with self.voiceover(SAY[1]) as vo:
            words = VGroup(loop_texts(loop), fix)
            self.play(FadeOut(ref), FadeOut(words), run_time=0.5)
            low = [m.copy().shift(ICON_LOW - ICON_C) for m in icon]      # below the strip first
            self.play(*[ReplacementTransform(a, b) for a, b in zip(loop_lines(loop), low)], run_time=0.8)
            self.play(*[ReplacementTransform(a, b) for a, b in zip(low, icon)], run_time=0.5)
            self.remove(loop, *loop.get_family(), fix, *fix.get_family(), *low)
            self.add(*icon)
            vo.wait_until("Part 4 of the same README")
            self.play(track(tr, 8, PART4), FadeIn(t, shift=UP * 0.2), run_time=0.7)
            self.add(tr)
            vo.wait_until("so these steps are extras")
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Pip install pre-commit")
            type_capture(self, t, C30, type_time=0.8)
            rows = out(self, t, [(C30.line(2), OUTPUT), ("…", S.GREY)] + [(s, OUTPUT) for s in soft([C30.line(39)], t.max_chars)])
            ver = next(r for r in rows if "pre-commit-4.7.0" in r.text)
            self.play(substring(ver, "pre-commit-4.7.0").animate.set_color(TURN), FadeIn(rec_tag), run_time=0.5)
            vo.wait_until("then pre-commit install")
            type_capture(self, t, C31, type_time=0.6)
            (hook_ln,) = out(self, t, [C31.line(2)])
            vo.wait_until("which puts the hook")
            rg = ring(substring(hook_ln, ".git/hooks/pre-commit"), TURN)
            self.play(Create(rg), run_time=0.5)
            attach(self, hook_ln, rg)

        # ========================================================== 2. pre-commit run --all-files
        info = row_tag("first run: a few minutes (downloads the hook environments)")
        turn = on_bar(t, turn_row())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(rec_tag), run_time=0.3)
            self.remove(rec_tag)
            t.clear(self)
            vo.wait_until("Then pre-commit run")
            type_capture(self, t, C32, type_time=0.8)
            (dots,) = out(self, t, [("…", S.GREY)])
            pin(self, dots, beside(info, dots))
            vo.wait_until("The hygiene checks pass")
            hyg = [(hook_row(s), hook_color(s)) for s in C32.at((15, 21))]
            out(self, t, hyg, run_time=1.0)
            vo.wait_until("Black fails")
            (blk,) = out(self, t, [(hook_row(C32.line(22)), ERR)])
            self.play(Indicate(substring(blk, "Failed"), color=ERR, scale_factor=1.25), run_time=0.6)
            vo.wait_until("because it modified a file")
            (mod,) = out(self, t, [C32.line(24)])
            self.play(Indicate(substring(mod, "files were modified"), color=INK, scale_factor=1.1), run_time=0.5)
            vo.wait_until("reformatted utils dot py")
            (ref_ln,) = out(self, t, [(C32.line(26), TURN)])
            self.play(Indicate(substring(ref_ln, "utils.py"), color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("Flake8 then passes")
            r29, r31 = out(self, t, [C32.line(29), (hook_row(C32.line(31)), PASS)])
            self.play(Indicate(substring(r31, "Passed"), color=PASS, scale_factor=1.25), run_time=0.6)
            vo.wait_until("Pause and run it")
            self.play(FadeIn(turn, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, turn)

        # ========================================================== 3. git diff: what Black changed
        before = mono("def power(base,exponent):", 22, INK)
        after = mono("def power(base, exponent):", 22, INK)
        before.move_to([-3.1, 1.78, 0])
        after.move_to(before).align_to(before, LEFT)
        bars = VGroup(*[RoundedRectangle(width=1.1, height=0.07, corner_radius=0.03, stroke_width=0)
                        .set_fill(S.GREY, 0.9) for _ in range(3)]).arrange(DOWN, buff=0.13)
        bl = label("blank lines", 20, S.GREY)
        blank = VGroup(bars, bl).arrange(RIGHT, buff=0.3).move_to([3.3, 1.78, 0])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(turn), run_time=0.3)
            self.remove(turn)
            t.clear(self)
            resize(self, t, 10)
            assert t.box.get_top()[1] < 1.45, t.box.get_top()
            vo.wait_until("Git diff")
            type_capture(self, t, C33, type_time=0.5)
            cols_ = {10: ERR, 11: PASS, 16: ERR}
            drows = out(self, t, [(s, cols_.get(n, OUTPUT)) for n, s in zip((6, *range(10, 18)), C33.at(6, (10, 17)))])
            vo.wait_until("shows exactly what Black changed")
            self.play(FadeIn(before, shift=DOWN * 0.15), FadeIn(blank, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("a space after the comma")
            self.play(TransformMatchingShapes(before, after), Indicate(drows[2], color=PASS, scale_factor=1.04),
                      run_time=0.9)
            k = len("def power(base,".replace(" ", ""))          # the comma's glyph index + 1
            gx = (after[k - 1].get_right()[0] + after[k].get_left()[0]) / 2
            glow = Rectangle(width=0.16, height=after.height + 0.12, stroke_width=0).set_fill(PASS, 0.5)
            glow.move_to([gx, after.get_center()[1], 0])
            self.add(glow)
            self.bring_to_back(glow)
            self.play(FadeIn(glow), run_time=0.3)
            self.play(glow.animate(rate_func=there_and_back).set_fill(PASS, 0.9), run_time=0.6)
            vo.wait_until("and one blank line gone")
            self.play(bars[2].animate.set_fill(ERR, 1), Indicate(drows[7], color=ERR, scale_factor=1.1), run_time=0.5)
            self.play(FadeOut(bars[2], shift=DOWN * 0.1), run_time=0.4)
            bars.remove(bars[2])
            self.play(bars.animate.move_to([bars.get_center()[0], bl.get_center()[1], 0]), run_time=0.4)

        # ========================================================== 4. run it again: all pass
        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(after, glow, blank)
            self.play(FadeOut(gone), run_time=0.4)
            self.remove(gone, *gone.get_family())
            t.clear(self)
            vo.wait_until("Run it again")
            type_capture(self, t, C34, type_time=0.8)
            hooks = out(self, t, [(hook_row(s), hook_color(s)) for s in C34.at((2, 10))], run_time=1.0)
            vo.wait_until("and every hook passes")
            passed = [substring(r, "Passed") for r in hooks if r.text.endswith("Passed")]
            self.play(LaggedStart(*[Indicate(p, color=PASS, scale_factor=1.2) for p in passed], lag_ratio=0.2),
                      run_time=1.4)
            vo.wait_until("Nothing is left to fix")
            box_ = ring(VGroup(*hooks), PASS, buff=0.05)
            self.play(Create(box_), run_time=0.6)
            attach(self, hooks[-1], box_)

        # ========================================================== 5. add, commit, push
        msg_chip = grey_chip("our message · the README has none", size=20)
        under_term(t, msg_chip)
        id_chip = row_tag("your commit ID will differ")
        turn2 = turn_row()
        with self.voiceover(SAY[5]) as vo:
            t.clear(self)
            vo.wait_until("Now git add dot")
            type_capture(self, t, C35, type_time=0.4)
            bare_prompt(self, t)
            vo.wait_until("and git commit with a message")
            (cm,) = type_capture(self, t, C36, type_time=1.0)
            vo.wait_until("Format utils dot py with Black")
            row_ = cm.rows[-1] if hasattr(cm, "rows") else cm
            self.play(Indicate(substring(row_, "Format utils.py with Black"), color=TURN, scale_factor=1.08),
                      run_time=0.6)
            vo.wait_until("The message is ours")
            self.play(FadeIn(msg_chip, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("The hooks run on the commit")
            crow = out(self, t, [(hook_row(s), hook_color(s)) for s in C36.at(9, 10)]
                       + [(C36.line(11), OUTPUT), (C36.line(12), OUTPUT)], run_time=0.8)
            self.play(LaggedStart(*[Indicate(substring(r, "Passed"), color=PASS, scale_factor=1.2) for r in crow[:2]],
                                  lag_ratio=0.3), run_time=0.8)
            pin(self, crow[2], beside(id_chip, crow[2]))
            vo.wait_until("Then git push")
            (pl,) = type_capture(self, t, C37, type_time=0.4)
            (pushed,) = out(self, t, [(C37.line(3), PASS)])
            self.play(Indicate(pushed, color=PASS, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Pause and push yours")
            pin(self, pl, beside(turn2, pl))
            flash_tag(self, turn2)

        # ========================================================== 6. run 2: all six green
        g = JobGraph(states=None, labels="short", size=20, pitch=0.62, col_gap=0.6)
        g.move_to([0, (TOP + (-3.3)) / 2, 0])
        assert g.get_top()[1] <= TOP + 1e-6, g.get_top()
        sl = steps_list("run2", "lint-and-format", [(5, 6)])
        sl.move_to([LEFT_X + sl.width / 2, TOP - sl.height / 2, 0])
        f8 = sl.row(6)
        real = f8.mark
        skipped = state_mark("skipped", real.height).move_to(real)
        f8.submobjects[f8.submobjects.index(real)] = skipped
        lg = run_log(LINT2, ((4, 5),), colors={4: PASS, 5: PASS})
        lg.move_to([0, -3.38 + lg.height / 2, 0])
        assert lg.get_top()[1] < sl.get_bottom()[1] - 0.25, (lg.get_top(), sl.get_bottom())
        was = grey_chip("run 1: skipped", size=20).next_to(sl.frame, RIGHT, buff=0.35).set_y(f8.get_center()[1])
        fork = VGroup(state_mark("success", 0.32), grey_chip("on a fork: your first run", size=22)).arrange(RIGHT, buff=0.2)
        fork.move_to([RIGHT_X - fork.width / 2, sl.head.get_center()[1], 0])
        assert fork.get_left()[0] > sl.get_right()[0] + 0.3, (fork.get_left(), sl.get_right())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(t), FadeOut(msg_chip), track(tr, 8, False), run_time=0.6)
            self.remove(t, *t.get_family(), msg_chip)
            self.add(tr)
            vo.wait_until("Run 2")
            self.play(FadeIn(g, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("all six green")
            g.reveal(self, RUN2, per=0.3)
            vo.wait_until("In the lint job")
            self.play(g.pulse("lint-and-format", PASS), run_time=0.6)
            self.play(FadeOut(g, shift=DOWN * 0.1), FadeIn(sl, shift=UP * 0.15), run_time=0.7)
            self.remove(g, *g.get_family())
            vo.wait_until("Black is happy")
            self.play(FadeIn(lg, shift=UP * 0.15), Indicate(sl.row(5).mark, color=PASS, scale_factor=1.3), run_time=0.6)
            self.play(Indicate(lg.row(5), color=PASS, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and this time Flake8 runs too")
            self.play(FadeIn(was, shift=LEFT * 0.15), run_time=0.4)
            self.play(Transform(skipped, state_mark("success", real.height).move_to(real)),
                      Indicate(f8.name, color=PASS, scale_factor=1.08), run_time=0.7)
            vo.wait_until("On a fork")
            self.play(FadeIn(fork, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and it's green")
            self.play(Indicate(fork[0], color=PASS, scale_factor=1.3), run_time=0.6)

        # ========================================================== 7. matches the screenshot; the loop closes
        g2 = JobGraph(states=RUN2, labels="short", size=20, pitch=0.62, col_gap=0.6)
        rec = recorded_graph()
        pair = VGroup(g2, rec).arrange(RIGHT, buff=0.55, aligned_edge=UP)
        pair.move_to([0, (TOP + (-3.3)) / 2, 0])
        assert pair.width <= 12.9 and pair.get_top()[1] <= TOP + 1e-6, (pair.width, pair.get_top())
        loop2 = CiLoop().move_to(LOOP_C)
        fix2 = fix_chip(loop2)
        with self.voiceover(SAY[7]) as vo:
            gone = VGroup(sl, lg, was, fork)
            self.play(FadeOut(gone), run_time=0.4)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(g2, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("matches the README's screenshot")
            self.play(FadeIn(rec, shift=LEFT * 0.6), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(g2.pulse(j, PASS), rec.graph.pulse(j, PASS)) for j in JOB_IDS],
                                  lag_ratio=0.25), run_time=1.6)
            vo.wait_until("One turn of the loop")
            low = VGroup(*icon)
            self.play(FadeOut(VGroup(g2, rec)), low.animate.shift(ICON_LOW - ICON_C), run_time=0.4)
            self.remove(g2, rec, *g2.get_family(), *rec.get_family())
            self.play(*[ReplacementTransform(a, b) for a, b in zip(icon, loop_lines(loop2))], run_time=0.6)
            words2 = VGroup(*[b.text for b in loop2.boxes.values()], loop2.devs[1], loop2.notify.text,
                            loop2.commits[2])
            self.remove(*icon)
            self.add(loop2)
            self.play(FadeIn(words2), run_time=0.3)
            loop2.close(self, run_time=0.3)
            vo.wait_until("a red notification")
            loop2.marks(self, run1_marks, run_time=0.4)
            vo.wait_until("a fix")
            self.play(FadeIn(fix2, shift=RIGHT * 0.2), run_time=0.3)
            loop2.go_around(self, PASS, run_time=1.2)        # the fix commit: Commits → … → a ✓ back
            vo.wait_until("and a green run")
            loop2.marks(self, ["success"] * len(JOB_IDS), run_time=0.4)
            self.play(loop2.light("notify", PASS), run_time=0.6)
        self.play(FadeOut(VGroup(loop2, fix2, tr, strip)), run_time=0.8)
        self.wait(0.3)

