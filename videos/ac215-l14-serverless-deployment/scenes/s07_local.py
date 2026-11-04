"""S07 · Part 2: the prebuilt app on your laptop — tracker [2.1] 1 → 4; lecture slides 10, 14.

Beats (script.md "## S07"; one voiceover block each):
0. TRACKER [2.1] 1 (appears). LECTURE 14 · 10, 14. README card (README.md · lines 237–240): you
   already have a working containerized app; sharing localhost does not share it. The V1 grid icon
   lights its container cell (YELLOW).
1. Terminal `laptop` (20 pt, so README:246's first row fits unfolded) types the README's two-row
   `docker run --rm -p 8086:8080 \\ cgumb/…` (laptop/10:1–2); `▶ your turn` on the title bar. On
   "remove when done" `--rm` rings GREY; on "publish port" `-p 8086:8080` rings PINK and V5's door
   picture draws above the terminal: a GREY laptop wall, a PINK door 8086 piped to a container
   ear 8080.
2. The terminal grows; TERM(laptop/10: 3–5, …, 15–17 wrap); the digest YELLOW; a README card
   (README.md · line 1069) slides in right under it and the two digests light character by
   character, GREEN chip "same bytes, same digest"; GREY chip "linux/amd64 · Apple Silicon:
   emulated · Cloud Run needs amd64".
3. The terminal scrolls: TERM(laptop/10: 18–22 wrap); `http://0.0.0.0:8080` PINK + GREY row tag
   "every network interface"; GREY chip on line 22 "recent gunicorn (25.1 and later) · 26.2.0 at
   the time of recording" (on screen only); timestamps and PIDs unhighlighted.
4. The terminal shrinks and steps back; strip `laptop · second tab` (TRACKER [2.1] 1 · extra) types
   laptop/16's six command rows → TERM(laptop/16: 11–12, 17). The two output lines Transform into
   V5's CommandSlots (ENTRYPOINT [] GREY, CMD TEAL); a ghost "your arguments" chip slides into the
   CMD slot and reverts; YELLOW chip "part 4". The strip fades.
5. V5 part b: the slots become a small TEAL CMD chip at the top; CODE(__main__.py: 22–26) with
   line 23 (PORT) and line 24 (os.execvp) YELLOW; the PURPLE "python" process, the envelope
   PORT=8080 (image ENV) and the PINK ear 0.0.0.0:8080; python morphs into gunicorn; line 25's
   `--workers 1 --threads 4` GREEN and four slots appear.
6. TRACKER [2.1] 1 · extra. Strip: `docker top …` → TERM(laptop/13: 2, 3–4 from "{gunicorn}",
   cut after the gunicorn path) with `{gunicorn}` YELLOW; `docker ps --format …` → TERM(laptop/12:
   2–3 wrap), `0.0.0.0:8086->8080/tcp` PINK, the door returns; `curl -sS http://localhost:8080/`
   → TERM(laptop/14: 2 wrap) RED; a knock on the wall at 8080 bounces, "refused".
7. TRACKER [2.1] 2. The drawn page (illustration) at http://localhost:8086 (README:251); strip
   (TRACKER [2.1] 2 · extra) `curl -s -i … | grep -E …` → TERM(laptop/11: 2–3, 5–6 wrap); 200 OK,
   Server: gunicorn, the title and the disabled Play audio button YELLOW; the page's button pulses.
8. TRACKER [2.1] 3. The page: Good afternoon everyone, en → fr. The page gives way to
   CODE(index.html: 76–80) with `method: 'POST'` and `JSON.stringify` PINK; a PINK JSON envelope
   {text, src, dest} flies out. TRACKER [2.1] 3 · extra: the laptop/21 POST → TERM(laptop/21: 2, 4);
   `\\u00e0` YELLOW + row tag "the browser shows: à"; the page returns and fills Bonjour à tous.
   GREY card "captured during a second run of the same command (laptop/20)"; `▶ your turn`.
9. V4's contrast: a PINK GET (query string) bounces off the app RED: laptop/26 → TERM(laptop/26: 2,
   4) RED, chip 405; the dest "xx" POST of laptop/25 → TERM(laptop/25: 2, 4) RED, chip 400.
10. TRACKER [2.1] 4. The page's Play audio pulses GREY; the /api/speech POST of laptop/24 →
   TERM(laptop/24: 2, 4 wrap) RED. Back in the main terminal: TERM(laptop/10: 23–26); V5's gunicorn
   gets a SIGINT arrow straight in (chip "main process · gets the signal") and folds away; `--rm`
   sweeps the container away; the TEAL image stays on the laptop's shelf.
11. TRACKER [2.1] 4 · extra. `docker run -d --name port-demo --rm -e PORT=9090 -p 8086:8080 …`
   (laptop/30; container id not printed); a new container (8080 pipe); the ear moves to 9090 (you
   wrote PORT); `curl -sS http://localhost:8086/` → TERM(laptop/31: 2) RED, the knock dies at the
   pipe's end; `docker logs …` → TERM(laptop/32: 3 wrap), 9090 YELLOW.
12. `docker stop port-demo` → TERM(laptop/33: 2); the run with `-p 8086:9090` (laptop/34, id not
   printed); the pipe reattaches to the ear; `curl -s … | grep -o …` → TERM(laptop/35: 2) GREEN,
   the knock arrives; BLUE chip "Cloud Run: sets PORT and knocks on it"; `docker stop port-demo` →
   TERM(laptop/36: 2). Fade out; empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S07"]

MAIN_PY = "tutorial/app/translation_demo/__main__.py"
INDEX = "tutorial/app/translation_demo/templates/index.html"
LOCAL = "http://localhost:8086"            # README:251


class _Quiet:
    """A stand-in 'scene' for building a set piece's state without playing it (the PLAYS methods
    then only assemble their parts; the piece is shown later with one FadeIn)."""

    mobjects: list = []

    def play(self, *a, **k):
        pass

    def add(self, *m):
        pass

    def remove(self, *m):
        pass


def row_with(rows, sub):
    """The first row (a mono_line) among `rows` whose text contains `sub`."""
    for r in rows:
        if sub in getattr(r, "text", ""):
            return r
    raise KeyError(f"{sub!r} not in {[getattr(r, 'text', '') for r in rows]}")


def color_sub(scene, t, rows, sub, color, run_time: float = 0.4, occurrence: int = 0):
    """PLAYS: colour substring `sub` of the row that holds it, then re-seat the terminal."""
    r = row_with(rows, sub)
    scene.play(*[g.animate.set_color(color) for g in substring(r, sub, occurrence)], run_time=run_time)
    reseat(scene, t)
    return r


def reseat(scene, t):
    """Re-seat terminal t as one mobject, then put the title-bar tags (scene.bar_tags) back on top:
    re-adding the terminal alone draws its bar over them and they vanish."""
    scene.add(t)
    for m in getattr(scene, "bar_tags", []):
        if m in scene.mobjects:
            scene.add(m)


def seat(pe):
    """PortEnvelope stores its ear height at construction: re-read it after the piece moved."""
    pe.ear_y = pe.p(0, -0.2)[1]
    return pe


def first_ear(pe, port: str = "8080"):
    """The container ear the way PortEnvelope.envelope() places it, without the envelope."""
    e = ear(port, size=pe.size)
    e.glyph.move_to([pe.box.get_left()[0] + 0.12, pe.ear_y, 0])
    e.text.next_to(e.glyph, DOWN, buff=0.15).align_to(e.glyph, RIGHT).shift(LEFT * 0.35)
    pe.ear_ = e
    return e


def env_group(port: str, writer: str, pe):
    """The envelope 'PORT=<port>' with its writer's name to its RIGHT (PortEnvelope.envelope puts
    the name on the left, on top of the box's 'container' label)."""
    col, who = {"image": (IMAGE, "image ENV"), "you": (YOU, "you · -e")}[writer]
    env = envelope(f"PORT={port}", col).move_to(pe.p(0.95, 0.95))
    wl = label(who, 20, col).next_to(env, RIGHT, buff=0.12)
    return VGroup(env, wl)


def env_in(scene, pe, port: str = "8080", writer: str = "image", run_time: float = 1.0):
    """PLAYS: PortEnvelope.envelope() with the writer's name on the right and the ear's address
    clear of the box edge: the envelope arrives, then the PINK ear and its wire to the process."""
    g = env_group(port, writer, pe)
    pe.env = g
    pe.show(scene, g, anims=[FadeIn(g[0], shift=DOWN * 0.3), FadeIn(g[1])], run_time=run_time * 0.5)
    e = first_ear(pe, f"0.0.0.0:{port}")
    wire = Line(e.glyph.get_right(), pe.proc.frame.get_left(), color=ROUTE, stroke_width=3)
    pe.show(scene, e, wire, anims=[FadeIn(e, scale=0.6), Create(wire)], run_time=run_time * 0.5)
    pe.wire = wire


def ghost(scene, cs, text: str = "your arguments", run_time: float = 2.0):
    """PLAYS: a GREY dashed ghost chip slides into the CMD slot and pushes the old CMD aside, then
    everything reverts (CommandSlots.ghost_args fills the dashed chip solid GREY over its word)."""
    g = dashed_chip(text, S.GREY)
    g.move_to(cs.cmd_slot).align_to(cs.cmd_slot, LEFT).shift(RIGHT * 0.15)
    old = cs.cmd_content
    scene.play(FadeIn(g, shift=RIGHT * 1.5), old.animate.shift(RIGHT * 2.6).set_opacity(0.2),
               run_time=run_time * 0.45)
    scene.wait(run_time * 0.2)
    scene.play(FadeOut(g, shift=LEFT * 0.6), old.animate.shift(LEFT * 2.6).set_opacity(1),
               run_time=run_time * 0.35)
    scene.remove(g)
    cs.heal(scene)


def sigint(scene, pe, run_time: float = 1.2):
    """PLAYS: PortEnvelope.sigint() with the arrow straight down into the process and 'SIGINT' beside
    it, inside the container (the shared version puts the label on the box's top border)."""
    top = pe.proc.frame.get_top()
    a = Arrow(top + UP * 0.75, top, buff=0.05, color=INK, stroke_width=3, tip_length=0.18)
    lab = mono("SIGINT", 20, INK).next_to(a.get_start(), RIGHT, buff=0.12).shift(DOWN * 0.12)
    pe.show(scene, a, lab, anims=[GrowArrow(a), FadeIn(lab)], run_time=run_time * 0.4)
    parts = [pe.proc] + [m for m in (pe.slots, getattr(pe, "wire", None)) if m is not None]
    pe.drop(scene, *parts, a, lab, run_time=run_time * 0.6)
    pe.wire = None
    pe.proc = pe.slots = None


def regrow(scene, t, rows: int, tags=(), keep=None, extra=(), run_time: float = 0.6):
    """PLAYS: resize() the second-tab strip and carry its title-bar tags (on scene) with the bar.
    keep=0 clears it first, so the next command starts on the top row."""
    ref = term(P_REPO, rows, T_TAB, size=t.size)
    dy = ref.box.get_top()[1] - t.box.get_top()[1]
    return resize(scene, t, rows, keep=keep, run_time=run_time,
                  extra=[*[m.animate.shift(UP * dy) for m in tags], *extra])


def app_box() -> VGroup:
    """The app as the server sees it: gunicorn on localhost:8086 with its one translate route."""
    head = label("the app · gunicorn on :8086", 20, S.GREY)
    route = mono("POST /api/translate · JSON", 20, INK)
    body = VGroup(head, route).arrange(DOWN, buff=0.3)
    fr = RoundedRectangle(width=body.width + 0.6, height=body.height + 0.6, corner_radius=0.14,
                          stroke_color=TOOL, stroke_width=2.5).set_fill(PANEL, 1).move_to(body)
    g = VGroup(fr, body)
    g.frame, g.route = fr, route
    return g


def right_at(m, y: float, right: float = 6.35):
    """Put m with its right edge at `right` and its centre at height y."""
    return m.move_to([right - m.width / 2, y, 0])


class RunTheImage(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 13, len(SAY)
        c10 = capture("laptop/10")
        assert c10.cmd_lines[1].strip() == IMAGE_REF and "--rm -p 8086:8080" in c10.cmd_lines[0]

        # ========================================================== 0. Part 2: an app that works on localhost
        tr = tracker_21(1)
        ref = lref("10, 14")
        body = ("Now imagine you already have a working containerized\nweb app on your laptop. …\n"
                "Sharing localhost does not make it available\non another person's computer.")
        rc = readme_card((237, 240), body).move_to([-1.3, 0.55, 0])
        icon = grid_icon(0.7).next_to(rc, RIGHT, buff=0.7)
        cell = icon.cells[1][1]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(ref), run_time=0.6)
            self.play(FadeIn(rc, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("Now imagine")
            self.play(FadeIn(icon, scale=0.8), run_time=0.6)
            vo.wait_until("Sharing localhost")
            self.play(Indicate(rc.body[2], color=TURN, scale_factor=1.04), run_time=0.9)
            vo.wait_until("so we deploy")
            self.play(cell.frame.animate.set_stroke(TURN, 4), cell.fill.animate.set_fill(TURN, 0.25),
                      run_time=0.6)
            self.play(Indicate(cell, color=TURN, scale_factor=1.15), run_time=0.8)

        # ========================================================== 1. docker run (README:246-249)
        t = term(P_REPO, 4, T_LAPTOP, size=20)
        pe1 = seat(PortEnvelope().shift(UP * 1.0 + RIGHT * 0.8))
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(rc), FadeOut(icon), run_time=0.5)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            typed = type_capture(self, t, c10, type_time=1.3)
            row1, row2 = rows_of(typed[0])[0], rows_of(typed[1])[0]
            yt = on_bar(t, turn_row())
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("remove when done")
            r_rm = ring(substring(row1, "--rm"), S.GREY)
            self.play(Create(r_rm), run_time=0.5)
            vo.wait_until("publish port")
            r_p = ring(substring(row1, "-p 8086:8080"), ROUTE)
            self.play(Create(r_p), run_time=0.5)
            e1 = first_ear(pe1)
            pe1.show(self, e1, anims=[FadeIn(pe1.box), FadeIn(pe1.blabel), FadeIn(e1, scale=0.6)],
                     run_time=0.6)
            pe1.wall(self, run_time=1.0)
            vo.wait_until("and the tutorial's public image")
            r_i = ring(substring(row2, IMAGE_REF), IMAGE)
            self.play(Create(r_i), run_time=0.6)
            vo.wait_until("Pause and run it")
            flash_tag(self, yt)

        # ========================================================== 2. the pull and the digest
        readme_dg = mono(readme(1069), 20, INK)
        assert readme(1069) == DIGEST
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(r_rm, r_p, r_i, yt)), FadeOut(pe1), run_time=0.5)
            resize(self, t, 12, run_time=0.7)
            out(self, t, c10.at((3, 5), "…", (15, 16)), wrap=True, run_time=0.9)   # 17 waits for the card
            room(self, t, 2)              # two free rows under the digest for the README card
            dg_row = row_with(t.lines, DIGEST)
            self.play(*[g.animate.set_color(TURN) for g in substring(dg_row, DIGEST)], run_time=0.4)
            self.add(t)
            vo.wait_until("The digest equals")
            card1069 = readme_card(1069, readme_dg, card_w=readme_dg.width + 0.45)
            dx = substring(dg_row, DIGEST)[0].get_left()[0] - readme_dg[0].get_left()[0]
            card1069.shift(RIGHT * dx)
            card1069.next_to(dg_row.strut, DOWN, buff=0.12, coor_mask=np.array([0, 1, 0]))
            self.play(FadeIn(card1069, shift=UP * 0.2), run_time=0.6)
            a = substring(dg_row, DIGEST)
            pairs = [AnimationGroup(a[i].animate.set_color(OWN), readme_dg[i].animate.set_color(OWN))
                     for i in range(len(a))]
            self.play(LaggedStart(*pairs, lag_ratio=0.08), run_time=2.2)
            self.add(t, card1069)
            same = ok_chip("same bytes, same digest")
            right_at(same, card1069.head.get_center()[1], card1069.frame.get_right()[0] - 0.15)
            self.play(FadeIn(same, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("The image is built for")
            arch = grey_chip("linux/amd64 · Apple Silicon: a platform WARNING prints first · harmless, it runs emulated")
            under_term(t, arch)
            self.play(FadeIn(arch, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("on Apple Silicon")
            self.play(Indicate(arch.text, color=INK, scale_factor=1.05), run_time=0.8)

        # ========================================================== 3. gunicorn listens on 0.0.0.0:8080
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(card1069, same, arch)), run_time=0.4)
            rows = out(self, t, c10.at((17, 22)), wrap=True, run_time=0.9, lag=0.12)
            vo.wait_until("port 8080")
            r19 = color_sub(self, t, rows, "http://0.0.0.0:8080", ROUTE)
            nxt = t.lines.submobjects[list(t.lines.submobjects).index(r19) + 1]
            vo.wait_until("every network interface")
            ev = beside(row_tag("every network interface"), nxt, buff=0.5)
            pin(self, nxt, ev)
            ctl = grey_chip("recent gunicorn (25.1 and later) · 26.2.0 at the time of recording")
            under_term(t, ctl)
            vo.wait_until("so connections")
            self.play(FadeIn(ctl, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(substring(r19, "0.0.0.0"), color=ROUTE, scale_factor=1.2), run_time=0.8)
            self.add(t)

        # ========================================================== 4. V5 a: the image's two start-up slots
        c16 = capture("laptop/16")
        tab = term(P_REPO, 4, T_TAB, size=20)
        xb = on_bar(tab, extra_row())
        cs = CommandSlots().move_to([0, 0.9, 0])
        self.bar_tags = [xb]
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(ctl), run_time=0.3)
            unpin(self, nxt, ev)
            resize(self, t, 4, run_time=0.6)
            self.play(FadeOut(t, shift=DOWN * 0.3), track(tr, 1, True), run_time=0.5)
            self.play(FadeIn(tab, shift=UP * 0.2), FadeIn(xb), run_time=0.5)
            for i, row in enumerate(c16.cmd_lines):        # one command over six rows; row 6 soft-wraps
                type_cmd(self, tab, row, 0.35, prompt=(i == 0), soft=(i == 5))
            r16 = out(self, tab, c16.at(11, 12, 17), run_time=0.5)
            vo.wait_until("the image has two start-up slots")
            frame_parts = VGroup(cs.block, cs.blabel, cs.entry_slot, cs.cmd_slot)
            self.play(FadeIn(frame_parts),
                      TransformFromCopy(r16[0], VGroup(cs.entry_name, cs.entry_content)),
                      TransformFromCopy(r16[1], VGroup(cs.cmd_name, cs.cmd_content)), run_time=1.2)
            self.remove(*cs.get_family())
            self.add(cs)
            reseat(self, tab)
            vo.wait_until("an empty entrypoint")
            self.play(Indicate(cs.entry_content, color=INK, scale_factor=1.3), run_time=0.7)
            cs.heal(self)
            vo.wait_until("and a command")
            self.play(Indicate(cs.cmd_content, color=IMAGE, scale_factor=1.08), run_time=0.8)
            cs.heal(self)
            vo.wait_until("Docker runs the entrypoint")
            self.play(Indicate(cs.entry_name, color=INK, scale_factor=1.15), run_time=0.6)
            cs.heal(self)
            self.play(Indicate(cs.cmd_name, color=IMAGE, scale_factor=1.2), run_time=0.6)
            cs.heal(self)
            vo.wait_until("and arguments you pass")
            ghost(self, cs, run_time=2.0)
            vo.wait_until("part 4 depends")
            p4 = chip("part 4", TURN, size=20).next_to(cs.block, UP, buff=0.12).align_to(cs.block, RIGHT)
            self.play(FadeIn(p4, shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeOut(tab), FadeOut(xb), run_time=0.5)

        # ========================================================== 5. V5 b: python becomes gunicorn
        cmd_chip = chip("CMD: [python -m translation_demo serve]", IMAGE, size=20, font=MONO)
        cmd_chip.move_to([6.4 - cmd_chip.width / 2, 2.45, 0])
        panel = code(MAIN_PY, 22, 26, font_size=20, dedent=True, cuts={25: '"--threads", "4",'})
        panel.move_to([0, 0.85, 0])
        pe = PortEnvelope().move_to(ORIGIN)
        pe.shift(-pe.ref.get_center() + np.array([-0.2, -2.05, 0]))
        seat(pe)
        with self.voiceover(SAY[5]) as vo:
            cmd = cs.cmd_content
            cs.remove(cmd)
            self.add(cmd)
            self.play(FadeOut(cs), ReplacementTransform(cmd, cmd_chip), FadeOut(p4), track(tr, 1, False),
                      run_time=0.8)
            self.play(FadeIn(panel, shift=UP * 0.15), FadeIn(pe), run_time=0.6)
            pe.start(self, run_time=0.5)
            vo.wait_until("takes its port")
            b23 = line_bar(panel.code, 1, TURN, 0.22)
            self.play(FadeIn(b23), run_time=0.3)
            env_in(self, pe, "8080", "image", run_time=1.0)
            vo.wait_until("replaces itself")
            b24 = line_bar(panel.code, 2, TURN, 0.22)
            self.play(FadeIn(b24), run_time=0.3)
            pe.execvp(self, run_time=0.9)
            vo.wait_until("1 worker")
            sp = code_span(panel.code, 3, '"--workers", "1", "--threads", "4"')
            self.play(*[g.animate.set_color(OWN) for g in sp], FadeOut(VGroup(b23, b24)), run_time=0.4)
            self.remove(b23, b24)
            self.add(panel)
            pe.threads(self, 4, run_time=0.6)

        # ========================================================== 6. extra checks: docker top, ps, curl :8080
        c13, c12, c14 = capture("laptop/13"), capture("laptop/12"), capture("laptop/14")
        top_lines = [c13.line(2)] + [cut(from_phrase(c13.line(n), "{gunicorn}"), "--threads 4")
                                     for n in (3, 4)]
        tab = term(P_REPO, 6, T_TAB, size=20)       # six rows: the command and both processes
        xb = on_bar(tab, extra_row())
        self.bar_tags = [xb]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(panel), FadeOut(cmd_chip), track(tr, 1, True),
                      run_time=0.4)
            self.play(pe.animate.shift(np.array([1.0, 3.05, 0])), run_time=0.6)
            seat(pe)
            pe.heal(self)
            self.play(FadeIn(tab, shift=UP * 0.2), FadeIn(xb), run_time=0.4)
            type_capture(self, tab, c13, type_time=0.8)
            rows13 = out(self, tab, top_lines, wrap=True, run_time=0.5)
            vo.wait_until("Docker top shows")
            self.play(*[g.animate.set_color(TURN) for r in rows13[1:] if "{gunicorn}" in r.text
                        for g in substring(r, "{gunicorn}")], run_time=0.5)
            reseat(self, tab)
            self.play(Indicate(pe.proc.frame, color=TOOL, scale_factor=1.04), run_time=0.6)
            pe.heal(self)
            r_thr = ring(substring(row_with(rows13, "--threads 4"), "--threads 4"), OWN)
            self.play(Create(r_thr), run_time=0.5)
            vo.wait_until("no Python is left")
            py_row = row_with(rows13, "python3.12")
            r_py = ring(substring(py_row, "/usr/local/bin/python3.12"), S.GREY, dashed=True)
            interp = card(["the interpreter running gunicorn ·", "python -m translation_demo is gone"],
                          size=20)
            interp.move_to([-6.35 + interp.width / 2, 1.9, 0])
            self.play(Create(r_py), FadeIn(interp, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Docker ps shows")
            self.play(FadeOut(VGroup(r_thr, r_py, interp)), run_time=0.3)
            type_capture(self, tab, c12, type_time=0.9)
            rows12 = out(self, tab, c12.at(2, 3), wrap=True, run_time=0.5)
            color_sub(self, tab, rows12, "0.0.0.0:8086->8080/tcp", ROUTE)
            pe.wall(self, run_time=1.0)
            vo.wait_until("so 8080 on the laptop")
            type_capture(self, tab, c14, type_time=0.6)
            out(self, tab, c14.at(2), wrap=True, run_time=0.4, color=ERR)
            before = list(pe.submobjects)
            pe.knock(self, "8080", ok=False, run_time=1.0)
            knock_parts = [m for m in pe.submobjects if m not in before]

        # ========================================================== 7. step 2: open localhost:8086
        c11 = capture("laptop/11")
        page = TranslatePage(url=LOCAL)
        page.shift(-page.frame.get_center() + np.array([-2.3, 0.84, 0]))
        ill = illustration_tag().next_to(page.frame, RIGHT, buff=0.2).align_to(page.frame, UP)
        with self.voiceover(SAY[7]) as vo:
            regrow(self, tab, 4, tags=[xb], extra=[FadeOut(pe), track(tr, 2, False)], run_time=0.6)
            self.play(FadeIn(page, shift=UP * 0.2), FadeIn(ill), run_time=0.7)
            self.play(Indicate(page.url, color=ROUTE, scale_factor=1.1), run_time=0.7)
            page.heal(self)
            vo.wait_until("An extra curl")
            self.play(track(tr, 2, True), run_time=0.4)
            type_capture(self, tab, c11, type_time=1.0)
            r2 = out(self, tab, c11.at(2, 3), run_time=0.4)
            vo.wait_until("status 200")
            color_sub(self, tab, r2, "200 OK", TURN, run_time=0.3)
            vo.wait_until("from gunicorn")
            color_sub(self, tab, r2, "Server: gunicorn", TURN, run_time=0.3)
            r5 = out(self, tab, c11.at(5), run_time=0.3)
            vo.wait_until("the title")
            color_sub(self, tab, r5, "<title>Translate · AC215</title>", TURN, run_time=0.3)
            vo.wait_until("and the disabled")
            r6 = out(self, tab, c11.at(6), wrap=True, run_time=0.4)
            color_sub(self, tab, r6, "disabled", TURN, run_time=0.3)
            r_pa = row_with(r6, "Play audio")          # the 72-character rows split the button's label
            r_p3 = row_with(r6, "part 3</button>")
            self.play(*[g.animate.set_color(TURN) for g in substring(r_pa, r_pa.text[r_pa.text.index("Play audio"):])],
                      *[g.animate.set_color(TURN) for g in substring(r_p3, "part 3")], run_time=0.3)
            reseat(self, tab)
            self.play(page.press("audio", S.GREY), run_time=0.7)
            page.heal(self)

        # ========================================================== 8. step 3: translate (a JSON POST)
        c21 = capture("laptop/21")
        idx = code(INDEX, 76, 80, font_size=20, dedent=True, cuts={78: "JSON.stringify({text:"})
        idx.move_to([0, 1.5, 0])                    # above the 7-row strip
        with self.voiceover(SAY[8]) as vo:
            self.play(track(tr, 3, False), run_time=0.4)
            page.type_in(self, run_time=0.8)
            page.set_dest(self, "fr", run_time=0.4)
            vo.wait_until("The button sends JSON")
            self.play(page.press("translate"), run_time=0.5)
            page.heal(self)
            self.play(FadeOut(page), FadeOut(ill), FadeIn(idx, shift=UP * 0.1), run_time=0.5)
            spans = [code_span(idx.code, 1, "method: 'POST'"), code_span(idx.code, 2, "JSON.stringify")]
            self.play(*[g.animate.set_color(ROUTE) for s in spans for g in s], run_time=0.3)
            self.add(idx)
            env = envelope("{text, src, dest}", ROUTE)
            env.move_to([spans[1].get_right()[0] + 0.3 + env.width / 2, idx.get_bottom()[1] - 0.1, 0])
            self.play(FadeIn(env, shift=DOWN * 0.2), run_time=0.3)
            self.play(env.animate.move_to([6.35 - env.width / 2, idx.get_bottom()[1] - 0.1, 0]), run_time=0.6)
            # the strip grows to 7 rows and clears: the whole command and its [HTTP 200] stay in view
            regrow(self, tab, 7, tags=[xb], keep=0, extra=[track(tr, 3, True), FadeOut(env)], run_time=0.4)
            type_cmd(self, tab, c21.cmd, 0.9, soft=True)    # quoted JSON: wraps like a real terminal
            r21 = out(self, tab, c21.at(2, 4), run_time=0.3)
            vo.wait_until("and gets back")
            color_sub(self, tab, r21, "\\u00e0", TURN, run_time=0.3)
            vo.wait_until("once the browser decodes")
            sec = card(["captured during a second", "run of the same command", "(laptop/20)"], size=20)
            sec.next_to(page.frame, RIGHT, buff=0.2).align_to(page.frame, DOWN)
            regrow(self, tab, 4, tags=[xb], run_time=0.5,
                   extra=[FadeOut(idx), FadeIn(page), FadeIn(ill), FadeIn(sec, shift=UP * 0.1)])
            bs = on_bar(tab, row_tag("the browser shows: à", TURN))
            self.bar_tags = [xb, bs]
            self.play(FadeOut(xb), FadeIn(bs), run_time=0.4)
            page.translate(self, "Bonjour à tous", run_time=0.8)
            yt2 = your_turn().next_to(ill, DOWN, buff=0.3).align_to(ill, LEFT)
            vo.wait_until("Pause and try it")
            self.play(FadeIn(yt2, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt2)

        # ========================================================== 9. V4's contrast: 405 and 400
        c26, c25 = capture("laptop/26"), capture("laptop/25")
        app = app_box()
        app.move_to([-6.3 + app.width / 2, 1.75, 0])
        right_x = app.frame.get_right()[0]
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(yt2), FadeOut(bs), FadeIn(xb), run_time=0.3)
            self.bar_tags = [xb]
            # the page steps back for the app; the strip grows to 7 rows and clears for each command
            regrow(self, tab, 7, tags=[xb], keep=0, run_time=0.5,
                   extra=[FadeOut(page), FadeOut(ill), FadeOut(sec), FadeIn(app)])
            type_cmd(self, tab, c26.cmd, 0.8, soft=True)
            out(self, tab, c26.at(2, 4), run_time=0.3, color=ERR)
            get = chip("GET · the query string", ROUTE, size=20)
            gy = app.frame.get_top()[1] - get.height / 2
            right_at(get, gy)
            self.play(FadeIn(get, shift=LEFT * 0.2), run_time=0.3)
            self.play(get.animate.move_to([right_x + get.width / 2 + 0.05, gy, 0]), run_time=0.35)
            self.play(get.animate.move_to([right_x + 0.4 + get.width / 2, gy, 0]).set_color(ERR), run_time=0.35)
            vo.wait_until("405 here")
            e405 = err_chip("405 · method not allowed", mono_font=False).next_to(get, DOWN, buff=0.12)
            e405.align_to(get, LEFT)
            self.play(FadeIn(e405, shift=UP * 0.1), run_time=0.3)
            vo.wait_until("this app wants JSON posts")
            self.play(Indicate(app.route, color=ROUTE, scale_factor=1.08), run_time=0.6)
            self.add(app)
            resize(self, tab, 7, keep=0, run_time=0.3)
            type_cmd(self, tab, c25.cmd, 0.6, soft=True)
            out(self, tab, c25.at(2, 4), run_time=0.3, color=ERR)
            vo.wait_until("A made-up language")
            xx = chip('dest: "xx"', ROUTE, size=20, font=MONO)
            xy = e405.get_bottom()[1] - 0.3 - xx.height / 2
            right_at(xx, xy)
            self.play(FadeIn(xx, shift=LEFT * 0.2), run_time=0.25)
            self.play(xx.animate.move_to([right_x + xx.width / 2 + 0.05, xy, 0]), run_time=0.3)
            e400 = err_chip("400", mono_font=False)
            e400.move_to([right_x + 0.4 + xx.width + 0.15 + e400.width / 2, xy, 0])
            self.play(xx.animate.move_to([right_x + 0.4 + xx.width / 2, xy, 0]).set_color(ERR),
                      FadeIn(e400, shift=LEFT * 0.1), run_time=0.35)

        # ========================================================== 10. step 4: speech 503; Ctrl+C
        c24 = capture("laptop/24")
        shelf = VGroup(image_block("image", 2.2), Line(LEFT * 1.4, RIGHT * 1.4, color=S.GREY, stroke_width=4))
        shelf[1].next_to(shelf[0], DOWN, buff=0.05)
        shelf.add(label("the laptop's images", 20, S.GREY).next_to(shelf[1], DOWN, buff=0.1))
        ab = page.audio_btn.copy().move_to(app.frame)
        ill2 = illustration_tag().next_to(ab, RIGHT, buff=0.3)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(get, e405, xx, e400)), FadeOut(app), FadeIn(ab), FadeIn(ill2),
                      track(tr, 4, False), run_time=0.5)
            self.play(Indicate(ab, color=S.GREY, scale_factor=1.08), run_time=0.8)
            vo.wait_until("and its request")
            resize(self, tab, 7, keep=0, extra=[track(tr, 4, True)], run_time=0.3)
            type_cmd(self, tab, c24.cmd, 1.0, soft=True)
            r24 = out(self, tab, c24.at(2, 4), wrap=True, run_time=0.4, color=ERR)
            vo.wait_until("speech is disabled")
            self.play(Indicate(row_with(r24, "[HTTP 503]"), color=ERR, scale_factor=1.1), run_time=0.6)
            reseat(self, tab)
            vo.wait_until("Stop with Control C")
            # back to the first terminal; the container picture returns at the same place as before
            pe.remove(*knock_parts)                     # the 8080 knock stays in its beat
            self.play(FadeOut(ab), FadeOut(ill2), FadeOut(tab), FadeOut(xb), track(tr, 4, False),
                      run_time=0.5)
            self.play(FadeIn(t), FadeIn(pe), run_time=0.5)
            out(self, t, c10.at((23, 26)), wrap=True, run_time=0.7)
            vo.wait_until("gunicorn is the main process")
            mp = grey_chip("main process · gets the signal").move_to([pe.box.get_center()[0], -0.8, 0])
            self.play(FadeIn(mp, shift=UP * 0.1), run_time=0.4)
            pe.drop(self, pe.env, run_time=0.3)
            pe.env = None
            sigint(self, pe, run_time=1.2)
            shelf.move_to(pe.box)
            rm = grey_chip("--rm: container removed · image kept", mono_font=False).move_to(mp)
            gone = [m for m in (pe.box, pe.blabel, pe.env, pe.ear_, pe.pipe, pe.pipe_label, pe.door)
                    if m is not None]
            pe.drop(self, *gone, run_time=0.7, shift=RIGHT * 0.6,
                    extra=[FadeIn(shelf, shift=UP * 0.1), ReplacementTransform(mp, rm)])

        # ========================================================== 11. extra: PORT=9090, pipe still at 8080
        c30, c31, c32 = capture("laptop/30"), capture("laptop/31"), capture("laptop/32")
        pe2 = PortEnvelope()
        pe2.shift(pe.ref.get_center() - pe2.ref.get_center())
        seat(pe2)
        q = _Quiet()
        pe2.start(q, "gunicorn")
        pe2.threads(q, 4)
        env_in(q, pe2, "8080", "image")
        pe2.wall(q)
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(rm), track(tr, 4, True), run_time=0.4)
            type_capture(self, t, c30, type_time=1.2)
            self.play(FadeOut(shelf), run_time=0.3)
            self.play(FadeOut(pe), FadeIn(pe2), run_time=0.5)
            vo.wait_until("set PORT to 9090")
            new_env = env_group("9090", "you", pe2)
            pe2.swap(self, pe2.env, new_env, run_time=0.6)
            pe2.env = new_env
            pe2.move_ear(self, "9090", run_time=0.8)
            vo.wait_until("but keep the pipe at 8080")
            self.play(Indicate(pe2.pipe_label, color=ROUTE, scale_factor=1.15), run_time=0.7)
            pe2.heal(self)
            vo.wait_until("the connection resets")
            type_capture(self, t, c31, type_time=0.6)
            out(self, t, c31.at(2), run_time=0.3, color=ERR)
            d = pulse_dot(r=0.11).move_to(pe2.door[0])
            end = pe2.pipe.get_end()
            self.add(d)
            self.play(d.animate.move_to(end), run_time=0.6)
            rs = err_chip("connection reset", mono_font=False)
            rs.move_to([pe2.wall_[0].get_center()[0] - 0.3 - rs.width / 2, pe2.ear_y - 0.65, 0])
            self.play(d.animate.set_color(ERR), FadeIn(rs), run_time=0.4)
            vo.wait_until("the log shows")
            type_capture(self, t, c32, type_time=0.7)
            r32 = out(self, t, c32.at(3), wrap=True, run_time=0.4)
            color_sub(self, t, r32, "9090", TURN, run_time=0.4)

        # ========================================================== 12. pipe to 9090: it answers
        c33, c34, c35, c36 = (capture(f"laptop/{n}") for n in (33, 34, 35, 36))
        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(VGroup(d, rs)), run_time=0.3)
            type_capture(self, t, c33, type_time=0.6)
            out(self, t, c33.at(2), run_time=0.3)
            type_capture(self, t, c34, type_time=1.0)
            pe2.repipe(self, "8086", "9090", run_time=0.8)
            vo.wait_until("and it answers")
            type_capture(self, t, c35, type_time=0.7)
            out(self, t, c35.at(2), run_time=0.3, color=OWN)
            pe2.knock(self, "9090", ok=True, run_time=1.0)
            vo.wait_until("The right-hand number")
            rp = ring(pe2.pipe_label[-4:], ROUTE)
            cr = chip("Cloud Run: sets PORT and knocks on it", CLOUD, size=20)
            cr.move_to([pe2.box.get_center()[0], -0.8, 0])
            self.play(Create(rp), FadeIn(cr, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(pe2.ear_.text, color=ROUTE, scale_factor=1.15), run_time=0.7)
            pe2.heal(self)
            type_capture(self, t, c36, type_time=0.6)
            out(self, t, c36.at(2), run_time=0.3)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
