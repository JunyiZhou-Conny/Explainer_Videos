"""S05 · A test cluster and a first look (AC215 L22, the full follow-along). TRACKER [W] 5 (beats 0-2),
6 (beat 4), 7 (beats 5-8). Lecture: 22 · 32–33 (beat 0), 37 (beat 4), 34 (beat 5), 35 (beat 6).

Beats (script.md "## S05", one voiceover block each):
0. TRACKER [W] 5. LECTURE 22 · 32–33. An 8-row toolbox terminal ('laptop · toolbox', prompt from
   b03:77). `gcloud container clusters create test-cluster --num-nodes 2 --zone us-east1-c` typed
   (folds) -> TERM(b15: 2 wrap) RED ('no active account' flashes); a YELLOW '▶ your turn' beside the
   typed command; the GOLD cost tag 'test cluster · billed per node-hour while it exists' slides in
   above the terminal. The lecture tag fades with the block.
1. The terminal shrinks to a 3-row strip. Left: a GREY card 'yours' (no output panel) whose three
   lines arrive phrase by phrase: 'a short wait', 'a table with test-cluster', 'kubeconfig entry
   generated' (PINK). Right: a BLUE dashed 'test-cluster · us-east1-c' outline with a PINK arrow from
   the kubeconfig line ("where to go"); node 1 (slide 32: one node), node 2 (README: two), one TEAL
   Pod lands in each; the GREY chip 'slide 32: 1 node · README: 2 nodes' under them, the GOLD cost
   tag moves under the chip.
2. TRACKER [W] 5 · extra. A 13-row terminal 'laptop · stand-in' at student@laptop:~$, 'extra' and
   'stand-in: kind, not GKE' on its title bar. Line 1 of k01 typed (folds) -> TERM(k01: 2–7, 15, 17,
   19, 21, 23, 25, 27, 29, 30); lines 5–7 (control-plane, worker, worker) PURPLE; 'extra' flashes on
   "It is not in the README".
3. The terminal fades. V1 (MasterDiagram, built) returns; to_standin(): the outline becomes GREY
   dashed with the stand-in tag, the plane's caption becomes 'a container you can see' (flashes),
   worker 3 leaves; under it 'on GKE: run by Google, out of sight' while the plane's outline flashes.
4. TRACKER [W] 6. LECTURE 22 · 37. README card 'README.md · lines 545–549' top; a schematic console
   ('illustration') 'Kubernetes Engine › Clusters › test-cluster › Nodes › node › Pods' whose crumbs
   light one per phrase; then a second console 'Compute Engine › VM instances' with two BLUE rows
   'node VM'.
5. TRACKER [W] 7 · extra. LECTURE 22 · 34. A 13-row 20 pt terminal 'laptop · toolbox · stand-in'
   (stand-in tag on the bar). `kubectl version` (+ 'extra' beside it) -> TERM(k02: 2, 4) +
   'at the time of recording'; both version strings YELLOW and flash together.
6. TRACKER [W] 7. LECTURE 22 · 35. `kubectl get all` -> TERM(k03: 2–3, AGE column cropped);
   'service/kubernetes' ORANGE; GREY 'namespace: default' beside the command.
7. `kubectl get all --all-namespaces` -> TERM(k04: 2, 5, 9, 10, 14, …, 18–19, cropped after the NAME
   column); `kubectl get pods --all-namespaces` -> TERM(k05: 2–15, cropped after the NAME column);
   'kube-system' ORANGE. The other rows fade, the four control-plane rows stay (terminal 4 rows) and a
   small V1 thumbnail (the control plane's four boxes) appears above; each row's name turns BLUE with
   its box on its word; GREY chip 'on GKE: run by Google, not listed'.
8. The terminal grows to 12 rows. `kubectl get componentstatuses` -> TERM(k06: 2–6), line 2 ORANGE
   with the GREY chip 'deprecated since 1.19: expected'; the three 'Healthy' flash; `kubectl get
   nodes` -> TERM(k07: 2–5); the three 'Ready' flash; lines 4–5 GREEN; line 3 GREY with a ring on
   'control-plane' and the chip 'GKE: not listed'; '▶ your turn' beside the command. Fade; empty frame.

Deviations from SHOW:
- Beats 0/1: the cost tag stays with the drawn test cluster in beat 1 (the billable thing on screen);
  the cluster outline and the PINK arrow make "so kubectl knows where to go" visible.
- Beats 5-8 use a 20 pt terminal (72 characters a row: k07's rows are 67–68 characters).
  k03's rows are 73 characters: the AGE column is cropped. k04/k05 rows (106–130 characters) are
  cropped after the NAME column (k04:10 after 'pod/kube-controller-manager…'); k05's header (line 2)
  prints and scrolls away with the command as the 13 rows fill.
- Beat 7: the V1 thumbnail needs room, so after k05 prints the other rows fade and the four
  control-plane rows stay in a 4-row terminal under the thumbnail (a "filter" move).
- Beat 3: the stand-in switch is done in place by v1_standin() (here) instead of
  MasterDiagram.to_standin(): that one cross-fades a new OPAQUE cluster box onto the top of the piece
  (it hides the plane and the workers) and builds it from the layout's original coordinates (wrong
  after a shift). The caption under V1 is a plain label, not md.callout() (whose Indicate floods the
  plane's fill YELLOW for half a second). The controllers→cloud arrow keeps its PINK label (SHOW does
  not mention it; S03 is where it turns RED on the stand-in).
- Beat 4: the two console panels do not fit together with the README card; the Compute Engine panel
  replaces the Kubernetes Engine one at "In Compute Engine", and each README line lights YELLOW with
  its crumb.
- Beat 3 (critic pass): the stand-in tag sits bottom right inside the outline (top right it touched
  worker 0 and the PINK arrow label); the longer caption gets an opaque plate in the plane's fill so
  the controllers→cloud arrow passes behind it instead of striking through the words.
- Beat 0 (critic pass): '--num-nodes 2' and '--zone us-east1-c' flash YELLOW on their words.
- Beat 8: the two chips sit just above the terminal (the rows they describe are too long to hold
  them beside), each with its row highlighted at the same moment.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S05"]
assert len(SAY) == SAY_COUNT["S05"] == 9

# ------------------------------------------------------------------ the real sources (checked)
B15 = capture("b15")
K01, K02, K03, K04, K05, K06, K07 = (capture(k) for k in ("k01", "k02", "k03", "k04", "k05", "k06", "k07"))

assert B15.cmd == "gcloud container clusters create test-cluster --num-nodes 2 --zone us-east1-c"
assert B15.cmd == readme(541)
assert B15.line(2).startswith("ERROR: (gcloud.container.clusters.create) You do not currently have an active account")
assert K01.cmd.startswith("cat kind-test-cluster.yaml; kind create cluster --name test-cluster")
assert [K01.line(n).strip() for n in (5, 6, 7)] == ["- role: control-plane", "- role: worker", "- role: worker"]
assert K01.line(15) == 'Creating cluster "test-cluster" ...'
assert K01.line(30) == 'Set kubectl context to "kind-test-cluster"'
assert K02.cmd == "kubectl version" and K02.line(2).startswith("Client Version: v1.34.12-gke")
assert K02.line(4) == "Server Version: v1.34.11"
assert K03.cmd == readme(553) == "kubectl get all"
assert "service/kubernetes" in K03.line(3)
assert K04.cmd == readme(554) and K05.cmd == readme(555)
assert "pod/etcd-test-cluster-control-plane" in K04.line(5)
assert "pod/kube-apiserver-test-cluster-control-plane" in K04.line(9)
assert "pod/kube-controller-manager-test-cluster-control-plane" in K04.line(10)
assert "pod/kube-scheduler-test-cluster-control-plane" in K04.line(14)
assert K04.line(18).startswith("default       service/kubernetes")
assert K04.line(19).startswith("kube-system   service/kube-dns")
CP_NAMES = {5: "etcd-test-cluster-control-plane", 9: "kube-apiserver-test-cluster-control-plane",
            10: "kube-controller-manager-test-cluster-control-plane",
            14: "kube-scheduler-test-cluster-control-plane"}
for n, nm in CP_NAMES.items():
    assert K05.line(n).split()[1] == nm, (n, K05.line(n))
assert K06.cmd == readme(559) and K06.line(2).startswith("Warning: v1 ComponentStatus is deprecated")
assert [K06.line(n).split()[1] for n in (4, 5, 6)] == ["Healthy"] * 3
assert K07.cmd == readme(560)
assert "control-plane" in K07.line(3) and all(" Ready " in K07.line(n) for n in (3, 4, 5))
CONSOLE_README = readme_lines(545, 549)
assert CONSOLE_README.split("\n")[0].startswith("• Go to the Kubernetes Engine menu item"), CONSOLE_README


def name_crop(cap, n: int) -> str:
    """A kubectl row cropped after its NAME column (the second field). The second field is searched
    AFTER the first one, so the header 'NAMESPACE   NAME' is not cut inside 'NAMESPACE'."""
    s = cap.line(n)
    f = s.split()
    i = s.index(f[1], s.index(f[0]) + len(f[0])) + len(f[1])
    assert s[:i].split() == f[:2], (n, s[:i])
    return s[:i]


def edge_flash(m, color=TURN, width: float = 6):
    """ANIM: an outline flashes `color` and returns."""
    return m.animate(rate_func=there_and_back).set_stroke(color, width)


def bar_follow(t, tg, rows: int):
    """ANIM: a tag on terminal t's title bar moves with the bar when t is resized to `rows`."""
    top = BOTTOM + rows * t.pitch + 0.85
    return tg.animate.move_to([tg.get_x(), top - t.bar_h / 2, 0])


def v1_standin(scene, md, run_time: float = 1.0):
    """PLAYS: V1 (built for GKE) becomes the kind stand-in in place: the cluster outline turns GREY
    dashed with the stand-in tag as its title, the plane's caption becomes 'a container you can
    see', worker 3 leaves. (Done here rather than with md.to_standin(), which redraws the opaque
    cluster box on top of the plane and the workers.)"""
    cl = md.parts["cluster"]
    old_edge, old_title = cl.frame.edge, cl.title
    new = frame_box(cl.frame.fill.width, cl.frame.fill.height, STANDIN, k=0.03, dashed=True).move_to(cl.frame.fill)
    new_title = standin_tag()
    # bottom right, inside the outline, under the two remaining workers (top right it touches worker 0
    # and the PINK 'nodes, load-balancer IP' label)
    new_title.move_to(cl.frame.fill).align_to(cl.frame.fill, DR).shift(np.array([-0.15, 0.1, 0]))
    cl.frame.remove(old_edge)
    cl.remove(old_title)
    scene.add(old_edge, old_title)
    scene.play(FadeOut(old_edge), FadeOut(old_title), Create(new.edge), FadeIn(new_title),
               cl.frame.fill.animate.set_fill(tint(STANDIN, 0.03), 1), run_time=run_time * 0.6)
    scene.remove(old_edge, old_title, new.edge, new_title)
    cl.frame.add(new.edge)
    cl.frame.edge = new.edge
    cl.add(new_title)
    cl.title = new_title
    md.standin = True
    md.heal(scene)
    # the longer caption crosses the controllers→cloud arrow: an opaque plate in the plane's fill lets
    # the arrow pass behind it instead of striking through the words
    txt = label("a container you can see", 20, S.GREY).move_to(md.parts["plane_cap"])
    plate = SurroundingRectangle(txt, buff=0.03, stroke_width=0).set_fill(tint(CLOUD, 0.14), 1)
    cap = VGroup(plate, txt)
    cap.text = txt
    md.parts["plane_cap"] = md.swap(scene, md.parts["plane_cap"], cap, run_time=run_time * 0.4)
    gone = [md.nodes[2], md.parts["fan"][2]]
    if "kubelet" in md.parts and len(md.parts["kubelet"]) == 3:
        gone.append(md.parts["kubelet"][2])
    md.drop(scene, *gone, run_time=run_time * 0.4)
    md.n_workers = 2


class TestCluster(VoiceScene):
    def construct(self):
        # ========================================================== 0. Create Cluster: it stops at once
        trk = tracker_w(5)
        ref = lref("32–33")
        t = toolbox_term(8)
        assert t.box.get_top()[1] < TRACK_BOTTOM - 0.1
        cost = cost_tag("test cluster · billed per node-hour while it exists")
        under_term(t, cost)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("gcloud container clusters create")
            cmd = type_capture(self, t, B15, type_time=1.4)[0]
            row2 = cmd.rows[-1]
            vo.wait_until("two nodes")
            self.play(Indicate(substring(row2, "--num-nodes 2"), color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("zone us east 1 c")
            self.play(Indicate(substring(row2, "--zone us-east1-c"), color=TURN, scale_factor=1.1), run_time=0.7)
            self.add(t)
            vo.wait_until("Ours stops at once")
            e = out(self, t, [(B15.line(2), ERR)], wrap=True, run_time=0.5)
            self.play(Indicate(substring(e[-1], "active account"), color=ERR, scale_factor=1.1), run_time=0.7)
            self.add(t)
            vo.wait_until("Pause and run yours")
            yt = turn_row()
            pin(self, cmd, beside(yt, cmd))
            flash_tag(self, yt, TURN)
            vo.wait_until("it costs money")
            self.play(FadeIn(cost, shift=LEFT * 0.4), run_time=0.6)
            flash_tag(self, cost, COST)
        self.play(FadeOut(ref), run_time=0.4)
        self.remove(ref)

        # ========================================================== 1. what yours does; one node vs two
        items = [label("a short wait", 22, INK),
                 VGroup(label("a table with", 22, INK), mono(TEST_CLUSTER, 22, INK)).arrange(RIGHT, buff=0.15),
                 label("kubeconfig entry generated", 22, ROUTE)]
        yours = card(items, head="yours · not captured here")
        yours.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, 2.6, 0], UP)
        for it in items:
            it.set_opacity(0)
        cl = frame_box(5.9, 2.45, CLOUD, k=0.04, dashed=True).move_to([3.45, 1.35, 0])
        cl_t = mono(f"{TEST_CLUSTER} · {ZONE_TEST}", 20, CLOUD)
        cl_t.move_to(cl).align_to(cl, UL).shift(np.array([0.18, -0.1, 0]))
        nodes = [node_box("node (VM)", 2.55, 1.45).move_to([x, 0.95, 0]) for x in (1.95, 4.95)]
        pods = [pod_glyph(r=0.24).move_to(nb.frame.get_center() + DOWN * 0.15) for nb in nodes]
        cmp_ = grey_chip("slide 32: 1 node · README: 2 nodes")
        cmp_.move_to([3.45, -0.3, 0])
        k_ar = arrow(items[2].get_right() + RIGHT * 0.1, cl.get_left() + DOWN * 0.3, ROUTE, stroke=4)
        assert yours.get_right()[0] < cl.get_left()[0] - 0.4, yours.get_right()
        with self.voiceover(SAY[1]) as vo:
            unpin(self, cmd, yt)
            resize(self, t, 3, keep=3, extra=[cost.animate.move_to([6.45 - cost.width / 2, -0.95, 0])],
                   run_time=0.6)
            self.play(FadeIn(yours.frame), FadeIn(yours.head), run_time=0.4)
            self.add(yours)
            vo.wait_until("Yours takes a short wait")
            self.play(items[0].animate.set_opacity(1), run_time=0.4)
            vo.wait_until("prints a table")
            self.play(items[1].animate.set_opacity(1), run_time=0.4)
            vo.wait_until("and adds an entry to your kubeconfig")
            self.play(items[2].animate.set_opacity(1), run_time=0.4)
            vo.wait_until("so kubectl knows where to go")
            self.play(Create(cl.edge), FadeIn(cl.fill), FadeIn(cl_t), run_time=0.6)
            self.play(GrowArrow(k_ar), run_time=0.5)
            vo.wait_until("The slide makes one node")
            self.play(FadeIn(nodes[0], shift=DOWN * 0.15), FadeIn(cmp_), run_time=0.5)
            vo.wait_until("the README two")
            self.play(FadeIn(nodes[1], shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("so two copies can land")
            self.play(GrowFromCenter(pods[0]), run_time=0.4)
            self.play(GrowFromCenter(pods[1]), run_time=0.4)
            self.play(*[Indicate(p, color=POD, scale_factor=1.2) for p in pods], run_time=0.6)
        gone1 = VGroup(yours, cl, cl_t, *nodes, *pods, cmp_, k_ar, cost, t)
        assert cost.get_bottom()[1] > STRIP_TOP + 0.1 and cost.get_right()[0] < 6.55, cost.get_right()

        # ========================================================== 2. the stand-in: kind (k01, extra)
        ts = laptop_term(13, P_LAPTOP, standin=True)
        assert ts.box.get_top()[1] < TRACK_BOTTOM - 0.1
        sr = on_bar(ts, standin_row())
        er = extra_row()
        er.move_to([sr.get_left()[0] - 0.15 - er.width / 2, sr.get_y(), 0])
        assert er.get_left()[0] > ts.title.get_right()[0] + 0.1, (er.get_left(), ts.title.get_right())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(gone1), track(trk, 5, True), run_time=0.5)
            self.remove(gone1, *gone1)
            self.play(FadeIn(ts, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(sr), FadeIn(er), run_time=0.4)
            ts.add(sr, er)
            type_capture(self, ts, K01, type_time=1.6)
            vo.wait_until("with a tool called kind")
            y = out(self, ts, K01.at((2, 7)), run_time=0.6)
            vo.wait_until("one control plane, two workers")
            roles = [substring(y[i], w) for i, w in ((3, "control-plane"), (4, "worker"), (5, "worker"))]
            self.play(*[r.animate.set_color(TOOL) for r in roles], run_time=0.4)
            self.play(each(roles, TOOL, 1.12), run_time=0.8)
            self.add(ts)
            vo.wait_until("Same API server")
            out(self, ts, K01.at(15, 17, 19, 21), run_time=0.8)
            vo.wait_until("but no Google")
            out(self, ts, K01.at(23, 25, 27, 29), run_time=0.8)
            last = out(self, ts, [(K01.line(30), ROUTE)], run_time=0.4)[0]
            vo.wait_until("It is not in the README")
            flash_tag(self, er, INK)
            vo.wait_until("don't run it")
            flash_tag(self, sr, INK)
            self.play(Indicate(last, color=ROUTE, scale_factor=1.04), run_time=0.6)
            self.add(ts)

        # ========================================================== 3. V1 on the laptop: the stand-in
        md = MasterDiagram(built=("laptop", "cluster", "plane", "parts", "beat23"))
        hide = label("on GKE: run by Google, out of sight", 24, INK).move_to([md.ref.get_x(), md.slot_y, 0])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(ts), run_time=0.4)
            self.remove(ts)
            self.play(FadeIn(md), run_time=0.6)
            v1_standin(self, md)
            vo.wait_until("a container we can see")
            self.play(Indicate(md.parts["plane_cap"].text, color=INK, scale_factor=1.15),
                      edge_flash(md.parts["plane"].frame.edge, TURN), run_time=0.8)
            md.heal(self)
            vo.wait_until("on GKE, Google hides it")
            self.play(FadeIn(hide, shift=UP * 0.1), edge_flash(md.parts["plane"].frame.edge, S.GREY), run_time=0.7)
            md.heal(self)

        # ========================================================== 4. the console (illustration)
        ref = lref("37")
        rc = readme_card((545, 549), CONSOLE_README, size=20)
        rc.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, 2.65, 0], UP)
        cv1 = console_view(["Kubernetes Engine", "Clusters", TEST_CLUSTER, "Nodes", "node", "Pods"])
        cv1.align_to([-6.45, 0, 0], LEFT).align_to([0, rc.get_bottom()[1] - 0.3, 0], UP)
        cv2 = console_view(["Compute Engine", "VM instances"], rows=["node VM", "node VM"])
        cv2.move_to(cv1, aligned_edge=UL)
        assert rc.get_right()[0] < 6.5 and cv1.get_right()[0] < 6.5, (rc.get_right(), cv1.get_right())
        assert cv2.get_bottom()[1] > -3.5, cv2.get_bottom()
        cr = cv1.crumbs
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(md, hide)), FadeIn(ref), track(trk, 6), run_time=0.5)
            self.remove(md, hide)
            self.play(FadeIn(rc, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("look around the console")
            self.play(FadeIn(cv1, shift=UP * 0.15), run_time=0.5)
            body = rc.body
            prev = None
            for phrase, ks, ln in (("Kubernetes Engine", (0, 1), 0), ("your cluster", (2,), 1),
                                   ("its nodes", (3,), 2), ("and the Pods on each node", (4, 5), 3)):
                vo.wait_until(phrase)
                back = [prev.animate.set_color(INK)] if prev is not None else []
                self.play(*[c.animate.set_color(TURN) for c in (cr[k] for k in ks)],
                          body[ln].animate.set_color(TURN), *back, run_time=0.3)
                self.play(*[Indicate(cr[k], color=TURN, scale_factor=1.12) for k in ks], run_time=0.5)
                self.add(cv1, rc)
                prev = body[ln]
            vo.wait_until("In Compute Engine")
            self.play(FadeOut(cv1, shift=LEFT * 0.4), prev.animate.set_color(INK),
                      body[4].animate.set_color(TURN), run_time=0.35)
            self.remove(cv1)
            self.play(FadeIn(cv2, shift=LEFT * 0.4), run_time=0.4)
            self.play(Indicate(cv2.crumbs[0], color=TURN, scale_factor=1.12), run_time=0.5)
            self.add(cv2, rc)
            vo.wait_until("your nodes are ordinary virtual machines")
            self.play(LaggedStart(*[edge_flash(r.box, CLOUD) for r in cv2.rows], lag_ratio=0.3), run_time=0.9)
            self.add(cv2)
        self.play(FadeOut(VGroup(rc, cv2, ref)), run_time=0.5)
        self.remove(rc, cv2, ref)

        # ========================================================== 5. kubectl version (extra): matched
        ref = lref("34")
        tk = term(toolbox_prompt(), 13, T_TB_STANDIN, size=20)
        assert tk.box.get_top()[1] < TRACK_BOTTOM - 0.1
        sk = on_bar(tk, standin_row())
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(tk, shift=UP * 0.2), FadeIn(ref), track(trk, 7, True), run_time=0.6)
            self.play(FadeIn(sk), run_time=0.3)
            tk.add(sk)
            vo.wait_until("First an extra, kubectl version")
            rv = type_capture(self, tk, K02, type_time=0.5)[0]
            ex = extra_row()
            pin(self, rv, beside(ex, rv))
            v = out(self, tk, K02.at(2, 4), run_time=0.5)
            tr_ = time_row()
            pin(self, v[1], beside(tr_, v[1]))
            vo.wait_until("the dispatcher picked a client")
            vs = [substring(v[0], "v1.34.12-gke.300.1+a8b9abb5a77ce6"), substring(v[1], "v1.34.11")]
            self.play(*[s.animate.set_color(TURN) for s in vs], run_time=0.4)
            self.play(Indicate(vs[0], color=TURN, scale_factor=1.08), run_time=0.6)
            self.add(tk)
            vo.wait_until("that matches the server's version")
            self.play(*[Indicate(s, color=TURN, scale_factor=1.08) for s in vs], run_time=0.8)
            self.add(tk)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 6. get all: only service/kubernetes
        ref = lref("35")
        with self.voiceover(SAY[6]) as vo:
            unpin(self, rv, ex, FadeIn(ref), track(trk, 7))
            vo.wait_until("get all")
            r3 = type_capture(self, tk, K03, type_time=0.4)[0]
            vo.wait_until("shows only a service named kubernetes")
            g3 = out(self, tk, [K03.crop(2, "PORT(S)"), K03.crop(3, "443/TCP")], run_time=0.4)
            sv = substring(g3[1], "service/kubernetes")
            self.play(sv.animate.set_color(SHARED), run_time=0.3)
            self.play(Indicate(sv, color=SHARED, scale_factor=1.1), run_time=0.6)
            self.add(tk)
            vo.wait_until("the door to the API server itself")
            self.play(Indicate(substring(g3[1], "443/TCP"), color=SHARED, scale_factor=1.12), run_time=0.7)
            self.add(tk)
            vo.wait_until("We are looking in the namespace called default")
            ns = row_tag("namespace: default")
            pin(self, r3, beside(ns, r3))
            flash_tag(self, ns, SHARED)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 7. all namespaces: the control plane
        boxes = VGroup(*[boxed(s, CLOUD, k=0.3) for s in ("etcd", "API server", "controller manager", "scheduler")])
        boxes.arrange(RIGHT, buff=0.35)
        plane = frame_box(boxes.width + 0.6, boxes.height + 1.25, CLOUD, k=0.1)
        pt = label("control plane", 20, INK)
        pc = label("a container you can see", 20, S.GREY)
        head = VGroup(pt, pc).arrange(RIGHT, buff=0.3)
        thumb = VGroup(plane, head, boxes)
        plane.move_to([0, 1.0, 0])
        head.move_to(plane).align_to(plane, UP).shift(DOWN * 0.15)
        boxes.move_to(plane).align_to(plane, DOWN).shift(UP * 0.3)
        hid = grey_chip("on GKE: run by Google, not listed")
        hid.next_to(plane, DOWN, buff=0.2)
        assert thumb.get_top()[1] < PIC_TOP and thumb.get_right()[0] < 6.5, thumb.get_right()
        assert hid.get_bottom()[1] > strip_top(4, 20) + 0.1, (hid.get_bottom(), strip_top(4, 20))
        with self.voiceover(SAY[7]) as vo:
            unpin(self, r3, ns)
            type_capture(self, tk, K04, type_time=0.5)
            g4 = out(self, tk, [name_crop(K04, 2), name_crop(K04, 5), name_crop(K04, 9),
                                K04.crop(10, "pod/kube-controller-manager", "…"), name_crop(K04, 14), "…",
                                K04.crop(18, "service/kubernetes"), K04.crop(19, "service/kube-dns")],
                     run_time=0.6)
            vo.wait_until("kube system appears")
            ks = [substring(r, "kube-system") for r in g4 if "kube-system" in r.text]
            ks.append(substring(g4[-2], "default"))
            self.play(*[k.animate.set_color(SHARED) for k in ks], run_time=0.4)
            self.add(tk)
            vo.wait_until("and here you can spot the control plane by name")
            type_capture(self, tk, K05, type_time=0.5)
            g5 = out(self, tk, [name_crop(K05, n) for n in range(2, 16)], run_time=0.8, chunk=7)
            by_n = {n: r for n, r in zip(range(2, 16), g5)}
            ks5 = [substring(r, "kube-system") for r in g5 if "kube-system" in r.text]
            self.play(*[k.animate.set_color(SHARED) for k in ks5], run_time=0.3)
            self.add(tk)
            keep = [by_n[n] for n in (5, 9, 10, 14)]
            resize(self, tk, 4, keep=keep, extra=[bar_follow(tk, sk, 4)], run_time=0.6)
            self.play(FadeIn(thumb, shift=DOWN * 0.15), run_time=0.5)
            for phrase, n, b in (("etcd", 5, 0), ("the API server", 9, 1), ("the controller manager", 10, 2),
                                 ("the scheduler", 14, 3)):
                vo.wait_until(phrase)
                nm = substring(by_n[n], CP_NAMES[n])
                self.play(nm.animate.set_color(CLOUD), edge_flash(boxes[b].frame.edge, TURN), run_time=0.4)
                self.add(tk)
            vo.wait_until("On GKE those stay hidden")
            self.play(FadeIn(hid, shift=UP * 0.1), plane.edge.animate.set_stroke(S.GREY), run_time=0.5)
            flash_tag(self, hid, INK, 1.06)

        # ========================================================== 8. componentstatuses, nodes; your turn
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(thumb, hid)), run_time=0.4)
            self.remove(thumb, hid)
            resize(self, tk, 12, keep=[], extra=[track(trk, 7), bar_follow(tk, sk, 12)], run_time=0.6)
            vo.wait_until("Component statuses prints")
            type_capture(self, tk, K06, type_time=0.5)
            g6 = out(self, tk, [(K06.line(2), SHARED)] + K06.at((3, 6)), run_time=0.5)
            vo.wait_until("which is expected")
            dep = grey_chip("deprecated since 1.19: expected")
            under_term(tk, dep)
            self.play(FadeIn(dep, shift=DOWN * 0.1), Indicate(g6[0], color=SHARED, scale_factor=1.03), run_time=0.6)
            self.add(tk)
            vo.wait_until("then three healthy lines")
            self.play(each([substring(g6[i], "Healthy") for i in (2, 3, 4)], OWN, 1.12), run_time=0.8)
            self.add(tk)
            vo.wait_until("Get nodes is the better check")
            self.play(FadeOut(dep), run_time=0.3)
            self.remove(dep)
            r7 = type_capture(self, tk, K07, type_time=0.4)[0]
            g7 = out(self, tk, K07.at((2, 5)), run_time=0.4)
            vo.wait_until("three nodes ready here")
            self.play(each([substring(g7[i], "Ready") for i in (1, 2, 3)], OWN, 1.15), run_time=0.8)
            self.add(tk)
            vo.wait_until("yours shows two workers")
            self.play(*[g7[i].animate.set_color(OWN) for i in (2, 3)], g7[1].animate.set_color(S.GREY), run_time=0.5)
            cp = substring(g7[1], "control-plane", occurrence=1)
            rg = ring(cp, S.GREY, buff=0.05, stroke=2.5)
            gk = grey_chip("control-plane · GKE: not listed")
            under_term(tk, gk)
            self.play(Create(rg), FadeIn(gk, shift=DOWN * 0.1), run_time=0.5)
            attach(self, g7[1], rg)
            vo.wait_until("Pause and try all five")
            yt2 = turn_row()
            pin(self, r7, beside(yt2, r7))
            flash_tag(self, yt2, TURN)

        self.play(FadeOut(VGroup(trk, tk, gk)), run_time=0.6)
        self.remove(trk, tk, gk)
        self.wait(0.4)
