"""S05 · Who may call it, who it runs as, where to look (AC215 L14 exam edition). Lecture: 14 · 16.

Beats (script.md "## S05", one voiceover block each):
0. The exam map (slots 1-3 filled) fades in, slot 4 activates ("4 · ...") and pulses. V4 (TwoDoors,
   lowered 0.7 so the README band above it holds a panel): the BLUE "translation-demo" box with a
   door on each side and the TEAL "your code" box. At "and the README keeps them separate"
   CODE(README.md: 361-362); at "Who may call" its "who may call our public app" turns PINK
   (underlined) and the left caption "who may call it" fades in; at "And what may" "what the running
   app may access" turns BLUE and the right caption "who it is when it calls out" fades in.
1. Left door. The GREY browser appears; at "With public access allowed" the schematic toggle "Allow
   public access" (ON, tag `illustration`, excerpt chip README.md line 281) and a PINK request
   passes the door to the code box; at "Without it" the toggle flips OFF and the next request
   bounces RED with "403"; at "before your code even runs" the code box dims (it never ran).
2. Right door. The 361-362 panel goes. At "The web app wears" the BLUE badge
   "translation-demo-runtime" pins under the box and the PINK email chip (README's
   YOUR_PROJECT_ID form) sits in the band; at "Agent Platform User" / "Service Usage Consumer"
   the role chips attach while CODE(README.md: 375) shows both names; at "You do not create"
   CODE(README.md: 380) with "You do not need to create or download a key" lit YELLOW, and the
   dashed GOLD key, crossed out, appears inside the box.
3. The left door and the README panel fade. At "The code just asks" CODE(speech.py: 102)
   `google.auth.default(` lit BLUE; at "the platform hands it a token" the BLUE "Cloud Run" block
   hands a token to the badge; at "for the attached account" CODE(speech.py: 109) (its message
   lit GRAY) and a PINK request leaves the right door for "Agent Platform"; at "No key file
   anywhere" the crossed key pulses GOLD.
4. At "One more arrow" the GREY "you" with an arrow to the badge, "Service Account User";
   CODE(README.md: 432-434), "Service Account User" and "to attach it" lit; at "That is a deployment
   permission" the GRAY chip "a deployment permission ≠ the badge's roles"; the roles pulse.
5. Two columns: the service box shrinks to the left column with its badge and two roles; at "The
   job gets its own badge" the BLUE "translation-audio (job)" box and its badge "translation-audio-job"
   on the right; at "the same two" copies of the two roles fly over; at "plus Storage Object Viewer"
   the PINK input-bucket chip and CODE(README.md: 685, 687 folded); at "and Storage Object Creator"
   the PINK output-bucket chip; at "The web app's account" the GRAY "no bucket roles" chip and
   CODE(README.md: 689-690); at "One badge per workload" both badges pulse.
6. Everything goes; lref(14, "16"). At "Slide 16 warns" the GRAY slide chip "Limited control and
   debugging"; at "The README says" three log windows and CODE(README.md: 1038, 1039, 1041, 1045
   folded); each window lights with its row ("build logs" + 1038; "service logs" + 1039, with 1041
   "Speech request is denied | Attached identity" lit BLUE; "job execution logs" + 1045). At "A
   finished build" the panel gives way to the excerpt chip README.md lines 228-229 "inspect logs
   rather than treating a completed build as proof", lit YELLOW.
7. The tag and the windows go; a fresh V4 (box, doors, captions, browser) returns above the card.
   RULE line 1 at "The rule" (a refused call bounces "403" at the door), line 2 at "The service
   account answers" (the call out to Agent Platform); at "When your own code is denied" that call
   turns RED and the card's second line pulses. The card shrinks into map slot 4; empty frame.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circumscribe,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Transform,
    VGroup,
)

from explainer import style as S
from explainer.scene import VoiceScene

from common import (
    CAPTION,
    CLOUD,
    COST,
    ERR,
    JOB_SA,
    NARRATION,
    ROUTE,
    RUNTIME_SA,
    RUNTIME_SA_EMAIL,
    SAFE_X,
    SAFE_Y,
    SERVICE_NAME,
    TURN,
    ExamMap,
    RuleCard,
    TwoDoors,
    _save_op,
    _set_op,
    badge,
    chip,
    dim,
    excerpt_chip,
    guard,
    illustration_tag,
    log_window,
    lref,
    role_chip,
    service_box,
    source_line,
    src_panel,
    under,
    undim,
    url_chip,
)

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real sources (checked)
README = "README.md"
SPEECH = "tutorial/app/translation_demo/speech.py"
WHO = "who may call our public app"
WHAT = "what the running app may access"
assert "Two permissions questions are separate" in source_line(README, 361) and WHO in source_line(README, 361)
assert WHAT in source_line(README, 362)
assert "Allow public access" in source_line(README, 281)
assert "Agent Platform User" in source_line(README, 375) and "Service Usage Consumer" in source_line(README, 375)
NOKEY = "You do not need to create or download a key."
assert NOKEY in source_line(README, 380)
assert "google.auth.default(" in source_line(SPEECH, 102)
MSG = "Configure local ADC or attach an authorized runtime service account."
assert MSG in source_line(SPEECH, 109)
assert "Service Account User" in source_line(README, 432) and "to attach it" in source_line(README, 433)
assert "Storage Object Viewer" in source_line(README, 685)
assert "Storage Object Creator" in source_line(README, 687)
assert "does not need these bucket" in source_line(README, 689)
assert "goes straight to the browser" in source_line(README, 690)
assert "Function build fails" in source_line(README, 1038) and "Build logs" in source_line(README, 1038)
assert "Text translation fails" in source_line(README, 1039) and "Service logs" in source_line(README, 1039)
assert "Speech request is denied" in source_line(README, 1041) and "Attached identity" in source_line(README, 1041)
assert "Output folder is empty" in source_line(README, 1045) and "Execution status, logs" in source_line(README, 1045)
L228 = source_line(README, 228).strip() + " " + source_line(README, 229).strip()
PROOF = "inspect logs rather than treating a completed build as proof"
assert PROOF in L228
assert RUNTIME_SA == "translation-demo-runtime" and JOB_SA == "translation-audio-job"
assert RUNTIME_SA_EMAIL == "translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com"

SLIDE16 = "Limited control and debugging"    # slide 16 (deck text)

RULE_TOP = "who may call → public access · refused at the door, code never runs"
RULE_BOTTOM = "what the code may touch → the service account's roles (no key) · a denied call from your code → fix the badge"

TOP_BAND = 2.55          # content stays below the active slot's label
BAND_TOP = 2.52          # the README band's top edge (under the label)
LEFT_X = -6.45


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


def band(p):
    """A README/code panel in the band under the map: left edge at LEFT_X, top at BAND_TOP."""
    return p.move_to([LEFT_X + p.width / 2, BAND_TOP - p.height / 2, 0])


def slide_chip(text: str, where: str):
    """A GREY lecture chip: the slide's words in quotes, then the slide number."""
    return chip(f"“{text}” · {where}", S.GREY, size=CAPTION)


class TwoQuestions(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        # ========================================================== 0. two permission questions
        m = ExamMap(filled=(1, 2, 3))
        td = TwoDoors()
        td.shift(DOWN * 0.7)                      # (the README band above it holds a panel)
        hide_now(td, "cap_l", "cap_r", "browser")
        td.parts["you"].move_to([-4.75, td.badge_.frame.get_center()[1] + 0.1, 0])   # (beat 4: left of the badge)
        p361 = band(src_panel(README, 361, 362, size=20, wrap_at=88))
        who = p361.span(361, WHO)
        what = p361.span(362, WHAT)
        u_who, u_what = under(who, ROUTE), under(what, CLOUD)
        inside_frame(td, p361)
        below_band(p361)
        apart(p361, td.parts["box"], 0.04)
        apart(p361, td.parts["cap_r"], 0.04)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(m), run_time=0.6)
            self.play(*m.activate(4), run_time=0.5)
            self.play(m.pulse(4), FadeIn(td, shift=UP * 0.15), run_time=1.0)
            vo.wait_until("and the README keeps them separate")
            self.play(FadeIn(p361, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Who may call")
            self.play(who.animate.set_color(ROUTE), Create(u_who), *td.parts_in("cap_l"), run_time=0.7)
            self.play(Indicate(td.doorl.leaf, color=ROUTE, scale_factor=1.1), run_time=0.6)
            vo.wait_until("And what may")
            self.play(what.animate.set_color(CLOUD), Create(u_what), *td.parts_in("cap_r"), run_time=0.7)
            self.play(Indicate(td.doorr.leaf, color=CLOUD, scale_factor=1.1), run_time=vo.remaining(0.6))

        # ========================================================== 1. the left door: who may call
        tg = td.toggle_
        illu = illustration_tag().next_to(td.parts["browser"], UP, buff=0.18).align_to(tg, LEFT)
        c281 = excerpt_chip("Allow public access", f"{README} · line 281 (excerpt)", line=source_line(README, 281))
        c281.next_to(tg, DOWN, buff=0.16).align_to(tg, LEFT)
        inside_frame(illu, c281)
        for a in (illu, c281, tg):
            apart(a, td.parts["box"], 0.05)
        apart(illu, td.parts["cap_l"], 0.05)
        with self.voiceover(SAY[1]) as vo:
            self.play(*td.parts_in("browser"), Indicate(td.parts["cap_l"], color=ROUTE, scale_factor=1.08),
                      run_time=0.8)
            vo.wait_until("With public access allowed")
            self.play(*td.set_public(True), FadeIn(illu), FadeIn(c281, shift=UP * 0.1), run_time=0.7)
            self.play(*td.call(True), run_time=1.3)
            vo.wait_until("Without it")
            self.play(*td.clear_calls(), *td.set_public(False), run_time=0.6)
            self.play(*td.call(False), run_time=1.2)
            c403 = td._last[2]
            vo.wait_until("before your code even runs")
            self.play(Indicate(c403, color=ERR, scale_factor=1.15), dim(td.parts["code"], 0.3), run_time=0.8)
            self.wait(vo.remaining(0.2))

        # ========================================================== 2. the right door: the badge and its roles
        email = band(url_chip(RUNTIME_SA_EMAIL))
        p375 = band(src_panel(README, 375, size=20, wrap_at=88))
        p380 = band(src_panel(README, 380, size=20, wrap_at=88))
        bar380 = p380.bar(380, TURN, 0.22)
        inside_frame(email, p375, p380)
        below_band(email, p375, p380)
        for p in (email, p375, p380):
            apart(p, td.parts["box"], 0.04)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p361, u_who, u_what)), run_time=0.5)
            self.play(Indicate(td.doorr.leaf, color=CLOUD, scale_factor=1.1),
                      Indicate(td.parts["cap_r"], color=CLOUD, scale_factor=1.06), run_time=0.8)
            vo.wait_until("The web app wears")
            self.play(*td.pin_badge(), FadeIn(email, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("translation demo runtime")
            self.play(Indicate(td.badge_.name, color=CLOUD, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Agent Platform User")
            self.play(FadeOut(email), FadeIn(p375), *td.add_roles("Agent Platform User"), run_time=0.6)
            self.play(p375.span(375, "Agent Platform User").animate.set_color(CLOUD), run_time=0.3)
            vo.wait_until("Service Usage Consumer")
            self.play(*td.add_roles("Service Usage Consumer"),
                      p375.span(375, "Service Usage Consumer").animate.set_color(CLOUD), run_time=0.6)
            vo.wait_until("You do not create")
            self.play(FadeOut(p375), FadeIn(p380), run_time=0.5)
            self.play(FadeIn(bar380), *td.no_key(), run_time=0.6)
            self.play(Indicate(td.parts["key"], color=COST, scale_factor=1.3), run_time=vo.remaining(0.6))
        roles = td.parts["roles"]
        inside_frame(roles, td.badge_)

        # ========================================================== 3. a token, not a key
        sp102 = band(src_panel(SPEECH, 102, size=20))
        bar102 = sp102.bar(102, CLOUD, 0.25)
        sp109 = band(src_panel(SPEECH, 109, size=20, wrap_at=72))
        bar109 = VGroup(*[sp109.bar(109, S.GREY, 0.25)])
        inside_frame(sp102, sp109, td.parts["platform"], td.parts["agent"])
        below_band(sp102, sp109)
        for p in (sp102, sp109):
            apart(p, td.parts["box"], 0.02)
            apart(p, td.parts["cap_r"], 0.02)
        apart(td.parts["platform"], td.badge_, 0.08)
        apart(td.parts["agent"], td.parts["cap_r"], 0.05)
        with self.voiceover(SAY[3]) as vo:
            self.play(*td.parts_out("door_l", "cap_l", "browser", "toggle"), *td.clear_calls(),
                      FadeOut(VGroup(illu, c281, p380, bar380)), undim(td.parts["code"]), run_time=0.7)
            self.play(FadeIn(sp102, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(bar102), Indicate(td.parts["code"], color=CLOUD, scale_factor=1.06), run_time=0.6)
            vo.wait_until("the platform hands it a token")
            self.play(*td.token(), run_time=1.4)
            vo.wait_until("for the attached account")
            self.play(FadeOut(VGroup(sp102, bar102)), FadeIn(sp109), FadeIn(bar109), run_time=0.6)
            self.play(*td.call_out(), Circumscribe(td.badge_.frame, color=CLOUD, buff=0.06), run_time=1.0)
            vo.wait_until("No key file anywhere")
            self.play(Indicate(td.parts["key"], color=COST, scale_factor=1.4), run_time=vo.remaining(0.8))

        # ========================================================== 4. your own arrow: Service Account User
        you = td.parts["you"]
        p432 = band(src_panel(README, 432, 434, size=20, wrap_at=88))
        u_sau = under(p432.span(432, "Service Account User"), TURN)
        u_att = under(p432.span(433, "to attach it"), TURN)
        dep = chip("a deployment permission ≠ badge roles", S.GREY, size=CAPTION)
        dep.move_to([-6.5 + dep.width / 2, -3.2, 0])
        inside_frame(you, p432, dep)
        below_band(p432)
        apart(p432, td.parts["box"], 0.04)
        apart(dep, roles, 0.08)
        apart(dep, you, 0.08)
        apart(you, td.parts["box"], 0.08)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(sp109, bar109)), run_time=0.4)
            vo.wait_until("One more arrow")
            self.play(*td.you_arrow(), run_time=1.6)
            sau = td.parts["sau"]
            inside_frame(sau)
            apart(sau, td.badge_, 0.06)
            apart(sau, dep, 0.06)
            vo.wait_until("To attach that badge")
            self.play(FadeIn(p432, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Service Account User on it")
            self.play(Create(u_sau), Create(u_att), Indicate(sau, color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("That is a deployment permission")
            self.play(FadeIn(dep, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("separate from what the badge")
            self.play(Indicate(roles, color=CLOUD, scale_factor=1.06), run_time=vo.remaining(0.8))

        # ========================================================== 5. one badge per workload
        COL_L, COL_R = -3.3, 3.3
        Y_BOX, Y_BADGE, ROW0, STEP = 2.05, 1.12, 0.5, 0.58
        w_box = td.parts["box"].copy()
        w_badge = td.badge_.copy()
        w_roles = roles.copy()
        tgt_box = service_box(SERVICE_NAME, w=4.2, h=0.7).move_to([COL_L, Y_BOX, 0])
        j_box = service_box("translation-audio (job)", w=4.2, h=0.7).move_to([COL_R, Y_BOX, 0])
        j_badge = badge(JOB_SA).move_to([COL_R, Y_BADGE, 0])
        b_tgt = w_badge.copy().move_to([COL_L, Y_BADGE, 0])
        r_tgt = [w_roles[k].copy().move_to([COL_L, ROW0 - k * STEP, 0]) for k in range(2)]
        j_same = [w_roles[k].copy().move_to([COL_R, ROW0 - k * STEP, 0]) for k in range(2)]
        j_in = role_chip("Storage Object Viewer · input bucket", ROUTE).move_to([COL_R, ROW0 - 2 * STEP, 0])
        j_out = role_chip("Storage Object Creator · output bucket", ROUTE).move_to([COL_R, ROW0 - 3 * STEP, 0])
        none_ = role_chip("no bucket roles", S.GREY).move_to([COL_L, ROW0 - 2 * STEP, 0])
        p685 = src_panel(README, [685, 687], size=20, wrap_at=88)
        p685.move_to([0, j_out.get_bottom()[1] - 0.08 - p685.height / 2, 0])
        p689 = src_panel(README, 689, 690, size=20, wrap={689: ["It does not"]})
        p689.move_to([0, j_out.get_bottom()[1] - 0.08 - p689.height / 2, 0])
        b685 = VGroup(p685.bar(685, ROUTE, 0.2), p685.bar(687, ROUTE, 0.2))
        b689 = VGroup(p689.bar(689, S.GREY, 0.25), p689.bar(690, S.GREY, 0.25))
        left_col = VGroup(tgt_box, b_tgt, *r_tgt, none_)
        right_col = VGroup(j_box, j_badge, *j_same, j_in, j_out)
        inside_frame(left_col, right_col, p685, p689)
        below_band(left_col, right_col)
        apart(left_col, right_col, 0.1)
        for p in (p685, p689):
            apart(p, left_col, 0.04)
            apart(p, right_col, 0.04)
        with self.voiceover(SAY[5]) as vo:
            self.add(w_box, w_badge, w_roles)
            self.play(FadeOut(td), FadeOut(VGroup(p432, u_sau, u_att, dep)), run_time=0.6)
            self.play(Transform(w_box, tgt_box), Transform(w_badge, b_tgt),
                      *[w_roles[k].animate.move_to(r_tgt[k]) for k in range(2)], run_time=1.0)
            vo.wait_until("The job gets its own badge")
            self.play(FadeIn(j_box, shift=LEFT * 0.3), run_time=0.5)
            self.play(FadeIn(j_badge, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("the same two Agent Platform roles")
            flying = [w_roles[k].copy() for k in range(2)]
            self.add(*flying)
            self.play(*[flying[k].animate.move_to(j_same[k]) for k in range(2)], run_time=0.9)
            vo.wait_until("plus Storage Object Viewer")
            self.play(FadeIn(j_in, shift=UP * 0.1), FadeIn(p685, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(b685[0]), run_time=0.3)
            vo.wait_until("and Storage Object Creator")
            self.play(FadeIn(j_out, shift=UP * 0.1), FadeIn(b685[1]), run_time=0.6)
            vo.wait_until("The web app's account")
            self.play(FadeOut(VGroup(p685, b685)), FadeIn(none_, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(p689, shift=UP * 0.1), FadeIn(b689), run_time=0.6)
            vo.wait_until("One badge per workload")
            self.play(Circumscribe(w_badge, color=TURN, buff=0.06), Circumscribe(j_badge, color=TURN, buff=0.06),
                      run_time=vo.remaining(0.8))

        # ========================================================== 6. where to look
        lr = lref(14, "16")
        s16 = slide_chip(SLIDE16, "slide 16")
        s16.move_to([LEFT_X + s16.width / 2, 2.2, 0])
        wins = VGroup(log_window("build logs"), log_window("service logs"), log_window("job execution logs"))
        wins.arrange(RIGHT, buff=0.6).move_to([0, 1.2, 0])
        plog = src_panel(README, [1038, 1039, 1041, 1045], size=20, wrap_at=72)
        plog.move_to([0, wins.get_bottom()[1] - 0.12 - plog.height / 2, 0])
        lb = {n: plog.bar(n, TURN, 0.2) for n in (1038, 1039, 1045)}
        lb[1041] = plog.bar(1041, CLOUD, 0.25)
        c228 = excerpt_chip(PROOF, f"{README} · lines 228–229 (excerpt)", line=L228)
        c228.move_to([0, -1.2, 0])
        inside_frame(lr, s16, wins, plog, c228)
        below_band(s16, wins)
        apart(s16, wins, 0.05)
        apart(wins, plog, 0.05)
        apart(wins, c228, 0.1)
        apart(s16, lr, 0.1)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(w_box, w_badge, w_roles, *flying, j_box, j_badge, j_in, j_out, none_,
                                     p689, b689)), run_time=0.6)
            vo.wait_until("Slide 16 warns")
            self.play(FadeIn(lr), FadeIn(s16, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("The README says where to look")
            self.play(LaggedStart(*[FadeIn(w, shift=UP * 0.1) for w in wins], lag_ratio=0.3), run_time=0.9)
            self.play(FadeIn(plog, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("build logs when a function build fails")
            self.play(*wins[0].light(TURN), FadeIn(lb[1038]), run_time=0.6)
            vo.wait_until("service logs when a request fails")
            self.play(*wins[1].light(TURN), FadeIn(lb[1039]), FadeIn(lb[1041]), run_time=0.6)
            vo.wait_until("and the job's execution logs")
            self.play(*wins[2].light(TURN), FadeIn(lb[1045]), run_time=0.6)
            vo.wait_until("A finished build is not proof")
            self.play(FadeOut(VGroup(plog, *lb.values())), FadeIn(c228, shift=UP * 0.1), run_time=0.6)
            self.play(c228.text.animate.set_color(TURN), Circumscribe(wins[0], color=TURN, buff=0.06),
                      run_time=vo.remaining(0.6))

        # ========================================================== 7. the rule -> map slot 4
        td2 = TwoDoors()
        rule = RuleCard(RULE_TOP, RULE_BOTTOM)
        inside_frame(td2, rule)
        below_band(td2)
        for k in ("box", "door_l", "door_r", "browser", "cap_l", "cap_r", "agent"):
            apart(td2.parts[k], rule, 0.06)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(s16, wins, c228, lr)), run_time=0.6)
            self.play(FadeIn(td2, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("public access answers who may call")
            self.play(rule.frame_in(), run_time=0.4)
            self.play(rule.line_in(0), run_time=0.6)
            vo.wait_until("and a refused caller")
            self.play(*td2.call(False), run_time=1.1)
            vo.wait_until("The service account answers")
            self.play(rule.line_in(1), *td2.clear_calls(), run_time=0.6)
            self.play(*td2.call_out(), run_time=0.9)
            vo.wait_until("When your own code is denied")
            self.play(td2.parts["out_arrow"].animate.set_color(ERR), Circumscribe(td2.parts["agent"], color=ERR, buff=0.06),
                      run_time=0.7)
            vo.wait_until("fix the badge")
            self.play(Indicate(rule.rows[1], color=TURN, scale_factor=1.03), run_time=vo.remaining(0.6))
        self.wait(0.6)
        self.play(FadeOut(td2), run_time=0.5)
        rule.shrink_into(self, m, 4)
        self.play(m.pulse(4), run_time=0.7)
        self.wait(0.5)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
        self.wait(0.3)
