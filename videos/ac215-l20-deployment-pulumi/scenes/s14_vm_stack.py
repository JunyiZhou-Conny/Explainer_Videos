"""S14 · Steps 3–4: the VM, its fences, provisioning (AC215 L20). TRACKER [P] 11-12 in beats 1-7;
no tracker in beat 0 and from beat 8 on.

Beats (script.md "## S14", one voiceover block each):
0. Lecture 20 · slides 19, 22. The six-step strip (chips 1-2 ticked, chip 3 'VM' YELLOW) lights and
   shrinks away. V1 at slide 22: the GCP outline, the empty BLUE VM panel, a BLUE disk cylinder on a
   cable '/mnt/disk-1'; a GREY-dashed 'NFS' chip by the cable flips to 'attached disk' with a GREY
   erratum tag; the GREY-dashed models pail stays dim.
1. TRACKER [P] 11. Terminal 'laptop · toolbox' at /app/deploy_images. GREY chip 'README:349 · cd into
   deploy_single_vm'; `cd ../deploy_single_vm` (no output; the prompt's path flashes). Then fast:
   `pulumi stack init dev` -> TERM(b18: 2); the three `pulumi config set …` (b19-1..3, sa_ masked; the
   GREY "README's default" row tag on the title bar) -> TERM(…: 2); TRACKER [P] 12: preview (b20: 2),
   up (b21: 2). Every error RED, the same line stacked.
2. TRACKER [P] 11 · extra. Cleared: `pulumi stack init dev` -> TERM(b40: 2) (extra row tag beside its output); the three
   config sets (b41-1..3) -> no output; `pulumi config` -> TERM(b42: 2-6 wrap): ssh_user row YELLOW
   (chip 'your OS Login user · masked'), the email rows PINK (chip 'the account the VM runs as'),
   every 'ac215-project' underlined GREY under a default_tag (also on the typed b41-3 line). YELLOW
   '▶ your turn' on the title bar.
3. CODE(deploy_single_vm/__main__.py: 15-26): lines 15, 18, 21-23, 26 light in order, each with a
   chip of its slide-19 step: '3 VM', '4 Provision', '5 Containers', '6 Web server'.
4. V7a VmFences: the BLUE VPC 'cheese-app-network' + a GREY card 'same name as part 1's Docker
   network, now a cloud network'; three PINK gates, one per phrase (80 http-server, 443 https-server,
   22 every VM); GREY reference 'create_instance.py · lines 51–89'.
5. The VPC steps aside for CODE(create_instance.py: 92-103): 92-97 BLUE (+ GREY chip
   '50 · line 36' beside line 95), 100-103 YELLOW. Then V7a returns: the VM, its two tags,
   the disk on its cable, the sealed PINK envelope '<instance_ip>' and the caption 'Output: opens when
   the VM exists'.
6. TRACKER [P] 12 · extra. V7a's picture gives way to its plan list (two columns); a 7-row terminal types `pulumi
   preview --stack dev --refresh` (extra) -> TERM(b43: 6-10, …, 21-22, …, 41 wrap, …, 44-45): the five
   create lines GREEN as the plan ticks Disk, Network and three Firewalls; line 21 YELLOW; 41 RED and
   the plan's get_image row RED; '+ 6 to create' GREEN, '1 errored' RED; a GREY chip 'yours: about 30
   resources'.
7. TRACKER [P] 12. A YELLOW card 'check the plan before -y' with a GREY example '~ gcp:compute:Instance
   … replace' ('illustration of what to look for'); two GOLD cost tags; in the strip a GREY ghost of
   `pulumi up --stack dev --refresh -y` with a YELLOW '▶ your turn'.
8. Lecture 20 · slides 14, 19. The strip returns (chip 3 ticked, chip 4 'Provision' YELLOW) with a
   GREY chip 'no slide draws this step'; V4's banner 'Pulumi manages infrastructure through cloud
   APIs' + GREY footnote '… and SSH, for the inside of the VM'. V7b: nine tiles fall in order.
9. Caption 'Pulumi remembers that a command ran, not what it changed'; the dominoes move down and
   CODE(provision_instance.py: 24-31) appears: line 29 YELLOW, 'blkid -o value -s TYPE' GREEN,
   '|| mkfs.ext4' RED-outlined.
10. Panel and caption go, the dominoes dim; a copy of tile 1 alone at the centre. PONDER 8 s.
11. V7b replay: tiles stand; the disk with 'chat history', 'model'; tile 1 refuses ('has a
    filesystem'); a GREY ghost tile without the guard wipes the disk (labels RED, gone); the guarded
    tile again: labels back GREEN. Caption 'scripts must be safe to run twice'. Fade; empty frame.

Deviations from SHOW:
- Beat 0: the erratum is a GREY 'erratum' tag beside the 'attached disk' chip (no "dot" glyph exists).
- Beat 1: the default_tag is the row-sized "README's default" tag on the terminal's title bar while the
  config sets type (the house default_tag is wider than the room beside a folded command row).
- Beat 2: the chip texts read 'your OS Login user · masked' (not 'from S12': a scene number means
  nothing to a viewer) and 'the account the VM runs as'; they sit above the terminal, colour-matched
  to their rows (no room beside the rows); one default_tag above the terminal, every 'ac215-project'
  underlined GREY. '▶ your turn' sits on the title bar.
- Beat 3: lines 15, 18, 22 and 26 are shortened with GREY '…' (elide / cuts) so the step chips fit to
  the right of the panel.
- Beat 5: CODE(create_instance.py) and V7a cannot share the frame (the VPC is 8.5 wide, the panel 7.4),
  so the VPC steps aside for the first sentence and returns for the second; a GREY chip names where
  the 50 comes from (line 36, outside the range).
- Beat 6: a terminal and the full VPC cannot share the frame either: the VPC picture fades and V7a's
  plan list (two columns of three, so the RED Response line stays visible in a 7-row terminal)
  carries the ticks; beat 7's ghost gets a fresh 3-row strip.
- Beat 7: the GOLD cost line is split into two tags (one line would be 13 units wide).
- Beat 10: the panel and caption fade out instead of dimming (the ponder card and the tile need the
  middle of the frame); the dominoes dim.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S14"]
assert len(SAY) == SAY_COUNT["S14"] == 12

# ------------------------------------------------------------------ the real sources (checked)
B18, B20, B21 = capture("b18"), capture("b20"), capture("b21")
B19 = [capture(f"b19-{i}") for i in (1, 2, 3)]
B40, B42, B43 = capture("b40"), capture("b42"), capture("b43")
B41 = [capture(f"b41-{i}") for i in (1, 2, 3)]
TOKEN_ERR = "error: PULUMI_ACCESS_TOKEN must be set for login during non-interactive CLI sessions"
assert readme(349).startswith("- cd into `deploy_single_vm`")
assert B18.cmd == readme(352) == "pulumi stack init dev" == B40.cmd
assert [c.cmd for c in B19] == [readme(n) for n in (353, 354, 355)] == [c.cmd for c in B41]
assert SA_MASK in B19[1].cmd and "deployment@ac215-project" in B19[2].cmd
assert B20.cmd == readme(361) == "pulumi preview --stack dev --refresh" == B43.cmd
assert B21.cmd == readme(366) == "pulumi up --stack dev --refresh -y"
for c in [B18, *B19, B20, B21]:
    assert c.line(2) == TOKEN_ERR, c.key
assert B40.line(2) == "Created stack 'dev'"
assert all(not c.lines for c in B41)
assert B42.cmd == "pulumi config"
assert B42.line(3).startswith("gcp:project") and B42.line(3).endswith(PROJECT_README)
assert B42.line(5).startswith("security:gcp_service_account_email  deployment@ac215-project")
assert B42.line(6) == f"security:ssh_user                   {SA_MASK}"
assert "gcp:compute:Disk" in B43.line(6) and "Firewall allow-ssh" in B43.line(10)
assert "create_instance.py\", line 100" in B43.line(21)
assert "invalid_grant" in B43.line(41)
assert B43.line(44).strip() == "+ 6 to create" and B43.line(45).strip() == "1 errored"

MAIN = "src/deployment/deploy_single_vm/__main__.py"
CREATE = "src/deployment/deploy_single_vm/create_instance.py"
PROV = "src/deployment/deploy_single_vm/provision_instance.py"
assert "create_instance()" in excerpt(MAIN, 15, 15) and "provision_instance(" in excerpt(MAIN, 18, 18)
assert "setup_containers(" in excerpt(MAIN, 21, 21) and "setup_webserver(" in excerpt(MAIN, 26, 26)
assert "gcp.compute.Disk(" in excerpt(CREATE, 92, 92) and 'type="pd-standard"' in excerpt(CREATE, 96, 96)
assert "get_image(" in excerpt(CREATE, 100, 100) and "persistent_disk_size = 50" in excerpt(CREATE, 36, 36)
assert "blkid -o value -s TYPE" in excerpt(PROV, 29, 29) and "|| mkfs.ext4" in excerpt(PROV, 29, 29)
assert "allow-http" in excerpt(CREATE, 52, 52) and '"22"' in excerpt(CREATE, 85, 85)

P_IMAGES, P_VMDIR = toolbox_prompt("/app/deploy_images"), toolbox_prompt("/app/deploy_single_vm")


def span_bar(code_, k0: int, k1: int, color, opacity: float = 0.2) -> Rectangle:
    """One translucent bar over lines k0..k1 (0-based) of a code_block."""
    top, bot = line_bar(code_, k0, color), line_bar(code_, k1, color)
    h = top.get_top()[1] - bot.get_bottom()[1]
    return Rectangle(width=top.width, height=h, stroke_width=0).set_fill(color, opacity).move_to(
        [top.get_center()[0], (top.get_top()[1] + bot.get_bottom()[1]) / 2, 0])


def plan_grid(vf, scene, run_time: float = 0.5):
    """VmFences.plan_rows laid out as two columns of three (Disk, Network, allow-http | allow-https,
    allow-ssh, get_image) at the top, so a 7-row terminal fits under it and the RED Response line
    stays on screen. Same parts as plan_rows (vf.plan, vf.plan_glyphs), so tick()/fail() work."""
    g = VGroup()
    for i, r in enumerate(vf.PLAN_ROWS):
        col, k = divmod(i, 3)
        g.add(label(r, 20, S.GREY).move_to([-4.3 + 4.9 * col, 1.9 - 0.5 * k, 0], aligned_edge=LEFT))
    hd = label("plan", 20, S.GREY).move_to([-4.75, 2.4, 0], aligned_edge=LEFT)
    vf.plan, vf.plan_glyphs = g, {}
    vf.show(scene, hd, g, run_time=run_time)
    return g


def same_err(c):
    """The token error of a b18-b21 capture: line 2, RED, wrapped."""
    return [(c.line(2), ERR)]


class VmStack(VoiceScene):
    def construct(self):
        # ========================================================== 0. step 3: the VM and its disk
        ref0 = lref("19, 22")
        ss = six_steps(3)
        ss.move_to([0, 0, 0]).shift(UP * (2.95 - ss.get_top()[1]))
        assert ss.get_top()[1] < ref0.get_bottom()[1] - 0.05
        md = MasterDiagram()
        md.shift(LEFT * 1.5)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref0), FadeIn(ss, shift=DOWN * 0.15), run_time=0.6)
            self.play(ss.light(3), run_time=0.7)
            self.add(ss)
            md.gcp(self)
            md.vm(self)
            ss.shrink_away(self)
            vo.wait_until("The slide draws a network share")
            dk = md.disk(self)
            mdl = md.models(self)
            self.play(mdl.animate.set_opacity(0.4), run_time=0.3)
            md.heal(self)
            nfs = dashed_chip("NFS").next_to(dk.frame, LEFT, buff=0.3)
            self.play(FadeIn(nfs, shift=RIGHT * 0.1), run_time=0.4)
            self.play(Indicate(nfs.text, color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("in this code that is a second disk")
            att = grey_chip("attached disk").next_to(dk.frame, LEFT, buff=0.3)
            er0 = erratum_tag().next_to(att, LEFT, buff=0.2)
            assert er0.get_left()[0] > md.parts["gcp"].frame.get_left()[0] + 0.1
            assert att.get_top()[1] < md.parts["vm"].frame.get_bottom()[1] - 0.05, att.get_top()
            self.play(ReplacementTransform(nfs, att), FadeIn(er0, shift=RIGHT * 0.1), run_time=0.7)
            self.play(Indicate(dk.frame, color=CLOUD, scale_factor=1.15), run_time=0.6)
            md.heal(self)
            vo.wait_until("mounted at mnt disk 1")
            self.play(Indicate(dk.text, color=TURN, scale_factor=1.12), run_time=0.7)
            md.heal(self)
        self.play(FadeOut(VGroup(md, att, er0, ref0)), run_time=0.5)
        self.remove(md, att, er0, ref0)

        # ========================================================== 1. b18-b21: the same error, stacked
        trk = tracker_p(11)
        t = toolbox_term(11, "/app/deploy_images")
        chip349 = under_term(t, grey_chip("README:349 · cd into deploy_single_vm"))
        dflt = on_bar(t, row_tag("the README's default", S.GREY))
        assert chip349.get_left()[0] > trk.get_right()[0] + 0.2 or chip349.get_bottom()[1] < trk.get_bottom()[1]
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.3), run_time=0.6)
            self.play(FadeIn(chip349, shift=DOWN * 0.1), run_time=0.3)
            type_cmd(self, t, "cd ../deploy_single_vm", type_time=0.4)
            cd_prompt(self, t, P_VMDIR, color=TURN, run_time=0.5)
            vo.wait_until("then stack init")
            self.play(FadeOut(chip349), run_time=0.2)
            self.remove(chip349)
            type_capture(self, t, B18, type_time=0.3)
            out(self, t, same_err(B18), wrap=True, run_time=0.3)
            vo.wait_until("three config sets")
            self.play(FadeIn(dflt), run_time=0.2)
            for c in B19:
                type_capture(self, t, c, type_time=0.25)
                out(self, t, same_err(c), wrap=True, run_time=0.25)
            self.play(FadeOut(dflt), track(trk, 12), run_time=0.3)
            self.remove(dflt)
            vo.wait_until("preview and up")
            type_capture(self, t, B20, type_time=0.3)
            out(self, t, same_err(B20), wrap=True, run_time=0.25)
            type_capture(self, t, B21, type_time=0.3)
            e21 = out(self, t, same_err(B21), wrap=True, run_time=0.25)
            vo.wait_until("each prints the same error")
            errs = VGroup(*[r for r in t.lines if r.text.startswith("error: PULUMI") or r.text == "non-interactive CLI sessions"])
            assert len(errs) >= 4 and len(e21) == 2
            self.play(Indicate(errs, color=ERR, scale_factor=1.03), run_time=0.8)
            self.add(t)

        # ========================================================== 2. b40-b42 on the local backend
        t2 = toolbox_term(9, "/app/deploy_single_vm")      # the size beat 2 shrinks to (for the layout)
        dt = default_tag().move_to([6.4, 2.45, 0], aligned_edge=RIGHT)
        c_user = chip("your OS Login user · masked", TURN, size=20).move_to([-6.3, 1.5, 0], aligned_edge=LEFT)
        c_mail = chip("the account the VM runs as", ROUTE, size=20).move_to([6.3, 1.5, 0], aligned_edge=RIGHT)
        assert c_user.get_right()[0] < c_mail.get_left()[0] - 0.3
        assert c_user.get_bottom()[1] > t2.box.get_top()[1] + 0.1 and dt.get_top()[1] < trk.get_bottom()[1] + 0.6
        assert dt.get_left()[0] > trk.get_right()[0] + 0.2 or dt.get_top()[1] < trk.get_bottom()[1] - 0.05
        with self.voiceover(SAY[2]) as vo:
            self.play(track(trk, 11, True), run_time=0.4)
            t.clear(self)
            resize(self, t, 9, run_time=0.5)
            assert abs(t.box.get_top()[1] - t2.box.get_top()[1]) < 0.02
            type_capture(self, t, B40, type_time=0.3)
            r40 = out(self, t, [B40.line(2)], run_time=0.25)[0]
            pin(self, r40, beside(extra_row(), r40), run_time=0.25)
            typed = []
            for c in B41:
                typed.append(type_capture(self, t, c, type_time=0.25)[-1])
            type_capture(self, t, B42, type_time=0.25)
            rows = out(self, t, [B42.line(2), B42.line(3), B42.line(4), (B42.line(5), ROUTE), (B42.line(6), TURN)],
                       wrap=True, run_time=0.5)
            assert [r.text for r in rows][3:] == ["security:gcp_service_account_email",
                                                  "deployment@ac215-project.iam.gserviceaccount.com",
                                                  B42.line(6)], [r.text for r in rows]
            vo.wait_until("the config shows the project")
            u_gcp = under(substring(rows[1], PROJECT_README), S.GREY, stroke=3)
            self.play(Create(u_gcp), FadeIn(dt, shift=DOWN * 0.1), run_time=0.5)
            attach(self, rows[1], u_gcp)
            vo.wait_until("your masked username")
            self.play(FadeIn(c_user, shift=DOWN * 0.1), Indicate(substring(rows[5], SA_MASK), color=TURN, scale_factor=1.06),
                      run_time=0.7)
            self.add(t)
            vo.wait_until("and the account the VM runs as")
            self.play(FadeIn(c_mail, shift=DOWN * 0.1), Indicate(rows[4], color=ROUTE, scale_factor=1.04), run_time=0.7)
            self.add(t)
            vo.wait_until("deployment at your own project")
            u_mail = under(substring(rows[4], PROJECT_README), S.GREY, stroke=3)
            unders = [u_mail]
            last_typed = rows_of(typed[2])
            for r in last_typed:
                if PROJECT_README in r.text:
                    unders.append(under(substring(r, PROJECT_README), S.GREY, stroke=3))
            self.play(*[Create(u) for u in unders], run_time=0.5)
            attach(self, rows[4], u_mail)
            for u, r in zip(unders[1:], [r for r in last_typed if PROJECT_README in r.text]):
                attach(self, r, u)
            flash_tag(self, dt, INK)
            vo.wait_until("Pause, set all three")
            yt = on_bar(t, turn_row())
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)
            vo.wait_until("and check them with pulumi config")
            self.play(Indicate(VGroup(*rows[1:]), color=INK, scale_factor=1.02), run_time=0.7)
            self.add(t)
        self.play(FadeOut(VGroup(t, dt, c_user, c_mail, yt)), run_time=0.5)
        self.remove(t, dt, c_user, c_mail, yt)

        # ========================================================== 3. __main__.py: four calls
        pm = code(MAIN, 15, 26, elide={15: "instance_ip, connection, persistent_disk, "},
                  cuts={18: "provision_instance(", 22: "configure_docker,", 26: "setup_webserver("})
        pm.move_to([0, 0, 0]).align_to([-6.4, 0, 0], LEFT).align_to([0, 2.7, 0], UP)
        steps = [(0, "3 VM"), (3, "4 Provision"), (7, "5 Containers"), (11, "6 Web server")]
        xs = pm.get_right()[0] + 0.3
        chips = []
        for k, s in steps:
            c = chip(s, TURN, size=20).move_to([xs, pm.code.code_lines[k].get_center()[1], 0], aligned_edge=LEFT)
            assert c.get_right()[0] < 6.5, (s, c.get_right())
            chips.append(c)
        assert pm.get_bottom()[1] > -3.55, pm.get_bottom()
        bars = [VGroup(line_bar(pm.code, 0, TURN, 0.2)), VGroup(line_bar(pm.code, 3, TURN, 0.2)),
                VGroup(*[line_bar(pm.code, k, TURN, 0.2) for k in (6, 7, 8)]), VGroup(line_bar(pm.code, 11, TURN, 0.2))]
        anchors = ["create the instance", "provision it", "set up the containers", "set up the web server"]
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(pm, shift=UP * 0.2), track(trk, 11), run_time=0.6)
            vo.wait_until("in the lecture's order")
            self.play(Indicate(pm.header, color=INK, scale_factor=1.05), run_time=0.6)
            for i, (bar, c, a) in enumerate(zip(bars, chips, anchors)):
                vo.wait_until(a)
                prev = [chips[i - 1].box.animate.set_stroke(S.GREY), bars[i - 1].animate.set_opacity(0.0)] if i else []
                self.play(FadeIn(bar), FadeIn(c, shift=LEFT * 0.2), *prev, run_time=0.5)
            self.wait(0.3)
            self.play(*[c.box.animate.set_stroke(OWN) for c in chips], run_time=0.5)
        self.play(FadeOut(VGroup(pm, *bars, *chips)), run_time=0.5)
        self.remove(pm, *bars, *chips)

        # ========================================================== 4. V7a: the network and its gates
        vf = VmFences()
        same = card(["same name as part 1's", "Docker network,", "now a cloud network"], size=20)
        same.move_to([4.55, 1.3, 0])
        refl = label("create_instance.py · lines 51–89", 20, S.GREY).move_to([6.4, -3.25, 0], aligned_edge=RIGHT)
        assert same.get_left()[0] > 2.4 and same.get_right()[0] < 6.5, same.get_left()
        with self.voiceover(SAY[4]) as vo:
            vf.vpc(self)
            self.play(FadeIn(refl), run_time=0.3)
            vo.wait_until("There is a cloud network")
            self.play(Indicate(vf.submobjects[-1], color=TURN, scale_factor=1.1), run_time=0.7)
            vf.heal(self)
            vo.wait_until("also called cheese app network")
            self.play(FadeIn(same, shift=LEFT * 0.2), run_time=0.5)
            self.play(Indicate(vf.frame, color=CLOUD, scale_factor=1.02), run_time=0.6)
            vf.heal(self)
            vo.wait_until("and three firewall gates")
            vf.gate(self, "80")
            vf.gate(self, "443")
            vo.wait_until("22 for every VM")
            vf.gate(self, "22")
            self.play(Indicate(vf.gates["22"].plate, color=ROUTE, scale_factor=1.15), run_time=0.6)
            vf.heal(self)

        # ========================================================== 5. disk, image lookup, the envelope
        pc = code(CREATE, 92, 103, dedent=True, cuts={99: "Ubuntu 22.04 LTS image"})
        pc.move_to([0, 0, 0]).align_to([-6.4, 0, 0], LEFT).align_to([0, 2.7, 0], UP)
        size_c = grey_chip("50 · line 36")
        size_c.move_to([pc.get_right()[0] + 0.3 + size_c.width / 2, pc.code.code_lines[3].get_center()[1], 0])
        assert size_c.get_right()[0] < 6.5, size_c.get_right()
        b_disk = span_bar(pc.code, 0, 5, CLOUD)
        b_img = span_bar(pc.code, 8, 11, TURN)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(vf), FadeOut(same), FadeOut(refl), FadeIn(pc, shift=UP * 0.2), run_time=0.6)
            self.remove(vf, same, refl)
            vo.wait_until("Then a 50 gigabyte data disk")
            self.play(FadeIn(b_disk), run_time=0.4)
            self.play(FadeIn(size_c, shift=LEFT * 0.2), run_time=0.4)
            vo.wait_until("and a lookup of the newest Ubuntu image")
            self.play(FadeIn(b_img), run_time=0.4)
            fam = code_span(pc.code, 9, '"ubuntu-2204-lts"')
            self.play(Indicate(fam, color=TURN, scale_factor=1.08), run_time=0.7)
            self.add(pc, b_disk, b_img)                  # re-seat the panel, bars on top
            vo.wait_until("The VM address is an output")
            self.play(FadeOut(VGroup(pc, b_disk, b_img, size_c)), FadeIn(vf), run_time=0.5)
            self.remove(pc, b_disk, b_img, size_c)
            vf.vm(self, run_time=0.4)
            vf.wear_tags(self, run_time=0.5)
            vf.disk(self, run_time=0.5)
            vo.wait_until("a sealed envelope")
            vf.envelope(self, run_time=0.5)
            vf.caption(self, "Output: opens when the VM exists", color=ROUTE)
            vo.wait_until("that opens once the VM exists")
            self.play(Indicate(vf.env, color=ROUTE, scale_factor=1.12), run_time=0.7)
            vf.heal(self)

        # ========================================================== 6. b43: the real preview
        t = toolbox_term(7, "/app/deploy_single_vm")
        yours = grey_chip("yours: about 30 resources")
        with self.voiceover(SAY[6]) as vo:
            parts = [m for m in vf.submobjects if m is not vf.ref]
            vf.drop(self, *parts, run_time=0.4)
            self.play(FadeIn(t, shift=UP * 0.3), track(trk, 12, True), run_time=0.5)
            plan_grid(vf, self, run_time=0.5)
            assert vf.plan.get_bottom()[1] > t.box.get_top()[1] + 0.3, (vf.plan.get_bottom(), t.box.get_top())
            assert vf.plan.get_top()[1] < trk.get_bottom()[1] - 0.2
            yours.move_to([6.3, vf.plan[5].get_center()[1], 0], aligned_edge=RIGHT)
            assert yours.get_left()[0] > vf.plan[5].get_right()[0] + 0.4
            ln = type_capture(self, t, B43, type_time=0.5)[-1]
            pin(self, ln, beside(extra_row(), ln), run_time=0.3)
            vo.wait_until("The real preview plans a disk")
            for i, n in enumerate(range(6, 11)):
                out(self, t, [(B43.line(n), OWN)], run_time=0.25)
                vf.tick(self, i, run_time=0.25)
            vo.wait_until("then stops at line 100")
            out(self, t, ["…", (B43.line(21), TURN), B43.line(22)], wrap=True, run_time=0.5)
            vo.wait_until("invalid grant")
            out(self, t, ["…", (B43.line(41), ERR)], wrap=True, run_time=0.5)
            vf.fail(self, 5)
            out(self, t, ["…", (B43.line(44), OWN), (B43.line(45), ERR)], run_time=0.5)
            vo.wait_until("the image lookup is the first call needing Google")
            self.play(Indicate(vf.plan[5], color=ERR, scale_factor=1.12), run_time=0.7)
            vf.heal(self)
            vo.wait_until("Yours goes on to about thirty resources")
            self.play(FadeIn(yours, shift=LEFT * 0.2), run_time=0.5)
            flash_tag(self, yours, INK)

        # ========================================================== 7. read the plan before -y; cost
        head = VGroup(label("check the plan before", 24, INK), mono("-y", 24, TURN)).arrange(RIGHT, buff=0.15)
        ex = mono("~ gcp:compute:Instance … replace", 22, S.GREY)
        exn = label("illustration of what to look for", 20, S.GREY)
        body = VGroup(head, ex, exn).arrange(DOWN, buff=0.22)
        frame = RoundedRectangle(width=body.width + 0.8, height=body.height + 0.6, corner_radius=0.16,
                                 stroke_color=TURN, stroke_width=3).set_fill(S.BG, 1)
        body.move_to(frame)
        plan_card = VGroup(frame, body).move_to([0, 1.25, 0])
        cost1 = cost_tag("VM n2d-standard-2 ≈ $2/day, roughly")
        cost2 = cost_tag("+ boot and data disks · external IP · check the pricing calculator")
        costs = VGroup(cost1, cost2).arrange(DOWN, buff=0.15).move_to([0, -0.55, 0])
        assert plan_card.get_bottom()[1] > costs.get_top()[1] + 0.15 and costs.get_bottom()[1] > strip_top(3) + 0.1
        assert plan_card.get_top()[1] < 2.85
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(vf), FadeOut(yours), FadeOut(t), track(trk, 12), run_time=0.4)
            self.remove(vf, yours, t)
            t = toolbox_term(3, "/app/deploy_single_vm")       # the ghost's strip, shown when it is typed
            assert costs.get_bottom()[1] > t.box.get_top()[1] + 0.1
            self.play(FadeIn(frame), FadeIn(head, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("a newer Ubuntu image")
            self.play(FadeIn(ex, shift=UP * 0.1), FadeIn(exn), run_time=0.5)
            vo.wait_until("into a VM replacement")
            self.play(Indicate(ex, color=TURN, scale_factor=1.06), run_time=0.7)
            self.add(plan_card)
            vo.wait_until("Then pause and run up")
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.3)
            g = type_cmd(self, t, B21.cmd, type_time=0.5)
            ghost_rows = rows_of(g)
            glyphs = VGroup(*[gl for r in ghost_rows for gl in glyph_range(r, 0)])
            self.play(glyphs.animate.set_color(S.GREY).set_opacity(0.55), run_time=0.3)
            self.add(t)
            yt = beside(turn_row(), ghost_rows[-1])
            pin(self, ghost_rows[-1], yt, run_time=0.3)
            flash_tag(self, yt, TURN)
            vo.wait_until("From here it costs roughly two dollars a day")
            self.play(FadeIn(cost1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("plus disks and an address")
            self.play(FadeIn(cost2, shift=UP * 0.1), run_time=0.5)
            flash_tag(self, cost1, COST)
        self.play(FadeOut(VGroup(t, plan_card, costs, trk)), run_time=0.5)
        self.remove(t, plan_card, costs, trk)

        # ========================================================== 8. step 4: provisioning, the dominoes
        ref8 = lref("14, 19")
        ss = six_steps(3)
        ss.move_to([0, 0, 0]).shift(UP * (2.95 - ss.get_top()[1]))
        nos = grey_chip("no slide draws this step")
        nos.next_to(ss.files[3], DOWN, buff=0.15)
        keep_inside(nos)
        el = EngineLoop()
        d = ProvisionDominoes()
        d.shift(DOWN * 0.4)
        assert d.get_top()[1] < nos.get_bottom()[1] + 0.6
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeIn(ref8), FadeIn(ss, shift=DOWN * 0.15), run_time=0.5)
            self.play(ss.goto(4), run_time=0.5)
            self.play(ss.light(4), run_time=0.6)
            self.add(ss)
            vo.wait_until("has no slide picture")
            self.play(FadeIn(nos, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("it happens inside the VM, over SSH")
            el.banner(self, run_time=0.4)
            el.footnote(self, run_time=0.5)
            self.play(Indicate(el.submobjects[-1], color=INK, scale_factor=1.05), run_time=0.6)
            el.heal(self)
            vo.wait_until("Nine remote commands")
            self.play(FadeOut(nos), run_time=0.2)
            self.remove(nos)
            ss.shrink_away(self, run_time=0.4)
            self.play(LaggedStart(*[FadeIn(tl, shift=DOWN * 0.15) for tl in d.tiles], lag_ratio=0.12),
                      FadeIn(d.arrows), run_time=1.0)
            self.remove(*d.tiles, d.arrows)
            self.add(d)
            vo.wait_until("format and mount the disk")
            d.fall(self, 3, per=0.3)
            vo.wait_until("update")
            d.fall(self, 6, per=0.25)
            vo.wait_until("install Docker")
            d.fall(self, 9, per=0.25)
        self.play(FadeOut(ref8), run_time=0.3)
        self.remove(ref8)

        # ========================================================== 9. blkid … || mkfs.ext4
        cap9 = label("Pulumi remembers that a command ran, not what it changed", 22, INK)
        cap9.move_to([0, -2.6, 0])
        pp = code(PROV, 24, 31, dedent=True, cuts={29: "mkfs.ext4"},
                  elide={29: "/dev/disk/by-id/google-persistent-disk-1"})
        down = DOWN * 1.65
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(el), run_time=0.3)
            self.remove(el)
            self.play(FadeIn(cap9, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("not what it changed")
            self.play(Indicate(cap9, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("Look at the first one")
            self.play(d.animate.shift(down), cap9.animate.move_to([0, 3.27, 0]), run_time=0.6)
            pp.move_to([0, 0, 0]).align_to([0, 2.99, 0], UP)
            assert pp.get_bottom()[1] > d.get_top()[1] + 0.05, (pp.get_bottom(), d.get_top())
            assert pp.get_top()[1] < cap9.get_bottom()[1] - 0.05
            self.play(FadeIn(pp, shift=UP * 0.2), Circumscribe(d.tiles[0], color=TURN, buff=0.06), run_time=0.6)
            self.add(d)
            k29 = 29 - 24
            code_span(pp.code, k29, "…", occurrence=1).set_color(S.GREY)
            b29 = line_bar(pp.code, k29, TURN, 0.28)
            vo.wait_until("block ID checks for a filesystem")
            green = code_span(pp.code, k29, "blkid -o value -s TYPE")
            ug = under(green, OWN, stroke=4)
            self.play(FadeIn(b29), green.animate.set_color(OWN), Create(ug), run_time=0.5)
            self.add(pp, b29, ug)
            vo.wait_until("and only if there is none")
            redp = code_span(pp.code, k29, "|| mkfs.ext4")
            rr = ring(redp, ERR, buff=0.06)
            self.play(Create(rr), run_time=0.5)
            vo.wait_until("make file system formats the disk")
            self.play(Indicate(redp, color=ERR, scale_factor=1.1), run_time=0.7)
            self.add(pp, b29, ug, rr)

        # ========================================================== 10. ponder
        solo = ProvisionDominoes(DOMINOES[:1], rows=(1,))
        solo.move_to(d.tiles[0])
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(pp, b29, rr, ug, cap9)), d.animate.set_opacity(0.2), run_time=0.5)
            self.remove(pp, b29, rr, ug, cap9)
            self.play(FadeIn(solo, scale=1.1), run_time=0.4)
            self.play(solo.animate.move_to([0, 2.75, 0]), run_time=0.8)
            vo.wait_until("Why check with block ID first")
            self.play(Circumscribe(solo.tiles[0], color=TURN, buff=0.08), run_time=0.7)
            solo.heal(self)
        pc_ = ponder(self, "Why blkid … || mkfs.ext4\ninstead of just mkfs.ext4?", 8, center=(0, 0.72))
        assert pc_.get_top()[1] < solo.get_bottom()[1] - 0.1 and pc_.get_bottom()[1] > d.get_top()[1] + 0.1, \
            (pc_.get_top(), pc_.get_bottom(), d.get_top())

        # ========================================================== 11. the answer: safe to run twice
        cap11 = label("scripts must be safe to run twice", 24, OWN).move_to([0, -2.75, 0])
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(pc_), FadeOut(solo), run_time=0.4)
            self.remove(pc_, solo)
            self.play(d.animate.shift(-down).set_opacity(1), run_time=0.6)
            d.heal(self)
            vo.wait_until("Because formatting erases")
            d.stand(self, run_time=0.5)
            d.disk(self, run_time=0.5)
            vo.wait_until("If this step ever ran again")
            d.refuse(self, 0)
            vo.wait_until("after a new trigger or a replaced resource")
            self.play(Wiggle(d.tiles[0], scale_value=1.08, rotation_angle=0.04 * TAU), run_time=0.8)
            d.heal(self)
            vo.wait_until("plain formatting would wipe the data disk")
            self.play(Indicate(d.disk_m[0], color=ERR, scale_factor=1.15), run_time=0.7)
            d.heal(self)
            vo.wait_until("the chat history and the model")
            d.wipe(self, run_time=1.4)
            vo.wait_until("Scripts Pulumi cannot inspect")
            self.play(Circumscribe(d.tiles[0], color=OWN, buff=0.08), run_time=0.6)
            d.heal(self)
            d.restore(self)
            self.play(FadeIn(cap11, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("must be safe to run twice")
            self.play(Indicate(cap11, color=OWN, scale_factor=1.06), run_time=0.7)
        self.play(FadeOut(VGroup(d, cap11)), run_time=0.6)
        self.remove(d, cap11)
        self.wait(0.4)
