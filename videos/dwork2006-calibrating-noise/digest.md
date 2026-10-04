# Digest — Calibrating Noise to Sensitivity in Private Data Analysis

C. Dwork, F. McSherry, K. Nissim, A. Smith. TCC 2006 (Theory of Cryptography Conference),
LNCS 3876, pp. 265–284. PDF: `library/privacy/differential-privacy/dwork2006calibrating.pdf`.
Page numbers below are the printed LNCS page numbers (PDF page = printed page − 264).

## In one paragraph

A trusted curator holds a database of n rows. An analyst asks a query f; the curator returns
f(x) plus random noise. The paper (i) defines privacy as **ε-indistinguishability** — changing any
single row changes the probability of every possible transcript by at most a factor e^ε (this is
what Dwork soon named *differential privacy*); (ii) defines the **sensitivity** S(f), the largest
L1 change in f that a single row can cause; and (iii) proves that adding **Laplace noise of scale
S(f)/ε** to each output coordinate achieves ε-indistinguishability — for any f, vector-valued and
even adaptively chosen. The noise depends only on ε and S(f), not on the database or its size.
It shows many useful functions (histograms, covariance matrices, distances to a property, functions
estimable from small samples) have low sensitivity, generalises the idea to arbitrary metric
output spaces, and proves that **non-interactive** sanitizations (publish once) cannot answer most
low-sensitivity queries unless the database is exponentially large in the row length d — an
exponential separation from the interactive setting, and an even stronger limit for randomized
response.

## Setting and notation (§2, p. 269–270)

- Database x ∈ Dⁿ: n rows from a domain D (typically {0,1}^d or ℝ^d). Hamming distance d_H counts
  differing rows; x, x′ are *neighbours* if d_H(x, x′) = 1.
- A mechanism San interacts with an adversary 𝒜; the transcript 𝒯_{San,𝒜}(x) is a random variable
  (randomness from San and 𝒜). Non-interactive schemes have no dependence on 𝒜.
- Lap(λ): density h(y) ∝ exp(−|y|/λ), mean 0. (The paper says "standard deviation λ"; the true
  standard deviation is √2·λ — λ is the scale.)

## Definitions

- **Definition 1 (ε-indistinguishability, p. 270).** For all neighbours x, x′, all adversaries 𝒜,
  all transcripts t: |ln(Pr[𝒯_𝒜(x) = t] / Pr[𝒯_𝒜(x′) = t])| ≤ ε. ε is called the *leakage*.
  For small ε, the ratio is ≈ 1 ± ε. Much stronger than small statistical (total-variation)
  distance: the ratio must be bounded at every point.
- **Definition 2 (L1 sensitivity, p. 271).** S(f) is the smallest number such that
  ‖f(x) − f(x′)‖₁ ≤ S(f) for all neighbours. Equivalently a Lipschitz constant w.r.t. Hamming
  distance. Inherent in f, not chosen by policy, independent of the actual database.
- **Definition 3 (sensitivity in a metric space, p. 275).** S_ℳ(f) = sup over neighbours of
  d_ℳ(f(x), f(x′)).
- **Appendix A (p. 282–284).** (k, ε)-simulatability (Def. 4), (k, ε)-indistinguishability
  (Def. 5), (k, ε)-semantic security (Def. 6). (1, ε/k)-indist. ⇒ (k, ε)-indist. by a chain of k
  single-row changes; Claim 2: (k, ε)-indist. ⇒ (k, ε)-simulatable ⇒ (k, 2ε)-indist.;
  Claim 3: (k, ε)-indist. ⇔ (k, ε)-semantically secure. So the definition protects against
  adversaries with arbitrary prior knowledge.

## Results, in order

| where | statement | why it matters |
| --- | --- | --- |
| Ex. 1, p. 270 | f(x) = Σxᵢ on {0,1}ⁿ, release f(x) + Lap(1/ε): ε-indistinguishable, since h(y)/h(y′) ≤ e^{ε|y−y′|} and neighbouring sums differ by 1 | the template for everything |
| p. 271 | constant-factor accuracy forces ε = Ω(1/n): if neighbouring distributions are o(1/n) apart, any two databases are o(1) apart (chain of n steps) and nothing can be learned | leakage must be non-negligible — unlike crypto |
| Ex. 2, p. 271 | 𝒯(x) = (i, xᵢ) for random i: statistical difference 1/n between neighbours, yet each output reveals a row; fails Def. 1 (probability 0 vs 1/n) | why average-case distances are the wrong metric |
| Ex. 3, p. 271–272 | sums on {0,1}: S = 1. Histograms over d disjoint bins: S = 2, independent of d | dimension-free sensitivity |
| Prop. 1, p. 272 | San_f(x) = f(x) + (Y₁,…,Y_d), Yᵢ i.i.d. Lap(S(f)/ε) is ε-indistinguishable (vector Laplace density ∝ exp(−‖y‖₁/λ), so z+Y vs z′+Y ratio ∈ exp(±‖z−z′‖₁/λ)) | **the Laplace mechanism** |
| Thm. 1, p. 273 | adaptive queries: transcript t = (a₁,…,a_d), query fₜ determined by earlier answers; answering with Lap(λ), λ = maxₜ S(fₜ)/ε, is ε-indistinguishable. Proof: chain rule; each conditional factor is a Laplace ratio; product = exp(‖fₜ(x) − fₜ(x′)‖₁/λ). Server may refuse when S(fₜ) is too large — not disclosive | ε as a **privacy budget** spent across queries |
| §3.2, p. 273 | histograms: earlier framework [6] adds O(√d/ε) noise per coordinate, total L1 error O(√d) larger; disjoint analyses: S(f) ≤ 2 maxᵢ S(fᵢ) | big savings for contingency tables |
| §3.2, p. 274 | mean μ and covariance C of v(xᵢ) with γ = max‖v(x)‖₁: one row changes μ by ≤ 2γ/n and C by ≤ 8γ²/n in L1; previous framework: O(d) factor more noise for C | linear algebra on private data |
| §3.2, p. 274–275 | distance from x to a set S ⊆ Dⁿ is 1-sensitive; e.g. min-cut weight of a graph with edge weights in [0,1] (distance to a disconnected graph), MST weight | graph statistics, "holistic" functions |
| Lemma 1, p. 275 | if a randomized algorithm A reads each xᵢ with probability ≤ α and is σ-accurate w.p. ≥ (1+α)/2, then S(f) ≤ 2σ. Converse false (Reed–Solomon example) | sample-approximable ⇒ insensitive |
| Thm. 2, p. 276 | any metric space: sample y with density ∝ exp(ε·d_ℳ(y, f(x)) / (2S_ℳ(f))) — read the exponent with a minus sign — is ε-indistinguishable (the factor 2 covers the normalising constant; Remark 1: drop it when the normaliser doesn't depend on the centre). Hamming cube example: flip each output bit independently with probability a bit below ½ | precursor of the **exponential mechanism** (McSherry–Talwar 2007) |
| Thm. 3, p. 277 | D = {0,1}^d, any ε-indist. non-interactive San: for ≥ 2/3 of the parity-type queries f_g(x) = Σᵢ rᵢ⊙xᵢ (mod-2 inner products), San(x) for x uniform with f_g = 0 vs with f_g = n has statistical difference O(n^{4/3} ε^{2/3} 2^{−d/3}); so if n = o(2^{d/4}/√ε) these queries can't be answered | **interactive ≫ non-interactive** |
| Prop. 2, p. 278 | randomized response (each row perturbed independently, Z(x₁),…,Z(xₙ)): even a single predicate r⊙x applied to all rows can't be estimated for most r unless n = Ω(2^{d/3}/ε^{2/3}) | local perturbation is weaker still |
| Lemma 2, p. 278 | for a random r ≠ 0, the half-domain D_r = {x : r⊙x = 0} is a pairwise-independent sample of {0,1}^d; an e^{±ε}-bounded randomized map can't tell Z(D_r) from Z(D): SD ≤ O((ε²/(α2^d))^{1/3}) w.p. 1−α | the engine of the separation |
| §4.2–4.3, p. 278–281 | hybrid argument: replace rows one at a time from uniform to D_r; each step costs σ, n steps cost nσ; Claim 1 bounds Var of the estimator via Chebyshev | proof technique |

## What is new relative to prior work

- Prior work [Dinur–Nissim 2003, Dwork–Nissim 2004, Blum–Dwork–McSherry–Nissim 2005 "SuLQ"]
  handled noisy **sums** f = Σ g(xᵢ), g → [0,1], with semantic-security-style definitions proved via
  indistinguishability and against *informed* adversaries. This paper: arbitrary f (vector-valued,
  adaptive), a single clean definition, noise calibrated to S(f), dimension-free bounds, metric
  spaces, and the interactive/non-interactive separation.
- Dinur–Nissim showed accurate answers to many subset-sum queries let an adversary reconstruct the
  database unless noise is Ω(√n) (poly-time adversary) or linear (unbounded adversary).

## Small errata / reading notes

- p. 270: "standard deviation λ" for Lap(λ) — the scale is λ, the std is √2λ.
- p. 266: "Pr[y] ∝ e^{−ε|y|/S(f)}" is the noise density; the paper's Prop. 1 states it as
  Lap(S(f)/ε).
- p. 272: "a histogram for B₁, …, B_m" should read B_d.
- p. 276: the exponent of h_{z,ε} is printed without its minus sign; the density decays with
  distance.
- p. 276 Hamming-cube remark: the flip probability "roughly ½ − ε/(2S(f))" is loose; the exact
  per-bit flip probability from the density is 1/(1 + e^{ε/(2S)}), ≈ ½ − ε/(8S) for small ε/S.

## Glossary for newcomers

- **Neighbouring databases** — differ in exactly one row.
- **Transcript** — everything the analyst sees: the questions and the noisy answers.
- **Statistical distance (total variation)** — half the L1 distance between two distributions;
  "how often can an optimal test tell them apart".
- **L1 norm** — ‖v‖₁ = Σ|vᵢ|.
- **Laplace distribution** — two-sided exponential; on a log scale its density is a tent.
- **Hybrid argument** — walk from one distribution to another through intermediate ones, bound
  each step, add up the steps.
- **Interactive vs non-interactive** — answering queries on demand vs publishing one sanitized
  object.
- **Randomized response** — each person perturbs their own record before release (today: *local*
  differential privacy).

## Where it led (for the legacy map)

- C. Dwork, *Differential Privacy*, ICALP 2006 — the name; impossibility of Dalenius-style absolute
  disclosure prevention.
- Dwork, Kenthapadi, McSherry, Mironov, Naor, *Our Data, Ourselves*, Eurocrypt 2006 — (ε, δ)-DP,
  Gaussian/binomial noise.
- McSherry & Talwar, *Mechanism Design via Differential Privacy*, FOCS 2007 — exponential mechanism.
- Nissim, Raskhodnikova, Smith, *Smooth Sensitivity and Sampling*, STOC 2007 — beyond worst-case
  sensitivity (e.g. the median).
- Dwork, Rothblum, Vadhan, *Boosting and Differential Privacy*, FOCS 2010 — advanced composition.
- Erlingsson, Pihur, Korolova, *RAPPOR*, CCS 2014 — local DP in Chrome; Apple (2016–).
- Abadi et al., *Deep Learning with Differential Privacy*, CCS 2016 — DP-SGD.
- Dwork & Roth, *The Algorithmic Foundations of Differential Privacy*, 2014 — the textbook.
- US Census Bureau, 2020 Census Disclosure Avoidance System.
- 2017 Gödel Prize (Dwork, McSherry, Nissim, Smith) for this paper.
