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
    """Display width in 'CJK character' units (a Latin character is about half as wide), rounded
    so that 48 Latin characters fit a 48 * 0.55 limit (the float sum is 26.40000000000002)."""
    return round(sum(1.0 if _CJK.match(ch) else 0.55 for ch in s), 6)


def _cuts(text: str, lines: bool = False) -> tuple[list[int], list[int]]:
    """Positions where a line or cue may break. 'good': after punctuation, and at spaces between
    Latin words. 'ok': between two CJK characters, at a space next to CJK text, or anywhere inside
    “…” or （…） (a last resort, see _cut_penalty). Never inside a number (255,168 / 0.5), between
    a number and its measure word (5 步), inside 《…》 (but at its spaces, as a last resort),
    before punctuation, after an opening bracket or before a bracket glued to the word it glosses
    (hybrid argument（混合论证）), except, between the `lines` of one cue, an English gloss of a
    Chinese term (差分隐私 / （differential privacy）: both lines are on screen together)."""
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
        if b in "（(" and a != " " and a not in _BREAK_AFTER:
            if lines and is_cjk(a) and re.match(r"[（(][A-Za-z]", text[i:]):
                ok.append(i)                                  # 差分隐私 / （differential privacy）
            continue
        if b in _NO_LINE_START or a in _OPENERS:
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
            if (p.isdigit() and is_cjk(b)) or (p in "第约" and b.isdigit()):
                continue                                      # "5 步", "第 4 节"
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


# an English line should not end on one of these ("by a / billion", "scrambles their own / row",
# "changes across / coordinates", "A published release cannot / know")
_AUXILIARIES = {"is", "are", "was", "were", "be", "been", "being", "has", "have", "had", "do", "does",
                "did", "can", "could", "will", "would", "shall", "should", "may", "might", "must",
                "cannot", "can't", "won't", "don't", "doesn't", "didn't", "isn't", "aren't", "wasn't",
                "weren't", "couldn't", "wouldn't", "shouldn't", "hasn't", "haven't", "hadn't"}
_PREPOSITIONS = {"of", "to", "by", "in", "on", "at", "for", "with", "from", "as", "into", "per", "than",
                 "against", "across", "like", "about", "between", "over", "through", "after", "before",
                 "without", "within", "under", "onto", "upon", "toward", "towards", "among", "along",
                 "around", "beyond", "during", "since", "via"}
_FUNCTION_WORDS = (_AUXILIARIES | _PREPOSITIONS |
                   {"a", "an", "the", "and", "or", "nor", "its", "their", "his", "her", "our", "your",
                    "my", "own", "that", "if", "but", "so", "not", "no", "each", "every", "until",
                    "unless", "whether", "where", "when", "while", "whose", "what", "which", "who",
                    "whom", "because", "though", "although"})
_NUMBER_WORDS = {"one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
                 "eleven", "twelve"}
_NUMBER = re.compile(r"\d+(?:[.,]\d+)*%?|(?:twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)"
                     r"(?:-(?:one|two|three|four|five|six|seven|eight|nine))?|" + "|".join(_NUMBER_WORDS))
_PRONOUNS = {"it", "we", "they", "he", "she", "you", "i"}
_ADVERBS = {"now", "also", "still", "only", "never", "always", "just", "even", "then", "really", "often",
            "first"}
_TERM_STOP = _FUNCTION_WORDS | _PRONOUNS | _ADVERBS | {"this", "one", "itself", "how", "many", "first",
                                                       "once", "yourself", "further", "early", "yes", "vs"}
_ADJECTIVES = {"random", "true", "whole", "next", "odd", "same", "real", "small", "large", "tiny", "huge",
               "new", "simple", "public", "private", "single", "full", "empty", "entire", "exact", "raw",
               "big", "high", "low", "few", "other", "last", "best", "worst", "own", "flat", "steep", "broad",
               "strong", "weak", "sharp", "wide", "narrow", "short", "long", "deep", "fair", "clean",
               "sharper", "earlier", "larger", "smaller", "bigger", "higher", "lower", "steeper", "weaker",
               "stronger", "simpler", "better", "greater", "wider", "closer", "later", "different",
               "independent", "consistent", "efficient", "important", "constant"}
_MODIFIER = re.compile(r"[a-z-]+(?:ed|ing|ive|ous|ful|ic|able|ible|est|less|al)")
_NOT_MODIFIERS = {"signal", "interval", "trial", "animal", "proposal", "need", "seed", "speed", "thing",
                  "nothing", "something", "anything", "everything", "string", "king", "ring", "logic"}


def _modifier(w: str) -> bool:
    """A word that looks like it modifies the noun after it (randomized, sharper, interactive, true)."""
    w = w.lower().rstrip(",")
    return w in _ADJECTIVES or (bool(_MODIFIER.fullmatch(w)) and w not in _NOT_MODIFIERS)


_EN_COMPOUNDS = {("deep", "learning"), ("neural", "network"), ("computer", "scientists"), ("birth", "date"),
                 ("zip", "code"), ("interactive", "curator"), ("computer", "program")}


@lru_cache(maxsize=1)
def _en_terms() -> frozenset[tuple[str, str]]:
    """Word pairs inside the English terms of videos/*/i18n/zh/glossary.yaml (each 2-3 word
    alternative of a term's en field: counting query, privacy budget, Laplace mechanism), which a
    line break should not split."""
    import yaml

    out = set(_EN_COMPOUNDS)
    for g in sorted((Path(__file__).resolve().parent.parent / "videos").glob("*/i18n/zh/glossary.yaml")):
        for t in (yaml.safe_load(g.read_text(encoding="utf-8")) or {}).get("terms") or []:
            for alt in re.split(r"[/;,:]", re.sub(r"\([^()]*\)", "", str(t.get("en") or ""))):
                ws = [w.lower() for w in alt.split()]
                if 2 <= len(ws) <= 3 and all(re.fullmatch(r"[a-z]{2,}", w) for w in ws) and not _TERM_STOP & set(ws):
                    out.update(zip(ws, ws[1:]))
    return frozenset(out)


def _in_term(text: str, c: int) -> bool:
    """The word gap before position c is inside a glossary term ("counting / query")."""
    a = text[:c].split()[-1:] or [""]
    b = text[c:].split()[:1] or [""]
    return (a[0].lower(), b[0].lower().rstrip(",.;:!?")) in _en_terms()


# a word that starts a clause: a cut before it (", which" / " and") lines up with a Chinese clause
_CLAUSE_STARTERS = {"and", "but", "or", "so", "yet", "which", "who", "whose", "what", "where", "when",
                    "while", "because", "then", "that", "if", "unless", "until", "whether", "although",
                    "though", "as"}
_SUBORDINATORS = {"if", "when", "unless", "whether", "because", "that", "where", "while", "until",
                  "although", "though", "than", "since", "whose", "which", "who"}
_DETERMINERS = {"a", "an", "the", "this", "that", "these", "those", "its", "their", "his", "her",
                "our", "your", "my", "each", "every", "one", "another", "any", "some", "all"}


# nor start with one of these ("single / out", "whatever / else")
_PARTICLES = {"out", "up", "off", "away", "back", "down", "else"}


# a Chinese line should not end on a preposition / conjunction ("统计从 / 现在这个棋盘"), a 的 that
# belongs to the next noun ("公开的 / 选民名单") or a negation, or start with a particle
_CJK_NO_END = set("从把在对给向跟和与被让将比以于为及或而但且的不没叫")   # 叫: "标题就叫 / 《…》"
_CJK_NO_START = set("的了着过地得们吗呢吧啊")
_CJK_NO_END_WORDS = re.compile(r"[这那每某哪一两几][个些种条份篇项位张件句段组批]$")   # "把这些 / query", "算一个 / counting query"
_CJK_NO_START_WORDS = ("以内", "以上", "以下", "以外", "之间", "之内", "之外")         # "clip 到 C / 以内"
_TITLE = re.compile(r"《[^《》]*》")
_GLOSS = re.compile(r"[A-Za-z][A-Za-z' -]*(?=[，；。]|$)")    # a spoken English gloss: "，sensitivity；"


# terms jieba splits (差分/隐私, 深度/网络, 不/可能) but a line must keep whole; the headwords of every
# video's glossary are added to them (_glossary_terms)
_TERMS = ("差分隐私", "本地化差分隐私", "深度网络", "不可能", "隐私预算", "拉普拉斯机制", "组合定理",
          "指数机制", "最小割", "比特串", "训练集")
_NOT_WORDS = ("是从",)          # jieba's dictionary has them, but they are two words: 指的是 / 从第一步
_TERM_EDGE = set("的了在是和与或被把对个种局条次步年第为到后再越先也都就")   # not a term's first or last character
_TERM_START = _TERM_EDGE | set("让想算占以除那一两已多共")      # 让可信, 想要大范围, 一个极小, 那条公式: phrases
_TERM_END = _TERM_EDGE | set("时中里下过出好起来去")            # 列表里, 括号下, 手算过, 估计出, 训练好
_TERM_INNER = set("的地得了着过就叫有为只再后是之那这不没也都又还被把将从向对在和与或及而但且吗呢吧啊么每越到")
_TERM_NOTES = ("保持", "保留", "不变", "注意", "标签", "卡片", "字幕", "原样", "括注", "首次", "文档")


def _glossary_terms() -> list[str]:
    """Headwords of videos/*/i18n/zh/glossary.yaml: each alternative of a term's zh_subtitle (split
    at ； and /, without its （…） note or a symbol beside it: 机制 M, ε-不可区分性; split at a 的:
    公开的选民名单 → 公开, 选民名单) that is a run of 2-7 CJK characters with no particle, preposition
    or adverb inside or at its edges, not starting on a verb, numeral or demonstrative (让可信, 一个极小,
    那条公式) nor ending on a postposition or complement (列表里, 括号下, 估计出). Not every CJK run of
    the field: it also holds example phrases
    and editorial notes (标题就叫…, 字幕不用…), which would make jieba keep a phrase like 标题就叫
    together and move a line break to a worse place."""
    import yaml

    out = []
    for g in sorted((Path(__file__).resolve().parent.parent / "videos").glob("*/i18n/zh/glossary.yaml")):
        for t in (yaml.safe_load(g.read_text(encoding="utf-8")) or {}).get("terms") or []:
            for alt in re.split(r"[；;]|/", str(t.get("zh_subtitle") or "")):
                alt = re.split(r"[（(]", alt, maxsplit=1)[0].strip()
                alt = re.sub(r"^[A-Za-zα-ωΑ-Ω0-9()′'.-]+[\s-]+|\s+[A-Za-zα-ωΑ-Ω0-9()′'.]+$", "", alt)
                for w in alt.split("的"):                        # 公开的选民名单: 选民名单
                    if (re.fullmatch(r"[一-鿿]{2,7}", w) and w[0] not in _TERM_START and w[-1] not in _TERM_END
                            and not _TERM_INNER & set(w[1:-1]) and not any(n in w for n in _TERM_NOTES)):
                        out.append(w)
    return list(dict.fromkeys(out))


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
    for w in _NOT_WORDS:
        jieba.del_word(w)
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


def _cut_penalty(text: str, c: int, lines: bool = False) -> float:
    """Extra cost (in units) of cutting at position c. English (at a word gap): a plain gap costs
    more than a cut after punctuation, a gap after a function word or next to a number much more.
    Chinese: a cut after a preposition or before a particle costs a lot. Both: a cut inside “…”
    or （…） costs a little (a lot at a cue boundary), one inside a 《…》 title more (cut before
    the 《 instead). `lines`: the cut is a line break inside a cue, not a cue boundary."""
    head = text[:c]
    cost = 0.0
    if head.count("“") + head.count("（") > head.count("”") + head.count("）"):
        cost += 5.0 if lines else 15.0                    # a cue boundary inside a gloss: "（混合 // 论证）"
    if head.count("《") > head.count("》"):
        cost += 10.0
    a, b = text[c - 1], text[c] if c < len(text) else ""
    if is_cjk(a) or is_cjk(b) or (a == " " and is_cjk(text[c - 2:c - 1] or " ")):
        before, after = head.rstrip(), text[c:].lstrip()
        bad_end = before[-1:] in _CJK_NO_END or _CJK_NO_END_WORDS.search(before)
        bad_start = after[:1] in _CJK_NO_START or (after.startswith(_CJK_NO_START_WORDS)
                                                   and before[-1:] not in _BREAK_AFTER)
        names = re.match(r"[和与及] [A-Z]", after) and before[-1:].isascii() and before[-1:].isalpha()
        clause = re.split(r"[，。、；：！？]", before)[-1]
        span = "从" in clause and "到" in clause[clause.rfind("从"):] + re.split(r"[，。、；：！？]", after)[0]
        if bad_end or bad_start or names or span:         # names: "Rothblum / 和 Vadhan"; span: "从第一步 / 到最后一步"
            cost += 6.0
        if before[-1:] in "，、" and _GLOSS.match(after):
            cost += 20.0                                  # "隐私预算 / privacy budget。": keep the gloss
        if b in "（(" and a != " ":
            cost += 2.0                                   # a line break before its English gloss
        if not lines and before[-1:] == "，" and _short_gloss(after):
            cost += 6.0                                   # a cue boundary before it: "边格 // 也就是……"
        bounds = _word_bounds(text) if is_cjk(a) and is_cjk(b) else None
        if bounds is not None and c not in bounds:
            cost += 8.0                                   # inside a word: 现|在
        return cost
    if a != " ":
        return cost
    prev = text[:c - 1].rsplit(" ", 1)[-1]
    if not prev[-1:].isalnum():
        return cost
    words = text[:c - 1].split()
    low, nxt = prev.lower(), text[c:].split(" ", 1)[0]
    word = nxt.rstrip(",.;:!?").lower()
    content = (word.isalpha() and nxt[:1].islower()
               and word not in _FUNCTION_WORDS | _CLAUSE_STARTERS | _DETERMINERS | _PRONOUNS)
    short_clause = word in _AUXILIARIES and _SUBORDINATORS & {w.lower() for w in words[-4:-1]}
    if low not in _FUNCTION_WORDS and (word in _CLAUSE_STARTERS | _AUXILIARIES | _PREPOSITIONS - {"of"}
                                       and not _list_and(text, c) and not short_clause):
        cost += 1.0                                       # before a clause, verb or phrase: "…table / and walking away"
    else:                                                 # (not "if the true count / is 42")
        cost += 4.0
    if (re.search(r", \S+ $", text[:c]) and re.match(r"\S+,? (?:and|or) ", text[c:])
            and _list_comma(text, text[:c].rstrip().rfind(",") + 1)):
        cost += 4.0                                       # inside a list item: "ZIP code, birth / date and sex"
    if low in _FUNCTION_WORDS:
        cost += 8.0
    elif (len(words) > 1 and words[-2].lower() in _AUXILIARIES - {"is", "are", "was", "were", "be", "been", "being"}
          and (low in _ADVERBS or low.endswith("ly"))):
        cost += 8.0                                       # "can now / move", "would actually / use"
    elif low in _PRONOUNS and len(words) > 1 and words[-2].lower() in _CLAUSE_STARTERS | {"so", "then"}:
        cost += 8.0                                       # "so it / counts"
    if prev[:1].isupper() and len(words) > 1 and (b.isupper() or re.match(r"(and|or) [A-Z]", text[c:])):
        cost += 8.0                                       # names: "Kobbi / Nissim", "Nissim / and Adam"
    if _in_term(text, c):
        cost += 8.0                                       # a glossary term: "counting / query"
    if word in _PARTICLES:
        cost += 6.0                                       # "single / out", "whatever / else"
    if low in _PARTICLES and (content or word in _DETERMINERS):
        cost += 3.0                                       # its object: "single out / most Americans"
    poss = next((j for j in range(len(words) - 1, max(-1, len(words) - 4), -1)
                 if words[j].endswith(("'s", "’s"))), None)
    if poss is not None and content and all(_modifier(w) for w in words[poss + 1:]):
        cost += 6.0                                       # "Alice's / row", "curator's randomized answering / rule"
    elif (content and len(words) > 1 and _modifier(prev)  # (not "any one person's row / changes")
          and (words[-2].lower() in _DETERMINERS | _PREPOSITIONS or _NUMBER.fullmatch(words[-2].lower())
               or _modifier(words[-2]))):
        cost += 8.0                                       # an adjective and its noun: "its published / tables",
                                                          # "for broad, flexible / accuracy"
    verbal = word in _AUXILIARIES | _CLAUSE_STARTERS | _PREPOSITIONS and word not in ("of", "to", "and", "or")
    if b.isdigit() or word in _NUMBER_WORDS or (prev[-1:].isdigit() and not verbal):
        cost += 4.0                                       # "on move / 6", "9 times / 8", "at most / one"
    if _NUMBER.fullmatch(low) and (content or re.match(r"(and|or) (a |\d|(%s)\b)" % "|".join(_NUMBER_WORDS),
                                                       text[c:])):   # (not "8 or 9 / have")
        cost += 8.0                                       # "at most one / empty square", "fifty-two / and a half"
    if low in ("even", "only", "just") and word in ("if", "though", "when", "as", "after", "before", "because"):
        cost += 8.0                                       # "even / if Alice's row…"
    if word == "as" and len(words) > 1 and words[-2].lower() == "as":
        cost += 8.0                                       # "as soon / as", "as long / as"
    if any(m.start() < c - 1 < m.end() for m in re.finditer(r"\S+ to the power of \S+", text)):
        cost += 8.0                                       # "10 to the power / of 120"
    elif "-" in prev.strip("-") and prev.islower() and content:
        cost += 4.0                                       # "the two-question / version"
    return cost


_STRONG = "。！？；：.!?;:—…"


def _short_gloss(after: str) -> bool:
    """`after` starts with a short explanation of the term before the comma: 意思是“赢家”, 也就是 1,
    也就是每条边正中间的那一格 (not a whole clause: 也就是改变一条记录最多能让答案变化多少)."""
    gloss = re.match(r"(?:意思是|也就是|就是说|即)[^，。！？；：]*(?=[，、])", after)   # not the end of the
    return bool(gloss) and units(gloss.group()) <= 14             # sentence: "乘 1，/ 也就是 24 种不同的顺序。"


def _mark_cost(text: str, c: int) -> float:
    """Weight of the mark a cut at c follows, so that the stronger mark wins when the balance is
    close: none after 。！？；：. ! ? ; : — …, 3 after a comma (or no mark at all), 8 after a comma
    that leaves a short clause before a 。；！？ (the cut belongs there), after a short lead-in that
    follows one (；在 Python 里，), before a short clause that continues the one before it (想……，
    又要强隐私，; 有人说数据集匿名化了，所以很安全，) or before a short gloss (winner，意思是“赢家”;
    边格，也就是每条边正中间的那一格), 6 after 、 (it splits a list: 光凭邮编、/ 出生日期), 10 after a 、 between two Latin names (Dwork、/ Rothblum) or a comma
    between two numbers (moves 7, / 8 and 9), two names or adjectives (Dwork, / Rothblum; broad, /
    flexible accuracy) or before a short appositive (f(x), / 41,; noise, / Y,)."""
    head = text[:c].rstrip()
    if head[-1:] in _STRONG:
        return 0.0
    nxt = text[c:].lstrip()[:1]
    if head[-1:] == "、":
        names = head[-2:-1].isascii() and head[-2:-1].isalpha() and nxt.isascii() and nxt.isalpha()
        return 10.0 if names else 6.0
    if head[-1:] == "," and head[-2:-1].isdigit() and nxt.isdigit():
        return 10.0                                        # a list of numbers: "moves 7, / 8 and 9"
    if head[-1:] == "," and (_list_comma(text, c) or re.match(r"([^\s,]*\d[^\s,]*|[A-Z]),(?:\s|$)", text[c:].lstrip())):
        return 10.0                                        # "Dwork, / Rothblum", "broad, / flexible", "f(x), / 41,"
    end = re.search(r"[。！？；.!?;]|$", text[c:])
    if head[-1:] in "，," and units(text[c:c + end.start()]) <= 7.5:
        return 8.0                  # a clause end a few characters on: "偶数个 1，/ 真实答案为 0；"
    if head[-1:] == "，":
        start = max(head.rfind(m, 0, len(head) - 1) for m in "。！？；：")
        if start >= 0 and units(head[start + 1:-1]) <= 7:
            return 8.0              # a short lead-in after a strong mark: "叫 Python；在 Python 里，/ 列表……"
        nxt_clause = re.match(r"(?:又|也|还|而且|并且|所以|却|但)[^，。！？；：、]*(?=，)", text[c:].lstrip())
        if nxt_clause and units(nxt_clause.group()) <= 6:
            return 8.0              # a short clause that continues this one: "想对各种问题都答得准，/ 又要强隐私，",
                                    # "数据集匿名化了，/ 所以很安全，你就知道……"
        if _short_gloss(text[c:].lstrip()):
            return 8.0              # a short gloss stays with its term: "叫 winner，/ 意思是“赢家”"
    return 3.0


def _pick_cuts(text: str, k: int, pool_of, total: float, lines: bool = False) -> list[int] | None:
    cuts, prev = [], 0
    for j in range(1, k):
        ideal_u = total * j / k
        pool = pool_of(prev, ideal_u, j == k - 1)
        if not pool:
            return None
        cut = min(pool, key=lambda c: abs(units(text[:c]) - ideal_u) + _cut_penalty(text, c, lines)
                  + _mark_cost(text, c))
        cuts.append(cut)
        prev = cut
    return cuts


# a word that starts a clause, for an English cue cut that has no punctuation ("…most Americans,
# / and in 1997 she linked … / and found the governor")
_CLAUSE_WORDS = {"and", "but", "or", "so", "yet", "which", "who", "whose", "what", "where", "when", "while",
                 "because", "then", "unless", "until", "if", "although", "though", "whereas", "whether"}


def _list_and(text: str, c: int) -> bool:
    """A gap before the 'and' / 'or' that closes a list: "ZIP code, birth date / and sex" (not
    "Over the following decades, statisticians / and computer scientists")."""
    m = re.match(r"(and|or) ", text[c:]) and re.search(r",( \S+){1,3} $", text[:c])
    return bool(m) and _list_comma(text, m.start() + 1)


def split_balanced(text: str, limit: float, hang: bool = False, clauses: bool = False,
                   line: float = 0.0) -> list[str]:
    """Fewest pieces of at most `limit` units each, balanced in length. Cuts at sentence marks
    (；。！？ ; . ! ?) when those alone give pieces that fit and none is tiny (a ；-structured
    sentence keeps one clause per piece; not ：, which often binds a short lead-in to what follows:
    分成两种思路：要么……), else at any punctuation whenever the pieces still fit
    (even if unbalanced, but not leaving a stray scrap at a comma), preferring the stronger mark
    (_mark_cost), else at the best word gap or between CJK characters; English pieces avoid ending
    on an article or preposition, Chinese pieces on a preposition. `clauses` (English cues): before
    a word gap, also try a gap before and / but / which … (not the 'and' of a list), and one more
    piece cut at punctuation, so that a cue boundary does not fall mid-phrase. `hang`: the pieces
    are cues, whose final ，。、；： is dropped (strip_end), so it does not count against the limit; a
    Chinese cue does not run on across a ；。！？ in mid-line (in lines of `line` units, default
    `limit`) when one cue more avoids it;
    and a whole 《…》 title may run 5 units over it (a 30-unit bilingual line is about 1040 px of the
    1840 px line at 1080p, measured with burn())."""
    text = " ".join(text.split())
    if units(strip_end(text) if hang else text) <= limit:
        return [text]
    lines = not hang
    good, ok = _cuts(text, lines=lines)
    stops = "，；：。！？,;:.!?…—"                     # not after 、, a closing quote or bracket
    punct = [c for c in good if _cut_penalty(text, c, lines) == 0 and text[c - 1] in stops + " "
             and (text[c - 1] != " " or text[c - 2] in stops)
             and (hang or clauses or _mark_cost(text, c) < 10)]   # a line does not break at "broad, / flexible"
    strong = [c for c in punct if text[:c].rstrip()[-1:] in "；。！？;.!?"
              and not (text[:c].rstrip()[-1:] == "." and text[c:c + 1].islower())]
    clause = sorted(set(punct) | {c for c in good if clauses and text[c - 1] == " " and text[c - 2].isalnum()
                                  and _clean_break(text, c)})
    total = units(text)

    def pieces_of(cuts):
        return [text[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(text)])]

    def fits(p):
        q = strip_end(p) if hang else p
        return p and (units(q) <= limit or (hang and _TITLE.fullmatch(q) and units(q) <= limit + 5))

    def fitting(cands):
        """Cuts of `cands` after prev whose piece fits (and the rest, for the last cut)."""
        return lambda prev, ideal, last: [c for c in cands if c > prev and fits(text[prev:c].strip())
                                          and (not last or fits(text[c:].strip()))]

    def stray(cuts, pieces):
        """A piece of a few characters cut off at a comma: "2016 年，/ Abadi 和合作者……", "…the
        honest answer, / f(x)." (under a quarter of the longest piece in Chinese, a sixth in English)."""
        short = max(units(p) for p in pieces) / (4 if _CJK.search(text) else 6)
        commas = [text[:c].rstrip()[-1:] in "，、," for c in cuts]   # the cut after each piece
        return any(units(p) < short and any(commas[max(0, j - 1):j + 1]) for j, p in enumerate(pieces))

    def straddles(pieces):
        """A Chinese cue that runs on across a ；。！？ between two clauses in mid-line ("在每个数据库上都是
        这样；那么 f 的敏感度最多是两倍 σ"): one cue more keeps one clause per cue."""
        if not (hang and _CJK.search(text)):
            return False
        rows = [r for p in pieces for r in (split_balanced(strip_end(p), line) if line and line < limit
                                            else [strip_end(p)])]
        return any(units(r[:m.start()]) >= 4 and units(r[m.end():].strip()) >= 4
                   for r in rows for m in re.finditer(r"[；。！？]", r))

    def gaps(k):
        """Word gaps near the ideal position (those that leave pieces that fit first: "the US Census
        Bureau protected / its published tables…", not a third line), else anywhere. Only near ones:
        a cut anywhere that fits is often inside a word, where one piece more is better."""
        def pool(prev, ideal, last):
            near = [c for c in good if c > prev and abs(units(text[:c]) - ideal) <= total / (2.5 * k)
                    and text[c - 1] != "、"]
            fit = [c for c in near if fits(text[prev:c].strip()) and (not last or fits(text[c:].strip()))
                   and _cut_penalty(text, c, lines) < 10]       # not "…one release that is / accurate…"
            return fit or near or [c for c in ok + good if c > prev]
        return pool

    def attempt(k, kind):
        pool_of = {"strong": fitting(strong), "punct": fitting(punct), "whole": fitting(punct),
                   "clause": fitting(clause)}.get(kind) or gaps(k)
        cuts = _pick_cuts(text, k, pool_of, total, lines)
        if cuts is None:
            return None
        pieces = pieces_of(cuts)
        if not all(fits(p) for p in pieces):
            return None
        sizes = [units(p) for p in pieces]
        if kind == "strong" and min(sizes) < limit / 4:
            return None                                   # not "第二：/ ……"
        if kind in ("punct", "whole") and stray(cuts, pieces):
            return None
        if kind == "whole" and straddles(pieces):
            return None
        if kind == "clause" and min(sizes) < max(sizes) / 3:
            return None
        return pieces

    for k in range(2, 40):
        plan = [(k, "strong"), (k, "punct")]
        if hang:                                          # whole clauses first, at one cue more if need be
            plan = [(k, "strong"), (k, "whole"), (k + 1, "strong"), (k + 1, "whole"), (k, "punct")]
        if clauses:
            plan += [(k, "clause"), (k + 1, "strong"), (k + 1, "punct"), (k + 1, "clause")]
        for kk, kind in plan + [(k, "gaps")]:
            pieces = attempt(kk, kind)
            if pieces:
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


def _spoken_parts(text: str, pieces: list[str], spoken: str) -> list[str] | None:
    """The part of the spoken sentence that each piece of `text` stands for, by a character
    alignment of the two forms (2016 年 / 二零一六年, e^ε / E 的艾普西隆次方; a gloss （计数查询）
    that is not read gets nothing). None when a piece cannot be found in `text` or gets nothing."""
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
    parts = [spoken[x:y] for x, y in zip(cuts, cuts[1:])]
    return parts if all(units(q) > 0 for q in parts) else None


def _spoken_weights(text: str, pieces: list[str], spoken: str) -> list[float] | None:
    """How long each piece of `text` takes to say: the units of its part of the spoken sentence
    (_spoken_parts). units() of the spoken text predicts the Xiaoyi sentence durations better than
    units() of the display text (R² 0.975 against 0.954 over the 417 sentences of both videos)."""
    parts = _spoken_parts(text, pieces, spoken)
    return [units(q) for q in parts] if parts else None


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
    - A cue still shorter than `min_dur` takes time from a contiguous neighbour (up to 0.2 s
      per unit of its first line, at most 1.5 s), as long as the neighbour keeps its own minimum.
    - Single-language cues have at most 2 lines; a longer piece becomes two cues (timed by the
      spoken form too), and an English cue whose two lines break mid-phrase becomes two cues
      when a clause cut gives cleaner lines.
    - In the bilingual track, the English sentence is cut where the Chinese one is (at the
      matching clause boundary, see _split_like); when it fits on one line and no boundary is
      close, the whole English sentence stays up under each Chinese piece.
    - Every cue stays up at least `min_show` seconds when the next cue leaves room."""
    zh, en, bi = [], [], []
    for n, (a, b, t, e, *say) in enumerate(pairs):
        spoken = say[0] if say and say[0] and timing == "tr" else None
        if t:
            zs = split_balanced(t, 2 * zh_limit, hang=True, line=zh_limit)
            parts = (spoken and _spoken_parts(t, zs, spoken)) or [None] * len(zs)
            times = _proportional(a, b, zs, parts[0] and [units(q) for q in parts])
            zh += [(s0, s1, z, q) for (s0, s1, z), q in zip(times, parts)]
        en += _proportional(a, b, split_balanced(e, 2 * en_limit, clauses=True))
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
    zh = _stretch([c for x in zh for c in _two_lines(x, zh_limit, min_dur)], min_dur)
    en = _stretch([c for x in en for c in _two_lines(x, en_limit, min_dur)], min_dur)
    bi = _stretch([(s0, s1, strip_end(z), e) for s0, s1, z, e, _ in bi], min_dur)
    return {"zh": _linger(zh, min_show), "en": _linger(en, min_show), "zh-en": _linger(bi, min_show)}


def _symbols(s: str) -> Counter:
    """Numbers and symbols of a piece (41, 52.5, 1/λ, e^ε → ε, x′ → ′), to match the English and
    the Chinese pieces of a bilingual cue."""
    return Counter(re.findall(r"\d+(?:[.,/]\d+)*|[^\x00-\x7f　-〿一-鿿＀-￯’‘“”—…]", s))


_INTRO = _PREPOSITIONS | _CLAUSE_WORDS | {"then", "now", "first", "second", "third", "next", "finally",
                                          "instead", "tails", "heads", "here", "there"}
_LIST_ITEM = r"(?:\d[\w.]*|[A-Za-z][\w′'-]*)"


_ZH_CONJ = {"而且": "and", "并且": "and", "但是": "but", "但": "but", "却": "but", "不过": "but", "可是": "but",
            "所以": "so", "因此": "so", "于是": "so", "如果": "if", "假如": "if", "要是": "if", "因为": "because",
            "直到": "until", "除非": "unless", "那么": "then", "然后": "then"}
_EN_CONJ = {"and": "and", "but": "but", "yet": "but", "though": "but", "so": "so", "if": "if",
            "because": "because", "until": "until", "unless": "unless", "then": "then"}


def _connectives(s: str) -> Counter:
    """Clause connectives of a piece, to match the English and Chinese pieces of a bilingual cue:
    而且 / and, 但 / but, yet, 所以 / so, 如果 / if, 那么 / then … at the start of a clause."""
    if _CJK.search(s):
        alts = "|".join(sorted(_ZH_CONJ, key=len, reverse=True))
        return Counter(_ZH_CONJ[m] for m in re.findall(r"(?:^|(?<=[，；：。]))(%s)" % alts, s.strip()))
    return Counter(_EN_CONJ[m.lower()] for m in re.findall(r"(?:^|(?<=[,;:.] ))(%s)\b" % "|".join(_EN_CONJ),
                                                            s.strip(), flags=re.I))


def _list_comma(e: str, c: int) -> bool:
    """A comma inside a list rather than at a clause boundary. Either the list closes with and / or
    a word or two later ("ZIP code, / birth date and sex"; "symmetric, / sharply peaked, and falling
    off"), its items being plain words, and what comes before the comma is not an opening phrase
    ("In 1950, / the mathematician and engineer", "If no line matches, / winner finds…"); or the
    comma ends a run of at most two words that does not start the sentence, and joins two
    capitalised words ("with Kenthapadi, McSherry, Mironov") or a run that is not a noun phrase to a
    lowercase content word ("for broad, flexible accuracy"; not "the curator, holds")."""
    head = e[:c].rstrip()
    if not head.endswith(","):
        return False
    runs = re.split(r"[,;:.!?—]\s", head[:-1])
    last, nxt = runs[-1].split(), (e[c:].split() or [""])[0]
    tail = re.match(r"\s*((?:%s ){0,1}%s),? (?:and|or) (%s)" % (_LIST_ITEM, _LIST_ITEM, _LIST_ITEM), e[c:])
    stop = _FUNCTION_WORDS | _PRONOUNS | _DETERMINERS | _ADVERBS
    if (tail and last and last[0].lower() not in _INTRO
            and not any(w.lower() in stop for w in tail.group(1).split() + [tail.group(2)])):
        return True
    words = head[:-1].split()
    if (words and words[-1][:1].isupper() and words[-1].isalpha()
            and re.match(r"\s*[A-Z][\w'-]*(?: [A-Z][\w'-]*)?(?:,| and | or )", e[c:])):
        return True                                       # names: "from Dwork, / Rothblum and Vadhan"
    if len(runs) < 2 or not last or len(last) > 2:
        return False
    names = last[-1][:1].isupper() and nxt[:1].isupper()
    adjectives = (nxt[:1].islower() and nxt not in _FUNCTION_WORDS | _CLAUSE_STARTERS
                  and last[0].lower() not in _DETERMINERS)
    return names or adjectives


def _clause_marks(s: str, zh: bool) -> int:
    """Clause marks inside a piece (not at its end): ，；：。！？ outside （…） for Chinese, , ; : . ! ? —
    before a space for English, not counting list or appositive commas."""
    if zh:
        return len(re.findall(r"[，；：。！？]", strip_end(re.sub(r"（[^（）]*）", "", s))))
    s = s.strip()
    return sum(1 for m in re.finditer(r"[,;:.!?—](?= )", s)
               if not (m.group() == "," and _mark_cost(s, m.end()) >= 10))


def _split_like(e: str, zp: list[str], limit: float) -> tuple[list[str], bool]:
    """Cut the English sentence into len(zp) pieces where the Chinese is cut. Each Chinese cut (at
    its share of the sentence, not counting subtitle-only glosses （…）; for a later cut, halfway
    between that and "the previous English cut + this piece's share", so a long English clause
    before it does not drag it off) takes, with the fewest numbers and symbols on the wrong side
    first (41 / 42, 1/n, e^ε):
    - the cheapest English clause stop (not a list comma) that is nearer to it than to the other
      cuts and at most half the shorter neighbouring piece away (or 4 units): its distance from
      where the numbers allow the cut ("…2 times 1, / so 24 ways.") + 4 for a ; or : under a
      Chinese ，, or for a comma under a Chinese ；：。 ("moves 7, 8 and 9, it gets much worse: /"
      under "就麻烦多了：/ 我们必须……");
    - when there is no such stop, or the best one misplaces numbers or differs from the Chinese
      piece by two clause marks or more, also a gap right at the cut (within 0.1 of the sentence)
      after a content word and before an auxiliary or conjunction (+4: "…sanitized table / and
      walking away", "…like this / is the L1 norm"); when there is neither, a plain gap in a
      sentence of 60 characters or more (+8: "The earlier framework's sharper analysis / got this
      down to about √d");
    each + 2 per clause mark more or fewer than in the Chinese piece ("Multiply each bar by its
    number, / add them up," under "把每根柱子乘上各自被算的次数 / 再全部加起来，……") and + 3 per
    connective on the wrong side (而且 / and, 但 / yet: "…the same mark, and that mark isn't a dot,
    / that player has won."). A piece may run 15 % over `limit` (a 110-character line is about
    1170 px of the 1840 px line, measured with burn()). When a cut has none, or only one that puts
    numbers on the wrong side ("list all 8 winning lines, / …" under "……都列出来 / 一共 8 条"), the
    whole sentence stays up under every piece if it fits on one line, else the cuts without one
    fall back to the word gap with the fewest misplaced numbers, then the cheapest. Returns
    (pieces, repeated): repeated = the whole sentence is shown under every Chinese piece."""
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
    zmarks = [_clause_marks(p, True) for p in zp]

    def mismatch(c, prev, j, of=_symbols):
        """Numbers and symbols (or connectives) on the wrong side of a cut at c, for the j-th cut."""
        rest = "".join(zp[j + 1:])
        a, b, za, zb = of(e[prev:c]), of(e[c:]), of(zp[j]), of(rest)
        return sum(((a - za) + (za - a) + (b - zb) + (zb - b)).values())

    def clause_cost(c, prev, j):                           # 2 per clause mark more or fewer
        d = abs(_clause_marks(e[prev:c], False) - zmarks[j])
        if j == k - 2:
            d += abs(_clause_marks(e[c:], False) - zmarks[k - 1])
        return 2.0 * d

    def stop_cost(c, j, target, misplaced):
        mark, zmark = e[:c].rstrip()[-1:], zp[j].rstrip()[-1:]
        if mark not in ",;:.!?—" or (_list_comma(e, c) and zmark != "、"):
            return None
        if abs(units(e[:c]) - targets[j]) > min(abs(units(e[:c]) - t) for t in targets):
            return None                                    # nearer to another Chinese cut
        cost = abs(units(e[:c]) - target) + 1.5 * misplaced  # 3 units per number on the wrong side
        cost += 4 if zmark in "，、" and mark in ";:—" else 0  # "上限，/ 从而" is not "sensitivity; / add"
        if cost > min(cap, max(4, min(share[j], share[j + 1]) / 2)):
            return None
        return cost + (4 if zmark in "；：。！？" and mark == "," else 0)

    def gap_cost(c, j, aim, misplaced, plain):
        """A word gap right at the Chinese cut: before a preposition, auxiliary or conjunction
        ("…between the tents / can never exceed…"), or a plain one in a long sentence."""
        if not (e[c - 1] == " " and e[c - 2].isalnum()) or abs(units(e[:c]) - aim) > 0.1 * units(e):
            return None
        nxt, before = (e[c:].split() or [""])[0].lower(), (e[:c].split() or [""])[-1].lower()
        if before in _FUNCTION_WORDS | _CLAUSE_STARTERS | _PRONOUNS | _DETERMINERS | _ADVERBS | _NUMBER_WORDS:
            return None                                    # not "…the coin talking, yet / over…"
        pen = _cut_penalty(e, c)
        if nxt in _AUXILIARIES | _CLAUSE_STARTERS and pen <= 1:   # not "whether a patient / was in…"
            extra = 4.0
        elif (plain and pen <= 4 and len(e) >= 60 and nxt != "of"
              and nxt not in _FUNCTION_WORDS - _PREPOSITIONS | _DETERMINERS | _PRONOUNS):
            extra = 8.0                                    # "…sharper analysis / got this down…"
        else:
            return None
        return abs(units(e[:c]) - aim) + 1.5 * misplaced + extra

    def pieces_of(cuts):
        return [e[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(e)])]

    best, prev = [], 0
    for j in range(k - 1):
        aim = (targets[j] + units(e[:prev]) + share[j]) / 2 if j else targets[j]   # halfway to "this
        pool = [c for c in good if c > prev and units(e[prev:c].strip()) <= 1.15 * limit]  # piece's share"
        miss = {c: mismatch(c, prev, j) for c in pool}
        floor = min(miss.values(), default=0)
        conj = {c: mismatch(c, prev, j, _connectives) for c in pool}
        conj_floor = min(conj.values(), default=0)
        span = [units(e[:c]) for c in pool if miss[c] == floor] or [aim]
        pinned = min(max(aim, min(span)), max(span))      # where the numbers allow the cut
        def total_cost(c, cost):                           # "…the same mark, and that mark isn't a dot, /
            return cost + clause_cost(c, prev, j) + 1.5 * (conj[c] - conj_floor)   # that player has won."
        scored = [(total_cost(c, cost), c) for c in pool
                  if (cost := stop_cost(c, j, pinned if miss[c] == floor else aim, miss[c] - floor))
                  is not None]
        def rank(x):                                       # the numbers first, then the cost
            return miss[x[1]], x[0]
        top = min(scored, key=rank, default=None)
        if top is None or miss[top[1]] > floor or clause_cost(top[1], prev, j) >= 4:
            gaps = [(total_cost(c, cost), c) for c in pool        # a gap only instead of no stop, or of
                    if (cost := gap_cost(c, j, aim, miss[c] - floor, plain=False)) is not None]   # a poor one
            if not gaps and not scored:                    # a plain gap only instead of nothing
                gaps = [(total_cost(c, cost), c) for c in pool
                        if (cost := gap_cost(c, j, aim, miss[c] - floor, plain=True)) is not None]
            scored += gaps
        c = min(scored, key=rank, default=(0.0, None))[1]
        if c is None or miss[c] > floor:                   # numbers on the wrong side: repeat, or
            best.append(None)                              # the fallback below ("…that ends on move 5 /
            continue                                       # a total of 24 times" under "第 5 步……/ 24 次")
        best.append(c)
        prev = c
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


def _break_cost(text: str, c: int) -> float:
    """How bad a line break at c is: its cut and mark cost, and for English 2 more before a
    determiner (a verb and its object: "got / this down")."""
    q = _cut_penalty(text, c, lines=True) + _mark_cost(text, c)
    prev, nxt = (text[:c].split() or [""])[-1].lower(), (text[c:].split() or [""])[0].lower()
    if nxt in _DETERMINERS - {"that"} and prev.isalpha() and prev not in _FUNCTION_WORDS:
        q += 2.0
    return q


def _clean_break(text: str, c: int) -> bool:
    """An English line or cue break at c that follows the sentence: after a clause mark (not a list
    or appositive comma), or before and / but / which … (not the 'and' that closes a list or joins
    two names or numbers, "McSherry / and Talwar's", "move 8 / or 9"; not then / so without a
    comma, "The joint density / then depends"; not "even / if")."""
    prev, nxt = (text[:c].split() or [""])[-1], (text[c:].split() or [""])[0]
    if prev[-1:] in ",;:.!?—":
        return _mark_cost(text, c) < 10
    return (nxt in _CLAUSE_WORDS - {"then", "so"} and prev.lower() not in _FUNCTION_WORDS
            and not _list_and(text, c) and _cut_penalty(text, c) <= 4)


def _rewrap(text: str, limit: float, accept, min_line: float = 0.0) -> list[str] | None:
    """The best 2-line wrap of text whose break passes `accept` (balance plus break cost), with
    both lines within `limit` and at least `min_line` units, or None."""
    good, ok = _cuts(text, lines=True)
    best = None
    for c in good + ok:
        left, right = text[:c].strip(), text[c:].strip()
        if (not left or not right or max(units(left), units(right)) > limit
                or min(units(left), units(right)) < min_line or not accept(c)):
            continue
        cost = abs(units(left) - units(right)) + _break_cost(text, c)
        if best is None or cost < best[0]:
            best = (cost, [left, right])
    return best and best[1]


def _two_lines(cue, limit: float, min_dur: float = 1.0) -> list[tuple[float, float, str]]:
    """A cue wrapped to at most 2 lines; a piece that needs more becomes two cues (time split in
    proportion to their spoken form, cue[3], when there is one, else their length), cut at a clause
    boundary when one gives two 2-line cues. Two lines that split a list at its 、 ("光凭邮编、/
    出生日期和性别") also become two cues when a clause cut gives two 2-line cues. Two English lines
    that break mid-phrase are re-wrapped at a clean break when one fits ("Remember the Gaussian /
    whose ratio escaped…"), else become two cues when a clause cut gives cues whose lines break no
    worse ("But SuLQ only covered sums," + "and its definition tolerated / a tiny chance…"). A
    Chinese line may run 1.5 units over the limit rather than break a list of Latin names (同年她与 /
    Kenthapadi、McSherry、Mironov 和 Naor 合作)."""
    a, b, text, *rest = cue
    spoken = rest[0] if rest else None
    text = strip_end(text)
    english = not _CJK.search(text)

    @lru_cache(maxsize=None)
    def wrap2(t):                                         # the lines of t
        ls = split_balanced(t, limit)
        if len(ls) != 2:
            return tuple(ls)
        c = len(t) - len(t[len(ls[0]):].lstrip())
        if not english and _mark_cost(t, c) >= 10:          # "Kenthapadi、/ McSherry、"
            ls = _rewrap(t, limit + 1.5, lambda x: not (re.search(r"[A-Za-z](?:、| [和与及])?$", t[:x].rstrip())
                                                        and re.match(r"(?:[和与及] )?[A-Za-z]", t[x:].lstrip()))) or ls
        elif english and not _clean_break(t, c):           # "Next, the computer needs to know /
            ls = _rewrap(t, limit, lambda x: _clean_break(t, x), limit / 3) or ls   # what counts as a win."
        return tuple(ls)

    def breaks(t):                                        # where the 2 lines of t break
        ls = wrap2(t)
        return [len(t) - len(t[len(ls[0]):].lstrip())] if len(ls) == 2 else []

    def listy(t):                                         # two lines that split a list at its 、
        return any(t[:c].rstrip()[-1:] == "、" for c in breaks(t))

    def worst(*parts):                                    # the worst line break of these cues
        return max([0.0] + [0.0 if english and _clean_break(t, c) else _break_cost(t, c)
                            for t in parts for c in breaks(t)])

    def midline(*parts):                                  # clause marks inside a line of these cues:
        n = 0                                             # "…starting / from zero, so our squares…"
        for t in parts:
            for ln in wrap2(t):
                n += len(re.findall(r"[;:?!](?= )|\.(?= [A-Z])", ln))
                n += sum(1 for m in re.finditer(r", (\w+)", ln)
                         if m.group(1) in _CLAUSE_WORDS - {"or"} and not _list_and(ln, m.start() + 2))
        return n

    lines = wrap2(text)
    mid_phrase = english and len(lines) == 2 and worst(text) > 0
    if len(lines) == 1 or (len(lines) == 2 and not listy(text) and not mid_phrase):
        return [(a, b, "\n".join(lines))]
    good, ok = _cuts(text)
    stops = "，、；：。！？,;:.!?…—"
    best = None
    for c in good + ok:
        left, right = text[:c].strip(), text[c:].strip()
        if not left or not right:
            continue
        if len(wrap2(strip_end(left))) > 2 or len(wrap2(right)) > 2:
            continue
        at_stop = text[c - 1] in stops or (text[c - 1] == " " and text[c - 2] in stops)
        at_stop = at_stop and text[:c].rstrip()[-1:] != "、"    # a cue cut inside a list: "一个集合 // 一个比特串"
        if english:
            at_stop = _clean_break(text, c)               # also before and / which …: "network // where each"
        clean = (at_stop and (left[-1:] in "，；：。！？,;:.!?" or english)
                 and min(units(left), units(right)) >= limit / 3
                 and not listy(strip_end(left)) and not listy(right) and _mark_cost(text, c) < 10)
        if len(lines) == 2 and not clean:
            continue                                      # instead of a 、 split: two clean clause cues
        if mid_phrase and not (worst(left, right) < worst(text)
                               or worst(text) > 4 and worst(left, right) <= worst(text) + 2
                               or worst(left, right) <= worst(text) and midline(left, right) < midline(text)):
            continue                                      # ... or for two cues whose lines break better
        if len(lines) == 2 and (b - a) * min(units(left), units(right)) / units(text) < min_dur:
            continue                                      # (not into a cue too short to read)
        if english:                                       # the lines matter more than the balance
            cost = (0.5 * abs(units(left) - units(right)) + _cut_penalty(text, c) + _mark_cost(text, c)
                    + worst(left, right))
        else:
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
    said = (spoken and _spoken_parts(text, halves, spoken)) or [None] * len(halves)
    out = []
    for (s0, s1, h), q in zip(_proportional(a, b, halves, said[0] and [units(x) for x in said]), said):
        out += _two_lines((s0, s1, h, q), limit, min_dur)
    return out


def _stretch(cues, min_dur: float):
    """A cue shorter than min_dur (a merge did not fit), or a Chinese cue shorter than 0.2 s per unit
    (at most 1.5 s: "这里说的“一局”" 0.68 → 1.4 s, "然后在 2003 年" 1.09 → 1.5 s in an English video,
    where the English voice sets the pace), takes the time from a contiguous neighbour with time to
    spare, the longer one first; the neighbour keeps its own minimum."""
    out = [list(c) for c in cues]

    def need(c):                                          # Chinese: 0.2 s per unit, up to 1.5 s
        return max(min_dur, min(1.5, 0.2 * units(c[2].replace("\n", "")))) if _CJK.search(c[2]) else min_dur

    for i, c in enumerate(out):
        if c[1] - c[0] >= need(c):
            continue
        nbrs = [j for j in (i - 1, i + 1) if 0 <= j < len(out) and abs(out[j][0] - c[1] if j > i
                                                                      else c[0] - out[j][1]) < 0.05]
        for j in sorted(nbrs, key=lambda j: out[j][0] - out[j][1]):
            give = min(need(c) - (c[1] - c[0]), (out[j][1] - out[j][0]) - need(out[j]))
            if give <= 0:
                continue
            if j > i:
                c[1] += give
                out[j][0] = c[1]
            else:
                c[0] -= give
                out[j][1] = c[0]
    return [tuple(c) for c in out]


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
                said = [c[3] for c in (cues[lo], cues[hi]) if len(c) > 3]
                cues[lo:hi + 1] = [[cues[lo][0], cues[hi][1], text, *(
                    [said[0] + said[1] if all(said) else None] if said else [])]]
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
