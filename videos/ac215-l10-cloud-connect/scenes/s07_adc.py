"""S07 · ADC: from key file to bearer token (AC215 L10) — concept scene, no tracker;
`Lecture 10 · slides 19–31, 42` top right for the whole scene.

Beats (script.md, ## S07; one voiceover block each):
0. CODE(api-service/api/routers/rag.py: 14–27, 20 pt) in two windows: 14–23 (lines 19, 21, 22 cut
   after `projects/`; `GCP_PROJECT` of line 15 flashes on "built from a project"), then 24–27 (the
   comment rules 24/25/27 cut; line 26 is 81 characters, so it is wrapped once inside its
   parentheses, whitespace only, GREY note 'line 26 · wrapped to fit') with line 26 YELLOW and its
   project / location arguments flashing. GREY chip 'no key path anywhere'. Slide 42's chain
   redrawn under the panel: mounted key → env var → client → ?? → IAM check; on "or ADC" the YELLOW
   '??' becomes a PINK 'ADC'.
1. The 'ADC' box rises to a heading ('looks in three places, in order'); V1's AdcPlaces rows arrive
   one per sentence while the PINK glass walks them; on "only when the one before is not set" a
   GREY note and the glass walks 1 → 2 → 3 again; on "Inside these containers" a TEAL container
   outline closes around them and rows 2 and 3 empty.
2. Row 1 lights; the glass slides into V1's AuthChain (teaser: key slot lit, the rest hollow), slot
   ADC lights. The key card (`illustration`) slides out of the key slot; a JWT envelope is written;
   the `private_key` row flashes and a GREEN pen grows from it, seals the envelope ('signed'); the
   envelope flies into slot 'signed JWT'. The key card's `token_uri` glows BLUE and its address
   flies up to become the desk's `oauth2.googleapis.com/token`; the desk lights. The key card folds
   into a GREEN file card (pen beside it) on the laptop side. A copy of the envelope reaches the
   desk; the BLUE public key with chip 'Google keeps this half' checks it: GREEN tick. The ticket
   slot lights ('≈ 60 min'); three `HTTPS · Authorization: Bearer …` requests take a ticket each;
   the file card and pen are circled GREEN ('never leaves your laptop').
3. The timer runs out, a fresh ticket mints (AuthChain.mint). A GREY bridge card (slides 19–23):
   a person → consent screen → the same BLUE desk (right under the chain's desk, a dashed BLUE
   link) → ticket; person and consent screen grey out and are crossed; caption 'same desk · no
   person, no consent screen'.
4. AdcPlaces again (rows 2, 3 empty) above a 3-row strip at P_LLMRAG with the `extra` tag on its
   bar: `sh docker-shell.sh` → TERM(29: 6–7); `ls -la /secrets` at the capture's prompt → (29:
   13–15) and a GREEN '/secrets/ · empty' beside row 1; the one-liner (soft-wrapped: every space
   but one is inside its quotes) → TERM(29: 17, …, 25–26, …, 30; wrap), the
   `_get_explicit_environ_credentials` frame ringed PINK (= place 1), line 30 RED; the glass flashes
   RED at row 1 and the rows grey out, the glass never walks on; GREY chip 'variable set → no
   fallback'. `exit` (29: 31–32), the laptop prompt returns.
5. Misconception card: a GREY 'your Mac's terminal' card with `export GOOGLE_APPLICATION_
   CREDENTIALS=~/secrets/llm-service-account.json` struck RED, caption 'on your Mac: authenticates
   nothing in a container'; under it the correct pair: host `secrets/` → GREEN tube
   (`../../secrets:/secrets`, docker-compose.yml line 11) → `/secrets/` in a TEAL container, and
   CODE(llm-rag/docker-shell.sh: 8) whose path points PINK at the file. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CAPTION, CLOUD, ERR, IMAGE, INK, KEY, NARRATION, P_LLMRAG, PASS, ROUTE,
                    SAY_COUNT, TURN, AdcPlaces, AuthChain, Ticket, arrow, bare_prompt, capture, card, check_mark,
                    code, code_panel, code_span, cross_mark, cut, desk_glyph, each, envelope, excerpt,
                    extra_row, file_card,
                    file_glyph, folder_glyph, greyed, grey_chip, illustration_tag, key_card, key_glyph, label,
                    line_bar, lref, mono, note, on_bar, out, outline_box, person_icon, ring, shown_path,
                    split_prompt, strike, substring, term, type_cmd, under)
from explainer import style as S

SAY = NARRATION["S07"]
RAG = "cheese-app-v0/api-service/api/routers/rag.py"
SHELL = "cheese-app-v0/llm-rag/docker-shell.sh"
CAP = capture("29")


# ------------------------------------------------------------------ local helpers
def place_top_left(p, x: float = -6.45, y: float = 3.05):
    """Put a code panel's top-left corner (its header) at (x, y)."""
    return p.shift(np.array([x - p.get_left()[0], y - p.get_top()[1], 0]))


def rag_window_b():
    """rag.py lines 24–27 at 20 pt. The comment rules (24, 25, 27) are cut with the house '…'; line 26
    (81 characters, wider than the frame at 20 pt) is wrapped once inside its parentheses, at a
    space: whitespace only, the rows join back to the line exactly."""
    l24, l25, l26, l27 = excerpt(RAG, 24, 27).split("\n")
    a, b = l26.split(" project=", 1)
    w1, w2 = a, "    project=" + b
    assert w1 + " " + w2.strip() == l26
    rows = [cut(l24, "#" * 44), cut(l25, "Initialize the LLM Client"), w1, w2, cut(l27, "#" * 44)]
    p = code_panel("\n".join(rows), shown_path(RAG), 24, "python", font_size=20)
    hd = p.header
    old = hd[1]
    new = label("· lines 24–27", CAPTION, S.GREY).move_to(old, aligned_edge=LEFT)
    hd.submobjects[1] = new
    for k in (0, 1, 4):
        code_span(p.code, k, "…").set_color(S.GREY)
    return p


def slide42_chain() -> VGroup:
    """Slide 42's chain, redrawn with this app's words: mounted key → env var → client → ?? → IAM
    check. .boxes (each .frame .text) .arrows"""
    names = (("mounted key", KEY, True), ("env var", S.GREY, True), ("client", S.GREY, True),
             ("??", TURN, False), ("IAM check", CLOUD, True))
    boxes = VGroup()
    for s, col, solid in names:
        fr = outline_box(2.2, 0.8, col, solid=solid, fill_opacity=0.06)
        t = label(s, 24, TURN if s == "??" else INK).move_to(fr)
        b = VGroup(fr, t)
        b.frame, b.text = fr, t
        boxes.add(b)
    boxes.arrange(RIGHT, buff=0.45)
    arrows = VGroup(*[arrow(boxes[i].get_right() + RIGHT * 0.06, boxes[i + 1].get_left() + LEFT * 0.06)
                      for i in range(4)])
    g = VGroup(arrows, boxes)
    g.boxes, g.arrows = boxes, arrows
    return g


def signing_pen(pen_l: float = 0.75, color=KEY) -> VGroup:
    """The private key as a pen (GREEN): a barrel and a nib, nib pointing down-right."""
    body = RoundedRectangle(width=pen_l, height=0.16, corner_radius=0.06, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.3)
    nib = Polygon([pen_l / 2, 0.08, 0], [pen_l / 2 + 0.22, 0, 0], [pen_l / 2, -0.08, 0],
                  stroke_color=color, stroke_width=2.5).set_fill(color, 0.7)
    g = VGroup(body, nib).rotate(-PI / 4)
    g.nib = nib
    return g


def sub_glyphs(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` in a one-line mono()/label() Text (its submobjects skip spaces)."""
    s = t.original_text
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t[a:a + n])


def oauth_card(desk_x: float, ticket_x: float) -> VGroup:
    """The lecture's OAuth flow (slides 19–23) reduced to three boxes and the ticket, GREY card:
    a person → consent screen → the token desk (BLUE, at desk_x) → ticket (at ticket_x).
    .frame .head .person .consent .desk .ticket .arrows .caption"""
    frame = outline_box(12.8, 2.75, S.GREY, solid=True, fill_opacity=0.08)
    frame.fill.set_fill(S.GREY_DARKER, 1)
    head = label("the lecture's OAuth flow · slides 19–23, reduced", CAPTION, S.GREY)
    head.move_to(frame.get_corner(UL) + np.array([0.3, -0.3, 0]), aligned_edge=LEFT)
    y = frame.get_center()[1] + 0.05
    pb = outline_box(2.2, 1.05, S.GREY, solid=True, fill_opacity=0.06)
    pi = person_icon(S.GREY, 0.5)
    pt = label("a person", 20, INK)
    VGroup(pi, pt).arrange(DOWN, buff=0.08).move_to(pb)
    person = VGroup(pb, pi, pt)
    cb = outline_box(2.4, 1.05, S.GREY, solid=True, fill_opacity=0.06)
    ct = VGroup(label("consent", 22, INK), label("screen", 22, INK)).arrange(DOWN, buff=0.06).move_to(cb)
    consent = VGroup(cb, ct)
    db = outline_box(2.1, 1.05, CLOUD, solid=True, fill_opacity=0.06)
    dg = desk_glyph(1.2).move_to(db.get_center() + UP * 0.12)
    desk = VGroup(db, dg)
    tk = Ticket(1.5, timer=False)
    person.move_to([desk_x - 7.4, y, 0])
    consent.move_to([desk_x - 4.3, y, 0])
    desk.move_to([desk_x, y, 0])
    tk.move_to([ticket_x, y, 0])
    arrows = VGroup(arrow(person.get_right() + RIGHT * 0.08, consent.get_left() + LEFT * 0.08),
                    arrow(consent.get_right() + RIGHT * 0.08, desk.get_left() + LEFT * 0.08),
                    arrow(desk.get_right() + RIGHT * 0.08, tk.get_left() + LEFT * 0.08))
    cap = label("same desk · no person, no consent screen", 22, INK)
    cap.move_to(frame.get_bottom() + UP * 0.35).align_to(head, LEFT)
    g = VGroup(frame, head, arrows, person, consent, desk, tk)
    g.frame, g.head, g.person, g.consent, g.desk, g.ticket, g.arrows, g.caption = \
        frame, head, person, consent, desk, tk, arrows, cap
    return g


def soft_type(scene, t, cmd: str, type_time: float | None = None):
    """Type a command whose spaces are (all but one) inside its quotes: it soft-wraps at the
    terminal's edge, as a terminal shows a long typed line (rows join back to prompt + command)."""
    full = t.prompt + " " + cmd
    n = t.max_chars
    rows = [full[i:i + n] for i in range(0, len(full), n)]
    assert "".join(rows) == full and all(len(r) <= n for r in rows)
    assert len(rows) <= t.rows, (len(rows), t.rows)
    t.fold = lambda text, first_prefix=0: list(rows)
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


def at_prompt(scene, t, n: int, type_time: float | None = None):
    """Type capture line n (a container prompt line) at that capture's own prompt."""
    prompt, typed = CAP.istep(n)
    t.set_prompt(prompt)
    return type_cmd(scene, t, typed, type_time)


class AdcToToken(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 6, len(SAY)
        ref = lref("19–31, 42")

        # ========================================================== 0. no key path anywhere
        win_a = place_top_left(code(RAG, 14, 23, font_size=20,
                                    cuts={19: '"projects/', 21: "projects/", 22: '"projects/'}))
        win_b = place_top_left(rag_window_b())
        wrapped = note("line 26 · wrapped to fit").next_to(win_b, DOWN, buff=0.15).align_to(win_b, LEFT)
        bars = VGroup(line_bar(win_b.code, 2, TURN), line_bar(win_b.code, 3, TURN))
        nokey = grey_chip("no key path anywhere").next_to(win_b.code, RIGHT, buff=0.35)
        chain42 = slide42_chain().move_to([0, -2.45, 0])
        cap42 = note("slide 42's chain, with this app").next_to(chain42, UP, buff=0.25).align_to(chain42, LEFT)
        qbox = chain42.boxes[3]
        adc_t = label("ADC", 26, ROUTE).move_to(qbox.frame)
        adc_fr = outline_box(2.2, 0.8, ROUTE, solid=True, fill_opacity=0.08).move_to(qbox.frame)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(win_a, shift=UP * 0.2), run_time=0.9)
            vo.wait_until("The API's Google client")
            self.play(Indicate(win_a.code.code_lines[1], color=INK, scale_factor=1.04), run_time=0.7)
            vo.wait_until("built from a project")
            proj = code_span(win_a.code, 1, 'os.environ["GCP_PROJECT"]')
            u = under(proj, TURN)
            self.play(Create(u), Indicate(proj, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("and a location")
            self.play(FadeOut(VGroup(win_a, u), shift=UP * 0.3), FadeIn(win_b, shift=UP * 0.3), run_time=0.7)
            self.remove(win_a, u)
            self.play(FadeIn(bars), FadeIn(wrapped), run_time=0.4)
            self.play(each([code_span(win_b.code, 3, "project=GCP_PROJECT"),
                            code_span(win_b.code, 3, 'location="global"')], TURN, scale=1.08, lag=0.5),
                      run_time=1.0)
            vo.wait_until("No code in this repo")
            self.play(FadeIn(nokey, shift=LEFT * 0.2), run_time=0.5)
            self.play(Indicate(nokey.text, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("a library does")
            self.play(FadeIn(cap42), LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in chain42.boxes],
                                                 lag_ratio=0.2), Create(chain42.arrows), run_time=1.2)
            vo.wait_until("by a convention called")
            self.play(Circumscribe(qbox, color=TURN, buff=0.08), run_time=0.8)
            vo.wait_until("or ADC")
            self.play(FadeOut(qbox.text), FadeIn(adc_t), Transform(qbox.frame, adc_fr), run_time=0.6)

        # ========================================================== 1. ADC's three places
        head_box = outline_box(1.5, 0.7, ROUTE, solid=True, fill_opacity=0.08).move_to([-5.7, 2.95, 0])
        head_adc = label("ADC", 26, ROUTE).move_to(head_box)
        head_t = label("looks in three places, in order", 26, INK).next_to(head_box, RIGHT, buff=0.3)
        ap = AdcPlaces().move_to([0.55, -0.45, 0])
        rule = note("the next place only when the one before is not set", INK, size=22)
        rule.move_to([0.55, -2.75, 0])
        encl, encl_anim = ap.enclose()

        with self.voiceover(SAY[1]) as vo:
            rest = VGroup(win_b, bars, wrapped, nokey, cap42, chain42.arrows,
                          *[chain42.boxes[i] for i in (0, 1, 2, 4)])
            self.play(FadeOut(rest), run_time=0.6)
            self.remove(rest)
            self.play(Transform(qbox.frame, head_box), Transform(adc_t, head_adc), run_time=0.8)
            self.play(FadeIn(head_t, shift=LEFT * 0.2), FadeIn(ap.glass, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("First, the file named")
            self.play(FadeIn(ap.rows[0], shift=LEFT * 0.2), run_time=0.6)
            self.play(Indicate(ap.rows[0].title, color=KEY, scale_factor=1.05), run_time=0.8)
            vo.wait_until("Second, a login file")
            self.play(FadeIn(ap.rows[1], shift=LEFT * 0.2), ap.visit(1), run_time=0.7)
            vo.wait_until("Third, the metadata server")
            self.play(FadeIn(ap.rows[2], shift=LEFT * 0.2), ap.visit(2), run_time=0.7)
            self.play(Indicate(ap.chip.text, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("ADC moves to the next place")
            self.play(ap.visit(0), FadeIn(rule, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("only when the one before")
            self.play(ap.visit(1, run_time=0.6))
            self.play(ap.visit(2, run_time=0.6))
            vo.wait_until("Inside these containers")
            self.play(ap.visit(0), FadeOut(rule), run_time=0.6)
            self.remove(rule)
            self.play(encl_anim, run_time=0.9)
            vo.wait_until("only the first place exists")
            self.play(ap.empty((1, 2)), run_time=0.8)

        # ========================================================== 2. key file to bearer token
        ch = AuthChain(teaser=True)
        ch.shift(np.array([0, 1.77 - ch.slots[0].frame.get_center()[1], 0]))
        kc = key_card().move_to([-1.85, -1.55, 0])
        ill = illustration_tag().next_to(kc.frame, RIGHT, buff=0.15).align_to(kc.frame, UP)
        env = envelope_at([4.75, -1.15, 0])
        signed = label("signed", 22, KEY).next_to(env, DOWN, buff=0.15)
        pen_at = np.array([kc.frame.get_right()[0] - 0.75, kc.private_key.get_center()[1], 0])
        pen = signing_pen().move_to(pen_at)
        uri_row = kc.rows["token_uri"]
        uri = sub_glyphs(uri_row, "oauth2.googleapis.com/token")
        fc = file_card("llm-service-account.json", KEY).move_to([-4.05, -2.95, 0])
        pen_home = np.array([fc.get_right()[0] - 0.3, fc.get_top()[1] + 0.45, 0])
        pub = key_glyph(1.0, CLOUD).move_to([4.5, -0.3, 0])
        half = grey_chip("Google keeps this half", color=CLOUD).next_to(pub, DOWN, buff=0.25)
        tick = check_mark(0.45, PASS)
        st = ch.staple(3).move_to([2.85, -1.95, 0])
        stays = note("never leaves your laptop", KEY, size=22).next_to(fc, UP, buff=0.25).align_to(fc, LEFT)

        with self.voiceover(SAY[2]) as vo:
            self.play(Indicate(ap.rows[0].title, color=KEY, scale_factor=1.06),
                      ap.rows[0].frame.frame.animate.set_stroke(KEY, 5), run_time=0.7)
            gone = VGroup(ap.rows, encl, qbox.frame, adc_t, head_t)
            self.play(FadeOut(gone), FadeIn(ch), ap.glass.animate.move_to(ch.slots[1].frame.get_center()
                                                                          + UP * 0.05), run_time=0.9)
            self.remove(gone)
            self.play(ch.reveal(1), FadeOut(ap.glass), run_time=0.6)
            self.remove(ap.glass)
            self.play(FadeIn(kc, target_position=ch.slots[0].frame), FadeIn(ill), run_time=0.8)
            vo.wait_until("a JSON web token")
            self.play(FadeIn(env, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("and signs it")
            self.play(Indicate(kc.private_key, color=KEY, scale_factor=1.06), run_time=0.6)
            self.play(GrowFromPoint(pen, kc.private_key.get_right()), run_time=0.5)
            self.play(pen.animate.move_to(env.seal.get_center() + np.array([-0.3, 0.32, 0])), run_time=0.7)
            env.add(env.seal)             # a child first: played alone it would stay on the scene
            self.play(GrowFromCenter(env.seal), FadeIn(signed, shift=UP * 0.1), run_time=0.5)
            self.play(pen.animate.move_to(pen_at), FadeOut(signed),
                      env.animate.move_to(ch.slots[2].frame.get_center() + UP * 0.05), run_time=0.9)
            self.remove(signed)
            self.play(ch.reveal(2), FadeOut(env), run_time=0.6)
            self.remove(env)
            vo.wait_until("It sends that note")
            self.play(Indicate(uri_row, color=CLOUD, scale_factor=1.04), run_time=0.6)
            self.play(TransformFromCopy(uri, ch.url), ch.reveal(3), run_time=1.0)
            vo.wait_until("at the address in your key file")
            self.play(Circumscribe(uri_row, color=CLOUD, buff=0.06), run_time=0.8)
            # the key card folds into its file on the laptop side; the pen stays beside it
            box_c = RoundedRectangle(width=fc.box.width, height=fc.box.height, corner_radius=0.14,
                                     stroke_color=KEY, stroke_width=3).move_to(fc.box)
            self.play(FadeOut(kc[1]), FadeOut(ill), run_time=0.4)
            self.play(ReplacementTransform(kc.frame, box_c), pen.animate.move_to(pen_home), run_time=0.7)
            self.play(FadeIn(fc), FadeOut(box_c), run_time=0.3)
            self.remove(kc, box_c)
            vo.wait_until("Google holds the matching")
            msg = envelope("JWT", sealed=True).move_to(ch.slots[2].frame.get_center() + UP * 0.05)
            self.add(msg)
            self.play(msg.animate.move_to([2.6, -0.3, 0]), FadeIn(pub, shift=LEFT * 0.2), run_time=0.8)
            self.play(FadeIn(half, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("so it checks your signature")
            tick.next_to(msg, RIGHT, buff=0.12).shift(UP * 0.2)
            self.play(Circumscribe(pub, color=CLOUD, buff=0.08), run_time=0.7)
            self.play(Create(tick), Indicate(msg.seal, color=PASS, scale_factor=1.6), run_time=0.6)
            vo.wait_until("Back comes an access token")
            self.play(FadeOut(VGroup(msg, tick, pub, half)), ch.reveal(4), run_time=0.8)
            self.remove(msg, tick, pub, half)
            vo.wait_until("valid for about an hour")
            self.play(Indicate(ch.ticket.minutes, color=CLOUD, scale_factor=1.2), run_time=0.8)
            vo.wait_until("That token rides")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(VGroup(r.pill, r.text), shift=RIGHT * 0.2),
                                                   FadeIn(r.ticket, target_position=ch.ticket))
                                    for r in st], lag_ratio=0.3), run_time=1.4)
            self.play(each([r.text for r in st], ROUTE, scale=1.04, lag=0.2), run_time=0.9)
            vo.wait_until("Your private key never leaves")
            self.play(Circumscribe(VGroup(fc, pen), color=KEY, buff=0.1), FadeIn(stays, shift=UP * 0.1),
                      run_time=0.9)
            vo.wait_until("only the short-lived ticket")
            self.play(each([r.ticket.text for r in st], CLOUD, scale=1.2, lag=0.2), run_time=0.9)

        # ========================================================== 3. a fresh ticket; the same desk
        desk_x, ticket_x = ch.slots[3].frame.get_center()[0], ch.slots[4].frame.get_center()[0]
        oc = oauth_card(desk_x, ticket_x).move_to([0, -1.75, 0])
        oc.caption.move_to(oc.frame.get_bottom() + UP * 0.35).align_to(oc.head, LEFT)   # not in the group
        link = DashedLine(ch.slots[3].text.get_bottom() + DOWN * 0.08, oc.desk.get_top() + UP * 0.08,
                          color=CLOUD, stroke_width=3, dash_length=0.1)
        crosses = VGroup(cross_mark(0.7, S.GREY).move_to(oc.person), cross_mark(0.7, S.GREY).move_to(oc.consent))

        with self.voiceover(SAY[3]) as vo:
            low = VGroup(fc, pen, stays, st)
            self.play(FadeOut(low), run_time=0.5)
            self.remove(low)
            ch.mint(self, run_time=1.4)
            vo.wait_until("The lecture's OAuth diagram")
            self.play(FadeIn(oc, shift=UP * 0.2), run_time=0.8)
            vo.wait_until("ends at this same desk")
            self.play(Create(link), run_time=0.5)
            self.play(Circumscribe(ch.slots[3].frame, color=CLOUD, buff=0.06),
                      Circumscribe(oc.desk, color=CLOUD, buff=0.06), run_time=0.9)
            vo.wait_until("minus the consent screen")
            self.play(Transform(oc.person, greyed(oc.person)), Transform(oc.consent, greyed(oc.consent)),
                      Create(crosses), run_time=0.8)
            vo.wait_until("no person is there")
            self.play(FadeIn(oc.caption, shift=UP * 0.1), run_time=0.6)

        # ========================================================== 4. ADC caught in the act
        t = term(P_LLMRAG, rows=3)
        xt = on_bar(t, extra_row())
        ap4 = AdcPlaces(row_h=0.85, gap=0.15)
        ap4.move_to([-0.13, 0.45, 0])
        for i in (1, 2):
            VGroup(ap4.rows[i].title, ap4.rows[i].sub).set_opacity(0.12)
        r0 = ap4.rows[0].frame
        sec = VGroup(folder_glyph(0.3, KEY), mono("/secrets/", 20, KEY), label("· empty", 20, S.GREY))
        sec.arrange(RIGHT, buff=0.12).next_to(r0, RIGHT, buff=0.25)
        nofall = grey_chip("variable set → no fallback").move_to([0, 2.5, 0]).align_to(r0, LEFT)
        rows_l = [CAP.line(n) for n in (17, 25, 26, 30)]

        with self.voiceover(SAY[4]) as vo:
            old = VGroup(ch, ch.url, oc, oc.caption, link, crosses)
            self.play(FadeOut(old), run_time=0.6)
            self.remove(old, *ch.slots)
            self.play(FadeIn(VGroup(ap4.rows, ap4.glass)), FadeIn(t), run_time=0.7)
            self.play(FadeIn(xt, shift=LEFT * 0.1), run_time=0.3)
            type_cmd(self, t, CAP.cmd, type_time=0.6)
            out(self, t, CAP.at((6, 7)), run_time=0.5)
            vo.wait_until("With slash secrets empty")
            at_prompt(self, t, 12, type_time=0.5)
            out(self, t, CAP.at((13, 15)), run_time=0.5)
            self.play(FadeIn(sec, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("an extra one-line Python check")
            prompt, typed = CAP.istep(16)
            assert prompt == split_prompt(CAP.line(12))[0]
            soft_type(self, t, typed, type_time=1.6)
            vo.wait_until("The variable is set")
            out(self, t, [rows_l[0], ("…", S.GREY)], run_time=0.4)
            fr = out(self, t, [rows_l[1]], wrap=True, run_time=0.4)
            frame_row = fr[-1]
            assert frame_row.text.endswith("in _get_explicit_environ_credentials"), frame_row.text
            rg = ring(substring(frame_row, "_get_explicit_environ_credentials"), ROUTE)
            self.play(Create(rg), Indicate(ap4.rows[0].title, color=ROUTE, scale_factor=1.05), run_time=0.7)
            vo.wait_until("finds no file")
            ap4.stop(self, 0)
            self.play(Indicate(sec[1], color=ERR, scale_factor=1.15), run_time=0.6)
            vo.wait_until("and stops right there")
            self.play(FadeOut(rg), run_time=0.2)
            self.remove(rg)
            out(self, t, [rows_l[2], ("…", S.GREY)], run_time=0.4)
            out(self, t, [(rows_l[3], ERR)], wrap=True, run_time=0.5)
            vo.wait_until("A wrong path never falls back")
            self.play(Transform(ap4.rows, greyed(ap4.rows)), Indicate(ap4.glass, color=ERR, scale_factor=1.15),
                      run_time=0.8)
            self.play(FadeIn(nofall, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("With your key in place")
            at_prompt(self, t, 31, type_time=0.3)
            out(self, t, CAP.at(32), run_time=0.3)
            t.set_prompt(P_LLMRAG)
            bare_prompt(self, t)

        # ========================================================== 5. the mix-up
        cmd = "export GOOGLE_APPLICATION_CREDENTIALS=~/secrets/llm-service-account.json"
        mline = mono(cmd, 20, INK)
        mc = card([mline], color=S.GREY, head="your Mac's terminal").move_to([0, 2.35, 0])
        sk = strike(mline, ERR, stroke=5)
        mcap = label("on your Mac: authenticates nothing in a container", 24, INK).next_to(mc, DOWN, buff=0.25)
        cbox = outline_box(5.9, 2.2, IMAGE, solid=True, fill_opacity=0.05).move_to([3.45, -0.75, 0])
        ctitle = label("container", 20, IMAGE).move_to(cbox.get_corner(UL) + np.array([0.2, -0.25, 0]),
                                                      aligned_edge=LEFT)
        cdir = VGroup(folder_glyph(0.3, KEY), mono("/secrets/", 20, KEY)).arrange(RIGHT, buff=0.12)
        cdir.move_to(cbox.get_corner(UL) + np.array([0.35, -0.75, 0]), aligned_edge=LEFT)
        cfile = VGroup(file_glyph(0.34, KEY), mono("llm-service-account.json", 20, INK)).arrange(RIGHT, buff=0.14)
        cfile.next_to(cdir, DOWN, buff=0.3, aligned_edge=LEFT).shift(RIGHT * 0.4)
        host_t = label("your laptop", 20, S.GREY).move_to([-5.0, -0.1, 0])
        hdir = VGroup(folder_glyph(0.3, KEY), mono("secrets/", 20, KEY)).arrange(RIGHT, buff=0.12)
        hdir.move_to([-5.0, cdir.get_center()[1], 0])
        host_t.next_to(hdir, UP, buff=0.25).align_to(hdir, LEFT)
        y_t = cdir.get_center()[1]
        tube = Line([hdir.get_right()[0] + 0.15, y_t, 0], [cdir.get_left()[0] - 0.15, y_t, 0], color=KEY,
                    stroke_width=6)
        ends = VGroup(Dot(tube.get_start(), radius=0.07, color=KEY), Dot(tube.get_end(), radius=0.07, color=KEY))
        mount = mono("../../secrets:/secrets", 20, KEY).next_to(tube, UP, buff=0.15)
        msrc = note("docker-compose.yml · line 11").next_to(tube, DOWN, buff=0.15)
        p8 = code(SHELL, 8, font_size=20).move_to([0, -2.95, 0])
        path_g = code_span(p8.code, 0, "/secrets/llm-service-account.json")
        ptr = Arrow(path_g.get_top() + UP * 0.05, cfile[1].get_bottom() + DOWN * 0.05, buff=0, color=ROUTE,
                    stroke_width=4, tip_length=0.2, max_tip_length_to_length_ratio=0.25)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(ap4.rows, ap4.glass, sec, nofall, t, xt)), run_time=0.6)
            self.remove(ap4, ap4.glass, sec, nofall, t, xt)
            self.play(FadeIn(mc, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("authenticates nothing")
            self.play(Create(sk), run_time=0.5)
            self.play(FadeIn(mcap, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("where the path must exist")
            self.play(FadeIn(VGroup(cbox, ctitle, cdir, cfile)), run_time=0.7)
            vo.wait_until("That is why the scripts set a container path")
            self.play(FadeIn(p8, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(path_g, color=ROUTE, scale_factor=1.06), run_time=0.6)
            self.play(GrowArrow(ptr), run_time=0.6)
            vo.wait_until("and mount the host folder")
            self.play(FadeIn(VGroup(host_t, hdir), shift=RIGHT * 0.2), run_time=0.5)
            self.play(Create(tube), FadeIn(ends), FadeIn(mount), FadeIn(msrc), run_time=0.8)
            dot = Dot(tube.get_start(), radius=0.1, color=KEY)
            self.play(MoveAlongPath(dot, tube), run_time=0.8)
            self.play(FadeOut(dot), Indicate(cdir[1], color=KEY, scale_factor=1.12), run_time=0.5)
            self.remove(dot)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)


def envelope_at(p) -> VGroup:
    """An unsealed JWT envelope at p, its GREEN seal built (not added) where the flap meets."""
    e = envelope("JWT", sealed=False)
    e.seal.move_to(e.flap.get_bottom())
    e.move_to(p)
    e.seal.move_to(e.flap.get_bottom())
    return e
