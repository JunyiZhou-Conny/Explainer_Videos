"""S01 · Two tables, two winners (cold open of AC215 L13) — the reference scene for common.py.

Beats (script.md, ## S01; one voiceover block each):
0. Black frame, no tracker. V2's first frame: two compact RunLedgers side by side, notebook A · cell 54
   (nbA:1283-1295) and notebook B · cell 55 (nbB:1703-1715), cropped to name · epochs · accuracy,
   values verbatim, each tagged `recorded`. YELLOW rings settle on both top rows; on "62.93" B's second
   row flashes WHITE. Two GREY chips under both: "same pipeline · same 1,156 photos · same five
   models" and "train_base True = fine-tuned · False = frozen".
1. The chips leave, the tables drop a little; a YELLOW question card settles above them. On "look at
   the epochs column" a GREY pointer slides down both epochs columns and rings the fine-tuned rows'
   15 and 10 (GREY); nothing else is explained.
2. V4 preview: the winning row sits in a BLUE Colab frame, lifts out, becomes the GREEN parcel
   "4 KB tarball", slides into a BLUE job tile whose GOLD meter starts (no numbers). A 3-row strip
   (GREY tag "preview · scene 10") prints laptop/40:75 from "--model_name" (folded at its commas)
   with the W&B key outlined RED.
3. Checklist card (✓ two Colab copies · ✓ W&B account · ✓ Docker · ✓ a GCP project with billing) and
   the GOLD cost tag (no amounts). Layout preview: tracker A (step 1) top-left, a 2-row strip (GREY
   tag "preview") with only the YELLOW `▶ your turn` row tag. On "two words": lecture_ref(13, "8")
   top right and "reproducibility · accountability" GREY. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CAPTION, CLOUD, COST, DATASET_SIZE, ERR, INK, NARRATION, OWNED, P_COCKPIT, P_LAPTOP,
                    SAY_COUNT, TRACKING_WORDS, TURN, RunLedger, at_commas, bare_prompt, beside, capture,
                    check_mark, cost_tag, each, flash_tag, from_, grey_chip, job_tile, label, lref,
                    meter_run, parcel, pin, preview_tag, ring, substring, term, tracker_a, turn_row)
from explainer import style as S

SAY = NARRATION["S01"]
HOOK_QUESTION = ("Which recipe is better — and from these two tables,", "can you even tell what was different?")
FINE_TUNED = "mobilenetv2_train_base_True"


def question_card(lines, size: float = 26) -> VGroup:
    """The YELLOW question card (S01; S12 brings it back small). .frame .text"""
    t = VGroup(*[label(s, size, INK) for s in lines]).arrange(DOWN, buff=0.12)
    fr = RoundedRectangle(width=t.width + 0.8, height=t.height + 0.5, corner_radius=0.16, stroke_color=TURN,
                          stroke_width=3).set_fill(S.BG, 1)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def pointer() -> VGroup:
    """A small GREY triangle pointing down (the 'look at this column' pointer)."""
    return Triangle(color=S.GREY, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI)


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S01"] == 4, len(SAY)

        # ========================================================== 0. two tables, two winners
        ta = RunLedger("A", frame=False)
        tb = RunLedger("B", frame=False)
        ta.move_to([-3.35, 0, 0])
        tb.move_to([3.35, 0, 0])
        dy = 2.75 - max(ta.get_top()[1], tb.get_top()[1])
        ta.shift(UP * dy)
        tb.shift(UP * dy)
        ra, rb = ta.ring_row(0), tb.ring_row(0)
        ia, ib = ta.find(FINE_TUNED), tb.find(FINE_TUNED)
        assert (ia, ib) == (0, 1), (ia, ib)
        assert tb.cell(ib, "accuracy").original_text == "62.93%"
        # "also at 68.97" is B's winner (row 0, the frozen run), not the fine-tuned row
        assert ta.cell(ia, "accuracy").original_text == tb.cell(0, "accuracy").original_text == "68.97%"
        assert len(ta.rows) == len(tb.rows) == 5
        photos = f"{int(DATASET_SIZE):,}"
        same = grey_chip(f"same pipeline · same {photos} photos · same five models")
        legend = grey_chip("train_base True = fine-tuned · False = frozen")
        chips = VGroup(same, legend).arrange(DOWN, buff=0.18).next_to(VGroup(ta, tb), DOWN, buff=0.35)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ta, shift=RIGHT * 0.4), FadeIn(tb, shift=LEFT * 0.4), run_time=1.0)
            vo.wait_until("run by the instructors")
            flash_tag(self, ta.tag, INK)
            flash_tag(self, tb.tag, INK)
            vo.wait_until("the same data pipeline")
            self.play(FadeIn(same, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("the same five models")
            names = [t.rows[i].cells["name"] for i in range(len(ta.rows)) for t in (ta, tb)]
            self.play(each(names, INK, scale=1.05, lag=0.08), run_time=1.4)
            vo.wait_until("Notebook A crowns")
            self.play(Create(ra), run_time=0.6)
            self.play(FadeIn(legend, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("at 68.97 percent")
            self.play(Indicate(ta.cell(ia, "accuracy"), color=TURN, scale_factor=1.15), run_time=0.9)
            vo.wait_until("Notebook B crowns")
            self.play(Create(rb), run_time=0.6)
            vo.wait_until("also at 68.97")
            self.play(Indicate(tb.cell(0, "accuracy"), color=TURN, scale_factor=1.15), run_time=0.9)
            vo.wait_until("and puts the fine-tuned one at 62.93")
            self.play(each(list(tb.rows[ib].cells.values()), INK, scale=1.08, lag=0.1), run_time=0.9)

        # ========================================================== 1. the question, and one clue
        qc = question_card(HOOK_QUESTION).move_to([0, 2.75, 0])
        down = 2.0 - max(ta.get_top()[1], tb.get_top()[1])
        pa, pb = pointer(), pointer()
        ea, eb = ta.heads[1], tb.heads[1]
        pa.next_to(ea, UP, buff=0.08)
        pb.next_to(eb, UP, buff=0.08)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(chips, shift=DOWN * 0.2), ta.animate.shift(UP * down), tb.animate.shift(UP * down),
                      ra.animate.shift(UP * down), rb.animate.shift(UP * down), run_time=0.8)
            self.remove(*chips)
            vo.wait_until("So which recipe is better")
            self.play(FadeIn(qc, shift=DOWN * 0.3), run_time=0.8)
            vo.wait_until("can you even tell what was different")
            self.play(Indicate(qc.text[1], color=TURN, scale_factor=1.06), run_time=1.0)
            vo.wait_until("One clue is visible")
            pa.next_to(ea, UP, buff=0.08)
            pb.next_to(eb, UP, buff=0.08)
            self.play(FadeIn(pa), FadeIn(pb), run_time=0.4)
            vo.wait_until("look at the epochs column")
            ya, yb = ta.cell(ia, "epochs"), tb.cell(ib, "epochs")
            self.play(pa.animate.next_to(ta.rows[-1].cells["epochs"], RIGHT, buff=0.06),
                      pb.animate.next_to(tb.rows[-1].cells["epochs"], RIGHT, buff=0.06), run_time=1.4)
            ga, gb = ring(ya, S.GREY, buff=0.07), ring(yb, S.GREY, buff=0.07)
            self.play(pa.animate.next_to(ya, LEFT, buff=0.06).rotate(PI / 2),
                      pb.animate.next_to(yb, LEFT, buff=0.06).rotate(PI / 2), Create(ga), Create(gb), run_time=0.8)
            vo.wait_until("Hold that question")
            self.play(Indicate(qc.frame, color=TURN, scale_factor=1.02), run_time=0.8)
            vo.wait_until("part of it is in what the table never wrote down")
            self.play(ta.rows[ia].frame.animate.set_stroke(opacity=1), Wiggle(qc.text[1], scale_value=1.04),
                      run_time=1.0)

        # ========================================================== 2. the road ahead: a tarball and one command
        nb = RoundedRectangle(width=4.6, height=1.5, corner_radius=0.14, stroke_color=CLOUD, stroke_width=2.5)
        nb.set_fill(S.GREY_DARKER, 1).move_to([-4.1, 0.55, 0])
        nbt = label("notebook A · Colab", CAPTION, CLOUD).move_to(nb.get_corner(UL) + np.array([0.2, -0.25, 0]),
                                                                  aligned_edge=LEFT)
        win = label(FINE_TUNED, 22, INK).move_to(nb.get_center() + DOWN * 0.15)
        box_ = RoundedRectangle(width=win.width + 0.3, height=0.46, corner_radius=0.06, stroke_color=TURN,
                                stroke_width=2.5).move_to(win)
        row = VGroup(box_, win)
        pc = parcel("4 KB tarball", OWNED, 22, 0.9, 0.62).move_to([-0.2, 1.05, 0])
        tile = job_tile("CPU, RAM", False, 22, 2.6, 2.2).move_to([4.2, 0.9, 0])
        strip = term(P_COCKPIT, rows=3)
        prev = preview_tag("preview · scene 10").next_to(strip.box, UP, buff=0.12).align_to(strip.box, RIGHT)
        line75 = capture("40").line(75)
        rows = at_commas(from_(line75, "--model_name"), strip.max_chars)
        key = "--wandb_key=" + line75.split("--wandb_key=", 1)[1]
        assert rows[-1] == key, rows

        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(ta, tb, ra, rb, qc, pa, pb, ga, gb)
            self.play(FadeOut(gone), run_time=0.7)
            self.remove(*gone)
            self.play(FadeIn(nb), FadeIn(nbt), FadeIn(row, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("leaves Colab")
            self.play(row.animate.move_to([-3.7, nb.get_top()[1] + 0.45, 0]), run_time=0.6)
            vo.wait_until("It gets packed into")
            self.play(ReplacementTransform(row, pc[:3]), FadeIn(pc[3]), run_time=0.9)
            vo.wait_until("trains on a machine you rent")
            self.play(FadeIn(tile, scale=0.9), run_time=0.6)
            self.play(FadeOut(pc[3]), run_time=0.3)
            self.remove(pc[3])
            self.play(pc[:3].animate.move_to(tile.slot.get_center() + UP * 0.1), meter_run(tile.meter), run_time=1.0)
            vo.wait_until("from one command")
            self.play(FadeIn(strip), FadeIn(prev, shift=LEFT * 0.15), run_time=0.6)
            printed = strip.print(self, rows, run_time=0.9, lag=0.15)
            vo.wait_until("That command carries your W and B key")
            kr = ring(substring(printed[-1], key), ERR, buff=0.06, stroke=3)
            self.play(Create(kr), run_time=0.7)

        # ========================================================== 3. what you need, how to follow
        def item(s):
            return VGroup(check_mark(0.32, S.GREY), label(s, 28, INK)).arrange(RIGHT, buff=0.22)

        items = [item("two Colab copies (free T4)"), item("W&B account (free tier)"), item("Docker"),
                 item("a GCP project with billing")]
        body = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        bill = cost_tag("Vertex AI jobs bill while they run · no amounts in this video\n"
                        "see the Vertex AI pricing page")
        inner = VGroup(body, bill).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        frame = RoundedRectangle(width=inner.width + 1.0, height=inner.height + 0.8, corner_radius=0.18,
                                 stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        frame.move_to([0, 0.35, 0])
        inner.move_to(frame)
        tr = tracker_a(1)
        lay = term(P_LAPTOP, rows=2)
        lay_tag = preview_tag().next_to(lay.box, UP, buff=0.12).align_to(lay.box, LEFT)
        words = label(" · ".join(TRACKING_WORDS), 36, S.GREY).move_to([0, 0.6, 0])
        ref = lref("8")

        with self.voiceover(SAY[3]) as vo:
            old = VGroup(nb, nbt, pc[:3], tile, strip, prev, kr)
            self.play(FadeOut(old), run_time=0.6)
            self.remove(*old, *strip.lines)
            self.play(FadeIn(frame, scale=0.97), run_time=0.4)
            for it, anchor in zip(items, ("two Colab copies", "a free account on W and B", "Docker, and",
                                          "a Google Cloud project")):
                vo.wait_until(anchor)
                self.play(FadeIn(it, shift=RIGHT * 0.25), run_time=0.45)
            vo.wait_until("Vertex AI jobs cost money")
            self.play(FadeIn(bill, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("gold tags mark each point")
            flash_tag(self, bill, COST)
            vo.wait_until("A yellow tag means pause")
            self.play(FadeOut(VGroup(frame, *items, bill), shift=DOWN * 0.2), run_time=0.5)
            self.remove(frame, *items, bill)
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(lay), FadeIn(lay_tag, shift=RIGHT * 0.15), run_time=0.7)
            ln = bare_prompt(self, lay)
            yt = beside(turn_row(), ln)
            pin(self, ln, yt)
            flash_tag(self, yt, TURN)
            vo.wait_until("Today's two words")
            self.play(FadeOut(VGroup(lay, lay_tag, *lay.lines)), FadeIn(ref), run_time=0.6)
            self.remove(lay, lay_tag, *lay.lines)
            vo.wait_until("reproducibility and accountability")
            self.play(FadeIn(words, shift=UP * 0.2), run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
