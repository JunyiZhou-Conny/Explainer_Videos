"""S10 · Setup: four APIs, two keys (AC215 L20). No tracker (beat 0), TRACKER [P] 1 (beat 1),
2 (beats 2-4), 2 · extra (beats 5-6). Lecture: 20 · 19 (beat 0), 20 · 20 (beat 1), 20 · 25 (beat 4).

Beats (script.md "## S10", one voiceover block each):
0. No tracker. LECTURE 20 · 19. The V1 automated variant opens the scene: the GREY 'Your Machine'
   laptop box (left, from MasterDiagram) and an empty dotted BLUE 'GCP' outline. Slide 19's six-step
   strip builds chip by chip above them while the narration lists the steps; on "Each maps to a file"
   the six files write under their chips; on "we start with step 1" chip 1 'Setup' turns YELLOW and
   the laptop's outline flashes YELLOW.
1. TRACKER [P] 1 (the tracker appears). LECTURE 20 · 20. The strip shrinks away; the laptop and the
   GCP outline rise a little and a schematic checklist 'APIs & Services' (tag `illustration`, no logo)
   appears inside the GCP outline; the four APIs tick GREEN one per phrase; the fifth, GREY-dashed row
   'Vertex AI API · from earlier lectures' flashes and ticks GREY on "Vertex AI".
2. TRACKER [P] 2. The laptop, the outline and the checklist leave. V8 KeyRing opens on the right (two
   rows: 'builds things' create · SSH · delete, 'runs things' read images · read stored files · use
   Vertex AI). A schematic IAM form (tag `illustration`) slides in on the left: 'Create service
   account', name `deployment`, the README's six roles (README:241-246) as GREY chips, a 'Create key ·
   JSON' button. The four named roles flash on their phrase; the six chips fly onto row 1's doors,
   which turn BLUE. On "Create a JSON key" the button flashes and a dashed '….json' file drops out of
   it; on "rename it" the file morphs into the `deployment.json` key (BLUE, RED rim) on row 1's hook.
3. The same form for `gcp-service` (the name morphs; three new chips, README:253-255) beside row 2;
   the chips fly onto row 2's doors (GREEN); the '….json' file becomes the `gcp-service.json` key.
4. LECTURE 20 · 25. The form leaves; the finished KeyRing moves to the centre. 'builds things' and
   the deployment key flash; on "It needs admin rights" the GREY line 'admin on your group's project'
   appears under the card with 'your' YELLOW beside a struck GREY `ac215-project`; on "not the
   README's default" the struck name flashes; 'runs things' and its three doors flash one per phrase.
5. TRACKER [P] 2 · extra. The KeyRing leaves; its two keys fly into the `secrets/` node of a small
   folder tree top right (~/ with `cheese-app-v3/` › `src/` › `deployment/` and `secrets/` beside the
   clone). A 9-row `laptop` terminal: `git clone …` (p01:1, extra · our spelling) types and dims GREY;
   a GREY row chip 'your keys → secrets/ (README:249, 258)' stands for p04 on its own prompt row;
   p05:1 (extra; folds) -> TERM(p05: 6–7, 11–12): `cheese-app-v3` and `secrets` YELLOW, the two key
   files GREEN. On "The deployment script" a PINK arrow climbs from `deployment/` three folders up
   (three '../' hops) and over to `secrets/`, with the GREY 'docker-shell.sh:9' over the PINK chip
   `../../../secrets/` on the left. YELLOW '▶ your turn' beside p05's command.
6. The terminal and the tree leave. A GREY card 'Nothing creates the registry repository' with an
   `erratum` tag; a GREY card (tag `extra · not in the README`, no output panel) with the folded
   `gcloud artifacts repositories create cheese-app-repository --repository-format=docker
   --location=us`; a GREY chip 'you run it in the next step, in the container', a GREEN chip 'look
   for: Created repository', a RED dashed ghost 'skip it → the push fails'. Fade; empty frame.

Deviations from SHOW:
- Beat 0: the laptop box and the GCP outline come first (they fill the opening sentence, which is
  otherwise silent on screen) and sit under the strip; the outline is drawn here rather than
  MasterDiagram's, which does not fit under a strip.
- Beat 1: the checklist sits inside the GCP outline (the APIs are switched on in your project), and
  the laptop stays on the left as the 'Your Machine' half of the V1 picture.
- Beats 2-3: the form holds the role chips itself (one column); they fly onto the row's doors. The
  downloaded key is a dashed '….json' file (no invented file name) that morphs into the named key.
- Beat 5: the 'three folders up' is drawn as a small folder tree (not in SHOW) so the arrow has
  folders to climb; the p04 chip stands on its own prompt row inside the terminal, where the command
  would be; the docker-shell.sh:9 chip is split into a GREY source line and a PINK path chip to fit.
  The terminal has 9 rows, not 3 (p01's two rows, the p04 row, p05's two rows and four output rows).
- Beat 6: the GREY chip says 'you run it in the next step, in the container' instead of naming S11
  (scene numbers are not on screen); the tracker shows ' · extra · not in the README'.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from common import _dotted_rect

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ the real sources (checked)
P01, P04, P05 = capture("p01"), capture("p04"), capture("p05")
assert P01.cmd == "git clone https://github.com/dlops-io/cheese-app-v3.git", P01.cmd
assert P04.cmd == "mkdir -p secrets" and not P04.lines, P04.lines
assert P05.cmd.startswith("ls -la; ls -la secrets; ls cheese-app-v3/src"), P05.cmd
assert P05.line(6).endswith(" cheese-app-v3") and P05.line(7).endswith(" secrets"), P05.at(6, 7)
assert P05.line(11).endswith(" deployment.json") and P05.line(12).endswith(" gcp-service.json"), P05.at(11, 12)
assert readme(234).strip() == "* Artifact Registry API" and readme(231).strip() == "* Compute Engine API"
assert [readme(n).strip(" -") for n in range(241, 247)] == list(ROLES_DEPLOY)
assert [readme(n).strip(" -") for n in range(253, 256)] == list(ROLES_SERVICE)
assert "deployment.json" in readme(250) and "gcp-service.json" in readme(259)
assert "secrets" in readme(249) and "secrets" in readme(258)
assert excerpt("src/deployment/docker-shell.sh", 9, 9).strip() == "export SECRETS_DIR=$(pwd)/../../../secrets/"
APIS = ["Compute Engine API", "Service Usage API", "Cloud Resource Manager API", "Artifact Registry API",
        "Vertex AI API · from earlier lectures"]
# not in the README (digest errata 1, BRIEF erratum 11): typed nowhere, shown as a card only
GCLOUD = ("gcloud artifacts repositories create cheese-app-repository \\",
          "    --repository-format=docker --location=us")

FORM_X = -6.45                 # the IAM form's left edge (beats 2-3)
FORM_W = 5.1
KR_SHIFT = np.array([2.65, -0.35, 0])


def iam_form(name: str, roles) -> VGroup:
    """Schematic 'Create service account' page (GREY, no logo, tag `illustration`): title, a name row,
    the README's roles as GREY chips in a column, a 'Create key · JSON' button.
    .frame .title .name .chips .button .tag"""
    tt = label("Create service account", 22, INK)
    nm_l = label("name", 20, S.GREY)
    nm = mono(name, 20, TURN)
    nrow = VGroup(nm_l, nm).arrange(RIGHT, buff=0.25)
    rl = label("roles", 20, S.GREY)
    chips = VGroup(*[grey_chip(r) for r in roles]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    btn = chip("Create key · JSON", S.GREY, size=20, fill_opacity=0.3)
    inner = VGroup(tt, nrow, rl, chips, btn).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    chips.shift(RIGHT * 0.2)
    if inner.width > FORM_W - 0.5:
        raise ValueError(f"iam_form: {inner.width:.2f} wide")
    fr = box(FORM_W, inner.height + 0.6, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.28)
    tg = illustration_tag()
    tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - 0.2, 0, 0]))
    g = VGroup(fr, tt, nrow, rl, chips, btn, tg)
    g.frame, g.title, g.name, g.chips, g.button, g.tag, g.roles_label = fr, tt, nm, chips, btn, tg, rl
    return g


def light(scene, c, col) -> None:
    """A named role chip lights up in its row's colour and stays lit until it flies."""
    scene.play(c.box.animate.set_stroke(col).set_fill(col, 0.25), Indicate(c.text, color=col, scale_factor=1.08),
               run_time=0.5)
    c.text.set_color(INK)


def json_file() -> VGroup:
    """The downloaded key, unnamed: a dashed GREY file card '….json'."""
    return file_card("….json", S.GREY, dashed=True)


def fly(scene, kr, row: int, chips) -> None:
    """The role chips fly into the row's doors, which open (BLUE row 0, GREEN row 1), as
    KeyRing.roles() does, for chips that already stand in the form."""
    doors = kr.doors[row]
    col = CLOUD if row == 0 else OWN
    moves = [c.animate.move_to(doors[i % len(doors)].frame).set_opacity(0) for i, c in enumerate(chips)]
    scene.play(LaggedStart(*moves, lag_ratio=0.12),
               *[d.frame.animate.set_stroke(col).set_fill(tint(col, 0.2), 1) for d in doors], run_time=1.1)
    scene.remove(*chips)
    kr.heal(scene)


def hang_key(scene, kr, row: int, src) -> VGroup:
    """`src` (the '….json' file on screen) morphs into the row's named key on its hook."""
    k = key_icon("deploy" if row == 0 else "service", True, 0.9)
    k.next_to(kr.hooks[row], DOWN, buff=0.05)
    kr.keys[row] = k
    scene.play(ReplacementTransform(src, k), run_time=0.8)
    scene.remove(src, k)
    kr.add(k)
    kr.heal(scene)
    return k


def folder_node(name: str, x: float, y: float, color=INK) -> VGroup:
    gl = folder_icon(0.26, color)
    t = mono(name, 20, color)
    g = VGroup(gl, t).arrange(RIGHT, buff=0.12).move_to([x, y, 0], aligned_edge=LEFT)
    g.glyph, g.text = gl, t
    return g


def folder_tree() -> VGroup:
    """~/ with cheese-app-v3/ › src/ › deployment/ and secrets/ beside the clone (right half of the
    frame, over the 9-row terminal). .home .clone .src .dep .secrets .lines"""
    home = folder_node("~/", 1.0, 2.58, S.GREY)
    clone = folder_node("cheese-app-v3/", 1.6, 2.15)
    secrets = folder_node("secrets/", 4.68, 2.15, LAPTOP)
    src = folder_node("src/", 2.2, 1.72)
    dep = folder_node("deployment/", 2.8, 1.29)
    lines = VGroup()
    for parent, child in ((home, clone), (clone, src), (src, dep)):
        x = parent.glyph.get_center()[0]
        a = [x, parent.get_bottom()[1] - 0.03, 0]
        b = [x, child.get_center()[1], 0]
        c = [child.glyph.get_left()[0] - 0.06, child.get_center()[1], 0]
        lines.add(VMobject().set_points_as_corners([a, b, c]).set_stroke(S.GREY_DARK, 2))
    x = home.glyph.get_center()[0]
    ln = VMobject().set_points_as_corners([[x, home.get_bottom()[1] - 0.03, 0], [x, 2.37, 0],
                                           [secrets.glyph.get_left()[0] - 0.06, 2.37, 0],
                                           [secrets.glyph.get_left()[0] - 0.06, secrets.get_center()[1], 0]])
    lines.add(ln.set_stroke(S.GREY_DARK, 2))
    g = VGroup(lines, home, clone, secrets, src, dep)
    g.home, g.clone, g.secrets, g.src, g.dep, g.lines = home, clone, secrets, src, dep, lines
    return g


class TwoKeys(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S10"] == 7, len(SAY)

        # ========================================================== 0. slide 19: six steps, step 1
        ref19 = lref("19")
        ss = six_steps(0)
        ss.move_to([0, 0, 0]).shift(UP * (2.95 - ss.get_top()[1]))
        assert ss.get_top()[1] < ref19.get_bottom()[1] - 0.1, (ss.get_top(), ref19.get_bottom())
        md = MasterDiagram()
        md.shift(DOWN * 1.5)                    # laptop box y -1.15 .. 1.15
        gcp = VGroup(_dotted_rect(8.9, 4.4, CLOUD).move_to([1.9, -1.05, 0]))
        gcp.add(label("GCP", 22, CLOUD).move_to(gcp[0].get_corner(UL) + np.array([0.2, -0.32, 0]), aligned_edge=LEFT))
        assert gcp.get_top()[1] < ss.get_bottom()[1] - 0.1 and gcp.get_bottom()[1] > -3.45, gcp.get_bottom()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref19), run_time=0.4)
            lap = md.laptop(self)
            self.play(Create(gcp[0]), FadeIn(gcp[1]), run_time=0.8)
            self.play(Indicate(lap.title, color=INK, scale_factor=1.1), run_time=0.6)
            md.heal(self)
            vo.wait_until("setup, images")
            for c in ss.chips:
                self.play(FadeIn(c, shift=DOWN * 0.15), run_time=0.45)
            vo.wait_until("Each maps to a file")
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in ss.files], lag_ratio=0.15), run_time=1.0)
            self.remove(*ss.chips, *ss.files)
            self.add(ss)
            vo.wait_until("we start with step 1")
            self.play(ss.goto(1), run_time=0.4)
            self.play(ss.light(1), lap.frame.animate(rate_func=there_and_back).set_stroke(TURN, width=5), run_time=0.8)
            self.add(ss)
            md.heal(self)

        # ========================================================== 1. slide 20: four APIs
        trk = tracker_p(1)
        ref20 = lref("20")
        lift = UP * 0.55
        ck = Checklist("APIs & Services", APIS, dashed=(4,))
        ck.move_to(gcp[0].get_center() + lift + RIGHT * 0.45)
        assert ck.get_top()[1] < gcp[0].get_top()[1] + 0.55 - 0.15, (ck.get_top(), gcp[0].get_top())
        assert ck.get_left()[0] > gcp[1].get_right()[0] + 0.2
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(ref19), run_time=0.3)
            self.remove(ref19)
            ss.shrink_away(self)
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref20), md.animate.shift(lift),
                      gcp.animate.shift(lift), run_time=0.6)
            self.play(FadeIn(ck, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Compute Engine")
            ck.tick(self, 0)
            vo.wait_until("Service Usage")
            ck.tick(self, 1)
            vo.wait_until("Cloud Resource Manager")
            ck.tick(self, 2)
            vo.wait_until("Artifact Registry")
            ck.tick(self, 3)
            vo.wait_until("The app's chat also needs Vertex AI")
            self.play(Indicate(ck.rows[4].text, color=INK, scale_factor=1.05), run_time=0.6)
            ck.heal(self)
            ck.tick(self, 4, color=S.GREY)

        # ========================================================== 2. deployment: six roles, one key
        kr = KeyRing()
        kr.shift(KR_SHIFT)
        f1 = iam_form("deployment", ROLES_DEPLOY)
        f1.move_to([FORM_X + FORM_W / 2, 0, 0]).shift(UP * (2.55 - f1.frame.get_top()[1]))
        assert f1.get_bottom()[1] > -3.5, f1.get_bottom()
        assert f1.tag.get_top()[1] < TRACK_BOTTOM - 0.05, f1.tag.get_top()
        assert f1.get_right()[0] < kr.frame.get_left()[0] - 0.2, (f1.get_right(), kr.frame.get_left())
        assert kr.frame.get_right()[0] < 6.5 and kr.frame.get_top()[1] < TRACK_BOTTOM
        named = [0, 1, 2, 5]                         # the four roles the narration names
        jf1 = json_file().next_to(f1.button, UP, buff=0.35).align_to(f1.button, LEFT)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(md, gcp, ck, ref20)), track(trk, 2), run_time=0.6)
            self.remove(md, gcp, ck, ref20)
            self.play(FadeIn(kr), run_time=0.6)
            shell = VGroup(f1.frame, f1.title, f1[2], f1.roles_label, f1.button, f1.tag)
            self.play(FadeIn(shell, shift=RIGHT * 0.3), run_time=0.6)
            self.remove(shell)
            f1.remove(f1.chips)
            self.add(f1)
            vo.wait_until("Deployment gets six roles")
            self.play(Indicate(f1.name, color=TURN, scale_factor=1.12), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in f1.chips], lag_ratio=0.12), run_time=0.8)
            for i, ph in zip(named, ("Compute Admin", "Compute OS Login", "Artifact Registry Administrator",
                                     "and Storage Admin")):
                vo.wait_until(ph)
                light(self, f1.chips[i], CLOUD)
            fly(self, kr, 0, f1.chips)
            vo.wait_until("Create a JSON key")
            flash_tag(self, f1.button, INK)
            self.play(FadeIn(jf1, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("and rename it")
            hang_key(self, kr, 0, jf1)

        # ========================================================== 3. gcp-service: three roles, one key
        f2 = iam_form("gcp-service", ROLES_SERVICE)
        f2.move_to([FORM_X + FORM_W / 2, 0, 0]).shift(UP * (kr.frame.get_bottom()[1] + 0.05 - f2.frame.get_bottom()[1]))
        assert f2.tag.get_top()[1] < TRACK_BOTTOM - 0.05
        jf2 = json_file().next_to(f2.button, UP, buff=0.35).align_to(f2.button, LEFT)
        assert jf2.get_top()[1] < f2.roles_label.get_bottom()[1] - 0.1 and jf2.get_right()[0] < f2.frame.get_right()[0] - 0.2
        with self.voiceover(SAY[3]) as vo:
            self.play(ReplacementTransform(f1.frame, f2.frame), ReplacementTransform(f1.title, f2.title),
                      ReplacementTransform(f1[2], f2[2]), ReplacementTransform(f1.roles_label, f2.roles_label),
                      ReplacementTransform(f1.button, f2.button), ReplacementTransform(f1.tag, f2.tag), run_time=0.8)
            self.remove(f1, *f1.get_family(), *f2.get_family())
            f2.remove(f2.chips)
            self.add(f2)
            self.play(Indicate(f2.name, color=TURN, scale_factor=1.12), run_time=0.5)
            vo.wait_until("gets three roles")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in f2.chips], lag_ratio=0.15), run_time=0.6)
            for c, ph in zip(f2.chips, ("Storage Object Viewer", "Vertex AI Administrator",
                                        "and Artifact Registry Reader")):
                vo.wait_until(ph)
                light(self, c, OWN)
            fly(self, kr, 1, f2.chips)
            vo.wait_until("Its key becomes")
            flash_tag(self, f2.button, INK, 1.12, 0.5)
            self.play(FadeIn(jf2, shift=UP * 0.2), run_time=0.4)
            hang_key(self, kr, 1, jf2)

        # ========================================================== 4. slide 25: why two?
        ref25 = lref("25")
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(f2, shift=LEFT * 0.3), run_time=0.4)
            self.remove(f2)
            self.play(kr.animate.shift(-KR_SHIFT + UP * 0.35), FadeIn(ref25), run_time=0.8)
            vo.wait_until("Deployment builds things")
            def row_box(r):
                return SurroundingRectangle(VGroup(kr.heads[r], *[d.frame for d in kr.doors[r]], kr.keys[r]),
                                            color=TURN, buff=0.07, corner_radius=0.08, stroke_width=3)
            focus = row_box(0)
            self.play(Create(focus), Indicate(kr.heads[0], color=TURN, scale_factor=1.15),
                      Indicate(kr.keys[0].glyph, color=CLOUD), run_time=0.7)
            kr.heal(self)
            self.add(focus)                 # heal() re-seats the card on top
            vo.wait_until("It needs admin rights")
            yp = kr.your_project(self)
            self.add(focus)
            your = yp[0][1]
            your.set_opacity(1)             # your_project()'s Indicate leaves 'your' invisible (common.py)
            self.play(Indicate(your, color=TURN, scale_factor=1.3), run_time=0.6)
            kr.heal(self)
            self.add(focus)                 # heal() re-seats the card on top
            vo.wait_until("not the README's default")
            self.play(Indicate(yp[1], color=S.GREY, scale_factor=1.12), run_time=0.6)
            kr.heal(self)
            self.add(focus)                 # heal() re-seats the card on top
            vo.wait_until("to create the VM")
            self.play(Indicate(kr.doors[0][0].text, color=CLOUD, scale_factor=1.15), run_time=0.6)
            vo.wait_until("and log in")
            self.play(Indicate(kr.doors[0][1].text, color=CLOUD, scale_factor=1.15), run_time=0.6)
            kr.heal(self)
            self.add(focus)                 # heal() re-seats the card on top
            vo.wait_until("The narrow account only runs things")
            self.play(Transform(focus, row_box(1)), Indicate(kr.heads[1], color=TURN, scale_factor=1.15),
                      Indicate(kr.keys[1].glyph, color=OWN), run_time=0.7)
            kr.heal(self)
            self.add(focus)                 # heal() re-seats the card on top
            vo.wait_until("it reads images")
            self.play(Indicate(kr.doors[1][0].text, color=OWN, scale_factor=1.1), run_time=0.5)
            vo.wait_until("and stored files")
            self.play(Indicate(kr.doors[1][1].text, color=OWN, scale_factor=1.1), run_time=0.5)
            vo.wait_until("and uses Vertex AI")
            self.play(Indicate(kr.doors[1][2].text, color=OWN, scale_factor=1.1), run_time=0.5)
            kr.heal(self)
            self.add(focus)                 # heal() re-seats the card on top
            self.play(FadeOut(focus), run_time=0.3)
            self.remove(focus)

        # ========================================================== 5. secrets/ next to the clone
        tree = folder_tree()
        t = term(P_LAPTOP, 10, T_LAPTOP, size=20)
        assert tree.dep.get_bottom()[1] > t.box.get_top()[1] + 0.08, (tree.dep.get_bottom(), t.box.get_top())
        assert tree.home.get_top()[1] < PIC_TOP and tree.secrets.get_right()[0] < 6.45
        kd = [key_icon("deploy", False, 0.55), key_icon("service", False, 0.55)]
        VGroup(*kd).arrange(RIGHT, buff=0.2).next_to(tree.secrets, DOWN, buff=0.2).align_to(tree.secrets.glyph, LEFT)
        assert kd[1].get_right()[0] < 6.5 and kd[0].get_bottom()[1] > t.box.get_top()[1] + 0.08
        src_l = label("docker-shell.sh:9", 20, S.GREY)
        path_c = route_chip("../../../secrets/")
        VGroup(src_l, path_c).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-6.4, 1.55, 0], aligned_edge=LEFT)
        assert path_c.get_right()[0] < tree.home.get_left()[0] - 0.3 and src_l.get_top()[1] < TRACK_BOTTOM - 0.1
        # the climb: three '../' hops on the tree's left side, then over to secrets/
        nodes = (tree.dep, tree.src, tree.clone, tree.home)
        hops = VGroup()
        for a, b in zip(nodes[:-1], nodes[1:]):
            hops.add(CurvedArrow(a.glyph.get_left() + LEFT * 0.08, b.glyph.get_left() + LEFT * 0.08, angle=-PI / 2.2,
                                 color=ROUTE, stroke_width=4, tip_length=0.16))
        over = CurvedArrow(tree.home.get_right() + RIGHT * 0.1, tree.secrets.get_top() + UP * 0.06, angle=-PI / 7,
                           color=ROUTE, stroke_width=4, tip_length=0.16)
        assert over.get_top()[1] < PIC_TOP + 0.05, over.get_top()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(ref25), track(trk, 2, True), run_time=0.4)
            self.remove(ref25)
            self.play(FadeIn(tree.lines), *[FadeIn(n) for n in (tree.home, tree.clone, tree.secrets, tree.src, tree.dep)],
                      kr.animate.shift(DOWN * 0.3).set_opacity(0.0), run_time=0.6)
            gk = [kr.keys[0].glyph.copy(), kr.keys[1].glyph.copy()]
            self.remove(kr)
            self.add(*gk)
            self.play(*[ReplacementTransform(g, k) for g, k in zip(gk, kd)],
                      Indicate(tree.secrets.text, color=TURN, scale_factor=1.12), run_time=0.8)
            self.remove(*gk)
            self.add(*kd)
            self.play(FadeIn(t, shift=UP * 0.3), run_time=0.4)
            cl = type_capture(self, t, P01, type_time=0.7)[0]
            pin(self, cl, beside(extra_row("our spelling"), cl))
            self.play(*[r.glyphs.animate.set_color(S.GREY_DARK) for r in rows_of(cl)], run_time=0.3)
            self.add(t)
            ph = bare_prompt(self, t)
            ph.bare = False                      # keep this row: it stands for p04
            pin(self, ph, beside(row_tag("your keys → secrets/ (README:249, 258)"), ph, buff=0.2))
            vo.wait_until("not inside it")
            ls = type_capture(self, t, P05, type_time=0.8)[0]
            xr = beside(extra_row(), ls)
            pin(self, ls, xr)
            rows = out(self, t, P05.at(6, 7, 11, 12), wrap=True, run_time=0.6)
            self.play(substring(rows[0], "cheese-app-v3").animate.set_color(TURN),
                      substring(rows[1], "secrets").animate.set_color(TURN), run_time=0.4)
            self.play(substring(rows[2], "deployment.json").animate.set_color(OWN),
                      substring(rows[4], "gcp-service.json").animate.set_color(OWN), run_time=0.4)
            self.add(t)
            vo.wait_until("The deployment script of the next step")
            self.play(Indicate(tree.dep.text, color=ROUTE, scale_factor=1.1), FadeIn(src_l, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("three folders up")
            for h in hops:
                self.play(Create(h), run_time=0.45)
            self.play(Create(over), FadeIn(path_c, shift=RIGHT * 0.2), run_time=0.6)
            self.play(Indicate(tree.secrets.text, color=ROUTE, scale_factor=1.15), run_time=0.5)
            vo.wait_until("Pause and place your keys")
            yt = beside(turn_row(), ls, min_x=xr.get_right()[0] + 0.2)
            pin(self, ls, yt)
            flash_tag(self, yt, TURN)
            self.add(t)

        # ========================================================== 6. the missing registry repository
        err = card(["Nothing creates the registry repository"], size=22)
        err.move_to([0, 1.75, 0])
        et = erratum_tag().next_to(err.frame, UP, buff=0.08).align_to(err.frame, RIGHT)
        cmd = VGroup(*[mono(s, 20, INK) for s in GCLOUD]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        gc = card([cmd])
        gc.move_to([0, -0.05, 0])
        xt = extra_tag("not in the README")
        xt.next_to(gc.frame, UP, buff=0.08).align_to(gc.frame, RIGHT)
        nxt = grey_chip("you run it in the next step, in the container")
        look = ok_chip("look for: Created repository")
        ghost = dashed_chip("skip it → the push fails", ERR)
        nxt.move_to([0, -1.4, 0])
        VGroup(look, ghost).arrange(RIGHT, buff=0.5).move_to([0, -2.3, 0])
        assert err.get_top()[1] < TRACK_BOTTOM - 0.15 and gc.get_left()[0] > -6.5 and gc.get_right()[0] < 6.5
        assert et.get_top()[1] < TRACK_BOTTOM - 0.05 and xt.get_top()[1] < err.get_bottom()[1] - 0.1
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(t, tree, *kd, hops, over, src_l, path_c)), run_time=0.5)
            self.remove(t, tree, *kd, hops, over, src_l, path_c)
            self.play(FadeIn(err, shift=DOWN * 0.15), FadeIn(et), run_time=0.6)
            vo.wait_until("nothing creates")
            self.play(Indicate(err.body[0], color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("the Artifact Registry repository")
            flash_tag(self, et, S.GREY, 1.12, 0.6)
            vo.wait_until("We create it with one extra gcloud line")
            self.play(FadeIn(gc, shift=UP * 0.15), FadeIn(xt), track(trk, 2, "extra · not in the README"), run_time=0.6)
            self.play(Indicate(cmd[0], color=TOOL, scale_factor=1.03), run_time=0.6)
            vo.wait_until("in the next step")
            self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(look, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("skip it, and the push fails")
            self.play(FadeIn(ghost, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(ghost.text, color=ERR, scale_factor=1.08), run_time=0.6)

        self.play(FadeOut(VGroup(trk, err, et, gc, xt, nxt, look, ghost)), run_time=0.6)
        self.remove(trk, err, et, gc, xt, nxt, look, ghost)
        self.wait(0.3)
