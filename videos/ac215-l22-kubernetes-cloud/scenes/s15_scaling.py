"""S15 · Logs, then scaling at two levels (AC215 L22, the full follow-along). TRACKER [G] 1 → 4
(beats 0-3), 4 · extra (beat 4), then (beats 5-10: the scaling half has no README step) the tracker
gives way to a GREY breadcrumb 'extra · scaling (no README step)' in its corner. Lecture: 22 · 18 (beat 5), 43 (beat 6).

Beats (script.md "## S15", one voiceover block each):
0. TRACKER [G] 1. A 4-row 20 pt toolbox terminal on the stand-in (title 'laptop · toolbox ·
   stand-in', standin row tag on the bar) types `k30:1` (folds) → TERM(k30: 2) RED (wrapped). The
   terminal leaves; the GREY README card 'README.md · lines 620–656' brings all 14 commands (the
   typed one first, the other 13 in a LaggedStart) while the tracker steps 1 → 4. On "they all fail"
   every 'cheese-app-cluster-namespace' turns RED in one sweep and the RED badge '✗ 14/14' stamps the
   card; on "most" a GREY strip under it prints TERM(k33: 2) (README:631, the one that answers
   differently).
1. The k33 strip leaves; two RED strips print TERM(k34: 2) and TERM(k36: 2) (no typing); on the card
   the '<' and '>' of the three '<pod-name>' turn PINK on a faint PINK glow, a PINK label 'redirection' with the 'erratum'
   tag beside line 634; on "replace the whole placeholder" the three placeholders flash.
2. The README card and strips leave. A GREEN card (tag 'extra · our spelling', no output) types its
   five lines one by one; 'cheese-app-namespace' flashes GREEN; a GREY chip "your pod's name" under
   the card points at 'xxxxx'; the GREY chip "drop -c wait-for-chromadb: the Job has one container";
   a YELLOW '▶ your turn'.
3. TRACKER [G] 4 · extra. A 10-row stand-in terminal (row tags 'extra' and 'stand-in: kind, not GKE'
   on the bar): `k60:1` (folds) → TERM(k60: 2, 4–5, 8; the 'condition met' line is left out so
   the command head stays on screen with its output); `kubectl logs job/hello-job` → TERM(k61: 2–3);
   `kubectl describe job hello-job` → TERM(k62: 18, 41–42 wrapped). Above it V4's Job cousin
   (ControllerLoop(job=True, name='hello-job', api=False)): the GREEN Job card emits one TEAL Pod that
   runs and turns 'Completed' GREY; on "done, one succeeded" 'done' and '1 Succeeded' flash; on
   "Nothing replaces" the finished Pod flashes and a GREY 'not replaced' appears under it.
4. A GREY note (tag 'erratum'): CODE(setup_containers.py: 150) and, with it, the GREY chip "today's
   chroma image writes to /data" (flashes on "but today's Chroma image"; both hold 2 s), and under them a GREY line 'so the disk stays empty · after a vector-db
   restart, run the loader Job again'. Fade.
5. The tracker leaves for the breadcrumb 'extra · scaling (no README step)'. LECTURE 22 · 18. A GREY card 'the lecture: scale by CPU, memory, custom
   metrics'; under it the GREY README heading card (README.md · line 392) 'Deployment with Scaling
   using Kubernetes', 'Scaling' YELLOW, tag 'erratum', and two RED crosses 'no replicas' · 'no Pod
   autoscaler'; then CODE(create_cluster.py: 63–66) with lines 64–65 GREEN and '1' / '2' flashing.
6. LECTURE 22 · 43. V8 BinPacking (tag 'illustration'): node 1's shelf ('allocatable: less than its
   8 GB'), the requests legend (frontend 250m / 2Gi, vector-db 100m / 128Mi, nginx 100m / 128Mi, api
   none) and CODE(setup_containers.py: 79–82) inset, line 80 YELLOW; the blocks drop in as named:
   frontend (fat), vector-db and nginx (small), 'api ?' dashed (no request).
7. A GREEN card (tags 'extra · our spelling' and the GREY chip 'Milestone 5 · show scaling') types
   `kubectl scale deployment frontend --replicas=3 -n cheese-app-namespace`; a small GREY recall of
   k55 ('S07 · the same command on the game', k55:2, tag 'stand-in'). Two fat blocks drop: one fits,
   the next hovers RED 'Pending' and the inset 'V1 · scheduler' lamp lights RED; node 2 slides in
   (GREY chip 'cluster autoscaler · max 2') and the block lands. On "Ask for many more" four more
   blocks: two land on node 2 (it holds three), two hover 'Pending'; the autoscaler chip flashes RED.
8. The "many more" blocks leave (back to three frontends). The BLUE disk 'persistent-pvc' is chained
   to node 1 under the api block, the PINK chip 'ReadWriteOnce · one node at a time', CODE inset
   setup_containers.py: 24 (cut after the access mode) top right with the access mode PINK; the RED
   chip 'thought experiment · don't run it'; a YELLOW question card. PONDER (10 s).
9. The ponder card and question card leave. A second api block on node 2 reaches for the disk; the
   RED chain snaps 'Multi-Attach'; the block stays 'ContainerCreating'; a GREY-dashed node 3 is
   crossed out RED ('more nodes don't help'); the disk flashes.
10. The small AsksChecklist (Failover and Load balancing ticked earlier) and V8's two levers: on
   "nodes automatically" a solid YELLOW tick on Scaling and the 'nodes' lever flashes; on "Pods in
   your hands" a GREY-dashed half tick and the 'Pods' lever flashes; on "a Pod autoscaler" the dashed
   'HPA: not configured · needs requests' chip and the 'api ?' block flash. A GREEN card (tag 'extra ·
   our spelling') types `kubectl scale deployment frontend --replicas=1 \\ / -n cheese-app-namespace`.
   Fade; empty frame.

Deviations from SHOW:
- Beat 0: the README card holds all 14 commands (the typed one moves into it first), so its header
  'lines 620–656' and the badge '✗ 14/14' count what is on it. The rows are in the label font: in
   mono at 20 pt the longest command (88 characters) is 14.7 units wide and would need six folded
   rows; in the label font every command fits one row (10.9 units) and the card fits above the
   strips. The card's header is its first row; the strips each carry the README line they answer.
- Beat 3: the Job cousin sits above the terminal (the terminal is full width, house rule).
- Beat 4: SHOW names only the code line and the chip; the GREY line under them says what the
  narration asks the chip to explain (the PVC at /chroma/chroma stays empty, so run the loader again).
- Beat 6: V8's blocks carry the Deployment names; the request sizes are on the legend card beside them
  (BinPacking's blocks are named only, and 'frontend 250m / 2Gi' inside a 1.6-wide block would be
  under 20 pt).
- Beat 7: "Ask for many more" has no command on screen (script.md: the SAY says "some stay pending";
  no --replicas number is shown); the drawing adds five blocks so that some hover (illustration).
  The V1 scheduler lamp is a small inset 'V1 · scheduler' with one lamp (V1 itself is not on screen).
- Beat 8: the "many more" blocks leave first so that node 2 has room for the thought experiment's
  api block (back to the three frontends of beat 7's command).
- Beat 10: the two levers (BRIEF V8) carry the notes 'nodes: GKE autoscaler 1–2: on' and 'Pods: you:
  kubectl scale' + the dashed 'HPA: not configured · needs requests' chip; the small checklist has no
  note rows. The scale-back card folds the command over two rows with a shell ' \\' (the small
  checklist holds the top-right corner).
- Beats 6-10: the blocks use S15's own widths (frontend 1.8, vector-db 1.26, nginx 0.85, api 0.95), so
  a node holds at most three 2Gi frontends (four would exceed its allocatable memory) and node 1 still
  takes its fifth block.
Critic fixes (2026-11-08): beat 0's terminal has 6 rows (the folded k30 command and its wrapped error
  stay on screen together); beat 5 lights 'CPU', 'memory', 'custom metrics' as they are named; beat 7's
  Milestone chip sits bottom right and leaves before node 2 slides in, and the second "many more"
  Pending block moves beside the first (the shared stack covered its 'Pending'); the ponder card sits
  right of the disk so the api block, the disk and the thought-experiment chip stay visible; beat 10
  drops the thought experiment's api block and its 'ContainerCreating' with the chain.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S15"]
assert len(SAY) == SAY_COUNT["S15"] == 11

# ------------------------------------------------------------------ the real sources (checked)
K30, K33, K34, K36, K55, K60, K61, K62 = (capture(k) for k in ("k30", "k33", "k34", "k36", "k55", "k60", "k61", "k62"))
DEBUG_ROWS = [s for s in readme_rows(620, 656) if not s.startswith("#")]
DEBUG_LINES = (620, 623, 626, 631, 634, 635, 638, 639, 642, 643, 646, 649, 653, 656)
assert len(DEBUG_ROWS) == 14 and all(readme(n) == r for n, r in zip(DEBUG_LINES, DEBUG_ROWS))
assert K30.cmd == readme(620) and K33.cmd == readme(631) and K34.cmd == readme(634) and K36.cmd == readme(638)
assert 'namespaces "cheese-app-cluster-namespace" not found' in K30.line(2)
assert K33.line(2) == "No resources found in cheese-app-cluster-namespace namespace."
assert "syntax error near unexpected token" in K34.line(2)
assert K36.line(2) == "bash: line 1: pod-name: No such file or directory"
assert K55.line(2) == "deployment.apps/web scaled"
assert K60.line(8).startswith("pod/hello-job-") and "Completed" in K60.line(8)
assert K61.cmd == "kubectl logs job/hello-job" and K61.at((2, 3)) == ["loading...", "done"]
assert K62.cmd == "kubectl describe job hello-job" and "1 Succeeded" in K62.line(18)
assert "Completed" in K62.line(42)
SC = "src/deployment/deploy_k8s/setup_containers.py"
CC = "src/deployment/deploy_k8s/create_cluster.py"
assert 'mount_path="/chroma/chroma"' in excerpt(SC, 150, 150)
assert 'requests={"cpu": "250m", "memory": "2Gi"}' in excerpt(SC, 80, 80)
assert 'access_modes=["ReadWriteOnce"]' in excerpt(SC, 24, 24)
assert "min_node_count=1" in excerpt(CC, 64, 64) and "max_node_count=2" in excerpt(CC, 65, 65)
assert readme(392) == "## Deployment with Scaling using Kubernetes"
FIXED = ["kubectl logs -n cheese-app-namespace job/vector-db-loader",
         "kubectl describe job vector-db-loader -n cheese-app-namespace",
         "kubectl get pods -n cheese-app-namespace | grep vector-db-loader",
         "kubectl logs -n cheese-app-namespace vector-db-loader-xxxxx",
         "kubectl logs deployment/api -n cheese-app-namespace -f"]
SCALE3 = "kubectl scale deployment frontend --replicas=3 -n cheese-app-namespace"
SCALE1 = ["kubectl scale deployment frontend --replicas=1 \\", "  -n cheese-app-namespace"]

P_K8S = toolbox_prompt("/app/deploy_k8s")
SIZE = 20


def tb(rows: int) -> Terminal:
    """The 20 pt stand-in toolbox terminal (72 characters a row), bottom edge at BOTTOM."""
    return term(P_K8S, rows, T_TB_STANDIN, size=SIZE)


def mrow(s: str, color=INK) -> VGroup:
    return mono_line(s, SIZE, color)


def lrow(s: str, color=INK) -> Text:
    """A label-font row whose glyphs map one to one onto its non-space characters (checked: a
    ligature would merge two)."""
    t = label(s, SIZE, color)
    assert len(t.submobjects) == len("".join(s.split())), s
    return t


def lsub(t: Text, sub: str, occurrence: int = 0) -> VGroup:
    """Glyphs of substring `sub` in an lrow (spaces have no glyphs)."""
    s = t.text
    i = -1
    for _ in range(occurrence + 1):
        i = s.find(sub, i + 1)
    if i < 0:
        raise ValueError(f"{sub!r} not in {s!r}")
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def typing(row, run_time: float = 0.6):
    """ANIM: a mono row appears glyph by glyph (typed into a card)."""
    return LaggedStart(*[FadeIn(g) for g in row.glyphs], lag_ratio=1.0, run_time=run_time)


def edge_tag(panel, tg, buff: float = 0.2, side=UR):
    """Put tag tg on the top edge of a card/panel, at its right end (side=UL: left end)."""
    fr = panel.frame
    if side is UL:
        return tg.move_to(fr.get_corner(UL) + np.array([tg.width / 2 + buff, 0, 0]))
    return tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - buff, 0, 0]))


def strip(where: str, s: str, color) -> VGroup:
    """A printed capture line in a thin GREY frame, with the README line it answers on the left."""
    head = label(where, SIZE, S.GREY)
    row = mrow(s, color)
    inner = VGroup(head, row).arrange(RIGHT, buff=0.3)
    fr = frame_box(inner.width + 0.4, 0.5, S.GREY, k=0.08)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.row = fr, row
    return g


def fit_row(rows, x0: float, y: float, gap: float = 0.3):
    """Lay chips out in one row from x0."""
    g = VGroup(*rows).arrange(RIGHT, buff=gap)
    return g.move_to([x0 + g.width / 2, y, 0])


class LogsAndScaling(VoiceScene):
    def construct(self):
        trk = tracker_g(1)

        # ========================================================== 0. k30, then all fourteen on the card
        t = tb(6)                               # k30:1 folds onto 3 rows + 3 wrapped error rows: no scroll
        sb = on_bar(t, standin_row()).set_z_index(5)
        rows = [lrow(r) for r in DEBUG_ROWS]
        body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.055)
        rc = readme_card((620, 656), body, size=SIZE)
        rc.move_to([0, 0, 0])
        rc.shift(UP * (2.82 - rc.get_top()[1]))
        assert rc.width < 13.0 and rc.get_top()[1] < TRACK_BOTTOM - 0.05, (rc.width, rc.get_top())
        ns = [lsub(r, OLD_NAMESPACE) for r in rows]
        badge_txt = label("14/14", 26, ERR)
        badge_x = cross_glyph(0.3)
        badge_in = VGroup(badge_x, badge_txt).arrange(RIGHT, buff=0.15)
        badge_fr = RoundedRectangle(width=badge_in.width + 0.45, height=badge_in.height + 0.3, corner_radius=0.12,
                                    stroke_color=ERR, stroke_width=4).set_fill(S.BG, 0.92)
        badge_in.move_to(badge_fr)
        badge = VGroup(badge_fr, badge_in).rotate(8 * DEGREES).set_z_index(5)
        badge.move_to([min(6.45, rc.frame.get_right()[0] + 0.5) - badge.width / 2,
                       (rows[12].get_y() + rows[13].get_y()) / 2, 0])
        assert badge.get_left()[0] > rows[11].get_right()[0] + 0.15, (badge.get_left(), rows[11].get_right())
        s33 = strip("README:631", K33.line(2), OUTPUT)
        s33.next_to(rc, DOWN, buff=0.12)
        assert s33.get_bottom()[1] > -3.55, s33.get_bottom()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.2), FadeIn(sb), run_time=0.5)
            typed = type_capture(self, t, K30, type_time=0.8)[0]
            out(self, t, [(K30.line(2), ERR)], wrap=True, run_time=0.3)
            vo.wait_until("14 kubectl commands")
            src = VGroup(*rows_of(typed))
            self.play(FadeIn(rc.frame), FadeIn(rc.head), FadeTransform(src.copy(), rows[0]),
                      FadeOut(VGroup(t, sb)), run_time=0.7)
            self.remove(t, sb)
            for k, grp in ((2, rows[1:5]), (3, rows[5:9]), (4, rows[9:])):
                self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in grp], lag_ratio=0.25),
                          track(trk, k), run_time=0.5)
            self.add(rc)
            vo.wait_until("As typed, they all fail")
            self.play(LaggedStart(*[n.animate.set_color(ERR) for n in ns], lag_ratio=0.08), run_time=1.0)
            self.play(FadeIn(badge, scale=1.6), run_time=0.4)
            vo.wait_until("most say")
            self.play(FadeIn(s33, shift=DOWN * 0.1), Indicate(rows[3], color=S.GREY, scale_factor=1.04),
                      run_time=0.5)
            self.add(rc)
            vo.wait_until("is not found")
            self.play(LaggedStart(*[Indicate(n, color=ERR, scale_factor=1.06) for n in ns], lag_ratio=0.05),
                      run_time=1.0)
            self.add(rc)

        # ========================================================== 1. <pod-name>: shell redirections
        s34 = strip("README:634", K34.line(2), ERR)
        s36 = strip("README:638", K36.line(2), ERR)
        s34.next_to(rc, DOWN, buff=0.1)
        s36.next_to(s34, DOWN, buff=0.06)
        assert s36.get_bottom()[1] > -3.58, s36.get_bottom()
        pods = [r for r in rows if "<pod-name>" in r.text]
        assert len(pods) == 3
        brackets = VGroup(*[VGroup(lsub(r, "<"), lsub(r, ">")) for r in pods])
        names = [lsub(r, "<pod-name>") for r in pods]
        glows = VGroup(*[hl_bar(g, ROUTE, 0.3, 0.03) for b in brackets for g in b]).set_z_index(4)
        redir = VGroup(label("redirection", SIZE, ROUTE), erratum_tag()).arrange(RIGHT, buff=0.25)
        redir.set_z_index(5)
        redir.next_to(pods[0], RIGHT, buff=0.45)
        assert redir.get_right()[0] < badge.get_left()[0] or redir.get_bottom()[1] > badge.get_top()[1]
        assert redir.get_right()[0] < 6.5
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(s33), run_time=0.3)
            self.remove(s33)
            self.play(FadeIn(s34, shift=DOWN * 0.1), Indicate(pods[0], color=S.GREY, scale_factor=1.04),
                      run_time=0.5)
            self.play(FadeIn(s36, shift=DOWN * 0.1), Indicate(pods[1], color=S.GREY, scale_factor=1.04),
                      run_time=0.5)
            self.add(rc)
            vo.wait_until("are shell redirections")
            self.play(brackets.animate.set_color(ROUTE), FadeIn(glows), run_time=0.4)
            self.play(LaggedStart(*[Indicate(b, color=ROUTE, scale_factor=1.6) for b in brackets], lag_ratio=0.2),
                      FadeIn(redir, shift=LEFT * 0.1), run_time=0.9)
            self.add(rc)
            vo.wait_until("replace the whole placeholder")
            self.play(LaggedStart(*[Indicate(n, color=TURN, scale_factor=1.12) for n in names], lag_ratio=0.2),
                      run_time=1.0)
            self.add(rc)
        self.play(FadeOut(VGroup(rc, badge, s34, s36, redir, glows)), run_time=0.5)
        self.remove(rc, badge, s34, s36, redir, glows)

        # ========================================================== 2. the corrected commands (no output)
        fx = [mrow(s) for s in FIXED]
        fixc = card(fx, OWN, size=SIZE, buff=0.14, head="our spelling · no output")
        fixc.move_to([0, 0, 0]).shift(UP * (2.75 - fixc.get_top()[1]))
        ftag = edge_tag(fixc, extra_tag("our spelling")).set_z_index(5)
        assert ftag.get_top()[1] < TRACK_BOTTOM - 0.02 or ftag.get_left()[0] > trk.get_right()[0] + 0.1
        xx = substring(fx[3], "xxxxx")
        pod_chip = grey_chip("your pod's name")
        pod_chip.move_to([xx.get_x(), fixc.get_bottom()[1] - 0.55, 0])
        keep_inside(pod_chip)
        pod_ar = arrow(pod_chip.get_top(), xx.get_bottom(), S.GREY, stroke=3, buff=0.08)
        drop = VGroup(grey_chip("drop  -c wait-for-chromadb", mono_font=True),
                      label("the Job has one container", SIZE, S.GREY)).arrange(RIGHT, buff=0.25)
        drop.move_to([0, pod_chip.get_bottom()[1] - 0.55, 0])
        yt = your_turn().next_to(drop, DOWN, buff=0.4)
        assert yt.get_bottom()[1] > -3.5
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(fixc.frame), FadeIn(fixc.head), FadeIn(ftag), run_time=0.4)
            vo.wait_until("the namespace is")
            for r in fx[:3]:
                self.play(typing(r, 0.45))
            self.play(LaggedStart(*[substring(r, NAMESPACE).animate.set_color(OWN) for r in fx[:3]],
                                  lag_ratio=0.2), run_time=0.6)
            self.add(fixc)
            vo.wait_until("and the Job has one container")
            self.play(typing(fx[3], 0.45))
            self.play(FadeIn(pod_chip, shift=UP * 0.1), GrowArrow(pod_ar), run_time=0.4)
            self.play(FadeIn(drop, shift=UP * 0.1), run_time=0.4)
            self.play(typing(fx[4], 0.45))
            self.play(LaggedStart(*[substring(r, NAMESPACE).animate.set_color(OWN) for r in fx[3:]],
                                  lag_ratio=0.2), Indicate(drop[0].text, color=INK, scale_factor=1.06), run_time=0.6)
            self.add(fixc)
            vo.wait_until("Pause and try them")
            self.play(FadeIn(yt, shift=RIGHT * 0.15), run_time=0.4)
            flash_tag(self, yt, TURN)
        self.play(FadeOut(VGroup(fixc, ftag, pod_chip, pod_ar, drop, yt)), run_time=0.5)
        self.remove(fixc, ftag, pod_chip, pod_ar, drop, yt)

        # ========================================================== 3. a Job that exists, on the stand-in
        t = tb(10)                              # k60:1 folds onto 5 rows + 4 output rows + the prompt
        sb = on_bar(t, standin_row()).set_z_index(5)
        xb = extra_row().set_z_index(5)
        xb.move_to([t.box.get_left()[0] + 1.3 + xb.width / 2, sb.get_y(), 0])
        assert xb.get_right()[0] < t.title.get_left()[0] - 0.1, (xb.get_right(), t.title.get_left())
        job = ControllerLoop(job=True, name="hello-job", api=False)
        job.shift(UP * 1.9)                      # built in y -0.75 .. 0.95: now 1.15 .. 2.85, under the tracker
        assert t.box.get_top()[1] < 1.15 - 0.1, t.box.get_top()
        with self.voiceover(SAY[3]) as vo:
            self.play(track(trk, 4, True), FadeIn(t, shift=UP * 0.2), FadeIn(sb), FadeIn(xb), run_time=0.5)
            job.job_card(self)
            type_capture(self, t, K60, type_time=0.35)
            out(self, t, K60.at(2, (4, 5), 8), run_time=0.4)   # 5 + 4 rows + the prompt: the command head stays
            job.run_job(self)
            vo.wait_until("the same commands work")
            type_capture(self, t, K61, type_time=0.3)
            r61 = out(self, t, K61.at((2, 3)), run_time=0.3)
            type_capture(self, t, K62, type_time=0.3)
            r62 = out(self, t, K62.at(18, (41, 42)), wrap=True, run_time=0.4)
            vo.wait_until("done, one succeeded")
            done = next(r for r in r61 if r.text == "done")
            succ = substring(next(r for r in r62 if "1 Succeeded" in r.text), "1 Succeeded")
            self.play(Indicate(done, color=OWN, scale_factor=1.15), Indicate(succ, color=OWN, scale_factor=1.1),
                      run_time=0.7)
            self.add(t)
            vo.wait_until("Nothing replaces")
            nr = label("not replaced", SIZE, S.GREY).next_to(job.jpod, RIGHT, buff=0.35)
            self.play(Indicate(job.jpod.circle, color=S.GREY, scale_factor=1.2), run_time=0.6)
            job.show(self, nr, run_time=0.4)
        self.play(FadeOut(VGroup(t, sb, xb, job)), run_time=0.5)
        self.remove(t, sb, xb, job)

        # ========================================================== 4. erratum: Chroma writes to /data
        cp = code(SC, 150, 150, font_size=SIZE, dedent=True, shown="deploy_k8s/setup_containers.py")
        dchip = grey_chip("today's chroma image writes to /data")
        top = VGroup(cp, dchip).arrange(RIGHT, buff=0.4)
        why = label("so that disk stays empty · after a vector-db restart, run the loader Job again", SIZE, S.GREY)
        note_g = VGroup(top, why).arrange(DOWN, buff=0.45).move_to([0, 0.4, 0])
        assert note_g.width < 13.0, note_g.width
        etag = erratum_tag().next_to(top, UP, buff=0.3).align_to(top, LEFT)
        mp = code_span(cp.code, 0, '"/chroma/chroma"')
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeIn(etag, shift=DOWN * 0.1), FadeIn(cp, shift=UP * 0.1), FadeIn(dchip, shift=LEFT * 0.15),
                      run_time=0.5)                 # the cause is up before the conclusion line
            self.play(mp.animate.set_color(ERR), run_time=0.3)
            self.add(cp)
            vo.wait_until("but today's Chroma image")
            self.play(Indicate(dchip.text, color=INK, scale_factor=1.06), run_time=0.6)
            self.add(dchip)
            vo.wait_until("So the vectors live")
            self.play(FadeIn(why, shift=UP * 0.1), run_time=0.5)
        self.wait(2.0)                              # the chip and the why line hold together
        self.play(FadeOut(VGroup(cp, dchip, why, etag)), run_time=0.4)
        self.remove(cp, dchip, why, etag)

        # ========================================================== 5. the promise, the README title, the code
        ref = lref("18")
        crumb = label("extra · scaling (no README step)", trk.size, S.GREY)
        crumb.move_to([TRACK_LEFT + crumb.width / 2, TRACK_TOP - crumb.height / 2, 0])
        lec = card(["scale by CPU, memory, custom metrics"], S.GREY, size=24, head="the lecture")
        lec.move_to([0, 2.15, 0])
        assert lec.get_top()[1] < crumb.get_bottom()[1] - 0.05 or lec.get_left()[0] > crumb.get_right()[0]
        hd = lrow("Deployment with Scaling using Kubernetes")
        hd.scale(1.0)
        rh = readme_card(392, hd, size=SIZE)
        rh.next_to(lec, DOWN, buff=0.35)
        rtag = edge_tag(rh, erratum_tag()).set_z_index(5)
        crosses = VGroup(*[VGroup(cross_glyph(0.28), mono(s, SIZE, ERR) if m else label(s, SIZE, ERR))
                           .arrange(RIGHT, buff=0.15) for s, m in (("no replicas", True), ("no Pod autoscaler", False))])
        for c_ in crosses:
            c_[1].set_color(ERR)
        crosses.arrange(RIGHT, buff=0.8).next_to(rh, DOWN, buff=0.3)
        cc = code(CC, 63, 66, font_size=SIZE, dedent=True, shown="deploy_k8s/create_cluster.py")
        cc.next_to(crosses, DOWN, buff=0.3)
        assert cc.get_bottom()[1] > -3.55, cc.get_bottom()
        bars = VGroup(line_bar(cc.code, 1, OWN, 0.2), line_bar(cc.code, 2, OWN, 0.2))
        cc.code.code_lines.set_z_index(2)
        bars.set_z_index(1)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(trk), FadeIn(crumb), FadeIn(ref), FadeIn(lec, shift=DOWN * 0.1), run_time=0.6)
            self.remove(trk)
            vo.wait_until("The lecture promises")
            self.play(Indicate(lec.body[0], color=INK, scale_factor=1.05), run_time=0.8)
            self.add(lec)
            vo.wait_until("on CPU")                 # the three promised metrics, one by one as they are named
            words = [lsub(lec.body[0], w) for w in ("CPU", "memory", "custommetrics")]  # Text.text drops spaces
            self.play(LaggedStart(*[Indicate(w, color=TURN, scale_factor=1.12) for w in words], lag_ratio=0.6),
                      run_time=1.8)
            self.add(lec)
            vo.wait_until("but the code sets")
            self.play(FadeIn(rh, shift=DOWN * 0.1), FadeIn(rtag), run_time=0.4)
            self.play(lsub(hd, "Scaling").animate.set_color(TURN), run_time=0.3)
            self.add(rh)
            self.play(LaggedStart(*[FadeIn(c_, shift=UP * 0.1) for c_ in crosses], lag_ratio=0.5), run_time=0.7)
            vo.wait_until("It switches on the node layer")
            self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(bars), run_time=0.3)
            vo.wait_until("one to two nodes")
            self.play(Indicate(code_span(cc.code, 1, "1"), color=OWN, scale_factor=1.4),
                      Indicate(code_span(cc.code, 2, "2"), color=OWN, scale_factor=1.4), run_time=0.7)
            self.add(cc)
        self.play(FadeOut(VGroup(lec, rh, rtag, crosses, cc, bars, ref)), run_time=0.5)
        self.remove(lec, rh, rtag, crosses, cc, bars, ref)

        # ========================================================== 6. V8: packing by requests
        ref = lref("43")
        bp = BinPacking()
        # a node takes at most three 2Gi frontends (4 x 2Gi > its allocatable memory): the frontend is
        # fat enough that node 2 holds three and a fourth pends, while node 1 still fits its own five
        bp.SIZES = {"frontend": 1.8, "vector-db": 1.26, "nginx": 0.85, "api": 0.95}
        bp.shift(DOWN * 0.45)
        itag = illustration_tag().move_to([1.0 - 0.0, 1.38, 0])
        itag.shift(LEFT * itag.width / 2)
        cr = code(SC, 79, 82, font_size=SIZE, dedent=True, shown="deploy_k8s/setup_containers.py")
        cr.move_to([0, 0, 0]).align_to([-6.3, 0, 0], LEFT).shift(UP * (-1.25 - cr.get_top()[1]))
        assert cr.get_bottom()[1] > -3.55 and cr.get_right()[0] < 3.3, (cr.get_bottom(), cr.get_right())
        b80 = line_bar(cr.code, 1, TURN, 0.2)
        cr.code.code_lines.set_z_index(2)
        b80.set_z_index(1)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(ref), run_time=0.3)
            bp.node(self, 0)
            self.play(FadeIn(itag), run_time=0.3)
            bp.legend(self)
            assert bp.legend_g.get_left()[0] > cr.get_right()[0] + 0.05, (bp.legend_g.get_left(), cr.get_right())
            vo.wait_until("The frontend asks")
            bp.add_block(self, "frontend", 0)
            self.play(FadeIn(cr, shift=UP * 0.15), run_time=0.4)
            self.play(FadeIn(b80), Indicate(code_span(cr.code, 1, '"250m"'), color=TURN, scale_factor=1.15),
                      run_time=0.6)
            self.add(cr)
            vo.wait_until("Chroma and nginx")
            bp.add_block(self, "vector-db", 0, run_time=0.4)
            bp.add_block(self, "nginx", 0, run_time=0.4)
            vo.wait_until("and the API for nothing")
            api = bp.add_block(self, "api", 0, run_time=0.5)
            vo.wait_until("so nobody can plan")
            self.play(Indicate(api.text, color=TURN, scale_factor=1.15), run_time=0.6)
            bp.heal(self)
        self.play(FadeOut(VGroup(cr, b80, ref)), run_time=0.4)
        self.remove(cr, b80, ref)

        # ========================================================== 7. kubectl scale: Pending, then node 2
        sc_row = mrow(SCALE3)
        scard = card([sc_row], OWN, size=SIZE, buff=0.1)
        scard.move_to([0, 2.22, 0])
        stag = edge_tag(scard, extra_tag("our spelling")).set_z_index(5)
        mile = grey_chip("Milestone 5 · show scaling")
        mile.move_to([6.5 - mile.width / 2, -1.75, 0])     # clear of the Pending column (x 1.3 .. 3.0)
        assert scard.get_bottom()[1] > bp.nodes[0].get_top()[1] + 0.05, (scard.get_bottom(), bp.nodes[0].get_top())
        k55c = card([mrow(K55.line(2), OUTPUT)], S.GREY, size=SIZE, head="part 1 · the same command on the game", buff=0.1)
        k55c.move_to([6.5 - k55c.width / 2, -2.75, 0])
        k55t = tag("stand-in", S.GREY).next_to(k55c, LEFT, buff=0.15).align_to(k55c, UP)
        lmp = lamp("off", r=0.2)
        lmp_on = lamp("red", r=0.2)
        sched = VGroup(lmp, label("no node has room", SIZE, ERR)).arrange(RIGHT, buff=0.2)
        shd = label("V1 · the scheduler", SIZE, CLOUD)
        sfr = frame_box(max(sched.width, shd.width) + 0.5, sched.height + 0.75, CLOUD, k=0.06)
        VGroup(shd, sched).arrange(DOWN, buff=0.12).move_to(sfr)
        inset = VGroup(sfr, shd, sched)
        inset.move_to([6.5 - inset.width / 2, 0.2, 0])
        lmp_on.move_to(lmp)
        with self.voiceover(SAY[7]) as vo:
            bp.drop(self, bp.legend_g, run_time=0.3)
            self.play(FadeIn(scard.frame), FadeIn(stag), run_time=0.3)
            self.play(typing(sc_row, 0.9))
            vo.wait_until("Milestone 5")
            self.play(FadeIn(mile, shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(k55c, shift=LEFT * 0.15), FadeIn(k55t), run_time=0.5)
            vo.wait_until("A copy that does not fit")
            self.play(FadeOut(VGroup(k55c, k55t)), run_time=0.3)
            self.remove(k55c, k55t)
            bp.add_block(self, "frontend", run_time=0.5)
            pend = bp.add_block(self, "frontend", run_time=0.6)
            self.play(FadeIn(inset), run_time=0.3)
            self.play(FadeTransform(lmp, lmp_on), run_time=0.3)
            inset.remove(sched)
            sched.remove(lmp)
            sched.add(lmp_on)
            inset.add(sched)
            self.add(inset)
            vo.wait_until("until the autoscaler adds")
            self.play(FadeOut(mile), run_time=0.3)   # node 2 slides in from the right, through this corner
            self.remove(mile)
            bp.node(self, 1)
            bp.land(self, pend, 1)
            self.play(FadeOut(inset), run_time=0.3)
            self.remove(inset)
            vo.wait_until("Ask for many more")
            for _ in range(4):                     # two land (node 2 holds three), two pend
                bp.add_block(self, "frontend", run_time=0.3)
            assert len(bp.blocks[1]) == 3 and len(bp.pending) == 2
            p1, p2 = bp.pending[-2:]               # the shared stack puts p2 over p1's 'Pending': side by side
            self.play(p2.animate.move_to(p1.get_center() + RIGHT * (p1.width + 0.3)), run_time=0.4)
            bp.heal(self)
            vo.wait_until("the pool stops at two")
            flash_tag(self, bp.autoscaler_chip, ERR, 1.08)
            bp.heal(self)
        self.play(FadeOut(VGroup(scard, stag)), run_time=0.4)
        self.remove(scard, stag)

        # ========================================================== 8. the API's disk; ponder
        extra = bp.blocks[1][1:] + list(bp.pending)
        assert len(extra) == 4
        fr1 = bp.nodes[1].frame
        cr24 = code(SC, 24, 24, font_size=SIZE, dedent=True, cuts={24: '["ReadWriteOnce"],'},
                    shown="deploy_k8s/setup_containers.py")
        cr24.move_to([6.5 - cr24.width / 2, 2.75 - cr24.height / 2, 0])
        rwo = code_span(cr24.code, 0, '"ReadWriteOnce"')
        thought = err_chip("thought experiment · don't run it", mono_font=False)
        thought.move_to([6.5 - thought.width / 2, 1.0, 0])
        q = question_card("What happens to them?\nCan the autoscaler fix it?", size=24)
        q.move_to([6.5 - q.width / 2, -1.4, 0])
        assert cr24.get_bottom()[1] > thought.get_top()[1] + 0.05 and thought.get_bottom()[1] > q.get_top()[1] + 0.05
        with self.voiceover(SAY[8]) as vo:
            bp.drop(self, *extra, run_time=0.4)
            bp.blocks[1] = bp.blocks[1][:1]
            bp.pending.clear()
            bp.cursor[1] = fr1.get_left()[0] + 0.1 + bp.SIZES["frontend"] + 0.08
            vo.wait_until("The API's disk")
            bp.disk(self)
            rw = bp.disk_g.rwo
            self.play(rw.animate.next_to(bp.disk_g[2], RIGHT, buff=0.3), run_time=0.5)
            bp.heal(self)
            assert rw.get_bottom()[1] > q.get_top()[1] + 0.05 and rw.get_top()[1] < bp.nodes[0].get_bottom()[1]
            self.play(FadeIn(cr24, shift=LEFT * 0.15), run_time=0.4)
            self.play(rwo.animate.set_color(ROUTE), run_time=0.3)
            self.play(Indicate(rwo, color=ROUTE, scale_factor=1.1), Indicate(bp.disk_g.rwo.text, color=ROUTE,
                                                                             scale_factor=1.06), run_time=0.7)
            self.add(cr24)
            bp.heal(self)
            vo.wait_until("Suppose you scaled the API")
            self.play(FadeIn(thought, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("What happens to them")
            self.play(FadeIn(q, scale=0.95), run_time=0.4)
        self.play(FadeOut(q), run_time=0.3)
        self.remove(q)
        pc = ponder(self, "Suppose api had 3 replicas.\nSome Pods land on node 2.\nWhat happens to them,\n"
                          "and can the autoscaler fix it?", 10, center=(3.45, -1.4), width=6.0)
        assert pc.get_bottom()[1] > -3.55 and pc.get_right()[0] < 6.55 and pc.get_top()[1] < thought.get_bottom()[1], pc
        assert pc.get_left()[0] > bp.disk_g.cyl.get_right()[0] + 0.3, (pc.get_left(), bp.disk_g.cyl.get_right())

        # ========================================================== 9. Multi-Attach
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            bp.multi_attach(self)
            vo.wait_until("the disk already sits on node 1")
            self.play(Indicate(bp.disk_g.cyl, color=CLOUD, scale_factor=1.2), run_time=0.6)
            bp.heal(self)
            vo.wait_until("More nodes do not help")
            bp.ghost_node(self)
            vo.wait_until("the limit is the disk")
            self.play(Indicate(bp.disk_g.cyl, color=ERR, scale_factor=1.2),
                      Indicate(bp.snap[2], color=ERR, scale_factor=1.1), run_time=0.7)
            bp.heal(self)

        # ========================================================== 10. two levels; scale back to 1
        asks = AsksChecklist(small=True, ticked=(0, 1))
        s1 = [mrow(s) for s in SCALE1]
        bcard = card(s1, OWN, size=SIZE, buff=0.1)
        bcard.move_to([-6.3 + bcard.width / 2, 2.2, 0])
        btag = edge_tag(bcard, extra_tag("our spelling")).set_z_index(5)
        assert bcard.get_right()[0] < asks.get_left()[0] - 0.1, (bcard.get_right(), asks.get_left())
        assert btag.get_left()[0] > crumb.get_right()[0] + 0.05 or btag.get_top()[1] < crumb.get_bottom()[1]
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(cr24, thought)), run_time=0.3)
            self.remove(cr24, thought)
            api2 = bp.blocks[1].pop()               # the thought experiment's api block (never ran)
            assert api2.key == "api"
            bp.drop(self, bp.disk_g.rwo, bp.snap[1], bp.snap[2], bp.snap[3], api2, bp.ghost, run_time=0.4)
            self.play(FadeIn(asks, shift=LEFT * 0.15), run_time=0.5)
            bp.levers(self)
            lv = bp.levers_g
            vo.wait_until("nodes automatically")
            asks.tick(self, 2)
            self.play(Indicate(lv[0][1][1], color=TURN, scale_factor=1.06), run_time=0.5)
            bp.heal(self)
            vo.wait_until("Pods in your hands")
            asks.tick(self, 2, dashed=True)
            self.play(Indicate(lv[0][0][1], color=INK, scale_factor=1.06), run_time=0.5)
            bp.heal(self)
            vo.wait_until("a Pod autoscaler on CPU needs requests")
            self.play(Indicate(lv[1].text, color=INK, scale_factor=1.06), run_time=0.6)
            bp.heal(self)
            vo.wait_until("and the API has none")
            api0 = next(b for b in bp.blocks[0] if b.key == "api")
            self.play(Indicate(api0.text, color=TURN, scale_factor=1.15), run_time=0.6)
            bp.heal(self)
            vo.wait_until("Scale back to 1")
            self.play(FadeIn(bcard.frame), FadeIn(btag), run_time=0.3)
            for r in s1:
                self.play(typing(r, 0.35))
            self.add(bcard)
            self.play(Indicate(substring(s1[0], "--replicas=1"), color=OWN, scale_factor=1.1), run_time=0.5)
            self.add(bcard)
        self.play(FadeOut(VGroup(bp, itag, asks, bcard, btag, crumb)), run_time=0.7)
        self.remove(bp, itag, asks, bcard, btag, crumb)
        self.wait(0.3)
