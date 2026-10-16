"""S05 · Step 2: ENTRYPOINT (README A8, one extra inspect, a bare bash prompt).

Beats (script.md "## S05", one voiceover block each):
 0  TRACKER A7 -> A8. CODE(README.md: 142) `ENTRYPOINT ["/bin/bash"]` at the top (its keyword and
    then its value pulse as they are said) and a 5-row strip terminal below it. The strip types
    `cat Dockerfile` (row tag `extra`; TRACKER A8 · extra while it is typed, as in S04/S06/S08)
    -> laptop/13 lines 2-5 while "slash bin slash bash" is said
    (the beat is 6.5 s: typed any later, the output would be gone a second after it appears); on
    "Put it under the FROM line" the FROM row pulses and line 5 (the new line) gets a YELLOW bar.
 1  TRACKER A8 (" · extra" fades as the build is typed). The terminal grows to 8 rows (the
    README panel stays above it; the cat output scrolls away under the build, its YELLOW
    ENTRYPOINT row last to go):
    `docker build -t simple-translate -f Dockerfile .` (folds onto 2 rows) + ▶ your turn ->
    laptop/14 lines 15 (cut after `@sha256:34386ef0`, folded onto 2 rows: wider than a row), 17, …,
    25. `#4 CACHED` turns TEAL and pulses on "The FROM step says CACHED". On "and no layer is added"
    the terminal shrinks to the 3-row strip (the command and its CACHED line) and S04's picture
    returns unchanged: the V2 stack (four thin ORANGE slabs, brace "base image", mono caption
    `python:3.12-slim-bookworm`) and the TEAL config card (ENTRYPOINT "null", CMD tile
    `["python3"]`, WorkingDir `""`, start-up line `python3`). On "ENTRYPOINT only writes" the
    panel's `["/bin/bash"]` is copied (TransformFromCopy, glyph to glyph, arcing over the card's
    rows) into the ENTRYPOINT slot, where its tile frame closes round it (the "null" note fades),
    and the caption "config only: / nothing downloaded, / no new layer" appears between stack
    and card.
 2  V3 close-up of the card: the README panel and caption leave, the stack dims. GREY labels with
    short arrows point at the slots from the left (the stacked card has no room under its slots):
    ENTRYPOINT "the program", CMD "its default arguments", each as it is said. The `["/bin/bash"]`
    tile pulses on "The entrypoint is now bash"; the inherited `["python3"]` tile turns dashed on
    "the command slot still says python3". On "So will the container start" the start-up line
    becomes `/bin/bash python3` (the tile's /bin/bash is copied down in front of python3) with a
    YELLOW "?". While the "?" wiggles, the strip clears and grows to 4 rows (so beat 3's command
    is typed on its first words).
 3  TRACKER A8 · extra (only the " · extra" suffix fades in: extra_caption()). The strip types
    `docker image inspect simple-translate --format 'Entrypoint={{json .Config.Entrypoint}}
    Cmd={{json .Config.Cmd}}'`
    (folded by hand at the two spaces outside the quotes, so it pastes back as one command: the
    quoted format string is exactly one row; row tag `extra`) -> laptop/15 line 2.
    `Entrypoint=["/bin/bash"]` gets a TEAL underline (the tile pulses), `Cmd=null` a YELLOW bar;
    on "Setting an entrypoint resets" the `["python3"]` tile falls off the card and fades, a GREY
    "null" takes its slot; "base image" pulses on "inherited from the base image"; on "So bash
    starts on its own" the start-up line becomes `/bin/bash` and the "?" goes.
 4  TRACKER A8 (" · extra" fades out). The picture leaves except the prediction: the start-up
    line `/bin/bash` moves top right with a GREY "predicted:" (S04's idiom); the strip clears and
    grows to 6 rows: `docker run --rm -ti simple-translate` (2 rows) + ▶ your turn -> the bare
    prompt `root@f72851da4a58:/#` (laptop/16 line 2), and the prediction gets a GREEN check. On
    "Read it left to right" the prompt is copied large above the terminal and a YELLOW arrow runs
    under it; on "You're root" it splits into its parts: `root` gets a
    YELLOW underline and "you, the administrator, / inside the container"; on "After the at sign"
    `f72851da4a58` gets "the container's ID / new every run" (TEAL); "which changes every run"
    pulses it.
 5  On "And the slash" the `/` gets its underline and "the top folder"; on "because this image
    sets no working directory" a GREY chip `WorkingDir=""` (laptop/10 line 2) with "no WORKDIR"
    appears and pulses with the slash. On "Type exit" it types `exit` at the container prompt
    (laptop/16 line 2) -> line 3; the laptop prompt returns. Fade out to an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.devops import code_span
from explainer.scene import VoiceScene

from common import (BUILD, CAT, INK, INSPECT_V2, IMAGE, LAPTOP_DIR, MONO, NARRATION, P_LAPTOP, RUN,
                    STRIP_ROWS, SYSTEM, TURN, VENV, ConfigCard, LayerStack, _caption, attach,
                    bare_prompt, beside, capture, check_mark, chip, code, cut, glyph_range, hl_bar, istep,
                    label, laptop_term, mono, mono_line, pin, resize, row_tag, steady, substring,
                    track, tracker_a, type_cmd, under, unpin)

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ real outputs (file line numbers)
C13 = capture("13", LAPTOP_DIR)                          # laptop/13-dockerfile-v2.txt
assert C13.cmd == CAT, C13.cmd
CAT_OUT = C13.at((2, 5))                                 # comment, FROM, "", ENTRYPOINT ["/bin/bash"]
assert CAT_OUT[3] == 'ENTRYPOINT ["/bin/bash"]', CAT_OUT

C14 = capture("14", LAPTOP_DIR)                          # laptop/14-build-v2.txt
assert C14.cmd == BUILD, C14.cmd
BUILD_OUT = [cut(C14.line(15), "@sha256:34386ef0"), *C14.at(17, "…", 25)]
assert BUILD_OUT[1] == "#4 CACHED" and "naming to" in BUILD_OUT[3], BUILD_OUT

C15 = capture("15", LAPTOP_DIR)                          # laptop/15-config-v2.txt
assert C15.cmd == INSPECT_V2, C15.cmd
INSPECT_OUT = C15.line(2)                                # Entrypoint=["/bin/bash"] Cmd=null
assert INSPECT_OUT == 'Entrypoint=["/bin/bash"] Cmd=null', INSPECT_OUT

C16 = capture("16", LAPTOP_DIR)                          # laptop/16-run-v2.txt
assert C16.cmd == RUN, C16.cmd
C_PROMPT, C_EXIT = C16.istep(2)                          # ('root@f72851da4a58:/#', 'exit')
assert C_EXIT == "exit", C16.line(2)
EXIT_ECHO = C16.at(3)                                    # ["exit"]

C10 = capture("10", LAPTOP_DIR)                          # laptop/10-config-v1.txt (S04's inspect)
_wd = C10.line(2)
WORKDIR = _wd[_wd.index("WorkingDir="):]                 # WorkingDir=""
assert WORKDIR == 'WorkingDir=""', WORKDIR

# INSPECT_V2 folded by hand: the tool's fold would hard-break inside the quoted format string.
# Breaking only at the two spaces outside the quotes, with " \" continuations, pastes back as the
# same command; the quoted string is exactly one 65-character row.
_q = INSPECT_V2.index("'")
INSPECT_ROWS = [P_LAPTOP + " docker image inspect \\", "    simple-translate --format \\", INSPECT_V2[_q:]]
assert INSPECT_V2 == "docker image inspect simple-translate --format " + INSPECT_ROWS[2]

# ------------------------------------------------------------------ layout
STACK_X, FLOOR_Y = -3.0, -0.25        # the V2 stack (3.2 wide) left of centre, clear of a 4-row strip
CARD_W, CARD_RIGHT, CARD_TOP = 3.4, 6.5, 3.4   # the stacked card at the right, clear of the tracker
                                                # caption (" · extra" ends at x = 2.7)
BIG = 40                              # the prompt copied large in beat 4


def turn_tag() -> VGroup:
    """YELLOW '▶ your turn', the height of a terminal row."""
    return row_tag("▶ your turn", TURN)


def type_rows(scene, t, rows_text: list[str], type_time: float, extra=()) -> VGroup:
    """type_cmd with rows folded by the caller (rows_text[0] starts with the prompt; a bare prompt
    line is replaced, as type_cmd does); `extra` animations play during the typing."""
    p = t.prompt + " "
    assert rows_text[0].startswith(p) and all(len(s) <= t.max_chars for s in rows_text)
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        last = t.lines[-1]
        scene.remove(last, *last.submobjects)
        t.lines.remove(last)
    t2c = t._prompt_colors(t.prompt)
    t._make_room(scene, len(rows_text))
    rows = []
    for k, s in enumerate(rows_text):
        ln = mono_line(s, t.size, INK, t2c=t2c if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        rows.append(ln)
    typed = [glyph_range(rows[0], len(p))] + [glyph_range(r, 0) for r in rows[1:]]
    scene.add(glyph_range(rows[0], 0, len(p)))
    scene.play(ShowIncreasingSubsets(VGroup(*[g for grp in typed for g in grp]), rate_func=linear),
               *extra, run_time=type_time)
    for r in rows:
        scene.add(r)
    g = VGroup(*rows)
    g.rows, g.text = rows, " ".join(r.text for r in rows)
    return g


def extra_caption(scene, tr, on: bool, run_time: float = 0.5) -> Animation:
    """Animation: ' · extra' fades in (on) or out after the tracker's caption while the shared text
    stays still. (common.track() morphs the whole caption, which scrambles it for a few frames
    when only the suffix changes.) The caption is swapped for its new version at once: the shared
    glyphs sit at the same place in both."""
    old, new = tr.caption, _caption(tr, tr.k, on)
    short, long_ = (old, new) if on else (new, old)
    n = len(short)
    assert len(long_) > n and np.allclose(short.get_left(), long_.get_left(), atol=1e-3) \
        and np.allclose(short[n - 1].get_center(), long_[n - 1].get_center(), atol=1e-3)
    suffix = VGroup(*long_[n:])
    tr.remove(old)
    tr.add(new)
    tr.caption = new
    if on:
        suffix.set_opacity(0)
        return suffix.animate(run_time=run_time).set_opacity(1)
    scene.add(suffix)                                    # the old suffix, on its own while it fades
    return FadeOut(suffix, run_time=run_time)


def startup_line(card: ConfigCard, s: str) -> Text:
    """The card's start-up line, left-aligned under the card (recorded as card.line)."""
    ln = card.startup(s, buff=0.22)
    ln.align_to(card.frame, LEFT)
    return ln


def side_label(s: str, slot) -> VGroup:
    """A GREY label left of a card slot with a short arrow to it. .text .arrow"""
    t = label(s, 22, S.GREY)
    y = slot.get_center()[1]
    x_end = slot.get_left()[0] - 0.12
    arrow = Arrow([x_end - 0.95, y, 0], [x_end, y, 0], buff=0, color=S.GREY, stroke_width=3,
                  max_tip_length_to_length_ratio=0.3, tip_length=0.16)
    t.next_to(arrow, LEFT, buff=0.12)
    g = VGroup(t, arrow)
    g.text, g.arrow = t, arrow
    return g


def part_label(first: str, second: str, color=INK) -> VGroup:
    """Two-line label under a part of the big prompt (first line coloured, second GREY). Steady
    texts, so both lines have the same height whatever their letters."""
    return VGroup(steady(first, 22, color), steady(second, 22, S.GREY)).arrange(DOWN, buff=0.04)


def clear_with(scene, t, *anims, run_time: float = 0.4) -> None:
    """t.clear(scene), played together with other animations."""
    scene.play(FadeOut(t.lines), *anims, run_time=run_time)
    for m in list(t.lines):
        t.lines.remove(m)


# ------------------------------------------------------------------ the scene
class StepEntrypoint(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, f"S05 has {len(SAY)} SAY lines; this scene times 6"

        tr = tracker_a(7)
        panel = code("README.md", 142, language="docker")
        panel.move_to([0, 1.73, 0])
        p_kw = code_span(panel.code, 0, "ENTRYPOINT")
        p_val = code_span(panel.code, 0, '["/bin/bash"]')
        t = laptop_term(5)                                   # the 5-row strip (top edge -0.63)

        # ========================================================== 0 · Step 2: one line
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.5)
            self.play(track(tr, 8), run_time=0.5)
            self.play(Indicate(VGroup(tr.dots[7], tr.caption), color=TURN, scale_factor=1.12), run_time=0.6)
            self.play(FadeIn(panel, shift=DOWN * 0.15), FadeIn(t), run_time=0.6)
            bare_prompt(self, t)
            vo.wait_until("ENTRYPOINT")
            self.play(Indicate(p_kw, color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("slash bin")
            self.play(Indicate(p_val, color=TURN, scale_factor=1.12), run_time=0.6)
            # an extra check: the tracker says so (" · extra") while it is typed, as in S04/S06/S08
            c0 = type_rows(self, t, [f"{t.prompt} {CAT}"], 0.45, extra=[extra_caption(self, tr, True)]).rows[0]
            pin(self, c0, beside(row_tag("extra"), c0), run_time=0.25)
            out0 = t.print(self, CAT_OUT, run_time=0.45, lag=0.12)
            from_row, ent_row = out0[1], out0[3]
            vo.wait_until("Put it under")
            self.play(Indicate(from_row.glyphs, color=INK, scale_factor=1.06), run_time=0.5)
            bar0 = hl_bar(ent_row.glyphs, TURN, 0.25)
            ent_row.add_to_back(bar0)
            self.add(ent_row)
            self.play(FadeIn(bar0), Indicate(ent_row.glyphs, color=TURN, scale_factor=1.06), run_time=0.6)

        # ========================================================== 1 · build again: CACHED, config only
        # S04's picture, unchanged: the stack of four base slabs and the config card
        stack = LayerStack(stack_w=3.2)
        stack.floor.move_to([STACK_X, FLOOR_Y, 0])
        base = [stack.make(None, SYSTEM, 0.15) for _ in range(4)]
        brace = stack.brace(base, "base image")
        base_name = mono("python:3.12-slim-bookworm", 20, S.GREY)
        base_name.next_to(stack.floor, DOWN, buff=0.12)
        card = ConfigCard(card_w=CARD_W)
        card.shift(np.array([CARD_RIGHT - card.frame.get_right()[0], CARD_TOP - card.frame.get_top()[1], 0]))
        n_ent = card.note("ENTRYPOINT", "null")
        t_cmd = card.place("CMD", card.tile('["python3"]'))
        n_wd = card.note("WorkingDir", '""')
        line0 = startup_line(card, "python3")
        picture = VGroup(*base, brace, base_name, card, n_ent, t_cmd, n_wd, line0)
        t_ent = card.tile('["/bin/bash"]')
        t_ent.move_to(card.slots["ENTRYPOINT"].get_left() + RIGHT * (0.08 + t_ent.width / 2))
        cfg_cap = VGroup(label("config only:", 22, IMAGE), label("nothing downloaded,", 22, S.GREY),
                         label("no new layer", 22, S.GREY)).arrange(DOWN, buff=0.1)
        cfg_cap.move_to([(stack.floor.get_right()[0] + card.frame.get_left()[0]) / 2, -0.3, 0])

        with self.voiceover(SAY[1]) as vo:
            resize(self, t, 8, run_time=0.5)
            # back to the README: " · extra" fades while its build is typed (folded as Terminal.type does)
            c1 = type_rows(self, t, t.fold(f"{t.prompt} {BUILD}", first_prefix=len(t.prompt) + 1), 0.8,
                           extra=[extra_caption(self, tr, False)])
            yt1 = beside(turn_tag(), c1.rows[0])
            pin(self, c1.rows[0], yt1, run_time=0.35)
            self.play(Wiggle(yt1, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.6)
            vo.wait_until("The FROM step")
            out1 = t.print(self, BUILD_OUT, run_time=0.5, wrap=True, lag=0.12)
            cached = t.find("#4 CACHED")
            self.play(cached.glyphs.animate.set_color(IMAGE), run_time=0.3)
            self.play(Indicate(cached.glyphs, color=IMAGE, scale_factor=1.15), run_time=0.6)
            vo.wait_until("nothing is downloaded")
            from_rows = VGroup(out1[0].glyphs, out1[1].glyphs)
            self.play(Indicate(from_rows, color=INK, scale_factor=1.03), run_time=0.7)
            vo.wait_until("and no layer")
            resize(self, t, STRIP_ROWS, keep=[*c1.rows, cached], run_time=0.7)
            self.play(FadeIn(picture, shift=UP * 0.1), run_time=0.6)
            stack.accept(self, *base)
            vo.wait_until("ENTRYPOINT only writes")
            # glyph to glyph (the tile's text has an invisible strut first); the frame closes round it
            self.play(TransformFromCopy(p_val, VGroup(*t_ent.text[1:]), path_arc=1.0),
                      FadeIn(t_ent.frame, rate_func=lambda a: smooth(max(0.0, 2 * a - 1))),
                      FadeOut(n_ent), run_time=1.0)
            self.remove(t_ent.frame, *t_ent.text)
            self.add(t_ent)
            card.tiles["ENTRYPOINT"] = t_ent
            card.notes.pop("ENTRYPOINT")
            self.play(FadeIn(cfg_cap, shift=UP * 0.1), Indicate(card.keys["ENTRYPOINT"], color=IMAGE),
                      run_time=0.6)

        # ========================================================== 2 · program + default arguments
        lab_ent = side_label("the program", card.slots["ENTRYPOINT"])
        lab_cmd = side_label("its default arguments", card.slots["CMD"])
        t_cmd2 = card.tile('["python3"]', dashed=True).move_to(t_cmd)
        line1 = steady("/bin/bash python3", 22, INK, mono_font=True)
        line1.move_to(line0, aligned_edge=LEFT)
        qmark = label("?", 30, TURN).next_to(line1, RIGHT, buff=0.12)
        dim = VGroup(*base, brace, base_name)

        with self.voiceover(SAY[2]) as vo:
            unpin(self, [(c1.rows[0], yt1)], 0.3, FadeOut(VGroup(panel, cfg_cap), shift=UP * 0.1),
                  dim.animate.set_opacity(0.35))
            vo.wait_until("Think of ENTRYPOINT")
            self.play(GrowArrow(lab_ent.arrow), FadeIn(lab_ent.text, shift=RIGHT * 0.15),
                      Indicate(card.keys["ENTRYPOINT"], color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("and CMD as")
            self.play(GrowArrow(lab_cmd.arrow), FadeIn(lab_cmd.text, shift=RIGHT * 0.15),
                      Indicate(card.keys["CMD"], color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("The entrypoint is now")
            self.play(Indicate(t_ent, color=TURN, scale_factor=1.12), run_time=0.8)
            vo.wait_until("and the command slot")
            self.play(FadeTransform(t_cmd, t_cmd2), run_time=0.6)
            card.tiles["CMD"] = t_cmd2
            self.play(Indicate(t_cmd2, color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("So will the container")
            # what became what: /bin/bash comes down from its tile, python3 slides right
            self.play(TransformFromCopy(VGroup(*t_ent.text[3:12]), VGroup(*line1[1:10])),
                      ReplacementTransform(VGroup(*line0[1:8]), VGroup(*line1[10:17])), run_time=1.0)
            self.remove(line0, *line1)
            self.add(line1)
            card.line = line1
            self.play(FadeIn(qmark, scale=1.5), run_time=0.4)
            # the build's rows leave while the question hangs, so the inspect is typed on its first words
            clear_with(self, t, Wiggle(qmark, scale_value=1.3), run_time=0.7)
            resize(self, t, 4, run_time=0.45)

        # ========================================================== 3 · inspect: Cmd=null
        line2 = steady("/bin/bash", 22, INK, mono_font=True).move_to(line1, aligned_edge=LEFT)
        null_cmd = card.note("CMD", "null")

        with self.voiceover(SAY[3]) as vo:
            c3 = type_rows(self, t, INSPECT_ROWS, 1.1, extra=[extra_caption(self, tr, True)])
            pin(self, c3.rows[0], beside(row_tag("extra"), c3.rows[0]), run_time=0.25)
            out3 = t.print(self, [INSPECT_OUT], run_time=0.3)[0]
            vo.wait_until("the entrypoint is bash")
            u_ent = under(substring(out3, 'Entrypoint=["/bin/bash"]'), IMAGE, y=out3.strut.get_bottom()[1] - 0.01)
            self.play(Create(u_ent), Indicate(t_ent, color=IMAGE, scale_factor=1.1), run_time=0.6)
            attach(self, out3, u_ent)
            vo.wait_until("and the command is now null")
            nul = substring(out3, "Cmd=null")
            bar3 = hl_bar(nul, TURN, 0.3)
            out3.add_to_back(bar3)
            self.add(out3)
            self.play(FadeIn(bar3), Indicate(nul, color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Setting an entrypoint")
            card.take(self, "CMD", run_time=0.7)
            self.play(FadeIn(null_cmd), run_time=0.35)
            vo.wait_until("inherited from")
            self.play(Indicate(brace.text, color=SYSTEM, scale_factor=1.2), dim.animate.set_opacity(0.7),
                      run_time=0.8)
            vo.wait_until("So bash starts")
            self.play(ReplacementTransform(VGroup(*line1[1:10]), VGroup(*line2[1:10])),
                      FadeOut(VGroup(*line1[10:17]), shift=DOWN * 0.3), FadeOut(qmark),
                      dim.animate.set_opacity(0.35), run_time=0.8)
            self.remove(line1, *line2)
            self.add(line2)
            card.line = line2
            self.play(Indicate(line2, color=IMAGE, scale_factor=1.15), run_time=0.6)

        # ========================================================== 4 · run it: read the prompt
        big = mono_line(C_PROMPT, BIG, INK, t2c=t._prompt_colors(C_PROMPT))
        big.move_to([0, 2.25, 0])
        p_root, p_at = glyph_range(big, 0, 4), glyph_range(big, 4, 5)
        p_id, p_colon = glyph_range(big, 5, 17), glyph_range(big, 17, 18)
        p_slash, p_hash = glyph_range(big, 18, 19), glyph_range(big, 19, 20)
        assert C_PROMPT[5:17] == "f72851da4a58" and C_PROMPT[18] == "/"
        sweep = Arrow([-3.6, 1.82, 0], [3.6, 1.82, 0], buff=0, color=TURN, stroke_width=4,
                      max_tip_length_to_length_ratio=0.05)
        # the picture leaves but the prediction stays: the start-up line moves top right (S04's idiom)
        everything3 = VGroup(card, *card.tiles.values(), *card.notes.values(), lab_ent, lab_cmd, dim)
        said = label("predicted:", 22, S.GREY)
        pred_to = VGroup(said, line2.copy()).arrange(RIGHT, buff=0.25)
        pred_to.move_to([5.9 - pred_to.width / 2, 3.2, 0])
        tick = check_mark(0.36, VENV).next_to(pred_to, RIGHT, buff=0.22)

        with self.voiceover(SAY[4]) as vo:
            clear_with(self, t, FadeOut(everything3, shift=UP * 0.1), extra_caption(self, tr, False),
                       run_time=0.4)
            resize(self, t, 6, run_time=0.45,
                   extra=[line2.animate.move_to(pred_to[1]), FadeIn(said, shift=LEFT * 0.1)])
            c4 = type_cmd(self, t, RUN, 0.6)
            yt4 = beside(turn_tag(), c4.rows[0])
            pin(self, c4.rows[0], yt4, run_time=0.3)
            t.set_prompt(C_PROMPT)
            p4 = bare_prompt(self, t)                    # bash, on its own: as predicted
            self.play(Create(tick), Indicate(line2, color=VENV, scale_factor=1.12),
                      Wiggle(yt4, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.6)
            vo.wait_until("Read it left")
            self.play(TransformFromCopy(p4.glyphs, big.glyphs), run_time=0.8)
            self.play(GrowArrow(sweep), run_time=0.7)
            self.play(FadeOut(sweep), run_time=0.25)
            # the parts move apart (spaced), then each gets its label as it is read
            vo.wait_until("You're root")
            self.play(p_root.animate.shift(LEFT * 0.9), p_at.animate.shift(LEFT * 0.45),
                      p_colon.animate.shift(RIGHT * 0.45), VGroup(p_slash, p_hash).animate.shift(RIGHT * 0.9),
                      run_time=0.5)
            y_u = big.strut.get_bottom()[1] - 0.04
            u_root = under(p_root, TURN, y=y_u)
            u_id = under(p_id, TURN, y=y_u)
            u_slash = under(p_slash, TURN, y=y_u, pad=0.12)
            l_root = part_label("you, the administrator,", "inside the container")
            l_root.next_to(u_root, DOWN, buff=0.18)
            l_id = part_label("the container's ID", "new every run", IMAGE).next_to(u_id, DOWN, buff=0.18)
            l_slash = part_label("the top folder", "of the image").next_to(u_slash, DOWN, buff=0.18)
            self.play(Create(u_root), FadeIn(l_root, shift=DOWN * 0.1),
                      Indicate(p_root, color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("After the at sign")
            self.play(u_root.animate.set_color(S.GREY), Indicate(p_at, color=TURN, scale_factor=1.3),
                      run_time=0.5)
            self.play(Create(u_id), FadeIn(l_id, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("which changes every run")
            self.play(Indicate(p_id, color=IMAGE, scale_factor=1.12), run_time=0.8)
            vo.wait_until("so yours will differ")
            self.play(Indicate(l_id[1], color=TURN, scale_factor=1.15), run_time=0.7)

        # ========================================================== 5 · the slash, and exit
        wd = chip(WORKDIR, S.GREY, size=22, font=MONO)
        no_wd = label("no WORKDIR", 22, S.GREY)
        wd_g = VGroup(wd, no_wd).arrange(RIGHT, buff=0.25)
        wd_g.next_to(l_slash, DOWN, buff=0.25)
        if wd_g.get_right()[0] > 6.4:
            wd_g.shift(LEFT * (wd_g.get_right()[0] - 6.4))

        with self.voiceover(SAY[5]) as vo:
            self.play(u_id.animate.set_color(S.GREY), Create(u_slash), FadeIn(l_slash, shift=DOWN * 0.1),
                      Indicate(p_slash, color=TURN, scale_factor=1.5), run_time=0.7)
            vo.wait_until("because this image")
            self.play(FadeIn(wd_g, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(p_slash, color=TURN, scale_factor=1.6), Indicate(wd, color=TURN, scale_factor=1.1),
                      run_time=0.9)
            vo.wait_until("Type exit")
            istep(self, t, C16.line(2), 0.3)
            t.print(self, EXIT_ECHO, run_time=0.3)
            t.set_prompt(P_LAPTOP)
            p5 = bare_prompt(self, t)
            self.play(Indicate(substring(p5, P_LAPTOP), color=INK, scale_factor=1.05), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
