r"""S10 · Transcribe and upload (README › transcribe_audio steps 11–12; V8 Speech-to-Text half,
V3, V1 small, the schematic leaderboard).

Nothing here talks to Google (no key was available): the two commands are typed, never run, and
every "what you should see" is a "with your key, look for" card citing the cli.py line that
prints it (ASSETS.md, "what could not be captured").

Beats (script.md "## S10", one voiceover block each):
 0  TRACKER A11. V8 low in the frame: a TEAL container "A · transcribe_audio" (widened so the
    ffmpeg step fits inside) holding a GREY `input-….mp3` page; a BLUE cloud "Speech-to-Text" on
    the right. CODE(transcribe_audio/cli.py: 67–69) top-left. On "ffmpeg first converts" an
    ORANGE funnel "ffmpeg" appears; a copy of the MP3 page drops into it (line 67 bar), a FLAC
    block comes out of the spout (line 68), the funnel pulses (line 69, ffmpeg.run). On "and
    that's why" the student's Dockerfile line 3 (`transcribe_audio/Dockerfile · line 3`, caption
    "from transcribe_audio/README.md · lines 41–90") appears under the code; `ffmpeg` underlines
    ORANGE.
 1  The panels swap to CODE(75–78) at 20 pt; the MP3 page and the funnel leave. Line 75: an INK
    request arrow grows to the cloud and the FLAC block rides inside it; GOLD "billed to the
    course project" above the arrow. Line 77: a TEAL ticket stub "operation" comes back at once
    (pulses on "like a ticket stub"). Line 78: the ring beside it fills, "up to 90 s". On "for
    the transcript" a transcript page travels back into the container; stub and ring fade.
 2  The panel swaps to CODE(84–91). The page splits into three short strips (the pieces);
    lines 86–88 bar and the strips pulse one by one; line 90 bars and the strips snap into one
    page; a GREY tag "the latest commit's fix" beside line 90.
 3  The panel and V8 go; the GOLD tag moves onto the strip's top-right corner. Terminal strip
    (TEAL, `container · transcribe_audio`; 2 rows, as S11 opens on it, so beat 4's window
    fits). A GREY README card above it, header `README.md · line 135`, the README's
    `python cli.py --transcribe` + tag "same as -t"; it types the command (no output). On "Look for" the README card gives way to the "with your key, look
    for" card: items write on their words (lines 64, 69, 79, 91); the RED-bordered "if it
    fails" line writes on "If it says no such file" and pulses on "add ffmpeg to line 3"; the
    tracker's step-13 dot pulses on "exit and rebuild".
 4  The card's line-95 item writes ("Then open the new text file"); the card and the GOLD tag
    go. V3 + V4 as S08 left them and S11 opens on them (mounted; the laptop folder holds cli.py,
    Dockerfile, pyproject.toml and uv.lock GREEN, secrets/ with the GOLD key, input_audios/,
    text_prompts/; the dashed "writable layer · throwaway" with 26 GREEN chips on its shelf),
    0.25 right of centre above the strip, with tag `illustration · with your key` top right: a
    page lands on the `text_prompts/` folder on the laptop and on the sheet over /app at the same
    instant, the PINK route pulses in width; the laptop's page opens into a page headed
    `text_prompts/group-01/input-….txt`, its text gray bars only, while V3 and its tag leave.
    "If it says None": that page dims, the tag comes back bottom left, and a copy of the page
    becomes a RED-bordered page reading `None` (the same file's other outcome); "Speech-to-Text
    returned nothing": CODE(cli.py: 80) above it with a GREY pointer from `None` up to `"None"`; "delete
    it…": the None page is struck, GREY note "delete it, transcribe again"; "because finished
    files are skipped": GREY note "files already done are skipped (cli.py lines 61–62): delete
    one to redo it".
 5  TRACKER A12. The picture goes, the GOLD tag returns; the strip clears. GREY README card
    `README.md · line 136`, `python cli.py --upload` + "same as -u"; it types the command. "It uploads only files
    starting with input": the card gives way to the line-108 excerpt chip of S02, `"input-*.txt"`
    turns PINK and underlines; "under the same name": CODE(111–115) at 20 pt, line 112 PINK bar.
    "look for": the chip goes, the panel rises, and a "with your key, look for" card: "Uploading:
    text_prompts/group-01/input-….txt …" (line 114); the prefix, the group and the file turn
    PINK on their words; a thin GREY line joins the item's "line 114" to that line of the panel.
 6  The strip and the panels go; the GOLD tag moves to the right. V1 small (letters only)
    top-left: a transcript page appears in A and drops into the second drawer, labelled PINK
    `text_prompts/group-01/`. The schematic leaderboard (tag illustration) lights the
    group-01 × Transcribe cell; caption "check: ac215-mega-pipeline.dlops.io" over
    "(transcribe_audio/README.md · line 134)". On
    "Pause": a static GREY card `README.md · lines 134–136` listing the three commands, ▶ your
    turn under it (the GOLD tag beside).
 7  TRACKER A12 · extra. The picture goes; on "the flags combine" the three-command card
    collapses into a chip `python cli.py -d -t -u` (extra; shown, not typed); three elbow arrows from -d, -t, -u to download(), transcribe(), upload() in
    CODE(121–126) as each flag is said; on "in order" the three call lines bar in sequence. The
    GOLD tag moves under the chip and pulses on "Each call is billed". Everything fades: empty
    frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import PANEL, box, code_span, label, line_bar, mono, mono_line, substring, tag
from explainer.scene import VoiceScene

from common import (CLOUD, CTR, ERR, GROUP, INK, LOOKUP, NARRATION, P_CTR, SYSTEM, TURN, VENV,
                    ApiCall, Leaderboard, LookFor, Relay, Window, asset_lines, caption_extra, cost_tag,
                    excerpt, extra_tag, file_panel, illustration_tag, page_token, pkg_dots, sans, source_text,
                    src_panel, strip_top, term, tracker, type_cmd, under, your_turn)

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ sources (checked, never typed by hand)
CLI = "transcribe_audio/cli.py"
DF = "files/transcribe_audio.Dockerfile"


def _src(n: int) -> str:
    return excerpt(CLI, n, n).strip()


assert [_src(n) for n in (67, 68, 69)] == ["stream = ffmpeg.input(audio_path)",
                                           "stream = ffmpeg.output(stream, flac_path)",
                                           "ffmpeg.run(stream)"]
assert _src(64) == 'print("Transcribing:", audio_path)'
assert _src(75) == "audio = speech.RecognitionAudio(content=content)"
assert _src(77) == "operation = client.long_running_recognize(config=config, audio=audio)"
assert _src(78) == "response = operation.result(timeout=90)"
assert _src(79) == 'print("response:", response)'
assert _src(80) == 'text = "None"'
assert _src(86) == "for result in response.results:"
assert _src(88) == "transcripts.append(result.alternatives[0].transcript)"
assert _src(90) == 'text = "".join(transcripts)'
assert _src(91) == "print(text)"
assert _src(61) == "if os.path.exists(text_file):" and _src(62) == "continue"
assert _src(95) == 'with open(text_file, "w") as f:'
GLOB_LINE = 108
GLOB = 'glob.glob(os.path.join(text_prompts, group_name, "input-*.txt"))'
assert GLOB in excerpt(CLI, GLOB_LINE, GLOB_LINE)
assert _src(112) == "destination_blob_name = os.path.join(text_prompts, group_name, filename)"
assert _src(114) == 'print("Uploading:",destination_blob_name, text_file)'
assert [_src(n) for n in (122, 124, 126)] == ["download()", "transcribe()", "upload()"]
assert asset_lines(DF, 3, 3) == 'ARG DEBIAN_PACKAGES="build-essential ffmpeg"'

_R = source_text("README.md").split("\n")
README_CMDS = _R[133:136]                         # README.md lines 134-136 (Quick Reference)
assert README_CMDS == ["python cli.py --download", "python cli.py --transcribe",
                       "python cli.py --upload"], README_CMDS
T_CMD, U_CMD = README_CMDS[1], README_CMDS[2]
_RA = source_text("transcribe_audio/README.md").split("\n")
assert "`python cli.py -t`" in _RA[131] and "`python cli.py -u`" in _RA[132]
assert "Verify that your uploaded data shows up" in _RA[133]      # line 134: the check
LB_URL = "ac215-mega-pipeline.dlops.io"
assert LB_URL in _RA[133], _RA[133]                                  # ... and its address

COMBO = "python cli.py -d -t -u"                  # extra: shown, not typed

# "with your key, look for" (the cli.py line that prints each)
LOOK_T = [("Transcribing: input_audios/…", "line 64"), ("ffmpeg's log", "line 69"),
          ("response: …", "line 79"), ("the transcript", "line 91"),
          (f"a new text_prompts/{GROUP}/input-….txt on your laptop", "line 95")]
FAIL_T = "if it fails: FileNotFoundError … 'ffmpeg' → Dockerfile line 3 lacks ffmpeg: fix, exit, rebuild"
LOOK_U = [(f"Uploading: text_prompts/{GROUP}/input-….txt …", "line 114")]
TXT_PATH = f"text_prompts/{GROUP}/input-….txt"

# ------------------------------------------------------------------ layout
TOP = 2.78                       # top of a panel under the tracker band (y 2.92..3.5)
EDGE = 6.3
CTR_L, CTR_W = -6.35, 4.7        # V8's container, widened so the ffmpeg step fits inside
V8_DY = -2.9                     # ApiCall's container centre y 0.6 -> -2.3
STRIP = 2                        # the container strip of beats 3-5: 2 rows, as S11 opens on it,
ST = strip_top(STRIP)            # so the 7-row window of beat 4 fits between it and the tracker
WIN_DX = 0.25                    # the window sits 0.25 right (as in S11): its writable layer clears the tracker

# V3 + V4 as S08 left them and S11 opens on them (s11_rebuild.py WIN_FILES / WIN_COPIED)
WIN_FILES = ("cli.py", "Dockerfile", ("pyproject.toml", VENV), "secrets/", ("uv.lock", VENV), "input_audios/",
             "text_prompts/")
WIN_COPIED = ("cli.py", "Dockerfile", "pyproject.toml", "secrets/")      # what the step-5 image copied


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


def tglyphs(t, sub: str, occ: int = 0) -> VGroup:
    """The glyphs of `sub` in a Text (spaces have no glyph); fails on a ligature (ff, fi…)."""
    src = t.original_text
    flat = "".join(src.split())
    assert len(flat) == len(t.submobjects), f"ligature in {src!r}: index by glyph is unsafe"
    key = "".join(sub.split())
    i = -1
    for _ in range(occ + 1):
        i = flat.find(key, i + 1)
    assert i >= 0, (sub, src)
    return VGroup(*t.submobjects[i:i + len(key)])


def lines_bar(code, a: int, b: int, color=TURN, opacity: float = 0.16) -> Rectangle:
    """A translucent bar over lines a..b (0-based) of a code_block."""
    top = line_bar(code, a, color, opacity)
    bot = line_bar(code, b, color, opacity)
    h = top.get_top()[1] - bot.get_bottom()[1]
    return Rectangle(width=top.width, height=h, stroke_width=0).set_fill(color, opacity) \
        .move_to([top.get_center()[0], (top.get_top()[1] + bot.get_bottom()[1]) / 2, 0])


def seed_prompt(t):
    """A bare prompt on terminal t, without animation (the terminal fades in with it)."""
    ln = mono_line(t.prompt + " ", t.size, INK, t2c=t._prompt_colors(t.prompt))
    t._place(ln, len(t.lines))
    t.lines.add(ln)
    ln.bare = True
    return ln


def funnel(w: float = 0.86, h: float = 0.74) -> VGroup:
    """ffmpeg (an apt package of the base image: ORANGE): a funnel with a spout. .mouth .spout"""
    n = 0.09
    cone = Polygon([-w / 2, h / 2, 0], [w / 2, h / 2, 0], [n, -h * 0.12, 0], [n, -h / 2, 0],
                   [-n, -h / 2, 0], [-n, -h * 0.12, 0], stroke_color=SYSTEM, stroke_width=3)
    cone.set_fill(SYSTEM, 0.18)
    g = VGroup(cone)
    g.mouth = lambda: cone.get_top() + DOWN * 0.08
    g.spout = lambda: cone.get_bottom()
    return g


def flac_block() -> VGroup:
    fr = RoundedRectangle(width=1.0, height=0.48, corner_radius=0.08, stroke_color=INK,
                          stroke_width=2.5).set_fill(INK, 0.1)
    t = mono("FLAC", 20, INK).move_to(fr)
    return VGroup(fr, t)


def slip(frac: float) -> VGroup:
    """One piece of a transcript: a short strip with one text bar."""
    fr = RoundedRectangle(width=1.4, height=0.32, corner_radius=0.06, stroke_color=INK,
                          stroke_width=2).set_fill(INK, 0.06)
    bar = Line(ORIGIN, RIGHT * 1.0 * frac, color=INK, stroke_width=2)
    bar.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.2)
    return VGroup(fr, bar)


def readme_cmd_card(line_no: int, cmd: str, short: str) -> VGroup:
    """README.md's own line (mono) in a GREY card headed `README.md · line n`, with a GREY tag
    naming the component README's short form. .frame .code .same .header"""
    code = mono_line(cmd, 20, INK)
    same = tag(f"same as {short}", S.GREY)
    row = VGroup(code, same).arrange(RIGHT, buff=0.35)
    fr = box(row.width + 0.5, row.height + 0.26, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.12)
    row.move_to(fr)
    head = VGroup(mono("README.md", 20, S.GREY), label(f"· line {line_no}", 20, S.GREY))
    head.arrange(RIGHT, buff=0.12)
    head.next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
    g = VGroup(fr, row, head)
    g.frame, g.code, g.same, g.header = fr, code, same, head
    return g


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


def excerpt_chip(path: str, n: int, expr: str) -> VGroup:
    """S02's excerpt chip: the exact sub-expression of `path` line n (mono 20) in a code-panel
    styled chip, headed "path · line n (excerpt)". .frame .code .header"""
    assert expr in excerpt(path, n, n), (path, n, expr)
    code = mono_line(expr, 20, INK)
    fr = RoundedRectangle(width=code.width + 0.5, height=code.strut.height + 0.3, corner_radius=0.12,
                          stroke_color=S.GREY_DARK, stroke_width=2).set_fill(PANEL, 1)
    code.move_to(fr)
    head = VGroup(mono(path, 20, S.GREY), label(f"· line {n} (excerpt)", 20, S.GREY))
    head.arrange(RIGHT, buff=0.14)
    head.next_to(fr, UP, buff=0.1).align_to(fr, LEFT).shift(RIGHT * 0.12)
    g = VGroup(fr, code, head)
    g.frame, g.code, g.header = fr, code, head
    return g


def readme_caption() -> VGroup:
    """'from transcribe_audio/README.md · lines 41–90' (the Dockerfile the README has you write),
    on three short rows."""
    rows = VGroup(label("from", 20, S.GREY), mono("transcribe_audio/README.md", 20, S.GREY),
                  label("lines 41–90", 20, S.GREY)).arrange(DOWN, aligned_edge=RIGHT, buff=0.08)
    return rows


def opened_page(w: float = 5.0, h: float = 1.9) -> VGroup:
    """The transcript file opened on the laptop: GREY page, its text as gray bars only (the real
    transcript is not known), header = the path. .frame .bars .header"""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=S.GREY,
                          stroke_width=2.5).set_fill(S.GREY, 0.06)
    bars = VGroup(*[Line(ORIGIN, RIGHT * (w - 0.8) * f, color=S.GREY, stroke_width=7)
                    for f in (0.92, 0.78, 0.96, 0.58)]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    bars.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.4)
    head = mono(TXT_PATH, 20, S.GREY).next_to(fr, UP, buff=0.1).align_to(fr, LEFT)
    g = VGroup(fr, bars, head)
    g.frame, g.bars, g.header = fr, bars, head
    return g


def dim_page(op, k: float) -> list:
    """Animations: the opened page fades to k of its look (its fill stays faint)."""
    return [op.frame.animate.set_stroke(opacity=k).set_fill(opacity=0.06 * k),
            op.bars.animate.set_stroke(opacity=k), op.header.animate.set_fill(opacity=k)]


def none_page(w: float = 2.5, h: float = 1.05) -> VGroup:
    """The same file when Speech-to-Text returned nothing: a RED-bordered page reading None."""
    fr = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=ERR,
                          stroke_width=3).set_fill(ERR, 0.06)
    t = mono("None", 24, INK)
    t.move_to(fr.get_corner(UL) + np.array([0.3 + t.width / 2, -0.36, 0]))
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def elbow(p0, p1, p2, color=INK) -> VGroup:
    """An elbow arrow p0 -> p1 -> p2 (a line, then an arrow)."""
    a = Line(p0, p1, color=color, stroke_width=3)
    n = float(np.linalg.norm(np.array(p2) - np.array(p1)))
    b = Arrow(p1, p2, buff=0, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.2 / n,
              max_stroke_width_to_length_ratio=20)
    return VGroup(a, b)


# ------------------------------------------------------------------ the scene
class TranscribeUpload(VoiceScene):
    def construct(self):
        assert len(SAY) == 8, f"S10 has {len(SAY)} SAY lines; this scene times 8"

        tr = tracker("A", 10)

        # ========================================================== 0 · step 11: ffmpeg MP3 -> FLAC
        api = ApiCall("Speech-to-Text", "A · transcribe_audio")
        api.shift(UP * V8_DY)
        cy = api.ctr.frame.get_center()[1]
        api.ctr.frame.become(box(CTR_W, 2.0, CTR, fill_opacity=0.06).move_to([CTR_L + CTR_W / 2, cy, 0]))
        api.ctr.title.next_to(api.ctr.frame, UP, buff=0.12)
        api.link.put_start_and_end_on(api.ctr.frame.get_right() + RIGHT * 0.1,
                                      api.api.shape.get_left() + LEFT * 0.1)
        cloud_c = api.api.shape.get_center()

        mp3 = page_token(color=S.GREY).scale(1.25)
        mp3_lab = mono("input-….mp3", 20, S.GREY)
        mp3_g = VGroup(mp3, mp3_lab.next_to(mp3, DOWN, buff=0.12))
        place(mp3_g, left=CTR_L + 0.15, cy=cy - 0.05)
        fun = funnel()
        fun.move_to([CTR_L + 2.65, cy + 0.05, 0])
        # the label sits under the funnel (like the MP3's), so the page dropping into the mouth
        # never crosses it
        fun_lab = mono("ffmpeg", 20, SYSTEM).next_to(fun, DOWN, buff=0.1)
        flac = flac_block()
        flac_home = np.array([CTR_L + CTR_W - 0.2 - flac.width / 2, cy - 0.12, 0])

        p1 = src_panel(CLI, 67, 69, size=22)
        place(p1, left=CTR_L, top=TOP)
        df = file_panel(DF, 3, 3, "transcribe_audio/Dockerfile", size=20)
        place(df, right=EDGE, top=p1.get_bottom()[1] - 0.2)
        dfcap = readme_caption()
        place(dfcap, right=df.get_left()[0] - 0.4, cy=df.code.get_center()[1])
        u_ff = under(code_span(df.code, 0, "ffmpeg"), SYSTEM)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(api), FadeIn(mp3_g), run_time=0.8)
            self.play(tr.goto(11), run_time=0.5)
            self.play(Indicate(api.api.title, color=CLOUD, scale_factor=1.12), run_time=0.6)
            vo.wait_until("For each recording")
            self.play(FadeIn(p1, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(mp3, color=INK, scale_factor=1.15), run_time=0.5)
            vo.wait_until("ffmpeg first converts")
            bar = line_bar(p1.code, 0, TURN)
            self.play(FadeIn(fun), FadeIn(fun_lab), FadeIn(bar), run_time=0.45)
            cp = mp3.copy()
            self.add(cp)
            self.play(cp.animate.move_to(fun.mouth() + UP * 0.12), run_time=0.55)
            self.play(FadeOut(cp, target_position=fun.get_center(), scale=0.25),
                      Transform(bar, line_bar(p1.code, 1, TURN)), run_time=0.4)
            flac.scale(0.3).move_to(fun.spout())
            self.play(flac.animate.scale(1 / 0.3).move_to(flac_home), run_time=0.7)
            self.play(Transform(bar, line_bar(p1.code, 2, TURN)),
                      Indicate(fun, color=SYSTEM, scale_factor=1.15), run_time=0.6)
            vo.wait_until("and that's why")
            self.play(FadeIn(df, shift=UP * 0.1), FadeIn(dfcap, shift=UP * 0.1), run_time=0.6)
            self.play(Create(u_ff), Indicate(fun_lab, color=SYSTEM, scale_factor=1.2), run_time=0.7)
            self.play(Indicate(code_span(df.code, 0, "ffmpeg"), color=SYSTEM, scale_factor=1.15),
                      run_time=0.6)

        # ========================================================== 1 · inline bytes, an operation, 90 s
        p2 = src_panel(CLI, 75, 78, size=20)
        place(p2, cx=0, top=TOP)
        c2 = p2.code
        arrow = Arrow(api.ctr.frame.get_right() + RIGHT * 0.06, api.api.shape.get_left() + RIGHT * 0.02,
                      buff=0, stroke_width=4, color=INK, max_tip_length_to_length_ratio=0.05)
        cost = cost_tag().next_to(arrow, UP, buff=0.14)
        u_content = under(code_span(c2, 0, "content=content"), TURN)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(p1, bar, df, dfcap, u_ff)), FadeOut(VGroup(mp3_g, fun, fun_lab)),
                      FadeIn(p2, shift=DOWN * 0.15), run_time=0.6)
            bar = line_bar(c2, 0, TURN)
            self.play(FadeIn(bar), Create(u_content), run_time=0.4)
            self.play(GrowArrow(arrow), flac.animate.move_to(arrow.get_center()), run_time=0.7)
            self.play(flac.animate.move_to(cloud_c), FadeIn(cost, shift=DOWN * 0.1), run_time=0.7)
            self.play(FadeOut(flac, scale=0.4), Indicate(api.api.shape, color=CLOUD, scale_factor=1.05),
                      run_time=0.5)
            vo.wait_until("The long-running recognize call")
            self.play(Transform(bar, line_bar(c2, 2, TURN)), FadeOut(u_content), run_time=0.35)
            vo.wait_until("hands back")
            stub = api.stub(self)
            vo.wait_until("like a ticket stub")
            self.play(Indicate(stub, color=CTR, scale_factor=1.15), run_time=0.7)
            vo.wait_until("Its result call")
            self.play(Transform(bar, line_bar(c2, 3, TURN)), run_time=0.3)
            ring = api.ring(self, stub, "up to 90 s", run_time=1.7)
            vo.wait_until("for the transcript")
            page = page_token().scale(1.25).move_to(cloud_c)
            self.play(FadeIn(page, scale=0.6), run_time=0.3)
            self.play(page.animate.move_to(api.inside()), FadeOut(arrow), FadeOut(stub, scale=0.6),
                      FadeOut(ring), run_time=0.9)
            self.play(Indicate(page, color=INK, scale_factor=1.15), run_time=0.5)

        # ========================================================== 2 · join every piece (lines 84-91)
        p3 = src_panel(CLI, 84, 91, size=20)
        place(p3, left=CTR_L, top=TOP)
        c3 = p3.code
        ic = api.inside()
        slips = VGroup(slip(0.95), slip(0.7), slip(0.85))
        for k, s in enumerate(slips):
            s.move_to(ic + UP * (0.5 - 0.5 * k) + RIGHT * (0.35 * (k - 1)))
        fix = tag("the latest commit's fix", S.GREY)
        fix.next_to(c3.code_lines[6], RIGHT, buff=0.5)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p2, bar)), FadeIn(p3, shift=DOWN * 0.15), run_time=0.6)
            self.play(ReplacementTransform(page, slips), run_time=0.8)
            vo.wait_until("so lines 84 to 91")
            bar = lines_bar(c3, 2, 4, TURN)
            self.play(FadeIn(bar), run_time=0.3)
            self.play(LaggedStart(*[Indicate(s, color=TURN, scale_factor=1.15) for s in slips], lag_ratio=0.5),
                      run_time=1.1)
            self.play(Transform(bar, line_bar(c3, 6, TURN)), run_time=0.3)
            page = page_token().scale(1.25).move_to(ic)
            self.play(ReplacementTransform(slips, page), run_time=0.8)
            vo.wait_until("that was the latest")
            self.play(FadeIn(fix, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(fix.text, color=INK, scale_factor=1.12), run_time=0.6)

        # ========================================================== 3 · type --transcribe; look for
        t = term(P_CTR, STRIP, component="transcribe_audio")
        seed_prompt(t)
        card_t = readme_cmd_card(135, T_CMD, "-t")
        place(card_t, left=-EDGE, bottom=ST + 0.14)
        lf = LookFor(LOOK_T, fail=FAIL_T)
        place(lf, cx=0, top=TOP - 0.02)
        cost_home = np.array([EDGE - cost.width / 2, ST + 0.08 + cost.height / 2, 0])
        assert lf.get_bottom()[1] > cost_home[1] + cost.height / 2 + 0.1, lf.get_bottom()

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(p3, bar, fix, page, api)), cost.animate.move_to(cost_home),
                      FadeIn(t), run_time=0.8)
            self.play(FadeIn(card_t, shift=UP * 0.1), run_time=0.5)
            type_cmd(self, t, T_CMD, 1.1)
            self.play(Indicate(card_t.code, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("or dash t")
            self.play(Indicate(card_t.same.text, color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("Look for transcribing")
            self.play(FadeOut(card_t, shift=DOWN * 0.1), FadeIn(lf), run_time=0.5)
            lf.write_item(self, 0, run_time=0.4)
            vo.wait_until("ffmpeg's log")
            lf.write_item(self, 1, run_time=0.4)
            vo.wait_until("the response")
            lf.write_item(self, 2, run_time=0.4)
            vo.wait_until("and the transcript")
            lf.write_item(self, 3, run_time=0.4)
            vo.wait_until("If it says no such file")
            lf.write_fail(self, run_time=0.5)
            vo.wait_until("add ffmpeg to line 3")
            self.play(Indicate(lf.fail_row, color=ERR, scale_factor=1.04), run_time=0.8)
            vo.wait_until("exit and rebuild")
            self.play(Indicate(tr.dots[12], color=TURN, scale_factor=2.2), run_time=0.8)

        # ========================================================== 4 · the file on your laptop; None
        # the same window S08 left and S11 opens on: 7 rows, the sheet captioned "throwaway", the
        # 26 packages of S08 still on this container's layer; plus the GOLD key S09 put in secrets/
        win = Window(files=WIN_FILES, copied=WIN_COPIED, key=True, mounted=True)
        cap = win.sheet.caption
        new_cap = sans("writable layer · throwaway", 20, CTR).move_to(cap, aligned_edge=LEFT)
        win.sheet.remove(cap)
        win.sheet.add(new_cap)
        win.sheet.caption = new_cap
        sh = win.sheet.shelf
        chips = pkg_dots(26, cols=13)
        if chips.width > sh.get_length() - 0.1:
            chips.scale_to_fit_width(sh.get_length() - 0.1)
        chips.next_to(sh, UP, buff=0.03)
        win.sheet.add(chips)
        place(win, bottom=ST + 0.06)
        win.shift(RIGHT * WIN_DX)
        assert win.get_top()[1] < tr.get_bottom()[1] - 0.02, win.get_top()
        assert win.sheet.frame.get_left()[0] > tr.get_right()[0] + 0.05
        # no room under the 7-row window: its tag sits top right (beside the tracker) while it is
        # up, and bottom left over the strip once the opened page replaces it
        ill = illustration_tag("with your key")
        place(ill, right=win.get_right()[0], cy=(tr.get_bottom()[1] + tr.get_top()[1]) / 2)
        assert ill.get_bottom()[1] > win.get_top()[1] + 0.05 and ill.get_left()[0] > tr.get_right()[0] + 0.3
        ill2 = illustration_tag("with your key")
        place(ill2, left=-EDGE, bottom=ST + 0.08)
        badges = []
        for side in ("laptop", "cover"):
            g = win.row("text_prompts/", side).glyph
            b = page_token().scale_to_fit_height(0.24)
            b.move_to(g.get_corner(UR) + np.array([-0.02, -0.02, 0]))
            badges.append(b)
        op = opened_page()
        place(op, left=-EDGE, top=TOP - 0.05)
        np_ = none_page()
        code80 = src_panel(CLI, 80, 80, size=20)
        place(code80, right=EDGE, top=TOP - 0.05)
        none_q = code_span(code80.code, 0, '"None"')
        place(np_, cy=0.65)
        np_.shift(RIGHT * (none_q.get_center()[0] - np_.text.get_center()[0]))
        ptr = Arrow([np_.text.get_center()[0], np_.frame.get_top()[1], 0],
                    none_q.get_bottom() + DOWN * 0.08, buff=0, color=S.GREY, stroke_width=3,
                    max_tip_length_to_length_ratio=0.25)
        u_none = under(none_q, ERR)
        strike_n = Line(np_.frame.get_corner(DL) + np.array([0.2, 0.15, 0]),
                        np_.frame.get_corner(UR) + np.array([-0.2, -0.15, 0]), color=S.GREY, stroke_width=4)
        del_note = label("delete it, transcribe again", 20, S.GREY)
        place(del_note, left=np_.get_left()[0], top=np_.get_bottom()[1] - 0.15)
        skip = VGroup(label("files already done are skipped", 20, S.GREY),
                      label("(cli.py lines 61–62): delete one to redo it", 20, S.GREY))
        skip.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        place(skip, left=-EDGE + 0.05, top=op.get_bottom()[1] - 0.25)

        with self.voiceover(SAY[4]) as vo:
            lf.write_item(self, 4, run_time=0.5)
            self.play(Indicate(lf.rows[4].text, color=INK, scale_factor=1.04), run_time=0.6)
            # the cost tag steps out while the window needs the bottom right (back in beat 5)
            self.play(FadeOut(lf), FadeOut(cost), FadeIn(win), FadeIn(ill), run_time=0.8)
            vo.wait_until("under text prompts")
            # the page lands on both sides at once: it reached the laptop through the mount (the
            # route is already PINK, so it pulses in width)
            self.play(*[FadeIn(b, scale=1.6) for b in badges],
                      win.route.animate(rate_func=there_and_back).set_stroke(width=12), run_time=0.7)
            vo.wait_until("on your laptop")
            self.play(Indicate(win.row("text_prompts/", "laptop"), color=TURN, scale_factor=1.15), run_time=0.45)
            grow = badges[0].copy()
            self.remove(badges[0])
            self.play(ReplacementTransform(grow, op), FadeOut(win), FadeOut(badges[1]), FadeOut(ill),
                      run_time=0.75)
            vo.wait_until("If it says None")
            # the None page is the same file in its other outcome: a copy of the page becomes it
            self.play(*dim_page(op, 0.5), FadeTransform(op.frame.copy(), np_), FadeIn(ill2), run_time=0.7)
            vo.wait_until("Speech-to-Text returned nothing")
            self.play(FadeIn(code80, shift=DOWN * 0.1), run_time=0.5)
            self.play(GrowArrow(ptr), Create(u_none), run_time=0.6)
            vo.wait_until("delete it and transcribe")
            self.play(Create(strike_n), FadeIn(del_note, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("because finished files")
            self.play(FadeIn(skip, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(skip[0], color=INK, scale_factor=1.05), run_time=0.7)

        # ========================================================== 5 · step 12: --upload
        card_u = readme_cmd_card(136, U_CMD, "-u")
        place(card_u, left=-EDGE, bottom=ST + 0.14)
        xc = excerpt_chip(CLI, GLOB_LINE, GLOB)
        place(xc, cx=0, top=TOP)
        g_inp = substring(xc.code, '"input-*.txt"')
        u_inp = under(g_inp, LOOKUP)
        p111 = src_panel(CLI, 111, 115, size=20)
        place(p111, cx=0, top=xc.get_bottom()[1] - 0.18)
        c111 = p111.code
        lfu = LookFor(LOOK_U)
        utext = lfu.rows[0].text
        parts = [tglyphs(utext, s) for s in ("text_prompts/", f"{GROUP}/", "input-….txt")]

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(op, np_, code80, ptr, u_none, strike_n, del_note, skip, ill2)),
                      FadeIn(cost), tr.goto(12), run_time=0.6)
            t.clear(self)
            vo.wait_until("python cli.py dash dash upload")
            self.play(FadeIn(card_u, shift=UP * 0.1), run_time=0.4)
            type_cmd(self, t, U_CMD, 1.0)
            vo.wait_until("or dash u")
            self.play(Indicate(card_u.same.text, color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("It uploads only")
            self.play(FadeOut(card_u, shift=DOWN * 0.1), FadeIn(xc, shift=DOWN * 0.1), run_time=0.6)
            self.play(g_inp.animate.set_color(LOOKUP), Create(u_inp), run_time=0.5)
            vo.wait_until("under the same name")
            self.play(FadeIn(p111, shift=DOWN * 0.1), run_time=0.5)
            bar = line_bar(c111, 1, LOOKUP, 0.2)
            self.play(FadeIn(bar), run_time=0.4)
            vo.wait_until("look for uploading")
            dy = TOP - p111.get_top()[1]
            place(lfu, left=-EDGE, top=p111.get_bottom()[1] + dy - 0.2)
            self.play(FadeOut(VGroup(xc, u_inp), shift=UP * 0.2), run_time=0.3)
            self.play(VGroup(p111, bar).animate.shift(UP * dy), FadeIn(lfu, shift=UP * 0.15), run_time=0.5)
            # the item's thin GREY line to the cli.py line it cites (114; line 115 is shorter, so
            # the line crosses no code)
            cite = lfu.rows[0].cite
            hook = Line(cite.get_top() + UP * 0.06,
                        [cite.get_center()[0], c111.code_lines[3].get_bottom()[1] - 0.05, 0],
                        color=S.GREY, stroke_width=2)
            assert c111.code_lines[4].get_right()[0] < cite.get_left()[0] - 0.2
            lfu.reveal(self, "item0", run_time=0.4, extra=[Create(hook)])
            vo.wait_until("then text prompts")
            self.play(parts[0].animate.set_color(LOOKUP), run_time=0.3)
            vo.wait_until("your group")
            self.play(parts[1].animate.set_color(LOOKUP), run_time=0.3)
            vo.wait_until("and the file")
            self.play(parts[2].animate.set_color(LOOKUP), run_time=0.3)

        # ========================================================== 6 · into your group's drawer; leaderboard
        relay = Relay(width=5.9, labels=False, bonus=False, box_h=0.8, drawer_h=0.85, gap=0.6)
        for let, b in zip(relay.letters, relay.boxes):
            let.move_to(b)
        place(relay, left=-EDGE, top=TOP - 0.05)
        d1 = relay.drawers[1].frame
        dlab = mono(f"text_prompts/{GROUP}/", 20, LOOKUP)
        place(dlab, left=relay.cabinet.get_left()[0] + 0.05, top=relay.cabinet.get_bottom()[1] - 0.22)
        tick = Line(d1.get_bottom() + DOWN * 0.04, [d1.get_center()[0], dlab.get_top()[1] + 0.06, 0],
                    color=LOOKUP, stroke_width=3)
        tok = page_token().move_to(relay.center_of(0))
        cards = commands_card("README.md · lines 134–136", README_CMDS)
        place(cards, right=EDGE, top=TOP - 0.05)
        yt = your_turn()
        place(yt, right=EDGE, top=cards.get_bottom()[1] - 0.18)
        lb = Leaderboard()
        place(lb, cx=0, top=-0.45)
        # where to check (the address S02 showed), and the README line that says so, under it
        lb_url = VGroup(label("check:", 20, S.GREY), mono(LB_URL, 20, S.GREY)).arrange(RIGHT, buff=0.12)
        lb_src = VGroup(label("(", 20, S.GREY), mono("transcribe_audio/README.md", 20, S.GREY),
                        label("· line 134)", 20, S.GREY))
        lb_src.arrange(RIGHT, buff=0.12)
        lb_src[0].next_to(lb_src[1], LEFT, buff=0.04)
        place(lb_url, left=lb.get_left()[0], top=lb.get_bottom()[1] - 0.2)
        place(lb_src, left=lb_url[1].get_left()[0] - lb_src[1].get_left()[0] + lb_src.get_left()[0],
              top=lb_url.get_bottom()[1] - 0.12)
        lb_cap = VGroup(lb_url, lb_src)
        assert lb_cap.get_bottom()[1] > -3.55, lb_cap.get_bottom()
        lb_ill = illustration_tag()
        place(lb_ill, right=lb.get_right()[0], cy=lb_url.get_center()[1])
        assert lb_ill.get_left()[0] > max(lb_url.get_right()[0], lb_src.get_right()[0]) + 0.3
        cost6 = np.array([yt.get_left()[0] - 0.25 - cost.width / 2, yt.get_center()[1], 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(t, p111, bar, lfu, hook)), cost.animate.move_to(cost6), run_time=0.6)
            relay.reveal(self, "letters", run_time=0.6,
                         extra=[FadeIn(VGroup(relay.cabinet, relay.drawers, relay.boxes))])
            self.play(FadeIn(tok, scale=0.5), Indicate(relay.boxes[0], color=CTR, scale_factor=1.08), run_time=0.4)
            self.play(tok.animate.move_to(relay.slot(1)), run_time=0.8)
            self.play(Create(tick), FadeIn(dlab, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and the transcribe cell")
            self.play(FadeIn(lb), FadeIn(lb_ill), run_time=0.6)
            self.play(lb.light(0, 0), Indicate(lb.row_names[0], color=INK, scale_factor=1.1), run_time=0.7)
            vo.wait_until("which is how the README")
            self.play(FadeIn(lb_cap, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(lb.cells[0][0], color=S.GREEN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("Pause and run")
            self.play(FadeIn(cards, shift=LEFT * 0.15), run_time=0.5)
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            self.play(Wiggle(yt, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)

        # ========================================================== 7 · -d -t -u combine (extra)
        p121 = src_panel(CLI, 121, 126, size=20)
        place(p121, right=EDGE, top=2.3)
        c121 = p121.code
        combo = mono_line(COMBO, 22, INK)
        cfr = box(combo.width + 0.5, combo.strut.height + 0.3, S.GREY, fill_opacity=0.12, radius=0.14)
        combo.move_to(cfr)
        chip_c = VGroup(cfr, combo)
        place(chip_c, left=-EDGE + 0.1, cy=-1.55)
        xtag = extra_tag()
        place(xtag, left=chip_c.get_right()[0] + 0.25, cy=chip_c.get_center()[1])
        flags = [substring(combo, f) for f in ("-d", "-t", "-u")]
        calls = [code_span(c121, k, s) for k, s in ((1, "download()"), (3, "transcribe()"), (5, "upload()"))]
        arrows = []
        for f, c in zip(flags, calls):
            p0 = f.get_top() + UP * 0.12
            p1_ = np.array([f.get_center()[0], c.get_center()[1], 0])
            p2_ = np.array([c.get_left()[0] - 0.16, c.get_center()[1], 0])
            arrows.append(elbow(p0, p1_, p2_))
        cost7 = np.array([chip_c.get_left()[0] + cost.width / 2, chip_c.get_bottom()[1] - 0.3 - cost.height / 2, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(tok, dlab, tick, lb, lb_cap, lb_ill, yt)), FadeOut(relay),
                      caption_extra(tr, True), cost.animate.move_to(cost7), run_time=0.7)
            vo.wait_until("the flags combine")
            # the three README commands collapse into the one extra command
            self.play(ReplacementTransform(cards.frame, cfr),
                      FadeTransform(cards.rows, combo, stretch=False, dim_to_match=0),
                      FadeOut(cards.header), FadeIn(xtag, shift=LEFT * 0.1), run_time=0.8)
            self.play(FadeIn(p121, shift=LEFT * 0.15), run_time=0.5)
            for k, phrase in enumerate(("so dash d", "dash t", "dash u")):
                vo.wait_until(phrase)
                self.play(flags[k].animate.set_color(TURN), Create(arrows[k]), run_time=0.5)
            vo.wait_until("in order")
            bars = [line_bar(c121, k, TURN).set_fill(opacity=0) for k in (1, 3, 5)]
            self.add(*bars)
            self.bring_to_front(*arrows)                 # the bars go under the arrow tips
            self.play(LaggedStart(*[b.animate.set_fill(opacity=0.16) for b in bars], lag_ratio=0.6),
                      run_time=1.0)
            vo.wait_until("Each call is billed")
            self.play(Wiggle(cost, scale_value=1.15, rotation_angle=0.015 * TAU), run_time=0.9)

        self.play(FadeOut(VGroup(tr, chip_c, xtag, p121, *arrows, *bars, cost)), run_time=0.8)
        self.wait(0.3)
