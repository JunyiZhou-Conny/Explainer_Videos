"""Bilingual captions of the short format: captions.yaml, reading times, layouts, .ass/.srt files.

A short has no narrator; its words are captions, one Chinese line with an English line under it (or
the other way round for an English-first master). They are kept per scene in the project's
`captions.yaml` (text that reviewers and translators edit without touching scene code):

    s01_cold_open:                      # scene file stem (or class name)
      - id: games                       # optional; lets scene code place it: self.caption("games")
        zh: 井字棋有多少种不同的对局？
        en: How many different games of tic-tac-toe are there?
        at: "1:2"                       # optional grid position in the scene ("bar:beat", from 0; or "4.8s")
        beats: 6                        # optional length (or dur: seconds); default: reading time
      - zh: 终局一样，顺序不同，就是两局。
        en: Same final board, different order. Two different games.

A caption with `at` is placed by the scene's grid automatically; one without is shown when the scene
calls `self.caption(id)` (or the n-th unplaced one with `self.caption()`); scene code may also pass
text inline: `self.caption(zh="…", en="…")`. Times land in the scene's events.json; text is re-read
from captions.yaml when the video is stitched, so a wording fix needs no re-render.

The stitch burns the captions into the picture (libass, `burn`), in the layout set by video.yaml:

    captions: {layout: zh-first}        # zh-first (default) | en-first | zh | en
                                        # layouts: [zh-first, en-first] makes one master per layout

zh-first: Chinese in a Song/Ming serif (Noto Serif CJK SC), glyphs about 39 px tall at 1080p with
the baseline at 87 % of the frame height; under it the English line in letter-spaced mono capitals
(Noto Sans Mono, cap height about 17 px, at about 93 %). en-first: English sentence case in Noto
Serif (cap height about 25 px) on top, the Chinese line (about 27 px) under it, grey. Fades 0.3 s.
The same cues are written as .zh.srt / .en.srt / .zh-en.srt sidecars.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field, replace
from functools import lru_cache
from pathlib import Path

from .grid import Grid

FADE = 0.3                 # seconds of fade in and out
MIN_DUR, MAX_DUR = 2.0, 6.5
ZH_RATE, EN_RATE = 5.0, 2.9   # characters / words per second a caption allows (the reference: 4-6, 2.9)

_CJK = re.compile(r"[⺀-鿿豈-﫿＀-￯　-〿]")


@dataclass(eq=False)          # captions are compared by identity (two lines may share a text)
class Caption:
    zh: str = ""
    en: str = ""
    id: str | None = None
    scene: str | None = None
    t: float | None = None         # start, seconds (scene time in a log; video time after stitching)
    dur: float | None = None
    at: str | None = None          # grid position from captions.yaml
    beats: float | None = None
    placed: str = ""               # "yaml" (by `at`), "code" (self.caption) or "" (not placed yet)
    fixed: bool = False            # its length was given (beats / dur), not the reading time

    @property
    def end(self) -> float:
        return (self.t or 0.0) + (self.dur or 0.0)

    def as_dict(self) -> dict:
        d = {"zh": self.zh, "en": self.en, "t": round(self.t or 0.0, 4), "dur": round(self.dur or 0.0, 4)}
        for k in ("id", "at", "beats"):
            if getattr(self, k) is not None:
                d[k] = getattr(self, k)
        d["placed"] = self.placed
        if self.fixed:
            d["fixed"] = True
        return d

    @classmethod
    def from_dict(cls, d: dict, scene: str | None = None) -> "Caption":
        return cls(zh=str(d.get("zh") or "").strip(), en=" ".join(str(d.get("en") or "").split()),
                   id=None if d.get("id") is None else str(d["id"]), scene=scene,
                   t=d.get("t"), dur=d.get("dur"), at=None if d.get("at") is None else str(d["at"]),
                   beats=d.get("beats"), placed=d.get("placed", ""),
                   fixed=bool(d.get("fixed") or d.get("beats") is not None or d.get("dur") is not None))


def cjk_count(s: str) -> int:
    return len(_CJK.findall(s or ""))


def reading_time(zh: str, en: str) -> float:
    """How long a caption stays up when no length is given: enough to read both lines."""
    t_zh = 0.8 + cjk_count(zh) / ZH_RATE if zh else 0.0
    t_en = 0.6 + len((en or "").split()) / EN_RATE if en else 0.0
    return round(min(MAX_DUR, max(MIN_DUR, t_zh, t_en)), 2)


def duration(c: Caption, grid: Grid) -> float:
    if c.dur is not None:
        return float(c.dur)
    if c.beats is not None:
        return float(c.beats) * grid.beat
    return reading_time(c.zh, c.en)


# ---------------------------------------------------------------- captions.yaml

def load(path: Path) -> dict[str, list[Caption]]:
    """{scene key: [Caption]} from a captions.yaml (missing file: {})."""
    import yaml

    path = Path(path)
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out: dict[str, list[Caption]] = {}
    for scene, items in data.items():
        if isinstance(items, dict):              # {id: {zh, en, ...}}
            items = [{"id": k, **(v or {})} for k, v in items.items()]
        out[str(scene)] = [Caption.from_dict(d or {}, str(scene)) for d in items or []]
    return out


def for_scene(table: dict[str, list[Caption]], *keys: str) -> list[Caption]:
    for k in keys:
        if k and k in table:
            return [replace(c) for c in table[k]]
    return []


def project_file(project: Path, spec: dict | None = None) -> Path:
    cfg = caption_config(spec or {})
    return Path(project) / cfg.get("file", "captions.yaml")


def caption_config(spec: dict) -> dict:
    c = spec.get("captions")
    if c is False:
        return {"enabled": False, "layouts": ["zh-first"], "layout": "zh-first"}
    if isinstance(c, str):
        c = {"layout": c}
    c = dict(c or {})
    c.setdefault("enabled", True)
    layouts = c.get("layouts") or [c.get("layout", "zh-first")]
    if isinstance(layouts, str):
        layouts = [layouts]
    c["layouts"] = list(layouts)
    c["layout"] = c["layouts"][0]
    return c


# ---------------------------------------------------------------- layouts

@dataclass(frozen=True)
class LineStyle:
    lang: str                      # which text: "zh" or "en"
    font: str
    size: float                    # libass font size at 1080p (font line height in px)
    color: str                     # "#RRGGBB"
    baseline: float                # where the line's glyph bottom (baseline) sits, fraction of height
    offset: float                  # px at 1080p from the glyph bottom down to the libass \an2 anchor
    upper: bool = False            # English in capitals
    spacing: float = 0.0           # letter spacing, px at 1080p (\fsp)
    advance: float | None = None   # mono fonts: advance per character in em (for exact wrapping)
    max_width: float = 0.86        # wrap beyond this fraction of the frame width


CJK_SERIF = "Noto Serif CJK SC"
MONO = "Noto Sans Mono"
SERIF = "Noto Serif"

LAYOUTS: dict[str, tuple[LineStyle, ...]] = {
    # measured with libass at 1080p: Noto Serif CJK SC at 60 -> 39 px glyphs, bottom 9 px above the anchor;
    # Noto Sans Mono at 30 -> 17 px capitals, 7 px above; Noto Serif at 46 -> about 25 px capitals
    "zh-first": (LineStyle("zh", CJK_SERIF, 60, "#E8E8E6", 0.870, 9),
                 LineStyle("en", MONO, 30, "#9CA3A3", 0.925, 7, upper=True, spacing=4.0, advance=0.6)),
    "en-first": (LineStyle("en", SERIF, 46, "#E8E8E6", 0.872, 12),
                 LineStyle("zh", CJK_SERIF, 42, "#9CA3A3", 0.932, 6)),
    "zh": (LineStyle("zh", CJK_SERIF, 60, "#E8E8E6", 0.900, 9),),
    "en": (LineStyle("en", SERIF, 46, "#E8E8E6", 0.900, 12),),
}


def layout(name: str) -> tuple[LineStyle, ...]:
    if name not in LAYOUTS:
        raise ValueError(f"unknown caption layout {name!r} (use one of {', '.join(LAYOUTS)})")
    return LAYOUTS[name]


@lru_cache(maxsize=32)
def _font_file(family: str) -> str | None:
    try:
        r = subprocess.run(["fc-match", "-f", "%{file}", family], capture_output=True, text=True, timeout=10)
        return r.stdout.strip() or None
    except Exception:
        return None


@lru_cache(maxsize=64)
def _pil_font(family: str, size: float):
    """A PIL font whose line height (ascent + descent) is `size`, as libass sizes fonts."""
    try:
        from PIL import ImageFont
    except ImportError:
        return None
    f = _font_file(family)
    if not f:
        return None
    try:
        probe = ImageFont.truetype(f, 100)
        a, d = probe.getmetrics()
        return ImageFont.truetype(f, max(1, int(round(100 * size / max(1, a + d)))))
    except Exception:
        return None


def text_width(s: str, st: LineStyle, scale: float = 1.0) -> float:
    """Rendered width in px (at the frame's scale) of one line in style `st`."""
    size = st.size * scale
    n = max(0, len(s) - 1)
    if st.advance is not None and not _CJK.search(s):
        em = size / 1.36                      # Noto Sans Mono: line height 1.36 em
        return len(s) * st.advance * em + n * st.spacing * scale
    font = _pil_font(st.font, round(size, 1))
    if font is not None:
        try:
            return float(font.getlength(s)) + n * st.spacing * scale
        except Exception:
            pass
    em = size / 1.4
    return sum(em if _CJK.match(ch) else 0.55 * em for ch in s) + n * st.spacing * scale


def wrap_line(s: str, st: LineStyle, width: int, scale: float) -> list[str]:
    """Break a caption line that is wider than the style allows: Chinese with the subtitle tool's
    balanced cuts (explainer.subtitles.split_balanced), English at balanced word gaps."""
    if not s:
        return []
    limit = st.max_width * width
    if "\n" in s:
        return [x.strip() for x in s.split("\n") if x.strip()]
    if text_width(s, st, scale) <= limit:
        return [s]
    from . import subtitles as subs
    for k in (2, 3):
        if st.lang == "zh" or _CJK.search(s):
            pieces = subs.split_balanced(s, subs.units(s) / k + 0.5)
        else:
            pieces = _balanced_words(s, k)
        if all(text_width(p, st, scale) <= limit for p in pieces):
            return pieces
    return pieces


def _balanced_words(s: str, k: int) -> list[str]:
    words = s.split()
    if len(words) < k:
        return [s]
    best, best_cost = [s], None
    from itertools import combinations
    for cuts in combinations(range(1, len(words)), k - 1):
        parts = [" ".join(words[a:b]) for a, b in zip((0,) + cuts, cuts + (len(words),))]
        lens = [len(p) for p in parts]
        cost = max(lens) - min(lens)
        if best_cost is None or cost < best_cost:
            best, best_cost = parts, cost
    return best


# ---------------------------------------------------------------- writers

def _ass_color(hex_rgb: str, alpha: int = 0) -> str:
    """'#RRGGBB' -> ASS '&HAABBGGRR' (alpha 0 = opaque)."""
    h = hex_rgb.lstrip("#")
    r, g, b = h[0:2], h[2:4], h[4:6]
    return f"&H{alpha:02X}{b}{g}{r}".upper()


def _ass_time(t: float) -> str:
    cs = int(round(max(0.0, t) * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h:d}:{m:02d}:{s:02d}.{cs:02d}"


def _ass_escape(s: str) -> str:
    return s.replace("\\", "\\\\").replace("{", "(").replace("}", ")")


def line_text(c: Caption, st: LineStyle) -> str:
    s = c.zh if st.lang == "zh" else c.en
    return s.upper() if st.upper else s


def write_ass(path: Path, cues: list[Caption], layout_name: str = "zh-first", width: int = 1920,
              height: int = 1080, title: str = "") -> None:
    """Captions over the full picture (no band): one event per line, bottom-anchored, so the second
    line never moves when the first wraps."""
    styles = layout(layout_name)
    k = height / 1080.0
    head = f"""[Script Info]
Title: {title}
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
"""
    for i, st in enumerate(styles):
        head += (f"Style: L{i},{st.font},{st.size * k:.1f},{_ass_color(st.color)},{_ass_color(st.color)},"
                 f"&H96000000,&H00000000,0,0,0,0,100,100,{st.spacing * k:.2f},0,1,{1.2 * k:.2f},0,2,0,0,0,1\n")
    ev = []
    fade = int(FADE * 1000)
    for c in cues:
        a, b = c.t or 0.0, c.end
        if b - a < 0.05:
            continue
        lines = [wrap_line(line_text(c, st), st, width, k) for st in styles]
        lift = 0.0                          # a wrapped lower line pushes the upper one up
        for i in reversed(range(len(styles))):
            st, ls = styles[i], lines[i]
            if not ls:
                continue
            y = st.baseline * height + st.offset * k - lift
            body = "\\N".join(_ass_escape(x) for x in ls)
            ev.append(f"Dialogue: {i},{_ass_time(a)},{_ass_time(b)},L{i},,0,0,0,,"
                      f"{{\\an2\\pos({width / 2:.0f},{y:.0f})\\fad({fade},{fade})}}{body}")
            lift += (len(ls) - 1) * st.size * k * 1.04
    Path(path).write_text(head + "\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, "
                          "MarginV, Effect, Text\n" + "\n".join(ev) + "\n", encoding="utf-8")


def write_srt(path: Path, cues: list[Caption], langs: tuple[str, ...] = ("zh", "en")) -> None:
    from .subtitles import write_srt as _srt
    rows = []
    for c in cues:
        texts = [c.zh if lg == "zh" else c.en for lg in langs]
        if any(texts):
            rows.append((c.t or 0.0, c.end, *[x for x in texts if x]))
    _srt(Path(path), rows)


def burn(src: Path, ass: Path, dst: Path, crf: int = 18, audio: bool = True) -> None:
    """Draw the captions into the picture itself (no band, no scaling). Re-encodes the video."""
    vf = f"ass='{str(ass).replace(chr(39), '')}'"
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", str(src), "-vf", vf, "-c:v", "libx264", "-preset", "medium",
           "-crf", str(crf), "-pix_fmt", "yuv420p"]
    cmd += ["-c:a", "copy"] if audio else ["-an"]
    subprocess.run(cmd + ["-movflags", "+faststart", str(dst)], check=True)


def tidy(cues: list[Caption], gap: float = 0.1) -> tuple[list[Caption], list[str]]:
    """Sort by start; a caption that runs into the next one ends `gap` before it. Returns warnings."""
    cues = sorted((c for c in cues if c.t is not None), key=lambda c: c.t)
    warn = []
    for a, b in zip(cues, cues[1:]):
        if a.end > b.t - gap:
            new = max(0.5, b.t - gap - a.t)
            warn.append(f"caption {a.id or a.zh[:12]!r} at {a.t:.2f}s runs into the next one: "
                        f"{a.dur:.2f}s -> {new:.2f}s")
            a.dur = new
    return cues, warn


@dataclass
class Track:
    """All captions of a stitched video, in video time."""
    cues: list[Caption] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def picture_only_share(self, total: float) -> float:
        covered, last = 0.0, 0.0
        for c in sorted(self.cues, key=lambda c: c.t):
            a, b = max(c.t, last), c.end
            if b > a:
                covered += b - a
                last = b
        return 1.0 - covered / total if total > 0 else 1.0
