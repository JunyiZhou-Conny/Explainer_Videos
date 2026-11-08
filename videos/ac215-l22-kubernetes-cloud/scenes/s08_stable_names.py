"""S08 · Labels, Services, namespaces, then delete (AC215 L22, the full follow-along; last scene of Part 1).
TRACKER [W] 10 · extra (beats 0-5), 11 · extra (beat 6), 11 (beat 7), 11 · extra (beat 8), 11 (beat 9).
Lecture: 22 · 39 (beat 0), 35 (beat 4), 27 (beat 5), 40 (beat 7), 44 (beat 9).

Beats (script.md "## S08", one voiceover block each):
0. LECTURE 22 · 39. Two small strips: k50:10 (the deleted Pod) and k54:4 (its replacement), each
   cropped after the IP column, the IPs YELLOW (never read). V3 (LabelLink) builds under them: the
   Deployment, two Pods, their PINK 'run: web' stickers, the Service and its PINK lasso. A 1-row
   toolbox terminal 'laptop · toolbox · stand-in' ('extra', 'stand-in: kind, not GKE' on its bar)
   prints TERM(k50: 19) PINK with the GREY chip 'recorded before the delete in S07'; its endpoints
   become V3's endpoints list; then (tag 'illustration') Pod 0 is replaced and 10.244.1.2 becomes
   10.244.1.7 in the list, while the new IP in the second strip flashes.
1. The strips and V3 fade; the terminal grows to 8 rows. Line 1 of k52 (extra; soft-wrapped at the row
   edge, since its quoted shell argument cannot fold with ' \\') -> TERM(k52: 4–5, 11). The name and the
   address turn PINK and form the PINK DNS card above; a small inset (k11:2, 4 cropped after
   CLUSTER-IP, 'the Service's CLUSTER-IP · S06') ties 10.96.52.79 to the Service with a GREY line;
   'http://web' and the game's <title> light up; the DNS name flashes on "The name stays".
2. The inset goes; a GREY-dashed V5 chip under the DNS card: TEAL 'api' → PINK 'vector-db:8000',
   '(part 2)'; the arrow grows on "by the Service name".
3. DNS card and chip fade. `kubectl exec --stdin --tty deployment/web -- /bin/sh` (k51:1, folds) at the
   toolbox prompt, then `hostname; ls; exit` at the Pod's '$' (k51:2) -> TERM(k51: 3–4); line 3 TEAL,
   with the GREY row tag 'recorded before the delete in S07'; above, a TEAL Pod whose three-colour name
   flies out of line 3; the file list's index.html YELLOW; the GREY chip 'README: the same exec, into
   the API → S14'.
4. LECTURE 22 · 35. Line 1 of k63 (extra; folds) -> TERM(k63: 2–7, 8–10). Above, one folder per
   namespace flies out of its row (default and kube-system ORANGE, the others GREY); 'default' rings
   YELLOW on "looks only in default"; a GREEN folder 'cheese-app-namespace' appears with line 8, a GREY
   'empty' with line 9, and is struck and fades with line 10.
5. LECTURE 22 · 27. Terminal and folders fade; the KubectlGrammar card returns with
   `kubectl get pods`, then `-n cheese-app-namespace` drops into the flags slot, PINK.
6. TRACKER [W] 11 · extra. The terminal returns. Line 1 of k80 typed crop "deploy-k8s-tic-tac-toe.yml"
   -> TERM(k80: 2–3). Above the terminal: the GREY chip 'on GKE: releases the load balancer while the
   cluster still exists' and a YELLOW '▶ your turn'.
7. TRACKER [W] 11. LECTURE 22 · 40. The stand-in tags leave the bar, the title becomes 'laptop ·
   toolbox'. `gcloud container clusters delete test-cluster --zone us-east1-c` -> TERM(b51: 2 wrap) RED
   ('active account' flashes). GREY chip 'yours: Do you want to continue (Y/n)? → Y'.
8. TRACKER [W] 11 · extra. A laptop terminal 'laptop · stand-in' at student@laptop:~$ (tags 'extra',
   'stand-in: kind, not GKE'); above it the GREY-dashed stand-in cluster drawing (control plane + two
   workers). Line 1 of k81 typed crop "--name test-cluster" -> TERM(k81: 2–3 wrap); the drawing's nodes
   fade one by one, then its outline.
9. TRACKER [W] 11. LECTURE 22 · 44. The GOLD 'Don't forget to delete' card centre, a YELLOW
   '▶ your turn' beside it; the GOLD cost tag from S05 slides in under it with a running cost dial,
   which stops on "check that your test cluster is gone". Fade; empty frame (end of Part 1).

Deviations from SHOW:
- Beat 0: the strips are cropped after the IP column (k50:10 is 140 characters; the IP is the point).
  V3 is built here (the scene opens on an empty frame after S07), so the lasso arrives with
  "The Service keeps a list"; k50:19's endpoints become V3's endpoints list (the list the illustration
  then edits), so the real line and the drawn list are both on screen.
- Beat 1: k52's command is soft-wrapped at the row edge (no ' \\'), because Terminal.fold would break
  inside its single-quoted 'nslookup … | head -5' argument, which a shell would not paste back. The
  inset's k11 rows are cropped after the CLUSTER-IP column.
- Beat 3: SHOW names no picture; a TEAL Pod above the terminal takes its name from the hostname line
  (what became what), and a GREY scene chip carries "The README shells into the API the same way".
- Beat 6: the '▶ your turn' and the GREY chip sit just above the terminal: the typed row (68
  characters) leaves no room beside it, and the bar holds the 'extra' and stand-in tags.
- Beat 7: the 'extra' and stand-in tags leave the bar and the title becomes 'laptop · toolbox' (b51 is
  the README's own command, run in the toolbox, not on the stand-in).
- Beat 9: the cost tag comes with a GOLD CostDial (the "meter"); its needle stops on "check that your
  test cluster is gone".
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S08"]
assert len(SAY) == SAY_COUNT["S08"] == 10

# ------------------------------------------------------------------ the real sources (checked)
K50, K54, K52, K11, K51, K63, K80, B51, K81 = (capture(k) for k in
                                               ("k50", "k54", "k52", "k11", "k51", "k63", "k80", "b51", "k81"))
POD_A = f"web-{RS_HASH}-{POD_SUFFIXES[0]}"
POD_NEW = f"web-{RS_HASH}-{NEW_SUFFIX}"
OLD_IP = ENDPOINTS[0].split(":")[0]
EPS = ",".join(ENDPOINTS)

assert K50.line(10).startswith(f"pod/{POD_A} ") and OLD_IP in K50.line(10)
assert K54.line(4).startswith(f"{POD_NEW} ") and NEW_POD_IP in K54.line(4)
assert K50.line(19).startswith("endpoints/web ") and EPS in K50.line(19)
assert K52.cmd.startswith("kubectl run dns-check --image=busybox:1.36") and "http://web" in K52.cmd
assert K52.line(4).split() == ["Name:", DNS_NAME] and K52.line(5).split() == ["Address:", SVC_IP]
assert "<title>CodePen - Tic Tac Toe</title>" in K52.line(11)
assert K11.line(2).split()[2] == "CLUSTER-IP" and K11.line(4).split()[:3] == ["web", "LoadBalancer", SVC_IP]
assert K51.cmd_lines == ["kubectl exec --stdin --tty deployment/web -- /bin/sh", "hostname; ls; exit"]
assert K51.line(3) == POD_A and "index.html" in K51.line(4)
assert K63.cmd.startswith("kubectl get namespaces; kubectl create namespace cheese-app-namespace;")
NS_ROWS = [K63.line(n).split()[0] for n in range(3, 8)]
assert NS_ROWS == ["default", "kube-node-lease", "kube-public", "kube-system", "local-path-storage"]
assert K63.line(8) == f"namespace/{NAMESPACE} created" and K63.line(9).startswith("No resources found")
assert K63.line(10).startswith(f'namespace "{NAMESPACE}" deleted')
assert K80.typed("deploy-k8s-tic-tac-toe.yml") == "kubectl delete -f deploy-k8s-tic-tac-toe.yml"
assert K80.line(2).startswith('deployment.apps "web" deleted') and K80.line(3).startswith('service "web" deleted')
assert B51.cmd == "gcloud container clusters delete test-cluster --zone us-east1-c"
assert "active account" in B51.line(2)
assert K81.typed("--name test-cluster") == "kind delete cluster --name test-cluster"
assert K81.line(2).startswith('Deleting cluster "test-cluster"') and K81.line(3).startswith("Deleted nodes:")

ROWS = 8                      # the toolbox terminal of beats 1-3 (20 pt, 72 characters a row)
ROWS4 = 10                    # beats 4-7: k63's four command rows + six namespace rows


def bar_follow(t, tags, rows: int):
    """ANIMs: tags on terminal t's title bar move with the bar when t is resized to `rows`."""
    top = BOTTOM + rows * t.pitch + 0.85
    return [g.animate.move_to([g.get_x(), top - t.bar_h / 2, 0]) for g in tags]


def bar_tags(t):
    """'extra' (left, after the dots) and 'stand-in: kind, not GKE' (right) on t's title bar."""
    sr = on_bar(t, standin_row())
    er = extra_row()
    er.move_to([t.dots.get_right()[0] + 0.3 + er.width / 2, sr.get_y(), 0])
    assert er.get_right()[0] < t.title.get_left()[0] - 0.1 and sr.get_left()[0] > t.title.get_right()[0] + 0.1
    return er, sr


def strip(text: str, hi: str) -> VGroup:
    """A terminal row on its own (20 pt mono on the terminal background, GREY edge), `hi` YELLOW."""
    ln = mono_line(text, 20, OUTPUT)
    substring(ln, hi).set_color(TURN)
    fr = RoundedRectangle(width=ln.width + 0.4, height=0.5, corner_radius=0.1, stroke_color=S.GREY_DARK,
                          stroke_width=2).set_fill(TERM_BG, 1)
    ln.move_to(fr)
    g = VGroup(fr, ln)
    g.frame, g.line = fr, ln
    return g


def folder(name: str, color) -> VGroup:
    """A namespace as a folder: glyph + mono name (20 pt). .glyph .text"""
    gl = folder_icon(0.42, color)
    t = mono(name, 20, INK if color != S.GREY else S.GREY)
    g = VGroup(gl, t).arrange(RIGHT, buff=0.14)
    g.glyph, g.text = gl, t
    return g


class StableNames(VoiceScene):
    def construct(self):
        trk = tracker_w(10, True)

        # ========================================================== 0. Pods are mortal; the list follows
        ref = lref("39")
        s1 = strip(K50.crop(10, OLD_IP), OLD_IP).move_to([0, 2.42, 0])
        s2 = strip(K54.crop(4, NEW_POD_IP), NEW_POD_IP).move_to([0, 1.82, 0])
        s1.align_to([-6.3, 0, 0], LEFT)
        s2.align_to([-6.3, 0, 0], LEFT)
        assert s1.get_top()[1] < TRACK_BOTTOM - 0.05 and s1.get_right()[0] < 6.5, (s1.get_top(), s1.get_right())
        lk = LabelLink()
        lk.shift(UP * 0.3)
        t = term(toolbox_prompt(), 1, T_TB_STANDIN, size=20)
        er, sr = bar_tags(t)
        t.add(er, sr)
        rec = grey_chip("recorded before the delete in S07")
        under_term(t, rec)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref), run_time=0.5)
            self.play(FadeIn(s1, shift=DOWN * 0.15), run_time=0.4)
            vo.wait_until("the new Pod got a new address")
            self.play(FadeIn(s2, shift=DOWN * 0.15), run_time=0.4)
            self.play(Indicate(substring(s1.line, OLD_IP), color=TURN, scale_factor=1.15),
                      Indicate(substring(s2.line, NEW_POD_IP), color=TURN, scale_factor=1.15), run_time=0.8)
            self.add(s1, s2)
            vo.wait_until("So how does traffic find it?")
            lk.deployment(self)
            lk.make_pods(self)
            lk.stickers(self)
            vo.wait_until("The Service keeps a list")
            lk.service(self)
            lk.lasso(self)
            vo.wait_until("of every Pod wearing its label")
            self.play(lk.flash_labels(), FadeIn(t, shift=UP * 0.2), run_time=0.8)
            lk.heal(self)
            e19 = out(self, t, [(K50.line(19), ROUTE)], run_time=0.4)[0]
            self.play(FadeIn(rec, shift=LEFT * 0.2), run_time=0.4)
            src = substring(e19, EPS).copy()
            lk.endpoints(self)
            self.add(src)
            self.play(src.animate.move_to(lk.eps.items).set_opacity(0), run_time=0.7)
            self.remove(src)
            lk.heal(self)
            assert lk.eps.get_bottom()[1] > rec.get_top()[1] + 0.08, (lk.eps.get_bottom(), rec.get_top())
            vo.wait_until("and that list follows the Pods")
            ill = illustration_tag()
            ill.next_to(lk.svc, UP, buff=0.25).align_to(lk.svc, RIGHT)
            assert ill.get_top()[1] < s2.get_bottom()[1] - 0.05, ill.get_top()
            self.play(FadeIn(ill), run_time=0.3)
            lk.replace_pod(self, 0)
            new_ep = lk.swap_endpoint(self, 0, f"{NEW_POD_IP}:8080")
            self.play(Indicate(new_ep, color=TURN, scale_factor=1.15),
                      Indicate(substring(s2.line, NEW_POD_IP), color=TURN, scale_factor=1.15), run_time=0.8)
            self.add(s2, lk)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 1. cluster DNS: the name stays (k52)
        dns = dns_card().move_to([0, 2.3, 0]).align_to([-6.3, 0, 0], LEFT)
        rows = [K11.crop(2, "CLUSTER-IP"), K11.crop(4, SVC_IP)]
        ins_l = VGroup(*[mono_line(r, 20, OUTPUT) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        ins_f = RoundedRectangle(width=ins_l.width + 0.4, height=ins_l.height + 0.3, corner_radius=0.1,
                                 stroke_color=S.GREY_DARK, stroke_width=2).set_fill(TERM_BG, 1)
        ins_l.move_to(ins_f)
        inset = VGroup(ins_f, ins_l)
        inset.move_to([0, 1.2, 0]).align_to(dns, RIGHT)
        ins_ip = substring(ins_l[1], SVC_IP)
        ins_note = note("the Service's CLUSTER-IP · S06").next_to(inset, RIGHT, buff=0.3)
        # the tie stops at the inset's top edge, above the CLUSTER-IP column (never through its header)
        tie = Line(dns.ip.get_bottom() + DOWN * 0.05, [ins_ip.get_x(), ins_f.get_top()[1], 0], color=S.GREY,
                   stroke_width=3)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(s1, s2, lk, ill, rec)), run_time=0.5)
            self.remove(s1, s2, lk, ill, rec)
            resize(self, t, ROWS, extra=bar_follow(t, [er, sr], ROWS), run_time=0.6)
            assert t.box.get_top()[1] < inset.get_bottom()[1] - 0.1, (t.box.get_top(), inset.get_bottom())
            vo.wait_until("An extra from a throwaway Pod")
            cmd = type_cmd(self, t, K52.cmd, type_time=2.2, soft=True)
            vo.wait_until("points to the Service")
            g1 = out(self, t, K52.at(4, 5, 11), run_time=0.5)
            nm, ip = substring(g1[0], DNS_NAME), substring(g1[1], SVC_IP)
            self.play(nm.animate.set_color(ROUTE), ip.animate.set_color(ROUTE), run_time=0.3)
            self.play(FadeIn(dns.frame), run_time=0.3)
            self.play(ReplacementTransform(nm.copy(), dns.name), ReplacementTransform(ip.copy(), dns.ip),
                      FadeIn(dns[1][1]), run_time=0.8)
            self.remove(dns.frame, dns.name, dns.ip, dns[1][1])
            self.add(dns, t)
            self.play(FadeIn(inset), FadeIn(ins_note), run_time=0.4)
            self.play(Create(tie), ins_ip.animate.set_color(ROUTE), run_time=0.5)
            self.play(Indicate(dns.ip, color=ROUTE, scale_factor=1.15), Indicate(ins_ip, color=ROUTE, scale_factor=1.15),
                      run_time=0.7)
            self.add(dns, inset)
            vo.wait_until("and fetching just web returns the game page")
            web = [r for r in rows_of(cmd) if "http://web" in r.text]
            assert web, [r.text for r in rows_of(cmd)]
            ttl = substring(g1[2], "<title>CodePen - Tic Tac Toe</title>")
            self.play(substring(web[0], "http://web").animate.set_color(ROUTE), ttl.animate.set_color(TURN),
                      run_time=0.4)
            self.play(Indicate(ttl, color=TURN, scale_factor=1.06), run_time=0.7)
            self.add(t)
            vo.wait_until("The name stays while the Pods change")
            self.play(Indicate(dns.name, color=ROUTE, scale_factor=1.06), run_time=0.8)
            self.add(dns)

        # ========================================================== 2. the cheese app will do the same
        v5 = VGroup(box_chip("api"), route_chip(f"{SVC_NAMES['vdb']}:{PORTS['vdb']}"))
        v5.arrange(RIGHT, buff=1.0)
        v5_ar = route(v5[0].get_right(), v5[1].get_left(), stroke=3)
        v5_n = note("(part 2)").next_to(v5, RIGHT, buff=0.25)
        v5_in = VGroup(v5, v5_ar, v5_n)
        v5_box = outline_box(v5_in.width + 0.5, v5_in.height + 0.36, PAST, solid=False)
        v5_box.move_to(v5_in)
        chip5 = VGroup(v5_box, v5[0], v5[1], v5_n)
        off = np.array([dns.get_left()[0] - v5_box.get_left()[0], 1.15 - v5_box.get_y(), 0])
        chip5.shift(off)
        v5_ar.shift(off)
        assert chip5.get_bottom()[1] > t.box.get_top()[1] + 0.1
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(inset, ins_note, tie)), run_time=0.4)
            self.remove(inset, ins_note, tie)
            self.play(FadeIn(chip5, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("by the Service name")
            self.play(GrowArrow(v5_ar), run_time=0.6)
            self.play(Indicate(v5[1], color=ROUTE, scale_factor=1.12), Indicate(dns.name, color=ROUTE, scale_factor=1.04),
                      run_time=0.8)
            self.add(dns)

        # ========================================================== 3. kubectl exec into the Deployment (k51)
        pg = pod_glyph(r=0.42).move_to([-3.8, 1.85, 0])
        pnm = pod_name(POD_A).next_to(pg, DOWN, buff=0.14)
        api_chip = scene_chip("README: the same exec, into the API → S14").move_to([2.6, 1.6, 0])
        assert api_chip.get_right()[0] < 6.5 and pnm.get_bottom()[1] > t.box.get_top()[1] + 0.1
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(dns, chip5, v5_ar)), run_time=0.4)
            self.remove(dns, chip5, v5_ar)
            vo.wait_until("Another extra")
            type_capture(self, t, K51, type_time=1.2, prompts=[toolbox_prompt(), "$"])
            t.set_prompt(toolbox_prompt())
            vo.wait_until("Hostname prints the name of one Pod")
            g3 = out(self, t, [(K51.line(3), POD), K51.line(4)], run_time=0.4)
            self.play(GrowFromCenter(pg), run_time=0.4)
            self.play(ReplacementTransform(substring(g3[0], POD_A).copy(), pnm), run_time=0.8)
            self.remove(pnm)
            self.add(t, pnm)
            rt = row_tag("recorded before the delete in S07")
            pin(self, g3[0], beside(rt, g3[0]))
            vo.wait_until("and the game's files are inside")
            ix = substring(g3[1], "index.html")
            self.play(ix.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(ix, color=TURN, scale_factor=1.15), Indicate(pg.circle, color=POD, scale_factor=1.1),
                      run_time=0.7)
            self.add(t)
            vo.wait_until("The README shells into the API the same way")
            self.play(FadeIn(api_chip, shift=LEFT * 0.2), run_time=0.5)
            flash_tag(self, api_chip, INK)

        # ========================================================== 4. namespaces: folders for objects (k63)
        ref = lref("35")
        cols = {"default": SHARED, "kube-system": SHARED}
        fds = [folder(n, cols.get(n, S.GREY)) for n in NS_ROWS]
        new_fd = folder(NAMESPACE, OWN)
        row1 = VGroup(*fds[:3]).arrange(RIGHT, buff=0.6)
        row2 = VGroup(*fds[3:], new_fd).arrange(RIGHT, buff=0.6)
        for r_, y in ((row1, 2.45), (row2, 1.75)):
            r_.move_to([0, y, 0]).align_to([-6.2, 0, 0], LEFT)
        assert row2.get_right()[0] < 6.5 and row1.get_right()[0] < 3.3 and row1.get_top()[1] < TRACK_BOTTOM - 0.05
        assert row2.get_bottom()[1] > strip_top(ROWS4, 20) + 0.15, (row2.get_bottom(), strip_top(ROWS4, 20))
        empty_t = note("empty").next_to(new_fd, DOWN, buff=0.1)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(pg, pnm, api_chip)), FadeIn(ref), run_time=0.4)
            self.remove(pg, pnm, api_chip)
            resize(self, t, ROWS4, extra=bar_follow(t, [er, sr], ROWS4), run_time=0.5)
            assert abs(t.box.get_top()[1] - strip_top(ROWS4, 20)) < 0.02, t.box.get_top()
            type_capture(self, t, K63, type_time=2.0)
            vo.wait_until("Namespaces: folders for objects")
            g4 = out(self, t, K63.at((2, 7)), run_time=0.5)
            by = {r.text.split()[0]: r for r in g4[1:]}
            self.play(*[substring(by[n], n).animate.set_color(SHARED) for n in ("default", "kube-system")],
                      run_time=0.3)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(f.glyph, scale=0.6),
                                                   ReplacementTransform(substring(by[n], n).copy(), f.text))
                                    for n, f in zip(NS_ROWS, fds)], lag_ratio=0.2), run_time=1.4)
            self.remove(*[f.glyph for f in fds], *[f.text for f in fds])
            self.add(*fds, t)
            vo.wait_until("Without a flag, kubectl looks only in default")
            rd = ring(fds[0], TURN, buff=0.12, stroke=4)
            self.play(Create(rd), run_time=0.4)
            self.play(Indicate(fds[0].text, color=TURN, scale_factor=1.12), run_time=0.7)
            self.add(fds[0])
            vo.wait_until("this extra lists them")
            self.play(each([f.glyph for f in fds], INK, 1.15), FadeOut(rd), run_time=0.9)
            self.remove(rd)
            self.add(*fds)
            vo.wait_until("then creates and deletes the cheese app namespace")
            g8 = out(self, t, [K63.line(8)], run_time=0.3)
            self.play(substring(g8[0], NAMESPACE).animate.set_color(OWN), FadeIn(new_fd, shift=DOWN * 0.15),
                      run_time=0.5)
            out(self, t, [K63.line(9)], run_time=0.3)
            self.play(FadeIn(empty_t), run_time=0.3)
            out(self, t, [K63.line(10)], run_time=0.3)
            x = cross_glyph(0.36).move_to(new_fd.glyph)
            self.play(Create(x), run_time=0.3)
            self.play(FadeOut(VGroup(new_fd, empty_t, x), shift=DOWN * 0.2), run_time=0.5)
            self.remove(new_fd, empty_t, x)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 5. the flags slot: -n cheese-app-namespace
        ref = lref("27")
        kg = KubectlGrammar()
        kg.move_to([0, 0.2, 0])
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(*fds)), FadeOut(t), FadeIn(ref), run_time=0.5)
            self.remove(*fds, t)
            self.play(FadeIn(kg, shift=UP * 0.2), run_time=0.5)
            kg.fill(self, "get", "pods")
            vo.wait_until("every command about the app gets dash n")
            kg.flag(self, f"-n {NAMESPACE}", ROUTE)
            vo.wait_until("in the flags slot")
            self.play(Indicate(kg.values[3], color=ROUTE, scale_factor=1.1),
                      Indicate(kg.heads[3], color=ROUTE, scale_factor=1.15), run_time=0.8)
            kg.heal(self)
        self.play(FadeOut(ref), FadeOut(kg), run_time=0.4)
        self.remove(ref, kg)

        # ========================================================== 6. the extra tip: kubectl delete -f (k80)
        gke = grey_chip("on GKE: releases the load balancer while the cluster still exists")
        gke.next_to(t.box, UP, buff=0.15).align_to(t.box, LEFT)
        yt6 = your_turn()
        under_term(t, yt6, buff=0.15)
        assert gke.get_right()[0] < yt6.get_left()[0] - 0.15, (gke.get_right(), yt6.get_left())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(t), track(trk, 11, True), run_time=0.5)
            vo.wait_until("kubectl delete with the same file")
            type_cmd(self, t, K80.typed("deploy-k8s-tic-tac-toe.yml"), type_time=1.0)
            out(self, t, K80.at(2, 3), run_time=0.4)
            self.play(FadeIn(yt6, shift=LEFT * 0.2), run_time=0.4)
            flash_tag(self, yt6, TURN)
            vo.wait_until("On GKE, this releases the load balancer")
            self.play(FadeIn(gke, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, gke, INK)

        # ========================================================== 7. Delete Cluster (b51): no account here
        ref = lref("40")
        yours = grey_chip("yours: Do you want to continue (Y/n)? → Y")
        under_term(t, yours, buff=0.15)
        with self.voiceover(SAY[7]) as vo:
            t.remove(er, sr)
            self.play(FadeOut(VGroup(gke, yt6, er, sr)), retitle(t, T_TOOLBOX), track(trk, 11, False), FadeIn(ref),
                      run_time=0.5)
            self.remove(gke, yt6, er, sr)
            self.add(t)
            vo.wait_until("gcloud container clusters delete")
            type_capture(self, t, B51, type_time=1.6)
            e7 = out(self, t, [(B51.line(2), ERR)], wrap=True, run_time=0.5)
            aa = [r for r in e7 if "active account" in r.text]
            if aa:
                self.play(Indicate(substring(aa[0], "active account"), color=ERR, scale_factor=1.1), run_time=0.6)
                self.add(t)
            vo.wait_until("Yours asks whether to continue")
            self.play(FadeIn(yours, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("answer yes")
            flash_tag(self, yours, INK)
        self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 8. the stand-in goes too (k81)
        lt = term(P_LAPTOP, 6, T_LAPTOP_STANDIN, size=20)
        er8, sr8 = bar_tags(lt)
        lt.add(er8, sr8)
        kc = frame_box(9.0, 2.3, STANDIN, k=0.04, dashed=True).move_to([0, 1.25, 0])
        kc_t = mono(f"{TEST_CLUSTER} · kind", 20, S.GREY)
        kc_t.move_to(kc).align_to(kc, UL).shift(np.array([0.2, -0.12, 0]))
        nds = VGroup(*[node_box(n, 2.6, 1.0, color=STANDIN, dashed=True)
                       for n in ("control-plane", "worker", "worker2")]).arrange(RIGHT, buff=0.3)
        nds.move_to(kc).shift(DOWN * 0.2)
        assert kc.get_bottom()[1] > lt.box.get_top()[1] + 0.15 and kc.get_top()[1] < TRACK_BOTTOM - 0.05
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(t), FadeOut(yours), FadeIn(lt), track(trk, 11, True), FadeIn(kc), FadeIn(kc_t),
                      FadeIn(nds), run_time=0.6)
            self.remove(t, yours)
            type_cmd(self, lt, K81.typed("--name test-cluster"), type_time=1.0)
            out(self, lt, K81.at(2, 3), wrap=True, run_time=0.5)
            self.play(LaggedStart(*[FadeOut(n, shift=DOWN * 0.15) for n in nds], lag_ratio=0.3), run_time=0.9)
            self.play(FadeOut(kc), FadeOut(kc_t), run_time=0.4)
            self.remove(kc, kc_t, nds)

        # ========================================================== 9. Don't forget to delete
        ref = lref("44")
        dfc = dont_forget_card().move_to([-1.2, 0.7, 0])
        yt9 = your_turn().next_to(dfc, RIGHT, buff=0.35)
        cost = cost_tag("test cluster · billed per node-hour while it exists")
        dial = CostDial(radius=0.42, caption=None)
        meter = VGroup(dial, cost).arrange(RIGHT, buff=0.35).move_to([0, -1.3, 0])
        assert yt9.get_right()[0] < 6.5 and meter.get_right()[0] < 6.5
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(lt), track(trk, 11, False), FadeIn(ref), run_time=0.5)
            self.remove(lt)
            self.play(FadeIn(dfc, scale=0.9), run_time=0.6)
            vo.wait_until("don't forget to delete")
            self.play(Indicate(dfc.title, color=COST, scale_factor=1.06),
                      FadeIn(meter, shift=LEFT * 1.2), dial.tracker.animate(rate_func=linear).increment_value(0.4),
                      run_time=1.0)
            dial.run(self, 0.6, 1.4)
            vo.wait_until("Pause, check that your test cluster is gone")
            self.play(FadeIn(yt9, shift=LEFT * 0.2), dial.tracker.animate(rate_func=linear).increment_value(0.15),
                      run_time=0.5)
            dial.freeze()
            flash_tag(self, yt9, TURN)
            vo.wait_until("and part 1 is done")
            back = (dial.tracker.get_value() % 1.0) * TAU          # the needle returns to zero and stays
            self.play(Rotate(dial.needle, back, about_point=dial.face.get_center()), run_time=0.6)
            self.play(Indicate(cost.text, color=COST, scale_factor=1.06), run_time=0.6)

        self.play(FadeOut(VGroup(trk, ref, dfc, yt9, meter)), run_time=0.6)
        self.remove(trk, ref, dfc, yt9, meter)
        self.wait(0.4)
