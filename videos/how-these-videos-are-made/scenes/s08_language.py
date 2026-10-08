"""S08 · Same video, second language.

Beats: the user's request for the Chinese versions (A06b, verbatim) in a PINK card, "sound weird"
underlined; a bilingual subtitle band (one real sentence pair of A27, drawn as a diagram of
"subtitles in both languages") -> the key rule: the band's two lines become the third row of the
real aligned entry (A27, tic-tac-toe i18n/zh/narration/g1.yaml lines 21-30): the English say line in
its three sentences on the left, the three Chinese sentences on the right, joined one to one by
GREY lines; "Flipped or turned" glows ORANGE, the ORANGE cue pin jumps to 翻转 and the file's anchor
line appears; counter "417 sentence pairs · both videos" -> the two columns fold into two outputs,
"English video" and "Chinese video", fed by one GREY "scene code" card; the real rule (A36,
docs/LANGUAGES.md) "The English video is never touched"; the English video splits into "English
render, before" and "after the Chinese edits"; a frame from each becomes a fingerprint (drawn: grey
squares), the two columns scroll through all 721 frames with a GREEN "=" on every row, and the
counter becomes the real result (A37) "tic-tac-toe scene 1, English 480p preview: all 721 frames
match"; dashed YELLOW footnote "a few scenes don't render exactly the same every time" -> the voice
bake-off (A28): the BLUE agent with S01's struck headphones asks a GREY speech recognizer; the
ORANGE "Mandarin voice 1 · zh-CN-XiaoxiaoNeural" flows in and comes out as noise -> "Nice",
epsilon -> "Excellent", Claude -> "Clark" (RED); "another voice" (zh-CN-XiaoyiNeural) flows in ->
GREEN "17 of 17 terms · 10 of 10 numbers" with the fuzzy-match footnote; the scoreboard (Brian, Ava,
Xiaoyi, Xiaoxiao), BLUE "chosen", the label becomes "the chosen voice"; dashed YELLOW "chosen by
speech recognition · no recorded check by ear yet" -> the Chinese tic-tac-toe video at 11:43: the
real picture (A04, 68d6c23) over a redrawn subtitle band with the OLD cue text (A30, as both QA
reviewers quoted it), tag "reconstruction · ..."; the English line ("No. ...") stays WHITE; the
Chinese line is glossed "It's not what a computer can do, not just counting games", RED "meaning
flipped" stamp; two faded-BLUE reviewers raise RED flags on the cue -> ponder (10 s): the frame
dims to 40 % except the two cue lines, the card sits above the band, and each line is circled as
the narration names it.

Waveforms here are drawings of "a voice" (DIAGRAM), not measured audio; the fingerprints are
drawn squares, not real hashes (only the 721 and the result line are real). Both say so on screen.

Continuity for S09 (which opens on the real A04 frame): the reconstructed frame here is the A04
picture cropped to FRAME_CROP, FRAME_W wide, its left edge at FRAME_X0, its top at FRAME_TOP, with
the redrawn band (subtitle_band, fill = the frame's own background) directly under it.

Every number and quote on screen is checked in _check() (runs on import) against the assets.

Helpers defined here (not in common.py): glyphs_of(), collect() (as in s05-s07, but a VGroup when it
can be, so FadeTransform works), zh_wrap() (Chinese line breaks after clause marks), en_wrap(),
sentence_box(), mini_video(), fingerprint(), equals(), fp_row(), voice_wave(), flag(),
recognizer_box(), heard_line().
"""

import numpy as np
import yaml
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.scene import VoiceScene
from explainer.voice import split_sentences

from common import (AGENT, AUDIO, BUG, CHINESE_REQUEST, EXCERPTS, INK, MEASURED, NARRATION, PANEL, QUOTES,
                    SUB_AGENT_TEXT, TOOL, USER, anchor_pin, asset, box, bug_tag, cant_hear_or_play, caption, dim,
                    emphasize, exhibit, fade_out_all, file_card, gloss, label, measured_badge, mono, open_outline,
                    ponder_drain, pulse, quote_card, recon_tag, role_icon, source_caption,
                    subtitle_band, video_player, waveform, zh)

SAY = NARRATION["S08"]
QUESTION = "The English is right.\nThe Chinese says the opposite.\nIs this a translation mistake?"

# ------------------------------------------------------------------ the real material (assets/)
A27, A28, A30, A36, A37 = EXCERPTS["A27"], EXCERPTS["A28"], EXCERPTS["A30"], EXCERPTS["A36"], EXCERPTS["A37"]
REQUEST = QUOTES["s08_chinese"]["screen"]           # verbatim (A06b)
ENTRY = yaml.safe_load(asset(A27["file"]).read_text(encoding="utf-8"))[0]
EN_SENTENCES = [s for _, s in split_sentences(ENTRY["en"])]      # the toolkit's own sentence splitter
ZH_SENTENCES = ENTRY["zh"]
ANCHOR_EN, ANCHOR_ZH = A27["anchor"]["en"], A27["anchor"]["zh"]   # "Flipped or turned" -> 翻转
PAIRS = A27["sentence_pairs"]                                     # 417 = 158 + 259
FRAMES = 721                                                      # A37: all 721 frames match
HEARD = A28["heard"]                                              # noise -> Nice, epsilon -> Excellent, ...
SCORES = [s.rsplit(" ", 1) for s in A28["scoreboard"].split(" · ")]
CHOSEN = "Xiaoyi (native Mandarin)"
CUE_OLD, CUE_EN = A30["before"], A30["english"]
GLOSS = A30["before_gloss"]
LANG_SRC = "docs/LANGUAGES.md, lines 8–9"

# the request card, broken into lines at spaces (the words stay exactly as written)
REQUEST_LINES = ["… there are a lot of terms that are derived", "from English and would thus sound weird",
                 "directly translate that into Chinese."]
BAND_PAIR = 2                                       # the sentence pair shown as the bilingual band


def _check():
    assert " ".join(REQUEST_LINES) == REQUEST
    assert REQUEST.startswith("… there are a lot of terms") and REQUEST.endswith("directly translate that into Chinese.")
    assert QUOTES["s08_chinese"]["caption"] == "chinese_request" and CHINESE_REQUEST.endswith("(request for the Chinese versions)")
    assert len(EN_SENTENCES) == 3 == len(ZH_SENTENCES), EN_SENTENCES
    assert EN_SENTENCES[2].startswith(ANCHOR_EN) and ANCHOR_ZH in ZH_SENTENCES[2]
    assert ENTRY["anchors"][ANCHOR_EN] == ANCHOR_ZH
    assert PAIRS == {"total": 417, "tictactoe": 158, "privacy": 259} and 158 + 259 == 417
    assert all(" " not in s for s in ZH_SENTENCES)
    assert A36["never_touched"] == "The English video is never touched"
    assert A36["never_touched_full"].startswith(A36["never_touched"] + ":")
    assert A37["screen"] == "tic-tac-toe scene 1, English 480p preview: all 721 frames match"
    assert "all 721 frames" in A37["text"] and A37["footnote"] == "a few scenes don't render exactly the same every time"
    assert A28["first_voice"] == "zh-CN-XiaoxiaoNeural" and A28["chosen_voice"] == "zh-CN-XiaoyiNeural"
    assert HEARD == [["noise", "Nice"], ["epsilon", "Excellent"], ["Claude", "Clark"]]
    assert A28["chosen_result"] == "17 of 17 terms · 10 of 10 numbers"
    assert A28["fuzzy_note"] == "a fuzzy match: 'Claude Shannon' came back as 'Cloud Shannon'"
    assert SCORES == [["Brian (male, English-first)", "0.997"], ["Ava (female, English-first)", "0.991–0.995"],
                      ["Xiaoyi (native Mandarin)", "0.991"], ["Xiaoxiao", "0.933"]]
    assert A30["before"] == "不是电脑能做的，不只是统计对局" and A30["english"] == "No. A computer can do more than count."
    assert A30["after"] == "不是。" + A30["before"][2:]          # the fix only puts back the full stop
    assert A30["recon_tag"] == "reconstruction · the old cue text, as both QA reviewers quoted it"
    assert A30["before_gloss"] == "It's not what a computer can do, not just counting games"
    asset("ttt_zh_1143.png")


_check()

# ------------------------------------------------------------------ layout
USER_AT = np.array([-5.25, 1.2, 0])
EN_X, EN_W, ZH_X, ZH_W = -3.1, 6.6, 3.75, 5.3      # the aligned entry: English left, Chinese right
HEAD_Y, ROWS_TOP, ROW_GAP, ROW_PAD = 2.95, 2.55, 0.28, 0.3
EN_SIZE, ZH_SIZE = 24, 24
PLAYER_Y, PLAYER_W, CODE_Y = 0.3, 2.3, 2.2      # beat 2: the scene code and its two outputs
HEADER_X, HEADER_Y, HEADER_W = 2.45, 1.78, 1.6   # the before / after renders
RULE_Y = 3.15
FP_TOP, FP_DY, FP_ROWS = 0.0, 0.56, 4           # fingerprint rows (top row centre, step, rows shown)
FP_X, FP_W, FP_H = 2.45, 2.6, 0.4
BADGE_Y, FOOT_Y = -2.3, -3.0
ROW1_Y, ROW2_Y = 0.65, -1.25         # beat 3: the two voices
REC_X = -0.8
FRAME_CROP = (120, 20, 1800, 920)    # the A04 picture (1920 x 1080; its band is redrawn below it)
FRAME_W, FRAME_X0, FRAME_TOP = 7.6, -6.35, 2.75
FRAME_BG = "#0D0E13"                 # the frame's own background colour (sampled)


# ------------------------------------------------------------------ helpers (this scene only)
def glyphs_of(t: Text, s: str, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of substring `sub` in a Text built from string s (whitespace and line breaks have
    no glyphs, so `sub` may run across a line break)."""
    flat, want = "".join(s.split()), "".join(sub.split())
    assert len(t.submobjects) == len(flat), (len(t.submobjects), len(flat), s)
    start = -1
    for _ in range(occurrence + 1):
        start = flat.find(want, start + 1)
    assert start >= 0, (sub, s)
    return VGroup(*t[start:start + len(want)])


def collect(scene, *mobs) -> Group:
    """Make several on-screen things ONE top-level group (each thing's whole family leaves the top
    level first, so no part that came on screen by itself stays behind)."""
    for m in mobs:
        scene.remove(*m.get_family())
    g = VGroup(*mobs) if all(isinstance(m, VMobject) for m in mobs) else Group(*mobs)
    scene.add(g)
    return g


def zh_wrap(s: str, n: int) -> str:
    """Break a Chinese sentence into lines of at most n characters, preferably after a clause
    mark (，、：；), never leaving a line that starts with punctuation."""
    clauses, cur = [], ""
    for ch in s:
        cur += ch
        if ch in "，、：；":
            clauses.append(cur)
            cur = ""
    if cur:
        clauses.append(cur)
    lines, line = [], ""
    for c in clauses:
        while len(c) > n:                       # a clause longer than a line: hard split
            if line:
                lines.append(line)
                line = ""
            lines.append(c[:n])
            c = c[n:]
        if len(line) + len(c) <= n:
            line += c
        else:
            lines.append(line)
            line = c
    if line:
        lines.append(line)
    for k in range(1, len(lines)):              # no line starts with punctuation
        while lines[k] and lines[k][0] in "，。、：；！？”）":
            lines[k - 1] += lines[k][0]
            lines[k] = lines[k][1:]
    return "\n".join(x for x in lines if x)


def en_wrap(s: str, n: int) -> str:
    import textwrap
    return "\n".join(textwrap.wrap(s, n, break_long_words=False, break_on_hyphens=False))


def sentence_box(t, width: float, height: float) -> VGroup:
    """One sentence of the aligned entry: the text on a dark GREY card. .box .text"""
    b = box(width, height, TOOL, fill=PANEL, fill_opacity=1, radius=0.12, stroke=2)
    t.move_to(b).align_to(b, LEFT).shift(RIGHT * 0.22)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def mini_video(lang: str, width: float = PLAYER_W) -> VGroup:
    """A small GREY player with a language mark on its screen ('EN' or 中). .player .mark"""
    p = video_player(width, progress=0.35)
    mark = (S.text("EN", 34, S.GREY, font=S.FONT_SANS, weight="BOLD") if lang == "en" else zh("中", 40, S.GREY))
    mark.move_to(p.screen)
    g = VGroup(p, mark)
    g.player, g.mark = p, mark
    return g


def fingerprint(f: int, width: float = FP_W, height: float = FP_H) -> VGroup:
    """A frame's fingerprint, drawn (a diagram, not a real hash): 12 grey squares whose shades
    depend only on the frame number, so the same frame always gives the same pattern."""
    rng = np.random.default_rng(7000 + f)
    n = 12
    b = box(width, height, TOOL, fill=PANEL, fill_opacity=1, radius=0.08, stroke=2)
    side = min(height - 0.14, (width - 0.3) / n - 0.04)
    cells = VGroup(*[Square(side, stroke_width=0).set_fill(interpolate_color(ManimColor(S.GREY_DARK),
                                                                               ManimColor(INK), v), 1)
                     for v in rng.uniform(0.0, 1.0, n)])
    cells.arrange(RIGHT, buff=(width - 0.3 - n * side) / (n - 1)).move_to(b)
    return VGroup(b, cells)


def equals(width: float = 0.3, color: str = MEASURED, stroke: float = 5) -> VGroup:
    return VGroup(*[Line(LEFT * width / 2, RIGHT * width / 2, color=color, stroke_width=stroke).shift(UP * dy)
                    for dy in (0.07, -0.07)])


def fp_row(f: int) -> VGroup:
    """Frame f in both renders: the same fingerprint on the left and the right, a GREEN '=' between."""
    return VGroup(fingerprint(f).move_to([-FP_X, 0, 0]), equals(), fingerprint(f).move_to([FP_X, 0, 0]))


def voice_wave(seed: int, width: float = 4.1, height: float = 0.62) -> VMobject:
    """A drawing of a voice (DIAGRAM): bursts like syllables, with short gaps. Not measured audio."""
    rng = np.random.default_rng(seed)
    n = 150
    env = np.zeros(n)
    i = 2
    while i < n - 6:
        w = int(rng.integers(5, 11))
        a = rng.uniform(0.45, 1.0)
        env[i:i + w] += a * np.sin(np.linspace(0, PI, w)) ** 0.8
        i += w + int(rng.integers(0, 4))
    env = np.clip(env + rng.uniform(0, 0.08, n), 0, None)
    return waveform(env, width=width, height=height, color=AUDIO, step=1, gamma=0.8)


def flag(height: float = 0.75, color: str = BUG) -> VGroup:
    """A raised flag: a pole and a RED pennant. .pole .cloth"""
    pole = Line(ORIGIN, UP * height, color=SUB_AGENT_TEXT, stroke_width=3)
    cloth = Polygon(pole.get_end(), pole.get_end() + np.array([0.42, -0.12, 0]), pole.get_end() + DOWN * 0.26,
                    stroke_width=0).set_fill(color, 1)
    g = VGroup(pole, cloth)
    g.pole, g.cloth = pole, cloth
    return g


def recognizer_box(height: float = 3.1, width: float = 2.35) -> VGroup:
    """The GREY speech recognizer: audio in (ORANGE bars), words out. .box .name"""
    b = box(width, height, TOOL, fill=PANEL, fill_opacity=1, radius=0.18)
    name = label("speech\nrecognizer", 28, INK, line_spacing=0.9)
    bars = VGroup(*[RoundedRectangle(width=0.07, height=h, corner_radius=0.03, stroke_width=0).set_fill(AUDIO, 1)
                    for h in (0.16, 0.34, 0.24, 0.4, 0.2)]).arrange(RIGHT, buff=0.05)
    arrow = Arrow(LEFT * 0.22, RIGHT * 0.22, buff=0, color=TOOL, stroke_width=3, tip_length=0.12,
                  max_tip_length_to_length_ratio=0.5)
    abc = label("abc", 24, INK)
    icon = VGroup(bars, arrow, abc).arrange(RIGHT, buff=0.1)
    VGroup(icon, name).arrange(DOWN, buff=0.28).move_to(b)
    g = VGroup(b, icon, name)
    g.box, g.name = b, name
    return g


def heard_line(said: str, heard: str, size: float = 26) -> VGroup:
    """'noise → “Nice”': what the script said (WHITE), what the recognizer heard (RED). .said .arrow .heard"""
    a, arr, b = label(said, size, INK), label("→", size, TOOL), label("“" + heard + "”", size, BUG)
    g = VGroup(a, arr, b).arrange(RIGHT, buff=0.16)
    g.said, g.arrow, g.heard = a, arr, b
    return g


class SecondLanguage(VoiceScene):
    def construct(self):
        # ---------------------------------------------------------- beat 1: the request, and the key rule
        user = role_icon("user", 1.15).move_to(USER_AT)
        user_l = label("the user", 24, USER).next_to(user, DOWN, buff=0.2)
        req = quote_card("\n".join(REQUEST_LINES), CHINESE_REQUEST, size=28, chars=80)
        req.next_to(user, RIGHT, buff=0.45).match_y(user).shift(UP * 0.1)
        weird = glyphs_of(req.quote, req.quote.original_text, "sound weird")
        weird_line = Line(weird.get_corner(DL) + DOWN * 0.07, weird.get_corner(DR) + DOWN * 0.07,
                          color=S.WHITE, stroke_width=3)

        band = subtitle_band(ZH_SENTENCES[BAND_PAIR], EN_SENTENCES[BAND_PAIR], width=8.6, zh_size=28,
                             en_size=22, fill=PANEL)
        band.move_to([0.3, -1.45, 0])
        band_frame = Rectangle(width=band.band.width, height=band.band.height, stroke_color=TOOL, stroke_width=2)
        band_frame.move_to(band.band)
        band_cap = caption("subtitles in both languages", 22).next_to(band, DOWN, buff=0.14)

        # the aligned entry (A27): one English say line, three sentences; one Chinese sentence each
        en_txt = [label(en_wrap(s, 41), EN_SIZE, INK, line_spacing=0.95) for s in EN_SENTENCES]
        zh_txt = [zh(zh_wrap(s, 16), ZH_SIZE, INK, line_spacing=0.95) for s in ZH_SENTENCES]
        for t, w in [(t, EN_W) for t in en_txt] + [(t, ZH_W) for t in zh_txt]:
            assert t.width <= w - 0.44 + 1e-6, (t.width, w)
        rows_h = [max(a.height, b.height) + ROW_PAD for a, b in zip(en_txt, zh_txt)]
        en_box, zh_box = VGroup(), VGroup()
        y = ROWS_TOP
        for a, b, h in zip(en_txt, zh_txt, rows_h):
            en_box.add(sentence_box(a, EN_W, h).move_to([EN_X, y - h / 2, 0]))
            zh_box.add(sentence_box(b, ZH_W, h).move_to([ZH_X, y - h / 2, 0]))
            a.move_to(en_box[-1].box).align_to(en_box[-1].box, LEFT).shift(RIGHT * 0.22)
            b.move_to(zh_box[-1].box).align_to(zh_box[-1].box, LEFT).shift(RIGHT * 0.22)
            y -= h + ROW_GAP
        links = VGroup(*[Line(e.box.get_right(), z.box.get_left(), color=TOOL, stroke_width=3)
                         for e, z in zip(en_box, zh_box)])
        nums = VGroup(*[caption(str(k + 1), 20).next_to(links[k], UP, buff=0.06) for k in range(3)])
        head_en = label("English say line · 3 sentences", 24, TOOL).move_to([EN_X, HEAD_Y, 0])
        head_zh = label("Chinese · one sentence each", 24, TOOL).move_to([ZH_X, HEAD_Y, 0]).align_to(head_en, UP)
        entry_src = source_caption("real aligned entry · tic-tac-toe video, i18n/zh/narration/g1.yaml, lines 21–30")
        assert en_box.get_bottom()[1] > -2.45, en_box.get_bottom()

        anchor_en = glyphs_of(en_txt[2], en_txt[2].original_text, ANCHOR_EN)
        anchor_zh = glyphs_of(zh_txt[2], zh_txt[2].original_text, ANCHOR_ZH)
        pin = VGroup(anchor_pin(AUDIO, 0.36), label("cue", 22, AUDIO))
        pin[1].next_to(pin[0], RIGHT, buff=0.08).shift(UP * 0.06)
        flipped = glyphs_of(en_txt[2], en_txt[2].original_text, "Flipped")
        pin.shift(flipped.get_top() + UP * 0.04 - pin[0].get_bottom())
        pin.shift(RIGHT * (flipped.get_x() - pin[0].get_x()))
        pin_zh_at = pin.get_center() + np.array([anchor_zh.get_x() - pin[0].get_x(),
                                                 anchor_zh.get_top()[1] + 0.04 - pin[0].get_bottom()[1], 0])

        count = DecimalNumber(PAIRS["total"], num_decimal_places=0, font_size=34, color=INK)
        count_l = label("sentence pairs · both videos", 24, INK)
        count_g = VGroup(count, count_l).arrange(RIGHT, buff=0.16, aligned_edge=DOWN)
        count_b = box(count_g.width + 0.5, count_g.height + 0.3, TOOL, fill=PANEL, fill_opacity=1)
        count_g.move_to(count_b)
        counter = VGroup(count_b, count_g).move_to([0, -2.8, 0]).align_to([6.45, 0, 0], RIGHT)
        count.set_value(0)
        count.add_updater(lambda m: m.next_to(count_l, LEFT, buff=0.16).align_to(count_l, DOWN))
        assert counter.get_top()[1] < en_box.get_bottom()[1] - 0.08

        # the anchor as the file writes it: "Flipped or turned": "翻转"
        a_key = label("anchors:", 22, TOOL)
        a_en = mono(f'"{ANCHOR_EN}":', 22, AUDIO)
        a_zh = VGroup(mono('"', 22, AUDIO), zh(ANCHOR_ZH, 24, AUDIO), mono('"', 22, AUDIO)).arrange(RIGHT, buff=0.04)
        a_line = VGroup(a_key, a_en, a_zh).arrange(RIGHT, buff=0.16)
        a_zh[1].align_to(a_en, DOWN).shift(DOWN * 0.03)
        a_box = box(a_line.width + 0.44, a_line.height + 0.26, TOOL, fill=PANEL, fill_opacity=1)
        a_line.move_to(a_box)
        anchor_chip = VGroup(a_box, a_line).move_to([0, -2.8, 0]).align_to([-6.4, 0, 0], LEFT)
        assert anchor_chip.get_right()[0] < counter.get_left()[0] - 0.2

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(user, shift=UP * 0.2), FadeIn(user_l), run_time=0.7)
            vo.wait_until("The user asked")
            self.play(FadeIn(req, shift=RIGHT * 0.25), run_time=0.9)
            vo.wait_until("that would sound weird")
            self.play(Create(weird_line), run_time=0.6)
            vo.wait_until("with subtitles")
            self.play(FadeIn(band.band), Create(band_frame), FadeIn(band.zh, shift=UP * 0.1),
                      FadeIn(band.en, shift=UP * 0.1), FadeIn(band_cap), run_time=0.9)
            self.play(Indicate(band.zh, color=S.WHITE, scale_factor=1.04), run_time=0.6)
            self.play(Indicate(band.en, color=S.WHITE, scale_factor=1.04), run_time=0.6)

            vo.wait_until("The key rule")
            self.add(en_box[2].box, zh_box[2].box)
            self.bring_to_back(en_box[2].box, zh_box[2].box)       # the cards go under the texts
            self.play(FadeOut(collect(self, user, user_l, req, weird_line), shift=UP * 0.3),
                      FadeOut(collect(self, band.band, band_frame, band_cap)),
                      ReplacementTransform(band.en, en_txt[2]), ReplacementTransform(band.zh, zh_txt[2]),
                      FadeIn(en_box[2].box), FadeIn(zh_box[2].box), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(VGroup(en_box[k].box, en_txt[k]), shift=DOWN * 0.15) for k in (0, 1)],
                                  lag_ratio=0.25), FadeIn(head_en), FadeIn(entry_src), run_time=0.8)
            vo.wait_until("one Chinese sentence")
            self.play(LaggedStart(*[FadeIn(VGroup(zh_box[k].box, zh_txt[k]), shift=LEFT * 0.2) for k in (0, 1)],
                                  lag_ratio=0.25), FadeIn(head_zh), run_time=0.8)
            vo.wait_until("for each English")
            self.play(LaggedStart(*[AnimationGroup(Create(links[k]), FadeIn(nums[k])) for k in range(3)],
                                  lag_ratio=0.35), run_time=1.2)

            vo.wait_until("so every animation cue")
            self.play(anchor_en.animate.set_color(AUDIO), FadeIn(pin, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("still has a sentence")
            self.play(pin.animate(path_arc=-PI / 2.2).move_to(pin_zh_at), FadeIn(anchor_chip, shift=UP * 0.15),
                      run_time=0.8)
            self.play(anchor_zh.animate.set_color(AUDIO), Flash(anchor_zh, color=AUDIO, line_length=0.15,
                                                                flash_radius=0.4), run_time=0.5)
            self.play(FadeIn(counter, shift=UP * 0.15), run_time=0.3)
            self.play(ChangeDecimalToValue(count, PAIRS["total"]), run_time=0.9, rate_func=smooth)
        count.clear_updaters()

        # ---------------------------------------------------------- beat 2: the English video is never touched
        en_vid = mini_video("en").move_to([-3.4, PLAYER_Y, 0])
        zh_vid = mini_video("zh").move_to([3.4, PLAYER_Y, 0])
        en_vid_l = label("English video", 26, INK).next_to(en_vid, DOWN, buff=0.18)
        zh_vid_l = label("Chinese video", 26, INK).next_to(zh_vid, DOWN, buff=0.18)
        code = file_card("scenes/*.py", "the same scene code").move_to([0, CODE_Y, 0])
        feeds = VGroup(*[Arrow(code.box.get_bottom() + side * 0.6, v.get_top() + UP * 0.08 - side * 0.3, buff=0,
                               color=TOOL, stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.25)
                         for side, v in ((LEFT, en_vid), (RIGHT, zh_vid))])
        rule_t = label("“" + A36["never_touched"] + "”", 26, INK)
        rule_b = box(rule_t.width + 0.6, rule_t.height + 0.3, TOOL, fill=PANEL, fill_opacity=1)
        rule_t.move_to(rule_b)
        rule_c = caption(LANG_SRC, 20)
        rule = VGroup(rule_b, rule_t)
        rule_top = VGroup(rule, rule_c).arrange(RIGHT, buff=0.25).move_to([0, RULE_Y, 0])
        assert rule_b.get_bottom()[1] > code.get_top()[1] + 0.08

        before = mini_video("en", HEADER_W).move_to([-HEADER_X, HEADER_Y, 0])
        after = mini_video("en", HEADER_W).move_to([HEADER_X, HEADER_Y, 0])
        before_l = label("English render, before", 24, INK).next_to(before, DOWN, buff=0.12)
        after_l = label("after the Chinese edits", 24, INK).next_to(after, DOWN, buff=0.12)
        assert before_l.get_bottom()[1] > FP_TOP + FP_H / 2 + 0.1

        rows0 = VGroup(*[fp_row(f).move_to([0, FP_TOP - j * FP_DY, 0]) for j, f in enumerate(range(FP_ROWS))])
        fp_gloss = gloss("fingerprint:\na short code\nmade from all\nof a frame's\npixels (drawn)", rows0[0][2], RIGHT,
                         size=22, length=0.45)
        fp_gloss.text.align_to(rows0[0][2], UP).shift(UP * 0.12)
        assert fp_gloss.get_right()[0] < 6.45
        scroll = ValueTracker(0.0)
        n_seen = DecimalNumber(FP_ROWS, num_decimal_places=0, font_size=40, color=INK)
        seen_l = label("frames compared", 22, TOOL)
        seen = VGroup(n_seen, seen_l).arrange(DOWN, buff=0.1).move_to([-5.3, FP_TOP - 0.85, 0])

        def keep_count(m):
            m.set_value(min(FRAMES, int(np.floor(scroll.get_value())) + FP_ROWS))
            m.next_to(seen_l, UP, buff=0.1)
        badge = measured_badge(A37["screen"], 24).move_to([0, BADGE_Y, 0])
        foot_t = label(A37["footnote"], 22, INK)
        foot = VGroup(open_outline(foot_t, buff=0.16), foot_t).move_to([2.4, FOOT_Y, 0])
        fp_src = source_caption("real result · frame-check run record")
        assert fp_src.get_right()[0] < foot.get_left()[0] - 0.2, (fp_src.get_right(), foot.get_left(), foot.width)

        def window(y: float) -> float:
            """Opacity of a fingerprint row at height y: the rows fade in and out at the window edges."""
            top, bot = FP_TOP + FP_DY * 0.5, FP_TOP - (FP_ROWS - 0.5) * FP_DY
            return float(np.clip(min(top - y, y - bot) / (FP_DY * 0.5), 0, 1))

        def rows_at():
            s = scroll.get_value()
            k0 = int(np.floor(s))
            g = VGroup()
            for j in range(FP_ROWS + 1):
                f = k0 + j
                if f >= FRAMES:
                    break
                y = FP_TOP - (j - (s - k0)) * FP_DY
                op = window(y)
                if op <= 0.01:
                    continue
                row = fp_row(f).move_to([0, y, 0])
                if op < 1:
                    row.fade(1 - op)
                g.add(row)
            return g

        with self.voiceover(SAY[1]) as vo:
            gone = collect(self, links, nums, pin, head_en, head_zh, counter, anchor_chip, entry_src)
            left_col = collect(self, *[VGroup(en_box[k].box, en_txt[k]) for k in range(3)])
            right_col = collect(self, *[VGroup(zh_box[k].box, zh_txt[k]) for k in range(3)])
            self.play(FadeOut(gone), FadeTransform(left_col, en_vid), FadeTransform(right_col, zh_vid), run_time=1.0)
            self.play(FadeIn(en_vid_l), FadeIn(zh_vid_l), FadeIn(code, shift=DOWN * 0.2), run_time=0.6)
            self.play(LaggedStart(*[GrowArrow(a) for a in feeds], lag_ratio=0.3), run_time=0.7)

            vo.wait_until("so the agent checks")
            self.play(FadeIn(rule_top, shift=DOWN * 0.15), *dim(zh_vid, zh_vid_l, feeds[1], opacity=0.35),
                      run_time=0.7)
            self.play(Circumscribe(en_vid, color=S.WHITE, buff=0.08, run_time=0.9))

            vo.wait_until("the English video didn't")
            out2 = collect(self, code, feeds, zh_vid, zh_vid_l)
            self.play(FadeOut(out2), ReplacementTransform(en_vid, before), FadeOut(en_vid_l), run_time=0.8)
            self.play(TransformFromCopy(before, after, path_arc=-PI / 4), FadeIn(before_l), FadeIn(after_l),
                      run_time=0.7)

            vo.wait_until("It compares")             # a frame from each render becomes its fingerprint
            shots = [Rectangle(width=v.player.screen.width * 0.8, height=v.player.screen.height * 0.8, stroke_color=INK,
                               stroke_width=2).set_fill(S.GREY_DARK, 0.6).move_to(v.player.screen) for v in (before, after)]
            self.add(*shots)
            self.play(ReplacementTransform(shots[0], rows0[0][0]), ReplacementTransform(shots[1], rows0[0][2]),
                      run_time=0.7)
            self.play(GrowFromCenter(rows0[0][1]), GrowArrow(fp_gloss.arrow), FadeIn(fp_gloss.text), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.12) for r in rows0[1:]], lag_ratio=0.3),
                      FadeIn(seen), FadeIn(fp_src), run_time=0.6)
            # scroll through all 721 frames
            self.remove(*rows0.get_family())
            live = always_redraw(rows_at)
            self.add(live)
            n_seen.add_updater(keep_count)
            self.play(scroll.animate.set_value(FRAMES - FP_ROWS),
                      run_time=vo.until("A few scenes", 2.2), rate_func=rate_functions.ease_in_out_sine)
            live.clear_updaters()
            n_seen.clear_updaters()
            n_seen.set_value(FRAMES).next_to(seen_l, UP, buff=0.1)
            self.play(ReplacementTransform(seen, badge), FadeOut(fp_gloss), run_time=0.6)
            self.play(Create(foot[0]), FadeIn(foot_t), run_time=0.8)
            vo.wait_until("but most match")
            self.play(emphasize(badge, run_time=0.9))

        # ---------------------------------------------------------- beat 3: which voice?
        agent = role_icon("agent", 0.95).move_to([-5.75, 2.65, 0])
        ears = cant_hear_or_play(0.55)[0].next_to(agent, RIGHT, buff=0.35).shift(UP * 0.05)
        rec = recognizer_box().move_to([REC_X, (ROW1_Y + ROW2_Y) / 2, 0])
        asked = DashedLine(ears.get_right() + RIGHT * 0.15, rec.box.get_top() + LEFT * 0.4 + UP * 0.06,
                           color=TOOL, stroke_width=3, dash_length=0.1)
        asked.add_tip(tip_length=0.15, tip_width=0.15)
        wave_x = -4.3
        w1, w2 = (voice_wave(3, 3.9).move_to([wave_x, ROW1_Y, 0]), voice_wave(11, 3.9).move_to([wave_x, ROW2_Y, 0]))
        v1 = VGroup(label("Mandarin voice 1", 26, AUDIO), mono(A28["first_voice"], 20, TOOL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08)
        v1.next_to(w1, UP, buff=0.18).align_to(w1, LEFT)
        v2_name = label("another voice", 26, AUDIO)
        v2_chosen = label("the chosen voice", 26, AUDIO)
        v2_id = mono(A28["chosen_voice"], 20, TOOL)
        v2 = VGroup(v2_name, v2_id).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        v2.next_to(w2, UP, buff=0.18).align_to(w2, LEFT)
        v2_chosen.move_to(v2_name, aligned_edge=LEFT)
        into = [np.array([rec.box.get_left()[0] + 0.05, y, 0]) for y in (ROW1_Y, ROW2_Y)]

        heard = VGroup(*[heard_line(a, b) for a, b in HEARD]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        for h in heard:                                   # the arrows in one column
            h.shift(RIGHT * (heard[0].arrow.get_x() - h.arrow.get_x()))
        heard_cap = caption("script word → what the recognizer heard", 20)
        heard_body = VGroup(heard_cap, heard).arrange(DOWN, buff=0.16, aligned_edge=LEFT)
        out1_b = box(heard_body.width + 0.5, heard_body.height + 0.36, TOOL, fill=PANEL, fill_opacity=1)
        heard_body.move_to(out1_b)
        out1 = VGroup(out1_b, heard_body).move_to([0, ROW1_Y, 0]).align_to(rec.box, LEFT).shift(
            RIGHT * (rec.box.width + 0.5))
        out1_a = Arrow(rec.box.get_right() * np.array([1, 0, 0]) + UP * ROW1_Y, out1_b.get_left() * np.array([1, 0, 0])
                       + UP * ROW1_Y, buff=0.05, color=TOOL, stroke_width=3, tip_length=0.15)
        result = measured_badge(A28["chosen_result"], 22)
        fuzzy = caption(A28["fuzzy_note"].replace(" came back", "\ncame back"), 20)
        out2_body = VGroup(result, fuzzy).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        out2_body.move_to([0, ROW2_Y - 0.22, 0]).align_to(out1_b, LEFT)
        out2_a = Arrow(rec.box.get_right() * np.array([1, 0, 0]) + UP * result.get_y(),
                       result.get_left() * np.array([1, 0, 0]) + UP * result.get_y(), buff=0.05, color=TOOL,
                       stroke_width=3, tip_length=0.15)

        board_rows = VGroup()
        for name, score in SCORES:
            n_t = label(name, 20, INK if name == CHOSEN else S.GREY)
            s_t = label(score, 20, INK if name == CHOSEN else S.GREY)
            board_rows.add(VGroup(n_t, s_t))
        name_w = max(r[0].width for r in board_rows)
        for k, r in enumerate(board_rows):
            r[0].move_to([0, -k * 0.34, 0], aligned_edge=LEFT)
            r[1].move_to([name_w + 0.35, -k * 0.34, 0], aligned_edge=LEFT)
        board_head = caption("bake-off scores, from the speech recognizer", 20)
        board = VGroup(board_head, board_rows).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        board.move_to([0, 2.74, 0]).align_to([6.45, 0, 0], RIGHT)
        chosen_row = board_rows[[n for n, _ in SCORES].index(CHOSEN)]
        chosen_box = SurroundingRectangle(chosen_row, color=AGENT, buff=0.06, stroke_width=2.5, corner_radius=0.06)
        chosen_l = label("chosen", 22, AGENT).next_to(chosen_box, LEFT, buff=0.15)
        verdict_t = label("chosen by speech recognition · no recorded check by ear yet", 24, INK)
        verdict = VGroup(open_outline(verdict_t, buff=0.16), verdict_t).move_to([0.4, -2.85, 0])
        bake_src = source_caption("real results · Chinese voice bake-off (workflow run record, commit 875166f) · "
                                  "waveforms drawn")
        assert out1.get_top()[1] < board.get_bottom()[1] - 0.12, (out1.get_top(), board.get_bottom())
        assert fuzzy.get_bottom()[1] > verdict.get_top()[1] + 0.12
        assert verdict.get_bottom()[1] > bake_src.get_top()[1] + 0.05

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(collect(self, *self.mobjects)), run_time=0.6)
            self.play(FadeIn(w1, shift=RIGHT * 0.2), FadeIn(v1), run_time=0.5)
            self.play(FadeIn(w2, shift=RIGHT * 0.2), FadeIn(v2), run_time=0.5)
            vo.wait_until("The agent can't listen")
            self.play(FadeIn(agent, shift=UP * 0.15), FadeIn(ears[0]), run_time=0.6)
            self.play(Create(ears[1]), run_time=0.4)
            vo.wait_until("so it asked")
            self.play(FadeIn(rec, scale=0.9), Create(asked), FadeIn(bake_src), run_time=0.9)

            vo.wait_until("With the first")
            self.play(Indicate(v1[0], color=S.WHITE, scale_factor=1.06), run_time=0.6)
            flow = w1.copy()                       # the voice flows in; a faint copy stays by its label
            self.play(flow.animate(rate_func=rate_functions.ease_in_sine).stretch_to_fit_width(0.05)
                      .move_to(into[0]).set_opacity(0.2), w1.animate.set_opacity(0.3), run_time=0.9)
            self.remove(flow)
            self.play(pulse(rec.box, 1.04, run_time=0.4))
            self.play(GrowArrow(out1_a), FadeIn(out1_b, shift=RIGHT * 0.2), FadeIn(heard_cap), run_time=0.6)
            vo.wait_until("the recognizer heard")
            self.play(FadeIn(heard[0], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(heard[0].heard, color=S.WHITE, scale_factor=1.12), run_time=0.6)
            vo.wait_until("and \"Excellent\"")
            self.play(FadeIn(heard[1], shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(heard[1].heard, color=S.WHITE, scale_factor=1.12), run_time=0.6)
            self.play(FadeIn(heard[2], shift=RIGHT * 0.15), run_time=0.5)

            vo.wait_until("Another voice")
            flow = w2.copy()
            self.play(flow.animate(rate_func=rate_functions.ease_in_sine).stretch_to_fit_width(0.05)
                      .move_to(into[1]).set_opacity(0.2), w2.animate.set_opacity(0.3), run_time=0.8)
            self.remove(flow)
            self.play(pulse(rec.box, 1.04, run_time=0.4))
            self.play(GrowArrow(out2_a), FadeIn(result, shift=RIGHT * 0.2), run_time=0.6)
            self.play(FadeIn(fuzzy, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and was chosen")
            self.play(FadeIn(board, shift=DOWN * 0.15), run_time=0.6)
            self.play(Create(chosen_box), FadeIn(chosen_l, shift=RIGHT * 0.1),
                      ReplacementTransform(v2_name, v2_chosen), run_time=0.7)
            vo.wait_until("There's no record")
            self.play(Create(verdict[0]), FadeIn(verdict_t), run_time=0.8)
            self.play(Circumscribe(ears, color=S.WHITE, buff=0.1, run_time=1.0))

        # ---------------------------------------------------------- beat 4: one subtitle flipped a meaning
        pic = exhibit("ttt_zh_1143.png", width=FRAME_W, crop=FRAME_CROP)
        pic.move_to([FRAME_X0 + FRAME_W / 2, FRAME_TOP - pic.height / 2, 0])
        pic.remove(pic.frame)
        cue = subtitle_band(CUE_OLD, CUE_EN, width=FRAME_W, zh_size=30, en_size=24, fill=FRAME_BG)
        cue.en.set_color(INK)                                 # the English line stays WHITE
        cue.next_to(pic.image, DOWN, buff=0)
        frame = Rectangle(width=FRAME_W, height=pic.image.height + cue.height, stroke_color=TOOL, stroke_width=2)
        frame.move_to(Group(pic.image, cue.band))
        rtag = recon_tag(A30["recon_tag"]).next_to(frame, UP, buff=0.12).align_to(frame, LEFT)
        pic_src = source_caption("picture: real frame of the Chinese tic-tac-toe video at 11:43 · subtitle band redrawn")
        no_m = glyphs_of(cue.en, CUE_EN, "No.")
        rest_m = glyphs_of(cue.en, CUE_EN, "A computer can do more than count.")
        assert rtag.get_top()[1] < 3.55 and frame.get_bottom()[1] > pic_src.get_top()[1] + 0.3

        gl_head = caption("the Chinese line says:", 22)
        gl_text = label("“" + GLOSS.replace("computer can", "computer\ncan").replace("just counting", "just\ncounting")
                        + "”", 26, INK, line_spacing=0.95)
        gl_body = VGroup(gl_head, gl_text).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        gl_box = box(gl_body.width + 0.5, gl_body.height + 0.4, TOOL, fill=PANEL, fill_opacity=1)
        gl_body.move_to(gl_box)
        gl_card = VGroup(gl_box, gl_body).move_to([4.1, 1.45, 0])
        gl_arrow = Arrow(gl_box.get_corner(DL) + RIGHT * 0.45, cue.zh.get_corner(UR) + np.array([-0.2, 0.05, 0]),
                         buff=0.08, color=TOOL, stroke_width=3, tip_length=0.16, max_tip_length_to_length_ratio=0.15)
        stamp = bug_tag("meaning flipped", 28).rotate(8 * DEGREES).move_to(gl_box.get_bottom() + np.array([0.8, -0.1, 0]))
        assert gl_card.get_right()[0] < 6.5 and gl_card.get_left()[0] > frame.get_right()[0] + 0.2

        revs = VGroup(role_icon("sub", 0.9), role_icon("sub", 0.9)).arrange(RIGHT, buff=0.95).move_to([4.25, -1.45, 0])
        flags = VGroup(*[flag().next_to(r.person, LEFT, buff=-0.05).align_to(r.person, DOWN).shift(UP * 0.35)
                         for r in revs])
        revs_l = label("both AI reviewers of\nthe Chinese version", 22, SUB_AGENT_TEXT, line_spacing=0.9)
        revs_l.next_to(revs, DOWN, buff=0.22)
        zh_line = Line(cue.zh.get_corner(DL) + DOWN * 0.06, cue.zh.get_corner(DR) + DOWN * 0.06, color=BUG,
                       stroke_width=4)
        assert revs_l.get_bottom()[1] > -3.25 and stamp.get_bottom()[1] > revs.get_top()[1] + 0.4

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(collect(self, *self.mobjects)), run_time=0.6)
            self.play(FadeIn(pic), FadeIn(cue.band), Create(frame), run_time=0.9)
            self.play(FadeIn(cue.zh, shift=UP * 0.08), FadeIn(cue.en, shift=UP * 0.08), FadeIn(rtag, shift=DOWN * 0.1),
                      FadeIn(pic_src), run_time=0.7)
            vo.wait_until("The English narration")
            self.play(Circumscribe(cue.en, color=S.WHITE, buff=0.08, run_time=1.1))
            vo.wait_until("with a short no")
            self.play(Indicate(no_m, color=S.WHITE, scale_factor=1.3), run_time=0.7)
            vo.wait_until("then says a computer")
            self.play(Indicate(rest_m, color=S.WHITE, scale_factor=1.08), run_time=0.9)

            vo.wait_until("The Chinese subtitle")
            self.play(Circumscribe(cue.zh, color=S.WHITE, buff=0.08, run_time=1.0))
            self.play(FadeIn(gl_card, shift=LEFT * 0.2), GrowArrow(gl_arrow), run_time=0.8)
            vo.wait_until("that this is not")
            self.play(FadeIn(stamp, scale=1.6), run_time=0.5)
            self.play(Wiggle(stamp, scale_value=1.08, rotation_angle=0.03 * TAU), run_time=0.7)

            vo.wait_until("Both AI reviewers")
            self.play(LaggedStart(*[FadeIn(r, shift=UP * 0.2) for r in revs], lag_ratio=0.25), FadeIn(revs_l),
                      run_time=0.7)
            self.play(LaggedStart(*[GrowFromEdge(f, DOWN) for f in flags], lag_ratio=0.3), run_time=0.7)
            self.play(Create(zh_line), *[Wiggle(f.cloth, scale_value=1.15, rotation_angle=0.02 * TAU,
                                                 rotate_about_point=f.pole.get_end()) for f in flags], run_time=0.8)

        # ---------------------------------------------------------- ponder (the band stays in view under the card)
        keep = set(cue.en.get_family()) | set(cue.zh.get_family()) | {zh_line}
        shown = [m for m in self.mobjects if not set(m.get_family()) & keep]      # the two cue lines stay bright
        card = ponder_card(QUESTION, width=8.6)
        card.move_to([FRAME_X0 + FRAME_W / 2 + 0.5, 0, 0]).align_to(cue.band, DOWN).shift(UP * (cue.band.height + 0.3))
        with self.voiceover(SAY[4]) as vo:
            self.play(*dim(*shown, opacity=0.4), run_time=0.5)
            vo.wait_until("Pause")
            self.play(FadeIn(card, scale=0.95), run_time=0.6)        # as ponder_in, placed above the band
            vo.wait_until("The English line")
            self.play(Circumscribe(cue.en, color=S.WHITE, buff=0.08, run_time=1.0))
            vo.wait_until("and the Chinese says")
            self.play(Circumscribe(cue.zh, color=S.WHITE, buff=0.08, run_time=1.0))
        ponder_drain(self, card, 10)
        fade_out_all(self)

