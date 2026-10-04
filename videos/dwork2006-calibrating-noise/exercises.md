# Exercises — Calibrating Noise to Sensitivity

The video gives you the intuition; these make it yours. Try each one *before* opening the answer.
Pen and paper is the point — the struggle is where the learning happens.

## Warm-up (from the end of the video)

**1. Sensitivity of an average.** Each of n people reports a number in [0, 1]. What is the
sensitivity of their average?

<details><summary>Answer</summary>

Changing one person's value changes the sum by at most 1, so the average moves by at most **1/n**.
Laplace noise of scale 1/(nε) suffices — the error shrinks as the population grows.
</details>

**2. A budget of ten questions.** You answer ten counting queries, each with Laplace noise of scale
1/0.1 = 10 (so each is 0.1-indistinguishable on its own). What is the total privacy loss?

<details><summary>Answer</summary>

**ε = 1.** Theorem 1: the transcript probability is a product of conditional Laplace terms, so the
log-ratios add: 10 × 0.1. Equivalently, view the ten counts as one vector query with L1
sensitivity 10 answered with Lap(10) per coordinate: ε = S/λ = 10/10 = 1.
</details>

**3. Trouble with the median.** Why does the median give the Laplace mechanism trouble, even
though on "typical" data it barely moves when one row changes?

<details><summary>Answer</summary>

Sensitivity is a *worst case over all neighbouring pairs*. Take n numbers in [0, 1], half 0s and
half 1s: changing a single row can move the median from 0 to 1. So S(median) is the whole range,
and Lap(range/ε) noise swamps the answer. The fix came a year later: *smooth sensitivity*
(Nissim, Raskhodnikova & Smith, STOC 2007) adapts the noise to how stable f is near the actual
database, without leaking that stability itself.
</details>

## Understanding the definition

**4. Why e^ε and not 1 + ε?** Show that if a mechanism is ε-indistinguishable for neighbours
(one row apart), then for databases k rows apart the ratio of probabilities is at most e^{kε}.
Why is the multiplicative form what makes this "chain" work?

<details><summary>Answer</summary>

Connect x and y by x = x⁽⁰⁾, x⁽¹⁾, …, x⁽ᵏ⁾ = y, each step changing one row. Then
Pr[𝒯(x)=t]/Pr[𝒯(y)=t] = Π_j Pr[𝒯(x⁽ʲ⁾)=t]/Pr[𝒯(x⁽ʲ⁺¹⁾)=t] ≤ (e^ε)^k. Ratios multiply, so
log-ratios add. An additive closeness notion (like statistical distance) also chains, but it
doesn't bound each output's probability — see exercise 5.
</details>

**5. The "publish a random row" mechanism (Example 2).** Compute the total-variation distance
between 𝒯(x) and 𝒯(x′) for neighbours x, x′ differing in row i. Then find an output t where the
ratio of probabilities is infinite.

<details><summary>Answer</summary>

The output (j, x_j) has probability 1/n under both databases for every j ≠ i; only the two outputs
(i, xᵢ) and (i, x′ᵢ) differ, each with probability 1/n in one world and 0 in the other.
TV distance = ½(1/n + 1/n) = **1/n**. The output t = (i, xᵢ) has probability 1/n under x and 0
under x′: ratio **∞**. Small on average, catastrophic for row i.
</details>

**6. The attacker's odds.** An attacker believes Alice's row is "1" with prior probability p.
Show that after seeing the output of an ε-indistinguishable mechanism, the posterior odds are
within a factor e^{±ε} of the prior odds p/(1−p) (assume the rest of the database is known).

<details><summary>Answer</summary>

Let x (Alice = 1) and x′ (Alice = 0) be the two candidate databases. By Bayes,
posterior odds = prior odds × Pr[𝒯(x)=t]/Pr[𝒯(x′)=t], and Definition 1 bounds that likelihood
ratio by e^{±ε}. This is why the guarantee holds "no matter what you knew beforehand".
</details>

## Understanding the noise

**7. The Laplace one-liner.** Prove that for the Laplace density h(y) ∝ e^{−|y|/λ},
h(t − a)/h(t − b) ≤ e^{|a − b|/λ} for all t.

<details><summary>Answer</summary>

h(t−a)/h(t−b) = exp((|t−b| − |t−a|)/λ) and by the triangle inequality |t−b| ≤ |t−a| + |a−b|.
</details>

**8. Why not Gaussian?** For N(a, σ²) vs N(b, σ²) compute the log-ratio of densities at t. Is it
bounded?

<details><summary>Answer</summary>

ln ratio = ((t−b)² − (t−a)²)/(2σ²) = (a−b)(2t − a − b)/(2σ²) — linear in t, **unbounded**. No ε
works for all outputs. Gaussian noise becomes usable under (ε, δ)-differential privacy
(Dwork, Kenthapadi, McSherry, Mironov, Naor 2006), which allows the bound to fail with tiny
probability δ.
</details>

**9. Histograms: one query or d queries?** You release a histogram with d bins under total
budget ε. Compare (a) treating it as one vector query (S = 2) with (b) answering each bin as a
separate counting query with budget ε/d each. What is the noise scale per bin in each case?

<details><summary>Answer</summary>

(a) Lap(2/ε) per bin, independent of d. (b) each bin needs Lap(1/(ε/d)) = Lap(d/ε): a factor d/2
worse. (The SuLQ framework did better than naive splitting, O(√d/ε) per bin, but still grew
with d.) Recognising that disjoint bins share one unit of sensitivity is the win.
</details>

## The separation (harder)

**10. Parity queries.** Rows are d-bit strings; for a mask r, g_r(x) = r·x mod 2. Why is
f_r(x) = Σᵢ g_r(xᵢ) 1-sensitive? Why can an interactive curator answer any single f_r with error
about 1/ε? And intuitively, why is one published sanitization in trouble when there are 2^d masks?

<details><summary>Answer</summary>

One row changes at most one term of the sum by at most 1, so S = 1, and f_r(x) + Lap(1/ε) works
for any r the analyst picks. A one-shot release must work for whichever r comes later; Lemma 2
shows that for most r, an ε-private randomized map barely distinguishes "rows drawn from the
parity-0 half" from "rows drawn from anywhere" — and the hybrid argument over the n rows keeps the
total distance small unless n is exponential in d. So the release can't tell "answer 0" from
"answer n".
</details>

## Code it (15 minutes)

```python
import numpy as np
rng = np.random.default_rng(0)

def laplace_mechanism(true_answer, sensitivity, eps, size=None):
    return true_answer + rng.laplace(scale=sensitivity / eps, size=size)

# Two neighbouring hospital databases: count 41 vs 42.
eps = 0.5
a = laplace_mechanism(41, 1, eps, size=2_000_000)
b = laplace_mechanism(42, 1, eps, size=2_000_000)
bins = np.linspace(31, 52, 43)               # where both histograms have plenty of samples
ha, _ = np.histogram(a, bins, density=True)
hb, _ = np.histogram(b, bins, density=True)
ok = (ha > 0.02) & (hb > 0.02)
print("max |log ratio| ≈", np.abs(np.log(ha[ok] / hb[ok])).max(), " (should be ≲ eps =", eps, ")")

# Relative error vs population size, same noise.
for n in [100, 10_000, 1_000_000]:
    true = n // 2
    err = np.abs(laplace_mechanism(true, 1, eps, size=10_000) - true).mean()
    print(f"n={n:>9,}: mean |error| = {err:.2f}  ({100 * err / true:.4f}% of the answer)")
```

Then try: replace `rng.laplace` with `rng.normal` and watch the log-ratio grow in the tails.

## Reading the paper with this map

Twenty pages; read in this order (printed page numbers):
1. p. 265–266 — the setting and the one-paragraph result.
2. p. 270 — Definition 1 and Example 1 (the whole idea in half a page).
3. p. 271 — non-negligible leakage, Example 2, Definition 2.
4. p. 272–273 — Proposition 1 and Theorem 1 (the proof is six lines).
5. p. 273–276 — skim the insensitive functions; read Theorem 2.
6. p. 276–278 — Theorem 3 and Proposition 2 statements and the remarks on quantifiers.
7. Optional: p. 278–281 (the separation proofs), p. 282–284 (Appendix A, semantic security).

See `digest.md` for a page-by-page summary and small errata.
