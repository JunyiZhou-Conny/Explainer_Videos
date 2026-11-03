"""S07 · A label is a record; read it back by name — tracker C5 → C6, then D1 → D3,
`lref("4, 6, 10, 13")` the whole scene.

Beats (script.md, ## S07; one voiceover block each):
0. TRACKER C5. A labeling-screen wireframe (`illustration`, README.md 174–177): one image frame (no
   photo), four choices; the cursor clicks `gouda`, then Submit; ▶ your turn. Its server side, an
   output-only 12-row terminal headed `POST /api/tasks/1/annotations · stand-in`, tag `extra ·
   stand-in`: laptop/33:2–4 wrapped, `"choices": ["gouda"]` YELLOW, `HTTP 201` GREEN.
1. V2 step 4: the WHITE envelope stops at the GREY database drawer; a copy flies on into
   cheeses_labeled/, a thread back to its photo in cheeses_unlabeled/, which never moved; GREY chip
   "on submit, via target storage · README.md:184–186 · not captured here". Slide 6's "Labeled"
   rows (V7 .slide6_big) morph into a stack of envelopes + chip "the slide draws what labels mean";
   the stack drops into V7's cheeses_labeled/ drawer, which lights (photos + notes in one bucket).
   TRACKER C6: console wireframe (`illustration`, README.md 184–187): cheeses_labeled/ holding
   json files with no object names drawn; one opens to the envelope `result → value → choices:
   ["gouda"]`.
2. V1 reprise: the CLI house joins the street, its name call to Label Studio, the `localhost:8080`
   arc hovering over it. PONDER 6 s.
3. TRACKER C6 · extra. 3-row strip at app@5bf8945fb887: laptop/41:108 → 109 RED (the arc curls back:
   RED cross), 41:110 → 111 GREEN (the name call, the PINK phone book); the browser's
   `localhost:8080` call comes in through the laptop door.
4. TRACKER D1: Account & Settings wireframe (`illustration`, README.md 193–196), token field blank,
   ▶ your turn. TRACKER D2: at app@eb57c56e6715 (container note), laptop/42:32 typed (token: "obviously
   fake"), 42:33, 36–38, 43, …, 66 wrapped; 37 and 43 RED; ▶ your turn.
5. TRACKER D2 · extra: the wireframe with two blank token rows, the legacy row greys out; stand-in
   strip `GET /api/jwt/settings · stand-in`: 27:2, `"legacy_api_tokens_enabled":false` RED. CODE
   cli.py:75–83, line 79 YELLOW, chip "the legacy client".
6. TRACKER D2 · extra: Organization → API Tokens Settings wireframe, the "legacy tokens" toggle
   switches ON; stand-in strip 43:2 `"legacy_api_tokens_enabled":true` GREEN. The Account wireframe
   again: "legacy token" row YELLOW, "personal access token" GREY; ▶ your turn; GREY chip (unspoken)
   "other fix: the SDK's LabelStudio client · exercise".
7. TRACKER D2: at app@e9e15714ac9b, 44:32 → 33–36 (`1 Cheese labels` GREEN, chip "object reprs, not
   dicts"); ▶ your turn. TRACKER D3: 44:37 → 38–42 wrapped (`Number of tasks: 3` + chip "ours: 3 ·
   yours: 21", `['gouda']` YELLOW). README card line 204 ('amanita' GREY, tag `erratum`, chip).
   Unspoken, TRACKER D3 · extra: at app@eb57c56e6715, 42:67 → 68–69 (`i required` GREY, `erratum`,
   chip "forgot -k? · cli.py:123's typo: is required"). Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S07"]
PONDER_Q = "Inside the CLI container,\nwhat if LABEL_STUDIO_URL were\nhttp://localhost:8080?"
CALL_ANNOTATE = "POST /api/tasks/1/annotations · stand-in"
CALL_JWT_GET = "GET /api/jwt/settings · stand-in"
CALL_JWT_POST = "POST /api/jwt/settings · stand-in"
CONSOLE_URL = "https://console.cloud.google.com/storage/browser"      # README.md:184
COPY_CHIP = "on submit, via target storage · README.md:184–186 · not captured here"
SLIDE_CHIP = "the slide draws what labels mean"
JSON_CHIP = "README.md:186 · “some json files” · one per annotation"
NOTE_SHAPE = 'result → value → choices: ["gouda"]'
SDK_CHIP = "other fix: the SDK's LabelStudio client · exercise"
AMANITA_CHIP = "a mushroom from an older course app · same format"
TYPO_CHIP = "forgot -k? · cli.py:123's typo: is required"


def drop(scene, *mobs) -> None:
    """Take mobjects and their whole families off the scene (a scrolled terminal is split into parts
    on the scene; a faded part left there snaps back at full opacity)."""
    fam = []
    for m in mobs:
        fam.extend(m.get_family())
    scene.remove(*fam)


def glyphs(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` inside a label/mono Text (its .text drops spaces; so do its glyphs)."""
    flat, key = t.text.replace(" ", ""), sub.replace(" ", "")
    i = flat.index(key)
    return VGroup(*t.submobjects[i:i + len(key)])


def row_with(rows, sub: str, occurrence: int = 0):
    """The printed terminal row (of `rows`) whose text contains `sub`."""
    hits = [r for r in rows if sub in r.text]
    return hits[occurrence]


def button(s: str, color=S.GREY) -> VGroup:
    """A schematic button (label 22 pt in a filled GREY box). .box .text"""
    t = label(s, 22, INK)
    b = RoundedRectangle(width=t.width + 0.5, height=0.5, corner_radius=0.1, stroke_color=color,
                         stroke_width=2).set_fill(S.GREY_DARKER, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def cursor_glyph(h: float = 0.42) -> VMobject:
    """A mouse pointer (WHITE outline); its tip is .tip (the point that clicks)."""
    pts = [[0, 0, 0], [0, -h, 0], [h * 0.27, -h * 0.74, 0], [h * 0.47, -h * 1.08, 0], [h * 0.6, -h * 1.0, 0],
           [h * 0.41, -h * 0.68, 0], [h * 0.72, -h * 0.68, 0]]
    p = Polygon(*pts, stroke_color=INK, stroke_width=2.5).set_fill(S.BG, 1)
    return p


def tip_to(c: VMobject, point) -> np.ndarray:
    """Where to move the cursor's centre so that its tip (first vertex) lands on `point`."""
    return np.array(point) + (c.get_center() - c.get_vertices()[0])


def choice_row(word: str) -> VGroup:
    """A radio button + the choice word (22 pt). .dot .ring .text"""
    rg = Circle(radius=0.14, stroke_color=S.GREY, stroke_width=2.5)
    dt = Dot(radius=0.07, color=TURN)
    t = label(word, 24, INK).next_to(rg, RIGHT, buff=0.22)
    dt.move_to(rg)
    g = VGroup(rg, t)
    g.ring, g.dot, g.text = rg, dt, t
    return g


def label_screen() -> VGroup:
    """The labeling screen (illustration): an image frame (no photo), four choices, Submit.
    .win .image .choices (rows by word) .submit .ill"""
    win = window("localhost:8080", 10.4, 4.7).move_to([0, 0.15, 0])
    img = tile(None, 3.4, LAPTOP).move_to([-2.35, -0.15, 0])
    rows = VGroup(*[choice_row(w) for w in CHOICES]).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    rows.move_to([1.85, 0.25, 0], aligned_edge=LEFT)
    sub = button("Submit").next_to(rows, DOWN, buff=0.5).align_to(rows, LEFT)
    ill = illustration_tag().move_to(win.content.get_corner(UR) + np.array([-1.0, -0.35, 0]))
    ill.align_to(win.content, RIGHT).shift(LEFT * 0.15)
    g = VGroup(win, img, rows, sub, ill)
    g.win, g.image, g.choices, g.submit, g.ill = win, img, {w: r for w, r in zip(CHOICES, rows)}, sub, ill
    return g


def token_row(lab: str, field_w: float = 4.6, color=S.GREY) -> VGroup:
    """A settings row: label (22 pt) left, a blank token field (no value: never token material).
    Left edge at x 0. .label .field"""
    lt = label(lab, 22, color)
    fd = RoundedRectangle(width=field_w, height=0.44, corner_radius=0.06, stroke_color=color,
                          stroke_width=2).set_fill(TERM_BG, 1)
    lt.move_to([0, 0, 0], aligned_edge=LEFT)
    fd.move_to([4.0 + field_w / 2, 0, 0])
    g = VGroup(lt, fd)
    g.label, g.field = lt, fd
    return g


def settings_page(crumbs, rows, y: float = 0.95, win_h: float = 3.3) -> VGroup:
    """A Label Studio settings page (illustration): breadcrumbs and setting rows, inside a window.
    .win .crumbs .rows .ill"""
    win = window("localhost:8080", 11.6, win_h).move_to([0, y, 0])
    cr = VGroup()
    for i, c in enumerate(crumbs):
        if i:
            cr.add(label("→", 22, S.GREY))
        cr.add(label(c, 22, INK))
    cr.arrange(RIGHT, buff=0.2)
    x0 = win.frame.get_left()[0] + 0.5
    top = win.content.get_top()[1]
    cr.move_to([x0, top - 0.35, 0], aligned_edge=LEFT)
    rs = VGroup(*rows)
    for i, r in enumerate(rows):
        r.move_to([x0, top - 1.1 - 0.62 * i, 0], aligned_edge=LEFT)
    ill = illustration_tag().move_to([0, cr.get_center()[1], 0]).align_to(win.frame, RIGHT).shift(LEFT * 0.25)
    g = VGroup(win, cr, rs, ill)
    g.win, g.crumbs, g.rows, g.ill = win, cr, list(rows), ill
    return g


def toggle(on: bool = False) -> VGroup:
    """An on/off switch: a pill and a knob (OFF GREY left, ON GREEN right). .pill .knob"""
    c = PASS if on else S.GREY
    pill = RoundedRectangle(width=0.8, height=0.4, corner_radius=0.2, stroke_color=c,
                            stroke_width=2.5).set_fill(c, 0.35 if on else 0.0)
    knob = Dot(radius=0.13, color=c).move_to(pill.get_center() + RIGHT * (0.2 if on else -0.2))
    g = VGroup(pill, knob)
    g.pill, g.knob = pill, knob
    return g


def copy_to_labeled(scene, v2, env):
    """V2 step 4b, as SignedTicket.copy_out() but the copy ends as a small envelope at the free right
    end of cheeses_labeled/ (copy_out's full-size copy covers the drawer's name): the word fades on
    the way, the shell shrinks; a thin WHITE thread ties it to a tile at the same end of
    cheeses_unlabeled/ (the photo never moved). Returns (mini envelope, thread, photo tile)."""
    lab = v2.vault.drawers["cheeses_labeled/"]
    unl = v2.vault.drawers["cheeses_unlabeled/"]
    w, h = 0.42, 0.28
    body = RoundedRectangle(width=w, height=h, corner_radius=0.03, stroke_color=NOTE, stroke_width=2.5).set_fill(S.BG, 1)
    flap = VMobject(stroke_color=NOTE, stroke_width=2)
    flap.set_points_as_corners([[-w / 2 + 0.02, h / 2 - 0.02, 0], [0, h / 2 - h * 0.45, 0], [w / 2 - 0.02, h / 2 - 0.02, 0]])
    mini = VGroup(body, flap).move_to(lab.box.get_right() + LEFT * 0.3)
    c = env.copy()
    shell = VGroup(c.body, c.flap)
    scene.add(c)
    scene.play(Transform(shell, mini), FadeOut(c.text, target_position=mini.get_center()), run_time=1.0)
    scene.remove(c, c.text)
    scene.add(shell)
    ph = tile(None, 0.36, CLOUD).move_to(unl.box.get_right() + LEFT * 0.3)
    th = Line(mini.get_top(), ph.get_bottom(), color=NOTE, stroke_width=2)
    scene.play(FadeIn(ph, scale=0.6), run_time=0.3)
    scene.play(Create(th), run_time=0.6)
    return shell, th, ph


def stand_in_strip(call: str):
    """An output-only 3-row stand-in strip (never typed): the call as its heading on the title bar,
    'extra · stand-in' at the bar's right end. Returns (terminal, heading, tag)."""
    t = term(P_LABELING, rows=3, title=None)
    hd = strip_head(call).move_to([t.box.get_center()[0] - 1.6, t.box.get_top()[1] - t.bar_h / 2, 0])
    tg = on_bar(t, standin_row())
    return t, hd, tg


def above(t, mob, side=LEFT, buff: float = 0.14):
    """Place `mob` just above terminal t's box, aligned with its left or right edge."""
    return mob.next_to(t.box, UP, buff=buff).align_to(t.box, side)


class LabelsAndTokens(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 8, len(SAY)

        # ========================================================== 0. one click, its server side
        tr = tracker("C", 5)
        ref = lref("4, 6, 10, 13")
        ls = label_screen()
        cur = cursor_glyph().move_to([4.6, -1.6, 0])
        gouda = ls.choices["gouda"]
        yt0 = your_turn().move_to([0, -2.72, 0]).align_to(ls.win.frame, RIGHT)
        c33 = capture("33")
        t0 = term(P_LABELING, rows=12, title=None)
        hd0 = strip_head(CALL_ANNOTATE).move_to([t0.box.get_center()[0] - 1.6, t0.box.get_top()[1] - t0.bar_h / 2, 0])
        tg0 = on_bar(t0, standin_row())

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.6)
            vo.wait_until("click a task")
            self.play(FadeIn(VGroup(ls.win, ls.image), scale=0.98), FadeIn(ls.ill), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in ls.choices.values()], lag_ratio=0.2),
                      FadeIn(ls.submit), FadeIn(cur), run_time=0.8)
            vo.wait_until("pick a cheese")
            self.play(cur.animate.move_to(tip_to(cur, gouda.ring.get_center() + np.array([0.05, -0.05, 0]))),
                      run_time=0.7)
            gouda.dot.move_to(gouda.ring)
            self.play(Indicate(cur, color=INK, scale_factor=0.85), FadeIn(gouda.dot, scale=0.4),
                      gouda.ring.animate.set_stroke(TURN), gouda.text.animate.set_color(TURN), run_time=0.5)
            vo.wait_until("and submit")
            self.play(cur.animate.move_to(tip_to(cur, ls.submit.box.get_center() + np.array([0.2, -0.05, 0]))),
                      run_time=0.6)
            self.play(Indicate(cur, color=INK, scale_factor=0.85), Indicate(ls.submit.text, color=TURN, scale_factor=1.12),
                      run_time=0.5)
            vo.wait_until("Pause and label some")
            self.play(FadeIn(yt0, shift=UP * 0.15), run_time=0.4)
            flash_tag(self, yt0, TURN)
            vo.wait_until("Here is what one click becomes")
            gone = VGroup(ls, gouda.dot, cur, yt0)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(t0), FadeIn(hd0), FadeIn(tg0), run_time=0.5)
            vo.wait_until("a small JSON document")
            r33 = out(self, t0, c33.at((2, 4)), wrap=True, run_time=1.4)
            vo.wait_until("whose result says")
            res = substring(r33[0], '"result"')
            self.play(Indicate(res, color=INK, scale_factor=1.12), run_time=0.5)
            ch = substring(row_with(r33, '"choices": ["gouda"]'), '"choices": ["gouda"]')
            self.play(ch.animate.set_color(TURN), run_time=0.4)
            u_ch = under(ch, TURN, stroke=3)
            ok = substring(r33[-1], "HTTP 201")
            self.play(Create(u_ch), ok.animate.set_color(PASS), run_time=0.6)

        # ========================================================== 1. database, copy, notes, the console
        v2 = SignedTicket()
        chip_cp = grey_chip(COPY_CHIP).move_to([0, -1.75, 0])
        m = PipelineMap.at("S07")
        big = m.slide6_big
        rows6 = big.labeled.rows
        envs = VGroup(*[annotation(w, 2.0, 0.7, 20) for w in SLIDE6_ROWS]).arrange(DOWN, buff=0.1)
        envs.move_to(rows6.get_center())
        chip6 = grey_chip(SLIDE_CHIP).next_to(envs, DOWN, buff=0.35)
        lab_d = m.bucket1.drawers["cheeses_labeled/"]
        unl_d = m.bucket1.drawers["cheeses_unlabeled/"]

        cw = window(CONSOLE_URL, 8.6, 3.3).move_to([-0.9, 1.0, 0])
        crumb = VGroup(label("Buckets", 22, INK), label("›", 22, S.GREY), mono(BUCKET, 20, CLOUD),
                       label("›", 22, S.GREY), mono("cheeses_labeled/", 20, CLOUD)).arrange(RIGHT, buff=0.16)
        crumb.move_to([cw.frame.get_left()[0] + 0.45, cw.content.get_top()[1] - 0.32, 0], aligned_edge=LEFT)
        frows = VGroup()
        for i in range(3):
            fg = file_glyph(0.36, INK)
            bar = RoundedRectangle(width=3.2, height=0.14, corner_radius=0.07, stroke_width=0).set_fill(S.GREY_DARK, 1)
            r = VGroup(fg, bar).arrange(RIGHT, buff=0.25)
            frows.add(r)
        frows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(crumb, DOWN, buff=0.42).align_to(crumb, LEFT)
        frows.shift(RIGHT * 0.2)
        ill_c = illustration_tag().next_to(cw, RIGHT, buff=0.25).align_to(cw, UP)
        chip_j = grey_chip(JSON_CHIP).next_to(cw, DOWN, buff=0.25).align_to(cw, LEFT)
        env_big = annotation("gouda", 2.1, 1.2, 24).move_to([-4.85, -2.45, 0])
        shape = VGroup(mono(NOTE_SHAPE, 22, INK))
        sframe = RoundedRectangle(width=shape.width + 0.6, height=shape.height + 0.4, corner_radius=0.1,
                                  stroke_color=NOTE, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        shape.move_to(sframe)
        note_card = VGroup(sframe, shape).move_to([0, -2.45, 0])
        note_card.shift(RIGHT * (env_big.get_right()[0] + 0.5 - note_card.get_left()[0]))
        shape_chip = grey_chip("the shape of laptop/33").next_to(note_card, DOWN, buff=0.15).align_to(note_card, RIGHT)

        with self.voiceover(SAY[1]) as vo:
            gone = VGroup(t0, hd0, tg0, u_ch)
            self.play(FadeOut(gone), FadeOut(VGroup(*t0.lines)), run_time=0.5)
            drop(self, gone, *t0.lines)
            self.play(FadeIn(v2), run_time=0.7)
            vo.wait_until("Label Studio saves it in its database")
            env = v2.envelope_to_db(self, "gouda")
            self.play(Indicate(v2.db.text, color=INK, scale_factor=1.08), run_time=0.5)
            vo.wait_until("and the target storage writes a copy")
            self.play(FadeIn(chip_cp, shift=UP * 0.15), run_time=0.4)
            cp, th, ph = copy_to_labeled(self, v2, env)
            vo.wait_until("pointing back at the photo")
            self.play(Indicate(th, color=NOTE, scale_factor=1.0), run_time=0.6)
            vo.wait_until("which never moved")
            self.play(Indicate(ph.frame, color=CLOUD, scale_factor=1.25), run_time=0.7)
            vo.wait_until("The slide sorts photos into rows")
            gone = VGroup(v2, env, cp, th, ph, chip_cp)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(big), FadeIn(chip6, shift=UP * 0.15), run_time=0.7)
            self.play(Indicate(rows6, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("but on disk a label is a small JSON note")
            rest = VGroup(big.unlabeled, big.arrows, big.question, big.training, big.labeled[0], big.labeled[2])
            self.play(FadeOut(rest), run_time=0.4)
            drop(self, rest)
            self.play(*[w.animate.move_to(e.text) for w, e in zip(rows6, envs)], run_time=0.6)
            self.play(FadeIn(envs, scale=0.9), FadeOut(rows6), run_time=0.6)
            drop(self, rows6)
            vo.wait_until("and a labeled dataset is photos plus notes")
            self.play(FadeOut(VGroup(*[e.text for e in envs])), FadeIn(m), run_time=0.6)
            drop(self, *[e.text for e in envs])
            shells = [VGroup(e.body, e.flap) for e in envs]
            self.play(LaggedStart(*[FadeOut(s, target_position=lab_d.get_center(), scale=0.2) for s in shells],
                                  lag_ratio=0.12), m.light("labeled"), FadeOut(chip6), run_time=1.0)
            drop(self, envs, chip6, *shells)
            self.play(each([unl_d.text, lab_d.text], INK, scale=1.08, lag=0.4), run_time=1.0)
            vo.wait_until("In the console")
            self.play(FadeOut(m), track(tr, 6), run_time=0.5)
            drop(self, m)
            self.play(FadeIn(cw), FadeIn(ill_c), FadeIn(crumb, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("one JSON file per annotation")
            self.play(LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in frows], lag_ratio=0.25),
                      FadeIn(chip_j, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("Open one to see the note")
            self.play(Indicate(frows[0][0], color=INK, scale_factor=1.25), run_time=0.4)
            self.play(FadeIn(env_big, target_position=frows[0][0].get_center(), scale=0.3), run_time=0.8)
            self.play(FadeIn(note_card, shift=UP * 0.15), FadeIn(shape_chip, shift=LEFT * 0.15), run_time=0.6)
        self.play(Indicate(glyphs(shape[0], '["gouda"]'), color=NOTE, scale_factor=1.1), run_time=0.8)
        self.wait(1.4)      # the opened note is the beat's payoff: let it be read

        # ========================================================== 2. the CLI house, by name; ponder
        sm = StationMap(laid=True, lit=("studio", "cli"), shown=("door", "browser"))
        nm = sm.call("name")
        loc = sm.call("local")
        loc.label.next_to(loc.path, LEFT, buff=0.15)      # clear of the laptop frame's top edge

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(cw, ill_c, crumb, frows, chip_j, env_big, note_card, shape_chip)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(sm), run_time=0.7)
            vo.wait_until("The command line container")
            self.play(sm.join_cli(), run_time=0.8)
            vo.wait_until("by name")
            self.play(Create(nm), run_time=0.9)
            vo.wait_until("what if its address were")
            self.play(FadeIn(loc, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(loc.label, color=ROUTE, scale_factor=1.1), run_time=0.5)
        pc = ponder(self, PONDER_Q, seconds=6, center=(0, 0.6))

        # ========================================================== 3. localhost refused; the name works
        c41 = capture("41")
        s3 = term(P_LABELING, rows=3)
        xt3 = on_bar(s3, extra_row())
        br = sm.call("browser")
        pb = sm.phone()

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(pc), FadeIn(s3), track(tr, 6, extra=True), run_time=0.5)
            self.remove(pc)
            self.play(FadeIn(xt3), run_time=0.3)
            istep(self, s3, c41.line(108), type_time=0.7)
            r109 = out(self, s3, [(x, ERR) for x in c41.at(109)], wrap=True, run_time=0.5)
            self.play(FadeIn(loc.cross, scale=1.5), run_time=0.4)
            vo.wait_until("inside a container, localhost is that container")
            self.play(Indicate(sm.cli.body if hasattr(sm.cli, "body") else sm.cli, color=IMAGE, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("and nothing listens there")
            self.play(Indicate(loc.cross, color=ERR, scale_factor=1.3), run_time=0.6)
            vo.wait_until("The name works")
            istep(self, s3, c41.line(110), type_time=0.7)
            r111 = out(self, s3, [(x, PASS) for x in c41.at(111)], run_time=0.4)
            self.play(Indicate(nm.label, color=ROUTE, scale_factor=1.08), run_time=0.6)
            vo.wait_until("because the Docker network keeps a phone book")
            self.play(FadeIn(pb, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(pb.head, color=ROUTE, scale_factor=1.06), run_time=0.6)
            self.play(Create(br), run_time=0.9)

        # ========================================================== 4. the token; the 401
        tr_d = tracker("D", 1)
        acct = settings_page(("User Profile", "Account & Settings"),
                             [VGroup(token_row("Access Token", 4.6, INK), button("Copy"))], y=0.6, win_h=3.4)
        acct.rows[0][1].next_to(acct.rows[0][0].field, RIGHT, buff=0.3)
        yt4 = your_turn().next_to(acct.win, DOWN, buff=0.3).align_to(acct.win, RIGHT)
        c42 = capture("42")
        t4 = term(P_LABELING, rows=11)
        cn4 = above(t4, container_note(), LEFT)
        yt4b = above(t4, your_turn(), RIGHT)

        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(sm, sm.cli, nm, loc, loc.cross, br, pb, s3, xt3)
            self.play(FadeOut(gone), FadeOut(VGroup(*s3.lines)), run_time=0.5)
            drop(self, gone, *s3.lines)
            tr = swap_tracker(self, tr, tr_d)
            self.play(FadeIn(acct.win), FadeIn(acct.crumbs, shift=RIGHT * 0.15), FadeIn(acct.ill), run_time=0.6)
            vo.wait_until("copy your access token")
            self.play(FadeIn(acct.rows[0], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(acct.rows[0][1].text, color=TURN, scale_factor=1.12), FadeIn(yt4, shift=UP * 0.15),
                      run_time=0.6)
            vo.wait_until("then run the README command")
            gone = VGroup(acct, yt4)
            self.play(FadeOut(gone), track(tr, 2), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(t4), FadeIn(cn4, shift=DOWN * 0.1), run_time=0.5)
            ln = istep(self, t4, c42.line(32), type_time=1.4)
            fk = beside(row_tag("obviously fake"), ln, buff=0.3)
            pin(self, ln, fk)
            vo.wait_until("Pause and try it")
            self.play(FadeIn(yt4b, shift=DOWN * 0.1), run_time=0.4)
            flash_tag(self, yt4b, TURN)
            vo.wait_until("it fails with")
            lines42 = [c42.line(33), c42.line(36), (c42.line(37), ERR), c42.line(38), (c42.line(43), ERR), "…",
                       c42.line(66)]
            r42 = out(self, t4, lines42, wrap=True, run_time=1.2)
            sc = row_with(r42, "Response status code: 401")
            self.play(Indicate(substring(sc, "401"), color=ERR, scale_factor=1.3), run_time=0.6)
            vo.wait_until("ours says legacy token")
            a43 = substring(row_with(r42, '"detail"'), "legacy token")
            b43 = substring(row_with(r42, "authentication has been disabled"), "authentication has been disabled")
            self.play(each([a43, b43], ERR, scale=1.08, lag=0.4), run_time=1.0)
            u43 = VGroup(under(a43, ERR, stroke=3), under(b43, ERR, stroke=3))
            self.play(Create(u43), run_time=0.5)

        # ========================================================== 5. two kinds of token; legacy off
        two = settings_page(("User Profile", "Account & Settings"),
                            [token_row("personal access token"), token_row("legacy token")], y=0.95, win_h=3.3)
        pers, leg = two.rows
        s5, hd5, tg5 = stand_in_strip(CALL_JWT_GET)
        c27 = capture("27")
        p79 = code("data-labeling/cli.py", 75, 83, font_size=20, cuts={78: "SDK: "}).move_to([0, 0.15, 0])
        bar79 = line_bar(p79.code, 79 - 75, TURN, opacity=0.25)
        chip79 = grey_chip("the legacy client", color=TURN).next_to(p79, DOWN, buff=0.3).align_to(p79, RIGHT)

        with self.voiceover(SAY[5]) as vo:
            gone = VGroup(t4, cn4, yt4b, fk, u43)
            self.play(FadeOut(gone), FadeOut(VGroup(*t4.lines)), track(tr, 2, extra=True), run_time=0.5)
            drop(self, gone, *t4.lines)
            self.play(FadeIn(two.win), FadeIn(two.crumbs, shift=RIGHT * 0.15), FadeIn(two.ill), run_time=0.6)
            vo.wait_until("two kinds of token")
            self.play(LaggedStart(FadeIn(pers, shift=RIGHT * 0.15), FadeIn(leg, shift=RIGHT * 0.15), lag_ratio=0.4),
                      run_time=0.8)
            vo.wait_until("The page shows a newer personal token")
            self.play(Indicate(pers.label, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("the legacy kind is switched off")
            self.play(leg.animate.set_opacity(0.35), FadeIn(s5), FadeIn(hd5), FadeIn(tg5), run_time=0.5)
            r27 = out(self, s5, c27.at(2), run_time=0.4)
            off = substring(r27[0], '"legacy_api_tokens_enabled":false')
            self.play(off.animate.set_color(ERR), run_time=0.4)
            vo.wait_until("and cli.py speaks only legacy")
            gone = VGroup(two, s5, hd5, tg5)
            self.play(FadeOut(gone), FadeOut(VGroup(*s5.lines)), run_time=0.5)
            drop(self, gone, *s5.lines)
            self.play(FadeIn(p79), run_time=0.6)
            self.play(FadeIn(bar79), FadeIn(chip79, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(code_span(p79.code, 79 - 75, "Client("), color=TURN, scale_factor=1.1), run_time=0.6)
        self.wait(1.5)      # the panel arrives at the sentence's end: give it reading time

        # ========================================================== 6. the fix: legacy tokens on; copy that one
        org = settings_page(("Organization", "API Tokens Settings"), [label("legacy tokens", 22, INK)], y=0.95,
                            win_h=3.3)
        sw_off, sw_on = toggle(False), toggle(True)
        sw_off.next_to(org.rows[0], RIGHT, buff=0.6)
        sw_on.move_to(sw_off)
        s6, hd6, tg6 = stand_in_strip(CALL_JWT_POST)
        c43 = capture("43")
        two2 = settings_page(("User Profile", "Account & Settings"),
                             [token_row("personal access token"), token_row("legacy token", color=TURN)], y=0.95,
                             win_h=3.3)
        yt6 = your_turn().move_to([0, -2.0, 0]).align_to(two2.win, RIGHT)
        sdk = grey_chip(SDK_CHIP).move_to([0, -2.0, 0]).align_to(two2.win, LEFT)

        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(p79, bar79, chip79)
            self.play(FadeOut(gone), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(org.win), FadeIn(org.crumbs, shift=RIGHT * 0.15), FadeIn(org.ill),
                      FadeIn(org.rows[0]), FadeIn(sw_off), run_time=0.6)
            vo.wait_until("enable legacy tokens")
            self.play(ReplacementTransform(sw_off, sw_on), Indicate(org.rows[0], color=PASS, scale_factor=1.06),
                      FadeIn(s6), FadeIn(hd6), FadeIn(tg6), run_time=0.7)
            r43 = out(self, s6, c43.at(2), run_time=0.4)
            on = substring(r43[0], '"legacy_api_tokens_enabled":true')
            self.play(on.animate.set_color(PASS), run_time=0.4)
            self.wait(1.2)      # the GREEN true is the proof of the fix: let it be read
            vo.wait_until("Then copy the legacy token")
            gone = VGroup(org, sw_on, s6, hd6, tg6)
            self.play(FadeOut(gone), FadeOut(VGroup(*s6.lines)), run_time=0.5)
            drop(self, gone, *s6.lines)
            self.play(FadeIn(two2), run_time=0.6)
            self.play(Indicate(two2.rows[1].label, color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("not the personal one")
            self.play(Indicate(two2.rows[0].label, color=S.GREY, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Pause and do both")
            self.play(FadeIn(yt6, shift=UP * 0.15), FadeIn(sdk, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, yt6, TURN)
        self.wait(2.0)      # the unspoken SDK chip needs reading time

        # ========================================================== 7. -p and -t with the legacy token; amanita
        c44 = capture("44")
        t7 = term(P_LABELING, rows=12)
        cn7 = above(t7, container_note(), LEFT)
        ours = above(t7, grey_chip("ours: 3 · yours: 21", color=TURN), RIGHT)
        yt7 = on_bar(t7, turn_row())
        rm = readme(204)
        k = rm.index("['amanita']}") + len("['amanita']}")
        body = VGroup(*[mono(s, 20, INK) for s in soft([rm[:k] + " …"], 62)]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rc = readme_card(204, body).move_to([0, 0.6, 0])
        am = next(glyphs(r, "'amanita'") for r in body if "'amanita'" in r.text)
        err7 = erratum_tag().next_to(rc, DOWN, buff=0.3).align_to(rc, LEFT)
        chip_am = grey_chip(AMANITA_CHIP).next_to(err7, RIGHT, buff=0.3)
        t8 = term(P_LABELING, rows=5)
        err8 = above(t8, erratum_tag(), LEFT)
        chip8 = grey_chip(TYPO_CHIP).next_to(err8, RIGHT, buff=0.3)

        with self.voiceover(SAY[7]) as vo:
            gone = VGroup(two2, yt6, sdk)
            self.play(FadeOut(gone), track(tr, 2), run_time=0.5)
            drop(self, gone)
            self.play(FadeIn(t7), FadeIn(cn7, shift=DOWN * 0.1), run_time=0.5)
            ln1 = istep(self, t7, c44.line(32), type_time=1.0)
            vo.wait_until("and it lists project 1")
            r44 = out(self, t7, [c44.line(33), c44.line(34), (c44.line(35), PASS), c44.line(36)], wrap=True,
                      run_time=0.8)
            self.play(Indicate(substring(row_with(r44, "1 Cheese labels"), "1 Cheese labels"), color=PASS,
                               scale_factor=1.1), run_time=0.6)
            rep = row_with(r44, "0x7f651f1b71a0")
            obj = beside(row_tag("object reprs, not dicts"), rep, buff=0.4)
            pin(self, rep, obj)
            self.play(FadeIn(yt7), run_time=0.3)
            vo.wait_until("Then dash t with your token")
            self.play(FadeOut(yt7), track(tr, 3), run_time=0.4)
            self.remove(yt7)
            istep(self, t7, c44.line(37), type_time=1.0)
            vo.wait_until("3 tasks in our stand-in")
            r38 = out(self, t7, c44.at((38, 41)), wrap=True, run_time=0.6)
            n3 = substring(row_with(r38, "Number of tasks: 3"), "Number of tasks: 3")
            self.play(n3.animate.set_color(TURN), FadeIn(ours, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(n3, color=TURN, scale_factor=1.08), run_time=0.5)
            vo.wait_until("ours has one labeled")
            self.play(FadeOut(ours), run_time=0.3)      # its row is about to scroll away
            self.remove(ours)
            r42b = out(self, t7, c44.at(42), wrap=True, run_time=1.0)
            gd = substring(row_with(r42b, "['gouda']"), "['gouda']")
            self.play(gd.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(gd, color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("Pause and run both")
            self.play(FadeIn(yt7), run_time=0.3)
            flash_tag(self, yt7, TURN)
            vo.wait_until("The README's sample says amanita")
            gone = VGroup(t7, cn7, yt7, obj)
            self.play(FadeOut(gone), FadeOut(VGroup(*t7.lines)), run_time=0.5)
            drop(self, gone, *t7.lines)
            self.play(FadeIn(rc, shift=UP * 0.15), run_time=0.6)
            self.play(am.animate.set_color(S.GREY), FadeIn(err7, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the format is the same")
            self.play(FadeIn(chip_am, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(am, color=S.GREY, scale_factor=1.12), run_time=0.6)

        # unspoken: the -k you forgot (TRACKER D3 · extra)
        gone = VGroup(rc, err7, chip_am)
        self.play(FadeOut(gone), track(tr, 3, extra=True), run_time=0.5)
        drop(self, gone)
        self.play(FadeIn(t8), run_time=0.4)
        ln8 = istep(self, t8, c42.line(67), type_time=0.5)
        fk8 = beside(row_tag("extra · forgot -k"), ln8)
        pin(self, ln8, fk8)
        r68 = out(self, t8, c42.at((68, 69)), wrap=True, run_time=0.6)
        ir = substring(row_with(r68, "i required"), "i required")
        self.play(ir.animate.set_color(S.GREY), FadeIn(err8, shift=UP * 0.1), FadeIn(chip8, shift=UP * 0.1),
                  run_time=0.6)
        self.play(Create(under(ir, S.GREY, stroke=3)), run_time=0.5)
        self.wait(1.2)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
