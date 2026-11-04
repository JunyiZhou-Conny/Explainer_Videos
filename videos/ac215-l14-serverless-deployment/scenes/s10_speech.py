"""S10 · Attach the identity, turn on speech — tracker [3.2] (no step) → 1 … 7 (+ gcloud
alternative at step 3); lecture_ref 16 in the last block only.

Beats (script.md "## S10"; one voiceover block each):
0. TRACKER [3.2] appears with no step lit (a prerequisite). V6 returns: the BLUE service box with
   its right door, the BLUE badge `translation-demo-runtime` with its two ORANGE project roles, and
   Agent Platform. A GREY "you" figure sends a thin GREY arrow to the badge, labelled "Service
   Account User" · `iam.serviceAccounts.actAs` (README:432-434); GREY chip "your deployment right ≠
   the badge's roles".
1. [3.2] 1: V6 condenses into the right column (service box, right door, badge, Agent Platform,
   an instance "revision 1"). CONSOLE "Cloud Run → Services · translation-demo" (README:436),
   illustration. [3.2] 2: the Security tab; "Service account" → `translation-demo-runtime`; the badge
   pins onto the right door; its email (two rows) rings YELLOW against the S09 note card
   (README:437-439).
2. A README card (README.md · line 379) "We add your developer access separately in section 3.3."
   with the `erratum` tag; a GREY chip "section 3.3 grants Token Creator instead"; two GREEN chips
   "owner: already has it" and "restricted: ask course staff".
3. [3.2] 3: "Containers → Variables & Secrets · Environment variables": the three rows fill
   (README:444-448): ENABLE_SPEECH true · GOOGLE_CLOUD_PROJECT "Your project ID" ·
   GOOGLE_CLOUD_LOCATION us-central1; GREY chip "fill Name 1 / Value 1, then Add variable"
   (README:441-442). The solid pin "Toronto · service" sits on the service; S03's dashed
   us-central1 pin returns by Agent Platform and connects to the third row (README:495-498).
4. [3.2] 4: View diff & redeploy → "Review changes to be deployed" (the three variables GREEN),
   "Serve this revision immediately ✓ (leave on)" → Deploy changes (README:450-452). The instance
   "revision 1" dissolves, a fresh dashed instance "revision 2" takes its place, chip "replaced, not
   edited". [3.2] 5: the rollout's three stages tick (README:453-454).
5. The speech path (illustration, no code panels): GREY browser → PINK `POST /api/speech` → the
   instance; three gates light in order: "flag", "≤ 4,000 bytes", "language" (speech.py:75-82);
   the pinned badge hands back a short-lived ticket labelled "ADC"; a PINK arrow to the BLUE Agent
   Platform with `gemini-2.5-flash-tts` and a us-central1 pin (speech.py:91-92); a WAV file flows
   straight back to the browser; a GREY bucket crossed out: "no bucket".
6. [3.2] 6: the drawn public page (illustration) reloads; GREY card "the page checks the flag when it
   loads" with CODE(web.py: 13–15), `speech_enabled=enabled()` YELLOW; the button reads "Play audio";
   Translate, then Play audio. RECORDED(part3-speech-recorded: 12), `recorded · speech GIF`; GOLD
   cost tag "Gemini TTS · billed per Play audio · check the pricing page"; `▶ your turn`.
7. [3.2] 7: README card (README.md · lines 457–458) and the where-to-look card (slot 2 "the service
   logs" glows). TERM(laptop/24) returns in a small terminal, GREY chip "captured in S07: the flag
   missing" (line 2 + the [HTTP 503] line). CODE(speech.py: 108–119), lines 109 and 113 YELLOW; the
   mapping under it: "no identity / 401 / 403 / 404 → 503", "429 / others → 502" (web.py:50-53).
8. LECTURE 14 · 16. GREY chip "limited control and debugging", then GREEN chip "the message names
   the badge or setting". [3.2] 3 · gcloud alternative: terminal `laptop · gcloud` types
   README:489-492 (four rows), no output panel. Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.devops import code_panel
from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _door, _field_box

SAY = NARRATION["S10"]

FORM_UL = np.array([-6.45, 2.72, 0])                 # forms hang from here, under the tracker
FORM_W = 7.5                                         # left column: x -6.45 .. 1.05

# the condensed V6 in the right column (beats 1-4)
SVC_C = np.array([4.075, -0.1, 0])                   # service box x 1.6 .. 6.55, y -1.5 .. 1.3
SVC_W, SVC_H = 4.95, 2.8
M_DOOR = np.array([2.5, 1.3, 0])                     # the right door, on the box's top edge
M_BADGE = np.array([4.075, 0.2, 0])
M_INST = np.array([2.6, -0.85, 0])
M_CLOUD = np.array([5.35, 2.2, 0])

SA_EMAIL_ROWS = (RUNTIME_SA, "@" + WEB_EMAIL.split("@", 1)[1])


def form_at(f: VGroup) -> VGroup:
    return f.move_to(FORM_UL, aligned_edge=UL)


def ill_for(f: VGroup) -> VGroup:
    """The illustration tag on the form's top edge, right end."""
    tg = illustration_tag()
    return tg.move_to(f.frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))


def email_rows(color=INK) -> VGroup:
    g = VGroup(*[mono(s, 20, color) for s in SA_EMAIL_ROWS]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    return g


def env_table() -> VGroup:
    """The schematic 'Environment variables' editor (README:440-448): three Name / Value rows (empty
    fields that fill), Add variable and View diff & redeploy. .names .values .add_btn .diff_btn .frame"""
    pt = label("Containers → Variables & Secrets", 20, S.GREY)
    tt = label("Environment variables", 24, INK)
    head = VGroup(pt, tt).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    nw, vw = 3.9, 2.55
    hn, hv = label("Name", 20, S.GREY), label("Value", 20, S.GREY)
    names, values, rows = [], [], VGroup()
    for _ in range(3):
        n, v = _field_box(nw, 20), _field_box(vw, 20)
        r = VGroup(n, v).arrange(RIGHT, buff=0.2)
        names.append(n)
        values.append(v)
        rows.add(r)
    rows.arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    hn.next_to(rows[0][0], UP, buff=0.12).align_to(rows[0][0], LEFT)
    hv.next_to(rows[0][1], UP, buff=0.12).align_to(rows[0][1], LEFT)
    table = VGroup(hn, hv, rows)

    def btn(s):
        t = label(s, 20, INK)
        b = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.28, corner_radius=0.08,
                             stroke_color=CLOUD, stroke_width=2.5).set_fill(CLOUD, 0.15)
        t.move_to(b)
        g = VGroup(b, t)
        g.box, g.text = b, t
        return g
    add_b, diff_b = btn("Add variable"), btn("View diff & redeploy")
    btns = VGroup(add_b, diff_b).arrange(RIGHT, buff=0.3)
    body = VGroup(head, table, btns).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    frame = RoundedRectangle(width=FORM_W, height=body.height + 0.6, corner_radius=0.14,
                             stroke_color=S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.3)
    sep = Line(frame.get_left() + RIGHT * 0.15, frame.get_right() + LEFT * 0.15, color=S.GREY_DARK,
               stroke_width=1.5).move_to([frame.get_center()[0], head.get_bottom()[1] - 0.15, 0])
    g = VGroup(frame, sep, head, table, btns)
    g.frame, g.names, g.values, g.add_btn, g.diff_btn = frame, names, values, add_b, diff_b
    return g


def in_field(field, s: str, font=mono, color=INK) -> Text:
    return font(s, 20, color).move_to(field).align_to(field, LEFT).shift(RIGHT * 0.15)


def two_row_card(rows, color=S.GREY, size: float = 20) -> VGroup:
    t = VGroup(*[label(s, size, INK) for s in rows]).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    b = box(t.width + 0.5, t.height + 0.35, color, fill=S.GREY_DARKER, fill_opacity=1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def map_chip(s: str, code_: str) -> VGroup:
    """A mapping chip 'causes → code' with the status code RED."""
    t = VGroup(label(s + " →", 20, INK), mono(code_, 20, ERR)).arrange(RIGHT, buff=0.15)
    b = box(t.width + 0.45, t.height + 0.3, S.GREY, fill=S.BG, fill_opacity=1)
    t.move_to(b)
    return VGroup(b, t)


class EnableSpeech(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S10"] == 9, len(SAY)
        gc_rows = readme_rows(489, 492)
        assert len(gc_rows) == 4 and gc_rows[0].startswith('gcloud run services update "$WEB_SERVICE"')
        assert "iam.serviceAccounts.actAs" in readme(433) and "Service Account User" in readme(432)
        assert "We add your developer access separately in section 3.3." in readme(379)
        assert readme(446) == "| `ENABLE_SPEECH` | `true` |" and "Your project ID" in readme(447)
        assert "`us-central1`" in readme(448)
        c24 = capture("laptop/24")
        assert c24.line(2).startswith('{"error":"Speech is disabled.') and c24.line(4) == "[HTTP 503]"

        # ========================================================== 0. your permission: Service Account User
        tr = tracker_32(None)
        d = IdentityDoors()
        d.remove(d.browser, d.switch, d.ll)            # this scene is about the right door only
        d.left_door.set_opacity(0.3)
        ycol = you("you").move_to([-5.6, -2.35, 0])
        sau = VGroup(label("Service Account User", 20, INK), mono("iam.serviceAccounts.actAs", 20, S.GREY))
        sau.arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([-4.95, -2.95, 0], aligned_edge=LEFT)
        right_chip = grey_chip("your deployment right ≠ the badge's roles").move_to([3.6, -3.1, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(d), run_time=0.7)
            d.add_badge(self, run_time=0.5)
            roles = d.roles(self, "Agent Platform User", "Service Usage Consumer", run_time=0.6)
            vo.wait_until("Attaching the account")
            self.play(Indicate(d.badge_, color=CLOUD, scale_factor=1.06), run_time=0.6)
            d.heal(self)
            vo.wait_until("takes a permission of yours")
            self.play(FadeIn(ycol, shift=UP * 0.15), run_time=0.5)
            a_you = arrow(ycol.figure.get_right() + RIGHT * 0.05, d.badge_.get_left(), S.GREY, stroke=2.5)
            self.play(GrowArrow(a_you), run_time=0.7)
            vo.wait_until("Service Account User on that account")
            self.play(FadeIn(sau[0], shift=RIGHT * 0.1), run_time=0.5)
            self.play(FadeIn(sau[1], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("That is your deployment right")
            self.play(Indicate(VGroup(a_you, sau), color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("separate from the account's own roles")
            self.play(FadeIn(right_chip, shift=UP * 0.1), run_time=0.5)
            self.play(*[Indicate(c, color=SHARED, scale_factor=1.06) for c in roles], run_time=0.7)
            d.heal(self)

        # ========================================================== 1. steps 1-2: the service, the Security tab
        m_box = RoundedRectangle(width=SVC_W, height=SVC_H, corner_radius=0.14, stroke_color=CLOUD,
                                 stroke_width=3).set_fill(CLOUD, 0.08).move_to(SVC_C)
        m_name = mono(SERVICE, 20, INK).move_to(m_box.get_corner(UR) + np.array([-0.2, -0.3, 0]),
                                                 aligned_edge=RIGHT)
        m_svc = VGroup(m_box, m_name)
        m_door = _door(S.GREY).move_to(M_DOOR)
        m_badge = badge(RUNTIME_SA).move_to(M_BADGE)
        m_cloud = cloud_shape("Agent Platform", CLOUD, 2.3).move_to(M_CLOUD)
        inst1 = instance(1.1, 0.65).move_to(M_INST)
        rev1 = label("revision 1", 20, INK).next_to(inst1, RIGHT, buff=0.2)
        hook = Line(m_door.frame.get_bottom(), [M_DOOR[0], m_badge.get_top()[1], 0], color=CLOUD, stroke_width=3)

        f1 = form_at(console_form(SERVICE, [("button", "Security")], form_w=FORM_W, path="Cloud Run → Services"))
        ill1 = ill_for(f1)
        f2 = form_at(console_form("Security", [("Service account", "")], form_w=FORM_W,
                                  path="Cloud Run → Services → translation-demo"))
        ill2 = ill_for(f2)
        em = email_rows()
        em_block = VGroup(label("its email", 20, S.GREY), em).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        em_block.next_to(f2, DOWN, buff=0.35).align_to(f2, LEFT).shift(RIGHT * 0.3)
        note9 = card([email_rows()], S.GREY, head="your note: the runtime account's email")
        note9.next_to(em_block, DOWN, buff=0.35).align_to(f2, LEFT)
        same = check_glyph(0.34, OWN).next_to(note9, RIGHT, buff=0.3).shift(UP * 0.6)
        assert note9.get_right()[0] < SVC_C[0] - SVC_W / 2 - 0.1 and note9.get_bottom()[1] > -3.5
        with self.voiceover(SAY[1]) as vo:
            parts = list(d.submobjects)
            self.remove(d)
            self.add(*parts)
            keep = {d.service, d.right_door, d.badge_, d.cloud}
            self.play(*[FadeOut(m) for m in parts if m not in keep], FadeOut(VGroup(ycol, a_you, sau, right_chip)),
                      ReplacementTransform(d.service, m_svc), ReplacementTransform(d.right_door, m_door),
                      ReplacementTransform(d.badge_, m_badge), ReplacementTransform(d.cloud, m_cloud),
                      FadeIn(inst1, scale=0.8), FadeIn(rev1), track(tr, 1), FadeIn(f1, shift=UP * 0.1),
                      FadeIn(ill1), run_time=0.9)
            vo.wait_until("open translation-demo")
            self.play(Indicate(f1.title_text, color=TURN, scale_factor=1.06),
                      Indicate(m_name, color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("Step 2: on the Security tab")
            self.play(track(tr, 2), f1.press(0), run_time=0.5)
            self.play(FadeOut(f1), FadeOut(ill1), run_time=0.25)
            self.play(FadeIn(f2, shift=UP * 0.1), FadeIn(ill2), run_time=0.3)
            vo.wait_until("choose your runtime account")
            self.play(f2.fill(0, RUNTIME_SA), run_time=0.6)
            self.play(Create(hook), m_door.frame.animate.set_stroke(CLOUD),
                      Indicate(m_badge, color=CLOUD, scale_factor=1.05), run_time=0.6)
            vo.wait_until("and check its email")
            self.play(FadeIn(em_block, shift=UP * 0.1), FadeIn(note9, shift=UP * 0.1), run_time=0.5)
            r1, r2 = ring(em, TURN), ring(note9.body, TURN)
            self.play(Create(r1), Create(r2), run_time=0.5)
            self.play(Create(same), run_time=0.4)
            self.wait(1.2)

        # ========================================================== 2. the README's small gap (line 379)
        gap_body = VGroup(label("We add your developer access", 22, INK), label("separately in section 3.3.", 22, INK))
        gap_body.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        gap = readme_card(379, gap_body).next_to(f2, DOWN, buff=0.35).align_to(f2, LEFT)
        etag = erratum_tag()
        etag.move_to(gap.frame.get_corner(UR) + np.array([-etag.width / 2 - 0.2, 0, 0]))
        tc = grey_chip("section 3.3 grants Token Creator instead").next_to(gap, DOWN, buff=0.3).align_to(gap, LEFT)
        own = ok_chip("owner: already has it").next_to(tc, DOWN, buff=0.3).align_to(gap, LEFT)
        rst = ok_chip("restricted: ask course staff").next_to(own, DOWN, buff=0.2).align_to(gap, LEFT)
        sec33 = gap_body[1]
        assert rst.get_bottom()[1] > -3.55 and max(m.get_right()[0] for m in (gap, tc, rst)) < 1.5
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(em_block, note9, r1, r2, same)), run_time=0.4)
            vo.wait_until("A small gap")
            self.play(FadeIn(gap, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(etag, scale=0.8), run_time=0.4)
            vo.wait_until("the README promises this access")
            self.play(Indicate(sec33, color=TURN, scale_factor=1.05), run_time=0.7)
            vo.wait_until("but that section grants Token Creator")
            self.play(FadeIn(tc, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Project owners already have it")
            self.play(FadeIn(own, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("in a restricted project")
            self.play(FadeIn(rst, shift=RIGHT * 0.1), run_time=0.5)
            self.play(Indicate(rst, color=OWN, scale_factor=1.05), run_time=0.6)

        # ========================================================== 3. step 3: three environment variables
        et = form_at(env_table())
        ill3 = ill_for(et)
        hint = grey_chip("fill Name 1 / Value 1, then Add variable").next_to(et, DOWN, buff=0.3).align_to(et, LEFT)
        names = [in_field(et.names[i], s) for i, s in
                 enumerate(("ENABLE_SPEECH", "GOOGLE_CLOUD_PROJECT", "GOOGLE_CLOUD_LOCATION"))]
        vals = [in_field(et.values[0], "true"), in_field(et.values[1], "Your project ID", label),
                in_field(et.values[2], SPEECH_LOCATION)]
        for t_ in names + vals:
            assert t_.get_right()[0] < et.frame.get_right()[0] - 0.15, t_.get_right()
        pin_t = region_pin("Toronto · service").move_to([1.8, -2.05, 0], aligned_edge=LEFT)
        pin_u = region_pin(SPEECH_LOCATION, dashed=True)
        pin_u.move_to([m_cloud.get_left()[0] - 0.35, M_CLOUD[1] + 0.05, 0], aligned_edge=RIGHT)
        assert pin_u.get_left()[0] > et.frame.get_right()[0] + 0.1, pin_u.get_left()
        link = DashedLine(pin_u.pin.get_left() + LEFT * 0.05, et.values[2].get_right() + RIGHT * 0.05,
                          color=CLOUD, stroke_width=2.5, dash_length=0.1)

        def type_in(t_):
            return ShowIncreasingSubsets(t_, rate_func=linear)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(gap, etag, tc, own, rst)), FadeOut(VGroup(f2, ill2)), track(tr, 3),
                      run_time=0.5)
            self.play(FadeIn(et, shift=UP * 0.1), FadeIn(ill3), FadeIn(pin_t, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("three environment variables")
            self.play(FadeIn(hint, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("ENABLE SPEECH, true")
            self.play(type_in(names[0]), run_time=0.6)
            self.play(type_in(vals[0]), run_time=0.3)
            self.play(et.add_btn.animate.set_stroke(TURN), run_time=0.2)
            self.play(et.add_btn.animate.set_stroke(CLOUD), run_time=0.2)
            vo.wait_until("GOOGLE CLOUD PROJECT, your project ID")
            self.play(type_in(names[1]), run_time=0.7)
            self.play(type_in(vals[1]), run_time=0.5)
            self.play(et.add_btn.animate.set_stroke(TURN), run_time=0.2)
            self.play(et.add_btn.animate.set_stroke(CLOUD), run_time=0.2)
            vo.wait_until("and GOOGLE CLOUD LOCATION")
            self.play(type_in(names[2]), run_time=0.7)
            self.play(type_in(vals[2]), run_time=0.5)
            vo.wait_until("The service runs in Toronto")
            self.play(Indicate(pin_t, color=CLOUD, scale_factor=1.08), run_time=0.7)
            vo.wait_until("the model in us-central1")
            self.play(FadeIn(pin_u, shift=DOWN * 0.15), run_time=0.5)
            self.play(Create(link), Indicate(vals[2], color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("two different settings")
            self.play(Indicate(pin_t.text, color=TURN, scale_factor=1.06),
                      Indicate(pin_u.text, color=TURN, scale_factor=1.06), run_time=0.8)

        # ========================================================== 4. steps 4-5: View diff & redeploy; the rollout
        rv = form_at(console_form("Review changes to be deployed",
                                  [("ENABLE_SPEECH", "true"), ("GOOGLE_CLOUD_PROJECT", "Your project ID"),
                                   ("GOOGLE_CLOUD_LOCATION", SPEECH_LOCATION),
                                   ("check", "Serve this revision immediately", True), ("button", "Deploy changes")],
                                  form_w=FORM_W))
        for i in range(3):
            rv.rows[i].label.set_color(OWN)
            rv.rows[i].value.set_color(OWN)
        ill4 = ill_for(rv)
        leave = label("(leave on)", 20, S.GREY).next_to(rv.rows[3], RIGHT, buff=0.25)
        assert leave.get_right()[0] < rv.frame.get_right()[0] - 0.1
        inst2 = instance(1.1, 0.65).move_to(M_INST)
        rev2 = label("revision 2", 20, INK).next_to(inst2, RIGHT, buff=0.2)
        replaced = grey_chip("replaced, not edited").move_to([4.075, -2.05, 0])
        stages = VGroup(*[label(s, 20, INK) for s in ("updating the service", "creating the revision",
                                                      "routing traffic")]).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        ticks = VGroup(*[check_glyph(0.26, OWN).next_to(s, LEFT, buff=0.2) for s in stages])
        roll = VGroup(stages, ticks)
        roll_card = card([roll], S.GREY, head="README.md · lines 453–454 · wait for")
        roll_card.move_to(FORM_UL, aligned_edge=UL)
        with self.voiceover(SAY[4]) as vo:
            vo.wait_until("View diff and redeploy")
            self.play(track(tr, 4), Indicate(et.diff_btn, color=TURN, scale_factor=1.08), run_time=0.6)
            self.play(FadeOut(VGroup(et, ill3, *names, *vals, hint, link, pin_u, pin_t)),
                      FadeIn(rv, shift=UP * 0.1), FadeIn(ill4), run_time=0.7)
            self.play(*[Indicate(rv.rows[i].label, color=OWN, scale_factor=1.05) for i in range(3)], run_time=0.6)
            vo.wait_until("keep Serve this revision immediately on")
            self.play(FadeIn(leave, shift=LEFT * 0.1), Indicate(rv.rows[3].tick, color=OWN, scale_factor=1.4),
                      run_time=0.6)
            vo.wait_until("then Deploy changes")
            self.play(rv.press(4), run_time=0.6)
            vo.wait_until("That makes a new revision")
            self.play(FadeOut(inst1, scale=0.6), FadeOut(rev1), run_time=0.6)
            self.play(FadeIn(inst2, scale=0.8), FadeIn(rev2), run_time=0.6)
            vo.wait_until("the old instance is replaced")
            self.play(FadeIn(replaced, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Step 5: wait for the rollout")
            self.play(track(tr, 5), FadeOut(VGroup(rv, ill4, leave)), run_time=0.35)
            self.play(FadeIn(roll_card, shift=UP * 0.1), run_time=0.4)
            for tk in ticks:
                self.play(Create(tk), run_time=0.35)

        # ========================================================== 5. the speech path (illustration)
        y0 = 0.9
        br = browser_icon(1.0)
        br.shift(np.array([-6.0, y0 + 0.4, 0]) - br.window.get_center())
        ibox = instance(5.0, 2.0, inner=False).move_to([-0.15, y0, 0])
        cont = RoundedRectangle(width=4.6, height=1.6, corner_radius=0.1, stroke_color=IMAGE,
                                stroke_width=2.5).set_fill(IMAGE, 0.08).move_to(ibox)
        gx = (-1.75, -0.15, 1.47)
        gates = VGroup(*[Line([x, y0 + 0.15, 0], [x, y0 + 0.7, 0], color=S.GREY, stroke_width=6) for x in gx])
        gl = VGroup(*[label(s, 20, INK).move_to([x, y0 - 0.3, 0])
                      for s, x in zip(("flag", "≤ 4,000 bytes", "language"), gx)])
        post_a = route(br.window.get_right(), np.array([ibox.get_left()[0], y0 + 0.4, 0]))
        post_t = mono("POST /api/speech", 20, ROUTE).next_to(post_a, DOWN, buff=0.15)
        assert post_t.get_left()[0] > br.window.get_right()[0] and post_t.get_right()[0] < ibox.get_left()[0] - 0.05
        sp_badge = badge(RUNTIME_SA).move_to([-0.15, -1.05, 0])
        sp_hook = Line(ibox.get_bottom(), sp_badge.get_top(), color=CLOUD, stroke_width=3)
        cl = cloud_shape("Agent Platform", CLOUD, 2.4).move_to([4.85, y0, 0])
        model = mono(TTS_MODEL, 20, INK).next_to(cl, DOWN, buff=0.12)
        loc = region_pin(SPEECH_LOCATION, dashed=True).next_to(model, DOWN, buff=0.15)
        out_a = route(np.array([ibox.get_right()[0], y0 + 0.4, 0]), np.array([cl.get_left()[0] + 0.05, y0 + 0.4, 0]))
        tk = ticket(CLOUD, 0.55).move_to(sp_badge.get_right() + RIGHT * 0.5)
        adc = label("ADC", 20, CLOUD)
        adc_long = label("Application Default Credentials", 20, S.GREY).next_to(sp_badge, DOWN, buff=0.2)
        wav = file_icon("WAV", INK, 0.4)
        wav_path = ArcBetweenPoints(cl.get_top() + DOWN * 0.1, br.window.get_top() + UP * 0.35, angle=PI / 6)
        nb = bucket(None, 0.8, S.GREY).move_to([4.0, -2.55, 0])
        nb_x = cross_glyph(0.7).move_to(nb)
        nb_t = label("no bucket", 20, S.GREY).next_to(nb, RIGHT, buff=0.3)
        ill5 = illustration_tag().move_to([-5.4, -3.2, 0])
        req = pulse_dot(r=0.11).move_to(br.window.get_right())
        assert gl[2].get_right()[0] < cont.get_right()[0] - 0.05 and gl[1].get_right()[0] < gl[2].get_left()[0] - 0.12
        assert model.get_right()[0] < 6.55 and tk.get_right()[0] < cl.get_left()[0]
        assert wav_path.get_top()[1] < PIC_TOP + 0.05 and nb_t.get_right()[0] < 6.55
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(roll_card, replaced, m_svc, m_door, m_badge, hook,
                                     inst2, rev2, m_cloud)), run_time=0.5)
            vo.wait_until("Here is the speech path")
            self.play(FadeIn(br), FadeIn(ibox), FadeIn(cont), FadeIn(cl), FadeIn(ill5), run_time=0.6)
            self.play(GrowArrow(post_a), FadeIn(post_t), FadeIn(req), run_time=0.6)
            self.play(req.animate.move_to([gx[0] - 0.45, y0 + 0.4, 0]), FadeIn(gates), FadeIn(gl), run_time=0.6)
            for k, phrase in enumerate(("The app checks the flag", "the size", "and the language")):
                vo.wait_until(phrase)
                self.play(req.animate.move_to([gx[k] + 0.45, y0 + 0.4, 0]),
                          gates[k].animate.set_color(OWN), gl[k].animate.set_color(OWN), run_time=0.5)
            vo.wait_until("then asks Google's auth library for a token")
            self.play(FadeIn(sp_badge, shift=UP * 0.1), Create(sp_hook), run_time=0.5)
            self.play(Indicate(sp_badge, color=CLOUD, scale_factor=1.05), run_time=0.5)
            vo.wait_until("on Cloud Run, the badge supplies it")
            self.play(FadeIn(tk, scale=0.5), run_time=0.3)
            self.play(tk.animate.move_to([ibox.get_right()[0] + 0.75, y0 - 0.1, 0]), run_time=0.8)
            adc.next_to(tk, DOWN, buff=0.12)
            vo.wait_until("That lookup is Application Default Credentials")
            self.play(FadeIn(adc, shift=UP * 0.1), FadeIn(adc_long, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(adc, color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("Gemini speech in us-central1")
            self.play(GrowArrow(out_a), FadeOut(req), FadeIn(model), FadeIn(loc, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("sends audio straight back")
            wav.move_to(wav_path.get_start())
            self.play(FadeIn(wav, scale=0.6), run_time=0.3)
            self.play(MoveAlongPath(wav, wav_path), run_time=1.2)
            vo.wait_until("no bucket")
            self.play(FadeIn(nb), FadeIn(nb_t), run_time=0.4)
            self.play(Create(nb_x), run_time=0.4)
            self.wait(0.8)

        # ========================================================== 6. step 6: reload, Translate, Play audio
        page = TranslatePage(SERVICE_URL).move_to([-2.25, 0.75, 0])
        page_ill = illustration_tag().next_to(page.frame, RIGHT, buff=0.3).shift(UP * 0.2)
        flag_card = two_row_card(["the page checks the flag", "when it loads"]).move_to([4.15, 2.05, 0])
        web_src = excerpt("tutorial/app/translation_demo/web.py", 13, 15).split("\n")
        web_src = [s[4:] for s in web_src]
        assert web_src[2].startswith('    return render_template(') and web_src[2].endswith(
            "speech_enabled=enabled())")
        web_src[2] = "    return render_template(…, speech_enabled=enabled())"
        wp = code_panel("\n".join(web_src), "tutorial/app/translation_demo/web.py", 13, "python", font_size=20)
        wp.move_to([0, -2.45, 0])
        code_span(wp.code, 2, "…").set_color(S.GREY)
        rec = recorded_card("part3-speech-recorded", [12], "speech GIF").move_to([-1.5, -2.0, 0])
        ct = cost_tag("Gemini TTS · billed per Play audio · check the pricing page").move_to([-1.5, -3.15, 0])
        yt = your_turn().next_to(page.frame, RIGHT, buff=0.3).align_to(page.frame, DOWN)
        assert flag_card.get_left()[0] > page.frame.get_right()[0] + 0.1 and wp.get_bottom()[1] > -3.55
        assert page.frame.get_bottom()[1] > wp.get_top()[1] + 0.05 and yt.get_right()[0] < 6.55
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(br, post_a, post_t, ibox, cont, gates, gl, sp_badge, sp_hook, tk, adc,
                                     adc_long, cl, model, loc, out_a, wav, nb, nb_x, nb_t, ill5)), run_time=0.5)
            vo.wait_until("Step 6: reload the page")
            self.play(track(tr, 6), FadeIn(page), FadeIn(page_ill), run_time=0.6)
            self.play(Indicate(page.audio_btn, color=S.GREY, scale_factor=1.06), run_time=0.5)
            page.heal(self)
            vo.wait_until("because it checks the flag when it loads")
            self.play(FadeIn(flag_card, shift=LEFT * 0.1), FadeIn(wp, shift=UP * 0.1), run_time=0.6)
            span = code_span(wp.code, 2, "speech_enabled=enabled()")
            self.play(*[g.animate.set_color(TURN) for g in span], run_time=0.5)
            self.add(wp)
            page.enable_speech(self, run_time=0.6)
            vo.wait_until("Then Translate and Play audio")
            self.play(FadeOut(wp), run_time=0.3)
            page.type_in(self, run_time=0.6)
            page.set_dest(self, "fr", run_time=0.3)
            page.translate(self, run_time=0.6)
            self.play(page.press("audio"), run_time=0.6)
            page.heal(self)
            vo.wait_until("the recording shows French audio playing")
            self.play(FadeIn(rec, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("A gold tag")
            self.play(FadeIn(ct, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("each Play audio is a paid model call")
            self.play(Indicate(ct, color=COST, scale_factor=1.06), page.press("audio", COST), run_time=0.7)
            page.heal(self)
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)

        # ========================================================== 7. step 7: the message, the logs, the codes
        rc7 = readme_card((457, 458), "If the request fails, read the message shown\nin the UI and inspect "
                                      "the service's Logs\nbefore changing permissions.")
        rc7.move_to(FORM_UL + DOWN * 0.15, aligned_edge=UL)
        wl = WhereToLook(card_w=5.4).move_to([3.55, 1.1, 0])
        w0 = label("the build and start-up logs", 20, INK).move_to(wl.slots[0]).align_to(wl.slots[0], LEFT).shift(RIGHT * 0.2)
        w1 = label("the service logs", 20, INK).move_to(wl.slots[1]).align_to(wl.slots[1], LEFT).shift(RIGHT * 0.2)
        wl.slots[0].frame.set_stroke(TURN)
        wl.slots[1].frame.set_stroke(TURN)
        wl.add(w0, w1)
        assert rc7.get_right()[0] < wl.get_left()[0] - 0.1, (rc7.get_right(), wl.get_left())
        lt = term(P_REPO, 8, T_LAPTOP, size=20)
        flag_chip = grey_chip("captured in S07: the flag missing")
        flag_chip.move_to([6.4 - flag_chip.width / 2, lt.box.get_top()[1] + 0.4, 0])
        assert flag_chip.get_bottom()[1] > lt.box.get_top()[1] and flag_chip.get_left()[0] > rc7.get_right()[0] + 0.2
        assert rc7.get_bottom()[1] > lt.box.get_top()[1] + 0.1
        cuts = {109: "unavailable", 111: "failed", 113: "access denied.", 115: "not found.", 117: "quota",
                119: "rejected"}
        sp = code("tutorial/app/translation_demo/speech.py", 108, 119, font_size=20, dedent=True, cuts=cuts)
        sp.move_to([0, 2.7 - sp.height / 2, 0])
        m1 = map_chip("no identity / 401 / 403 / 404", "503")
        m2 = map_chip("429 / others", "502")
        mp = VGroup(m1, m2).arrange(RIGHT, buff=0.35)
        msrc = label("web.py · lines 50–53", 20, S.GREY)
        mrow = VGroup(mp, msrc).arrange(RIGHT, buff=0.35).next_to(sp, DOWN, buff=0.25)
        assert mrow.width < 12.9 and mrow.get_bottom()[1] > -3.0, (mrow.width, mrow.get_bottom())
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(page, page_ill, flag_card, rec, ct, yt)), run_time=0.5)
            vo.wait_until("Step 7: if it fails")
            self.play(track(tr, 7), FadeIn(rc7, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("check the message and the logs")
            self.play(FadeIn(wl, shift=LEFT * 0.15), run_time=0.5)
            self.play(wl.glow(1), run_time=0.8)
            vo.wait_until("before changing permissions")
            self.play(Indicate(rc7.body[2], color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("Without the flag")
            self.play(FadeOut(wl), FadeIn(lt, shift=UP * 0.15), run_time=0.5)
            type_capture(self, lt, c24, type_time=0.9)
            self.play(FadeIn(flag_chip, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("you get our captured 503")
            rows = out(self, lt, [(c24.line(2), ERR), (c24.line(4), ERR)], wrap=True, run_time=0.6)
            vo.wait_until("speech is disabled")
            self.play(Indicate(rows[0], color=ERR, scale_factor=1.03), run_time=0.7)
            self.add(lt)
            vo.wait_until("A missing identity or a denied call")
            self.play(FadeOut(VGroup(rc7, lt, flag_chip)), run_time=0.4)
            self.play(FadeIn(sp, shift=UP * 0.1), run_time=0.5)
            b109, b113 = line_bar(sp.code, 1, TURN, 0.22), line_bar(sp.code, 5, TURN, 0.22)
            self.play(FadeIn(b109), FadeIn(b113), run_time=0.5)
            self.play(FadeIn(m1, shift=UP * 0.1), FadeIn(m2, shift=UP * 0.1), FadeIn(msrc), run_time=0.6)

        # ========================================================== 8. lecture 16; the gcloud alternative
        ref = lref("16")
        lim = grey_chip("limited control and debugging")
        okc = ok_chip("the message names the badge or setting")
        VGroup(lim, okc).arrange(RIGHT, buff=0.4).move_to([0, -3.2, 0])
        assert VGroup(lim, okc).width < 12.9
        gt = term(P_REPO, 7, T_GCLOUD, size=20)
        npc = no_panel_chip()
        npc.move_to([6.5 - npc.width / 2, gt.box.get_top()[1] + 0.45, 0])
        assert npc.get_top()[1] < TRACK_BOTTOM - 0.1
        with self.voiceover(SAY[8]) as vo:
            vo.wait_until("That is limited control and debugging")
            self.play(FadeIn(ref, shift=LEFT * 0.1), FadeIn(lim, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("made workable")
            self.play(FadeIn(okc, shift=UP * 0.1), Indicate(b109, color=OWN), Indicate(b113, color=OWN),
                      run_time=0.6)
            vo.wait_until("The gcloud alternative")
            self.play(FadeOut(VGroup(sp, b109, b113, m1, m2, msrc, lim, okc, ref)), track(tr, 3, "gcloud"),
                      run_time=0.5)
            self.play(FadeIn(gt, shift=UP * 0.15), run_time=0.4)
            type_lines(self, gt, gc_rows, type_time=0.45)
            self.play(FadeIn(npc, shift=DOWN * 0.1), run_time=0.4)
            self.wait(1.2)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
