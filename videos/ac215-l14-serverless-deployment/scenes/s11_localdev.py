"""S11 · Develop locally with ADC — tracker [3.3] (no step) → 1 … 5 (+ gcloud alternative at step 1,
extras at steps 3, 4 and 5); no lecture_ref.

Beats (script.md "## S11"; one voiceover block each):
0. TRACKER [3.3] appears, no step lit. A GREY chip "needs uv · docs.astral.sh/uv" (README:556).
   README card (README.md · lines 506–509): no image per edit; ADC lets the same code discover
   credentials locally and on Cloud Run. CODE(speech.py: 102) `google.auth.default(…` forks into two
   arrows: up to a BLUE "Cloud Run: the badge's token", down to a GREY "your laptop: an ADC file".
1. V6 impersonation ribbon: "you" signs in ("your Google account"), a PINK "Token Creator" ribbon
   to the BLUE runtime badge, short-lived tickets flow back and drop a GREY "ADC file" on the laptop
   disk; the dashed GOLD key crossed out "no private key downloaded"; a GREY-dashed L3 card
   "secrets/ key file" slides in and greys out.
2. TRACKER [3.3] 1. CONSOLE (README:519-525, illustration): Service Accounts → runtime account →
   Principals with access → Grant access; New principals YOUR_GOOGLE_ACCOUNT_EMAIL; Role Service
   Account Token Creator; a RED-struck "Service Account Admin · don't leave it"; Save. Then APIs &
   Services → Library → IAM Service Account Credentials API → Enable.
   RECORDED(part3-speech-recorded: 4) tagged "recorded · impersonation GIF".
3. TRACKER [3.3] 1 · gcloud alternative. Terminal `laptop · gcloud` types README:541-545 verbatim
   (no output panel); the three commands are bracketed, GREY chip "= step 1, as commands (README:538)".
4. TRACKER [3.3] 2. The bracket fades; README:547-548 typed; row chip "browser sign-in · no output
   shown". Two GREY cards: gcloud auth login → gcloud's own login / gcloud auth application-default
   login → the app's ADC file (README:86-87). They give way to README card 551–552 and a GREY card
   (README:552-554) on the quota project / Service Usage Consumer. `▶ your turn`.
5. TRACKER [3.3] 3. Terminal `laptop · dev shell`: `cd tutorial/app`, prompt changes, `uv sync
   --frozen` → TERM(dev/10: 3–4, …, 14, 23, 25, 27, 31, 32, 50); Installed 41 YELLOW, the six direct
   pins GREEN; GREY chip "Python 3.12.15 · uv 0.13.7 · at the time of recording"; GREEN lock chip on
   --frozen "install exactly the lock · never re-resolve". TRACKER [3.3] 3 · extra: `uv tree --depth 1`
   → TERM(dev/17: 3–9).
6. TRACKER [3.3] 4. GREY chip "same terminal as your exports · $PROJECT_ID must be set". Types
   dev/11's three rows → TERM(dev/11: 4–8 wrap); `http://0.0.0.0:8086` PINK. V5's envelope: GREY
   "you" writes PORT=8086 for the PURPLE gunicorn process, its PINK ear 0.0.0.0:8086 (no TEAL
   container: uv runs the app directly on the laptop). `▶ your turn`.
7. TRACKER [3.3] 4 · extra. Strip `laptop · second tab`: dev/12 → line 3 wrap (Play audio GREEN);
   dev/13 → 2, 4; dev/14 → 2, 4 RED. V6's laptop disk with an empty ADC slot; GREY chip "no sign-in on
   this recording machine = what skipping step 2 looks like". Then the main terminal: TERM(dev/11:
   9–12) (line 9 is the captured ^C).
8. TRACKER [3.3] 5. `cd ../..; pwd` → TERM(dev/18: 2); prompt back to the repository root; GREY
   chip "extra: pwd"; GREY chip "the app guide's 17 offline tests · exercises". Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S11"]

SPEECH_PY = "tutorial/app/translation_demo/speech.py"
FORM_UL = np.array([-6.45, 2.72, 0])


def row_with(rows, sub):
    """The first row (a mono_line) among `rows` whose text contains `sub`."""
    for r in rows:
        if sub in getattr(r, "text", ""):
            return r
    raise KeyError(f"{sub!r} not in {[getattr(r, 'text', '') for r in rows]}")


def color_sub(scene, t, rows, sub, color, run_time: float = 0.4):
    """PLAYS: colour substring `sub` of the row that holds it, then re-seat the terminal."""
    r = row_with(rows, sub)
    scene.play(*[g.animate.set_color(color) for g in substring(r, sub)], run_time=run_time)
    scene.add(t)
    return r


def ill_for(f: VGroup) -> VGroup:
    """The illustration tag on a form's top edge, right end."""
    tg = illustration_tag()
    return tg.move_to(f.frame.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))


def lock_glyph(h: float = 0.3, color=OWN) -> VGroup:
    """A small padlock (text-free): the lock file, --frozen."""
    body = RoundedRectangle(width=h * 1.1, height=h * 0.8, corner_radius=0.04, stroke_color=color,
                            stroke_width=2.5).set_fill(color, 0.3)
    shackle = Arc(radius=h * 0.33, start_angle=0, angle=PI, color=color, stroke_width=3)
    shackle.next_to(body, UP, buff=0)
    return VGroup(shackle, body)


def two_line_card(top, bottom, color=S.GREY) -> VGroup:
    """A GREY card of a mono command over a GREY label line."""
    return card([mono(top, 20, INK), label(bottom, 20, S.GREY)], color, buff=0.12)


def type_after_prompt(scene, t: Terminal, cmd: str, type_time: float):
    """PLAYS: type a command whose first token does not fit beside the long prompt: the prompt row
    ends in ' \\' and the command starts on the next row (the house fold would hard-break a word)."""
    def fold(text: str, first_prefix: int = 0) -> list[str]:
        rest = "    " + text[first_prefix:]
        assert len(rest) <= t.max_chars, rest
        return [text[:first_prefix] + "\\", rest]
    t.fold = fold
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


class LocalDevelopment(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S11"] == 9, len(SAY)
        assert "docs.astral.sh/uv" in readme(556)
        assert readme(506).startswith("You should not need to publish an image for every code edit.")
        assert "Application Default Credentials (ADC)" in readme(508) and "locally and on Cloud Run" in readme(509)
        assert "google.auth.default(" in excerpt(SPEECH_PY, 102, 102)
        assert "Service Account Token Creator" in readme(519) and "Service Account Admin" in readme(523)
        assert "IAM Service Account Credentials API" in readme(524)
        rows_541 = readme_rows(541, 545)
        rows_547 = readme_rows(547, 548)
        assert len(rows_541) == 5 and rows_541[0] == "export DEVELOPER_EMAIL=YOUR_GOOGLE_ACCOUNT_EMAIL"
        assert rows_547[0].startswith("gcloud auth application-default login --impersonate")
        assert "Equivalent commands" in readme(538)
        assert "does **not** set up the" in readme(86)
        assert "The ADC file stays on your machine" in readme(551) and "Service Usage Consumer" in readme(554)
        c10, c11, c12, c13, c14 = (capture(f"dev/{n}") for n in ("10", "11", "12", "13", "14"))
        c17, c18 = capture("dev/17"), capture("dev/18")
        assert c10.cmd_lines == ["cd tutorial/app", "uv sync --frozen"]
        assert c10.line(14).startswith("Installed 41 packages")
        assert c11.line(9) == "^C" and "Listening at: http://0.0.0.0:8086" in c11.line(5)
        assert c14.line(4) == "[HTTP 503]" and "Google credentials are unavailable" in c14.line(2)
        assert c18.cmd == "cd ../..; pwd"
        pins = (23, 25, 27, 31, 32, 50)
        assert [c10.line(n).split("==")[0].strip(" +") for n in pins] == \
            ["flask", "google-auth", "google-cloud-storage", "googletrans", "gunicorn", "requests"]

        # ========================================================== 0. why ADC: one line, two places
        tr = tracker_33(None)
        uv = grey_chip("needs uv · docs.astral.sh/uv")
        uv.move_to([6.5 - uv.width / 2, 3.25, 0])
        why = readme_card((506, 509), "\n".join([
            "You should not need to publish an image for every code edit. …",
            "Application Default Credentials (ADC) lets the same code",
            "discover credentials locally and on Cloud Run."]))
        why.move_to([0, 1.75, 0])
        adc_words = why.body[1][:34]                       # 'Application Default Credentials (ADC)' (no spaces)
        panel = code(SPEECH_PY, 102, dedent=True, cuts={102: "default("})
        panel.move_to([-2.6, -1.35, 0])
        fork = np.array([panel.get_right()[0] + 0.15, panel.code.get_center()[1], 0])
        up_t = VGroup(badge(RUNTIME_SA).scale(1.0), label("Cloud Run: the badge's token", 20, CLOUD))
        up_t.arrange(DOWN, buff=0.12).move_to([4.3, -0.15, 0])
        dn_t = VGroup(file_card("ADC file", LAPTOP), label("your laptop: an ADC file", 20, LAPTOP))
        dn_t.arrange(DOWN, buff=0.12).move_to([4.3, -2.65, 0])
        a_up = arrow(fork, up_t.get_left() + LEFT * 0.05, CLOUD)
        a_dn = arrow(fork, dn_t.get_left() + LEFT * 0.05, LAPTOP)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("and needs uv")
            self.play(FadeIn(uv, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("how would you develop locally")
            self.play(FadeIn(why, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("without publishing an image")
            self.play(Indicate(why.body[0], color=TURN, scale_factor=1.03), run_time=0.9)
            vo.wait_until("Application Default Credentials")
            self.play(adc_words.animate.set_color(TURN), run_time=0.5)
            self.add(why)
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("a token on Cloud Run")
            self.play(GrowArrow(a_up), FadeIn(up_t, shift=LEFT * 0.2), run_time=0.7)
            vo.wait_until("and a file on your laptop")
            self.play(GrowArrow(a_dn), FadeIn(dn_t, shift=LEFT * 0.2), run_time=0.7)

        # ========================================================== 1. V6: the impersonation ribbon
        rib = ImpersonationRibbon()
        l3 = VGroup(dashed_chip("L3"), file_card("secrets/ key file", PAST, dashed=True)).arrange(RIGHT, buff=0.2)
        l3.move_to([3.6, -2.55, 0])
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(why, panel, up_t, dn_t, a_up, a_dn, uv)), run_time=0.6)
            self.play(FadeIn(rib), run_time=0.6)
            vo.wait_until("your laptop impersonates it")
            rib.ribbon(self, run_time=1.0)
            vo.wait_until("You sign in as yourself")
            rib.sign_in(self, run_time=0.6)
            vo.wait_until("and receive short-lived tokens")
            rib.tickets(self, 3, run_time=1.6)
            rib.adc_file(self, run_time=0.6)
            vo.wait_until("no private key is ever downloaded")
            rib.no_key(self, run_time=0.7)
            self.play(FadeIn(l3, shift=LEFT * 0.6), run_time=0.6)
            self.play(l3.animate.set_opacity(0.35), run_time=0.8)

        # ========================================================== 2. step 1: the Token Creator grant (console)
        f1 = console_form("Principals with access → Grant access",
                          [("New principals", ""), ("Role", ""), ("button", "Save")],
                          form_w=8.4, path="IAM & Admin → Service Accounts → translation-demo-runtime")
        f1.move_to(FORM_UL, aligned_edge=UL)
        ill1 = ill_for(f1)
        sa_admin = label("Service Account Admin", 20, ERR)
        dont = label("don't leave it", 20, INK)
        st_in = VGroup(sa_admin, dont).arrange(DOWN, buff=0.1)
        st_box = box(st_in.width + 0.5, st_in.height + 0.35, ERR, fill=S.BG, fill_opacity=1)
        st_in.move_to(st_box)
        st_line = strike(sa_admin)
        struck = VGroup(st_box, st_in, st_line)
        struck.next_to(f1.frame, RIGHT, buff=0.3).match_y(f1.rows[1])
        f2 = console_form("IAM Service Account Credentials API", [("button", "Enable")], form_w=8.4,
                          path="APIs & Services → Library")
        f2.move_to(FORM_UL, aligned_edge=UL)
        ill2 = ill_for(f2)
        rec = recorded_card("part3-speech-recorded", 4, "impersonation GIF")
        rec.move_to([-6.45, -2.3, 0], aligned_edge=LEFT)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(rib), FadeOut(l3), track(tr, 1), run_time=0.6)
            self.play(FadeIn(f1, shift=UP * 0.2), FadeIn(ill1), run_time=0.7)
            vo.wait_until("grant your own user")
            self.play(f1.fill(0, DEV_EMAIL, color=TURN), run_time=0.8)
            vo.wait_until("Service Account Token Creator")
            self.play(f1.fill(1, "Service Account Token Creator"), run_time=0.8)
            vo.wait_until("Replace any preselected role")
            self.play(FadeIn(struck[:2], shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("and don't leave Service Account Admin")
            self.play(Create(st_line), run_time=0.5)
            self.play(f1.press(2), run_time=0.6)
            self.play(FadeIn(rec, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("Enable the IAM Service Account Credentials API")
            self.play(FadeOut(VGroup(f1, ill1, struck), shift=UP * 0.2), FadeIn(f2, shift=UP * 0.2), FadeIn(ill2),
                      run_time=0.7)
            self.play(f2.press(0), run_time=0.7)

        # ========================================================== 3. step 2 opens with step 1 as commands
        g = term(P_REPO, 8, T_GCLOUD, size=20)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(f2, ill2, rec)), track(tr, 1, "gcloud"), run_time=0.6)
            self.play(FadeIn(g, shift=UP * 0.2), run_time=0.5)
            typed = type_lines(self, g, rows_541, type_time=0.8)
            rows3 = [r for ln in typed for r in rows_of(ln)]
            bracket = SurroundingRectangle(VGroup(*[r.strut for r in rows3]), color=S.GREY, buff=0.06,
                                           stroke_width=2.5, corner_radius=0.06)
            bchip = grey_chip("= step 1, as commands (README:538)")
            under_term(g, bchip)
            vo.wait_until("if you used the console")
            self.play(Create(bracket), FadeIn(bchip, shift=DOWN * 0.1), run_time=0.6)
            self.play(Indicate(bchip, color=INK, scale_factor=1.05), run_time=0.7)

        # ========================================================== 4. step 2: ADC login + quota project
        auth_a = two_line_card("gcloud auth login", "→ gcloud's own login")
        auth_b = two_line_card("gcloud auth application-default login", "→ the app's ADC file")
        cards = VGroup(auth_a, auth_b).arrange(RIGHT, buff=0.4, aligned_edge=UP).move_to([0, 1.85, 0])
        stays = readme_card((551, 552), "The ADC file stays on your machine; it does not go into Git or the image.")
        stays.move_to([0, 2.2, 0])
        quota = card(["you also need to use the quota project",
                      "restricted? Service Usage Consumer from course staff"], S.GREY, size=20, buff=0.1)
        quota.next_to(stays, DOWN, buff=0.2).align_to(g.box, LEFT)
        yt = on_bar(g, turn_row())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(bracket, bchip)), track(tr, 2), run_time=0.5)
            typed2 = type_lines(self, g, rows_547, type_time=0.9)
            nchip = under_term(g, no_panel_chip("browser sign-in · no output shown"))
            self.play(FadeIn(nchip, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("impersonating the runtime account")
            imp_row = rows_of(typed2[0])[-1]
            r_imp = ring(substring(imp_row, '--impersonate-service-account="$WEB_EMAIL"'), ROUTE)
            self.play(Create(r_imp), run_time=0.5)
            vo.wait_until("and its quota project")
            q_row = rows_of(typed2[1])[-1]
            r_q = ring(substring(q_row, "set-quota-project"), S.GREY)
            self.play(Create(r_q), run_time=0.5)
            vo.wait_until("It is separate from gcloud auth login")
            self.play(FadeOut(r_imp), FadeOut(r_q), FadeIn(auth_a, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(auth_b, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("and its file stays on your machine")
            self.play(FadeOut(cards, shift=UP * 0.2), FadeIn(stays, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("Pause and sign in")
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("a restricted project may also need")
            self.play(FadeIn(quota, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(quota.body[1], color=SHARED, scale_factor=1.04), run_time=0.8)

        # ========================================================== 5. step 3: uv sync --frozen
        t = term(P_REPO, 12, T_DEV, size=20)
        ver = grey_chip("Python 3.12.15 · uv 0.13.7 · at the time of recording")
        under_term(t, ver)
        lk = VGroup(lock_glyph(), label("install exactly the lock · never re-resolve", 20, OWN)).arrange(RIGHT, buff=0.15)
        lk_box = box(lk.width + 0.4, lk.height + 0.24, OWN, fill_opacity=0.12)
        lk.move_to(lk_box)
        lock = VGroup(lk_box, lk)
        lock.next_to(ver, UP, buff=0.1).align_to(t.box, RIGHT)
        out10 = [(c10.line(3), OUTPUT), (c10.line(4), OUTPUT), ("…", OUTPUT), (c10.line(14), TURN)] + \
            [(c10.line(n), OWN) for n in pins]
        xb = on_bar(t, extra_row())
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(g, yt, stays, quota, nchip)), track(tr, 3), run_time=0.6)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            type_cmd(self, t, c10.cmd_lines[0], 0.6)
            t.set_prompt(P_APP)
            uvrow = type_cmd(self, t, c10.cmd_lines[1], 0.6)
            vo.wait_until("It installs 41 packages")
            out(self, t, out10, run_time=1.2)
            self.play(FadeIn(ver, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("exactly as the lock file says")
            r_fz = ring(substring(uvrow, "--frozen"), OWN)
            self.play(Create(r_fz), FadeIn(lock, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("An extra uv tree")
            self.play(FadeOut(r_fz), FadeOut(ver), track(tr, 3, True), FadeIn(xb), run_time=0.5)
            type_capture(self, t, c17, type_time=0.6)
            tree = out(self, t, c17.at((3, 9)), run_time=0.8)
            self.play(each(VGroup(*tree[1:]), OWN, scale=1.04, lag=0.1), run_time=1.0)
            self.add(t)

        # ========================================================== 6. step 4: run serve with three variables + PORT
        exp = grey_chip("same terminal as your exports · $PROJECT_ID must be set")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(lock), FadeOut(xb), track(tr, 4), run_time=0.5)
            resize(self, t, 9, keep=0, run_time=0.6)
            yt2 = on_bar(t, turn_row())
            exp.next_to(t.box, UP, buff=0.12).align_to(t.box, LEFT)
            self.play(FadeIn(exp, shift=DOWN * 0.1), run_time=0.4)
            type_after_prompt(self, t, c11.cmd_lines[0], 0.8)
            for row in c11.cmd_lines[1:]:
                type_cmd(self, t, row, 0.7, prompt=False)
            vo.wait_until("and PORT set to 8086")
            o11 = out(self, t, c11.at((4, 8)), wrap=True, run_time=0.9)
            lrow = color_sub(self, t, o11, "http://0.0.0.0:8086", ROUTE)
            # V5's envelope, laptop edition: no container, you hand gunicorn its port
            proc = RoundedRectangle(width=2.4, height=0.9, corner_radius=0.1, stroke_color=TOOL,
                                    stroke_width=3).set_fill(TOOL, 0.15).move_to([4.7, 2.1, 0])
            ptxt = mono("gunicorn", 22, INK).move_to(proc)
            e = ear("0.0.0.0:8086")
            e.glyph.move_to(proc.get_left() + LEFT * 0.22)
            e.text.next_to(proc, DOWN, buff=0.15).align_to(proc, LEFT)
            env = envelope("PORT=8086", YOU).move_to([0.7, 2.1, 0])
            me = you("you").move_to([-1.2, 2.0, 0])
            vo.wait_until("this time you set the port")
            self.play(FadeIn(VGroup(proc, ptxt)), FadeIn(me), run_time=0.5)
            self.play(FadeIn(env, shift=RIGHT * 0.4), run_time=0.6)
            self.play(env.animate.next_to(e.glyph, LEFT, buff=0.2), run_time=0.7)
            self.play(FadeIn(e, scale=0.6), Indicate(substring(lrow, "8086"), color=ROUTE, scale_factor=1.25),
                      run_time=0.7)
            self.add(t)
            vo.wait_until("Pause, run it")
            self.play(FadeIn(yt2, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("then translate and Play audio")
            self.play(Indicate(substring(lrow, "http://0.0.0.0:8086"), color=ROUTE, scale_factor=1.12), run_time=0.8)
            self.add(t, yt2)
            vo.wait_until("with your sign-in, it speaks")
            self.play(Indicate(e, color=ROUTE, scale_factor=1.15), run_time=0.8)
        pic = VGroup(proc, ptxt, e, env, me)

        # ========================================================== 7. extras: page, translate, speech 503; ^C
        tab = term(P_REPO, 8, T_TAB, size=20)
        txb = on_bar(tab, extra_row())
        r2 = ImpersonationRibbon()
        r2.remove(r2.you_, r2.badge_)
        r2.shift(np.array([2.3, 3.4, 0]))            # disk near (-2.5, 1.8): above the strip
        nosign = grey_chip("no sign-in on this recording machine = what skipping step 2 looks like")
        nosign.move_to([0.0, 0.75, 0])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(pic, exp, yt2)), FadeOut(t, shift=DOWN * 0.3), track(tr, 4, True),
                      run_time=0.6)
            self.play(FadeIn(tab, shift=UP * 0.2), FadeIn(txb), FadeIn(r2), run_time=0.5)
            type_capture(self, tab, c12, type_time=0.6)
            o12 = out(self, tab, c12.at(3), wrap=True, run_time=0.5)
            color_sub(self, tab, o12, "Play audio", OWN)
            vo.wait_until("and translation works")
            type_capture(self, tab, c13, type_time=0.5)
            o13 = out(self, tab, c13.at(2, 4), run_time=0.4)
            color_sub(self, tab, o13, "[HTTP 200]", PASS, run_time=0.3)
            vo.wait_until("Speech answers 503")
            type_capture(self, tab, c14, type_time=0.5)
            out(self, tab, c14.at(2, 4), wrap=True, run_time=0.5, color=ERR)
            r2.empty_slot(self, run_time=0.5)
            vo.wait_until("That is the missing sign-in")
            self.play(FadeIn(nosign, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(nosign.text, color=INK, scale_factor=1.04), run_time=0.8)
            self.wait(0.8)
            self.play(FadeOut(VGroup(tab, txb, r2, nosign)), track(tr, 4), run_time=0.5)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.4)
            out(self, t, c11.at((9, 12)), wrap=True, run_time=0.8)

        # ========================================================== 8. step 5: back to the repository root
        pwd = on_bar(t, row_tag("extra: pwd"))
        tests = grey_chip("the app guide's 17 offline tests · exercises")
        tests.next_to(t.box, UP, buff=0.12).align_to(t.box, RIGHT)
        with self.voiceover(SAY[8]) as vo:
            self.play(track(tr, 5), run_time=0.5)
            type_capture(self, t, c18, type_time=0.6)
            self.play(FadeIn(pwd, shift=LEFT * 0.1), run_time=0.3)
            out(self, t, c18.at(2), run_time=0.3)
            cd_prompt(self, t, P_REPO)
            self.play(FadeIn(tests, shift=DOWN * 0.1), run_time=0.4)
        self.play(FadeOut(VGroup(t, pwd, tests, tr)), run_time=0.8)
        self.wait(0.3)
