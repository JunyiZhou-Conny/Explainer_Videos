"""S04 · A Python function becomes a URL (AC215 L18, part 1). Tracker [A] "README › Backend API
Container" 4 → 8. Lecture: 18 · 39–41 (APIs) in beats 1–2.

Beats (script.md "## S04", one voiceover block each):
0. Ponder 1's answer. S03's last picture comes back (tracker A 4, V3 bound to 127.0.0.1, a `curl`
   glyph inside the container, "your browser" outside): on "Inside, yes" a PINK request runs from the
   curl glyph to the lo · 127.0.0.1 plate and on to the socket (GREEN tick); on "From the browser, no"
   a request comes through the tunnel onto eth0, finds no listener and stops RED; on "That is why"
   the badge flips back to 0.0.0.0 and the request walks in (GREEN tick).
1. Tracker A 5, lecture_ref 39–41. V3 goes; the README card (README.md · lines 52–58) with the
   square_root snippet; on "decorated Python function" its @app.get line gets a PURPLE bracket
   "decorator → route"; on "Add the README's" the GREY chip "your editor" (the heredoc is never
   typed). On "and save" the card goes and a `laptop · second tab` terminal (prompt
   …/cheese-app-v1/src/api-service) types `git -C ~/cheese-app-v1 diff` (row tag extra) → a05:13–21,
   the + lines GREEN; on "x squared plus y squared" the line `z = x**2 + y**2` turns YELLOW.
2. The terminal goes; V3 returns over a 4-row `laptop` strip (the uvicorn terminal): a03:47 YELLOW
   (StatReload …), 48–50; V3's app card slides out and a fresh one slides in with two routes
   (GET / → get_index, GET /square_root/); 51–54 (54 GREEN); the new route flashes on
   "You restarted nothing".
3. Lecture tag off. Tracker A 6. V4 UrlCall over a 4-row `second tab` strip: the URL splits into
   PINK tokens (scheme, host, port, path; the trailing slash flashes), the path finds the function
   (its name and defaults YELLOW). The strip types `curl -s http://localhost:9000/square_root/; echo`
   (extra) → a06:2; the body becomes √(1² + 2²) → 2.23606797749979 (GREEN); a small browser drawing
   (illustration) shows the same number. ▶ your turn on the strip's bar.
4. Tracker A 7. The browser goes; the URL grows `?x=2&y=10`; the strip types
   `curl -s 'http://localhost:9000/square_root/?x=2&y=10'; echo` (extra); on "The query string fills"
   x=2 and y=10 fly into the signature (defaults dim), the body becomes √(2² + 10²); on "back comes"
   a07:2 and the GREEN result 10.198039027185569.
5. Tracker A 7 · extra. The query becomes `?x=abc`; a08's command is typed; on "A letter" `x=abc`
   bounces RED off the first `float` hint and the RED chip "422 · float_parsing" lands; a08:2 (wrap,
   `float_parsing` YELLOW), 3 (`[HTTP 422]` RED).
6. The query goes and the path's trailing slash dims; a09's command is typed; on "FastAPI answers
   307" a PINK U-turn over the path "307 → /square_root/", a09:2 (307 PINK); on "points to the slash
   version" the slash comes back and a09:6 `location: …/square_root/` (PINK).
7. V4 and the tab go; the uvicorn terminal (`laptop`, 8 rows) prints a03:55–59 (wrapped at spaces);
   on "with its status" the status words write in colour one by one: 200 ×3 GREEN, 422 RED,
   307 PINK; IPs and ports stay GREY.
8. Tracker A 8. The log goes; a 4-row `second tab` strip types the a10 grep (extra) → a10:3, 6
   (`<title>API Server - Swagger UI</title>` and `url: '/openapi.json'` YELLOW); a small GREY
   route-table card (V3's two routes) sits above it. On "FastAPI built this page" the strip goes and
   the card unfolds into a GREY browser drawing at localhost:9000/docs (illustration; chip
   "extra · a11 openapi.json"): GET /, GET /square_root/ expanded with x · number · default 1,
   y · number · default 2 and a "Try it out" button. On "x and y appear" those rows flash; on "you can
   try" the button flashes.
9. The signature returns at the top with the RED 422 chip; on "The type hints became" both `float`
   hints glow and two GREEN threads run from them: one to the 422 chip, one to the docs rows; the
   caption "type hints → validation + docs". On "Pause" ▶ your turn beside "Try it out". Fade; empty
   frame.
"""

import re

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ the real sources (checked)
A03 = capture("a03")
A05 = capture("a05")
A06 = capture("a06")
A07 = capture("a07")
A08 = capture("a08")
A09 = capture("a09")
A10 = capture("a10")
A11 = capture("a11")
assert A05.cmd_lines[-1] == "git -C ~/cheese-app-v1 diff", A05.cmd_lines
assert A05.line(13).startswith("@@ -18,3 +18,8 @@") and A05.line(20) == "+    z = x**2 + y**2", A05.at((13, 21))
assert A03.line(47) == "WARNING:  StatReload detected changes in 'api/service.py'. Reloading...", A03.line(47)
assert A03.line(54) == "INFO:     Application startup complete.", A03.line(54)
assert [s.rsplit('"', 1)[1].strip() for s in A03.at((55, 59))] == [
    "200 OK", "200 OK", "200 OK", "422 Unprocessable Entity", "307 Temporary Redirect"], A03.at((55, 59))
assert A06.cmd == "curl -s http://localhost:9000/square_root/; echo" and A06.line(2) == "2.23606797749979"
assert A07.cmd == "curl -s 'http://localhost:9000/square_root/?x=2&y=10'; echo" and A07.line(2) == "10.198039027185569"
assert A08.cmd.endswith("'http://localhost:9000/square_root/?x=abc'") and '"float_parsing"' in A08.line(2)
assert A08.line(3) == "[HTTP 422]", A08.line(3)
assert A09.cmd == "curl -s -i http://localhost:9000/square_root | head -6", A09.cmd
assert A09.line(2) == "HTTP/1.1 307 Temporary Redirect" and A09.line(6) == "location: http://localhost:9000/square_root/"
assert A10.line(3).strip() == "<title>API Server - Swagger UI</title>" and A10.line(6).strip() == "url: '/openapi.json',"
# the docs drawing's parameter rows come from the OpenAPI JSON (a11:32-48, extra)
assert ('"name": "x"' in A11.line(32) and '"type": "number"' in A11.line(36) and '"default": 1' in A11.line(37)
        and '"name": "y"' in A11.line(42) and '"type": "number"' in A11.line(46) and '"default": 2' in A11.line(47))

README_V1 = f"{V1}/README.md"
R52 = md_plain(readme(52, V1))
R_CODE = [s.rstrip() for s in excerpt(README_V1, 54, 57).split("\n")]
assert R52 == "• Add the following code at the end of the file:", R52
assert R_CODE[0] == '@app.get("/square_root/")' and R_CODE[2] == "    z = x**2 + y**2", R_CODE
assert excerpt(README_V1, 53, 53).strip() == "```" and excerpt(README_V1, 58, 58).strip() == "```"
# the diff's added lines are the README's snippet, unchanged
assert [s[1:] for s in A05.at((18, 21))] == R_CODE, A05.at((18, 21))

V3_END = np.array([2.0, 0.8, 0])     # where S03's ponder left V3
V3_STRIP = UP * 0.8                  # V3 over a 4-row 20 pt strip (strip top -1.18, V3 bottom -1.15)
U_AT = UP * 0.55 + LEFT * 1.4        # V4 over a 4-row strip, left so the beat-3 browser fits at the right


class _Quiet:
    """A stand-in scene for building a piece's state without playing it (nothing is drawn)."""
    mobjects: list = []

    def play(self, *a, **k):
        pass

    def add(self, *m):
        pass

    def remove(self, *m):
        pass


def _first_row(rows, sub):
    for r in rows:
        if sub in r.text:
            return r
    raise KeyError(sub)


class FunctionToUrl(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S04"] == 10, len(SAY)

        # ========================================================== 0. the ponder's answer
        trk = tracker_a(4)
        v = ServerAppDiagram()
        v.shift(V3_END - v.ref.get_center())
        quiet = _Quiet()                     # S03's end state, built without playing anything
        v.add_route(quiet, "GET / → get_index")
        v.split_target(quiet)
        eye = eye_glyph(0.24).next_to(v.chips[0], RIGHT, buff=0.1)
        v.show(quiet, eye)
        v.bind(quiet, "127.0.0.1")
        b_icon = browser_icon(0.9, name="your browser")
        curl_box = RoundedRectangle(width=0.95, height=0.44, corner_radius=0.08, stroke_color=S.GREY,
                                    stroke_width=2.5).set_fill(TERM_BG, 1)
        curl_i = VGroup(curl_box, mono("curl", 20, INK).move_to(curl_box))
        curl_i.move_to(v.p(-4.05, -0.62))
        with self.voiceover(SAY[0]) as vo:
            b_icon.move_to([-5.55, v.eth0.get_y() - 0.1, 0])
            assert b_icon.get_right()[0] < v.eth0.get_left()[0] - 0.6, (b_icon.get_right(), v.eth0.get_left())
            self.play(FadeIn(trk), FadeIn(v), FadeIn(b_icon), FadeIn(curl_i), run_time=0.7)
            vo.wait_until("Inside, yes")
            d = pulse_dot(ROUTE, 0.11).move_to(curl_i.get_bottom())
            self.add(d)
            self.play(d.animate.move_to(v.lo.get_center()), run_time=0.6)
            self.play(d.animate.move_to(v.socket.get_center()), run_time=0.6)
            tick0 = check_glyph(0.32, OWN).next_to(v.socket, DOWN, buff=0.1)
            self.play(FadeIn(tick0, scale=1.3), FadeOut(d), Indicate(v.lo, color=OWN), run_time=0.5)
            self.remove(d)
            vo.wait_until("From the browser, no")
            self.play(Indicate(b_icon, color=ROUTE, scale_factor=1.1), run_time=0.5)
            cross = v.walk_in(self, "eth0", ok=False, run_time=1.2)
            vo.wait_until("where nothing listens")
            self.play(Indicate(v.eth0, color=ERR, scale_factor=1.12), run_time=0.7)
            v.heal(self)
            vo.wait_until("That is why")
            v.drop(self, cross, run_time=0.3, extra=[FadeOut(tick0)])
            v.bind(self, "0.0.0.0", run_time=0.7)
            self.play(Indicate(v.badge, color=OWN, scale_factor=1.15), run_time=0.5)
            v.heal(self)
            tick1 = v.walk_in(self, "eth0", ok=True, run_time=1.0)

        # ========================================================== 1. step 5: add the route
        ref = lref("39–41 (APIs)")
        body = VGroup(label(R52, 20, INK),
                      VGroup(*[mono_line(s, 20, INK) for s in R_CODE]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for ln in body[1]:
            ln.shift(RIGHT * (body[1][0].strut.get_left()[0] - ln.strut.get_left()[0]))
        card1 = readme_card((52, 58), body)
        card1.move_to([-6.45 + card1.width / 2, 0.9, 0])
        dec = body[1][0]
        bracket = ring(dec, TOOL)
        dec_l = label("decorator → route", 20, TOOL).next_to(bracket, RIGHT, buff=0.25)
        ed = editor_chip().next_to(card1, RIGHT, buff=0.35).align_to(card1, UP)
        assert card1.get_top()[1] < TRACK_BOTTOM - 0.05 and dec_l.get_right()[0] < 6.5
        assert ed.get_right()[0] < 6.5, ed.get_right()
        t = term(P_V1_API, rows=11, title=T_TAB, size=20)
        with self.voiceover(SAY[1]) as vo:
            v.remove(tick1)
            self.play(FadeOut(v), FadeOut(tick1), FadeOut(b_icon), FadeOut(curl_i), track(trk, 5), run_time=0.6)
            self.play(FadeIn(ref), FadeIn(card1, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("decorated Python function")
            self.play(Create(bracket), FadeIn(dec_l, shift=LEFT * 0.1), run_time=0.6)
            self.play(Indicate(dec, color=TOOL, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Add the README's")
            self.play(FadeIn(ed, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, ed, S.GREY)
            vo.wait_until("and save")
            self.play(FadeOut(VGroup(card1, bracket, dec_l, ed), shift=UP * 0.2), FadeIn(t), run_time=0.5)
            gd = type_capture(self, t, A05, type_time=0.8)[0]
            pin(self, gd, beside(extra_row(), gd, buff=0.4))
            diff = [(s, OWN) if s.startswith("+") else s for s in A05.at((13, 21))]
            rows = out(self, t, diff, run_time=0.7)
            vo.wait_until("x squared plus y squared")
            zr = _first_row(rows, "z = x**2 + y**2")
            self.play(substring(zr, "z = x**2 + y**2").animate.set_color(TURN), run_time=0.5)
            self.add(t)
            self.play(Indicate(substring(zr, "x**2 + y**2"), color=TURN, scale_factor=1.08), run_time=0.7)
            self.add(t)

        # ========================================================== 2. StatReload: a fresh app
        ut = term(container_prompt(A03, 38), rows=4, title=T_LAPTOP, size=20)
        v.shift(V3_STRIP - v.ref.get_center())
        assert ut.box.get_top()[1] < v.container.get_bottom()[1] - 0.02, (ut.box.get_top(), v.container.get_bottom())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(t), run_time=0.4)
            self.play(FadeIn(v), FadeIn(ut), run_time=0.6)
            vo.wait_until("StatReload sees the change")
            w = out(self, ut, [(A03.line(47), TURN)] + A03.at((48, 50)), run_time=0.6)
            self.play(Indicate(substring(w[0], "StatReload detected changes"), color=TURN, scale_factor=1.05),
                      run_time=0.6)
            self.add(ut)
            vo.wait_until("swaps in a fresh app")
            v.reload(self, ["GET / → get_index", "GET /square_root/"], run_time=1.2)
            out(self, ut, A03.at((51, 53)) + [(A03.line(54), OWN)], run_time=0.6)
            vo.wait_until("You restarted nothing")
            self.play(v.flash_route(1), run_time=0.8)
            v.heal(self)

        # ========================================================== 3. step 6: the URL finds the function
        u = UrlCall()
        u.shift(U_AT - u.ref.get_center())
        tab = term(P_V1_API, rows=4, title=T_TAB, size=20)
        br = Browser("localhost:9000/square_root/", win_w=4.4, win_h=1.3)
        br.move_to([6.45 - br.width / 2, -0.45, 0])
        ill = illustration_tag().next_to(br, UP, buff=0.05).align_to(br, RIGHT)
        turn3 = row_tag("▶ your turn", TURN)
        turn3.move_to([tab.dots.get_right()[0] + 0.3 + turn3.width / 2, tab.box.get_top()[1] - tab.bar_h / 2, 0])
        assert br.get_top()[1] < u.sig.get_bottom()[1] - 0.05 or br.get_left()[0] > u.sig.get_right()[0] + 0.05
        assert br.get_bottom()[1] > tab.box.get_top()[1] + 0.05, (br.get_bottom(), tab.box.get_top())
        assert ill.get_top()[1] < u.sig.get_bottom()[1] or ill.get_left()[0] > u.sig.get_right()[0], ill.get_top()
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(v), FadeOut(ut), FadeOut(ref), track(trk, 6), run_time=0.6)
            self.play(FadeIn(u), FadeIn(tab), run_time=0.6)
            vo.wait_until("open square root")
            u.split(self, run_time=0.9)
            vo.wait_until("with its trailing slash")
            self.play(Indicate(u.tokens["path"][-1], color=TURN, scale_factor=1.6), run_time=0.6)
            u.heal(self)
            u.match(self, run_time=0.9)
            vo.wait_until("No arguments")
            type_capture(self, tab, A06, type_time=0.8)
            ex3 = extra_row()
            on_bar(tab, ex3)
            self.play(FadeIn(ex3), run_time=0.3)
            tab.add(ex3)
            vo.wait_until("the defaults 1 and 2 apply")
            self.play(Indicate(u.default(0), color=TURN, scale_factor=1.25),
                      Indicate(u.default(1), color=TURN, scale_factor=1.25), run_time=0.7)
            u.heal(self)
            b5 = mono_line("√(1² + 2²)", 26, INK).move_to(u.body).align_to(u.body.strut, LEFT)
            u.body = u.swap(self, u.body, b5, run_time=0.5)
            vo.wait_until("the square root of 5")
            out(self, tab, [(A06.line(2), OWN)], run_time=0.4)
            u.result(self, A06.line(2), run_time=0.6)
            assert u.res.get_right()[0] < br.get_left()[0] - 0.1, (u.res.get_right(), br.get_left())
            self.play(FadeIn(br), FadeIn(ill), run_time=0.5)
            br.fill(self, [A06.line(2)], mono_font=True)
            vo.wait_until("Pause and try it")
            self.play(FadeIn(turn3, shift=LEFT * 0.1), run_time=0.4)
            tab.add(turn3)
            flash_tag(self, turn3, TURN)
            self.add(tab)

        # ========================================================== 4. step 7: the query fills the arguments
        with self.voiceover(SAY[4]) as vo:
            tab.remove(turn3)
            self.play(FadeOut(br), FadeOut(ill), FadeOut(turn3), track(trk, 7), run_time=0.5)
            u.reset(self, run_time=0.4)
            vo.wait_until("add x equals 2")
            u.add_query(self, "?x=2&y=10", run_time=0.6)
            type_capture(self, tab, A07, type_time=1.0)
            vo.wait_until("The query string fills")
            u.fly_args(self, run_time=1.4)
            vo.wait_until("and back comes")
            out(self, tab, [(A07.line(2), OWN)], run_time=0.4)
            u.result(self, A07.line(2), run_time=0.7)
            self.play(Indicate(u.res, color=OWN, scale_factor=1.06), run_time=0.6)
            u.heal(self)

        # ========================================================== 5. extra: a letter bounces off the hint
        with self.voiceover(SAY[5]) as vo:
            self.play(track(trk, 7, extra=True), run_time=0.4)
            u.reset(self, run_time=0.4)
            qa = mono_line("?x=abc", 26, ROUTE).move_to(u.query).align_to(u.query.strut, LEFT)
            u.query = u.swap(self, u.query, qa, run_time=0.5)
            type_capture(self, tab, A08, type_time=1.4)
            vo.wait_until("A letter instead of a number")
            e422 = u.bounce(self, "x=abc", code="422 · float_parsing", run_time=1.4)
            rows8 = out(self, tab, A08.at(2) + [(A08.line(3), ERR)], wrap=True, run_time=0.6)
            fp = _first_row(rows8, "float_parsing")
            self.play(substring(fp, "float_parsing").animate.set_color(TURN), run_time=0.4)
            self.add(tab)

        # ========================================================== 6. extra: no slash, 307
        slash = u.tokens["path"][-1]
        with self.voiceover(SAY[6]) as vo:
            qcap = u.captions[-1]
            u.drop(self, u.query, qcap, run_time=0.4, extra=[slash.animate.set_opacity(0.2)])
            u.query = None
            type_capture(self, tab, A09, type_time=1.0)
            vo.wait_until("FastAPI answers 307")
            r9 = out(self, tab, [(A09.line(2), ROUTE)], run_time=0.4)
            u.uturn(self, "307 → /square_root/", run_time=0.8)
            vo.wait_until("points to the slash version")
            self.play(slash.animate.set_opacity(1), run_time=0.4)
            self.play(Indicate(slash, color=TURN, scale_factor=1.8), run_time=0.6)
            u.heal(self)
            out(self, tab, [(A09.line(6), ROUTE)], run_time=0.4)

        # ========================================================== 7. the server's log
        lt = term(container_prompt(A03, 38), rows=8, title=T_LAPTOP, size=20)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(u), FadeOut(tab), run_time=0.5)
            self.play(FadeIn(lt), run_time=0.4)
            logs = out(self, lt, A03.at((55, 59)), wrap=True, run_time=0.8)
            # each request's status (a wrapped line carries its status words on the next row)
            spans, codes, i = [], [], 0
            while i < len(logs):
                m = re.search(r'HTTP/1\.1" (\d{3})', logs[i].text)
                assert m, logs[i].text
                g = VGroup(*glyph_range(logs[i], m.start(1)))
                if i + 1 < len(logs) and not logs[i + 1].text.startswith("INFO:"):
                    g.add(*logs[i + 1].glyphs)
                    i += 1
                codes.append(m.group(1))
                spans.append((g, {"200": OWN, "422": ERR, "307": ROUTE}[m.group(1)]))
                i += 1
            assert codes == ["200", "200", "200", "422", "307"], codes
            vo.wait_until("with its status")
            for g, col in spans:
                self.play(g.animate.set_color(col), run_time=0.35)
            self.add(lt)
            self.play(LaggedStart(*[Indicate(g, color=col, scale_factor=1.12) for g, col in spans], lag_ratio=0.25),
                      run_time=1.2)
            self.add(lt)

        # ========================================================== 8. step 8: /docs
        tab8 = term(P_V1_API, rows=4, title=T_TAB, size=20)
        tbl_rows = VGroup(*[mono(s, 20, INK) for s in ("GET /", "GET /square_root/")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        tbl_h = label("routes", 20, S.GREY)
        tbl_in = VGroup(tbl_h, tbl_rows).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        tbl_fr = RoundedRectangle(width=tbl_in.width + 0.6, height=tbl_in.height + 0.4, corner_radius=0.1,
                                  stroke_color=TOOL, stroke_width=2.5).set_fill(tint(TOOL, 0.14), 1)
        tbl_in.move_to(tbl_fr)
        tbl = VGroup(tbl_fr, tbl_in).move_to([0, 0.7, 0])
        docs = Browser("localhost:9000/docs", win_w=7.6, win_h=3.55)
        docs.move_to([6.45 - docs.width / 2, -1.3, 0])
        btn_t = label("Try it out", 20, INK)
        btn = VGroup(RoundedRectangle(width=btn_t.width + 0.4, height=0.42, corner_radius=0.08, stroke_color=S.GREY,
                                      stroke_width=2).set_fill(S.GREY_DARKER, 1), btn_t)
        btn_t.move_to(btn[0])
        r_get = mono("GET /", 20, INK)
        r_sq = VGroup(mono("GET /square_root/", 20, INK), btn).arrange(RIGHT, buff=0.5)
        r_x = label("x · number · default 1", 20, INK)
        r_y = label("y · number · default 2", 20, INK)
        params = VGroup(r_x, r_y).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        page_rows = [r_get, r_sq, params]
        ill8 = illustration_tag()
        ex8 = extra_tag("openapi.json")
        tags8 = VGroup(ill8, ex8).arrange(RIGHT, buff=0.25).next_to(docs, UP, buff=0.08).align_to(docs, RIGHT)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(lt), track(trk, 8), run_time=0.5)
            self.play(FadeIn(tab8), FadeIn(tbl, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("open slash docs")
            l10 = type_capture(self, tab8, A10, type_time=1.2)[0]
            ex10 = extra_row()
            on_bar(tab8, ex10)
            self.play(FadeIn(ex10), run_time=0.3)
            tab8.add(ex10)
            o10 = out(self, tab8, [A10.line(3), A10.line(6)], run_time=0.4)
            self.play(substring(o10[0], "<title>API Server - Swagger UI</title>").animate.set_color(TURN),
                      substring(o10[1], "url: '/openapi.json'").animate.set_color(TURN), run_time=0.5)
            self.add(tab8)
            vo.wait_until("FastAPI built this page")
            self.play(FadeOut(tab8), run_time=0.4)
            fr_copy = docs.frame.copy()
            self.play(ReplacementTransform(tbl_fr, fr_copy), FadeOut(tbl_in), run_time=0.8)
            self.play(FadeIn(docs), run_time=0.4)
            self.remove(fr_copy)
            self.play(FadeIn(tags8, shift=UP * 0.1), run_time=0.4)
            docs.fill(self, page_rows, buff=0.18, run_time=0.6)
            params.shift(RIGHT * 0.45)
            vo.wait_until("x and y appear as numbers")
            self.play(Indicate(r_x, color=TURN, scale_factor=1.06), Indicate(r_y, color=TURN, scale_factor=1.06),
                      run_time=0.8)
            docs.heal(self)
            vo.wait_until("and you can try a call")
            self.play(Indicate(btn, color=TURN, scale_factor=1.12), run_time=0.7)
            docs.heal(self)
        assert docs.get_bottom()[1] > -3.55 and tags8.get_top()[1] < 2.8, (docs.get_bottom(), tags8.get_top())

        # ========================================================== 9. type hints → validation + docs
        # keep only the signature and the 422 chip of V4 (they come back at the top left)
        for m in (u.url, u.body, u.res, u.captions):
            if m is not None:
                u._detach(m)
        for m in list(u.marks.submobjects):
            if m is not e422:
                u.marks.remove(m)
        u.shift(np.array([-6.45 - u.sig.get_left()[0], 2.35 - u.sig.get_y(), 0]))
        e422.next_to(u.sig, DOWN, buff=0.75).align_to(u.sig, LEFT).shift(RIGHT * 0.3)
        cap = label("type hints → validation + docs", 22, OWN)
        cap.move_to([-6.45 + cap.width / 2, -2.4, 0])
        turn9 = your_turn().next_to(btn, UP, buff=0.12).align_to(btn, RIGHT)
        h1 = u.hint(1)
        th0 = Line(u.hint(0).get_bottom() + DOWN * 0.05, e422.get_top() + UP * 0.03, color=OWN, stroke_width=3)
        th1 = Line(h1.get_bottom() + DOWN * 0.05, [h1.get_x(), docs.frame.get_top()[1] + 0.03, 0], color=OWN,
                   stroke_width=3)
        assert u.sig.get_right()[0] < 6.5 and u.sig.get_bottom()[1] > tags8.get_top()[1] + 0.05, u.sig.get_bottom()
        assert cap.get_right()[0] < docs.get_left()[0] - 0.1, (cap.get_right(), docs.get_left())
        assert turn9.get_top()[1] < docs.bar[0].get_y() - 0.05 and turn9.get_left()[0] > r_get.get_right()[0] + 0.2, \
            (turn9.get_top(), docs.bar[0].get_y())
        assert not (tags8.get_left()[0] < h1.get_x() < tags8.get_right()[0]), (tags8.get_left(), h1.get_x())
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeIn(u.sig, shift=DOWN * 0.15), FadeIn(e422, shift=DOWN * 0.15), run_time=0.6)
            self.add(u)
            vo.wait_until("The type hints became")
            self.play(*[Indicate(u.hint(i), color=TURN, scale_factor=1.15) for i in (0, 1)], run_time=0.6)
            self.play(Create(th0), Create(th1), run_time=0.7)
            vo.wait_until("the validation")
            self.play(Indicate(e422.text, color=ERR, scale_factor=1.1), run_time=0.5)
            vo.wait_until("and the documentation")
            self.play(Indicate(params, color=OWN, scale_factor=1.05), FadeIn(cap, shift=UP * 0.1), run_time=0.7)
            u.heal(self)
            docs.heal(self)
            vo.wait_until("Pause and try one call")
            self.play(FadeIn(turn9, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, turn9, TURN)

        self.play(FadeOut(VGroup(u, docs, tags8, cap, turn9, th0, th1)), FadeOut(trk), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
