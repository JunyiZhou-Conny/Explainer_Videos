"""S04 · When does the pipeline wake up? (AC215 L21). TRACKER P5 1 throughout (README Part 5,
step 1: the trigger sentence). Lecture: 21 · slides 25 (beat 0), 23 (beat 4), 24 (beat 5).

Beats (script.md "## S04", one voiceover block each):
0. TRACKER P5 1 fades in. lecture_ref 25. A GREY quote chip from the slide, "on every push or pull
   request" (left); CODE(ci.yml 7–11) beside it (right); a GREY arrow "more precisely:" from the
   chip to the panel. Lines 8–9 (push: branches) get PINK bars on "pushes to main or develop", lines
   10–11 (pull_request: branches) on "and pull requests into".
1. Lecture tag off. The chip and arrow go; the panel shrinks (22 → 20 pt) into the top-right corner.
   V3 TriggerLanes (main GREEN, develop, feature/login; GREY runners, GOLD 'runs' meter) fades in on
   the left. A push dot lands on main: PINK spark, main's runner lights BLUE, the meter ticks; the
   same on develop; a dot on feature/login: no spark, the dot turns GREY, its runner stays GREY.
   On "waits for your pull request" the feature runner is ringed and the panel's pull_request lines
   flash PINK. "A small note": the one-line panel ci.yml:2 (the comment) appears bottom right,
   "main branch" is underlined YELLOW, two GREY erratum tags stack beside the lanes ("erratum · the
   comment: main only", "the triggers: main and develop") and the corner panel's branch lines
   flash.
2. The corner panel, comment strip and tags go; the runners reset to GREY. Three new dots land on
   feature/login (GREY, no spark), one per phrase; a dashed PINK arrow "PR → main" waits, unlit,
   from the feature tip up to main. PONDER (8 s): the card sits right of the lanes (same words,
   line breaks moved to fit 4.5 units at ~24 pt) so the dots and the PR arrow stay in view.
3. The card leaves and the lanes slide to the middle. The three dots are ringed: GREY chip "0 runs"
   beside the feature runner. The PR arrow lights solid PINK: a spark, main's runner lights BLUE,
   the meter ticks, BLUE chip "1 run"; a fifth dot lands on feature/login, the arrow re-aims from
   the new tip, a second spark and tick, GREY chip "+1 per push while it's open" under the tip.
4. lecture_ref 23. The feature tip is ringed; a GREY dashed ghost merge commit 'github.sha' appears
   above main, joined to both tips, with a PINK arrow into main's runner; the PR arrow turns GREY
   dashed and its label goes (the runner's arrow now comes from the ghost). The ghost's label flashes on "the commit ID the jobs
   see"; GREY caption "each merge is tested".
5. lecture_ref 24. The answer chips and caption go. The GOLD meter blocks pulse one by one; three
   GREY chips dock on the meter row, one per phrase: "branch filter", "one shared build", "image
   kept 1 day"; GOLD cost tag "private repos: every run counts · public: free" under them.
6. Lecture tag off. The lanes leave. A small replay of S02's door: BLUE 'GitHub.com' server with
   its door, the GREEN 'branch protection' gate in front of it, the bell inside with the BLUE
   'Actions' badge. A GREEN dot passes the open gate and the door and lands; only then the PINK spark
   fires and the bell rings. S02's GREY caption "Actions on a push is the bell, not the gate."
   writes under the server; a RED failure mark appears at the bell while the landed dot stays
   (flashes GREEN). Everything fades with the tracker; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.components import ponder_card
from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ the real sources (checked)
CI = ".github/workflows/ci.yml"
assert excerpt(CI, 2, 2).strip() == "# Runs on every push and pull request to main branch"
assert excerpt(CI, 7, 7).strip() == "on:"
assert excerpt(CI, 8, 8).strip() == "push:" and excerpt(CI, 10, 10).strip() == "pull_request:"
assert excerpt(CI, 9, 9).strip() == "branches: [main, develop]"
assert excerpt(CI, 11, 11).strip() == "branches: [main, develop]"
assert TRIGGER_BRANCHES == ("main", "develop")

FEATURE = "feature/login"
SHIFT3 = 1.6   # beat 3: the lanes move from the left edge to the middle once the ponder card is gone
LANES_LEFT, LANES_Y = -6.3, -0.5
# script.md's question, same words; the line breaks moved so the card fits right of the lanes
# (4.5 wide, ~24 pt) and the viewer keeps the three dots and the PR arrow in view while thinking
PONDER_Q = ("You push three commits\nto feature/login.\nHow many CI runs start?\n"
            "Then you open a PR\ninto main: how many now?")


def pr_arrow(scene, tl: TriggerLanes, src: str = FEATURE, dst: str = "main"):
    """TriggerLanes.pr(fire=False) with the label placed between the main and develop lanes, left of
    the arc (the piece's own label lands on the develop lane). Sets the attributes pr_fire() uses."""
    a = tl.dots[src][-1].get_center() + UP * 0.12
    b = np.array([tl.lx1 - 0.3, tl.lanes[dst].line.get_center()[1], 0]) + DOWN * 0.12
    ar = route(a, b, arc=-0.6, dashed=True)
    y = tl.lanes[dst].line.get_center()[1] - tl.pitch * 0.5
    pts = route(a, b, arc=-0.6).get_points()
    p = min(pts, key=lambda q: abs(q[1] - y))
    t = label(f"PR → {dst}", 20, ROUTE)
    t.move_to([p[0] - 0.25 - t.width / 2, y, 0])
    scene.play(Create(ar), FadeIn(t), run_time=0.6)
    tl.pr_arrow, tl.pr_label, tl.pr_dst, tl.pr_a, tl.pr_b = ar, t, dst, a, b
    tl.keep(scene, ar, t)
    return ar, t


class WhenItRuns(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S04"] == 7, len(SAY)

        # ========================================================== 0. slide 25 vs the file
        tr = tracker_p5(1)
        ref = lref("25")
        quote = grey_chip("“on every push or pull request”", size=22).move_to([-4.25, 0.1, 0])
        p0 = code(CI, 7, 11).move_to([3.35, 0.1, 0])
        more = arrow(quote.get_right() + RIGHT * 0.1, p0.get_left() + LEFT * 0.1, S.GREY)
        more_t = label("more precisely:", 20, S.GREY).next_to(more, UP, buff=0.15)
        more_t.set_x(more.get_center()[0])
        push_bars = VGroup(line_bar(p0.code, 1, ROUTE, 0.25), line_bar(p0.code, 2, ROUTE, 0.25))
        pr_bars = VGroup(line_bar(p0.code, 3, ROUTE, 0.25), line_bar(p0.code, 4, ROUTE, 0.25))
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("The slide says")
            self.play(FadeIn(ref), FadeIn(quote, shift=UP * 0.2), run_time=0.6)
            flash_tag(self, quote, INK)
            vo.wait_until("The file is more precise")
            self.play(FadeIn(p0, shift=LEFT * 0.2), run_time=0.5)
            self.play(GrowArrow(more), FadeIn(more_t), run_time=0.5)
            vo.wait_until("pushes to main or develop")
            self.play(LaggedStart(*[FadeIn(b) for b in push_bars], lag_ratio=0.3),
                      Indicate(p0.code.code_lines[1], color=ROUTE, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and pull requests into")
            self.play(LaggedStart(*[FadeIn(b) for b in pr_bars], lag_ratio=0.3),
                      Indicate(p0.code.code_lines[3], color=ROUTE, scale_factor=1.06), run_time=0.6)

        # ========================================================== 1. three lanes
        p1 = code(CI, 7, 11, font_size=20)
        p1.shift(np.array([6.5 - p1.get_right()[0], 3.5 - p1.get_top()[1], 0]))
        tl = TriggerLanes(lane_w=8.0)
        dx = LANES_LEFT - tl.get_left()[0]
        tl.shift(np.array([dx, LANES_Y - tl.lanes["develop"].line.get_center()[1], 0]))
        tl.lx0 += dx   # the piece keeps its lane ends as plain floats: follow the shift
        tl.lx1 += dx
        strip2 = code_strip(CI, 2, font_size=20)
        strip2.shift(np.array([6.5 - strip2.get_right()[0], -3.55 - strip2.get_bottom()[1], 0]))
        main_words = code_span(strip2.code, 0, "main branch")
        main_ul = under(main_words, TURN)
        errs = VGroup(erratum_tag("erratum · the comment: main only"),
                      erratum_tag("the triggers: main and develop")).arrange(DOWN, aligned_edge=RIGHT, buff=0.18)
        errs.next_to(strip2, UP, buff=0.3).align_to(strip2, RIGHT)
        with self.voiceover(SAY[1]) as vo:
            gone = VGroup(quote, more, more_t, push_bars, pr_bars)
            self.play(FadeOut(gone), FadeOut(ref), run_time=0.4)
            self.remove(gone, *gone.get_family(), ref)
            self.play(Transform(p0, p1), run_time=0.7)
            self.remove(p0)
            self.add(p1)
            self.play(FadeIn(tl, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Push to main")
            tl.push(self, "main")
            vo.wait_until("Push to develop")
            tl.push(self, "develop")
            vo.wait_until("Push to a feature branch")
            d = tl.push(self, FEATURE)
            vo.wait_until("and nothing happens")
            self.play(d.animate.set_color(S.GREY), Indicate(tl.runners[FEATURE], color=S.GREY, scale_factor=1.2),
                      run_time=0.6)
            vo.wait_until("on any other branch")
            r_ring = ring(tl.runners[FEATURE], S.GREY, buff=0.1)
            self.play(Create(r_ring), run_time=0.5)
            vo.wait_until("the pipeline waits for your pull request")
            p1_pr = VGroup(line_bar(p1.code, 3, ROUTE, 0.25), line_bar(p1.code, 4, ROUTE, 0.25))
            self.play(FadeIn(p1_pr), Indicate(p1.code.code_lines[3], color=ROUTE, scale_factor=1.08), run_time=0.7)
            vo.wait_until("A small note")
            self.play(FadeOut(r_ring), FadeOut(p1_pr), FadeIn(strip2, shift=UP * 0.2), run_time=0.6)
            self.remove(r_ring, p1_pr)
            vo.wait_until("the comment at the top of the file")
            self.play(Create(main_ul), Indicate(main_words, color=TURN, scale_factor=1.12), run_time=0.6)
            self.play(FadeIn(errs[0], shift=UP * 0.15), run_time=0.4)
            vo.wait_until("the triggers say main and develop")
            p1_br = VGroup(line_bar(p1.code, 2, TURN, 0.2), line_bar(p1.code, 4, TURN, 0.2))
            self.play(FadeIn(errs[1], shift=UP * 0.15), FadeIn(p1_br), run_time=0.5)
            self.play(Indicate(p1.code.code_lines[2], color=TURN, scale_factor=1.06),
                      Indicate(p1.code.code_lines[4], color=TURN, scale_factor=1.06), run_time=0.6)

        # ========================================================== 2. the ponder
        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(p1, p1_br, strip2, main_ul, errs)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            tl.reset_runners(self)
            vo.wait_until("You push three commits")
            new = []
            for _ in range(3):
                dd = tl.push(self, FEATURE)
                self.play(dd.animate.set_color(S.GREY), run_time=0.2)
                new.append(dd)
            vo.wait_until("How many runs start")
            self.play(Indicate(tl.runners[FEATURE], color=TURN, scale_factor=1.25), run_time=0.6)
            vo.wait_until("Then you open a pull request")
            pr_arrow(self, tl)
            vo.wait_until("How many now")
            self.play(Indicate(tl.runners["main"], color=TURN, scale_factor=1.25), run_time=0.6)
        # pause_and_ponder, placed right of the lanes instead of centred over them
        card = ponder_card(PONDER_Q, width=4.5).move_to([4.3, 0.0, 0])
        self.play(FadeIn(card, scale=0.95), run_time=0.6)
        bar = card[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 3. the answer
        zero = grey_chip("0 runs", size=22).next_to(tl.runners[FEATURE], RIGHT, buff=0.3)
        one = github_chip("1 run", size=22).next_to(tl.runners["main"], RIGHT, buff=0.3)
        plus = grey_chip("+1 per push while it's open", size=22)
        with self.voiceover(SAY[3]) as vo:
            # the card leaves and the lanes slide to the middle (room for the answer chips on the right)
            self.play(FadeOut(card), tl.animate.shift(RIGHT * SHIFT3), run_time=0.6)
            self.remove(card)
            tl.lx0 += SHIFT3
            tl.lx1 += SHIFT3
            tl.pr_a, tl.pr_b = tl.pr_a + RIGHT * SHIFT3, tl.pr_b + RIGHT * SHIFT3
            zero.next_to(tl.runners[FEATURE], RIGHT, buff=0.3)
            one.next_to(tl.runners["main"], RIGHT, buff=0.3)
            three = VGroup(*new)
            three_ring = ring(three, S.GREY, buff=0.12)
            self.play(Create(three_ring), run_time=0.5)
            self.play(FadeIn(zero, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("the branch filter")
            self.play(Indicate(VGroup(tl.lanes["main"].name, tl.lanes["develop"].name), color=OWN,
                               scale_factor=1.1), FadeOut(three_ring), run_time=0.7)
            self.remove(three_ring)
            vo.wait_until("One when the pull request opens")
            tl.pr_fire(self)
            self.play(FadeIn(one, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("and one more for every later push")
            tip = tl.push(self, FEATURE)
            self.play(tip.animate.set_color(S.GREY), run_time=0.2)
            tl.pr_a = tip.get_center() + UP * 0.12
            tl.pr_fire(self)
            plus.move_to([tip.get_x() - 0.3 + plus.width / 2, tip.get_y() - 0.72, 0])
            self.play(FadeIn(plus, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("while it stays open")
            self.play(Indicate(tl.pr_arrow, color=ROUTE, scale_factor=1.04), run_time=0.6)

        # ========================================================== 4. the ghost merge (slide 23)
        ref23 = lref("23")
        cap = label("each merge is tested", 22, S.GREY)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(zero, one, plus)), FadeIn(ref23), run_time=0.5)
            self.remove(zero, one, plus)
            tip_ring = ring(tip, TURN, buff=0.1)
            self.play(Create(tip_ring), run_time=0.5)
            self.play(Indicate(tip, color=TURN, scale_factor=1.4), run_time=0.5)
            vo.wait_until("GitHub makes a temporary merge")
            self.play(FadeOut(tip_ring), run_time=0.3)
            self.remove(tip_ring)
            ghost = tl.ghost_merge(self)
            dim = route(tl.pr_a, tl.pr_b, arc=-0.6, color=S.GREY, dashed=True)
            self.play(Transform(tl.pr_arrow, dim), run_time=0.5)
            tl.drop(self, tl.pr_label, run_time=0.3)
            vo.wait_until("and the commit ID the jobs see")
            sha_t = ghost[1]
            self.play(Indicate(sha_t, color=ROUTE, scale_factor=1.15), run_time=0.6)
            self.play(ShowPassingFlash(ghost[4].copy().set_stroke(TURN, 6), time_width=0.6), run_time=0.6)
            vo.wait_until("What will land is what gets tested")
            self.play(Indicate(ghost[0], color=INK, scale_factor=1.4), run_time=0.6)
            vo.wait_until("each merge is tested")
            cap.next_to(sha_t, RIGHT, buff=0.5)
            self.play(Write(cap), run_time=0.7)

        # ========================================================== 5. what it costs (slide 24)
        ref24 = lref("24")
        blocks = list(tl.meter[1:])
        chips = [grey_chip(s, size=20) for s in ("branch filter", "one shared build", "image kept 1 day")]
        row = VGroup(*chips).arrange(RIGHT, buff=0.25)
        row.next_to(tl.meter, RIGHT, buff=0.45)
        cost = cost_tag("private repos: every run counts · public: free")
        cost.next_to(row, DOWN, buff=0.22).align_to(tl.meter, LEFT)
        cues = ("with a branch filter", "one build shared by every job", "and an image kept one day")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(cap), ReplacementTransform(ref23, ref24), run_time=0.5)
            self.remove(cap)
            vo.wait_until("integrating often costs compute")
            for b in blocks:
                self.play(Indicate(b, color=COST, scale_factor=1.35), run_time=0.3)
            self.add(tl)
            for c, cue in zip(chips, cues):
                vo.wait_until(cue)
                self.play(FadeIn(c, shift=LEFT * 0.3), run_time=0.45)
            vo.wait_until("On private repositories")
            self.play(FadeIn(cost, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, cost)
            vo.wait_until("public ones run free")
            self.play(Indicate(cost.text, color=COST, scale_factor=1.06), run_time=0.6)

        # ========================================================== 6. the bell, not the gate
        sd = ServerDoor(name="GitHub.com", box_w=5.0, box_h=3.0)
        for m in (sd.gate, sd.gate.text, sd.bell_text):
            sd.remove(m)
        prot = gate_glyph(0.9, 0.6, PASS).move_to(sd.door.get_left() + LEFT * 0.42)
        prot_t = label("branch protection", 20, PASS).next_to(prot, UP, buff=0.12)
        prot_t.shift(LEFT * max(0, prot_t.get_right()[0] - (sd.door.get_left()[0] - 0.12)))
        act = github_chip("Actions").next_to(sd.bell, UP, buff=0.12)
        sd.add(prot, prot_t, act)
        sd.shift(np.array([1.2 - sd.server.get_center()[0], 0.35 - sd.server.get_center()[1], 0]))
        bell_cap = sd.caption().next_to(sd.server, DOWN, buff=0.45)
        bell_cap.set_x(0)
        with self.voiceover(SAY[6]) as vo:
            lanes_all = VGroup(tl, row, cost)
            self.play(FadeOut(lanes_all, shift=LEFT * 0.4), FadeOut(ref24), run_time=0.6)
            self.remove(lanes_all, *lanes_all.get_family(), ref24)
            self.play(FadeIn(sd, shift=LEFT * 0.3), run_time=0.6)
            vo.wait_until("the run starts after GitHub has accepted your push")
            d = sd.enter(self, dot(PASS), gate=prot)
            sp = spark().move_to(act)
            self.play(FadeIn(sp, scale=0.5), Indicate(act, color=ROUTE, scale_factor=1.1),
                      prot.bar.animate.set_color(PASS), run_time=0.35)
            self.play(FadeOut(sp, scale=1.4), run_time=0.25)
            self.remove(sp)
            sd.ring(self)
            vo.wait_until("It's the bell, not the gate")
            self.play(Write(bell_cap), run_time=0.9)
            vo.wait_until("a red run doesn't undo the push")
            red = state_mark("failure", 0.4).next_to(sd.bell, LEFT, buff=0.3)
            self.play(FadeIn(red, scale=0.6), run_time=0.4)
            self.play(Flash(d, color=PASS), Indicate(d, color=PASS, scale_factor=1.4), run_time=0.7)
            sd.keep(self, d, red)

        everything = VGroup(sd, bell_cap, tr)
        self.play(FadeOut(everything), run_time=0.6)
        self.remove(everything, *everything.get_family())
        self.wait(0.3)
