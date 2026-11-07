"""S05 · Six jobs, one graph (AC215 L21). TRACKER P5 2 → 2 · extra → 3. Lecture: 21 · slides 26–27
(beats 2–4 only).

Beats (script.md "## S05", one voiceover block each):
0. TRACKER P5 2. README(285–287) card at the top. Six job chips in two rows, one per name as it is
   said: the job id (GREY mono) above its ci.yml `name:` (WHITE).
1. The card shrinks into the tracker caption. The six names pulse YELLOW together, the ids dim; a
   GREY chip "GitHub shows the names · S15".
2. LECTURE 21 · 26–27. The chips clear. Slide 26's row at full size (V2 PipelineStrip): `Commit`
   drops out of the row and turns PINK with a chip "the event, not a job"; `Build Container` slides
   to the left edge and becomes the graph's `build` node.
3. V4 JobGraph, S05 form. Commit leaves; the row leaves a GREY dashed ghost. `Lint and Format`
   slides into the bottom lane, `Test` splits into `unit-tests`, `integration-tests`, `system-tests`.
   A one-line CODE(ci.yml) strip (bottom left) shows line 44, 73, 108, 131 in turn (YELLOW bar), one
   needs arrow drawing from build for each; the four lanes turn BLUE: "each on its own machine".
4. The strip becomes CODE(ci.yml 175–176) (`needs: [...]`, `if: always()`); `Summary` becomes
   `test-summary` and three arrows draw from the test jobs. The lint node pulses, the GREY dashed
   gap with a YELLOW "?" appears; the ghost row shrinks top-left with a GREY erratum chip "a straight
   row → a graph"; the four lanes pulse, the three needs arrows flash PINK, the "?" flashes.
5. LECTURE off. TRACKER P5 2 · extra. The graph folds into a text-free mini graph at the top (a
   full terminal and a picture never share the frame); an 8-row laptop terminal types `act -l`
   (row tag "extra", chip "act 0.2.97 · at the time of recording" on the bar) and prints laptop/61
   lines 3–9 (Stage, Job ID, Job name only). On each "Stage N" its rows get a YELLOW bar, the mini
   graph's column pulses and a GREY "stage N" label appears above it.
6. TRACKER P5 3. Terminal and labels go; the mini graph unfolds back into the graph. README(332–342)
   as five GREY chips under it, each flying to its place as named: Artifact Sharing + Unique Image
   Tags → above build (GREY "S08"); Parallel Execution → above the four lanes (they pulse);
   Conditional Execution + Network Modes → right of the dashed gap, system-tests ringed YELLOW and
   pulsing with them (GREY "S10"; no connector: any line there would cross the gap and its "?").
7. RECORDED(screenshot): each node stretches into its Gantt bar (Transform node → bar), tag
   "recorded · README screenshot"; the bars' labels and times appear; the critical path glows
   YELLOW with the WHITE ruler "about 2 min on the clock"; the GOLD billed row (six one-minute
   blocks, "about 6 billed minutes") and the GOLD cost tag. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ the real sources (checked)
CI = ".github/workflows/ci.yml"
NEEDS_LINES = (("lint-and-format", 44), ("unit-tests", 73), ("integration-tests", 108), ("system-tests", 131))
for _j, _n in NEEDS_LINES:
    assert excerpt(CI, _n, _n).strip() == "needs: build", (_j, _n)
assert excerpt(CI, 175, 175).strip() == "needs: [unit-tests, integration-tests, system-tests]"
assert excerpt(CI, 176, 176).strip() == "if: always()"
for _j, _name in JOBS:
    assert f"name: {_name}" in source_text(CI), _name
assert "6 jobs" in readme(287) and "except for dependencies" in readme(287)
CONCEPTS = {"Artifact Sharing": 334, "Parallel Execution": 336, "Conditional Execution": 338,
            "Unique Image Tags": 340, "Network Modes": 342}
for _c, _n in CONCEPTS.items():
    assert readme(_n).startswith(f"**{_c}**"), (_c, readme(_n))

CAP61 = capture("laptop/61")
assert CAP61.cmd_lines == ["act -l"] and CAP61.exit == 0, CAP61.cmd_lines
ACT_ROWS = cols(CAP61.at((3, 9)), ["Stage", "Job ID", "Job name"])
assert ACT_ROWS[0].split() == ["Stage", "Job", "ID", "Job", "name"], ACT_ROWS[0]
ACT_STAGE = [r.split()[0] for r in ACT_ROWS[1:]]
ACT_JOB = [r.split()[1] for r in ACT_ROWS[1:]]
assert ACT_STAGE == ["0", "1", "1", "1", "1", "2"] and ACT_JOB[0] == "build" and ACT_JOB[-1] == "test-summary"
assert VERSIONS["act"] == "0.2.97"
assert SCREENSHOT_TIMES == {"build": 54, "lint-and-format": 22, "unit-tests": 18, "integration-tests": 20,
                            "system-tests": 39, "test-summary": 4}, SCREENSHOT_TIMES

NAME_CUES = ("Build Docker Image", "Lint and Format Check", "Unit Tests", "Integration Tests",
             "System Tests", "and Test Summary")
GRAPH_Y = 0.1


def job_chip(j: str) -> VGroup:
    """Beat 0's chip: the job id (GREY mono 20) above its ci.yml name (WHITE 22). .id .name .frame"""
    i = mono(j, 20, S.GREY)
    n = label(JOB_NAME[j], 22, INK)
    inner = VGroup(i, n).arrange(DOWN, buff=0.14)
    fr = RoundedRectangle(width=3.75, height=inner.height + 0.36, corner_radius=0.14, stroke_color=S.GREY,
                          stroke_width=2).set_fill(PANEL, 1)
    inner.move_to(fr)
    g = VGroup(fr, inner)
    g.frame, g.id, g.name = fr, i, n
    return g


def recolor_node(nd, color, stroke: float = 3.0):
    """ANIM: a graph node's frame takes `color` (the whole node is transformed, text stays on top)."""
    new = nd.copy()
    new.frame.set_stroke(color, stroke)
    return Transform(nd, new)


def textless(m) -> VGroup:
    """A copy of `m` with every Text taken out (it may shrink: no small text)."""
    c = m.copy()

    def strip(g):
        for s in list(g.submobjects):
            if isinstance(s, (Text, MarkupText)):
                g.remove(s)
            else:
                strip(s)

    strip(c)
    return c


class SixJobs(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S05"] == 8, len(SAY)

        # ========================================================== 0. the README: six jobs
        tr = tracker_p5(2)
        card = readme_panel(285, 287).move_to([0, 1.95, 0])
        chips = {j: job_chip(j) for j in JOB_IDS}
        row1 = VGroup(*[chips[j] for j in JOB_IDS[:3]]).arrange(RIGHT, buff=0.3)
        row2 = VGroup(*[chips[j] for j in JOB_IDS[3:]]).arrange(RIGHT, buff=0.3)
        VGroup(row1, row2).arrange(DOWN, buff=0.35).move_to([0, -0.85, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(card, shift=UP * 0.2), Indicate(tr.caption, color=TURN, scale_factor=1.05),
                      run_time=0.6)
            vo.wait_until("6 jobs that run in parallel")
            self.play(Circumscribe(card.rows[287], color=TURN, buff=0.08), run_time=0.9)
            vo.wait_until("Each has an ID and a name")
            self.play(Indicate(card.rows[287], color=INK, scale_factor=1.03), run_time=0.6)
            for j, cue in zip(JOB_IDS, NAME_CUES):
                vo.wait_until(cue)
                self.play(FadeIn(chips[j], shift=UP * 0.2), run_time=0.4)

        # ========================================================== 1. remember the names
        names = VGroup(*[chips[j].name for j in JOB_IDS])
        ids = VGroup(*[chips[j].id for j in JOB_IDS])
        s15 = grey_chip("GitHub shows the names · S15", size=22).move_to([0, -2.85, 0])
        with self.voiceover(SAY[1]) as vo:
            # the card shrinks into the tracker caption (no text morph: a morph garbles the caption)
            self.play(FadeOut(card, scale=0.15, target_position=tr.caption.get_center()),
                      Indicate(tr.caption, color=TURN, scale_factor=1.05), run_time=0.6)
            self.remove(card, *card.get_family())
            self.add(tr)
            vo.wait_until("GitHub shows them")
            self.play(names.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(names, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("not the IDs")
            self.play(ids.animate.set_color(S.GREY_DARK), run_time=0.5)
            vo.wait_until("and we'll need them")
            self.play(FadeIn(s15, shift=UP * 0.2), run_time=0.4)
            flash_tag(self, s15, INK)

        # ========================================================== 2. slide 26's row: commit drops out
        ref = lref("26–27")
        fs = PipelineStrip(full=True).move_to([0, 2.2, 0])
        bx = list(fs.boxes)
        ghost = dashed_copy(VGroup(*[b.frame for b in bx]), S.GREY, 2.5, 9)   # the row as it was
        g = JobGraph(labels="ids", badge=False, tag_text=None, edges=False)
        # edges=False: the needs lines and the gap are not members yet, so they move with the nodes here
        VGroup(g, *g.edges.values(), g.gap, g.gap_q).shift(
            np.array([-(g.nodes["build"].get_left()[0] + g.nodes["test-summary"].get_right()[0]) / 2, GRAPH_Y, 0]))
        nd = g.nodes
        commit_spot = [bx[0].get_center()[0] + 0.25, 0.95, 0]
        ev_chip = route_chip("the event, not a job", size=22, mono_font=False)
        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(*chips.values(), s15)
            self.play(FadeOut(gone, shift=DOWN * 0.2), FadeIn(ref), run_time=0.6)
            self.remove(gone, *gone.get_family())
            vo.wait_until("Start from the lecture's row")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.15) for b in bx], lag_ratio=0.15),
                      LaggedStart(*[GrowArrow(a) for a in fs.arrows], lag_ratio=0.15), run_time=1.0)
            vo.wait_until("Commit drops out first")
            pink = bx[0].copy().move_to(commit_spot)
            pink.frame.set_stroke(ROUTE, 3).set_fill(ROUTE, 0.18)
            pink.text.set_color(ROUTE)
            self.play(Transform(bx[0], pink), FadeOut(fs.arrows[0]), run_time=0.7)
            vo.wait_until("it's the event")
            ev_chip.next_to(bx[0], RIGHT, buff=0.3)
            self.play(FadeIn(ev_chip, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("Build Container stays on the left")
            self.play(Circumscribe(bx[1], color=TURN, buff=0.06), Indicate(bx[1].text, color=TURN, scale_factor=1.08),
                      run_time=0.6)
            self.play(FadeOut(fs.arrows[1]), ReplacementTransform(bx[1], nd["build"]), run_time=0.8)
            vo.wait_until("it's the build job")
            self.play(g.pulse("build", TURN), run_time=0.6)

        # ========================================================== 3. needs lines draw the arrows
        strip = code_strip(CI, 44)
        strip.move_to([-6.4 + strip.width / 2, -2.6, 0])
        machine = VGroup(runner_icon(0.45, lit=True), label("each on its own machine", 22, GITHUB)) \
            .arrange(RIGHT, buff=0.2).move_to([3.2, -2.6, 0])
        lanes = ("unit-tests", "integration-tests", "system-tests", "lint-and-format")
        with self.voiceover(SAY[3]) as vo:
            evg = VGroup(bx[0], ev_chip)
            self.play(FadeOut(evg), FadeIn(ghost), run_time=0.5)
            self.remove(evg, *evg.get_family())
            self.play(FadeOut(VGroup(fs.arrows[2], fs.arrows[3])),
                      ReplacementTransform(bx[2], nd["lint-and-format"]),
                      ReplacementTransform(bx[3], nd["unit-tests"]),
                      TransformFromCopy(bx[3], nd["integration-tests"]),
                      TransformFromCopy(bx[3], nd["system-tests"]), run_time=1.0)
            self.remove(fs.arrows[2], fs.arrows[3])
            self.play(FadeIn(strip, shift=UP * 0.2), run_time=0.4)
            cur = strip
            bar = line_bar(cur.code, 0, TURN)
            self.play(FadeIn(bar), run_time=0.25)
            cues = ("Lint and format needs build", "Unit tests, integration tests", "integration tests and system",
                    "and system tests each need build")
            for (j, n), cue in zip(NEEDS_LINES, cues):
                vo.wait_until(cue)
                if n != 44:
                    nxt = code_strip(CI, n).move_to(cur)
                    self.play(FadeOut(bar), run_time=0.15)
                    self.remove(bar)
                    self.play(Transform(cur, nxt), run_time=0.35)
                    bar = line_bar(cur.code, 0, TURN)
                    self.play(FadeIn(bar), run_time=0.15)
                e = g.edges[("build", j)]
                self.play(Create(e), g.pulse(j, TURN), run_time=0.6)
            vo.wait_until("So after the build")
            self.play(Indicate(nd["build"], color=TURN, scale_factor=1.06), run_time=0.5)
            self.play(LaggedStart(*[g.pulse(j, TURN) for j in lanes], lag_ratio=0.15), run_time=0.9)
            vo.wait_until("each on its own machine")
            self.play(*[recolor_node(nd[j], GITHUB, 3.5) for j in lanes], FadeIn(machine, shift=UP * 0.15),
                      run_time=0.6)

        # ========================================================== 4. the summary needs only the tests
        panel = code(CI, 175, 176)
        panel.move_to([-6.4 + panel.width / 2, -2.6, 0])
        err = erratum_tag("erratum · a straight row → a graph")
        mini_ghost_w = 0.5
        test_edges = [g.edges[(j, "test-summary")] for j in TEST_JOBS]
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(bar), FadeOut(machine), run_time=0.3)
            self.remove(bar, machine)
            self.play(Transform(cur, panel), run_time=0.5)
            bars2 = VGroup(line_bar(cur.code, 0, TURN))
            self.play(FadeIn(bars2), run_time=0.3)
            self.play(ReplacementTransform(bx[4], nd["test-summary"]), run_time=0.7)
            self.play(*[Create(e) for e in test_edges], run_time=0.8)
            self.play(Indicate(nd["test-summary"].text, color=TURN, scale_factor=1.08), run_time=0.5)
            vo.wait_until("Look closely")
            self.play(Circumscribe(cur.code.code_lines[0], color=TURN, buff=0.06), run_time=0.8)
            vo.wait_until("the lint job isn't")
            self.play(g.pulse("lint-and-format", TURN), run_time=0.6)
            self.play(Create(g.gap), FadeIn(g.gap_q), run_time=0.7)
            self.remove(*g.get_family())
            g.add_to_back(*g.edges.values())
            g.add_to_back(g.gap)
            g.add(g.gap_q)
            self.add(g)
            vo.wait_until("The lecture lists the stages")
            target = ghost.copy().scale(mini_ghost_w)
            target.move_to([-6.4 + target.width / 2, 2.25, 0])
            err.next_to(target, RIGHT, buff=0.35)
            self.play(Transform(ghost, target), run_time=0.7)
            self.play(FadeIn(err, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("on GitHub, four of them")
            self.play(LaggedStart(*[g.pulse(j, GITHUB) for j in lanes], lag_ratio=0.12), run_time=0.9)
            vo.wait_until("and the summary listens")
            self.play(*[ShowPassingFlash(e.copy().set_stroke(ROUTE, 6), time_width=0.6) for e in test_edges],
                      Indicate(nd["test-summary"].text, color=ROUTE, scale_factor=1.06), run_time=0.9)
            vo.wait_until("Keep that gap in mind")
            self.play(Indicate(g.gap_q, color=TURN, scale_factor=1.5), run_time=0.7)
            self.add(g)

        # ========================================================== 5. extra: act -l, the same stages
        t = term(rows=8)
        mini_scale = 0.45
        full_sk = textless(g)
        mini = full_sk.copy().scale(mini_scale).move_to([0, 1.55, 0])
        vchip = row_tag(f"act {VERSIONS['act']} · at the time of recording")
        on_bar(t, vchip)
        stage_cols = (["build"], list(MIDDLE), ["test-summary"])
        n_off = 1 + len(g.edges)     # textless(g) keeps g's order: gap, the needs edges, the six nodes
        with self.voiceover(SAY[5]) as vo:
            old = VGroup(cur, bars2, ghost, err)
            self.play(FadeOut(old), FadeOut(ref), track(tr, 2, True), run_time=0.6)
            self.remove(old, *old.get_family(), ref)
            texts = VGroup(*[n.text.copy() for n in nd.values()])
            sk = full_sk.copy()
            self.remove(*g.get_family())
            self.add(sk, texts)
            self.play(FadeOut(texts), Transform(sk, mini), run_time=0.8)
            self.remove(texts)
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(vchip, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("a tool called act")
            cmd = type_capture(self, t, CAP61)[0]
            pin(self, cmd, beside(extra_row(), cmd))
            vo.wait_until("takes the same file")
            rows = out(self, t, ACT_ROWS)
            self.play(Indicate(rows[0], color=INK, scale_factor=1.03), run_time=0.5)
            stage_rows = ([1], [2, 3, 4, 5], [6])
            lbls = VGroup()
            col_x = (mini.get_left()[0] + (nd["build"].get_center()[0] - g.get_left()[0]) * mini_scale,
                     mini.get_left()[0] + (nd["unit-tests"].get_center()[0] - g.get_left()[0]) * mini_scale,
                     mini.get_left()[0] + (nd["test-summary"].get_center()[0] - g.get_left()[0]) * mini_scale)
            hls = VGroup()
            for k, (rr, cue) in enumerate(zip(stage_rows, ("Stage 0, build", "Stage 1, the four checks",
                                                            "Stage 2, the summary"))):
                vo.wait_until(cue)
                lb = label(f"stage {k}", 22, S.GREY).move_to([col_x[k], mini.get_top()[1] + 0.3, 0])
                hs = VGroup(*[hl_bar(rows[i], TURN, 0.25) for i in rr])
                hls.add(hs)
                self.play(FadeIn(hs), FadeIn(lb, shift=DOWN * 0.15), run_time=0.5)
                minis = VGroup(*[sk[n_off + JOB_IDS.index(j)] for j in stage_cols[k]])
                self.play(Indicate(lb, color=TURN, scale_factor=1.15), Indicate(minis, color=TURN, scale_factor=1.1),
                          run_time=0.5)
                lbls.add(lb)

        # ========================================================== 6. the key concepts on the graph
        conc = {c: grey_chip(c, size=22) for c in CONCEPTS}
        crow1 = VGroup(*[conc[c] for c in list(CONCEPTS)[:3]]).arrange(RIGHT, buff=0.3)
        crow2 = VGroup(*[conc[c] for c in list(CONCEPTS)[3:]]).arrange(RIGHT, buff=0.3)
        head = VGroup(mono("README.md", CAPTION, S.GREY), label("· lines 332–342", CAPTION, S.GREY)) \
            .arrange(RIGHT, buff=0.12)
        cblock = VGroup(head, crow1, crow2).arrange(DOWN, buff=0.22).move_to([0, -2.5, 0])
        b_c = nd["build"].get_center()
        elbow_x = g.edges[("build", "unit-tests")].get_left()[0] + 0.5 * (
            nd["unit-tests"].get_left()[0] - nd["build"].get_right()[0])        # the needs lines' vertical
        bw = max(conc["Artifact Sharing"].width, conc["Unique Image Tags"].width)
        bx_c = min(b_c[0], elbow_x - 0.2 - bw / 2)                              # clear of the needs lines
        art_pos = [bx_c, b_c[1] + 0.75, 0]
        tag_pos = [bx_c, b_c[1] + 1.35, 0]
        s08 = label("S08", 22, S.GREY).move_to([bx_c, b_c[1] + 1.95, 0])
        par_pos = [nd["unit-tests"].get_center()[0], nd["unit-tests"].get_top()[1] + 0.45, 0]
        cw = conc["Conditional Execution"].width
        c_left = min(g.gap_q.get_right()[0] + 0.45, 6.45 - cw)   # clear of the gap's '?', inside the frame
        assert c_left > g.gap_q.get_right()[0] + 0.15, c_left
        cond_pos = [c_left + cw / 2, -0.95, 0]
        net_pos = [c_left + cw / 2, -1.55, 0]
        s10 = label("S10", 22, S.GREY).move_to([c_left + cw / 2, -2.1, 0])
        sys_ring = ring(nd["system-tests"], TURN, buff=0.1)
        with self.voiceover(SAY[6]) as vo:
            gone = VGroup(t, vchip, lbls, hls)
            self.play(FadeOut(gone), track(tr, 3, False), run_time=0.5)
            self.remove(gone, *gone.get_family())
            back = full_sk.copy()
            self.play(Transform(sk, back), run_time=0.7)
            texts = VGroup(*[n.text for n in nd.values()])
            self.play(FadeIn(texts), run_time=0.4)
            self.remove(sk, texts)
            self.add(g)
            vo.wait_until("Then the key concepts")
            self.play(FadeIn(head, shift=UP * 0.15),
                      LaggedStart(*[FadeIn(c, shift=UP * 0.15) for c in conc.values()], lag_ratio=0.1),
                      run_time=0.8)
            vo.wait_until("Artifact sharing")
            self.play(FadeOut(head), conc["Artifact Sharing"].animate.move_to(art_pos),
                      conc["Unique Image Tags"].animate.move_to(tag_pos), run_time=0.8)
            self.remove(head)
            self.play(FadeIn(s08, shift=DOWN * 0.1), g.pulse("build", TURN), run_time=0.6)
            vo.wait_until("parallel execution")
            self.play(conc["Parallel Execution"].animate.move_to(par_pos), run_time=0.6)
            self.play(LaggedStart(*[g.pulse(j, TURN) for j in lanes], lag_ratio=0.12), run_time=0.8)
            vo.wait_until("conditional execution")
            self.play(conc["Conditional Execution"].animate.move_to(cond_pos),
                      conc["Network Modes"].animate.move_to(net_pos), run_time=0.8)
            pair = VGroup(conc["Conditional Execution"], conc["Network Modes"])
            self.play(Create(sys_ring), FadeIn(s10, shift=DOWN * 0.1), run_time=0.5)
            self.play(g.pulse("system-tests", TURN), Indicate(VGroup(*[c.text for c in pair]), color=TURN,
                      scale_factor=1.06), run_time=0.7)

        # ========================================================== 7. the screenshot's times
        gantt = Gantt().move_to([0, 0.35, 0])
        rtag = recorded_tag("README screenshot")
        rtag.move_to([6.4 - rtag.width / 2, gantt.get_top()[1] + 0.3, 0])
        bars = gantt.bars
        rest = VGroup(*gantt.labels.values(), *gantt.times.values())
        with self.voiceover(SAY[7]) as vo:
            notes = VGroup(*conc.values(), s08, s10, sys_ring)
            self.play(FadeOut(notes), run_time=0.4)
            self.remove(notes, *notes.get_family())
            edges = VGroup(*g.edges.values(), g.gap, g.gap_q)
            self.play(FadeOut(edges), *[ReplacementTransform(nd[j], bars[j]) for j in JOB_IDS], run_time=1.0)
            self.remove(g, *g.get_family())
            self.add(*bars.values())
            self.play(FadeIn(rest), FadeIn(rtag, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("about 2 minutes on the clock")
            gantt.critical(self)
            self.play(Create(gantt.ruler[0]), FadeIn(gantt.ruler[1], shift=UP * 0.1), run_time=0.7)
            vo.wait_until("with four jobs side by side")
            self.play(LaggedStart(*[Indicate(bars[j], color=GITHUB, scale_factor=1.05) for j in MIDDLE],
                                  lag_ratio=0.1), run_time=0.8)
            vo.wait_until("On a private repository")
            row = gantt.billed(self)
            vo.wait_until("each job is billed")
            self.play(LaggedStart(*[Indicate(b, color=COST, scale_factor=1.08) for b in row[0]], lag_ratio=0.12),
                      run_time=1.0)
            ctag = cost_tag("private repos · public: free · digest §2, not measured here")
            ctag.next_to(row, DOWN, buff=0.25).align_to(row, LEFT)
            vo.wait_until("about 6 billed minutes")
            self.play(FadeIn(ctag, shift=UP * 0.1), Indicate(row[1], color=COST, scale_factor=1.08), run_time=0.7)

        self.remove(*bars.values(), rest, gantt.ruler)
        self.add(gantt)
        everything = VGroup(gantt, rtag, ctag, tr)
        self.play(FadeOut(everything), run_time=0.6)
        self.remove(everything, *everything.get_family())
        self.wait(0.3)
