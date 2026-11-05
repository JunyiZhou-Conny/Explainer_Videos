"""S03 · v1: a server, an app, a port (AC215 L18, part 1). Tracker [A] "README › Backend API
Container" from beat 2. Lecture: 18 · 25–26, 27–28, 34–41 (APIs).

Beats (script.md "## S03", one voiceover block each):
0. lecture_ref 25–26. The lecture's loop redrawn: a GREY laptop ("browser") left, a GREY server
   right, a PINK "HTTP request" arrow on top and a PINK "HTTP response" arrow below; an envelope
   "GET /" rides the request, "200 OK" rides back. On "A port picks" the server grows doors: 22, 80,
   443 (the lecture's, PINK) and, in YELLOW, the tutorial's 9000, 8080, 3000, 8000. On "public
   sites" 80 and 443 flash and https://example.com appears (port left out); on "ours" a
   localhost:9000 address with its port in YELLOW.
1. lecture_ref 27–28. The loop shrinks into the top-left corner. One chip morphs through the
   lecture's ladder: API → Web API (over HTTP) → REST API (HTTP methods: …) → FastAPI (PURPLE). On
   "Every client": three GREY client chips whose PINK lines merge ("REST / JSON") and cross a dashed
   divider to one TEAL "API" box; on "only the API" it fans out to stores, databases, models.
2. Lecture tag off. Tracker [A] 1 appears. README card (README.md · line 41) over a full-width
   `laptop` terminal: it types `cd cheese-app-v1/api-service` → a01:2 in RED. Tracker 1 · extra,
   the card takes the GREY tag "erratum · add src/"; it types `cd cheese-app-v1/src/api-service && ls`
   (row tag `extra`) → a02:2–7.
3. Tracker 2. The terminal shrinks to a 3-row strip; CODE(docker-shell.sh: 13–21) above it. The
   prompt becomes ~/cheese-app-v1/src/api-service; it types `sh docker-shell.sh`. On "builds" line 13's
   `docker build` turns PURPLE; on "removes itself" `--rm` rings GREY; on "mounts" lines 17–19 bar
   GREEN; on "publishes" `-p 9000:9000` rings PINK and a tunnel picture draws (GREY laptop wall
   door 9000 piped to a TEAL container door 9000). `▶ your turn` on "Pause".
4. The code and tunnel go; the strip grows: a03:3 (GREY), …, 30–37 (32 GREEN), the row tag "at the
   time of recording" on line 35 and a GREY row tag "your prompt shows your own user · on a Mac:
   aarch64" on line 33 (not spoken). Tracker 3; at the container prompt of a03:38 it types the uvicorn
   line (folds into two rows). The terminal shrinks to a 4-row strip keeping those rows, and V3
   ServerAppDiagram builds above it: TEAL container, PURPLE "uvicorn · the server" with the PINK
   socket :9000 (on "owns the port"), then the PURPLE card "FastAPI · the app".
5. `api.service:app` turns PINK in the typed row and splits into three chips on the card (folder
   api/, file service.py, variable app); each flashes as it is named.
6. `--host 0.0.0.0` turns GREEN; the plates appear (eth0 on the wall, lo · 127.0.0.1 inside); the
   GREEN 0.0.0.0 badge binds both; a PINK request walks in through eth0 (GREEN tick). On "Reload"
   `--reload --reload-dir api/` turns PURPLE and an eye watches the api/ chip. On "the last part"
   `"$@"` rings GREY and the terminal's bar tag "extra arguments · none here" appears.
7. a03:39–40 (the URL PINK), 41 (the reloader words PURPLE, the PID not), 42–44 (44 GREEN).
8. The strip goes; V3 slides right; CODE(api/service.py: 5–14) at the left: line 5 bar PURPLE; on
   "CORS middleware" lines 8–14 ring GREY with the chip "part 2's ending". On "and one route" it
   morphs into CODE(api/service.py: 17–20) at the bottom: lines 18–20 bar YELLOW, and the row
   "GET / → get_index" writes into V3's route table.
9. Tracker 4, lecture_ref 34–41. V3 goes; V1 RequestTrace (browser at localhost:9000 tagged
   illustration, the laptop with one TEAL cheese-app-api-service box). A 4-row `laptop · second tab`
   strip (bar tag "extra · the same request") types `curl -s -i http://localhost:9000/`
   → a04:2, 4, 6, 8 (200 OK GREEN, server: uvicorn PURPLE); the browser shows the welcome JSON.
   `▶ your turn` on the bar on "Pause".
10. The strip goes; the six hops play with their captions, timed to the phrases (4: get_index runs).
11. Hops clear. Under the API box the lecture's label "localhost:9000" appears in GREY with the tags
   "erratum" and "slide 37", then morphs into "port 9000 of the container · listening on 0.0.0.0".
12. Lecture tag off; the trace goes; V3 returns with both plates; the badge flips to 127.0.0.1 with a
   line to lo only (eth0 unconnected). Two dashed PINK arrows end in "?": from a small `curl` terminal
   inside the container, and from a browser outside toward eth0. PONDER (8 s). Then an empty frame.
"""

import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.devops import laptop as laptop_glyph, server as server_glyph
from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ the real sources (checked)
A01 = capture("a01")
A02 = capture("a02")
A03 = capture("a03")
A04 = capture("a04")
assert A01.cmd == "cd cheese-app-v1/api-service", A01.cmd
assert A01.line(2).endswith("No such file or directory"), A01.line(2)
assert A02.cmd == "cd cheese-app-v1/src/api-service && ls", A02.cmd
assert A02.at((2, 7)) == ["Dockerfile", "api", "docker-entrypoint.sh", "docker-shell.sh", "pyproject.toml",
                          "uv.lock"], A02.lines
assert A03.cmd == "sh docker-shell.sh", A03.cmd
assert A03.line(3).startswith("[+] Building 49.9s (11/11) FINISHED"), A03.line(3)
assert A03.line(32) == "Container is running!!!" and A03.line(33) == "Architecture: x86_64"
assert A03.line(35) == "Python version: Python 3.12.16", A03.line(35)
UVICORN = 'uvicorn api.service:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir api/ "$@"'
assert at_prompt(A03, 38)[1] == UVICORN
assert readme_rows(47, 47, V1)[0].endswith(f"run `{UVICORN}` from the docker shell"), readme_rows(47, 47, V1)
assert "Uvicorn running on http://0.0.0.0:9000" in A03.line(40)
assert "Started reloader process [12] using StatReload" in A03.line(41)
assert A03.line(44) == "INFO:     Application startup complete.", A03.line(44)
assert A04.cmd == "curl -s -i http://localhost:9000/", A04.cmd
assert A04.at(2, 4, 6) == ["HTTP/1.1 200 OK", "server: uvicorn", "content-type: application/json"], A04.lines
# a04's last line carries the capture's own '[exit 0]' marker (curl printed no newline): drop it
JSON = re.sub(r"\[exit \d+\]$", "", A04.line(8))
assert JSON == '{"message":"Welcome to AC215"}', JSON
README_41 = readme_lines(41, 41, V1)
assert "cheese-app-v1/api-service" in README_41, README_41

DS = f"{V1}/src/api-service/docker-shell.sh"
SVC = f"{V1}/src/api-service/api/service.py"
assert excerpt(DS, 13, 13).startswith("docker build") and "--rm" in excerpt(DS, 16, 16)
assert excerpt(DS, 20, 20).strip() == "-p 9000:9000 \\", excerpt(DS, 20, 20)
assert excerpt(SVC, 5, 5).startswith("app = FastAPI(") and "CORSMiddleware" in excerpt(SVC, 9, 9)
assert excerpt(SVC, 18, 18) == '@app.get("/")' and "get_index" in excerpt(SVC, 19, 19)

PONDER_Q = ("uvicorn listens on --host 127.0.0.1\ninside the container instead.\n"
            "curl from inside the container: works?\nYour browser on localhost:9000: works?")
LADDER = ("API", "Web API (over HTTP)", "REST API (HTTP methods: GET, POST, PUT, DELETE)", "FastAPI")
V3_AT = UP * 0.8               # V3 over a 4-row 20 pt strip (strip top -1.18, V3 bottom -1.15)


def _row_with(line, sub: str):
    """The row of a typed (maybe folded) command that contains `sub`."""
    for r in rows_of(line):
        if sub in r.text:
            return r
    raise KeyError(sub)


def _rung(s: str, color) -> VGroup:
    """One rung of the lecture's API ladder: a chip whose words morph (steady text)."""
    t = steady(s, 22, INK)
    b = RoundedRectangle(width=t.width + 0.6, height=0.62, corner_radius=0.2, stroke_color=color,
                         stroke_width=3).set_fill(tint(color), 1)
    t.move_to(b)
    return VGroup(b, t)


def span_bar(code_, k0: int, k1: int, color, opacity: float = 0.2) -> Rectangle:
    """One translucent bar over code lines k0..k1 (0-based; line_bar() per line would overlap)."""
    top = code_.code_lines[k0].get_top()[1] + 0.07
    bot = code_.code_lines[k1].get_bottom()[1] - 0.07
    bg = code_.background
    return Rectangle(width=bg.width - 0.12, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([bg.get_center()[0], (top + bot) / 2, 0])


def _env(s: str) -> VGroup:
    e = envelope(s, ROUTE)
    e.body.set_fill(S.BG, 1)
    return e


class ServerAndApp(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 13, len(SAY)

        # ========================================================== 0. request, response, a port
        ref0 = lref("25–26 (APIs)")
        lap = laptop_glyph(2.4).move_to([-4.4, 0.35, 0])
        lap_l = label("browser", 22, LAPTOP).next_to(lap, DOWN, buff=0.15)
        srv = server_glyph(2.0).move_to([1.9, 0.35, 0])
        srv_l = label("server", 22, LAPTOP).next_to(srv, DOWN, buff=0.15)
        req = Arrow([-3.0, 1.15, 0], [0.65, 1.15, 0], buff=0, color=ROUTE, stroke_width=5, tip_length=0.22)
        res = Arrow([0.65, -0.45, 0], [-3.0, -0.45, 0], buff=0, color=ROUTE, stroke_width=5, tip_length=0.22)
        req_l = label("HTTP request", 22, ROUTE).next_to(req, UP, buff=0.12)
        res_l = label("HTTP response", 22, ROUTE).next_to(res, DOWN, buff=0.12)
        e_req, e_res = _env("GET /"), _env("200 OK")
        lect = VGroup(*[door(p) for p in ("22", "80", "443")]).arrange(DOWN, buff=0.22)
        tut = VGroup(*[door(p, color=TURN) for p in ("9000", "8080", "3000", "8000")]).arrange(DOWN, buff=0.22)
        lect.move_to([3.95, 0.35, 0])
        tut.move_to([5.55, 0.35, 0])
        lect_h = label("lecture", 20, S.GREY).next_to(lect, UP, buff=0.18)
        tut_h = label("this tutorial", 20, TURN).next_to(tut, UP, buff=0.18).set_x(tut.get_x())
        studs = VGroup(*[Line(srv.get_right(), d.get_left(), color=S.GREY_DARK, stroke_width=2)
                         for d in lect])
        addr1 = VGroup(mono("https://example.com", 22, ROUTE), label("· port 443, left out", 22, S.GREY)
                       ).arrange(RIGHT, buff=0.2)
        addr2 = VGroup(mono("http://localhost", 22, ROUTE), mono(":9000", 22, TURN),
                       label("· the port, written out", 22, S.GREY)).arrange(RIGHT, buff=0.06)
        addr2[2].shift(RIGHT * 0.14)
        addrs = VGroup(addr1, addr2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-1.2, -2.6, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref0), FadeIn(lap), FadeIn(lap_l), FadeIn(srv), FadeIn(srv_l), run_time=0.7)
            self.play(GrowArrow(req), FadeIn(req_l), run_time=0.6)
            # the envelopes ride inside the loop (under the request arrow, over the response arrow), so
            # they never cover the arrow labels
            dy_req = DOWN * (e_req.height / 2 + 0.12)
            e_req.move_to(req.get_start() + RIGHT * (e_req.width / 2 + 0.1) + dy_req)
            self.play(FadeIn(e_req, scale=0.8), run_time=0.25)
            self.play(e_req.animate.move_to(req.get_end() + LEFT * (e_req.width / 2 + 0.25) + dy_req), run_time=0.9)
            self.play(FadeOut(e_req), run_time=0.2)
            vo.wait_until("a server sends a response")
            self.play(GrowArrow(res), FadeIn(res_l), run_time=0.6)
            dy_res = UP * (e_res.height / 2 + 0.12)
            e_res.move_to(res.get_start() + LEFT * (e_res.width / 2 + 0.25) + dy_res)
            self.play(FadeIn(e_res, scale=0.8), run_time=0.25)
            self.play(e_res.animate.move_to(res.get_end() + RIGHT * (e_res.width / 2 + 0.1) + dy_res), run_time=0.9)
            self.play(FadeOut(e_res), run_time=0.2)
            vo.wait_until("A port picks which program")
            self.play(LaggedStart(*[FadeIn(d, target_position=srv.get_right()) for d in lect], lag_ratio=0.2),
                      LaggedStart(*[Create(s) for s in studs], lag_ratio=0.2), FadeIn(lect_h), run_time=0.9)
            self.play(LaggedStart(*[FadeIn(d, target_position=srv.get_right()) for d in tut], lag_ratio=0.2),
                      FadeIn(tut_h), run_time=1.0)
            vo.wait_until("public sites leave")
            self.play(FadeIn(addr1, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(lect[1], color=TURN), Indicate(lect[2], color=TURN), run_time=0.8)
            vo.wait_until("ours show the port")
            self.play(FadeIn(addr2, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(addr2[1], color=TURN, scale_factor=1.2), Indicate(tut[0], color=TURN), run_time=0.8)

        # ========================================================== 1. the ladder, and one API for every client
        ref1 = lref("27–28 (APIs)")
        loop = VGroup(lap, srv, req, res)
        small = loop.copy().scale(0.36).move_to([-4.95, 2.35, 0])
        rungs = [_rung(LADDER[0], CONTAINER), _rung(LADDER[1], CONTAINER), _rung(LADDER[2], CONTAINER),
                 _rung(LADDER[3], TOOL)]
        for r in rungs:
            r.move_to([1.3, 2.3, 0])
        rungs[3][1].set_color(TOOL)
        assert rungs[2].get_left()[0] > small.get_right()[0] + 0.2, (rungs[2].get_left(), small.get_right())
        clients = VGroup(*[grey_chip(s, 22) for s in ("browser", "mobile", "edge")])
        for c, y in zip(clients, (0.55, -0.6, -1.75)):
            c.move_to([-5.3, y, 0])
        merge = np.array([-3.25, -0.6, 0])
        feeds = VGroup(*[Line(c.get_right(), merge, color=ROUTE, stroke_width=4) for c in clients])
        api = cbox("API", 1.7, 0.9, size=24, mono_font=False)
        api.name.move_to(api.frame)
        api.move_to([0.45, -0.6, 0])
        trunk = Arrow(merge, api.get_left(), buff=0.02, color=ROUTE, stroke_width=4, tip_length=0.2)
        rest_l = label("REST / JSON", 20, ROUTE).next_to(trunk, UP, buff=0.1).shift(LEFT * 0.35)
        divider = DashedLine([-1.35, 1.25, 0], [-1.35, -2.5, 0], color=S.GREY_DARK, stroke_width=2.5,
                             dash_length=0.12)
        backs = VGroup(*[grey_chip(s, 22) for s in ("stores", "databases", "models")])
        for c, y in zip(backs, (0.55, -0.6, -1.75)):
            c.move_to([4.3, y, 0])
        fans = VGroup(*[Arrow(api.get_right(), c.get_left(), buff=0.08, color=S.GREY, stroke_width=3,
                              tip_length=0.16) for c in backs])
        with self.voiceover(SAY[1]) as vo:
            self.play(ReplacementTransform(ref0, ref1),
                      FadeOut(VGroup(lap_l, srv_l, req_l, res_l, lect, tut, lect_h, tut_h, studs, addrs)),
                      run_time=0.5)
            self.play(Transform(loop, small), FadeIn(rungs[0], shift=DOWN * 0.15), run_time=0.7)
            cur = rungs[0]
            for i, cue in ((1, "an API means"), (2, "a REST API"), (3, "built with FastAPI")):
                vo.wait_until(cue)
                self.play(Transform(cur[0], rungs[i][0]), Transform(cur[1], rungs[i][1]), run_time=0.5)
            vo.wait_until("Every client")
            self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.2) for c in clients], lag_ratio=0.2), run_time=0.6)
            self.play(LaggedStart(*[Create(f) for f in feeds], lag_ratio=0.15), Create(divider), run_time=0.6)
            self.play(GrowArrow(trunk), FadeIn(rest_l), FadeIn(api), run_time=0.7)
            vo.wait_until("and only the API")
            self.play(LaggedStart(*[GrowArrow(f) for f in fans], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(c, shift=RIGHT * 0.15) for c in backs], lag_ratio=0.15), run_time=0.8)
            self.play(Indicate(api.name, color=TURN, scale_factor=1.2), run_time=0.7)

        # ========================================================== 2. step 1: the README's path misses src
        trk = tracker_a(1)
        t = term(P_LAPTOP, rows=9, title=T_LAPTOP, size=20)
        card1 = readme_card(41, README_41, size=20)
        card1.move_to([-6.45 + card1.width / 2, t.box.get_top()[1] + 0.3 + card1.height / 2, 0])
        assert card1.get_top()[1] < TRACK_BOTTOM - 0.1, card1.get_top()
        slip = erratum_tag("erratum · add src/")
        slip.move_to(card1.frame.get_corner(UR) + np.array([-slip.width / 2 - 0.2, 0, 0]))
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(loop, cur, clients, feeds, divider, trunk, rest_l, api, fans, backs)),
                      FadeOut(ref1), run_time=0.6)
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t), run_time=0.6)
            vo.wait_until("Step 1")
            self.play(FadeIn(card1, shift=DOWN * 0.15), run_time=0.5)
            ln1 = type_capture(self, t, A01, type_time=0.9)[0]
            vo.wait_until("misses src")
            err = out(self, t, [(A01.line(2), ERR)], run_time=0.4)
            self.play(Indicate(card1.body, color=ERR, scale_factor=1.03), run_time=0.6)
            vo.wait_until("A small slip")
            self.play(FadeIn(slip, scale=0.9), track(trk, 1, extra=True), run_time=0.5)
            ln2 = type_capture(self, t, A02, type_time=0.7)[0]
            pin(self, ln2, beside(extra_row(), ln2, buff=0.4))
            out(self, t, A02.at((2, 7)), run_time=0.5)
            self.add(t)
            self.wait(0.6)                       # the listing stays a moment before the strip shrinks

        # ========================================================== 3. step 2: docker-shell.sh
        panel = code(DS, 13, 21, font_size=20, shown="docker-shell.sh")
        panel.move_to([-6.45 + panel.width / 2, 0.75, 0])
        ln_build = code_span(panel.code, 0, "docker build")
        rm_ring = ring(code_span(panel.code, 3, "--rm"), S.GREY)
        v_bars = span_bar(panel.code, 4, 6, OWN, 0.22)
        p_ring = ring(code_span(panel.code, 7, "-p 9000:9000"), ROUTE)
        # the tunnel picture (right of the panel): laptop wall door 9000 -> container door 9000
        tx0 = panel.get_right()[0] + 0.35
        lapf = RoundedRectangle(width=6.45 - tx0, height=2.7, corner_radius=0.14, stroke_color=LAPTOP,
                                stroke_width=3).set_fill(S.BG, 1).move_to([(tx0 + 6.45) / 2, 0.55, 0])
        lapt = label("your laptop", 20, LAPTOP).next_to(lapf.get_corner(UR), DL, buff=0.12)
        cont = RoundedRectangle(width=1.5, height=1.5, corner_radius=0.1, stroke_color=CONTAINER,
                                stroke_width=3).set_fill(tint(CONTAINER), 1)
        cont.move_to([lapf.get_right()[0] - 0.95, lapf.get_y() - 0.25, 0])
        contt = label("container", 20, CONTAINER).next_to(cont, UP, buff=0.08)
        d_out = door("9000", color=LAPTOP).move_to([lapf.get_left()[0], cont.get_y(), 0])
        d_in = door("9000", color=CONTAINER).move_to([cont.get_left()[0], cont.get_y(), 0])
        pipe = Line(d_out.get_right(), d_in.get_left(), color=ROUTE, stroke_width=6)
        tunnel = VGroup(lapf, lapt, cont, contt, pipe, d_out, d_in)
        assert pipe.get_length() > 0.3, pipe.get_length()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(card1), FadeOut(slip), track(trk, 2), run_time=0.5)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.5)
            cd_prompt(self, t, P_V1_API)
            ln_sh = type_capture(self, t, A03, type_time=0.6)[0]
            vo.wait_until("It builds the image")
            self.play(ln_build.animate.set_color(TOOL), run_time=0.5)
            self.add(panel)
            vo.wait_until("removes itself on exit")
            self.play(Create(rm_ring), run_time=0.5)
            vo.wait_until("mounts your code")
            self.play(FadeIn(v_bars), run_time=0.5)
            vo.wait_until("and publishes port 9000")
            self.play(Create(p_ring), run_time=0.5)
            self.play(FadeIn(VGroup(lapf, lapt, d_out)), run_time=0.4)
            self.play(FadeIn(VGroup(cont, contt, d_in)), Create(pipe), run_time=0.7)
            vo.wait_until("Pause and run it")
            turn = on_bar(t, turn_row())       # the typed row runs to x 5.1: the tag rides the title bar
            self.play(FadeIn(turn, shift=LEFT * 0.1), run_time=0.4)
            t.add(turn)
            flash_tag(self, turn, TURN)
            self.add(t)

        # ========================================================== 4. step 3: uvicorn is the server, FastAPI the app
        build = [(A03.line(3)[:len("[+] Building 49.9s (11/11) FINISHED")] + "…", S.GREY), "…",
                 cut(A03.line(30), "cheese-app-api-service:latest"),
                 cut(A03.line(31), "cheese-app-api-service:latest"),
                 (A03.line(32), OWN)] + A03.at((33, 37))
        v = ServerAppDiagram().shift(V3_AT)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(panel, rm_ring, v_bars, p_ring, tunnel)), run_time=0.4)
            t.remove(turn)
            self.play(FadeOut(turn), run_time=0.2)
            resize(self, t, 11, run_time=0.5)
            rows = out(self, t, build, run_time=0.6)
            r33 = [r for r in rows if r.text == A03.line(33)][0]
            r35 = [r for r in rows if r.text == A03.line(35)][0]
            pin(self, r35, beside(time_row(), r35, buff=0.4))
            pin(self, r33, beside(row_tag("your prompt shows your own user · on a Mac: aarch64"), r33, buff=0.4))
            vo.wait_until("the README's long uvicorn line")
            self.play(track(trk, 3), run_time=0.4)
            uv = type_at(self, t, A03, 38, type_time=1.6)
            uv_rows = rows_of(uv)
            assert len(uv_rows) == 2, [r.text for r in uv_rows]
            vo.wait_until("Here, uvicorn is the server")
            resize(self, t, 4, keep=uv_rows, extra=[FadeIn(v.container), FadeIn(v.title)], run_time=0.7)
            self.play(FadeIn(v.uvicorn), FadeIn(v.u_title), run_time=0.5)
            vo.wait_until("it owns the port")
            self.play(FadeIn(v.socket, scale=1.3), run_time=0.5)
            self.play(Indicate(v.socket, color=TURN, scale_factor=1.2), run_time=0.6)
            vo.wait_until("FastAPI is the app")
            self.play(FadeIn(v.card, shift=DOWN * 0.15), run_time=0.6)
            self.add(v)
            self.play(Indicate(v.card.title, color=TOOL, scale_factor=1.15), run_time=0.6)
            v.heal(self)
            self.add(t)
        assert t.box.get_top()[1] < v.container.get_bottom()[1] - 0.02, (t.box.get_top(), v.container.get_bottom())

        # ========================================================== 5. api.service:app is an address
        row0, row1 = uv_rows
        with self.voiceover(SAY[5]) as vo:
            tgt = substring(row0, "api.service:app")
            self.play(tgt.animate.set_color(ROUTE), run_time=0.5)
            self.add(t)
            vo.wait_until("is an address")
            v.split_target(self, src=tgt, run_time=0.9)
            for i, cue in enumerate(("folder api", "file service dot py", "variable app")):
                vo.wait_until(cue)
                self.play(Indicate(v.chips[i], color=ROUTE, scale_factor=1.12), run_time=0.6)
                v.heal(self)

        # ========================================================== 6. --host 0.0.0.0, --reload, "$@"
        args = row_tag("extra arguments · none here")
        on_bar(t, args)
        with self.voiceover(SAY[6]) as vo:
            self.play(substring(row0, "--host 0.0.0.0").animate.set_color(OWN), run_time=0.5)
            self.add(t)
            v.plates(self, run_time=0.5)
            vo.wait_until("the container's own loopback")
            v.bind(self, "0.0.0.0", run_time=0.7)
            vo.wait_until("where the tunnel arrives")
            tick1 = v.walk_in(self, "eth0", ok=True, run_time=1.0)
            vo.wait_until("Reload restarts the app")
            self.play(substring(row1, "--reload --reload-dir api/").animate.set_color(TOOL), run_time=0.5)
            self.add(t)
            eye = eye_glyph(0.24).next_to(v.chips[0], RIGHT, buff=0.1)
            assert eye.get_right()[0] < v.card.head.get_left()[0], (eye.get_right(), v.card.head.get_left())
            v.show(self, eye, anims=[FadeIn(eye, scale=1.4)], run_time=0.5)
            self.play(Indicate(eye, color=TOOL, scale_factor=1.25), run_time=0.6)
            v.heal(self)
            vo.wait_until("the last part passes on")
            dollar = ring(substring(row1, '"$@"'), S.GREY)
            self.play(Create(dollar), FadeIn(args, shift=LEFT * 0.1), run_time=0.6)
            row1.add(dollar)
            t.add(args)
            self.add(t)

        # ========================================================== 7. the log agrees
        with self.voiceover(SAY[7]) as vo:
            log1 = out(self, t, A03.at(39, 40), run_time=0.5)
            self.play(substring(log1[1], "Uvicorn running on http://0.0.0.0:9000").animate.set_color(ROUTE),
                      run_time=0.5)
            self.add(t)
            vo.wait_until("a reloader watching api")
            log2 = out(self, t, A03.at(41), run_time=0.4)
            self.play(substring(log2[0], "Started reloader process").animate.set_color(TOOL),
                      substring(log2[0], "using StatReload").animate.set_color(TOOL),
                      Indicate(eye, color=TOOL, scale_factor=1.2), run_time=0.6)
            self.add(t)
            v.heal(self)
            vo.wait_until("startup complete")
            out(self, t, A03.at((42, 43)) + [(A03.line(44), OWN)], run_time=0.6)

        # ========================================================== 8. service.py: the app, CORS, one route
        p5 = code(SVC, 5, 14, font_size=20, cuts={5: "app = FastAPI("}, shown="api/service.py")
        # the code's top sits under V3's title row (the header's words stay left of the title)
        p5.shift(np.array([-6.45 - p5.get_left()[0], 2.25 - p5.code.get_top()[1], 0]))
        bar5 = line_bar(p5.code, 0, TOOL, 0.3)
        p5.add(bar5)
        cors = ring(VGroup(*[p5.code.code_lines[k] for k in range(3, 10)]), S.GREY, buff=0.1)
        end2 = grey_chip("part 2's ending").next_to(cors, DOWN, buff=0.18).align_to(cors, LEFT)
        p17 = code(SVC, 17, 20, font_size=20, shown="api/service.py")
        p17.move_to([-6.45 + p17.width / 2, -3.5 + p17.height / 2, 0])
        bars = span_bar(p17.code, 1, 3, TURN, 0.22)
        shift_v = RIGHT * 2.0
        with self.voiceover(SAY[8]) as vo:
            # the plates, the 0.0.0.0 binding, the tick and the eye have done their job: they leave with
            # the terminal (the opaque panel would otherwise cut them into fragments, and the eye would
            # run into the route row). The plates come back in beat 12.
            v.drop(self, v.eth0, v.lo, v.binds, tick1, eye, extra=[FadeOut(t)], run_time=0.5)
            v.eth0 = v.lo = v.badge = v.host = None
            v.binds = VGroup()
            v.add(v.binds)
            self.play(v.animate.shift(shift_v), run_time=0.6)
            self.play(FadeIn(p5, shift=RIGHT * 0.2), run_time=0.6)
            assert p5.get_right()[0] < v.socket.get_left()[0] - 0.05, (p5.get_right(), v.socket.get_left())
            assert p5.header.get_right()[0] < v.title.get_left()[0] - 0.1, (p5.header.get_right(), v.title.get_left())
            assert p5.code.get_top()[1] < v.title.get_bottom()[1] - 0.03, (p5.code.get_top(), v.title.get_bottom())
            assert end2.get_bottom()[1] > -3.55, end2.get_bottom()
            vo.wait_until("the app adds CORS middleware")
            self.play(Create(cors), FadeIn(end2, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("and one route")
            self.play(FadeOut(cors), FadeOut(end2), FadeOut(p5, shift=DOWN * 0.2), run_time=0.5)
            self.play(FadeIn(p17, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(bars), run_time=0.4)
            assert p17.get_top()[1] < v.container.get_bottom()[1] - 0.05, (p17.get_top(), v.container.get_bottom())
            vo.wait_until("GET slash returns a welcome")
            v.add_route(self, "GET / → get_index", run_time=0.6)
            self.play(v.flash_route(0), Indicate(p17.code.code_lines[1], color=TURN, scale_factor=1.05),
                      run_time=0.8)
            v.heal(self)

        # ========================================================== 9. step 4: localhost:9000, and an extra curl
        ref2 = lref("34–41 (APIs)")
        tr = RequestTrace("localhost:9000", rows=("api",), browser_w=4.0).shift(UP * 0.84)
        ill = illustration_tag().next_to(tr.browser, UP, buff=0.03).align_to(tr.browser, LEFT)
        assert ill.get_top()[1] < TRACK_BOTTOM - 0.05, ill.get_top()
        tab = term(P_LAPTOP, rows=4, title=T_TAB, size=20)
        same = on_bar(tab, row_tag("extra · the same request"))
        turn9 = row_tag("▶ your turn", TURN)
        turn9.move_to([tab.dots.get_right()[0] + 0.3 + turn9.width / 2, same.get_y(), 0])
        assert same.get_left()[0] > tab.title.get_right()[0] + 0.05, (same.get_left(), tab.title.get_right())
        assert tab.box.get_top()[1] < tr.net.frame.get_bottom()[1] - 0.02
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(p17, bars)), FadeOut(v), track(trk, 4), run_time=0.6)
            self.play(FadeIn(tr), FadeIn(ill), FadeIn(ref2), run_time=0.7)
            vo.wait_until("open localhost 9000")
            self.play(tr.browser.flash(TURN), Indicate(tr.browser.address, color=ROUTE, scale_factor=1.15),
                      run_time=0.7)
            tr.heal(self)
            vo.wait_until("An extra curl")
            self.play(FadeIn(tab, shift=UP * 0.2), FadeIn(same, shift=UP * 0.2), run_time=0.5)
            tab.add(same)
            type_capture(self, tab, A04, type_time=0.8)
            vo.wait_until("status 200 from uvicorn")
            o9 = out(self, tab, [(A04.line(2), OWN), A04.line(4)], run_time=0.4)
            self.play(substring(o9[1], "uvicorn").animate.set_color(TOOL), run_time=0.4)
            self.add(tab)
            vo.wait_until("and the welcome")
            out(self, tab, [A04.line(6), JSON], run_time=0.4)
            tr.browser.fill(self, ['{"message":', '"Welcome to AC215"}'], mono_font=True)
            vo.wait_until("Pause and try it")
            self.play(FadeIn(turn9, shift=LEFT * 0.1), run_time=0.4)
            tab.add(turn9)
            flash_tag(self, turn9, TURN)
            self.add(tab)

        # ========================================================== 10. the lecture's trip, hop by hop
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(tab), run_time=0.4)
            tr.hop(self, 1, "api", run_time=0.6)
            vo.wait_until("forwarded to the published port")
            tr.hop(self, 2, "api", run_time=0.6)
            vo.wait_until("mapped into the container")
            tr.hop(self, 3, "api", run_time=0.6)
            vo.wait_until("the function runs")
            tr.hop(self, 4, "api", text="4 the function runs: get_index", run_time=0.7)
            vo.wait_until("and the JSON comes back")
            tr.hop(self, 5, "api", run_time=0.7)
            tr.hop(self, 6, run_time=0.6)

        # ========================================================== 11. a kind note on slide 37
        bx = tr.net.boxes["api"]
        old_t = steady("localhost:9000", 20, S.GREY, mono_font=True)
        old_b = RoundedRectangle(width=old_t.width + 0.5, height=0.5, corner_radius=0.12, stroke_color=S.GREY,
                                 stroke_width=2.5).set_fill(S.BG, 1)
        new_t = steady("port 9000 of the container · listening on 0.0.0.0", 20, INK)
        new_b = RoundedRectangle(width=new_t.width + 0.5, height=0.5, corner_radius=0.12, stroke_color=CONTAINER,
                                 stroke_width=2.5).set_fill(tint(CONTAINER), 1)
        spot = np.array([tr.net.frame.get_x(), bx.get_bottom()[1] - 0.55, 0])
        for m in (old_t, old_b, new_t, new_b):
            m.move_to(spot)
        tie = Line(bx.get_bottom(), old_b.get_top(), color=S.GREY, stroke_width=2.5)
        notes = VGroup(erratum_tag(), grey_chip("slide 37")).arrange(RIGHT, buff=0.2)
        notes.next_to(old_b, DOWN, buff=0.2)
        assert notes.get_bottom()[1] > tr.net.frame.get_bottom()[1] + 0.05, notes.get_bottom()
        assert new_b.get_left()[0] > tr.net.frame.get_left()[0] + 0.05
        assert new_b.get_right()[0] < tr.net.frame.get_right()[0] - 0.05
        with self.voiceover(SAY[11]) as vo:
            tr.clear_hops(self, run_time=0.4)
            vo.wait_until("the slide labels the inside")
            self.play(Create(tie), FadeIn(old_b), FadeIn(old_t), run_time=0.6)
            self.play(FadeIn(notes, shift=UP * 0.1), run_time=0.4)
            self.wait(0.8)
            self.play(Circumscribe(bx, color=CONTAINER, stroke_width=3, buff=0.08), run_time=1.0)
            tr.heal(self)
            self.add(tie, old_b, old_t, notes)
            vo.wait_until("Take it as port 9000")
            self.play(Transform(old_b, new_b), Transform(old_t, new_t), run_time=0.9)
            vo.wait_until("uvicorn listens on 0.0.0.0")
            self.play(Indicate(old_t, color=OWN, scale_factor=1.06), Indicate(tr.net.inner["api"], color=TOOL),
                      run_time=0.8)
            tr.heal(self)
            self.add(tie, old_b, old_t, notes)   # back above the laptop's opaque frame
            self.wait(1.0)
            self.play(Circumscribe(old_b, color=CONTAINER, stroke_width=3, buff=0.06), run_time=1.1)
            self.add(tie, old_b, old_t, notes)

        # ========================================================== 12. what if it listened on 127.0.0.1?
        b_icon = browser_icon(0.9, name="your browser")
        curl_box = RoundedRectangle(width=0.86, height=0.44, corner_radius=0.08, stroke_color=S.GREY,
                                    stroke_width=2.5).set_fill(TERM_BG, 1)
        curl_t = mono("curl", 20, INK).move_to(curl_box)
        curl_i = VGroup(curl_box, curl_t)
        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(VGroup(tr, ill, tie, old_b, old_t, notes)), FadeOut(ref2), run_time=0.6)
            eth0 = door("eth0", color=S.GREY, size=v.size).move_to(v.p(-4.5, 0.55))
            lo = door("lo · 127.0.0.1", color=S.GREY, size=v.size, mono_font=False).move_to(v.p(-3.2, -1.55))
            self.play(FadeIn(v), FadeIn(eth0), FadeIn(lo), run_time=0.7)
            self.remove(eth0, lo)
            v.add(eth0, lo)
            v.eth0, v.lo = eth0, lo
            v.heal(self)
            v.bind(self, "0.0.0.0", run_time=0.5)
            b_icon.move_to([-5.55, v.eth0.get_y() - 0.1, 0])
            curl_i.move_to(v.p(-3.95, -0.62))
            assert curl_i.get_left()[0] > v.container.get_left()[0] + 0.08, (curl_i.get_left(), v.container.get_left())
            assert curl_i.get_top()[1] < v.badge.get_bottom()[1] - 0.08, (curl_i.get_top(), v.badge.get_bottom())
            assert lo.get_bottom()[1] > v.container.get_bottom()[1] + 0.1, (lo.get_bottom(), v.container.get_bottom())
            assert b_icon.get_right()[0] < v.eth0.get_left()[0] - 0.6, (b_icon.get_right(), v.eth0.get_left())
            vo.wait_until("If uvicorn listened on 127.0.0.1")
            v.bind(self, "127.0.0.1", run_time=0.8)
            self.play(Indicate(v.badge, color=TURN, scale_factor=1.15), run_time=0.6)
            v.heal(self)
            vo.wait_until("would a curl from inside")
            a_in = DashedVMobject(Arrow(curl_i.get_bottom() + DOWN * 0.03,
                                        [curl_i.get_x() + 0.1, v.lo.get_top()[1] + 0.03, 0], buff=0, color=ROUTE,
                                        stroke_width=4, tip_length=0.15, max_tip_length_to_length_ratio=0.5),
                                  num_dashes=3).set_stroke(ROUTE, 4)
            q_in = label("?", 26, ROUTE).next_to(a_in, LEFT, buff=0.12)
            assert q_in.get_left()[0] > v.container.get_left()[0] + 0.05, (q_in.get_left(), v.container.get_left())
            self.play(FadeIn(curl_i, scale=1.2), run_time=0.4)
            self.play(Create(a_in), FadeIn(q_in), run_time=0.6)
            vo.wait_until("And your browser")
            a_out = DashedVMobject(Arrow(b_icon.window.get_right(), v.eth0.get_left(), buff=0.06, color=ROUTE,
                                         stroke_width=4, tip_length=0.18), num_dashes=7).set_stroke(ROUTE, 4)
            q_out = label("?", 26, ROUTE).next_to(a_out, UP, buff=0.1)
            self.play(FadeIn(b_icon, shift=RIGHT * 0.2), run_time=0.4)
            self.play(Create(a_out), FadeIn(q_out), run_time=0.6)
        card = ponder(self, PONDER_Q, seconds=8, center=(0, -1.45))

        # one group, the card last: it stays above the picture while everything fades
        self.play(FadeOut(VGroup(v, b_icon, curl_i, a_in, q_in, a_out, q_out, card)), FadeOut(trk), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
