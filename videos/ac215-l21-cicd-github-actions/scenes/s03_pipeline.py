"""S03 · The CI loop and the workflow file (AC215 L21). No tracker until beat 4 (README Part 5,
step 1). Lecture: 21 · slides 22, 17, 21, 25–27 (beats 0–3 only).

Beats (script.md "## S03", one voiceover block each):
0. lecture_ref 22. A GREY code box (left) and three '>_' script glyphs joined by GREY arrows. A
   GREEN commit dot lands on the box and the glyphs light YELLOW in sequence by themselves ("run
   automatically"); on "whenever the code changes" a second dot lands and they run again. Four
   GREEN chips dock under the glyph row, one per phrase: integrate continuously, test
   automatically, enforce coding standards, static code analysis.
1. lecture_ref 17. The chips fade. Three icons fly down out of the glyph row, one per phrase, each
   with a GREY caption: a short arrow (faster releases), a GREEN check mark (better code), a pair of
   people (easier teamwork); then a GREY dashed chip "+ machine learning: at the end" pulses once.
2. lecture_ref 21. The picture clears. V2 CiLoop drawn open, piece by piece: Developers and the
   PINK Commits arrow into Codebase; Build, Test in the GREY dashed row; the dashed PINK return
   lines, the Notifications bar and the dashed way back. On "For now" a YELLOW "?" on the returns.
3. lecture_ref 25–27. The loop shrinks (text-free) into the top-left corner. V2 PipelineStrip at
   full size: five WHITE-outlined boxes appear with a GREY chip "built with GitHub Actions"; each
   box pulses YELLOW as it is named and slide 27's purpose writes on under it.
4. Lecture tag off. The strip shrinks to the thin Part 2 row and slides off the top; the corner
   loop goes. TRACKER P5 1 appears with README(277–283) (lines 277, 279, 283); "Python 3.11 (same
   as production)" turns YELLOW; a GREY erratum tag under the card: "erratum · no production yet ·
   read: the same image you would deploy".
5. TRACKER P5 1 · extra. The card shrinks into the tracker caption. A full-width laptop terminal
   (6 rows, GREY 'extra' tag on its bar) types `ls -la .github/workflows/` and prints laptop/04
   lines 2–5; `ci.yml` turns GREEN. The terminal shrinks to a 3-row strip (the command and the
   ci.yml row) and a file tree draws above it: cheese-app-ci-cd/ (GREEN, "repository root") →
   .github/ → workflows/ → ci.yml (GREEN); "GitHub looks only there" rings .github/workflows/; a GREY
   dashed ghost "my-project/subfolder/.github/workflows/" with a RED ✗ "never runs", and the GREY
   chip "fix: move to the root .github/workflows/ + defaults: run: working-directory: · study guide".
6. TRACKER P5 1. The strip and the tree go. CODE(ci.yml 5–11): line 5 YELLOW on "a name", lines
   7–11 PINK on "The key named on". Transform to CODE(ci.yml 13–20): lines 13 and 15 YELLOW on
   "Under jobs", line 17 BLUE on "its own machine".
7. V4 WorkflowTree (S03 form): the panel's `jobs:` line becomes the column of six BLUE job ids,
   the PINK root "on: push · pull_request" and "workflow: CI Pipeline" fade in above it. The build
   job opens into its five steps (puzzle = uses:, '>_' = run:), the other jobs dim. The run steps
   pulse YELLOW, the uses steps PURPLE; on "like actions checkout" the one-line panel ci.yml:20
   (`uses: actions/checkout@v4`) appears under the steps and Checkout code is ringed. Each layer
   pulses on "Event, workflow, jobs, steps". Everything fades; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.devops import file_tree
from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ the real sources (checked)
CAP04 = capture("laptop/04")
assert CAP04.cmd_lines == ["ls -la .github/workflows/"], CAP04.cmd_lines
LS_OUT = CAP04.at((2, 5))
assert LS_OUT[0] == "total 16" and LS_OUT[3].endswith(" ci.yml") and CAP04.exit == 0, LS_OUT
CI = ".github/workflows/ci.yml"
assert excerpt(CI, 5, 5).strip() == "name: CI Pipeline"
assert excerpt(CI, 7, 7).strip() == "on:" and excerpt(CI, 11, 11).strip() == "branches: [main, develop]"
assert excerpt(CI, 13, 13).strip() == "jobs:" and excerpt(CI, 15, 15).strip() == "build:"
assert excerpt(CI, 17, 17).strip() == "runs-on: ubuntu-latest"
assert excerpt(CI, 20, 20).strip() == "uses: actions/checkout@v4"
assert "Python 3.11 (same as production)" in readme(279)

CI_PHRASES = (("integrate continuously", "They integrate changes continuously"),
              ("test automatically", "test automatically"),
              ("enforce coding standards", "enforce coding standards"),
              ("static code analysis", "and run static analysis"))
PAYOFF_CUES = ("faster releases", "better code", "and easier teamwork")
PAYOFF_TEXT = ("faster releases", "better code", "easier teamwork")
STRIP_CUES = ("A commit triggers it", "the container is built", "Black and Flake8 check the code",
              "the tests run", "and a summary reports")
GLYPH_Y = 1.3


def code_box() -> VGroup:
    """The GREY 'code' box of beat 0: a box with four short code strokes and a caption."""
    fr = box(2.2, 1.5, LAPTOP, fill_opacity=0.08)
    strokes = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2, color=S.GREY, stroke_width=4)
                       for w in (1.3, 0.9, 1.5, 1.1)]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    strokes.move_to(fr)
    cap = label("code", 22, LAPTOP).next_to(fr, DOWN, buff=0.15)
    g = VGroup(fr, strokes, cap)
    g.frame, g.cap = fr, cap
    return g


def skeleton(m) -> VGroup:
    """A copy of `m` with every Text taken out (so it can shrink without small text)."""
    c = m.copy()

    def strip(g):
        for s in list(g.submobjects):
            if isinstance(s, (Text, MarkupText)):
                g.remove(s)
            else:
                strip(s)

    strip(c)
    return c


def texts_of(m) -> list:
    return [s for s in m.get_family() if isinstance(s, (Text, MarkupText))]


def text_span(t: Text, phrase: str) -> VGroup:
    """The glyphs of `phrase` in a Text (Text drops spaces from its glyphs and its .text)."""
    p = phrase.replace(" ", "")
    i = t.text.find(p)
    if i < 0:
        raise ValueError(f"{phrase!r} not in {t.text!r}")
    return VGroup(*t[i:i + len(p)])


class CiPipeline(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 8, len(SAY)

        # ========================================================== 0. scripts that run by themselves
        ref = lref("22")
        cbox = code_box().move_to([-4.6, GLYPH_Y - 0.2, 0])
        cbox.shift(UP * (GLYPH_Y - cbox.frame.get_center()[1]))
        glyphs = VGroup(*[script_glyph(0.62) for _ in range(3)]).arrange(RIGHT, buff=1.05)
        glyphs.move_to([0.9, GLYPH_Y, 0])
        links = VGroup(arrow(cbox.frame, glyphs[0]), arrow(glyphs[0], glyphs[1]), arrow(glyphs[1], glyphs[2]))
        chips = [ok_chip(s, size=22) for s, _ in CI_PHRASES]
        row1 = VGroup(chips[0], chips[1]).arrange(RIGHT, buff=0.35)
        row2 = VGroup(chips[2], chips[3]).arrange(RIGHT, buff=0.35)
        grid = VGroup(row1, row2).arrange(DOWN, buff=0.3).move_to([0.9, -0.55, 0])
        commits = []

        def run_once():
            d = dot(PASS).move_to([cbox.frame.get_left()[0] + 0.45 + 0.4 * len(commits), 3.0, 0])
            land = [d.get_center()[0], cbox.frame.get_top()[1] + 0.02, 0]
            self.play(FadeIn(d, shift=DOWN * 0.2), run_time=0.2)
            self.play(d.animate.move_to(land), run_time=0.35)
            self.play(Indicate(cbox.frame, color=PASS, scale_factor=1.04), run_time=0.35)
            commits.append(d)
            for ln, g in zip(links, glyphs):
                self.play(ShowPassingFlash(ln.copy().set_stroke(TURN, 6), time_width=0.6),
                          Indicate(g, color=TURN, scale_factor=1.15), run_time=0.4)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(cbox, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("as a series of scripts")
            self.play(LaggedStart(*[FadeIn(g, shift=UP * 0.2) for g in glyphs], lag_ratio=0.25),
                      LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.25), run_time=0.9)
            vo.wait_until("that run automatically")
            run_once()
            vo.wait_until("whenever the code changes")
            run_once()
            for c, (_, cue) in zip(chips, CI_PHRASES):
                vo.wait_until(cue)
                start = c.copy().move_to([c.get_center()[0], -3.2, 0]).set_opacity(0)
                self.play(Transform(start, c), run_time=0.45)
                self.remove(start)
                self.add(c)
                self.play(Indicate(glyphs, color=PASS, scale_factor=1.06), run_time=0.35)

        # ========================================================== 1. what it buys
        ref2 = lref("17")
        icon_y = -0.75
        icons = [Arrow(LEFT * 0.55, RIGHT * 0.55, buff=0, color=INK, stroke_width=6, tip_length=0.25),
                 check_mark(0.6, PASS, stroke=6),
                 VGroup(person_icon(LAPTOP, 0.6), person_icon(LAPTOP, 0.6)).arrange(RIGHT, buff=0.12)]
        xs = (-3.3, 0.9, 5.0)
        caps = []
        for ic, x, s in zip(icons, xs, PAYOFF_TEXT):
            ic.move_to([x, icon_y, 0])
            caps.append(label(s, 22, S.GREY).next_to(ic, DOWN, buff=0.25).set_x(x))
        ml = dashed_chip("+ machine learning: at the end", size=22).move_to([0.9, -2.55, 0])
        with self.voiceover(SAY[1]) as vo:
            self.play(ReplacementTransform(ref, ref2), *[FadeOut(c) for c in chips], run_time=0.5)
            self.remove(*chips)
            for g, ic, cp, cue in zip(glyphs, icons, caps, PAYOFF_CUES):
                vo.wait_until(cue)
                tgt = ic.get_center().copy()
                ic.move_to(g)
                self.play(ic.animate.move_to(tgt), FadeIn(ic), Indicate(g, color=TURN, scale_factor=1.1),
                          run_time=0.55)
                self.play(FadeIn(cp, shift=UP * 0.15), run_time=0.3)
            vo.wait_until("Machine learning adds a twist")
            self.play(FadeIn(ml, shift=UP * 0.2), run_time=0.4)
            flash_tag(self, ml, INK)

        # ========================================================== 2. slide 21's loop, drawn open
        ref3 = lref("21")
        loop = CiLoop().shift(DOWN * 0.3)
        b = loop.boxes
        beat01 = VGroup(cbox, glyphs, links, *commits, *icons, *caps, ml)
        with self.voiceover(SAY[2]) as vo:
            self.play(ReplacementTransform(ref2, ref3), FadeOut(beat01), run_time=0.6)
            self.remove(beat01, *beat01.get_family())
            self.play(Create(loop.row_frame), run_time=0.6)
            vo.wait_until("Developers commit to the codebase")
            self.play(FadeIn(loop.devs, shift=UP * 0.2), run_time=0.4)
            self.play(Create(loop.commits[0]), GrowArrow(loop.commits[1]), FadeIn(loop.commits[2]),
                      FadeIn(b["codebase"], shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("the codebase is built")
            self.play(GrowArrow(loop.row_arrows[0]), FadeIn(b["build"], shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("then tested")
            self.play(GrowArrow(loop.row_arrows[1]), FadeIn(b["test"], shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("and notifications flow back")
            self.play(Create(loop.returns), FadeIn(loop.notify, shift=UP * 0.15), run_time=0.7)
            self.play(Create(loop.back), loop.light("devs", ROUTE), run_time=0.7)
            self.add(loop)
            vo.wait_until("For now")
            loop.question(self)
            self.play(Indicate(loop.q, color=TURN, scale_factor=1.3), run_time=0.6)

        # ========================================================== 3. slide 26's five boxes
        ref4 = lref("25–27")
        fs = PipelineStrip(full=True).move_to([0, 0.75, 0])
        purposes = fs.purposes(size=20)
        gha = grey_chip("built with GitHub Actions", size=22).move_to([0, -1.6, 0])
        skel = skeleton(loop)
        words = VGroup(*[t.copy() for t in texts_of(loop)])
        with self.voiceover(SAY[3]) as vo:
            self.remove(loop, *loop.get_family())
            self.add(skel, words)
            mini_w = skel.width * 0.26
            corner = [-6.45 + mini_w / 2, 3.45 - skel.height * 0.26 / 2, 0]
            self.play(ReplacementTransform(ref3, ref4), FadeOut(words, run_time=0.3),
                      skel.animate.scale(0.26).move_to(corner), run_time=0.8)
            self.remove(words)
            vo.wait_until("has five stages")
            self.play(LaggedStart(*[FadeIn(bx, shift=RIGHT * 0.15) for bx in fs.boxes], lag_ratio=0.15),
                      LaggedStart(*[GrowArrow(a) for a in fs.arrows], lag_ratio=0.15), run_time=1.0)
            self.add(fs)
            self.play(FadeIn(gha, shift=UP * 0.15), run_time=0.4)
            for bx, pu, cue in zip(fs.boxes, purposes, STRIP_CUES):
                vo.wait_until(cue)
                self.play(Indicate(bx, color=TURN, scale_factor=1.08), Write(pu), run_time=0.6)

        # ========================================================== 4. README Part 5
        tr = tracker_p5(1)
        thin = pipeline_strip()
        card = readme_panel(277, 283, lines=(277, 279, 283)).move_to([0, 0.75, 0])
        phrase = text_span(card.rows[279][0], "Python 3.11 (same as production)")
        err = erratum_tag("erratum · no production yet · read: the same image you would deploy")
        err.next_to(card, DOWN, buff=0.3).align_to(card, RIGHT)
        with self.voiceover(SAY[4]) as vo:
            self.play(Transform(fs, thin), FadeOut(purposes), FadeOut(gha), FadeOut(skel), FadeOut(ref4),
                      run_time=0.7)
            self.play(FadeOut(fs, shift=UP * 0.6), run_time=0.4)
            self.remove(fs, purposes, gha, skel, ref4)
            vo.wait_until("Now the README")
            self.play(FadeIn(tr, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(card, shift=UP * 0.2), Indicate(tr.caption, color=TURN, scale_factor=1.05),
                      run_time=0.6)
            vo.wait_until("It says all CI tests")
            self.play(Circumscribe(card.rows[279], color=INK, buff=0.08), run_time=0.8)
            vo.wait_until("using Python 3.11")
            self.play(phrase.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(phrase, color=TURN, scale_factor=1.06), run_time=0.5)
            vo.wait_until("This repo has no production yet")
            self.play(FadeIn(err, shift=UP * 0.15), run_time=0.4)
            flash_tag(self, err)
            vo.wait_until("take it as the same image")
            self.play(Indicate(phrase, color=TURN, scale_factor=1.06), run_time=0.6)

        # ========================================================== 5. extra: the workflows folder
        t = term(rows=6)
        bar_tag = on_bar(t, extra_row())
        tree = file_tree(["cheese-app-ci-cd/", "  .github/", "    workflows/", "      ci.yml"], size=22,
                         colors={"cheese-app-ci-cd/": OWN, ".github/": INK, "workflows/": INK, "ci.yml": OWN},
                         notes={"cheese-app-ci-cd/": "repository root"})
        tree.shift(np.array([-5.9 - tree.get_left()[0], 2.45 - tree.get_top()[1], 0]))
        ghost = dashed_chip("my-project/subfolder/.github/workflows/", size=22, mono_font=True)
        ghost.next_to(tree, DOWN, buff=0.4).align_to(tree, LEFT)
        never = VGroup(cross_mark(0.3, ERR), label("never runs", 22, ERR)).arrange(RIGHT, buff=0.15)
        never.next_to(ghost, RIGHT, buff=0.35)
        fix = grey_chip("fix: move to the root .github/workflows/ + defaults: run: working-directory: · study guide")
        fix.next_to(ghost, DOWN, buff=0.3).align_to(tree, LEFT)
        gh_dirs = VGroup(tree.row(".github/"), tree.row("workflows/"))
        with self.voiceover(SAY[5]) as vo:
            cap_copy = tr.caption.copy()
            self.play(ReplacementTransform(VGroup(card, err), cap_copy), run_time=0.6)
            self.remove(cap_copy, card, err)
            self.play(track(tr, 1, True), FadeIn(t, shift=UP * 0.2), FadeIn(bar_tag, shift=UP * 0.2),
                      run_time=0.6)
            vo.wait_until("list the workflows folder")
            cmd = type_capture(self, t, CAP04)[0]
            rows = out(self, t, LS_OUT)
            ci_row = rows[-1]
            vo.wait_until("One file")
            name = substring(ci_row, "ci.yml")
            self.play(name.animate.set_color(OWN), run_time=0.3)
            self.play(Indicate(name, color=OWN, scale_factor=1.15), run_time=0.5)
            vo.wait_until("in dot github")
            dy = STRIP_TOP - t.box.get_top()[1]
            resize(self, t, 3, keep=[cmd, ci_row], extra=[bar_tag.animate.shift(UP * dy)])
            self.play(FadeIn(tree.rows[0], shift=RIGHT * 0.15), run_time=0.35)
            self.play(FadeIn(tree.rows[1], shift=RIGHT * 0.15), run_time=0.35)
            vo.wait_until("workflows, at the root")
            self.play(FadeIn(tree.rows[2], shift=RIGHT * 0.15), run_time=0.35)
            self.play(TransformFromCopy(name, tree.rows[3]), run_time=0.6)
            vo.wait_until("at the root of the repository")
            self.play(Indicate(tree.rows[0], color=OWN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("GitHub looks only there")
            self.play(Circumscribe(gh_dirs, color=TURN, buff=0.1), run_time=0.8)
            vo.wait_until("a workflow in a subfolder never runs")
            self.play(FadeIn(ghost, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(never, shift=LEFT * 0.15), run_time=0.4)
            self.play(FadeIn(fix, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 6. name, on, jobs
        p1 = code(CI, 5, 11).move_to([0, 0.1, 0])
        p2 = code(CI, 13, 20).move_to([0, 0.1, 0])
        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(t, bar_tag, tree, ghost, never, fix)
            self.play(FadeOut(gone), track(tr, 1, False), run_time=0.6)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("The file gives the workflow a name")
            bar_name = line_bar(p1.code, 0, TURN)
            self.play(FadeIn(bar_name), Indicate(p1.code.code_lines[0], color=TURN, scale_factor=1.05),
                      run_time=0.6)
            vo.wait_until("The key named on")
            bars_on = VGroup(*[line_bar(p1.code, k, ROUTE) for k in range(2, 7)])
            self.play(LaggedStart(*[FadeIn(bb) for bb in bars_on], lag_ratio=0.15), run_time=0.7)
            self.play(Indicate(p1.code.code_lines[2], color=ROUTE, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Under jobs")
            self.play(FadeOut(bar_name), FadeOut(bars_on), run_time=0.25)
            self.remove(bar_name, bars_on)
            self.play(ReplacementTransform(p1, p2), run_time=0.7)
            bars_jobs = VGroup(line_bar(p2.code, 0, TURN), line_bar(p2.code, 2, TURN))
            self.play(FadeIn(bars_jobs), run_time=0.4)
            vo.wait_until("each job gets its own machine")
            bar_runs = line_bar(p2.code, 4, GITHUB, opacity=0.25)
            self.play(FadeIn(bar_runs), Indicate(p2.code.code_lines[4], color=GITHUB, scale_factor=1.05),
                      run_time=0.6)

        # ========================================================== 7. event, workflow, jobs, steps
        wt = WorkflowTree()
        jobs_line = p2.code.code_lines[0]
        chk = code_strip(CI, 20)
        with self.voiceover(SAY[7]) as vo:
            rest = VGroup(p2, bars_jobs, bar_runs)
            self.play(ReplacementTransform(jobs_line.copy(), wt.col), FadeOut(rest), run_time=0.8)
            self.remove(rest, *rest.get_family())
            self.play(FadeIn(wt.root, shift=DOWN * 0.2), FadeIn(wt.wf, shift=DOWN * 0.2), Create(wt.links),
                      run_time=0.6)
            self.add(wt)
            vo.wait_until("Inside a job")
            self.play(Indicate(wt.jobs["build"], color=TURN, scale_factor=1.08), run_time=0.4)
            wt.open_job(self, per=0.3)
            wt.dim_others(self)
            vo.wait_until("A step is either a shell script")
            runs = VGroup(*[r for r in wt.steps if r.kind == "run"])
            uses = VGroup(*[r for r in wt.steps if r.kind == "uses"])
            self.play(Indicate(runs, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("or a reusable action")
            self.play(Indicate(uses, color=TOOL, scale_factor=1.06), run_time=0.7)
            vo.wait_until("like actions checkout")
            chk.next_to(wt.steps, DOWN, buff=0.4).align_to(wt.steps, LEFT)
            self.play(FadeIn(chk, shift=UP * 0.15), Circumscribe(wt.steps[0], color=TOOL, buff=0.08),
                      run_time=0.8)
            vo.wait_until("which copies your repository")
            self.play(Indicate(wt.steps[0], color=TOOL, scale_factor=1.06), run_time=0.6)
            for layer, cue in (("event", "Event, workflow"), ("workflow", "workflow, jobs"),
                               ("jobs", "jobs, steps"), ("steps", "steps: that is")):
                vo.wait_until(cue)
                self.play(wt.pulse(layer), run_time=0.45)
                self.add(wt)

        everything = VGroup(wt, chk, tr)
        self.play(FadeOut(everything), run_time=0.6)
        self.remove(everything, *everything.get_family())
        self.wait(0.3)
