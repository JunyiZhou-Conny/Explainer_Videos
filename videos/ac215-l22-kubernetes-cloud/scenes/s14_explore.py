"""S14 · kubectl on the app, and the outputs (AC215 L22, the full follow-along). TRACKER [C] 5 (beats
0-2; · extra in beat 1), 6 (beats 3-4), 7 (beats 5-7). Lecture: 22 · 34–36 (beat 0), 33 (beat 1).

Beats (script.md "## S14", one voiceover block each):
0. TRACKER [C] 5. LECTURE 22 · 34–36. A 13-row 20 pt toolbox terminal at …:/app/deploy_k8s#: the five
   README commands (README:478–480, 484–485) as a fast montage, `kubectl get all` -> TERM(b40: 7),
   `kubectl get all --all-namespaces` -> TERM(b41: 7), `kubectl get pods --all-namespaces` ->
   TERM(b42: 7), `kubectl get componentstatuses` -> TERM(b43: 7), `kubectl get nodes` -> TERM(b44: 7);
   each line 7 RED (wrapped); on "all five say connection refused" the five 'refused' flash; on "any
   new toolbox session" a GREY chip 'new toolbox session · no kubeconfig (docker-shell.sh: --rm)'.
1. TRACKER [C] 5 · extra. LECTURE 22 · 33. The terminal shrinks to 5 rows (cleared); `gcloud container
   clusters get-credentials cheese-app-cluster --zone us-central1 --project your-gcp-project` (extra on
   the title bar; folds) -> TERM(b52: 2 wrap) RED ('active account' flashes). Above it the GREEN card
   (tag 'extra · our spelling', no output) with the --region form, '--region' YELLOW; on "The code
   passes the region" '--zone' in the typed command is underlined RED and the GREY chip 'the code
   passes the region to --zone' with its 'erratum' tag appears under the card.
2. TRACKER [C] 5. A GREY card 'what yours shows · no output here' whose rows arrive phrase by phrase
   (get all → only service/kubernetes; -n cheese-app-namespace → frontend-…, vector-db-…, api-…, the
   nginx controller, vector-db-loader-… Completed, job.batch/vector-db-loader 1/1; get nodes → 1 node,
   2 if the autoscaler added one). Under it two GREY stand-in thumbnails of S05's k03 and k07 (cropped
   columns), each tagged 'stand-in: kind, not GKE'.
3. TRACKER [C] 6. A 4-row toolbox terminal: `kubectl get pods --namespace=cheese-app-namespace` ->
   TERM(b45: 7 wrap) RED. A GREY README card 'README.md · lines 491–492' above it into which the other
   two commands type verbatim (no output); on "use the name" the Pod name 'api-c4fb784b-2llgs' is struck
   GREY in both and a YELLOW chip 'the name your first command prints' points at it.
4. A GREY recall card of S08's k51 (its two commands and line 3, tag 'stand-in: kind, not GKE'); a
   GREEN card 'inside the API Pod' (tag 'extra · our spelling', no output): `env | grep ROOT_PATH`, the
   GREY chip 'yours: ROOT_PATH=/api-service · setup_containers.py:310–311', then `exit` and a bare
   prompt back at …:/app/deploy_k8s# in the terminal; a YELLOW '▶ your turn'.
5. TRACKER [C] 7. EXPECTED(expected/readme-pulumi-outputs: 2–9) top left, tagged 'expected ·
   README:497–506'; CODE(src/deployment/deploy_k8s/__main__.py: 46–49) under it. 'ingress_name :
   "nginx-ingress"' and 'nginx_ingress_ip' RED with the 'erratum' tag; line 48 'ip_address' GREEN; the
   GREY chip 'setup_loadbalancer.py:65 → cheese-app-ingress'; an inset of c20:40 ('ip_address :
   [unknown]').
6. A schematic browser (tag 'illustration') at http://<IP>.sslip.io: a 'Formaggio' header bar, grey
   placeholder lines, the footer 'API version: 3.0' YELLOW; a YELLOW '▶ your turn' beside the address
   bar; a PINK arrow from the footer to '/api-service/status'; then the GREY chip 'chat › model: RAG
   (/chat?model=llm-rag)'.
7. The GREY two-row chip 'first moments: 502 / 503 → the API is still loading TensorFlow · wait,
   retry' (the 502 / 503 RED). Fade; empty frame.

Deviations from SHOW:
- The terminals are 20 pt (72 characters a row), as in S11/S12: b40-b45 line 7 (98 characters) and
  b52:2 wrap to two rows.
- Beat 0: SHOW names no picture for "the kubeconfig Pulumi wrote went away with the old container";
  a GREY chip above the terminal says it (docker-shell.sh:34 runs the toolbox with --rm).
- Beat 1: on "the zone flag" the typed command's '--zone' gets a RED underline, so the slip is seen in
  the line that carries it. The GREEN card splits the corrected command over two rows with a shell
  ' \\' continuation (61 characters a row at 20 pt).
- Beat 2: S05's k03/k07 rows are too wide for 'small thumbnails' at >= 20 pt: they are cropped after
  the TYPE (k03) and STATUS (k07) columns.
- Beat 3: README:492 (92 characters) wraps inside the README card after '--tty' (an indented second
  row that starts with the Pod name); the YELLOW chip sits between the card and the terminal with an
  arrow up to that struck name.
- Beat 4: the terminal shrinks to an empty 3-row strip (keeping b45's last rows left a dangling fold
  row without its prompt) to make room for the recall card and the GREEN card; after `exit` the bare
  prompt returns in it; '▶ your turn' sits under the ROOT_PATH chip.
- Beat 1: on "gcloud container clusters" the typed command's rows flash (the narration reads it out);
  the 'erratum' chip comes with the '--zone' underline, in the place the GREEN card then arrives above.
- Beat 5: CODE shows lines 46–49 instead of 43–49: seven code lines plus the 8-row Outputs panel do
  not fit the frame at >= 20 pt, and side by side neither fits the width. 46–49 hold the three names
  the narration compares (namespace, ingress_name, ip_address) and app_url. The c20:40 inset is a GREY
  card in the right-hand column with the capture line left-stripped.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S14"]
assert len(SAY) == SAY_COUNT["S14"] == 8

# ------------------------------------------------------------------ the real sources (checked)
MONTAGE = [capture(k) for k in ("b40", "b41", "b42", "b43", "b44")]
REFUSED = "The connection to the server localhost:8080 was refused - did you specify the right host or port?"
for _c, _n in zip(MONTAGE, (478, 479, 480, 484, 485)):
    assert _c.cmd == readme(_n), (_c.cmd, readme(_n))
    assert _c.line(7) == REFUSED
B45, B52, K03, K07, K51, C20 = (capture(k) for k in ("b45", "b52", "k03", "k07", "kind/k51", "c20"))
assert B45.cmd == readme(490) == "kubectl get pods --namespace=cheese-app-namespace" and B45.line(7) == REFUSED
assert B52.cmd == ("gcloud container clusters get-credentials cheese-app-cluster --zone us-central1 "
                   "--project your-gcp-project")
assert "You do not currently have an active account selected." in B52.line(2)
POD_README = "api-c4fb784b-2llgs"
R491, R492 = readme(491), readme(492)
assert R491 == f"kubectl get pod {POD_README} --namespace=cheese-app-namespace"
assert R492 == f"kubectl exec --stdin --tty {POD_README} --namespace=cheese-app-namespace  -- /bin/bash"
assert K03.line(3).startswith("service/kubernetes   ClusterIP")
assert all(" Ready " in K07.line(n) for n in (3, 4, 5))
assert K51.cmd_lines == ["kubectl exec --stdin --tty deployment/web -- /bin/sh", "hostname; ls; exit"]
assert K51.line(3) == f"web-{RS_HASH}-{POD_SUFFIXES[0]}"
C20_40 = C20.line(40).strip()
assert C20_40 == "ip_address      : [unknown]"
SC = "src/deployment/deploy_k8s/setup_containers.py"
assert 'name="ROOT_PATH"' in excerpt(SC, 310, 310) and 'value="/api-service"' in excerpt(SC, 311, 311)
assert 'name=f"{app_name}-ingress"' in excerpt("src/deployment/deploy_k8s/setup_loadbalancer.py", 65, 65)
MAIN = "src/deployment/deploy_k8s/__main__.py"
assert 'pulumi.export("ingress_name", ingress.metadata.name)' in excerpt(MAIN, 47, 47)
assert 'pulumi.export("ip_address", ip_address)' in excerpt(MAIN, 48, 48)
assert "API version: {version}" in excerpt("src/frontend-react/src/components/layout/Footer.jsx", 37, 37)
assert "formaggio.me" in excerpt("src/frontend-react/src/components/layout/Footer.jsx", 36, 36)  # Header.jsx:47 (h1 Formaggio) is not in assets/source
assert '"3.0"' in excerpt("src/api-service/api/service.py", 36, 36)
assert 'prefix="/llm-rag"' in excerpt("src/api-service/api/service.py", 44, 44)
assert "--rm" in source_text("src/deployment/docker-shell.sh")

P_K8S = toolbox_prompt("/app/deploy_k8s")
SIZE = 20


def tb(rows: int) -> Terminal:
    """The 20 pt toolbox terminal (72 characters a row), bottom edge at BOTTOM."""
    return term(P_K8S, rows, T_TOOLBOX, size=SIZE)


def row_with(rows, s: str):
    """The first printed row whose text contains s."""
    return next(r for r in rows if s in r.text)


def edge_tag(panel, tg, buff: float = 0.2):
    """Put tag tg on the top edge of a card/panel, at its right end."""
    fr = panel.frame
    return tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - buff, 0, 0]))


def mrow(s: str, color=INK, t2c=None) -> VGroup:
    return mono_line(s, SIZE, color, t2c=t2c)


def typing(row, run_time: float = 0.8):
    """ANIM: a mono row appears glyph by glyph (typed into a card)."""
    return LaggedStart(*[FadeIn(g) for g in row.glyphs], lag_ratio=1.0, run_time=run_time)


def thumb(cap, nums, upto: str, head: str) -> VGroup:
    """A GREY stand-in thumbnail: capture rows (file lines `nums`) cropped just before the column
    header `upto` (the next column), with a GREY head and the stand-in tag on its top edge."""
    hdr = cap.line(nums[0])
    cut_at = hdr.index(upto)
    rows = [mrow(cap.line(n)[:cut_at].rstrip(), OUTPUT) for n in nums]
    c = card(rows, S.GREY, size=SIZE, head=head, buff=0.1)
    tg = edge_tag(c, standin_tag()).shift(UP * 0.06)
    c.add(tg)
    c.tag, c.rows = tg, rows
    return c


class ExploreApp(VoiceScene):
    def construct(self):
        # ========================================================== 0. five README commands, five refusals
        trk = tracker_c(5)
        t = tb(13)
        ref = lref("34–36")
        gone = grey_chip("new toolbox session · no kubeconfig (docker-shell.sh runs it with --rm)")
        under_term(t, gone)
        refused = []
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.2), FadeIn(ref), run_time=0.6)
            for cap in MONTAGE:
                type_capture(self, t, cap, type_time=0.35)
                rows = out(self, t, [(cap.line(7), ERR)], wrap=True, run_time=0.25)
                refused.append(row_with(rows, "refused"))
            vo.wait_until("With no cluster here")
            live = [r for r in refused if r in t.lines.submobjects]
            self.play(each([substring(r, "refused") for r in live], ERR, 1.15, 0.12), run_time=1.0)
            self.add(t)
            vo.wait_until("You will see exactly this")
            self.play(FadeIn(gone, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("the kubeconfig Pulumi wrote")
            flash_tag(self, gone, INK, 1.05)
            self.play(FadeOut(ref), run_time=0.3)
        self.remove(ref)

        # ========================================================== 1. get-credentials, and the --region spelling
        ref = lref("33")
        fix = card([mrow("gcloud container clusters get-credentials cheese-app-cluster \\"),
                    mrow("  --region us-central1 --project <your project>")], OWN, size=SIZE, buff=0.12)
        substring(fix.body[1], "--region").set_color(TURN)
        substring(fix.body[1], "<your project>").set_color(S.GREY)
        fix.move_to([0, 1.75, 0])
        fix_tag = edge_tag(fix, extra_tag("our spelling"))
        assert fix_tag.get_top()[1] < TRACK_BOTTOM - 0.05
        slip = VGroup(grey_chip("the code passes the region to --zone"), erratum_tag()).arrange(RIGHT, buff=0.3)
        slip.next_to(fix, DOWN, buff=0.3)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(gone), FadeIn(ref), track(trk, 5, True), run_time=0.4)
            self.remove(gone)
            resize(self, t, 5, keep=[], run_time=0.5)
            xr = on_bar(t, extra_row())
            typed = type_capture(self, t, B52, type_time=0.9)[0]
            vo.wait_until("an extra here")
            self.play(FadeIn(xr), run_time=0.3)
            flash_tag(self, xr, INK, 1.08)
            e52 = out(self, t, [(B52.line(2), ERR)], wrap=True, run_time=0.3)
            self.play(Indicate(substring(row_with(e52, "active account"), "active account"), color=ERR,
                               scale_factor=1.12), run_time=0.6)
            self.add(t, xr)                                 # keep the 'extra' tag above the bar
            vo.wait_until("gcloud container clusters")
            _cr = rows_of(typed)
            _parts = [substring(_cr[0], "gcloud container clusters")] + [substring(r, r.text.strip().rstrip(" \\"))
                                                                          for r in _cr[1:]]
            self.play(each(_parts, TURN, 1.08, 0.35), run_time=1.4)
            self.add(t, xr)                                 # keep the 'extra' tag above the bar
            vo.wait_until("The code passes the region")
            zrow = row_with(rows_of(typed), "--zone")
            zu = under(substring(zrow, "--zone us-central1"), ERR)
            self.play(Create(zu), FadeIn(slip, shift=UP * 0.1), run_time=0.5)
            attach(self, zrow, zu)
            vo.wait_until("write region")
            self.play(FadeIn(fix, shift=DOWN * 0.15), FadeIn(fix_tag), run_time=0.5)
            self.play(Indicate(substring(fix.body[1], "--region"), color=TURN, scale_factor=1.2), run_time=0.6)
        self.play(FadeOut(VGroup(t, xr, fix, fix_tag, slip, ref)), track(trk, 5), run_time=0.5)
        self.remove(t, xr, fix, fix_tag, slip, ref)

        # ========================================================== 2. what yours shows (no output panel)
        def r(*parts):
            g = VGroup(*[(mono if m else label)(s, SIZE, c) for s, c, m in parts]).arrange(RIGHT, buff=0.18)
            return g
        A = "→"
        rows2 = [
            r(("get all", INK, True), (A, S.GREY, False), ("only", INK, False), ("service/kubernetes", SHARED, True)),
            r(("-n cheese-app-namespace", OWN, True), (A, S.GREY, False),
              ("frontend-…  vector-db-…  api-…", POD, True)),
            r(("the nginx controller,", INK, False), ("vector-db-loader-…", POD, True),
              ("Completed", S.GREY, True)),
            r(("job.batch/vector-db-loader  1/1", OWN, True)),
            r(("get nodes", INK, True), (A, S.GREY, False), ("1 node", NODE, False),
              ("(2 if the autoscaler added one)", S.GREY, False)),
        ]
        for k in (2, 3):
            pad = Rectangle(width=0.6, height=0.1, stroke_width=0, fill_opacity=0)
            pad.next_to(rows2[k], LEFT, buff=0)
            rows2[k].add_to_back(pad)
        yours = card(rows2, S.GREY, size=SIZE, head="what yours shows · no output here", buff=0.16)
        assert yours.width < 13.0, yours.width
        yours.move_to([0, 1.2, 0])
        assert yours.get_top()[1] < TRACK_BOTTOM - 0.05, yours.get_top()
        th3 = thumb(K03, (2, 3), "CLUSTER-IP", "part 1 · kubectl get all")
        th7 = thumb(K07, (2, 3, 4, 5), "ROLES", "part 1 · kubectl get nodes")
        thumbs = VGroup(th3, th7).arrange(RIGHT, buff=0.5, aligned_edge=UP)
        thumbs.next_to(yours, DOWN, buff=0.45)
        assert thumbs.get_bottom()[1] > -3.55 and thumbs.width < 13.0, (thumbs.get_bottom(), thumbs.width)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeIn(yours.frame), FadeIn(yours.head), run_time=0.4)
            vo.wait_until("get all still shows")
            self.play(FadeIn(rows2[0], shift=RIGHT * 0.1), run_time=0.4)
            self.play(Indicate(rows2[0][3], color=SHARED, scale_factor=1.1), run_time=0.5)
            vo.wait_until("because the app sits")
            self.play(FadeIn(th3, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("With dash n")
            self.play(FadeIn(rows2[1][0], shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("yours lists the frontend")
            self.play(FadeIn(VGroup(rows2[1][1], rows2[1][2]), shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("and nginx controller")
            self.play(FadeIn(rows2[2][1], shift=RIGHT * 0.1), run_time=0.3)
            vo.wait_until("and a loader Pod")
            self.play(FadeIn(VGroup(rows2[2][2], rows2[2][3]), shift=RIGHT * 0.1), FadeIn(rows2[3], shift=RIGHT * 0.1),
                      run_time=0.5)
            vo.wait_until("Get nodes shows")
            self.play(FadeIn(rows2[4], shift=RIGHT * 0.1), FadeIn(th7, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(rows2[4][2], color=NODE, scale_factor=1.15), run_time=0.5)
        self.play(FadeOut(VGroup(yours, thumbs)), run_time=0.5)
        self.remove(yours, thumbs)

        # ========================================================== 3. shell into a Pod: the README's Pod name
        t = tb(4)
        cut492 = R492.index(POD_README)
        cmd_rows = [mrow(R491), mrow(R492[:cut492 - 1]), mrow("    " + R492[cut492:])]
        assert cmd_rows[1].text + " " + cmd_rows[2].text.lstrip() == R492
        body = VGroup(*cmd_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rc = readme_card((491, 492), body, size=SIZE)
        rc.move_to([0, 1.55, 0])
        assert rc.get_top()[1] < TRACK_BOTTOM - 0.05, rc.get_top()
        names = [substring(cmd_rows[0], POD_README), substring(cmd_rows[2], POD_README)]
        strikes = VGroup(*[strike(n, S.GREY, 3) for n in names])
        hint = chip("the name your first command prints", TURN, size=SIZE)
        hint.move_to([names[1].get_x() + 1.0, (rc.get_bottom()[1] + t.box.get_top()[1]) / 2, 0])
        harrow = arrow(hint.get_top(), names[1].get_bottom(), TURN, stroke=3, buff=0.1)
        with self.voiceover(SAY[3]) as vo:
            self.play(track(trk, 6), FadeIn(t, shift=UP * 0.2), run_time=0.5)
            type_capture(self, t, B45, type_time=0.6)
            out(self, t, [(B45.line(7), ERR)], wrap=True, run_time=0.25)
            vo.wait_until("The Pod name in the README")
            self.play(FadeIn(rc.frame), FadeIn(rc.head), run_time=0.3)
            for row in cmd_rows:
                self.play(typing(row, 0.45))
            vo.wait_until("use the name")
            self.play(*[n.animate.set_color(S.GREY) for n in names], Create(strikes), run_time=0.4)
            self.play(FadeIn(hint, shift=UP * 0.1), GrowArrow(harrow), run_time=0.4)
        self.play(FadeOut(VGroup(rc, strikes, hint, harrow)), run_time=0.4)
        self.remove(rc, strikes, hint, harrow)

        # ========================================================== 4. inside the API Pod: env | grep ROOT_PATH
        rec_rows = [mrow("$ " + K51.cmd_lines[0]), mrow("$ " + K51.cmd_lines[1]), mrow(K51.line(3), POD)]
        rec = card(rec_rows, S.GREY, size=SIZE, head="part 1 · inside the game's Pod", buff=0.1)
        rec.move_to([-6.45 + rec.width / 2, 1.6, 0])
        rec_tag = edge_tag(rec, standin_tag())
        assert rec_tag.get_top()[1] < TRACK_BOTTOM - 0.02, rec_tag.get_top()
        env_rows = [mrow("env | grep ROOT_PATH"), mrow("exit")]
        _w = label("inside the API Pod", CAPTION).width + extra_tag("our spelling").width + 1.0
        inside = card(env_rows, OWN, size=SIZE, head="inside the API Pod", buff=0.12, card_w=_w)
        inside.move_to([-6.45 + inside.width / 2, -0.5, 0])
        in_tag = edge_tag(inside, extra_tag("our spelling"))
        assert in_tag.get_top()[1] < rec.get_bottom()[1] - 0.05, (in_tag.get_top(), rec.get_bottom())
        t2_top = BOTTOM + 3 * t.pitch + 0.85                # the terminal shrinks to 3 rows here
        assert inside.get_bottom()[1] > t2_top + 0.05, (inside.get_bottom(), t2_top)
        root = two_row_chip("yours: ROOT_PATH=/api-service", "setup_containers.py:310–311", S.GREY)
        root.next_to(inside, RIGHT, buff=0.4).align_to(inside, UP).shift(DOWN * 0.1)
        yt = your_turn().next_to(root, DOWN, buff=0.25).align_to(root, LEFT)
        with self.voiceover(SAY[4]) as vo:
            resize(self, t, 3, keep=[], run_time=0.5)   # a fresh 3-row strip: no dangling fold row
            self.play(FadeIn(rec, shift=RIGHT * 0.15), FadeIn(rec_tag), run_time=0.5)
            vo.wait_until("just as we did in the game")
            self.play(Indicate(rec_rows[2], color=POD, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Print its environment")
            self.play(FadeIn(inside.frame), FadeIn(inside.head), FadeIn(in_tag), run_time=0.3)
            self.play(typing(env_rows[0], 0.6))
            vo.wait_until("look for ROOT PATH")
            self.play(FadeIn(root, shift=LEFT * 0.15), run_time=0.4)
            self.play(Indicate(root.text[0], color=INK, scale_factor=1.06), run_time=0.5)
            vo.wait_until("Pause and try it")
            self.play(typing(env_rows[1], 0.2))
            bp = bare_prompt(self, t)
            self.play(Indicate(substring(bp, "/app/deploy_k8s"), color=TURN, scale_factor=1.1),
                      FadeIn(yt, shift=RIGHT * 0.15), run_time=0.6)
            self.add(t)
            flash_tag(self, yt, TURN)
        self.play(FadeOut(VGroup(t, rec, rec_tag, inside, in_tag, root, yt)), run_time=0.5)
        self.remove(t, rec, rec_tag, inside, in_tag, root, yt)

        # ========================================================== 5. the README's Outputs vs the code
        q = quote_card("readme-pulumi-outputs", (2, 9), source="README:497–506", mono_font=True)
        q.move_to([-6.5 + q.width / 2, 2.55 - q.height / 2, 0])
        assert q.tag.get_top()[1] < TRACK_BOTTOM - 0.02 or q.tag.get_left()[0] > -0.5, q.tag.get_top()
        r_ing = row_with(q.body, "ingress_name")
        r_nip = row_with(q.body, "nginx_ingress_ip")
        cp = code(MAIN, 46, 49, font_size=SIZE)
        cp.move_to([0, 0, 0]).next_to(q, DOWN, buff=0.15).set_x(0)
        assert cp.get_bottom()[1] > -3.55, cp.get_bottom()
        b48 = line_bar(cp.code, 2, OWN, 0.2)
        cp.code.code_lines.set_z_index(2)
        b48.set_z_index(1)
        ipa = code_span(cp.code, 2, '"ip_address"')
        col_x = q.get_right()[0] + 0.12
        ing = two_row_chip("setup_loadbalancer.py:65 →", "cheese-app-ingress", S.GREY)
        ing.text[1].set_color(ROUTE)
        ing.move_to([col_x + ing.width / 2, r_ing.get_y(), 0])
        er = erratum_tag()
        er.next_to(ing, UP, buff=0.25).align_to(ing, LEFT)
        c20row = mrow(C20_40, OUTPUT)
        substring(c20row, "ip_address").set_color(OWN)
        c20head = label("c20 · line 40 · today's key", SIZE, S.GREY)
        c20in = VGroup(c20head, c20row).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        c20fr = frame_box(c20in.width + 0.24, c20in.height + 0.26, S.GREY, k=0.08)
        c20in.move_to(c20fr)
        inset = VGroup(c20fr, c20in).next_to(ing, DOWN, buff=0.25).align_to(ing, LEFT)
        assert inset.get_right()[0] < 6.55 and er.get_top()[1] < 3.5 and inset.get_bottom()[1] > cp.get_top()[1], (inset.get_right(), ing.get_top(), inset.get_bottom(), cp.get_top(), er.get_center(), q.get_right())
        with self.voiceover(SAY[5]) as vo:
            self.play(track(trk, 7), FadeIn(q, shift=RIGHT * 0.15), run_time=0.6)
            vo.wait_until("a little older than the code")
            self.play(FadeIn(cp, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Today the address is called ip address")
            self.play(FadeIn(b48), ipa.animate.set_color(OWN), run_time=0.4)
            self.play(Indicate(ipa, color=OWN, scale_factor=1.1), FadeIn(inset, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("not nginx ingress ip")
            self.play(substring(r_nip, "nginx_ingress_ip").animate.set_color(ERR), FadeIn(er, shift=LEFT * 0.1),
                      run_time=0.4)
            self.play(Indicate(substring(r_nip, "nginx_ingress_ip"), color=ERR, scale_factor=1.1), run_time=0.5)
            vo.wait_until("and the Ingress is called")
            self.play(substring(r_ing, "ingress_name").animate.set_color(ERR),
                      substring(r_ing, '"nginx-ingress"').animate.set_color(ERR),
                      FadeIn(ing, shift=LEFT * 0.1), run_time=0.5)
            self.play(Indicate(ing.text[1], color=ROUTE, scale_factor=1.08), run_time=0.6)
        self.play(FadeOut(VGroup(q, cp, b48, er, ing, inset)), run_time=0.5)
        self.remove(q, cp, b48, er, ing, inset)

        # ========================================================== 6. the app in a browser (illustration)
        bw = browser_window(APP_URL, win_w=6.4, win_h=4.1)
        bw.move_to([-2.9, 0.05, 0])
        if bw.tag is not None:
            assert bw.tag.get_top()[1] < TRACK_BOTTOM - 0.02 or bw.tag.get_left()[0] > -0.5
        pg = bw.page
        hdr_box = frame_box(pg.width - 0.3, 0.55, S.GREY, k=0.12)
        hdr_box.move_to(pg.get_top() + DOWN * 0.42)
        hdr = VGroup(hdr_box, label("Formaggio", SIZE + 2, INK).move_to(hdr_box).align_to(hdr_box, LEFT).shift(RIGHT * 0.25))
        filler = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2, color=S.GREY_DARK, stroke_width=6)
                          for w in (4.6, 3.6, 4.2)]).arrange(DOWN, buff=0.32, aligned_edge=LEFT)
        filler.next_to(hdr_box, DOWN, buff=0.4).align_to(hdr_box, LEFT).shift(RIGHT * 0.25)
        foot_line = Line(LEFT * (pg.width - 0.3) / 2, RIGHT * (pg.width - 0.3) / 2, color=S.GREY_DARK,
                         stroke_width=2).move_to(pg.get_bottom() + UP * 0.62)
        footer = label("API version: 3.0", SIZE, TURN).next_to(foot_line, DOWN, buff=0.14).align_to(foot_line, RIGHT)
        page = VGroup(hdr, filler, foot_line, footer)
        assert footer.get_bottom()[1] > pg.get_bottom()[1]
        yt6 = your_turn().next_to(bw.frame, RIGHT, buff=0.3).set_y(bw.address.get_y())
        st = route_chip("/api-service/status")
        st.move_to([4.55, footer.get_y() + 0.9, 0])
        st_ar = arrow(footer.get_right(), st.get_left(), ROUTE, stroke=4, buff=0.15)
        chat = VGroup(label("chat › model: RAG", SIZE, INK), mono("/chat?model=llm-rag", SIZE, ROUTE)) \
            .arrange(DOWN, buff=0.08)
        chat_fr = box(chat.width + 0.4, chat.height + 0.3, S.GREY, fill_opacity=0.12, radius=0.16)
        chat.move_to(chat_fr)
        chat_c = VGroup(chat_fr, chat).next_to(st, DOWN, buff=0.45)
        assert chat_c.get_right()[0] < 6.6 and yt6.get_right()[0] < 6.6
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(bw, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(yt6, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt6, TURN)
            vo.wait_until("A footer that says")
            self.play(FadeIn(page, lag_ratio=0.2), run_time=0.8)
            self.play(Indicate(footer, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("proves the whole path works")
            self.play(ShowPassingFlash(ring(bw.frame, ROUTE, buff=0.06, stroke=6), time_width=0.6), run_time=1.4)
            vo.wait_until("it asks slash api service")
            self.play(GrowArrow(st_ar), FadeIn(st, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Then pick the RAG model")
            self.play(FadeIn(chat_c, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("a reply proves")
            self.play(Indicate(chat[1], color=ROUTE, scale_factor=1.08), run_time=0.6)

        # ========================================================== 7. 502 / 503 in the first moments
        wait = VGroup(err_chip("502 / 503"), two_row_chip("first moments: the API is still loading TensorFlow",
                                                          "wait, retry", S.GREY)).arrange(RIGHT, buff=0.3)
        wait.move_to([0, -2.85, 0])
        assert wait.get_top()[1] < bw.frame.get_bottom()[1] - 0.05 and wait.width < 13.0, (wait.get_top(), wait.width)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeIn(wait, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(wait[0].text, color=ERR, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Wait, and try again")
            self.play(Indicate(wait[1].text[1], color=INK, scale_factor=1.1), run_time=0.6)
            bw.reload(self)
        self.play(FadeOut(VGroup(bw, page, yt6, st, st_ar, chat_c, wait, trk)), run_time=0.7)
        self.remove(bw, page, yt6, st, st_ar, chat_c, wait, trk)
        self.wait(0.3)
