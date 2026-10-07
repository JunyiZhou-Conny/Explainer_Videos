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
translated sentence. That lets every scene keep its English `vo.wait_until("...")` anchors (each is
mapped into the matching Chinese sentence: at the Chinese words named in the line's `anchors:` map,
or else at the same relative position as in the English sentence), and it pairs the two lines of
every bilingual subtitle.

All commands below run from the repository root (the toolkit is imported from there).

## Workflow

1. **Glossary first.** Decide, for this audience, which words stay in English and which use the
   standard Chinese term. Ask how a real speaker in that setting talks: a Chinese PhD student
   presenting a DP paper keeps *query*, *trick*, *hybrid argument* and names in English but says
   差分隐私, 敏感度, 拉普拉斯机制; a teacher of 12-year-olds keeps only `explore`, `winner`, `None`,
   Python and X/O, and glosses each once. Write it in `GLOSSARY.md` + `glossary.yaml`.
2. **Translate.** `narration/*.yaml` (one entry per SAY line of `script.md`), `strings/*.yaml` and
   `meta.yaml`. To list every on-screen string (in English: the keys for `strings/*.yaml`) with its
   call site: `python -m explainer.strings videos/<id>` (writes `build/strings.en.json`); with
   `--lang zh` each entry also shows its current translation (`tr`), which finds leftovers.
3. **Check.** `python -m explainer.i18n check videos/<id> --lang zh` (alignment, spoken-text
   hygiene, Latin words not allowed by the glossary). Timing against the English, per SAY block
   (synthesizes and caches all narration): `python -m explainer.script videos/<id>/script.md --lang zh`.
4. **Adapt the scenes.** Per scene: `python -m explainer.preview videos/<id>/scenes/<file> <Class> --lang zh`
   (prints each Chinese sentence with its start time, writes contact sheets) and
   `python -m explainer.check videos/<id>/scenes/<file> <Class> --lang zh`. Typical fixes: glyph indices that
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
   (`EXPLAINER_EDGE_VIA_AZURE=0` opts out). Every scene render is stamped with the narrator it was
   made with (`build/media_*/<scene>/voice.json`), so the next build re-renders scenes made with
   the Edge endpoint. A local Kokoro voice was evaluated too; its Mandarin
   is weaker and it is not wired in.
6. **Review the whole video** (a bilingual reviewer and someone from the target audience), fix,
   and rebuild. `--subs-only` rewrites subtitles, chapters and transcript from existing renders.
7. **Build.** `python -m explainer.build videos/<id> --lang zh --crf 25` → `output/zh/<id>.mp4`
   (1080p60, bilingual subtitles burned in a band under the slightly scaled-down picture;
   `--no-burn` keeps it clean), `<id>.zh.srt`, `<id>.en.srt` (English on the Chinese timing),
   `<id>.zh-en.srt` / `.ass`, `chapters.txt` and `transcript.md`; each part gets its own
   `<id>_<part>.mp4`, subtitle files and `chapters_<part>.txt` (the transcript covers the whole
   video). The English build also writes `<id>.zh.srt` / `<id>.zh-en.srt` / `.ass` for the English
   video.

## Subtitles

Made by `explainer/subtitles.py` from the narration timings recorded while rendering:

- Each sentence is cut into its own cues (no cue runs from the middle of one sentence into the
  next). A cue shorter than 1 s is then merged into the neighbouring cue when they are contiguous
  and the result fits, even across a sentence boundary, and the sentence punctuation stays inside
  it (不是。电脑能做的……). Only the end of a Chinese cue loses its 。，、；： (so that mark does not
  count against the line width either). A Chinese cue still shorter than 0.2 s per character
  (at most 1.5 s) borrows time from a neighbour of the same sentence that has some to spare, but
  past 1 s only while that neighbour still reads slower (这里说的“一局” 1.0 s, not 1.4 s that leave
  the next cue 23 units in 2.1 s). A cue that could not stay 1 s up borrows the missing bit across
  the 0.05 s gap to the next sentence (Why?, 不矛盾 || No.).
- Cues follow the clause structure: a sentence split at ；。！？ keeps one clause per cue when
  those cuts alone fit; among the clause plans of up to two cues more, a Chinese sentence takes
  the one with the fewest run-ons across a mid-line ；。！？, then without a weak comma (a short
  scope phrase 对大多数 mask，, a condition 光凭……，/ 就能……, a gloss, a continuation, a result
  从而……), then the fewest cues (DP-SGD: 对每个样本的梯度做 clip（梯度裁剪） / 就像我们的收入上限，
  从而限制了敏感度 / 加上高斯噪声；并在……); a .zh.srt cue piece must wrap into 2 lines. A cue is
  not cut inside a 、 list (第三，答案不一定是一个数 / 一个排名、一个集合、一个比特串，……) — in the
  band only when the list itself is wider than the 30-unit line (the four authors of the paper:
  2006 年，Cynthia Dwork、Frank McSherry / Kobbi Nissim 和 Adam Smith) — nor inside a 先……再……
  sequence or between a manner adverbial and its verb (一局接一局，/ 把……) when the balance allows.
- Lines break at punctuation whenever the pieces fit, preferring the stronger mark (；：。 over ，,
  and ， over 、, which splits a list) and never leaving a scrap of a few characters at a comma
  (2016 年，/ …); otherwise at the cheapest gap. The costs steer English away from ending a line on
  an article, preposition, auxiliary or possessive, splitting a name (Kobbi / Nissim, McSherry /
  and Talwar's), a list (birth / date and sex; broad, / flexible), an adjective from its noun (its
  published / tables), a glossary term (counting / query) or a phrasal verb (single / out), and
  Chinese away from ending a line on a preposition (从, 把, 在 …), a 的, a negation, a demonstrative
  or a numeral and its measure word (这些 / query, 一个 / counting query), starting one with a
  particle (的, 了 …) or a postposition (以内, 之间 …), breaking inside a word (jieba, with the
  glossary headwords registered: terms only, not the example phrases of zh_subtitle) or inside
  “…” and （…）, cutting off a gloss from its term (hybrid argument（混合论证）, 叫 winner，意思是
  “赢家”), splitting a short clause from the one it continues (想……，又要强隐私，/ 就……), and cutting
  inside a 《…》 title rather than before it. They are costs, not absolute rules; a line with a
  list of Latin names (、 or 和) may run 1.5 units over rather than break the list or leave a scrap
  cue (然后在 2003 年，Irit Dinur 和 Kobbi Nissim / 证明了一个令人警醒的结论). English also avoids
  ending a line one word into a phrase (to measure / sensitivity), on a determiner before its noun
  (call those / made-up endings), before an object pronoun (let / it play) or before the verb of a
  clause whose "that" is left out (proves the first / is → proves / the first is).
- An English cue whose two lines break mid-phrase is re-wrapped at a clean break when one fits
  (Remember the Gaussian / whose ratio…), or at a much cheaper break whatever the balance (It
  founded / what we now call…), else split into two cues at a clause boundary when that gives
  lines that break better or follow the commas (But SuLQ only covered sums, // and its definition
  tolerated / a tiny chance…), not at a weak comma and not into a scrap cue (Trying a path, then
  stepping back / to try the next one, is called backtracking.). An English cue boundary costs more
  than a line break: never after an article, preposition or auxiliary (…just ask // the
  interactive curator), nor inside a list (Frank McSherry, // Kobbi Nissim); before "that" + a
  clause it is clean (…one release // that is accurate). The English video's own .srt
  (build.split_cues, 44 characters) uses the same line breaks (subtitles.wrap_en), and a sentence
  that fits only with a bad break becomes two cues at a comma.
- In the bilingual band (Chinese line ≤ 30 units, a whole 《…》 title ≤ 35; English line ≤ 96
  characters, ≤ 110 for a clause piece — burned at 1080p a 110-character line is about 1170 px of
  the 1840 px line) the English sentence is cut where the Chinese one is: at the nearest clause
  stop that keeps the numbers and symbols on the same side as the Chinese (41 / 42, 1/n, e^ε), has
  about as many clause marks as the Chinese piece, keeps connectives (而且 / and, 但 / yet) on the
  same side and matches a Chinese ：；。 with a strong mark, not at a comma inside a list of names
  or adjectives; failing that, or when that stop is poor, at a gap right at the cut before an
  auxiliary or conjunction (Games that end on move 8 or 9 / have at most…), and in a long sentence
  at a plain gap (also against a stop whose clause marks do not match: Three: Laplace noise with
  scale sensitivity/ε / makes it private, …); if the numbers cannot be put on the right side and
  the sentence fits on one line, the whole sentence stays up under each piece — unless only a
  poor gap would put them right and a stop misplaces just one number (list all 8 winning lines, /
  under 一共 8 条).
- In the English video (timing="en") the band follows the English pieces, but where a Chinese
  piece would read faster than 9 units/s the switch moves (by at most 1 s) toward equal reading
  rates, and a sentence's Chinese may run up to 0.5 s into the next sentence when that one has
  time to spare (没想到吧：答案是边格，也就是每条边正中间的那一格 2.3 s, was 1.3 s). The .zh.srt cues of
  that video switch exactly where the band switches.
- Inside a sentence the Chinese cues are timed by the spoken form (say:, recorded in
  <scene>.subs.json as `tr_say`), so 二零一六年, E 的艾普西隆次方 and a gloss that is not read move
  the cue switches to where the voice is, in the .zh.srt as in the band.
- Sidecar cues have at most 2 lines (22 units per Chinese line, 48 characters per English line);
  short cues stay up 1.6 s when the next one leaves room. Regression tests: tests/test_subtitles.py.

## Lessons from the Chinese versions

- **Anchors drift.** An `anchors:` entry is placed by its character position in the displayed
  Chinese sentence, so spoken forms longer than their display (1/ε → 艾普西隆分之一) make later words
  come early, Latin words (query, Google) make them come late, and a subtitle-only gloss （……）
  makes the words before it come early. A phrase without an entry is placed at its relative
  position in the English sentence, so it drifts wherever the Chinese word order differs. Check
  beats against word times (Whisper) and aim the anchor a little earlier or later.
- **No italics for Chinese.** Pango only slants Hanzi synthetically: set Chinese upright under
  `i18n.active()` where the English uses `slant=ITALIC`. Bold is fine.
- **Punctuation fonts.** The Latin house font comes first in the fallback list. In `Text`, Chinese
  quotes and `……` are drawn from the CJK font automatically (in `MarkupText` or `Paragraph`, set
  that font yourself); `——` stays in the house font (two CJK U+2014 leave a gap). No half-width space next to full-width punctuation (`→“是”`, not `→ “是”`).
- **TeX.** CJK in TeX goes through XeLaTeX + ctex; xeCJK adds no space at the end of `\text{…}`
  before maths, so write it (`\text{答案}\ 0`); no `\quad` after a full-width ：.
- **Say numbers and symbols the way a teacher would** with `say:` (ε → 艾普西隆, 轮到 X 的时候),
  and test every sentence with a round trip through speech recognition.
