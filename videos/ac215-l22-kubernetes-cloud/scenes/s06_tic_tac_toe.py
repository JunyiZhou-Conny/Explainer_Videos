"""S06 · Two objects: a Deployment and a Service (AC215 L22, the full follow-along). TRACKER [W] 8
(beats 0-3), 8 · extra (beat 4), 9 (beats 5-7), 10 (beat 8), 10 · extra (beat 9). Lecture: 22 · 38–39
(beats 0-1), 24–25 (beat 3), 38 (beat 5), 24 (beat 7), 29 (beat 9).

Beats (script.md "## S06", one voiceover block each):
0. TRACKER [W] 8. LECTURE 22 · 38–39. V3 LabelLink, picture first: the GREEN card 'Deployment · web ·
   keep 2' emits two TEAL Pods, each gets a PINK sticker 'run: web'; the PINK door 'Service · web · :80'
   throws a lasso around both. On "The Deployment says" the picture slides down into a strip under the
   panels and the card TransformFromCopy's into CODE(deploy-k8s-tic-tac-toe.yml: 3–14) on the left
   (GREEN bracket 'Deployment: what runs in a Pod, how many copies, keep them running'); on "The Service
   says" the door does the same into CODE(…: 24–35) on the right (PINK bracket 'Service: how traffic
   reaches them; lets Pods die').
1. LECTURE (held). Line 7 'replicas: 2' GREEN; lines 9–10 and 13–14 PINK on the left, 33–34 PINK on
   the right; a GREY chip 'slide 39 trims these lines' with the erratum tag. The stickers and the lasso
   in the strip Indicate together with lines 13–14 and 33–34.
2. The left panel scrolls to CODE(…: 15–22): line 17 'dlops/tic-tac-toe' TEAL, line 21
   'containerPort: 8080' PINK. The strip leaves; a PINK path of three ports draws under the panels, each
   chip rising from its line: 'port: 80' (30) → 'targetPort: 8080' (32) → 'containerPort: 8080' (21).
3. The panels fade. A 3-row toolbox strip ('laptop · toolbox · stand-in', stand-in tag on its bar);
   V1 (stand-in) above. `kubectl apply -f deploy-k8s-tic-tac-toe.yml` → TERM(k10: 2–3) GREEN. LECTURE 22 ·
   24–25 on "Apply only hands a wish": a GREEN card rides kubectl → API server → etcd; the scheduler
   picks the two workers; the kubelets flash and two TEAL Pods start.
4. TRACKER [W] 8 · extra. V1 fades, the terminal grows to 12 rows. Line 1 of k12 (extra; folds) →
   TERM(k12: 2–4 wrap, 6 wrap, 7 wrap), each line on its phrase; the NODE column of lines 6–7 YELLOW.
5. TRACKER [W] 9. LECTURE 22 · 38. The terminal clears; `kubectl get services` → TERM(k11: 2–4). On line
   4: 'LoadBalancer' BLUE, '<pending>' YELLOW, '80:31366/TCP' PINK, with three PINK labels beneath it,
   one per phrase: '80 outside', '31366 on every node', '8080 in the Pod'.
6. `kubectl get services` again → TERM(k13: 4); '43s' and '<pending>' YELLOW. The terminal shrinks to
   the strip (k11's '0s' line stays above k13's for comparison); V1 (stand-in) above, all lamps dark.
   PONDER (8 s): the question card, opaque, over V1.
7. LECTURE 22 · 24. The controllers lamp lights YELLOW; the PINK controllers → cloud provider arrow turns
   RED; the strip leaves and a GREY chip 'kind: no cloud here' sits under the laptop column; a GREY
   dashed chip 'on GKE: a load balancer and an IP, after a short wait' under the cluster.
8. TRACKER [W] 10. A schematic browser (illustration) at http://<EXTERNAL-IP> with the 3 × 3 grid of
   empty squares; README card 'README.md · lines 574–575'; a YELLOW '▶ your turn' beside the address bar.
9. TRACKER [W] 10 · extra. Toolbox terminal (8 rows, 'extra' and stand-in tags on its bar). Line 1 of
   k57 (extra; folds) → TERM(k57: 2, 13, 14); 'HTTP/1.1 200 OK' GREEN. LECTURE 22 · 29: a GREY chip with
   the erratum tag 'a port-forward started in the toolbox opens inside the toolbox → test it with curl
   there' above the terminal. Fade; empty frame.

Deviations from SHOW:
- Beat 0: the picture slides down (no scaling: text stays >= 20 pt) instead of shrinking. The code
  panels are 20 pt and their header shows the file name 'deploy-k8s-tic-tac-toe.yml' (the full
  'src/deployment/…' header is 8.3 units wide: two panels side by side could not fit). The brackets
  are drawn inside each panel's free right side, as four short rows.
- Beat 2: the LabelLink strip leaves when the port path draws (the path takes its place under the
  panels).
- Beats 3–9: the terminal is 20 pt and 13.0 wide (74 characters a row) so that k11/k13's 73-character
  Service rows print whole (the AGE column is the point of beat 6). V1 leaves while k12's 11 rows print
  (beat 4) and returns in beat 6.
- Beat 6: the YELLOW question is the ponder card itself (opaque, over V1); during the SAY the
  YELLOW-highlighted '43s' / '<pending>' carry the question.
- Beat 7: the 'no cloud here' chip and the GKE ghost sit in the row under V1 (the strip leaves for
  them): V1 has no free room beside its cloud arrow. The ghost is a dashed chip (no second arrow).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S06"]
assert len(SAY) == SAY_COUNT["S06"] == 10

# ------------------------------------------------------------------ the real sources (checked)
YML = "src/deployment/deploy-k8s-tic-tac-toe.yml"
YML_SHOWN = "deploy-k8s-tic-tac-toe.yml"
K10, K11, K12, K13, K57 = (capture(k) for k in ("k10", "k11", "k12", "k13", "k57"))

_Y = excerpt(YML, 1, 35).split("\n")
assert _Y[6] == "  replicas: 2" and _Y[8].strip() == "matchLabels:" and _Y[9].strip() == "run: web"
assert _Y[12].strip() == "labels:" and _Y[13].strip() == "run: web"
assert _Y[16].strip() == "- image: dlops/tic-tac-toe" and _Y[20].strip() == "- containerPort: 8080"
assert _Y[29].strip() == "- port: 80" and _Y[31].strip() == "targetPort: 8080"
assert _Y[32].strip() == "selector:" and _Y[33].strip() == "run: web"
assert K10.cmd == readme(565) == "kubectl apply -f deploy-k8s-tic-tac-toe.yml"
assert K10.at(2, 3) == ["deployment.apps/web created", "service/web created"]
assert K11.cmd == K13.cmd == readme(570) == "kubectl get services"
assert K11.line(4).split()[:4] == ["web", "LoadBalancer", "10.96.52.79", "<pending>"]
assert "80:31366/TCP" in K11.line(4) and K11.line(4).endswith("0s")
assert K13.line(4).endswith("43s") and "<pending>" in K13.line(4)
assert K12.cmd == "kubectl rollout status deployment/web --timeout=300s; kubectl get pods -o wide"
assert "0 of 2" in K12.line(2) and "1 of 2" in K12.line(3) and "successfully rolled out" in K12.line(4)
assert "test-cluster-worker2" in K12.line(6) and "test-cluster-worker " in K12.line(7)
assert K57.cmd.startswith("kubectl port-forward service/web 8080:80")
assert K57.line(2) == "HTTP/1.1 200 OK" and K57.line(13) == "<!DOCTYPE html>"
assert K57.line(14).startswith("Forwarding from 127.0.0.1:8080")
VIEW_README = readme_lines(574, 575)
assert "External IP" in VIEW_README and "EXTERNAL IP" in VIEW_README, VIEW_README

TW = 13.0                    # terminal width: 74 characters a row at 20 pt (k11's rows are 73)


def tterm(rows: int) -> Terminal:
    """The stand-in toolbox terminal of this scene (20 pt, 13.0 wide)."""
    return term(toolbox_prompt(), rows, T_TB_STANDIN, size=20, width=TW)


def bar_follow(t, tg, rows: int):
    """ANIM: a tag on terminal t's title bar moves with the bar when t is resized to `rows`."""
    top = BOTTOM + rows * t.pitch + 0.85
    return tg.animate.move_to([tg.get_x(), top - t.bar_h / 2, 0])


def bracket(panel, color, rows):
    """A bracket inside a code panel's free right side: a `color` line along the code, its rows
    (first row in `color`) beside it."""
    c = panel.code
    x = c.get_right()[0] + 0.25
    top, bot = c.get_top()[1] - 0.12, c.get_bottom()[1] + 0.12
    ln = VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(
        [[x - 0.14, top, 0], [x, top, 0], [x, bot, 0], [x - 0.14, bot, 0]])
    txt = VGroup(*[label(r, 20, color if i == 0 else INK) for i, r in enumerate(rows)])
    txt.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    txt.next_to(ln, RIGHT, buff=0.2).align_to([0, top - 0.05, 0], UP)
    g = VGroup(ln, txt)
    g.line, g.text = ln, txt
    return g


def bars(panel, ks, color):
    """Translucent line bars over code lines ks (0-based) of a panel."""
    return VGroup(*[line_bar(panel.code, k, color, opacity=0.22) for k in ks])


class TicTacToe(VoiceScene):
    def construct(self):
        # ========================================================== 0. the picture, then the real file
        trk = tracker_w(8)
        ref = lref("38–39")
        ll = LabelLink()
        ll.shift(UP * 0.35)
        pl = code(YML, 3, 14, font_size=20, shown=YML_SHOWN)
        pr = code(YML, 24, 35, font_size=20, shown=YML_SHOWN)
        pl.align_to([-6.45, 0, 0], LEFT).align_to([0, 2.8, 0], UP)
        pr.align_to([6.45, 0, 0], RIGHT).align_to([0, 2.8, 0], UP)
        assert pl.get_right()[0] < pr.get_left()[0] - 0.3, (pl.get_right(), pr.get_left())
        br_l = bracket(pl, OWN, ["Deployment:", "what runs in a Pod,", "how many copies,", "keep them running"])
        br_r = bracket(pr, ROUTE, ["Service:", "how traffic", "reaches them;", "lets Pods die"])
        assert br_l.get_right()[0] < pr.get_left()[0] - 0.15, br_l.get_right()
        assert br_r.get_right()[0] < 6.5, br_r.get_right()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref), run_time=0.5)
            vo.wait_until("The warm-up deploys a small game")
            ll.deployment(self)
            vo.wait_until("tic-tac-toe")
            ll.make_pods(self)
            vo.wait_until("from one file with two objects")
            ll.stickers(self)
            ll.service(self)
            ll.lasso(self)
            vo.wait_until("The Deployment says")
            strip_dy = (min(pl.get_bottom()[1], pr.get_bottom()[1]) - 0.08) - ll.get_top()[1]
            self.play(ll.animate.shift(UP * strip_dy), run_time=0.6)
            assert ll.get_bottom()[1] > -3.6, ll.get_bottom()
            self.play(FadeTransform(ll.card.copy(), pl), run_time=0.9)
            vo.wait_until("what runs in a Pod")
            self.play(Create(br_l.line), FadeIn(br_l.text[:2]), run_time=0.5)
            vo.wait_until("how many copies")
            self.play(FadeIn(br_l.text[2]), run_time=0.3)
            vo.wait_until("and to keep them running")
            self.play(FadeIn(br_l.text[3]), run_time=0.3)
            vo.wait_until("The Service says")
            self.play(FadeTransform(ll.svc.copy(), pr), run_time=0.9)
            vo.wait_until("how traffic reaches them")
            self.play(Create(br_r.line), FadeIn(br_r.text[:3]), run_time=0.5)
            vo.wait_until("and lets Pods die")
            self.play(FadeIn(br_r.text[3]), run_time=0.3)
            self.play(Indicate(br_r.text[3], color=ROUTE, scale_factor=1.08), run_time=0.6)

        # ========================================================== 1. the glue: run: web
        rep = bars(pl, (4,), OWN)
        glue_l = bars(pl, (6, 7, 10, 11), ROUTE)
        glue_r = bars(pr, (9, 10), ROUTE)
        tmpl = [code_span(pl.code, 10, "labels:"), code_span(pl.code, 11, "run: web")]
        sel = [code_span(pl.code, 6, "matchLabels:"), code_span(pl.code, 7, "run: web"),
               code_span(pr.code, 9, "selector:"), code_span(pr.code, 10, "run: web")]
        err = VGroup(erratum_tag(), two_row_chip("slide 39 trims", "these lines", S.GREY)).arrange(DOWN, buff=0.12)
        err.next_to(br_l.line, RIGHT, buff=0.2).align_to(glue_l[0], UP).shift(DOWN * 0.05)
        assert err.get_right()[0] < pr.get_left()[0] - 0.1 and err.get_top()[1] < br_l.text.get_bottom()[1] - 0.05, \
            (err.get_right(), err.get_top(), br_l.text.get_bottom())
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(rep), code_span(pl.code, 4, "replicas: 2").animate.set_color(OWN), run_time=0.5)
            self.add(pl, rep)
            vo.wait_until("The slide trims the lines")
            self.play(FadeIn(glue_l), FadeIn(glue_r), run_time=0.6)
            seat = (pl, pr, rep, glue_l, glue_r)
            vo.wait_until("that glue them together")
            self.play(FadeIn(err, shift=LEFT * 0.15), run_time=0.5)
            flash_tag(self, err[0], INK)
            vo.wait_until("The template gives every Pod a label")
            self.play(*[Indicate(g, color=ROUTE, scale_factor=1.12) for g in tmpl], ll.flash_labels(), run_time=0.9)
            self.add(*seat)
            ll.heal(self)
            vo.wait_until("and both objects find their Pods by that label")
            self.play(*[Indicate(g, color=ROUTE, scale_factor=1.15) for g in tmpl + sel], ll.flash_labels(),
                      run_time=0.9)
            self.add(*seat)
            ll.heal(self)
            vo.wait_until("not by name")
            self.play(Indicate(ll.svc, color=ROUTE, scale_factor=1.06), run_time=0.6)
            ll.heal(self)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 2. image and ports
        p3 = code(YML, 15, 22, font_size=20, shown=YML_SHOWN)
        p3.align_to(pl, LEFT).align_to(pl, UP)
        img = code_span(p3.code, 2, "dlops/tic-tac-toe")
        cport = code_span(p3.code, 6, "containerPort: 8080")
        b_img, b_cp = bars(p3, (2,), CONTAINER), bars(p3, (6,), ROUTE)
        b_sp = [bars(pr, (6,), ROUTE), bars(pr, (8,), ROUTE)]
        pp = port_path()
        pp.move_to([0, -2.65, 0])
        assert pp.get_top()[1] < min(p3.get_bottom()[1], pr.get_bottom()[1]) - 0.15, pp.get_top()
        sp = [code_span(pr.code, 6, "port: 80"), code_span(pr.code, 8, "targetPort: 8080")]
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(pl, rep, glue_l, br_l, err), shift=UP * 0.5),
                      FadeIn(p3, shift=UP * 0.5), FadeOut(VGroup(glue_r, br_r)), run_time=0.7)
            self.remove(pl, rep, glue_l, br_l, err, glue_r, br_r)
            self.play(FadeOut(ll, shift=DOWN * 0.3), run_time=0.4)
            self.remove(ll)
            vo.wait_until("Each Pod runs the image")
            self.play(FadeIn(b_img), img.animate.set_color(CONTAINER), run_time=0.4)
            self.play(Indicate(img, color=CONTAINER, scale_factor=1.12), run_time=0.6)
            self.add(p3, b_img)
            vo.wait_until("listening on port 8080")
            self.play(FadeIn(b_cp), run_time=0.4)
            self.play(Indicate(cport, color=ROUTE, scale_factor=1.12), run_time=0.6)
            seat = [p3, pr, b_img, b_cp]
            self.add(*seat)
            vo.wait_until("The Service listens on port 80")
            self.play(FadeIn(b_sp[0]), run_time=0.3)
            seat.append(b_sp[0])
            self.play(TransformFromCopy(sp[0], pp.chips[0]), run_time=0.7)
            self.add(*seat)
            vo.wait_until("and forwards to 8080")
            self.play(FadeIn(b_sp[1]), GrowArrow(pp.arrows[0]), run_time=0.4)
            seat.append(b_sp[1])
            self.play(TransformFromCopy(sp[1], pp.chips[1]), run_time=0.6)
            self.play(GrowArrow(pp.arrows[1]), run_time=0.3)
            self.play(TransformFromCopy(cport, pp.chips[2]), run_time=0.6)
            self.add(*seat)
            self.play(LaggedStart(*[Indicate(c, color=ROUTE, scale_factor=1.06) for c in pp.chips], lag_ratio=0.3),
                      run_time=0.9)
            self.add(pp)

        # ========================================================== 3. kubectl apply: a wish, then Pods
        t = tterm(3)
        sr = on_bar(t, standin_row())
        md = MasterDiagram(standin=True, built=("laptop", "cluster", "plane", "parts"))
        assert md.get_bottom()[1] > t.box.get_top()[1] + 0.1, (md.get_bottom(), t.box.get_top())
        ref = lref("24–25")
        with self.voiceover(SAY[3]) as vo:
            gone2 = VGroup(p3, pr, pp, b_img, b_cp, *b_sp)
            self.play(FadeOut(gone2), run_time=0.5)
            self.remove(gone2, *gone2)
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(md), run_time=0.6)
            self.play(FadeIn(sr), run_time=0.3)
            t.add(sr)
            vo.wait_until("kubectl apply, dash f")
            type_capture(self, t, K10, type_time=1.0)
            g10 = out(self, t, [(s, OWN) for s in K10.at(2, 3)], run_time=0.5)
            vo.wait_until("Apply only hands a wish")
            self.play(FadeIn(ref), each(list(g10), OWN, 1.05), run_time=0.6)
            self.add(t)
            md.wish(self, "web · keep 2")
            vo.wait_until("the scheduler picks two nodes")
            md.pick(self, (0, 1))
            vo.wait_until("and their kubelets start the containers")
            self.play(*[Indicate(ch, color=TURN, scale_factor=1.12) for ch in md.parts["kubelet"]], run_time=0.6)
            md.heal(self)
            md.pods(self, 0, 1)
            md.pods(self, 1, 1)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 4. rollout status (extra)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(md), track(trk, 8, True), run_time=0.5)
            self.remove(md)
            resize(self, t, 12, extra=[bar_follow(t, sr, 12)], run_time=0.6)
            vo.wait_until("An extra check, rollout status")
            r12 = type_capture(self, t, K12, type_time=1.0)[0]
            ex = extra_row()
            pin(self, r12, beside(ex, r12))
            vo.wait_until("zero, then one of two available")
            out(self, t, K12.at(2), wrap=True, run_time=0.4)
            vo.wait_until("then one of two available")
            out(self, t, K12.at(3), wrap=True, run_time=0.4)
            vo.wait_until("then rolled out")
            out(self, t, [(K12.line(4), OWN)], run_time=0.4)
            vo.wait_until("on two different workers")
            g67 = out(self, t, K12.at(6, 7), wrap=True, run_time=0.5)
            nodes = [substring(r, "test-cluster-worker2" if "worker2" in r.text else "test-cluster-worker")
                     for r in g67 if "test-cluster-worker" in r.text]
            assert len(nodes) == 2, [r.text for r in g67]
            self.play(*[n.animate.set_color(TURN) for n in nodes], run_time=0.4)
            self.play(each(nodes, TURN, 1.1), run_time=0.8)
            self.add(t)

        # ========================================================== 5. get services: 80 → 31366 → 8080
        ref = lref("38")
        with self.voiceover(SAY[5]) as vo:
            unpin(self, r12, ex, track(trk, 9), FadeIn(ref))
            resize(self, t, 12, keep=[], run_time=0.4)
            vo.wait_until("Next, kubectl get services")
            type_capture(self, t, K11, type_time=0.5)
            g11 = out(self, t, K11.at(2, 3, 4), run_time=0.5)
            row = g11[2]
            lb, pend, prt = substring(row, "LoadBalancer"), substring(row, "<pending>"), substring(row, "80:31366/TCP")
            vo.wait_until("The web Service is a load balancer")
            self.play(lb.animate.set_color(CLOUD), run_time=0.3)
            self.play(Indicate(lb, color=CLOUD, scale_factor=1.1), run_time=0.6)
            self.add(t)
            p80, p313 = substring(row, "80:"), substring(row, "31366")
            pitch = t.pitch
            y0 = row.strut.get_center()[1]
            labs = [label("80 outside", 20, ROUTE), label("31366 on every node", 20, ROUTE),
                    label("8080 in the Pod", 20, ROUTE)]
            xs = [p80.get_left()[0], p313.get_left()[0], p313.get_left()[0]]
            for i, (lab_, x) in enumerate(zip(labs, xs)):
                lab_.move_to([x + lab_.width / 2, y0 - (i + 1) * pitch * 1.05, 0])
                keep_inside(lab_)
            assert labs[-1].get_bottom()[1] > t.box.get_bottom()[1] + 0.1
            vo.wait_until("port 80, mapped to 31366")
            self.play(prt.animate.set_color(ROUTE), FadeIn(labs[0], shift=DOWN * 0.1), run_time=0.4)
            self.add(t, *[x for x in labs if x in self.mobjects])
            vo.wait_until("mapped to 31366 on every node")
            self.play(FadeIn(labs[1], shift=DOWN * 0.1), Indicate(p313, color=ROUTE, scale_factor=1.12), run_time=0.5)
            self.add(t, *[x for x in labs if x in self.mobjects])
            vo.wait_until("and on to 8080 in the Pod")
            self.play(FadeIn(labs[2], shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Its external IP says pending")
            self.play(pend.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(pend, color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(t, *[x for x in labs if x in self.mobjects])
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 6. 43 s later: still pending (ponder)
        md = MasterDiagram(standin=True, built=("laptop", "cluster", "plane", "parts"))
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(*labs)), run_time=0.3)
            self.remove(*labs)
            vo.wait_until("43 seconds later")
            type_capture(self, t, K13, type_time=0.4)
            g13 = out(self, t, K13.at(4), run_time=0.4)
            age, pend2 = substring(g13[0], "43s"), substring(g13[0], "<pending>")
            self.play(age.animate.set_color(TURN), pend2.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(age, color=TURN, scale_factor=1.2), Indicate(pend2, color=TURN, scale_factor=1.1),
                      run_time=0.7)
            self.add(t)
            vo.wait_until("Which part of the cluster picture is waiting")
            resize(self, t, 3, keep=3, extra=[bar_follow(t, sr, 3)], run_time=0.6)
            self.play(FadeIn(md), run_time=0.6)
        card = ponder(self, "EXTERNAL-IP is still <pending>\nafter 43 seconds.\nWhich part of the cluster is waiting,\n"
                            "and on what?", seconds=8, center=(0, 0.6))

        # ========================================================== 7. the controllers, waiting on the cloud
        ref = lref("24")
        nocloud = grey_chip("kind: no cloud here")
        nocloud.move_to([-5.0, -2.05, 0])
        ghost = dashed_chip("on GKE: a load balancer and an IP, after a short wait")
        ghost.move_to([1.55, -2.05, 0])
        assert ghost.get_right()[0] < 6.5 and nocloud.get_right()[0] < ghost.get_left()[0] - 0.2, \
            (ghost.get_left(), ghost.get_right())
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(card), FadeIn(ref), run_time=0.5)
            self.remove(card)
            vo.wait_until("The controllers")
            md.lamp(self, "controllers", TURN)
            self.play(md.light("controllers"), run_time=0.6)
            md.heal(self)
            vo.wait_until("waiting on the cloud provider")
            md.cloud_arrow(self, ERR)
            self.play(FadeOut(t), run_time=0.4)
            self.remove(t)
            self.play(FadeIn(nocloud, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("On GKE they ask Google")
            self.play(Indicate(md.parts["cloud"], color=CLOUD, scale_factor=1.06), run_time=0.6)
            md.heal(self)
            self.play(FadeIn(ghost, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("which arrives after a short wait")
            self.play(Indicate(ghost.text, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("The kind cluster has no cloud to ask")
            flash_tag(self, nocloud, ERR)
            self.play(Indicate(md.parts["cloud_arrow"], color=ERR, scale_factor=1.04), run_time=0.6)
            md.heal(self)
        self.play(FadeOut(VGroup(md, nocloud, ghost, ref)), run_time=0.5)
        self.remove(md, nocloud, ghost, ref)

        # ========================================================== 8. View the App (illustration)
        rc = readme_card((574, 575), VIEW_README, size=20)
        rc.align_to([-6.45, 0, 0], LEFT).align_to([0, 2.6, 0], UP)
        bw = browser_window("http://" + EXT_IP, win_w=5.6, win_h=3.6)
        bw.align_to([-6.45, 0, 0], LEFT).align_to([0, rc.get_bottom()[1] - 0.35, 0], UP)
        assert bw.get_bottom()[1] > -3.5, bw.get_bottom()
        grid = ttt_grid(0.5)
        grid.move_to(bw.at(0, 0))
        yt = your_turn()
        yt.next_to(bw.frame, RIGHT, buff=0.3).set_y(bw.address.get_y())
        grp8 = VGroup(rc, bw, grid, yt)
        grp8.shift(RIGHT * -grp8.get_center()[0])
        with self.voiceover(SAY[8]) as vo:
            self.play(track(trk, 10), FadeIn(bw, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(rc, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("wait for the external IP")
            self.play(Indicate(rc.body[0], color=TURN, scale_factor=1.04), run_time=0.7)
            self.add(rc)
            vo.wait_until("copy it into your browser")
            addr = bw.address
            self.play(Indicate(addr, color=TURN, scale_factor=1.06), FadeIn(yt, shift=LEFT * 0.15), run_time=0.7)
            self.add(bw)
            vo.wait_until("and the game appears")
            self.play(LaggedStart(*[Create(sq) for sq in grid], lag_ratio=0.08), run_time=0.9)
            self.play(Indicate(grid, color=INK, scale_factor=1.06), run_time=0.7)
        self.wait(0.5)
        self.play(FadeOut(VGroup(bw, grid, rc, yt)), run_time=0.5)
        self.remove(bw, grid, rc, yt)

        # ========================================================== 9. port-forward + curl (extra)
        t9 = tterm(8)
        sr9 = on_bar(t9, standin_row())
        assert sr9.get_left()[0] > t9.title.get_right()[0] + 0.1, (sr9.get_left(), t9.title.get_right())
        ref = lref("29")
        note29 = VGroup(erratum_tag(), two_row_chip("a port-forward started in the toolbox opens inside the toolbox",
                                                    "→ test it with curl there", S.GREY))
        note29.arrange(RIGHT, buff=0.25)
        under_term(t9, note29, buff=0.25)
        assert note29.get_top()[1] < TRACK_BOTTOM - 0.1 and note29.get_left()[0] > -6.5, note29.get_left()
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeIn(t9, shift=UP * 0.2), track(trk, 10, True), run_time=0.6)
            self.play(FadeIn(sr9), run_time=0.3)
            t9.add(sr9)
            vo.wait_until("port forward to the Service")
            r57 = type_capture(self, t9, K57, type_time=1.6)[0]
            er9 = extra_row()
            pin(self, r57, beside(er9, r57))
            vo.wait_until("then curl: 200 OK")
            g57 = out(self, t9, [(K57.line(2), OWN)] + K57.at(13, 14), run_time=0.5)
            self.play(Indicate(g57[0], color=OWN, scale_factor=1.08), run_time=0.6)
            self.add(t9)
            vo.wait_until("The lecture suggests it for your browser")
            self.play(FadeIn(ref), FadeIn(note29, shift=DOWN * 0.1), run_time=0.5)
            flash_tag(self, note29[0], INK)
            vo.wait_until("from the toolbox the port opens inside the container")
            self.play(Indicate(note29[1].text[0], color=INK, scale_factor=1.04), run_time=0.7)
            vo.wait_until("test it there")
            self.play(Indicate(note29[1].text[1], color=OWN, scale_factor=1.08), run_time=0.6)

        self.play(FadeOut(VGroup(trk, t9, note29, ref)), run_time=0.6)
        self.remove(trk, t9, note29, ref)
        self.wait(0.4)
