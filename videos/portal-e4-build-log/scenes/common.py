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
