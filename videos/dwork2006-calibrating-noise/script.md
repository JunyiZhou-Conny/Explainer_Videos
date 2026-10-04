# Calibrating Noise to Sensitivity — narration script & visual plan

Paper: C. Dwork, F. McSherry, K. Nissim, A. Smith. *Calibrating Noise to Sensitivity in Private
Data Analysis.* TCC 2006, LNCS 3876, pp. 265–284. (`library/privacy/differential-privacy/dwork2006calibrating.pdf`)

Audience: a smart newcomer — e.g. a PhD student in reinforcement learning or medical imaging —
comfortable with basic probability, who has never heard of differential privacy. Goal: intuition
first, then the exact statements from the paper; the viewer predicts before we reveal.

Conventions
- `SAY:` lines are spoken verbatim by the narrator (one `voiceover` block each) and become subtitles.
  Write numbers and symbols the way they should be *spoken* ("e to the epsilon", "one over n").
- `SHOW:` lines describe the visuals that accompany the following `SAY:` block.
- `PONDER(n s, "question")` inside a SHOW line: after that SAY block, show
  `pause_and_ponder(self, "question", seconds=n)` — a silent timer — then remove the card at the
  start of the next block.
- Semantic colours (keep them fixed for the whole video): analyst / attacker = PURPLE ·
  database **x** = BLUE · neighbouring database **x′** = ORANGE · Alice / the one changed row = PINK ·
  **ε** (privacy loss / budget) = YELLOW · sensitivity **S(f)** = GREEN · noise / Laplace = RED ·
  true answer = WHITE · secondary text = GREY · "this paper" highlight = YELLOW frame.
- Running example: in world **x** Alice's row says "no condition X" (count 41); in world **x′** it
  says "condition X" (count 42). So f(x) = 41 (BLUE), f(x′) = 42 (ORANGE) everywhere.
- One symbol for the mechanism on screen: **M** (footnote once in S04: "paper: 𝒯 = transcript,
  San = sanitizer"). Use "statistical distance" everywhere (the paper says "statistical difference").
- Paper references in brackets (e.g. [Def. 1, p. 270]) are for reviewers; they are not spoken.

---

## S01 · The differencing attack — `s01_hook.py` · `Hook`

SHOW: A grid of 120 person icons (15 × 8) labelled "Hospital database"; 41 PINK (have condition X),
plus the slot where Alice will arrive. A query card slides in: "How many patients have condition X?"
SAY: Here is a hospital database, one row per patient. A researcher asks an innocent question: how many patients have condition X? The hospital releases no records. It just says: forty-one.

SHOW: The answer "41" appears under the query. Then a new PINK icon labelled "Alice" slides into the
grid. The same query card fires again; the answer becomes "42".
SAY: A week later, one new patient, Alice, is admitted. The researcher asks again. The answer is now forty-two.

SHOW: "42 − 41 = 1" written out; a red tag "Alice has condition X" with an arrow to Alice.
PONDER(10 s, "Would rounding the count to the nearest ten protect Alice?")
SAY: Subtract, and the researcher has learned something very specific about Alice, without seeing a single record. Before we go on, try to fix this yourself. Pause and ponder: would rounding the count to the nearest ten protect Alice? Pause the video if you need more time.

SHOW: A number line 40–50 with a dashed rounding cut drawn between 44 and 45 (round half up): "x: 44" (BLUE) curves to "40"; with Alice, "x′: 45" (ORANGE) curves to "50" (RED flash). S05 reuses exactly this look.
SAY: Most weeks, yes. But if the count goes from forty-four to forty-five, the rounded answer jumps from forty to fifty, and Alice is exposed again. Any fixed rule that ever changes its answer has a jump like that somewhere.

SHOW: Everything fades except a large question mark; two short lines of text appear:
"What makes a statistic private?" / "How much noise is enough?"
SAY: So what would it even mean for a statistic to be private? And if the fix is to add noise, how much is enough?

SHOW: Page 1 of the actual paper (asset `paper_p1.png`) on the left; the title is boxed in YELLOW.
On the right: "Dwork · McSherry · Nissim · Smith", "TCC 2006", "Gödel Prize 2017".
SAY: In 2006, Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith answered both questions in this paper: Calibrating Noise to Sensitivity in Private Data Analysis. It founded what we now call differential privacy, and in 2017 it won the Gödel Prize.

SHOW: Heading "In this video"; four numbered idea cards appear one by one:
"1 · A definition of privacy" (YELLOW), "2 · Sensitivity" (GREEN), "3 · The Laplace mechanism"
(RED tent curve), "4 · Why one published table falls short" (GREY).
SAY: This video covers its three big ideas: a definition of privacy, a number called sensitivity, and a recipe for how much noise is enough. Plus a surprising limit on what one published table can achieve, if it must be private in this sense.

---

## S02 · Where this paper sits — `s02_map.py` · `LineageBefore`

SHOW: A "mentor map": three thin horizontal lanes over a shared 1960–2010 axis, GREY lane labels on
the left: "Randomize", "Attacks", "Provable noise". Lane 1, card "Warner 1965 · randomized response":
a person icon with a coin; branches "heads → truth", "tails → coin decides"; then a crowd's share of
"yes" settling near the true rate.
SAY: First, a map of where this paper comes from. In 1965, Stanley Warner proposed randomized response for sensitive surveys. In a popular version, you flip a coin in private. Heads, you answer truthfully. Tails, you flip again and say yes for heads, no for tails. Any single yes could be the coin talking, yet over thousands of people the true rate can still be estimated. Keep this coin in mind.

SHOW: Lane 1 continues: card "Statistical disclosure control (Denning 1980; Adam & Wortmann 1989)"
with two mini-icons "scramble inputs" (jittered rows) and "scramble outputs" (exact rows, noisy
answer); card "Evfimievski, Gehrke & Srikant 2003 · worst-case belief change".
SAY: Over the following decades, statisticians and computer scientists refined such tricks, in two flavours: scramble the data going in, or scramble the answers coming out.

SHOW: Lane 2: card "Sweeney · 'anonymous' ≠ anonymous": "ZIP + birth date + sex → most people
unique"; a voter list and a hospital table joined by a line, picking out one row ("the governor").
SAY: Meanwhile, the obvious fix, just remove the names, kept failing. Latanya Sweeney showed that ZIP code, birth date and sex alone single out most Americans, and in 1997 she linked supposedly anonymous hospital records to a public voter list and found the governor of Massachusetts. The lesson: privacy must be a property of the process, not of how the released table looks, and it must hold whatever else the attacker knows.

SHOW: Lane 2: card "Dinur & Nissim 2003 · too many accurate answers ⇒ reconstruction".
Mini-animation: queries hit a database; each answer has a tiny error bar "error ≪ √n"; the
attacker's copy of a 0/1 column fills in cell by cell until it matches; the S01 "42 − 41" fills the
first cell.
SAY: Then, in 2003, Irit Dinur and Kobbi Nissim proved something sobering. Answer too many questions too accurately, with errors much smaller than the square root of n, and an attacker can rebuild almost the entire database. Our subtraction was the two-question version of this attack. Noise is the price of answering many questions.

SHOW: Lane 3: cards "Dwork & Nissim 2004", "Blum, Dwork, McSherry & Nissim 2005 · SuLQ: sub-linear
queries, noisy sums"; caption "number of questions ≪ n".
SAY: The hopeful flip side: with a limited number of questions, modest noise is enough. Dwork, Nissim and colleagues built this into a framework called SuLQ, for sub-linear queries, which answers noisy sums like counts. Remember that limit on questions. This paper turns it into a budget.

SHOW: Each lane ends in an arrow into the YELLOW 2006 card "Dwork, McSherry, Nissim & Smith ·
TCC 2006", labelled with what it hands over: "randomness", "must survive any attacker", "noise you
can analyse". The card fills three slots: "one definition (ε)", "one number (S(f))", "one recipe
(Lap(S(f)/ε))". Caption: "TCC = a cryptography conference: define security first, then prove it".
SAY: But SuLQ only covered sums, and its definition tolerated a tiny chance of a large leak. This paper takes the leap: any function of the data, one clean definition, and one simple rule for the noise. Fittingly, it appeared at a cryptography conference, where the habit is to define security against every possible attacker first, and then prove it.

---

## S03 · The setup: a trusted curator — `s03_setup.py` · `Curator`

SHOW: Left: a vault/box labelled "database x" (BLUE) containing n rows (row stack). Middle: a
"curator" figure next to the box. Right: an "analyst" figure. An arrow from analyst to curator
carries "query f".
SAY: Here is the setting. A trusted server, the curator, holds a database x: n rows, one per person. An analyst sends a query f, any function of the database that returns a number, or a list of numbers.

SHOW: Inside the curator: "f(x)" computed (WHITE) but locked (a small lock icon — it never leaves).
A RED noise blob "Y" appears; the output "f(x) + Y" travels back to the analyst. More query arrows fly
in: "interactive: ask, answer, repeat". A faded GREY "published table" icon labelled
"non-interactive" appears beside the curator.
SAY: The curator never releases the honest answer, f of x. Instead it draws random noise, Y, and releases f of x plus Y. Because the analyst can keep asking, this is called the interactive setting. The alternative, publishing one sanitized table and walking away, is non-interactive. At the end, the paper proves the first is fundamentally more powerful.

SHOW: A dial labelled "noise": left end "too little → Alice exposed", right end "too much →
useless". Then the paper's title phrase appears: "Calibrate the noise to the sensitivity".
SAY: So everything hinges on one question: what distribution should Y have? Too little noise, and Alice is exposed. Too much, and the answer is useless. The title gives the answer: calibrate the noise to the sensitivity. But first, what does private actually mean?

---

## S04 · Defining privacy — `s04_definition.py` · `Definition`

SHOW: Two database row-stacks side by side, same number of rows: "x" (BLUE) and "x′" (ORANGE). All
rows identical except one row highlighted PINK (Alice): "no X" in x, "has X" in x′. A bracket
"neighbors: differ in one row". Under each: "count = 41" (BLUE) and "count = 42" (ORANGE).
SAY: The key move is to imagine two worlds. In one, the database is x. In the other, it is x prime: identical except for one row. Say, Alice's. Databases like this are called neighbors. In the hospital, Alice was added; here, her row just says something different. Either way, no single person's row should matter much.

SHOW: Each database feeds a mechanism box "M"; out come two smooth output distributions over a
shared horizontal axis "output t" — BLUE and ORANGE curves, heavily overlapping. Small GREY footnote:
"paper: 𝒯 = transcript, San = sanitizer".
SAY: Run the mechanism, the curator's randomized answering rule, in each world. Whatever the analyst gets to see, the paper calls the transcript; for now, a single noisy answer. Because the mechanism is random, each world gives a whole distribution of possible outputs.

SHOW: A point t slides along the axis; vertical lines up to both curves; a live readout
"BLUE height ÷ ORANGE height" (values near 1, e.g. 0.85 … 1.2) that stays inside a YELLOW band [e^{−ε}, e^{ε}].
SAY: Pick any output t, and compare the heights of the two curves there. Slide t along and watch their ratio. A private mechanism keeps that ratio close to one everywhere: never above e to the epsilon, never below e to the minus epsilon.

SHOW: Definition 1 written as a caption for what was just seen [Def. 1, p. 270]:
|ln( Pr[M(x)=t] / Pr[M(x′)=t] )| ≤ ε — numerator BLUE, denominator ORANGE, ε YELLOW; Indicate
|ln(·)| when it is spoken. Caption "for all neighbors x, x′, all analysts, all outputs t";
note "small ε: e^ε ≈ 1 + ε".
SAY: That is the paper's definition, which it calls epsilon-indistinguishability. The log of the ratio is the privacy loss at t. For every pair of neighbors, every analyst and every output, it must be at most epsilon in absolute value. The absolute value makes it symmetric: a ratio of two and a ratio of one half count the same. For small epsilon, e to the epsilon is about one plus epsilon.

SHOW: PONDER(12 s, "Warner's coin: what is its ε?") — the coin diagram from S02 returns on the left.
SAY: Let's test it on Warner's coin from our map. Pause and ponder: if Alice's true answer is yes, how likely is she to say yes? And if it is no?

SHOW: Table: "truth yes → says yes w.p. 1/2 + 1/4 = 3/4" · "truth no → says yes w.p. 1/4";
"3/4 ÷ 1/4 = 3"; "ε = ln 3 ≈ 1.1" in YELLOW.
SAY: If the truth is yes, she says yes three quarters of the time: heads, or tails then heads. If it is no, only the second coin can say yes: one quarter. The worst ratio is three, so the coin satisfies the definition with epsilon equal to the log of three, about one point one.

SHOW: An attacker icon looking at the output t: "posterior odds = prior odds × (BLUE height ÷ ORANGE
height)", the ratio clamped in the YELLOW band. Then a small table "start 50/50 between the two
worlds → at most": "ε = 0.1: 52.5%" · "ε = 0.5: 62%" · "ε = 1: 73%" · "coin, ε = ln 3: 75%".
Label "ε is set by policy — the paper calls it the leakage".
SAY: Now be the attacker, trying to tell the two worlds apart. By Bayes' rule, your new odds are your old odds times exactly this ratio, so they move by at most a factor of e to the epsilon, whatever you knew before. Starting from fifty-fifty, epsilon one tenth leaves you at most fifty-two and a half percent sure; epsilon one, at most seventy-three. Epsilon is set by policy; the paper calls it the leakage.

SHOW: A small vignette: "Study finds: smokers get more heart disease". Alice (PINK) with a cigarette
icon; "Her insurer now worries" — then Alice's row is swapped for a stranger's and the same headline
still appears: "would happen even with Alice's row replaced ✓ not a privacy breach" [p. 267, App. A].
SAY: Notice what this does not promise. If a study reveals that smokers get more heart disease, and Alice smokes, people may now think she is at higher risk. That is not a privacy violation: the same lesson could be learned from everyone else's data, so it would happen even if Alice's row were replaced by someone else's.

---

## S05 · Why so strict? — `s05_strict.py` · `WhyStrict`

SHOW: Title "Why a ratio, for every output?". Two nearly identical curves with the area between them
shaded: "statistical distance = ½ × shaded area".
SAY: Why demand a ratio bound for every single output? Cryptography often settles for something weaker: statistical distance, half the area between the two curves. Equivalently, the most the probability of any event can differ between the worlds. The paper shows why that is not enough here.

SHOW: Database row-stack (n rows). A random pointer spins and lands on a row; the whole row is copied
out as the published output "(name, value)". Caption: "Mechanism: publish one random row"
[Example 2, p. 271]. Then the output distribution as a bar chart over outputs "(Bob, no) (Bob, has)
… (Alice, no) (Alice, has)": BLUE and ORANGE bars coincide except at Alice's two outputs; "statistical
distance = 1/n (tiny)".
SAY: Consider this mechanism: pick one row at random and publish it, word for word. Change one person's row, and the output distribution moves by only one over n. For a big database that is tiny, so by the averaged measure this looks private.

SHOW: Zoom into the bar "(Alice, has)": "world x′: 1/n" vs "world x: 0"; "1/n ÷ 0 = ∞" in RED; a big
RED ✗ over "privacy".
SAY: But every output is somebody's complete record. The ratio test catches it: the output showing Alice's real value has probability one over n in one world, and zero in the other. The ratio is infinite.

SHOW: Text: "Averages hide catastrophes that are rare for each person." Then the S01 rounding number
line returns: at the jump, "probability 1 vs 0 → ∞"; caption "to pass the ratio test, a mechanism
must be random".
SAY: Averages let catastrophes slip through, as long as each is rare for any single person. A ratio bound rules them out everywhere. It also settles our rounding question: at the jump, one world gives that answer with probability one, the other with probability zero. To pass this test, a mechanism has to be random.

---

## S06 · Sensitivity — `s06_sensitivity.py` · `Sensitivity`

SHOW: A function machine "f" taking a database to a number line. Swap one row (PINK) and the
output dot moves; the gap is marked. Then the definition (S in GREEN) [Def. 2, p. 271]:
S(f) = max over neighbors x, x′ of |f(x) − f(x′)|.
SAY: So how much noise do we need? It depends on a single property of the query: its sensitivity, the most that changing one row can ever change the answer, over all pairs of neighboring databases, including ones that do not exist yet.

SHOW: Counting query: the hospital count 41 → 42 when Alice's row flips; "S(count) = 1".
SAY: For a counting query, like our hospital count, one row changes the answer by at most one. Sensitivity one.

SHOW: A histogram with 5 bins; Alice (PINK) hovering above it. PONDER(8 s, "If Alice's row changes,
how much can the whole histogram change in total? Does it depend on the number of bins?")
SAY: Now a histogram: split the possible values of a row into d bins, and release how many rows fall in each. Before I show you, pause: if Alice's row changes, how much can the whole histogram change in total? Does it depend on the number of bins?

SHOW: Alice moves from bin 2 to bin 4: one bar drops by 1, another rises by 1 → "|−1| + |+1| = 2".
The definition morphs |·| into ‖·‖₁ ("‖v‖₁ = |v₁| + |v₂| + …"). Then the histogram morphs into 20
bins, then 60 thin bins; "S = 2" stays put [Example 3, p. 271–272].
SAY: She moves out of one bin and into another: one count goes down by one, another goes up by one. Total change: two. Adding up absolute changes across coordinates like this is the L1 norm, the paper's way to measure sensitivity for lists of numbers. And it is two whether there are five bins or five thousand. It does not depend on the dimension at all.

SHOW: Contrast (marked "illustration"): "largest income in the database". One extreme row (a gold
coin stack) drags the answer far right; "S huge" in GREEN. Then a cap line slices the stack at "1M":
"cap every value → S ≤ 1M".
SAY: Contrast that with: what is the largest income in the database? One billionaire can move that answer by a billion, and with no cap there is no limit at all. The standard fix is to cap every value, say at a million, first. Remember that trick: it is exactly what private deep learning does to gradients.

SHOW: Two labelled boxes: "ε — a choice (policy)" in YELLOW and "S(f) — a fact about f" in GREEN.
"S(f) does not depend on the actual database".
SAY: Two things to remember. Sensitivity is a property of the function alone, not of the particular database, and it is not chosen by policy. Epsilon is a choice. Sensitivity is a fact.

---

## S07 · The Laplace mechanism — `s07_laplace.py` · `LaplaceMechanism`

SHOW: Axes; the Laplace density (RED) drawn as a sharp tent-shaped peak. Formula
h(y) ∝ e^{−|y|/λ}, with λ labelled "scale"; λ is dialled wider and narrower.
SAY: Now for the noise. The paper uses the Laplace distribution: symmetric, sharply peaked, and falling off exponentially with distance from the center. Its width is set by a scale parameter, lambda.

SHOW: Two Laplace curves, BLUE centred at f(x) = 41 and ORANGE centred at f(x′) = 42 (λ = 1).
SAY: Here is the trick. Center one Laplace curve at f of x, forty-one, and another at f of x prime, forty-two: the output distributions of our two worlds.

SHOW: A second axis below: the log of the ratio of the two densities, swept out as t moves left to
right — flat at +1/λ for t ≤ 41, a straight ramp between 41 and 42, flat at −1/λ for t ≥ 42. A YELLOW
band from −1/λ to +1/λ contains it.
SAY: Now plot the log of their ratio for every output t. To the left of forty-one, it is exactly constant. To the right of forty-two, constant again. In between, a straight ramp. It never rises above one over lambda, and never falls below minus one over lambda: the shift, divided by the scale.

SHOW: Switch the top plot to log-density: each Laplace becomes a "tent" of two straight lines, each
side labelled "slope ±1/λ". Slide the ORANGE tent from 41 to 42: the vertical gap between the tents
is shown never exceeding 1/λ.
SAY: Why? On a log scale, a Laplace density is a tent whose sides have slope one over lambda, never steeper. Slide the tent over, and the gap between the tents can never exceed the slide times that slope. That is the whole design principle: privacy needs noise whose log density is never steep.

SHOW: One-line proof (colours: S GREEN, ε YELLOW); beside it a number line with t, f(x), f(x′) and
two distance brackets showing "|t−f(x′)| − |t−f(x)| ≤ |f(x)−f(x′)|":
|ln[h(t−f(x)) / h(t−f(x′))]| = | |t−f(x′)| − |t−f(x)| |/λ ≤ |f(x)−f(x′)|/λ ≤ S(f)/λ.
Then substitute λ = S(f)/ε ⇒ ≤ ε. Box it.
SAY: In symbols: two distances to t can differ by at most the distance between the centers. So the privacy loss of any output is at most the sensitivity divided by lambda. Set lambda to the sensitivity over epsilon, and the ratio stays within e to the epsilon, for every output and every pair of neighbors. Privacy, proven in one line.

SHOW: Proposition 1 card [p. 272]: M(x) = f(x) + (Y₁, …, Y_d), Yᵢ ~ Lap(S(f)/ε) i.i.d.
Small 2-D picture: joint density contours are diamonds (L1 balls) around two nearby centres.
SAY: If the query returns several numbers, add independent Laplace noise to each. The joint density then depends on the L1 distance, which is exactly why sensitivity is measured in the L1 norm. That is Proposition 1: Laplace noise of scale S of f over epsilon in every coordinate.

SHOW: PONDER(10 s, "Why not uniform noise, anywhere between −10 and +10?")
SAY: Pause and ponder: why not something simpler, like uniform noise anywhere between minus ten and plus ten?

SHOW: Two boxes on one axis: BLUE [31, 51] and ORANGE [32, 52]; the output 51.5 lights up: ORANGE > 0,
BLUE = 0, "∞" in RED, with a thumbnail of the S05 random-row ✗.
SAY: Look at the edges. An output of fifty-one and a half is possible if the true count is forty-two, but impossible if it is forty-one: the same infinite ratio that sank the random-row mechanism. Good noise must never rule an output out.

SHOW: Compare with a Gaussian (GREY) [not from the paper]: its log-ratio is a straight line that
leaves the YELLOW band in both tails (RED overflow arrows), while the Laplace log-ratio stays inside.
SAY: And why not the familiar bell curve? On a log scale a Gaussian is a parabola, steeper and steeper, so the gap between two shifted parabolas grows without bound. In the tails the ratio explodes, and no single epsilon works. Hold on to that Gaussian, though: it comes back, and it is the noise you would actually use to train a neural network privately.

SHOW: Title-style summary: "noise scale = S(f) / ε" (S GREEN, ε YELLOW); lines: "more sensitive
question → more noise", "stronger privacy (smaller ε) → more noise".
SAY: So here is the recipe in the title: noise scale equals sensitivity divided by epsilon. A more sensitive question needs more noise. Stronger privacy needs more noise.

---

## S08 · Privacy for individuals, accuracy for populations — `s08_payoff.py` · `Payoff`

SHOW: Back to the hospital query. ε = 0.5 ⇒ Laplace scale 2. Week 1: true 41 → released "43.7";
week 2: true 42 → released "40.6". Two broad overlapping Laplace curves (BLUE at 41, ORANGE at 42).
Then "40.6 − 43.7 = −3.1"; the S01 arrow from the difference to Alice appears and is crossed out in
RED; annotation "50/50 → at most 62%".
SAY: Back to the hospital, with epsilon one half: Laplace noise of scale two. Week one, the curator reports about forty-three point seven. Week two, when the true count is forty-two, about forty point six. Subtract as before, and Alice seems to have lowered the count by three. A fifty-fifty guess about her can now move to at most about sixty-two percent.

SHOW: Highlight "scale = S(f)/ε" — circle the two inputs; a crossed-out "n".
SAY: Now look at what the noise scale depends on: the sensitivity and epsilon. Not the size of the database.

SHOW: Three number lines stacked: n = 100 (true count ≈ 50), n = 10,000 (≈ 5,000), n = 1,000,000
(≈ 500,000), each centred on the true answer; the RED noise band is the same absolute width
("typical noise ≈ 2", never labelled as a standard deviation) and becomes visually negligible;
labels "≈ 4%", "≈ 0.04%", "≈ 0.0004%".
SAY: With a hundred patients, noise of typical size two is a few percent of the answer. With a million, it is a rounding error. Alice is protected by noise that is large compared to her own contribution, which is one, but tiny compared to the population's.

SHOW: Two-line slogan: "Privacy for individuals. Accuracy for populations."
SAY: Privacy for individuals. Accuracy for populations. That is the bargain.

SHOW: PONDER(12 s, "Noise ≈ 1/ε. What goes wrong if ε is much smaller than 1/n?")
SAY: Here is one you can answer yourself. Pause and ponder: the noise has size about one over epsilon. What goes wrong if epsilon is much smaller than one over n?

SHOW: The noise band swells past the whole range 0…n. Then a chain of databases x = x⁽⁰⁾ → x⁽¹⁾ → …
→ x⁽ⁿ⁾ = y, one row changing per step (PINK), each arrow "× e^ε", total "≤ e^{nε} ≈ 1": "all
databases look alike ⇒ nothing can be learned" [p. 271]. Label "hybrid argument".
SAY: The noise outgrows n, bigger than the count could ever be, and the answer is pure noise. This is not Laplace's fault. Any two databases are linked by a chain of at most n single-row changes, each changing probabilities by at most e to the epsilon, so the ends differ by at most e to the n epsilon. If n epsilon is tiny, every database looks alike, and nothing can be learned. This chain trick is called a hybrid argument, and it comes back at the end.

---

## S09 · Many questions: the privacy budget — `s09_budget.py` · `Budget`

SHOW: Analyst asks f₁ → a₁; the next query f₂ visibly depends on a₁ (an arrow from a₁ into f₂);
then f₃ … A strip labelled "transcript" builds: [a₁, a₂, a₃, …].
SAY: One question is never enough. Real analysts ask many, adaptively, each chosen after seeing earlier answers. Maybe you spot a spike in one bin, and zoom in.

SHOW: [Thm. 1, p. 273] The transcript probability as a product with two kinds of factors: GREY
"analyst picks the next question (same in both worlds)" — struck through as it cancels in the ratio —
and curator factors "Pr[aᵢ | earlier; x] ÷ Pr[aᵢ | earlier; x′] ≤ e^{|Δᵢ|/λ}", caption
"Δᵢ = how much question i's true answer differs between x and x′". Then the product becomes a sum in
the exponent: "exp(Σ|Δᵢ|/λ) = exp(‖fₜ(x) − fₜ(x′)‖₁/λ) ≤ e^ε when λ = maxₜ S(fₜ)/ε".
SAY: The paper's Theorem 1 handles this. Write the probability of the whole transcript as a product, step by step. The analyst's choice of the next question is the same in both worlds, so in the ratio it cancels, leaving one Laplace ratio per answer. If you know reinforcement learning, this is the trajectory-ratio trick: whatever is identical in both worlds cancels, and the per-step log ratios add up.

SHOW: A YELLOW "privacy budget ε" bar. Each answered query drains a segment. When it is empty, the
curator shows "refused". A mini Dinur–Nissim card flies in from the map and docks next to the bar.
GREY caption: "refusing depends only on the queries' sensitivity, not the data".
SAY: So privacy losses add up, and epsilon behaves like a budget. Each answer spends part of it; once it is spent, the curator stops. That is the answer to Dinur and Nissim: the budget makes the limit on questions explicit and measurable.

SHOW: PONDER(12 s, "d bins, total budget ε. Each bin as its own counting query, budget split
evenly: noise per bin?")
SAY: You can now compute a real saving yourself. Pause: a histogram with d bins, total budget epsilon. Treat each bin as its own counting query and split the budget evenly. How much noise does each bin get?

SHOW: Two noisy histograms of the same data, d = 100 bins (seeded noise). Left "d separate queries":
"Lap(d/ε) per bin". Right "one query, S = 2": "Lap(2/ε) per bin". Small GREY note: "earlier SuLQ
analysis: ~√d/ε per bin — still grows with d" [§3.2, p. 273].
SAY: Each bin gets one over d of the budget, so noise of scale d over epsilon. Treated as one query with sensitivity two, each bin gets two over epsilon, whatever d is. The earlier framework's sharper analysis got this down to about the square root of d, but it still grew with d.

---

## S10 · Beyond counting — `s10_beyond.py` · `BeyondCounting`

SHOW: Three tiles that light up (and grow) in turn: "Distance to a property", "Small random
samples", "Outputs that aren't numbers".
SAY: Sensitivity reaches far beyond counts. Three examples from the paper.

SHOW: Tile 1: a small social network; caption "each possible link = one row (present / absent)"; the
minimum cut highlighted (RED dashed line) with its size; one link changes and the cut changes by at
most 1; label "min cut is 1-sensitive" [p. 274]. Then: "how many rows must change to make P true?
→ sensitivity 1".
SAY: First, picture a social network where each possible link is one row of the database. How many links must you cut to split the network in two? That minimum cut moves by at most one when one link changes, so it is one-sensitive. In general, any question of the form, how many rows would you have to change to make something true, has sensitivity one.

SHOW: Tile 2: a big crowd; a small random sample is highlighted; Alice is usually not in it.
"Lemma 1: if A reads each row with probability ≤ α and is within σ of f most of the time, on every
database ⇒ S(f) ≤ 2σ" [p. 275].
SAY: Second: if an algorithm that rarely looks at any particular row, like one working from a small random sample, approximates f to within sigma most of the time, on every database, then f has sensitivity at most two sigma. That is Lemma 1.

SHOW: Tile 3: a bit string whose bits flicker, and a cloud of candidate outputs shaded by
weight exp(−ε·dist(y, f(x)) / 2S) — brighter near the true answer [Thm. 2, p. 276; sign corrected,
the paper's Eqn. 4 omits the minus]. Caption "rankings, sets, bit strings: anything with a distance".
SAY: Third, the answer need not be a number: a ranking, a set, a string of bits, anything with a distance between answers. Pick an output with probability that decays exponentially with its distance from the true answer, at a rate of epsilon over twice the sensitivity. For bit strings, that flips each bit with probability a little below one half: Warner's coin again, applied to the answer.

---

## S11 · Interactive vs. one-shot releases — `s11_separation.py` · `Separation`

SHOW: Split screen. Left "Interactive": curator answering a stream of queries. Right
"Non-interactive": curator publishes a sanitized table "M(x)" once, then walks away; many users
query the table.
SAY: Now the last part of the paper. Statisticians and data miners traditionally prefer the non-interactive model: sanitize the data once, publish it, and let anyone compute anything. Can that work under this definition?

SHOW: Rows as d-bit strings (a small table, d = 8). Each row gets its own random mask (highlighted
bit positions, different per row); for each row, the parity of its masked bits is shown (0 = even,
1 = odd). Caption: "query: how many rows have odd parity inside their own mask?", "sensitivity 1".
On the left, the interactive curator answers it with "± 1/ε".
SAY: The paper proves a striking limit. Let each row be a string of d bits. Here is a family of simple counting queries: give each row its own mask, a subset of bit positions, and count the rows with an odd number of ones inside their mask. Each query has sensitivity one, so an interactive curator can answer any one of them with noise of about one over epsilon.

SHOW: A fan of many mask-sets. Two random databases: "every row even → answer 0" vs "every row odd →
answer n"; both feed M; the two outputs look nearly identical ("statistical distance ≈ 0", with a
thumbnail of the S05 shaded area). Caption [Thm. 3, p. 277]: "for ≥ 2/3 of the queries:
statistical distance O(n^{4/3} ε^{2/3} 2^{−d/3}) — tiny unless n is exponential in d (roughly
n > 2^{d/4}/√ε)".
SAY: But a one-shot release must prepare for all of them at once. Theorem 3 shows that for at least two thirds of these queries, the release looks almost the same for a random database where every row has even parity, true answer zero, as for one where every row is odd, true answer n. The most extreme difference possible, and it cannot be seen, unless the database is exponentially large: roughly, every four extra bits per row doubles the rows you would need.

SHOW: PONDER(10 s, "Couldn't an analyst ask the interactive curator all of these queries too?")
SAY: Pause and ponder: couldn't an analyst just ask the interactive curator all of these queries too?

SHOW: The S09 YELLOW budget bar empties after a handful of parity queries; "refused".
SAY: No: the budget would run out. The curator only has to answer the few questions someone actually asks, chosen later. A published release cannot know which few those will be, so it must be ready for all of them at once. That is where it breaks.

SHOW: A small "proof idea" tag. The d-bit cube's points coloured by parity under one random mask:
two interleaved halves (salt-and-pepper); one half highlighted as "a random poll of all rows"
[Lemma 2, p. 278]. Then the hybrid chain from S08: start from n completely random rows; replace them
one at a time by even-parity rows (each under its own mask); each step "+σ", total "nσ" — small
unless n is huge. The same for odd parity; both ends meet at "completely random rows".
SAY: The proof idea uses two facts. Privacy forces the release to treat every possible row almost alike. And a random mask splits all rows into two halves mixed like salt and pepper, so the even half is like a random poll of everything. Then the chain trick: start from completely random rows, and swap them one at a time for even ones. Each swap barely moves the output, and unless n is huge, all n swaps together barely move it. The same goes for odd rows, so both databases look like random rows.

SHOW: The Warner coin icon from S02 flies in next to a picture of each person scrambling their own
row locally; no curator holds raw data. Caption [Prop. 2, p. 278]: "same mask for every row: for
most masks, can't learn the fraction with odd parity unless n ≳ 2^{d/3}/ε^{2/3}".
SAY: Warner's coin, randomized response, where each person scrambles their own row so nobody holds the raw data, is even more limited. Proposition 2: even when every row uses the same mask, for most masks it cannot estimate the odd count unless n is exponentially large.

SHOW: Two lines in words: "Any ONE query, known in advance → easy to publish for ✓" vs "ONE private
release that works for MOST queries → impossible unless n is huge ✗". Final line: "Want broad
accuracy + strong privacy? Keep a curator in the loop."
SAY: Careful with the quantifiers. For any one query known in advance, a one-shot release can answer it well. What is impossible, unless the database is exponentially large, is one private release that answers most of them. The lesson: for broad, flexible accuracy with strong privacy, keep the curator in the loop.

---

## S12 · What grew from this paper — `s12_legacy.py` · `Legacy`

SHOW: The S02 lanes return, compressed to the left; THIS paper's card (YELLOW, with its four idea
slots coloured YELLOW/GREEN/RED/GREY) moves to the centre. Descendant cards grow to the right, each
arrow leaving from the matching idea slot and carrying a thumbnail of the scene it echoes:
"Dwork 2006 (ICALP): the name *differential privacy*"; "Dwork, Kenthapadi, McSherry, Mironov & Naor
2006: (ε, δ)" ← thumbnail of the Gaussian escaping the band (S07).
SAY: Back to our map, to see what grew from this paper. The same year, in an invited paper titled simply Differential Privacy, Dwork introduced the name the field still uses. Another 2006 paper, with Kenthapadi, McSherry, Mironov and Naor, added a tiny slack, delta. Remember the Gaussian whose ratio escaped the band in the tails? Delta pays for those rare tails, and lets the bell curve back in.

SHOW: "Exponential mechanism (McSherry & Talwar 2007)" ← bit-flip tile (S10); "Composition theorems
(Dwork, Rothblum & Vadhan 2010): loss of k questions ~ √k" ← budget bar (S09).
SAY: Scoring every possible answer became McSherry and Talwar's exponential mechanism. The privacy budget grew into a theory of composition, with a surprise from Dwork, Rothblum and Vadhan: allow that tiny delta, and the total loss of k questions grows only like the square root of k.

SHOW: "Local DP: Google RAPPOR (2014), Apple (2016)" ← Warner's coin (S02/S11).
SAY: Warner's coin, the model Section four showed is most limited, is what we now call local differential privacy, used by Google in Chrome and by Apple on iPhones. Why the weakest model? Nobody has to be trusted with the raw data, and with millions of users, a few simple statistics can afford the noise.

SHOW: "DP-SGD (Abadi et al. 2016): clip each example's gradient (= the income cap, S06) + Gaussian
noise, budget tracked over thousands of steps"; card "Membership inference (Shokri et al. 2017):
the differencing attack, against models".
SAY: In 2016, Abadi and colleagues made it practical to train deep networks privately: clip each example's gradient, like our income cap, which bounds its sensitivity; add Gaussian noise; and track the budget over thousands of steps. If you train models on patient data, this is your entry point. A trained network is just another f of x, and attacks that ask whether a patient was in the training set are our subtraction attack, scaled up.

SHOW: "US Census 2020: published tables protected with DP (a few counts, e.g. state totals, exact)".
PONDER(8 s, "The Census published one release. Does Section 4 forbid it?")
SAY: And for the 2020 census, the US Census Bureau protected its published tables with differential privacy; only a few counts, like state populations, were exact. But that is a one-shot release. Pause and ponder: does Section four forbid it?

SHOW: The two quantifier lines from S11, the first one ticked: "a fixed set of tables chosen in
advance ✓". A trophy, silently: "Gödel Prize 2017 · TCC Test-of-Time Award 2016". Last card:
"Still open: choosing ε in practice · when no one can be trusted with the data".
SAY: No. The Census tuned its release for a fixed set of tables chosen in advance. Section four only rules out one release that is accurate for most of a huge family of questions.

---

## S13 · Recap and questions — `s13_recap.py` · `Recap`

SHOW: Four panels build up, each with its formula (reuse the exact formulas/colours from S04, S06,
S07, S11): 1 "Privacy: |ln(Pr[M(x)=t]/Pr[M(x′)=t])| ≤ ε" · 2 "Sensitivity: S(f) = max ‖f(x)−f(x′)‖₁"
· 3 "Laplace mechanism: f(x) + Lap(S(f)/ε)" · 4 "One published table: most parity counts need
exponentially many rows".
SAY: Let's recap. One: privacy means changing any one person's row changes the probability of any output by at most a factor of e to the epsilon. Two: a query's sensitivity is the most one row can change its answer. Three: Laplace noise with scale sensitivity over epsilon makes it private, with error that does not grow with the database. Four: one private published table cannot answer most simple parity counts unless the database is exponentially large.

SHOW: Header "Test yourself" (YELLOW). Question card 1: "Sensitivity of the average of n numbers in
[0, 1]?" PONDER(8 s, "Sensitivity of the average of n numbers in [0, 1]?")
SAY: Some questions to test yourself; pause after each. First: what is the sensitivity of the average of n numbers between zero and one?

SHOW: Question card 2: "Each patient contributes 50 slices; each slice's gradient is clipped to size
C. How much can one patient change the summed gradient?" PONDER(10 s, same text)
SAY: Second: in a medical imaging dataset, each patient contributes fifty slices, and each slice's gradient is clipped to size C. How much can one patient change the summed gradient?

SHOW: Question card 3: "Why does the median give the Laplace mechanism trouble?" PONDER(8 s, same
text); footer "answers + more exercises: companion notes (exercises.md)".
SAY: Third: why does the median give the Laplace mechanism trouble? Answers, and more exercises, are in the companion notes.

SHOW: Final card: "What's the epsilon? · What counts as one person's row?" then the paper citation.
SAY: Next time someone says a dataset is safe because it is anonymized, you will know the better questions: what is the epsilon, and what counts as one person's row?
