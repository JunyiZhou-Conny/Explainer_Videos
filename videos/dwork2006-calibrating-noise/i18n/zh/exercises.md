# 练习：Calibrating Noise to Sensitivity

视频给你的是直觉，这些题才能让它真正变成你自己的。每道题都请*先*自己做，再展开答案。重点就是动笔：卡住、琢磨的那段时间，正是真正在学的时候。

## 热身（视频结尾的自测题）

**1. 平均值的敏感度。** n 个人每人报告一个 [0, 1] 内的数。它们的平均值的敏感度是多少？

<details><summary>答案</summary>

改变一个人的取值，总和最多变化 1，所以平均值最多变化 **1/n**。尺度为 1/(nε) 的拉普拉斯噪声就够了：人数越多，误差越小。
</details>

**2. 十个问题的预算。** 你回答了十个 counting query，每个都加尺度为 1/0.1 = 10 的拉普拉斯噪声（所以单看每一个，都满足 0.1-差分隐私）。总的隐私损失是多少？

<details><summary>答案</summary>

**ε = 1。** 定理 1：transcript 的概率是一串条件拉普拉斯项的乘积，所以对数比值相加：10 × 0.1。等价地，也可以把这十个计数看成一个向量 query，它的 L1 敏感度是 10，每个分量加 Lap(10) 噪声：ε = S/λ = 10/10 = 1。（这就是序列组合（也叫串行组合）最简单的形式：预算按次相加。）
</details>

**3. 中位数的麻烦。** 为什么中位数会给拉普拉斯机制带来麻烦？明明在“典型”的数据上，改动一条记录，它几乎不动。

<details><summary>答案</summary>

敏感度是*取遍每一对相邻数据库的最坏情况*。取 n 个 [0, 1] 内的数，一半是 0，一半是 1：只改一条记录，中位数就可能从 0 变成 1。所以 S(中位数) 是整个取值范围，Lap(范围/ε) 的噪声会把答案彻底淹没。一年后才有了解决办法：*平滑敏感度*（smooth sensitivity；Nissim、Raskhodnikova 和 Smith，STOC 2007）让噪声随 f 在实际数据库附近有多稳定而调整，同时又不泄露这个稳定程度本身。
</details>

**2b. 什么才算一个人？** 在一个医学影像数据集里，每个病人贡献 50 张切片，训练时做逐样本梯度裁剪：每张切片的梯度都裁剪到范数 C 以内。一个*病人*最多能让梯度之和改变多少？

<details><summary>答案</summary>

最多 **50·C**（对这个病人的 50 个裁剪后的梯度用三角不等式）。差分隐私保护的是“一条记录”所代表的那个单位。如果一条记录应该是一个病人，要么按病人裁剪（先把这个病人所有切片的梯度加起来，再把总和裁剪到 C），要么按 50·C 校准噪声。按切片裁剪、又按 C 校准噪声，保护的其实只是切片，而不是人，而且不会有任何提示。
</details>

**2c. 量一量 Warner 的硬币。** 在随机响应的硬币版本里（正面：如实回答；反面：再掷一次，正面答“是”，反面答“否”），ε 是多少？

<details><summary>答案</summary>

Pr[回答“是” | 真实为“是”] = 1/2 + 1/4 = 3/4，Pr[回答“是” | 真实为“否”] = 1/4；回答“否”时，比值也一样。最坏的比值是 3，所以 **ε = ln 3 ≈ 1.1**。五五开的先验，最多只能变成 75%。
</details>

## 理解定义

**4. 为什么是 e^ε，而不是 1 + ε？** 证明：如果一个机制对相邻数据库（只差一条记录）满足 ε-差分隐私，那么对相差 k 条记录的两个数据库，概率之比最多是 e^{kε}。为什么正是乘法形式让这条“链”成立？

<details><summary>答案</summary>

用 x = x⁽⁰⁾, x⁽¹⁾, …, x⁽ᵏ⁾ = y 把 x 和 y 连起来，每一步只改一条记录。于是 Pr[𝒯(x)=t]/Pr[𝒯(y)=t] = Π_j Pr[𝒯(x⁽ʲ⁾)=t]/Pr[𝒯(x⁽ʲ⁺¹⁾)=t] ≤ (e^ε)^k。比值相乘，所以对数比值相加。加法形式的接近程度（比如统计距离）也能这样串起来，但它管不住每个输出的概率，见第 5 题。
</details>

**5. “随机发布一条记录”的机制（例 2）。** 对只在第 i 条记录上不同的相邻数据库 x、x′，计算 𝒯(x) 和 𝒯(x′) 之间的总变差距离（TV 距离）。再找出一个输出 t，使两边的概率之比为无穷大。

<details><summary>答案</summary>

对每个 j ≠ i，输出 (j, x_j) 在两个数据库下的概率都是 1/n；只有 (i, xᵢ) 和 (i, x′ᵢ) 这两个输出不同，各自在一个世界里概率为 1/n，在另一个世界里为 0。TV 距离 = ½(1/n + 1/n) = **1/n**。输出 t = (i, xᵢ) 在 x 下概率为 1/n，在 x′ 下为 0：比值为 **∞**。平均来看很小，对第 i 条记录却是灾难。
</details>

**6. 攻击者的概率比。** 攻击者认为 Alice 的记录是“1”的先验概率为 p。证明：看到一个满足 ε-差分隐私的机制的输出之后，后验概率比与先验概率比 p/(1−p)（即 odds，也叫几率）最多相差 e^{±ε} 倍（假设数据库的其余部分已知）。

<details><summary>答案</summary>

设 x（Alice = 1）和 x′（Alice = 0）是两个候选数据库。根据贝叶斯公式，后验概率比 = 先验概率比 × Pr[𝒯(x)=t]/Pr[𝒯(x′)=t]，而定义 1 把这个似然比限制在 e^{±ε} 以内。所以这个保证“无论你之前知道什么”都成立。
</details>

## 理解噪声

**7. 一个不等式证完拉普拉斯机制。** 证明：对拉普拉斯密度 h(y) ∝ e^{−|y|/λ}，对任意 t 都有 h(t − a)/h(t − b) ≤ e^{|a − b|/λ}。

<details><summary>答案</summary>

h(t−a)/h(t−b) = exp((|t−b| − |t−a|)/λ)，而由三角不等式，|t−b| ≤ |t−a| + |a−b|。
</details>

**8. 为什么不用高斯？** 对 N(a, σ²) 和 N(b, σ²)，计算两个密度在 t 处的对数比值。它有界吗？

<details><summary>答案</summary>

ln(比值) = ((t−b)² − (t−a)²)/(2σ²) = (a−b)(2t − a − b)/(2σ²)，关于 t 是线性的，**无界**。没有哪个 ε 能对所有输出都成立。在 (ε, δ)-差分隐私（近似差分隐私，approximate DP）下，高斯噪声就能用了（Dwork、Kenthapadi、McSherry、Mironov 和 Naor，2006），它允许上界以极小的概率 δ 不成立。这就是今天的高斯机制；相应地，只用 ε 的定义叫纯差分隐私。
</details>

**9. 直方图：一个 query 还是 d 个 query？** 你要在总预算 ε 下发布一个有 d 个桶的直方图。比较两种做法：(a) 把它当成一个向量 query（S = 2）；(b) 把每个桶当成一个单独的 counting query，每个分到 ε/d 的预算。两种情况下，每个桶的噪声尺度各是多少？

<details><summary>答案</summary>

(a) 每个桶 Lap(2/ε)，与 d 无关。(b) 每个桶需要 Lap(1/(ε/d)) = Lap(d/ε)：差了 d/2 倍。（SuLQ 框架比简单平分要好，每个桶 O(√d/ε)，但仍然随 d 增大。）省下来的关键，是看出互不相交的桶共用同一份敏感度（这也是并行组合背后的道理）。
</details>

## 分离结果（较难）

**10. 奇偶 query。** 每条记录是一个 d 位比特串；对一个 mask r，g_r(x) = r·x mod 2。为什么 f_r(x) = Σᵢ g_r(xᵢ) 的敏感度为 1？为什么交互式的数据管理者回答任意单个 f_r，误差只要 1/ε 左右？直观上，为什么在有 2^d 个 mask 时，一次性发布的那份经过隐私处理的数据会陷入麻烦？

<details><summary>答案</summary>

一条记录最多改变求和里的一项，而且最多改变 1，所以 S = 1；对分析者挑的任何 r，f_r(x) + Lap(1/ε) 都管用。一次性发布则必须对之后才出现的任何 r 都管用；引理 2 表明，对大多数 r，一个满足 ε-差分隐私的随机映射几乎分不清“从 mask 内有偶数个 1 的那一半里抽的记录”和“从全空间里抽的记录”；再对 n 条记录做 hybrid argument（混合论证），总距离会一直很小，除非 n 随 d 指数增长。所以发布结果分不清“答案是 0”和“答案是 n”。
</details>

## 动手写代码（15 分钟）

```python
import numpy as np
rng = np.random.default_rng(0)

def laplace_mechanism(true_answer, sensitivity, eps, size=None):
    return true_answer + rng.laplace(scale=sensitivity / eps, size=size)

# 两个相邻的医院数据库：计数 41 vs 42。
eps = 0.5
a = laplace_mechanism(41, 1, eps, size=2_000_000)
b = laplace_mechanism(42, 1, eps, size=2_000_000)
bins = np.linspace(31, 52, 43)               # 两个直方图在这个范围内都有足够多的样本
ha, _ = np.histogram(a, bins, density=True)
hb, _ = np.histogram(b, bins, density=True)
ok = (ha > 0.02) & (hb > 0.02)
print("max |log ratio| ≈", np.abs(np.log(ha[ok] / hb[ok])).max(), " (should be ≲ eps =", eps, ")")

# 噪声不变，看相对误差随人数怎么变。
for n in [100, 10_000, 1_000_000]:
    true = n // 2
    err = np.abs(laplace_mechanism(true, 1, eps, size=10_000) - true).mean()
    print(f"n={n:>9,}: mean |error| = {err:.2f}  ({100 * err / true:.4f}% of the answer)")
```

第一行输出是对数比值的最大绝对值（应当不超过 eps）；后三行是平均绝对误差，以及它占答案的百分比。然后试试：把 `rng.laplace` 换成 `rng.normal`，看对数比值在尾部怎么越变越大。

## 带着这张地图读论文

全文二十页，建议按这个顺序读（页码为印刷页码）：
1. p. 265–266：问题设定，以及用一段话概括的主要结果。
2. p. 270：定义 1 和例 1（半页纸讲完整个想法）。
3. p. 271：leakage 为什么必须不可忽略、例 2、定义 2。
4. p. 272–273：命题 1 和定理 1（证明只有六行）。
5. p. 273–276：敏感度低的那些函数可以略读；定理 2 要读。
6. p. 276–278：定理 3 和命题 2 的陈述，以及关于量词的几条注。
7. 选读：p. 278–281（分离结果的证明），p. 282–284（附录 A，语义安全）。

逐页摘要和勘误见 [`digest.md`](digest.md)。

## 中英术语对照表

| English | 本片用词 | 常见变体 |
| --- | --- | --- |
| differential privacy | 差分隐私 | |
| ε-indistinguishability | ε-不可区分性（即 ε-差分隐私） | |
| sensitivity (global, L1) | 敏感度 S(f)（全局敏感度，本文即 L1 敏感度） | 不是诊断试验的“灵敏度” |
| smooth sensitivity | 平滑敏感度 | |
| Laplace mechanism | 拉普拉斯机制 | Laplace 机制 |
| noise scale | 噪声尺度 | |
| privacy budget | 隐私预算 | |
| privacy loss | 隐私损失 | |
| neighbouring databases | 相邻数据库 | 相邻数据集 / 兄弟数据集 |
| query / counting query | query / counting query | 查询 / 计数查询 |
| transcript | transcript | 交互历史 |
| total variation (TV) distance | 统计距离（即 TV 距离） | 总变差距离 / 全变差距离 |
| sequential / parallel composition | 序列组合 / 并行组合 | 串行组合 |
| (ε, δ)-DP, approximate DP | (ε, δ)-差分隐私，近似差分隐私 | |
| pure DP / Gaussian mechanism | 纯差分隐私 / 高斯机制 | |
| randomized response | 随机响应 | |
| sub-linear queries (SuLQ) | 次线性数量的 query | 亚线性 |
| hybrid argument | hybrid argument | 混合论证 |
| per-example gradient clipping | 逐样本梯度裁剪 | |
| odds / likelihood ratio | 先验 / 后验概率比；似然比 | 几率（odds，即 p/(1−p)） |
| mask | mask | 掩码 |

注：本文的敏感度 S(f) 指全局敏感度（global sensitivity），即一条记录最多能让 f 变化多少；它不是医学诊断里衡量真阳性率的“灵敏度”。
