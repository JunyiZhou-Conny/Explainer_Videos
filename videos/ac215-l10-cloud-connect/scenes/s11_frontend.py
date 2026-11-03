"""S11 · One server, two addresses (AC215 L10) — tracker D1 → D4, `lref("4, 7–9")` the whole scene.
Terminals at 20 pt (72 columns): 51's npm run dev output is 14 rows under its command, so the
terminal grows to 15 rows (top 2.86, under the tracker's 2.96).

Beats (script.md, ## S11; one voiceover block each):
0. TRACKER D1 (tracker D appears). A 8-row terminal at P_FRONTEND types `sh docker-shell.sh`
   (README.md line 161) → TERM(50: 3, …, 9, …, 19; build rows squashed, 9 and 19 cut with the house
   '…' after `node:20-alpine` / the image name); `▶ your turn` on the bar; `node:20-alpine` ringed;
   the root prompt `d263d94eb5c2:/app#` returns bare. The terminal shrinks to a 3-row strip and
   CODE(frontend-ai-chatbot/docker-shell.sh: 8–11, 20 pt, line 11 cut after `-p 3200:3000`) shows
   above it with `-p 3200:3000` highlighted; the prompt's '#' flashes.
1. TRACKER D2. The terminal grows; `npm install` (README.md line 167) → TERM(50: 22–26, …, 28; wrap),
   deprecation lines GREY, line 28 ringed with `at the time of recording`, `▶ your turn` beside the
   command. V3 echo over a 3-row strip: `node_modules/` appears in /app and rides the mount tube to
   the host folder. A straight cut (no `exit`, no second shell typed): the prompt becomes
   `6c23fe52ca92:/app#` under a GREY card (our capture: a fresh session per step; the README's one
   session works the same). TRACKER D3: `npm run dev` (README.md line 168) → TERM(51: 23–36; the
   telemetry lines 31–33 cut with the house '…', 31–34 GREY); line 26 `at the time of recording`;
   line 27 ringed RED-dashed, 'the container's view'; line 36 GREEN; `▶ your turn` on both commands.
2. TRACKER D4 · extra. A second 14-row terminal (P_FRONTEND): (a) 53 (fold) with a YELLOW '?' held
   2 s, → 53:2 RED; (b) 52 (folds) → 52:2–3 GREEN; (c) 55 (folds) → 55:2 GREEN. Then (D4) the README
   card (line 177) with `▶ your turn`, a schematic browser at `localhost:3200` (`illustration`) and
   the GREY caption quoting README.md · lines 179–180.
3. V4 part 2: PortDoor('3200', '3000'); the tunnel plays, the number morphs at the door; the ear and
   the browser flash; two address notes (localhost:3200 outside, localhost:3000 inside). TRACKER D4 ·
   extra: a 3-row strip types `docker ps` → TERM(54: 2–3) as its PORTS and NAMES columns (see
   deviations), the `0.0.0.0:3200->3000/tcp` cell ringed.
4. The 0–65535 number line: system (22, 80, 443), registered (3000, 3200, 8000, 9000), dynamic note.
5. The honest beat: CODE(api-service/docker-entrypoint.sh: 6–9; 7 and 8 cut after `--host 0.0.0.0`),
   'listen: every side of the container'; the TEAL API house with its loop and street-side door: a
   PINK packet arrives at the door, the ear on the loop alone stays deaf, it widens to every side and
   the packet is heard. Right: the 54 cell, 'publish: every side of the laptop'. Then the map
   (AppMap.at("S11"); the frontend lights and door 3200 opens: S12's starting state) with the Wi-Fi
   street and reach lines; a GREY neighbour walks up to door 9000; `-p 127.0.0.1:9000:9000` bricks
   up its Wi-Fi side; GREY caption 'port_toy (L04) wrote 127.0.0.1:'. Fade to an empty frame.

Deviations: 54's row is shown as its PORTS and NAMES columns only (`cols(…, ["PORTS", "NAMES"])`):
IMAGE + PORTS + NAMES is 103 characters (IMAGE equals NAMES here); 51:31–33 are cut with '…' rather
than wrapped so 26/27 stay on screen with 36. The map's Wi-Fi reach line under door 9000 crosses
the floor label 'localhost · 127.0.0.1': the scene draws its own reach segments around the label.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (ERR, IMAGE, INK, LAPTOP, NARRATION, P_FRONTEND, PASS, ROUTE, SAY_COUNT, T_SECOND,
                    TURN, AppMap, PortDoor, PortLine, bare_prompt, beside, bricks, capture, card, check_mark,
                    chip, code, code_span, cols, cut, door_glyph, each, extra_row, flash_tag, folder_glyph,
                    house, illustration_tag, istep, label, line_bar, lref, mono, note, on_bar, out,
                    person_icon, pin, readme, readme_card, resize, ring, route, squash, substring, term,
                    time_row, track, tracker, travel, turn_row, type_cmd, unpin, your_turn, browser_glyph,
                    outline_box, bounce, MONO)
from explainer import style as S

SAY = NARRATION["S11"]
SIZE = 20                       # the scene's terminals: 72 columns
SHELL = "cheese-app-v0/frontend-ai-chatbot/docker-shell.sh"
ENTRY = "cheese-app-v0/api-service/docker-entrypoint.sh"


# ------------------------------------------------------------------ local helpers
def clear_but(scene, *keep, anims=(), run_time: float = 0.6):
    """Plays: everything on screen fades except the families of `keep` (the tracker may have been
    split into parts by track()), then `keep` is re-added whole. Same as S09's."""
    ids = {id(f) for k in keep for f in k.get_family()}
    gone = [x for x in scene.mobjects if not any(id(f) in ids for f in x.get_family())]
    scene.play(FadeOut(Group(*gone)), *anims, run_time=run_time)
    scene.remove(*gone)
    scene.add(*keep)


def recolor(rows, color):
    """Animation: the glyphs of terminal rows `rows` take `color`."""
    return AnimationGroup(*[r.glyphs.animate.set_color(color) for r in rows])


def drop(scene, *mobs, anims=(), run_time: float = 0.3):
    """Plays: free overlays (rings, bar tags) fade and leave the scene."""
    scene.play(FadeOut(VGroup(*mobs)), *anims, run_time=run_time)
    scene.remove(*mobs)


def wipe(scene, t, run_time: float = 0.4):
    """Plays: every row of terminal t fades (the straight cut); the box stays."""
    rows = list(t.lines.submobjects)
    scene.play(FadeOut(VGroup(*rows)), run_time=run_time)
    for r in rows:
        t.lines.remove(r)
        scene.remove(r)


def mount_echo() -> VGroup:
    """S04's portal, small: the host folder (GREY) and the container's /app (TEAL) joined by the
    bind-mount tube (docker-shell.sh line 11's `-v` argument over it). .host .cont .tube .nm_c .nm_h"""
    hf = VGroup(folder_glyph(0.34, LAPTOP), mono("frontend-ai-chatbot/", SIZE, INK)).arrange(RIGHT, buff=0.15)
    hcap = label("your laptop", SIZE, LAPTOP)
    host_box = outline_box(4.4, 2.0, LAPTOP, solid=True, fill_opacity=0.05)
    VGroup(hcap, hf).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(host_box).align_to(host_box, UP) \
        .shift(DOWN * 0.25).align_to(host_box, LEFT).shift(RIGHT * 0.3)
    host = VGroup(host_box, hcap, hf).move_to([-3.9, 0.75, 0])
    cf = VGroup(folder_glyph(0.34, IMAGE), mono("/app/", SIZE, INK)).arrange(RIGHT, buff=0.15)
    ccap = label("container", SIZE, IMAGE)
    cont_box = outline_box(3.4, 2.0, IMAGE, solid=True, fill_opacity=0.08)
    VGroup(ccap, cf).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to(cont_box).align_to(cont_box, UP) \
        .shift(DOWN * 0.25).align_to(cont_box, LEFT).shift(RIGHT * 0.3)
    cont = VGroup(cont_box, ccap, cf).move_to([4.4, 0.75, 0])
    a, b = hf.get_right() + RIGHT * 0.25, cf.get_left() + LEFT * 0.25
    core = Line(a, b, color=LAPTOP, stroke_width=5)
    glow = core.copy().set_stroke(LAPTOP, 14, opacity=0.18)
    vtext = mono('-v "$(pwd)/:/app/"', SIZE, S.GREY).next_to(core, UP, buff=0.18)
    tube = VGroup(glow, core, vtext)
    nm_c = VGroup(folder_glyph(0.3, IMAGE), mono("node_modules/", SIZE, INK)).arrange(RIGHT, buff=0.12)
    nm_c.next_to(cf, DOWN, buff=0.22).align_to(cf, LEFT).shift(RIGHT * 0.35)
    nm_h = VGroup(folder_glyph(0.3, LAPTOP), mono("node_modules/", SIZE, INK)).arrange(RIGHT, buff=0.12)
    nm_h.next_to(hf, DOWN, buff=0.22).align_to(hf, LEFT).shift(RIGHT * 0.35)
    g = VGroup(host, cont, tube)
    g.host, g.cont, g.tube, g.nm_c, g.nm_h, g.core = host, cont, tube, nm_c, nm_h, core
    return g


def page_skeleton(br) -> VGroup:
    """GREY placeholder bars inside the schematic page (no text, no logo)."""
    rows = VGroup()
    for w in (2.6, 4.2, 3.6, 4.0):
        rows.add(RoundedRectangle(width=w, height=0.18, corner_radius=0.06, stroke_width=0)
                 .set_fill(S.GREY_DARK, 1))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    rows.next_to(br.url, DOWN, buff=0.4).align_to(br.window, LEFT).shift(RIGHT * 0.45)
    return rows


def api_house() -> VGroup:
    """The honest beat's API house: its own loop (127.0.0.1) on the left, a street-side door on the
    right, the name in the roof. .body .roof .name .loop .door"""
    h = house(None, 3.6, 2.1, lit=True)
    name = label("API", SIZE, INK).move_to(h.roof.get_center() + UP * 0.02)
    lp = Arc(radius=0.2, start_angle=-PI / 2 + 0.5, angle=2 * PI - 1.0, color=INK, stroke_width=3)
    lp.add_tip(tip_length=0.12, tip_width=0.12)
    lt = mono("127.0.0.1", SIZE, INK)
    loop = VGroup(lp, lt).arrange(DOWN, buff=0.1)
    loop.move_to(h.body.get_center()).align_to(h.body, LEFT).shift(RIGHT * 0.3)
    d = door_glyph(0.42, 0.62).move_to(h.body.get_bottom(), aligned_edge=DOWN).align_to(h.body, RIGHT) \
        .shift(LEFT * 0.35)
    g = VGroup(h, name, loop, d)
    g.body, g.roof, g.name, g.loop, g.door = h.body, h.roof, name, loop, d
    return g


def ear(around, buff: float = 0.18) -> VGroup:
    """The server's ear: a TEAL dashed outline around what it listens on."""
    r = RoundedRectangle(width=around.width + 2 * buff, height=around.height + 2 * buff, corner_radius=0.2)
    r.move_to(around)
    d = DashedVMobject(r, num_dashes=int((r.width + r.height) * 6), dashed_ratio=0.55).set_stroke(IMAGE, 4)
    return d


def reach_segments(m, w, port: str, skip=None) -> VGroup:
    """Door `port`'s Wi-Fi reach as GREY dashed segments, broken around mobject `skip` (the floor
    label) so no line runs through text."""
    ln = w.reach[port]
    x, top, bot = ln.get_start()[0], ln.get_start()[1], ln.get_end()[1]
    if skip is None or not (skip.get_left()[0] - 0.05 < x < skip.get_right()[0] + 0.05):
        return VGroup(DashedLine([x, top, 0], [x, bot, 0], color=S.GREY, stroke_width=2.5))
    a, b = skip.get_top()[1] + 0.08, skip.get_bottom()[1] - 0.08
    return VGroup(DashedLine([x, top, 0], [x, a, 0], color=S.GREY, stroke_width=2.5),
                  DashedLine([x, b, 0], [x, bot, 0], color=S.GREY, stroke_width=2.5))


class FrontendPorts(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S11"] == 6, len(SAY)

        # ========================================================== 0. D1: the frontend's shell
        tr = tracker("D", 1)
        ref = lref("4, 7–9")
        sh = capture("50")
        assert sh.cmd == readme(161) == "sh docker-shell.sh", sh.cmd
        p21, typed21 = sh.istep(21)
        assert (p21, typed21) == ("d263d94eb5c2:/app#", "npm install") and typed21 == readme(167)
        build = squash(sh.at(3, "…", 9, "…", 19))
        build[2] = cut(build[2], "node:20-alpine")
        build[4] = cut(build[4], "llm-rag-analysis-frontend-ai-chatbot")
        t = term(P_FRONTEND, rows=8, size=SIZE)
        yt0 = turn_row()
        panel = code(SHELL, 8, 11, font_size=SIZE, cuts={11: "-p 3200:3000"}).move_to([0, 0.75, 0])
        bar11 = line_bar(panel.code, 3, TURN)
        p_flag = code_span(panel.code, 3, "-p 3200:3000")

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(t, shift=UP * 0.2), run_time=0.8)
            first = bare_prompt(self, t)
            vo.wait_until("open a new terminal in the frontend folder")
            self.play(Indicate(substring(first, "frontend-ai-chatbot"), color=LAPTOP, scale_factor=1.08),
                      run_time=0.8)
            vo.wait_until("Run its shell script")
            type_cmd(self, t, sh.cmd, type_time=0.6)
            on_bar(t, yt0)
            self.play(FadeIn(yt0, shift=LEFT * 0.1), run_time=0.4)
            out(self, t, build, run_time=0.8)
            t.set_prompt(p21)
            root = bare_prompt(self, t)
            vo.wait_until("pause and do it")
            flash_tag(self, yt0, TURN)
            vo.wait_until("The image holds just Node")
            r9 = t.find("node:20-alpine")
            g9 = ring(substring(r9, "node:20-alpine"), TURN, buff=0.05)
            self.play(Create(g9), run_time=0.5)
            self.play(Indicate(substring(r9, "node:20-alpine"), color=INK, scale_factor=1.12), run_time=0.7)
            vo.wait_until("so you run npm yourself")
            drop(self, g9, yt0)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(panel, shift=DOWN * 0.2), run_time=0.6)
            self.play(FadeIn(bar11), Indicate(p_flag, color=TURN, scale_factor=1.12), run_time=0.8)
            vo.wait_until("the hash sign means you are root")
            hash_ = substring(root, "#")
            g_hash = ring(hash_, TURN, buff=0.06)
            self.play(Create(g_hash), Indicate(hash_, color=TURN, scale_factor=1.5), run_time=0.8)

        # ========================================================== 1. D2 + D3: npm install, npm run dev
        dev = capture("51")
        p51, typed51 = dev.istep(21)
        assert (p51, typed51) == ("6c23fe52ca92:/app#", "npm run dev") and typed51 == readme(168)
        inst = [(s, S.GREY) for s in sh.at((22, 26))] + ["…", sh.line(28)]
        dev_lines = dev.at((23, 36))
        for k in (31, 32, 33):                                   # telemetry prose: the house '…'
            dev_lines[k - 23] = cut(dev.line(k), {31: "anonymous telemetry", 32: "roadmap",
                                                  33: "how to opt-out"}[k])
        colours = {k: S.GREY for k in (31, 32, 33, 34)}
        colours[36] = PASS
        dev_items = [(s, colours[k]) if k in colours else s for k, s in zip(range(23, 37), dev_lines)]
        echo = mount_echo()
        fresh = card(["our capture: a fresh session for each step",
                      "one session (the README's way) works the same:",
                      "node_modules is on your disk"], size=SIZE).move_to([0, 0.9, 0])
        yt1, yt2, tm1, tm2 = turn_row(), turn_row(), time_row(), time_row()

        with self.voiceover(SAY[1]) as vo:
            drop(self, panel, bar11, g_hash, anims=[track(tr, 2)], run_time=0.5)
            resize(self, t, 15, keep=1, run_time=0.6)
            ln_i = istep(self, t, sh.line(21), type_time=0.5)
            beside(yt1, ln_i)
            pin(self, ln_i, yt1)
            out(self, t, inst, wrap=True, run_time=0.9)
            r28 = t.find("added 773 packages")
            vo.wait_until("773 packages")
            g28 = ring(substring(r28, "added 773 packages"), TURN, buff=0.05)
            beside(tm1, r28)
            self.play(Create(g28), FadeIn(tm1, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("plus deprecation warnings")
            self.play(each([t.find("rimraf@3.0.2"), t.find("glob@7.2.3")], INK, scale=1.05), run_time=0.8)
            vo.wait_until("They land in your folder")
            drop(self, g28, tm1)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(echo.host), FadeIn(echo.cont), run_time=0.5)
            self.play(Create(echo.tube[:2]), FadeIn(echo.tube[2]), run_time=0.6)
            self.play(FadeIn(echo.nm_c, shift=DOWN * 0.15), run_time=0.4)
            dot = Dot(echo.core.get_end(), radius=0.09, color=INK)
            self.play(FadeIn(dot, scale=0.5), run_time=0.2)
            self.play(MoveAlongPath(dot, Line(echo.core.get_end(), echo.core.get_start())), run_time=0.7)
            self.play(FadeOut(dot), FadeIn(echo.nm_h, shift=DOWN * 0.15), run_time=0.4)
            vo.wait_until("so our capture could step out")
            wipe(self, t)
            t.set_prompt(p51)
            bare_prompt(self, t)
            self.play(FadeOut(VGroup(echo, echo.nm_c, echo.nm_h)), FadeIn(fresh, shift=DOWN * 0.2), run_time=0.6)
            self.remove(echo, echo.nm_c, echo.nm_h)
            self.play(Indicate(fresh.body[2], color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("Then npm run dev")
            self.play(track(tr, 3), run_time=0.4)
            ln_d = istep(self, t, dev.line(21), type_time=0.4)    # typed in the strip: the card stays up
            drop(self, fresh, run_time=0.3)
            resize(self, t, 15, keep=1, run_time=0.5)
            beside(yt2, ln_d)
            pin(self, ln_d, yt2)
            out(self, t, dev_items, run_time=1.0)
            r26, r27, r36 = t.find("Next.js 14.2.4"), t.find("- Local:"), t.find("Ready in 1648ms")
            vo.wait_until("The Next.js server says ready")
            self.play(Indicate(r36.glyphs, color=PASS, scale_factor=1.08), run_time=0.7)
            vo.wait_until("version 14.2.4")
            g26 = ring(substring(r26, "Next.js 14.2.4"), TURN, buff=0.05)
            beside(tm2, r26)
            self.play(Create(g26), FadeIn(tm2, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("prints the line that fools everyone")
            g27 = ring(substring(r27, "http://localhost:3000"), ERR, buff=0.06, dashed=True)
            view = note("the container's view", ERR, SIZE)
            beside(view, r27)
            self.play(Create(g27), FadeIn(view, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("local, localhost 3000")
            self.play(Indicate(substring(r27, "localhost:3000"), color=ERR, scale_factor=1.15), run_time=0.8)
            vo.wait_until("Pause and run both")
            flash_tag(self, yt2, TURN)        # (npm install's tag went with the straight cut)

        # ========================================================== 2. D4 · extra: three angles
        c53, c52, c55 = capture("53"), capture("52"), capture("55")
        assert c53.cmd == "curl -sS --max-time 10 http://localhost:3000/", c53.cmd
        assert c55.cmd.startswith("docker exec llm-rag-analysis-frontend-ai-chatbot wget"), c55.cmd
        t2 = term(P_FRONTEND, rows=14, size=SIZE, title=T_SECOND)
        xt2 = extra_row()
        q = label("?", 44, TURN)
        br = browser_glyph(url="localhost:3200", glyph_w=6.4, glyph_h=3.0, name="your browser")
        br.move_to([-1.2, -0.75, 0])
        bars = page_skeleton(br)
        ill = illustration_tag().next_to(br.window, UP, buff=0.12).align_to(br.window, RIGHT)
        rc = readme_card(177, readme(177), size=SIZE)
        rc.move_to([-6.3 + rc.width / 2, 2.15, 0])
        yt3 = your_turn().next_to(rc, RIGHT, buff=0.3)
        quote = readme(180).lstrip("> ").strip()
        assert quote == "Use Chrome browser for best performance.", quote
        chrome = VGroup(note(f"README.md · lines 179–180: “{quote}”", S.GREY, SIZE),
                        note("likely inherited from the hosted L05 site", S.GREY, SIZE)) \
            .arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(br, DOWN, buff=0.15).align_to(br.window, LEFT)

        with self.voiceover(SAY[2]) as vo:
            clear_but(self, tr, ref, anims=[track(tr, 4, extra=True)], run_time=0.6)
            on_bar(t2, xt2)
            self.play(FadeIn(t2, shift=UP * 0.2), FadeIn(xt2, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("First, predict")
            la = type_cmd(self, t2, c53.cmd, type_time=0.7)
            q.next_to(la.rows[-1] if hasattr(la, "rows") else la, RIGHT, buff=0.4)
            vo.wait_until("will localhost 3000 answer")
            self.play(FadeIn(q, scale=0.6), run_time=0.4)
            self.play(q.animate(rate_func=there_and_back).scale(1.2), run_time=0.8)
            self.wait(0.8)                                                  # the prediction is held
            vo.wait_until("No, it fails to connect")
            self.play(FadeOut(q), run_time=0.3)
            self.remove(q)
            out(self, t2, c53.at(2), wrap=True, color=ERR, run_time=0.5)
            vo.wait_until("From your laptop, localhost 3200")
            type_cmd(self, t2, c52.cmd, type_time=0.9)
            out(self, t2, c52.at((2, 3)), color=PASS, run_time=0.4)
            self.play(Indicate(t2.find("<title>RAG App</title>").glyphs, color=PASS, scale_factor=1.1), run_time=0.6)
            vo.wait_until("And from inside the container")
            type_cmd(self, t2, c55.cmd, type_time=0.8)
            r55 = out(self, t2, c55.at(2), color=PASS, run_time=0.3)[0]
            vo.wait_until("answers with the same page")
            self.play(Indicate(r55.glyphs, color=PASS, scale_factor=1.1), run_time=0.7)
            vo.wait_until("Now open localhost 3200")
            clear_but(self, tr, ref, anims=[track(tr, 4, extra=False)], run_time=0.5)
            self.play(FadeIn(rc, shift=DOWN * 0.15), FadeIn(br, shift=UP * 0.15), FadeIn(ill), run_time=0.7)
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bars], lag_ratio=0.2), FadeIn(yt3),
                      run_time=0.8)
            vo.wait_until("the README suggests Chrome")
            self.play(FadeIn(chrome, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Pause and look")
            flash_tag(self, yt3, TURN)

        # ========================================================== 3. the tunnel; docker ps
        pd = PortDoor("3200", "3000", "frontend").move_to([0, 0.95, 0])
        c54 = capture("54")
        assert c54.cmd == "docker ps", c54.cmd
        ps_rows = cols(c54.at((2, 3)), ["PORTS", "NAMES"])
        strip = term(P_FRONTEND, rows=3, size=SIZE, title=T_SECOND)
        a_out = mono("localhost:3200", SIZE, LAPTOP).next_to(pd.browser, DOWN, buff=0.15)
        a_in = mono("localhost:3000", SIZE, IMAGE).next_to(pd.ear, DOWN, buff=0.12)
        xt3 = extra_row()

        with self.voiceover(SAY[3]) as vo:
            clear_but(self, tr, ref, run_time=0.5)
            self.play(FadeIn(pd, scale=0.95), run_time=0.7)
            vo.wait_until("The flag dash p")
            dt = pd.door.text
            self.play(each([dt[0:4], dt[5:9]], TURN, scale=1.3, lag=0.5), run_time=1.0)
            vo.wait_until("means host port 3200 forwards")
            arrived = pd.tunnel(self, run_time=2.0)
            vo.wait_until("to container port 3000")
            self.play(Indicate(arrived.text, color=INK, scale_factor=1.2), run_time=0.7)
            vo.wait_until("The Next server listens on 3000")
            self.play(Indicate(pd.ear.text, color=IMAGE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("inside its own house")
            self.play(Indicate(pd.house.text, color=INK, scale_factor=1.15), run_time=0.7)
            vo.wait_until("your browser knocks on 3200")
            self.play(Indicate(pd.browser.window, color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("One server, two addresses")
            self.play(FadeIn(a_out, shift=UP * 0.1), FadeIn(a_in, shift=UP * 0.1), run_time=0.6)
            self.play(each([a_out, a_in], INK, scale=1.12, lag=0.4), run_time=0.9)
            vo.wait_until("An extra docker ps")
            self.play(FadeIn(strip, shift=UP * 0.2), track(tr, extra=True), run_time=0.5)
            lp = type_cmd(self, strip, c54.cmd, type_time=0.4)
            beside(xt3, lp)
            pin(self, lp, xt3)
            out(self, strip, ps_rows, run_time=0.4)
            cell = substring(strip.find("0.0.0.0:3200->3000/tcp"), "0.0.0.0:3200->3000/tcp")
            g_cell = ring(cell, TURN, buff=0.05)
            self.play(Create(g_cell), Indicate(pd.door.text, color=TURN, scale_factor=1.15), run_time=0.7)

        # ========================================================== 4. the number line
        pl = PortLine().move_to([0, 0.1, 0])
        pl.dynamic_note.shift(DOWN * 0.38)        # (common.py: it sits on the '65535' end label)

        with self.voiceover(SAY[4]) as vo:
            clear_but(self, tr, ref, anims=[track(tr, extra=False)], run_time=0.5)
            self.play(FadeIn(pl, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("The low ones belong to the system")
            self.play(Indicate(pl.bands[0].name, color=INK, scale_factor=1.12), pl.drop(0), run_time=0.9)
            vo.wait_until("like 80 and 443")
            self.play(each([pl.chips[0][1], pl.chips[0][2]], INK, scale=1.15, lag=0.4), run_time=0.8)
            vo.wait_until("Pick yours from the middle band")
            self.play(Indicate(pl.bands[1].name, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("3000, 3200, 8000, and 9000")
            self.play(pl.drop(1, run_time=1.4))
            vo.wait_until("The top band holds")
            self.play(pl.note_in(), Indicate(pl.bands[2].name, color=INK, scale_factor=1.12), run_time=0.8)

        # ========================================================== 5. 0.0.0.0 twice; the Wi-Fi side
        ep = code(ENTRY, 6, 9, cuts={7: "--host 0.0.0.0", 8: "--host 0.0.0.0"}).move_to([0, 1.45, 0])
        host_span = code_span(ep.code, 1, "--host 0.0.0.0")
        cap_listen = note("listen: every side of the container", IMAGE, SIZE)
        ah = api_house().move_to([-3.0, -1.55, 0])
        small = ear(ah.loop)
        wide = ear(VGroup(ah.body, ah.loop), buff=0.12)
        cap_listen.next_to(wide, DOWN, buff=0.15)
        ear_t1 = label("listens: loop only", SIZE, IMAGE).next_to(ah.roof, UP, buff=0.12)
        ear_t2 = label("listens: 0.0.0.0", SIZE, IMAGE).move_to(ear_t1)
        tun_a = ah.door.get_right() + np.array([2.0, -0.05, 0])
        tun = route(tun_a, ah.door.get_right() + RIGHT * 0.06)
        cell_txt = "0.0.0.0:3200->3000/tcp"
        assert cell_txt in c54.line(3)
        pub = chip(cell_txt, S.GREY, size=22, font=MONO).move_to([3.7, -0.9, 0])
        cap_pub = note("publish: every side of the laptop", LAPTOP, SIZE).next_to(pub, DOWN, buff=0.2)
        m = AppMap.at("S11")
        wf = m.wifi()
        reach = {p: reach_segments(m, wf, p, skip=m.loop[1]) for p in ("8000", "3200", "9000")}
        nb = person_icon(S.GREY, 0.5)
        nb_y = wf[0].get_bottom()[1] - 0.38              # the neighbour stands just below the Wi-Fi street
        nb.move_to([-4.2, nb_y, 0])
        x9 = m.doors["9000"].glyph.get_center()[0]
        r9 = reach["9000"]
        prefix = chip("-p 127.0.0.1:9000:9000", S.GREY, size=22, font=MONO)
        toy = note("port_toy (L04) wrote 127.0.0.1:", S.GREY, SIZE)
        VGroup(prefix, toy).arrange(RIGHT, buff=0.5).move_to([-1.0, -3.15, 0])
        wall = bricks(0.42, 0.34).move_to([x9, wf[0].get_center()[1], 0])     # on the Wi-Fi side only

        with self.voiceover(SAY[5]) as vo:
            clear_but(self, tr, ref, run_time=0.5)
            self.play(FadeIn(ep, shift=DOWN * 0.15), run_time=0.6)
            g_host = ring(host_span, TURN, buff=0.05)
            self.play(Create(g_host), run_time=0.5)
            self.play(FadeIn(pub, shift=LEFT * 0.15), run_time=0.5)
            self.play(each([host_span, pub.text[0:7]], TURN, scale=1.15, lag=0.5), run_time=1.0)
            vo.wait_until("Inside the container")
            self.play(FadeIn(ah, shift=UP * 0.15), run_time=0.5)
            self.play(Create(small), FadeIn(ear_t1), run_time=0.5)
            vo.wait_until("the tunnel arrives at the street side")
            pk = Dot(tun_a, radius=0.1, color=ROUTE)
            self.play(Create(tun), FadeIn(pk), run_time=0.5)
            self.play(MoveAlongPath(pk, Line(tun_a, ah.door.get_right() + RIGHT * 0.12)), run_time=0.6)
            vo.wait_until("not at the loopback")
            self.play(pk.animate.set_color(S.GREY), Indicate(small, color=S.GREY, scale_factor=1.05), run_time=0.6)
            vo.wait_until("so the API server listens on every side")
            self.play(Transform(small, wide), FadeOut(ear_t1, shift=UP * 0.1), FadeIn(ear_t2, shift=UP * 0.1),
                      run_time=0.8)
            self.remove(ear_t1)
            ok = check_mark(0.3, PASS).next_to(ah.door, UP, buff=0.12)
            self.play(pk.animate.set_color(ROUTE).move_to(ah.door.get_center()), Create(ok), FadeIn(cap_listen),
                      run_time=0.6)
            vo.wait_until("Docker publishes on every side of your laptop")
            self.play(FadeIn(cap_pub, shift=UP * 0.1), Indicate(pub.text, color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("unless you add a prefix")
            clear_but(self, tr, ref, run_time=0.5)
            self.play(FadeIn(m, scale=1.04), run_time=0.6)
            self.play(m.light("frontend"), m.open_door("3200"), run_time=0.7)
            vo.wait_until("The ports lecture wrote")
            self.play(FadeIn(toy, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("before its port")
            self.play(Indicate(toy, color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("but this app writes none")
            self.play(each([m.doors[p].text for p in ("8000", "3200", "9000")], INK, scale=1.15, lag=0.25),
                      run_time=0.9)
            vo.wait_until("So these doors face your Wi-Fi too")
            self.play(FadeIn(wf), *[Create(r) for r in reach.values()],
                      Indicate(m.loop[1], color=LAPTOP, scale_factor=1.05), run_time=0.9)
            vo.wait_until("and anyone on that network can knock")
            self.play(FadeIn(nb, shift=RIGHT * 0.2), run_time=0.4)
            self.play(nb.animate.move_to([x9, nb_y, 0]), run_time=1.0)
            self.play(bounce(nb, nb.get_center() + UP * 0.22), Indicate(m.doors["9000"].text, color=INK,
                      scale_factor=1.15), run_time=0.7)
            vo.wait_until("Adding 127.0.0.1 before the host port")
            self.play(FadeIn(prefix, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("before the host port")
            self.play(Indicate(prefix.text, color=INK, scale_factor=1.08), run_time=0.7)
            vo.wait_until("closes that side")
            self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.1) for b in wall], lag_ratio=0.05),
                      r9.animate.set_stroke(opacity=0.3), run_time=0.7)
            self.play(bounce(nb, nb.get_center() + UP * 0.22), run_time=0.6)
            self.play(nb.animate.shift(LEFT * 0.8), run_time=0.5)

        self.wait(0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
