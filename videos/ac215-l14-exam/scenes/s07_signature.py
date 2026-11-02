"""S07 · Register serve: preprocess, then model (AC215 L14 exam edition). Lecture: 15 · 14.

Beats (script.md "## S07", one voiceover block each):
0. The exam map (slots 1-4 filled, 5 half) fades in, slot 5 activates and pulses again; lref(15, "14").
   V6's pipeline writes in as it is named: PINK "JPEG bytes" -> GREEN "decode" -> "to float" ->
   "resize" -> "model" -> four probability bars (parmigiano · gruyere · brie · gouda, the order of
   model-deployment/README.md line 187), which rise at "and four probabilities".
1. CODE(model-deployment/cli.py: 100–105) under the pipeline: lines 102, 103, 104 light in step with
   the three GREEN blocks; the bracket "preprocess_image" closes around them at "for one image";
   at "It returns an image" line 105 lights and a 224×224×3 image glyph pops out of the bracket.
2. CODE(cli.py: 108–114): line 109 lit PINK ("a batch of strings", the JPEG bytes block pulses),
   111–113 GREEN (the preprocess bracket pulses), 114 GREEN (the model block pulses); the bracket
   "serving_function" closes under all five blocks; line 108's comment lit YELLOW with a PINK
   request-key chip "bytes_inputs" over the bytes block; the GRAY alias chip "a.k.a. serve".
3. The pipeline and panel go; CODE(cli.py: 117–122) at the top: line 122
   (add_endpoint(name="serving_default", fn=serving_function)) lit YELLOW as the GREEN SavedModel
   and its empty socket "serving_default" appear; the PURPLE model server and its wire at "and the
   model server calls"; at "The slide saves it" lines 117–119 lit GRAY and the GRAY lecture chip
   "slide 14: tf.saved_model.save(…, signatures={"serving_default": …})" at the bottom.
4. The panel and chip go; the map and lecture tag leave (the card needs the top); the SavedModel
   and server dim to 20 %, the socket stays bright; the two small GREY clients of the question (a
   phone app, a web page) appear bottom left as they are named. After the SAY: PONDER P3 (12 s)
   card with the question and options A-D at the top (the clients dim too).
5. The card cross-fades into the compact docked card "P3" (top); everything comes back. Plug B
   "preprocess_image" pushes into the socket: out comes a 224×224×3 image, RED ✗ "no prediction";
   under B, RED "returns 224×224 images, not predictions".
6. Unplug. Plug A/D "raw model": the socket's label becomes "expects float tensors", the PINK bytes
   chip bounces RED; under A the RED reason; the two clients come back, GREEN gears jump from the
   SavedModel back onto them (V5 rewound), a RED "clients disagree" band flickers; under D the RED
   reason.
7. Unplug. Plug C "serving_function": bytes go in, the four bars rise, brie tallest, YELLOW. At "The
   phone app switches" C fills YELLOW ✓ with the GREEN note, and the clients' gears fly into the
   serving_function plug and vanish; the clients leave. At "The repo's test step" the card fades and CODE(cli.py: 157–158, 160, 163 folded)
   comes in: 158 and 163 lit YELLOW, 160's comment lit GRAY.
8. The panel, plug and model server go; the map returns. S04's name tag "entry point: hello_http"
   slides in on the left, the socket moves to the right, a YELLOW bracket joins them: "the
   platform calls the name you register".
9. RULE line 1 at "The rule", line 2 at "Preprocessing alone"; the tag and socket leave; the card
   shrinks into map slot 5, which is now full and GREEN-ticked; empty frame.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circumscribe,
    FadeIn,
    FadeOut,
    Indicate,
    ReplacementTransform,
    SurroundingRectangle,
    VGroup,
)

from explainer import style as S
from explainer.scene import VoiceScene

from common import (
    CAPTION,
    ERR,
    NARRATION,
    OWN,
    ROUTE,
    SAFE_X,
    SAFE_Y,
    TURN,
    ExamMap,
    MCQCard,
    RuleCard,
    ServingPlug,
    _set_op,
    chip,
    dim,
    entry_tag,
    gear,
    guard,
    hbracket,
    image_glyph,
    lref,
    mono,
    phone_glyph,
    sans,
    source_line,
    src_panel,
    step_badge,
    undim,
    url_chip,
    webpage_glyph,
)

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real sources (checked)
CLI = "cli.py"                                   # = model-deployment/cli.py
README = "model-deployment/README.md"
assert "def preprocess_image(bytes_input):" in source_line(CLI, 101)
assert "tf.io.decode_jpeg(bytes_input, channels=3)" in source_line(CLI, 102)
assert "tf.image.convert_image_dtype(decoded, tf.float32)" in source_line(CLI, 103)
assert "tf.image.resize(decoded, size=(224, 224))" in source_line(CLI, 104)
assert source_line(CLI, 105).strip() == "return resized"
assert "The argument name (bytes_inputs) is the key clients must use" in source_line(CLI, 108)
assert "input_signature=[tf.TensorSpec([None], tf.string)]" in source_line(CLI, 109)
assert "def serving_function(bytes_inputs):" in source_line(CLI, 110)
assert "tf.map_fn(" in source_line(CLI, 111) and "preprocess_image, bytes_inputs" in source_line(CLI, 112)
assert "return prediction_model(images, training=False)" in source_line(CLI, 114)
assert "tf.saved_model.save()" in source_line(CLI, 117)
assert "ExportArchive()" in source_line(CLI, 120)
assert 'add_endpoint(name="serving_default", fn=serving_function)' in source_line(CLI, 122)
assert 'signature_def["serving_default"]' in source_line(CLI, 158)
assert "Send raw image bytes" in source_line(CLI, 160)
assert 'signature.inputs["bytes_inputs"]' in source_line(CLI, 163)
assert "parmigiano, gruyere, brie, gouda" in source_line(README, 187)

SIG_LINES = (108, 114)     # 107 (a comment) left out: 107–114 needs 4.7 units, 3.9 fit
EXPORT_LINES = (117, 122)     # 116 and 123 left out: the panel must fit above the SavedModel
TEST_LINES = [157, 158, 160, 163]

SLIDE14 = 'slide 14: tf.saved_model.save(…, signatures={"serving_default": …})'

Q = ("`serving_default` is the raw model. The phone app sends resized float arrays; a new web client "
     "sends JPEG bytes. One place to fix or roll back preprocessing: what do they register?")
OPTS = ["The raw model: the server decodes JPEGs", "`preprocess_image`",
        "A function: preprocess each image, then call the model",
        "The raw model, plus the resize code copied into the web client"]
WHY_A = "the server only turns base64 into bytes · the signature decides what they become"
WHY_B = "returns 224×224 images, not predictions"
WHY_D = "two copies to keep in sync · every rollback = two client releases"
WHY_C = "after one switch to bytes · every later fix or rollback = one deployment"

RULE_TOP = "register the function that does preprocessing AND inference"
RULE_BOTTOM = "preprocess alone → images · raw model → every client preprocesses"

TOP_BAND = 2.55          # content stays below the active slot's label while the map shows
CARD_TOP = 3.5           # the P3 cards use the top strip (map and tag leave for them)


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


def bars(panel, lines, color, opacity=0.22):
    g = VGroup()
    for n in lines:
        g.add(*panel.bar(n, color, opacity))
    return g


def lower_bytes_chip(sp, anims, gap: float = 0.1):
    """The plug's PINK bytes chip sits 0.35 above the plug; the docked card needs that room: move
    it down to `gap` above the plug. The "raw" plug also animates the chip (turn RED, bounce left
    and back), but both of its `.animate` targets were built from one shared `chip.target` while the
    chip was still hidden (common.py: it ends PINK, 0.4 to the left, or invisible): give those two
    animations their own targets here, at the new place: RED, then RED and 0.4 to the left."""
    p, c = sp.cur[0], sp.cur[1]
    c.shift(DOWN * (c.get_bottom()[1] - (p.get_top()[1] + gap)))
    found = []

    def walk(a):
        for sub in getattr(a, "animations", []) or []:
            walk(sub)
        if getattr(a, "mobject", None) is c and getattr(a, "target_mobject", None) is not None:
            found.append(a)

    for a in anims:
        walk(a)
    shown = c.copy()
    _set_op(shown)
    for k, a in enumerate(found):
        t = shown.copy().set_color(ERR)
        if k == 1:
            t.shift(LEFT * 0.4)
        a.target_mobject = t
    return c


def gray_chip(text):
    return chip(text, S.GREY, size=CAPTION)


class ServeSignature(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0. the chain
        m = ExamMap(filled=(1, 2, 3, 4), half=(5,))
        sp = ServingPlug(show=())
        lr = lref(15, "14")
        inside_frame(sp, lr)
        below_band(sp)
        with self.voiceover(SAY[0]) as vo:
            self.add(sp)
            self.play(FadeIn(m), run_time=0.6)
            self.play(*m.activate(5), FadeIn(lr), run_time=0.7)
            self.play(m.pulse(5), run_time=0.8)
            vo.wait_until("calls the right function")
            self.play(m.pulse(5), run_time=0.8)
            vo.wait_until("Here is the chain")
            self.play(*sp.write_block(0), run_time=0.5)
            vo.wait_until("decode")
            self.play(*sp.write_block(1), run_time=0.4)
            vo.wait_until("convert to floats")
            self.play(*sp.write_block(2), run_time=0.4)
            vo.wait_until("resize")
            self.play(*sp.write_block(3), run_time=0.4)
            vo.wait_until("the model")
            self.play(*sp.write_block(4), run_time=0.4)
            vo.wait_until("and four probabilities")
            self.play(*sp.write_block(5), run_time=0.4)
            self.play(*sp.bars.rise(hi=None), run_time=0.8)
            vo.wait_until("one per cheese")
            self.play(Indicate(sp.bars.labels, color=TURN, scale_factor=1.05), run_time=vo.remaining(0.8))

        # ========================================================== 1. preprocess_image
        blk = sp.blocks
        p1 = src_panel(CLI, 100, 105, size=20)
        p1.move_to([-6.45 + p1.width / 2, 0.2 - p1.height / 2, 0])
        lit1 = [p1.bar(n, OWN, 0.22) for n in (102, 103, 104)]
        lit105 = p1.bar(105, TURN, 0.22)
        img = image_glyph(0.42)
        img.move_to([5.0, -1.0, 0])
        inside_frame(p1, img)
        apart(p1, sp.parts["serve"], 0.05)
        apart(p1, sp.parts["alias"], 0.05)
        apart(img, p1, 0.2)
        apart(img, sp.bars, 0.1)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(p1, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("does the first three steps")
            for k in range(3):
                self.play(FadeIn(lit1[k]), Indicate(blk[k + 1], color=TURN, scale_factor=1.06), run_time=0.45)
            vo.wait_until("for one image")
            self.play(*sp.bracket("pre"), run_time=0.6)
            vo.wait_until("It returns an image")
            start = img.copy().move_to(sp.parts["pre"].text)
            self.play(FadeIn(lit105), FadeIn(start, scale=0.5), run_time=0.5)
            self.play(ReplacementTransform(start, img), run_time=0.7)
            vo.wait_until("not an answer")
            self.play(Circumscribe(sp.bars, color=TURN, buff=0.08), run_time=vo.remaining(0.8))

        # ========================================================== 2. serving_function
        p2 = src_panel(CLI, *SIG_LINES, size=20, wrap_at=75)
        p2.move_to([-6.45 + p2.width / 2, 0.2 - p2.height / 2, 0])
        b109 = bars(p2, [109], ROUTE)
        b111 = bars(p2, [111, 112, 113], OWN)
        b114 = bars(p2, [114], OWN)
        b108 = bars(p2, [108], TURN)
        key = url_chip('"bytes_inputs"')
        key.move_to([-6.45 + key.width / 2, blk[0].get_top()[1] + 0.25 + key.height / 2, 0])
        inside_frame(p2, key)
        below_band(key)
        apart(p2, sp.parts["serve"], 0.05)
        apart(p2, sp.parts["alias"], 0.05)
        apart(key, sp.parts["pre"].text, 0.1)
        apart(key, sp.parts["pre"].line, 0.0)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p1, *lit1, lit105, img)), run_time=0.4)
            self.play(FadeIn(p2, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("takes a batch of strings")
            self.play(FadeIn(b109), Indicate(blk[0], color=ROUTE, scale_factor=1.06), run_time=0.6)
            vo.wait_until("maps preprocess image")
            self.play(FadeIn(b111), Indicate(sp.parts["pre"], color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("then calls the model")
            self.play(FadeIn(b114), Indicate(blk[4], color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Preprocessing and inference")
            self.play(*sp.parts_in("serve"), run_time=0.7)
            vo.wait_until("Its argument")
            self.play(FadeIn(b108), FadeIn(key, shift=DOWN * 0.1), run_time=0.6)
            self.play(Indicate(key, color=TURN), run_time=0.6)
            vo.wait_until("Exam questions may call")
            self.play(*sp.parts_in("alias"), run_time=0.5)
            vo.wait_until("not the web app")
            self.play(Indicate(sp.parts["alias"], color=TURN), run_time=0.6)
            vo.wait_until("but the function that preprocesses")
            self.play(Circumscribe(sp.parts["serve"], color=TURN, buff=0.06), run_time=vo.remaining(0.8))

        # ========================================================== 3. the export registers it
        p3 = src_panel(CLI, *EXPORT_LINES, size=20, wrap_at=76)   # line 122 (76 chars) whole
        p3.move_to([-6.45 + p3.width / 2, 2.5 - p3.height / 2, 0])
        b122 = bars(p3, [122], TURN)
        b117 = bars(p3, [117, 118, 119], S.GREY, 0.3)
        s14 = gray_chip(SLIDE14).move_to([0, -3.15, 0])
        low = VGroup(sp.parts["saved"], sp.sock, sp.parts["server"], sp.parts["wire"])
        inside_frame(p3, s14, low)
        below_band(p3)
        apart(p3, sp.parts["saved"], 0.05)
        apart(p3, sp.sock, 0.05)
        apart(p3, sp.parts["server"], 0.05)
        apart(s14, sp.sock, 0.08)
        apart(p3, lr, 0.05)
        top_parts = ("blocks", "arrows", "bars", "pre", "serve", "alias")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p2, b109, b111, b114, b108, key)), *sp.parts_out(*top_parts), run_time=0.6)
            self.play(FadeIn(p3, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("registers it under the name")
            self.play(FadeIn(b122), *sp.parts_in("saved", "socket"), run_time=0.8)
            vo.wait_until("serving default")
            self.play(Indicate(sp.sock.label, color=TURN), run_time=0.7)
            vo.wait_until("and the model server calls")
            self.play(*sp.parts_in("server", "wire"), run_time=0.7)
            vo.wait_until("whatever sits behind")
            self.play(Circumscribe(sp.sock.frame, color=TURN, buff=0.06), run_time=0.8)
            vo.wait_until("The slide saves it")
            self.play(FadeIn(b117), FadeIn(s14, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("the idea is the same")
            self.play(Indicate(b122, color=TURN, scale_factor=1.02), run_time=vo.remaining(0.7))

        # ========================================================== 4. PONDER P3
        phone = phone_glyph(0.62)
        web = webpage_glyph(0.9)
        cl = VGroup(phone, web).arrange(RIGHT, buff=0.9)
        gpos = [phone.get_right() + RIGHT * 0.28, web.get_right() + RIGHT * 0.28]
        spots = VGroup(*[gear(0.17).move_to(q) for q in gpos])
        band = SurroundingRectangle(VGroup(cl, spots), buff=0.12, stroke_color=ERR, stroke_width=2) \
            .set_fill(ERR, 0.16)
        shift = [-6.5 - band.get_left()[0], -3.5 - band.get_bottom()[1], 0]
        for mob in (cl, band):
            mob.shift(shift)
        gpos = [q + shift for q in gpos]
        band_lab = sans("clients disagree", CAPTION, ERR).next_to(band, RIGHT, buff=0.15)
        band_lab.align_to(band, DOWN)
        wide = mono("expects float tensors", CAPTION + 2, ERR).move_to(sp.sock.label)
        mini = VGroup(cl, band, band_lab)
        inside_frame(mini)
        apart(band, wide, 0.15)
        apart(band_lab, wide, 0.1)
        apart(band, sp.sock.label, 0.15)
        card = MCQCard(Q, OPTS, reason_rows=0)
        card.move_to([0, CARD_TOP - card.height / 2, 0])
        inside_frame(card)
        apart(card, low, 0.08)
        side = (sp.parts["saved"], sp.parts["server"], sp.parts["wire"])
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p3, b122, b117, s14)), run_time=0.5)
            vo.wait_until("one last check")
            self.play(FadeOut(m), FadeOut(lr), *[dim(x) for x in side], run_time=0.6)
            vo.wait_until("A phone app")
            self.play(FadeIn(phone, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a new web client")
            self.play(FadeIn(web, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("one place to fix")
            self.play(Circumscribe(sp.sock.frame, color=TURN, buff=0.06), run_time=0.8)
        self.play(FadeIn(card, scale=0.97), dim(cl), run_time=0.6)
        card.run_timer(self, 12)

        # ========================================================== 5. plug B: preprocess_image
        dock = MCQCard(None, OPTS, size=20, reason_rows=1, header="P3")
        dock.move_to([0, CARD_TOP - dock.height / 2, 0])
        inside_frame(dock)
        apart(dock, low, 0.08)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(card), FadeIn(dock), *[undim(x) for x in side], run_time=0.8)
            vo.wait_until("Try B first")
            anims = sp.plug("preprocess", letter="B")
            c = lower_bytes_chip(sp, anims)
            plug_b = sp.cur[0]
            apart(c, dock, 0.08)
            inside_frame(plug_b)
            self.play(*anims, run_time=2.2)
            vo.wait_until("Nothing was classified")
            self.play(*dock.wrong(1, WHY_B), run_time=0.7)
            self.play(Indicate(sp.cur[2], color=ERR), run_time=vo.remaining(0.6))

        # ========================================================== 6. plug A/D: the raw model
        gears = VGroup(*[gear(0.17).scale(0.3).move_to(sp.parts["saved"][0].get_center()) for _ in range(2)])
        with self.voiceover(SAY[6]) as vo:
            self.play(*sp.unplug(), run_time=0.5)
            vo.wait_until("A and D keep the raw model")
            anims = sp.plug("raw", letter="A")
            c = lower_bytes_chip(sp, anims)
            p = sp.cur[0]
            dx = sp.sock.mouth()[0] + 0.18 - p.prongs.get_right()[0]
            d = step_badge("D", TURN).next_to(p.badge, LEFT, buff=0.1).shift(RIGHT * dx)
            sp.cur.add(d)
            apart(c, dock, 0.08)
            inside_frame(p, d)
            apart(p.copy().shift(RIGHT * dx), mini, 0.05)
            apart(d, mini, 0.05)
            self.play(*anims, run_time=2.4)
            self.play(FadeIn(d, scale=0.6), run_time=0.4)
            vo.wait_until("The server only turns base64")
            self.play(*dock.wrong(0, WHY_A), run_time=0.7)
            vo.wait_until("The gears jump back")
            self.play(undim(cl), FadeIn(gears), run_time=0.4)
            self.play(*[g.animate(path_arc=0.8).scale(1 / 0.3).move_to(q) for g, q in zip(gears, gpos)],
                      run_time=0.9)
            vo.wait_until("two copies to keep in sync")
            self.play(FadeIn(band), FadeIn(band_lab), *dock.wrong(3, WHY_D), run_time=0.5)
            self.play(band.animate.set_fill(ERR, 0.04), run_time=0.3)
            self.play(band.animate.set_fill(ERR, 0.16), run_time=vo.remaining(0.3))

        # ========================================================== 7. plug C: serving_function
        p7 = src_panel(CLI, TEST_LINES, size=20)
        p7.move_to([-6.45 + p7.width / 2, 3.45 - p7.height / 2, 0])
        b158 = bars(p7, [158, 163], TURN)
        b160 = bars(p7, [160], S.GREY, 0.3)
        inside_frame(p7)
        with self.voiceover(SAY[7]) as vo:
            self.play(*sp.unplug(), FadeOut(VGroup(band, band_lab)), run_time=0.5)
            vo.wait_until("C, the serving function")
            anims = sp.plug("serve", letter="C")
            c = lower_bytes_chip(sp, anims)
            apart(c, dock, 0.08)
            apart(c, p7, 0.08)
            apart(sp.out_bars, p7, 0.08)
            self.play(*anims, run_time=2.2)
            vo.wait_until("The phone app switches")
            anims = dock.right(2, WHY_C)
            hl, tk, nt = dock.marks[-3:]
            both = VGroup(dock.rows[2], nt)
            hl.stretch_to_fit_height(both.height + 0.16).set_y(both.get_center()[1])
            tk.set_y(both.get_center()[1])
            guard(hl.get_top()[1] < dock.rows[1].get_bottom()[1] and hl.get_bottom()[1] > dock.rows[3].get_top()[1],
                  "C's highlight reaches B or D")
            self.play(*anims, run_time=0.7)
            into = sp.cur[0].body.get_center()
            self.play(*[g.animate(path_arc=-0.8).move_to(into).scale(0.3).set_opacity(0) for g in gears],
                      run_time=0.9)
            self.remove(gears)
            self.play(FadeOut(cl), run_time=0.4)
            vo.wait_until("every fix or rollback is one deployment")
            self.play(Indicate(sp.parts["saved"], color=TURN, scale_factor=1.05), run_time=0.7)
            vo.wait_until("The repo's test step")
            self.play(FadeOut(dock), run_time=0.5)
            self.play(FadeIn(p7, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("loads serving default")
            self.play(FadeIn(b158[: len(p7.rows_of(158))]), FadeIn(b160), run_time=0.5)
            vo.wait_until("feeds it bytes inputs")
            self.play(FadeIn(b158[len(p7.rows_of(158)):]), run_time=vo.remaining(0.5))

        # ========================================================== 8. the entry point echo
        tag = entry_tag()
        tag.move_to([-3.4, 0.9, 0])
        sock_to = sp.sock.copy().move_to([2.9, 0.9, 0])
        br = hbracket(VGroup(tag, sock_to), "the platform calls the name you register", DOWN, TURN)
        echo = VGroup(tag, sock_to, br)
        inside_frame(echo)
        below_band(echo)
        apart(tag, sock_to, 0.5)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(p7, b158, b160)), *sp.unplug(),
                      *sp.parts_out("saved", "server", "wire"), run_time=0.6)
            self.play(FadeIn(m), sp.sock.animate.move_to(sock_to), FadeIn(tag, shift=RIGHT * 0.6), run_time=1.0)
            vo.wait_until("the platform calls exactly")
            self.play(FadeIn(br, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("nothing downstream")
            self.play(Indicate(tag.name, color=TURN, scale_factor=1.05), Indicate(sp.sock.label, color=TURN, scale_factor=1.05),
                      run_time=vo.remaining(0.8))

        # ========================================================== 9. the rule -> map slot 5 (full)
        rule = RuleCard(RULE_TOP, RULE_BOTTOM)
        inside_frame(rule)
        apart(rule, echo, 0.08)
        with self.voiceover(SAY[9]) as vo:
            vo.wait_until("The rule")
            self.play(rule.frame_in(), run_time=0.4)
            self.play(rule.line_in(0), run_time=0.6)
            vo.wait_until("preprocessing and inference")
            self.play(Indicate(rule.rows[0], color=TURN, scale_factor=1.03), run_time=0.8)
            vo.wait_until("Preprocessing alone")
            self.play(rule.line_in(1), run_time=0.6)
            vo.wait_until("and the raw model")
            self.play(Indicate(rule.rows[1], color=TURN, scale_factor=1.03), run_time=vo.remaining(0.7))
        self.play(FadeOut(VGroup(tag, br)), FadeOut(sp), run_time=0.5)
        rule.shrink_into(self, m, 5, frac=1.0)
        self.play(m.pulse(5), run_time=0.7)
        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
        self.wait(0.3)
