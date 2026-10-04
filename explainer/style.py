"""Shared look: a 3Blue1Brown-flavoured dark palette with *semantic* colours.

The single most useful habit from 3b1b: a concept keeps its colour for the whole video.
Pick colours by meaning (`X_COLOR` for database x, `EPS_COLOR` for epsilon, ...), never ad hoc.
Videos may add their own semantic aliases on top of these.
"""

from manim import (DOWN, LEFT, ORIGIN, RIGHT, UP, MathTex, Tex, Text, TexTemplate, VGroup,
                   config)

# ---------------------------------------------------------------- canvas
BG = "#0D0F14"          # near-black with a hint of blue
config.background_color = BG

# ---------------------------------------------------------------- base palette (3b1b-ish)
WHITE = "#ECECEC"
GREY = "#8A8F98"
GREY_DARK = "#3A3F4A"
GREY_DARKER = "#22262E"
BLUE = "#58C4DD"
TEAL = "#5CD0B3"
GREEN = "#83C167"
YELLOW = "#FFD54F"
GOLD = "#E8B04B"
ORANGE = "#FF8F40"
RED = "#FC6255"
PINK = "#F28FB5"
PURPLE = "#B189F5"

# ---------------------------------------------------------------- typography
FONT = "CMU Serif"          # matches the LaTeX maths
FONT_SANS = "CMU Sans Serif"
TITLE_SIZE = 56
BODY_SIZE = 34
SMALL_SIZE = 26
TINY_SIZE = 20

TEX_TEMPLATE = TexTemplate()
TEX_TEMPLATE.add_to_preamble(r"\usepackage{amsmath,amssymb,bm}")


def text(s: str, size: float = BODY_SIZE, color: str = WHITE, font: str = FONT, **kw) -> Text:
    """Plain text in the house font."""
    return Text(s, font=font, font_size=size, color=color, **kw)


def math(*s: str, size: float = 44, color: str = WHITE, **kw) -> MathTex:
    return MathTex(*s, font_size=size, color=color, tex_template=TEX_TEMPLATE, **kw)


def tex(*s: str, size: float = 40, color: str = WHITE, **kw) -> Tex:
    return Tex(*s, font_size=size, color=color, tex_template=TEX_TEMPLATE, **kw)


def bullets(items, size: float = BODY_SIZE, color: str = WHITE, buff: float = 0.32,
            bullet: str = "•") -> VGroup:
    rows = VGroup(*[text(f"{bullet}  {it}", size, color) for it in items])
    rows.arrange(DOWN, aligned_edge=LEFT, buff=buff)
    return rows


# Frame helpers (default Manim frame is 14.22 x 8 units)
FRAME_W = config.frame_width
FRAME_H = config.frame_height
SAFE_W = FRAME_W - 1.0   # keep content 0.5 units away from the left/right edges
SAFE_H = FRAME_H - 0.8

__all__ = [n for n in dir() if n.isupper() or n in {"text", "math", "tex", "bullets"}] + [
    "UP", "DOWN", "LEFT", "RIGHT", "ORIGIN"]
