"""S01 · Red run, green summary (cold open of AC215 L21, the full follow-along). No tracker until
the sample in beat 6. Lecture: 21 · slides 1, 4 (beat 4 only).

Beats (script.md "## S01", one voiceover block each):
0. Black frame. GRAPH(run1) builds with every node GREY (tag 'illustration · colors from our live
   runs'). On "Soon after" the Test Summary node expands (the log grows out of it) into LOG(run1/test-summary/01:
   13–16), title "Test Summary › Check test results", the multi-line heading collapsed into one GREY
   row "Check test results", tag 'live · our fresh machine' (QA: 'stand-in runner' is explained only in S07); the graph dims to 20 % behind it.
   The three `success` words light GREEN one by one, then line 16 `✅ All tests passed!` grows GREEN
   (✅ drawn as a check mark). The log collapses back into its node, which turns GREEN.
1. A 1-row laptop strip along the bottom (no typing in this scene) prints act's last line
   ACT(750) `Error: Job 'Lint and Format Check' failed` in RED, GREY tag 'act (a local runner) · same file' on its
   bar. "Five machines green": Build and the three tests turn GREEN; "one red": Lint and Format
   Check turns RED; "and the whole run red": the run badge flips RED. Then the GREEN summary and the
   RED badge pulse in turn ("every test passed" / "the pipeline failed").
2. The strip fades; the graph dims except the RED lint node and the GREEN summary node, which pulse
   together. A YELLOW question card drops in under them: "Which machine said no, / and why didn't
   the summary hear it?"; on "By the end of part 1" it shrinks to 20 pt and pins top right, where it
   stays to the end of the scene.
3. The graph fades. Left: a GREY laptop frame "your laptop" with three GREY dashed gates and the
   dashed chip "lecture 9 · your hooks"; a GREEN commit dot passes them. A PINK arrow (chip "push ·
   main") carries it right into a BLUE box "GitHub", where six small BLUE machines light one after
   another; GREY caption "a fresh machine per job · nobody owns them".
4. lecture_ref(21, "1, 4") (under the pinned card, which holds the top-right corner). The picture
   fades; four WHITE-outlined labels appear in a row, one per phrase: Remote Git hooks, GitHub
   webhooks, Continuous integration, Continuous deployment; GREY caption "slide by slide · README
   Part 5 step by step".
5. Lecture tag off; the labels fade. Four chips, one per phrase: "a fresh clone (L09's has the fix
   committed)", "Docker running", "a GitHub account + a repository of your own", GREEN "no cloud · no
   keys · public repo: no bill".
6. The chips fade. Four samples, each on its phrase while the previous one dims to 30 %: the YELLOW
   tracker top-left (Part 5, step 1 of 8), a code panel `.github/workflows/ci.yml · lines 7–11`, a
   1-row laptop strip typing `git push` with a YELLOW '▶ your turn' row tag, and a tiny run graph
   with the GREY 'illustration' tag at the bottom right. Everything fades; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources (checked)
SUMMARY = capture("run1/test-summary/01")
assert SUMMARY.at((13, 16)) == ["Unit Tests: success", "Integration Tests: success", "System Tests: success",
                                "✅ All tests passed!"], SUMMARY.at((13, 16))
assert SUMMARY.step_name == "Check test results" and SUMMARY.exit == 0
ACT_LAST = act_lines(750)
assert ACT_LAST == ["Error: Job 'Lint and Format Check' failed"], ACT_LAST
RUN1 = results("run1")
assert RUN1["lint-and-format"] == "failure" and all(
    RUN1[j] == "success" for j in JOB_IDS if j != "lint-and-format"), RUN1
assert excerpt(".github/workflows/ci.yml", 7, 7).strip() == "on:"
QUESTION = "Which machine said no,\nand why didn't the summary hear it?"
SECTIONS_21 = (("Remote\nGit hooks", "remote Git hooks"), ("GitHub\nwebhooks", "GitHub webhooks"),
               ("Continuous\nintegration", "continuous integration"),
               ("Continuous\ndeployment", "and continuous deployment"))
CHIPS = (("a fresh clone (L09's has the fix committed)", "you need a fresh clone"),
         ("Docker running", "Docker running"),
         ("a GitHub account + a repository of your own", "a GitHub account"),
         ("no cloud · no keys · public repo: no bill", "No cloud and no keys"))
GRAPH_Y = 0.35                  # the run graph's centre (its tag stays above the 1-row strip)


def dim(m, f: float = 0.3):
    """Scale every part's own fill and stroke opacity by f (a stroke-only line stays unfilled, unlike
    set_opacity). Use as ApplyFunction(lambda m: dim(m, 0.3), group)."""
    for s in m.family_members_with_points():
        s.set_fill(opacity=s.get_fill_opacity() * f)
        s.set_stroke(opacity=s.get_stroke_opacity() * f)
    return m


def fade_to(m, f: float = 0.3, run_time: float = 0.5) -> ApplyFunction:
    """ANIM: m dims to f of its opacity."""
    return ApplyFunction(lambda x: dim(x, f), m, run_time=run_time)


def section_card(text: str, size: float = 24) -> VGroup:
    """One of slide 4's four sections: a WHITE-outlined card with a two-line label."""
    t = VGroup(*[label(s, size, INK) for s in text.split("\n")]).arrange(DOWN, buff=0.1)
    fr = RoundedRectangle(width=2.75, height=t.height + 0.55, corner_radius=0.14, stroke_color=INK,
                          stroke_width=2.5).set_fill(PANEL, 1)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 7, len(SAY)

        # ========================================================== 0. green summary
        graph = run_graph(None)
        graph.shift(UP * (GRAPH_Y - graph.get_center()[1]))
        summ = graph.nodes["test-summary"]
        log = run_log(SUMMARY, lines=((13, 16),), tag_text="live · our fresh machine").move_to([0, GRAPH_Y, 0])
        with self.voiceover(SAY[0]) as vo:
            mid = VGroup(*[graph.nodes[j] for j in MIDDLE])
            self.play(FadeIn(graph.badge, shift=DOWN * 0.15), FadeIn(graph.nodes["build"], shift=RIGHT * 0.2),
                      run_time=0.6)
            self.play(LaggedStart(*[Create(graph.edges[(s, d)]) for (s, d) in graph.edges if s == "build"],
                                  lag_ratio=0.1),
                      LaggedStart(*[FadeIn(n, shift=RIGHT * 0.2) for n in mid], lag_ratio=0.2), run_time=1.0)
            self.play(LaggedStart(*[Create(graph.edges[(s, d)]) for (s, d) in graph.edges if d == "test-summary"],
                                  lag_ratio=0.1),
                      FadeIn(summ, shift=RIGHT * 0.2), FadeIn(graph.tag), run_time=0.9)
            self.add(graph)
            vo.wait_until("Soon after")
            self.play(graph.pulse("test-summary", TURN), run_time=0.6)
            self.add(graph)
            self.play(fade_to(graph, 0.2), FadeIn(log, target_position=summ, scale=0.15), run_time=0.9)
            self.add(log)
            for k, cue in ((13, "unit tests, success"), (14, "Integration tests, success"),
                           (15, "System tests, success")):
                vo.wait_until(cue)
                w = substring(log.row(k), "success")
                self.play(w.animate.set_color(PASS).scale(1.15), run_time=0.3)
                self.play(w.animate.scale(1 / 1.15), run_time=0.25)
            vo.wait_until("All tests passed")
            last = log.row(16)
            self.play(last.animate.set_color(PASS).scale(1.12), run_time=0.45)
            self.play(last.animate.scale(1 / 1.12), Circumscribe(last, color=PASS, buff=0.08), run_time=0.7)
            self.play(FadeOut(log, target_position=summ, scale=0.15), fade_to(graph, 5.0), run_time=0.8)
            self.remove(log)
            self.play(graph.set_state("test-summary", "success"), run_time=0.4)
            self.add(graph)

        # ========================================================== 1. act: the same file fails
        strip = term(rows=1)
        bar_tag = on_bar(strip, row_tag("act (a local runner) · same file"))
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(strip, shift=UP * 0.3), FadeIn(bar_tag, shift=UP * 0.3), run_time=0.5)
            strip.add(bar_tag)
            vo.wait_until("run end to end")
            flash_tag(self, bar_tag, INK)
            vo.wait_until("job Lint and Format Check failed")
            err_ln = out(self, strip, [(ACT_LAST[0], ERR)], run_time=0.5)[0]
            self.play(Indicate(err_ln, color=ERR, scale_factor=1.05), run_time=0.6)
            vo.wait_until("Five machines green")
            self.play(*[graph.set_state(j, "success") for j in ("build",) + TEST_JOBS], run_time=0.6)
            self.add(graph)
            vo.wait_until("one red")
            self.play(graph.set_state("lint-and-format", "failure"), run_time=0.5)
            self.add(graph)
            vo.wait_until("and the whole run red")
            self.play(graph.set_badge("failure"), run_time=0.5)
            self.add(graph)
            vo.wait_until("The pipeline says every test passed")
            self.play(graph.pulse("test-summary", PASS), run_time=0.7)
            self.add(graph)
            vo.wait_until("and the pipeline failed")
            self.play(Circumscribe(graph.badge, color=ERR, buff=0.06),
                      Indicate(VGroup(graph.badge.mark, graph.badge.text), color=ERR, scale_factor=1.06),
                      run_time=0.7)
            self.add(graph)

        # ========================================================== 2. the question
        others = VGroup(*[graph.nodes[j] for j in JOB_IDS if j not in ("lint-and-format", "test-summary")],
                        *graph.edges.values(), graph.badge, graph.tag)
        lint = graph.nodes["lint-and-format"]
        card = question_card(QUESTION)
        card.move_to([(lint.get_center()[0] + summ.get_center()[0]) / 2, -2.75, 0])
        small = question_card(QUESTION, size=20)
        small.move_to([6.6 - small.width / 2, 3.6 - small.height / 2, 0])
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(strip), fade_to(others, 0.25), run_time=0.6)
            self.remove(strip, bar_tag)
            self.play(graph.pulse("lint-and-format", ERR), graph.pulse("test-summary", PASS), run_time=0.8)
            self.add(graph)
            self.play(FadeIn(card, shift=DOWN * 0.6), run_time=0.6)
            vo.wait_until("By the end of part 1")
            self.play(Transform(card, small), run_time=0.8)
            vo.wait_until("In part 2")
            self.play(graph.pulse("lint-and-format", ERR), graph.pulse("test-summary", PASS), run_time=0.8)
            self.add(graph)

        # ========================================================== 3. from your laptop to GitHub
        lap = box(4.6, 2.5, LAPTOP, fill_opacity=0.06, radius=0.2).move_to([-3.9, 0.2, 0])
        lap_t = label("your laptop", 22, LAPTOP).next_to(lap.get_corner(UL), DR, buff=0.18)
        gates = VGroup(*[dashed_copy(gate_glyph(0.7, 0.6)) for _ in range(3)]).arrange(RIGHT, buff=0.55)
        gates.move_to(lap).shift(DOWN * 0.25)
        hooks = dashed_chip("lecture 9 · your hooks").next_to(lap, DOWN, buff=0.2)
        laptop_g = VGroup(lap, lap_t, gates, hooks)
        gh = box(4.6, 2.5, GITHUB, fill_opacity=0.1, radius=0.2).move_to([3.9, 0.2, 0])
        gh_t = label("GitHub", 24, GITHUB).next_to(gh.get_corner(UL), DR, buff=0.18)
        runners = VGroup(*[runner_icon(0.5) for _ in range(6)]).arrange_in_grid(2, 3, buff=(0.45, 0.3))
        runners.move_to(gh).shift(DOWN * 0.22)
        fresh = label("a fresh machine per job · nobody owns them", 20, S.GREY).next_to(gh, DOWN, buff=0.2)
        fresh.align_to(gh, RIGHT)
        gh_g = VGroup(gh, gh_t, runners)
        y_dot = gates.get_center()[1]
        c_dot = dot(PASS).move_to([lap.get_left()[0] + 0.35, y_dot, 0])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(graph), run_time=0.5)
            self.remove(graph)
            self.play(FadeIn(VGroup(lap, lap_t)), LaggedStart(*[Create(g) for g in gates], lag_ratio=0.2),
                      run_time=0.8)
            self.play(FadeIn(hooks, shift=UP * 0.15), FadeIn(c_dot, scale=0.5), run_time=0.4)
            vo.wait_until("before a commit")
            for g in gates:
                self.play(c_dot.animate.move_to([g.get_center()[0], y_dot, 0]), run_time=0.3)
                self.play(Indicate(g, color=PASS, scale_factor=1.1), run_time=0.25)
            self.play(c_dot.animate.move_to([lap.get_right()[0] - 0.3, y_dot, 0]), run_time=0.3)
            vo.wait_until("Today they move to GitHub")
            self.play(FadeIn(gh_g, shift=LEFT * 0.3), run_time=0.6)
            a, b = c_dot.get_center(), np.array([gh.get_left()[0] + 0.35, y_dot, 0])
            path = route(a, b, arc=-0.4)
            track_ = Line(a, b, path_arc=-0.4)
            self.play(Create(path), MoveAlongPath(c_dot, track_), run_time=1.0)
            vo.wait_until("and they run on every push to main")
            push_c = route_chip("push · main").next_to(path, UP, buff=0.12)
            self.play(FadeIn(push_c, shift=DOWN * 0.15), Flash(c_dot, color=ROUTE), run_time=0.6)
            vo.wait_until("on fresh machines")
            self.play(FadeOut(c_dot, scale=0.4), FadeIn(fresh, shift=UP * 0.1), run_time=0.4)
            for i, r in enumerate(runners):
                lit = runner_icon(0.5, lit=True).move_to(r)
                self.play(Transform(r, lit), run_time=0.22)

        # ========================================================== 4. the lecture's four sections
        lr = lref("1, 4")
        lr.next_to(small, DOWN, buff=0.15).align_to(small, RIGHT)
        cards = VGroup(*[section_card(s) for s, _ in SECTIONS_21]).arrange(RIGHT, buff=0.3).move_to([0, 0.35, 0])
        cap = label("slide by slide · README Part 5 step by step", 24, S.GREY).next_to(cards, DOWN, buff=0.55)
        picture = VGroup(laptop_g, gh_g, path, push_c, fresh)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeIn(lr), FadeOut(picture), run_time=0.6)
            self.remove(picture)
            for c, (_, cue) in zip(cards, SECTIONS_21):
                vo.wait_until(cue)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.45)
            vo.wait_until("We follow it slide by slide")
            self.play(FadeIn(cap, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("and the README Part 5")
            self.play(Indicate(cap, color=TURN, scale_factor=1.05), run_time=0.7)

        # ========================================================== 5. what you need
        chips = VGroup(*[grey_chip(s, size=24) for s, _ in CHIPS[:3]], ok_chip(CHIPS[3][0], size=24))
        chips.arrange(DOWN, buff=0.32).move_to([0, 0.0, 0])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(lr), FadeOut(cards), FadeOut(cap), run_time=0.5)
            self.remove(lr, cards, cap)
            for c, (_, cue) in zip(chips, CHIPS):
                vo.wait_until(cue)
                self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.45)
            vo.wait_until("and on a public repository")
            self.play(Circumscribe(chips[3], color=PASS, buff=0.08), run_time=0.8)

        # ========================================================== 6. how to read this video
        tr = tracker_p5(1)
        panel = code(".github/workflows/ci.yml", 7, 11).move_to([-1.2, 0.55, 0])
        demo = term(rows=1)
        mini = graph_icon(1.3)
        ill = illustration_tag()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(chips), run_time=0.4)
            self.remove(chips)
            self.play(FadeIn(tr, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("code panels name their file and lines")
            self.play(fade_to(tr), FadeIn(panel, shift=UP * 0.2), run_time=0.5)
            self.play(Circumscribe(panel.header, color=TURN, buff=0.06), run_time=0.7)
            vo.wait_until("and a yellow tag, your turn")
            self.play(fade_to(panel), FadeIn(demo, shift=UP * 0.2), run_time=0.5)
            ln = type_cmd(self, demo, "git push", type_time=0.5)
            turn = beside(turn_row(), ln, buff=0.5)
            pin(self, ln, turn)
            flash_tag(self, turn, TURN)
            self.add(demo)
            vo.wait_until("The runs you will see")
            mini.move_to([4.4, -1.25, 0])
            ill.next_to(mini, LEFT, buff=0.3)
            self.play(fade_to(demo), FadeIn(mini, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("the GitHub pages are drawings")
            self.play(FadeIn(ill, shift=RIGHT * 0.15), run_time=0.4)
            flash_tag(self, ill)
            vo.wait_until("and they say so")
            flash_tag(self, ill, INK, run_time=0.6)

        everything = VGroup(tr, panel, demo, mini, ill, card)
        self.play(FadeOut(everything), run_time=0.6)
        self.remove(everything, *everything.get_family())
        self.wait(0.3)
