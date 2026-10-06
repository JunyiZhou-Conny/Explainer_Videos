"""Subtitles in one or two languages, from the narration timings recorded while rendering.

Every narration clip in <scene>.subs.json carries the English line, the times at which its
sentences start, and for a translated render (EXPLAINER_LANG=zh) the translated sentences with
their exact spans. Because translations are sentence-aligned (explainer.i18n), each sentence
pair (Chinese, English) shares one time span:

    tracks(clips, lang) -> {"zh": [(start, end, text)], "en": [...], "zh-en": [(start, end, zh, en)]}

`write_srt` writes plain .srt files (2 lines max per cue); `write_ass` writes a styled bilingual
.ass (Chinese line above, smaller English line below); `burn` renders a video with the bilingual
subtitles in a band under the picture (the picture is scaled down a little so subtitles never
cover the bottom of a scene, where these videos often put labels).
"""

from __future__ import annotations

import re
import subprocess
from functools import lru_cache
from pathlib import Path

_CJK = re.compile(r"[⺀-鿿豈-﫿＀-￯　-〿]")
_BREAK_AFTER = "，、；：。！？,;:—)）」』”…"
_NO_LINE_START = "，、；：。！？,;:)）」』”…"
_OPENERS = "（(「『“《"
_DROP_AT_END = "。，、；：,;:"
_FULLWIDTH_PUNCT = "，、；：。！？（）「」『』“”《》…—"
SENTENCE_GAP = 0.32


def is_cjk(ch: str) -> bool:
    return bool(_CJK.match(ch))


def units(s: str) -> float:
    """Display width in 'CJK character' units (a Latin character is about half as wide)."""
    return sum(1.0 if _CJK.match(ch) else 0.55 for ch in s)


def _cuts(text: str) -> tuple[list[int], list[int]]:
    """Positions where a line or cue may break. 'good': after punctuation, and at spaces between
    Latin words. 'ok': between two CJK characters, or at a space next to CJK text. Never inside a
    number (255,168 / 0.5), between a number and its measure word (5 步), inside 《…》, before
    punctuation or after an opening bracket."""
    good, ok = [], []
    depth = 0
    mixed = bool(_CJK.search(text))
    for i in range(1, len(text)):
        a, b = text[i - 1], text[i]
        if a in ",;:)" and b != " " and not is_cjk(b) and i < len(text):
            continue                                          # S(f)/ε, 2,5: only before a space/CJK
        if a == "《":
            depth += 1
        elif a == "》":
            depth = max(0, depth - 1)
        if b in _NO_LINE_START or a in _OPENERS:
            continue
        if depth:                                             # inside 《…》: only at spaces, as a last resort
            if a == " " and b != " ":
                ok.append(i)
            continue
        if a in ",." and i >= 2 and text[i - 2].isdigit() and b.isdigit():
            continue                                          # inside a number
        if a in _BREAK_AFTER:
            good.append(i)
        elif a == " ":
            p = text[i - 2] if i >= 2 else ""
            if p.isdigit() and is_cjk(b):
                continue                                      # "5 步"
            if not is_cjk(p) and not is_cjk(b):
                if not mixed:
                    good.append(i)                            # between words of an English line
                elif _latin_run(text, i) > 24:
                    ok.append(i)                              # a long English run inside Chinese
                # otherwise keep kept-English terms whole: hybrid argument, Kobbi Nissim
            else:
                ok.append(i)
        elif b == " ":
            continue                                          # cut after the space instead
        elif a.isdigit() and is_cjk(b):
            continue
        elif is_cjk(a) or is_cjk(b):
            ok.append(i)
    return good, ok


def _latin_run(text: str, i: int) -> int:
    """Length of the run of non-CJK characters around position i."""
    lo = i
    while lo > 0 and not is_cjk(text[lo - 1]) and text[lo - 1] not in "，。、；：！？":
        lo -= 1
    hi = i
    while hi < len(text) and not is_cjk(text[hi]) and text[hi] not in "，。、；：！？":
        hi += 1
    return hi - lo


def join_pieces(a: str, b: str) -> str:
    if not a or not b:
        return (a or b).strip()
    sep = "" if (is_cjk(a[-1]) or is_cjk(b[0])) and not (a[-1].isalnum() and b[0].isalnum()
                                                          and not is_cjk(a[-1]) and not is_cjk(b[0])) else " "
    if (is_cjk(a[-1]) and b[0].isascii() and b[0].isalnum()) or (is_cjk(b[0]) and a[-1].isascii() and a[-1].isalnum()):
        sep = " "                                             # keep the CJK-Latin space (rule B1)
    if a[-1] in _FULLWIDTH_PUNCT or b[0] in _FULLWIDTH_PUNCT:
        sep = ""                                              # full-width punctuation has its own space
    return (a.rstrip() + sep + b.lstrip()).strip()


def strip_end(piece: str) -> str:
    """Subtitle convention for Chinese: no 。，、；： at the end of a cue (keep ？！…… ” ）)."""
    return piece.rstrip(_DROP_AT_END + " ") if piece and _CJK.search(piece) else piece


# an English line should not end on one of these ("by a / billion")
_FUNCTION_WORDS = {"a", "an", "the", "of", "to", "by", "in", "on", "at", "for", "and", "or", "nor",
                   "with", "from", "as", "is", "are", "was", "be", "its", "their", "his", "her",
                   "that", "than", "into", "per", "if", "but", "so", "not", "no", "each", "every"}


# a Chinese line should not end on a preposition / conjunction ("统计从 / 现在这个棋盘")
# or start with a particle
_CJK_NO_END = set("从把在对给向跟和与被让将比以于为及或而但且")
_CJK_NO_START = set("的了着过地得们吗呢吧啊")


@lru_cache(maxsize=4096)
def _word_bounds(text: str) -> frozenset[int] | None:
    """Character offsets between words (jieba segmentation), or None without jieba."""
    try:
        import logging

        import jieba
        jieba.setLogLevel(logging.WARNING)
    except ImportError:
        return None
    out, i = set(), 0
    for w in jieba.cut(text, HMM=True):
        i += len(w)
        out.add(i)
    return frozenset(out)


def _cut_penalty(text: str, c: int) -> float:
    """Extra cost (in units) of cutting at position c. English (at a word gap): a plain gap costs
    more than a cut after punctuation, a gap after a function word or next to a number much more.
    Chinese: a cut after a preposition or before a particle costs a lot."""
    a, b = text[c - 1], text[c] if c < len(text) else ""
    if is_cjk(a) or is_cjk(b) or (a == " " and _CJK.search(text)):
        prev = text[:c].rstrip()[-1:]
        nxt = text[c:].lstrip()[:1]
        cost = 6.0 if prev in _CJK_NO_END or nxt in _CJK_NO_START else 0.0
        bounds = _word_bounds(text) if is_cjk(a) and is_cjk(b) else None
        if bounds is not None and c not in bounds:
            cost += 8.0                                   # inside a word: 现|在
        return cost
    if a != " ":
        return 0.0
    prev = text[:c - 1].rsplit(" ", 1)[-1]
    if not prev[-1:].isalnum():
        return 0.0
    cost = 4.0
    if prev.lower() in _FUNCTION_WORDS:
        cost += 8.0
    if prev[-1:].isdigit() or b.isdigit():
        cost += 4.0                                       # "on move / 6", "9 times / 8"
    return cost


def _pick_cuts(text: str, k: int, pool_of, total: float) -> list[int] | None:
    cuts, prev = [], 0
    for j in range(1, k):
        ideal_u = total * j / k
        pool = pool_of(prev, ideal_u)
        if not pool:
            return None
        cut = min(pool, key=lambda c: abs(units(text[:c]) - ideal_u) + _cut_penalty(text, c))
        cuts.append(cut)
        prev = cut
    return cuts


def split_balanced(text: str, limit: float) -> list[str]:
    """Fewest pieces of at most `limit` units each, balanced in length. Cuts at punctuation
    whenever the pieces still fit (even if unbalanced), else at the best word gap or between CJK
    characters; English pieces avoid ending on an article or preposition, Chinese pieces on a
    preposition."""
    text = " ".join(text.split())
    if units(text) <= limit:
        return [text]
    good, ok = _cuts(text)
    stops = "，、；：。！？,;:.!?…—"                    # not after a closing quote or bracket
    punct = [c for c in good if _cut_penalty(text, c) == 0 and text[c - 1] in stops + " "
             and (text[c - 1] != " " or text[c - 2] in stops)]
    total = units(text)

    def pieces_of(cuts):
        return [text[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(text)])]

    for k in range(2, 40):
        tries = (
            lambda prev, ideal: [c for c in punct if c > prev],
            lambda prev, ideal: ([c for c in good if c > prev and abs(units(text[:c]) - ideal) <= total / (2.5 * k)]
                                 or [c for c in ok + good if c > prev]),
        )
        for pool_of in tries:
            cuts = _pick_cuts(text, k, pool_of, total)
            if cuts is None:
                continue
            pieces = pieces_of(cuts)
            if all(p and units(p) <= limit for p in pieces):
                return pieces
    return [text]


def wrap(text: str, limit: float, max_lines: int = 2) -> str:
    lines = split_balanced(text, limit)
    return "\n".join(lines[:max_lines]) if len(lines) <= max_lines else "\n".join(lines)


# ---------------------------------------------------------------- sentence pairs and tracks

def sentence_pairs(clip: dict, offset: float, translation=None) -> list[tuple[float, float, str, str]]:
    """(start, end, translated, english) for each sentence of one narration clip.

    Timing comes from the translated audio when the clip was rendered in another language
    (clip["tr_spans"]), else from the English sentence marks. `translation` (an i18n.Line) supplies
    the translated text for an English render."""
    from .voice import split_sentences

    en_sents = [s for _, s in split_sentences(clip["text"])]
    display = clip.get("en_display") or (translation.en_display if translation is not None else [])
    en_sents = [d if d else e for e, d in zip(en_sents, list(display) + [None] * len(en_sents))]
    if clip.get("tr") and clip.get("tr_spans"):
        tr_sents = clip["tr"]
        spans = [(offset + clip["start"] + a, offset + clip["start"] + b) for a, b in clip["tr_spans"]]
    else:
        tr_sents = translation.sentences if translation is not None else [""] * len(en_sents)
        marks = clip.get("marks") or []
        base = offset + clip["start"]
        if len(marks) == len(en_sents):
            starts = [base + t for _, t in marks]
        else:                               # old renders: proportional to characters
            n = max(1, len(clip["text"]))
            dur = clip["end"] - clip["start"]
            starts = [base + dur * o / n for o, _ in split_sentences(clip["text"])]
        end = offset + clip["end"]
        spans = [(a, (starts[i + 1] - SENTENCE_GAP) if i + 1 < len(starts) else end)
                 for i, a in enumerate(starts)]
    if len(tr_sents) != len(en_sents):     # misaligned translation: one cue for the whole clip
        a, b = spans[0][0], spans[-1][1]
        return [(a, b, " ".join(tr_sents), " ".join(en_sents))]
    return [(a, b, t, e) for (a, b), t, e in zip(spans, tr_sents, en_sents)]


def _proportional(a: float, b: float, pieces: list[str]) -> list[tuple[float, float, str]]:
    total = sum(units(p) for p in pieces) or 1
    out, t = [], a
    for p in pieces:
        dt = (b - a) * units(p) / total
        out.append((t, t + dt, p))
        t += dt
    return out


def tracks(pairs: list[tuple[float, float, str, str]], timing: str = "tr",
           zh_limit: float = 22, en_limit: float = 44 * 0.55,
           bi_zh_limit: float = 30, bi_en_limit: float = 88 * 0.55, min_dur: float = 1.0,
           min_show: float = 1.6) -> dict:
    """Subtitle tracks from sentence pairs. `timing` = "tr" (the translated audio drives the
    timing inside a sentence) or "en".

    - Cues shorter than `min_dur` are merged into a neighbour when the result still fits; the
      sentence punctuation inside a merged cue stays (不是。电脑能做的……), and only the end of a
      Chinese cue loses its 。，、；：.
    - Single-language cues have at most 2 lines; a longer piece becomes two cues.
    - In the bilingual track, the English sentence is cut where the Chinese one is (at the
      matching clause boundary); when it fits on one line and no boundary is close, the whole
      English sentence stays up under each Chinese piece.
    - Every cue stays up at least `min_show` seconds when the next cue leaves room."""
    zh, en, bi = [], [], []
    for n, (a, b, t, e) in enumerate(pairs):
        if t:
            zh += _proportional(a, b, split_balanced(t, 2 * zh_limit))
        en += _proportional(a, b, split_balanced(e, 2 * en_limit))
        if t:
            zp = split_balanced(t, bi_zh_limit)
            ne = len(split_balanced(e, bi_en_limit))
            if ne > len(zp):
                zp = _split_k(t, ne, bi_zh_limit)
            ep, same = _split_like(e, zp, bi_en_limit)
            drive = zp if timing == "tr" else [p or e for p in ep]
            for (s0, s1, _), zt, et in zip(_proportional(a, b, drive), zp, ep):
                bi.append((s0, s1, zt, et, n if same else None))
    zh = _merge_short(zh, lambda x, y: _fits_join(x, y, zh_limit, 2), min_dur)
    en = _merge_short(en, lambda x, y: _fits_join(x, y, en_limit, 2), min_dur)
    bi = _merge_short(bi, None, min_dur, bi_zh_limit, bi_en_limit)
    zh = _linger([c for x in zh for c in _two_lines(x, zh_limit)], min_show)
    en = _linger([c for x in en for c in _two_lines(x, en_limit)], min_show)
    bi = _linger([(s0, s1, strip_end(z), e) for s0, s1, z, e, _ in bi], min_show)
    return {"zh": zh, "en": en, "zh-en": bi}


def _split_like(e: str, zp: list[str], limit: float) -> tuple[list[str], bool]:
    """Cut the English sentence into len(zp) pieces at the positions proportional to the Chinese
    cuts, preferring clause boundaries. Returns (pieces, repeated): repeated = the whole sentence
    is shown under every Chinese piece."""
    k = len(zp)
    e = " ".join(e.split())
    if k == 1:
        return [e], False
    zt = sum(units(p) for p in zp) or 1
    fr = [sum(units(p) for p in zp[:j]) / zt for j in range(1, k)]
    good, _ = _cuts(e)
    total = units(e)
    stops = ",;:.!?—"

    def at_stop(c):
        return e[c - 1] in stops or (e[c - 1] == " " and e[c - 2] in stops)

    cuts, prev = [], 0
    for f in fr:
        target = f * total
        near = [c for c in good if c > prev and at_stop(c) and abs(units(e[:c]) - target) <= 0.25 * total]
        if not near:
            cuts = None
            break
        c = min(near, key=lambda c: abs(units(e[:c]) - target))
        cuts.append(c)
        prev = c
    if cuts:
        pieces = [e[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(e)])]
        if all(p and units(p) <= limit for p in pieces):
            return pieces, False
    if units(e) <= limit:
        return [e] * k, True
    cuts, prev = [], 0
    for f in fr:                                           # too long for one line: best gap
        target = f * total
        pool = [c for c in good if c > prev]
        if not pool:
            break
        c = min(pool, key=lambda c: abs(units(e[:c]) - target) + _cut_penalty(e, c))
        cuts.append(c)
        prev = c
    pieces = [e[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(e)])]
    if len(pieces) == k and all(p and units(p) <= limit for p in pieces):
        return pieces, False
    return _split_k(e, k, limit), False


def _two_lines(cue, limit: float) -> list[tuple[float, float, str]]:
    """A cue wrapped to at most 2 lines; a piece that needs more becomes two cues (time split
    in proportion to their length), cut at a clause boundary when one gives two 2-line cues."""
    a, b, text = cue
    text = strip_end(text)
    lines = split_balanced(text, limit)
    if len(lines) <= 2:
        return [(a, b, "\n".join(lines))]
    good, ok = _cuts(text)
    stops = "，、；：。！？,;:.!?…—"
    best = None
    for c in good + ok:
        left, right = text[:c].strip(), text[c:].strip()
        if not left or not right:
            continue
        if len(split_balanced(strip_end(left), limit)) > 2 or len(split_balanced(right, limit)) > 2:
            continue
        cost = abs(units(left) - units(right)) + _cut_penalty(text, c)
        cost += 0 if text[c - 1] in stops or (text[c - 1] == " " and text[c - 2] in stops) else 12
        if best is None or cost < best[0]:
            best = (cost, [left, right])
    halves = best[1] if best else [join_pieces(*lines[:2]), "".join(lines[2:]) if _CJK.search(text)
                                                         else " ".join(lines[2:])]
    out = []
    for s0, s1, h in _proportional(a, b, halves):
        out += _two_lines((s0, s1, h), limit)
    return out


def _linger(cues, min_show: float):
    """Let a short cue stay up to `min_show` s, but never into the next cue."""
    out = [list(c) for c in cues]
    for i, c in enumerate(out):
        nxt = out[i + 1][0] - 0.05 if i + 1 < len(out) else c[0] + min_show
        if c[1] - c[0] < min_show:
            c[1] = max(c[1], min(c[0] + min_show, nxt))
    return [tuple(c) for c in out]


def _fits_join(x: str, y: str, limit: float, lines: int):
    joined = join_pieces(x, y)
    return joined if len(split_balanced(strip_end(joined), limit)) <= lines else None


def _merge_short(cues, join, min_dur, bi_zh=None, bi_en=None):
    """Fold cues shorter than min_dur into the following cue (or the previous one at the end)
    when the merged text still fits; contiguous cues only (gap < 0.4 s). Bilingual cues carry a
    5th field: the sentence number when their English line is the whole sentence repeated, so
    a merge does not repeat it."""
    cues = [list(c) for c in cues]
    i = 0
    while i < len(cues):
        c = cues[i]
        if c[1] - c[0] >= min_dur or len(cues) == 1:
            i += 1
            continue
        merged = False
        for j in (i + 1, i - 1):
            if not 0 <= j < len(cues):
                continue
            lo, hi = min(i, j), max(i, j)
            if cues[hi][0] - cues[lo][1] > 0.4:
                continue
            if join is not None:
                text = join(cues[lo][2], cues[hi][2])
                if text is None:
                    continue
                cues[lo:hi + 1] = [[cues[lo][0], cues[hi][1], text]]
            else:
                z = join_pieces(cues[lo][2], cues[hi][2])
                same = cues[lo][4] is not None and cues[lo][4] == cues[hi][4]
                e = cues[lo][3] if same else join_pieces(cues[lo][3], cues[hi][3])
                if units(strip_end(z)) > bi_zh or units(e) > bi_en:
                    continue
                cues[lo:hi + 1] = [[cues[lo][0], cues[hi][1], z, e, cues[lo][4] if same else None]]
            merged = True
            break
        if not merged:
            i += 1
        else:
            i = max(0, min(i, j))
    return [tuple(c) for c in cues]


def _split_k(text: str, k: int, limit: float) -> list[str]:
    """Split into exactly k balanced pieces (fewer pieces are padded by splitting the longest)."""
    pieces = split_balanced(text, limit)
    while len(pieces) < k:
        i = max(range(len(pieces)), key=lambda j: units(pieces[j]))
        sub = split_balanced(pieces[i], units(pieces[i]) / 2 + 0.6)
        if len(sub) < 2:
            pieces.append(pieces[-1])                     # nothing to cut: the line stays up
            continue
        rest = sub[1]
        for extra in sub[2:]:
            rest = join_pieces(rest, extra)
        pieces[i:i + 1] = [sub[0], rest]
    while len(pieces) > k:                   # merge the shortest neighbours
        i = min(range(len(pieces) - 1), key=lambda j: units(pieces[j]) + units(pieces[j + 1]))
        pieces[i:i + 2] = [join_pieces(pieces[i], pieces[i + 1])]
    return pieces


# ---------------------------------------------------------------- writers

def fmt_srt(t: float) -> str:
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(path: Path, cues) -> None:
    rows = []
    for n, cue in enumerate(cues, 1):
        a, b = cue[0], cue[1]
        body = "\n".join(x for x in cue[2:] if x)
        rows.append(f"{n}\n{fmt_srt(a)} --> {fmt_srt(b)}\n{body}\n")
    Path(path).write_text("\n".join(rows), encoding="utf-8")


def _ass_time(t: float) -> str:
    cs = int(round(t * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def _ass_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("{", "(").replace("}", ")").replace("\n", "\\N")


BAND = 0.13        # fraction of the frame height reserved for subtitles when burning


def write_ass(path: Path, bi_cues, width: int = 1920, height: int = 1080, band: float = BAND,
              title: str = "") -> None:
    """Bilingual .ass: the translated line (larger, white) above the English line (smaller, grey),
    as ONE event per cue so the two lines always stack in that order. Positioned for `burn()`'s
    layout (both lines inside the band under the scaled picture); as a soft subtitle over the full
    picture they sit at the bottom as usual."""
    band_px = int(round(height * band))
    zh_size, en_size = int(height * 0.047), int(height * 0.031)
    margin = max(6, int(band_px * 0.12))
    en_tag = r"{\fs%d\c&H00C8C0B8&\bord1.4}" % en_size
    head = f"""[Script Info]
Title: {title}
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Bilingual,Noto Sans CJK SC,{zh_size},&H00F2F2F2,&H00F2F2F2,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,2,0,2,40,40,{margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    for a, b, zh, en in bi_cues:
        parts = [_ass_escape(zh)] if zh else []
        if en:
            parts.append(en_tag + _ass_escape(en))
        if parts:
            body = "\\N".join(parts)
            ev.append(f"Dialogue: 0,{_ass_time(a)},{_ass_time(b)},Bilingual,,0,0,0,,{body}")
    Path(path).write_text(head + "\n".join(ev) + "\n", encoding="utf-8")


def burn(src: Path, ass: Path, dst: Path, band: float = BAND, crf: int = 23, bg: str = "0x0D0F14") -> None:
    """Scale the picture to (1 - band) of the frame, centred at the top, and draw the bilingual
    subtitles in the band underneath. Re-encodes the video (x264), copies the audio."""
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=width,height", "-of", "csv=p=0:s=x", str(src)],
                       capture_output=True, text=True, check=True)
    W, H = (int(x) for x in r.stdout.strip().split("x"))
    w, h = int(W * (1 - band)) // 2 * 2, int(H * (1 - band)) // 2 * 2
    vf = (f"scale={w}:{h}:flags=lanczos,pad={W}:{H}:{(W - w) // 2}:0:color={bg},"
          f"ass='{str(ass).replace(chr(39), '')}'")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", vf, "-c:v", "libx264",
                    "-preset", "medium", "-tune", "animation", "-crf", str(crf), "-pix_fmt", "yuv420p",
                    "-c:a", "copy", "-movflags", "+faststart", str(dst)], check=True)
