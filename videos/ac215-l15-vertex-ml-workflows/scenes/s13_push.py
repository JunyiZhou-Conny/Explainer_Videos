"""S13 · Build and push: your own registry (README B › Build & Push steps 1-11, slide 34 redrawn,
the registry route).

Beats (script.md "## S13", one voiceover block each):
 0  TRACKER B5 (appears, 11 dots, none lit). README card (README.md · line 153, chip B): "This step
    has already been done for this tutorial.", tag `erratum`. CODE(src/workflow/cli.py: 34-36)
    (the f-strings' middle elided to fit at 20 pt): `{ACCOUNT_ID}` YELLOW + chip "your account".
    Two TEAL image blocks (collector, processor) march into a BLUE "your ECR" shelf. Mini-legend
    chip "Artifact Registry → ECR" lower right.
 1  LECTURE 15 · 34. Slide 34's three steps as three numbered GREY cards: 1 callable (✓ done),
    2 build and push YELLOW, 3 describe the DAG (later). The tag and the legend chip leave with them.
 2  TRACKER B5 1-3. Registry route (top band): TEAL cube on the GREY laptop, GREY-dashed "Docker Hub"
    shelf, BLUE "your ECR" shelf. 3-row strip at ~/ml-workflow-aws/src/model-training: `cd
    ../data-collector` (chip "exit the container first · these run on your laptop") -> prompt. The
    four README commands typed verbatim (soft wrap): login (`-p <ACCESS TOKEN>` ringed ORANGE +
    chip "lands in your shell history · prefer --password-stdin"), build (the Docker Hub name
    under the cube), the M1/2 build (bar tag "M1/2 Macs"; `amd64/v2` YELLOW + chip "SageMaker runs
    amd64"), push (a copy of the cube rises to Docker Hub); chip "needs your Docker Hub account · no
    output shown"; GREY extra chip "amd64 image already local? … docker tag … skips Docker Hub".
 3  TRACKER B5 4. The strip grows to 7 rows: laptop/80's six command lines typed (soft wrap) ->
    TERM(laptop/80: 7-8 RED (row tag "region still set" GREEN), 10 wrap RED, 11 wrap with the
    leading '.' ringed RED). ▶ your turn on the title bar.
 4  The strip shrinks to 3 rows (line 11 kept). README card (line 169) shown alone: the bracket
    note GREY-struck, `us-east-1` GREEN; tag `erratum`. RED chip "URI starts with '.' → account
    lookup failed → fix your keys".
 5  TRACKER B5 5: the Docker Hub copy comes back down; 5-row strip types `docker pull …` (no-output
    chip). TRACKER B5 6 · extra: laptop/81 line 1 (bar tag extra; chip "our capture re-sets the two
    variables"), then B5 6: `aws ecr create-repository … || true` -> TERM(laptop/81: 4 wrap) RED;
    `|| true` ORANGE; chip "[exit 0] · || true hides it".
 6  TRACKER B5 7-11 ticking as each line is typed (3-row strip): ECR login (two rows, ' \\'
    continuation), `docker tag` (the ECR name label clips onto the same cube), `docker push` (a copy
    of the cube rides the PINK arrow into "your ECR"), `list-images`, `echo`; no-output chip; chip
    "on your laptop · the workflow container (next) has no docker". The route leaves; README card
    (lines 201-203) "Repeat for both images"; the strip types `cd ../data-processor` and `export
    REPO=cheese-app-data-processor`, chip "then steps 2–11 again"; GOLD cost tag "ECR storage · two
    images". Fade to empty.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.devops import code_panel
from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S13"]
SIZE = 20                                     # terminal font: 72 characters a row

# ------------------------------------------------------------------ the real sources (checked)
C80, C81 = capture("80"), capture("81")
assert C80.cmd_lines[0] == "export REGION=us-east-1 [YOUR DEVELOPMENT REGION]" and len(C80.cmd_lines) == 6
assert C80.cmd_lines[5] == 'echo "ECR URI: $ECR_URI"'
OUT80_ERR = C80.at(7, 8)
assert all(s.endswith("not a valid identifier") for s in OUT80_ERR), OUT80_ERR
ERR80 = C80.line(10)
assert "(InvalidClientTokenId)" in ERR80
URI80 = C80.line(11)
assert URI80 == "ECR URI: .dkr.ecr.us-east-1.amazonaws.com/cheese-app-data-collector:latest"
assert C81.cmd_lines == ["export REGION=us-east-1 REPO=cheese-app-data-collector",
                         'aws ecr create-repository --repository-name "$REPO" --region "$REGION" || true']
ERR81 = C81.line(4)
assert "(UnrecognizedClientException)" in ERR81 and C81.exit == 0

# README B, verbatim (B:153, 158-162, 169-173, 179-198, 201-203)
assert readme(153, "B").startswith("This step has already been done for this tutorial.")
HUB = ["docker login -u <USER NAME> -p <ACCESS TOKEN>",
       "docker build -t <USER NAME>/<IMAGE_NAME> -f Dockerfile .",
       "docker build -t <USER NAME>/<IMAGE_NAME> --platform=linux/amd64/v2 -f Dockerfile .",
       "docker push <USER NAME>/<IMAGE_NAME>"]
_hub_src = "\n".join(readme(n, "B") for n in range(155, 163))
assert all(f"`{c}`" in _hub_src for c in HUB), _hub_src
assert readme(169, "B") == C80.cmd_lines[0]
assert [readme(n, "B") for n in range(170, 174)] == C80.cmd_lines[1:5]
assert readme(198, "B") == C80.cmd_lines[5]
ECR = readme_rows(176, 198, "B")
PULL = "docker pull <YOUR_DOCKER_HUB_USERNAME>/$REPO:$TAG"
CREATE = C81.cmd_lines[1]
LOGIN = ['aws ecr get-login-password --region "$REGION" \\',
         '| docker login --username AWS --password-stdin "$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com"']
TAG_C = 'docker tag <YOUR_DOCKER_HUB_USERNAME>/$REPO:$TAG "$ECR_URI"'
PUSH_C = 'docker push "$ECR_URI"'
LIST_C = 'aws ecr list-images --repository-name "$REPO" --region "$REGION" --output table'
ECHO_C = 'echo "ECR URI: $ECR_URI"'
for c in [PULL, CREATE, *LOGIN, TAG_C, PUSH_C, LIST_C, ECHO_C]:
    assert c in ECR, c
assert readme(171, "B") == "export REPO=cheese-app-data-collector  # or cheese-app-data-processor"
REPO_B = "export REPO=cheese-app-data-processor"
assert readme(201, "B") == "**Repeat for both images:**"
assert readme(202, "B") == "- `cheese-app-data-collector`" and readme(203, "B") == "- `cheese-app-data-processor`"

CLI = "B/src/workflow/cli.py"
CLI_34_36 = excerpt(CLI, 34, 36).split("\n")
assert CLI_34_36[0] == "# ECR Docker images"
assert CLI_34_36[1] == ('DATA_COLLECTOR_IMAGE = f"{ACCOUNT_ID}.dkr.ecr.{AWS_REGION}.amazonaws.com/'
                        'cheese-app-data-collector:latest"')
assert CLI_34_36[2] == CLI_34_36[1].replace("COLLECTOR", "PROCESSOR").replace("collector", "processor")


def elide(s: str) -> str:
    """cli.py:35-36 at 20 pt: the variable name and '.amazonaws.com' elided (GREY '…'), as the
    script writes it: `{ACCOUNT_ID}.dkr.ecr.{AWS_REGION}…/cheese-app-data-collector:latest`."""
    name, rest = s.split(" = ", 1)
    return "… = " + rest.replace(".amazonaws.com", "…")


def cli_panel() -> VGroup:
    lines = [CLI_34_36[0], elide(CLI_34_36[1]), elide(CLI_34_36[2])]
    p = code_panel("\n".join(lines), shown_path(CLI), 34, "python", font_size=20)
    for k in (1, 2):
        for occ in (0, 1):
            code_span(p.code, k, "…", occ).set_color(S.GREY)
    return p


def fixed_tracker(key: str, step=None, extra=False) -> VGroup:
    """common.tracker() with its head put back above the dots (the head's arrange() centres it at
    y 0; the workaround of S01, S03-S11; requested fix in the report)."""
    tr = tracker(key, step, extra)
    tr.head.next_to(tr.dots, UP, buff=0.14, aligned_edge=LEFT)
    place_tracker(tr)
    assert tr.get_bottom()[1] >= TRACK_BOTTOM - 0.05, tr.get_bottom()
    return tr


def two_line_chip(top: VGroup, bottom: VGroup, color=S.GREY) -> VGroup:
    """A chip of two rows (label / mono). .box .text"""
    t = VGroup(top, bottom).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    b = box(t.width + 0.48, t.height + 0.3, color, fill_opacity=0.16, radius=0.16)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def step_card(n: int, text: str, color=S.GREY, note_: str | None = None, mark=None) -> VGroup:
    """One of slide 34's three numbered steps (redrawn): a GREY card, its number, its words, an
    optional GREY note on the right ('done' with a GREEN tick, 'later'). .frame .num .text .note"""
    num = label(str(n), 26, color if color != S.GREY else INK)
    tx = label(text, 22, INK)
    row = VGroup(num, tx).arrange(RIGHT, buff=0.35)
    extra = VGroup()
    if mark is not None:
        extra.add(mark)
    if note_:
        extra.add(label(note_, 20, S.GREY))
    if len(extra):
        extra.arrange(RIGHT, buff=0.15)
    w = 11.2
    fr = outline_box(w, 0.85, color, solid=True, fill_opacity=0.12 if color != S.GREY else 0.06)
    row.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.35)
    g = VGroup(fr, row)
    if len(extra):
        extra.move_to(fr).align_to(fr, RIGHT).shift(LEFT * 0.35)
        g.add(extra)
    g.frame, g.num, g.text, g.note = fr, num, tx, extra
    return g


def shelf(name: str, color, dashed: bool, w: float = 2.7, h: float = 1.25, plank_: bool = True) -> VGroup:
    """A registry shelf: an outline box with its name at the top (Docker Hub GREY dashed, your ECR
    BLUE solid) and a plank the cube lands on. .frame .name .plank .spot"""
    fr = outline_box(w, h, color, solid=not dashed, fill_opacity=0.08)
    if plank_:                       # the route's shelves: the name at the bottom, the cube above it
        nm = label(name, 22, INK if not dashed else S.GREY).move_to(fr.get_bottom() + UP * 0.24)
    else:                            # beat 0's shelf: the name at the top, the image blocks under it
        nm = label(name, 22, INK).move_to(fr.get_top() + DOWN * 0.27)
    py = fr.get_bottom()[1] + 0.48
    plank = Line([fr.get_left()[0] + 0.35, py, 0], [fr.get_right()[0] - 0.35, py, 0], color=color, stroke_width=4)
    g = VGroup(fr, nm, plank) if plank_ else VGroup(fr, nm)
    g.frame, g.name, g.plank = fr, nm, plank
    g.spot = lambda: plank.get_center() + UP * 0.335
    return g


def name_tag(rows, color=IMAGE) -> VGroup:
    """An image name label (mono, 20 pt, one or two rows) in a TEAL-edged tag. .box .text"""
    t = VGroup(*[mono(s, 20, INK) for s in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    b = box(t.width + 0.36, t.height + 0.22, color, fill=S.BG, fill_opacity=0.9, radius=0.1)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


class PushToECR(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S13"] == 7, len(SAY)
        self.bar_tags = []
        self.t = None

        # ========================================================== 0. "already done" · your account
        tr = fixed_tracker("B5")
        rc = readme_card(153, "This step has already been done for this tutorial.", repo="B")
        rc.move_to([-6.45 + rc.width / 2, 2.75 - rc.height / 2, 0])
        er0 = erratum_tag().next_to(rc, RIGHT, buff=0.3)
        cp = cli_panel()
        cp.move_to([-6.45 + cp.width / 2, rc.get_bottom()[1] - 0.25 - cp.height / 2, 0])
        assert cp.get_right()[0] < 6.5 and rc.get_top()[1] < 2.85, (cp.get_right(), rc.get_top())
        assert rc.get_left()[0] > tr.get_left()[0] - 0.1 and rc.get_top()[1] < tr.get_bottom()[1], rc.get_top()
        acc_span = code_span(cp.code, 1, "{ACCOUNT_ID}")
        acc_chip = chip("your account", TURN, size=20).next_to(cp, DOWN, buff=0.15)
        acc_chip.set_x(acc_span.get_center()[0])
        legend = bridge_chip(5)
        legend.move_to([6.45 - legend.width / 2, -3.45 + legend.height / 2, 0])
        ecr0 = shelf("your ECR", CLOUD, dashed=False, w=4.6, h=1.75, plank_=False)
        ecr0.move_to([0.4, acc_chip.get_bottom()[1] - 0.12 - ecr0.height / 2, 0])
        assert ecr0.get_right()[0] < legend.get_left()[0] - 0.1 and ecr0.get_bottom()[1] > -3.55, \
            (ecr0.get_right(), legend.get_left(), ecr0.get_bottom())
        imgs = VGroup(image_block("cheese-app-data-collector", box_w=4.0, box_h=0.5),
                      image_block("cheese-app-data-processor", box_w=4.0, box_h=0.5))
        imgs.arrange(DOWN, buff=0.12).move_to([-4.45, ecr0.get_center()[1] - 0.15, 0])
        assert imgs.get_right()[0] < ecr0.get_left()[0] - 0.2, (imgs.get_right(), ecr0.get_left())
        assert imgs.get_left()[0] > -6.55 and imgs.get_bottom()[1] > -3.55, imgs.get_bottom()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("The README says")
            self.play(FadeIn(rc, shift=DOWN * 0.2), run_time=0.6)
            self.play(Indicate(rc.body, color=TURN, scale_factor=1.03), run_time=0.7)
            vo.wait_until("A small gap")
            self.play(FadeIn(er0, shift=LEFT * 0.1), run_time=0.4)
            self.play(FadeIn(cp, shift=DOWN * 0.2), run_time=0.6)
            self.play(FadeIn(legend, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("the workflow code pulls both images")
            self.play(FadeIn(ecr0, shift=LEFT * 0.2), FadeIn(imgs, shift=RIGHT * 0.2), run_time=0.6)
            self.play(Indicate(ecr0.name, color=CLOUD, scale_factor=1.1), run_time=0.6)
            vo.wait_until("of your own account")
            self.play(*[code_span(cp.code, k, "{ACCOUNT_ID}").animate.set_color(TURN) for k in (1, 2)],
                      FadeIn(acc_chip, shift=UP * 0.1), run_time=0.6)
            self.add(cp)
            vo.wait_until("so you push them yourself")
            dest = imgs.copy().move_to(ecr0.frame.get_center() + DOWN * 0.25)
            assert dest.get_bottom()[1] > ecr0.get_bottom()[1] + 0.05 and dest.get_top()[1] < ecr0.name.get_bottom()[1] - 0.05
            self.play(LaggedStart(*[b.animate.move_to(d) for b, d in zip(imgs, dest)], lag_ratio=0.35),
                      run_time=1.4)
            self.play(Indicate(imgs, color=IMAGE, scale_factor=1.04), run_time=0.6)

        # ========================================================== 1. slide 34: three steps
        lt = lref("34")
        cards = VGroup(
            step_card(1, "make the container callable", note_="done", mark=check_glyph(0.28)),
            step_card(2, "build and push to a registry the platform can pull", color=TURN),
            step_card(3, "describe the DAG", note_="later"),
        ).arrange(DOWN, buff=0.3).move_to([0, 0.75, 0])
        assert cards.get_top()[1] < PIC_TOP and cards.get_bottom()[1] > legend.get_top()[1] + 0.2, cards.get_bottom()

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(rc, er0, cp, acc_chip, ecr0, imgs)), run_time=0.5)
            self.play(FadeIn(lt), LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in cards], lag_ratio=0.25),
                      run_time=1.0)
            vo.wait_until("push the images to a registry")
            self.play(Indicate(cards[1].text, color=TURN, scale_factor=1.05), run_time=0.8)
            self.play(Indicate(legend, color=INK, scale_factor=1.06), run_time=0.7)

        # ========================================================== 2. steps 1-3: Docker Hub
        lap = laptop_glyph(1.8).move_to([-5.15, 1.95, 0])
        cb = cube(0.45, depth=0.2).move_to(lap.screen)
        hub = shelf("Docker Hub", S.GREY, dashed=True, h=1.2).move_to([-0.35, 2.18, 0])
        ecr = shelf("your ECR", CLOUD, dashed=False, h=1.2).move_to([4.95, 1.85, 0])
        hub_name = name_tag(["<USER NAME>/<IMAGE_NAME>"])
        hub_name.move_to([-3.9 + hub_name.width / 2, 1.12 - hub_name.height / 2, 0])
        assert hub_name.get_top()[1] < hub.get_bottom()[1] - 0.05 and hub_name.get_left()[0] > lap.get_right()[0], \
            (hub_name.get_top(), hub.get_bottom(), lap.get_right())
        up_r = route(lap.screen.get_right() + RIGHT * 0.1 + UP * 0.1, hub.frame.get_left() + LEFT * 0.08 + UP * 0.15,
                     arc=-0.5)
        assert hub.get_top()[1] < PIC_TOP and ecr.get_right()[0] < 6.5, (hub.get_top(), ecr.get_right())
        assert hub.get_left()[0] > lap.get_right()[0] + 0.4, (hub.get_left(), lap.get_right())
        t = term(P_SRC("model-training"), rows=4, size=SIZE)
        self.t = t
        assert hub_name.get_bottom()[1] > 0.45, hub_name.get_bottom()
        exit_c = grey_chip("exit the container first · these run on your laptop")
        under_term(t, exit_c)
        tok_c = chip("lands in your shell history · prefer --password-stdin", SHARED, size=20)
        under_term(t, tok_c)
        amd_c = grey_chip("SageMaker runs amd64")
        under_term(t, amd_c)
        np_hub = no_panel_chip("needs your Docker Hub account · no output shown")
        under_term(t, np_hub)
        skip_c = two_line_chip(label("extra · your amd64 image is already local? This line skips Docker Hub:", 20, INK),
                               mono('docker tag cheese-app-data-collector "$ECR_URI"', 20, INK))
        skip_c.next_to(np_hub, UP, buff=0.12).align_to(np_hub, RIGHT)
        assert skip_c.get_top()[1] < hub_name.get_bottom()[1] - 0.05 or skip_c.get_left()[0] > hub_name.get_right()[0], \
            (skip_c.get_top(), skip_c.get_left())
        assert skip_c.get_width() < 12.9

        # The narration names all three steps in its first 4 s: typing runs back to back, and each
        # note stays up until the next one takes its place (no note flashes for under a second).
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(cards), FadeOut(lt), FadeOut(legend), run_time=0.4)
            self.play(FadeIn(lap), FadeIn(cb, scale=0.8), FadeIn(hub), FadeIn(ecr), FadeIn(t),
                      FadeIn(exit_c, shift=DOWN * 0.1), run_time=0.6)
            type_cmd(self, t, "cd ../data-collector", type_time=0.4)
            cd_prompt(self, t, P_SRC("data-collector"), run_time=0.4)
            self.play(track(tr, 1), run_time=0.3)
            ln = type_cmd(self, t, HUB[0], type_time=0.55)
            tok = self.find(ln, "-p <ACCESS TOKEN>")
            rg = ring(tok, SHARED)
            self.play(Create(rg), FadeOut(exit_c), FadeIn(tok_c, shift=DOWN * 0.1), track(tr, 2), run_time=0.45)
            attach(self, [r for r in rows_of(ln) if "-p <ACCESS TOKEN>" in r.text][0], rg)   # scrolls with its row
            self.reseat()
            type_cmd(self, t, HUB[1], type_time=0.5)
            self.play(FadeIn(hub_name, shift=UP * 0.1), Indicate(cb, color=IMAGE, scale_factor=1.2), run_time=0.5)
            vo.wait_until("The Mac line builds")
            ln = type_cmd(self, t, HUB[2], type_time=0.6)
            mac = on_bar(t, row_tag("M1/2 Macs"))
            self.play(self.find(ln, "amd64/v2").animate.set_color(TURN), FadeOut(tok_c),
                      FadeIn(amd_c, shift=DOWN * 0.1), FadeIn(mac), run_time=0.45)
            self.bar_tags.append(mac)
            self.reseat()
            vo.wait_until("because SageMaker runs that")
            self.play(Indicate(amd_c.text, color=TURN, scale_factor=1.06), FadeIn(skip_c, shift=DOWN * 0.1),
                      run_time=0.6)
            self.play(track(tr, 3), run_time=0.3)
            type_cmd(self, t, HUB[3], type_time=0.45)
            hub_cb = cb.copy()
            self.add(hub_cb)
            self.play(Create(up_r), FadeOut(amd_c), FadeIn(np_hub, shift=DOWN * 0.1), run_time=0.4)
            self.play(hub_cb.animate.move_to(hub.spot()), run_time=0.8)

        # ========================================================== 3. step 4: five variables
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(np_hub), FadeOut(skip_c), FadeOut(up_r), *self.unbar_anims(), track(tr, 4), run_time=0.4)
            self.resize(7, keep=0)
            assert t.box.get_top()[1] < hub_name.get_bottom()[1] - 0.2, t.box.get_top()
            for row in C80.cmd_lines:
                type_cmd(self, t, row, type_time=0.45)
            self.bar(on_bar(t, turn_row()))
            vo.wait_until("Pasted exactly as written")
            r78 = out(self, t, [(s, ERR) for s in OUT80_ERR], run_time=0.4)
            vo.wait_until("because export rejects the bracket note")
            self.play(each([substring(r78[0], "`[YOUR'"), substring(r78[1], "`REGION]'")], ERR, 1.15),
                      run_time=0.8)
            self.reseat()
            vo.wait_until("though the region is still set")
            rs = beside(row_tag("region still set", OWN), r78[1], buff=0.3)
            pin(self, r78[1], rs)
            vo.wait_until("The account lookup fails")
            r10 = out(self, t, [(ERR80, ERR)], wrap=True, run_time=0.5)
            hit = [r for r in r10 if "(InvalidClientTokenId)" in r.text][0]
            self.play(Indicate(substring(hit, "(InvalidClientTokenId)"), color=ERR, scale_factor=1.1), run_time=0.7)
            self.reseat()
            vo.wait_until("and the URI starts with a dot")
            r11 = out(self, t, [URI80], wrap=True, run_time=0.4)
            dot_row = [r for r in r11 if r.text.startswith(".dkr")][0]
            dot = glyph_range(dot_row, 0, 1)
            dr = ring(dot, ERR, buff=0.1)
            self.play(Create(dr), dot.animate.set_color(ERR), run_time=0.5)
            self.reseat()
            attach(self, dot_row, dr)
            self.play(Indicate(dr, color=ERR, scale_factor=1.3), run_time=0.6)
            self.reseat()

        # ========================================================== 4. erratum: paste only the value
        body = mono_line(C80.cmd_lines[0], 20, INK)
        rc169 = readme_card(169, body, repo="B")
        rc169.move_to([6.45 - rc169.width / 2, hub_name.get_bottom()[1] - 0.08 - rc169.height / 2, 0])
        br = substring(body, "[YOUR DEVELOPMENT REGION]")
        st = strike(br, S.GREY)
        er4 = erratum_tag().next_to(rc169, LEFT, buff=0.3)
        assert er4.get_left()[0] > -6.5, er4.get_left()
        dot_c = err_chip("URI starts with '.' → account lookup failed → fix your keys", mono_font=False)

        with self.voiceover(SAY[4]) as vo:
            self.play(*self.unbar_anims(), run_time=0.3)
            self.resize(3, keep=2)
            under_term(t, dot_c)
            assert rc169.get_bottom()[1] > dot_c.get_top()[1] + 0.05, (rc169.get_bottom(), dot_c.get_top())
            self.play(FadeIn(rc169, shift=DOWN * 0.2), FadeIn(er4, shift=LEFT * 0.1), run_time=0.6)
            self.play(Create(st), br.animate.set_color(S.GREY), run_time=0.5)
            self.play(substring(body, "us-east-1").animate.set_color(OWN), run_time=0.4)
            self.add(rc169, st)
            self.play(Indicate(substring(body, "us-east-1"), color=OWN, scale_factor=1.15), run_time=0.7)
            self.add(rc169, st)
            vo.wait_until("And if your URI starts with a dot")
            self.play(FadeIn(dot_c, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(dr, color=ERR, scale_factor=1.3), run_time=0.7)
            self.reseat()
            vo.wait_until("fix your keys first")
            self.play(Indicate(dot_c.text, color=ERR, scale_factor=1.05), run_time=0.7)

        # ========================================================== 5. steps 5-6: pull, create repo
        dn_r = route(hub.frame.get_left() + LEFT * 0.08 + DOWN * 0.3, lap.screen.get_right() + RIGHT * 0.1 + DOWN * 0.15,
                     arc=-0.6)
        np5 = no_panel_chip()
        cap_c = grey_chip("our capture re-sets the two variables")
        ex_c = VGroup(mono("[exit 0]", 20, INK), label("·", 20, S.GREY), mono("|| true", 20, SHARED),
                      label("hides it", 20, SHARED)).arrange(RIGHT, buff=0.14)
        ex_b = box(ex_c.width + 0.48, ex_c.height + 0.26, S.GREY, fill_opacity=0.16, radius=0.2)
        ex_c.move_to(ex_b)
        exit_chip = VGroup(ex_b, ex_c)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(rc169, st, er4, dot_c)), track(tr, 5), run_time=0.4)
            # the copy comes back down while the strip grows (the pull is named in the first 2 s)
            self.resize(5, keep=0, more=[Succession(Create(dn_r, run_time=0.3),
                                                    hub_cb.animate(run_time=0.5).move_to(cb))])
            self.remove(hub_cb)
            for c in (np5, cap_c, exit_chip):
                under_term(t, c)
            type_cmd(self, t, PULL, type_time=0.5)
            self.play(Indicate(cb, color=IMAGE, scale_factor=1.2), FadeOut(dn_r), FadeIn(np5, shift=DOWN * 0.1),
                      run_time=0.4)
            vo.wait_until("Step 6 creates the repository")
            self.play(FadeOut(np5), track(tr, 6, True), run_time=0.3)
            type_cmd(self, t, C81.cmd_lines[0], type_time=0.45)
            ex_tag = on_bar(t, extra_row())
            self.play(FadeIn(ex_tag), FadeIn(cap_c, shift=DOWN * 0.1), run_time=0.35)
            self.bar_tags.append(ex_tag)
            self.play(track(tr, 6), *self.unbar_anims(), run_time=0.3)
            cl = type_cmd(self, t, CREATE, type_time=0.6)
            r4 = out(self, t, [(ERR81, ERR)], wrap=True, run_time=0.45)
            vo.wait_until("and the or true at the end hides the error")
            self.play(self.find(cl, "|| true").animate.set_color(SHARED), run_time=0.4)
            self.reseat()
            hit = [r for r in r4 if "(UnrecognizedClientException)" in r.text][0]
            self.play(Indicate(substring(hit, "(UnrecognizedClientException)"), color=ERR, scale_factor=1.08),
                      run_time=0.6)
            self.reseat()
            vo.wait_until("the command exits with zero")
            self.play(FadeOut(cap_c), FadeIn(exit_chip, shift=DOWN * 0.1), run_time=0.45)
            self.play(Indicate(ex_c[0], color=INK, scale_factor=1.15), run_time=0.6)

        # ========================================================== 6. steps 7-11: tag, push, repeat
        ecr_name = name_tag(["<account>.dkr.ecr.us-east-1…", "/cheese-app-…:latest"])
        ecr_name.next_to(hub_name, DOWN, buff=0.1).align_to(hub_name, LEFT)
        ecr_r = route(np.array([lap.get_right()[0] + 0.1, 1.38, 0]), np.array([ecr.frame.get_left()[0] - 0.08, 1.38, 0]))
        np6 = no_panel_chip()
        lap_c = grey_chip("on your laptop · the workflow container (next) has no docker")
        rc201 = readme_card((201, 203), VGroup(
            label("Repeat for both images:", 22, INK),
            mono("- cheese-app-data-collector", 22, INK),
            mono("- cheese-app-data-processor", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.12), repo="B")
        rc201.move_to([-6.45 + rc201.width / 2, 2.75 - rc201.height / 2, 0])
        again = grey_chip("then steps 2–11 again")
        cost = cost_tag("ECR storage · two images · check the pricing page")

        with self.voiceover(SAY[6]) as vo:
            self.resize(4, keep=0, more=[FadeOut(exit_chip), track(tr, 7)])
            for c in (np6, lap_c, again):
                under_term(t, c)
            assert ecr_name.get_bottom()[1] > np6.get_top()[1] + 0.05, (ecr_name.get_bottom(), np6.get_top())
            assert hub_name.get_top()[1] + 0.1 < ecr_r.get_bottom()[1] and ecr_r.get_top()[1] < hub.get_bottom()[1] - 0.05, \
                (ecr_r.get_bottom(), ecr_r.get_top(), hub.get_bottom())
            assert ecr.get_bottom()[1] < 1.38 - 0.1, ecr.get_bottom()
            # The narration lists all five steps in its first 6 s: the five commands type back to back.
            type_cmd(self, t, LOGIN[0], type_time=0.4)
            type_cmd(self, t, LOGIN[1], type_time=0.5, prompt=False)
            self.play(track(tr, 8), run_time=0.25)
            type_cmd(self, t, TAG_C, type_time=0.5)
            self.play(FadeIn(ecr_name, shift=UP * 0.15), track(tr, 9), run_time=0.4)
            type_cmd(self, t, PUSH_C, type_time=0.35)
            ecr_cb = cb.copy()
            self.add(ecr_cb)
            self.play(Create(ecr_r), ecr_cb.animate.scale(0.55).move_to(ecr_r.get_start()), run_time=0.35)
            self.play(ecr_cb.animate.move_to(ecr_r.get_end() + LEFT * 0.2), run_time=0.7)
            self.play(ecr_cb.animate.scale(1 / 0.55).move_to(ecr.spot()), track(tr, 10), run_time=0.35)
            type_cmd(self, t, LIST_C, type_time=0.45)
            self.play(track(tr, 11), run_time=0.25)
            type_cmd(self, t, ECHO_C, type_time=0.35)
            self.play(FadeIn(np6, shift=DOWN * 0.1), run_time=0.35)
            vo.wait_until("Tag only adds a second name")
            names = VGroup(hub_name.text, ecr_name.text)       # the words light up, not the tag boxes
            self.play(Indicate(cb, color=IMAGE, scale_factor=1.25),
                      Indicate(names, color=IMAGE, scale_factor=1.04), run_time=0.8)
            vo.wait_until("Run them on your laptop")
            self.play(FadeOut(np6), FadeIn(lap_c, shift=DOWN * 0.1), Indicate(lap, color=INK, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("which has no docker")
            self.play(Indicate(lap_c.text, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Then repeat for the processor image")
            self.play(FadeOut(VGroup(lap, cb, hub, hub_cb, ecr, ecr_cb, ecr_r, hub_name, ecr_name)), FadeOut(lap_c),
                      FadeIn(rc201, shift=DOWN * 0.2), run_time=0.6)
            self.play(Indicate(rc201.body[2], color=TURN, scale_factor=1.05), run_time=0.5)
            self.wipe(run_time=0.3)
            type_cmd(self, t, "cd ../data-processor", type_time=0.35)
            cd_prompt(self, t, P_SRC("data-processor"), run_time=0.4)
            type_cmd(self, t, REPO_B, type_time=0.35)
            cost.next_to(rc201, DOWN, buff=0.35).align_to(rc201, LEFT)
            assert cost.get_bottom()[1] > again.get_top()[1] + 0.1, (cost.get_bottom(), again.get_top())
            self.play(FadeIn(again, shift=DOWN * 0.1), FadeIn(cost, shift=UP * 0.1), run_time=0.5)
            self.play(Circumscribe(cost, color=COST, buff=0.06), run_time=0.8)
            self.wait(1.2)

        self.play(FadeOut(VGroup(rc201, again, cost, t, tr)), *self.unbar_anims(), run_time=0.8)
        self.wait(0.3)

    # ------------------------------------------------------------------ helpers
    def find(self, ln, sub: str) -> VGroup:
        """The glyphs of `sub` in a typed line (a soft-wrapped command: the row holding it)."""
        for r in rows_of(ln):
            if sub in r.text:
                return substring(r, sub)
        raise ValueError(f"{sub!r} not on one row of {[r.text for r in rows_of(ln)]}")

    def bar(self, tg):
        """Show a title-bar tag (on_bar) and remember it, so it fades with the terminal."""
        self.play(FadeIn(tg), run_time=0.3)
        self.bar_tags.append(tg)

    def unbar_anims(self):
        tgs, self.bar_tags = self.bar_tags, []
        return [FadeOut(tg) for tg in tgs]

    def resize(self, rows: int, keep=None, more=()):
        """common.resize() with the title-bar tags riding along (and `more` animations alongside)."""
        dy = (rows - self.t.rows) * self.t.pitch
        resize(self, self.t, rows, keep=keep, extra=[*[tg.animate.shift(UP * dy) for tg in self.bar_tags], *more])

    def wipe(self, *extra, run_time: float = 0.4):
        """PLAYS: the terminal's rows fade out (with `extra` alongside) and leave it for good."""
        t = self.t
        gone = list(t.lines.submobjects)
        for m in gone:
            t.lines.remove(m)
        if gone or extra:
            self.play(*[FadeOut(m) for m in gone], *extra, run_time=run_time)
        self.remove(*gone)
        self.reseat()

    def reseat(self):
        """Re-seat the terminal as one mobject (split trap) and keep its bar tags on top."""
        if self.t is not None:
            self.add(self.t, *self.bar_tags)
