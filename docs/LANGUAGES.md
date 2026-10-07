# Language versions

A video can have versions in other languages that reuse its animation unchanged: translated
narration (code-switched where real speakers code-switch), translated on-screen text, and
bilingual subtitles (the translation on top, the English original below). Chinese is the first
one; both videos in this repo have it (`videos/<id>/i18n/zh/`, rendered to `videos/<id>/output/zh/`).

The English video is never touched: every language-specific change in a scene is guarded by
`i18n.active()` or is a refactor that builds the same objects, and that is checked frame by frame.

## Files

```
videos/<id>/i18n/zh/
  GLOSSARY.md, glossary.yaml   terminology and code-switching policy (the binding rules; yaml is read by the checker)
  narration/*.yaml             every SAY line, translated sentence by sentence (+ say: spoken forms, anchors)
  strings/*.yaml               on-screen text: exact, re: and "<scene stem>|<text>" keys
  meta.yaml                    title, description, chapter and part titles
  README.md, exercises.md, playground.html, digest.md, assets/   companions in Chinese
explainer/locales/zh.yaml      toolkit strings ("Pause and ponder" → 暂停想一想)
explainer/lexicon.zh.yaml      respellings for the Chinese voice (e.g. SuLQ → "sulk")
```

The formats are documented in the docstring of `explainer/i18n.py`. Sentence alignment is the key
idea: each English sentence (as split by `explainer.voice.split_sentences`) has exactly one
translated sentence. That lets every scene keep its English `vo.wait_until("...")` anchors (they
are mapped onto the matching Chinese sentence, by position or through an explicit `anchors:` map),
and it pairs the two lines of every bilingual subtitle.

## Workflow

1. **Glossary first.** Decide, for this audience, which words stay in English and which use the
   standard Chinese term. Ask how a real speaker in that setting talks: a Chinese PhD student
   presenting a DP paper keeps *query*, *trick*, *hybrid argument* and names in English but says
   差分隐私, 敏感度, 拉普拉斯机制; a teacher of 12-year-olds keeps only `explore`, `winner`, `None`,
   Python and X/O, and glosses each once. Write it in `GLOSSARY.md` + `glossary.yaml`.
2. **Translate.** `narration/*.yaml` (one entry per SAY line of `script.md`), `strings/*.yaml` and
   `meta.yaml`. To list every on-screen string with its call site:
   `python -m explainer.strings videos/<id> --lang zh`.
3. **Check.** `python -m explainer.i18n check videos/<id> --lang zh` (alignment, spoken-text
   hygiene, Latin words not allowed by the glossary). Timing against the English, per SAY block
   (synthesizes and caches all narration): `cd videos/<id> && python -m explainer.script script.md --lang zh`.
4. **Adapt the scenes.** Per scene: `python -m explainer.preview scenes/<file> <Class> --lang zh`
   (prints each Chinese sentence with its start time, writes contact sheets) and
   `python -m explainer.check scenes/<file> <Class> --lang zh`. Typical fixes: glyph indices that
   assume English text (find glyphs by searching the rendered string instead), coloured
   sub-phrases, labels that overflow, zh-only `run_time`s where a Chinese sentence reaches a word
   earlier. **English regression:** before editing a scene, render its English preview and save
   `ffmpeg -v error -i <movie> -map 0:v -f framemd5 before.md5`; afterwards the English render must
   be identical. Render both with `PYTHONHASHSEED=0 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
   MKL_NUM_THREADS=1`, otherwise a few scenes differ run to run in fade frames.
5. **Voice.** The default Chinese narrator is `zh-CN-XiaoyiNeural` (edge-tts; `DEFAULT_VOICES` in
   `explainer/build.py`), chosen with a speech-recognition round trip: Xiaoxiao read the kept
   English terms with a heavy accent (noise → "Nice", epsilon → "Excellent"). A `video.yaml` can
   override it: `languages: {zh: {voice: {backend: edge, voice: ..., speed: 1.0}}}`.
   **Publishing:** the free Edge endpoint is not licensed for published videos. Set
   `AZURE_SPEECH_KEY` and `AZURE_SPEECH_REGION` (an Azure AI Speech resource; the free F0 tier is
   enough for these videos) and the same voices come from the official API automatically
   (`EXPLAINER_EDGE_VIA_AZURE=0` opts out). A local Kokoro voice was evaluated too; its Mandarin
   is weaker and it is not wired in.
6. **Review the whole video** (a bilingual reviewer and someone from the target audience), fix,
   and rebuild. `--subs-only` rewrites subtitles, chapters and transcript from existing renders.
7. **Build.** `python -m explainer.build videos/<id> --lang zh --crf 25` → `output/zh/<id>.mp4`
   (1080p60, bilingual subtitles burned in a band under the slightly scaled-down picture;
   `--no-burn` keeps it clean), `<id>.zh.srt`, `<id>.en.srt` (English on the Chinese timing),
   `<id>.zh-en.srt` / `.ass`, `chapters.txt`, `transcript.md`, and the same per part. The English
   build also writes `<id>.zh.srt` / `<id>.zh-en.srt` / `.ass` for the English video.

## Subtitles

Made by `explainer/subtitles.py` from the narration timings recorded while rendering:

- Cues never cross sentences; a cue shorter than 1 s merges into a neighbour, keeping the
  sentence punctuation inside it (不是。电脑能做的……). Only the end of a Chinese cue loses its 。，、；：.
- Lines break at punctuation whenever the pieces fit; otherwise at the best word gap. English never
  ends a line on an article or preposition or next to a number; Chinese never ends a line on a
  preposition (从, 把, 在 …), starts one with a particle (的, 了 …) or cuts inside a word (jieba).
- In the bilingual band the English sentence is cut where the Chinese one is, at the matching
  clause; if none is close and it fits on one line, the whole sentence stays up under each piece.
- Sidecar cues have at most 2 lines; short cues stay up 1.6 s when the next one leaves room.

## Lessons from the Chinese versions

- **Anchors drift where spoken and displayed text differ.** An anchor is placed by its character
  position in the displayed sentence. Spoken forms longer than their display (1/ε → 艾普西隆分之一)
  make later words come early; Latin words (query, Google) make them come late; a subtitle-only
  gloss （……） shifts the words before it. Check beats against word times (Whisper) and aim the
  anchor a little earlier or later.
- **No italics for Chinese.** Pango only slants Hanzi synthetically: set Chinese upright under
  `i18n.active()` where the English uses `slant=ITALIC`. Bold is fine.
- **Punctuation fonts.** The Latin house font comes first in the fallback list: Chinese quotes and
  `……` are drawn from the CJK font automatically; `——` stays in the house font (two CJK U+2014
  leave a gap). No half-width space next to full-width punctuation (`→“是”`, not `→ “是”`).
- **TeX.** CJK in TeX goes through XeLaTeX + ctex; xeCJK adds no space at the end of `\text{…}`
  before maths, so write it (`\text{答案}\ 0`); no `\quad` after a full-width ：.
- **Say numbers and symbols the way a teacher would** with `say:` (ε → 艾普西隆, 轮到 X 的时候),
  and test every sentence with a round trip through speech recognition.
