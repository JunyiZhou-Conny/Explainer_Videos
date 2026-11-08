"""S15 · The delete that deletes nothing — TRACKER B 15 (README › Deployment Steps · Delete instance).
V4 PlayCard (the create play's first three tasks), the toolbox terminal (laptop/48), CODE
(deploy-create-instance.yml: 94–100), the GOLD clean-up card (Checklist, illustration), the laptop
strip (laptop/49). Lecture: 23 · slide 15 (beat 3).

Beats (script.md "## S15", one voiceover block each):
0. TRACKER B 15. README(147) card. V4's create play card with its first three tiles: "Create
   security group · when: cluster_state == "present"" (line 24), "Create EBS volume · when: …" (line
   37), "Create EC2 instance" with a GREY "no when:" chip. Right of tile 1 a GREEN `register:
   security_group` chip (line 23), a PINK thread from it to `security_group.group_id` (line 45) right
   of tile 3, plain. PONDER (8 s).
1. TRACKER B 15, ▶ your turn. The ponder card, README card and play card leave. Toolbox terminal
   (13 rows) types README 147 (folded) → TBX(laptop/48: 44–45, 47–48, 50, 51 msg, recap 54):
   `skipping` twice GREY; the fatal head and its msg RED ('group_id' flashes); PlayRecap from
   line 54 (ok=1 · failed=1 RED · skipped=2) in the terminal; GREY chip "before any AWS call".
2. V4 again: the two `when:` tiles go GREY dashed, the "Create EC2 instance" tile trips RED, the
   PINK thread breaks RED dashed. Then CODE(deploy-create-instance.yml: 94–100): line 98's
   `id: "{{ ebs_volume.volume_id }}"` RED dashed ring + RED chip "set only by a create run"; GREY
   chip "no task terminates the instance"; "So clean up by hand" → a GOLD "clean up by hand" chip.
3. LECTURE 23 · 15. The GOLD clean-up card (illustration) with three EC2 lines, each with its GOLD
   cost tag where a meter runs, ticking GREEN as said; GREY chip on the frame "lecture: cost is a
   CD challenge".
4. LECTURE off. The card continues: ECR, IAM, GitHub rows slide in and tick.
5. TRACKER B 15 · extra. The last row "Locally: docker image rm cheese-app-deployment · 2.52 GB"
   ticks; the card leaves; the laptop terminal (4 rows) types `cd /home/student/cheese-app-aws &&
   git status --short` (extra) → TERM(laptop/49: 2–4); S05's "your edits" checklist slides in above
   it and collapses into these three rows; GREY chips "keep, or git restore" and "yours also:
   deploy-setup-containers.yml (the Chroma pin), .docker-tag (after a real step 5)". Fade; empty frame.

Deviations from SHOW: cost tags sit only on the card lines that run a meter
(instance, volumes, ECR): security groups, key pairs, IAM and secrets carry no charge, and cost_tag
names meters only. The laptop terminal in beat 5 has 4 rows, not 3, so the folded command's second
row stays visible above its three output rows (the "your edits" card needs the rest of the frame). The disk size "2.52 GB" is shown without the capture name.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S15"]

CI = "src/deployment/deploy-create-instance.yml"
X48 = toolbox_capture("48")
C49 = capture("49")
C29 = capture("29")
README_CMD = readme(147).strip()
CMD = X48.cmd
assert CMD == README_CMD == ("ansible-playbook deploy-create-instance.yml -i inventory.yml "
                             "--extra-vars cluster_state=absent"), (CMD, README_CMD)
assert X48.at(44)[0] == "TASK [Create security group]" and X48.at(45)[0] == "skipping: [localhost]"
assert X48.at(47)[0] == "TASK [Create EBS volume]" and X48.at(48)[0] == "skipping: [localhost]"
assert X48.at(50)[0] == "TASK [Create EC2 instance]"
MSG = X48.msg(51)
assert MSG[0] == "fatal: [localhost]: FAILED! =>" and MSG[1].endswith("has no attribute 'group_id'"), MSG
assert X48.recap()[1]["ok"] == 1 and X48.recap()[1]["failed"] == 1 and X48.recap()[1]["skipped"] == 2
assert excerpt(CI, 7, 7).strip() == "- name: Create security group"
assert excerpt(CI, 23, 23).strip() == "register: security_group"
assert excerpt(CI, 24, 24).strip() == 'when: cluster_state == "present"'
assert excerpt(CI, 27, 27).strip() == "- name: Create EBS volume"
assert excerpt(CI, 37, 37).strip() == 'when: cluster_state == "present"'
assert excerpt(CI, 40, 40).strip() == "- name: Create EC2 instance"
assert "when:" not in excerpt(CI, 40, 61)
assert excerpt(CI, 45, 45).strip() == 'security_group: "{{ security_group.group_id }}"'
assert excerpt(CI, 98, 98).strip() == 'id: "{{ ebs_volume.volume_id }}"'
assert excerpt(CI, 100, 100).strip() == 'when: cluster_state == "absent"'
assert "state: terminated" not in source_text(CI) and source_text(CI).count("state: absent") == 1 \
    and "state: absent" in excerpt(CI, 99, 99)
assert "2.52GB" in C29.line(3) and C29.line(3).startswith("cheese-app-deployment:latest")
assert C49.cmd == "cd /home/student/cheese-app-aws && git status --short"
assert [s.strip() for s in C49.at(2, 3, 4)] == ["M src/deployment/Dockerfile", "M src/deployment/docker-shell.sh",
                                                "M src/deployment/inventory.yml"], C49.at(2, 3, 4)
assert INSTANCE == "cheese-app-demo" and POLICY == "CheeseAppECRPolicy"
assert 'persistent_disk_name: "cheese-app-demo-disk"' in excerpt("src/deployment/inventory.yml", 21, 21)
assert "name: app_security_group" in excerpt(CI, 9, 9)

WHEN = 'when: cluster_state == "present"'
PLAY_TITLE = X48.at(39)[0][6:-1]
assert PLAY_TITLE == "Create App Application Machine", PLAY_TITLE
S05_ROWS = ["docker-shell.sh:10 · ../../../secrets", None, "Dockerfile · drop Helm (33–34, 36)",
            "docker-shell.sh:26 · three ../", "docker-shell.sh:17 · your account ID"]
PONDER_Q = "cluster_state=absent.\nWhich of these three tasks run?"


# ------------------------------------------------------------------ helpers of this scene
def gone(scene, *mobs, run_time: float = 0.5):
    """FadeOut mobjects that are not members of a piece, and take them off the scene."""
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def find_row(rows, sub):
    hits = [r for r in rows if sub in r.text]
    assert hits, (sub, [r.text for r in rows])
    return hits[0]


def words(*parts):
    """One line of mixed text: parts are (text, 'mono'|'label', colour)."""
    g = VGroup(*[(mono if k == "mono" else label)(s, 20, c) for s, k, c in parts])
    return g.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)


def row(main, sub=None, cost=None, cost_on_sub=False):
    """A clean-up card row: the main line, an optional GREY second line, an optional GOLD cost tag
    right of the main line (or of the second line). .words (the main line's words) .cost"""
    words_ = main
    tg = cost_tag(cost) if cost else None
    if tg is not None and not cost_on_sub:
        main = VGroup(main, tg).arrange(RIGHT, buff=0.3)
    if tg is not None and cost_on_sub:
        sub = VGroup(sub, tg).arrange(RIGHT, buff=0.3)
    g = VGroup(main) if sub is None else VGroup(main, sub).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    g.words, g.cost, g.sub = words_, tg, sub
    return g


def tick(scene, ck, i, run_time: float = 0.45):
    """PLAYS: tick row i of the clean-up card; only its words flash (never a filled cost tag)."""
    r = ck.rows[i]
    m = check_mark(0.3, OWN, stroke=4).move_to(r.box).shift(UP * 0.04 + RIGHT * 0.03)
    scene.play(Create(m), Indicate(r.text.words, color=OWN, scale_factor=1.04), run_time=run_time)
    r.add(m)
    ck._reseat(scene)


def cleanup_rows():
    I = INK
    G = S.GREY
    return [
        row(words(("EC2 › Instances:", "label", I), ("terminate", "label", I), (INSTANCE, "mono", I)),
            cost="EC2 instance · by the hour"),
        row(words(("EC2 › Volumes: delete every", "label", I), (INSTANCE, "mono", I),
                  ("volume left,", "label", I)),
            words(("attached or not ·", "label", G), ("cheese-app-demo-disk", "mono", G),
                  ("outlives the instance", "label", G)),
            cost="EBS · per GB-month", cost_on_sub=True),
        row(words(("EC2 › Security Groups:", "label", I), ("app_security_group", "mono", I),
                  ("· Key Pairs: yours", "label", I))),
        row(words(("ECR: delete the three repositories", "label", I)), cost="ECR storage"),
        row(words(("IAM: deactivate + delete the access key", "label", I)),
            words(("the user and", "label", G), (POLICY, "mono", G), ("if made only for this", "label", G))),
        row(words(("GitHub: delete the four repository secrets", "label", I))),
        row(words(("Locally:", "label", I), ("docker image rm cheese-app-deployment", "mono", I)),
            words(("2.52 GB", "label", G))),
    ]


def edits_card():
    """S05's GREEN 'your edits' checklist, all ticked (as S14 rebuilds it)."""
    ck = Checklist("your edits", [r if r else VGroup(label("Linux: bash, not sh", 20, INK), erratum_tag())
                                  .arrange(RIGHT, buff=0.18) for r in S05_ROWS],
                   color=OWN, tag_text=None)
    for r in ck.rows:
        m = check_mark(0.3, OWN, stroke=4).move_to(r.box).shift(UP * 0.04 + RIGHT * 0.03)
        r.add(m)
    return ck


def play_card():
    card = PlayCard(PLAYBOOKS[1], PLAY_TITLE, "localhost",
                    [("Create security group", WHEN), ("Create EBS volume", WHEN), "Create EC2 instance"],
                    cols=1, tile_w=6.6)
    return card


class Teardown(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S15"] == 6, len(SAY)
        tr = tracker_b(15)

        # ========================================================== 0. the delete step: which tasks run?
        rd = readme_panel(147, 147)
        rd.move_to([0, 0, 0]).shift(np.array([6.5 - rd.get_right()[0], 2.75 - rd.get_top()[1], 0]))
        card = play_card()
        card.move_to([0, 0, 0]).shift(np.array([-6.3 - card.get_left()[0],
                                                rd.get_bottom()[1] - 0.3 - card.get_top()[1], 0]))
        t3 = card.tiles[2]
        nowhen = grey_chip("no when:", mono_font=True)
        nowhen.next_to(t3.frame.get_right(), LEFT, buff=0.18)
        reg = ok_chip("register: security_group", mono_font=True)
        reg.next_to(card.frame, RIGHT, buff=0.35).set_y(card.tiles[0].get_y())
        gid = route_chip("security_group.group_id")
        gid.next_to(card.frame, RIGHT, buff=0.35).set_y(t3.get_y())
        thread = CurvedArrow(reg.get_bottom() + DOWN * 0.05, gid.get_top() + UP * 0.05, angle=-PI / 3,
                             color=ROUTE, stroke_width=3, tip_length=0.2)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(rd, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("It runs the same playbook")
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.7)
            self.play(Indicate(substring_label(rd, "cluster_state=absent"), color=TURN, scale_factor=1.08),
                      run_time=0.8)
            vo.wait_until("Look at the when lines")
            self.play(Indicate(card.tiles[0].sub, color=TURN, scale_factor=1.06),
                      Indicate(card.tiles[1].sub, color=TURN, scale_factor=1.06), run_time=0.8)
            self.play(FadeIn(nowhen, shift=LEFT * 0.1), run_time=0.4)
            self.play(FadeIn(reg, shift=LEFT * 0.1), run_time=0.4)
            self.play(Create(thread), FadeIn(gid, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("Which of these three tasks run")
            self.play(Circumscribe(card.tiles, color=TURN, buff=0.08), run_time=0.9)
        q = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 1. run it as written
        t = toolbox_term("48", rows=13)
        pic = VGroup(card, nowhen, reg, gid, thread)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(q), FadeOut(rd), FadeOut(pic), run_time=0.5)
            self.remove(q, rd, pic, *q.get_family(), *rd.get_family(), *pic.get_family())
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.4)
            cmd = type_cmd(self, t, CMD, type_time=1.6)
            assert " ".join(r.text.rstrip(" \\").strip() for r in cmd.rows).endswith(CMD), [r.text for r in cmd.rows]
            yt = beside(turn_row(), cmd)
            pin(self, cmd, yt)
            vo.wait_until("Security group, skipping")
            out(self, t, [X48.at(44)[0], (X48.at(45)[0], S.GREY)], run_time=0.5)
            vo.wait_until("E B S volume, skipping")
            out(self, t, [X48.at(47)[0], (X48.at(48)[0], S.GREY)], run_time=0.5)
            vo.wait_until("Then the instance task")
            out(self, t, [X48.at(50)[0]], run_time=0.35)
            vo.wait_until("and fails")
            fe = out(self, t, [(m, ERR) for m in MSG], wrap=True, run_time=0.6)
            vo.wait_until("no attribute group ID")
            gr = find_row(fe, "group_id")
            self.play(Indicate(substring(gr, "has no attribute 'group_id'"), color=ERR, scale_factor=1.06),
                      run_time=0.8)
            vo.wait_until("That is before any AWS call")
            rc = play_recap("48")
            y = t._slot(len(t.lines))[1] - 0.3
            rc.move_to([t.box.get_center()[0], y - rc.height / 2 + 0.1, 0])
            assert rc.get_bottom()[1] > t.box.get_bottom()[1] + 0.05, (len(t.lines), rc.get_bottom())
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.4)
            self.play(rc.flash("failed"), rc.flash("skipped", color=S.GREY), run_time=0.8)
            bf = under_term(t, grey_chip("before any AWS call"))
            self.play(FadeIn(bf, shift=DOWN * 0.1), run_time=0.4)

        # ========================================================== 2. why: a skipped register, no terminate
        card2 = play_card()
        card2.move_to([0, 0, 0]).shift(np.array([-6.3 - card2.get_left()[0], 2.7 - card2.get_top()[1], 0]))
        t3 = card2.tiles[2]
        nowhen2 = grey_chip("no when:", mono_font=True)
        nowhen2.next_to(t3.frame.get_right(), LEFT, buff=0.18)
        reg2 = ok_chip("register: security_group", mono_font=True)
        reg2.next_to(card2.frame, RIGHT, buff=0.35).set_y(card2.tiles[0].get_y())
        gid2 = route_chip("security_group.group_id")
        gid2.next_to(card2.frame, RIGHT, buff=0.35).set_y(t3.get_y())
        thread2 = CurvedArrow(reg2.get_bottom() + DOWN * 0.05, gid2.get_top() + UP * 0.05, angle=-PI / 3,
                              color=ROUTE, stroke_width=3, tip_length=0.2)
        broken = DashedVMobject(thread2.copy().set_color(ERR), num_dashes=12)
        gid_bad = err_chip("security_group.group_id", mono_font=True).move_to(gid2)
        missing = err_chip("missing", size=20).next_to(gid_bad, DOWN, buff=0.15)
        pic2 = VGroup(card2, nowhen2, reg2, gid2, thread2)

        p = code(CI, 94, 100)
        p.move_to([0, 0, 0]).shift(UP * (2.7 - p.get_top()[1]))
        k98 = 98 - 94
        span = code_span(p.code, k98, 'id: "{{ ebs_volume.volume_id }}"')
        rring = DashedLine(span.get_corner(DL) + DOWN * 0.06, span.get_corner(DR) + DOWN * 0.06,
                           color=ERR, stroke_width=4, dash_length=0.12)
        only = err_chip("set only by a create run")
        only.next_to(span, RIGHT, buff=0.4)
        noterm = grey_chip("no task terminates the instance")
        noterm.next_to(p, DOWN, buff=0.35)
        byhand = cost_tag("clean up by hand")
        byhand.next_to(noterm, DOWN, buff=0.35)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(t), FadeOut(bf), FadeOut(rc), run_time=0.5)
            self.remove(t, bf, rc, *t.get_family(), *bf.get_family(), *rc.get_family())
            self.play(FadeIn(card2, shift=UP * 0.15), FadeIn(nowhen2), FadeIn(reg2), FadeIn(gid2),
                      FadeIn(thread2), run_time=0.6)
            self.play(card2.set_state(0, "skipped"), card2.set_state(1, "skipped"), run_time=0.6)
            self.play(Indicate(reg2.text, color=S.GREY, scale_factor=1.06), run_time=0.6)
            vo.wait_until("so the instance task trips")
            self.play(card2.set_state(2, "failed"), ReplacementTransform(thread2, broken),
                      ReplacementTransform(gid2, gid_bad), FadeIn(missing, shift=UP * 0.1), run_time=0.7)
            pic2 = VGroup(card2, nowhen2, reg2, gid_bad, broken, missing)
            vo.wait_until("Even past that")
            self.play(FadeOut(pic2), run_time=0.4)
            self.remove(pic2, *pic2.get_family())
            self.play(FadeIn(p, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("needs a volume ID")
            self.play(Create(rring), span.animate.set_color(ERR), run_time=0.5)
            self.play(FadeIn(only, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("and no task terminates")
            self.play(FadeIn(noterm, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(noterm.text, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("So clean up by hand")
            self.play(FadeIn(byhand, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 3. EC2 console: instance, volume, SG, key
        rows = cleanup_rows()
        full = Checklist("clean-up · do it by hand", rows, color=COST)
        card_w = full.frame.width
        ck = Checklist("clean-up · do it by hand", cleanup_rows()[:3], color=COST, card_w=card_w)
        ck.move_to([0, 0, 0]).shift(np.array([-ck.frame.get_center()[0], 2.7 - ck.frame.get_top()[1], 0]))
        lr = lref("15")
        lec = tag("lecture: cost is a CD challenge", S.GREY)      # opaque: it sits on the card's edge
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p, rring, only, noterm)), byhand.animate.move_to(ck.head).set_opacity(0),
                      run_time=0.6)
            self.remove(p, rring, only, noterm, byhand, *p.get_family(), *byhand.get_family())
            self.play(FadeIn(ck, shift=UP * 0.15), FadeIn(lr), run_time=0.6)
            vo.wait_until("terminate the instance")
            tick(self, ck, 0)
            vo.wait_until("then delete the 50 gigabyte volume")
            tick(self, ck, 1)
            vo.wait_until("which outlives it")
            self.play(Indicate(ck.rows[1].text.sub[0], color=COST, scale_factor=1.05), run_time=0.7)
            vo.wait_until("the security group and your key pair")
            tick(self, ck, 2)
            vo.wait_until("Cost is one of")
            lec.move_to([ck.frame.get_right()[0] - lec.width / 2 - 0.3, ck.frame.get_bottom()[1], 0])
            self.play(FadeIn(lec, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and this server bills")
            flash_tag(self, ck.rows[0].text.cost, run_time=0.6)
            flash_tag(self, ck.rows[1].text.cost, run_time=0.6)

        # ========================================================== 4. ECR, IAM, GitHub
        more = cleanup_rows()
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(lr), FadeOut(lec), run_time=0.4)
            self.remove(lr, lec)
            vo.wait_until("In E C R")
            ck.add_row(self, more[3])
            tick(self, ck, 3)
            vo.wait_until("In IAM")
            ck.add_row(self, more[4])
            vo.wait_until("and the user and the policy")
            tick(self, ck, 4)
            vo.wait_until("On GitHub")
            ck.add_row(self, more[5])
            tick(self, ck, 5)

        # ========================================================== 5. locally: the image, your edits
        lt = laptop_term(4)
        ex = on_bar(lt, extra_row())
        ed = edits_card()
        with self.voiceover(SAY[5]) as vo:
            ck.add_row(self, more[6])
            vo.wait_until("remove the toolbox image")
            tick(self, ck, 6)
            vo.wait_until("two and a half gigabytes")
            self.play(Indicate(ck.rows[6].text.sub, color=COST, scale_factor=1.1), run_time=0.6)
            vo.wait_until("and keep or restore")
            self.play(FadeOut(ck), track(tr, 15, True), run_time=0.5)
            self.remove(ck, *ck.get_family())
            self.play(FadeIn(lt, shift=UP * 0.2), FadeIn(ex), run_time=0.4)
            type_cmd(self, lt, C49.cmd, type_time=1.2)
            ed.move_to([0, 0, 0]).shift(np.array([6.4 - ed.frame.get_right()[0], 2.7 - ed.frame.get_top()[1], 0]))
            assert ed.frame.get_bottom()[1] > lt.box.get_top()[1] + 0.1, (ed.frame.get_bottom(), lt.box.get_top())
            self.play(FadeIn(ed, shift=LEFT * 0.4), run_time=0.6)
            self.play(Indicate(ed.head, color=OWN, scale_factor=1.08), run_time=0.7)
            self.wait(0.5)
            room(self, lt, 3)                  # the prompt row scrolls off; the command's tail stays
            res = VGroup()                     # the three output rows, placed but not yet shown
            for s_ in C49.at(2, 3, 4):
                guard(s_)
                ln = mono_line(s_, lt.size, OUTPUT)
                lt._place(ln, len(lt.lines))
                lt.lines.add(ln)
                res.add(ln)
            assert len(lt.lines) <= lt.rows, len(lt.lines)
            self.play(FadeTransform(ed, res), run_time=1.0)
            self.remove(res, ed, *ed.get_family())
            self.add(lt, ex)
            self.play(LaggedStart(*[Indicate(r, color=OWN, scale_factor=1.04) for r in res], lag_ratio=0.25),
                      run_time=0.9)
            keep = grey_chip("keep, or git restore", mono_font=False)
            also = label_box(["yours also: deploy-setup-containers.yml (the Chroma pin),",
                              ".docker-tag (after a real step 5)"], S.GREY)
            notes = VGroup(keep, also).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
            notes.move_to([0, 0, 0]).shift(np.array([-6.3 - notes.get_left()[0],
                                                     lt.box.get_top()[1] + 0.35 - notes.get_bottom()[1], 0]))
            self.play(FadeIn(keep, shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(also, shift=UP * 0.1), run_time=0.5)
            self.wait(1.2)
        self.play(FadeOut(VGroup(tr, lt, ex, keep, also)), run_time=0.7)
        self.remove(*self.mobjects)
        self.wait(0.3)


def substring_label(rd, sub):
    """The README card row holding `sub` (a label Text: no per-character glyph map, so the row)."""
    for n, r in rd.rows.items():
        txt = getattr(r, "text", None)
        if isinstance(txt, str) and sub in txt:
            return r
        if hasattr(r, "submobjects") and any(sub in getattr(x, "text", "") for x in r.submobjects):
            return r
    raise ValueError(sub)
