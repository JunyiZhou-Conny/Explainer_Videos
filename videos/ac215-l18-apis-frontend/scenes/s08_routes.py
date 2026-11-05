"""S08 · Screens decide the routes (AC215 L18, part 1). Tracker [B] "README › Tutorial: Backend APIs"
4 → 9. Lecture: 18 · 29 (beat 0), 44 (beat 1), 30–33 (beat 2), 39–41 (beat 3), 41 (beat 8) (APIs).

Beats (script.md "## S08", one voiceover block each):
0. Tracker [B] 4, lecture_ref 29. Slide 29 redrawn: three GREY phone outlines "Newsletters" (a card),
   "Podcasts" (an episode with a play button), "Chat" (a photo and the bubble "What type of cheese is
   this?"). On "Each screen needs data" a PINK thread grows up from each phone to a data chip:
   "newsletters", "podcasts", "chat + photo"; on "each kind of data" the chips pulse.
1. lecture_ref 44. The phones go; the three chips become slide 44's six WHITE-outlined route groups
   (V4 RouteTree.groups, top row). CODE(api/service.py: 31–40) (the three `*_utils.respond`
   arguments elided with a GREY '…' so the panel fits): on "newsletters and podcasts" lines 36–37
   light, on "under slash api" their "/api" prefixes turn PINK. On "Then one function" the three
   `create_router` spans turn PURPLE; the panel gives way to V4: the PINK root /api, the branches
   newsletters and podcasts, then the PURPLE stamp "create_router" prints llm, llm-cnn, llm-rag (each
   with chats). WHITE "Ask", "Identify", "Cheese books" write on their words. On "The lecture shows six
   groups" five chips snap onto their branches and turn GREEN; "Agent Chat" stays GREY dashed and
   unattached, with the erratum tag "slide 44: six · this repo: five routers".
2. lecture_ref 30–33. The tree steps aside (fades; it returns in beat 3). One GREY dashed diagram:
   browser → API service → a bus with Newsletters, Podcasts, Image Model, Cheese KB. An agent box slides
   behind the API while an MCP box fades in (slide 30); on "with or without" the MCP box goes and the
   agent wires straight to the bus (slide 31), then the browser goes and the agent slides out front as
   the client (slide 32). On "This repository has none" a one-line GREY chip (slide 33): "REST API · for
   apps · FastAPI | MCP · for agents · FastMCP · not in this repo".
3. lecture_ref 39–41. The diagram goes, the tree returns. A GREY card "slide 39 · the idea" with the
   slide's one-file form @app.get("/newsletters") and the erratum tag; on "The repository puts" /api,
   its edge and newsletters light PINK in turn and the PINK label /api/newsletters writes on the row.
4. Lecture off. Tracker [B] 5. The groups, Agent Chat, label and card go; the tree fades. A README card
   (README.md · lines 106–112) with the demo route; the GREY chip "your editor"; on "and save" the
   card gives way to a `laptop · second tab` terminal (…/src/api-service) that types `git diff
   api/service.py` (bar tag extra) → b27:20–21, 24–29 (the blank context rows dropped), + lines GREEN.
   On "The server reloads by itself" the terminal goes; the tree returns over a 3-row uvicorn strip
   (`laptop`, the container prompt): b21:65 (YELLOW), 70–72 (72 GREEN), and the leaf square_root grows
   under /api.
5. The tree's '/' root with healthz and readyz appears; V6's readiness lamp (small, by readyz) drops to
   amber. The strip becomes the `second tab`: extra b30 → b30:2–3 (GREEN); the lamp turns GREEN.
6. Tracker [B] 6. The strip types b28 (extra) → b28:2; a GREY browser drawing (illustration) at
   localhost:9000/api/square_root shows the same number; then b29 → b29:2 `5.0` GREEN, the browser goes
   to ?x=3&y=4 and shows 5.0. ▶ your turn on the bar.
7. Tracker [B] 7. Browser and lamp go. The strip types b31 (extra) → b31:2–4, `/api/openapi.json`
   YELLOW. Tracker [B] 7 · extra: b32 (folds) → b32:2–27 scroll through the strip; on "the leaves of
   this tree" V4's 25 leaf dots fill the tree and the GREY counter "25 operations" writes.
8. Tracker [B] 8. Tree and strip go. A GREY browser drawing of localhost:9000/api/docs (illustration)
   with GET /api/newsletters, limit = 2 and an Execute button; ▶ your turn beside it. An 8-row
   `second tab` types b33 → b33:5–9, 15–19, 25–26 (the progress meter, lines 2–4, dropped); the two
   "title" lines YELLOW; on "newest first" the two "dts" lines flash. On "the lecture's example"
   lecture_ref 41 and a small GREY card "slide 41: a JSON list of newsletters". On "An unknown ID" b34
   (extra) → b34:2–3 RED.
9. Lecture off. Tracker [B] 9. A README card (README.md · lines 123–132: File and What it does, long
   descriptions cut with '…') gives way to the tree with V4's file map: service.py, settings.py, the
   routers on their branches, chat.py under the stamp, the three utils files on the three chat rows, and
   chat_utils.py GREEN "saves chats"; each lights on its phrase. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S08"]

# ------------------------------------------------------------------ the real sources (checked)
B21 = capture("b21")
B27 = capture("b27")
B28 = capture("b28")
B29 = capture("b29")
B30 = capture("b30")
B31 = capture("b31")
B32 = capture("b32")
B33 = capture("b33")
B34 = capture("b34")
assert B21.line(65) == "WARNING:  StatReload detected changes in 'api/service.py'. Reloading...", B21.line(65)
assert B21.at((70, 72)) == ["INFO:     Started server process [35]", "INFO:     Waiting for application startup.",
                            "INFO:     Application startup complete."], B21.at((70, 72))
assert B27.cmd_lines[-1] == "git diff api/service.py", B27.cmd_lines
assert B27.line(20).startswith("@@ -33,6 +33,12 @@ def get_status():"), B27.line(20)
assert B27.line(24) == '+@app.get("/api/square_root")' and B27.line(29) == "+", B27.at((24, 29))
assert not B27.line(22).strip() and not B27.line(23).strip()
assert B28.cmd == "curl -s http://localhost:9000/api/square_root; echo" and B28.line(2) == "2.23606797749979"
assert B29.cmd == "curl -s 'http://localhost:9000/api/square_root?x=3&y=4'; echo" and B29.line(2) == "5.0"
assert B30.cmd.startswith("curl -s -i http://localhost:9000/readyz") and B30.at(2, 3) == ["HTTP/1.1 200 OK", '{"ok":true}']
assert B31.line(2).strip() == "<title>Cheese App API - Swagger UI</title>" and B31.line(3).strip() == "url: '/api/openapi.json',"
assert B31.line(4) == "[HTTP 200]"
assert B32.line(2) == "{'title': 'Cheese App API', 'version': '0.1.0'}" and len(B32.at((3, 27))) == 25
assert B32.line(26).split() == ["GET", "/healthz"] and B32.line(27).split() == ["GET", "/readyz"]
assert B33.cmd.startswith("curl -X 'GET' 'http://localhost:9000/api/newsletters?limit=2'")
assert '"title": "Spanish Cheese Journey"' in B33.line(9) and '"title": "The Art of Blue Cheese"' in B33.line(19)
assert '"dts": 1730476705' in B33.line(8) and '"dts": 1729871905' in B33.line(18)
assert B33.line(26) == "]" and B33.line(5) == "["
assert B34.at(2, 3) == ['{"detail":"Newsletter not found"}', "[HTTP 404]"], B34.at(2, 3)

SERVICE = f"{V2}/src/api-service/api/service.py"
assert excerpt(SERVICE, 31, 31).strip() == '@app.get("/api/status")'
assert excerpt(SERVICE, 36, 36).strip() == 'app.include_router(newsletter.router, prefix="/api/newsletters")'
assert excerpt(SERVICE, 37, 37).strip() == 'app.include_router(podcast.router, prefix="/api/podcasts")'
assert all("create_router" in excerpt(SERVICE, n, n) for n in (38, 39, 40))
ELIDE = {38: ", llm_utils.respond", 39: ", llm_cnn_utils.respond", 40: ", llm_rag_utils.respond"}

R106 = md_plain(readme(106))
assert R106 == "Open api/service.py, add this after get_status, and save. api_server reloads by itself.", R106
R_CODE = [s.rstrip() for s in excerpt(f"{V2}/README.md", 108, 111).split("\n")]
assert R_CODE[0] == '@app.get("/api/square_root")' and R_CODE[2] == "    z = x**2 + y**2", R_CODE
assert excerpt(f"{V2}/README.md", 105, 105).strip() == "### Create a demo route"
assert excerpt(f"{V2}/README.md", 112, 112).strip() == "```"
assert [s[1:] for s in B27.at((24, 27))] == R_CODE, B27.at((24, 27))
TABLE = [md_plain(s) for s in excerpt(f"{V2}/README.md", 125, 132).split("\n")]
assert excerpt(f"{V2}/README.md", 123, 123).strip() == "| File | What it does |"
assert TABLE[0].startswith("api/service.py · ") and TABLE[-1].startswith("api/utils/chat_utils.py · "), TABLE

TREE_UP = UP * 0.75           # V4 over a 4-row 20 pt strip (strip top -1.18, stamp bottom ~ -1.08)


# ------------------------------------------------------------------ local helpers
class _Quiet:
    """A stand-in scene: builds a piece's state without playing anything."""
    mobjects: list = []

    def play(self, *a, **k):
        pass

    def add(self, *m):
        pass

    def remove(self, *m):
        pass


def bar_tag(scene, t: Terminal, tg, left: bool = False):
    """PLAYS: a row-sized tag on the terminal's title bar: right end (replacing the one there), or
    left=True just after the window dots (▶ your turn)."""
    if left:
        tg.move_to([t.dots.get_right()[0] + 0.3 + tg.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])
        scene.play(FadeIn(tg, shift=RIGHT * 0.1), run_time=0.4)
        t.add(tg)
        return tg
    old = getattr(t, "bar_tag", None)
    on_bar(t, tg)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    else:
        scene.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    t.add(tg)
    t.bar_tag = tg
    return tg


def unbar(t: Terminal) -> list:
    """The title-bar tag (if any) taken off the terminal: returns [FadeOut(tag)] to play (resize() moves
    the bar but not a tag riding on it)."""
    old = getattr(t, "bar_tag", None)
    if old is None:
        return []
    t.remove(old)
    t.bar_tag = None
    return [FadeOut(old)]


def clear_lines(scene, t: Terminal, run_time: float = 0.3):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    if not gone:
        return
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
    scene.remove(*gone)


def first_row(rows, sub):
    for r in rows:
        if sub in r.text:
            return r
    raise KeyError(sub)


def phone(title: str, kind: str, w: float = 2.3, h: float = 2.6) -> VGroup:
    """Slide 29's wireframe screen (GREY outline, title, a little content). kind: 'news' | 'pod' |
    'chat'. .frame .title"""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.18, stroke_color=LAPTOP, stroke_width=3)
    fr.set_fill(PANEL, 1)
    t = label(title, 20, INK).move_to(fr.get_top() + DOWN * 0.36)
    sep = Line(fr.get_left() + RIGHT * 0.15, fr.get_right() + LEFT * 0.15, color=S.GREY_DARK, stroke_width=2)
    sep.set_y(t.get_bottom()[1] - 0.14)
    body_c = fr.get_center() + DOWN * 0.3
    if kind in ("news", "pod"):
        cardr = RoundedRectangle(width=w - 0.5, height=1.2, corner_radius=0.1, stroke_color=S.GREY,
                                 stroke_width=2).move_to(body_c)
        bars = VGroup(*[Line(LEFT * (w - 0.9) / 2, RIGHT * (w - 0.9) / 2 * (1 - 0.35 * i), color=S.GREY_DARK,
                             stroke_width=6) for i in range(3)]).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        bars.move_to(cardr).align_to(cardr, LEFT).shift(RIGHT * 0.2)
        content = VGroup(cardr, bars)
        if kind == "pod":
            play_ = Triangle(color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.6).rotate(-PI / 2).scale(0.13)
            play_.move_to(cardr.get_corner(DR) + np.array([-0.3, 0.3, 0]))
            content.add(play_)
    else:
        photo = RoundedRectangle(width=0.8, height=0.5, corner_radius=0.06, stroke_color=S.GREY, stroke_width=2)
        wedge = Polygon([-0.25, -0.15, 0], [0.25, -0.15, 0], [0.12, 0.13, 0], color=S.GREY, stroke_width=2)
        wedge.set_fill(S.GREY, 0.4).move_to(photo)
        pic = VGroup(photo, wedge)
        q = VGroup(label("What type of", 20, INK), label("cheese is this?", 20, INK)).arrange(DOWN, buff=0.06)
        bub = RoundedRectangle(width=q.width + 0.24, height=q.height + 0.2, corner_radius=0.12,
                               stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        q.move_to(bub)
        content = VGroup(pic, VGroup(bub, q)).arrange(DOWN, buff=0.14, aligned_edge=RIGHT).move_to(body_c)
    g = VGroup(fr, t, sep, content)
    g.frame, g.title = fr, t
    return g


def agents_diagram() -> VGroup:
    """Slides 30–33 redrawn (GREY dashed). Parts in a dict .p: browser, api, bus, ends (four chips),
    links (bus stubs), b2a (browser → API), a2b (API → bus); agent / mcp are made by the scene."""
    p = {}
    p["browser"] = dashed_chip("browser").move_to([-5.0, 1.3, 0])
    p["api"] = dashed_chip("API service").move_to([-1.6, 1.3, 0])
    bus_x = 2.3
    ends = VGroup(*[dashed_chip(s) for s in ("Newsletters", "Podcasts", "Image Model", "Cheese KB")])
    for i, c in enumerate(ends):
        c.move_to([3.1 + c.width / 2, 2.0 - i * 0.75, 0])
    p["ends"] = ends
    p["bus"] = DashedLine([bus_x, 2.2, 0], [bus_x, -0.8, 0], color=S.GREY, stroke_width=3)
    p["links"] = VGroup(*[Line([bus_x, c.get_y(), 0], [c.get_left()[0], c.get_y(), 0], color=S.GREY,
                               stroke_width=2.5) for c in ends])
    p["b2a"] = arrow(p["browser"].get_right(), p["api"].get_left(), S.GREY, stroke=3)
    p["a2b"] = Line(p["api"].get_right(), [bus_x, 1.3, 0], color=S.GREY, stroke_width=2.5)
    g = VGroup(*p.values())
    g.p = p
    g.bus_x = bus_x
    return g


def readme_table() -> VGroup:
    """README 123–132 as the card shows it: GREY header row, then File (mono) · What it does (label,
    cut at a word boundary with the house '…')."""
    def short(s, n=34):
        if len(s) <= n:
            return s
        k = s.rfind(" ", 0, n)
        return s[:k].rstrip(",.:") + " …"
    hdr = [label("File", 20, S.GREY), label("What it does", 20, S.GREY)]
    rows = []
    for s in TABLE:
        f, what = s.split(" · ", 1)
        rows.append([mono(f, 20, INK), label(short(what), 20, INK)])
    allr = [hdr] + rows
    x1 = max(r[0].width for r in allr) + 0.5
    for i, r in enumerate(allr):
        y = -i * 0.46
        r[0].move_to([r[0].width / 2, y, 0])
        r[1].move_to([x1 + r[1].width / 2, y, 0])
    return VGroup(*[VGroup(*r) for r in allr])


class ScreensToRoutes(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S08"] == 10, len(SAY)
        quiet = _Quiet()

        # ========================================================== 0. slide 29: the screens need data
        trk = tracker_b(4)
        ref = lref("29 (APIs)")
        phones = VGroup(phone("Newsletters", "news"), phone("Podcasts", "pod"), phone("Chat", "chat"))
        for ph, x in zip(phones, (-4.0, 0.0, 4.0)):
            ph.move_to([x, -0.8, 0])
        datas = VGroup(*[route_chip(s) for s in ("newsletters", "podcasts", "chat + photo")])
        for d, ph in zip(datas, phones):
            d.move_to([ph.get_x(), 1.55, 0])
        threads = VGroup(*[Line(ph.get_top(), d.get_bottom(), color=ROUTE, stroke_width=4)
                           for ph, d in zip(phones, datas)])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk), run_time=0.5)
            vo.wait_until("The lecture starts from the screens")
            self.play(FadeIn(ref), LaggedStart(*[FadeIn(p, shift=UP * 0.2) for p in phones], lag_ratio=0.25),
                      run_time=1.0)
            vo.wait_until("newsletters, podcasts")
            self.play(phones[0].frame.animate.set_stroke(TURN), run_time=0.4)
            vo.wait_until("podcasts, and a chat")
            self.play(phones[0].frame.animate.set_stroke(LAPTOP), phones[1].frame.animate.set_stroke(TURN), run_time=0.4)
            vo.wait_until("and a chat that takes a photo")
            self.play(phones[1].frame.animate.set_stroke(LAPTOP), phones[2].frame.animate.set_stroke(TURN), run_time=0.4)
            self.play(Indicate(phones[2][3][0], color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Each screen needs data")
            self.play(phones[2].frame.animate.set_stroke(LAPTOP), run_time=0.3)
            self.play(LaggedStart(*[Create(t) for t in threads], lag_ratio=0.2), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.15) for d in datas], lag_ratio=0.2), run_time=0.7)
            vo.wait_until("and each kind of data")
            self.play(LaggedStart(*[Indicate(d, color=ROUTE, scale_factor=1.1) for d in datas], lag_ratio=0.2),
                      run_time=1.0)

        # ========================================================== 1. slide 44 and service.py: the tree
        ref44 = lref("44 (APIs)")
        rt = RouteTree()
        rt.groups(quiet)                                  # built in place (row y 2.45), shown by the morph
        gc = rt.group_chips
        panel = code(SERVICE, 31, 40, font_size=20, elide=ELIDE)
        panel.move_to([0, 0.0, 0])
        assert panel.get_top()[1] < min(c.get_bottom()[1] for c in gc.values()) - 0.05, panel.get_top()
        assert panel.get_left()[0] > -SAFE_X and panel.get_right()[0] < SAFE_X, panel.width
        pc = panel.code
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(phones), FadeOut(threads), FadeOut(ref), FadeIn(ref44), run_time=0.5)
            tgt = {"newsletters": [gc["Newsletters"]], "podcasts": [gc["Podcasts"]],
                   "chat": [gc[n] for n in ("LLM Chat", "LLM + CNN Chat", "RAG Chat", "Agent Chat")]}
            copies, anims = [], []
            for d, key in zip(datas, ("newsletters", "podcasts", "chat")):
                cs = VGroup(*[c.copy() for c in tgt[key]])
                copies.append(cs)
                anims.append(FadeTransform(d, cs))
            self.play(*anims, run_time=1.0)
            self.remove(*copies)
            self.add(rt)
            self.play(FadeIn(panel, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("newsletters and podcasts get a router each")
            bars = VGroup(line_bar(pc, 5, TURN), line_bar(pc, 6, TURN))
            self.play(FadeIn(bars), run_time=0.5)
            vo.wait_until("under slash api")
            apis = [code_span(pc, 5, '"/api'), code_span(pc, 6, '"/api')]
            self.play(*[a.animate.set_color(ROUTE) for a in apis], run_time=0.4)
            self.add(panel)
            self.play(*[Indicate(a, color=ROUTE, scale_factor=1.15) for a in apis], run_time=0.6)
            self.add(panel)
            vo.wait_until("Then one function stamps out")
            crs = [code_span(pc, k, "create_router") for k in (7, 8, 9)]
            self.play(FadeOut(bars), *[c.animate.set_color(TOOL) for c in crs], run_time=0.5)
            self.add(panel)
            self.play(FadeOut(panel, shift=DOWN * 0.2), run_time=0.4)
            rt.roots(self, run_time=0.3)
            rt.branch(self, "newsletters", run_time=0.35)
            rt.branch(self, "podcasts", run_time=0.35)
            rt.stamp(self, run_time=1.6)
            for k, word in (("llm", "Ask"), ("llm-cnn", "Identify and"), ("llm-rag", "Cheese books")):
                vo.wait_until(word)
                m = label(RouteTree.MODES[k], 20, INK).move_to(rt.p(0, rt.BR_Y[k]))
                m.set_x(rt.p(1.4, 0)[0] + m.width / 2)
                rt.mode_labels[k] = m
                rt.show(self, m, anims=[FadeIn(m, shift=LEFT * 0.1)], run_time=0.4)
            vo.wait_until("The lecture shows six groups")
            agent = rt.snap(self, run_time=1.3)
            vo.wait_until("agent chat has no router")
            err44 = erratum_tag("slide 44: six · this repo: five routers")
            err44.next_to(agent, DOWN, buff=0.15)
            err44.set_x(SAFE_X - 0.15 - err44.width / 2)
            assert err44.get_bottom()[1] > -SAFE_Y + 0.05
            self.play(Indicate(agent, color=S.GREY, scale_factor=1.12), FadeIn(err44, shift=UP * 0.1), run_time=0.7)
            rt.heal(self)

        # ========================================================== 2. slides 30–33: where an agent sits
        ref30 = lref("30–33 (APIs)")
        dg = agents_diagram()
        P = dg.p
        agent_c = dashed_chip("agent").move_to([-5.0, -0.5, 0])
        mcp = dashed_chip("MCP service").move_to([0.4, -0.5, 0])
        behind = np.array([-1.6, -0.5, 0])
        a33 = grey_chip("REST API · for apps · FastAPI  |  MCP · for agents · FastMCP · not in this repo")
        a33.move_to([0, -2.2, 0])
        assert a33.width < 2 * SAFE_X - 0.3, a33.width
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(rt), FadeOut(err44), FadeOut(ref44), FadeIn(ref30), run_time=0.5)
            self.play(FadeIn(dg), FadeIn(agent_c), run_time=0.7)
            # slide 30: the agent behind the API, with an MCP service
            l_api_agent = Line(P["api"].get_bottom(), behind + UP * 0.25, color=S.GREY, stroke_width=2.5)
            l_agent_mcp = Line(behind + RIGHT * 0.5, mcp.get_left(), color=S.GREY, stroke_width=2.5)
            l_mcp_bus = Line(mcp.get_right(), [dg.bus_x, -0.5, 0], color=S.GREY, stroke_width=2.5)
            self.play(agent_c.animate.move_to(behind), FadeIn(mcp), run_time=0.8)
            self.play(Create(l_api_agent), Create(l_agent_mcp), Create(l_mcp_bus), run_time=0.5)
            vo.wait_until("with or without an MCP service")
            # slide 31: no MCP; the agent wires straight to the bus
            l_direct = Line(behind + RIGHT * 0.5, [dg.bus_x, -0.5, 0], color=S.GREY, stroke_width=2.5)
            self.play(FadeOut(mcp), FadeOut(l_agent_mcp), FadeOut(l_mcp_bus), Create(l_direct), run_time=0.6)
            self.wait(0.3)
            # slide 32: the agent is the client
            front = P["browser"].get_center()
            self.play(FadeOut(P["browser"]), FadeOut(P["b2a"]), FadeOut(l_api_agent), FadeOut(l_direct),
                      run_time=0.4)
            self.play(agent_c.animate.move_to(front), run_time=0.7)
            a2api = arrow(agent_c.get_right(), P["api"].get_left(), S.GREY, stroke=3)
            self.play(GrowArrow(a2api), run_time=0.4)
            vo.wait_until("This repository has none")
            self.play(FadeIn(a33, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(a33.text, color=INK, scale_factor=1.04), run_time=0.6)

        # ========================================================== 3. slides 39–41: the one-file route
        ref39 = lref("39–41 (APIs)")
        idea = card([mono('@app.get("/newsletters")', 22, INK)], head="slide 39 · the idea")
        idea.move_to([SAFE_X - 0.15 - idea.width / 2, 2.05, 0])
        err39 = erratum_tag()
        err39.next_to(idea, LEFT, buff=0.25)
        assert idea.get_top()[1] < ref39.get_bottom()[1] - 0.05, (idea.get_top(), ref39.get_bottom())
        assert err39.get_left()[0] > trk.get_right()[0] + 0.1 or err39.get_top()[1] < trk.get_bottom()[1]
        assert idea.get_bottom()[1] > gc["Newsletters"].get_top()[1] + 0.05
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(*[P[k] for k in ("api", "ends", "bus", "links", "a2b")])),
                      FadeOut(agent_c), FadeOut(a2api), FadeOut(a33), FadeOut(ref30), run_time=0.5)
            self.remove(dg)
            self.play(FadeIn(rt), FadeIn(ref39), run_time=0.5)
            self.play(FadeIn(idea, shift=DOWN * 0.15), FadeIn(err39), run_time=0.5)
            vo.wait_until("The repository puts the same function")
            for k in ("api", "newsletters"):
                self.play(rt.light(k, TURN), run_time=0.35)
                rt.heal(self)
            self.play(rt.edges["newsletters"].animate.set_color(ROUTE), run_time=0.3)
            rt.heal(self)
            vo.wait_until("mounted at slash api")
            plabel = rt.path_label(self, "newsletters", "/api/newsletters", run_time=0.6)
            self.play(Indicate(plabel, color=ROUTE, scale_factor=1.1), run_time=0.6)
            rt.heal(self)

        # ========================================================== 4. step 5: the demo route, StatReload
        body = VGroup(label("Open api/service.py, add this after get_status, and save.", 20, INK),
                      label("api_server reloads by itself.", 20, INK),
                      VGroup(*[mono_line(s, 20, INK) for s in R_CODE]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        for ln in body[2]:
            ln.shift(RIGHT * (body[2][0].strut.get_left()[0] - ln.strut.get_left()[0]))
        card4 = readme_card((106, 112), body)
        card4.move_to([-6.45 + card4.width / 2, 0.6, 0])
        ed = editor_chip().next_to(card4, DOWN, buff=0.3).align_to(card4, LEFT)
        assert card4.get_top()[1] < TRACK_BOTTOM and card4.get_right()[0] < SAFE_X
        t4 = term(P_V2_API, rows=9, title=T_TAB, size=20)
        diff = [(s, OWN) if s.startswith("+") else s for s in B27.at((20, 21), (24, 29))]
        ut = term(container_prompt(B21, 37), rows=4, title=T_LAPTOP, size=20)
        with self.voiceover(SAY[4]) as vo:
            rt.drop(self, *gc.values(), plabel, run_time=0.4,
                    extra=[FadeOut(idea), FadeOut(err39), FadeOut(ref39), track(trk, 5)])
            rt.group_chips = {}
            for k in ("api", "newsletters"):
                rt.nodes[k].box.set_stroke(ROUTE)
            rt.edges["newsletters"].set_color(S.GREY)
            self.play(FadeOut(rt), FadeIn(card4, shift=DOWN * 0.15), run_time=0.6)
            vo.wait_until("add the README's function")
            self.play(FadeIn(ed, shift=UP * 0.1), run_time=0.4)
            flash_tag(self, ed, S.GREY)
            vo.wait_until("and save")
            self.play(FadeOut(card4, shift=UP * 0.2), FadeIn(t4),
                      ed.animate.move_to(under_term(t4, ed.copy()).get_center()), run_time=0.6)
            type_capture(self, t4, B27, type_time=0.7)
            bar_tag(self, t4, extra_row())
            out(self, t4, diff, run_time=0.8)
            vo.wait_until("The server reloads by itself")
            rt.shift(TREE_UP)
            self.play(FadeOut(t4), FadeOut(ed), run_time=0.4)
            self.play(FadeIn(rt), FadeIn(ut), run_time=0.5)
            w = out(self, ut, [(B21.line(65), TURN)], run_time=0.4)
            self.play(Indicate(substring(w[0], "StatReload detected changes"), color=TURN, scale_factor=1.05),
                      run_time=0.6)
            self.add(ut)
            rt.add_leaf(self, "square_root", run_time=0.6)
            out(self, ut, B21.at(70, 71) + [(B21.line(72), OWN)], run_time=0.6)

        # ========================================================== 5. extra: readyz again
        tab = term(P_V2_API, rows=4, title=T_TAB, size=20)
        with self.voiceover(SAY[5]) as vo:
            rt.probes(self, run_time=0.5)
            ry = rt.nodes["readyz"]
            lp = lamp("amber", 0.17).move_to([ry.get_x(), ry.get_bottom()[1] - 0.3, 0])
            assert lp.get_top()[1] < ry.get_bottom()[1] + 0.02, (lp.get_top(), ry.get_bottom())
            assert lp.get_bottom()[1] > rt.nodes["api"].get_top()[1] + 0.02
            rt.show(self, lp, anims=[FadeIn(lp, scale=1.3)], run_time=0.5)
            self.play(Indicate(lp, color=AMBER, scale_factor=1.25), run_time=0.6)
            rt.heal(self)
            vo.wait_until("and readyz is back to 200")
            self.play(FadeOut(ut), FadeIn(tab), run_time=0.4)
            type_capture(self, tab, B30, type_time=0.6)
            bar_tag(self, tab, extra_row())
            out(self, tab, [(s, OWN) for s in B30.at(2, 3)], run_time=0.5)
            lp = rt.swap(self, lp, lamp("green", 0.17).move_to(lp), run_time=0.5)

        # ========================================================== 6. step 6: try the route
        br = Browser("localhost:9000/api/square_root", win_w=6.3, win_h=1.55)
        br._addr("localhost:9000/api/square_root?x=3&y=4")         # the long address must fit too
        br.move_to([SAFE_X - 0.15 - br.width / 2, 1.9, 0])
        ill = illustration_tag().next_to(br, DOWN, buff=0.1).align_to(br, RIGHT)
        assert br.get_top()[1] < TRACK_BOTTOM - 0.1 and br.get_left()[0] > rt.nodes["square_root"].get_right()[0] + 0.1
        assert ill.get_left()[0] > max(m.get_right()[0] for m in rt.mode_labels.values()) + 0.1
        with self.voiceover(SAY[6]) as vo:
            self.play(track(trk, 6), run_time=0.5)
            clear_lines(self, tab)
            vo.wait_until("Then open slash api, square root")
            ln = type_capture(self, tab, B28, type_time=0.8)[0]
            bar_tag(self, tab, extra_row())
            out(self, tab, [B28.line(2)], run_time=0.4)
            self.play(FadeIn(br), FadeIn(ill), run_time=0.5)
            br.fill(self, [B28.line(2)], mono_font=True, run_time=0.4)
            vo.wait_until("With x equals 3 and y equals 4")
            type_capture(self, tab, B29, type_time=0.8)
            five = out(self, tab, [(B29.line(2), OWN)], run_time=0.4)
            br.goto(self, "localhost:9000/api/square_root?x=3&y=4", run_time=0.5)
            br.fill(self, [B29.line(2)], mono_font=True, color=OWN, run_time=0.4)
            self.play(Indicate(five[0], color=OWN, scale_factor=1.3), br.flash(OWN), run_time=0.7)
            self.add(tab)
            vo.wait_until("Pause and try both")
            turn6 = bar_tag(self, tab, turn_row(), left=True)

        # ========================================================== 7. step 7: API docs, the 25 leaves
        with self.voiceover(SAY[7]) as vo:
            rt.drop(self, lp, run_time=0.4, extra=[FadeOut(br), FadeOut(ill), track(trk, 7)])
            tab.remove(turn6)
            # the docs check and the extra listing fold onto 2 and 5 rows: the strip grows over the tree
            # for them, then shrinks back under it for the leaves
            self.play(FadeOut(turn6), FadeOut(rt), *unbar(tab), run_time=0.4)
            clear_lines(self, tab)
            resize(self, tab, 10, run_time=0.6)
            type_capture(self, tab, B31, type_time=1.0)
            bar_tag(self, tab, extra_row())
            rows = out(self, tab, B31.at((2, 4)), run_time=0.5)
            oa = first_row(rows, "openapi.json")
            self.play(substring(oa, "/api/openapi.json").animate.set_color(TURN), run_time=0.4)
            self.add(tab)
            vo.wait_until("An extra listing")
            self.play(track(trk, 7, extra=True), run_time=0.4)
            clear_lines(self, tab)
            type_capture(self, tab, B32, type_time=1.0)
            out(self, tab, B32.at((2, 27)), run_time=1.6, chunk=10)
            vo.wait_until("the leaves of this tree")
            resize(self, tab, 4, extra=[FadeIn(rt), *unbar(tab)], run_time=0.7)
            cnt = rt.leaves(self, run_time=1.4)
            self.play(Indicate(cnt, color=INK, scale_factor=1.1), run_time=0.6)
            rt.heal(self)

        # ========================================================== 8. step 8: GET /api/newsletters
        t8 = term(P_V2_API, rows=9, title=T_TAB, size=20)
        dbr = Browser("localhost:9000/api/docs", win_w=4.8, win_h=1.95)
        dbr.move_to([-SAFE_X + 0.15 + dbr.width / 2, 1.8, 0])
        assert dbr.get_bottom()[1] > t8.box.get_top()[1] + 0.1 and dbr.get_top()[1] < TRACK_BOTTOM - 0.1
        get_row = VGroup(mono("GET", 20, INK), mono("/api/newsletters", 20, ROUTE)).arrange(RIGHT, buff=0.25)
        lim_row = VGroup(label("limit", 20, S.GREY), mono("= 2", 20, INK)).arrange(RIGHT, buff=0.2)
        exe = grey_chip("Execute")
        ref41 = lref("41 (APIs)")
        c41 = card(["slide 41: a JSON list of newsletters"], size=20)
        c41.move_to([SAFE_X - 0.15 - c41.width / 2, 2.0, 0])
        assert c41.get_top()[1] < ref41.get_bottom()[1] - 0.05 and c41.get_left()[0] > dbr.get_right()[0] + 0.1
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(rt), FadeOut(tab), track(trk, 8), run_time=0.5)
            self.play(FadeIn(dbr), FadeIn(t8), run_time=0.5)
            dbr.fill(self, [get_row, VGroup(lim_row, exe).arrange(RIGHT, buff=0.6)], run_time=0.5)
            ill8 = illustration_tag().next_to(dbr, RIGHT, buff=0.2).align_to(dbr, UP)
            turn8 = your_turn().next_to(exe, RIGHT, buff=0.35)
            turn8.set_x(dbr.get_right()[0] + 0.2 + turn8.width / 2)
            assert turn8.get_right()[0] < c41.get_left()[0] or turn8.get_top()[1] < c41.get_bottom()[1]
            assert turn8.get_top()[1] < ill8.get_bottom()[1] - 0.05, (turn8.get_top(), ill8.get_bottom())
            assert ill8.get_right()[0] < c41.get_left()[0] - 0.1, (ill8.get_right(), c41.get_left())
            self.play(FadeIn(ill8), run_time=0.3)
            vo.wait_until("pause and try get newsletters")
            self.play(Indicate(get_row, color=ROUTE, scale_factor=1.08), FadeIn(turn8, shift=LEFT * 0.1), run_time=0.6)
            dbr.heal(self)
            vo.wait_until("with a limit of 2")
            self.play(Indicate(lim_row, color=TURN, scale_factor=1.12), run_time=0.5)
            self.play(Indicate(exe, color=TURN, scale_factor=1.12), run_time=0.5)
            dbr.heal(self)
            type_capture(self, t8, B33, type_time=1.0)
            vo.wait_until("Two newsletters come back")
            rows = out(self, t8, B33.at((5, 9), (15, 19), (25, 26)), run_time=0.8)
            titles = [r for r in rows if '"title"' in r.text and r in t8.lines]
            assert len(titles) == 2, len(titles)
            self.play(*[r.animate.set_color(TURN) for r in titles], run_time=0.5)
            self.add(t8)
            vo.wait_until("newest first")
            dts = [r for r in rows if '"dts"' in r.text and r in t8.lines]
            self.play(*[r.animate(rate_func=there_and_back).set_color(INK) for r in dts], run_time=0.8)
            self.add(t8)
            vo.wait_until("the lecture's example, now real")
            self.play(FadeIn(ref41), FadeIn(c41, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("An unknown ID gets 404")
            type_capture(self, t8, B34, type_time=0.8)
            bar_tag(self, t8, extra_row())
            out(self, t8, [(s, ERR) for s in B34.at(2, 3)], run_time=0.4)

        # ========================================================== 9. step 9: review the code
        tbl = readme_table()
        card9 = readme_card((123, 132), tbl)
        card9.move_to([0, -0.3, 0])
        assert card9.get_top()[1] < TRACK_BOTTOM - 0.05 and card9.width < 2 * SAFE_X - 0.2, card9.width
        with self.voiceover(SAY[9]) as vo:
            keep = set(trk.get_family())
            gone = [m for m in self.mobjects if m not in keep]
            self.play(*[FadeOut(m) for m in gone], track(trk, 9), run_time=0.6)
            self.remove(*gone)
            self.play(FadeIn(card9, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Service dot py builds the app")
            # the tree comes back at its full-frame place, without leaves and counter
            rt.extra.remove(*list(rt.extra.submobjects))
            rt.shift(-TREE_UP)
            self.play(FadeOut(card9, shift=UP * 0.2), FadeIn(rt), run_time=0.6)
            fs = rt.file_map(self, run_time=1.0)
            svc, st = fs[5], fs[6]
            rest = fs[7:]
            chat_py = [f for f in rest if hasattr(f, "text") and getattr(f.text, "text", "") == "chat.py"]
            cu = fs[-1]
            self.play(Indicate(svc, color=TURN, scale_factor=1.12), run_time=0.6)
            rt.heal(self)
            vo.wait_until("settings dot py holds every setting")
            self.play(Indicate(st, color=TURN, scale_factor=1.12), run_time=0.6)
            rt.heal(self)
            vo.wait_until("the routers hold the routes")
            self.play(*[Indicate(f, color=TURN, scale_factor=1.1) for f in fs[:2] + chat_py], run_time=0.7)
            rt.heal(self)
            vo.wait_until("and one utils file per chat mode")
            self.play(LaggedStart(*[Indicate(f, color=TURN, scale_factor=1.1) for f in fs[2:5]], lag_ratio=0.3),
                      run_time=1.0)
            rt.heal(self)
            self.play(Indicate(cu, color=OWN, scale_factor=1.06), run_time=0.6)
            rt.heal(self)
            self.wait(0.6)
            self.play(FadeOut(rt), FadeOut(trk), run_time=0.8)
        self.wait(0.3)
