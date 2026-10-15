r"""S09 · Who is calling? The key and ADC (README › transcribe_audio step 10; V5).

The house terminal is the container's (TEAL frame, title `container · transcribe_audio`, prompt
`app@5b4d4981ec25:/app$`): 13 rows in beats 0–2, a 3-row strip under V5 in beats 3–7 (the
command and the RED last line of the traceback), 12 rows in beat 8, the strip again under the
code panel at the end of beat 8; beat 9 has no terminal (the panel and the card need the frame).

Beats (script.md "## S09", one voiceover block each):
 0  TRACKER A9→A10. The 13-row terminal with a waiting prompt; a one-line README chip in the top
    band, right of the tracker: `README.md · line 134 · --download`. It types `python cli.py
    --download`; on "or dash d" the chip turns into `transcribe_audio/README.md · line 131 · -d`.
    TERM(07-download.txt: 2–3, …, 9–10, …, 22–23, …, 36; wrap), line 36 RED; GREY tag
    "recorded without the key" at the right end of the first `…` row.
 1  Lines 2 and 3 get GREEN checks and the GREY note "printed before any Google call"; on "The
    last line says" a RED bar lies behind both rows of line 36; "DefaultCredentialsError" and then
    "secrets/mega" + "-pipeline.json" underline RED.
 2  The rows off the reading path dim. A YELLOW eye reads downward: line 9 (white, "line 36"
    pulses) with the label "our code" → line 10 `client = storage.Client()` turns YELLOW → line 23
    `google.auth.default()` turns PINK, label "the client asks" → line 36, label "google.auth looks
    for the file".
 3  The eye and labels go; `storage.Client()` (line 10) and `google.auth` (line 23; its
    `.default()` fades) lift out of the terminal, which shrinks to the strip (the command + both
    rows of line 36, RED) while the two words fly to their places in V5; then the container
    outline and the boxes draw in around them: the `storage.Client()` machine and the GREY
    `google.auth` box. The client pulses ("never passes the key"), then asks
    "who am I?"; GREY tag "ADC · Application Default Credentials" under them; on "its first stop"
    the PINK signpost is planted at /app with a small tag "Dockerfile · line 10".
 4  The signpost's board, then its path line, then the /app root pulse; on "Through the window"
    the laptop folder (secrets/, the GOLD key mega-pipeline.json) and the dashed PINK window appear
    and google.auth follows the signpost out to the key, which glows.
 5  The followed path goes; the key stamps out the GOLD token (small clock) with the GOLD word
    "short-lived" over it; Google Cloud (BLUE) appears, the request arrow grows and the token
    rides it up to gate 1; a GOLD tag "billed to the course project" under the cloud, pinned to
    the arrow by a thin GOLD line.
 6  README chip `README.md · lines 92–95` in the top band. Gate 1 pulses; its question "who is
    calling?" turns into "service account" (GREEN) and gets a GREEN check while the key pulses;
    gate 2 pulses; its question becomes "IAM roles allow it", the padlock opens and the bucket
    door opens.
 7  Error branch: the cloud, gates, token, arrow and tags go; container, signpost and laptop stay.
    The key vanishes (RED cross), google.auth follows the signpost again into the empty secrets/.
    Three causes, one at a time, each undone before the next, with a RED numbered badge and
    two-line caption top right: (1) no key in this component's secrets/ (line 36 pulses RED in
    the strip); (2) the root slides from /app to /tmp (RED cross: nothing there); (3) the window
    re-aims at mega-pipeline/. The root label and the folder name cross-fade (local reroot()/
    reaim(), not the shared letter morph). After the voice, V5 leaves and a GREY footnote card
    stands alone above the strip: "a different error: 403 … storage.buckets.get → the key lacks
    rights: ask the staff".
 8  TRACKER A10 · extra. The picture goes, the terminal grows to 12 rows: `ls -la input_audios
    text_prompts text_prompts/*` (extra; folds) → TERM(08-ls-after-download.txt: 2, …, 7, …, 11,
    13); input_audios: and text_prompts: get GREY bars, `group-01` a GREY box. Then the terminal
    shrinks to the strip (the command + the group-01 row); above it CODE(transcribe_audio/cli.py:
    33–36) and a GREY laptop folder with the two empty folders input_audios/ and
    text_prompts/group-01/ (they pulse); on "The code makes them" lines 33–34 get a GREY bar +
    "clear, then make the folders", on "before it builds the client" line 36 a PINK bar + "the
    client".
 9  TRACKER A10. The strip and the folder go; the panel swaps to CODE(cli.py: 39–43); the caption
    card "with your key, look for" (no terminal frame) and the GOLD tag "billed to the course
    project" appear; items write in on their words: "download" (line 30), "one object name per
    recording: input_audios/…" (line 41, its panel line gets a YELLOW bar), "the audio files in
    input_audios/ on your laptop" (line 43, GREY bar). On "Pause" the README chip `README.md ·
    line 134` and ▶ your turn arrive in the top band. Everything fades: empty frame.
"""

import numpy as np
from manim import *

from explainer import style as S
from explainer.devops import (CAPTION, box, check_mark, cross_mark, label, line_bar, mono,
                              step_badge, substring, tag)
from explainer.scene import VoiceScene

from common import (CLOUD, COST, CTR, ERR, GROUP, INK, LAPTOP, LOOKUP, NARRATION, P_CTR, TURN, VENV,
                    AdcChain, LookFor, _set_op, asset_lines, bare_prompt, caption_extra, capture,
                    cost_tag, extra_tag, file_row, nokey_tag, pin, readme_chip, resize, source_text,
                    src_panel, term, tracker, type_cmd, your_turn)

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ commands and real outputs
DL = capture("07-download", "transcribe_audio")
DL_CMD = "python cli.py --download"                 # README.md:134
assert DL.cmd == DL_CMD, DL.cmd
DL_OUT = DL.at((2, 3), "…", (9, 10), "…", (22, 23), "…", 36)
assert DL_OUT[0].startswith("Args: Namespace(download=True") and DL_OUT[1] == "download"
assert DL_OUT[3] == '  File "/app/cli.py", line 36, in download', DL_OUT[3]
assert DL_OUT[4].strip() == "client = storage.Client()", DL_OUT[4]
assert DL_OUT[7].strip() == "_, project = google.auth.default()", DL_OUT[7]
LAST = DL_OUT[9]
assert LAST == ("google.auth.exceptions.DefaultCredentialsError: File secrets/mega-pipeline.json "
                "was not found."), LAST

LS = capture("08-ls-after-download", "transcribe_audio")
LS_CMD = "ls -la input_audios text_prompts text_prompts/*"
assert LS.cmd == LS_CMD, LS.cmd
LS_OUT = LS.at(2, "…", 7, "…", 11, 13)
assert LS_OUT[0] == "input_audios:" and LS_OUT[2] == "text_prompts:"
assert LS_OUT[4].endswith(" group-01") and LS_OUT[5] == "text_prompts/group-01:", LS_OUT

_RM = source_text("README.md").split("\n")
assert _RM[133] == DL_CMD, _RM[133]                                   # README.md line 134
assert "authenticated" in _RM[92] and "authorized" in _RM[92]          # README.md lines 92-95
assert "Service Account" in _RM[94] and "IAM" in _RM[94]
_RA = source_text("transcribe_audio/README.md").split("\n")
assert "`python cli.py -d`" in _RA[130], _RA[130]                     # its line 131
_CLI = source_text("transcribe_audio/cli.py").split("\n")
assert _CLI[29].strip() == 'print("download")' and _CLI[40].strip() == "print(blob.name)"
assert _CLI[42].strip() == "blob.download_to_filename(blob.name)"
assert _CLI[35].strip() == "client = storage.Client()" and _CLI[33].strip() == "makedirs()"
assert asset_lines("files/transcribe_audio.Dockerfile", 10, 10) == \
    "ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json"     # the signpost's source

# ------------------------------------------------------------------ layout
EDGE = 6.45                        # right edge for chips and tags
BAND_Y = 3.21                      # centre of the top band (tracker row), right of the tracker
CHAIN_Y = 0.75                     # V5 above a 3-row strip
TERM_ROWS = 13


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


def note_chip(where: str, note: str | None = None, mono_note: bool = False) -> VGroup:
    """A README chip whose last words are ours, not the README's (so: no quotes)."""
    path, _, rest = where.partition(" · ")
    parts = [mono(path, 20, S.GREY)] + ([label(f"· {rest}", 20, S.GREY)] if rest else [])
    if note:
        parts.append(mono(note, 20, INK) if mono_note else label(f"· {note}", 20, INK))
    row = VGroup(*parts).arrange(RIGHT, buff=0.12)
    if mono_note and note:
        row[-1].shift(RIGHT * 0.1)
    fr = box(row.width + 0.4, row.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.92, radius=0.1)
    fr.move_to(row)
    g = VGroup(fr, row)
    g.frame, g.row = fr, row
    return g


def stick(scene, line, *mobs, under: bool = False):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded), so
    they move and fade with it; under=True draws them beneath the row's glyphs (a bar)."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        if under:
            row.submobjects.insert(0, m)
        else:
            row.add(m)
    scene.add(row)


def rbar(lines, color, opacity=0.18, pad=0.08) -> Rectangle:
    """A translucent bar behind whole terminal rows (first glyph to last)."""
    lines = lines if isinstance(lines, (list, tuple)) else [lines]
    left = min(ln.glyphs.get_left()[0] for ln in lines) - pad
    right = max(ln.glyphs.get_right()[0] for ln in lines) + pad
    top = lines[0].strut.get_top()[1] + 0.02
    bot = lines[-1].strut.get_bottom()[1] - 0.02
    return Rectangle(width=right - left, height=top - bot, stroke_width=0).set_fill(color, opacity) \
        .move_to([(left + right) / 2, (top + bot) / 2, 0])


def uline(line, sub, color, stroke=3.5, occ=0, pad=0.02) -> Line:
    """A Line under substring `sub` of terminal row `line`, in the gap under the row."""
    g = substring(line, sub, occ)
    y = line.strut.get_bottom()[1] + 0.01
    return Line([g.get_left()[0] - pad, y, 0], [g.get_right()[0] + pad, y, 0], color=color,
                stroke_width=stroke)


def eye_glyph(w: float = 0.5, color: str = TURN) -> VGroup:
    """A YELLOW eye (an almond outline, an iris and a pupil): the reader's eye on a traceback."""
    top = ArcBetweenPoints(LEFT * w / 2, RIGHT * w / 2, angle=-0.62 * PI, color=color, stroke_width=3)
    bot = ArcBetweenPoints(LEFT * w / 2, RIGHT * w / 2, angle=0.62 * PI, color=color, stroke_width=3)
    iris = Circle(radius=w * 0.17, color=color, stroke_width=3)
    pupil = Dot(radius=w * 0.07, color=color)
    return VGroup(top, bot, iris, pupil)


def show_part(piece, name: str):
    """A hidden part of a Piece becomes visible at once (a lifted copy has just landed on it)."""
    m = piece.parts[name]
    _set_op(m)
    piece._flag(m, False)


def swap_words(old, new) -> Animation:
    """old fades out, then new fades in on the same spot (never both half-visible at once)."""
    return LaggedStart(old.animate.set_opacity(0), FadeIn(new, shift=UP * 0.1), lag_ratio=1.0)


def _xfade_into(scene, old, new, shift=ORIGIN, anims=(), run_time: float = 0.8):
    """old (a member of a piece) fades out over the first half of `shift`, `new` fades in over
    the second half; then old takes new's shape, so the piece keeps its member. No
    letter-by-letter morph, and the two words are never on screen together."""
    swap = LaggedStart(old.animate.shift(shift * 0.5).set_opacity(0), FadeIn(new, shift=shift * 0.5),
                       lag_ratio=1.0)
    scene.play(swap, *anims, run_time=run_time)
    if swap.group in scene.mobjects:
        scene.remove(swap.group)
    old.become(new)
    scene.remove(new)


def reroot(scene, chain, text: str | None = "/tmp", dx: float = 1.9, run_time: float = 1.0):
    """AdcChain.reroot, with the root label cross-fading instead of morphing its letters."""
    top = chain.post.post.get_start()
    dot = top + DOWN * 0.5 + (RIGHT * dx if text is not None else 0)
    new_post = Line(top, dot, color=LOOKUP, stroke_width=4)
    new_foot = chain.post.foot.copy().move_to(dot)
    new_label = mono(text or "/app", CAPTION, LOOKUP).next_to(Dot(dot), RIGHT, buff=0.15)
    new_label.shift(DOWN * 0.05)
    shift = new_label.get_left() - chain.root_label.get_left()
    _xfade_into(scene, chain.root_label, new_label, shift=shift,
                anims=[chain.root_dot.animate.move_to(dot), Transform(chain.post.post, new_post),
                       Transform(chain.post.foot, new_foot)], run_time=run_time)


def reaim(scene, chain, folder: str, run_time: float = 0.8):
    """AdcChain.reaim (run from the wrong laptop folder): the folder name cross-fades into
    `folder` (RED) while secrets/ and the key vanish."""
    new = mono(folder, CAPTION, ERR).move_to(chain.folder, aligned_edge=LEFT)
    old = chain.folder
    swap = swap_words(old, new)
    chain.hide(scene, "secrets", "key", run_time=run_time, extra=[swap])
    if swap.group in scene.mobjects:
        scene.remove(swap.group)
    old.become(new)
    scene.remove(new)


def glyph_dim(lines, k: float):
    """Animations: the glyphs (and anything pinned) of terminal rows to opacity k; the row's
    invisible strut stays invisible."""
    return [VGroup(*[m for m in ln.submobjects if m is not ln.strut]).animate.set_opacity(k)
            for ln in lines]


def cause_badge(k: int, lines: list[str]) -> VGroup:
    """A RED numbered badge with a two-line caption under it (the error causes of beat 7)."""
    b = step_badge(k, ERR, size=22, radius=0.26)
    txt = VGroup(*[label(s, 20, INK) for s in lines]).arrange(DOWN, buff=0.08)
    g = VGroup(b, txt).arrange(DOWN, buff=0.18)
    g.badge, g.text = b, txt
    return g


def footnote_card() -> VGroup:
    rows = VGroup(label("a different error:", 20, S.GREY),
                  mono("403 … storage.buckets.get", 20, ERR),
                  label("→ the key lacks rights: ask the staff", 20, INK))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    fr = RoundedRectangle(width=rows.width + 0.6, height=rows.height + 0.44, corner_radius=0.14,
                          stroke_color=S.GREY, stroke_width=2).set_fill(S.BG, 0.96).move_to(rows)
    return VGroup(fr, rows)


def laptop_folders() -> VGroup:
    """Your laptop's transcribe_audio/ folder with the two (empty) folders the failed run made."""
    head = VGroup(label("your laptop ·", 20, LAPTOP), mono("transcribe_audio/", 20, LAPTOP))
    head.arrange(RIGHT, buff=0.12)
    head[0].align_to(head[1], DOWN)
    r1, r2 = file_row("input_audios/"), file_row(f"text_prompts/{GROUP}/")
    rows = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    empty = label("both empty", 20, S.GREY)
    body = VGroup(head, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    empty.next_to(rows, RIGHT, buff=0.6)
    inner = VGroup(body, empty)
    fr = box(inner.width + 0.5, inner.height + 0.36, LAPTOP, fill_opacity=0.05).move_to(inner)
    g = VGroup(fr, head, rows, empty)
    g.frame, g.head, g.rows, g.empty = fr, head, rows, empty
    return g


# ------------------------------------------------------------------ the scene
class WhoIsCalling(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, f"S09 has {len(SAY)} SAY lines; this scene times 10"

        tr = tracker("A", 9)

        # ========================================================== 0 · step 10: python cli.py --download
        t = term(P_CTR, TERM_ROWS, component="transcribe_audio")
        assert t.box.get_top()[1] < 2.9, t.box.get_top()[1]
        chip0 = note_chip("README.md · line 134", "--download", mono_note=True)
        chip1 = note_chip("transcribe_audio/README.md · line 131", "-d", mono_note=True)
        tr10_right = tracker("A", 10).get_right()[0]    # the chips arrive with step 10
        for c in (chip0, chip1):
            place(c, right=EDGE, cy=BAND_Y)
            assert c.get_left()[0] > tr10_right + 0.15, (c.get_left()[0], tr10_right)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.7)
            bare_prompt(self, t)
            self.play(tr.goto(10), FadeIn(chip0, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("python cli.py dash dash")
            c0 = type_cmd(self, t, DL_CMD, 1.2)
            vo.wait_until("or dash d for short")
            self.play(ReplacementTransform(chip0, chip1), run_time=0.6)
            self.play(Indicate(chip1.row[-1], color=TURN, scale_factor=1.4), run_time=0.6)
            vo.wait_until("Our machine had no key")
            items = [s if i != 9 else (s, ERR) for i, s in enumerate(DL_OUT)]
            out = t.print(self, items, run_time=1.4, lag=0.08, wrap=True)
            assert len(out) == 12 and len(t.lines) == TERM_ROWS, (len(out), len(t.lines))
            L2, L3, E1, L9, L10, E2, L22a, L22b, L23, E3, L36a, L36b = out
            assert L36a.text.endswith("secrets/mega") and L36b.text.startswith("-pipeline.json")
            nk = nokey_tag()
            place(nk, right=t.box.get_right()[0] - 0.15, cy=E1.strut.get_center()[1])
            pin(self, E1, nk, run_time=0.5)

        # ========================================================== 1 · what it printed
        ck2 = check_mark(0.26, VENV)
        place(ck2, left=L2.glyphs.get_right()[0] + 0.25, cy=L2.strut.get_center()[1])
        ck3 = check_mark(0.26, VENV)
        place(ck3, left=L3.glyphs.get_right()[0] + 0.25, cy=L3.strut.get_center()[1])
        before = label("printed before any Google call", 20, S.GREY)
        place(before, left=ck3.get_right()[0] + 0.3, cy=L3.strut.get_center()[1])
        assert before.get_right()[0] < nk.get_left()[0] - 0.2
        with self.voiceover(SAY[1]) as vo:
            pin(self, L2, ck2, run_time=0.5, anim=Create(ck2))
            self.play(Indicate(substring(L2, "Namespace"), color=VENV, scale_factor=1.1), run_time=0.6)
            vo.wait_until("and the word download")
            pin(self, L3, ck3, run_time=0.5, anim=Create(ck3))
            pin(self, L3, before, run_time=0.5)
            vo.wait_until("then a traceback")
            tb = VGroup(*[ln.glyphs for ln in (L9, L10, L22a, L22b, L23)])
            self.play(Indicate(tb, color=INK, scale_factor=1.02), run_time=0.8)
            vo.wait_until("The last line says")
            bar36 = rbar([L36a, L36b], ERR, 0.2)
            self.play(FadeIn(bar36), run_time=0.5)
            stick(self, L36a, bar36, under=True)
            vo.wait_until("default credentials error")
            u1 = uline(L36a, "DefaultCredentialsError", ERR)
            pin(self, L36a, u1, run_time=0.5, anim=Create(u1))
            vo.wait_until("the file secrets")
            u2 = uline(L36a, "secrets/mega", ERR)
            u3 = uline(L36b, "-pipeline.json", ERR)
            self.play(Create(u2), run_time=0.35)
            self.play(Create(u3), run_time=0.3)
            stick(self, L36a, u2)
            stick(self, L36b, u3)
            vo.wait_until("was not found")
            self.play(Indicate(substring(L36b, "was not found."), color=ERR, scale_factor=1.15),
                      run_time=0.7)

        # ========================================================== 2 · read it downward
        eye = eye_glyph()
        lab_code = label("our code", 20, TURN)
        lab_asks = label("the client asks", 20, LOOKUP)
        lab_file = label("google.auth looks for the file", 20, ERR)

        def eye_at(line):
            return np.array([line.glyphs.get_right()[0] + 0.45, line.strut.get_center()[1], 0])

        place(lab_code, left=eye_at(L9)[0] + 0.4, cy=L9.strut.get_center()[1])
        place(lab_asks, left=eye_at(L23)[0] + 0.4, cy=L23.strut.get_center()[1])
        place(lab_file, left=eye_at(L36b)[0] + 0.4, cy=L36b.strut.get_center()[1])
        for lab in (lab_code, lab_asks, lab_file):
            assert lab.get_right()[0] < t.box.get_right()[0] - 0.2, lab
        off_path = [L2, L3, E1, E2, L22a, L22b, E3]
        with self.voiceover(SAY[2]) as vo:
            eye.move_to(eye_at(L9))
            self.play(*glyph_dim(off_path, 0.3), L9.glyphs.animate.set_color(INK), run_time=0.6)
            self.play(FadeIn(eye, scale=1.4), run_time=0.5)
            vo.wait_until("Our code, line 36")
            self.play(FadeIn(lab_code, shift=LEFT * 0.1), run_time=0.4)
            self.play(Indicate(substring(L9, "line 36"), color=TURN, scale_factor=1.2), run_time=0.7)
            vo.wait_until("built a storage client")
            self.play(eye.animate.move_to(eye_at(L10)),
                      substring(L10, "client = storage.Client()").animate.set_color(TURN), run_time=0.6)
            vo.wait_until("the client asked")
            self.play(eye.animate.move_to(eye_at(L23)),
                      substring(L23, "_, project = google.auth.default()").animate.set_color(LOOKUP),
                      run_time=0.7)
            self.play(FadeIn(lab_asks, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("and that library looked")
            self.play(eye.animate.move_to(eye_at(L36b)), run_time=0.7)
            self.play(FadeIn(lab_file, shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 3 · the chain when it works (V5)
        chain = AdcChain(show=("ctr",)).move_to([0, CHAIN_Y, 0])
        adc = tag("ADC · Application Default Credentials", S.GREY, size=20)
        place(adc, cx=(chain.client.get_left()[0] + chain.auth.get_right()[0]) / 2,
              cy=(chain.client.get_bottom()[1] + chain.ctr_frame.get_bottom()[1]) / 2)
        df = tag("Dockerfile · line 10", S.GREY, size=20)
        with self.voiceover(SAY[3]) as vo:
            # the lifted words are copies; the originals go invisible under them (no double text)
            c10 = substring(L10, "storage.Client()").copy()
            c23 = substring(L23, "google.auth").copy()
            c23t = substring(L23, ".default()").copy()
            substring(L10, "storage.Client()").set_opacity(0)
            substring(L23, "google.auth.default()").set_opacity(0)
            self.add(c10, c23, c23t)
            self.play(FadeOut(eye), FadeOut(lab_code), FadeOut(lab_asks), FadeOut(lab_file), FadeOut(chip1),
                      c10.animate.shift(UP * 0.12).set_color(CTR), c23.animate.shift(UP * 0.12).set_color(INK),
                      FadeOut(c23t, shift=UP * 0.12), run_time=0.45)
            # word to word: each copy lands on the identical text of its V5 box (no shape morph)
            tgt_c, tgt_a = chain.client[1].copy(), chain.auth[1].copy()
            _set_op(tgt_c)
            _set_op(tgt_a)
            resize(self, t, 3, keep=[c0, L36a, L36b], run_time=0.85,
                   extra=[Transform(c10, tgt_c), Transform(c23, tgt_a)])
            # then the container and the two boxes draw in around the words
            bx_c, bx_a = chain.client[0].copy(), chain.auth[0].copy()
            _set_op(bx_c)
            _set_op(bx_a)
            self.add(chain, bx_c, bx_a)
            self.bring_to_front(c10, c23)
            self.play(FadeIn(chain), FadeIn(bx_c), FadeIn(bx_a), run_time=0.55)
            self.remove(c10, c23, bx_c, bx_a)
            show_part(chain, "client")
            show_part(chain, "auth")
            vo.wait_until("Your code never passes")
            self.play(Indicate(chain.client, color=CTR, scale_factor=1.1), run_time=0.8)
            vo.wait_until("the client asks")
            chain.ask(self, run_time=0.8)
            vo.wait_until("That search is called")
            self.play(FadeIn(adc, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("or ADC")
            self.play(Indicate(adc.text, color=INK, scale_factor=1.12), run_time=0.7)
            vo.wait_until("and its first stop")
            chain.reveal(self, "post", "root", run_time=0.7)
            place(df, left=chain.root_label.get_right()[0] + 0.35, cy=chain.root_dot.get_center()[1])
            self.play(FadeIn(df, shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 4 · the signpost and the window
        with self.voiceover(SAY[4]) as vo:
            self.play(Indicate(chain.post.text, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("secrets, slash")
            self.play(Indicate(chain.post.text[1], color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("starting from the current folder")
            self.play(Flash(chain.root_dot, color=LOOKUP, line_length=0.15, flash_radius=0.2),
                      Indicate(chain.root_label, color=TURN, scale_factor=1.3), run_time=0.8)
            vo.wait_until("Through the window")
            self.play(FadeOut(df), run_time=0.3)
            chain.reveal(self, "laptop", "window", run_time=0.5)
            chain.follow(self, run_time=2.0)

        # ========================================================== 5 · a short-lived token, a request
        cost = cost_tag()
        with self.voiceover(SAY[5]) as vo:
            chain.unfollow(self, run_time=0.3)
            tok = chain.mint(self, run_time=0.8)
            short = label("short-lived", 20, COST).next_to(tok, UP, buff=0.12)
            vo.wait_until("a short-lived")
            self.play(FadeIn(short, shift=DOWN * 0.1), Indicate(tok[1][0], color=COST, scale_factor=1.5),
                      run_time=0.6)
            vo.wait_until("and every request")
            chain.reveal(self, "google", run_time=0.5)
            arrow = chain.request(self, None, run_time=0.6)
            spot = tok.copy().next_to(arrow, UP, buff=0.08)
            place(spot, right=min(spot.get_right()[0], chain.gates[0].bar.get_center()[0] - 0.15))
            self.play(tok.animate.move_to(spot), FadeOut(short), run_time=0.6)
            gap_x = (chain.ctr_frame.get_right()[0] + chain.google_frame.get_left()[0]) / 2
            place(cost, right=EDGE, cy=(chain.google_frame.get_bottom()[1] + t.box.get_top()[1]) / 2)
            pin_line = Line([gap_x, cost.get_top()[1], 0], [gap_x, arrow.get_bottom()[1] + 0.02, 0],
                            color=COST, stroke_width=2.5)
            self.play(FadeIn(cost, shift=UP * 0.1), Create(pin_line), run_time=0.5)

        # ========================================================== 6 · two checks (README.md 92-95)
        chip_auth = readme_chip("README.md · lines 92–95")
        place(chip_auth, right=EDGE, cy=BAND_Y)
        g1, g2 = chain.gates
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(chip_auth, shift=DOWN * 0.1), run_time=0.5)
            self.play(Indicate(VGroup(g1.word, g1.question, g2.word, g2.question), color=CLOUD,
                               scale_factor=1.05), run_time=0.8)
            vo.wait_until("Authentication asks")
            self.play(Indicate(VGroup(g1.word, g1.question), color=TURN, scale_factor=1.08),
                      Indicate(tok, color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("and the key says")
            ans1 = label("service account", 20, VENV).move_to(g1.question, aligned_edge=LEFT)
            chain.attach(self, ans1, anims=[swap_words(g1.question, ans1),
                                            Indicate(chain.key, color=COST, scale_factor=1.4)],
                         run_time=0.8, into=g1)
            ck_1 = chain.check(self, 1, run_time=0.6)
            vo.wait_until("authorization asks")
            self.play(Indicate(VGroup(g2.word, g2.question), color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("and IAM roles")
            ans2 = label("IAM roles allow it", 20, VENV).move_to(g2.question, aligned_edge=LEFT)
            chain.attach(self, ans2, anims=[swap_words(g2.question, ans2),
                                            Indicate(chain.padlock, color=VENV, scale_factor=1.3)],
                         run_time=0.8, into=g2)
            ck_2 = chain.check(self, 2, run_time=0.8)

        # ========================================================== 7 · three ways to get the error
        causes = [cause_badge(1, ["key not in this", "component's secrets/"]),
                  cause_badge(2, ["changed directory", "away from /app"]),
                  cause_badge(3, ["docker run from the", "wrong laptop folder"])]
        for c in causes:
            place(c, cx=chain.google_frame.get_center()[0], top=chain.google_frame.get_top()[1] - 0.15)
        note = footnote_card()
        place(note, cx=0, cy=CHAIN_Y)              # alone above the strip, once V5 has gone
        with self.voiceover(SAY[7]) as vo:
            chain.detach(self, tok, arrow, ck_1, ck_2,
                         extra=[FadeOut(cost), FadeOut(pin_line), FadeOut(chip_auth), FadeOut(adc)],
                         run_time=0.4)
            chain.hide(self, "google", run_time=0.35)
            chain.fail(self, run_time=0.5)
            chain.follow(self, run_time=1.0, found=False)
            vo.wait_until("The key isn't")
            self.play(FadeIn(causes[0], shift=DOWN * 0.1),
                      Indicate(VGroup(L36a.glyphs, L36b.glyphs), color=ERR, scale_factor=1.04), run_time=0.6)
            self.play(Indicate(chain.secrets, color=ERR, scale_factor=1.2), run_time=0.7)
            vo.wait_until("you changed directory")
            chain.unfollow(self, run_time=0.3)
            self.play(ReplacementTransform(causes[0], causes[1]), run_time=0.4)
            chain.unfail(self, run_time=0.5)
            reroot(self, chain, "/tmp", run_time=0.9)
            nothing = cross_mark(0.26, ERR).next_to(chain.root_label, RIGHT, buff=0.2)
            self.play(Create(nothing), run_time=0.4)
            vo.wait_until("or you ran docker run")
            self.play(FadeOut(nothing), ReplacementTransform(causes[1], causes[2]), run_time=0.4)
            reroot(self, chain, None, run_time=0.6)
            reaim(self, chain, "mega-pipeline/", run_time=0.8)
            self.play(Indicate(chain.window, color=LOOKUP, scale_factor=1.0),
                      Indicate(chain.folder, color=ERR, scale_factor=1.15), run_time=0.8)
        # the footnote is a different error: V5 leaves, the card stands alone above the strip
        self.wait(0.3)
        self.play(FadeOut(causes[2]), FadeOut(chain), FadeIn(note, shift=UP * 0.1), run_time=0.7)
        self.wait(1.0)
        self.play(Indicate(note[1][1], color=ERR, scale_factor=1.08), run_time=0.7)
        self.wait(1.0)

        # ========================================================== 8 · extra: the folders it made
        ls_rows = 12
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(note), caption_extra(tr), run_time=0.6)
            resize(self, t, ls_rows, run_time=0.7)
            c8 = type_cmd(self, t, LS_CMD, 1.2)
            assert hasattr(c8, "rows") and len(c8.rows) == 2, c8
            pin(self, c8, place(extra_tag(), left=c8.rows[-1].glyphs.get_right()[0] + 0.3,
                                cy=c8.rows[-1].strut.get_center()[1]), run_time=0.3)
            out8 = t.print(self, LS_OUT, run_time=0.7, lag=0.1)
            ia, tp, g01 = out8[0], out8[2], out8[4]
            vo.wait_until("input audios")
            b_ia = rbar(ia, S.GREY, 0.22)
            self.play(FadeIn(b_ia), run_time=0.3)
            stick(self, ia, b_ia, under=True)
            self.play(Indicate(ia.glyphs, color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("and text prompts")
            b_tp = rbar(tp, S.GREY, 0.22)
            self.play(FadeIn(b_tp), run_time=0.3)
            stick(self, tp, b_tp, under=True)
            vo.wait_until("with your group inside")
            sq = SurroundingRectangle(substring(g01, GROUP), color=S.GREY, buff=0.06, stroke_width=3)
            pin(self, g01, sq, run_time=0.5, anim=Create(sq))
            self.play(Indicate(substring(g01, GROUP), color=INK, scale_factor=1.2), run_time=0.6)

            panel = src_panel("transcribe_audio/cli.py", 33, 36)
            place(panel, left=-6.3, top=2.7)
            code = panel.code
            b0, b1 = line_bar(code, 0, S.GREY), line_bar(code, 1, S.GREY)
            bar_mk = Rectangle(width=b0.width, height=b0.get_top()[1] - b1.get_bottom()[1], stroke_width=0)
            bar_mk.set_fill(S.GREY, 0.2).move_to([b0.get_center()[0], (b0.get_top()[1] + b1.get_bottom()[1]) / 2, 0])
            bar_cl = line_bar(code, 3, LOOKUP, 0.2)
            note_mk = label("clear, then make the folders", 20, INK)     # INK: legible on the bar
            place(note_mk, left=code.code_lines[1].get_right()[0] + 0.5, cy=code.code_lines[1].get_center()[1])
            note_cl = label("the client", 20, LOOKUP)
            place(note_cl, left=code.code_lines[3].get_right()[0] + 0.5, cy=code.code_lines[3].get_center()[1])
            folders = laptop_folders()
            place(folders, left=-6.3, top=panel.get_bottom()[1] - 0.2)
            resize(self, t, 3, keep=[c8.rows[0], c8.rows[1], g01], run_time=0.7)
            assert folders.get_bottom()[1] > t.box.get_top()[1] + 0.1, folders.get_bottom()[1]
            self.play(FadeIn(folders, shift=UP * 0.1), FadeIn(panel, shift=DOWN * 0.1), run_time=0.6)
            self.play(Indicate(folders.rows, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("The code makes them")
            self.play(FadeIn(bar_mk), FadeIn(note_mk, shift=LEFT * 0.1), run_time=0.5)
            self.play(Indicate(code.code_lines[1], color=INK, scale_factor=1.1), run_time=0.6)
            vo.wait_until("before it builds the client")
            self.play(FadeIn(bar_cl), FadeIn(note_cl, shift=LEFT * 0.1), run_time=0.5)
        self.wait(0.8)

        # ========================================================== 9 · with your key, look for
        panel2 = src_panel("transcribe_audio/cli.py", 39, 43)
        place(panel2, cx=0, top=2.7)
        look = LookFor([("download", "line 30"),
                        ("one object name per recording: input_audios/…", "line 41"),
                        ("the audio files in input_audios/ on your laptop", "line 43")])
        cost2 = cost_tag()
        row_w = look.width + 0.4 + cost2.width
        place(look, left=-row_w / 2, top=panel2.get_bottom()[1] - 0.45)
        place(cost2, left=look.get_right()[0] + 0.4, cy=look.title.get_center()[1])
        assert cost2.get_right()[0] < EDGE + 0.01, cost2.get_right()[0]
        code2 = panel2.code
        b41 = line_bar(code2, 2, TURN, 0.2)
        b43 = line_bar(code2, 4, S.GREY, 0.22)
        chip_go = readme_chip("README.md · line 134")
        place(chip_go, right=EDGE, cy=BAND_Y)
        yt = your_turn()
        place(yt, right=chip_go.get_left()[0] - 0.25, cy=BAND_Y)
        assert yt.get_left()[0] > tr10_right + 0.15, (yt.get_left()[0], tr10_right)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(panel, bar_mk, bar_cl, note_mk, note_cl), shift=UP * 0.1),
                      FadeOut(folders), FadeOut(t), caption_extra(tr, False), run_time=0.6)
            self.play(FadeIn(panel2, shift=DOWN * 0.1), FadeIn(look), run_time=0.6)
            self.play(FadeIn(cost2, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("look for the word download")
            look.write_item(self, 0)
            vo.wait_until("one object name per recording")
            look.write_item(self, 1)
            self.play(FadeIn(b41), Indicate(code2.code_lines[2], color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("and the audio files appearing")
            look.write_item(self, 2)
            self.play(FadeIn(b43), Indicate(code2.code_lines[4], color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Pause, check your key")
            self.play(FadeIn(chip_go, shift=DOWN * 0.1), run_time=0.4)
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
            self.play(Wiggle(yt, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.6)
        self.wait(1.2)
        self.play(FadeOut(VGroup(tr, chip_go, yt, panel2, b41, b43, look, cost2)), run_time=0.8)
        self.wait(0.3)
