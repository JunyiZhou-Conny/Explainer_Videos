"""S14 · Webhooks, secrets and the Slack bell (AC215 L21). TRACKER P5 8 · extra, STRIP Summary.
Lecture: 21 · slides 7, 9 (beat 0), 21 · slides 10–12 (beat 2). Set pieces V8 SlackRoute, V6 on the
step rows (beats 6–7).

Beats (script.md "## S14", one voiceover block each):
0. TRACKER P5 8 · extra; the Part 2 strip with `Summary` current. LECTURE 21 · 7, 9. V8 arrow 1: the
   BLUE "GitHub" box fires a PINK "POST" arrow out to three GREY targets, one per phrase: "external
   CI (Jenkins)", "deploy server", "chat".
1. LECTURE off. A GREY chip "optional · your own Slack workspace · Slack app → Incoming Webhooks →
   Add New Webhook". Arrow 1 dims to a ghost ("the other direction"); V8 arrow 2: a BLUE runner
   (test-summary's last steps) POSTs in to the GREY '#build-alerts' window's PINK "incoming webhook"
   slot; the dimmed GitHub box wiggles ("doesn't ring this bell"), the runner's steps light up.
2. LECTURE 21 · 10–12. Left, a GREY card "the lecture's wish" (a friendly RED bell, tag
   `illustration`): Build failed · Failed step · Tests: failing / passing · Lint: errors / warnings
   · Duration. Right, a GREY chat window '#build-alerts' captioned "what this workflow sends" (tag
   `illustration`), re-drawn from ci.yml:207–252: "Build failed" flies into the ✓ Passed / ✗ Failed
   header (209/215), the tests row into the three per-job marks (243); the fields (219–236) and the
   two links (250) fade in as named; the three other wishes dim with a dashed "not sent" chip.
3. LECTURE off. A schematic Settings page (BLUE frame, tag `illustration`): breadcrumb "Settings →
   Secrets and variables → Actions → New repository secret", Name `SLACK_WEBHOOK_URL`, Secret
   `https://hooks.slack.com/services/<your-webhook-path>` (placeholder, GREY). A struck GREY tab
   "Settings → Webhooks", RED ✗ "not here". The value drops into a BLUE vault; "in logs: ***"; a RED
   chip "never in the repository" and a GREY chip "PRs from forks: no secrets".
4. CODE(.github/workflows/ci.yml: 194–205): 197 YELLOW, 198 and 200 PINK, 204 YELLOW. Then
   CODE(history/199abd9-to-1a5e363-ci.yml.diff: 9–20) at 20 pt: line 19 RED, 9–16 and 20 GREEN.
5. LOG(run1/test-summary/02: 1–5 as heading) (title "Test Summary › Check if Slack webhook is
   configured"): `""` YELLOW; a PINK `enabled=false` note. The log folds to its first row and
   STEPS(run1/test-summary: 2–5) comes in under it: "Send Slack notification" ⊘ with its chip.
6. STEPS(run-demo/test-summary: 2–5), V6 on the rows: row 1 shuts RED (chip "1"), row 2 greys
   out (dashed chip "no if: always()"), row 3 reads `enabled: ''` → `'' == 'true'` → false. The
   GREY chat window '#build-alerts' stays silent; its RED bell gets a slash.
7. CODE(.github/workflows/ci.yml: 194–195) with a GREEN fix overlay `+ if: always()` (GREY chip
   "exercises.md · hardened with env:"); row 2's dashed chip turns GREEN `if: always()`, the
   bell loses its slash and rings ✗ "CI Pipeline Failed" into the chat window. Fade; empty frame.

Deviations from SHOW: arrow 1's picture dims in place (SlackRoute.ghost_outward) instead of
shrinking above the bottom band: the piece's layout already puts it above. The outward arrows are
drawn here, one per spoken phrase (SlackRoute.outward plays all three at once; its targets are
added to the piece so ghost_outward dims them). The run-1 log is shown in full, then folds to its
first row so the step list fits under it. In beat 7 the step list's marks are not changed (they are
the demo run's real states): the fix is drawn as the GREEN chip on the row and the bell ringing,
tagged "with the fix".
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S14"]

# ------------------------------------------------------------------ the real sources (checked)
CI = source_text(".github/workflows/ci.yml").split("\n")
assert CI[194 - 1].strip() == "- name: Check if Slack webhook is configured", CI[193]
assert CI[195 - 1].strip() == "id: slack-check", CI[194]
assert 'if [ -n "${{ secrets.SLACK_WEBHOOK_URL }}" ]; then' in CI[197 - 1], CI[196]
assert 'echo "enabled=true" >> $GITHUB_OUTPUT' in CI[198 - 1] and 'echo "enabled=false"' in CI[200 - 1]
assert CI[204 - 1].strip() == "if: always() && steps.slack-check.outputs.enabled == 'true'", CI[203]
assert "✅ CI Pipeline Passed" in CI[209 - 1] and "❌ CI Pipeline Failed" in CI[215 - 1]
assert all(k in "".join(CI[222:236]) for k in ("*Repository:*", "*Branch:*", "*Commit:*", "*Author:*"))
assert all(k in CI[243 - 1] for k in ("Unit Tests:", "Integration Tests:", "System Tests:", "✅ Passed", "❌ Failed"))
assert "View Commit" in CI[250 - 1] and "View Workflow Run" in CI[250 - 1]
DIFF = source_text("history/199abd9-to-1a5e363-ci.yml.diff").split("\n")
assert DIFF[19 - 1].strip() == "-        if: always() && secrets.SLACK_WEBHOOK_URL != ''".strip(), DIFF[18]
assert DIFF[20 - 1].startswith("+") and all(DIFF[n - 1].startswith("+") for n in range(9, 17)), DIFF[8:20]
C02 = capture("run1/test-summary/02")
assert C02.k == 5 and C02.exit == 0 and not C02.lines, (C02.k, C02.lines)
assert C02.raw[0] == '$ if [ -n "" ]; then' and 'echo "enabled=false"' in C02.raw[3], C02.raw
assert C02.step_name == "Check if Slack webhook is configured", C02.step_name
S1 = {s.num: s for s in steps("run1", "test-summary")}
assert S1[1].state == "success" and S1[2].state == "success" and S1[3].state == "skipped", S1
assert S1[3].note == "steps.slack-check.outputs.enabled is 'false'", S1[3].note
SD = {s.num: s for s in steps("run-demo", "test-summary")}
assert SD[1].state == "failure" and SD[2].state == "skipped" and SD[3].state == "skipped", SD
assert SD[3].note == "steps.slack-check.outputs.enabled is ''", SD[3].note
assert capture("run-demo/test-summary/01").exit == 1
assert WEBHOOK_PH == "https://hooks.slack.com/services/<your-webhook-path>" and MASKED == "***"

# ------------------------------------------------------------------ layout
TOP = 2.05                       # Part 2 pictures stay below PIC_TOP2 (2.15)
LOW = -3.5


def heading_log(cap, rows=None, colors=None, title=None) -> VGroup:
    """LOG(…: 1–k as heading): a job-log panel (run_log's look) whose body is the capture's
    command rows in GREY mono 20 (a run: script with no output). rows: indices into the command
    rows to show (None: all); '…' items allowed. .frame .title .rows .badge .tag"""
    colors = colors or {}
    src = cap.raw[:cap.k]
    pick = list(range(len(src))) if rows is None else rows
    lines = VGroup()
    for i in pick:
        if isinstance(i, str):
            lines.add(mono_line(i, 20, S.GREY))
        else:
            lines.add(mono_line(src[i], 20, colors.get(i, S.GREY)))
    pitch = line_pitch(20)
    for i, r in enumerate(lines):
        r.shift(-r.strut.get_corner(UL) + DOWN * i * pitch)
    tt = label(title or f"{JOB_NAME[cap.job]} › {cap.step_name}", 22, INK)
    bd = exit_badge(cap.exit)
    w = max(lines.width + 0.8, tt.width + bd.width + 1.2)
    bar_h = 0.52
    h = bar_h + lines.height + 0.5
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.14, stroke_color=S.GREY_DARK,
                          stroke_width=2).set_fill(TERM_BG, 1)
    sep = Line(fr.get_corner(UL) + DOWN * bar_h, fr.get_corner(UR) + DOWN * bar_h, color=S.GREY_DARK,
               stroke_width=2)
    tt.move_to(fr.get_top() + DOWN * bar_h / 2).align_to(fr, LEFT).shift(RIGHT * 0.3)
    lines.next_to(sep, DOWN, buff=0.22).align_to(fr, LEFT).shift(RIGHT * 0.3)
    bd.move_to(fr.get_corner(UR) + np.array([-0.35 - bd.width / 2, 0, 0]))
    tg = standin_tag().move_to(fr.get_corner(DR) + np.array([-0.3, 0, 0]))
    tg.shift(LEFT * tg.width / 2)
    g = VGroup(fr, sep, tt, lines, bd, tg)
    g.frame, g.title, g.rows, g.badge, g.tag = fr, tt, lines, bd, tg
    return g


def mark_row(text: str, size: float = 20, color=INK) -> VGroup:
    """'Unit Tests:' then a GREEN ✓ / a RED ✗ (the payload's ✅ Passed || ❌ Failed)."""
    t = label(text, size, color)
    ok = check_mark(0.22, PASS, stroke=3.5)
    sl = label("/", size, S.GREY)
    no = cross_mark(0.2, ERR, stroke=3.5)
    return VGroup(t, ok, sl, no).arrange(RIGHT, buff=0.14)


def wish_card() -> VGroup:
    """Slide 11 re-drawn as the lecture's wish list (no names). .frame .head .bell .rows"""
    hd = label("the lecture's wish", 22, S.GREY)
    bell = bell_glyph(0.5, ERR)
    head = VGroup(hd, bell).arrange(RIGHT, buff=0.3)
    r0 = VGroup(cross_mark(0.22, ERR, stroke=3.5), label("Build failed", 22, INK)).arrange(RIGHT, buff=0.18)
    rows = VGroup(r0, label("Failed step", 22, INK), label("Tests: failing / passing", 22, INK),
                  label("Lint: errors / warnings", 22, INK), label("Duration", 22, INK))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
    fr = box(5.6, body.height + 0.8, S.GREY, fill=S.GREY_DARKER, fill_opacity=1, radius=0.16)
    body.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.4)
    g = VGroup(fr, body)
    g.frame, g.head, g.bell, g.rows = fr, hd, bell, rows
    return g


class SlackBell(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S14"] == 8, len(SAY)

        # ========================================================== 0. slides 7, 9: GitHub calls out
        tr = tracker_p5(8, True)
        strip = pipeline_strip("Summary")
        ref = lref("7, 9")
        sr = SlackRoute()                     # absolute layout (see its docstring); not shifted
        names = ("external CI (Jenkins)", "deploy server", "chat")
        ys = (1.65, 1.05, 0.45)
        cues = ("to start an outside CI system", "to deploy", "or to post to a chat")
        hook = label("webhook", 22, ROUTE).next_to(sr.github, UP, buff=0.12).align_to(sr.github, LEFT)
        assert hook.get_top()[1] < 2.15, hook.get_top()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(strip, shift=RIGHT * 0.3), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(sr.github, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(sr.github.text, color=GITHUB, scale_factor=1.1), run_time=0.6)
            vo.wait_until("A webhook is GitHub calling")
            self.play(FadeIn(hook, shift=DOWN * 0.1), run_time=0.5)
            sr.keep(self, hook)
            vo.wait_until("when something happens")
            sp = spark(ROUTE).move_to(sr.github.frame.get_right() + RIGHT * 0.3)
            self.play(Indicate(sr.github, color=ROUTE, scale_factor=1.06), FadeIn(sp, scale=0.5), run_time=0.6)
            self.play(FadeOut(sp, scale=1.6), run_time=0.4)
            self.remove(sp)
            for i, (name, y, cue) in enumerate(zip(names, ys, cues)):
                vo.wait_until(cue)
                c = grey_chip(name, size=22).move_to([3.6, y, 0])
                ar = route(sr.github.frame.get_right(), c.get_left() + LEFT * 0.05)
                parts = [GrowArrow(ar), FadeIn(c, shift=LEFT * 0.2)]
                grp = VGroup(ar)
                if i == 0:
                    pt = label("POST", 20, ROUTE).move_to(ar.point_from_proportion(0.55) + UP * 0.28)
                    parts.append(FadeIn(pt))
                    grp.add(pt)
                self.play(*parts, run_time=0.6)
                sr.targets.add(c)
                sr.out_arrows.add(grp)
                sr.keep(self, c, *grp)
            sr.top = VGroup(sr.github, hook, sr.targets, sr.out_arrows)
            self.play(LaggedStart(*[Indicate(a[0], color=ROUTE, scale_factor=1.0) for a in sr.out_arrows],
                                  lag_ratio=0.25), run_time=0.9)

        # ========================================================== 1. the other direction: Slack's incoming webhook
        opt = grey_chip("optional · your own Slack workspace · Slack app → Incoming Webhooks → Add New Webhook",
                        size=20).move_to([0, -3.05, 0])
        assert opt.width < 13.0 and opt.get_top()[1] < -2.55, (opt.width, opt.get_top())
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(ref), FadeIn(opt, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("And this webhook works the other way round")
            sr.ghost_outward(self)
            vo.wait_until("Slack gives you an incoming webhook")
            sr.inward(self)
            self.play(Circumscribe(sr.slot, color=ROUTE, buff=0.06), Indicate(sr.slot[1], color=ROUTE),
                      run_time=0.8)
            vo.wait_until("and the last steps of the test summary job")
            self.play(Indicate(sr.runner.steps, color=GITHUB, scale_factor=1.06), run_time=0.7)
            self.play(Indicate(sr.in_arrow, color=ROUTE, scale_factor=1.05), run_time=0.6)
            vo.wait_until("GitHub doesn't ring this bell")
            self.play(Wiggle(sr.github, scale_value=1.05, rotation_angle=0.03 * TAU), run_time=0.8)
            vo.wait_until("your workflow does")
            self.play(Indicate(sr.runner.steps[1], color=TURN, scale_factor=1.08),
                      Indicate(sr.bell, color=TURN, scale_factor=1.2), run_time=0.8)

        # ========================================================== 2. slides 10–12: the wish vs the payload
        ref2 = lref("10–12")
        wc = wish_card()
        wc.move_to([-6.45 + wc.width / 2, TOP - 0.05 - wc.height / 2, 0])
        wtag = illustration_tag().next_to(wc, DOWN, buff=0.15).align_to(wc, LEFT)
        chat = chat_window(CHANNEL, (), 6.2, 4.25)
        chat.move_to([6.45 - chat.width / 2, TOP - 0.05 - chat.height / 2, 0])
        ccap = VGroup(label("what this workflow sends", 20, S.GREY), illustration_tag()).arrange(RIGHT, buff=0.3)
        ccap.next_to(chat, DOWN, buff=0.15).align_to(chat, RIGHT)
        hdr = VGroup(check_mark(0.24, PASS, stroke=3.5), label("CI Pipeline Passed", 20, INK), label("/", 20, S.GREY),
                     cross_mark(0.22, ERR, stroke=3.5), label("CI Pipeline Failed", 20, INK)).arrange(RIGHT, buff=0.14)
        fields = label("Repository · Branch · Commit · Author", 20, INK)
        tres = label("Test Results:", 20, S.GREY)
        tests = VGroup(mark_row("Unit Tests:"), mark_row("Integration Tests:"), mark_row("System Tests:"))
        tests.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        links = label("View Commit  |  View Workflow Run", 20, GITHUB)
        payload = VGroup(hdr, fields, tres, tests, links).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        payload.next_to(chat.title, DOWN, buff=0.38).align_to(chat.title, LEFT)
        assert payload.get_bottom()[1] > chat.frame.get_bottom()[1] + 0.1, payload.get_bottom()
        assert payload.get_right()[0] < chat.frame.get_right()[0] - 0.1, payload.get_right()
        assert wc.get_right()[0] < chat.get_left()[0] - 0.2, (wc.get_right(), chat.get_left())
        assert ccap.get_bottom()[1] > -3.55 and wtag.get_bottom()[1] > -3.55, ccap.get_bottom()
        notsent = dashed_chip("not sent").next_to(wc.rows[3], RIGHT, buff=0.35)
        notsent.align_to(wc.frame, RIGHT).shift(LEFT * 0.25)
        assert notsent.get_left()[0] > wc.rows[3].get_right()[0] + 0.1, notsent.get_left()
        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(sr, opt)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            vo.wait_until("The lecture imagines")
            self.play(FadeIn(ref2), FadeIn(wc.frame), FadeIn(wc.head), FadeIn(wc.bell), FadeIn(wtag), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in wc.rows[:1]], lag_ratio=0.2), run_time=0.4)
            vo.wait_until("failures included")
            w = ring_waves(wc.bell, ERR)
            self.play(Indicate(wc.rows[0], color=ERR, scale_factor=1.06),
                      LaggedStart(*[Create(a) for a in w], lag_ratio=0.2), run_time=0.7)
            vo.wait_until("with the failed step")
            self.play(FadeIn(wc.rows[1], shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("counts and duration")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in wc.rows[2:]], lag_ratio=0.3),
                      run_time=0.9)
            vo.wait_until("This workflow sends less")
            self.play(FadeOut(w), FadeIn(chat, shift=LEFT * 0.2), FadeIn(ccap), run_time=0.6)
            self.remove(w)
            vo.wait_until("passed or failed")
            self.play(ReplacementTransform(wc.rows[0].copy(), hdr), run_time=0.8)
            vo.wait_until("the repository, branch, commit and author")
            self.play(FadeIn(fields, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(fields, color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("one mark per test job")
            self.play(FadeIn(tres), ReplacementTransform(wc.rows[2].copy(), tests), run_time=0.8)
            dim = VGroup(wc.rows[1], wc.rows[3], wc.rows[4])
            self.play(dim.animate.set_opacity(0.35), FadeIn(notsent, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and two links")
            self.play(FadeIn(links, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(links, color=GITHUB, scale_factor=1.06), run_time=0.6)

        # ========================================================== 3. the secret: Settings, not Webhooks
        crumb = "Settings → Secrets and variables → Actions → New repository secret"
        pg = gh_page(crumb, 9.75, 3.25)
        pg.move_to([-6.45 + pg.width / 2, TOP - 0.05 - pg.height / 2, 0])
        f_name = field_row("Name", SECRET_NAME)
        f_val = field_row("Secret", WEBHOOK_PH, value_color=S.GREY)
        form = VGroup(f_name, f_val).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        form.move_to(pg.body).align_to(pg.body, LEFT).align_to(pg.body, UP).shift(DOWN * 0.08)
        ptag = illustration_tag().move_to(pg.frame.get_corner(DR) + LEFT * 0.3)
        ptag.shift(LEFT * ptag.width / 2)
        assert form.get_bottom()[1] > pg.frame.get_bottom()[1] + 0.2, form.get_bottom()
        assert form.get_right()[0] < pg.frame.get_right()[0] - 0.1, form.get_right()
        vault = vault_glyph(1.2).move_to([4.95, 1.0, 0])
        assert vault.get_left()[0] > pg.get_right()[0] + 0.3, vault.get_left()
        vname = mono(SECRET_NAME, 20, GITHUB).next_to(vault, DOWN, buff=0.2)
        logs = VGroup(label("in logs:", 20, S.GREY), mono(MASKED, 24, INK)).arrange(RIGHT, buff=0.2)
        logs.next_to(vname, DOWN, buff=0.4)
        assert vname.get_right()[0] < 6.55 and vname.get_left()[0] > pg.get_right()[0] + 0.1, vname.get_left()
        wh_t = label("Settings → Webhooks", 22, S.GREY)
        wh = VGroup(box(wh_t.width + 0.5, 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1), wh_t)
        wh_t.move_to(wh[0])
        nothere = VGroup(cross_mark(0.26, ERR, stroke=4), label("not here", 22, ERR)).arrange(RIGHT, buff=0.15)
        whrow = VGroup(wh, nothere).arrange(RIGHT, buff=0.35)
        whrow.move_to([-6.45 + whrow.width / 2, -1.95, 0])
        wh_x = strike(wh[0])
        never = err_chip("never in the repository", size=22)
        forks = grey_chip("PRs from forks: no secrets", size=22)
        chips3 = VGroup(never, forks).arrange(RIGHT, buff=0.5).move_to([0, -3.0, 0])
        assert whrow.get_top()[1] < pg.get_bottom()[1] - 0.2, whrow.get_top()
        assert logs.get_left()[0] > whrow.get_right()[0] + 0.3 or logs.get_bottom()[1] > whrow.get_top()[1] + 0.1
        assert logs.get_bottom()[1] > chips3.get_top()[1] + 0.15, logs.get_bottom()
        with self.voiceover(SAY[3]) as vo:
            gone = VGroup(wc, wtag, chat, ccap, hdr, fields, tres, tests, links, notsent)
            self.play(FadeOut(gone), FadeOut(ref2), run_time=0.5)
            self.remove(gone, ref2, *gone.get_family())
            vo.wait_until("The webhook address is a secret")
            self.play(FadeIn(pg.frame), FadeIn(pg[2]), FadeIn(ptag), run_time=0.5)
            vo.wait_until("Add it under Settings")
            self.play(FadeIn(pg.crumb, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(pg.crumb, color=GITHUB, scale_factor=1.04), run_time=0.8)
            vo.wait_until("as a new repository secret")
            self.play(FadeIn(f_name, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(f_val, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("not under Webhooks")
            self.play(FadeIn(wh, shift=UP * 0.1), run_time=0.4)
            self.play(Create(wh_x), FadeIn(nothere, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("It never goes in the repository")
            self.play(FadeIn(vault, shift=LEFT * 0.2), run_time=0.4)
            drop = f_val.value.copy()
            self.play(drop.animate.scale(0.2).move_to(vault).set_opacity(0), FadeIn(vname, shift=UP * 0.1),
                      run_time=0.9)
            self.remove(drop)
            self.play(Indicate(vault, color=GITHUB, scale_factor=1.12), FadeIn(never, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("logs show it as three stars")
            self.play(FadeIn(logs, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(logs[1], color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("and pull requests from forks")
            self.play(FadeIn(forks, shift=UP * 0.15), run_time=0.5)

        # ========================================================== 4. the check step, and the repo's own history
        p4 = code(".github/workflows/ci.yml", 194, 205)
        p4.move_to([0, TOP - p4.height / 2, 0])
        assert p4.get_bottom()[1] > -3.55, p4.get_bottom()
        p4b = code("history/199abd9-to-1a5e363-ci.yml.diff", 9, 20, font_size=20)
        p4b.move_to([0, TOP - p4b.height / 2, 0])
        with self.voiceover(SAY[4]) as vo:
            gone = VGroup(pg, form, ptag, vault, vname, logs, wh, wh_x, nothere, never, forks)
            self.play(FadeOut(gone), run_time=0.5)
            self.remove(gone, *gone.get_family())
            self.play(FadeIn(p4, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("The check step tests")
            b197 = line_bar(p4.code, 3, TURN)
            self.play(FadeIn(b197), Indicate(code_span(p4.code, 3, "secrets.SLACK_WEBHOOK_URL"), color=TURN,
                                             scale_factor=1.06), run_time=0.7)
            vo.wait_until("and writes enabled")
            b198, b200 = line_bar(p4.code, 4, ROUTE), line_bar(p4.code, 6, ROUTE)
            self.play(FadeIn(b198), FadeIn(b200), run_time=0.5)
            self.play(Indicate(code_span(p4.code, 4, "enabled=true"), color=ROUTE, scale_factor=1.1),
                      Indicate(code_span(p4.code, 6, "enabled=false"), color=ROUTE, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Why not test the secret")
            b204 = line_bar(p4.code, 10, TURN)
            self.play(FadeIn(b204), Indicate(code_span(p4.code, 10, "steps.slack-check.outputs.enabled"),
                                             color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("the repository's own history tried it")
            self.play(FadeOut(VGroup(b197, b198, b200, b204)), run_time=0.3)
            self.play(ReplacementTransform(p4, p4b), run_time=0.8)
            b19 = line_bar(p4b.code, 10, ERR, opacity=0.22)
            self.play(FadeIn(b19), Indicate(code_span(p4b.code, 10, "secrets.SLACK_WEBHOOK_URL != ''"), color=ERR,
                                            scale_factor=1.06), run_time=0.7)
            vo.wait_until("and replaced it with this shell check")
            greens = VGroup(*[line_bar(p4b.code, k, PASS, opacity=0.18) for k in (*range(0, 8), 11)])
            self.play(LaggedStart(*[FadeIn(b) for b in greens], lag_ratio=0.08), run_time=0.9)

        # ========================================================== 5. run 1: no secret, enabled=false, skipped
        lg = heading_log(C02, colors={})
        lg.move_to([-6.45 + lg.width / 2, TOP - lg.height / 2, 0])
        q = substring(lg.rows[0], '""')
        en = route_chip("enabled=false").next_to(lg.rows[3], RIGHT, buff=0.3)
        en.shift(RIGHT * (lg.frame.get_right()[0] + 0.35 - en.get_left()[0]))
        assert en.get_right()[0] < 6.5, en.get_right()
        lg5 = heading_log(C02, rows=[0])
        lg5.move_to([-6.45 + lg5.width / 2, TOP - lg5.height / 2, 0])
        en5 = route_chip("enabled=false").next_to(lg5.frame, RIGHT, buff=0.35)
        st1 = steps_list("run1", "test-summary", ((2, 5),))
        st1.move_to([0, LOW + st1.height / 2, 0])
        assert st1.get_top()[1] < lg5.get_bottom()[1] - 0.15, (st1.get_top(), lg5.get_bottom())
        assert lg.get_bottom()[1] > -3.55, lg.get_bottom()
        with self.voiceover(SAY[5]) as vo:
            gone = VGroup(p4b, b19, greens)
            self.play(FadeOut(gone), run_time=0.4)
            self.remove(gone, *gone.get_family())
            vo.wait_until("In run 1 there's no secret")
            self.play(FadeIn(lg, shift=UP * 0.15), run_time=0.5)
            self.play(q.animate.set_color(TURN), Circumscribe(q, color=TURN, buff=0.06), run_time=0.7)
            vo.wait_until("so enabled is false")
            self.play(FadeIn(en, shift=LEFT * 0.15), lg.rows[3].animate.set_color(ROUTE), run_time=0.5)
            vo.wait_until("and the Slack step is skipped")
            lg5.rows[0].set_color(S.GREY)
            substring(lg5.rows[0], '""').set_color(TURN)
            self.play(ReplacementTransform(lg, lg5), ReplacementTransform(en, en5), run_time=0.6)
            self.play(FadeIn(st1, shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(st1.row(4), color=S.GREY, scale_factor=1.04),
                      Circumscribe(st1.notes[4], color=ROUTE, buff=0.05), run_time=0.8)

        # ========================================================== 6. the demo run: the bell can't ring
        sd = steps_list("run-demo", "test-summary", ((2, 5),))
        sd.move_to([-6.45 + sd.width / 2, TOP - sd.height / 2, 0])
        c1 = sd.code_chip(2, 1)
        noalw = dashed_chip("no if: always()", mono_font=True).next_to(sd.row(3), RIGHT, buff=0.35)
        assert noalw.get_right()[0] < sd.frame.get_right()[0] - 0.1, noalw.get_right()
        band_top = sd.get_bottom()[1] - 0.2
        cw = chat_window(CHANNEL, (), 3.7, 1.85)
        cw.move_to([-6.45 + cw.width / 2, LOW + cw.height / 2, 0])
        assert cw.get_top()[1] < band_top, (cw.get_top(), band_top)
        bell = bell_glyph(0.55, ERR).move_to(cw.frame.get_corner(DR) + np.array([-1.0, 0.5, 0]))
        assert ring_waves(bell).get_right()[0] < cw.frame.get_right()[0] - 0.12, ring_waves(bell).get_right()
        bell_x = bell_glyph(0.55, ERR, slashed=True).move_to(bell)
        enE = route_chip("enabled: ''")
        cond = VGroup(mono("'' == 'true'", 22, INK), label("→", 22, S.GREY), label("false", 22, ERR)).arrange(RIGHT, buff=0.2)
        crow = VGroup(enE, cond).arrange(RIGHT, buff=0.6)
        crow.move_to([(cw.get_right()[0] + 6.45) / 2, cw.get_center()[1] + 0.2, 0])
        assert crow.get_left()[0] > cw.get_right()[0] + 0.3, crow.get_left()
        with self.voiceover(SAY[6]) as vo:
            vo.wait_until("Now the demo run")
            self.play(FadeOut(VGroup(lg5, en5)), run_time=0.4)
            self.remove(lg5, en5, *lg5.get_family())
            self.play(ReplacementTransform(st1, sd), run_time=0.8)
            self.play(FadeIn(cw, shift=UP * 0.15), FadeIn(bell), run_time=0.4)
            vo.wait_until("Check test results fails")
            self.play(FadeIn(c1, shift=LEFT * 0.1), Circumscribe(sd.row(2), color=ERR, buff=0.06), run_time=0.7)
            vo.wait_until("The check step has no if always")
            self.play(FadeIn(noalw, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("so it's skipped too")
            self.play(Indicate(sd.row(3), color=S.GREY, scale_factor=1.05), run_time=0.6)
            vo.wait_until("enabled stays empty")
            self.play(FadeIn(enE, shift=UP * 0.1), Circumscribe(sd.notes[4], color=ROUTE, buff=0.05), run_time=0.7)
            vo.wait_until("and the Slack step's condition is false")
            self.play(FadeIn(cond, shift=LEFT * 0.1), run_time=0.5)
            self.play(Transform(bell, bell_x), cw.title.animate.set_opacity(0.4), run_time=0.6)

        # ========================================================== 7. the fix: if: always() on the check step
        p7 = code(".github/workflows/ci.yml", 194, 195, font_size=20)
        p7.move_to([cw.get_right()[0] + 0.25 + p7.width / 2, LOW + 0.05 + p7.height / 2, 0])
        assert p7.get_left()[0] > cw.get_right()[0] + 0.15 and p7.get_top()[1] < band_top, (p7.get_left(), p7.get_top())
        fix = ok_chip("+ if: always()", mono_font=True)
        fix.next_to(p7.header, RIGHT, buff=0.22).shift(UP * 0.05)
        assert fix.get_right()[0] < 6.5, fix.get_right()
        assert fix.get_bottom()[1] > p7.code.get_top()[1] - 0.02 and fix.get_top()[1] < band_top, fix.get_bottom()
        fix_g = ok_chip("if: always()", mono_font=True).move_to(noalw).align_to(noalw, LEFT)
        ex = grey_chip("exercises.md · hardened with env:").next_to(sd.head, RIGHT, buff=0.6)
        ex.align_to(sd.frame, RIGHT).shift(LEFT * 0.3)
        assert ex.get_left()[0] > sd.head.get_right()[0] + 0.2, ex.get_left()
        with_fix = tag("with the fix", S.GREY).next_to(cw.frame.get_corner(DL), UR, buff=0.15)
        assert with_fix.get_right()[0] < bell.get_left()[0] - 0.15, with_fix.get_right()
        bell_r = bell_glyph(0.55, ERR).move_to(bell)
        with self.voiceover(SAY[7]) as vo:
            vo.wait_until("As written")
            self.play(Wiggle(bell, scale_value=1.15), Indicate(c1, color=ERR, scale_factor=1.15), run_time=0.8)
            vo.wait_until("The fix is one line")
            self.play(FadeOut(crow), run_time=0.4)
            self.remove(crow, *crow.get_family())
            self.play(FadeIn(p7, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("if always, on the check step")
            self.play(FadeIn(fix, shift=LEFT * 0.15), Indicate(code_span(p7.code, 1, "slack-check"), color=PASS,
                                                                scale_factor=1.08), run_time=0.6)
            self.play(ReplacementTransform(noalw, fix_g), Circumscribe(sd.row(3), color=PASS, buff=0.06), run_time=0.7)
            self.play(Transform(bell, bell_r), cw.title.animate.set_opacity(1), FadeIn(with_fix), run_time=0.5)
            w7 = ring_waves(bell, ERR)
            card = VGroup(cross_mark(0.24, ERR, stroke=3.5), label("CI Pipeline Failed", 20, INK)).arrange(RIGHT, buff=0.15)
            card.next_to(cw.title, DOWN, buff=0.25).align_to(cw.title, LEFT)
            assert card.get_bottom()[1] > max(bell.get_top()[1], with_fix.get_top()[1]) + 0.03, card.get_bottom()
            self.play(LaggedStart(*[Create(a) for a in w7], lag_ratio=0.2), FadeIn(card, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("The exercises have a hardened version")
            self.play(FadeIn(ex, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(ex, color=INK, scale_factor=1.05), run_time=0.6)
        self.play(FadeOut(VGroup(sd, c1, fix_g, ex, cw, bell, w7, card, with_fix, p7, fix, tr, strip)), run_time=0.8)
        self.wait(0.3)
