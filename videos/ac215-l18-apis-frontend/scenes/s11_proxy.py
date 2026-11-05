"""S11 · One origin: the Vite proxy (AC215 L18, part 2). Tracker [R] "README › Tutorial: React Frontend
Setup" 4 → 4 · extra → 5 → 6 → 7. Lecture: 18 · 24–26 (Frontend), beat 0 only.

Beats (script.md "## S11", one voiceover block each):
0. Tracker [R] 4, lecture_ref 24–26 (Frontend). V1 RequestTrace (localhost:3000; frontend-react with
   the "?" courier, API, vector-db, the GREEN cable; illustration tag): the lecture's picture, the
   page's JavaScript fires a PINK arrow at the API's door. On "Here, every call in api dot js" the trace
   goes and CODE(src/lib/api.js: 33–44) comes in (line 35 cut after the timeout): line 44 `fetch(path,
   options)` YELLOW with a PINK chip "path = /api/… · relative"; line 34 X-Session-ID PINK on "with
   the session ID"; on "from local storage" the panel gives way to CODE(api.js: 17–24), localStorage
   YELLOW.
1. Lecture off. CODE(vite.config.js: 5–15) (comments cut, line 13's API_URL fallback elided):
   `host: true` and `5173` PINK as it lands; line 13 YELLOW on "holds the courier", `'/api'` and the
   container URL PINK on their words. On "by container name" the panel goes, V1 returns and the "?"
   in the frontend box flips to a PURPLE "Vite".
2. V1 + V5: arrows 1–3 to door 3000; door 9000 dims with the GREY note "for /api/docs and curl"; the
   network's phone book (vector-db → 172.19.0.2, api-service) appears; on "carries each slash api
   request" the API entry lights and hop 3½ (the Vite courier) walks the cable; hops 4 and 5 (back
   through 3000). The note and book go; a 4-row `second tab` strip (extra) types d04's line 1 →
   d04:2, 5, `server: uvicorn` YELLOW.
3. The strip goes. Two PINK arrows, "the page" and "/api/… calls", both land on door 3000; a PINK
   "http://localhost:3000" under the browser splits into "http" · "localhost" · "3000" (lit on
   their words); both arrows pulse with it; an ORANGE-outlined chip "same-origin policy · the
   browser's rule" stays quiet beside it; a permission-slip glyph appears right of the API box,
   struck GREY, "not needed"; a GREEN card quotes docs/contract.md:6–7 (cut, not spoken).
4. Everything but V1 goes; the browser holds an envelope addressed http://cheese-app-api-service:9000.
   PONDER (8 s) under the laptop.
5. The card leaves. The envelope travels to the GREY desk "your laptop's DNS" under the browser: RED
   "not found". The phone book returns under the laptop with a GREY dashed chip "nginx · the next
   scene" above it; on "the Vite proxy" the courier and the
   API entry light, on "nginx" the nginx chip, on "the API"
   the API box.
6. Tracker [R] 4 · extra. The API is unplugged from the cable; the courier turns back with a RED 502
   and an empty envelope; the API plugs back in. V1 goes: a 5-row `second tab` (extra) types d09
   (folds) → d09:3 RED; above it the Vite terminal (`laptop · new terminal`) shows d02:85–86 with
   ENOTFOUND cheese-app-api-service RED; on "the README's troubleshooting row" RECORDED(04: 13),
   tag recorded · README:232.
7. Tracker [R] 5. V1 again (illustration): Home, then /podcasts and /newsletters, each with the
   courier carrying its /api/… envelope; then /chat with a "Recent" list (text-free rows) that survives
   a GREY reload sweep. V1 goes: a browser at localhost:3000/chat with the three mode chips over a
   7-row `second tab` (extra): Identify → d07 (folds) → d07:3 GREEN; Ask → d06 → d06:2–3 RED with the
   GOLD cost tag; Cheese books with "How is Tolminc cheese made?" → b40 → b40:2–3 RED. ▶ your turn.
8. Tracker [R] 6. A README card (README.md · lines 177–185, the separator row dropped); ticks lay onto
   the three files seen (vite.config.js, src/main.jsx, src/lib/api.js); ▶ your turn; it holds ~4 s.
   Tracker [R] 7. A 10-row `laptop · new terminal` at …/src/frontend-react$ types ./docker-shell.sh →
   d12:2 (wrap); at d12:3's container prompt `npm run check` → d12:6 (YELLOW), 9, 11, 24–25 (cut after
   the size), 27; line 25's dist/assets/index-….js GREEN. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S11"]

# ------------------------------------------------------------------ the real sources (checked)
FR = f"{V2}/src/frontend-react"
API_JS = f"{FR}/src/lib/api.js"
VITE = f"{FR}/vite.config.js"
CONTRACT = f"{V2}/docs/contract.md"

D02 = capture("d02")
D04 = capture("d04")
D06 = capture("d06")
D07 = capture("d07")
D09 = capture("d09")
D12 = capture("d12")
B40 = capture("b40")

assert excerpt(API_JS, 34, 34).strip() == "headers: { 'X-Session-ID': sessionId() },"
assert excerpt(API_JS, 44, 44).strip() == "response = await fetch(path, options)"
assert "AbortSignal.timeout(130_000)," in excerpt(API_JS, 35, 35)
assert excerpt(API_JS, 17, 17).strip() == "function sessionId() {"
assert "localStorage.getItem(SESSION_KEY)" in excerpt(API_JS, 19, 19)
assert "localStorage.setItem(SESSION_KEY, id)" in excerpt(API_JS, 22, 22)
assert excerpt(VITE, 10, 10).strip().startswith("host: true,")
assert excerpt(VITE, 11, 11).strip() == "port: 5173,"
assert excerpt(VITE, 13, 13).strip() == "proxy: { '/api': process.env.API_URL || 'http://cheese-app-api-service:9000' },"
C6, C7 = excerpt(CONTRACT, 6, 6), excerpt(CONTRACT, 7, 7)
CONTRACT_ROWS = ("The browser calls relative /api/... paths on its own origin. …",
                 "… so nothing strips a prefix and the API needs no CORS.")
assert md_plain(C6).startswith(CONTRACT_ROWS[0][:-2]), C6
assert md_plain(C7).endswith(CONTRACT_ROWS[1][2:]), C7

assert D04.line(2) == "HTTP/1.1 200 OK" and D04.line(5) == "server: uvicorn", D04.lines
assert D09.cmd.startswith("docker network disconnect cheese-app-network cheese-app-api-service; curl"), D09.cmd
assert D09.line(3) == "[HTTP 502]", D09.lines
assert D02.line(85).endswith("[vite] http proxy error: /api/newsletters?limit=2"), D02.line(85)
assert D02.line(86) == "Error: getaddrinfo ENOTFOUND cheese-app-api-service", D02.line(86)
assert "localhost:3000/api/llm-cnn/chats" in D07.cmd and D07.line(3) == "[HTTP 200]"
assert "localhost:3000/api/llm/chats" in D06.cmd and D06.at((2, 3)) == ["Internal Server Error", "[HTTP 500]"]
assert "How is Tolminc cheese made?" in B40.cmd and B40.at((2, 3)) == ["Internal Server Error", "[HTTP 500]"]
assert D12.cmd == "./docker-shell.sh"
assert D12.line(2) == "Container 'cheese-app-frontend-react' is already running. Shelling into it..."
assert at_prompt(D12, 3)[1] == "npm run check"
assert D12.line(6) == "> eslint . && prettier --check . && vite build"
assert D12.line(9) == "All matched files use Prettier code style!"
assert D12.line(11) == "✓ 2385 modules transformed."
assert D12.line(24).startswith("dist/assets/index-") and D12.line(24).split()[0].endswith(".css")
assert D12.line(25).startswith("dist/assets/index-") and D12.line(25).split()[0].endswith(".js")
assert D12.line(27) == "✓ built in 470ms"
JS_FILE = D12.line(25).split()[0]

TROUBLE = recorded("04-troubleshooting", 13)
assert TROUBLE[0].startswith("Pages load with no content"), TROUBLE

# README "Review the code" table (177–185) without its separator row (178)
TABLE = [md_plain(s) for s in excerpt(f"{V2}/README.md", 177, 185).split("\n")]
assert TABLE[1].startswith("---"), TABLE[1]
TABLE = [TABLE[0]] + TABLE[2:]
SEEN = ("vite.config.js", "src/main.jsx", "src/lib/api.js")
for _f in SEEN:
    assert any(r.startswith(_f + " ·") for r in TABLE), _f
assert "How is Tolminc cheese made?" in readme(172)

QUESTION = "Could the page's JavaScript call\nhttp://cheese-app-api-service:9000\ndirectly?"
BOOK_AT = (3.53, -2.75)          # the phone book under the laptop, right (5.9 wide)
SHIFT_UP = 0.85                     # V1 over a 4-row 20 pt strip: y -1.15 .. 2.85 (beside the tracker)


# ------------------------------------------------------------------ local helpers
def envelope2(rows, color=ROUTE, size: float = 20) -> VGroup:
    """An envelope with two mono rows (a long address). .body .flap .text"""
    t = VGroup(*[mono(r, size, INK) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
    w, h = t.width + 0.5, t.height + 0.55
    body = Rectangle(width=w, height=h, stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)
    flap = VMobject(stroke_color=color, stroke_width=2.5).set_points_as_corners(
        [body.get_corner(UL), body.get_center() + UP * (h / 2 - 0.2), body.get_corner(UR)])
    t.move_to(body).shift(DOWN * 0.1)
    g = VGroup(body, flap, t)
    g.body, g.flap, g.text = body, flap, t
    return g


def bar_tag(scene, t: Terminal, tg):
    """PLAYS: a row-sized tag on the terminal's title bar."""
    on_bar(t, tg)
    scene.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    t.add(tg)
    return tg


def strip_at(rows: int, title: str, prompt: str = P_LAPTOP, size: float = 20, bottom: float = BOTTOM):
    t = term(prompt, rows=rows, title=title, size=size)
    t.shift(UP * (bottom - t.box.get_bottom()[1]))
    return t


class OneOrigin(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S11"] == 9, len(SAY)

        trk = tracker_r(4)
        tr = RequestTrace("localhost:3000", rows=("front", "api", "vdb"), front="react", courier="?",
                          caption=False, browser_w=4.1).shift(UP * SHIFT_UP)
        net = tr.net
        ill = illustration_tag().next_to(tr.browser, DOWN, buff=0.1).align_to(tr.browser, LEFT)
        assert tr.get_top()[1] <= 2.86, tr.get_top()
        assert net.frame.get_left()[0] > trk.get_right()[0], (net.frame.get_left(), trk.get_right())

        # ========================================================== 0. the lecture's picture; api.js
        ref = lref("24–26 (Frontend)")
        pa = code(API_JS, 33, 44, font_size=20, dedent=True, shown="frontend-react/src/lib/api.js",
                  cuts={35: "130_000),"})
        pa.align_to([-6.5, 0, 0], LEFT).align_to([0, PIC_TOP - 0.02, 0], UP)
        assert pa.get_bottom()[1] > -SAFE_Y, pa.get_bottom()
        rel = route_chip("path = /api/… · relative", mono_font=False)
        pb = code(API_JS, 17, 24, font_size=20, dedent=True, shown="frontend-react/src/lib/api.js")
        pb.align_to([-6.5, 0, 0], LEFT).align_to([0, PIC_TOP - 0.02, 0], UP)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(tr), FadeIn(ill), run_time=0.8)
            vo.wait_until("In the lecture")
            self.play(Indicate(ref, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("the page's JavaScript calls the API")
            tr.page_call(self, "api", run_time=0.8)
            self.play(net.door_pulse("api", ROUTE), Indicate(net.inner["api"], color=TURN), run_time=0.7)
            net.heal(self)
            vo.wait_until("Here, every call")
            tr.clear_hops(self, run_time=0.3)
            self.play(FadeOut(tr), FadeOut(ill), run_time=0.5)
            self.play(FadeIn(pa, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("goes to a relative path")
            b44 = line_bar(pa.code, 11, TURN)
            self.play(FadeIn(b44), code_span(pa.code, 11, "fetch(path, options)").animate.set_color(TURN),
                      run_time=0.5)
            self.add(pa, b44)
            rel.next_to(pa, DOWN, buff=0.15).align_to(code_span(pa.code, 11, "fetch(path"), LEFT)
            assert rel.get_bottom()[1] > -SAFE_Y and rel.get_right()[0] < SAFE_X, rel.get_bottom()
            self.play(FadeIn(rel, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("with the session ID")
            b34 = line_bar(pa.code, 1, ROUTE)
            self.play(FadeIn(b34), code_span(pa.code, 1, "'X-Session-ID'").animate.set_color(ROUTE),
                      run_time=0.5)
            self.add(pa, b44, b34)
            vo.wait_until("from local storage")
            self.play(FadeOut(VGroup(pa, b44, b34, rel)), FadeIn(pb, shift=UP * 0.15), run_time=0.6)
            ls = VGroup(*[code_span(pb.code, k, "localStorage") for k in (2, 5)])
            self.play(ls.animate.set_color(TURN), run_time=0.4)
            self.add(pb)
            self.play(Indicate(ls, color=TURN, scale_factor=1.12), run_time=0.7)
            self.add(pb)

        # ========================================================== 1. vite.config.js: the courier
        pv = code(VITE, 5, 15, font_size=20, shown="frontend-react/vite.config.js",
                  cuts={5: "// The browser always calls /api/... on its own origin.",
                        6: "// container by name, on cheese-app-network;", 10: "host: true,"},
                  elide={13: "process.env.API_URL || "})
        pv.align_to([-6.5, 0, 0], LEFT).align_to([0, PIC_TOP - 0.02, 0], UP)
        assert pv.get_bottom()[1] > -SAFE_Y and pv.get_right()[0] < SAFE_X, (pv.get_bottom(), pv.get_right())
        with self.voiceover(SAY[1]) as vo:
            code_span(pv.code, 5, "host: true").set_color(ROUTE)
            code_span(pv.code, 6, "5173").set_color(ROUTE)
            self.play(FadeOut(ref), FadeOut(pb), FadeIn(pv, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("holds the courier")
            b13 = line_bar(pv.code, 8, TURN)
            self.play(FadeIn(b13), run_time=0.4)
            self.add(pv, b13)
            vo.wait_until("a proxy rule")
            self.play(Indicate(code_span(pv.code, 8, "proxy"), color=TURN, scale_factor=1.2), run_time=0.6)
            self.add(pv, b13)
            vo.wait_until("forwards slash api")
            self.play(code_span(pv.code, 8, "'/api'").animate.set_color(ROUTE).scale(1.15), run_time=0.3)
            self.play(code_span(pv.code, 8, "'/api'").animate.scale(1 / 1.15), run_time=0.3)
            self.add(pv, b13)
            vo.wait_until("to cheese app API service")
            url = code_span(pv.code, 8, "'http://cheese-app-api-service:9000'")
            self.play(url.animate.set_color(ROUTE), run_time=0.4)
            self.play(Indicate(url, color=ROUTE, scale_factor=1.06), run_time=0.6)
            self.add(pv, b13)
            vo.wait_until("by container name")
            self.play(FadeOut(VGroup(pv, b13)), run_time=0.4)
            self.play(FadeIn(tr), FadeIn(ill), run_time=0.5)
            net.set_courier(self, "Vite", run_time=0.5)
            self.play(Indicate(net.courier, color=TOOL, scale_factor=1.25), run_time=0.6)
            net.heal(self)

        # ========================================================== 2. every arrow lands on 3000
        tS = strip_at(4, T_TAB, bottom=-3.56)
        assert tS.box.get_top()[1] < net.frame.get_bottom()[1] - 0.05, (tS.box.get_top(), net.frame.get_bottom())
        with self.voiceover(SAY[2]) as vo:
            tr.hop(self, 1, "front", run_time=0.5)
            tr.hop(self, 2, "front", run_time=0.4)
            tr.hop(self, 3, "front", run_time=0.4)
            vo.wait_until("localhost 3000")
            self.play(net.door_pulse("front", TURN), run_time=0.6)
            net.heal(self)
            net.dim_door(self, "api", None, run_time=0.4)
            dc = grey_chip("9000 · for /api/docs and curl").next_to(net.frame, DOWN, buff=0.15).align_to(net.frame, LEFT)
            self.play(FadeIn(dc, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Vite, in the frontend container")
            bk = net.phone_book(self, ((C_VDB, VDB_IP), (C_API, None)), at=BOOK_AT, run_time=0.5)
            assert bk.get_top()[1] < net.frame.get_bottom()[1] - 0.05 and bk.get_right()[0] < SAFE_X
            assert dc.get_right()[0] < bk.get_left()[0] - 0.1 or dc.get_bottom()[1] > bk.get_top()[1] + 0.1, \
                (dc.get_bottom(), bk.get_top())
            vo.wait_until("carries each slash api request")
            self.play(net.book_light(1), run_time=0.5)
            net.heal(self)
            tr.hop(self, 3.5, run_time=0.7)
            vo.wait_until("That is why uvicorn answered")
            tr.hop(self, 4, "api", run_time=0.5)
            tr.hop(self, 5, "api", run_time=0.5)
            net.drop(self, bk, run_time=0.3, extra=[FadeOut(dc)])
            net.book = None
            self.play(FadeIn(tS, shift=UP * 0.2), run_time=0.4)
            tagS = bar_tag(self, tS, extra_row())
            type_capture(self, tS, D04, type_time=0.5)
            o2 = out(self, tS, D04.at(2, 5), run_time=0.4)
            srv = o2[1]
            assert srv.text == "server: uvicorn"
            self.play(srv.animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(srv, color=TURN, scale_factor=1.08), net.boxes["api"].animate(
                rate_func=there_and_back).set_stroke(TURN, width=6), run_time=0.7)
            self.add(tS)
            net.heal(self)

        # ========================================================== 3. one origin
        url0 = mono("http://localhost:3000", 22, ROUTE)
        oc = origin_chips("http", "localhost", "3000")
        oc.move_to([0, -1.5, 0]).align_to([-6.5, 0, 0], LEFT)
        url0.move_to(oc)
        sop = grey_chip("same-origin policy · the browser's rule", color=SHARED)
        sop.next_to(oc, RIGHT, buff=0.45)
        assert sop.get_right()[0] < SAFE_X, sop.get_right()
        api_y = net.row_y("api")
        sg = slip_glyph(0.5).move_to([(net.frame.get_right()[0] + SAFE_X) / 2, api_y + 0.25, 0])
        sg_x = Line(sg.get_corner(UL) + np.array([-0.08, 0.08, 0]), sg.get_corner(DR) + np.array([0.08, -0.08, 0]),
                    color=S.GREY, stroke_width=5)
        nn = VGroup(label("not", 20, S.GREY), label("needed", 20, S.GREY)).arrange(DOWN, buff=0.06)
        nn.next_to(sg, DOWN, buff=0.14)
        assert nn.get_left()[0] > net.frame.get_right()[0] + 0.04 and nn.get_right()[0] < SAFE_X, nn.get_left()
        cc = card(list(CONTRACT_ROWS), OWN, size=20, head="docs/contract.md · lines 6–7")
        cc.align_to([-6.5, 0, 0], LEFT).align_to([0, -3.56, 0], DOWN)
        assert cc.get_top()[1] < oc.get_bottom()[1] - 0.08, (cc.get_top(), oc.get_bottom())
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(tS), run_time=0.4)
            tr.clear_hops(self, run_time=0.3)
            door3 = net.door_point("front") + LEFT * 0.03
            t_page = label("the page", 20, ROUTE).move_to(tr.browser.at(-0.35, 0.3))
            t_api = mono("/api/… calls", 20, ROUTE).move_to(tr.browser.at(-0.25, -0.45))
            a_page = Arrow(t_page.get_right() + RIGHT * 0.05, door3, buff=0.06, color=ROUTE, stroke_width=4,
                           tip_length=0.18)
            a_api = Arrow(t_api.get_right() + RIGHT * 0.05, door3, buff=0.06, color=ROUTE, stroke_width=4,
                          tip_length=0.18)
            self.play(FadeIn(t_page), GrowArrow(a_page), run_time=0.6)
            vo.wait_until("An origin is")
            self.play(FadeIn(url0, shift=UP * 0.1), run_time=0.4)
            self.play(ReplacementTransform(url0, oc), run_time=0.6)
            for i, cue in enumerate(("the scheme", "the host", "and the port")):
                vo.wait_until(cue)
                self.play(Indicate(oc.parts[i], color=TURN, scale_factor=1.15), run_time=0.45)
            vo.wait_until("The page and its API calls")
            self.play(FadeIn(t_api), GrowArrow(a_api), run_time=0.6)
            vo.wait_until("share one origin")
            self.play(a_page.animate(rate_func=there_and_back).set_color(TURN),
                      a_api.animate(rate_func=there_and_back).set_color(TURN),
                      Indicate(oc, color=ROUTE, scale_factor=1.08), net.door_pulse("front", ROUTE), run_time=0.9)
            tr.heal(self)
            self.add(a_page, a_api, t_page, t_api)        # above the (opaque) browser again
            vo.wait_until("so the browser has nothing to object to")
            self.play(FadeIn(sop, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and the API needs no permission slip")
            self.play(FadeIn(sg, scale=0.8), run_time=0.4)
            self.play(Create(sg_x), FadeIn(nn), run_time=0.5)
            self.play(FadeIn(cc, shift=UP * 0.15), run_time=0.6)

        # ========================================================== 4. PONDER: call the name directly?
        ev = envelope2(("http://cheese-app-", "api-service:9000"))
        ev.move_to(tr.browser.at(0, -0.05))
        assert ev.width < tr.browser.page.width - 0.1, ev.width
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(oc, sop, sg, sg_x, nn, cc, t_page, t_api, a_page, a_api)), run_time=0.5)
            vo.wait_until("Could the page's JavaScript")
            self.play(FadeIn(ev, shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(ev.text, color=ROUTE, scale_factor=1.06), run_time=0.6)
        pc = ponder(self, QUESTION, 8, center=(net.frame.get_x(), net.frame.get_y()), width=7.7)
        assert pc.get_left()[0] > tr.divider.get_x() + 0.05 and pc.get_right()[0] < SAFE_X, pc.get_left()

        # ========================================================== 5. no: the laptop's DNS has no page for it
        desk = card(["your laptop's DNS"], S.GREY, size=20)
        desk.align_to([-6.5, 0, 0], LEFT).align_to([0, -3.55, 0], DOWN)
        nf = err_chip("not found", mono_font=False).next_to(desk, RIGHT, buff=0.15)
        ngx = dashed_chip("nginx · the next scene")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pc), run_time=0.5)
            vo.wait_until("The JavaScript runs in your browser")
            self.play(Indicate(tr.browser.frame, color=TURN, scale_factor=1.03), run_time=0.6)
            tr.heal(self)
            self.add(ev)
            vo.wait_until("and the laptop's DNS")
            self.play(FadeIn(desk, shift=UP * 0.1), run_time=0.4)
            self.play(ev.animate.next_to(desk, UP, buff=0.12).align_to(desk, LEFT), run_time=0.8)
            assert ev.get_top()[1] < ill.get_bottom()[1] - 0.05, ev.get_top()
            vo.wait_until("knows no container names")
            self.play(FadeIn(nf, scale=1.2), ev.animate.set_opacity(0.4), run_time=0.5)
            vo.wait_until("Only code inside the network")
            bk = net.phone_book(self, ((C_VDB, VDB_IP), (C_API, None)), at=BOOK_AT, run_time=0.5)
            ngx.move_to([0, (net.frame.get_bottom()[1] + bk.get_top()[1]) / 2, 0]).align_to(bk, LEFT)
            assert ngx.get_top()[1] < net.frame.get_bottom()[1] - 0.05 and ngx.get_bottom()[1] > bk.get_top()[1] + 0.05
            assert ngx.get_left()[0] > nf.get_right()[0] + 0.2, (ngx.get_left(), nf.get_right())
            self.play(FadeIn(ngx, shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("the Vite proxy")
            self.play(Indicate(net.courier, color=TOOL, scale_factor=1.3), net.book_light(1), run_time=0.7)
            net.heal(self)
            vo.wait_until("nginx")
            self.play(Indicate(ngx, color=INK, scale_factor=1.1), net.book_light(1), run_time=0.6)
            net.heal(self)
            vo.wait_until("the API")
            self.play(net.boxes["api"].animate(rate_func=there_and_back).set_stroke(TURN, width=6),
                      net.book_light(0), run_time=0.7)
            net.heal(self)

        # ========================================================== 6. extra: unplug the API → 502
        tT = strip_at(5, T_TAB)
        tV = strip_at(2, T_NEW, prompt=P_V2_REACT, bottom=tT.box.get_top()[1] + 0.12)
        rc = quote_card("04-troubleshooting", 13, "recorded", "README:232", size=20, width_chars=100)
        rc.align_to([-6.5, 0, 0], LEFT).next_to(tV.box, UP, buff=0.3)
        rc.align_to([-6.5, 0, 0], LEFT)
        assert rc.get_top()[1] < PIC_TOP and rc.get_right()[0] < SAFE_X, (rc.get_top(), rc.get_right())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(desk, nf, ev, ngx)), track(trk, 4, extra=True), run_time=0.5)
            net.drop(self, bk, run_time=0.3)
            net.book = None
            vo.wait_until("unplug the API")
            net.unplug(self, "api", run_time=0.5)
            self.play(net.light("api", ERR), run_time=0.3)
            net.heal(self)
            vo.wait_until("for one request")
            net.courier_walk(self, fail="502", run_time=1.2)
            net.plug(self, "api", run_time=0.4)
            self.play(net.light("api", CONTAINER), run_time=0.3)
            net.heal(self)
            vo.wait_until("The browser gets 502")
            self.play(FadeOut(tr), FadeOut(ill), run_time=0.4)
            self.play(FadeIn(tT, shift=UP * 0.2), FadeIn(tV, shift=UP * 0.2), run_time=0.4)
            bar_tag(self, tT, extra_row())
            type_capture(self, tT, D09, type_time=0.3)
            o6 = out(self, tT, [(D09.line(3), ERR)], run_time=0.3)
            self.play(Indicate(o6[0], color=ERR, scale_factor=1.15), run_time=0.5)
            self.add(tT)
            ov = out(self, tV, D02.at(85, 86), run_time=0.4)
            self.play(substring(ov[1], "ENOTFOUND cheese-app-api-service").animate.set_color(ERR), run_time=0.4)
            self.add(tV)
            vo.wait_until("the README's troubleshooting row")
            self.play(FadeIn(rc, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(rc.body, color=INK, scale_factor=1.04), run_time=0.7)
            self.add(rc)

        # ========================================================== 7. review the app
        recent = VGroup(label("Recent", 20, INK),
                        *[RoundedRectangle(width=w, height=0.18, corner_radius=0.09, stroke_width=0)
                          .set_fill(S.GREY_DARK, 1) for w in (2.6, 2.1)]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        tC = strip_at(7, T_TAB)
        bc = Browser("localhost:3000/chat", win_w=6.2, win_h=2.7)
        bc.move_to([-6.5 + 3.1, 0, 0]).align_to([0, PIC_TOP - 0.05, 0], UP)
        assert bc.frame.get_bottom()[1] > tC.box.get_top()[1] + 0.1, (bc.frame.get_bottom(), tC.box.get_top())
        illc = illustration_tag().next_to(bc.frame, RIGHT, buff=0.2).align_to(bc.frame, UP)
        modes = VGroup(*[chip(m, S.GREY, size=20) for m in ("Ask", "Identify", "Cheese books")]).arrange(RIGHT, buff=0.2)
        qrow = grey_chip("How is Tolminc cheese made?")
        cost = cost_tag("Gemini · with your key: billed")
        turn = your_turn()
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(tT, tV, rc)), track(trk, 5), run_time=0.5)
            self.play(FadeIn(tr), FadeIn(ill), run_time=0.5)
            tr.browser.fill(self, ["Home"], run_time=0.3)
            vo.wait_until("home, podcasts")
            self.play(tr.browser.flash(ROUTE), run_time=0.4)
            tr.heal(self)
            call7 = tr.page_call(self, "front", run_time=0.4)
            for path in ("podcasts", "newsletters"):
                if path == "newsletters":
                    vo.wait_until("and newsletters")
                tr.browser.goto(self, f"localhost:3000/{path}", run_time=0.3)
                tr.browser.fill(self, [path.capitalize()], run_time=0.3)
                net.courier_walk(self, text=f"/api/{path}", run_time=0.8)
            vo.wait_until("and the Recent tab")
            tr.browser.goto(self, "localhost:3000/chat", run_time=0.3)
            tr.browser.fill(self, list(recent), run_time=0.4)
            vo.wait_until("across a reload")
            tr.browser.reload(self, run_time=0.7)
            self.play(Indicate(tr.browser.rows, color=OWN, scale_factor=1.06), run_time=0.6)
            tr.heal(self)
            del call7
            vo.wait_until("In chat, Identify")
            self.play(FadeOut(tr), FadeOut(ill), run_time=0.4)
            self.play(FadeIn(bc), FadeIn(illc), FadeIn(tC, shift=UP * 0.2), run_time=0.5)
            bc.fill(self, [modes], run_time=0.3)
            bar_tag(self, tC, extra_row())
            self.play(modes[1].animate.set_color(TURN), run_time=0.3)
            type_capture(self, tC, D07, type_time=0.2)
            o7 = out(self, tC, [(D07.line(3), OWN)], run_time=0.3)
            self.play(Indicate(o7[0], color=OWN), modes[1].box.animate.set_stroke(OWN), run_time=0.5)
            self.add(tC)
            bc.heal(self)
            vo.wait_until("Ask, and Cheese books")
            cost.next_to(bc.frame, RIGHT, buff=0.2).align_to(bc.frame, DOWN).shift(UP * 0.1)
            assert cost.get_right()[0] < SAFE_X, cost.get_right()
            self.play(modes[0].box.animate.set_stroke(TURN), FadeIn(cost, shift=LEFT * 0.1), run_time=0.4)
            bc.heal(self)
            type_capture(self, tC, D06, type_time=0.2)
            out(self, tC, [(s, ERR) for s in D06.at((2, 3))], run_time=0.3)
            self.play(modes[0].box.animate.set_stroke(ERR), run_time=0.3)
            bc.heal(self)
            qrow.next_to(modes, DOWN, buff=0.25).align_to(modes, LEFT)
            self.play(modes[2].box.animate.set_stroke(TURN), run_time=0.3)
            bc.show(self, qrow, run_time=0.4, into=bc.rows)
            bc.heal(self)
            type_capture(self, tC, B40, type_time=0.2)
            out(self, tC, [(s, ERR) for s in B40.at((2, 3))], run_time=0.3)
            self.play(modes[2].box.animate.set_stroke(ERR), run_time=0.3)
            bc.heal(self)
            vo.wait_until("Pause and click through")
            turn.next_to(bc.frame, RIGHT, buff=0.2).align_to(bc.frame, UP).shift(DOWN * 0.6)
            self.play(FadeIn(turn, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, turn, TURN)

        # ========================================================== 8. the code table; npm run check
        body = "\n".join(TABLE)
        rcard = readme_card((177, 185), body, size=20)
        rcard.move_to([0, 0.1, 0])
        assert rcard.get_top()[1] < PIC_TOP and rcard.width < 2 * SAFE_X, (rcard.get_top(), rcard.width)
        rows = rcard.body
        t8 = term(P_V2_REACT, rows=10, title=T_NEW, size=20)      # 20 pt: the prompt + ./docker-shell.sh fit one row
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(bc, illc, tC, cost, turn, qrow)), track(trk, 6), run_time=0.6)
            self.play(FadeIn(rcard, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("names the files we just saw")
            ticks = VGroup()
            for f in SEEN:
                r = rows[[i for i, x in enumerate(TABLE) if x.startswith(f + " ·")][0]]
                tk = check_glyph(0.26).next_to(r, RIGHT, buff=0.2)
                ticks.add(tk)
            self.play(LaggedStart(*[FadeIn(tk, scale=1.4) for tk in ticks], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("pause to match each one")
            t2 = your_turn().next_to(rcard.frame, UP, buff=0.1).align_to(rcard.frame, RIGHT)
            self.play(FadeIn(t2, shift=DOWN * 0.1), run_time=0.4)
            flash_tag(self, t2, TURN)
            vo.wait_until("Then, in a second terminal")
            self.play(FadeOut(VGroup(rcard, ticks, t2)), track(trk, 7), run_time=0.5)
            self.play(FadeIn(t8, shift=UP * 0.2), run_time=0.4)
            type_capture(self, t8, D12, type_time=0.4)
            out(self, t8, [D12.line(2)], wrap=True, run_time=0.3)
            vo.wait_until("npm run check")
            type_at(self, t8, D12, 3, type_time=0.4)
            o8 = out(self, t8, [D12.line(6)], run_time=0.3)
            vo.wait_until("a lint")
            self.play(o8[0].animate.set_color(TURN), run_time=0.3)
            self.play(Indicate(substring(o8[0], "eslint ."), color=TURN, scale_factor=1.2), run_time=0.5)
            self.add(t8)
            vo.wait_until("a format check")
            o9 = out(self, t8, [D12.line(9)], run_time=0.3)
            self.play(Indicate(substring(o8[0], "prettier --check ."), color=TURN, scale_factor=1.15), run_time=0.5)
            self.add(t8)
            vo.wait_until("and a production build")
            o11 = out(self, t8, [D12.line(11), cut(D12.line(24), "kB"), cut(D12.line(25), "kB"), D12.line(27)],
                      run_time=0.6)
            self.play(Indicate(substring(o8[0], "vite build"), color=TURN, scale_factor=1.15), run_time=0.5)
            self.add(t8)
            vo.wait_until("That build is what production serves")
            self.play(substring(o11[2], JS_FILE).animate.set_color(OWN), run_time=0.4)
            self.play(Indicate(o11[2], color=OWN, scale_factor=1.04), run_time=0.7)
            self.add(t8)
            del o9

        self.play(FadeOut(t8), FadeOut(trk), run_time=0.7)
        self.wait(0.3)
