"""Language versions of a video: translated narration, on-screen text and metadata.

    EXPLAINER_LANG=en   (default) the original video, untouched
    EXPLAINER_LANG=zh   the Chinese version

A language version lives next to the video, in videos/<id>/i18n/<lang>/:

    narration.yaml   (and/or narration/*.yaml fragments, merged; same for strings)
                     every SAY line of script.md, translated SENTENCE BY SENTENCE:
                       S03:
                       - en: "Here's the catch. Real tic-tac-toe stops as soon as ..."
                         zh: ["关键在这里。", "真正的井字棋，只要有人连成三个就结束了……"]
                         say: [null, "真正的井字棋，只要有人连成三个就结束了……"]  # optional spoken form
                         anchors: {"Real tic-tac-toe stops": "真正的井字棋"}        # optional
                         en_display: [null, "Real tic-tac-toe stops ... 3 in a row."]  # optional English
                                     # subtitle line per sentence (digits/symbols instead of words)
                     `en` must equal the SAY line (so a changed script is detected), and `zh` must have
                     exactly one entry per English sentence (explainer.voice.split_sentences). That
                     alignment is what lets every scene keep its English anchors: vo.wait_until("Second,
                     X fills") is mapped to the same place in the matching Chinese sentence, and it is
                     what pairs the Chinese and English lines of the bilingual subtitles.
    strings.yaml     on-screen text: {"English string": "中文"}; keys starting with "re:" are regular
                     expressions (Python re, full match) whose value may use \\1, \\2 ...; keys
                     "<scene file stem>|<English>" apply only to strings created by that scene file
                     (e.g. "s04_definition|H": "正" translates one coin label, not every "H").
                     Keys of t2c / t2w / t2s / t2f / t2g, tex_to_color_map and
                     substrings_to_isolate are translated through the same table, so colours survive.
    meta.yaml        title, description, chapter titles ({scene file stem or class: title}), part titles
    assets/          localized assets, e.g. assets/play_all_games.py with Chinese comments
                     (see `localized()`).

Toolkit strings (e.g. the "Pause and ponder" card) are translated by explainer/locales/<lang>.yaml.

When EXPLAINER_LANG is not "en", `install()` (called by explainer.style) wraps Manim's Text,
MarkupText, Paragraph, Tex and MathTex so every on-screen string is looked up in those tables
(Code keeps the code and translates only `# comment` texts),
CJK text gets a matching CJK font (Noto Serif/Sans/Mono CJK SC), and TeX with CJK characters is
typeset with XeLaTeX + ctex. Untranslated strings that contain English words are collected in
build/i18n/missing.<lang>.json for review.
"""

from __future__ import annotations

import atexit
import json
import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

TOOLKIT_DIR = Path(__file__).resolve().parent

# CJK fonts that pair with the house fonts (installed by setup/install.sh: fonts-noto-cjk)
CJK_FONTS = {"serif": "Noto Serif CJK SC", "sans": "Noto Sans CJK SC", "mono": "Noto Sans Mono CJK SC"}

_CJK = re.compile(r"[　-〿㐀-䶿一-鿿豈-﫿＀-￯]")
_WORD = re.compile(r"[A-Za-z]{2,}")


def lang() -> str:
    return (os.environ.get("EXPLAINER_LANG") or "en").strip().lower()


def active() -> bool:
    return lang() != "en"


def has_cjk(s: str) -> bool:
    return bool(_CJK.search(s or ""))


@lru_cache(maxsize=1)
def project_dir() -> Path | None:
    """The video project being rendered: EXPLAINER_PROJECT, else the nearest folder with video.yaml
    above the working directory (build, preview and check all run scenes from the project folder)."""
    env = os.environ.get("EXPLAINER_PROJECT")
    if env:
        return Path(env).resolve()
    for p in [Path.cwd(), *Path.cwd().parents]:
        if (p / "video.yaml").exists():
            return p
    return None


def lang_dir(code: str | None = None, project: Path | None = None) -> Path | None:
    project = project or project_dir()
    return project / "i18n" / (code or lang()) if project else None


def _yaml(path: Path):
    import yaml

    return (yaml.safe_load(path.read_text(encoding="utf-8")) or {}) if path.exists() else {}


def norm(s: str) -> str:
    """Whitespace-normalized key (VoiceScene and load_narration normalize SAY lines the same way)."""
    return " ".join(str(s).split())


# ---------------------------------------------------------------- narration

@dataclass
class Line:
    """One SAY line in another language, sentence-aligned to the English."""
    en: str
    sentences: list[str]                      # display text, one per English sentence
    spoken: list[str]                         # what the TTS reads (defaults to the display text)
    anchors: dict[str, str] = field(default_factory=dict)
    en_display: list[str | None] = field(default_factory=list)   # English subtitle line overrides


def _merged(d: Path | None, name: str) -> dict:
    """<name>.yaml plus every <name>/*.yaml (fragments written by different translators)."""
    if d is None:
        return {}
    data: dict = {}
    files = ([d / f"{name}.yaml"] if (d / f"{name}.yaml").exists() else []) + sorted((d / name).glob("*.yaml"))
    for f in files:
        part = _yaml(f) or {}
        for k, v in part.items():
            if isinstance(v, list) and isinstance(data.get(k), list):
                data[k] = data[k] + v
            else:
                data[k] = v
    return data


@lru_cache(maxsize=4)
def narration(code: str | None = None, project: Path | None = None) -> dict[str, Line]:
    d = lang_dir(code, project)
    data = _merged(d, "narration")
    out: dict[str, Line] = {}
    for scene_id, items in (data or {}).items():
        for it in items or []:
            sents = [norm(s) for s in (it.get(code or lang()) or it.get("tr") or [])]
            say = it.get("say") or [None] * len(sents)
            spoken = [norm(sp) if sp else s for s, sp in zip(sents, list(say) + [None] * len(sents))]
            en_disp = [norm(x) if x else None for x in (it.get("en_display") or [])]
            out[norm(it["en"])] = Line(norm(it["en"]), sents, spoken, dict(it.get("anchors") or {}),
                                       en_disp)
    return out


def line_for(text_en: str) -> Line | None:
    return narration().get(norm(text_en))


def check_narration(project: Path, code: str) -> list[str]:
    """Problems with a translated narration file: missing / stale lines, sentence-count mismatches,
    anchors that point nowhere."""
    from .script import load_narration
    from .voice import split_sentences

    problems = []
    narration.cache_clear()
    tr = narration(code, project)
    say = load_narration(project / "script.md")
    wanted = {norm(t): sid for sid, lines in say.items() for t in lines}
    for key, sid in wanted.items():
        line = tr.get(key)
        if line is None:
            problems.append(f"{sid}: no {code} translation for: {key[:90]}")
            continue
        n_en = len(split_sentences(key))
        if len(line.sentences) != n_en:
            problems.append(f"{sid}: {n_en} English sentences but {len(line.sentences)} {code} sentences: {key[:70]}")
        if any(not s.strip() for s in line.sentences):
            problems.append(f"{sid}: empty {code} sentence in: {key[:70]}")
        for a_en, a_tr in line.anchors.items():
            if a_en not in key:
                problems.append(f"{sid}: anchor {a_en!r} is not in the English line")
            if not any(a_tr in s for s in line.sentences):
                problems.append(f"{sid}: anchor target {a_tr!r} is not in the {code} line")
    for key in tr:
        if key not in wanted:
            problems.append(f"stale {code} line (no such SAY line in script.md): {key[:90]}")
    allowed = allowed_latin(project, code)
    for key, line in tr.items():
        sid = wanted.get(key, "?")
        for i, (disp, spoken) in enumerate(zip(line.sentences, line.spoken)):
            for msg in spoken_problems(spoken, allowed):
                problems.append(f"{sid}: sentence {i + 1}: {msg}: {spoken[:60]}")
            if not re.search(r"[。！？…]$|[。！？…][”」）)]$", disp):
                problems.append(f"{sid}: sentence {i + 1} must end with 。！？: {disp[-30:]}")
            if re.search(r"[。！？](?!$)(?![”」）)]$)", disp):
                problems.append(f"{sid}: sentence {i + 1} has 。！？ inside (one sentence per English sentence): {disp[:60]}")
    return problems


# what the voice reads badly (rules measured with the zh voice, see the videos' GLOSSARY.md)
_SPOKEN_BAD = [
    (re.compile(r"[（）()《》\[\]{}]"), "brackets are read aloud or break the voice"),
    (re.compile(r"[εδλσαΔ′√≤≥≈×÷^=<>→←+]|!=|==|\+="), "maths symbol in spoken text (write it in words)"),
    (re.compile(r"\d\s*!"), "n! is misread (say: n 的阶乘)"),
    (re.compile(r"[A-Za-z]+_[A-Za-z_]+"), "identifier with underscore is read as 下划线"),
    (re.compile(r"种[。，！？]"), "a clause ending in 种 is misheard (多少种。 -> 多少重)"),
]


def spoken_problems(spoken: str, allowed: set[str] | None = None) -> list[str]:
    out = [msg for rx, msg in _SPOKEN_BAD if rx.search(spoken)]
    if allowed is not None:
        for w in re.findall(r"[A-Za-z][A-Za-z'.-]*", spoken):
            if w not in allowed and w.lower() not in allowed and len(w) > 1:
                out.append(f"English word {w!r} is not in the glossary's spoken forms")
    if re.search(r"[\u4e00-\u9fff][A-Za-z0-9]|[A-Za-z0-9][\u4e00-\u9fff]", spoken):
        out.append("missing half-width space between Chinese and Latin/digits (the lexicon needs it)")
    return out


def allowed_latin(project: Path, code: str) -> set[str]:
    """Latin words a translation may speak: every Latin word in the glossary's spoken and subtitle
    forms (code names, people, kept-English terms), plus single letters and symbols' names."""
    d = project / "i18n" / code
    g = _yaml(d / "glossary.yaml") if (d / "glossary.yaml").exists() else {}
    words: set[str] = set()
    for t in g.get("terms") or []:
        for f in ("zh_spoken", "zh_subtitle", "first_use"):
            for w in re.findall(r"[A-Za-z][A-Za-z'.-]*", str(t.get(f) or "")):
                words.add(w)
                words.add(w.lower())
    for w in (g.get("allowed_spoken_latin") or []):
        words.add(str(w))
        words.add(str(w).lower())
    return words


# ---------------------------------------------------------------- on-screen strings

@lru_cache(maxsize=4)
def _tables(code: str):
    exact: dict[str, str] = {}
    scoped: dict[tuple[str, str], str] = {}
    patterns: list[tuple[re.Pattern, str]] = []
    tables = [_yaml(TOOLKIT_DIR / "locales" / f"{code}.yaml")]
    d = lang_dir(code)
    if d:
        tables.append(_merged(d, "strings"))
    for table in tables:                       # the video's own table wins over the toolkit's
        for k, v in (table or {}).items():
            if v is None:
                continue
            k = str(k)
            if k.startswith("re:"):
                patterns.insert(0, (re.compile(k[3:], re.S), str(v)))
            elif "|" in k and re.fullmatch(r"[A-Za-z0-9_]+", k.split("|", 1)[0]):
                stem, text = k.split("|", 1)
                scoped[(stem, text)] = str(v)
            else:
                exact[k] = str(v)
                exact.setdefault(norm(k), str(v))
    return exact, scoped, patterns


def _caller_stem() -> str | None:
    """File stem of the scene (or helper) module that is creating the current text object."""
    import inspect

    project = project_dir()
    frame = inspect.currentframe()
    while frame is not None:
        f = Path(frame.f_code.co_filename)
        if f.suffix == ".py" and project is not None and project in f.resolve().parents:
            return f.stem
        frame = frame.f_back
    return None


_MISSING: dict[str, set] = {}


def tr(s: str, kind: str = "text") -> str:
    """Translate one on-screen string into the active language (unchanged if no entry)."""
    if not active() or not isinstance(s, str) or not s.strip():
        return s
    exact, scoped, patterns = _tables(lang())
    if scoped:
        stem = _caller_stem()
        if stem and (stem, s) in scoped:
            return scoped[(stem, s)]
    if s in exact:
        return exact[s]
    if norm(s) in exact:
        return exact[norm(s)]
    for rx, repl in patterns:
        m = rx.fullmatch(s)
        if m:
            return m.expand(repl)
    if _WORD.search(re.sub(r"\\[A-Za-z]+", "", s)):      # English words left in a visible string
        _MISSING.setdefault(kind, set()).add(s)
    return s


def localized(path: str | Path) -> Path:
    """`assets/x.py` -> `i18n/<lang>/assets/x.py` when that file exists, else the original path."""
    path = Path(path)
    project = project_dir()
    if not active() or project is None:
        return path
    try:
        rel = path.resolve().relative_to(project)
    except ValueError:
        return path
    alt = lang_dir() / rel
    return alt if alt.exists() else path


def meta(code: str | None = None, project: Path | None = None) -> dict:
    d = lang_dir(code, project)
    return _yaml(d / "meta.yaml") if d else {}


@atexit.register
def _dump_missing():
    if not _MISSING or project_dir() is None:
        return
    out = project_dir() / "build" / "i18n" / f"missing.{lang()}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        old = json.loads(out.read_text()) if out.exists() else {}
    except json.JSONDecodeError:
        old = {}
    for kind, items in _MISSING.items():
        old[kind] = sorted(set(old.get(kind, [])) | items)
    out.write_text(json.dumps(old, ensure_ascii=False, indent=1))


# ---------------------------------------------------------------- Manim hooks

def _cjk_font(font: str | None) -> str:
    f = (font or "").lower()
    kind = "mono" if "mono" in f else "sans" if "sans" in f else "serif"
    base = font or ""
    return f"{base}, {CJK_FONTS[kind]}" if base else CJK_FONTS[kind]


@lru_cache(maxsize=1)
def cjk_tex_template():
    """XeLaTeX + ctex, with the same maths packages as the house template."""
    from manim import TexTemplate

    t = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
    t.add_to_preamble(r"\usepackage{amsmath,amssymb,bm}")
    t.add_to_preamble(r"\usepackage[UTF8,scheme=plain]{ctex}")
    t.add_to_preamble(rf"\setCJKmainfont{{{CJK_FONTS['serif']}}}")
    t.add_to_preamble(rf"\setCJKsansfont{{{CJK_FONTS['sans']}}}")
    return t


_INSTALLED = False


def install() -> None:
    """Route every Manim text object through `tr()` (no-op for English)."""
    global _INSTALLED
    if _INSTALLED or not active():
        return
    _INSTALLED = True
    from manim import MarkupText, MathTex, Paragraph, Tex, Text

    def tr_keys(kw, names, kind):
        for name in names:
            m = kw.get(name)
            if isinstance(m, dict):
                kw[name] = {tr(k, kind) if isinstance(k, str) else k: v for k, v in m.items()}
            elif isinstance(m, (list, tuple)):
                kw[name] = type(m)(tr(k, kind) if isinstance(k, str) else k for k in m)

    def wrap_text(cls, kind):
        orig = cls.__init__

        def init(self, text, *a, **kw):
            text = tr(text, kind)
            tr_keys(kw, ("t2c", "t2w", "t2s", "t2f", "t2g"), kind)
            if has_cjk(text):
                kw["font"] = _cjk_font(kw.get("font"))
                quotes = [q for q in "“”‘’" if q in text]
                if quotes and kind == "text":   # the Latin font comes first and has narrow quotes
                    cjk = CJK_FONTS["sans" if "sans" in kw["font"].lower() else "serif"]
                    kw["t2f"] = {**{q: cjk for q in quotes}, **(kw.get("t2f") or {})}
                if kw.get("t2c") and kind == "text":
                    # Pango lays out every t2c run on its own; in CJK text a run of only Latin
                    # letters/digits (the X of "X 赢了！") then sits ~0.05-0.08 units above the
                    # line. Lay the text out in one piece and copy the run colours glyph by glyph.
                    ref = type(self).__new__(type(self))
                    orig(ref, text, *a, **kw)
                    plain = {k: v for k, v in kw.items() if k != "t2c"}
                    orig(self, text, *a, **plain)
                    if len(ref) == len(self):
                        for g, r in zip(self, ref):
                            g.set_color(r.get_color())
                        return
                    orig(self, text, *a, **kw)        # glyph counts differ: keep Pango's colours
                    return
            orig(self, text, *a, **kw)
        cls.__init__ = init

    wrap_text(Text, "text")
    wrap_text(MarkupText, "markup")

    orig_par = Paragraph.__init__

    def par_init(self, *lines, **kw):
        lines = tuple(tr(s, "paragraph") for s in lines)
        if any(has_cjk(s) for s in lines):
            kw["font"] = _cjk_font(kw.get("font"))
        orig_par(self, *lines, **kw)
    Paragraph.__init__ = par_init

    def wrap_tex(cls, kind):
        orig = cls.__init__

        def init(self, *strings, **kw):
            strings = tuple(tr(s, kind) if isinstance(s, str) else s for s in strings)
            tr_keys(kw, ("tex_to_color_map", "substrings_to_isolate"), kind)
            if any(isinstance(s, str) and has_cjk(s) for s in strings):
                kw["tex_template"] = cjk_tex_template()
            orig(self, *strings, **kw)
        cls.__init__ = init

    wrap_tex(MathTex, "mathtex")
    wrap_tex(Tex, "tex")

    from manim import Code

    orig_code = Code.__init__
    comment = re.compile(r"(#\s*)(.*?)(\s*)$")

    def code_init(self, *a, **kw):
        """Code stays code; only `# comments` are translated (key: the comment text)."""
        src = kw.get("code_string")
        if isinstance(src, str):
            out = []
            for ln in src.split("\n"):
                i = ln.find("#")
                if i >= 0 and ln[:i].count('"') % 2 == 0 and ln[:i].count("'") % 2 == 0:
                    m = comment.match(ln[i:])
                    if m and m.group(2):
                        ln = ln[:i] + m.group(1) + tr(m.group(2), "code-comment") + m.group(3)
                out.append(ln)
            kw["code_string"] = "\n".join(out)
        orig_code(self, *a, **kw)
        if isinstance(src, str) and has_cjk(kw["code_string"]):
            _even_code_lines(self, kw)
    Code.__init__ = code_init


def _even_code_lines(code, kw) -> None:
    """A code line whose translated comment falls back to the CJK font sits lower than the others
    (that font's taller ascent). Move each such line to where it would sit with Latin glyphs only,
    so the panel keeps the English line pitch."""
    from manim import UP, Code, Paragraph

    lines = code._code_html.get_text().removesuffix("\n").split("\n")
    rows = [k for k, t in enumerate(lines) if t.strip() and k < len(code.code_lines)]
    cjk = [k for k in rows if has_cjk(lines[k])]
    plain = [k for k in rows if k not in cjk]
    if not cjk or not plain:
        return
    cfg = {**Code.default_paragraph_config, **(kw.get("paragraph_config") or {})}
    font = cfg.pop("font", None) or "Monospace"
    ref = Paragraph(*[lines[k].strip()[0] for k in rows], font=font, **cfg)
    yr = {k: ref[i][0].get_bottom()[1] for i, k in enumerate(rows)}
    yc = {k: code.code_lines[k][0].get_bottom()[1] for k in rows}
    j = plain[0]
    scale = code.code_lines[j][0].height / max(1e-6, ref[rows.index(j)][0].height)
    for k in cjk:
        code.code_lines[k].shift(UP * (yc[j] - (yr[j] - yr[k]) * scale - yc[k]))


def main(argv=None) -> int:
    """python -m explainer.i18n check videos/<id> [--lang zh]"""
    import argparse

    ap = argparse.ArgumentParser(description="check a language version of a video")
    ap.add_argument("cmd", choices=["check"])
    ap.add_argument("project", type=Path)
    ap.add_argument("--lang", default="zh")
    args = ap.parse_args(argv)
    project = args.project.resolve()
    problems = check_narration(project, args.lang)
    for p in problems:
        print("NARRATION", p)
    missing = project / "build" / "i18n" / f"missing.{args.lang}.json"
    if missing.exists():
        data = json.loads(missing.read_text())
        n = sum(len(v) for v in data.values())
        print(f"STRINGS   {n} untranslated on-screen strings with English words seen in renders ({missing})")
    print("OK" if not problems else f"{len(problems)} narration problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
