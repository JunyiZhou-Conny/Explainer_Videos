"""S01 · One container stops, the site goes dark (cold open of AC215 L20, the full follow-along). No
tracker (only the sample in beat 6). Lecture: 20 · 7 (the goal picture), 20 · 4–5 (roadmap, problem).

Beats (script.md "## S01", one voiceover block each):
0. Black frame. A full-width terminal `cheese-app-vm` (GREY row tag `extra` on its title bar) slides
   in and types vm/58's command exactly as captured (folds with ' \\' into five rows at 20 pt) just before the
   voice → TERM(vm/58: 2–8). On "the frontend" line 6 `frontend  Exited (0) …` turns YELLOW; on "and
   restarted the web server" line 5 `nginx  Exited (1) …` turns RED; on "The API container is still
   up" / "and so is the vector database" lines 7–8 tick GREEN.
1. TERM(vm/58: 10 (wrap), 11): the `[emerg] host not found in upstream "frontend"` line RED, then
   `http://localhost/ -> 000` with `000` RED and a PINK chip "nothing answers". On "the address of the
   API included" a GREY dashed ghost row `http://localhost/api-service/ -> ?` (never output: vm/58:1
   curls only `/`) with a GREY chip "same door: nginx is down".
2. The terminal shrinks to a 2-row strip at the top (the GREEN api-service row, the RED 000 row). A
   YELLOW card in the centre: "The API is up. / Why is the API's address dead too?" It holds, then
   shrinks into a small YELLOW sticky note top right while the strip fades.
3. lecture_ref(20, "7"), left of the sticky. V1 MasterDiagram teaser (slide 7 redrawn): 'Local
   Computer' with IDE / CLI, Containers and six dashed TEAL squares; the dotted BLUE GCP outline and
   the 'Compute Instance (VM)' panel; the hollow GREY arrow; nginx, API, frontend, vector DB grow;
   the PINK 'HTTP 80' door on the VM's top edge; the browser and the PINK request arrows. GREY
   `illustration` tag bottom left. On "by hand" and on "then as code" the VM outline pulses YELLOW.
4. lecture_ref(20, "4–5"). The diagram slides away. Slide 4 redrawn small: GREY arrow POC /
   Prototype / MVP, dashed boundaries, staggered GREY bars; a dashed YELLOW marker moves from "Build
   Cheese App" down to "Deployment, Scaling & Automation". Under it slide 5's line: a GREY laptop
   with a GREEN tick "runs on your computer", a BLUE server with a "?" "reaches users". The sticky
   fades at the end of the block.
5. The roadmap fades; the V1 laptop ('Local Computer') waits at the left. Four chips slide out of it,
   one per phrase: "cheese-app-v3 + secrets/ beside it", "a GCP project with billing", "a Docker Hub
   account", and the GOLD cost tag "this lecture costs money · delete it at the end of each part".
6. The chips fade. Sample YELLOW tracker (README › Deployment to GCP (Manual) · step 2 of 15, Docker
   login, the step whose command is the sample) top left; code panel `nginx.conf · lines 35–44`;
   a 2-row strip types README:21's `docker login -u <USER NAME> -p <ACCESS TOKEN>` and a YELLOW
   `▶ your turn` row tag pulses beside it, each on its phrase.
7. The samples fade. A text-free terminal glyph returns and moves into the left column of a GREY
   two-column card: "a machine you own / → real, complete" (GREEN tick) | "Google · Docker Hub /
   → stops at its first honest error" (RED dot), GREY footer "and we say what yours prints". Fade;
   empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403
from explainer.devops import laptop

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources (checked)
C58 = capture("vm/58")
assert C58.cmd.startswith("sudo docker stop frontend; sudo docker restart nginx; sleep 3;"), C58.cmd
assert C58.line(5).startswith("nginx ") and "Exited (1)" in C58.line(5), C58.line(5)
assert C58.line(6).startswith("frontend ") and "Exited (0)" in C58.line(6), C58.line(6)
assert C58.line(7).startswith("api-service ") and "Up 10 minutes" in C58.line(7), C58.line(7)
assert C58.line(8).startswith("cheese-app-vector-db ") and "Up 16 minutes" in C58.line(8), C58.line(8)
assert C58.line(10) == 'nginx: [emerg] host not found in upstream "frontend" in /etc/nginx/nginx.conf:48'
assert C58.line(11) == "http://localhost/ -> 000", C58.line(11)
assert "api-service" not in C58.cmd          # the ghost row below is NOT output: only '/' was curled
GHOST = "http://localhost/api-service/ -> ?"
QUESTION = "The API is up.\nWhy is the API's address dead too?"
STICKY = "The API is up.\nWhy is its address dead?"
CHIPS = ("cheese-app-v3 + secrets/ beside it", "a GCP project with billing", "a Docker Hub account")
CHIP_CUES = ("You need cheese app version 3", "a Google Cloud project with billing", "and a Docker Hub account",
             "This costs real money")
COST_TEXT = "this lecture costs money · delete it at the end of each part"
LOGIN = "docker login -u <USER NAME> -p <ACCESS TOKEN>"
assert f"`{LOGIN}`" in readme(21), readme(21)
NGINX = "src/deployment/nginx-conf/nginx/nginx.conf"
TOP = 3.5                       # top edge of the strip (no tracker in this scene)


def refit(scene, t, rows: int, keep, top: float, bar_tag=None, extra=(), run_time: float = 0.7):
    """PLAYS: terminal t shrinks to `rows`, keeps exactly the line mobjects in `keep` and moves so
    its top edge sits at `top`; the title-bar tag rides along (L18 S01's helper, one terminal)."""
    title = t.title.text if t.title is not None else None
    ref = Terminal(prompt=t.prompt, width=t.box.width, rows=rows, size=t.size, title=title)
    ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0], top - ref.box.get_top()[1], 0]))
    kept = [ln for ln in t.lines.submobjects if ln in keep]
    assert len(kept) == len(keep) <= rows, (len(kept), len(keep), rows)
    gone = [ln for ln in t.lines.submobjects if ln not in keep]
    for ln in gone:
        t.lines.remove(ln)
    anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar), t.dots.animate.move_to(ref.dots)]
    if t.title is not None:
        anims.append(t.title.animate.move_to(ref.title))
    for i, ln in enumerate(kept):
        anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
    if bar_tag is not None:
        anims.append(bar_tag.animate.move_to(on_bar(ref, bar_tag.copy()).get_center()))
    scene.play(*anims, *[FadeOut(g) for g in gone], *extra, run_time=run_time)
    scene.remove(*gone)
    t.rows = rows
    scene.add(t)


def roadmap() -> VGroup:
    """Slide 4 redrawn small (our shapes, the slide's structure): .arrow .phases .bounds .bars{name}
    .marker (dashed YELLOW, on 'Build Cheese App')"""
    yc, hh = 2.0, 0.3
    pts = [[-6.3, yc + hh, 0], [5.8, yc + hh, 0], [5.8, yc + hh + 0.14, 0], [6.45, yc, 0],
           [5.8, yc - hh - 0.14, 0], [5.8, yc - hh, 0], [-6.3, yc - hh, 0]]
    arr = Polygon(*pts, stroke_color=S.GREY, stroke_width=3).set_fill(S.GREY, 0.2)
    phases = VGroup(*[label(s, 22, INK).move_to([x, yc, 0])
                      for s, x in (("POC", -4.4), ("Prototype", -0.65), ("MVP", 3.7))])
    for ph in phases[1:]:
        ph.align_to(phases[0], UP)              # cap tops level ('Prototype' has descenders)
    bounds = VGroup(*[DashedLine([x, yc - hh - 0.05, 0], [x, -0.75, 0], color=S.GREY, stroke_width=2,
                                 dash_length=0.12) for x in (-2.55, 1.25)])
    bars = {}
    for s, x0, x1, y in (("Build Baseline Models", -6.3, -2.75, 1.2), ("Build Better Models", -2.35, 1.05, 1.2),
                         ("ML Workflow", -2.35, 1.05, 0.5), ("Build Cheese App", 1.45, 6.3, 0.5),
                         ("Deployment, Scaling & Automation", -0.6, 6.3, -0.2)):
        b = box(x1 - x0, 0.5, S.GREY, fill_opacity=0.15).move_to([(x0 + x1) / 2, y, 0])
        t = label(s, 20, INK).move_to(b)
        assert t.width < b.width - 0.2, s
        bars[s] = VGroup(b, t)
    marker = DashedVMobject(RoundedRectangle(width=4.85 + 0.2, height=0.64, corner_radius=0.1),
                            num_dashes=40).set_stroke(TURN, 3).move_to(bars["Build Cheese App"])
    assert marker.get_left()[0] > bars["ML Workflow"].get_right()[0] + 0.1, marker.get_left()
    g = VGroup(arr, phases, bounds, *bars.values(), marker)
    g.arrow, g.phases, g.bounds, g.bars, g.marker = arr, phases, bounds, bars, marker
    return g


def problem_line() -> VGroup:
    """Slide 5's two bullets as one line of pictures: .lap .tick .lap_t .srv .q .srv_t .arrow"""
    lap = laptop(1.2, LAPTOP).move_to([-3.6, -2.35, 0])
    tick = check_glyph(0.34).next_to(lap.screen, UP, buff=0.08).shift(RIGHT * 0.45)
    tick.move_to(lap.screen.get_center())
    lap_t = label("runs on your computer", 22, INK).next_to(lap, DOWN, buff=0.15)
    srv = server(1.0, 3, CLOUD).move_to([2.6, -2.25, 0])
    q = label("?", 36, TURN).next_to(srv, RIGHT, buff=0.2)
    srv_t = label("reaches users", 22, INK).next_to(srv, DOWN, buff=0.15)
    srv_t.align_to(lap_t, UP)
    ar = arrow(lap.get_right() + RIGHT * 0.2, srv.get_left() + LEFT * 0.2, S.GREY, stroke=3)
    g = VGroup(lap, tick, lap_t, srv, q, srv_t, ar)
    g.lap, g.tick, g.lap_t, g.srv, g.q, g.srv_t, g.arrow = lap, tick, lap_t, srv, q, srv_t, ar
    return g


def term_glyph(glyph_w: float = 2.0, color=LAPTOP) -> VGroup:
    """A text-free terminal: box, title bar with three dots, a few GREY line stubs."""
    h = glyph_w * 0.62
    fr = RoundedRectangle(width=glyph_w, height=h, corner_radius=0.08, stroke_color=color,
                          stroke_width=2.5).set_fill(TERM_BG, 1)
    bar = Line(fr.get_corner(UL) + DOWN * 0.22, fr.get_corner(UR) + DOWN * 0.22, color=color, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.035, color=S.GREY_DARK) for _ in range(3)]).arrange(RIGHT, buff=0.06)
    dots.move_to(fr.get_corner(UL) + np.array([0.24, -0.11, 0]))
    stubs = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2, color=S.GREY, stroke_width=3)
                     for w in (glyph_w * 0.6, glyph_w * 0.45, glyph_w * 0.7)]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    stubs.move_to(fr.get_center() + DOWN * 0.1).align_to(fr, LEFT).shift(RIGHT * 0.18)
    stubs[-1].set_color(OWN)
    return VGroup(fr, bar, dots, stubs)


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 8, len(SAY)

        # ========================================================== 0. one container stops
        t = term(P_VM, rows=16, title=T_VM, size=20)   # 20 pt: 5 command rows + 10 output rows + the ghost
        assert t.box.get_top()[1] < 3.55, t.box.get_top()
        tag0 = on_bar(t, extra_row())
        self.play(FadeIn(t, shift=RIGHT * 0.8), FadeIn(tag0, shift=RIGHT * 0.8), run_time=0.4)
        t.add(tag0)                           # the tag rides with its terminal
        cmd = type_capture(self, t, C58, type_time=1.4)[0]
        assert len(rows_of(cmd)) == 5, len(rows_of(cmd))
        with self.voiceover(SAY[0]) as vo:
            rows = out(self, t, C58.at((2, 8)), run_time=0.6)
            byname = {r.text.split()[0]: r for r in rows if r.text.split()}
            ng, fe, api, vdb = byname["nginx"], byname["frontend"], byname["api-service"], byname["cheese-app-vector-db"]
            assert "Exited (1)" in ng.text and "Exited (0)" in fe.text, (ng.text, fe.text)
            vo.wait_until("the frontend")
            self.play(fe.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(fe, color=TURN, scale_factor=1.06), run_time=0.6)
            self.add(t)
            vo.wait_until("and restarted the web server")
            self.play(ng.animate.set_color(ERR), run_time=0.4)
            self.play(Indicate(ng, color=ERR, scale_factor=1.06), run_time=0.6)
            self.add(t)
            ticks = []
            for cue, ln in (("The API container is still up", api), ("and so is the vector database", vdb)):
                vo.wait_until(cue)
                tk = beside(check_glyph(0.28), ln, buff=0.35)
                self.play(ln.animate.set_color(OWN), FadeIn(tk, scale=1.4), run_time=0.5)
                attach(self, ln, tk)
                ticks.append(tk)
            self.add(t)

        # ========================================================== 1. the whole site answers nothing
        with self.voiceover(SAY[1]) as vo:
            emerg = out(self, t, C58.at(10), wrap=True, run_time=0.5, color=ERR)
            assert len(emerg) == 2, len(emerg)
            vo.wait_until("answers nothing")
            dead = out(self, t, C58.at(11), run_time=0.3)[0]
            zero = substring(dead, "000")
            self.play(zero.animate.set_color(ERR), run_time=0.3)
            self.add(t)
            nothing = beside(row_tag("nothing answers", ROUTE), dead, buff=0.5)
            pin(self, dead, nothing)
            vo.wait_until("the address of the API included")
            ghost = mono_line(GHOST, 20, S.GREY)
            ghost.shift(t._slot(len(t.lines)) - ghost.strut.get_corner(UL))
            gbox = outline_box(ghost.width + 0.3, t.pitch, S.GREY, solid=False).move_to(ghost)
            same = row_tag("same door: nginx is down")
            same.move_to([gbox.get_right()[0] + 0.4 + same.width / 2, gbox.get_center()[1], 0])
            self.play(FadeIn(ghost), Create(gbox), run_time=0.5)
            self.play(FadeIn(same, shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 2. today's puzzle
        qc = question_card(QUESTION).move_to([0, -0.5, 0])
        note_ = sticky(STICKY)
        note_.move_to([6.5 - note_.width / 2, 3.5 - note_.height / 2, 0])
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(ghost, gbox, same)), run_time=0.3)
            refit(self, t, 2, [api, dead], TOP, tag0, run_time=0.7)
            self.play(FadeIn(qc, scale=0.9), run_time=0.6)
            vo.wait_until("why is its address dead too")
            self.play(Indicate(qc.body[1], color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("We answer it once")
            self.play(ReplacementTransform(qc, note_), FadeOut(t), run_time=0.9)
            self.remove(*t.get_family())

        # ========================================================== 3. the goal: slide 7
        md = MasterDiagram()
        ref7 = lref("7")
        ref7.move_to([note_.get_left()[0] - 0.25 - ref7.width / 2, 3.6 - ref7.height / 2, 0])
        ill = illustration_tag().move_to([-6.45, -3.15, 0], aligned_edge=LEFT)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(ref7), run_time=0.4)
            lap = md._make("laptop", title="Local Computer")
            lap.squares.shift(RIGHT * 0.03)         # the piece's 'Containers' word touches the squares
            lap[4].shift(LEFT * 0.1)
            assert lap.squares.get_right()[0] < lap.frame.get_right()[0] - 0.15   # clear of the hollow arrow
            assert lap[4].get_left()[0] > lap.frame.get_left()[0] + 0.05
            assert lap[4].get_right()[0] < lap.squares.get_left()[0] - 0.05
            md.parts["laptop"] = lap
            md.show(self, lap, run_time=0.6)
            md.gcp(self)
            md.vm(self)
            self.play(FadeIn(ill), run_time=0.3)
            vo.wait_until("the containers from your laptop")
            self.play(Indicate(md.parts["laptop"].squares, color=CONTAINER, scale_factor=1.15), run_time=0.7)
            md.heal(self)
            vo.wait_until("move to one virtual machine")
            md.hollow(self)
            for k in ("nginx", "api", "front", "vdb"):
                md.box(self, k)
            vo.wait_until("with port 80 the only door")
            md.door(self, on="vm")
            md.browser(self)
            md.routes(self)
            for cue in ("by hand", "then as code"):      # one YELLOW pulse of the VM per build
                vo.wait_until(cue)
                self.play(md.light("vm"), run_time=0.35)
                self.play(md.normal("vm"), run_time=0.35)
        assert md.parts["browser"].get_top()[1] < note_.get_bottom()[1] - 0.05
        assert md.parts["laptop"].get_right()[0] < ref7.get_left()[0] or \
            md.parts["laptop"].get_top()[1] < ref7.get_bottom()[1]

        # ========================================================== 4. the roadmap, slides 4–5
        rm = roadmap()
        pl = problem_line()
        ref45 = lref("4–5")
        ref45.move_to([note_.get_left()[0] - 0.25 - ref45.width / 2, 3.6 - ref45.height / 2, 0])
        lap_keep = md.parts["laptop"]
        assert rm.arrow.get_top()[1] < note_.get_bottom()[1] - 0.05, (rm.arrow.get_top(), note_.get_bottom())
        with self.voiceover(SAY[4]) as vo:
            md._detach(lap_keep)              # the laptop comes back in beat 5: keep it out of the slide-away
            self.play(FadeOut(md, shift=LEFT * 3), FadeOut(lap_keep, shift=LEFT * 3),
                      ReplacementTransform(ref7, ref45), FadeOut(ill), run_time=0.6)
            self.remove(lap_keep)
            self.play(FadeIn(VGroup(rm.arrow, rm.phases, rm.bounds)), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in rm.bars.values()], lag_ratio=0.15),
                      run_time=0.9)
            self.play(Create(rm.marker), run_time=0.5)
            vo.wait_until("to deployment, scaling and automation")
            dep = rm.bars["Deployment, Scaling & Automation"]
            self.play(rm.marker.animate.move_to(dep).stretch_to_fit_width(dep[0].width + 0.2), run_time=1.0)
            self.play(dep[0].animate.set_stroke(TURN), run_time=0.4)
            vo.wait_until("Everything so far")
            self.play(FadeIn(pl.lap), FadeIn(pl.lap_t), run_time=0.5)
            self.play(Create(pl.tick), run_time=0.4)
            vo.wait_until("Users need a server")
            self.play(GrowArrow(pl.arrow), FadeIn(pl.srv, shift=LEFT * 0.2), FadeIn(pl.srv_t), run_time=0.6)
            self.play(FadeIn(pl.q, scale=1.4), run_time=0.4)
            self.play(FadeOut(note_), run_time=0.4)

        # ========================================================== 5. what you need
        lap_keep.move_to([-6.45 + lap_keep.width / 2, 0, 0])
        cost = cost_tag(COST_TEXT)
        chips = VGroup(*[grey_chip(s) for s in CHIPS], cost).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        chips.move_to([-2.85 + chips.width / 2, 0, 0])
        assert chips.get_right()[0] < 6.5, chips.get_right()
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(rm, pl, ref45)), run_time=0.5)
            self.play(FadeIn(lap_keep, shift=RIGHT * 0.3), run_time=0.5)
            for c, cue in zip(chips, CHIP_CUES):
                vo.wait_until(cue)
                start = c.copy().move_to(lap_keep.get_right() + RIGHT * c.width / 2).set_opacity(0)
                self.play(ReplacementTransform(start, c), run_time=0.6)
            vo.wait_until("so each part ends by deleting everything")
            flash_tag(self, cost, COST)

        # ========================================================== 6. how to read the screen
        trk = tracker_m(2)
        panel = code(NGINX, 35, 44, font_size=20, dedent=True, cuts={36: "# Remove the rewrite"}, shown="nginx.conf")
        tS = term(P_LAPTOP, rows=2, title=T_LAPTOP)
        panel.move_to([0, (TRACK_BOTTOM - 0.1 + tS.box.get_top()[1] + 0.1) / 2, 0])
        assert panel.get_top()[1] < TRACK_BOTTOM - 0.05 and panel.get_bottom()[1] > tS.box.get_top()[1] + 0.05, \
            (panel.get_top(), panel.get_bottom(), tS.box.get_top())
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(chips, lap_keep)), run_time=0.5)
            self.play(FadeIn(trk, shift=RIGHT * 0.3), run_time=0.6)
            self.play(Indicate(trk.caption, color=TURN, scale_factor=1.06), run_time=0.8)
            self.add(trk)
            vo.wait_until("code panels name their file and lines")
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(panel.header, color=INK, scale_factor=1.1), run_time=0.8)
            self.add(panel)
            vo.wait_until("and a yellow tag")
            self.play(FadeIn(tS), run_time=0.3)
            ln = type_cmd(self, tS, LOGIN, type_time=0.8)
            turn = on_bar(tS, turn_row())      # the command row has no room beside it
            self.play(FadeIn(turn, shift=LEFT * 0.1), run_time=0.4)
            tS.add(turn)
            vo.wait_until("means pause and run it")
            flash_tag(self, turn, TURN)
            self.add(tS)

        # ========================================================== 7. one honest note
        glyph = term_glyph(2.0)
        left = VGroup(label("a machine you own", 24, INK), label("→ real, complete", 24, OWN)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        right = VGroup(label("Google · Docker Hub", 24, INK), label("→ stops at its first honest error", 24, ERR)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        tick = check_glyph(0.34)
        dot = Dot(radius=0.12, color=ERR)
        cloud = cloud_shape(None, CLOUD, cloud_w=2.0)
        lcol = VGroup(glyph, VGroup(tick, left).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.35)
        rcol = VGroup(cloud, VGroup(dot, right).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.35)
        cols = VGroup(lcol, rcol).arrange(RIGHT, buff=0.9, aligned_edge=UP)
        rcol[0].align_to(lcol[0], DOWN)               # icons on one baseline,
        rcol[1].match_y(lcol[1])                      # the two text rows level
        foot = label("and we say what yours prints", 22, S.GREY)
        inner = VGroup(cols, foot).arrange(DOWN, buff=0.4)
        frame = outline_box(inner.width + 0.9, inner.height + 0.8, S.GREY, solid=True, fill_opacity=0.08)
        frame.move_to(ORIGIN)
        inner.move_to(frame)
        sep = DashedLine(frame.get_top() + DOWN * 0.3, foot.get_top() + UP * 0.2, color=S.GREY, stroke_width=2)
        sep.set_x((lcol.get_right()[0] + rcol.get_left()[0]) / 2)
        assert frame.width < 13.0 and frame.height < 7.0, (frame.width, frame.height)
        glyph_start = glyph.copy().move_to(ORIGIN + UP * 0.2)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(trk, panel, tS)), run_time=0.5)
            self.play(FadeIn(glyph_start, scale=1.3), run_time=0.5)
            vo.wait_until("our recording machine has no Google account")
            self.play(FadeIn(frame), ReplacementTransform(glyph_start, glyph), run_time=0.8)
            self.play(Create(sep), FadeIn(cloud, shift=DOWN * 0.2), FadeIn(right[0]), run_time=0.5)
            vo.wait_until("What runs on a machine you own is real")
            self.play(FadeIn(left, shift=UP * 0.15), run_time=0.5)
            self.play(Create(tick), run_time=0.4)
            vo.wait_until("every cloud step stops")
            self.play(FadeIn(right[1], shift=UP * 0.15), FadeIn(dot, scale=1.5), run_time=0.5)
            vo.wait_until("and we say what yours prints")
            self.play(FadeIn(foot, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(foot, color=INK, scale_factor=1.06), run_time=0.7)
        self.play(FadeOut(VGroup(frame, sep, glyph, cloud, left, right, tick, dot, foot)), run_time=0.6)
        self.wait(0.3)
