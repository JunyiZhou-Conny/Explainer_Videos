"""S12 · SSH keys and OS Login (AC215 L20). TRACKER [P] 5 (beats 0-2), 6 (3-4), 7 (5), 8 (6).
No lecture tag (the slides skip this setup): a GREY chip 'not on the slides' top right in beat 0.

Beats (script.md "## S12", one voiceover block each):
0. TRACKER [P] 5. GREY chip 'not on the slides'. V8: the BLUE deployment key (deployment.json), then
   the PURPLE key ssh-key-deployment beside it (SshKey.appear). Below, a sketch: the GREY laptop
   (Pulumi inside) -> PINK 'SSH' arrow -> an outlined BLUE VM ('scripts', 'docker'), and a badge
   'who logs in?' (YELLOW) 'deployment, via OS Login'; the deployment key flashes on "The deployment
   service account".
1. Sketch, deployment key and chip go; the PURPLE key stays parked above a 6-row terminal
   'laptop · toolbox' (prompt from b02d:77). Types b08 (folds) -> TERM(b08: 2) RED; on "the angle
   bracket lesson" every < and > of the typed line turns PINK and pulses; on "replace the whole
   placeholder" '<YOUR GCP_PROJECT>' is underlined YELLOW.
2. Types b09 (folds); 'ac215-project' flashes YELLOW with the GREY default_tag above the terminal
   -> TERM(b09: 2 wrap) RED; GREY ghost row tag 'yours: Updated […]' (said, not output).
3. TRACKER [P] 6. Fresh screen. b10 typed command by command: `cd /secrets` (at …:/app#), then at
   …:/secrets# `ssh-keygen -f ssh-key-deployment` -> TERM(b10: 4-8) with a YELLOW '⏎ Enter' tag after
   lines 5 and 6; the PURPLE key is cut into 'private' and '.pub' when lines 7-8 print; `cd /app` at
   …:/secrets#, then the prompt is back at …:/app# (path flashes). A RED-outlined chip (GREY words)
   'no passphrase: Pulumi cannot type one' above the terminal.
4. TRACKER [P] 6 · extra. Fresh screen. `ls -la /secrets` (extra row tag) -> TERM(b11: 6-9); a PINK
   arrow from '/secrets' up to a GREY folder card 'secrets/' 'on your laptop' + PINK 'the same
   folder'; on "the private key" line 8's name YELLOW and '-rw-------' GREEN, the private half
   flashes; on "the public half" line 9's name YELLOW, the .pub half flashes.
5. TRACKER [P] 7. Fresh screen. b12 typed (folds) while the BLUE 'deployment · OS Login profile' card
   appears and '.pub' flies up to it -> TERM(b12: 2 wrap) RED. On "the README shows yours" the profile
   hands back the YELLOW 'sa_000…' tag; the halves go, profile and tag move left, the terminal
   shrinks to a 2-row strip (the error stays) and EXPECTED(expected/oslogin: 2-10) slides in from the
   right (tag 'expected · README:306–314'); its 'username: sa_000…' row YELLOW and ringed. YELLOW
   '▶ your turn' under the name tag.
6. TRACKER [P] 8. README card (README.md · lines 318–322) top left with a GREY erratum tag,
   'inventory.yml' underlined RED. TRACKER [P] 8 · extra: b13 (folds) -> TERM(b13: 2) RED. A
   GREY-dashed chip 'earlier · Ansible' and a GREEN arrow to 'Pulumi config · VM stack'. Fade; empty
   frame.

Deviations from SHOW:
- Beat 0: the sketch's laptop holds a PURPLE 'pulumi' chip and the VM 'scripts' / 'docker' chips (the
  SAY names them); the badge has two rows.
- Beat 3: b10's three README lines are typed one at a time with the keygen dialogue between them (the
  order a viewer sees when running them), instead of all three first.
- Beat 5: the EXPECTED panel cannot sit beside a full-width terminal: the terminal shrinks to a 2-row
  strip holding the RED error, and the panel fills the right of the frame; the SshKey profile and its
  name tag move to the left of it.
- Beat 6: the GREEN arrow's target reads 'Pulumi config · VM stack' instead of '(S14)' (a scene number
  means nothing to a viewer; beat 5's SAY calls it the VM stack's config). The README card shows line 319's empty
  bullet as '•'.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S12"]
assert len(SAY) == SAY_COUNT["S12"] == 7

# ------------------------------------------------------------------ the real sources (checked)
B08, B09, B10, B11, B12, B13 = (capture(k) for k in ("b08", "b09", "b10", "b11", "b12", "b13"))
assert B08.cmd == readme(286) == ("gcloud compute project-info add-metadata --project <YOUR GCP_PROJECT> "
                                  "--metadata enable-oslogin=TRUE")
assert B08.line(2) == "bash: line 1: YOUR: No such file or directory"
assert B09.cmd == readme(290) and "--project ac215-project" in B09.cmd
assert B09.line(2) == ("ERROR: (gcloud.compute.project-info.add-metadata) You do not currently have an "
                       "active account selected.")
assert B10.cmd_lines == [readme(295), readme(296), readme(297)] == ["cd /secrets", "ssh-keygen -f ssh-key-deployment",
                                                                     "cd /app"]
assert B10.line(4) == "Generating public/private rsa key pair."
assert B10.line(5) == "Enter passphrase (empty for no passphrase):"
assert B10.line(6) == "Enter same passphrase again:"
assert B10.line(7) == "Your identification has been saved in ssh-key-deployment"
assert B10.line(8) == "Your public key has been saved in ssh-key-deployment.pub"
assert B11.cmd == "ls -la /secrets"
assert B11.line(8).startswith("-rw------- 1 root app") and B11.line(8).endswith(" ssh-key-deployment")
assert B11.line(9).startswith("-rw-r--r-- 1 root app") and B11.line(9).endswith(" ssh-key-deployment.pub")
assert B12.cmd == readme(302) == "gcloud compute os-login ssh-keys add --key-file=/secrets/ssh-key-deployment.pub"
assert B12.line(2) == ("ERROR: (gcloud.compute.os-login.ssh-keys.add) You do not currently have an active "
                       "account selected.")
assert B13.cmd.startswith("ls inventory.yml; find / -name inventory.yml")
assert B13.line(2) == "ls: cannot access 'inventory.yml': No such file or directory"
assert readme(318) == "#### Deployment Setup" and "inventory.yml" in readme(320)
OSL = recorded("oslogin-ssh-keys-add", (2, 10), plain=False)
assert OSL[-1].strip() == f"username: {SA_MASK}"

P_APP, P_SECRETS = toolbox_prompt("/app"), toolbox_prompt("/secrets")
assert P_APP == P_TOOLBOX

TERM_ROWS = 6                      # top edge at about -0.23: the picture lives in y in [-0.1, 2.8]
PIECE_SHIFT = np.array([1.0, 1.0, 0])    # SshKey: key at (-1.2, 0.4), profile at (2.5, 2.2)


def readme_body() -> VGroup:
    """README.md:318-322 as card rows (markdown stripped; line 319's lone bullet shown as '•')."""
    rows = []
    for n in range(318, 323):
        s = md_plain(readme(n))
        rows.append("•" if s.strip() == "*" else s)
    return VGroup(*[label(s, 22, INK) for s in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)


def word(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` in a label Text (its submobjects skip whitespace; a ligature such as the
    'fi' of 'file' is one glyph, so `sub` must come before any ligature on its row)."""
    flat = t.text.replace(" ", "").replace("\n", "")
    i = flat.index(sub.replace(" ", ""))
    assert not any(lig in flat[:i + len(sub)] for lig in ("fi", "fl", "ff")), t.text
    return VGroup(*t.submobjects[i:i + len(sub.replace(" ", ""))])


class SshKeys(VoiceScene):
    def construct(self):
        # ========================================================== 0. why SSH, who logs in
        trk = tracker_p(5)
        skip = grey_chip("not on the slides")
        skip.move_to([SAFE_X - 0.1 - skip.width / 2, 3.25, 0])
        dep = key_icon("deploy", True, 0.9).move_to([-3.9, 0.4, 0])
        sk = SshKey()
        sk.shift(PIECE_SHIFT)
        sk.key.shift(PIECE_SHIFT)          # built in __init__ but only added by appear(): move it too
        assert dep.get_right()[0] < sk.key.get_left()[0] - 0.2 and dep.get_left()[0] > -6.5

        y0 = -1.7
        lap_box = outline_box(3.4, 1.3, LAPTOP, solid=True, fill_opacity=0.08).move_to([-4.8, y0, 0])
        lap_t = label("your laptop", 20, LAPTOP).move_to(lap_box).align_to(lap_box, UP).shift(DOWN * 0.14)
        lap_p = tool_chip("pulumi").next_to(lap_t, DOWN, buff=0.14)
        lap = VGroup(lap_box, lap_t, lap_p)
        vm_box = outline_box(3.4, 1.3, CLOUD, solid=True, fill_opacity=0.08).move_to([4.8, y0, 0])
        vm_t = label("VM", 20, CLOUD).move_to(vm_box).align_to(vm_box, UP).shift(DOWN * 0.14)
        vm_c = VGroup(grey_chip("scripts"), tool_chip("docker")).arrange(RIGHT, buff=0.12)
        vm_c.next_to(vm_t, DOWN, buff=0.14)
        assert vm_c.width < vm_box.width - 0.4, vm_c.width
        vm = VGroup(vm_box, vm_t)
        ssh = route(lap_box.get_right() + RIGHT * 0.05, vm_box.get_left() + LEFT * 0.05)
        ssh_t = label("SSH", 22, ROUTE).next_to(ssh, UP, buff=0.12)
        q1 = label("who logs in?", 20, TURN)
        q2 = label("deployment, via OS Login", 20, INK)
        qrows = VGroup(q1, q2).arrange(DOWN, buff=0.08)
        qbox = outline_box(qrows.width + 0.5, qrows.height + 0.3, S.GREY, solid=True, fill_opacity=0.08)
        qbox.next_to(ssh, DOWN, buff=0.14)
        qrows.move_to(qbox)
        assert qbox.get_bottom()[1] > -3.55 and qbox.get_left()[0] > lap_box.get_right()[0] + 0.1, qbox.get_bottom()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(skip, shift=LEFT * 0.2), run_time=0.7)
            self.play(FadeIn(dep, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("Pulumi will log in to the VM over SSH")
            self.play(FadeIn(lap, shift=RIGHT * 0.2), FadeIn(vm, shift=LEFT * 0.2), run_time=0.6)
            self.play(GrowArrow(ssh), FadeIn(ssh_t, shift=UP * 0.1), run_time=0.6)
            sk.appear(self, run_time=0.5)
            vo.wait_until("to run scripts and drive Docker")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in vm_c], lag_ratio=0.4), run_time=0.7)
            vo.wait_until("Who logs in?")
            self.play(FadeIn(qbox), FadeIn(q1, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(q1, color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("The deployment service account")
            self.play(FadeIn(q2, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(dep.glyph, color=CLOUD, scale_factor=1.25), Indicate(dep.text, color=INK, scale_factor=1.1),
                      run_time=0.8)
            vo.wait_until("through OS Login")
            self.play(Indicate(q2, color=CLOUD, scale_factor=1.08), run_time=0.7)

        # ========================================================== 1. OS Login: the template fails
        t = toolbox_term(TERM_ROWS)
        assert abs(t.box.get_top()[1] - (-0.23)) < 0.05
        assert sk.key.get_bottom()[1] > t.box.get_top()[1] + 0.1, sk.key.get_bottom()
        sketch = VGroup(lap, vm, vm_c, ssh, ssh_t, qbox, q1, q2)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(sketch), FadeOut(dep), FadeOut(skip), run_time=0.5)
            self.remove(sketch, dep, skip)
            self.play(FadeIn(t, shift=UP * 0.3), run_time=0.5)
            ln1 = type_capture(self, t, B08, type_time=0.9)[0]
            vo.wait_until("Typed as printed")
            self.play(Indicate(ln1.rows[1], color=TURN, scale_factor=1.03), run_time=0.6)
            self.add(t)
            vo.wait_until("the template fails with no such file")
            e1 = out(self, t, [(B08.line(2), ERR)], run_time=0.4)[0]
            self.play(Indicate(substring(e1, "No such file or directory"), color=ERR, scale_factor=1.08), run_time=0.6)
            self.add(t)
            vo.wait_until("It is the angle bracket lesson again")
            brackets = VGroup()
            for row in rows_of(ln1):
                for i, ch in enumerate(row.text):
                    if ch in "<>":
                        brackets.add(*glyph_range(row, i, i + 1))
            assert len(brackets) == 2
            self.play(brackets.animate.set_color(ROUTE), run_time=0.4)
            self.play(Indicate(brackets, color=ROUTE, scale_factor=1.6), run_time=0.7)
            self.add(t)
            vo.wait_until("replace the whole placeholder")
            ph = substring(ln1.rows[1], "<YOUR GCP_PROJECT>")
            u1 = under(ph, TURN, stroke=4)
            self.play(Create(u1), run_time=0.5)
            attach(self, ln1.rows[1], u1)
            self.play(Indicate(ph, color=TURN, scale_factor=1.08), run_time=0.6)
            self.add(t)

        # ========================================================== 2. the README's example project
        dtag = under_term(t, default_tag())
        assert dtag.get_left()[0] > sk.key.get_right()[0] + 0.2, dtag.get_left()
        with self.voiceover(SAY[2]) as vo:
            ln2 = type_capture(self, t, B09, type_time=0.9)[0]
            pr = substring(ln2.rows[1], PROJECT_README)
            self.play(pr.animate.set_color(TURN), FadeIn(dtag, shift=DOWN * 0.1), run_time=0.5)
            self.add(t)
            vo.wait_until("which you change to yours")
            self.play(Indicate(pr, color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(t)
            flash_tag(self, dtag, INK)
            vo.wait_until("Ours says no active account")
            e2 = out(self, t, [(B09.line(2), ERR)], wrap=True, run_time=0.5)
            vo.wait_until("yours prints updated")
            ghost = row_tag("yours: Updated […]", S.GREY)
            pin(self, e2[-1], beside(ghost, e2[-1]))
            flash_tag(self, ghost, INK)

        # ========================================================== 3. ssh-keygen, no passphrase
        nopass = chip("no passphrase: Pulumi cannot type one", ERR, size=20, text_color=S.GREY, fill_opacity=0.08)
        under_term(t, nopass)
        assert nopass.get_left()[0] > sk.key.get_right()[0] + 0.2
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(dtag), track(trk, 6), run_time=0.5)
            self.remove(dtag)
            t.clear(self)
            vo.wait_until("in slash secrets")
            c1 = type_cmd(self, t, B10.cmd_lines[0], type_time=0.5)
            t.set_prompt(P_SECRETS)
            vo.wait_until("run ssh keygen")
            type_cmd(self, t, B10.cmd_lines[1], type_time=0.8)
            out(self, t, [B10.line(4)], run_time=0.3)
            vo.wait_until("press Enter twice")
            enters = []
            for n in (5, 6):
                r = out(self, t, [B10.line(n)], run_time=0.3)[0]
                e = row_tag("⏎ Enter", TURN)
                pin(self, r, beside(e, r, buff=0.3), run_time=0.3)
                enters.append(e)
            r78 = out(self, t, [B10.line(7), B10.line(8)], run_time=0.4)
            sk.cut(self)
            self.play(*[Indicate(substring(r, "ssh-key-deployment"), color=TOOL, scale_factor=1.06) for r in r78],
                      run_time=0.6)
            self.add(t)
            vo.wait_until("and go back to slash app")
            type_cmd(self, t, B10.cmd_lines[2], type_time=0.4)
            cd_prompt(self, t, P_APP, color=TURN)
            vo.wait_until("No passphrase")
            self.play(FadeIn(nopass, shift=DOWN * 0.1), run_time=0.5)
            self.play(*[Indicate(e.text, color=TURN, scale_factor=1.15) for e in enters], run_time=0.7)
            self.add(t)
            assert c1 is not None

        # ========================================================== 4. ls -la /secrets (extra)
        fold_g = folder_icon(0.5, LAPTOP)
        fold_n = mono("secrets/", 22, INK)
        fold_c = label("on your laptop", 20, LAPTOP)
        frow = VGroup(fold_g, fold_n).arrange(RIGHT, buff=0.18)
        fin = VGroup(frow, fold_c).arrange(DOWN, buff=0.12)
        fbox = outline_box(fin.width + 0.5, fin.height + 0.35, LAPTOP, solid=True, fill_opacity=0.08)
        fbox.move_to([4.7, 1.3, 0])
        fin.move_to(fbox)
        fcard = VGroup(fbox, fin)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(nopass), track(trk, 6, True), run_time=0.5)
            self.remove(nopass)
            t.clear(self)
            ls = type_capture(self, t, B11, type_time=0.6)[0]
            pin(self, ls, beside(extra_row(), ls))
            rows = out(self, t, B11.at((6, 9)), run_time=0.6)
            assert len(rows) == 4 and rows[2].text == B11.line(8) and rows[3].text == B11.line(9)
            vo.wait_until("on your laptop")
            src = substring(ls, "/secrets")
            a = arrow(src.get_top() + UP * 0.08, fbox.get_corner(DL) + np.array([0.3, -0.02, 0]), ROUTE,
                      stroke=4, buff=0.0)
            same = label("the same folder", 20, ROUTE).next_to(fbox, DOWN, buff=0.12).align_to(fbox, RIGHT)
            assert same.get_bottom()[1] > t.box.get_top()[1] + 0.05, same.get_bottom()
            self.play(src.animate.set_color(ROUTE), FadeIn(fcard, shift=DOWN * 0.15), run_time=0.5)
            self.play(GrowArrow(a), FadeIn(same, shift=UP * 0.1), run_time=0.6)
            self.add(t)
            vo.wait_until("the private key")
            nm8 = substring(rows[2], "ssh-key-deployment")
            pm8 = substring(rows[2], "-rw-------")
            self.play(nm8.animate.set_color(TURN), pm8.animate.set_color(OWN), run_time=0.4)
            self.play(Indicate(sk.halves[0], color=TOOL, scale_factor=1.15), run_time=0.6)
            sk.heal(self)
            vo.wait_until("readable only by you")
            self.play(Indicate(pm8, color=OWN, scale_factor=1.15), run_time=0.6)
            self.add(t)
            vo.wait_until("and the public half")
            nm9 = substring(rows[3], "ssh-key-deployment.pub")
            self.play(nm9.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(sk.halves[1], color=TOOL, scale_factor=1.15), Indicate(nm9, color=TURN, scale_factor=1.06),
                      run_time=0.6)
            sk.heal(self)
            self.add(t)

        # ========================================================== 5. upload the .pub; the sa_ user
        panel = quote_card("oslogin-ssh-keys-add", (2, 10), source="README:306–314", mono_font=True, width_chars=50)
        user_row = panel.body[-1]
        # the wrapped 'name:' row: its continuation lines up under the value (quote_card indents it by 2)
        k_name = next(i for i, r in enumerate(panel.body) if r.text.startswith("    name: "))
        cont = panel.body[k_name + 1]
        assert cont.text.startswith("  ") and not cont.text.startswith("   ") and len(cont.text) + 8 <= 50, cont.text
        cont.shift(RIGHT * 8 * cell_width(20))
        assert user_row.text.strip() == f"username: {SA_MASK}", user_row.text
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(a, same, fcard)), track(trk, 7), run_time=0.5)
            self.remove(a, same, fcard)
            t.clear(self)
            vo.wait_until("to the OS Login profile")
            type_capture(self, t, B12, type_time=0.9)
            sk.upload(self)
            vo.wait_until("Ours stops at the same error")
            out(self, t, [(B12.line(2), ERR)], wrap=True, run_time=0.5)
            vo.wait_until("the README shows yours")
            sk.username(self)
            sk.drop(self, sk.halves, run_time=0.3)
            resize(self, t, 2, extra=[sk.animate.shift(np.array([-7.2, -0.6, 0]))], run_time=0.7)
            sk.heal(self)
            panel.move_to([0, 0, 0]).align_to([6.5, 0, 0], RIGHT)
            panel.align_to([0, t.box.get_top()[1] + 0.14, 0], DOWN)
            assert panel.tag.get_top()[1] < 3.0 and panel.frame.get_left()[0] > sk.profile.get_right()[0] + 0.15, \
                (panel.tag.get_top(), panel.frame.get_left(), sk.profile.get_right())
            assert panel.frame.get_left()[0] > sk.name_tag.get_right()[0] + 0.15
            self.play(FadeIn(panel, shift=LEFT * 0.6), run_time=0.6)
            vo.wait_until("ending in a username")
            val = substring(user_row, SA_MASK)
            ringu = ring(user_row, TURN)
            self.play(user_row.animate.set_color(TURN), Create(ringu), run_time=0.6)
            self.play(Indicate(val, color=TURN, scale_factor=1.06), Indicate(sk.name_tag, color=TURN, scale_factor=1.1),
                      run_time=0.7)
            sk.heal(self)
            self.add(panel, ringu)         # re-seat the panel, then the ring ON TOP (its filled frame hid it)
            vo.wait_until("Copy it")
            yt = your_turn().next_to(sk.name_tag, DOWN, buff=0.3)
            assert yt.get_bottom()[1] > t.box.get_top()[1] + 0.1 and yt.get_right()[0] < panel.frame.get_left()[0] - 0.1
            self.play(FadeIn(yt, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)
            vo.wait_until("the VM stack's config needs it")
            self.play(Indicate(sk.name_tag, color=TURN, scale_factor=1.12), run_time=0.6)
            sk.heal(self)

        # ========================================================== 6. inventory.yml: an Ansible leftover
        body = readme_body()
        rc = readme_card((318, 322), body)
        rc.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, 2.65, 0], UP)
        er = erratum_tag().next_to(rc, RIGHT, buff=0.3).align_to(rc, UP)
        inv = [word(r, "inventory.yml") for r in body[2:]]
        unders = VGroup(*[under(g, ERR, stroke=3) for g in inv])
        past = dashed_chip("earlier · Ansible")
        cfg = ok_chip("Pulumi config · VM stack")
        right_x = (rc.get_right()[0] + 6.5) / 2
        past.move_to([right_x, 1.0, 0])
        cfg.move_to([right_x, -0.35, 0])
        g_ar = arrow(past.get_bottom(), cfg.get_top(), OWN, stroke=4)
        assert er.get_right()[0] < 6.5 and cfg.get_right()[0] < 6.5 and past.get_left()[0] > rc.get_right()[0] + 0.15, \
            (er.get_right(), cfg.get_right(), past.get_left())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(sk, panel, ringu, yt)), track(trk, 8), run_time=0.5)
            self.remove(sk, panel, ringu, yt)
            t.clear(self, run_time=0.2)
            resize(self, t, 4, run_time=0.5)
            assert rc.get_bottom()[1] > t.box.get_top()[1] + 0.12, (rc.get_bottom(), t.box.get_top())
            self.play(FadeIn(rc, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("the next heading asks you to edit inventory dot yml")
            self.play(FadeIn(er), LaggedStart(*[Create(u) for u in unders], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("No such file exists")
            self.play(track(trk, 8, True), run_time=0.4)
            l13 = type_capture(self, t, B13, type_time=1.0)[0]
            out(self, t, [(B13.line(2), ERR)], run_time=0.4)
            assert l13 is not None
            vo.wait_until("it belongs to an earlier, Ansible version")
            self.play(FadeIn(past, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("The Pulumi config replaces it")
            self.play(GrowArrow(g_ar), FadeIn(cfg, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(cfg.text, color=OWN, scale_factor=1.1), run_time=0.6)

        self.play(FadeOut(VGroup(trk, t, rc, er, unders, past, cfg, g_ar)), run_time=0.6)
        self.remove(trk, t, rc, er, unders, past, cfg, g_ar)
        self.wait(0.4)
