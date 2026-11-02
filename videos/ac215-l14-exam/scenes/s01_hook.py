"""S01 · A job that never finishes (cold open of the AC215 L14 exam edition). Lecture: 14 · 14.

Beats (script.md "## S01", one voiceover block each):
0. Cold open, no lecture tag. A schematic BLUE job chip "Cloud Run job · translation-audio" writes in
   top left with the GREY `illustration` tag; at "It uses the same image" the TEAL image block
   (IMAGE, README.md line 59) and, at "a translation web app", the GREY chip "the same image as the
   working web app". At "We press Execute" the GREY Execute button presses and a YELLOW pulse drops
   down into the V1 strip (EndlessStrip: axis, running clock), which starts drawing left to right;
   the BLUE output bucket `gs://YOUR_OUTPUT_BUCKET/run-001/` (README.md line 765) sits at its right.
1. The strip keeps growing, the clock runs past 1, 2, 3, 4 minutes. At "Nothing lands" the bucket
   pulses, a GREY "empty" note above it. At "It runs straight into" the excerpt chip
   `README.md · line 778 (excerpt)` "set Task timeout to `5`" writes in above the wall's place; at
   "5 minutes" the RED wall "task timeout · 5 min" slams down, the bar end turns RED, RED chip
   "execution failed".
2. The setup, the chip and the strip's labels go; the strip (wall and "5 min" clock kept) shrinks to
   the top. CODE(tutorial/app/Dockerfile: 11–12): at "its default command" line 12 lit RED with
   `"serve"` underlined RED. At "The README's troubleshooting table" CODE(README.md: 1035, 1036,
   1044 folded) writes in under it; at "a job that starts a server" row 1044 lit YELLOW.
3. Panels and strip fade. A YELLOW question writes across the middle (no timer): "Same image, same
   code. / Why does the web app work — and the job never end?" At "So why does the web app" two
   tiny strips grow from one small TEAL image block: "web app" (dashed BLUE, YELLOW pulses dropping
   in, each answered by a short return arrow) and "job" (TEAL, running on past a faded dashed end).
4. The tiny strips fade; the question moves down and shrinks (22 pt). The exam map builds along the
   top: each slot writes in as the SAY names it, its label under it ("1 · service or job" …
   "5 · the model endpoint"), the label swapping slot by slot. At "where preprocessing lives" the
   GREY caption "Quiz 4 · Lecture 14 (+ Lecture 15 · slides 11–17)" writes in under the map.
5. The question, label and caption fade; the map dims to 35 %. At "The gray tag" the specimen tag
   lref(14, "14") pulses top right with a GREY caption "the lecture slide"; then a code-panel header
   specimen (`tutorial/app/translation_demo/__main__.py · line 1`, caption "the source file and
   lines") and the GREY chip "no live runs · concepts, not clicks". A hold, then everything fades to
   an empty frame (S02 rebuilds the map).
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    Rectangle,
    RoundedRectangle,
    VGroup,
    Write,
    linear,
)

from explainer import style as S
from explainer.scene import VoiceScene

from common import (
    CAPTION,
    CLOUD,
    CTR,
    ERR,
    EXAM_SLOTS,
    IMAGE,
    INK,
    JOB_NAME,
    MAP_Y,
    NARRATION,
    PULSE,
    ROUTE,
    SAFE_X,
    SAFE_Y,
    TURN,
    EndlessStrip,
    ExamMap,
    ImageBlock,
    _header_text,
    chip,
    dim,
    excerpt_chip,
    execute_button,
    grey_tag,
    guard,
    illustration_tag,
    label,
    lref,
    bucket_glyph,
    note,
    shown_path,
    source_line,
    src_panel,
    under,
    url_chip,
)

SAY = NARRATION["S01"]

# ------------------------------------------------------------------ the real sources (checked)
DOCKERFILE = "tutorial/app/Dockerfile"
README = "README.md"
assert source_line(DOCKERFILE, 12) == 'CMD ["python", "-m", "translation_demo", "serve"]'
assert IMAGE in source_line(README, 59)
OUT_URI = source_line(README, 765).strip()
assert OUT_URI == "gs://YOUR_OUTPUT_BUCKET/run-001/", OUT_URI
TIMEOUT_SUB = "set Task timeout to `5`"                       # README.md line 778 ("**" dropped)
assert TIMEOUT_SUB in source_line(README, 778)
assert "Job starts a server instead of finishing" in source_line(README, 1044)
assert "Command `python` and separate batch arguments" in source_line(README, 1044)
assert source_line(README, 1035).startswith("| Symptom | Check |")
MAIN = "tutorial/app/translation_demo/__main__.py"
assert JOB_NAME == "translation-audio"
assert EXAM_SLOTS == ("service or job", "who pays for idle", "what you hand over",
                      "who calls, who it runs as", "the model endpoint")

QUESTION = ("Same image, same code.", "Why does the web app work — and the job never end?")
CAPTION_MAP = "Quiz 4 · Lecture 14 (+ Lecture 15 · slides 11–17)"
SLOT_CUES = ("Service or job", "Who pays for idle", "What you hand over", "Who may call your code",
             "And the model endpoint")


def inside_frame(*mobs):
    for m in mobs:
        guard(m.get_left()[0] >= -SAFE_X - 1e-6 and m.get_right()[0] <= SAFE_X + 1e-6,
              f"x out of frame: {m.get_left()[0]:.2f}..{m.get_right()[0]:.2f}")
        guard(m.get_bottom()[1] >= -SAFE_Y - 1e-6 and m.get_top()[1] <= SAFE_Y + 1e-6,
              f"y out of frame: {m.get_bottom()[1]:.2f}..{m.get_top()[1]:.2f}")


def apart(a, b, gap: float = 0.05):
    sep = (a.get_right()[0] + gap <= b.get_left()[0] or b.get_right()[0] + gap <= a.get_left()[0]
           or a.get_top()[1] + gap <= b.get_bottom()[1] or b.get_top()[1] + gap <= a.get_bottom()[1])
    guard(sep, f"overlap: {a.get_corner(DOWN + LEFT)} {a.get_corner(UP + RIGHT)} / "
               f"{b.get_corner(DOWN + LEFT)} {b.get_corner(UP + RIGHT)}")


def tiny_strips():
    """Beat 3: one small TEAL image block, a web-app strip (dashed BLUE) and a job strip (TEAL)
    growing from it. Returns (block, svc_bar, job_bar, svc_label, job_label, end_mark)."""
    blk = RoundedRectangle(width=1.9, height=0.6, corner_radius=0.1, stroke_color=CTR, stroke_width=3) \
        .set_fill(CTR, 0.15)
    blk_t = label("one image", CAPTION, INK).move_to(blk)
    block = VGroup(blk, blk_t).move_to([-5.4, -1.55, 0])
    x0 = block.get_right()[0] + 0.35
    ys = (-0.95, -2.15)
    svc = Rectangle(width=0.05, height=0.36, stroke_color=CLOUD, stroke_width=2).set_fill(CLOUD, 0.2)
    svc.move_to([x0, ys[0], 0], aligned_edge=LEFT)
    job = Rectangle(width=0.05, height=0.36, stroke_color=CTR, stroke_width=2).set_fill(CTR, 0.35)
    job.move_to([x0, ys[1], 0], aligned_edge=LEFT)
    wires = VGroup(*[Line(block.get_right(), [x0, y, 0], color=S.GREY, stroke_width=2) for y in ys])
    svc_l = label("web app · answers each request", CAPTION, CLOUD).next_to([x0, ys[0] + 0.18, 0], UP, buff=0.1,
                                                                            aligned_edge=LEFT)
    job_l = label("job · never ends", CAPTION, ERR).next_to([x0, ys[1] + 0.18, 0], UP, buff=0.1,
                                                            aligned_edge=LEFT)
    end = DashedLine([x0 + 4.2, ys[1] - 0.3, 0], [x0 + 4.2, ys[1] + 0.3, 0], color=S.GREY, stroke_width=3)
    end_l = note("where a job should end", S.GREY).next_to(end, DOWN, buff=0.08)
    return block, wires, svc, job, svc_l, job_l, VGroup(end, end_l), x0, ys


class Hook(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, len(SAY)

        # ========================================================== 0. the job, the image, Execute
        job_chip = chip(f"Cloud Run job · {JOB_NAME}", CLOUD, size=CAPTION + 2)
        job_chip.move_to([-6.45 + job_chip.width / 2, 3.15, 0])
        ill = illustration_tag().next_to(job_chip, RIGHT, buff=0.3)
        img = ImageBlock(IMAGE, commands=())
        img.next_to(job_chip, DOWN, buff=0.3).align_to(job_chip, LEFT)
        exe = execute_button().next_to(img, DOWN, buff=0.3).align_to(img, LEFT)
        same = chip("the same image as the working web app", S.GREY, size=CAPTION)
        same.next_to(img, DOWN, buff=0.3).align_to(img, RIGHT)

        en = EndlessStrip(9.4)
        en.shift([exe.get_center()[0] - en.parts["axis"].get_left()[0], -1.05, 0])
        x_start = en.parts["axis"].get_left()[0]
        bucket = bucket_glyph(0.55).move_to([5.75, -1.05, 0])
        uri = url_chip(OUT_URI, size=CAPTION)
        uri.move_to([SAFE_X - 0.1 - uri.width / 2, -2.75, 0])
        empty = note("empty", S.GREY).next_to(bucket, UP, buff=0.15)
        uri_wire = Line(bucket.get_bottom(), [bucket.get_center()[0], uri.get_top()[1], 0], color=CLOUD,
                        stroke_width=2)
        xw = en.parts["wall"].get_center()[0]
        tmo = excerpt_chip(TIMEOUT_SUB, f"{README} · line 778 (excerpt)", line=source_line(README, 778))
        tmo.move_to([min(xw, SAFE_X - tmo.width / 2 - 0.05), 1.15, 0])

        pulse_dot = Dot(radius=0.11, color=PULSE).move_to(exe.get_bottom())
        pulse_path = Line(exe.get_bottom(), [x_start, en.parts["bar"].get_center()[1], 0])

        inside_frame(job_chip, ill, img, exe, same, en, bucket, uri, tmo)
        apart(job_chip, ill)
        apart(img, same)
        apart(exe, same)
        apart(same, en)
        apart(en, bucket, 0.02)
        apart(uri, en.parts["fail"])
        apart(tmo, img)
        apart(tmo, en.parts["wall_label"])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(job_chip, shift=RIGHT * 0.2), FadeIn(ill), run_time=0.8)
            vo.wait_until("It uses the same image")
            self.play(FadeIn(img, shift=DOWN * 0.15), run_time=0.7)
            vo.wait_until("translation web app")
            self.play(FadeIn(same, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("We press Execute")
            self.play(FadeIn(exe), run_time=0.3)
            self.play(exe.press(), run_time=0.45)
            self.add(pulse_dot)
            self.play(MoveAlongPath(pulse_dot, pulse_path), FadeIn(en), FadeIn(bucket), FadeIn(uri),
                      Create(uri_wire), run_time=0.8, rate_func=linear)
            self.play(FadeOut(pulse_dot, scale=2.2), *en.grow_to(0.08, run_time=0.8))
            self.play(*en.grow_to(0.2, run_time=vo.remaining(0.6)))

        # ========================================================== 1. it runs into the wall
        with self.voiceover(SAY[1]) as vo:
            self.play(*en.grow_to(0.42, run_time=vo.until("Nothing lands")))
            self.play(*en.grow_to(0.52, run_time=0.9), Indicate(bucket, color=TURN, scale_factor=1.25),
                      FadeIn(empty, shift=DOWN * 0.1))
            self.play(*en.grow_to(0.66, run_time=vo.until("It runs straight into")))
            self.play(*en.grow_to(0.74, run_time=0.8), FadeIn(tmo, shift=DOWN * 0.15))
            self.play(*en.grow_to(en.wall_at, run_time=vo.until("5 minutes")))
            self.play(*en.hit_wall(), run_time=0.6)
            self.play(Indicate(en.parts["wall_label"], color=ERR, scale_factor=1.1), run_time=vo.remaining(0.6))

        # ========================================================== 2. the clue: CMD … serve
        dock = src_panel(DOCKERFILE, 11, 12)
        tab = src_panel(README, [1035, 1036, 1044])
        top_y = 2.75
        dock.move_to([0, 1.05, 0])
        tab.next_to(dock, DOWN, buff=0.35)
        inside_frame(dock, tab)
        apart(dock, tab)
        bar12 = dock.bar(12, ERR, 0.25)
        serve = dock.span(12, '"serve"')
        ul = under(serve, ERR, stroke=4)
        bar44 = tab.bar(1044, TURN, 0.22)

        with self.voiceover(SAY[2]) as vo:
            en.clock.freeze()
            self.play(FadeOut(VGroup(job_chip, ill, img, exe, same, tmo, empty, uri, uri_wire)),
                      *en.parts_out("wall_label", "fail"), run_time=0.6)
            strip = VGroup(en, bucket)
            tgt = strip.copy()
            tgt[0].rescale(0.6)
            tgt[1].scale(0.6).next_to(tgt[0], RIGHT, buff=0.25)
            tgt.move_to([0, top_y, 0])
            self.play(en.animate.rescale(0.6).move_to(tgt[0]), bucket.animate.scale(0.6).move_to(tgt[1]),
                      run_time=0.8)
            guard(VGroup(en, bucket).get_bottom()[1] > dock.get_top()[1] + 0.05, "strip over the Dockerfile panel")
            self.play(FadeIn(dock, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("its default command")
            self.play(FadeIn(bar12), Write(ul), serve.animate.set_color(ERR), run_time=0.7)
            vo.wait_until("troubleshooting table")
            self.play(FadeIn(tab, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("a job that starts a server")
            self.play(FadeIn(bar44), run_time=0.6)
            self.play(Indicate(tab.span(1044, "Job starts a server instead of finishing"), color=TURN,
                               scale_factor=1.05), run_time=vo.remaining(0.8))

        # ========================================================== 3. the question
        q1 = label(QUESTION[0], 30, TURN)
        q2 = label(QUESTION[1], 30, TURN)
        q = VGroup(q1, q2).arrange(DOWN, buff=0.22).move_to([0, 1.55, 0])
        block, wires, svc, job, svc_l, job_l, end, x0, ys = tiny_strips()
        inside_frame(q, block, svc_l, job_l, end)
        apart(q, svc_l, 0.15)
        apart(job_l, svc, 0.05)
        ticks = []
        for k, x in enumerate((x0 + 1.0, x0 + 2.6, x0 + 3.5, x0 + 5.2, x0 + 7.4)):
            d = Dot(radius=0.08, color=PULSE).move_to([x, ys[0] + 0.55, 0])
            back = Arrow([x + 0.12, ys[0] + 0.15, 0], [x + 0.35, ys[0] + 0.6, 0], buff=0, color=ROUTE,
                         stroke_width=3, tip_length=0.12, max_tip_length_to_length_ratio=0.4)
            ticks.append((d, back))
        last_x = ticks[-1][0].get_center()[0]
        guard(last_x + 0.5 <= SAFE_X, "tiny strips reach the frame edge")

        def grow(bar, w, rt):
            return bar.animate(rate_func=linear, run_time=rt).stretch_to_fit_width(w).align_to(bar, LEFT)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(dock, tab, bar12, ul, bar44)), FadeOut(en), FadeOut(bucket), run_time=0.6)
            self.play(Write(q1), run_time=0.9)
            vo.wait_until("So why does the web app")
            self.play(Write(q2), run_time=1.2)
            self.play(FadeIn(block), Create(wires), FadeIn(svc), FadeIn(job), FadeIn(svc_l), FadeIn(job_l),
                      run_time=0.5)
            # both bars grow; pulses drop onto the web app and are answered
            seg = [2.0, 3.6, 5.6, 7.9]
            self.play(grow(svc, seg[0] - 0.8, 0.7), grow(job, seg[0] - 0.8, 0.7), FadeIn(end))
            for k, (d, back) in enumerate(ticks[:4]):
                w = min(seg[min(k, 3)], last_x - x0 + 0.6)
                self.play(FadeIn(d, shift=DOWN * 0.3), grow(svc, w, 0.55), grow(job, w + 0.2, 0.55),
                          run_time=0.55)
                self.play(FadeOut(d), Create(back), run_time=0.3)
            self.play(grow(svc, last_x - x0 + 0.4, vo.remaining(0.6)),
                      grow(job, last_x - x0 + 0.6, vo.remaining(0.6)))

        # ========================================================== 4. the exam map
        m = ExamMap()
        labels = [m.label_of(i) for i in range(1, 6)]
        cap = note(CAPTION_MAP, S.GREY).move_to([m.get_center()[0], 2.28, 0])
        q_small_y = 1.2
        inside_frame(m, cap, *labels)
        for lb in labels:
            apart(lb, cap, 0.05)

        with self.voiceover(SAY[4]) as vo:
            backs = VGroup(*[b for _, b in ticks if b in self.mobjects])
            self.play(FadeOut(VGroup(block, wires, svc, job, svc_l, job_l, end, backs)),
                      q.animate.scale(22 / 30).move_to([0, q_small_y, 0]), run_time=0.8)
            apart(q, cap, 0.2)
            shown = None
            for i, cue in enumerate(SLOT_CUES, start=1):
                vo.wait_until(cue)
                anims = [m.slot_in(i), FadeIn(labels[i - 1], shift=DOWN * 0.1)]
                if shown is not None:
                    anims.append(FadeOut(shown))
                self.play(*anims, run_time=0.6)
                self.play(m.pulse(i), run_time=0.6)
                shown = labels[i - 1]
            vo.wait_until("where preprocessing lives")
            self.play(FadeIn(cap, shift=DOWN * 0.1), run_time=0.6)
            self.play(Indicate(q, color=TURN, scale_factor=1.04), run_time=vo.remaining(0.6))

        # ========================================================== 5. how to read the frame
        spec = lref(14, "14")
        spec_cap = note("the lecture slide", S.GREY).next_to(spec, DOWN, buff=0.15).align_to(spec, RIGHT)
        hdr = _header_text(f"{shown_path(MAIN)} · line 1")
        hdr_box = RoundedRectangle(width=hdr.width + 0.4, height=hdr.height + 0.3, corner_radius=0.08,
                                   stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 0.0)
        hdr_g = VGroup(hdr_box, hdr.move_to(hdr_box)).move_to([0, 0.7, 0])
        hdr_cap = note("a code panel names its source file and lines", S.GREY).next_to(hdr_g, DOWN, buff=0.15)
        nolive = grey_tag("no live runs · concepts, not clicks").move_to([0, -1.3, 0])
        inside_frame(spec, spec_cap, hdr_g, hdr_cap, nolive)
        apart(spec, m, 0.1)
        apart(spec_cap, m, 0.1)
        apart(hdr_cap, nolive, 0.2)
        assert source_line(MAIN, 1).strip() != ""

        slots = VGroup(*m.slots)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(q, shown, cap)), dim(slots, 0.35), FadeIn(spec), run_time=0.6)
            vo.wait_until("names the lecture slide")
            self.play(Indicate(spec, color=INK, scale_factor=1.12), FadeIn(spec_cap, shift=UP * 0.1),
                      run_time=0.8)
            self.play(FadeIn(hdr_g, shift=UP * 0.1), FadeIn(hdr_cap), run_time=vo.remaining(0.6))
        self.play(Indicate(hdr_g, color=INK, scale_factor=1.06), run_time=0.8)
        self.play(FadeIn(nolive, shift=UP * 0.1), run_time=0.6)
        self.wait(1.6)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
        self.wait(0.3)
