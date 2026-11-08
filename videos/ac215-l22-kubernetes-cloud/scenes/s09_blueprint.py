"""S09 · The cheese app's cluster, as code (AC215 L22, the full follow-along; Part 2 opens here). No
tracker. Lecture: 22 · 41 (beat 0), 21–22 (beat 1).

Beats (script.md "## S09", one voiceover block each):
0. LECTURE 22 · 41. Two GREY README cards, stacked: 'README.md · line 392 / Deployment with Scaling using
   Kubernetes' (a PINK arrow from the left, 'course link lands here') and 'README.md · line 436 / Create &
   Deploy Cluster' (a GREY chip 'the cluster steps' and the tag 'erratum' beside it). Under each card its
   README tracker (D, then C) in YELLOW, small.
1. LECTURE 22 · 21–22. V5 CheeseBlueprint: the GREY-dashed L20 VM (nginx, api-service, frontend,
   vector-db, dashed loader) dissolves into the BLUE cluster; the table on the right writes
   'container → Deployment + Pods' (the three TEAL boxes become GREEN Deployment cards with a Pod) and
   'loader → Job' (the dashed loader becomes the GREEN Job card).
2. Table rows 'Docker network names → Services + DNS' (PINK 'frontend :3000', 'api :9000',
   'vector-db :8000') and '/mnt/disk-1 folders → 2 PVCs on cloud disks' (BLUE disks 'persistent-pvc
   5Gi', 'chromadb-pvc 10Gi').
3. Rows 'nginx container → Ingress controller + Ingress' ('nginx-f5', 'cheese-app-ingress'),
   'gcp-service.json → Workload Identity · no key', 'restart policy → ReplicaSet' (GREEN rings on the
   cards), 'one VM → node pool · 1–2 nodes'.
4. The table fades, the picture slides to the centre: BLUE 'cheese-app-vpc · subnet 10.0.0.0/19'
   frame; the pool's 'public IPs' badge peels off ('private nodes'); the BLUE 'Cloud NAT · outbound
   only' funnel at the VPC's right edge; the GREEN dashed 'cheese-app-namespace' frame; the BLUE load
   balancer at the left edge with a PINK arrow to nginx. GREY scene chips 'Workload Identity → S12',
   'Ingress → S13', 'PVC → S15', each joined to its part.
5. CODE(src/deployment/deploy_k8s/__main__.py: 19–30): the calls light in turn (YELLOW bar) with a GREY
   chip naming the file beside the comment line above each call (create_network.py, create_cluster.py,
   setup_containers.py); the panel scrolls to (31–40), the three chips line up under it and
   setup_loadbalancer.py joins them at line 38's call. An inset of line 17 `setupSSL = False` with the
   GREY chip 'HTTPS variant: off'.
6. A GOLD cost card, one line per phrase ('regional cluster · management fee', '1–2 × n2d-standard-2
   nodes', 'load balancer', 'Cloud NAT', '2 disks') with the GOLD meter sweeping beside it; the GOLD
   total tag; the GREY line 'check the pricing calculator · destroy it the same day'; the GREY chip
   'registry images outlive destroy (S16)'. Fade; empty frame.

Deviations from SHOW:
- Beat 0: "the two tracker titles" are the two README trackers themselves (tracker_d(), tracker_c(),
  YELLOW, no step lit), so the viewer sees both step lists the video follows.
- Beat 5: the 12-line limit means 19–30, then 31–40; the three file chips stand beside the comment line
  above each call (the calls themselves are 60+ characters, so a chip beside them would leave the
  frame) and move under the panel at the scroll, where the fourth joins them. Both panels are 20 pt
  (line 35 is 72 characters).
- Beat 6: the total reads '≈ $5–8 a day, roughly · our estimate' (cost_tag allows an amount only with
  '≈' and 'roughly'); 'check the pricing calculator' is a GREY line under it with the narration's
  'destroy it the same day'. A CostDial (the series' GOLD meter) sweeps beside the card so something
  moves while the lines arrive.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S09"]
assert len(SAY) == SAY_COUNT["S09"] == 7

MAIN = "src/deployment/deploy_k8s/__main__.py"
assert readme(392) == "## Deployment with Scaling using Kubernetes"
assert readme(436) == "## Create & Deploy Cluster"
assert excerpt(MAIN, 17, 17) == "setupSSL = False"
assert excerpt(MAIN, 19, 19) == "# Create the required network setups"
assert "create_network(region, app_name)" in excerpt(MAIN, 20, 20)
assert excerpt(MAIN, 22, 22) == "# Create & Setup Cluster"
assert excerpt(MAIN, 23, 23).endswith("= create_cluster(")
assert excerpt(MAIN, 27, 27) == "# Setup Containers"
assert excerpt(MAIN, 28, 28).endswith("= setup_containers(")
assert excerpt(MAIN, 32, 32) == "# Setup Load Balancer"
assert excerpt(MAIN, 38, 38).endswith("= setup_loadbalancer(")

CALLS = (  # (comment line, call line, call name, file chip)
    (19, 20, "create_network", "create_network.py"),
    (22, 23, "create_cluster", "create_cluster.py"),
    (27, 28, "setup_containers", "setup_containers.py"),
    (32, 38, "setup_loadbalancer", "setup_loadbalancer.py"),
)


class Blueprint(VoiceScene):
    def construct(self):
        # ========================================================== 0. the handover: two README headings
        ref = lref("41")
        c1 = readme_card(392, "Deployment with Scaling using Kubernetes")
        c2 = readme_card(436, "Create & Deploy Cluster")
        c1.move_to([-2.2, 2.0, 0], aligned_edge=LEFT)
        c2.move_to([-2.2, -0.55, 0], aligned_edge=LEFT)
        tr1 = tracker_d().move_to([-2.2, 0.95, 0], aligned_edge=LEFT)
        tr2 = tracker_c().move_to([-2.2, -1.6, 0], aligned_edge=LEFT)
        for tr in (tr1, tr2):          # the two trackers, small and YELLOW (no step lit yet)
            tr.head[2].set_color(TURN)
            tr.dots.set_color(TURN)
        land = label("course link lands here", 22, ROUTE).move_to([-6.45, 2.0, 0], aligned_edge=LEFT)
        land_a = route(land.get_right(), c1.get_left(), stroke=4)
        steps = grey_chip("the cluster steps", size=22).next_to(c2, RIGHT, buff=0.3)
        err = erratum_tag().next_to(steps, RIGHT, buff=0.2)
        assert err.get_right()[0] < 6.5, err.get_right()
        steps_a = arrow(steps.get_left() + LEFT * 0.02, c2.get_right(), S.GREY, buff=0.04)
        part2 = label("Part 2 · the cheese app on GKE, as Pulumi code", 26, INK).move_to([0, -2.85, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(part2, shift=UP * 0.3, scale=0.9), run_time=1.2)
            vo.wait_until("The course link lands")
            self.play(FadeIn(c1, shift=RIGHT * 0.3), run_time=0.6)
            self.play(FadeIn(land), GrowArrow(land_a), run_time=0.6)
            self.play(FadeIn(tr1, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("the cluster steps continue")
            self.play(FadeIn(c2, shift=RIGHT * 0.3), run_time=0.6)
            self.play(FadeIn(steps), GrowArrow(steps_a), run_time=0.5)
            self.play(FadeIn(tr2, shift=DOWN * 0.15), FadeIn(err), run_time=0.5)
            vo.wait_until("Create and Deploy Cluster")
            self.play(Indicate(c2.body, color=TURN, scale_factor=1.06), run_time=0.8)
        beat0 = VGroup(c1, c2, tr1, tr2, land, land_a, steps, steps_a, err, part2)
        self.play(FadeOut(beat0), FadeOut(ref), run_time=0.5)
        self.remove(beat0, ref)

        # ========================================================== 1. L20's VM dissolves into the cluster
        ref = lref("21–22")
        cb = CheeseBlueprint()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(ref), run_time=0.3)
            cb.l20(self)
            vo.wait_until("piece by piece")
            cb.dissolve(self)
            vo.wait_until("Each long-running container")
            cb.row(self, 0)
            vo.wait_until("The one-shot loader")
            cb.row(self, 1)
            vo.wait_until("it retries a failed run")
            self.play(Indicate(cb.parts["job"], color=OWN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("once it succeeds")
            self.play(Circumscribe(cb.parts["job"], color=OWN, run_time=1.0))
            cb.heal(self)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 2. Services and PVCs
        with self.voiceover(SAY[2]) as vo:
            cb.row(self, 2)
            self.play(each([cb.parts[f"svc_{k}"] for k in ("front", "api", "vdb")], ROUTE), run_time=0.8)
            cb.heal(self)
            vo.wait_until("The folders on the VM disk")
            cb.row(self, 3)
            vo.wait_until("each backed by a cloud disk")
            self.play(each([cb.parts["pvc1"], cb.parts["pvc2"]], CLOUD), run_time=0.8)
            cb.heal(self)

        # ========================================================== 3. Ingress, Workload Identity, ReplicaSet, pool
        with self.voiceover(SAY[3]) as vo:
            cb.row(self, 4)
            vo.wait_until("The JSON key")
            cb.row(self, 5)
            cb.row(self, 6)
            vo.wait_until("One machine")
            cb.row(self, 7)
            self.play(Indicate(cb.parts["pool"], color=CLOUD, scale_factor=1.04), run_time=0.8)
            cb.heal(self)

        # ========================================================== 4. around it: VPC, private nodes, NAT, namespace, LB
        with self.voiceover(SAY[4]) as vo:
            cb.drop_table(self)
            cb.slide_center(self)
            cb.vpc(self)
            vo.wait_until("The nodes get no public addresses")
            cb.private_nodes(self)
            vo.wait_until("a Cloud NAT gateway")
            cb.nat(self)
            vo.wait_until("for example to pull Chroma")
            self.play(Indicate(cb.extras["nat"], color=CLOUD, scale_factor=1.08), run_time=0.7)
            cb.heal(self)
            vo.wait_until("The app sits in one namespace")
            cb.namespace(self)
            vo.wait_until("behind one load balancer")
            cb.lb(self)
            cb.chip(self, "ingress", "Ingress → S13")
            cb.chip(self, "pvc2", "PVC → S15")
            # Workload Identity sits bottom-left: its chip goes left of the VPC (a chip in the right
            # column would draw its line across the whole cluster)
            wi = cb.parts["wi"]
            wchip = two_row_chip("Workload Identity", "→ S12", S.GREY)
            vpc_left = cb.extras["vpc"][0].get_left()[0]
            wchip.move_to([vpc_left - 0.25 - wchip.width / 2, wi.get_y(), 0])
            assert wchip.get_left()[0] > -6.55, wchip.get_left()
            wline = Line(wchip.get_right(), wi.get_left(), color=S.GREY, stroke_width=1.5)
            cb.extras["chip_wi"] = cb.show(self, VGroup(wline, wchip), anims=[Create(wline), FadeIn(wchip)],
                                           run_time=0.5)
        self.play(FadeOut(cb), run_time=0.5)
        self.remove(cb)

        # ========================================================== 5. __main__.py: four calls, four files
        pa = code(MAIN, 19, 30, font_size=20)
        pa.move_to([0, 1.95, 0], aligned_edge=UP)
        pb = code(MAIN, 32, 40, font_size=20)
        pb.move_to([0, 1.95, 0], aligned_edge=UP)
        chips = []
        for cmt, call, fn, fname in CALLS:
            p = pa if call <= 30 else pb
            first = 19 if p is pa else 32
            ch = grey_chip(fname, mono_font=True)
            anchor_ln = p.code.code_lines[cmt - first]
            ch.move_to([anchor_ln.get_right()[0] + 0.5 + ch.width / 2, anchor_ln.get_y(), 0])
            chips.append(ch)
        assert all(ch.get_right()[0] < 6.5 for ch in chips)
        inset = code(MAIN, 17, 17, font_size=20).move_to([-1.55, 2.85, 0])
        https = grey_chip("HTTPS variant: off").next_to(inset, RIGHT, buff=0.3)
        assert inset.get_top()[1] < 3.55 and inset.get_bottom()[1] > pa.get_top()[1] + 0.05, inset.get_bottom()
        row_top = pb.get_bottom()[1] - 0.25
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeIn(pa, shift=UP * 0.2), run_time=0.6)
            bars = []
            for (cmt, call, fn, fname), ch, word in zip(CALLS[:3], chips, ("the network", "the cluster",
                                                                            "the containers")):
                vo.wait_until(word)
                bar = line_bar(pa.code, call - 19, TURN)
                bars.append(bar)
                self.play(FadeIn(bar), code_span(pa.code, call - 19, fn).animate.set_color(TURN),
                          FadeIn(ch, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("the load balancer")
            # scroll: 19-30 out upwards, 31-40 in; the three chips line up under the new panel
            row = VGroup(*[c.copy() for c in chips]).arrange_in_grid(2, 2, buff=(0.4, 0.2))
            row.move_to([0, row_top, 0], aligned_edge=UP)
            assert row.get_bottom()[1] > -3.5 and row.width < 12.8, (row.get_bottom(), row.width)
            self.play(FadeOut(VGroup(pa, *bars), shift=UP * 0.4), FadeIn(pb, shift=UP * 0.4),
                      *[ch.animate.move_to(r.get_center()) for ch, r in zip(chips[:3], row[:3])],
                      run_time=0.8)
            self.remove(pa, *bars)
            bar4 = line_bar(pb.code, 38 - 32, TURN)
            chips[3].move_to(row[3])
            fresh = code_span(pb.code, 38 - 32, "setup_loadbalancer")
            self.play(FadeIn(bar4), fresh.animate.set_color(TURN), FadeIn(chips[3], shift=DOWN * 0.2),
                      run_time=0.5)
            self.add(pb, bar4)
            self.play(each(chips, TURN), run_time=0.8)
            vo.wait_until("Line 17")
            low = VGroup(pb, bar4, *chips)
            dy = min(0.45, low.get_bottom()[1] + 3.45)
            assert inset.get_bottom()[1] > pb.get_top()[1] - dy + 0.05, dy
            self.play(low.animate.shift(DOWN * dy), FadeIn(inset, shift=DOWN * 0.2), run_time=0.6)
            self.play(FadeIn(https, shift=LEFT * 0.2),
                      code_span(inset.code, 0, "False").animate.set_color(TURN), run_time=0.5)
            self.add(inset)
        beat5 = VGroup(pb, bar4, inset, https, *chips)
        self.play(FadeOut(beat5), run_time=0.5)
        self.remove(beat5)

        # ========================================================== 6. the meter while it is up
        rows = ("regional cluster · management fee", f"1–2 × {MACHINE} nodes", "load balancer", "Cloud NAT",
                "2 disks")
        cc = card(rows, color=COST, size=24, head="billed while it is up")
        cc.move_to([0.9, 0.85, 0])
        lines = list(cc.body.submobjects)
        shell = VGroup(cc.frame, cc.head)
        dial = CostDial(0.6, "the meter").next_to(cc, LEFT, buff=0.6)
        total = cost_tag("≈ $5–8 a day, roughly · our estimate").next_to(cc, DOWN, buff=0.35)
        calc = label("check the pricing calculator · destroy it the same day", 22, S.GREY)
        calc.next_to(total, DOWN, buff=0.25)
        reg = grey_chip("registry images outlive destroy (S16)").next_to(calc, DOWN, buff=0.3)
        allg = VGroup(cc, dial, total, calc, reg)
        assert allg.get_top()[1] < 3.5 and allg.get_bottom()[1] > -3.5 and allg.get_left()[0] > -6.5, \
            (allg.get_top(), allg.get_bottom(), allg.get_left())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(shell), FadeIn(dial), run_time=0.6)
            for ln, word in zip(lines, ("the fee of a regional cluster", "one or two nodes", "a load balancer",
                                        "one NAT gateway", "two disks")):
                vo.wait_until(word)
                self.play(FadeIn(ln, shift=RIGHT * 0.2), run_time=0.35)
                dial.run(self, 0.12, 0.45)
            vo.wait_until("By our estimate")
            self.play(FadeIn(total, shift=UP * 0.15), run_time=0.5)
            dial.run(self, 0.2, 0.9)
            vo.wait_until("check the pricing calculator")
            self.play(FadeIn(calc), run_time=0.5)
            vo.wait_until("and destroy it the same day")
            self.play(FadeIn(reg, shift=UP * 0.15), run_time=0.5)
            dial.run(self, 0.15, 0.8)
        dial.freeze()
        self.play(FadeOut(VGroup(shell, *lines, dial, total, calc, reg)), run_time=0.6)
        self.remove(*self.mobjects)
        self.wait(0.3)
