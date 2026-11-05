"""S10 · Why a framework: React with Vite (AC215 L18, part 2 opens). No tracker until
`cd src/frontend-react`; then tracker [R] "README › Tutorial: React Frontend Setup" 1 → 4
(4 · extra in beat 10). Lecture tags: Frontend slides 30–31, 32–33, 35–37 (beats 1–5).

Beats (script.md "## S10", one voiceover block each):
0. Title "Part 2 · the frontend" over V5's laptop (API and vector-db boxes on the GREEN cable, the
   API box badged GREEN '26 passed'); on "up on port 9000" the badge and door 9000 pulse; on "a page
   that uses it" an empty GREY browser (illustration) slides in with a dashed PINK arrow toward the
   laptop.
1. LECTURE 30–31. V8 OneShell part a: four separate pages (header strip, name, JS / CSS chips);
   headers, then script and style chips flash; GREY chips "nothing shared", "every page loads
   separately", "slow"; two GREY reload sweeps; "slow" flashes.
2. LECTURE 32–33. The pages collapse into one outline "single-page app · components"; the four
   framework chips of slide 33 (no logos), React YELLOW.
3. LECTURE 35–37. V8 part b: the component card "function → markup (JSX)"; the shell (Header ·
   defined once / middle block / Footer); a YELLOW pin on the header; the middle block swaps Home →
   Newsletters → Chat while the header stays.
4. A GREY chip under the React chip "React + Vite (dev server, build) + React Router (pages)" with
   the tag "erratum · today's repo". Then the chips and card go, the shell slides right and
   CODE(src/main.jsx: 17–24) comes in on the left (element names cut, '…'): index, chat,
   newsletters, newsletters/:id, podcasts fly one by one into the PINK address bar above the shell
   and the middle block shows the matching page; on "with a star" `*` → "Not found".
5. CODE(src/App.jsx: 15–17) and CODE(App.jsx: 52–59) stacked on the left: line 17 `<header` → the
   shell's header (the pin pulses once), line 55 `<Outlet />` → the middle block (tag "<Outlet />"),
   line 59 `<footer` → the footer. LECTURE off at the end.
6. Tracker [R] 1. A 3-row `laptop · new terminal` strip at ~/cheese-app-v2 types `cd
   src/frontend-react` (d01, the prompt changes); tracker [R] 2, `./docker-shell.sh` (d02:1).
   CODE(frontend-react/docker-shell.sh: 14–23) on the left, a small V5 on the right (the laptop frame,
   the API box and a dimmed vector-db box on the GREEN cable, as in beat 0 and S11): line 19 GREEN, line 20 ORANGE (an ORANGE chip "named volume" under the frontend
   box), line 21 PINK (the frontend box comes in behind door 3000, ':5173'), line 22 GREEN (its stub
   joins the cable). ▶ your turn on the title bar.
7. The panel and the drawing go; the terminal grows to 10 rows: d02:2–3 (cut), …, 21–25, 27
   (YELLOW), 29–33 (31 wrapped); row tag "at the time of recording" on the Node line; the GREY chip
   "your first run: a full install into the volume · docker-entrypoint.dev.sh:8" above the terminal.
8. Tracker [R] 3. At d02:35's container prompt it types `npm run dev` → d02:37–38, 80 (PURPLE),
   82–83 with a GREY brace "inside the container"; V5's frontend row (door 3000 → :5173) returns
   above the terminal and its door pulses PINK on "use 3000". ▶ your turn.
9. Tracker [R] 4. The terminal goes; a GREY browser (illustration) at localhost:3000. A 5-row
   `laptop · second tab` strip types d03:1 (extra) → d03:2, 23, 26–27; `<div id="root"></div>` and
   `/src/main.jsx` YELLOW. In the browser: an empty dashed `root` box; the `/src/main.jsx` card
   beside it; on "The whole app is one page" an arrow from the script fills the root box with a
   header / page / footer.
10. Tracker [R] 4 · extra. The browser goes; the tab (8 rows) types d08:1 (folds, extra) → d08:2–6,
   every `200 text/html` YELLOW, `/nope` flashes. On "The browser picks the page" the tab shrinks to
   2 rows and the V8 shell returns: its PINK address bar cycles /podcasts, /newsletters,
   /chat?model=llm, /nope, the middle block swaps to the matching page and, for /nope, "Not found".
   Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ the real sources (checked)
D01 = capture("d01")
D02 = capture("d02")
D03 = capture("d03")
D08 = capture("d08")

assert D01.cmd == "cd src/frontend-react" and D01.lines == [], D01.lines
assert D02.cmd == "./docker-shell.sh"
assert D02.line(2) == "Building cheese-app-frontend-react (Dockerfile.dev)..."
assert D02.line(3).startswith("[+] Building 0.4s (7/7) FINISHED")
assert D02.at((21, 25)) == ["Container is running!!!", "Architecture: x86_64", "Node version: v24.22.1",
                            "npm version: 11.19.1", "Installing dependencies..."], D02.at((21, 25))
assert D02.line(27) == "up to date in 571ms"
assert D02.line(29) == "The following commands are available:" and D02.line(30).strip() == "npm run dev"
assert D02.line(32).strip() == "npm run check"
assert at_prompt(D02, 35)[1] == "npm run dev"
assert D02.at((37, 38)) == ["> cheese-app-frontend@2.0.0 dev", "> vite"], D02.at((37, 38))
assert D02.line(80).strip().startswith("VITE v8.3.5  ready")
assert D02.line(82).strip() == "➜  Local:   http://localhost:5173/"
assert D02.line(83).strip().startswith("➜  Network: http://172.19.0.4:5173/")
assert D03.cmd == "curl -s -i http://localhost:3000/ | grep -v '^\\s*$'", D03.cmd
assert D03.line(2) == "HTTP/1.1 200 OK" and D03.line(23).strip() == "<title>Formaggio</title>"
assert D03.line(26).strip() == '<div id="root"></div>'
assert D03.line(27).strip() == '<script type="module" src="/src/main.jsx"></script>'
assert D08.cmd.startswith("for u in / /podcasts /newsletters /chat?model=llm /nope; do")
D08_ROWS = D08.at((2, 6))
assert [r.split()[0] for r in D08_ROWS] == ["/", "/podcasts", "/newsletters", "/chat?model=llm", "/nope"]
assert all(r.endswith("200 text/html") for r in D08_ROWS), D08_ROWS

FR = f"{V2}/src/frontend-react"
MAIN = f"{FR}/src/main.jsx"
APP = f"{FR}/src/App.jsx"
DSH = f"{FR}/docker-shell.sh"
EPD = f"{FR}/docker-entrypoint.dev.sh"
# main.jsx's route table: (file line, the text that flies, the address it becomes, the page it shows)
ROUTES = [(18, "index", "/", "Home"), (19, 'path="chat"', "/chat", "Chat"),
          (20, 'path="newsletters"', "/newsletters", "Newsletters"),
          (21, 'path="newsletters/:id"', "/newsletters/:id", "Newsletter"),
          (22, 'path="podcasts"', "/podcasts", "Podcasts"), (23, 'path="*"', "/*", "Not found")]
for _n, _sub, _p, _pg in ROUTES:
    assert _sub in excerpt(MAIN, _n, _n), (_n, _sub)
    assert f"<{_pg.replace(' ', '')}" in excerpt(MAIN, _n, _n) or _pg == "Not found", (_n, _pg)
assert "<NotFound />" in excerpt(MAIN, 23, 23)
assert excerpt(MAIN, 17, 17).strip() == "<Route element={<App />}>"
assert excerpt(APP, 17, 17).strip().startswith("<header ") and excerpt(APP, 16, 16).strip().startswith("<div ")
assert excerpt(APP, 55, 55).strip() == "<Outlet />" and excerpt(APP, 59, 59).strip().startswith("<footer ")
assert excerpt(APP, 54, 54).strip().startswith("<main ")
assert excerpt(DSH, 19, 19).strip() == '-v "$(pwd)":/app \\'
assert excerpt(DSH, 20, 20).strip() == '-v "${IMAGE_NAME}-node_modules:/app/node_modules" \\'
assert excerpt(DSH, 21, 21).strip() == "-p 3000:5173 \\"
assert excerpt(DSH, 22, 22).strip() == "--network cheese-app-network \\"
assert "a full install only the first time" in excerpt(EPD, 8, 8)


# ------------------------------------------------------------------ local helpers (as in S07)
def bar_tag(scene, t: Terminal, tg):
    """PLAYS: a row-sized tag on the terminal's title bar (replacing the one there)."""
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


def clear_bar(scene, t: Terminal, *extra):
    """PLAYS: the title-bar tag (if any) leaves."""
    old = getattr(t, "bar_tag", None)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), *extra, run_time=0.3)
        t.bar_tag = None
    elif extra:
        scene.play(*extra, run_time=0.3)


def clear_lines(scene, t: Terminal, run_time: float = 0.4):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    if not gone:
        return
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
    scene.remove(*gone)


def recolor(scene, row, sub: str, color, run_time: float = 0.4):
    """PLAYS: colour `sub` inside terminal row `row`."""
    scene.play(substring(row, sub).animate.set_color(color), run_time=run_time)


def strip_flash(scene, rect, text=None, color=TURN, *extra, run_time: float = 0.6):
    """PLAYS: pulse an unfilled copy of a filled strip's outline (and flash its words): Indicate on the
    filled strip itself paints a solid block over the words."""
    edge = rect.copy().set_fill(opacity=0)
    anims = [edge.animate(rate_func=there_and_back).set_stroke(color, width=6)]
    if text is not None:
        anims.append(Indicate(text, color=color, scale_factor=1.08))
    scene.play(*anims, *extra, run_time=run_time)
    scene.remove(edge)


def mini_net():
    """Beats 6 and 8: a compact V5 on the right, in the same shape as the opening's and S11's laptop: the
    GREY frame 'your laptop' (x 2.35 .. 6.55, its left wall carrying the doors), the API box behind door
    9000 and the vector-db box behind door 8000 (dimmed: not part of this step) on the GREEN cable; the
    frontend row on top (door 3000, ':5173', box), its stub and the ORANGE 'named volume' chip are built
    here and shown on their phrases.
    .frame .title .api .api_door .api_tun .vdb .cable .stub_api .label .front .door .tunnel .port .stub .vol"""
    g = VGroup()
    cx, wall = 6.3, 2.35
    yf, ya, yv = 1.92, 0.44, -0.54
    frame = RoundedRectangle(width=4.2, height=4.18, corner_radius=0.16, stroke_color=LAPTOP,
                             stroke_width=3).set_fill(S.BG, 1)
    frame.move_to([wall + 2.1, 2.78 - 4.18 / 2, 0])
    title = label("your laptop", 20, LAPTOP).align_to(frame, UR).shift(np.array([-0.18, -0.12, 0]))
    api = cbox(("cheese-app-", "api-service"), 2.7, 0.84).move_to([4.45, ya, 0])
    front = cbox(("cheese-app-", "frontend-react"), 2.7, 0.84).move_to([4.45, yf, 0])
    vbox = cbox(("cheese-app-", "vector-db"), 2.7, 0.84).move_to([4.45, yv, 0])
    cable = Line([cx, yf + 0.3, 0], [cx, yv - 0.3, 0], color=NET, stroke_width=6)
    stub_api = Line(api.get_right(), [cx, ya, 0], color=NET, stroke_width=5)
    stub = Line(front.get_right(), [cx, yf, 0], color=NET, stroke_width=5)
    lab = mono(NETWORK, 20, NET).next_to(vbox, DOWN, buff=0.12)
    lab.shift(RIGHT * (cx + 0.1 - lab.get_right()[0]))
    api_door = door("9000").move_to([wall, ya, 0])
    api_tun = Line(api_door.get_right(), api.get_left(), color=ROUTE, stroke_width=4)
    v_door = door("8000").move_to([wall, yv, 0])
    v_tun = Line(v_door.get_right(), vbox.get_left(), color=ROUTE, stroke_width=4)
    v_stub = Line(vbox.get_right(), [cx, yv, 0], color=NET, stroke_width=5)
    vdb = VGroup(v_tun, v_stub, v_door, vbox)
    vdb.fade(0.6)
    dr = door("3000").move_to([wall, yf, 0])
    tun = Line(dr.get_right(), front.get_left(), color=ROUTE, stroke_width=4)
    port = mono(":5173", 20, ROUTE).next_to(front.frame.get_corner(UL), UP, buff=0.04)
    port.align_to(front.frame, LEFT).shift(RIGHT * 0.12)
    vol = chip("named volume", SHARED, size=20)
    vol.move_to([front.get_x(), (front.get_bottom()[1] + api.get_top()[1]) / 2, 0])
    g.add(frame, title, cable, stub_api, api_tun, vdb, api_door, api, lab)
    g.frame, g.title, g.vdb = frame, title, vdb
    g.api, g.api_door, g.api_tun, g.cable, g.stub_api, g.label = api, api_door, api_tun, cable, stub_api, lab
    g.front, g.door, g.tunnel, g.port, g.stub, g.vol = front, dr, tun, port, stub, vol
    return g


def root_fill(bx, top: float) -> VGroup:
    """Beat 9: what main.jsx renders into the empty root box, below y=`top`: a header bar, a page, a
    footer bar (text-free; the shell of beat 3 in small)."""
    w = bx.width - 0.3
    h = top - bx.get_bottom()[1] - 0.12
    hd = Rectangle(width=w, height=0.26, stroke_color=TOOL, stroke_width=2).set_fill(tint(TOOL, 0.25), 1)
    md = Rectangle(width=w, height=h - 0.26 - 0.2 - 0.2, stroke_color=S.GREY, stroke_width=2)
    ft = Rectangle(width=w, height=0.2, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
    g = VGroup(hd, md, ft).arrange(DOWN, buff=0.1)
    g.move_to([bx.get_x(), 0, 0]).align_to([0, top, 0], UP)
    return g


def route_to(scene, sh: OneShell, path: str, page: str, src=None, extra=(), run_time: float = 0.45):
    """PLAYS: OneShell's address bar shows `path` and its middle block `page` in ONE animation (the
    shared address() and page() play one after the other). src: glyphs (a code_span) whose copy morphs
    into the new address. The new texts become the piece's .bar_text / .mid_text."""
    tgt = mono(path, 22, ROUTE).move_to(sh.bar_text).align_to(sh.bar, LEFT).shift(RIGHT * 0.25)
    mid = label(page, 26, ERR if page == "Not found" else INK).move_to(sh.middle)
    old_t, old_m = sh.bar_text, sh.mid_text
    sh._detach(old_t)
    sh._detach(old_m)
    scene.add(old_t, old_m)
    anims = [FadeOut(old_t), ReplacementTransform(old_m, mid)]
    if src is not None:
        fly = src.copy()
        scene.add(fly)
        anims.append(ReplacementTransform(fly, tgt))
    else:
        fly = None
        anims.append(FadeIn(tgt))
    scene.play(*anims, *extra, run_time=run_time)
    scene.remove(old_t, old_m, mid, tgt, *([fly] if fly is not None else []))
    sh.add(tgt, mid)
    sh.bar_text, sh.mid_text = tgt, mid
    sh.heal(scene)
    return tgt


class ReactShell(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S10"] == 11, len(SAY)

        # ========================================================== 0. Part 2: a page that uses the API
        title = label("Part 2 · the frontend", 40, INK).move_to([0, 2.75, 0])
        uline = Line(LEFT, RIGHT, color=TURN, stroke_width=3).set_width(title.width + 0.3)
        uline.next_to(title, DOWN, buff=0.12)
        net0 = TwoLocalhosts(rows=("api", "vdb"), cable=True).move_to(ORIGIN)
        net0.shift(np.array([3.0, -0.75, 0]) - net0.p(0, 0))
        br0 = Browser("localhost:3000", win_w=4.4, win_h=3.0).move_to([-4.3, -0.55, 0])
        ill0 = illustration_tag().next_to(br0.frame, DOWN, buff=0.12).align_to(br0.frame, LEFT)
        y_front = net0.p(0, TwoLocalhosts.ROW_Y["front"])[1]
        a0 = DashedLine([br0.frame.get_right()[0] + 0.1, y_front, 0], [net0.wall_x() - 0.15, y_front, 0],
                        color=ROUTE, dash_length=0.12, stroke_width=4)
        tip0 = Triangle(color=ROUTE, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-PI / 2)
        tip0.move_to(a0.get_end())
        assert net0.get_bottom()[1] > -SAFE_Y and net0.get_right()[0] < SAFE_X, (net0.get_bottom(), net0.get_right())
        assert a0.get_length() > 0.5, a0.get_length()
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(title, shift=DOWN * 0.15), Create(uline), run_time=0.8)
            self.play(FadeIn(net0), run_time=0.6)
            badge = net0.on_box(self, "api", ok_chip("26 passed"))
            vo.wait_until("The API is up on port 9000")
            flash_tag(self, badge, OWN, 1.12, 0.9, net0.door_pulse("api", OWN))
            net0.heal(self)
            vo.wait_until("now a page that uses it")
            self.play(FadeIn(br0, shift=RIGHT * 0.6), FadeIn(ill0), run_time=0.6)
            self.play(Create(a0), FadeIn(tip0, rate_func=lambda x: min(1.0, 2 * x)), run_time=0.5)
            self.play(br0.flash(ROUTE), run_time=0.5)

        # ========================================================== 1. LECTURE 30–31: one page per feature
        ref1 = lref("30–31 (Frontend)")
        sh = OneShell()
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(title, uline, net0, br0, ill0, a0, tip0)), run_time=0.5)
            self.play(FadeIn(ref1), run_time=0.4)
            pages = sh.pages(self, run_time=1.0)
            vo.wait_until("Each carries its own header")
            self.play(LaggedStart(*[AnimationGroup(p[1].animate(rate_func=there_and_back).set_stroke(TURN, width=4),
                                                   Indicate(p[2], color=TURN, scale_factor=1.2)) for p in pages],
                                  lag_ratio=0.2), run_time=1.0)
            sh.heal(self)
            vo.wait_until("script and style")
            self.play(LaggedStart(*[Indicate(p[4], color=TURN, scale_factor=1.1) for p in pages], lag_ratio=0.2),
                      run_time=1.0)
            sh.heal(self)
            vo.wait_until("nothing is shared")
            sh.notes(self, run_time=1.0)
            vo.wait_until("and every click loads a whole page")
            strip_flash(self, pages[0][1], pages[0][2], ROUTE, run_time=0.4)
            sh.heal(self)
            sh.reload(self, 1, run_time=0.6)
            sh.reload(self, 3, run_time=0.6)
            vo.wait_until("slow")
            flash_tag(self, sh.note_chips[2], ERR, 1.15, 0.7)
            sh.heal(self)

        # ========================================================== 2. LECTURE 32–33: one app, a framework
        ref2 = lref("32–33 (Frontend)")
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(ref1), FadeIn(ref2), run_time=0.4)
            vo.wait_until("The fix")
            sh.collapse(self, run_time=1.2)
            vo.wait_until("with a framework")
            strip_flash(self, sh.outline, getattr(sh, "ol_title", None), TURN, run_time=0.8)
            sh.heal(self)
            vo.wait_until("The lecture names the common ones")
            fw = sh.frameworks(self, run_time=1.0)
            react = [c for c in fw if c.text.text == "React"][0]
            vo.wait_until("and picks React")
            flash_tag(self, react, TURN, 1.15, 0.8)
            sh.heal(self)

        # ========================================================== 3. LECTURE 35–37: components; one shell
        ref3 = lref("35–37 (Frontend)")
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(ref2), FadeIn(ref3), run_time=0.4)
            vo.wait_until("In React")
            comp = sh.component(self, run_time=0.6)
            assert comp.get_left()[0] > -SAFE_X, comp.get_left()
            vo.wait_until("written in JSX")
            self.play(Indicate(comp.body[1], color=TOOL, scale_factor=1.1), run_time=0.6)
            sh.heal(self)
            vo.wait_until("The app is one shell")
            sh.shell(self, "Home", run_time=0.9)
            vo.wait_until("a header defined only once")
            strip_flash(self, sh.header[0], sh.header[1], TURN, run_time=0.6)
            sh.heal(self)
            sh.pin_header(self)
            vo.wait_until("a footer")
            strip_flash(self, sh.footer[0], sh.footer[1], TURN, run_time=0.6)
            sh.heal(self)
            vo.wait_until("and in between a block")
            self.play(sh.middle.animate.set_stroke(TURN), run_time=0.3)
            sh.heal(self)
            sh.page(self, "Newsletters", run_time=0.5)
            self.wait(0.3)
            sh.page(self, "Chat", run_time=0.5)
            self.play(sh.middle.animate.set_stroke(S.GREY), Indicate(sh.pin, color=TURN, scale_factor=1.2),
                      run_time=0.6)
            sh.heal(self)

        # ========================================================== 4. today's repo: React + Vite + React Router; main.jsx
        rr = grey_chip("React + Vite (dev server, build) + React Router (pages)")
        err4 = erratum_tag("erratum · today's repo")
        row4 = VGroup(rr, err4).arrange(RIGHT, buff=0.25)
        pm = code(MAIN, 17, 24, font_size=20, dedent=True, shown="frontend-react/src/main.jsx",
                  cuts={n: sub for n, sub, _p, _pg in ROUTES})
        with self.voiceover(SAY[4]) as vo:
            row4.move_to([0, react.get_bottom()[1] - 0.2 - rr.height / 2, 0])
            assert row4.width < 2 * SAFE_X - 0.1 and row4.get_bottom()[1] > -SAFE_Y, row4.get_bottom()
            flash_tag(self, react, TURN, 1.1, 0.5)
            sh.heal(self)
            self.play(FadeIn(rr, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("a development server and build tool")
            self.play(Indicate(rr.text, color=TOOL, scale_factor=1.04), run_time=0.6)
            vo.wait_until("plus React Router")
            self.play(FadeIn(err4, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("In main dot jsx")
            sh.drop(self, *fw, comp, run_time=0.4, extra=[FadeOut(rr), FadeOut(err4)])
            pm.move_to([0, 0, 0]).align_to([-6.5, 0, 0], LEFT)
            pm.align_to([0, sh.outline.get_top()[1], 0], UP)
            assert pm.get_right()[0] < sh.outline.get_left()[0] + 3.3 - 0.15, (pm.get_right(), sh.outline.get_left())
            assert pm.get_bottom()[1] > -SAFE_Y, pm.get_bottom()
            self.play(sh.animate.shift(RIGHT * 3.3), FadeIn(pm, shift=RIGHT * 0.2), run_time=0.6)
            sh.heal(self)
            sh.address(self, "/", run_time=0.3)
            cur = None
            for n, sub, path, page in ROUTES:
                if n == 23:
                    vo.wait_until("with a star")
                k = n - 17
                bar = line_bar(pm.code, k, ROUTE)
                bar_anim = FadeIn(bar) if cur is None else ReplacementTransform(cur, bar)
                route_to(self, sh, path, page, src=code_span(pm.code, k, sub), extra=[bar_anim], run_time=0.55)
                cur = bar
                self.add(pm, cur)
            self.play(Indicate(code_span(pm.code, 6, "*"), color=ERR, scale_factor=1.4), run_time=0.6)
            self.add(pm, cur)

        # ========================================================== 5. App.jsx: header, Outlet, footer
        pa = code(APP, 15, 17, font_size=20, shown="frontend-react/src/App.jsx", cuts={16: "<div", 17: "<header"})
        pb = code(APP, 52, 59, font_size=20, shown="frontend-react/src/App.jsx", cuts={54: "<main", 59: "<footer"})
        VGroup(pa, pb).arrange(DOWN, aligned_edge=LEFT, buff=0.2).align_to([-6.5, 0, 0], LEFT)
        VGroup(pa, pb).align_to([0, 3.0, 0], UP)
        assert pb.get_bottom()[1] > -SAFE_Y + 0.05, pb.get_bottom()
        assert max(pa.get_right()[0], pb.get_right()[0]) < sh.outline.get_left()[0] - 0.15, pa.get_right()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(pm, cur)), run_time=0.4)
            route_to(self, sh, "/", "Home", run_time=0.4)
            self.play(FadeIn(pa, shift=RIGHT * 0.2), FadeIn(pb, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("the header and footer are written once")
            bh = line_bar(pa.code, 2, TURN)
            strip_flash(self, sh.header[0], sh.header[1], TURN, FadeIn(bh), run_time=0.7)
            self.add(pa, bh)
            sh.heal(self)
            self.play(Indicate(sh.pin, color=TURN, scale_factor=1.3), run_time=0.6)
            sh.heal(self)
            bf = line_bar(pb.code, 7, TURN)
            strip_flash(self, sh.footer[0], sh.footer[1], TURN, FadeIn(bf), run_time=0.7)
            self.add(pb, bf)
            sh.heal(self)
            vo.wait_until("and between them sits the outlet")
            bo = line_bar(pb.code, 3, ROUTE)
            self.play(FadeIn(bo), code_span(pb.code, 3, "<Outlet />").animate.set_color(ROUTE), run_time=0.5)
            self.add(pb, bo)
            sh.outlet(self, run_time=0.5)
            vo.wait_until("the window where the current page appears")
            self.play(sh.middle.animate.set_stroke(ROUTE), run_time=0.3)
            sh.heal(self)
            sh.page(self, "Newsletters", run_time=0.45)
            sh.page(self, "Home", run_time=0.45)
            self.play(sh.middle.animate.set_stroke(S.GREY), FadeOut(ref3), run_time=0.5)
            sh.heal(self)

        # ========================================================== 6. tracker R 1–2: cd; docker-shell.sh
        trk = tracker_r(1)
        t = term(P_V2, rows=3, title=T_NEW, size=20)
        pd = code(DSH, 14, 23, font_size=20, dedent=True, shown="frontend-react/docker-shell.sh",
                  cuts={14: 'echo "Building', 15: "docker build"}, elide={20: "${IMAGE_NAME}"})
        mn = mini_net()
        pd.move_to([0, 0, 0]).align_to([-6.5, 0, 0], LEFT).align_to([0, PIC_TOP - 0.02, 0], UP)
        assert pd.get_bottom()[1] > t.box.get_top()[1] + 0.05, (pd.get_bottom(), t.box.get_top())
        assert pd.get_right()[0] < mn.door.get_left()[0] - 0.1, (pd.get_right(), mn.door.get_left())
        assert mn.label.get_bottom()[1] > t.box.get_top()[1] + 0.05, mn.label.get_bottom()
        assert mn.port.get_top()[1] < mn.frame.get_top()[1] - 0.08 and mn.port.get_right()[0] < mn.title.get_left()[0] - 0.2, mn.port.get_top()
        assert mn.frame.get_top()[1] < PIC_TOP, mn.frame.get_top()
        assert mn.front.get_top()[1] < mn.title.get_bottom()[1] - 0.04, (mn.front.get_top(), mn.title.get_bottom())
        assert mn.label.get_bottom()[1] > mn.frame.get_bottom()[1] + 0.05, mn.label.get_bottom()
        assert mn.frame.get_bottom()[1] > t.box.get_top()[1] + 0.1, mn.frame.get_bottom()
        assert mn.frame.get_right()[0] < SAFE_X, mn.frame.get_right()
        assert mn.vol.get_top()[1] < mn.front.get_bottom()[1] - 0.05 and mn.vol.get_bottom()[1] > mn.api.get_top()[1] + 0.05
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(pa, pb, bh, bf, bo)), FadeOut(sh), run_time=0.5)
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(t, shift=UP * 0.2), FadeIn(mn), run_time=0.6)
            strip_flash(self, mn.api.frame, mn.api.name, OWN, run_time=0.7)
            vo.wait_until("in a new terminal")
            self.play(Indicate(t.title, color=TURN), run_time=0.6)
            self.add(t)
            vo.wait_until("step 1")
            type_capture(self, t, D01, type_time=0.6)
            cd_prompt(self, t, P_V2_REACT)
            vo.wait_until("and run docker-shell.sh")
            self.play(track(trk, 2), run_time=0.4)
            type_capture(self, t, D02, type_time=0.5)
            vo.wait_until("It mounts your code")
            self.play(FadeIn(pd, shift=UP * 0.15), FadeIn(mn.front, shift=LEFT * 0.2), run_time=0.5)
            marks = VGroup()
            for k, phrase, colour in ((5, "It mounts your code", OWN), (6, "keeps node modules", SHARED),
                                      (7, "publishes 3000", ROUTE), (8, "and joins the network", NET)):
                vo.wait_until(phrase)
                b = line_bar(pd.code, k, colour, opacity=0.22)
                marks.add(b)
                self.play(FadeIn(b), run_time=0.35)
                self.add(pd, marks)
                if k == 6:
                    self.play(FadeIn(mn.vol, shift=UP * 0.1), run_time=0.5)
                if k == 7:
                    self.play(code_span(pd.code, 7, "-p 3000:5173").animate.set_color(ROUTE), run_time=0.3)
                    self.add(pd, marks)
                    self.play(FadeIn(mn.door), Create(mn.tunnel), FadeIn(mn.port), run_time=0.6)
                    self.play(mn.door.animate(rate_func=there_and_back).scale(1.15), run_time=0.5)
                if k == 8:
                    self.play(code_span(pd.code, 8, "--network cheese-app-network").animate.set_color(NET),
                              Create(mn.stub), run_time=0.6)
                    self.add(pd, marks)
                    self.play(Indicate(mn.cable, color=NET, scale_factor=1.03), Indicate(mn.label, color=NET),
                              run_time=0.6)
            vo.wait_until("Pause and run it")
            turn6 = bar_tag(self, t, turn_row())
            flash_tag(self, turn6, TURN)
            self.add(t)

        # ========================================================== 7. the banner: Node, npm, up to date
        first = grey_chip("your first run: a full install into the volume · docker-entrypoint.dev.sh:8")
        with self.voiceover(SAY[7]) as vo:
            clear_bar(self, t, FadeOut(VGroup(pd, marks)),
                      FadeOut(VGroup(mn, mn.front, mn.door, mn.tunnel, mn.port, mn.stub, mn.vol)))
            resize(self, t, 10, run_time=0.5)
            o7 = out(self, t, [D02.line(2), cut(D02.line(3), "FINISHED"), "…", *D02.at((21, 24))], run_time=0.6)
            vo.wait_until("Node and npm")
            pin(self, o7[5], beside(time_row(), o7[5], buff=0.5))
            self.play(Indicate(o7[5].glyphs, color=TURN, scale_factor=1.03), Indicate(o7[6].glyphs, color=TURN, scale_factor=1.03),
                      run_time=0.7)
            self.add(t)
            vo.wait_until("Your first run installs")
            o7b = out(self, t, [D02.line(25), (D02.line(27), TURN)], run_time=0.5)
            under_term(t, first, buff=0.14)
            assert first.get_top()[1] < TRACK_BOTTOM - 0.05 and first.get_left()[0] > -SAFE_X, first.get_top()
            self.play(FadeIn(first, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("ours was already up to date")
            self.play(Indicate(o7b[1], color=TURN, scale_factor=1.06), run_time=0.7)
            self.add(t)
            out(self, t, D02.at((29, 33)), wrap=True, run_time=0.6)

        # ========================================================== 8. step 2: npm run dev; two addresses inside; use 3000
        fr8 = VGroup(mn.door.copy(), mn.tunnel.copy(), mn.front.copy(), mn.port.copy())
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(first), track(trk, 3), run_time=0.5)
            vo.wait_until("npm run dev")
            type_at(self, t, D02, 35, type_time=0.5)
            vo.wait_until("Vite is ready")
            o8 = out(self, t, [*D02.at((37, 38)), (D02.line(80), TOOL)], run_time=0.5)
            self.play(Indicate(o8[2], color=TOOL, scale_factor=1.05), run_time=0.6)
            self.add(t)
            vo.wait_until("and prints two addresses on 5173")
            o8b = out(self, t, D02.at((82, 83)), run_time=0.5)
            self.play(*[substring(r, ":5173").animate.set_color(ROUTE) for r in o8b], run_time=0.4)
            self.add(t)
            vo.wait_until("both are inside the container")
            gl = VGroup(*[r.glyphs for r in o8b])
            br8 = Brace(gl, RIGHT, color=S.GREY, buff=0.15)
            bt8 = label("inside the container", 20, S.GREY).next_to(br8, RIGHT, buff=0.15)
            assert bt8.get_right()[0] < t.box.get_right()[0] - 0.1, bt8.get_right()
            self.play(GrowFromCenter(br8), FadeIn(bt8, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("so on your laptop, use 3000")
            fr8.shift(np.array([0, t.box.get_top()[1] + 0.2 - fr8.get_bottom()[1], 0]))
            assert fr8.get_top()[1] < TRACK_BOTTOM - 0.05, fr8.get_top()
            self.play(FadeIn(fr8, shift=DOWN * 0.1), run_time=0.5)
            self.play(fr8[0].animate(rate_func=there_and_back).scale(1.2).set_stroke(ROUTE, width=5),
                      Indicate(fr8[3], color=ROUTE, scale_factor=1.2), run_time=0.9)
            vo.wait_until("Pause and start it")
            turn8 = bar_tag(self, t, turn_row())
            flash_tag(self, turn8, TURN)
            self.add(t)

        # ========================================================== 9. step 3: open localhost 3000: one div, one script
        tab = term(P_LAPTOP, rows=5, title=T_TAB, size=20)
        br9 = Browser("localhost:3000", win_w=5.0, win_h=3.3)
        br9.move_to([-3.5, 0, 0]).align_to([0, PIC_TOP - 0.05, 0], UP)
        ill9 = illustration_tag().next_to(br9.frame, RIGHT, buff=0.2).align_to(br9.frame, UP)
        assert br9.get_bottom()[1] > tab.box.get_top()[1] + 0.1, (br9.get_bottom(), tab.box.get_top())
        rb = DashedVMobject(Rectangle(width=br9.page.width - 0.4, height=br9.page.height - 0.4,
                                      stroke_color=S.GREY, stroke_width=2.5), num_dashes=40)
        rb.move_to(br9.page)
        rlab = mono('div id="root"', 20, S.GREY).next_to(rb.get_corner(UL), DR, buff=0.2)
        scr = file_card("/src/main.jsx").next_to(br9.frame, RIGHT, buff=0.9)
        scr.shift(UP * (rb.get_y() - scr.get_y() - 0.2))
        assert scr.get_right()[0] < SAFE_X - 0.05, scr.get_right()
        fill9 = root_fill(rb, rlab.get_bottom()[1] - 0.1)
        assert fill9.get_top()[1] < rlab.get_bottom()[1] - 0.04, (fill9.get_top(), rlab.get_bottom())
        with self.voiceover(SAY[9]) as vo:
            clear_bar(self, t, FadeOut(VGroup(br8, bt8, fr8)))
            self.play(FadeOut(t), track(trk, 4), run_time=0.5)
            self.play(FadeIn(br9, shift=RIGHT * 0.2), FadeIn(ill9), FadeIn(tab, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("open localhost 3000")
            self.play(br9.flash(ROUTE), Indicate(br9.address, color=ROUTE, scale_factor=1.1), run_time=0.6)
            br9.heal(self)
            l3 = type_capture(self, tab, D03, type_time=0.8)[0]
            bar_tag(self, tab, extra_row())
            vo.wait_until("The HTML is almost empty")
            o9 = out(self, tab, D03.at(2, 23, 26, 27), run_time=0.5)
            vo.wait_until("one div called root")
            recolor(self, o9[2], '<div id="root"></div>', TURN)
            self.add(tab)
            self.play(Create(rb), FadeIn(rlab), run_time=0.6)
            vo.wait_until("and a script, main dot jsx")
            recolor(self, o9[3], "/src/main.jsx", TURN)
            self.add(tab)
            self.play(FadeIn(scr, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("The whole app is one page")
            arr9 = Arrow(scr.get_left(), rb.get_right() + LEFT * 0.05, buff=0.08, color=S.GREY, stroke_width=4,
                         tip_length=0.18)
            self.play(GrowArrow(arr9), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(m, shift=DOWN * 0.08) for m in fill9], lag_ratio=0.3), run_time=0.9)
            edges9 = [m.copy().set_fill(opacity=0) for m in fill9]
            self.play(*[e.animate(rate_func=there_and_back).set_stroke(TOOL, width=6) for e in edges9], run_time=0.6)
            self.remove(*edges9)
        del l3

        # ========================================================== 10. extra: every address, the same HTML
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(br9, ill9, rb, rlab, scr, arr9, fill9)), track(trk, 4, extra=True), run_time=0.5)
            clear_bar(self, tab)
            clear_lines(self, tab, run_time=0.3)
            resize(self, tab, 8, run_time=0.5)
            vo.wait_until("An extra check")
            type_capture(self, tab, D08, type_time=1.4)
            bar_tag(self, tab, extra_row())
            vo.wait_until("every address")
            o10 = out(self, tab, D08_ROWS, run_time=0.7)
            self.play(*[substring(r, "200 text/html").animate.set_color(TURN) for r in o10], run_time=0.5)
            self.add(tab)
            vo.wait_until("even one that does not exist")
            self.play(Indicate(substring(o10[4], "/nope"), color=TURN, scale_factor=1.2), run_time=0.7)
            self.add(tab)
            vo.wait_until("The browser picks the page")
            clear_bar(self, tab)
            resize(self, tab, 2, run_time=0.5)
            sh.shift(np.array([-sh.outline.get_x(), 0, 0]))
            sh.shift(UP * (tab.box.get_top()[1] + 0.12 - sh.outline.get_bottom()[1]))
            assert sh.bar.get_top()[1] < PIC_TOP + 0.05 and sh.outline.get_bottom()[1] > tab.box.get_top()[1], sh.get_top()
            self.play(FadeIn(sh), run_time=0.5)
            for path, page in (("/podcasts", "Podcasts"), ("/newsletters", "Newsletters"),
                               ("/chat?model=llm", "Chat"), ("/nope", "Not found")):
                route_to(self, sh, path, page, run_time=0.45)
                self.wait(0.15)
            self.play(Indicate(sh.mid_text, color=ERR, scale_factor=1.1), run_time=0.6)
            sh.heal(self)

        self.play(FadeOut(sh), FadeOut(tab), FadeOut(trk), run_time=0.7)
        self.wait(0.3)
