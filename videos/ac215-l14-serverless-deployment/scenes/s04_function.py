"""S04 · Part 1: write a function — tracker [1.1] 1 → 6, then [1.2] 1 → 4; lecture slides 10–12.

Beats (script.md "## S04"; one voiceover block each):
0. No tracker. LECTURE 14 · 11. Slide 11 in one picture: a GREEN `main.py` page in a dashed BLUE
   outline; three PINK bolts strike it ("file upload", "database change", "HTTP request"); the first
   two go GREY-dashed, the third stays PINK with the chip "today". A GOLD meter under it ticks only
   while a bolt is active; on "scales by itself" the outline duplicates once.
1. LECTURE 14 · 11–12. Slide 12's four steps as a GREY checklist; a product-name card (tag
   `erratum`): "Cloud Functions" → "Cloud Run functions (formerly Cloud Functions 2nd gen)" + GREY
   chip "the slide's link still lands here"; a README card (line 99).
2. TRACKER [1.1] 1. The checklist shrinks to a text-free icon at the right edge. CONSOLE
   (README:99-103, `illustration`): "Cloud Run → Services" with **Write a function** pulsing (GREY chip
   "narrow window: under More actions"), then the form "Create service". [1.1] 2: a GREY dialog
   "Enable required APIs? · Enable" (chip "only if prompted"). [1.1] 3: the worksheet card
   `translate-function` flies up into "Service name"; "Region" fills `northamerica-northeast2 (Toronto)`.
3. [1.1] 4: "Runtime" → Python 3.12 + GREY chip (tag `erratum`, under the form) "the older README
   (4eaf343): Python 3.10 · the slides name no runtime". [1.1] 5: Allow public access + a GREY browser icon "anyone with
   the URL"; Create pulses.
4. [1.1] 6: the form gives way to a schematic Source editor (tabs `main.py`, `requirements.txt`, GREY
   sample bars, chip "sample code · replaced next"). ▶ your turn. GOLD cost tags (two rows).
5. TRACKER [1.2] 1. GREY chip "read-only? select Edit source". CODE(tutorial/function/main.py: 3–12)
   slides into the `main.py` tab; line 7's decorator YELLOW, line 8's `hello_http` GREEN, lines 9–11
   light one by one and each default is underlined GREY.
6. LECTURE 14 · 10. The code panel gives way to main.py 7–12 at the bottom; the lecture sketch card (tag `erratum`) with the GREY
   note "the slide calls translate(text, src, dest) by position" and the googletrans 4.0.0rc1
   signature card; `dest` flashes RED under the note's second argument; line 12's keywords GREEN.
7. [1.2] 2. LECTURE 14 · 11–12. CODE(tutorial/function/requirements.txt: 1–2) in the
   `requirements.txt` tab; both pins GREEN, chip "two exact versions"; GREY chip "newer googletrans:
   async · breaks this sync handler".
8. [1.2] 3. CONSOLE field "Function entry point" types `hello_http`; a GREEN name tag flies to line 8
   (main.py 7–8 above the form) and clicks onto `def hello_http`. README card (lines 150–151). [1.2] 4: **Save and
   redeploy** pulses, GREY status "Waiting for the revision to become ready". ▶ your turn.
9. LECTURE 14 · 11–12. The checklist returns from the right edge; item 3 (tag `erratum`) expands into
   three GREEN chips `main.py`, `requirements.txt`, `entry point: hello_http`. Fade out: empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from explainer import style as S

SAY = NARRATION["S04"]

MAIN = "tutorial/function/main.py"
REQS = "tutorial/function/requirements.txt"
STEPS12 = ("open the console page", "enable the APIs", "create a Python file", "deploy")   # slide 12
EVENTS = ("file upload", "database change", "HTTP request")                              # slide 11
REGION_VALUE = f"{REGION} ({REGION_CITY})"
RUNTIME = "Python 3.12"
SIGNATURE = "translate(text, dest='en', src='auto')"     # googletrans 4.0.0rc1 (digest, SLIDES Conflict 3)
SLIDE_CALL = "translate(text, src, dest)"
EDITOR_TOP = 2.15                                        # top of the editor body / code panel


# ------------------------------------------------------------------ pictures of this scene
def fn_box(color=CLOUD) -> VGroup:
    """Slide 11's function: a GREEN main.py page inside a dashed BLUE outline. .frame .page"""
    fr = outline_box(2.8, 2.5, color, solid=False)
    page = file_glyph(1.2, OWN)
    name = mono("main.py", 24, INK)
    inner = VGroup(page, name).arrange(DOWN, buff=0.18).move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.page = fr, inner
    return g


def check_list(size: float = 22) -> VGroup:
    """Slide 12's four steps: GREY boxes + words. .items (rows) .marks"""
    rows = []
    for i, s in enumerate(STEPS12, start=1):
        mk = RoundedRectangle(width=0.32, height=0.32, corner_radius=0.05, stroke_color=S.GREY, stroke_width=2.5)
        t = label(f"{i}.  {s}", size, INK)
        rows.append(VGroup(mk, t).arrange(RIGHT, buff=0.22))
    items = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
    hd = label("four steps", 20, S.GREY)
    g = VGroup(hd, items).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    g.items, g.head = items, hd
    return g


def mini_list() -> VGroup:
    """The text-free checklist icon (the shrunken checklist at the right edge)."""
    fr = RoundedRectangle(width=0.8, height=0.56, corner_radius=0.06, stroke_color=S.GREY, stroke_width=2)
    rows = VGroup()
    for i, w in enumerate((0.42, 0.34, 0.46, 0.22)):
        sq = Rectangle(width=0.07, height=0.07, stroke_color=S.GREY, stroke_width=1.5)
        bar = Line(ORIGIN, RIGHT * w, color=S.GREY, stroke_width=2).next_to(sq, RIGHT, buff=0.06)
        rows.add(VGroup(sq, bar))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to(fr)
    return VGroup(fr, rows)


def name_card() -> VGroup:
    """The product-name card: the lecture's name above, today's name below (an arrow between).
    .old .new .arrow .frame"""
    old_t = label("Cloud Functions", 24, S.GREY)
    old_c = label("the lecture's name", 20, S.GREY)
    old = VGroup(old_t, old_c).arrange(DOWN, buff=0.1)
    new_t = label("Cloud Run functions", 24, INK)
    new_c = label("(formerly Cloud Functions 2nd gen)", 20, S.GREY)
    new = VGroup(new_t, new_c).arrange(DOWN, buff=0.1)
    ar = Arrow(UP * 0.35, DOWN * 0.35, buff=0, color=S.GREY, stroke_width=3,
               max_tip_length_to_length_ratio=0.35)
    inner = VGroup(old, ar, new).arrange(DOWN, buff=0.18)
    fr = box(inner.width + 0.8, inner.height + 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr)
    g = VGroup(fr, old, ar, new)
    g.frame, g.old, g.arrow, g.new, g.old_t = fr, old, ar, new, old_t
    return g


def dialog() -> VGroup:
    """The GREY 'Enable required APIs?' dialog (README:102), opaque. .button"""
    t = label("Enable required APIs?", 22, INK)
    bt = label("Enable", 20, INK)
    bb = RoundedRectangle(width=bt.width + 0.5, height=bt.height + 0.28, corner_radius=0.08, stroke_color=CLOUD,
                          stroke_width=2.5).set_fill(CLOUD, 0.15)
    bt.move_to(bb)
    btn = VGroup(bb, bt)
    inner = VGroup(t, btn).arrange(RIGHT, buff=0.5)
    fr = RoundedRectangle(width=inner.width + 0.7, height=inner.height + 0.6, corner_radius=0.12,
                          stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.button = btn
    return g


def tab(text: str, active: bool) -> VGroup:
    t = mono(text, 20, INK if active else S.GREY)
    b = RoundedRectangle(width=t.width + 0.44, height=0.44, corner_radius=0.07,
                         stroke_color=INK if active else S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def tab_row(active: int = 0) -> VGroup:
    """'Source' + the two editor tabs (main.py, requirements.txt), left at -6.45, centre y 2.55."""
    word = label("Source", 22, S.GREY)
    tabs = [tab("main.py", active == 0), tab("requirements.txt", active == 1)]
    g = VGroup(word, *tabs).arrange(RIGHT, buff=0.22)
    g.move_to([-6.45 + g.width / 2, 2.53, 0])
    g.tabs = tabs
    return g


def set_tab(row: VGroup, active: int):
    """ANIMs: tab `active` lit (INK outline + words), the other dimmed."""
    anims = []
    for i, tb in enumerate(row.tabs):
        on = i == active
        anims += [tb.box.animate.set_stroke(INK if on else S.GREY_DARK), tb.text.animate.set_color(INK if on else S.GREY)]
    return anims


def sample_body(body_w: float, body_h: float) -> VGroup:
    """The editor body before the code arrives: GREY bars (no invented code). .frame .bars"""
    fr = RoundedRectangle(width=body_w, height=body_h, corner_radius=0.12, stroke_color=S.GREY_DARK,
                          stroke_width=2).set_fill(TERM_BG, 1)
    bars = VGroup()
    for w in (3.2, 4.6, 0.0, 2.4, 5.6, 4.0, 3.0):
        bars.add(Line(ORIGIN, RIGHT * max(w, 0.01), color=S.GREY_DARK, stroke_width=8 if w else 0))
    bars.arrange(DOWN, aligned_edge=LEFT, buff=0.33)
    bars.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.5)
    g = VGroup(fr, bars)
    g.frame, g.bars = fr, bars
    return g


def note_row() -> VGroup:
    """GREY note: 'the slide calls, by position:' over the mono call. .call (mono_line)"""
    call = mono_line(SLIDE_CALL, 22, S.GREY)
    g = VGroup(label("the slide calls, by position:", 20, S.GREY), call)
    g.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    g.call = call
    return g


def signature_card() -> VGroup:
    """The googletrans 4.0.0rc1 signature on a GREY card. .sig (mono_line)"""
    sig = mono_line(SIGNATURE, 22, INK)
    c = card([sig], head="googletrans 4.0.0rc1 · its signature")
    c.sig = sig
    return c


class WriteAFunction(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S04"] == 10, len(SAY)

        # ========================================================== 0. slide 11: what a function is
        ref = lref("11")
        fb = fn_box().move_to([0.6, 0.5, 0])
        bolts, names, strikes = [], [], []
        for i, (ev, y) in enumerate(zip(EVENTS, (1.7, 0.5, -0.7))):
            b = bolt(0.75).move_to([-2.9, y, 0])
            n = label(ev, 24, ROUTE).next_to(b, LEFT, buff=0.3)
            bolts.append(b)
            names.append(n)
            strikes.append(route(b.get_right() + RIGHT * 0.05, fb.frame.get_left() + UP * (y - 0.5) * 0.5))
        today = chip("today", TURN).next_to(names[2], DOWN, buff=0.2).align_to(names[2], RIGHT)
        m_fr = RoundedRectangle(width=2.8, height=0.28, corner_radius=0.07, stroke_color=COST, stroke_width=2.5)
        m_fr.next_to(fb, DOWN, buff=0.35)
        m_fill = Rectangle(width=0.02, height=0.16, stroke_width=0).set_fill(COST, 0.85)
        m_fill.align_to(m_fr, LEFT).shift(RIGHT * 0.05).set_y(m_fr.get_y())
        m_lbl = label("billed while it runs", 22, COST).next_to(m_fr, DOWN, buff=0.15)
        fb2 = fn_box().move_to(fb).shift(RIGHT * 3.4)
        m_steps = iter((0.55, 1.1, 1.65, 2.2, 2.65))

        def tick():
            w = next(m_steps)
            return m_fill.animate.stretch_to_fit_width(w).align_to(m_fr, LEFT).shift(RIGHT * 0.05)

        def hit(i, rt=0.7):
            self.play(GrowArrow(strikes[i]), tick(), Indicate(fb.frame, color=ROUTE, scale_factor=1.03), run_time=rt)
            self.play(FadeOut(strikes[i]), run_time=0.3)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(fb, scale=0.95), run_time=0.7)
            self.play(Create(m_fr), FadeIn(m_fill), FadeIn(m_lbl), run_time=0.6)
            vo.wait_until("lightweight code")
            self.play(Indicate(fb.page, color=OWN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("that an event starts")
            self.play(Indicate(fb.frame, color=ROUTE, scale_factor=1.04), run_time=0.8)
            vo.wait_until("like a file upload")
            self.play(FadeIn(bolts[0], shift=DOWN * 0.2), FadeIn(names[0]), run_time=0.5)
            hit(0)
            vo.wait_until("a database change")
            self.play(FadeIn(bolts[1], shift=DOWN * 0.2), FadeIn(names[1]), run_time=0.5)
            hit(1)
            vo.wait_until("or today")
            dashed = [DashedVMobject(bolt(0.75, S.GREY), num_dashes=14).set_stroke(S.GREY, 2.5).move_to(b)
                      for b in bolts[:2]]
            self.play(*[ReplacementTransform(b, d) for b, d in zip(bolts[:2], dashed)],
                      *[n.animate.set_color(S.GREY) for n in names[:2]], run_time=0.6)
            vo.wait_until("an HTTP request")
            self.play(FadeIn(bolts[2], shift=DOWN * 0.2), FadeIn(names[2]), FadeIn(today, shift=UP * 0.1),
                      run_time=0.5)
            hit(2)
            vo.wait_until("It is billed while it runs")
            hit(2, 0.9)
            self.play(Indicate(m_lbl, color=COST, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and scales by itself")
            s4 = route(strikes[2].get_start(), strikes[2].get_end())
            self.play(TransformFromCopy(fb, fb2), GrowArrow(s4), tick(), run_time=0.9)
            self.play(FadeOut(s4), run_time=0.3)

        # ========================================================== 1. slide 12's four steps + the name
        ref2 = lref("11–12")
        cl = check_list(24).move_to([-6.3, 2.45, 0], aligned_edge=UL)
        nc = name_card().move_to([3.4, 1.15, 0])
        nc_tag = erratum_tag().move_to(nc.frame.get_corner(UR) + np.array([-0.75, 0, 0]))
        link = grey_chip("the slide's link still lands here").next_to(nc, DOWN, buff=0.25)
        words = VGroup(label("open", 22, INK), label("Cloud Run → Services", 22, INK, weight=BOLD),
                       label("and select", 22, INK), label("Write a function", 22, INK, weight=BOLD)
                       ).arrange(RIGHT, buff=0.14)
        base = words[2][0].get_bottom()[1]                # baseline: "a" of "and select"
        for w in words:                                   # "open" has a descender: sit it on the baseline
            w.shift(UP * (base - w[0].get_bottom()[1]))
        rc = readme_card(99, words)
        rc.move_to([0, -2.6, 0])

        with self.voiceover(SAY[1]) as vo:
            gone0 = VGroup(fb, fb2, *dashed, bolts[2], *names, today, m_fr, m_fill, m_lbl)
            self.play(FadeOut(gone0), FadeTransform(ref, ref2), run_time=0.6)
            self.play(FadeIn(cl.head), run_time=0.3)
            for item, phrase in zip(cl.items, ("open the console", "enable the APIs", "write a Python file",
                                               "deploy")):
                vo.wait_until(phrase)
                self.play(FadeIn(item, shift=RIGHT * 0.15), run_time=0.45)
            vo.wait_until("One name has changed")
            self.play(FadeIn(nc.frame), FadeIn(nc.old), run_time=0.5)
            vo.wait_until("are now Cloud Run functions")
            nc_x = strike(nc.old_t, S.GREY)
            self.play(GrowArrow(nc.arrow), FadeIn(nc.new, shift=DOWN * 0.15), Create(nc_x),
                      FadeIn(nc_tag), run_time=0.8)
            self.play(FadeIn(link, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("so the README starts")
            self.play(FadeIn(rc, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Write a function")
            self.play(Indicate(rc.body[3], color=TURN, scale_factor=1.06), run_time=0.7)

        # ========================================================== 2. Create service: APIs, name, region
        tr = tracker_11(1)
        mini = mini_list().move_to([6.05, 2.5, 0])
        FORM_UL = np.array([-6.45, 2.72, 0])
        svc = console_form("Services", [("button", "Write a function")], path="Cloud Run", form_w=8.2)
        svc.move_to(FORM_UL, aligned_edge=UL)
        f = console_form("Create service", [("Service name", ""), ("Region", ""), ("Runtime", ""),
                                            ("note", "Authentication"), ("radio", "Allow public access", False),
                                            ("button", "Create")], form_w=8.2)
        f.move_to(FORM_UL, aligned_edge=UL)
        ill = illustration_tag().move_to(f.frame.get_corner(UR) + np.array([-0.95, 0, 0]))
        ill_s = illustration_tag().move_to(svc.frame.get_corner(UR) + np.array([-0.95, 0, 0]))
        RX = f.frame.get_right()[0] + 0.3                 # the right column for chips
        narrow = grey_chip("narrow window: under More actions")
        narrow.next_to(svc.rows[0], RIGHT, buff=0.5)
        dlg = dialog().move_to(f.frame).shift(UP * 0.2)
        if_asked = grey_chip("only if prompted").move_to([RX, dlg.get_y(), 0], aligned_edge=LEFT)
        ws = worksheet_card(FUNCTION, "function").move_to([f.frame.get_x(), -3.05, 0])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(nc, nc_tag, nc_x, link, rc)), ReplacementTransform(cl, mini),
                      FadeIn(tr, shift=DOWN * 0.15), FadeIn(svc, shift=UP * 0.1), FadeIn(ill_s),
                      FadeIn(narrow, shift=LEFT * 0.1), run_time=0.8)
            self.play(svc.press(0), run_time=0.8)
            vo.wait_until("Enable the APIs")
            self.play(FadeOut(narrow), ReplacementTransform(svc, f), ReplacementTransform(ill_s, ill),
                      run_time=0.5)
            self.play(track(tr, 2), FadeIn(dlg, scale=0.95), FadeIn(if_asked, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("if it asks")
            self.play(Indicate(dlg.button, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Name the service")
            self.play(FadeOut(dlg), FadeOut(if_asked), track(tr, 3), FadeIn(ws, shift=UP * 0.2), run_time=0.6)
            self.play(ws.animate.move_to(f.rows[0].field).set_opacity(0), f.fill(0, FUNCTION), run_time=0.9)
            self.remove(ws)
            vo.wait_until("choose your region")
            self.play(f.fill(1, REGION_VALUE), run_time=0.9)

        # ========================================================== 3. runtime, public access, Create
        old_rt = grey_chip("the older README (4eaf343): Python 3.10 · the slides name no runtime")
        rt_tag = erratum_tag()
        VGroup(rt_tag, old_rt).arrange(RIGHT, buff=0.2).next_to(f, DOWN, buff=0.35).align_to(f, LEFT)
        radio = f.rows[4]
        web = browser_icon(0.55, name=None)
        anyone = label("anyone with the URL", 20, S.GREY)
        pub = VGroup(web, anyone).arrange(RIGHT, buff=0.18).next_to(radio.text, RIGHT, buff=0.55)

        with self.voiceover(SAY[3]) as vo:
            self.play(track(tr, 4), f.fill(2, RUNTIME), run_time=0.8)
            vo.wait_until("the older README said")
            self.play(FadeIn(old_rt, shift=LEFT * 0.15), FadeIn(rt_tag), run_time=0.6)
            vo.wait_until("Choose Allow public access")
            self.play(track(tr, 5), radio.tick.animate.set_opacity(1), Indicate(radio.text, color=TURN,
                                                                                scale_factor=1.06), run_time=0.7)
            vo.wait_until("so anyone with the URL")
            self.play(FadeIn(pub, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("then Create")
            self.play(f.press(5), run_time=0.8)

        # ========================================================== 4. the Source editor, your turn, cost
        tabs = tab_row(0)
        probe = code(MAIN, 3, 12, font_size=20)
        body = sample_body(probe.width, probe.height).move_to([0, EDITOR_TOP - probe.height / 2, 0])
        sample = grey_chip("sample code · replaced next").move_to(body.frame.get_corner(DR) + np.array([-2.0, 0.45, 0]))
        yt = your_turn().next_to(tabs, RIGHT, buff=0.5)
        cost1 = cost_tag("billed as a Cloud Run service · every deploy runs a build")
        cost2 = cost_tag("the build stores an image · check the pricing page")
        costs = VGroup(cost1, cost2).arrange(DOWN, buff=0.15).move_to([0, -2.85, 0])
        assert costs.width < 12.8

        with self.voiceover(SAY[4]) as vo:
            self.play(track(tr, 6), FadeOut(VGroup(old_rt, rt_tag, pub)), run_time=0.5)
            self.play(FadeOut(f, shift=UP * 0.1), FadeOut(ill), FadeIn(tabs, shift=UP * 0.1),
                      FadeIn(body, shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[Create(b) for b in body.bars], lag_ratio=0.15), FadeIn(sample), run_time=1.0)
            vo.wait_until("pause and create yours")
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)
            vo.wait_until("A gold tag")
            self.play(FadeIn(cost1, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(cost2, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and every deploy runs a build")
            flash_tag(self, cost1, COST)

        # ========================================================== 5. main.py: decorator, name, three args
        tr12 = tracker_12(1)
        p = code(MAIN, 3, 12, font_size=20).move_to(body.frame)
        ro = grey_chip("read-only? select Edit source").next_to(tabs, RIGHT, buff=0.5)
        deco = code_span(p.code, 4, "@functions_framework.http")
        name8 = code_span(p.code, 5, "hello_http")
        bars = [line_bar(p.code, k, TURN) for k in (6, 7, 8)]
        dflt = [code_span(p.code, k, s) for k, s in ((6, '"Welcome to AC215"'), (7, '"en"'), (8, '"es"'))]
        unders = [under(d, S.GREY, stroke=3) for d in dflt]
        deco_bar = line_bar(p.code, 4, TURN)
        name_ring = ring(VGroup(*name8), OWN)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(yt, cost1, cost2)), run_time=0.4)
            tr = swap_tracker(self, tr, tr12)
            self.play(FadeIn(ro, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("with the tutorial's handler")
            self.play(FadeOut(VGroup(body, sample), shift=LEFT * 0.4), FadeIn(p, shift=LEFT * 0.6), run_time=0.9)
            vo.wait_until("The decorator")
            # syntax colours already match TURN/OWN: emphasise with a bar and a ring instead
            self.play(FadeIn(deco_bar), *[g.animate.set_color(TURN) for g in deco], run_time=0.6)
            self.add(p, deco_bar)  # re-adding the panel would cover the bar: keep it on top
            vo.wait_until("hello underscore HTTP")
            self.play(Create(name_ring), *[g.animate.set_color(OWN) for g in name8], run_time=0.6)
            self.add(p, deco_bar, name_ring)
            self.play(Indicate(VGroup(*name8), color=OWN, scale_factor=1.15), run_time=0.7)
            self.add(p, deco_bar, name_ring)
            vo.wait_until("It takes text")
            self.play(FadeIn(bars[0]), run_time=0.4)
            vo.wait_until("source and")
            self.play(FadeIn(bars[1]), run_time=0.4)
            vo.wait_until("destination from the request")
            self.play(FadeIn(bars[2]), run_time=0.4)
            vo.wait_until("each with a default")
            self.play(LaggedStart(*[Create(u) for u in unders], lag_ratio=0.3), run_time=0.9)

        # ========================================================== 6. the lecture sketch passes source second
        ref3 = lref("10")
        sk = sketch_card()
        sk.move_to([-6.5, 2.45, 0], aligned_edge=UL)
        sk_tag = erratum_tag().move_to(sk.frame.get_corner(UR) + np.array([-0.75, 0, 0]))
        nt = note_row()
        sig = signature_card()
        right = VGroup(nt, sig).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right.move_to([sk.get_right()[0] + 0.5, 2.1, 0], aligned_edge=UL)
        # the signature's `dest` sits right under the note's second argument (same column)
        src2 = substring(nt.call, "src")
        dest2 = substring(sig.sig, "dest")
        sig.shift(RIGHT * (nt.call.get_left()[0] - sig.sig.get_left()[0]))
        p6 = code(MAIN, 7, 12, font_size=20)
        p6.move_to([0, BOTTOM + 0.05 + p6.height / 2, 0])
        for g in code_span(p6.code, 0, "@functions_framework.http"):
            g.set_color(TURN)
        for g in code_span(p6.code, 1, "hello_http"):
            g.set_color(OWN)
        kw = [code_span(p6.code, 5, "src=source"), code_span(p6.code, 5, "dest=destination")]

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(tabs, ro, deco_bar, name_ring, *bars, *unders)), FadeTransform(ref2, ref3), run_time=0.5)
            # lines 7-12 travel to the new panel (same text); lines 3-4 leave; the frame follows
            self.play(FadeOut(VGroup(*p.code.code_lines[:4], p.header)), run_time=0.3)
            self.play(ReplacementTransform(p.code.background, p6.code.background),
                      *[ReplacementTransform(p.code.code_lines[4 + i], p6.code.code_lines[i]) for i in range(6)],
                      FadeIn(p6.header, shift=DOWN * 0.3), run_time=0.8)
            self.remove(p)
            self.add(p6)
            self.play(FadeIn(sk, shift=RIGHT * 0.2), FadeIn(sk_tag), run_time=0.6)
            vo.wait_until("passes source second")
            self.play(FadeIn(nt, shift=DOWN * 0.1), run_time=0.5)
            self.play(*[g.animate.set_color(INK) for g in src2], run_time=0.4)
            self.add(nt)
            vo.wait_until("In this library")
            self.play(FadeIn(sig, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("the second slot is the destination")
            u_src, u_dest = under(src2, ERR, stroke=3), under(dest2, ERR, stroke=3)
            self.play(*[g.animate.set_color(ERR) for g in dest2], Create(u_src), Create(u_dest), run_time=0.6)
            self.add(sig)
            self.play(each(list(dest2), ERR, scale=1.2, lag=0.1), run_time=0.7)
            self.add(sig)
            vo.wait_until("the handler passes them by name")
            self.play(*[g.animate.set_color(OWN) for span in kw for g in span], run_time=0.6)
            self.add(p6)
            self.play(each([kw[0], kw[1]], OWN, scale=1.12, lag=0.3), run_time=0.9)
            self.add(p6)

        # ========================================================== 7. requirements.txt: two exact pins
        ref4 = lref("11–12")
        tabs2 = tab_row(0)
        q = code(REQS, 1, 2).move_to([-6.47, EDITOR_TOP, 0], aligned_edge=UL)
        pins = [code_span(q.code, 0, "==3.10.2"), code_span(q.code, 1, "==4.0.0rc1")]
        exact = ok_chip("two exact versions").next_to(q, RIGHT, buff=0.4)
        asy = grey_chip("newer googletrans: async · breaks this sync handler")
        asy.next_to(q, DOWN, buff=0.3).align_to(q, LEFT)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(sk, sk_tag, nt, sig, u_src, u_dest)), FadeTransform(ref3, ref4),
                      FadeOut(p6, shift=LEFT * 0.6), track(tr, 2), run_time=0.7)
            self.play(FadeIn(tabs2, shift=UP * 0.1), run_time=0.4)
            self.play(*set_tab(tabs2, 1), FadeIn(q, shift=LEFT * 0.6), run_time=0.8)
            vo.wait_until("two exact pins")
            self.play(*[g.animate.set_color(OWN) for span in pins for g in span], run_time=0.6)
            self.add(q)
            self.play(FadeIn(exact, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("The newer googletrans")
            self.play(FadeIn(asy, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("would break this simple handler")
            self.play(Indicate(asy.text, color=INK, scale_factor=1.05), run_time=0.7)

        # ========================================================== 8. entry point, Save and redeploy
        p7 = code(MAIN, 7, 8).move_to([-6.47, EDITOR_TOP, 0], aligned_edge=UL)
        for g in code_span(p7.code, 0, "@functions_framework.http"):
            g.set_color(TURN)
        def_name = code_span(p7.code, 1, "hello_http")
        for g in def_name:
            g.set_color(OWN)
        ef = console_form("Source", [("Function entry point", ""), ("button", "Save and redeploy")], form_w=6.3)
        ef.move_to([-6.45, p7.get_bottom()[1] - 0.45, 0], aligned_edge=UL)
        ef_ill = illustration_tag().move_to(ef.frame.get_corner(UR) + np.array([-0.95, 0, 0]))
        rc2 = readme_card((150, 151), "This is the Python function\nthe serving framework should call,\n"
                                      "not the filename or service name.", quote=True, size=20)
        rc2.move_to([6.5, ef.get_top()[1], 0], aligned_edge=UR)
        status = label("Waiting for the revision to become ready", 20, S.GREY)
        status.next_to(rc2, DOWN, buff=0.35).align_to(rc2, LEFT)
        yt2 = your_turn().next_to(ef.rows[1], RIGHT, buff=0.5)
        line8 = p7.code.code_lines[1]
        etag = entry_tag()
        click = Line(ORIGIN, RIGHT * 0.5, color=OWN, stroke_width=4)

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(q, exact, asy)), *set_tab(tabs2, 0), track(tr, 3), run_time=0.6)
            self.play(FadeIn(p7, shift=LEFT * 0.4), FadeIn(ef, shift=UP * 0.1), FadeIn(ef_ill), run_time=0.8)
            vo.wait_until("hello underscore HTTP")
            self.play(ef.fill(0, ENTRY, color=OWN), run_time=0.8)
            etag.move_to(ef.rows[0].value)
            self.play(FadeIn(etag, scale=0.9), run_time=0.3)
            dest = np.array([p7.get_right()[0] + 0.85 + etag.width / 2, line8.get_y(), 0])
            self.play(etag.animate.move_to(dest), run_time=0.9)
            click.put_start_and_end_on(line8.get_right() + RIGHT * 0.12, etag.get_left() + LEFT * 0.02)
            self.play(Create(click), each(list(def_name), OWN, scale=1.2, lag=0.06), run_time=0.6)
            self.add(p7)
            vo.wait_until("In the README's words")
            self.play(FadeIn(rc2, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("not the file name or service name")
            self.play(Indicate(rc2.body[2], color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Select Save and redeploy")
            self.play(track(tr, 4), ef.press(1), run_time=0.8)
            vo.wait_until("and wait for the revision")
            self.play(FadeIn(status, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Pause and do it")
            self.play(FadeIn(yt2, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt2, TURN)

        # ========================================================== 9. the slide's step, in full
        cl2 = check_list().move_to([-6.3, 2.3, 0], aligned_edge=UL)
        item3 = cl2.items[2]
        e3 = erratum_tag().next_to(item3, RIGHT, buff=0.4)
        trio = VGroup(ok_chip("main.py", mono_font=True), ok_chip("requirements.txt", mono_font=True),
                      ok_chip(f"entry point: {ENTRY}", mono_font=True)).arrange(RIGHT, buff=0.35)
        trio.next_to(cl2, DOWN, buff=0.7).align_to(cl2, LEFT).shift(RIGHT * 0.5)

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(p7, ef, ef_ill, rc2, status, yt2, etag, click, tabs2)), run_time=0.6)
            self.play(ReplacementTransform(mini, cl2), run_time=0.9)
            vo.wait_until("create a Python file")
            self.play(Indicate(item3, color=TURN, scale_factor=1.05), FadeIn(e3, shift=LEFT * 0.1), run_time=0.8)
            vo.wait_until("is the short version")
            self.play(item3.animate.set_color(S.GREY), run_time=0.4)
            vo.wait_until("The console wants the file")
            self.play(FadeIn(trio[0], target_position=item3[1], scale=0.6), run_time=0.6)
            vo.wait_until("its dependencies")
            self.play(FadeIn(trio[1], target_position=item3[1], scale=0.6), run_time=0.6)
            vo.wait_until("and the name of the function")
            self.play(FadeIn(trio[2], target_position=item3[1], scale=0.6), run_time=0.6)
            self.play(each(list(trio), OWN, scale=1.06, lag=0.2), run_time=0.8)

        self.play(FadeOut(VGroup(cl2, e3, trio, tr, ref4)), run_time=0.8)
        self.wait(0.3)
