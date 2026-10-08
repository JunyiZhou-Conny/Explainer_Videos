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
               "independent", "consistent", "efficient", "important", "constant", "first", "second",
               "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth", "only",
               "early", "old", "final", "human", "chinese", "english"}     # "an early / draft", "the Chinese / version"
_MODIFIER = re.compile(r"[a-z-]+(?:ed|ing|ive|ous|ful|ic|able|ible|est|less|al)")
_NOT_MODIFIERS = {"signal", "interval", "trial", "animal", "proposal", "need", "seed", "speed", "thing",
                  "nothing", "something", "anything", "everything", "string", "king", "ring", "logic"}


def _modifier(w: str) -> bool:
    """A word that looks like it modifies the noun after it (randomized, sharper, interactive, true)."""
    w = w.lower().rstrip(",")
    return w in _ADJECTIVES or (bool(_MODIFIER.fullmatch(w)) and w not in _NOT_MODIFIERS)


# a verb that takes a clause without "that" ("the paper proves / the first is…", "someone says / a
# dataset is safe"), and a noun with the preposition it takes ("its distance / from the true answer")
_CLAUSE_VERBS = {"prove", "proves", "proved", "show", "shows", "showed", "say", "says", "said", "mean",
                 "means", "meant", "know", "knows", "knew", "guarantees", "ensures", "implies", "suggests",
                 "argues", "claims", "notice", "notices", "realize", "realizes", "think", "thinks"}
_NOUN_PREPS = {("distance", "from"), ("limit", "on"), ("limits", "on"), ("bound", "on"), ("cap", "on")}
_VERB_PREPS = {(v, p) for p, vs in {"on": "depend depends depended depending rely relies relied relying",
                                    "to": "lead leads led leading belong belongs refer refers referred apply applies compared",
                                    "of": "consist consists consisted", "at": "look looks looked looking",
                                    "with": "deal deals dealt", "in": "result results resulted",
                                    "like": "look looks looked looking sound sounds sounded feel feels felt "
                                            "seem seems seemed"}.items()
               for v in vs.split()}                       # a prepositional verb: "depends / on", "leads / to",
                                                          # "looked / like"
_GREEK = r"(?:epsilon|lambda|sigma|delta|alpha|beta|mu)"
_OPERAND = r"(?:(?:[b-zB-HJ-Z]|\d+(?:\.\d+)?)(?: %s)?|%s)(?: prime)?" % (_GREEK, _GREEK)
_SPOKEN_MATH = re.compile(                                # "S of f over epsilon", "e to the epsilon", "one over n",
    r"\b(?:scale )?(?:%s(?: (?:of|over|to the(?: minus)?|plus|minus|times|divided by) %s)+\b|"   # "scale sensitivity
    r"[a-z]+ (?:over|divided by) (?:%s|[b-zB-HJ-Z]|\d+)\b)" % (_OPERAND, _OPERAND, _GREEK))     # over epsilon"


def _bare_clause(text: str, c: int) -> bool:
    """At c, after a verb that takes a clause, a clause without "that": determiner, one or two words
    and an auxiliary ("proves / the first is fundamentally more powerful")."""
    prev = (text[:c].split() or [""])[-1].lower()
    det = "|".join(sorted(_DETERMINERS - {"that"}, key=len, reverse=True))
    aux = "|".join(sorted(_AUXILIARIES, key=len, reverse=True))
    return prev in _CLAUSE_VERBS and bool(re.match(r"(?:%s) (?:[\w'-]+ ){0,1}[\w'-]+ (?:%s)\b" % (det, aux),
                                                     text[c:].lstrip(), flags=re.I))


def _that_clause(text: str, c: int) -> bool:
    """At c, "that" starts a clause, not a noun phrase: "…one release / that is accurate", "showed /
    that ZIP code…" (not "allow / that tiny δ")."""
    m = re.match(r"that ([\w'-]+)", text[c:].lstrip())
    if not m:
        return False
    w = m.group(1)
    return (w.lower() in _AUXILIARIES | _DETERMINERS | _PRONOUNS | _PREPOSITIONS | _ADVERBS
            or w[0].isupper() or w[0].isdigit())


def _adverb_yet(text: str, c: int) -> bool:
    """At c, "yet" is the adverb of "no record yet", after a word and before a preposition or the
    end of its clause ("There's no record yet of anyone…", "no measure yet."), not the conjunction
    of "simple, yet powerful" or "…, yet it works"."""
    m = re.match(r"yet(?=$|[,.;:!?]| )(?: (\S+))?", text[c:].lstrip())
    prev = (text[:c].split() or [""])[-1]
    if not m or not prev[-1:].isalnum():
        return False
    after = text[c:].lstrip()[3:4]
    return after in ("", ",", ".", ";", ":", "!", "?") or (m.group(1) or "").lower() in _PREPOSITIONS


_LIKE_VERBS = {"look", "looks", "looked", "looking", "sound", "sounds", "sounded", "feel", "feels", "felt",
               "seem", "seems", "seemed"}


def _verb_like(text: str, c: int) -> bool:
    """Before c, the "like" of "looked like", "sounds like", ending its clause (a preposition, a
    clause word or punctuation follows): "Here's what a paused frame looked like / in an early
    draft", not "looks like / a tree"."""
    words = text[:c].split()
    if len(words) < 2 or words[-1].lower() != "like" or words[-2].lower() not in _LIKE_VERBS:
        return False
    nxt = (text[c:].split() or [""])[0].lower()
    return nxt in _PREPOSITIONS | _CLAUSE_STARTERS or nxt == ""


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
                "our", "your", "my", "each", "every", "one", "another", "any", "some", "all", "both",
                "either", "neither", "such", "several", "many", "most"}
_PRE_NOUN = {"any", "every", "each", "some", "another", "both", "either", "neither", "such", "several",
             "most", "many"}


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
    if prev in _OPERATORS or text[c:c + 1] in _OPERATORS and text[c + 1:c + 2] == " ":
        return cost + 12.0                                # "ε = / 0.1", "f(x) / + Y"
    if not prev[-1:].isalnum() and not prev.endswith(("s'", "s’")):   # (a plural possessive goes on:
        return cost                                                   # "the fixers' / work")
    words = text[:c - 1].split()
    low, nxt = prev.lower(), text[c:].split(" ", 1)[0]
    word = nxt.rstrip(",.;:!?").lower()
    like = _verb_like(text, c)                            # "what a paused frame looked like / in an early draft"
    yet_end = low == "yet" and _adverb_yet(text, c - 4)   # "There's no record yet / of anyone…"
    content = (word.replace("-", "").isalpha() and nxt[:1].islower()          # (made-up)
               and word not in _FUNCTION_WORDS | _CLAUSE_STARTERS | _DETERMINERS | _PRONOUNS)
    short_clause = word in _AUXILIARIES and _SUBORDINATORS & {w.lower() for w in words[-4:-1]}
    gerund = _gerund_subject(text, c)
    complement = word in ("what", "how", "where", "why", "who", "which") and bool(   # "it is exactly / what…"
        re.search(r"\b(?:is|are|was|were|be|been)(?: [a-z]+ly| just| not)? $", text[:c]))
    main_verb = low in ("has", "have", "had") and (word in _DETERMINERS | _NUMBER_WORDS | {"at", "no", "more", "fewer"}
                                                   or word[:1].isdigit())   # "chess has / at least 10…"
    if (low not in _FUNCTION_WORDS or main_verb or like or yet_end) and (
            (word in _CLAUSE_STARTERS | _AUXILIARIES | _PREPOSITIONS - {"of", "per", "than"}
             and not _adverb_yet(text, c)
             and not _list_and(text, c) and not short_clause and not _binomial(text, c) and not complement)
            or _bare_clause(text, c) or gerund):
        cost += 1.0                                       # before a clause, verb or phrase: "…table / and walking away",
                                                          # "because going first / gives X more chances"
    else:                                                 # (not "if the true count / is 42"; the 'and' of a list:
        cost += 8.0 if _binomial(text, c) else 6.0 if _list_and(text, c) else 4.0   # "birth date / and sex"; of two
                                                          # bare nouns: "the mathematician / and engineer Claude Shannon")
    if (re.search(r", \S+ $", text[:c]) and re.match(r"\S+,? (?:and|or) ", text[c:])
            and _list_comma(text, text[:c].rstrip().rfind(",") + 1)):
        cost += 4.0                                       # inside a list item: "ZIP code, birth / date and sex"
    quantifier = low in ("most", "least") and len(words) > 1 and words[-2].lower() == "at"   # "is at most / the…"
    if ((low in _FUNCTION_WORDS | _PRE_NOUN and not main_verb and not quantifier and not like)
            or (low in ("this", "these", "those") and content)):
        cost += 8.0                                       # "…the probability of any / event", "call those / made-up…"
    elif (len(words) > 1 and words[-2].lower() in _AUXILIARIES - {"is", "are", "was", "were", "be", "been", "being"}
          and (low in _ADVERBS or low.endswith("ly"))):
        cost += 8.0                                       # "can now / move", "would actually / use"
    elif low in _PRONOUNS and ((len(words) > 1 and words[-2].lower() in _CLAUSE_STARTERS | {"so", "then"})
                               or word in _AUXILIARIES):
        cost += 8.0                                       # "so it / counts", "for most masks it / cannot…"
    elif (low in ("it", "them") and content and len(words) > 1 and words[-2].isalpha()
          and words[-2].lower() not in _FUNCTION_WORDS | _CLAUSE_STARTERS):
        cost += 6.0                                       # an object and its complement: "makes it / private"
    elif (word in ("it", "them", "him", "us", "me") and low.isalpha() and low not in _FUNCTION_WORDS | _CLAUSE_STARTERS
          and (text[c + len(nxt):].split() or [""])[0].lower() not in _AUXILIARIES):
        cost += 4.0                                       # a verb and its object pronoun: "and let / it play"
                                                          # (not "for most masks / it cannot…")
    elif low in _ADVERBS - {"then", "first", "now"} and content:
        cost += 4.0                                       # an adverb and its verb: "never / releases"
    elif low.endswith("ly") and content and _modifier(nxt):
        cost += 8.0                                       # and its adjective: "supposedly / anonymous"
    if prev[:1].isupper() and len(words) > 1 and (b.isupper() or re.match(r"(and|or) [A-Z]", text[c:])):
        cost += 8.0                                       # names: "Kobbi / Nissim", "Nissim / and Adam"
    if _in_term(text, c) or (content and low in _ADJECTIVES and _in_term(text, c + len(nxt) + 1)):
        cost += 8.0                                       # a glossary term: "counting / query", "private / deep learning"
    if (low, word) in _NOUN_PREPS:                       # "its distance / from the true answer", "the limit / on
        bare = (text[c + len(nxt):].split() or [""])[0].lower() not in _SUBORDINATORS | {"what", "how", "why"}
        cost += 6.0 if bare else 3.0                      # questions" (not "a surprising limit / on what…")
    if (low, word) in _VERB_PREPS:
        cost += 8.0                                       # a prepositional verb: "depends / on", "leads / to"
    if len(words) > 1 and words[-2].lower() in _PREPOSITIONS and (
            (words[-2].lower() == "to" and content) or (nxt[:1].islower() and not nxt.rstrip(",.;:!?").isalpha())):
        cost += 3.0                                       # one word into a phrase: "to measure / sensitivity",
                                                          # "with scale / sensitivity/ε" (not "per row / doubles")
    if word in _AUXILIARIES and any(_bare_clause(text, len(" ".join(words[:j]))) for j in (len(words) - 2, len(words) - 3)
                                    if j > 0):
        cost += 6.0                                       # "the paper proves the first / is…": a garden path
    if word == "of" and not yet_end:
        after = (text[c + len(nxt):].split() or [""])[0].lower()
        cost += 4.0 if after in _NUMBER_WORDS or after[:1].isdigit() else 2.0   # "an odd number / of ones",
                                                          # "a ratio / of one half"
    if (word in _PARTICLES | {"alone"} or (word in _PREPOSITIONS and nxt[-1:] in ",.;:!?")
            or _adverb_yet(text, c)):                    # "There's no record / yet of anyone…"
        cost += 6.0                                       # "single / out", "whatever / else", "going / in,",
                                                          # "ZIP code, birth date and sex / alone"
    if low in _PARTICLES and (content or word in _DETERMINERS):
        cost += 3.0                                       # its object: "single out / most Americans"
    poss = next((j for j in range(len(words) - 1, max(-1, len(words) - 4), -1)
                 if words[j].endswith(("'s", "’s", "s'", "s’"))), None)   # (and "the fixers' / work")
    if poss is not None and content and all(_modifier(w) for w in words[poss + 1:]):
        cost += 6.0                                       # "Alice's / row", "curator's randomized answering / rule"
    elif (content and len(words) > 1 and _modifier(prev) and not gerund   # (not "any one person's row / changes",
                                                          # "because going first / gives X")
          and (words[-2].lower() in _DETERMINERS | _PREPOSITIONS | {"no"} or _NUMBER.fullmatch(words[-2].lower())
               or _modifier(words[-2]) or words[-2].lower().endswith("ly"))):   # "supposedly anonymous /"
        cost += 8.0                                       # an adjective and its noun: "its published / tables",
                                                          # "for broad, flexible / accuracy"
    verbal = word in _AUXILIARIES | _CLAUSE_STARTERS | _PREPOSITIONS and word not in ("of", "to", "and", "or")
    if b.isdigit() or word in _NUMBER_WORDS or (prev[-1:].isdigit() and not verbal):
        cost += 4.0                                       # "on move / 6", "9 times / 8", "at most / one"
        if re.search(r"\b(?:at least|at most|more than|fewer than|less than|about|only|nearly|almost|roughly|exactly)$",
                     " ".join(words[-2:]).lower()):
            cost += 4.0                                   # a number and its quantifier: "at least / two thirds"
    if _NUMBER.fullmatch(low) and (content or re.match(r"(and|or) (a |\d|(%s)\b)" % "|".join(_NUMBER_WORDS),
                                                       text[c:])):   # (not "8 or 9 / have")
        cost += 8.0                                       # "at most one / empty square", "fifty-two / and a half"
    if low in ("even", "only", "just") and word in ("if", "though", "when", "as", "after", "before", "because"):
        cost += 8.0                                       # "even / if Alice's row…"
    if word == "as" and len(words) > 1 and words[-2].lower() == "as":
        cost += 8.0                                       # "as soon / as", "as long / as"
    if any(m.start() < c - 1 < m.end() for m in re.finditer(r"\S+ to the power of \S+", text)):
        cost += 12.0                                      # one number: "10 to the power / of 120", "10 / to the…"
    elif any(m.start() < c - 1 < m.end() for m in _SPOKEN_MATH.finditer(text)):
        cost += 12.0                                      # spoken math: "S of f / over epsilon", "e / to the epsilon"
    elif "-" in prev.strip("-") and prev.islower() and content:
        cost += 4.0                                       # "the two-question / version"
    return cost


_STRONG = "。！？；：.!?;:—…"
_SEMI_LIST = re.compile(r"(?:(?<=：)|^)(?:[^：。！？；]*；)+(?:以及|和|还有|及|或者)[^。！？；]*")   # "：A；B；以及 C"
_OPERATORS = set("=+−-×·<>≤≥≈")


def _short_gloss(after: str) -> bool:
    """`after` starts with a short explanation of the term before the comma: 意思是“赢家”, 也就是 1,
    也就是每条边正中间的那一格, explore 就是“探索”的意思 (not a whole clause: 也就是改变一条记录最多能让答案
    变化多少)."""
    gloss = (re.match(r"(?:意思是|也就是|就是说|即)[^，。！？；：]*(?=[，、])", after)   # not the end of the
             or _QUOTE_GLOSS.match(after))                                # sentence: "乘 1，/ 也就是 24 种不同的顺序。"
    return bool(gloss) and units(gloss.group()) <= 14


# the term restated with its meaning: "一个叫 explore 的函数，explore 就是“探索”的意思"
_QUOTE_GLOSS = re.compile(r"[A-Za-z][\w']*\s*(?:就是|的意思是)“[^”]*”(?:的意思)?(?=[，、。！？]|$)")


def _number_appositive(rest: str) -> bool:
    """`rest` starts with a short noun phrase ending in a number and a comma: "true answer 0, as
    for one…" (after "…even parity,"), not "say at $1M, first"."""
    m = re.match(r"((?:[a-z]+ ){1,2})[^\s,]*\d[^\s,]*,(?:\s|$)", rest)
    return bool(m) and not _FUNCTION_WORDS & set(m.group(1).split())


def _mark_cost(text: str, c: int) -> float:
    """Weight of the mark a cut at c follows, so that the stronger mark wins when the balance is
    close: none after 。！？；：. ! ? ; : — …, 3 after a comma (or no mark at all), 8 after a comma
    that leaves a short clause before a 。；！？ (the cut belongs there), after a short lead-in that
    follows one (；在 Python 里，), before a short clause that continues the one before it (想……，
    又要强隐私，; 有人说数据集匿名化了，所以很安全，) or before a short gloss (winner，意思是“赢家”;
    边格，也就是每条边正中间的那一格), after a condition, a means or a comparison before its result
    or predicate (光凭……，/ 就; 到了第 5 步，/ 才; 先……再撤销，/ 就; 比起……，也就是 1，/ 算是很大), inside a
    先……再…… sequence and after a ； inside a list that follows a ：, 6 after 、 (it splits a list:
    光凭邮编、/ 出生日期), 10 after a 、 between two Latin names (Dwork、/ Rothblum) or a comma
    between two numbers (moves 7, / 8 and 9), two names or adjectives (Dwork, / Rothblum; broad, /
    flexible accuracy) or before a short appositive (f(x), / 41,; noise, / Y,)."""
    head = text[:c].rstrip()
    if head[-1:] == "；" and any(m.start() < len(head) < m.end() for m in _SEMI_LIST.finditer(text)):
        return 8.0                  # inside a list after a ：, like a 、: "三个核心想法：隐私的定义；/ 一个数叫……"
    if head[-1:] in _STRONG:
        return 0.0
    nxt = text[c:].lstrip()[:1]
    if head[-1:] == "、":
        names = head[-2:-1].isascii() and head[-2:-1].isalpha() and nxt.isascii() and nxt.isalpha()
        return 10.0 if names else 6.0
    if head[-1:] == "," and head[-2:-1].isdigit() and nxt.isdigit():
        return 10.0                                        # a list of numbers: "moves 7, / 8 and 9"
    if head[-1:] == "," and (_list_comma(text, c) or re.match(r"([^\s,]*\d[^\s,]*|[A-Z]),(?:\s|$)", text[c:].lstrip())
                             or _number_appositive(text[c:].lstrip())
                             or (re.match(r"[A-Z][a-z]+, [a-z]", text[c:].lstrip())
                                 and re.search(r"\b[a-z]+,$", head))):   # "one new patient, / Alice, is…"
        return 10.0                                        # "Dwork, / Rothblum", "broad, / flexible", "f(x), / 41,",
                                                           # "even parity, / true answer 0, as for…"
    if head[-1:] == ",":
        lead = re.split(r"[.;:!?—]\s", head[:-1])
        if len(lead) > 1 and len(lead[-1].split()) <= 2 and lead[-1].split()[0].lower() not in _DETERMINERS:
            return 8.0              # a short lead-in after a strong mark: "…exponentially large: roughly, / every 4…"
        if re.match(r"(?:is|are|was|were|has|have|had|can|could|will|would|must|should|may|might) ", text[c:].lstrip()):
            return 8.0              # the verb after a long subject: "Trying a path, …the next one, / is called…"
    end = re.search(r"[。！？；!?;:]|\.(?!\d)|$", text[c:])      # (not the point of 0.1; "Gaussian, / though:")
    if head[-1:] in "，," and units(text[c:c + end.start()]) <= 7.5:
        return 8.0                  # a clause end a few characters on: "偶数个 1，/ 真实答案为 0；"
    if head[-1:] == "，":
        start = max(head.rfind(m, 0, len(head) - 1) for m in "。！？；：")
        if start >= 0 and units(head[start + 1:-1]) <= 7:
            return 8.0              # a short lead-in after a strong mark: "叫 Python；在 Python 里，/ 列表……"
        clause = re.split(r"[，。！？；：]", head[:-1])[-1]
        if re.match(r"(?:对于|关于|随着|根据|对|在|从|当|按)", clause) and units(clause) <= 7:
            return 8.0              # a short scope phrase: "即使……同一个 mask，对大多数 mask，/ 它也估计不出……"
        if re.search(r"一(.)接一\1$|一(.)一\2$", clause):
            return 10.0             # a manner adverbial and its verb: "再让它一局接一局，/ 把所有可能的对局都下一遍"
        if (re.match(r"[就才便]", text[c:].lstrip())
                and re.search(r"光凭|凭|只要|只有|一旦|如果|要是|假如|到了|等到|直到|先.*再",
                              re.split(r"[。！？；：]", head)[-1])):
            return 8.0              # a condition and its result: "光凭邮编、出生日期和性别，/ 就能唯一识别……",
                                    # "所以到了第 5 步，/ 才可能有人凑齐三个棋子", "先试走一步，往下探索，再撤销，/ 就把……"
        if any(m.start() < len(head) < m.end() for m in re.finditer(r"先[^。！？；]*?再[^，。！？；]*", text)):
            return 8.0              # inside a 先……再…… sequence, like a list: "先试走一步，/ 往下探索，再撤销"
        clauses = re.split(r"[，。！？；：]", head[:-1])
        if len(clauses) > 1 and _short_gloss(clauses[-1] + "，"):
            clauses.pop()           # (past its gloss: "比起她自己的贡献，也就是 1，/ 算是很大")
        if re.match(r"比起|相比|相较", clauses[-1]) or re.search(r"(?:和|与|跟|同).*相比$", clauses[-1]):
            return 8.0              # a comparison and its predicate: "比起她自己的贡献，也就是 1，/ 算是很大"
        nxt_clause = re.match(r"(?:又|也|还|而且|并且|所以|却|但)[^，。！？；：、]*(?=，)", text[c:].lstrip())
        if nxt_clause and units(nxt_clause.group()) <= 6:
            return 8.0              # a short clause that continues this one: "想对各种问题都答得准，/ 又要强隐私，",
                                    # "数据集匿名化了，/ 所以很安全，你就知道……"
        if _short_gloss(text[c:].lstrip()):
            return 8.0              # a short gloss stays with its term: "叫 winner，/ 意思是“赢家”"
        if re.match(r"从而|进而|借此|以此", text[c:].lstrip()):
            return 8.0              # the result of this clause: "就像我们的收入上限，/ 从而限制了敏感度"
    return 3.0


def _pick_cuts(text: str, k: int, pool_of, total: float, lines: bool = False, cue: bool = False) -> list[int] | None:
    """k - 1 cuts, each the cheapest of its pool: distance from the ideal plus the cut's cost (for
    an English cue, `cue`: half the distance plus _cue_cost)."""
    cuts, prev = [], 0
    for j in range(1, k):
        ideal_u = total * j / k
        pool = pool_of(prev, ideal_u, j == k - 1)
        if not pool:
            return None
        if cue:                                           # an English cue: the cut matters more than the balance
            cut = min(pool, key=lambda c: 0.5 * abs(units(text[:c]) - ideal_u) + _cue_cost(text, c))
        else:
            cut = min(pool, key=lambda c: abs(units(text[:c]) - ideal_u) + _cut_penalty(text, c, lines)
                      + _mark_cost(text, c))
        cuts.append(cut)
        prev = cut
    return cuts


# a word that starts a clause, for an English cue cut that has no punctuation ("…most Americans,
# / and in 1997 she linked … / and found the governor")
_CLAUSE_WORDS = {"and", "but", "or", "so", "yet", "which", "who", "whose", "what", "where", "when", "while",
                 "because", "then", "unless", "until", "if", "although", "though", "whereas", "whether"}


def _name_gap(text: str, c: int) -> bool:
    """The word gap before c is inside a name or a list of names: "Kobbi / Nissim", "Nissim / and Adam"."""
    prev, nxt = (text[:c].split() or [""])[-1], text[c:].split()[:2]
    return (prev[:1].isupper() and prev.rstrip(",").isalpha() and len(text[:c].split()) > 1
            and bool(nxt) and (nxt[0][:1].isupper() or (nxt[0] in ("and", "or") and nxt[1:2] and nxt[1][:1].isupper())))


def _binomial(text: str, c: int) -> bool:
    """At c, an and / or that joins two bare nouns or adjectives: "the mathematician / and engineer
    Claude Shannon", "statisticians / and computer scientists", "explicit / and measurable" (not a
    clause or a verb phrase: "…table / and walking away", "…voter list / and found the governor",
    "…at random / and publish it"; the 'and' of a longer list is _list_and)."""
    prev = (text[:c].split() or [""])[-1]
    m = re.match(r"(?:and|or) ([a-z][a-z-]*)([,.;:!?]?)(?: ([\w'’-]+))?", text[c:])
    if (not m or not prev.isalpha() or prev.endswith("ly")       # (a name too: "Abadi / and colleagues")
            or prev.lower() in _FUNCTION_WORDS | _ADVERBS | _PARTICLES | _PRONOUNS | {"again"}):
        return False
    y1, punct, y2 = m.group(1), m.group(2), m.group(3) or ""
    if (y1 in _FUNCTION_WORDS | _DETERMINERS | _PRONOUNS | _ADVERBS | _CLAUSE_STARTERS | _NUMBER_WORDS
            or y1.endswith(("ing", "ed")) or _list_and(text, c)):
        return False
    return bool(punct) or not y2 or not (
        y2.lower() in _FUNCTION_WORDS | _DETERMINERS | _PRONOUNS | _ADVERBS | {"yes", "no", "them", "him", "us", "me"}
        or y2[:1].isdigit() or y2.lower() in _NUMBER_WORDS)


_GERUND = re.compile(r"(?:^|[.!?;:] |\b(?:%s) )([A-Za-z]+ing)((?: [\w'’/^-]+){1,6}) $" % "|".join(
    sorted(_CLAUSE_VERBS | {"because", "that", "if", "when", "since", "while", "although", "though", "so"},
           key=len, reverse=True)))


def _gerund_subject(text: str, c: int) -> bool:
    """At c, the verb after a gerund subject, which a break may separate: "because going first / gives
    X more chances to win", "privacy means changing any one person's row / changes the probability…",
    "Multiplying the choices / gives nine factorial" (not a participle after a comma: ", filling the
    squares in order")."""
    m = _GERUND.search(text[:c])
    if not m or m.group(1).lower() in _NOT_MODIFIERS:
        return False
    if any(w.lower() in _AUXILIARIES | _CLAUSE_STARTERS for w in m.group(2).split()):
        return False
    rest = text[c:].split()[:2]
    if len(rest) < 2:
        return False
    verb, obj = rest
    return (bool(re.fullmatch(r"[a-z]+(?:[^s']s|ed)", verb)) and verb not in _FUNCTION_WORDS
            and (obj.lower() in _DETERMINERS | _NUMBER_WORDS or obj[:1].isupper() or obj[:1].isdigit()))


def _list_and(text: str, c: int) -> bool:
    """A gap before the 'and' / 'or' that closes a list: "ZIP code, birth date / and sex" (not
    "Over the following decades, statisticians / and computer scientists")."""
    m = re.match(r"(and|or) ", text[c:]) and re.search(r",( \S+){1,3} $", text[:c])
    return bool(m) and _list_comma(text, m.start() + 1)


def split_balanced(text: str, limit: float, hang: bool = False, clauses: bool = False,
                   line: float = 0.0, min_piece: float = 0.0) -> list[str]:
    """Fewest pieces of at most `limit` units each, balanced in length. Cuts at sentence marks
    (；。！？ ; . ! ?) when those alone give pieces that fit and none is tiny (a ；-structured
    sentence keeps one clause per piece; not ：, which often binds a short lead-in to what follows:
    分成两种思路：要么……), else at any punctuation whenever the pieces still fit
    (even if unbalanced, but not leaving a stray scrap at a comma), preferring the stronger mark
    (_mark_cost), else at the best word gap or between CJK characters; English pieces avoid ending
    on an article or preposition, Chinese pieces on a preposition. `clauses` (English cues): before
    a word gap, also try a gap before and / but / which … (not the 'and' of a list), and one more
    piece cut at punctuation, so that a cue boundary does not fall mid-phrase; a piece must have a
    2-line layout that does not split a name, and a word gap whose _cue_cost is 10 or more is
    used only when no number of pieces avoids it; when the result still has a cue cut whose
    _cue_cost is 10 or more, a piece may also take a 2-line layout whose break costs up to 16 (not
    inside a name) if that avoids such cuts ("that chess has at least / 10 to the power of 120
    possible games." at 44 characters, not four one-line cues). `hang`: the pieces
    are cues, whose final ，。、；： is dropped (strip_end), so it does not count against the limit; a
    Chinese cue does not run on across a ；。！？ in mid-line (in lines of `line` units, default
    `limit`) when one cue more avoids it;
    and a whole 《…》 title may run 5 units over it (a 30-unit bilingual line is about 1040 px of the
    1840 px line at 1080p, measured with burn()). `min_piece`: no piece under that many units (the
    English video's .srt asks for it when a cue would be too short to read and cannot join its own
    sentence's neighbour: "Minutes later, it started six sub-agents building scenes" + "while the
    review was still running.", not "Minutes later," alone)."""
    text = " ".join(text.split())
    if units(strip_end(text) if hang else text) <= limit:
        return [text]
    lines = not hang
    good, ok = _cuts(text, lines=lines)
    stops = "，；：。！？,;:.!?…—"                     # not after 、, a closing quote or bracket
    punct = [c for c in good if _cut_penalty(text, c, lines) == 0 and text[c - 1] in stops + " "
             and (text[c - 1] != " " or text[c - 2] in stops)
             and (hang or _mark_cost(text, c) < 10)]   # no line or English cue break at "broad, / flexible"
    strong = [c for c in punct if text[:c].rstrip()[-1:] in "；。！？;.!?"
              and not (text[:c].rstrip()[-1:] == "." and text[c:c + 1].islower())]
    clause = sorted(set(punct) | {c for c in good if clauses and text[c - 1] == " " and text[c - 2].isalnum()
                                  and _clean_break(text, c)})
    total = units(text)

    def pieces_of(cuts):
        return [text[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(text)])]

    def fits(p):
        q = strip_end(p) if hang else p
        if clauses and units(q) > limit / 2:              # an English cue: two lines of limit / 2, not
            return any(units(q[:x].strip()) <= limit / 2 and units(q[x:].strip()) <= limit / 2   # broken
                       and (_break_cost(q, x) <= 12 or relax and _break_cost(q, x) <= 16   # inside a name
                            and not _name_gap(q, x)) for x in _cuts(q, lines=True)[0])
        if hang and line and line < limit and units(q) > line:   # a cue of 2 lines: one that wraps in 2
            return len(_wrapped(q, line)) <= 2                     # ("…clip（梯度裁剪），/ 就像……敏感度")
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
        """How often a Chinese cue runs on across a ；。！？ between two clauses in mid-line ("在每个数据库上
        都是这样；那么 f 的敏感度最多是两倍 σ"): one cue more keeps one clause per cue."""
        if not (hang and _CJK.search(text)):
            return 0
        rows = [(r, bool(_SEMI_LIST.search(strip_end(p)))) for p in pieces   # (not in a ；-list: 隐私的定义；
                for r in (_wrapped(strip_end(p), line) if line and line < limit else [strip_end(p)])]   # 一个数……)
        return sum(1 for r, listed in rows for m in re.finditer(r"[；。！？]", r)
                   if units(r[:m.start()]) >= 4 and units(r[m.end():].strip()) >= 4
                   and not (m.group() == "；" and listed))

    def weak(pieces):
        """A cut at a weak comma ("对大多数 mask，/ 它也估计不出……", "叫 winner，/ 意思是……")."""
        pos, out = 0, False
        for p in pieces[1:]:
            pos = text.find(p, pos + 1)
            out = out or _mark_cost(text, pos) >= 8
        return out

    def gaps(k):
        """Word gaps near the ideal position (those that leave pieces that fit first: "the US Census
        Bureau protected / its published tables…", not a third line), else anywhere. Only near ones:
        a cut anywhere that fits is often inside a word, where one piece more is better."""
        def pool(prev, ideal, last):
            near = [c for c in good if c > prev and abs(units(text[:c]) - ideal) <= total / (2.5 * k)
                    and text[c - 1] != "、"]
            fit = [c for c in near if fits(text[prev:c].strip()) and (not last or fits(text[c:].strip()))
                   and _cut_penalty(text, c, lines) < 10]       # not "…one release that is / accurate…"
            if clauses:                                   # an English cue: rather one cue more than
                fit = [c for c in fit if _cue_cost(text, c) < 10]   # "…Adam Smith answered // both questions"
            return fit or near or [c for c in ok + good if c > prev]
        return pool

    def attempt(k, kind):
        pool_of = {"strong": fitting(strong), "punct": fitting(punct), "whole": fitting(punct),
                   "firm": fitting([c for c in punct if _mark_cost(text, c) < 8]),   # no weak comma
                   "clause": fitting(clause)}.get(kind) or gaps(k)
        cuts = _pick_cuts(text, k, pool_of, total, lines, cue=clauses)
        if cuts is None:
            return None
        pieces = pieces_of(cuts)
        if not all(fits(p) for p in pieces):
            return None
        sizes = [units(p) for p in pieces]
        if min_piece and min(sizes) < min_piece:
            return None
        if kind == "strong" and min(sizes) < limit / 4:
            return None                                   # not "第二：/ ……"
        if kind in ("punct", "whole", "firm") and stray(cuts, pieces):
            return None
        if kind == "clause" and min(sizes) < max(sizes) / 3:
            return None
        return pieces

    def search():
        found = []                                        # Chinese cues: whole clauses (at up to two cues
        for k in range(2, 40):                            # more), the fewest run-ons across a ；。！？, no
                                                          # weak comma when one cue more avoids it
            plan = [(k, "strong"), (k, "punct")]
            if hang:                                      # whole clauses first, at one cue more if need be
                plan = [(k, "strong"), (k, "whole"), (k, "firm"), (k + 1, "strong"), (k + 1, "whole"),
                        (k, "punct")]
            if clauses:
                plan += [(k, "clause"), (k + 1, "strong"), (k + 1, "punct"), (k + 1, "clause")]
            if hang and _CJK.search(text):
                found += [(straddles(p), weak(p), len(p), n, p) for n, (kk, kind) in enumerate(plan[:5])
                          if (p := attempt(kk, kind))]
                if found and (k > min(len(x[4]) for x in found) or not any(found[0][:2])):
                    return min(found, key=lambda x: x[:4])[4]
                if found:
                    continue
                plan = plan[5:]
            for kk, kind in plan + [(k, "gaps")]:
                pieces = attempt(kk, kind)
                if pieces:
                    return pieces
        return [text]

    relax = False
    out = search()
    if not clauses or len(out) < 2:
        return out

    def bad(pieces):                                      # cue cuts at a gap that costs 10 or more
        pos, n = 0, 0
        for q in pieces[1:]:
            pos = text.find(q, pos + 1)
            n += _cue_cost(text, pos) >= 10
        return n
    if bad(out):                                          # rather a line break that costs up to 16 (not in
        relax = True                                      # a name) than such a cue cut: "that chess has at
        alt = search()                                    # least / 10 to the power of 120 possible games."
        if bad(alt) < bad(out):                           # (44 characters), not "…at least // 10 to the…"
            out = alt
    return out


@lru_cache(maxsize=8192)
def _wrapped(text: str, line: float) -> tuple[str, ...]:
    """The lines of a Chinese cue: split_balanced, but a line may run 1.5 units over rather than break
    a list of Latin names or leave the cue a line too many ("然后在 2003 年，Irit Dinur 和 Kobbi Nissim /
    证明了一个令人警醒的结论", "同年她与 / Kenthapadi、McSherry、Mironov 和 Naor 合作")."""
    ls = split_balanced(text, line)
    if not _CJK.search(text) or len(ls) == 1:
        return tuple(ls)
    c = len(text) - len(text[len(ls[0]):].lstrip())
    if len(ls) > 2 or _mark_cost(text, c) >= 10:          # "Kenthapadi、/ McSherry、"
        alt = _rewrap(text, line + 1.5, lambda x: not (re.search(r"[A-Za-z](?:、| [和与及])?$", text[:x].rstrip())
                                                       and re.match(r"(?:[和与及] )?[A-Za-z]", text[x:].lstrip())))
        x = len(alt[0]) if alt else 0
        if (alt and all(units(y) <= line or _NAME_LIST.search(y) for y in alt)
                and (len(ls) == 2 or (max(units(y) for y in alt) > line and _break_cost(text, x) < 8))):
            return tuple(alt)                             # (not a 2-line wrap that split_balanced passed over)
    if len(ls) > 2 and _SEMI_LIST.search(text):           # a ；-list item may run 0.5 over: "隐私的定义；一个数叫
        alt = _rewrap(text, line + 0.5, lambda x: text[:x].rstrip()[-1:] == "；")   # 敏感度（sensitivity）；/ 以及……"
        if alt:
            return tuple(alt)
    return tuple(ls)


_NAME_LIST = re.compile(r"[A-Za-z][\w.'-]*(?:、| [和与及] )[A-Z]")   # Kenthapadi、McSherry; Dinur 和 Kobbi


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


def _balance(times, us: list[float], rate: float = 9.0, shift: float = 1.0, min_dur: float = 1.0):
    """timing="en": the band pieces of one sentence are timed by their English pieces, so a long
    Chinese piece over a short English one reads too fast ("没想到吧：答案是边格，也就是每条边正中间的
    那一格 || Surprise: the edge," 24 units in 1.3 s). When the faster of two neighbouring pieces
    reads faster than `rate` units/s (`us`: the units of each piece) and than their average, their
    switch moves toward equal reading rates, by at most `shift` s (the English stays near its
    voice) and keeping the slower piece min_dur s up."""
    out = [list(x) for x in times]
    for i in range(len(out) - 1):
        lo, t, hi = out[i][0], out[i][1], out[i + 1][1]
        u1, u2 = us[i], us[i + 1]
        if hi - lo <= 0 or u1 + u2 <= 0:
            continue
        cap = max(rate, (u1 + u2) / (hi - lo))
        if u1 > cap * (t - lo):
            t2 = min(lo + u1 / cap, t + shift, max(t, hi - min_dur))
        elif u2 > cap * (hi - t):
            t2 = max(hi - u2 / cap, t - shift, min(t, lo + min_dur))
        else:
            continue
        out[i][1] = out[i + 1][0] = t2
    return [tuple(x) for x in out]


class _Clock:
    """When each position of a sentence is on screen (timing="en": at the band's switch times,
    linear in units inside a band piece), so that the sidecar cues of the sentence switch where
    the band switches, also when _two_lines re-splits one of them. A clock is carried in a cue's
    4th field, like the spoken form for timing="tr"; `offset` is where the cue starts in the text."""

    def __init__(self, text: str, ref: list[str], ref_times, offset: int = 0, knots=None):
        self.text, self.offset = " ".join(text.split()), offset
        if knots is None:
            pos, knots = 0, []
            for p, (s0, s1, _) in zip(ref, ref_times):
                pos = max(pos, self.text.find(p, pos))
                knots.append((units(self.text[:pos]), s0))
            knots.append((units(self.text), ref_times[-1][1]))
        self.knots = knots

    def at(self, pos: int) -> float:
        u = units(self.text[:self.offset + pos])
        for (k0, t0), (k1, t1) in zip(self.knots, self.knots[1:]):
            if u <= k1 + 1e-9:
                return t0 + (t1 - t0) * max(0.0, u - k0) / ((k1 - k0) or 1)
        return self.knots[-1][1]

    def times(self, text: str, pieces: list[str], a: float, b: float) -> list[tuple] | None:
        """(start, end, piece, clock) for consecutive pieces of `text` (this cue's text), or None
        when a piece is not found."""
        starts, pos = [], 0
        for p in pieces:
            pos = text.find(p, pos)
            if pos < 0:
                return None
            starts.append(pos)
        cuts = [a] + [min(b, max(a, self.at(x))) for x in starts[1:]] + [b]
        return [(x, y, p, _Clock(self.text, [], [], self.offset + o, self.knots))
                for x, y, p, o in zip(cuts, cuts[1:], pieces, starts)]


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
    - A cue still shorter than `min_dur` takes time from a neighbour of its sentence (a Chinese
      cue up to 0.2 s per unit, at most 1.5 s, while that neighbour reads slower), as long as the
      neighbour keeps its own minimum; after `min_show`, a cue still under `min_dur` borrows across
      the 0.05 s gap to the next sentence.
    - timing="en": the band pieces follow the English pieces, but a switch moves toward equal
      Chinese reading rates where a piece would read faster than 9 units/s (_balance), and the
      Chinese of a sentence may run up to 0.5 s into the next one (_push); the .zh.srt cues switch
      where the band switches (_Clock).
    - Single-language cues have at most 2 lines; a longer piece becomes two cues (timed by the
      spoken form too), and an English cue whose two lines break mid-phrase becomes two cues
      when a clause cut gives cleaner lines; an English cue boundary that is not a clean break
      then moves to the nearest clean one when both cues keep good lines (_reflow_en).
    - In the bilingual track, the English sentence is cut where the Chinese one is (at the
      matching clause boundary, see _split_like); when it fits on one line and no boundary is
      close, the whole English sentence stays up under each Chinese piece.
    - Every cue stays up at least `min_show` seconds when the next cue leaves room."""
    zh, en, bi = [], [], []
    free = float("-inf")                                  # timing="en": where the previous Chinese ended
    for n, (a, b, t, e, *say) in enumerate(pairs):
        spoken = say[0] if say and say[0] and timing == "tr" else None
        en += _proportional(a, b, split_balanced(e, 2 * en_limit, clauses=True))
        if not t:
            continue
        zp = split_balanced(t, bi_zh_limit, hang=True)
        ne = len(split_balanced(e, bi_en_limit))
        if ne > len(zp):
            zp = _split_k(t, ne, bi_zh_limit)
        ep, same = _split_like(e, zp, bi_en_limit)
        if timing != "tr":                                # the Chinese may stay into the pause after
            a = max(a, free)                              # a fast English sentence (9 units/s), and
            b = max(b, min(_room(pairs, n) + _push(pairs, n, a), a + units(t) / 9))   # up to 0.5 s into
            free = b + 0.05                               # the next one when that one has time to spare
        if timing == "tr":
            band = _proportional(a, b, zp, spoken and _spoken_weights(t, zp, spoken))
        elif same:                                        # the English stays up: the Chinese sets the pace
            band = _proportional(a, b, zp)
        else:                                             # the English pieces, then the Chinese reading rate
            band = _balance(_proportional(a, b, ep), [units(strip_end(p)) for p in zp], min_dur=min_dur)
        for (s0, s1, _), zt, et in zip(band, zp, ep):
            bi.append((s0, s1, zt, et, n if same else None))
        zs = split_balanced(t, 2 * zh_limit, hang=True, line=zh_limit)
        timed = timing != "tr" and _Clock(t, zp, band).times(" ".join(t.split()), zs, a, b)
        if not timed:
            parts = (spoken and _spoken_parts(t, zs, spoken)) or [None] * len(zs)
            times = _proportional(a, b, zs, parts[0] and [units(q) for q in parts])
            timed = [(s0, s1, z, q) for (s0, s1, z), q in zip(times, parts)]
        zh += timed                                       # timing="en": switch where the band switches
    zh = _merge_short(zh, lambda x, y: _fits_join(x, y, zh_limit, 2), min_dur)
    en = _merge_short(en, lambda x, y: _fits_join(x, y, en_limit, 2), min_dur)
    bi = _merge_short(bi, None, min_dur, bi_zh_limit, bi_en_limit)
    zh = _stretch([c for x in zh for c in _two_lines(x, zh_limit, min_dur)], min_dur)
    en = _stretch(_reflow_en([c for x in en for c in _two_lines(x, en_limit, min_dur)], en_limit), min_dur)
    bi = _stretch([(s0, s1, strip_end(z), e) for s0, s1, z, e, _ in bi], min_dur)
    out = {"zh": zh, "en": en, "zh-en": bi}             # a cue that could not linger to min_dur
    return {k: _stretch(_linger(v, min_show), min_dur, gap=0.06, per_unit=False)   # borrows across the
            for k, v in out.items()}                                                # 0.05 s gap


def _room(pairs, n: int) -> float:
    """timing="en": until when the Chinese of sentence n may stay up (just before the next sentence)."""
    return pairs[n + 1][0] - 0.05 if n + 1 < len(pairs) else pairs[n][1]


def _push(pairs, n: int, a: float, rate: float = 9.0, most: float = 0.5) -> float:
    """timing="en": how far the Chinese of sentence n, from `a`, may run into sentence n + 1, which
    then starts that much later: as far as it needs to be read at `rate` units/s ("没想到吧：答案是边格，
    也就是每条边正中间的那一格 || Surprise: the edge," 24 units under a 19-character English piece), at
    most `most` s, and only while sentence n + 1 can still be read at that rate."""
    if n + 1 >= len(pairs) or not pairs[n + 1][2]:
        return 0.0
    over = a + units(pairs[n][2]) / rate - _room(pairs, n)
    a1, b1, t1 = pairs[n + 1][:3]
    spare = max(b1, min(_room(pairs, n + 1), a1 + units(t1) / rate)) - a1 - units(t1) / rate
    return max(0.0, min(over, most, spare))


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
    if (len(runs) > 1 and last and len(last) <= 3 and last[0].lower() in ("a", "an", "the")
            and nxt.lower() in ("a", "an", "the")):
        return True                                       # "a ranking, / a set, a string of bits"
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
    zu = [units(re.sub(r"（[^（）]*）", "", strip_end(p))) for p in zp]   # the glosses have no English,
                                                                        # the closing ，nothing on screen,
    if not re.search(r"\bmean(?:s|ing)?\b", e):                         # nor a restated term ("explore
        zu = [max(1.0, u - sum(units(m.group()) for m in _QUOTE_GLOSS.finditer(p)))   # 就是“探索”的意思"
              for u, p in zip(zu, zp)]                                  # under "…called explore.")
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
        if not (e[c - 1] == " " and e[c - 2].isalnum()) or abs(units(e[:c]) - aim) > (0.1 if plain else 0.12) * units(e):
            return None                                    # (a clean gap a little further: "…move 8 or 9 / have…")
        nxt, before = (e[c:].split() or [""])[0].lower(), (e[:c].split() or [""])[-1].lower()
        if before in _FUNCTION_WORDS | _CLAUSE_STARTERS | _PRONOUNS | _DETERMINERS | _ADVERBS | _NUMBER_WORDS:
            return None                                    # not "…the coin talking, yet / over…"
        pen = _cut_penalty(e, c)
        if nxt in _AUXILIARIES | _CLAUSE_STARTERS and pen <= 1:   # not "whether a patient / was in…"
            extra = 4.0
        elif (plain and pen <= 4 and len(e) >= 60 and nxt != "of"
              and nxt not in _FUNCTION_WORDS - _PREPOSITIONS | _DETERMINERS | _PRONOUNS):
            extra = 6.0                                    # "…sharper analysis / got this down…"
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
            if not gaps and (top is None or clause_cost(top[1], prev, j) >= 4):   # a plain gap only instead
                gaps = [(total_cost(c, cost), c) for c in pool     # of nothing or of a stop whose clauses
                                                                    # do not match ("…sensitivity/ε / makes it
                                                                    # private," under "……拉普拉斯噪声 / 就能让它……")
                        if (cost := gap_cost(c, j, aim, miss[c] - floor, plain=True)) is not None]
            scored += gaps
        c = min(scored, key=rank, default=(0.0, None))[1]
        stops = []                                         # no clean gap near puts the numbers right: a stop
        if c is not None and miss[c] > floor and not any(miss[x] == floor and _cut_penalty(e, x) <= 1
                                                         and abs(units(e[:x]) - aim) <= cap for x in pool):
            stops = [x for x in scored if miss[x[1]] - floor <= 2 and clause_cost(x[1], prev, j) < 4
                     and e[:x[1]].rstrip()[-1:] in ",;:.!?—"]   # that misplaces one number and otherwise
            c = min(stops, key=rank)[1] if stops else c   # matches ("list all 8 winning lines, /" under
        if c is None or miss[c] > floor and not stops:     # "……都列出来 / 一共 8 条", not "list all / 8"); else
            best.append(None)                              # repeat, or the fallback below ("…that ends on move 5 /
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
            c = min(pool, key=lambda x: (mismatch(x, prev, j),   # (as a cue end: "…person's row // changes
                                         abs(units(e[:x]) - targets[j]) + _cue_cost(e, x)))   # the…", not "…changes // the")
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
    if (nxt in _DETERMINERS - {"that"} and prev.isalpha() and prev not in _FUNCTION_WORDS
            and not _bare_clause(text, c)):
        q += 2.0
    return q


_ENDERS = _DETERMINERS | _PREPOSITIONS | _AUXILIARIES


def _cue_cost(text: str, c: int) -> float:
    """How bad an English cue boundary at c is: the cost of the cut and its mark, 4 more before a
    determiner (a verb and its object: "…Adam Smith answered // both questions"), 6 more inside a list
    ("Frank McSherry, // Kobbi Nissim and Adam Smith") and 20 more after an article, determiner,
    preposition or auxiliary ("…just ask the // interactive curator")."""
    prev, nxt = (text[:c].split() or [""])[-1].lower(), (text[c:].split() or [""])[0].lower()
    q = _cut_penalty(text, c) + _mark_cost(text, c)
    if (nxt in _DETERMINERS - {"that"} and prev.isalpha() and prev not in _FUNCTION_WORDS
            and not _bare_clause(text, c)):
        q += 4.0                                          # (a line break there costs 2)
    if _mark_cost(text, c) >= 10 or _list_and(text, c):
        q += 6.0                                          # inside a list: "Frank McSherry, // Kobbi Nissim"
    pronoun = prev in ("this", "that", "these", "those") and nxt in _AUXILIARIES   # "…like this // is the L1 norm"
    return q + (20.0 if prev in _ENDERS and not pronoun and not _verb_like(text, c) else 0.0)


def _clean_break(text: str, c: int) -> bool:
    """An English line or cue break at c that follows the sentence: after a clause mark (not a list
    or appositive comma), or before and / but / which … (not the 'and' that closes a list or joins
    two names or numbers, "McSherry / and Talwar's", "move 8 / or 9"; not then / so without a
    comma, "The joint density / then depends"; not "even / if")."""
    prev, nxt = (text[:c].split() or [""])[-1], (text[c:].split() or [""])[0]
    if prev[-1:] in ",;:.!?—":
        return _mark_cost(text, c) < 10
    complement = nxt in ("what", "how", "where", "why", "who", "which") and bool(   # "it is exactly / what…"
        re.search(r"\b(?:is|are|was|were|be|been)(?: [a-z]+ly| just| not)? $", text[:c]))
    return (((nxt in _CLAUSE_WORDS - {"then", "so"} and not _adverb_yet(text, c))   # (not "no record / yet")
             or _that_clause(text, c) or _bare_clause(text, c))
            and prev.lower() not in _FUNCTION_WORDS and not _list_and(text, c) and not _binomial(text, c)
            and not complement
            and _cut_penalty(text, c) <= 4)


def _rewrap(text: str, limit: float, accept, min_line: float = 0.0, weight: float = 1.0) -> list[str] | None:
    """The best 2-line wrap of text whose break passes `accept` (`weight` per unit of imbalance plus
    the break cost), with both lines within `limit` and at least `min_line` units, or None."""
    good, ok = _cuts(text, lines=True)
    best = None
    for c in good + ok:
        left, right = text[:c].strip(), text[c:].strip()
        if (not left or not right or max(units(left), units(right)) > limit
                or min(units(left), units(right)) < min_line or not accept(c)):
            continue
        cost = weight * abs(units(left) - units(right)) + _break_cost(text, c)
        if best is None or cost < best[0]:
            best = (cost, [left, right])
    return best and best[1]


@lru_cache(maxsize=4096)
def wrap_en(text: str, limit: float) -> tuple[str, ...]:
    """The lines of an English cue (2 when it fits): balanced, but re-wrapped at a clean break when
    the balanced one splits a phrase and a clean one fits ("Remember the Gaussian / whose ratio
    escaped…"), and when it costs 7 or more, at a break that costs 3 less whatever the balance if
    that one starts a clause or the first costs 10 or more ("Theorem 3 shows / that for at least 2/3
    of these queries," not "…for at least / 2/3…"; "It founded / what we now call…"). Also the
    lines of the English video's .srt (explainer.build.split_cues)."""
    ls = split_balanced(text, limit)
    if len(ls) != 2:
        return tuple(ls)
    c = len(text) - len(text[len(ls[0]):].lstrip())
    if not _clean_break(text, c):
        ls = _rewrap(text, limit, lambda x: _clean_break(text, x), limit / 3) or ls
        c = len(text) - len(text[len(ls[0]):].lstrip())
    q = _break_cost(text, c)

    def better(x):                                        # before a clause, or much cheaper (before a
        nxt = (text[x:].split() or [""])[0]               # preposition: "track the budget / over thousands…")
        q2 = _break_cost(text, x)
        return q2 <= q - 3 and (q >= 10 or nxt in _SUBORDINATORS | {"what", "how", "why"} or _bare_clause(text, x)
                                or (nxt in _PREPOSITIONS and q2 <= q - 5))
    if q >= 7:
        ls = _rewrap(text, limit, better, limit / 5, 0.25) or ls
    return tuple(ls)


def _two_lines(cue, limit: float, min_dur: float = 1.0) -> list[tuple[float, float, str]]:
    """A cue wrapped to at most 2 lines; a piece that needs more becomes two cues (time split in
    proportion to their spoken form, cue[3], when there is one, else their length), cut at a clause
    boundary when one gives two 2-line cues. Two lines that split a list at its 、 ("光凭邮编、/
    出生日期和性别") also become two cues when a clause cut gives two 2-line cues. Two English lines
    that break mid-phrase are re-wrapped at a clean break when one fits ("Remember the Gaussian /
    whose ratio escaped…"), else become two cues when a clause cut gives cues whose lines break no
    worse ("But SuLQ only covered sums," + "and its definition tolerated / a tiny chance…"). An
    English cue that needs 3 lines is cut at one of its own line breaks or at a clean break ("First:
    what is the sensitivity" + "of the average of n numbers / between zero and one?"), and of two
    clean stops the stronger mark wins ("Pause and ponder:" + "if Alice's true answer is yes, /
    how likely…"). A Chinese line may run 1.5 units over the limit rather than break a list of
    Latin names (同年她与 / Kenthapadi、McSherry、Mironov 和 Naor 合作)."""
    a, b, text, *rest = cue
    spoken = rest[0] if rest else None
    text = strip_end(text)
    english = not _CJK.search(text)

    @lru_cache(maxsize=None)
    def wrap2(t):                                         # the lines of t
        ls = split_balanced(t, limit)
        if len(ls) != 2 and not english:
            return _wrapped(t, limit)
        if len(ls) != 2:
            return tuple(ls)
        if english:                                       # "Next, the computer needs to know /
            return wrap_en(t, limit)                       # what counts as a win."
        return _wrapped(t, limit)

    def breaks(t):                                        # where the 2 lines of t break
        ls = wrap2(t)
        return [len(t) - len(t[len(ls[0]):].lstrip())] if len(ls) == 2 else []

    def listy(t):                                         # two lines that split a list at its 、
        return any(t[:c].rstrip()[-1:] == "、" for c in breaks(t))

    def worst(*parts):                                    # the worst line break of these cues ("ask the /
        return max([0.0] + [0.0 if english and _clean_break(t, c) else _break_cost(t, c)   # interactive")
                            + (20.0 if english and (t[:c].split() or [""])[-1].lower() in _ENDERS
                                      and not _verb_like(t, c) else 0.0)
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
    own = set()                                           # an English cue of 3 lines: cut at one of its line
    if english and len(lines) > 2:                        # breaks or at a clean break ("First: what is the
        pos = 0                                           # sensitivity" + "of the average of n numbers /
        for ln in lines[1:]:                              # between zero and one?")
            pos = text.find(ln, pos + 1)
            own.add(pos)
    for c in good + ok:
        left, right = text[:c].strip(), text[c:].strip()
        if not left or not right:
            continue
        if own and c not in own and not _clean_break(text, c):
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
        weak = max(0.0, _mark_cost(text, c) - 3)          # a weak comma: "…the next one, // is called…"
        split = worst(left, right) + weak
        orphan = min(units(left), units(right)) < limit / 3
        short = min(units(left), units(right)) < limit / 2
        tail = units(right) < limit / 2 and right[-1:] in ",;"   # a fragment that runs on into the next cue
        if mid_phrase and (orphan and worst(text) <= 4 or not (   # (not "Trying a path," alone for
                split < worst(text) or worst(text) > 4 and split <= worst(text) + 2 and not short   # "…back /
                or not weak and split <= worst(text) + 3 and midline(left, right) < midline(text) and not tail)):
            continue                                      # to try…", nor "its sensitivity," alone for "…property
                                                          # / of the query:")
        if len(lines) == 2 and (b - a) * min(units(left), units(right)) / units(text) < min_dur:
            continue                                      # (not into a cue too short to read)
        if english:                                       # the lines matter more than the balance
            cost = (0.5 * abs(units(left) - units(right)) + _cue_cost(text, c) + worst(left, right)
                    + (2 * _mark_cost(text, c) if at_stop and not orphan else 0))   # the stronger of two clean
                                                          # marks: "Pause and ponder:" +
                                                          # "if Alice's true answer is yes, / how likely is she…"
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
    timed = isinstance(spoken, _Clock) and spoken.times(text, halves, a, b)
    if not timed:
        said = (isinstance(spoken, str) and _spoken_parts(text, halves, spoken)) or [None] * len(halves)
        timed = [(s0, s1, h, q) for (s0, s1, h), q in
                 zip(_proportional(a, b, halves, said[0] and [units(x) for x in said]), said)]
    return [c for x in timed for c in _two_lines(x, limit, min_dur)]


def _reflow_en(cues, limit: float):
    """Move the boundary between two English cues of one sentence (back to back) that is not a clean
    break to the nearest clean break in either cue, when both cues still have 2 lines that break no
    worse ("Latanya Sweeney showed / that ZIP code, birth date and sex alone" + "single out most
    Americans," → "Latanya Sweeney showed" + "that ZIP code, birth date and sex alone / single out most
    Americans,"); the switch time moves with the text (in proportion to its length)."""
    out = [list(c) for c in cues]

    def lines_cost(t):                                    # the worst line break of a cue, or None (3 lines)
        ls = wrap_en(t, limit)
        if len(ls) > 2:
            return None
        return 0.0 if len(ls) == 1 or _clean_break(t, len(ls[0]) + 1) else _break_cost(t, len(ls[0]) + 1)

    for i in range(len(out) - 1):
        (a0, a1, x), (b0, b1, y) = out[i][:3], out[i + 1][:3]
        if _CJK.search(x + y) or abs(b0 - a1) > 1e-6 or re.search(r"[.!?]$", x.replace("\n", " ").strip()):
            continue
        x, y = " ".join(x.split()), " ".join(y.split())
        text, c = x + " " + y, len(x) + 1
        if _clean_break(text, c) or _cue_cost(text, c) < 7:
            continue                                      # (a bad break may move into a cue: a line break
        now = max(lines_cost(x) or 0.0, lines_cost(y) or 0.0, min(_cue_cost(text, c), 9.0))   # is milder)
        best = None
        for d in [d for d in _cuts(text)[0] if d != c and _clean_break(text, d) and _cue_cost(text, d) < 7]:
            left, right = text[:d].strip(), text[d:].strip()
            q = [lines_cost(left), lines_cost(right)]
            if None in q or max(q) > now or min(units(left), units(right)) < limit / 3:
                continue
            if best is None or abs(d - c) < abs(best - c):
                best = d
        if best is not None:
            t = a0 + (b1 - a0) * len(text[:best].strip()) / max(1, len(text) - 1)
            out[i][1:3] = [t, "\n".join(wrap_en(text[:best].strip(), limit))]
            out[i + 1][0], out[i + 1][2] = t, "\n".join(wrap_en(text[best:].strip(), limit))
    return [tuple(c) for c in out]


def _stretch(cues, min_dur: float, gap: float = 0.01, per_unit: bool = True):
    """A cue shorter than min_dur (a merge did not fit), or (`per_unit`) a Chinese cue shorter than
    0.2 s per unit (at most 1.5 s, in an English video, where the English voice sets the pace),
    takes the time from a neighbour less than `gap` s away (by default: of the same sentence) with
    time to spare, the longer one first. The neighbour keeps
    its own minimum, and beyond min_dur a Chinese neighbour gives only until the two read equally
    fast ("这里说的“一局”" 0.68 s + 23 units in 2.85 s → 1.0 s + 2.53 s, not 1.42 s + 2.11 s)."""
    out = [list(c) for c in cues]

    def zh_units(c):
        return units(c[2].replace("\n", "")) if _CJK.search(c[2]) else 0.0

    def need(c):                                          # Chinese: 0.2 s per unit, up to 1.5 s
        return max(min_dur, min(1.5, 0.2 * zh_units(c))) if per_unit else min_dur

    for i, c in enumerate(out):
        if c[1] - c[0] >= need(c):
            continue
        nbrs = [j for j in (i - 1, i + 1) if 0 <= j < len(out) and -1e-6 <= (out[j][0] - c[1] if j > i
                                                                           else c[0] - out[j][1]) < gap]
        for j in sorted(nbrs, key=lambda j: out[j][0] - out[j][1]):
            dc, dd = c[1] - c[0], out[j][1] - out[j][0]
            want = need(c) - dc
            uc, ud = zh_units(c), zh_units(out[j])
            if uc and ud:                                 # past min_dur, only while it reads slower
                want = min(want, max(min_dur - dc, (uc * dd - ud * dc) / (uc + ud)))
            give = min(want, dd - need(out[j]))
            if give <= 0:
                continue
            if j > i:                                     # (a gap between them stays)
                c[1] += give
                out[j][0] += give
            else:
                c[0] -= give
                out[j][1] -= give
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
        order = (i + 1, i - 1)
        ask = [0 <= j < len(cues) and cues[j][2].rstrip()[-1:] in "？?" for j in (i - 1, i, i + 1)]
        if ask[0] and ask[1] and not ask[2]:              # a short question joins the parallel question before
            order = (i - 1, i + 1)                        # it: "猜一猜。一百？一百万？" + "暂停一下视频……"
        for j in order:
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
                cues[lo:hi + 1] = [[cues[lo][0], cues[hi][1], text, *(   # (the spoken forms; not clocks)
                    [said[0] + said[1] if all(isinstance(x, str) for x in said) else None] if said else [])]]
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
