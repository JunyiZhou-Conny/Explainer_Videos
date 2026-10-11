# CareOneX E6 · Measuring search: Marco's experiments — script & visual plan (v1)

Series: *CareOneX, layer by layer* (`videos/careonex-series/SERIES.md`). Watch after E0 and E2.

Audience: a complete beginner who has seen E0 (the start-up commands) and E2 (the library). Goal:
after E6 the viewer can say what Marco's branch changes about search, read a precision / MRR / NDCG
table, and say honestly what the evidence on the branch does and does not show.

**No narrator.** SAY lines are the subtitles (Chinese above, English below), ~2.2 words/s.

**Sources.** `nadirbt/careonex-agents`, branch `feat/sonic_with_rag_updated` at `1591ed2` (Marco Ren,
2026-10-10; one commit on top of `main` that carries the whole pipeline plus his changes). Docs on
that branch: `RAG_RANKING_CHUNKING_VOICE_EVAL.md`, `HIERARCHICAL_CHUNKING_EXPERIMENT.md`,
`RAG_HANDOFF.md`, `docs/EVALUATION.md`. Every number marked MEASURED comes from rerunning his own
scripts on the files he committed, offline (`videos/careonex-series/checks/marco/`).

Source tags as in the series: READ IN CODE · TEAM NOTES · MEASURED · INFERRED.
Colours: our code BLUE · stored data GREEN · AWS ORANGE · question / query YELLOW · problems RED ·
the three chunkers A = GREY, B = BLUE, C = TEAL.

---

## S01 · What is on Marco's branch — `s01_branch.py` · `Branch`

SHOW: A bar: 213 files changed, 46,458 lines added; split into "code and tests" and "evaluation data"
(questions, saved search results, grades). Tag READ IN CODE (git).
SAY: Marco's branch arrived as one large commit: 213 files and about 46,000 new lines. Most of those lines are not code. They are evidence: test questions, saved search results, and grades.

SHOW: The E2 map shrinks to the retrieve box; three dials appear around it: "how the text is cut"
(chunking), "how we search" (one search or feedback search), "how results are ordered" (reranking).
A fourth dial below, "how we check answers".
SAY: Almost all of it is about one question: when a caller asks something, does search hand the agent the right passages? Marco turned three dials. How the documents are cut. How the search is run. And how results are ordered. He also added a way to check the spoken answers.

---

## S02 · How do you measure "found the right passage"? — `s02_metrics.py` · `Metrics`

SHOW: A question strip (YELLOW) and five returned passages, ranks 1–5. A person grades each one:
0 no help, 1 partly, 2 answers it. Grades appear: 0, 2, 1, 0, 0.
SAY: First, how do you score a search? You ask a question, take the top 5 passages it returns, and a person grades each one: 0 if it does not help, 1 if it partly helps, 2 if it answers the question.

SHOW: Precision at 5: count of passages with grade above 0 / 5 = 2/5 = 0.4. MRR: first helpful passage
is at rank 2 → 1/2 = 0.5.
SAY: Precision at 5 is the share of the five that help at all, here 2 out of 5. MRR looks only at the first helpful passage: it is at rank 2, so the score is one half. Rank 1 would score 1.

SHOW: NDCG: the same grades, each divided by a "discount" that grows with rank; then the best
possible order (2, 1, 0, 0, 0) gets the same treatment; NDCG = ours / best = 2.39 / 3.63 = 0.66 (gain
2^g − 1, discount log2(rank + 1)). Footnote: in Marco's scorer "best order" = the best five passages that
any of the three libraries returned for that question.
SAY: NDCG rewards putting the best passages first. It scores our order, then scores the best possible order of the same passages, and divides. 1 means perfect order.

SHOW: A warning card: "grades come from people → scores are only as good as the grading".
SAY: All three numbers depend on the grades. No grades, no score.

---

## S03 · Three ways to cut, three test libraries — `s03_chunkers.py` · `Chunkers`

SHOW: The same document (the team summary) cut three ways, side by side:
A "legacy": the E2 chunker (v2), 1,600 / 2,800. B "section-safe" (v4): never folds a short section into
a different heading, repeats a table's header row (now including the program-name row), up to 120
characters of overlap. C "hierarchical": small "children" of about 950 characters are indexed; each
points to a bigger "parent" of up to 2,400 characters kept for context. Tag READ IN CODE.
SAY: The first dial is chunking. Marco compared three chunkers. A is the original one from episode 2. B never merges sections with different headings, and repeats the table rows that name the programs. C makes small passages for searching, each linked to a larger parent passage for context.

SHOW: Three separate staging Knowledge Bases (ORANGE), one per chunker, beside the untouched main
library. Names: A 3C45…, B FJBD…, C UYC7… (masked). "C = the library Marco's voice demo uses (E0)".
SAY: To compare them fairly, he built three separate test libraries, called staging knowledge bases, and left the main one untouched. Library C is the one his voice demo points at, the ID we met in episode 0.

SHOW: 25 questions × 3 libraries × top 5 = 375 passages, each graded 0 / 1 / 2 by hand, labelled
"provisional". Tag TEAM NOTES (`docs/EVALUATION.md`: "manually/provisionally graded").
SAY: He asked the same 25 questions to all three, took the top 5 each time, and graded all 375 passages by hand. The team's notes call these grades provisional.

---

## S04 · What the chunking test shows — `s04_chunk_results.py` · `ChunkResults`

SHOW: A grouped bar chart: precision@5 A 0.52 · B 0.47 · C 0.50; MRR A 0.69 · B 0.67 · C 0.73;
NDCG A 0.60 · B 0.53 · C 0.58; time per search about 0.41 s for all three. Tag MEASURED (his scorer,
rerun on his grades).
SAY: We reran Marco's own scoring script on his grades. The original chunker A has the best precision and NDCG. The hierarchical chunker C finds the first helpful passage a little sooner. B is lowest on all three. All three take about four tenths of a second.

SHOW: Per question, which chunker had the best NDCG: A 9 · C 7 · tie 6 (B shares the top 3 times) ·
B alone 0 · and 3 questions (RED) where no library returned a single helpful passage (their text:
home health aide for meals and dressing · Medicaid paying a family caregiver · where to start). Tag
MEASURED. Note: "home health aide" occurs in 15 chunks of the E2 library (MEASURED), so the words are there.
SAY: Question by question, A was best 9 times and C 7 times. 6 were ties, and B was never best on its own. For 3 questions, none of the three libraries found anything helpful, although related words do appear in the documents. Cutting the text differently did not fix them, so these are the questions to study next.

SHOW: Two notes: "on this branch `careonex-chunk run` uses B (CHUNKER_VERSION 4); the main library was
built with A (version 2)" READ IN CODE; "25 questions, provisional grades: differences this small may not hold up" (GREY).
SAY: That matters, because on this branch B becomes the default chunker. With 25 questions and provisional grades, these gaps are small and could change. But nothing here shows B is better, and that is worth discussing before the main library is rebuilt with it.

---

## S05 · Feedback search, step by step — `s05_feedback.py` · `Feedback`

SHOW: The pipeline of `feedback` mode (retrieve/feedback_expansion.py + retriever.py):
1 first search with the caller's exact question (10 candidates) → 2 read the top results → 3 plan at
most one extra search (the setting allows two; the saved run used up to two) → 4 run it → 5 keep a new
passage only if it matches the question → 6 merge the lists, keep the top 5. Tag READ IN CODE.
SAY: The second dial is the search itself. In feedback mode, retrieve first searches with the caller's exact question. Then it reads what came back, and may plan one more search. It runs it, keeps a new passage only if it matches the question, and merges the two lists.

SHOW: Where an extra search comes from: (a) a heading or short phrase in a top result that shares real
words with the question, followed by "Relevant to caller question: <the question>"; (b) if none
qualifies, a rewrite: the caller's key words plus at most two variants from a fixed list of ~30 word
pairs (showering → bathing, lonely → companionship). Examples: saved run "My mother needs help
showering…" → "bathing in bed, in the tub or shower. Relevant to caller question: …"; today's planner
"Can a caregiver help prepare meals at home?" → "prepare meals preparation".
SAY: An extra search comes from words that are actually there: a heading or phrase in the first results that shares real words with the question. If none qualifies, it uses the caller's own key words, plus a variant from a short fixed list, like lonely to companionship. For "my mother needs help showering", one run added the search "bathing in bed, in the tub or shower", a line from the personal care page.

SHOW: "Model-free": no AI model writes the extra searches; contrast with the `intent` mode, which asks
Nova Lite; the README: "require IAM permission your team profile may not have". Tag READ IN CODE / TEAM NOTES.
SAY: This is what model-free means: no AI model writes the extra searches, only fixed rules. Another mode, called intent, asks a language model, but the README warns that the team's account may not be allowed to call it.

SHOW: Reciprocal rank fusion: each list gives a passage 1 / (60 + rank) points; the first search's
points count 1.5×; a passage found by two searches adds both. Small worked example with two lists.
SAY: To merge the lists, each passage gets points from every list it appears in: more for a high rank, and the first search counts one and a half times. A passage that both searches agree on rises. This is called reciprocal rank fusion.

SHOW: The consequence, checked with his own `reciprocal_rank_fusion` and today's weights (MEASURED,
`checks/marco/rrf_reach.py`): a passage found only by the extra search scores at most 1 / 61 = 0.016; the
10th result of the first search scores 1.5 / 70 = 0.021. Merged top 5 with every extra hit new: first1–5.
Only when the first search returns 4 does one new passage get in. The code comment ("require a novel
supplemental-only hit to address the original question before RRF can promote it") suggests new
passages were meant to get in: INFERRED, ask Marco. (The saved 40-question run merged with equal weights:
there, passages outside the first search's top 5 entered it in 14 of 40 questions, MEASURED.)
SAY: We checked one consequence with Marco's own merge code. A passage found only by the extra search scores at most 1 over 61. The tenth result of the first search scores 1.5 over 70, which is more. So today the extra search can reorder what the first search found. It cannot add a new passage to the top five, unless the first search returned fewer than five. The code's comments suggest new passages were meant to get in, so this is worth a conversation with Marco.

---

## S06 · What the 40-question run shows — `s06_feedback_results.py` · `FeedbackResults`

SHOW: The saved 40-question run (40 home-care questions; library C; an earlier planner version):
extra searches used for 18 of 40; top-5 list unchanged for 23 of 40. Tag MEASURED.
SAY: Marco saved a run of 40 everyday home-care questions, with and without feedback. Extra searches were used for 18 of them. For 23 of the 40, the top five passages came out exactly the same.

SHOW: Time per search: median 0.43 s → 0.51 s; slowest tenth (90th percentile) 0.51 s → 1.01 s. Tag MEASURED.
SAY: Feedback costs time. The typical search went from about 0.43 to 0.51 seconds, and the slowest tenth from about half a second to about one second.

SHOW: A grade column for the 40-question run, every cell "—": 0 of 788 passages graded. RED.
SAY: And here is the key gap: none of the 788 passages in that run were graded. So the run tells us about speed and behaviour, but not whether feedback finds better passages.

SHOW: Today's planner, replayed offline on those 40 first searches: an extra search for 17 of 40; 16
of them built from the caller's own words, 1 from a retrieved heading. Tag MEASURED. Then the E0
sticky note `CAREONEX_VOICE_SEARCH_MODE = "feedback"`: "the voice app's default".
SAY: The planner has changed since that run. We replayed today's version offline on the same 40 first searches: it adds a search for 17 questions, almost all of them rewrites of the caller's own words. And feedback is now the default in the voice app.

---

## S07 · Checking the spoken answer — `s07_text_eval.py` · `TextEval`

SHOW: Voice-to-voice call → two transcripts (caller, assistant) → `text_eval.py` compares them with a
"gold" reference answer: word error rate of the question transcript; word cosine of the answer vs the
gold answer; expected and forbidden phrases; whether a lookup happened and returned passages.
Tag READ IN CODE.
SAY: The last dial checks answers, not passages. A test call produces two transcripts. A script compares the assistant's answer with a reference answer written by a person: shared words, required and forbidden phrases, and whether the agent actually looked anything up.

SHOW: Word cosine: two bags of word counts, the angle between them (link to E2's cosine, but over
word counts, not meaning). Then a trap: "the income limit is $4,855" vs "the income limit is $5,855":
(made-up example) → word cosine 0.93, wrong number (RED). Computed with his `text_cosine`.
SAY: Shared words are measured with cosine similarity again, this time over word counts. That has a trap: an answer with one wrong dollar amount shares almost every word with the right one. Marco's notes say it plainly: similarity is not correctness. A person still has to check the facts.

SHOW: The gold file today: 1 question (Medicaid), marked "starter, not a reviewed legal reference".
TEAM NOTES.
SAY: Right now there is one reference answer, marked as a starter. Real testing needs 20 to 30 checked ones.

---

## S08 · Fixes, and what is still open — `s08_open.py` · `OpenItems`

SHOW: The E2 table problem, three steps on the branch:
1 chunker B now repeats the program-name row → the $1,090 chunk says JACC ✓ (MEASURED);
2 a new extractor reads the PDF's table lines and writes one section per program, but on the real 2026
PDF it fails on all four pages: it finds 9 columns where it expects 7, and one program name sits on a
second header row ✗ (MEASURED);
3 retrieve now drops any side-by-side chunk that extractor did not verify → the table never reaches
the agent; the team summary carries its numbers (READ IN CODE).
SAY: Episode 2 ended with a table that hid its program names. Marco's branch attacks it three ways. The new chunker fixes it: we checked, and the 1,090 dollar chunk now says JACC. A new extractor was written for that PDF, but on the real file it fails on all four pages, because it finds nine columns where it expects seven. And retrieve now drops every chunk from that table that the extractor did not verify. So for now, the table does not reach the agent at all.

SHOW: Voice safety changes (READ IN CODE): a callback number is saved only after the agent reads the
digits back and the caller says yes; one search per lookup (an age no longer doubles the searches);
empty or malformed results never count as evidence.
SAY: On the voice side, a phone number is saved only after the agent reads it back and the caller says yes. And empty search results can no longer be presented as evidence.

SHOW: Open list: grade the 40-question feedback run, ideally without knowing which mode produced
which passage · decide whether the merge should let new passages in (S05) · fix the extractor for the real layout · choose which library is live · nothing is in
the main library yet: re-ingestion needs team approval · the branch puts the AWS account and library
IDs in a public repository, which the team's setup guide kept out (INFERRED: not a password, but
worth a team decision).
SAY: What is open: grade the feedback run, ideally without knowing which mode produced which passage. Decide whether the merge should let new passages in. Fix the extractor for the real PDF. Decide which library is the live one, since none of this is in the main library yet. And note that the branch puts the AWS account number and library IDs into a public repository, which the setup guide had kept out.

SHOW: Ponder card with three questions.
SAY: Three questions to test yourself. Why can a search with a perfect MRR still have a low precision? Why can today's extra search reorder the top five but not add to it? And why is high word similarity not proof of a correct answer?

SHOW: Closing map: the three dials around retrieve; "next: E3 · finding the right passage, and E4 ·
the voice loop".
SAY: Next, episode 3 goes inside a single search, and episode 4 follows a whole phone call through the voice app.
