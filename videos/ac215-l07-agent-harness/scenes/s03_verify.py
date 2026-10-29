"""S03 · Verify offline, and the Colab road (README "Setup › Verify" steps 1-3, "Setup › Model",
"Setup › Notebook path" steps 1-2; the course Colab's setup cells, Colab steps 1-3).
Lecture: none, then 44 (beats 5-7: the lecture links this repo and this Colab).

Beats (script.md "## S03", one voiceover block each):
 0  TRACKER Verify 1. Container terminal (13 rows, TEAL), GREEN title-bar tag "offline · free".
    `python -m scripts.check_sdk` -> container/03 lines 2–11, 12–24 folded to
    `"features": { … },`, …, 29. GREY tag "at the time of recording" on line 3; the versions of
    lines 3 (python), 5 (agent-framework) and 8 (openai) turn GREEN; the folded features row gets
    a GREEN tag "11 features · all true".
 1  TRACKER Verify 2. The terminal clears: `python -m tests` -> container/04 line 2 (wrapped: five
    rows of dots), 3–4, 6; "Ran 281 tests in 99.378s" and OK turn GREEN. The terminal shrinks to
    the strip (the command, Ran, OK); above it (tag illustration) a GREEN ring "the harness" around
    a BLUE dashed seat "scripted model responses" (tag scripted), a PINK HTTPS line to the BLUE
    cloud "OpenAI", which a GREY cross strikes out; chip "no key · no tokens"; top chip README.md ·
    line 127 "does not establish live model quality".
 2  TRACKER Verify 3. The picture leaves, the terminal grows back and clears: `python -m tests
    --show-logs` -> container/05 lines 2 (wrapped), 3 (RED, wrapped), …, 1885–1888. Line 3 flashes,
    GREY tag "deliberate"; line 2's "Ignored an approval response" and "approval occurrence
    identity" get YELLOW underlines, GREY tag "again in act 4"; line 1888 `OK` GREEN, caption
    "trust the last line".
 3  TRACKER Model 1. The terminal clears: `python -c '…'` -> container/06 line 2 `gpt-5.6-luna`. The
    terminal shrinks to the strip; above it CODE(formaggio/config.py: 9): "gpt-5.6-luna" BLUE, GREY
    tag "at the time of recording" under it. A PINK precedence chain writes left to right:
    `--model` › `OPENAI_CHAT_MODEL` › default (GREY "README.md · line 137"); the code's
    OPENAI_CHAT_MODEL and "gpt-5.6-luna" flash with their links; GREY caption under the env link
    "set it inside the container (README.md · line 145)"; GREY dashed chip "a Gemini name doesn't
    switch providers (README.md · line 155)"; the first two links flash YELLOW ("set either").
 4  TRACKER Notebook 1, then 2. The terminal grows back (10 rows, two band rows above it) with
    the chip README.md · line 108 (excerpt) "Run every remaining command inside the container";
    `python -m tests -p test_notebook.py` -> container/07 lines 2–4, 6, then `python -m tests -p
    test_chat_view.py` -> container/08 lines 2–4, 6 (both at "two more test commands"); the 108
    chip flashes at "They run in the container too"; "Ran 9 tests" GREEN; the 108 chip leaves and
    README.md · line 82 `show_chat(DB_PATH, act1_result["run_id"])` comes in with the GREY caption
    "notebook only · the image has no IPython" (no capture folder on screen); "Ran 12 tests" GREEN;
    both OK GREEN; a 0.6 s hold keeps the chip readable.
 5  LECTURE 44. TRACKER Colab 1, then 2. The terminal fades. A BLUE frame "Agent Harness · Colab"
    (tag illustration): File › Save a copy in Drive (excerpt chip Agent Harness · cell 1 (excerpt)
    "Save a copy in Drive"); a schematic Secrets panel (GOLD key, "Name: OPENAI_API_KEY", no
    value, a toggle "Notebook access" that turns on, YELLOW); CODE(colab/cell-10.py: 3–6) (GREY
    subtitle "Setup OpenAI Key"), `userdata.get('OPENAI_API_KEY')` GOLD.
 6  TRACKER Colab 3. CODE(colab/cell-08.py: 6–8) (subtitle "Install Dependencies"; lines 7, 8
    wrap), line 7 YELLOW; seven small GREEN pin chips "7 pins (pyproject.toml)"; a GREY dashed
    ghost `uv.lock` "not used here"; a row of GREY unpinned dependencies that drift, GREY tag
    "their ~200 dependencies: unpinned"; a TEAL chip "Docker: uv sync from uv.lock".
 7  Line 8 YELLOW; under the panel RECORDED(expected/colab-c08-install.txt: 2) (wrapped at a
    space; the GREEN caption "check_sdk · returncode=0" on its header row) and
    RECORDED(expected/colab-c11-utils.txt: 2–3) side by side (20 pt, headers "cell 8 / cell 11 ·
    saved output": the frame names the notebook), one GREY tag "recorded · the staff's saved Colab
    run" centred under both; caption "every recorded answer in this video: this notebook's saved run".
    The frame and the lecture tag fade; the static ▶ card (the six commands as typed, "or: the
    Colab setup cells", GREY "if a step fails: README › Troubleshooting (lines 828–839)", GREEN
    "offline · free"). Hold 2 s; fade to an empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    RoundedRectangle,
    VGroup,
)

from common import *  # noqa: F401,F403
from common import _mixed_row  # one chip mixing mono and serif pieces on one baseline
from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ the real captures (file line numbers)
SDK = capture("container/03")
assert SDK.cmd == "python -m scripts.check_sdk", SDK.cmd
assert SDK.line(3) == '  "python": "3.13.16",' and '"agent-framework": "1.19.0"' in SDK.line(5), SDK.lines[:5]
assert '"openai": "3.19.2"' in SDK.line(8) and SDK.line(29) == "}", SDK.line(8)
assert all(SDK.line(n).rstrip(",").endswith(": true") for n in range(13, 24))        # 11 features, all true
FEATURES = SDK.fold(12, 24, '  "features": { … },')
TESTS = capture("container/04")
assert TESTS.cmd == "python -m tests" and TESTS.line(4) == "Ran 281 tests in 99.378s", TESTS.lines
LOGS = capture("container/05")
assert LOGS.cmd == "python -m tests --show-logs", LOGS.cmd
assert "Injected nested checkout audit outage" in LOGS.line(3) and LOGS.line(1888) == "OK", LOGS.line(3)
MODELC = capture("container/06")
assert MODELC.cmd == "python -c 'from formaggio.config import MODEL; print(MODEL)'", MODELC.cmd
assert MODELC.line(2) == MODEL_ID, MODELC.lines
NB = capture("container/07")
assert NB.cmd == "python -m tests -p test_notebook.py" and NB.line(4).startswith("Ran 9 tests"), NB.lines
CV = capture("container/08")
assert CV.cmd == "python -m tests -p test_chat_view.py" and CV.line(4).startswith("Ran 12 tests"), CV.lines
C08 = capture("expected/colab-c08-install")
assert C08.line(2).endswith("returncode=0)"), C08.line(2)
C11 = capture("expected/colab-c11-utils")
assert C11.line(2) == f"Model: {MODEL_ID}" and C11.line(3) == "live model", C11.lines
NO_IPY = capture("container/01")
assert "No module named 'IPython'" in NO_IPY.line(14), NO_IPY.line(14)

# README phrases (exact sub-strings) and the notebook-only line
R127 = "does not establish live model quality"                       # README.md:127
R108 = "Run every remaining command inside the container"            # README.md:108 (excerpt)
R82 = 'show_chat(DB_PATH, act1_result["run_id"])'                    # README.md:82 (the whole line)
assert R127 in source_line("README.md", 127)
assert R108 in source_line("README.md", 108)
assert source_line("README.md", 82).strip() == R82
assert "`--model`, then `OPENAI_CHAT_MODEL`, then the default" in source_line("README.md", 137)
assert "**inside the container**" in source_line("README.md", 145)
assert "changing `--model` to a Gemini name does not switch providers" in source_line("README.md", 155)
SAVE = "Save a copy in Drive"                                        # Colab cell 1 line 5
assert SAVE in source_line("colab/cell-01.md", 5)
assert "userdata.get('OPENAI_API_KEY')" in source_line("colab/cell-10.py", 4)
assert '*project["project"]["dependencies"]' in source_line("colab/cell-08.py", 7)
PINS = [ln.strip() for ln in source_text("pyproject.toml").split("dependencies = [", 1)[1].split("]", 1)[0]
        .splitlines() if ln.strip()]
assert len(PINS) == 7 and all("==" in p for p in PINS), PINS            # seven pins, every one "=="
TROUBLE = (828, 839)
assert source_line("README.md", 828) == "## Troubleshooting" and source_line("README.md", 839).startswith("| Changes")

# ------------------------------------------------------------------ layout
T_ROWS = 13                     # beats 0-2: the container terminal (top 2.59)
NB_ROWS = 10                    # beat 4: two notebook test runs (top 1.38: two band rows above)
BAND1_Y, BAND2_Y = 1.85, 2.45   # rows of the band between a 10-row terminal and the tracker
GAP_Y = STRIP_TOP + 0.14        # the lowest y a picture above the 3-row strip uses
COLAB_TOP = 2.6                 # the Colab frame's top border (its title tab stays under the tracker)
BOX_PT = 20                     # the two saved-output boxes (side by side under the cell 8 panel)


# ------------------------------------------------------------------ small helpers
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


def wait_at(scene, vo, phrase: str, dt: float = 0.0):
    """vo.wait_until(phrase), moved by dt seconds. Inside a sentence an anchor is interpolated by
    character count, and spoken numbers ("3.13.16") run far longer than their characters
    (docs/PLAYBOOK.md §2.6). Every dt below was measured from the punctuation pauses of the cached
    af_heart clip (speed 0.9): the clause starts where the voice really says the phrase."""
    t = vo.time_until(phrase) + dt
    if t > 1 / 60:
        scene.wait(t)


def light(scene, mob, color: str, k: float = 1.2, sub=None, run_time: float = 0.7):
    """mob turns `color`, then it (or its part `sub`) pulses in that colour: two plays, so the
    pulse never undoes the colour change (an Indicate restores its start state at the end)."""
    scene.play(mob.animate.set_color(color), run_time=0.3)
    scene.play(flash(mob if sub is None else sub, color, k), run_time=run_time - 0.3)


def rows_of(line) -> list:
    """The rows of a typed command (one, or the rows of a folded one)."""
    return list(line.rows) if hasattr(line, "rows") else [line]


def under_rows(rows, sub: str, color: str = TURN) -> VGroup:
    """One underline per row for `sub` in ONE printed line that may have folded over `rows`."""
    full = rows[0].src
    i = full.find(sub)
    assert i >= 0, (sub, full)
    j = i + len(sub)
    out = VGroup()
    for r in rows:
        a, b = r.src_span
        lo, hi = max(i, a), min(j, b)
        if lo < hi:
            out.add(under(glyph_range(r, lo - a + r.src_indent, hi - a + r.src_indent), color, stroke=4))
    return out


def dashed_chip(text: str, color: str = S.GREY, font: str | None = None) -> VGroup:
    """A GREY dashed chip (a ghost, a lecture-style aside): text in its colour, dashed border."""
    t = mono(text, CAPTION, color) if font == MONO else label(text, CAPTION, color)
    b = box(t.width + 0.5, t.height + 0.3, color, dashed=True, stroke=2.5).move_to(t)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def mixed_chip(parts, color: str) -> VGroup:
    """A chip whose text mixes mono ("`code`") and serif pieces on one baseline."""
    t = _mixed_row(parts, CAPTION, INK)
    b = box(t.width + 0.5, t.height + 0.3, color, fill_opacity=0.14, stroke=2.5, radius=0.2).move_to(t)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def toggle():
    """A schematic switch (off: GREY knob left). .pill .knob; turn_on() -> animations."""
    pill = RoundedRectangle(width=0.78, height=0.38, corner_radius=0.19, stroke_color=S.GREY,
                            stroke_width=2.5).set_fill(S.GREY, 0.12)
    knob = Circle(radius=0.13, stroke_width=0).set_fill(S.GREY, 1).move_to(pill.get_left() + RIGHT * 0.2)
    g = VGroup(pill, knob)
    g.pill, g.knob = pill, knob

    def turn_on():
        return [pill.animate.set_stroke(TURN, 3).set_fill(TURN, 0.25),
                knob.animate.move_to(pill.get_right() + LEFT * 0.2).set_fill(TURN, 1)]
    g.turn_on = turn_on
    return g


def secrets_panel() -> VGroup:
    """Colab's Secrets panel, schematic (no screenshot, no logo): a GOLD key and "Secrets", one row
    "Name: OPENAI_API_KEY" (no value shown), under it a "Notebook access" switch. .frame .field .switch
    .on (the YELLOW "on", hidden until the switch flips) .head"""
    kg = key_glyph(0.3, KEY)
    title = label("Secrets", CAPTION, INK)
    head = VGroup(kg, title).arrange(RIGHT, buff=0.2)
    name_l = label("Name:", CAPTION, S.GREY)
    ft = mono(KEY_VAR, CAPTION, INK)
    fb = box(ft.width + 0.45, ft.height + 0.3, S.GREY, fill=S.BG, fill_opacity=1, stroke=2, radius=0.08).move_to(ft)
    field = VGroup(fb, ft)
    acc_l = label("Notebook access:", CAPTION, S.GREY)
    sw = toggle()
    on = label("on", CAPTION, TURN)
    row1 = VGroup(name_l, field).arrange(RIGHT, buff=0.25)
    row2 = VGroup(acc_l, sw, on).arrange(RIGHT, buff=0.25)
    body = VGroup(head, row1, row2).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    fr = box(body.width + 0.8, body.height + 0.6, S.GREY, fill=S.BG, fill_opacity=0.95, stroke=2.5,
             radius=0.16).move_to(body)
    on.set_opacity(0)
    g = VGroup(fr, head, row1, row2)
    g.frame, g.head, g.field, g.switch, g.on = fr, head, field, sw, on
    return g


def pin_row() -> VGroup:
    """Seven small GREEN pin chips "==" (pyproject.toml's seven pinned dependencies)."""
    chips = VGroup()
    for _ in PINS:
        t = mono("==", BOX_PT, HARNESS)
        b = box(t.width + 0.26, t.height + 0.26, HARNESS, fill_opacity=0.15, stroke=2.5, radius=0.08).move_to(t)
        chips.add(VGroup(b, t))
    return chips.arrange(RIGHT, buff=0.12)


def loose_deps(n_cols: int = 13, seed: int = 7) -> VGroup:
    """Two rows of small GREY open circles: the pins' own dependencies, unpinned."""
    dots = VGroup(*[Circle(radius=0.085, stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY, 0.15)
                    for _ in range(2 * n_cols)])
    dots.arrange_in_grid(rows=2, cols=n_cols, buff=(0.2, 0.16))
    return dots


def saved_output(rows, header: str) -> VGroup:
    """RECORDED: a saved Colab output as an output box (never a terminal frame), BOX_PT mono rows
    (two boxes side by side need 20 pt: the frame is 12.9 wide)."""
    return output_box(rows, header, size=BOX_PT)


class VerifyOffline(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, len(SAY)

        # ========================================================== 0 · step 1: check_sdk
        tr = tracker("Verify", 1)
        t = term(container=True, rows=T_ROWS)
        ft = frame_tags(t, offline_tag())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.25), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("offline")
            self.play(FadeIn(ft, shift=DOWN * 0.1), run_time=0.4)
            self.play(flash(ft[0].text, HARNESS, 1.2), run_time=0.6)
            vo.wait_until("Step 1 checks")
            type_cmd(self, t, SDK.cmd, 0.8)
            vo.wait_until("and prints the installed")
            out0 = show(self, t, SDK, (2, 11), FEATURES, "…", 29, run_time=1.0)
            r3, r5, r8, rf = out0[1], out0[3], out0[6], out0[10]
            wait_at(self, vo, "at the time of recording", -0.9)      # spoken 7.7 s, interpolated 8.6 s
            pin(self, r3, beside(grey_tag("at the time of recording"), t, r3, buff=0.6), run_time=0.4)
            wait_at(self, vo, "Python 3.13.16", -1.5)                # spoken 9.5 s, interpolated 11.1 s
            light(self, substring(r3, '"3.13.16"'), HARNESS)
            vo.wait_until("agent framework 1.19.0")
            v5, v8 = substring(r5, '"1.19.0"'), substring(r8, '"3.19.2"')
            light(self, v5, HARNESS)
            light(self, v8, HARNESS)
            wait_at(self, vo, "and every feature true", 0.8)         # spoken 15.7 s, interpolated 14.9 s
            ftag = tag("11 features · all true", HARNESS)
            pin(self, rf, beside(ftag, t, rf, buff=0.6), run_time=0.4)
            self.play(flash(substring(rf, '"features"'), HARNESS, 1.15), run_time=0.6)

        # ========================================================== 1 · step 2: the 281 tests; what they test
        c127 = top_chip(R127, where="README.md · line 127")
        # the picture above the strip (illustration): the harness, a scripted seat, no route out
        ring_ = RoundedRectangle(width=4.4, height=2.6, corner_radius=1.0, stroke_color=HARNESS,
                                 stroke_width=10).move_to([-2.5, 0.25, 0])
        ring_t = label("the harness", CAPTION, HARNESS).next_to(ring_, UP, buff=0.24)   # clear of the thick ring
        seat_t = VGroup(label("scripted model", CAPTION, INK), label("responses", CAPTION, INK)) \
            .arrange(DOWN, buff=0.08)
        seat = box(seat_t.width + 0.5, seat_t.height + 0.36, CLOUD, dashed=True, stroke=3)
        seat.move_to(ring_).shift(UP * 0.3)
        seat_t.move_to(seat)
        stag = scripted_tag().next_to(seat, DOWN, buff=0.18)
        ill = illustration_tag()
        place(ill, left=-6.3, cy=ring_t.get_center()[1])
        cl = cloud(2.2, CLOUD).move_to([4.75, 0.3, 0])
        clt = label("OpenAI", CAPTION, INK).move_to(cl)
        hl = Line(ring_.get_right() + RIGHT * 0.08, cl.get_left() + RIGHT * 0.05, color=LOOKUP, stroke_width=4)
        ht = label("HTTPS", CAPTION, LOOKUP).next_to(hl.point_from_proportion(0.3), UP, buff=0.12)
        xm = cross_mark(0.5, S.GREY, 6).move_to(hl.point_from_proportion(0.66))
        nokey = chip("no key · no tokens", S.GREY, size=CAPTION).next_to(xm, DOWN, buff=0.3)
        harness_g = VGroup(ring_, ring_t, seat, seat_t, stag, ill)
        route_g = VGroup(hl, ht, cl, clt)
        with self.voiceover(SAY[1]) as vo:
            self.play(tr.goto(2), run_time=0.5)
            t.clear(self, run_time=0.3)
            type_cmd(self, t, TESTS.cmd, 0.5)
            vo.wait_until("281 of them")
            show(self, t, TESTS, 2, wrap=True, run_time=1.2)
            out1 = show(self, t, TESTS, 3, 4, 6, run_time=0.4)
            ran, ok = out1[1], out1[2]
            bare_prompt(self, t)
            light(self, ran.glyphs, HARNESS, 1.3, sub=substring(ran, "281"))
            vo.wait_until("in about 100 seconds")
            self.play(flash(substring(ran, "99.378s"), TURN, 1.2), run_time=0.6)
            vo.wait_until("ending in OK")
            light(self, ok.glyphs, HARNESS, 1.5)
            vo.wait_until("They use scripted")
            cmd1 = t.lines[0]
            resize(self, t, 3, keep=[cmd1, ran, ok], run_time=0.6, extra=[FadeOut(ft)])
            # the scripted seat lands while "scripted model responses" is spoken
            self.play(FadeIn(VGroup(ring_, ring_t, ill)), Create(seat), FadeIn(seat_t),
                      FadeIn(stag, shift=DOWN * 0.08), run_time=0.7)
            self.play(FadeIn(route_g), FadeIn(c127, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("so they test the machinery")
            self.play(flash(ring_, HARNESS, 1.06), flash(ring_t, HARNESS, 1.2), run_time=0.8)
            vo.wait_until("not the model")
            self.play(Create(xm), hl.animate.set_stroke(opacity=0.35), ht.animate.set_opacity(0.4),
                      VGroup(cl, clt).animate.set_opacity(0.4), run_time=0.5)
            self.play(FadeIn(nokey, shift=UP * 0.1), run_time=0.4)
            self.play(flash(c127.phrase, TURN, 1.03), run_time=0.6)
            self.wait(0.6)                              # the picture holds before the terminal grows back

        # ========================================================== 2 · step 3: the logs; trust the last line
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(harness_g, route_g, xm, nokey, c127)), tr.goto(3), run_time=0.5)
            t.clear(self, run_time=0.25)
            resize(self, t, T_ROWS, run_time=0.5)
            ft = frame_tags(t, offline_tag())
            self.play(FadeIn(ft), run_time=0.3)
            type_cmd(self, t, LOGS.cmd, 0.6)
            out2 = show(self, t, LOGS, 2, (LOGS.line(3), ERR), "…", wrap=True, run_time=0.7)
            show(self, t, LOGS, (1885, 1888), run_time=0.4)
            ok2 = t.lines[-1]
            bare_prompt(self, t)
            l2, l3 = item_rows(out2, 0), item_rows(out2, 1)
            vo.wait_until("deliberate failures")
            self.play(flash(VGroup(*[r.glyphs for r in l3]), ERR, 1.04), run_time=0.7)
            pin(self, l3[-1], beside(grey_tag("deliberate"), t, l3[-1], buff=0.5), run_time=0.4)
            vo.wait_until("and an approval-identity warning")
            u2 = VGroup(*under_rows(l2, "Ignored an approval response"),
                        *under_rows(l2, "approval occurrence identity"))
            self.play(Create(u2), run_time=0.6)
            a4 = beside(grey_tag("again in act 4"), t, l2[-1], buff=0.5)
            a4.shift(RIGHT * max(0.0, u2.get_right()[0] + 0.25 - a4.get_left()[0]))   # not under the underline
            assert a4.get_right()[0] < t.box.get_right()[0] - 0.12
            pin(self, l2[-1], a4, run_time=0.4)
            vo.wait_until("Trust the last line")
            light(self, ok2.glyphs, HARNESS, 1.5)
            pin(self, ok2, beside(note("trust the last line", HARNESS), t, ok2, buff=0.5), run_time=0.4)

        # ========================================================== 3 · the model check; precedence
        p9 = src_panel("formaggio/config.py", 9)
        place(p9, cx=0, top=2.55)
        span_m = p9.span(9, '"gpt-5.6-luna"')
        span_env = p9.span(9, '"OPENAI_CHAT_MODEL"')
        att = grey_tag("at the time of recording")
        place(att, right=span_m.get_right()[0] + 0.1, top=p9.get_bottom()[1] - 0.12)
        link_flag = chip("--model", LOOKUP, size=CAPTION, font=MONO)
        link_env = chip("OPENAI_CHAT_MODEL", LOOKUP, size=CAPTION, font=MONO)
        link_def = chip("default", LOOKUP, size=CAPTION)
        gt1, gt2 = label("›", 30, LOOKUP), label("›", 30, LOOKUP)
        chain = VGroup(link_flag, gt1, link_env, gt2, link_def).arrange(RIGHT, buff=0.25)
        src137 = note("(README.md · line 137)")
        place(chain, left=-6.0, cy=0.2)
        src137.next_to(chain, RIGHT, buff=0.35)
        cap145 = note("set it inside the container (README.md · line 145)")
        place(cap145, left=link_env.get_left()[0], cy=-0.36)
        gem = dashed_chip("a Gemini name doesn't switch providers (README.md · line 155)")
        place(gem, left=-6.0, cy=-0.95)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(u2), run_time=0.3)
            tr = switch_section(self, tr, "Model", 1)
            t.clear(self, run_time=0.25)
            mc = type_cmd(self, t, MODELC.cmd, 0.9)
            om = show(self, t, MODELC, 2, run_time=0.4)[0]
            bare_prompt(self, t)
            wait_at(self, vo, "GPT 5.6 Luna", -0.9)                  # spoken 3.4 s, interpolated 4.3 s
            light(self, om.glyphs, CLOUD, 1.2)
            resize(self, t, 3, keep=[*rows_of(mc), om], run_time=0.6, extra=[FadeOut(ft)])
            self.play(FadeIn(p9, shift=UP * 0.15), run_time=0.5)
            light(self, span_m, CLOUD, 1.2)
            vo.wait_until("at the time of recording")
            self.play(FadeIn(att, shift=UP * 0.08), run_time=0.4)
            vo.wait_until("A model flag")
            self.play(FadeIn(link_flag, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("beats an environment variable")
            self.play(FadeIn(gt1), FadeIn(link_env, shift=RIGHT * 0.15), run_time=0.5)
            light(self, span_env, LOOKUP, 1.15)
            vo.wait_until("which beats this default")
            self.play(FadeIn(gt2), FadeIn(link_def, shift=RIGHT * 0.15), FadeIn(src137), run_time=0.5)
            self.play(flash(span_m, LOOKUP, 1.2), run_time=0.6)
            vo.wait_until("if your account")
            self.play(FadeIn(cap145, shift=DOWN * 0.08), run_time=0.5)
            self.play(FadeIn(gem, shift=DOWN * 0.08), run_time=0.5)
            vo.wait_until("set either")
            self.play(flash(link_flag, TURN, 1.2), flash(link_env, TURN, 1.2), run_time=0.8)

        # ========================================================== 4 · the notebook path's two test commands
        c108 = readme_chip("README.md · line 108 (excerpt)", R108)
        place(c108, left=-6.3, cy=BAND2_Y)
        c82 = excerpt_chip(R82, "README.md · line 82", line=source_line("README.md", 82))
        c82.header.next_to(c82.chip, LEFT, buff=0.3)
        place(c82, left=-6.3, cy=BAND2_Y)
        # the image's missing IPython is an extra check (container/01 line 14, ASSETS.md); the
        # caption names no capture folder (script.md: headers never name one)
        cap82 = note("notebook only · the image has no IPython")
        place(cap82, left=c82.chip.get_left()[0] + 0.1, cy=BAND1_Y)
        with self.voiceover(SAY[4]) as vo:
            gone = list(t.lines)
            self.play(FadeOut(VGroup(p9, att, chain, src137, cap145, gem, *gone)), run_time=0.4)
            for ln in gone:
                t.lines.remove(ln)
            tr = switch_section(self, tr, "Notebook", 1)
            resize(self, t, NB_ROWS, run_time=0.5)
            ft = frame_tags(t, offline_tag())
            # SHOW order: the line-108 chip first (it governs both commands), then the typing
            self.play(FadeIn(ft), FadeIn(c108, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("two more test commands")
            type_cmd(self, t, NB.cmd, 0.5)
            o7 = show(self, t, NB, (2, 4), 6, run_time=0.4)
            self.play(tr.goto(2), run_time=0.3)
            type_cmd(self, t, CV.cmd, 0.5)
            o8 = show(self, t, CV, (2, 4), 6, run_time=0.4)
            vo.wait_until("They run in the container too")
            self.play(flash(c108.phrase, TURN, 1.03), run_time=0.6)
            vo.wait_until("9 notebook tests")
            light(self, o7[2].glyphs, HARNESS, 1.15, sub=substring(o7[2], "Ran 9 tests"))
            # the chat-view chip comes in as "12 chat view tests" is spoken (old chip out, then new in)
            self.play(FadeOut(c108), run_time=0.3)
            self.play(FadeIn(c82, shift=DOWN * 0.1), FadeIn(cap82, shift=DOWN * 0.08), run_time=0.5)
            vo.wait_until("and 12 chat view tests")
            light(self, o8[2].glyphs, HARNESS, 1.15, sub=substring(o8[2], "Ran 12 tests"))
            vo.wait_until("both OK")
            self.play(o7[3].glyphs.animate.set_color(HARNESS), o8[3].glyphs.animate.set_color(HARNESS),
                      run_time=0.3)
            self.play(flash(o7[3].glyphs, HARNESS, 1.5), flash(o8[3].glyphs, HARNESS, 1.5), run_time=0.6)
        self.wait(0.6)                                  # the line-82 chip and its caption stay readable

        # ========================================================== 5 · the second road: the course Colab
        lr = lref("44")
        cf = colab_frame(top=COLAB_TOP)
        menu = menu_path(["File", SAVE])
        place(menu, left=-6.0, cy=1.75)
        ex1 = excerpt_chip(SAVE, "Agent Harness · cell 1 (excerpt)", line=source_line("colab/cell-01.md", 5))
        place(ex1, left=-6.0, top=menu.get_bottom()[1] - 0.35)
        sp = secrets_panel()
        place(sp, right=6.0, cy=0.9)
        p10 = src_panel("colab/cell-10.py", 3, 6, subtitle=True)
        place(p10, cx=0, bottom=-3.3)
        span_k = p10.span(4, "userdata.get('OPENAI_API_KEY')")
        bar_k = p10.bar(4, COST, 0.2)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(t, ft, c82, cap82)), run_time=0.5)
            tr = switch_section(self, tr, "Colab", 1)
            self.play(FadeIn(cf), FadeIn(lr, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Save a copy")
            self.play(FadeIn(menu, shift=DOWN * 0.1), run_time=0.4)
            self.play(menu.light(0), run_time=0.3)
            self.play(menu.light(1), run_time=0.4)
            self.play(FadeIn(ex1, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("add your key as a secret")
            self.play(tr.goto(2), run_time=0.4)
            self.play(FadeIn(sp, shift=UP * 0.1), run_time=0.5)
            self.play(flash(sp.head[0], KEY, 1.4), flash(sp.field[1], TURN, 1.08), run_time=0.7)
            wait_at(self, vo, "allow notebook access", 0.55)         # spoken 8.8 s, interpolated 8.3 s
            self.play(*sp.switch.turn_on(), sp.on.animate.set_opacity(1), run_time=0.6)
            wait_at(self, vo, "and run the setup cells", 0.45)       # spoken 10.4 s, interpolated 10.0 s
            self.play(FadeIn(p10, shift=UP * 0.12), run_time=0.5)
            self.play(FadeIn(bar_k), span_k.animate.set_color(COST), run_time=0.5)
            self.play(flash(span_k, COST, 1.08), run_time=0.6)

        # ========================================================== 6 · setup cells: seven pins, not the lockfile
        p8 = src_panel("colab/cell-08.py", 6, 8, wrap=True, subtitle=True)
        place(p8, cx=0, top=2.3)
        bar7 = p8.bar(7, TURN, 0.18)
        pins = pin_row()
        place(pins, left=-6.0, cy=-0.95)
        pins_t = _mixed_row(["7 pins", "`(pyproject.toml)`"], CAPTION, HARNESS).next_to(pins, RIGHT, buff=0.3)
        ghost = dashed_chip("uv.lock", font=MONO)
        ghost_t = note("not used here")
        gg = VGroup(ghost, ghost_t).arrange(DOWN, buff=0.12)
        place(gg, right=6.0, top=pins.get_top()[1] + 0.05)
        deps = loose_deps()
        place(deps, left=-6.0, cy=-1.85)
        deps_t = grey_tag("their ~200 dependencies: unpinned").next_to(deps, RIGHT, buff=0.4)
        dock = mixed_chip(["Docker:", "`uv sync`", "from", "`uv.lock`"], CTR)
        place(dock, right=6.0, cy=-2.75)
        rng = np.random.default_rng(3)
        drift = [d.animate.shift(np.array([rng.uniform(-0.09, 0.09), rng.uniform(-0.07, 0.07), 0])) for d in deps]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(menu, ex1, sp, p10, bar_k)), tr.goto(3), run_time=0.5)
            self.play(FadeIn(p8, shift=UP * 0.12), run_time=0.5)
            self.play(FadeIn(bar7), run_time=0.4)
            vo.wait_until("installs the seven pinned")
            self.play(flash(p8.span(7, '*project["project"]["dependencies"]'), HARNESS, 1.08), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in pins], lag_ratio=0.12), run_time=0.8)
            self.play(FadeIn(pins_t), run_time=0.4)
            vo.wait_until("not the lockfile")
            self.play(FadeIn(gg, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("so their dependencies")
            self.play(FadeIn(deps, lag_ratio=0.05), run_time=0.6)
            self.play(*drift, FadeIn(deps_t, shift=LEFT * 0.1), run_time=0.8)
            vo.wait_until("for identical versions")
            self.play(FadeIn(dock, shift=UP * 0.1), run_time=0.5)
            self.play(flash(dock, CTR, 1.06), run_time=0.6)

        # ========================================================== 7 · the saved run; ▶ verify either way
        bar8 = p8.bar(8, TURN, 0.18)
        c08_rows = [row for row, *_ in wrap_output(C08.line(2), 44)]
        assert "".join(r.strip() for r in c08_rows).replace(" ", "") == C08.line(2).replace(" ", "")
        b08 = saved_output(c08_rows, "cell 8 · saved output")
        b11 = saved_output(C11.at((2, 3)), "cell 11 · saved output")
        boxes = VGroup(b08, b11).arrange(RIGHT, buff=0.45, aligned_edge=UP)
        place(boxes, cx=0, top=p8.get_bottom()[1] - 0.25)
        # GREEN caption on the cell-8 box's header row (on line 8's YELLOW bar it was hard to read)
        ok8 = label("check_sdk · returncode=0", CAPTION, HARNESS)
        ok8.next_to(b08.header, RIGHT, buff=0.45).set_y(b08.header.get_center()[1])
        assert ok8.get_right()[0] < b08.frame.get_right()[0]
        rec = recorded_tag()
        place(rec, cx=boxes.get_center()[0], top=boxes.get_bottom()[1] - 0.15)   # one tag for both boxes
        every = label("every recorded answer in this video: this notebook's saved run", CAPTION, INK)
        place(every, cx=0, top=rec.get_bottom()[1] - 0.15)
        card = turn_card([SDK.cmd, TESTS.cmd, LOGS.cmd, MODELC.cmd, NB.cmd, CV.cmd,
                          Prose("or: the Colab setup cells"),
                          (Prose(f"if a step fails: README › Troubleshooting (lines {TROUBLE[0]}–{TROUBLE[1]})"),
                           S.GREY),
                          (Prose("offline · free"), HARNESS)])
        place(card, cx=0, cy=-0.35)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(pins, pins_t, gg, deps, deps_t, dock, bar7)), run_time=0.4)
            self.play(FadeIn(bar8), run_time=0.4)
            self.play(FadeIn(b08, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(ok8, shift=LEFT * 0.1), run_time=0.4)
            self.play(FadeIn(b11, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(rec), run_time=0.3)
            self.play(FadeIn(every, shift=UP * 0.08), run_time=0.5)
            vo.wait_until("Pause, and verify")
            self.play(FadeOut(VGroup(cf, p8, bar8, ok8, boxes, rec, every, lr)), run_time=0.5)
            self.play(FadeIn(card, shift=UP * 0.1), run_time=0.5)
        self.wait(2)                                    # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tr, card)), run_time=0.6)
        self.wait(0.3)
