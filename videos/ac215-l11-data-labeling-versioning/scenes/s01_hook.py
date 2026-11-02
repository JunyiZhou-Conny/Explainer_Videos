"""S01 · Same names, different data? (cold open of AC215 L11) — the reference scene for common.py.

Beats (script.md, ## S01; one voiceover block each):
0. Black frame, no tracker. Two GREY folder cards slide in, 'cheese_dataset · Monday' and
   'cheese_dataset · Friday' (tag `illustration`: invented names), each listing Image_1.jpg …
   Image_4.jpg with a GREY chip '4 files'. Between them a GREY model card; on "On Friday" a RED down
   arrow and a '?' (no accuracy numbers). On "And can you get exactly", the YELLOW caption 'which
   photos, with which labels, did Monday's model see?' settles at the top.
1. Slide 24's idea redrawn (`lecture_ref(11, "20, 24")` top right to the end): a 3-row terminal strip
   (tag `illustration`, our own invented names) whose `ls` fills row by row and scrolls; a RED '?'
   stamps on the last row.
2. Dark frame; the caption shrinks to the top-left edge. One PINK line types alone, centred: the md5
   line of laptop/95:59 (HOOK_LINE), a GREY chip 'same bytes, same fingerprint'; on "pin down" a GREY
   '?' under it.
3. The PINK line fades; a WHITE envelope with the single word 'gouda' floats in, centred, under a
   GREY '?'.
4. Checklist card (✓ Docker Desktop running · ✓ a GCP project with billing + your own bucket + the
   GOLD cost tag · ✓ a GitHub account). Layout preview: tracker A (step 1) top-left in a YELLOW ring;
   on "follows both READMEs" the ring flicks through the twelve trackers A–L and back to A. A 2-row
   strip (GREY tag 'preview') types laptop/01's clone with the YELLOW `▶ your turn` row tag, then
   laptop/02's `git log` with the GREY `extra` row tag (tracker caption gains ' · extra'), then a GREY
   `recorded` chip above the strip. Tags never stacked. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (COST, HASH, HOOK_LINE, IMAGES, INK, LAPTOP, NARRATION, P_LAPTOP_HOME, SAY_COUNT, TURN, ERR,
                    annotation, beside, capture, check_mark, cost_tag, each, extra_row, flash_tag,
                    grey_chip, illustration_tag, label, lref, mono, pin, preview_tag, recorded_tag,
                    swap_tracker, term, tile, track, tracker, turn_row, type_cmd, unpin, out)
from explainer import style as S

SAY = NARRATION["S01"]
# our own invented names (slide 24's habit; tagged `illustration`), never the slide's screenshot
FINAL_FINAL = ("cheese-final.zip", "cheese-final-v2.zip", "cheese-final-final-v3.zip",
               "cheese-final-final-v3-USE-THIS.zip", "…")
CAPTION = "which photos, with which labels, did Monday's model see?"


def tracker_ring(tr, stroke: float = 3, opacity: float = 1.0) -> RoundedRectangle:
    """The YELLOW ring around the tracker's place: fixed top-left corner, as wide as `tr`."""
    x0, y0 = -6.58, 3.58
    x1, y1 = tr.get_right()[0] + 0.2, tr.get_bottom()[1] - 0.1
    r = RoundedRectangle(width=x1 - x0, height=y0 - y1, corner_radius=0.14, stroke_color=TURN,
                         stroke_width=stroke, stroke_opacity=opacity)
    return r.move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])


def folder_card(day: str) -> VGroup:
    """A GREY folder card 'cheese_dataset · <day>' listing Image_1-4.jpg and a '4 files' chip.
    .frame .head .rows (each: tile glyph + name) .chip"""
    head = VGroup(mono("cheese_dataset", 22, INK), label(f"· {day}", 22, S.GREY))
    head.arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
    rows = VGroup()
    for n in IMAGES[:4]:
        r = VGroup(tile(None, 0.4, LAPTOP), mono(n, 22, INK)).arrange(RIGHT, buff=0.18)
        rows.add(r)
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    ch = grey_chip("4 files")
    body = VGroup(head, rows, ch).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    rows.shift(RIGHT * 0.3)
    fr = RoundedRectangle(width=body.width + 0.5, height=body.height + 0.5, corner_radius=0.16,
                          stroke_color=LAPTOP, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.head, g.rows, g.chip = fr, head, rows, ch
    return g


def model_card() -> VGroup:
    """The GREY model card (no numbers anywhere). .frame .text"""
    t = label("model", 26, INK)
    fr = RoundedRectangle(width=2.0, height=1.3, corner_radius=0.16, stroke_color=LAPTOP,
                          stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
    t.move_to(fr).shift(UP * 0.25)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 5, len(SAY)

        # ========================================================== 0. two folders, one question
        mon = folder_card("Monday").move_to([-4.15, -0.3, 0])
        fri = folder_card("Friday").move_to([4.15, -0.3, 0])
        mdl = model_card().move_to([0, -0.3, 0])
        ill = illustration_tag().next_to(fri, UP, buff=0.15).align_to(fri, RIGHT)
        a_mon = Arrow(mon.frame.get_right(), mdl.frame.get_left(), buff=0.15, color=S.GREY, stroke_width=3,
                      tip_length=0.18)
        down = Arrow(UP * 0.3, DOWN * 0.3, buff=0, color=ERR, stroke_width=6, tip_length=0.22)
        down.move_to(mdl.frame.get_center() + np.array([-0.3, -0.25, 0]))
        q_mdl = label("?", 36, ERR).next_to(down, RIGHT, buff=0.2)
        cap = label(CAPTION, 30, TURN).move_to([0, 2.75, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(mon, shift=RIGHT * 0.4), FadeIn(fri, shift=LEFT * 0.4), run_time=1.0)
            self.play(FadeIn(ill), run_time=0.4)
            vo.wait_until("with the same file names")
            self.play(each([mon.rows, fri.rows], INK, scale=1.05, lag=0.3), run_time=1.0)
            self.play(Indicate(mon.chip.text, color=INK), Indicate(fri.chip.text, color=INK), run_time=0.7)
            vo.wait_until("On Monday you trained")
            self.play(FadeIn(mdl, scale=0.9), Create(a_mon), run_time=0.8)
            vo.wait_until("On Friday the model got worse")
            self.play(GrowArrow(down), Indicate(fri.head, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("and nobody touched the code")
            self.play(FadeIn(q_mdl, scale=1.4), run_time=0.5)
            vo.wait_until("So which photos")
            self.play(each(list(mon.rows), TURN, scale=1.08, lag=0.2), run_time=1.2)
            vo.wait_until("And can you get exactly")
            self.play(FadeIn(cap, shift=DOWN * 0.3), run_time=0.8)

        # ========================================================== 1. final, final-v2, final-final-v3 …
        ref = lref("20, 24")
        strip = term(P_LAPTOP_HOME, rows=3, title="laptop")
        ill2 = illustration_tag().next_to(strip.box, UP, buff=0.15).align_to(strip.box, RIGHT)
        old = VGroup(mon, fri, mdl, ill, a_mon, down, q_mdl)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(old, shift=UP * 0.2), FadeIn(ref), run_time=0.7)
            self.remove(*old)
            self.play(FadeIn(strip), FadeIn(ill2, shift=LEFT * 0.2), run_time=0.6)
            type_cmd(self, strip, "ls", type_time=0.3)
            vo.wait_until("final, final version 2")
            for name in FINAL_FINAL[:-1]:
                out(self, strip, [name], run_time=0.4)
            vo.wait_until("until nobody knows")
            rows = out(self, strip, [FINAL_FINAL[-1]], run_time=0.3)
            q = label("?", 40, ERR).next_to(strip.lines[-1], RIGHT, buff=0.5)
            self.play(FadeIn(q, scale=2.0), run_time=0.5)
            self.play(Indicate(q, color=ERR, scale_factor=1.3), run_time=0.6)

        # ========================================================== 2. one short line
        small = label(CAPTION, 22, TURN).move_to([-6.5, 3.38, 0], aligned_edge=LEFT)
        line = mono(HOOK_LINE, 32, HASH).move_to([0, 0.5, 0])
        fp = grey_chip("same bytes, same fingerprint").next_to(line, DOWN, buff=0.4)
        tiles = VGroup(*[tile(n, 0.6, LAPTOP) for n in IMAGES[:4]]).arrange(RIGHT, buff=0.55)
        tiles.next_to(line, UP, buff=0.6)
        q2 = label("?", 44, S.GREY).next_to(fp, DOWN, buff=0.35)
        assert HOOK_LINE == capture("95").line(59).strip()[2:]

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(strip, ill2, q)), Transform(cap, small), run_time=0.8)
            self.remove(strip, ill2, q, *strip.lines)
            vo.wait_until("one short line")
            self.play(AddTextLetterByLetter(line, time_per_char=0.03), run_time=1.3)
            vo.wait_until("from 4 cheese photos")
            self.play(LaggedStart(*[FadeIn(t, shift=DOWN * 0.2) for t in tiles], lag_ratio=0.2), run_time=1.0)
            self.play(LaggedStart(*[t.animate.move_to(line.get_center()).set_opacity(0) for t in tiles],
                                  lag_ratio=0.15), Indicate(line, color=HASH, scale_factor=1.04), run_time=1.0)
            self.remove(tiles)
            vo.wait_until("It will match")
            self.play(FadeIn(fp, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("character for character")
            ul = Underline(line, color=HASH, buff=0.08)
            self.play(Create(ul), run_time=0.8)
            vo.wait_until("pin down")
            self.play(FadeIn(q2, shift=UP * 0.2), FadeOut(ul), run_time=0.6)

        # ========================================================== 3. where does the word go?
        env = annotation("gouda", 2.2, 1.35, 30).move_to([0, -0.3, 0])
        q3 = label("?", 44, S.GREY).next_to(env, UP, buff=0.4)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(line, fp, q2)), run_time=0.6)
            self.remove(line, fp, q2)
            vo.wait_until("when someone clicks gouda")
            self.play(FadeIn(env, shift=UP * 0.6, scale=0.8), run_time=1.0)
            vo.wait_until("where does that word")
            self.play(FadeIn(q3, shift=DOWN * 0.15), env.animate.shift(DOWN * 0.1), run_time=0.7)

        # ========================================================== 4. what you need, how to follow
        def row(*parts):
            return VGroup(check_mark(0.32, LAPTOP), *parts).arrange(RIGHT, buff=0.2)

        rows = [row(label("Docker Desktop running", 28, INK)),
                row(label("a GCP project with billing + your own bucket", 28, INK)),
                row(label("a GitHub account", 28, INK))]
        body = VGroup(*rows).arrange(DOWN, aligned_edge=LEFT, buff=0.36)
        bill = cost_tag("storage: a few MB, a fraction of a cent a month")
        bill.next_to(body, DOWN, buff=0.3).align_to(body, LEFT).shift(RIGHT * 0.5)
        frame = RoundedRectangle(width=max(body.width, bill.width + 0.5) + 1.0, height=body.height + bill.height + 1.05,
                                 corner_radius=0.18, stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        frame.move_to([0, 0.6, 0])
        VGroup(body, bill).move_to(frame).align_to(frame, LEFT).shift(RIGHT * 0.5)
        bill.align_to(body, LEFT).shift(RIGHT * 0.52)

        trs = {k: tracker(k, 1) for k in "ABCDEFGHIJKL"}
        tr = trs["A"]
        rng = tracker_ring(tr)
        strip = term(P_LAPTOP_HOME, rows=2, title="laptop")
        prev = preview_tag().next_to(strip.box, UP, buff=0.15).align_to(strip.box, LEFT)
        rec = recorded_tag("recorded · source named").next_to(strip.box, UP, buff=0.15).align_to(strip.box, RIGHT)
        clone, log = capture("01").cmd, capture("02").cmd

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(env, q3)), run_time=0.5)
            self.remove(env, q3)
            self.play(FadeIn(frame, scale=0.96), run_time=0.4)
            for r, anchor in zip(rows, ("you need Docker Desktop", "a Google Cloud project", "and a GitHub account")):
                vo.wait_until(anchor)
                self.play(FadeIn(r, shift=RIGHT * 0.25), run_time=0.5)
            vo.wait_until("This lecture stores")
            self.play(FadeIn(bill, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("gold tags mark where")
            flash_tag(self, bill, COST)
            vo.wait_until("The tracker in the top left")
            self.play(FadeOut(VGroup(frame, *rows, bill), shift=DOWN * 0.2), FadeOut(cap), run_time=0.5)
            self.remove(frame, *rows, bill, cap)
            self.play(FadeIn(tr, shift=DOWN * 0.15), Create(rng), run_time=0.8)
            vo.wait_until("follows both READMEs")
            for k in "BCDEFGHIJKL":
                new = trs[k]
                tr = swap_tracker(self, tr, new, Transform(rng, tracker_ring(new)), run_time=0.22)
            back = tracker("A", 1)
            tr = swap_tracker(self, tr, back, Transform(rng, tracker_ring(back)), run_time=0.4)
            vo.wait_until("A yellow your-turn tag")
            self.play(FadeIn(strip), FadeIn(prev, shift=RIGHT * 0.2), rng.animate.set_stroke(opacity=0.35),
                      run_time=0.6)
            ln1 = type_cmd(self, strip, clone, type_time=1.0)
            yt = beside(turn_row(), ln1)
            pin(self, ln1, yt)
            vo.wait_until("means pause and run it")
            flash_tag(self, yt, TURN)
            vo.wait_until("a gray extra tag")
            unpin(self, ln1, yt)
            ln2 = type_cmd(self, strip, log, type_time=0.5)
            xt = beside(extra_row(), ln2)
            pin(self, ln2, xt, anim=AnimationGroup(FadeIn(xt, shift=LEFT * 0.1), track(tr, extra=True),
                                                   Transform(rng, tracker_ring(tracker("A", 1, True), opacity=0.35))))
            vo.wait_until("marks a check")
            flash_tag(self, xt, INK)
            vo.wait_until("Every command")
            unpin(self, ln2, xt)
            self.play(FadeIn(rec, shift=LEFT * 0.15), FadeOut(rng), run_time=0.6)
            self.remove(rng)
            flash_tag(self, rec, INK)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
