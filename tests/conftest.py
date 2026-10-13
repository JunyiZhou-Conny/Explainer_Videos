"""Shared test setup: register the project fonts for this process.

Font-metric tests (e.g. the RollingCounter separator) measure text set in the project
fonts. CI runners have no Inter/Noto CJK in fontconfig, so register the downloaded
copies from assets/fonts exactly as scenes do; tools/setup-runtime fetches them.
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PROJECT_FONTS = ("Inter-Variable.ttf", "NotoSansCJKsc-Regular.otf", "NotoSansCJKsc-Bold.otf")


def register_project_fonts() -> list[str]:
    missing = []
    fonts_dir = Path(os.environ.get("EXPLAINER_FONTS_DIR", ROOT / "assets/fonts"))
    try:
        import manimpango
    except ImportError:
        return list(PROJECT_FONTS)
    for name in PROJECT_FONTS:
        path = fonts_dir / name
        if not path.is_file() or not manimpango.register_font(str(path)):
            missing.append(name)
    return missing


MISSING_FONTS = register_project_fonts()
