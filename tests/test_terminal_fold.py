"""Terminal.fold keeps every character of a typed command."""
from types import SimpleNamespace

import pytest

devops = pytest.importorskip("explainer.devops")
fold = devops.Terminal.fold


def _join(rows):
    """Undo the folding: drop ' \\' row ends and the 4-space continuation indents."""
    out = rows[0][:-2] if len(rows) > 1 else rows[0]
    for i, r in enumerate(rows[1:], start=1):
        body = r[4:]
        out += body[:-2] if i < len(rows) - 1 else body
    return out


def test_hard_break_keeps_every_character():
    term = SimpleNamespace(max_chars=20)
    text = "$ " + "abcdefghijklmnopqrstuvwxyz0123456789"   # no space after the prompt
    rows = fold(term, text, first_prefix=2)
    assert all(len(r) <= 20 for r in rows)
    assert _join(rows) == text


def test_soft_break_drops_only_the_space():
    term = SimpleNamespace(max_chars=24)
    text = "$ docker run --rm -p 8000:8000 my-image:latest"
    rows = fold(term, text, first_prefix=2)
    assert all(len(r) <= 24 for r in rows)
    assert " ".join([rows[0][:-2]] + [r[4:].removesuffix(" \\") for r in rows[1:]]) == text
