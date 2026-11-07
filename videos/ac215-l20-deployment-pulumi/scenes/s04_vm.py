"""S04 · A VM with Docker, folders and a network (AC215 L20). TRACKER [M] 4 (beats 0-2), 5 (3-4),
6 (5-6), 7 (7), 8 (8). Lecture: 20 · 8 (beat 0 only: slide 8's stage '2 Setup VM').

Beats (script.md "## S04", one voiceover block each):
0. TRACKER [M] 4. lecture_ref(20, "8"). Slide 8's four stage chips under the top edge, '1 Push'
   GREEN, '2 Setup VM' YELLOW. A schematic console form 'Create an instance' (console_form, tag
   `illustration`, no logo): GREY 'default' rows, then one field per phrase in YELLOW: machine type
   N2D, OS and storage 50 GB, Networking ☑ Allow HTTP traffic ☑ Allow HTTPS traffic.
1. No lecture tag. The form becomes a narrower one on the left (the four YELLOW fields only). V1's
   empty BLUE VM panel ('Compute Instance (VM)') appears on the right with its disk on a cable
   ('50 GB disk'). The two ticks fly onto the VM as PINK name tags `http-server`, `https-server`; a
   dotted PINK fence 'firewall · network edge' draws itself a little outside the VM's box; two gates
   '80' and '443' open in the fence, each tied to its tag by a thin line. A GOLD cost tag 'billed
   while it runs · the disk while it exists'.
2. TRACKER [M] 4 · extra. The VM panel shrinks to the top right (a smaller VM inside its fence with
   both gates; the tags, the disk and the form leave). Full-width terminal `cheese-app-vm`; it types
   vm/00's line 1 (extra, folds) -> TERM(vm/00: 3, 4, 8, 9, 10); line 9 YELLOW with a row tag 'no
   docker yet'; a GREY chip 'stand-in for your VM' points at the corner VM.
3. TRACKER [M] 5. `curl -fsSL https://get.docker.com -o get-docker.sh` -> no output; `sudo sh
   get-docker.sh` -> TERM(vm/02: 2–3, …, 8 wrap, …, 12 wrap, …, 21, 22, 24): 'bookworm' YELLOW on
   line 8; on line 12 docker-ce, docker-buildx-plugin, docker-compose-plugin PURPLE; a GREY row tag
   on the '…' after line 12 'on a real VM, systemd starts Docker here' (not spoken). The corner VM
   gets an ORANGE layer 'Docker'.
4. `sudo docker --version` -> TERM(vm/03: 2) with 'at the time of recording' beside it; YELLOW
   '▶ your turn' beside the command.
5. TRACKER [M] 6. The terminal shrinks to a 4-row strip; the corner VM steps aside while a README
   card 'README.md · lines 53–68' shows the six bullets and the code block side by side; folder names
   YELLOW on "persistent folder …", '0777' ORANGE on "writable by anyone"; a GREY '=' between the two
   lists, then a YELLOW chip 'run them once'. The card leaves, the corner VM returns, and the six
   commands type fast (vm/10 … vm/15, no output); each mkdir drops a folder into the VM, each chmod
   turns it ORANGE.
6. TRACKER [M] 6 · extra. `ls -la` (extra) -> TERM(vm/16: 8, 10, 11): `drwxrwxrwx` ORANGE, `root
   root` YELLOW. GREY chip 'demo grade: anyone on the VM may write here'; PINK chip `$(pwd)` 'later
   mounts use the current folder'.
7. TRACKER [M] 7. `echo '<___Json Key___>' > secrets/gcp-service.json` -> no output; TRACKER [M] 7
   · extra: `cat secrets/gcp-service.json` (extra) -> TERM(vm/18: 2) YELLOW. A GREEN key
   'gcp-service.json' with a GREY-dashed 'your key text here' label, then it slides into the VM's
   secrets/ row; GREY chips 'your laptop: secrets/gcp-service.json' and 'made in part 2 if you have
   none'; a RED chip 'never commit · never show' (kept into beat 8 until the terminal shrinks).
8. TRACKER [M] 8. `sudo docker network create cheese-app-network` -> TERM(vm/19: 2) GREY (the id,
   never read). The terminal shrinks to a 3-row strip and the corner VM opens into V2
   `NamePhoneBook`: a GREEN cable `cheese-app-network` and an empty phone book 'names on this
   network'. YELLOW '▶ your turn' beside the network create line. Fade; empty frame.

Deviations from SHOW:
- Beat 1: the form cannot shrink (text never scales below 20 pt), so it is replaced by a narrower
  form holding only the four fields that matter. The disk stays outside the fence (the fence is the
  network edge; the disk is not on the network).
- Beat 2: the corner VM keeps its fence and both gates but not the tags or the disk (no room at
  >= 20 pt); the tags come back in S07.
- Beat 3: a '…' line is printed between line 8 and line 12 (lines 9-11 are skipped; the series rule
  marks every gap); line 13 and lines 14-16 sit inside the second '…'.
- Beat 5: the README card is full width (two 33-character columns at 20 pt), so the corner VM steps
  out while it is on screen and returns for the typing; the six commands type after the narration's
  last words ("from your home directory"). Folders appear in the corner VM (not in SHOW) so that the
  key of beat 7 has its secrets/ row to slide into.
- Beat 6: `$(pwd)` is shown as text inside the PINK chip (it is not in the ls output).
- Beat 7: the laptop chip is split in two ('your laptop: …' / 'made in part 2 if you have none') to
  fit beside the strip; 'S10' (SHOW's scene id) reads 'part 2' on screen, as the narration says. The
  RED 'never' chip, the only on-screen key warning, stays through beat 8's `network create` and
  leaves when the terminal shrinks (whole-video QA: it was on screen for about 1 s).
- Beats 1-2 (whole-video QA, follow-along): a YELLOW '▶ your turn' sits on the small form for all of
  beat 1 (creating the VM is the viewer's job), and on "SSH in" a GREY chip 'VM instances list · SSH
  button' says how (README:46 says only "SSH into the VM"). The narration has no pause line here
  yet (script.md owns it).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ the real sources (checked)
V00, V01, V02, V03 = capture("vm/00"), capture("vm/01"), capture("vm/02"), capture("vm/03")
FOLDERS = [capture(f"vm/{n}") for n in range(10, 16)]
V16, V17, V18, V19 = capture("vm/16"), capture("vm/17"), capture("vm/18"), capture("vm/19")

assert V00.cmd.startswith("date -u ") and V00.cmd.endswith("; pwd"), V00.cmd
assert V00.line(3) == "cheese-app-vm" and "bookworm" in V00.line(4), V00.at(3, 4)
assert V00.line(8) == "x86_64" and V00.line(9) == "which-docker-exit:1" and V00.line(10) == "/home/student"
assert V01.cmd == "curl -fsSL https://get.docker.com -o get-docker.sh" and not V01.lines, V01.lines
assert V02.cmd == "sudo sh get-docker.sh", V02.cmd
assert V02.line(2).startswith("# Executing docker install script")
assert "bookworm stable" in V02.line(8), V02.line(8)
for pkg in ("docker-ce ", "docker-compose-plugin", "docker-buildx-plugin"):
    assert pkg in V02.line(12), (pkg, V02.line(12))
assert V02.line(14).startswith("Using systemd") and "unable to enable" in V02.line(16)
assert V02.line(21).startswith("To run Docker as a non-privileged user") and V02.line(23) == ""
assert V02.line(24).strip() == "dockerd-rootless-setuptool.sh install", V02.line(24)
assert V03.cmd == "sudo docker --version" and V03.line(2).startswith("Docker version 29.9.3")
FOLDER_CMDS = ("sudo mkdir persistent-folder", "sudo mkdir secrets", "sudo mkdir -p conf/nginx",
               "sudo chmod 0777 persistent-folder", "sudo chmod 0777 secrets", "sudo chmod -R 0777 conf")
for c, cmd in zip(FOLDERS, FOLDER_CMDS):
    assert c.cmd == cmd and not c.lines, (c.cmd, c.lines)
for i, n in enumerate(range(54, 60)):
    assert readme(n).strip() == f"* `{FOLDER_CMDS[i]}`", readme(n)
for i, n in enumerate(range(62, 68)):
    assert readme(n).strip() == FOLDER_CMDS[i], readme(n)
assert readme(53).strip() == "#### Create folders and give permissions"
assert V16.cmd == "ls -la"
for n, name in ((8, "conf"), (10, "persistent-folder"), (11, "secrets")):
    assert V16.line(n).startswith("drwxrwxrwx") and "root    root" in V16.line(n) and V16.line(n).endswith(name)
assert V17.cmd == "echo '<___Json Key___>' > secrets/gcp-service.json" and not V17.lines
assert V18.cmd == "cat secrets/gcp-service.json" and V18.line(2) == "<___Json Key___>"
assert V19.cmd == "sudo docker network create cheese-app-network"
assert re.fullmatch(r"[0-9a-f]{64}", V19.line(2)), V19.line(2)

# ------------------------------------------------------------------ the corner VM (beats 2-8)
CV_C = np.array([4.15, 2.02, 0])          # the corner VM's centre: frame x 1.95 .. 6.35, y 0.92 .. 3.12
CV_W, CV_H = 4.4, 2.2
FOLDER_Y = (2.45, 2.03, 1.61)             # persistent-folder/, secrets/, conf/nginx/
FOLDER_NAMES = ("persistent-folder/", "secrets/", "conf/nginx/")


def _cv_fence(w: float, h: float) -> VMobject:
    r = RoundedRectangle(width=w, height=h, corner_radius=0.18)
    return DashedVMobject(r, num_dashes=max(20, int((w + h) * 9)), dashed_ratio=0.4).set_stroke(ROUTE, 2.5)


def corner_vm() -> VGroup:
    """The small VM top right: BLUE frame, mono title, dotted PINK fence, gates 80 / 443 on the
    fence's left edge. .frame .title .fence .gates"""
    fr = RoundedRectangle(width=CV_W, height=CV_H, corner_radius=0.14, stroke_color=CLOUD,
                          stroke_width=3).set_fill(tint(CLOUD, 0.05), 1).move_to(CV_C)
    tt = mono(T_VM, 20, CLOUD).move_to([2.35, 2.88, 0], aligned_edge=LEFT)
    fe = _cv_fence(CV_W + 0.28, CV_H + 0.26).move_to(CV_C)
    g80 = door("80", door_w=0.62).move_to([fe.get_left()[0], 2.55, 0])
    g443 = door("443", door_w=0.72).move_to([fe.get_left()[0], 1.55, 0])
    g = VGroup(fe, fr, tt, g80, g443)
    g.frame, g.title, g.fence, g.gates = fr, tt, fe, VGroup(g80, g443)
    return g


def folder_row(i: int, color=INK) -> VGroup:
    gl = folder_icon(0.26, color)
    t = mono(FOLDER_NAMES[i], 20, color)
    g = VGroup(gl, t).arrange(RIGHT, buff=0.14)
    g.move_to([2.4, FOLDER_Y[i], 0], aligned_edge=LEFT)
    g.glyph, g.text = gl, t
    return g


def docker_layer() -> VGroup:
    b = RoundedRectangle(width=CV_W - 0.3, height=0.34, corner_radius=0.08, stroke_color=SHARED,
                         stroke_width=3).set_fill(tint(SHARED, 0.22), 1).move_to([CV_C[0], 1.15, 0])
    t = label("Docker", 20, INK).move_to(b)
    return VGroup(b, t)


def vm_form(fields, **kw) -> VGroup:
    """console_form with the second Networking tick under the first one (its label is empty)."""
    f = console_form("Create an instance", fields, **kw)
    for i, r in enumerate(f.rows):
        if i and not fields[i][0]:
            r.value.align_to(f.rows[i - 1].value, LEFT)
    return f


def folder_card() -> VGroup:
    """README:53-68: the six bullets and the code block side by side. .left .right .eq .mk .chm"""
    left_rows = VGroup()
    for c in FOLDER_CMDS:
        d = Dot(radius=0.04, color=INK)
        t = mono_line(c, 20, INK)
        left_rows.add(VGroup(d, t).arrange(RIGHT, buff=0.1))
    left_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    head = label("Create folders and give permissions", 20, INK)
    left = VGroup(head, left_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    right_rows = VGroup(*[mono_line(c, 20, INK) for c in FOLDER_CMDS]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    rb = RoundedRectangle(width=right_rows.width + 0.2, height=right_rows.height + 0.24, corner_radius=0.08,
                          stroke_color=S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1)
    rb.move_to(right_rows)
    right = VGroup(rb, right_rows)
    eq = label("=", 36, S.GREY)
    body = VGroup(left, eq, right).arrange(RIGHT, buff=0.18)
    right.align_to(left_rows, DOWN)
    eq.move_to([eq.get_center()[0], left_rows.get_center()[1], 0])
    c = readme_card((53, 68), body)
    c.left, c.right, c.eq, c.lrows, c.rrows = left, right, eq, left_rows, right_rows
    return c


class VmWithDocker(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S04"] == 9, len(SAY)

        # ========================================================== 0. stage 2: create the VM
        trk = tracker_m(4)
        ref8 = lref("8")
        stages = VGroup(*[chip(s, S.GREY, size=20) for s in STAGES_MANUAL]).arrange(RIGHT, buff=0.25)
        stages.move_to([0, 2.3, 0])
        assert stages.get_top()[1] < TRACK_BOTTOM - 0.1 and stages.get_left()[0] > -6.5
        fields = [("Name · region · zone", "default", S.GREY),
                  ("Machine type", "N2D", TURN),
                  ("OS and storage", "disk size 50 GB", TURN),
                  ("Networking", "☑ Allow HTTP traffic", TURN),
                  ("", "☑ Allow HTTPS traffic", TURN),
                  ("Everything else", "default", S.GREY)]
        form = vm_form(fields)
        form.move_to([0, -0.75, 0])
        assert form.get_top()[1] < stages.get_bottom()[1] - 0.2 and form.get_bottom()[1] > -3.5
        vals = [r.value for r in form.rows]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref8), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in stages], lag_ratio=0.15), run_time=0.6)
            self.play(stages[0].box.animate.set_stroke(OWN, width=3), stages[1].box.animate.set_stroke(TURN, width=4),
                      run_time=0.4)
            self.play(Indicate(stages[1].text, color=TURN, scale_factor=1.15), run_time=0.6)
            self.add(stages)
            vo.wait_until("In the console")
            self.play(FadeIn(form.frame), FadeIn(form.title), FadeIn(form.tag),
                      *[FadeIn(r.label) for r in form.rows], run_time=0.6)
            vo.wait_until("with the defaults")
            self.play(FadeIn(vals[0], shift=RIGHT * 0.1), FadeIn(vals[5], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("except machine type")
            self.play(Write(vals[1]), run_time=0.5)
            vo.wait_until("a 50 gigabyte disk")
            self.play(Write(vals[2]), run_time=0.6)
            vo.wait_until("and HTTP and HTTPS allowed")
            self.play(Write(vals[3]), run_time=0.5)
            self.play(Write(vals[4]), run_time=0.5)
            self.remove(*vals)
            self.add(form)

        # ========================================================== 1. two ticks = two tags; the fence
        small = vm_form(fields[1:5], form_w=5.6)
        small.move_to([-6.45 + small.width / 2, 0.55, 0])
        md = MasterDiagram(manual=True)
        md.shift(UP * 0.55)
        fence = _cv_fence(6.2, 3.85)
        fence.move_to([3.4, -0.075, 0])
        cyl = disk_cyl(0.6).move_to([3.85, -2.62, 0])
        dk = VGroup(Line([3.85, -1.85, 0], cyl.get_top(), color=CLOUD, stroke_width=4), cyl,
                    label("50 GB disk", 20, INK).next_to(cyl, RIGHT, buff=0.2))
        assert cyl.get_top()[1] < fence.get_bottom()[1] - 0.1, (cyl.get_top(), fence.get_bottom())
        assert fence.get_right()[0] < 6.55, fence.get_right()
        fence_t = label("firewall · network edge", 20, ROUTE)
        fence_t.move_to([fence.get_left()[0] + 0.15, fence.get_top()[1] + 0.25, 0], aligned_edge=LEFT)
        assert fence_t.get_top()[1] < PIC_TOP, fence_t.get_top()
        t_http = route_chip("http-server").move_to([1.1, 0.75, 0], aligned_edge=LEFT)
        t_https = route_chip("https-server").move_to([1.1, -0.2, 0], aligned_edge=LEFT)
        x_f = fence.get_left()[0]
        gate80 = door("80", door_w=0.62).move_to([x_f, 0.75, 0])
        gate443 = door("443", door_w=0.72).move_to([x_f, -0.2, 0])
        ties = VGroup(Line(gate80.get_right(), t_http.get_left(), color=ROUTE, stroke_width=2),
                      Line(gate443.get_right(), t_https.get_left(), color=ROUTE, stroke_width=2))
        cost = cost_tag("billed while it runs · the disk while it exists")
        cost.move_to([-6.45 + cost.width / 2, -3.15, 0])
        assert small.get_right()[0] < gate80.get_left()[0] - 0.2, (small.get_right(), gate80.get_left())
        yt_form = your_turn().next_to(small.frame, UP, buff=0.12).align_to(small.frame, LEFT).shift(RIGHT * 0.2)
        assert yt_form.get_top()[1] < TRACK_BOTTOM - 0.05, yt_form.get_top()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(stages, ref8)), run_time=0.4)
            self.remove(stages, ref8)
            self.play(ReplacementTransform(form, small), run_time=0.7)
            self.play(FadeIn(yt_form, shift=DOWN * 0.1), run_time=0.4)
            flash_tag(self, yt_form, TURN)
            md.vm(self)
            self.play(Create(dk[0]), FadeIn(dk[1:], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Those two ticks add network tags")
            tick1, tick2 = small.rows[2].value.copy(), small.rows[3].value.copy()
            self.add(tick1, tick2)
            self.play(ReplacementTransform(tick1, t_http), run_time=0.7)
            self.play(ReplacementTransform(tick2, t_https), run_time=0.7)
            vo.wait_until("http server and https server")
            self.play(Indicate(t_http.text, color=ROUTE, scale_factor=1.12), run_time=0.5)
            self.play(Indicate(t_https.text, color=ROUTE, scale_factor=1.12), run_time=0.5)
            vo.wait_until("the default firewall opens 80 and 443")
            self.play(Create(fence), FadeIn(fence_t), run_time=0.9)
            self.play(GrowFromCenter(gate80), GrowFromCenter(gate443), run_time=0.5)
            vo.wait_until("only to VMs with them")
            self.play(Create(ties), run_time=0.5)
            self.play(Indicate(gate80.text, color=ROUTE, scale_factor=1.25),
                      Indicate(gate443.text, color=ROUTE, scale_factor=1.25), run_time=0.6)
            vo.wait_until("The VM now bills while it runs")
            self.play(FadeIn(cost, shift=UP * 0.15), run_time=0.5)
            self.play(md.light("vm", COST), run_time=0.4)
            vo.wait_until("its disk while it exists")
            self.play(dk[1][-1].animate.set_stroke(COST), dk[1][2].animate.set_stroke(COST),
                      dk[1][3].animate.set_stroke(COST), Indicate(dk[2], color=COST, scale_factor=1.1), run_time=0.6)
            self.add(dk)

        # ========================================================== 2. SSH in: the stand-in
        cv = Piece()
        cvm = corner_vm()
        t = vm_term(rows=8)
        assert t.box.get_top()[1] < cvm.fence.get_bottom()[1] - 0.1, (t.box.get_top(), cvm.fence.get_bottom())
        stand = grey_chip("stand-in for your VM")
        stand.move_to([0.0, 2.2, 0])
        stand_ar = arrow(stand.get_right() + RIGHT * 0.05, cvm.fence.get_left() + np.array([0, 0.15, 0]) + LEFT * 0.42,
                         S.GREY, stroke=3, buff=0)
        ssh = grey_chip("VM instances list · SSH button")
        ssh.move_to([-6.45 + ssh.width / 2, 1.45, 0])
        assert ssh.get_bottom()[1] > t.box.get_top()[1] + 0.1, (ssh.get_bottom(), t.box.get_top())
        assert ssh.get_right()[0] < cvm.fence.get_left()[0] - 0.5, ssh.get_right()
        with self.voiceover(SAY[2]) as vo:
            vm_part, disk_part = md.parts["vm"], dk
            self.remove(md)
            self.add(vm_part, disk_part, fence, gate80, gate443)
            self.play(FadeOut(VGroup(small, yt_form, t_http, t_https, ties, cost, fence_t, disk_part)),
                      track(trk, 4, True), run_time=0.5)
            self.play(ReplacementTransform(vm_part.frame, cvm.frame), ReplacementTransform(vm_part.title, cvm.title),
                      ReplacementTransform(fence, cvm.fence), ReplacementTransform(gate80, cvm.gates[0]),
                      ReplacementTransform(gate443, cvm.gates[1]), run_time=0.8)
            self.remove(*cvm.get_family(), vm_part, fence, gate80, gate443)
            cv.add(cvm)
            self.add(cv)
            self.play(FadeIn(t, shift=UP * 0.3), FadeIn(ssh, shift=RIGHT * 0.2), run_time=0.4)
            ln = type_capture(self, t, V00, type_time=0.9)[0]
            et = on_bar(t, extra_row())
            self.play(FadeIn(et), run_time=0.3)
            vo.wait_until("Our VM is a stand-in")
            rows = out(self, t, V00.at(3, 4, 8, 9, 10), run_time=0.6)
            self.play(FadeIn(stand, shift=RIGHT * 0.2), GrowArrow(stand_ar), run_time=0.5)
            self.play(Indicate(rows[0], color=CLOUD, scale_factor=1.05), run_time=0.6)
            self.add(t)
            vo.wait_until("a fresh Debian 12 machine")
            self.play(Indicate(substring(rows[1], "Debian GNU/Linux 12 (bookworm)"), color=INK, scale_factor=1.06),
                      run_time=0.6)
            self.add(t)
            vo.wait_until("without Docker")
            self.play(rows[3].animate.set_color(TURN), run_time=0.4)
            nd = beside(row_tag("no docker yet", TURN), rows[3])
            pin(self, rows[3], nd)
            vo.wait_until("Every command is the same on yours")
            self.play(Indicate(stand.text, color=INK, scale_factor=1.08), run_time=0.6)

        # ========================================================== 3. install Docker
        dl = docker_layer()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(stand, stand_ar, et, ssh)), track(trk, 5), run_time=0.5)
            self.remove(stand, stand_ar, et, ssh)
            vo.wait_until("download it with curl")
            type_capture(self, t, V01, type_time=0.8)
            bare_prompt(self, t)
            vo.wait_until("run it with sudo")
            type_capture(self, t, V02, type_time=0.5)
            out(self, t, V02.at((2, 3), "…"), wrap=True, run_time=0.5)
            vo.wait_until("It adds the Docker repository")
            r8 = out(self, t, [V02.line(8)], wrap=True, run_time=0.5)
            vo.wait_until("for bookworm")
            bw = next(r for r in r8 if "bookworm" in r.text)
            self.play(substring(bw, "bookworm").animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(substring(bw, "bookworm"), color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(t)
            vo.wait_until("and installs the engine")
            r12 = out(self, t, ["…", V02.line(12)], wrap=True, run_time=0.5)
            pk = [substring(r, s) for s in ("docker-ce ", "docker-buildx-plugin", "docker-compose-plugin")
                  for r in r12 if s in r.text]
            self.play(*[p.animate.set_color(TOOL) for p in pk], run_time=0.4)
            self.add(t)
            cv.show(self, dl, anims=[FadeIn(dl, shift=UP * 0.15)], run_time=0.5)
            vo.wait_until("buildx and compose")
            self.play(*[Indicate(p, color=TOOL, scale_factor=1.1) for p in pk[1:]], run_time=0.6)
            self.add(t)
            tail = out(self, t, ["…", *V02.at(21, 22, 24)], run_time=0.5)
            sd = beside(row_tag("on a real VM, systemd starts Docker here"), tail[0])
            pin(self, tail[0], sd)

        # ========================================================== 4. check the version; your turn
        with self.voiceover(SAY[4]) as vo:
            vo.wait_until("Then check it")
            ver = type_capture(self, t, V03, type_time=0.6)[0]
            vr = out(self, t, V03.at(2), run_time=0.4)
            tr = beside(time_row(), vr[0])
            pin(self, vr[0], tr)
            self.play(Indicate(substring(vr[0], "29.9.3"), color=INK, scale_factor=1.2), run_time=0.6)
            self.add(t)
            vo.wait_until("Pause here")
            yt = beside(turn_row(), ver)
            pin(self, ver, yt)
            flash_tag(self, yt, TURN)
            self.add(t)

        # ========================================================== 5. folders: six commands, run once
        fc = folder_card()
        fc.move_to([0, 0.85, 0])
        assert fc.get_left()[0] > -6.55 and fc.get_right()[0] < 6.55, (fc.get_left(), fc.get_right())
        assert fc.get_top()[1] < TRACK_BOTTOM - 0.05, fc.get_top()
        once = chip("run them once", TURN, size=20)
        once.move_to([fc.frame.get_right()[0] - 0.25 - once.width / 2, fc.head.get_center()[1], 0])
        rr = ring(fc.right, S.GREY, buff=0.06)
        with self.voiceover(SAY[5]) as vo:
            self.play(track(trk, 6), run_time=0.4)
            resize(self, t, 4, keep=0, run_time=0.6)
            assert fc.get_bottom()[1] > t.box.get_top()[1] + 0.1, (fc.get_bottom(), t.box.get_top())
            self.play(FadeOut(cv, shift=RIGHT * 0.4), run_time=0.4)
            self.remove(cv)
            self.play(FadeIn(fc.frame), FadeIn(fc.head), FadeIn(fc.left), run_time=0.6)
            vo.wait_until("persistent folder, secrets and conf nginx")
            names = [substring(fc.lrows[i][1], n) for i, n in enumerate(("persistent-folder", "secrets", "conf/nginx"))]
            for nm in names:
                self.play(nm.animate.set_color(TURN), run_time=0.3)
            vo.wait_until("writable by anyone")
            perms = [substring(fc.lrows[i][1], "0777") for i in (3, 4, 5)]
            self.play(*[p.animate.set_color(SHARED) for p in perms], run_time=0.4)
            self.play(*[Indicate(p, color=SHARED, scale_factor=1.15) for p in perms], run_time=0.6)
            self.add(fc)
            vo.wait_until("The README lists these six commands twice")
            self.play(FadeIn(fc.right, shift=LEFT * 0.2), run_time=0.5)
            self.play(FadeIn(fc.eq, scale=1.4), Create(rr), run_time=0.5)
            vo.wait_until("run them once")
            self.play(FadeIn(once, scale=0.9), run_time=0.4)
            flash_tag(self, once, TURN)
            self.play(FadeOut(VGroup(fc, rr, once)), FadeIn(cv, shift=LEFT * 0.4), run_time=0.4)
            self.remove(fc, rr, once)
            self.add(cv)
            frows = []
            for i, c in enumerate(FOLDERS):
                type_capture(self, t, c, type_time=0.22)
                if i < 3:
                    frows.append(cv.show(self, folder_row(i), anims=None, run_time=0.2))
                else:
                    f = frows[i - 3]
                    self.play(f.animate.set_color(SHARED), run_time=0.2)
                    cv.heal(self)
            bare_prompt(self, t)

        # ========================================================== 6. ls -la (extra): root, but 0777
        demo = grey_chip("demo grade: anyone on the VM may write here")
        demo.move_to([-6.45 + demo.width / 2, 1.9, 0])
        pwd = VGroup(mono("$(pwd)", 20, ROUTE), label("later mounts use the current folder", 20, ROUTE))
        pwd.arrange(RIGHT, buff=0.2)
        pwd_b = RoundedRectangle(width=pwd.width + 0.48, height=pwd.height + 0.26, corner_radius=0.14,
                                 stroke_color=ROUTE, stroke_width=2).set_fill(tint(ROUTE, 0.12), 1)
        pwd.move_to(pwd_b)
        pwd_c = VGroup(pwd_b, pwd)
        pwd_c.move_to([-6.45 + pwd_c.width / 2, 0.6, 0])
        assert demo.get_right()[0] < cvm.fence.get_left()[0] - 0.5 and pwd_c.get_right()[0] < cvm.fence.get_left()[0] - 0.2
        with self.voiceover(SAY[6]) as vo:
            self.play(track(trk, 6, True), run_time=0.4)
            ls = type_capture(self, t, V16, type_time=0.4)[0]
            pin(self, ls, beside(extra_row(), ls))
            lsr = out(self, t, V16.at(8, 10, 11), run_time=0.5)
            vo.wait_until("the folders belong to root")
            self.play(*[substring(r, "root    root").animate.set_color(TURN) for r in lsr], run_time=0.4)
            self.add(t)
            vo.wait_until("but anyone may write there")
            self.play(*[substring(r, "drwxrwxrwx").animate.set_color(SHARED) for r in lsr], run_time=0.4)
            self.play(*[Indicate(substring(r, "drwxrwxrwx"), color=SHARED, scale_factor=1.1) for r in lsr],
                      run_time=0.6)
            self.add(t)
            vo.wait_until("fine for a demo VM only")
            self.play(FadeIn(demo, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("Stay in your home directory")
            self.play(FadeIn(pwd_c, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("later mounts use the current folder")
            self.play(Indicate(pwd[0], color=ROUTE, scale_factor=1.2), run_time=0.6)

        # ========================================================== 7. the app's key
        key = key_icon("service", name=True)
        key.move_to([-5.4, 2.05, 0])
        dash_l = dashed_chip("your key text here")
        dash_l.next_to(key, RIGHT, buff=0.35)
        lap1 = grey_chip("your laptop: secrets/gcp-service.json")
        lap2 = grey_chip("made in part 2 if you have none")
        VGroup(lap1, lap2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-6.45, 0.45, 0], aligned_edge=LEFT)
        never = chip("never commit · never show", ERR, size=20, fill_opacity=0.14)
        never.move_to([-6.45 + never.width / 2, -0.6, 0])
        assert lap1.get_right()[0] < cvm.fence.get_left()[0] - 0.4 and never.get_bottom()[1] > -0.95
        assert lap1.get_top()[1] < key.get_bottom()[1] - 0.2, (lap1.get_top(), key.get_bottom())
        key_dst = key.glyph.copy().move_to([4.75, FOLDER_Y[1], 0])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(demo, pwd_c)), track(trk, 7), run_time=0.5)
            self.remove(demo, pwd_c)
            echo = type_capture(self, t, V17, type_time=0.8)[0]
            self.play(Indicate(substring(rows_of(echo)[-1], "secrets/gcp-service.json"), color=TURN,
                               scale_factor=1.06), run_time=0.6)
            self.add(t)
            vo.wait_until("ours holds just the placeholder")
            self.play(track(trk, 7, True), run_time=0.4)
            ct = type_capture(self, t, V18, type_time=0.4)[0]
            pin(self, ct, beside(extra_row(), ct))
            cr = out(self, t, [(V18.line(2), TURN)], run_time=0.4)
            self.play(FadeIn(key, scale=0.9), FadeIn(dash_l, shift=LEFT * 0.2), run_time=0.5)
            self.play(Indicate(cr[0], color=TURN, scale_factor=1.06), run_time=0.5)
            self.add(t)
            vo.wait_until("Paste in the gcp service key")
            self.play(FadeIn(lap1, shift=RIGHT * 0.2), run_time=0.4)
            moving = key.glyph
            key.remove(moving)
            self.add(moving)
            self.play(moving.animate.move_to(key_dst), FadeOut(key.text), FadeOut(dash_l), run_time=0.8)
            self.remove(key, key.text, dash_l, moving)
            cv.add(moving)
            self.add(cv)
            self.play(Indicate(moving, color=OWN, scale_factor=1.3), run_time=0.6)
            cv.heal(self)
            vo.wait_until("part 2 shows how to make one")
            self.play(FadeIn(lap2, shift=RIGHT * 0.2), run_time=0.4)
            vo.wait_until("Never show or commit it")
            self.play(FadeIn(never, scale=0.9), run_time=0.4)
            flash_tag(self, never, ERR)

        # ========================================================== 8. the Docker network
        nb = NamePhoneBook()
        nb.shift(UP * 0.36)
        nb.cable.shift(UP * 0.36)            # built in __init__ but not members until cable_on()
        nb.book.shift(UP * 0.36)
        assert nb.title.get_top()[1] < TRACK_BOTTOM - 0.05, nb.title.get_top()
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(lap1, lap2)), track(trk, 8), run_time=0.5)
            self.remove(lap1, lap2)
            net = type_capture(self, t, V19, type_time=0.6)[0]
            idr = out(self, t, [(V19.line(2), S.GREY)], run_time=0.4)
            vo.wait_until("a private network")
            self.play(FadeOut(never), run_time=0.3)
            self.remove(never)
            resize(self, t, 3, keep=[*rows_of(net), idr[0]] if hasattr(net, "rows") else [net, idr[0]],
                   run_time=0.5)
            assert nb.vm.get_bottom()[1] > t.box.get_top()[1] + 0.1, (nb.vm.get_bottom(), t.box.get_top())
            cvm_ = cv.submobjects[0]
            self.remove(cv)
            rest = [m for m in cv.submobjects if m is not cvm_] + [cvm_.fence, cvm_.gates]
            self.add(*cv.submobjects)
            self.play(ReplacementTransform(cvm_.frame, nb.vm), ReplacementTransform(cvm_.title, nb.title),
                      *[FadeOut(m) for m in rest], run_time=0.8)
            self.remove(*[m for m in cv.get_family()])
            self.add(nb)
            nb.cable_on(self)
            vo.wait_until("find each other by name")
            self.play(Indicate(nb.book[1], color=OWN, scale_factor=1.08), run_time=0.6)
            nb.heal(self)
            vo.wait_until("Pause and run these three steps")
            yt2 = beside(turn_row(), net)
            pin(self, net, yt2)
            flash_tag(self, yt2, TURN)
            self.add(t)

        self.play(FadeOut(VGroup(trk, t, nb)), run_time=0.6)
        self.remove(trk, t, nb)
        self.wait(0.3)
