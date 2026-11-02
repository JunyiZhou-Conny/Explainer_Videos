"""S02 · Service or job: read the lifecycle (AC215 L14 exam edition). Lecture: 14 · 14.

Beats (script.md "## S02", one voiceover block each):
0. The exam map (nothing filled yet) fades in, slot 1 activates (YELLOW, label "1 · service or
   job") and pulses; lref(14, "14") top right. The GREY redrawn slide-14 line "Run containers as
   service or job." writes in. CODE(__main__.py: 1) above the V1 TEAL image block (IMAGE, GREEN
   `serve` / `batch` tags); line 1 lit YELLOW. At "two startup commands" the panel grows to the
   folded lines 1, 12, 13 and lines 12-13 light GREEN.
1. The slide line goes; the panel switches to CODE(__main__.py: 22–26), lines 23-24 lit. At
   "gunicorn" a PURPLE "gunicorn" chip slides out of the `serve` tag. At "Then it waits" the panel
   and image block go, the `serve` tag (copy) and the gunicorn chip become the strip's label, and the
   V1 service strip draws: a dashed BLUE instance with the ear "listening on :8080"; at "answers each
   request" PINK request arrows arrive, each answered by a YELLOW return arrow.
2. At "That shape is a service" the instance pulses; at "It has a URL" the PINK `https://…run.app`
   chip writes in above the strip; at "adds instances" a burst: a second dashed instance splits off
   (GREY "max instances 2"), both answer; at "scale to zero" the traffic stops and both dissolve
   ("scale to zero"). At "listening is its job" the ear caption pulses.
3. The service strip shrinks into a thumbnail, top right. A GREEN `batch` tag and the V1 job strip
   come in at the bottom, CODE(__main__.py: 52–57) above it; the four segments read / translate /
   speak / save run as the SAY names them, lines 53 / 54-55 / 56 / 57 lighting in step; at "and
   exits" the GREEN edge "exit 0". At "If a step fails" the panel scrolls to CODE(__main__.py:
   58–61) lit RED and a short strip (read, translate) to the right ends in a RED edge "exit 1"; at
   "so the execution shows failed" line 59's comment lights YELLOW.
4. The failed strip goes; the panel switches to CODE(README.md: 582–585), line 585 lit YELLOW. At
   "no URL" a crossed-out PINK URL chip and a GREY chip "no URL · it exits" sit right of the job
   strip, the excerpt chip `README.md · line 833 (excerpt)` under them. At "Something starts it" the
   job strip's `batch` tag pulses; at "runs to completion" its exit edge pulses.
5. "Now the hook": panel, chips and job strip go; S01's endless strip drops in on the job row (its
   default-command tag `serve`, RED) and runs into the RED "task timeout · 5 min" wall again. At
   "The job inherited" CODE(README.md: 747–748) comes in; at "The fix" "This replaces the image's
   web-server command" lights YELLOW. At "the command python" the panel gives way to the GREEN
   command chip `python` and the argument chips of README.md lines 755–765 (PINK gs:// paths,
   shortened with "…"), and the RED `serve` tag transforms into the GREEN `python -m
   translation_demo batch …` chip. At "Same image, and now the strip ends" the endless bar is cut
   into the job's four segments, which run to the GREEN "exit 0" edge.
6. The two strips side by side, small: the service thumbnail on the left, the job strip on the
   right. At "In the README, you click Execute" the GREY Execute button (tag `illustration`) presses
   and a PINK trigger drops onto the job strip, which runs again and ends. At "For a nightly run"
   the BLUE Cloud Scheduler clock comes in with a small three-night timeline; at each night a PINK
   trigger drops and a small job strip runs and ends; at "which this README does not use" the GREY
   chip "not in this README".
7. "Try one." The strips and the Scheduler fade out. After the block: PONDER P1 (10 s): the
   multiple-choice card, the map and the lecture tag dimmed to 20 %.
8. Reveal: B fills YELLOW ✓ with the GREEN note; at "A pays", "C breaks", "D works" each RED reason
   writes in. The card fades; map and tag come back.
9. RULE: the GREEN "exam rule" card writes in (line 1 at "So the rule", line 2 at "If it says it
   answers"); then it shrinks into map slot 1, which fills GREEN with its tick. Everything fades to
   an empty frame.
"""

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    ReplacementTransform,
    Succession,
    Transform,
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
    IMAGE,
    IN_BUCKET,
    INK,
    MONO,
    NARRATION,
    OUT_BUCKET,
    OWN,
    PORT,
    ROUTE,
    SAFE_X,
    SAFE_Y,
    TOOL,
    TURN,
    EndlessStrip,
    ExamMap,
    ImageBlock,
    JobStrip,
    RuleCard,
    ServiceStrip,
    _header_text,
    chip,
    dim,
    excerpt_chip,
    ear_chip,
    execute_button,
    grey_tag,
    guard,
    illustration_tag,
    instance_box,
    label,
    lref,
    mcq_ponder,
    note,
    scheduler_clock,
    source_line,
    src_panel,
    strike,
    undim,
    url_chip,
)

SAY = NARRATION["S02"]

# ------------------------------------------------------------------ the real sources (checked)
MAIN = "tutorial/app/translation_demo/__main__.py"
README = "README.md"
assert source_line(MAIN, 1) == '"""One image, different startup commands: serve or batch."""'
assert '"serve"' in source_line(MAIN, 12) and '"batch"' in source_line(MAIN, 13)
assert 'os.environ.get("PORT", "8080")' in source_line(MAIN, 23) and PORT == 8080
assert '"gunicorn"' in source_line(MAIN, 24) and "0.0.0.0:{port}" in source_line(MAIN, 24)
assert "read_text(args.input_uri)" in source_line(MAIN, 53)
assert "translate(text" in source_line(MAIN, 55)
assert "synthesize(translated" in source_line(MAIN, 56)
assert "save_artifacts(" in source_line(MAIN, 57)
assert source_line(MAIN, 58).strip() == "except Exception as exc:"
COMMENT59 = "so execution status is truthful"
assert COMMENT59 in source_line(MAIN, 59)
assert "raise SystemExit(1)" in source_line(MAIN, 61)
JOB_LINE = "That is a job, rather than an HTTP service waiting for requests."   # "**" dropped
assert source_line(README, 585).strip() == JOB_LINE
NO_URL = "it does not provide a web URL"
assert "The job exits; it does not provide a web URL." in source_line(README, 833)
REPLACES = "This replaces the image's web-server command."
assert REPLACES in source_line(README, 748)
assert "enter `python` in Container command" in source_line(README, 747)
ARGS_README = [source_line(README, n).strip() for n in range(755, 766)]
assert ARGS_README == ["-m", "translation_demo", "batch", "--input-uri",
                       "gs://YOUR_INPUT_BUCKET/run-001/passage.txt", "--src", "en", "--dest", "fr",
                       "--output-uri", "gs://YOUR_OUTPUT_BUCKET/run-001/"], ARGS_README
# shown shortened, as script.md asks: gs://YOUR_INPUT_BUCKET/…, gs://YOUR_OUTPUT_BUCKET/…
ARGS_SHOWN = ARGS_README[:4] + [IN_BUCKET] + ARGS_README[5:10] + [OUT_BUCKET]
assert IN_BUCKET.rstrip("…") in ARGS_README[4] and OUT_BUCKET.rstrip("…") in ARGS_README[10]

SLIDE_LINE = "Run containers as service or job."
FIXED_CMD = "python -m translation_demo batch …"

# ------------------------------------------------------------------ P1 (script.md S02, BRIEF "Ponder questions")
P1_Q = ("A container indexes new documents from a bucket, writes embeddings to another bucket, "
        "then exits. It runs once an hour. Best fit?")
P1_OPTS = ["Cloud Run service, min instances 1, looping",
           "Cloud Run job, run hourly by Cloud Scheduler",
           "Cloud Run service that indexes at startup, then exits",
           "Compute Engine VM with a cron entry"]
P1_RIGHT = (1, "finite work · runs to completion · billed only while it runs")
P1_WRONG = {0: "pays for an always-on instance · between requests its CPU is throttled, so a loop stalls",
            2: "a service must keep listening on $PORT · exiting = a crashed instance",
            3: "works, but the VM bills every idle minute between runs"}

RULE_TOP = "runs, writes output, exits · 'every night' → job (+ Cloud Scheduler)"
RULE_BOTTOM = "answers requests · URL · port → service"

# ------------------------------------------------------------------ layout
PANEL_TOP = 1.6           # code panels in beats 3-5 hang from here (the thumbnail sits above, right)
JOB_Y = -2.95             # the job row (segments' centre) in beats 3-5
JOB_X0 = -6.2             # the job strip's left edge
SEG_W = 1.3
JOB_W = 5.4


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


def words(panel, n: int, text: str) -> VGroup:
    """The glyphs of each word of `text` in file line n of a (possibly wrapped) panel."""
    return VGroup(*[panel.span(n, w) for w in text.split()])


def cmd_tag(text: str, color: str = OWN):
    """A GREEN mono command tag (the image block's `serve` / `batch`)."""
    return chip(text, color, size=CAPTION + 2, font=MONO)


def place_job(job: JobStrip, x0: float, y: float) -> JobStrip:
    """Move a JobStrip (built centred at ORIGIN) so its left edge is at x0 and its segments at y."""
    job.shift([x0 + job.W / 2, y, 0])
    return job


def arg_chips(width: float = 12.4) -> VGroup:
    """README.md lines 755–765 as chips: header, then the command `python` and its argument chips
    (GREEN; the gs:// paths PINK), flowed into rows."""
    hdr = _header_text(f"{README} · lines 755–765 (container arguments)")
    cmd_l = label("command", CAPTION, S.GREY)
    cmd = chip("python", OWN, size=CAPTION, font=MONO)
    args_l = label("arguments", CAPTION, S.GREY)
    chips = [chip(a, ROUTE if a.startswith("gs://") else OWN, size=CAPTION, font=MONO) for a in ARGS_SHOWN]
    row0 = VGroup(cmd_l, cmd).arrange(RIGHT, buff=0.2)
    rows, cur, w = [], [args_l], args_l.width
    for c in chips:
        if w + 0.15 + c.width > width:
            rows.append(VGroup(*cur).arrange(RIGHT, buff=0.15))
            cur, w = [c], c.width
        else:
            cur.append(c)
            w += 0.15 + c.width
    rows.append(VGroup(*cur).arrange(RIGHT, buff=0.15))
    body = VGroup(row0, *rows).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    g = VGroup(hdr, body).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    g.hdr, g.cmd, g.chips, g.rows = hdr, cmd, chips, VGroup(row0, *rows)
    return g


class ServiceOrJob(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0. two shapes, one image
        m = ExamMap()
        lr = lref(14, "14")
        slide = label(SLIDE_LINE, 26, S.GREY).move_to([-1.0, 2.2, 0])
        img = ImageBlock(IMAGE)
        img.move_to([0, -2.1, 0])
        p1 = src_panel(MAIN, 1, 1)
        p1.move_to([0, 0.7, 0])
        pf = src_panel(MAIN, [1, 12, 13])
        pf.next_to(slide, DOWN, buff=0.3).set_x(0)
        inside_frame(m, lr, slide, img, p1, pf)
        apart(slide, m.label_of(1), 0.1)
        apart(pf, img, 0.12)
        apart(slide, pf, 0.1)
        bar1 = p1.bar(1, TURN, 0.22)
        bars_f = VGroup(pf.bar(12, OWN, 0.22), pf.bar(13, OWN, 0.22))

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(m), FadeIn(lr), run_time=0.6)
            self.play(*m.activate(1), run_time=0.5)
            self.play(m.pulse(1), Write(slide), run_time=1.0)
            vo.wait_until("The demo app shows both")
            self.play(FadeIn(img, shift=UP * 0.15), FadeIn(p1, shift=DOWN * 0.1), run_time=0.7)
            self.play(FadeIn(bar1), run_time=0.4)
            vo.wait_until("two startup commands")
            self.play(FadeOut(VGroup(p1, bar1)), FadeIn(pf), run_time=0.7)
            self.play(FadeIn(bars_f), Indicate(img.cmds["serve"], color=TURN, scale_factor=1.15),
                      Indicate(img.cmds["batch"], color=TURN, scale_factor=1.15), run_time=vo.remaining(0.8))

        # ========================================================== 1. serve: gunicorn on $PORT
        p22 = src_panel(MAIN, 22, 26)
        p22.move_to([0, 2.45 - p22.height / 2, 0])
        inside_frame(p22)
        apart(p22, img, 0.12)
        guard(p22.get_top()[1] <= 2.55, "the 22-26 panel reaches the map label")
        bars22 = VGroup(p22.bar(23, TURN, 0.22), p22.bar(24, TURN, 0.22))
        serve_tag = img.cmds["serve"]
        gun = chip("gunicorn", TOOL, size=CAPTION + 2).move_to(serve_tag)
        gun_to = serve_tag.get_center() + LEFT * 2.3

        sv = ServiceStrip(10.0, url=None)
        sv.shift(DOWN * 0.5)
        lab_serve = cmd_tag("serve")
        lab_gun = chip("gunicorn", TOOL, size=CAPTION + 2)
        lab_row = VGroup(lab_serve, lab_gun).arrange(RIGHT, buff=0.2)
        lab_row.move_to([sv.x(0) + lab_row.width / 2, 1.75, 0])
        url = url_chip("https://…run.app").move_to([1.2, 1.15, 0])
        inside_frame(sv, lab_row, url)
        apart(lab_row, url, 0.1)
        guard(url.get_bottom()[1] > sv.lane_y(0) + 0.9, "URL chip over the request arrows")
        guard(lab_row.get_top()[1] <= 2.55, "strip label under the map label")

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(slide), FadeOut(VGroup(pf, bars_f)), run_time=0.5)
            self.play(FadeIn(p22, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(bars22), run_time=0.4)
            vo.wait_until("gunicorn")
            self.add(gun)
            self.play(gun.animate.move_to(gun_to), run_time=0.7)
            vo.wait_until("8080 by default")
            self.play(Indicate(p22.span(23, '"8080"'), color=TURN, scale_factor=1.2), run_time=0.7)
            vo.wait_until("Then it waits")
            s_copy = serve_tag.copy()
            self.add(s_copy)
            self.play(FadeOut(VGroup(p22, bars22)), FadeOut(img), ReplacementTransform(s_copy, lab_serve),
                      ReplacementTransform(gun, lab_gun), run_time=0.7)
            self.play(FadeIn(sv), run_time=0.3)
            self.play(*sv.start(0.05), run_time=0.6)
            vo.wait_until("answers each request")
            self.play(*sv.grow(0.14), *sv.request(0.1), run_time=0.7)
            self.play(*sv.grow(0.24), *sv.request(0.2), run_time=0.7)
            self.play(*sv.grow(0.32), *sv.request(0.29), run_time=vo.remaining(0.7))

        # ========================================================== 2. the shape of a service
        with self.voiceover(SAY[2]) as vo:
            self.play(Indicate(sv.bars[0], color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("It has a URL")
            self.play(FadeIn(url, shift=DOWN * 0.1), *sv.grow(0.38), run_time=0.6)
            vo.wait_until("adds instances")
            self.play(*sv.grow(0.44), *sv.request(0.41), run_time=0.5)
            self.play(*sv.split(0.45), *sv.grow(0.47, lanes=(0,)), run_time=0.5)
            self.play(*sv.grow(0.53), *sv.request(0.49), *sv.request(0.51, 1), run_time=0.6)
            self.play(*sv.grow(0.58), *sv.request(0.55), *sv.request(0.57, 1), run_time=0.6)
            vo.wait_until("scale to zero")
            self.play(*sv.stop(0.64), run_time=1.6)
            vo.wait_until("listening is its job")
            self.play(Indicate(sv.parts["ear"], color=TURN, scale_factor=1.12), run_time=vo.remaining(0.8))

        # ========================================================== 3. batch: a strip with an end
        thumb_k = 0.42
        job = place_job(JobStrip(JOB_W, seg_w=SEG_W), JOB_X0, JOB_Y)
        batch_tag = cmd_tag("batch")
        batch_tag.move_to([JOB_X0 + batch_tag.width / 2, JOB_Y + 0.3 + batch_tag.height / 2, 0])
        fail = place_job(JobStrip(2 * SEG_W, steps=("read", "translate"), seg_w=SEG_W, code=1, axis=False),
                         1.2, JOB_Y)
        p52 = src_panel(MAIN, 52, 57)
        p52.move_to([0, PANEL_TOP - p52.height / 2, 0])
        p58 = src_panel(MAIN, 58, 61)
        p58.move_to([0, PANEL_TOP - p58.height / 2, 0])
        step_lines = [(53,), (54, 55), (56,), (57,)]
        step_cues = ["reads the passage", "translates it", "generates speech", "saves the files"]
        step_bars = [VGroup(*[p52.bar(n, OWN, 0.22) for n in ns]) for ns in step_lines]
        bars58 = VGroup(*[p58.bar(n, ERR, 0.2) for n in (58, 60, 61)])
        bar59 = p58.bar(59, TURN, 0.25)

        # the thumbnail: the service strip without its captions, shapes x thumb_k, top right
        thumb_lab = VGroup(lab_serve.copy(), lab_gun.copy()).arrange(RIGHT, buff=0.2)
        with self.voiceover(SAY[3]) as vo:
            self.play(*sv.parts_out("ear", "max_chip", "zero_chip", "time"), run_time=0.4)
            tgt = sv.copy()
            tgt.rescale(thumb_k)
            ax = tgt.parts["axis"]
            tgt.shift([6.0 - ax.get_right()[0], 1.8 - ax.get_center()[1], 0])
            thumb_lab.move_to([ax.get_left()[0] - 0.25 - thumb_lab.width / 2, 0, 0])
            thumb_lab.set_y(tgt.lane_y(0) + 0.1)
            self.play(sv.animate.rescale(thumb_k).move_to(tgt), Transform(lab_row, thumb_lab),
                      FadeOut(url), run_time=0.8)
            thumb = VGroup(sv.parts["axis"], sv.arrows, lab_row)
            inside_frame(thumb, job, batch_tag, fail, p52, p58)
            apart(thumb, p52, 0.1)
            apart(thumb, lr, 0.1)
            apart(thumb, VGroup(*m.slots), 0.1)
            apart(thumb, m.caption, 0.1)
            apart(p52, job.parts["exit"], 0.08)
            apart(p52, batch_tag, 0.08)
            apart(p58, fail.parts["exit"], 0.08)
            apart(job, fail, 0.2)
            self.play(FadeIn(batch_tag, shift=DOWN * 0.15), FadeIn(job), FadeIn(p52, shift=UP * 0.1),
                      run_time=0.6)
            for i, cue in enumerate(step_cues):
                vo.wait_until(cue)
                self.play(*job.run(i, run_time=0.6), FadeIn(step_bars[i]), run_time=0.6)
            vo.wait_until("and exits")
            self.play(*job.finish(), run_time=0.5)
            vo.wait_until("If a step fails")
            self.play(FadeOut(VGroup(p52, *step_bars)), FadeIn(p58, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(bars58), FadeIn(fail), run_time=0.4)
            self.play(*fail.run(0, 0.4), run_time=0.4)
            self.play(*fail.run(1, 0.4), run_time=0.4)
            vo.wait_until("status 1")
            self.play(*fail.finish(), run_time=0.5)
            vo.wait_until("so the execution shows failed")
            self.play(FadeIn(bar59), Indicate(words(p58, 59, "so execution status is truthful."),
                                               color=TURN, scale_factor=1.06),
                      run_time=vo.remaining(0.8))

        # ========================================================== 4. the README: a job, no URL
        p582 = src_panel(README, 582, 585)
        p582.move_to([0, PANEL_TOP - p582.height / 2, 0])
        bar585 = p582.bar(585, TURN, 0.22)
        x_url = url_chip("https://…run.app")
        x_cross = strike(x_url, ERR)
        no_url = chip("no URL · it exits", S.GREY, size=CAPTION)
        top_row = VGroup(VGroup(x_url, x_cross), no_url).arrange(RIGHT, buff=0.25)
        ex833 = excerpt_chip(NO_URL, f"{README} · line 833 (excerpt)", line=source_line(README, 833))
        right = VGroup(top_row, ex833).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        right.move_to([SAFE_X - 0.1 - right.width / 2, JOB_Y + 0.27, 0])
        inside_frame(p582, right)
        apart(p582, right, 0.1)
        apart(p582, thumb, 0.1)
        apart(right, job, 0.15)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(p58, bars58, bar59)), FadeOut(fail), FadeIn(p582, shift=UP * 0.1),
                      run_time=0.6)
            self.play(FadeIn(bar585), run_time=0.4)
            vo.wait_until("no URL")
            self.play(FadeIn(x_url), run_time=0.3)
            self.play(Create(x_cross), FadeIn(no_url, shift=LEFT * 0.1), run_time=0.5)
            self.play(FadeIn(ex833, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Something starts it")
            self.play(Indicate(batch_tag, color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("runs to completion")
            self.play(Indicate(VGroup(job.parts["edge"], job.parts["exit"]), color=TURN, scale_factor=1.2),
                      run_time=vo.remaining(0.8))

        # ========================================================== 5. the hook, fixed
        en = EndlessStrip(12.4)
        en.shift([JOB_X0 - en.parts["axis"].get_left()[0], JOB_Y, 0])
        red_tag = cmd_tag("serve", ERR)
        clock_r = en.clock.get_right()[0]
        red_tag.move_to([clock_r + 0.35 + red_tag.width / 2, en.clock.face.get_center()[1], 0])
        fixed = chip(FIXED_CMD, OWN, size=CAPTION, font=MONO)
        fixed.move_to([clock_r + 0.35 + fixed.width / 2, en.clock.face.get_center()[1] + 0.25, 0])
        p747 = src_panel(README, 747, 748)
        p747.move_to([0, PANEL_TOP - p747.height / 2, 0])
        bar748 = p747.bar(748, TURN, 0.22)
        args = arg_chips()
        args.move_to([0, PANEL_TOP - args.height / 2 - 0.05, 0])
        job2 = place_job(JobStrip(JOB_W, seg_w=SEG_W), JOB_X0, JOB_Y)
        en_vis = VGroup(*[en.parts[n] for n in ("axis", "clock", "bar", "wall", "wall_label")])
        inside_frame(en_vis, red_tag, fixed, p747, args)
        apart(fixed, en.parts["wall_label"], 0.15)
        apart(fixed, job2.parts["exit"], 0.06)
        apart(fixed, args, 0.1)
        apart(p747, en_vis, 0.1)
        apart(args, en_vis, 0.1)
        apart(p747, thumb, 0.1)
        apart(args, thumb, 0.1)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p582, bar585, right)), FadeOut(job), FadeOut(batch_tag), run_time=0.6)
            self.play(FadeIn(en, shift=DOWN * 2.0), FadeIn(red_tag, shift=DOWN * 2.0), run_time=0.8)
            self.play(*en.grow_to(en.wall_at, run_time=1.2))
            self.play(*en.parts_in("wall", anim=lambda mob: FadeIn(mob, shift=DOWN * 0.6)),
                      *en.parts_in("wall_label"), en.parts["bar"].animate.set_stroke(ERR, 3), run_time=0.5)
            vo.wait_until("The job inherited")
            self.play(FadeIn(p747, shift=UP * 0.1), Indicate(red_tag, color=ERR, scale_factor=1.2), run_time=0.7)
            vo.wait_until("The fix")
            self.play(FadeIn(bar748), Indicate(words(p747, 748, "This replaces image's web-server command."),
                                               color=TURN, scale_factor=1.04), run_time=0.8)
            vo.wait_until("the command python")
            self.play(FadeOut(VGroup(p747, bar748)), FadeIn(args.hdr), FadeIn(args.rows[0], shift=RIGHT * 0.1),
                      ReplacementTransform(red_tag, fixed), run_time=0.7)
            vo.wait_until("with the batch arguments")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in args.rows[1:]], lag_ratio=0.4),
                      run_time=0.9)
            vo.wait_until("Same image")
            en.clock.freeze()
            self.add(job2)
            self.play(*en.cut_into(job2), run_time=0.8)
            self.play(job2.run_all(1.4), FadeOut(en), run_time=vo.remaining(1.4))

        # ========================================================== 6. who presses start?
        sx = -6.3   # the service thumbnail moves left; the job strip moves right
        job_dx = 0.9 - JOB_X0
        job_dy = 1.25 - JOB_Y
        exe = execute_button()
        ill = illustration_tag()
        sch = scheduler_clock()
        sch.move_to([-5.4, -1.75, 0])
        not_here = grey_tag("not in this README")
        night_y = -2.35
        axis = Arrow([-4.4, night_y, 0], [6.3, night_y, 0], buff=0, color=S.GREY, stroke_width=2.5,
                     tip_length=0.16, max_tip_length_to_length_ratio=0.05)
        nights, minis, drops = VGroup(), [], []
        for k, x in enumerate((-2.7, 0.75, 4.2)):
            nights.add(label(f"night {k + 1}", CAPTION, S.GREY).move_to([x + 0.65, night_y - 0.35, 0]))
            bar = Rectangle(width=1.3, height=0.3, stroke_color=CTR, stroke_width=2).set_fill(CTR, 0.3)
            bar.move_to([x, night_y + 0.4, 0], aligned_edge=LEFT)
            edge = Line([x + 1.3, night_y + 0.2, 0], [x + 1.3, night_y + 0.6, 0], color=OWN, stroke_width=6)
            minis.append((bar, edge))
            drops.append(Arrow([x, night_y + 1.45, 0], [x, night_y + 0.58, 0], buff=0, color=ROUTE,
                               stroke_width=3, tip_length=0.14))
        not_here.move_to([-6.4 + not_here.width / 2, -0.65, 0])
        sched = VGroup(sch, not_here, axis, nights)

        with self.voiceover(SAY[6]) as vo:
            ax = sv.parts["axis"]
            sv_d = [sx - ax.get_left()[0], 0.65 - ax.get_center()[1], 0]
            lab_to = lab_row.copy().move_to([sx + lab_row.width / 2, 2.2, 0])
            self.play(sv.animate.shift(sv_d), Transform(lab_row, lab_to), FadeOut(args),
                      FadeOut(fixed), job2.animate.shift([job_dx, job_dy, 0]), run_time=0.9)
            exe.move_to([job2.span()[0] + exe.width / 2, 2.25, 0])
            ill.next_to(exe, RIGHT, buff=0.25)
            trig = Arrow(exe.get_bottom(), [job2.span()[0] + 0.15, job2.parts["seg0"].get_top()[1], 0], buff=0.05,
                         color=ROUTE, stroke_width=3, tip_length=0.14)
            inside_frame(thumb, job2, exe, ill, sched)
            apart(thumb, job2, 0.2)
            apart(exe, job2.parts["exit"], 0.1)
            apart(ill, job2.parts["exit"], 0.1)
            apart(exe, VGroup(*m.slots), 0.1)
            apart(VGroup(exe, ill), lr, 0.1)
            apart(thumb, m.label_of(1), 0.08)
            apart(job2, sched, 0.3)
            apart(not_here, VGroup(*drops), 0.1)
            vo.wait_until("you click Execute")
            self.play(FadeIn(exe), FadeIn(ill), run_time=0.4)
            self.play(exe.press(), *job2.parts_out(*[f"seg{i}" for i in range(4)],
                                                   *[f"lab{i}" for i in range(4)], "edge", "exit"), run_time=0.45)
            self.play(Create(trig), run_time=0.4)
            self.play(job2.run_all(1.4), run_time=1.4)
            vo.wait_until("For a nightly run")
            self.play(FadeIn(sch), Create(axis), FadeIn(nights), FadeOut(trig), run_time=0.7)
            for k in range(3):
                bar, edge = minis[k]
                self.play(*sch.run_to(k + 1, 0.5), Create(drops[k]), run_time=0.5)
                self.play(GrowFromEdge(bar, LEFT), run_time=0.5, rate_func=linear)
                self.play(Create(edge), run_time=0.2)
                if k == 1:
                    vo.wait_until("which this README does not use")
                    self.play(FadeIn(not_here, shift=LEFT * 0.1), run_time=0.4)
            self.wait(vo.remaining(0.3))

        # ========================================================== 7. try one (PONDER P1)
        nightly = VGroup(sched, *drops, *[VGroup(b, e) for b, e in minis])
        stem = chip("indexes new documents → exits · once an hour", S.GREY, size=CAPTION + 2)
        stem.move_to([0, -1.1, 0])
        inside_frame(stem)
        apart(stem, VGroup(thumb, job2), 0.2)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(nightly), run_time=0.6)
            vo.wait_until("A container indexes")
            self.play(FadeIn(stem, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("Read the lifecycle")
            self.play(Indicate(thumb, color=TURN, scale_factor=1.06), run_time=0.9)
            self.play(Indicate(VGroup(job2.parts["edge"], job2.parts["exit"]), color=TURN, scale_factor=1.25),
                      run_time=vo.remaining(0.9))
        # the stage is dimmed here, before the card, so the card comes in on its own
        self.play(FadeOut(VGroup(sv, lab_row)), FadeOut(VGroup(job2, exe, ill)), FadeOut(stem),
                  dim(m), dim(lr), run_time=0.5)
        card = mcq_ponder(self, P1_Q, P1_OPTS, seconds=10)

        # ========================================================== 8. the reveal
        with self.voiceover(SAY[8]) as vo:
            anims = card.right(*P1_RIGHT)
            # MCQCard.right()'s YELLOW box is one row tall and its bottom edge crosses the note
            # (reported): grow it here to hold the option row and its note.
            hl, note_b = card.marks[0], card.marks[2]
            top = card.rows[1].get_top()[1] + 0.07
            hl.stretch_to_fit_height(top - note_b.get_bottom()[1] + 0.07)
            hl.move_to([hl.get_center()[0], top - hl.height / 2, 0])
            guard(hl.get_bottom()[1] > card.rows[2].get_top()[1] + 0.02, "B's box reaches option C")
            self.play(*anims, run_time=0.7)
            vo.wait_until("A pays for")
            self.play(*card.wrong(0, P1_WRONG[0]), run_time=0.6)
            vo.wait_until("C breaks")
            self.play(*card.wrong(2, P1_WRONG[2]), run_time=0.6)
            vo.wait_until("D works")
            self.play(*card.wrong(3, P1_WRONG[3]), run_time=0.6)
            vo.wait_until("Why that matters")
            self.play(Indicate(card.rows[1], color=TURN, scale_factor=1.03), run_time=vo.remaining(0.6))

        # ========================================================== 9. the rule -> map slot 1
        rule = RuleCard(RULE_TOP, RULE_BOTTOM)
        mini_job = place_job(JobStrip(JOB_W, seg_w=SEG_W, axis=False), -6.1, 0.2)
        job_t = label("job", CAPTION + 4, CTR).next_to(mini_job.parts["seg0"], UP, buff=0.55) \
            .align_to(mini_job.parts["seg0"], LEFT)
        inst = instance_box(2.6, 0.5)
        ear = ear_chip().next_to(inst, DOWN, buff=0.15).align_to(inst, LEFT)
        surl = url_chip("https://…run.app").next_to(inst, UP, buff=0.2).align_to(inst, LEFT)
        svc = VGroup(inst, ear, surl).move_to([3.6, 0.25, 0])
        svc_t = label("service", CAPTION + 4, CLOUD).next_to(svc, UP, buff=0.2).align_to(svc, LEFT)
        req = Arrow(inst.get_top() + RIGHT * 1.6 + UP * 0.55, inst.get_top() + RIGHT * 1.6, buff=0.02,
                    color=ROUTE, stroke_width=3, tip_length=0.14)
        inside_frame(rule, mini_job, job_t, svc, svc_t)
        apart(VGroup(mini_job, job_t), VGroup(svc, svc_t), 0.3)
        apart(VGroup(mini_job, job_t, svc, svc_t), rule, 0.2)
        apart(VGroup(job_t, svc_t, surl), m.caption, 0.1)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(card), undim(m), undim(lr), run_time=0.6)
            self.play(rule.frame_in(), run_time=0.4)
            self.play(rule.line_in(0), run_time=0.8)
            vo.wait_until("pick a job")
            self.add(mini_job)
            self.play(FadeIn(job_t), mini_job.run_all(1.4), run_time=1.4)
            vo.wait_until("If it says it answers")
            self.play(rule.line_in(1), run_time=0.8)
            vo.wait_until("pick a service")
            self.play(FadeIn(svc_t), FadeIn(inst), FadeIn(ear), FadeIn(surl), run_time=0.6)
            self.play(Create(req), Indicate(ear, color=TURN, scale_factor=1.1), run_time=vo.remaining(0.8))
        self.wait(0.6)
        self.play(FadeOut(VGroup(mini_job, job_t, svc, svc_t, req)), run_time=0.5)
        rule.shrink_into(self, m, 1)
        self.play(m.pulse(1), run_time=0.7)
        self.wait(0.6)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)
        self.wait(0.3)
