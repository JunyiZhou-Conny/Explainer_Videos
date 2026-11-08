"""S02 · The final map, in AWS words (AC215 L23). No tracker (a lecture scene).
Lecture: 23 · slide 19 (beats 0–4), slides 5–6 (beat 5), slides 17–18 (beats 6–7).

Beats (script.md "## S02", one voiceover block each):
0. lecture_ref(23, "19") fades in. V2 TermMap draws slide 19's bottom flow left to right, one box
   per phrase: Dev Team -> PINK Commits -> GitHub (Code · Branches · Actions) -> GitHub Actions
   (Build → Deploy) -> the cloud box (GREY dashed Storage, Vertex AI, Kubernetes) -> Users.
1. Above it, slide 19's chain box by box: Data Collector … Frontend (WHITE outlines).
2. The GREY dashed source chip 'slides: Google Cloud · cheese-app-v4' turns into the BLUE 'this
   video: AWS · cheese-app-aws · as in L15'. The GCP words 'Artifact Registry' (in the cloud) and
   'Pulumi (L20)' (under Actions) appear, then three transforms, one per sentence: Kubernetes ->
   'one EC2 server · Docker containers', Artifact Registry -> 'ECR · 3 repositories', Pulumi ->
   'Ansible playbooks'. The BLUE chip pulses on "as in lecture 15", the EC2 label on "running
   Docker containers".
3. Three more, one per clause: 'service-account key' -> badge + key glyphs ('IAM access key', 'EC2
   key pair'); PINK '/deploy-app' over the commit arrow -> '/run-deploy-app'; dashed 'ingress' in
   the cloud -> TEAL 'nginx container'.
4. The EC2 server and Ansible labels are circled; the four ML boxes turn GREY dashed, the dashed
   Vertex AI chip dims (outline and text only)
   ('not in this repo · the AWS ML pipeline was L15'); the Model Deploy → Backend API arrow goes
   dashed with the chip 'a fixed model file, not a pipeline'.
5. The map and its tag fade (TermMap may not be scaled: its words would drop under 20 pt);
   lecture_ref(23, "5–6"); slide 6's five cards in a row under a GREY heading; marks per phrase:
   pipeline jobs and model training GREY dashed ✗ 'L15' (both chips pulse on "those were
   lecture 15"); frontend and backend GREEN ✓ with a bracket
   'always together · one keyword'; building and pushing containers GREEN ✓ 'three app images'.
6. The cards clear; lecture_ref(23, "17–18"). A TEAL crate `cheese-app-deployment` with a GREEN
   chip 'src/deployment/' under it; on the left a GREY laptop and a hand reach it ('part 1 · you');
   on the right a BLUE runner's arrow reaches it ('part 2 · GitHub's runner'); the crate's name
   pulses on "Here it's called".
7. Over the crate a GREY dashed chip 'invoke CLI in the deployment container' transforms into two
   PURPLE lines ('part 1: ansible-playbook … typed at its prompt', 'part 2: bash -c "…
   ansible-playbook …"'); each line pulses with its side, and the GREY captions 'Part 1 · deploy by
   hand' (left) and 'Part 2 · a commit presses the button' (right) write on. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S02"]

CRATE_Y = 0.0
LINE1 = ("part 1:", "ansible-playbook …", "typed at its prompt")
LINE2 = ("part 2:", 'bash -c "… ansible-playbook …"', "")


def purple_line(parts) -> VGroup:
    """A PURPLE line: label, mono command, label (20 pt)."""
    a, cmd, b = parts
    items = [label(a, 20, TOOL), mono(cmd, 20, TOOL)]
    if b:
        items.append(label(b, 20, TOOL))
    return VGroup(*items).arrange(RIGHT, buff=0.16)


class LectureMap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 8, len(SAY)

        # ========================================================== 0. slide 19's bottom flow
        m = TermMap()
        # 'Commits' is built 0.06 into the GitHub box's left edge: nudge it clear (still hidden here)
        m.commits_label.shift(LEFT * 0.13 + UP * 0.1)
        ref19 = lref("19")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref19), run_time=0.4)
            m.draw_flow(self, per=0.9)
            vo.wait_until("and users reach")
            self.play(Indicate(m.flow["users"], color=INK, scale_factor=1.15), run_time=0.7)

        # ========================================================== 1. the chain above it
        with self.voiceover(SAY[1]) as vo:
            m.draw_chain(self, per=0.4)

        # ========================================================== 2. GCP words -> AWS words
        with self.voiceover(SAY[2]) as vo:
            m.source(self)
            vo.wait_until("we follow the AWS repository")
            m.source(self)
            vo.wait_until("as in lecture 15")
            self.play(Indicate(m.src_chip, color=CLOUD, scale_factor=1.06), run_time=0.7)
            vo.wait_until("Now the same map")
            m.gcp(self, "registry")
            m.gcp(self, "pulumi")
            vo.wait_until("The Kubernetes cluster")
            m.relabel(self, "kubernetes")
            vo.wait_until("running Docker containers")
            self.play(Indicate(m.labels["kubernetes"], color=CLOUD, scale_factor=1.08), run_time=0.7)
            vo.wait_until("The image registry")
            m.relabel(self, "registry")
            vo.wait_until("Pulumi becomes")
            m.relabel(self, "pulumi")

        # ========================================================== 3. key, keyword, ingress
        with self.voiceover(SAY[3]) as vo:
            m.gcp(self, "key")
            vo.wait_until("an IAM access key")
            m.relabel(self, "key")
            vo.wait_until("The keyword")
            m.gcp(self, "keyword")
            vo.wait_until("slash run deploy app")
            m.relabel(self, "keyword")
            vo.wait_until("and the ingress")
            m.gcp(self, "ingress")
            vo.wait_until("one nginx container")
            m.relabel(self, "ingress")

        # ========================================================== 4. no K8s, no Pulumi, no ML lane
        with self.voiceover(SAY[4]) as vo:
            self.play(Circumscribe(m.labels["kubernetes"], color=CLOUD, buff=0.06), run_time=0.8)
            vo.wait_until("one server, set up by Ansible")
            self.play(Circumscribe(m.labels["pulumi"], color=CLOUD, buff=0.06), run_time=0.8)
            vo.wait_until("and no machine learning lane")
            # fade_ml dims Vertex AI with set_opacity, which also fills its dashed box (a grey blob):
            # hand it a stand-in and dim the real chip's stroke and text only, in the same beat
            vtx = m.cloud_rows["vertex"]
            stand_in = VectorizedPoint(vtx.get_center())
            m.cloud_rows["vertex"] = stand_in
            m.fade_ml(self)
            self.remove(stand_in)
            m.cloud_rows["vertex"] = vtx
            self.play(vtx.box.animate.set_stroke(opacity=0.45), vtx.text.animate.set_opacity(0.45),
                      run_time=0.5)

        # ========================================================== 5. slide 6's five cards
        ref56 = lref("5–6")
        sc = ScoreCards()
        sc.move_to([0, -0.3, 0])
        head = label("what the lecture wants automated", 24, S.GREY).move_to([0, 1.9, 0])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(m), FadeOut(ref19), run_time=0.6)
            self.remove(m, *m.get_family())
            self.play(FadeIn(ref56), FadeIn(head, shift=DOWN * 0.1),
                      LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in sc.cards], lag_ratio=0.15),
                      run_time=1.0)
            self.add(sc)
            vo.wait_until("For this repo")
            l15a = sc.mark(self, 0, False, "L15")[1]
            l15b = sc.mark(self, 1, False, "L15")[1]
            vo.wait_until("those were lecture 15")
            self.play(Indicate(l15a, color=INK, scale_factor=1.15),
                      Indicate(l15b, color=INK, scale_factor=1.15), run_time=0.8)
            vo.wait_until("Frontend and backend deployment")
            sc.mark(self, 2, True)
            sc.mark(self, 3, True)
            vo.wait_until("always together")
            # own brace: ScoreCards.bracket sits on the check marks (buff 0.08)
            br = Brace(VGroup(*sc.cards[2:4]), UP, color=PASS, buff=0.3)
            brt = label("always together · one keyword", 20, PASS).next_to(br, UP, buff=0.08)
            self.play(Create(br), FadeIn(brt), run_time=0.5)
            sc.keep(self, br, brt)
            vo.wait_until("Building and pushing containers")
            sc.mark(self, 4, True, "three app images")

        # ========================================================== 6. one crate, two operators
        ref1718 = lref("17–18")
        box_ = crate(T_TOOLBOX).move_to([0, CRATE_Y, 0])
        src = ok_chip("src/deployment/", mono_font=True).next_to(box_, DOWN, buff=0.18)
        lap = laptop_icon(1.2).move_to([-5.3, CRATE_Y, 0])
        hand = hand_glyph(0.8).rotate(PI / 2).next_to(lap, RIGHT, buff=0.15)
        you = label("part 1 · you", 22, LAPTOP).next_to(lap, DOWN, buff=0.3).shift(RIGHT * 0.6)
        run = runner_icon(0.75, lit=True).move_to([5.2, CRATE_Y, 0])
        reach = arrow(run.get_left(), box_.get_right(), CLOUD, 4)
        gh = label("part 2 · GitHub's runner", 22, CLOUD).next_to(run, DOWN, buff=0.3)
        gh.shift(LEFT * max(0.0, gh.get_right()[0] - 6.4))
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(sc), FadeOut(head), FadeOut(ref56), run_time=0.6)
            self.remove(sc, *sc.get_family())
            self.play(FadeIn(ref1718), FadeIn(box_, scale=0.9), run_time=0.7)
            vo.wait_until("we already have")
            self.play(FadeIn(src, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(lap), FadeIn(hand), FadeIn(you), run_time=0.5)
            self.play(hand.animate.shift(RIGHT * (box_.get_left()[0] - 0.12 - hand.get_right()[0])),
                      run_time=0.8)
            vo.wait_until("so let GitHub Actions run it")
            self.play(FadeIn(run, shift=LEFT * 0.2), FadeIn(gh), run_time=0.5)
            self.play(GrowArrow(reach), run_time=0.7)
            vo.wait_until("Here it's called")
            self.play(Indicate(box_.text, color=IMAGE, scale_factor=1.12), run_time=0.8)
            self.play(Indicate(src, color=OWN, scale_factor=1.08), run_time=0.6)

        # ========================================================== 7. invoke the CLI = ansible-playbook
        cli = dashed_chip("invoke CLI in the deployment container", PAST).move_to([0, 1.55, 0])
        l1 = purple_line(LINE1)
        l2 = purple_line(LINE2)
        lines = VGroup(l1, l2).arrange(DOWN, buff=0.22).move_to([0, 1.55, 0])
        cap1 = label("Part 1 · deploy by hand", 22, S.GREY)
        cap1.move_to([-6.4 + cap1.width / 2, -1.75, 0])
        cap2 = label("Part 2 · a commit presses the button", 22, S.GREY)
        cap2.move_to([6.4 - cap2.width / 2, -1.75, 0])
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeIn(cli, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Here, that means")
            self.play(ReplacementTransform(cli, lines), run_time=0.9)
            vo.wait_until("In part 1 you type them")
            self.play(Indicate(l1, color=TOOL, scale_factor=1.06),
                      Indicate(hand, color=INK, scale_factor=1.15), run_time=0.7)
            self.play(Write(cap1), run_time=0.7)
            vo.wait_until("in part 2")
            self.play(Indicate(l2, color=TOOL, scale_factor=1.06),
                      Indicate(run, color=CLOUD, scale_factor=1.15), run_time=0.7)
            self.play(Write(cap2), run_time=0.8)
        everything = VGroup(lines, box_, src, lap, hand, you, run, reach, gh, cap1, cap2, ref1718)
        self.play(FadeOut(everything), run_time=0.7)
        self.remove(*everything.get_family())
        self.wait(0.3)
