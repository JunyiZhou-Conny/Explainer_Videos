"""S03 · Inside a cluster: brain and workers (AC215 L22, the full follow-along). No tracker.
Lecture: 22 · 22, 23, 24–25 (held through beat 3), 26 (held through beat 5), 22–26 (recap), 27.

V1 MasterDiagram, moved down 0.6 so its callout slot sits under it (y about -2.3).

Beats (script.md "## S03", one voiceover block each):
0. LECTURE 22 · 22. Beat 22: the GREY 'your laptop' box with the TEAL toolbox and its six PURPLE
   chips (kubectl largest) on "Let's open the cluster", the BLUE dashed 'Kubernetes cluster' outline;
   on "First: one control plane" the control plane panel and three BLUE 'worker node (VM)' boxes, the
   fan of arrows to them; the arrows turn PINK on "with arrows"; the nodes' outlines flash on "each an
   ordinary virtual machine".
1. LECTURE 22 · 23. Beat 23: 'run by Google' under 'control plane', the slot under the diagram gets
   the GREY-dashed 'slides: master nodes' and the BLUE node-pool line (1–2 × n2d-standard-2 ·
   us-central1-a); the plane flashes on "the brain", its caption on "Google runs it", the nodes on
   "The workers carry", the node-pool line on "a pool of one or two nodes".
2. LECTURE 22 · 24–25. The slot empties. 'API server' grows, a YELLOW pulse runs kubectl → API server
   and 'API server · the single entry point' writes in the slot; 'scheduler' and 'controllers' (a
   stack of three cards) grow above it, greyed under a veil, each joined to the API server only; the
   etcd cylinder grows below, its callout writes, and a GREEN 'desired state' card rides kubectl →
   API server → into etcd.
3. LECTURE (held). The pulse goes API server → scheduler, its veil lifts, its callout writes and
   it picks worker 2 (flashes); then API server → controllers, veil lifts, callout, a YELLOW ring
   turns; on "some of them ask the cloud" the BLUE 'cloud provider API' box appears top left and the
   PINK arrow 'nodes, load-balancer IP' runs to it from the controllers.
4. LECTURE 22 · 26. Worker 1 (the tall node) glows YELLOW (no zoom: it would cover workers 2, 3); inside it kubelet (all workers), kube-proxy and
   the strip 'container runtime: containerd' grow one per phrase with their callouts in the slot;
   two TEAL Pods with container dots grow on the strip on "grouped in Pods".
5. LECTURE (held). The slide's 'Docker' in a GREY-dashed chip right of kube-proxy, just above the
   word containerd (the gap over the strip is too narrow), is crossed out and 'containerd' flashes;
   the 'erratum' tag waits right of where the panel goes; the slot empties and a one-line panel
   CODE(create_cluster.py: 52, the comment's middle elided) slides up, "cos_containerd" YELLOW;
   on "You still build images with Docker" the toolbox's docker chip flashes, on "they run
   unchanged" the Pods do.
6. LECTURE 22 · 22–26. Recap: the note and panel fade. A YELLOW pulse kubectl → API server ('the
   only door' in the slot); the GREEN 'desired state' card drops into etcd; the arrowheads turn
   round: YELLOW arrows scheduler → API server and workers 1, 2 → API server replace two PINK fan
   arrows, 'watch · they ask the API server for work' in the slot, the two kubelets flash.
7. LECTURE 22 · 27. V1 dims behind a veil (instead of shrinking: text never scales below its size);
   the fan arrows turn back to PINK; KubectlGrammar on a PURPLE card centre: the four slots flash on "a
   command", "a type", "an optional name" (GREY chip 'optional · one object'), "and flags"; then
   'kubectl get nodes', 'kubectl get pods', 'kubectl get pods --all-namespaces' slot in.
8. The card fades; the veil lifts. The scheduler, controllers and kubelets flash on "ask which of
   these parts"; four small YELLOW lamps light, unlabelled (scheduler, controllers, cloud arrow,
   kubelet), pulse on "each with a symptom", go out. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S03"]

CC = "src/deployment/deploy_k8s/create_cluster.py"


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


def edge_flash(frames, color=TURN, width: float = 6):
    """ANIMs: frame_box() outlines flash `color` (Indicate would fill an opaque box solid)."""
    return [f.edge.animate(rate_func=there_and_back).set_stroke(color, width) for f in frames]


def stroke_flash(shapes, color=TURN, width: float = 6):
    """ANIMs: plain outlines (a chip's .box) flash `color`."""
    return [m.animate(rate_func=there_and_back).set_stroke(color, width) for m in shapes]


def veil(m, color, opacity: float = 0.7, pad: float = 0.06) -> Rectangle:
    """A borderless rectangle in the background colour laid over `m`: it looks greyed out."""
    return Rectangle(width=m.width + 2 * pad, height=m.height + 2 * pad, stroke_width=0) \
        .set_fill(color, opacity).move_to(m)


def lamp_glyph(color=TURN) -> VGroup:
    """V1's symptom lamp (as MasterDiagram.lamp draws it), placed by the scene."""
    c = Circle(radius=0.12, stroke_color=color, stroke_width=3).set_fill(color, 0.85)
    glow = Circle(radius=0.2, stroke_width=0).set_fill(color, 0.25)
    return VGroup(glow, c)


def lamp_points(md):
    """Where S03's four unlabelled lamps sit, clear of every word: the scheduler's top-left corner,
    the controllers' top-right corner, the cloud arrow just left of its bend, the first kubelet's top-left."""
    ca = md.parts["cloud_arrow"].line[0].get_points()
    bend = max((pt for pt in ca), key=lambda q: (q[1], q[0]))
    return [md.parts["scheduler"].frame.get_corner(UL) + np.array([0.02, 0.02, 0]),
            md.parts["controllers"].frame.get_corner(UR) + np.array([0.1, 0.12, 0]),
            bend + LEFT * 0.3,
            md.parts["kubelet"][0].box.get_corner(UL) + np.array([-0.08, 0.1, 0])]


class ClusterAnatomy(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 9, len(SAY)

        md = MasterDiagram()
        md.shift(DOWN * 0.6)
        md._layout()                    # the layout is computed from the anchor: recompute after the move
        plane_tint = tint(CLOUD, 0.14)

        # ========================================================== 0. slide 22: plane and workers
        with self.voiceover(SAY[0]) as vo:
            ref = swap_ref(self, None, "22")
            md.laptop_box(self, chips=("gcloud", "docker", "pulumi", "kubectl", "helm", "gke-gcloud-auth-plugin"))
            md.cluster(self)
            vo.wait_until("The lecture draws it in three steps")
            self.play(Indicate(md.parts["cluster"].title, color=TURN, scale_factor=1.1), run_time=0.8)
            md.heal(self)
            vo.wait_until("First: one control plane")
            md.beat22(self, run_time=1.0)
            vo.wait_until("with arrows to several worker nodes")
            self.play(md.parts["fan"].animate.set_color(ROUTE), run_time=0.6)
            md.heal(self)
            vo.wait_until("each an ordinary virtual machine")
            self.play(*edge_flash([n.frame for n in md.nodes]), run_time=0.9)
            md.heal(self)

        # ========================================================== 1. slide 23: the planes get names
        with self.voiceover(SAY[1]) as vo:
            ref = swap_ref(self, ref, "23")
            md.beat23(self, run_time=1.0)
            vo.wait_until("The control plane is the brain")
            self.play(*edge_flash([md.parts["plane"].frame]),
                      Indicate(md.parts["plane"].title, color=TURN, scale_factor=1.1), run_time=0.9)
            md.heal(self)
            vo.wait_until("On GKE, Google runs it")
            self.play(Indicate(md.parts["plane_cap"], color=TURN, scale_factor=1.15), run_time=0.8)
            md.heal(self)
            vo.wait_until("The workers carry your containers")
            self.play(*edge_flash([n.frame for n in md.nodes]), run_time=0.9)
            md.heal(self)
            vo.wait_until("a pool of one or two nodes")
            self.play(Indicate(md.slot[1], color=TURN, scale_factor=1.06), run_time=0.9)
            md.heal(self)

        # ========================================================== 2. slides 24-25: API server and etcd
        with self.voiceover(SAY[2]) as vo:
            ref = swap_ref(self, ref, "24–25")
            md.clear_slot(self)
            vo.wait_until("The API server is the single entry point")
            md.part(self, "api", run_time=0.6)
            md.pulse(self, ["kubectl", "api"], run_time=0.8)
            md.callout(self, "api")
            vo.wait_until("every other part talks only to it")
            md.part(self, "scheduler", run_time=0.5)
            md.part(self, "controllers", run_time=0.5)
            v_s = veil(md.parts["scheduler"], plane_tint)
            v_c = veil(md.parts["controllers"], plane_tint)
            md.show(self, v_s, v_c, run_time=0.4)
            vo.wait_until("Etcd is the memory of the cluster")
            md.part(self, "etcd", run_time=0.6)
            md.callout(self, "etcd")
            md.wish(self, run_time=1.6)

        # ========================================================== 3. scheduler, controllers, cloud
        with self.voiceover(SAY[3]) as vo:
            md.drop(self, v_s, run_time=0.3)
            md.pulse(self, ["api", "scheduler"], run_time=0.6)
            md.callout(self, "scheduler")
            md.pick(self, (1,), run_time=1.0)
            vo.wait_until("The controllers keep watching")
            md.drop(self, v_c, run_time=0.3)
            md.pulse(self, ["api", "controllers"], run_time=0.6)
            md.callout(self, "controllers")
            vo.wait_until("and fix any difference")
            md.loop(self, run_time=1.4)
            vo.wait_until("some of them ask the cloud")
            md.part(self, "cloud", run_time=0.5)
            md.part(self, "cloud_arrow", run_time=0.7)
            md.callout(self, "cloud")

        # ========================================================== 4. slide 26: inside a worker
        with self.voiceover(SAY[4]) as vo:
            ref = swap_ref(self, ref, "26")
            md.clear_slot(self)
            self.play(*edge_flash([md.nodes[0].frame], TURN, 7), run_time=0.9)
            md.heal(self)
            vo.wait_until("the kubelet is the hands of the API server")
            md.part(self, "kubelet", run_time=0.6)
            md.callout(self, "kubelet")
            vo.wait_until("it starts and stops the containers")
            self.play(*stroke_flash([c.box for c in md.parts["kubelet"]]), run_time=0.8)
            md.heal(self)
            vo.wait_until("Kube proxy routes traffic for Services")
            md.part(self, "proxy", run_time=0.6)
            md.callout(self, "proxy")
            vo.wait_until("and a container runtime runs the containers")
            md.part(self, "runtime", run_time=0.6)
            md.callout(self, "runtime")
            vo.wait_until("grouped in Pods")
            pods = md.pods(self, 0, 2, run_time=0.7)

        # ========================================================== 5. erratum: Docker → containerd
        with self.voiceover(SAY[5]) as vo:
            panel = code(CC, 52, dedent=True, elide={52: "Container-Optimized OS with "})
            panel.move_to([-0.55, 0, 0]).align_to([0, md.parts["cluster"].frame.get_bottom()[1] - 0.3, 0], UP)
            vo.wait_until("the slide names Docker as the runtime")
            strip = md.parts["runtime"]
            cd_word = strip.text[-len("containerd"):]
            docker = dashed_chip("Docker")
            docker.next_to(md.parts["proxy"], RIGHT, buff=0.3)
            x_out = strike(docker.text, S.GREY)
            err = erratum_tag().next_to(panel, RIGHT, buff=0.2)
            md.show(self, docker, run_time=0.5)
            md.show(self, x_out, err, anims=[Create(x_out), FadeIn(err)], run_time=0.5)
            self.play(Indicate(cd_word, color=TURN, scale_factor=1.12), run_time=0.7)
            md.heal(self)
            vo.wait_until("On GKE it is containerd")
            md.clear_slot(self)
            self.play(FadeIn(panel, shift=UP * 0.3), run_time=0.6)
            hl = code_span(panel.code, 0, '"cos_containerd"')
            self.play(hl.animate.set_color(TURN), run_time=0.5)
            self.add(panel)
            vo.wait_until("You still build images with Docker")
            self.play(Indicate(md.chips["docker"], color=TURN, scale_factor=1.15), run_time=0.8)
            md.heal(self)
            vo.wait_until("and they run unchanged")
            self.play(*[Indicate(p, color=TURN, scale_factor=1.15) for p in pods], run_time=0.8)
            md.heal(self)

        # ========================================================== 6. recap: follow the arrows
        with self.voiceover(SAY[6]) as vo:
            ref = swap_ref(self, ref, "22–26")
            self.play(FadeOut(panel), run_time=0.4)
            self.remove(panel)
            md.drop(self, docker, x_out, err, run_time=0.4)
            vo.wait_until("Every kubectl command goes to one place")
            md.pulse(self, ["kubectl", "api"], run_time=0.6)
            md.callout(self, "api", "API server · the only door")
            vo.wait_until("which stores your wish in etcd")
            md.wish(self, run_time=1.1)
            vo.wait_until("The scheduler and the kubelets")
            # the arrowheads turn round: scheduler and the workers of two nodes → API server ('watch')
            fan = md.parts["fan"]
            api_r = md.parts["api"].frame.get_right()
            sch = md.parts["scheduler"].frame
            back = [fan[i].copy() for i in (0, 1)]
            w_s = arrow(sch.get_bottom() + RIGHT * 0.3, md.parts["api"].frame.get_top() + LEFT * 0.35, TURN,
                        stroke=4, buff=0.02)
            w_n = [arrow(md.nodes[i].frame.get_left() + RIGHT * 0.02, api_r, TURN, stroke=4) for i in (0, 1)]
            watch_t = label("watch · they ask the API server for work", 24, TURN)
            watch_t.move_to([md.ref.get_center()[0], md.slot_y, 0])
            md.clear_slot(self)
            md.show(self, w_s, anims=[GrowArrow(w_s)], run_time=0.4)
            olds = [fan[0], fan[1]]
            for i in (0, 1):
                md.swap(self, olds[i], w_n[i], run_time=0.4)
            md._set_slot(self, watch_t, run_time=0.5)
            self.play(*stroke_flash([c.box for c in list(md.parts["kubelet"])[:2]]), run_time=0.7)
            md.heal(self)

        # ========================================================== 7. slide 27: kubectl's grammar
        with self.voiceover(SAY[7]) as vo:
            ref = swap_ref(self, ref, "27")
            dim = veil(md, S.BG, opacity=0.88, pad=0.1)
            md.clear_slot(self)
            md.drop(self, w_s, run_time=0.3)
            for i in (0, 1):
                md.swap(self, w_n[i], back[i], run_time=0.3)
            kg = KubectlGrammar()
            card_bg = frame_box(13.0, 2.9, TOOL, k=0.05).move_to([0, -0.2, 0])
            md.show(self, dim, run_time=0.5)
            self.play(FadeIn(card_bg), FadeIn(kg), run_time=0.6)
            vo.wait_until("a command")
            self.play(*edge_flash([kg.slots[0]]), Indicate(kg.heads[0], color=TURN), run_time=0.5)
            vo.wait_until("a type")
            self.play(*edge_flash([kg.slots[1]]), Indicate(kg.heads[1], color=TURN), run_time=0.5)
            vo.wait_until("an optional name")
            self.play(*edge_flash([kg.slots[2]]), Indicate(kg.heads[2], color=TURN), run_time=0.5)
            kg.name_note(self)
            vo.wait_until("and flags")
            self.play(*edge_flash([kg.slots[3]]), Indicate(kg.heads[3], color=TURN), run_time=0.5)
            kg.heal(self)
            vo.wait_until("Get nodes")
            kg.fill(self, "get", "nodes")
            vo.wait_until("Get pods.")
            kg.fill(self, "get", "pods")
            vo.wait_until("Get pods, with a flag")
            kg.fill(self, "get", "pods", None, "--all-namespaces")

        # ========================================================== 8. four lamps, for later
        with self.voiceover(SAY[8]) as vo:
            ref = swap_ref(self, ref, None)
            self.play(FadeOut(kg), FadeOut(card_bg), run_time=0.5)
            self.remove(kg, card_bg)
            md.drop(self, dim, run_time=0.5)
            vo.wait_until("ask which of these parts is waiting")
            self.play(LaggedStart(*edge_flash([md.parts["scheduler"].frame, md.parts["controllers"].frame]),
                                  *stroke_flash([c.box for c in md.parts["kubelet"]]),
                                  lag_ratio=0.25), run_time=1.4)
            md.heal(self)
            vo.wait_until("Four lamps on this picture")
            lamps = [lamp_glyph().move_to(p) for p in lamp_points(md)]
            md.show(self, *lamps, anims=[LaggedStart(*[GrowFromCenter(lp) for lp in lamps], lag_ratio=0.3)],
                    run_time=1.0)
            vo.wait_until("each with a symptom you will meet")
            self.play(*[Indicate(lp, color=TURN, scale_factor=1.3) for lp in lamps], run_time=0.8)
            md.heal(self)
            md.drop(self, *lamps, run_time=0.5)
        self.play(FadeOut(md), run_time=0.6)
        self.remove(md)
        self.wait(0.3)
