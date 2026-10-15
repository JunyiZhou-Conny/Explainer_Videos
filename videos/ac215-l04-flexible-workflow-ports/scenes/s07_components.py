"""S07 · Five components, five honest errors (Quick Reference, all five components: QA/2 to QE/3;
generate_text README "Other model"; two errata).

Beats (script.md "## S07", one voiceover block each):
 0  TRACKER QA/2. The TEAL terminal fades in empty (13 rows, container · transcribe_audio, prompt
    app@0ceffb272288:/app$); `python cli.py --download` -> mega-transcribe_audio/09 lines 2–3, …,
    11–12, …, 52 (wrapped); line 11 turns YELLOW, line 52 prints RED with the tag "recorded
    without a key".
 1  The terminal shrinks to the strip (the command and the error). Above it, a glyph-only V3
    miniature (no key on the laptop, the dashed /secrets slot empty, "gate 1 · who?"): the route
    pulses, the slot flashes RED, a request dot stops at the container's wall with a RED flash,
    the doors stay dark. Three RED 20 pt chips write in: no key in ../../secrets/ · another file
    name · script run from another folder.
 2  TRACKER QA/3, QA/4: the strip types `python cli.py --transcribe` and `python cli.py --upload`,
    each with a GREY note "same error, same reason". Above, the GREY card "with your key, look for"
    writes in line by line (cli.py lines 44; 67, 86; 62; 108) and a BLUE drawer
    text_prompts/group-01/ lights (illustration).
 3  GOLD tag "Speech-to-Text: billed per minute of audio"; CODE(transcribe_audio/cli.py: 84–86),
    results[0] underlined RED, tag "erratum · keeps only the first chunk", GREY chip "main branch:
    joins all chunks". The panel clears; a static GREY card (transcribe_audio, with your key: the
    three commands, then check text_prompts/group-01/ in the bucket) with ▶ your turn and the
    GREY note "with your key".
 4  The terminal grows back (13 rows): `exit` -> mega-laptop/12 lines 38–39; GREY frame, prompt
    …/transcribe_audio$; `cd ../generate_text` (README chip "README.md · line 52" in the top band);
    TRACKER QB/1; `./docker-shell.sh` -> 31 lines 4, 14–17, 24, 26–27 (BuildKit rows): [2/5] gets a
    TEAL badge + box, its 24.8s tag YELLOW; generate_text/Dockerfile · line 4 as a one-line chip in
    the band, GREY note "build-essential only · no ffmpeg" beside the command; "Building 52.6s"
    underlined. TEAL frame, app@45263bb6ca36:/app$, `python cli.py --help` -> 31 lines 28–37;
    README chip generate_text/README.md · lines 114–123 with a GREEN tick "identical".
 5  TRACKER QB/2: the terminal clears; `python cli.py --download` -> mega-generate_text/02 lines
    2–3, …, 11–12, …, 52 (RED, tag "recorded without a key"). TRACKER QB/3: `python cli.py
    --generate` -> 03 lines 2–3; GREY chip "exit status 0 · from the capture" beside it. On the
    question the terminal shrinks to the strip. PONDER (6 s) above the strip.
 6  Excerpt chip generate_text/cli.py · line 53 (glob.glob(…)) over line 54 (for text_file in
    text_files:); the glob highlights, a GREY bubble "[ ] · no files" pops from it, a GREY drawer
    text_prompts/group-01/ "on your laptop · empty"; the for chip dims, RED "0 rounds". The exit
    chip in the strip flashes.
 7  TRACKER QB/4: the strip (5 rows here) types `python cli.py --upload`, GREY note "needs the
    key". TRACKER QB/5: README chip generate_text/README.md · lines 91–94 in the band; `export
    GEMINI_MODEL=gemini-2.5-flash`, `python cli.py --generate` -> 05 lines 3–4. Above:
    CODE(generate_text/cli.py: 73–77), line 73 barred YELLOW, os.environ.get(…) boxed, the
    default underlined GREY with the tag "default"; GOLD tag "Gemini: billed per token".
 8  TRACKER QC/1. The terminal grows (13 rows): `exit` -> 31 lines 38–39; `cd
    ../synthesis_audio_en`; `./docker-shell.sh` -> 40 lines 4, 14–17, 24, 26–27; "Building 8.2s"
    underlined; "CACHED [2/5]" boxed GREEN, tag "same as generate_text"; TEAL frame,
    app@ba0b1df0eadc:/app$, `python cli.py --help` -> 40 lines 28–33: line 33 RED with the GREY
    tag "cli.py left unedited on purpose"; the assert line flashes.
 9  TRACKER QC/1 · extra. The TEAL terminal shrinks to 6 rows; a second terminal (5 rows) opens
    on ~ (flashing YELLOW, "new terminal: cd here first"), then …/synthesis_audio_en$. Title-bar
    icons: cli.py (laptop) and /app/cli.py (container). A pencil edits cli.py ("in your editor");
    both icons blink at the same instant; `git diff cli.py` (extra) -> 41 lines 16–17. The second
    terminal goes, the TEAL terminal grows to 10 rows: `python cli.py --help` ->
    mega-synthesis_audio_en/02 lines 2–4, …, 55 (wrapped): line 3 YELLOW, CODE(cli.py: 23) as a
    one-line chip above with the tag "runs on import", line 55 RED.
10  The terminal shrinks to the strip. PANEL(expected/mega-synthesis_audio_en-help: 3–10, "with
    your key · synthesis_audio_en/README.md · lines 99–107"), tag expected. TRACKER QC/2, QC/3:
    `python cli.py --download`, `python cli.py --synthesis` (GREY "needs the key" each). README
    chip README.md · line 257 "no separate --upload step"; a BLUE Text-to-Speech door writes a
    waveform straight into a BLUE drawer text_audios/group-01/ (illustration); GREY caption "empty
    at first? …" ; GOLD tag "Text-to-Speech: billed per character".
11  Montage (12 rows), TRACKER QD/1→4: `exit` (40 lines 34–35), `cd ../translate_text`,
    `./docker-shell.sh` -> 51 lines 4, 14 (CACHED turns GREEN), app@40d7497c50f2:/app$ `python
    cli.py --help` -> 51 lines 28–31, …, 64–65 (joined, wrapped, RED); `--download`,
    `--translate`, `--upload` with GREY "needs the key".
12  Montage, TRACKER QE/1→3: `exit` (51 lines 66–67), `cd ../synthesis_audio`, `./docker-shell.sh`
    -> 61 lines 4, 14, app@6172f2cd7728:/app$ `python cli.py --help` -> 61 lines 28–31, …, 93–94;
    `--download`, `--synthesis`. The terminal gives way to the static GREY card: per folder the
    flags typed after `python cli.py`, and "with your key, look for" (message, cli.py line, bucket
    folder), footer "bucket looks empty? …"; ▶ your turn + GREY note "with your key".
13  Card 1 (erratum): CODE(translate_text/cli.py: 64) with "es" RED, over CODE(synthesis_audio/
    cli.py: 48–49) (comment cut) with fr-FR BLUE; GREEN fix chip target_language="fr" + GREY tag
    "you set it in Before you run, step 2". Card 2 (erratum): GREY caption "optional ElevenLabs
    bonus: cli_11.py looks for its key file inside /app" and the GREEN fix chip (header
    synthesis_audio/cli_11.py · line 30). No ▶. Fade out to an empty frame.

Deviations from SHOW (and why):
- Beat 0: the tag "recorded without a key" is pinned beside the error's second row (the only row
  with room); it stays in the strip with it.
- Beat 1: the miniature shows the laptop's secrets/ folder without a key (the most common cause,
  and the slot is empty); the readable label "gate 1 · who?" sits outside the glyph-only piece.
- Beat 4: [2/5] gets the TEAL badge "2" at the row's left margin and a TEAL box on "[2/5]" (the cut
  row has no room for the worded badge, as in S06); the Dockerfile chip goes in the top band
  (no room above a 13-row terminal) and its note "build-essential only · no ffmpeg" sits beside
  the `./docker-shell.sh` row.
- Beat 5: the terminal shrinks to the strip already as the question is asked (beat 6's strip), so
  the ponder card has the frame above it; the strip shows the generate command, its output and
  the exit chip (the question's evidence, not its answer).
- Beat 7: the strip is 5 rows here, so the export line stays visible with its output.
- Beat 8: the tag "same as generate_text" sits beside the [3/5] row, under the GREEN box on
  "CACHED [2/5]" (the cut [2/5] row has no room).
- Beat 9: the "folder icons" are two small title-bar icons (laptop: cli.py, container:
  /app/cli.py) that blink together; the second terminal leaves when the TEAL terminal grows to
  10 rows for the help output, so the line-23 chip can sit above it.
- Beat 10: the expected panel shows while download and synthesis are typed; the Text-to-Speech
  picture replaces it on "There's no upload step".
- Beat 12: the final card does not fit above the strip (five folders × two lines + headers ≈ 5.3
  tall at 20 pt), so the terminal leaves and the card stands below the tracker; its command
  column lists the flags under the header "python cli.py …" (each folder's commands in one row).
- Beat 13: no strip (the terminal left in beat 12); both cards stand centred below the tracker.
"""

from common import *
from common import _drop_bare, _header_text, _row_of, _save_op, _set_op
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Circle,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    RoundedRectangle,
    Transform,
    VGroup,
    Wiggle,
)

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import Terminal
from explainer.scene import VoiceScene

SAY = NARRATION["S07"]
assert len(SAY) == 14, len(SAY)

A, B, C, D, E = COMPONENTS
ML = "mega-laptop"
README = "mega-pipeline/README.md"
TA = "mega-pipeline/transcribe_audio/cli.py"
GB = "mega-pipeline/generate_text/cli.py"
GB_DOCKER = "mega-pipeline/generate_text/Dockerfile"
GB_README = "mega-pipeline/generate_text/README.md"
SE = "mega-pipeline/synthesis_audio_en/cli.py"
SE_README = "mega-pipeline/synthesis_audio_en/README.md"
TT = "mega-pipeline/translate_text/cli.py"
SY = "mega-pipeline/synthesis_audio/cli.py"
SY11 = "mega-pipeline/synthesis_audio/cli_11.py"
SY_README = "mega-pipeline/synthesis_audio/README.md"

# ------------------------------------------------------------------ the README's commands (checked)
QA_CMDS = excerpt(README, 237, 239).split("\n")
QB_CMDS = excerpt(README, 245, 247).split("\n")
QC_CMDS = excerpt(README, 253, 254).split("\n")
QD_CMDS = excerpt(README, 262, 264).split("\n")
QE_CMDS = excerpt(README, 270, 271).split("\n")
assert QA_CMDS == ["python cli.py --download", "python cli.py --transcribe", "python cli.py --upload"]
assert QB_CMDS == ["python cli.py --download", "python cli.py --generate", "python cli.py --upload"]
assert QC_CMDS == QE_CMDS == ["python cli.py --download", "python cli.py --synthesis"]
assert QD_CMDS == ["python cli.py --download", "python cli.py --translate", "python cli.py --upload"]
CD_B, CD_C, CD_D, CD_E = (f"cd ../{c}" for c in (B, C, D, E))     # README.md:52 (implied)
SHELL = "./docker-shell.sh"
assert "you'll `cd` into each one" in excerpt(README, 52, 52)
assert "no separate `--upload` step" in excerpt(README, 257, 257)
assert excerpt(GB_README, 92, 93) == "export GEMINI_MODEL=gemini-2.5-flash\npython cli.py --generate"

# ------------------------------------------------------------------ real outputs (checked)
CA9 = capture("09", "mega-transcribe_audio")
assert CA9.cmd == QA_CMDS[0] and CA9.exit == 1
assert CA9.line(11) == '  File "/app/cli.py", line 39, in download'
ERR_LINE = "google.auth.exceptions.DefaultCredentialsError: File /secrets/mega-pipeline.json was not found."
assert CA9.line(52) == ERR_LINE
C12 = capture("12", ML)
assert C12.at(38, 39) == ["app@0ceffb272288:/app$ exit", "exit"]
C31 = capture("31", ML)
assert C31.cmd == SHELL
B_BUILD = C31.at(4, (14, 17), 24)
assert "Building 52.6s" in B_BUILD[0] and "[2/5]" in B_BUILD[1] and B_BUILD[1].rstrip().endswith("24.8s")
assert C31.at(26, 27) == ["Run Docker container...", "Using local image..."]
assert C31.typed(28) == "python cli.py --help" and C31.at(38, 39) == ["app@45263bb6ca36:/app$ exit", "exit"]
assert [s.rstrip() for s in C31.at((29, 37))] == [s.rstrip() for s in excerpt(GB_README, 115, 123).split("\n")]
CB2 = capture("02", "mega-generate_text")
assert CB2.cmd == QB_CMDS[0] and CB2.line(52) == ERR_LINE
CB3 = capture("03", "mega-generate_text")
assert CB3.cmd == QB_CMDS[1] and CB3.at(2, 3) == ["Args: Namespace(download=False, generate=True, upload=False)",
                                                   "generate"] and CB3.exit == 0
CB5 = capture("05", "mega-generate_text")
assert CB5.cmd == "export GEMINI_MODEL=gemini-2.5-flash" and CB5.line(2) == "python cli.py --generate"
C40 = capture("40", ML)
C_BUILD = C40.at(4, (14, 17), 24)
assert "Building 8.2s" in C_BUILD[0] and "CACHED [2/5]" in C_BUILD[1] and "CACHED [3/5]" in C_BUILD[2]
assert C40.typed(28) == "python cli.py --help" and C40.line(33) == "AssertionError: Update group name"
assert C40.line(31).strip() == 'assert group_name!="", "Update group name"'
assert C40.at(34, 35) == ["app@ba0b1df0eadc:/app$ exit", "exit"]
C41 = capture("41", ML)
assert C41.cmd == "git diff cli.py" and C41.line(17).startswith('+group_name = "group-01"')
CC2 = capture("02", "mega-synthesis_audio_en")
assert CC2.cmd == "python cli.py --help" and CC2.line(3) == '  File "/app/cli.py", line 23, in <module>'
assert CC2.line(55) == ERR_LINE
EXP = capture("mega-synthesis_audio_en-help", "expected")
assert [s.rstrip() for s in EXP.at((3, 10))] == [s.rstrip() for s in excerpt(SE_README, 100, 107).split("\n")]
C51 = capture("51", ML)
assert "Building 7.9s" in C51.line(4) and "CACHED [2/5]" in C51.line(14)
assert C51.typed(28) == "python cli.py --help" and C51.join(64, 65) == ERR_LINE
assert C51.at(66, 67) == ["app@40d7497c50f2:/app$ exit", "exit"]
C61 = capture("61", ML)
assert "Building 7.9s" in C61.line(4) and "CACHED [2/5]" in C61.line(14)
assert C61.typed(28) == "python cli.py --help" and C61.join(93, 94) == ERR_LINE

# ------------------------------------------------------------------ sources quoted (checked)
assert excerpt(TA, 39, 39).strip() == "client = storage.Client()"
assert excerpt(TA, 44, 44).strip() == "print(blob.name)"
assert excerpt(TA, 62, 62).strip() == 'text_file = os.path.join(text_prompts, group_name, uuid + ".txt")'
assert excerpt(TA, 67, 67).strip() == 'print("Transcribing:", audio_path)'
assert excerpt(TA, 85, 85).strip() == "text = response.results[0].alternatives[0].transcript"
assert excerpt(TA, 86, 86).strip() == "print(text)"
assert excerpt(TA, 108, 108).strip().startswith('print("Uploading:"')
DOCK4 = 'ARG DEBIAN_PACKAGES="build-essential"'
assert excerpt(GB_DOCKER, 4, 4) == DOCK4
GLOB = 'glob.glob(os.path.join(text_prompts, group_name, "input-*.txt"))'
FOR = "for text_file in text_files:"
assert GLOB in excerpt(GB, 53, 53) and excerpt(GB, 54, 54).strip() == FOR
assert 'os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")' in excerpt(GB, 73, 73)
assert excerpt(GB, 80, 80).strip() == 'print("Generated text:")'
assert excerpt(SE, 23, 23) == "client = texttospeech.TextToSpeechLongAudioSynthesizeClient()"
assert excerpt(SE, 92, 92).strip() == 'print("Audio file will be saved to GCS bucket automatically.")'
assert "refresh" in excerpt(SE_README, 121, 121) and "refresh" in excerpt(SY_README, 121, 121)
assert excerpt(TT, 64, 64).strip() == 'target_language="es",'
assert excerpt(TT, 90, 90).strip().startswith('print("Uploading:"')
assert excerpt(SY, 48, 48).strip().startswith('language_code = "fr-FR"')
assert excerpt(SY, 91, 91).strip() == 'print("Audio file will be saved to GCS bucket automatically.")'
assert excerpt(SY11, 30, 30) == "secrets_file_path = 'secrets/11lab_api_key.txt'"
FIX11 = "secrets_file_path = '/secrets/11lab_api_key.txt'"

# ------------------------------------------------------------------ layout
TOP = 2.8                # top of the pictures under the tracker (tracker bottom 2.92)
BAND_Y = 3.21            # the top band, right of the tracker
ABOVE = (TOP + STRIP_TOP) / 2      # centre of the room above a 3-row strip


def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def band_x(key: str) -> float:
    """Left edge of the top band: right of the tracker of section `key` at its widest step."""
    n = len(SECTIONS[key][1])
    return max(tracker(key, k).get_right()[0] for k in range(1, n + 1)) + 0.3


def in_band(m, key: str, y: float = BAND_Y):
    return m.move_to([band_x(key) + m.width / 2, y, 0])


def swap_tracker(old, key: str, step: int = 1):
    """(new tracker, [animations]): the old tracker lifts away, the new one drops in (as
    switch_section, but played with other animations)."""
    new = tracker(key, step)
    return new, [FadeOut(old, shift=UP * 0.25), FadeIn(new, shift=DOWN * 0.25)]


def dimmed(m, k: float = 0.35) -> Transform:
    """Animation: every member of m fades to k of its own opacity (fill and stroke alike)."""
    _save_op(m, "_dop")
    target = m.copy()
    _set_op(target, k, "_dop")
    return Transform(m, target)


def quick_scroll(t, run_time: float = 0.2):
    """Montage pace: this terminal scrolls in `run_time` instead of the default 0.35 s."""
    t._make_room = lambda scene, n_new, run_time_=run_time: Terminal._make_room(t, scene, n_new, run_time_)


def _part(s: str, size: float, color: str, font: str | None = None) -> VGroup:
    """Text built after a "|" that is dropped again, so the parts of a row share a baseline."""
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


def framed(content, color: str = S.GREY, pad_x: float = 0.3, pad_y: float = 0.25,
           fill_opacity: float = 0.95, stroke: float = 2) -> VGroup:
    """A rounded GREY card around `content` (centred). .frame .content"""
    fr = box(content.width + 2 * pad_x, content.height + 2 * pad_y, color, fill=S.BG,
             fill_opacity=fill_opacity, radius=0.14, stroke=stroke)
    fr.move_to(content)
    g = VGroup(fr, content)
    g.frame, g.content = fr, content
    return g


def mixed_chip(parts, color: str = ERR, size: float = CAPTION) -> VGroup:
    """A chip (the devops look: border in its colour, faint tint) around a mixed row."""
    row = mixed(parts, size, INK)
    h = mono("|", size).height + 0.24
    b = box(row.width + 0.48, h, color, fill_opacity=0.16, radius=h / 2.6)
    b.move_to(row)
    g = VGroup(b, row)
    g.box, g.text = b, row
    return g


def note_beside(scene, t, line, text: str, color: str = S.GREY, run_time: float = 0.3):
    """A GREY 20 pt note right after a terminal line's text, pinned to it (scrolls with it)."""
    n = beside(note(text, color), t, line, buff=0.22)
    row = _row_of(line)
    assert n.get_left()[0] > row.glyphs.get_right()[0] + 0.08, (text, row.text)
    pin(scene, line, n, run_time=run_time)
    return n


def tag_beside(scene, t, line, mob, run_time: float = 0.35, buff: float = 0.3):
    """A tag beside a terminal line, pinned (asserts it fits after the line's text)."""
    beside(mob, t, line, buff=buff)
    row = _row_of(line)
    assert mob.get_left()[0] > row.glyphs.get_right()[0] + 0.08, row.text
    pin(scene, line, mob, run_time=run_time)
    return mob


def type_extra(scene, t, cmd: str, type_time: float = 0.5):
    """Type an extra command and pin its GREY `extra` tag beside it."""
    ln = type_cmd(scene, t, cmd, type_time=type_time)
    tag_beside(scene, t, ln, extra_tag(), run_time=0.25)
    return ln


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


def slim_times(t, rows):
    """Build rows' time tags one row high (stacked tags of consecutive rows would overlap)."""
    for r in rows:
        tg = getattr(r, "time_tag", None)
        if tg is not None:
            tg.box.stretch_to_fit_height(t.pitch - 0.05)


def attach(scene, line, *mobs, anims, run_time: float = 0.5):
    """Play `anims`, then make `mobs` part of terminal line `line` (they scroll with it)."""
    scene.play(*anims, run_time=run_time)
    row = _row_of(line)
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def build_rows(scene, t, rows, run_time: float = 0.6):
    new = print_build(scene, t, rows, run_time=run_time, lag=0.1)
    slim_times(t, new)
    return new


def turn_box(rows: VGroup, header: str | None, with_key: bool = True, min_w: float = 8.6) -> VGroup:
    """The static GREY "your turn" card around prebuilt rows (mobjects), header above its left
    edge, the YELLOW ▶ your turn tag on its top-right corner and the GREY note "with your key"
    left of the tag. .frame .rows .tag"""
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    w = max(rows.width + 0.6, min_w)
    fr = box(w, rows.height + 0.6, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    fr.move_to(rows).align_to(rows, LEFT).shift(LEFT * 0.3)
    g = VGroup(fr, rows)
    if header:
        h = note(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.12)
        g.add(h)
    tg = your_turn().move_to(fr.get_corner(UP + RIGHT)).shift(LEFT * 1.0)
    g.add(tg)
    if with_key:
        wk = note("with your key").next_to(tg, LEFT, buff=0.2)
        wk.shift(UP * (fr.get_top()[1] + 0.08 - wk.get_bottom()[1]))
        g.add(wk)
    g.frame, g.rows, g.tag = fr, rows, tg
    return g


def look_card(items, title: str = "with your key, look for") -> VGroup:
    """The "with your key, look for" GREY caption card (never terminal-styled): one mixed row per
    item, invisible until written in (FadeIn(card.rows[i])). .frame .rows .title"""
    rows = VGroup(*[mixed(it, CAPTION, INK) for it in items]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    ttl = label(title, CAPTION, S.GREY)
    w = max(rows.width, ttl.width) + 0.6
    fr = box(w, rows.height + ttl.height + 0.75, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    ttl.move_to(fr.get_corner(UP + LEFT) + np.array([0.3, -0.3, 0]), aligned_edge=LEFT)
    rows.next_to(ttl, DOWN, buff=0.2, aligned_edge=LEFT)
    g = VGroup(fr, ttl, rows)
    g.frame, g.rows, g.title = fr, rows, ttl
    return g


def api_door(name: str = "Text-to-Speech") -> VGroup:
    """A BLUE API door (V3's look): frame, name, knob."""
    fr = box(2.9, 0.5, CLOUD, fill_opacity=0.12, radius=0.06)
    nm = sans(name, CAPTION, INK).move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
    knob = Dot(fr.get_right() + LEFT * 0.16, radius=0.04, color=CLOUD)
    g = VGroup(fr, nm, knob)
    g.frame = fr
    return g


def waveform(color: str = CLOUD) -> VGroup:
    hs = [0.12, 0.26, 0.42, 0.22, 0.36, 0.5, 0.3, 0.16, 0.34, 0.2, 0.1]
    bars = VGroup(*[Line(DOWN * h / 2, UP * h / 2, color=color, stroke_width=4) for h in hs])
    return bars.arrange(RIGHT, buff=0.08)


def bubble(parts, color: str = S.GREY) -> VGroup:
    """A thought bubble around a mixed row, its two small circles trailing up-left (it pops
    from something above it). .frame .text"""
    t = mixed(parts, CAPTION, INK)
    b = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.4, corner_radius=0.2,
                         stroke_color=color, stroke_width=2.5).set_fill(S.BG, 0.95).move_to(t)
    c1 = Circle(radius=0.08, stroke_color=color, stroke_width=2).move_to(
        b.get_corner(UP + LEFT) + np.array([0.3, 0.18, 0]))
    c2 = Circle(radius=0.05, stroke_color=color, stroke_width=2).move_to(c1.get_center() + np.array([-0.1, 0.16, 0]))
    g = VGroup(b, t, c1, c2)
    g.frame, g.text = b, t
    return g


def title_icon(t, name: str, color: str, folder: bool = False) -> VGroup:
    """A small file (or folder) icon + name at the right end of a terminal's title bar."""
    g = folder_glyph(0.2, color) if folder else file_glyph(0.24, color)
    n = mono(name, CAPTION, color)
    ic = VGroup(g, n).arrange(RIGHT, buff=0.1)
    y = t.box.get_top()[1] - t.bar_h / 2
    return ic.move_to([t.box.get_right()[0] - 0.25 - ic.width / 2, y, 0])


def run_all_card() -> VGroup:
    """Beat 12's static card: per folder the flags typed after `python cli.py`, and what to look for
    with a key (message, the cli.py line that prints it, the bucket folder)."""
    entries = [
        (A, "--download --transcribe --upload", [("“Uploading: …”", INK)], 108, "text_prompts/group-01/"),
        (B, "--download --generate --upload", [("“Generated text:”", INK)], 80, "text_paragraphs/group-01/"),
        (C, "--download --synthesis",
         [("“Audio file will be saved to GCS bucket automatically.”", INK)], 92, "text_audios/group-01/"),
        (D, "--download --translate --upload", [("“Uploading: …”", INK), "· French after the edit"], 90,
         "text_translated/group-01/"),
        (E, "--download --synthesis", [("the same message", INK), "· the final output"], 91,
         "output_audios/group-01/"),
    ]
    cells = []
    for folder, flags, msg, ln, bucket in entries:
        a = VGroup(mono(folder, CAPTION, CTR), mono(flags, CAPTION, INK)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        b = VGroup(mixed(msg, CAPTION, S.GREY),
                   mixed([f"cli.py line {ln} ·", ("mono", bucket, S.GREY)], CAPTION, S.GREY))
        b.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        cells.append((a, b))
    ha = mixed(["in each folder:", ("mono", "python cli.py …")], CAPTION, S.GREY)
    hb = label("with your key, look for", CAPTION, S.GREY)
    wa = max(ha.width, *[a.width for a, _ in cells])
    wb = max(hb.width, *[b.width for _, b in cells])
    gap = 0.35
    x0 = 0.0
    xb = x0 + wa + gap
    y = 0.0
    mobs = VGroup()
    ha.move_to([x0, y, 0], aligned_edge=UP + LEFT)
    hb.move_to([xb, y, 0], aligned_edge=UP + LEFT)
    mobs.add(ha, hb)
    y -= max(ha.height, hb.height) + 0.14
    sep = Line([x0, y + 0.05, 0], [xb + wb, y + 0.05, 0], color=S.GREY_DARK, stroke_width=2)
    mobs.add(sep)
    y -= 0.1
    rows = []
    for a, b in cells:
        h = max(a.height, b.height)
        a.move_to([x0, y, 0], aligned_edge=UP + LEFT)
        b.move_to([xb, y, 0], aligned_edge=UP + LEFT)
        mobs.add(a, b)
        rows.append(VGroup(a, b))
        y -= h + 0.2
    foot = label("bucket looks empty? wait a moment and refresh · synthesis READMEs line 121", CAPTION, S.GREY)
    foot.move_to([x0, y - 0.02, 0], aligned_edge=UP + LEFT)
    mobs.add(foot)
    card = framed(mobs, pad_x=0.25, pad_y=0.22)
    tg = your_turn().move_to(card.frame.get_corner(UP + RIGHT)).shift(LEFT * 1.0)
    wk = note("with your key").next_to(tg, LEFT, buff=0.2)
    wk.shift(UP * (card.frame.get_top()[1] + 0.08 - wk.get_bottom()[1]))
    card.add(tg, wk)
    card.rows, card.tag = rows, tg
    return card


class RunComponents(VoiceScene):
    def construct(self):
        tr = tracker("QA", 2)

        # ========================================================== 0 · transcribe_audio --download
        t = term(rows=13, component=A)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(t), FadeIn(tr, shift=DOWN * 0.2), run_time=0.8)
            vo.wait_until("the Quick Reference")
            self.play(flash(tr.head, TURN, 1.08), run_time=0.8)
            vo.wait_until("The download step")
            dl = type_cmd(self, t, CA9.cmd, type_time=0.8)
            vo.wait_until("prints its arguments")
            t.print(self, CA9.at((2, 3)), run_time=0.5)
            vo.wait_until("then stops")
            mid = t.print(self, CA9.at("", (11, 12), ""), run_time=0.5)
            err = t.print(self, [(ERR_LINE, ERR)], wrap=True, run_time=0.5)
            self.play(mid[1].animate.set_color(TURN), run_time=0.4)
            vo.wait_until("default credentials error")
            self.play(flash(err, ERR, 1.03), run_time=0.7)
            tag_beside(self, t, err[-1], nokey_tag(), run_time=0.4)

        # ========================================================== 1 · gate 1, inside the container
        v3 = ThreeGates(show=("container", "doors", "laptop", "route"))
        mini = v3.glyph_only()
        mini.key.set_opacity(0)                      # no key on the laptop
        mini.scale(0.75)
        mini.move_to([0, 1.05, 0])
        doors = mini.parts["doors"]
        cf = mini.container_frame
        g1 = label("gate 1 · who?", CAPTION, TURN).next_to(cf, UP, buff=0.12)
        g1.set_x(max(mini.slot.get_center()[0], mini.get_left()[0] + g1.width / 2))
        wall = Line(cf.get_corner(UP + RIGHT), cf.get_corner(DOWN + RIGHT), color=ERR, stroke_width=6)
        req = Dot(mini.stamp.get_center(), radius=0.07, color=INK)
        stop_pt = np.array([cf.get_right()[0] - 0.12, mini.stamp.get_center()[1], 0])
        stop_x = cross_mark(0.26, ERR).move_to([cf.get_right()[0] + 0.25, stop_pt[1], 0])
        chips = VGroup(mixed_chip(["no key in", ("mono", "../../secrets/", INK)]),
                       mixed_chip(["another file name"]),
                       mixed_chip(["script run from another folder"]))
        chips.arrange(RIGHT, buff=0.35)
        chips.move_to([0, (mini.get_bottom()[1] + STRIP_TOP) / 2, 0])
        assert chips.get_top()[1] < mini.get_bottom()[1] - 0.1 and chips.get_bottom()[1] > STRIP_TOP + 0.1
        with self.voiceover(SAY[1]) as vo:
            resize(self, t, 3, keep=[dl, err[0], err[1]], run_time=0.7)
            self.play(FadeIn(mini), FadeIn(g1), run_time=0.6)
            self.play(Indicate(mini.route, color=TURN, scale_factor=1.0), run_time=0.6)
            self.play(flash(mini.slot, ERR, 1.25), flash(err, ERR, 1.03),
                      run_time=0.7)
            self.add(req)
            self.play(req.animate.move_to(stop_pt), run_time=0.6)
            self.play(Create(wall), FadeIn(stop_x, scale=1.4), FadeOut(req), dimmed(doors, 0.35),
                      run_time=0.5)
            vo.wait_until("no key in")
            self.play(FadeIn(chips[0], shift=UP * 0.15), flash(mini.parts["laptop"], ERR, 1.15), run_time=0.6)
            vo.wait_until("another file name")
            self.play(FadeIn(chips[1], shift=UP * 0.15), run_time=0.5)
            vo.wait_until("or the script run")
            self.play(FadeIn(chips[2], shift=UP * 0.15), run_time=0.5)

        # ========================================================== 2 · --transcribe, --upload; what to look for
        card2 = look_card([
            ["object names printed", "· cli.py line 44"],
            [("mono", "Transcribing: …", INK), ("and the transcript", INK), "· lines 67, 86"],
            [("mono", "text_prompts/group-01/input-….txt", INK), ("on your laptop", INK), "· line 62"],
            [("mono", "Uploading: …", INK), "· line 108"],
        ])
        card2.move_to([-6.35 + card2.width / 2, TOP - card2.height / 2, 0])
        for r in card2.rows:
            r.set_opacity(0)
        dr2 = drawer("text_prompts/group-01/", 4.4, CLOUD)
        dr2.move_to([6.35 - dr2.width / 2, (card2.get_bottom()[1] + STRIP_TOP) / 2 - 0.05, 0])
        ill2 = illustration_tag().next_to(dr2, UP, buff=0.12).align_to(dr2, RIGHT)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(mini, g1, wall, stop_x, chips)), tr.goto(3), run_time=0.5)
            ln = type_cmd(self, t, QA_CMDS[1], type_time=0.6)
            note_beside(self, t, ln, "same error, same reason")
            self.play(tr.goto(4), run_time=0.3)
            ln = type_cmd(self, t, QA_CMDS[2], type_time=0.5)
            note_beside(self, t, ln, "same error, same reason")
            vo.wait_until("With your key, look for")
            self.play(FadeIn(card2.frame), FadeIn(card2.title), run_time=0.4)
            card2.rows[0].set_opacity(1)
            self.play(FadeIn(card2.rows[0], shift=RIGHT * 0.15), run_time=0.4)
            vo.wait_until("the transcript")
            card2.rows[1].set_opacity(1)
            self.play(FadeIn(card2.rows[1], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("then a text file")
            card2.rows[2].set_opacity(1)
            self.play(FadeIn(card2.rows[2], shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("and in the bucket")
            card2.rows[3].set_opacity(1)
            self.play(FadeIn(card2.rows[3], shift=RIGHT * 0.15), FadeIn(dr2), FadeIn(ill2), run_time=0.5)
            self.play(flash(dr2, TURN, 1.06), run_time=0.7)

        # ========================================================== 3 · billing; the first chunk; your turn
        cost3 = cost_tag("Speech-to-Text: billed per minute of audio")
        p3 = src_panel(TA, 84, 86)
        p3.move_to([0, 0, 0]).shift(UP * (TOP - 0.7 - p3.get_top()[1]))
        cost3.move_to([6.35 - cost3.width / 2, TOP - 0.2, 0])
        r0 = p3.span(85, "results[0]")
        u3 = under(r0, ERR)
        err3 = erratum_tag("keeps only the first chunk")
        main3 = chip("main branch: joins all chunks", S.GREY, size=CAPTION)
        row3 = VGroup(err3, main3).arrange(RIGHT, buff=0.3)
        row3.move_to([p3.get_left()[0] + 0.2 + row3.width / 2, p3.get_bottom()[1] - 0.45, 0])
        turn_rows = VGroup(*[mono(c, CAPTION, INK) for c in QA_CMDS],
                           mixed(["then check", ("mono", "text_prompts/group-01/", INK), "in the bucket"],
                                 CAPTION, INK))
        tc3 = turn_box(turn_rows, "your turn · transcribe_audio")
        tc3.move_to([0, ABOVE - 0.1, 0])
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(card2, dr2, ill2)), FadeIn(cost3, shift=DOWN * 0.1), run_time=0.6)
            self.play(FadeIn(p3, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("and this branch keeps")
            self.play(Create(u3), flash(r0, ERR, 1.15), run_time=0.6)
            self.play(FadeIn(err3, shift=UP * 0.1), run_time=0.4)
            self.play(FadeIn(main3, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("use a short clip")
            self.play(flash(cost3, COST, 1.08), run_time=0.6)
            vo.wait_until("Pause and run it")
            self.play(FadeOut(VGroup(p3, u3, row3, cost3)), FadeIn(tc3.frame), FadeIn(tc3.rows),
                      FadeIn(tc3[2]), run_time=0.6)
            self.play(FadeIn(VGroup(*tc3[3:]), shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 4 · exit, cd ../generate_text, build, help
        chip52 = in_band(readme_chip("README.md · line 52", "cd into each one"), "QB")
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(tc3), run_time=0.4)
            resize(self, t, 12, run_time=0.6)
            session(self, t, C12, (38, 39), type_time=0.35, out_time=0.3)
            self.play(*leave_container(t, p_comp(A)), run_time=0.5)
            type_cmd(self, t, CD_B, type_time=0.5)
            self.play(FadeIn(chip52, shift=DOWN * 0.1), run_time=0.4)
            cd_prompt(self, t, p_comp(B), run_time=0.6)
            tr = switch_section(self, tr, "QB", 1, run_time=0.5)
            ds = type_cmd(self, t, SHELL, type_time=0.5)
            vo.wait_until("Without ffmpeg")
            rows = build_rows(self, t, B_BUILD, run_time=0.7)
            dock = excerpt_chip(DOCK4, "generate_text/Dockerfile · line 4", line=excerpt(GB_DOCKER, 4, 4))
            in_band(dock, "QB", y=(t.box.get_top()[1] + 3.45) / 2)
            assert dock.get_bottom()[1] > t.box.get_top()[1] + 0.15
            b2 = build_badge(2, words=False).move_to([t.box.get_left()[0] + 0.2, rows[1].strut.get_center()[1], 0])
            box25 = glyph_box(rows[1], "[2/5]", CTR)
            self.play(FadeOut(chip52), FadeIn(dock, shift=DOWN * 0.1), run_time=0.5)
            attach(self, rows[1], b2, box25, anims=[FadeIn(b2, scale=1.3), Create(box25), *hi_time(rows[1])],
                   run_time=0.6)
            note_beside(self, t, ds, "build-essential only · no ffmpeg")
            vo.wait_until("a fresh build")
            u52 = under(substring(rows[0], "Building 52.6s"), TURN)
            attach(self, rows[0], u52, anims=[Create(u52)], run_time=0.5)
            self.play(flash(rows[1].time_tag, TURN, 1.2), run_time=0.6)
            t.print(self, C31.at(26, 27), run_time=0.4)
            vo.wait_until("Help matches")
            self.play(*enter_container(t, B), run_time=0.5)
            session(self, t, C31, (28, 37), type_time=0.5, out_time=0.6)
            chip114 = readme_chip("generate_text/README.md · lines 114–123")
            tick = check_mark(0.3, VENV)
            same = label("identical", CAPTION, VENV)
            band4 = VGroup(chip114, tick, same).arrange(RIGHT, buff=0.2)
            in_band(band4, "QB")
            self.play(FadeOut(dock), FadeIn(chip114, shift=DOWN * 0.1), run_time=0.4)
            self.play(Create(tick), FadeIn(same), run_time=0.5)

        # ========================================================== 5 · --download fails; --generate exits 0
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(band4), tr.goto(2), run_time=0.4)
            t.clear(self)
            type_cmd(self, t, CB2.cmd, type_time=0.6)
            t.print(self, CB2.at((2, 3), "", (11, 12), ""), run_time=0.5)
            err5 = t.print(self, [(ERR_LINE, ERR)], wrap=True, run_time=0.4)
            tag_beside(self, t, err5[-1], nokey_tag(), run_time=0.3)
            vo.wait_until("The generate step")
            self.play(tr.goto(3), run_time=0.4)
            gl = type_cmd(self, t, CB3.cmd, type_time=0.6)
            vo.wait_until("prints only its arguments")
            out5 = t.print(self, CB3.at(2, 3), run_time=0.5)
            vo.wait_until("the word generate")
            self.play(flash(out5[1], TURN, 1.2), run_time=0.6)
            vo.wait_until("then exits with status 0")
            ex0 = tag_beside(self, t, out5[1], chip("exit status 0 · from the capture", S.GREY, size=CAPTION),
                             run_time=0.4)
            vo.wait_until("Did it call Gemini?")
            resize(self, t, 3, keep=[gl, out5[0], out5[1]], run_time=0.7)
        q = ponder_card("It exited with status 0.\nDid it call Gemini?")
        q.move_to([0, ABOVE, 0])
        self.play(FadeIn(q, scale=0.95), run_time=0.6)
        bar = q[3]
        self.play(bar.animate(rate_func=lambda x: x).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=6)

        # ========================================================== 6 · no: the loop had nothing to read
        gch = excerpt_chip(GLOB, "generate_text/cli.py · line 53 (excerpt)", line=excerpt(GB, 53, 53))
        fch = excerpt_chip(FOR, "generate_text/cli.py · line 54", line=excerpt(GB, 54, 54))
        gch.move_to([-6.35 + gch.width / 2, TOP - gch.height / 2, 0])
        gsub = gch.text[:9]                               # "glob.glob"
        bub = bubble([("mono", "[ ]", INK), ("· no files", INK)])
        bub.move_to([gsub.get_left()[0] + bub.width / 2 - 0.05, gch.get_bottom()[1] - 0.35 - bub.height / 2, 0])
        fch.move_to([-6.35 + fch.width / 2, bub.get_bottom()[1] - 0.3 - fch.height / 2, 0])
        assert fch.get_bottom()[1] > STRIP_TOP + 0.3
        zero = label("0 rounds", CAPTION + 2, ERR).next_to(fch.chip, RIGHT, buff=0.35)
        dr6 = drawer("text_prompts/group-01/", 4.4, LAPTOP)
        lap6 = note("on your laptop · empty")
        grp6 = VGroup(dr6, lap6).arrange(RIGHT, buff=0.25)
        grp6.move_to([6.35 - grp6.width / 2, bub.get_center()[1], 0])
        assert grp6.get_left()[0] > bub.get_right()[0] + 0.4
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(q), run_time=0.3)
            self.play(FadeIn(gch, shift=DOWN * 0.1), FadeIn(fch, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("The download had failed")
            self.play(FadeIn(grp6, shift=LEFT * 0.1), run_time=0.5)
            self.play(gsub.animate.set_color(TURN), run_time=0.3)
            self.play(flash(gsub, TURN, 1.15), run_time=0.6)
            self.play(FadeIn(bub, scale=0.6), run_time=0.5)
            vo.wait_until("so the loop had no prompts")
            self.play(fch.animate.set_opacity(0.35), FadeIn(zero, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("Exit status 0")
            self.play(flash(ex0, TURN, 1.1), run_time=0.8)

        # ========================================================== 7 · --upload; another model
        rm91 = readme_chip("generate_text/README.md · lines 91–94")
        p7 = src_panel(GB, 73, 77, size=20)
        TOP5 = strip_top(5)
        p7.move_to([0, 0, 0]).shift(UP * (TOP - 0.15 - p7.get_top()[1]))
        bar73 = p7.bar(73, TURN)
        env = p7.span(73, 'os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")')
        dflt = p7.span(73, '"gemini-2.5-flash-lite"')
        u_d = under(dflt, S.GREY)
        t_d = grey_tag("default")
        cost7 = cost_tag("Gemini: billed per token")
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(gch, fch, bub, zero, grp6)), tr.goto(4), run_time=0.5)
            resize(self, t, 5, run_time=0.5)
            up7 = type_cmd(self, t, QB_CMDS[2], type_time=0.5)
            note_beside(self, t, up7, "needs the key")
            vo.wait_until("The generate text README")
            in_band(rm91, "QB")
            self.play(tr.goto(5), FadeIn(rm91, shift=DOWN * 0.1), run_time=0.5)
            type_cmd(self, t, CB5.cmd, type_time=0.6)
            type_cmd(self, t, CB5.line(2), type_time=0.5)
            t.print(self, CB5.at(3, 4), run_time=0.4)
            assert p7.get_bottom()[1] > TOP5 + 0.1, (p7.get_bottom()[1], TOP5)
            vo.wait_until("a variable picks")
            self.play(FadeIn(p7, shift=DOWN * 0.1), run_time=0.5)
            box_env = ring(env, TURN, buff=0.05)
            self.play(FadeIn(bar73), Create(box_env), run_time=0.6)
            t_d.next_to(u_d, DOWN, buff=0.12).align_to(u_d, RIGHT)
            self.play(Create(u_d), FadeIn(t_d, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Gemini bills per token")
            cost7.move_to([p7.get_right()[0] - cost7.width / 2, p7.header.get_center()[1], 0])
            self.play(FadeIn(cost7, shift=DOWN * 0.1), run_time=0.5)

        # ========================================================== 8 · synthesis_audio_en: cached; the assert
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(p7, bar73, box_env, u_d, t_d, cost7, rm91)), run_time=0.4)
            tr = switch_section(self, tr, "QC", 1, run_time=0.5)
            resize(self, t, 13, run_time=0.5)
            session(self, t, C31, (38, 39), type_time=0.3, out_time=0.3)
            self.play(*leave_container(t, p_comp(B)), run_time=0.4)
            type_cmd(self, t, CD_C, type_time=0.5)
            cd_prompt(self, t, p_comp(C), run_time=0.5)
            type_cmd(self, t, SHELL, type_time=0.4)
            rows8 = build_rows(self, t, C_BUILD, run_time=0.6)
            vo.wait_until("builds in 8 seconds")
            u82 = under(substring(rows8[0], "Building 8.2s"), TURN)
            attach(self, rows8[0], u82, anims=[Create(u82)], run_time=0.4)
            vo.wait_until("its system layer cached")
            bx = glyph_box(rows8[1], "CACHED [2/5]", VENV)
            same8 = tag("same as generate_text", VENV)
            beside(same8, t, rows8[2], buff=0.4)
            assert same8.get_left()[0] > rows8[2].glyphs.get_right()[0] + 0.1
            assert same8.get_right()[0] < rows8[2].time_tag.get_left()[0] - 0.1
            attach(self, rows8[1], bx, anims=[Create(bx)], run_time=0.4)
            attach(self, rows8[2], same8, anims=[FadeIn(same8, shift=LEFT * 0.1)], run_time=0.4)
            t.print(self, C40.at(26, 27), run_time=0.3)
            vo.wait_until("We left its cli.py")
            self.play(*enter_container(t, C), run_time=0.4)
            out8 = session(self, t, C40, (28, 33), type_time=0.5, out_time=0.6, colors={33: ERR})
            vo.wait_until("help stops at the assert")
            tag_beside(self, t, out8[33], grey_tag("cli.py left unedited on purpose"), run_time=0.4)
            vo.wait_until("here, the guard works")
            self.play(flash(out8[31], VENV, 1.06), run_time=0.8)

        # ========================================================== 9 · edit on the laptop; help needs the key
        t2 = term(P_HOME, rows=5, title="laptop · second terminal", top=2.75)
        with self.voiceover(SAY[9]) as vo:
            self.play(caption_extra(tr, True), run_time=0.3)
            resize(self, t, 6, run_time=0.5, extra=[FadeIn(t2, shift=DOWN * 0.3)])
            assert t2.box.get_bottom()[1] > t.box.get_top()[1] + 0.05
            ln = bare_prompt(self, t2)
            tilde = glyph_range(ln, P_HOME.index("~"), P_HOME.index("~") + 1)
            cap = beside(note("new terminal: cd here first"), t2, ln, buff=0.5)
            self.play(Indicate(tilde, color=TURN, scale_factor=1.4), FadeIn(cap), run_time=0.6)
            self.wait(0.2)
            _drop_bare(self, t2)
            t2.set_prompt(p_comp(C))
            ln2 = bare_prompt(self, t2)
            ic_lap = title_icon(t2, "cli.py", LAPTOP)
            ic_ctr = title_icon(t, "/app/cli.py", CTR, folder=True)
            pen = pencil(0.45).next_to(ic_lap, LEFT, buff=0.15)
            ed = note("in your editor").next_to(pen, LEFT, buff=0.15)
            self.play(FadeOut(cap), Indicate(glyph_range(ln2, p_comp(C).index(":") + 1, len(p_comp(C)) - 1),
                                             color=TURN, scale_factor=1.05),
                      FadeIn(ic_lap), FadeIn(ic_ctr), run_time=0.5)
            self.play(FadeIn(pen, shift=DOWN * 0.15), FadeIn(ed), run_time=0.4)
            self.play(Wiggle(pen, scale_value=1.15, rotation_angle=0.08), run_time=0.6)
            vo.wait_until("the window shows it at once")
            self.play(flash(ic_lap, TURN, 1.3), flash(ic_ctr, TURN, 1.3), run_time=0.7)
            self.play(FadeOut(VGroup(pen, ed)), run_time=0.3)
            type_extra(self, t2, C41.cmd, type_time=0.5)
            diff = t2.print(self, [(C41.line(16), S.GREY), (C41.line(17), INK)], run_time=0.4)
            self.play(flash(substring(diff[1], '"group-01"'), TURN, 1.15), run_time=0.5)
            vo.wait_until("Now help fails")
            self.play(caption_extra(tr, False), run_time=0.3)
            resize(self, t, 10, run_time=0.6, extra=[FadeOut(VGroup(t2, ic_lap, ic_ctr))])
            hl = type_cmd(self, t, CC2.cmd, type_time=0.5)
            o9 = t.print(self, CC2.at((2, 4), "") + [(ERR_LINE, ERR)], wrap=True, run_time=0.6)
            l3 = o9[1]
            assert "line 23" in l3.text
            self.play(l3.animate.set_color(TURN), run_time=0.4)
            vo.wait_until("which builds the Google client")
            p23 = src_panel(SE, 23, 23, size=20)
            p23.move_to([-6.35 + p23.width / 2, 0, 0]).shift(UP * (TOP - p23.get_top()[1]))
            assert p23.get_bottom()[1] > t.box.get_top()[1] + 0.05
            imp = grey_tag("runs on import").next_to(p23.header, RIGHT, buff=0.4)
            imp.set_y(p23.header.get_center()[1])
            self.play(FadeIn(p23, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(imp, shift=LEFT * 0.1), flash(p23.code, TURN, 1.03), run_time=0.5)
            vo.wait_until("even help needs the key")
            self.play(flash(VGroup(*o9[-2:]), ERR, 1.03), run_time=0.7)

        # ========================================================== 10 · the README's help; no upload step
        exp = log_panel(EXP.at((3, 10)), "with your key · synthesis_audio_en/README.md · lines 99–107", width=11.0)
        exp.move_to([-6.35 + exp.width / 2, 0, 0]).shift(UP * (TOP - 0.1 - exp.get_top()[1]))
        etag = expected_tag().next_to(exp.frame, RIGHT, buff=0.15).align_to(exp.frame, UP)
        if etag.get_right()[0] > 6.4:
            etag.move_to(exp.frame.get_corner(UP + RIGHT) + np.array([-etag.width / 2 - 0.15, -0.3, 0]))
        door = api_door()
        dr10 = drawer("text_audios/group-01/", 5.4, CLOUD)
        door.move_to([-3.6, 0.8, 0])
        dr10.move_to([6.35 - dr10.width / 2, 0.8, 0])
        wave = waveform().next_to(door, RIGHT, buff=0.2)
        cap10 = mixed(["empty at first? wait a moment and refresh ·", ("mono", "synthesis_audio_en/README.md"), "line 121"])
        cap10.move_to([0, -0.3, 0])
        ill10 = illustration_tag().next_to(dr10, UP, buff=0.15).align_to(dr10, RIGHT)
        cost10 = cost_tag("Text-to-Speech: billed per character").next_to(door, UP, buff=0.3).align_to(door, LEFT)
        with self.voiceover(SAY[10]) as vo:
            self.play(FadeOut(VGroup(p23, imp)), run_time=0.3)
            resize(self, t, 3, keep=[hl, o9[-2], o9[-1]], run_time=0.6)
            self.play(FadeIn(exp, shift=DOWN * 0.1), FadeIn(etag), run_time=0.5)
            self.play(tr.goto(2), run_time=0.3)
            ln = type_cmd(self, t, QC_CMDS[0], type_time=0.4)
            note_beside(self, t, ln, "needs the key", run_time=0.25)
            self.play(tr.goto(3), run_time=0.3)
            ln = type_cmd(self, t, QC_CMDS[1], type_time=0.4)
            note_beside(self, t, ln, "needs the key", run_time=0.25)
            vo.wait_until("There's no upload step")
            r257 = in_band(readme_chip("README.md · line 257", "no separate --upload step"), "QC")
            self.play(FadeOut(VGroup(exp, etag)), FadeIn(r257, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(door), FadeIn(dr10), FadeIn(ill10), run_time=0.5)
            vo.wait_until("writes the audio straight")
            self.play(FadeIn(wave, scale=0.5), flash(door, CLOUD, 1.05), run_time=0.5)
            self.play(dr10_receive(wave, dr10), run_time=0.9)
            self.play(flash(dr10, TURN, 1.06), FadeIn(cost10, shift=DOWN * 0.1), FadeIn(cap10), run_time=0.7)

        # ========================================================== 11 · montage: translate_text
        with self.voiceover(SAY[11]) as vo:
            tr, swap = swap_tracker(tr, "QD", 1)
            self.play(FadeOut(VGroup(door, dr10, wave, ill10, cost10, cap10, r257)), *swap, run_time=0.4)
            resize(self, t, 12, run_time=0.45)
            quick_scroll(t, 0.15)
            session(self, t, C40, (34, 35), type_time=0.25, out_time=0.2)
            self.play(*leave_container(t, p_comp(C)), run_time=0.25)
            type_cmd(self, t, CD_D, type_time=0.3)
            cd_prompt(self, t, p_comp(D), run_time=0.35)
            type_cmd(self, t, SHELL, type_time=0.3)
            rows11 = build_rows(self, t, C51.at(4, 14), run_time=0.3)
            self.play(substring(rows11[1], "CACHED").animate.set_color(VENV), *enter_container(t, D), run_time=0.3)
            session(self, t, C51, (28, 31), "", type_time=0.3, out_time=0.3)
            t.print(self, [(C51.join(64, 65), ERR)], wrap=True, run_time=0.25)
            for k, cmd in enumerate(QD_CMDS, start=2):
                self.play(tr.goto(k), run_time=0.2)
                ln = type_cmd(self, t, cmd, type_time=0.25)
                note_beside(self, t, ln, "needs the key", run_time=0.15)

        # ========================================================== 12 · montage: synthesis_audio; run all five
        card12 = run_all_card()
        card12.move_to([0, (TOP + BOTTOM) / 2 - 0.05, 0])
        with self.voiceover(SAY[12]) as vo:
            tr, swap = swap_tracker(tr, "QE", 1)
            self.play(*swap, run_time=0.3)
            session(self, t, C51, (66, 67), type_time=0.25, out_time=0.2)
            self.play(*leave_container(t, p_comp(D)), run_time=0.25)
            type_cmd(self, t, CD_E, type_time=0.3)
            cd_prompt(self, t, p_comp(E), run_time=0.35)
            type_cmd(self, t, SHELL, type_time=0.25)
            rows12 = build_rows(self, t, C61.at(4, 14), run_time=0.3)
            self.play(substring(rows12[1], "CACHED").animate.set_color(VENV), *enter_container(t, E), run_time=0.3)
            session(self, t, C61, (28, 31), "", type_time=0.25, out_time=0.3)
            t.print(self, [(C61.join(93, 94), ERR)], wrap=True, run_time=0.25)
            for k, cmd in enumerate(QE_CMDS, start=2):
                self.play(tr.goto(k), run_time=0.2)
                ln = type_cmd(self, t, cmd, type_time=0.25)
                note_beside(self, t, ln, "needs the key", run_time=0.15)
            vo.wait_until("Pause, and run all five")
            self.add(t)
            self.play(FadeOut(t), FadeIn(card12), run_time=0.7)
            self.play(flash(card12.tag, TURN, 1.15), run_time=0.7)
        self.wait(1.5)                    # the your-turn card stays up

        # ========================================================== 13 · two small slips
        p64 = src_panel(TT, 64, 64)
        p48 = src_panel(SY, 48, 49, cut_comments=True)
        es = p64.span(64, '"es"')
        fr = VGroup(p48.span(48, '"fr-FR"'), p48.span(49, '"fr-FR'))
        fix1 = fix_chip('target_language="fr"', font=MONO)
        why1 = grey_tag("you set it in Before you run, step 2")
        fx1 = VGroup(fix1, why1).arrange(RIGHT, buff=0.3)
        body1 = VGroup(p64, p48, fx1).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        card1 = framed(body1, pad_x=0.35, pad_y=0.3)
        card1.move_to([0, (TOP + BOTTOM) / 2 + 0.2, 0])
        et1 = erratum_tag().move_to(card1.frame.get_corner(UP + RIGHT)).shift(LEFT * 0.9)
        u_es = under(es, ERR)
        cap2 = mixed(["optional ElevenLabs bonus:", ("mono", "cli_11.py", INK), "looks for its key file inside",
                      ("mono", "/app", INK)], CAPTION, S.GREY)
        fix2 = fix_chip(FIX11, font=MONO)
        h2 = _header_text("synthesis_audio/cli_11.py · line 30")
        fx2 = VGroup(h2, fix2).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        body2 = VGroup(cap2, fx2).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        card2b = framed(body2, pad_x=0.35, pad_y=0.3)
        card2b.move_to([0, (TOP + BOTTOM) / 2 + 0.2, 0])
        et2 = erratum_tag().move_to(card2b.frame.get_corner(UP + RIGHT)).shift(LEFT * 0.9)
        with self.voiceover(SAY[13]) as vo:
            self.play(FadeOut(card12), run_time=0.5)
            self.play(FadeIn(card1.frame), FadeIn(et1), run_time=0.4)
            vo.wait_until("The translation targeted Spanish")
            self.play(FadeIn(p64, shift=DOWN * 0.1), run_time=0.5)
            self.play(es.animate.set_color(ERR), Create(u_es), run_time=0.5)
            vo.wait_until("but the final voice is French")
            self.play(FadeIn(p48, shift=DOWN * 0.1), run_time=0.5)
            u_fr = VGroup(*[under(m, CLOUD) for m in fr])
            self.play(*[m.animate.set_color(CLOUD) for m in fr], Create(u_fr), run_time=0.6)
            vo.wait_until("that's why you switched it")
            self.play(FadeIn(fix1, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(why1, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("And the optional ElevenLabs bonus")
            self.play(FadeOut(VGroup(card1, et1, u_es, u_fr)), run_time=0.5)
            self.play(FadeIn(card2b.frame), FadeIn(et2), FadeIn(cap2, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("point it at slash secrets")
            self.play(FadeIn(fx2, shift=UP * 0.1), run_time=0.6)
            self.play(flash(substring_text(fix2.text, FIX11, "/secrets/"), VENV, 1.15), run_time=0.7)
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)


def dr10_receive(mob, dr):
    """Animation: the waveform slides into the drawer (ends on its handle side)."""
    return mob.animate.scale(0.55).move_to(dr.frame.get_right() + LEFT * 0.95)


def substring_text(text_mob, s: str, sub: str):
    """Glyphs of `sub` in a Text built from string `s` (no spaces counted as glyphs)."""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*text_mob.submobjects[a:a + n])
