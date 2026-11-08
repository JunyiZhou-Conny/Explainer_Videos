"""S13 · Secrets and the runner — TRACKER C 2..5 (workflow › ci_cd_aws.yml · not in the README).
V3 KeyJourney (beats 2 and 8), V5 SiblingContainers on a BLUE runner (beat 7). No lecture tag.

Beats (script.md "## S13", one voiceover block each):
0. TRACKER C 2. ▶ your turn. CONSOLE("GitHub › New repository"; name cheese-app-aws, Private),
   illustration. A 4-row laptop terminal at P_REPO shows `git remote set-url origin
   https://github.com/<your-user>/cheese-app-aws.git` and `git push -u origin main`, written out,
   not run (bar tags `extra` + `written out, not run`). GREY chips "a fork works too · then Actions ›
   enable workflows" and "its last message is 'cleanup': no /run-, nothing runs" (laptop/03: 2).
1. TRACKER C 2. ▶ your turn. CONSOLE("GitHub › your repository › Settings › Secrets and variables ›
   Actions"): the four secret rows (`***`) appear one per phrase; erratum chip "not in the README ·
   names from ci_cd_aws.yml:21–22, 33, 81, 102–108".
2. TRACKER C 2. V3 KeyJourney(~/secrets/, GitHub vault): the badge, then the key, copy themselves
   into the vault; caption "badge · copy 3, on GitHub", a counter "key · copy 2" under the vault; a
   small runner glyph with the GOLD cost_tag("Actions minutes · private repos").
3. TRACKER C 3. CODE(ci_cd_aws.yml: 18–23): line 19 PURPLE, lines 21–22 PINK; a BLUE runner box
   "GitHub runner · fresh Ubuntu machine". Transform to CODE(25–33): line 27, line 28, line 33
   (YELLOW bars); line 33's secret sits past the panel's right edge, so a PINK chip quotes it:
   "line 33 · … ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr…".
4. TRACKER C 4. CODE(41–44): line 44 TEAL; a TEAL toolbox crate "built on the runner"; GREY chip
   "the committed Dockerfile → commit the Helm fix (S05)"; GREY dashed chip "same certificate error
   on GitHub's runner? not tested".
5. TRACKER C 4. CODE(46–50): line 48 GREEN (+ a GREEN chip "line 48 → …/src/deployment/.docker-tag",
   the line is trimmed), line 50 PINK. Laptop strip: heading row "ci_cd_aws.yml · lines 47–50 · run
   by hand" (bar tag "extra · the workflow's own commands, run by hand") → laptop/51: 5 GREEN; the
   GREEN tag card is stamped with that value.
6. TRACKER C 4. CODE(52–58): lines 56, 57, 58 TEAL one per phrase; GREY chip "lines 60–70: the same
   for vector-db-cli and api-service · not built here"; a BLUE runner row with the three TEAL images
   and a GREY dashed "not deploy-docker-images.yml".
7. TRACKER C 4. V5 SiblingContainers('runner'): crate, socket, then the mounts on their phrases
   (/deployment, /root/.ssh); the three app folders stay GREY dashed with a dashed chip "the runner
   built them already".
8. TRACKER C 5. CODE(72–81): lines 76–78 (the SSH config), line 81 PINK → Transform to CODE(83–90):
   lines 84–85 (chmod 600), lines 88–90 (copy). Laptop strip heading "ci_cd_aws.yml · lines 73–97 ·
   run by hand" → laptop/52: 15, 19–21, 25–26. The panel and strip leave; V3 KeyJourney(vault, runner
   ~/.ssh, toolbox /root/.ssh): the key lands in /root/.ssh with the GREEN chip "on the runner only ·
   never committed". Fade; empty frame.

Deviations from SHOW: beat 1's "TRACKER C 2 · extra" and beat 5's "C 4 · extra": tracker C's caption
is always "not in the README" (common.tracker), so "extra" is carried by tags on the terminals.
Beat 3: line 33's `secrets.AWS_ACCOUNT_ID` is past column 62 and is trimmed off the panel (the
whole line is 170 characters), so it is quoted in a PINK chip under the panel. Beat 5: likewise
line 48's `.docker-tag` path (a GREEN chip). Beat 8: the key's landing in /root/.ssh is drawn with V3
(the PLACES 'runner_ssh' -> 'toolbox_ssh' row) rather than V5's crate, which left in beat 7.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S13"]

WF = ".github/workflows/ci_cd_aws.yml"
assert excerpt(WF, 19, 19).strip() == "uses: aws-actions/configure-aws-credentials@v4"
assert "secrets.AWS_ACCESS_KEY_ID" in excerpt(WF, 21, 21) and "secrets.AWS_SECRET_ACCESS_KEY" in excerpt(WF, 22, 22)
assert excerpt(WF, 27, 28).split("\n") == ["          aws sts get-caller-identity", "          aws s3 ls"]
assert "secrets.AWS_ACCOUNT_ID" in excerpt(WF, 33, 33) and "aws ecr get-login-password" in excerpt(WF, 33, 33)
assert excerpt(WF, 44, 44).strip() == "docker build -t cheese-app-deployment -f Dockerfile ."
assert "date +%Y%m%d%H%M%S" in excerpt(WF, 48, 48) and ".docker-tag" in excerpt(WF, 48, 48)
assert excerpt(WF, 50, 50).strip() == 'echo "DOCKER_TAG=$DOCKER_TAG" >> $GITHUB_ENV'
assert excerpt(WF, 56, 56).strip().startswith("docker build -t cheese-app-frontend-react")
assert excerpt(WF, 57, 57).strip().startswith("docker tag ") and excerpt(WF, 58, 58).strip().startswith("docker push ")
assert excerpt(WF, 81, 81).strip() == 'echo "${{ secrets.AWS_SSH_KEY }}" > ~/.ssh/ac215_2024.pem'
assert excerpt(WF, 84, 85).split("\n") == ["          chmod 600 ~/.ssh/config", "          chmod 600 ~/.ssh/ac215_2024.pem"]
assert excerpt(WF, 88, 88).strip().startswith("mkdir -p") and excerpt(WF, 90, 90).strip().startswith("cp ~/.ssh/ac215_2024.pem")
C03 = capture("03")
assert C03.line(2).endswith(" cleanup"), C03.line(2)
C51 = capture("51")
assert C51.line(5) == "DOCKER_TAG=" + TAG_CI, C51.line(5)
C52 = capture("52")
L52 = C52.at(15, (19, 21), (25, 26))
assert L52[0] == "Runner SSH directory:" and L52[1].endswith("ac215_2024.pem") and L52[4].endswith("ac215_2024.pem")
assert L52[3] == "Deployment secrets directory:"
SET_URL = "git remote set-url origin " + YOUR_REPO_URL
PUSH = "git push -u origin main"


def gone(scene, *mobs, run_time: float = 0.5):
    """FadeOut mobjects that are not members of a piece, and take them off the scene."""
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def at_top(p, top: float = 2.75):
    """Centre a panel horizontally with its top edge at `top`."""
    return p.move_to([0, 0, 0]).shift(UP * (top - p.get_top()[1]))


def byhand_bar(t):
    """The run-by-hand strip's bar: its title moves left beside the dots, so that 'extra' and the
    long 'the workflow's own commands, run by hand' tag both fit on the bar's right end."""
    t.title.next_to(t.dots, RIGHT, buff=0.35)
    tags = VGroup(row_tag("the workflow's own commands, run by hand"), extra_row()).arrange(RIGHT, buff=0.15)
    return on_bar(t, tags)


def bars(p, ks, color, opacity: float = 0.22):
    return VGroup(*[line_bar(p.code, k, color, opacity) for k in ks])


class RunnerSecrets(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S13"] == 9, len(SAY)
        tr = tracker_c(2)

        # ========================================================== 0. your own repository
        c0 = console_drawing("GitHub › New repository",
                             [("Repository name", REPO), ("check", "Private", True)], where="github")
        c0.shift(np.array([-6.4 - c0.get_left()[0], 2.75 - c0.get_top()[1], 0]))
        turn0 = your_turn().next_to(c0.frame, RIGHT, buff=0.3).align_to(c0.frame, UP)
        fork = grey_chip("a fork works too · then Actions › enable workflows")
        fork.next_to(turn0, DOWN, buff=0.35).align_to(turn0, LEFT)
        clean = grey_chip("its last message is 'cleanup': no /run-, nothing runs")
        clean.next_to(fork, DOWN, buff=0.25).align_to(fork, LEFT)
        t0 = term(P_REPO, rows=4)
        bar0 = VGroup(row_tag("extra"), row_tag("written out, not run")).arrange(RIGHT, buff=0.15)
        on_bar(t0, bar0)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(c0, shift=UP * 0.2), run_time=0.7)
            self.play(Indicate(c0.where, color=CLOUD, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Pause, create an empty private one")
            self.play(FadeIn(turn0, shift=LEFT * 0.15), run_time=0.4)
            self.play(Circumscribe(c0.rows[0], color=TURN, buff=0.06), run_time=0.7)
            self.play(Indicate(c0.rows[1].text, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("point origin at it")
            self.play(FadeIn(t0, shift=UP * 0.2), FadeIn(bar0), run_time=0.5)
            type_cmd(self, t0, SET_URL, type_time=1.0)
            vo.wait_until("and push main")
            type_cmd(self, t0, PUSH, type_time=0.6)
            self.play(FadeIn(fork, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("Its last message")
            self.play(FadeIn(clean, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("so nothing runs yet")
            self.play(Indicate(clean.text, color=INK, scale_factor=1.06), run_time=0.7)

        # ========================================================== 1. four repository secrets
        c1 = console_drawing("GitHub › your repository › Settings › Secrets and variables › Actions",
                             [(s, MASKED) for s in SECRETS], where="github")
        at_top(c1)
        c1.shift(LEFT * 0.4)
        shell1 = VGroup(c1[0], c1[1], c1.where, c1.crumb, c1.tag)
        turn1 = your_turn().next_to(c1.frame, RIGHT, buff=0.25).align_to(c1.frame, UP)
        if turn1.get_right()[0] > 6.5:
            turn1.shift(LEFT * (turn1.get_right()[0] - 6.5))
        err1 = erratum_tag("not in the README · names from ci_cd_aws.yml:21–22, 33, 81, 102–108")
        err1.next_to(c1.frame, DOWN, buff=0.35)
        with self.voiceover(SAY[1]) as vo:
            gone(self, c0, turn0, fork, clean, t0, bar0)
            self.play(FadeIn(shell1, shift=UP * 0.2), FadeIn(turn1, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("in your repository, settings")
            self.play(Indicate(c1.crumb, color=TURN, scale_factor=1.04), run_time=1.0)
            for i, phrase in enumerate(["the access key ID", "the secret key", "your account ID",
                                        "and AWS S S H key"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c1.rows[i], shift=RIGHT * 0.15), run_time=0.4)
                self.play(Indicate(c1.rows[i].label, color=TURN, scale_factor=1.06), run_time=0.5)
            vo.wait_until("the whole pem file")
            self.play(Circumscribe(c1.rows[3], color=ROUTE, buff=0.06), run_time=0.8)
            vo.wait_until("The names come from the workflow")
            self.play(FadeIn(err1, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(err1.text, color=INK, scale_factor=1.05), run_time=0.7)

        # ========================================================== 2. V3: copies in a vault
        kj = KeyJourney(places=("secrets", "vault"))
        kj.places["secrets"].shift(LEFT * 1.2)
        kj.places["vault"].shift(RIGHT * 1.2)
        kj.move_to([0, 0.1, 0])
        kc = note("key · copy 2").next_to(kj.places["vault"].frame, DOWN, buff=0.3)
        run = runner_icon(0.42, lit=True)
        cost = cost_tag("Actions minutes · private repos")
        shelf = VGroup(run, cost).arrange(RIGHT, buff=0.25)
        shelf.next_to(kc, DOWN, buff=0.45)
        with self.voiceover(SAY[2]) as vo:
            gone(self, shell1, c1.rows, turn1, err1)
            self.play(FadeIn(kj, shift=UP * 0.15), run_time=0.5)
            kj.start(self, run_time=0.5)
            vo.wait_until("Your badge has a third copy now")
            kj.send(self, "badge", "secrets", "vault", run_time=1.2)
            kj.counter(self, "badge · copy 3, on GitHub")
            vo.wait_until("in a vault on GitHub")
            self.play(Indicate(kj.places["vault"].text, color=CLOUD, scale_factor=1.06), run_time=0.7)
            vo.wait_until("and your key a second")
            kj.send(self, "key", "secrets", "vault", arc=-0.6, run_time=1.2)
            self.play(FadeIn(kc, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Every copy is one more place")
            self.play(LaggedStart(*[Indicate(c, color=TURN, scale_factor=1.4)
                                    for k in ("secrets", "vault") for c in kj.copies[k]], lag_ratio=0.2),
                      run_time=1.2)
            self.play(FadeIn(shelf, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, cost, COST)

        # ========================================================== 3. AWS login on the runner
        p3 = at_top(code(WF, 18, 23))
        b19 = line_bar(p3.code, 1, TOOL, 0.25)
        b21 = bars(p3, (3, 4), ROUTE)
        runner = label_box(["GitHub runner", "fresh Ubuntu machine"], CLOUD, size=22)
        runner.text[1].set_color(S.GREY)
        ricon = runner_icon(0.5, lit=True)
        rbox = VGroup(ricon, runner).arrange(RIGHT, buff=0.3).move_to([0, -1.45, 0])
        p4 = at_top(code(WF, 25, 33, trim=62))
        b27 = line_bar(p4.code, 2, TURN, 0.22)
        b28 = line_bar(p4.code, 3, TURN, 0.22)
        b33 = line_bar(p4.code, 8, TURN, 0.22)
        acct = route_chip("line 33 · …${{ secrets.AWS_ACCOUNT_ID }}.dkr…")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(kj), FadeOut(kc), FadeOut(shelf), track(tr, 3), run_time=0.5)
            self.remove(kj, kc, shelf, *kj.get_family())
            self.play(FadeIn(p3, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("fresh Ubuntu machine")
            self.play(FadeIn(rbox, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(runner.text[1], color=CLOUD, scale_factor=1.08), run_time=0.6)
            vo.wait_until("An action from AWS")
            self.play(FadeIn(b19), run_time=0.4)
            self.play(Indicate(code_span(p3.code, 1, "aws-actions/configure-aws-credentials@v4"), color=TOOL,
                               scale_factor=1.06), run_time=0.7)
            vo.wait_until("from two secrets")
            self.play(FadeIn(b21), run_time=0.4)
            self.play(Indicate(code_span(p3.code, 3, "secrets.AWS_ACCESS_KEY_ID"), color=ROUTE, scale_factor=1.08),
                      Indicate(code_span(p3.code, 4, "secrets.AWS_SECRET_ACCESS_KEY"), color=ROUTE,
                               scale_factor=1.08), run_time=0.7)
            vo.wait_until("Then it checks who it is")
            self.play(FadeOut(VGroup(b19, b21)), ReplacementTransform(p3, p4),
                      rbox.animate.move_to([-6.4 + rbox.width / 2, -2.35, 0]), run_time=0.8)
            self.remove(b19, b21)
            self.play(FadeIn(b27), run_time=0.4)
            vo.wait_until("lists S3")
            self.play(FadeIn(b28), run_time=0.4)
            vo.wait_until("and logs Docker in")
            acct.move_to([6.5 - acct.width / 2, -2.35, 0])
            self.play(FadeIn(b33), run_time=0.4)
            self.play(FadeIn(acct, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(acct.text, color=ROUTE, scale_factor=1.05), run_time=0.7)

        # ========================================================== 4. the same toolbox, from the commit
        p5 = at_top(code(WF, 41, 44))
        b44 = line_bar(p5.code, 3, IMAGE, 0.25)
        box4 = crate(T_TOOLBOX, sub="built on the runner")
        box4.move_to([0, -0.3, 0])
        helm = grey_chip("the committed Dockerfile → commit the Helm fix (S05)", size=22)
        helm.move_to([0, -1.6, 0])
        cert = dashed_chip("same certificate error on GitHub's runner? not tested", size=22)
        cert.move_to([0, -2.6, 0])
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p4, b27, b28, b33, acct, rbox)), track(tr, 4), run_time=0.5)
            self.remove(p4, b27, b28, b33, acct, rbox, *p4.get_family())
            self.play(FadeIn(p5, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("Then it builds the same toolbox")
            self.play(FadeIn(b44), run_time=0.4)
            self.play(TransformFromCopy(code_span(p5.code, 3, "cheese-app-deployment"), box4.text),
                      FadeIn(VGroup(box4.frame, box4.sub)), run_time=0.8)
            vo.wait_until("from the committed Dockerfile")
            self.play(Indicate(code_span(p5.code, 3, "Dockerfile"), color=IMAGE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("So the Helm fix")
            self.play(FadeIn(helm, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(helm.text, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("We didn't test")
            self.play(FadeIn(cert, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(cert.text, color=S.GREY, scale_factor=1.05), run_time=0.7)

        # ========================================================== 5. a fresh tag (run by hand)
        p6 = at_top(code(WF, 46, 50, font_size=20, trim=72))
        b48 = line_bar(p6.code, 2, OWN, 0.25)
        b50 = line_bar(p6.code, 4, ROUTE, 0.25)
        dtag = ok_chip("line 48 → …/src/deployment/.docker-tag", mono_font=True)
        dtag.next_to(p6, DOWN, buff=0.3).align_to(p6, RIGHT)
        t5 = term(P_REPO, rows=3)
        bar5 = byhand_bar(t5)
        card = tag_card(TAG_CI, OWN)
        card.next_to(p6, DOWN, buff=0.3).align_to(p6, LEFT).shift(RIGHT * 0.4)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p5, b44, box4, helm, cert)), run_time=0.5)
            self.remove(p5, b44, box4, helm, cert, *p5.get_family())
            self.play(FadeIn(p6, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("a fresh tag from the date")
            self.play(FadeIn(b48), run_time=0.4)
            self.play(Indicate(code_span(p6.code, 2, "date +%Y%m%d%H%M%S"), color=OWN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("written to dot docker tag")
            self.play(FadeIn(dtag, shift=UP * 0.12), run_time=0.5)
            vo.wait_until("and to a file GitHub keeps")
            self.play(FadeIn(b50), run_time=0.4)
            self.play(Indicate(code_span(p6.code, 4, ">> $GITHUB_ENV"), color=ROUTE, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Run by hand")
            self.play(FadeIn(t5, shift=UP * 0.2), FadeIn(bar5), run_time=0.5)
            h5 = put_heading(self, t5, "ci_cd_aws.yml · lines 47–50 · run by hand")
            row = out(self, t5, [(C51.line(5), OWN)], run_time=0.5)
            vo.wait_until("it gives a timestamp")
            self.play(TransformFromCopy(row[0], card), run_time=0.8)
            self.play(Indicate(card.text, color=OWN, scale_factor=1.08), run_time=0.6)

        # ========================================================== 6. plain docker build / tag / push
        p7 = at_top(code(WF, 52, 58, font_size=20, trim=72))
        b56, b57, b58 = [line_bar(p7.code, k, IMAGE, 0.25) for k in (4, 5, 6)]
        rest = grey_chip("lines 60–70: the same for vector-db-cli and api-service · not built here")
        rest.next_to(p7, DOWN, buff=0.3)
        imgs = VGroup(*[image_chip(n) for n in SHORT_IMAGES]).arrange(RIGHT, buff=0.25)
        rlab = VGroup(runner_icon(0.42, lit=True), label("runner builds", 22, CLOUD)).arrange(RIGHT, buff=0.2)
        rrow = VGroup(rlab, imgs).arrange(RIGHT, buff=0.4)
        rframe = box(rrow.width + 0.6, rrow.height + 0.4, CLOUD, fill_opacity=0.05)
        rframe.move_to(rrow)
        rgrp = VGroup(rframe, rrow).move_to([0, -2.1, 0])
        notpb = dashed_chip("not deploy-docker-images.yml", mono_font=True)
        notpb.next_to(rgrp, DOWN, buff=0.2)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(p6, b48, b50, dtag, t5, bar5, card)), run_time=0.5)
            self.remove(p6, b48, b50, dtag, t5, bar5, card, *p6.get_family(), *t5.get_family())
            self.play(FadeIn(p7, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("Then plain docker build")
            self.play(FadeIn(b56), run_time=0.4)
            self.play(Indicate(code_span(p7.code, 4, "docker build"), color=IMAGE, scale_factor=1.15), run_time=0.5)
            vo.wait_until("docker tag and")
            self.play(FadeIn(b57), run_time=0.4)
            vo.wait_until("docker push for")
            self.play(FadeIn(b58), run_time=0.4)
            self.play(Indicate(code_span(p7.code, 2, "# Frontend React"), color=IMAGE, scale_factor=1.1), run_time=0.6)
            vo.wait_until("and the same for the other two")
            self.play(FadeIn(rest, shift=UP * 0.12), run_time=0.5)
            vo.wait_until("In C I, the runner builds")
            self.play(FadeIn(VGroup(rframe, rlab), shift=UP * 0.15), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.2) for m in imgs], lag_ratio=0.25), run_time=0.8)
            vo.wait_until("not the playbook")
            self.play(FadeIn(notpb, shift=UP * 0.12), run_time=0.5)

        # ========================================================== 7. V5 on the runner
        v5 = SiblingContainers("runner")
        v5.move_to([0, -0.1, 0])
        built = dashed_chip("the runner built them already")
        app_keys = ("api", "frontend", "vectordb")
        apps = VGroup(*[v5.folders[k] for k in app_keys])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(p7, b56, b57, b58, rest, rgrp, notpb)), run_time=0.5)
            self.remove(p7, b56, b57, b58, rest, rgrp, notpb, *p7.get_family())
            self.play(FadeIn(v5, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("So the toolbox only deploys")
            self.play(Circumscribe(v5.crate.frame, color=IMAGE, buff=0.06), run_time=0.9)
            vo.wait_until("Compared with your laptop")
            self.play(Indicate(v5.crate.text, color=IMAGE, scale_factor=1.08), run_time=0.7)
            vo.wait_until("same socket")
            v5.mount(self, "socket", run_time=0.7)
            vo.wait_until("But the deployment folder")
            v5.mount(self, "deployment", run_time=0.7)
            self.play(Indicate(v5.mpoints["deployment"], color=OWN, scale_factor=1.1), run_time=0.5)
            vo.wait_until("the keys at slash root")
            v5.mount(self, "ssh", run_time=0.7)
            self.play(Indicate(v5.mpoints["ssh"], color=ROUTE, scale_factor=1.1), run_time=0.5)
            vo.wait_until("and no app folders")
            built.next_to(v5.frame, DOWN, buff=0.2).align_to(v5.frame, LEFT)
            self.play(LaggedStart(*[Indicate(f, color=S.GREY, scale_factor=1.08) for f in apps], lag_ratio=0.2),
                      FadeIn(built, shift=UP * 0.15), run_time=0.8)
        # a short hold after the block: the three folders that are never mounted, and why
        self.play(Indicate(built.text, color=S.GREY, scale_factor=1.08),
                  LaggedStart(*[Indicate(v5.mpoints[k], color=S.GREY, scale_factor=1.08) for k in app_keys],
                              lag_ratio=0.2), run_time=1.0)
        self.wait(0.6)

        # ========================================================== 8. the SSH key on the runner
        p8 = at_top(code(WF, 72, 81))
        b_cfg = bars(p8, (4, 5, 6), TURN)
        b81 = line_bar(p8.code, 9, ROUTE, 0.25)
        p9 = at_top(code(WF, 83, 90, font_size=20, trim=72))
        b84 = bars(p9, (1, 2), TURN)
        b88 = bars(p9, (5, 6, 7), TURN)
        t8 = term(P_REPO, rows=4)
        bar8 = byhand_bar(t8)
        kj2 = KeyJourney(places=("vault", "runner_ssh", "toolbox_ssh"))
        kj2.move_to([0, 0.4, 0])
        safe = ok_chip("on the runner only · never committed", size=22)
        safe.next_to(kj2, DOWN, buff=0.6)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(v5), FadeOut(built), track(tr, 5), run_time=0.5)
            self.remove(v5, built, *v5.get_family())
            self.play(FadeIn(p8, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("The step writes an S S H config")
            self.play(FadeIn(b_cfg), run_time=0.4)
            vo.wait_until("and your key as AC215")
            self.play(FadeIn(b81), run_time=0.4)
            self.play(Indicate(code_span(p8.code, 9, "secrets.AWS_SSH_KEY"), color=ROUTE, scale_factor=1.1),
                      Indicate(code_span(p8.code, 9, "~/.ssh/ac215_2024.pem"), color=ROUTE, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("with mode 600")
            self.play(FadeOut(VGroup(b_cfg, b81)), ReplacementTransform(p8, p9), run_time=0.6)
            self.remove(b_cfg, b81)
            self.play(FadeIn(b84), FadeIn(t8, shift=UP * 0.2), FadeIn(bar8), run_time=0.4)
            h8 = put_heading(self, t8, "ci_cd_aws.yml · lines 73–97 · run by hand", run_time=0.3)
            rows8 = out(self, t8, L52[:3], run_time=0.5)
            self.play(*[Indicate(VGroup(*r.glyphs[:10]), color=TURN, scale_factor=1.1) for r in rows8[1:]],
                      run_time=0.6)
            vo.wait_until("It copies both")
            self.play(FadeIn(b88), run_time=0.4)
            rows8 = out(self, t8, L52[3:], run_time=0.5)
            vo.wait_until("on the runner only")
            self.play(Indicate(VGroup(*rows8[1].glyphs[-14:]), color=ROUTE, scale_factor=1.08), run_time=0.6)
            vo.wait_until("never committed")
            self.play(FadeOut(VGroup(p9, b84, b88, t8, bar8)), run_time=0.5)
            self.remove(p9, b84, b88, t8, bar8, *p9.get_family(), *t8.get_family())
            self.play(FadeIn(kj2, shift=UP * 0.15), run_time=0.5)
            kj2.send(self, "key", "vault", "runner_ssh", run_time=0.9)
            kj2.send(self, "key", "runner_ssh", "toolbox_ssh", run_time=0.9)
            self.play(FadeIn(safe, shift=UP * 0.15), run_time=0.5)
        # a short hold after the block: the key's two places on the runner, and the promise
        self.play(Indicate(safe.text, color=OWN, scale_factor=1.06),
                  Circumscribe(kj2.places["toolbox_ssh"].frame, color=IMAGE, buff=0.06), run_time=1.0)
        self.wait(1.2)
        del rows8

        self.play(FadeOut(kj2), FadeOut(safe), FadeOut(tr), run_time=0.6)
        self.remove(kj2, safe, tr, *kj2.get_family())
        self.wait(0.3)
