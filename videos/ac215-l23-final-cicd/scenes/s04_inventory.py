"""S04 · Ansible in one picture — tracker A 6 (README › Before you deploy · Deployment setup). No
lecture tag (script.md has no LECTURE mark in this scene). V4 AnsibleMachine and its inventory tree.

Beats (script.md "## S04"; one voiceover block each):
0. TRACKER A 5 → 6. Two cards side by side: GREY dashed "Pulumi · L20: describe the infrastructure you
   want" and PURPLE "Ansible: an ordered list of tasks · machines from an inventory"; under the Ansible
   card, stacked, the GREEN chip "many modules: state: present" and the GREY chip "this repo: plenty of
   shell too", each on its clause.
1. The cards leave. V4 AnsibleMachine: the GREEN inventory tree (left) and the two play cards (GREY chip
   "here: one play per playbook"); the hosts chips and the tiles flash on their clauses; the AWS /
   toolbox / server column arrives on "The hosts line"; on "localhost" a PURPLE spark fires in the TEAL
   toolbox (ec2_group, a PINK call up to AWS); on "appserver" the dot rides the PINK SSH arrow into the
   BLUE server, chip "ubuntu + your key".
2. TRACKER A 6. The machine leaves except the tree, which lies down into a row along the bottom (all →
   appserver → <EXTERNAL_IP>); its `all` card expands (TransformFromCopy) into CODE(inventory.yml:
   1–11) at 20 pt, trim 70. Line 3 YELLOW (+ "ubuntu" flashes); lines 4 and 7 YELLOW with one YELLOW
   bookmark "remember both" in the free space of rows 5–6; lines 9–11 PINK, three PINK arrows
   to a TEAL label "toolbox environment" under the panel, right.
3. TRACKER A 6. Transform to CODE(inventory.yml: 14–25) (left): BLUE bars on 14 (region) and 15
   (t2.large), YELLOW bar on 16 + "## Change this" flashes, BLUE bar on 17 with the chips "per region"
   and the GREY card "if step 6 says InvalidAMIID: pick a current Ubuntu image in EC2 › AMIs,
   us-east-1" right of the panel, BLUE bars on 21–22 (the 50 GB disk).
4. TRACKER A 6. The panel moves right; README(67–72) card left. Bullets 2 and 4 fly as YELLOW ticks
   onto lines 14–23 (a bracket) and 16; bullets 1 and 3 fly onto two GREY chips "line 3 ✓ (seen)" and
   "lines 9–11 ✓ (seen)" under the card (they leave when the strip comes). Line 24 YELLOW; a 1-row
   laptop strip (prompt student@laptop:~$, `▶ your turn` on its bar) types `openssl rand -base64 32`
   (row tags "extra" and "written out, not run"; never run).
   On "The host on line 30": the card, chips, strip go; the tree row returns; Transform to
   CODE(inventory.yml: 27–30), line 30 GREY dashed ring + chip "after the server exists"; the panel then Transforms
   into the row's leaf <EXTERNAL_IP>, GREY dashed.
5. The tree row rises; under it the five counters ok · changed · unreachable · failed · skipped
   (GREY); "failed" and "unreachable" turn GREEN zeros on "zero". A two-tile play card (apt · state:
   present, shell · lsb_release -cs; from deploy-provision-instance.yml) runs twice ("sketch · run
   1/2"): run 1 both YELLOW changed; run 2 the apt tile GREEN ok, the shell tile YELLOW again; the
   counters follow. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S04"]

INV = "src/deployment/inventory.yml"
PROV = "src/deployment/deploy-provision-instance.yml"

# ------------------------------------------------------------------ the real sources (checked)
assert excerpt(INV, 3, 3).strip() == "ansible_user: ubuntu"
assert "## Github Actions" in excerpt(INV, 4, 4)
assert excerpt(INV, 7, 7).lstrip().startswith("# ansible_ssh_private_key_file")
assert all("lookup('env'," in excerpt(INV, n, n) for n in (9, 10, 11))
assert excerpt(INV, 14, 14).strip() == 'aws_region: "us-east-1"'
assert excerpt(INV, 15, 15).strip() == 'aws_instance_type: "t2.large"'
assert excerpt(INV, 16, 16).strip().startswith('aws_keypair_name: "ac215_2024"  ## Change this')
assert excerpt(INV, 17, 17).strip().startswith("aws_ami_id:")
assert excerpt(INV, 22, 22).strip() == "persistent_disk_size: 50"
assert excerpt(INV, 24, 24).strip().startswith("nextauth_secret:")
assert excerpt(INV, 30, 30).strip() == "<EXTERNAL_IP>:"
assert readme(67) == "### Deployment Setup"
assert "ansible user" in readme(69) and "instance details" in readme(70)
assert "Access Key" in readme(71) and "Key Pair" in readme(72)
assert excerpt(PROV, 1, 2) == "- name: Configure app server instance\n  hosts: appserver"
assert excerpt(PROV, 14, 14).strip() == "shell: lsb_release -cs"
assert excerpt(PROV, 153, 155).split() == ["apt:", "name:", "docker-ce", "state:", "present"]

ROW_Y = -2.62          # the inventory tree, lying down along the bottom (beats 2-4)


# ------------------------------------------------------------------ helpers of this scene
def tree_row(host: str = EXTERNAL_IP, dashed_host: bool = False):
    """V4's inventory tree lying down: all (vars) → appserver → host, GREEN, left-aligned at -6.4.
    .all .group .leaf .edges"""
    a = label_box(["all", "vars"], OWN)
    a.text[1].set_color(S.GREY)
    g = label_box("appserver", OWN, mono_font=True)
    lf = leaf_box(host, dashed_host)
    VGroup(a, g, lf).arrange(RIGHT, buff=0.55)
    e = VGroup(Line(a.get_right(), g.get_left(), color=OWN, stroke_width=3),
               Line(g.get_right(), lf.get_left(), color=OWN, stroke_width=3))
    row = VGroup(e, a, g, lf)
    row.all, row.group, row.leaf, row.edges = a, g, lf, e
    row.move_to([-6.4 + row.width / 2, ROW_Y, 0])
    return row


def leaf_box(host: str, dashed: bool = False):
    return label_box(host, S.GREY if dashed else OWN, dashed=dashed, mono_font=True)


def _rows(p):
    """(centre of row 0, row pitch) of panel p's code, on an even grid: glyph boxes differ per line
    (descenders, quotes), so bars sized from them overlap their neighbours as brighter slivers."""
    cs = [ln.get_center()[1] for ln in p.code.code_lines]
    pitch = (cs[0] - cs[-1]) / max(1, len(cs) - 1)
    c0 = sum(c + k * pitch for k, c in enumerate(cs)) / len(cs)
    return c0, pitch


def bars(p, first: int, a: int, b: int, color, opacity: float = 0.2):
    """One bar over file lines a..b of panel p (which starts at file line `first`); adjacent bars
    meet edge to edge, never overlap."""
    c0, pitch = _rows(p)
    ya, yb = c0 - (a - first) * pitch, c0 - (b - first) * pitch
    bg = p.code.background
    return Rectangle(width=bg.width - 0.12, height=(b - a + 1) * pitch, stroke_width=0) \
        .set_fill(color, opacity).move_to([bg.get_center()[0], (ya + yb) / 2, 0])


def bar(p, first: int, n: int, color, opacity: float = 0.2):
    """A translucent bar over file line n of panel p."""
    return bars(p, first, n, n, color, opacity)


def line_y(p, first: int, n: int) -> float:
    return p.code.code_lines[n - first].get_center()[1]


def line_right(p, first: int, n: int) -> float:
    return p.code.code_lines[n - first].get_right()[0]


def mixed_chip(parts, color=S.GREY, size: float = 20):
    """A chip whose text mixes the label font and mono: parts = [(text, 'mono'|'label'), …]."""
    t = VGroup(*[mono(x, size, INK) if k == "mono" else label(x, size, INK) for x, k in parts])
    t.arrange(RIGHT, buff=0.12)
    h =mono("|", size).height + 0.24
    b = box(t.width + 0.48, h, color, fill_opacity=0.16, radius=h / 2)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def run_chip(n: int):
    return grey_chip(f"sketch · run {n}")


class AnsibleInOnePicture(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S04"] == 6, len(SAY)

        # ========================================================== 0. a new tool: Ansible
        tr = tracker_a(5)
        pul = label_box(["Pulumi · L20", "describe the infrastructure", "you want"], PAST, dashed=True,
                        size=24, box_w=5.6, pad=0.3)
        ans = label_box(["Ansible", "an ordered list of tasks", "machines from an inventory"], TOOL, size=24,
                        box_w=5.6, pad=0.3)
        ans.text[0].set_color(INK)
        VGroup(pul, ans).arrange(RIGHT, buff=0.8).move_to([0, 0.9, 0])
        new_tool = tool_chip("Ansible", size=24).move_to(ans.text[0])
        c_state = ok_chip("many modules: state: present")
        c_shell = mixed_chip([("this repo: plenty of", "label"), ("shell", "mono"), ("too", "label")])
        VGroup(c_state, c_shell).arrange(DOWN, buff=0.18).next_to(ans, DOWN, buff=0.35)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), run_time=0.5)
            self.play(track(tr, 6), run_time=0.6)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("brings a new tool")
            self.play(FadeIn(new_tool, scale=0.8), run_time=0.6)
            self.play(Indicate(new_tool.text, color=TOOL, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Pulumi, in lecture 20")
            self.play(FadeIn(pul, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("described the infrastructure")
            self.play(Indicate(pul.text[1], color=INK, scale_factor=1.06),
                      Indicate(pul.text[2], color=INK, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Ansible runs an ordered list")
            self.play(FadeIn(ans, shift=UP * 0.15), FadeOut(new_tool), run_time=0.6)
            self.play(Indicate(ans.text[1], color=TOOL, scale_factor=1.06), run_time=0.7)
            vo.wait_until("against the machines")
            self.play(Indicate(ans.text[2], color=TOOL, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Many of its modules")
            self.play(FadeIn(c_state, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("this repo also runs")
            self.play(FadeIn(c_shell, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(c_shell.text[1], color=INK, scale_factor=1.12), run_time=0.7)

        # ========================================================== 1. inventory → play → task → module
        a = AnsibleMachine()
        c0, c1 = a.cards
        one = grey_chip("here: one play per playbook")
        one.move_to([c0.frame.get_right()[0] - one.width / 2, c0.frame.get_top()[1] + 0.12 + one.height / 2, 0])
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(pul, ans, c_state, c_shell), shift=DOWN * 0.2), run_time=0.5)
            self.play(FadeIn(a.tree, shift=RIGHT * 0.15), FadeIn(a.cards, shift=UP * 0.15), run_time=0.7)
            self.play(FadeIn(one, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Each play names its hosts")
            self.play(Indicate(c0.hosts_chip.text, color=IMAGE, scale_factor=1.12),
                      Indicate(c1.hosts_chip.text, color=CLOUD, scale_factor=1.12), run_time=0.8)
            vo.wait_until("each task calls one module")
            self.play(LaggedStart(*[Indicate(t.text, color=TOOL, scale_factor=1.12)
                                    for t in [*c0.tiles, *c1.tiles]], lag_ratio=0.15), run_time=1.2)
            vo.wait_until("The hosts line decides")
            self.play(FadeIn(a.aws, shift=LEFT * 0.15), FadeIn(a.toolbox, shift=LEFT * 0.15),
                      FadeIn(a.server, shift=LEFT * 0.15), run_time=0.6)
            self.remove(a.tree, a.cards, a.aws, a.toolbox, a.server)
            self.add(a)
            self.play(Circumscribe(c0.hosts_chip, color=IMAGE, buff=0.06),
                      Circumscribe(c1.hosts_chip, color=CLOUD, buff=0.06), run_time=0.9)
            vo.wait_until("localhost means")
            a.fire(self, 0, 0)
            vo.wait_until("appserver means")
            a.fire(self, 1, 0)

        # ========================================================== 2. inventory.yml lines 1-11
        row = tree_row()
        p1 = code(INV, 1, 11, font_size=20, trim=70)
        p1.move_to([0, 2.75 - p1.height / 2, 0])
        b3 = bar(p1, 1, 3, TURN)
        b4, b7 = bar(p1, 1, 4, TURN), bar(p1, 1, 7, TURN)
        bookmark = row_tag("▲ 4: GitHub Actions · ▼ 7: your laptop · remember both", TURN)
        y5 = (p1.code.code_lines[3].get_bottom()[1] + p1.code.code_lines[5].get_top()[1]) / 2   # blank line 5
        bookmark.move_to([p1.code.background.get_right()[0] - 0.2 - bookmark.width / 2, y5, 0])
        b911 = bars(p1, 1, 9, 11, ROUTE)
        env = label_box("toolbox environment", IMAGE)
        env.move_to([6.4 - env.width / 2, ROW_Y, 0])
        x_end = max(line_right(p1, 1, n) for n in (9, 10, 11)) + 0.12
        env_arrows = VGroup(*[
            Arrow([x_end, line_y(p1, 1, n), 0], env.get_top() + RIGHT * (0.5 * (n - 10)), color=ROUTE,
                  stroke_width=3, buff=0.06, max_tip_length_to_length_ratio=0.12, tip_length=0.16)
            for n in (9, 10, 11)])
        with self.voiceover(SAY[2]) as vo:
            a.drop(self, a.cards, a.aws, a.toolbox, a.server, a.api_arrow, a.ssh_arrow, a.ssh_chip, run_time=0.5)
            self.play(FadeOut(one), run_time=0.3)
            tree = a.tree
            self.remove(a)
            a.remove(tree)
            self.add(tree)
            self.play(ReplacementTransform(tree.all, row.all), ReplacementTransform(tree.group, row.group),
                      ReplacementTransform(tree.leaf, row.leaf), ReplacementTransform(tree.edges, row.edges),
                      run_time=0.8)
            self.remove(tree)
            self.add(row)
            self.play(TransformFromCopy(row.all, p1), run_time=0.9)
            vo.wait_until("Ansible logs in")
            self.play(FadeIn(b3), run_time=0.4)
            self.play(Indicate(code_span(p1.code, 2, "ubuntu"), color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("Line 4 points")
            self.play(FadeIn(b4), run_time=0.4)
            self.play(Indicate(code_span(p1.code, 3, '"/root/.ssh/ac215_2024.pem"'), color=TURN, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("line 7, commented out")
            self.play(FadeIn(b7), run_time=0.4)
            self.play(FadeIn(bookmark, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Lines 9 to 11")
            self.play(FadeIn(b911), run_time=0.5)
            vo.wait_until("from the environment")
            self.play(FadeIn(env, shift=UP * 0.1), LaggedStart(*[GrowArrow(x) for x in env_arrows], lag_ratio=0.2),
                      run_time=0.9)
            vo.wait_until("nothing to type")
            self.play(Indicate(env.text, color=IMAGE, scale_factor=1.08), run_time=0.8)

        # ========================================================== 3. inventory.yml lines 14-25
        p2 = code(INV, 14, 25, font_size=20)
        p2.move_to([-6.45 + p2.width / 2, 2.75 - p2.height / 2, 0])
        b14, b15 = bar(p2, 14, 14, CLOUD), bar(p2, 14, 15, CLOUD)
        b16 = bar(p2, 14, 16, TURN)
        b17 = bar(p2, 14, 17, CLOUD)
        b2122 = bars(p2, 14, 21, 22, CLOUD)
        per = cloud_chip("per region")
        per.move_to([p2.get_right()[0] + 0.25 + per.width / 2, line_y(p2, 14, 17), 0])
        ami = label_box(["if step 6 says InvalidAMIID:", "pick a current Ubuntu image", "in EC2 › AMIs, us-east-1"],
                        S.GREY)
        ami.next_to(per, DOWN, buff=0.2).align_to(per, LEFT)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(b3, b4, b7, bookmark, b911, env, env_arrows)), run_time=0.4)
            self.play(FadeTransform(p1, p2), run_time=0.9)
            self.remove(p1)
            self.add(p2)
            vo.wait_until("the region")
            self.play(FadeIn(b14), run_time=0.4)
            self.play(Indicate(code_span(p2.code, 0, "us-east-1"), color=CLOUD, scale_factor=1.12), run_time=0.6)
            vo.wait_until("and a T 2 large")
            self.play(FadeIn(b15), run_time=0.4)
            self.play(Indicate(code_span(p2.code, 1, "t2.large"), color=CLOUD, scale_factor=1.12), run_time=0.6)
            vo.wait_until("The key pair name")
            self.play(FadeIn(b16), run_time=0.4)
            vo.wait_until("marked change this")
            self.play(Indicate(code_span(p2.code, 2, "## Change this"), color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("An Ubuntu machine image")
            self.play(FadeIn(b17), FadeIn(per, shift=LEFT * 0.1), run_time=0.5)
            self.play(FadeIn(ami, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and the disk names")
            self.play(FadeIn(b2122), run_time=0.5)
            self.play(Indicate(code_span(p2.code, 8, "50"), color=CLOUD, scale_factor=1.25), run_time=0.6)

        # ========================================================== 4. the README's four bullets
        rp = readme_panel(67, 72, size=20, card_w=4.0)
        rp.move_to([-6.5 + rp.width / 2, 2.75 - rp.height / 2, 0])
        dx = 6.55 - p2.get_right()[0]
        p2_right = p2.copy().shift(RIGHT * dx)
        # targets measured on the moved copy
        gap_x = (rp.get_right()[0] + p2_right.get_left()[0]) / 2
        y14 = p2_right.code.code_lines[0].get_top()[1]
        y23 = p2_right.code.code_lines[9].get_bottom()[1]
        y16 = p2_right.code.code_lines[2].get_center()[1]
        bracket = Line([gap_x + 0.12, y14, 0], [gap_x + 0.12, y23, 0], color=TURN, stroke_width=4)
        tick2 = check_mark(0.3, TURN).move_to([gap_x - 0.08, (y14 + y23) / 2 - 0.4, 0])
        tick4 = check_mark(0.3, TURN).move_to([gap_x - 0.08, y16, 0])
        seen1 = grey_chip("line 3 ✓ (seen)")
        seen3 = grey_chip("lines 9–11 ✓ (seen)")
        VGroup(seen1, seen3).arrange(DOWN, buff=0.1, aligned_edge=LEFT).next_to(rp, DOWN, buff=0.12) \
            .align_to(rp, LEFT)
        strip = term(P_HOME, rows=1)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(b14, b15, b17, b2122, per, ami)), FadeOut(row), run_time=0.5)
            self.play(VGroup(p2, b16).animate.shift(RIGHT * dx), FadeIn(rp, shift=RIGHT * 0.2), run_time=0.8)
            vo.wait_until("point at exactly these lines")
            self.play(LaggedStart(
                Succession(FadeIn(t2 := check_mark(0.3, TURN).move_to(rp.rows[70][0].get_left() + LEFT * 0.2)),
                           Transform(t2, tick2)),
                Succession(FadeIn(t4 := check_mark(0.3, TURN).move_to(rp.rows[72][0].get_left() + LEFT * 0.2)),
                           Transform(t4, tick4)), lag_ratio=0.4), Create(bracket), run_time=1.4)
            self.play(LaggedStart(TransformFromCopy(rp.rows[69], seen1), TransformFromCopy(rp.rows[71], seen3),
                                  lag_ratio=0.4), run_time=1.0)
            vo.wait_until("Change two now")
            self.play(Indicate(rp.rows[72], color=TURN, scale_factor=1.04), run_time=0.6)
            vo.wait_until("the key pair name, unless")
            self.play(Indicate(code_span(p2.code, 2, '"ac215_2024"'), color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("and line 24")
            b24 = bar(p2, 14, 24, TURN)
            yt = on_bar(strip, turn_row())
            self.play(FadeIn(b24), run_time=0.3)
            self.play(FadeOut(VGroup(seen1, seen3)), FadeIn(strip, shift=UP * 0.2), FadeIn(yt), run_time=0.4)
            ln = type_cmd(self, strip, "openssl rand -base64 32", type_time=0.7)
            pin(self, ln, beside(extra_row(), ln))
            sh = beside(row_tag("written out, not run"), ln, buff=0.3 + extra_row().width + 0.45 + 0.15)
            pin(self, ln, sh)
            self.play(Indicate(code_span(p2.code, 10, '"<nextauth-secret>"'), color=TURN, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("comes later")
            self.play(FadeOut(VGroup(rp, t2, t4, bracket, b16, b24, yt, strip)), run_time=0.5)
            self.remove(strip, ln)
            p3 = code(INV, 27, 30, font_size=20)
            p3.move_to([0, 0.9, 0])
            self.play(FadeIn(row), FadeTransform(p2, p3), run_time=0.8)
            self.remove(p2)
            self.add(p3)
            p3.code.code_lines[3].set_color(S.GREY)
            r30 = ring(p3.code.code_lines[3], S.GREY, buff=0.03, stroke=2.5, dashed=True)
            after = grey_chip("after the server exists")
            after.next_to(r30, RIGHT, buff=0.25)
            self.play(Create(r30), FadeIn(after, shift=LEFT * 0.1), run_time=0.5)
        self.wait(0.5)
        new_leaf = leaf_box(EXTERNAL_IP, dashed=True).move_to(row.leaf)
        l30 = p3.code.code_lines[3]
        rest = VGroup(*[m for m in p3.get_family() if m is not p3 and not m.submobjects
                        and m not in l30.get_family()])
        self.play(FadeOut(VGroup(rest, after)), run_time=0.4)
        self.remove(p3)
        self.add(l30, r30)
        self.play(ReplacementTransform(l30, new_leaf.text), ReplacementTransform(r30, new_leaf.frame),
                  FadeOut(row.leaf), run_time=0.9)
        self.remove(new_leaf.text, new_leaf.frame)
        row.remove(row.leaf)
        self.remove(row.leaf)
        row.add(new_leaf)
        row.leaf = new_leaf
        self.add(row)

        # ========================================================== 5. the recap; ok on a second run
        rc = PlayRecap()
        greys = {k: chip(f"{k}=0", S.GREY, size=20, font=MONO).move_to(rc.cells[k]) for k in ("unreachable", "failed")}
        for k, g in greys.items():
            rc.cells[k].become(g)
        card = PlayCard("deploy-provision-instance.yml", "Configure app server instance", "appserver",
                        [("apt", "state: present"), ("shell", "lsb_release -cs")], cols=2, mono_tiles=True)
        with self.voiceover(SAY[5]) as vo:
            self.play(row.animate.move_to([0, 2.15, 0]), run_time=0.7)
            rc.move_to([0, 1.0, 0])
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("success means")
            self.play(rc.flash("failed", S.GREY), rc.flash("unreachable", S.GREY), run_time=0.8)
            vo.wait_until("stay at zero")
            self.play(*[Transform(rc.cells[k], chip(f"{k}=0", PASS, size=20, font=MONO).move_to(rc.cells[k]))
                        for k in ("unreachable", "failed")], run_time=0.5)
            self.play(rc.flash("failed"), rc.flash("unreachable"), run_time=0.7)
            vo.wait_until("A declarative task")
            card.move_to([-0.9, -1.55, 0])
            rn = run_chip(1).next_to(card.frame, RIGHT, buff=0.3)
            self.play(FadeIn(card, shift=UP * 0.15), FadeIn(rn), run_time=0.6)
            self.play(card.set_state(0, "changed"), card.set_state(1, "changed"), run_time=0.5)
            rc.set(self, "ok", 2, run_time=0.3)
            rc.set(self, "changed", 2, run_time=0.3)
            vo.wait_until("reports ok the second time")
            self.play(Transform(rn, run_chip(2).move_to(rn)), card.set_state(0, "idle"), card.set_state(1, "idle"),
                      run_time=0.5)
            self.play(card.set_state(0, "ok"), run_time=0.5)
            self.play(card.set_state(1, "changed"), run_time=0.5)
            rc.set(self, "changed", 1, run_time=0.4)
        self.play(Indicate(card.tiles[0].text, color=PASS, scale_factor=1.15), rc.flash("ok"), run_time=0.9)
        self.wait(0.6)
        self.play(FadeOut(VGroup(tr, row, rc, card, rn)), run_time=0.7)
        self.wait(0.3)
