# Calibrating Noise to Sensitivity — narration script & visual plan

Paper: C. Dwork, F. McSherry, K. Nissim, A. Smith. *Calibrating Noise to Sensitivity in Private
Data Analysis.* TCC 2006, LNCS 3876, pp. 265–284. (`library/privacy/differential-privacy/dwork2006calibrating.pdf`)

Audience: a smart newcomer (comfortable with basic probability and functions; has never heard of
differential privacy). Goal: intuition first, then the exact statements from the paper.

Conventions
- `SAY:` lines are spoken verbatim by the narrator (one `voiceover` block each) and become subtitles.
  Write numbers and symbols the way they should be *spoken* ("e to the epsilon", "one over n").
- `SHOW:` lines describe the visuals that accompany the following `SAY:` block.
- Semantic colours (keep them fixed for the whole video):
  database **x** = BLUE · neighbouring database **x′** = ORANGE · Alice / the one changed row = PINK ·
  **ε** (privacy loss / budget) = YELLOW · sensitivity **S(f)** = GREEN · noise / Laplace = RED ·
  true answer = WHITE · secondary text = GREY · "this paper" highlight = YELLOW frame.
- Paper references in brackets (e.g. [Def. 1, p. 270]) are for reviewers; they are not spoken.

---

## S01 · The differencing attack — `s01_hook.py` · `Hook`

SHOW: A grid of ~40 grey person icons labelled "Hospital database". A few icons are PINK (have
condition X). A query card slides in from the right: "How many patients have condition X?"
SAY: Here is a hospital database, one row per patient. A researcher asks an innocent-looking question: how many patients have condition X? The hospital releases no records at all. It just says: forty-one.

SHOW: The answer "41" appears under the query. Then a new PINK icon labelled "Alice" slides into the
grid. The same query card fires again; the answer becomes "42".
SAY: A week later, one new patient, Alice, is admitted. The researcher asks the exact same question. The answer is now forty-two.

SHOW: "42 − 41 = 1" written out; an arrow from the 1 to Alice; a red tag "Alice has condition X".
SAY: Subtract, and the researcher has learned something very specific about Alice, without ever seeing a single record. No names were released. Only counts. But the counts were exact.

SHOW: Everything fades except a large question mark; two short lines of text appear:
"What makes a statistic private?" / "How much noise is enough?"
SAY: So aggregate statistics are not automatically private. But then what would it even mean for a statistic to be private? And if the fix is to add noise, how much noise is enough?

SHOW: Page 1 of the actual paper (asset `paper_p1.png`) slides in on the left, tilted slightly; the
title is boxed in YELLOW. On the right: "Dwork · McSherry · Nissim · Smith", "TCC 2006",
"Gödel Prize 2017".
SAY: In 2006, Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith answered both questions in this paper: Calibrating Noise to Sensitivity in Private Data Analysis. It is the paper that founded what we now call differential privacy, and in 2017 it won the Gödel Prize.

SHOW: The page shrinks away. Four numbered idea cards appear one by one:
"1 · A definition of privacy" (YELLOW ε icon), "2 · Sensitivity" (GREEN), "3 · The Laplace mechanism"
(RED tent curve), "4 · A limit on one-shot releases" (GREY).
SAY: By the end of this video, you will understand its three big ideas: a definition of privacy, a number called sensitivity, and a recipe for exactly how much noise to add. Plus a surprising limit on what any one-shot anonymized release can achieve.

---

## S02 · Where this paper sits — `s02_map.py` · `LineageBefore`

SHOW: A horizontal timeline from 1960 to 2010 along the bottom. Above 1965 a card appears:
"Warner 1965 — Randomized response".
SAY: First, a quick map, so you know where this paper sits. Protecting privacy with randomness is an old idea. In 1965, Stanley Warner proposed randomized response for sensitive surveys: each person randomizes their own answer with a private coin, so no single answer can be held against them.

SHOW: Card at ~1980: "Statistical disclosure control — perturb inputs or outputs" (Denning 1980;
Adam & Wortmann 1989). Card at ~2000: "Sweeney — 'anonymous' ≠ anonymous" with a small graphic:
"ZIP + birth date + sex → 87% unique".
SAY: Statisticians spent decades refining such tricks. Meanwhile, the intuitive fix, just remove the names, kept failing. Latanya Sweeney showed that ZIP code, birth date and sex alone single out most Americans, and she famously matched anonymous hospital records back to the governor of Massachusetts.

SHOW: Card at 2003: "Dinur & Nissim 2003 — too many accurate answers ⇒ reconstruction".
Mini-animation: a stream of queries hits a database; each answer has a tiny error bar labelled
"error ≪ √n"; the database "reassembles" on the attacker's side.
SAY: Then, in 2003, Irit Dinur and Kobbi Nissim proved something sobering. If a database answers too many questions too accurately, with errors much smaller than the square root of n, an attacker can reconstruct almost the entire database. Noise is not optional. It is the price of answering at all.

SHOW: Cards at 2004–2005: "Dwork & Nissim 2004", "Blum, Dwork, McSherry & Nissim 2005 — SuLQ:
noisy sums". Under them a label: "only sums Σᵢ g(xᵢ)".
SAY: Dwork, Nissim and colleagues then found the positive side. With a limited number of questions, noisy sums, such as counts of rows with some property, can be answered both usefully and privately. That framework was called SuLQ.

SHOW: The 2006 card for THIS paper drops in with a YELLOW frame: "Dwork, McSherry, Nissim & Smith
2006 — any function f · one definition · noise ∝ sensitivity". Arrows from the 2003–2005 cards
into it.
SAY: But it only covered sums, and its definitions were complicated. This paper takes the leap: any function of the data, one clean definition, and one simple rule for the noise. Hold on to this map. We will come back at the end to see what grew out of it.

---

## S03 · The setup: a trusted curator — `s03_setup.py` · `Curator`

SHOW: Left: a vault/box labelled "database x" (BLUE) containing n rows (row stack). Middle: a
"curator" figure next to the box. Right: an "analyst" figure. An arrow from analyst to curator
carries "query f".
SAY: Here is the setting. A trusted server, let's call it the curator, holds a database x: n rows, one per person. An analyst sends a query f, any function that maps the database to a number, or to a list of numbers.

SHOW: Inside the curator: "f(x)" computed (WHITE) but locked (a small lock icon — it never leaves).
A RED die/noise blob "Y" appears; the output "f(x) + Y" travels back to the analyst. Then a second
and third query arrow fly in, labelled "interactive: ask, answer, repeat".
SAY: The honest answer is f of x, but the curator never releases it. Instead, it draws random noise, Y, and releases f of x plus Y. And because the analyst can keep asking, one question after another, this is called the interactive setting. Remember that word.

SHOW: A dial labelled "noise": left end "too little → Alice exposed", right end "too much →
useless". Then the paper's title phrase appears: "Calibrate the noise to the sensitivity".
SAY: That is the entire mechanism. Everything in this paper is about one question: what distribution should Y have? Too little noise, and Alice is exposed. Too much, and the answer is useless. The title gives the answer: calibrate the noise to the sensitivity. But first, we need to pin down what private actually means.

---

## S04 · Defining privacy — `s04_definition.py` · `Definition`

SHOW: Two database row-stacks side by side: "x" (BLUE) and "x′" (ORANGE). All rows identical
except one row highlighted PINK (Alice): value 1 in x, 0 in x′. A "≠ only here" bracket.
SAY: The key move is to imagine two worlds. In one world, the database is x. In the other, it is x prime: identical in every row except one. Say, Alice's.

SHOW: Each database feeds a mechanism box "𝒯"; out come two smooth output distributions over a
shared horizontal axis "output t" — BLUE and ORANGE curves, heavily overlapping.
SAY: Run the mechanism in each world. Because it is random, each world produces a whole distribution of possible outputs.

SHOW: Pick a point t on the axis; vertical lines up to both curves give Pr[𝒯(x)=t] (BLUE) and
Pr[𝒯(x′)=t] (ORANGE). Then Definition 1 is written out in full:
|ln( Pr[𝒯(x)=t] / Pr[𝒯(x′)=t] )| ≤ ε   (ε in YELLOW) with caption
"for all x, x′ differing in one row, and all outputs t" [Def. 1, p. 270].
SAY: The paper's definition, which it calls epsilon-indistinguishability, says this. For every pair of databases that differ in a single row, and for every possible output t, the log of the ratio of these two probabilities is at most epsilon in absolute value.

SHOW: Transform the formula into e^{−ε} ≤ ratio ≤ e^{ε}; below, a plot of the ratio as t sweeps
left to right, staying inside a YELLOW band [e^{−ε}, e^{ε}]. Small note: "small ε: e^ε ≈ 1 + ε".
SAY: Equivalently, the ratio stays between e to the minus epsilon and e to the epsilon. When epsilon is small, that is roughly one plus or minus epsilon. Every output is almost equally likely in both worlds.

SHOW: An attacker icon looking at the output t. Above Alice: a "belief" bar (odds that Alice's row
is 1). Seeing t changes the bar only slightly; label "odds change by at most × e^ε".
SAY: Now be the attacker. You see the output, and you want to know which world you are in. But whatever you see was roughly as likely either way. By Bayes' rule, your odds about Alice's row can change by at most a factor of e to the epsilon, no matter what you knew beforehand.

SHOW: A small vignette: "Study finds: smoking → heart disease". Alice (PINK) with a cigarette icon;
"Her insurer now worries" — then a tick: "would happen with or without Alice's row ✓ not a privacy
breach" [p. 267, App. A].
SAY: Notice what this does not promise. Suppose the study reveals that smoking causes heart disease. If Alice smokes, people may now believe she is at higher risk. The paper argues that is not a privacy violation, because it would happen whether or not Alice was in the database. What is protected is exactly the contribution of Alice's own row.

SHOW: A dial for ε (YELLOW): "smaller ε → stronger privacy". Label "set by policy" and the paper's
word "leakage".
SAY: And epsilon is a dial, set by policy. The paper calls it the leakage. Smaller epsilon means stronger privacy.

---

## S05 · Why so strict? — `s05_strict.py` · `WhyStrict`

SHOW: Title "Why a ratio, for every output?". Two curves that are "close on average": total
variation distance shown as a small shaded sliver.
SAY: Why demand a ratio bound for every single output? In cryptography it is common to settle for something weaker: two distributions count as close if they differ by a small total amount, a small statistical distance. The paper shows why that is not good enough here.

SHOW: Database row-stack (n rows). A random pointer spins and lands on row i; the whole row
(name + value) is copied out as the published output "(i, xᵢ)". Caption: "Mechanism: publish one
random row" [Example 2, p. 271].
SAY: Consider this mechanism: pick one row at random and publish it, word for word. Change one person's row, and the output distribution changes by only one over n. For a big database that is tiny, so by the averaged measure this looks wonderfully private.

SHOW: The pointer lands on Alice's row: output "(Alice, 1)". Side-by-side probabilities:
"in world x: 1/n" vs "in world x′: 0". Ratio "1/n ÷ 0 = ∞" in RED; a big RED ✗ over
"privacy".
SAY: But every output is somebody's complete record. The ratio test catches it immediately. If x and x prime differ in Alice's row, then the output showing Alice's real value has probability one over n in one world, and zero in the other. The ratio is infinite.

SHOW: Text: "Averages hide rare catastrophes. Ratios rule them out everywhere."
SAY: Averages let rare catastrophes slip through. A ratio bound rules them out everywhere.

SHOW: Pause-and-ponder card: "Why can't ε be much smaller than 1/n?" (timer bar drains ~4 s).
SAY: One more subtlety. Pause and ponder this: why can't we make epsilon vanishingly small, say much smaller than one over n?

SHOW: A chain of databases x = x⁽⁰⁾ → x⁽¹⁾ → … → x⁽ⁿ⁾ = y, each arrow labelled "× e^ε", one row
changing per step (PINK). The total "≤ e^{nε}" grows at the end. Then: "nε ≪ 1 ⇒ all databases look
alike ⇒ nothing can be learned" [p. 271].
SAY: Here is why. Any two databases are connected by a chain of at most n single-row changes. Each step can change output probabilities by at most a factor of e to the epsilon, so the two ends differ by at most e to the n epsilon. If n times epsilon is tiny, every database produces essentially the same outputs, and nothing at all can be learned. So useful privacy must leak a little: epsilon of at least about one over n. This chain trick, called a hybrid argument, will come back later.

---

## S06 · Sensitivity — `s06_sensitivity.py` · `Sensitivity`

SHOW: A function machine "f" taking a database to a number line. Swap one row (PINK) and the
output dot moves; the gap is marked. Then the definition appears (S in GREEN) [Def. 2, p. 271]:
S(f) = max over neighbouring x, x′ of ‖f(x) − f(x′)‖₁.
SAY: So how much noise do we need? The paper's answer depends on a single property of the query: its sensitivity. That is the most that changing one row can ever change the answer. Formally, it is the maximum, over all pairs of neighboring databases, of the distance between f of x and f of x prime, measured in the L1 norm: add up the absolute differences of all the coordinates.

SHOW: Counting query: the hospital count 41 → 42 when Alice's row flips; "S(count) = 1".
SAY: For a counting query, like our hospital count, changing one row changes the answer by at most one. Sensitivity one.

SHOW: A histogram with 5 bins. Alice (PINK) moves from bin 2 to bin 4: one bar drops by 1, another
rises by 1 → "|−1| + |+1| = 2". Then the histogram morphs into 20 bins, then 60 thin bins; the
label "S = 2" stays put [Example 3, p. 271–272].
SAY: Now a histogram: split the population into d bins and release every count. Change Alice's row, and she moves out of one bin and into another. One count goes down by one, another goes up by one. Total change: two. And that is true whether there are five bins or five thousand. The sensitivity does not depend on the dimension at all.

SHOW: Contrast (marked "illustration"): "largest income in the database". One extreme row (a
gold coin stack) drags the answer far right; "S huge" in GREEN.
SAY: Contrast that with a query like: what is the largest income in the database? A single billionaire can move that answer by a billion. That query is highly sensitive, so it will need a lot of noise.

SHOW: Two labelled boxes: "ε — a choice (policy)" in YELLOW and "S(f) — a fact about f" in GREEN.
"S(f) does not depend on the actual database".
SAY: Two things to remember. Sensitivity is a property of the function alone, not of the particular database. And it is not chosen by policy; it is inherent in the question being asked. Epsilon is a choice. Sensitivity is a fact.

---

## S07 · The Laplace mechanism — `s07_laplace.py` · `LaplaceMechanism`

SHOW: Axes; the Laplace density (RED) drawn as a sharp tent-shaped peak. Formula
h(y) ∝ e^{−|y|/λ}, with λ labelled "scale".
SAY: Now for the noise. The paper uses the Laplace distribution: symmetric, sharply peaked, with a density that falls off exponentially with distance from the center. Its width is set by a scale parameter, lambda.

SHOW: Two Laplace curves, BLUE centred at f(x) = 41 and ORANGE centred at f(x′) = 42 (λ = 1).
SAY: Here is the trick that makes it work. Center one Laplace curve at f of x, say forty-one, and another at f of x prime, forty-two. These are the output distributions in our two worlds.

SHOW: A second axis below: the log of the ratio of the two densities as a function of t — flat at
+1/λ on the left, a straight ramp between 41 and 42, flat at −1/λ on the right. A YELLOW band of
height ±1/λ around 0 contains it.
SAY: Now plot the log of their ratio, for every possible output t. Far to the left, it is constant. Far to the right, constant again. In between, a straight ramp. It never leaves a band of height one over lambda: the shift, divided by the scale.

SHOW: Switch the top plot to log-density: each Laplace becomes a "tent" of two straight lines.
Shift the tent by 1: the vertical gap between the tents is shown never exceeding 1/λ.
SAY: Why? On a log scale, a Laplace density is just a tent made of two straight lines. Slide the tent over, and the vertical gap between the two tents can never exceed the size of the slide, divided by lambda. That is the triangle inequality in disguise.

SHOW: One-line proof (colours: S GREEN, ε YELLOW):
ln[h(t−f(x)) / h(t−f(x′))] = (|t−f(x′)| − |t−f(x)|)/λ ≤ |f(x)−f(x′)|/λ ≤ S(f)/λ.
Then substitute λ = S(f)/ε ⇒ ≤ ε. Box it.
SAY: So for any output, the privacy loss is at most the sensitivity divided by lambda. Set lambda equal to the sensitivity over epsilon, and the ratio is bounded by e to the epsilon, for every output and every pair of neighboring databases. Privacy, proven in one line.

SHOW: Proposition 1 card [p. 272]: San_f(x) = f(x) + (Y₁, …, Y_d), Yᵢ ~ Lap(S(f)/ε) i.i.d.
Small 2-D picture: joint density contours are diamonds (L1 balls).
SAY: If the query returns several numbers, add independent Laplace noise to each coordinate. The joint density then depends on the L1 distance, which is exactly why sensitivity is measured in the L1 norm. That is the paper's Proposition 1: Laplace noise of scale S of f over epsilon in every coordinate.

SHOW: Compare with a Gaussian (GREY): on the log scale it is a parabola; two shifted parabolas
differ by a straight line that grows without bound; the log-ratio plot shoots out of the YELLOW band
in the tails (RED overflow arrows).
SAY: Why not the familiar bell curve? On a log scale a Gaussian is a parabola, and the gap between two shifted parabolas is a straight line that grows without bound. Far out in the tails the ratio explodes, so no single epsilon works for every output. Laplace tails are exactly heavy enough.

SHOW: Title-style summary: "noise scale = S(f) / ε" (S GREEN, ε YELLOW); two arrows: "more sensitive
→ more noise", "stronger privacy → more noise".
SAY: That is the recipe in the title. Noise scale equals sensitivity divided by epsilon. A more sensitive question needs more noise. Stronger privacy needs more noise. And nothing else matters.

---

## S08 · Privacy for individuals, accuracy for populations — `s08_payoff.py` · `Payoff`

SHOW: Back to the hospital query. ε = 0.5 ⇒ Laplace scale 2. Week 1: true 41 → released "43.7";
week 2: true 42 → released "40.6". Two broad overlapping Laplace curves (BLUE at 41, ORANGE at 42).
SAY: Back to the hospital. With epsilon equal to one half, the curator adds Laplace noise of scale two. Week one, it reports about forty-three point seven. Week two, after Alice arrives, about forty point six. The difference tells the researcher almost nothing about Alice. The two worlds' answer distributions overlap heavily.

SHOW: Highlight "scale = S(f)/ε" — circle the two inputs; a crossed-out "n".
SAY: Now look at what the noise scale depends on: the sensitivity and epsilon. Not the size of the database.

SHOW: Three number lines stacked: n = 100 (true count ≈ 50), n = 10,000 (≈ 5,000), n = 1,000,000
(≈ 500,000), each zoomed so the true answer is centred; the RED noise band is the same absolute width
(±2) and becomes visually negligible; labels "≈ 4%", "≈ 0.04%", "≈ 0.0004%".
SAY: With a hundred patients, noise of size two is a few percent of the answer. With a million patients, it is a rounding error. Alice is protected by noise that is large compared to her own contribution, which is one, but tiny compared to the whole population.

SHOW: Two-line slogan: "Privacy for individuals. Accuracy for populations."
SAY: Privacy for individuals. Accuracy for populations. That is the bargain.

---

## S09 · Many questions: the privacy budget — `s09_budget.py` · `Budget`

SHOW: Analyst asks f₁ → a₁; the next query f₂ visibly depends on a₁ (an arrow from a₁ into f₂);
then f₃ … A transcript strip builds: t = [a₁, a₂, a₃, …].
SAY: One question is never enough. Real analysts ask many, and adaptively, each question chosen after seeing the earlier answers. Maybe you spot a spike in one bin of a histogram, and zoom in on it.

SHOW: Pr[t] = Π Pr[aᵢ | a₁…aᵢ₋₁] ; under it the per-factor bounds e^{|Δᵢ|/λ}; the product
turns into a sum in the exponent: exp(Σ|Δᵢ|/λ) ≤ exp(S/λ) [Thm. 1, p. 273].
SAY: The paper's Theorem 1 handles this. The probability of the whole conversation is a product: each answer's probability, given the answers before it. Each factor is a Laplace term with its own small privacy loss, and when probabilities multiply, log ratios add.

SHOW: A YELLOW "privacy budget ε" bar. Each answered query drains a segment. When it is empty, the
curator shows "refused". Note: "refusal depends only on S(fₜ) → reveals nothing about the data".
SAY: So privacy losses add up. Epsilon behaves like a budget. Each answer spends part of it, and once it is spent, the curator stops answering. Crucially, the curator decides whether to answer by looking only at the sensitivity of the queries, which does not depend on the data, so even a refusal reveals nothing.

SHOW: Two noisy histograms of the same data with d = 100 bins. Left "each bin as its own query
(earlier framework)": noise bars grow like √d. Right "one query, S = 2 (this paper)": small constant
noise bars [§3.2, p. 273].
SAY: This view also reveals hidden savings. In the earlier framework, a histogram with d bins was treated as d separate questions, so the noise in each bin grew with the number of bins, roughly like the square root of d. Here the whole histogram is a single question with sensitivity two, so each bin gets noise of about two over epsilon, no matter how many bins there are.

---

## S10 · Beyond counting — `s10_beyond.py` · `BeyondCounting`

SHOW: A 2×2 grid of tiles that light up in turn: "Covariance matrices", "Distance to a property",
"Small random samples", "Any metric space".
SAY: Sensitivity reaches far beyond counts. Here are a few examples from the paper.

SHOW: Tile 1: a d×d matrix heat-map; label "d² numbers, one query → a factor d less noise than d²
separate queries" [p. 274].
SAY: Means and covariance matrices have d squared entries, but treated as a single query, they need a factor of d less noise than asking for each entry separately.

SHOW: Tile 2: a small social network graph; a minimum cut highlighted (RED dashed line) with its
weight "3"; one edge changes and the cut changes by at most 1; label "min cut is 1-sensitive" [p. 274].
SAY: Distances work too. How much would you need to change the data to give it some property? Changing one row moves that distance by at most one. Picture a social network, where each link is a person's data. The minimum cut, the total weight of links you must remove to split the network, is one-sensitive, so it can be released with just a little noise.

SHOW: Tile 3: a big crowd; a small random sample is highlighted; Alice is usually not in it;
"Lemma 1: approximable from a small sample ⇒ low sensitivity" [p. 275].
SAY: And anything you can estimate well from a small random sample has low sensitivity. A small sample rarely contains Alice, so her row cannot matter much. That is the paper's Lemma 1.

SHOW: Tile 4: outputs in a general space (points on a plane); a glowing true answer f(x); every
candidate output y is shaded by weight exp(−ε·d(y, f(x)) / 2S) — brighter near the truth
[Thm. 2, p. 276]. Caption: "→ exponential mechanism (McSherry & Talwar 2007)".
SAY: Finally, the answer need not be a number at all. Section three point three handles any metric space: choose an output with probability that decays exponentially with its distance from the true answer. Answers near the truth are exponentially favored. Later, McSherry and Talwar generalized this idea into the exponential mechanism, one of the workhorses of the field.

---

## S11 · Interactive vs. one-shot releases — `s11_separation.py` · `Separation`

SHOW: Split screen. Left "Interactive": curator answering a stream of queries. Right
"Non-interactive": curator publishes a sanitized table "San(x)" once, then walks away; many users
query the table.
SAY: The last part of the paper asks a question practitioners cared about deeply. Statisticians and data miners traditionally prefer the non-interactive model: sanitize the data once, publish an anonymized table, and let anyone compute anything. Can that work under this strong definition of privacy?

SHOW: Rows as d-bit strings. A random mask r selects some bit positions (highlighted columns); for
each row, the parity of the selected bits is shown (0 or 1). Caption: "parity query: how many rows
have r · x = 1 (mod 2)?", "sensitivity 1". On the left, the interactive curator answers it with
"± 1/ε".
SAY: The paper proves a striking limit. Suppose each row is a string of d bits. Consider parity queries: choose a subset of the bit positions, and ask how many rows have an odd number of ones in that subset. Each such query has sensitivity one, so an interactive curator can answer any one of them with noise of about one over epsilon.

SHOW: "2^d parity queries" — a fan of many masks. Two databases: "every row has parity 0 → answer 0"
vs "every row has parity 1 → answer n"; both feed San; the two outputs look nearly identical
("statistical difference ≈ 0"). Caption: "unless n ≳ 2^{Ω(d)}" [Thm. 3, p. 277].
SAY: But a single published release must prepare for all two to the d parity queries at once. Theorem 3 shows that, for most of them, the release looks almost the same whether every row has parity zero, so the true answer is zero, or every row has parity one, so the true answer is n. The most extreme difference possible, and the release cannot tell them apart, unless the database has exponentially many rows in d.

SHOW: The d-bit cube's points coloured by parity: two interleaved halves (salt-and-pepper).
Lemma 2 [p. 278]: "a random half looks like the whole space to an ε-private map". Then the hybrid
chain: replace rows one at a time from "any row" to "parity-0 row"; each step "+σ", total "nσ".
SAY: The proof reuses the chain trick. A random parity splits all possible rows into two interleaved halves, and Lemma 2 shows that a private randomized map can barely tell a random half from the whole space. So swap the rows one at a time, from any row at all, to rows of parity zero. Each swap barely moves the output, and even n swaps together barely move it. The same holds for parity one, so both databases look like the same thing.

SHOW: Randomized response: each person (icons) perturbs their own row locally before sending it;
no curator holds raw data. Caption: "Proposition 2: can't even learn one population parity unless
n ≳ 2^{d/3}" [p. 278].
SAY: Randomized response, where each person scrambles their own data before sending it, so nobody ever holds the raw data, is even more limited. Proposition 2 shows it cannot even estimate the population count for most such parities unless n is exponentially large.

SHOW: Quantifier reminder: "∀ one query: easy to sanitize for it" vs "∃ one release for most
queries: impossible". Final line: "Want broad accuracy + strong privacy? Keep a curator in the loop."
SAY: Careful with the quantifiers. For any one particular query, it is easy to design a one-shot release that answers it well. What is impossible is a single release that answers most of them. The lesson: if you want broad, flexible accuracy with strong privacy, keep the curator in the loop.

---

## S12 · What grew from this paper — `s12_legacy.py` · `Legacy`

SHOW: The S02 map returns, compressed to the left; THIS paper's card (YELLOW) moves to the centre.
Descendant cards appear to the right, each with an arrow labelled by the section it grew from:
"Dwork 2006 (ICALP): the name *differential privacy*".
"Dwork, Kenthapadi, McSherry, Mironov & Naor 2006: (ε, δ) — Gaussian noise allowed".
SAY: Let's return to our map and see what grew from this paper. The same year, Dwork gave the definition its lasting name: differential privacy. Another 2006 paper, with Kenthapadi, McSherry, Mironov and Naor, relaxed it to allow a tiny probability of failure, delta, which finally lets Gaussian noise in.

SHOW: "§3.3 metric spaces → Exponential mechanism (McSherry & Talwar 2007)";
"Thm 1 budget → Composition theorems (Dwork, Rothblum & Vadhan 2010)".
SAY: The metric space idea of section three point three became McSherry and Talwar's exponential mechanism. The privacy budget of Theorem 1 grew into a whole theory of composition, including the advanced composition theorem of Dwork, Rothblum and Vadhan.

SHOW: "§4 randomized response → Local DP: Google RAPPOR (2014), Apple (2016)";
"S(f) + noise inside SGD → DP-SGD (Abadi et al. 2016): clip each gradient = bound sensitivity".
SAY: The randomized response model of Section four became local differential privacy, deployed by Google in Chrome and by Apple on iPhones. And in 2016, Abadi and colleagues trained deep neural networks with differential privacy: clip each example's gradient, which bounds its sensitivity, then add noise. Calibrating noise to sensitivity, inside gradient descent.

SHOW: "US Census 2020: published statistics protected with DP"; a trophy: "Gödel Prize 2017".
SAY: For the 2020 census, the US Census Bureau protected its published statistics with differential privacy. And in 2017, this paper won the Gödel Prize, one of the highest honors in theoretical computer science.

---

## S13 · Recap and questions — `s13_recap.py` · `Recap`

SHOW: Four panels build up, each with its formula:
1 "Privacy: |ln(Pr[𝒯(x)=t]/Pr[𝒯(x′)=t])| ≤ ε" · 2 "Sensitivity: S(f) = max ‖f(x)−f(x′)‖₁" ·
3 "Laplace mechanism: f(x) + Lap(S(f)/ε)" · 4 "One-shot releases need n ≳ 2^{Ω(d)}".
SAY: Let's recap. One: privacy means that changing any one person's row changes the probability of any output by at most a factor of e to the epsilon. Two: a query's sensitivity is the most that one row can change its answer. Three: add Laplace noise with scale sensitivity over epsilon, and you are private, with error that does not grow with the size of the database. And four: one-shot sanitized releases cannot match what an interactive curator can do.

SHOW: Three "test yourself" questions appear (YELLOW header):
"Sensitivity of the average of n numbers in [0, 1]?" · "Ten counting queries at ε = 0.1 each: total
privacy loss?" · "Why does the median give the Laplace mechanism trouble?" ·
footer: "answers + exercises: exercises.md".
SAY: Some questions to test yourself. What is the sensitivity of the average of n numbers between zero and one? If you answer ten counting queries, each with epsilon of one tenth, what is your total privacy loss? And why does the median give the Laplace mechanism trouble? Answers and more exercises are in the companion notes.

SHOW: Final card: "What's the epsilon?" then the paper citation.
SAY: Next time someone tells you a dataset is safe because it is anonymized, you will know the better question to ask: what is the epsilon?
