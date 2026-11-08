"""S08 · Create a server, then provision it — tracker B 6 → 7 → 9 (early) → 8 (README 92–111).
No lecture tag (script.md has no LECTURE mark in S08). V4 PlayCard, V7 VmLayout, V3's badge glyph.

Beats (script.md "## S08"; one voiceover block each):
0. TRACKER B 6. The create play card (deploy-create-instance.yml, 9 tasks from laptop/37: 43–51,
   hosts: localhost; "Remove EBS volume" GREY dashed, sub-line "when: absent") on the left, the
   TEAL toolbox and the BLUE "AWS · us-east-1" box on the right with a PINK API arrow. On "First,
   a security group" the card folds into a one-tile task strip at the top ("task n/9 · name") and
   the toolbox moves left; each task fires a PINK API call from the toolbox: V7's security-group
   wall (doors 22, 80, 443, ORANGE 0.0.0.0/0), a GREEN 50 GB disk "us-east-1a" outside; the AWS
   box becomes V7's EC2 box (t2.large), the WHITE key glyph on door 22, two GREEN disks inside
   ("100 GB root", "100 GB · /dev/sdf", chip "deleted with the instance"); a PINK SSH arrow waits
   (GREY chip "times out after 120 s? your network may block port 22"); the 50 GB disk moves
   toward the box and stops at a GREY dashed outline just outside the wall (not attached), GREY dashed
   note "untested: …" (kept into block 1 until "its disks"); the strip's
   tile 7 "Remove EBS volume" is GREY dashed ("when: absent").
1. TRACKER B 6. Three GOLD cost tags by the box (instance on top; disks and public IPv4 under it)
   and a GOLD CostDial right of the box that starts ticking.
2. TRACKER B 6. ▶ your turn. Toolbox terminal (prompt laptop/42: 35) types README 94 (folded) →
   TBX(42: 39, 41, 42, 44, 45 wrap, its generic "An exception occurred … The error was:" head
   cropped to "…"): ok GREEN, line 45 RED; V4 PlayRecap from line 49 (ok=1,
   failed=1 RED). On "With real keys" the terminal shrinks to a 3-row strip (line 45's last rows)
   and a GREY dashed "not tested" note sits above it over a dashed tile "Attach EBS volume to
   instance".
3. TRACKER B 6. README(92) card, "in GCP" underlined, erratum tag "it's an EC2 instance · carried
   over from the GCP README".
4. TRACKER B 7. ▶ your turn. CONSOLE("EC2 › Instances"; running instance chip, Public IPv4 address
   <EXTERNAL_IP>); the address copy flies down into a 4-row laptop strip (P_LAPTOP; GREY chip
   "second laptop terminal · …"); on "into the inventory" the console leaves and the strip grows to
   7 rows (command + output together), which types laptop/43 line 1 (row tag "sed is our editor") and
   prints 43: 2–5; EXTERNAL_IP: YELLOW + GREY chip "placeholder: we have no server".
5. TRACKER B 9 (shown early). ▶ your turn. README(107–111) card + erratum tag "README order: do
   step 9 before step 8"; the card folds into a chip (top left) and S04's YELLOW bookmark
   "remember both" returns beside it and flashes; the strip grows to 8 rows and types laptop/45
   line 1 (extra) → 45: 3, 5–6 (wrapped): line 3 GREY, line 6 GREEN, `/secrets/ac215_2024.pem`
   YELLOW + GREY chip "the file in ~/secrets must be named ac215_2024.pem"; line 3's key path
   flashes on the last sentence.
6. TRACKER B 8. ▶ your turn. Toolbox terminal (prompt laptop/44: 35) types README 102 →
   TBX(44: 39, 41, 42 msg) RED; PlayRecap from line 45 (unreachable=1 RED). On "On yours" it
   shrinks to a 3-row strip (the UNREACHABLE lines); above: the toolbox, a PINK SSH arrow
   "ubuntu + your key" ending at a RED "?" in a GREY dashed server outline; on "Host key checking"
   a GREY mono chip "ansible.cfg:2  host_key_checking = False" + tag "trade-off".
7. TRACKER B 8. No terminal. Left: the provision play card (deploy-provision-instance.yml,
   "Configure app server instance", hosts: appserver) with 38 text-free task tiles (laptop/37:
   81–118) that collapse into four GREEN group labels in one column, GREY caption "what success
   looks like · schematic"; right: a V7 server (shifted right). "Docker CE" → V7's Docker label;
   "format + mount /mnt/disk-1" → the GREEN disk /dev/xvdf docks to the folder /mnt/disk-1;
   "AWS CLI v2"; "aws configure" → CODE(deploy-provision-instance.yml: 288–292) replaces the column
   for ~2 s, then leaves; the WHITE badge glyph lands on the server, GREY counter "badge · copy 1
   on the server". Fade; empty frame.

Deviations from SHOW: block 0 cannot hold the nine-tile card next to V7 (V7 is 7.0 wide plus the
wall's chips at 20 pt), so the card is shown on the first sentence and then folds into a one-tile
task strip that steps through the tasks as the API calls fire (tasks 4, 5, 8 and 9 are passed on
the strip without narration). The 50 GB disk's "pinned to us-east-1a" sits under it as its zone
label; the untested-attach and SSH-timeout notes are GREY chips in the band under the box, one at
a time. Block 1's three cost tags stand above and under the box, not "beside" it (no room at the
side). Block 4 grows the strip to 7 rows, not 3, once the console has left: the sed command folds onto
3 rows and must stay on screen with the four output lines. Block 5 first shrinks it back to 4 rows
(the output) so the README card fits above it. Block 5 grows the strip to 8 rows after the README card folds away (the
command folds onto 3 rows; lines 3 and 6 wrap). Block 6 draws the SSH arrow on its own small
picture (toolbox → dashed server with a RED "?") rather than V7, which is not on screen there.
Block 2 crops line 45's generic head ("An exception occurred during task execution. To see the full
traceback, use -vvv. The error was: ") to "…" so the PlayRecap fits inside a 12-row terminal; the
ClientError and the AuthFailure text are kept whole. Block 7's 38 tasks are text-free tiles (38 names at 20 pt cannot fit), and the badge counter is a
GREY note (V3's KeyJourney is not on screen in this scene).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S08"]

CI = "src/deployment/deploy-create-instance.yml"
PV = "src/deployment/deploy-provision-instance.yml"
X42, X44 = toolbox_capture("42"), toolbox_capture("44")
C43, C45 = capture("43"), capture("45")
CMD6, CMD8 = readme(94), readme(102)

# ------------------------------------------------------------------ the real sources (checked)
assert X42.cmd == CMD6 == "ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=present"
assert X44.cmd == CMD8 == "ansible-playbook deploy-provision-instance.yml -i inventory.yml"
assert readme(92) == "#### Create Compute Instance (VM) Server in GCP"
CTASKS = task_names("deploy-create-instance.yml")
assert len(CTASKS) == 9 and CTASKS[5] == "Attach EBS volume to instance" and CTASKS[6] == "Remove EBS volume"
PTASKS = task_names("deploy-provision-instance.yml")
assert len(PTASKS) == 38 and PTASKS[15] == "Install Docker" and PTASKS[16].startswith("Format EBS volume")
assert PTASKS[18] == "Mount EBS volume" and PTASKS[26] == "Install dependencies for AWS CLI"
assert PTASKS[35] == "Clean up AWS CLI installer" and PTASKS[36] == "Configure AWS credentials"
assert excerpt(CI, 14, 14).strip() == "ports: 80" and excerpt(CI, 20, 20).strip() == "ports: 22"
assert excerpt(CI, 15, 15).strip() == "cidr_ip: 0.0.0.0/0"
assert excerpt(CI, 30, 30).strip() == 'zone: "{{ aws_region }}a"'
assert excerpt(CI, 53, 53).strip() == "- device_name: /dev/sdf" and excerpt(CI, 90, 90).strip() == "device_name: /dev/sdf"
assert excerpt(CI, 55, 55).strip().startswith("volume_size: 100")
assert excerpt(CI, 81, 81).strip() == "timeout: 120"
assert excerpt(CI, 100, 100).strip() == 'when: cluster_state == "absent"'
assert excerpt("src/deployment/inventory.yml", 22, 22).strip() == "persistent_disk_size: 50"
assert excerpt("src/deployment/inventory.yml", 15, 15).strip() == 'aws_instance_type: "t2.large"'
assert excerpt("src/deployment/ansible.cfg", 2, 2).strip() == "host_key_checking = False"
assert excerpt(PV, 288, 288).strip() == "- name: Configure AWS credentials"
assert X42.at(39) == ["PLAY [Create App Application Machine]"]
assert X42.at(42) == ["ok: [localhost]"] and X42.at(44) == ["TASK [Create security group]"]
L45 = X42.at(45)[0]
assert L45.endswith("AWS was not able to validate the provided access credentials"), L45
assert X42.recap()[1]["ok"] == 1 and X42.recap()[1]["failed"] == 1
MSG44 = X44.msg(42)
assert MSG44[0] == "fatal: [EXTERNAL_IP]: UNREACHABLE! =>"
assert "Could not resolve hostname external_ip" in MSG44[1]
assert X44.recap()[1]["unreachable"] == 1
assert X44.at(39) == ["PLAY [Configure app server instance]"] and X44.at(41) == ["TASK [Gathering Facts]"]
assert C43.at(5) == ["        EXTERNAL_IP:"]
assert C45.at(3)[0].startswith("    # ansible_ssh_private_key_file:") and "/root/.ssh/ac215_2024.pem" in C45.at(3)[0]
assert "/secrets/ac215_2024.pem" in C45.at(6)[0] and not C45.at(6)[0].lstrip().startswith("#")

UNTESTED = ("untested: the attach reuses /dev/sdf, and the disk is pinned to us-east-1a", "· watch that task")
NOT_TESTED = ("on a real account, 'Attach EBS volume' may fail: /dev/sdf is taken, or another zone",
              "· the server still works",
              "· the 50 GB volume stays detached and billed (part 2)")
SECOND = "second laptop terminal · the toolbox stays open · /app is this folder, edits show up inside at once"
BOOKMARK = "▲ 4: GitHub Actions · ▼ 7: your laptop · remember both"   # S04's bookmark, same words
GROUPS = (("Docker CE", list(range(0, 16)) + list(range(19, 26)) + [37]),
          ("format + mount /mnt/disk-1", [16, 17, 18]),
          ("AWS CLI v2", list(range(26, 36))),
          ("aws configure", [36]))
assert sorted(i for _, g in GROUPS for i in g) == list(range(38))


# ------------------------------------------------------------------ helpers of this scene
def at_top_left(m, left: float = -6.5, top: float = 2.75):
    return m.move_to([left + m.width / 2, top - m.height / 2, 0])


def drop_all(scene, *mobs, run_time: float = 0.4, shift=ORIGIN):
    scene.play(*[FadeOut(m, shift=shift) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def find_row(rows, sub):
    hits = [r for r in rows if sub in r.text]
    assert hits, (sub, [r.text for r in rows])
    return hits[0]


def task_tile(i: int, state: str = "changed") -> VGroup:
    """The one-tile task strip of block 0: 'task n/9 · <name>' (YELLOW while it runs; GREY dashed
    with 'when: absent' when skipped)."""
    if state == "skipped":
        t = VGroup(label(f"task {i + 1}/9 ·", 20, S.GREY), label(CTASKS[i], 20, S.GREY),
                   mono("when: absent", 20, S.GREY)).arrange(RIGHT, buff=0.15)
        fr = outline_box(t.width + 0.45, 0.55, SKIP, solid=False)
    else:
        t = VGroup(label(f"task {i + 1}/9 ·", 20, S.GREY), label(CTASKS[i], 20, INK)).arrange(RIGHT, buff=0.15)
        fr = box(t.width + 0.45, 0.55, TURN, fill_opacity=0.2, radius=0.08)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def note_box(lines, tag_text: str | None = None, color=S.GREY) -> VGroup:
    """A GREY dashed note of 1-3 lines (an optional tag on its top edge). .frame .text .tag"""
    t = VGroup(*[label(s, 20, color) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = outline_box(t.width + 0.5, t.height + (0.62 if tag_text else 0.4), color, solid=False)
    t.move_to(fr).shift(DOWN * (0.08 if tag_text else 0))
    g = VGroup(fr, t)
    g.frame, g.text, g.tag = fr, t, None
    if tag_text:
        tg = not_tested_tag(tag_text)
        tg.move_to(fr.get_corner(UL) + np.array([0.3 + tg.width / 2, 0, 0]))
        g.add(tg)
        g.tag = tg
    return g


def disk_row(text: str, h: float = 0.4, color=OWN) -> VGroup:
    d = disk_glyph(h, color)
    t = mono(text, 20, INK)
    g = VGroup(d, t).arrange(RIGHT, buff=0.12)
    g.disk, g.text = d, t
    return g


class CreateAndProvision(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S08"] == 8, len(SAY)

        # ========================================================== 0. step 6: what the playbook builds
        tr = tracker_b(6)
        card = PlayCard(PLAYBOOKS[1], X42.at(39)[0][6:-1], "localhost",
                        [*CTASKS[:6], (CTASKS[6], "when: absent"), *CTASKS[7:]], cols=2)
        at_top_left(card, top=2.7)
        tbx = crate("toolbox", sub="localhost")
        awsb = aws_box(box_w=2.6, box_h=1.4)
        tbx.move_to([5.2, 1.7, 0])
        awsb.move_to([5.2, -0.6, 0])
        api0 = route(tbx.frame.get_bottom(), awsb.frame.get_top(), stroke=3)
        api_t = label("AWS API", 20, ROUTE).next_to(api0, RIGHT, buff=0.1)

        v = VmLayout()
        v.frame.save_state()
        v.title.save_state()
        v.frame.set_opacity(0)
        v.title.set_opacity(0)
        frame_show = v.frame.saved_state.copy()
        title_show = v.title.saved_state.copy()
        tbx_left = [-5.15, -0.35, 0]
        aws_top = label("AWS · us-east-1", 20, CLOUD)
        aws_top.move_to([5.3, 2.45, 0])
        disk50 = VGroup(disk_glyph(0.5), VGroup(mono("50 GB", 20, INK), mono("us-east-1a", 20, S.GREY))
                        .arrange(DOWN, aligned_edge=LEFT, buff=0.06)).arrange(RIGHT, buff=0.15)
        disk50.move_to([-6.45 + disk50.width / 2, -1.75, 0])
        own = VGroup(disk_row("100 GB root"), disk_row("100 GB · /dev/sdf")).arrange(RIGHT, buff=0.5)
        own.move_to([0.6, -1.35, 0])
        deleted = grey_chip("deleted with the instance").next_to(own, DOWN, buff=0.15)
        slot = outline_box(0.85, 0.75, S.GREY, solid=False).move_to([-3.75, -1.75, 0])   # outside the wall: not attached
        ssh_chip = grey_chip("times out after 120 s? your network may block port 22")
        ssh_chip.move_to([0.5, -2.85, 0])
        untested = note_box(UNTESTED)
        untested.move_to([0.5, -2.95, 0])

        def api_call(target, run_time: float = 0.7):
            """A PINK API call from the toolbox to `target` (a point or a mobject)."""
            p = target if isinstance(target, np.ndarray) else target.get_center()
            ln = Line(tbx.frame.get_right(), p, color=ROUTE, stroke_width=3)
            d = dot()
            d.move_to(ln.get_start())
            self.play(Create(ln), d.animate.move_to(p), run_time=run_time * 0.6)
            self.play(FadeOut(ln), FadeOut(d), run_time=run_time * 0.4)

        def swap(old, new, *extra, run_time: float = 0.5):
            """Cross-fade the task strip (a Transform between tiles squeezes the words below 20 pt)."""
            self.play(FadeOut(old, shift=UP * 0.15), FadeIn(new, shift=UP * 0.15), *extra, run_time=run_time)
            self.remove(old)
            return new

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(card, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(tbx), FadeIn(awsb), run_time=0.5)
            vo.wait_until("from localhost")
            self.play(Indicate(card.hosts_chip, color=IMAGE, scale_factor=1.08), Indicate(tbx.text, color=IMAGE),
                      run_time=0.8)
            vo.wait_until("through the AWS API")
            self.play(GrowArrow(api0), FadeIn(api_t), run_time=0.6)
            self.play(card.set_state(6, "skipped"), run_time=0.5)

            vo.wait_until("First, a security group")
            tile = task_tile(0).move_to([-2.9, 2.45, 0])
            tile.align_to(np.array([-2.9, 0, 0]), LEFT)
            self.play(FadeOut(card), FadeOut(api0), FadeOut(api_t), FadeIn(tile, shift=DOWN * 0.1),
                      tbx.animate.move_to(tbx_left), awsb.animate.move_to([5.3, 0.3, 0]), run_time=0.8)
            self.remove(card, api0, api_t)
            api_call(np.array([-3.0, 0.5, 0]))
            v.wall(self)
            vo.wait_until("open to anyone")
            self.play(each([v.doors[p].text for p in SG_PORTS], SHARED, lag=0.2),
                      Indicate(v.sg.cidr.text, color=SHARED), run_time=1.0)
            vo.wait_until("and a 50 gigabyte disk")
            t2 = task_tile(1).move_to(tile).align_to(tile, LEFT)
            tile = swap(tile, t2)
            api_call(disk50[0])
            self.play(FadeIn(disk50, scale=0.9), run_time=0.5)

            vo.wait_until("Then a T 2 large instance")
            t3 = task_tile(2).move_to(tile).align_to(tile, LEFT)
            tile = swap(tile, t3)
            api_call(np.array([4.6, -0.3, 0]))      # passes the wall between doors 80 and 443
            self.play(ReplacementTransform(awsb.frame, frame_show), ReplacementTransform(awsb.text, aws_top),
                      FadeIn(title_show), FadeOut(awsb.body), run_time=0.9)
            self.remove(awsb, frame_show, title_show)
            v.frame.restore()
            v.title.restore()
            v._reseat(self)
            self.add(aws_top)
            vo.wait_until("with your key pair")
            key = key_glyph(0.42).move_to([-2.35, 1.0, 0])
            self.play(FadeIn(key, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(key, color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("and two 100 gigabyte disks")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.15) for r in own], lag_ratio=0.4), run_time=0.8)
            self.play(FadeIn(deleted, shift=UP * 0.1), run_time=0.4)
            t45 = task_tile(4).move_to(tile).align_to(tile, LEFT)
            ssh = route(tbx.frame.get_top(), v.doors[22].text.get_left() + LEFT * 0.08, arc=-0.3, stroke=3)
            tile = swap(tile, t45, Create(ssh), FadeIn(ssh_chip, shift=UP * 0.1))

            vo.wait_until("Last, it tries to attach")
            t6 = task_tile(5).move_to(tile).align_to(tile, LEFT)
            tile = swap(tile, t6, FadeOut(ssh_chip), FadeOut(deleted))
            self.remove(ssh_chip, deleted)
            self.play(FadeIn(slot), run_time=0.3)
            self.play(disk50[0].animate.move_to(slot), disk50[1].animate.next_to(slot, LEFT, buff=0.15), run_time=0.9)
            self.play(Indicate(slot, color=S.GREY, scale_factor=1.1), FadeIn(untested, shift=UP * 0.1), run_time=0.6)
            t7 = task_tile(6, "skipped").move_to(tile).align_to(tile, LEFT)
            tile = swap(tile, t7)

        # ========================================================== 1. the meter starts
        c_ec2 = cost_tag("EC2 instance · by the hour, until terminated")
        c_ec2.move_to([-2.9 + c_ec2.width / 2, 2.45, 0])
        c_ebs = cost_tag("EBS disks · per GB-month")
        c_ip = cost_tag("public IPv4 address · by the hour")
        VGroup(c_ebs, c_ip).arrange(RIGHT, buff=0.5).move_to([0.5, -2.85, 0])
        dial = CostDial(0.42, "cost")
        dial.move_to([5.3, 1.5, 0])
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(tile), run_time=0.4)
            self.remove(tile)
            self.play(FadeIn(dial), run_time=0.4)
            vo.wait_until("the meter runs")
            self.play(dial.tracker.animate(rate_func=linear).increment_value(0.3), run_time=1.2)
            vo.wait_until("the instance by the hour")
            self.play(FadeIn(c_ec2, shift=DOWN * 0.1), Indicate(v.title, color=COST, scale_factor=1.05),
                      dial.tracker.animate(rate_func=linear).increment_value(0.2), run_time=1.0)
            vo.wait_until("its disks")
            self.play(FadeOut(untested), run_time=0.3)
            self.remove(untested)
            self.play(FadeIn(c_ebs, shift=UP * 0.1), Indicate(VGroup(own, disk50), color=COST, scale_factor=1.05),
                      dial.tracker.animate(rate_func=linear).increment_value(0.2), run_time=1.0)
            vo.wait_until("and its public I P address")
            self.play(FadeIn(c_ip, shift=UP * 0.1), Indicate(v.title, color=COST, scale_factor=1.05),
                      dial.tracker.animate(rate_func=linear).increment_value(0.2), run_time=1.0)
            self.play(dial.tracker.animate(rate_func=linear).increment_value(0.3), run_time=1.2)
        dial.freeze()

        # ========================================================== 2. run step 6: the first error
        t = toolbox_term("42", rows=12)
        with self.voiceover(SAY[2]) as vo:
            drop_all(self, v, key, own, disk50, slot, ssh, tbx, aws_top, c_ec2, c_ebs, c_ip, dial, run_time=0.5)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            cmd = type_cmd(self, t, CMD6, type_time=2.4)
            assert " ".join(r.text.rstrip(" \\").strip() for r in cmd.rows).endswith(CMD6), [r.text for r in cmd.rows]
            turn2 = beside(turn_row(), cmd)
            pin(self, cmd, turn2)
            flash_tag(self, turn2)
            vo.wait_until("Gathering facts works")
            o1 = out(self, t, [X42.at(39)[0], X42.at(41)[0], (X42.at(42)[0], PASS)], run_time=0.6)
            self.play(Indicate(o1[2], color=PASS, scale_factor=1.05), run_time=0.6)
            vo.wait_until("then it fails")
            o2 = out(self, t, [X42.at(44)[0], (from_phrase(L45, "botocore."), ERR)], wrap=True, run_time=0.8)
            vo.wait_until("AWS was not able")
            auth = VGroup(find_row(o2, "AWS was not"), find_row(o2, "able to validate"))
            self.play(Indicate(auth, color=ERR, scale_factor=1.04), run_time=0.8)
            rc = play_recap("42")
            y = t._slot(len(t.lines))[1] - 0.3
            rc.move_to([t.box.get_center()[0], y - rc.height / 2 + 0.1, 0])
            assert rc.get_bottom()[1] > t.box.get_bottom()[1] + 0.05, (len(t.lines), t.rows, rc.get_bottom(), t.box.get_bottom(), rc.height)
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.4)
            self.play(rc.flash("failed"), run_time=0.8)

            vo.wait_until("With real keys")
            self.play(FadeOut(rc), run_time=0.3)
            self.remove(rc)
            keep = [ln for ln in t.lines][-3:]
            resize(self, t, 3, keep=keep, run_time=0.7)
            nt = note_box(NOT_TESTED, "not tested")
            att = VGroup(label(CTASKS[5], 20, INK))
            at_tile = outline_box(att.width + 0.45, 0.55, TURN, solid=False)
            att.move_to(at_tile)
            attach_t = VGroup(at_tile, att)
            col = VGroup(attach_t, nt).arrange(DOWN, buff=0.45)
            col.move_to([0, (PIC_TOP - 0.1 + STRIP_TOP + 0.1) / 2, 0])
            self.play(FadeIn(attach_t, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("watch the untested attach task")
            self.play(Circumscribe(attach_t, color=TURN, buff=0.08), FadeIn(nt, shift=UP * 0.1), run_time=1.0)
            vo.wait_until("If it fails")
            self.play(Indicate(nt.text[0], color=INK, scale_factor=1.03), run_time=0.7)
            self.play(Indicate(nt.text[1], color=PASS, scale_factor=1.05), run_time=0.7)
            vo.wait_until("delete that spare disk")
            self.play(Indicate(nt.text[2], color=COST, scale_factor=1.05), run_time=0.9)

        # ========================================================== 3. a kind note on the heading
        rp = readme_panel(92, 92)
        rp.move_to([0, 0.9, 0])
        row92 = rp.rows[92]
        gcp = VGroup(*row92[-5:])        # "in GCP": the last five glyphs
        ul = under(gcp, ERR)
        et = erratum_tag("erratum · it's an EC2 instance · carried over from the GCP README")
        et.next_to(rp, DOWN, buff=0.35)
        with self.voiceover(SAY[3]) as vo:
            drop_all(self, t, attach_t, nt, run_time=0.4)
            self.play(FadeIn(rp, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("the heading says G C P")
            self.play(Create(ul), Indicate(gcp, color=ERR, scale_factor=1.1), run_time=0.8)
            vo.wait_until("it came over from")
            self.play(FadeIn(et, shift=UP * 0.1), run_time=0.5)
            flash_tag(self, et)

        # ========================================================== 4. step 7: the address into the inventory
        lt = laptop_term(4)
        side = grey_chip(SECOND).next_to(lt.box, UP, buff=0.15)
        con = console_drawing("EC2 › Instances", [("chip", "cheese-app-demo · running · t2.large", CLOUD),
                                                   ("Public IPv4 address", EXTERNAL_IP)])
        con.move_to([0, (PIC_TOP - 0.05 + side.get_top()[1] + 0.15) / 2, 0])
        assert con.get_bottom()[1] > side.get_top()[1] + 0.05, (con.get_bottom(), side.get_top())
        turn4 = your_turn()
        turn4.next_to(con.frame, RIGHT, buff=0.3)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(rp), FadeOut(ul), FadeOut(et), track(tr, 7), run_time=0.5)
            self.remove(rp, ul, et)
            self.play(FadeIn(con, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(turn4, shift=UP * 0.1), run_time=0.3)
            vo.wait_until("copy the public I P address")
            ipv = con.rows[1].value
            self.play(Circumscribe(con.rows[1].field, color=TURN, buff=0.05), run_time=0.7)
            self.play(FadeIn(lt, shift=UP * 0.2), FadeIn(side), run_time=0.5)
            fly = ipv.copy()
            self.play(fly.animate.move_to(lt.box.get_center() + UP * 0.5), run_time=0.7)
            self.play(FadeOut(fly, scale=0.6), run_time=0.3)
            self.remove(fly)
            vo.wait_until("into the inventory")
            # the console has done its job: the strip grows to 7 rows so the typed sed command
            # (3 folded rows) and the four output lines are all on screen together
            top7 = strip_top(7)
            side_to = side.copy().move_to([side.get_center()[0], top7 + 0.15 + side.height / 2, 0])
            turn_to = turn4.copy().next_to(side_to, UP, buff=0.12).align_to(side_to, RIGHT)
            resize(self, lt, 7, keep=0, run_time=0.6,
                   extra=(FadeOut(con), Transform(side, side_to), Transform(turn4, turn_to)))
            self.remove(con)
            assert abs(lt.box.get_top()[1] - top7) < 0.05, (lt.box.get_top(), top7)
            type_capture(self, lt, C43, type_time=1.6)
            ed = on_bar(lt, row_tag("sed is our editor"))
            self.play(FadeIn(ed), run_time=0.3)
            vo.wait_until("under appserver hosts")
            rows4 = out(self, lt, C43.at((2, 5)), run_time=0.6)
            self.play(*[g.animate.set_color(TURN) for g in substring(rows4[-1], "EXTERNAL_IP:")],
                      Indicate(rows4[1], color=OWN, scale_factor=1.04), run_time=0.6)
            vo.wait_until("Ours is a placeholder name")
            ph = beside(row_tag("placeholder: we have no server"), rows4[-1])
            pin(self, rows4[-1], ph)

        # ========================================================== 5. step 9 first: the key line
        tr9 = tracker_b(9)
        rp5 = readme_panel(107, 111, size=20)
        rp5.move_to([0, 2.55 - rp5.height / 2, 0])
        e5 = erratum_tag("erratum · README order: do step 9 before step 8")
        e5.next_to(rp5, DOWN, buff=0.2).align_to(rp5, RIGHT)
        rchip = at_top_left(grey_chip("README.md · lines 107–111"), top=2.72)
        e5s = erratum_tag("erratum · README order: do step 9 before step 8").next_to(rchip, RIGHT, buff=0.25)
        bm = row_tag(BOOKMARK, TURN)
        bm.next_to(rchip, DOWN, buff=0.1).align_to(rchip, LEFT)
        named = grey_chip(f"the file in ~/secrets must be named {PEM_CODE}")
        with self.voiceover(SAY[5]) as vo:
            unpin(self, rows4[-1], ph)
            drop_all(self, turn4, side, ed, run_time=0.4)
            resize(self, lt, 4, keep=4, extra=(ReplacementTransform(tr, tr9),), run_time=0.5)
            tr = tr9
            assert rp5.get_bottom()[1] > lt.box.get_top()[1] + 0.05, (rp5.get_bottom(), lt.box.get_top())
            self.play(FadeIn(rp5, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("the key switch of step 9")
            self.play(FadeIn(e5, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, e5)
            vo.wait_until("Pause, comment out line 4")
            self.play(ReplacementTransform(rp5, rchip), ReplacementTransform(e5, e5s), run_time=0.7)
            self.play(FadeIn(bm, shift=DOWN * 0.1), run_time=0.4)
            flash_tag(self, bm)
            resize(self, lt, 9, keep=0, run_time=0.6)
            assert bm.get_bottom()[1] > lt.box.get_top()[1] + 0.6, (bm.get_bottom(), lt.box.get_top())
            type_capture(self, lt, C45, type_time=1.6)
            ex5 = on_bar(lt, extra_row())
            turn5 = your_turn().next_to(lt.box, UP, buff=0.1).align_to(lt.box, RIGHT)
            self.play(FadeIn(ex5), FadeIn(turn5, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and turn on line 7")
            rows5 = out(self, lt, [(C45.at(3)[0], S.GREY), C45.at(5)[0], (C45.at(6)[0].rstrip(), OWN)], wrap=True,
                        run_time=0.8)
            vo.wait_until("It reads slash secrets")
            pem_row = find_row(rows5, "/secrets/ac215_2024.pem")
            pem = substring(pem_row, "/secrets/ac215_2024.pem")
            self.play(*[g.animate.set_color(TURN) for g in pem], run_time=0.5)
            named.next_to(lt.box, UP, buff=0.1).align_to(lt.box, LEFT)
            assert named.get_top()[1] < bm.get_bottom()[1] - 0.03
            assert named.get_right()[0] < turn5.get_left()[0] - 0.1
            self.play(FadeIn(named, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("that exact name")
            self.play(Indicate(pem, color=TURN, scale_factor=1.06), Indicate(named.text, color=INK), run_time=0.8)
            vo.wait_until("The key on line 4")
            ci_row = find_row(rows5, "/root/.ssh/ac215_2024.pem")
            self.play(Indicate(substring(ci_row, "/root/.ssh/ac215_2024.pem"), color=S.GREY, scale_factor=1.06),
                      run_time=0.8)
            st = strike(substring(ci_row, "/root/.ssh/ac215_2024.pem"), S.GREY, stroke=3)
            self.play(Create(st), run_time=0.4)
            attach(self, ci_row, st)

        # ========================================================== 6. step 8: provision
        t6 = toolbox_term("44", rows=9)
        tbx6 = crate("toolbox", sub="localhost")
        srv = outline_box(2.2, 1.3, S.GREY, solid=False)
        q = label("?", 36, ERR).move_to(srv)
        srv_t = label("server", 20, S.GREY).next_to(srv, UP, buff=0.1)
        pic_y = 0.75
        tbx6.move_to([-4.2, pic_y, 0])
        VGroup(srv, q).move_to([3.6, pic_y, 0])
        srv_t.next_to(srv, UP, buff=0.1)
        ssh6 = route(tbx6.frame.get_right(), srv.get_left(), stroke=4)
        who = route_chip("ubuntu + your key", mono_font=False).next_to(ssh6, UP, buff=0.12)
        hk = VGroup(grey_chip("ansible.cfg:2  host_key_checking = False", mono_font=True), tag("trade-off", S.GREY))
        hk.arrange(RIGHT, buff=0.2).move_to([ssh6.get_center()[0], pic_y - 1.05, 0])
        assert hk.get_top()[1] < srv.get_bottom()[1] - 0.05 and hk.get_bottom()[1] > STRIP_TOP + 0.1
        with self.voiceover(SAY[6]) as vo:
            drop_all(self, lt, rchip, e5s, bm, named, turn5, ex5, run_time=0.4)
            self.play(track(tr, 8), FadeIn(t6, shift=UP * 0.2), run_time=0.5)
            cmd6 = type_cmd(self, t6, CMD8, type_time=1.8)
            turn6 = beside(turn_row(), cmd6)
            pin(self, cmd6, turn6)
            flash_tag(self, turn6)
            vo.wait_until("Unreachable")
            o6 = out(self, t6, [X44.at(39)[0], X44.at(41)[0]] + [(s, ERR) for s in MSG44], wrap=True, run_time=0.7)
            vo.wait_until("could not resolve hostname")
            hn = find_row(o6, "external_ip")
            self.play(Indicate(substring(hn, "external_ip"), color=ERR, scale_factor=1.15), run_time=0.8)
            rc6 = play_recap("44")
            y6 = t6._slot(len(t6.lines))[1] - 0.3
            rc6.move_to([t6.box.get_center()[0], y6 - rc6.height / 2 + 0.1, 0])
            assert rc6.get_bottom()[1] > t6.box.get_bottom()[1] + 0.05
            self.play(FadeIn(rc6, shift=UP * 0.1), run_time=0.4)
            self.play(rc6.flash("unreachable"), run_time=0.8)
            vo.wait_until("On yours")
            self.play(FadeOut(rc6), run_time=0.3)
            self.remove(rc6)
            unpin(self, cmd6, turn6)
            resize(self, t6, 3, keep=[ln for ln in t6.lines][-3:], run_time=0.6)
            self.play(FadeIn(tbx6), FadeIn(srv), FadeIn(srv_t), run_time=0.5)
            self.play(GrowArrow(ssh6), run_time=0.6)
            self.play(FadeIn(q, scale=0.6), FadeIn(who, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Host key checking is off")
            self.play(FadeIn(hk, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a trade-off")
            flash_tag(self, hk[1])

        # ========================================================== 7. what provisioning does
        v7 = VmLayout()
        v7.shift(RIGHT * 2.0)
        pc_head = VGroup(mono(PLAYBOOKS[2], 20, S.GREY), label(X44.at(39)[0][6:-1], 20, INK),
                         chip("hosts: appserver", CLOUD, size=20, font=MONO)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        minis = VGroup(*[Rectangle(width=0.42, height=0.24, stroke_color=S.GREY, stroke_width=2)
                         .set_fill(S.GREY, 0.1) for _ in range(38)])
        minis.arrange_in_grid(rows=5, cols=8, buff=(0.1, 0.1), flow_order="rd")
        count = label("38 tasks", 20, S.GREY)
        pc_inner = VGroup(pc_head, minis, count).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        pc_fr = box(max(pc_inner.width, 4.4) + 0.4, pc_inner.height + 0.4, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
        pc_inner.move_to(pc_fr).align_to(pc_fr, LEFT).shift(RIGHT * 0.2)
        pcard = VGroup(pc_fr, pc_inner)
        at_top_left(pcard, top=2.7)
        assert pcard.get_right()[0] < v7.frame.get_left()[0] - 0.1, (pcard.get_right(), v7.frame.get_left())
        cap7 = note("what success looks like · schematic")
        labels = VGroup(*[label_box(name, S.GREY, size=20, box_w=4.4) for name, _ in GROUPS])
        lit = [label_box(name, OWN, size=20, box_w=4.4, fill_opacity=0.3) for name, _ in GROUPS]
        for lb in lit:
            lb.text.set_color(INK)
        labels.arrange(DOWN, buff=0.22)
        at_top_left(labels, top=2.4)
        for lb, ln in zip(labels, lit):
            ln.move_to(lb)
        cap7.next_to(labels, DOWN, buff=0.3).align_to(labels, LEFT)
        o7 = v7._o()
        folder = VGroup(folder_glyph(0.3, OWN), mono("/mnt/disk-1", 20, OWN)).arrange(RIGHT, buff=0.1)
        folder.move_to(np.array([-1.0, -1.65, 0]) + o7)
        xvdf = disk_row("/dev/xvdf")
        xvdf.move_to(np.array([2.6, -1.65, 0]) + o7)
        p288 = code(PV, 288, 292, font_size=20)
        p288.move_to([0, -0.3, 0])
        badge = badge_glyph(0.42)
        def light(i, *extra):
            """A group label lights GREEN (a cross-fade to its lit twin)."""
            self.play(FadeOut(labels[i]), FadeIn(lit[i]), *extra, run_time=0.5)
            labels.submobjects[i] = lit[i]
            self.remove(lit[i])
            self.add(labels)

        with self.voiceover(SAY[7]) as vo:
            drop_all(self, t6, tbx6, srv, q, srv_t, ssh6, who, hk, run_time=0.4)
            self.play(FadeIn(v7), FadeIn(pcard, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("38 tasks")
            self.play(LaggedStart(*[m.animate.set_fill(OWN, 0.35).set_stroke(OWN) for m in minis], lag_ratio=0.03),
                      run_time=1.4)
            groups = [VGroup(*[minis[i] for i in idx]) for _, idx in GROUPS]
            self.play(FadeOut(pc_head), FadeOut(count), FadeOut(pc_fr),
                      *[ReplacementTransform(g, lb) for g, lb in zip(groups, labels)], run_time=1.0)
            self.remove(pcard, pc_fr, pc_head, count, minis)
            self.add(labels)
            self.play(FadeIn(cap7), run_time=0.3)
            vo.wait_until("install Docker")
            light(0)
            v7.engine(self)
            self.play(Indicate(v7.engine_label, color=INK, scale_factor=1.15), run_time=0.6)
            vo.wait_until("then format the second disk")
            light(1, FadeIn(xvdf, shift=UP * 0.1), FadeIn(folder))
            vo.wait_until("and mount it")
            self.play(xvdf.animate.next_to(folder, RIGHT, buff=0.3), run_time=0.9)
            self.play(Indicate(folder, color=OWN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("They install the AWS command line")
            light(2)
            self.play(Indicate(labels[2].text, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("and run AWS configure")
            light(3)
            v7.save_state()
            folder.save_state()
            xvdf.save_state()
            self.play(FadeOut(labels), FadeOut(cap7), v7.animate.set_opacity(0.12),
                      folder.animate.set_opacity(0.12), xvdf.animate.set_opacity(0.12),
                      FadeIn(p288, shift=UP * 0.1), run_time=0.5)
            self.remove(labels, cap7)
            self.play(Indicate(code_span(p288.code, 2, "aws_access_key_id"), color=TURN, scale_factor=1.05), run_time=0.8)
            self.wait(0.7)
            badge.move_to(code_span(p288.code, 2, "aws_access_key_id").get_center())
            self.play(FadeIn(badge, scale=0.6), FadeOut(p288), Restore(v7), Restore(folder), Restore(xvdf),
                      FadeIn(labels), FadeIn(cap7), run_time=0.6)
            self.remove(p288)
            vo.wait_until("your badge now has a copy")
            dst = v7.engine_label.get_bottom() + DOWN * 0.45
            self.play(badge.animate.move_to(dst), run_time=0.8)
            cnt = note("badge · copy 1 on the server")
            cnt.next_to(badge, LEFT, buff=0.3)
            assert cnt.get_left()[0] > v7.frame.get_left()[0] + 0.2
            self.play(FadeIn(cnt, shift=RIGHT * 0.1), Indicate(badge, color=INK, scale_factor=1.2), run_time=0.7)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.remove(*self.mobjects)
        self.wait(0.3)
