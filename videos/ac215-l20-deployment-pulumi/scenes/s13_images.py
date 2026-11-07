"""S13 · Step 2: images with timestamps (AC215 L20). No tracker (beats 0-2), TRACKER [P] 9 (3-5),
9 · extra · not for you (4), 9 · extra (5), 10 (6-7), 10 · extra (8-9), 10 (9 end-10).
Lecture: 20 · 19, 21 (beat 0), 20 · 13, 18 (beats 1-2).

Beats (script.md "## S13", one voiceover block each):
0. No tracker. LECTURE 20 · 19, 21. The six-step strip: chip 1 YELLOW turns to a GREEN tick and chip
   2 'Images · deploy_images/' turns YELLOW on "Step 2"; the strip shrinks away. V1 at slide 21: the
   GREY 'Your Machine' box, the dotted BLUE GCP outline and the BLUE 'Artifact Registry' panel with
   three image bars (bottom left of GCP); on "Your laptop's arrow" the push arrow grows onto the
   registry. On "slide 21 still calls it GCR" a GREY '(GCR on the slides)' appears over the panel; on
   "today it is Artifact Registry" it fades and the panel's title flashes. The VM half stays empty.
1. LECTURE 20 · 13, 18. A GREEN card 'one program' with three stack cards under it ('dev',
   'staging', 'prod'), each with its own GREEN scroll 'state' and GREY 'config' chip. On "The
   tutorial has one stack" the program card splits into the two project cards
   'deploy_images/Pulumi.yaml' / 'deploy_single_vm/Pulumi.yaml' (each with its real line 1,
   'name: deploy-images' / 'name: deploy-single-vm'); staging and prod fade, dev moves under the
   first project and a copy under the second.
2. LECTURE (held). On "Its full name" the GREEN 'organization/deploy-images/dev' writes under the
   deploy-images stack; on "is used by the VM project" a GREY ghost of setup_containers.py · line 27
   appears at the bottom with a PINK dotted line from the name to its string and a GREY 'used by
   name'; on "so do not rename it" a RED-outlined chip "don't rename". On "Every stack" that group
   dims, a small BLUE bucket 'your state bucket' appears between the stacks and both state scrolls
   slide into it.
3. TRACKER [P] 9. A 10-row 'laptop · toolbox' terminal. b14's two commands typed (`cd deploy_images`
   at …:/app#, `pulumi stack init dev` at …:/app/deploy_images#) -> TERM(b14: 3 wrap, 5, 7 crop "or"),
   line 7 ORANGE. GREY chip 'no bucket login → Pulumi offers its own cloud' above the terminal; on
   "If yours says" a GREY chip `pulumi stack select dev` · 'second time'.
4. Same terminal. `pulumi config set gcp:project ac215-project` (default_tag above the terminal,
   'ac215-project' YELLOW) -> TERM(b15: 2 wrap) RED; (tracker stays 9) `pulumi preview --stack dev
   --refresh` -> TERM(b16: 2 wrap) RED; `pulumi up --stack dev --refresh -y` -> TERM(b17: 2 wrap) RED;
   on "Pulumi access token must be set" the three PULUMI_ACCESS_TOKEN words flash RED. TRACKER [P] 9 ·
   extra · not for you: `pulumi login --local` (tag 'extra · not for you' on the title bar) ->
   TERM(b30: 2 crop "as root"), the container id GREY.
5. TRACKER [P] 9 · extra. Fresh terminal page. `pulumi stack init dev` -> TERM(b31: 2) GREEN;
   `pulumi config set gcp:project ac215-project` -> (no output); b33:1 (folds) -> TERM(b33: 2-3,
   6-9): 'gcp:project  ac215-project' with a row-sized default tag, `dev*` and `0` YELLOW. Above the
   terminal a GREEN file card 'Pulumi.dev.yaml' glows with the GREY two-row note 'committed in the repo
   · config set rewrites it' / 'shows in git status: keep it on your branch'.
6. TRACKER [P] 10. The terminal leaves. CODE(deploy_images/__main__.py: 9–15) at the top: line 13
   YELLOW (on "Line 13"), the format string flashes on "down to the second", lines 14-15 PINK. V6
   TimestampPipe starts below the panel: the three Dockerfiles, then three TEAL crates on the conveyor.
7. V6 steps aside; CODE(…: 23–32) at the top: lines 23-25 YELLOW, the timestamp_tag of line 25 flashes
   on "a timestamped tag", line 29 GREEN on "push true", line 31 GOLD on "retain on delete", line 28
   PINK on "one platform". On "An Apple silicon Mac" a GREY chip with a chip icon 'Apple silicon →
   amd64 under emulation: slow' and a BLUE chip 'the VM is amd64' under the panel. On "Lines 34 and
   35" the panel scrolls to CODE(…: 33–35) at the bottom (lines 34-35 GREEN), V6 returns above it,
   each crate gets its YELLOW 'tag' badge and pulumi.export copies the stamp onto the GREEN ticket.
8. TRACKER [P] 10 · extra. V6 steps aside again; a 9-row terminal at 20 pt (72 characters a row). b34:1 typed (soft-wrapped; 'extra
   · recording only' on the title bar) -> TERM(b34: 3–7), which collapse into one PURPLE chip
   '5 providers' above the terminal; '…', 30 GREEN; 35 (wrap); '…', 41–43 wrap: the stamp YELLOW, the
   'ac215-project' part YELLOW with the GREY default_tag above the terminal; then line 35 turns YELLOW
   on "and a warning"; '…', 48 '+ 2 to create'. V4 small (EngineLoop compact, the desired column only,
   cards 'Stack' and 'Image', top right): the cards drop in on "one image to create", a YELLOW padlock
   'unknown' on the Image card on "and a warning", and a GREY chip 'no build in a preview' on "A
   preview never builds".
9. The terminal becomes a 4-row strip, V6 is back above it (the stamped crates on the conveyor, the
   ticket). b35b:1 typed ('extra · recording only' on the bar) -> TERM(b35b: 5 wrap, …, 141 wrap, …,
   170 wrap, 205 wrap, …, 223 wrap, …, 260 wrap, …, 293–295): 'DONE 71.1s', '✓ Compiled successfully',
   'DONE 54.2s', 'pushing layers' YELLOW; the frontend crate flashes while it builds; on "which fails
   here" line 260 prints RED and the frontend crate bounces off a RED padlock at the shelf; '2 errored'
   RED. On "Yours builds all three images" a GREY card 'with your key / + the repository / → the tag
   lands' and the three crates are shelved. On "Pause and run it" the strip leaves; a GREY-dashed ghost
   line `pulumi up --stack dev --refresh -y` (README:344) with a YELLOW '▶ your turn'; TRACKER [P] 10.
10. The ghost leaves; the YELLOW sticky 'hold that thought' returns bottom left. On "each up rebuilds
   the images" a second run: three NEW crates stamped with a later stamp, shelved in column 2; the
   ticket shows the new stamp. On "Each run can add image layers" the shelf flashes and the GOLD
   cost tag 'registry storage · grows with every changed layer' appears. Fade; empty frame.

Deviations from SHOW:
- Beat 0: the strip starts with chip 1 YELLOW and moves to chip 2 on "Step 2" (so the change is seen).
- Beat 1: the project cards carry their real first line ('name: deploy-images', Pulumi.yaml:1) as the
  project name.
- Beat 2: the ghost is the real line (setup_containers.py · line 27, dedented, GREY) at the bottom of
  the frame, not a free-floating label.
- Beat 3: the chip says 'no bucket login → …' without '(S11)' (scene numbers are not on screen).
- Beat 5: the file card 'Pulumi.dev.yaml' is GREEN (the colour table: Pulumi.dev.yaml is
  project-owned), its note GREY; SHOW said a GREY icon.
- Beats 6-7: CODE 9–15 shows line 12's clock emoji as a GREY '…' (the code font has no emoji glyph:
  the panel refuses it). A 10-line panel and V6 do not fit the frame together, so V6 steps aside while
  CODE 23–32 is on screen and comes back with CODE 33–35; the crates are stamped and the ticket is
  written on "Lines 34 and 35" (V6's crates are shelved in beat 9, on "Yours builds all three images",
  so that the frontend crate can bounce off the padlock first).
- Beat 8: V4 small is the desired column only (the compact loop's other trees would sit under the
  padlock), and 'no build in a preview' is our GREY chip rather than EngineLoop.preview_stop
  ('nothing applied'). The default tag sits above the terminal (line 42 wraps over two rows).
- Beats 8-9: the terminal is 20 pt (72 characters a row) so that b34's and b35b's 67-68 character
  rows stay whole; the strip has 4 rows (line 260 wraps over four).
- V6 is the scene-local `Pipe` (TimestampPipe with tighter 'tag' badges inside each crate's width, so
  they clear shelf column 2 and the shelf edge). Beat 9 brings the registry shelf in on "then the
  push", so the 403 padlock sits on the registry; beat 10 pulses the shelf's outline GOLD (no fill flash).
- Beat 10: V6 slides down a little (the strip is gone) to centre the picture. The chip of SHOW ('with your key + the repository from S11 → the tag lands') is a
  three-row GREY card without '(S11)'. The README's command reappears as a dashed ghost card under
  V6, not as a terminal row (it was not run here).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S13"]
assert len(SAY) == SAY_COUNT["S13"] == 11

# ------------------------------------------------------------------ the real sources (checked)
B14, B15, B16, B17 = (capture(k) for k in ("b14", "b15", "b16", "b17"))
B30, B31, B32, B33, B34, B35 = (capture(k) for k in ("b30", "b31", "b32", "b33", "b34", "b35b"))
TOKEN_ERR = "error: PULUMI_ACCESS_TOKEN must be set for login during non-interactive CLI sessions"
assert B14.cmd_lines == ["cd deploy_images", "pulumi stack init dev"]
assert readme(332) == "pulumi stack init dev" and "deploy_images" in readme(329)
assert B14.line(3).startswith("Connect to Pulumi Cloud for state storage")
assert B14.line(5) == "Run `pulumi login --help` for alternative login options."
assert B14.crop(7, "or") == "Press <ENTER> to log in with your browser, or"
assert B15.cmd == readme(333) == "pulumi config set gcp:project ac215-project" and B15.line(2) == TOKEN_ERR
assert B16.cmd == readme(339) == "pulumi preview --stack dev --refresh" and B16.line(2) == TOKEN_ERR
assert B17.cmd == readme(344) == "pulumi up --stack dev --refresh -y" and B17.line(2) == TOKEN_ERR
assert B30.cmd == "pulumi login --local"
assert B30.crop(2, "as root") == "Logged in to 3e978a898fa8 as root"
assert B31.cmd == "pulumi stack init dev" and B31.line(2) == "Created stack 'dev'"
assert B32.cmd == B15.cmd and not B32.lines
assert B33.cmd == "pulumi config; cat Pulumi.dev.yaml; pulumi stack ls"
assert B33.line(3) == "gcp:project  ac215-project" and B33.line(7) == "  gcp:project: ac215-project"
assert B33.line(9).split() == ["dev*", "now", "0"]
assert B34.cmd.startswith("pulumi preview --stack dev --refresh --target 'urn:pulumi:dev::deploy-images::")
assert all(B34.line(n).startswith("Downloading plugin ") for n in range(3, 8))
assert B34.line(30).strip() == "+  docker-build:index:Image build-cheese-app-frontend-react create"
assert B34.line(35).strip() == "warning: Skipping preview build because some inputs are unknown."
assert B34.line(42).endswith(f'/ac215-project/cheese-app-repository/cheese-app-frontend-react:{STAMP_1}"')
assert B34.line(48).strip() == "+ 2 to create"
assert B35.cmd.startswith("pulumi up --stack dev -y --target 'urn:pulumi:dev::deploy-images::")
assert B35.line(141).endswith("#13 DONE 71.1s") and B35.line(205).endswith("#17 DONE 54.2s")
assert B35.line(170).endswith("✓ Compiled successfully") and B35.line(223).endswith("#21 pushing layers")
assert B35.line(260).endswith(": 403 Forbidden")
assert [B35.line(n).strip() for n in (293, 294, 295)] == ["Resources:", "3 unchanged", "2 errored"]
assert STAMP_2 in B35.line(17)
MAIN = "src/deployment/deploy_images/__main__.py"
MAIN_SHOWN = "deploy_images/__main__.py"
assert excerpt(MAIN, 13, 13) == 'timestamp_tag = datetime.datetime.now().strftime("%Y%m%d%H%M%S")'
assert excerpt(MAIN, 28, 28).strip() == "platforms=[docker_build.Platform.LINUX_AMD64],"
assert excerpt(MAIN, 29, 29).strip() == "push=True,"
assert excerpt(MAIN, 31, 31).strip() == "retain_on_delete=True)"
assert excerpt(MAIN, 34, 34).startswith("pulumi.export(")
SC = "src/deployment/deploy_single_vm/setup_containers.py"
assert excerpt(SC, 27, 27).strip() == 'images_stack = pulumi.StackReference("organization/deploy-images/dev")'
NAME_IMG = excerpt("src/deployment/deploy_images/Pulumi.yaml", 1, 1)
NAME_VM = excerpt("src/deployment/deploy_single_vm/Pulumi.yaml", 1, 1)
assert NAME_IMG == "name: deploy-images" and NAME_VM == "name: deploy-single-vm"
FULL_NAME = "organization/deploy-images/dev"
CID = "3e978a898fa8"                    # the toolbox container id (b30:2): GREY, never read aloud

P_APP = toolbox_prompt("/app")
P_IMG = toolbox_prompt("/app/deploy_images")

V6_LOW = -2.57          # V6 under CODE 9–15 (beat 6)
V6_MID = 0.0            # V6 over CODE 33–35 (beat 7)
V6_HIGH = 0.25          # V6 over the 4-row 20 pt strip (beat 9)


# ------------------------------------------------------------------ small glyphs of this scene
def scroll_glyph(h: float = 0.36, color=OWN) -> VGroup:
    """A small scroll (a stack's state): a sheet between two rolls. Text-free."""
    body = Rectangle(width=h * 0.7, height=h * 0.78, stroke_color=color, stroke_width=2).set_fill(tint(color, 0.25), 1)
    r1 = RoundedRectangle(width=h * 0.92, height=h * 0.2, corner_radius=h * 0.1, stroke_color=color,
                          stroke_width=2).set_fill(tint(color, 0.4), 1).move_to(body.get_top())
    r2 = r1.copy().move_to(body.get_bottom())
    return VGroup(body, r1, r2)


def chip_icon(h: float = 0.3, color=S.GREY) -> VGroup:
    """A processor chip: a square with three pins a side. Text-free."""
    sq = Square(h, stroke_color=color, stroke_width=2.5).set_fill(tint(color, 0.3), 1)
    pins = VGroup()
    for i in (-1, 0, 1):
        o = i * h * 0.28
        pins.add(Line([o, h / 2, 0], [o, h / 2 + h * 0.18, 0]), Line([o, -h / 2, 0], [o, -h / 2 - h * 0.18, 0]),
                 Line([h / 2, o, 0], [h / 2 + h * 0.18, o, 0]), Line([-h / 2, o, 0], [-h / 2 - h * 0.18, o, 0]))
    pins.set_stroke(color, 2)
    return VGroup(pins, sq)


def stack_card(name: str) -> VGroup:
    """A stack: a GREEN card with its name, and under it its own scroll 'state' and GREY 'config'.
    .card .scroll .state .config"""
    b = RoundedRectangle(width=2.5, height=0.56, corner_radius=0.1, stroke_color=OWN,
                         stroke_width=3).set_fill(tint(OWN, 0.14), 1)
    t = label(name, 22, INK).move_to(b)
    cd = VGroup(b, t)
    sc = scroll_glyph(0.38, OWN)
    st = label("state", 20, OWN)
    s_row = VGroup(sc, st).arrange(RIGHT, buff=0.1)
    cf = grey_chip("config")
    under = VGroup(s_row, cf).arrange(RIGHT, buff=0.25).next_to(cd, DOWN, buff=0.2)
    g = VGroup(cd, s_row, cf)
    g.card, g.scroll, g.state, g.config, g.name_t = cd, sc, st, cf, t
    assert under.width < 2.9, under.width
    return g


def program_card() -> VGroup:
    gl = file_glyph(0.4, OWN)
    t = label("one program", 22, INK)
    row = VGroup(gl, t).arrange(RIGHT, buff=0.16)
    b = outline_box(row.width + 0.6, row.height + 0.4, OWN, solid=True, fill_opacity=0.12)
    row.move_to(b)
    return VGroup(b, row)


def project_card(path: str, name_line: str) -> VGroup:
    """A Pulumi project: GREEN outline, the file path (GREY mono) over its real first line (mono)."""
    hd = VGroup(file_glyph(0.32, OWN), mono(path, 20, S.GREY)).arrange(RIGHT, buff=0.14)
    nm = mono(name_line, 22, INK)
    inner = VGroup(hd, nm).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    b = outline_box(inner.width + 0.5, inner.height + 0.4, OWN, solid=True, fill_opacity=0.12)
    inner.move_to(b)
    g = VGroup(b, inner)
    g.name_t = nm
    return g


def move_v6(tp, dy: float) -> None:
    """Shift V6 by dy, its shelf too while the shelf is not yet part of the piece (built in __init__,
    added by shelf_on)."""
    tp.shift(UP * dy)
    if tp.shelf not in tp.submobjects:
        tp.shelf.shift(UP * dy)


class Pipe(TimestampPipe):
    """V6 with tighter 'tag' badges: TimestampPipe.stamp centres a 0.52-high chip on the crate's
    top-right corner, so it overhangs the next shelf column (gap 0.3) and the shelf's right edge.
    Here the badge (0.34 high, opaque backing) straddles the crate's top edge, right-aligned inside
    the crate: clear of the crate's label, of the row above and of column 2 / the shelf edge."""

    def stamp(self, scene, stamp: str = STAMP_1, run: int | None = None, run_time: float = 0.6):
        run = run or self.run_n
        self.stamp_text = stamp
        bs = []
        for c in self.crates[run]:
            ch = chip("tag", TURN, size=20, pad_x=0.12, pad_y=0.03)
            back = ch.box.copy().set_fill(S.BG, 1).set_stroke(width=0)
            b = VGroup(back, ch)
            b.move_to(c.get_top()).align_to(c, RIGHT).shift(LEFT * 0.1)
            b.set_z_index(2)
            b.crate = c
            bs.append(b)
            c.badge = b
        self.show(scene, *bs, anims=[LaggedStart(*[FadeIn(b, scale=1.6) for b in bs], lag_ratio=0.2)],
                  run_time=run_time, into=self.badges)
        return bs


def bars(panel, spec) -> VGroup:
    """Translucent bars over file lines: spec = [(k, colour), …] with k = file line - first."""
    return VGroup(*[line_bar(panel.code, k, c, 0.22) for k, c in spec])


class ImagesStack(VoiceScene):
    def construct(self):
        # ========================================================== 0. step 2: the registry (slide 21)
        ref0 = lref("19, 21")
        ss = six_steps(1).move_to([0, 0.6, 0])
        md = MasterDiagram()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref0, shift=LEFT * 0.2), FadeIn(ss, shift=UP * 0.2), run_time=0.7)
            self.play(ss.goto(2), run_time=0.6)
            self.play(ss.light(2), Indicate(ss.files[1], color=TURN, scale_factor=1.1), run_time=0.8)
            ss.heal(self)
            vo.wait_until("Your laptop's arrow")
            ss.shrink_away(self, run_time=0.4)
            md.laptop(self)
            md.gcp(self)
            md.registry(self)
            md.push(self)
            vo.wait_until("slide 21 still calls it GCR")
            gcr = md.gcr_note(self)
            self.play(Indicate(gcr, color=S.GREY, scale_factor=1.1), run_time=0.6)
            md.heal(self)
            vo.wait_until("today it is Artifact Registry")
            md.drop(self, gcr, run_time=0.4)
            del md.parts["gcr"]
            self.play(Indicate(md.parts["registry"].title, color=CLOUD, scale_factor=1.15), run_time=0.8)
            md.heal(self)

        # ========================================================== 1. stacks of one program (13, 18)
        ref1 = lref("13, 18")
        prog = program_card().move_to([0, 2.1, 0])
        stacks = [stack_card(n) for n in ("dev", "staging", "prod")]
        for s, x in zip(stacks, (-4.2, 0.0, 4.2)):
            s.move_to([x, 0.1, 0])
        links = VGroup(*[arrow(prog[0].get_bottom(), s.card.get_top(), OWN, stroke=3, buff=0.08)
                         for s in stacks])
        proj_l = project_card("deploy_images/Pulumi.yaml", NAME_IMG).move_to([-3.3, 2.0, 0])
        proj_r = project_card("deploy_single_vm/Pulumi.yaml", NAME_VM).move_to([3.3, 2.0, 0])
        assert proj_l.get_right()[0] < proj_r.get_left()[0] - 0.2 and proj_r.get_right()[0] < 6.5
        dev_l_target = stacks[0].copy().move_to([-3.3, 0.1, 0])
        dev_r = stacks[0].copy().move_to([3.3, 0.1, 0])
        link_l = arrow(proj_l[0].get_bottom(), dev_l_target.card.get_top(), OWN, stroke=3, buff=0.08)
        link_r = arrow(proj_r[0].get_bottom(), dev_r.card.get_top(), OWN, stroke=3, buff=0.08)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(md), FadeOut(ref0), run_time=0.5)
            self.remove(md, ref0)
            self.play(FadeIn(ref1, shift=LEFT * 0.2), FadeIn(prog, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("dev, staging and production")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(s.card, shift=DOWN * 0.15))
                                    for a, s in zip(links, stacks)], lag_ratio=0.35), run_time=1.2)
            vo.wait_until("each with its own state and config")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(s[1]), FadeIn(s.config, shift=UP * 0.1))
                                    for s in stacks], lag_ratio=0.25), run_time=1.0)
            for s in stacks:                          # re-seat each stack as one mobject
                self.remove(*s.submobjects)
                self.add(s)
            self.play(*[Indicate(s.scroll, color=OWN, scale_factor=1.3) for s in stacks], run_time=0.7)
            vo.wait_until("The tutorial has one stack")
            self.play(FadeOut(VGroup(stacks[1], stacks[2], links[1], links[2]), shift=DOWN * 0.2),
                      FadeOut(links[0]), run_time=0.5)
            self.remove(stacks[1], stacks[2], links)
            self.play(ReplacementTransform(prog, VGroup(proj_l, proj_r)),
                      stacks[0].animate.move_to(dev_l_target), run_time=0.9)
            self.play(TransformFromCopy(stacks[0], dev_r), GrowArrow(link_l), GrowArrow(link_r), run_time=0.8)
            vo.wait_until("per project")
            self.play(Indicate(proj_l.name_t, color=OWN, scale_factor=1.06),
                      Indicate(proj_r.name_t, color=OWN, scale_factor=1.06), run_time=0.7)
        dev_l = stacks[0]

        # ========================================================== 2. the full name; states in the bucket
        full = mono(FULL_NAME, 20, OWN).next_to(dev_l, DOWN, buff=0.35)
        ghost = code(SC, 27, dedent=True, font_size=20, shown="deploy_single_vm/setup_containers.py")
        ghost.move_to([0, -2.88, 0])
        ghost.set_opacity(0.55)
        g_str = code_span(ghost.code, 0, FULL_NAME)
        dot_line = DashedLine(full.get_corner(DR) + np.array([-0.3, -0.06, 0]),
                              g_str.get_corner(UL) + np.array([2.4, 0.08, 0]), color=ROUTE,
                              stroke_width=3, dash_length=0.08).set_z_index(2)   # over the re-seated ghost panel
        used = label("used by name", 20, S.GREY).next_to(dot_line.get_center(), UR, buff=0.08)
        assert used.get_left()[0] > ghost.header.get_right()[0] + 0.1 or used.get_bottom()[1] > ghost.get_top()[1] + 0.05
        nope = chip("don't rename", ERR, size=20, text_color=INK, fill_opacity=0.08).next_to(full, RIGHT, buff=0.3)
        assert nope.get_right()[0] < dev_r.get_left()[0] - 0.1, nope.get_right()
        assert ghost.get_top()[1] < used.get_bottom()[1] + 0.6 and ghost.get_bottom()[1] > -3.55, ghost.get_bottom()
        pail_ = bucket("your state bucket", 1.0, CLOUD, mono_font=False).move_to([0, 0.35, 0])
        assert pail_.get_left()[0] > dev_l.get_right()[0] + 0.1 and pail_.get_right()[0] < dev_r.get_left()[0] - 0.1
        with self.voiceover(SAY[2]) as vo:
            self.play(Write(full), run_time=0.9)
            self.play(Indicate(full, color=OWN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("is used by the VM project")
            self.play(FadeIn(ghost, shift=UP * 0.15), run_time=0.5)
            self.play(Create(dot_line), FadeIn(used, shift=RIGHT * 0.1), g_str.animate.set_opacity(1).set_color(ROUTE),
                      run_time=0.7)
            self.add(ghost)
            vo.wait_until("so do not rename it")
            self.play(FadeIn(nope, scale=1.2), run_time=0.4)
            self.play(Indicate(nope.text, color=ERR, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Every stack")
            dim = VGroup(full, ghost, dot_line, used, nope)
            self.play(dim.animate.set_opacity(0.25), FadeIn(pail_, shift=UP * 0.15), run_time=0.6)
            self.play(dev_l.scroll.animate.move_to(pail_.pail).scale(0.7),
                      dev_r.scroll.animate.move_to(pail_.pail).scale(0.7), run_time=1.0)
            self.play(Indicate(pail_.pail, color=CLOUD, scale_factor=1.15), run_time=0.6)

        # ========================================================== 3. stack init: Pulumi Cloud asks
        trk = tracker_p(9)
        t = toolbox_term(10)
        ch_cloud = grey_chip("no bucket login → Pulumi offers its own cloud").move_to([0, 2.3, 0])
        ch_cloud.align_to(t.box, LEFT).shift(RIGHT * 0.1)
        sel_t = VGroup(mono("pulumi stack select dev", 20, INK), label("· second time", 20, S.GREY)).arrange(RIGHT, buff=0.14)
        sel = VGroup(box(sel_t.width + 0.48, 0.48, S.GREY, fill_opacity=0.16, radius=0.18), sel_t)
        sel_t.move_to(sel[0])
        sel.move_to([0, 1.8, 0]).align_to(t.box, LEFT).shift(RIGHT * 0.1)
        assert sel.get_bottom()[1] > t.box.get_top()[1] + 0.05, sel.get_bottom()
        scene_1 = VGroup(proj_l, proj_r, dev_l, dev_r, link_l, link_r, pail_, full, ghost, dot_line, used, nope)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(scene_1), FadeOut(ref1), run_time=0.5)
            self.remove(scene_1, ref1, *scene_1)
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.3), run_time=0.6)
            type_capture(self, t, B14, type_time=0.5, prompts=[P_APP, P_IMG])
            vo.wait_until("Without a bucket login")
            out(self, t, [B14.line(3)], wrap=True, run_time=0.5)
            self.play(FadeIn(ch_cloud, shift=DOWN * 0.1), run_time=0.4)
            out(self, t, [B14.line(5), (B14.crop(7, "or"), SHARED)], run_time=0.5)
            vo.wait_until("waits for a browser")
            self.play(Indicate(t.find("Press <ENTER>"), color=SHARED, scale_factor=1.04), run_time=0.7)
            self.add(t)
            vo.wait_until("If yours says the stack already exists")
            self.play(FadeIn(sel, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(sel_t[0], color=TURN, scale_factor=1.08), run_time=0.7)

        # ========================================================== 4. no token: then the local folder
        dtag = default_tag().move_to([0, 2.15, 0]).align_to(t.box, RIGHT).shift(LEFT * 0.1)
        nfy = on_bar(t, extra_row("not for you")).set_z_index(3)     # above the bar when t is re-seated
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(ch_cloud), FadeOut(sel), run_time=0.4)
            self.remove(ch_cloud, sel)
            ln = type_cmd(self, t, B15.cmd, type_time=0.5)
            pr = substring(rows_of(ln)[-1], PROJECT_README)
            self.play(pr.animate.set_color(TURN), FadeIn(dtag, shift=DOWN * 0.1), run_time=0.4)
            self.add(t)
            e1 = out(self, t, [(B15.line(2), ERR)], wrap=True, run_time=0.3)
            # the tracker stays on 9 through beats 3-5 (moves to 10 only with the program, beat 6)
            type_cmd(self, t, B16.cmd, type_time=0.45)
            e2 = out(self, t, [(B16.line(2), ERR)], wrap=True, run_time=0.3)
            type_cmd(self, t, B17.cmd, type_time=0.45)
            e3 = out(self, t, [(B17.line(2), ERR)], wrap=True, run_time=0.3)
            vo.wait_until("Pulumi access token must be set")
            toks = [substring(e[0], "PULUMI_ACCESS_TOKEN") for e in (e1, e2, e3) if len(e) and e[0] in t.lines]
            assert toks, "the token errors scrolled away"
            self.play(*[Indicate(k, color=ERR, scale_factor=1.1) for k in toks], run_time=0.8)
            self.add(t)
            vo.wait_until("To show them anyway")
            self.play(FadeOut(dtag), track(trk, 9, "not for you"), run_time=0.5)
            self.remove(dtag)
            type_cmd(self, t, B30.cmd, type_time=0.5)
            self.play(FadeIn(nfy, shift=LEFT * 0.1), run_time=0.4)
            r30 = out(self, t, [B30.crop(2, "as root")], run_time=0.4)[0]
            self.play(substring(r30, CID).animate.set_color(S.GREY), run_time=0.3)
            self.add(t)
            vo.wait_until("extra, and not for you")
            flash_tag(self, nfy, INK)

        # ========================================================== 5. on the local backend: config written
        dev_file = file_card("Pulumi.dev.yaml", OWN)
        note2 = VGroup(note("committed in the repo · config set rewrites it"),
                       note("shows in git status: keep it on your branch")).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        fgrp = VGroup(dev_file, note2).arrange(RIGHT, buff=0.35).move_to([0, 2.1, 0])
        assert fgrp.get_bottom()[1] > t.box.get_top()[1] + 0.05 and fgrp.get_top()[1] < 2.8, fgrp.get_top()
        assert fgrp.get_left()[0] > -6.5 and fgrp.get_right()[0] < 6.5
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(nfy), track(trk, 9, True), run_time=0.4)
            self.remove(nfy)
            t.clear(self)
            type_cmd(self, t, B31.cmd, type_time=0.4)
            r31 = out(self, t, [(B31.line(2), OWN)], run_time=0.3)[0]
            self.play(Indicate(r31, color=OWN, scale_factor=1.05), run_time=0.5)
            self.add(t)
            vo.wait_until("and config set writes")
            type_cmd(self, t, B32.cmd, type_time=0.45)
            bare_prompt(self, t)
            type_capture(self, t, B33, type_time=0.5)
            rows = out(self, t, B33.at((2, 3), (6, 9)), run_time=0.6)
            assert rows[1].text == B33.line(3) and rows[3].text == B33.line(7) and rows[5].text == B33.line(9)
            pin(self, rows[1], beside(default_row(), rows[1]))
            self.play(substring(rows[1], PROJECT_README).animate.set_color(TURN),
                      substring(rows[3], PROJECT_README).animate.set_color(TURN),
                      substring(rows[5], "dev*").animate.set_color(TURN),
                      substring(rows[5], "0").animate.set_color(TURN), run_time=0.4)
            self.add(t)
            vo.wait_until("Pulumi dot dev dot yaml")
            self.play(FadeIn(dev_file, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(dev_file, color=OWN, scale_factor=1.08), Indicate(rows[3], color=TURN, scale_factor=1.04),
                      FadeIn(note2, shift=LEFT * 0.1), run_time=0.8)
            self.add(t)

        # ========================================================== 6. the program: a timestamp, an address
        p1 = code(MAIN, 9, 15, shown=MAIN_SHOWN, elide={12: "🕒"})
        p1.move_to([0, 0, 0]).align_to([0, 2.75, 0], UP)
        b13 = bars(p1, [(4, TURN)])
        b1415 = bars(p1, [(5, ROUTE), (6, ROUTE)])
        tp = Pipe()
        move_v6(tp, V6_LOW)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(t), FadeOut(fgrp), track(trk, 10), run_time=0.5)
            self.remove(t, fgrp)
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.6)
            tp.files(self, run_time=0.5)
            assert tp.files_head.get_top()[1] < p1.get_bottom()[1] - 0.05, tp.files_head.get_top()
            vo.wait_until("Line 13 makes a timestamp")
            self.play(FadeIn(b13), run_time=0.4)
            self.play(Indicate(code_span(p1.code, 4, "timestamp_tag"), color=TURN, scale_factor=1.1), run_time=0.6)
            self.add(p1, b13)
            vo.wait_until("down to the second")
            fmt = code_span(p1.code, 4, '"%Y%m%d%H%M%S"')
            self.play(Indicate(fmt, color=TURN, scale_factor=1.12), run_time=0.8)
            self.add(p1, b13)
            vo.wait_until("and lines 14 and 15")
            self.play(FadeIn(b1415), run_time=0.4)
            self.play(Indicate(code_span(p1.code, 6, "us-docker.pkg.dev"), color=ROUTE, scale_factor=1.08), run_time=0.6)
            self.add(p1, b13, b1415)
            tp.crates_up(self, run_time=0.9)

        # ========================================================== 7. one Image resource per image; export
        p2 = code(MAIN, 23, 32, shown=MAIN_SHOWN,
                  elide={25: '"/", image_config["image_name"], ":", '},
                  cuts={26: "BuildContextArgs(", 27: "dockerfile=", 30: "ResourceOptions("})
        p2.move_to([0, 0, 0]).align_to([0, 2.75, 0], UP)
        b2325 = bars(p2, [(0, TURN), (1, TURN), (2, TURN)])
        b29, b31_, b28 = bars(p2, [(6, OWN)]), bars(p2, [(8, COST)]), bars(p2, [(5, ROUTE)])
        apple_t = label("Apple silicon → amd64 under emulation: slow", 20, INK)
        apple_r = VGroup(chip_icon(0.28, S.GREY), apple_t).arrange(RIGHT, buff=0.2)
        apple = VGroup(box(apple_r.width + 0.5, 0.52, S.GREY, fill_opacity=0.16, radius=0.2), apple_r)
        apple_r.move_to(apple[0])
        vmchip = chip("the VM is amd64", CLOUD, size=20)
        achips = VGroup(apple, vmchip).arrange(RIGHT, buff=0.4).move_to([0, -2.45, 0])
        assert achips.get_top()[1] < p2.get_bottom()[1] - 0.1 and achips.width < 12.8, achips.get_top()
        p3 = code(MAIN, 33, 35, shown=MAIN_SHOWN)
        p3.move_to([0, 0, 0]).align_to([0, -3.5, 0], DOWN)
        b3435 = bars(p3, [(1, OWN), (2, OWN)])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(p1, b13, b1415)), FadeOut(tp), run_time=0.5)
            self.remove(p1, b13, b1415, tp)
            move_v6(tp, V6_MID - V6_LOW)              # moved while off screen
            self.play(FadeIn(p2, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(b2325), run_time=0.4)
            self.play(Indicate(code_span(p2.code, 0, "docker_build.Image"), color=TURN, scale_factor=1.08), run_time=0.6)
            self.add(p2, b2325)
            vo.wait_until("a timestamped tag")
            self.play(Indicate(code_span(p2.code, 2, "timestamp_tag"), color=TURN, scale_factor=1.15), run_time=0.6)
            self.add(p2, b2325)
            vo.wait_until("push true")
            self.play(FadeIn(b29), Indicate(code_span(p2.code, 6, "push=True"), color=OWN, scale_factor=1.12), run_time=0.6)
            self.add(p2, b2325, b29)
            vo.wait_until("retain on delete")
            self.play(FadeIn(b31_), Indicate(code_span(p2.code, 8, "retain_on_delete=True"), color=COST, scale_factor=1.1),
                      run_time=0.6)
            self.add(p2, b2325, b29, b31_)
            vo.wait_until("and one platform")
            self.play(FadeIn(b28), Indicate(code_span(p2.code, 5, "LINUX_AMD64"), color=ROUTE, scale_factor=1.12),
                      run_time=0.6)
            self.add(p2, b2325, b29, b31_, b28)
            vo.wait_until("An Apple silicon Mac")
            self.play(FadeIn(apple, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(vmchip, shift=UP * 0.15), run_time=0.4)
            vo.wait_until("Lines 34 and 35")
            self.play(FadeOut(VGroup(p2, b2325, b29, b31_, b28, achips), shift=UP * 0.3), run_time=0.5)
            self.remove(p2, b2325, b29, b31_, b28, achips)
            self.play(FadeIn(p3, shift=UP * 0.3), FadeIn(tp), run_time=0.6)
            self.play(FadeIn(b3435), run_time=0.3)
            self.add(p3, b3435)
            tp.stamp(self, STAMP_1, run_time=0.5)
            tp.ticket(self, run_time=0.7)
            self.play(Indicate(code_span(p3.code, 1, "pulumi.export"), color=OWN, scale_factor=1.1), run_time=0.5)
            self.add(p3, b3435)

        # ========================================================== 8. the extra preview: no build
        t2 = term(P_IMG, 9, T_TOOLBOX, size=20)      # 72 characters a row: b34/b35b's rows are 67-68 wide
        rec = on_bar(t2, extra_row("recording only")).set_z_index(3)
        el = EngineLoop(cards=("Stack", "Image"), compact=True)
        d_el = np.array([0.8 - el.xs["desired"] - el.p(0, 0)[0], 1.6, 0])
        el.shift(d_el)
        for m in [*el.heads.values(), *el.cards.values()]:     # built in __init__, added only when shown
            m.shift(d_el)
        nob = grey_chip("no build in a preview")
        dtag2 = default_tag()
        prov = tool_chip("5 providers", mono_font=False)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(p3, b3435)), FadeOut(tp), track(trk, 10, True), run_time=0.5)
            self.remove(p3, b3435, tp)
            self.play(FadeIn(t2, shift=UP * 0.3), run_time=0.5)
            type_capture(self, t2, B34, type_time=0.9)
            self.play(FadeIn(rec, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("five provider plugins")
            dl = out(self, t2, B34.at((3, 7)), run_time=0.5)
            prov.move_to([0, 2.25, 0]).align_to(t2.box, LEFT).shift(RIGHT * 0.1)
            for r in dl:
                t2.lines.remove(r)
            self.play(ReplacementTransform(VGroup(*dl), prov), run_time=0.8)
            self.remove(*dl)
            self.add(prov, t2)
            vo.wait_until("one image to create")
            r30 = out(self, t2, ["…", (B34.line(30), OWN)], wrap=True, run_time=0.4)[-1]
            el.run(self, run_time=0.8)
            dhead = el.heads["desired"]
            assert dhead.get_top()[1] < 2.8 and el.cards["desired"][1].get_bottom()[1] > t2.box.get_top()[1] + 0.1
            vo.wait_until("with its timestamped tag")
            r35 = out(self, t2, [B34.line(35)], wrap=True, run_time=0.3)
            r41 = out(self, t2, ["…"] + B34.at((41, 43)), wrap=True, run_time=0.5)
            stamp_rows = [r for r in r41 if STAMP_1 in r.text]
            proj_rows = [r for r in r41 if PROJECT_README in r.text]
            assert stamp_rows and proj_rows
            dtag2.next_to(prov, DOWN, buff=0.15).align_to(prov, LEFT)
            assert dtag2.get_bottom()[1] > t2.box.get_top()[1] + 0.05, dtag2.get_bottom()
            self.play(substring(stamp_rows[0], STAMP_1).animate.set_color(TURN),
                      substring(proj_rows[0], PROJECT_README).animate.set_color(TURN),
                      FadeIn(dtag2, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(substring(stamp_rows[0], STAMP_1), color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(t2)
            vo.wait_until("and a warning")
            self.play(*[r.animate.set_color(TURN) for r in r35], run_time=0.4)
            pk = el.unknown(self, 1, run_time=0.5)
            self.play(Indicate(VGroup(*r35), color=TURN, scale_factor=1.03), run_time=0.6)
            self.add(t2)
            vo.wait_until("A preview never builds")
            out(self, t2, ["…", B34.line(48)], run_time=0.4)
            nob.next_to(pk, DOWN, buff=0.15).align_to(pk, LEFT)
            if nob.get_bottom()[1] < t2.box.get_top()[1] + 0.05:
                nob.next_to(el.cards["desired"][0], RIGHT, buff=0.15)
                nob.shift(UP * (pk.get_top()[1] + 0.05 + nob.height / 2 - nob.get_center()[1]))
            self.play(FadeIn(nob, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(nob.text, color=INK, scale_factor=1.1), run_time=0.6)
            assert r30 is not None

        # ========================================================== 9. the extra up: build, push, 403
        lock_card = card(["with your key", "+ the repository", "→ the tag lands"], size=20)
        g_rows = readme_rows(344, 344)
        assert g_rows == [B17.cmd]
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(el, prov, dtag2, nob, rec)), run_time=0.5)
            self.remove(el, prov, dtag2, nob, rec)
            t2.clear(self, run_time=0.25)
            resize(self, t2, 4, run_time=0.6)
            move_v6(tp, V6_HIGH - V6_MID)
            self.play(FadeIn(tp), run_time=0.5)
            assert tp.get_bottom()[1] > t2.box.get_top()[1] + 0.05, (tp.get_bottom(), t2.box.get_top())
            type_capture(self, t2, B35, type_time=0.8)
            rec2 = on_bar(t2, extra_row("recording only")).set_z_index(3)
            self.play(FadeIn(rec2, shift=LEFT * 0.1), run_time=0.3)
            front = tp.crates[1][1]
            vo.wait_until("the npm install")
            out(self, t2, [B35.line(5), "…"], wrap=True, run_time=0.4)
            r141 = out(self, t2, [B35.line(141)], wrap=True, run_time=0.3)
            self.play(substring(r141[-1], "DONE 71.1s").animate.set_color(TURN),
                      Indicate(front, color=CONTAINER, scale_factor=1.08), run_time=0.5)
            tp.heal(self)
            self.add(t2)
            vo.wait_until("the Next.js build")
            r170 = out(self, t2, ["…", B35.line(170), B35.line(205)], wrap=True, run_time=0.5)
            done = [r for r in r170 if "Compiled successfully" in r.text or "DONE 54.2s" in r.text]
            self.play(*[substring(r, "Compiled successfully" if "Compiled" in r.text else "DONE 54.2s").animate.set_color(TURN)
                        for r in done], Indicate(front, color=CONTAINER, scale_factor=1.08), run_time=0.5)
            tp.heal(self)
            self.add(t2)
            vo.wait_until("then the push")
            tp.shelf_on(self, run_time=0.4)           # the registry the push goes to (the 403's padlock sits on it)
            r223 = out(self, t2, ["…", B35.line(223)], wrap=True, run_time=0.4)
            self.play(substring(r223[-1], "pushing layers").animate.set_color(TURN), run_time=0.3)
            self.add(t2)
            vo.wait_until("which fails here with 403 forbidden")
            out(self, t2, ["…", (B35.line(260), ERR)], wrap=True, run_time=0.5)
            tp.refused(self, 1, run_time=0.9, keep=True)
            vo.wait_until("Yours builds all three images")
            r29 = out(self, t2, ["…"] + B35.at((293, 295)), run_time=0.4)
            self.play(r29[-1].animate.set_color(ERR), run_time=0.3)
            self.add(t2)
            tp.drop(self, tp.refused_lock, run_time=0.3)
            lock_card.move_to(tp.p(4.95, -0.35))
            assert lock_card.get_left()[0] > tp.shelf.get_right()[0] + 0.05 and lock_card.get_right()[0] < 6.55, \
                (lock_card.get_left(), lock_card.get_right())
            assert lock_card.get_top()[1] < tp.ticket_m.get_bottom()[1] - 0.05
            self.play(FadeIn(lock_card, shift=LEFT * 0.1), run_time=0.5)
            tp.shelve(self, run_time=0.9)
            vo.wait_until("and ends with each tag in the outputs")
            self.play(Indicate(tp.ticket_m, color=OWN, scale_factor=1.06), run_time=0.6)
            tp.heal(self)
            vo.wait_until("Pause and run it")
            gl = mono(g_rows[0], 22, S.GREY)
            gbox = outline_box(gl.width + 0.6, gl.height + 0.4, S.GREY, solid=False)
            gl.move_to(gbox)
            yt = your_turn()
            gline = VGroup(gbox, gl)
            VGroup(gline, yt).arrange(RIGHT, buff=0.3).move_to([0, -2.3, 0])
            self.play(FadeOut(t2), FadeOut(rec2), track(trk, 10), run_time=0.5)
            self.remove(t2, rec2)
            self.play(FadeIn(gline, shift=UP * 0.15), run_time=0.4)
            self.play(FadeIn(yt, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt)

        # ========================================================== 10. every up: new stamps, more storage
        stk = sticky("hold that thought").move_to([-4.6, -2.65, 0])
        cost = cost_tag("registry storage · grows with every changed layer")
        cost.move_to([1.9, -2.65, 0])
        assert cost.get_left()[0] > stk.get_right()[0] + 0.2 and cost.get_right()[0] < 6.55, cost.get_right()
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(gline, yt)), FadeOut(lock_card), tp.animate.shift(DOWN * (V6_HIGH + 0.25)),
                      run_time=0.6)
            self.play(FadeIn(stk, shift=UP * 0.2), run_time=0.4)
            self.remove(gline, yt, lock_card)
            self.play(Indicate(stk, color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("each up rebuilds the images")
            tp.second_run(self, STAMP_2)
            vo.wait_until("because the timestamp is new every run")
            tp.ticket(self, run_time=0.7)
            self.play(Indicate(tp.ticket_m.stamp, color=TURN, scale_factor=1.12), run_time=0.6)
            tp.heal(self)
            vo.wait_until("Each run can add image layers")
            self.play(tp.shelf.frame.animate(rate_func=there_and_back).set_stroke(COST, 7),
                      FadeIn(cost, shift=UP * 0.15), run_time=0.8)
            tp.heal(self)
            vo.wait_until("and storage costs money")
            flash_tag(self, cost)

        self.play(FadeOut(VGroup(tp, stk, cost, trk)), run_time=0.8)
        self.remove(tp, stk, cost, trk)
        self.wait(0.3)
