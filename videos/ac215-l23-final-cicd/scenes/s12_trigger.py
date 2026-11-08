"""S12 · Two sieves on one commit message — TRACKER C 1 (workflow › ci_cd_aws.yml · not in the
README) for the whole scene. V1 KeywordSieves (full). Lecture: 23 · slide 20 (beat 7 only).

Beats (script.md "## S12", one voiceover block each):
0. TRACKER C 1. CODE(.github/workflows/ci_cd_aws.yml: 3–9) at the top: lines 3–5 (`on: push:
   branches: [ "main" ]`) PINK on "every push to main"; line 9 (`if: contains(…, '/run-')`) YELLOW on
   "but the job runs only if"; the first sieve forms out of line 9 under the panel (PURPLE rim,
   label `if: … '/run-'`).
1. TRACKER C 1. The panel transforms into CODE(ci_cd_aws.yml: 99–100) (20 pt: line 100 is 71
   characters); line 99's step name is circled; the sieve rises and the job box with its four step
   tiles fades in under it; the 'deploy' tile is circled on "the last step"; line 100 YELLOW and the
   second, smaller sieve forms out of it over the 'deploy' tile only.
2. The panel leaves; V1 settles at full size (ECR shelf and the EC2 server fade in); a GREY
   "push to" + BLUE `main` chip with a PINK arrow feeds the ribbons. Both sieves are circled on "Two
   sieves". Ribbon 1 `update readme` slides off the first sieve; the job dims and a GREY chip "job
   skipped · nothing runs" sits on it.
3. The chip stays until "You push"; then the job comes back and ribbon 2 `fix typo /run-tests` hovers above the sieves. PONDER (8 s).
4. The card leaves. Ribbon 2 passes the first sieve (GREEN flash), a PINK dot enters the job (the
   job is circled), the build tiles are circled, three TEAL cubes land on the ECR shelf, GOLD
   cost_tag("three new images in ECR per /run- push") under the shelf; the dot stops on the second
   sieve (RED flash); the server is circled and gets a GREEN chip "old tag".
5. Ribbon 3 `/run-deploy-app` passes both sieves (two GREEN flashes); three more cubes; the dot
   enters 'deploy', a PINK route reaches the server, its three TEAL containers blink out and back
   in, and its chip turns "new tag".
6. Ribbon 4, the history's `\\run-deploy-app` (laptop/50: 5) with a GREY chip "from the opening":
   the backslash glows RED; a PINK search window `/run-` slides along the message and finds nothing
   (RED cross); the ribbon bounces off the first sieve, RED. S01's question card returns top right
   for a moment and gets a GREEN ✓.
7. LECTURE 23 · 20. The sieves leave. Slide 20's idea redrawn as a GREY card: "workflow file in
   .github/workflows", "keyword in the commit message:" + a GREY dashed `/deploy-app`; the GCP
   keyword moves out right with a GREY chip "the Google Cloud repo's keyword", and a PINK
   `/run-deploy-app` takes its place in the card; under the card the three lines `git add .`,
   `git commit -m "your message /run-deploy-app"`, `git push` (GREY) with the GREY chip "the slide's
   three commands, with a dot and this repo's keyword · you type them later".
8. LECTURE off. The sieves and the job come back (without ECR and server). Three ribbons arrive as
   one push; the first two turn GREY and leave, only the last is fed (GREEN flash); GREY chip
   "head_commit = the last commit of the push" under the sieves. Then `/RUN-DEPLOY-APP` passes
   both sieves GREEN; GREY chip "contains() ignores case". Fade; empty frame.

Deviations from SHOW: beats 0–1 keep V1 lower on the frame while a code panel holds the top (the
whole piece is shifted down 0.7, and sieve 1 a further step down in beat 0), and it rises to its
built position in beat 2. Beats 4 and 5 replay KeywordSieves.drop()'s stop-1 and stop-2 sequences
step by step in the scene (with the piece's own flash/images/_recreate), so each step lands on its
clause. Beat 8 brings back only the sieves and the job (ECR and server stay away) so that the two
chips fit under the sieves. Beat 7's rings on the dot and the keyword and its "you type them later" chip come
in a 2.3 s hold right after the block (the narration reaches "Here it's" only 2 s before it ends).
Beat 8's three-commit push is 'update readme', 'fix typo', '/run-deploy-app' (the SHOW names no
messages); only the last, '/run-deploy-app', is fed to sieve 1.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S12"]

WF = ".github/workflows/ci_cd_aws.yml"
assert excerpt(WF, 3, 5).split("\n") == ["on:", "  push:", '    branches: [ "main" ]'], excerpt(WF, 3, 5)
assert excerpt(WF, 9, 9).strip() == "if: contains(github.event.head_commit.message, '/run-')", excerpt(WF, 9, 9)
assert excerpt(WF, 99, 99).strip() == "- name: Run Deployment Container", excerpt(WF, 99, 99)
assert excerpt(WF, 100, 100).strip() == "if: contains(github.event.head_commit.message, '/run-deploy-app')"
LOG = capture("50")
assert LOG.line(5).strip() == "1 \\run-deploy-app", LOG.line(5)
assert [r for r, _ in RIBBONS] == ["update readme", "fix typo /run-tests", KEYWORD, BACKSLASH]
QUESTION = "How does a sentence deploy a server,\nand why did one character stop it?"   # S01's card
PONDER_Q = "You push 'fix typo /run-tests' to main.\nNothing, build-and-push only,\nor a full deploy?"
GIT_LINES = ("git add .", 'git commit -m "your message /run-deploy-app"', "git push")

DOWN1 = 0.7          # beats 0–1: the whole piece sits this much lower (the code panel holds the top)


def gone(scene, *mobs, run_time: float = 0.5):
    """FadeOut mobjects that are not members of a piece, and take them off the scene."""
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def dim(m, f: float):
    for s in m.family_members_with_points():
        s.set_fill(opacity=s.get_fill_opacity() * f)
        s.set_stroke(opacity=s.get_stroke_opacity() * f)
    return m


def fade_to(m, f: float, run_time: float = 0.5):
    return ApplyFunction(lambda x: dim(x, f), m, run_time=run_time)


class TwoSieves(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S12"] == 9, len(SAY)
        tr = tracker_c(1)
        k = KeywordSieves()
        k.shift(DOWN * DOWN1)                     # instantly; k.entry (a point) stays at the built place
        s1, s2 = k.sieves[0], k.sieves[1]

        # ========================================================== 0. on: push · if '/run-'
        p1 = code(WF, 3, 9)
        p1.move_to([0, 0, 0]).shift(UP * (2.75 - p1.get_top()[1]))
        bar_on = VGroup(*[line_bar(p1.code, i, ROUTE, 0.22) for i in range(3)])
        bar_if = line_bar(p1.code, 6, TURN, 0.22)
        lift = (p1.get_bottom()[1] - 0.75) - s1.rim.get_y()          # sieve 1 under the panel in beat 0
        s1.shift(UP * lift)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(p1, shift=UP * 0.2), run_time=0.7)
            self.play(Circumscribe(p1.header, color=TURN, buff=0.06), run_time=0.8)
            vo.wait_until("isn't in the README")
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("so every step on this tracker")
            self.play(Circumscribe(tr.dots, color=TURN, buff=0.06), run_time=0.9)
            vo.wait_until("on every push to main")
            self.play(FadeIn(bar_on), run_time=0.5)
            self.play(Indicate(code_span(p1.code, 2, '"main"'), color=ROUTE, scale_factor=1.15), run_time=0.6)
            vo.wait_until("but the job runs only if")
            self.play(FadeIn(bar_if), run_time=0.5)
            vo.wait_until("contains slash run dash")
            self.play(TransformFromCopy(p1.code.code_lines[6], s1.text), Create(s1.rim),
                      LaggedStart(*[Create(m) for m in s1.mesh], lag_ratio=0.05), run_time=1.1)
            self.play(Indicate(code_span(p1.code, 6, "'/run-'"), color=TURN, scale_factor=1.2), run_time=0.6)

        # ========================================================== 1. the last step's own if
        p2 = code(WF, 99, 100, font_size=20)
        p2.move_to([0, 0, 0]).shift(UP * (2.75 - p2.get_top()[1]))
        bar_dep = line_bar(p2.code, 1, TURN, 0.22)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(bar_on, bar_if)), FadeTransform(p1, p2), s1.animate.shift(DOWN * lift),
                      run_time=0.9)
            self.remove(bar_on, bar_if)
            self.play(FadeIn(VGroup(k.job, k.tiles), shift=UP * 0.2), run_time=0.6)
            vo.wait_until("And the last step")
            self.play(Circumscribe(code_span(p2.code, 0, "Run Deployment Container"), color=TURN, buff=0.05),
                      Circumscribe(k.tiles[3], color=TURN, buff=0.06), run_time=1.0)
            vo.wait_until("has its own condition")
            self.play(FadeIn(bar_dep), run_time=0.5)
            vo.wait_until("it must contain")
            self.play(TransformFromCopy(p2.code.code_lines[1], s2.text), Create(s2.rim),
                      LaggedStart(*[Create(m) for m in s2.mesh], lag_ratio=0.08), run_time=1.0)
            self.play(Indicate(code_span(p2.code, 1, "'/run-deploy-app'"), color=TURN, scale_factor=1.12),
                      run_time=0.6)

        # ========================================================== 2. two sieves; ribbon 1 slides off
        push = VGroup(label("push to", 20, ROUTE), cloud_chip("main", mono_font=True)).arrange(RIGHT, buff=0.15)
        push.move_to([0, 2.3, 0]).align_to([-6.4, 0, 0], LEFT)
        feed = arrow(push.get_right() + RIGHT * 0.1, np.array([-3.0, 2.3, 0]), ROUTE, 3, buff=0)
        skipped = grey_chip("job skipped · nothing runs", size=22)
        skipped.box.set_fill(S.BG, 0.95)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p2, bar_dep)), run_time=0.5)
            self.remove(p2, bar_dep, *p2.get_family())
            self.play(VGroup(k.job, k.tiles, s1, s2).animate.shift(UP * DOWN1), run_time=0.7)
            k.ecr.shift(UP * DOWN1)
            k.server.shift(UP * DOWN1)
            self.play(FadeIn(k.ecr, shift=UP * 0.15), FadeIn(k.server, shift=LEFT * 0.15),
                      FadeIn(push, shift=RIGHT * 0.15), GrowArrow(feed), run_time=0.7)
            k._reseat(self)
            vo.wait_until("Two sieves")
            self.play(Circumscribe(s1.rim, color=TOOL, buff=0.12), Circumscribe(s2.rim, color=TOOL, buff=0.12),
                      run_time=0.8)
            vo.wait_until("The message update readme")
            r1 = k.hover(self, RIBBONS[0][0])
            self.play(Indicate(feed, color=ROUTE), run_time=0.5)
            vo.wait_until("so the job is skipped")
            k.drop(self, r1, 0, miss="slide", run_time=1.0)
            skipped.move_to([VGroup(*k.tiles[:3]).get_x(), k.job.frame.get_y() + 0.1, 0])
            self.play(fade_to(VGroup(k.job, k.tiles), 0.35), FadeIn(skipped, scale=1.1), run_time=0.6)
            k._reseat(self)
            vo.wait_until("and nothing runs")
            self.play(Indicate(skipped.text, color=INK, scale_factor=1.08), run_time=0.7)

        # ========================================================== 3. your turn: fix typo /run-tests
        with self.voiceover(SAY[3]) as vo:
            vo.wait_until("You push")
            self.play(FadeOut(skipped), fade_to(VGroup(k.job, k.tiles), 1 / 0.35), run_time=0.5)
            self.remove(skipped, *skipped.get_family())
            k._reseat(self)
            r2 = k.hover(self, RIBBONS[1][0])
            self.play(Indicate(feed, color=ROUTE), Indicate(r2.text, color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Nothing, build and push")
            self.play(Circumscribe(s1.rim, color=TOOL, buff=0.12), run_time=0.8)
            self.play(Circumscribe(s2.rim, color=TOOL, buff=0.12), run_time=0.8)
        card = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 4. build and push only
        cost = cost_tag("three new images in ECR per /run- push")
        cost.next_to(k.ecr.frame, DOWN, buff=0.2)
        old = ok_chip("old tag", size=22).next_to(k.server.frame, DOWN, buff=0.2)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.remove(card, *card.get_family())
            vo.wait_until("It passes the first sieve")
            self.play(r2.animate.move_to([s1.rim.get_x(), s1.rim.get_y() + 0.35, 0]), run_time=0.4)
            self.play(k.flash(0, True), run_time=0.5)
            d = dot(ROUTE).move_to(r2.get_bottom())
            self.play(d.animate.move_to(k.job.text.get_right() + RIGHT * 0.3),
                      Circumscribe(k.job.frame, color=CLOUD, buff=0.05), run_time=0.8)
            vo.wait_until("so the runner builds")
            self.play(LaggedStart(*[Circumscribe(k.tiles[i], color=CLOUD, buff=0.05) for i in range(2)],
                                  lag_ratio=0.4), run_time=0.8)
            vo.wait_until("and pushes them")
            self.play(Circumscribe(k.tiles[2], color=CLOUD, buff=0.05), run_time=0.5)
            k.images(self, k.tiles[2])
            vo.wait_until("where they cost storage")
            self.play(FadeIn(cost, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, cost, COST)
            vo.wait_until("It stops at the second sieve")
            self.play(d.animate.move_to([s2.rim.get_x(), s2.rim.get_y() + 0.22, 0]), run_time=0.5)
            self.play(k.flash(1, False), d.animate.set_color(ERR), run_time=0.6)
            vo.wait_until("so the server keeps")
            self.play(FadeOut(d), FadeOut(r2), Circumscribe(k.server.frame, color=CLOUD, buff=0.05),
                      run_time=0.6)
            self.remove(d, r2)
            self.play(FadeIn(old, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(old.text, color=PASS, scale_factor=1.1), run_time=0.6)

        # ========================================================== 5. /run-deploy-app: both sieves
        new = ok_chip("new tag", size=22).move_to(old)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(cost), run_time=0.3)
            self.remove(cost)
            r3 = k.hover(self, RIBBONS[2][0], run_time=0.4)
            self.play(r3.animate.move_to([s1.rim.get_x(), s1.rim.get_y() + 0.35, 0]), run_time=0.4)
            vo.wait_until("passes both sieves")
            self.play(k.flash(0, True), run_time=0.5)
            d = dot(ROUTE).move_to(r3.get_bottom())
            self.play(d.animate.move_to([s2.rim.get_x(), s2.rim.get_y() + 0.22, 0]), run_time=0.6)
            self.play(k.flash(1, True), run_time=0.5)
            vo.wait_until("new images")
            self.play(LaggedStart(*[Circumscribe(k.tiles[i], color=CLOUD, buff=0.05) for i in range(3)],
                                  lag_ratio=0.3), run_time=0.7)
            k.images(self, k.tiles[2], run_time=0.8)
            vo.wait_until("and the containers")
            self.play(d.animate.move_to(k.tiles[3].get_top()), Circumscribe(k.tiles[3], color=CLOUD, buff=0.05),
                      run_time=0.5)
            path = route(k.tiles[3].get_right(), k.server.frame.get_left(), arc=-0.3)
            self.play(GrowArrow(path), run_time=0.5)
            k._recreate(self, run_time=1.0)
            self.play(Transform(old, new), run_time=0.5)
            self.play(FadeOut(VGroup(d, r3, path)), run_time=0.4)
            self.remove(d, r3, path)

        # ========================================================== 6. the commit from the opening
        r4 = ribbon(BACKSLASH, ROUTE).move_to(k.entry)
        src = grey_chip("from the opening", size=20).next_to(r4, RIGHT, buff=0.3)
        n = len(BACKSLASH)
        win = SurroundingRectangle(VGroup(*r4.text[0:5]), color=ROUTE, buff=0.05, stroke_width=3)
        win_t = mono(JOB_KEY, 20, ROUTE).next_to(r4, DOWN, buff=0.08).set_x(win.get_x())
        search = VGroup(win, win_t)
        span = r4.text[n - 5].get_left()[0] - r4.text[0].get_left()[0]
        miss = cross_mark(0.3, ERR).next_to(r4, RIGHT, buff=0.3)
        corner = question_card(QUESTION, size=20)
        corner.move_to([6.6 - corner.width / 2, 3.6 - corner.height / 2, 0])
        tick = check_mark(0.42, PASS).next_to(corner, DOWN, buff=0.15).align_to(corner, RIGHT).shift(LEFT * 0.2)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(old), run_time=0.3)
            self.remove(old, *old.get_family())
            self.play(FadeIn(r4, shift=DOWN * 0.3), FadeIn(src, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("Its slash is a backslash")
            self.play(r4.text[0].animate.set_color(ERR), run_time=0.3)
            self.play(Indicate(r4.text[0], color=ERR, scale_factor=1.8), run_time=0.8)
            vo.wait_until("The text slash run dash")
            self.play(FadeOut(src), FadeIn(search), run_time=0.4)
            self.remove(src)
            self.play(search.animate.shift(RIGHT * span), run_time=1.4, rate_func=linear)
            self.play(win.animate.set_color(ERR), win_t.animate.set_color(ERR), FadeIn(miss, scale=1.3), run_time=0.4)
            vo.wait_until("so it bounces off")
            self.play(FadeOut(search), FadeOut(miss), run_time=0.3)
            self.remove(search, miss)
            k.drop(self, r4, 0, miss="bounce", run_time=1.0)
            vo.wait_until("That's the one character")
            self.play(FadeIn(corner, shift=DOWN * 0.2), run_time=0.5)
            self.play(Create(tick), run_time=0.4)
            self.play(Indicate(corner.text, color=TURN, scale_factor=1.04), run_time=0.6)

        # ========================================================== 7. slide 20: the same, in GCP words
        lr = lref("20")
        r_wf = VGroup(label("workflow file in", 22, INK), mono(".github/workflows", 22, INK)).arrange(RIGHT, buff=0.2)
        r_kw_l = label("keyword in the commit message:", 22, INK)
        gcp = dashed_chip(SLIDES_KEYWORD, PAST, 22, mono_font=True)
        aws = route_chip(KEYWORD, size=22)
        r_kw = VGroup(r_kw_l, gcp).arrange(RIGHT, buff=0.25)
        rows = VGroup(r_wf, r_kw).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        cw = r_kw_l.width + 0.25 + aws.width + 0.8
        cframe = box(cw, rows.height + 0.7, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        rows.move_to(cframe).align_to(cframe, LEFT).shift(RIGHT * 0.4)
        slide = VGroup(cframe, rows).move_to([0, 0, 0])
        slide.shift(np.array([-6.3 - slide.get_left()[0], 2.35 - slide.get_top()[1], 0]))
        aws.move_to(gcp).align_to(gcp, LEFT)
        gcp_to = gcp.copy().next_to(cframe, RIGHT, buff=0.45).set_y(gcp.get_y())
        gnote = grey_chip("the Google Cloud repo's keyword", size=20)
        gnote.move_to([gcp_to.get_x(), cframe.get_bottom()[1] - 0.45, 0])
        if gnote.get_right()[0] > 6.5:
            gnote.shift(LEFT * (gnote.get_right()[0] - 6.5))
        gl = VGroup(*[mono(s, 22, S.GREY) for s in GIT_LINES]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        gl.next_to(cframe, DOWN, buff=0.8).align_to(cframe, LEFT).shift(RIGHT * 0.4)
        gnote2 = grey_chip("the slide's three commands, with a dot and this repo's keyword · you type them later", size=20)
        gnote2.next_to(gl, DOWN, buff=0.35).align_to(gl, LEFT)
        dot_hl = ring(gl[0][-1], TURN, buff=0.06)
        kw_hl = ring(gl[1][-1 - len(KEYWORD):-1], ROUTE, buff=0.05)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(corner), FadeOut(tick), FadeOut(push), FadeOut(feed), FadeOut(k), run_time=0.6)
            self.remove(corner, tick, push, feed, k, *corner.get_family(), *k.get_family())
            self.play(FadeIn(lr), FadeIn(cframe, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("a workflow file")
            self.play(FadeIn(r_wf, shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(r_wf[1], color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and a keyword")
            self.play(FadeIn(r_kw, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("Its keyword")
            self.play(Indicate(gcp.text, color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("belongs to the Google Cloud repo")
            self.play(Transform(gcp, gcp_to), run_time=0.7)
            self.play(FadeIn(gnote, shift=UP * 0.12), run_time=0.5)
            vo.wait_until("Here it's")
            self.play(TransformFromCopy(gcp, aws), run_time=0.6)
            self.play(Indicate(aws.text, color=ROUTE, scale_factor=1.12),
                      LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in gl], lag_ratio=0.3), run_time=0.9)
        # a short hold after the block: the slide's commands, written out (no narration of their own)
        self.play(Create(dot_hl), Create(kw_hl), FadeIn(gnote2, shift=UP * 0.1), run_time=0.6)
        self.play(Indicate(gl[0][-1], color=TURN, scale_factor=1.6), run_time=0.7)
        self.wait(1.0)
        lecture = VGroup(slide, gcp, gnote, aws, gl, gnote2, dot_hl, kw_hl)

        # ========================================================== 8. head_commit; ignores case
        core = VGroup(k.job, k.tiles, s1, s2)
        msgs = ("update readme", "fix typo", KEYWORD)
        trio = VGroup(*[ribbon(m, ROUTE) for m in msgs]).arrange(RIGHT, buff=0.25)
        trio.move_to([0, 2.3, 0]).align_to([-2.85, 0, 0], LEFT)
        c1 = grey_chip("head_commit = the last commit of the push", size=22)
        c1.move_to([k.job.frame.get_x(), k.job.frame.get_bottom()[1] - 0.5, 0])
        c2 = grey_chip("contains() ignores case", size=22).next_to(c1, DOWN, buff=0.25)
        caps = ribbon(KEYWORD.upper(), ROUTE).move_to(k.entry)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(lr), FadeOut(lecture), run_time=0.6)
            self.remove(lr, lecture, *lecture.get_family())
            self.play(FadeIn(core), FadeIn(push), GrowArrow(feed), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.3) for x in trio], lag_ratio=0.25), run_time=0.9)
            vo.wait_until("so three commits")
            self.play(fade_to(VGroup(trio[0], trio[1]), 0.35), Indicate(trio[2].text, color=INK, scale_factor=1.1),
                      run_time=0.6)
            self.play(FadeIn(c1, shift=UP * 0.15), run_time=0.5)
            self.play(FadeOut(VGroup(trio[0], trio[1])), trio[2].animate.move_to(k.entry), run_time=0.6)
            self.play(trio[2].animate.move_to([s1.rim.get_x(), s1.rim.get_y() + 0.35, 0]), run_time=0.4)
            self.play(k.flash(0, True), run_time=0.5)
            self.play(FadeOut(trio[2]), run_time=0.3)
            self.remove(trio)
            vo.wait_until("And the match ignores case")
            self.play(FadeIn(caps, shift=DOWN * 0.3), FadeIn(c2, shift=UP * 0.15), run_time=0.5)
            self.play(caps.animate.move_to([s1.rim.get_x(), s1.rim.get_y() + 0.35, 0]), run_time=0.4)
            self.play(k.flash(0, True), k.flash(1, True), caps.frame.animate.set_stroke(PASS), run_time=0.6)

        rest = VGroup(core, push, feed, c1, c2, caps)
        self.play(FadeOut(rest), FadeOut(tr), run_time=0.6)
        self.remove(rest, tr, *rest.get_family())
        self.wait(0.3)
