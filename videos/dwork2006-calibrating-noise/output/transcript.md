# Calibrating Noise to Sensitivity — the paper that invented differential privacy

## 00:00 — The differencing attack
Here is a hospital database, one row per patient. A researcher asks an innocent question: how many patients have condition X? The hospital releases no records. It just says: forty-one.
A week later, one new patient, Alice, is admitted. The researcher asks again. The answer is now forty-two.
Subtract, and the researcher has learned something very specific about Alice, without seeing a single record. Before we go on, try to fix this yourself. Pause and ponder: would rounding the count to the nearest ten protect Alice? Pause the video if you need more time.
Most weeks, yes. But if the count goes from forty-four to forty-five, the rounded answer jumps from forty to fifty, and Alice is exposed again. Any fixed rule that ever changes its answer has a jump like that somewhere.
So what would it even mean for a statistic to be private? And if the fix is to add noise, how much is enough?
In 2006, Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith answered both questions in this paper: Calibrating Noise to Sensitivity in Private Data Analysis. It founded what we now call differential privacy, and in 2017 it won the Gödel Prize.
This video covers its three big ideas: a definition of privacy, a number called sensitivity, and a recipe for how much noise is enough. Plus a surprising limit on what one published table can achieve, if it must be private in this sense.

## 01:40 — Where this paper sits
First, a map of where this paper comes from. In 1965, Stanley Warner proposed randomized response for sensitive surveys. In a popular version, you flip a coin in private. Heads, you answer truthfully. Tails, you flip again and say yes for heads, no for tails. Any single yes could be the coin talking, yet over thousands of people the true rate can still be estimated. Keep this coin in mind.
Over the following decades, statisticians and computer scientists refined such tricks, in two flavours: scramble the data going in, or scramble the answers coming out.
Meanwhile, the obvious fix, just remove the names, kept failing. Latanya Sweeney showed that ZIP code, birth date and sex alone single out most Americans, and in 1997 she linked supposedly anonymous hospital records to a public voter list and found the governor of Massachusetts. The lesson: privacy must be a property of the process, not of how the released table looks, and it must hold whatever else the attacker knows.
Then, in 2003, Irit Dinur and Kobbi Nissim proved something sobering. Answer too many questions too accurately, with errors much smaller than the square root of n, and an attacker can rebuild almost the entire database. Our subtraction was the two-question version of this attack. Noise is the price of answering many questions.
The hopeful flip side: with a limited number of questions, modest noise is enough. Dwork, Nissim and colleagues built this into a framework called SuLQ, for sub-linear queries, which answers noisy sums like counts. Remember that limit on questions. This paper turns it into a budget.
But SuLQ only covered sums, and its definition tolerated a tiny chance of a large leak. This paper takes the leap: any function of the data, one clean definition, and one simple rule for the noise. Fittingly, it appeared at a cryptography conference, where the habit is to define security against every possible attacker first, and then prove it.

## 03:45 — The setup: a trusted curator
Here is the setting. A trusted server, the curator, holds a database x: n rows, one per person. An analyst sends a query f, any function of the database that returns a number, or a list of numbers.
The curator never releases the honest answer, f of x. Instead it draws random noise, Y, and releases f of x plus Y. Because the analyst can keep asking, this is called the interactive setting. The alternative, publishing one sanitized table and walking away, is non-interactive. At the end, the paper proves the first is fundamentally more powerful.
So everything hinges on one question: what distribution should Y have? Too little noise, and Alice is exposed. Too much, and the answer is useless. The title gives the answer: calibrate the noise to the sensitivity. But first, what does private actually mean?

## 04:39 — Defining privacy
The key move is to imagine two worlds. In one, the database is x. In the other, it is x prime: identical except for one row. Say, Alice's. Databases like this are called neighbors. In the hospital, Alice was added; here, her row just says something different. Either way, no single person's row should matter much.
Run the mechanism, the curator's randomized answering rule, in each world. Whatever the analyst gets to see, the paper calls the transcript; for now, a single noisy answer. Because the mechanism is random, each world gives a whole distribution of possible outputs.
Pick any output t, and compare the heights of the two curves there. Slide t along and watch their ratio. A private mechanism keeps that ratio close to one everywhere: never above e to the epsilon, never below e to the minus epsilon.
That is the paper's definition, which it calls epsilon-indistinguishability. The log of the ratio is the privacy loss at t. For every pair of neighbors, every analyst and every output, it must be at most epsilon in absolute value. The absolute value makes it symmetric: a ratio of two and a ratio of one half count the same. For small epsilon, e to the epsilon is about one plus epsilon.
Let's test it on Warner's coin from our map. Pause and ponder: if Alice's true answer is yes, how likely is she to say yes? And if it is no?
If the truth is yes, she says yes three quarters of the time: heads, or tails then heads. If it is no, only the second coin can say yes: one quarter. The worst ratio is three, so the coin satisfies the definition with epsilon equal to the log of three, about one point one.
Now be the attacker, trying to tell the two worlds apart. By Bayes' rule, your new odds are your old odds times exactly this ratio, so they move by at most a factor of e to the epsilon, whatever you knew before. Starting from fifty-fifty, epsilon one tenth leaves you at most fifty-two and a half percent sure; epsilon one, at most seventy-three. Epsilon is set by policy; the paper calls it the leakage.
Notice what this does not promise. If a study reveals that smokers get more heart disease, and Alice smokes, people may now think she is at higher risk. That is not a privacy violation: the same lesson could be learned from everyone else's data, so it would happen even if Alice's row were replaced by someone else's.

## 07:23 — Why so strict?
Why demand a ratio bound for every single output? Cryptography often settles for something weaker: statistical distance, half the area between the two curves. Equivalently, the most the probability of any event can differ between the worlds. The paper shows why that is not enough here.
Consider this mechanism: pick one row at random and publish it, word for word. Change one person's row, and the output distribution moves by only one over n. For a big database that is tiny, so by the averaged measure this looks private.
But every output is somebody's complete record. The ratio test catches it: the output showing Alice's real value has probability one over n in one world, and zero in the other. The ratio is infinite.
Averages let catastrophes slip through, as long as each is rare for any single person. A ratio bound rules them out everywhere. It also settles our rounding question: at the jump, one world gives that answer with probability one, the other with probability zero. To pass this test, a mechanism has to be random.

## 08:31 — Sensitivity
So how much noise do we need? It depends on a single property of the query: its sensitivity, the most that changing one row can ever change the answer, over all pairs of neighboring databases, including ones that do not exist yet.
For a counting query, like our hospital count, one row changes the answer by at most one. Sensitivity one.
Now a histogram: split the possible values of a row into d bins, and release how many rows fall in each. Before I show you, pause: if Alice's row changes, how much can the whole histogram change in total? Does it depend on the number of bins?
She moves out of one bin and into another: one count goes down by one, another goes up by one. Total change: two. Adding up absolute changes across coordinates like this is the L1 norm, the paper's way to measure sensitivity for lists of numbers. And it is two whether there are five bins or five thousand. It does not depend on the dimension at all.
Contrast that with: what is the largest income in the database? One billionaire can move that answer by a billion, and with no cap there is no limit at all. The standard fix is to cap every value, say at a million, first. Remember that trick: it is exactly what private deep learning does to gradients.
Two things to remember. Sensitivity is a property of the function alone, not of the particular database, and it is not chosen by policy. Epsilon is a choice. Sensitivity is a fact.

## 10:12 — The Laplace mechanism
Now for the noise. The paper uses the Laplace distribution: symmetric, sharply peaked, and falling off exponentially with distance from the center. Its width is set by a scale parameter, lambda.
Here is the trick. Center one Laplace curve at f of x, forty-one, and another at f of x prime, forty-two: the output distributions of our two worlds.
Now plot the log of their ratio for every output t. To the left of forty-one, it is exactly constant. To the right of forty-two, constant again. In between, a straight ramp. It never rises above one over lambda, and never falls below minus one over lambda: the shift, divided by the scale.
Why? On a log scale, a Laplace density is a tent whose sides have slope one over lambda, never steeper. Slide the tent over, and the gap between the tents can never exceed the slide times that slope. That is the whole design principle: privacy needs noise whose log density is never steep.
In symbols: two distances to t can differ by at most the distance between the centers. So the privacy loss of any output is at most the sensitivity divided by lambda. Set lambda to the sensitivity over epsilon, and the ratio stays within e to the epsilon, for every output and every pair of neighbors. Privacy, proven in one line.
If the query returns several numbers, add independent Laplace noise to each. The joint density then depends on the L1 distance, which is exactly why sensitivity is measured in the L1 norm. That is Proposition 1: Laplace noise of scale S of f over epsilon in every coordinate.
Pause and ponder: why not something simpler, like uniform noise anywhere between minus ten and plus ten?
Look at the edges. An output of fifty-one and a half is possible if the true count is forty-two, but impossible if it is forty-one: the same infinite ratio that sank the random-row mechanism. Good noise must never rule an output out.
And why not the familiar bell curve? On a log scale a Gaussian is a parabola, steeper and steeper, so the gap between two shifted parabolas grows without bound. In the tails the ratio explodes, and no single epsilon works. Hold on to that Gaussian, though: it comes back, and it is the noise you would actually use to train a neural network privately.
So here is the recipe in the title: noise scale equals sensitivity divided by epsilon. A more sensitive question needs more noise. Stronger privacy needs more noise.

## 13:01 — Privacy for individuals, accuracy for populations
Back to the hospital, with epsilon one half: Laplace noise of scale two. Week one, the curator reports about forty-three point seven. Week two, when the true count is forty-two, about forty point six. Subtract as before, and Alice seems to have lowered the count by three. A fifty-fifty guess about her can now move to at most about sixty-two percent.
Now look at what the noise scale depends on: the sensitivity and epsilon. Not the size of the database.
With a hundred patients, noise of typical size two is a few percent of the answer. With a million, it is a rounding error. Alice is protected by noise that is large compared to her own contribution, which is one, but tiny compared to the population's.
Privacy for individuals. Accuracy for populations. That is the bargain.
Here is one you can answer yourself. Pause and ponder: the noise has size about one over epsilon. What goes wrong if epsilon is much smaller than one over n?
The noise outgrows n, bigger than the count could ever be, and the answer is pure noise. This is not Laplace's fault. Any two databases are linked by a chain of at most n single-row changes, each changing probabilities by at most e to the epsilon, so the ends differ by at most e to the n epsilon. If n epsilon is tiny, every database looks alike, and nothing can be learned. This chain trick is called a hybrid argument, and it comes back at the end.

## 14:44 — Many questions: the privacy budget
One question is never enough. Real analysts ask many, adaptively, each chosen after seeing earlier answers. Maybe you spot a spike in one bin, and zoom in.
The paper's Theorem 1 handles this. Write the probability of the whole transcript as a product, step by step. The analyst's choice of the next question is the same in both worlds, so in the ratio it cancels, leaving one Laplace ratio per answer. If you know reinforcement learning, this is the trajectory-ratio trick: whatever is identical in both worlds cancels, and the per-step log ratios add up.
So privacy losses add up, and epsilon behaves like a budget. Each answer spends part of it; once it is spent, the curator stops. That is the answer to Dinur and Nissim: the budget makes the limit on questions explicit and measurable.
You can now compute a real saving yourself. Pause: a histogram with d bins, total budget epsilon. Treat each bin as its own counting query and split the budget evenly. How much noise does each bin get?
Each bin gets one over d of the budget, so noise of scale d over epsilon. Treated as one query with sensitivity two, each bin gets two over epsilon, whatever d is. The earlier framework's sharper analysis got this down to about the square root of d, but it still grew with d.

## 16:21 — Beyond counting
Sensitivity reaches far beyond counts. Three examples from the paper.
First, picture a social network where each possible link is one row of the database. How many links must you cut to split the network in two? That minimum cut moves by at most one when one link changes, so it is one-sensitive. In general, any question of the form, how many rows would you have to change to make something true, has sensitivity one.
Second: if an algorithm that rarely looks at any particular row, like one working from a small random sample, approximates f to within sigma most of the time, on every database, then f has sensitivity at most two sigma. That is Lemma 1.
Third, the answer need not be a number: a ranking, a set, a string of bits, anything with a distance between answers. Pick an output with probability that decays exponentially with its distance from the true answer, at a rate of epsilon over twice the sensitivity. For bit strings, that flips each bit with probability a little below one half: Warner's coin again, applied to the answer.

## 17:30 — Interactive vs one-shot releases
Now the last part of the paper. Statisticians and data miners traditionally prefer the non-interactive model: sanitize the data once, publish it, and let anyone compute anything. Can that work under this definition?
The paper proves a striking limit. Let each row be a string of d bits. Here is a family of simple counting queries: give each row its own mask, a subset of bit positions, and count the rows with an odd number of ones inside their mask. Each query has sensitivity one, so an interactive curator can answer any one of them with noise of about one over epsilon.
But a one-shot release must prepare for all of them at once. Theorem 3 shows that for at least two thirds of these queries, the release looks almost the same for a random database where every row has even parity, true answer zero, as for one where every row is odd, true answer n. The most extreme difference possible, and it cannot be seen, unless the database is exponentially large: roughly, every four extra bits per row doubles the rows you would need.
Pause and ponder: couldn't an analyst just ask the interactive curator all of these queries too?
No: the budget would run out. The curator only has to answer the few questions someone actually asks, chosen later. A published release cannot know which few those will be, so it must be ready for all of them at once. That is where it breaks.
The proof idea uses two facts. Privacy forces the release to treat every possible row almost alike. And a random mask splits all rows into two halves mixed like salt and pepper, so the even half is like a random poll of everything. Then the chain trick: start from completely random rows, and swap them one at a time for even ones. Each swap barely moves the output, and unless n is huge, all n swaps together barely move it. The same goes for odd rows, so both databases look like random rows.
Warner's coin, randomized response, where each person scrambles their own row so nobody holds the raw data, is even more limited. Proposition 2: even when every row uses the same mask, for most masks it cannot estimate the odd count unless n is exponentially large.
Careful with the quantifiers. For any one query known in advance, a one-shot release can answer it well. What is impossible, unless the database is exponentially large, is one private release that answers most of them. The lesson: for broad, flexible accuracy with strong privacy, keep the curator in the loop.

## 20:17 — What grew from this paper
Back to our map, to see what grew from this paper. The same year, in an invited paper titled simply Differential Privacy, Dwork introduced the name the field still uses. Another 2006 paper, with Kenthapadi, McSherry, Mironov and Naor, added a tiny slack, delta. Remember the Gaussian whose ratio escaped the band in the tails? Delta pays for those rare tails, and lets the bell curve back in.
Scoring every possible answer became McSherry and Talwar's exponential mechanism. The privacy budget grew into a theory of composition, with a surprise from Dwork, Rothblum and Vadhan: allow that tiny delta, and the total loss of k questions grows only like the square root of k.
Warner's coin, the model Section four showed is most limited, is what we now call local differential privacy, used by Google in Chrome and by Apple on iPhones. Why the weakest model? Nobody has to be trusted with the raw data, and with millions of users, a few simple statistics can afford the noise.
In 2016, Abadi and colleagues made it practical to train deep networks privately: clip each example's gradient, like our income cap, which bounds its sensitivity; add Gaussian noise; and track the budget over thousands of steps. If you train models on patient data, this is your entry point. A trained network is just another f of x, and attacks that ask whether a patient was in the training set are our subtraction attack, scaled up.
And for the 2020 census, the US Census Bureau protected its published tables with differential privacy; only a few counts, like state populations, were exact. But that is a one-shot release. Pause and ponder: does Section four forbid it?
No. The Census tuned its release for a fixed set of tables chosen in advance. Section four only rules out one release that is accurate for most of a huge family of questions.

## 22:32 — Recap and questions
Let's recap. One: privacy means changing any one person's row changes the probability of any output by at most a factor of e to the epsilon. Two: a query's sensitivity is the most one row can change its answer. Three: Laplace noise with scale sensitivity over epsilon makes it private, with error that does not grow with the database. Four: one private published table cannot answer most simple parity counts unless the database is exponentially large.
Some questions to test yourself; pause after each. First: what is the sensitivity of the average of n numbers between zero and one?
Second: in a medical imaging dataset, each patient contributes fifty slices, and each slice's gradient is clipped to size C. How much can one patient change the summed gradient?
Third: why does the median give the Laplace mechanism trouble? Answers, and more exercises, are in the companion notes.
Next time someone says a dataset is safe because it is anonymized, you will know the better questions: what is the epsilon, and what counts as one person's row?
