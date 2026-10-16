"""Visual vocabulary for code-and-infrastructure videos (the AC215 MLOps series and any other
tutorial walkthrough): terminals that type, code panels with their path and line numbers, file
trees, machines (laptop, server, VM, container, cloud), README step trackers and schematic
browser/console windows.

Everything is drawn from primitives in the house palette (no logos or product screenshots), and
every piece of text is at least 20 pt.

Quick map:
    text       mono() label() mono_line() cell_width()
    boxes      box() chip() tag() check_mark() cross_mark() warning_sign()
    terminal   Terminal(...) .run(scene, cmd, output) .type(scene, cmd) .print(scene, lines) .clear(scene)
    code       code_block() code_panel() code_span() line_bar()
    files      file_tree([...]) .row(name)   folder_glyph() file_glyph()
    machines   laptop() server() cloud() machine_box() layer_bar()
    follow     ReadmeTracker(section, steps) .goto(k)   step_badge()
    browser    browser_window(url) form_rows([(label, value), ...])

A Terminal keeps a fixed size and scrolls like a real one, so the frame never jumps:

    term = Terminal(prompt="conny@instance-1:~$", width=12, rows=9).to_edge(DOWN)
    self.play(FadeIn(term))
    term.run(self, "sudo apt-get update", ["Hit:1 http://deb.debian.org/debian bookworm InRelease",
                                          "Reading package lists... Done"], type_time=1.2)
    term.set_prompt("conny@instance-1:~/simple-translate$")
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np
from manim import (DL, DOWN, DR, LEFT, ORIGIN, RIGHT, UL, UP, UR, AnimationGroup, Circle, Code,
                   DashedVMobject, Dot, FadeIn, FadeOut, Line, Polygon, Rectangle,
                   RoundedRectangle, ShowIncreasingSubsets, Text, Union, VGroup, VMobject, linear)

from . import style as S

# ------------------------------------------------------------------ fonts and sizes
MONO = "DejaVu Sans Mono"      # the house code font
SANS = S.FONT_SANS
INK = S.WHITE
TERM_BG = "#090A0D"
PANEL = S.GREY_DARKER

TITLE = 48
BODY = 32
LABEL = 26
SMALL = 24
TAG = 22
CAPTION = 20                   # the toolkit minimum

# default terminal colours (a Debian-like prompt)
PROMPT_USER = S.GREEN
PROMPT_PATH = S.BLUE
OUTPUT = "#C9CDD4"             # console output: a soft white, so the typed commands stand out
COMMENT = S.GREY


# ------------------------------------------------------------------ text
def label(s: str, size: float = LABEL, color: str = INK, **kw) -> Text:
    """House-font text (CMU Serif)."""
    return S.text(s, size, color, **kw)


def mono(s: str, size: float = SMALL, color: str = INK, **kw) -> Text:
    """Monospace text for file names, commands and console output (one line)."""
    return S.text(s, size, color, font=MONO, **kw)


@lru_cache(maxsize=16)
def cell_width(size: float) -> float:
    """Width of one monospace character cell at `size`."""
    return mono("M" * 40, size).width / 40


@lru_cache(maxsize=16)
def line_pitch(size: float) -> float:
    """Distance between two baselines of monospace lines at `size`."""
    return mono("|", size).height * 1.32


def mono_line(s: str, size: float = SMALL, color: str = INK, t2c: dict | None = None) -> VGroup:
    """One line of monospace text with a FIXED vertical extent, whatever its glyphs (a line of
    dots and a line of 'Hgy|' sit on the same baseline when their tops are aligned).

    Built as Text("|" + s) and the pipe dropped after layout, so every line spans the pipe's full
    ascent and descent. `t2c` maps substrings or "[a:b]" slices of `s` to colours.
    Returns a VGroup of the glyphs, with .text (the string) and .strut (an invisible rectangle of
    the line's full height, used for alignment)."""
    s = s if s else " "
    shifted = None
    if t2c:
        shifted = {}
        for k, v in t2c.items():
            if k.startswith("[") and k.endswith("]") and ":" in k:
                a, b = k[1:-1].split(":")
                a = int(a) + 1 if a else 1
                b = int(b) + 1 if b else len(s) + 1
                shifted[f"[{a}:{b}]"] = v
            else:
                shifted[k] = v
    t = S.text("|" + s, size, color, font=MONO, t2c=shifted or {})
    pipe = t.submobjects[0]
    strut = Rectangle(width=max(0.01, t.width), height=pipe.height, stroke_width=0, fill_opacity=0)
    strut.move_to(pipe.get_center()).align_to(t, LEFT)
    glyphs = VGroup(*t.submobjects[1:])
    g = VGroup(strut, *glyphs.submobjects)
    g.shift(LEFT * cell_width(size))            # the pipe's cell is gone
    g.text, g.strut, g.glyphs = s, strut, VGroup(*glyphs.submobjects)
    g.pt = size
    return g


def glyph_range(line: VGroup, start: int, end: int | None = None) -> VGroup:
    """The glyphs for characters s[start:end] of a mono_line (spaces have no glyphs)."""
    s = line.text
    end = len(s) if end is None else end
    a = len("".join(s[:start].split()))
    n = len("".join(s[start:end].split()))
    return VGroup(*line.glyphs.submobjects[a:a + n])


def substring(line: VGroup, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of substring `sub` in a mono_line (to colour, circle or underline it)."""
    i = -1
    for _ in range(occurrence + 1):
        i = line.text.find(sub, i + 1)
    if i < 0:
        raise ValueError(f"{sub!r} not in {line.text!r}")
    return glyph_range(line, i, i + len(sub))


# ------------------------------------------------------------------ boxes, chips, marks
def box(width: float, height: float, color: str = S.GREY, fill: str | None = None,
        fill_opacity: float = 0.12, stroke: float = 2.5, radius: float = 0.14,
        dashed: bool = False) -> VMobject:
    """A rounded box: stroke in `color`, a faint fill of the same colour (or `fill`)."""
    r = RoundedRectangle(width=width, height=height, corner_radius=min(radius, height / 2, width / 2),
                         stroke_color=color, stroke_width=stroke)
    if dashed:
        r.set_fill(S.BG, 0)
        d = DashedVMobject(r, num_dashes=max(12, int((width + height) * 7)), dashed_ratio=0.55)
        d.set_stroke(color, stroke)
        return d
    r.set_fill(fill or color, fill_opacity)
    return r


def chip(s: str, color: str = S.GREY, size: float = SMALL, text_color: str = INK,
         font: str | None = None, pad_x: float = 0.24, pad_y: float = 0.12,
         fill_opacity: float = 0.16) -> VGroup:
    """A thing named in a word or two: border in its colour, faint tint, WHITE text.
    font=MONO for package names and commands. .box .text"""
    t = mono(s, size, text_color) if font == MONO else label(s, size, text_color)
    h = mono("|", size).height + 2 * pad_y
    b = box(t.width + 2 * pad_x, h, color, fill_opacity=fill_opacity, radius=h / 2.6)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def tag(s: str, color: str = S.GREY, size: float = TAG, text_color: str | None = None) -> VGroup:
    """A small tag ON something: text in the tag's colour, opaque dark fill. .box .text"""
    t = label(s, size, text_color or color)
    h = mono("|", size).height + 0.16
    b = RoundedRectangle(width=t.width + 0.4, height=h, corner_radius=h / 2,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def lecture_ref(lecture: int | str, slides: str, color: str = S.GREY) -> VGroup:
    """'Lecture 2 · slides 10–18': where the idea on screen is in the instructor's lecture slides
    (docs/AC215_SERIES.md, rule 9). A tag pinned top right inside the safe frame, opposite the
    README tracker; the slides themselves are never shown. .box .text"""
    g = tag(f"Lecture {int(lecture)} · slides {slides}", color)
    return g.move_to([6.6 - g.width / 2, 3.6 - g.height / 2, 0])


def check_mark(height: float = 0.3, color: str = S.GREEN, stroke: float = 5) -> VMobject:
    h = height
    m = VMobject(stroke_color=color, stroke_width=stroke)
    m.set_points_as_corners([[-0.5 * h, 0.05 * h, 0], [-0.15 * h, -0.4 * h, 0], [0.55 * h, 0.45 * h, 0]])
    return m


def cross_mark(height: float = 0.3, color: str = S.RED, stroke: float = 5) -> VGroup:
    h = height / 2
    return VGroup(Line([-h, -h, 0], [h, h, 0]), Line([-h, h, 0], [h, -h, 0])).set_stroke(color, stroke)


def warning_sign(height: float = 0.5, color: str = S.YELLOW) -> VGroup:
    """A warning triangle with an exclamation mark."""
    tri = Polygon([0, height * 0.5, 0], [-height * 0.58, -height * 0.5, 0], [height * 0.58, -height * 0.5, 0],
                  stroke_color=color, stroke_width=4).set_fill(color, 0.15)
    bar = Line([0, height * 0.22, 0], [0, -height * 0.12, 0], color=color, stroke_width=5)
    dot = Dot([0, -height * 0.3, 0], radius=height * 0.05, color=color)
    return VGroup(tri, bar, dot)


# ------------------------------------------------------------------ terminal
class Terminal(VGroup):
    """A terminal window of fixed size that types commands, prints output and scrolls.

    Terminal(prompt="conny@instance-1:~$", width=12.0, rows=9, size=22, title="ssh · instance-1")
      .run(scene, cmd, output=None, type_time=None, out_time=0.5)   type a command, then print
      .type(scene, cmd, type_time=None, wrap=True)                  type a command at the prompt;
                                                                    a long one folds with " \\"
      .find(substring)                                              the latest line containing it
      .print(scene, lines, color=OUTPUT, run_time=0.5)              print output lines
      .set_prompt(prompt)                                           e.g. after `cd`
      .clear(scene)                                                 like `clear`
      .last(n=1)                                                    the last n line mobjects
    The prompt is coloured like Debian's: user@host GREEN, path BLUE; a leading "(venv) " is
    GREEN too. A line of output can be a string, or (string, colour). Long output lines are cut
    with '…' unless .print/.run get wrap=True (then they fold at the edge, like a real terminal).
    """

    def __init__(self, prompt: str = "$", width: float = 12.0, rows: int = 9, size: float = 22,
                 title: str | None = None, **kw):
        super().__init__(**kw)
        self.prompt, self.size, self.rows = prompt, size, rows
        self.pitch = line_pitch(size)
        bar_h = 0.4
        h = rows * self.pitch + 0.45 + bar_h
        self.box = RoundedRectangle(width=width, height=h, corner_radius=0.14,
                                    stroke_color=S.GREY_DARK, stroke_width=2).set_fill(TERM_BG, 1)
        self.bar = Line(self.box.get_corner(UL) + DOWN * bar_h, self.box.get_corner(UR) + DOWN * bar_h,
                        color=S.GREY_DARK, stroke_width=2)
        dots = VGroup(*[Dot(radius=0.055, color=S.GREY_DARK) for _ in range(3)]).arrange(RIGHT, buff=0.1)
        dots.move_to(self.box.get_corner(UL) + np.array([0.35, -bar_h / 2, 0]))
        self.dots = dots
        self.add(self.box, self.bar, dots)
        if title:
            self.title = mono(title, CAPTION, S.GREY).move_to(self.box.get_top() + DOWN * bar_h / 2)
            self.add(self.title)
        else:
            self.title = None
        self.bar_h = bar_h
        self.max_chars = int((width - 0.6) / cell_width(size))
        self.lines = VGroup()
        self.add(self.lines)

    # -- geometry
    def _slot(self, i: int) -> np.ndarray:
        """Top-left point of text row i (0 = first row under the title bar)."""
        return self.box.get_corner(UL) + np.array([0.3, -self.bar_h - 0.22 - i * self.pitch, 0])

    def _place(self, line: VGroup, i: int) -> VGroup:
        line.shift(self._slot(i) - line.strut.get_corner(UL))
        return line

    def _cut(self, s: str) -> str:
        return s if len(s) <= self.max_chars else s[: self.max_chars - 1] + "…"

    def _prompt_colors(self, prompt: str) -> dict:
        colors, start = {}, 0
        if prompt.startswith("(") and ") " in prompt:          # an active venv: "(app) user@host:..."
            start = prompt.index(") ") + 2
            colors[f"[0:{start - 1}]"] = S.GREEN
        if "@" in prompt and ":" in prompt[start:]:
            a = prompt.index(":", start)
            b = len(prompt.rstrip("$# ").rstrip())
            colors.update({f"[{start}:{a}]": PROMPT_USER, f"[{a + 1}:{b}]": PROMPT_PATH})
        return colors

    def set_prompt(self, prompt: str) -> "Terminal":
        self.prompt = prompt
        return self

    def last(self, n: int = 1) -> VGroup:
        return VGroup(*self.lines.submobjects[-n:])

    # -- scrolling
    def _make_room(self, scene, n_new: int, run_time: float = 0.35) -> None:
        overflow = len(self.lines) + n_new - self.rows
        if overflow <= 0:
            return
        gone = VGroup(*self.lines.submobjects[:overflow])
        stay = VGroup(*self.lines.submobjects[overflow:])
        anims = [FadeOut(gone, shift=UP * self.pitch * overflow)]
        if len(stay):
            anims.append(stay.animate.shift(UP * self.pitch * overflow))
        scene.play(*anims, run_time=run_time)
        for m in gone:
            self.lines.remove(m)

    # -- actions
    def fold(self, text: str, first_prefix: int = 0) -> list[str]:
        """Split a typed command line (prompt included) into rows of at most `max_chars`.
        Breaks only at a space outside quotes, ends every row but the last with " \\" and
        indents the next one by 4 spaces, so the rows paste back as one valid shell command.
        A single token longer than a row is broken where it must (never inside the prompt)."""
        limit = self.max_chars
        if len(text) <= limit:
            return [text]
        rows, cur, indent = [], text, ""
        while len(cur) > limit:
            room = limit - 2                     # keep space for " \"
            breaks, quote = [], None
            for i, ch in enumerate(cur):
                if quote:
                    quote = None if ch == quote else quote
                elif ch in "\"'":
                    quote = ch
                elif ch == " " and i > max(first_prefix if not rows else len(indent), len(indent)):
                    breaks.append(i)
            ok = [b for b in breaks if b <= room]
            # prefer to break before an option ("-x" / "--xx"), so an option keeps its value
            opt = [b for b in ok if b + 1 < len(cur) and cur[b + 1] == "-"]
            lo = len(indent) + (room - len(indent)) * 0.5
            if opt and opt[-1] >= lo:
                ok = opt
            cut = ok[-1] if ok else (breaks[0] if breaks and breaks[0] < len(cur) - 1 else room)
            if cut > room:                        # no space early enough: hard break
                cut = room
                rows.append(cur[:cut] + " \\")
                cur = "    " + cur[cut:]
            else:
                rows.append(cur[:cut] + " \\")
                cur = "    " + cur[cut + 1:]
            indent = "    "
        rows.append(cur)
        return rows

    def type(self, scene, cmd: str, type_time: float | None = None, color: str = INK,
             wrap: bool = True) -> VGroup:
        """Show the prompt and type `cmd` after it. A command longer than a row folds onto
        continuation rows (see fold; wrap=False cuts it with '…' instead). Returns the line, or
        a VGroup of the rows when it folded (.rows)."""
        p = self.prompt + (" " if self.prompt and not self.prompt.endswith(" ") else "")
        t2c = self._prompt_colors(self.prompt)
        texts = self.fold(p + cmd, first_prefix=len(p)) if wrap else [self._cut(p + cmd)]
        self._make_room(scene, len(texts))
        rows = []
        for k, t in enumerate(texts):
            ln = mono_line(t, self.size, color, t2c=t2c if k == 0 else None)
            self._place(ln, len(self.lines))
            self.lines.add(ln)
            rows.append(ln)
        prompt_glyphs = glyph_range(rows[0], 0, len(p))
        typed = [glyph_range(rows[0], len(p))] + [glyph_range(r, 0) for r in rows[1:]]
        cmd_glyphs = VGroup(*[g for grp in typed for g in grp])
        scene.add(prompt_glyphs)
        if len(cmd_glyphs):
            rt = type_time if type_time is not None else min(2.4, max(0.4, 0.045 * len(cmd)))
            scene.play(ShowIncreasingSubsets(cmd_glyphs, rate_func=linear), run_time=rt)
        for r in rows:
            scene.add(r)
        if len(rows) == 1:
            return rows[0]
        g = VGroup(*rows)
        g.rows, g.text = rows, " ".join(r.text for r in rows)
        return g

    def find(self, sub: str) -> VGroup:
        """The most recent line on screen whose text contains `sub` (to highlight or underline it)."""
        for ln in reversed(self.lines.submobjects):
            if sub in getattr(ln, "text", ""):
                return ln
        raise KeyError(f"no terminal line contains {sub!r}")

    def print(self, scene, lines, color: str = OUTPUT, run_time: float = 0.5, wrap: bool = False,
              lag: float = 0.15) -> VGroup:
        """Print output lines (fade in, slightly staggered). Returns the new lines."""
        items = []
        for x in ([lines] if isinstance(lines, (str, tuple)) else lines):
            s, col = (x, color) if isinstance(x, str) else x
            if wrap and len(s) > self.max_chars:
                while len(s) > self.max_chars:
                    items.append((s[: self.max_chars], col))
                    s = s[self.max_chars:]
                items.append((s, col))
            else:
                items.append((self._cut(s), col))
        if not items:
            return VGroup()
        self._make_room(scene, len(items))
        new = VGroup()
        for s, col in items:
            ln = mono_line(s, self.size, col)
            self._place(ln, len(self.lines))
            self.lines.add(ln)
            new.add(ln)
        from manim import LaggedStart
        scene.play(LaggedStart(*[FadeIn(m) for m in new], lag_ratio=lag), run_time=run_time)
        return new

    def run(self, scene, cmd: str, output=None, type_time: float | None = None,
            out_time: float = 0.5, color: str = OUTPUT, wrap: bool = False) -> VGroup:
        """Type `cmd` (folded if long), then print `output` (a list of lines, or None; `wrap` folds
        long output lines). Returns the command line (or its rows)."""
        line = self.type(scene, cmd, type_time)
        if output:
            self.print(scene, output, color=color, run_time=out_time, wrap=wrap)
        return line

    def clear(self, scene, run_time: float = 0.3) -> None:
        if len(self.lines):
            scene.play(FadeOut(self.lines), run_time=run_time)
            for m in list(self.lines):
                self.lines.remove(m)


# ------------------------------------------------------------------ code
def _house_code_style():
    """Monokai with light comments (the house style of the other videos' code panels)."""
    from pygments.styles import get_style_by_name
    from pygments.token import Comment
    base = get_style_by_name("monokai")
    return type("HouseCodeStyle", (base,), {"styles": {**base.styles, Comment: "#D9D3B8",
                                                        Comment.Single: "#D9D3B8"}})


HOUSE_CODE_STYLE = _house_code_style()


def code_block(source: str, language: str = "python", font_size: float = 22,
               width: float | None = None, line_numbers: bool = False, first_line: int = 1) -> Code:
    """Real code in the house style on a dark rounded panel. `width` scales the whole panel:
    keep the result >= 20 pt (font_size * scale). language: python, docker, toml, bash, yaml, json…"""
    c = Code(code_string=source, language=language, formatter_style=HOUSE_CODE_STYLE,
             add_line_numbers=line_numbers, line_numbers_from=first_line, background="rectangle",
             background_config={"fill_color": PANEL, "stroke_color": S.GREY_DARK,
                                "stroke_width": 2, "corner_radius": 0.15},
             paragraph_config={"font_size": font_size, "font": MONO})
    if width is not None:
        c.scale_to_fit_width(width)
    c.source = source
    return c


def code_span(code: Code, k: int, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of substring `sub` in line k (0-based) of a code_block."""
    line = code.source.split("\n")[k]
    i = -1
    for _ in range(occurrence + 1):
        i = line.find(sub, i + 1)
    if i < 0:
        raise ValueError(f"{sub!r} not in line {k}: {line!r}")
    start = len("".join(line[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*code.code_lines[k][start:start + n])


def line_bar(code: Code, k: int, color: str = S.YELLOW, opacity: float = 0.16) -> Rectangle:
    """A translucent bar over line k (0-based) of a code_block (add it after the code)."""
    ln, bg = code.code_lines[k], code.background
    return Rectangle(width=bg.width - 0.12, height=ln.height + 0.14, stroke_width=0) \
        .set_fill(color, opacity).move_to([bg.get_center()[0], ln.get_center()[1], 0])


def code_panel(source: str, path: str, first_line: int = 1, language: str = "python",
               focus=None, font_size: float = 22, width: float | None = None,
               dim: float = 0.3, caption_size: float = CAPTION) -> VGroup:
    """A real excerpt with a header tab "path · lines a–b" on top (so the viewer can find it in
    their own clone). Lines not in `focus` (0-based indices) are faded. .code .header"""
    c = code_block(source, language, font_size, width)
    n = len(source.split("\n"))
    if focus is not None:
        keep = {focus} if isinstance(focus, int) else set(focus)
        for k in range(n):
            if k not in keep and k < len(c.code_lines):
                c.code_lines[k].set_opacity(dim)
    last = first_line + n - 1
    where = f"line {first_line}" if n == 1 else f"lines {first_line}–{last}"
    head = mono(f"{path}", caption_size, S.GREY)
    where_t = label(f"· {where}", caption_size, S.GREY)
    header = VGroup(head, where_t).arrange(RIGHT, buff=0.14)
    header.next_to(c, UP, buff=0.1).align_to(c, LEFT).shift(RIGHT * 0.12)
    g = VGroup(c, header)
    g.code, g.header = c, header
    return g


# ------------------------------------------------------------------ file trees
def folder_glyph(height: float = 0.26, color: str = S.BLUE) -> VGroup:
    w = height * 1.3
    body = RoundedRectangle(width=w, height=height * 0.78, corner_radius=height * 0.08,
                            stroke_color=color, stroke_width=2).set_fill(color, 0.35)
    tab = RoundedRectangle(width=w * 0.45, height=height * 0.3, corner_radius=height * 0.06,
                           stroke_color=color, stroke_width=2).set_fill(color, 0.35)
    tab.next_to(body, UP, buff=-0.06).align_to(body, LEFT)
    return VGroup(tab, body)


def file_glyph(height: float = 0.3, color: str = S.GREY) -> VGroup:
    w = height * 0.76
    c = height * 0.28
    page = Polygon([-w / 2, height / 2, 0], [w / 2 - c, height / 2, 0], [w / 2, height / 2 - c, 0],
                   [w / 2, -height / 2, 0], [-w / 2, -height / 2, 0],
                   stroke_color=color, stroke_width=2).set_fill(color, 0.2)
    fold = VMobject(stroke_color=color, stroke_width=2).set_points_as_corners(
        [[w / 2 - c, height / 2, 0], [w / 2 - c, height / 2 - c, 0], [w / 2, height / 2 - c, 0]])
    return VGroup(page, fold)


class FileTree(VGroup):
    """file_tree(...): .rows (one per entry), .row(name) -> the row whose name is `name`."""

    def row(self, name: str) -> VGroup:
        for r in self.rows:
            if r.name == name or r.name.rstrip("/") == name.rstrip("/"):
                return r
        raise KeyError(name)


def file_tree(entries, size: float = SMALL, indent: float = 0.42, buff: float = 0.1,
              colors: dict | None = None, notes: dict | None = None,
              note_color: str = S.GREY) -> FileTree:
    """A directory listing. entries: strings with two spaces of indent per level, folders end
    with '/':  ["simple-translate/", "  cli.py", "  pyproject.toml", "  .venv/", "    bin/"].
    colors: {name: colour} for names; notes: {name: "short note"} printed in GREY to the right.
    Each row: .glyph .name_text .note .name .level"""
    colors, notes = colors or {}, notes or {}
    rows = VGroup()
    for e in entries:
        depth = (len(e) - len(e.lstrip(" "))) // 2
        name = e.strip()
        is_dir = name.endswith("/")
        col = colors.get(name, colors.get(name.rstrip("/"), S.BLUE if is_dir else INK))
        g = folder_glyph(0.24, col if is_dir else S.BLUE) if is_dir else file_glyph(0.3, S.GREY)
        t = mono_line(name, size, col)
        row = VGroup(g, t)
        t.next_to(g, RIGHT, buff=0.14)
        g.match_y(t.strut)
        note = None
        if name in notes or name.rstrip("/") in notes:
            note = label(notes.get(name, notes.get(name.rstrip("/"))), size - 2, note_color)
            note.next_to(t.strut, RIGHT, buff=0.35)
            row.add(note)
        row.glyph, row.name_text, row.note, row.name, row.level = g, t, note, name, depth
        rows.add(row)
    pitch = line_pitch(size) + buff
    for i, r in enumerate(rows):
        r.shift(np.array([r.level * indent - r.glyph.get_left()[0],
                          -i * pitch - r.name_text.strut.get_top()[1], 0]))
    tree = FileTree(*rows)
    tree.rows = rows
    return tree


# ------------------------------------------------------------------ machines
def laptop(width: float = 2.2, color: str = S.GREY) -> VGroup:
    """A laptop glyph: screen (.screen, a rectangle to put things on) and base."""
    screen = RoundedRectangle(width=width, height=width * 0.62, corner_radius=0.08,
                              stroke_color=color, stroke_width=3).set_fill(PANEL, 1)
    base = Polygon([-width * 0.62, 0, 0], [width * 0.62, 0, 0], [width * 0.55, width * 0.07, 0],
                   [-width * 0.55, width * 0.07, 0], stroke_color=color, stroke_width=3).set_fill(color, 0.3)
    base.next_to(screen, DOWN, buff=0.02)
    g = VGroup(screen, base)
    g.screen = screen
    return g


def server(height: float = 1.6, units: int = 3, color: str = S.GREY) -> VGroup:
    """A rack server glyph: `units` stacked slabs with status lights."""
    w = height * 1.1
    slab_h = height / units
    slabs = VGroup()
    for i in range(units):
        r = RoundedRectangle(width=w, height=slab_h * 0.86, corner_radius=0.05, stroke_color=color,
                             stroke_width=2.5).set_fill(PANEL, 1)
        lights = VGroup(*[Dot(radius=0.035, color=S.GREEN if j == 0 else color) for j in range(2)])
        lights.arrange(RIGHT, buff=0.07).move_to(r.get_right() + LEFT * 0.25)
        vents = VGroup(*[Line(UP * slab_h * 0.22, DOWN * slab_h * 0.22, color=color, stroke_width=1.5)
                         for _ in range(4)]).arrange(RIGHT, buff=0.07).move_to(r.get_left() + RIGHT * 0.35)
        slabs.add(VGroup(r, lights, vents))
    slabs.arrange(DOWN, buff=slab_h * 0.14)
    return slabs


def cloud(width: float = 3.0, color: str = S.BLUE, fill_opacity: float = 0.12) -> VMobject:
    """A cloud outline (union of circles)."""
    u = width / 3.0
    circles = [Circle(radius=0.55 * u).shift(LEFT * 0.75 * u + DOWN * 0.1 * u),
               Circle(radius=0.75 * u).shift(UP * 0.2 * u),
               Circle(radius=0.55 * u).shift(RIGHT * 0.8 * u + DOWN * 0.1 * u),
               RoundedRectangle(width=2.6 * u, height=0.75 * u, corner_radius=0.37 * u).shift(DOWN * 0.3 * u)]
    shape = Union(*circles)
    shape.set_stroke(color, 3).set_fill(color, fill_opacity)
    return shape


def machine_box(title: str, subtitle: str | None = None, width: float = 5.0, height: float = 3.2,
                color: str = S.BLUE, title_size: float = LABEL, sub_size: float = CAPTION,
                dashed: bool = False, fill_opacity: float = 0.06) -> VGroup:
    """A machine / VM / container drawn as a box with a header strip: title (and a GREY subtitle
    such as 'e2-medium · Debian 12'). .frame .header .title .subtitle .body (a point-holder
    rectangle for the inside area; place children with .move_to(box.body))."""
    frame = box(width, height, color, fill_opacity=fill_opacity, dashed=dashed)
    t = label(title, title_size, color)
    head = VGroup(t)
    st = None
    if subtitle:
        st = label(subtitle, sub_size, S.GREY)
        head = VGroup(t, st).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
    head_h = max(t.height, st.height if st else 0) + 0.3
    head.move_to(frame.get_top() + DOWN * head_h / 2)
    if head.width > width - 0.3:
        head.scale_to_fit_width(width - 0.3)
    sep = Line(frame.get_corner(UL) + DOWN * head_h, frame.get_corner(UR) + DOWN * head_h,
               color=color, stroke_width=1.5, stroke_opacity=0.6)
    body = Rectangle(width=width - 0.3, height=height - head_h - 0.2, stroke_width=0, fill_opacity=0)
    body.move_to(frame.get_bottom() + UP * (height - head_h) / 2)
    g = VGroup(frame, sep, head, body)
    g.frame, g.header, g.title, g.subtitle, g.body, g.sep = frame, head, t, st, body, sep
    return g


def layer_bar(text: str, width: float = 6.0, height: float = 0.6, color: str = S.GREY,
              size: float = SMALL, fill_opacity: float = 0.2) -> VGroup:
    """A horizontal layer of a stack (hardware / hypervisor / OS ...). .box .text"""
    b = box(width, height, color, fill_opacity=fill_opacity, radius=0.08)
    t = label(text, size, INK).move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


# ------------------------------------------------------------------ follow-along helpers
def step_badge(n: int | str, color: str = S.YELLOW, size: float = TAG, radius: float = 0.22) -> VGroup:
    c = Circle(radius=radius, stroke_color=color, stroke_width=2.5).set_fill(S.BG, 1)
    t = S.text(str(n), size, color, font=SANS, weight="BOLD").move_to(c)
    return VGroup(c, t)


class ReadmeTracker(VGroup):
    """Where we are in the tutorial README, pinned top-left: the section name and one dot per
    step; .goto(k) returns the animation that moves the highlight to step k (1-based) and shows
    "step k of N: <short label>". Keeps the viewer's place while they follow along.

        tr = ReadmeTracker("Installing App on VM Manually", ["Create VM", "SSH", "apt-get update", ...])
        self.play(FadeIn(tr)); self.play(tr.goto(3))
    """

    def __init__(self, section: str, steps: list[str], color: str = S.YELLOW, size: float = CAPTION,
                 corner=UL, **kw):
        super().__init__(**kw)
        self.steps, self.hi_color, self.size = steps, color, size
        head = VGroup(mono("README", size, S.GREY), label("›", size, S.GREY), label(section, size, INK))
        head.arrange(RIGHT, buff=0.12)
        dots = VGroup(*[Dot(radius=0.06, color=S.GREY_DARK) for _ in steps]).arrange(RIGHT, buff=0.13)
        dots.next_to(head, DOWN, buff=0.14, aligned_edge=LEFT)
        self.head, self.dots = head, dots
        self.k = 0
        self.caption = label(" ", size, color).next_to(dots, RIGHT, buff=0.25)
        self.add(head, dots, self.caption)
        self.to_corner(corner, buff=0.32)

    def _caption(self, k: int) -> Text:
        t = label(f"step {k} of {len(self.steps)}: {self.steps[k - 1]}", self.size, self.hi_color)
        return t.next_to(self.dots, RIGHT, buff=0.25)

    def set_step(self, k: int) -> "ReadmeTracker":
        """Jump to step k without animating (for a scene that starts mid-section)."""
        for i, d in enumerate(self.dots, start=1):
            d.set_color(self.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK))
            d.scale((1.5 if i == k else 1.0) / (d.width / 0.12))
        self.caption.become(self._caption(k))
        self.k = k
        return self

    def goto(self, k: int, run_time: float = 0.5):
        from manim import Transform
        anims = []
        for i, d in enumerate(self.dots, start=1):
            col = self.hi_color if i == k else (S.GREY if i < k else S.GREY_DARK)
            anims.append(d.animate.set_color(col).scale((1.5 if i == k else 1.0) / (d.width / 0.12)))
        new = self._caption(k)
        anims.append(Transform(self.caption, new))
        self.k = k
        return AnimationGroup(*anims, run_time=run_time)


# ------------------------------------------------------------------ browser / console
def browser_window(url: str, width: float = 9.0, height: float = 5.6, size: float = CAPTION,
                   color: str = S.GREY_DARK) -> VGroup:
    """A schematic browser window (no logos): title bar with an address field showing `url`.
    .frame .address .content (rectangle of the page area)."""
    frame = RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=color,
                             stroke_width=2).set_fill(PANEL, 1)
    bar_h = 0.55
    bar = Line(frame.get_corner(UL) + DOWN * bar_h, frame.get_corner(UR) + DOWN * bar_h,
               color=color, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.055, color=S.GREY_DARK) for _ in range(3)]).arrange(RIGHT, buff=0.1)
    dots.move_to(frame.get_corner(UL) + np.array([0.35, -bar_h / 2, 0]))
    addr_box = RoundedRectangle(width=width - 1.4, height=0.36, corner_radius=0.18,
                                stroke_width=0).set_fill(TERM_BG, 1)
    addr_box.move_to(frame.get_top() + DOWN * bar_h / 2 + RIGHT * 0.35)
    addr = mono(url, size, S.GREY)
    if addr.width > addr_box.width - 0.3:
        addr.scale_to_fit_width(addr_box.width - 0.3)
    addr.move_to(addr_box).align_to(addr_box, LEFT).shift(RIGHT * 0.18)
    content = Rectangle(width=width - 0.3, height=height - bar_h - 0.25, stroke_width=0, fill_opacity=0)
    content.move_to(frame.get_bottom() + UP * (height - bar_h) / 2)
    g = VGroup(frame, bar, dots, addr_box, addr)
    g.frame, g.address, g.content = frame, addr, content
    g.add(content)
    return g


def form_rows(fields, width: float = 7.5, size: float = CAPTION + 2, value_color: str = INK,
              label_color: str = S.GREY, buff: float = 0.16) -> VGroup:
    """A schematic web form: rows of (label, value) with an input box for each value.
    Each row: .label .field .value; the group has .rows"""
    rows = VGroup()
    lw = width * 0.38
    for lab, val in fields:
        lt = label(lab, size, label_color)
        field = RoundedRectangle(width=width - lw, height=mono("|", size).height + 0.2, corner_radius=0.06,
                                 stroke_color=S.GREY_DARK, stroke_width=1.5).set_fill(TERM_BG, 1)
        vt = mono(val, size - 2, value_color)
        if vt.width > field.width - 0.25:
            vt.scale_to_fit_width(field.width - 0.25)
        lt.move_to(ORIGIN, aligned_edge=LEFT)
        field.move_to([lw + field.width / 2, 0, 0])
        vt.move_to(field).align_to(field, LEFT).shift(RIGHT * 0.12)
        row = VGroup(lt, field, vt)
        row.label, row.field, row.value = lt, field, vt
        rows.add(row)
    rows.arrange(DOWN, buff=buff, aligned_edge=LEFT)
    rows.rows = rows
    return rows


__all__ = [
    "MONO", "SANS", "INK", "TERM_BG", "PANEL", "TITLE", "BODY", "LABEL", "SMALL", "TAG", "CAPTION",
    "PROMPT_USER", "PROMPT_PATH", "OUTPUT", "COMMENT",
    "label", "mono", "cell_width", "line_pitch", "mono_line", "glyph_range", "substring",
    "box", "chip", "tag", "check_mark", "cross_mark", "warning_sign",
    "Terminal", "code_block", "code_span", "line_bar", "code_panel",
    "folder_glyph", "file_glyph", "FileTree", "file_tree",
    "laptop", "server", "cloud", "machine_box", "layer_bar",
    "step_badge", "ReadmeTracker", "browser_window", "form_rows",
]
