r"""S12 · generate_text: same recipe, two surprises (README › generate_text steps 1–13; V2 small,
V7 second half, PONDER 4).

Nothing here talks to Google: steps 10–12 are typed only, and what to look for is a "with your
key, look for" card citing the cli.py line that prints each item (ASSETS.md). Every terminal line
comes from assets/terminal (30–35 on the laptop, generate_text/01–05 in the container).

Beats (script.md "## S12", one voiceover block each):
 0  The tracker switches section (A13 lifts away, "README › generate_text" drops in, 13 dots). On
    "follows the same recipe" the 13 step titles unfold downward out of their dots into a numbered
    list, then fold back into the dots (≈ 2 s). TRACKER B1: terminal (12 rows, laptop, transcribe_
    audio prompt). It types `cd ../generate_text` (folds at the prompt's width) → no output; the
    prompt becomes student@laptop:~/mega-pipeline/generate_text$. TRACKER B2: above the terminal
    a GREY secrets/ folder; a GOLD key drops into it, its name mega-pipeline.json appears beside;
    tag illustration.
 1  TRACKER B2 · extra. It types `ls -a` (extra) → 30-b-ls.txt lines 2–8; "pyproject.toml" gets a
    GREEN bar on "this folder already has". It types `cat pyproject.toml` (extra) → lines 9–16.
    "listing both packages": lines 14–15 GREEN + GREEN tag "already listed"; "requiring Python
    3.14": line 12 YELLOW bar, `>=3.14` YELLOW; "Leave that until step 13": GREY tag "leave it ·
    step 13", the tracker's dot 13 pulses.
 2  TRACKER B3. The terminal shrinks to 10 rows (room for the chip). It types `uv init --bare` →
    31-b-uv-init.txt line 2 (wrap), RED; "Project is already initialized" underlines RED. Under the
    tracker band the one-line README chip `generate_text/README.md · lines 20–24` "uv init --bare";
    tag erratum on "a small mistake"; on "skip step 3" a GREY strike line through the quoted
    command and the GREY note "skip it · main.py is a leftover" (its main.py part pulses on "and
    ignore the leftover").
 3  TRACKER B4. The terminal shrinks to the strip. CODE(files/transcribe_audio.Dockerfile: 3) as
    `transcribe_audio/Dockerfile · line 3` (caption "from transcribe_audio/README.md / lines
    41–90"); on "except line 3 drops ffmpeg" `ffmpeg` is struck through and a copy of the panel
    slides down into PANEL(files/generate_text.Dockerfile: 3), headed `generate_text/Dockerfile ·
    line 3`; caption "the only difference · generate_text/README.md line 45" on "since this
    component"; "Copy yours": B's line gets a YELLOW bar.
 4  TRACKER B5. The terminal clears and grows to 7 rows while a small V2 (right) and lecture 2's
    config card (left, the ARG line `DEBIAN_PACKAGES · build-essential ffmpeg`, ORANGE) fade in
    above. It types `docker build -t generate_text .` → 32-b-build.txt lines 3, 14–17 (live view:
    each row's time lifts into a compact GREY tag at the right end; row 14 cut at 46 so its tag can
    grow; line 3 cut at 65 with its run of spaces dropped, "FINISHED …").
    "and the big RUN step": `[2/5]` TEAL in a TEAL box + a TEAL circled 2 after the row; its tag
    becomes ORANGE "22.8s · not cached". "because the package list": the card's line loses
    ffmpeg; a thin ORANGE thread runs from it to the apt slab, which dissolves and re-forms (no
    CACHED stamp). "Pause and run it": ▶ your turn by the command; row 17's 5.9s tag pulses.
 5  V2 and the card go; the terminal shrinks to the strip (rows 15–17 stay). V7 above: the axis
    3.10 … 3.16, an ORANGE dot "image · Python 3.12" (on "The image has"), the GREEN interval from
    3.14 with `requires-python = ">=3.14"` (on "this pyproject.toml asks"), the dot outside it;
    three GREY answer chips "fail?" "use 3.12 anyway?" "something else?" (on "Which Python").
    After the SAY: PONDER (8 s), the card over the strip (V7 shows no answer).
 6  The card and the chips go. Row 17 `[5/5] RUN uv sync` gets a YELLOW bar that unfolds into
    PANEL(32-b-build.plain.txt: 341–344, "the same build, full log · lines 341–344") in the strip's
    place (the strip fades). "uv downloaded": the Downloading part of line 341 underlines PURPLE
    and `(35.9MiB)` GREY; "3.15.0 at the time": `3.15.0` (line 343) YELLOW + tag "at the time of
    recording"; "and built the venv": `/home/app/.venv` GREEN.
 7  V7: the 3.12 dot turns RED (outside); on "so uv fetched" a PURPLE download arrow drops a
    GREEN-ringed dot onto 3.15, labelled "3.15.0 · uv-managed · 35.9 MiB" above it and "the newest
    at the time of recording" below; on "as in lecture 2" the panel's 3.15.0 row and the new dot
    pulse together.
 8  TRACKER B6. Panel and V7 go; the strip returns and grows to 10 rows. It types `docker run
    --rm -ti -v "$(pwd):/app" generate_text` (folds); TEAL frame, title "container ·
    generate_text". TRACKER B6 · extra. It types `python --version` (extra) →
    generate_text/01-python-version.txt line 3, then `readlink -f $(which python)` (extra) → line 4
    (wrap); "from uv's folder": `/home/app/.local/share/uv/python/` underlines PURPLE.
 9  TRACKER B7. It types `uv add google-cloud-storage google-genai` → 02-uv-add.txt lines 2–3; on
    "since both packages" a GREY tag "nothing new: both already listed", which grows "· writes
    uv.lock" on "it only writes".
10  TRACKER B8: the terminal shrinks to 8 rows and an editor inset (top right, above it; over a
    10-row terminal it would cover the tracker caption) shows CODE(generate_text/cli.py: 19,
    comment cut); `group_name` YELLOW, underlined; YELLOW "line 19 here" left of it. TRACKER B9:
    the inset goes, the terminal clears to 10 rows, it types `python cli.py --help` → 04-help.txt
    lines 2–10; "which matches the README": a GREEN check and "= generate_text/README.md · lines
    116–124" beside "Generate text from prompt". ▶ your turn on "Pause".
11  TRACKER B10 → B12. The inset goes; the terminal clears and shrinks to the strip. Above it the
    GREY README card `README.md · lines 141–143` (the three commands) with a GREY tag "same as -d ·
    -g · -u"; the strip types the three commands one after another, no output, the tracker ticking
    10, 11, 12. "The generate step": the card goes; CODE(generate_text/cli.py: 73–76) at the top
    (dedented); line 73 YELLOW bar, the default model underlines; a BLUE cloud "Gemini · Vertex AI"
    between panel and strip; the bar moves to line 75, a transcript page rides to the cloud; GOLD
    "billed to the course project" under the cloud. "Google retires": the bar returns to line 73
    and a GREY card slides in under it (over lines 74–76): "Vertex AI retires gemini-2.5-flash-lite
    on 2026-10-20 · then:"; "after that, start": the chip `docker run --rm -ti -e
    GEMINI_MODEL=<current model> -v "$(pwd):/app" generate_text` (two rows, extra, shown, not
    typed); "in the Gemini model variable": GEMINI_MODEL underlines YELLOW in line 73 and the chip.
12  The panel, card and cloud go; the GOLD tag moves to the strip's top-right corner. The "with
    your key, look for" card writes item by item (lines 74, 80, 81, 84, 103) on their words, then
    the RED-bordered "if it fails: 429 RESOURCE_EXHAUSTED …" line; ▶ your turn beside the strip's
    last command on "Pause".
13  TRACKER B13. The card goes; the terminal grows to 8 rows and types `exit` (GREY frame, title
    laptop, generate_text prompt). "brings the fix": an editor inset with
    CODE(generate_text/pyproject.toml: 4); "lower the minimum": `">=3.14"` becomes `">=3.12"`
    GREEN, tag "the fix · not in the README". TRACKER B13 · extra: `grep -n requires-python
    pyproject.toml` (extra) → 34-b-fix-requires-python.txt line 2 (GREEN). "Git status lists":
    `git status --short .` (extra) → lines 3–5; "this folder has no": `?? Dockerfile` GREY tag "no
    .gitignore here" and, beside ` M pyproject.toml`, the GREY caption "yours also shows M cli.py
    (your group name)".
14  TRACKER B13. The inset goes; the terminal clears to 7 rows; `docker build -t generate_text .`
    → 35-b-rebuild-312.txt lines 3, 14–17 (time tags); ▶ your turn. "uv sync now uses": the
    terminal shrinks to the strip, V7 returns (band from 3.14, the 3.12 dot RED, the uv-managed
    3.15 dot); row 17 unfolds into PANEL(35-b-rebuild-312.plain.txt: 31, "full log · line 31")
    above the strip, `Using CPython 3.12.15 interpreter at: /usr/local/bin/python3` ORANGE; the
    interval's start drags back to 3.12, the dot turns ORANGE inside, the 3.15 dot fades. "as does
    the next container": the panel goes, the terminal clears to 6 rows; TRACKER B13 · extra; it
    types `docker run --rm -ti -v "$(pwd):/app" generate_text` (extra; TEAL) and `python
    --version; readlink -f $(which python)` (extra) → 05-python-version-312.txt lines 2–3
    (ORANGE). "Exit it": `exit` (GREY frame, title laptop). "Better still": V7's interval label
    pulses; the generate_text prompt returns. Fade out: empty frame.
"""

import textwrap

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import (box, check_mark, chip, code_panel, code_span, folder_glyph, label, line_bar,
                              mono, mono_line, step_badge, substring, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, CTR, ERR, GROUP, INK, KEY, LAPTOP, NARRATION, P_A, SYSTEM, TERMINAL, TOOL, TURN,
                    VENV, ConfigCard, LayerStack, LookFor, VersionLine, asset_lines, bare_prompt, beside,
                    caption_extra, capture, cost_tag, editor_inset, enter_container, erratum_tag, excerpt,
                    extra_tag, file_panel, illustration_tag, key_glyph, leave_container, live_split,
                    log_panel, p_comp, page_token, pin, readme_chip, resize, sans, source_text,
                    src_panel, strike, strip_top, switch_section, term, tracker, type_cmd, under, your_turn)

SAY = NARRATION["S12"]

# ------------------------------------------------------------------ commands and real outputs
B = "generate_text"
P_B = p_comp(B)
CD = "cd ../generate_text"                      # generate_text/README.md:13 ("cd into the folder")

LS = capture("30-b-ls")
assert LS.cmd == "ls -a; cat pyproject.toml", LS.cmd   # typed as two commands (script.md)
LS_CMD, CAT_CMD = "ls -a", "cat pyproject.toml"
LS_OUT = LS.at((2, 8))
assert LS_OUT == [".", "..", "README.md", "cli.py", "main.py", "pyproject.toml", "secrets"], LS_OUT
CAT_OUT = LS.at((9, 16))
assert CAT_OUT[3] == 'requires-python = ">=3.14"' and CAT_OUT[0] == "[project]", CAT_OUT
assert "google-cloud-storage" in CAT_OUT[5] and "google-genai" in CAT_OUT[6], CAT_OUT

UVI = capture("31-b-uv-init")
assert UVI.cmd == "uv init --bare" and UVI.exit == 2
UVI_OUT = UVI.at(2)
assert UVI_OUT[0].startswith("error: Project is already initialized in")

DF_A, DF_B = "files/transcribe_audio.Dockerfile", "files/generate_text.Dockerfile"
assert asset_lines(DF_A, 3, 3) == 'ARG DEBIAN_PACKAGES="build-essential ffmpeg"'
assert asset_lines(DF_B, 3, 3) == 'ARG DEBIAN_PACKAGES="build-essential"'
_RB = source_text("generate_text/README.md").split("\n")
assert _RB[44] == 'ARG DEBIAN_PACKAGES="build-essential"', _RB[44]          # README line 45
assert _RB[21] == "uv init --bare" and _RB[19].startswith("Inside the `generate_text` folder")
RUN = _RB[98]                                                                     # README line 99
assert RUN == 'docker run --rm -ti -v "$(pwd):/app" generate_text', RUN

BUILD_CMD = "docker build -t generate_text ."   # README :95 names the image; no --network host
_BD = capture("32-b-build")
assert _BD.cmd == "docker build --network host -t generate_text .", _BD.cmd
_RB2 = capture("35-b-rebuild-312")
assert _RB2.cmd == _BD.cmd


def live_rows(cap, cut14: int = 46):
    """Line 3 and the live-view rows 14-17 of a build capture: (texts, times). Row 14's text is
    cut at `cut14` characters (its tag needs room to grow); the others at 65. Line 3 (79 chars,
    "FINISHED", a run of spaces, "docker:default") is cut at 65 and its trailing spaces dropped,
    so its '…' follows FINISHED instead of floating at the row's end."""
    l3 = cap.line(3)
    texts, times = [l3[:64].rstrip() + " …" if len(l3) > 65 else l3], [None]
    for n in (14, 15, 16, 17):
        txt, tm = live_split(cap.line(n), width=cut14 if n == 14 else 65)
        texts.append(txt)
        times.append(tm)
    return texts, times


B_ROWS, B_TIMES = live_rows(_BD)
assert B_ROWS[0].startswith("[+] Building 54.0s") and B_TIMES[1:] == ["22.8s", "0.1s", "0.0s", "5.9s"]
assert B_ROWS[1].startswith(" => [2/5] RUN apt-get") and B_ROWS[4] == " => [5/5] RUN uv sync"
R_ROWS, R_TIMES = live_rows(_RB2)
assert R_ROWS[0].startswith("[+] Building 10.4s") and R_TIMES[4] == "3.4s"
assert R_ROWS[1].startswith(" => CACHED [2/5]") and R_ROWS[2].startswith(" => CACHED [3/5]")


def plain_lines(name: str, *ns: int) -> list[str]:
    """A plain build log's lines by FILE line number (read with newline="" so apt's lone '\r'
    progress rows don't shift the numbering; each line is checked against capture())."""
    with open(TERMINAL / "laptop" / f"{name}.txt", encoding="utf-8", newline="") as f:
        raw = [s.rstrip("\r") for s in f.read().split("\n")]
    cap = capture(name)
    out = []
    for n in ns:
        assert raw[n - 1] in cap.lines, (name, n, raw[n - 1])
        out.append(raw[n - 1])
    return out


PLAIN = plain_lines("32-b-build.plain", 341, 342, 343, 344)
assert PLAIN[0].endswith("Downloading cpython-3.15.0-linux-x86_64-gnu (download) (35.9MiB)"), PLAIN[0]
assert PLAIN[2].endswith("Using CPython 3.15.0") and PLAIN[3].endswith("/home/app/.venv"), PLAIN
PLAIN31 = plain_lines("35-b-rebuild-312.plain", 31)
assert PLAIN31[0].endswith("Using CPython 3.12.15 interpreter at: /usr/local/bin/python3"), PLAIN31

PYV = capture("01-python-version", B)
assert PYV.cmd == "which python; python --version; readlink -f $(which python)", PYV.cmd
PYV_CMD, RL_CMD = "python --version", "readlink -f $(which python)"   # the script types these two
assert PYV.line(3) == "Python 3.15.0"
assert PYV.line(4) == "/home/app/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu/bin/python3.15"
UV_DIR = "/home/app/.local/share/uv/python/"

UVA = capture("02-uv-add", B)
assert UVA.cmd == "uv add google-cloud-storage google-genai", UVA.cmd
UVA_OUT = UVA.at((2, 3))
assert UVA_OUT[0].startswith("Resolved 35 packages") and UVA_OUT[1].startswith("Checked 34 packages")

HELP = capture("04-help", B)
assert HELP.cmd == "python cli.py --help"
HELP_OUT = HELP.at((2, 10))
assert HELP_OUT[0] == "usage: cli.py [-h] [-d] [-g] [-u]"
assert _RB[115:124] == HELP_OUT, "the help must match generate_text/README.md lines 116-124"

FIX = capture("34-b-fix-requires-python")
assert FIX.cmd == "grep -n requires-python pyproject.toml; git status --short .", FIX.cmd
GREP_CMD, GIT_CMD = "grep -n requires-python pyproject.toml", "git status --short ."
GREP_OUT = FIX.at(2)
GIT_OUT = FIX.at((3, 5))
assert GREP_OUT == ['4:requires-python = ">=3.12"'] and GIT_OUT == [" M pyproject.toml", "?? Dockerfile",
                                                                     "?? uv.lock"], (GREP_OUT, GIT_OUT)
FIXED_LINE = GREP_OUT[0].split(":", 1)[1]                 # the edited line 4, as grep printed it

PY312 = capture("05-python-version-312", B)
assert PY312.cmd == "python --version; readlink -f $(which python)"   # typed as one line (script)
PY312_OUT = PY312.at((2, 3))
assert PY312_OUT == ["Python 3.12.15", "/usr/local/bin/python3.12"], PY312_OUT

CLI = "generate_text/cli.py"
assert excerpt(CLI, 19, 19, cut_comments=True) == 'group_name = "pavlos"  # …'
M73 = textwrap.dedent(excerpt(CLI, 73, 76))
assert [s.strip() for s in M73.split("\n")] == [s.strip() for s in excerpt(CLI, 73, 76).split("\n")]
assert M73.split("\n")[0] == 'model_name = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")'
assert M73.split("\n")[2] == "response = client.models.generate_content("


def _src(n: int) -> str:
    return excerpt(CLI, n, n).strip()


assert _src(74) == 'print(input_prompt,"\\n\\n\\n")', _src(74)
assert _src(80) == 'print("Generated text:")' and _src(81) == "print(paragraph)"
assert _src(84) == 'with open(paragraph_file, "w") as f:'
assert _src(103) == 'print("Uploading:",destination_blob_name, text_file)'
assert source_text("generate_text/pyproject.toml").split("\n")[3] == 'requires-python = ">=3.14"'

_R = source_text("README.md").split("\n")
README_CMDS = _R[140:143]                          # README.md lines 141-143 (Quick Reference)
assert README_CMDS == ["python cli.py --download", "python cli.py --generate", "python cli.py --upload"]
GEMINI_CMD = ['docker run --rm -ti -e GEMINI_MODEL=<current model> \\',
              '    -v "$(pwd):/app" generate_text']   # extra: shown, not typed

LOOK = [("your prompt, printed", "line 74"), ("Generated text:", "line 80"),
        ("a long podcast script", "line 81"),
        (f"text_paragraphs/{GROUP}/input-….txt on your laptop", "line 84"),
        (f"Uploading: text_paragraphs/{GROUP}/…", "line 103")]
FAIL = "if it fails: 429 RESOURCE_EXHAUSTED → the class shares one quota; wait a minute, retry"

PONDER_Q = ("The image has Python 3.12.\nThis pyproject.toml says >=3.14.\n"
            "Which Python will the venv use?")

# ------------------------------------------------------------------ layout
TOP = 2.8                         # top of a picture under the tracker band (y 2.92..3.5)
EDGE = 6.45
AX_Y = 0.55                       # V7's axis in beats 5-7 (the ponder card / log panel under it)
AX_Y14 = 1.3                      # V7's axis in beat 14 (a 1-row panel fits under it)
ST_X, ST_FLOOR = 4.45, 0.45       # small V2 above the 7-row terminal (top 0.17)
H_V2 = {"base": 0.42, "apt": 0.55, "workdir": 0.07, "copy": 0.26, "sync": 0.38}


# ------------------------------------------------------------------ small helpers
def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None):
    if left is not None:
        m.shift(RIGHT * (left - m.get_left()[0]))
    if right is not None:
        m.shift(RIGHT * (right - m.get_right()[0]))
    if top is not None:
        m.shift(UP * (top - m.get_top()[1]))
    if bottom is not None:
        m.shift(UP * (bottom - m.get_bottom()[1]))
    if cx is not None:
        m.set_x(cx)
    if cy is not None:
        m.set_y(cy)
    return m


def seed_prompt(t):
    """A bare prompt on terminal t, without animation (the terminal fades in with it)."""
    ln = mono_line(t.prompt + " ", t.size, INK, t2c=t._prompt_colors(t.prompt))
    t._place(ln, len(t.lines))
    t.lines.add(ln)
    ln.bare = True
    return ln


def room(scene, t, n: int):
    """Make room for n new rows: the oldest rows fade where they are, then the rest move up
    (Terminal's own scroll slides old rows over the title bar)."""
    over = len(t.lines) + n - t.rows
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        over -= 1                                   # type_cmd replaces the bare prompt
    if over <= 0:
        return
    gone = t.lines.submobjects[:over]
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(VGroup(*gone)), run_time=0.2)
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=0.25)


def reset(scene, t, rows: int, extra=(), run_time: float = 0.5):
    """Clear the terminal and resize it to `rows` in one move (the old rows fade while the frame
    changes; `extra` animations play along)."""
    old = list(t.lines)
    scene.add(*old)                                   # top-level, so they can fade on their own
    for m in old:
        t.lines.remove(m)
    fades = [FadeOut(VGroup(*old))] if old else []
    resize(scene, t, rows, run_time=run_time, extra=[*fades, *extra])
    scene.remove(*old)


def tcmd(scene, t, cmd: str, type_time: float | None = None):
    """Type `cmd` at the prompt (scrolling first so nothing slides over the title bar)."""
    p = t.prompt + " "
    room(scene, t, len(t.fold(p + cmd, first_prefix=len(p))))
    return type_cmd(scene, t, cmd, type_time)


def tprint(scene, t, lines, wrap: bool = False, run_time: float = 0.5, color=None, lag: float = 0.15):
    n = sum(max(1, -(-len(s) // t.max_chars)) if wrap else 1 for s in lines)
    room(scene, t, n)
    kw = {} if color is None else {"color": color}
    return t.print(scene, lines, wrap=wrap, run_time=run_time, lag=lag, **kw)


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded)."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def uline(line, sub, color, stroke=3.5, occ=0, pad=0.02) -> Line:
    """A Line under substring `sub` of terminal row `line`, in the gap under the row."""
    g = substring(line, sub, occ)
    y = line.strut.get_bottom()[1] + 0.01
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def rbar(lines, color, opacity=0.2, pad=0.08, right=None) -> Rectangle:
    """A translucent bar behind whole terminal rows."""
    lines = lines if isinstance(lines, (list, tuple)) else [lines]
    left = min(ln.glyphs.get_left()[0] for ln in lines) - pad
    rx = right if right is not None else max(ln.glyphs.get_right()[0] for ln in lines) + pad
    top = lines[0].strut.get_top()[1] + 0.03
    bot = lines[-1].strut.get_bottom()[1] - 0.03
    return Rectangle(width=rx - left, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([(left + rx) / 2, (top + bot) / 2, 0])


def ttag(time: str, color=S.GREY) -> VGroup:
    """A live-view row's time as a compact GREY tag (20 pt, 0.34 tall: rows are 0.40 apart)."""
    t = label(time, 20, color)
    fr = RoundedRectangle(width=t.width + 0.3, height=0.34, corner_radius=0.17, stroke_color=color,
                          stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.box, g.text = fr, t
    return g


def at_right(m, t, line):
    """Put m at the right end of terminal row `line`, inside the frame."""
    return m.move_to(line.strut).align_to(t.box, RIGHT).shift(LEFT * 0.12)


def beside_or_below(mob, t, line, buff: float = 0.3):
    """beside(), but when the row is full (the tag would cover its end) the tag sits at the right
    end of the row below, which is still empty there."""
    beside(mob, t, line, buff=buff)
    row = line.rows[-1] if hasattr(line, "rows") else line
    if mob.get_left()[0] < row.glyphs.get_right()[0] + 0.1:
        mob.set_y(row.strut.get_center()[1] - t.pitch)
    return mob


def tag20(s: str, color=S.GREY) -> VGroup:
    """A tag that fits inside one 22 pt terminal row (20 pt text)."""
    return tag(s, color, size=20)


def compact_ponder(question: str, width: float = 12.9, size: float = 24) -> VGroup:
    """pause_and_ponder's card (frame, header, question, timer bar) with less padding, wide enough
    to cover the strip. Returns VGroup(frame, header, question, bar)."""
    card = ponder_card(question, width=width, size=size)
    fr, head, q, bar = card
    body = VGroup(head, q).arrange(DOWN, buff=0.14)
    fr.become(RoundedRectangle(width=width, height=body.height + 0.55, corner_radius=0.2,
                               stroke_color=TURN, stroke_width=3).set_fill(S.BG, 1))
    body.move_to(fr).shift(UP * 0.09)
    bar.become(Line(fr.get_corner(DL) + RIGHT * 0.3 + UP * 0.17, fr.get_corner(DR) + LEFT * 0.3 + UP * 0.17,
                    color=TURN, stroke_width=4))
    return card


def recipe_rows(tr) -> VGroup:
    """The section's 13 step titles as a numbered list under the tracker (20 pt)."""
    rows = VGroup()
    for k, s in enumerate(tr.steps, start=1):
        n = sans(f"{k}", 20, TURN)
        n.move_to([-6.1, 2.62 - (k - 1) * 0.33, 0], aligned_edge=RIGHT)
        txt = sans(s, 20, INK).move_to([-5.9, n.get_center()[1], 0], aligned_edge=LEFT)
        rows.add(VGroup(n, txt))
    return rows


def commands_card(where: str, cmds) -> VGroup:
    """A static GREY card listing commands (mono), header `where` above. .frame .rows .header"""
    rows = VGroup(*[mono_line(c, 20, INK) for c in cmds]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = box(rows.width + 0.5, rows.height + 0.36, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    rows.move_to(fr)
    path, _, rest = where.partition(" · ")
    head = VGroup(mono(path, 20, S.GREY), label(f"· {rest}", 20, S.GREY)).arrange(RIGHT, buff=0.12)
    head.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head
    return g


def make_stack() -> LayerStack:
    """A small V2 (five slabs as S11 left them; no stamps), floor at (ST_X, ST_FLOOR)."""
    st = LayerStack(slab_w=3.5)
    for name in ("base", "apt", "workdir", "copy", "sync"):
        s = st.make(name, h=H_V2[name])
        st.slabs[name] = s
        st.order.append(name)
        st.add(s)
    st.move_to([ST_X, ST_FLOOR, 0], aligned_edge=DOWN)
    return st


def make_v7(axis_y: float):
    """V7 for generate_text: the axis 3.10..3.16 with the interval from 3.14, and the image's dot
    at 3.12 (label below). Returns (vl, d12)."""
    vl = VersionLine(10, 16, lo=14)
    vl.shift(UP * (axis_y - vl.axis.get_center()[1]))
    d12 = vl.dot(12, "image · Python 3.12", SYSTEM, above=False)
    return vl, d12


def uv_dot(vl) -> VGroup:
    """The uv-managed 3.15.0: a PURPLE dot in a GREEN ring, on the axis at 3.15."""
    c = vl.point(15)
    ring = Circle(radius=0.19, stroke_color=VENV, stroke_width=4).move_to(c)
    d = Dot(c, radius=0.1, color=TOOL)
    return VGroup(ring, d)


def unfold_panel(lines, header: str, width: float = 12.9) -> VGroup:
    """A full-log panel (20 pt rows) headed by a plain GREY label, bottom at the frame's foot."""
    p = log_panel(lines, "x", width=width, size=20)
    head = label(header, 20, S.GREY)
    head.next_to(p.frame, UP, buff=0.1).align_to(p.frame, LEFT).shift(RIGHT * 0.12)
    p.remove(p.header)
    p.header = head
    p.add(head)
    place(p, cx=0)
    p.shift(UP * (-3.5 - p.frame.get_bottom()[1]))
    return p


def gemini_chip() -> VGroup:
    """The GEMINI_MODEL docker run, shown not typed: two mono rows (folded like the terminal)."""
    rows = VGroup(*[mono_line(s, 20, INK) for s in GEMINI_CMD]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = box(rows.width + 0.5, rows.height + 0.32, S.GREY, fill_opacity=0.14, radius=0.12)
    rows.move_to(fr)
    g = VGroup(fr, rows)
    g.frame, g.rows = fr, rows
    return g


# ------------------------------------------------------------------ the scene
class GenerateText(VoiceScene):
    def construct(self):
        assert len(SAY) == 15, f"S12 has {len(SAY)} SAY lines; this scene times 15"

        # ========================================================== 0 · same recipe; cd; the key
        tr_a = tracker("A", 13)
        t = term(P_A, 12)
        seed_prompt(t)
        fold = folder_glyph(0.42, LAPTOP)
        sname = mono("secrets/", 20, INK).next_to(fold, RIGHT, buff=0.14)
        kname = mono("mega-pipeline.json", 20, KEY).next_to(sname, RIGHT, buff=0.3)
        ill0 = illustration_tag().next_to(kname, RIGHT, buff=0.35)
        srow = VGroup(fold, sname, kname, ill0)
        place(srow, right=EDGE, cy=2.56)
        kname.align_to(sname, DOWN)
        key = key_glyph(0.3)
        key.move_to([fold.get_center()[0], 3.35, 0])
        key_in = fold[1].get_center() + DOWN * 0.02

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr_a, shift=DOWN * 0.1), run_time=0.4)
            tr = switch_section(self, tr_a, "B", None, run_time=0.7)
            vo.wait_until("follows the same recipe")
            rec = recipe_rows(tr)
            self.play(LaggedStart(*[TransformFromCopy(tr.dots[k], rec[k]) for k in range(13)],
                                  lag_ratio=0.07), run_time=1.1)
            self.wait(0.9)
            self.play(LaggedStart(*[rec[k].animate.scale(0.05).move_to(tr.dots[k]).set_opacity(0)
                                    for k in range(13)], lag_ratio=0.04), run_time=0.8)
            self.remove(rec)
            self.play(FadeIn(t), tr.goto(1), run_time=0.6)
            vo.wait_until("Steps 1 and 2")
            tcmd(self, t, CD, 0.8)
            t.set_prompt(P_B)
            ln0 = bare_prompt(self, t)
            self.play(Indicate(substring(ln0, B), color=TURN, scale_factor=1.12), run_time=0.6)
            vo.wait_until("and copy the key")
            self.play(tr.goto(2), FadeIn(VGroup(fold, sname, ill0)), FadeIn(key, shift=DOWN * 0.2),
                      run_time=0.5)
            self.play(key.animate.scale(0.62).move_to(key_in), run_time=0.6)
            self.play(FadeIn(kname, shift=LEFT * 0.15), Indicate(fold, color=KEY, scale_factor=1.15),
                      run_time=0.6)

        # ========================================================== 1 · ls -a; cat pyproject.toml (extra)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(srow, key)), caption_extra(tr, True), run_time=0.4)
            c1 = tcmd(self, t, LS_CMD, 0.4)
            pin(self, c1, beside(extra_tag(), t, c1), run_time=0.3)
            o1 = tprint(self, t, LS_OUT, run_time=0.6)
            vo.wait_until("this folder already has")
            pyp = o1[5]
            b_pyp = rbar(pyp, VENV, 0.22)
            self.play(FadeIn(b_pyp), pyp.glyphs.animate.set_color(VENV), run_time=0.4)
            stick(self, pyp, b_pyp)
            c2 = tcmd(self, t, CAT_CMD, 0.6)
            pin(self, c2, beside_or_below(extra_tag(), t, c2), run_time=0.3)
            o2 = tprint(self, t, CAT_OUT, run_time=0.7, lag=0.1)
            r12, r14, r15 = o2[3], o2[5], o2[6]
            vo.wait_until("listing both packages")
            b_pk = rbar([r14, r15], VENV, 0.2)
            listed = tag("already listed", VENV)
            place(listed, left=r14.glyphs.get_right()[0] + 0.4,
                  cy=(r14.strut.get_center()[1] + r15.strut.get_center()[1]) / 2)
            self.play(FadeIn(b_pk), r14.glyphs.animate.set_color(VENV), r15.glyphs.animate.set_color(VENV),
                      run_time=0.5)
            stick(self, r14, b_pk)
            pin(self, r14, listed, run_time=0.4)
            vo.wait_until("and requiring Python")
            b12 = rbar(r12, TURN, 0.22)
            self.play(FadeIn(b12), substring(r12, '">=3.14"').animate.set_color(TURN), run_time=0.5)
            stick(self, r12, b12)
            self.play(Indicate(substring(r12, "3.14"), color=TURN, scale_factor=1.3), run_time=0.6)
            vo.wait_until("Leave that until step 13")
            leave = beside(tag20("leave it · step 13"), t, r12, buff=0.4)
            pin(self, r12, leave, run_time=0.4)
            self.play(Indicate(tr.dots[12], color=TURN, scale_factor=2.4), run_time=0.8)

        # ========================================================== 2 · surprise one: uv init fails
        rchip = readme_chip("generate_text/README.md · lines 20–24", "uv init --bare")
        place(rchip, left=-6.4, top=2.8)
        err_t = erratum_tag()
        place(err_t, left=rchip.get_right()[0] + 0.3, cy=rchip.get_center()[1])
        s_line = strike(rchip.phrase)
        note = VGroup(label("skip it ·", 20, S.GREY), mono("main.py", 20, S.GREY),
                      label("is a leftover", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        note[1].align_to(note[0], DOWN)
        place(note, left=rchip.where.get_left()[0], top=rchip.get_bottom()[1] - 0.16)

        with self.voiceover(SAY[2]) as vo:
            self.play(tr.goto(3), run_time=0.4)
            resize(self, t, 10, run_time=0.6)
            tcmd(self, t, UVI.cmd, 0.6)
            o3 = tprint(self, t, UVI_OUT, wrap=True, color=ERR, run_time=0.5)
            vo.wait_until("the project is already")
            u3 = uline(o3[0], "Project is already initialized", ERR)
            pin(self, o3[0], u3, run_time=0.5, anim=Create(u3))
            self.play(Indicate(substring(o3[1], "`pyproject.toml` file exists"), color=ERR, scale_factor=1.06),
                      run_time=0.7)
            vo.wait_until("The README still says")
            self.play(FadeIn(rchip, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(rchip.phrase, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("a small mistake")
            self.play(FadeIn(err_t, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("skip step 3")
            self.play(Create(s_line), Indicate(tr.dots[2], color=TURN, scale_factor=2.2), run_time=0.5)
            self.play(FadeIn(note, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("and ignore the leftover")
            self.play(Indicate(note[1], color=INK, scale_factor=1.2), run_time=0.7)

        # ========================================================== 3 · step 4: line 3 drops ffmpeg
        df_a = file_panel(DF_A, 3, 3, "transcribe_audio/Dockerfile")
        place(df_a, left=-6.4, top=TOP - 0.05)
        cap_a = VGroup(label("from", 20, S.GREY), mono("transcribe_audio/README.md", 20, S.GREY),
                       label("· lines 41–90", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        place(cap_a, right=EDGE, cy=df_a.header.get_center()[1])
        assert cap_a.get_left()[0] > df_a.header.get_right()[0] + 0.3
        df_b = file_panel(DF_B, 3, 3, "generate_text/Dockerfile")
        place(df_b, left=-6.4, top=df_a.get_bottom()[1] - 0.45)
        cap_b = VGroup(label("the only difference ·", 20, S.GREY), mono("generate_text/README.md", 20, S.GREY),
                       label("line 45", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        place(cap_b, left=df_b.code.get_left()[0] + 0.1, top=df_b.get_bottom()[1] - 0.2)
        ff = code_span(df_a.code, 0, "ffmpeg")
        s_ff = Line(ff.get_left() + LEFT * 0.06, ff.get_right() + RIGHT * 0.06, color=S.GREY, stroke_width=4)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(rchip, err_t, s_line, note)), tr.goto(4), run_time=0.5)
            resize(self, t, 3, run_time=0.7)
            self.play(FadeIn(df_a, shift=DOWN * 0.1), FadeIn(cap_a), run_time=0.6)
            vo.wait_until("except line 3 drops ffmpeg")
            self.play(Indicate(ff, color=SYSTEM, scale_factor=1.15), run_time=0.5)
            self.play(Create(s_ff), ff.animate.set_opacity(0.45), run_time=0.4)
            self.play(FadeIn(df_b, shift=DOWN * (df_a.get_center()[1] - df_b.get_center()[1])), run_time=0.9)
            vo.wait_until("since this component")
            self.play(FadeIn(cap_b, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Copy yours")
            bar_b = line_bar(df_b.code, 0, TURN)
            self.play(FadeIn(bar_b), run_time=0.4)
            self.play(Indicate(code_span(df_b.code, 0, '"build-essential"'), color=SYSTEM, scale_factor=1.12),
                      run_time=0.7)

        # ========================================================== 4 · step 5: build; apt runs again
        st = make_stack()
        card = ConfigCard(width=6.6, rows=1)
        place(card, left=-6.4, cy=1.55)
        arg = card.line("DEBIAN_PACKAGES · build-essential ffmpeg", SYSTEM, key="arg")
        card.add(arg)
        apt = st.slabs["apt"]

        with self.voiceover(SAY[4]) as vo:
            reset(self, t, 7, run_time=0.6,
                  extra=[FadeOut(VGroup(df_a, df_b, cap_a, cap_b, s_ff, bar_b)), tr.goto(5),
                         FadeIn(st, shift=UP * 0.15), FadeIn(card, shift=UP * 0.15)])
            c4 = tcmd(self, t, BUILD_CMD, 0.6)
            o4 = tprint(self, t, B_ROWS, run_time=0.4, lag=0.1)
            tags4 = [None] + [at_right(ttag(tm), t, o4[i]) for i, tm in enumerate(B_TIMES[1:], start=1)]
            self.play(*[FadeIn(g) for g in tags4[1:]], run_time=0.25)
            for i in range(1, 5):
                stick(self, o4[i], tags4[i])
            vo.wait_until("and the big RUN step")
            r14 = o4[1]
            k2 = substring(r14, "[2/5]")
            box2 = SurroundingRectangle(k2, color=CTR, buff=0.05, stroke_width=2.5, corner_radius=0.05)
            bd2 = step_badge(2, CTR, size=20, radius=0.17)
            place(bd2, left=r14.glyphs.get_right()[0] + 0.2, cy=r14.strut.get_center()[1])
            nc = ttag("22.8s · not cached", SYSTEM)
            place(nc, right=tags4[1].get_right()[0], cy=tags4[1].get_center()[1])
            assert nc.get_left()[0] > bd2.get_right()[0] + 0.1, (nc.get_left(), bd2.get_right())
            self.play(Create(box2), k2.animate.set_color(CTR), FadeIn(bd2, scale=1.3), Transform(tags4[1], nc),
                      run_time=0.5)
            stick(self, r14, box2, bd2)
            vo.wait_until("because the package list")
            arg_to = sans("DEBIAN_PACKAGES · build-essential", 20, SYSTEM).move_to(arg.get_left(), aligned_edge=LEFT)
            p0 = arg_to.get_right() + RIGHT * 0.15
            p1 = apt.box.get_left() + LEFT * 0.05
            thread = CubicBezier(p0, p0 + RIGHT * 1.2, p1 + LEFT * 1.2, p1).set_stroke(SYSTEM, 2.5)
            self.play(card.restyle("arg", "DEBIAN_PACKAGES · build-essential"), Create(thread), run_time=0.7)
            saved = VGroup(apt.box.copy(), apt.label.copy())
            self.play(apt.box.animate.set_opacity(0).scale(1.04), apt.label.animate.set_opacity(0),
                      run_time=0.4)
            self.play(Transform(apt.box, saved[0]), Transform(apt.label, saved[1]), run_time=0.5)
            vo.wait_until("Pause and run it")
            yt4 = beside(your_turn(), t, c4)
            pin(self, c4, yt4, run_time=0.4)
            self.play(Wiggle(yt4, scale_value=1.12, rotation_angle=0.02 * TAU),
                      Indicate(tags4[4], color=TURN, scale_factor=1.25), run_time=0.8)

        # ========================================================== 5 · ponder: which Python?
        vl, d12 = make_v7(AX_Y)
        answers = VGroup(*[chip(s, S.GREY, size=22) for s in ("fail?", "use 3.12 anyway?", "something else?")])
        answers.arrange(RIGHT, buff=0.45)
        place(answers, cx=0, cy=2.35)
        pcard = compact_ponder(PONDER_Q)
        place(pcard, cx=0, bottom=-3.55)

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(st, card, thread)), run_time=0.5)
            resize(self, t, 3, run_time=0.7)
            self.play(FadeIn(vl.axis), FadeIn(vl.ticks), run_time=0.5)
            vo.wait_until("The image has Python 3.12")
            self.play(FadeIn(d12, shift=DOWN * 0.3), run_time=0.6)
            vo.wait_until("this pyproject.toml asks")
            self.play(GrowFromEdge(vl.band, LEFT), FadeIn(vl.band_label, shift=DOWN * 0.1), run_time=0.9)
            self.bring_to_back(vl.band)
            self.play(Indicate(d12.dot, color=SYSTEM, scale_factor=1.8), run_time=0.6)
            vo.wait_until("Which Python")
            self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.1) for a in answers], lag_ratio=0.3),
                      run_time=0.9)
        self.play(FadeIn(pcard, scale=0.95), run_time=0.6)
        pbar = pcard[3]
        self.play(pbar.animate(rate_func=linear).become(pbar.copy().scale(0.001, about_point=pbar.get_start())),
                  run_time=8)

        # ========================================================== 6 · the full log shows it
        panel = unfold_panel(PLAIN, "the same build, full log · lines 341–344")
        p_rows = panel.rows

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(pcard), FadeOut(answers), run_time=0.4)
            r17 = t.lines[-1]
            assert r17.text == B_ROWS[4], r17.text
            b17 = rbar(r17, TURN, 0.3, right=t.box.get_right()[0] - 0.1)
            self.play(FadeIn(b17), run_time=0.3)
            self.play(Indicate(r17.glyphs, color=TURN, scale_factor=1.06), run_time=0.5)
            vo.wait_until("the full log shows it")
            self.play(FadeOut(t), ReplacementTransform(b17, panel.frame), FadeIn(panel.header), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(r) for r in p_rows], lag_ratio=0.15), run_time=0.6)
            self.remove(panel.frame, panel.header, *p_rows)
            self.add(panel)                                  # one mobject on the scene from here on
            vo.wait_until("uv downloaded its own")
            dl = "Downloading cpython-3.15.0-linux-x86_64-gnu"
            u_dl = uline(p_rows[0], dl, TOOL)
            u_mb = uline(p_rows[0], "(35.9MiB)", S.GREY)
            self.play(Create(u_dl), substring(p_rows[0], dl).animate.set_color(TOOL), run_time=0.6)
            self.play(Create(u_mb), run_time=0.4)
            vo.wait_until("3.15.0 at the time")
            v315 = substring(p_rows[2], "3.15.0")
            atr = ttag("at the time of recording")
            place(atr, left=p_rows[2].glyphs.get_right()[0] + 0.45, cy=p_rows[2].strut.get_center()[1])
            self.play(v315.animate.set_color(TURN), FadeIn(atr, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("and built the venv")
            venv = substring(p_rows[3], "/home/app/.venv")
            u_v = uline(p_rows[3], "/home/app/.venv", VENV)
            self.play(venv.animate.set_color(VENV), Create(u_v), run_time=0.5)

        # ========================================================== 7 · V7: outside, so uv fetched one
        arrow = vl.download_arrow(15, "3.15.0 · uv-managed · 35.9 MiB")
        ud = uv_dot(vl)
        newest = label("the newest at the time of recording", 20, S.GREY)
        place(newest, cx=vl.point(15)[0], cy=d12.text.get_center()[1])
        if newest.get_right()[0] > EDGE:
            place(newest, right=EDGE)

        with self.voiceover(SAY[7]) as vo:
            self.play(d12.dot.animate.set_color(ERR), run_time=0.4)
            self.play(Indicate(d12.dot, color=ERR, scale_factor=1.8), run_time=0.6)
            vo.wait_until("so uv fetched")
            self.play(GrowArrow(arrow.arrow), FadeIn(arrow[1], shift=DOWN * 0.1), run_time=0.7)
            self.play(FadeIn(ud, scale=1.6), run_time=0.5)
            self.play(FadeIn(newest, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("as in lecture 2")
            self.play(Indicate(ud, color=VENV, scale_factor=1.4), Indicate(v315, color=TURN, scale_factor=1.3),
                      run_time=0.8)

        # ========================================================== 8 · step 6: run; Python 3.15.0 (extra)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(panel, u_dl, u_mb, atr, u_v)), FadeOut(VGroup(vl, d12, arrow, ud, newest)),
                      FadeIn(t), tr.goto(6), run_time=0.5)
            resize(self, t, 10, run_time=0.5)
            tcmd(self, t, RUN, 0.9)
            self.play(*enter_container(t, B), caption_extra(tr, True), run_time=0.4)
            vo.wait_until("and an extra check")
            c9 = tcmd(self, t, PYV_CMD, 0.4)
            pin(self, c9, beside(extra_tag(), t, c9), run_time=0.25)
            o9 = tprint(self, t, [PYV.line(3)], run_time=0.25)
            self.play(Indicate(substring(o9[0], "3.15.0"), color=TURN, scale_factor=1.3), run_time=0.5)
            c10 = tcmd(self, t, RL_CMD, 0.6)
            pin(self, c10, beside(extra_tag(), t, c10), run_time=0.25)
            o10 = tprint(self, t, [PYV.line(4)], wrap=True, run_time=0.3)
            assert o10[0].text.startswith(UV_DIR), o10[0].text
            vo.wait_until("from uv's folder")
            u_uv = uline(o10[0], UV_DIR, TOOL)
            self.play(Create(u_uv), substring(o10[0], UV_DIR).animate.set_color(TOOL), run_time=0.6)
            stick(self, o10[0], u_uv)

        # ========================================================== 9 · step 7: uv add, nothing new
        with self.voiceover(SAY[9]) as vo:
            self.play(tr.goto(7), run_time=0.4)
            tcmd(self, t, UVA.cmd, 0.9)
            o11 = tprint(self, t, UVA_OUT, run_time=0.4)
            vo.wait_until("since both packages")
            nn = beside(tag20("nothing new: both already listed"), t, o11[1], buff=0.4)
            pin(self, o11[1], nn, run_time=0.4)
            self.play(Indicate(substring(o11[1], "Checked 34 packages"), color=INK, scale_factor=1.08),
                      run_time=0.6)
            vo.wait_until("it only writes")
            nn2 = tag20("nothing new: both already listed · writes uv.lock")
            place(nn2, left=nn.get_left()[0], cy=nn.get_center()[1])
            self.play(Transform(nn, nn2), run_time=0.5)

        # ========================================================== 10 · steps 8-9: group name; --help
        p19 = src_panel(CLI, 19, 19, cut_comments=True, size=20)
        ins = editor_inset(p19)
        place(ins, right=EDGE, top=TOP + 0.02)
        assert ins.get_bottom()[1] > strip_top(8) + 0.08, ins.get_bottom()
        gn = code_span(p19.code, 0, "group_name")
        u_gn = under(gn, TURN)
        here = sans("line 19 here", 22, TURN)
        place(here, right=ins.get_left()[0] - 0.3, cy=gn.get_center()[1])

        with self.voiceover(SAY[10]) as vo:
            resize(self, t, 8, run_time=0.6, extra=[tr.goto(8), FadeIn(ins, shift=DOWN * 0.15)])
            self.play(gn.animate.set_color(TURN), Create(u_gn), run_time=0.5)
            vo.wait_until("here on line 19")
            self.play(FadeIn(here, shift=RIGHT * 0.1), run_time=0.4)
            self.play(Indicate(gn, color=TURN, scale_factor=1.15), run_time=0.5)
            vo.wait_until("and check the help")
            reset(self, t, 10, run_time=0.5, extra=[tr.goto(9), FadeOut(VGroup(ins, u_gn, here), shift=UP * 0.1)])
            c12 = tcmd(self, t, HELP.cmd, 0.5)
            o12 = tprint(self, t, HELP_OUT, run_time=0.6, lag=0.08)
            vo.wait_until("which matches the README")
            ok = VGroup(check_mark(0.3, VENV),
                        VGroup(label("=", 20, S.GREY), mono("generate_text/README.md", 20, S.GREY),
                               label("· lines 116–124", 20, S.GREY)).arrange(RIGHT, buff=0.12))
            ok.arrange(RIGHT, buff=0.18)
            beside(ok, t, o12[2], buff=0.4)
            pin(self, o12[2], ok, run_time=0.5)
            vo.wait_until("Pause and catch up")
            yt10 = beside(your_turn(), t, c12)
            pin(self, c12, yt10, run_time=0.4)
            self.play(Wiggle(yt10, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.7)

        # ========================================================== 11 · steps 10-12; Gemini; the model date
        rcard = commands_card("README.md · lines 141–143", README_CMDS)
        place(rcard, left=-6.4, bottom=-1.44 + 0.2)
        same = tag("same as -d · -g · -u", S.GREY)
        place(same, left=rcard.get_right()[0] + 0.35, cy=rcard.frame.get_center()[1])
        p73 = code_panel(M73, CLI, 73, "python", font_size=20)
        place(p73, left=-6.4, top=TOP)
        c73 = p73.code
        u_def = under(code_span(c73, 0, '"gemini-2.5-flash-lite"'), TURN)
        gem = cloud_group()
        place(gem, right=EDGE - 0.1, top=p73.get_bottom()[1] - 0.25)
        cost = cost_tag()
        place(cost, right=gem.title.get_right()[0], top=gem.title.get_bottom()[1] - 0.2)
        note11 = VGroup(label("Vertex AI retires", 20, S.GREY), mono("gemini-2.5-flash-lite", 20, S.GREY),
                        label("on 2026-10-20 · then:", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        gchip = gemini_chip()
        xt = extra_tag()
        body = VGroup(note11, VGroup(gchip, xt).arrange(RIGHT, buff=0.3, aligned_edge=UP))
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        ncard_fr = box(body.width + 0.5, body.height + 0.4, S.GREY, fill=S.BG, fill_opacity=1, radius=0.12)
        ncard_fr.move_to(body)
        ncard = VGroup(ncard_fr, body)
        gap73 = (c73.code_lines[0].get_bottom()[1] + c73.code_lines[1].get_top()[1]) / 2
        place(ncard, left=c73.get_left()[0] + 0.25, top=gap73)
        nfr0 = box(note11.width + 0.5, note11.height + 0.4, S.GREY, fill=S.BG, fill_opacity=1, radius=0.12)
        place(nfr0, left=ncard_fr.get_left()[0], top=ncard_fr.get_top()[1])
        u_env1 = under(code_span(c73, 0, '"GEMINI_MODEL"'), TURN)
        cost_home = np.array([EDGE - cost.width / 2, -1.44 + 0.12 + cost.height / 2, 0])
        u_env2 = under(substring(gchip.rows[0], "GEMINI_MODEL"), TURN)

        with self.voiceover(SAY[11]) as vo:
            reset(self, t, 3, run_time=0.6, extra=[FadeIn(rcard, shift=UP * 0.1), FadeIn(same)])
            for k, cmd in enumerate(README_CMDS):
                self.play(tr.goto(10 + k), Indicate(rcard.rows[k], color=TURN, scale_factor=1.05), run_time=0.35)
                type_cmd(self, t, cmd, 0.6)
            vo.wait_until("The generate step")
            self.play(FadeOut(VGroup(rcard, same)), FadeIn(p73, shift=DOWN * 0.1), run_time=0.5)
            bar = line_bar(c73, 0, TURN)
            self.play(FadeIn(bar), Create(u_def), FadeIn(gem), run_time=0.5)
            self.play(Transform(bar, line_bar(c73, 2, TURN)), run_time=0.4)
            pg = page_token().move_to(c73.code_lines[2].get_right() + RIGHT * 0.5)
            self.play(FadeIn(pg, scale=0.6), run_time=0.3)
            self.play(pg.animate.move_to(gem.shape.get_center()), run_time=0.9)
            self.play(FadeOut(pg, scale=0.4), Indicate(gem.title, color=CLOUD, scale_factor=1.1),
                      FadeIn(cost, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Google retires")
            self.play(Transform(bar, line_bar(c73, 0, TURN)), FadeOut(gem), cost.animate.move_to(cost_home),
                      run_time=0.5)
            full_fr = ncard_fr.copy()
            ncard_fr.become(nfr0)
            self.play(FadeIn(ncard_fr), FadeIn(note11, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("after that, start the container")
            self.play(Transform(ncard_fr, full_fr), run_time=0.4)
            self.play(FadeIn(gchip, shift=DOWN * 0.1), FadeIn(xt), run_time=0.5)
            vo.wait_until("in the Gemini model variable")
            self.play(Create(u_env1), Create(u_env2), run_time=0.5)
            self.play(Indicate(substring(gchip.rows[0], "GEMINI_MODEL=<current model>"), color=TURN,
                               scale_factor=1.06), run_time=0.7)

        # ========================================================== 12 · with your key, look for
        lf = LookFor(LOOK, fail=FAIL)
        place(lf, cx=0, top=TOP)

        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(VGroup(p73, bar, u_def, ncard, u_env1, u_env2)), run_time=0.5)
            self.play(FadeIn(lf), run_time=0.4)
            lf.write_item(self, 0, run_time=0.4)
            vo.wait_until("generated text")
            lf.write_item(self, 1, run_time=0.4)
            vo.wait_until("and a long podcast")
            lf.write_item(self, 2, run_time=0.4)
            lf.write_item(self, 3, run_time=0.4)
            vo.wait_until("then the upload")
            lf.write_item(self, 4, run_time=0.4)
            lf.write_fail(self, run_time=0.4)
            vo.wait_until("Pause and run all three")
            last = t.lines[-1]
            yt12 = beside(your_turn(), t, last)
            pin(self, last, yt12, run_time=0.4)
            self.play(Wiggle(yt12, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.7)

        # ========================================================== 13 · step 13: exit; the fix; git status
        pp_old = src_panel("generate_text/pyproject.toml", 4, 4)
        pp_new = code_panel(FIXED_LINE, "generate_text/pyproject.toml", 4, "toml")
        ins13 = editor_inset(pp_old)
        place(ins13, right=EDGE, top=TOP - 0.02)
        pp_new.move_to(pp_old)
        old_v = code_span(pp_old.code, 0, '">=3.14"')
        new_v = code_span(pp_new.code, 0, '">=3.12"').set_color(VENV)
        fixtag = tag("the fix · not in the README", S.GREY)
        place(fixtag, right=ins13.get_left()[0] - 0.3, cy=old_v.get_center()[1])

        with self.voiceover(SAY[13]) as vo:
            last.remove(yt12)
            self.play(FadeOut(lf), FadeOut(cost), FadeOut(yt12), tr.goto(13), run_time=0.5)
            resize(self, t, 8, run_time=0.6)
            tcmd(self, t, "exit", 0.3)
            self.play(*leave_container(t, P_B), run_time=0.5)
            vo.wait_until("brings the fix")
            self.play(FadeIn(ins13, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("lower the minimum")
            self.play(Transform(old_v, new_v), run_time=0.7)
            self.play(FadeIn(fixtag, shift=RIGHT * 0.1), run_time=0.4)
            self.play(caption_extra(tr, True), run_time=0.3)
            c13 = tcmd(self, t, GREP_CMD, 0.8)
            pin(self, c13, beside(extra_tag(), t, c13), run_time=0.3)
            o13 = tprint(self, t, GREP_OUT, run_time=0.3)
            self.play(substring(o13[0], '">=3.12"').animate.set_color(VENV), run_time=0.3)
            vo.wait_until("Git status lists")
            c14 = tcmd(self, t, GIT_CMD, 0.6)
            pin(self, c14, beside(extra_tag(), t, c14), run_time=0.3)
            o14 = tprint(self, t, GIT_OUT, run_time=0.4)
            self.play(Indicate(o14[1].glyphs, color=INK, scale_factor=1.12), run_time=0.5)
            vo.wait_until("this folder has no")
            ng = beside(tag20("no .gitignore here"), t, o14[1], buff=0.4)
            pin(self, o14[1], ng, run_time=0.4)
            yours = VGroup(label("yours also shows", 20, S.GREY), mono("M cli.py", 20, S.GREY),
                           label("(your group name)", 20, S.GREY)).arrange(RIGHT, buff=0.12)
            beside(yours, t, o14[0], buff=0.5)
            pin(self, o14[0], yours, run_time=0.4)

        # ========================================================== 14 · rebuild on 3.12; run; exit
        vl2, d12b = make_v7(AX_Y14)
        d12b.dot.set_color(ERR)
        ud2 = uv_dot(vl2)
        p31 = unfold_panel(PLAIN31, "full log · line 31", width=12.6)
        place(p31, cx=0, bottom=-1.44 + 0.12)
        assert p31.get_top()[1] < d12b.text.get_bottom()[1] - 0.08, (p31.get_top(), d12b.text.get_bottom())
        assert strip_top(6) < d12b.text.get_bottom()[1] - 0.1, d12b.text.get_bottom()
        u31 = uline(p31.rows[0], "Using CPython 3.12.15 interpreter at: /usr/local/bin/python3", SYSTEM)

        with self.voiceover(SAY[14]) as vo:
            reset(self, t, 7, run_time=0.45, extra=[FadeOut(VGroup(ins13, fixtag)), caption_extra(tr, False)])
            c15 = tcmd(self, t, BUILD_CMD, 0.6)
            o15 = tprint(self, t, R_ROWS, run_time=0.4, lag=0.08)
            tags15 = [at_right(ttag(tm), t, o15[i]) for i, tm in enumerate(R_TIMES[1:], start=1)]
            yt14 = beside(your_turn(), t, c15)
            self.play(*[FadeIn(g) for g in tags15], FadeIn(yt14, shift=LEFT * 0.1), run_time=0.3)
            for i, g in enumerate(tags15, start=1):
                stick(self, o15[i], g)
            stick(self, c15, yt14)
            vo.wait_until("uv sync now uses")
            resize(self, t, 3, run_time=0.5,
                   extra=[FadeIn(VGroup(vl2, d12b, ud2), shift=DOWN * 0.1)])
            r17b = t.lines[-1]
            b17b = rbar(r17b, TURN, 0.3, right=t.box.get_right()[0] - 0.1)
            self.play(ReplacementTransform(b17b, p31.frame), FadeIn(p31.header), FadeIn(p31.rows), run_time=0.5)
            self.remove(p31.frame, p31.header, p31.rows)
            self.add(p31)
            self.play(Create(u31), substring(p31.rows[0], "Using CPython 3.12.15 interpreter at: /usr/local/bin/"
                                                          "python3").animate.set_color(SYSTEM), run_time=0.4)
            self.play(*vl2.move_lo(12), d12b.dot.animate.set_color(SYSTEM), FadeOut(ud2), run_time=0.8)
            vo.wait_until("as does the next container")
            reset(self, t, 6, run_time=0.4, extra=[FadeOut(p31), FadeOut(u31), caption_extra(tr, True)])
            tcmd(self, t, RUN, 0.7)
            self.play(*enter_container(t, B), run_time=0.3)
            tcmd(self, t, PY312.cmd, 0.6)
            tprint(self, t, PY312_OUT, run_time=0.3, color=SYSTEM)
            vo.wait_until("Exit it")
            tcmd(self, t, "exit", 0.3)
            self.play(*leave_container(t, P_B), run_time=0.3)
            vo.wait_until("Better still")
            self.play(Indicate(vl2.band_label, color=VENV, scale_factor=1.12), run_time=0.9)
            room(self, t, 1)
            bare_prompt(self, t)

        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)


def cloud_group() -> VGroup:
    """A BLUE cloud "Gemini · Vertex AI" (no logo). .shape .title"""
    from explainer.devops import cloud
    shp = cloud(2.0)
    ttl = sans("Gemini · Vertex AI", 22, CLOUD).next_to(shp, LEFT, buff=0.25)
    g = VGroup(shp, ttl)
    g.shape, g.title = shp, ttl
    return g
