"""Shared data for E0 'Decoding the start-up commands'. Boxes, colours and widgets come from the series
kit (videos/careonex-series/careonex_kit.py)."""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
SERIES = PROJECT.parent / "careonex-series"
sys.path.insert(0, str(SERIES))

from careonex_kit import *  # noqa: E402,F401,F403
from explainer.script import load_narration  # noqa: E402

NARRATION = load_narration(PROJECT / "script.md")

# Marco's two command blocks (team chat, 2026-10-10 16:08), exactly; the Knowledge Base id is masked
# because this repository is public (the team's own docs keep account identifiers out of git).
KB_ID_MASKED = "UYC7······"
T1 = [
    'cd "C:\\Users\\Marco\\Desktop\\CareOneX_Requester_Live_Voice_App"',
    '',
    '$env:HOME = $HOME',
    '$env:AWS_PROFILE = "careonex-team"',
    '$env:AWS_DEFAULT_REGION = "us-east-1"',
    f'$env:CAREONEX_KB_ID = "{KB_ID_MASKED}"',
    '',
    'aws sso login --profile careonex-team',
    '',
    'docker compose up --build retrieve',
]
T2 = [
    'cd "C:\\Users\\Marco\\Desktop\\CareOneX_Requester_Live_Voice_App"',
    '',
    '$env:AWS_PROFILE = "careonex-team"',
    '$env:AWS_DEFAULT_REGION = "us-east-1"',
    '$env:CAREONEX_RETRIEVE_URL = "http://127.0.0.1:8080"',
    '$env:CAREONEX_VOICE_SEARCH_MODE = "feedback"',
    '',
    'uv run --python 3.12 --extra mic --directory services/voice python -c',
    '   "import asyncio; from nova_sonic.__main__ import run; asyncio.run(run())"',
]
UV_LINE = ('uv run --python 3.12 --extra mic --directory services/voice python -c '
           '"import asyncio; from nova_sonic.__main__ import run; asyncio.run(run())"')


def big_line(text: str, size: float = 30, color=None):
    """One command line, large, on a dark strip (the line being explained)."""
    return text_panel([text], size=size, color=color or QUERY_C, border=QUERY_C)
