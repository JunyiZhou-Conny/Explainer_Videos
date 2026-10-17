"""S08 · Step 5: CMD, the solution, the build (README A11 -> A13; V3: the start-up command line).

Beats (script.md "## S08", one voiceover block each):
 0  TRACKER A10 -> A11. CODE(README.md: 163-164) between the tracker and a 5-row strip terminal.
    The strip types `cat Dockerfile` (TRACKER A11 · extra, row tag `extra`) -> laptop/23 lines
    14-15 early in the beat, so the file's new last line stays readable. The panel's `CMD`,
    `"-c"`, `source .venv/bin/activate` and `exec bash` pulse YELLOW as they are said; on "Add it
    at the end" the strip's CMD row (the file's last line) gets a YELLOW bar.
 1  V3. The strip leaves (tracker drops "· extra") and the panel rises; the TEAL config card (S05's
    state: ENTRYPOINT `["/bin/bash"]`, CMD "null") appears under it. The panel's CMD value is copied
    down (TransformFromCopy) into the CMD tile `["-c", "source .venv/bin/activate && exec bash"]`
    (the "null" fades). On "join into one command line" copies of `/bin/bash`, `-c` and the quoted
    string come down from the two tiles and assemble the start-up line
    `/bin/bash -c "source .venv/bin/activate && exec bash"` (the brackets and commas stay behind);
    its three parts pulse as "bash, dash c, then that string" is said. On "On its own" the GREY
    note "bash -c: run this string, then exit" appears under it and pulses on "runs the string".
 2  Card and panel fade, then the start-up line rises to the top (it no longer crosses the card).
    A TEAL bubble "bash 1" appears (its name copied from the line's `/bin/bash`); inside it "runs
    source .venv/bin/activate" (copied from the line) and PATH as a door row: `/usr/local/bin`
    (ORANGE), `…`. "which puts the bin folder": the doors move right and a GREEN
    `/.venv/bin` door forms at the front from the `.venv/bin` of the running command. "Then exec
    bash": `exec bash` underlines in the line, the bubble now runs `exec bash`, and in place
    "bash 1" becomes "bash 2 · interactive" (the 1 rolls over to 2, " · interactive" joins; the
    door row unchanged); "keeps the new PATH": the GREEN door pulses; "gives you a prompt": the
    capture's prompt `root@473b6edd3dab:/#` (laptop/26 line 2) appears with a blinking cursor.
 3  TRACKER A11. Full terminal (12 rows): `docker build -t simple-translate -f Dockerfile .`
    (two rows) + ▶ your turn -> laptop/24 lines 23-24, 26-27, 29, 30 (wrap). On "Again COPY" line
    27 `#7 DONE 0.0s` gets a YELLOW bar, line 29's `RUN uv sync` pulses on "and uv sync"; on "and
    Python downloads again" line 30's `Downloading cpython-3.15.0-…` gets a bar too; on "for one
    added line" the GREY row tag "one line added · part 2 explains" sits beside line 29, pulsing on
    "Part 2 explains why".
 4  The terminal clears; `docker run --rm -ti simple-translate` (two rows) + ▶ your turn -> the
    bare prompt `root@473b6edd3dab:/#`. "No app in parentheses": GREY tag "no (app)" beside the
    prompt, the prompt pulses. "These extra checks" (TRACKER A11 · extra): the tag slides right,
    `which python`, `python --version`, `echo $VIRTUAL_ENV` (laptop/26 lines 2-7, row tags
    `extra` in one column), each output turning GREEN as it is said (`/.venv/bin/python`,
    `Python 3.15.0`, `/.venv`). "The fresh bash set its own prompt": GREY tag "not an error" after
    "no (app)". "The lecture's run command" (the bridge, SLIDES.md Conflict 1): GREY
    `Lecture 2 · slides 64, 75` (lecture_ref, top right, over the 12-row terminal's top edge), then
    the `docker run` command pulses YELLOW; the three GREEN outputs pulse on "and the venv with it".
    "Then type exit": the tag goes, `exit` (line 8) -> line 9; the laptop prompt returns and pulses
    YELLOW on "back to your laptop".
 5  TRACKER A12. The terminal clears to the laptop prompt and shrinks to the 3-row strip; the
    README card (`README.md · lines 167-168`: "Solution Dockerfile:" / `Dockerfile.txt`, 26 pt)
    appears above it; once it lands, GREY `Lecture 2 · slides 57` (lecture_ref, top right, until
    "if yours prints") and, under the card, the GREY note "lecture slide 57: a different version ·
    build this file" (22 pt; SLIDES.md Conflict 2). `Dockerfile.txt` pulses on "Dockerfile.txt".
    "An extra diff" (A12 · extra): the card and its note fade (a full terminal and a picture never
    share the frame; parked top right it sat on the 12-row terminal's top edge), the terminal grows to 12 rows and types `diff Dockerfile
    Dockerfile.txt` (a full row: its `extra` tag stands just above the terminal's top edge, its right
    edge at the command's end, a short GREY leader down to the command; on the next row it read as a
    tag of the first output row) -> laptop/27 lines 8-18, `+` lines GREEN, `-` lines dim RED.
    "if yours prints less-than…": the +/- column pulses and a two-line GREY note appears in the
    empty rows: "our diff prints + and −" / "on a Mac, Linux or Git Bash: diff -u for this layout"
    (`diff -u` pulses YELLOW on "add dash u").
    "First, three ENV lines": the note goes, the three `+ENV` rows pulse, and GREY row tags appear
    one by one as said: "no apt questions", "UTF-8 text", "logs appear at once".
 6  The tags go; the terminal continues -> laptop/27 "…", 20-26, "…", 33-34 (it scrolls: the rows
    that leave fade in place, so nothing flies over the tracker; line 20 is 66 characters, one more
    than a row, so it wraps like a real terminal, its last letter on the next row: the excerpt then
    fills all 12 rows). "one bigger RUN": an ORANGE bracket right of lines 21-26 with "one RUN: /
    update, upgrade, / clean, newer pip, uv"; the rows pulse as they are said. "And ENTRYPOINT moved to the end": a YELLOW bracket at lines
    33-34, "ENTRYPOINT moved to the end"; the ENTRYPOINT row pulses on "the order of ENTRYPOINT".
 7  TRACKER A12. The terminal clears and shrinks to the strip (the laptop prompt); the README card
    fades back in at the centre (26 pt) with the GREY note "the README only names the file" under
    it. "an extra command" (A12 · extra): `cp Dockerfile.txt Dockerfile` (laptop/28: no output;
    the prompt returns). The cp line nearly fills its row, so its `extra` tag stands just above the
    strip's top edge, its right edge at the command's end, with a short GREY leader down to the
    command (as the diff's `extra`; on the prompt row the tags read as tags of the empty prompt);
    later `▶ your turn` joins left of it. `Dockerfile.txt`, then `Dockerfile`, pulse on "copy it
    over yours"; ▶ your turn on "Pause and do that".
 8  TRACKER A13. The README card (`README.md · lines 172-174`: "In a terminal make sure you are the
    location of simple-translate") replaces the first one at the top; the terminal clears and grows
    to 10 rows with the laptop prompt; `simple-translate` pulses in the card and in the prompt.
    "the same build": `docker build -t simple-translate -f Dockerfile .` + ▶ your turn ->
    laptop/29 lines 3 (fit), 9 (cut after `python:3.12-slim-bookworm`; 66 characters, so it folds
    with its `…` on the next row), 13-15 (fit), 22 (fit), the compact view; `simple-translate:latest`
    TEAL; GREY row tag "what your terminal shows". "four steps": `[1/4]`…`[4/4]` pulse; "the apt and
    pip step the slowest": `13.3s` gets a YELLOW bar, `4.9s` a fainter one. Fade out to an empty
    frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer import style as S
from explainer.devops import code_span, lecture_ref
from explainer.scene import VoiceScene

from common import (BUILD, CAT, ERR, IMAGE, INK, LAPTOP_DIR, NARRATION, OUTPUT, P_LAPTOP, ROUTE, RUN,
                    STRIP_ROWS, SYSTEM, TURN, VENV, ConfigCard, PathDoors, bare_prompt,
                    beside, capture, code, cut, fit, glyph_range, hl_bar, istep, label, laptop_term,
                    mono, pin, readme_card, resize, row_tag, steady, substring, track, tracker_a,
                    type_cmd, under, unpin)

SAY = NARRATION["S08"]

DIFF = "diff Dockerfile Dockerfile.txt"
CP = "cp Dockerfile.txt Dockerfile"
VALUE = '["-c", "source .venv/bin/activate && exec bash"]'           # README.md line 164
STARTUP = '/bin/bash -c "source .venv/bin/activate && exec bash"'      # ENTRYPOINT + CMD

# ------------------------------------------------------------------ real outputs (file line numbers)
C23 = capture("23", LAPTOP_DIR)                          # laptop/23-dockerfile-v5.txt
assert C23.cmd == CAT, C23.cmd
CAT_OUT = C23.at((14, 15))                               # the comment + the CMD line (the file's end)
assert CAT_OUT[1] == "CMD " + VALUE, CAT_OUT

C24 = capture("24", LAPTOP_DIR)                          # laptop/24-build-v5.txt
assert C24.cmd == BUILD, C24.cmd
BUILD_OUT = C24.at((23, 24), (26, 27), 29, 30)
assert BUILD_OUT[3] == "#7 DONE 0.0s" and "Downloading cpython-3.15.0" in BUILD_OUT[5], BUILD_OUT

C26 = capture("26", LAPTOP_DIR)                          # laptop/26-run-v5.txt
assert C26.cmd == RUN, C26.cmd
C_PROMPT = C26.istep(2)[0]                               # root@473b6edd3dab:/#
assert C_PROMPT == "root@473b6edd3dab:/#" and C26.istep(8)[1] == "exit", C26.raw
assert C26.at(3, 5, 7, 9) == ["/.venv/bin/python", "Python 3.15.0", "/.venv", "exit"], C26.raw

C27 = capture("27", LAPTOP_DIR)                          # laptop/27-diff-solution.txt
assert C27.cmd == DIFF, C27.cmd
DIFF_A = C27.at((8, 18))                                 # -ENTRYPOINT … three +ENV lines
DIFF_B = C27.at("…", (20, 26), "…", (33, 34))            # the bigger RUN … ENTRYPOINT at the end
assert DIFF_A[2] == "+ENV DEBIAN_FRONTEND=noninteractive" and DIFF_A[10] == "+ENV PYTHONUNBUFFERED=1"
assert DIFF_B[2] == "+RUN set -ex; \\" and DIFF_B[10] == '+ENTRYPOINT ["/bin/bash"]', DIFF_B

C28 = capture("28", LAPTOP_DIR)                          # laptop/28-cp-solution.txt (no output)
assert C28.cmd == CP and not C28.lines and C28.exit == 0, C28.raw

C29 = capture("29", LAPTOP_DIR)                          # laptop/29-build.txt (the compact view)
assert C29.cmd == BUILD, C29.cmd
FINAL_OUT = [fit(C29.line(3)), cut(C29.line(9), "python:3.12-slim-bookworm"),
             *[fit(C29.line(n)) for n in (13, 14, 15, 22)]]
assert "13.3s" in FINAL_OUT[2] and FINAL_OUT[4].endswith("4.9s") and "simple-translate:latest" in FINAL_OUT[5]

# ------------------------------------------------------------------ layout
PANEL_Y0, PANEL_Y1 = 1.13, 2.0       # README panel (10.1 x 1.56): beat 0 (over the 5-row strip), beat 1
CARD_TOP = 1.1                       # the config card (8.8 x 2.63) under the raised panel
LINE_Y = 2.2                         # beat 2: the start-up line at the top
BUBBLE_Y = -0.6                      # beat 2: the bash bubble (8.6 x 3.4)
EXTRA_X = 1.25                       # beat 4: left edge of the `extra` tags of the three checks
DIM_RED = interpolate_color(ManimColor(ERR), ManimColor(S.BG), 0.35)


# ------------------------------------------------------------------ helpers
def turn_tag() -> VGroup:
    """YELLOW '▶ your turn', the height of a terminal row."""
    return row_tag("▶ your turn", TURN)


def xtag() -> VGroup:
    """GREY 'extra' row tag (a command the README doesn't have)."""
    return row_tag("extra")


def at_x(mob, row, x_left: float):
    """Put `mob` on terminal row `row` with its left edge at x_left."""
    return mob.move_to([x_left + mob.width / 2, row.strut.get_center()[1], 0])


def at_right(mob, row, x_right: float = 6.1):
    """Put `mob` on terminal row `row` with its right edge at x_right."""
    return mob.move_to([x_right - mob.width / 2, row.strut.get_center()[1], 0])


def head_tag(t, row, tg) -> VGroup:
    """A row tag for command row `row` (the terminal's first row) when the command fills its row:
    `tg` stands just above the terminal's top edge, its right edge just past the command's end, and
    a short GREY leader drops from it to the command's last characters. Beside the next row it would
    read as a tag of that row. .tag .lead"""
    x_end = row.glyphs.get_right()[0]
    tg.move_to([x_end + 0.1 - tg.width / 2, t.box.get_top()[1] + 0.1 + tg.height / 2, 0])
    x = x_end - 0.09                                  # over the command's last character
    lead = Line([x, tg.get_bottom()[1], 0], [x, row.strut.get_top()[1] + 0.04, 0]).set_stroke(S.GREY, 2)
    g = VGroup(lead, tg)                              # the leader first: the tag's fill covers its top
    g.tag, g.lead = tg, lead
    return g


def show_head_tag(g, *extra) -> AnimationGroup:
    """The tag drops in while its leader draws down to the command."""
    return AnimationGroup(FadeIn(g.tag, shift=DOWN * 0.1), Create(g.lead), *extra)


def bar_on(scene, row, glyphs, color, opacity: float = 0.25):
    """A translucent bar behind `glyphs` of terminal row `row` (part of the row)."""
    b = hl_bar(glyphs, color, opacity)
    row.add_to_back(b)
    scene.add(row)
    return b


def gl(t, s: str, sub: str, occurrence: int = 0) -> VGroup:
    """Glyphs of `sub` in a steady() text `t` built from string `s` (glyph 0 is the hidden strut;
    spaces have no glyphs)."""
    i = -1
    for _ in range(occurrence + 1):
        i = s.index(sub, i + 1)
    a = 1 + len("".join(s[:i].split()))
    return VGroup(*t[a:a + len("".join(sub.split()))])


def bracket_right(rows, x: float, color) -> VMobject:
    """A ']' bracket right of terminal rows, from the first row's top to the last row's bottom."""
    top = rows[0].strut.get_top()[1] - 0.03
    bot = rows[-1].strut.get_bottom()[1] + 0.03
    return VMobject().set_points_as_corners([[x - 0.12, top, 0], [x, top, 0], [x, bot, 0], [x - 0.12, bot, 0]]) \
        .set_stroke(color, 4)


def right_edge(rows) -> float:
    return max(r.glyphs.get_right()[0] for r in rows if len(r.glyphs))


def diff_rows(lines):
    """A diff's lines coloured: '+' GREEN, '-' dim RED, context and '…' as plain output."""
    out = []
    for s in lines:
        if s.startswith("+"):
            out.append((s, VENV))
        elif s.startswith("-"):
            out.append((s, DIM_RED))
        else:
            out.append((s, OUTPUT))
    return out


def card_167(size: float) -> VGroup:
    """README card, lines 167-168: 'Solution Dockerfile:' / `Dockerfile.txt` (body at `size`). .file"""
    body = VGroup(label("Solution Dockerfile:", size, INK), mono("Dockerfile.txt", size, INK))
    body.arrange(DOWN, aligned_edge=LEFT, buff=0.1 if size < 22 else 0.14)
    c = readme_card((167, 168), body)
    c.file = body[1]
    return c


def note_box(lines, size: float = 20) -> VGroup:
    """A GREY note of a few lines (each a list of (text, 'mono'|'label') parts) on an opaque box. .lines"""
    rows = VGroup()
    for parts in lines:
        r = VGroup(*[mono(x, size, S.GREY) if k == "mono" else label(x, size, S.GREY) for x, k in parts])
        r.arrange(RIGHT, buff=0.12, aligned_edge=DOWN)
        rows.add(r)
    rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    b = RoundedRectangle(width=rows.width + 0.4, height=rows.height + 0.26, corner_radius=0.16,
                         stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 0.94)
    rows.move_to(b)
    g = VGroup(b, rows)
    g.box, g.lines = b, rows
    return g


def pulse_tag(tg, color, scale: float = 1.08):
    """Point at a row tag: its text pulses in `color` and its outline flashes (an Indicate on the
    whole tag would also colour its opaque fill)."""
    # box first: the group an AnimationGroup adds to the scene draws its parts in this order, and
    # the box's opaque fill must stay under the text
    return AnimationGroup(tg.box.animate(rate_func=there_and_back).set_stroke(color, width=3),
                          Indicate(tg.text, color=color, scale_factor=scale))


def scroll_in_place(scene, t, n_new: int, run_time: float = 0.4) -> None:
    """Make room for n_new rows: the rows that would scroll off fade where they are (instead of
    flying up over the frame), the rest move up."""
    overflow = len(t.lines) + n_new - t.rows
    if overflow <= 0:
        return
    gone = VGroup(*t.lines.submobjects[:overflow])
    stay = VGroup(*t.lines.submobjects[overflow:])
    # first the rows that leave fade, then the rest move up through the empty rows (moving while
    # the others fade, the kept rows would slide across them)
    scene.play(FadeOut(gone), run_time=run_time / 2)
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * overflow), run_time=run_time / 2)


def clear_with(scene, t, *anims, keep=None, run_time: float = 0.4) -> None:
    """Fade the terminal's lines (all but `keep`) together with other animations."""
    gone = [m for m in t.lines if m is not keep]
    scene.play(FadeOut(VGroup(*gone)), *anims, run_time=run_time)
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)


def blink(scene, cursor, until: float) -> None:
    """Blink `cursor` (0.5 s on, 0.5 s off) until scene time `until`."""
    on = True
    while scene.renderer.time + 0.5 <= until:
        scene.wait(0.45)
        on = not on
        scene.play(cursor.animate.set_opacity(1 if on else 0), run_time=0.1)
    if not on:
        scene.play(cursor.animate.set_opacity(1), run_time=0.1)


# ------------------------------------------------------------------ the scene
class StepCmd(VoiceScene):
    def construct(self):
        assert len(SAY) == 9, f"S08 has {len(SAY)} SAY lines; this scene times 9"

        tr = tracker_a(10)

        # ========================================================== 0 · Step 5: CMD
        panel = code("README.md", 163, 164, "docker")
        panel.move_to([0, PANEL_Y0, 0])
        src = panel.code
        s_cmd = code_span(src, 1, "CMD")
        s_c = code_span(src, 1, '"-c"')
        s_src = code_span(src, 1, "source .venv/bin/activate")
        s_exec = code_span(src, 1, "exec bash")
        s_val = code_span(src, 1, VALUE)
        t = laptop_term(5)                                   # the 5-row strip (top edge -0.63)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.5)
            self.play(track(tr, 11), run_time=0.5)
            self.play(Indicate(VGroup(tr.dots[10], tr.caption), color=TURN, scale_factor=1.12),
                      FadeIn(panel, shift=DOWN * 0.15), FadeIn(t), run_time=0.6)
            c0 = type_cmd(self, t, CAT, 0.45)
            x0 = beside(xtag(), c0)
            pin(self, c0, x0, run_time=0.3, anim=AnimationGroup(FadeIn(x0, shift=LEFT * 0.1),
                                                                track(tr, 11, extra=True)))
            out0 = t.print(self, CAT_OUT, run_time=0.4, lag=0.12)
            vo.wait_until("CMD")
            self.play(Indicate(s_cmd, color=TURN, scale_factor=1.2), run_time=0.45)
            vo.wait_until("It holds dash c")
            self.play(Indicate(s_c, color=TURN, scale_factor=1.25), run_time=0.6)
            vo.wait_until("source the activate")
            self.play(Indicate(s_src, color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("then exec bash")
            self.play(Indicate(s_exec, color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("Add it at the end")
            bar0 = bar_on(self, out0[1], out0[1].glyphs, TURN, 0.25)
            self.play(FadeIn(bar0), Indicate(out0[1].glyphs, color=TURN, scale_factor=1.04), run_time=0.7)

        # ========================================================== 1 · V3: ENTRYPOINT + CMD -> one line
        card = ConfigCard(rows=("ENTRYPOINT", "CMD"), card_w=8.8, inline=False)
        card.shift(UP * (CARD_TOP - card.frame.get_top()[1]))
        ent = card.place("ENTRYPOINT", card.tile('["/bin/bash"]'))
        null = card.note("CMD", "null")
        cmd_tile = card.tile(VALUE)
        card.place("CMD", cmd_tile)
        line = card.startup(STARTUP)
        l_bash, l_c = gl(line, STARTUP, "/bin/bash"), gl(line, STARTUP, "-c")
        l_str = gl(line, STARTUP, '"source .venv/bin/activate && exec bash"')
        e_bash = gl(ent.text, '["/bin/bash"]', "/bin/bash")
        c_c = gl(cmd_tile.text, VALUE, "-c")
        c_str = gl(cmd_tile.text, VALUE, '"source .venv/bin/activate && exec bash"')
        note1 = VGroup(mono("bash -c", 22, S.GREY), label(": run this string, then exit", 22, S.GREY))
        note1.arrange(RIGHT, buff=0.04, aligned_edge=DOWN).next_to(line, DOWN, buff=0.38)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(t), track(tr, 11), panel.animate.move_to([0, PANEL_Y1, 0]), run_time=0.6)
            self.play(FadeIn(VGroup(card, ent, null), shift=UP * 0.1), run_time=0.5)
            self.play(TransformFromCopy(s_val, cmd_tile, path_arc=-0.4), FadeOut(null), run_time=1.0)
            card.notes.pop("CMD")
            vo.wait_until("join into one")
            self.play(TransformFromCopy(e_bash, l_bash), TransformFromCopy(c_c, l_c),
                      TransformFromCopy(c_str, l_str), run_time=1.2)
            self.remove(l_bash, l_c, l_str, *l_bash, *l_c, *l_str)
            self.add(line)
            vo.wait_until("bash, dash c")
            self.play(Indicate(l_bash, color=TURN, scale_factor=1.15), run_time=0.45)
            self.play(Indicate(l_c, color=TURN, scale_factor=1.4), run_time=0.45)
            vo.wait_until("then that string")
            self.play(Indicate(l_str, color=TURN, scale_factor=1.03), run_time=0.8)
            vo.wait_until("On its own")
            self.play(FadeIn(note1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("runs the string")
            self.play(Indicate(note1, color=INK, scale_factor=1.06), run_time=0.8)

        # ========================================================== 2 · source, then exec bash
        bubble = RoundedRectangle(width=8.6, height=3.4, corner_radius=0.35, stroke_color=IMAGE,
                                  stroke_width=3).set_fill(IMAGE, 0.06)
        bubble.move_to([0, BUBBLE_Y, 0])
        b_top, b_left, b_right = bubble.get_top()[1], bubble.get_left()[0], bubble.get_right()[0]
        name1 = steady("bash 1", 24, IMAGE)
        name1.move_to([b_left + 0.4 + name1.width / 2, b_top - 0.45, 0])
        name2 = steady("bash 2 · interactive", 24, IMAGE)
        name2.move_to(name1, aligned_edge=LEFT)
        SRC = "source .venv/bin/activate"
        runs_w = label("runs", 22, S.GREY)
        runs_src = mono(SRC, 22, INK)
        runs1 = VGroup(runs_w, runs_src).arrange(RIGHT, buff=0.18, aligned_edge=DOWN)
        runs1.move_to([b_right - 0.4 - runs1.width / 2, name1.get_center()[1], 0])
        runs_exec = mono("exec bash", 22, INK)
        runs_exec.move_to(runs_src, aligned_edge=RIGHT)
        runs_w2 = runs_w.copy().next_to(runs_exec, LEFT, buff=0.18, aligned_edge=DOWN)
        prompt2 = mono(C_PROMPT, 22, INK)
        cursor = Rectangle(width=0.15, height=0.32, stroke_width=0).set_fill(INK, 1)
        prompt_g = VGroup(prompt2, cursor).arrange(RIGHT, buff=0.12)
        prompt_g.move_to([b_right - 0.4 - prompt_g.width / 2, name1.get_center()[1], 0])
        path_l = mono("PATH", 22, ROUTE)
        doors = PathDoors(["/usr/local/bin", "…"], colors={"/usr/local/bin": SYSTEM}, door_h=1.1)
        path_l.move_to([b_left + 0.45 + path_l.width / 2, BUBBLE_Y - 0.35, 0])
        doors.next_to(path_l, RIGHT, buff=0.35)
        doors.shift(UP * (path_l.get_center()[1] - doors.doors[0].frame.get_center()[1]))
        venv_door = doors._door("/.venv/bin", VENV)
        venv_door.align_to(doors.doors[0].frame, UP).align_to(doors.doors[0].frame, LEFT)
        slide = RIGHT * (venv_door.frame.width + doors.gap)
        venv_src = substring_of(runs_src, SRC, ".venv/bin")
        l_src = gl(line, STARTUP, "source .venv/bin/activate")
        l_exec = gl(line, STARTUP, "exec bash")
        top_line = line.copy().move_to([0, LINE_Y, 0])
        u_src = under(gl(top_line, STARTUP, "source .venv/bin/activate"), VENV)
        u_exec = under(gl(top_line, STARTUP, "exec bash"), TURN)

        with self.voiceover(SAY[2]) as vo:
            # first the card and the panel go, then the line rises through the empty room (it would
            # otherwise cross the fading card)
            self.play(FadeOut(VGroup(card, ent, cmd_tile, note1, panel)), run_time=0.4)
            self.play(line.animate.move_to([0, LINE_Y, 0]), run_time=0.5)
            self.play(Create(bubble), TransformFromCopy(VGroup(*l_bash[-4:]), name1), run_time=0.8)
            self.play(Create(u_src), FadeIn(runs_w), TransformFromCopy(l_src, runs_src), run_time=0.8)
            self.play(FadeIn(path_l), FadeIn(doors, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("which puts the bin folder")
            self.play(doors.doors.animate.shift(slide), run_time=0.45)
            self.play(FadeIn(VGroup(venv_door.frame, venv_door[1])),
                      TransformFromCopy(venv_src, venv_door.label), run_time=0.8)
            self.remove(venv_door.frame, venv_door[1], venv_door.label)
            self.add(venv_door)
            self.play(Indicate(venv_door, color=VENV, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Then exec bash")
            self.play(FadeOut(u_src), Create(u_exec), FadeOut(runs_src, shift=UP * 0.2),
                      TransformFromCopy(l_exec, runs_exec), Transform(runs_w, runs_w2), run_time=0.7)
            # the same bubble, a new bash: "bash" stays, the 1 rolls over to 2, " · interactive" joins
            # (a letter-by-letter Transform of the whole name scrambles it for most of a second)
            self.play(FadeOut(name1[5], shift=UP * 0.25), FadeIn(name2[5], shift=UP * 0.25),
                      Indicate(bubble, color=IMAGE, scale_factor=1.02), run_time=0.5)
            self.play(FadeIn(VGroup(*name2[6:]), shift=LEFT * 0.15), run_time=0.4)
            self.remove(name1, *name1)
            self.add(name2)
            name1 = name2
            vo.wait_until("that keeps the new PATH")
            self.play(Indicate(path_l, color=ROUTE, scale_factor=1.15),
                      Indicate(venv_door, color=VENV, scale_factor=1.1), run_time=0.8)
            vo.wait_until("and gives you a prompt")
            self.play(FadeOut(VGroup(runs_w, runs_exec), shift=UP * 0.2), FadeIn(prompt_g, shift=UP * 0.2),
                      run_time=0.5)
            blink(self, cursor, vo.start + vo.duration - 0.1)

        picture2 = VGroup(line, u_exec, bubble, name1, path_l, doors, venv_door, prompt_g)

        # ========================================================== 3 · build again
        t = laptop_term(12)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(picture2), FadeIn(t), run_time=0.45)
            c3 = type_cmd(self, t, BUILD, 0.65)
            yt3 = beside(turn_tag(), c3.rows[-1])
            pin(self, c3.rows[-1], yt3, run_time=0.25)
            self.play(Wiggle(yt3, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.5)
            vo.wait_until("Again COPY")
            t.print(self, BUILD_OUT, run_time=0.4, wrap=True, lag=0.1)
            r27 = t.find("#7 DONE")
            bar27 = bar_on(self, r27, r27.glyphs, TURN, 0.28)
            self.play(FadeIn(bar27), Indicate(r27.glyphs, color=TURN, scale_factor=1.12), run_time=0.55)
            vo.wait_until("and uv sync")
            r29 = t.find("#8 [4/4] RUN uv sync")
            self.play(Indicate(substring(r29, "RUN uv sync"), color=TURN, scale_factor=1.1), run_time=0.5)
            vo.wait_until("and Python downloads")
            r30 = t.find("Downloading cpython")
            g30 = substring(r30, "Downloading cpython-3.15.0-linux-x86_64-gnu")
            bar30 = bar_on(self, r30, g30, TURN, 0.28)
            self.play(FadeIn(bar30), Indicate(g30, color=TURN, scale_factor=1.05), run_time=0.7)
            vo.wait_until("for one added line")
            n3 = beside(row_tag("one line added · part 2 explains"), r29)
            pin(self, r29, n3, run_time=0.4)
            vo.wait_until("Part 2 explains")
            self.play(pulse_tag(n3, INK, 1.04), run_time=0.7)

        # ========================================================== 4 · run: the venv is active, no (app)
        with self.voiceover(SAY[4]) as vo:
            unpin(self, [(c3.rows[-1], yt3), (r29, n3)], 0.25)
            clear_with(self, t, run_time=0.3)
            c4 = type_cmd(self, t, RUN, 0.6)
            t.set_prompt(C_PROMPT)
            p4 = bare_prompt(self, t)
            yt4 = beside(turn_tag(), c4.rows[-1])
            pin(self, c4.rows[-1], yt4, run_time=0.25)
            self.play(Wiggle(yt4, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.5)
            vo.wait_until("No app in parentheses")
            noapp = row_tag([("no ", "label"), ("(app)", "mono")])
            at_x(noapp, p4, p4.glyphs.get_right()[0] + 0.45)
            self.play(FadeIn(noapp, shift=LEFT * 0.1), Indicate(p4.glyphs, color=INK, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("is the venv active")
            self.play(pulse_tag(noapp, TURN), run_time=0.7)
            vo.wait_until("These extra checks")
            self.play(noapp.animate.move_to([EXTRA_X + 0.96 + 0.2 + noapp.width / 2, noapp.get_center()[1], 0]),
                      track(tr, 11, extra=True), run_time=0.4)
            checks = []
            for k, (n_cmd, n_out) in enumerate(((2, 3), (4, 5), (6, 7))):
                r = istep(self, t, C26.line(n_cmd), 0.4)
                xk = at_x(xtag(), r, EXTRA_X)
                self.play(FadeIn(xk, shift=LEFT * 0.1), run_time=0.2)
                out = t.print(self, C26.at(n_out), run_time=0.25)[0]
                checks.append((r, xk, out))
                phrase = ("which python points", "it's 3", "and the virtual env")[k]
                vo.wait_until(phrase)
                self.play(out.glyphs.animate.set_color(VENV), run_time=0.25)
                self.play(Indicate(out.glyphs, color=VENV, scale_factor=1.12), run_time=0.5)
            vo.wait_until("The fresh bash")
            nae = row_tag("not an error")
            nae.next_to(noapp, RIGHT, buff=0.2)
            self.play(FadeIn(nae, shift=LEFT * 0.1), pulse_tag(noapp, INK), run_time=0.6)
            vo.wait_until("The lecture's run command")
            lref4 = lecture_ref(2, "64, 75")                 # top right, over the terminal's top edge
            assert lref4.get_bottom()[1] > t.get_top()[1] + 0.1, (lref4.get_bottom(), t.get_top())
            self.play(FadeIn(lref4), run_time=0.5)
            # our run command pulses as "run command" is said (the lecture's adds a flag to it); without
            # it nothing would move for ~4.5 s until "and the venv with it"
            run4 = VGroup(substring(c4.rows[0], "docker run --rm"), substring(c4.rows[1], "-ti simple-translate"))
            self.play(Indicate(run4, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("and the venv with it")
            self.play(*[Indicate(o.glyphs, color=TURN, scale_factor=1.08) for _, _, o in checks], run_time=0.8)
            vo.wait_until("Then type exit")
            self.play(FadeOut(lref4), run_time=0.2)
            istep(self, t, C26.line(8), 0.25)
            t.print(self, C26.at(9), run_time=0.25)
            t.set_prompt(P_LAPTOP)
            p4b = bare_prompt(self, t)
            vo.wait_until("back to your laptop")
            self.play(Indicate(p4b.glyphs, color=TURN, scale_factor=1.06), run_time=0.8)

        # ========================================================== 5 · the solution file: diff (ENV)
        card_c = card_167(26)
        card_c.move_to([0, 0.75, 0])
        note5 = note_box([[("our diff prints + and −", "label")],
                          [("on a Mac, Linux or Git Bash:", "label"), ("diff -u", "mono"),
                           ("for this layout", "label")]])
        note5_diffu = note5.lines[1][1]
        env_tags = ["no apt questions", "UTF-8 text", "logs appear at once"]
        lref5 = lecture_ref(2, "57")                         # top right, above the diff's `extra` tag
        note57 = label("lecture slide 57: a different version · build this file", 22, S.GREY)
        note57.next_to(card_c, DOWN, buff=0.25)              # between the card and the strip

        with self.voiceover(SAY[5]) as vo:
            marks4 = [noapp, nae] + [x for _, x, _ in checks]
            unpin(self, [(c4.rows[-1], yt4)], 0.3, *[FadeOut(m) for m in marks4], track(tr, 12))
            resize(self, t, STRIP_ROWS, keep=[p4b], extra=[FadeIn(card_c, shift=UP * 0.1)], run_time=0.7)
            assert note57.get_bottom()[1] > t.get_top()[1] + 0.2, (note57.get_bottom(), t.get_top())
            self.play(FadeIn(lref5), FadeIn(note57, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Dockerfile.txt")
            self.play(Indicate(card_c.file, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("An extra diff")
            # a full terminal and a picture never share the frame: the card goes while the terminal grows
            # (parked top right it sat on the 12-row terminal's top edge); it returns in beat 7
            resize(self, t, 12, extra=[FadeOut(card_c, shift=UP * 0.15), FadeOut(note57, shift=UP * 0.15),
                                       track(tr, 12, extra=True)], run_time=0.7)
            c5 = type_cmd(self, t, DIFF, 0.6)
            # the command fills its row: the tag stands above the terminal, a leader down to the command
            x5 = head_tag(t, c5, xtag())
            pin(self, c5, x5, run_time=0.3, anim=show_head_tag(x5))
            out5 = t.print(self, diff_rows(DIFF_A), run_time=0.6, lag=0.06)
            vo.wait_until("if yours prints")
            pm = VGroup(*[glyph_range(r, 0, 1) for r in out5 if r.text[:1] in "+-"])
            at_right(note5, out5[4])                     # over rows 11-13 (all short)
            self.play(*[Indicate(g, color=TURN, scale_factor=1.6) for g in pm], FadeOut(lref5), run_time=0.8)
            self.play(FadeIn(note5, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("add dash u")
            self.play(Indicate(note5_diffu, color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("First, three")
            env_rows = [t.find("+ENV DEBIAN"), t.find("+ENV LANG"), t.find("+ENV PYTHONUNBUFFERED")]
            self.play(FadeOut(note5), run_time=0.3)
            self.play(*[Indicate(r.glyphs, color=VENV, scale_factor=1.06) for r in env_rows], run_time=0.8)
            env_marks = []
            for r, s, phrase in zip(env_rows, env_tags, ("no questions from apt", "a UTF-8 locale",
                                                         "and unbuffered logs")):
                vo.wait_until(phrase)
                m = at_x(row_tag(s), r, 0.85)
                pin(self, r, m, run_time=0.35)
                self.play(Indicate(substring(r, r.text[5:r.text.index("=")]), color=INK, scale_factor=1.1),
                          run_time=0.5)
                env_marks.append((r, m))

        # ========================================================== 6 · one bigger RUN, ENTRYPOINT moved
        with self.voiceover(SAY[6]) as vo:
            unpin(self, [(c5, x5), *env_marks], 0.25)
            # line 20 is one character wider than a row: it wraps (wrap=True), so count its rows
            n6 = sum(max(1, -(-len(s) // t.max_chars)) for s in DIFF_B)
            scroll_in_place(self, t, n6, run_time=0.6)
            out6 = t.print(self, diff_rows(DIFF_B), run_time=0.5, wrap=True, lag=0.05)
            assert len(out6) == n6 <= t.rows, (len(out6), n6)
            i21 = next(i for i, r in enumerate(out6) if r.text.startswith("+RUN set -ex"))
            run_rows = list(out6[i21:i21 + 6])               # lines 21-26
            ep_rows = list(out6[-2:])                        # lines 33-34
            assert ep_rows[1].text == DIFF_B[-1], ep_rows[1].text
            xb = right_edge(run_rows) + 0.22
            br_run = bracket_right(run_rows, xb, SYSTEM)
            lab_run = VGroup(label("one RUN:", 20, SYSTEM), label("update, upgrade,", 20, S.GREY),
                             label("clean, newer pip, uv", 20, S.GREY)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            lab_run.next_to(br_run, RIGHT, buff=0.18)
            xe = right_edge(ep_rows) + 0.22
            br_ep = bracket_right(ep_rows, xe, TURN)
            lab_ep = VGroup(mono("ENTRYPOINT", 22, TURN), label("moved to the end", 22, TURN))
            lab_ep.arrange(RIGHT, buff=0.14, aligned_edge=DOWN).next_to(br_ep, RIGHT, buff=0.2)
            vo.wait_until("one bigger RUN")
            self.play(Create(br_run), FadeIn(lab_run[0], shift=LEFT * 0.1),
                      Indicate(run_rows[0].glyphs, color=SYSTEM, scale_factor=1.08), run_time=0.6)
            vo.wait_until("update and upgrade")
            self.play(FadeIn(lab_run[1], shift=LEFT * 0.1),
                      *[Indicate(r.glyphs, color=SYSTEM, scale_factor=1.06) for r in run_rows[1:3]],
                      run_time=0.8)
            vo.wait_until("clean up")
            self.play(Indicate(run_rows[3].glyphs, color=SYSTEM, scale_factor=1.06), run_time=0.6)
            vo.wait_until("upgrade pip")
            self.play(FadeIn(lab_run[2], shift=LEFT * 0.1),
                      Indicate(run_rows[4].glyphs, color=SYSTEM, scale_factor=1.04), run_time=0.6)
            vo.wait_until("and install uv")
            self.play(Indicate(run_rows[5].glyphs, color=SYSTEM, scale_factor=1.08), run_time=0.6)
            vo.wait_until("And ENTRYPOINT moved")
            self.play(Create(br_ep), FadeIn(lab_ep, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("the order of ENTRYPOINT")
            self.play(Indicate(ep_rows[1].glyphs, color=TURN, scale_factor=1.1), run_time=0.8)

        # ========================================================== 7 · cp the solution over yours (extra)
        card_c2 = card_167(26).move_to([0, 1.25, 0])
        note7 = label("the README only names the file", 24, S.GREY).next_to(card_c2, DOWN, buff=0.4)

        with self.voiceover(SAY[7]) as vo:
            clear_with(self, t, FadeOut(VGroup(br_run, lab_run, br_ep, lab_ep)), track(tr, 12), run_time=0.4)
            resize(self, t, STRIP_ROWS, extra=[FadeIn(card_c2, shift=DOWN * 0.15)], run_time=0.7)
            bare_prompt(self, t)
            self.play(FadeIn(note7, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("So here's the quickest")
            self.play(Indicate(card_c2.file, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("an extra command")
            c7 = type_cmd(self, t, CP, 0.55)
            bare_prompt(self, t)
            # the cp line nearly fills its row: its tags stand above the strip, a leader down to the
            # command (as the diff's `extra` in beat 5); beside the next row they'd tag the empty prompt
            x7 = head_tag(t, c7, xtag())
            pin(self, c7, x7, run_time=0.3, anim=show_head_tag(x7, track(tr, 12, extra=True)))
            vo.wait_until("copy it over yours")
            self.play(Indicate(substring(c7, "Dockerfile.txt"), color=TURN, scale_factor=1.12), run_time=0.6)
            self.play(Indicate(substring(c7, "Dockerfile", 1), color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Pause and do that")
            yt7 = turn_tag().next_to(x7.tag, LEFT, buff=0.2)
            pin(self, c7, yt7, run_time=0.3)
            self.play(Wiggle(yt7, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.6)

        # ========================================================== 8 · Build Docker Image: the compact view
        body8 = VGroup(label("In a terminal make sure you are the location of", 22, INK),
                       mono("simple-translate", 22, INK)).arrange(RIGHT, buff=0.14, aligned_edge=DOWN)
        card8 = readme_card((172, 174), body8).move_to([0, 2.22, 0])

        with self.voiceover(SAY[8]) as vo:
            unpin(self, [(c7, x7), (c7, yt7)], 0.25, FadeOut(note7), FadeOut(card_c2, shift=UP * 0.1))
            clear_with(self, t, track(tr, 13), FadeIn(card8, shift=DOWN * 0.1), run_time=0.5)
            resize(self, t, 10, run_time=0.6)
            p8 = bare_prompt(self, t)
            vo.wait_until("from the simple-translate")
            self.play(Indicate(body8[1], color=TURN, scale_factor=1.06),
                      Indicate(substring(p8, "~/simple-translate"), color=TURN, scale_factor=1.12), run_time=0.9)
            vo.wait_until("the same build")
            c8 = type_cmd(self, t, BUILD, 0.7)
            vo.wait_until("Pause and run it")
            yt8 = beside(turn_tag(), c8.rows[-1])
            pin(self, c8.rows[-1], yt8, run_time=0.25)
            self.play(Wiggle(yt8, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.5)
            vo.wait_until("This compact view")
            t.print(self, FINAL_OUT, run_time=0.6, wrap=True, lag=0.08)
            r22 = t.find("naming to")
            r14 = t.find("[3/4] COPY")
            wy = at_x(row_tag("what your terminal shows"), r14, r14.glyphs.get_right()[0] + 0.5)
            self.play(substring(r22, "simple-translate:latest").animate.set_color(IMAGE),
                      FadeIn(wy, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("four steps")
            steps = VGroup(*[substring(t.find(f"[{k}/4]"), f"[{k}/4]") for k in (1, 2, 3, 4)])
            self.play(*[Indicate(g, color=TURN, scale_factor=1.2) for g in steps], run_time=0.8)
            vo.wait_until("the apt and pip step")
            r13, r15 = t.find("[2/4] RUN"), t.find("[4/4] RUN uv sync")
            g13, g15 = substring(r13, "13.3s"), substring(r15, "4.9s")
            b13 = bar_on(self, r13, g13, TURN, 0.3)
            self.play(FadeIn(b13), Indicate(g13, color=TURN, scale_factor=1.3), run_time=0.7)
            b15 = bar_on(self, r15, g15, TURN, 0.15)
            self.play(FadeIn(b15), Indicate(g15, color=TURN, scale_factor=1.15), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)


def substring_of(text_mob, s: str, sub: str) -> VGroup:
    """Glyphs of `sub` in a plain mono()/label() Text built from `s` (no hidden strut)."""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    return VGroup(*text_mob[a:a + len("".join(sub.split()))])
