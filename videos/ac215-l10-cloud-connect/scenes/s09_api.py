"""S09 · Run the API, and survive line 14 (AC215 L10) — tracker C1 → C4, no lecture tag (BRIEF);
the last scene of part 1. One 20 pt laptop terminal (72 columns: laptop/30's sed is 206 characters
with P_API, three rows; laptop/33's uvicorn lines 35/36 fit unwrapped), and a 20 pt second terminal.

Beats (script.md, ## S09; one voiceover block each):
0. TRACKER C1 (tracker C appears). The running map (AppMap.at("S09")) over a 3-row strip at
   P_LLMRAG; the API house flashes on "the API". `cd ../api-service` → the prompt changes. laptop/30's
   sed soft-wraps (its quoted argument is longer than a row; the rows join back to the command,
   asserted), GREY bar tag 'our editor; use yours' → TERM(30: 2–6; line 5, 73 wide, cut with the
   house '…'), line 4 `export GCP_PROJECT="your-gcp-project"` ringed GREEN. `▶ your turn` on the bar.
1. TRACKER C2. `sh docker-shell.sh` (README.md line 134) → TERM(31: 2; wrap) RED, `▶ your turn` on
   the bar. The API house stays dark (a RED flash on its name), the cheese-app street flashes on "the
   network already exists".
2. TRACKER C2 · extra. The map and strip leave. The `erratum` card: CODE(api-service/docker-shell.sh:
   3–14, 20 pt; the first window of 1–16: lines 1–2 are the shebang and a blank line) with line 14 RED
   and line 4 `set -e` YELLOW (its comment, line 3, flashes); a caption 'network exists → line 14
   fails → set -e stops the script'. Then the second window CODE(13–16) with line 14 RED, S05's sticky
   note 'inspect … || create' returns beside it from the top-right corner; a 4-row strip (the sed of
   laptop/32 needs four rows at 72 columns) soft-wraps the fix, bar tags 'our editor; use yours' +
   'extra' → TERM(32: 2; wrap). The resulting line is shown large (24 pt, broken at two spaces), GREEN,
   caption 'your new line 14', `▶ your turn` beside it; line 14 in the window is struck RED.
3. TRACKER C2. The strip grows to 11 rows; `sh docker-shell.sh` again (`▶ your turn` on the bar) →
   TERM(33: 2–3, …, 16, …, 26–32; squash on the build rows), line 3 `Building 188.2s` and line 16
   `RUN pipenv sync` ringed with `at the time of recording`; the help text (28–30) GREEN with
   `uvicorn_server` ringed; the prompt `(app) app@ed21c759d782:/app$`. TRACKER C3: `uvicorn_server`
   (README.md line 140) → TERM(33: 35–41); line 41 GREEN; line 36's `0.0.0.0` ringed GREY with 'hold
   0.0.0.0 for part 2' on the bar; `▶ your turn` beside the uvicorn_server row. The terminal shrinks
   to a 3-row strip under the map: the API house lights, the GREEN secrets tube draws into it, the
   GREY door 9000→9000 opens.
4. TRACKER C3 · extra. 'Application startup complete.' and the API house flash; a GREEN 'empty' note
   beside the drawer. A second terminal (`laptop · second terminal`, P_API, 5 rows) types laptop/37's
   curl (folds) with GOLD 'this bills your project' + 'extra' on its bar → TERM(37: 2, …, 8) RED.
   The server terminal returns (11 rows) → TERM(33: 46, …, 104–105, …, 143, …, 162; wrap): `500`
   ringed, the rag.py frame flashes, line 162 RED, the bearer line 143 YELLOW. The terminal shrinks
   to a 3-row strip under V1 (teaser, GREEN '/secrets/ · empty' over the key slot): the glass finds
   nothing, the chain greys again.
5. TRACKER C3. The chain rises; a GREY card `{"embedding": [` 256 thin BLUE bars `]}` (no values;
   a brace '256') with the tag `recorded · rag.py:218–223 · EMBEDDING_DIMENSION = 256 (rag.py:17)`;
   CODE(llm-rag/cli.py: 26) beside it, caption 'must match'. The whole chain lights at once and a
   GREEN `200` lands under the bearer ticket.
6. TRACKER C4. A README card (line 149) with `▶ your turn` and a schematic Swagger page (tag
   `illustration`, address `localhost:9000/docs`). TRACKER C4 · extra: a 3-row strip under it types
   laptop/34 (folds) → 34: 2, then laptop/35 (folds) → 35: 2 (`200` ringed). The page leaves, the
   strip grows to 7 rows; the route list (laptop/36, soft-wrapped: its quoted Python is longer than a
   row) → 36: 2–7 under a README card (README.md · lines 263–269, Method and Route columns); `GET /`
   ringed GREY ('not in the table').
7. End of part 1 on the map (AppMap.at("S09") with the API lit, its tube and door 9000): a GREY tag
   `recorded · rag.py:218–223`; a small GREEN badge rides the BLUE lane to Google's IAM door, the door
   opens (GREEN check); the API house glows. A YELLOW question card slides in: 'The API is up on your
   laptop. / How does a web page find it, and who else can?'. Fade to an empty frame (end of part 1).
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, IMAGE, INK, KEY, NARRATION, P_API, P_LLMRAG, PASS, ROUTE, SAY_COUNT,
                    T_LAPTOP, T_SECOND, TURN, AppMap, AuthChain, EmbeddingBars, bare_prompt, beside, capture,
                    card, cd_prompt, check_mark, code, code_span, cost_row, cut, editor_row, erratum_tag,
                    extra_row, flash_tag, folder_glyph, illustration_tag, istep, label, line_bar, mono,
                    note, on_bar, out, readme, readme_card, recorded_tag, resize, ring, room, row_tag,
                    squash, strike, substring, term, time_row, track, tracker, travel, turn_row, type_cmd,
                    browser_glyph, your_turn)
from explainer import style as S

SAY = NARRATION["S09"]
SIZE = 20                       # the scene's terminals: 72 columns
SHELL = "cheese-app-v0/api-service/docker-shell.sh"
CLI = "cheese-app-v0/llm-rag/cli.py"


# ------------------------------------------------------------------ local helpers
def soft_type(scene, t, cmd: str, type_time: float | None = None):
    """Type a command whose long quoted argument cannot fold at a space outside quotes: it
    soft-wraps at the terminal's edge, as a terminal shows a long typed line (the rows join back
    to exactly the prompt and the command). Same as S05's."""
    full = t.prompt + " " + cmd
    n = t.max_chars
    rows = [full[i:i + n] for i in range(0, len(full), n)]
    assert "".join(rows) == full and all(len(r) <= n for r in rows)
    assert len(rows) <= t.rows, (len(rows), t.rows)
    t.fold = lambda text, first_prefix=0: list(rows)
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


def clear_but(scene, *keep, anims=(), run_time: float = 0.6):
    """Plays: everything on screen fades except the families of `keep` (the tracker may have been
    split into parts by track()), then `keep` is re-added whole."""
    ids = {id(f) for k in keep for f in k.get_family()}
    drop = [x for x in scene.mobjects if not any(id(f) in ids for f in x.get_family())]
    scene.play(FadeOut(Group(*drop)), *anims, run_time=run_time)
    scene.remove(*drop)
    scene.add(*keep)


def recolor(rows, color):
    """Animation: the glyphs of terminal rows `rows` take `color`."""
    return AnimationGroup(*[r.glyphs.animate.set_color(color) for r in rows])


def drop(scene, *mobs, anims=(), run_time: float = 0.3):
    """Plays: free overlays (rings, bar tags) fade and leave the scene."""
    scene.play(FadeOut(VGroup(*mobs)), *anims, run_time=run_time)
    scene.remove(*mobs)


def sticky_note() -> VGroup:
    """S05's GREY sticky note of the idempotent shape."""
    return card([mono("inspect … || create", 22, INK), label("remember this shape", 22, S.GREY)])


def big_line(s: str, breaks=(" >/dev/null", " docker network create"), size: float = 24, color=PASS) -> VGroup:
    """laptop/32:2 shown large: the line broken into rows at the spaces before `breaks` (whitespace
    only: the rows joined with single spaces are the line)."""
    parts, rest = [], s
    for b in breaks:
        i = rest.index(b)
        parts.append(rest[:i])
        rest = rest[i + 1:]
    parts.append(rest)
    assert " ".join(parts) == s, parts
    return VGroup(*[mono(p, size, color) for p in parts]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)


def swagger_page() -> VGroup:
    """A schematic Swagger page (always tagged `illustration`): a browser window at
    localhost:9000/docs with GREY placeholder rows (no route names, no logo). .page .rows"""
    page = browser_glyph(url="localhost:9000/docs", glyph_w=4.6, glyph_h=3.2, name=None)
    rows = VGroup()
    for i in range(5):
        pill = RoundedRectangle(width=0.62, height=0.26, corner_radius=0.08, stroke_color=S.GREY,
                                stroke_width=2).set_fill(S.GREY, 0.25)
        bar = RoundedRectangle(width=2.7 - 0.25 * (i % 3), height=0.16, corner_radius=0.06,
                               stroke_width=0).set_fill(S.GREY_DARK, 1)
        rows.add(VGroup(pill, bar).arrange(RIGHT, buff=0.2))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    title = RoundedRectangle(width=1.9, height=0.22, corner_radius=0.06, stroke_width=0).set_fill(S.GREY, 0.6)
    body = VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
    body.next_to(page.url, DOWN, buff=0.3).align_to(page.window, LEFT).shift(RIGHT * 0.35)
    g = VGroup(page, body)
    g.page, g.rows = page, rows
    return g


def mini_badge(color=KEY) -> VGroup:
    """Our service account's badge, small enough to ride the map's lane (no text: the full badge()
    with the email is S03's)."""
    fr = RoundedRectangle(width=0.42, height=0.52, corner_radius=0.07, stroke_color=color,
                          stroke_width=3).set_fill(S.GREY_DARKER, 1)
    clip = RoundedRectangle(width=0.2, height=0.09, corner_radius=0.03, stroke_color=color,
                            stroke_width=2).set_fill(S.BG, 1).move_to(fr.get_top())
    face = Circle(radius=0.09, stroke_color=color, stroke_width=2.5).move_to(fr.get_center() + UP * 0.06)
    line_ = Line(LEFT * 0.12, RIGHT * 0.12, color=color, stroke_width=2.5).move_to(fr.get_center() + DOWN * 0.14)
    return VGroup(fr, clip, face, line_)


def routes_card() -> VGroup:
    """README.md lines 263–269 (the API Endpoints table): its Method and Route columns, as written
    (backticks dropped)."""
    rows = []
    for n in range(265, 270):
        cells = [c.strip().strip("`") for c in readme(n).strip("|").split("|")]
        rows.append((cells[0], cells[1]))
    w = max(len(m) for m, _ in rows)
    body = VGroup(*[mono(f"{m.ljust(w)}  {r}", 20, INK) for m, r in rows]).arrange(DOWN, aligned_edge=LEFT,
                                                                                  buff=0.1)
    return readme_card((263, 269), body, size=20)


class ApiService(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S09"] == 8, len(SAY)

        # ========================================================== 0. C1: the second project-name edit
        tr = tracker("C", 1)
        m = AppMap.at("S09")
        t = term(P_LLMRAG, rows=3, size=SIZE)
        sed = capture("30")
        assert sed.cmd.startswith("sed -i 's|export GCP_PROJECT=\"ac215-project\" # CHANGE TO YOUR PROJECT ID|")
        sed_lines = sed.at((2, 6))
        sed_lines[3] = cut(sed_lines[3], "llm-service-account")     # 30:5 is 73 wide: the house '…'
        ed0, yt0 = editor_row(), turn_row()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(m, scale=1.1), FadeIn(t, shift=UP * 0.2), run_time=0.9)
            vo.wait_until("the API")
            self.play(Indicate(m.houses["api"].text, color=INK, scale_factor=1.3), run_time=0.8)
            vo.wait_until("In the api-service folder")
            type_cmd(self, t, "cd ../api-service", type_time=0.6)
            cd_prompt(self, t, P_API)
            vo.wait_until("make the second project-name edit")
            soft_type(self, t, sed.cmd, type_time=2.0)
            on_bar(t, ed0)
            self.play(FadeIn(ed0, shift=LEFT * 0.1), run_time=0.4)
            out(self, t, sed_lines, chunk=3)
            row_gp = t.find('export GCP_PROJECT="your-gcp-project"')
            ring_gp = ring(row_gp.glyphs, PASS, buff=0.06)
            self.play(Create(ring_gp), run_time=0.5)
            vo.wait_until("Pause and do it")
            yt0.next_to(ed0, LEFT, buff=0.2)
            self.play(FadeIn(yt0, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt0, TURN)

        # ========================================================== 1. C2: sh docker-shell.sh dies
        sh31 = capture("31")
        assert sh31.cmd == readme(134) == "sh docker-shell.sh", sh31.cmd
        yt1 = turn_row()

        with self.voiceover(SAY[1]) as vo:
            drop(self, ring_gp, ed0, yt0, anims=[track(tr, 2)], run_time=0.5)
            vo.wait_until("Then the README's command")
            type_cmd(self, t, sh31.cmd, type_time=0.6)
            vo.wait_until("Pause and run it")
            on_bar(t, yt1)
            self.play(FadeIn(yt1, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt1, TURN)
            vo.wait_until("It dies at once")
            err_rows = out(self, t, sh31.at(2), wrap=True, color=ERR)
            self.play(Indicate(m.houses["api"].text, color=ERR, scale_factor=1.3),
                      Indicate(err_rows[0].glyphs[:13], color=ERR, scale_factor=1.1), run_time=0.8)
            vo.wait_until("the network already exists")
            self.play(Indicate(m.streets["cheese-app"].text, color=ROUTE, scale_factor=1.15),
                      Indicate(substring(err_rows[0], "cheese-app-network"), color=ROUTE, scale_factor=1.1),
                      run_time=0.9)
            self.play(Indicate(substring(err_rows[-1], "exists"), color=ERR, scale_factor=1.2), run_time=0.6)

        # ========================================================== 2. C2 · extra: line 14, set -e, the fix
        panel = code(SHELL, 3, 14, font_size=20).move_to([0, -0.3, 0])
        etag = erratum_tag()
        etag.move_to([panel.get_right()[0] - etag.width / 2, panel.get_top()[1] + 0.32, 0])
        kind = note("not your fault", S.GREY, 22).next_to(etag, LEFT, buff=0.3)
        bar14 = line_bar(panel.code, 11, ERR, opacity=0.28)
        red14 = ring(code_span(panel.code, 11, "docker network create cheese-app-network"), ERR)
        bar4 = line_bar(panel.code, 1, TURN, opacity=0.25)
        ring4 = ring(code_span(panel.code, 1, "set -e"), TURN)
        why = VGroup(label("network exists", 22, INK), label("→", 22, S.GREY), label("line 14 fails", 22, ERR),
                     label("→", 22, S.GREY), mono("set -e", 22, TURN), label("stops the script", 22, ERR))
        why.arrange(RIGHT, buff=0.18).next_to(panel, DOWN, buff=0.28)

        w14 = code(SHELL, 13, 16, font_size=20)
        w14.move_to([-6.45 + w14.width / 2, 1.85, 0])
        w_bar = line_bar(w14.code, 1, ERR, opacity=0.28)
        w_span = code_span(w14.code, 1, "docker network create cheese-app-network")
        sticky = sticky_note()
        sticky_from = sticky.copy().move_to([6.4 - sticky.width / 2, 1.75, 0])     # where S05 parked it
        sticky.move_to([6.4 - sticky.width / 2, w14.get_center()[1], 0])
        fix = capture("32")
        assert fix.cmd.startswith("sed -i 's|^docker network create cheese-app-network$|"), fix.cmd
        new14 = fix.at(2)[0]
        assert new14 == readme(74), (new14, readme(74))
        big = big_line(new14)
        new_cap = label("your new line 14", 24, PASS)
        yt2 = your_turn()
        ed2, xt2 = editor_row(), extra_row()

        with self.voiceover(SAY[2]) as vo:
            clear_but(self, tr, anims=[track(tr, extra=True)], run_time=0.6)
            self.play(FadeIn(panel, shift=UP * 0.2), FadeIn(etag, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("and not your fault")
            self.play(FadeIn(kind, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("Line 14 creates the network")
            self.play(FadeIn(bar14), Create(red14), run_time=0.6)
            vo.wait_until("and set dash e")
            self.play(FadeIn(bar4), Create(ring4), run_time=0.6)
            vo.wait_until("stops the script at the first error")
            self.play(Indicate(code_span(panel.code, 0, "exit immediately"), color=INK, scale_factor=1.08),
                      run_time=0.8)
            vo.wait_until("So it fails whenever")
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.1) for x in why], lag_ratio=0.25), run_time=1.2)
            vo.wait_until("even right after")
            self.play(Indicate(why[0], color=INK, scale_factor=1.12), run_time=0.8)
            vo.wait_until("The fix is the shape")
            self.play(FadeOut(VGroup(panel, bar14, red14, bar4, ring4, why, kind)),
                      etag.animate.next_to(w14, UP, buff=0.12).align_to(w14, RIGHT), run_time=0.6)
            self.remove(panel, bar14, red14, bar4, ring4, why, kind)
            self.play(FadeIn(w14, shift=DOWN * 0.15), FadeIn(w_bar), FadeIn(sticky_from, scale=1.1), run_time=0.6)
            self.play(Transform(sticky_from, sticky), run_time=0.7)
            t2 = term(P_API, rows=4, size=SIZE)
            on_bar(t2, ed2)
            xt2.next_to(ed2, LEFT, buff=0.2)
            vo.wait_until("make line 14 the README's")
            self.play(FadeIn(t2, shift=UP * 0.2), FadeIn(ed2), FadeIn(xt2), run_time=0.5)
            soft_type(self, t2, fix.cmd, type_time=2.2)
            new_rows = out(self, t2, fix.at(2), wrap=True)
            big.move_to([-6.2 + big.width / 2, -0.25, 0])
            new_cap.next_to(big, UP, buff=0.18).align_to(big, LEFT)
            self.play(FadeIn(big, target_position=new_rows.get_center(), scale=0.8),
                      Create(strike(w_span, ERR)), run_time=0.9)
            self.play(FadeIn(new_cap, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Pause and make that edit")
            yt2.next_to(big, RIGHT, buff=0.45)
            self.play(FadeIn(yt2, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt2, TURN)
            vo.wait_until("the sed is ours")
            flash_tag(self, ed2, INK)
            flash_tag(self, xt2, INK)

        # ========================================================== 3. C2 → C3: run again, uvicorn_server
        cap = capture("33")
        assert cap.cmd == readme(134), cap.cmd
        p34, typed34 = cap.istep(34)
        assert typed34 == readme(140) == "uvicorn_server", typed34
        yt3a, yt3b, tm = turn_row(), turn_row(), time_row()
        hold = row_tag("hold 0.0.0.0 for part 2", S.GREY)

        with self.voiceover(SAY[3]) as vo:
            clear_but(self, tr, t2, anims=[track(tr, 2, extra=False)], run_time=0.6)
            t = t2
            resize(self, t, 11, keep=2)
            vo.wait_until("Run the script again")
            type_cmd(self, t, cap.cmd, type_time=0.6)
            on_bar(t, yt3a)
            self.play(FadeIn(yt3a, shift=LEFT * 0.1), run_time=0.4)
            out(self, t, squash(cap.at(2, 3, "…", 16, "…")))
            r3, r16 = t.find("[+] Building 188.2s"), t.find("RUN pipenv sync")
            vo.wait_until("The first build installs")
            g16 = ring(substring(r16, "RUN pipenv sync"), TURN, buff=0.05)
            self.play(Create(g16), run_time=0.5)
            self.play(Indicate(substring(r16, "pipenv"), color=INK, scale_factor=1.2), run_time=0.7)
            vo.wait_until("which took about three minutes")
            g3 = ring(substring(r3, "Building 188.2s"), TURN, buff=0.05)
            self.play(Create(g3), run_time=0.5)
            vo.wait_until("at the time of recording")
            beside(tm, r16)
            self.play(FadeIn(tm, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, tm, INK)
            vo.wait_until("You land in the pipenv shell")
            drop(self, g16, g3, tm, yt3a)
            out(self, t, cap.at((26, 32)), run_time=0.8)
            t.set_prompt(p34)
            bare_prompt(self, t)
            help_rows = [t.find("The following commands are available:"), t.find("    uvicorn_server"),
                         t.find("Run the Uvicorn Server")]
            self.play(recolor(help_rows, PASS), run_time=0.5)
            g29 = ring(substring(help_rows[1], "uvicorn_server"), PASS, buff=0.05)
            self.play(Create(g29), run_time=0.4)
            vo.wait_until("Type uvicorn server")
            drop(self, g29, anims=[track(tr, 3)], run_time=0.4)
            uv = istep(self, t, cap.line(34), type_time=0.6)
            out(self, t, cap.at((35, 41)), run_time=0.8)
            r36, r41 = t.find("Uvicorn running on"), t.find("Application startup complete.")
            vo.wait_until("and the API starts on port 9000")
            self.play(recolor([r41], PASS), Indicate(substring(r36, "9000"), color=INK, scale_factor=1.25),
                      run_time=0.7)
            vo.wait_until("listening on 0.0.0.0")
            g36 = ring(substring(r36, "0.0.0.0"), S.GREY, buff=0.05)
            on_bar(t, hold)
            self.play(Create(g36), FadeIn(hold, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Pause and run both")
            beside(yt3b, uv)
            self.play(FadeIn(yt3b, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt3b, TURN)
        # the API is up: the strip and the map
        drop(self, g36, hold, yt3b)
        resize(self, t, 3, run_time=0.6)
        self.play(FadeIn(m, scale=1.05), run_time=0.6)
        self.play(m.light("api"), m.tube_on("api"), m.open_door("9000"), run_time=0.9)

        # ========================================================== 4. C3 · extra: green startup, a 500
        empty = note("empty", KEY, 22).next_to(m.drawer, RIGHT, buff=0.2)
        e37 = capture("37")
        assert e37.cmd == "curl -s -i 'http://localhost:9000/rag/embedding?text=hello'", e37.cmd
        t3 = term(P_API, rows=5, title=T_SECOND, size=SIZE)
        bill, xt4 = cost_row(), extra_row()
        on_bar(t3, bill)
        xt4.next_to(bill, LEFT, buff=0.2)
        chain = AuthChain(teaser=True)
        chain.shift(UP * 0.55)
        k0 = chain.slots[0].frame
        sec = VGroup(folder_glyph(0.26, KEY), mono("/secrets/", 22, KEY), note("empty", KEY, 22)).arrange(RIGHT,
                                                                                                     buff=0.15)
        sec.next_to(k0, UP, buff=0.2).align_to(k0, LEFT)

        with self.voiceover(SAY[4]) as vo:
            self.play(track(tr, extra=True), run_time=0.4)
            vo.wait_until("The server started cleanly")
            r41 = t.find("Application startup complete.")
            self.play(Indicate(r41.glyphs, color=PASS, scale_factor=1.06),
                      Indicate(m.houses["api"].text, color=INK, scale_factor=1.3), run_time=0.9)
            vo.wait_until("with an empty secrets folder")
            self.play(FadeIn(empty, shift=LEFT * 0.1), Indicate(m.drawer.text, color=KEY, scale_factor=1.15),
                      run_time=0.7)
            vo.wait_until("because the Google client")
            self.play(Circumscribe(m.houses["api"], color=TURN, buff=0.1, stroke_width=3), run_time=1.0)
            vo.wait_until("until its first request")
            self.play(Indicate(m.google.guard, color=CLOUD, scale_factor=1.2), run_time=0.8)
            vo.wait_until("In a second terminal")
            clear_but(self, tr, run_time=0.5)
            self.play(FadeIn(t3, shift=UP * 0.2), FadeIn(xt4), run_time=0.5)
            vo.wait_until("an extra curl asks for an embedding")
            type_cmd(self, t3, e37.cmd, type_time=1.2)
            self.play(FadeIn(bill, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, bill, COST)
            vo.wait_until("and gets a 500")
            r500 = out(self, t3, e37.at(2, "…", 8), color=ERR)
            g500 = ring(substring(r500[0], "500 Internal Server Error"), ERR, buff=0.05)
            self.play(Create(g500), run_time=0.5)
            vo.wait_until("The server log shows")
            clear_but(self, tr, run_time=0.4)
            self.play(FadeIn(t), run_time=0.4)
            resize(self, t, 11, run_time=0.6)
            out(self, t, cap.at(46, "…", (104, 105), "…", 143, "…", 162), wrap=True, run_time=1.0)
            r46 = t.find("500 Internal Server Error")          # 33:46 wraps after its request
            r104 = t.find('"/app/api/routers/rag.py", line 222')
            a143, b143 = t.find("http_request.headers['Authorization']"), t.find("{self._access_token()}'")
            a162 = t.find("google.auth.exceptions.DefaultCredentialsError")
            b162 = t.find("/secrets/llm-service-account.json was not found.")
            self.play(Indicate(substring(r46, "500"), color=ERR, scale_factor=1.4),
                      Indicate(substring(r104, "rag.py"), color=INK, scale_factor=1.2), run_time=0.8)
            vo.wait_until("the same default credentials error")
            self.play(recolor([a162, b162], ERR), run_time=0.5)
            self.play(Indicate(substring(a162, "DefaultCredentialsError"), color=ERR, scale_factor=1.1), run_time=0.7)
            vo.wait_until("raised while building the bearer header")
            self.play(recolor([a143, b143], TURN), run_time=0.5)
            self.play(Indicate(substring(a143, "f'Bearer"), color=CLOUD, scale_factor=1.2), run_time=0.7)
            vo.wait_until("A green startup")
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(chain, shift=UP * 0.2), FadeIn(sec), run_time=0.6)
            cross = chain.break_at(self, 0)

        # ========================================================== 5. with a real key: 256 floats, a 200
        bars = EmbeddingBars(256, bars_w=4.2, bar_h=0.55)
        open_ = mono('{"embedding": [', 22, INK)
        close_ = mono("]}", 22, INK)
        emb = VGroup(open_, bars, close_).arrange(RIGHT, buff=0.18)
        brace = Brace(bars, DOWN, buff=0.08, color=S.GREY)
        n256 = mono("256", 22, CLOUD).next_to(brace, DOWN, buff=0.08)
        rec_card = card([VGroup(emb, brace, n256)])
        rec_card.move_to([-2.05, -0.55, 0])
        rec = recorded_tag("recorded · rag.py:218–223 · EMBEDDING_DIMENSION = 256 (rag.py:17)")
        rec.next_to(rec_card.frame, DOWN, buff=0.15).align_to(rec_card.frame, LEFT)
        c26 = code(CLI, 26)
        c26.move_to([6.4 - c26.width / 2, rec_card.get_center()[1] + 0.25, 0])
        must = label("must match", 24, INK).next_to(c26, DOWN, buff=0.3)
        link = DashedLine(n256.get_right() + RIGHT * 0.15, must.get_left() + LEFT * 0.15, color=S.GREY,
                          stroke_width=2.5, dash_length=0.1)
        ok200 = VGroup(check_mark(0.3, PASS), mono("200", 26, PASS)).arrange(RIGHT, buff=0.12)
        frame200 = RoundedRectangle(width=ok200.width + 0.4, height=0.55, corner_radius=0.2, stroke_color=PASS,
                                    stroke_width=3).set_fill(S.BG, 1)

        with self.voiceover(SAY[5]) as vo:
            clear_but(self, tr, chain, anims=[FadeOut(VGroup(sec, cross)), track(tr, extra=False)], run_time=0.6)
            self.remove(sec, cross)
            self.play(chain.animate.shift(UP * 1.2), run_time=0.6)
            ok_pt = chain.slots[4].text.get_bottom() + DOWN * 0.75
            frame200.move_to(ok_pt)
            ok200.move_to(frame200)
            down = Arrow(chain.slots[4].text.get_bottom() + DOWN * 0.04, frame200.get_top() + UP * 0.02, buff=0,
                         color=PASS, stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.5)
            vo.wait_until("With a real key")
            self.play(FadeIn(rec_card.frame), FadeIn(open_), FadeIn(close_), FadeIn(rec, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("a list of 256 numbers")
            self.play(bars.grow(1.2), run_time=1.2)
            self.play(GrowFromCenter(brace), FadeIn(n256, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the embedding")
            flash_tag(self, rec, INK)
            vo.wait_until("That length must match the loader's")
            self.play(FadeIn(c26, shift=LEFT * 0.2), run_time=0.6)
            g26 = ring(code_span(c26.code, 0, "256"), CLOUD, buff=0.05)
            self.play(Create(g26), Create(link), FadeIn(must, shift=UP * 0.1), run_time=0.7)
            vo.wait_until("or the database queries fail")
            self.play(Indicate(must, color=INK, scale_factor=1.12), Indicate(n256, color=CLOUD, scale_factor=1.3),
                      run_time=0.8)
            vo.wait_until("And the whole chain lights up")
            self.play(chain.light_all(1.2), run_time=1.2)
            vo.wait_until("through to a 200")
            self.play(GrowArrow(down), FadeIn(VGroup(frame200, ok200), shift=DOWN * 0.15), run_time=0.6)
            self.play(Indicate(ok200[1], color=PASS, scale_factor=1.3), run_time=0.6)

        # ========================================================== 6. C4: /docs, and the routes
        c149 = readme_card(149, VGroup(label("Go to", 22, INK), mono("http://localhost:9000/docs", 22, INK),
                                       label("to see the API docs.", 22, INK)).arrange(RIGHT, buff=0.15))
        sw = swagger_page()
        ill = illustration_tag()
        yt6 = your_turn()
        t4 = term(P_API, rows=3, title=T_SECOND, size=SIZE)
        xt6 = on_bar(t4, extra_row())
        c34, c35, c36 = capture("34"), capture("35"), capture("36")
        assert c34.cmd == "curl -s http://localhost:9000/", c34.cmd
        assert c35.cmd.endswith("http://localhost:9000/docs"), c35.cmd
        assert c36.cmd.startswith("curl -s http://localhost:9000/openapi.json | python3 -c '"), c36.cmd
        rc = routes_card()

        with self.voiceover(SAY[6]) as vo:
            clear_but(self, tr, anims=[track(tr, 4)], run_time=0.6)
            sw.move_to([6.35 - sw.width / 2, 0.6, 0])
            ill.next_to(sw, UP, buff=0.12).align_to(sw, RIGHT)
            c149.move_to([-6.4 + c149.width / 2, 1.55, 0])
            yt6.next_to(c149, DOWN, buff=0.25).align_to(c149, LEFT)
            self.play(FadeIn(c149, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("open localhost 9000 slash docs")
            self.play(FadeIn(sw, scale=1.05), FadeIn(ill), run_time=0.7)
            self.play(Indicate(sw.page.url, color=INK, scale_factor=1.15),
                      Indicate(c149.body[1], color=INK, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Pause and look")
            self.play(FadeIn(yt6, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt6, TURN)
            vo.wait_until("Extra curls")
            self.play(FadeIn(t4, shift=UP * 0.2), FadeIn(xt6), track(tr, extra=True), run_time=0.5)
            type_cmd(self, t4, c34.cmd, type_time=0.5)
            out(self, t4, c34.at(2), run_time=0.3)
            vo.wait_until("show the docs page")
            type_cmd(self, t4, c35.cmd, type_time=0.9)
            r35 = out(self, t4, c35.at(2), run_time=0.3)[0]
            g35 = ring(substring(r35, "200 text/html"), PASS, buff=0.05)
            self.play(Create(g35), Indicate(sw.rows, color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("and the README's five routes")
            drop(self, g35, xt6, c149, yt6, sw, ill, run_time=0.4)
            resize(self, t4, 7, run_time=0.5)
            on_bar(t4, xt6)
            rc.move_to([-6.4 + rc.width / 2, t4.box.get_top()[1] + 0.2 + rc.height / 2, 0])
            self.play(FadeIn(rc, shift=DOWN * 0.15), FadeIn(xt6), run_time=0.5)
            soft_type(self, t4, c36.cmd, type_time=1.4)
            out(self, t4, c36.at((2, 7)), run_time=0.6)
            rows36 = [t4.find(f"{mth} {rt}") for mth, rt in (("GET", "/rag/embedding"), ("POST", "/rag/llm-response"),
                                                               ("GET", "/rag/agent_call"),
                                                               ("POST", "/rag/llm-agent-response"),
                                                               ("POST", "/rag/fine-tune-llm-response"))]
            self.play(LaggedStart(*[Indicate(r.glyphs, color=INK, scale_factor=1.05) for r in rows36],
                                  lag_ratio=0.2), Indicate(rc.body, color=INK, scale_factor=1.03), run_time=1.2)
            vo.wait_until("plus one more at the root")
            root = [r for r in t4.lines if getattr(r, "text", "") == "GET /"][-1]
            g_root = ring(root.glyphs, S.GREY, buff=0.06)
            nt = row_tag("not in the table", S.GREY)
            beside(nt, root, buff=0.3)
            self.play(Create(g_root), FadeIn(nt, shift=LEFT * 0.1), run_time=0.6)
            flash_tag(self, nt, INK)

        # ========================================================== 7. end of part 1
        m7 = AppMap.at("S09", lit=("chroma", "api"), doors=("8000", "9000"), tubes=("loader", "api"))
        rec7 = recorded_tag("recorded · rag.py:218–223")
        rec7.move_to([6.45 - rec7.width / 2, m7.get_top()[1] + 0.12 + rec7.height / 2, 0])
        lane = m7.call("api", "google")
        bdg = mini_badge().move_to(lane.path.get_start())
        door = m7.google.door
        ajar = door.frame.copy().stretch(0.25, 0, about_edge=LEFT).set_fill(CLOUD, 0.35)
        ok7 = check_mark(0.3, PASS).next_to(m7.google.guard, UP, buff=0.12)
        glow = m7.houses["api"].body.copy().set_stroke(IMAGE, 14, opacity=0.35).set_fill(opacity=0)
        q = card([label("The API is up on your laptop.", 26, INK),
                  label("How does a web page find it, and who else can?", 26, INK)], color=TURN)
        q.move_to([0, -2.45, 0])
        q_from = q.get_center() + DOWN * 1.2

        with self.voiceover(SAY[7]) as vo:
            clear_but(self, tr, anims=[track(tr, extra=False)], run_time=0.6)
            self.play(FadeIn(m7, scale=1.05), FadeIn(rec7, shift=LEFT * 0.15), run_time=0.8)
            vo.wait_until("the auth chain is now complete")
            self.play(FadeIn(bdg, scale=0.6), Create(lane), run_time=0.6)
            self.play(travel(bdg, lane.path, run_time=1.2))
            self.play(Transform(door.frame, ajar), FadeOut(door.knob), Create(ok7), run_time=0.6)
            vo.wait_until("and the API answers on your laptop")
            self.play(FadeIn(glow), Indicate(m7.houses["api"].text, color=INK, scale_factor=1.3), run_time=0.8)
            vo.wait_until("Leave it running")
            self.play(glow.animate(rate_func=there_and_back).set_stroke(width=24), run_time=1.0)
            vo.wait_until("Part 2 asks two questions")
            self.play(FadeIn(q, target_position=q_from), run_time=0.7)
            vo.wait_until("how does a web page find this API")
            self.play(Indicate(m7.browser.window, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("and who else can")
            self.play(Indicate(q.body[1], color=TURN, scale_factor=1.05), run_time=0.8)
        self.wait(1.0)                                   # the question stays a moment: end of part 1

        self.play(FadeOut(Group(*self.mobjects)), run_time=1.0)
        self.remove(*self.mobjects)
