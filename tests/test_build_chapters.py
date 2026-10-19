"""Chapter times are rounded down to the second, after rounding away float noise.

A scene's offset is a sum of ffprobe durations; L04's S09 started at 1004.999999 s, and plain
truncation put its chapter at 16:44, on the previous scene's last second.

    PYTHONPATH=. python -m pytest -q tests/test_build_chapters.py
"""

from explainer.build import fmt_chapter


def test_a_chapter_never_points_past_its_scene():
    assert fmt_chapter(310.55) == "05:10"
    assert fmt_chapter(0.0) == "00:00"
    assert fmt_chapter(59.9989) == "00:59"


def test_float_noise_below_a_whole_second_is_not_a_second_early():
    assert fmt_chapter(1004.999999) == "16:45"
    assert fmt_chapter(3599.9999999) == "1:00:00"
    assert fmt_chapter(3725.2) == "1:02:05"
