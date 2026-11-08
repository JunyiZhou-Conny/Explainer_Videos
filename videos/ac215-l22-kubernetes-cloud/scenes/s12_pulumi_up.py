"""S12 · pulumi up: what builds, in what order (AC215 L22, the full follow-along). TRACKER [C] 4
throughout (· extra while c21 is on screen). Lecture: 22 · 24–25 (beats 2 and 6).

Beats (script.md "## S12", one voiceover block each):
0. TRACKER [C] 4. A 13-row 20 pt toolbox terminal at …:/app/deploy_k8s#. `pulumi up --stack dev
   --refresh -y` -> TERM(b33: 2 wrap) RED. TRACKER [C] 4 · extra: the same again (extra, local; 'extra'
   beside it, the GREY tags 'placeholder image tags · nothing built' and the README's default tag
   above the terminal) -> TERM(c21: 45, 47, 55, 58, 165 wrap, 166 crop 'account not found"}' wrap);
   line 58 RED, 'ac215-project' in line 165 ringed GREY; on "the very first resource" line 55 / 58
   flash; on "invalid grant" 'invalid_grant' turns RED.
1. The terminal shrinks to a 3-row strip (c21:58's first row and c21:166); the placeholder tag sits
   above it. A GREY two-row chip "the first resource that needs Google · from here: a picture, not a
   recording" with an arrow to line 58. On "Pause and start yours" a YELLOW '▶ your turn' and the
   GOLD cost tag 'the meter starts'; on "the meter runs" the cost tag flashes.
2. LECTURE 22 · 24–25 + the GREY 'illustration' tag (top centre). V6 ResourceTree: the seven empty
   groups appear in dependency order; the network card opens, cheese-app-vpc and cheese-app-subnet
   fill; "side by side": router and NAT fill while the cluster group pulses; the network group fills;
   the cluster card opens, cheese-app-cluster fills; "the long wait": the GOLD-ringed clock
   '15–25 min · our estimate'; its hand turns again on "a quarter of an hour".
3. The clock leaves; the cluster card opens, cheese-app-pool fills; the cluster group fills and two
   small BLUE node boxes sit under it. A GREY card "kubeconfig, built from the cluster's outputs"
   rides from the cluster group into the PURPLE provider group, which fills. CODE(create_cluster.py:
   134–138) at the bottom, line 137 YELLOW ('depends_on=[node_pool]'); on "so no Pod" the cluster →
   provider arrow and the node boxes flash YELLOW.
4. The panel leaves. identity: cheese-app-namespace, api-ksa (GREEN), api-gsa-wi-user (BLUE) fill in
   its card, the group fills; storage: both PVCs; app: frontend, frontend-service, vector-db,
   vector-db-service fill in its card.
5. The app card closes. V4's Job cousin under the tree: the GREEN Job card 'vector-db-loader' with
   the dashed 'api' card; its Pod runs and turns 'Completed' GREY; the YELLOW hourglass 'Pulumi waits
   for Complete' between them; CODE(setup_containers.py: 319–321) at the bottom, line 320 YELLOW; the
   api card turns solid and the app group fills.
6. LECTURE (held, shown again). The Job and the panel leave. The ingress card opens, nginx-f5 fills.
   A V1 inset under the tree (this block only): the cluster outline with the nginx Service
   ('type: LoadBalancer', PINK) and the controllers box with its lamp; the lamp lights GREEN, the
   controllers → 'cloud provider API' arrow grows GREEN ('red on the stand-in' under it); a BLUE door
   '<IP>' comes back to the cluster's edge and '<IP>.sslip.io' writes PINK; cheese-app-ingress fills
   last; the ingress group fills. Everything but the tracker fades.
7. Identity 1: PURPLE chips 'pulumi' / 'kubectl' → a GREY kubeconfig card (create_cluster.py:107–110 as
   YAML; 'command: gke-gcloud-auth-plugin' PURPLE, chip 'fix 2 from S04') → BLUE 'API server'; a
   YELLOW dot rides the path. Below, a GREY-dashed stand-in card from TERM(k65: 4, 6–7) with the tag
   'stand-in: kind, not GKE'; on "no cluster password" its certificate line flashes.
8. Identity 2: inside a BLUE dashed 'cheese-app-cluster' outline, the TEAL API Pod with a GREEN
   'api-ksa' badge; at the edge, a BLUE door 'Vertex AI'. The badge rides to the edge and becomes a
   GREEN key 'gcp-service' ('Workload Identity'), which goes on to Vertex AI. GREY chip 'no JSON key
   inside the cluster'.
9. CODE(create_cluster.py: 192–198), lines 195–197 YELLOW; GREY chip 'runs once, at create, inside
   this toolbox · docker-shell.sh runs it with --rm'; the TEAL toolbox with its kubeconfig fades
   (dashed) and 'next session: no kubeconfig (S14)' appears. After the narration: the GREY 'if yours
   stops' card, its four lines flashing in turn, and the GREEN chip 'success: Outputs with app_url
   (S14)'. Fade; empty frame.

Deviations from SHOW:
- The terminal is 20 pt (72 characters a row), as in S11; c21:165 wraps to 4 rows, :166 to 2. The
  README's 'ac215-project' in c21:165 is ringed and carries the default tag (script conventions,
  Masking), which the S12 SHOW line does not list.
- Beat 1: '▶ your turn' and the cost tag stand under the GREY chip: the command has scrolled away.
- Beat 2: the cluster card opens after the network card closes (one card at a time); 'side by side' is
  shown by the cluster group pulsing while router and NAT fill.
- Beat 3: the kubeconfig card fades into the provider group as it fills (no scaling of text).
- Beat 5: the Job cousin sits under the tree (the tree's own app card cannot be open at the same time);
  the hourglass is between the Job and the cousin's 'api' card, and the app group fills at the end.
  JobCousin (below) moves the hourglass caption left and up: in common.py it touches the api card.
- Beat 6: the 'small V1 inset' is drawn here with V1's names (cluster outline, Service, controllers
  lamp, cloud provider API) at full text size: MasterDiagram is 12.9 units wide and text may never be
  scaled down. The lecture tag is shown again for this block (script: 'LECTURE (held)').
- Beat 7: the GKE kubeconfig is a card of create_cluster.py:107–110 (the dict that yaml.dump writes),
  with its source in the header.
- Tree12 (below): the app card opens below its box, the network card hugs the left edge, and the GOLD
  clock sits beside a two-row caption under the cluster box (common.py's corner clock covers '×2').
  Beat 6 closes the ingress card while the V1 inset plays and reopens it for cheese-app-ingress, so
  the filled app group is not hidden for 14 s.
- Boxes are flashed by their words plus an outline pulse (pulse/box_flash): Indicate on a whole
  opaque box floods its fill and hides its words.
- Beat 9: the 'if yours stops' card and the success chip come after the narration ends (about 7 s,
  each line flashing in turn), since the SAY line is short.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S12"]
assert len(SAY) == SAY_COUNT["S12"] == 10

# ------------------------------------------------------------------ the real sources (checked)
B33, C21, K65 = capture("b33"), capture("c21"), capture("kind/k65")
TOKEN_ERR = "error: PULUMI_ACCESS_TOKEN must be set for login during non-interactive CLI sessions"
assert B33.cmd == readme(454)
assert B33.cmd == "pulumi up --stack dev --refresh -y" and B33.line(2) == TOKEN_ERR
assert C21.cmd == B33.cmd
assert C21.line(45).strip() == "+ 23 to create" and C21.line(47) == "Updating (dev):"
assert C21.line(55).strip() == "+  gcp:compute:Network cheese-app-vpc creating (0s)"
assert "**creating failed**" in C21.line(58) and "cheese-app-vpc" in C21.line(58)
assert "Error creating Network" in C21.line(165) and PROJECT_README in C21.line(165)
L166 = C21.crop(166, 'account not found"}')
assert L166.strip() == 'Response: {"error":"invalid_grant","error_description":"Invalid grant: account not found"}'
K65_LINES = K65.at(4, (6, 7))
assert K65_LINES[0].strip() == "server: https://test-cluster-control-plane:6443"
assert K65_LINES[2].strip() == "client-certificate-data: <redacted>"

CC = "src/deployment/deploy_k8s/create_cluster.py"
SC = "src/deployment/deploy_k8s/setup_containers.py"
assert '"gke_k8s_v2"' in excerpt(CC, 135, 135)
assert "depends_on=[node_pool]" in excerpt(CC, 137, 137)
assert '"exec": {' in excerpt(CC, 108, 108) and '"command": "gke-gcloud-auth-plugin"' in excerpt(CC, 110, 110)
assert '"user": {' in excerpt(CC, 107, 107)
assert "depends_on=[vector_db_loader_job]" in excerpt(SC, 320, 320)
assert '"connect-k8s-command"' in excerpt(CC, 193, 193)
assert "get-credentials" in excerpt(CC, 195, 195) and "--zone {region}" in excerpt(CC, 197, 197)

P_K8S = toolbox_prompt("/app/deploy_k8s")
SIZE = 20
GROUP_ORDER = ("network", "cluster", "provider", "identity", "storage", "app", "ingress")


def tb(rows: int) -> Terminal:
    """The 20 pt toolbox terminal (72 characters a row), bottom edge at BOTTOM."""
    return term(P_K8S, rows, T_TOOLBOX, size=SIZE)


def span_bar(code_, k0: int, k1: int, color, opacity: float = 0.2):
    """ONE translucent bar over code lines k0..k1 (0-based)."""
    a, b = line_bar(code_, k0, color, opacity), line_bar(code_, k1, color, opacity)
    top, bot = a.get_top()[1], b.get_bottom()[1]
    return Rectangle(width=a.width, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([a.get_x(), (top + bot) / 2, 0])


def bars_behind(panel, bars, z: int = 1):
    """Draw translucent line bars under a code panel's text (z-order), not over it."""
    panel.code.code_lines.set_z_index(z + 1)
    for b in bars:
        b.set_z_index(z)


def ind(s: str, color=INK, size: float = SIZE, parts=None) -> VGroup:
    """A mono row that keeps its leading spaces (Text drops them): an invisible anchor at the row's
    left, the text shifted right by the indent. parts: [(text, colour), …] instead of s."""
    cw = mono("x" * 20, size).width / 20
    n = len(s) - len(s.lstrip(" ")) if s else 0
    parts = parts or [(s.strip(), color)]
    txt = VGroup(*[mono(x, size, c) for x, c in parts]).arrange(RIGHT, buff=cw)
    anchor = Dot(radius=0.001).set_opacity(0)
    txt.next_to(anchor, RIGHT, buff=n * cw)
    return VGroup(anchor, txt)


class JobCousin(ControllerLoop):
    """V4's Job cousin with the hourglass caption moved left and up: in common.py it touches the
    dashed api card's top-left corner (requested as a shared fix)."""

    def hourglass(self, scene):
        h = hourglass(0.55).move_to(self.p(1.3, 0.0))
        t = label("Pulumi waits for Complete", 20, TURN).next_to(h, UP, buff=0.25).shift(LEFT * 0.75)
        assert t.get_right()[0] < self.api_card.get_left()[0] - 0.1
        self.glass = VGroup(h, t)
        self.show(scene, self.glass, run_time=0.5)
        scene.play(Rotate(h, PI), run_time=0.6)
        self.heal(scene)


def pulse(fb, color, width: float = 7):
    """ANIM: pulse a frame_box's outline (Indicate on a whole box floods its fill and hides its words)."""
    return fb.edge.animate(rate_func=there_and_back).set_stroke(color, width=width)


def box_flash(b, color, scale: float = 1.08):
    """ANIMS for a boxed(): its words flash and its outline pulses."""
    return [Indicate(b.text, color=color, scale_factor=scale), pulse(b.frame, color)]


class Tree12(ResourceTree):
    """V6 with two S12 layout tweaks (requested as shared fixes):
    - cards: the network card hugs the left safe edge (it would cover more of 'identity'); the 7-member
      app card opens BELOW its box (common.py pushes it up over 'ingress'; nothing is under the tree
      while it is open in S12);
    - clock: the GOLD ring sits beside a two-row caption under the cluster box, left of the provider →
      identity arrow (common.py puts it on the box's corner, over its '×2')."""

    def _card(self, key):
        c = super()._card(key)
        g = self.groups[key]
        if key == "network":
            c.shift(LEFT * (c.get_left()[0] + 6.55))
        elif key == "app":
            c.next_to(g.box, DOWN, buff=0.08).align_to(g.box, LEFT)
            keep_inside(c)
            assert c.get_top()[1] < self.groups["storage"].box.get_bottom()[1] or \
                c.get_left()[0] > self.groups["storage"].box.get_right()[0]
        return c

    def clock(self, scene):
        g = self.groups["cluster"]
        c = clock_face(0.2, COST, hour=4)
        rg = Circle(radius=0.27, stroke_color=COST, stroke_width=3)
        t = VGroup(label("15–25 min", 20, COST), label("our estimate", 20, COST)).arrange(DOWN, aligned_edge=LEFT,
                                                                                        buff=0.06)
        row = VGroup(rg, t).arrange(RIGHT, buff=0.14)
        row.next_to(g.box, DOWN, buff=0.08)
        row.shift(RIGHT * (-1.35 - row.get_right()[0]))
        c.move_to(rg)
        assert row.get_left()[0] > self.groups["network"].box.get_right()[0] + 0.05 and row.get_bottom()[1] > self.groups["identity"].box.get_top()[1] + 0.05, \
            (row.get_right(), row.get_bottom())
        self.clock_g = VGroup(rg, c, t)
        self.show(scene, self.clock_g, run_time=0.5)
        scene.play(Rotate(c.hands[1], -TAU, about_point=c[0].get_center()), run_time=1.0)
        self.heal(scene)


def row_with(rows, s: str):
    """The first printed row whose text contains s."""
    return next(r for r in rows if s in r.text)


class PulumiUp(VoiceScene):
    def construct(self):
        # ========================================================== 0. pulumi up: README, then local
        trk = tracker_c(4)
        t = tb(13)
        ph, dft = placeholder_tag(), default_tag()
        ph.next_to(t.box, UP, buff=0.12).align_to(t.box, LEFT)
        under_term(t, dft)
        assert ph.get_right()[0] < dft.get_left()[0] - 0.1
        assert dft.get_top()[1] < TRACK_BOTTOM - 0.05, dft.get_top()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("pulumi up, stack dev")
            type_capture(self, t, B33, type_time=0.6)
            e33 = out(self, t, [(B33.line(2), ERR)], wrap=True, run_time=0.3)
            self.play(Indicate(substring(e33[0], "PULUMI_ACCESS_TOKEN"), color=ERR, scale_factor=1.1), run_time=0.5)
            self.add(t)
            vo.wait_until("On the local backend")
            self.play(track(trk, 4, True), run_time=0.3)
            r21 = type_capture(self, t, C21, type_time=0.5)[0]
            xr = extra_row()
            on_bar(t, xr)
            self.play(FadeIn(xr), FadeIn(ph, shift=DOWN * 0.1), run_time=0.3)
            vo.wait_until("the update starts")
            g1 = out(self, t, [C21.line(45), C21.line(47), C21.line(55)], run_time=0.4)
            r55 = g1[-1]
            vo.wait_until("and the very first resource")
            g2 = out(self, t, [(C21.line(58), ERR)], wrap=True, run_time=0.3)
            r58 = g2[0]
            self.play(Indicate(substring(r55, "cheese-app-vpc"), color=CLOUD, scale_factor=1.12),
                      Indicate(substring(r58, "**creating failed**"), color=ERR, scale_factor=1.1), run_time=0.7)
            self.add(t)
            g3 = out(self, t, [C21.line(165), L166], wrap=True, run_time=0.5)
            r_proj = row_with(g3, PROJECT_README)
            rg = ring(substring(r_proj, PROJECT_README), S.GREY, buff=0.04, stroke=2.5)
            self.play(Create(rg), FadeIn(dft, shift=DOWN * 0.1), run_time=0.4)
            attach(self, r_proj, rg)
            r_grant = row_with(g3, "invalid_grant")
            r_found = g3[-1]
            vo.wait_until("invalid grant")
            ig = substring(r_grant, "invalid_grant")
            self.play(ig.animate.set_color(ERR), substring(r_found, "account not found").animate.set_color(ERR),
                      run_time=0.3)
            self.play(Indicate(ig, color=ERR, scale_factor=1.12), run_time=0.7)
            self.add(t)

        # ========================================================== 1. from here: a picture
        why = two_row_chip("the first resource that needs Google", "from here: a picture, not a recording", S.GREY)
        yt, cost = your_turn(), cost_tag("the meter starts")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(dft), FadeOut(xr), run_time=0.3)
            self.remove(dft, xr)
            keep = [g2[0], g3[-2], g3[-1]]
            resize(self, t, 3, keep=keep, run_time=0.6)
            on_bar(t, xr)
            self.play(ph.animate.next_to(t.box, UP, buff=0.12).align_to(t.box, LEFT), FadeIn(xr), run_time=0.4)
            why.move_to([0.6, 0.9, 0])
            ar = arrow(why.get_bottom() + DOWN * 0.05, substring(r58, "**creating failed**").get_top() + UP * 0.1,
                       ERR, stroke=3, buff=0)
            vo.wait_until("The network is the first thing")
            self.play(FadeIn(why, shift=DOWN * 0.15), run_time=0.5)
            self.play(GrowArrow(ar), run_time=0.4)
            vo.wait_until("so from here on")
            flash_tag(self, why, INK, 1.04)
            VGroup(yt, cost).arrange(RIGHT, buff=0.5).next_to(why, UP, buff=0.4)
            assert VGroup(yt, cost).get_top()[1] < TRACK_BOTTOM - 0.05
            vo.wait_until("Pause and start yours")
            self.play(FadeIn(yt, shift=RIGHT * 0.15), run_time=0.4)
            flash_tag(self, yt, TURN)
            vo.wait_until("from now on, the meter runs")
            self.play(FadeIn(cost, shift=RIGHT * 0.15), run_time=0.4)
            flash_tag(self, cost, COST)
        self.play(FadeOut(VGroup(t, xr, ph, why, ar, yt, cost)), track(trk, 4), run_time=0.5)
        self.remove(t, xr, ph, why, ar, yt, cost)

        # ========================================================== 2. network, then router/NAT and the cluster
        rt = Tree12()
        ref = lref("24–25")
        ill = illustration_tag().move_to([0.65, 3.2, 0])
        assert ill.get_left()[0] > trk.get_right()[0] + 0.2 and ill.get_right()[0] < ref.get_left()[0] - 0.2
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(ref), FadeIn(ill), run_time=0.4)
            for k in GROUP_ORDER:
                rt.group(self, k, run_time=0.22)
            vo.wait_until("First the network")
            rt.expand(self, "network", run_time=0.4)
            rt.fill_member(self, "network", "cheese-app-vpc")
            vo.wait_until("and its subnet")
            rt.fill_member(self, "network", "cheese-app-subnet")
            vo.wait_until("Then, side by side")
            self.play(pulse(rt.groups["cluster"].box, CLOUD), Indicate(rt.groups["cluster"].text, color=CLOUD),
                      run_time=0.8)
            rt.heal(self)
            vo.wait_until("the router with its NAT gateway")
            rt.fill_member(self, "network", "cheese-app-router")
            rt.fill_member(self, "network", "cheese-app-nat")
            vo.wait_until("and the cluster, the long wait")
            rt.collapse(self)
            rt.fill(self, "network")
            rt.expand(self, "cluster", run_time=0.35)
            rt.fill_member(self, "cluster", "cheese-app-cluster")
            rt.collapse(self)
            rt.clock(self)
            vo.wait_until("a quarter of an hour")
            hand = rt.clock_g[1].hands[1]
            self.play(Rotate(hand, -TAU, about_point=rt.clock_g[1][0].get_center()),
                      Indicate(rt.clock_g[2], color=COST, scale_factor=1.06), run_time=1.2)
            rt.heal(self)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 3. node pool; the provider waits for it
        cp = code(CC, 134, 138, font_size=SIZE, dedent=True,
                  cuts={136: "cluster_kubeconfig,", 137: "depends_on=[node_pool]),"})
        cp.move_to([0, 0, 0]).align_to([0, BOTTOM, 0], DOWN)
        b137 = line_bar(cp.code, 3, TURN, 0.22)
        bars_behind(cp, [b137])
        dep = code_span(cp.code, 3, "depends_on=[node_pool]")
        with self.voiceover(SAY[3]) as vo:
            rt.drop(self, rt.clock_g, run_time=0.3)
            rt.expand(self, "cluster", run_time=0.35)
            rt.fill_member(self, "cluster", "cheese-app-pool")
            rt.collapse(self)
            rt.fill(self, "cluster")
            cb = rt.groups["cluster"].box
            nodes = VGroup(*[frame_box(0.5, 0.32, NODE, k=0.45) for _ in range(2)]).arrange(RIGHT, buff=0.15)
            nodes.next_to(cb, DOWN, buff=0.12)
            self.play(LaggedStart(*[GrowFromCenter(n) for n in nodes], lag_ratio=0.4), run_time=0.5)
            vo.wait_until("A Kubernetes provider")
            kc = card(["kubeconfig, built from the cluster's outputs"], S.GREY, size=20)
            kc.move_to([0.0, -0.4, 0])
            self.play(FadeIn(kc, shift=UP * 0.2), pulse(cb, CLOUD), run_time=0.6)
            rt.heal(self)
            pv = rt.groups["provider"].box
            self.play(kc.animate.move_to(pv.get_center() + DOWN * 0.05).set_opacity(0), run_time=0.9)
            self.remove(kc)
            rt.fill(self, "provider")
            vo.wait_until("waits for that pool")
            self.play(FadeIn(cp, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(b137), dep.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(dep, color=TURN, scale_factor=1.08), run_time=0.6)
            vo.wait_until("so no Pod is created")
            edge = rt.arrows[("cluster", "provider")]
            self.play(Indicate(edge, color=TURN, scale_factor=1.3), Indicate(nodes, color=TURN, scale_factor=1.15),
                      run_time=0.9)
            rt.heal(self)

        # ========================================================== 4. identity, storage, frontend, vector db
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(cp, b137)), run_time=0.4)
            self.remove(cp, b137)
            vo.wait_until("Through it come the namespace")
            rt.expand(self, "identity", run_time=0.35)
            rt.fill_member(self, "identity", "cheese-app-namespace")
            vo.wait_until("the service account of the API")
            rt.fill_member(self, "identity", "api-ksa")
            vo.wait_until("and its binding")
            rt.fill_member(self, "identity", "api-gsa-wi-user", color=CLOUD)
            rt.collapse(self)
            rt.fill(self, "identity")
            vo.wait_until("the two disk claims")
            rt.expand(self, "storage", run_time=0.35)
            rt.fill_member(self, "storage", "persistent-pvc")
            rt.fill_member(self, "storage", "chromadb-pvc")
            rt.collapse(self)
            rt.fill(self, "storage")
            vo.wait_until("the frontend and the vector database")
            rt.expand(self, "app", run_time=0.35)
            for m in ("frontend", "frontend-service"):
                rt.fill_member(self, "app", m, run_time=0.3)
            for m in ("vector-db", "vector-db-service"):
                rt.fill_member(self, "app", m, run_time=0.3)

        # ========================================================== 5. the loader Job, then the API
        job = JobCousin(job=True, name="vector-db-loader", api=True)
        job.shift(DOWN * 0.95)
        sp = code(SC, 319, 321, font_size=SIZE)
        sp.move_to([0, 0, 0]).align_to([0, -3.55, 0], DOWN)
        b320 = line_bar(sp.code, 1, TURN, 0.22)
        bars_behind(sp, [b320])
        dvl = code_span(sp.code, 1, "depends_on=[vector_db_loader_job]")
        with self.voiceover(SAY[5]) as vo:
            rt.collapse(self)
            vo.wait_until("Next, the loader Job")
            job.job_card(self)
            assert job.get_top()[1] < rt.groups["identity"].box.get_bottom()[1] - 0.1, job.get_top()
            job.run_job(self)
            vo.wait_until("Pulumi creates the API only after")
            job.hourglass(self)
            vo.wait_until("the Job completes")
            self.play(Indicate(job.jpod.status, color=INK, scale_factor=1.15),
                      *box_flash(job.api_card, OWN), run_time=0.8)
            job.heal(self)
            vo.wait_until("lines 319 to 321")
            self.play(FadeIn(sp, shift=UP * 0.15), run_time=0.4)
            assert sp.get_top()[1] < job.get_bottom()[1] - 0.02, (sp.get_top(), job.get_bottom())
            self.play(FadeIn(b320), dvl.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(dvl, color=TURN, scale_factor=1.06), run_time=0.6)
            job.release(self)
            rt.fill(self, "app")

        # ========================================================== 6. nginx, the load balancer, the Ingress last
        ref = lref("24–25")
        inset, parts = self._inset()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(sp, b320)), FadeOut(job), FadeIn(ref), run_time=0.4)
            self.remove(sp, b320, job)
            vo.wait_until("In parallel, Helm installs")
            rt.expand(self, "ingress", run_time=0.35)
            rt.fill_member(self, "ingress", "nginx-f5")
            vo.wait_until("Its Service asks for a load balancer")
            rt.collapse(self)
            self.play(FadeIn(parts["outline"]), FadeIn(parts["svc"], shift=UP * 0.1),
                      FadeIn(parts["ctl"], shift=UP * 0.1), run_time=0.6)
            self.play(GrowArrow(parts["ask"]), run_time=0.4)
            vo.wait_until("so the controllers ask the cloud")
            self.play(FadeIn(parts["api"], shift=LEFT * 0.15), run_time=0.4)
            self.play(Transform(parts["lamp"], parts["lamp_on"]), GrowArrow(parts["cloud_arrow"]), run_time=0.6)
            vo.wait_until("the part 1 lamp")
            self.play(FadeIn(parts["note"], shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(parts["lamp"], color=OWN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("That address becomes a host name")
            self.play(GrowArrow(parts["back"]), run_time=0.4)
            self.play(FadeIn(parts["door"], shift=LEFT * 0.3), run_time=0.4)
            self.play(Write(parts["host"]), run_time=0.6)
            vo.wait_until("and the Ingress comes last")
            rt.expand(self, "ingress", run_time=0.3)
            rt.fill_member(self, "ingress", "cheese-app-ingress")
            rt.collapse(self)
            rt.fill(self, "ingress")
            self.play(pulse(rt.groups["ingress"].box, OWN), Indicate(rt.groups["ingress"].text, color=OWN), run_time=0.6)
            rt.heal(self)
        self.play(FadeOut(VGroup(rt, nodes, inset, ref, ill)), run_time=0.6)
        self.remove(rt, nodes, inset, ref, ill)

        # ========================================================== 7. identity 1: the auth plugin
        chips = VGroup(tool_chip("pulumi"), tool_chip("kubectl")).arrange(DOWN, buff=0.25)
        chips.move_to([-5.4, 1.2, 0])
        rows = [ind("user:"), ind("  exec:"),
                ind("    x", parts=[("command:", INK), ("gke-gcloud-auth-plugin", TOOL)])]
        kcard = card(rows, S.GREY, size=SIZE, head="kubeconfig · create_cluster.py:107–110", buff=0.1)
        kcard.move_to([-0.6, 1.2, 0])
        api = boxed(["API server"], CLOUD, size=22).move_to([5.2, 1.2, 0])
        a1 = arrow(chips.get_right() + RIGHT * 0.05, kcard.get_left() + LEFT * 0.05, TOOL, buff=0)
        a2 = arrow(kcard.get_right() + RIGHT * 0.05, api.get_left() + LEFT * 0.05, TOOL, buff=0)
        fix = scene_chip("fix 2 from S04").next_to(kcard, DOWN, buff=0.15).align_to(kcard, RIGHT)
        st_rows = [ind(s.rstrip(), S.GREY) for s in K65_LINES]
        scard = card(st_rows, S.GREY, size=SIZE, dashed=True, head="the stand-in's kubeconfig · k65", buff=0.1)
        scard.move_to([-0.6, -1.65, 0])
        stag = standin_tag().next_to(scard, DOWN, buff=0.15).align_to(scard, RIGHT)
        assert stag.get_bottom()[1] > -3.55 and fix.get_bottom()[1] > scard.get_top()[1] + 0.1, \
            (stag.get_bottom(), fix.get_bottom(), scard.get_top())
        assert chips.get_right()[0] < kcard.get_left()[0] - 0.3 and kcard.get_right()[0] < api.get_left()[0] - 0.3
        with self.voiceover(SAY[7]) as vo:
            vo.wait_until("Identity, in two parts")
            self.play(FadeIn(chips, shift=RIGHT * 0.2), FadeIn(api, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("Pulumi and kubectl reach the API server")
            self.play(FadeIn(kcard, shift=UP * 0.15), GrowArrow(a1), run_time=0.5)
            self.play(GrowArrow(a2), run_time=0.4)
            dot = pulse_dot(TURN, 0.1).move_to(a1.get_start())
            path = VMobject().set_points_as_corners([a1.get_start(), kcard.get_left(), kcard.get_right(), a2.get_end()])
            self.play(FadeIn(dot), run_time=0.15)
            self.play(travel(dot, path, run_time=1.2))
            self.play(FadeOut(dot), *box_flash(api, CLOUD), run_time=0.5)
            self.remove(dot)
            vo.wait_until("through the GKE auth plugin")
            plug = rows[2][1][1]
            self.play(Indicate(plug, color=TOOL, scale_factor=1.1), run_time=0.7)
            vo.wait_until("fix two from the toolbox")
            self.play(FadeIn(fix, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("so there is no cluster password")
            self.play(FadeIn(scard, shift=UP * 0.15), FadeIn(stag), run_time=0.5)
            self.play(Indicate(st_rows[2], color=INK, scale_factor=1.06), run_time=0.7)
        self.play(FadeOut(VGroup(chips, kcard, api, a1, a2, fix, scard, stag)), run_time=0.5)
        self.remove(chips, kcard, api, a1, a2, fix, scard, stag)

        # ========================================================== 8. identity 2: Workload Identity
        cl = outline_box(7.6, 4.0, CLOUD, solid=False).move_to([-2.5, 0.55, 0])
        cl_t = mono("cheese-app-cluster", SIZE, CLOUD).next_to(cl, UP, buff=0.0).align_to(cl, LEFT).shift(
            DOWN * 0.42 + RIGHT * 0.25)
        pod = pod_glyph(None, None, r=0.42)
        pod.move_to([-4.6, 0.55, 0])
        pod_l = label("api Pod", SIZE, INK).next_to(pod, DOWN, buff=0.15)
        badge = chip("api-ksa", OWN, size=SIZE, font=MONO).next_to(pod, RIGHT, buff=0.25)
        vtx = boxed(["Vertex AI"], CLOUD, size=22).move_to([5.25, 0.55, 0])
        edge_x = cl.get_right()[0]
        door_ = Rectangle(width=0.16, height=1.0, stroke_width=0).set_fill(CLOUD, 0.85).move_to([edge_x, 0.55, 0])
        key = key_icon("service", name="gcp-service")
        key.move_to([edge_x + 1.2, 0.55, 0])
        wi = label("Workload Identity", SIZE, OWN).next_to(key, UP, buff=0.3)
        wi.set_x(max(key.get_x(), edge_x + 0.3 + wi.width / 2))
        assert wi.get_right()[0] < vtx.get_left()[0] - 0.1
        nojson = grey_chip("no JSON key inside the cluster").move_to([-2.5, -2.15, 0])
        assert nojson.get_top()[1] < cl.get_bottom()[1] - 0.1
        assert key.get_right()[0] < vtx.get_left()[0] - 0.1, (key.get_right(), vtx.get_left())
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeIn(cl), FadeIn(cl_t), run_time=0.5)
            vo.wait_until("And the API Pod wears")
            self.play(GrowFromCenter(pod), FadeIn(pod_l), run_time=0.5)
            self.play(FadeIn(badge, shift=LEFT * 0.2), run_time=0.4)
            self.play(Indicate(badge, color=OWN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("which Workload Identity swaps")
            self.play(FadeIn(vtx, shift=LEFT * 0.2), FadeIn(door_), run_time=0.4)
            self.play(badge.animate.move_to([edge_x - badge.width / 2 - 0.15, 0.55, 0]), run_time=0.8)
            self.play(FadeIn(wi, shift=DOWN * 0.1), ReplacementTransform(badge, key), run_time=0.8)
            vo.wait_until("at the door to Vertex AI")
            self.play(*box_flash(vtx, CLOUD), Indicate(key, color=OWN, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("No JSON key sits in the cluster")
            self.play(FadeIn(nojson, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, nojson, INK, 1.04)
        self.play(FadeOut(VGroup(cl, cl_t, pod, pod_l, vtx, door_, key, wi, nojson)), run_time=0.5)
        self.remove(cl, cl_t, pod, pod_l, vtx, door_, key, wi, nojson)

        # ========================================================== 9. get-credentials runs once; if yours stops
        gp = code(CC, 192, 198, font_size=SIZE)
        gp.move_to([0, 0, 0]).align_to([-6.4, 0, 0], LEFT).align_to([0, 2.7, 0], UP)
        bg = span_bar(gp.code, 3, 5, TURN, 0.2)
        bars_behind(gp, [bg])
        once = two_row_chip("runs once, at create, inside this toolbox", "docker-shell.sh runs it with --rm", S.GREY)
        once.next_to(gp, DOWN, buff=0.3).align_to(gp, LEFT)
        box_ = crate("toolbox", 2.4, 0.7)
        kfile = file_card("kubeconfig")
        tbx = VGroup(box_, kfile).arrange(DOWN, buff=0.2).move_to([4.9, 1.3, 0])
        box_dash = crate("toolbox", 2.4, 0.7, dashed=True).move_to(box_)
        nxt = two_row_chip("next session:", "no kubeconfig (S14)", S.GREY).next_to(tbx, DOWN, buff=0.35)
        assert tbx.get_left()[0] > gp.get_right()[0] + 0.2, (tbx.get_left(), gp.get_right())
        assert once.get_bottom()[1] > -3.5
        with self.voiceover(SAY[9]) as vo:
            vo.wait_until("Pulumi connects kubectl once")
            self.play(FadeIn(gp, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(bg), run_time=0.3)
            self.play(FadeIn(tbx, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("inside this toolbox")
            self.play(FadeIn(once, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("which is removed when you exit")
            self.play(FadeOut(kfile, shift=DOWN * 0.2), FadeOut(box_), FadeIn(box_dash), run_time=0.7)
            self.remove(kfile, box_)
            vo.wait_until("The next session starts unconnected")
            self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, nxt, INK, 1.04)
        self.play(FadeOut(VGroup(gp, bg, once, box_dash, nxt)), run_time=0.5)
        self.remove(gp, bg, once, box_dash, nxt)

        stops = self._stops_card()
        ok = ok_chip("success: Outputs with app_url (S14)").next_to(stops, DOWN, buff=0.3)
        assert ok.get_bottom()[1] > -3.5 and stops.get_top()[1] < TRACK_BOTTOM - 0.05
        self.play(FadeIn(stops, shift=UP * 0.15), run_time=0.6)
        for item in stops.items:
            self.play(Indicate(item, color=TURN, scale_factor=1.04), run_time=0.9)
            self.wait(0.4)
        self.play(FadeIn(ok, shift=UP * 0.1), run_time=0.4)
        flash_tag(self, ok, OWN, 1.04)
        self.wait(1.0)
        self.play(FadeOut(VGroup(stops, ok, trk)), run_time=0.6)
        self.remove(stops, ok, trk)
        self.wait(0.3)

    # ------------------------------------------------------------------ pictures
    def _inset(self):
        """Beat 6's V1 inset under the tree (y -3.35 .. -0.35): the cluster outline with the nginx
        Service and the controllers (lamp), the cloud provider API, the door <IP> and its host name."""
        p = {}
        outline = outline_box(7.0, 2.85, CLOUD, solid=False).move_to([-2.85, -1.9, 0])
        o_t = mono(CLUSTER, SIZE, CLOUD).move_to(outline).align_to(outline, UL).shift(DOWN * 0.15 + RIGHT * 0.25)
        p["outline"] = VGroup(outline, o_t)
        svc = boxed(["nginx Service", "type: LoadBalancer"], ROUTE, size=SIZE).move_to([-4.6, -1.85, 0])
        p["svc"] = svc
        ctl = boxed(["controllers"], CLOUD, size=SIZE, k=0.08).move_to([-1.15, -1.85, 0])
        lp = lamp("off", 0.16).next_to(ctl, UP, buff=0.08).align_to(ctl, RIGHT)
        lp_on = lamp("green", 0.16).move_to(lp)
        p["ctl"] = VGroup(ctl, lp)
        p["lamp"], p["lamp_on"] = lp, lp_on
        p["ask"] = arrow(svc.get_right() + RIGHT * 0.05, ctl.get_left() + LEFT * 0.05, ROUTE, buff=0)
        api = boxed(["cloud provider", "API"], CLOUD, size=SIZE).move_to([3.9, -1.3, 0])
        p["api"] = api
        p["cloud_arrow"] = arrow(ctl.get_right() + RIGHT * 0.05, api.get_left() + LEFT * 0.05, OWN, stroke=4, buff=0)
        p["note"] = label("red on the stand-in", SIZE, S.GREY).next_to(ctl, DOWN, buff=0.18)
        dr = door(IP_PH, CLOUD).move_to([outline.get_right()[0], -2.85, 0])
        p["door"] = dr
        p["back"] = arrow(api.get_corner(DL) + np.array([0.3, -0.05, 0]), dr.get_top() + UP * 0.08, CLOUD, buff=0,
                          arc=-0.4)
        p["host"] = mono(HOST_PH, 22, ROUTE).next_to(dr, RIGHT, buff=0.3).align_to(dr, DOWN)
        g = VGroup(p["outline"], svc, p["ctl"], p["ask"], api, p["cloud_arrow"], p["note"], dr, p["back"], p["host"])
        assert g.get_bottom()[1] > -3.55 and g.get_right()[0] < 6.55, (g.get_bottom(), g.get_right())
        return g, p

    def _stops_card(self):
        """The GREY 'if yours stops' card: four lines (label font, commands in mono)."""
        def row(*parts):
            return VGroup(*[mono(s, SIZE, INK) if m else label(s, SIZE, INK) for s, m in parts]).arrange(RIGHT, buff=0.1)

        items = [
            VGroup(row(("403 at", False), ("api-gsa-wi-user", True), ("→ Service Account Admin (S10)", False))),
            VGroup(row(("stuck at", False), ("vector-db-loader", True), ("→ logs (S15), then", False)),
                   row(("kubectl delete job vector-db-loader -n cheese-app-namespace", True)),
                   row(("and up again", False))).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(row(("ImagePullBackOff →", False), ("kubectl describe pod … -n cheese-app-namespace", True)),
                   row(("repository missing, or images not built", False))).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
            VGroup(row(("quota → delete lecture 20's VM, request more", False))),
        ]
        c = card(items, S.GREY, size=SIZE, head="if yours stops", buff=0.22)
        c.move_to([0, 0.35, 0])
        c.items = items
        return c
