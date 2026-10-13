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

# language versions (EXPLAINER_LANG=zh ...): translate every on-screen string, pick CJK fonts
from . import i18n as _i18n  # noqa: E402

_i18n.install()


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


# ---------------------------------------------------------------- fonts of the short format (docs/SHORTS.md)
# Free OFL fonts, installed by setup/install.sh (apt: fonts-noto-cjk fonts-noto-core fonts-noto-mono fonts-montserrat
# fonts-inter fonts-ebgaramond). The long videos keep the fonts above; nothing here changes them.
FONT_CJK_SERIF = "Noto Serif CJK SC"   # Song/Ming serif: Chinese captions, huge title glyphs
FONT_CJK_SANS = "Noto Sans CJK SC"
FONT_CJK_MONO = "Noto Sans Mono CJK SC"
FONT_TRACKED = "Montserrat"            # geometric sans for wide-tracked title words ("E N T R O P Y")
FONT_HEAVY = "Inter"                   # with weight=HEAVY (Inter Black): the one hero number of a scene
FONT_OLDSTYLE = "EB Garamond"          # old-style serif (italic) for small formula labels
FONT_MONO = "Noto Sans Mono"           # HUD readouts, the English caption line

# old-style maths for formula labels: EB Garamond letters and digits through XeLaTeX + mathspec
OLDSTYLE_TEX = TexTemplate(tex_compiler="xelatex", output_format=".xdv")
OLDSTYLE_TEX.add_to_preamble(r"\usepackage{mathspec}\setmainfont{EB Garamond}"
                             r"\setmathsfont(Digits,Latin,Greek){EB Garamond}")


def font_available(family: str) -> bool:
    """Whether Pango can find `family` (e.g. after setup/install.sh installed the OFL fonts)."""
    import manimpango
    return family in manimpango.list_fonts()


# Frame helpers (default Manim frame is 14.22 x 8 units)
FRAME_W = config.frame_width
FRAME_H = config.frame_height
SAFE_W = FRAME_W - 1.0   # keep content 0.5 units away from the left/right edges
SAFE_H = FRAME_H - 0.8

__all__ = [n for n in dir() if n.isupper() or n in {"text", "math", "tex", "bullets", "font_available"}] + [
    "UP", "DOWN", "LEFT", "RIGHT", "ORIGIN"]
