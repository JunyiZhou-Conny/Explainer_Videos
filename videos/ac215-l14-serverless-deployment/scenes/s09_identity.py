"""S09 · Who may call it, and who it runs as — tracker [3.1] 1 → 5 (+ gcloud alternative); no
lecture_ref (identity is tutorial-only: SLIDES "What the slides leave to the tutorial").

Beats (script.md "## S09"; one voiceover block each):
0. No tracker. A GREY README card (README.md · lines 361–362): "Two permissions questions are
   separate: who may call our public app, and what the running app may access." Each question
   lights as it is spoken; S08's YELLOW parked question returns and docks under the card.
1. V6 IdentityDoors: BLUE service box `translation-demo` with two doors. Left door "who may call it":
   the GREY browser's PINK request passes because the switch "Allow public access" is on; GREY chip
   `--no-invoker-iam-check` (docs/lifecycle.md · lines 78–79). The switch flips off: the request
   bounces RED 403; GREY chip "an organization policy can forbid public access"; the switch flips
   back on. The right door ("who it is when it calls out") stays empty and dim.
2. A PINK dashed arrow tries to leave through the right door toward the BLUE Agent Platform cloud
   (a YELLOW "?" on it). PONDER (6 s).
3. The card leaves. The left door's switch dims GREY (irrelevant); the outbound call stops at the
   empty right door, RED. A dashed ORANGE badge "default compute account" hangs on the right door,
   GREY chip "normally, until you attach one".
4. TRACKER [3.1] 1 (appears). V6 condenses to its right half (right door, "who it runs as", the
   default badge, Agent Platform) on the right. CONSOLE (README:366-367, 382-384, illustration):
   APIs & Services → Library → Agent Platform API → Enable; chip "service ID
   aiplatform.googleapis.com"; GREY dashed chip "earlier lectures: Vertex AI".
5. [3.1] 2: CONSOLE IAM & Admin → Service Accounts → Create service account (README:368). [3.1] 3:
   name `Translation demo runtime`; the worksheet card `translation-demo-runtime` flies into the ID
   field; the email line `translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com`
   (README:369-371). On V6 the default badge gives way to the BLUE badge `translation-demo-runtime`.
6. [3.1] 4: "Permissions (optional)": Agent Platform User, then Add another role → Service Usage
   Consumer (README:374-379); two ORANGE role cards hang from the badge ("may call the model", "may
   bill the quota project"). CODE(tutorial/app/translation_demo/speech.py: 102–105), line 104
   `quota_project_id=project` YELLOW. Then "Principals with access (optional)": both fields left
   empty; Done.
7. [3.1] 5. The email copies to a GREY note. README card (README.md · line 380) "You do not need to
   create or download a key."; on V6 a dashed GOLD key is crossed out; a GREY-dashed callback card
   "L3 · secrets/…json key" slides in and is retired beside it. RECORDED(expected/
   part3-speech-recorded.txt: 2), tag "recorded · identity GIF". `▶ your turn`.
8. [3.1] 4 · gcloud alternative. Terminal `laptop · gcloud` (20 pt, 13 rows) types README:412-419
   verbatim, all eight rows, about 0.9 s per command; no output panel (GREY chip "needs your project
   · no output shown"); the two `projects add-iam-policy-binding` lines ring ORANGE with the chip
   "project-wide". Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _door

SAY = NARRATION["S09"]

FORM_UL = np.array([-6.45, 2.72, 0])                 # forms hang from here, under the tracker
FORM_W = 7.8                                         # left column: x -6.45 .. 1.35
PONDER_Q = "The service allows public access.\nDoes that let it call Agent Platform?"
PARKED_Q = "To speak, the app must call an API that asks who is calling.\nWho is it?"   # S08's card

# the condensed V6 on the right (beats 4-7): door, its label, the badge spot, Agent Platform
M_DOOR = np.array([2.75, 1.7, 0])
M_BADGE = np.array([4.25, 0.85, 0])
M_CLOUD = np.array([5.35, 2.55, 0])


def form_at(f: VGroup) -> VGroup:
    return f.move_to(FORM_UL, aligned_edge=UL)


def ill_for(f: VGroup) -> VGroup:
    """The illustration tag on the form's top edge, right end (the right column is V6's)."""
    tg = illustration_tag()
    return tg.move_to(f.frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))


def role_card(name: str, what: str) -> VGroup:
    """An ORANGE (project-wide) role card in two rows: the role, and what it lets the badge do."""
    t = VGroup(label(name, 20, INK), label(what, 20, S.GREY)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    b = box(t.width + 0.5, t.height + 0.3, SHARED, fill_opacity=0.16)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def recorded_rows(file: str, n: int, rows, source: str, size: float = 22) -> VGroup:
    """recorded_card() with its line broken where we choose (it wraps at 60 characters): the rows
    must join back to the recorded line exactly. .frame .body .tag"""
    line = recorded(file, n)[0]
    assert " ".join(rows) == line, (rows, line)
    body = VGroup(*[label(s, size, INK) for s in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    frame = box(body.width + 0.7, body.height + 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    body.move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.35 + DOWN * 0.05)
    tg = recorded_tag(source)
    tg.move_to(frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g = VGroup(frame, body, tg)
    g.frame, g.body, g.tag = frame, body, tg
    return g


class RuntimeIdentity(VoiceScene):
    def flash(self, *mobs, color=TURN, run_time: float = 0.8, extra=()):
        """A YELLOW ring that draws round each of `mobs` and fades (Indicate would fill a door or a
        field box solid)."""
        rs = [ring(m, color, buff=0.1, stroke=4) for m in mobs]
        self.play(*[Create(r) for r in rs], *extra, run_time=run_time * 0.55)
        self.play(*[FadeOut(r) for r in rs], run_time=run_time * 0.45)
        self.remove(*rs)

    def construct(self):
        assert len(SAY) == SAY_COUNT["S09"] == 9, len(SAY)
        gc_rows = readme_rows(412, 419)
        assert len(gc_rows) == 8 and gc_rows[0].startswith("gcloud services enable aiplatform")
        assert gc_rows[-1].endswith("--condition=None")
        assert readme(371).endswith(f"`{WEB_EMAIL}`.") and RUNTIME_SA == "translation-demo-runtime"

        # ========================================================== 0. two questions (README:361-362)
        q1 = label("who may call our public app,", 24, INK)
        q2 = label("and what the running app may access.", 24, INK)
        body = VGroup(label("Two permissions questions are separate:", 24, INK), q1, q2)
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rc = readme_card((361, 362), body).move_to([0, 1.55, 0])
        parked = question_card(PARKED_Q, size=24).move_to([0, -2.55, 0])
        u1, u2 = under(q1, ROUTE), under(q2, CLOUD)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(parked, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("The README separates")
            self.play(FadeIn(rc, shift=DOWN * 0.15), run_time=0.6)
            self.play(parked.animate.next_to(rc, DOWN, buff=0.45), run_time=0.8)
            vo.wait_until("who may call our public app")
            self.play(Create(u1), Indicate(q1, color=ROUTE, scale_factor=1.05), run_time=0.8)
            vo.wait_until("and what the running app")
            self.play(Create(u2), Indicate(q2, color=CLOUD, scale_factor=1.05), run_time=0.8)
            self.play(Indicate(parked.body[1], color=TURN, scale_factor=1.12), run_time=0.8)

        # ========================================================== 1. the first door: Allow public access
        d = IdentityDoors()
        noinv = grey_chip("--no-invoker-iam-check", mono_font=True).move_to([-3.0, -2.0, 0])
        src = label("docs/lifecycle.md · lines 78–79", 20, S.GREY).next_to(noinv, DOWN, buff=0.12)
        org = grey_chip("an organization policy can forbid public access").move_to([-3.0, -3.15, 0])
        dim = VGroup(d.right_door, d.rl)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(rc, parked, u1, u2)), run_time=0.5)
            self.play(FadeIn(d), run_time=0.7)
            self.play(dim.animate.set_opacity(0.3), run_time=0.4)
            d.heal(self)
            vo.wait_until("The first door")
            self.flash(d.left_door, extra=[Indicate(d.ll, color=TURN)])
            d.heal(self)
            vo.wait_until("is Allow public access")
            self.play(Indicate(d.switch, color=OWN, scale_factor=1.1), run_time=0.6)
            d.heal(self)
            d.call(self, True, run_time=0.9)
            vo.wait_until("gcloud spells it")
            self.play(FadeIn(noinv, shift=UP * 0.1), FadeIn(src), run_time=0.5)
            vo.wait_until("If an organization policy")
            self.play(FadeIn(org, shift=UP * 0.1), run_time=0.4)
            d.set_public(self, False)
            vo.wait_until("the URL answers 403")
            ch403 = d.call(self, False, run_time=0.9)
            self.play(Indicate(ch403, color=ERR, scale_factor=1.15), run_time=0.5)
            d.heal(self)
        d.drop(self, ch403, run_time=0.3)
        d.set_public(self, True, run_time=0.4)

        # ========================================================== 2. calling out (PONDER)
        start = d.right_door.frame.get_center() + LEFT * 1.0
        q_arrow = DashedLine(start, d.cloud.get_left() + RIGHT * 0.15, color=ROUTE, stroke_width=4,
                             dash_length=0.12).add_tip(tip_length=0.2)
        qm = label("?", 30, TURN).next_to(q_arrow, UP, buff=0.12).shift(RIGHT * 0.6)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(noinv, src, org)), run_time=0.4)
            self.play(dim.animate.set_opacity(1), run_time=0.4)
            d.heal(self)
            vo.wait_until("The service allows public access")
            self.play(Indicate(d.switch, color=OWN, scale_factor=1.1), run_time=0.7)
            d.heal(self)
            vo.wait_until("Does that let it call")
            d.show(self, q_arrow, anims=[Create(q_arrow)], run_time=0.8)
            d.show(self, qm, run_time=0.3)
            d.out_arrow = VGroup(q_arrow, qm)
        pc = ponder(self, PONDER_Q, seconds=6, center=(0, -2.12))   # below the doors' labels

        # ========================================================== 3. no: the other door, the default account
        normally = grey_chip("normally, until you attach one")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            vo.wait_until("That door only admits callers")
            self.flash(d.left_door, run_time=0.6)
            self.play(d.switch.animate.set_opacity(0.35), d.ll.animate.set_color(S.GREY), run_time=0.5)
            d.heal(self)
            vo.wait_until("Calling out goes through")
            d.call_out(self, ok=False, run_time=0.9)
            self.flash(d.right_door, extra=[Indicate(d.rl, color=TURN)], run_time=0.7)
            d.heal(self)
            vo.wait_until("until you attach one")
            d.default_badge(self, run_time=0.6)
            normally.next_to(d.default_, DOWN, buff=0.2)
            self.play(FadeIn(normally, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("default compute account")
            self.play(Indicate(d.default_[0], color=SHARED, scale_factor=1.06), run_time=0.7)
            d.heal(self)

        # ========================================================== 4. step 1: enable the Agent Platform API
        tr = tracker_31(1)
        m_door = _door(S.GREY).move_to(M_DOOR)
        m_lab = label("who it runs as", 20, INK).next_to(m_door, RIGHT, buff=0.2)
        m_badge0 = badge("default compute account", SHARED, dashed=True, mono_font=False).move_to(M_BADGE)
        m_hook0 = DashedLine(m_door.frame.get_bottom(), m_badge0.get_top(), color=SHARED, stroke_width=2)
        m_def = VGroup(m_badge0, m_hook0)
        m_cloud = cloud_shape("Agent Platform", CLOUD, 2.3).move_to(M_CLOUD)
        f4 = form_at(console_form("Agent Platform API", [("button", "Enable")], form_w=FORM_W,
                                  path="APIs & Services → Library"))
        ill4 = ill_for(f4)
        sid = VGroup(label("service ID", 20, S.GREY), mono("aiplatform.googleapis.com", 20, INK))
        sid.arrange(RIGHT, buff=0.2)
        sid_chip = VGroup(box(sid.width + 0.5, sid.height + 0.3, S.GREY), sid)
        sid.move_to(sid_chip[0])
        sid_chip.next_to(f4, DOWN, buff=0.35).align_to(f4, LEFT)
        vtx = dashed_chip("earlier lectures: Vertex AI").next_to(sid_chip, DOWN, buff=0.25).align_to(f4, LEFT)
        enabled = check_glyph(0.3, OWN).next_to(f4.rows[0], RIGHT, buff=0.3)
        with self.voiceover(SAY[4]) as vo:
            parts = [m for m in d.submobjects]
            self.remove(d)
            self.add(*parts)
            keep = {d.right_door, d.rl, d.default_, d.cloud}
            self.play(*[FadeOut(m) for m in parts if m not in keep], FadeOut(normally),
                      ReplacementTransform(d.right_door, m_door), ReplacementTransform(d.rl, m_lab),
                      ReplacementTransform(d.default_, m_def), ReplacementTransform(d.cloud, m_cloud),
                      FadeIn(tr, shift=DOWN * 0.15), run_time=0.9)
            self.play(FadeIn(f4, shift=UP * 0.1), FadeIn(ill4), run_time=0.5)
            vo.wait_until("in the API Library")
            self.play(Indicate(f4.path_text, color=TURN, scale_factor=1.05), run_time=0.7)
            vo.wait_until("enable the Agent Platform API")
            self.play(f4.press(0), run_time=0.7)
            self.add(ill4)
            self.play(Create(enabled), Indicate(m_cloud, color=CLOUD, scale_factor=1.05),
                      FadeIn(sid_chip, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("the console's current name")
            self.play(Indicate(f4.title_text, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("earlier lectures called")
            self.play(FadeIn(vtx, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 5. steps 2 and 3: create the account
        f5 = form_at(console_form("Create service account",
                                  [("Service account name", ""), ("Service account ID", ""),
                                   ("button", "Create and continue")],
                                  form_w=FORM_W, path="IAM & Admin → Service Accounts"))
        ill5 = ill_for(f5)
        ws = worksheet_card(RUNTIME_SA, "web account").move_to([-2.7, -1.6, 0])
        em_lab = label("its email", 20, S.GREY)
        em = mono(WEB_EMAIL, 20, INK)
        email = VGroup(em_lab, em).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([0, -2.95, 0])
        m_badge = badge(RUNTIME_SA).move_to(M_BADGE)
        with self.voiceover(SAY[5]) as vo:
            self.add(ill4)
            self.play(track(tr, 2), ReplacementTransform(f4, f5), ReplacementTransform(ill4, ill5),
                      FadeOut(VGroup(sid_chip, vtx, enabled)), run_time=0.8)
            vo.wait_until("create a service account")
            self.play(track(tr, 3), f5.fill(0, "Translation demo runtime"), run_time=0.9)
            self.add(ill5)
            vo.wait_until("with the ID")
            self.play(FadeIn(ws, shift=UP * 0.2), run_time=0.4)
            self.play(ws.animate.move_to(f5.rows[1].field).set_opacity(0), f5.fill(1, RUNTIME_SA),
                      run_time=0.9)
            self.remove(ws)
            self.play(FadeIn(email, shift=UP * 0.1), run_time=0.5)
            self.play(FadeOut(m_def), FadeIn(m_badge, scale=0.8), run_time=0.7)
            self.play(Indicate(m_badge, color=CLOUD, scale_factor=1.06), run_time=0.6)

        # ========================================================== 6. step 4: two roles; the quota project
        f6 = form_at(console_form("Permissions (optional)",
                                  [("Role", ""), ("button", "Add another role"), ("Role", "")],
                                  form_w=FORM_W, path="IAM & Admin → Service Accounts"))
        ill6 = ill_for(f6)
        r1 = role_card("Agent Platform User", "may call the model")
        r2 = role_card("Service Usage Consumer", "may bill the quota project")
        r1.next_to(m_badge, DOWN, buff=0.15)
        r2.next_to(r1, DOWN, buff=0.12)
        p = code("tutorial/app/translation_demo/speech.py", 102, 105, font_size=20, dedent=True,
                 cuts={103: "scopes=["})
        p.next_to(f6, DOWN, buff=0.3).align_to(f6, LEFT)
        bar = line_bar(p.code, 2, TURN, 0.22)
        f7 = form_at(console_form("Principals with access (optional)",
                                  [("Service account users role", ""), ("Service account admins role", ""),
                                   ("button", "Done")],
                                  form_w=FORM_W, path="IAM & Admin → Service Accounts"))
        ill7 = ill_for(f7)
        assert p.get_bottom()[1] > -3.55 and p.get_right()[0] < r2.get_left()[0] - 0.2, (p.get_bottom(), p.get_right())
        assert r2.get_bottom()[1] > -2.0 and r2.get_right()[0] < 6.55
        with self.voiceover(SAY[6]) as vo:
            self.add(ill5)
            self.play(track(tr, 4), ReplacementTransform(f5, f6), ReplacementTransform(ill5, ill6),
                      FadeOut(email), run_time=0.8)
            self.add(ill6)
            vo.wait_until("Agent Platform User lets it")
            self.play(f6.fill(0, "Agent Platform User"), run_time=0.7)
            self.add(ill6)
            self.play(FadeIn(r1, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Service Usage Consumer lets it")
            self.play(f6.press(1), run_time=0.6)
            self.add(ill6)
            self.play(f6.fill(2, "Service Usage Consumer"), run_time=0.7)
            self.add(ill6)
            self.play(FadeIn(r2, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("the project whose quota")
            self.play(Indicate(r2.text[1], color=COST, scale_factor=1.08), run_time=0.8)
            vo.wait_until("The app names your project")
            self.play(FadeIn(p, shift=UP * 0.1), run_time=0.6)
            span = code_span(p.code, 2, "quota_project_id=project")
            self.play(FadeIn(bar), *[g.animate.set_color(TURN) for g in span], run_time=0.6)
            self.add(p, bar)
            vo.wait_until("Leave both principal fields")
            self.add(ill6)
            self.play(FadeOut(VGroup(p, bar)), ReplacementTransform(f6, f7), ReplacementTransform(ill6, ill7),
                      run_time=0.8)
            self.add(ill7)
            self.flash(f7.rows[0].field, f7.rows[1].field, run_time=0.8)
            vo.wait_until("and select Done")
            self.play(f7.press(2), run_time=0.7)
            self.add(ill7)

        # ========================================================== 7. step 5: the email; no key; the recording
        note_rows = VGroup(mono(RUNTIME_SA, 20, INK), mono("@" + WEB_EMAIL.split("@", 1)[1], 20, INK))
        note_rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        email_note = card([note_rows], S.GREY, head="your note: the runtime account's email")
        email_note.move_to(FORM_UL, aligned_edge=UL)
        rm380 = readme_card(380, "You do not need to create or download a key.")
        rm380.next_to(email_note, DOWN, buff=0.3).align_to(email_note, LEFT)
        key = crossed_key(0.9).move_to([2.3, -2.45, 0])
        l3 = dashed_chip("L3 · secrets/…json key").next_to(key, RIGHT, buff=0.35)
        rec = recorded_rows("part3-speech-recorded", 2,
                            ["Filtered result: runtime account Enabled, No keys;", "open its row"],
                            "identity GIF")
        rec.next_to(rm380, DOWN, buff=0.35).align_to(email_note, LEFT)
        yt = your_turn().next_to(rec, DOWN, buff=0.2).align_to(rec, RIGHT)
        assert l3.get_right()[0] < 6.55 and yt.get_bottom()[1] > -3.55
        assert max(m.get_right()[0] for m in (email_note, rm380, rec)) < r1.get_left()[0] - 0.2
        with self.voiceover(SAY[7]) as vo:
            self.play(track(tr, 5), FadeOut(VGroup(f7, ill7)), run_time=0.6)
            vo.wait_until("note the account's email")
            self.play(FadeIn(email_note, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(note_rows, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("No key to create")
            self.play(FadeIn(rm380, shift=UP * 0.1), FadeIn(key.key), run_time=0.6)
            self.play(Create(key.cross), run_time=0.5)
            vo.wait_until("in lecture 3")
            self.play(FadeIn(l3, shift=LEFT * 0.4), run_time=0.6)
            vo.wait_until("here none exists")
            l3_x = strike(l3.text, S.GREY, stroke=2)   # thin: the words stay legible
            self.play(Create(l3_x), l3.text.animate.set_opacity(0.8),
                      Indicate(key.cross, color=ERR, scale_factor=1.2),
                      run_time=0.7)
            vo.wait_until("The recording shows")
            self.play(FadeIn(rec, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(rec.body, color=TURN, scale_factor=1.03), run_time=0.7)
            vo.wait_until("pause and create yours")
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)

        # ========================================================== 8. the gcloud alternative (README:412-419)
        gt = term(P_REPO, 13, T_GCLOUD, size=20)
        npc = no_panel_chip()
        npc.move_to([6.5 - npc.width / 2, (gt.box.get_top()[1] + TRACK_BOTTOM) / 2, 0])
        assert npc.get_left()[0] > tr.get_right()[0] + 0.2 and gt.box.get_top()[1] < TRACK_BOTTOM - 0.1
        groups = [gc_rows[0:1], gc_rows[1:3], gc_rows[3:5], gc_rows[5:8]]
        anchors = ["enables the API", "creates the account", "and adds the two roles", None]
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(email_note, rm380, key, l3, l3_x, rec, yt, m_door, m_lab, m_badge, m_cloud,
                                     r1, r2)), track(tr, 4, "gcloud"), run_time=0.6)
            self.play(FadeIn(gt, shift=UP * 0.15), run_time=0.4)
            typed = []
            for rows, phrase in zip(groups, anchors):
                if phrase:
                    vo.wait_until(phrase)
                typed += type_lines(self, gt, rows, type_time=0.9 / len(rows))
            self.play(FadeIn(npc, shift=DOWN * 0.1), run_time=0.4)
            all_rows = [r for ln in typed for r in rows_of(ln)]
            binds = [r for r in all_rows if "add-iam-policy-binding" in getattr(r, "text", "")]
            assert len(binds) == 2, [getattr(r, "text", "") for r in all_rows]
            rings = [ring(substring(r, "add-iam-policy-binding"), SHARED) for r in binds]
            short = [r for r in all_rows if getattr(r, "text", "").strip() == gc_rows[6].strip()]
            assert len(short) == 1
            pw = row_tag("project-wide", SHARED)
            beside(pw, short[0], buff=0.45)
            vo.wait_until("both bindings are on the whole project")
            self.play(*[Create(rg) for rg in rings], run_time=0.6)
            self.add(gt, *rings)
            pin(self, short[0], pw, run_time=0.4)
            self.play(*[Indicate(rg, color=SHARED, scale_factor=1.03) for rg in rings],
                      Indicate(pw, color=SHARED, scale_factor=1.1), run_time=0.8)
            self.add(gt, *rings)
            self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
