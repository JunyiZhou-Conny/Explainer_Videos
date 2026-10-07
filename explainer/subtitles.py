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
from collections import Counter
from difflib import SequenceMatcher
from functools import lru_cache, reduce
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
    Latin words. 'ok': between two CJK characters, at a space next to CJK text, or anywhere inside
    “…” or （…） (a last resort, see _cut_penalty). Never inside a number (255,168 / 0.5), between
    a number and its measure word (5 步), inside 《…》 (but at its spaces, as a last resort),
    before punctuation, after an opening bracket or before a bracket glued to the word it glosses
    (hybrid argument（混合论证）)."""
    good, ok = [], []
    depth = quoted = 0
    mixed = bool(_CJK.search(text))
    for i in range(1, len(text)):
        a, b = text[i - 1], text[i]
        if a in ",;:)" and b != " " and not is_cjk(b) and i < len(text):
            continue                                          # S(f)/ε, 2,5: only before a space/CJK
        if a == "《":
            depth += 1
        elif a == "》":
            depth = max(0, depth - 1)
        quoted = quoted + 1 if a in "“（" else max(0, quoted - 1) if a in "”）" else quoted
        if b in _NO_LINE_START or a in _OPENERS or (b in "（(" and a != " " and a not in _BREAK_AFTER):
            continue
        if depth:                                             # inside 《…》: only at spaces, as a last resort
            if a == " " and b != " ":
                ok.append(i)
            continue
        if a in ",." and i >= 2 and text[i - 2].isdigit() and b.isdigit():
            continue                                          # inside a number
        best = ok if quoted else good                         # inside “…” or （…）: a last resort
        if a in _BREAK_AFTER:
            best.append(i)
        elif a == " ":
            p = text[i - 2] if i >= 2 else ""
            if p.isdigit() and is_cjk(b):
                continue                                      # "5 步"
            if not is_cjk(p) and not is_cjk(b):
                if not mixed:
                    best.append(i)                            # between words of an English line
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


# an English line should not end on one of these ("by a / billion", "scrambles their own / row")
_FUNCTION_WORDS = {"a", "an", "the", "of", "to", "by", "in", "on", "at", "for", "and", "or", "nor",
                   "with", "from", "as", "is", "are", "was", "were", "be", "been", "being",
                   "has", "have", "had", "do", "does", "did", "can", "could", "will", "would",
                   "shall", "should", "may", "might", "must", "its", "their", "his", "her", "our",
                   "your", "my", "own", "that", "than", "into", "per", "if", "but", "so", "not", "no",
                   "each", "every"}


# nor start with one of these ("single / out", "whatever / else")
_PARTICLES = {"out", "up", "off", "away", "back", "down", "else"}


# a Chinese line should not end on a preposition / conjunction ("统计从 / 现在这个棋盘"), a 的 that
# belongs to the next noun ("公开的 / 选民名单") or a negation, or start with a particle
_CJK_NO_END = set("从把在对给向跟和与被让将比以于为及或而但且的不没")
_CJK_NO_START = set("的了着过地得们吗呢吧啊")
_CJK_NO_END_WORDS = ("这些", "那些", "这个", "那个", "这种", "那种", "每个", "某个")   # "把这些 / query"
_CJK_NO_START_WORDS = ("以内", "以上", "以下", "以外", "之间", "之内", "之外")         # "clip 到 C / 以内"
_TITLE = re.compile(r"《[^《》]*》")
_GLOSS = re.compile(r"[A-Za-z][A-Za-z' -]*(?=[，；。]|$)")    # a spoken English gloss: "，sensitivity；"


# terms jieba splits (差分/隐私, 深度/网络, 不/可能) but a line must keep whole; the zh terms of every
# video's glossary are added to them (_glossary_terms)
_TERMS = ("差分隐私", "本地化差分隐私", "深度网络", "不可能", "隐私预算", "拉普拉斯机制", "组合定理",
          "指数机制", "最小割", "比特串", "训练集")
_TERM_EDGE = set("的了在是和与或被把对个种局条次步年第")   # not a term's first or last character


def _glossary_terms() -> list[str]:
    """Chinese terms of videos/*/i18n/zh/glossary.yaml: each run of 2-7 CJK characters of a term's
    zh_subtitle (its alternatives and label forms) that does not start or end on a particle,
    preposition or measure word."""
    import yaml

    out = []
    for g in sorted((Path(__file__).resolve().parent.parent / "videos").glob("*/i18n/zh/glossary.yaml")):
        for t in (yaml.safe_load(g.read_text(encoding="utf-8")) or {}).get("terms") or []:
            for w in re.split(r"[^一-鿿]+", str(t.get("zh_subtitle") or "")):
                if 2 <= len(w) <= 7 and w[0] not in _TERM_EDGE and w[-1] not in _TERM_EDGE:
                    out.append(w)
    return out


@lru_cache(maxsize=1)
def _jieba():
    """jieba with the project's terms registered, or None when it is not installed."""
    try:
        import logging

        import jieba
    except ImportError:
        return None
    jieba.setLogLevel(logging.WARNING)
    for w in [*_TERMS, *_glossary_terms()]:
        jieba.add_word(w)
    return jieba


@lru_cache(maxsize=4096)
def _word_bounds(text: str) -> frozenset[int] | None:
    """Character offsets between words (jieba segmentation), or None without jieba."""
    jieba = _jieba()
    if jieba is None:
        return None
    out, i = set(), 0
    for w in jieba.cut(text, HMM=True):
        i += len(w)
        out.add(i)
    return frozenset(out)


def _cut_penalty(text: str, c: int) -> float:
    """Extra cost (in units) of cutting at position c. English (at a word gap): a plain gap costs
    more than a cut after punctuation, a gap after a function word or next to a number much more.
    Chinese: a cut after a preposition or before a particle costs a lot. Both: a cut inside “…”
    or （…） costs a little, one inside a 《…》 title more (cut before the 《 instead)."""
    head = text[:c]
    cost = 5.0 if head.count("“") + head.count("（") > head.count("”") + head.count("）") else 0.0
    if head.count("《") > head.count("》"):
        cost += 10.0
    a, b = text[c - 1], text[c] if c < len(text) else ""
    if is_cjk(a) or is_cjk(b) or (a == " " and is_cjk(text[c - 2:c - 1] or " ")):
        before, after = head.rstrip(), text[c:].lstrip()
        bad_end = before[-1:] in _CJK_NO_END or before.endswith(_CJK_NO_END_WORDS)
        bad_start = after[:1] in _CJK_NO_START or (after.startswith(_CJK_NO_START_WORDS)
                                                   and before[-1:] not in _BREAK_AFTER)
        names = re.match(r"[和与及] [A-Z]", after) and before[-1:].isascii() and before[-1:].isalpha()
        if bad_end or bad_start or names:                 # names: "Rothblum / 和 Vadhan"
            cost += 6.0
        if before[-1:] in "，、" and _GLOSS.match(after):
            cost += 20.0                                  # "隐私预算 / privacy budget。": keep the gloss
        bounds = _word_bounds(text) if is_cjk(a) and is_cjk(b) else None
        if bounds is not None and c not in bounds:
            cost += 8.0                                   # inside a word: 现|在
        return cost
    if a != " ":
        return cost
    prev = text[:c - 1].rsplit(" ", 1)[-1]
    if not prev[-1:].isalnum():
        return cost
    cost += 4.0
    if prev.lower() in _FUNCTION_WORDS:
        cost += 8.0
    words = text[:c - 1].split()
    if prev[:1].isupper() and len(words) > 1 and (b.isupper() or re.match(r"(and|or) [A-Z]", text[c:])):
        cost += 8.0                                       # names: "Kobbi / Nissim", "Nissim / and Adam"
    if text[c:].split(" ", 1)[0].rstrip(",.;:!?") in _PARTICLES:
        cost += 6.0                                       # "single / out", "whatever / else"
    if prev.endswith(("'s", "’s")):
        cost += 6.0                                       # "Alice's / row"
    elif len(words) > 1 and words[-2].endswith(("'s", "’s")):
        cost += 4.0                                       # "framework's sharper / analysis": a noun phrase
    if prev[-1:].isdigit() or b.isdigit():
        cost += 4.0                                       # "on move / 6", "9 times / 8"
    return cost


_STRONG = "。！？；：.!?;:—…"


def _mark_cost(text: str, c: int) -> float:
    """Weight of the mark a cut at c follows, so that the stronger mark wins when the balance is
    close: none after 。！？；：. ! ? ; : — …, 3 after a comma (or no mark at all), 8 after a comma
    that leaves a short clause before a 。；！？ (the cut belongs there), 6 after 、 (it splits a
    list: 光凭邮编、/ 出生日期), 10 after a 、 between two Latin names (Dwork、/ Rothblum) or a comma
    between two numbers (moves 7, / 8 and 9)."""
    head = text[:c].rstrip()
    if head[-1:] in _STRONG:
        return 0.0
    nxt = text[c:].lstrip()[:1]
    if head[-1:] == "、":
        names = head[-2:-1].isascii() and head[-2:-1].isalpha() and nxt.isascii() and nxt.isalpha()
        return 10.0 if names else 6.0
    if head[-1:] == "," and head[-2:-1].isdigit() and nxt.isdigit():
        return 10.0                                        # a list of numbers: "moves 7, / 8 and 9"
    end = re.search(r"[。！？；.!?;]", text[c:])
    if head[-1:] in "，," and end and units(text[c:c + end.start()]) <= 7:
        return 8.0                  # a clause end a few characters on: "偶数个 1，/ 真实答案为 0；"
    return 3.0


def _pick_cuts(text: str, k: int, pool_of, total: float) -> list[int] | None:
    cuts, prev = [], 0
    for j in range(1, k):
        ideal_u = total * j / k
        pool = pool_of(prev, ideal_u)
        if not pool:
            return None
        cut = min(pool, key=lambda c: abs(units(text[:c]) - ideal_u) + _cut_penalty(text, c)
                  + _mark_cost(text, c))
        cuts.append(cut)
        prev = cut
    return cuts


def split_balanced(text: str, limit: float, hang: bool = False) -> list[str]:
    """Fewest pieces of at most `limit` units each, balanced in length. Cuts at punctuation
    whenever the pieces still fit (even if unbalanced, but not leaving a stray scrap at a comma),
    preferring the stronger mark (_mark_cost), else at the best word gap or between CJK
    characters; English pieces avoid ending on an article or preposition, Chinese pieces on a
    preposition. `hang`: the pieces are cues, whose final ，。、；： is dropped (strip_end), so it
    does not count against the limit, and a whole 《…》 title may run 5 units over it (a 30-unit
    bilingual line is about 1040 px of the 1840 px line at 1080p, measured with burn())."""
    text = " ".join(text.split())
    if units(strip_end(text) if hang else text) <= limit:
        return [text]
    good, ok = _cuts(text)
    stops = "，；：。！？,;:.!?…—"                     # not after 、, a closing quote or bracket
    punct = [c for c in good if _cut_penalty(text, c) == 0 and text[c - 1] in stops + " "
             and (text[c - 1] != " " or text[c - 2] in stops)]
    total = units(text)

    def pieces_of(cuts):
        return [text[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(text)])]

    def fits(p):
        q = strip_end(p) if hang else p
        return p and (units(q) <= limit or (hang and _TITLE.fullmatch(q) and units(q) <= limit + 5))

    def stray(cuts, pieces):
        """A piece of a few characters cut off at a comma: "2016 年，/ Abadi 和合作者……", "…the
        honest answer, / f(x)." (under a quarter of the longest piece in Chinese, a sixth in English)."""
        short = max(units(p) for p in pieces) / (4 if _CJK.search(text) else 6)
        commas = [text[:c].rstrip()[-1:] in "，、," for c in cuts]   # the cut after each piece
        return any(units(p) < short and any(commas[max(0, j - 1):j + 1]) for j, p in enumerate(pieces))

    for k in range(2, 40):
        tries = (
            lambda prev, ideal: [c for c in punct if c > prev],
            lambda prev, ideal: ([c for c in good if c > prev and abs(units(text[:c]) - ideal) <= total / (2.5 * k)]
                                 or [c for c in ok + good if c > prev]),
        )
        for n, pool_of in enumerate(tries):
            cuts = _pick_cuts(text, k, pool_of, total)
            if cuts is None:
                continue
            pieces = pieces_of(cuts)
            if all(fits(p) for p in pieces) and not (n == 0 and stray(cuts, pieces)):
                return pieces
    return [text]


def wrap(text: str, limit: float, max_lines: int = 2) -> str:
    lines = split_balanced(text, limit)
    return "\n".join(lines[:max_lines]) if len(lines) <= max_lines else "\n".join(lines)


# ---------------------------------------------------------------- sentence pairs and tracks

def sentence_pairs(clip: dict, offset: float, translation=None) -> list[tuple]:
    """(start, end, translated, english, spoken) for each sentence of one narration clip; spoken
    is what the voice read (clip["tr_say"], the say: form) or None when it is the translated text.

    Timing comes from the translated audio when the clip was rendered in another language
    (clip["tr_spans"]), else from the English sentence marks. `translation` (an i18n.Line) supplies
    the translated text for an English render, and the spoken form for a translated render made
    before clips recorded it."""
    from .voice import split_sentences

    en_sents = [s for _, s in split_sentences(clip["text"])]
    display = clip.get("en_display") or (translation.en_display if translation is not None else [])
    en_sents = [d if d else e for e, d in zip(en_sents, list(display) + [None] * len(en_sents))]
    say = [None] * len(en_sents)
    if clip.get("tr") and clip.get("tr_spans"):
        tr_sents = clip["tr"]
        spans = [(offset + clip["start"] + a, offset + clip["start"] + b) for a, b in clip["tr_spans"]]
        say = clip.get("tr_say") or (translation.spoken if translation is not None
                                     and translation.sentences == tr_sents else [None] * len(tr_sents))
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
        return [(a, b, " ".join(tr_sents), " ".join(en_sents), None)]
    return [(a, b, t, e, sp) for (a, b), t, e, sp in zip(spans, tr_sents, en_sents, say)]


def _proportional(a: float, b: float, pieces: list[str], weights=None) -> list[tuple[float, float, str]]:
    """The span a..b shared among the pieces in proportion to `weights` (default: their units)."""
    weights = weights or [units(p) for p in pieces]
    total = sum(weights) or 1
    out, t = [], a
    for p, w in zip(pieces, weights):
        dt = (b - a) * w / total
        out.append((t, t + dt, p))
        t += dt
    return out


def _spoken_weights(text: str, pieces: list[str], spoken: str) -> list[float] | None:
    """How long each piece of `text` takes to say: the units of the part of the spoken sentence it
    stands for, by a character alignment of the two forms (2016 年 / 二零一六年, e^ε / E 的艾普西隆
    次方; a gloss （计数查询） that is not read weighs nothing). units() of the spoken text predicts
    the Xiaoyi sentence durations better than units() of the display text (R² 0.975 against 0.954
    over the 417 sentences of both videos). None when a piece cannot be found in `text`."""
    ops = SequenceMatcher(None, text, spoken, autojunk=False).get_opcodes()

    def at(i):                                             # text position -> spoken position
        for tag, i1, i2, j1, j2 in ops:
            if i1 <= i < i2:
                return j1 + (i - i1) if tag == "equal" else j1 + round((j2 - j1) * (i - i1) / (i2 - i1))
        return len(spoken)

    starts, pos = [], 0
    for p in pieces:
        pos = text.find(p, pos)
        if pos < 0:
            return None
        starts.append(pos)
    cuts = [0] + [at(i) for i in starts[1:]] + [len(spoken)]
    weights = [units(spoken[x:y]) for x, y in zip(cuts, cuts[1:])]
    return weights if all(w > 0 for w in weights) else None


def tracks(pairs: list[tuple], timing: str = "tr",
           zh_limit: float = 22, en_limit: float = 48 * 0.55,
           bi_zh_limit: float = 30, bi_en_limit: float = 96 * 0.55, min_dur: float = 1.0,
           min_show: float = 1.6) -> dict:
    """Subtitle tracks from sentence pairs (start, end, translated, english[, spoken]). `timing` =
    "tr" (the translated audio drives the timing inside a sentence, its pieces weighted by the
    spoken form when one is given: 2016 年 is read 二零一六年, a gloss （计数查询） is not read) or "en".

    - Cues shorter than `min_dur` are merged into a neighbour when the result still fits; the
      sentence punctuation inside a merged cue stays (不是。电脑能做的……), and only the end of a
      Chinese cue loses its 。，、；：.
    - Single-language cues have at most 2 lines; a longer piece becomes two cues.
    - In the bilingual track, the English sentence is cut where the Chinese one is (at the
      matching clause boundary, see _split_like); when it fits on one line and no boundary is
      close, the whole English sentence stays up under each Chinese piece.
    - Every cue stays up at least `min_show` seconds when the next cue leaves room."""
    zh, en, bi = [], [], []
    for n, (a, b, t, e, *say) in enumerate(pairs):
        spoken = say[0] if say and say[0] and timing == "tr" else None
        if t:
            zs = split_balanced(t, 2 * zh_limit, hang=True)
            zh += _proportional(a, b, zs, spoken and _spoken_weights(t, zs, spoken))
        en += _proportional(a, b, split_balanced(e, 2 * en_limit))
        if t:
            zp = split_balanced(t, bi_zh_limit, hang=True)
            ne = len(split_balanced(e, bi_en_limit))
            if ne > len(zp):
                zp = _split_k(t, ne, bi_zh_limit)
            ep, same = _split_like(e, zp, bi_en_limit)
            if timing == "tr":
                times = _proportional(a, b, zp, spoken and _spoken_weights(t, zp, spoken))
            else:
                times = _proportional(a, b, [p or e for p in ep])
            for (s0, s1, _), zt, et in zip(times, zp, ep):
                bi.append((s0, s1, zt, et, n if same else None))
    zh = _merge_short(zh, lambda x, y: _fits_join(x, y, zh_limit, 2), min_dur)
    en = _merge_short(en, lambda x, y: _fits_join(x, y, en_limit, 2), min_dur)
    bi = _merge_short(bi, None, min_dur, bi_zh_limit, bi_en_limit)
    zh = _linger([c for x in zh for c in _two_lines(x, zh_limit)], min_show)
    en = _linger([c for x in en for c in _two_lines(x, en_limit)], min_show)
    bi = _linger([(s0, s1, strip_end(z), e) for s0, s1, z, e, _ in bi], min_show)
    return {"zh": zh, "en": en, "zh-en": bi}


# a word that starts a clause: a cut before it (", which" / " and") lines up with a Chinese clause
_CLAUSE_STARTERS = {"and", "but", "or", "so", "yet", "which", "who", "where", "when", "while",
                    "because", "then", "that", "if", "unless", "as"}
_DETERMINERS = {"a", "an", "the", "this", "that", "these", "those", "its", "their", "his", "her",
                "our", "your", "my", "each", "every", "one"}


def _symbols(s: str) -> Counter:
    """Numbers and symbols of a piece (41, 52.5, 1/λ, e^ε → ε, x′ → ′), to match the English and
    the Chinese pieces of a bilingual cue."""
    return Counter(re.findall(r"\d+(?:[.,/]\d+)*|[^\x00-\x7f　-〿一-鿿＀-￯’‘“”—…]", s))


def _list_comma(e: str, c: int) -> bool:
    """A comma between two names or two adjectives rather than at a clause boundary: it ends a
    run of at most two words that does not start the sentence, and joins two capitalised words
    ("with Kenthapadi, McSherry, Mironov") or a run that is not a noun phrase to a lowercase
    content word ("for broad, flexible accuracy"; not "the curator, holds")."""
    head = e[:c].rstrip()
    if not head.endswith(","):
        return False
    runs = re.split(r"[,;:.!?—]\s", head[:-1])
    last, nxt = runs[-1].split(), (e[c:].split() or [""])[0]
    if len(runs) < 2 or not last or len(last) > 2:
        return False
    names = last[-1][:1].isupper() and nxt[:1].isupper()
    adjectives = (nxt[:1].islower() and nxt not in _FUNCTION_WORDS | _CLAUSE_STARTERS
                  and last[0].lower() not in _DETERMINERS)
    return names or adjectives


def _split_like(e: str, zp: list[str], limit: float) -> tuple[list[str], bool]:
    """Cut the English sentence into len(zp) pieces where the Chinese is cut. Each Chinese cut (at
    its share of the sentence, not counting subtitle-only glosses （…）) takes the cheapest English
    clause stop (not a list comma) that is nearer to it than to the other cuts, preferring one that
    leaves the numbers and symbols on the same side as the Chinese (41 / 42, 1/n, e^ε): cost =
    distance from where the numbers allow the cut ("…2 times 1, / so 24 ways.") + 3 per number on
    the wrong side + 4 for a ; or : under a Chinese ，, at most half the shorter neighbouring piece
    (or 4 units). Without one, a plain gap right at the cut before a
    preposition, auxiliary or conjunction will do. A piece may run 15 % over `limit` (a 110-character
    line is about 1170 px of the 1840 px line, measured with burn()). Failing that, the whole
    sentence stays up under every piece if it fits on one line, else the cuts without a stop fall
    back to the best word gap. Returns (pieces, repeated): repeated = the whole sentence is shown
    under every Chinese piece."""
    k = len(zp)
    e = " ".join(e.split())
    if k == 1:
        return [e], False
    zu = [units(re.sub(r"（[^（）]*）", "", p)) for p in zp]  # the glosses have no English
    share = [u / (sum(zu) or 1) * units(e) for u in zu]      # how long each piece would be ...
    targets = [sum(share[:j]) for j in range(1, k)]          # ... and where it would end
    good, _ = _cuts(e)
    whole = units(e) <= 1.15 * limit
    cap = (0.25 if whole else 0.35) * units(e)              # how far a clause stop may be

    def mismatch(c, prev, j):
        """Numbers and symbols on the wrong side of a cut at c, for the j-th Chinese cut."""
        rest = "".join(zp[j + 1:])
        a, b, za, zb = _symbols(e[prev:c]), _symbols(e[c:]), _symbols(zp[j]), _symbols(rest)
        return sum(((a - za) + (za - a) + (b - zb) + (zb - b)).values())

    def stop_cost(c, j, target, misplaced):
        mark, zmark = e[:c].rstrip()[-1:], zp[j].rstrip()[-1:]
        if mark not in ",;:.!?—" or (_list_comma(e, c) and zmark != "、"):
            return None
        if abs(units(e[:c]) - targets[j]) > min(abs(units(e[:c]) - t) for t in targets):
            return None                                    # nearer to another Chinese cut
        cost = abs(units(e[:c]) - target) + 1.5 * misplaced  # 3 units per number on the wrong side
        cost += 4 if zmark in "，、" and mark in ";:—" else 0  # "上限，/ 从而" is not "sensitivity; / add"
        return cost if cost <= min(cap, max(4, min(share[j], share[j + 1]) / 2)) else None

    def pieces_of(cuts):
        return [e[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(e)])]

    def clean_gap(c, j):
        """A plain word gap right at the Chinese cut, before a preposition, auxiliary or
        conjunction: "…between the tents / can never exceed…"."""
        nxt = (e[c:].split() or [""])[0].lower()
        return (e[c - 1] == " " and e[c - 2].isalnum() and _cut_penalty(e, c) <= 4
                and abs(units(e[:c]) - targets[j]) <= 0.1 * units(e)
                and nxt in (_FUNCTION_WORDS - _DETERMINERS - {"of"}) | _CLAUSE_STARTERS)

    best, prev = [], 0
    for j in range(k - 1):
        pool = [c for c in good if c > prev]
        miss = {c: mismatch(c, prev, j) for c in pool}
        floor = min(miss.values(), default=0)
        span = [units(e[:c]) for c in pool if miss[c] == floor] or [targets[j]]
        pinned = min(max(targets[j], min(span)), max(span))     # where the numbers allow the cut
        scored = [((miss[c], cost), c) for c in pool if units(e[prev:c].strip()) <= 1.15 * limit
                  and (cost := stop_cost(c, j, pinned if miss[c] == floor else targets[j],
                                         miss[c] - floor)) is not None]
        if not scored:                                     # no stop: a clean gap will do
            scored = [((0, abs(units(e[:c]) - targets[j])), c) for c in pool
                      if miss[c] == floor and clean_gap(c, j)]
        best.append(min(scored)[1] if scored else None)
        prev = best[-1] or prev
    if all(best):
        pieces = pieces_of(best)
        if all(p and units(p) <= 1.15 * limit for p in pieces):
            return pieces, False
    if whole:
        return [e] * k, True
    cuts, prev = [], 0
    for j, c in enumerate(best):                           # too long for one line: best gap, for
        if c is None:                                      # the cuts without a clause stop only
            upper = next((x for x in best[j + 1:] if x), len(e))
            pool = [x for x in good if prev < x < upper]
            if not pool:
                break
            c = min(pool, key=lambda x: (mismatch(x, prev, j),
                                         abs(units(e[:x]) - targets[j]) + _cut_penalty(e, x)))
        cuts.append(c)
        prev = c
    pieces = pieces_of(cuts)
    if len(pieces) == k and all(p and units(p) <= 1.15 * limit for p in pieces):
        return pieces, False
    return _split_k(e, k, limit), False


def _two_lines(cue, limit: float) -> list[tuple[float, float, str]]:
    """A cue wrapped to at most 2 lines; a piece that needs more becomes two cues (time split
    in proportion to their length), cut at a clause boundary when one gives two 2-line cues. Two
    lines that split a list at its 、 ("光凭邮编、/ 出生日期和性别") also become two cues when a clause
    cut gives two 2-line cues."""
    a, b, text = cue
    text = strip_end(text)
    lines = split_balanced(text, limit)

    def listy(t):                                         # two lines that split a list at its 、
        ls = split_balanced(t, limit)
        return len(ls) == 2 and t[:len(t) - len(t[len(ls[0]):].lstrip())].rstrip()[-1:] == "、"

    if len(lines) == 1 or (len(lines) == 2 and not listy(text)):
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
        at_stop = text[c - 1] in stops or (text[c - 1] == " " and text[c - 2] in stops)
        clean = (at_stop and left[-1:] in "，；：。！？,;:.!?" and min(units(left), units(right)) >= limit / 3
                 and not listy(strip_end(left)) and not listy(right))
        if len(lines) == 2 and not clean:
            continue                                      # instead of a 、 split: two clean clause cues
        cost = abs(units(left) - units(right)) + _cut_penalty(text, c) + _mark_cost(text, c)
        cost += 0 if at_stop else 20
        if min(units(left), units(right)) < limit / 3:
            cost += 15                                    # an orphan cue: "First:" / "真实答案为 0；"
        if best is None or cost < best[0]:
            best = (cost, [left, right])
    if len(lines) == 2 and best is None:
        return [(a, b, "\n".join(lines))]
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
    """Split into exactly k balanced pieces (fewer pieces are padded by splitting the longest in
    two, joining its sub-pieces where the halves balance best: "一个亿万富翁，就能让答案变动 10 亿，
    / 不封顶就根本没有上限", not "一个亿万富翁 / 就能……")."""
    pieces = split_balanced(text, limit, hang=True)
    while len(pieces) < k:
        i = max(range(len(pieces)), key=lambda j: units(pieces[j]))
        sub = split_balanced(pieces[i], units(pieces[i]) / 2 + 0.6, hang=True)
        if len(sub) < 2:
            pieces.append(pieces[-1])                     # nothing to cut: the line stays up
            continue
        halves = [(reduce(join_pieces, sub[:j]), reduce(join_pieces, sub[j:])) for j in range(1, len(sub))]
        pieces[i:i + 1] = min(halves, key=lambda h: abs(units(h[0]) - units(h[1])))
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
