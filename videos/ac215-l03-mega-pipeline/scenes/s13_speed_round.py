r"""S13 · Synthesize, translate, synthesize (README › synthesis_audio_en steps 1–12, translate_text
steps 1–13, synthesis_audio steps 1–12 and the optional ElevenLabs bonus; V2 shared slab, V5
callback, V8 Text-to-Speech and Translation halves, V1 + the schematic leaderboard).

Nothing here reaches Google or ElevenLabs (no key was available when the captures were made):
--download / --synthesis / --translate / --upload are typed, never run. The --help runs and the
bonus --download are the real keyless failures (tagged "recorded without the key"); what --help
prints with a key is the README's own block (assets/terminal/expected, tagged "expected").

Beats (script.md "## S13", one voiceover block each):
 0  B13 fades in and the tracker switches section: "README › synthesis_audio_en", 12 dots; the
    section name pulses. Terminal (12 rows, laptop, generate_text prompt). TRACKER C1: it types
    `cd ../synthesis_audio_en` (folds) → no output; the new prompt's folder pulses. TRACKER C2: a
    GOLD key drops from above its name into a GREY secrets/ folder above the terminal
    (mega-pipeline.json, tag illustration; it starts right of the tracker caption, never across it).
    TRACKER C3: `uv init --bare` → 40-c-uv-init.txt line 2; TRACKER C3 · extra: `cat
    pyproject.toml` (extra) → lines 3–7. "If it stamps 3.13": `>=3.11` GREEN (bar), GREY tag
    "3.13 or newer? → 3.12" on that row; "here and in D and E": the tag pulses (frame and text only,
    so it stays readable).
 1  TRACKER C4. The terminal shrinks to the strip. PANEL(files/synthesis_audio_en.Dockerfile: 3)
    headed `synthesis_audio_en/Dockerfile · line 3`, GREY "= generate_text's Dockerfile" beside it.
    "A small slip": README card `synthesis_audio_en/README.md · line 38` ("so keep ffmpeg in the
    system packages") + tag erratum by its header; "here and in E": GREY tag "same in
    synthesis_audio/README.md" right of the card; "the README's text says": the card's line
    pulses; "but its code block": card `… · line 45` (the ARG, mono); "which is right": GREEN
    check + "right", line 38 struck GREY; "leaves it out": GREY note "neither synthesis cli.py /
    uses ffmpeg".
 2  TRACKER C5. The panel and cards go; the terminal clears and grows to 7 rows while B's V2 stack
    (generate_text, five slabs) fades in above. It types `docker build -t synthesis_audio_en .` →
    41-c-build.txt lines 3, 14–17 (each row's time in a compact GREY tag). "build step 2 is
    cached": CACHED GREEN, `[2/5]` TEAL-boxed + TEAL circled 2; "and the build takes":
    `Building 0.6s` GREEN. "C's Dockerfile matches": C's stack (synthesis_audio_en) forms beside
    B's: its base and apt slabs are dashed ORANGE ghosts; GREY caption right "not CACHED? a line
    differs / from B's: fine, only slower". "so Docker reuses": a GREEN arrow "shared" from C's
    ghost apt slab to B's apt slab, which pulses; C's own thin slabs (WORKDIR, COPY, venv) drop on.
 3  TRACKER C6. V2 goes; the terminal clears to 10 rows. `docker run --rm -ti -v "$(pwd):/app"
    synthesis_audio_en` (folds; TEAL frame, "container · synthesis_audio_en"). TRACKER C7:
    `uv add google-cloud-storage google-cloud-texttospeech` → synthesis_audio_en/01-uv-add.txt
    lines 2, 8; "24 packages": "Installed 24 packages" GREEN, underlined.
 4  TRACKER C8: the terminal shrinks to 8 rows; editor inset (top right) CODE(synthesis_audio_en/
    cli.py: 18, comment cut), `group_name` YELLOW + underline. "then check the help": TRACKER C9,
    the inset goes, the terminal clears to 10 rows; `python cli.py --help` → 03-help.txt lines
    2–4, …, 25 (wrap). "Without a key": line 25 RED, underlined; GREY tag "recorded without the
    key". "line 22 builds": `line 22` YELLOW in the traceback; the terminal shrinks to the strip
    (command + line 25); V5 callback above: "cli.py runs top to bottom" (a GREY arrow down the
    left), CODE(cli.py: 22); a YELLOW dot runs down to it and line 22 gets a YELLOW bar. "as soon as
    the script starts": an arrow
    from line 22 to google.auth; the PINK signpost GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-
    pipeline.json; PINK arrows google.auth → signpost → secrets/, where a RED cross lands; the
    strip's RED line pulses. "before reading any flags": a dim `parse_args()` chip (line 118 ·
    reads --help) with GREY "never reached". "Pause and catch up": the picture gives way to
    PANEL(expected/synthesis_audio_en-help.txt: 3–10, "synthesis_audio_en/README.md · lines
    116–123"), tag expected + "with your key"; its help text gets a YELLOW outline; ▶ your turn
    beside the strip's `python cli.py --help` (held 1 s).
 5  The terminal and panel go. V8, Text-to-Speech half: TEAL container "C · synthesis_audio_en"
    left, BLUE cloud "Text-to-Speech · long audio" right, the drawer text_audios/group-01/ under
    the cloud; CODE(cli.py: 78) at the top. "The request carries the text": a long page in C.
    "and an address in the bucket": `gs://{bucket_name}/{audio_blob_name}` turns PINK; a copy
    flies down and becomes the PINK address label gs://…/text_audios/group-01/… above the link.
    "line 78": the panel's header pulses. "Google's long audio service": the page rides into the
    cloud and the label slides along the link up to it; GOLD "billed to the course project".
    "writes the speech straight there": a PINK dashed route from the cloud down to the drawer; the
    label lands on it and the drawer's name turns PINK. "never through your container": a GREY
    dashed return arrow to C, crossed RED.
 6  The panel swaps to CODE(cli.py: 88–91, comment cut). Line 88 bar: a TEAL ticket stub
    "operation" comes back to C. "for up to 300 seconds": line 90 bar; the ring beside the stub
    fills ("up to 300 s") while a waveform crate travels from the cloud straight down into
    text_audios/group-01/ (under its name). "then prints that": line 91 bar, the print pulses.
    "so C has no upload step": the README chip `README.md · line 151` "no separate --upload" (top
    right); the crate pulses (its frame and wave, not a white fill).
 7  TRACKER C10 → C12. V8 goes; the terminal returns (10 rows, container). One-line README chip
    `README.md · lines 148–149` + GREY tag "same as -d · -s" under the tracker. It types
    `python cli.py --download`, `python cli.py --synthesis` (a compact GOLD "billed" tag beside
    it), `exit` (GREY frame, laptop), `docker build -t synthesis_audio_en .` → 42-c-rebuild.txt
    lines 3, 14–17; CACHED GREEN. ▶ your turn: one 0.9 s move brings the terminal back, types
    `--download` and lands ▶ beside it just after "pause" (it wiggles on "pause to run" and stays
    until the section switch); a second ▶ by the rebuild once it is typed; the CACHED rows held 1 s.
 8  The terminal clears; the tracker switches: "README › translate_text", 13 dots, and the section
    name pulses. "races through the same setup": dots 1–5 ripple. The montage starts at "cd, key"
    (fast typing): TRACKER D1 `cd ../translate_text`; D2 the GOLD key drops into secrets/; D3
    `uv init --bare` → 50-d-uv-init.txt line 2; D4 PANEL(files/translate_text.Dockerfile: 3)
    flashes by (top right, its line barred YELLOW); D5 `docker build -t translate_text .` →
    51-d-build.txt lines 3, 14 (CACHED GREEN).
 9  The terminal clears to 8 rows (no scrolling in the race). TRACKER D6 `docker run …
    translate_text` (TEAL); D7 `uv add google-cloud-storage google-cloud-translate` →
    translate_text/01-uv-add.txt lines 2, 8; "and set the group name": D8, editor inset
    CODE(translate_text/cli.py: 18, comment cut), group_name YELLOW; it stays up while D9 types
    `python cli.py --help` → 03-help.txt lines 2–4, …, 22 (wrap), line 22 RED. "Like C, even
    help": tag "recorded without the key"; the inset goes, the terminal shrinks to the strip and
    PANEL(expected/translate_text-help.txt: 3–11, "translate_text/README.md · lines 116–124")
    appears above (expected, "with your key"). "Pause and catch up": the panel gives way to the
    static GREY card "translate_text · steps 1–9" (held ≥ 4 s) and ▶ your turn.
10  V8, Translation half: CODE(translate_text/cli.py: 58–65) top left; container "D ·
    translate_text" (with the laptop folder text_translated/group-01/ inside, GREY) and the BLUE
    cloud "Translation" along the bottom. A long page rides to the cloud (lines 60–61 YELLOW,
    "en" → "fr"), GOLD tag and GREY "no ticket stub" above the link. "the French comes straight
    back": a French page (FR chip) returns to D at once; "no ticket stub" pulses (frame and text).
    "is printed": line 65 bar. "and saved
    under": the page drops onto text_translated/group-01/, GREY "saved here · line 68 / on your
    laptop". "so D needs an upload": a dashed BLUE bucket drawer text_translated/group-01/ (top
    right, empty) with GREY "--upload puts it here · still empty".
11  TRACKER D10 → D13. V8 goes; the terminal returns (11 rows, container). README chip
    `README.md · lines 155–157` + "same as -d · -t · -u". It types the three commands (compact
    GOLD "billed" by --translate), `exit`, `docker build -t translate_text .` → 52-d-rebuild.txt
    lines 3, 14–17. "Pause to run" (the first words): the same 0.9 s move as in C10 brings the
    terminal back with `--download` typed and ▶ your turn beside it (wiggles; it stays until the
    section switch), a second ▶ by the rebuild once it is typed; the CACHED rows held 1 s.
12  The terminal clears to 8 rows while the tracker switches: "README › synthesis_audio", 12 dots.
    A quicker montage: E1 `cd ../synthesis_audio`; E2 key; E3 `uv init --bare` → 60 line 2; E4
    the Dockerfile line 3 flashes; E5 `docker build -t synthesis_audio .` → 61 lines 3, 14; E6
    `docker run … synthesis_audio`; E7 `uv add …texttospeech` → synthesis_audio/01 lines 2, 8; E8
    the cli.py:18 inset (group_name YELLOW, underlined) stays up while E9 types `python cli.py
    --help` → 03-help.txt line 25 (wrap, RED, recorded without the key). "its help text says":
    the inset goes, the strip; PANEL(expected/synthesis_audio-help.txt: 3–10) above (expected). "transcribe audio file to text": its line 5 "Synthesis audio
    from text" gets a GREEN bar + GREY "README"; the excerpt `synthesis_audio/cli.py · line 105
    (excerpt)` slides up over the whole strip, `ArgumentParser(description="Transcribe audio file
    to text")`, the description RED; "pasted from A's code": tag erratum + GREY "pasted from
    transcribe_audio/cli.py". "Pause and catch up": the static GREY card "synthesis_audio · steps
    1–9" (≥ 4 s), ▶ your turn.
13  TRACKER E10 → E11. No picture, so the terminal grows back to 10 rows (the --help lines stay
    on top); README chip `README.md · lines 162–163` + "same as -d · -s" under the tracker;
    `python cli.py --download`, `python cli.py --synthesis` (compact GOLD "billed"); "with your
    key": ▶ your turn beside `--download` (the --synthesis row is full with "billed").
14  The chips and ▶ go; the terminal shrinks to the strip (the two commands). The tracker
    switches: "README › ElevenLabs bonus" + tag optional (right of the widest caption, so no
    step's caption runs under it), 3 dots. A small schematic
    (illustration): a French page → GREY cloud "ElevenLabs" → a wave into the dashed bonus drawer
    output_audios_pp/, with the GREY note "synthesis_audio_en/README.md mentions cli_11.py too ·
    the file is in synthesis_audio/" under it; "in the instructor's voice" under the cloud. "It
    uses your own": the schematic goes; GOLD tag "your own ElevenLabs key and quota" (right). "a
    key file in secrets": TRACKER X1, GREY card `synthesis_audio/README.md · lines 139–142`: file
    secrets/11lab_api_key.txt holding `XI_API_KEY=…`. "your group name": editor inset
    CODE(synthesis_audio/cli_11.py: 19, comment cut), group_name YELLOW, caption
    "synthesis_audio/README.md · line 112: here too". "and uv add requests": TRACKER X2, the strip
    types `uv add requests` → 04-bonus-uv-add-requests.txt lines 2–3, GREY tag "already
    installed · now listed".
15  TRACKER X3. The cards go; a GREY README card `synthesis_audio/README.md · lines 151–153` with
    the three cli_11.py commands, the GOLD tag moves beside it; the terminal grows to 7 rows; it
    types `python cli_11.py --download` → 05-bonus-cli11-download.txt lines 2–3, 6 (wrap), line 6
    RED. "even download fails": underline + tag "recorded without the key". "the script reads that
    file": the card goes, the terminal shrinks to the strip, CODE(synthesis_audio/cli_11.py:
    30–39) slides in above; lines 33–37 YELLOW, YELLOW "read at start-up". "as soon as it starts":
    line 30 (the path) and line 33 pulse.
16  The tracker returns to "synthesis_audio", TRACKER E12; the panel goes; the terminal clears to
    8 rows: `exit` (laptop), `docker build -t synthesis_audio .` + ▶ your turn → 62-e-rebuild.txt
    lines 3, 14–17. "With all five done": the terminal goes; V1 (letters, drawer labels, the dashed
    bonus drawer) with A's and B's drawers already filled; GREY "your group's files:" + PINK
    `<prefix>/group-01/…`. "your group's drawers fill": C, D, E pulse, their letters step left and
    a wave, a French page and a wave appear in the space they leave, then drop into text_audios/,
    text_translated/, output_audios/ while a compact GOLD "billed" takes their place in each box. "and your leaderboard row": the schematic
    leaderboard (illustration) lights group-01's last three cells (the first two already lit),
    held, then everything fades: empty frame.
"""

import textwrap

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (box, check_mark, chip, cloud, code_panel, code_span, cross_mark, folder_glyph,
                              glyph_range, label, line_bar, mono, mono_line, step_badge, substring, tag)
from explainer.scene import VoiceScene

# after `from manim import *`: manim exports a `capture` too
from common import (CLOUD, COST, CTR, ERR, GROUP, INK, KEY, LAPTOP, LOOKUP, NARRATION, P_CTR, TURN, VENV,
                    ApiCall, LayerStack, Leaderboard, Relay, asset_lines, bare_prompt, beside, caption_extra,
                    capture, cost_tag, editor_inset, erratum_tag, excerpt, expected_tag, extra_tag,
                    file_panel, file_row, illustration_tag, key_glyph, live_split, log_panel, optional_tag,
                    p_comp, page_token, pin, readme_card, readme_chip, resize, sans, signpost, source_text,
                    src_panel, strike, strip_top, switch_section, term, tracker, type_cmd, wave_token,
                    your_turn)

SAY = NARRATION["S13"]

# ------------------------------------------------------------------ the three components
C, D, E = "synthesis_audio_en", "translate_text", "synthesis_audio"
P_B, P_C, P_D, P_E = p_comp("generate_text"), p_comp(C), p_comp(D), p_comp(E)
CD = {C: "cd ../synthesis_audio_en", D: "cd ../translate_text", E: "cd ../synthesis_audio"}
CLI_C, CLI_D, CLI_E = f"{C}/cli.py", f"{D}/cli.py", f"{E}/cli.py"
CLI_11 = f"{E}/cli_11.py"

_RC = source_text(f"{C}/README.md").split("\n")
_RD = source_text(f"{D}/README.md").split("\n")
_RE = source_text(f"{E}/README.md").split("\n")
for _r, _c in ((_RC, C), (_RD, D), (_RE, E)):
    assert f"`cd` into the `{_c}` folder" in _r[12], _r[12]          # README line 13: cd
    assert _r[21] == "uv init --bare"                                  # line 22
    assert f"give your image the name `{_c}`" in _r[94]               # line 95: build
assert "keep `ffmpeg` in the system packages" in _RC[37] and "keep `ffmpeg`" in _RE[37]
assert _RC[44] == _RE[44] == _RD[44] == 'ARG DEBIAN_PACKAGES="build-essential"'
assert "cli_11.py" in _RC[131] and "Do the same in `cli_11.py`" in _RE[111]
assert _RE[138:141] == ["2. Create a file `secrets/11lab_api_key.txt` with the following content:", "```",
                        "XI_API_KEY=your_api_key_here"], _RE[138:141]
assert _RE[145] == "uv add requests"
BONUS_CMDS = _RE[150:153]                                              # lines 151-153
assert BONUS_CMDS == ["python cli_11.py --download", "python cli_11.py --synthesis",
                      "python cli_11.py --upload"], BONUS_CMDS
RUN = {C: _RC[98], D: _RD[98], E: _RE[98]}                             # line 99
for _c, _cmd in RUN.items():
    assert _cmd == f'docker run --rm -ti -v "$(pwd):/app" {_c}', _cmd

_R = source_text("README.md").split("\n")
CMDS = {C: _R[147:149], D: _R[154:157], E: _R[161:163]}               # Quick Reference
assert CMDS[C] == CMDS[E] == ["python cli.py --download", "python cli.py --synthesis"], CMDS
assert CMDS[D] == ["python cli.py --download", "python cli.py --translate", "python cli.py --upload"]
assert "no separate `--upload` step needed" in _R[150]

# ------------------------------------------------------------------ captures (never typed by hand)
UVI = {C: capture("40-c-uv-init"), D: capture("50-d-uv-init"), E: capture("60-e-uv-init")}
for _c, _cap in UVI.items():
    assert _cap.cmd == "uv init --bare; cat pyproject.toml", _cap.cmd   # typed as two commands
    assert _cap.line(2) == f"Initialized project `{_c.replace('_', '-')}`", _cap.line(2)
UVI_CMD, CAT_CMD = "uv init --bare", "cat pyproject.toml"
CAT_OUT = UVI[C].at((3, 7))
assert CAT_OUT[3] == 'requires-python = ">=3.11"', CAT_OUT

BUILD = {c: f"docker build -t {c} ." for c in (C, D, E)}    # README :95 names the image; no --network host
BLD = {C: capture("41-c-build"), D: capture("51-d-build"), E: capture("61-e-build")}
RBLD = {C: capture("42-c-rebuild"), D: capture("52-d-rebuild"), E: capture("62-e-rebuild")}
for _c in (C, D, E):
    assert BLD[_c].cmd == RBLD[_c].cmd == f"docker build --network host -t {_c} .", BLD[_c].cmd

UVA = {c: capture("01-uv-add", c) for c in (C, D, E)}
assert UVA[C].cmd == UVA[E].cmd == "uv add google-cloud-storage google-cloud-texttospeech"
assert UVA[D].cmd == "uv add google-cloud-storage google-cloud-translate"
assert UVA[C].line(8).startswith("Installed 24 packages") and UVA[D].line(8).startswith("Installed 25")

HELP = {c: capture("03-help", c) for c in (C, D, E)}
HELP_C_OUT = HELP[C].at((2, 4), "…", 25)
HELP_D_OUT = HELP[D].at((2, 4), "…", 22)
HELP_E_OUT = HELP[E].at(25)
NOKEY = "google.auth.exceptions.DefaultCredentialsError: File secrets/mega-pipeline.json was not found."
assert HELP_C_OUT[-1] == HELP_D_OUT[-1] == HELP_E_OUT[-1] == NOKEY
assert HELP_C_OUT[1] == '  File "/app/cli.py", line 22, in <module>', HELP_C_OUT[1]
assert HELP_D_OUT[1] == '  File "/app/cli.py", line 20, in <module>', HELP_D_OUT[1]

EXP = {c: capture(f"{c}-help", "expected") for c in (C, D, E)}
EXP_OUT = {C: EXP[C].at((3, 10)), D: EXP[D].at((3, 11)), E: EXP[E].at((3, 10))}
EXP_HEAD = {C: f"{C}/README.md · lines 116–123", D: f"{D}/README.md · lines 116–124",
            E: f"{E}/README.md · lines 116–123"}
for _c in (C, D, E):
    assert EXP[_c].cmd == "python cli.py --help"
    _a, _b = (116, 124) if _c == D else (116, 123)
    assert source_text(f"{_c}/README.md").split("\n")[_a - 1:_b] == EXP_OUT[_c], _c
assert EXP_OUT[E][2] == "Synthesis audio from text"

REQ = capture("04-bonus-uv-add-requests", E)
assert REQ.cmd == "uv add requests" and REQ.line(3).startswith("Checked 24 packages")
C11 = capture("05-bonus-cli11-download", E)
assert C11.cmd == BONUS_CMDS[0]
C11_OUT = C11.at((2, 3), 6)
assert C11_OUT[2] == "FileNotFoundError: [Errno 2] No such file or directory: 'secrets/11lab_api_key.txt'"

DF_LINE = 'ARG DEBIAN_PACKAGES="build-essential"'
for _c in (C, D, E):
    assert asset_lines(f"files/{_c}.Dockerfile", 3, 3) == DF_LINE
    assert asset_lines(f"files/{_c}.Dockerfile", 1, 27) == asset_lines("files/generate_text.Dockerfile", 1, 27)

# source lines the panels quote
assert excerpt(CLI_C, 18, 18, cut_comments=True) == 'group_name = "pavlos"  # …'
assert excerpt(CLI_D, 18, 18, cut_comments=True) == 'group_name = "pavlos"  # …'
assert excerpt(CLI_E, 18, 18, cut_comments=True) == 'group_name = "pavlos"  # …'
assert excerpt(CLI_11, 19, 19, cut_comments=True) == 'group_name = "pavlos"  # …'
assert excerpt(CLI_C, 22, 22) == "client = texttospeech.TextToSpeechLongAudioSynthesizeClient()"
assert excerpt(CLI_C, 118, 118).strip() == "args = parser.parse_args()"
M78 = textwrap.dedent(excerpt(CLI_C, 78, 78))
assert M78 == 'output_gcs_uri = f"gs://{bucket_name}/{audio_blob_name}"', M78
M88 = textwrap.dedent(excerpt(CLI_C, 88, 91, cut_comments=True))
assert M88.split("\n") == ["operation = client.synthesize_long_audio(request=request)", "# …",
                           "result = operation.result(timeout=300)",
                           'print("Audio file will be saved to GCS bucket automatically.")'], M88
M58 = textwrap.dedent(excerpt(CLI_D, 58, 65))
assert M58.split("\n")[2] == '    source_language="en",' and M58.split("\n")[7] == "print(translated_text)"
assert excerpt(CLI_D, 68, 68).strip() == 'with open(translated_file, "w") as f:'
L105 = excerpt(CLI_E, 105, 105)
ARGP = 'ArgumentParser(description="Transcribe audio file to text")'
assert ARGP in L105, L105
assert excerpt(CLI_11, 30, 30) == "secrets_file_path = 'secrets/11lab_api_key.txt'"
assert excerpt(CLI_11, 33, 33) == "with open(secrets_file_path) as f:"

# ------------------------------------------------------------------ layout
TOP = 2.8                         # top of a picture under the tracker band (y 2.92..3.5)
EDGE = 6.45
BAND_Y = 3.2                      # the top band, right of the tracker
STRIP = strip_top(3)              # -1.44
BOTTOM_Y = -3.5                   # the terminal's bottom edge (common.BOTTOM)
H_V2 = {"base": 0.42, "apt": 0.55, "workdir": 0.07, "copy": 0.26, "sync": 0.38}
STB_X, STC_X, ST_FLOOR = -4.3, 0.85, 0.45


# ------------------------------------------------------------------ small helpers (as in S12)
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


PACE = [1.0]                      # run-time factor for room()'s scrolls (the E montage runs quicker)


def room(scene, t, n: int):
    """Make room for n new rows: the oldest rows fade where they are, then the rest move up."""
    over = len(t.lines) + n - t.rows
    if len(t.lines) and getattr(t.lines[-1], "bare", False):
        over -= 1                                   # type_cmd replaces the bare prompt
    if over <= 0:
        return
    gone = t.lines.submobjects[:over]
    stay = VGroup(*t.lines.submobjects[over:])
    scene.play(FadeOut(VGroup(*gone)), run_time=0.15 * PACE[0])
    for m in gone:
        t.lines.remove(m)
        scene.remove(m)
    if len(stay):
        scene.play(stay.animate.shift(UP * t.pitch * over), run_time=0.2 * PACE[0])


def reset(scene, t, rows: int, extra=(), run_time: float = 0.5):
    """Clear the terminal and resize it to `rows` in one move (`extra` animations play along)."""
    old = list(t.lines)
    scene.add(*old)
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


def tprint(scene, t, lines, wrap: bool = False, run_time: float = 0.4, color=None, lag: float = 0.12):
    n = 0
    for x in lines:
        s = x if isinstance(x, str) else x[0]
        n += max(1, -(-len(s) // t.max_chars)) if wrap else 1
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
    """A translucent bar behind whole terminal / log rows."""
    lines = lines if isinstance(lines, (list, tuple)) else [lines]
    left = min(ln.glyphs.get_left()[0] for ln in lines) - pad
    rx = right if right is not None else max(ln.glyphs.get_right()[0] for ln in lines) + pad
    top = lines[0].strut.get_top()[1] + 0.03
    bot = lines[-1].strut.get_bottom()[1] - 0.03
    return Rectangle(width=rx - left, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([(left + rx) / 2, (top + bot) / 2, 0])


def ttag(text: str, color=S.GREY) -> VGroup:
    """A compact tag that fits inside one 22 pt terminal row (20 pt text, 0.34 tall)."""
    t = label(text, 20, color)
    fr = RoundedRectangle(width=t.width + 0.3, height=0.34, corner_radius=0.17, stroke_color=color,
                          stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.box, g.text = fr, t
    return g


def pulse(frame, body, color=INK, scale: float = 1.12) -> AnimationGroup:
    """Pulse a filled tag or crate without flooding it: the frame's stroke flashes `color` and
    the body grows and flashes (Indicate on the whole group would fill the frame and hide the text)."""
    return AnimationGroup(frame.animate(rate_func=there_and_back).set_stroke(color, 3.5),
                          Indicate(body, color=color, scale_factor=scale))


def at_right(m, t, line):
    """Put m at the right end of terminal row `line`, inside the frame."""
    return m.move_to(line.strut).align_to(t.box, RIGHT).shift(LEFT * 0.12)


def live_rows(cap, cut14: int = 52):
    """Line 3 and the live-view rows 14-17 of a build capture: (texts, times). Line 3 (79 chars)
    is cut at 65 with its run of spaces dropped; row 14 at `cut14` (room for its badge)."""
    l3 = cap.line(3)
    texts, times = [l3[:64].rstrip() + " …" if len(l3) > 65 else l3], [None]
    for n in (14, 15, 16, 17):
        txt, tm = live_split(cap.line(n), width=cut14 if n == 14 else 65)
        texts.append(txt)
        times.append(tm)
    return texts, times


def gray_line(*parts) -> VGroup:
    """A GREY 20 pt caption mixing serif words and mono names: gray_line("=", ("generate_text",),
    "'s Dockerfile") — a tuple is mono."""
    ms = [mono(p[0], 20, S.GREY) if isinstance(p, tuple) else label(p, 20, S.GREY) for p in parts]
    g = VGroup(*ms).arrange(RIGHT, buff=0.12)
    for m in ms[1:]:
        m.align_to(ms[0], DOWN)
    return g


def code_card(where: str, code: str) -> VGroup:
    """A README card whose content is one line of code (mono), header `where` above."""
    row = mono_line(code, 20, INK)
    fr = box(row.width + 0.5, row.strut.height + 0.36, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    row.move_to(fr)
    path, _, rest = where.partition(" · ")
    head = VGroup(mono(path, 20, S.GREY), label(f"· {rest}", 20, S.GREY)).arrange(RIGHT, buff=0.12)
    head.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, row, head)
    g.frame, g.rows, g.header = fr, VGroup(row), head
    return g


def dedent_panel(name: str, a: int, b: int, cut: bool = False, size: float = 20) -> VGroup:
    """src_panel's look for a dedented excerpt (header "path · lines a–b" + " · comment cut")."""
    raw = excerpt(name, a, b)
    src = textwrap.dedent(excerpt(name, a, b, cut_comments=cut))
    p = code_panel(src, name, a, "python", font_size=size)
    if cut and excerpt(name, a, b, cut_comments=True) != raw:
        where = f"line {a}" if a == b else f"lines {a}–{b}"
        head = VGroup(mono(name, 20, S.GREY), label(f"· {where} · comment cut", 20, S.GREY))
        head.arrange(RIGHT, buff=0.14).move_to(p.header, aligned_edge=LEFT)
        p.remove(p.header)
        p.header = head
        p.add(head)
    return p


def help_panel(c: str) -> VGroup:
    """The README's --help block for component c (expected/*.txt), 20 pt, full width."""
    p = log_panel(EXP_OUT[c], EXP_HEAD[c], width=12.6, size=20)
    place(p, cx=0, top=TOP)
    tg = VGroup(expected_tag(), label("with your key", 20, S.GREY)).arrange(RIGHT, buff=0.2)
    place(tg, right=p.frame.get_right()[0] - 0.05, cy=p.header.get_center()[1])
    p.add(tg)
    p.tags = tg
    return p


def secrets_row(cy: float = 2.5):
    """The GREY secrets/ folder (top right) and the GOLD key that drops into it.
    Returns (row without the key name, key, key name, target point)."""
    fold = folder_glyph(0.42, LAPTOP)
    sname = mono("secrets/", 20, INK).next_to(fold, RIGHT, buff=0.14)
    kname = mono("mega-pipeline.json", 20, KEY).next_to(sname, RIGHT, buff=0.3)
    ill = illustration_tag().next_to(kname, RIGHT, buff=0.35)
    g = VGroup(fold, sname, kname, ill)
    place(g, right=EDGE, cy=cy)
    kname.align_to(sname, DOWN)
    # the key starts above its own name (right of the tracker's caption, which it would cross if it
    # fell straight down onto the folder) and drops into the folder
    key = key_glyph(0.3).move_to([kname.get_center()[0], cy + 0.62, 0])
    assert key.get_left()[0] > 0.4 and key.get_top()[1] + 0.2 < 3.6, (key.get_left(), key.get_top())
    return VGroup(fold, sname, ill), key, kname, fold[1].get_center() + DOWN * 0.02, fold


def drop_key(scene, cy: float = 2.5, extra=(), k: float = 1.0):
    """The GOLD key drops into secrets/ (README step 2); k scales the run times. Returns what to
    fade later."""
    row, key, kname, target, fold = secrets_row(cy)
    scene.play(FadeIn(row), FadeIn(key, shift=DOWN * 0.2), *extra, run_time=0.35 * k)
    scene.play(key.animate.scale(0.62).move_to(target), run_time=0.4 * k)
    scene.play(FadeIn(kname, shift=LEFT * 0.15), Indicate(fold, color=KEY, scale_factor=1.15), run_time=0.35 * k)
    return VGroup(row, key, kname)


def steps_card(comp: str, items) -> VGroup:
    """The static GREY card a montage settles into: `comp · steps 1–9` above, one row per README
    step (YELLOW number, then a mono command or a serif note)."""
    rows = VGroup()
    for k, (txt, is_cmd) in enumerate(items, start=1):
        n = sans(str(k), 20, TURN)
        body = mono_line(txt, 20, INK) if is_cmd else label(txt, 20, INK)
        r = VGroup(n, body)
        rows.add(r)
    pitch = 0.36
    for i, r in enumerate(rows):
        n, body = r
        y = -i * pitch
        n.move_to([0.0, y, 0], aligned_edge=RIGHT)
        if isinstance(body, VGroup) and hasattr(body, "strut"):
            body.shift(np.array([0.2 - body.glyphs.get_left()[0], y - body.strut.get_center()[1], 0]))
        else:
            body.move_to([0.2, y, 0], aligned_edge=LEFT)
    fr = box(rows.width + 0.6, rows.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.12)
    fr.move_to(rows)
    head = VGroup(mono(comp, 20, S.GREY), label("· steps 1–9", 20, S.GREY)).arrange(RIGHT, buff=0.12)
    head.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head
    return g


def montage_items(c: str):
    return [(CD[c], True), ("copy the key into secrets/", False), (UVI_CMD, True),
            ("Dockerfile = C's" if c == D else "Dockerfile = C's (and B's)", False), (BUILD[c], True),
            (RUN[c], True), (UVA[c].cmd, True), ("group name, line 18", False), ("python cli.py --help", True)]


def inset18(cli: str) -> tuple:
    """The editor inset with `group_name = ...` (line 18, comment cut), top right."""
    p = src_panel(cli, 18, 18, cut_comments=True, size=20)
    ins = editor_inset(p)
    place(ins, right=EDGE, top=TOP + 0.02)
    gn = code_span(p.code, 0, "group_name")
    u = Line(gn.get_corner(DL) + DOWN * 0.05, gn.get_corner(DR) + DOWN * 0.05, color=TURN, stroke_width=4)
    return ins, gn, u


def live_build(scene, t, cap, rows_: tuple = (14, 15, 16, 17), run_time: float = 0.35):
    """Print line 3 and live-view rows of a build capture with their time tags. Returns
    (printed rows, tags). Rows are in `rows_` order after line 3."""
    texts, times = live_rows(cap)
    idx = [0] + [(14, 15, 16, 17).index(n) + 1 for n in rows_]
    out = tprint(scene, t, [texts[i] for i in idx], run_time=run_time, lag=0.08)
    tags = []
    for k, i in enumerate(idx[1:], start=1):
        g = at_right(ttag(times[i]), t, out[k])
        tags.append(g)
    scene.play(*[FadeIn(g) for g in tags], run_time=0.2)
    for k, g in enumerate(tags, start=1):
        stick(scene, out[k], g)
    return out, tags


def cached_green(scene, row, run_time: float = 0.35):
    scene.play(substring(row, "CACHED").animate.set_color(VENV), run_time=run_time)


def _retitle(scene, t, text: str, color, stroke: tuple, prompt: str, run_time: float, extra=()):
    """enter_container / leave_container with a cross-fade of the title instead of a Transform
    (a Transform between titles of different widths squeezes the 20 pt text below 20 pt)."""
    t.set_prompt(prompt)
    old = t.title
    new = mono(text, 20, color).move_to(old).set_opacity(0)
    t.add(new)
    t.title = new
    scene.play(t.box.animate.set_stroke(*stroke), old.animate.set_opacity(0), new.animate.set_opacity(1),
               *extra, run_time=run_time)
    t.remove(old)
    scene.remove(old)


def enter(scene, t, comp: str, run_time: float = 0.3, extra=()):
    _retitle(scene, t, f"container · {comp}", CTR, (CTR, 3), P_CTR, run_time, extra)


def leave(scene, t, prompt: str, run_time: float = 0.3, extra=()):
    _retitle(scene, t, "laptop", S.GREY, (S.GREY_DARK, 2), prompt, run_time, extra)


def _out_early(a: float) -> float:
    """rate_func: an outgoing picture is gone by 60 % of the run."""
    return smooth(min(1.0, a / 0.6))


def _in_late(a: float) -> float:
    """rate_func: the incoming terminal and chip start at 40 % of the run (they barely overlap the
    outgoing picture, whose code panel sits where the chip lands)."""
    return smooth(max(0.0, (a - 0.4) / 0.6))


def _typed(a: float) -> float:
    """rate_func: the first command is typed from 45 % to 80 % of the run, as the terminal shows."""
    return min(1.0, max(0.0, (a - 0.45) / 0.35))


def _tag_in(a: float) -> float:
    """rate_func: ▶ your turn comes in over the last 20 % of the run, once its command is typed."""
    return smooth(max(0.0, (a - 0.8) / 0.2))


def back_to_terminal(scene, old, t, chip, note, tr_anim, cmd: str, run_time: float = 0.9):
    """One move from a V8 picture to the pause terminal, so ▶ is up while "pause" is still being
    heard: the picture goes; the terminal, the README chip and its 'same as' note come in; `cmd` is
    typed at the prompt as soon as the terminal shows, and ▶ your turn lands beside it, pinned to its
    row so it stays until the terminal clears; the tracker steps on. `t` starts empty (its prompt
    comes with the command). Returns (the typed line, as Terminal.type returns it; the tag)."""
    assert not len(t.lines), "the pause terminal starts empty"
    p = t.prompt + " "
    assert len(t.fold(p + cmd, first_prefix=len(p))) == 1, cmd
    ln = t._place(mono_line(p + cmd, t.size, INK, t2c=t._prompt_colors(t.prompt)), 0)
    yt = beside(your_turn(), t, ln)
    assert yt.get_left()[0] > ln.glyphs.get_right()[0] + 0.1, (yt.get_left(), ln.glyphs.get_right())
    scene.play(FadeOut(old, rate_func=_out_early), FadeIn(t, rate_func=_in_late),
               FadeIn(glyph_range(ln, 0, len(p)), rate_func=_in_late),
               ShowIncreasingSubsets(glyph_range(ln, len(p)), rate_func=_typed),
               FadeIn(yt, shift=LEFT * 0.1, rate_func=_tag_in),
               FadeIn(chip, shift=DOWN * 0.1, rate_func=_in_late), FadeIn(note, shift=DOWN * 0.1, rate_func=_in_late),
               tr_anim, run_time=run_time)
    scene.remove(yt)
    ln.add(yt)                                        # pinned, as pin() does
    t.lines.add(ln)
    scene.add(ln)
    return ln, yt


# ------------------------------------------------------------------ the scene
class SpeedRound(VoiceScene):
    def construct(self):
        assert len(SAY) == 17, f"S13 has {len(SAY)} SAY lines; this scene times 17"

        # ========================================================== 0 · C: cd, key, uv init (C1-C3)
        tr = tracker("B", 13)
        t = term(P_B, 12)
        seed_prompt(t)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.5)
            tr = switch_section(self, tr, "C", None, run_time=0.7)
            self.play(Indicate(tr.head[2], color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("For C, synthesis audio")
            self.play(tr.goto(1), run_time=0.3)
            tcmd(self, t, CD[C], 0.6)
            t.set_prompt(P_C)
            ln0 = bare_prompt(self, t)
            self.play(Indicate(substring(ln0, C), color=TURN, scale_factor=1.1), run_time=0.5)
            vo.wait_until("copy the key")
            keyg = drop_key(self, cy=2.56, extra=[tr.goto(2)], k=0.8)
            self.play(FadeOut(keyg), tr.goto(3), run_time=0.3)
            tcmd(self, t, UVI_CMD, 0.4)
            tprint(self, t, [UVI[C].line(2)], run_time=0.2)
            self.play(caption_extra(tr, True), run_time=0.25)
            c0 = tcmd(self, t, CAT_CMD, 0.35)
            pin(self, c0, beside(extra_tag(), t, c0), run_time=0.25)
            o0 = tprint(self, t, CAT_OUT, run_time=0.4, lag=0.08)
            r6 = o0[3]
            vo.wait_until("If it stamps 3.13")
            b6 = rbar(r6, VENV, 0.2)
            self.play(FadeIn(b6), substring(r6, '">=3.11"').animate.set_color(VENV), run_time=0.45)
            stick(self, r6, b6)
            t313 = beside(ttag("3.13 or newer? → 3.12"), t, r6, buff=0.4)
            pin(self, r6, t313, run_time=0.4)
            vo.wait_until("here and in D and E")
            self.play(pulse(t313.box, t313.text), run_time=0.7)

        # ========================================================== 1 · C4: the Dockerfile; the ffmpeg slip
        df = file_panel(f"files/{C}.Dockerfile", 3, 3, f"{C}/Dockerfile")
        place(df, left=-6.4, top=TOP)
        same = VGroup(label("=", 20, S.GREY), mono("generate_text", 20, S.GREY), label("'s Dockerfile", 20, S.GREY))
        same.arrange(RIGHT, buff=0.12)
        same[2].next_to(same[1], RIGHT, buff=0.04)         # "generate_text's": no gap before the 's
        same[2].align_to(same[1], UP).shift(DOWN * 0.02)    # the apostrophe sits at the mono cap height
        place(same, left=df.get_right()[0] + 0.4, cy=df.code.get_center()[1])
        card38 = readme_card(f"{C}/README.md · line 38", ["so keep ffmpeg in the system packages"])
        place(card38, left=-6.4, top=df.get_bottom()[1] - 0.25)
        err1 = erratum_tag()
        place(err1, left=card38.header.get_right()[0] + 0.3, cy=card38.header.get_center()[1])
        same_e = VGroup(label("same in", 22, S.GREY), mono(f"{E}/README.md", 22, S.GREY)).arrange(RIGHT, buff=0.12)
        sefr = RoundedRectangle(width=same_e.width + 0.4, height=0.47, corner_radius=0.23, stroke_color=S.GREY,
                                stroke_width=2).set_fill(S.BG, 0.92).move_to(same_e)
        same_e = VGroup(sefr, same_e)
        place(same_e, left=card38.frame.get_right()[0] + 0.35, cy=card38.frame.get_center()[1])
        card45 = code_card(f"{C}/README.md · line 45", DF_LINE)
        place(card45, left=-6.4, top=card38.frame.get_bottom()[1] - 0.22)
        ok = VGroup(check_mark(0.3, VENV), label("right", 22, VENV)).arrange(RIGHT, buff=0.12)
        place(ok, left=card45.frame.get_right()[0] + 0.3, cy=card45.frame.get_center()[1])
        note1 = VGroup(gray_line("neither synthesis", ("cli.py",)), gray_line("uses ffmpeg"))
        note1.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        place(note1, left=ok.get_right()[0] + 0.45, cy=ok.get_center()[1])
        s38 = strike(card38.rows[0])
        assert card45.frame.get_bottom()[1] > STRIP + 0.1, card45.frame.get_bottom()
        assert note1.get_right()[0] < EDGE and same_e.get_right()[0] < EDGE, (note1.get_right(), same_e.get_right())

        with self.voiceover(SAY[1]) as vo:
            self.play(tr.goto(4), caption_extra(tr, False), run_time=0.4)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(df, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(same, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("A small slip")
            self.play(FadeIn(card38, shift=DOWN * 0.1), FadeIn(err1, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("here and in E")
            self.play(FadeIn(same_e, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("the README's text says")
            self.play(Indicate(card38.rows[0], color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("but its code block")
            self.play(FadeIn(card45, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("which is right")
            self.play(Create(ok[0]), FadeIn(ok[1]), Create(s38), card38.rows[0].animate.set_opacity(0.5),
                      run_time=0.5)
            vo.wait_until("leaves it out")
            self.play(FadeIn(note1, shift=LEFT * 0.1), run_time=0.45)

        # ========================================================== 2 · C5: build; B's big layer is shared
        stB = LayerStack(slab_w=3.5)
        for name in ("base", "apt", "workdir", "copy", "sync"):
            s = stB.make(name, h=H_V2[name])
            stB.slabs[name] = s
            stB.order.append(name)
            stB.add(s)
        stB.move_to([STB_X, ST_FLOOR, 0], aligned_edge=DOWN)
        nameB = mono("generate_text", 20, CTR).next_to(stB, UP, buff=0.14)
        stC = LayerStack(slab_w=3.5)
        stC.move_to([STC_X, ST_FLOOR + stC.floor.get_center()[1] - stC.get_bottom()[1], 0])
        stC.floor.move_to([STC_X, stB.floor.get_center()[1], 0])
        ghosts = VGroup()
        for name in ("base", "apt"):
            s = stC.make(name, text="", h=H_V2[name], dashed=True)
            stC.slabs[name] = s
            stC.order.append(name)
            stC.add(s)
            ghosts.add(s)
        own = VGroup()
        for name in ("workdir", "copy", "sync"):
            s = stC.make(name, h=H_V2[name])
            stC.slabs[name] = s
            stC.order.append(name)
            stC.add(s)
            own.add(s)
        nameC = mono(C, 20, CTR)
        place(nameC, cx=STC_X, cy=nameB.get_center()[1])
        a_apt, b_apt = stC.slabs["apt"].box, stB.slabs["apt"].box
        shared = Arrow(a_apt.get_left() + LEFT * 0.08, b_apt.get_right() + RIGHT * 0.08, buff=0, color=VENV,
                       stroke_width=5, max_tip_length_to_length_ratio=0.18, max_stroke_width_to_length_ratio=10)
        shared_l = sans("shared", 20, VENV).next_to(shared, UP, buff=0.12)
        why = VGroup(sans("not CACHED? a line differs", 20, S.GREY), sans("from B's: fine, only slower", 20, S.GREY))
        why.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        place(why, right=EDGE, cy=1.35)
        assert why.get_left()[0] > stC.floor.get_right()[0] + 0.1, (why.get_left(), stC.floor.get_right())
        assert nameB.get_top()[1] < 2.9

        with self.voiceover(SAY[2]) as vo:
            reset(self, t, 7, run_time=0.5,
                  extra=[FadeOut(VGroup(df, same, card38, err1, same_e, card45, ok, note1, s38)), tr.goto(5),
                         FadeIn(VGroup(stB, nameB), shift=UP * 0.15)])
            tcmd(self, t, BUILD[C], 0.45)
            o2, _ = live_build(self, t, BLD[C], run_time=0.3)
            vo.wait_until("build step 2 is cached")
            r14 = o2[1]
            k2 = substring(r14, "[2/5]")
            box2 = SurroundingRectangle(k2, color=CTR, buff=0.05, stroke_width=2.5, corner_radius=0.05)
            bd2 = step_badge(2, CTR, size=20, radius=0.17)
            place(bd2, left=r14.glyphs.get_right()[0] + 0.25, cy=r14.strut.get_center()[1])
            self.play(substring(r14, "CACHED").animate.set_color(VENV), Create(box2), k2.animate.set_color(CTR),
                      FadeIn(bd2, scale=1.3), run_time=0.5)
            stick(self, r14, box2, bd2)
            vo.wait_until("and the build takes")
            r3 = o2[0]
            u3 = uline(r3, "Building 0.6s", VENV)
            self.play(substring(r3, "Building 0.6s").animate.set_color(VENV), Create(u3), run_time=0.5)
            stick(self, r3, u3)
            vo.wait_until("C's Dockerfile matches")
            self.play(FadeIn(stC.floor), FadeIn(nameC, shift=DOWN * 0.1), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(g, shift=DOWN * 0.3) for g in ghosts], lag_ratio=0.4), run_time=0.6)
            self.play(FadeIn(why, shift=LEFT * 0.1), run_time=0.45)
            vo.wait_until("so Docker reuses")
            self.play(GrowArrow(shared), FadeIn(shared_l), run_time=0.5)
            self.play(Indicate(b_apt, color=VENV, scale_factor=1.05), Indicate(a_apt, color=VENV, scale_factor=1.05),
                      run_time=0.6)
            self.play(LaggedStart(*[FadeIn(s, shift=DOWN * 0.3) for s in own], lag_ratio=0.35), run_time=0.7)

        # ========================================================== 3 · C6-C7: run; uv add
        v2_all = VGroup(stB, nameB, stC.floor, ghosts, own, nameC, shared, shared_l, why)
        with self.voiceover(SAY[3]) as vo:
            reset(self, t, 10, run_time=0.5, extra=[FadeOut(v2_all), tr.goto(6)])
            tcmd(self, t, RUN[C], 0.6)
            enter(self, t, C)
            self.play(tr.goto(7), run_time=0.25)
            tcmd(self, t, UVA[C].cmd, 0.6)
            o3 = tprint(self, t, UVA[C].at(2, 8), run_time=0.3)
            vo.wait_until("24 packages")
            u24 = uline(o3[1], "Installed 24 packages", VENV)
            self.play(substring(o3[1], "Installed 24 packages").animate.set_color(VENV), Create(u24), run_time=0.5)
            stick(self, o3[1], u24)

        # ========================================================== 4 · C8-C9: group name; --help needs the key
        ins, gn, u_gn = inset18(CLI_C)
        assert ins.get_bottom()[1] > strip_top(8) + 0.08, ins.get_bottom()
        # V5 callback (small): cli.py runs top to bottom; line 22 asks google.auth at once
        flow_l = label("cli.py runs top to bottom", 20, S.GREY)
        place(flow_l, left=-6.4, cy=2.62)
        flow = Arrow([-6.25, 2.42, 0], [-6.25, -1.05, 0], buff=0, color=S.GREY, stroke_width=3,
                     max_tip_length_to_length_ratio=0.06)
        p22 = src_panel(CLI_C, 22, 22, size=20)
        place(p22, left=-5.9, top=2.42)
        y22 = p22.code.get_center()[1]
        bar22 = line_bar(p22.code, 0, TURN)               # line 22 lights (the panel itself stays dark)
        runner = Dot([-6.25, 2.38, 0], radius=0.09, color=TURN)
        gauth_t = mono("google.auth", 20, INK)
        gauth = VGroup(box(gauth_t.width + 0.3, 0.6, S.GREY, fill_opacity=0.12).move_to(gauth_t), gauth_t)
        place(gauth, left=-5.9, cy=0.45)
        a22 = Arrow([gauth.get_center()[0], p22.code.get_bottom()[1] - 0.02, 0], gauth.get_top() + UP * 0.02,
                    buff=0, color=S.GREY, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        post = signpost(["GOOGLE_APPLICATION_CREDENTIALS=", "secrets/mega-pipeline.json"], post_h=0.25)
        post.shift(np.array([gauth.get_right()[0] + 0.5 - post.board.get_left()[0],
                             gauth.get_center()[1] - post.board.get_center()[1], 0]))
        sec = file_row("secrets/")
        place(sec, left=post.board.get_right()[0] + 0.6, cy=gauth.get_center()[1])
        xk = cross_mark(0.32, ERR).next_to(sec, RIGHT, buff=0.25)
        pa1 = Arrow(gauth.get_right(), post.board.get_left() + LEFT * 0.02, buff=0.06, color=LOOKUP, stroke_width=3,
                    max_tip_length_to_length_ratio=0.3)
        pa2 = Arrow(post.board.get_right() + RIGHT * 0.3, sec.get_left(), buff=0.06, color=LOOKUP, stroke_width=3,
                    max_tip_length_to_length_ratio=0.35)
        pchip = chip("parse_args()", S.GREY, size=20, font="DejaVu Sans Mono")
        pnote = gray_line("line 118 · reads --help ·", "never reached")
        pg = VGroup(pchip, pnote).arrange(RIGHT, buff=0.3)
        place(pg, left=-5.9, cy=-0.8)
        v5 = VGroup(flow_l, flow, p22, bar22, runner, gauth, a22, post, sec, xk, pa1, pa2, pg)
        assert xk.get_right()[0] < EDGE and pg.get_bottom()[1] > STRIP + 0.1
        hp_c = help_panel(C)
        assert hp_c.get_bottom()[1] > STRIP + 0.08, hp_c.get_bottom()

        with self.voiceover(SAY[4]) as vo:
            resize(self, t, 8, run_time=0.5, extra=[tr.goto(8), FadeIn(ins, shift=DOWN * 0.15)])
            self.play(gn.animate.set_color(TURN), Create(u_gn), run_time=0.5)
            vo.wait_until("then check the help")
            reset(self, t, 10, run_time=0.45, extra=[tr.goto(9), FadeOut(VGroup(ins, u_gn), shift=UP * 0.1)])
            c4 = tcmd(self, t, "python cli.py --help", 0.45)
            o4 = tprint(self, t, HELP_C_OUT[:-1] + [(HELP_C_OUT[-1], ERR)], wrap=True, run_time=0.45, lag=0.08)
            e1, e2 = o4[-2], o4[-1]
            vo.wait_until("Without a key")
            ue = Line([e1.glyphs.get_left()[0], e1.strut.get_bottom()[1] + 0.01, 0],
                      [e1.glyphs.get_right()[0], e1.strut.get_bottom()[1] + 0.01, 0], color=ERR, stroke_width=3)
            self.play(Create(ue), run_time=0.35)
            stick(self, e1, ue)
            nk = at_right(ttag("recorded without the key"), t, e2)
            pin(self, e2, nk, run_time=0.3)
            vo.wait_until("line 22 builds")
            self.play(substring(o4[1], "line 22").animate.set_color(TURN),
                      Indicate(substring(o4[1], "line 22"), color=TURN, scale_factor=1.2), run_time=0.5)
            resize(self, t, 3, keep=[c4, e1, e2], run_time=0.5,
                   extra=[FadeIn(flow_l), GrowArrow(flow), FadeIn(p22, shift=DOWN * 0.1)])
            self.add(runner)
            self.play(runner.animate.move_to([-6.25, y22, 0]), run_time=0.5)
            self.play(FadeIn(bar22), Flash(runner, color=TURN), run_time=0.5)
            vo.wait_until("as soon as the script starts")
            self.play(GrowArrow(a22), FadeIn(gauth, shift=DOWN * 0.1), run_time=0.45)
            self.play(FadeIn(post, shift=DOWN * 0.1), GrowArrow(pa1), run_time=0.45)
            self.play(GrowArrow(pa2), FadeIn(sec), run_time=0.45)
            # the strip's RED line answers: a flash runs along its underline (a full-width row cannot grow)
            self.play(Create(xk), ShowPassingFlash(ue.copy().set_stroke(ERR, 8), time_width=0.6), run_time=0.6)
            vo.wait_until("before reading any flags")
            pg.set_opacity(0.75)
            self.play(FadeIn(pg, shift=UP * 0.1), run_time=0.45)
            vo.wait_until("Pause and catch up")
            self.play(FadeOut(v5), FadeIn(hp_c, shift=DOWN * 0.1), run_time=0.55)
            hb = SurroundingRectangle(VGroup(*hp_c.rows), color=TURN, buff=0.1, stroke_width=2.5, corner_radius=0.08)
            self.play(Create(hb), run_time=0.5)
            yt4 = beside(your_turn(), t, c4)
            pin(self, c4, yt4, run_time=0.35)
            self.play(Wiggle(yt4, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)
            self.wait(1.0)                                    # hold the pause point

        # ========================================================== 5 · V8: the request carries an address
        api = ApiCall("Text-to-Speech · long audio", "C · synthesis_audio_en", drawers=[f"text_audios/{GROUP}/"])
        api.drawers.shift(UP * 0.6)
        api.drawers[0].frame.stretch_to_fit_height(1.1, about_edge=UP)
        api.shift(DOWN * 1.6)
        cloud_c = api.api.shape.get_center()
        link_y = api.link.get_center()[1]
        drawer = api.drawers[0]
        p78 = dedent_panel(CLI_C, 78, 78)
        place(p78, left=-6.4, top=TOP)
        span78 = code_span(p78.code, 0, "gs://{bucket_name}/{audio_blob_name}")
        u78 = Line(span78.get_corner(DL) + DOWN * 0.05, span78.get_corner(DR) + DOWN * 0.05, color=LOOKUP,
                   stroke_width=3)
        page = page_token(long=True).move_to(api.inside())
        addr = mono(f"gs://…/text_audios/{GROUP}/…", 20, LOOKUP)
        place(addr, cx=api.link.get_center()[0], cy=link_y + 0.32)
        cost5 = cost_tag()
        place(cost5, cx=api.link.get_center()[0], cy=link_y + 0.85)
        route = DashedLine(api.api.shape.get_bottom() + UP * 0.05, drawer.frame.get_top() + DOWN * 0.02,
                           color=LOOKUP, stroke_width=4, dash_length=0.1)
        back_y = link_y - 0.42
        back = DashedLine([api.api.shape.get_left()[0] + 0.1, back_y, 0], [api.ctr.frame.get_right()[0] + 0.1, back_y, 0],
                          color=S.GREY, stroke_width=2.5, dash_length=0.1).add_tip(tip_length=0.18)
        back_x = cross_mark(0.34, ERR).move_to(back.get_center())
        assert api.get_top()[1] < p78.get_bottom()[1] - 0.1 and api.get_bottom()[1] > -3.6, (api.get_top(), api.get_bottom())

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(t), FadeOut(hp_c), FadeOut(hb), FadeIn(api), FadeIn(p78, shift=DOWN * 0.1),
                      run_time=0.7)
            self.play(FadeIn(page, scale=0.6), run_time=0.35)
            vo.wait_until("and an address in the bucket")
            self.play(span78.animate.set_color(LOOKUP), Create(u78), run_time=0.35)
            cp = span78.copy()
            self.add(cp)
            self.play(Transform(cp, addr), run_time=0.8)
            self.remove(cp)
            self.add(addr)
            vo.wait_until("line 78")
            self.play(Indicate(p78.header, color=INK, scale_factor=1.08), run_time=0.5)
            vo.wait_until("Google's long audio service")
            ride = max(0.0, api.api.shape.get_left()[0] - 0.15 - addr.get_right()[0])
            self.play(page.animate.move_to(cloud_c), addr.animate.shift(RIGHT * ride), run_time=0.9)
            self.play(FadeOut(page, scale=0.4), Indicate(api.api.shape, color=CLOUD, scale_factor=1.05),
                      FadeIn(cost5, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("writes the speech straight there")
            self.play(Create(route), run_time=0.5)
            self.play(addr.animate.move_to(drawer.text).set_opacity(0), drawer.text.animate.set_color(LOOKUP),
                      run_time=0.6)
            self.remove(addr)
            self.play(Indicate(drawer.frame, color=CLOUD, scale_factor=1.05), run_time=0.5)
            vo.wait_until("never through your container")
            self.play(Create(back), run_time=0.5)
            self.play(Create(back_x), run_time=0.35)

        # ========================================================== 6 · stub, 300 s, the crate goes straight in
        p88 = dedent_panel(CLI_C, 88, 91, cut=True)
        place(p88, left=-6.4, top=TOP)
        assert api.get_top()[1] < p88.get_bottom()[1] - 0.08, (api.get_top(), p88.get_bottom())
        r151 = readme_chip("README.md · line 151", "no separate --upload")
        place(r151, right=EDGE, cy=BAND_Y)
        crate_w = wave_token(0.3)
        crate_b = box(crate_w.width + 0.3, 0.46, S.GREY, fill=S.BG, fill_opacity=0.9, radius=0.08).move_to(crate_w)
        crate = VGroup(crate_b, crate_w).move_to(cloud_c)
        crate_to = drawer.frame.get_bottom() + UP * 0.32
        assert crate_to[1] + 0.23 < drawer.text.get_bottom()[1] - 0.1, (crate_to, drawer.text.get_bottom())

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(p78, u78, back, back_x)), FadeIn(p88, shift=DOWN * 0.1), run_time=0.5)
            bar = line_bar(p88.code, 0, TURN)
            self.play(FadeIn(bar), run_time=0.25)
            stub = api.stub(self, run_time=0.6)
            vo.wait_until("for up to 300 seconds")
            self.play(Transform(bar, line_bar(p88.code, 2, TURN)), run_time=0.3)
            arc = Arc(radius=0.24, start_angle=PI / 2, angle=-TAU, stroke_color=CTR, stroke_width=4)
            arc.next_to(stub, RIGHT, buff=0.18)
            base = Circle(radius=0.24, stroke_color=CTR, stroke_width=1.5, stroke_opacity=0.35).move_to(arc)
            rlab = label("up to 300 s", 20, CTR).next_to(VGroup(stub, arc), DOWN, buff=0.15)
            self.play(FadeIn(rlab), FadeIn(base), FadeIn(crate, scale=0.6), run_time=0.3)
            self.play(Create(arc, rate_func=linear), crate.animate(rate_func=smooth).move_to(crate_to), run_time=1.3)
            vo.wait_until("then prints that")
            self.play(Transform(bar, line_bar(p88.code, 3, TURN)), run_time=0.3)
            self.play(Indicate(code_span(p88.code, 3, '"Audio file will be saved to GCS bucket automatically."'),
                               color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("so C has no upload step")
            self.play(FadeIn(r151, shift=DOWN * 0.1), run_time=0.45)
            self.play(pulse(crate_b, crate_w, scale=1.15), Indicate(r151.phrase, color=INK, scale_factor=1.08),
                      run_time=0.7)

        # ========================================================== 7 · C10-C12: download, synthesis; exit; rebuild
        t2 = term(P_CTR, 10, component=C)
        rc7 = readme_chip("README.md · lines 148–149")
        place(rc7, left=-6.4, cy=2.45)
        sm7 = tag("same as -d · -s", S.GREY)
        place(sm7, left=rc7.get_right()[0] + 0.3, cy=rc7.get_center()[1])
        assert rc7.get_bottom()[1] > strip_top(10) + 0.1

        with self.voiceover(SAY[7]) as vo:
            # ▶ beside the first command to run (as in E10) lands just after "pause" is spoken, in the
            # same move that brings the terminal back; it stays until the section switch
            l7a, yt7 = back_to_terminal(self, VGroup(api, p88, bar, stub, arc, base, rlab, crate, cost5, route, r151),
                                        t2, rc7, sm7, tr.goto(10), CMDS[C][0])
            vo.wait_until("pause to run")
            self.play(Wiggle(yt7, scale_value=1.12, rotation_angle=0.02 * TAU), tr.goto(11), run_time=0.6)
            l7 = tcmd(self, t2, CMDS[C][1], 0.45)
            ct7 = beside(ttag("billed", COST), t2, l7)
            pin(self, l7, ct7, run_time=0.3)
            self.play(tr.goto(12), run_time=0.25)
            tcmd(self, t2, "exit", 0.25)
            leave(self, t2, P_C)
            c7 = tcmd(self, t2, BUILD[C], 0.5)
            yt7b = beside(your_turn(), t2, c7)
            pin(self, c7, yt7b, run_time=0.25)                # and on the rebuild as soon as it is typed (as in E12)
            o7, _ = live_build(self, t2, RBLD[C])
            cached_green(self, o7[1])
            self.wait(1.0)                                    # the CACHED rows, before the section switch

        # ========================================================== 8 · D1-D5: the montage, first half
        dfD = file_panel(f"files/{D}.Dockerfile", 3, 3, f"{D}/Dockerfile")
        place(dfD, right=EDGE, top=TOP)

        with self.voiceover(SAY[8]) as vo:
            reset(self, t2, 10, run_time=0.4, extra=[FadeOut(VGroup(rc7, sm7))])
            tr = switch_section(self, tr, "D", None, run_time=0.6)
            self.play(Indicate(tr.head[2], color=TURN, scale_factor=1.1), run_time=0.5)
            vo.wait_until("races through")
            # "the same setup": the five steps this montage covers ripple
            self.play(LaggedStart(*[Indicate(d, color=TURN, scale_factor=1.8) for d in tr.dots[:5]], lag_ratio=0.3),
                      run_time=1.0)
            vo.wait_until("cd, key")
            self.play(tr.goto(1), run_time=0.2)
            tcmd(self, t2, CD[D], 0.35)
            t2.set_prompt(P_D)
            bare_prompt(self, t2)
            keyg = drop_key(self, cy=2.45, extra=[tr.goto(2)], k=0.55)
            self.play(FadeOut(keyg), tr.goto(3), run_time=0.2)
            tcmd(self, t2, UVI_CMD, 0.3)
            tprint(self, t2, [UVI[D].line(2)], run_time=0.2)
            barD = line_bar(dfD.code, 0, TURN)
            self.play(tr.goto(4), FadeIn(dfD, shift=DOWN * 0.1), run_time=0.3)
            self.play(FadeIn(barD), run_time=0.25)
            self.wait(0.15)
            self.play(FadeOut(VGroup(dfD, barD), shift=UP * 0.1), tr.goto(5), run_time=0.25)
            tcmd(self, t2, BUILD[D], 0.35)
            o8, _ = live_build(self, t2, BLD[D], rows_=(14,), run_time=0.25)
            cached_green(self, o8[1], run_time=0.3)

        # ========================================================== 9 · D6-D9: run, uv add, group name, --help
        ins_d, gn_d, u_gn_d = inset18(CLI_D)
        hp_d = help_panel(D)
        assert hp_d.get_bottom()[1] > STRIP + 0.08, hp_d.get_bottom()
        card_d = steps_card(D, montage_items(D))
        place(card_d, left=-6.4, top=TOP)
        assert card_d.get_bottom()[1] > STRIP + 0.08, card_d.get_bottom()
        yt9 = your_turn()
        place(yt9, left=card_d.frame.get_right()[0] + 0.35, bottom=card_d.frame.get_bottom()[1])

        with self.voiceover(SAY[9]) as vo:
            reset(self, t2, 8, run_time=0.35, extra=[tr.goto(6)])    # a clean screen: no scrolling in the race
            tcmd(self, t2, RUN[D], 0.4)
            enter(self, t2, D, run_time=0.25, extra=[tr.goto(7)])
            tcmd(self, t2, UVA[D].cmd, 0.4)
            tprint(self, t2, UVA[D].at(2, 8), run_time=0.25)
            vo.wait_until("and set the group name")
            self.play(tr.goto(8), FadeIn(ins_d, shift=DOWN * 0.1), run_time=0.3)
            self.play(gn_d.animate.set_color(TURN), Create(u_gn_d), run_time=0.35)
            self.play(tr.goto(9), run_time=0.2)            # the inset stays up while --help runs
            c9 = tcmd(self, t2, "python cli.py --help", 0.35)
            o9 = tprint(self, t2, HELP_D_OUT[:-1] + [(HELP_D_OUT[-1], ERR)], wrap=True, run_time=0.35, lag=0.06)
            d1, d2 = o9[-2], o9[-1]
            vo.wait_until("Like C, even help")
            nk9 = at_right(ttag("recorded without the key"), t2, d2)
            pin(self, d2, nk9, run_time=0.25)
            resize(self, t2, 3, keep=[c9, d1, d2], run_time=0.45,
                   extra=[FadeOut(VGroup(ins_d, u_gn_d), shift=UP * 0.1), FadeIn(hp_d, shift=DOWN * 0.1)])
            vo.wait_until("Pause and catch up")
            self.play(FadeOut(hp_d), FadeIn(card_d, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(yt9, shift=LEFT * 0.1), run_time=0.35)
            self.play(Wiggle(yt9, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)
            self.wait(2.7)                                    # the static card: >= 4 s

        # ========================================================== 10 · V8: Translation has no stub
        p58 = dedent_panel(CLI_D, 58, 65)
        place(p58, left=-6.4, top=TOP)
        api2 = ApiCall("Translation", "D · translate_text")
        api2.shift(DOWN * 2.8)
        cy2 = api2.ctr.frame.get_center()[1]
        api2.ctr.frame.become(box(4.9, 2.0, CTR, fill_opacity=0.06).move_to([-6.4 + 2.45, cy2, 0]))
        api2.ctr.title.next_to(api2.ctr.frame, UP, buff=0.12)
        api2.link.put_start_and_end_on(api2.ctr.frame.get_right() + RIGHT * 0.1,
                                       api2.api.shape.get_left() + LEFT * 0.1)
        fr2 = api2.ctr.frame
        folder = file_row(f"text_translated/{GROUP}/", color=INK, glyph_color=LAPTOP)
        place(folder, left=fr2.get_left()[0] + 0.15, cy=fr2.get_bottom()[1] + 0.35)
        cloud2 = api2.api.shape.get_center()
        lk2 = api2.link.get_center()
        assert api2.ctr.title.get_top()[1] < p58.get_bottom()[1] - 0.08, (api2.ctr.title.get_top(), p58.get_bottom())
        assert api2.get_bottom()[1] > -3.6
        en_pg = page_token(long=True).move_to(fr2.get_center() + UP * 0.25)
        fr_pg = page_token(fr=True)
        cost10 = cost_tag()
        place(cost10, cx=lk2[0], cy=lk2[1] + 0.9)
        nostub = ttag("no ticket stub")
        place(nostub, cx=lk2[0], cy=lk2[1] + 0.36)
        assert cost10.get_top()[1] < p58.get_bottom()[1] - 0.08, (cost10.get_top(), p58.get_bottom())
        saved = VGroup(gray_line("saved here · line 68"), gray_line("on your laptop"))
        saved.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        place(saved, left=fr2.get_right()[0] + 0.3, cy=folder.get_center()[1])
        assert saved.get_right()[0] < api2.api.shape.get_left()[0] - 0.15, saved.get_right()
        assert saved.get_top()[1] < nostub.get_bottom()[1] - 0.1, (saved.get_top(), nostub.get_bottom())
        bt = mono(f"text_translated/{GROUP}/", 20, INK)
        bfr = box(bt.width + 0.5, 0.8, CLOUD, dashed=True)
        bt.move_to(bfr.get_top() + DOWN * 0.24)
        bucket = VGroup(bfr, bt)
        place(bucket, right=EDGE, top=1.9)
        bcap = sans("bucket", 20, CLOUD).next_to(bfr, UP, buff=0.1).align_to(bfr, LEFT)
        up_note = gray_line(("--upload",), "puts it here · still empty")
        place(up_note, right=EDGE, top=bfr.get_bottom()[1] - 0.15)
        assert bucket.get_left()[0] > p58.get_right()[0] + 0.2, (bucket.get_left(), p58.get_right())
        assert up_note.get_bottom()[1] > api2.api.title.get_top()[1] + 0.1, up_note.get_bottom()

        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(t2, card_d, yt9)), FadeIn(api2), FadeIn(folder), FadeIn(p58, shift=DOWN * 0.1),
                      run_time=0.6)
            bar10 = VGroup(line_bar(p58.code, 2, TURN), line_bar(p58.code, 3, TURN))
            self.play(FadeIn(en_pg, scale=0.6), FadeIn(bar10), code_span(p58.code, 2, '"en"').animate.set_color(TURN),
                      code_span(p58.code, 3, '"fr"').animate.set_color(TURN), run_time=0.4)
            self.play(en_pg.animate.move_to(cloud2), FadeIn(cost10, shift=DOWN * 0.1), FadeIn(nostub), run_time=0.8)
            self.play(FadeOut(en_pg, scale=0.4), Indicate(api2.api.shape, color=CLOUD, scale_factor=1.05), run_time=0.4)
            vo.wait_until("the French comes straight back")
            fr_pg.move_to(cloud2)
            self.play(FadeIn(fr_pg, scale=0.6), run_time=0.25)
            self.play(fr_pg.animate.move_to(fr2.get_center() + UP * 0.25), run_time=0.7)
            self.play(pulse(nostub.box, nostub.text, scale=1.1), run_time=0.5)
            vo.wait_until("is printed")
            self.play(Transform(bar10, line_bar(p58.code, 7, TURN)), Indicate(fr_pg, color=INK, scale_factor=1.15),
                      run_time=0.5)
            vo.wait_until("and saved under")
            self.play(fr_pg.animate.next_to(folder, UP, buff=0.08).align_to(folder, LEFT).shift(RIGHT * 0.05), run_time=0.5)
            self.play(Indicate(folder, color=LAPTOP, scale_factor=1.06), FadeIn(saved, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("so D needs an upload")
            self.play(FadeIn(bucket), FadeIn(bcap), run_time=0.45)
            self.play(FadeIn(up_note, shift=DOWN * 0.1), run_time=0.4)

        # ========================================================== 11 · D10-D13: download, translate, upload; rebuild
        t3 = term(P_CTR, 11, component=D)
        rc11 = readme_chip("README.md · lines 155–157")
        place(rc11, left=-6.4, cy=2.45)
        sm11 = tag("same as -d · -t · -u", S.GREY)
        place(sm11, left=rc11.get_right()[0] + 0.3, cy=rc11.get_center()[1])
        assert rc11.get_bottom()[1] > strip_top(11) + 0.08, (rc11.get_bottom(), strip_top(11))

        with self.voiceover(SAY[11]) as vo:
            # "Pause" opens this line: ▶ lands beside the first command to run in the same move that
            # brings the terminal back (0.9 s), and stays until the section switch
            vo.wait_until("Pause to run")
            l11a, yt11 = back_to_terminal(self, VGroup(api2, folder, p58, bar10, cost10, nostub, fr_pg, saved, bucket,
                                                       bcap, up_note), t3, rc11, sm11, tr.goto(10), CMDS[D][0])
            self.play(Wiggle(yt11, scale_value=1.12, rotation_angle=0.02 * TAU), tr.goto(11), run_time=0.6)
            l11 = tcmd(self, t3, CMDS[D][1], 0.4)
            pin(self, l11, beside(ttag("billed", COST), t3, l11), run_time=0.25)
            self.play(tr.goto(12), run_time=0.2)
            tcmd(self, t3, CMDS[D][2], 0.4)
            self.play(tr.goto(13), run_time=0.2)
            tcmd(self, t3, "exit", 0.25)
            leave(self, t3, P_D)
            c11 = tcmd(self, t3, BUILD[D], 0.45)
            yt11b = beside(your_turn(), t3, c11)
            pin(self, c11, yt11b, run_time=0.25)              # and on the rebuild as soon as it is typed (as in E12)
            o11, _ = live_build(self, t3, RBLD[D])
            cached_green(self, o11[1], run_time=0.3)
            self.wait(1.0)                                    # the CACHED rows, before the section switch

        # ========================================================== 12 · E1-E9: the montage again; the help slip
        dfE = file_panel(f"files/{E}.Dockerfile", 3, 3, f"{E}/Dockerfile")
        place(dfE, right=EDGE, top=TOP)
        ins_e, gn_e, u_gn_e = inset18(CLI_E)
        assert ins_e.get_bottom()[1] > strip_top(8) + 0.08, ins_e.get_bottom()
        hp_e = help_panel(E)
        r5 = hp_e.rows[2]
        assert r5.text == "Synthesis audio from text"
        b5 = rbar(r5, VENV, 0.22)
        readme_t = ttag("README")
        place(readme_t, left=r5.glyphs.get_right()[0] + 0.4, cy=r5.strut.get_center()[1])
        x_row = mono_line(ARGP, 20, INK)
        x_fr = box(x_row.width + 0.5, x_row.strut.height + 0.34, S.GREY, fill=S.BG, fill_opacity=1, radius=0.12)
        x_row.move_to(x_fr)
        x_head = VGroup(mono(CLI_E, 20, S.GREY), label("· line 105 (excerpt)", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        x_head.next_to(x_fr, UP, buff=0.08).align_to(x_fr, LEFT).shift(RIGHT * 0.1)
        x_top, x_bot = STRIP + 0.06, BOTTOM_Y - 0.08          # covers the whole strip
        x_bg = Rectangle(width=13.0, height=x_top - x_bot, stroke_width=0).set_fill(S.BG, 1)
        x_bg.move_to([0, (x_top + x_bot) / 2, 0])
        x_body = VGroup(x_fr, x_row, x_head)
        place(x_body, left=-6.2, top=STRIP - 0.12)
        xchip = VGroup(x_bg, x_body)
        x_err = erratum_tag()
        place(x_err, left=x_head.get_right()[0] + 0.3, cy=x_head.get_center()[1])
        x_note = gray_line("pasted from", ("transcribe_audio/cli.py",))
        place(x_note, left=x_fr.get_left()[0] + 0.1, top=x_fr.get_bottom()[1] - 0.14)
        assert x_note.get_bottom()[1] > BOTTOM_Y and x_err.get_right()[0] < EDGE, (x_note.get_bottom(), x_err.get_right())
        card_e = steps_card(E, montage_items(E))
        place(card_e, left=-6.4, top=TOP)
        yt12 = your_turn()
        place(yt12, left=card_e.frame.get_right()[0] + 0.35, bottom=card_e.frame.get_bottom()[1])

        with self.voiceover(SAY[12]) as vo:
            PACE[0] = 0.5                                     # the montage: quicker scrolls
            trE = tracker("E", 1)
            reset(self, t3, 8, run_time=0.35, extra=[FadeOut(VGroup(rc11, sm11)), FadeOut(tr, shift=UP * 0.25),
                                                    FadeIn(trE, shift=DOWN * 0.25)])
            tr = trE
            tcmd(self, t3, CD[E], 0.25)
            t3.set_prompt(P_E)
            bare_prompt(self, t3)
            keyg = drop_key(self, cy=2.45, extra=[tr.goto(2)], k=0.45)
            self.play(FadeOut(keyg), tr.goto(3), run_time=0.15)
            tcmd(self, t3, UVI_CMD, 0.25)
            tprint(self, t3, [UVI[E].line(2)], run_time=0.15)
            self.play(tr.goto(4), FadeIn(dfE, shift=DOWN * 0.1), run_time=0.25)
            self.play(FadeOut(dfE, shift=UP * 0.1), tr.goto(5), run_time=0.2)
            tcmd(self, t3, BUILD[E], 0.25)
            o12, _ = live_build(self, t3, BLD[E], rows_=(14,), run_time=0.2)
            self.play(substring(o12[1], "CACHED").animate.set_color(VENV), tr.goto(6), run_time=0.15)
            tcmd(self, t3, RUN[E], 0.25)
            enter(self, t3, E, run_time=0.15, extra=[tr.goto(7)])
            tcmd(self, t3, UVA[E].cmd, 0.25)
            tprint(self, t3, UVA[E].at(2, 8), run_time=0.15)
            gn_e.set_color(TURN)
            self.play(tr.goto(8), FadeIn(ins_e, shift=DOWN * 0.1), Create(u_gn_e), run_time=0.25)
            self.play(tr.goto(9), run_time=0.15)           # the inset stays up while --help runs
            c12 = tcmd(self, t3, "python cli.py --help", 0.25)
            o12b = tprint(self, t3, [(HELP_E_OUT[0], ERR)], wrap=True, run_time=0.15)
            nk12 = at_right(ttag("recorded without the key"), t3, o12b[-1])
            pin(self, o12b[-1], nk12, run_time=0.15)
            PACE[0] = 1.0
            vo.wait_until("its help text says")
            resize(self, t3, 3, keep=[c12, o12b[0], o12b[1]], run_time=0.4,
                   extra=[FadeOut(VGroup(ins_e, u_gn_e), shift=UP * 0.1), FadeIn(hp_e, shift=DOWN * 0.1)])
            vo.wait_until("transcribe audio file to text")
            self.play(FadeIn(b5), FadeIn(readme_t, shift=LEFT * 0.1), run_time=0.35)
            self.play(FadeIn(xchip, shift=UP * 0.3), run_time=0.5)
            desc = substring(x_row, '"Transcribe audio file to text"')
            self.play(desc.animate.set_color(ERR), run_time=0.35)
            vo.wait_until("pasted from A's code")
            self.play(FadeIn(x_err, shift=LEFT * 0.1), FadeIn(x_note, shift=DOWN * 0.1), run_time=0.45)
            vo.wait_until("Pause and catch up")
            self.play(FadeOut(VGroup(hp_e, b5, readme_t, xchip, x_err, x_note)), FadeIn(card_e, shift=DOWN * 0.1),
                      run_time=0.5)
            self.play(FadeIn(yt12, shift=LEFT * 0.1), run_time=0.35)
            self.play(Wiggle(yt12, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)
            self.wait(2.7)                                    # the static card: >= 4 s

        # ========================================================== 13 · E10-E11: download, synthesis
        # no picture here: the terminal grows back to full size (as in C10 and D10), the README chip
        # sits under the tracker, and ▶ goes beside a command (the --synthesis row is full with "billed")
        rc13 = readme_chip("README.md · lines 162–163")
        place(rc13, left=-6.4, cy=2.45)
        sm13 = tag("same as -d · -s", S.GREY)
        place(sm13, left=rc13.get_right()[0] + 0.3, cy=rc13.get_center()[1])
        assert rc13.get_bottom()[1] > strip_top(10) + 0.08, (rc13.get_bottom(), strip_top(10))

        with self.voiceover(SAY[13]) as vo:
            resize(self, t3, 10, run_time=0.45, extra=[FadeOut(VGroup(card_e, yt12)), FadeIn(rc13, shift=DOWN * 0.1),
                                                      FadeIn(sm13, shift=DOWN * 0.1), tr.goto(10)])
            l13a = tcmd(self, t3, CMDS[E][0], 0.4)
            self.play(tr.goto(11), run_time=0.2)
            l13 = tcmd(self, t3, CMDS[E][1], 0.4)
            pin(self, l13, beside(ttag("billed", COST), t3, l13), run_time=0.25)
            vo.wait_until("with your key")
            yt13 = beside(your_turn(), t3, l13a)
            assert yt13.get_left()[0] > l13a.glyphs.get_right()[0] + 0.1, (yt13.get_left(), l13a.glyphs.get_right())
            pin(self, l13a, yt13, run_time=0.3)
            self.play(Wiggle(yt13, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)
            self.wait(0.6)                                    # hold the pause point

        # ========================================================== 14 · the ElevenLabs bonus: X1-X2
        opt = optional_tag()
        _wide = tracker("X", 2)                              # the widest caption: "step 2 of 3: uv add requests"
        place(opt, left=_wide.get_right()[0] + 0.35, cy=_wide.get_center()[1])
        assert opt.get_top()[1] < 3.55 and opt.get_bottom()[1] > 2.95, (opt.get_top(), opt.get_bottom())
        fr14 = page_token(fr=True)
        el = cloud(2.6, color=S.GREY)
        el_t = sans("ElevenLabs", 20, INK)
        el_c = label("the instructor's voice", 20, S.GREY).next_to(el, DOWN, buff=0.12)
        bdr_t = mono("output_audios_pp/", 20, INK)
        bdr_f = box(bdr_t.width + 0.5, 1.1, CLOUD, dashed=True)
        bdr_t.move_to(bdr_f.get_top() + DOWN * 0.24)
        bdr = VGroup(bdr_f, bdr_t)
        bonus_t = tag("bonus", S.GREY)
        row14 = VGroup(fr14, el, bdr).arrange(RIGHT, buff=1.6)
        place(row14, cx=0, cy=1.0)
        el_t.next_to(el, UP, buff=0.12)
        el_c.next_to(el, DOWN, buff=0.12)
        bonus_t.next_to(bdr_f, DOWN, buff=0.12)
        a14a = Arrow(fr14.get_right(), el.get_left(), buff=0.15, color=S.GREY, stroke_width=3)
        a14b = Arrow(el.get_right(), bdr_f.get_left(), buff=0.15, color=S.GREY, stroke_width=3)
        wv14 = wave_token(0.34).move_to(el)
        wv14_to = bdr_f.get_bottom() + UP * 0.32
        assert wv14_to[1] + 0.17 < bdr_t.get_bottom()[1] - 0.08
        quota14 = cost_tag("your own ElevenLabs key and quota")
        ill14 = illustration_tag()
        place(ill14, right=EDGE, top=TOP)
        # X1: the key file; the group name in cli_11.py
        kf_name = file_row("secrets/11lab_api_key.txt", color=INK, glyph_color=S.GREY)
        kf_line = mono_line("XI_API_KEY=…", 20, INK)
        kf_body = VGroup(kf_name, kf_line).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        kf_line.shift(RIGHT * 0.4)
        kf_fr = box(kf_body.width + 0.5, kf_body.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
        kf_fr.move_to(kf_body)
        kf_head = VGroup(mono(f"{E}/README.md", 20, S.GREY), label("· lines 139–142", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        kf_head.next_to(kf_fr, UP, buff=0.08).align_to(kf_fr, LEFT).shift(RIGHT * 0.1)
        kcard = VGroup(kf_fr, kf_body, kf_head)
        place(kcard, left=-6.4, top=TOP)
        place(quota14, right=EDGE, cy=kf_fr.get_center()[1])
        assert quota14.get_left()[0] > kcard.get_right()[0] + 0.2, (quota14.get_left(), kcard.get_right())
        p19 = src_panel(CLI_11, 19, 19, cut_comments=True, size=20)
        ins19 = editor_inset(p19)
        place(ins19, left=-6.4, top=kcard.get_bottom()[1] - 0.3)
        gn19 = code_span(p19.code, 0, "group_name")
        u19 = Line(gn19.get_corner(DL) + DOWN * 0.05, gn19.get_corner(DR) + DOWN * 0.05, color=TURN, stroke_width=4)
        cap19 = VGroup(gray_line((f"{E}/README.md",)), gray_line("· line 112: here too"))
        cap19.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        place(cap19, left=ins19.get_right()[0] + 0.4, cy=p19.code.get_center()[1])
        note14 = gray_line((f"{C}/README.md",), "mentions", ("cli_11.py",), "too · the file is in", (f"{E}/",))
        place(note14, cx=0, top=row14.get_bottom()[1] - 0.75)
        assert ins19.get_bottom()[1] > STRIP + 0.1 and cap19.get_right()[0] < EDGE, (ins19.get_bottom(), cap19.get_right())
        assert note14.get_right()[0] < EDGE and note14.get_bottom()[1] > STRIP + 0.1, (note14.get_right(), note14.get_bottom())

        with self.voiceover(SAY[14]) as vo:
            (l13a.rows[-1] if hasattr(l13a, "rows") else l13a).remove(yt13)
            self.add(yt13)                                    # ▶ leaves with the chips; the strip keeps the commands
            resize(self, t3, 3, keep=[l13a, l13], run_time=0.4, extra=[FadeOut(VGroup(rc13, sm13, yt13))])
            tr = switch_section(self, tr, "X", None, run_time=0.5)
            self.play(FadeIn(opt, shift=LEFT * 0.1), FadeIn(fr14, shift=RIGHT * 0.1), FadeIn(VGroup(el, el_t)),
                      FadeIn(bdr), FadeIn(bonus_t), FadeIn(ill14), run_time=0.45)
            vo.wait_until("speaks the French")
            self.play(GrowArrow(a14a), fr14.animate.move_to(el.get_center()).set_opacity(0), run_time=0.7)
            self.remove(fr14)
            self.play(FadeIn(wv14, scale=0.6), Indicate(el, color=INK, scale_factor=1.05), run_time=0.35)
            self.play(GrowArrow(a14b), wv14.animate.move_to(wv14_to), run_time=0.7)
            self.play(FadeIn(note14, shift=UP * 0.1), run_time=0.35)
            vo.wait_until("in the instructor's voice")
            self.play(FadeIn(el_c, shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(wv14, color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("It uses your own")
            self.play(FadeOut(VGroup(fr14, el, el_t, el_c, bdr, bonus_t, a14a, a14b, ill14, wv14, note14)), run_time=0.45)
            self.play(FadeIn(quota14, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("a key file in secrets")
            self.play(tr.goto(1), FadeIn(kcard, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(kf_line, color=INK, scale_factor=1.08), run_time=0.5)
            vo.wait_until("your group name in the bonus")
            self.play(FadeIn(ins19, shift=DOWN * 0.1), run_time=0.4)
            self.play(gn19.animate.set_color(TURN), Create(u19), FadeIn(cap19, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("and uv add requests")
            self.play(tr.goto(2), run_time=0.25)
            tcmd(self, t3, REQ.cmd, 0.4)
            o14 = tprint(self, t3, REQ.at(2, 3), run_time=0.3)
            ai = beside(ttag("already installed · now listed"), t3, o14[1], buff=0.4)
            pin(self, o14[1], ai, run_time=0.35)

        # ========================================================== 15 · X3: cli_11.py reads the key file at start-up
        rc15 = VGroup()
        for s in BONUS_CMDS:
            rc15.add(mono_line(s, 20, INK))
        rc15.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rc15_fr = box(rc15.width + 0.5, rc15.height + 0.36, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
        rc15.move_to(rc15_fr)
        rc15_h = VGroup(mono(f"{E}/README.md", 20, S.GREY), label("· lines 151–153", 20, S.GREY)).arrange(RIGHT, buff=0.12)
        rc15_h.next_to(rc15_fr, UP, buff=0.08).align_to(rc15_fr, LEFT).shift(RIGHT * 0.1)
        card15 = VGroup(rc15_fr, rc15, rc15_h)
        place(card15, left=-6.4, top=TOP)
        quota_to = quota14.copy()                     # the X1 tag moves next to the commands
        place(quota_to, left=card15.get_right()[0] + 0.4, cy=rc15_fr.get_center()[1])
        assert card15.get_bottom()[1] > strip_top(7) + 0.1 and quota_to.get_right()[0] < EDGE, quota_to.get_right()
        p30 = src_panel(CLI_11, 30, 39, size=20)
        place(p30, left=-6.4, top=TOP + 0.02)
        assert p30.get_bottom()[1] > STRIP + 0.03, p30.get_bottom()
        bar30 = VGroup(*[line_bar(p30.code, k, TURN) for k in range(3, 8)])
        startup = sans("read at start-up", 22, TURN)
        place(startup, left=p30.get_right()[0] + 0.4, cy=bar30.get_center()[1])
        assert startup.get_right()[0] < EDGE

        with self.voiceover(SAY[15]) as vo:
            self.play(FadeOut(VGroup(kcard, ins19, u19, cap19)), tr.goto(3), run_time=0.4)
            resize(self, t3, 7, run_time=0.45, extra=[FadeIn(card15, shift=DOWN * 0.1),
                                                     quota14.animate.move_to(quota_to)])
            c15 = tcmd(self, t3, BONUS_CMDS[0], 0.45)
            o15 = tprint(self, t3, C11_OUT[:-1] + [(C11_OUT[-1], ERR)], wrap=True, run_time=0.35, lag=0.08)
            f1, f2 = o15[-2], o15[-1]
            vo.wait_until("even download fails")
            uf = Line([f1.glyphs.get_left()[0], f1.strut.get_bottom()[1] + 0.01, 0],
                      [f1.glyphs.get_right()[0], f1.strut.get_bottom()[1] + 0.01, 0], color=ERR, stroke_width=3)
            self.play(Create(uf), run_time=0.3)
            stick(self, f1, uf)
            nk15 = at_right(ttag("recorded without the key"), t3, f2)
            pin(self, f2, nk15, run_time=0.3)
            vo.wait_until("the script reads that file")
            resize(self, t3, 3, keep=[c15, f1, f2], run_time=0.45,
                   extra=[FadeOut(VGroup(card15, quota14)), FadeIn(p30, shift=UP * 0.2)])
            self.play(FadeIn(bar30), FadeIn(startup, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("as soon as it starts")
            self.play(Indicate(code_span(p30.code, 0, "'secrets/11lab_api_key.txt'"), color=INK, scale_factor=1.06),
                      Indicate(code_span(p30.code, 3, "open(secrets_file_path)"), color=INK, scale_factor=1.08),
                      run_time=0.8)

        # ========================================================== 16 · E12: exit, rebuild; the pipeline fills
        relay = Relay(width=12.4, labels=False, bonus=True, box_h=0.8, gap=0.55)
        place(relay, cx=0, top=2.62)
        for let, b in zip(relay.letters, relay.boxes):
            let.move_to(b)
        relay.parts["bonus_tag"].next_to(relay.bonus.frame, LEFT, buff=0.2)
        done = VGroup(*[relay.token_at(i) for i in (0, 1, 2)])
        done[2].scale(0.8, about_edge=DOWN)
        news = [(2, "wave"), (3, "fr"), (4, "wave")]
        toks = [token_at_box(relay, j, k).shift(RIGHT * 0.36) for j, k in news]    # where "billed" goes
        for (j, _), tk in zip(news, toks):
            assert tk.get_right()[0] < relay.boxes[j].get_right()[0] - 0.03, (j, tk.get_right())
            assert tk.get_left()[0] > relay.letters[j].get_right()[0] - 0.45 + 0.05, (j, tk.get_left())
        grp = VGroup(label("your group's files:", 20, S.GREY), mono(f"<prefix>/{GROUP}/…", 20, LOOKUP))
        grp.arrange(RIGHT, buff=0.15)
        place(grp, left=relay.cabinet.get_left()[0] + 0.05, top=relay.cabinet.get_bottom()[1] - 0.15)
        # GOLD "billed" inside C, D and E, right of their letters (which step left)
        billed = VGroup(*[ttag("billed", COST).move_to(relay.boxes[j].get_center() + RIGHT * 0.36) for j in (2, 3, 4)])
        for j, bt in zip((2, 3, 4), billed):
            assert bt.get_right()[0] < relay.boxes[j].get_right()[0] - 0.05, j
        lb = Leaderboard(row_h=0.46)
        place(lb, cx=0.35, top=relay.bonus.frame.get_bottom()[1] - 0.15)
        for c in (0, 1):
            lb.cells[0][c].set_fill(VENV, 0.55).set_stroke(VENV, 2)
        lb_ill = illustration_tag()
        place(lb_ill, right=lb.col_names[0].get_left()[0] - 0.3, cy=lb.col_names[0].get_center()[1])
        assert lb.get_bottom()[1] > -3.55 and lb_ill.get_left()[0] > -6.5 and lb.get_right()[0] < EDGE, \
            (lb.get_bottom(), lb_ill.get_left(), lb.get_right())
        assert grp.get_right()[0] < relay.bonus.frame.get_left()[0] - 0.1 and grp.get_bottom()[1] > lb.get_top()[1], \
            (grp.get_right(), grp.get_bottom(), lb.get_top())

        with self.voiceover(SAY[16]) as vo:
            trE = tracker("E", 12)
            # a cleared 8-row terminal: exit + build + its 5 rows fit without scrolling
            reset(self, t3, 8, run_time=0.4, extra=[FadeOut(VGroup(tr, opt), shift=UP * 0.25),
                                                   FadeIn(trE, shift=DOWN * 0.25), FadeOut(VGroup(p30, bar30, startup))])
            tr = trE
            tcmd(self, t3, "exit", 0.2)
            leave(self, t3, P_E, run_time=0.2)
            c16 = tcmd(self, t3, BUILD[E], 0.35)
            yt16 = beside(your_turn(), t3, c16)
            pin(self, c16, yt16, run_time=0.25)               # ▶ as soon as the rebuild is typed
            o16, _ = live_build(self, t3, RBLD[E], run_time=0.25)
            cached_green(self, o16[1], run_time=0.2)
            vo.wait_until("With all five done")
            self.play(FadeOut(t3), FadeIn(VGroup(relay.cabinet, relay.drawers, relay.boxes)), run_time=0.5)
            relay.reveal(self, "letters", "drawer_labels", "bonus_tag", run_time=0.4,
                         extra=[FadeIn(done), FadeIn(relay.bonus), FadeIn(grp, shift=UP * 0.1)])
            vo.wait_until("your group's drawers fill")
            # C, D and E's letters step left; each box's new token appears in the space they leave
            self.play(*[FadeIn(tk, scale=0.5) for tk in toks],
                      *[relay.letters[j].animate.shift(LEFT * 0.45) for j in (2, 3, 4)],
                      *[Indicate(relay.boxes[j], color=CTR, scale_factor=1.08) for j, _ in news], run_time=0.5)
            self.play(*[tk.animate.move_to(relay.slot(j + 1)) for tk, (j, _) in zip(toks, news)],
                      FadeIn(billed, shift=LEFT * 0.1), run_time=0.8)
            vo.wait_until("and your leaderboard row")
            self.play(FadeIn(lb), FadeIn(lb_ill), run_time=0.45)
            self.play(LaggedStart(*[lb.light(0, c) for c in (2, 3, 4)], lag_ratio=0.35),
                      Indicate(lb.row_names[0], color=INK, scale_factor=1.1), run_time=0.9)

        self.wait(0.8)                                        # the lit row, before the fade
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)


def token_at_box(relay, j: int, kind: str) -> VGroup:
    """A new token (not on screen) in box j."""
    from common import token
    return token(kind).move_to(relay.center_of(j))
