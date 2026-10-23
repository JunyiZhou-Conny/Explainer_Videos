"""S03 · An identity for code (AC215 L10) — tracker A2 → A3, `Lecture 10 · slides 24–25, 31–38`.

Beats (script.md, ## S03; one voiceover block each):
0. Concept first (slide 25 redrawn): a TEAL server box 'your code'; an ID badge is minted (GREEN
   outline, the service account's email on three rows); it clips onto the server; a BLUE arrow runs
   from the server to the BLUE Google building, a small badge rides it; a GREY 'login screen' chip is
   struck: no human figure anywhere.
1. Slide 31's rule as a four-row decision card (row 4 GREY dashed). A YELLOW pointer walks down,
   stops on row 3 (ringed), slides to row 4; a 'CI runner · GitHub Actions' chip is stamped
   'vouched for', a 'your laptop' chip 'nobody vouches'; a GREEN key file arrives by the laptop.
2. A schematic console (`illustration`, README.md · lines 48–52): IAM & Admin → Service accounts →
   Create service account (name typed) → Grant this service account access to project: Storage
   Admin · Gemini Enterprise Agent Platform User, with the GREY 'formerly Vertex AI User' chip
   (llm-finetuning README.md:44–46). `▶ your turn`; a GREY `extra` card (gcloud equivalents,
   YOUR_PROJECT_ID; not spoken) in the bottom-right corner.
3. The `erratum` card, three lines, one per sentence.
4. Tracker A3. Console continued (README.md · lines 54–55): the account → KEYS → ADD Key (Create New
   Key) → JSON; a key file drops out; the two banners in our own words; `▶ your turn`. The key card
   (`illustration`, KEY_FIELDS: zeroed ids, PLACEHOLDER) unfolds from the file; its rows light as
   named; `private_key` glows RED with the chip 'something you have · one factor'. Empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, ERR, IMAGE, INK, KEY, NARRATION, PASS, SAY_COUNT, TURN, card, dashed_chip,
                    extra_tag, file_glyph, flash_tag, google_building, grey_chip, illustration_tag,
                    key_card, key_glyph, label, lref, mono, note, ring, steady, strike, tag, track,
                    tracker, under, warning_sign, erratum_tag, your_turn, SA_NAME)
from explainer import style as S

SAY = NARRATION["S03"]


# ------------------------------------------------------------------ local pieces
def id_badge(size: float = 22) -> VGroup:
    """The service account's ID badge, the email on three rows (the shared badge() is 8 wide on two
    rows; this one clips onto a small server). .frame .clip .text (rows: name, @project, domain)"""
    txt = VGroup(mono(SA_NAME, size, INK), mono("@your-gcp-project", size, INK),
                 mono(".iam.gserviceaccount.com", size, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    port = RoundedRectangle(width=0.62, height=0.62, corner_radius=0.08, stroke_color=KEY,
                            stroke_width=2.5).set_fill(KEY, 0.15)
    gear = Circle(radius=0.15, stroke_color=KEY, stroke_width=3).move_to(port)
    row = VGroup(VGroup(port, gear), txt).arrange(RIGHT, buff=0.3)
    frame = RoundedRectangle(width=row.width + 0.55, height=row.height + 0.5, corner_radius=0.14,
                             stroke_color=KEY, stroke_width=3.5).set_fill(S.GREY_DARKER, 1)
    row.move_to(frame)
    clip = RoundedRectangle(width=0.55, height=0.18, corner_radius=0.05, stroke_color=KEY,
                            stroke_width=2.5).set_fill(S.BG, 1).move_to(frame.get_top())
    g = VGroup(frame, row, clip)
    g.frame, g.clip, g.text = frame, clip, txt
    return g


def server_box(bw: float = 2.0, bh: float = 1.35) -> VGroup:
    """A small TEAL server: a box, its name, two rack slots with lights. .body .text"""
    body = RoundedRectangle(width=bw, height=bh, corner_radius=0.1, stroke_color=IMAGE,
                            stroke_width=3).set_fill(IMAGE, 0.12)
    t = label("your code", 22, INK).move_to(body.get_top() + DOWN * 0.32)
    slots = VGroup()
    for k in range(2):
        y = body.get_top()[1] - 0.72 - k * 0.3
        slots.add(Line([-bw / 2 + 0.25, y, 0], [bw / 2 - 0.55, y, 0], color=IMAGE, stroke_width=3))
        slots.add(Dot([bw / 2 - 0.32, y, 0], radius=0.05, color=IMAGE))
    g = VGroup(body, slots, t)
    g.body, g.text = body, t
    return g


RULES = (("public metered call", "API key"),
         ("an app acting for a consenting user", "OAuth"),
         ("code calling Google", "service account"),
         ("code outside Google, vouched for", "federation"))


def rule_card(size: float = 24) -> VGroup:
    """Slide 31's rule, redrawn: four rows 'situation → credential' in aligned columns; row 4 GREY
    with a GREY dashed outline. .frame .rows (each row: .left .right) .dash"""
    lefts = [label(a, size, S.GREY if i == 3 else INK) for i, (a, _) in enumerate(RULES)]
    lw = max(m.width for m in lefts)
    rows = []
    for i, (lf, (_, b)) in enumerate(zip(lefts, RULES)):
        col = S.GREY if i == 3 else (KEY if i == 2 else INK)
        ar = label("→", size, S.GREY)
        rt = label(b, size, col)
        lf.move_to(ORIGIN, aligned_edge=LEFT)
        ar.move_to([lw + 0.45, 0, 0])
        rt.next_to(ar, RIGHT, buff=0.3)
        r = VGroup(lf, ar, rt)
        r.left, r.right = lf, rt
        rows.append(r)
    c = card(rows, head="which credential? · slide 31's rule, redrawn", buff=0.32)
    dash = ring(rows[3], S.GREY, buff=0.12, dashed=True)
    c.add(dash)
    c.rows, c.dash = rows, dash
    return c


def stamp(s: str, color) -> VGroup:
    """A small rotated stamp (a tag in `color`)."""
    return tag(s, color).rotate(0.12)


def console_window(ref: str, win_w: float = 12.6, win_h: float = 3.7, nav_w: float = 3.2) -> VGroup:
    """The schematic console (no logo, no screenshot): GREY frame, a title bar 'Cloud console ·
    <README ref>' with the illustration tag at its right end, a nav column 'IAM & Admin' >
    'Service accounts'. Centre at the origin. .frame .title .tag .nav (.iam .sa) .sep .div"""
    frame = RoundedRectangle(width=win_w, height=win_h, corner_radius=0.16, stroke_color=S.GREY,
                             stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    bar_h = 0.55
    top = win_h / 2
    sep = Line([-win_w / 2, top - bar_h, 0], [win_w / 2, top - bar_h, 0], color=S.GREY, stroke_width=2)
    title = steady(f"Cloud console  ·  {ref}", 20, S.GREY)
    title.move_to([-win_w / 2 + 0.3, top - bar_h / 2, 0], aligned_edge=LEFT)
    tg = illustration_tag().move_to([win_w / 2 - 0.25, top - bar_h / 2, 0], aligned_edge=RIGHT)
    x_div = -win_w / 2 + nav_w
    div = Line([x_div, top - bar_h, 0], [x_div, -win_h / 2, 0], color=S.GREY, stroke_width=2)
    iam = label("IAM & Admin", 22, INK).move_to([-win_w / 2 + 0.3, top - bar_h - 0.5, 0], aligned_edge=LEFT)
    sa = label("Service accounts", 22, INK).move_to([-win_w / 2 + 0.6, top - bar_h - 1.1, 0], aligned_edge=LEFT)
    nav = VGroup(iam, sa)
    nav.iam, nav.sa = iam, sa
    g = VGroup(frame, sep, div, title, tg, nav)
    g.frame, g.title, g.tag, g.nav, g.sep, g.div = frame, title, tg, nav, sep, div
    return g


def pane_origin(con) -> tuple[float, float]:
    """(left x, top y) of the console's main pane, wherever the console stands."""
    return con.div.get_x() + 0.35, con.sep.get_y() - 0.3


def field_box(text_mob, box_w: float, color=S.GREY, caret: bool = False) -> VGroup:
    """An input box (GREY outline) holding `text_mob` at its left (and a '▾' at the right)."""
    b = RoundedRectangle(width=box_w, height=0.56, corner_radius=0.08, stroke_color=color,
                         stroke_width=2).set_fill(S.BG, 1)
    text_mob.move_to(b.get_left() + RIGHT * (0.2 + text_mob.width / 2))
    g = VGroup(b, text_mob)
    if caret:
        g.add(label("▾", 22, S.GREY).move_to(b.get_right() + LEFT * 0.3))
    g.box, g.text = b, text_mob
    return g


def two_line_chip(a: str, b: str, color=S.GREY, size: float = 20, text_color=S.GREY) -> VGroup:
    """A chip of two short lines (label font). .box .text"""
    t = VGroup(label(a, size, text_color), label(b, size, text_color)).arrange(DOWN, aligned_edge=LEFT,
                                                                               buff=0.08)
    bx = RoundedRectangle(width=t.width + 0.45, height=t.height + 0.3, corner_radius=0.12,
                          stroke_color=color, stroke_width=2).set_fill(color, 0.1)
    t.move_to(bx)
    g = VGroup(bx, t)
    g.box, g.text = bx, t
    return g


def banner(s: str, banner_w: float, size: float = 22) -> VGroup:
    """A console warning banner in our own words: YELLOW warning sign + text, GREY box."""
    w = warning_sign(0.34, TURN)
    t = label(s, size, INK)
    row = VGroup(w, t).arrange(RIGHT, buff=0.25)
    bx = RoundedRectangle(width=banner_w, height=0.6, corner_radius=0.1, stroke_color=S.GREY,
                          stroke_width=2).set_fill(S.GREY_DARKER, 1)
    row.move_to(bx).align_to(bx, LEFT).shift(RIGHT * 0.25)
    g = VGroup(bx, row)
    g.box, g.text = bx, t
    return g


class IdentityForCode(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 5, len(SAY)

        tr = tracker("A", 2)
        ref = lref("24–25, 31–38")

        # ========================================================== 0. an identity for software
        server = server_box().move_to([-3.4, 1.55, 0])
        bdg = id_badge().move_to([0.6, 0.2, 0])
        hang = bdg.copy().move_to([server.get_center()[0], 0, 0]).align_to(server, UP).shift(DOWN * 1.75)
        lanyard = Line(server.body.get_bottom(), hang.clip.get_top(), color=KEY, stroke_width=3)
        gb = google_building(2.4, 3.0, door=False, meter_=False).move_to([4.75, -1.15, 0], aligned_edge=DOWN)
        y_call = 1.45
        call = Arrow([server.body.get_right()[0], y_call, 0], [gb.frame.get_left()[0] + 0.12, y_call, 0], buff=0.1,
                     color=CLOUD, stroke_width=4, tip_length=0.22, max_tip_length_to_length_ratio=0.1)
        rider = RoundedRectangle(width=0.36, height=0.26, corner_radius=0.05, stroke_color=KEY,
                                 stroke_width=2.5).set_fill(KEY, 0.4).move_to(call.get_start())
        login = dashed_chip("login screen", S.GREY, 22).move_to([0.45, y_call + 0.6, 0])
        no_login = strike(login.text, S.GREY)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.8)
            vo.wait_until("A service account is an identity")
            self.play(FadeIn(server, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("Its email looks like this badge")
            self.play(GrowFromCenter(bdg), run_time=0.8)
            self.play(Indicate(bdg.frame, color=KEY, scale_factor=1.04), run_time=0.6)
            vo.wait_until("llm-service-account, at")
            self.play(Indicate(bdg.text[0], color=KEY, scale_factor=1.12), run_time=0.7)
            vo.wait_until("at your project")
            self.play(Indicate(bdg.text[1], color=KEY, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Code wears it")
            self.play(bdg.animate.move_to(hang), run_time=0.9)
            self.play(Create(lanyard), run_time=0.4)
            vo.wait_until("to call Google")
            self.play(FadeIn(gb, shift=LEFT * 0.2), GrowArrow(call), run_time=0.8)
            self.add(rider)
            self.play(rider.animate.move_to(call.get_end() + LEFT * 0.25), run_time=0.9)
            vo.wait_until("with no login screen")
            self.play(FadeIn(login, shift=DOWN * 0.15), run_time=0.4)
            self.play(Create(no_login), run_time=0.4)
            self.play(FadeOut(VGroup(login, no_login)), run_time=0.5)

        # ========================================================== 1. slide 31's rule, walked
        rc = rule_card().move_to([0.35, 0.95, 0])
        ptr = Triangle(color=TURN).set_fill(TURN, 1).set_stroke(width=0).rotate(-PI / 2)
        ptr.stretch_to_fit_height(0.3).stretch_to_fit_width(0.3)

        def at_row(i):
            return [rc.frame.get_left()[0] - 0.3, rc.rows[i].get_center()[1], 0]

        ptr.move_to(at_row(0))
        r3 = ring(rc.rows[2], TURN, buff=0.1)
        ci = grey_chip("CI runner · GitHub Actions", 22).move_to([-3.4, -1.75, 0])
        lap = grey_chip("your laptop", 22).move_to([2.1, -1.75, 0])
        st_ci = stamp("vouched for", PASS).next_to(ci, DOWN, buff=0.15)
        st_lap = stamp("nobody vouches", S.GREY).next_to(lap, DOWN, buff=0.15)
        kg = key_glyph(0.9).next_to(lap, RIGHT, buff=0.7)
        kl = label("a key file", 22, KEY).next_to(kg, DOWN, buff=0.25)
        old0 = VGroup(server, bdg, lanyard, gb, call, rider)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(old0, shift=UP * 0.2), run_time=0.5)
            self.remove(old0)
            self.play(FadeIn(rc, shift=DOWN * 0.2), FadeIn(ptr), run_time=0.7)
            self.play(Indicate(rc.rows[0].right, color=INK, scale_factor=1.12), run_time=0.6)
            vo.wait_until("An app acting for a consenting user")
            self.play(ptr.animate.move_to(at_row(1)), run_time=0.4)
            self.play(Indicate(rc.rows[1].right, color=INK, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Our code calls Vertex AI")
            self.play(ptr.animate.move_to(at_row(2)), run_time=0.4)
            vo.wait_until("so it gets a service account")
            self.play(Create(r3), Indicate(rc.rows[2].right, color=KEY, scale_factor=1.12), run_time=0.7)
            vo.wait_until("The rule's last line")
            self.play(ptr.animate.move_to(at_row(3)), r3.animate.set_stroke(opacity=0.35), run_time=0.5)
            self.play(Indicate(rc.rows[3].right, color=INK, scale_factor=1.12), run_time=0.6)
            vo.wait_until("That needs someone to vouch")
            self.play(FadeIn(ci, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("as GitHub does")
            self.play(FadeIn(st_ci, scale=1.4), run_time=0.4)
            flash_tag(self, st_ci, PASS)
            vo.wait_until("A laptop has nobody")
            self.play(FadeIn(lap, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(st_lap, scale=1.4), run_time=0.4)
            vo.wait_until("so the course hands you a key file")
            self.play(FadeIn(kg, shift=LEFT * 0.3), FadeIn(kl), run_time=0.6)
            self.play(Indicate(kg, color=KEY, scale_factor=1.2), run_time=0.6)

        # ========================================================== 2. the console: account and roles
        con = console_window("README.md · lines 48–52").move_to([0, 0.9, 0])
        px, py = pane_origin(con)
        sel = ring(con.nav.iam, TURN, buff=0.1)
        sel_sa = ring(con.nav.sa, TURN, buff=0.1)
        # step a: create
        h1 = label("Create service account", 24, INK).move_to([px, py - 0.2, 0], aligned_edge=LEFT)
        lab1 = note("Service account name").next_to(h1, DOWN, buff=0.35).align_to(h1, LEFT)
        name = mono(SA_NAME, 22, INK)
        fld = field_box(name, 5.2).next_to(lab1, DOWN, buff=0.15).align_to(h1, LEFT)
        step_a = VGroup(h1, lab1, fld)
        # step b: grant
        h2 = label("Grant this service account access to project", 24, INK)
        h2.move_to([px, py - 0.2, 0], aligned_edge=LEFT)
        role1 = field_box(label("Storage Admin", 22, INK), 7.0, caret=True)
        role2 = field_box(label("Gemini Enterprise Agent Platform User", 22, INK), 7.0, caret=True)
        r1 = VGroup(note("Role"), role1).arrange(RIGHT, buff=0.3)
        r2 = VGroup(note("Role"), role2).arrange(RIGHT, buff=0.3)
        r1.next_to(h2, DOWN, buff=0.3).align_to(h2, LEFT)
        r2.next_to(r1, DOWN, buff=0.15).align_to(h2, LEFT)
        was = two_line_chip("formerly Vertex AI User · role ID roles/aiplatform.user",
                            "llm-finetuning README.md:44–46")
        was.next_to(role2, DOWN, buff=0.15).align_to(role2, LEFT)
        yt = your_turn().move_to([-5.3, -1.75, 0])
        xc = card([VGroup(extra_tag(), note("the same from a terminal · suggested, not in the repo"))
                   .arrange(RIGHT, buff=0.25),
                   mono("gcloud iam service-accounts create \\", 20, INK),
                   mono("  llm-service-account --project=YOUR_PROJECT_ID", 20, INK),
                   mono("gcloud projects add-iam-policy-binding \\", 20, INK),
                   mono("  YOUR_PROJECT_ID --member=… --role=…", 20, INK)], size=20, buff=0.1)
        xc.move_to([6.5, -1.07, 0], aligned_edge=UR)
        old1 = VGroup(rc, ptr, r3, ci, lap, st_ci, st_lap, kg, kl)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(old1, shift=UP * 0.2), run_time=0.5)
            self.remove(old1)
            self.play(FadeIn(con, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("Open IAM and Admin")
            self.play(Create(sel), run_time=0.5)
            vo.wait_until("then Service accounts")
            self.play(Transform(sel, sel_sa), run_time=0.5)
            vo.wait_until("Create one named")
            self.play(FadeIn(h1, shift=LEFT * 0.2), FadeIn(lab1), FadeIn(fld.box), run_time=0.5)
            self.play(AddTextLetterByLetter(name), run_time=1.0)
            vo.wait_until("Grant it two roles")
            self.play(FadeOut(step_a, shift=UP * 0.3), FadeIn(h2, shift=UP * 0.3), run_time=0.6)
            self.remove(step_a)
            vo.wait_until("Storage Admin")
            self.play(FadeIn(r1, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("and Gemini Enterprise")
            self.play(FadeIn(r2, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("The second role was formerly")
            self.play(FadeIn(was, shift=DOWN * 0.15), Indicate(role2.text, color=INK, scale_factor=1.05),
                      run_time=0.7)
            vo.wait_until("it is the same role underneath")
            self.play(Indicate(was.text[0], color=INK, scale_factor=1.06), run_time=0.7)
            self.play(FadeIn(xc, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("Pause and create yours")
            self.play(FadeIn(yt, shift=RIGHT * 0.2), run_time=0.4)
            flash_tag(self, yt, TURN)

        # ========================================================== 3. two kind notes (erratum)
        lines = ["slides: data-service-account, one storage role → next week's account (L11)",
                 "this app: the Gemini role does the work; Storage Admin rides along for L08 reuse",
                 "slide 45: Storage Object Admin, and only when needed"]
        ec = card(lines, size=22, buff=0.3).move_to([0, 0.35, 0])
        et = erratum_tag().next_to(ec.frame, UP, buff=0.15).align_to(ec.frame, RIGHT)
        for ln in ec.body:
            ln.set_opacity(0)
        both = grey_chip("README.md · lines 50–52: grant both", 22).next_to(ec.frame, DOWN, buff=0.4)
        old2 = VGroup(con, sel, h2, r1, r2, was, xc, yt)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(old2, shift=UP * 0.2), run_time=0.5)
            self.remove(old2)
            self.play(FadeIn(ec.frame, scale=0.97), FadeIn(et, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("The slides' demo account")
            self.play(ec.body[0].animate.set_opacity(1), run_time=0.6)
            vo.wait_until("next week's")
            self.play(Indicate(ec.body[0], color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("And this app never touches storage")
            self.play(ec.body[1].animate.set_opacity(1), run_time=0.6)
            vo.wait_until("Grant both anyway")
            self.play(FadeIn(both, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("The lecture's rule, least privilege")
            self.play(ec.body[2].animate.set_opacity(1), run_time=0.6)
            vo.wait_until("would grant less")
            self.play(Indicate(ec.body[2], color=INK, scale_factor=1.04), run_time=0.7)
            vo.wait_until("part 2 comes back to it")
            flash_tag(self, et, INK)

        # ========================================================== 4. the key: KEYS → ADD Key → JSON
        con2 = console_window("README.md · lines 54–55").move_to([0, 0.9, 0])
        px, py = pane_origin(con2)
        sel2 = ring(con2.nav.sa, TURN, buff=0.1)
        acct = VGroup(mono(SA_NAME, 24, INK), note("service account")).arrange(RIGHT, buff=0.3)
        acct.move_to([px, py - 0.2, 0], aligned_edge=LEFT)
        strip_y = acct.get_bottom()[1] - 0.62
        tabline = Line([px, strip_y, 0], [con2.frame.get_right()[0] - 0.35, strip_y, 0], color=S.GREY,
                       stroke_width=2)
        keys = label("KEYS", 22, INK).move_to([px + 0.6, strip_y + 0.24, 0])
        keys_u = under(keys, TURN, stroke=5, y=strip_y)
        btn_t = label("ADD Key (Create New Key)", 22, INK)
        btn = RoundedRectangle(width=btn_t.width + 0.5, height=0.56, corner_radius=0.08, stroke_color=S.GREY,
                               stroke_width=2.5).set_fill(S.BG, 1)
        btn.move_to([px, strip_y - 0.55, 0], aligned_edge=LEFT)
        btn_t.move_to(btn)
        json_opt = field_box(mono("JSON", 22, INK), 2.0).next_to(btn, DOWN, buff=0.12).align_to(btn, LEFT)
        btn_ring = ring(VGroup(btn), TURN, buff=0.06)
        json_ring = ring(json_opt.box, TURN, buff=0.06)
        fdl = file_glyph(0.7, KEY)
        fdl.move_to(json_opt.get_right() + RIGHT * 0.6)
        land = np.array([-5.7, -1.75, 0])
        fl = label("a private key JSON file", 22, KEY).next_to(land, DOWN, buff=0.55).align_to([-6.3, 0, 0], LEFT)
        ban1 = banner("a leaked key is a risk", 8.4).move_to([2.1, -1.75, 0])
        ban2 = banner("Google disables keys it finds in public repositories", 8.4).next_to(ban1, DOWN, buff=0.15)
        yt2 = your_turn().move_to([6.4, -3.25, 0], aligned_edge=RIGHT)
        pane = VGroup(acct, tabline, keys)

        kc = key_card(size=20).move_to([-1.75, 0.5, 0])
        kc.align_to([-6.3, 0, 0], LEFT)
        kt = illustration_tag().next_to(kc.frame, RIGHT, buff=0.3).align_to(kc.frame, UP)
        pk = kc.private_key
        pk_ring = ring(pk, ERR, buff=0.08)
        fac = two_line_chip("something you have", "one factor", ERR, 22, INK)
        fac.next_to(kc.frame, RIGHT, buff=0.3).match_y(pk)
        fac_ln = Line(pk_ring.get_right(), fac.get_left(), color=ERR, stroke_width=3)
        props = VGroup(grey_chip("works anywhere", 22), grey_chip("no second step", 22),
                       grey_chip("until deleted or disabled", 22)).arrange(RIGHT, buff=0.3)
        props.next_to(kc.frame, DOWN, buff=0.4).align_to(kc.frame, LEFT)
        pw = VGroup(label("treat it like a password,", 26, INK), label("never like config", 26, S.GREY)) \
            .arrange(RIGHT, buff=0.2).move_to(props).align_to(kc.frame, LEFT)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(ec, et, both), shift=UP * 0.2), track(tr, 3), run_time=0.6)
            self.remove(ec, et, both)
            self.play(FadeIn(con2, shift=UP * 0.2), FadeIn(sel2), FadeIn(acct), FadeIn(tabline), run_time=0.7)
            vo.wait_until("On the account's Keys tab")
            self.play(FadeIn(keys, shift=UP * 0.1), Create(keys_u), run_time=0.5)
            vo.wait_until("add a key")
            self.play(FadeIn(VGroup(btn, btn_t), shift=DOWN * 0.1), run_time=0.4)
            self.play(Create(btn_ring), run_time=0.4)
            vo.wait_until("choose JSON")
            self.play(FadeIn(json_opt, shift=DOWN * 0.1), FadeOut(btn_ring), run_time=0.4)
            self.play(Create(json_ring), run_time=0.3)
            vo.wait_until("and a file downloads")
            self.play(FadeIn(fdl, scale=0.6), run_time=0.3)
            self.play(fdl.animate.move_to(land), run_time=0.8)
            self.play(FadeIn(fl), FadeIn(ban1, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(ban2, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Pause and make yours")
            self.play(FadeIn(yt2, shift=LEFT * 0.2), run_time=0.4)
            flash_tag(self, yt2, TURN)
            vo.wait_until("Inside are your project")
            consolegrp = VGroup(con2, sel2, pane, keys_u, btn, btn_t, json_opt, json_ring, ban1, ban2, yt2, fl)
            self.play(FadeOut(consolegrp), run_time=0.5)
            self.remove(consolegrp)
            self.play(FadeIn(kc, scale=0.4, target_position=fdl.get_center()), FadeOut(fdl), run_time=0.8)
            self.play(FadeIn(kt, shift=LEFT * 0.15), Indicate(kc.rows["project_id"], color=INK, scale_factor=1.08),
                      run_time=0.7)
            vo.wait_until("the account's email")
            self.play(Indicate(kc.rows["client_email"], color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("a token address")
            self.play(Indicate(kc.rows["token_uri"], color=CLOUD, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and a private key")
            self.play(Indicate(pk, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("That private key is the whole secret")
            self.play(Create(pk_ring), Indicate(pk, color=ERR, scale_factor=1.1), run_time=0.7)
            vo.wait_until("It is one factor")
            self.play(Create(fac_ln), FadeIn(fac, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("it works anywhere")
            self.play(FadeIn(props[0], shift=UP * 0.15), run_time=0.4)
            vo.wait_until("with no second step")
            self.play(FadeIn(props[1], shift=UP * 0.15), run_time=0.4)
            vo.wait_until("until deleted or disabled")
            self.play(FadeIn(props[2], shift=UP * 0.15), run_time=0.4)
            vo.wait_until("Treat this file like a password")
            self.play(FadeOut(props, shift=DOWN * 0.15), FadeIn(pw, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(kc.frame, color=KEY, scale_factor=1.02), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
