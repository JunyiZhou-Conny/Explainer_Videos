"""S07 · Watch the run: six colors (AC215 L21, end of part 1). TRACKER P5 7 → 7 · extra → 8.
Lecture: 21 · slide 21 (beat 6 only, while the loop is on screen).

Beats (script.md "## S07", one voiceover block each):
0. TRACKER P5 7. README(353–357) as a five-line card (left; each row flashes as said). Right, the
   schematic Actions tab (BLUE frame, tag `illustration`): tabs with "Actions" YELLOW, one run row
   "demo class 1 · CI Pipeline · main" with a YELLOW dot; a legend row under it (YELLOW "in
   progress", GREEN ✓ "success", RED ✗ "failure") appears on its phrases; with the yellow dot, two GREY
   cards at the bottom (up ~10 s): "no run?"
   (ci.yml at the repo root · S03, branch main/develop · S04, fork: enable workflows · S06) and
   "yellow annotations? deprecation notices, the run still counts". On "Pause and open yours":
   YELLOW `▶ your turn` beside the Actions tab. Short-label graphs write Lint as "Lint and Format".
1. A GREY cursor dot clicks the run row. The README card shrinks into the tracker caption, the tab
   and the cards go; GRAPH(run1) at its start state (six GREY nodes, names), `Build Docker Image`
   turns YELLOW (running), then the four middle nodes and the summary pulse on their phrases.
2. The graph becomes the short-label graph on the right (no text is scaled down). Inset left: six
   BLUE boxes in the graph's layout, each with an empty Docker shelf; caption "a fresh machine ·
   empty Docker"; below, a GREY laptop with a PURPLE "act" chip and "second witness"; on "the same
   verdict" a GREEN tick beside each and a GREEN chip "same verdict".
3. The inset folds into a GREY note under the graph's `illustration` tag: "drawn from ci.yml · log
   lines real"; the tag flashes on "marked illustration", the note on "Every log line".
4. The graph returns to the centre (names), build YELLOW, the other five GREY. A small replay of
   S04's door (BLUE server, door, GREEN dot inside, "main") pulses on "on main"; the run badge pulses
   on "refuse it". No colors change. PONDER (8 s): the question card.
5. The card leaves. The dot in the server flashes ("it's on main"); the door icon leaves; the reveal
   from runner/run1/results.txt on each phrase: Build ✓; Lint and Format Check ✗; the three tests
   (YELLOW, then GREEN) and Test Summary ✓; the run badge ✗.
6. LECTURE 21 · 21. The graph moves left (short labels); slide 21's loop, redrawn small (Codebase →
   Build → Test, the PINK returns, the GREY "Notifications" bar, a developer), comes in on the
   right; the six marks fly from the graph onto the bar. On "And act": the loop, the tag and the
   graph go (a full terminal and a picture never share the frame), TRACKER P5 7 · extra, a 10-row
   laptop terminal types laptop/62 line 1 (extra; folds) and prints ACT(421, 513, 567, 682, 732, 749,
   750): five "Job succeeded" GREEN, 513 and 750 RED.
7. TRACKER P5 8. The terminal leaves; the short graph returns left, RECORDED(screenshot) slides in
   right (six GREEN nodes with their times, tag `recorded · README screenshot`), GREY erratum tag
   "erratum · an earlier version of the code"; the RED run badge pulses on "Your first run is red".
8. The screenshot leaves; the graph returns to the centre. The RED lint node and the GREEN summary
   node pulse together; S01's question card returns small under them: "Which machine said no, and
   why didn't the summary hear it?" Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S07"]

# ------------------------------------------------------------------ the real sources (checked)
WATCH = readme_lines(353, 357)
assert [n for n, _ in WATCH] == [353, 354, 355, 356, 357], WATCH
assert WATCH[1][1] == '2. Click the "Actions" tab'
assert WATCH[3][1] == "4. Green checkmark = success ✅" and WATCH[4][1] == "5. Red X = failure ❌", WATCH
RUN1 = results("run1")
assert RUN1 == {"build": "success", "lint-and-format": "failure", "unit-tests": "success",
                "integration-tests": "success", "system-tests": "success", "test-summary": "success"}, RUN1
C62 = capture("laptop/62")
assert C62.cmd_lines == ["act push -P ubuntu-latest=-self-hosted --artifact-server-path /tmp/act-artifacts"]
ACT_NUMS = (421, 513, 567, 682, 732, 749, 750)
ACT = act_lines(*ACT_NUMS)
assert all(s.endswith("Job succeeded") for i, s in enumerate(ACT) if i not in (1, 6)), ACT
assert ACT[1] == "[CI Pipeline/Lint and Format Check] 🏁  Job failed", ACT[1]
assert ACT[6] == "Error: Job 'Lint and Format Check' failed", ACT[6]
ACT_COL = [ERR if i in (1, 6) else PASS for i in range(len(ACT))]
QUESTION = "Which machine said no,\nand why didn't the summary hear it?"          # S01's card
PONDER_Q = ("This run turns red, as in the opening.\nIs your push on main in your repository,\n"
            "or did the red run refuse it?")

GRAPH_Y = -0.3          # the names graph, centred (12.4 wide)
# short-label graphs keep the red node's spoken name (S05: "GitHub shows them, not the IDs")
LINT_TEXT = {"lint-and-format": "Lint and Format"}


# ------------------------------------------------------------------ local helpers
def centred(g: VGroup, y: float = GRAPH_Y, x: float = 0.0) -> VGroup:
    """Centre a graph's nodes (and with them the whole graph) at (x, y)."""
    nodes = VGroup(*g.nodes.values())
    g.shift(np.array([x - nodes.get_center()[0], y - nodes.get_center()[1], 0]))
    return g


def note_card(rows, head: str, color=S.GREY, size: float = 20) -> VGroup:
    """A GREY card: a head line (GREY) and short WHITE rows. .frame .body"""
    items = [label(head, size, S.GREY)] + [label(r, size, INK) for r in rows]
    body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = box(body.width + 0.5, body.height + 0.36, color, fill=S.GREY_DARKER, fill_opacity=1)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.body = fr, body
    return g


def legend_item(state: str, text: str) -> VGroup:
    return VGroup(state_mark(state, 0.3), label(text, 20, STATE_COLOR[state])).arrange(RIGHT, buff=0.14)


def stand_in_box(bw: float = 1.3, bh: float = 0.55) -> VGroup:
    """A BLUE stand-in machine with an empty Docker shelf (text-free)."""
    fr = RoundedRectangle(width=bw, height=bh, corner_radius=0.1, stroke_color=GITHUB,
                          stroke_width=2.5).set_fill(GITHUB, 0.15)
    sh = shelf(bw * 0.62, text=None, color=S.GREY).move_to(fr).shift(DOWN * bh * 0.12)
    return VGroup(fr, sh)


def door_icon() -> VGroup:
    """S04's door, replayed small: a BLUE server with a door in its left wall and the landed GREEN dot
    on 'main'. .server .door .dot .text"""
    sv = RoundedRectangle(width=1.7, height=1.0, corner_radius=0.12, stroke_color=GITHUB,
                          stroke_width=3).set_fill(GITHUB, 0.12)
    dr = Rectangle(width=0.14, height=0.55, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.BG, 1)
    dr.move_to(sv.get_left())
    d = dot(PASS, 0.12).move_to(sv.get_center() + LEFT * 0.25)
    t = label("main", 20, PASS).next_to(d, RIGHT, buff=0.15)
    g = VGroup(sv, dr, d, t)
    g.server, g.door, g.dot, g.text = sv, dr, d, t
    return g


def mini_loop(size: float = 20) -> VGroup:
    """Slide 21's CI loop redrawn small in series colours (CiLoop is ~8.5 wide and cannot shrink
    without scaling text): Codebase → Build → Test in a GREY dashed frame, PINK dashed returns from
    Build and Test down to the GREY Notifications bar, a GREY developer left of the bar, PINK
    'commits' up into Codebase and the dashed PINK way back. .boxes{key} .bar .slot (mark area)"""
    boxes = {}
    for k, n in (("codebase", "Codebase"), ("build", "Build"), ("test", "Test")):
        t = label(n, size, INK)
        fr = RoundedRectangle(width=t.width + 0.36, height=0.56, corner_radius=0.1, stroke_color=INK,
                              stroke_width=2.5).set_fill(PANEL, 1)
        t.move_to(fr)
        b = VGroup(fr, t)
        b.frame, b.text = fr, t
        boxes[k] = b
    row = VGroup(*boxes.values()).arrange(RIGHT, buff=0.42)
    rf = outline_box(row.width + 0.36, row.height + 0.3, S.GREY).move_to(row)
    ras = VGroup(arrow(boxes["codebase"], boxes["build"], S.GREY, 2.5, 0.06),
                 arrow(boxes["build"], boxes["test"], S.GREY, 2.5, 0.06))
    bar = RoundedRectangle(width=row.width, height=0.48, corner_radius=0.1, stroke_color=S.GREY,
                           stroke_width=2.5).set_fill(S.GREY, 0.12)
    bar.next_to(row, DOWN, buff=1.0).align_to(row, LEFT)
    bt = label("Notifications", size, S.GREY).next_to(bar, DOWN, buff=0.12).align_to(bar, LEFT)
    rets = VGroup(*[DashedLine(boxes[k].get_bottom() + DOWN * 0.18, [boxes[k].get_center()[0], bar.get_top()[1] + 0.03, 0],
                               color=ROUTE, stroke_width=3.5, dash_length=0.1) for k in ("build", "test")])
    dev = person_icon(LAPTOP, 0.45).next_to(bar, LEFT, buff=0.55)
    up = dev.get_top() + UP * 0.06
    to = boxes["codebase"].get_left() + LEFT * 0.2
    com = VMobject().set_points_as_corners([up, [up[0], to[1], 0], to]).set_stroke(ROUTE, 3.5)
    tip = Arrow(to + LEFT * 0.3, to + RIGHT * 0.02, buff=0, color=ROUTE, stroke_width=3.5, tip_length=0.18,
                max_tip_length_to_length_ratio=0.6)
    back = DashedLine(bar.get_left() + LEFT * 0.04, dev.get_right() + RIGHT * 0.06, color=ROUTE, stroke_width=3.5,
                      dash_length=0.1)
    g = VGroup(rf, ras, *boxes.values(), bar, bt, rets, dev, com, tip, back)
    g.boxes, g.bar = boxes, bar
    return g


def swap_graph(scene, old: JobGraph, new: JobGraph, *extra, run_time: float = 0.9) -> JobGraph:
    """PLAYS: one graph becomes another of a different size (names <-> short labels, moved): the
    labels fade, then frames, marks, edges, badge and tag move and reshape into their new places,
    then the new labels fade in (labels are never morphed letter by letter). Leaves exactly `new`
    on the scene. `extra` animations play with the move."""
    olds = VGroup(*[old.nodes[j].text for j in JOB_IDS if old.nodes[j].text is not None])
    news = VGroup(*[new.nodes[j].text for j in JOB_IDS if new.nodes[j].text is not None])
    scene.play(FadeOut(olds), run_time=run_time * 0.25)
    moves = []
    for j in JOB_IDS:
        o, n = old.nodes[j], new.nodes[j]
        moves += [ReplacementTransform(o.frame, n.frame), ReplacementTransform(o.mark, n.mark)]
    for k, e in old.edges.items():
        moves.append(ReplacementTransform(e, new.edges[k]))
    for a, b in ((old.badge, new.badge), (old.tag, new.tag)):
        if a is not None and b is not None:
            moves.append(ReplacementTransform(a, b))
    scene.play(*moves, *extra, run_time=run_time * 0.5)
    scene.play(FadeIn(news), run_time=run_time * 0.25)
    scene.remove(old, *old.get_family())
    scene.add(new)
    return new


class WatchTheRun(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S07"] == 9, len(SAY)

        # ========================================================== 0. the Actions tab
        tr = tracker_p5(7)
        card = readme_panel(353, 357)
        card.align_to(np.array([-6.45, 0, 0]), LEFT).align_to(np.array([0, 2.55, 0]), UP)
        # readme_panel's label font drops the emoji at the ends of lines 356 / 357: draw them (emo_line rule)
        emo = VGroup(check_mark(0.26, PASS, stroke=3.5).next_to(card.rows[356], RIGHT, buff=0.15),
                     cross_mark(0.2, ERR, stroke=3.5).next_to(card.rows[357], RIGHT, buff=0.2))
        card.add(emo)
        tab = actions_tab()
        tab.align_to(np.array([6.45, 0, 0]), RIGHT).align_to(np.array([0, 2.55, 0]), UP)
        ill = illustration_tag().next_to(tab, DOWN, buff=0.15).align_to(tab, RIGHT)
        leg = VGroup(legend_item("running", "in progress"), legend_item("success", "success"),
                     legend_item("failure", "failure")).arrange(RIGHT, buff=0.45)
        leg.next_to(ill, DOWN, buff=0.25).align_to(tab, LEFT).shift(RIGHT * 0.25)
        turn = your_turn().next_to(tab.tabs["Actions"], UP, buff=0.12).align_to(tab.tabs["Actions"], RIGHT)
        # (right of the tab it would leave the frame: the tab row ends ~1.0 from the page edge)
        norun = note_card(["ci.yml not at the repo root · S03", "branch not main / develop · S04",
                           "fork: workflows not enabled · S06"], "no run?")
        notes = note_card(["deprecation notices", "the run still counts"], "yellow annotations?")
        tips = VGroup(norun, notes).arrange(RIGHT, buff=0.5, aligned_edge=UP)
        tips.move_to([0, -2.45, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), FadeIn(card, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("go to your repository")
            self.play(FadeIn(tab, shift=LEFT * 0.2), FadeIn(ill), Indicate(card.rows[353], color=TURN,
                      scale_factor=1.05), run_time=0.7)
            vo.wait_until("and click the Actions tab")
            self.play(Indicate(card.rows[354], color=TURN, scale_factor=1.05),
                      Circumscribe(tab.tabs["Actions"], color=TURN, buff=0.08), run_time=0.8)
            vo.wait_until("Your run is listed under the commit message")
            self.play(Indicate(card.rows[355], color=TURN, scale_factor=1.05),
                      Indicate(tab.row[1], color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("with a yellow dot")
            self.play(FadeIn(leg[0], shift=UP * 0.15), Indicate(tab.mark, color=TURN, scale_factor=1.4),
                      run_time=0.7)
            self.play(LaggedStart(FadeIn(norun, shift=UP * 0.15), FadeIn(notes, shift=UP * 0.15), lag_ratio=0.4),
                      run_time=0.8)
            vo.wait_until("A green checkmark means success")
            self.play(FadeIn(leg[1], shift=UP * 0.15), Indicate(card.rows[356], color=PASS, scale_factor=1.05),
                      run_time=0.7)
            vo.wait_until("a red X means failure")
            self.play(FadeIn(leg[2], shift=UP * 0.15), Indicate(card.rows[357], color=ERR, scale_factor=1.05),
                      run_time=0.7)
            vo.wait_until("Pause and open yours")
            self.play(FadeIn(turn, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, turn)

        # ========================================================== 1. click: the graph
        cur = cursor_dot().move_to(tab.row_box.get_right() + LEFT * 0.45)
        g = centred(run_graph(None))
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(cur, scale=0.5), run_time=0.3)
            self.play(Indicate(cur, color=INK, scale_factor=1.5), Indicate(tab.row, color=TURN, scale_factor=1.03),
                      run_time=0.5)
            vo.wait_until("and GitHub draws the run")
            cap = tr.caption.copy()
            rest = VGroup(tab, ill, leg, turn, tips, cur)
            self.play(FadeTransform(card, cap), FadeOut(rest), run_time=0.6)
            self.remove(cap, card, rest, *rest.get_family())
            self.add(tr)
            self.play(FadeIn(g, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("build first")
            self.play(g.set_state("build", "running"), g.set_badge("running"), run_time=0.5)
            self.add(g)
            self.play(g.pulse("build", TURN), run_time=0.6)
            vo.wait_until("four jobs side by side")
            self.play(*[g.pulse(j, GITHUB) for j in MIDDLE], run_time=0.8)
            vo.wait_until("the summary last")
            self.play(g.pulse("test-summary", GITHUB), run_time=0.7)

        # ========================================================== 2. how we show it
        gs = JobGraph(states={"build": "running"}, labels="short", col_gap=0.3, texts=LINT_TEXT)  # narrow: inset left
        gs.shift(np.array([6.45 - gs.get_right()[0], -0.15 - VGroup(*gs.nodes.values()).get_center()[1], 0]))
        boxes = {}
        cx = {"build": -5.75, "test-summary": -2.05}
        for i, j in enumerate(MIDDLE):
            boxes[j] = stand_in_box().move_to([-3.9, 2.25 - 0.68 * i, 0])
        for j in ("build", "test-summary"):
            boxes[j] = stand_in_box().move_to([cx[j], 2.25 - 0.68 * 1.5, 0])
        mach = VGroup(*[boxes[j] for j in JOB_IDS])
        mcap = label("each: a fresh machine · empty Docker", 20, GITHUB).next_to(mach, DOWN, buff=0.3)
        mcap.align_to(np.array([-6.45, 0, 0]), LEFT)      # left edge: its tick stays clear of the graph
        lap = laptop_icon(1.0).move_to([-5.6, -1.35, 0])
        act_c = tool_chip("act").next_to(lap, RIGHT, buff=0.3)
        wit = label("second witness", 20, S.GREY).next_to(act_c, RIGHT, buff=0.25)
        tick1 = state_mark("success", 0.4).next_to(mcap, RIGHT, buff=0.2)
        tick2 = state_mark("success", 0.4).next_to(wit, RIGHT, buff=0.2)
        same = ok_chip("same verdict").move_to([mach.get_center()[0], -2.35, 0])
        inset = VGroup(mach, mcap, lap, act_c, wit, tick1, tick2, same)
        with self.voiceover(SAY[2]) as vo:
            swap_graph(self, g, gs)
            vo.wait_until("We ran every job of this file right here")
            self.play(LaggedStart(*[FadeIn(boxes[j], scale=0.7) for j in JOB_IDS], lag_ratio=0.15), run_time=1.0)
            vo.wait_until("each on a brand-new machine with an empty Docker")
            self.play(FadeIn(mcap, shift=UP * 0.1), run_time=0.4)
            self.play(LaggedStart(*[Indicate(boxes[j][1], color=GITHUB, scale_factor=1.2) for j in JOB_IDS],
                                  lag_ratio=0.1), run_time=0.8)
            vo.wait_until("as GitHub does")
            self.play(*[gs.pulse(j, GITHUB) for j in JOB_IDS], run_time=0.7)
            vo.wait_until("And a tool called act")
            self.play(FadeIn(lap, shift=RIGHT * 0.2), run_time=0.4)
            self.play(FadeIn(act_c, scale=0.8), FadeIn(wit, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("with the same verdict")
            self.play(FadeIn(tick1, scale=0.5), FadeIn(tick2, scale=0.5), FadeIn(same, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(same.text, color=PASS, scale_factor=1.08), run_time=0.6)

        # ========================================================== 3. drawings, real log lines
        note = grey_chip("drawn from ci.yml · log lines real").next_to(gs.tag, DOWN, buff=0.15).align_to(gs.tag, RIGHT)
        with self.voiceover(SAY[3]) as vo:
            vo.wait_until("are drawings built from the workflow file")
            self.play(FadeTransform(inset, note), run_time=0.9)
            self.remove(inset, *inset.get_family())
            self.add(note)
            vo.wait_until("marked illustration")
            flash_tag(self, gs.tag)
            vo.wait_until("Every log line in them is real")
            self.play(Indicate(note.text, color=INK, scale_factor=1.08), run_time=0.7)

        # ========================================================== 4. ponder: is it on main?
        g = centred(JobGraph(states={"build": "running"}, labels="names"))
        door = door_icon().move_to([5.3, 1.35, 0])
        with self.voiceover(SAY[4]) as vo:
            swap_graph(self, gs, g, FadeOut(note))
            self.remove(note)
            vo.wait_until("You already know this run turns red")
            self.play(Indicate(g.badge, color=INK, scale_factor=1.08), run_time=0.7)   # no colors change
            vo.wait_until("Is your push on main")
            self.play(FadeIn(door, scale=0.8), run_time=0.5)
            self.play(Indicate(door, color=GITHUB, scale_factor=1.08), run_time=0.6)
            vo.wait_until("or did the red run refuse it")
            self.play(Circumscribe(g.badge, color=TURN, buff=0.06), Indicate(g.badge.text, color=TURN,
                      scale_factor=1.06), run_time=0.8)
        # pause_and_ponder, narrower and left of centre so the door replay stays in view
        pc = ponder_card(PONDER_Q, width=8.6).move_to([-1.1, GRAPH_Y, 0])
        self.play(FadeIn(pc, scale=0.95), run_time=0.6)
        bar = pc[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 5. the reveal
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            self.play(Flash(door.dot, color=PASS), Indicate(door.text, color=PASS, scale_factor=1.15), run_time=0.7)
            vo.wait_until("the push landed before any job started")
            self.play(Indicate(door.dot, color=PASS, scale_factor=1.6), g.pulse("build", TURN), run_time=0.8)
            vo.wait_until("and a red run can't undo it")
            self.play(Circumscribe(door, color=PASS, buff=0.08), run_time=0.7)
            self.play(FadeOut(door, scale=0.8), run_time=0.4)
            self.remove(door)
            vo.wait_until("Build: green")
            self.play(g.set_state("build", "success"), run_time=0.4)
            self.add(g)
            vo.wait_until("Lint and Format Check: red")
            self.play(g.set_state("lint-and-format", "running"), run_time=0.25)
            self.play(g.set_state("lint-and-format", "failure"), run_time=0.4)
            self.add(g)
            vo.wait_until("The three tests and Test Summary: green")
            self.play(*[g.set_state(j, "running") for j in TEST_JOBS], run_time=0.3)
            self.play(LaggedStart(*[g.set_state(j, "success") for j in TEST_JOBS], lag_ratio=0.25), run_time=0.7)
            self.play(g.set_state("test-summary", "running"), run_time=0.25)
            self.play(g.set_state("test-summary", "success"), run_time=0.4)
            self.add(g)
            vo.wait_until("The run: red")
            self.play(g.set_badge("failure"), run_time=0.5)
            self.add(g)
            self.play(Circumscribe(g.badge, color=ERR, buff=0.06), run_time=0.6)

        # ========================================================== 6. notifications; act agrees
        gs = run_graph("run1", labels="short", col_gap=0.3, texts=LINT_TEXT)   # narrow and low: the loop's
        gs.shift(np.array([-6.45 - gs.get_left()[0], -0.6 - VGroup(*gs.nodes.values()).get_center()[1], 0]))  # developer
        lp = mini_loop()
        lp.move_to([0, 0, 0]).align_to(np.array([6.45, 0, 0]), RIGHT).align_to(np.array([0, 2.4, 0]), UP)
        ref = lref("21")
        order = ["build", "lint-and-format", "unit-tests", "integration-tests", "system-tests", "test-summary"]
        marks = VGroup(*[state_mark(RUN1[j], 0.3) for j in order]).arrange(RIGHT, buff=0.08)
        marks.move_to(lp.bar).align_to(lp.bar, RIGHT).shift(LEFT * 0.15)
        t = term(P_LAPTOP, rows=10)
        with self.voiceover(SAY[6]) as vo:
            swap_graph(self, g, gs, FadeIn(ref, shift=LEFT * 0.2))
            self.play(FadeIn(lp, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("next to your commit")
            flying = VGroup(*[gs.nodes[j].mark.copy() for j in order])
            self.add(flying)
            self.play(LaggedStart(*[Transform(f, m) for f, m in zip(flying, marks)], lag_ratio=0.12), run_time=1.2)
            vo.wait_until("are the lecture's notifications")
            self.play(Circumscribe(lp.bar, color=ROUTE, buff=0.08), Indicate(flying, color=INK, scale_factor=1.1),
                      run_time=0.8)
            vo.wait_until("And act, the second witness")
            gone = VGroup(gs, lp, flying, ref)
            self.play(FadeOut(gone), track(tr, 7, True), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            self.remove(gone, *gone.get_family())
            typed = type_capture(self, t, C62, type_time=0.8)
            last = typed[-1]
            last = last.rows[-1] if hasattr(last, "rows") else last
            xt = beside(extra_row("act"), last, buff=0.4)
            if xt.get_right()[0] <= t.box.get_right()[0] - 0.12:
                pin(self, last, xt)
            else:
                on_bar(t, xt)
                self.play(FadeIn(xt), run_time=0.3)
                t.add(xt)
            rows = out(self, t, list(zip(ACT, ACT_COL)), run_time=0.6)
            vo.wait_until("five jobs succeeded")
            ok = VGroup(*[r for r, c in zip(rows, ACT_COL) if c == PASS])
            self.play(Indicate(ok, color=PASS, scale_factor=1.03), run_time=0.7)
            vo.wait_until("one failed")
            bad = VGroup(rows[1], rows[6])
            self.play(Indicate(bad, color=ERR, scale_factor=1.04), run_time=0.7)

        # ========================================================== 7. the README's screenshot
        gs = run_graph("run1", labels="short", col_gap=0.6, texts=LINT_TEXT)
        gs.shift(np.array([-6.45 - gs.get_left()[0], 0.2 - VGroup(*gs.nodes.values()).get_center()[1], 0]))
        rec = recorded_graph()
        rec.shift(np.array([6.4 - rec.get_right()[0], 0.2 - VGroup(*rec.graph.nodes.values()).get_center()[1], 0]))
        err = erratum_tag("erratum · an earlier version of the code").next_to(rec, UP, buff=0.3)
        err.align_to(rec, RIGHT)          # above: below it would crowd the graph's illustration tag
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(t, shift=DOWN * 0.2), track(tr, 8, False), run_time=0.5)
            self.remove(t, *t.get_family())
            self.play(FadeIn(gs, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("the README's screenshot is all green")
            self.play(FadeIn(rec, shift=LEFT * 0.3), run_time=0.6)
            self.play(*[Indicate(rec.graph.nodes[j].mark, color=PASS, scale_factor=1.3) for j in JOB_IDS],
                      run_time=0.7)
            vo.wait_until("It shows an earlier version of the code")
            self.play(FadeIn(err, shift=UP * 0.15), run_time=0.4)
            flash_tag(self, err)
            vo.wait_until("Your first run is red")
            self.play(Circumscribe(gs.badge, color=ERR, buff=0.06), gs.pulse("lint-and-format", ERR), run_time=0.8)
            vo.wait_until("and in part 2 you turn it green")
            self.play(Circumscribe(rec.graph, color=PASS, buff=0.12), run_time=0.9)

        # ========================================================== 8. the hook, on your push
        g = centred(run_graph("run1"), y=0.35)
        qc = question_card(QUESTION, size=20)
        lint, summ = g.nodes["lint-and-format"], g.nodes["test-summary"]
        qc.move_to([(lint.get_center()[0] + summ.get_center()[0]) / 2, -2.75, 0])
        with self.voiceover(SAY[8]) as vo:
            gone = VGroup(rec, err)
            self.play(FadeOut(gone, shift=RIGHT * 0.3), run_time=0.5)
            self.remove(gone, *gone.get_family())
            swap_graph(self, gs, g)
            vo.wait_until("two of these six machines disagree")
            self.play(g.pulse("lint-and-format", ERR), g.pulse("test-summary", PASS), run_time=0.9)
            self.play(FadeIn(qc, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("In part 2 we open every log")
            self.play(g.pulse("lint-and-format", ERR), g.pulse("test-summary", PASS),
                      Indicate(qc.text, color=TURN, scale_factor=1.04), run_time=0.9)
            vo.wait_until("one job at a time")
            self.play(LaggedStart(*[g.pulse(j, GITHUB) for j in JOB_IDS], lag_ratio=0.3), run_time=1.6)
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=0.8)
        self.remove(*self.mobjects)
        self.wait(0.3)
