"""S03 · Clone: five folders, no Dockerfile (README › Clone this Repository steps 1-2, then
transcribe_audio step 1, and a first look at transcribe_audio/cli.py).

Beats (script.md "## S03", one voiceover block each):
 0  TRACKER R1 (its dot pulses). The house terminal (12 rows, title laptop, student@laptop:~$)
    types `git clone https://github.com/dlops-io/mega-pipeline.git` (two rows) -> 03-clone.txt
    line 2. A one-line README chip "README.md · lines 32–34" sits in the top band right of the
    tracker; on "copied from the README" it flashes YELLOW and "copy it from here" writes in
    beside it. ▶ your turn on "and pause".
 1  TRACKER R2. `cd mega-pipeline` -> (no output); the bare prompt student@laptop:~/mega-pipeline$
    returns and its new path part flashes BLUE. TRACKER R2 · extra; the chip leaves.
    `ls; git log --oneline -1; git branch` (extra; folds after "-1;") -> 04-ls.txt lines 2-11
    (rows that scroll away fade in place: nothing slides over the title bar). GREY bars on the
    five folder names, then on `* main` (line 11), then on `c6bbc9b` (line 10, cut with …) with
    the GREY tag "the commit in this video" over that row's cut end.
 2  `ls -a transcribe_audio generate_text synthesis_audio_en translate_text synthesis_audio`
    (extra, tagged on its first row; two rows, the second indented 2 spaces so that it fits)
    -> `…`; the terminal shrinks to the 3-row strip while the listing of 05-ls-components.txt
    lines 2-42 (parsed from the capture, never retyped) appears above it: at left the full
    transcribe_audio/ tree (22 pt), at right, level with the tree's entries, four one-line rows
    saying only how each other folder differs (20 pt). README.md, cli.py and secrets/ get GREY
    bars as named; a dashed GREY ghost Dockerfile draws in as the tree's last row with the GREY
    caption "none of the five has a Dockerfile" under the rows; then YELLOW "you write it" +
    GREY "README.md · line 114" beside the ghost.
 3  The two "same" rows dim. In the generate_text/ row, pyproject.toml and main.py get YELLOW
    bars as named and "no .gitignore" a YELLOW tag "keep in mind"; in the synthesis_audio/ row,
    cli_11.py gets a GREY tag "bonus".
 4  The listing fades and the terminal grows back to 12 rows. The tracker switches to
    "README › transcribe_audio" (13 dots, step 1); its dot and caption pulse on "whose step 1";
    `cd transcribe_audio` -> (no output), the prompt becomes
    student@laptop:~/mega-pipeline/transcribe_audio$. ▶ your turn on "Pause".
 5  The terminal shrinks to the strip (the cd line and the new prompt). CODE(transcribe_audio/
    cli.py: 4-12) top-left: GREY bracket + tag "comes with Python" on lines 4-8 (and a bare GREY
    bracket on line 12, tempfile, also standard library); the two `google.cloud` and `ffmpeg`
    turn PINK and get PINK underlines (Monokai's keywords are pink too) under a PINK bracket on
    9-11; its tag "where from? · part 2" on "Part 2".
 6  The panel scrolls to CODE(cli.py: 18-21) (· comment cut; 28 pt, room for three tags): BLUE
    bracket + tag "the bucket" (18), BLUE bracket + tag "its two drawers" (19-20), YELLOW bar on
    21 with `group_name` YELLOW, then a YELLOW bracket + tag "you'll change this".
 7  The panel scrolls to CODE(cli.py: 118-126): `def main` gets a YELLOW bar; YELLOW badges
    1 download, 2 transcribe, 3 upload beside lines 121-122, 123-124, 125-126 as each verb is
    said. Everything fades: empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (code_span, file_glyph, file_tree, label, line_bar, line_pitch, mono,
                              mono_line, step_badge, substring, tag)
from explainer.scene import VoiceScene

from common import (CAPTION, CLOUD, COMPONENTS, INK, LAPTOP, LOOKUP, NARRATION, P_A, P_HOME, P_REPO,
                    TERM_BG, TURN, bare_prompt, beside, capture, caption_extra, extra_tag, readme_chip,
                    resize, sans, src_panel, switch_section, term, tracker, type_cmd, your_turn)

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ commands and captures
CLONE = capture("03-clone")
assert CLONE.cmd == "git clone https://github.com/dlops-io/mega-pipeline.git", CLONE.cmd
CLONE_OUT = CLONE.at(2)                                   # Cloning into 'mega-pipeline'...
CD_REPO = "cd mega-pipeline"                              # README.md:34, no output
LS = capture("04-ls")
assert LS.cmd == "ls; git log --oneline -1; git branch", LS.cmd
LS_OUT = LS.at((2, 11))
COMMIT = LS.line(10).split()[0]
assert COMMIT == "c6bbc9b" and LS.line(11) == "* main", (COMMIT, LS.line(11))
LSA = capture("05-ls-components")
assert LSA.cmd == "ls -a " + " ".join(COMPONENTS), LSA.cmd
CD_A = "cd transcribe_audio"                              # transcribe_audio/README.md:13, no output
CLI = "transcribe_audio/cli.py"


def listing(cap) -> dict:
    """`ls -a a b c` output (folder headers "name:", blank separators) -> {folder: [entries]},
    without "." and ".."."""
    out, cur = {}, None
    for s in cap.lines:
        if s.endswith(":"):
            cur = s[:-1]
            out[cur] = []
        elif s and s not in (".", ".."):
            out[cur].append(s)
    return out


FOLDERS = listing(LSA)                                    # 05-ls-components.txt lines 2-42
assert set(FOLDERS) == set(COMPONENTS), FOLDERS
assert not any("Dockerfile" in e for v in FOLDERS.values() for e in v)
A_FILES = FOLDERS["transcribe_audio"]
assert A_FILES == [".gitignore", "README.md", "cli.py", "secrets"], A_FILES
_base = set(A_FILES)
EXTRA = {c: [e for e in FOLDERS[c] if e not in _base] for c in COMPONENTS[1:]}
MISSING = {c: [e for e in A_FILES if e not in FOLDERS[c]] for c in COMPONENTS[1:]}
# the differences the rows state (script.md S03), checked against the capture
assert sorted(EXTRA["generate_text"]) == ["main.py", "pyproject.toml"] and \
    MISSING["generate_text"] == [".gitignore"], (EXTRA, MISSING)
assert EXTRA["synthesis_audio"] == ["cli_11.py"] and not MISSING["synthesis_audio"]
for _c in ("synthesis_audio_en", "translate_text"):
    assert not EXTRA[_c] and not MISSING[_c], _c

# ------------------------------------------------------------------ layout
X0 = -6.3                  # left edge of the code panels
PANEL_TOP = 2.75           # top of a code panel (the tracker band ends at 2.92)
TREE_PT = 22
ROW_PT = CAPTION           # the four difference rows (20 pt)
TREE_X = -6.45             # left edge of the transcribe_audio/ tree (beat 2)
ROWS_X = -2.75             # left edge of the difference rows (level with the tree's entries)
WORD_PT = CAPTION + 2      # the sans words between the names of a row ("+", "same", ", no")


# ------------------------------------------------------------------ small helpers
def place(m, left=None, top=None, cy=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if cy is not None:
        m.set_y(cy)
    return m


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line`, so they scroll and fade with it
    (pin() without its own animation, for mobs shown in a shared play)."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def unstick(scene, line, mob):
    """The reverse of stick(): mob leaves terminal row `line` and is a scene member again."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    if mob in row.submobjects:
        row.remove(mob)
    scene.add(mob)
    return mob


def hl(mob, color=LAPTOP, opacity=0.3, pad_x=0.06, pad_y=0.05) -> Rectangle:
    """A translucent bar over `mob` (a terminal word, a file name)."""
    return Rectangle(width=mob.width + 2 * pad_x, height=mob.height + 2 * pad_y,
                     stroke_width=0).set_fill(color, opacity).move_to(mob)


def row_bar(line, sub, color=LAPTOP, opacity=0.3) -> Rectangle:
    """A bar over substring `sub` of a terminal row, as tall as the row's strut."""
    g = substring(line, sub)
    h = line.strut.height * 0.92
    return Rectangle(width=g.width + 0.12, height=h, stroke_width=0).set_fill(color, opacity) \
        .move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def make_room(scene, t, n_new, run_time=0.45):
    """Scroll before n_new rows arrive, like Terminal's own scroll, except that the rows that
    leave fade where they are first (they never slide up over the title bar), then the rest
    move up."""
    overflow = len(t.lines) + n_new - t.rows
    if overflow <= 0:
        return
    gone = VGroup(*t.lines.submobjects[:overflow])
    stay = VGroup(*t.lines.submobjects[overflow:])
    scene.play(FadeOut(gone), run_time=run_time * 0.4)
    for m in gone:
        t.lines.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * overflow), run_time=run_time * 0.6)


def late(start=0.6):
    """A rate function that waits until `start` of the run, then eases in (a fade that begins
    once a shrinking terminal has left the room)."""
    return lambda a: smooth(min(1.0, max(0.0, (a - start) / (1 - start))))


def type_folded(scene, t, cmd, rows, type_time=None):
    """type_cmd with the fold given explicitly (rows of the prompt + command, each ending in
    ' \\' but the last; they must join back to exactly the command)."""
    p = t.prompt + " "
    assert " ".join(r[:-2] if r.endswith(" \\") else r for r in rows).split() == \
        (p + cmd).split(), rows
    assert all(len(r) <= t.max_chars for r in rows), [len(r) for r in rows]
    t.fold = lambda text, first_prefix=0: list(rows)       # this one call only
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


def cl(p, n):
    """The glyphs of file line n in code panel p."""
    return p.code.code_lines[n - p.first]


def span(p, n, sub, occurrence=0):
    return code_span(p.code, n - p.first, sub, occurrence)


def bar(p, n, color=TURN, opacity=0.16):
    return line_bar(p.code, n - p.first, color, opacity)


def lines_span(p, a, b, pad=-0.02):
    """(top, bottom) y of file lines a..b of panel p (a slightly negative pad keeps the
    brackets of adjacent lines apart)."""
    g = VGroup(*[cl(p, n) for n in range(a, b + 1) if len(cl(p, n))])
    return g.get_top()[1] + pad, g.get_bottom()[1] - pad


def bracket(top, bottom, x, color, tick=0.14) -> VMobject:
    """A thin ']' from top to bottom at x, ticks pointing left (at the code)."""
    return VMobject().set_points_as_corners(
        [[x - tick, top, 0], [x, top, 0], [x, bottom, 0], [x - tick, bottom, 0]]).set_stroke(color, 3)


def side(p, a, b, color, text=None, x=None):
    """A bracket on lines a..b right of panel p, and (optionally) a tag right of it."""
    t, bt = lines_span(p, a, b)
    x = p.code.get_right()[0] + 0.25 if x is None else x
    br = bracket(t, bt, x, color)
    if text is None:
        return br, None
    tg = tag(text, color).next_to(br, RIGHT, buff=0.18)
    return br, tg


_FLAT = set("acemnorsuvwxz")             # glyphs that sit on the baseline, no ascender


def base_line(glyphs, s, color=LOOKUP, drop=0.05) -> Line:
    """An underline just under the baseline of `glyphs` (the code is set tight: an underline
    under the descenders would touch the next line)."""
    i = next(k for k, ch in enumerate(s.replace(" ", "")) if ch in _FLAT)
    y = glyphs[i].get_bottom()[1] - drop
    return Line([glyphs.get_left()[0], y, 0], [glyphs.get_right()[0], y, 0], color=color,
                stroke_width=3.5)


def scroll(scene, old, new, dist=0.35, run_time=0.8):
    """Swap one code panel (with everything in `old`) for the next, as if scrolling down."""
    scene.play(FadeOut(old, shift=UP * dist), run_time=run_time * 0.45)
    scene.play(FadeIn(new, shift=UP * dist), run_time=run_time * 0.55)


# ------------------------------------------------------------------ the listing (beat 2)
def ghost_row(name: str, size: float) -> VGroup:
    """A dashed GREY file row in the tree's style (a file that doesn't exist yet). .glyph .name_text"""
    g = file_glyph(0.3, LAPTOP)
    dashed = DashedVMobject(g[0], num_dashes=18).set_stroke(LAPTOP, 2)
    t = mono_line(name, size, LAPTOP)
    t.next_to(dashed, RIGHT, buff=0.14)
    dashed.match_y(t.strut)
    row = VGroup(dashed, t)
    row.glyph, row.name_text = dashed, t
    return row


def build_tree():
    """transcribe_audio/ and its four entries (05-ls-components.txt lines 28-34; `secrets` is a
    folder), and a ghost Dockerfile row under them (not added to the tree)."""
    entries = ["transcribe_audio/"] + [f"  {e}/" if e == "secrets" else f"  {e}" for e in A_FILES]
    tree = file_tree(entries, size=TREE_PT,
                     colors={"transcribe_audio/": LAPTOP, "secrets/": LAPTOP})
    for r in tree.rows:
        r.name_text.glyphs.set_color(INK)
    place(tree, left=TREE_X, top=2.6)
    pitch = line_pitch(TREE_PT) + 0.1
    last = tree.rows[-1]
    ghost = ghost_row("Dockerfile", TREE_PT)
    ghost.shift(np.array([tree.rows[1].glyph.get_left()[0] - ghost.glyph.get_left()[0],
                          last.name_text.strut.get_center()[1] - pitch
                          - ghost.name_text.strut.get_center()[1], 0]))
    return tree, ghost


def _flat(text_mob, s: str):
    """(baseline y, x-height) of a Text built from s, read off its first flat glyph."""
    chars = s.replace(" ", "")
    for i, ch in enumerate(chars):
        if ch in _FLAT:
            g = text_mob[i]
            return g.get_bottom()[1], g.height
    raise ValueError(f"no flat glyph in {s!r}")


def diff_row(folder: str) -> VGroup:
    """One line: `folder/` and what it has beyond transcribe_audio/ (+ name) or lacks (no name),
    or "same" (20 pt). .folder .parts {text: mob}"""
    order = {"generate_text": ["pyproject.toml", "main.py"]}.get(folder, EXTRA[folder])
    assert sorted(order) == sorted(EXTRA[folder])
    parts = [("m", folder + "/", 0)]
    if not order and not MISSING[folder]:
        parts.append(("g", "same", 0.3))
    for k, e in enumerate(order):
        parts += [("s", "+", 0.26 if k == 0 else 0.18), ("m", e, 0.12)]
    for k, e in enumerate(MISSING[folder]):
        parts += [("s", ", no" if order else "no", 0.04 if order else 0.3), ("m", e, 0.14)]
    mobs = []
    for kind, s, _ in parts:
        mobs.append(mono(s, ROW_PT, INK) if kind == "m" else
                    sans(s, WORD_PT, LAPTOP if kind == "g" else INK))
    for prev, (m, (_, _, buff)) in zip(mobs, list(zip(mobs, parts))[1:]):
        m.next_to(prev, RIGHT, buff=buff)
    # one baseline (mono and sans glyphs differ): each word's first flat glyph sits on the folder
    # name's; "+" is centred on the x-height
    base, xh = _flat(mobs[0], folder)
    for (_, s, _), m in zip(parts[1:], mobs[1:]):
        if s == "+":
            m.set_y(base + xh / 2)
        else:
            m.shift(UP * (base - _flat(m, s)[0]))
    row = VGroup(*mobs)
    row.folder = mobs[0]
    row.parts = {s: m for (_, s, _), m in zip(parts, mobs)}
    return row


class CloneRepo(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, f"S03 has {len(SAY)} SAY lines; this scene animates 8"

        tr = tracker("R", 1)
        t = term(P_HOME, rows=12)
        chip = readme_chip("README.md · lines 32–34")
        copy_note = sans("copy it from here", CAPTION + 2, TURN)
        place(chip, left=tr.get_right()[0] + 1.2, cy=tr.get_center()[1])
        copy_note.next_to(chip, RIGHT, buff=0.3)

        # ========================================================== 0 · git clone
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            self.play(Indicate(tr.dots[0], color=TURN, scale_factor=1.6), run_time=0.6)
            self.play(FadeIn(chip, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Type git clone")
            c0 = type_cmd(self, t, CLONE.cmd, 1.6)
            vo.wait_until("copied from the README")
            self.play(chip.frame.animate.set_stroke(TURN, 3), Write(copy_note), run_time=0.6)
            self.play(Indicate(chip.where, color=TURN, scale_factor=1.1), run_time=0.6)
            t.print(self, CLONE_OUT, run_time=0.4)
            vo.wait_until("and pause")
            yt0 = beside(your_turn(), t, c0)
            self.play(FadeIn(yt0, shift=LEFT * 0.1), run_time=0.4)
            stick(self, c0, yt0)
            self.play(Wiggle(yt0, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 1 · cd + ls; git log; git branch
        with self.voiceover(SAY[1]) as vo:
            self.wait(0.5)                     # the your-turn tag stays a moment into this block
            unstick(self, c0, yt0)
            self.play(FadeOut(yt0), FadeOut(copy_note), chip.frame.animate.set_stroke(S.GREY, 2.5),
                      tr.goto(2), run_time=0.4)
            type_cmd(self, t, CD_REPO, 0.7)
            t.set_prompt(P_REPO)
            bp = bare_prompt(self, t)
            new_part = substring(bp, "/mega-pipeline")
            self.play(Indicate(new_part, color=S.BLUE, scale_factor=1.15), run_time=0.7)

            vo.wait_until("An extra check")
            self.play(caption_extra(tr), FadeOut(chip, shift=UP * 0.1), run_time=0.4)
            c1 = type_folded(self, t, LS.cmd, [P_REPO + " ls; git log --oneline -1; \\",
                                               "    git branch"], 1.3)
            x1 = beside(extra_tag(), t, c1)
            self.play(FadeIn(x1, shift=LEFT * 0.1), run_time=0.3)
            stick(self, c1, x1)
            vo.wait_until("lists the files")
            make_room(self, t, len(LS_OUT))
            out1 = t.print(self, LS_OUT, run_time=0.8)
            names = [ln for ln in out1 if ln.text in COMPONENTS]
            assert len(names) == 5
            commit_ln, main_ln = out1[-2], out1[-1]

            vo.wait_until("five component folders")
            bars = [row_bar(ln, ln.text) for ln in names]
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.25), run_time=1.0)
            for ln, b in zip(names, bars):
                stick(self, ln, b)
            vo.wait_until("on the main branch")
            bm = row_bar(main_ln, "main")
            self.play(FadeIn(bm), Indicate(substring(main_ln, "main"), color=INK, scale_factor=1.2),
                      run_time=0.6)
            stick(self, main_ln, bm)
            vo.wait_until("at the commit this video")
            bc = row_bar(commit_ln, COMMIT)
            ctag = tag("the commit in this video", S.GREY)
            ctag.box.set_fill(TERM_BG, 1)          # opaque: it covers the row's cut end
            ctag.move_to(commit_ln.strut).align_to(t.box, RIGHT).shift(LEFT * 0.12)
            self.play(FadeIn(bc), FadeIn(ctag, shift=LEFT * 0.1), run_time=0.5)
            stick(self, commit_ln, bc, ctag)

        # ========================================================== 2 · ls -a of the five folders
        tree, ghost = build_tree()
        rows = VGroup(*[diff_row(c) for c in COMPONENTS[1:]])
        for r, entry in zip(rows, tree.rows[1:]):          # level with the tree's four entries
            place(r, left=ROWS_X, cy=entry.name_text.strut.get_center()[1])
        none_cap = sans("none of the five has a Dockerfile", CAPTION + 2, LAPTOP)
        place(none_cap, left=ROWS_X, cy=ghost.name_text.strut.get_center()[1] - 0.6)
        you_write = sans("you write it", CAPTION + 2, TURN).next_to(ghost, RIGHT, buff=0.3)
        you_write.match_y(ghost.name_text.strut)
        where114 = VGroup(mono("README.md", CAPTION, LAPTOP), label("· line 114", CAPTION, LAPTOP))
        where114.arrange(RIGHT, buff=0.12).next_to(you_write, RIGHT, buff=0.3)
        where114.match_y(you_write)
        common_rows = [tree.row(n) for n in ("README.md", "cli.py", "secrets/")]

        with self.voiceover(SAY[2]) as vo:
            make_room(self, t, 3)                         # the two command rows and the …
            c2 = type_folded(self, t, LSA.cmd,
                             [P_REPO + " ls -a transcribe_audio \\",
                              "  generate_text synthesis_audio_en translate_text synthesis_audio"], 1.5)
            x2 = beside(extra_tag(), t, c2.rows[0])       # the second row is full
            self.play(FadeIn(x2, shift=LEFT * 0.1), run_time=0.3)
            stick(self, c2.rows[0], x2)
            t.print(self, ["…"], run_time=0.25)
            resize(self, t, 3, keep=3, run_time=1.0,
                   extra=[FadeIn(tree, shift=UP * 0.2, rate_func=late()),
                          FadeIn(rows, shift=UP * 0.2, rate_func=late())])

            vo.wait_until("Each has a README")
            cbars = [hl(r.name_text.glyphs) for r in common_rows]
            for b in cbars:
                self.play(FadeIn(b), run_time=0.45)
                self.wait(0.3)
            vo.wait_until("and not one has a Dockerfile")
            self.play(Create(ghost.glyph), FadeIn(ghost.name_text), run_time=0.8)
            self.play(FadeIn(none_cap, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the README says")
            self.play(Write(you_write), FadeIn(where114, shift=UP * 0.1), run_time=0.7)
            self.play(Indicate(ghost.name_text, color=TURN, scale_factor=1.1), run_time=0.6)

        # ========================================================== 3 · two differences
        g_row, e_row = rows[0], rows[3]
        same_rows = VGroup(rows[1], rows[2])
        pp, mp, ng = g_row.parts["pyproject.toml"], g_row.parts["main.py"], g_row.parts[".gitignore"]
        no_word = g_row.parts[", no"]
        keep_tag = tag("keep in mind", TURN).next_to(VGroup(no_word, ng), UP, buff=0.14)
        bonus = tag("bonus", S.GREY).next_to(e_row, RIGHT, buff=0.3)
        c11 = e_row.parts["cli_11.py"]

        with self.voiceover(SAY[3]) as vo:
            self.play(same_rows.animate.set_opacity(0.35), *[FadeOut(b) for b in cbars],
                      run_time=0.6)
            vo.wait_until("The generate text folder")
            self.play(Indicate(g_row.folder, color=INK, scale_factor=1.1), run_time=0.7)
            vo.wait_until("its own pyproject.toml")
            b_pp = hl(pp, TURN, 0.28)
            self.play(FadeIn(b_pp), run_time=0.4)
            vo.wait_until("and a main dot py")
            b_mp = hl(mp, TURN, 0.28)
            self.play(FadeIn(b_mp), run_time=0.4)
            vo.wait_until("but no dot gitignore")
            self.play(FadeIn(keep_tag, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(ng, color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("And synthesis audio")
            self.play(Indicate(e_row.folder, color=INK, scale_factor=1.1), run_time=0.6)
            self.play(FadeIn(bonus, shift=LEFT * 0.1), Indicate(c11, color=INK, scale_factor=1.15),
                      run_time=0.6)

        # ========================================================== 4 · cd transcribe_audio
        listing_mobs = VGroup(tree, ghost, rows, none_cap, you_write, where114, b_pp, b_mp, keep_tag,
                              bonus)
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(listing_mobs), run_time=0.5)
            resize(self, t, 12, run_time=0.8)
            vo.wait_until("The tracker switches")
            tr = switch_section(self, tr, "A", 1)
            self.play(Indicate(tr.head[-1], color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("whose step 1")
            self.play(Indicate(VGroup(tr.dots[0], tr.caption), color=TURN, scale_factor=1.15),
                      run_time=0.6)
            c4 = type_cmd(self, t, CD_A, 0.9)
            t.set_prompt(P_A)
            bare_prompt(self, t)
            vo.wait_until("Pause")
            yt4 = beside(your_turn(), t, c4)
            self.play(FadeIn(yt4, shift=LEFT * 0.1), run_time=0.4)
            stick(self, c4, yt4)
            self.play(Wiggle(yt4, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 5 · cli.py: the imports
        p5 = src_panel(CLI, 4, 12)
        place(p5, left=X0, top=PANEL_TOP)
        xb = p5.code.get_right()[0] + 0.25
        br48, tg48 = side(p5, 4, 8, LAPTOP, "comes with Python", x=xb)
        br12, _ = side(p5, 12, 12, LAPTOP, x=xb)
        br911, tg911 = side(p5, 9, 11, LOOKUP, "where from? · part 2", x=xb)
        pink = [span(p5, 9, "google.cloud"), span(p5, 10, "google.cloud"), span(p5, 11, "ffmpeg")]
        uls = [base_line(w, word) for w, word in zip(pink, ["google.cloud", "google.cloud", "ffmpeg"])]

        with self.voiceover(SAY[5]) as vo:
            self.wait(0.4)
            self.play(FadeOut(unstick(self, c4, yt4)), run_time=0.3)
            resize(self, t, 3, keep=2, run_time=0.8)
            self.play(FadeIn(p5, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("The first imports")
            self.play(Create(br48), Create(br12), FadeIn(tg48, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("but the two Google Cloud")
            self.play(pink[0].animate.set_color(LOOKUP), pink[1].animate.set_color(LOOKUP),
                      Create(uls[0]), Create(uls[1]), Create(br911), run_time=0.6)
            vo.wait_until("and ffmpeg")
            self.play(pink[2].animate.set_color(LOOKUP), Create(uls[2]), run_time=0.4)
            self.play(Indicate(pink[2], color=LOOKUP, scale_factor=1.15), run_time=0.5)
            vo.wait_until("Part 2 shows")
            self.play(FadeIn(tg911, shift=LEFT * 0.1), run_time=0.5)
            self.play(Wiggle(tg911, scale_value=1.1, rotation_angle=0.02 * TAU), run_time=0.8)

        # ========================================================== 6 · cli.py: four settings
        p6 = src_panel(CLI, 18, 21, cut_comments=True, size=28)     # room for three tags
        place(p6, left=X0, top=PANEL_TOP)
        xb6 = p6.code.get_right()[0] + 0.25
        br18, tg18 = side(p6, 18, 18, CLOUD, "the bucket", x=xb6)
        br1920, tg1920 = side(p6, 19, 20, CLOUD, "its two drawers", x=xb6)
        br21, tg21 = side(p6, 21, 21, TURN, "you'll change this", x=xb6)
        bar21 = bar(p6, 21, TURN, 0.16)
        gname = span(p6, 21, "group_name")

        with self.voiceover(SAY[6]) as vo:
            scroll(self, VGroup(p5, br48, br12, tg48, br911, tg911, *uls), p6)
            vo.wait_until("the bucket's name")
            self.play(Create(br18), FadeIn(tg18, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("the two drawers")
            self.play(Create(br1920), FadeIn(tg1920, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("and on line 21")
            self.play(FadeIn(bar21), gname.animate.set_color(TURN), run_time=0.5)
            self.play(Indicate(gname, color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("which you'll change")
            self.play(Create(br21), FadeIn(tg21, shift=LEFT * 0.1), run_time=0.6)

        # ========================================================== 7 · main: three verbs
        p7 = src_panel(CLI, 118, 126)
        place(p7, left=X0, top=PANEL_TOP)
        bar118 = bar(p7, 118, TURN, 0.16)
        xb7 = p7.code.get_right()[0] + 0.45
        badges = VGroup()
        for k, (n, verb) in enumerate([(121, "download"), (123, "transcribe"), (125, "upload")], 1):
            top, bot = lines_span(p7, n, n + 1)
            b = VGroup(step_badge(k, TURN), sans(verb, CAPTION + 2, TURN)).arrange(RIGHT, buff=0.15)
            place(b, left=xb7, cy=(top + bot) / 2)
            badges.add(b)

        with self.voiceover(SAY[7]) as vo:
            scroll(self, VGroup(p6, br18, tg18, br1920, tg1920, br21, tg21, bar21), p7)
            vo.wait_until("main runs")
            self.play(FadeIn(bar118), Indicate(span(p7, 118, "main"), color=TURN, scale_factor=1.15),
                      run_time=0.6)
            for b, word in zip(badges, ["download,", "transcribe,", "upload"]):
                vo.wait_until(word)
                self.play(FadeIn(b, scale=1.3), run_time=0.35)
            self.wait(1.0)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
