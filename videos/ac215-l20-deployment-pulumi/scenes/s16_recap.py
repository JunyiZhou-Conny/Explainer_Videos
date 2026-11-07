"""S16 · Destroy, recap, and what's next (AC215 L20). TRACKER [P] 14 in beats 1-3; no tracker from
beat 4 on. Lecture tags: 20 · 29 (beat 0), 20 · 19 (beat 6), 20 · 12 (beat 7), 20 · 4 (beat 8).
Ends part 2 on an empty frame.

Beats (script.md "## S16", one voiceover block each):
0. LECTURE 20 · 29. A GOLD card in the centre, words only: "Don't forget to delete"; five GOLD meters
   under it (VM, disks, IP, registry, bucket) sweep.
1. TRACKER [P] 14. Terminal 'laptop · toolbox' at /app/deploy_single_vm types `pulumi destroy --stack
   dev --refresh -y` -> TERM(b22: 2) RED, a YELLOW '▶ your turn' beside the typed line. TRACKER [P] 14
   · extra: the same command on the local backend (extra row tag) -> TERM(b45: 2, 6, 10, 12 wrap, 13);
   'Duration: 1s' lights.
2. V4 plays backwards on the finished V1 (laptop + state, the VPC 'cheese-app-network' with its three
   PINK gates, the VM, its disk and four containers): RED '-' glyphs pop on every part, then the parts
   fade in reverse order, one per phrase: the containers (a pulse through the PINK SSH tunnel), the
   VM, the disk, the firewalls, the network.
3. Two folder cards: deploy_single_vm (GREEN tick 'destroys the VM') and deploy_images (YELLOW 'only
   forgets the images'); V6's shelf of crates stays, each crate gets a small GOLD padlock,
   'retain_on_delete' under it. GREY erratum tag "the README doesn't say which folder".
4. No tracker. The GOLD teardown checklist: items 1-3 write in and tick one per phrase (2 and 3 with
   an 'extra' tag, no output panel). Item 1's check is `gcloud compute instances list → empty`
   (extra); item 3 gets a GREY line 'after pulumi destroy in deploy_images too' at "once no stack"
   (the images stack still lists its three images until then).
5. Items 4-6 write in and tick.
6. LECTURE 20 · 19. The checklist goes; the six-step strip at full width, each chip with its file;
   above it a compact V1 grows one layer per chip (toolbox -> registry crates -> VM + disk ->
   provisioning tiles -> containers -> nginx and the browser).
7. LECTURE 20 · 12. Slide 12's six principles as six GREY chips around a PURPLE 'Pulumi' hub, then a
   scorecard: GREEN ticks on real languages, declarative, state & previews; GREY crosses on components,
   tests; a GREY chip 'many providers, one cloud' beside multi-cloud.
8. LECTURE 20 · 4. Slide 4's roadmap returns (marker on 'Deployment, Scaling & Automation'); a single
   VM pulses RED 'single point of failure'; three GREY-dashed chips slide in under the bar: L21, L22,
   L23.
9. Clear. 'Test yourself · 1/5': card 1.
10. Card 1 -> 2 -> 3 on the sentence starts.
11. Card 3 -> 4 -> 5; at 'Answers are in' card 5 fades, then the progress dots become the GREY
    pointer card 'answers: exercises.md · study guide', which moves to the centre. Fade (within ~1 s
    of the last word); empty frame.

Deviations from SHOW:
- Beat 0: the meters are V1's GOLD cost dials (text-free needles) with one-word captions.
- Beat 2: V1 has no firewall or network parts, so the scene adds the VPC (BLUE dashed, 'VPC ·
  cheese-app-network') with its three gates (22 / 80 / 443) on the wall facing the laptop; the
  registry and browser are left out (the registry is beat 3's subject). All '-' glyphs pop together
  first (V4's diff), then the parts fade one per phrase (V4's backwards()).
- Beat 3: V6's shelf is drawn already filled (two runs of crates), not replayed through the conveyor.
  The GOLD padlocks are drawn here (on each crate's top edge, right end) instead of TimestampPipe.retain(),
  whose padlocks sit on the crate's bottom-left corner over the name.
- Beat 6: the full V1 (6 units tall) cannot sit above the strip, so a compact V1 of the same parts and
  colours grows there (text-free provisioning tiles, short names).
- Beat 7: the principles sit in a hub around a 'Pulumi' chip (slide 12's layout; no logo).
- Beat 8: the roadmap comes back at its S01 size (text never shrinks below 20 pt); the VM and the
  chips sit under it.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from s01_hook import roadmap

SAY = NARRATION["S16"]

# ------------------------------------------------------------------ the real sources (checked)
B22 = capture("b22")
B45 = capture("b45")
CMD = "pulumi destroy --stack dev --refresh -y"
assert B22.cmd == CMD and B45.cmd == CMD, (B22.cmd, B45.cmd)
assert readme(389).strip() == CMD, readme(389)
assert B22.line(2).startswith("error: PULUMI_ACCESS_TOKEN must be set"), B22.line(2)
assert B45.line(2) == "Previewing destroy (dev):" and B45.line(6) == "Destroying (dev):", B45.lines
assert B45.line(10) == "Duration: 1s", B45.line(10)
assert B45.line(12).startswith("The resources in the stack have been deleted"), B45.line(12)
assert B45.line(13).startswith("If you want to remove the stack completely"), B45.line(13)
BUCKET = "gs://your-gcp-project-pulumi-state-bucket"
assert 'PULUMI_BUCKET="gs://$GCP_PROJECT-pulumi-state-bucket"' in excerpt("src/deployment/docker-shell.sh", 17, 17)

P_SINGLE = toolbox_prompt("/app/deploy_single_vm")
METERS = ("VM", "disks", "IP", "registry", "bucket")
SHELF = ("api-service", "frontend-react", "vector-db")

# Slide 12's six principles (our short names), hub order: left column 1-3, right column 4-6
PRINCIPLES = ("real languages", "declarative", "components", "multi-cloud", "state & previews", "tests")
SCORE = ("yes", "yes", "no", "note", "yes", "no")

# Test-yourself cards: one row per clause; (s, 'm') = mono
QUESTIONS = (
    (("Trace", ("http://<instance_ip>/api-service/status", "m"), ":"),
     ("which gate, which container, which", ("location", "m"), "block,"),
     ("and which character makes FastAPI see", ("/status", "m"), "?")),
    (("What three things does", ("pulumi up", "m"), "compare,"),
     ("what does", ("--refresh", "m"), "change,"),
     ("and what does", ("-y", "m"), "skip?")),
    (("Name the two service accounts,",),
     ("where each key sits (laptop, VM),",),
     ("and what each may do.",)),
    (("Which of slide 19's six steps can Pulumi inspect afterwards,",),
     ("and which does it only remember running?",),
     ("Why must those scripts be safe to run twice?",)),
    (("What survives", ("pulumi destroy", "m"), "in", ("deploy_single_vm", "m"), ","),
     ("and how do you clean it up?",)),
)
Q_W = 12.0


def parts_row(*parts, size: float = 20, base=INK) -> VGroup:
    """A row of pieces: str -> label; (s, 'm') -> mono; (s, colour) -> label in that colour; a mobject
    is used as it is. Punctuation hugs the piece before it."""
    ms = []
    for p in parts:
        if isinstance(p, VMobject):
            ms.append(p)
        elif isinstance(p, str):
            ms.append(label(p, size, base))
        elif p[1] == "m":
            ms.append(mono(p[0], size, base))
        else:
            ms.append(label(p[0], size, p[1]))
    g = VGroup(*ms)
    for a, b in zip(ms, ms[1:]):
        punct = isinstance(b, Text) and b.original_text[:1] in ",:;?."
        b.next_to(a, RIGHT, buff=0.04 if punct else 0.14)
        if punct:
            b.align_to(a, DOWN)
        else:
            b.set_y(ms[0].get_y())
    return g


def qcard(rows_spec, size: float = 26) -> VGroup:
    """A YELLOW question card with mono spans. .frame .body"""
    rows = VGroup(*[parts_row(*r, size=size) for r in rows_spec]).arrange(DOWN, buff=0.2)
    frame = RoundedRectangle(width=Q_W, height=rows.height + 0.7, corner_radius=0.16, stroke_color=TURN,
                             stroke_width=3).set_fill(S.BG, 1)
    rows.move_to(frame)
    assert rows.width < Q_W - 0.5, rows.width
    g = VGroup(frame, rows)
    g.frame, g.body = frame, rows
    return g


def minus(w: float = 0.32, color=ERR) -> Line:
    """V4's RED '-' (delete) glyph, drawn as a bar so it reads at any size."""
    return Line(LEFT * w / 2, RIGHT * w / 2, color=color, stroke_width=8)


def teardown_items() -> list:
    """The six checklist rows (each a VGroup of one or two lines)."""
    n = lambda k: label(k, 20, COST)  # noqa: E731
    i1 = VGroup(parts_row(n("1"), ("pulumi destroy --stack dev --refresh -y", "m"), "in",
                          ("deploy_single_vm", "m")),
                parts_row(("gcloud compute instances list", "m"), "→ empty", extra_tag(), base=S.GREY))
    i2 = VGroup(parts_row(n("2"), ("gcloud artifacts repositories delete", "m")),
                parts_row(("cheese-app-repository --location=us", "m"), extra_tag()))
    i3 = VGroup(parts_row(n("3"), ("gcloud storage rm -r", "m")),
                parts_row((BUCKET, "m"), ("· last", COST), extra_tag()),
                parts_row("after", ("pulumi destroy", "m"), "in", ("deploy_images", "m"),
                          "too (it only forgets the images)", base=S.GREY))
    i4 = VGroup(parts_row(n("4"), "the part 1 VM, if it still runs"))
    i5 = VGroup(parts_row(n("5"), "Docker Hub images · free, optional"))
    i6 = VGroup(parts_row(n("6"), "the two service-account keys, when the course ends"))
    items = [i1, i2, i3, i4, i5, i6]
    for it in items:
        it.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for sub in it[1:]:
            sub.shift(RIGHT * (it[0][1].get_left()[0] - sub.get_left()[0]))   # indent under the command
    return items


def recap_picture(top: float, bottom: float) -> dict:
    """A compact V1 between y=bottom and y=top (series colours, short names): one layer per slide-19
    step. Returns {'setup', 'images', 'vm', 'provision', 'containers', 'web', 'pull'}."""
    L = {}
    # 1 setup: the laptop with the toolbox
    lap_top, lap_bot = top - 0.75, (top + bottom) / 2 + 0.25
    lap = RoundedRectangle(width=2.6, height=lap_top - lap_bot, corner_radius=0.16, stroke_color=LAPTOP,
                           stroke_width=3).set_fill(tint(LAPTOP, 0.06), 1)
    lap.move_to([-5.0, (lap_top + lap_bot) / 2, 0])
    lt = label("Your Machine", 20, LAPTOP).next_to(lap.get_corner(UL), DR, buff=0.12)
    tb = svc_box("toolbox", None, 2.0, 0.55).next_to(lt, DOWN, buff=0.15).set_x(lap.get_center()[0])
    L["setup"] = VGroup(lap, lt, tb)
    L["toolbox"] = tb
    # 2 images: Artifact Registry with three crates
    reg_top, reg_bot = lap_bot - 0.2, bottom
    reg = RoundedRectangle(width=2.6, height=reg_top - reg_bot, corner_radius=0.16, stroke_color=CLOUD,
                           stroke_width=3).set_fill(tint(CLOUD, 0.07), 1)
    reg.move_to([-5.0, (reg_top + reg_bot) / 2, 0])
    rt = label("Artifact Registry", 20, CLOUD).next_to(reg.get_top(), DOWN, buff=0.12)
    crates = VGroup(*[crate(nm, crate_w=2.25, crate_h=0.42) for nm in SHELF]).arrange(DOWN, buff=0.08)
    crates.next_to(rt, DOWN, buff=0.12)
    assert crates.get_bottom()[1] > reg.get_bottom()[1] + 0.05, (crates.get_bottom(), reg.get_bottom())
    L["registry"] = VGroup(reg, rt)
    L["crates"] = crates
    # 3 VM (+ disk on a cable)
    vm_top = top - 1.0
    vm = RoundedRectangle(width=6.6, height=vm_top - bottom, corner_radius=0.16, stroke_color=CLOUD,
                          stroke_width=3).set_fill(tint(CLOUD, 0.05), 1)
    vm.move_to([0.2, (vm_top + bottom) / 2, 0])
    vt = label("VM", 20, CLOUD).next_to(vm.get_corner(UL), DR, buff=0.12)
    dk = disk_cyl(0.55).move_to([4.6, bottom + 0.55, 0])
    cable = Line(vm.get_right()[0] * RIGHT + dk.get_center()[1] * UP, dk.get_left(), color=CLOUD, stroke_width=4)
    L["vm"] = VGroup(vm, vt, cable, dk)
    L["pull"] = arrow(reg.get_right() + UP * 0.2, np.array([vm.get_left()[0], reg.get_right()[1] + 0.2, 0]), LAPTOP,
                      stroke=4, buff=0.05)
    # 4 provision: nine text-free PURPLE tiles (V7b) along the VM's floor
    tiles = VGroup(*[RoundedRectangle(width=0.34, height=0.34, corner_radius=0.05, stroke_color=TOOL,
                                      stroke_width=3).set_fill(tint(TOOL, 0.18), 1) for _ in range(9)])
    tiles.arrange(RIGHT, buff=0.24).move_to([0.2, bottom + 0.35, 0])
    L["provision"] = tiles
    # 5 containers
    ys = bottom + 1.2
    boxes = VGroup(svc_box("frontend", PORTS["front"], 1.85, 0.72).move_to([-1.9, ys, 0]),
                   svc_box("api-service", PORTS["api"], 1.85, 0.72).move_to([0.2, ys, 0]),
                   svc_box("vector-db", PORTS["vdb"], 1.85, 0.72).move_to([2.3, ys, 0]))
    L["containers"] = boxes
    # 6 web server: nginx, the 80 door, the browser and the routes
    ng = svc_box("nginx", None, 1.8, 0.56).move_to([0.2, ys + 1.0, 0])
    d80 = door("80").move_to([0.2, vm.get_top()[1], 0])
    br = mini_browser(f"http://{IP_PH}/").move_to([0.2, top - 0.3, 0])
    rts = VGroup(route(br.get_bottom(), d80.get_top() + UP * 0.02),
                 route(d80.get_bottom(), ng.frame.get_top()),
                 route(ng.frame.get_bottom() + LEFT * 0.5, boxes[0].frame.get_top() + RIGHT * 0.3),
                 route(ng.frame.get_bottom(), boxes[1].frame.get_top()),
                 route(boxes[1].frame.get_right(), boxes[2].frame.get_left()))
    L["web"] = VGroup(ng, d80, br)
    L["routes"] = rts
    # layout checks
    assert vt.get_top()[1] < vm.get_top()[1] and ng.frame.get_top()[1] < vm.get_top()[1] - 0.3
    assert boxes.get_bottom()[1] > tiles.get_top()[1] + 0.1 and ng.frame.get_bottom()[1] > boxes.get_top()[1] + 0.15
    assert boxes.get_left()[0] > vm.get_left()[0] + 0.1 and boxes.get_right()[0] < vm.get_right()[0] - 0.1
    assert vm.get_left()[0] > reg.get_right()[0] + 0.4 and dk.get_right()[0] < 6.5
    assert br.get_top()[1] < PIC_TOP + 0.05 and br.get_bottom()[1] > d80.get_top()[1] + 0.1, (br.get_top(), d80.get_top())
    assert vt.get_right()[0] < boxes[0].get_left()[0] or vt.get_bottom()[1] > boxes.get_top()[1]
    return L


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S16"] == 12, len(SAY)

        # ========================================================== 0. slide 29: don't forget to delete
        r29 = lref("29")
        word = label("Don't forget to delete", 40, COST)
        wfr = outline_box(word.width + 0.9, word.height + 0.6, COST, solid=True, fill_opacity=0.1)
        word.move_to(wfr)
        dcard = VGroup(wfr, word).move_to([0, 1.0, 0])
        dials = VGroup(*[CostDial(0.42, m) for m in METERS]).arrange(RIGHT, buff=0.75).move_to([0, -1.6, 0])
        assert dials.get_top()[1] < dcard.get_bottom()[1] - 0.4 and dials.width < 12.4
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(r29), FadeIn(dcard, scale=1.1), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.15) for d in dials], lag_ratio=0.15), run_time=0.7)
            vo.wait_until("don't forget to delete")
            self.play(Indicate(word, color=COST, scale_factor=1.06),
                      *[d.tracker.animate(rate_func=linear).increment_value(0.6 + 0.1 * i)
                        for i, d in enumerate(dials)], run_time=1.6)
        for d in dials:
            d.freeze()

        # ========================================================== 1. b22, then b45 on the local backend
        trk = tracker_p(14)
        t = toolbox_term(13, "/app/deploy_single_vm")      # 13 rows: b22 (4) + b45 (9) without a scroll
        assert t.box.get_top()[1] < TRACK_BOTTOM - 0.1, t.box.get_top()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(dcard, dials, r29)), run_time=0.4)
            self.remove(dcard, dials, r29)
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.3), run_time=0.6)
            typed = type_capture(self, t, B22, type_time=0.9)[-1]
            e22 = out(self, t, [(B22.line(2), ERR)], wrap=True, run_time=0.4)
            vo.wait_until("Pause and run yours")
            pin(self, typed, beside(turn_row(), typed), run_time=0.4)
            vo.wait_until("Ours shows the login error")
            self.play(Indicate(e22, color=ERR, scale_factor=1.03), run_time=0.8)
            self.add(t)
            vo.wait_until("on the local backend")
            self.play(track(trk, 14, True), run_time=0.4)
            typed2 = type_capture(self, t, B45, type_time=0.7)[-1]
            pin(self, typed2, beside(extra_row(), typed2), run_time=0.3)
            rows = out(self, t, [B45.line(2), B45.line(6), (B45.line(10), OUTPUT), B45.line(12), B45.line(13)],
                       wrap=True, run_time=0.8)
            dur = [r for r in rows if r.text == "Duration: 1s"]
            assert len(dur) == 1, [r.text for r in rows]
            vo.wait_until("it finishes in a second")
            self.play(Indicate(dur[0], color=TURN, scale_factor=1.1), run_time=0.8)
            self.add(t)

        # ========================================================== 2. V4 backwards on the finished V1
        md = MasterDiagram(built=("laptop", "state", "vm", "disk", "front", "api", "vdb", "nginx", "routes"))
        P = md.parts
        vpc_box = DashedVMobject(RoundedRectangle(width=6.2, height=4.85, corner_radius=0.2),
                                 num_dashes=110, dashed_ratio=0.55).set_stroke(CLOUD, 3).move_to([3.4, -0.9, 0])
        vpc_t = VGroup(label("VPC ·", 20, CLOUD), mono(NETWORK, 20, CLOUD)).arrange(RIGHT, buff=0.12)
        vpc_t.next_to(vpc_box, UP, buff=0.12).align_to(vpc_box, LEFT).shift(RIGHT * 0.1)
        gx = vpc_box.get_left()[0]
        gates = VGroup(*[door(pt).move_to([gx, y, 0]) for pt, y in (("22", 0.45), ("80", -0.35), ("443", -1.15))])
        net = VGroup(vpc_box, vpc_t)
        assert gates.get_right()[0] < P["front"].frame.get_left()[0] - 0.1, gates.get_right()
        assert gates[0].get_right()[0] < P["vm"].title.get_left()[0] or gates[0].get_top()[1] < P["vm"].title.get_bottom()[1]
        assert vpc_t.get_top()[1] < PIC_TOP and vpc_box.get_bottom()[1] > -3.55 and vpc_box.get_right()[0] < 6.55
        assert P["disk"].get_bottom()[1] > vpc_box.get_bottom()[1] + 0.05, P["disk"].get_bottom()
        lap_fr = P["laptop"].frame
        tunnel = Line([lap_fr.get_right()[0], 0.75, 0], gates[0].get_left() + UP * 0.1, color=ROUTE, stroke_width=8)
        ssh_t = label("SSH", 20, ROUTE).next_to(tunnel.get_center(), UP, buff=0.15)
        # the '-' glyphs: one per part
        g_box = {k: minus(0.24).next_to(P[k].frame, LEFT, buff=0.05) for k in ("front", "api", "vdb", "nginx")}
        g_vm = minus().move_to(P["vm"].frame.get_corner(UR) + np.array([-0.3, -0.3, 0]))
        g_disk = minus().next_to(P["disk"].frame, LEFT, buff=0.15)
        g_gates = [minus().next_to(g, LEFT, buff=0.12).shift(DOWN * 0.12) for g in gates]
        g_net = minus().next_to(vpc_t, LEFT, buff=0.12)
        for k, g in g_box.items():
            assert g.get_left()[0] > P["vm"].frame.get_left()[0] + 0.02, k
        assert g_gates[0].get_left()[0] > lap_fr.get_right()[0] + 0.1
        all_g = [*g_box.values(), g_vm, g_disk, *g_gates, g_net]
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(t), track(trk, 14), run_time=0.4)
            self.remove(t)
            self.play(FadeIn(md), FadeIn(net), FadeIn(gates), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(g, scale=1.6) for g in all_g], lag_ratio=0.08), run_time=1.0)
            vo.wait_until("the containers over SSH")
            dot = pulse_dot().move_to(tunnel.get_start())
            self.play(Create(tunnel), FadeIn(ssh_t), run_time=0.4)
            self.add(dot)
            self.play(travel(dot, tunnel, run_time=0.5))
            self.remove(dot)
            md.drop(self, P["routes"], P["front"], P["api"], P["vdb"], P["nginx"], run_time=0.4,
                    extra=[FadeOut(VGroup(*g_box.values()))])
            self.remove(*g_box.values())
            vo.wait_until("then the VM")
            md.drop(self, P["vm"], run_time=0.4, extra=[FadeOut(g_vm), FadeOut(VGroup(tunnel, ssh_t))])
            self.remove(g_vm, tunnel, ssh_t)
            vo.wait_until("the disk")
            md.drop(self, P["disk"], run_time=0.4, extra=[FadeOut(g_disk)])
            self.remove(g_disk)
            vo.wait_until("the firewalls")
            self.play(FadeOut(gates), FadeOut(VGroup(*g_gates)), run_time=0.4)
            self.remove(gates, *g_gates)
            vo.wait_until("and the network")
            self.play(FadeOut(net), FadeOut(g_net), run_time=0.5)
            self.remove(net, g_net)
            self.play(Indicate(P["state"], color=OWN, scale_factor=1.08), run_time=0.7)
            md.heal(self)

        # ========================================================== 3. which folder; images retained
        def folder_card(name, note_text, color):
            row = VGroup(folder_icon(0.4, OWN), mono(name, 22, INK)).arrange(RIGHT, buff=0.18)
            nt = label(note_text, 20, color)
            inner = VGroup(row, nt).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
            fr = outline_box(5.2, inner.height + 0.45, color, solid=True, fill_opacity=0.08)
            inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
            g = VGroup(fr, inner)
            g.frame, g.note = fr, nt
            return g

        ca = folder_card("deploy_single_vm", "destroys the VM", OWN).move_to([-3.75, 1.0, 0])
        tick_a = check_glyph(0.36, OWN).move_to(ca.frame.get_right() + LEFT * 0.45)
        cb = folder_card("deploy_images", "only forgets the images", TURN).move_to([-3.75, -0.7, 0])
        err = erratum_tag("the README doesn't say which folder").next_to(cb, DOWN, buff=0.4).align_to(cb, LEFT)
        tp = TimestampPipe()
        tp.add(tp.shelf)
        for run, x in ((1, -0.25), (2, 1.95)):
            tp.crates[run] = [crate(nm).move_to(tp.p(x, y)) for nm, y in zip(SHELF, tp.ROW_Y)]
            tp.add(*tp.crates[run])
        tp.run_n = 2
        tp.shift(RIGHT * 3.25 + DOWN * 0.3)
        keep = mono("retain_on_delete", 20, COST).next_to(tp.shelf.frame, DOWN, buff=0.2)
        link = DashedLine(cb.frame.get_right(), tp.shelf.frame.get_left() + DOWN * 0.6, color=TURN,
                          stroke_width=3, dash_length=0.12)
        assert ca.get_right()[0] < tp.shelf.frame.get_left()[0] - 0.3, (ca.get_right(), tp.shelf.frame.get_left())
        assert tp.shelf.get_top()[1] < PIC_TOP and tp.shelf.get_right()[0] < 6.55, tp.shelf.get_corner(UR)
        assert ca.get_top()[1] < PIC_TOP and err.get_bottom()[1] > -3.5 and keep.get_bottom()[1] > -3.5
        # GOLD padlocks straddling each crate's top edge at its right end (clear of the crate's name;
        # TimestampPipe.retain() puts them on the bottom-left corner, over the name's first letter)
        locks = []
        for run in (1, 2):
            for c in tp.crates[run]:
                lk = padlock(0.3, COST).move_to(c.box.get_corner(UR) + np.array([-0.2, 0.02, 0]))
                assert lk.get_bottom()[1] > c.text.get_top()[1] + 0.03 or lk.get_left()[0] > c.text.get_right()[0] + 0.03
                locks.append(lk)
        assert tick_a.get_left()[0] > ca.note.get_right()[0] + 0.2 and tick_a.get_left()[0] > ca[1][0].get_right()[0] + 0.2
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(md), run_time=0.4)
            self.remove(md)
            self.play(FadeIn(ca, shift=RIGHT * 0.2), FadeIn(err, shift=UP * 0.1), run_time=0.6)
            self.play(Create(tick_a), run_time=0.4)
            vo.wait_until("in deploy images it only forgets")
            self.play(FadeIn(cb, shift=RIGHT * 0.2), run_time=0.5)
            self.play(Indicate(cb.note, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("which stay in the registry")
            self.play(FadeIn(tp), Create(link), run_time=0.7)
            vo.wait_until("retained on delete")
            self.play(LaggedStart(*[FadeIn(lk, scale=1.4) for lk in locks], lag_ratio=0.1), run_time=0.7)
            self.play(FadeIn(keep, shift=UP * 0.1), run_time=0.4)

        # ========================================================== 4-5. the teardown checklist
        items = teardown_items()
        cl = Checklist("Teardown checklist", items, color=COST, tag_text=None)
        cl.move_to([0, -0.3, 0])
        ctag = cost_tag("billed until deleted")
        ctag.move_to(cl.frame.get_corner(UR) + np.array([-ctag.width / 2 - 0.3, 0, 0]))
        assert cl.width < 12.9 and cl.get_top()[1] < 3.3 and cl.get_bottom()[1] > -3.5, (cl.width, cl.get_top(), cl.get_bottom())
        assert ctag.get_left()[0] > cl.head.get_right()[0] + 0.3
        cl.add(ctag)                    # part of the piece: it stays on top of the frame as rows are added
        rows = list(cl.rows)
        cl.rows.remove(*rows)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(ca, tick_a, cb, err, tp, keep, link, *locks)), FadeOut(trk), run_time=0.5)
            self.remove(ca, tick_a, cb, err, tp, keep, link, trk, *locks)
            self.play(FadeIn(cl, shift=DOWN * 0.1), run_time=0.6)
            for i, (a, b) in enumerate((("One:", "and check the VM list"), ("Two:", "delete the registry"),
                                        ("Three:", "last, once no stack"))):
                vo.wait_until(a)
                if i == 2:
                    rows[2].text[2].save_state().set_opacity(0)      # 'after … deploy_images too' comes in at "once no stack"
                cl.show(self, rows[i], anims=[FadeIn(rows[i], shift=RIGHT * 0.15)], run_time=0.5, into=cl.rows)
                vo.wait_until(b)
                if i == 2:
                    self.play(Indicate(rows[2].text[1][1], color=COST, scale_factor=1.15), run_time=0.5)
                    cl.heal(self)
                    vo.wait_until("once no stack")
                    self.play(rows[2].text[2].animate.restore(), run_time=0.5)
                    cl.heal(self)
                cl.tick(self, i)

        with self.voiceover(SAY[5]) as vo:
            for i, (a, b) in enumerate((("Four:", "if it still runs"), ("Five:", "free and optional"),
                                        ("Six:", "both service account keys")), start=3):
                vo.wait_until(a)
                cl.show(self, rows[i], anims=[FadeIn(rows[i], shift=RIGHT * 0.15)], run_time=0.5, into=cl.rows)
                vo.wait_until(b)
                cl.tick(self, i)

        # ========================================================== 6. slide 19: six steps, V1 grows
        r19 = lref("19")
        strip = six_steps(0)
        strip.shift(DOWN * (strip.get_bottom()[1] + 3.45))
        pic = recap_picture(PIC_TOP, strip.get_top()[1] + 0.15)
        cues = ("docker-shell.sh", "deploy images", "create instance", "provision instance", "setup containers",
                "and setup webserver")
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(cl, shift=UP * 0.4), run_time=0.5)
            self.remove(cl)
            self.play(FadeIn(r19), FadeIn(strip, shift=UP * 0.2), run_time=0.6)
            for k, cue in enumerate(cues, start=1):
                vo.wait_until(cue)
                self.play(strip.goto(k), run_time=0.3)
                if k == 1:
                    self.play(FadeIn(pic["setup"], shift=RIGHT * 0.15), run_time=0.5)
                elif k == 2:
                    cr = pic["crates"]
                    starts = [c.copy().move_to(pic["toolbox"]).set_opacity(0) for c in cr]
                    self.play(FadeIn(pic["registry"]), run_time=0.3)
                    self.play(LaggedStart(*[ReplacementTransform(s, c) for s, c in zip(starts, cr)], lag_ratio=0.2),
                              run_time=0.7)
                elif k == 3:
                    self.play(FadeIn(pic["vm"], scale=0.97), GrowArrow(pic["pull"]), run_time=0.6)
                elif k == 4:
                    tl = pic["provision"]
                    self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.15) for x in tl], lag_ratio=0.1), run_time=0.6)
                    self.play(LaggedStart(*[Rotate(x, -PI / 9, about_point=x.get_corner(DR)) for x in tl],
                                          lag_ratio=0.1), run_time=0.6)
                elif k == 5:
                    src = [pic["crates"][i].copy() for i in (1, 0, 2)]      # frontend, api, vector-db images
                    self.play(*[ReplacementTransform(s, b) for s, b in zip(src, pic["containers"])], run_time=0.7)
                else:
                    self.play(FadeIn(pic["web"][0], scale=0.9), FadeIn(pic["web"][1]), run_time=0.4)
                    self.play(FadeIn(pic["web"][2], shift=DOWN * 0.2),
                              LaggedStart(*[GrowArrow(a) for a in pic["routes"]], lag_ratio=0.25), run_time=0.8)
            self.play(strip.goto(7), run_time=0.4)
            self.wait(0.8)

        # ========================================================== 7. slide 12: six principles, a scorecard
        r12 = lref("12")
        hub = tool_chip("Pulumi", size=24, mono_font=False).move_to([0, 0.3, 0])
        pchips = []
        for i, nm in enumerate(PRINCIPLES):
            c = chip(nm, S.GREY, size=22)
            y = (1.7, 0.3, -1.1)[i % 3]
            if i < 3:
                c.move_to([-1.9 - c.width / 2, y, 0])
            else:
                c.move_to([1.9 + c.width / 2, y, 0])
            pchips.append(c)
        spokes = VGroup(*[Line(hub.get_left() if i < 3 else hub.get_right(),
                               c.get_right() if i < 3 else c.get_left(), color=S.GREY, stroke_width=2)
                          for i, c in enumerate(pchips)])
        marks, note_c = [], None
        for i, (c, sc) in enumerate(zip(pchips, SCORE)):
            side = LEFT if i < 3 else RIGHT
            if sc == "yes":
                m = check_glyph(0.38, OWN).next_to(c, side, buff=0.25)
            elif sc == "no":
                m = cross_glyph(0.32, S.GREY).next_to(c, side, buff=0.25)
            else:
                m = grey_chip("many providers, one cloud").next_to(c, side, buff=0.25)
                note_c = m
            marks.append(m)
        allp = VGroup(hub, *pchips, *marks)
        VGroup(allp, spokes).shift(LEFT * (allp.get_left()[0] + allp.get_right()[0]) / 2)
        assert allp.get_left()[0] > -6.55 and allp.get_right()[0] < 6.55, (allp.get_left(), allp.get_right())
        assert allp.get_top()[1] < PIC_TOP and allp.get_bottom()[1] > -3.4
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(*pic.values()), strip), ReplacementTransform(r19, r12), run_time=0.6)
            self.remove(*pic.values(), strip)
            self.play(FadeIn(hub, scale=1.2), run_time=0.4)
            self.play(Create(spokes), LaggedStart(*[FadeIn(c, scale=0.9) for c in pchips], lag_ratio=0.15),
                      run_time=1.0)

            def score(i):
                c = pchips[i]
                if SCORE[i] == "yes":
                    return AnimationGroup(Create(marks[i]), c.box.animate.set_stroke(OWN).set_fill(OWN, 0.16),
                                          run_time=0.5)
                if SCORE[i] == "no":
                    return AnimationGroup(Create(marks[i]), c.text.animate.set_color(S.GREY), run_time=0.5)
                return AnimationGroup(FadeIn(marks[i], shift=LEFT * 0.15), run_time=0.5)

            vo.wait_until("Real language")
            self.play(score(0))
            vo.wait_until("declarative")
            self.play(score(1))
            vo.wait_until("state with previews")
            self.play(score(4))
            vo.wait_until("Components and tests")
            self.play(score(2))
            self.play(score(5))
            vo.wait_until("Many providers")
            self.play(score(3))
            self.play(Indicate(note_c, color=INK, scale_factor=1.06), run_time=0.6)

        # ========================================================== 8. slide 4: single point of failure, L21-L23
        r4 = lref("4")
        rm = roadmap()
        dep = rm.bars["Deployment, Scaling & Automation"]
        rm.marker.move_to(dep).stretch_to_fit_width(dep[0].width + 0.2)
        dep[0].set_stroke(TURN)
        assert rm.get_top()[1] < PIC_TOP, rm.get_top()
        srv = server(1.0, 3, CLOUD).move_to([-4.7, -1.75, 0])
        spof = label("single point of failure", 22, ERR).next_to(srv, DOWN, buff=0.2)
        ring_ = ring(srv, ERR, buff=0.12)
        nxt = VGroup(dashed_chip("L21 · CI/CD"), dashed_chip("L22 · Kubernetes · same toolbox, same images stack"),
                     dashed_chip("L23 · pulumi up in GitHub Actions"))
        nxt.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        nxt.move_to([dep.get_left()[0] + nxt.width / 2, -2.2, 0])
        assert nxt.get_top()[1] < rm.get_bottom()[1] - 0.15 and nxt.get_right()[0] < 6.5, (nxt.get_top(), nxt.get_right())
        assert spof.get_right()[0] < nxt.get_left()[0] - 0.2 and spof.get_bottom()[1] > -3.5, spof.get_corner(DR)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(spokes, *pchips, *marks, hub)), ReplacementTransform(r12, r4), run_time=0.5)
            self.remove(spokes, *pchips, *marks, hub)
            self.play(FadeIn(rm), run_time=0.6)
            self.play(FadeIn(srv, shift=UP * 0.2), run_time=0.4)
            vo.wait_until("single point of failure")
            self.play(Create(ring_), FadeIn(spof, shift=UP * 0.1), Indicate(srv, color=ERR, scale_factor=1.1),
                      run_time=0.8)
            for c, cue in zip(nxt, ("Lecture 21 automates", "lecture 22 moves to Kubernetes", "and lecture 23 runs")):
                vo.wait_until(cue)
                self.play(FadeIn(c, shift=RIGHT * 0.6), run_time=0.5)

        # ========================================================== 9-11. test yourself
        head = label("Test yourself", 30, TURN).move_to([-6.4, 2.55, 0], aligned_edge=LEFT)
        heads = [label(f"· {k + 1}/5", 30, TURN).next_to(head, RIGHT, buff=0.2) for k in range(5)]
        for h in heads:
            h.align_to(head, DOWN)
        qcards = [qcard(q).move_to([0, 0.15, 0]) for q in QUESTIONS]
        for q in qcards:
            assert q.get_top()[1] < head.get_bottom()[1] - 0.3 and q.get_bottom()[1] > -2.6, q.get_top()
        dots = VGroup(*[Circle(radius=0.11, stroke_color=S.GREY, stroke_width=2.5) for _ in range(5)])
        dots.arrange(RIGHT, buff=0.35).move_to([0, -2.9, 0])
        assert dots.get_top()[1] < min(q.get_bottom()[1] for q in qcards) - 0.2
        dots[0].set_fill(TURN, 1).set_stroke(TURN)
        cur = [qcards[0], heads[0]]

        def to_card(k):
            c0, h0 = cur
            nx = qcards[k]
            anims = [ReplacementTransform(c0.frame, nx.frame), FadeOut(c0.body, shift=UP * 0.2),
                     FadeIn(nx.body, shift=UP * 0.2), ReplacementTransform(h0, heads[k]),
                     dots[k - 1].animate.set_fill(S.GREY, 1).set_stroke(S.GREY),
                     dots[k].animate.set_fill(TURN, 1).set_stroke(TURN)]
            cur[0], cur[1] = nx, heads[k]
            return AnimationGroup(*anims, run_time=0.8)

        def mark(k, r):
            return Indicate(qcards[k].body[r], color=TURN, scale_factor=1.04, run_time=0.7)

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(rm, srv, spof, ring_, nxt, r4)), run_time=0.6)
            self.remove(rm, srv, spof, ring_, nxt, r4)
            self.play(FadeIn(head, shift=DOWN * 0.1), FadeIn(heads[0], shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Trace your instance IP")
            self.play(FadeIn(qcards[0], shift=UP * 0.15), FadeIn(dots, lag_ratio=0.15), run_time=0.7)
            vo.wait_until("which gate")
            self.play(mark(0, 1))
            vo.wait_until("and which character")
            self.play(mark(0, 2))

        with self.voiceover(SAY[10]) as vo:
            vo.wait_until("What three things")
            self.play(to_card(1))
            vo.wait_until("what does refresh change")
            self.play(mark(1, 1))
            vo.wait_until("and what does dash y skip")
            self.play(mark(1, 2))
            vo.wait_until("Name the two service accounts")
            self.play(to_card(2))
            vo.wait_until("where each key sits")
            self.play(mark(2, 1))
            vo.wait_until("and what each may do")
            self.play(mark(2, 2))

        ans = card(["answers: exercises.md · study guide"], S.GREY, size=24).move_to(dots)
        with self.voiceover(SAY[11]) as vo:
            vo.wait_until("Which of the six steps")
            self.play(to_card(3))
            vo.wait_until("and which does it only remember")
            self.play(mark(3, 1))
            vo.wait_until("What survives destroy")
            self.play(to_card(4))
            vo.wait_until("Answers are in")
            self.play(FadeOut(cur[0], shift=UP * 0.2), FadeOut(cur[1]), FadeOut(head), run_time=0.5)
            self.play(ReplacementTransform(dots, ans), run_time=0.5)     # after card 5: the dots become the pointer
            self.play(ans.animate.move_to([0, 0.15, 0]), run_time=0.5)
        self.wait(0.4)
        self.play(FadeOut(ans), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
