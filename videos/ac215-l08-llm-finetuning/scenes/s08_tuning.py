"""S08 · Hand it to Google: the tuning job (README "Fine-tune › Run Container" and "Fine-tune ›
Fine-tune Model"). Lecture: 13–16 (one beat, block 7).

Beats (script.md "## S08", one voiceover block each):
 0  TRACKER FtRun (no step yet, then 1). Full-width TEAL terminal at app@6f5113cdb660:/app$: `exit`
    -> laptop/07 line 28; the frame turns GREY (`laptop`, prompt …/dataset-creator$). `docker ps -a`
    (extra) -> laptop/14 line 2 (the header only). `cd ../gemini-finetuner && pwd && ls` (extra form
    of README.md:236) -> laptop/17 lines 2–8; the prompt becomes …/gemini-finetuner$.
 1  TRACKER FtRun 1 · extra. The terminal shrinks to a 3-row strip: `grep -n 'gs://' cli.py` (extra)
    -> gemini-finetuner/04 lines 2–3 (cut at the row; the panel above shows them whole). Above it
    CODE(gemini-finetuner/cli.py: 9–11, 13–15 folded): `gs://cheese-dataset` on lines 10–11 YELLOW,
    the GREY `erratum` tag "the course's bucket · # Replace with your dataset"; a YELLOW chip
    `gs://<your-bucket>` slides over each. The panel gives way to V2 (laptop, gemini-finetuner,
    their PINK mounts): `gemini-finetuner/ -> /app` pulses, note "files in the folder: live inside
    · no rebuild" and "env.dev is different: read at start".
 2  TRACKER FtRun 2. Full terminal: `sh docker-shell.sh` + `▶ your turn` -> laptop/18 lines 3,
    12–16, …, 21 (BuildKit spaces collapsed, times as GREY tags); "Building 0.0s" lights, each
    `CACHED` GREEN; line 27 cut before " exit" is the new prompt: the frame turns TEAL
    (`container · gemini-finetuner`). The terminal shrinks to a strip (the uv sync row, the COPY
    row, the prompt); above it the extra card "are the two folders built the same way?" with
    laptop/16 lines 2–4 as a GREEN chip row.
 3  TRACKER FtRun 3. Full terminal: `python cli.py --help` -> gemini-finetuner/01 lines 2–9;
    `--train` and `--chat` light. The terminal shrinks to a strip (the three option rows); above it
    CODE(cli.py: 12–14, 19–23 folded) left and a small BLUE "Google Cloud" with V2's three pins
    right: global (dim, the teacher), us-central1 lights with train_client; the window Transforms
    into CODE(cli.py: 26–32) and `us` lights with chat_client, its base_url PINK with a PINK route
    to the pin.
 4  The strip and the cloud leave. CODE(cli.py: 44, 48–49, 52–55, 61–62 folded; 56 the display
    name and 63–65 not shown): 48–49 PINK (the gs:// datasets), 53 `epoch_count=1`, 55
    `adapter_size="ADAPTER_SIZE_FOUR"` YELLOW + the GREY hedge chip "by our reading: Google's
    managed small-adapter idea · see part 2", 61–62 YELLOW.
 5  TRACKER FtModel 1. Full TEAL terminal (tags no key · billed): `python cli.py --train` ->
    gemini-finetuner/02 lines 2–5, …, 69 (wrapped): line 4 GREY with the tag "harmless". The
    terminal shrinks to a strip; V2 above it with the route from gemini-finetuner toward
    us-central1 (GREY dashed: where it would go); at "the missing key" line 69 prints RED in the
    strip as the route stops at the wall with the RED "no key" stamp.
 6  The stage leaves. GREY dashed "with your key, look for" card: excerpt chips cli.py lines 67,
    68 (note "…/locations/us-central1/tuningJobs/…"), 89 (note "→ None after a minute"), and a RED
    chip "403? → your bucket in cli.py lines 10–11 · both roles · API enabled". Then CODE(cli.py:
    125–126) with `wait_for_job=False` YELLOW and the GREY note "waits 60 s, then leaves · never
    waits for the job to finish (lines 71–72)", and the dry-cleaner glyph (illustration): a
    garment goes over the counter, a ticket comes back. Then the "your turn" card (cli.py lines
    10–11 → your bucket · sh docker-shell.sh · python cli.py --train; GOLD "tuning: billed per
    training token · the README's table comes next"). 2 s hold.
 7  LECTURE 13–16. The strip leaves; V2 returns (laptop, gemini-finetuner, cloud, pins): a GREY
    dashed miniature memory column "GPU memory · part 2" (concept · lecture only, no numbers)
    appears on the laptop, then slides across to the us-central1 pin and settles. TRACKER
    FtModel 2: a schematic job page along the bottom (illustration, no logos; address
    console.cloud.google.com/agent-platform/tuning/managed, README.md:261): status Running →
    Succeeded, rows "tuned model" and "endpoint: projects/…/locations/us/endpoints/…" (GREY
    placeholders); V2's PINK arrow runs from the bucket straight into the job.
 8  The lecture tag leaves; the job page shrinks into a small page in the cloud; the stage dims;
    the ponder card enters (8 s).
 9  The ponder card leaves, the stage comes back: the TEAL container and its mounts fade out
    entirely (--rm); the job at us-central1 and the bucket arrow stay, the job page stays; caption
    "the container only submitted the job". Everything fades to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    Dot,
    DashedVMobject,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    ShowPassingFlash,
    Transform,
    VGroup,
    VMobject,
)

from common import *  # noqa: F401,F403
from common import _with_header
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S08"]

# ------------------------------------------------------------------ the real captures and sources
GF = "gemini-finetuner/cli.py"
DCSH = capture("laptop/07")
assert DCSH.line(27) == P_CTR_DC + " exit" and DCSH.line(28) == "exit", (DCSH.line(27), DCSH.line(28))
EXIT_CMD = "exit"
PS = capture("laptop/14")
assert PS.cmd == "docker ps -a" and PS.line(2).startswith("CONTAINER ID"), PS.cmd
CDG = capture("laptop/17")
assert CDG.cmd == "cd ../gemini-finetuner && pwd && ls", CDG.cmd
assert CDG.line(2) == "/home/student/AC215/llm-finetuning/gemini-finetuner", CDG.line(2)
URIS = capture("gemini-finetuner/04")
assert URIS.cmd == "grep -n 'gs://' cli.py" and URIS.line(2).startswith("10:TRAIN_DATASET"), URIS.cmd
GFSH = capture("laptop/18")
assert GFSH.cmd == "sh docker-shell.sh", GFSH.cmd
assert GFSH.cut_before(27, " exit") == P_CTR_GF, GFSH.line(27)
assert "Building 0.0s" in GFSH.line(3) and all("CACHED" in GFSH.line(n) for n in (12, 13, 14, 15))
assert "uv sync" in GFSH.line(15) and "[6/6] COPY" in GFSH.line(16), GFSH.line(15)
DIFF = capture("laptop/16")
assert [DIFF.line(n) for n in (2, 3, 4)] == ["uv.lock: identical", "pyproject.toml: identical",
                                              "Dockerfile: identical"]
HELP = capture("gemini-finetuner/01")
assert HELP.cmd == "python cli.py --help" and "[--train] [--chat]" in HELP.line(2), HELP.cmd
TRAIN = capture("gemini-finetuner/02")
assert TRAIN.cmd == "python cli.py --train" and TRAIN.exit == 1, TRAIN.cmd
assert "ExperimentalWarning" in TRAIN.line(4) and "was not found." in TRAIN.line(69), TRAIN.line(69)
L67, L68, L89 = (source_line(GF, n) for n in (67, 68, 89))
assert "gs://cheese-dataset" in source_line(GF, 10) and "gs://cheese-dataset" in source_line(GF, 11)
assert 'adapter_size="ADAPTER_SIZE_FOUR"' in source_line(GF, 55) and "epoch_count=1" in source_line(GF, 53)
assert "wait_for_job=False" in source_line(GF, 126) and "time.sleep(60)" in source_line(GF, 71)
assert 'base_url="https://aiplatform.us.rep.googleapis.com"' in source_line(GF, 31)
README_261 = source_line("README.md", 261)
CONSOLE_URL = "console.cloud.google.com/agent-platform/tuning/managed"
assert CONSOLE_URL in README_261, README_261

# ------------------------------------------------------------------ layout
TOP_Y = 2.86                     # top of a panel under the tracker
SAFE_R = 6.45


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    """Move m so the given edge / centre coordinate is where asked."""
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if cx is not None:
        m.set_x(cx)
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def flash(mob, color: str = TURN, k: float = 1.15):
    return Indicate(mob, color=color, scale_factor=k)


def pin_row(p, dim: bool = False):
    """A copy of one of V2's cloud pins (dot, mono location, BLUE role)."""
    c = p.copy()
    for m in c.get_family():
        m.set_opacity(0.4 if dim else 1)
    return c


def mini_cloud(stage) -> VGroup:
    """V2's three location pins (global · us-central1 · us) in a narrow BLUE "Google Cloud" box
    for beat 3 (the stage's own cloud is 4.5 wide; the code panel needs the rest). .pins .frame"""
    pins = {k: pin_row(stage.pins[k], dim=(k == "pin_global")) for k in ("pin_global", "pin_tune", "pin_us")}
    col = VGroup(*pins.values()).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
    fr = box(3.0, 4.1, CLOUD, fill_opacity=0.05, radius=0.3)
    ttl = label("Google Cloud", CAPTION, CLOUD)
    ttl.move_to(fr.get_corner(UP + LEFT), aligned_edge=UP + LEFT).shift(np.array([0.2, -0.12, 0]))
    col.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.25 + DOWN * 0.2)
    g = VGroup(fr, ttl, col)
    g.frame, g.pins = fr, pins
    return g


def ghost_route(stg, cmd: str) -> VMobject:
    """The route `cmd` would take with a key: a GREY dashed path (the PINK one stops at the wall)."""
    a = stg.route(cmd)
    return DashedVMobject(a, num_dashes=24, dashed_ratio=0.5).set_stroke(S.GREY, 2.5, opacity=0.7)


def look_card() -> VGroup:
    """The GREY dashed "with your key, look for" card: three excerpt chips (cli.py 67, 68, 89) with
    GREY notes. .frame .title .items"""
    e67 = excerpt_chip("Training job started. Monitoring progress...", f"{GF} · line 67 (excerpt)", line=L67)
    e68 = excerpt_chip("Job name: {tuning_job.name}", f"{GF} · line 68 (excerpt)", line=L68)
    n68 = note("…/locations/us-central1/tuningJobs/…")
    e89 = excerpt_chip("Tuned model info: {tuning_job.tuned_model}", f"{GF} · line 89 (excerpt)", line=L89)
    n89 = note("→ None after a minute")
    r68 = VGroup(e68, n68)
    n68.next_to(e68.chip, RIGHT, buff=0.3)
    r89 = VGroup(e89, n89)
    n89.next_to(e89.chip, RIGHT, buff=0.3)
    items = VGroup(VGroup(e67), r68, r89).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    ttl = label("with your key, look for", CAPTION, S.GREY)
    body = VGroup(ttl, items).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
    fr = box(body.width + 0.7, body.height + 0.28, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14, dashed=True)
    body.move_to(fr)
    g = VGroup(fr, body)
    g.frame, g.title, g.items = fr, ttl, items
    return g


def shirt(color: str = OWN, w: float = 0.7) -> VMobject:
    """A garment outline (the job you hand in)."""
    pts = [(-0.5, 0.5), (-0.2, 0.62), (0.0, 0.5), (0.2, 0.62), (0.5, 0.5), (0.75, 0.15), (0.5, 0.02),
           (0.42, 0.18), (0.42, -0.6), (-0.42, -0.6), (-0.42, 0.18), (-0.5, 0.02), (-0.75, 0.15)]
    s = Polygon(*[np.array([x, y, 0]) for x, y in pts], stroke_color=color, stroke_width=3).set_fill(color, 0.3)
    return s.scale_to_fit_width(w)


def dry_cleaner() -> VGroup:
    """The dry-cleaner illustration: the TEAL container (you) left, a counter, BLUE Google right; a
    garment (the job) goes over the counter, a ticket (the job name) comes back.
    .you .google .counter .garment .ticket .ticket_home"""
    yf = box(1.9, 0.8, CTR, fill_opacity=0.14, radius=0.12, stroke=3)
    you = VGroup(yf, mono("--train", CAPTION, CTR).move_to(yf))
    goo = model_box("Google", w=1.9, h=0.8, color=CLOUD)
    you.move_to([-3.4, 0, 0])
    goo.move_to([3.4, 0, 0])
    counter = VGroup(Line([-1.0, -0.4, 0], [1.0, -0.4, 0], color=S.GREY, stroke_width=5),
                     Line([0, -0.4, 0], [0, -0.8, 0], color=S.GREY, stroke_width=4))
    ctr_lab = label("counter", CAPTION, S.GREY).next_to(counter, DOWN, buff=0.08)
    garment = shirt().next_to(you, RIGHT, buff=0.25).shift(UP * 0.35)
    tk = RoundedRectangle(width=1.5, height=0.42, corner_radius=0.05, stroke_color=S.GREY, stroke_width=2.5)
    tk.set_fill(S.BG, 1)
    tk_t = label("job name", CAPTION, INK).move_to(tk)
    ticket = VGroup(tk, tk_t).next_to(goo, LEFT, buff=0.25).shift(DOWN * 0.12)
    g = VGroup(you, goo, counter, ctr_lab)
    g.you, g.google, g.counter, g.garment, g.ticket = you, goo, counter, garment, ticket
    g.ticket_home = Dot(you.get_right() + RIGHT * (0.25 + tk.width / 2) + DOWN * 0.12, radius=0.01).set_opacity(0)
    g.garment_home = Dot(goo.get_left() + LEFT * (0.25 + garment.width / 2) + UP * 0.6, radius=0.01).set_opacity(0)
    g.add(g.ticket_home, g.garment_home)
    return g


def job_page(width: float = TERM_W, height: float = 2.2) -> VGroup:
    """The schematic tuning-job page (illustration, no logos): the README's console address
    (README.md:261), "Agent Platform › Tuning" with its status chip, the tuned model and endpoint
    rows (GREY placeholders). .window .head .status .status_ok .rows .tag"""
    w = browser_window(CONSOLE_URL, width=width, height=height)
    head = label("Agent Platform › Tuning", CAPTION, INK)
    st = chip("Running", S.GREY, size=CAPTION)
    ok = chip("Succeeded", CLOUD, size=CAPTION)
    top = VGroup(head, st).arrange(RIGHT, buff=0.4)
    r1 = VGroup(label("tuned model:", CAPTION, S.GREY), mono("…", CAPTION, S.GREY)).arrange(RIGHT, buff=0.2)
    r2 = VGroup(label("endpoint:", CAPTION, S.GREY),
                mono("projects/…/locations/us/endpoints/…", CAPTION, S.GREY)).arrange(RIGHT, buff=0.2)
    rows = VGroup(r1, r2).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    body = VGroup(top, rows).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    content = w.content
    body.move_to(content).align_to(content, LEFT).shift(RIGHT * 0.3)
    ok.move_to(st).align_to(st, LEFT)
    tg = illustration_tag("README.md:261")
    tg.move_to(content).align_to(content, RIGHT).shift(LEFT * 0.15).set_y(top.get_center()[1])
    assert tg.get_left()[0] > ok.get_right()[0] + 0.3, (tg.get_left(), ok.get_right())
    assert body.get_bottom()[1] > w.frame.get_bottom()[1] + 0.08, (body.get_bottom(), w.frame.get_bottom())
    g = VGroup(w, head, st, rows, tg)
    g.window, g.status, g.status_ok, g.rows, g.tag, g.head = w, st, ok, rows, tg, head
    return g


def mini_page() -> VGroup:
    """The job page, shrunk: a small page frame in the cloud holding its status chip."""
    ok = chip("Succeeded", CLOUD, size=CAPTION)
    fr = RoundedRectangle(width=ok.width + 0.3, height=ok.height + 0.38, corner_radius=0.08,
                          stroke_color=S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1)
    bar = Line(fr.get_corner(UP + LEFT) + DOWN * 0.18, fr.get_corner(UP + RIGHT) + DOWN * 0.18,
               color=S.GREY_DARK, stroke_width=2)
    ok.move_to(fr).shift(DOWN * 0.08)
    g = VGroup(fr, bar, ok)
    g.frame, g.status = fr, ok
    return g


def mini_column(w: float = 0.5, k: float = 0.009) -> VGroup:
    """V5 preview: a GREY dashed miniature of the memory column (the lecture's 20 / 20 / 80 GB
    proportions, no numbers). .blocks"""
    blocks = VGroup()
    y = 0.0
    for gb in (20, 20, 80):
        h = gb * k
        r = DashedVMobject(Rectangle(width=w, height=h - 0.03), num_dashes=max(10, int((w + h) * 9)),
                           dashed_ratio=0.55).set_stroke(FUTURE, 2.5)
        r.move_to([0, y + h / 2, 0])
        blocks.add(r)
        y += h
    bg = Rectangle(width=w, height=y, stroke_width=0).set_fill(S.BG, 0.9).move_to([0, y / 2, 0])
    g = VGroup(bg, blocks)
    g.blocks = blocks
    return g


def over_span(sp, text: str, pitch: float) -> VGroup:
    """`text` (YELLOW mono, the code's size) on an opaque patch exactly over the glyphs `sp` (the
    value you type over the course's): a template edit, drawn where the old text was. The patch is
    0.9 of a code row (`pitch`) tall, centred on the row, so it never touches the wrapped row below."""
    t = mono(text, 20, TURN)
    h = max(pitch * 0.9, t.height + 0.01)
    patch = Rectangle(width=max(sp.width, t.width) + 0.12, height=h, stroke_color=TURN,
                      stroke_width=1.5).set_fill(PANEL, 1)
    patch.move_to(sp).align_to(sp, LEFT).shift(LEFT * 0.06)
    t.move_to(patch).align_to(sp, LEFT)
    g = VGroup(patch, t)
    return g


def hedge_card(rows) -> VGroup:
    """A small GREY card of serif rows (a hedge: our reading, not the docs)."""
    body = VGroup(*[label(r, CAPTION, S.GREY) for r in rows]).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
    fr = box(body.width + 0.4, body.height + 0.3, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
    body.move_to(fr)
    return VGroup(fr, body)


class TuningJob(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, len(SAY)

        # ========================================================== 0 · exit, docker ps -a, cd ../gemini-finetuner
        tr = tracker("FtRun", None)
        t = term(P_CTR_DC, rows=12, container="dc")
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("Type exit")
            type_cmd(self, t, EXIT_CMD, 0.3)
            show(self, t, DCSH, 28, run_time=0.3)
            anims = leave_container(t, P_DC)
            bare_prompt(self, t)
            self.play(*anims, run_time=0.6)
            vo.wait_until("and an extra docker ps")
            ps = type_cmd(self, t, PS.cmd, 0.5)
            pin(self, ps, beside(extra_tag(), t, ps), run_time=0.3)
            hdr = show(self, t, PS, 2, run_time=0.3)[0]
            vo.wait_until("shows nothing left")
            self.play(flash(hdr, S.GREY, 1.04), run_time=0.6)
            vo.wait_until("Step 1")
            self.play(tr.goto(1), run_time=0.5)
            cdl = type_cmd(self, t, CDG.cmd, 0.6)
            pin(self, cdl, beside(extra_tag(), t, cdl), run_time=0.3)
            out0 = show(self, t, CDG, (2, 8), run_time=0.6)
            self.play(out0[0].animate.set_color(LAPTOP), run_time=0.3)
            cd_prompt(self, t, P_GF, run_time=0.7)

        # ========================================================== 1 · extra: lines 10-11 point at the course bucket
        p1 = src_panel(GF, [(9, 11), (13, 15)], size=20,
                       wrap={10: ['train.jsonl"'], 11: ['test.jsonl"']})
        place(p1, left=-6.45, top=TOP_Y)
        assert p1.get_bottom()[1] > STRIP_TOP + 0.05, p1.get_bottom()
        err1 = erratum_tag("the course's bucket · # Replace with your dataset")
        place(err1, right=p1.get_right()[0], top=p1.get_bottom()[1] - 0.04)
        assert err1.get_bottom()[1] > STRIP_TOP + 0.02, err1.get_bottom()
        sp10, sp11 = p1.span(10, "gs://cheese-dataset"), p1.span(11, "gs://cheese-dataset")
        pitch1 = sp10.get_center()[1] - p1.span(10, 'train.jsonl"').get_center()[1]   # one code row
        mine = [over_span(sp, BUCKET_TEMPLATE, pitch1) for sp in (sp10, sp11)]
        for m, n in zip(mine, (10, 11)):
            wrapped = p1.span(n, 'train.jsonl"' if n == 10 else 'test.jsonl"')
            assert m.get_bottom()[1] > wrapped.get_top()[1] + 0.01, (n, m.get_bottom(), wrapped.get_top())
            assert m.get_left()[0] < p1.span(n, "gs://cheese-dataset").get_left()[0], n
        start_spot = np.array([3.6, -0.9, 0])
        stg1 = Stage(show=("laptop", "gf", "mounts_gf"))
        live = VGroup(VGroup(label("files in the folder:", CAPTION, INK),
                             label("live inside · no rebuild", CAPTION, INK)).arrange(DOWN, buff=0.1, aligned_edge=LEFT),
                      VGroup(label("env.dev is different:", CAPTION, S.GREY),
                             label("read at start", CAPTION, S.GREY)).arrange(DOWN, buff=0.1, aligned_edge=LEFT))
        live.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        place(live, left=stg1.boxes["gf"].frame.get_right()[0] + 0.35, cy=stg1.boxes["gf"].frame.get_center()[1])
        assert live.get_right()[0] < SAFE_R, live.get_right()
        with self.voiceover(SAY[1]) as vo:
            resize(self, t, 3, keep=1, run_time=0.6)
            self.play(caption_extra(tr), run_time=0.4)
            g1 = type_cmd(self, t, URIS.cmd, 0.5)
            show(self, t, URIS, 2, 3, run_time=0.4)
            vo.wait_until("lines 10 and 11")
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.6)
            b10, b11 = p1.bar(10, TURN), p1.bar(11, TURN)
            self.play(FadeIn(b10), FadeIn(b11), run_time=0.4)
            vo.wait_until("the course bucket")
            self.play(sp10.animate.set_color(TURN), sp11.animate.set_color(TURN), FadeIn(err1, shift=UP * 0.1),
                      run_time=0.6)
            vo.wait_until("Point them at your own")
            for c in mine:
                c.save_state()
                c.move_to(start_spot)
                c.set_opacity(0)
            self.play(*[c.animate.restore() for c in mine], run_time=0.9)
            self.play(flash(VGroup(*mine), TURN, 1.08), run_time=0.5)
            vo.wait_until("The folder is mounted")
            self.play(FadeOut(VGroup(p1, b10, b11, err1, *mine)), run_time=0.5)
            self.play(FadeIn(stg1), run_time=0.6)
            m_app = stg1.parts["mounts_gf"][0]
            self.play(ShowPassingFlash(m_app.copy().set_stroke(TURN, 7), time_width=0.6),
                      flash(stg1.row("gf"), LOOKUP, 1.1), run_time=0.8)
            vo.wait_until("so there's no need")
            self.play(FadeIn(live[0], shift=LEFT * 0.1), flash(stg1.boxes["gf"].app, LOOKUP, 1.2), run_time=0.6)
            self.play(FadeIn(live[1], shift=LEFT * 0.1), flash(stg1.row("env"), S.GREY, 1.1), run_time=0.6)

        # ========================================================== 2 · step 2: sh docker-shell.sh (all cached)
        xc = extra_card("are the two folders built the same way?")
        chips2 = VGroup(*[chip(DIFF.line(n), OWN, size=CAPTION, font=MONO) for n in (2, 3, 4)])
        chips2.arrange(RIGHT, buff=0.3)
        stack2 = VGroup(xc, chips2).arrange(DOWN, buff=0.45)
        place(stack2, cx=0, cy=(STRIP_TOP + TOP_Y) / 2 - 0.1)
        assert chips2.width < 12.8 and stack2.get_bottom()[1] > STRIP_TOP + 0.1, (chips2.width, stack2.get_bottom())
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(stg1, live)), caption_extra(tr, on=False), run_time=0.5)
            resize(self, t, 12, run_time=0.6)
            self.play(tr.goto(2), run_time=0.5)
            sh = type_cmd(self, t, GFSH.cmd, 0.5)
            pin(self, sh, beside(your_turn(), t, sh), run_time=0.4)
            vo.wait_until("It's instant")
            out2 = print_build(self, t, [GFSH.cut(3, "FINISHED"), GFSH.squeeze(12), GFSH.squeeze(13),
                                         GFSH.squeeze(14), GFSH.squeeze(15), GFSH.squeeze(16), "…",
                                         GFSH.line(21)], run_time=1.0)
            r3, r15, r16 = out2[0], out2[4], out2[5]
            b00 = substring(r3, "Building 0.0s")
            self.play(b00.animate.set_color(TURN), run_time=0.3)
            self.play(flash(b00, TURN, 1.15), run_time=0.5)
            vo.wait_until("every layer up to uv sync")
            self.play(*[substring(out2[k], "CACHED").animate.set_color(OWN) for k in (1, 2, 3, 4)], run_time=0.6)
            self.play(flash(substring(r15, "uv sync"), OWN, 1.2), run_time=0.5)
            anims = enter_container(t, "gf")
            pr2 = bare_prompt(self, t)
            self.play(*anims, run_time=0.6)
            vo.wait_until("because both folders share")
            resize(self, t, 3, keep=[r15, r16, pr2], run_time=0.6)
            self.play(FadeIn(xc, shift=DOWN * 0.1), caption_extra(tr), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips2], lag_ratio=0.3), run_time=0.9)
        self.wait(1.0)          # the three "identical" chips stay up past the sentence

        # ========================================================== 3 · step 3: --help; the three locations
        cl = mini_cloud(Stage())
        place(cl, right=SAFE_R, top=TOP_Y)
        assert cl.get_bottom()[1] > STRIP_TOP + 0.05, cl.get_bottom()
        w1 = src_panel(GF, [(12, 14), (19, 23)], size=20, wrap={12: ["serve on"]})
        _with_header(w1, f"{GF} · lines 12–23 (folded)")     # the GREY ↪ shows the wrap of line 12
        w2 = src_panel(GF, 26, 32, size=20, wrap={31: ['"https']})
        for w in (w1, w2):
            place(w, left=-6.45, top=TOP_Y)
            assert w.get_right()[0] < cl.get_left()[0] - 0.12, (w.get_right(), cl.get_left())
            assert w.get_bottom()[1] > STRIP_TOP + 0.05, w.get_bottom()
        url = w2.span(31, '"https://aiplatform.us.rep.googleapis.com"')
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(xc, chips2)), caption_extra(tr, on=False), run_time=0.4)
            resize(self, t, 12, run_time=0.6)
            self.play(tr.goto(3), run_time=0.5)
            hl = type_cmd(self, t, HELP.cmd, 0.5)
            pin(self, hl, beside(your_turn(), t, hl), run_time=0.4)
            out3 = show(self, t, HELP, (2, 9), run_time=0.6)
            vo.wait_until("two flags")
            r8, r9 = out3[6], out3[7]
            self.play(substring(r8, "--train").animate.set_color(TURN),
                      substring(r9, "--chat").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("The train client")
            resize(self, t, 3, keep=[out3[5], r8, r9], run_time=0.6)
            self.play(FadeIn(w1, shift=UP * 0.15), FadeIn(cl.frame), FadeIn(cl[1]), FadeIn(cl.pins["pin_global"]),
                      run_time=0.6)
            b19 = VGroup(w1.bar(13, TURN), w1.bar(19, TURN), w1.bar(22, TURN))
            self.play(FadeIn(b19), run_time=0.4)
            vo.wait_until("in us-central1")
            self.play(FadeIn(cl.pins["pin_tune"], shift=LEFT * 0.1), run_time=0.4)
            self.play(flash(cl.pins["pin_tune"].where, TURN, 1.2), flash(w1.span(13, '"us-central1"'), TURN, 1.1),
                      run_time=0.6)
            vo.wait_until("The chat client")
            self.play(FadeOut(b19), run_time=0.2)
            body1 = VGroup(*[m for m in w1.submobjects if m is not w1.header])
            body2 = VGroup(*[m for m in w2.submobjects if m is not w2.header])
            self.play(FadeOut(w1.header, run_time=0.3), Transform(body1, body2, run_time=0.8),
                      FadeIn(w2.header, run_time=0.8, rate_func=lambda x: max(0.0, (x - 0.6) / 0.4)))
            self.remove(body1, w1)
            self.add(w2)
            b26 = VGroup(w2.bar(26, TURN), w2.bar(29, TURN))
            self.play(FadeIn(b26), run_time=0.3)
            vo.wait_until("in the multi-region")
            self.play(FadeIn(cl.pins["pin_us"], shift=LEFT * 0.1), run_time=0.4)
            self.play(flash(cl.pins["pin_us"].where, TURN, 1.3), run_time=0.5)
            vo.wait_until("at its own address")
            route = _route_arrow(url, cl.pins["pin_us"].dot, x0=w2.get_right()[0] + 0.04)
            b31 = w2.bar(31, LOOKUP)
            self.play(url.animate.set_color(LOOKUP), FadeIn(b31), run_time=0.4)
            self.play(GrowArrow(route), run_time=0.6)

        # ========================================================== 4 · train(): datasets, epoch, adapter size, tune()
        p4 = src_panel(GF, [44, (48, 49), (52, 55), (61, 62)], size=20)
        place(p4, cx=0, top=TOP_Y)
        hedge = hedge_card(["by our reading: Google's managed", "small-adapter idea · see part 2"])
        a55 = p4.span(55, '"ADAPTER_SIZE_FOUR",')
        place(hedge, right=p4.get_right()[0] - 0.15, cy=a55.get_center()[1])
        ends = [p4.span(n, sub).get_right()[0] for n, sub in ((53, "epoch_count=1,"), (54, "multiplier=1.0,"),
                                                              (61, "tune("), (62, "MODEL,"))]
        assert hedge.get_left()[0] > max(ends + [a55.get_right()[0]]) + 0.4, (hedge.get_left(), ends)
        assert hedge.get_top()[1] < p4.span(52, "CreateTuningJobConfig(").get_bottom()[1] - 0.05, hedge.get_top()
        assert hedge.get_bottom()[1] > p4.get_bottom()[1] + 0.1, hedge.get_bottom()
        lead = Line(a55.get_right() + RIGHT * 0.12, [hedge.get_left()[0] - 0.05, a55.get_center()[1], 0],
                    color=S.GREY, stroke_width=2)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(t, w2, b26, b31, route, cl)), run_time=0.6)
            self.play(FadeIn(p4, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("wraps your bucket files")
            b48 = VGroup(p4.bar(48, LOOKUP), p4.bar(49, LOOKUP))
            self.play(FadeIn(b48), p4.span(48, "gcs_uri=TRAIN_DATASET").animate.set_color(LOOKUP),
                      p4.span(49, "gcs_uri=VALIDATION_DATASET").animate.set_color(LOOKUP), run_time=0.6)
            vo.wait_until("and asks for one epoch")
            b53 = p4.bar(53, TURN)
            self.play(FadeIn(b53), p4.span(53, "epoch_count=1").animate.set_color(TURN), run_time=0.5)
            vo.wait_until("and an adapter of size four")
            b55 = p4.bar(55, TURN)
            self.play(FadeIn(b55), p4.span(55, 'adapter_size="ADAPTER_SIZE_FOUR"').animate.set_color(TURN),
                      run_time=0.5)
            vo.wait_until("By our reading")
            self.play(Create(lead), FadeIn(hedge, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("the idea you'll build")
            self.play(flash(hedge, S.GREY, 1.06), run_time=0.6)
            vo.wait_until("One call starts")
            b61 = VGroup(p4.bar(61, TURN), p4.bar(62, TURN))
            self.play(FadeIn(b61), p4.span(61, "train_client.tunings.tune(").animate.set_color(TURN), run_time=0.5)
            self.play(flash(p4.span(61, "train_client.tunings.tune("), TURN, 1.08), run_time=0.6)

        # ========================================================== 5 · --train: the warning, the missing key
        t5 = term(P_CTR_GF, rows=12, container="gf")
        tags5 = frame_tags(t5, nokey_tag(), billed_tag())
        stg5 = Stage(show=("laptop", "key", "gf", "mounts_gf", "cloud", "pin_global", "pin_bucket", "pin_tune",
                           "pin_us"))
        blk = stg5.blocked("--train")
        ghost5 = ghost_route(stg5, "--train")
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p4, b48, b53, b55, b61, hedge, lead)), run_time=0.5)
            tr = switch_section(self, tr, "FtModel", 1)
            self.play(FadeIn(t5, shift=UP * 0.2), FadeIn(tags5, shift=UP * 0.2), run_time=0.5)
            bare_prompt(self, t5)
            vo.wait_until("python cli.py dash dash train")
            tc5 = type_cmd(self, t5, TRAIN.cmd, 0.5)
            show(self, t5, TRAIN, 2, 3, run_time=0.4)
            r4 = t5.print(self, [(TRAIN.line(4), S.GREY)], wrap=True, run_time=0.4)
            show(self, t5, TRAIN, 5, "…", run_time=0.4)
            vo.wait_until("The experimental warning")
            hm = harmless_tag()
            beside(hm, t5, r4[-1], buff=0.4)
            pin(self, r4[-1], hm, run_time=0.4)
            self.play(flash(wrapped_glyphs(r4, "ExperimentalWarning"), S.GREY, 1.08), run_time=0.6)
            # the strip and the stage arrive before the error, so the error line, the stub and the
            # "no key" stamp land on "Then the missing key" together
            resize(self, t5, 3, keep=[tc5], run_time=0.6,
                   extra=[tags5.animate.set_y(STRIP_TOP - t5.bar_h / 2)])
            self.play(FadeIn(stg5), Create(ghost5), run_time=0.6)
            vo.wait_until("Then the missing key")
            r69 = t5.print(self, [(TRAIN.line(69), ERR)], wrap=True, run_time=0.4)
            self.play(flash(wrapped_glyphs(r69, "was not found."), ERR, 1.12), Create(blk.stub), run_time=0.6)
            self.play(FadeIn(blk.stamp, scale=1.3), run_time=0.4)
            vo.wait_until("no job was created")
            self.play(flash(stg5.pins["pin_tune"], S.GREY, 1.06), flash(blk.stamp, ERR, 1.1), run_time=0.7)

        # ========================================================== 6 · with a key, look for …; wait_for_job=False; your turn
        look = look_card()
        e403 = chip("403? → your bucket in cli.py lines 10–11 · both roles · API enabled", ERR, size=CAPTION)
        place(look, cx=0, top=TOP_Y + 0.06)
        place(e403, cx=0, top=look.get_bottom()[1] - 0.1)
        assert e403.get_bottom()[1] > STRIP_TOP + 0.05 and look.get_right()[0] < SAFE_R, (e403.get_bottom(), look.width)
        p6 = src_panel(GF, 125, 126, size=20)
        place(p6, cx=-1.6, top=TOP_Y)
        n6 = VGroup(note("waits 60 s, then leaves · never waits for the job to finish"),
                    note(f"{GF} · lines 71–72")).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        place(n6, left=p6.get_right()[0] + 0.35, cy=p6.get_center()[1] - 0.2)
        if n6.get_right()[0] > SAFE_R:
            place(n6, left=p6.get_left()[0], top=p6.get_bottom()[1] - 0.15)
        dc = dry_cleaner()
        ill = illustration_tag()
        dgroup = VGroup(dc, dc.garment, dc.ticket)
        place(dgroup, cx=0, top=min(n6.get_bottom()[1], p6.get_bottom()[1]) - 0.15)
        ill.next_to(dc.google, RIGHT, buff=0.2)
        assert ill.get_right()[0] < SAFE_R, ill.get_right()
        assert dc.get_bottom()[1] > STRIP_TOP + 0.05, dc.get_bottom()
        tc = turn_card([[f"`{GF}`", "lines 10–11 → your bucket"], GFSH.cmd, TRAIN.cmd,
                        (Prose("tuning: billed per training token · the README's table comes next"), COST)])
        place(tc, cx=0, cy=(TOP_Y + STRIP_TOP) / 2 - 0.05)
        assert tc.get_bottom()[1] > STRIP_TOP + 0.05 and tc.get_top()[1] < TOP_Y + 0.05, tc.get_top()
        with self.voiceover(SAY[6]) as vo:
            self.play(flash(stg5.parts["key"], KEY, 1.4), ShowPassingFlash(ghost5.copy().set_stroke(TURN, 5),
                                                                        time_width=0.6), run_time=0.8)
            vo.wait_until("look for")
            self.play(FadeOut(VGroup(stg5, ghost5, blk)), run_time=0.4)
            self.play(FadeIn(look.frame), FadeIn(look.title), run_time=0.3)
            vo.wait_until("training job started")
            self.play(FadeIn(look.items[0], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("a job name in us-central1")
            self.play(FadeIn(look.items[1], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("and after a minute")
            self.play(FadeIn(look.items[2], shift=RIGHT * 0.15), run_time=0.5)
            self.play(FadeIn(e403, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Main calls train")
            self.play(FadeOut(VGroup(look, e403)), run_time=0.4)
            self.play(FadeIn(p6, shift=UP * 0.15), run_time=0.5)
            w126 = p6.span(126, "wait_for_job=False")
            b126 = p6.bar(126, TURN)
            self.play(FadeIn(b126), w126.animate.set_color(TURN), run_time=0.4)
            vo.wait_until("so the command hands in")
            self.play(FadeIn(n6, shift=LEFT * 0.1), run_time=0.5)
            self.play(FadeIn(dc), FadeIn(dc.garment), FadeIn(ill), run_time=0.5)
            self.play(dc.garment.animate.move_to(dc.garment_home.get_center()), run_time=0.9)
            vo.wait_until("like a ticket")
            self.play(FadeIn(dc.ticket, scale=0.8), run_time=0.3)
            self.play(dc.ticket.animate.move_to(dc.ticket_home.get_center()), run_time=0.9)
            vo.wait_until("Read the cost table")
            self.play(FadeOut(VGroup(p6, b126, n6, dc, dc.garment, dc.ticket, ill)), run_time=0.5)
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("then pause")
            self.play(flash(tc.tag, TURN, 1.1), run_time=0.5)
        self.wait(2)

        # ========================================================== 7 · LECTURE 13–16: the GPU bill is Google's; watch the job
        stg7 = Stage(show=("laptop", "key", "gf", "mounts_gf", "cloud", "pin_global", "pin_bucket", "pin_tune",
                           "pin_us"))
        col = mini_column()
        col_lab = VGroup(label("GPU memory · part 2", CAPTION, S.GREY), concept_tag()).arrange(DOWN, buff=0.12)
        lap = stg7.parts["laptop"][0]
        col_lab.arrange(DOWN, buff=0.1)
        VGroup(col, col_lab).arrange(DOWN, buff=0.15).move_to(lap.get_center() + UP * 0.25)
        assert col_lab.get_bottom()[1] > stg7.parts["laptop"][1].get_top()[1] + 0.05, col_lab.get_bottom()
        lap_rows = stg7.parts["laptop"][2]
        key7 = stg7.parts["key"]          # the key glyph sits under the concept tag: dim it with the rows
        col_home = np.array([5.95, -0.2 + col.height / 2, 0])
        assert col_home[0] - col.width / 2 > stg7.pins["pin_bucket"].get_right()[0] + 0.1
        page = job_page()
        place(page, cx=0, bottom=BOTTOM)
        page.status_ok.move_to(page.status).align_to(page.status, LEFT)
        assert page.get_top()[1] < stg7.get_bottom()[1] - 0.04, (page.get_top(), stg7.get_bottom())
        jarr = stg7.job_arrow()
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(tc, t5, tags5)), run_time=0.5)
            lr = lref("13–16")
            self.play(FadeIn(lr), FadeIn(stg7), run_time=0.6)
            vo.wait_until("far more GPU memory")
            key7.save_state()
            # the tree and key go fully out while the column stands over them (0.12 read as garbled text)
            self.play(lap_rows.animate.set_opacity(0), key7.animate.set_opacity(0), FadeIn(col, scale=0.8),
                      FadeIn(col_lab, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("than a laptop has")
            self.play(flash(lap, ERR, 1.03), run_time=0.6)
            vo.wait_until("here that's Google's problem")
            self.play(FadeOut(col_lab), run_time=0.3)
            self.play(col.animate.move_to(col_home), lap_rows.animate.set_opacity(1), key7.animate.restore(),
                      run_time=1.0)
            self.play(flash(stg7.pins["pin_tune"].dot, CLOUD, 1.6), run_time=0.5)
            vo.wait_until("Step 2")
            self.play(tr.goto(2), FadeIn(page.window), FadeIn(page.tag), run_time=0.6)
            self.play(FadeIn(page.head), FadeIn(page.status), Create(jarr), run_time=0.6)
            vo.wait_until("until it says succeeded")
            self.play(ReplacementTransform(page.status, page.status_ok), run_time=0.6)
            vo.wait_until("with a tuned model")
            self.play(FadeIn(page.rows[0], shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("and an endpoint")
            self.play(FadeIn(page.rows[1], shift=RIGHT * 0.1), run_time=0.4)

        # ========================================================== 8 · ponder
        mp = mini_page()
        place(mp, right=6.22, bottom=-1.17)
        assert col_home[1] - col.height / 2 > mp.get_top()[1] + 0.03, (col_home, mp.get_top())
        assert mp.get_right()[0] < stg7.cloud_frame.get_right()[0] - 0.1 and mp.get_bottom()[1] > -1.2, mp.get_corner(DOWN + RIGHT)
        whole_page = VGroup(page.window, page.head, page.status_ok, page.rows, page.tag)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(lr), ReplacementTransform(whole_page, mp), run_time=0.8)
            for m in (col, jarr, mp):
                self.remove(m)
                stg7.add(m)
            self.play(stg7.dim_to(0.3), run_time=0.4)
        card = ponder_at(self, y=-2.45, question="--train returns after about a minute.\nWhere is the training happening, and what would\n"
                               "you lose if you deleted the container right now?", seconds=8)

        # ========================================================== 9 · on Google's hardware; the container only submitted
        cap9 = label("the container only submitted the job", 28, INK)
        place(cap9, cx=0, cy=-2.35)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(card), stg7.undim(), run_time=0.6)
            self.play(flash(stg7.pins["pin_tune"], CLOUD, 1.08), run_time=0.6)
            vo.wait_until("reading your bucket directly")
            self.play(ShowPassingFlash(jarr.copy().set_stroke(TURN, 7), time_width=0.6), run_time=0.9)
            vo.wait_until("Deleting the container")
            self.play(*stg7.parts_out("gf", "mounts_gf"), run_time=1.0)
            vo.wait_until("it only submitted")
            self.play(FadeIn(cap9, shift=UP * 0.1), ShowPassingFlash(mp.frame.copy().set_fill(opacity=0).set_stroke(CLOUD, 5), time_width=0.6), run_time=0.6)
        self.wait(0.6)
        self.play(FadeOut(VGroup(stg7, cap9, tr)), run_time=0.8)
        self.wait(0.3)


def _route_arrow(src, pin_dot, x0: float):
    """A PINK arrow from a code span's row (the base_url), starting at x0 (the panel's edge), to a
    pin's dot."""
    from manim import Arrow
    a = np.array([x0, src.get_center()[1], 0])
    b = pin_dot.get_center() + LEFT * 0.12
    return Arrow(a, b, buff=0, color=LOOKUP, stroke_width=3.5, tip_length=0.18, max_tip_length_to_length_ratio=0.2)
