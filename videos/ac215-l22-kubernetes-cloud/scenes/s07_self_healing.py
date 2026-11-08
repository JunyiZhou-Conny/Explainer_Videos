"""S07 · Desired state: Pods that come back (AC215 L22, the full follow-along). TRACKER [W] 10 · extra
throughout (every command here is an extra on the kind stand-in). Small AsksChecklist top right for the
whole scene. Lecture: 22 · 7 (beat 0), 36 (beat 1), 18, 30 (beat 3), 13, 39 (beat 8).

Beats (script.md "## S07", one voiceover block each):
0. LECTURE 22 · 7. A small GREY redrawing of S01's night: a clock '2:00 a.m.', a cracked 'API 1' box, the
   operator sliding along a dashed SSH line to restart it by hand; on "a controller does" the operator
   figure transforms into the BLUE-greyed 'controllers' box (the box V4 uses).
1. LECTURE 22 · 36. An 11-row 20 pt toolbox terminal 'laptop · toolbox · stand-in' ('extra' and
   'stand-in: kind, not GKE' on its title bar). Line 1 of k50 typed (folds) -> TERM(k50: 2 cropped, 3, 4,
   6, 7, 9–11, columns cropped after AGE); line 2 GREY. The terminal shrinks to a 4-row strip keeping
   lines 4, 7, 10, 11; V4 (ControllerLoop) builds above: the controllers box flies into its place,
   `deployment.apps/web` (line 4) flies up into the GREEN Deployment card, `replicaset.apps/web-5cd9789488`
   (line 7) into the GREEN ReplicaSet card (hash flashes in both), the two Pod names (lines 10–11) into
   the TEAL Pods with three-colour names (hash, then suffixes flash). The terminal dims to 40 %.
2. The terminal brightens and prints TERM(k50: 20–22 wrap); `pod-template-hash=5cd9789488` YELLOW
   (with the V4 hashes), `run=web` PINK.
3. LECTURE 22 · 18, 30. The terminal shrinks to a 3-row strip. Ring 'observe → compare → act' around
   the controllers box with the counter 'desired 2 · actual 2' and a dial; the Pods flash on "observe",
   'replicas: 2' and the counter on "compare", the ring turns on "act"; the GREY caption 'you set the
   number; the controller keeps it true'; the needle swings back on "keeps it true".
4. The terminal grows back to 4 rows. Line 1 of k55 typed (folds) -> TERM(k55: 2, 7–10, 13, columns
   cropped); counter 'desired 4 · actual 2' RED, two Pods grow (gmbqz on worker, grq79 on worker2),
   counter GREEN 4·4; lane titles flash; line 13's '+ 1 more...' PINK. Line 1 of k56 typed -> TERM(k56:
   2, 4–5); the two Pods fade, counter back to 2. GREY tag 'Milestone 5 · manual scaling' beside k56.
5. Pod …-5h48s glows YELLOW (ring). The strip steps aside; PONDER(8 s) card over the right half.
6. The card goes, the strip returns. Line 1 of k53 typed (folds) -> TERM(k53: 2–5); in V4 …-5h48s is
   struck and fades, counter RED 'desired 2 · actual 1'; the new Pod …-lmk52 grows 'ContainerCreating'
   (line 5's status YELLOW); its hash flashes with line 5's, then its new suffix.
7. Line 1 of k54 typed -> TERM(k54: 2–4, columns cropped); both 'Running' GREEN; the V4 Pod turns
   'Running', counter GREEN 2·2; the ring turns on "the loop noticed, and acted".
8. LECTURE 22 · 13, 39. V4 fades; the AsksChecklist grows to the centre, 'Failover' ticks YELLOW with
   the footnote 'a restart, not a hot standby · keep replicas: 2', then shrinks back.
9. The terminal fades. Left GREY dashed card 'L20 · Docker restart policy / same machine', right GREEN
   card 'ReplicaSet / a new Pod wherever there is room', a WHITE line 'Declare, don't script.' Fade;
   empty frame.

Deviations from SHOW:
- TERM(k50: 3–4, 6–7, 9–11 wrap) and TERM(k55: 7–10 wrap), TERM(k54: 2–4 wrap): the rows are cropped
  after their AGE column instead of wrapped (as S05 crops k03–k05). Wrapped, k50 alone needs ~20 rows,
  which leaves no room for V4 above the strip; the cropped columns are IPs, nodes, images and selectors.
  The nodes of the scaled Pods are shown by V4's two worker lanes (taken from k55's NODE column); the
  labels are beat 2 (k50: 20–22, wrapped as written); the IPs are S08's.
- k50:2 (the GREY deprecation warning, not read) is cropped after 'v1.33+;' with '…': an 11-row
  terminal is the tallest that stays under the AsksChecklist corner.
- The terminal is 20 pt (72 characters a row) for the whole scene: k53's and k54's rows are 66–68
  characters.
- Beat 4: the terminal "grows back" to a 4-row strip only (V4 needs the rest of the frame), so it
  scrolls: k55's first Pod row scrolls away as line 13 arrives. 'Milestone 5 · manual scaling' is a
  row tag beside k56's 'deployment.apps/web scaled' (the command's last row is too long to hold
  it, and the caption row is under the 4-row strip's top).
- Beat 5: the 4-row strip fades for the ponder timer so the opaque card fits beside the glowing Pod,
  clear of the AsksChecklist; it returns at the start of beat 6.
- Beat 8: V4 fades before the checklist grows (the full card needs the centre); SHOW does not say when
  V4 leaves.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S07"]
assert len(SAY) == SAY_COUNT["S07"] == 10

# ------------------------------------------------------------------ the real sources (checked)
K50, K53, K54, K55, K56 = (capture(k) for k in ("k50", "k53", "k54", "k55", "k56"))
POD_A, POD_B = (f"web-{RS_HASH}-{s}" for s in POD_SUFFIXES)
POD_NEW = f"web-{RS_HASH}-{NEW_SUFFIX}"
POD_S1, POD_S2 = (f"web-{RS_HASH}-{s}" for s in SCALE_SUFFIXES)

assert K50.cmd.startswith("kubectl get deployment,replicaset,pods,service,endpoints -o wide;")
assert K50.line(2).startswith("Warning: v1 Endpoints is deprecated")
assert K50.line(4).startswith("deployment.apps/web ")
assert K50.line(7).startswith(f"replicaset.apps/web-{RS_HASH} ")
assert K50.line(10).startswith(f"pod/{POD_A} ") and "test-cluster-worker2" in K50.line(10)
assert K50.line(11).startswith(f"pod/{POD_B} ") and K50.line(11).split()[6] == "test-cluster-worker"
assert K50.line(20).split()[-1] == "LABELS"
assert K50.line(21).startswith(POD_A) and K50.line(21).endswith(f"pod-template-hash={RS_HASH},run=web")
assert K50.line(22).startswith(POD_B) and K50.line(22).endswith(f"pod-template-hash={RS_HASH},run=web")
assert K55.cmd.startswith("kubectl scale deployment web --replicas=4;")
assert K55.line(2) == "deployment.apps/web scaled"
assert [K55.line(n).split()[0] for n in (7, 8, 9, 10)] == [POD_A, POD_B, POD_S1, POD_S2]
assert K55.line(9).split()[6] == "test-cluster-worker" and K55.line(10).split()[6] == "test-cluster-worker2"
assert K55.line(13).startswith("web ") and "+ 1 more..." in K55.line(13)
assert K56.cmd.startswith("kubectl scale deployment web --replicas=2;")
assert K56.line(2) == "deployment.apps/web scaled"
assert [K56.line(n).split()[0] for n in (4, 5)] == [POD_A, POD_B]
assert K53.cmd == f"kubectl delete pod {POD_A}; kubectl get pods -l run=web"
assert K53.line(2).startswith(f'pod "{POD_A}" deleted')
assert K53.line(5).split()[:3] == [POD_NEW, "0/1", "ContainerCreating"]
assert K54.cmd == "kubectl get pods -l run=web -o wide"
assert K54.line(3).split()[:3] == [POD_B, "1/1", "Running"]
assert K54.line(4).split()[:3] == [POD_NEW, "1/1", "Running"] and K54.line(4).split()[6] == "test-cluster-worker2"


def to_age(cap, n: int) -> str:
    """A kubectl row cropped after its AGE column (the header's 'AGE', a Pod row's age)."""
    f = cap.line(n).split()
    word = "AGE" if f[0] == "NAME" else f[4]
    return cap.crop(n, word)


def bar_follow(t, tags, rows: int):
    """ANIMs: tags on terminal t's title bar move with the bar when t is resized to `rows`."""
    top = BOTTOM + rows * t.pitch + 0.85
    return [g.animate.move_to([g.get_x(), top - t.bar_h / 2, 0]) for g in tags]


def glyphs_of(t):
    """Every glyph currently in terminal t (folded commands included), for dimming."""
    gs = []
    for ln in t.lines:
        for r in rows_of(ln):
            gs.extend(r.glyphs.submobjects)
    return VGroup(*gs)


def suffix_of(pg):
    """The TEAL suffix glyphs of a V4 Pod's three-colour name."""
    txt = pg.name.text
    return txt[len(f"web-{RS_HASH}-"):]


class SelfHealing(VoiceScene):
    def construct(self):
        trk = tracker_w(10, True)
        ac = AsksChecklist(small=True)

        # ========================================================== 0. who restarts it? a controller
        ref = lref("7")
        clk = clock_face(0.34, S.GREY).move_to([-4.9, 1.6, 0])
        clk_t = label("2:00 a.m.", 22, S.GREY).next_to(clk, RIGHT, buff=0.18)
        api = boxed("API 1", S.GREY, box_w=1.8, box_h=0.7).move_to([1.7, 0.1, 0])
        crack = VMobject(stroke_color=ERR, stroke_width=4).set_points_as_corners(
            [api.get_top() + LEFT * 0.12, api.get_center() + RIGHT * 0.14, api.get_center() + LEFT * 0.1,
             api.get_bottom() + RIGHT * 0.08])
        op = you("the operator").move_to([-4.9, 0.0, 0])
        ssh = DashedLine([-4.3, -0.55, 0], [api.get_left()[0], -0.55, 0], color=S.GREY, stroke_width=3,
                         dash_length=0.12)
        ssh_t = label("SSH · restart by hand", 20, S.GREY).next_to(ssh, DOWN, buff=0.12)
        cl = ControllerLoop()
        ctl0 = cl.ctl.copy().move_to([-1.0, 0.1, 0])
        park = np.array([1.6, 2.2, 0])
        t = term(toolbox_prompt(), 11, T_TB_STANDIN, size=20)
        assert t.box.get_top()[1] < min(park[1] - 0.4, ac.get_bottom()[1] - 0.1), t.box.get_top()
        sr = on_bar(t, standin_row())
        er = extra_row()
        er.move_to([t.dots.get_right()[0] + 0.3 + er.width / 2, sr.get_y(), 0])
        assert er.get_right()[0] < t.title.get_left()[0] - 0.1 and sr.get_left()[0] > t.title.get_right()[0] + 0.1
        t.add(sr, er)
        bar_tags = [sr, er]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ac), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(clk), FadeIn(clk_t), FadeIn(api), FadeIn(op), run_time=0.6)
            self.play(Create(crack), Rotate(clk.hands[1], -0.6, about_point=clk[0].get_center()),
                      run_time=0.6)
            vo.wait_until("who restarts the container")
            self.play(Create(ssh), FadeIn(ssh_t), run_time=0.5)
            self.play(op.animate.move_to([-1.0, 0.0, 0]), run_time=0.8)
            self.play(FadeOut(crack), api.frame.edge.animate.set_stroke(INK), run_time=0.4)
            self.play(api.frame.edge.animate.set_stroke(S.GREY), run_time=0.3)
            self.remove(crack)
            vo.wait_until("In Kubernetes, a controller does")
            self.play(ReplacementTransform(op, ctl0), FadeOut(ssh), FadeOut(ssh_t), run_time=0.9)
            self.remove(ssh, ssh_t)
            vo.wait_until("Let's watch one work")
            self.play(Indicate(ctl0, color=CLOUD, scale_factor=1.12), run_time=0.7)
            self.play(FadeOut(VGroup(clk, clk_t, api)), ctl0.animate.move_to(park), FadeIn(t, shift=UP * 0.2),
                      run_time=0.6)
            self.remove(clk, clk_t, api)
        self.play(FadeOut(ref), run_time=0.2)
        self.remove(ref)

        # ========================================================== 1. k50: the chain, into V4
        ref = lref("36")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(ref), run_time=0.3)
            type_capture(self, t, K50, type_time=0.6)
            g = out(self, t, [(K50.crop(2, "v1.33+;", "…"), S.GREY)] + [to_age(K50, n) for n in (3, 4, 6, 7, 9, 10, 11)],
                    wrap=True, run_time=0.6)
            by = {n: r for n, r in zip((4, 7, 10, 11), (g[2], g[4], g[6], g[7]))}
            assert by[4].text.startswith("deployment.apps/web") and by[10].text.startswith("pod/" + POD_A)
            vo.wait_until("The Deployment named web")
            d4 = substring(by[4], "deployment.apps/web")
            self.play(d4.animate.set_color(OWN), run_time=0.3)
            self.play(Indicate(d4, color=OWN, scale_factor=1.1), run_time=0.5)
            self.add(t)
            resize(self, t, 4, keep=list(by.values()),
                   extra=[*bar_follow(t, bar_tags, 4), FadeIn(cl.lanes), ctl0.animate.move_to(cl.ctl)], run_time=0.7)
            self.remove(ctl0, cl.lanes)
            self.add(cl)
            cl.deployment(self, src=d4)
            vo.wait_until("owns a ReplicaSet")
            cl.replicaset(self, src=substring(by[7], f"replicaset.apps/web-{RS_HASH}"))
            vo.wait_until("whose name adds a hash")
            rs_hash = cl.rs.rows[1][4:]
            self.play(Indicate(rs_hash, color=OWN, scale_factor=1.15),
                      Indicate(substring(by[7], RS_HASH), color=OWN, scale_factor=1.15), run_time=0.8)
            self.add(t, cl)
            vo.wait_until("The ReplicaSet owns two Pods")
            cl.pods(self, srcs=(substring(by[10], POD_A), substring(by[11], POD_B)))
            pa, pb = cl.pod_map[POD_SUFFIXES[0]], cl.pod_map[POD_SUFFIXES[1]]
            vo.wait_until("each with that hash")
            self.play(each([pa.name.hash, pb.name.hash], OWN, 1.15), run_time=0.8)
            self.add(cl)
            vo.wait_until("and a short random suffix")
            self.play(each([suffix_of(pa), suffix_of(pb)], POD, 1.2), run_time=0.8)
            self.add(cl)
            self.play(glyphs_of(t).animate.set_opacity(0.4), run_time=0.4)
            self.add(t)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 2. the labels (k50: 20-22)
        with self.voiceover(SAY[2]) as vo:
            self.play(glyphs_of(t).animate.set_opacity(1), run_time=0.4)
            self.add(t)
            g2 = out(self, t, K50.at(20, 21, 22), wrap=True, run_time=0.6)
            lab = [r for r in g2 if "pod-template-hash=" in r.text]
            assert len(lab) == 2, [r.text for r in g2]
            vo.wait_until("every Pod carries the template hash")
            hs = [substring(r, f"pod-template-hash={RS_HASH}") for r in lab]
            self.play(*[h.animate.set_color(TURN) for h in hs], run_time=0.4)
            self.play(each(hs, TURN, 1.06), Indicate(pa.name.hash, color=TURN), Indicate(pb.name.hash, color=TURN),
                      run_time=0.9)
            self.add(t, cl)
            vo.wait_until("and the run web label")
            rw = [substring(r, "run=web") for r in lab]
            self.play(*[w.animate.set_color(ROUTE) for w in rw], run_time=0.4)
            self.play(each(rw, ROUTE, 1.12), run_time=0.7)
            self.add(t)

        # ========================================================== 3. the loop: observe, compare, act
        ref = lref("18, 30")
        with self.voiceover(SAY[3]) as vo:
            resize(self, t, 3, extra=[FadeIn(ref), *bar_follow(t, bar_tags, 3)], run_time=0.6)
            vo.wait_until("runs a loop")
            cl.loop(self)
            vo.wait_until("observe the Pods")
            self.play(each([pa.circle, pb.circle], POD, 1.3), run_time=0.8)
            self.add(cl)
            vo.wait_until("compare with the number you declared")
            self.play(Indicate(cl.dep.rows[1], color=OWN, scale_factor=1.15),
                      Indicate(cl.counter, color=OWN, scale_factor=1.1), run_time=0.9)
            self.add(cl)
            vo.wait_until("act on the difference")
            cl.spin(self)
            vo.wait_until("You set the number")
            cl.caption(self)
            vo.wait_until("the controller keeps it true")
            cl.needle(self)
            vo.wait_until("like a thermostat")
            cl.needle(self)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 4. scale to 4 and back (k55, k56)
        with self.voiceover(SAY[4]) as vo:
            cl.clear_caption(self)
            resize(self, t, 4, extra=bar_follow(t, bar_tags, 4), run_time=0.5)
            vo.wait_until("kubectl scale")
            type_capture(self, t, K55, type_time=1.2)
            vo.wait_until("Two more Pods appear")
            cl.count(self, 4, 2)
            out(self, t, [K55.line(2)] + [to_age(K55, n) for n in (7, 8, 9, 10)], run_time=0.6)
            cl.pod(self, SCALE_SUFFIXES[0], 1)
            cl.pod(self, SCALE_SUFFIXES[1], 0)
            cl.count(self, 4, 4)
            vo.wait_until("spread over both workers")
            self.play(each([ln.title for ln in cl.lanes], CLOUD, 1.15), run_time=0.8)
            self.add(cl)
            vo.wait_until("and the Service already lists them")
            e13 = out(self, t, [K55.crop(13, "+ 1 more...")], run_time=0.4)[0]
            more = substring(e13, "+ 1 more...")
            self.play(more.animate.set_color(ROUTE), run_time=0.3)
            self.play(Indicate(more, color=ROUTE, scale_factor=1.15), run_time=0.6)
            self.add(t)
            vo.wait_until("Scale back to 2")
            type_capture(self, t, K56, type_time=0.9)
            g56 = out(self, t, K56.at(2, 4, 5), run_time=0.5)
            cl.count(self, 2, 4)
            cl.remove_pod(self, SCALE_SUFFIXES[0])
            cl.remove_pod(self, SCALE_SUFFIXES[1])
            cl.count(self, 2, 2)
            vo.wait_until("remember this command")
            ms = row_tag("Milestone 5 · manual scaling")
            pin(self, g56[0], beside(ms, g56[0]))
            flash_tag(self, ms, INK)

        # ========================================================== 5. ponder: delete one Pod
        pg_a = cl.pod_map[POD_SUFFIXES[0]]
        glow = ring(pg_a, TURN, buff=0.08, stroke=4)
        with self.voiceover(SAY[5]) as vo:
            vo.wait_until("Now delete one of the two web Pods")
            self.play(Create(glow), pg_a.circle.animate.set_stroke(TURN), run_time=0.6)
            self.play(Indicate(pg_a.name, color=TURN, scale_factor=1.08), run_time=0.7)
            self.add(cl)
            self.bring_to_front(glow)
            vo.wait_until("how many web Pods are there")
            self.play(Indicate(cl.counter, color=TURN, scale_factor=1.1), run_time=0.7)
            self.add(cl)
            self.bring_to_front(glow)
            vo.wait_until("which part of the new name stays the same")
            self.play(Indicate(pg_a.name.hash, color=TURN, scale_factor=1.15), run_time=0.7)
            self.add(cl)
            self.bring_to_front(glow)
        self.play(FadeOut(t), run_time=0.4)
        self.remove(t)
        pw = 7.4
        px = pg_a.name.get_right()[0] + 0.3 + pw / 2
        assert px + pw / 2 < 6.5, px
        card_ = ponder(self, "Delete one of the two web Pods.\nA second later: how many?\n"
                             "Which part of the new name\nstays the same?", 8, center=(px, -1.0), width=pw)
        assert card_.get_top()[1] < ac.get_bottom()[1] - 0.1 and card_.get_bottom()[1] > -3.55, card_.get_top()

        # ========================================================== 6. it comes back (k53)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(card_), FadeIn(t), run_time=0.5)
            self.remove(card_)
            type_capture(self, t, K53, type_time=0.9)
            vo.wait_until("The delete returns")
            out(self, t, K53.at(2), run_time=0.3)
            self.remove(glow)
            cl.kill(self, POD_SUFFIXES[0])
            vo.wait_until("a new Pod is already being created")
            g6 = out(self, t, K53.at(3, 4, 5), run_time=0.4)
            cc = substring(g6[-1], "ContainerCreating")
            self.play(cc.animate.set_color(TURN), run_time=0.3)
            pn = cl.respawn(self)
            vo.wait_until("Its name keeps the ReplicaSet hash")
            self.play(Indicate(pn.name.hash, color=OWN, scale_factor=1.2),
                      Indicate(substring(g6[-1], RS_HASH), color=OWN, scale_factor=1.15), run_time=0.8)
            self.add(t, cl)
            vo.wait_until("with a new suffix")
            self.play(Indicate(suffix_of(pn), color=POD, scale_factor=1.25),
                      Indicate(substring(g6[-1], NEW_SUFFIX), color=POD, scale_factor=1.2), run_time=0.8)
            self.add(t, cl)

        # ========================================================== 7. both run (k54)
        with self.voiceover(SAY[7]) as vo:
            type_capture(self, t, K54, type_time=0.6)
            g7 = out(self, t, [to_age(K54, n) for n in (2, 3, 4)], run_time=0.4)
            vo.wait_until("both run")
            runs = [substring(g7[i], "Running") for i in (1, 2)]
            self.play(*[r.animate.set_color(OWN) for r in runs], run_time=0.3)
            cl.status(self, NEW_SUFFIX, "Running")
            cl.count(self, 2, 2)
            self.play(each(runs, OWN, 1.15), run_time=0.6)
            self.add(t)
            vo.wait_until("Nobody logged in")
            self.play(Indicate(cl.ctl, color=CLOUD, scale_factor=1.1), run_time=0.6)
            self.add(cl)
            vo.wait_until("the loop noticed, and acted")
            cl.spin(self, run_time=1.2)

        # ========================================================== 8. failover, ticked (honestly)
        ref = lref("13, 39")
        NOTE = "a restart, not a hot standby · keep replicas: 2"
        probe = AsksChecklist()
        w0 = probe.card.frame.width
        off = probe.card.rows[0].note.get_left()[0] - probe.card.frame.get_left()[0]
        w1 = max(w0, off + label(NOTE, 20).width + 0.4)
        cx = -(w1 - w0) / 2
        assert cx - w0 / 2 > -6.5 and cx - w0 / 2 + w1 < 3.6, (cx, w0, w1)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(cl), FadeIn(ref), run_time=0.5)
            self.remove(cl)
            ac.grow(self, center=(cx, 0.7))
            vo.wait_until("That ticks failover")
            fr = ac.card.frame
            wide = RoundedRectangle(width=w1, height=fr.height, corner_radius=0.14, stroke_color=TURN,
                                    stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
            wide.move_to(fr).align_to(fr, LEFT)
            self.play(Transform(fr, wide), run_time=0.4)
            ac.heal(self)
            ac.tick(self, 0, note=NOTE)
            vo.wait_until("it is a restart, not a hot standby")
            nt = ac.card.rows[0].note
            self.play(Indicate(nt, color=INK, scale_factor=1.06), run_time=0.7)
            self.add(ac)
            vo.wait_until("With one replica there is a short gap")
            self.play(Indicate(ac.card.rows[0].text, color=TURN, scale_factor=1.1), run_time=0.7)
            self.add(ac)
            vo.wait_until("why the game's file asks for two replicas")
            self.play(Indicate(nt, color=OWN, scale_factor=1.06), run_time=0.7)
            self.add(ac)
            ac.shrink(self)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 9. declare, don't script
        left = card([label("L20 · Docker restart policy", 26, INK), label("same machine", 24, S.GREY)],
                    PAST, dashed=True)
        right = card([label("ReplicaSet", 26, INK), label("a new Pod wherever there is room", 24, INK)], OWN)
        left.move_to([-3.75, 0.5, 0])
        right.move_to([2.75, 0.5, 0])
        arr = arrow(left.get_right(), right.get_left(), S.GREY, buff=0.15)
        assert left.get_right()[0] < right.get_left()[0] - 0.3 and right.get_right()[0] < 6.5, right.get_right()
        assert right.get_top()[1] < ac.get_bottom()[1] - 0.1, (right.get_top(), ac.get_bottom())
        motto = label("Declare, don't script.", 32, INK).move_to([0, -1.3, 0])
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(t), run_time=0.4)
            self.remove(t)
            vo.wait_until("In lecture 20")
            self.play(FadeIn(left, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("A ReplicaSet places a new Pod")
            self.play(GrowArrow(arr), FadeIn(right, shift=RIGHT * 0.3), run_time=0.8)
            vo.wait_until("Declare the result")
            self.play(Write(motto), run_time=0.9)
            self.play(Indicate(motto, color=OWN, scale_factor=1.05), run_time=0.7)

        self.play(FadeOut(VGroup(trk, ac, left, right, arr, motto)), run_time=0.6)
        self.remove(trk, ac, left, right, arr, motto)
        self.wait(0.4)
