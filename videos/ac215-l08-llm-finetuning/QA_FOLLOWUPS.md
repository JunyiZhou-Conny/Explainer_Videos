# L08 QA follow-ups (from the whole-video QA and its verifiers, deferred out of the episode)

Each item was found on the QA draft (e7ddece, QA committed at 2678243); check it in the CURRENT code and on frames.

- Shared, toolkit PR (explainer/subtitles.py, not this episode): the English .srt two-line breaker splits the
  en_display artifacts across lines: `docker ps` / `-a` at 13:08, `source:` / `not found` at 05:11, `KeyError:` /
  `'question'` at 09:40. It should treat the glossary's A1 artifacts (`docker ps -a`, `source: not found`,
  `KeyError: 'question'`, `Tuned model info: None`) as unbreakable spans. No episode-side change is needed;
  re-check those three cues once the toolkit fix lands.
