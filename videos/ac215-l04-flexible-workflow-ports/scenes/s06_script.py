"""S06 · docker-shell.sh: one script, two windows (README "How to Run a Component" steps 1, 5, 6;
Quick Reference transcribe_audio step 1).

Beats (script.md "## S06", one voiceover block each):
 0  TRACKER R/1. CODE(transcribe_audio/docker-shell.sh: 6–14), full width, centred under the
    tracker; its header flashes PURPLE ("its docker-shell.sh"). Line 7 gets a YELLOW bar,
    IMAGE_NAME flashes, a two-row tag "image name = / container name" beside it (hanging upward
    from the bar into the empty end of row 6, so line 8's bar stays clear);
    lines 8–9 get bars, both $(pwd) are underlined PINK, tag "the folder you're in" beside line 8.
 1  YELLOW caption "run it from the component folder" beside line 9. Line 10: PINK bar, tag
    "the key's path inside the container" on the blank row 11 under it; line 13: BLUE bar, tag
    "Docker Hub account"; line 14: GREY tag "default".
 2  V4. The panel becomes CODE(docker-shell.sh: 28–39) at left (6.2 wide); "$1" flashes PURPLE and
    the switchboard grows out of it at right (input "first word", four tracks with their line
    chips). The tracks light one by one as named, each with a YELLOW bar on the branch of the code
    it takes (no argument: line 28 skips the case; prod 30–32; dev 33–35; run 36–38).
 3  The code panel becomes the README card README.md · lines 212–215 (the four commands, each row
    beside its station); the default row and track glow YELLOW, the other three dim (tracks by
    stroke only); GREY tag "later in this part" under the dimmed stations.
 4  V5. CODE(docker-shell.sh: 92–96) at the top, the two-windows picture under it (laptop,
    container, venv). Line 93: PINK bar + route transcribe_audio/ → /app. The walker climbs ".."
    and "../.." into secrets/ while $(pwd)/../../secrets/ writes itself (GREY "docker-shell.sh ·
    line 9" under the laptop); line 94: bar + route secrets/ → /secrets. Line 95: bar,
    GOOGLE_APPLICATION_CREDENTIALS underlined PINK, the signpost rises into /secrets.
 5  The 92–96 panel goes; CODE(Dockerfile: 17) above the container with a GREEN line to the venv
    box, which glows; a GREY laptop sheet slides over /app and leaves the venv uncovered. "The key
    is never copied": the TEAL image slab, "never in here" across it. "slash secrets shows it": the
    clock "docker run" ticks, the /secrets route pulses and a GOLD key outline appears in /secrets
    (the laptop's key stays and flashes with it); the clock reads "exit", the outline vanishes.
 6  13-row laptop terminal at ~/AC215/mega-pipeline: `cd transcribe_audio` (GREY two-row caption
    in the top band: transcribe_audio/README.md · line 15, "cd into the transcribe_audio folder"),
    the new path flashes; `./docker-shell.sh` (on the row under the long prompt) → mega-laptop/12
    lines 2–4, 14–18, 24 (BuildKit rows, GREY time tags one row high). "Build Mode: dev-run"
    boxed; "Building 99.5s" underlined; [2/5] boxed TEAL with a TEAL "2" badge, its 44.7s tag YELLOW; the 52.9s tag
    YELLOW; GREY note "first build: Docker also pulls python:3.14-slim-bookworm"; ▶ your turn.
 7  The terminal shrinks to the strip (the command and the [5/5] uv sync row, its 1.6s tag YELLOW).
    Above: CODE(pyproject.toml: 6) over the GREEN band of a version line, and PANEL(12-a-docker-
    shell.plain: 1427) "the same build, full log · line 1427" with 3.14.8 boxed and tagged "at the
    time of recording"; a copy of 3.14.8 lifts out and becomes the label of an ORANGE dot inside
    the band (label above the dot); the band and ">=3.14" flash, then the 1.6s tag turns GREEN.
 8  The terminal grows back (13 rows): 12 lines 26–27; title "container · transcribe_audio", TEAL
    frame; the prompt app@0ceffb272288:/app$ with "user" under app, "container ID · your numbers
    will differ" under the ID, PINK "the window" under /app. TRACKER QA/1: `python cli.py --help`
    → 12 lines 28–37 (session); README chip transcribe_audio/README.md · lines 98–107 with a GREEN
    tick "identical".
 9  TRACKER QA/1 · extra: `which python` → mega-transcribe_audio/03 line 2 (GREEN), `echo
    $GOOGLE_APPLICATION_CREDENTIALS` → 05 line 2 (PINK), `ls -la /secrets` → 06 lines 2–4, tag
    "empty here · yours lists mega-pipeline.json" (all three tagged extra). The TEAL terminal
    shrinks to the strip; a second terminal (7 rows) opens on ~ ("new terminal: cd here first"),
    then reads ~/AC215/mega-pipeline/transcribe_audio; the docker inspect (extra, folded) →
    mega-laptop/14 lines 2–3; GREY caption "one command · copy it from the study guide".
10  TRACKER R/5 · extra: `ls -l docker-shell.sh` → mega-laptop/19 line 2, -rwxr-xr-x boxed; TRACKER
    R/5: `chmod +x docker-shell.sh` → the prompt returns; GREY tag "already executable · needed
    only if the bit got lost". TRACKER R/6: the second terminal gives way to a GREY card (README.md ·
    line 226): Windows: Git BASH, "the input device is not a TTY" → winpty in front; "Git BASH" and
    winpty flash as named, the quoted error turns RED, underlined, at "if Docker says"; then the GREY
    row "paths mangled (C:/Program Files/Git/…)? → study guide". Fade out to an empty frame.

Deviations from SHOW (and why):
- Beat 0: line 7's tag has two rows ("image name =" / "container name"): one row is 4.5 wide and
  line 7 leaves 3.0 of the panel; rows 6 and 8 are empty at that height.
- Beat 1: the YELLOW caption sits beside line 9 (there is no free row under lines 8–9: line 10
  follows) and reads "run it from the component folder", the SAY's words ("from inside the
  component folder" is 4.8 wide and ran past the panel); line 10's tag sits on the blank row 11
  right under it (line 10 fills the panel).
- Beat 3: the README card replaces the 28–39 code panel at left, its four rows level with the
  four stations, so "side by side" reads row by row; the code panel's job was done in beat 2.
  The card and the switchboard cross-fade into beat 4's panel and picture (no empty frame).
- Beat 4: the chip "docker-shell.sh · line 9" is a GREY header-style caption under the laptop box
  (there is no room for a framed chip inside it).
- Beat 5: the Dockerfile line sits ABOVE the container with a GREEN line down to the venv box (under
  the venv box is the signpost); the 92–96 panel leaves to make room. "never in here" comes first,
  with "The key is never copied", and the clock / pulse / outline follow "slash secrets shows it
  only while the container runs" (SHOW lists the bar last; the SAY says "never copied" first).
- Beat 6: the README line-15 caption is two rows in the top band (one row is 10.5 wide; the band
  right of the tracker is 7.9); "build step 2" is a TEAL badge "2" at the row's left margin plus a
  TEAL box on [2/5] (the cut row has no room for the worded badge).
- Beat 7: "at the time of recording" sits just above the log row, right of the panel header (the
  68-character row has no room beside it); the drop lands at "already satisfies" and flies straight
  to the line (a first hop up would park the copy on that tag).
- Beat 9: the docker inspect is typed on the row under the prompt and folded by this scene at
  spaces (never inside a word: Terminal.type's fold would split `{{println}}`); the rows, joined,
  are the captured command. The kept strip rows are the last three (total 8 / . / ..).
- Beat 10: the chmod tag reads "already executable · needed only if the bit got lost" ("after a
  clone" left out: the full text is 8.9 wide and the chmod row leaves 7.0); the Windows card
  replaces the second terminal (no room above the strip with both).
"""

from common import *
from common import _drop_bare, _header_text
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    TAU,
    UP,
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    FadeTransform,
    Indicate,
    Line,
    Rectangle,
    Rotate,
    ShowIncreasingSubsets,
    Transform,
    VGroup,
    linear,
    there_and_back,
)

from explainer import style as S
from explainer.scene import VoiceScene

SAY = NARRATION["S06"]
assert len(SAY) == 11, len(SAY)

ML, MT = "mega-laptop", "mega-transcribe_audio"
SH = "mega-pipeline/transcribe_audio/docker-shell.sh"
README = "mega-pipeline/README.md"
A_README = "mega-pipeline/transcribe_audio/README.md"
DOCKERFILE = "mega-pipeline/transcribe_audio/Dockerfile"
PYPROJECT = "mega-pipeline/transcribe_audio/pyproject.toml"

# ------------------------------------------------------------------ sources (checked)
assert excerpt(SH, 7, 7) == 'export IMAGE_NAME="mega-pipeline-transcribe-audio"'
assert excerpt(SH, 8, 9).count("$(pwd)") == 2
assert excerpt(SH, 10, 10) == "export GOOGLE_APPLICATION_CREDENTIALS=/secrets/mega-pipeline.json"
assert excerpt(SH, 11, 11) == ""
assert excerpt(SH, 13, 14) == 'DOCKER_USERNAME="dlops"\nBUILD_MODE="dev-run"  # Default mode'
assert excerpt(SH, 29, 29).strip() == 'case "$1" in'
assert [excerpt(SH, n, n).strip() for n in (30, 33, 36)] == ["prod)", "dev)", "run)"]
assert excerpt(SH, 93, 93).strip() == '-v "$BASE_DIR":/app \\'
assert excerpt(SH, 94, 94).strip() == '-v "$SECRETS_DIR":/secrets \\'
assert "-e GOOGLE_APPLICATION_CREDENTIALS=" in excerpt(SH, 95, 95)
assert excerpt(DOCKERFILE, 17, 17) == "ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv"
assert excerpt(PYPROJECT, 6, 6) == 'requires-python = ">=3.14"'
MODE_CMDS = [s.split("#")[0].rstrip() for s in excerpt(README, 212, 215).split("\n")]
assert MODE_CMDS == ["./docker-shell.sh", "./docker-shell.sh dev", "./docker-shell.sh run",
                     "./docker-shell.sh prod"]
L226 = excerpt(README, 226, 226)
assert "Git BASH" in L226 and "`winpty`" in L226 and "the input device is not a TTY" in L226
L15 = excerpt(A_README, 15, 15)
assert L15.startswith("`cd` into the `transcribe_audio` folder")
assert excerpt(A_README, 98, 107).split("\n")[0] == "$ python cli.py --help"

# ------------------------------------------------------------------ commands and real outputs
CD_A = "cd transcribe_audio"                      # transcribe_audio/README.md:15 (implied)
C12 = capture("12", ML)
assert C12.cmd == "./docker-shell.sh"
BUILD = C12.at((2, 4), (14, 18), 24)
assert BUILD[0] == "Docker Username: dlops, Build Mode: dev-run"
assert "[2/5]" in BUILD[3] and BUILD[3].rstrip().endswith("44.7s")
assert "[5/5] RUN uv sync" in BUILD[6] and BUILD[6].rstrip().endswith("1.6s")
assert "exporting to image" in BUILD[7] and BUILD[7].rstrip().endswith("52.9s")
assert "naming to" in BUILD[8]
assert C12.at(26, 27) == ["Run Docker container...", "Using local image..."]
assert C12.typed(28) == "python cli.py --help"
HELP = C12.at((29, 37))
assert [s.rstrip() for s in HELP] == [s.rstrip() for s in excerpt(A_README, 99, 107).split("\n")]
PLAIN = capture("12-a-docker-shell.plain", ML).line(1427)
assert PLAIN == "#9 0.250 Using CPython 3.14.8 interpreter at: /usr/local/bin/python3"

C03, C05, C06 = capture("03", MT), capture("05", MT), capture("06", MT)
assert C03.cmd == "which python" and C03.line(2) == "/home/app/.venv/bin/python"
assert C05.cmd == "echo $GOOGLE_APPLICATION_CREDENTIALS" and C05.line(2) == "/secrets/mega-pipeline.json"
assert C06.cmd == "ls -la /secrets"
LS_SEC = C06.at((2, 4))
assert LS_SEC[0] == "total 8" and LS_SEC[1].endswith(" .") and LS_SEC[2].endswith(" ..")

C14 = capture("14", ML)
MOUNTS = C14.at(2, 3)
assert MOUNTS == ["/home/student/AC215/mega-pipeline/transcribe_audio -> /app",
                  "/home/student/AC215/secrets -> /secrets"]
INSPECT_ROWS = ["    docker inspect --format '{{range .Mounts}}{{.Source}} -> \\",
                "    {{.Destination}}{{println}}{{end}}' \\",
                "    mega-pipeline-transcribe-audio"]
assert " ".join(r.strip().removesuffix(" \\") for r in INSPECT_ROWS) == C14.cmd

C19, C20 = capture("19", ML), capture("20", ML)
assert C19.cmd == "ls -l docker-shell.sh" and C19.line(2).startswith("-rwxr-xr-x ")
assert C20.cmd == "chmod +x docker-shell.sh" and C20.lines == []

# ------------------------------------------------------------------ layout
TOP = 2.78               # top of the pictures under the tracker (tracker bottom 2.92)
BAND_Y = 3.21            # the top band, right of the tracker
BAND_X = -1.45           # its left edge (tracker R right edge: -1.71)


def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def flash_framed(g, color: str = TURN, k: float = 1.2, run_time: float = 0.6):
    """Indicate for a framed tag or signpost (.box or .board, and .text): it grows, its frame's
    stroke and its text take `color`, its dark fill stays (Indicate would fill it solid in
    `color` and hide the text)."""
    frame = getattr(g, "box", None) or g.board
    tgt = g.copy().scale(k)
    tgt[g.submobjects.index(frame)].set_stroke(color)
    tgt[g.submobjects.index(g.text)].set_color(color)
    return Transform(g, tgt, rate_func=there_and_back, run_time=run_time)


def code_row(panel, n: int):
    """The glyphs of file line n of a src_panel (first row when wrapped)."""
    return panel.code.code_lines[panel.rows_of(n)[0]]


def row_y(panel, n: int) -> float:
    return panel.bar(n).get_center()[1]


def tag2(lines, color: str = S.GREY, size: float = TAG) -> VGroup:
    """A two-row tag (the house tag's look: text in its colour, dark fill, rounded frame)."""
    rows = VGroup(*[label(s, size, color) for s in lines]).arrange(DOWN, buff=0.05)
    fr = box(rows.width + 0.4, rows.height + 0.16, color, fill=S.BG, fill_opacity=0.92, stroke=2,
             radius=0.2)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.box, g.text = fr, rows
    return g


def _part(s: str, size: float, color: str, font: str | None = None) -> VGroup:
    """Text built after a "|" that is dropped again, so parts of a row share a baseline whatever
    their glyphs (as mono_line does). .ref_dy = the pipe's centre relative to the glyphs'."""
    t = label("|" + s, size, color, **({"font": font} if font else {}))
    pipe = t.submobjects[0]
    g = VGroup(*t.submobjects[1:])
    g.ref_dy = pipe.get_center()[1] - g.get_center()[1]
    return g


def mixed(parts, size: float = CAPTION, color: str = S.GREY, buff: float = 0.12) -> VGroup:
    """One row of serif and mono parts on one baseline: parts = [str | ("mono", str[, colour]) |
    (str, colour) ...]."""
    mobs = VGroup()
    for p in parts:
        if isinstance(p, tuple) and p[0] == "mono":
            mobs.add(_part(p[1], size, p[2] if len(p) > 2 else color, MONO))
        elif isinstance(p, tuple):
            mobs.add(_part(p[0], size, p[1]))
        else:
            mobs.add(_part(p, size, color))
    mobs.arrange(RIGHT, buff=buff)
    y = mobs[0].get_center()[1] + mobs[0].ref_dy
    for m in mobs[1:]:
        m.shift(UP * (y - m.get_center()[1] - m.ref_dy))
    return mobs


def fit_tag(t, line, s: str = "extra"):
    """A GREY tag beside terminal line `line` (its last row): 22 pt, or 20 pt when the row leaves
    too little room. Positioned, not added; None when even 20 pt doesn't fit."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    end = row.glyphs.get_right()[0]
    for size in (TAG, CAPTION):
        tg = beside(tag(s, S.GREY, size=size), t, line)
        if tg.get_left()[0] >= end + 0.1:
            return tg
    return None


def type_extra(scene, t, cmd: str, type_time: float = 0.5):
    """Type an extra command and pin its GREY `extra` tag beside it."""
    ln = type_cmd(scene, t, cmd, type_time=type_time)
    tg = fit_tag(t, ln)
    assert tg is not None, cmd
    pin(scene, ln, tg, run_time=0.25)
    return ln


def type_rows(scene, t, rows_text, type_time: float = 2.0):
    """Type a command folded by hand: the prompt alone on its row, then `rows_text` (the command's
    rows, as in type_cmd's 'under the prompt' layout). Returns a VGroup with .rows."""
    _drop_bare(scene, t)
    texts = [t.prompt] + list(rows_text)
    t._make_room(scene, len(texts))
    rows = []
    for k, s in enumerate(texts):
        ln = mono_line(s, t.size, INK, t2c=t._prompt_colors(t.prompt) if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        rows.append(ln)
    scene.add(rows[0])
    typed = VGroup(*[g for r in rows[1:] for g in glyph_range(r, 0)])
    scene.play(ShowIncreasingSubsets(typed, rate_func=linear), run_time=type_time)
    for r in rows:
        scene.add(r)
    g = VGroup(*rows)
    g.rows, g.text = rows, " ".join(r.text.strip() for r in rows)
    return g


def hi_time(line, color: str = TURN):
    """Animations: a build row's GREY time tag turns `color`."""
    tg = line.time_tag
    return [tg.box.animate.set_stroke(color, 3), tg.text.animate.set_color(color)]


def glyph_box(line, sub: str, color: str = TURN, pad: float = 0.06, occurrence: int = 0):
    """A box around the glyphs of `sub` in a mono line, as tall as the row (not added)."""
    g = substring(line, sub, occurrence)
    r = box(g.width + 2 * pad + 0.04, line.strut.height + 0.06, color, fill_opacity=0.0, radius=0.06,
            stroke=3)
    return r.move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def dim_modes(sw, *modes, k: float = 0.3, run_time: float = 0.5):
    """Animation: Switchboard modes fade to k. The tracks are open polylines, so only their stroke
    fades (Switchboard.dim_modes sets their fill opacity too, which fills them in GREY)."""
    anims = []
    for m in modes:
        st = sw.stations[m]
        anims.append(sw.tracks[m].animate.set_stroke(opacity=k))
        anims += [x.animate.set_opacity(k) for x in (st.dot, st.word, st.desc, st.chip)]
    return AnimationGroup(*anims, run_time=run_time)


def slim_times(t, rows):
    """Build rows' time tags one row high (the house tag is 0.47 tall, a row 0.40: stacked tags of
    consecutive rows would overlap); the text keeps its size."""
    for r in rows:
        tg = getattr(r, "time_tag", None)
        if tg is not None:
            tg.box.stretch_to_fit_height(t.pitch - 0.05)


def readme_modes(sw) -> VGroup:
    """README.md:212-215 (the four commands) as a GREY card whose rows sit level with the
    switchboard's stations. .rows .frame .header"""
    ys = [sw.stations[m].dot.get_center()[1] for m in ("", "dev", "run", "prod")]
    rows = VGroup(*[mono(c, CAPTION, INK) for c in MODE_CMDS])
    x0 = -6.05
    for r, y in zip(rows, ys):
        r.move_to([x0 + r.width / 2, y, 0])
    w = rows.width + 0.6
    fr = box(w, ys[0] - ys[-1] + 0.8, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    fr.move_to([x0 - 0.3 + w / 2, (ys[0] + ys[-1]) / 2, 0])
    head = _header_text("README.md · lines 212–215").next_to(fr, UP, buff=0.08)
    head.align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head
    return g


def windows_card() -> VGroup:
    """README.md:226 as a GREY card: the Windows rule and the study-guide pointer. Row 1's parts:
    [0] "Windows: Git BASH", [2] the quoted error, [4] winpty."""
    r1 = mixed(["Windows: Git BASH", "·", "“the input device is not a TTY”", "→  put", ("mono", "winpty", INK),
                "in front"], TAG, INK, buff=0.2)
    r2 = mixed(["paths mangled", ("mono", "(C:/Program Files/Git/…)?", S.GREY), "→  study guide"],
               TAG, S.GREY, buff=0.2)
    rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    fr = box(rows.width + 0.6, rows.height + 0.5, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    rows.move_to(fr)
    head = _header_text("README.md · line 226").next_to(fr, UP, buff=0.08).align_to(fr, LEFT)
    head.shift(RIGHT * 0.12)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head
    return g


class DockerShell(VoiceScene):
    def construct(self):
        tr = tracker("R", 1)

        # ========================================================== 0 · lines 6-14: names and paths
        p0 = src_panel(SH, 6, 14)
        p0.shift(UP * ((TOP + BOTTOM) / 2 + 0.2 - p0.get_center()[1]))
        bar7 = p0.bar(7, TURN)
        bars89 = VGroup(p0.bar(8, TURN), p0.bar(9, TURN))
        # underlines hug the glyphs: the rows are tight, a lower line touches the next row's caps
        pwd = VGroup(under(p0.span(8, "$(pwd)"), LOOKUP, 3, 0.01), under(p0.span(9, "$(pwd)"), LOOKUP, 3, 0.01))
        t7 = tag2(["image name =", "container name"])
        # hangs from line 7's bar upward (row 6 is empty there): line 8's bar stays uncovered
        t7.next_to(code_row(p0, 7), RIGHT, buff=0.3).set_y(bar7.get_bottom()[1] + 0.1 + t7.height / 2)
        assert t7.get_top()[1] < p0.code.background.get_top()[1] - 0.05      # inside the panel
        t8 = grey_tag("the folder you're in")
        t8.next_to(code_row(p0, 8), RIGHT, buff=0.3).set_y(row_y(p0, 8))
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(p0, shift=UP * 0.15), run_time=0.8)
            self.play(flash(p0.header, TOOL, 1.06), run_time=0.8)
            vo.wait_until("Line 7 names")
            self.play(FadeIn(bar7), flash(p0.span(7, "IMAGE_NAME")), run_time=0.7)
            self.play(FadeIn(t7, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Lines 8 and 9")
            self.play(FadeIn(bars89), run_time=0.5)
            self.play(Create(pwd), run_time=0.6)
            vo.wait_until("the folder you're in")
            self.play(FadeIn(t8, shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 1 · run it from the folder; key path; account
        c9 = label("run it from the component folder", CAPTION, TURN)
        c9.next_to(code_row(p0, 9), RIGHT, buff=0.25).set_y(row_y(p0, 9))
        bar10 = p0.bar(10, LOOKUP, 0.22)
        t10 = grey_tag("the key's path inside the container")
        # under line 10's bar (its descenders reach the bar's edge), on the blank row 11
        t10.move_to([code_row(p0, 10).get_right()[0] - t10.width / 2,
                     bar10.get_bottom()[1] - 0.02 - t10.height / 2, 0])
        bar13 = p0.bar(13, CLOUD, 0.25)
        t13 = grey_tag("Docker Hub account")
        t13.next_to(code_row(p0, 13), RIGHT, buff=0.3).set_y(row_y(p0, 13))
        assert t10.get_bottom()[1] > t13.get_top()[1] + 0.02
        t14 = grey_tag("default")
        t14.next_to(code_row(p0, 14), RIGHT, buff=0.3).set_y(row_y(p0, 14))
        t14.set_x(max(t14.get_center()[0], t13.get_right()[0] + 0.25 + t14.width / 2))
        t14.set_y(min(row_y(p0, 14), bar13.get_bottom()[1] - 0.02 - t14.height / 2))   # clear of line 13's bar
        assert t14.get_bottom()[1] > p0.get_bottom()[1] + 0.05
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(c9, shift=LEFT * 0.15), flash(pwd, TURN, 1.05), run_time=0.7)
            vo.wait_until("Line 10 is")
            self.play(FadeIn(bar10), flash(p0.span(10, "/secrets/mega-pipeline.json"), LOOKUP, 1.08),
                      run_time=0.7)
            self.play(FadeIn(t10, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("line 13 names")
            self.play(FadeIn(bar13), FadeIn(t13, shift=LEFT * 0.1), run_time=0.6)
            self.play(flash(p0.span(13, '"dlops"'), CLOUD, 1.15), run_time=0.6)
            self.play(FadeIn(t14, shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 2 · the case statement: the switchboard
        notes0 = [bar7, bars89, pwd, t7, t8, c9, bar10, t10, bar13, t13, t14]
        p2 = src_panel(SH, 28, 39, width=6.2)
        p2.move_to([-6.45 + p2.code.width / 2 + (p2.get_center()[0] - p2.code.get_center()[0]), 0, 0])
        p2.shift(UP * (TOP - p2.get_top()[1]))
        sw = Switchboard()
        sw.move_to([6.45 - sw.width / 2, -0.1, 0])
        quote = p2.span(29, '"$1"')
        bar28 = p2.bar(28, TURN)
        branch = {"prod": VGroup(*[p2.bar(n, TURN) for n in (30, 31, 32)]),
                  "dev": VGroup(*[p2.bar(n, TURN) for n in (33, 34, 35)]),
                  "run": VGroup(*[p2.bar(n, TURN) for n in (36, 37, 38)])}
        with self.voiceover(SAY[2]) as vo:
            self.play(*[FadeOut(m) for m in notes0], run_time=0.3)
            self.play(FadeTransform(p0, p2), run_time=0.9)
            self.play(flash(quote, TOOL, 1.3), run_time=0.6)
            ghost = quote.copy()
            self.add(ghost)
            self.play(ghost.animate.move_to(sw.input).set_opacity(0), FadeIn(sw, shift=LEFT * 0.3),
                      run_time=0.9)
            self.remove(ghost)
            vo.wait_until("No word")
            self.play(sw.light(""), FadeIn(bar28), run_time=0.6)
            vo.wait_until("Dev only builds")
            self.play(sw.unlight(""), FadeOut(bar28), sw.light("dev"), FadeIn(branch["dev"]), run_time=0.6)
            vo.wait_until("run only runs")
            self.play(sw.unlight("dev"), FadeOut(branch["dev"]), sw.light("run"), FadeIn(branch["run"]),
                      run_time=0.6)
            vo.wait_until("and prod builds")
            self.play(sw.unlight("run"), FadeOut(branch["run"]), sw.light("prod"), FadeIn(branch["prod"]),
                      run_time=0.6)

        # ========================================================== 3 · the README's four lines; default first
        card = readme_modes(sw)
        later = grey_tag("later in this part")
        prod_st = sw.stations["prod"]
        later.move_to([VGroup(prod_st.word, prod_st.desc).get_center()[0], prod_st.chip.get_bottom()[1] - 0.42, 0])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(branch["prod"]), sw.unlight("prod"), run_time=0.3)
            self.play(FadeTransform(p2, card), run_time=0.8)
            self.play(sw.light(""), card.rows[0].animate.set_color(TURN), run_time=0.6)
            vo.wait_until("then come back")
            self.play(dim_modes(sw, "dev", "run", "prod"), *[r.animate.set_opacity(0.3) for r in card.rows[1:]],
                      FadeIn(later, shift=UP * 0.1), run_time=0.7)

        # ========================================================== 4 · two windows: -v, -v, -e
        p4 = src_panel(SH, 92, 96, size=20)
        p4.move_to([0, 0, 0]).shift(UP * (TOP - p4.get_top()[1]))
        v5 = TwoWindows(show=("laptop", "container", "venv"))
        v5.shift(np.array([0, TOP - p4.height - 0.18 - v5.get_top()[1], 0]))
        line9 = _header_text("docker-shell.sh · line 9")
        line9.next_to(v5.laptop_frame, DOWN, buff=0.12).align_to(v5.laptop_frame, LEFT).shift(RIGHT * 0.1)
        bar93, bar94 = p4.bar(93, LOOKUP, 0.22), p4.bar(94, LOOKUP, 0.22)
        bar95 = p4.bar(95, LOOKUP, 0.22)
        gac = under(p4.span(95, "GOOGLE_APPLICATION_CREDENTIALS"), LOOKUP, 3, 0.0)   # 20 pt rows: hug the glyphs
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(card, sw, later)), FadeIn(p4, shift=DOWN * 0.1), FadeIn(v5), run_time=0.7)
            vo.wait_until("two windows")
            self.play(flash(v5.app, TURN, 1.08), flash(v5.secrets_area, TURN, 1.08), run_time=0.8)
            vo.wait_until("Dash v puts")
            self.play(FadeIn(bar93), *v5.parts_in("route_app", anim=Create), run_time=0.9)
            self.play(v5.blink("app"), run_time=0.7)
            vo.wait_until("and the secrets folder")
            walker, steps = v5.walk(run_time=0.5)
            self.play(steps[0], FadeIn(line9), run_time=0.3)
            for a in steps[1:]:
                self.play(a)
            vo.wait_until("at slash secrets")
            self.play(FadeIn(bar94), *v5.parts_in("route_secrets", anim=Create), run_time=0.9)
            vo.wait_until("Dash e sets")
            self.play(FadeOut(walker), FadeOut(line9), FadeIn(bar95), Create(gac), run_time=0.6)
            self.play(*v5.parts_in("post", anim=lambda m: FadeIn(m, shift=UP * 0.35)), run_time=0.8)
            vo.wait_until("a signpost to the key")
            self.play(flash_framed(v5.post, LOOKUP, 1.06), flash(v5.key, KEY, 1.3), run_time=0.8)

        # ========================================================== 5 · the venv stays visible; the key never copied
        p5 = src_panel(DOCKERFILE, 17, 17, size=20)
        p5.move_to([v5.container_frame.get_right()[0] - p5.width / 2, 0, 0])
        p5.shift(UP * (v5.get_top()[1] + 0.25 - p5.get_bottom()[1]))
        span17 = p5.span(17, "/home/app/.venv")
        bar17 = p5.bar(17, VENV, 0.2)
        vx = v5.venv_box.get_left()[0] + 0.45
        link = Line([vx, p5.get_bottom()[1] - 0.04, 0], [vx, v5.venv_box.get_top()[1] + 0.02, 0], color=VENV,
                    stroke_width=4)
        sheet = Rectangle(width=v5.app.width + 0.12, height=v5.app.height + 0.12).set_stroke(LAPTOP, 2)
        sheet.set_fill(LAPTOP, 0.55).move_to(v5.app).shift(LEFT * 0.9)
        hand = v5.parts["clock"][0][1]
        clock_c = v5.parts["clock"][0][0]
        clock_l = v5.parts["clock"][1]
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(p4, bar93, bar94, bar95, gac)), run_time=0.4)
            self.play(FadeIn(p5, shift=DOWN * 0.1), FadeIn(bar17), run_time=0.6)
            vo.wait_until("the venv lives outside")
            self.play(Create(link), flash(span17, VENV, 1.1), run_time=0.7)
            self.play(flash(v5.venv_box, VENV, 1.08), run_time=0.7)
            vo.wait_until("so the window")
            sheet.set_opacity(0)
            self.add(sheet)
            self.play(sheet.animate.move_to(v5.app).set_fill(LAPTOP, 0.55).set_stroke(LAPTOP, 2, 1), run_time=0.8)
            self.play(flash(v5.venv_box, VENV, 1.1), run_time=0.7)
            vo.wait_until("The key is never copied")
            self.play(FadeOut(sheet), FadeOut(link), *v5.parts_in("image"), run_time=0.5)
            self.play(*v5.parts_in("never"), run_time=0.6)
            vo.wait_until("slash secrets shows it")
            self.play(*v5.parts_in("clock"), run_time=0.4)
            self.play(Rotate(hand, -TAU, about_point=clock_c.get_center()), v5.pulse("secrets"),
                      run_time=1.2)
            self.play(Rotate(hand, -TAU, about_point=clock_c.get_center()), flash(v5.key, KEY, 1.25),
                      flash(v5.parts["ghost"], KEY, 1.25), run_time=1.0)
            exit_l = mono("exit", CAPTION, S.GREY).move_to(clock_l, aligned_edge=LEFT)
            self.play(Transform(clock_l, exit_l), *v5.parts_out("ghost"), run_time=0.6)

        # ========================================================== 6 · cd, then ./docker-shell.sh
        t = term(P_REPO, rows=13)
        q15 = mixed(["“", ("mono", "cd"), "into the", ("mono", "transcribe_audio"), "folder”"])
        q15[0].shift(RIGHT * 0.09)                     # the opening quote hugs `cd`, as the closing one does
        cap15 = VGroup(_header_text("transcribe_audio/README.md · line 15"), q15)
        cap15.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        cap15.move_to([BAND_X + cap15.width / 2, 3.1, 0])
        pull = mixed(["first build: Docker also pulls", ("mono", "python:3.14-slim-bookworm")])
        pull.move_to([BAND_X + pull.width / 2, BAND_Y, 0])
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(v5, p5, bar17)), FadeIn(t), run_time=0.7)
            type_cmd(self, t, CD_A, type_time=0.6)
            self.play(FadeIn(cap15, shift=DOWN * 0.1), run_time=0.4)
            cd_prompt(self, t, p_comp("transcribe_audio"), run_time=0.7)
            vo.wait_until("and run docker-shell.sh")
            ds = type_cmd(self, t, C12.cmd, type_time=0.6)
            rows = print_build(self, t, BUILD, run_time=0.9, lag=0.1)
            slim_times(t, rows)
            mode_box = glyph_box(rows[0], "Build Mode: dev-run")
            self.play(Create(mode_box), run_time=0.5)
            vo.wait_until("Two steps take")
            u99 = under(substring(rows[2], "Building 99.5s"), TURN)
            self.play(Create(u99), run_time=0.5)
            vo.wait_until("build step 2")
            b2 = build_badge(2, words=False).move_to([t.box.get_left()[0] + 0.24, rows[3].strut.get_center()[1], 0])
            box25 = glyph_box(rows[3], "[2/5]", CTR)
            self.play(FadeIn(b2, scale=1.3), Create(box25), *hi_time(rows[3]), run_time=0.6)
            self.play(flash_framed(rows[3].time_tag, TURN, 1.2), run_time=0.6)
            vo.wait_until("and writing out the image")
            self.play(*hi_time(rows[7]), run_time=0.4)
            self.play(flash_framed(rows[7].time_tag, TURN, 1.2), run_time=0.6)
            vo.wait_until("a first build also pulls")
            self.play(FadeOut(cap15), FadeIn(pull, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Pause and run it")
            pin(self, ds, beside(your_turn(), t, ds), run_time=0.4)

        # ========================================================== 7 · uv sync is quick: 3.14.8 inside >=3.14
        uv_row = rows[6]
        pp = src_panel(PYPROJECT, 6, 6)
        pp.move_to([6.3 - pp.width / 2, 0, 0]).shift(UP * (TOP - pp.get_top()[1]))
        vl = VersionLine(10, 16, lo=14, label_=False)
        vl.move_to([0, 0, 0]).shift(UP * (pp.get_bottom()[1] - 0.78 - vl.axis.get_center()[1]))
        dot = vl.dot(14.3, "3.14.8", SYSTEM)
        assert dot.text.get_top()[1] < pp.get_bottom()[1] - 0.02
        lg = log_panel([PLAIN], "the same build, full log · line 1427")
        lg.shift(UP * (STRIP_TOP + 0.14 - lg.frame.get_bottom()[1]))
        v148 = substring(lg.rows[0], "3.14.8")
        box148 = glyph_box(lg.rows[0], "3.14.8")
        rec = recorded_tag()
        rec.next_to(lg.header, RIGHT, buff=0.35).set_y(lg.header.get_center()[1] + 0.02)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(mode_box, u99, b2, box25, pull)), run_time=0.3)
            resize(self, t, 3, keep=[ds.rows[0], ds.rows[1], uv_row])
            self.play(*hi_time(uv_row), FadeIn(lg, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(pp), FadeIn(vl), run_time=0.6)
            vo.wait_until("the image's Python")
            self.play(Create(box148), run_time=0.4)
            vo.wait_until("at the time of recording")
            self.play(FadeIn(rec, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("already satisfies")
            # straight up to its place on the line (a first hop up would park it on the tag)
            lift = v148.copy()
            self.add(lift)
            self.play(Transform(lift, dot.text), FadeIn(dot.dot, scale=2.0), run_time=1.0)
            self.remove(lift, dot.dot)
            self.add(dot)
            self.play(flash(vl.band, VENV, 1.04), flash(pp.span(6, '">=3.14"'), VENV, 1.15), run_time=0.8)
            vo.wait_until("so uv downloads none")
            self.play(*hi_time(uv_row, VENV), run_time=0.4)
            self.play(flash_framed(uv_row.time_tag, VENV, 1.25), run_time=0.6)

        # ========================================================== 8 · inside: user app, /app, a new id each run
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(lg, box148, rec, pp, vl, dot)), run_time=0.4)
            resize(self, t, 13, run_time=0.6)
            t.print(self, C12.at(26, 27), run_time=0.4)
            self.play(*enter_container(t, "transcribe_audio"), run_time=0.6)
            pr = bare_prompt(self, t)
            p_app = glyph_range(pr, 0, 3)
            p_id = glyph_range(pr, 4, 16)
            p_win = glyph_range(pr, 17, 21)
            y1 = pr.strut.get_center()[1] - t.pitch - 0.05
            u_app, u_id, u_win = under(p_app, S.GREY, 3), under(p_id, S.GREY, 3), under(p_win, LOOKUP, 3)
            tg_user = grey_tag("user").move_to([p_app.get_left()[0] - 0.05, y1, 0], aligned_edge=LEFT)
            tg_user.set_y(y1)
            tg_win = tag("the window", LOOKUP).move_to([p_win.get_center()[0], y1, 0])
            assert tg_win.get_left()[0] > tg_user.get_right()[0] + 0.1
            tg_id = grey_tag("container ID · your numbers will differ")
            tg_id.move_to([p_id.get_left()[0] + 0.15 + tg_id.width / 2, y1 - t.pitch - 0.1, 0])
            vo.wait_until("as user app")
            self.play(Create(u_app), FadeIn(tg_user, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("in slash app")
            self.play(Create(u_win), FadeIn(tg_win, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("after the at sign")
            self.play(Create(u_id), FadeIn(tg_id, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("The first check")
            # tags out and tracker switch in one move, so the chip and tick land on "matches the README"
            # (done one after the other they ran ~1 s past the sentence and delayed SAY[9])
            qa = tracker("QA", 1)
            self.play(FadeOut(VGroup(u_app, u_id, u_win, tg_user, tg_win, tg_id)),
                      FadeOut(tr, shift=UP * 0.25), FadeIn(qa, shift=DOWN * 0.25), run_time=0.6)
            tr = qa
            session(self, t, C12, (28, 37), type_time=0.45, out_time=0.45)
            chip98 = readme_chip("transcribe_audio/README.md · lines 98–107")
            tick = check_mark(0.3, VENV)
            same = label("identical", CAPTION, VENV)
            band8 = VGroup(chip98, tick, same).arrange(RIGHT, buff=0.2)
            band8.move_to([tr.get_right()[0] + 0.35 + band8.width / 2, BAND_Y, 0])
            vo.wait_until("matches the README")
            self.play(FadeIn(chip98, shift=DOWN * 0.1), run_time=0.35)
            self.play(Create(tick), FadeIn(same), run_time=0.4)

        # ========================================================== 9 · three extra checks; the mounts from outside
        with self.voiceover(SAY[9]) as vo:
            self.wait(1.1)                      # the "identical" tick stays a moment (tracker caption needs its room)
            self.play(FadeOut(band8), caption_extra(tr, True), run_time=0.4)
            type_extra(self, t, C03.cmd)
            t.print(self, [(C03.line(2), VENV)], run_time=0.3)
            vo.wait_until("the signpost points")
            type_extra(self, t, C05.cmd)
            t.print(self, [(C05.line(2), LOOKUP)], run_time=0.3)
            vo.wait_until("and slash secrets is empty")
            type_extra(self, t, C06.cmd)
            ls_rows = t.print(self, LS_SEC, run_time=0.4)
            pin(self, ls_rows[0], beside(grey_tag("empty here · yours lists mega-pipeline.json"), t, ls_rows[0]),
                run_time=0.4)
            vo.wait_until("In a second terminal")
            resize(self, t, 3, run_time=0.6)
            t2 = second_terminal(self, p_comp("transcribe_audio"), rows=7, top=2.75)
            insp = type_rows(self, t2, INSPECT_ROWS, type_time=1.3)
            pin(self, insp, fit_tag(t2, insp), run_time=0.25)
            cap14 = note("one command · copy it from the study guide")
            cap14.move_to([t2.box.get_left()[0] + 0.15 + cap14.width / 2,
                           (t2.box.get_bottom()[1] + t.box.get_top()[1]) / 2, 0])
            m_rows = t2.print(self, MOUNTS, run_time=0.5)
            self.play(FadeIn(cap14), flash(substring(m_rows[0], "-> /app"), LOOKUP, 1.1),
                      flash(substring(m_rows[1], "-> /secrets"), LOOKUP, 1.1), run_time=0.7)

        # ========================================================== 10 · chmod +x (harmless); winpty on Windows
        card226 = windows_card()
        card226.move_to([0, (TOP + STRIP_TOP) / 2 + 0.1, 0])
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(cap14), run_time=0.3)
            tr = switch_section(self, tr, "R", 5, run_time=0.6)
            self.play(caption_extra(tr, True), run_time=0.3)
            type_extra(self, t2, C19.cmd)
            out19 = t2.print(self, [C19.line(2)], run_time=0.4)[0]
            rwx = glyph_box(out19, "-rwxr-xr-x", TURN)
            pin(self, out19, rwx, anim=Create(rwx))
            self.play(caption_extra(tr, False), run_time=0.3)
            ch = type_cmd(self, t2, C20.cmd, type_time=0.6)
            bare_prompt(self, t2)
            done = fit_tag(t2, ch, "already executable · needed only if the bit got lost")
            assert done is not None
            pin(self, ch, done, run_time=0.4)
            vo.wait_until("Step 6")
            self.play(tr.goto(6), FadeOut(t2), run_time=0.6)
            self.play(FadeIn(card226.frame), FadeIn(card226.header), FadeIn(card226.rows[0]), run_time=0.6)
            r226 = card226.rows[0]
            vo.wait_until("use Git BASH")
            self.play(flash(r226[0], TURN, 1.06), run_time=0.6)
            vo.wait_until("and put winpty in front")
            self.play(flash(r226[4], TURN, 1.12), run_time=0.7)
            vo.wait_until("if Docker says")
            err = under(r226[2], ERR, 3, 0.06)
            self.play(r226[2].animate.set_color(ERR), Create(err), run_time=0.6)
            self.wait(0.6)
            self.play(FadeIn(card226.rows[1], shift=UP * 0.1), run_time=0.5)
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)
