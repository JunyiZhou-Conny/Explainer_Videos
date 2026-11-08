"""S10 · One front door: nginx — tracker B 12 → 12 · extra → 12 → 13 → 14 (README 136–143).
LECTURE 23 · 37 in block 0 only. V7 VmLayout (shifted down 0.8 so a one-line code strip fits above it).

Beats (script.md "## S10"; one voiceover block each):
0. TRACKER B 12. lref("37"). Slide 37's routing redrawn in series style: a GREY "Browser" →
   ("one address") → a GREY dashed "Ingress Controller", which forks: PINK `/` → dashed "Frontend ·
   3000"; PINK `/api/` → dashed "API · 9000" → `vector-db:8000` → dashed "Vector DB". On "Here the
   same shape": V7's server fades in around it (security-group wall, doors 22/80/443); Frontend,
   API and Vector DB **transform** into the TEAL frontend, api-service and vector-db containers and
   the two branches re-attach. On "the ingress becomes": the ingress box transforms into the TEAL
   nginx container at doors 80/443; the browser's arrow re-routes through door 80. The lecture tag
   leaves with the lecture picture.
1. TRACKER B 12. README(136–137) card + GREEN chip "already in the repo"; the card shrinks into the
   tracker caption. CODE(nginx.conf: 25–27) (`listen 80` YELLOW) → Transform → CODE(…: 34–37)
   (`location ^~ /api/` and `api-service:9000` PINK) → Transform → CODE(…: 46–48) (`location /`
   and `frontend:3000` PINK).
2. The panel becomes CODE(…: 37) on top; V7 returns under it; a PINK request chip
   `/api/newsletters` hovers outside door 80. On "the very end": a thin GREY box frames `9000/;`.
   PONDER(8 s).
3. The card leaves; the trailing `/` turns YELLOW and is underlined (the rest of the URL, which the
   highlighter paints yellow, turns WHITE so the slash stands out); the request enters through door 80, nginx cuts
   `/api` off (falls away RED), `/newsletters` rides on to api-service. TRACKER B 12 · extra. V7
   leaves; a 10-row laptop terminal (bar tag "extra · stand-in on the laptop") types laptop/62
   line 1 (folded) → 62: 34 GREEN, 36, 38 YELLOW, each with a GREY row tag naming its request
   (lines 2, 4, 6 of the capture); "HTTP 301" flashes on "a redirect".
4. TRACKER B 12. CODE(.env.production: 2) replaces line 37 (`NEXT_PUBLIC_BASE_API_URL=/api`
   GREEN); a drawing: Browser → PINK `<EXTERNAL_IP>/api/…` → nginx → PINK `/…` → api-service;
   then CODE(api-service/api/service.py: 25) with `prefix="/newsletters"` GREEN and a GREEN ✓
   "they fit".
5. TRACKER B 13. Toolbox terminal (laptop/47: 35's prompt) types README 141; ▶ your turn beside
   it; TBX(47: 42 msg) RED; PlayRecap from 45 (unreachable=1 RED). On "On a real server": V7
   returns without nginx, the four task names of laptop/37 as tiles above it, GREY caption "what
   success looks like" top right; the tiles light in turn: a GREEN `nginx.conf` file lands in the
   server, the nginx container starts (doors 80, 443 and its ":80 :443" flash), then restarts.
6. TRACKER B 14. A schematic browser (illustration) `http://<EXTERNAL_IP>/` with a GREY page
   outline "Formaggio" (its illustration tag inside the page, right), ▶ your turn just above its
   top-right corner; a GREY chip "blank or 502? / step 11:
   container ls, logs api-service". V7: ':3000 :8000 :9000' painted inside the wall (no hole),
   door 80 GREEN; door 443 ORANGE "open" and nginx's ":443" flash, a GREY dashed chip "nginx
   serves nothing here · no HTTPS".
7. V7 leaves; the browser shrinks into a text-free browser glyph; GREY caption "Part 1 · about a
   dozen commands · five playbooks · by hand"; a PINK ribbon `/run-deploy-app` drifts in from the
   right edge and stops; it flashes on "Next, a commit message". Fade; empty frame.

Deviations from SHOW: V7 is shifted down 0.8 for the whole scene so line 37 can stand above it in
block 2. In V7 the API branch runs as an arc under nginx and api-service (their slots are 0.2
apart). Block 3 drives the request by hand instead of VmLayout.route() (its chip would cross the
wall and overlap the api-service box at this offset): the cut happens as the request reaches the
door, then `/newsletters` passes through nginx to api-service. Block 3 adds GREY row tags naming which curl
each printed line answers (capture lines 2, 4, 6 are the requests; they are not typed). Block 4
adds CODE(service.py: 25) for "the API mounts its routes without the prefix". Block 5's tiles light
WHITE, not in an Ansible state colour (nothing ran: no state is claimed). Block 6: the browser sits
above V7, not beside it (a browser whose address is >= 20 pt is 6.3 wide; V7 is 10.7); doors 3000,
8000 and 9000 are V7's ':3000 :8000 :9000' painted inside the wall (V7 has no door glyphs for
them); nginx sits against the wall, so "443 forwarded to nginx" is door 443 plus nginx's ':443'
flashing together, not a line. The browser's tags sit off its top edge (on it they covered the
address and touched the tracker caption). Block 7: "the browser shrinks" = it turns into a text-free browser glyph (its text cannot
go under 20 pt).
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S10"]

NG = "src/deployment/nginx-conf/nginx/nginx.conf"
ENV = "src/frontend-react/.env.production"
SVC = "src/api-service/api/service.py"
C62 = capture("62")
X47 = toolbox_capture("47")
CMD13 = readme(141)
TASKS = task_names("deploy-setup-webserver.yml")
SH = 0.8          # V7 shifted down by this much (line 37 fits above it)

# ------------------------------------------------------------------ the real sources (checked)
assert X47.cmd == CMD13 == "ansible-playbook deploy-setup-webserver.yml -i inventory.yml"
assert excerpt(NG, 26, 26).strip() == "listen 80;"
assert excerpt(NG, 35, 35).strip() == "location ^~ /api/ {"
assert excerpt(NG, 37, 37).strip() == "proxy_pass http://api-service:9000/;"
assert excerpt(NG, 47, 47).strip() == "location / {"
assert excerpt(NG, 48, 48).strip() == "proxy_pass http://frontend:3000;"
assert excerpt(ENV, 2, 2).strip() == "NEXT_PUBLIC_BASE_API_URL=/api"
assert excerpt(SVC, 25, 25).strip() == 'app.include_router(newsletter.router, prefix="/newsletters")'
assert readme(137).strip().endswith("Create nginx.conf file for defaults routes in web server")
assert C62.cmd.startswith("docker run -d --name nginx --network appnetwork -p 80:80 -p 443:443")
assert C62.line(2) == "curl -s localhost/api/newsletters" and C62.line(4) == "curl -s localhost/"
assert C62.line(6).endswith("localhost/api")
assert C62.line(34) == "api-service received /newsletters"
assert C62.line(36) == "frontend received /" and C62.line(38) == "HTTP 301"
MSG47 = X47.msg(42)
assert MSG47[0] == "fatal: [EXTERNAL_IP]: UNREACHABLE! =>" and "external_ip" in MSG47[1]
assert X47.recap()[1]["unreachable"] == 1
assert TASKS == ["Ensure Docker network exists", "Copy nginx config files", "Create nginx container",
                 "Restart nginx container"], TASKS


# ------------------------------------------------------------------ helpers of this scene
def drop_all(scene, *mobs, run_time: float = 0.4):
    scene.play(*[FadeOut(m) for m in mobs], run_time=run_time)
    for m in mobs:
        scene.remove(m, *m.get_family())


def lec_box(lines, dashed=True, color=S.GREY, box_w=None):
    return label_box(lines, color, dashed=dashed, box_w=box_w)


def lit(tl) -> AnimationGroup:
    """ANIM: a dim task tile lights up (WHITE text, WHITE outline; no Ansible state is claimed)."""
    return AnimationGroup(tl.text.animate.set_opacity(1), tl.frame.animate.set_stroke(INK, opacity=1))


def substring_label(t: Text, sub: str) -> VGroup:
    """The glyphs of `sub` in a one-line mono Text (spaces carry no glyph)."""
    s = t.text
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    return VGroup(*t[a:a + len("".join(sub.split()))])


def span_bar(c, k0: int, k1: int, color: str) -> Rectangle:
    """One translucent bar over lines k0..k1 of a code_block (two line_bars overlap into a seam)."""
    a, b = line_bar(c, k0, color), line_bar(c, k1, color)
    return Rectangle(width=a.width, height=a.get_top()[1] - b.get_bottom()[1], stroke_width=0) \
        .set_fill(color, 0.16).move_to([a.get_x(), (a.get_top()[1] + b.get_bottom()[1]) / 2, 0])


def tag_for(path: str) -> VGroup:
    """A GREY row tag naming the request a printed line answers."""
    return row_tag([("for", "label"), (path, "mono")])


class FrontDoor(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S10"] == 8, len(SAY)

        # ========================================================== 0. the lecture's routing → one machine
        tr = tracker_b(12)
        lr = lref("37")
        v = VmLayout()
        v.shift(DOWN * SH)
        o = v._o()
        P = {k: v.slots[k] + o for k in ("nginx", "frontend", "api", "vectordb")}
        y80 = 0.0 + o[1]                       # door 80's height
        # the lecture picture (spacious), in GREY: the GCP words before they turn AWS
        brw = lec_box("Browser", dashed=False, color=LAPTOP)
        brw.move_to([-5.55, y80 - 0.22, 0])
        ing = lec_box("Ingress\nController")
        ing.move_to([-1.9, y80 - 0.22, 0])
        fe = lec_box("Frontend · 3000").move_to([1.3, 1.25, 0])
        api = lec_box("API · 9000").move_to([1.1, -1.75, 0])
        vdb = lec_box("Vector DB").move_to([5.6, -1.75, 0])
        a_in = arrow(brw.get_right(), ing.get_left(), S.GREY)
        one = note("one address").next_to(a_in, UP, buff=0.12)
        a_fe = route(ing.get_right() + UP * 0.15, fe.get_left(), arc=0.25, stroke=3)
        a_api = route(ing.get_right() + DOWN * 0.15, api.get_left(), arc=-0.25, stroke=3)
        l_fe = mono("/", 22, ROUTE).next_to(a_fe.get_center(), UL, buff=0.08)
        l_api = mono("/api/", 22, ROUTE).next_to(a_api.get_center(), DL, buff=0.08)
        a_vdb = arrow(api.get_right(), vdb.get_left(), S.GREY)
        l_vdb = mono("vector-db:8000", 20, S.GREY).next_to(a_vdb, UP, buff=0.1)
        assert l_vdb.get_left()[0] > api.get_right()[0] + 0.05 and l_vdb.get_right()[0] < vdb.get_left()[0] - 0.05
        # the same shape on V7
        boxes = {k: v._box(k).move_to(P[k]) for k in ("nginx", "frontend", "api", "vectordb")}
        ng_top, ng_bot = boxes["nginx"].get_top(), boxes["nginx"].get_bottom()
        r_fe = route(ng_top + RIGHT * 0.2, boxes["frontend"].get_left(), arc=-0.6, stroke=3)
        r_api = route(ng_bot + RIGHT * 0.2, boxes["api"].get_bottom(), arc=0.9, stroke=3)
        rl_fe = mono("/", 22, ROUTE).move_to(r_fe.point_from_proportion(0.5) + np.array([-0.3, 0.15, 0]))
        rl_api = mono("/api/", 22, ROUTE).move_to([(P["nginx"][0] + P["api"][0]) / 2, ng_bot[1] - 0.75, 0])
        brw2 = brw.copy().move_to([-5.55, y80 - 0.22, 0])
        r_in = route(brw2.get_right() + RIGHT * 0.02, boxes["nginx"].get_left() + UP * 0.1, stroke=3)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(lr, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(brw, shift=RIGHT * 0.1), run_time=0.4)
            self.play(GrowArrow(a_in), FadeIn(one), FadeIn(ing, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("slash to the frontend")
            self.play(Create(a_fe), FadeIn(l_fe), FadeIn(fe, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("slash API slash to the API")
            self.play(Create(a_api), FadeIn(l_api), FadeIn(api, shift=RIGHT * 0.1), run_time=0.7)
            self.play(GrowArrow(a_vdb), FadeIn(l_vdb), FadeIn(vdb, shift=RIGHT * 0.1), run_time=0.6)
            vo.wait_until("Here the same shape")
            self.play(FadeOut(one), FadeOut(a_in), FadeOut(a_vdb), FadeOut(l_vdb), FadeIn(v),
                      ReplacementTransform(fe, boxes["frontend"]), ReplacementTransform(api, boxes["api"]),
                      ReplacementTransform(vdb, boxes["vectordb"]),
                      ReplacementTransform(a_fe, r_fe), ReplacementTransform(a_api, r_api),
                      ReplacementTransform(l_fe, rl_fe), ReplacementTransform(l_api, rl_api), run_time=1.2)
            v.wall(self, run_time=0.6)
            for k in ("frontend", "api", "vectordb"):
                v.containers[k] = boxes[k]
                v.keep(self, boxes[k])
            vo.wait_until("and the ingress becomes")
            self.play(ReplacementTransform(ing, boxes["nginx"]), run_time=0.9)
            v.containers["nginx"] = boxes["nginx"]
            v.keep(self, boxes["nginx"])
            self.play(GrowArrow(r_in), Indicate(v.doors[80].text, color=ROUTE, scale_factor=1.3), run_time=0.6)
            self.play(Indicate(boxes["nginx"].text, color=IMAGE, scale_factor=1.15), FadeOut(lr), run_time=0.7)
        self.remove(lr)
        routes = VGroup(r_fe, r_api, rl_fe, rl_api, r_in)

        # ========================================================== 1. step 12: nginx.conf is already there
        rp = readme_panel(136, 137)
        rp.move_to([0, 2.55 - rp.height / 2, 0])
        here = ok_chip("already in the repo").next_to(rp, DOWN, buff=0.25).align_to(rp, RIGHT)
        p25 = code(NG, 25, 27)
        p34 = code(NG, 34, 37, trim=60)
        p46 = code(NG, 46, 48)
        for p in (p25, p34, p46):
            p.move_to([0, 0.2, 0])
        with self.voiceover(SAY[1]) as vo:
            drop_all(self, v, brw, routes, run_time=0.4)
            self.play(FadeIn(rp, shift=UP * 0.15), Indicate(tr.caption, color=TURN, scale_factor=1.05), run_time=0.6)
            vo.wait_until("it's already in the repo")
            self.play(FadeIn(here, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(here.text, color=OWN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("It listens on port 80")
            self.play(FadeOut(rp, target_position=tr.caption.get_center(), scale=0.2), FadeOut(here),
                      FadeIn(p25, shift=UP * 0.15), run_time=0.7)
            self.remove(rp, here)
            bar = line_bar(p25.code, 1, TURN)
            self.play(FadeIn(bar), *[g.animate.set_color(TURN) for g in code_span(p25.code, 1, "listen 80")],
                      run_time=0.4)
            self.play(Indicate(code_span(p25.code, 1, "listen 80"), color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Paths that start with")
            self.play(FadeOut(bar), FadeTransform(p25, p34), run_time=0.7)
            self.remove(bar)
            bars = VGroup(line_bar(p34.code, 1, ROUTE), line_bar(p34.code, 3, ROUTE))
            self.play(FadeIn(bars[0]), *[g.animate.set_color(ROUTE) for g in code_span(p34.code, 1, "location ^~ /api/")],
                      run_time=0.4)
            self.play(FadeIn(bars[1]), *[g.animate.set_color(ROUTE) for g in code_span(p34.code, 3, "api-service:9000")],
                      run_time=0.4)
            self.play(Indicate(code_span(p34.code, 1, "/api/"), color=ROUTE, scale_factor=1.2), run_time=0.8)
            self.play(Indicate(code_span(p34.code, 3, "api-service:9000"), color=ROUTE, scale_factor=1.12), run_time=0.8)
            vo.wait_until("everything else goes")
            self.play(FadeOut(bars), FadeTransform(p34, p46), run_time=0.7)
            self.remove(bars, *bars)
            bars = VGroup(span_bar(p46.code, 1, 2, ROUTE))
            self.play(FadeIn(bars), *[g.animate.set_color(ROUTE) for g in code_span(p46.code, 1, "location /")],
                      *[g.animate.set_color(ROUTE) for g in code_span(p46.code, 2, "frontend:3000")], run_time=0.5)

        # ========================================================== 2. predict: which path arrives?
        p37 = code(NG, 37, 37)
        p37.move_to([0, 2.8 - p37.height / 2, 0])
        assert p37.get_bottom()[1] > v.frame.get_top()[1] + 0.05, (p37.get_bottom(), v.frame.get_top())
        req = route_chip("/api/newsletters")
        req.move_to([-6.5 + req.width / 2, y80 + 0.55, 0])
        end37 = code_span(p37.code, 0, "9000/;")
        frm = SurroundingRectangle(end37, color=S.GREY, buff=0.07, stroke_width=2)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(bars), FadeTransform(p46, p37), run_time=0.7)
            self.remove(bars, *bars)
            self.play(FadeIn(v), FadeIn(brw), FadeIn(routes), run_time=0.6)
            vo.wait_until("the browser asks nginx")
            self.play(FadeIn(req, shift=RIGHT * 0.3), run_time=0.5)
            self.play(req.animate.shift(UP * 0.08), rate_func=there_and_back, run_time=0.6)
            vo.wait_until("Which path does the API service receive")
            self.play(Indicate(boxes["api"].text, color=IMAGE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("Look at the very end")
            self.play(Create(frm), run_time=0.5)
        card = ponder(self, "The browser asks nginx for /api/newsletters.\nWhich path does api-service receive?",
                      seconds=8)

        # ========================================================== 3. /newsletters: the trailing slash
        slash = code_span(p37.code, 0, "/;")[0]
        t3 = term(P_LAPTOP, rows=10)
        assert t3.box.get_top()[1] < p37.get_bottom()[1] - 0.05, (t3.box.get_top(), p37.get_bottom())
        sb = on_bar(t3, standin_row())
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(card), run_time=0.4)
            self.remove(card, *card.get_family())
            vo.wait_until("The trailing slash")
            url = code_span(p37.code, 0, "http://api-service:9000")
            ul = under(slash, TURN)
            self.play(FadeOut(frm), url.animate.set_color(INK), slash.animate.set_color(TURN), Create(ul), run_time=0.5)
            self.play(Indicate(slash, color=TURN, scale_factor=1.6), run_time=0.6)
            # the request reaches the front door (nginx); nginx cuts the prefix, the rest goes on
            ngb = boxes["nginx"]
            self.play(req.animate.shift(RIGHT * (v.frame.get_left()[0] - 0.1 - req.get_right()[0]) + DOWN * 0.15),
                      Indicate(ngb.text, color=IMAGE, scale_factor=1.15), run_time=0.7)
            keep_ = route_chip("/newsletters").move_to(req).align_to(req, RIGHT).shift(RIGHT * 0.12)
            gone = err_chip("/api", mono_font=True).move_to(req)
            gone.shift(RIGHT * (keep_.get_left()[0] - 0.05 - gone.get_right()[0]))
            assert gone.get_left()[0] > -6.6, gone.get_left()
            self.play(FadeOut(req), FadeIn(gone), FadeIn(keep_), run_time=0.35)
            self.remove(req)
            self.play(gone.animate.shift(DOWN * 0.45).set_opacity(0), run_time=0.5)
            self.remove(gone)
            self.play(keep_.animate.move_to(ngb), run_time=0.5)
            self.play(keep_.animate.move_to(boxes["api"].get_top() + UP * 0.4), run_time=0.6)
            self.play(Indicate(boxes["api"].text, color=ROUTE, scale_factor=1.15), run_time=0.5)
            vo.wait_until("Our stand-ins on the laptop")
            drop_all(self, v, brw, routes, keep_, run_time=0.4)
            self.play(track(tr, 12, True), FadeIn(t3, shift=UP * 0.2), FadeIn(sb), run_time=0.5)
            type_capture(self, t3, C62, type_time=1.6)
            o3 = out(self, t3, [(C62.line(34), PASS), C62.line(36), (C62.line(38), TURN)], run_time=0.5)
            tg = [beside(tag_for(pth), ln) for pth, ln in zip(("/api/newsletters", "/", "/api"), o3)]
            self.play(*[FadeIn(x, shift=LEFT * 0.1) for x in tg], run_time=0.4)
            for x, ln in zip(tg, o3):
                attach(self, ln, x)
            self.play(Indicate(substring(o3[0], "/newsletters"), color=PASS, scale_factor=1.15), run_time=0.6)
            vo.wait_until("and slash API without its last slash")
            self.play(Indicate(substring(o3[2], "HTTP 301"), color=TURN, scale_factor=1.2), run_time=0.7)

        # ========================================================== 4. the frontend calls /api on the same host
        penv = code(ENV, 2, 2)
        penv.move_to([0, 2.8 - penv.height / 2, 0])
        psvc = code(SVC, 25, 25)
        psvc.move_to([0, -3.45 + psvc.height / 2, 0])
        dy = (penv.get_bottom()[1] + psvc.get_top()[1]) / 2
        b4 = lec_box("Browser", dashed=False, color=LAPTOP).move_to([-5.6, dy, 0])
        n4 = crate("nginx", box_w=1.9, box_h=0.9, sub=":80").move_to([0.3, dy, 0])
        s4 = crate("api-service", box_w=1.9, box_h=0.9, sub=":9000").move_to([4.9, dy, 0])
        a41 = route(b4.get_right(), n4.get_left(), stroke=3)
        a42 = route(n4.get_right(), s4.get_left(), stroke=3)
        c41 = route_chip(f"{EXTERNAL_IP}/api/…").next_to(a41, UP, buff=0.12)
        c42 = route_chip("/…").next_to(a42, UP, buff=0.12)
        fit = VGroup(check_mark(0.3, PASS, stroke=4), label("they fit", 20, PASS)).arrange(RIGHT, buff=0.12)
        fit.next_to(s4, DOWN, buff=0.2)
        with self.voiceover(SAY[4]) as vo:
            drop_all(self, t3, sb, ul, run_time=0.4)
            self.play(track(tr, 12), FadeTransform(p37, penv), run_time=0.7)
            self.play(*[g.animate.set_color(PASS) for g in code_span(penv.code, 0, "NEXT_PUBLIC_BASE_API_URL=/api")],
                      FadeIn(b4), run_time=0.5)
            self.play(GrowArrow(a41), FadeIn(c41, shift=RIGHT * 0.1), FadeIn(n4), run_time=0.7)
            vo.wait_until("and the API mounts its routes")
            self.play(GrowArrow(a42), FadeIn(c42, shift=RIGHT * 0.1), FadeIn(s4), run_time=0.6)
            self.play(FadeIn(psvc, shift=UP * 0.15), run_time=0.5)
            self.play(*[g.animate.set_color(PASS) for g in code_span(psvc.code, 0, 'prefix="/newsletters"')],
                      run_time=0.4)
            vo.wait_until("they fit")
            self.play(Create(fit[0]), FadeIn(fit[1]), run_time=0.5)
            self.play(Indicate(fit[1], color=PASS, scale_factor=1.1), run_time=0.5)

        # ========================================================== 5. step 13: unreachable; what success looks like
        tr13 = tracker_b(13)
        t5 = toolbox_term("47", rows=8)
        cap = note("what success looks like")
        cap.move_to([6.5 - cap.width / 2, 3.25, 0])
        tiles = VGroup(*[label_box(n, INK, box_w=4.3, pad=0.12) for n in TASKS])
        tiles.arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.15))
        tiles.move_to([0.0, 2.75 - tiles.height / 2, 0])
        for tl in tiles:
            tl.text.set_opacity(0.4)
            tl.frame.set_stroke(S.GREY, opacity=0.5)
        assert tiles.get_bottom()[1] > v.frame.get_top()[1] + 0.05, (tiles.get_bottom(), v.frame.get_top())
        conf = ok_chip("nginx.conf", mono_font=True)
        with self.voiceover(SAY[5]) as vo:
            drop_all(self, penv, psvc, b4, n4, s4, a41, a42, c41, c42, fit, run_time=0.4)
            self.play(ReplacementTransform(tr, tr13), FadeIn(t5, shift=UP * 0.2), run_time=0.6)
            tr = tr13
            cmd5 = type_cmd(self, t5, CMD13, type_time=1.4)
            turn5 = beside(turn_row(), cmd5)
            pin(self, cmd5, turn5)
            vo.wait_until("Unreachable again")
            o5 = out(self, t5, [(s, ERR) for s in MSG47], wrap=True, run_time=0.6)
            rc = play_recap("47")
            y = t5._slot(len(t5.lines))[1] - 0.3
            rc.move_to([t5.box.get_center()[0], y - rc.height / 2 + 0.1, 0])
            assert rc.get_bottom()[1] > t5.box.get_bottom()[1] + 0.05
            self.play(FadeIn(rc, shift=UP * 0.1), run_time=0.4)
            self.play(rc.flash("unreachable"), run_time=0.6)
            vo.wait_until("On a real server")
            ng_old = v.containers.pop("nginx")
            v.remove(ng_old)
            drop_all(self, t5, rc, run_time=0.4)
            self.play(FadeIn(v), FadeIn(cap), LaggedStart(*[FadeIn(x) for x in tiles], lag_ratio=0.15), run_time=0.7)
            self.play(lit(tiles[0]), run_time=0.3)
            vo.wait_until("it copies the config")
            self.play(lit(tiles[1]), run_time=0.3)
            conf.next_to(tiles[1], DOWN, buff=0.1)
            self.play(FadeIn(conf), run_time=0.3)
            self.play(conf.animate.move_to([P["nginx"][0] + 0.15, P["nginx"][1] + 0.85, 0]), run_time=0.7)
            vo.wait_until("starts nginx on ports 80 and 443")
            self.play(lit(tiles[2]), run_time=0.3)
            ng5 = v.container(self, "nginx", run_time=0.5)
            self.play(conf.animate.move_to(ng5).scale(0.5).set_opacity(0), run_time=0.5)
            self.remove(conf)
            self.play(Indicate(v.doors[80].text, color=ROUTE, scale_factor=1.3),
                      Indicate(v.doors[443].text, color=ROUTE, scale_factor=1.3),
                      Indicate(ng5.sub, color=ROUTE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("and restarts it")
            self.play(lit(tiles[3]), run_time=0.3)
            ng5 = v.recreate(self, "nginx", run_time=1.0)

        # ========================================================== 6. step 14: open the address
        tr14 = tracker_b(14)
        bw = browser(EXTERNAL_IP.join(("http://", "/")), page_w=6.3, page_h=1.35)
        bw.tag.move_to([bw.content.get_right()[0] - 0.1 - bw.tag.width / 2, bw.content.get_y(), 0])
        bw.shift([6.5 - bw.frame.get_right()[0], 2.8 - bw.frame.get_top()[1], 0])
        page = outline_box(2.6, 0.5, S.GREY).move_to(bw.content).align_to(bw.content, LEFT).shift(RIGHT * 0.3)
        page_t = label("Formaggio", 20, S.GREY).move_to(page)
        turn6 = your_turn()
        turn6.move_to([bw.frame.get_right()[0] - turn6.width / 2, bw.frame.get_top()[1] + 0.06 + turn6.height / 2, 0])
        hint = label_box(["blank or 502?", "step 11: container ls, logs api-service"], S.GREY, fill_opacity=0.08)
        hint.move_to([-6.5 + hint.width / 2, 1.95, 0])
        assert turn6.get_top()[1] < 3.6 and turn6.get_left()[0] > tr14.get_right()[0] + 0.2
        assert hint.get_right()[0] < bw.get_left()[0] - 0.1, (hint.get_right(), bw.get_left())
        assert hint.get_bottom()[1] > v.frame.get_top()[1] + 0.08, (hint.get_bottom(), v.frame.get_top())
        assert bw.frame.get_bottom()[1] > v.frame.get_top()[1] + 0.03, (bw.frame.get_bottom(), v.frame.get_top())
        none = dashed_chip("nginx serves nothing here · no HTTPS")
        none.move_to([P["nginx"][0] - 0.8 + none.width / 2, ng5.get_bottom()[1] - 0.45, 0])
        assert none.get_right()[0] < v.frame.get_right()[0] - 0.1
        with self.voiceover(SAY[6]) as vo:
            drop_all(self, tiles, cap, run_time=0.4)
            self.play(ReplacementTransform(tr, tr14), FadeIn(bw, shift=DOWN * 0.15), FadeIn(page), FadeIn(page_t),
                      run_time=0.6)
            tr = tr14
            self.play(FadeIn(turn6, shift=DOWN * 0.1), run_time=0.4)
            flash_tag(self, turn6)
            self.play(FadeIn(hint, shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("Only port 80 does the work")
            v.ports_inside(self, run_time=0.4)
            v.door(self, 80, "used", run_time=0.4)
            self.play(Indicate(v.doors[80].text, color=PASS, scale_factor=1.3), run_time=0.6)
            vo.wait_until("Port 443 is open")
            v.door(self, 443, "open", run_time=0.4)
            self.play(Indicate(v.doors[443].text, color=SHARED, scale_factor=1.3),
                      Indicate(substring_label(ng5.sub, ":443"), color=SHARED, scale_factor=1.2), run_time=0.7)
            vo.wait_until("but nginx serves nothing there")
            self.play(FadeIn(none, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(none.text, color=S.GREY, scale_factor=1.06), run_time=0.6)

        # ========================================================== 7. part 1 ends; a commit message next
        small = VGroup(*[m.copy() for m in (bw.frame, bw[1], bw[2])])
        small_target = small.copy().scale(0.45).move_to([0, 1.4, 0])
        small_target[0].set_stroke(S.GREY, width=2, opacity=1)
        part = note("Part 1 · about a dozen commands · five playbooks · by hand")
        part.move_to([0, 0.2, 0])
        rib = ribbon(KEYWORD)
        rib.move_to([7.4 + rib.width / 2, -1.2, 0])
        with self.voiceover(SAY[7]) as vo:
            drop_all(self, v, none, hint, turn6, run_time=0.4)
            others = [m for m in bw if m not in (bw.frame, bw[1], bw[2])]
            self.add(small)
            self.play(*[FadeOut(m) for m in others], FadeOut(page), FadeOut(page_t),
                      FadeOut(VGroup(bw.frame, bw[1], bw[2])), run_time=0.3)
            self.remove(bw, page, page_t)
            self.play(Transform(small, small_target), run_time=0.8)
            self.play(FadeIn(part, shift=UP * 0.1), run_time=0.5)
            self.play(rib.animate.move_to([0, -1.2, 0]), run_time=3.0, rate_func=rate_functions.ease_out_cubic)
            vo.wait_until("Next, a commit message")
            self.play(Indicate(rib.text, color=ROUTE, scale_factor=1.08), run_time=0.6)
        self.wait(0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.remove(*self.mobjects)
        self.wait(0.3)
