"""Shared helpers for 项目周记 E4 'Two days, a hundred-plus commits' (3b1b house style).

Re-exports E2's helpers (videos/portal-e2-thinking/scenes/common.py: the CareOneX kit, the semantic
colours, zh(), zh_wrap(), quote_panel(), ponder_zh(), clear() …) and adds time axes for the week's
commits. Every time, count and quote is listed in ../SOURCES.md.
"""

import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent

_spec = importlib.util.spec_from_file_location(
    "portal_e2_common", PROJECT.parent / "portal-e2-thinking" / "scenes" / "common.py")
_e2 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_e2)
globals().update({k: v for k, v in vars(_e2).items()
                  if not k.startswith("__") and k not in ("HERE", "PROJECT", "NARRATION")})

from explainer.script import load_narration  # noqa: E402

NARRATION = load_narration(PROJECT / "script.md")   # this episode's lines, not E2's

# Commit times, hours after Tuesday 2026-10-27 00:00 Boston (git log --format=%ct; ../SOURCES.md)
# PR #36 (c05cd2e..17228bd) and PR #41 (17228bd..b7ab98e): own commits and merge commits
H36 = [12.372, 12.567, 12.801, 12.963, 13.047, 13.05, 13.05, 14.209, 14.964, 14.964, 14.965, 14.965, 15.026, 15.139,
       18.662, 21.359, 21.429, 21.454, 21.549, 21.718, 21.808, 22.464, 22.53, 22.591, 22.687, 22.704, 22.777, 22.857,
       22.914, 22.993, 23.006, 23.093, 23.142, 23.212, 23.272, 23.388, 23.447, 23.89, 23.969, 24.127, 25.877, 34.091,
       34.1, 35.073, 35.236, 35.326, 35.516, 35.888, 35.946, 37.687, 37.888, 42.773, 43.128, 43.337, 43.337, 43.394,
       45.071, 45.481, 47.278, 48.752]
M36 = [25.855, 43.173, 43.179]
H41 = [25.984, 26.273, 26.383, 34.035, 34.15, 34.247, 34.67, 34.965, 34.987, 35.075, 35.151, 35.394, 35.46, 35.587,
       35.713, 36.114, 37.66, 38.051, 38.355, 39.326, 39.366, 39.628, 40.881, 41.152, 41.824, 42.749, 43.074, 43.274]
M41 = [35.328, 35.53, 35.897, 35.947, 37.694, 37.901, 42.405, 42.406, 42.417, 43.057, 43.195, 43.275, 43.359, 43.415,
       45.081, 45.564, 47.292, 48.767]
# the own commits whose message names Bugbot, Codex or a review (53 of 88; ../SOURCES.md)
R36 = [12.963, 14.964, 14.964, 14.965, 14.965, 15.026, 15.139, 21.454, 21.549, 21.808, 22.464, 22.53, 22.591, 22.687,
       22.704, 22.777, 22.857, 22.914, 22.993, 23.006, 23.093, 23.142, 23.212, 23.272, 23.388, 23.447, 23.969, 24.127,
       34.091, 35.236, 35.326, 35.516, 35.946, 37.888, 43.337, 43.394, 45.071, 45.481, 47.278, 48.752]
R41 = [34.247, 35.394, 35.46, 35.587, 36.114, 38.051, 38.355, 39.326, 39.366, 40.881, 41.152, 41.824, 43.274]
SESSION_SWITCH = 25.85   # session 1: 10-27 12:22 → 10-28 00:07; session 2 from 10-28 01:51


def clock(h: float) -> str:
    """Hours after Tuesday 00:00 → 'Tue 21:21'."""
    day = ["Tue", "Wed", "Thu"][int(h // 24)]
    hh = h % 24
    return f"{day} {int(hh):02d}:{round(hh % 1 * 60) % 60:02d}"


def week_axis(x0: float = -5.9, x1: float = 5.9, y: float = -1.0, h0: float = 12.0, h1: float = 49.0,
              step: float = 6.0, size: float = 20):
    """A Boston-time axis from Tue noon to Thu 01:00; returns (line, ticks, x_of)."""
    line = Line([x0, y, 0], [x1, y, 0], color=S.GREY, stroke_width=2)

    def x_of(h):
        return x0 + (h - h0) / (h1 - h0) * (x1 - x0)
    ticks = VGroup()
    h = h0
    while h <= h1 + 1e-9:
        lab = clock(h).split()[0] + " " + f"{int(h % 24)}:00"
        ticks.add(VGroup(Line([x_of(h), y - 0.08, 0], [x_of(h), y + 0.08, 0], color=S.GREY),
                         sans(lab, size, S.GREY).move_to([x_of(h), y - 0.35, 0])))
        h += step
    return line, ticks, x_of


def commit_ticks(x_of, hours, y: float, height: float, color, width: float = 3) -> VGroup:
    return VGroup(*[Line([x_of(h), y, 0], [x_of(h), y + height, 0], color=color, stroke_width=width) for h in hours])
