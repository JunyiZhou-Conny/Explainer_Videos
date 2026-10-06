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
from pathlib import Path

_CJK = re.compile(r"[⺀-鿿豈-﫿＀-￯　-〿]")
_BREAK_AFTER = "，、；：。！？,;:—)）」』”"
SENTENCE_GAP = 0.32


def units(s: str) -> float:
    """Display width in 'CJK character' units (a Latin character is about half as wide)."""
    return sum(1.0 if _CJK.match(ch) else 0.55 for ch in s)


def _cuts(text: str) -> list[int]:
    """Positions where a line or cue may break: after punctuation, at spaces, between CJK chars."""
    good, ok = [], []
    for i in range(1, len(text)):
        a, b = text[i - 1], text[i]
        if a in _BREAK_AFTER or (a == " " and b != " "):
            good.append(i)
        elif (_CJK.match(a) or _CJK.match(b)) and b not in _BREAK_AFTER and a not in "（(「『“":
            ok.append(i)
    return good, ok


def split_balanced(text: str, limit: float) -> list[str]:
    """Fewest pieces of at most `limit` units each, balanced in length, cut at punctuation or
    spaces when possible (anywhere between CJK characters otherwise)."""
    text = " ".join(text.split())
    if units(text) <= limit:
        return [text]
    good, ok = _cuts(text)
    total = units(text)
    for k in range(2, 40):
        cuts, prev = [], 0
        for j in range(1, k):
            ideal_u = total * j / k
            def u_at(i):
                return units(text[:i])
            window = [c for c in good if c > prev and abs(u_at(c) - ideal_u) <= total / (2.5 * k)]
            pool = window or [c for c in ok + good if c > prev]
            if not pool:
                break
            cut = min(pool, key=lambda c: abs(u_at(c) - ideal_u))
            cuts.append(cut)
            prev = cut
        pieces = [text[a:b].strip() for a, b in zip([0, *cuts], [*cuts, len(text)])]
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
           bi_zh_limit: float = 30, bi_en_limit: float = 88 * 0.55) -> dict:
    """Subtitle tracks from sentence pairs. `timing` = "tr" (the translated audio drives the
    timing inside a sentence) or "en"."""
    zh, en, bi = [], [], []
    for a, b, t, e in pairs:
        if t:
            zh += _proportional(a, b, [wrap(p, zh_limit) for p in split_balanced(t, 2 * zh_limit)])
        en += _proportional(a, b, [wrap(p, en_limit) for p in split_balanced(e, 2 * en_limit)])
        if t:
            k_zh = len(split_balanced(t, bi_zh_limit))
            k_en = len(split_balanced(e, bi_en_limit))
            k = max(k_zh, k_en)
            zp = _split_k(t, k, bi_zh_limit)
            ep = _split_k(e, k, bi_en_limit)
            drive = zp if timing == "tr" else ep
            for (s0, s1, _), zt, et in zip(_proportional(a, b, drive), zp, ep):
                bi.append((s0, s1, zt, et))
    return {"zh": zh, "en": en, "zh-en": bi}


def _split_k(text: str, k: int, limit: float) -> list[str]:
    """Split into exactly k balanced pieces (fewer pieces are padded by splitting the longest)."""
    pieces = split_balanced(text, limit)
    while len(pieces) < k:
        i = max(range(len(pieces)), key=lambda j: units(pieces[j]))
        sub = split_balanced(pieces[i], units(pieces[i]) / 2 + 0.6)
        if len(sub) < 2:
            pieces.append("")
            continue
        pieces[i:i + 1] = sub[:2] if len(sub) == 2 else [sub[0], " ".join(sub[1:])]
    while len(pieces) > k:                   # merge the shortest neighbours
        i = min(range(len(pieces) - 1), key=lambda j: units(pieces[j]) + units(pieces[j + 1]))
        sep = "" if (pieces[i] and _CJK.match(pieces[i][-1])) else " "
        pieces[i:i + 2] = [(pieces[i] + sep + pieces[i + 1]).strip()]
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
