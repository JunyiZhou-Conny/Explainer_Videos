# Review lens 4: spoken flow, TTS, translatability

Script: `videos/ac215-l13-training-workflows/script.md` at commit 1d1134b, branch
`claude/ac215-l09-l13-batch`.
Method: all 106 SAY blocks were split with `explainer.voice.split_sentences`, which gives 312
sentences. Each sentence went through `KokoroBackend.phonemize`, the call the renderer makes, with the
current `explainer/lexicon.yaml` spliced in. Every row of the script's "Lexicon candidates" table, and
the names and numbers found in the sweep, were also probed raw with `engine.tokenizer.phonemize(…,
"en-us")`. Proposed entries were checked by monkeypatching `load_lexicon` in a throwaway probe. That
probe re-phonemized all 312 sentences with and without the proposed entries: 51 sentences change, all
for the better, and no other sentence changes. Every rewrite marked "verified" was phonemized clean
with the entries in place. `lexicon.yaml` was not edited, and every proposed IPA character is in
Kokoro's vocab.

Format: `V<n> · S<scene>.<block>.<sentence> · severity (wrong | confusing | polish) · quote · issue ·
concrete rewrite`.

**A new trap, found in this script: a sentence-final "." breaks the last decimal number.** Kokoro's
tokenizer calls `phonemizer.phonemize(…, preserve_punctuation=True)`. phonemizer 3.4.0's
`Punctuation._preserve_line` cuts each chunk with `line.split(mark.mark)`, which splits at the *first*
occurrence of the mark. When the mark is the bare sentence-final ".", that first "." is a decimal point
if the last clause holds a decimal. So "at 68.97 percent." comes out as `sˈɪksti ˈeɪt. nˈaɪnti sˈɛvən
pɚsˈɛnt` ("sixty-eight. Ninety-seven percent"), while "at 68.97 percent, and more." is fine. A decimal
breaks only if its own chunk (the text after the last ", " ": " "; " mark or lexicon key) ends the
sentence. Editing punctuation can therefore move a number in or out of danger, and so can adding a
lexicon key, because a key starts a new chunk. That is why Appendix B keys **every** decimal this
script speaks, not just the 9 that break today. A toolkit fix belongs in its own PR (for example,
phonemize a segment's terminal punctuation separately in `KokoroBackend.phonemize`). Outside this
lens: the same signature appears in 6 sentences of L09 (for example, "…insists on exactly 5.0."). L10,
L11 and the other episodes are clean.

**Splice trap: clean.** No SAY sentence and no proposed rewrite puts "a" or "A" directly before an
existing or proposed key. A regex sweep with all proposed entries added confirmed this. The one "a 403"
(S11.4.3) fires its guard: `ɐ fˈɔːɹ ˈoʊ θɹˈiː`. A related, harmless effect of splicing: a function
word just before a key gets its stressed form ("to wandb config" gives `tuː`, "in task.py" gives
`ˈɪn`). Do not write "notebook A's", because the key would leave a bare "'s" to be read as a letter.

**Homograph sweep.** "project" (×13), "console" (×4), "row", "rows", "invalid", "update" (both noun
and verb), "upload(s)", "used", "logs" and "closed" are all right. There are three misses: the verb
"presents" gets noun stress (V17), the verb "conflicts" gets noun stress (V36), and "replay" gets noun
stress (V37). The verb "export" comes out `ˈɛkspɔːɹt` (S07.7.1, S10.7.3, S15.1.2). For a shell command,
"EX-port" is the normal reading, so this is not a finding.

---

## Findings

### wrong

V1 · S01.1.2, S01.1.3 · **wrong** · "Notebook A crowns the fine-tuned MobileNet, at 68.97 percent." / "…and puts the fine-tuned one at 62.93."
· The hook's own numbers are spoken as two numbers with a stop between them: `sˈɪksti ˈeɪt. nˈaɪnti
sˈɛvən pɚsˈɛnt` ("sixty-eight. Ninety-seven percent") and `sˈɪksti tˈuː. nˈaɪnti θɹˈiː`. The Chinese
cue and the subtitle show 68.97 while the voice says "sixty-eight… ninety-seven". This is the
decimal-split trap above. Only the first 68.97 in S01.1.3 survives, because a comma follows it. · Add
the entries `68.97` and `62.93` (Appendix B). Text unchanged. Verified: `æt sˈɪksti ˈeɪt pɔɪnt nˈaɪn
sˈɛvən pɚsˈɛnt.` and `æt sˈɪksti tˈuː pɔɪnt nˈaɪn θɹˈiː.` The S01 SHOW cue "on 62.93" still finds
its text.

V2 · S03.1.2, S03.6.2, S04.1.2, S09.1.5, S09.2.2, S11.5.2, S13.2.2, S14.2.2 · **wrong** · eight more sentences hit by the same trap
· The voice gives the wrong value in each case:
  - "TensorFlow 2.19.0" becomes `tˈuː. nˈaɪntiːn pɔɪnt zˈiəɹoʊ` ("two. Nineteen point zero").
  - "9.5 percent" becomes "nine. Five percent".
  - "0.22.2" becomes "zero. Twenty-two point two".
  - "2.59 gigabytes" becomes "two. Fifty-nine gigabytes".
  - "0.15.11" becomes `zˈiəɹoʊ. fˈɪftiːn pɔɪnt wˈʌn wˈʌn`, twice ("zero. Fifteen point one one", the
    wandb pin).
  - "8.93" becomes "eight. Ninety-three".
  - "2.17" becomes "two. Seventeen".
  - In S14.2.2, "2.14" is read `tˈuː pɔɪnt wˈʌn fˈɔːɹ` ("two point one four"). That is a different
    style from "two point seventeen" in the same contrast.

· Add the entries `2.19.0`, `9.5`, `0.22.2`, `2.59`, `0.15.11`, `8.93`, `2.17` and `2.14`, plus the
robustness keys `4.31`, `7.61`, `0.86` and `0.001`. Those four are clean today, but the V24/V26 splits
move `7.61` into a breaking position. All 8 sentences were verified clean, for example `zˈiəɹoʊ pɔɪnt
fˈɪftiːn pɔɪnt ɪlˈɛvən.` and `tˈuː pɔɪnt fˈɔːɹtiːn, wˈɛɹ sˌiːˌɛlˈaɪ dˈɑːt ˌɛsˈeɪtʃ jˈuːsᵻz tˈuː pɔɪnt
sˈɛvəntˌiːn.` The key `2.14` cannot change L09's "torch 2.14.1", because the longer existing key
matches first. That was checked.

V3 · S04.1.2, S08.9.1 · **wrong** · "…in our signed-out stand-in, 0.31.0 at the time of recording…" / "…then Python 3.13.17 and uv 0.13.5, at the time of recording."
· This is the splice issue the candidates table predicted, and it is real. The existing key `0.31`
matches inside `0.31.0`, because "." is not a word-boundary character in `_lexicon_regex`. The
leftover ".0" then starts its own chunk with a stop: `zˈiəɹoʊ pɔɪnt θˈɜːɾi wˈʌn.zˈiəɹoʊ` ("zero point
thirty-one. Zero"). The keys `3.13` and `0.13` do the same to `3.13.17` (`θˈɜːtiːn.sˈɛvəntˌiːn`) and
`0.13.5` (`θˈɜːtiːn.fˈaɪv`). · Add the exact-version entries `0.31.0`, `3.13.17` and `0.13.5`. Being
longer, they win over the short keys. Verified: `zˈiəɹoʊ pɔɪnt θˈɜːɾi wˈʌn pɔɪnt zˈiəɹoʊ` and
`θɹˈiː pɔɪnt θˈɜːtiːn pɔɪnt sˈɛvəntˌiːn ænd jˌuːvˈiː zˈiəɹoʊ pɔɪnt θˈɜːtiːn pɔɪnt fˈaɪv`.

### confusing

V4 · S01.1.2, S02.5.2, S03.1.1, S03.7.3, S12.6.6 · confusing · "Notebook A crowns…" / "notebook A fills a folder…" / "Open notebook A from…" / "notebook A wins by two photos." / "…why tables A and B could not be compared…"
· When no comma follows, Kokoro reads the label "A" as the article: `nˈoʊtbʊk ɐ kɹˈaʊnz` ("notebook
uh crowns"), and `tˈeɪbəlz ɐ ænd bˈiː`. The whole hook rests on the contrast between A and B, and the
first line of the video loses the letter. "notebook A, but" (S04.2.1) and "notebook A, so" (S04.8.2)
are fine because of the comma. · Add the multi-word entries `notebook A` and `Notebook A` = `nˈoʊtbʊk
ˈeɪ`. No other episode says either phrase. For S12.6.6, rewrite: "That is exactly why the two tables
could not be compared, and exercise 1 adds a small callback." ("notebooks A and B" also gives `ɐ`.)
All 5 verified.

V5 · S07.2.3, S10.1.1, S10.3.1, S12.6.2, S14.2.2, S15.1.2 · confusing · "…cli.sh runs on CPU today…" / "Review cli.sh…" / "Now sh cli.sh…"
· `cli.sh` comes out as `klˈaɪ.ˌɛsˈeɪtʃ`: "cly", a full stop, then "S H". This is the episode's main
command, spoken 7 times, and the literal "." is a pause, the same issue L11 V2 fixed. The candidates
table expected "C L I dot S H", like the existing `cli.py`. · Add the entry `cli.sh`. No other episode
says it. Verified: `sˌiːˌɛlˈaɪ dˈɑːt ˌɛsˈeɪtʃ`.

V6 · S07.4.1, S09.2.1, S09.3.1, S09.4.1, S09.4.3, S09.6.2, S11.8.2, S12.4.3, S14.2.1, S14.7.2 · confusing · the other dotted names
· Each one jams together and has a literal stop:
  - `setup.py` becomes `sˈɛɾʌp.pˈaɪ`.
  - `task.py` becomes `tˈæsk.pˈaɪ`.
  - `model-trainer.json` becomes `mˈɑːdəltɹˈeɪnɚ.dʒˈeɪsˈɑːn`.
  - `package-trainer.sh` becomes `pˈækɪdʒtɹˈeɪnɚ.ˌɛsˈeɪtʃ`.
  - `cli-multi-gpu.sh` becomes `klˈaɪmˈʌltaɪdʒˌiːpˌiːjˈuː.ˌɛsˈeɪtʃ` ("cly-multi-GPU. S H").
  - `cheese-app-trainer.tar.gz` becomes `tʃˈiːzˈæptɹˈeɪnɚ.tˈɑːɹ.dʒˌiːzˈiː`, with two stops.

· Add the six entries (Appendix B). None of them occurs in another episode's SAY. All ten sentences
were verified, for example `sˌiːˌɛlˈaɪ mˈʌlti dʒˌiːpˌiːjˈuː dˈɑːt ˌɛsˈeɪtʃ`.

V7 · S07.6.2, S08.3.2, S08.4.2 · confusing · "…our placeholder returns 404, it exists nowhere, while the README's name returns 401…"
· `404` comes out as `fˈɔːɹhˈʌndɹɪd fˈɔːɹ` ("four hundred four"), while the existing `401` and `403`
entries say "four oh one" and "four oh three". S07.6.2 contrasts 404 with 401 in a single sentence,
so the two readings jar. · Add the entry `"404"` = "four oh four". No other episode says 404. No SAY
has "a 404", so no guard is needed now. Add `a 404` and `A 404` only if a later edit writes one.
Verified in all 3 sentences.

V8 · S10.3.2 · confusing · "The first line is real: the Vertex AI endpoint in us-central1."
· This comes out as `ˌʌssˈɛntɹəl wˈʌn`, "us-central one", with "us" read as the pronoun. The region
name is the one real line the viewer sees succeed. · Add the entry `us-central1` = "U S central one",
which matches the existing `us-east-1`. Verified: `ˈɪn jˌuːˈɛs sˈɛntɹəl wˈʌn`.

V9 · S04.4.2, S04.6.3, S04.7.1, S05.1.2, S05.2.2, S05.4.2 (×2), S05.5.2, S05.7.1, S09.2.2, S11.5.2, S11.6.1, S11.8.1, S15.4.1 · confusing · "…with wandb init…" / "…wandb, pinned to…" / "this old wandb pin…"
· `wandb` comes out as `wˈændˌiːbiː` ("WAND-ee-bee"). The Conventions say the library is spoken "W
and B", so the voice and the convention disagree in 14 places. The ear hears an unknown word right
beside "W and B". · Add the entry `wandb` = `dˈʌbəljˌuː ænd bˈiː`. No other episode's SAY contains
"wandb", so a single-word key is safe. All 14 were verified, for example `stˈɑːɹt ðə ɹˈʌn wɪð
dˈʌbəljˌuː ænd bˈiː ɪnɪt.`

V10 · S09.1.3 · confusing · "…with Cloud SDK 590.0.0 and the Vertex AI library 1.120.0…"
· `1.120.0` comes out as `wˈʌn pɔɪnt wˈʌn tˈuː zˈiəɹoʊpɔɪnt zˈiəɹoʊ` ("one point one two zero-point
zero"), and `590.0.0` as "five hundred ninety point zero-point zero". The candidates table asks for
"one point one twenty point zero" and "five ninety point zero point zero". · Add the entries
`590.0.0` and `1.120.0`. The sentence also gets split (V27). Verified.

V11 · S13.1.5, S14.2.2, S14.7.1 · confusing · "And the quota: T4s for custom training in this region."
· `T4s` comes out as `tˈiː fˈɔːɹ z`: "T four", then a bare buzzing "z" as its own word. · Add the
entry `T4s` = `tˈiː fˈɔːɹz` ("T fours"). No other episode says it. Verified in all 3.

V12 · S15.2.2 · confusing · "…nothing calls model save, and the model dir flag is ignored."
· "dir" comes out as `dˈaɪɚ` ("dyer"), so the viewer hears "model dyer flag". This is the same issue
as L11's "implicit dirs". · Add the multi-word entry `model dir` = `mˈɑːdəl dˈɜː` ("model dur"). A
bare `dir` key is not needed. Verified.

V13 · S07 (fifth SHOW/SAY) · confusing · SHOW: "On "a source we name", two GREY chips settle under it"
· S07.5's SAY says "successes come from named sources", not "a source we name", so this cue cannot
fire. · Re-anchor the SHOW on "named sources" (0 words). This is the recommended fix, because S07 is
at 332 words against a cap of 333. The SAY alternative "…, and every success comes from a source we
name." (verified, +3) would push S07 over the cap.

V14 · S08 (fourth SHOW/SAY) · confusing · SHOW: "on "before docker run", CODE chip `set -e` flashes"
· The SAY has "The script's set dash e then skips docker run.", so the cue phrase is absent. · "The
script's set dash e then stops it before docker run." (Verified, +2.)

V15 · S05.6.1 · confusing · "And run save with the word test uploads files that match test; it does not save the run."
· Garden path: "And run save…" opens like an instruction to the viewer ("and run save"), and the
listener only finds the real verb at "uploads". A Chinese line cannot keep the ambiguity. · "The call
run save, with the word test, uploads the files that match test; it does not save the run."
(Verified, +2.)

V16 · S11.8.2 · confusing · "We could not check the key format W and B issues today, so if your key has a different length, raise the pin in setup.py."
· Garden path: "the key format W and B issues" is heard with "issues" as a noun ("W and B issues",
meaning problems). The sentence is also 25 words long. · "We could not check which key format W and
B gives out today. If your key has a different length, raise the pin in setup.py." (Verified, 0
words.)

V17 · S10.2.2 · confusing · "A small slip: the README presents GPU first and CPU as optional…"
· The verb "presents" gets noun stress (`pɹˈɛzənts`, "PREsents", as in gifts). · "A small slip: the
README shows GPU first and CPU as optional, but the script already runs on CPU." (Verified.)

V18 · S15.4.1 · confusing · "The whole lecture on one map: a folder of runs, runs on a shared axis, config passed to wandb init, a tarball that travels while your image stays home, a key inside one command, three badges, three switches, and two GPUs in step."
· At 43 words, this is the longest sentence in the script: an eight-item list with no verb. The SHOW
relights one piece per item, and a single subtitle cue would hold all eight. · "The whole lecture on
one map. A folder of runs, then runs on a shared axis. Config passed to wandb init. A tarball that
travels while your image stays home, and a key inside one command. Three badges, three switches, and
two GPUs in step." (Verified, 5 sentences of 6/10/5/15/9 words, +2.)

V19 · S14.3.2 · confusing · "It makes the three changes of the lecture: it creates the mirrored strategy, multiplies the batch size by the number of replicas, here GPUs, not machines, and builds and compiles the model inside the scope of the strategy."
· At 38 words, this sentence holds all three of the lecture's call-outs (BLUE, GREEN, RED). The
nested "here GPUs, not machines" sits between two commas inside a list. · "It makes the three changes
of the lecture. It creates the mirrored strategy. It multiplies the batch size by the number of
replicas, which here means GPUs, not machines. And it builds and compiles the model inside the scope
of the strategy." (Verified, +4. There is one sentence per call-out.)

V20 · S14.4.3 · confusing · "A global batch of 64 splits into two halves of 32; each GPU computes gradients on its half, the two are averaged across a link called all-reduce, and both copies take the same step, so they stay identical."
· At 38 words, this is the V7 mechanism sentence: split, compute, all-reduce, step. It has four
animation beats in one cue. · "A global batch of 64 splits into two halves of 32. Each GPU computes
gradients on its half. The two are averaged across a link called all-reduce, and both copies take the
same step, so they stay identical." (Verified, 0 words.)

V21 · S04.7.1 · confusing · "Two more things: both MobileNet runs show the same name, so tell them apart by run ID, and no cell finishes the last run, so add wandb finish after cell 52; that one is an extra."
· 36 words, with two unrelated instructions and two "so" clauses. · "Two more things. Both MobileNet
runs show the same name, so tell them apart by run ID. And no cell finishes the last run, so add
wandb finish after cell 52; that one is an extra." (Verified, 0 words.)

V22 · S07.5.2 · confusing · "This recording machine has no Google credentials, no W and B account, no GPU and no browser, and the key in that listing is an obviously invalid stand-in, moved out before the container starts."
· 34 words. The SHOW's honest card has "three lines building on their sentences", but the block has
only two content sentences, so line 2 cannot get its own cue. · "This recording machine has no Google
credentials, no W and B account, no GPU and no browser. The key in that listing is an obviously
invalid stand-in, moved out before the container starts." (Verified, −1 word.) The card's three lines
then map to S07.5.2a, S07.5.2b and S07.5.3.

V23 · S10.1.2 · confusing · "It names the job with random hex, asks for one n1-standard-4 machine, sets a GPU image, points at your package and module, and builds the arguments, ending with your W and B key."
· 33 words, a six-step list over a 12-line scrolling window. · "It names the job with random hex,
asks for one n1-standard-4 machine, and sets a GPU image. Then it points at your package and module,
and builds the arguments, ending with your W and B key." (Verified, +3.)

V24 · S13.2.2 · confusing · "An extra check shows the prebuilt images are still served, at the time of recording: the CPU image at 4.31 gigabytes compressed, and two GPU images at 8.93 and 7.61."
· 30 words and three sizes. "8.93" is broken by the decimal trap (V2), and "two GPU images at 8.93
and 7.61" omits the unit. · "An extra check shows the prebuilt images are still served, at the time
of recording. The CPU image is 4.31 gigabytes compressed, and the two GPU images are 8.93 and 7.61."
(Verified with the V2 keys, +1.) Without the `7.61` key, this split would break "7.61" instead.

V25 · S06.3.1 · confusing · "Step one: move the notebook code into a Python file and turn its hard-coded choices into flags: epochs, batch size and model name, plus train base and your W and B key."
· 32 words with two colons. The second colon's list is heard as part of "flags: epochs…" only after
the fact. · "Step one: move the notebook code into a Python file, and turn its hard-coded choices
into flags. The flags are epochs, batch size and model name, plus train base and your W and B key."
(Verified, +3.)

V26 · S04.1.2 · confusing · "Its first cell installs it, and the dash U flag means whatever is newest: in our signed-out stand-in, 0.31.0 at the time of recording, while the stored run used 0.22.2."
· 30 words. Both versions are mangled (V2, V3), and the clause after the colon has no verb. · "Its
first cell installs it, and the dash U flag means whatever is newest. In our signed-out stand-in that
is 0.31.0, at the time of recording, while the stored run used 0.22.2." (Verified with the keys, +2.)

V27 · S09.1.3 · confusing · "Project, bucket and key came through, and gcloud, gsutil and uv are here, with Cloud SDK 590.0.0 and the Vertex AI library 1.120.0, at the time of recording."
· 28 words: three tool names, then two long version strings in one breath. · "Project, bucket and
key came through, and gcloud, gsutil and uv are here. At the time of recording, that is Cloud SDK
590.0.0 and the Vertex AI library 1.120.0." (Verified with the V10 keys, +1.)

### polish

V28 · S09.2.4, S09.4.2, S09.1.3, S11.6.1 · polish · "gsutil" / "scikit-learn"
· `gsutil` comes out as `dʒˈiːsˈuːɾɪl` ("gee-SOO-til"), where the table asks for "G S util".
`scikit-learn` comes out as `sˈɪkɪtlˈɜːn` ("SICK-it-learn"), where the table asks for "sy-kit learn",
the project's own reading. · Optional entries `gsutil` = `dʒˌiːˈɛs jˈuːtɪl` and `scikit-learn` =
`sˈaɪkɪt lˈɜːn`. No other episode says either. Verified in all 4.

V29 · S01.4.2, S10.8.1 · polish · "Vertex AI jobs bill while they run…" / "…the job's machine bills your project."
· The verb "bill" sounds like the name Bill (L10 V10, L11 V50). · "Vertex AI jobs cost money while
they run; gold tags mark each point, without amounts." (+1) / "A gold tag: from submission until the
script exits, your project pays for the job's machine." (+1) (Both verified.) The noun "the bill"
(S13.5.1) and "still billed" (S13.7.2) are fine.

V30 · S04.8.4 · polish · "…yours will say cheese."
· "say cheese" is the photo idiom, and Chinese gets either a literal "说奶酪" or a pun it cannot carry.
· "The lecture's dashboard comes from an earlier project; yours will show the cheese project."
(Verified, +2.)

V31 · S04.8.2 · polish · "…the fine-tuned MobileNet trained 10 here and 15 in notebook A…"
· The unit is missing ("10 what?"), and the Chinese line needs it (10 个 epoch). · "…trained 10 epochs
here and 15 in notebook A, so it is not a fair comparison." (Verified, +1.)

V32 · S03.2.3, S03.4.2 · polish · "…936 for training, 104 for validation, 116 for testing." / "…is 104 for validation."
· "104 for" gives `wˈʌnhˈʌndɹɪd fˈɔːɹ fɔːɹ` ("one hundred four for"), a stutter that hits right on a
count the ponder asks about. · "Then the split: 936 to train on, 104 to validate, and 116 to test."
(+2) / "…then 10 percent of the remaining 1,040 is 104, the validation set." (+1) (Both verified.)

V33 · S03.6.2 · polish · "…9.5 percent would rank above 68."
· A bare "68" after "9.5 percent" is heard as a different quantity. · "…9.5 percent would rank above
68 percent." (Verified with the `9.5` key, +1.)

V34 · S05.7.3 · polish · "…exercise 1 puts a callback back."
· "callback back" stutters, and "put … back" is a phrasal verb. · "…exercise 1 adds the callback
again." (Verified, 0 words.)

V35 · S06.4.2 · polish · "Step three runs from what the lecture calls the Model Trainer CLI Container, on your laptop, which asks Vertex AI for a job."
· "which" could attach to the laptop or the container, and Chinese has to choose. · "Step three runs
from what the lecture calls the Model Trainer CLI Container. It sits on your laptop and asks Vertex
AI for a job." (Verified, +2.)

V36 · S10.7.3 · polish · "…exit any old cockpit first, or the name conflicts."
· The verb "conflicts" gets noun stress (`kˈɑːnflɪkts`), and "the name conflicts" is terse. · "Exit,
export, and start again; exit any old cockpit first, or its name is still taken." (Verified, +2.)

V37 · S11.5.1 · polish · "…so we replay the job's first step on the laptop…"
· The verb "replay" gets noun stress (`ɹˈiːpleɪ`). · "…so we rerun the job's first step on the laptop,
tagged as a stand-in." This uses the existing `rerun` entry (`ɹˌiːɹˈʌn`). (Verified, 0 words.)

V38 · S12.4.2 · polish · "Kindly put, not with this code."
· The inverted idiom is odd to the ear and is translated word by word. · "To put it kindly: not with
this code." (Verified, +2.)

V39 · S09.1.2 · polish · "Slash secrets is empty, our sandbox."
· The appositive "our sandbox" has nothing to attach to. · "Slash secrets is empty here, in our
sandbox." (Verified, +2.)

V40 · S08.9.2 · polish · "A small slip: activated is printed before the activation, a label, not a fact."
· "activated is printed" is heard with "activated" as an adjective, not as the quoted word. · "A
small slip: the banner prints activated before anything is activated; it is a label, not a fact."
(Verified, +4.)

V41 · S08.8.4, S10.6.1 · polish · "…since the entrypoint has no set dash e." / "Anyone who can view jobs in this project, since the job spec keeps its arguments, plus your shell history if typed inline."
· "since" can be causal or temporal, a common Chinese alignment trap (L11 V38). "if typed inline" has
no subject. · "…because the entrypoint has no set dash e." (0) / "Anyone who can view jobs in this
project, because the job spec keeps its arguments. Also your shell history, if you typed the key
inline." (+3) (Both verified.)

V42 · S10.3.3 · polish · "Then it stops with no active account, the key that never loaded…"
· The appositive equates "account" with "key". · "Then it stops with no active account, because the
key never loaded; an extra auth list confirms it." (Verified, 0 words.)

V43 · S11.7.2, S11.7.3 · polish · "The empty key from scene 10 fails, api key not configured, and…" / "The default of 16 fails: API key must be 40 characters long, yours was 2."
· Quoted error text dropped in mid-sentence reads as the narrator's own words ("yours was 2"
addresses the viewer). · "The empty key from scene 10 fails with api key not configured, and on
Vertex that comes after the paid data download." (+1) / "The default of 16 fails, and the error says:
API key must be 40 characters long, yours was 2." (+4) (Both verified.)

V44 · S12.3.3 · polish · "…with no epochs, loss or times, then training job complete."
· The log line is heard as a statement ("then training [is] complete"). · "…, then the line training
job complete." (Verified, +2.)

V45 · S02.1.2 · polish · "Today pulls the third one: you rent hardware."
· "Today" as the subject of "pulls" is unusual and translates literally. · "Today we pull the third
one: you rent hardware." (Verified, +1.)

V46 · eighteen sentences of 25 to 30 words · polish · each one joins two ideas, and the Chinese line would carry both
· Every rewrite below was verified with the Appendix B keys. The word change is in brackets.
  - S03.7.2 (29) "The folder keeps settings and scores, but not which 116 photos were the test set. The
    split has no seed, so every run is graded on a different 116." [0]
  - S08.2.1 (29) "A small slip: the README's copy of this script is not the real file. It has notes in
    brackets and an older line for Apple chips, so edit the script itself." [+2]
  - S01.4.1 (28) "To follow along, you need two Colab copies with a free T4 GPU, and a free account on
    W and B. You also need Docker, and a Google Cloud project with billing." [+4]
  - S07.4.1 (28) "Then the identity: a service account called model trainer, with Storage Admin, AI
    Platform Admin and Vertex AI Administrator. Save one JSON key for it in secrets, as
    model-trainer.json." [+1]
  - S10.4.3 (28) "Then the full command: the worker pool spec with machine, replica count, image and
    module. Last come the arguments, ending with your W and B key in plain text." [+1]
  - S14.6.2 (28) "Two caveats. The learning rate stays at 0.001 while the batch doubles. And two GPUs
    are not twice as fast, because start-up, image pull and download don't shrink." [0]
  - S05.7.2 (27) "But the middle line is gone. One commit in October 2025 removed the callback,
    without saying why, 51 minutes after the image moved to a newer TensorFlow." [0]
  - S05.5.1 (26) "Here is the proof, on today's W and B in offline mode, as our stand-in. The name
    points at a plain dict, and the run's config is empty." [+2]
  - S10.7.2 (26) "Inside, its length is 0, and the arguments end with an empty key. So the job would
    download its data, and only then fail at login." [0]
  - S04.2.1 (25) "…about 510 megabytes you never use. You may delete that line." [0]
  - S08.3.2 (25) "Today it fails at step 2 of 14. All 22 packages return 404 Not Found from the Debian
    mirror, and the build stops at line 18." [+1]
  - S11.6.1 (25) "…but no TensorFlow and no scikit-learn. Those come from the prebuilt image Google
    still serves." [0]
  - S12.4.1 (25) "To view metrics, the README sends you to the W and B project cheese training vertex
    AI. It promises training metrics, tracked and updated automatically." [0]
  - S14.2.2 (25) "It asks for one n1-standard-32 machine with two T4s, for 5 epochs. A small slip: its
    TensorFlow image is older, 2.14, where cli.sh uses 2.17." [0] This also takes the mid-list
    "a small slip" out of its parentheses.
  - S15.1.2 (25) "As an extra run, it fails at once, because only cli.sh sets the region variable.
    Export that variable, and it fails at the missing key file." [+1]
  - S11.8.2 is covered by V16, S06.4.2 by V35, and S10.6.1 by V41.

---

## Long sentences (≥ 25 words), status

28 of 312 sentences reach 25 words. All of them have a split above except two: S02.5.3 (25) and S03.5.3
(25). Both are lists of short parallel clauses that the SHOW flashes piece by piece, so they read
well and are left as they are. Ranked: S15.4.1 43 (V18), S14.3.2 38 (V19), S14.4.3 38 (V20), S04.7.1
36 (V21), S07.5.2 34 (V22), S10.1.2 33 (V23), S06.3.1 32 (V25), S04.1.2 30 (V26), S13.2.2 30 (V24),
S03.7.2 29, S08.2.1 29, S01.4.1 28, S07.4.1 28, S09.1.3 28 (V27), S10.4.3 28, S14.6.2 28, S05.7.2 27,
S05.5.1 26, S10.7.2 26, and S04.2.1, S08.3.2, S11.6.1, S11.8.2 (V16), S12.4.1, S14.2.2, S15.1.2 at
25 (V46). With all splits applied, the longest remaining sentences are the two 25-word lists and
seven untouched 24-word sentences (S01.3.2, S04.6.2, S08.5.2, S09.2.3, S09.3.3, S14.1.1, S15.2.2).
That is acceptable.

Word budget, with every rewrite applied and the V13 SHOW re-anchor (not the SAY alternative): about
+58 words, from 4,239 to about 4,297. Per scene, against the BRIEF cap of +15 %:

| scene | now | after | cap |
| --- | --- | --- | --- |
| S01 | 218 | 223 | 253 |
| S03 | 304 | 308 | 322 |
| S04 | 305 | 310 | 333 |
| S06 | 246 | 251 | 287 |
| S07 | 332 | 332 | 333 |
| S08 | 342 | 351 | 391 |
| S10 | 323 | 333 | 356 |
| S12 | 267 | 270 | 333 |
| S14 | 326 | 330 | 345 |
| S15 | 292 | 295 | 310 |

All other scenes change by 1 to 4 words. **S07 is the tight one**: it has a margin of one word, which
is why V13 re-anchors the SHOW rather than lengthening the SAY. Re-run `python -m explainer.script`
after edits.

## Anchors (SHOW phrases that the SAY must contain)

| SHOW anchor | SAY sentence | status |
| --- | --- | --- |
| S01 "62.93" | S01.1.3, last word | ok; spoken right only with the V1 key |
| S01 "look at the epochs column" | S01.2.3 | ok |
| S01 "two words" | S01.4.4 | ok |
| S02 "the third", "bookkeeping" | S02.1.2, S02.1.3 | ok; V45 keeps "the third" |
| S05 "moves the name" | S05.4.3 | ok |
| S07 "a source we name" | **absent** ("named sources") | V13 |
| S08 "before docker run" | **absent** ("skips docker run") | V14 |
| S13 "all three" | S13.1.6 | ok |
| S07 honest card, three lines on three sentences | S07.5.2, only 2 content sentences | V22 split |
| S14 lecture call-outs BLUE, GREEN and RED | S14.3.2, all in one 38-word sentence | V19 split |
| S14 V7 split, compute, all-reduce, step | S14.4.3, 38 words | V20 split |
| S15 V1 relight, one piece per item | S15.4.1, 8 items in 43 words | V18 split |

## Translatability notes (no extra findings)

The episode's metaphors match their visuals and render cleanly in Chinese: ledger (账本), drawer
(抽屉), sticky label (标签), badge and lanyard (工牌), building (大楼), cockpit (驾驶舱), parcel or
tarball trip, switches (开关) and replicas (副本). Questions are short and standalone. The answers
open with their key word ("A callback.", "Zero:", "Only the package script.", "Two:"). Idioms that
remain and are acceptable are "hold that question", "carries on", "in step", "goes wrong" and "a
small slip" (a deliberate series phrase). The script keeps its promises: no "read", "live", "close",
"lead", "content", "object", "record(s)" or singular "minute", and "shut down" instead of "teardown".
"the FROM line" (S08.5.1) comes out with the weak `fɹʌm`, exactly as in L02 and L03 (6 SAY uses). A
stressed `FROM` key would change those episodes, so it is left alone. "October 2025" (S05.7.2) is read
"two thousand twenty-five", consistent with the series, since L11's optional `October 2025` key was
not adopted.

---

## Appendix A: lexicon candidates, probed

"Raw" is the isolated `tokenizer.phonemize(w, "en-us")`. "In context" is `KokoroBackend.phonemize` on
the script's own sentence. Cross-video collisions were checked with the splicer's own boundary regex
over every other episode's SAY lines. No proposed key occurs in another episode, except `2.14`,
which appears only inside L09's "2.14.1". That string already has its own longer key, so it is
unaffected.

| word | raw / in context | verdict | entry |
| --- | --- | --- | --- |
| TensorFlow | `tˈɛnsɚ flˈoʊ` | ok | none |
| MobileNet | `mˈoʊbəl nˈɛt` | ok | none |
| wandb | `wˈændˌiːbiː` ("WAND-ee-bee") | **needs entry** (V9) | yes |
| W and B | `dˈʌbəljˌuː ænd bˈiː` | ok | none |
| Weights and Biases | `wˈeɪts ænd bˈaɪəsᵻz` | ok | none |
| Vertex AI | `vˈɜːtɛks ˌeɪˈaɪ` | ok | none |
| gcloud | `dʒˈiːklˈaʊd` | ok | none |
| gsutil | `dʒˈiːsˈuːɾɪl` ("gee-SOO-til") | optional (V28) | yes (optional) |
| uv | `jˌuːvˈiː` | ok | none |
| google-cloud-sdk / -cli | existing L11 entries fire | ok | none |
| apt, sed, Tar, dict, hex | `ˈæpt`, `sˈɛd`, `tˈɑːɹ`, `dˈɪkt`, `hˈɛks` | ok | none |
| FROM | `fɹʌm` (weak) | series-consistent (L02, L03) | none |
| Bullseye, bookworm, Debian | `bˈʊlsaɪ`, `bˈʊkwɜːm`, `dˈɛbiən` | ok | none |
| Dockerfile | `dˈɑːkɚfˌaɪl` | ok | none |
| Kubernetes | `kˌuːbɚnˈɛɾiːz` | ok | none |
| amd64 | `ˌeɪˌɛmdˈiː sˈɪksti fˈɔːɹ` | ok | none |
| x86 64 | `ˈɛks ˈeɪɾi sˈɪks sˈɪksti fˈɔːɹ` | ok | none |
| sh, ps | `ˌɛsˈeɪtʃ`, `pˌiːˈɛs` | ok | none |
| task.py | `tˈæsk.pˈaɪ` (literal stop) | **needs entry** (V6) | yes |
| setup.py | `sˈɛɾʌp.pˈaɪ` (literal stop) | **needs entry** (V6) | yes |
| cli.sh | `klˈaɪ.ˌɛsˈeɪtʃ` ("cly. S H") | **needs entry** (V5) | yes |
| package-trainer.sh | `pˈækɪdʒtɹˈeɪnɚ.ˌɛsˈeɪtʃ` | **needs entry** (V6) | yes |
| cli-multi-gpu.sh | `klˈaɪmˈʌltaɪdʒˌiːpˌiːjˈuː.ˌɛsˈeɪtʃ` | **needs entry** (V6) | yes |
| model-trainer.json | `mˈɑːdəltɹˈeɪnɚ.dʒˈeɪsˈɑːn` | **needs entry** (V6) | yes |
| cheese-app-trainer.tar.gz | `tʃˈiːzˈæptɹˈeɪnɚ.tˈɑːɹ.dʒˌiːzˈiː` | **needs entry** (V6) | yes |
| JSON, api, ID | `dʒˈeɪsˈɑːn`, `ˌeɪpˌiːˈaɪ`, `aɪdˈiː` | ok | none |
| scikit-learn | `sˈɪkɪtlˈɜːn` ("SICK-it") | optional (V28) | yes (optional) |
| MLflow | `ˈɛm ˈɛlflˈoʊ` | ok ("M L flow") | none |
| init | `ɪnɪt` | ok ("in-it") | none |
| T4 / T4s | `tˈiː fˈɔːɹ` / `tˈiː fˈɔːɹ z` (bare "z") | T4s **needs entry** (V11) | yes |
| n1-standard-4 / -32 | `ˈɛn wˈʌnstˈændɚd fˈɔːɹ` / `… θˈɜːɾi tˈuː` | ok | none |
| us-central1 | `ˌʌssˈɛntɹəl wˈʌn` ("us central") | **needs entry** (V8) | yes |
| all-reduce | `ˈɔːlɹᵻdˈuːs` | ok | none |
| Unix, GitHub, Workbench, Cheese App | `jˈuːnɪks`, `ɡˈɪt hˈʌb`, `wˈɜːkbɛntʃ`, `tʃˈiːz ˈæp` | ok | none |
| 404 | `fˈɔːɹhˈʌndɹɪd fˈɔːɹ` | **needs entry** (V7) | yes |
| 2.19.0 | raw `tˈuː pɔɪnt wˈʌn nˈaɪnpɔɪnt zˈiəɹoʊ`; in context `tˈuː. nˈaɪntiːn…` | **needs entry** (V2) | yes |
| 0.31.0 | in context `…θˈɜːɾi wˈʌn.zˈiəɹoʊ` (the `0.31` key splices inside) | **needs entry** (V3) | yes |
| 0.22.2 | in context `zˈiəɹoʊ. twˈɛnti tˈuː pɔɪnt tˈuː` | **needs entry** (V2) | yes |
| 0.15.11 | in context `zˈiəɹoʊ. fˈɪftiːn pɔɪnt wˈʌn wˈʌn` (×2) | **needs entry** (V2) | yes |
| 3.13.17 | in context `…θˈɜːtiːn.sˈɛvəntˌiːn` (the `3.13` key splices inside) | **needs entry** (V3) | yes |
| 0.13.5 | in context `…θˈɜːtiːn.fˈaɪv` (the `0.13` key splices inside) | **needs entry** (V3) | yes |
| 590.0.0 | `fˈaɪvhˈʌndɹɪd nˈaɪnti pɔɪnt zˈiəɹoʊpɔɪnt zˈiəɹoʊ` | **needs entry** (V10) | yes |
| 1.120.0 | `wˈʌn pɔɪnt wˈʌn tˈuː zˈiəɹoʊpɔɪnt zˈiəɹoʊ` | **needs entry** (V10) | yes |
| 2.14, 2.17 | `tˈuː pɔɪnt wˈʌn fˈɔːɹ`; 2.17 in context `tˈuː. sˈɛvəntˌiːn` | **needs entries** (V2) | yes |
| 3.10 (existing) | fires in "Python 3.10 container": `θɹˈiː pɔɪnt tˈɛn` | ok | none |
| 68.97, 62.93 | in context `sˈɪksti ˈeɪt. nˈaɪnti sˈɛvən`, `sˈɪksti tˈuː. nˈaɪnti θɹˈiː` | **needs entries** (V1) | yes |
| 9.5, 2.59, 8.93 | in context "nine. five", "two. fifty-nine", "eight. ninety-three" | **needs entries** (V2) | yes |
| 0.86, 0.2, 0.001, 4.31, 7.61 | clean in context today | robustness keys for 0.86, 0.001, 4.31, 7.61; `0.2` not needed | yes (4) |
| 1,156, 1,040, 4,016 | spelled out in full, correct | ok | none |
| 936, 104, 116, 510 | correct; "104 for" stutters (V32) | fix by rewrite | none |
| notebook A, tables A | `nˈoʊtbʊk ɐ` (article) unless a comma follows | **needs entry** (V4) + rewrite | yes |
| model dir | `mˈɑːdəl dˈaɪɚ` ("dyer") | **needs entry** (V12), multi-word | yes |
| presents, conflicts, replay (verbs) | noun stress | fix by rewrite (V17, V36, V37) | none |
| "a 403" (existing guard) | `ɐ fˈɔːɹ ˈoʊ θɹˈiː` | ok | none |
| docker-shell.sh, cli.py, uv.lock, pyproject.toml, Colab, CUDA, README's, entrypoint (existing) | all fire correctly | ok | none |

## Appendix B: ready-to-paste lexicon block

Every IPA character below was checked against `engine.tokenizer.vocab`. Every entry was verified in its
script sentences with `load_lexicon` monkeypatched, and all 312 sentences were re-run: 51 change, all
for the better. The required block holds 33 keys, and the optional block holds 2. Paste it under a new
`# AC215 L13` heading. Keys are whole-word and case-sensitive. `notebook A`, `Notebook A` and `model
dir` are deliberately multi-word. The exact versions `0.31.0`, `3.13.17` and `0.13.5` must be added
together with the existing short keys, because the longer key wins.

```yaml
# AC215 L13 (videos/ac215-l13-training-workflows); verified against Kokoro af_heart phonemes.
# Every spoken decimal is keyed: phonemizer splits a sentence-final chunk at its first "." (decimal point).
"0.31.0": {ipa: "zˈiəɹoʊ pɔɪnt θˈɜːɾi wˈʌn pɔɪnt zˈiəɹoʊ", say: "zero point thirty-one point zero"}
"0.22.2": {ipa: "zˈiəɹoʊ pɔɪnt twˈɛnti tˈuː pɔɪnt tˈuː", say: "zero point twenty-two point two"}
"2.19.0": {ipa: "tˈuː pɔɪnt nˈaɪntiːn pɔɪnt zˈiəɹoʊ", say: "two point nineteen point zero"}
"0.15.11": {ipa: "zˈiəɹoʊ pɔɪnt fˈɪftiːn pɔɪnt ɪlˈɛvən", say: "zero point fifteen point eleven"}
"3.13.17": {ipa: "θɹˈiː pɔɪnt θˈɜːtiːn pɔɪnt sˈɛvəntˌiːn", say: "three point thirteen point seventeen"}
"0.13.5": {ipa: "zˈiəɹoʊ pɔɪnt θˈɜːtiːn pɔɪnt fˈaɪv", say: "zero point thirteen point five"}
"590.0.0": {ipa: "fˈaɪv nˈaɪnti pɔɪnt zˈiəɹoʊ pɔɪnt zˈiəɹoʊ", say: "five ninety point zero point zero"}
"1.120.0": {ipa: "wˈʌn pɔɪnt wˈʌn twˈɛnti pɔɪnt zˈiəɹoʊ", say: "one point one twenty point zero"}
"2.14": {ipa: "tˈuː pɔɪnt fˈɔːɹtiːn", say: "two point fourteen"}
"2.17": {ipa: "tˈuː pɔɪnt sˈɛvəntˌiːn", say: "two point seventeen"}
"68.97": {ipa: "sˈɪksti ˈeɪt pɔɪnt nˈaɪn sˈɛvən", say: "sixty-eight point nine seven"}
"62.93": {ipa: "sˈɪksti tˈuː pɔɪnt nˈaɪn θɹˈiː", say: "sixty-two point nine three"}
"9.5": {ipa: "nˈaɪn pɔɪnt fˈaɪv", say: "nine point five"}
"2.59": {ipa: "tˈuː pɔɪnt fˈaɪv nˈaɪn", say: "two point five nine"}
"8.93": {ipa: "ˈeɪt pɔɪnt nˈaɪn θɹˈiː", say: "eight point nine three"}
"4.31": {ipa: "fˈɔːɹ pɔɪnt θɹˈiː wˈʌn", say: "four point three one"}
"7.61": {ipa: "sˈɛvən pɔɪnt sˈɪks wˈʌn", say: "seven point six one"}
"0.86": {ipa: "zˈiəɹoʊ pɔɪnt ˈeɪt sˈɪks", say: "zero point eight six"}
"0.001": {ipa: "zˈiəɹoʊ pɔɪnt zˈiəɹoʊ zˈiəɹoʊ wˈʌn", say: "zero point zero zero one"}
"404": {ipa: "fˈɔːɹ ˈoʊ fˈɔːɹ", say: "four oh four"}
cli.sh: {ipa: "sˌiːˌɛlˈaɪ dˈɑːt ˌɛsˈeɪtʃ", say: "C-L-I dot S-H"}
cli-multi-gpu.sh: {ipa: "sˌiːˌɛlˈaɪ mˈʌlti dʒˌiːpˌiːjˈuː dˈɑːt ˌɛsˈeɪtʃ", say: "C-L-I multi G-P-U dot S-H"}
package-trainer.sh: {ipa: "pˈækɪdʒ tɹˈeɪnɚ dˈɑːt ˌɛsˈeɪtʃ", say: "package trainer dot S-H"}
setup.py: {ipa: "sˈɛɾʌp dˈɑːt pˈaɪ", say: "setup dot pie"}
task.py: {ipa: "tˈæsk dˈɑːt pˈaɪ", say: "task dot pie"}
model-trainer.json: {ipa: "mˈɑːdəl tɹˈeɪnɚ dˈɑːt dʒˈeɪsˈɑːn", say: "model trainer dot JSON"}
cheese-app-trainer.tar.gz: {ipa: "tʃˈiːz ˈæp tɹˈeɪnɚ dˈɑːt tˈɑːɹ dˈɑːt dʒˌiːzˈiː", say: "cheese app trainer dot tar dot G-Z"}
wandb: {ipa: "dˈʌbəljˌuː ænd bˈiː", say: "W and B"}
us-central1: {ipa: "jˌuːˈɛs sˈɛntɹəl wˈʌn", say: "U S central one"}
notebook A: {ipa: "nˈoʊtbʊk ˈeɪ", say: "notebook A"}
Notebook A: {ipa: "nˈoʊtbʊk ˈeɪ", say: "Notebook A"}
T4s: {ipa: "tˈiː fˈɔːɹz", say: "T fours"}
model dir: {ipa: "mˈɑːdəl dˈɜː", say: "model dur"}
# optional (V28)
gsutil: {ipa: "dʒˌiːˈɛs jˈuːtɪl", say: "G-S util"}
scikit-learn: {ipa: "sˈaɪkɪt lˈɜːn", say: "sy-kit learn"}
```

---

VERDICT: APPROVE WITH FIXES. There are 3 wrong findings (V1–V3), all number readings:
- The hook's 68.97 and 62.93 and nine other decimals or versions come out as two numbers split by a
  stop. The cause is a phonemizer punctuation bug that is new to the series.
- The existing short keys `0.31`, `3.13` and `0.13` splice inside `0.31.0`, `3.13.17` and `0.13.5`.

There are 24 confusing findings (V4–V27): 9 mangled names or readings that need entries ("notebook
uh", `cli.sh` and six other dotted names with a literal-stop pause, "four hundred four", "us central
one", `wandb` against the script's own "W and B", two Cloud SDK and Vertex AI versions, "T four z",
"model dyer"), 2 missing `wait_until` anchors (S07 "a source we name", S08 "before docker run"), 2
garden paths, 1 noun-stressed verb, and 10 long sentences on core mechanisms (9 of them 30 words or
more, including the 43-word recap). There are 19 polish findings (V28–V46). The splice trap is clean, and the
one "a 403" guard fires. Lexicon work required before TTS is 33 keys (Appendix B), plus 2 optional
ones. The required keys include robustness keys for every spoken decimal, because the decimal trap
moves when punctuation changes.
