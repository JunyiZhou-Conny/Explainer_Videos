"""S01 · Who gets to say no? (cold open of AC215 L9) — the reference scene for common.py.

Beats (script.md, ## S01; one voiceover block each):
0. Black frame, no tracker. CODE(cheese-app-ci-cd-history/c3b227f-service.py: 38–48), header
   `c3b227f · service.py · lines 38–48` (the script's 38–50 crops to 11 lines: 49 is 78 characters
   and the panel may not exceed the frame or 12 lines). On "The distance from a point" the
   docstring's `sqrt(x^2 + y^2)` (line 40) is underlined WHITE; on "This line takes" line 44
   `result = math.sqrt(2 * z)` glows RED; on "just wrong" its `2 *` wiggles. A GREY chip under the
   panel: "committed live, in class" (source: git-log-oneline.txt, c3b227f "demo class 1").
1. The lecture tag `Lecture 9 · slides 41, 98–99` (top right, until the checklist). The panel dims
   and turns into a GREY envelope "your commit" (V1, CommitGate(5)) beside a HISTORY vault; on
   "Before that commit exists" it slides toward the vault; on "who gets to say no" an unlabeled
   turnstile of five empty arches drops between them and the envelope stops. On "a gate," a GREY
   label "a gate" lands on the turnstile. On "watch it refuse" the envelope passes two arches
   (GREEN), the third turns RED, and it bounces back.
2. The words fade; the text-free gate shrinks to the bottom-right corner. 26 GREY tiles (slides
   4–6 redrawn, no tag): on "the model is a few tiles" 9 light GREEN ("data and model"); on "the
   rest is engineering" the other 17 pulse with the GREY caption "engineering"; on "and the hook
   that runs them" the corner gate pulses.
3. Checklist card, rows as named: ✓ your clone of cheese-app-ci-cd · ✓ Docker Desktop running ·
   ✓ Python 3.9 or newer (GREY checks: your laptop) · GREEN ✗ no cloud, no credentials, no bill.
4. Layout preview: tracker A (step 1) top-left in a YELLOW ring; the ring cycles the six trackers
   A–D (on "4 from the cheese README"), E ("1 for the guest lecture"), F ("1 for cleanup", where
   it stays: step 1 of 3: container ls). A 2-row strip (GREY tag "preview", prompt
   student@laptop:~$) types `docker container ls` with the YELLOW `▶ your turn` row tag; that tag
   clears, then `ls -la` with the GREY `extra` row tag (the tracker caption gains " · extra").
   No footer. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (ERR, INK, LAPTOP, NARRATION, P_LAPTOP_HOME, TURN, VENV, CommitGate, check_mark,
                    code, code_span, cross_mark, extra_row, grey_chip, label, line_bar, lref, mono,
                    pin, preview_tag, beside, swap_tracker, term, track, tracker, turn_row, type_cmd,
                    under, unpin)
from explainer import style as S

SAY = NARRATION["S01"]
SRC = "cheese-app-ci-cd-history/c3b227f-service.py"
FIRST, LAST, BUG = 38, 48, 44


def tracker_ring(tr, stroke: float = 3, opacity: float = 1.0) -> RoundedRectangle:
    """The YELLOW ring around the tracker's place: fixed top-left corner, as wide as `tr`."""
    x0, y0 = -6.58, 3.58
    x1, y1 = tr.get_right()[0] + 0.2, tr.get_bottom()[1] - 0.1
    r = RoundedRectangle(width=x1 - x0, height=y0 - y1, corner_radius=0.14, stroke_color=TURN,
                         stroke_width=stroke, stroke_opacity=opacity)
    return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def tile_grid() -> tuple[VGroup, list[int]]:
    """26 tiles (slides 4 and 6: 26 aspects of an ML project) in rows of 7, 7, 6, 6; returns the
    tiles and the indices of the 9 ML ones (Data 4, Model 5) as one block in the middle."""
    tiles = VGroup()
    for n in (7, 7, 6, 6):
        row = VGroup(*[RoundedRectangle(width=0.82, height=0.5, corner_radius=0.08, stroke_color=S.GREY,
                                        stroke_width=2).set_fill(S.GREY, 0.18) for _ in range(n)])
        tiles.add(row.arrange(RIGHT, buff=0.16))
    tiles.arrange(DOWN, buff=0.16)
    flat = VGroup(*[t for row in tiles for t in row])
    ml = [8, 9, 10, 11, 14, 15, 16, 17, 18]          # row 2: cols 2-5 (data), row 3: cols 1-5 (model)
    return flat, ml


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == 5, len(SAY)

        # ========================================================== 0. the line that was wrong
        panel = code(SRC, FIRST, LAST)                          # 22 pt, 13.0 wide
        panel.move_to([0, 0.75, 0])
        bug = BUG - FIRST
        doc = code_span(panel.code, 40 - FIRST, "sqrt(x^2 + y^2)")
        doc_line = under(doc, INK, stroke=3)
        bar = line_bar(panel.code, bug, ERR, 0.22)
        bug_span = code_span(panel.code, bug, "math.sqrt(2 * z)")
        two = code_span(panel.code, bug, "2 *")
        note = grey_chip("committed live, in class")
        note.next_to(panel, DOWN, buff=0.3).align_to(panel, RIGHT)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(panel, shift=UP * 0.2), run_time=1.0)
            vo.wait_until("committed, live")
            self.play(FadeIn(note, shift=LEFT * 0.2), run_time=0.6)
            vo.wait_until("The distance from a point")
            self.play(Create(doc_line), Indicate(doc, color=INK, scale_factor=1.08), run_time=1.0)
            vo.wait_until("This line takes")
            self.play(FadeIn(bar), bug_span.animate.set_color(ERR), run_time=0.7)
            self.play(Indicate(bug_span, color=ERR, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Nothing crashed")
            self.play(bar.animate.set_fill(ERR, 0.32), run_time=0.5)
            self.play(bar.animate.set_fill(ERR, 0.22), run_time=0.5)
            vo.wait_until("just wrong")
            self.play(Wiggle(two, scale_value=1.25), run_time=0.9)

        # ========================================================== 1. a commit, a gate, a vault
        gate = CommitGate(5)
        gate.move_to([0, -0.6, 0]).shift(UP * (-1.2 - gate.floor.get_center()[1]))
        gate.envelope.shift(LEFT * 1.3)            # it starts further left and slides in
        ref = lref("41, 98–99")
        word = label("a gate", 26, S.GREY).next_to(gate.turnstile, UP, buff=0.3)
        start = VGroup(panel, note, bar, doc_line)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(ref), start.animate.set_opacity(0.35), run_time=0.6)
            # the code becomes the commit: the panel folds into the envelope
            self.play(FadeTransform(start, gate.envelope), FadeIn(gate.vault), FadeIn(gate.floor),
                      run_time=1.2)
            vo.wait_until("Before that commit exists")
            self.play(gate.envelope.animate.shift(RIGHT * 0.8), run_time=1.2, rate_func=linear)
            vo.wait_until("who gets to say no")
            self.play(gate.drop_in(run_time=0.9), gate.approach(run_time=0.9))
            vo.wait_until("a gate,")
            self.play(FadeIn(word, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("anything that can fail")
            self.play(Indicate(gate.turnstile, color=S.GREY, scale_factor=1.05), run_time=0.8)
            vo.wait_until("watch it refuse")
            gate.refuse(self, 2, "fail", run_time=0.3)

        # ========================================================== 2. most of it is engineering
        tiles, ml = tile_grid()
        tiles.move_to([0, 0.75, 0])
        ml_tiles = VGroup(*[tiles[i] for i in ml])
        rest = VGroup(*[t for i, t in enumerate(tiles) if i not in ml])
        cap_ml = VGroup(RoundedRectangle(width=0.36, height=0.24, corner_radius=0.05, stroke_color=VENV,
                                         stroke_width=2).set_fill(VENV, 0.55), label("data and model", 24, VENV))
        cap_ml.arrange(RIGHT, buff=0.15)
        cap_en = VGroup(RoundedRectangle(width=0.36, height=0.24, corner_radius=0.05, stroke_color=S.GREY,
                                         stroke_width=2).set_fill(S.GREY, 0.18), label("engineering", 24, S.GREY))
        cap_en.arrange(RIGHT, buff=0.15)
        caps = VGroup(cap_ml, cap_en).arrange(RIGHT, buff=0.8).next_to(tiles, DOWN, buff=0.45)
        texts = VGroup(word, gate.envelope.text, gate.vault.text)

        with self.voiceover(SAY[2]) as vo:
            # words off first (and out of their parents, so they never snap back), then the
            # text-free gate shrinks into the bottom-right corner
            self.play(FadeOut(texts), gate.turnstile.mark_all(["idle"] * 5), run_time=0.5)
            gate.envelope.remove(gate.envelope.text)
            gate.vault.remove(gate.vault.text)
            self.remove(word)
            k = 0.32
            corner = [6.4 - gate.width * k / 2, -3.45 + gate.height * k / 2, 0]
            self.play(gate.animate.scale(k).move_to(corner),
                      LaggedStart(*[FadeIn(t, scale=0.8) for t in tiles], lag_ratio=0.03), run_time=1.4)
            vo.wait_until("the model is a few tiles")
            self.play(ml_tiles.animate.set_fill(VENV, 0.55).set_stroke(VENV), FadeIn(cap_ml, shift=UP * 0.15),
                      run_time=0.8)
            vo.wait_until("the rest is engineering")
            self.play(FadeIn(cap_en, shift=UP * 0.15), Indicate(rest, color=INK, scale_factor=1.04), run_time=1.0)
            vo.wait_until("Today is that engineering")
            self.play(rest.animate.set_stroke(INK, 2.5), ml_tiles.animate.set_fill(VENV, 0.25), run_time=0.8)
            vo.wait_until("and the hook that runs them")
            self.play(Indicate(gate, color=TURN, scale_factor=1.15), run_time=0.9)

        # ========================================================== 3. what you need
        def row(mark, *parts):
            g = VGroup(mark, *parts).arrange(RIGHT, buff=0.2)
            for p in parts[1:]:
                p.align_to(parts[0], DOWN)
            return g

        rows = [
            row(check_mark(0.32, LAPTOP), label("your clone of", 28, INK), mono("cheese-app-ci-cd", 26, INK)),
            row(check_mark(0.32, LAPTOP), label("Docker Desktop running", 28, INK)),
            row(check_mark(0.32, LAPTOP), label("Python 3.9 or newer", 28, INK)),
            row(cross_mark(0.3, VENV), label("no cloud, no credentials, no bill", 28, VENV)),
        ]
        body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        frame = RoundedRectangle(width=body.width + 1.0, height=body.height + 0.8, corner_radius=0.18,
                                 stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        card = VGroup(frame, body).move_to([0, 0.2, 0])
        body.move_to(frame)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(tiles, caps, gate, ref)), run_time=0.6)
            self.remove(tiles, caps, gate, ref)
            self.play(FadeIn(frame, scale=0.96), run_time=0.5)
            for r, anchor in zip(rows, ("your own clone", "Docker Desktop running", "Python 3.9",
                                        "No cloud")):
                vo.wait_until(anchor)
                self.play(FadeIn(r, shift=RIGHT * 0.25), run_time=0.5)
            vo.wait_until("which is the point")
            self.play(Indicate(rows[3], color=VENV, scale_factor=1.06), run_time=0.9)

        # ========================================================== 4. how to follow along
        trs = {k: tracker(k, 1) for k in "ABCDEF"}
        tr = trs["A"]
        rng = tracker_ring(tr)
        strip = term(P_LAPTOP_HOME, rows=2, title="laptop")
        prev = preview_tag()
        prev.next_to(strip.box, UP, buff=0.15).align_to(strip.box, LEFT)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(card), run_time=0.5)
            self.remove(card)
            self.play(FadeIn(tr, shift=DOWN * 0.15), Create(rng), run_time=0.8)
            vo.wait_until("6 sections today")
            self.play(Indicate(rng, color=TURN, scale_factor=1.03), run_time=0.7)
            vo.wait_until("4 from the cheese README")
            for k in "BCD":
                new = trs[k]
                tr = swap_tracker(self, tr, new, Transform(rng, tracker_ring(new)), run_time=0.45)
            vo.wait_until("1 for the guest lecture")
            tr = swap_tracker(self, tr, trs["E"], Transform(rng, tracker_ring(trs["E"])), run_time=0.5)
            vo.wait_until("1 for cleanup")
            tr = swap_tracker(self, tr, trs["F"], Transform(rng, tracker_ring(trs["F"])), run_time=0.5)
            vo.wait_until("When the yellow")
            self.play(FadeIn(strip), FadeIn(prev, shift=RIGHT * 0.2), rng.animate.set_stroke(opacity=0.35),
                      run_time=0.6)
            ln1 = type_cmd(self, strip, "docker container ls", type_time=0.8)
            yt = beside(turn_row(), ln1)
            pin(self, ln1, yt)
            vo.wait_until("pause and run")
            self.play(Indicate(yt, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("A gray extra tag")
            unpin(self, ln1, yt)
            ln2 = type_cmd(self, strip, "ls -la", type_time=0.5)
            xt = beside(extra_row(), ln2)
            pin(self, ln2, xt, anim=AnimationGroup(FadeIn(xt, shift=LEFT * 0.1), track(tr, extra=True),
                                                   Transform(rng, tracker_ring(tracker("F", 1, True), opacity=0.35))))
            vo.wait_until("marks a check")
            self.play(Indicate(xt, color=S.GREY, scale_factor=1.15), run_time=0.8)
            vo.wait_until("Every command")
            self.play(FadeOut(rng), run_time=0.6)
            self.remove(rng)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
