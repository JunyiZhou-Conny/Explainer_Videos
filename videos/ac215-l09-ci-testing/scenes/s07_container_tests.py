"""S07 · Tests inside the shipping image (README Part 3, tracker C1 -> C5, then C9 -> C10).

Beats (script.md, ## S07; one voiceover block each):
0. TRACKER C1 appears; `Lecture 9 · slides 87–90` (top right, until the gate table). A TEAL image
   box `cheese-app-api:local` takes "the app", then "its tests"; the three README routes as GREY chips (Option 1 · docker run per suite / Option 2 · live server for system
   tests / Option 3 · interactive shell). V7: CODE(Dockerfile: 31–41) at left; as lines light, the
   slabs stack at right, small: thin GREY `pyproject.toml`, fat ORANGE `pip install --user .`, four
   thin COPY slabs `api/`, `tests/`, `pytest.ini`, `docker-entrypoint.sh` (TEAL outlines). The
   entrypoint slab opens into CODE(docker-entrypoint.sh: 5–13): line 5 (PATH) PINK, line 12
   `exec "$@"` YELLOW; an exit-code chain pytest -> container -> docker run -> CI step (dashed).
1. Full terminal: `docker build -t cheese-app-api:local .` (README:169) -> part3-opt1-01: 2, …,
   23–24, …, 59 (CACHED ringed). TRACKER C2: `docker run --rm cheese-app-api:local pytest
   tests/unit/ -v` (README:172, folds) -> part3-opt1-02: 2–3, 11, 13, …, 23, 25 (25 GREEN).
   `▶ your turn` on both commands; the command's parts flash as the narration names them.
2. TRACKER C3: integration (README:175) -> part3-opt1-03: 13, …, 22, 24. TRACKER C4: both
   (README:178) -> part3-opt1-04: 35. Both summary lines highlight; `1 warning` gets
   `at the time of recording`. `▶ your turn`.
3. TRACKER C5: coverage (README:181) -> part3-opt1-05: 28–35; the service.py row RED with the row
   tag "never imported"; the TOTAL row tagged "Miss = lines no test ran". `▶ your turn`.
4. The terminal shrinks to a strip; the gate table slides in and its tests row fills (YELLOW, then
   final colours). TRACKER C9: `sh docker-shell.sh` (README:210) -> part3-opt3-01: 31–33; TRACKER
   C10: the four README commands (216–225) at `app@f738c22fed33:/app$`, each collapsed to its
   summary line (56, 78, 111; 137–138). The table leaves, the terminal grows: `ls htmlcov/ | head
   -4` (extra) -> 140–143 in a RED dashed box, caption "inside a --rm container · gone on exit";
   `exit` -> 145, the laptop prompt returns, the listing dims; GREY chip `--cov-report=term`.
5. Comparison card: CODE(pyproject.toml: 7–18) (black, flake8, pre-commit, pytest lines barred
   TEAL; the `>=` pins flash), dimmed behind the TEAL left column "this image: …" with `erratum`;
   right a GREEN dashed "part 2: dev tools in groups · one lockfile". Then the GREY host file
   `utils.py` glows with an edit (YELLOW "edited"); a crossed dashed arrow to the TEAL `api/`
   slab, "yesterday's copy"; a rebuild arrow and only the four COPY slabs are replaced; caption
   "packages before code". Fade out.

Deviations (reported to the coordinator): CODE(Dockerfile) is 31–41, not 27–41 (15 lines; the
panel takes at most 12; 27–30 are USER/WORKDIR, not narrated); CODE(pyproject.toml) is 7–18, not
7–19 (13 lines; 19 is the closing `]`). Code panels are 20 pt so the Dockerfile and the slab stack
share the frame and the entrypoint's 70-character comment fits. pytest's summary lines are shown
without their `=` padding (as S03 shows part3-opt1-03:24), so they fit a 65-character row and the
`at the time of recording` tag fits beside them; pytest's long PASSED rows break at the last
space that fits (soft()), so `PASSED` never splits; their text is the capture's. The image box
and the three route chips of beat 0 are added for the narration's opening sentence (no SHOW
for it; the frame would sit empty for ~10 s).
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer import style as S

from common import (CLOUD, ERR, IMAGE, INK, LAPTOP, MODIFIED, NARRATION, P_LAPTOP, PASS,
                    ROUTE, SYSTEM, TURN, VENV, GateTable, LayerStack, arrow, attach, bare_prompt,
                    beside, capture, chip, code, code_span, cross_mark, dashed_chip, erratum_tag,
                    extra_row, file_card, grey_chip, istep, label, line_bar, lref, mono, note,
                    outline_box, pin, readme, resize, ring, row_tag, substring, term, time_row,
                    tool_chip, track, tracker, turn_row, type_cmd, unpin)

SAY = NARRATION["S07"]
DOCKERFILE = "cheese-app-ci-cd/Dockerfile"
ENTRY = "cheese-app-ci-cd/docker-entrypoint.sh"
PYPROJECT = "cheese-app-ci-cd/pyproject.toml"
D0, D1 = 31, 41                    # Dockerfile window (<= 12 lines)
E0, E1 = 5, 13                     # docker-entrypoint.sh window
P0, P1 = 7, 18                     # pyproject.toml window
# the slabs of V7, with the script's names (Dockerfile:32, 35, 38–41)
SLABS = (("pyproject.toml", LAPTOP, 0.4, 32), ("pip install --user .", SYSTEM, 0.95, 35),
         ("api/", LAPTOP, 0.4, 38), ("tests/", LAPTOP, 0.4, 39), ("pytest.ini", LAPTOP, 0.4, 40),
         ("docker-entrypoint.sh", LAPTOP, 0.4, 41))


def summary(cap, n: int) -> str:
    """A pytest summary line without its '=' padding (S03 shows part3-opt1-03:24 the same way)."""
    s = cap.line(n)
    assert s.startswith("=") and s.endswith("="), s
    return s.strip("= ")


def soft(lines: list[str], n: int) -> list[str]:
    """pytest's long PASSED rows broken at their last space that fits a row (the text is the
    capture's, only the row break moves), so 'PASSED' never splits in two."""
    out = []
    for s in lines:
        while len(s) > n:
            k = s.rfind(" ", 0, n + 1)
            assert k > 0, s
            out.append(s[:k])
            s = s[k + 1:]
        out.append(s)
    return out


def rows_of(line) -> list:
    return list(line.rows) if hasattr(line, "rows") else [line]


def find_in(line, sub: str) -> VGroup:
    """The glyphs of `sub` in a typed command (a single row, or the rows of a folded one)."""
    for r in rows_of(line):
        if sub in r.text:
            return substring(r, sub)
    raise KeyError(sub)


def turn_on(scene, line):
    """Pin '▶ your turn' beside a typed command: its last row, or its first row when the last
    row of a folded command is too long to leave room. Returns (row, tag) for unpin()."""
    rs = rows_of(line)
    tag = beside(turn_row(), rs[-1])
    row = rs[-1]
    if tag.get_right()[0] > 6.55:
        row = rs[0]
        tag = beside(turn_row(), row)
    assert tag.get_right()[0] <= 6.55, line
    pin(scene, row, tag)
    return row, tag


def build_stack(x: float, floor_y: float) -> tuple[LayerStack, list]:
    st = LayerStack(stack_w=3.9)
    st.move_to([x, floor_y, 0])
    slabs = [st.make(t, fill, h) for t, fill, h, _ in SLABS]
    return st, slabs


class TestsInImage(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)
        build, unit, integ = capture("part3-opt1-01"), capture("part3-opt1-02"), capture("part3-opt1-03")
        both, cov, shell = capture("part3-opt1-04"), capture("part3-opt1-05"), capture("part3-opt3-01")
        for c, n in ((build, 169), (unit, 172), (integ, 175), (both, 178), (cov, 181), (shell, 210)):
            assert c.cmd == readme(n), (c.cmd, readme(n))
        for ln, n in ((34, 216), (57, 219), (79, 222), (112, 225)):
            assert shell.line(ln).endswith("$ " + readme(n)), (shell.line(ln), readme(n))

        # ========================================================== 0. what the image holds
        tr = tracker("C", 1)
        ref = lref("87–90")
        routes = VGroup(*[grey_chip(s, size=24) for s in (
            "Option 1 · docker run per suite", "Option 2 · a live server for the system tests",
            "Option 3 · an interactive shell")]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        routes.move_to([2.75, 0.2, 0])
        # the image the tests run in: the app and its tests, side by side inside it
        img_box = RoundedRectangle(width=4.0, height=2.5, corner_radius=0.16, stroke_color=IMAGE,
                                   stroke_width=3).set_fill(IMAGE, 0.08).move_to([-3.75, 0.2, 0])
        img_title = mono("cheese-app-api:local", 20, IMAGE).next_to(img_box.get_top(), DOWN, buff=0.25)
        app_chip = grey_chip("the app", size=22)
        tests_chip = grey_chip("its tests", size=22)
        VGroup(app_chip, tests_chip).arrange(RIGHT, buff=0.4).move_to(img_box).shift(DOWN * 0.3)
        intro = VGroup(img_box, img_title, app_chip, tests_chip)

        dock = code(DOCKERFILE, D0, D1, font_size=20)
        dock.move_to([-6.6 + dock.width / 2, 0.05, 0])
        st, slabs = build_stack(4.45, -1.75)
        img_name = mono("cheese-app-api:local", 20, IMAGE).move_to([4.45, -2.2, 0])
        bars = {n: line_bar(dock.code, n - D0, TURN, 0.2) for *_, n in SLABS}

        entry = code(ENTRY, E0, E1, font_size=20)
        entry.move_to([0, 0.5, 0])
        path_bar = line_bar(entry.code, 5 - E0, ROUTE, 0.25)
        exec_bar = line_bar(entry.code, 12 - E0, TURN, 0.25)
        args = code_span(entry.code, 12 - E0, '"$@"')
        chain = [tool_chip("pytest"), chip("container", IMAGE, size=20), tool_chip("docker run"),
                 dashed_chip("CI step", CLOUD)]
        head = label("exit code:", 22, S.GREY)
        links = [head]
        for i, c in enumerate(chain):
            links.append(c)
        row = VGroup(*links).arrange(RIGHT, buff=0.6)
        row.next_to(entry, DOWN, buff=0.5)
        arrows = VGroup(*[arrow(chain[i].get_right() + RIGHT * 0.08, chain[i + 1].get_left() + LEFT * 0.08, S.GREY)
                          for i in range(3)])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.8)
            self.play(Indicate(tr.dots[0], color=TURN, scale_factor=1.6), run_time=0.6)
            vo.wait_until("where the app lives")
            self.play(Create(img_box), FadeIn(img_title), FadeIn(app_chip, shift=DOWN * 0.2), run_time=0.9)
            vo.wait_until("inside the image")
            self.play(FadeIn(tests_chip, shift=LEFT * 0.4), Indicate(img_box, color=IMAGE, scale_factor=1.03),
                      run_time=0.8)
            vo.wait_until("by three routes")
            for chp, anchor in zip(routes, ("docker run per suite", "a live server", "or an interactive shell")):
                vo.wait_until(anchor)
                self.play(FadeIn(chp, shift=RIGHT * 0.25), run_time=0.5)
            vo.wait_until("The Dockerfile copies")
            self.play(FadeOut(routes, shift=UP * 0.2), FadeOut(intro), run_time=0.5)
            self.play(FadeIn(dock, shift=RIGHT * 0.2), FadeIn(img_name), run_time=0.8)
            self.play(FadeIn(bars[32]), run_time=0.3)
            st.drop(self, slabs[0], run_time=0.6)
            vo.wait_until("installs the dependencies")
            self.play(FadeOut(bars[32]), FadeIn(bars[35]), run_time=0.4)
            st.drop(self, slabs[1], run_time=0.7)
            vo.wait_until("one fat layer")
            self.play(Indicate(slabs[1], color=SYSTEM, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Then four thin copy lines")
            self.play(FadeOut(bars[35]), run_time=0.3)
            prev = None
            for k, anchor in zip(range(2, 6), ("the api code", "the tests", "the pytest config",
                                                "and the entrypoint")):
                vo.wait_until(anchor)
                n = SLABS[k][3]
                if prev is not None:
                    self.play(FadeOut(bars[prev]), FadeIn(bars[n]), run_time=0.25)
                else:
                    self.play(FadeIn(bars[n]), run_time=0.25)
                st.drop(self, slabs[k], run_time=0.45)
                prev = n

            # the entrypoint slab opens into the entrypoint script
            vo.wait_until("The entrypoint puts pytest")
            shell_box = slabs[5].box.copy()
            ghost = RoundedRectangle(width=entry.width, height=entry.height, corner_radius=0.15,
                                     stroke_color=IMAGE, stroke_width=2.5).move_to(entry)
            self.play(FadeOut(VGroup(dock, bars[prev], img_name)), FadeOut(st),
                      Transform(shell_box, ghost), run_time=0.9)
            self.remove(st, *slabs)
            self.play(FadeIn(entry), FadeOut(shell_box), run_time=0.6)
            vo.wait_until("on PATH")
            self.play(FadeIn(path_bar), Indicate(code_span(entry.code, 0, "/home/app/.local/bin"),
                                                 color=ROUTE, scale_factor=1.08), run_time=0.9)
            vo.wait_until("and its exec line")
            self.play(FadeIn(exec_bar), run_time=0.5)
            vo.wait_until("whatever command you pass")
            self.play(Indicate(args, color=TURN, scale_factor=1.25), run_time=0.9)
            vo.wait_until("The container's exit code")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in
                                    (head, chain[0], arrows[0], chain[1], arrows[1], chain[2])],
                                  lag_ratio=0.25), run_time=1.4)
            vo.wait_until("fail a CI step")
            self.play(GrowArrow(arrows[2]), FadeIn(chain[3], shift=RIGHT * 0.15), run_time=0.7)

        # ========================================================== 1. build, then the unit suite
        t = term(P_LAPTOP, rows=13)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(entry, path_bar, exec_bar, row, arrows)), run_time=0.5)
            self.play(FadeIn(t), run_time=0.5)
            b_ln = type_cmd(self, t, build.cmd, type_time=1.0)
            b_row, b_tag = turn_on(self, b_ln)
            out = t.print(self, build.at(2, "…", (23, 24), "…", 59), run_time=0.9, lag=0.2)
            cached = substring(out[3], "CACHED")
            vo.wait_until("all cached")
            cring = ring(cached, IMAGE, buff=0.06)
            self.play(Create(cring), run_time=0.5)
            attach(self, out[3], cring)
            vo.wait_until("then run the unit tests")
            self.play(track(tr, 2), run_time=0.5)
            u_ln = type_cmd(self, t, unit.cmd, type_time=1.3)
            u_row, u_tag = turn_on(self, u_ln)
            for anchor, sub, col in (("docker run,", "docker run", TURN), ("dash dash rm", "--rm", TURN),
                                     ("the image", "cheese-app-api:local", IMAGE),
                                     ("pytest tests slash unit", "pytest tests/unit/", TURN)):
                vo.wait_until(anchor)
                self.play(Indicate(find_in(u_ln, sub), color=col, scale_factor=1.12), run_time=0.6)
            t.print(self, unit.at(2, 3, 11), run_time=0.5)
            t.print(self, soft(unit.at(13, "…", 23), t.max_chars), run_time=0.6, lag=0.2)
            u_sum = t.print(self, [(summary(unit, 25), PASS)], run_time=0.4)[0]
            vo.wait_until("11 passed")
            self.play(Indicate(substring(u_sum, "11 passed"), color=PASS, scale_factor=1.15), run_time=0.7)
            vo.wait_until("Pause and run both")
            self.play(Indicate(u_tag, color=TURN, scale_factor=1.15), run_time=0.8)

        # ========================================================== 2. integration, then both
        with self.voiceover(SAY[2]) as vo:
            unpin(self, u_row, u_tag, track(tr, 3))
            i_ln = type_cmd(self, t, integ.cmd, type_time=1.2)
            i_row, i_tag = turn_on(self, i_ln)
            t.print(self, soft(integ.at(13, "…", 22), t.max_chars), run_time=0.6, lag=0.2)
            i_sum = t.print(self, [summary(integ, 24)], run_time=0.4)[0]
            vo.wait_until("10 passed, 1 warning")
            self.play(substring(i_sum, "10 passed").animate.set_color(PASS), run_time=0.5)
            vo.wait_until("both suites together")
            self.play(track(tr, 4), run_time=0.4)
            bo_ln = type_cmd(self, t, both.cmd, type_time=1.2)
            bo_row, bo_tag = turn_on(self, bo_ln)
            b_sum = t.print(self, [summary(both, 35)], run_time=0.4)[0]
            vo.wait_until("21 passed, 1 warning")
            self.play(substring(b_sum, "21 passed").animate.set_color(PASS), run_time=0.5)
            vo.wait_until("Pause and run them")
            self.play(Indicate(VGroup(i_tag, bo_tag), color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("The 1 warning is")
            w1, w2 = substring(i_sum, "1 warning"), substring(b_sum, "1 warning")
            self.play(Indicate(w1, color=TURN, scale_factor=1.15), Indicate(w2, color=TURN, scale_factor=1.15),
                      run_time=0.9)
            vo.wait_until("at the time of recording")
            tags = [beside(time_row(), ln) for ln in (i_sum, b_sum)]
            pin(self, i_sum, tags[0])
            pin(self, b_sum, tags[1])
            vo.wait_until("same tests, same results")
            self.play(Indicate(VGroup(substring(i_sum, "10 passed"), substring(b_sum, "21 passed")),
                               color=PASS, scale_factor=1.1), run_time=0.8)

        # ========================================================== 3. coverage
        with self.voiceover(SAY[3]) as vo:
            unpin(self, bo_row, bo_tag, track(tr, 5))
            c_ln = type_cmd(self, t, cov.cmd, type_time=1.3)
            c_row, c_tag = turn_on(self, c_ln)
            vo.wait_until("measuring the api package")
            self.play(Indicate(find_in(c_ln, "--cov=api"), color=TURN, scale_factor=1.12), run_time=0.7)
            t.print(self, cov.at((28, 34)), run_time=0.9, lag=0.1)
            t.print(self, [(summary(cov, 35), PASS)], run_time=0.3)[0]
            vo.wait_until("Pause and run it")
            self.play(Indicate(c_tag, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("Look at service.py")
            svc = t.find("api/service.py")
            assert svc.text == cov.line(31)
            self.play(svc.glyphs.animate.set_color(ERR), run_time=0.5)
            svc_ring = ring(svc.glyphs, ERR, buff=0.06)
            self.play(Create(svc_ring), run_time=0.5)
            attach(self, svc, svc_ring)
            vo.wait_until("never import it")
            pin(self, svc, beside(row_tag("never imported", ERR), svc))
            vo.wait_until("Coverage is a list")
            tot = t.find("TOTAL")
            pin(self, tot, beside(row_tag("Miss = lines no test ran", S.GREY), tot))
            vo.wait_until("not a score")
            self.play(Indicate(substring(tot, "14%"), color=S.GREY, scale_factor=1.25), run_time=0.8)
            vo.wait_until("Hold that thought")
            self.play(Indicate(substring(svc, "0%"), color=ERR, scale_factor=1.25), run_time=0.8)

        # ========================================================== 4. the gate table, Option 3
        gt = GateTable(keys=("tests",))
        gt.move_to([0, 0.75, 0])

        with self.voiceover(SAY[4]) as vo:
            unpin(self, c_row, c_tag)
            t.clear(self)
            resize(self, t, 3, keep=0, extra=[FadeOut(ref)])
            self.remove(ref)
            self.play(FadeIn(gt, shift=LEFT * 0.6), run_time=0.8)
            vo.wait_until("unit and integration tests")
            gt.fill(self, "tests")
            vo.wait_until("hermetic,")
            gt.settle(self, "tests")
            vo.wait_until("one docker command")
            self.play(Indicate(gt.rows["tests"].cells[2], color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Option 2 waits")
            self.play(Indicate(VGroup(*tr.dots[5:8]), color=S.GREY, scale_factor=1.6), run_time=0.8)
            vo.wait_until("Option 3 is the same")
            self.play(track(tr, 9), run_time=0.5)
            vo.wait_until("docker-shell again")
            type_cmd(self, t, shell.cmd, type_time=0.7)
            t.print(self, shell.at((31, 33)), run_time=0.5, lag=0.15)
            vo.wait_until("the same pytest commands")
            self.play(track(tr, 10), run_time=0.4)
            for ln, out_n in ((34, [56]), (57, [78]), (79, [111]), (112, [137, 138])):
                istep(self, t, shell.line(ln), type_time=0.6)
                outs = [shell.line(n) if n == 137 else (summary(shell, n), PASS) for n in out_n]
                t.print(self, outs, run_time=0.35)
            vo.wait_until("One trap:")
            resize(self, t, 10, keep=2, extra=[FadeOut(gt)])
            self.remove(gt)
            ls_ln = istep(self, t, shell.line(139), type_time=0.7)
            x_tag = beside(extra_row(), ls_ln)
            pin(self, ls_ln, x_tag, anim=AnimationGroup(FadeIn(x_tag, shift=LEFT * 0.1), track(tr, extra=True)))
            listing = t.print(self, shell.at((140, 143)), run_time=0.6, lag=0.12)
            vo.wait_until("lands inside a container")
            lw = max(r.glyphs.get_right()[0] for r in listing) - listing.get_left()[0]
            red = outline_box(lw + 0.4, listing.height + 0.04, ERR)
            red.move_to([listing.get_left()[0] + lw / 2, listing.get_center()[1], 0])
            cap = label("inside a --rm container · gone on exit", 22, ERR)
            cap.next_to(red, RIGHT, buff=0.4)
            self.play(Create(red.frame), FadeIn(cap, shift=LEFT * 0.15), run_time=0.8)
            attach(self, listing[0], red)
            attach(self, listing[0], cap)
            vo.wait_until("gone when you exit")
            unpin(self, ls_ln, x_tag, track(tr, extra=False))
            istep(self, t, shell.line(144), type_time=0.3)
            t.print(self, shell.at(145), run_time=0.3)
            t.set_prompt(P_LAPTOP)
            bare_prompt(self, t)
            self.play(*[r.glyphs.animate.set_opacity(0.25) for r in listing], run_time=0.7)
            vo.wait_until("Prefer the terminal report")
            pref = grey_chip("--cov-report=term", size=22, mono_font=True, color=PASS)
            pref.next_to(cap, DOWN, buff=0.35).align_to(cap, LEFT)
            self.play(FadeIn(pref, shift=UP * 0.15), run_time=0.6)
            attach(self, listing[0], pref)

        # ========================================================== 5. what the image ships, and when
        pp = code(PYPROJECT, P0, P1, font_size=20)
        pp.move_to([-3.35, -0.35, 0])
        tool_lines = (8, 10, 12, 15)                     # black, flake8, pre-commit, pytest
        tbars = VGroup(*[line_bar(pp.code, n - P0, IMAGE, 0.3) for n in tool_lines])
        pins = VGroup(*[code_span(pp.code, k, ">=") for k in range(1, 12)])

        def column(lines, color, first_color):
            body = VGroup(*[label(s, 24, first_color if i == 0 else color) for i, s in enumerate(lines)])
            return body.arrange(DOWN, aligned_edge=LEFT, buff=0.22)

        left_t = column(["this image:", "black, flake8, pytest, pre-commit", "ship as runtime deps",
                         ">= pins · no lockfile"], INK, IMAGE)
        left_f = RoundedRectangle(width=left_t.width + 0.7, height=left_t.height + 0.6, corner_radius=0.16,
                                  stroke_color=IMAGE, stroke_width=3).set_fill(S.BG, 0.82)
        left = VGroup(left_f, left_t)
        left_t.move_to(left_f)
        left.move_to(pp.code)
        err = erratum_tag().next_to(left_f, UP, buff=0.15).align_to(left_f, LEFT)
        right_t = column(["part 2:", "dev tools in groups", "one lockfile"], INK, VENV)
        right_f = outline_box(right_t.width + 0.8, left_f.height, VENV)
        right_t.move_to(right_f)
        right = VGroup(right_f, right_t).move_to([3.65, left.get_center()[1], 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(t), run_time=0.6)
            self.remove(t)
            self.play(FadeIn(pp, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("ships its dev tools")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in tbars], lag_ratio=0.25), run_time=1.0)
            vo.wait_until("open ended pins")
            self.play(Indicate(pins, color=TURN, scale_factor=1.25), run_time=0.8)
            vo.wait_until("no lockfile")
            self.play(VGroup(pp, tbars).animate.fade(0.75), FadeIn(left, scale=0.96), FadeIn(err), run_time=0.8)
            vo.wait_until("the guest lecture keeps them")
            self.play(Create(right_f.frame), FadeIn(right_t, shift=LEFT * 0.2), run_time=0.8)

            # the part 1 warning: the host edit never reaches the baked-in copy
            st2, s2 = build_stack(2.6, -2.3)
            img2 = mono("cheese-app-api:local", 20, IMAGE).next_to(st2.floor, DOWN, buff=0.15)
            uf = file_card("utils.py", LAPTOP, size=22).move_to([-4.1, -0.25, 0])
            host = label("on your laptop", 22, LAPTOP).next_to(uf, DOWN, buff=0.25)
            edited = row_tag("edited", MODIFIED).next_to(uf, UP, buff=0.2)
            vo.wait_until("And the part 1 warning")
            self.play(FadeOut(VGroup(pp, tbars, left, err, right)), run_time=0.6)
            self.remove(pp, tbars, left, err, right)
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in s2], lag_ratio=0.08), FadeIn(img2),
                      run_time=1.0)
            st2.accept(self, *s2)
            vo.wait_until("edit utils.py")
            self.play(FadeIn(uf, shift=RIGHT * 0.2), FadeIn(host), run_time=0.6)
            self.play(uf.box.frame.animate.set_stroke(MODIFIED), FadeIn(edited, shift=DOWN * 0.1),
                      Indicate(uf.text, color=MODIFIED, scale_factor=1.1), run_time=0.8)
            vo.wait_until("still tests yesterday's copy")
            api = s2[2]
            link = DashedLine(uf.get_right() + RIGHT * 0.1, api.box.get_left() + LEFT * 0.12,
                              color=S.GREY, stroke_width=3, dash_length=0.12)
            x = cross_mark(0.32, ERR).move_to(link.get_center())
            old = label("yesterday's copy", 22, S.GREY).next_to(link, UP, buff=0.2)
            self.play(Create(link), run_time=0.6)
            self.play(FadeIn(x, scale=1.4), FadeIn(old, shift=DOWN * 0.1),
                      Indicate(api.box, color=IMAGE, scale_factor=1.05), run_time=0.8)
            vo.wait_until("Rebuild,")
            copies = s2[2:]
            reb = CurvedArrow(copies[0].box.get_right() + RIGHT * 0.25, copies[-1].box.get_right() + RIGHT * 0.25,
                              angle=PI / 2, color=TURN, stroke_width=4, tip_length=0.2)
            rlab = label("rebuild", 22, TURN).next_to(reb, RIGHT, buff=0.15)
            self.play(Create(reb), FadeIn(rlab), FadeOut(VGroup(link, x, old)), run_time=0.6)
            st2.rebuild(self, copies, run_time=1.2)
            self.play(uf.box.frame.animate.set_stroke(LAPTOP), FadeOut(edited), run_time=0.4)
            self.remove(edited)
            vo.wait_until("or you test the past")
            pbc = note("packages before code", S.GREY, 24).next_to(VGroup(s2[0], s2[1]), LEFT, buff=0.4)
            self.play(FadeIn(pbc, shift=RIGHT * 0.15), Indicate(VGroup(s2[0].box, s2[1].box), color=SYSTEM,
                                                                  scale_factor=1.03), run_time=0.9)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
