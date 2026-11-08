"""S03 · A policy, a user and two keys — tracker A 1 → 5 (README › Before you deploy). No lecture tag
(script.md has no LECTURE mark in this scene). V3 KeyJourney begins here (the ~/secrets/ place, the
badge, then the key).

Beats (script.md "## S03"; one voiceover block each):
0. TRACKER A 1 · extra. Terminal `laptop` (22 pt, 11 rows), prompt student@laptop:~$. `git ls-remote …`
   (extra) → laptop/01: 2–3 (ids cut to 5950118…); `git clone …` (extra) → laptop/02: 2 typed on "the
   README has no clone step" (kept under the ls-remote rows, so "One branch" can point at
   refs/heads/main and 5950118); the terminal clears on "and inside src": `ls -a …` (extra) →
   laptop/04: 12–20, line 17 `deployment` YELLOW + ring on "the deployment folder".
1. TRACKER A 1. The terminal sinks away. README(7–13) card; lines 9–13 inside a GREY dashed box with the
   chip "inside a comment · renders empty". A GREY check card (Bedrock › Model access · us-east-1 ·
   Claude 3 / 3.5 Sonnet and Titan embeddings · api-service/api/utils) and under it the GREY dashed chip
   "model IDs from 2024 · may be retired: not checked".
2. TRACKER A 2. CODE(README.md: 22–33): line 29 YELLOW, lines 30–33 PURPLE; Transform to CODE(README.md:
   34–44): lines 34–38 PURPLE, line 40 ORANGE.
3. TRACKER A 2 (· extra while the strip's command is on screen). The panel shrinks into a GREY chip at
   the left; CONSOLE "IAM › Policies › Create policy" (JSON pasted, Name CheeseAppECRPolicy) at the
   right; ▶ your turn. A 5-row laptop strip types `sed -n '23,43p' … | python3 -m json.tool` (extra) →
   laptop/10: 2, …, 22; a GREEN ✓ beside the closing brace. A RED dashed chip "no ecr:CreateRepository
   → S07" slides in under the shrunken panel.
4. TRACKER A 3. The policy page becomes CONSOLE "IAM › Users › Create user" (user name, "Attach
   policies directly"); ▶ your turn; three ORANGE managed-policy chips drop in one per word, then the
   GREEN CheeseAppECRPolicy chip (README 48–50).
5. TRACKER A 4. CONSOLE "IAM › deployment-ac215-user › Create access key" (Third Party Service, the
   placeholder key, [Download .csv file]); ▶ your turn. V3 begins: the GREY ~/secrets/ place; the WHITE
   badge pops out of the download button into it, and a GREY CSV card (the placeholder row, folded after
   its comma) appears under it. The console goes; the place and the card move up; a 7-row laptop strip
   types `ls ~; ls -l ~/secrets` → laptop/12: 2–3, 5–6 (wrapped; the .pem rows GREY until beat 6);
   `cheese-app-aws` and `secrets` flash; the CSV name YELLOW + row tag "keep AWS's file name ·
   docker-shell.sh:10".
6. TRACKER A 5. The strip shrinks to its four .csv/.pem rows; CONSOLE "EC2 › Key Pairs › Create key pair"
   (Name cheese-app-ac215-key-pair, [Download .pem]); ▶ your turn + YELLOW chip under it "wait: name
   it ac215_2024 · see next" (QA: the viewer pauses here, before beat 7's erratum); the WHITE key drops into ~/secrets/
   beside the badge; the strip's .pem rows turn YELLOW + row tag "a throwaway key stands in here". The
   console goes; the place moves to the middle; PINK arrows: badge → BLUE "AWS API", key → BLUE "SSH door
   · your server", each on its clause.
7. TRACKER A 5 · extra. Full terminal (20 pt, 14 rows): `cd cheese-app-aws && grep -rn …` (extra) →
   laptop/13: 2 (wrapped; cheese-app-ac215-key-pair ORANGE), then 5–9 (6 and 9 cut after the .pem path) and
   `…`, every ac215_2024 YELLOW. On "Easiest fix" the terminal keeps its last 9 rows and the erratum
   card appears above it.
8. TRACKER A 5 · extra. The card goes; the prompt is now student@laptop:~/cheese-app-aws$ (the cd of
   beat 7); `chmod 400 … && ls -l ~/secrets` (extra) → laptop/14: 2–4 (wrapped); a GREY ring and the
   chip "our stand-in kept the README's name · yours: ac215_2024.pem"; `-r--------` GREEN on "S S H
   refuses". Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ the real sources (checked)
C01, C02, C04 = capture("01"), capture("02"), capture("04")
assert C01.cmd == f"git ls-remote {COURSE_URL}", C01.cmd
assert C02.cmd == f"git clone {COURSE_URL}", C02.cmd
assert C04.cmd == "ls -a cheese-app-aws cheese-app-aws/src cheese-app-aws/src/deployment", C04.cmd
assert C01.at(3)[0].startswith(PIN + "…") and C01.at(3)[0].endswith("refs/heads/main")
assert C04.line(17) == "deployment"
C10, C12, C13, C14 = capture("10"), capture("12"), capture("13"), capture("14")
assert C10.cmd == "sed -n '23,43p' cheese-app-aws/README.md | python3 -m json.tool", C10.cmd
assert C10.line(2) == "{" and C10.line(22) == "}" and C10.exit == 0
assert C12.cmd == "ls ~; ls -l ~/secrets", C12.cmd
assert C12.line(5).endswith(PEM_README) and C12.line(6).endswith(CSV_NAME)
assert C13.cmd.startswith("cd cheese-app-aws && grep -rn"), C13.cmd
assert "src/deployment/inventory.yml:16:" in C13.line(7) and "docker-shell.sh:27:" in C13.line(8)
assert C14.cmd == f"chmod 400 ~/secrets/{PEM_README} && ls -l ~/secrets", C14.cmd
assert C14.line(3).startswith("-r-------- ") and C14.line(3).endswith(PEM_README)
assert readme(46).startswith('Click on "Review Policy" -> Name: CheeseAppECRPolicy')
assert all(p in readme(48) for p in MANAGED_POLICIES) and IAM_USER in readme(48)
assert "Third Party Service" in readme(52) and "Download .csv file" in readme(52)
assert f"Key Pair Name: {KEYPAIR_README}" in readme(64)
assert 'CSV_FILE="../../../../secrets/deployment-ac215-user_accessKeys.csv"' == excerpt(
    "src/deployment/docker-shell.sh", 10, 10)

T20 = 20          # beats 7-8: 72 characters a row (the grep lines)


# ------------------------------------------------------------------ helpers of this scene
def recolor(glyphs, color):
    """ANIMs, glyph by glyph (never animate a substring group itself: split trap)."""
    return [g.animate.set_color(color) for g in glyphs]


def all_of(row, sub):
    """Glyph groups of every occurrence of `sub` in terminal row `row`."""
    res, n = [], row.text.count(sub)
    for i in range(n):
        res.append(substring(row, sub, i))
    return res


def edge_tag(frame, tg, side=DOWN, dx: float = 0.25):
    """A tag sitting on a console frame's bottom (or top) edge, right end."""
    y = frame.get_bottom()[1] if side is DOWN else frame.get_top()[1]
    return tg.move_to([frame.get_right()[0] - dx - tg.width / 2, y, 0])


def at_top_right(m, right: float = 6.5, top: float = 2.75):
    return m.move_to([right - m.width / 2, top - m.height / 2, 0])


def at_top_left(m, left: float = -6.5, top: float = 2.75):
    return m.move_to([left + m.width / 2, top - m.height / 2, 0])


def csv_card():
    """The GREY CSV card: AWS's file holds one header and one row; on screen only the placeholders,
    the row folded after its comma."""
    rows = VGroup(mono(KEY_ID + ",", 20, INK), mono(SECRET_KEY, 20, INK)).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.12)
    fr = box(rows.width + 0.5, rows.height + 0.4, LAPTOP, fill_opacity=0.08)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


class ConsoleSetup(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 9, len(SAY)

        # ========================================================== 0. clone the repo (extras)
        tr = tracker_a(1, True)
        t = term(P_HOME, rows=11)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            ln1 = type_cmd(self, t, C01.cmd, type_time=0.6)
            pin(self, ln1, beside(extra_row(), ln1))
            o1 = out(self, t, C01.at(2, 3), run_time=0.4)
            vo.wait_until("the README has no clone step")
            ln2 = type_cmd(self, t, C02.cmd, type_time=0.6)
            pin(self, ln2, beside(extra_row(), ln2))
            out(self, t, C02.at(2), run_time=0.3)
            vo.wait_until("One branch")
            main = substring(o1[1], "refs/heads/main")
            self.play(*recolor(main, TURN), run_time=0.4)
            self.play(Indicate(main, color=TURN, scale_factor=1.08), run_time=0.6)
            self.add(t)
            vo.wait_until("unchanged since we pinned it")
            pins = [substring(o1[0], PIN), substring(o1[1], PIN)]
            self.play(*recolor(pins[0], OWN), *recolor(pins[1], OWN), run_time=0.4)
            pinned = beside(row_tag(f"{PIN} · the commit we follow", OWN), o1[1], buff=0.5)
            pin(self, o1[1], pinned)
            vo.wait_until("and inside src")
            t.clear(self)
            ln3 = type_cmd(self, t, C04.cmd, type_time=0.6)
            pin(self, ln3, beside(extra_row(), ln3))
            rows = out(self, t, C04.at((12, 20)), run_time=0.6)
            dep = [r for r in rows if r.text == "deployment"][0]
            vo.wait_until("the deployment folder")
            self.play(*recolor(dep.glyphs, TURN), run_time=0.4)
            rg = ring(dep.glyphs, TURN, buff=0.08)
            self.play(Create(rg), run_time=0.4)
            attach(self, dep, rg)

        # ========================================================== 1. APIs to enable: a comment
        rp = readme_panel(7, 13, size=20)
        at_top_left(rp, top=2.7)
        body = VGroup(*[rp.rows[n] for n in (9, 10, 11, 12, 13)])
        head7 = rp.rows[7]
        c_top = (head7.get_bottom()[1] + rp.rows[9].get_top()[1]) / 2
        c_bot = (rp.rows[13].get_bottom()[1] + rp.frame.get_bottom()[1]) / 2
        c_l, c_r = rp.frame.get_left()[0] + 0.12, rp.frame.get_right()[0] - 0.12
        com = outline_box(c_r - c_l, c_top - c_bot, S.GREY, solid=False).move_to([(c_l + c_r) / 2,
                                                                                (c_top + c_bot) / 2, 0])
        com_chip = grey_chip("inside a comment · renders empty")
        com_chip.next_to(rp, DOWN, buff=0.15).align_to(rp, RIGHT)
        chk_rows = VGroup(label("check: Bedrock › Model access · us-east-1", 20, INK),
                          label("the API asks for Claude 3 / 3.5 Sonnet and Titan embeddings", 20, S.GREY),
                          mono("(api-service/api/utils)", 20, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        chk_fr = box(chk_rows.width + 0.5, chk_rows.height + 0.36, S.GREY, fill_opacity=0.06)
        chk_rows.move_to(chk_fr)
        chk = VGroup(chk_fr, chk_rows)
        chk.next_to(com_chip, DOWN, buff=0.18).align_to(rp, LEFT)
        old = dashed_chip("model IDs from 2024 · may be retired: not checked")
        old.next_to(chk, DOWN, buff=0.15).align_to(chk, LEFT)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(t, shift=DOWN * 0.4), track(tr, 1, False), run_time=0.6)
            self.remove(t)
            self.play(FadeIn(rp, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("sits inside a comment")
            self.play(Create(com.frame), run_time=0.7)
            self.play(FadeIn(com_chip, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("on AWS there's nothing to switch on")
            self.play(body.animate.set_opacity(0.45), run_time=0.6)
            vo.wait_until("One check")
            self.play(FadeIn(chk, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("the API calls Bedrock models")
            self.play(Indicate(chk_rows[1], color=INK, scale_factor=1.04), run_time=0.8)
            vo.wait_until("chosen in 2024")
            self.play(FadeIn(old, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("so check your account")
            self.play(Indicate(chk_rows[0], color=TURN, scale_factor=1.05), run_time=0.8)

        # ========================================================== 2. the policy JSON
        p1 = code("README.md", 22, 33)
        p1.move_to([0, 2.75 - p1.height / 2, 0])
        p2 = code("README.md", 34, 44)
        p2.move_to(p1, aligned_edge=UL)
        assert "sts:GetCallerIdentity" in p1.code.source.split("\n")[29 - 22]
        assert '"Resource": "*"' in p2.code.source.split("\n")[40 - 34]
        b29 = line_bar(p1.code, 29 - 22, TURN, 0.25)
        b30 = [line_bar(p1.code, k - 22, TOOL, 0.3) for k in range(30, 34)]
        b34 = [line_bar(p2.code, k - 34, TOOL, 0.3) for k in range(34, 39)]
        b40 = line_bar(p2.code, 40 - 34, SHARED, 0.3)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(rp), FadeOut(com), FadeOut(com_chip), FadeOut(chk), FadeOut(old),
                      track(tr, 2), run_time=0.5)
            self.play(FadeIn(p1, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("create a policy from this JSON")
            self.play(Circumscribe(p1, color=S.GREY, buff=0.06, stroke_width=3), run_time=1.0)
            vo.wait_until("It allows one identity check")
            self.play(FadeIn(b29), run_time=0.4)
            self.play(Indicate(code_span(p1.code, 29 - 22, "sts:GetCallerIdentity"), color=TURN,
                               scale_factor=1.06), run_time=0.7)
            vo.wait_until("and nine E C R actions")
            self.play(LaggedStart(*[FadeIn(b) for b in b30], lag_ratio=0.3), run_time=0.8)
            self.wait(0.4)
            # scroll: lines 22-33 (with their bars) leave upwards as lines 34-44 come up
            self.play(FadeOut(VGroup(p1, b29, *b30), shift=UP * 0.8), FadeIn(p2, shift=UP * 0.8),
                      run_time=0.8)
            self.play(LaggedStart(*[FadeIn(b) for b in b34], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("on any resource")
            self.play(FadeIn(b40), run_time=0.4)
            self.play(Indicate(code_span(p2.code, 40 - 34, '"*"'), color=SHARED, scale_factor=1.3), run_time=0.7)
        self.wait(0.6)

        # ========================================================== 3. create the policy; extra check
        jchip = grey_chip("README.md · lines 22–44 · the policy JSON")
        at_top_left(jchip, top=2.55)
        c3 = console_drawing("IAM › Policies › Create policy", [("JSON", "(pasted)"), ("Name", POLICY)])
        at_top_right(c3)
        turn3 = edge_tag(c3.frame, your_turn())
        nocreate = dashed_chip("no ecr:CreateRepository → the image build", color=ERR)
        nocreate.next_to(jchip, DOWN, buff=0.45).align_to(jchip, LEFT)
        s3 = term(P_HOME, rows=5)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(b34[0], *b34[1:], b40)), run_time=0.3)
            self.play(FadeTransform(p2, jchip), FadeIn(c3, shift=LEFT * 0.2), run_time=0.7)
            self.play(Indicate(c3.rows[1].value, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("and pause to create it")
            self.play(FadeIn(turn3, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("an extra check")
            self.play(FadeIn(s3, shift=UP * 0.2), track(tr, 2, True), run_time=0.5)
            type_cmd(self, s3, C10.cmd, type_time=0.6)
            ex3 = on_bar(s3, extra_row())
            self.play(FadeIn(ex3), run_time=0.3)
            o10 = out(self, s3, C10.at(2, "…", 22), run_time=0.5)
            ok = check_mark(0.32, OWN, stroke=6)
            beside(ok, o10[-1], buff=0.4)
            self.play(Create(ok), run_time=0.4)
            attach(self, o10[-1], ok)
            vo.wait_until("It can't create a repository")
            self.play(FadeIn(nocreate, shift=RIGHT * 0.3), run_time=0.6)
            vo.wait_until("so you'll make three by hand later")
            self.play(Indicate(nocreate.text, color=ERR, scale_factor=1.06), run_time=0.7)

        # ========================================================== 4. the user and four policies
        c4 = console_drawing("IAM › Users › Create user",
                             [("User name", IAM_USER), "Attach policies directly",
                              *[("chip", p, SHARED) for p in MANAGED_POLICIES], ("chip", POLICY, OWN)])
        c4.move_to([1.0, 2.75 - c4.height / 2, 0])
        pols = list(c4.rows[2:])
        for r in pols:
            c4.rows.remove(r)
        turn4 = edge_tag(c4.frame, your_turn())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(s3), FadeOut(ex3), FadeOut(nocreate), FadeOut(jchip), FadeOut(turn3),
                      track(tr, 3), run_time=0.5)
            self.remove(s3, ex3)
            self.play(ReplacementTransform(c3, c4), run_time=0.8)
            self.play(FadeIn(turn4, shift=UP * 0.1), Indicate(c4.rows[0].value, color=TURN, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("It gets three policies")
            self.play(Indicate(c4.rows[1].text, color=INK, scale_factor=1.08), run_time=0.7)
            for p_, w in zip(pols[:3], ("full access to S3", "E C 2", "and Bedrock")):
                vo.wait_until(w)
                self.play(FadeIn(p_, shift=DOWN * 0.35), run_time=0.45)
            vo.wait_until("And your own E C R policy")
            self.play(FadeIn(pols[3], shift=DOWN * 0.35), run_time=0.5)
            self.play(Indicate(pols[3].text, color=OWN, scale_factor=1.08), run_time=0.6)

        # ========================================================== 5. the access key (V3 begins)
        c5 = console_drawing("IAM › deployment-ac215-user › Create access key",
                             [("Use case", "Third Party Service"), ("Access key", KEY_ID),
                              ("button", "Download .csv file")])
        at_top_left(c5)
        turn5 = edge_tag(c5.frame, your_turn())
        kj = KeyJourney(places=("secrets",))
        kj.move_to([3.9, 2.25, 0])
        card = csv_card()
        card.next_to(kj, DOWN, buff=0.35)
        s5 = term(P_HOME, rows=7)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(c4, *pols)), FadeOut(turn4), track(tr, 4), run_time=0.5)
            self.play(FadeIn(c5, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(turn5, shift=UP * 0.1), run_time=0.3)
            vo.wait_until("and download the C S V file")
            btn = c5.rows[2]
            self.play(Indicate(btn.text, color=TURN, scale_factor=1.08), FadeIn(kj, shift=LEFT * 0.2), run_time=0.6)
            badge = badge_glyph(0.3).move_to(btn.box)
            self.play(FadeIn(badge, scale=1.8), run_time=0.4)
            self.play(badge.animate(path_arc=-PI / 3).move_to(kj._slot("secrets", 0)), run_time=0.9)
            badge.kind = "badge"
            kj.copies["secrets"].add(badge)
            kj.keep(self, badge)
            self.play(FadeIn(card, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Save it in a secrets folder")
            self.play(FadeOut(c5), FadeOut(turn5), run_time=0.4)
            self.play(kj.animate.move_to([-2.4, 1.85, 0]), card.animate.move_to([2.3, 1.85, 0]),
                      FadeIn(s5, shift=UP * 0.2), run_time=0.7)
            type_cmd(self, s5, C12.cmd, type_time=0.5)
            r12 = out(self, s5, C12.at(2, 3) + [(C12.line(5), S.GREY), C12.line(6)], wrap=True, run_time=0.6)
            vo.wait_until("beside your clone")
            self.play(Indicate(r12[0], color=TURN, scale_factor=1.06), Indicate(r12[1], color=TURN, scale_factor=1.06),
                      run_time=0.8)
            self.add(s5)
            vo.wait_until("not inside it")
            csv_row = [r for r in r12 if r.text == CSV_NAME][0]
            self.play(*recolor(csv_row.glyphs, TURN), run_time=0.4)
            keep = beside(row_tag("keep this name · docker-shell.sh:10"), csv_row, buff=0.45)
            pin(self, csv_row, keep)
            vo.wait_until("so it can never be committed")
            self.play(Indicate(kj.places["secrets"].text, color=INK, scale_factor=1.08), run_time=0.8)

        # ========================================================== 6. the key pair
        c6 = console_drawing("EC2 › Key Pairs › Create key pair",
                             [("Name", KEYPAIR_README), ("button", "Download .pem")])
        at_top_left(c6)
        turn6 = edge_tag(c6.frame, your_turn())
        # the README's name is the wrong one (beat 7): say so before the viewer pauses to create it
        wait6 = grey_chip("wait: name it ac215_2024 · see next", color=TURN)
        wait6.next_to(turn6, RIGHT, buff=0.3)
        pem_i = [i for i, r in enumerate(r12) if r.text == PEM_README][0]
        pem2 = [r12[pem_i - 1], r12[pem_i]]
        assert pem2[0].text.startswith("-rw------- ")
        kept = list(pem2) + [r12[-2], r12[-1]]
        with self.voiceover(SAY[6]) as vo:
            unpin(self, csv_row, keep, track(tr, 5))
            resize(self, s5, 4, keep=kept, extra=[kj.animate.move_to([3.9, 2.25, 0]),
                                                 card.animate.move_to([3.9, 0.55, 0])], run_time=0.8)
            self.play(FadeIn(c6, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(turn6, shift=UP * 0.1), FadeIn(wait6, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and save its pem file there too")
            btn = c6.rows[1]
            self.play(Indicate(btn.text, color=TURN, scale_factor=1.08), run_time=0.5)
            key = key_glyph(0.3).move_to(btn.box)
            self.play(FadeIn(key, scale=1.8), run_time=0.4)
            self.play(key.animate(path_arc=-PI / 3).move_to(kj._slot("secrets", 1)), run_time=0.9)
            key.kind = "key"
            kj.copies["secrets"].add(key)
            kj.keep(self, key)
            self.play(*[a for r in pem2 for a in recolor(r.glyphs, TURN)], run_time=0.4)
            stand = beside(row_tag("a throwaway key stands in here"), pem2[-1], buff=0.45)
            pin(self, pem2[-1], stand)
            vo.wait_until("The badge talks to the AWS API")
            self.play(FadeOut(c6), FadeOut(turn6), FadeOut(wait6), FadeOut(card), kj.animate.move_to([0, 1.25, 0]), run_time=0.6)
            api = cloud_chip("AWS API").move_to([4.0, 1.75, 0])
            a1 = route(badge.get_right() + RIGHT * 0.05, api.get_left() + LEFT * 0.08, arc=-0.4, stroke=3)
            self.play(GrowArrow(a1), Indicate(badge, color=INK, scale_factor=1.4), run_time=0.6)
            self.play(FadeIn(api, shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("the key opens the S S H door")
            door = cloud_chip("SSH door · your server").move_to([-4.0, 1.75, 0])
            a2 = route(key.get_left() + LEFT * 0.05, door.get_right() + RIGHT * 0.08, arc=0.4, stroke=3)
            self.play(GrowArrow(a2), Indicate(key, color=INK, scale_factor=1.4), run_time=0.6)
            self.play(FadeIn(door, shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 7. a small gap: three names
        t7 = term(P_HOME, rows=14, size=T20)
        g13 = [cut(C13.line(2), KEYPAIR_README)] + C13.at(5) + [cut(C13.line(6), "ac215_2024.pem'")] + C13.at(7, 8) + [cut(C13.line(9), "ac215_2024.pem")]
        err_t = erratum_tag()
        # two Texts, not t2c: t2c swallowed the space before ac215_2024 ("name yoursac215_2024")
        fix1 = VGroup(label("three names, one key pair → name yours", 22, INK),
                      label("ac215_2024", 22, TURN)).arrange(RIGHT, buff=0.15, aligned_edge=DOWN)
        fix2 = label("(or change inventory.yml:16 and the key paths)", 22, S.GREY)
        fix_rows = VGroup(fix1, fix2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        fix_fr = box(fix_rows.width + 0.6, fix_rows.height + 0.45, S.GREY, fill_opacity=0.06)
        fix_rows.move_to(fix_fr)
        fix = VGroup(fix_fr, fix_rows)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(kj, api, door, a1, a2)), FadeOut(s5), FadeOut(stand),
                      track(tr, 5, True), run_time=0.5)
            self.remove(s5, kj)
            self.play(FadeIn(t7, shift=UP * 0.2), run_time=0.5)
            type_cmd(self, t7, C13.cmd, type_time=0.8)
            ex7 = on_bar(t7, extra_row())
            self.play(FadeIn(ex7), run_time=0.3)
            vo.wait_until("The README names the key pair")
            r2 = out(self, t7, [g13[0]], wrap=True, run_time=0.5)
            hit = [r for r in r2 if KEYPAIR_README in r.text]
            assert hit, [r.text for r in r2]
            self.play(*recolor(substring(hit[0], KEYPAIR_README), SHARED), run_time=0.5)
            self.add(t7, ex7)
            vo.wait_until("The code expects")
            r5 = out(self, t7, g13[1:] + ["…"], wrap=True, run_time=0.8)
            vo.wait_until("in three files")
            hits = [g for r in r5 for g in all_of(r, KEYPAIR_CODE)]
            assert len(hits) >= 4, len(hits)
            self.play(LaggedStart(*[AnimationGroup(*recolor(g, TURN)) for g in hits], lag_ratio=0.25), run_time=1.0)
            self.add(t7, ex7)
            vo.wait_until("Easiest fix")
            self.play(FadeOut(ex7), run_time=0.2)
            self.remove(ex7)
            resize(self, t7, 9, run_time=0.6)
            on_bar(t7, ex7)
            self.play(FadeIn(ex7), run_time=0.2)
            fix.move_to([0, (t7.box.get_top()[1] + 2.75) / 2 - 0.05, 0])
            err_t.next_to(fix, UP, buff=0.06).align_to(fix, LEFT).shift(RIGHT * 0.2)
            self.play(FadeIn(fix, shift=DOWN * 0.15), FadeIn(err_t), run_time=0.6)
            vo.wait_until("so the file is")
            self.play(Indicate(fix1[1], color=TURN, scale_factor=1.06), run_time=0.8)

        # ========================================================== 8. chmod 400
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(fix), FadeOut(err_t), run_time=0.4)
            t7.clear(self)
            self.play(FadeOut(ex7), run_time=0.2)
            self.remove(ex7)
            resize(self, t7, 7, run_time=0.5)
            cd_prompt(self, t7, P_REPO)
            on_bar(t7, ex7)
            self.play(FadeIn(ex7), run_time=0.2)
            type_cmd(self, t7, C14.cmd, type_time=0.7)
            r14 = out(self, t7, C14.at(2, 3, 4), wrap=True, run_time=0.6)
            perm = [r for r in r14 if r.text.startswith("-r--------")][0]
            name = [r for r in r14 if r.text == PEM_README][0]
            rg = ring(name.glyphs, S.GREY, buff=0.07)
            ours = under_term(t7, grey_chip("our stand-in kept the README's name · yours: ac215_2024.pem"))
            self.play(Create(rg), FadeIn(ours, shift=DOWN * 0.1), run_time=0.5)
            attach(self, name, rg)
            vo.wait_until("S S H refuses a private key")
            mode = substring(perm, "-r--------")
            self.play(*recolor(mode, OWN), run_time=0.4)
            self.play(Indicate(mode, color=OWN, scale_factor=1.15), run_time=0.7)
            self.add(t7, ex7)
        self.wait(1.0)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.remove(*self.mobjects)
        self.wait(0.3)
