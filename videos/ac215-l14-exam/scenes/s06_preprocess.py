"""S06 · Where preprocessing lives (AC215 L14 exam edition). Lecture: 15 · 11, 13.

Beats (script.md "## S06", one voiceover block each):
0. The exam map (slots 1-4 filled) fades in, slot 5 activates ("5 · the model endpoint") and pulses;
   lref(15, "11"). A dashed BLUE Cloud Run instance at the right morphs into V5's BLUE "Vertex AI
   endpoint" box at "the next lecture uses". At "Picture two clients" the GREY phone app writes in,
   at "and a web page" the web page.
1. lref(15, "13"). V5: each client gets its GREEN gear; at "decode the JPEG" / "scale the pixels" /
   "and resize" the three GREEN recipe chips write in, one by one, in a row above the phone's gear
   (a GREEN dashed link to the gear; the web page's gear stays unlabelled). At "Only then" a PINK
   arrow grows from each gear with its "float tensor" chip; the answer bubbles appear GREEN. At "That
   is two copies" both gears are circled.
2. At "The lecture calls this" the GRAY lecture chip "client-side brittleness" · slide 13. At
   "Every client preprocesses" the web page's gear turns RED and the RED chip "resize: crop first"
   sits under it. At "quietly receives another" its tensor chip turns RED and travels along the
   arrow into the endpoint; the web page's answer bubble turns RED.
3. At "Now move the gear" both gears fly into the endpoint and become one GREEN gear; the arrows
   now carry PINK {"b64": "…"} chips; the recipe, the RED chip and the slide chip leave. At
   "Clients send raw JPEG bytes" the excerpt chip model-deployment/README.md · line 191 (the full
   {"bytes_inputs": {"b64": "<base64-encoded JPEG>"}} line). At "The preprocessing travels" the
   clients dim and CODE(model-deployment/README.md: 60) (wrapped at 50) covers them, with
   "The preprocessing travels … used in training." lit YELLOW; the endpoint's gear pulses.
4. CODE(cli.py: 249–253, 255 folded) at the lower right (lines 250–253, the base64 `instances`
   list, lit PINK; 255 `endpoint.predict(instances=instances)` lit YELLOW). The phone and its
   arrow stay bright; at "No resizing" the GRAY chip "no resize · no normalize" by the phone; at
   "That is a thin client" the phone's b64 chip pulses.
5. The panel goes; everything comes back. At "Now ship" the version dial "v1" appears under the
   endpoint's model; it turns to "v2": the endpoint gear turns RED with a RED "bad resize" chip
   above the endpoint, and both answer bubbles turn RED at the same instant ("Both clients
   break"). At "Roll back" it turns back to "v1": both healthy at once with a YELLOW flash. At
   "One deployment" the GRAY chip "one deployment · no client release".
6. Replay, labelled with the GRAY chip "replay · preprocessing on the clients": the gears return
   to the clients, the endpoint gear goes and the dial grays out. PONDER(6 s, "Gears on the
   clients: what does one rollback cost?") in the lower third.
7. The card goes. The piece fades while the two client gears become the stubs of two GREY release
   bars on a day axis: at "a phone update" the bar "phone app · app-store review" grows to day 10;
   at "and a web deploy" the bar "web deploy" ends at day 1; at "They land" both ends flash; at
   "in between" a RED band "clients disagree" spans the two ends.
8. RULE line 1 at "The rule"; the two bar labels pulse at "several clients", "clients disagree"
   at "and no client release" (row 1 pulses at "put preprocessing at the endpoint"), line 2 at
   "Preprocessing on the clients" (both release bars pulse at "in lockstep"). The timeline and
   the tag leave, the card shrinks into map slot 5 (half-filled: the gear); empty frame.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AnimationGroup,
    Circumscribe,
    DashedLine,
    FadeIn,
    FadeOut,
    Flash,
    GrowArrow,
    Indicate,
    Line,
    Rectangle,
    ReplacementTransform,
    SurroundingRectangle,
    Transform,
    VGroup,
)

from explainer import style as S
from explainer.components import timeline
from explainer.scene import VoiceScene

from common import (
    CAPTION,
    CLOUD,
    ERR,
    NARRATION,
    OWN,
    ROUTE,
    SAFE_X,
    SAFE_Y,
    TURN,
    ExamMap,
    RuleCard,
    _appear,
    _save_op,
    _set_op,
    chip,
    dim,
    excerpt_chip,
    guard,
    instance_box,
    lref,
    lref_swap,
    ponder_at,
    sans,
    source_line,
    src_panel,
    undim,
)
from common import ThinClients as ClientsPiece

SAY = NARRATION["S06"]

# ------------------------------------------------------------------ the real sources (checked)
README = "model-deployment/README.md"
CLI = "cli.py"                                   # = model-deployment/cli.py
TRAVELS = ("The preprocessing travels with the model, so every client gets exactly the same "
           "preprocessing that was used in training.")
assert TRAVELS in source_line(README, 60)
L191 = source_line(README, 191).strip()
assert L191 == '{"bytes_inputs": {"b64": "<base64-encoded JPEG>"}}', L191
assert "instances = [" in source_line(CLI, 250)
assert '{"bytes_inputs": {"b64": base64.b64encode(image).decode("utf-8")}}' in source_line(CLI, 251)
assert "endpoint.predict(instances=instances)" in source_line(CLI, 255)
assert "load_sample_images()" in source_line(CLI, 249)
CLI_LINES = [249, 250, 251, 252, 253, 255]       # 245-248 are comments: 245-255 cannot fit 12 rows

SLIDE13 = "client-side brittleness"              # Lecture 15, slide 13 ("Client-side brittleness")

RULE_TOP = "several clients · update or roll back once · no client release → preprocessing at the endpoint"
RULE_BOTTOM = "on the clients → every client re-released in lockstep"

TOP_BAND = 2.55          # content stays below the active slot's label
BOTTOM_Y = -2.6          # the chip row under the piece (the piece ends at y -1.9)


def inside_frame(*mobs):
    for m in mobs:
        guard(m.get_left()[0] >= -SAFE_X - 1e-6 and m.get_right()[0] <= SAFE_X + 1e-6,
              f"x out of frame: {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f}")
        guard(m.get_bottom()[1] >= -SAFE_Y - 1e-6 and m.get_top()[1] <= SAFE_Y + 1e-6,
              f"y out of frame: {m.get_bottom()[1]:.2f}..{m.get_top()[1]:.2f}")


def below_band(*mobs):
    for m in mobs:
        guard(m.get_top()[1] <= TOP_BAND + 1e-6, f"reaches the map's label: top {m.get_top()[1]:.2f}")


def apart(a, b, gap: float = 0.05):
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    guard(sep, f"overlap: {a.get_corner(DOWN + LEFT)} {a.get_corner(UP + RIGHT)} / "
               f"{b.get_corner(DOWN + LEFT)} {b.get_corner(UP + RIGHT)}")


def hide_now(piece, *names):
    """Start these shown-by-default parts of a set piece invisible (revealed later with parts_in)."""
    for n in names:
        m = piece.parts[n]
        _save_op(m)
        _set_op(m, 0)
        piece._flag(m, True)


def show_now(piece, name):
    """A hidden part back at its saved opacities, in this frame (after a morph drew it)."""
    m = piece.parts[name]
    _set_op(m)
    piece._flag(m, False)


def lit_spans(panel, n, sentence):
    """Glyph groups of `sentence` in file line n of a wrapped panel (it may run over several rows)."""
    words = sentence.split()
    out, i = [], 0
    for k in panel.rows_of[n] if isinstance(panel.rows_of, dict) else panel.rows_of(n):
        if i >= len(words):
            break
        best = None
        for j in range(len(words), i, -1):
            try:
                best = (j, panel.span(n, " ".join(words[i:j])))
                break
            except ValueError:
                continue
        if best is not None:
            i, g = best
            out.append(g)
    assert i == len(words), f"lit_spans: only {i} of {len(words)} words found"
    return out


def gray_chip(text):
    return chip(text, S.GREY, size=CAPTION)


class ThinClients(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, len(SAY)

        # ========================================================== 0. the endpoint and two clients
        m = ExamMap(filled=(1, 2, 3, 4))
        tc = ClientsPiece()
        hide_now(tc, "phone", "web", "endpoint", "arrow0", "arrow1")
        ep = tc.parts["endpoint"]
        inst = VGroup(instance_box(2.2, 1.4), sans("Cloud Run", CAPTION, CLOUD))
        inst.arrange(DOWN, buff=0.15).move_to(ep.get_center())
        ep_copy = ep.copy()
        _set_op(ep_copy)                          # the endpoint as it will look (for the morph)
        lr = lref(15, "11")
        inside_frame(tc, inst, lr)
        below_band(tc)
        with self.voiceover(SAY[0]) as vo:
            self.add(tc)
            self.play(FadeIn(m), run_time=0.6)
            self.play(*m.activate(5), FadeIn(inst, shift=UP * 0.1), FadeIn(lr), run_time=0.7)
            vo.wait_until("the next lecture uses")
            self.play(ReplacementTransform(inst, ep_copy), run_time=1.0)
            self.remove(ep_copy)
            show_now(tc, "endpoint")
            vo.wait_until("and the quiz asks")
            self.play(m.pulse(5), Indicate(ep, color=TURN, scale_factor=1.03), run_time=0.8)
            vo.wait_until("Picture two clients")
            self.play(*tc.parts_in("phone"), run_time=0.6)
            vo.wait_until("and a web page")
            self.play(*tc.parts_in("web"), run_time=vo.remaining(0.6))

        # ========================================================== 1. the same gear, twice
        rec = tc.parts["recipe"]
        g0, g1 = tc.parts["gear0"], tc.parts["gear1"]
        link = DashedLine(g0.get_top() + UP * 0.04, [g0.get_center()[0], rec.get_bottom()[1] - 0.04, 0],
                          color=OWN, stroke_width=2.5, dash_length=0.08)
        guard(rec.get_bottom()[1] - g0.get_top()[1] > 0.3, "recipe row sits on the phone's gear")
        with self.voiceover(SAY[1]) as vo:
            lr = lref_swap(self, lr, 15, "13")
            vo.wait_until("Each client carries")
            self.play(*tc.parts_in("gear0", "gear1"), run_time=0.6)
            tc._flag(rec, False)
            vo.wait_until("decode the JPEG")
            self.play(_appear(rec[0]), FadeIn(link), run_time=0.5)
            vo.wait_until("scale the pixels")
            self.play(_appear(rec[1]), run_time=0.5)
            vo.wait_until("and resize")
            self.play(_appear(rec[2]), run_time=0.5)
            vo.wait_until("Only then")
            self.play(*tc.parts_in("arrow0", "arrow1", anim=GrowArrow), run_time=0.8)
            self.play(*tc.parts_in("chip0", "chip1"), *tc.answers(OWN), run_time=0.6)
            vo.wait_until("That is two copies")
            self.play(Circumscribe(g0, color=TURN, buff=0.06), Circumscribe(g1, color=TURN, buff=0.06),
                      run_time=0.9)
            vo.wait_until("in two code bases")
            self.play(Indicate(tc.parts["phone"], color=TURN, scale_factor=1.05),
                      Indicate(tc.parts["web"], color=TURN, scale_factor=1.05), run_time=vo.remaining(0.8))

        # ========================================================== 2. client-side brittleness
        s13 = gray_chip(f"“{SLIDE13}” · slide 13").move_to([0.4, BOTTOM_Y - 0.35, 0])
        crop = chip("resize: crop first", ERR, size=CAPTION)
        crop.move_to([g1.get_left()[0] + crop.width / 2, g1.get_bottom()[1] - 0.12 - crop.height / 2, 0])
        c1 = tc.parts["chip1"]
        c1_home = c1.get_center().copy()
        arrow1 = tc.parts["arrow1"]
        c1_end = arrow1.get_end() + LEFT * (c1.width / 2 + 0.15) + UP * 0.32
        inside_frame(s13, crop)
        apart(s13, crop, 0.08)
        apart(crop, tc.parts["web"], 0.05)
        apart(s13, tc, 0.05)
        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("The lecture calls this")
            self.play(FadeIn(s13, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Every client preprocesses")
            self.play(g1.animate.set_stroke(ERR), FadeIn(crop, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("and a model trained")
            self.play(Indicate(rec, color=OWN, scale_factor=1.04), run_time=0.8)
            vo.wait_until("quietly receives another")
            self.play(c1.box.animate.set_stroke(ERR), run_time=0.3)
            self.play(c1.animate.move_to(c1_end), run_time=1.0)
            self.play(*tc.answers(ERR, (1,)), Indicate(tc.parts["ans1"], color=ERR), run_time=vo.remaining(0.6))

        # ========================================================== 3. the gear moves into the endpoint
        e191 = excerpt_chip(L191, f"{README} · line 191", line=source_line(README, 191))
        e191.move_to([0, BOTTOM_Y - 0.25, 0])
        p60 = src_panel(README, 60, size=20, wrap_at=50)
        p60.move_to([-6.45 + p60.width / 2, -0.2, 0])
        lit = lit_spans(p60, 60, TRAVELS)
        lit_bg = VGroup(*[SurroundingRectangle(g, buff=0.04, stroke_width=0).set_fill(TURN, 0.22) for g in lit])
        inside_frame(e191, p60)
        below_band(p60)
        apart(e191, tc, 0.05)
        apart(p60, tc.parts["endpoint"], 0.08)
        side3 = ("phone", "web", "arrow0", "arrow1", "b64_0", "b64_1", "ans0", "ans1")
        with self.voiceover(SAY[3]) as vo:
            vo.wait_until("Now move the gear")
            self.play(FadeOut(VGroup(crop, s13, link)), *tc.parts_out("recipe"), run_time=0.5)
            self.play(*tc.to_endpoint(), run_time=1.5)
            c1.move_to(c1_home).box.set_stroke(ROUTE)     # (hidden now; the replay brings it home)
            vo.wait_until("Clients send raw JPEG bytes")
            self.play(FadeIn(e191, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(tc.parts["b64_0"], color=TURN), Indicate(tc.parts["b64_1"], color=TURN),
                      run_time=0.8)
            vo.wait_until("The preprocessing travels")
            self.play(FadeOut(e191), *[dim(tc.parts[n], 0.15) for n in side3], run_time=0.5)
            self.play(FadeIn(p60, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("so every client gets")
            self.play(FadeIn(lit_bg), *[g.animate.set_color(TURN) for g in lit], run_time=0.6)
            self.play(Circumscribe(tc.parts["egear"], color=TURN, buff=0.08), run_time=vo.remaining(0.8))

        # ========================================================== 4. the repo's thin client
        pcl = src_panel(CLI, CLI_LINES, size=20, wrap_at=50)
        pcl.move_to([6.45 - pcl.width / 2, -3.55 + pcl.height / 2, 0])
        b_pink = pcl.bar(250, ROUTE, 0.22)
        for n in (251, 252, 253):
            b_pink.add(*pcl.bar(n, ROUTE, 0.22))
        b_pred = pcl.bar(255, TURN, 0.22)
        b_read = pcl.bar(249, S.GREY, 0.25)
        thin = gray_chip("no resize · no normalize")
        thin.move_to([tc.parts["ans0"].get_right()[0] + 0.2 + thin.width / 2, tc.parts["ans0"].get_center()[1], 0])
        inside_frame(pcl, thin)
        below_band(thin)
        apart(pcl, tc.parts["phone"], 0.1)
        apart(pcl, tc.parts["arrow0"], 0.05)
        apart(thin, tc.parts["arrow0"], 0.05)
        apart(thin, tc.parts["b64_0"], 0.05)
        apart(thin, pcl, 0.05)
        side4 = ("endpoint", "egear")
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p60, lit_bg)), *[dim(tc.parts[n], 0.15) for n in side4],
                      *[undim(tc.parts[n]) for n in ("phone", "arrow0", "b64_0", "ans0")], run_time=0.6)
            self.play(FadeIn(pcl, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("It reads the image files")
            self.play(FadeIn(b_read), run_time=0.4)
            vo.wait_until("base64 encodes them")
            self.play(FadeIn(b_pink), run_time=0.6)
            vo.wait_until("and calls predict")
            self.play(FadeIn(b_pred), run_time=0.5)
            vo.wait_until("No resizing")
            self.play(FadeIn(thin, shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("That is a thin client")
            self.play(Indicate(tc.parts["phone"], color=TURN, scale_factor=1.06),
                      Indicate(tc.parts["b64_0"], color=TURN), run_time=vo.remaining(0.8))

        # ========================================================== 5. one deployment, every client
        bad = chip("bad resize", ERR, size=CAPTION)
        bad.move_to([tc.ep.get_center()[0], tc.ep.get_top()[1] + 0.15 + bad.height / 2, 0])
        one = gray_chip("one deployment · no client release").move_to([0, BOTTOM_Y, 0])
        inside_frame(bad, one)
        below_band(bad)
        apart(one, tc, 0.05)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(pcl, b_read, b_pink, b_pred, thin)),
                      *[undim(tc.parts[n]) for n in ("web", "arrow1", "b64_1", "ans1", *side4)], run_time=0.6)
            vo.wait_until("Now ship")
            self.play(*tc.parts_in("dial"), run_time=0.5)
            vo.wait_until("in version 2")
            self.play(*tc.set_version("v2", bad=True), FadeIn(bad, shift=DOWN * 0.1), run_time=0.8)
            vo.wait_until("Both clients break")
            self.play(Indicate(tc.parts["ans0"], color=ERR), Indicate(tc.parts["ans1"], color=ERR), run_time=0.7)
            vo.wait_until("Roll back")
            self.play(*tc.set_version("v1"), FadeOut(bad), run_time=1.2)
            vo.wait_until("One deployment")
            self.play(FadeIn(one, shift=UP * 0.1), Circumscribe(tc.ep, color=TURN, buff=0.06),
                      run_time=vo.remaining(0.8))

        # ========================================================== 6. replay: gears on the clients
        replay = gray_chip("replay · preprocessing on the clients")
        replay.move_to([-0.6, 2.15, 0])
        inside_frame(replay)
        below_band(replay)
        apart(replay, tc.parts["ans0"], 0.1)
        apart(replay, tc.parts["endpoint"], 0.1)
        apart(replay, tc.parts["chip0"], 0.1)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(one), FadeIn(replay, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Now put the gears back")
            self.play(*tc.to_clients(), run_time=1.2)
            vo.wait_until("What does the same rollback cost")
            self.play(Indicate(g0, color=TURN), Indicate(g1, color=TURN), run_time=vo.remaining(0.8))
        card = ponder_at(self, "Gears on the clients: what does one rollback cost?", 6, y=-2.8)
        apart(card, tc.parts["web"], 0.02)

        # ========================================================== 7. two releases on a day axis
        ax = timeline(0, 14, width=7.0, step=7).move_to([2.2, -0.45, 0])
        days = sans("days", CAPTION, S.GREY).next_to(ax[0], RIGHT, buff=0.15)

        def x_at(d):
            return ax.year_to_point(d)[0]

        def bar(d1, y):
            return Rectangle(width=x_at(d1) - x_at(0), height=0.36, stroke_color=S.GREY, stroke_width=2.5) \
                .set_fill(S.GREY, 0.45).move_to([(x_at(0) + x_at(d1)) / 2, y, 0])

        PH_END, WEB_END = 10, 1
        bars = VGroup(bar(PH_END, 0.95), bar(WEB_END, 0.3))
        stubs = VGroup(*[b.copy().stretch_to_fit_width(0.12, about_edge=LEFT) for b in bars])
        labs = VGroup(sans("phone app · app-store review", CAPTION, S.GREY), sans("web deploy", CAPTION, S.GREY))
        for lb, b in zip(labs, bars):
            lb.move_to([x_at(0) - 0.25 - lb.width / 2, b.get_center()[1], 0])
        band = Rectangle(width=x_at(PH_END) - x_at(WEB_END), height=1.15, stroke_color=ERR, stroke_width=2) \
            .set_fill(ERR, 0.18).move_to([(x_at(WEB_END) + x_at(PH_END)) / 2, 0.62, 0])
        band_lab = sans("clients disagree", CAPTION, ERR).next_to(band, UP, buff=0.12)
        ends = VGroup(*[Line(b.get_corner(UP + RIGHT) + UP * 0.1, b.get_corner(DOWN + RIGHT) + DOWN * 0.1,
                             color=TURN, stroke_width=5) for b in bars])
        tl = VGroup(ax, days, bars, labs, band, band_lab)
        inside_frame(tl)
        below_band(tl)
        apart(labs[0], bars[0], 0.1)
        rule = RuleCard(RULE_TOP, RULE_BOTTOM)
        inside_frame(rule)
        apart(tl, rule, 0.08)
        with self.voiceover(SAY[7]) as vo:
            gcopies = VGroup(g0.copy(), g1.copy())
            self.add(gcopies)
            self.play(FadeOut(card), FadeOut(replay), FadeOut(tc), FadeIn(ax), FadeIn(days),
                      ReplacementTransform(gcopies[0], stubs[0]), ReplacementTransform(gcopies[1], stubs[1]),
                      run_time=1.0)
            vo.wait_until("a phone update")
            self.play(FadeIn(labs[0], shift=RIGHT * 0.1), Transform(stubs[0], bars[0]), run_time=2.0)
            vo.wait_until("and a web deploy")
            self.play(FadeIn(labs[1], shift=RIGHT * 0.1), Transform(stubs[1], bars[1]), run_time=0.7)
            vo.wait_until("They land at different times")
            self.play(FadeIn(ends), Flash(ends[1].get_center(), color=TURN), Flash(ends[0].get_center(), color=TURN),
                      run_time=0.8)
            vo.wait_until("in between")
            self.play(FadeIn(band), FadeIn(band_lab, shift=DOWN * 0.1), run_time=vo.remaining(0.8))

        # ========================================================== 8. the rule -> map slot 5 (half)
        with self.voiceover(SAY[8]) as vo:
            vo.wait_until("The rule")
            self.play(rule.frame_in(), run_time=0.4)
            self.play(rule.line_in(0), run_time=0.6)
            vo.wait_until("several clients")
            self.play(Indicate(labs, color=TURN, scale_factor=1.05), run_time=0.7)
            vo.wait_until("and no client release")
            self.play(Indicate(band_lab, color=ERR, scale_factor=1.08), run_time=0.7)
            vo.wait_until("put preprocessing at the endpoint")
            self.play(Indicate(rule.rows[0], color=TURN, scale_factor=1.03), run_time=0.8)
            vo.wait_until("Preprocessing on the clients")
            self.play(rule.line_in(1), run_time=0.6)
            vo.wait_until("in lockstep")
            self.play(Indicate(stubs, color=TURN, scale_factor=1.04), run_time=vo.remaining(0.7))
        self.wait(0.5)
        self.play(FadeOut(VGroup(ax, days, stubs, labs, ends, band, band_lab, lr)), run_time=0.5)
        rule.shrink_into(self, m, 5, frac=0.5)
        self.play(m.pulse(5), run_time=0.7)
        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
        self.wait(0.3)
