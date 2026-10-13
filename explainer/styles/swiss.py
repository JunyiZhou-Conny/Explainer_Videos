"""Swiss components: the reusable visual vocabulary of the `swiss` preset.

Extracted from the first Swiss episode (videos/skills-ecosystem/scenes.py) so the next
Swiss episode starts from a library instead of re-authoring helpers that can drift from
the preset. Colours and sizes come from presets/swiss.tokens.json — one source of truth.

Use from an episode's scenes.py:

    from explainer.styles import swiss
    from explainer.styles.swiss import PAPER, INK, RED, GRAY, FAINT, label, at, left, line, card, folder, arrow
    swiss.setup_fonts()          # registers Inter + Noto CJK for this process
    config.background_color = PAPER
"""
from __future__ import annotations

import os
from pathlib import Path

from manim import (BOLD, NORMAL, Arrow, Line, Rectangle, Text, VGroup)

from . import ROOT, tokens

TOKENS = tokens("swiss")
PAPER = TOKENS["palette"]["background"]
INK = TOKENS["palette"]["ink"]
RED = TOKENS["palette"]["accent"]
GRAY = TOKENS["palette"]["muted"]
FAINT = TOKENS["palette"]["faint"]
LATIN = TOKENS["type"]["latin"]
CJK = TOKENS["type"]["cjk"]

PROJECT_FONTS = ("Inter-Variable.ttf", "NotoSansCJKsc-Regular.otf", "NotoSansCJKsc-Bold.otf")


def setup_fonts() -> None:
    """Register the licensed project fonts for this process, without changing system fonts."""
    import manimpango
    fonts_dir = Path(os.environ.get("EXPLAINER_FONTS_DIR", ROOT / "assets/fonts"))
    for font_name in PROJECT_FONTS:
        font_path = fonts_dir / font_name
        if not font_path.is_file() or not manimpango.register_font(str(font_path)):
            raise RuntimeError(f"Project font unavailable: {font_path}. "
                               "Run tools/setup-runtime --assets-only.")


def label(s, size=30, color=INK, width=None, bold=False):
    t = Text(s, font=LATIN if not any("一" <= c <= "鿿" for c in s) else CJK,
             font_size=size, color=color, weight=BOLD if bold else NORMAL, line_spacing=0.9)
    if width and t.width > width:
        t.scale_to_fit_width(width)
    return t


def at(s, x, y, size=30, color=INK, width=None, bold=False):
    return label(s, size, color, width, bold).move_to([x, y, 0])


def left(s, x, y, size=30, color=INK, width=None, bold=False):
    t = label(s, size, color, width, bold)
    t.move_to([x + t.width / 2, y, 0])
    return t


def line(x1, y1, x2, y2, color=INK, stroke=2):
    return Line([x1, y1, 0], [x2, y2, 0], color=color, stroke_width=stroke)


def card(title, sub, x, y, w=3.6, h=1.9, accent=False):
    frame = Rectangle(width=w, height=h, stroke_color=RED if accent else INK, stroke_width=2,
                      fill_color=PAPER, fill_opacity=1).move_to([x, y, 0])
    return VGroup(frame, left(title, x - w / 2 + .22, y + .28, 32, RED if accent else INK,
                              w - .44, True),
                  left(sub, x - w / 2 + .22, y - .37, 21, GRAY, w - .44))


def folder(name, x, y, w=3.6, color=INK):
    body = Rectangle(width=w, height=1.15, stroke_color=color, stroke_width=2,
                     fill_color=PAPER, fill_opacity=1).move_to([x, y, 0])
    tab = Rectangle(width=w * .38, height=.18, stroke_color=color, stroke_width=2,
                    fill_color=PAPER, fill_opacity=1).move_to([x - w * .30, y + .66, 0])
    text = at(name, x, y, 25, color, w - .3)
    return VGroup(tab, body, text)


def arrow(a, b, color=RED):
    return Arrow(a, b, buff=.08, color=color, stroke_width=3,
                 max_tip_length_to_length_ratio=.12)
