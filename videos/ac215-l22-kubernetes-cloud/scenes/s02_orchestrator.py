"""S02 · From one box to a fleet (AC215 L22, the full follow-along). No tracker (except beat 5's sample).
Lecture: 22 · 17, 19 (held through beat 2), 21–22; beat 5 shows a sample tag 'slides 4–11'.

Beats (script.md "## S02", one voiceover block each):
0. LECTURE 22 · 17. 'Kubernetes' writes centre top in WHITE; on "an orchestrator" the two-line WHITE
   definition writes under it ('an orchestrator' YELLOW); on "The name is Greek" the GREY line
   'Greek: helmsman, the one who steers' (no wheel, no logo); on "and Helm" the GREY-dashed chip
   'Helm · part 2' slides in under it. (The SHOW lists the Greek line first; the narration says
   the definition first, so the picture follows the ear.)
1. LECTURE 22 · 19. V2 FleetMorph: left, one BLUE machine with a long GREY 'Docker' bar and five TEAL
   boxes, caption 'container deployment' (flashes on "one Docker engine"); on "On the right" a copy
   transforms into three BLUE nodes, each with its own runtime strip and the TEAL trio spread over
   them, lines up to one BLUE 'control plane', caption 'Kubernetes deployment'; the nodes flash on
   "called nodes", the control plane on "one control plane".
2. LECTURE (held). The GREY-dashed note under the right caption: 'deployment = a way of deploying ·
   ≠ Deployment, the object (S06)'; 'Deployment' glows GREEN; on "not the Deployment object" both
   captions' word 'deployment' is underlined YELLOW.
3. LECTURE 22 · 21–22. V5's opening frame drawn with V1's pieces: a GREY-dashed 'L20 · one VM' (TEAL
   nginx, frontend, api-service, vector-db, dashed loader) right of a GREY 'your laptop' box holding
   the TEAL toolbox with PURPLE gcloud, docker, pulumi. On "Now the same app goes to a cluster" the
   VM's outline transforms into the BLUE dashed 'Kubernetes cluster' outline (the app boxes stay
   inside); on "the tools gain kubectl" the largest chip kubectl arrives and flashes YELLOW; on "plus
   Helm" helm and gke-gcloud-auth-plugin arrive; on "which the slides do not list" a GREY-dashed
   'not on the slides' chip points at those two.
4. No lecture tag. The cluster and the note leave; the laptop stays left; chips slide in on the right,
   one per phrase: GREY 'cheese-app-v3 + secrets/ beside it', 'Docker running', 'a GCP project with
   billing', then the GOLD cost_tag 'clusters cost money by the hour · each part ends with a delete'.
5. Everything fades. Samples, one per phrase, each in the place it will occupy, each with one
   Indicate, at most two on screen: the YELLOW tracker top left (README › Create Simple Kubernetes
   Cluster Tutorial, step 1 of 11); a code panel centre (deploy-k8s-tic-tac-toe.yml · lines 2–7);
   a 3-row toolbox strip typing README:553 'kubectl get all' with a YELLOW '▶ your turn'; the GREY
   tag 'Lecture 22 · slides 4–11' top right.
6. The samples fade. A GREY card: left 'a machine you own → real, complete' (GREEN tick), right
   'Google → stops at its first honest error' (RED dot), a spanning line 'kubectl → a small stand-in
   cluster on the laptop, labelled [stand-in]', GREY footer 'and we say what yours prints'; each
   part writes on its phrase.
7. The card fades. A full-width 'laptop' terminal types p02 line 1 up to "%s'" (extra; the branch
   list p02:3–7 is never printed) and prints p02:2 (wrapped); the hash glows YELLOW, the date PINK,
   the message GREY (the date gets a PINK underline); the GREY chip 'the course site links: main' sits above the terminal.
8. The terminal fades. Two GREY cards: 'Part 1 · by hand · the lecture's warm-up' (a small GREY-dashed
   cluster with a TEAL game Pod) and 'Part 2 · as code · the cheese app on GKE' (a small BLUE-dashed
   cluster with GREEN cards over TEAL Pods). Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S02"]

TTT = "src/deployment/deploy-k8s-tic-tac-toe.yml"
SAMPLE_CMD = readme_rows(553, 553)[0]          # README:553 (› Try some kubectl commands)
assert SAMPLE_CMD == "kubectl get all", SAMPLE_CMD


def swap_ref(scene, old, slides: str | None, run_time: float = 0.4):
    """PLAYS: the lecture tag `old` (or None) cross-fades into lref(slides) (or nothing). Returns the new tag."""
    new = lref(slides) if slides else None
    anims = []
    if old is not None:
        anims.append(FadeOut(old))
    if new is not None:
        anims.append(FadeIn(new))
    if anims:
        scene.play(*anims, run_time=run_time)
    if old is not None:
        scene.remove(old)
    return new


def flash(boxes, color, width: float = 6):
    """ANIMs: each boxed() part's outline flashes `color` and its text pulses (Indicate on the whole box
    would fill the opaque box solid)."""
    out_ = []
    for b in boxes:
        out_.append(b.frame.edge.animate(rate_func=there_and_back).set_stroke(color, width))
        out_.append(Indicate(b.text, color=color, scale_factor=1.1))
    return out_


def edge_flash(frames, color, width: float = 6):
    """ANIMs: frame_box() outlines flash `color`."""
    return [f.edge.animate(rate_func=there_and_back).set_stroke(color, width) for f in frames]


def tag_flash(t, color, width: float = 4):
    """ANIMs: a tag()'s outline flashes `color` and its text pulses (Indicate on the whole tag would fill
    its opaque pill solid and hide the words)."""
    return [t.box.animate(rate_func=there_and_back).set_stroke(color, width),
            Indicate(t.text, color=color, scale_factor=1.03)]


def mini_cluster(colour, dashed_title: str) -> VGroup:
    """A small dashed cluster outline (2.6 x 1.5) with a GREY title under its top edge."""
    fr = frame_box(3.4, 1.7, colour, k=0.05, dashed=True)
    t = label(dashed_title, 20, colour).move_to(fr).align_to(fr, UL).shift(np.array([0.12, -0.06, 0]))
    g = VGroup(fr, t)
    g.frame = fr
    return g


class Orchestrator(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S02"] == 9, len(SAY)

        # ========================================================== 0. Kubernetes: an orchestrator
        with self.voiceover(SAY[0]) as vo:
            ref = swap_ref(self, None, "17")
            word = label("Kubernetes", 56, INK).move_to(UP * 1.75)
            self.play(Write(word), run_time=1.0)
            vo.wait_until("is an orchestrator")
            d1 = label("an orchestrator: runs containers across a cluster of machines,", 26, INK,
                       t2c={"an orchestrator": TURN})
            d2 = label("and keeps them as you declared", 26, INK)
            defn = VGroup(d1, d2).arrange(DOWN, buff=0.16).move_to(UP * 0.35)
            self.play(FadeIn(d1, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("across a cluster of machines")
            self.play(Indicate(substring_label(d1, "a cluster of machines"), color=TURN, scale_factor=1.08),
                      run_time=0.8)
            vo.wait_until("and keeps them the way you declared")
            self.play(FadeIn(d2, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("The name is Greek")
            greek = label("Greek: helmsman, the one who steers", 24, S.GREY).move_to(DOWN * 1.05)
            self.play(FadeIn(greek, shift=UP * 0.1), Indicate(word, color=INK, scale_factor=1.04),
                      run_time=0.8)
            vo.wait_until("and Helm")
            helm = dashed_chip("Helm · part 2").move_to(DOWN * 1.95)
            self.play(FadeIn(helm, shift=UP * 0.25), run_time=0.6)
            self.play(Indicate(helm.text, color=INK, scale_factor=1.1), run_time=0.6)

        # ========================================================== 1. container deployment → Kubernetes deployment
        with self.voiceover(SAY[1]) as vo:
            ref = swap_ref(self, ref, "19")
            self.play(FadeOut(VGroup(word, defn, greek, helm)), run_time=0.5)
            fm = FleetMorph()
            fm.docker_host(self, run_time=0.9)
            vo.wait_until("one machine runs every container")
            boxes5 = fm.host[2]
            self.play(LaggedStart(*[Indicate(b, color=TURN, scale_factor=1.08) for b in boxes5], lag_ratio=0.15),
                      run_time=1.0)
            fm.heal(self)
            vo.wait_until("on one Docker engine")
            self.play(*flash([fm.host[1]], TURN), run_time=0.8)
            fm.heal(self)
            vo.wait_until("On the right")
            fm.to_cluster(self, run_time=1.4)
            vo.wait_until("called nodes")
            plane, nodes, apps, links = fm.cluster_g
            self.play(*edge_flash([n[0] for n in nodes], TURN), run_time=0.9)
            fm.heal(self)
            vo.wait_until("share the containers")
            self.play(*flash([b for col in apps for b in col], TURN, 5), run_time=1.0)
            fm.heal(self)
            vo.wait_until("and one control plane")
            self.play(*flash([plane], TURN),
                      ShowPassingFlash(links.copy().set_stroke(TURN, 5), time_width=0.6), run_time=1.0)
            fm.heal(self)

        # ========================================================== 2. deployment ≠ Deployment
        with self.voiceover(SAY[2]) as vo:
            vo.wait_until("here, deployment means")
            fm.deployment_note(self)
            vo.wait_until("not the Deployment object")
            caps = [fm.host_cap, fm.cluster_cap]
            uls = VGroup(*[under(substring_label(c, "deployment"), TURN) for c in caps])
            self.play(Create(uls), run_time=0.6)
            self.play(Indicate(fm.note_g[1][2], color=OWN, scale_factor=1.12), run_time=0.7)
            fm.heal(self)

        # ========================================================== 3. L20's one VM → a cluster; the tools gain kubectl
        with self.voiceover(SAY[3]) as vo:
            ref = swap_ref(self, ref, "21–22")
            self.play(FadeOut(uls), run_time=0.3)
            self.remove(uls)
            fm.fade_all(self)
            md = MasterDiagram()          # its layout is fixed at construction: never shifted (see report)
            vm = l20_vm(9.8, 4.0).move_to(md.p(1.55, 0.75))
            shell = VGroup(vm.frame, vm.title)
            app = VGroup(*vm.boxes.values())
            md.laptop_box(self, chips=())
            # (the cluster's opaque fill fades in above the app boxes: hold them in front while it does)
            self.play(FadeIn(shell), FadeIn(app), run_time=0.6)
            md.add_chips(self, ("gcloud", "docker", "pulumi"), flash=False)
            vo.wait_until("Now the same app goes to a cluster")
            self.add_foreground_mobjects(app)
            md.cluster(self, source=shell, run_time=1.0)
            self.remove_foreground_mobjects(app)
            self.remove(app)
            md.add(app)                   # above the cluster's opaque fill; leaves with it in beat 4
            md.heal(self)
            self.play(*flash(list(vm.boxes.values()), TURN, 5), run_time=0.8)
            md.heal(self)
            vo.wait_until("and the tools gain kubectl")
            md.add_chips(self, ("kubectl",), flash=True)
            vo.wait_until("plus Helm and the GKE auth plugin")
            md.add_chips(self, ("helm", "gke-gcloud-auth-plugin"), flash=False)
            vo.wait_until("which the slides do not list")
            pair = VGroup(md.chips["helm"], md.chips["gke-gcloud-auth-plugin"])
            nots = dashed_chip("not on the slides")
            nots.next_to(md.parts["laptop"][0], DOWN, buff=0.18).align_to(md.parts["laptop"][0], LEFT)
            self.play(FadeIn(nots, shift=UP * 0.1),
                      *[Indicate(c, color=INK, scale_factor=1.08) for c in pair], run_time=0.8)
            md.heal(self)

        # ========================================================== 4. what you need; it costs money
        with self.voiceover(SAY[4]) as vo:
            ref = swap_ref(self, ref, None)
            md.drop(self, md.parts["cluster"], app, run_time=0.5, extra=[FadeOut(nots)])
            self.remove(nots)
            col_x = 1.6
            reqs = [grey_chip("cheese-app-v3 + secrets/ beside it", size=22),
                    grey_chip("Docker running", size=22),
                    grey_chip("a GCP project with billing", size=22)]
            for i, c in enumerate(reqs):
                c.move_to([col_x, 1.65 - i * 0.95, 0])
            vo.wait_until("cheese app version 3")
            self.play(FadeIn(reqs[0], shift=LEFT * 0.4), run_time=0.6)
            vo.wait_until("Docker,")
            self.play(FadeIn(reqs[1], shift=LEFT * 0.4), Indicate(md.chips["docker"], color=TURN), run_time=0.6)
            md.heal(self)
            vo.wait_until("and a Google Cloud project")
            self.play(FadeIn(reqs[2], shift=LEFT * 0.4), run_time=0.6)
            vo.wait_until("A cluster costs money")
            cost = cost_tag("clusters cost money by the hour · each part ends with a delete")
            cost.move_to([col_x, -1.6, 0])
            keep_inside(cost)
            self.play(FadeIn(cost, scale=1.1), run_time=0.6)
            vo.wait_until("so each part ends by deleting it")
            self.play(*tag_flash(cost, COST), run_time=0.8)

        # ========================================================== 5. how to read the screen: samples
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(md), FadeOut(VGroup(*reqs, cost)), run_time=0.5)
            self.remove(md, *reqs, cost)
            tr = tracker_w(1)
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(tr.caption, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("code panels name their file and lines")
            cp = code(TTT, 2, 7).move_to(UP * 0.55)
            self.play(FadeIn(cp, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(cp.header, color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("and your turn means")
            self.play(FadeOut(tr), run_time=0.3)
            self.remove(tr)
            t = toolbox_term(3)
            self.play(FadeIn(t), run_time=0.4)
            ln = type_cmd(self, t, SAMPLE_CMD)
            yt = beside(turn_row(), ln)
            pin(self, ln, yt)
            self.play(Indicate(yt, color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("A grey tag in the corner")
            self.play(FadeOut(cp), run_time=0.3)
            self.remove(cp)
            ref = swap_ref(self, ref, "4–11")
            self.play(*tag_flash(ref, INK), run_time=0.7)

        # ========================================================== 6. the honest note
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(t), run_time=0.4)
            self.remove(t)
            ref = swap_ref(self, ref, None)
            frame = outline_box(11.6, 4.6, S.GREY, solid=True, fill_opacity=0.08)
            frame.fill.set_fill(S.GREY_DARKER, 1)
            frame.move_to(UP * 0.2)
            head = label("an honest note: our recording machine has no Google account", 22, S.GREY)
            head.move_to(frame).align_to(frame, UP).shift(DOWN * 0.35)
            self.play(FadeIn(frame), FadeIn(head), run_time=0.6)
            vo.wait_until("What runs on a machine you own")
            lx, rx = -3.0, 2.9
            ltk = check_glyph(0.34)
            lt = VGroup(label("a machine you own", 24, INK), label("→ real, complete", 24, OWN))
            lt.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            left = VGroup(ltk, lt).arrange(RIGHT, buff=0.25).move_to([lx, 0.85, 0])
            self.play(FadeIn(left, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("every Google step")
            rdot = Dot(radius=0.13, color=ERR)
            rt = VGroup(label("Google", 24, INK), label("→ stops at its first honest error", 24, ERR))
            rt.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
            right = VGroup(rdot, rt).arrange(RIGHT, buff=0.25).move_to([rx, 0.85, 0])
            self.play(FadeIn(right, shift=UP * 0.1), run_time=0.6)
            span = VGroup(mono("kubectl", 22, TOOL), label("→ a small stand-in cluster on the laptop, labelled", 22, INK),
                          tag("stand-in", S.GREY)).arrange(RIGHT, buff=0.18)
            span.move_to([0, -0.45, 0])
            sep = DashedLine([-5.4, 0.0, 0], [5.4, 0.0, 0], color=S.GREY_DARK, stroke_width=2)
            self.play(Create(sep), FadeIn(span, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("and we say what yours prints")
            foot = label("and we say what yours prints", 22, S.GREY).move_to([0, -1.4, 0])
            self.play(FadeIn(foot, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(foot, color=INK, scale_factor=1.06), run_time=0.6)
            honest = VGroup(frame, head, left, right, sep, span, foot)

        # ========================================================== 7. which commit: git log
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(honest), run_time=0.5)
            self.remove(honest)
            t = laptop_term(5)
            t.shift(UP * (0.2 - t.box.get_center()[1]))
            site = grey_chip("the course site links: main", size=22)
            under_term(t, site)
            self.play(FadeIn(t), run_time=0.4)
            self.play(FadeIn(site, shift=DOWN * 0.1), run_time=0.4)
            p02 = capture("p02")
            ln = type_cmd(self, t, p02.typed("%s'"))
            xt = beside(extra_row(), ln)
            pin(self, ln, xt)
            rows = out(self, t, p02.at(2), wrap=True)
            whole = "".join(r.text + " " for r in rows)
            assert "3ecef56fea879ac480d260c0906cd95baf05179a" in whole and "2025-11-28" in whole and "v4->v3" in whole
            vo.wait_until("at this November 2025 commit")
            h = substring(rows[0], "3ecef56fea879ac480d260c0906cd95baf05179a")
            self.play(h.animate.set_color(TURN), run_time=0.5)
            date_row = next(r for r in rows if "2025-11-28" in r.text)
            msg_row = next(r for r in rows if "v4->v3" in r.text)
            dt = substring(date_row, "2025-11-28")
            self.play(dt.animate.set_color(ROUTE), run_time=0.4)
            dul = under(dt, ROUTE)
            self.play(Create(dul), run_time=0.5)
            msg = substring(msg_row, "v4->v3")
            self.play(msg.animate.set_color(S.GREY), run_time=0.4)
            self.add(t, dul)
            vo.wait_until("Git log tells you")
            self.play(Indicate(ln.rows[0] if hasattr(ln, "rows") else ln, color=TURN, scale_factor=1.03),
                      run_time=0.8)
            self.add(t, dul)

        # ========================================================== 8. two parts
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(t), FadeOut(site), FadeOut(dul), run_time=0.5)
            self.remove(t, site, dul)
            c1 = mini_cluster(STANDIN, "cluster")
            pod = pod_glyph(r=0.3).move_to(c1.frame.get_center() + DOWN * 0.15 + LEFT * 0.6)
            grid = ttt_grid(0.2).next_to(pod, RIGHT, buff=0.35)
            pic1 = VGroup(c1, pod, grid)
            card1 = card(["Part 1 · by hand", pic1, "the lecture's warm-up"], S.GREY, size=24, card_w=5.6)
            c2 = mini_cluster(CLOUD, "GKE")
            cards2 = VGroup(*[VGroup(frame_box(0.75, 0.5, OWN, k=0.16), pod_glyph(r=0.14, dots=1)).arrange(DOWN, buff=0.08)
                              for _ in range(3)]).arrange(RIGHT, buff=0.25)
            cards2.move_to(c2.frame.get_center() + DOWN * 0.12)
            pic2 = VGroup(c2, cards2)
            card2 = card(["Part 2 · as code", pic2, "the cheese app on GKE"], S.GREY, size=24, card_w=5.6)
            VGroup(card1, card2).arrange(RIGHT, buff=0.5).move_to(DOWN * 0.1)
            self.play(FadeIn(card1, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(pod, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Part 2 deploys the cheese app")
            self.play(FadeIn(card2, shift=UP * 0.15), run_time=0.6)
            self.play(LaggedStart(*[AnimationGroup(c[0].edge.animate(rate_func=there_and_back).set_stroke(TURN, 5),
                                                   Indicate(c[1], color=TURN, scale_factor=1.15))
                                    for c in cards2], lag_ratio=0.2), run_time=0.8)
        self.play(FadeOut(card1), FadeOut(card2), run_time=0.6)
        self.wait(0.3)


def substring_label(cap, word: str) -> VGroup:
    """The glyphs of `word` in a label() caption (a Text: neither its .text nor its glyphs keep spaces)."""
    s = "".join(cap.text.split())
    w = "".join(word.split())
    i = s.find(w)
    if i < 0:
        raise ValueError(f"{word!r} not in {cap.text!r}")
    return VGroup(*cap.submobjects[i:i + len(w)])
