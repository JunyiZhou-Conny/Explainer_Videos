"""The English-only .srt shows a sentence's `en_display` form, as the bilingual track does.

A follow-along video says commands as words ("dash dash rm") and the i18n files give the form the
viewer types (`--rm`) as `en_display`. The English track used to ignore it.

    PYTHONPATH=. python -m pytest -q tests/test_build_english_display.py
"""

from explainer.build import _english_display, split_cues
from explainer.i18n import Line
from explainer.voice import split_sentences

TEXT = "Run docker run dash dash rm dash t i simple translate. Then type exit. Done."


def _cue(marks=True):
    sents = split_sentences(TEXT)
    cue = {"text": TEXT, "start": 0.0, "end": 8.0}
    if marks:
        cue["marks"] = [(o, 1.0 + 2.5 * i) for i, (o, _) in enumerate(sents)]
    return cue


def _table(display):
    key = " ".join(TEXT.split())
    return {"zh": {key: Line(TEXT, ["一", "二", "三"], ["一", "二", "三"], {}, display)}}


def test_display_form_replaces_the_spoken_sentence_and_keeps_its_time():
    shown, marks = _english_display(_cue(), _table(["Run docker run --rm -ti simple-translate.", None, None]))
    assert shown == "Run docker run --rm -ti simple-translate. Then type exit. Done."
    assert [t for _, t in marks] == [1.0, 3.5, 6.0]
    assert [o for o, _ in marks] == [o for o, _ in split_sentences(shown)]
    cues = split_cues(0.0, 8.0, shown, marks=marks)
    assert [(a, c) for a, _, c in cues] == [(1.0, "Run docker run --rm -ti simple-translate."),
                                            (3.5, "Then type exit."), (6.0, "Done.")]


def test_no_display_leaves_the_clip_untouched():
    cue = _cue()
    assert _english_display(cue, {}) == (TEXT, cue["marks"])
    assert _english_display(cue, _table([None, None, None])) == (TEXT, cue["marks"])


def test_the_clips_own_display_wins_and_unmarked_clips_still_work():
    cue = _cue(marks=False)
    cue["en_display"] = [None, "Then type `exit`.", None]
    shown, marks = _english_display(cue, _table(["ignored.", None, None]))
    assert shown == "Run docker run dash dash rm dash t i simple translate. Then type `exit`. Done."
    assert marks is None
