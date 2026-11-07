"""S16 · Non-determinism, CD next, and recap (AC215 L21, part 2, last scene). No tracker, no strip.
Lecture: 21 · 18–20 (beat 0), 21 · 32–34 (beat 1), off from beat 2. Set pieces V2 CiLoop (beats 1
and 3), small text-free copies of V1, V4, V5, V6 and S02's door for the questions. Ends on an empty
frame.

Beats (script.md "## S16", one voiceover block each):
0. LECTURE 21 · 18–20. A GREY header "when the code trains a model"; four GREY stage boxes in a row,
   "training", "data", "tests", "deployment"; each gets a small YELLOW wobbling "?" (non-determinism).
   Four GREEN answer chips drop under them, one per phrase: "version everything (L11: DVC)",
   "automate retraining and testing" (+ YELLOW chip "Milestone 5"), "monitor in production",
   "controlled rollout".
1. LECTURE 21 · 32–34. The row goes; V2 CiLoop (left of centre). Its Test box grows a GREY dashed
   arrow to the GREY dashed "Deploy (CD) · lecture 23" box (CiLoop.deploy); above, the repo name
   `cheese-app-ci-cd` with "ci" GREEN and "cd" GREY in a dashed outline.
2. LECTURE off. The loop goes; a GREY teardown card with four items, each ticking GREEN on its
   phrase (item 1's four rows light one by one: git checkout main · git branch -D … · git push origin
   --delete … (closes the PR) · Settings → Branches: delete the rule; then Slack; private repo: Disable
   workflow; local: L09's Docker cleanup (README 568–574) · act's images).
3. The card fades; V2 CiLoop one last time, a part per phrase: the PINK Commits arrow ("event"); six
   BLUE rooms flash under Build (1) and Test (5) ("fresh machine"); a TEAL suitcase rides from
   Build's room to Test's ("artifact"); above Test a gate holds a GREEN 0 (opens) then a RED 1
   (shuts) ("exit code"); three PINK tokens ride Test's return line into Notifications while a GREY
   dashed "Lint" box stays outside ("only the jobs it needs").
4.–8. "Test yourself" (YELLOW heading, "question k of 5 · answers in exercises.md"), one YELLOW
   question card at a time with a small text-free picture that moves on its phrase: (1) a laptop
   with three hook gates, a RED dashed arc over them into a BLUE repo box whose two gates turn GREEN;
   (2) a BLUE room whose shelf empties on "fresh machine", then a suitcase lands and unfolds;
   (3) V4's graph, lint turns RED and its token stops at the dashed gap, the three test tokens reach
   the summary; (4) V6's two gates, Flake8 shunted, then Black shuts and Flake8 is skipped; (5) the
   door and bell: pre-receive gate pulses, the dot crosses the door and the bell rings, then a GREEN
   protection gate docks at the door. A GREY chip "answers: exercises.md · every command: the study
   guide". Fade out; empty frame.

Deviations from SHOW: the "?" marks are YELLOW (the loop's question colour); beat 0 adds a small GREY
header so the four boxes read as stages of an ML project. Question 4's picture uses V6's own
labelled gates (names at 20 pt, not scaled); the other pictures are text-free.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _elbow

SAY = NARRATION["S16"]
SX, SY = 6.6, 3.6

STAGES = ("training", "data", "tests", "deployment")
ANSWERS = (("version everything", "(L11: DVC)"), ("automate retraining", "and testing"),
           ("monitor", "in production"), ("controlled", "rollout"))

QUESTIONS = (
    ["Name two ways code reaches the shared repository", "without passing your local hooks.",
     "Which checks does this pipeline repeat,", "and which not?"],
    ["Which unit gets a fresh machine, a job or a step?", "Why does that force the image tar",
     "and a docker load in every check job?"],
    ["Your run is red but Test Summary says", "✅ All tests passed!",
     "Explain, and give the one-line fix."],
    ["Why can Flake8 fail without failing its job,", "and why don't you see Flake8's output",
     "when Black fails?"],
    ["In the lecture's terms, is a push-triggered", "Actions run a pre-receive or a post-receive",
     "check, and what turns it into a gate", "on GitHub.com?"],
)
EMOJI_LINE = (2, 1)          # question 3, line 2: the summary's real output, drawn emoji-safe

assert set(results("run1").values()) == {"success", "failure"}
assert results("run1")["lint-and-format"] == "failure" and results("run1")["test-summary"] == "success"


# ------------------------------------------------------------------ helpers
def stage_box(s: str) -> VGroup:
    t = label(s, 26, S.GREY)
    fr = box(2.8, 0.9, S.GREY, fill_opacity=0.08)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def answer_chip(lines, color=PASS, size: float = 22, chip_w: float = 2.9) -> VGroup:
    t = VGroup(*[label(s, size, INK) for s in lines]).arrange(DOWN, buff=0.08)
    fr = box(max(chip_w, t.width + 0.4), t.height + 0.32, color, fill_opacity=0.14)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def parts_row(*parts, size: float = 20) -> VGroup:
    """A row: 'text' label INK, ('text', 'm') mono INK."""
    ms = []
    for p in parts:
        s, kind = (p, "l") if isinstance(p, str) else p
        ms.append(mono(s, size, INK) if kind == "m" else label(s, size, INK))
    return VGroup(*ms).arrange(RIGHT, buff=0.14)


TEAR = (
    [parts_row("Part 6:", ("git checkout main", "m")),
     parts_row(("git branch -D feature/test-protection", "m")),
     parts_row(("git push origin --delete feature/test-protection", "m"), "(closes the PR)"),
     parts_row("Settings → Branches: delete the rule")],
    [parts_row("Slack: delete the secret + the incoming webhook")],
    [parts_row("private repo: Actions → CI Pipeline → ⋯ → Disable workflow")],
    [parts_row("local: L09's Docker cleanup (README 568–574) · act's images")],
)


def tick_box(h: float = 0.32) -> VGroup:
    return RoundedRectangle(width=h, height=h, corner_radius=0.05, stroke_color=S.GREY, stroke_width=2.5)


def teardown_card() -> VGroup:
    """GREY card 'Clean up', four items with a tick box each. .frame .head .items .boxes .rows"""
    head = label("Clean up", 24, S.GREY)
    items, boxes = [], []
    for rows in TEAR:
        body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        bx = tick_box().next_to(rows[0], LEFT, buff=0.25)
        items.append(VGroup(bx, body))
        boxes.append(bx)
    col = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
    inner = VGroup(head, col).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    fr = box(inner.width + 0.7, inner.height + 0.6, S.GREY, fill_opacity=0.06)
    inner.move_to(fr)
    g = VGroup(fr, head, *items)
    g.frame, g.head, g.items, g.boxes = fr, head, items, boxes
    g.rows = [r for rows in TEAR for r in rows]
    return g


def repo_name() -> VGroup:
    """'cheese-app-ci-cd': 'ci' GREEN, 'cd' GREY in a dashed outline. .ci .cd .cd_box
    One mono_line (a shared baseline: separate Text pieces aligned DOWN dropped the '-' to the
    baseline, so the name read 'ci_cd')."""
    name = "cheese-app-ci-cd"
    line = mono_line(name, 26, INK, t2c={"[11:13]": PASS, "[14:16]": S.GREY})
    ci, cd = substring(line, "ci"), glyph_range(line, 14, 16)
    ob = outline_box(cd.width + 0.22, line.strut.height + 0.06, S.GREY).move_to(
        [cd.get_center()[0], line.strut.get_center()[1], 0])
    g = VGroup(line, ob)
    g.ci, g.cd, g.cd_box = ci, cd, ob
    return g


def q_card(lines, k: int, card_w: float = 8.4, size: float = 24) -> VGroup:
    rows = []
    for i, s in enumerate(lines):
        rows.append(emo_line(s, size, INK) if (k, i) == EMOJI_LINE else label(s, size, INK))
    t = VGroup(*rows).arrange(DOWN, buff=0.14)
    fr = RoundedRectangle(width=card_w, height=t.height + 0.55, corner_radius=0.16, stroke_color=TURN,
                          stroke_width=3).set_fill(S.BG, 0.96)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


# ------------------------------------------------------------------ the small pictures
def icon_hooks() -> VGroup:
    """Q1: a laptop with three hook gates; a BLUE repo box with two gates. .laptop .gates .repo .rgates"""
    lp = laptop_icon(1.5)
    gates = VGroup(*[gate_glyph(0.3, 0.3, S.GREY) for _ in range(3)]).arrange(RIGHT, buff=0.1)
    gates.move_to(lp[0])
    repo = box(1.4, 1.3, GITHUB, fill_opacity=0.1, radius=0.16)
    rg = VGroup(*[gate_glyph(0.3, 0.34, S.GREY) for _ in range(2)]).arrange(RIGHT, buff=0.16).move_to(repo)
    left = VGroup(lp, gates)
    right = VGroup(repo, rg)
    VGroup(left, right).arrange(RIGHT, buff=0.5)
    right.align_to(lp[0], UP)
    g = VGroup(left, right)
    g.laptop, g.gates, g.repo, g.rgates = lp, gates, repo, rg
    return g


def icon_room() -> VGroup:
    """Q2: a BLUE room with a shelf and a cube on it. .frame .shelf .cube"""
    fr = box(2.6, 1.7, GITHUB, fill_opacity=0.08, radius=0.14)
    sh = shelf(1.5, text=None).move_to(fr.get_bottom() + UP * 0.45)
    cb = cube_glyph(0.45).next_to(sh.board, UP, buff=0.04)
    g = VGroup(fr, sh, cb)
    g.frame, g.shelf, g.cube = fr, sh, cb
    return g


def icon_graph() -> JobGraph:
    """Q3: V4 text-free, every node idle, edges drawn, the gap hidden (shown on 'red')."""
    return JobGraph(labels=None, pitch=0.62, col_gap=0.7, badge=False, tag_text=None)


def swap_node(scene, g: JobGraph, jobs, state: str, run_time: float = 0.4):
    """PLAYS: text-free nodes change state by a cross-fade (a Transform from the idle mark's empty
    centre flies the new mark in from elsewhere)."""
    olds, news = [], []
    for j in jobs:
        nd = g.nodes[j]
        new = g._node(j, state, None).move_to(nd)
        olds.append(nd)
        news.append(new)
    scene.play(*[FadeOut(o) for o in olds], *[FadeIn(n) for n in news], run_time=run_time)
    for j, o, n in zip(jobs, olds, news):
        g.remove(o)
        g.add(n)
        g.nodes[j] = n
        g.states[j] = state
    scene.add(g)


def icon_door() -> VGroup:
    """Q5: S02's door and bell, text-free. .server .door .gate .bell .start .landing"""
    sv = box(2.2, 1.7, GITHUB, fill_opacity=0.08, radius=0.18)
    door = Rectangle(width=0.14, height=0.8, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1)
    door.move_to(sv.get_left())
    gate = gate_glyph(0.7, 0.55, S.GREY).move_to(door.get_center() + LEFT * 1.45)
    bell = bell_glyph(0.6, S.GREY).move_to(sv.get_center() + RIGHT * 0.3 + UP * 0.1)
    g = VGroup(sv, door, gate, bell)
    g.server, g.door, g.gate, g.bell = sv, door, gate, bell
    return g


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S16"] == 9, len(SAY)

        # ========================================================== 0. non-determinism, four answers
        ref0 = lref("18–20")
        head0 = label("when the code trains a model", 26, S.GREY).move_to([0, 2.45, 0])
        xs = (-4.95, -1.65, 1.65, 4.95)
        stages = VGroup(*[stage_box(s).move_to([x, 1.1, 0]) for s, x in zip(STAGES, xs)])
        qs = VGroup(*[label("?", 32, TURN).next_to(b.frame.get_corner(UR), UP, buff=0.08).shift(LEFT * 0.3)
                      for b in stages])
        answers = [answer_chip(a).move_to([x, -0.95, 0]) for a, x in zip(ANSWERS, xs)]
        m5 = chip("Milestone 5", TURN, size=22).next_to(answers[1], DOWN, buff=0.35)
        assert qs.get_top()[1] < head0.get_bottom()[1] + 0.3
        for a in answers:
            assert a.get_left()[0] > -SX and a.get_right()[0] < SX, a.get_corner(DR)
        for a, b in zip(answers, answers[1:]):
            assert a.get_right()[0] < b.get_left()[0] - 0.1, (a.get_right(), b.get_left())
        assert head0.get_top()[1] < ref0.get_bottom()[1] - 0.1
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref0), FadeIn(head0, shift=DOWN * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.15) for b in stages], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("non-determinism enters every stage")
            self.play(LaggedStart(*[FadeIn(q, scale=1.6) for q in qs], lag_ratio=0.25), run_time=1.0)
            self.play(*[Wiggle(q, scale_value=1.25, rotation_angle=0.08 * TAU) for q in qs], run_time=1.4)
            vo.wait_until("Its answers")
            self.play(*[Wiggle(q, scale_value=1.2, rotation_angle=0.06 * TAU) for q in qs], run_time=1.0)
            vo.wait_until("version everything")
            self.play(FadeIn(answers[0], shift=DOWN * 0.4), run_time=0.5)
            vo.wait_until("automate retraining")
            self.play(FadeIn(answers[1], shift=DOWN * 0.4), run_time=0.5)
            vo.wait_until("which Milestone 5")
            self.play(FadeIn(m5, shift=UP * 0.2), run_time=0.4)
            self.play(Indicate(m5, color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("monitor")
            self.play(FadeIn(answers[2], shift=DOWN * 0.4), run_time=0.5)
            vo.wait_until("and roll out")
            self.play(FadeIn(answers[3], shift=DOWN * 0.4), run_time=0.5)
            self.play(LaggedStart(*[Indicate(a.text, color=PASS, scale_factor=1.06) for a in answers],
                                  lag_ratio=0.2), run_time=1.0)

        # ========================================================== 1. CD is lecture 23
        ref1 = lref("32–34")
        loop = CiLoop().move_to([-1.2, -0.55, 0])
        rn = repo_name().move_to([-1.2, 2.55, 0])
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(head0, stages, qs, *answers, m5)), ReplacementTransform(ref0, ref1),
                      run_time=0.5)
            self.play(FadeIn(loop), FadeIn(rn[0], shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(rn.ci, color=PASS, scale_factor=1.2), run_time=0.6)
            vo.wait_until("automates the release")
            cd = loop.deploy(self, run_time=0.8)
            assert cd.get_right()[0] < SX, cd.get_right()
            vo.wait_until("that's lecture 23")
            self.play(Create(rn.cd_box.frame), Indicate(rn.cd, color=S.GREY, scale_factor=1.2),
                      Indicate(cd[1], color=S.GREY, scale_factor=1.08), run_time=0.8)

        # ========================================================== 2. teardown
        card = teardown_card().move_to([0, 0.1, 0])
        assert card.frame.width <= 2 * SX and card.frame.height <= 2 * SY - 0.3, (card.frame.width, card.frame.height)
        rows = card.rows

        def tick(k):
            t = check_mark(0.3, PASS).move_to(card.boxes[k])
            self.play(Create(t), card.boxes[k].animate.set_stroke(PASS), run_time=0.35)
            return t

        def light(row):
            """The spoken row turns GREEN and stays so (where we are on the card stays visible)."""
            self.play(row.animate.set_color(PASS), run_time=0.5)

        ticks = []
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(loop, rn)), FadeOut(ref1), run_time=0.5)
            self.remove(loop, *loop.get_family())
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("switch to main")
            light(rows[0])
            vo.wait_until("and delete the test protection branch")
            light(rows[1])
            vo.wait_until("and on GitHub")
            light(rows[2])
            vo.wait_until("Remove the branch rule")
            light(rows[3])
            ticks.append(tick(0))
            vo.wait_until("and the Slack secret")
            light(rows[4])
            ticks.append(tick(1))
            vo.wait_until("Disable the workflow")
            light(rows[5])
            ticks.append(tick(2))
            vo.wait_until("and run the Docker cleanup")
            light(rows[6])
            ticks.append(tick(3))

        # ========================================================== 3. the loop, one last time
        loop = CiLoop().move_to([-0.6, -0.7, 0])
        b = loop.boxes
        bx, tx = b["build"].get_x(), b["test"].get_x()
        top_y = b["build"].frame.get_bottom()[1]
        bar_y = loop.notify.bar.get_top()[1]
        r_build = runner_icon(0.34, lit=True).move_to([bx - 0.5, (top_y + bar_y) / 2 + 0.3, 0])
        r_test = VGroup(*[runner_icon(0.3, lit=True) for _ in range(5)]).arrange(DOWN, buff=0.12)
        r_test.move_to([tx + 0.5, (top_y + bar_y) / 2, 0])
        assert r_test.get_top()[1] < top_y - 0.05 and r_test.get_bottom()[1] > bar_y + 0.05, r_test.get_top()
        rooms = VGroup(r_build, r_test)
        case = suitcase_glyph(0.32).next_to(r_build, DOWN, buff=0.12)
        gate = gate_glyph(0.55, 0.6, S.GREY).move_to(b["test"].get_top() + UP * 0.95)
        c0 = chip("0", PASS, size=22, font=MONO).next_to(gate, RIGHT, buff=0.25)
        c1 = chip("1", ERR, size=22, font=MONO).next_to(gate, RIGHT, buff=0.25)
        assert gate.get_bottom()[1] > loop.row_frame.get_top()[1] + 0.1
        lint = dashed_chip("Lint", S.GREY, size=22).next_to(loop.notify.bar, RIGHT, buff=0.75)
        stub = DashedLine(lint.get_left() + LEFT * 0.08, loop.notify.bar.get_right() + RIGHT * 0.25,
                          color=S.GREY, stroke_width=2.5, dash_length=0.08)
        assert lint.get_right()[0] < SX, lint.get_right()
        # CiLoop.return_paths are not members of the piece (they stay where it was built): use the
        # dashed return line itself, which moved with the loop
        ret = Line(loop.returns[1].get_start(), loop.returns[1].get_end())
        toks = VGroup(*[Dot(radius=0.09, color=ROUTE) for _ in range(3)])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(card, *ticks)), run_time=0.5)
            self.play(FadeIn(loop), run_time=0.7)
            vo.wait_until("Your push is the event")
            flash = loop.commits[0].copy().set_stroke(ROUTE, 9)
            self.play(Create(flash), Indicate(loop.commits[2], color=ROUTE, scale_factor=1.2), run_time=0.8)
            self.play(FadeOut(flash), run_time=0.3)
            vo.wait_until("Each job gets a fresh machine")
            self.play(LaggedStart(FadeIn(r_build, scale=0.6), *[FadeIn(r, scale=0.6) for r in r_test],
                                  lag_ratio=0.15), run_time=1.0)
            self.play(Indicate(rooms, color=GITHUB, scale_factor=1.1), run_time=0.6)
            vo.wait_until("so the image travels")
            self.play(FadeIn(case, scale=0.6), run_time=0.3)
            self.play(case.animate.next_to(r_test, LEFT, buff=0.15), run_time=1.1)
            self.play(Indicate(case, color=IMAGE, scale_factor=1.2), run_time=0.5)
            vo.wait_until("Every step is a gate")
            self.play(FadeOut(VGroup(rooms, case)), FadeIn(gate, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("that reads an exit code")
            self.play(FadeIn(c0, shift=UP * 0.15), run_time=0.3)
            self.play(Transform(gate.bar, gate.bar.copy().rotate(PI / 2.4, about_point=gate.bar.get_start())
                                .set_color(PASS)), run_time=0.4)
            self.play(Transform(gate.bar, gate.bar.copy().rotate(-PI / 2.4, about_point=gate.bar.get_start())
                                .set_color(S.GREY)), FadeOut(c0), run_time=0.3)
            self.play(FadeIn(c1, shift=UP * 0.15), gate.bar.animate.set_color(ERR),
                      Indicate(gate.posts, color=ERR, scale_factor=1.05), run_time=0.5)
            vo.wait_until("and the summary hears only")
            self.play(FadeOut(VGroup(gate, c1)), FadeIn(lint), Create(stub), run_time=0.5)
            for t in toks:
                t.move_to(ret.get_start())
            self.play(FadeIn(toks), run_time=0.2)
            self.play(LaggedStart(*[MoveAlongPath(t, ret) for t in toks], lag_ratio=0.3), run_time=1.2)
            self.play(FadeOut(toks, scale=0.4), loop.light("notify", ROUTE), Wiggle(lint, scale_value=1.05),
                      run_time=0.8)

        # ========================================================== 4-8. test yourself
        head = label("Test yourself", 30, TURN).move_to([-6.4, 2.75, 0], aligned_edge=LEFT)
        counters = [label(f"question {k + 1} of 5 · answers in exercises.md", 22, S.GREY) for k in range(5)]
        for c in counters:
            c.next_to(head, RIGHT, buff=0.4).align_to(head, DOWN)
            assert c.get_right()[0] < SX, c.get_right()
        qcards = [q_card(q, k).move_to([-2.15, 0.1, 0]) for k, q in enumerate(QUESTIONS)]
        for q in qcards:
            assert q.text.width < q.frame.width - 0.3, q.text.width
            assert q.get_left()[0] > -SX and q.get_top()[1] < head.get_bottom()[1] - 0.15, q.get_corner(UL)
        IX, IY = 4.45, 0.1
        i1 = icon_hooks().move_to([IX, IY, 0])
        i2 = icon_room().move_to([IX, IY, 0])
        i3 = icon_graph()
        off = np.array([IX, IY, 0]) - i3.get_center()
        i3.shift(off)
        i3.gap.shift(off)                     # gap and '?' are not members until show_gap()
        i3.gap_q.shift(off)
        i4 = ExitGates(names=("Black", "Flake8"), gate_h=0.55).move_to([IX - 0.35, IY, 0])
        i5 = icon_door().move_to([IX, IY, 0])
        icons = [i1, i2, i3, i4, i5]
        for q, ic in zip(qcards, icons):
            assert q.get_right()[0] < ic.get_left()[0] - 0.2, (q.get_right(), ic.get_left())
            assert ic.get_right()[0] < SX - 0.05 and ic.get_bottom()[1] > -SY, ic.get_corner(DR)
        ans = grey_chip("answers: exercises.md · every command: the study guide", size=22)
        ans.next_to(qcards[4], DOWN, buff=0.4).align_to(qcards[4], LEFT)
        assert ans.get_bottom()[1] > -SY and ans.get_right()[0] < SX, ans.get_corner(DR)
        cur = None
        for k in range(5):
            with self.voiceover(SAY[4 + k]) as vo:
                if k == 0:
                    self.play(FadeOut(VGroup(loop, lint, stub)), FadeIn(head, shift=DOWN * 0.1),
                              FadeIn(counters[0]), run_time=0.7)
                    self.remove(loop, *loop.get_family())
                    vo.wait_until("One:")
                    self.play(FadeIn(qcards[0], shift=UP * 0.15), FadeIn(i1), run_time=0.6)
                else:
                    self.play(FadeOut(cur[0], shift=LEFT * 0.4), FadeOut(cur[1]), FadeOut(counters[k - 1]),
                              run_time=0.35)
                    self.remove(cur[1], *cur[1].get_family())
                    self.play(FadeIn(qcards[k], shift=LEFT * 0.4), FadeIn(icons[k]), FadeIn(counters[k]),
                              run_time=0.45)
                cur = (qcards[k], icons[k])
                if k == 0:
                    vo.wait_until("name two ways")
                    self.play(Indicate(qcards[0].text[0], color=TURN, scale_factor=1.04), run_time=0.7)
                    vo.wait_until("without passing your local hooks")
                    a = i1.gates.get_left() + LEFT * 0.15
                    z = i1.repo.get_left() + RIGHT * 0.25 + UP * 0.2
                    arc = DashedVMobject(ArcBetweenPoints(a, z, angle=-PI * 0.55), num_dashes=16).set_stroke(ERR, 3.5)
                    d = dot(PASS, 0.11).move_to(a)
                    self.play(FadeIn(d), Create(arc), run_time=0.7)
                    self.play(MoveAlongPath(d, ArcBetweenPoints(a, z, angle=-PI * 0.55)), run_time=0.9)
                    i1.add(arc, d)
                    vo.wait_until("Which checks does this pipeline repeat")
                    self.play(*[g.bar.animate.set_color(PASS) for g in i1.rgates],
                              Indicate(i1.rgates, color=PASS, scale_factor=1.1), run_time=0.7)
                    self.play(Indicate(i1.gates, color=S.GREY, scale_factor=1.1), run_time=0.7)
                elif k == 1:
                    vo.wait_until("which unit gets a fresh machine")
                    self.play(Indicate(qcards[1].text[0], color=TURN, scale_factor=1.04), run_time=0.7)
                    self.play(FadeOut(i2.cube, shift=UP * 0.3), Indicate(i2.shelf, color=S.GREY), run_time=0.7)
                    i2.remove(i2.cube)
                    vo.wait_until("And why does that force")
                    sc = suitcase_glyph(0.36).next_to(i2.frame, UP, buff=0.1)
                    self.play(FadeIn(sc, shift=DOWN * 0.2), run_time=0.3)
                    self.play(sc.animate.next_to(i2.shelf.board, UP, buff=0.04), run_time=0.6)
                    cb = cube_glyph(0.45).next_to(i2.shelf.board, UP, buff=0.04)
                    self.play(ReplacementTransform(sc, cb), run_time=0.6)
                    i2.add(cb)
                elif k == 2:
                    vo.wait_until("your run is red")
                    swap_node(self, i3, ["lint-and-format"], "failure", run_time=0.5)
                    lp_, sp_ = i3.nodes["lint-and-format"].get_right(), i3.nodes["test-summary"].get_left()
                    gpath = _elbow(lp_, sp_, lp_[0] + (sp_[0] - lp_[0]) * 0.62)
                    lt = Dot(radius=0.08, color=ROUTE).move_to(lp_)
                    i3.show_gap(self, run_time=0.5)
                    self.play(FadeIn(lt), run_time=0.2)
                    self.play(MoveAlongPath(lt, gpath), rate_func=lambda t: 0.55 * t, run_time=0.8)
                    self.play(Indicate(i3.gap_q, color=TURN, scale_factor=1.3), run_time=0.5)
                    i3.add(lt)
                    vo.wait_until("but the summary says")
                    swap_node(self, i3, ["unit-tests", "integration-tests", "system-tests"], "success")
                    tk = VGroup(*[Dot(radius=0.08, color=ROUTE).move_to(i3.edges[(j, "test-summary")].get_start())
                                  for j in ("unit-tests", "integration-tests", "system-tests")])
                    self.play(FadeIn(tk), run_time=0.2)
                    self.play(*[MoveAlongPath(t, i3.edges[(j, "test-summary")]) for t, j in
                                zip(tk, ("unit-tests", "integration-tests", "system-tests"))], run_time=0.8)
                    self.play(FadeOut(tk, scale=0.3), run_time=0.3)
                    swap_node(self, i3, ["test-summary"], "success")
                    vo.wait_until("Why, and what is the one-line fix")
                    self.play(Indicate(qcards[2].text[2], color=TURN, scale_factor=1.04), i3.pulse("lint-and-format", TURN),
                              run_time=0.8)
                elif k == 3:
                    vo.wait_until("why can Flake8 fail without failing its job")
                    self.play(Indicate(i4.names[1], color=TURN, scale_factor=1.2), run_time=0.5)
                    vo.wait_until("without failing its job")
                    i4.shunt(self, 1, 1)
                    vo.wait_until("and why don't you see its output")
                    i4.reset(self)
                    self.play(Indicate(i4.names[1], color=TURN, scale_factor=1.2), run_time=0.4)
                    vo.wait_until("when Black fails")
                    i4.hold(self, 0, 1)
                    i4.skip(self, [1])
                    self.wait(0.6)            # let the skipped gate be seen before question 5
                else:
                    vo.wait_until("is a push-triggered run a pre-receive")
                    self.play(Indicate(i5.gate, color=TURN, scale_factor=1.15), run_time=0.6)
                    vo.wait_until("or a post-receive check")
                    d5 = dot(PASS, 0.11).move_to(i5.gate.get_left() + LEFT * 0.35)
                    self.play(FadeIn(d5), run_time=0.2)
                    self.play(Transform(i5.gate.bar, i5.gate.bar.copy().rotate(
                        PI / 2.4, about_point=i5.gate.bar.get_start()).set_color(PASS)), run_time=0.3)
                    self.play(d5.animate.move_to(i5.door), run_time=0.4)
                    self.play(d5.animate.move_to(i5.server.get_center() + LEFT * 0.45),
                              Transform(i5.gate.bar, i5.gate.bar.copy().rotate(
                                  -PI / 2.4, about_point=i5.gate.bar.get_start()).set_color(S.GREY)), run_time=0.35)
                    w = ring_waves(i5.bell)
                    self.play(LaggedStart(*[Create(a_) for a_ in w], lag_ratio=0.25),
                              Indicate(i5.bell, color=ROUTE), run_time=0.7)
                    i5.add(d5, w)
                    vo.wait_until("and what makes it a gate")
                    pg = gate_glyph(0.7, 0.45, PASS).move_to(i5.door.get_left() + LEFT * 0.5)
                    assert pg.get_left()[0] > i5.gate.get_right()[0] + 0.2, (pg.get_left(), i5.gate.get_right())
                    self.play(FadeIn(pg, shift=RIGHT * 0.3), run_time=0.4)
                    self.play(Indicate(pg, color=PASS, scale_factor=1.15), run_time=0.6)
                    i5.add(pg)
                    vo.wait_until("Answers are in")
                    self.play(FadeIn(ans, shift=UP * 0.1), run_time=0.5)
                    self.play(Indicate(ans, color=INK, scale_factor=1.05), run_time=0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
