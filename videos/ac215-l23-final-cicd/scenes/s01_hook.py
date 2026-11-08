"""S01 · Thirty-three commits, one backslash (cold open of AC215 L23). No tracker until the sample
in beat 5. Lecture: 23 · slides 1–4 (beat 3 only).

Beats (script.md "## S01", one voiceover block each):
0. Black frame. A full-width terminal 'laptop' (centred), prompt student@laptop:~$, types the extra
   `git -C /home/student/cheese-app-aws log --format=%s | sort | uniq -c | sort -rn` (folds with
   ' \\'; GREY 'extra' row tag beside it), then TERM(laptop/50: 2–8) (line 7, the merge subject, is
   wrapped: 73 characters). On "33 of them" line 2 turns YELLOW and the others dim to 40 %; the
   message is underlined on "slash run deploy app"; the line pulses on "That sentence is a button".
1. Line 5 (`\\run-deploy-app`) grows and turns RED, its backslash pulses. The terminal shrinks
   away; V1 KeywordSieves teaser: one PURPLE sieve `contains(…, '/run-')`, 33 PINK dots stream
   through it and light the small BLUE server; a RED ribbon `\\run-deploy-app` waits above the sieve
   and, on "nothing runs at all", hits it and bounces off. The sieve flashes RED on "One character".
2. The sieve dims; a YELLOW question card drops in the middle; on "By the end of part 2" it shrinks
   to 20 pt and pins top left (the sieve fades).
3. lecture_ref(23, "1–4") top right. A title card "Lecture 23 · Final Deployment and Review", three
   chips under it (Motivation, Automation, Review) one per phrase; beside "Motivation" our own GREY
   sketch: a web page with a rising curve and a dashed "now" line; a PINK arrow from the page to a
   small BLUE server box ("runs somewhere"); the curve grows and the "now" line moves on "stays
   current".
4. Lecture tag and card fade. Three groups, one per sentence: a GREY laptop ("this recording
   machine"), a GREEN ✓ "ran right here" under it; a BLUE box "AWS · us-east-1" with a RED chip
   "first real error"; a small schematic console page with its 'illustration' tag (flashed).
5. Three chips: "Docker running", "your AWS account + billing" (GOLD cost tag "this lecture runs a
   server until you delete it"), "a GitHub repository (part 2)". The question card moves to the top
   right (the tracker owns the top left). Samples: the YELLOW tracker (Deployment Steps, step 5 of
   15) top left, a code panel `src/deployment/inventory.yml · lines 1–11` (header circled), a YELLOW
   '▶ your turn' tag under it. Everything fades, the question card last; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources (checked)
LOG = capture("50")
assert LOG.cmd == "git -C /home/student/cheese-app-aws log --format=%s | sort | uniq -c | sort -rn", LOG.cmd
LOG_LINES = LOG.at((2, 8))
assert LOG_LINES[0] == "     33 /run-deploy-app", LOG_LINES[0]
assert LOG_LINES[3] == "      1 \\run-deploy-app", LOG_LINES[3]
assert LOG.exit == 0
assert 33 + 6 == sum(int(s.split()[0]) for s in LOG_LINES) == 39
QUESTION = "How does a sentence deploy a server,\nand why did one character stop it?"
LECTURE_TITLE = "Lecture 23 · Final Deployment and Review"
PARTS = (("Motivation", "Its motivation"), ("Automation", "in three parts"), ("Review", "in three parts"))
NEEDS = (("Docker running", "You need Docker"), ("your AWS account + billing", "your own AWS account"),
         ("a GitHub repository (part 2)", "a GitHub repository"))


def dim(m, f: float = 0.3):
    """Scale every part's own fill and stroke opacity by f (as L21 S01)."""
    for s in m.family_members_with_points():
        s.set_fill(opacity=s.get_fill_opacity() * f)
        s.set_stroke(opacity=s.get_stroke_opacity() * f)
    return m


def fade_to(m, f: float = 0.3, run_time: float = 0.5) -> ApplyFunction:
    """ANIM: m dims to f of its opacity (f > 1 brings it back)."""
    return ApplyFunction(lambda x: dim(x, f), m, run_time=run_time)


def glyph_anim(glyphs, **kw):
    """ANIM: one .animate per glyph (glyphs of a terminal row stay inside the row on the scene)."""
    anims = []
    for g in glyphs:
        a = g.animate
        if "color" in kw:
            a = a.set_color(kw["color"])
        if "opacity" in kw:
            a = a.set_opacity(kw["opacity"])
        anims.append(a)
    return AnimationGroup(*anims)


def _curve_pts(page, n: int) -> list:
    """Points of the sketch's rising curve, k = 0..n (n = 10 reaches the page's right side)."""
    x0, y0 = page.get_left()[0] + 0.3, page.get_bottom()[1] + 0.3
    return [[x0 + 0.24 * k, y0 + 0.04 * k + 0.009 * k * k, 0] for k in range(n + 1)]


def _curve(pts) -> VMobject:
    c = VMobject(stroke_color=S.GREY, stroke_width=4)
    c.set_points_smoothly(pts)
    return c


def web_sketch() -> VGroup:
    """Our own GREY sketch of a prediction web page: a page with a top bar, a rising curve (up to
    'now') and a dashed 'now' line (its word under the page). .page .curve .now .now_text; curve_to(n) the curve up to step n."""
    page = box(3.0, 2.1, S.GREY, fill_opacity=0.05, radius=0.12)
    bar = Line(page.get_corner(UL) + DOWN * 0.32, page.get_corner(UR) + DOWN * 0.32, color=S.GREY,
               stroke_width=2)
    dots_ = VGroup(*[Dot(radius=0.04, color=S.GREY) for _ in range(3)]).arrange(RIGHT, buff=0.08)
    dots_.move_to(page.get_corner(UL) + np.array([0.3, -0.16, 0]))
    pts = _curve_pts(page, 7)
    curve = _curve(pts)
    xn, y0 = pts[-1][0], page.get_bottom()[1] + 0.2
    now = DashedLine([xn, y0, 0], [xn, page.get_top()[1] - 0.45, 0], color=S.GREY, stroke_width=2.5,
                     dash_length=0.08)
    nt = label("now", 20, S.GREY).next_to(page, DOWN, buff=0.1).set_x(xn)
    g = VGroup(page, bar, dots_, curve, now, nt)
    g.page, g.chrome, g.curve, g.now, g.now_text = page, VGroup(bar, dots_), curve, now, nt
    g.curve_to = lambda n: _curve(_curve_pts(page, n))
    return g


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 6, len(SAY)

        # ========================================================== 0. 33 commits, one message
        t = term(P_HOME, rows=10)
        t.shift(UP * (0 - t.box.get_center()[1]))
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            cmd = type_cmd(self, t, LOG.cmd, type_time=1.3)
            ex = beside(extra_row(), cmd, buff=0.5)
            pin(self, cmd, ex)
            rows = out(self, t, LOG_LINES, wrap=True, run_time=0.6)
            top = rows[0]
            assert top.text.strip() == "33 /run-deploy-app"
            others = [r for r in rows if r is not top]
            vo.wait_until("33 of them")
            self.play(glyph_anim(top.glyphs, color=TURN),
                      *[glyph_anim(r.glyphs, opacity=0.4) for r in others], run_time=0.6)
            self.play(Indicate(substring(top, "33"), color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("slash run deploy app")
            msg = substring(top, "/run-deploy-app")
            ul = under(msg, TURN)
            self.play(Create(ul), run_time=0.5)
            attach(self, top, ul)
            vo.wait_until("That sentence is a button")
            self.play(Indicate(msg, color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Pushed to main")
            self.play(Circumscribe(top, color=TURN, buff=0.08), run_time=0.9)

        # ========================================================== 1. the backslash
        back = [r for r in rows if r.text.strip() == "1 \\run-deploy-app"][0]
        k = KeywordSieves(teaser=True)
        k.shift(LEFT * 0.4 + DOWN * 0.1)
        with self.voiceover(SAY[1]) as vo:
            self.play(glyph_anim(back.glyphs, color=ERR, opacity=1.0), run_time=0.4)
            self.play(back.animate.scale(1.18, about_edge=LEFT), run_time=0.5)
            vo.wait_until("the slash leans")
            self.play(Indicate(substring(back, "\\"), color=ERR, scale_factor=1.8), run_time=0.7)
            vo.wait_until("To the workflow")
            self.play(FadeOut(t, scale=0.3), run_time=0.5)
            self.remove(t, *t.get_family())
            self.play(FadeIn(k), run_time=0.5)
            k.stream(self, 33, run_time=1.8)
            rib = k.hover(self, ribbon(BACKSLASH, ERR), run_time=0.3)
            vo.wait_until("and nothing runs at all")
            k.drop(self, rib, 0, miss="bounce", run_time=0.9)
            vo.wait_until("One character")
            self.play(k.flash(0, False, run_time=0.6))

        # ========================================================== 2. the question
        card = question_card(QUESTION)
        card.move_to([0, 0.2, 0])
        small = question_card(QUESTION, size=20)
        small.move_to([-6.6 + small.width / 2, 3.6 - small.height / 2, 0])
        with self.voiceover(SAY[2]) as vo:
            self.play(fade_to(k, 0.3), run_time=0.5)
            self.play(FadeIn(card, shift=DOWN * 0.6), run_time=0.6)
            vo.wait_until("By the end of part 2")
            self.play(Transform(card, small), FadeOut(k), run_time=0.9)
            self.remove(k, *k.get_family())
            self.play(Indicate(card.text, color=TURN, scale_factor=1.05), run_time=0.7)

        # ========================================================== 3. the lecture: three parts
        lr = lref("1–4")
        head = label(LECTURE_TITLE, 28, INK)
        head_fr = RoundedRectangle(width=head.width + 0.7, height=head.height + 0.5, corner_radius=0.14,
                                   stroke_color=INK, stroke_width=2.5).set_fill(PANEL, 1)
        head.move_to(head_fr)
        title = VGroup(head_fr, head).move_to([0, 1.75, 0])
        chips = VGroup(*[grey_chip(s, size=24, color=INK) for s, _ in PARTS])
        chips.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-4.75, -0.55, 0])
        sk = web_sketch().move_to([-0.6, -0.45, 0])
        srv = runner_icon(0.95).move_to([4.2, sk.page.get_center()[1], 0])
        srv_t = label("server", 20, CLOUD).next_to(srv, DOWN, buff=0.15)
        arw = route(sk.page.get_right() + RIGHT * 0.1, srv.get_left() + LEFT * 0.12)
        curve2 = sk.curve_to(10)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(lr), FadeIn(title, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("in three parts")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in chips], lag_ratio=0.35), run_time=1.0)
            vo.wait_until("Its motivation")
            self.play(Indicate(chips[0].text, color=TURN, scale_factor=1.1),
                      chips[0].box.animate.set_stroke(TURN), run_time=0.6)
            self.play(Create(sk.page), FadeIn(sk.chrome), run_time=0.6)
            vo.wait_until("our reading of it")
            self.play(Create(sk.curve), run_time=0.9)
            self.play(Create(sk.now), FadeIn(sk.now_text), run_time=0.5)
            vo.wait_until("only useful when it runs somewhere")
            self.play(Create(arw), FadeIn(VGroup(srv, srv_t), shift=LEFT * 0.2), run_time=0.8)
            self.play(Transform(srv, runner_icon(0.95, lit=True).move_to(srv)), run_time=0.4)
            vo.wait_until("and stays current")
            self.play(VGroup(sk.now, sk.now_text).animate.shift(RIGHT * 0.72), Transform(sk.curve, curve2),
                      run_time=0.9)
        lecture = VGroup(title, chips, sk, srv, srv_t, arw)

        # ========================================================== 4. the honesty sentence
        lap = laptop_icon(2.2).move_to([-4.3, 0.55, 0])
        lap_t = label("this recording machine", 20, LAPTOP).next_to(lap, DOWN, buff=0.2)
        ok = VGroup(check_mark(0.34, PASS), label("ran right here", 22, PASS)).arrange(RIGHT, buff=0.15)
        ok.next_to(lap_t, DOWN, buff=0.35)
        aws = aws_box(box_w=3.3, box_h=1.7).move_to([0, 0.55, 0])
        first = err_chip("first real error", size=22).next_to(aws, DOWN, buff=0.35)
        con = console_drawing("IAM › Users", [("button", "Create user")])
        con.move_to([4.4, 0.45, 0])
        g_lap, g_aws = VGroup(lap, lap_t, ok), VGroup(aws, first)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(lr), FadeOut(lecture), run_time=0.6)
            self.remove(lr, lecture, *lecture.get_family())
            self.play(FadeIn(VGroup(lap, lap_t), shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Everything on the laptop")
            self.play(Create(ok[0]), FadeIn(ok[1], shift=RIGHT * 0.15), run_time=0.6)
            self.play(Indicate(ok[1], color=PASS, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Every command that talks to AWS")
            self.play(FadeIn(aws, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("up to its real first error")
            self.play(FadeIn(first, shift=UP * 0.15), run_time=0.4)
            self.play(Indicate(first.text, color=ERR, scale_factor=1.1), run_time=0.5)
            vo.wait_until("The consoles")
            self.play(FadeIn(VGroup(con.frame, con[1], con[2]), shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("marked illustration")
            self.play(FadeIn(con.tag, scale=1.2), run_time=0.4)
            flash_tag(self, con.tag, INK)
        honest = VGroup(g_lap, g_aws, con)

        # ========================================================== 5. what you need, how to read it
        needs = VGroup(*[grey_chip(s, size=24) for s, _ in NEEDS]).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        needs.move_to([-1.9, 0.0, 0])
        cost = cost_tag("this lecture runs a server until you delete it")
        cost.next_to(needs[1], DOWN, buff=0.12).align_to(needs[1], LEFT).shift(RIGHT * 0.4)
        needs[2].shift(DOWN * 0.45)
        corner = question_card(QUESTION, size=20)
        corner.move_to([6.6 - corner.width / 2, 3.6 - corner.height / 2, 0])
        tr = tracker_b(5)
        panel = code("src/deployment/inventory.yml", 1, 11, font_size=20, trim=70)
        panel.move_to([0, 0, 0])
        panel.shift(UP * (min(2.35, corner.get_bottom()[1] - 0.15) - panel.get_top()[1]))
        turn = your_turn().next_to(panel, DOWN, buff=0.2).align_to(panel, RIGHT)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(honest), Transform(card, corner), run_time=0.7)
            self.remove(honest, *honest.get_family())
            for c, (_, cue) in zip(needs, NEEDS):
                vo.wait_until(cue)
                self.play(FadeIn(c, shift=RIGHT * 0.2), run_time=0.45)
            vo.wait_until("This lecture runs a server")
            self.play(FadeIn(cost, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, cost, COST)
            vo.wait_until("The tracker names the README step")
            self.play(FadeOut(needs), FadeOut(cost), FadeIn(tr, shift=RIGHT * 0.2), run_time=0.6)
            self.remove(needs, cost)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06), run_time=0.6)
            self.play(fade_to(tr, 0.35), FadeIn(panel, shift=UP * 0.2), run_time=0.5)
            self.play(Circumscribe(panel.header, color=TURN, buff=0.06), run_time=0.6)
            vo.wait_until("and your turn means")
            self.play(fade_to(panel, 0.35), FadeIn(turn, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, turn, TURN)

        rest = VGroup(tr, panel, turn)
        self.play(FadeOut(rest), run_time=0.5)
        self.remove(rest, *rest.get_family())
        self.play(FadeOut(card), run_time=0.4)
        self.remove(card, *card.get_family())
        self.wait(0.3)
