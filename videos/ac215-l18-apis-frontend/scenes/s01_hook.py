"""S01 · Who answered on port 3000? (cold open of AC215 L18, the full follow-along). No tracker until
the sample in beat 6. Lecture: 18 · 27 (Frontend), 18 · 19–21 (APIs).

Beats (script.md "## S01", one voiceover block each):
0. Black frame. A full-width terminal `laptop` (GREY row tag `extra` on its title bar) slides in and
   types d04's command exactly as captured (folds) → TERM(d04: 2, 5–7). On "port 3000" the `3000` of
   the typed URL glows PINK; on "two newsletters" line 2 `HTTP/1.1 200 OK` turns GREEN with a tick;
   on "who answered" line 5 `server: uvicorn` turns YELLOW and a PURPLE chip "the API's server ·
   port 9000" points at it.
1. The terminal shrinks to a 2-row strip at the top (the URL row with 3000, the uvicorn row). Below
   it a second terminal `laptop · branch 2025` (tag `extra · branch 2025`) types c25's command
   (folds); a GREY row tag "last year's version of the same app" sits beside its first row; on
   "port 9000" the 9000 of its URL glows PINK → TERM(c25: 2–7, wrap); both
   `access-control-allow-origin: *` lines (4, 7) turn YELLOW.
2. The two strips shrink to one row each (`server: uvicorn`; `access-control-allow-origin: *`). A
   third terminal `laptop` (tag `extra`, 20 pt so the folded command fits) types b43's line 1 (folds)
   → TERM(b43: 2–3) only (the 405 half is not shown). A GREY dashed ghost row
   "access-control-allow-origin" appears where the header would be and is struck through RED. The
   three strips fade; a YELLOW card settles in the centre: "The page talks to 3000. / The answer
   comes from 9000. / Who carried it?"
3. lecture_ref(18, "27 (Frontend)"). The card becomes a one-line strip top-left. V1 RequestTrace at
   full size (`localhost:3000/chat`, frontend-react 3000, api-service 9000, vector-db 8000, the BLUE
   dashed cloud 'Vertex AI · Gemini'; GREY `illustration` tag over the browser). Circles 1–6 light
   along the PINK arrows, each with its phrase (1–3 to the frontend, 4 in the API, 5 back from the
   3000 door, 6 the page). Then a PURPLE "?" pops up in the frontend box and circle 3½ ("the
   courier") walks the cable to the API.
4. lecture_ref(18, "19–21 (APIs)"). The trace fades except its three port numbers; V2
   ArchitectureMap appears as a GREY ghost with only the cluster drawn; on "the same three ports"
   the numbers fly onto the cluster's PINK edge labels. GREEN "App is ready!", then a RED strike and
   GREY "Well not really, / we need to build it". On "Today we build" the cluster's outline flashes
   YELLOW.
5. Lecture tag off; the map fades. Four chips, one per phrase: "cheese-app-v1 + cheese-app-v2",
   "Docker running", the GOLD-outlined disk chip "about 10 GB free · more for branch 2025", and the
   GOLD-outlined "your Google key · chat answers only".
6. The chips fade. The sample YELLOW tracker (Tutorial: Backend APIs · step 1 of 10) top-left; a small
   code panel `api/service.py · lines 43–45` in the middle; a 3-row strip (tag `preview`) types the
   README's `cd src/api-service` and a YELLOW `▶ your turn` row tag pulses beside it. Everything fades;
   empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources (checked)
D04 = capture("d04")
C25 = capture("c25")
B43 = capture("b43")
assert D04.cmd == "curl -s -i 'http://localhost:3000/api/newsletters?limit=2' | sed -n '1,8p'", D04.cmd
assert D04.line(2) == "HTTP/1.1 200 OK" and D04.line(5) == "server: uvicorn", D04.lines
assert C25.cmd.startswith("curl -s -i -L -H 'Origin: http://localhost:8080' 'http://localhost:9000/"), C25.cmd
assert C25.line(4) == C25.line(7) == "access-control-allow-origin: *", C25.lines
assert B43.at((2, 3)) == ["HTTP/1.1 200 OK", "content-type: application/json"], B43.lines
assert not any("access-control" in s for s in B43.at((2, 3)))
CD_API = readme_rows(88, 88)
assert CD_API == ["cd src/api-service"], CD_API
QUESTION = "The page talks to 3000.\nThe answer comes from 9000.\nWho carried it?"
CHIPS = ("cheese-app-v1 + cheese-app-v2", "Docker running", "about 10 GB free · more for branch 2025",
         "your Google key · chat answers only")
CHIP_CUES = ("clone both repositories", "keep Docker running", "and free about 10 gigabytes", "Your Google key")
TOP = 3.56                      # top edge of the stacked strips
GAP = 0.06


def _row_with(line_group, sub: str):
    """The row of a typed (maybe folded) command that contains `sub`."""
    for r in rows_of(line_group):
        if sub in r.text:
            return r
    raise KeyError(sub)


def refit(scene, specs, extra=(), run_time: float = 0.7):
    """PLAYS: several terminals shrink at once to `rows`, keep exactly the line mobjects in `keep`,
    and move so their top edge sits at `top`; their title-bar tag rides along.
    specs: [(terminal, rows, keep, top, bar_tag or None), ...]"""
    anims, gone_all = [], []
    for t, rows, keep, top, tg in specs:
        title = t.title.text if t.title is not None else None
        ref = Terminal(prompt=t.prompt, width=t.box.width, rows=rows, size=t.size, title=title)
        ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0], top - ref.box.get_top()[1], 0]))
        kept = [ln for ln in t.lines.submobjects if ln in keep]
        assert len(kept) == len(keep) <= rows, (len(kept), len(keep), rows)
        gone = [ln for ln in t.lines.submobjects if ln not in keep]
        for ln in gone:
            t.lines.remove(ln)
        gone_all += gone
        anims += [Transform(t.box, ref.box), Transform(t.bar, ref.bar), t.dots.animate.move_to(ref.dots)]
        if t.title is not None:
            anims.append(t.title.animate.move_to(ref.title))
        for i, ln in enumerate(kept):
            anims.append(ln.animate.shift(ref._slot(i) - ln.strut.get_corner(UL)))
        if tg is not None:
            anims.append(tg.animate.move_to(on_bar(ref, tg.copy()).get_center()))
        t.rows = rows
    scene.play(*anims, *[FadeOut(g) for g in gone_all], *extra, run_time=run_time)
    scene.remove(*gone_all)
    for t, *_ in specs:
        scene.add(t)


def glow(scene, glyphs, color=ROUTE, run_time: float = 0.6):
    """PLAYS: glyphs turn `color` with a small pulse."""
    scene.play(glyphs.animate.set_color(color).scale(1.25), run_time=run_time * 0.5)
    scene.play(glyphs.animate.scale(1 / 1.25), run_time=run_time * 0.5)


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 7, len(SAY)

        # ========================================================== 0. port 3000, and uvicorn answers
        tA = term(P_LAPTOP, rows=7, title=T_LAPTOP)
        tA.shift(UP * (0.3 - tA.box.get_center()[1]))
        tagA = on_bar(tA, extra_row())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tA, shift=RIGHT * 0.8), FadeIn(tagA, shift=RIGHT * 0.8), run_time=0.5)
            tA.add(tagA)                         # the tag rides with (and stays above) its terminal
            cmdA = type_capture(self, tA, D04, type_time=1.3)[0]
            rowA = _row_with(cmdA, "3000")
            glow(self, substring(rowA, "3000"), ROUTE)
            self.add(tA)
            vo.wait_until("It asks for two newsletters")
            outA = out(self, tA, D04.at(2, (5, 7)), run_time=0.6)
            ok_ln, srv_ln = outA[0], outA[1]
            assert ok_ln.text == "HTTP/1.1 200 OK" and srv_ln.text == "server: uvicorn"
            vo.wait_until("and gets them")
            tick = check_glyph(0.3).move_to(beside(Dot(), ok_ln, buff=0.35).get_center() + RIGHT * 0.15)
            self.play(ok_ln.animate.set_color(OWN), FadeIn(tick, scale=1.4), run_time=0.6)
            attach(self, ok_ln, tick)
            vo.wait_until("But look who answered")
            self.play(srv_ln.animate.set_color(TURN), run_time=0.5)
            self.play(Indicate(srv_ln, color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("uvicorn, the API's server")
            who = tool_chip("the API's server · port 9000", mono_font=False)
            beside(who, srv_ln, buff=1.2)
            poke = arrow(who.get_left(), srv_ln.strut.get_right() + RIGHT * 0.1, TOOL, buff=0.08)
            self.play(FadeIn(who, shift=LEFT * 0.2), GrowArrow(poke), run_time=0.6)
            attach(self, srv_ln, poke)
            attach(self, srv_ln, who)
            self.add(tA)
            vo.wait_until("and the API listens on port 9000")
            flash_tag(self, who, TOOL)
            self.add(tA)

        # ========================================================== 1. last year's version: 9000 + a slip
        tB = term(P_LAPTOP, rows=11, title=T_2025)
        hA = 2 * tA.pitch + 0.85
        tB.shift(UP * (TOP - hA - GAP - tB.box.get_top()[1]))
        assert tB.box.get_bottom()[1] >= -3.58, tB.box.get_bottom()
        tagB = on_bar(tB, extra_row("branch 2025"))
        with self.voiceover(SAY[1]) as vo:
            refit(self, [(tA, 2, [rowA, srv_ln], TOP, tagA)], run_time=0.6)
            self.play(FadeIn(tB, shift=UP * 0.3), FadeIn(tagB, shift=UP * 0.3), run_time=0.5)
            tB.add(tagB)
            cmdB = type_capture(self, tB, C25, type_time=1.6)[0]
            first = rows_of(cmdB)[0]
            last_year = beside(row_tag("last year's version of the same app"), first, buff=0.5)
            pin(self, first, last_year)
            vo.wait_until("Its page called port 9000 directly")
            glow(self, substring(_row_with(cmdB, "9000"), "9000"), ROUTE)
            self.add(tB)
            vo.wait_until("and every answer carried")
            outB = out(self, tB, C25.at((2, 7)), wrap=True, run_time=0.6)
            slips = [ln for ln in outB if ln.text == "access-control-allow-origin: *"]
            assert len(slips) == 2
            vo.wait_until("a permission slip")
            self.play(*[s.animate.set_color(TURN) for s in slips], run_time=0.5)
            self.play(LaggedStart(*[Indicate(s, color=TURN, scale_factor=1.08) for s in slips], lag_ratio=0.4),
                      run_time=1.0)

        # ========================================================== 2. this year's API: no slip
        hB = 1 * tB.pitch + 0.85
        topB = TOP - (1 * tA.pitch + 0.85) - GAP
        tC = term(P_LAPTOP, rows=10, title=T_LAPTOP, size=20)
        tC.shift(UP * (topB - hB - GAP - tC.box.get_top()[1]))
        assert tC.box.get_bottom()[1] >= -3.59, tC.box.get_bottom()
        tagC = on_bar(tC, extra_row())
        with self.voiceover(SAY[2]) as vo:
            refit(self, [(tA, 1, [srv_ln], TOP, tagA), (tB, 1, [slips[1]], topB, tagB)],
                  extra=[FadeIn(tC, shift=UP * 0.3), FadeIn(tagC, shift=UP * 0.3)], run_time=0.7)
            tC.add(tagC)
            cmdC = type_capture(self, tC, B43, type_time=1.3)[0]
            assert len(rows_of(cmdC)) == 7, len(rows_of(cmdC))
            outC = out(self, tC, B43.at((2, 3)), run_time=0.4)
            ghost = mono_line("access-control-allow-origin", 20, S.GREY)
            ghost.shift(tC._slot(len(tC.lines)) - ghost.strut.get_corner(UL))
            gbox = outline_box(ghost.width + 0.3, tC.pitch, S.GREY, solid=False).move_to(ghost)
            self.play(FadeIn(ghost), Create(gbox), run_time=0.5)
            cut_ = strike(ghost, ERR)
            self.play(Create(cut_), run_time=0.4)
            vo.wait_until("from 3000 to 9000")
            strips = VGroup(tA, tagA, tB, tagB, tC, tagC, ghost, gbox, cut_)
            qc = question_card(QUESTION).move_to(ORIGIN)
            self.play(FadeOut(strips), run_time=0.5)
            self.play(FadeIn(qc, scale=0.9), run_time=0.6)
            vo.wait_until("and why did last")
            self.play(Indicate(qc.body[2], color=TURN, scale_factor=1.1), run_time=0.8)

        # ========================================================== 3. the lecture's six steps, plus 3½
        ref1 = lref("27 (Frontend)")
        strip_q = question_card("From 3000 to 9000: who carried it?", size=22)
        strip_q.move_to([-6.5 + strip_q.width / 2, TOP - strip_q.height / 2, 0])
        tr = RequestTrace("localhost:3000/chat", rows=("front", "api", "vdb"), front="react", cloud=True)
        tr.shift(UP * 0.15)
        ill = illustration_tag().next_to(tr.browser, UP, buff=0.12).align_to(tr.browser, LEFT)
        assert strip_q.get_right()[0] < ref1.get_left()[0] - 0.2
        assert ill.get_top()[1] < strip_q.get_bottom()[1] - 0.05, (ill.get_top(), strip_q.get_bottom())
        with self.voiceover(SAY[3]) as vo:
            self.play(ReplacementTransform(qc, strip_q), FadeIn(ref1), run_time=0.8)
            self.play(FadeIn(tr), FadeIn(ill), run_time=0.8)
            vo.wait_until("request, forward")
            tr.hop(self, 1, "front", run_time=0.5)
            vo.wait_until("forward, map")
            tr.hop(self, 2, "front", run_time=0.5)
            vo.wait_until("map into a container")
            tr.hop(self, 3, "front", run_time=0.5)
            vo.wait_until("run a function")
            tr.hop(self, 4, "api", run_time=0.6)
            vo.wait_until("respond, show")
            tr.hop(self, 5, "front", run_time=0.6)
            vo.wait_until("show it")
            tr.hop(self, 6, run_time=0.6)
            vo.wait_until("We add one step")
            tr.net.set_courier(self, "?")
            self.play(Indicate(tr.net.courier, color=TOOL, scale_factor=1.25), run_time=0.7)
            vo.wait_until("three and a half")
            tr.hop(self, 3.5, text="3½ the courier", run_time=0.8)

        # ========================================================== 4. zoom out: the lecture's blueprint
        ref2 = lref("19–21 (APIs)")
        m = ArchitectureMap(built=True)
        for n in m.shown:
            if n != "cluster":
                m.layers[n].set_color(S.GREY).fade(0.55)
        cl = m.layers["cluster"]
        # in this scene the edge labels are the bare port numbers that fly over from V1 ('HTTP 3000'
        # does not fit between the cluster's frame and its arrows), and the cluster's title is one row
        # (two rows touched the NGINX box: they move up)
        e1, e2, e3 = cl[2], cl[3], cl[4]
        old = [m.ports[k] for k in ("3000", "9000", "8000")]
        labels = [mono("3000", 20, ROUTE).next_to(e1.get_center(), LEFT, buff=0.14),
                  mono("9000", 20, ROUTE).next_to(e2.get_center(), RIGHT, buff=0.14),
                  mono("8000", 20, ROUTE).next_to(e3, LEFT, buff=0.12)]
        for lb in old:
            cl.remove(lb)
        title1 = m.cluster_title
        title1.arrange(DOWN, buff=0.02).next_to(m.cluster_frame.get_top(), DOWN, buff=0.05)
        assert title1.get_bottom()[1] > m.boxes["nginx"].get_top()[1] + 0.02, (title1.get_bottom(),
                                                                               m.boxes["nginx"].get_top())
        for lb in labels:
            assert lb.get_left()[0] > m.cluster_frame.get_left()[0] + 0.05
            assert lb.get_right()[0] < m.cluster_frame.get_right()[0] - 0.05
        nums = [tr.net.doors[r].text.copy() for r in ("front", "api", "vdb")]
        assert [x.text for x in nums] == ["3000", "9000", "8000"], [x.text for x in nums]
        with self.voiceover(SAY[4]) as vo:
            self.add(*nums)
            self.play(ReplacementTransform(ref1, ref2), FadeOut(tr), FadeOut(ill), FadeOut(strip_q),
                      run_time=0.8)
            self.play(FadeIn(m), *[ReplacementTransform(a, b) for a, b in zip(nums, labels)], run_time=1.4)
            cl.add(*labels)
            self.add(m)
            vo.wait_until("with the same three ports")
            self.play(LaggedStart(*[Indicate(lb, color=ROUTE, scale_factor=1.2) for lb in labels], lag_ratio=0.3),
                      run_time=1.0)
            vo.wait_until("The lecture calls the app ready")
            m.ready(self)
            vo.wait_until("then admits")
            m.not_ready(self, run_time=0.9)
            vo.wait_until("Today we build the right-hand side")
            self.play(m.cluster_frame.animate(rate_func=there_and_back).set_stroke(TURN, width=7), run_time=1.0)
            self.add(m)
            vo.wait_until("on your laptop")
            edges = [b.frame.copy().set_fill(opacity=0) for b in m.boxes.values()]   # outline copies: the
            self.add(*edges)                                                          # names stay on top
            self.play(LaggedStart(*[e.animate(rate_func=there_and_back).set_stroke(TURN, width=6)
                                    for e in edges], lag_ratio=0.2), run_time=1.0)
            self.remove(*edges)
            self.add(m)

        # ========================================================== 5. what you need
        chips = VGroup(grey_chip(CHIPS[0], mono_font=True), grey_chip(CHIPS[1]), disk_chip(CHIPS[2]),
                       grey_chip(CHIPS[3], color=COST)).arrange(DOWN, buff=0.35).move_to(ORIGIN)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(ref2), FadeOut(m), run_time=vo.until(CHIP_CUES[0], 0.6))
            for c, cue in zip(chips, CHIP_CUES):
                vo.wait_until(cue)
                self.play(FadeIn(c, shift=UP * 0.2), run_time=0.5)
            self.play(Indicate(chips[3].text, color=COST, scale_factor=1.08), run_time=0.8)

        # ========================================================== 6. how to read the screen
        trk = tracker_b(1)
        panel = code(f"{V2}/src/api-service/api/service.py", 43, 45, shown="api/service.py")
        panel.move_to([0, 0.75, 0])
        tS = term(P_V2, rows=3, title=T_LAPTOP)
        tagS = on_bar(tS, row_tag("preview"))
        assert panel.get_top()[1] < TRACK_BOTTOM - 0.1 and panel.get_bottom()[1] > tS.box.get_top()[1] + 0.1
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(chips), run_time=0.5)
            vo.wait_until("The tracker in the corner")
            self.play(FadeIn(trk, shift=RIGHT * 0.3), run_time=0.6)
            self.play(Indicate(trk.caption, color=TURN, scale_factor=1.06), run_time=0.8)
            self.add(trk)
            vo.wait_until("code panels name their file and lines")
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(panel.header, color=INK, scale_factor=1.1), run_time=0.8)
            self.add(panel)
            vo.wait_until("and a yellow tag")
            self.play(FadeIn(tS), FadeIn(tagS), run_time=0.4)
            ln = type_lines(self, tS, CD_API, type_time=0.8)[0]
            turn = beside(turn_row(), ln, buff=0.5)
            pin(self, ln, turn)
            vo.wait_until("means pause and run it")
            flash_tag(self, turn, TURN)
            self.add(tS)
            self.play(FadeOut(VGroup(trk, panel, tS, tagS)), run_time=0.6)
        self.wait(0.3)
