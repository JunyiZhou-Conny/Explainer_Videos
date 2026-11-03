"""S02 · Three levers and a missing row (AC215 L13) — `LeversAndRecord`.

Beats (script.md, ## S02; one voiceover block each). No tracker; lref("5–6, 9–12") top right, whole scene.
0. Slide 5 redrawn: three GREY dials (More Data · Better/Faster Models · Faster Hardware, each with
   one GREY line of the slide's bullets). On "Today we pull the third one" the third needle swings
   and the dial lights YELLOW; on "bookkeeping" a small GREY ledger icon pops up beside it.
1. Slide 6 redrawn: the POC → Prototype → MVP arrow, phase lines, eight GREY bars; the dashed box
   around "Setup Experiment Tracking" + "Build Baseline Models" turns YELLOW with a "today" chip;
   a GREY Milestone 3 chip below.
2. Slide 10 redrawn: four rows snap into homes (code → GitHub · data → versioning · L11, DVC ·
   environment → pyproject.toml, uv.lock · weights, metrics, logs → a dashed slot with a RED "?").
   Slide 9's seven items build as a GREY checklist at the right + chip "→ the ledger's columns".
3. Slide 12 in one line at the bottom: YELLOW "W&B · hosted" · GREY "MLflow · self-host" · GREY
   chip "the milestone accepts an equivalent"; a BLUE W&B box catches the "?" row.
4. V1 (TrainingMap.at("S02"), all dark) builds lane by lane; each piece flashes as named, then dims
   (the CPU tile and the stream route appear for "Vertex AI runs it … reports to W and B", then
   leave). Caption "today we light both". Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, ERR, INK, NARRATION, SAY_COUNT, TURN, TrainingMap, grey_chip, label, lref, mono,
                    outline_box)
from explainer import style as S
from explainer.devops import chip

SAY = NARRATION["S02"]

LEVERS = (("More Data", "pipeline · labels · versions"),
          ("Better/Faster Models", "architectures · transfer learning"),
          ("Faster Hardware", "GPUs · TPUs · multi-GPU"))
PHASES = (("POC", -6.4, -2.1), ("Prototype", -2.1, 2.2), ("MVP", 2.2, 6.4))
ROADMAP = (("Design Cheese App", -6.3, 0.5), ("Data Collection", -6.3, -3.6),
           ("Setup Experiment Tracking", -4.6, -0.9), ("Build Baseline Models", -3.6, -0.4),
           ("Build Better Models", -0.6, 2.2), ("ML Workflow", 0.2, 2.4),
           ("Build Cheese App", 2.6, 6.3), ("Deployment, Scaling & Automation", 0.4, 6.3))
MILESTONE = "Milestone 3: experiment tracking + one serverless training run, logged and reproducible"
SEVEN = ("environment", "code", "data", "model", "metrics", "artifacts", "notes")


def lever_dial(title: str, sub: str, radius: float = 1.2) -> VGroup:
    """A GREY dial (half arc, ticks, a needle low on the left) with its title and one GREY line.
    .arc .ticks .needle .pivot .title .sub"""
    arc = Arc(radius=radius, start_angle=0, angle=PI, color=S.GREY, stroke_width=5)
    ticks = VGroup(*[Line(radius * 0.82 * np.array([np.cos(a), np.sin(a), 0]),
                          radius * 0.98 * np.array([np.cos(a), np.sin(a), 0]), color=S.GREY, stroke_width=3)
                     for a in np.linspace(0.12 * PI, 0.88 * PI, 5)])
    a0 = 0.82 * PI
    needle = Line(ORIGIN, radius * 0.75 * np.array([np.cos(a0), np.sin(a0), 0]), color=S.GREY, stroke_width=5)
    pivot = Dot(ORIGIN, radius=0.07, color=S.GREY)
    t = label(title, 24, INK).next_to(arc, DOWN, buff=0.3)
    s = label(sub, 20, S.GREY).next_to(t, DOWN, buff=0.14)
    g = VGroup(arc, ticks, needle, pivot, t, s)
    g.arc, g.ticks, g.needle, g.pivot, g.title, g.sub = arc, ticks, needle, pivot, t, s
    return g


def dimmed(d: VGroup) -> VGroup:
    """A copy of a lever dial pushed back: strokes and words at low opacity, no fills added."""
    c = d.copy()
    for m in (c.arc, c.ticks, c.needle):
        m.set_stroke(opacity=0.35)
    c.pivot.set_fill(opacity=0.35)
    c.title.set_opacity(0.4)
    c.sub.set_opacity(0.4)
    return c


def ledger_icon() -> VGroup:
    """A small GREY ledger: a sheet with a header rule, rows and a column line, plus a word."""
    sheet = RoundedRectangle(width=0.9, height=0.75, corner_radius=0.06, stroke_color=S.GREY,
                             stroke_width=3).set_fill(S.GREY_DARKER, 1)
    c = sheet.get_center()
    rows = VGroup(*[Line(c + np.array([-0.36, y, 0]), c + np.array([0.36, y, 0]), color=S.GREY,
                         stroke_width=2.5 if y > 0.15 else 1.5) for y in (0.2, 0.02, -0.14, -0.28)])
    col = Line(c + np.array([-0.05, 0.3, 0]), c + np.array([-0.05, -0.32, 0]), color=S.GREY, stroke_width=1.5)
    word = label("bookkeeping", 20, S.GREY).next_to(sheet, DOWN, buff=0.14)
    return VGroup(sheet, rows, col, word)


def road_bar(text: str, x0: float, x1: float, y: float) -> VGroup:
    """A roadmap bar from x0 to x1 (GREY, WHITE words). .box .text"""
    b = RoundedRectangle(width=x1 - x0, height=0.4, corner_radius=0.08, stroke_color=S.GREY,
                         stroke_width=2).set_fill(S.GREY_DARK, 0.6).move_to([(x0 + x1) / 2, y, 0])
    t = label(text, 20, INK).move_to(b)
    assert t.width < b.width - 0.1, text
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def home_box(content: Mobject, color=S.GREY, dashed: bool = False) -> VGroup:
    """A home in the 'where do we track what' table: an outlined box around `content`. .box .text"""
    ob = outline_box(max(content.width + 0.5, 1.1), 0.62, color, solid=not dashed, fill_opacity=0.1)
    ob.move_to(content)
    g = VGroup(ob, content)
    g.box, g.text = ob, content
    return g


class LeversAndRecord(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 5, len(SAY)
        ref = lref("5–6, 9–12")

        # ========================================================== 0. three levers (slide 5)
        dials = [lever_dial(t, s) for t, s in LEVERS]
        for d, x in zip(dials, (-4.6, -0.55, 3.5)):
            d.move_to([x, 0.2, 0])
        third = dials[2]
        piv = third.pivot.get_center()
        ledger = ledger_icon().move_to([5.75, 1.15, 0])
        lit_arc = third.arc.copy().set_stroke(TURN, 6)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), run_time=0.5)
            for d, anchor in zip(dials, ("more data", "better models", "and faster hardware")):
                vo.wait_until(anchor)
                self.play(FadeIn(d, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Today we pull the third one")
            self.play(Rotate(third.needle, angle=-0.62 * PI, about_point=piv),
                      third.needle.animate.set_color(TURN), third.pivot.animate.set_color(TURN),
                      Transform(third.arc, lit_arc), third.ticks.animate.set_color(TURN),
                      third.title.animate.set_color(TURN), run_time=1.0)
            vo.wait_until("you rent hardware")
            self.play(Indicate(third.title, color=TURN, scale_factor=1.08),
                      *[Transform(d, dimmed(d)) for d in dials[:2]], run_time=0.8)
            vo.wait_until("bookkeeping")
            self.play(FadeIn(ledger, scale=0.6, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("whether it helped")
            self.play(Wiggle(ledger[:3], scale_value=1.08), run_time=0.8)

        # ========================================================== 1. the roadmap (slide 6)
        arrow_body = Polygon([-6.4, 2.85, 0], [6.0, 2.85, 0], [6.45, 2.55, 0], [6.0, 2.25, 0], [-6.4, 2.25, 0],
                             stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        phase_words = VGroup(*[label(p, 24, INK).move_to([(a + b) / 2, 2.55, 0]) for p, a, b in PHASES])
        seps = VGroup(*[DashedLine([x, 2.2, 0], [x, -1.8, 0], dash_length=0.12, color=S.GREY_DARK, stroke_width=2)
                        for x in (-2.1, 2.2)])
        ys = [1.85 - 0.5 * i for i in range(len(ROADMAP))]
        bars = [road_bar(t, a, b, y) for (t, a, b), y in zip(ROADMAP, ys)]
        two = VGroup(bars[2], bars[3])
        tb = DashedVMobject(Rectangle(width=two.width + 0.3, height=two.height + 0.12).move_to(two),
                            num_dashes=40).set_stroke(S.GREY, 2.5)
        tb_lit = tb.copy().set_stroke(TURN, 3.5)
        today = chip("today", TURN, size=22).next_to(tb, LEFT, buff=0.15).align_to(tb, DOWN)
        mile = grey_chip(MILESTONE).move_to([0, -2.55, 0])
        road = VGroup(arrow_body, phase_words, seps, *bars, tb)

        with self.voiceover(SAY[1]) as vo:
            gone = VGroup(*dials, ledger)
            self.play(FadeOut(gone, shift=DOWN * 0.2), run_time=0.5)
            self.remove(*gone)
            self.play(FadeIn(arrow_body), FadeIn(phase_words), Create(seps), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.3) for b in bars], lag_ratio=0.12), run_time=1.2)
            vo.wait_until("the dashed box around")
            self.play(Create(tb), run_time=0.6)
            vo.wait_until("is today")
            self.play(Transform(tb, tb_lit), FadeIn(today, shift=RIGHT * 0.15),
                      *[b.box.animate.set_stroke(TURN) for b in (bars[2], bars[3])], run_time=0.6)
            vo.wait_until("Your third milestone")
            self.play(FadeIn(mile, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(mile.text, color=INK, scale_factor=1.03), run_time=0.8)

        # ========================================================== 2. where each piece goes (slides 10, 9)
        head = label("Where do we track what?", 26, S.GREY).move_to([-6.4, 2.55, 0], aligned_edge=LEFT)
        row_y = (1.55, 0.6, -0.35, -1.3)
        items = ("code", "data", "environment", "weights, metrics, logs")
        homes_c = (label("GitHub", 24, INK), label("versioning · L11, DVC", 24, INK),
                   mono("pyproject.toml, uv.lock", 22, INK), label("?", 32, ERR))
        rows = []
        for it, hc, y in zip(items, homes_c, row_y):
            t = label(it, 24, INK).move_to([-3.35, y, 0], aligned_edge=RIGHT)
            hc.move_to([-2.4, y, 0], aligned_edge=LEFT)
            h = home_box(hc, dashed=(it.startswith("weights")))
            h.shift(RIGHT * (-2.4 - h.box.get_left()[0]))
            a = Arrow(t.get_right(), h.box.get_left(), buff=0.12, color=S.GREY, stroke_width=3,
                      max_tip_length_to_length_ratio=0.3)
            rows.append((t, a, h))
        qh = rows[3][2]
        qh.box.frame.set_stroke(ERR)
        hang = DashedLine(rows[3][0].get_right() + RIGHT * 0.12, qh.box.get_left() + LEFT * 0.12, dash_length=0.1,
                          color=S.GREY, stroke_width=3)
        rows[3] = (rows[3][0], hang, qh)

        ck_head = label("a complete run keeps", 22, S.GREY)
        ck_items = [VGroup(Square(0.26, stroke_color=S.GREY, stroke_width=2.5), label(s, 22, INK))
                    .arrange(RIGHT, buff=0.2) for s in SEVEN]
        ck_body = VGroup(*ck_items).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        ck = VGroup(ck_head, ck_body).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        ck.move_to([3.4, 0.2, 0], aligned_edge=LEFT)
        ck_frame = RoundedRectangle(width=ck.width + 0.6, height=ck.height + 0.5, corner_radius=0.14,
                                    stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1).move_to(ck)
        cols_chip = grey_chip("→ the ledger's columns").next_to(ck_frame, DOWN, buff=0.2)

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(road, today, mile)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(*gone)
            self.play(FadeIn(head, shift=RIGHT * 0.2), run_time=0.5)
            for (t, a, h), anchor in zip(rows[:3], ("Code to GitHub", "data to the versioning",
                                                    "and the environment to")):
                vo.wait_until(anchor)
                self.play(FadeIn(t, shift=RIGHT * 0.3), run_time=0.35)
                self.play(GrowArrow(a), FadeIn(h, shift=LEFT * 0.3), run_time=0.45)
                self.play(Indicate(h.text, color=INK, scale_factor=1.06), run_time=0.4)
            vo.wait_until("Weights, metrics and logs")
            t, a, h = rows[3]
            self.play(FadeIn(t, shift=RIGHT * 0.3), run_time=0.4)
            self.play(Create(a), FadeIn(h.box), run_time=0.5)
            vo.wait_until("have no home yet")
            self.play(FadeIn(h.text, scale=1.5), run_time=0.5)
            self.play(Wiggle(h.text, scale_value=1.2), run_time=0.7)
            vo.wait_until("A complete run should keep")
            self.play(FadeIn(ck_frame), FadeIn(ck_head), run_time=0.5)
            for it, anchor in zip(ck_items, ("environment, code", "code, data", "data, model", "model, metrics",
                                             "metrics, artifacts", "artifacts and", "and notes")):
                vo.wait_until(anchor)
                self.play(FadeIn(it, shift=LEFT * 0.2), run_time=0.3)
            self.play(FadeIn(cols_chip, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 3. one tracker (slide 12)
        wb = chip("W&B · hosted", TURN, size=22)
        mlf = chip("MLflow · self-host", S.GREY, size=22)
        eq = grey_chip("the milestone accepts an equivalent")
        line = VGroup(wb, mlf, eq).arrange(RIGHT, buff=0.35).move_to([0, -2.85, 0])
        catch = home_box(label("W&B", 24, INK), CLOUD)
        catch.move_to(qh.box, aligned_edge=LEFT)
        solid = Arrow(rows[3][0].get_right(), catch.box.get_left(), buff=0.12, color=S.GREY, stroke_width=3,
                      max_tip_length_to_length_ratio=0.3)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(wb, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("W and B for short")
            self.play(Indicate(wb.text, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("which is hosted for you")
            self.play(FadeOut(qh), FadeOut(hang), ReplacementTransform(wb.copy(), catch),
                      run_time=0.9)
            self.play(GrowArrow(solid), run_time=0.4)
            vo.wait_until("MLflow is the usual choice")
            self.play(FadeIn(mlf, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("if you must host it yourself")
            self.play(FadeIn(eq, shift=UP * 0.2), run_time=0.6)

        # ========================================================== 4. the map, built dark (V1)
        m = TrainingMap.at("S02")
        P = m.parts
        colab = VGroup(*[P[k] for k in ("nbA", "laneA", "folder", "bucket", "nbB", "laneB", "wandb")])
        repo = VGroup(*[P[k] for k in ("laptop", "cockpit", "secrets", "gcp", "vertex")])
        cap = label("today we light both", 26, INK).move_to([0, -2.45, 0])

        with self.voiceover(SAY[4]) as vo:
            gone = Group(*[x for x in self.mobjects if x is not ref])
            self.play(FadeOut(gone), run_time=0.6)
            self.remove(*gone)
            vo.wait_until("On top, the Colab lane")
            self.play(FadeIn(colab, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("notebook A fills a folder")
            self.play(m.light("nbA", "laneA", "folder"), run_time=0.6)
            vo.wait_until("and uploads it")
            self.play(m.light("bucket"), run_time=0.5)
            vo.wait_until("and notebook B streams")
            self.play(m.unlight("nbA", "laneA", "folder", "bucket"), m.light("nbB", "laneB", "wandb"), run_time=0.7)
            vo.wait_until("Below, the repo lane")
            self.play(m.unlight("nbB", "laneB", "wandb"), FadeIn(repo, shift=UP * 0.15), run_time=0.8)
            self.remove(colab, repo)
            self.add(m)
            vo.wait_until("your laptop packs the code")
            self.play(m.light("laptop", "cockpit"), run_time=0.6)
            vo.wait_until("a bucket holds it")
            self.play(m.unlight("laptop", "cockpit"), m.light("gcp", "bucket"), run_time=0.6)
            vo.wait_until("Vertex AI runs it")
            self.play(m.unlight("bucket"), m.light("vertex"), m.reveal("cpu_tile"), run_time=0.7)
            vo.wait_until("and the run reports to W and B")
            self.play(m.reveal("stream"), m.light("wandb"), run_time=0.8)
            vo.wait_until("Today we light both")
            self.play(m.conceal("cpu_tile", "stream"), m.unlight("gcp", "vertex", "wandb"),
                      FadeIn(cap, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(cap, color=TURN, scale_factor=1.05), run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
