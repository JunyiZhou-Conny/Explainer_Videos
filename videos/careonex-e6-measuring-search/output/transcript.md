# CareOneX E6 · Measuring search: Marco's experiments with chunking, feedback search and answer checks

## 00:00 — What is on Marco's branch
Marco's branch arrived as one large commit: 213 files and about 46,000 new lines. Most of those lines are not code. They are evidence: test questions, saved search results, and grades.
Almost all of it is about one question: when a caller asks something, does search hand the agent the right passages? Marco turned three dials. How the documents are cut. How the search is run. And how results are ordered. He also added a way to check the spoken answers.

## 00:38 — Scoring a search
First, how do you score a search? You ask a question, take the top 5 passages it returns, and a person grades each one: 0 if it does not help, 1 if it partly helps, 2 if it answers the question.
Precision at 5 is the share of the five that help at all, here 2 out of 5. MRR looks only at the first helpful passage: it is at rank 2, so the score is one half. Rank 1 would score 1.
NDCG rewards putting the best passages first. It scores our order, then scores the best possible order of the same passages, and divides. 1 means perfect order.
All three numbers depend on the grades. No grades, no score.

## 01:35 — Three ways to cut
The first dial is chunking. Marco compared three chunkers. A is the original one from episode 2. B never merges sections with different headings, and repeats the table rows that name the programs. C makes small passages for searching, each linked to a larger parent passage for context.
To compare them fairly, he built three separate test libraries, called staging knowledge bases, and left the main one untouched. Library C is the one his voice demo points at, the ID we met in episode 0.
He asked the same 25 questions to all three, took the top 5 each time, and graded all 375 passages by hand. The team's notes call these grades provisional.

## 02:29 — What the chunking test shows
We reran Marco's own scoring script on his grades. The original chunker A has the best precision and NDCG. The hierarchical chunker C finds the first helpful passage a little sooner. B is lowest on all three. All three take about four tenths of a second.
Question by question, A was best 9 times and C 7 times. 6 were ties, and B was never best on its own. For 3 questions, none of the three libraries found anything helpful, although related words do appear in the documents. Cutting the text differently did not fix them, so these are the questions to study next.
That matters, because on this branch B becomes the default chunker. With 25 questions and provisional grades, these gaps are small and could change. But nothing here shows B is better, and that is worth discussing before the main library is rebuilt with it.

## 03:38 — Feedback search
The second dial is the search itself. In feedback mode, retrieve first searches with the caller's exact question. Then it reads what came back, and may plan one more search. It runs it, keeps a new passage only if it matches the question, and merges the two lists.
An extra search comes from words that are actually there: a heading or phrase in the first results that shares real words with the question. If none qualifies, it uses the caller's own key words, plus a variant from a short fixed list, like lonely to companionship. For "my mother needs help showering", one run added the search "bathing in bed, in the tub or shower", a line from the personal care page.
This is what model-free means: no AI model writes the extra searches, only fixed rules. Another mode, called intent, asks a language model, but the README warns that the team's account may not be allowed to call it.
To merge the lists, each passage gets points from every list it appears in: more for a high rank, and the first search counts one and a half times. A passage that both searches agree on rises. This is called reciprocal rank fusion.
We checked one consequence with Marco's own merge code. A passage found only by the extra search scores at most 1 over 61. The tenth result of the first search scores 1.5 over 70, which is more. So today the extra search can reorder what the first search found. It cannot add a new passage to the top five, unless the first search returned fewer than five. The code's comments suggest new passages were meant to get in, so this is worth a conversation with Marco.

## 05:51 — What the 40-question run shows
Marco saved a run of 40 everyday home-care questions, with and without feedback. Extra searches were used for 18 of them. For 23 of the 40, the top five passages came out exactly the same.
Feedback costs time. The typical search went from about 0.43 to 0.51 seconds, and the slowest tenth from about half a second to about one second.
And here is the key gap: none of the 788 passages in that run were graded. So the run tells us about speed and behaviour, but not whether feedback finds better passages.
The planner has changed since that run. We replayed today's version offline on the same 40 first searches: it adds a search for 17 questions, almost all of them rewrites of the caller's own words. And feedback is now the default in the voice app.

## 06:56 — Checking the spoken answer
The last dial checks answers, not passages. A test call produces two transcripts. A script compares the assistant's answer with a reference answer written by a person: shared words, required and forbidden phrases, and whether the agent actually looked anything up.
Shared words are measured with cosine similarity again, this time over word counts. That has a trap: an answer with one wrong dollar amount shares almost every word with the right one. Marco's notes say it plainly: similarity is not correctness. A person still has to check the facts.
Right now there is one reference answer, marked as a starter. Real testing needs 20 to 30 checked ones.

## 07:48 — Fixes, and what is still open
Episode 2 ended with a table that hid its program names. Marco's branch attacks it three ways. The new chunker fixes it: we checked, and the 1,090 dollar chunk now says JACC. A new extractor was written for that PDF, but on the real file it fails on all four pages, because it finds nine columns where it expects seven. And retrieve now drops every chunk from that table that the extractor did not verify. So for now, the table does not reach the agent at all.
On the voice side, a phone number is saved only after the agent reads it back and the caller says yes. And empty search results can no longer be presented as evidence.
What is open: grade the feedback run, ideally without knowing which mode produced which passage. Decide whether the merge should let new passages in. Fix the extractor for the real PDF. Decide which library is the live one, since none of this is in the main library yet. And note that the branch puts the AWS account number and library IDs into a public repository, which the setup guide had kept out.
Three questions to test yourself. Why can a search with a perfect MRR still have a low precision? Why can today's extra search reorder the top five but not add to it? And why is high word similarity not proof of a correct answer?
Next, episode 3 goes inside a single search, and episode 4 follows a whole phone call through the voice app.
