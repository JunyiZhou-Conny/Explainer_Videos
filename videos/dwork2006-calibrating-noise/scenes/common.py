"""Shared settings for this video: semantic colours, assets, and the narration from script.md."""

from pathlib import Path

from explainer import style as S
from explainer.script import load_narration

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
ASSETS = PROJECT / "assets"
PAPER_P1 = ASSETS / "paper_p1.png"   # page 1 of the paper (title + abstract)
PAPER_P6 = ASSETS / "paper_p6.png"   # page 270: Definition 1, Example 1
PAPER_P8 = ASSETS / "paper_p8.png"   # page 272: Proposition 1

# Semantic colours — keep fixed for the whole video (see script.md).
X_COLOR = S.BLUE        # database x / world 1
XP_COLOR = S.ORANGE     # neighbouring database x' / world 2
ALICE = S.PINK          # Alice / the single changed row
EPS_COLOR = S.YELLOW    # epsilon: privacy loss / budget
SENS_COLOR = S.GREEN    # sensitivity S(f)
NOISE_COLOR = S.RED     # noise, Laplace densities
TRUTH_COLOR = S.WHITE   # true answers
DIM = S.GREY            # secondary text

NARRATION = load_narration(PROJECT / "script.md")
ANALYST_COLOR = S.PURPLE  # the analyst / attacker figure, in every scene


def budget_bar(width: float = 4.0, n: int = 8, height: float | None = None, spent: int = 0,
               label: bool = True, label_size: float = 30):
    """THE privacy-budget bar of this video (S02, S09, S11, S12 all use this one object).

    A YELLOW outlined frame holding n equal YELLOW segments; the last `spent` segments start empty.
    Returns VGroup(frame, segs[, label]) with attributes .frame, .segs, .label (or None).
    Drain it by fading segments out from the right: FadeOut(bar.segs[-1]) or
    bar.segs[i].animate.set_fill(opacity=0).
    """
    from manim import RIGHT, UP, Rectangle, VGroup

    height = height if height is not None else max(0.22, 0.09 * width)
    gap = max(0.04, 0.015 * width)
    frame = Rectangle(width=width, height=height, stroke_color=EPS_COLOR, stroke_width=2.5)
    seg_w = (width - gap * (n + 1)) / n
    segs = VGroup(*[Rectangle(width=seg_w, height=height - 2 * gap, stroke_width=0)
                    .set_fill(EPS_COLOR, 0.0 if i >= n - spent else 0.9) for i in range(n)])
    segs.arrange(RIGHT, buff=gap).move_to(frame)
    parts = [frame, segs]
    lab = None
    if label:
        lab = S.math(r"\text{privacy budget }", r"\varepsilon", size=label_size, color=EPS_COLOR)
        lab.next_to(frame, UP, buff=0.2)
        parts.append(lab)
    bar = VGroup(*parts)
    bar.frame, bar.segs, bar.label = frame, segs, lab
    return bar
