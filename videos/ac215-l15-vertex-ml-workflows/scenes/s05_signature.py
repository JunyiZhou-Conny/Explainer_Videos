"""S05 · Where does preprocessing live? (README A › Run Container, step 5 stays lit and dim: a
concept beat with one extra check; the V3 TwoPipes set piece; lecture slides 13 and 14 redrawn).

Beats (script.md "## S05", one voiceover block each):
 0  TRACKER A2 5, dim. LECTURE 15 · 13: the question "where does preprocessing happen?"; left a
    GREY notebook whose three cells (resize, normalize, predict) light one by one; right a BLUE
    endpoint: a JPEG goes in, one answer (four bars) comes out, chip "one request". The picture
    and its lecture tag leave together.
 1  V3 TwoPipes, left pipe (piece anchored 1.2 up): the client zone and photo; CODE(cli.py:
    219-225) under it at 20 pt. "opens the photo" lights line 221; the resize gear arrives with line
    222; the ÷ 255 gear with line 223 and the photo becomes the 224 × 224 × 3 cube; on "sends" the
    wire and the endpoint appear, the cube rides to the door, line 225 PINK.
 2  TRACKER A2 5 · extra (undimmed). The code leaves; a 4-row strip (20 pt) types laptop/43's
    command (cut) -> TERM(laptop/43: 13-15, 18-20); DT_FLOAT and (-1, 224, 224, 3) YELLOW, then
    (-1, 4) GREEN. The door gets its label inputs['input'] · floats (-1, 224, 224, 3); four bars
    come out of the back. "your side of the wire": the client zone flashes.
 3  LECTURE 15 · 13. The strip leaves, the tracker dims. Under the pipe: the three client cards
    (web app / phone app no ÷ 255 RED / notebook another resize) and the label
    "client-side brittleness". The phone's cube rides into the door and the bars turn RED (one
    tall, confident wrong bar). A GREEN "one copy in the model" chip with two arrows "roll back" and
    "version". Cards, label, chips and the lecture tag leave together.
 4  LECTURE 15 · 14. Right pipe, picture only, GREY chip "part 2 · task.py": the gears cross the
    wire into the endpoint (decode_jpeg → float32 → resize, serving_default over it); callout 1
    "define preprocessing"; the three operations light in turn.
 5  LECTURE 15 · 14 (held). The cube becomes a stack of three JPEGs that rides the wire into the
    door (callout 2 "new signature: a batch of strings"); the gears turn; callout 3 "save as serving
    default" with serving_default flashing GREEN; "JPEG bytes" flashes and three dashed '?' bars
    come out (the class count is S12's fix A).
 6  The picture and its lecture tag leave. README card (README.md · line 115, chip A); under it
    GREEN "format change ✓" and GREY-struck "signature change". Fade to an empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S05"]
SIZE = 20                                     # terminal font: 72 characters a row
DIM = 0.35                                    # the tracker in concept beats

# ------------------------------------------------------------------ the real sources (checked)
C43 = capture("43")
assert C43.cmd.startswith("docker run --rm --entrypoint pipenv") and "saved_model_cli show" in C43.cmd
assert C43.cmd.endswith("--signature_def serving_default")
OUT43A = C43.at((13, 15))
OUT43B = C43.at((18, 20))
assert OUT43A[0].strip() == "inputs['input'] tensor_info:" and OUT43A[1].strip() == "dtype: DT_FLOAT"
assert OUT43A[2].strip() == "shape: (-1, 224, 224, 3)"
assert OUT43B[0].strip() == "outputs['output_0'] tensor_info:" and OUT43B[2].strip() == "shape: (-1, 4)"
CLI = excerpt("A/cli.py", 219, 225).split("\n")
assert "Image.open(img_path)" in CLI[2] and '.resize((224, 224))' in CLI[3] and "/ 255.0" in CLI[4]
assert CLI[6].strip() == 'payload = {"instances": [arr.tolist()]}'
README115 = readme(115, "A")
assert README115 == "2. Prepare the model in TensorFlow SavedModel format", README115


def fixed_tracker(key: str, step: int, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (common.py's head arrange() centres
    it at y 0; the same workaround as S01, S03 and S04)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def opacities(m) -> list:
    """(member, fill, stroke) opacities of `m` at full strength: set_opacity() would light up the
    tracker's invisible strut (steady() text), so dimming scales each member's own opacity."""
    return [(sm, sm.get_fill_opacity(), sm.get_stroke_opacity()) for sm in m.family_members_with_points()]


def scale_opacity(base, k: float):
    for sm, fo, so in base:
        sm.set_fill(opacity=fo * k)
        sm.set_stroke(opacity=so * k)


def dim_anim(m, base, k0: float, k1: float):
    """ANIM: `m` goes from k0 to k1 times its full-strength opacities."""
    return UpdateFromAlphaFunc(m, lambda _, a: scale_opacity(base, k0 + (k1 - k0) * a))


def nb_cell(n: int, text: str) -> VGroup:
    """One notebook cell: a GREY '[n]' and a rounded cell with a word in it. .num .box .text"""
    num = mono(f"[{n}]", 20, S.GREY)
    bx = RoundedRectangle(width=3.4, height=0.62, corner_radius=0.08, stroke_color=LAPTOP,
                          stroke_width=2).set_fill(S.GREY_DARKER, 1)
    t = label(text, 22, INK).move_to(bx).align_to(bx, LEFT).shift(RIGHT * 0.25)
    c = VGroup(bx, t)
    g = VGroup(num, c).arrange(RIGHT, buff=0.2)
    g.num, g.box, g.text = num, bx, t
    return g


def callout(n: int, text: str, color) -> VGroup:
    """Slide 14's numbered call-outs, redrawn: a circled number in `color` and a short label."""
    c = Circle(radius=0.21, stroke_color=color, stroke_width=3).set_fill(S.BG, 1)
    d = label(str(n), 20, color).move_to(c)
    t = label(text, 22, INK)
    return VGroup(VGroup(c, d), t).arrange(RIGHT, buff=0.2)


class FrontDoor(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S05"] == 7, len(SAY)
        self.bar_tags = []

        # ========================================================== 0. slide 13: notebook vs endpoint
        tr = fixed_tracker("A2", 5)
        base = opacities(tr)
        scale_opacity(base, DIM)
        ref13 = lref("13")
        q = label("where does preprocessing happen?", 28, TURN).move_to([0, 2.25, 0])
        assert q.get_left()[0] > tr.get_right()[0] - 0.1 or q.get_top()[1] < tr.get_bottom()[1] - 0.1
        nb_fr = outline_box(5.0, 3.15, LAPTOP, solid=True, fill_opacity=0.05).move_to([-3.6, -0.55, 0])
        nb_h = label("notebook", 22, LAPTOP).move_to(nb_fr.get_corner(UL) + np.array([0.25, -0.32, 0]),
                                                       aligned_edge=LEFT)
        cells = [nb_cell(i + 1, s) for i, s in enumerate(("resize", "normalize", "predict"))]
        VGroup(*cells).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(nb_fr).shift(DOWN * 0.25)
        nb = VGroup(nb_fr, nb_h, *cells)
        ep_fr = RoundedRectangle(width=2.6, height=2.1, corner_radius=0.14, stroke_color=CLOUD,
                                 stroke_width=3).set_fill(CLOUD, 0.1).move_to([3.4, -0.55, 0])
        ep_t = label("endpoint", 22, CLOUD).move_to(ep_fr.get_top() + DOWN * 0.32)
        ep_g = gear(0.22, CLOUD).move_to(ep_fr.get_center() + DOWN * 0.2)
        ep0 = VGroup(ep_fr, ep_t, ep_g)
        jpg = file_icon(None, INK, h=0.5).move_to([0.75, -0.55, 0])
        jpg_l = mono("photo.jpg", 20, INK).next_to(jpg, DOWN, buff=0.12)
        ans = bars((0.1, 0.75, 0.1, 0.05), 0.16, 0.9, OWN).move_to([5.75, -0.55, 0])
        one = chip("one request", ROUTE, size=20).next_to(ep_fr, DOWN, buff=0.3)
        assert ans.get_right()[0] < 6.55 and one.get_bottom()[1] > -3.5 and nb_fr.get_bottom()[1] > -3.5

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(ref13, shift=LEFT * 0.1), run_time=0.6)
            self.play(Write(q), run_time=1.0)
            vo.wait_until("where does preprocessing happen")
            self.play(Indicate(q, color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("In a notebook")
            self.play(FadeIn(nb_fr), FadeIn(nb_h), LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in cells],
                                                               lag_ratio=0.3), run_time=0.9)
            vo.wait_until("you resize")
            for c in cells[:2]:
                self.play(c.box.animate.set_fill(TURN, 0.25), c.num.animate.set_color(TURN), run_time=0.45)
                self.play(c.box.animate.set_fill(S.GREY_DARKER, 1), run_time=0.3)
            vo.wait_until("cell by cell")
            self.play(cells[2].box.animate.set_fill(TURN, 0.25), cells[2].num.animate.set_color(TURN), run_time=0.45)
            self.play(cells[2].box.animate.set_fill(S.GREY_DARKER, 1), run_time=0.3)
            vo.wait_until("A production endpoint")
            self.play(FadeIn(ep0, shift=LEFT * 0.2), FadeIn(jpg), FadeIn(jpg_l), run_time=0.7)
            vo.wait_until("take the raw photo")
            self.play(FadeOut(jpg_l), jpg.animate.scale(0.6).move_to(ep_fr.get_left() + RIGHT * 0.35), run_time=0.9)
            self.play(FadeOut(jpg), Rotate(ep_g, PI), run_time=0.5)
            vo.wait_until("and do all of that itself")
            self.play(Rotate(ep_g, PI), LaggedStart(*[GrowFromEdge(b, DOWN) for b in ans], lag_ratio=0.2),
                      run_time=0.9)
            self.play(FadeIn(one, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(one, color=ROUTE, scale_factor=1.08), run_time=0.6)

        # ========================================================== 1. V3 left pipe: the client does it
        v = TwoPipes().shift(UP * 1.2)
        # TwoPipes(built=False) builds its parts at ORIGIN in __init__ but holds only its anchor
        # until each part is shown, so shift() moved the anchor alone: move the unshown parts too.
        for m in (v.zone, v.photo, *v.gear_list, *v.gear_labels, v.cube_g, v.wire, v.ep, v.door):
            m.shift(UP * 1.2)
        p1 = code("A/cli.py", 219, 225, font_size=20)
        p1.move_to([0, -0.3 - p1.height / 2, 0])
        b221 = line_bar(p1.code, 2, TURN, 0.2)
        b222 = line_bar(p1.code, 3, TOOL, 0.25)
        b223 = line_bar(p1.code, 4, TOOL, 0.25)
        b225 = line_bar(p1.code, 6, ROUTE, 0.25)
        assert p1.get_bottom()[1] > -3.5 and v.zone.get_bottom()[1] > p1.get_top()[1] + 0.1, \
            (p1.get_bottom(), p1.get_top(), v.zone.get_bottom())
        assert v.zone.get_top()[1] < PIC_TOP, v.zone.get_top()

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(q, nb, ep0, ans, one)), FadeOut(ref13), run_time=0.6)
            v.client(self)
            self.play(Indicate(v.zone[1], color=LAPTOP, scale_factor=1.1), run_time=0.6)
            vo.wait_until("The predict code")
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("opens the photo")
            self.play(FadeIn(b221), Indicate(v.photo, color=TURN, scale_factor=1.15), run_time=0.6)
            v.heal(self)
            vo.wait_until("converts it to R G B")
            self.play(FadeOut(b221), FadeIn(b222), run_time=0.4)
            v.gears(self, 0)
            vo.wait_until("and resizes it")
            v.light(self, 0)
            self.play(Indicate(code_span(p1.code, 3, "resize((224, 224))"), color=TOOL, scale_factor=1.15),
                      run_time=0.6)
            self.add(p1, b222)
            vo.wait_until("Then it divides by 255")
            self.play(FadeIn(b223), run_time=0.3)
            v.gears(self, 1)
            v.light(self, 1)
            self.play(Indicate(code_span(p1.code, 4, "/ 255.0"), color=TOOL, scale_factor=1.25), run_time=0.5)
            self.add(p1, b222, b223)
            vo.wait_until("and sends the numbers")
            v.to_cube(self)
            self.play(FadeIn(b225), code_span(p1.code, 6, "payload").animate.set_color(ROUTE), run_time=0.4)
            self.add(p1, b222, b223, b225)
            v.send(self)
        code1 = VGroup(p1, b222, b223, b225)

        # ========================================================== 2. the signature (extra check)
        t = term(P_MD, rows=4, size=SIZE)
        self.t = t
        assert t.box.get_top()[1] < v.zone.get_bottom()[1] - 0.15, (t.box.get_top(), v.zone.get_bottom())
        ex2 = on_bar(t, extra_row())

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(code1), run_time=0.4)
            self.play(dim_anim(tr, base, DIM, 1.0), run_time=0.3)
            self.play(FadeIn(t), track(tr, 5, True), run_time=0.5)
            self.bar(ex2)
            room(self, t, 1)
            t.type(self, C43.cmd, type_time=1.0, wrap=False)
            r43 = out(self, t, OUT43A, run_time=0.5)
            vo.wait_until("which TensorFlow calls a signature")
            self.play(Indicate(substring(r43[0], "inputs['input']"), color=TURN, scale_factor=1.1), run_time=0.6)
            self.reseat()
            vo.wait_until("It takes floats")
            self.paint(r43[1], "DT_FLOAT", TURN)
            vo.wait_until("shaped any number")
            self.paint(r43[2], "(-1, 224, 224, 3)", TURN)
            v.label_door(self)
            vo.wait_until("and gives four numbers")
            r43b = out(self, t, OUT43B, run_time=0.5)
            self.paint(r43b[2], "(-1, 4)", OWN)
            v.out(self, (0.15, 0.1, 0.65, 0.1))
            vo.wait_until("Preprocessing sits on your side")
            self.play(Indicate(v.zone[1], color=TURN, scale_factor=1.12),
                      v.zone[0].frame.animate.set_stroke(TURN), run_time=0.8)
            self.play(v.zone[0].frame.animate.set_stroke(LAPTOP), run_time=0.4)
            v.heal(self)

        # ========================================================== 3. slide 13: client-side brittleness
        cc = client_cards()
        cc.move_to([-6.45 + cc.width / 2, -2.2, 0])
        brit = label("client-side brittleness", 28, ERR)
        brit.move_to([-6.45 + brit.width / 2, -0.62, 0])
        assert cc.get_bottom()[1] > -3.5 and brit.get_top()[1] < v.zone.get_bottom()[1] - 0.1
        assert brit.get_bottom()[1] > cc.get_top()[1] + 0.08, (brit.get_bottom(), cc.get_top())
        one_copy = ok_chip("one copy in the model", size=22)
        one_copy.move_to([v.ep[0].get_center()[0], -1.25, 0])
        keep_inside(one_copy)
        rb_a = Arrow(ORIGIN, LEFT * 0.9, color=OWN, stroke_width=4, buff=0, tip_length=0.18)
        rb = VGroup(rb_a, label("roll back", 22, OWN)).arrange(RIGHT, buff=0.15)
        vs_a = Arrow(ORIGIN, RIGHT * 0.9, color=OWN, stroke_width=4, buff=0, tip_length=0.18)
        vs = VGroup(label("version", 22, OWN), vs_a).arrange(RIGHT, buff=0.15)
        rbvs = VGroup(rb, vs).arrange(RIGHT, buff=0.6).next_to(one_copy, DOWN, buff=0.3)
        keep_inside(rbvs)
        assert one_copy.get_left()[0] > cc.get_right()[0] + 0.2 and rbvs.get_left()[0] > cc.get_right()[0] + 0.2, \
            (one_copy.get_left(), rbvs.get_left(), cc.get_right())
        ref13b = lref("13")
        phone = cc.cards[1]

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(t), *self.unbar_anims(), track(tr, 5), run_time=0.5)
            self.remove(t)
            base = opacities(tr)                      # the new caption (track() rebuilt it)
            self.play(dim_anim(tr, base, 1.0, DIM), run_time=0.3)
            v.drop(self, v.door_label)
            v.door_label = None
            self.play(FadeIn(ref13b, shift=LEFT * 0.1),
                      LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cc.cards], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("client-side brittleness")
            self.play(Write(brit), run_time=1.0)
            vo.wait_until("Every client must repeat")
            gs = [g for c in cc.cards for g in c.gears if len(g) == 3]       # gears (a cross has 2 lines)
            self.play(LaggedStart(*[Rotate(g, PI / 2) for g in gs], lag_ratio=0.15), run_time=1.0)
            vo.wait_until("and a phone app")
            self.play(Indicate(phone, color=ERR, scale_factor=1.06), run_time=0.7)
            vo.wait_until("gets confident nonsense")
            pc = cube(0.42).move_to(phone.frame.get_right() + RIGHT * 0.3)
            door = v.door.get_center()
            path = VMobject().set_points_as_corners([pc.get_center(), [-0.25, v.wire.get_center()[1], 0], door])
            self.play(FadeIn(pc, scale=0.6), run_time=0.25)
            self.play(MoveAlongPath(pc, path), run_time=0.9)
            self.play(FadeOut(pc), run_time=0.2)
            v.bar_g = v.out(self, (0.05, 0.95, 0.05, 0.05), color=ERR)   # out()'s swap keeps the old ref
            self.play(Indicate(v.bar_g, color=ERR, scale_factor=1.15), run_time=0.6)
            v.heal(self)
            vo.wait_until("One copy inside the model")
            self.play(FadeIn(one_copy, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("roll back")
            self.play(GrowArrow(rb_a), FadeIn(rb[1]), run_time=0.5)
            vo.wait_until("and version")
            self.play(GrowArrow(vs_a), FadeIn(vs[0]), run_time=0.5)
        side3 = VGroup(cc, brit, one_copy, rbvs)

        # ========================================================== 4. slide 14: the right pipe
        ref14 = lref("14")
        p2 = grey_chip("part 2 · task.py", size=22)
        p2.move_to([6.45 - p2.width / 2, -1.0, 0])
        co = [callout(1, "define preprocessing", TOOL),
              callout(2, "new signature: a batch of strings", ROUTE),
              callout(3, "save as serving default", OWN)]
        VGroup(*co).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        VGroup(*co).move_to([-6.45 + VGroup(*co).width / 2, -2.2, 0])
        assert VGroup(*co).get_bottom()[1] > -3.5 and VGroup(*co).get_top()[1] < -0.4
        assert VGroup(*co).get_right()[0] < p2.get_left()[0] or VGroup(*co).get_top()[1] < p2.get_bottom()[1]

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(side3), FadeOut(ref13b), run_time=0.5)
            v.drop(self, v.bar_g)
            v.bar_g = None
            self.play(FadeIn(ref14, shift=LEFT * 0.1), FadeIn(p2, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("sits in the part 2 trainer")
            row = v.inside(self, run_time=1.8)
            vo.wait_until("The preprocess function")
            self.play(FadeIn(co[0], shift=RIGHT * 0.15), run_time=0.5)
            ops = [row[0], row[2], row[4]]
            for k, ph in enumerate(("decodes the JPEG", "converts it to floats", "and resizes it")):
                vo.wait_until(ph)
                self.play(Indicate(ops[k], color=TURN, scale_factor=1.15), Rotate(v.gear_list[k], PI / 2),
                          run_time=0.6)
                v.heal(self)

        # ========================================================== 5. a batch of JPEG strings
        stack = VGroup(*[file_glyph(0.42, INK) for _ in range(3)])
        for k, m in enumerate(stack):
            m.move_to(v.cube_g[0].get_center() + np.array([0.12 * k, -0.1 * k, 0]))
        q_l = mono("?", 24, S.GREY)

        with self.voiceover(SAY[5]) as vo:
            v.swap(self, v.cube_g[0], stack, run_time=0.6)
            vo.wait_until("takes a batch of JPEG strings")
            self.play(FadeIn(co[1], shift=RIGHT * 0.15), run_time=0.4)
            riders = stack.copy()
            self.add(riders)
            self.play(riders.animate.arrange(RIGHT, buff=0.05).scale(0.7).move_to(v.wire.get_center()),
                      run_time=0.7)
            self.play(riders.animate.scale(0.5).move_to(v.door.get_center()), run_time=0.5)
            self.play(FadeOut(riders), v.door.animate.set_fill(OWN, 0.35), run_time=0.3)
            self.remove(riders)
            v.heal(self)
            vo.wait_until("prepares each one")
            self.play(*[Rotate(g, PI / 2) for g in v.gear_list], run_time=0.7)
            vo.wait_until("and calls the model")
            self.play(Indicate(v.ep[0], color=CLOUD, scale_factor=1.04), run_time=0.6)
            v.heal(self)
            vo.wait_until("It is saved as the serving default")
            self.play(FadeIn(co[2], shift=RIGHT * 0.15), run_time=0.4)
            self.play(Indicate(v.door_label, color=OWN, scale_factor=1.2), run_time=0.7)
            v.heal(self)
            vo.wait_until("Raw bytes in")
            self.play(Indicate(v.cube_g[1], color=IMAGE, scale_factor=1.2), run_time=0.6)
            v.heal(self)
            vo.wait_until("one score per class out")
            qb = bars(("?", "?", "?"), 0.16, 1.0, S.GREY, buff=0.16).move_to(v.p(5.95, 0.05))
            qb.align_to(v.p(0, -0.45), DOWN)            # where TwoPipes.out() puts its bars
            q_l.next_to(qb, UP, buff=0.15)
            assert qb.get_right()[0] < 6.55, qb.get_right()
            v.show(self, qb, q_l, anims=[LaggedStart(*[GrowFromEdge(m, DOWN) for m in qb], lag_ratio=0.25),
                                         FadeIn(q_l, shift=DOWN * 0.1)], run_time=0.7)

        # ========================================================== 6. the README's word: format, not signature
        rc = readme_card(115, README115, "A", size=26)
        rc.move_to([0, 0.9, 0])
        fmt = ok_chip("format change ✓", size=22)
        sig = grey_chip("signature change", size=22)
        VGroup(fmt, sig).arrange(RIGHT, buff=0.8).next_to(rc, DOWN, buff=0.6)
        sig_x = strike(sig, S.GREY)

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(v), FadeOut(VGroup(*co)), FadeOut(p2), FadeOut(ref14), run_time=0.6)
            vo.wait_until("The README says")
            self.play(FadeIn(rc, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("converts the model")
            self.play(Indicate(rc.body, color=TURN, scale_factor=1.04), run_time=0.8)
            vo.wait_until("That is a change of format")
            self.play(FadeIn(fmt, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("not the change of signature")
            self.play(FadeIn(sig, shift=UP * 0.15), run_time=0.5)
            self.play(Create(sig_x), run_time=0.5)
        self.play(FadeOut(VGroup(rc, fmt, sig, sig_x, tr)), run_time=0.8)
        self.wait(0.3)

    # ------------------------------------------------------------------ terminal helpers (as S04)
    def bar(self, tg):
        """Show a title-bar tag (on_bar) and remember it, so it fades with the terminal."""
        self.play(FadeIn(tg), run_time=0.3)
        self.bar_tags.append(tg)

    def unbar_anims(self):
        tgs, self.bar_tags = self.bar_tags, []
        return [FadeOut(tg) for tg in tgs]

    def reseat(self):
        """Re-seat the terminal as one mobject (split trap) and keep its bar tags on top."""
        self.add(self.t, *self.bar_tags)

    def paint(self, row, sub, color, run_time: float = 0.4):
        """Colour substring `sub` of terminal row `row`."""
        self.play(substring(row, sub).animate.set_color(color), run_time=run_time)
        self.reseat()
