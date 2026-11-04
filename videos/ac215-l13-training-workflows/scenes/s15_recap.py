"""S15 · The missing model, teardown, recap (AC215 L13) — `Recap`.

Beats (script.md, ## S15; one voiceover block each). No tracker at first; lref("5–6, 9–10, 21") top
right, whole scene.
0. A cockpit terminal (chip "our capture: a fresh cockpit", every command `extra`): `python cli.py`
   → laptop/60: 43, …, 47–48 (48 RED); CODE(cli.py: 7) above. `export GCP_REGION=us-central1` (no
   output), `python cli.py` → 60: 51–52, …, 119 (wrapped, RED). The code panel gives way to the GREY
   chip "the Python SDK route · L15 · sends no --wandb_key (scene 11: yours was 2)".
1. V4 step 5 (the miniature VM): it runs, the script exits, the VM dissolves, the meter stops, the
   trained weights are left as a GREY-dashed ghost that drifts up. `erratum` chips "nothing calls
   model.save" and "--model-dir and --lr: parsed, never used" with CODE(task.py: 27–30); the run
   record's artifacts cell stays "?". A GREY-dashed arrow to "L15 · saves the model to a bucket";
   chip "exercise 4: today".
2. Tracker `extra · clean-up` 1→3 and the GOLD-framed shutdown checklist, one page per tracker step
   (deviation: six items and two terminal outputs do not fit one card): page 1 = items 1–3 (jobs,
   bucket, console); page 2 = item 4 (`exit`) with a laptop terminal: `docker ps -a` (90:2, nothing
   listed, "--rm") and `docker image ls` (91:2–7, `2.59GB` ringed, `at the time of recording`), then
   the "need the disk?" rows; page 3 = items 5–6 (notebooks, keys). `▶ your turn` on every page.
3. V1 complete (TrainingMap.at("S15") built dark) lights one group per sentence with a companion
   strip under it: the folder + the WHITE seven-column ledger; the shared axis with its PURPLE
   callback pipe and the Config drawer inside `wandb.init`; the GREEN tarball into Google's
   ORANGE-banded TEAL image (the cockpit stays home), the ORANGE service-agent badge, the args chip
   with the RED key; the three switches and two replicas on a PINK all-reduce link. Then all_dark().
4. "Test yourself": five questions one at a time (24 pt, 3 lines max) with a shape-only thumbnail;
   each answered card collapses into a numbered label list at the left.
5. Footer cards (exercises.md, study guide), the GREY-dashed "Next" card (L14, L15), then slide 5's
   three dials with the third lit and the small ledger. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, COST, CPU_IMAGE, ERR, FUTURE, IMAGE, INK, NARRATION, OWNED, P_COCKPIT, P_REPO,
                    ROUTE, SAY_COUNT, SYSTEM, TURN, RunLedger, TarballTrip, TrainingMap, arrow, beside, capture,
                    code, container_note, dashed_chip, drawer, err_chip, erratum_tag, extra_row, flash_tag,
                    grey_chip, istep, label, line_bar, lref, mono, on_bar, out, outline_box, parcel, pin, ring,
                    row_tag, split_prompt, squeeze, substring, term, time_row, track, tracker_cleanup, type_cmd,
                    your_turn)
from explainer import style as S

SAY = NARRATION["S15"]

SDK_NOTE = "the Python SDK route · L15 · sends no --wandb_key (scene 11: yours was 2)"
SEVEN_COLS = ("environment", "code", "data", "model", "metrics", "artifacts", "notes")
QUESTIONS = (
    ("two tables", ("Notebooks A and B crowned different MobileNets.",
                    "Name two things neither table wrote down",
                    "that you'd need before calling the difference real.")),
    ("the trip", ("What travels from your laptop to Vertex AI,",
                  "which image does it run in,",
                  "and what never makes the trip?")),
    ("the config", ("After wandb.config = {...}, the run's config is {}.",
                    "Why, and what is the one-line fix?")),
    ("badges", ("Which identity submits the job, which runs it,",
                "and where does your W&B key end up?")),
    ("replicas", ("With MirroredStrategy on two GPUs, what is split,",
                  "what is averaged, and what must be created",
                  "inside strategy.scope()?")),
)
LEVERS = (("More Data", "pipeline · labels · versions"),
          ("Better/Faster Models", "architectures · transfer learning"),
          ("Faster Hardware", "GPUs · TPUs · multi-GPU"))


# ------------------------------------------------------------------ local helpers (no common.py names)
def seg_row(parts, size: float = 20) -> VGroup:
    """One row of mixed text: a str is WHITE label text; (text, 'm'|'l', colour) picks the font."""
    ms = []
    for p in parts:
        if isinstance(p, str):
            ms.append(label(p, size, INK))
        else:
            s, k, c = p
            ms.append(mono(s, size, c) if k == "m" else label(s, size, c))
    return VGroup(*ms).arrange(RIGHT, buff=0.14)


def check_item(n, rows, size: float = 20) -> VGroup:
    """A numbered checklist item: GREY number, rows left-aligned beside it. .num .rows"""
    num = label(str(n), 22, TURN)
    body = VGroup(*[seg_row(r, size) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
    g = VGroup(num, body).arrange(RIGHT, aligned_edge=UP, buff=0.25)
    g.num, g.rows = num, body
    return g


def gold_frame(content: Mobject, pad_x: float = 0.35, pad_y: float = 0.28, frame_w: float | None = None):
    """The GOLD frame of the shutdown checklist (opaque) around `content`."""
    w = frame_w or content.width + 2 * pad_x
    return RoundedRectangle(width=w, height=content.height + 2 * pad_y, corner_radius=0.16, stroke_color=COST,
                            stroke_width=3).set_fill(S.GREY_DARKER, 1)


def lever_dial(title: str, sub: str, radius: float = 1.2) -> VGroup:
    """S02's slide-5 dial (GREY half arc, ticks, needle low on the left, title, one GREY line)."""
    arc = Arc(radius=radius, start_angle=0, angle=PI, color=S.GREY, stroke_width=5)
    ticks = VGroup(*[Line(radius * 0.82 * np.array([np.cos(a), np.sin(a), 0]),
                          radius * 0.98 * np.array([np.cos(a), np.sin(a), 0]), color=S.GREY, stroke_width=3)
                     for a in np.linspace(0.12 * PI, 0.88 * PI, 5)])
    a0 = 0.82 * PI
    needle = Line(ORIGIN, radius * 0.75 * np.array([np.cos(a0), np.sin(a0), 0]), color=S.GREY, stroke_width=5)
    pivot = Dot(ORIGIN, radius=0.07, color=S.GREY)
    t = label(title, 24, INK).next_to(arc, DOWN, buff=0.3)
    s = label(sub, 20, S.GREY).next_to(t, DOWN, buff=0.14)
    g = VGroup(arc, ticks, needle, pivot, t, s)
    g.arc, g.ticks, g.needle, g.pivot, g.title, g.sub = arc, ticks, needle, pivot, t, s
    return g


def dim_dial(d: VGroup) -> VGroup:
    for m in (d.arc, d.ticks, d.needle):
        m.set_stroke(opacity=0.35)
    d.pivot.set_fill(opacity=0.35)
    d.title.set_opacity(0.4)
    d.sub.set_opacity(0.4)
    return d


def ledger_icon() -> VGroup:
    """S02's small GREY ledger (a sheet with rows) and its word."""
    sheet = RoundedRectangle(width=0.9, height=0.75, corner_radius=0.06, stroke_color=S.GREY,
                             stroke_width=3).set_fill(S.GREY_DARKER, 1)
    c = sheet.get_center()
    rows = VGroup(*[Line(c + np.array([-0.36, y, 0]), c + np.array([0.36, y, 0]), color=S.GREY,
                         stroke_width=2.5 if y > 0.15 else 1.5) for y in (0.2, 0.02, -0.14, -0.28)])
    col = Line(c + np.array([-0.05, 0.3, 0]), c + np.array([-0.05, -0.32, 0]), color=S.GREY, stroke_width=1.5)
    word = label("bookkeeping", 20, S.GREY).next_to(sheet, DOWN, buff=0.14)
    return VGroup(sheet, rows, col, word)


def seven_ledger() -> VGroup:
    """V2 in brief: the seven column heads over two WHITE run rows (empty cells: no values)."""
    heads = VGroup(*[label(s, 20, INK) for s in SEVEN_COLS]).arrange(RIGHT, buff=0.3)
    w = heads.width + 0.4
    rows = VGroup(*[RoundedRectangle(width=w, height=0.3, corner_radius=0.05, stroke_color=INK, stroke_width=2)
                    for _ in range(2)]).arrange(DOWN, buff=0.08)
    rows.next_to(heads, DOWN, buff=0.12)
    seps = VGroup(*[Line([(heads[i].get_right()[0] + heads[i + 1].get_left()[0]) / 2, rows.get_top()[1], 0],
                         [(heads[i].get_right()[0] + heads[i + 1].get_left()[0]) / 2, rows.get_bottom()[1], 0],
                         color=S.GREY, stroke_width=1.5) for i in range(6)])
    return VGroup(heads, rows, seps)


def switch_glyph(word: str) -> VGroup:
    """A small switch, on (GREEN pill, knob right), with its word under it."""
    pill = RoundedRectangle(width=0.8, height=0.36, corner_radius=0.18, stroke_color=OWNED,
                            stroke_width=3).set_fill(OWNED, 0.25)
    knob = Dot(pill.get_right() + LEFT * 0.18, radius=0.12, color=OWNED)
    t = label(word, 20, INK).next_to(pill, DOWN, buff=0.1)
    return VGroup(pill, knob, t)


def gpu_card(word: str, card_w: float = 1.3, card_h: float = 0.9) -> VGroup:
    """A GPU card for the recap: BLUE frame, a small network of dots, its word under it."""
    fr = RoundedRectangle(width=card_w, height=card_h, corner_radius=0.08, stroke_color=CLOUD,
                          stroke_width=3).set_fill(CLOUD, 0.1)
    dots = VGroup(*[VGroup(*[Dot(radius=0.05, color=IMAGE) for _ in range(n)]).arrange(DOWN, buff=0.1)
                    for n in (2, 3, 2)]).arrange(RIGHT, buff=0.25).move_to(fr)
    t = label(word, 20, INK).next_to(fr, DOWN, buff=0.1)
    return VGroup(fr, dots, t)


def mini_badge(color, gear: bool = False) -> VGroup:
    """A badge without words (thumbnail): frame, clip, a portrait square (a gear for the agent)."""
    fr = RoundedRectangle(width=0.75, height=0.95, corner_radius=0.08, stroke_color=color,
                          stroke_width=3).set_fill(S.GREY_DARKER, 1)
    clip = RoundedRectangle(width=0.32, height=0.12, corner_radius=0.04, stroke_color=color,
                            stroke_width=2).set_fill(S.BG, 1).move_to(fr.get_top())
    pf = RoundedRectangle(width=0.36, height=0.36, corner_radius=0.05, stroke_color=color,
                          stroke_width=2).set_fill(color, 0.2).move_to(fr.get_center() + UP * 0.12)
    inner = (Circle(radius=0.09, stroke_color=color, stroke_width=2.5).move_to(pf) if gear
             else Dot(pf.get_center(), radius=0.06, color=color))
    lines = VGroup(*[Line(LEFT * 0.22, RIGHT * 0.22, color=S.GREY, stroke_width=2) for _ in range(2)])
    lines.arrange(DOWN, buff=0.08).next_to(pf, DOWN, buff=0.1)
    return VGroup(fr, clip, pf, inner, lines)


def thumb_frame(content: Mobject) -> VGroup:
    fr = RoundedRectangle(width=4.2, height=2.2, corner_radius=0.12, stroke_color=S.GREY_DARK,
                          stroke_width=2).set_fill(S.BG, 1)
    content.move_to(fr)
    return VGroup(fr, content)


def thumb_tables() -> VGroup:
    def grid():
        rows = VGroup(*[RoundedRectangle(width=1.4, height=0.2, corner_radius=0.03, stroke_color=INK,
                                         stroke_width=1.8) for _ in range(5)]).arrange(DOWN, buff=0.07)
        ringed = SurroundingRectangle(rows[0], color=TURN, buff=0.05, stroke_width=2.5)
        return VGroup(rows, ringed)
    return thumb_frame(VGroup(grid(), grid()).arrange(RIGHT, buff=0.5))


def thumb_trip() -> VGroup:
    home = RoundedRectangle(width=0.9, height=0.6, corner_radius=0.06, stroke_color=IMAGE,
                            stroke_width=2.5).set_fill(IMAGE, 0.2)
    roof = Polygon(home.get_corner(UL), home.get_top() + UP * 0.3, home.get_corner(UR), stroke_color=IMAGE,
                   stroke_width=2.5)
    house_ = VGroup(home, roof)
    pc = parcel(None, OWNED, 20, 0.45, 0.32)
    vmb = RoundedRectangle(width=1.5, height=1.3, corner_radius=0.08, stroke_color=CLOUD,
                           stroke_width=2.5).set_fill(CLOUD, 0.08)
    img = Rectangle(width=1.3, height=0.22, stroke_width=0).set_fill(IMAGE, 0.8).move_to(vmb.get_bottom() + UP * 0.22)
    lay = Rectangle(width=1.3, height=0.2, stroke_width=0).set_fill(SYSTEM, 0.8).next_to(img, UP, buff=0.04)
    vm_ = VGroup(vmb, img, lay)
    row = VGroup(house_, pc, vm_).arrange(RIGHT, buff=0.55)
    rt = Arrow(pc.get_right(), vmb.get_left(), buff=0.08, color=ROUTE, stroke_width=4, tip_length=0.16)
    stay = DashedLine(house_.get_right() + RIGHT * 0.05, pc.get_left() + LEFT * 0.05, color=S.GREY, stroke_width=2)
    return thumb_frame(VGroup(row, rt, stay))


def thumb_config() -> VGroup:
    run = RoundedRectangle(width=1.6, height=1.2, corner_radius=0.08, stroke_color=CLOUD,
                           stroke_width=2.5).set_fill(CLOUD, 0.08)
    dr = RoundedRectangle(width=1.1, height=0.4, corner_radius=0.05, stroke_color=OWNED,
                          stroke_width=2.5).set_fill(OWNED, 0.12).move_to(run.get_center() + DOWN * 0.2)
    empty = mono("{}", 20, ERR).move_to(dr)
    loose = RoundedRectangle(width=1.3, height=0.9, corner_radius=0.06, stroke_color=ERR,
                             stroke_width=2.5).set_fill(INK, 0.08)
    keys = VGroup(*[Line(LEFT * 0.4, RIGHT * 0.4, color=INK, stroke_width=2) for _ in range(4)]).arrange(DOWN, buff=0.12)
    keys.move_to(loose)
    pair = VGroup(VGroup(run, dr, empty), VGroup(loose, keys)).arrange(RIGHT, buff=0.8)
    ptr = Arrow(run.get_top() + UP * 0.1 + RIGHT * 0.5, loose.get_top() + UP * 0.05, buff=0.05, color=TURN,
                stroke_width=3, tip_length=0.14, path_arc=-1.2)
    return thumb_frame(VGroup(pair, ptr))


def thumb_badges() -> VGroup:
    bs = VGroup(mini_badge(OWNED), mini_badge(SYSTEM, gear=True), mini_badge(ERR)).arrange(RIGHT, buff=0.5)
    cords = VGroup(*[VGroup(Line(b.get_top() + UP * 0.45 + LEFT * 0.2, b.get_top(), color=S.GREY, stroke_width=2),
                            Line(b.get_top() + UP * 0.45 + RIGHT * 0.2, b.get_top(), color=S.GREY, stroke_width=2))
                     for b in bs])
    return thumb_frame(VGroup(cords, bs))


def thumb_replicas() -> VGroup:
    def card_():
        fr = RoundedRectangle(width=1.2, height=0.8, corner_radius=0.06, stroke_color=CLOUD,
                              stroke_width=2.5).set_fill(CLOUD, 0.1)
        tiles = VGroup(*[Square(0.12, stroke_width=0).set_fill(INK, 0.8) for _ in range(8)])
        tiles.arrange_in_grid(rows=2, buff=0.05).move_to(fr)
        return VGroup(fr, tiles)
    a, b = card_(), card_()
    pair = VGroup(a, b).arrange(RIGHT, buff=1.0)
    link = Line(a.get_right(), b.get_right() + LEFT * 1.2, color=ROUTE, stroke_width=4)
    up_a = Arrow(a.get_top(), a.get_top() + UP * 0.45, buff=0.02, color=ROUTE, stroke_width=3, tip_length=0.12)
    up_b = Arrow(b.get_top(), b.get_top() + UP * 0.45, buff=0.02, color=ROUTE, stroke_width=3, tip_length=0.12)
    return thumb_frame(VGroup(pair, link, up_a, up_b))


THUMBS = (thumb_tables, thumb_trip, thumb_config, thumb_badges, thumb_replicas)


def question_panel(i: int) -> VGroup:
    """Question i+1: a YELLOW-framed card with the question (24 pt) and its thumbnail. .frame .text .thumb"""
    name, lines = QUESTIONS[i]
    head = label(f"{i + 1} · {name}", 22, TURN)
    txt = VGroup(*[label(s, 24, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
    th = THUMBS[i]()
    inner = VGroup(head, txt, th).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    th.align_to(txt, LEFT)
    fr = RoundedRectangle(width=8.7, height=inner.height + 0.5, corner_radius=0.16, stroke_color=TURN,
                          stroke_width=3).set_fill(S.BG, 1)
    inner.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
    g = VGroup(fr, inner)
    g.frame, g.text, g.thumb = fr, txt, th
    return g


class Recap(VoiceScene):
    def keep_only(self, *keep, run_time: float = 0.6, shift=UP * 0.2):
        fam = {id(x) for k in keep for x in k.get_family()}
        gone = [m for m in self.mobjects if not any(id(x) in fam for x in m.get_family())]
        if gone:
            self.play(FadeOut(Group(*gone), shift=shift), run_time=run_time)
            self.remove(*gone)

    def construct(self):
        assert len(SAY) == SAY_COUNT["S15"] == 6, len(SAY)
        ref = lref("5–6, 9–10, 21")
        c60 = capture("60")

        # ========================================================== 0. cli.py, the launcher the README never mentions
        t = term(P_COCKPIT, rows=9)
        ex = on_bar(t, extra_row())
        note0 = container_note("our capture: a fresh cockpit")
        note0.move_to([t.box.get_left()[0] + note0.width / 2, 2.65, 0])
        p7 = code("cli.py", 7)
        p7.move_to([t.box.get_right()[0] - p7.width / 2, t.box.get_top()[1] + 0.2 + p7.height / 2, 0])
        assert p7.get_top()[1] < note0.get_bottom()[1] + 0.4 and p7.get_left()[0] > note0.get_right()[0] - 3.0
        bar7 = line_bar(p7.code, 0, ERR)
        sdk = grey_chip(SDK_NOTE).move_to([0, p7.get_center()[1], 0])
        assert sdk.width < 12.8, sdk.width
        e1 = c60.at(43, "…", (47, 48))
        e2 = c60.at(51, 52, "…", 119)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(ref), FadeIn(t), FadeIn(note0, shift=DOWN * 0.15), run_time=0.7)
            ln0 = istep(self, t, c60.line(42))
            vo.wait_until("the Python SDK route")
            self.play(Indicate(substring(ln0, "cli.py"), color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("As an extra run")
            self.play(FadeIn(ex, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, ex, INK)
            vo.wait_until("it fails at once")
            r1 = out(self, t, e1[:3] + [(e1[3], ERR)])
            vo.wait_until("because only cli.sh")
            self.play(FadeIn(p7, shift=DOWN * 0.15), run_time=0.6)
            self.play(FadeIn(bar7), Indicate(r1[-1], color=ERR, scale_factor=1.03), run_time=0.6)
            vo.wait_until("Export it")
            istep(self, t, c60.line(49))
            self.play(FadeOut(VGroup(p7, bar7), shift=UP * 0.15), FadeIn(sdk, shift=DOWN * 0.15), run_time=0.6)
            self.remove(p7, bar7)
            istep(self, t, c60.line(50))
            vo.wait_until("it fails at the missing key file")
            r2 = out(self, t, e2[:3] + [(e2[3], ERR)], wrap=True)
            self.play(Indicate(r2[-2:], color=ERR, scale_factor=1.02), run_time=0.7)

        # ========================================================== 1. where is the trained model?
        vm = TarballTrip.vm(mini=True, center=(-3.6, 1.25))
        er = erratum_tag()
        c_save = grey_chip("nothing calls model.save")
        c_flags = grey_chip("--model-dir and --lr: parsed, never used")
        right = VGroup(er, c_save, c_flags).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        right.move_to([0.0, 1.75, 0], aligned_edge=LEFT)
        p27 = code("package/trainer/task.py", 27, 30, font_size=20,
                   cuts={28: 'default="test",', 30: "default=0.001,"})
        p27.move_to([0, -3.4 + p27.height / 2, 0])
        bars27 = VGroup(line_bar(p27.code, 1, TURN), line_bar(p27.code, 3, TURN))
        art_lab = label("artifacts", 20, INK)
        art_cell = outline_box(0.7, 0.42, FUTURE, solid=False)
        q_mark = label("?", 24, ERR).move_to(art_cell)
        art = VGroup(art_lab, VGroup(art_cell, q_mark)).arrange(RIGHT, buff=0.2)
        art.move_to([-3.6, 0.25, 0])
        l15 = dashed_chip("L15 · saves the model to a bucket").next_to(c_flags, DOWN, buff=0.45, aligned_edge=LEFT)
        ex4 = grey_chip("exercise 4: today").next_to(l15, DOWN, buff=0.2, aligned_edge=LEFT)
        assert ex4.get_bottom()[1] > p27.get_top()[1] + 0.1, (ex4.get_bottom(), p27.get_top())

        with self.voiceover(SAY[1]) as vo:
            self.keep_only(ref, shift=DOWN * 0.2)
            self.play(vm.appear(), run_time=0.8)
            self.play(vm.image_in(), run_time=0.6)
            self.play(vm.unwrap(), run_time=0.7)
            self.play(vm.pip(), vm.run(), run_time=0.7)
            vo.wait_until("When the script ends")
            self.play(vm.dissolve(), run_time=1.6)
            self.remove(vm.meter, *vm.meter.get_family())   # the stopped needle lingers otherwise
            ghost = vm.ghost
            vo.wait_until("and the weights with it")
            self.play(ghost.animate.shift(UP * 0.3), run_time=0.6)
            self.play(ghost[0].frame.animate.set_stroke(opacity=0.6), ghost[1].animate.set_opacity(0.75),
                      FadeIn(art, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("nothing calls model save")
            self.play(FadeIn(er, shift=LEFT * 0.1), FadeIn(c_save, shift=LEFT * 0.15), FadeIn(p27, shift=UP * 0.15),
                      run_time=0.6)
            vo.wait_until("and the model dir flag is ignored")
            self.play(FadeIn(bars27[0]), FadeIn(c_flags, shift=LEFT * 0.15), run_time=0.6)
            self.play(FadeIn(bars27[1]), run_time=0.4)
            vo.wait_until("Lecture 15 saves the model")
            ar = arrow(ghost.get_right(), l15.get_left(), FUTURE, buff=0.15)
            ar_d = DashedVMobject(ar, num_dashes=14)
            self.play(Create(ar_d), FadeIn(l15, shift=LEFT * 0.15), run_time=0.8)
            vo.wait_until("exercise 4 does it today")
            self.play(FadeIn(ex4, shift=UP * 0.1), run_time=0.5)
            flash_tag(self, ex4, INK)

        # ========================================================== 2. shut down (tracker extra · clean-up)
        tr = tracker_cleanup(1)
        assert tr.caption.get_right()[0] < ref.get_left()[0]
        yt = your_turn()
        cmd_list = split_prompt(capture("40").line(91))[1]
        assert cmd_list == "gcloud ai custom-jobs list --region=us-central1", cmd_list
        it1 = check_item(1, [["in the cockpit:", (cmd_list, "m", INK), ("→ the JOB_ID", "l", S.GREY)],
                             [("gcloud ai custom-jobs cancel JOB_ID --region=us-central1", "m", INK)],
                             [("nothing RUNNING or PENDING · tried cli.py? also check Training pipelines", "l",
                               S.GREY)]])
        it2 = check_item(2, [[("gsutil rm $GCS_BUCKET_URI/cheese-app-trainer.tar.gz", "m", INK)],
                             ["the", ("experiment_<ts>/", "m", INK), "folders",
                              ("(notebook B: under your account's folder)", "l", S.GREY)],
                             [("or delete the bucket", "l", INK)]])
        it3 = check_item(3, [["or in the console: Vertex AI → Training → Custom jobs → Cancel"],
                             ["Cloud Storage → your bucket → delete"]])
        hd1 = label("shut down", 22, COST)
        page1 = VGroup(hd1, it1, it2, it3).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        fr1 = gold_frame(page1, frame_w=12.9)
        fr1.move_to([0, 2.65 - fr1.height / 2, 0])
        page1.move_to(fr1).align_to(fr1, LEFT).shift(RIGHT * 0.35)
        assert page1.width < 12.3 and fr1.get_bottom()[1] > -3.5, (page1.width, fr1.get_bottom())
        yt.move_to([fr1.get_right()[0] - 0.25 - yt.width / 2, hd1.get_center()[1], 0])

        it4 = check_item(4, [["then", ("exit", "m", INK), "the cockpit", ("(--rm removes it)", "l", S.GREY)]])
        disk = VGroup(seg_row(["need the disk?", ("docker image rm model-training-cli", "m", INK)]),
                      seg_row([("python:3.13-slim-bookworm python:3.13-slim-bullseye", "m", INK)]),
                      seg_row([("ran our extras? also", "l", S.GREY),
                               ("trainer-standin python:3.10-slim-bookworm", "m", INK)]),
                      seg_row([("Linux:", "l", S.GREY), ("sudo rm trainer.tar.gz", "m", INK)]))
        disk.arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        disk[1].shift(RIGHT * (disk[0][1].get_left()[0] - disk[1].get_left()[0]))
        page2 = VGroup(it4, disk).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        disk.shift(RIGHT * (it4.rows.get_left()[0] - disk.get_left()[0]))
        fr2_full = gold_frame(page2, frame_w=12.9)
        fr2_full.move_to([0, 2.65 - fr2_full.height / 2, 0])
        page2.move_to(fr2_full).align_to(fr2_full, LEFT).shift(RIGHT * 0.35)
        fr2 = gold_frame(it4, frame_w=12.9)
        fr2.move_to([0, 2.65 - fr2.height / 2, 0])
        it4.move_to(fr2).align_to(fr2, LEFT).shift(RIGHT * 0.35)
        disk.next_to(it4, DOWN, buff=0.22, aligned_edge=LEFT).align_to(it4.rows, LEFT)
        fr2_full.align_to(fr2, UP)
        t2 = term(P_REPO, rows=9)
        assert t2.box.get_top()[1] < fr2.get_bottom()[1] - 0.1, (t2.box.get_top(), fr2.get_bottom())
        img_rows = squeeze(capture("91").at((2, 7)))

        it5 = check_item(5, [["notebook B:", ("wandb.finish()", "m", INK),
                              ("· both notebooks: Runtime → Disconnect and delete runtime", "l", INK)]])
        it6 = check_item(6, [["end of term: delete the", ("model-trainer", "m", INK), "key in IAM and its JSON in",
                              ("secrets/", "m", INK)],
                             ["rotate your W&B key", ("and update the Colab secret", "l", INK), ("WandB", "m", INK)],
                             [("the old export lives on in that terminal: open a new one", "l", S.GREY)]])
        page3 = VGroup(it5, it6).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        fr3 = gold_frame(page3, frame_w=12.9)
        fr3.move_to([0, 2.65 - fr3.height / 2, 0])
        page3.move_to(fr3).align_to(fr3, LEFT).shift(RIGHT * 0.35)
        def below(fr):
            return [fr.get_right()[0] - yt.width / 2, fr.get_bottom()[1] - 0.12 - yt.height / 2, 0]

        for pg in (page2, page3):
            assert pg.width < 12.3, pg.width

        with self.voiceover(SAY[2]) as vo:
            self.keep_only(ref, shift=DOWN * 0.2)
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(fr1, scale=0.97), FadeIn(hd1), run_time=0.7)
            vo.wait_until("pause and work through the list")
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt, TURN)
            vo.wait_until("From inside the cockpit")
            self.play(FadeIn(it1, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("or in the console")
            self.play(FadeIn(it3, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("make sure no custom job")
            self.play(Indicate(it1.rows[2], color=TURN, scale_factor=1.03), run_time=0.7)
            vo.wait_until("Remove the tarball")
            self.play(FadeIn(it2, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("Then exit")
            self.play(FadeOut(VGroup(it1, it2, it3, hd1), shift=UP * 0.2), Transform(fr1, fr2),
                      yt.animate.move_to(below(fr2)),
                      track(tr, 2), run_time=0.7)
            self.remove(it1, it2, it3, hd1)
            self.play(FadeIn(it4, shift=RIGHT * 0.2), FadeIn(t2), run_time=0.6)
            ln = type_cmd(self, t2, "docker ps -a", type_time=0.5)
            pin(self, ln, beside(extra_row(), ln))
            o90 = out(self, t2, [(r, S.GREY) for r in squeeze(capture("90").at(2))])
            pin(self, o90[-1], beside(row_tag("nothing listed · --rm"), o90[-1]))
            ln2 = type_cmd(self, t2, "docker image ls", type_time=0.5)
            pin(self, ln2, beside(extra_row(), ln2))
            o91 = out(self, t2, img_rows, run_time=0.5)
            tm = on_bar(t2, time_row())
            self.play(FadeIn(tm), run_time=0.4)
            gb = ring(substring(o91[1], "2.59GB"), TURN, buff=0.05)
            self.play(Create(gb), run_time=0.5)
            self.wait(0.8)
            self.play(FadeOut(VGroup(t2, tm, gb, *t2.lines), shift=DOWN * 0.2), run_time=0.5)
            self.remove(t2, tm, gb, *t2.lines)
            self.play(Transform(fr1, fr2_full), FadeIn(disk, shift=UP * 0.15), yt.animate.move_to(below(fr2_full)),
                      run_time=0.7)
            self.play(Indicate(disk[0][1], color=INK, scale_factor=1.04), run_time=0.8)
            self.wait(1.4)   # the disk rows get a moment even though the narration has moved on
            vo.wait_until("Finish the last W and B run")
            self.play(FadeOut(VGroup(it4, disk), shift=UP * 0.2), Transform(fr1, fr3), yt.animate.move_to(below(fr3)),
                      track(tr, 3), run_time=0.7)
            self.remove(it4, disk)
            self.play(FadeIn(it5, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("At the end of term")
            self.play(FadeIn(it6, shift=RIGHT * 0.2), run_time=0.7)
            vo.wait_until("which traveled in a job")
            kr = ring(it6.rows[1][0], ERR, buff=0.06)
            self.play(Create(kr), run_time=0.6)

        # ========================================================== 3. the whole lecture on one map
        m = TrainingMap.at("S15", lit=())
        cy = -2.45

        def strip_(*mobs, buff=0.6):
            g = VGroup(*mobs).arrange(RIGHT, buff=buff)
            g.move_to([0, cy, 0])
            assert g.width < 13.0 and g.get_bottom()[1] > -3.55, (g.width, g.get_bottom())
            return g

        folder = drawer("experiment_<ts>/", S.GREY, 20)
        s1 = strip_(folder, seven_ledger())
        axis = Rectangle(width=2.2, height=0.95, stroke_color=S.GREY, stroke_width=2)
        fit = mono("model.fit", 20, INK)
        g_axis = VGroup(fit, axis).arrange(RIGHT, buff=0.9)
        initbox = RoundedRectangle(width=4.0, height=1.05, corner_radius=0.1, stroke_color=CLOUD,
                                   stroke_width=2.5).set_fill(CLOUD, 0.08)
        init_t = mono("wandb.init(config=…)", 20, INK)
        cfg = drawer("Config", OWNED, 20, glyph=False, mono_font=False)
        VGroup(init_t, cfg).arrange(DOWN, buff=0.08).move_to(initbox)
        g_init = VGroup(initbox, init_t, cfg)
        strip_(g_axis, g_init, buff=1.0)
        curves = RunLedger.curves(axis)
        cpipe = RunLedger.callback_pipe(fit.get_right() + RIGHT * 0.08, axis)
        pc = parcel(None, OWNED, 20, 0.6, 0.42)
        img = VGroup(*[Rectangle(width=3.4, height=0.4, stroke_width=0) for _ in range(2)]).arrange(DOWN, buff=0.04)
        img[0].set_fill(SYSTEM, 0.35).set_stroke(SYSTEM, 2)
        img[1].set_fill(IMAGE, 0.35).set_stroke(IMAGE, 2)
        img_w = VGroup(label("TensorFlow · expected", 20, INK).move_to(img[0]), mono(CPU_IMAGE, 20, INK).move_to(img[1]))
        g_img = VGroup(img, img_w)
        agent = VGroup(mini_badge(SYSTEM, gear=True), label("service agent", 20, INK)).arrange(DOWN, buff=0.08)
        chip_err = err_chip("--wandb_key=…")
        args = VGroup(mono("--args", 20, S.GREY), chip_err).arrange(RIGHT, buff=0.15)
        strip_(pc, g_img, agent, args, buff=0.45)
        trip_ar = Arrow(pc.get_right(), img.get_left(), buff=0.08, color=ROUTE, stroke_width=4, tip_length=0.16)
        sws = VGroup(*[switch_glyph(w) for w in ("accelerator", "image", "quota")]).arrange(RIGHT, buff=0.35)
        gpus = VGroup(gpu_card("GPU 0"), gpu_card("GPU 1")).arrange(RIGHT, buff=1.3)
        strip_(sws, gpus, buff=1.2)
        link = Line(gpus[0][0].get_right(), gpus[1][0].get_left(), color=ROUTE, stroke_width=4)
        link_t = label("all-reduce", 20, ROUTE).next_to(link, UP, buff=0.08)

        with self.voiceover(SAY[3]) as vo:
            self.keep_only(ref, shift=DOWN * 0.2)
            self.play(FadeIn(m), run_time=0.9)
            vo.wait_until("A run is only as useful")
            self.play(m.light("nbA", "laneA", "folder", "bucket"), FadeIn(s1, shift=UP * 0.15), run_time=0.9)
            vo.wait_until("Curves need a callback")
            self.play(FadeOut(s1, shift=DOWN * 0.15), m.light("nbB", "laneB", "wandb"), run_time=0.6)
            self.remove(s1)
            self.play(FadeIn(g_axis), run_time=0.4)
            self.play(Create(cpipe), Create(curves), run_time=0.9)
            vo.wait_until("config goes into wandb init")
            self.play(FadeIn(g_init, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Only the tarball travels")
            gone = VGroup(g_axis, g_init, cpipe, curves)
            self.play(FadeOut(gone, shift=DOWN * 0.15), m.light("laptop", "cockpit", "secrets", "gcp", "tarball",
                                                                 "upload"), run_time=0.7)
            self.remove(gone)
            self.play(FadeIn(pc, shift=RIGHT * 0.2), Indicate(m.parts["tarball"], color=OWNED), run_time=0.6)
            vo.wait_until("into Google's image")
            self.play(m.light("vertex", "cpu_tile", "pull"), FadeIn(g_img), GrowArrow(trip_ar), run_time=0.8)
            vo.wait_until("run as the service agent")
            self.play(FadeIn(agent, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("your key in its arguments")
            self.play(m.light("key", "submit", "stream"), FadeIn(args, shift=UP * 0.15), run_time=0.7)
            vo.wait_until("One GPU needs three switches")
            gone = VGroup(pc, g_img, trip_ar, agent, args)
            self.play(FadeOut(gone, shift=DOWN * 0.15), m.light("gpu_tile"), run_time=0.6)
            self.remove(gone)
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in sws], lag_ratio=0.3), run_time=0.9)
            vo.wait_until("two GPUs split the batch")
            self.play(FadeIn(gpus, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("average gradients")
            self.play(Create(link), FadeIn(link_t), run_time=0.7)
            st = m.stamp_
            st_dim = st.copy()
            st_dim.box.set_stroke(S.GREY_DARK)
            st_dim.text.set_color(S.GREY)
            m.stamp_ = None   # all_dark() would fill the stamp's box GREY_DARK over its words
            self.play(m.all_dark(), Transform(st, st_dim), FadeOut(VGroup(sws, gpus, link, link_t), shift=DOWN * 0.15), run_time=1.2)
            self.remove(sws, gpus, link, link_t)

        # ========================================================== 4. test yourself
        head4 = label("Test yourself", 30, TURN).move_to([-4.65, 2.45, 0])
        panels = [question_panel(i) for i in range(5)]
        for p in panels:
            p.move_to([2.05, 0.2, 0])
            assert p.get_left()[0] > -2.45 and p.get_right()[0] < 6.5 and p.get_top()[1] < 2.85 \
                and p.get_bottom()[1] > -3.5, (p.get_left(), p.get_right(), p.get_top(), p.get_bottom())
        items = VGroup(*[label(f"{i + 1} · {QUESTIONS[i][0]}", 24, INK) for i in range(5)])
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([-6.2, 0.9, 0], aligned_edge=LEFT)
        items.align_to(np.array([0, 1.75, 0]), UP)
        anchors = ("One: what did neither", "Two: what travels", "Three: why is the config", "Four: who submits",
                   "Five: with two GPUs")

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(m), run_time=0.6)
            self.remove(m)
            self.play(FadeIn(head4, shift=DOWN * 0.15), run_time=0.6)
            cur = None
            for i, an in enumerate(anchors):
                vo.wait_until(an)
                anims = [FadeIn(panels[i], shift=LEFT * 0.3)]
                if cur is not None:
                    anims += [FadeOut(cur, shift=LEFT * 0.6), FadeIn(items[i - 1], shift=LEFT * 0.4)]
                self.play(*anims, run_time=0.7)
                if cur is not None:
                    self.remove(cur)
                cur = panels[i]
                self.play(Indicate(cur.thumb[1], color=TURN, scale_factor=1.04), run_time=0.7)

        # ========================================================== 5. answers, next, close on the dials
        foot1 = grey_chip("Answers: exercises.md", size=22)
        foot2 = grey_chip("Study guide + every command: MLOps_Learning · guides/L13-training-workflows.md")
        nxt_l14 = label("L14 · serving containers, serverless", 22, INK)
        nxt_l15 = label("L15 · save this model, chain the steps in Pipelines", 22, INK)
        nxt_sub = label("(slide 21's third entry)", 20, S.GREY)
        nxt_body = VGroup(label("Next", 22, S.GREY), nxt_l14, nxt_l15, nxt_sub)
        nxt_body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        nxt_sub.shift(RIGHT * 0.9 + UP * 0.06)
        nxt_fr = outline_box(nxt_body.width + 0.6, nxt_body.height + 0.5, FUTURE, solid=False)
        nxt_fr.move_to([2.05, 1.2, 0])
        nxt_body.move_to(nxt_fr)
        nxt = VGroup(nxt_fr, nxt_body)
        assert nxt.get_left()[0] > -2.45 and nxt.get_right()[0] < 6.5, (nxt.get_left(), nxt.get_right())
        foots = VGroup(foot1, foot2).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        foots.move_to([0, -2.55, 0])
        assert foots.get_left()[0] > -6.5 and foots.get_right()[0] < 6.5 and foot2.width < 13, foots.width
        dials = [lever_dial(a, b) for a, b in LEVERS]
        for d, x in zip(dials, (-4.6, -0.55, 3.5)):
            d.move_to([x, 0.2, 0])
        for d in dials[:2]:
            dim_dial(d)
        third = dials[2]
        piv = third.pivot.get_center()
        ledger = ledger_icon().move_to([5.75, 1.15, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(cur, shift=LEFT * 0.6), FadeIn(items[4], shift=LEFT * 0.4), run_time=0.6)
            self.remove(cur)
            self.play(FadeIn(foot1, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(foot2, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Next, lecture 14")
            self.play(FadeIn(nxt, shift=LEFT * 0.2), run_time=0.7)
            self.play(Indicate(nxt_l14, color=INK, scale_factor=1.05), run_time=0.6)
            vo.wait_until("and lecture 15 saves this model")
            self.play(Indicate(nxt_l15, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Hardware rented")
            self.keep_only(ref, run_time=0.6)
            self.play(LaggedStart(*[FadeIn(d, shift=UP * 0.2) for d in dials], lag_ratio=0.2), run_time=0.8)
            self.play(Rotate(third.needle, angle=-0.62 * PI, about_point=piv),
                      third.needle.animate.set_color(TURN), third.pivot.animate.set_color(TURN),
                      third.arc.animate.set_stroke(TURN, 6), third.ticks.animate.set_color(TURN),
                      third.title.animate.set_color(TURN), run_time=0.9)
            vo.wait_until("and a log of what you rented it for")
            self.play(FadeIn(ledger, scale=0.6, shift=LEFT * 0.2), run_time=0.6)
            self.play(Wiggle(ledger[:3], scale_value=1.08), run_time=0.8)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
