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
