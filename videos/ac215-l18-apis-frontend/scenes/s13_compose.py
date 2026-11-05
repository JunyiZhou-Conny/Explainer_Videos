"""S13 · One command, then clean up (AC215 L18, part 2). Tracker [S] "README › Tutorial: Setup & Run
Cheese App" 1 → 6, then [C2] "README › Docker Cleanup" 1 → 2 (· extra for e04). No lecture tag.

Beats (script.md "## S13", one voiceover block each):
0. TRACKER [S] 1. README card (README.md · line 193). A 10-row `laptop` terminal at ~/cheese-app-v2:
   f01's sed line (row tag "extra · or edit the file") and its `git diff src/docker-compose.yml`
   → f01: 7, 11–12, 16, 20–21; the two `+` lines GREEN, both flash on "It appears twice".
1. The terminal goes. CODE(src/docker-compose.yml) pages 7–10, 34–40, 55–63 (entrypoints elided),
   each service name TEAL and a TEAL chip for it in a row along the bottom (file order, the loader's
   slot left open); on "The loader first checks" the page 18–22 (comment cut, line 22 elided and cut)
   with line 22 YELLOW, the loader's chip fills its slot, and line 22 unfolds under the panel:
   "1 check  python cli.py --get …" / "2 only if that fails  || python cli.py --download --load …",
   with the YELLOW chip "check · load only if empty".
2. TRACKER [S] 2. README card (lines 198–199); a GREY chip "cd src/vector-db" over the terminal;
   prompt …/src/vector-db$ types `docker compose down` → f02: 2–7 (2–3 wrapped, GREY; a row tag
   "set by docker-shell.sh · harmless here" on the title bar), line 7 `Removed` flashes.
3. TRACKER [S] 3. Chip "cd ../.."; the prompt goes back to ~/cheese-app-v2, `cd src` → the prompt
   returns at …/src$. The card goes, the terminal grows to 12 rows. TRACKER [S] 4: `docker compose
   up --build`, ▶ your turn.
4. f04: 3, …, 66–68 (wrapped, ORANGE; row tag "warnings, not errors" on line 67), 69, 70–76 (cut
   after Built / Created); the four `Created` lines TEAL, flashed on "four containers are created".
5. The terminal shrinks to a 4-row strip; V2's laptop (S02's cluster on the laptop: NGINX, Cheese
   App, API Service, Vector DB) above it, right. f04: 98–99 → Vector DB lights GREEN; 109 (wrapped)
   → API Service; 118 → Cheese App; 124 → API Service flashes; 130 → NGINX's two arrows go and its box
   becomes a TEAL `vector-db-loader` that lights, then turns GREY "exited 0"; GREY chip "dev: no NGINX
   · nginx was the :prod image" left. Extra: the strip becomes a `second tab` (…/src$) and types
   f04-x-compose-ps → 2–6 (cut after the status), `Exited (0)` GREEN. Then a GREY README card
   (lines 210–211, 215–216) left.
6. TRACKER [S] 5. The tab: f04-curl-3000 → 2–3 (Cheese App flashes), f04-curl-api-docs → 2–3 (API
   Service flashes). README card (line 213) with `localhost:900` RED and the tag "erratum · use 9000";
   extra: f04-x-readme-url → 2 (wrapped, RED).
7. TRACKER [S] 6. The strip is the compose terminal again: f04: 142–151, each pair of `Stopped`
   lines darkens its box; `docker compose down` → f10: 8, 9, 13, 17, each `Removed` fades its box.
8. The laptop goes. TRACKER [C2] 1: chip "cd vector-db", prompt …/src/vector-db$, the strip grows to
   10 rows: `docker compose down` → e02:4 from "No resource found". Above, right: a GREEN
   `cheese-app-network` chip and an ORANGE "build cache" chip. TRACKER [C2] 2: `docker system prune`
   → e03: 2–6, 8, 9–10, …, 32 (line 7 blank, dropped); `[y/N] y` YELLOW, the network chip is struck
   and goes with `cheese-app-network`, the cache chip goes with `Total reclaimed space: 4.583GB` GREEN.
9. TRACKER [C2] 2 · extra. e04 (folds) → 3–6 (cut after the size), …, 13–14; `4.2GB` GOLD,
   `cheese-app-frontend-react-node_modules` ORANGE with the row tag "erratum · the cleanup misses it";
   two GREY chips `docker volume rm cheese-app-frontend-react-node_modules` · `docker image rm …`.
   Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S13"]

# ------------------------------------------------------------------ the real sources (checked)
F01 = capture("f01")
F02 = capture("f02")
F03 = capture("f03")
F04 = capture("f04-docker-compose-up")
F04_PS = capture("f04-x-compose-ps")
F04_3000 = capture("f04-curl-3000")
F04_DOCS = capture("f04-curl-api-docs")
F04_URL = capture("f04-x-readme-url")
F10 = capture("f10")
E02 = capture("e02")
E03 = capture("e03")
E04 = capture("e04")

assert F01.cmd_lines == ["sed -i 's/ac215-project/your-gcp-project/' src/docker-compose.yml",
                         "git diff src/docker-compose.yml"], F01.cmd_lines
assert F01.line(12).startswith("+") and F01.line(21).startswith("+") and "your-gcp-project" in F01.line(21)
assert F01.line(11).startswith("-") and F01.line(7).startswith("@@") and F01.line(16).startswith("@@")
assert F02.cmd == "docker compose down" and F02.line(7).strip() == "Container cheese-app-vector-db Removed"
assert "GOOGLE_APPLICATION_CREDENTIALS" in F02.line(2) and "GCP_PROJECT" in F02.line(3)
assert F03.cmd == "cd src" and F03.lines == []
assert F04.cmd == "docker compose up --build"
assert F04.line(3).startswith("[+] Building") and F04.line(66).startswith("WARN") and F04.line(68).startswith("WARN")
assert F04.line(69) == "[+] up 7/7"
assert all("Built" in F04.line(n) for n in (70, 71, 72)) and all("Created" in F04.line(n) for n in range(73, 77))
assert F04.line(98).endswith("Saving data to: /data") and "Uvicorn running on http://0.0.0.0:9000" in F04.line(109)
assert "VITE v8.3.5  ready" in F04.line(118) and F04.line(124).endswith("Application startup complete.")
assert F04.line(130) == "vector-db-loader-1 exited with code 0"
assert F04.line(142) == "^C" and F04.line(151) == "Container cheese-app-vector-db Stopped"
STOPPED = {146: "nginx", 147: "app", 149: "api", 151: "vdb"}   # the loader sits in NGINX's slot
assert "src-vector-db-loader-1 Stopped" in F04.line(146) and "frontend-react Stopped" in F04.line(147)
assert "api-service Stopped" in F04.line(149)
assert "Exited (0)" in F04_PS.line(6) and F04_PS.line(2).startswith("NAME")
assert F04_3000.at(2, 3) == ["HTTP/1.1 200 OK", "    <title>Formaggio</title>"]
assert "Swagger UI" in F04_DOCS.line(2) and F04_DOCS.line(3) == "[HTTP 200]"
assert "localhost:900/api/docs" in F04_URL.cmd and "Failed to connect to localhost:900" in F04_URL.line(2)
REMOVED = {8: "nginx", 9: "app", 13: "api", 17: "vdb"}
assert all(F10.line(n).rstrip().endswith("Removed") for n in REMOVED)
assert "No resource found" in E02.line(4)
assert E03.cmd == "docker system prune" and E03.line(8).endswith("[y/N] y") and E03.line(10) == "cheese-app-network"
assert E03.line(32) == "Total reclaimed space: 4.583GB" and E03.line(7) == ""
assert "cheese-app-api-service:latest" in E04.line(4) and "4.2GB" in E04.line(4)
assert E04.line(14).split() == ["local", "cheese-app-frontend-react-node_modules"]

COMPOSE = f"{V2}/src/docker-compose.yml"
for n, s in ((8, "vector-db:"), (19, "vector-db-loader:"), (34, "api-service:"), (55, "frontend-react:")):
    assert excerpt(COMPOSE, n, n).strip() == s, (n, excerpt(COMPOSE, n, n))
L22 = excerpt(COMPOSE, 22, 22)
CHECK = "python cli.py --get --chunk_type recursive-split > /dev/null 2>&1"
LOAD = "|| python cli.py --download --load --chunk_type recursive-split"
assert CHECK in L22 and LOAD in L22, L22
assert readme(193) == "Instead of three terminals, one command builds and starts the whole app."
R198 = " ".join([md_plain(readme(198)), md_plain(readme(199))])
assert R198.startswith("2. If any of the containers above are still running"), R198
R213 = md_plain(readme(213))
assert R213 == "4. Open http://localhost:3000. and http://localhost:900/api/docs.", R213


# ------------------------------------------------------------------ local helpers (as in S12)
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


def drop_bar_tag(scene, t: Terminal, run_time: float = 0.3):
    old = getattr(t, "bar_tag", None)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), run_time=run_time)
        scene.remove(old)
        t.bar_tag = None


def clear_lines(scene, t: Terminal, run_time: float = 0.3):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    if not gone:
        return
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
    scene.remove(*gone)


def recolor(scene, t: Terminal, row, sub: str, color, *extra, run_time: float = 0.35):
    """PLAYS: colour `sub` inside terminal row `row` (then re-seat the terminal)."""
    scene.play(substring(row, sub).animate.set_color(color), *extra, run_time=run_time)
    scene.add(t)


class LaptopMap(ArchitectureMap):
    """V2's cluster as S02 left it on the laptop (NGINX on top, Cheese App and API Service, Vector DB
    under the API; HTTP 3000 / 9000 beside NGINX, HTTP 8000 on the API's arrow), drawn directly as
    'your laptop' and compact enough (4.75 x 3.7) to sit over a 4-row strip. Only the 'cluster' layer."""

    BOX = {"nginx": (0.0, 0.8), "app": (-1.15, -0.25), "api": (1.15, -0.25), "vdb": (1.15, -1.3)}
    FRAME_H = 3.7

    def __init__(self, **kw):
        super().__init__(built=False, **kw)
        g = self._make("cluster")
        self.layers["cluster"] = g
        self.add(g)
        self.shown.append("cluster")

    def _make(self, name: str):
        if name != "cluster":
            return super()._make(name)
        sz, p = self.size, self.p
        fr = RoundedRectangle(width=4.75, height=self.FRAME_H, corner_radius=0.14, stroke_color=LAPTOP,
                              stroke_width=3).set_fill(S.BG, 1).move_to(p(0, 0))
        t = label("your laptop", 22, LAPTOP).next_to(fr.get_corner(UL), DR, buff=0.12)
        self.cluster_frame, self.cluster_title = fr, t
        for k, (x, y) in self.BOX.items():
            w = 1.4 if k == "nginx" else 1.8
            b = cbox([self.BOX_TEXT[k]], w, 0.58, size=sz, mono_font=False)
            b.name.move_to(b.frame)
            b.move_to(p(x, y))
            self.boxes[k] = b
        bx = self.boxes
        e1 = arrow(bx["nginx"].get_bottom() + LEFT * 0.4, bx["app"].get_top(), ROUTE, buff=0.04)
        e2 = arrow(bx["nginx"].get_bottom() + RIGHT * 0.4, bx["api"].get_top(), ROUTE, buff=0.04)
        e3 = arrow(bx["api"].get_bottom(), bx["vdb"].get_top(), ROUTE, buff=0.04)
        l1 = label("HTTP 3000", sz, ROUTE).next_to(bx["nginx"], LEFT, buff=0.12)
        l2 = label("HTTP 9000", sz, ROUTE).next_to(bx["nginx"], RIGHT, buff=0.12)
        l3 = label("HTTP 8000", sz, ROUTE).next_to(e3, LEFT, buff=0.12)
        self.ports = {"3000": l1, "9000": l2, "8000": l3}
        self.edges = (e1, e2, e3)
        return VGroup(fr, t, e1, e2, e3, *bx.values(), l1, l2, l3)


def lit(m: LaptopMap, key: str, color=OWN):
    """ANIM: a box lights (outline colour) and pulses."""
    b = m.boxes[key]
    return AnimationGroup(b.frame.animate.set_stroke(color, width=5),
                          Indicate(b.name, color=color, scale_factor=1.12))


class ComposeUp(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S13"] == 10, len(SAY)

        # ========================================================== 0. Step 1: project ID into the compose file
        trk = tracker_s(1)
        rc0 = readme_card(193, readme(193))
        rc0.move_to([0, 0, 0]).align_to([0, 2.75, 0], UP).align_to([-6.5, 0, 0], LEFT)
        t = term(P_V2, rows=10, title=T_LAPTOP, size=20)
        assert rc0.get_bottom()[1] > t.box.get_top()[1] + 0.15, (rc0.get_bottom(), t.box.get_top())
        assert rc0.get_top()[1] < TRACK_BOTTOM - 0.05 and rc0.get_right()[0] < SAFE_X, rc0.get_corner(UR)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(rc0, shift=DOWN * 0.15), run_time=0.7)
            self.play(Indicate(rc0.body, color=TURN, scale_factor=1.03), run_time=0.6)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("Step 1")
            self.play(Indicate(trk.caption, color=TURN, scale_factor=1.06), run_time=0.5)
            self.add(trk)
            sed, diff = type_capture(self, t, F01, type_time=0.8)
            bar_tag(self, t, extra_row("or edit the file"))
            o0 = out(self, t, [F01.line(7), F01.line(11), (F01.line(12), OWN), F01.line(16), F01.line(20),
                               (F01.line(21), OWN)], run_time=0.6)
            self.play(substring(o0[2], "your-gcp-project").animate.set_color(TURN),
                      substring(o0[5], "your-gcp-project").animate.set_color(TURN), run_time=0.4)
            self.add(t)
            vo.wait_until("It appears twice")
            self.play(Indicate(o0[2], color=OWN, scale_factor=1.03), Indicate(o0[5], color=OWN, scale_factor=1.03),
                      run_time=0.8)
            self.add(t)

        # ========================================================== 1. the four services; the loader checks first
        pages = {
            8: code(COMPOSE, 7, 10, font_size=20),
            34: code(COMPOSE, 34, 40, font_size=20, cuts={40: "api.service:app"},
                     elide={40: '"/bin/bash", "-c", "uv sync --frozen && '}),
            55: code(COMPOSE, 55, 63, font_size=20, elide={61: '"/bin/bash", "-c", "npm install --no-fund --no-audit && '}),
            19: code(COMPOSE, 18, 22, font_size=20, cuts={18: "then stops.", 22: "--get"},
                     elide={22: '"/bin/bash", "-c", '}),
        }
        first = {8: 7, 34: 34, 55: 55, 19: 18}
        names = {8: "vector-db", 19: "vector-db-loader", 34: "api-service", 55: "frontend-react"}
        for k, p in pages.items():
            p.align_to([-6.5, 0, 0], LEFT).align_to([0, 2.75, 0], UP)
            assert p.get_right()[0] < SAFE_X - 0.05 and p.get_bottom()[1] > -2.4, (k, p.get_corner(DR))
        chips = {k: box_chip(names[k]) for k in (8, 19, 34, 55)}
        row = VGroup(*[chips[k] for k in (8, 19, 34, 55)]).arrange(RIGHT, buff=0.3).move_to([0, -3.1, 0])
        assert row.width < 2 * SAFE_X - 0.2, row.width
        p19 = pages[19]
        # line 22 unfolded under its page: the check, and the load only if the check fails
        labs = VGroup(label("1 check", 24, TURN), label("2 else load", 24, TURN))
        cmds = VGroup(mono(CHECK, 20, INK), mono(LOAD, 20, INK))
        cmds.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        for lb, c in zip(labs, cmds):
            lb.move_to(c).align_to([0, 0, 0], LEFT)
        labs.next_to(cmds, LEFT, buff=0.3)
        for lb, c in zip(labs, cmds):
            lb.align_to(labs, LEFT).set_y(c.get_y())
        un = VGroup(VGroup(labs[0], cmds[0]), VGroup(labs[1], cmds[1]))
        un.next_to(p19, DOWN, buff=0.35).align_to(p19, LEFT)
        assert un.get_right()[0] < SAFE_X - 0.05, un.get_right()
        chk = chip("check · load only if empty", TURN, size=22)
        chk.next_to(un, DOWN, buff=0.3).align_to(un, LEFT)
        assert chk.get_bottom()[1] > row.get_top()[1] + 0.15, (chk.get_bottom(), row.get_top())
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(t), FadeOut(rc0), run_time=0.5)
            t.remove(t.bar_tag)                  # the 'extra · or edit the file' tag leaves with it
            t.bar_tag = None
            cur = None
            for k in (8, 34, 55):
                p = pages[k]
                span = code_span(p.code, k - first[k], names[k])
                if cur is None:
                    self.play(FadeIn(p, shift=RIGHT * 0.2), run_time=0.45)
                else:
                    self.play(FadeOut(cur), FadeIn(p, shift=UP * 0.15), run_time=0.45)
                self.play(span.animate.set_color(CONTAINER), run_time=0.25)
                self.add(p)
                self.play(TransformFromCopy(span, chips[k]), run_time=0.5)
                cur = p
            vo.wait_until("The loader first checks")
            self.play(FadeOut(cur), FadeIn(p19, shift=UP * 0.15), run_time=0.5)
            span = code_span(p19.code, 1, "vector-db-loader")
            self.play(span.animate.set_color(CONTAINER), run_time=0.25)
            self.add(p19)
            self.play(TransformFromCopy(span, chips[19]), run_time=0.5)
            bar22 = line_bar(p19.code, 4, TURN, opacity=0.25)
            self.play(FadeIn(bar22), FadeIn(chk, shift=LEFT * 0.15), run_time=0.5)
            self.add(p19, bar22)
            vo.wait_until("whether the books are already in Chroma")
            self.play(FadeIn(un[0], shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(un[0][1], color=OWN, scale_factor=1.03), run_time=0.6)
            vo.wait_until("and loads them only if not")
            self.play(FadeIn(un[1], shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(un[1][1], color=TURN, scale_factor=1.03), run_time=0.6)

        # ========================================================== 2. Step 2: compose down in src/vector-db
        body2 = "\n".join(soft([R198], 74))
        rc2 = readme_card((198, 199), body2, size=20)
        rc2.align_to([-6.5, 0, 0], LEFT).align_to([0, 2.75, 0], UP)
        t.set_prompt(P_V2_VDB)
        for ln in list(t.lines):           # the terminal is off screen: its rows go silently
            t.lines.remove(ln)
        cd2 = grey_chip("cd src/vector-db", mono_font=True)
        under_term(t, cd2)
        assert rc2.get_bottom()[1] > t.box.get_top()[1] + 0.25 and rc2.get_right()[0] < cd2.get_left()[0] - 0.2, \
            (rc2.get_corner(DR), cd2.get_left())
        assert rc2.get_right()[0] < SAFE_X - 0.05
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p19, bar22, chk, un, row)), run_time=0.5)
            self.play(track(trk, 2), FadeIn(rc2, shift=DOWN * 0.15), run_time=0.6)
            self.add(trk)
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(cd2, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("then docker compose down")
            bare_prompt(self, t)
            type_capture(self, t, F02, type_time=0.5)
            vo.wait_until("Compose warns about two unset variables")
            o2 = out(self, t, [(F02.line(2), S.GREY), (F02.line(3), S.GREY)], wrap=True, run_time=0.5)
            bar_tag(self, t, row_tag("set by docker-shell.sh · harmless here", S.GREY))
            o2b = out(self, t, F02.at((4, 7)), run_time=0.5)
            vo.wait_until("the shell scripts set them")
            self.play(Indicate(t.bar_tag.text, color=INK, scale_factor=1.08), run_time=0.6)
            self.add(t)
            # Indicate and set_color on the same glyphs in one play keep the old colour: two plays
            self.play(Indicate(o2b[3], color=CONTAINER, scale_factor=1.03), run_time=0.6)
            self.add(t)
            recolor(self, t, o2b[3], "Removed", CONTAINER, run_time=0.4)
        del o2

        # ========================================================== 3. Step 3: cd src; docker compose up --build
        cd3 = grey_chip("cd ../..", mono_font=True)
        under_term(t, cd3)
        with self.voiceover(SAY[3]) as vo:
            drop_bar_tag(self, t)
            self.play(track(trk, 3), FadeOut(rc2), ReplacementTransform(cd2, cd3), run_time=0.5)
            self.add(trk)
            cd_prompt(self, t, P_V2)
            vo.wait_until("change into src")
            type_capture(self, t, F03, type_time=0.4)
            cd_prompt(self, t, P_V2_SRC)
            self.play(FadeOut(cd3), run_time=0.3)
            clear_lines(self, t, run_time=0.3)
            resize(self, t, 12, run_time=0.5)
            vo.wait_until("and docker compose up with build")
            self.play(track(trk, 4), run_time=0.4)
            self.add(trk)
            up = type_capture(self, t, F04, type_time=0.6)[0]
            tn = beside(turn_row(), up, buff=0.4)
            assert tn.get_right()[0] < SAFE_X - 0.05, tn.get_right()
            vo.wait_until("Pause and run it")
            pin(self, up, tn)
            flash_tag(self, tn, TURN)

        # ========================================================== 5. Chroma, uvicorn, Vite; the loader exits 0
        m = LaptopMap()
        m.move_to([0, 0, 0])
        m.shift(np.array([SAFE_X - 0.1 - m.cluster_frame.get_right()[0], 2.78 - m.cluster_frame.get_top()[1], 0]))
        st_top = strip_top(4, 20)
        assert m.cluster_frame.get_bottom()[1] > st_top + 0.08, (m.cluster_frame.get_bottom(), st_top)
        x_left = m.cluster_frame.get_left()[0]
        nonginx = grey_chip("dev: no NGINX · nginx was the :prod image")
        nonginx.move_to([(-6.5 + x_left - 0.3) / 2, 2.3, 0])
        assert nonginx.get_left()[0] > -SAFE_X and nonginx.get_right()[0] < x_left - 0.15, nonginx.get_corner(DR)
        loader_txt = "vector-db-loader"
        tab = term(P_V2_SRC, rows=4, title=T_TAB, size=20)
        # README 210–211, 215–216: the two sentences the beat needs, quoted whole
        s210 = (md_plain(readme(210)) + " " + md_plain(readme(211)))
        s210 = s210[s210.index("Later runs"):]
        s215 = md_plain(readme(215)) + " " + md_plain(readme(216))
        s215 = s215[s215.index("To open a shell"):]
        assert s210 == "Later runs reuse the images and skip the load, because the books are already in Chroma.", s210
        assert s215.endswith("run its docker-shell.sh as before."), s215
        rc5 = readme_card((210, 211), "\n".join(soft([s210], 44) + soft([s215], 44)), size=20)
        new_head = label("· lines 210–211, 215–216", CAPTION, S.GREY).move_to(rc5.head[1], aligned_edge=LEFT)
        rc5.head.submobjects[1] = new_head
        rc5.move_to([(-6.5 + x_left - 0.25) / 2, 0, 0]).align_to([0, nonginx.get_bottom()[1] - 0.3, 0], UP)
        assert rc5.get_left()[0] > -SAFE_X and rc5.get_right()[0] < x_left - 0.1, (rc5.get_left(), rc5.get_right(), x_left)
        assert new_head.get_right()[0] < rc5.frame.get_right()[0] - 0.1
        assert rc5.get_bottom()[1] > st_top + 0.08 and rc5.get_top()[1] < TRACK_BOTTOM - 0.05, rc5.get_corner(UL)
        # ========================================================== 4. two warnings, four containers
        def cut_at(n, word):
            return cut(F04.line(n), word)
        with self.voiceover(SAY[4]) as vo:
            out(self, t, [F04.line(3), "…"], run_time=0.4)
            o4 = out(self, t, [(F04.line(66), SHARED), (F04.line(67), SHARED), (F04.line(68), SHARED)], wrap=True,
                     run_time=0.6)
            row67 = next(r for r in o4 if r.text.startswith("Set"))
            warn = beside(row_tag("warnings, not errors", SHARED), row67, buff=0.4)
            assert warn.get_right()[0] < SAFE_X - 0.05, warn.get_right()
            vo.wait_until("the network and the volume already exist")
            self.play(Indicate(substring(o4[0], "cheese-app-network"), color=SHARED, scale_factor=1.1), run_time=0.6)
            self.add(t)
            self.play(Indicate(substring(o4[-2], "cheese-app-frontend-react-node_modules")
                               if "node_modules" in o4[-2].text else o4[-2], color=SHARED, scale_factor=1.05),
                      run_time=0.6)
            self.add(t)
            vo.wait_until("They are warnings, not errors")
            pin(self, row67, warn)
            flash_tag(self, warn, SHARED)
            vo.wait_until("Then four containers are created")
            o4b = out(self, t, [F04.line(69), *[cut_at(n, "Built") for n in (70, 71, 72)],
                                *[(cut_at(n, "Created"), CONTAINER) for n in range(73, 77)]], run_time=0.8)
            self.play(LaggedStart(*[Indicate(r, color=CONTAINER, scale_factor=1.03) for r in o4b[4:]], lag_ratio=0.25),
                      run_time=1.2)
            self.add(t)
            # the log continues in a strip; V2's laptop comes in above it
            if rows_of(up)[-1] in t.lines:           # 'up' has scrolled off: its tag left with it
                unpin(self, up, tn)
            else:
                rows_of(up)[-1].remove(tn)
            resize(self, t, 4, run_time=0.5)
            self.play(FadeIn(m, shift=LEFT * 0.2), run_time=0.5)

        with self.voiceover(SAY[5]) as vo:
            vo.wait_until("Chroma")
            o5 = out(self, t, F04.at(98, 99), run_time=0.3, lag=0.04)
            self.play(lit(m, "vdb"), run_time=0.4)
            m.heal(self)
            vo.wait_until("uvicorn")
            out(self, t, [F04.line(109)], wrap=True, run_time=0.3, lag=0.04)
            self.play(lit(m, "api"), run_time=0.4)
            m.heal(self)
            vo.wait_until("and Vite start together")
            out(self, t, F04.at(118, 124), run_time=0.3, lag=0.04)
            self.play(lit(m, "app"), Indicate(m.boxes["api"].name, color=OWN, scale_factor=1.1), run_time=0.4)
            m.heal(self)
            vo.wait_until("and the loader exits with 0")
            o5b = out(self, t, [(F04.line(130), CONTAINER)], run_time=0.25)
            e1, e2, _ = m.edges
            m.drop(self, e1, e2, m.ports["3000"], m.ports["9000"], run_time=0.3)
            m.swap_box(self, "nginx", loader_txt, run_time=0.5)
            self.play(lit(m, "nginx"), run_time=0.4)
            m.heal(self)
            ex = label("exited 0", 20, S.GREY).next_to(m.boxes["nginx"], DOWN, buff=0.08)
            m.show(self, ex, run_time=0.5, extra=[m.boxes["nginx"].frame.animate.set_stroke(S.GREY, width=3),
                                                  m.boxes["nginx"].name.animate.set_color(S.GREY),
                                                  FadeIn(nonginx, shift=RIGHT * 0.15)])
            vo.wait_until("it found the books already loaded")
            self.play(Indicate(m.boxes["vdb"].name, color=OWN, scale_factor=1.12), FadeIn(rc5, shift=UP * 0.15),
                      run_time=0.6)
            m.heal(self)
            self.play(Indicate(rc5.body[0], color=TURN, scale_factor=1.03), run_time=0.6)
            # extra: docker compose ps from a second tab
            self.play(FadeOut(t), FadeIn(tab), run_time=0.4)
            bar_tag(self, tab, extra_row())
            type_capture(self, tab, F04_PS, type_time=0.6)
            o5c = out(self, tab, [cut(F04_PS.line(2), "STATUS")] +
                      [cut(F04_PS.line(n), "Up 9 seconds") for n in (3, 4, 5)] + [F04_PS.line(6).rstrip()],
                      run_time=0.6)
            recolor(self, tab, o5c[-1], "Exited (0)", OWN)
            self.wait(1.2)  # hold the Exited (0) proof before step 4 clears the tab
        del o5, o5b

        # ========================================================== 6. Step 4: open 3000 and the API docs; README says 900
        k6 = R213.index("http://localhost:900")
        body6 = VGroup(label(R213[:k6].rstrip(), 22, INK),
                       label(R213[k6:], 22, INK, t2c={"localhost:900/": ERR})).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        rc6 = readme_card(213, body6)
        er6 = erratum_tag("erratum · use 9000")
        rc6.move_to([(-6.5 + x_left - 0.25) / 2, 0.4, 0])
        er6.next_to(rc6.frame, UP, buff=0.12).align_to(rc6.frame, RIGHT)
        assert rc6.get_left()[0] > -SAFE_X and rc6.get_right()[0] < x_left - 0.1, (rc6.get_left(), rc6.get_right())
        assert er6.get_top()[1] < TRACK_BOTTOM - 0.05, er6.get_top()
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(nonginx), track(trk, 5), run_time=0.5)
            self.add(trk)
            clear_lines(self, tab, run_time=0.25)
            vo.wait_until("open localhost 3000")
            type_capture(self, tab, F04_3000, type_time=0.6)
            o6 = out(self, tab, F04_3000.at(2, 3), run_time=0.4)
            self.play(lit(m, "app", OWN), substring(o6[0], "200 OK").animate.set_color(OWN), run_time=0.6)
            m.heal(self)
            self.add(tab)
            vo.wait_until("and the API docs")
            clear_lines(self, tab, run_time=0.25)
            type_capture(self, tab, F04_DOCS, type_time=0.6)
            o6b = out(self, tab, F04_DOCS.at(2, 3), run_time=0.4)
            self.play(lit(m, "api", OWN), substring(o6b[1], "200").animate.set_color(OWN), run_time=0.6)
            m.heal(self)
            self.add(tab)
            vo.wait_until("A small slip")
            self.play(FadeOut(rc5), run_time=0.3)
            self.play(FadeIn(rc6, shift=UP * 0.15), FadeIn(er6, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("the README prints port 900")
            self.play(Indicate(body6, color=ERR, scale_factor=1.03), run_time=0.6)
            self.add(rc6)
            clear_lines(self, tab, run_time=0.2)
            type_capture(self, tab, F04_URL, type_time=0.6)
            out(self, tab, [(F04_URL.line(2), ERR)], wrap=True, run_time=0.4)
            vo.wait_until("use 9000")
            flash_tag(self, er6, INK)

        # ========================================================== 7. Step 5: Ctrl-C, docker compose down
        t.bar_tag = None
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(rc6, er6)), FadeOut(tab), FadeIn(t), track(trk, 6), run_time=0.5)
            self.add(trk)
            vo.wait_until("Control C")
            out(self, t, F04.at(142, 143), run_time=0.25)
            for chunk, keys in (((144, 147), ("nginx", "app")), ((148, 149), ("api",)), ((150, 151), ("vdb",))):
                out(self, t, F04.at(chunk), run_time=0.25, lag=0.04)
                self.play(*[m.dark(k, 0.5) for k in keys], run_time=0.25)
                m.heal(self)
            vo.wait_until("then docker compose down")
            clear_lines(self, t, run_time=0.25)
            type_capture(self, t, F10, type_time=0.4)
            self.wait(0.3)
            out(self, t, F10.at(*REMOVED), run_time=0.4, lag=0.04)
            vo.wait_until("removes all four containers")
            self.play(LaggedStart(*[m.dark(k, 0.7) for k in REMOVED.values()], lag_ratio=0.3), run_time=1.0)
            m.heal(self)

        # ========================================================== 8. Docker Cleanup: compose down in vector-db; system prune
        trk2 = tracker_c2(1)
        cd8 = grey_chip("cd vector-db", mono_font=True)
        net8 = ok_chip(NETWORK, mono_font=True)
        cache8 = chip("build cache", SHARED, size=20)
        with self.voiceover(SAY[8]) as vo:
            trk = swap_tracker(self, trk, trk2, FadeOut(m))
            clear_lines(self, t, run_time=0.25)
            resize(self, t, 10, run_time=0.5)
            under_term(t, cd8)
            VGroup(net8, cache8).arrange(RIGHT, buff=0.4).next_to(cd8, UP, buff=0.35).align_to(t.box, RIGHT)
            assert VGroup(net8, cache8).get_top()[1] < PIC_TOP, VGroup(net8, cache8).get_top()
            self.play(FadeIn(cd8, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("compose down in vector db")
            cd_prompt(self, t, P_V2_VDB)
            type_capture(self, t, E02, type_time=0.4)
            o8 = out(self, t, [from_phrase(E02.line(4), "No resource found")], run_time=0.4)
            vo.wait_until("finds nothing left")
            self.play(Indicate(o8[0], color=INK, scale_factor=1.03), run_time=0.6)
            self.add(t)
            vo.wait_until("Docker system prune")
            self.play(FadeOut(cd8), FadeIn(net8, shift=DOWN * 0.1), FadeIn(cache8, shift=DOWN * 0.1),
                      track(trk, 2), run_time=0.5)
            self.add(trk)
            type_capture(self, t, E03, type_time=0.5)
            o8b = out(self, t, E03.at((2, 6), 8), run_time=0.5)
            vo.wait_until("asks first")
            self.play(Indicate(substring(o8b[-1], "[y/N] y"), color=TURN, scale_factor=1.2), run_time=0.5)
            self.add(t)
            recolor(self, t, o8b[-1], "[y/N] y", TURN)
            vo.wait_until("then deletes the network")
            o8c = out(self, t, [E03.line(9), (E03.line(10), OWN)], run_time=0.4)
            st8 = strike(net8, ERR)
            self.play(Create(st8), run_time=0.4)
            self.play(FadeOut(VGroup(net8, st8), shift=UP * 0.1), Indicate(o8c[1], color=OWN, scale_factor=1.05),
                      run_time=0.5)
            self.add(t)
            vo.wait_until("about four and a half gigabytes")
            o8d = out(self, t, ["…", (E03.line(32), OWN)], run_time=0.4)
            self.play(FadeOut(cache8, scale=0.3), Indicate(substring(o8d[1], "4.583GB"), color=OWN,
                                                                         scale_factor=1.2), run_time=0.7)
            self.remove(cache8)
            self.add(t)

        # ========================================================== 9. extra: what prune leaves behind
        rm1 = grey_chip("docker volume rm cheese-app-frontend-react-node_modules", mono_font=True)
        rm2 = grey_chip("docker image rm …", mono_font=True)
        with self.voiceover(SAY[9]) as vo:
            clear_lines(self, t, run_time=0.3)
            self.play(track(trk, 2, extra=True), run_time=0.4)
            self.add(trk)
            type_capture(self, t, E04, type_time=0.7)
            o9 = out(self, t, [cut(E04.line(3), "DISK USAGE")] +
                     [cut(E04.line(n), sz) for n, sz in ((4, "4.2GB"), (5, "331MB"), (6, "94.8MB"))] +
                     ["…", E04.line(13), E04.line(14)], run_time=0.6)
            vo.wait_until("including the API's image")
            self.play(Indicate(substring(o9[1], "4.2GB"), color=COST, scale_factor=1.25), run_time=0.6)
            self.add(t)
            recolor(self, t, o9[1], "4.2GB", COST)
            self.play(Indicate(substring(o9[1], "cheese-app-api-service:latest"), color=COST, scale_factor=1.05),
                      run_time=0.5)
            self.add(t)
            vo.wait_until("and the node modules volume")
            recolor(self, t, o9[-1], "cheese-app-frontend-react-node_modules", SHARED, run_time=0.4)
            er9 = beside(row_tag("erratum · cleanup misses it", S.GREY), o9[-1], buff=0.3)
            assert er9.get_right()[0] < SAFE_X - 0.05, er9.get_right()
            pin(self, o9[-1], er9)
            vo.wait_until("Remove those by name")
            VGroup(rm1, rm2).arrange(DOWN, aligned_edge=RIGHT, buff=0.15).next_to(t.box, UP, buff=0.2) \
                .align_to(t.box, RIGHT)
            assert VGroup(rm1, rm2).get_top()[1] < TRACK_BOTTOM - 0.05, VGroup(rm1, rm2).get_top()
            self.play(FadeIn(rm1, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(rm2, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(rm1.text, color=INK, scale_factor=1.04), run_time=0.6)

        self.play(FadeOut(VGroup(rm1, rm2)), FadeOut(t), FadeOut(trk), run_time=0.7)
        self.wait(0.3)
