"""S11 · CI, CD, and who presses release — no tracker (lecture scene). V8 ReleaseLoop and
ReleaseToggle; the lecture's pictures redrawn in series colours (slides 7, 36, 8–10, 11–12, 13–15,
16–18). Part 2 starts here.

Beats (script.md "## S11"; one voiceover block each):
0. LECTURE 23 · 7. V8 ReleaseLoop drawn piece by piece: Codebase → Build → Test → Deploy → Monitor;
   "Developers" bottom left with the PINK "Commits" arrow up into Codebase; a PINK commit dot rides
   it and runs Build, Test (bracket "CI"), Deploy, Monitor (bracket "CD"); the dashed PINK
   notification lines drop from every box after Codebase into the GREY "Notifications" bar.
1. LECTURE 23 · 36. The same loop: Release slides in between Test and Deploy (its own notification
   line comes with the re-layout); Release is lit YELLOW.
2. LECTURE 23 · 8–10. The loop fades. Slide 10's idea redrawn: three GREY developers → "Shared
   Repository" → the pipe "Automated Quality Checks" whose three tiles fill in one per phrase
   ("automated tests", "coding standards · style, consistency", "static analysis · defects,
   vulnerabilities, without running the code") → "Functional Codebase" with a GREEN ✓; a code card
   rides the whole way; GREY chip "L09 · L21".
3. LECTURE 23 · 11–12. Slide 12's toggle: the conveyor of code cards; the RED RELEASE button with
   the GREY hand ("continuous delivery"), the hand presses; then the button swaps for the GREEN
   "auto" ring ("continuous deployment") and the cards stream through.
4. LECTURE 23 · 13–15. Two GREY cards, "CI for ML" (+ data quality, + model performance,
   expensive) and "CD for ML" (release only within a tolerance, challenge: data drift), rows in one
   per phrase; a GREY dashed chip "this repo: an app, not a model · L15 was the model".
5. The cards leave; V8 comes back. This repo's version: Codebase, Build, Release and Deploy turn
   BLUE; Release chip "tagged images land in ECR"; Test a GREY dashed outline + dashed chip "L21";
   CODE(.github/workflows/ci_cd_aws.yml: 1–2) at the bottom, "Continuous Integration" highlighted,
   erratum chip "runs no test: the CD half" on the panel's top edge; the CD bracket flashes; Monitor chip
   "the run's color + your own check".
6. LECTURE 23 · 16–18. A row of six blank GREY service tiles (no logos), one turns PURPLE "GitHub
   Actions"; a BLUE runner box sends two arrows, "build it" and "run it", to the TEAL crate
   `cheese-app-deployment`; a PINK commit dot reaches the runner; GREY caption "thin YAML · thick
   container", with a GREEN `ci_cd_aws.yml` chip under the runner and a GREEN "the playbooks you
   ran" chip under the crate. Fade; empty frame.

Deviations from SHOW: block 2 "the loop shrinks to the top" — the loop fades instead (its text is
20 pt; shrinking would put it under 20 pt) and comes back in block 5 ("V8 grows back"). Block 5
draws this_repo() step by step (one change per phrase) with ReleaseLoop's own box and chip helpers
instead of the single this_repo() call, and places its three chips itself on opaque backings
(ReleaseLoop.chip's levels made the Release chip touch the L21 and Monitor chips, with the dashed
lines running through the text). The code panel is set at 20 pt so it fits under the loop;
the erratum chip sits on the panel's top edge, right of its header (no room beside its
54-character line 1, nor under the panel).
Critic pass: the slide-10 code card rides inside the pipe at the left of each tile (it sat on the
pipe's border before); Test turns dashed by a cross-fade (Transform scrambled the dashes mid-way).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S11"]

WF = ".github/workflows/ci_cd_aws.yml"
assert excerpt(WF, 1, 1).strip() == "name: Continuous Integration and Continuous Deployment"
assert "submitted a CI CD Action" in excerpt(WF, 2, 2)

LOOP_UP = 0.5          # the loop sits 0.5 higher than built, to leave room for the code panel


def settle(scene, piece):
    """Members of a piece that an animation brought onto the scene go back under the piece."""
    piece._reseat(scene)


def drop_all(scene, *mobs, run_time: float = 0.5):
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def ref_swap(scene, old, slides: str, run_time: float = 0.4):
    new = lref(slides)
    if old is None:
        scene.play(FadeIn(new), run_time=run_time)
    else:
        scene.play(FadeOut(old), FadeIn(new), run_time=run_time)
        scene.remove(old)
    return new


def code_card(w: float = 0.62, h: float = 0.48, color=INK) -> VGroup:
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.06, stroke_color=color,
                          stroke_width=2).set_fill(PANEL, 1)
    ls = VGroup(*[Line(LEFT * w * 0.3, RIGHT * w * 0.3, color=S.GREY, stroke_width=2) for _ in range(3)])
    ls.arrange(DOWN, buff=h * 0.15).move_to(fr)
    return VGroup(fr, ls)


def text_card(head: str, rows, card_w: float, color=S.GREY) -> VGroup:
    """A GREY card: a 22 pt head and 20 pt rows ((text, colour) or text). .frame .head .rows"""
    hd = label(head, 22, INK)
    rs = VGroup(*[label(r, 20, S.GREY) if isinstance(r, str) else label(r[0], 20, r[1]) for r in rows])
    rs.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    inner = VGroup(hd, rs).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
    fr = box(card_w, inner.height + 0.6, color, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.32)
    g = VGroup(fr, hd, rs)
    g.frame, g.head, g.rows = fr, hd, rs
    return g


def loop_chip(lp, key: str, text: str, color, y: float, dashed: bool = False, x: float | None = None) -> VGroup:
    """A chip under a loop box on an opaque backing (the dashed notification lines pass behind it),
    centred under the box (or at x), kept inside x <= 6.5."""
    c = dashed_chip(text, color) if dashed else chip(text, color, size=20)
    back = RoundedRectangle(width=c.width, height=c.height, corner_radius=c.height / 2.6, stroke_width=0)
    back.set_fill(S.BG, 1).move_to(c)
    g = VGroup(back, c).move_to([lp.boxes[key].get_x() if x is None else x, y, 0])
    if g.get_right()[0] > 6.5:
        g.shift(LEFT * (g.get_right()[0] - 6.5))
    return g


class WhoPressesRelease(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S11"] == 7, len(SAY)

        # ========================================================== 0. slide 7: the loop
        lp = ReleaseLoop()
        lp.shift(UP * LOOP_UP)
        keys5 = ["codebase", "build", "test", "deploy", "monitor"]
        bx = lp.boxes
        dc = lp.decor
        with self.voiceover(SAY[0]) as vo:
            ref = ref_swap(self, None, "7")
            self.play(LaggedStart(*[FadeIn(bx[k], shift=UP * 0.1) for k in keys5], lag_ratio=0.15), run_time=1.0)
            self.play(LaggedStart(*[GrowArrow(a) for a in dc.arrows], lag_ratio=0.2), run_time=0.8)
            vo.wait_until("Developers commit")
            self.play(FadeIn(lp.devs, shift=UP * 0.1), run_time=0.5)
            self.play(Create(dc.cpath), FadeIn(dc[6]), FadeIn(dc[7]), run_time=0.8)
            d = dot(ROUTE).move_to(dc.cpath.get_start())
            self.play(FadeIn(d), run_time=0.2)
            self.play(MoveAlongPath(d, dc.cpath.copy()), run_time=0.7)
            self.play(d.animate.move_to(bx["codebase"].get_top() + UP * 0.14), Indicate(bx["codebase"].text, color=ROUTE),
                      run_time=0.4)
            vo.wait_until("It is built")
            for k in ("build", "test"):
                self.play(d.animate.move_to(bx[k].get_top() + UP * 0.14), Indicate(bx[k].text, color=ROUTE),
                          run_time=0.5)
            self.play(FadeIn(dc.brackets[0], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Then it is deployed")
            for k in ("deploy", "monitor"):
                self.play(d.animate.move_to(bx[k].get_top() + UP * 0.14), Indicate(bx[k].text, color=ROUTE),
                          run_time=0.5)
            self.play(FadeIn(dc.brackets[1], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Every stage")
            self.play(FadeOut(d), run_time=0.2)
            self.remove(d)
            self.play(LaggedStart(*[Create(x) for x in dc.drops], lag_ratio=0.2), FadeIn(dc.bar), FadeIn(dc[2]),
                      run_time=1.0)
            self.play(Create(dc[4]), Indicate(lp.devs, color=ROUTE, scale_factor=1.05), run_time=0.7)
            settle(self, lp)

        # ========================================================== 1. slide 36: Release
        with self.voiceover(SAY[1]) as vo:
            ref = ref_swap(self, ref, "36")
            vo.wait_until("adds one box")
            lp.add_release(self, run_time=1.4)
            vo.wait_until("release, the moment")
            self.play(lp.light("release", TURN, run_time=0.9))
            self.play(*lp._set_box("release", TURN, fill=0.12), run_time=0.5)
            settle(self, lp)

        # ========================================================== 2. slides 8–10: CI as a pipe of checks
        devs3 = VGroup(*[person_icon(LAPTOP, 0.45) for _ in range(3)]).arrange(DOWN, buff=0.35).move_to([-6.05, 0, 0])
        repo = label_box(["Shared", "Repository"], INK, box_w=2.0).move_to([-4.15, 0, 0])
        ptitle = label("Automated Quality Checks", 22, INK)
        tiles_txt = [["automated tests"], ["coding standards", "style, consistency"],
                     ["static analysis", "defects, vulnerabilities,", "without running the code"]]
        tiles = VGroup(*[label_box(t, INK, box_w=4.8) for t in tiles_txt]).arrange(DOWN, buff=0.16)
        for tl in tiles:
            for ln in tl.text[1:]:
                ln.set_color(S.GREY)
        pin_ = VGroup(ptitle, tiles).arrange(DOWN, buff=0.22).move_to([0.75, -0.1, 0])
        pipe = box(5.4, pin_.height + 0.45, S.GREY, fill=S.GREY_DARKER, fill_opacity=0.6).move_to(pin_)
        func = label_box(["Functional", "Codebase"], OWN, box_w=2.1).move_to([5.3, 0, 0])
        fck = check_mark(0.38, OWN, stroke=5).next_to(func, UP, buff=0.15)
        a_dev = VGroup(*[arrow(p_, repo.frame.get_left(), S.GREY, buff=0.12) for p_ in devs3])
        a_in = arrow(np.array([repo.get_right()[0] + 0.08, 0, 0]), np.array([pipe.get_left()[0] - 0.08, 0, 0]), S.GREY)
        a_out = arrow(np.array([pipe.get_right()[0] + 0.08, 0, 0]), np.array([func.get_left()[0] - 0.08, 0, 0]), S.GREY)
        lch = grey_chip("L09 · L21").next_to(func, DOWN, buff=0.35)
        assert pipe.get_bottom()[1] > -3.4 and tiles.get_bottom()[1] > pipe.get_bottom()[1] + 0.1, tiles.get_bottom()
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(lp), FadeOut(ref), run_time=0.5)
            self.remove(lp, ref)
            ref = lref("8–10")
            self.play(FadeIn(ref), FadeIn(pipe), FadeIn(ptitle), run_time=0.6)
            self.play(FadeIn(a_in), FadeIn(a_out), FadeIn(repo), FadeIn(func), run_time=0.6)
            vo.wait_until("Many developers")
            self.play(LaggedStart(*[FadeIn(p_, shift=RIGHT * 0.1) for p_ in devs3], lag_ratio=0.2), run_time=0.6)
            self.play(LaggedStart(*[GrowArrow(a) for a in a_dev], lag_ratio=0.2), Indicate(repo.text, color=INK),
                      run_time=0.7)
            cc = code_card().move_to(repo.get_top() + UP * 0.4)
            self.play(FadeIn(cc, shift=DOWN * 0.1), run_time=0.3)
            # the card rides inside the pipe, on the left of each tile (clear of the tile text)
            ride_x = tiles.get_left()[0] + 0.45
            vo.wait_until("and every change passes")
            self.play(cc.animate.move_to([ride_x, tiles[0].get_y(), 0]), run_time=0.5)
            self.play(FadeIn(tiles[0], shift=LEFT * 0.15), run_time=0.5)
            self.bring_to_front(cc)
            vo.wait_until("coding standards")
            self.play(cc.animate.move_to([ride_x, tiles[1].get_y(), 0]),
                      FadeIn(tiles[1], shift=LEFT * 0.15), run_time=0.5)
            self.bring_to_front(cc)
            vo.wait_until("and static analysis")
            self.play(cc.animate.move_to([ride_x, tiles[2].get_y(), 0]),
                      FadeIn(tiles[2].frame), FadeIn(tiles[2].text[0]), run_time=0.5)
            self.bring_to_front(cc)
            vo.wait_until("which finds defects")
            self.play(FadeIn(tiles[2].text[1:], shift=UP * 0.08), run_time=0.6)
            self.play(cc.animate.move_to(func.get_left() + LEFT * 0.45 + DOWN * 0.0), run_time=0.7)
            self.play(FadeOut(cc, target_position=func.get_center(), scale=0.5), Create(fck),
                      Indicate(func.text, color=OWN, scale_factor=1.05), run_time=0.6)
            self.remove(cc)
            vo.wait_until("You built this")
            self.play(FadeIn(lch, shift=UP * 0.1), run_time=0.4)
        slide10 = VGroup(devs3, repo, pipe, ptitle, tiles, func, fck, a_dev, a_in, a_out, lch)

        # ========================================================== 3. slides 11–12: delivery vs deployment
        tg = ReleaseToggle()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(slide10), FadeOut(ref), run_time=0.5)
            self.remove(slide10, ref)
            ref = lref("11–12")
            self.play(FadeIn(ref), FadeIn(tg.belt), FadeIn(tg.cards, shift=RIGHT * 0.3), run_time=0.6)
            self.play(tg.cards.animate.shift(RIGHT * 0.6), run_time=0.8)
            settle(self, tg)
            vo.wait_until("Continuous delivery")
            tg.delivery(self)
            n1 = tg.label_end(self, "continuous delivery", at="button")
            self.play(tg.cards.animate.shift(RIGHT * 0.5), run_time=0.8)
            settle(self, tg)
            vo.wait_until("but a person presses")
            self.play(tg.hand.animate(rate_func=there_and_back).shift(DOWN * 0.18),
                      tg.button.frame.animate(rate_func=there_and_back).set_fill(ERR, 0.95),
                      Indicate(tg.button.text, color=INK), run_time=0.8)
            settle(self, tg)
            vo.wait_until("Continuous deployment")
            tg.drop(self, n1, run_time=0.3)
            tg.deployment(self, run_time=1.4)
            tg.label_end(self, "continuous deployment", at="ring")
            vo.wait_until("by itself")
            self.play(LaggedStart(*[c.animate.move_to(tg.ring.get_center()).set_opacity(0) for c in reversed(tg.cards)],
                                  lag_ratio=0.3), Rotate_safe(tg.ring.ring), run_time=1.4)
            settle(self, tg)

        # ========================================================== 4. slides 13–15: CI/CD for ML
        ci = text_card("CI for ML", ["+ data quality", "+ model performance", ("expensive", COST)], card_w=5.6)
        cd = text_card("CD for ML", ["release only within a tolerance", "challenge: data drift"], card_w=5.6)
        cd.frame.stretch_to_fit_height(ci.frame.height)
        VGroup(cd.head, cd.rows).align_to(cd.frame, UP).shift(DOWN * 0.3)
        cards = VGroup(ci, cd).arrange(RIGHT, buff=0.6).move_to([0, 0.4, 0])
        VGroup(cd.head, cd.rows).align_to(cd.frame, UP).shift(DOWN * 0.3)
        VGroup(ci.head, ci.rows).align_to(ci.frame, UP).shift(DOWN * 0.3)
        app = dashed_chip("this repo: an app, not a model · L15 was the model").next_to(cards, DOWN, buff=0.6)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(tg), FadeOut(ref), run_time=0.5)
            self.remove(tg, ref, *tg.get_family())
            ref = lref("13–15")
            self.play(FadeIn(ref), FadeIn(ci.frame), FadeIn(ci.head), run_time=0.5)
            vo.wait_until("also checks data quality")
            self.play(FadeIn(ci.rows[0], shift=RIGHT * 0.1), run_time=0.4)
            self.play(FadeIn(ci.rows[1], shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("which makes it expensive")
            self.play(FadeIn(ci.rows[2], shift=RIGHT * 0.1), run_time=0.4)
            self.play(Indicate(ci.rows[2], color=COST), run_time=0.6)
            vo.wait_until("And C D releases")
            self.play(FadeIn(cd.frame), FadeIn(cd.head), run_time=0.5)
            self.play(FadeIn(cd.rows[0], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("and must cope")
            self.play(FadeIn(cd.rows[1], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("This repo deploys")
            self.play(FadeIn(app, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("lecture 15")
            self.play(Indicate(app.text, color=INK, scale_factor=1.04), run_time=0.6)

        # ========================================================== 5. this repo on the loop
        p = code(WF, 1, 2, font_size=20)
        p.move_to([0, -1.55 - p.height / 2, 0])
        uline = hl_bar(code_span(p.code, 0, "Continuous Integration"), TURN, 0.22)
        y_hi = lp.boxes["test"].get_bottom()[1] - 0.4
        c_test = loop_chip(lp, "test", "L21", S.GREY, y_hi, dashed=True)
        c_rel = loop_chip(lp, "release", "tagged images land in ECR", CLOUD, y_hi)
        c_rel.align_to(c_test, LEFT).shift(RIGHT * (c_test.width + 0.25))
        c_mon = loop_chip(lp, "monitor", "the run's color + your own check", S.GREY, y_hi - 0.6)
        assert c_mon.get_bottom()[1] > lp.decor.bar.get_top()[1] + 0.05, (c_mon.get_bottom(), lp.decor.bar.get_top())
        assert c_rel.get_bottom()[1] > c_mon.get_top()[1] + 0.05
        err = erratum_tag("runs no test: the CD half").next_to(p.header, RIGHT, buff=0.3)
        assert err.get_right()[0] < 6.5, err.get_right()
        assert err.get_bottom()[1] > -3.6, err.get_bottom()
        assert p.get_top()[1] < lp.devs.get_bottom()[1] - 0.15, (p.get_top(), lp.devs.get_bottom())
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(cards), FadeOut(app), FadeOut(ref), run_time=0.5)
            self.remove(cards, app, ref)
            self.play(FadeIn(lp, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("Build, release and deploy")
            self.play(*[a for k in ("codebase", "build", "release", "deploy") for a in lp._set_box(k, CLOUD)],
                      run_time=0.8)
            settle(self, lp)
            vo.wait_until("release is when")
            self.play(FadeIn(c_rel, shift=UP * 0.1), run_time=0.4)
            lp.keep(self, c_rel)
            self.play(lp.light("release", CLOUD), run_time=0.6)
            settle(self, lp)
            vo.wait_until("Test stays dashed")
            # solid -> dashed as a cross-fade (a Transform scrambles the dashes mid-way)
            tb = lp.boxes["test"]
            t_dash = outline_box(tb.frame.width, tb.frame.height, S.GREY).move_to(tb.frame)
            self.play(FadeIn(t_dash), tb.frame.animate.set_stroke(opacity=0).set_fill(opacity=0),
                      tb.text.animate.set_color(S.GREY), run_time=0.6)
            tb.frame.become(t_dash)
            self.remove(t_dash)
            self.play(FadeIn(c_test, shift=UP * 0.1), run_time=0.4)
            lp.keep(self, c_test)
            settle(self, lp)
            vo.wait_until("the workflow is named")
            self.play(FadeIn(p, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(uline), run_time=0.5)
            vo.wait_until("but runs no test")
            self.play(FadeIn(err, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("It's the C D half")
            self.play(Indicate(lp.brackets[1], color=INK, scale_factor=1.06), run_time=0.7)
            settle(self, lp)
            vo.wait_until("And monitor")
            self.play(FadeIn(c_mon, shift=UP * 0.1), run_time=0.4)
            lp.keep(self, c_mon)
            self.play(lp.light("monitor", INK), run_time=0.6)
            settle(self, lp)

        # ========================================================== 6. slides 16–18: thin YAML, thick container
        tiles6 = VGroup(*[box(1.8, 0.9, S.GREY, fill_opacity=0.08) for _ in range(6)]).arrange(RIGHT, buff=0.25)
        tiles6.move_to([0, 1.9, 0])
        gha_box = box(1.8, 0.9, TOOL, fill_opacity=0.18).move_to(tiles6[2])
        gha_txt = VGroup(label("GitHub", 20, TOOL), label("Actions", 20, TOOL)).arrange(DOWN, buff=0.06).move_to(gha_box)
        runner = VGroup(runner_icon(0.55, lit=True), label("runner", 22, CLOUD)).arrange(DOWN, buff=0.12)
        rbox = box(2.3, runner.height + 0.45, CLOUD, fill_opacity=0.08).move_to([-4.3, -0.6, 0])
        runner.move_to(rbox)
        rgrp = VGroup(rbox, runner)
        cr = crate(T_TOOLBOX, box_h=1.3).move_to([3.0, -0.6, 0])
        a_build = Arrow(rbox.get_right() + UP * 0.3, cr.get_left() + UP * 0.3, buff=0.12, color=CLOUD, stroke_width=3,
                        tip_length=0.18)
        a_run = Arrow(rbox.get_right() + DOWN * 0.3, cr.get_left() + DOWN * 0.3, buff=0.12, color=CLOUD,
                      stroke_width=3, tip_length=0.18)
        t_build = label("build it", 20, INK).next_to(a_build, UP, buff=0.1)
        t_run = label("run it", 20, INK).next_to(a_run, DOWN, buff=0.1)
        link = DashedLine(gha_box.get_bottom(), rbox.get_top() + RIGHT * 0.4, color=TOOL, stroke_width=2.5,
                          dash_length=0.1)
        cap1 = label("thin YAML", 22, S.GREY)
        cap2 = label("· thick container", 22, S.GREY)
        caps = VGroup(cap1, cap2).arrange(RIGHT, buff=0.15).move_to([0, -2.6, 0])
        yaml_strip = ok_chip("ci_cd_aws.yml", mono_font=True).next_to(rbox, DOWN, buff=0.25)
        books = ok_chip("the playbooks you ran").next_to(cr, DOWN, buff=0.25)
        assert tiles6.get_left()[0] > -6.6 and tiles6.get_right()[0] < 6.6, tiles6.get_width()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(lp), FadeOut(p), FadeOut(uline), FadeOut(err), run_time=0.6)
            self.remove(lp, p, uline, err, *lp.get_family())
            ref = lref("16–18")
            self.play(FadeIn(ref), LaggedStart(*[FadeIn(t, shift=DOWN * 0.1) for t in tiles6], lag_ratio=0.15),
                      run_time=1.2)
            vo.wait_until("the course uses")
            self.play(ReplacementTransform(tiles6[2], gha_box), FadeIn(gha_txt), run_time=0.6)
            vo.wait_until("to build the deployment container")
            self.play(Create(link), FadeIn(rgrp, shift=DOWN * 0.1), FadeIn(cr, shift=LEFT * 0.1), run_time=0.7)
            self.play(GrowArrow(a_build), FadeIn(t_build), run_time=0.5)
            vo.wait_until("and run it")
            self.play(GrowArrow(a_run), FadeIn(t_run), Indicate(cr.text, color=IMAGE, scale_factor=1.04), run_time=0.6)
            vo.wait_until("on every commit")
            cd_ = dot(ROUTE).move_to([-6.2, 0.75, 0])
            self.play(FadeIn(cd_), run_time=0.2)
            self.play(cd_.animate.move_to(rbox.get_top() + LEFT * 0.4), run_time=0.6)
            self.play(FadeOut(cd_), Indicate(runner, color=CLOUD, scale_factor=1.06), run_time=0.4)
            self.remove(cd_)
            vo.wait_until("The workflow file stays thin")
            self.play(FadeIn(yaml_strip), FadeIn(cap1, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("the deploy logic")
            self.play(FadeIn(cap2, shift=UP * 0.1), FadeIn(books, shift=UP * 0.1), Circumscribe(cr, color=IMAGE, buff=0.08),
                      Indicate(cr.text, color=IMAGE, scale_factor=1.04), run_time=0.9)
        everything = VGroup(tiles6, gha_box, gha_txt, link, rgrp, cr, a_build, a_run, t_build, t_run, yaml_strip, books, caps, ref)
        self.play(FadeOut(everything), run_time=0.8)
        self.remove(everything, *everything.get_family())
        self.wait(0.4)
