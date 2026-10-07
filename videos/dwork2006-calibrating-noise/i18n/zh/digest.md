# 论文笔记：Calibrating Noise to Sensitivity in Private Data Analysis

C. Dwork, F. McSherry, K. Nissim, A. Smith. TCC 2006 (Theory of Cryptography Conference), LNCS 3876, pp. 265–284. PDF：`library/privacy/differential-privacy/dwork2006calibrating.pdf`。下文页码均为 LNCS 的印刷页码（PDF 页码 = 印刷页码 − 264）。

## 一段话概括

可信的数据管理者持有一个有 n 条记录的数据库。分析者提出 query f，管理者返回 f(x) 加上随机噪声。论文 (i) 把隐私定义为 **ε-不可区分性**：改动任何一条记录，每一种可能的 transcript 的概率最多变化 e^ε 倍（Dwork 不久后把它命名为**差分隐私**）；(ii) 定义了**敏感度** S(f)：单条记录能让 f 产生的最大 L1 变化；(iii) 证明在每个输出分量上加**尺度为 S(f)/ε 的拉普拉斯噪声**，就能满足 ε-不可区分性，对任意 f 都成立，包括向量值的、甚至自适应选择的 f。噪声只取决于 ε 和 S(f)，与数据库本身及其规模无关。论文还说明了许多有用的函数（直方图、协方差矩阵、到某个性质的距离、能从小样本估计的函数）敏感度都很低，把这个想法推广到任意度量空间上的输出，并证明**非交互式**的隐私处理（只发布一次）答不好大多数低敏感度的 query，除非数据库规模随记录长度 d 指数增长。这是交互式设定与非交互式设定之间的指数级分离；对随机响应，限制还要更强。

## 设定与记号（§2，p. 269–270）

- 数据库 x ∈ Dⁿ：来自域 D（通常是 {0,1}^d 或 ℝ^d）的 n 条记录。汉明距离 d_H 数的是不同记录的条数；若 d_H(x, x′) = 1，就称 x、x′ **相邻**。
- 机制 San 与敌手 𝒜 交互；transcript 𝒯_{San,𝒜}(x) 是一个随机变量（随机性来自 San 和 𝒜）。非交互式方案不依赖于 𝒜。这种由可信的数据管理者持有原始数据、对外只给加噪答案的模型，今天叫中心化差分隐私（与本地化差分隐私相对）。
- Lap(λ)：密度 h(y) ∝ exp(−|y|/λ)，均值为 0。（论文写的是“standard deviation λ”；真正的标准差是 √2·λ，λ 是尺度。）

## 定义

- **定义 1（ε-不可区分性，p. 270）。** 对任意相邻的 x、x′，任意敌手 𝒜，任意 transcript t：|ln(Pr[𝒯_𝒜(x) = t] / Pr[𝒯_𝒜(x′) = t])| ≤ ε。ε 被称为 *leakage*（泄露量）。ε 很小时，比值 ≈ 1 ± ε。这比“统计距离（总变差距离）很小”强得多：比值必须在每一点都有界。
- **定义 2（L1 敏感度，p. 271）。** S(f) 是使所有相邻数据库都满足 ‖f(x) − f(x′)‖₁ ≤ S(f) 的最小数。等价地，它是 f 关于汉明距离的 Lipschitz 常数。它是 f 本身的性质，不是人为选定的，也与实际数据库无关。今天的文献把它叫全局敏感度（global sensitivity）。
- **定义 3（度量空间中的敏感度，p. 275）。** S_ℳ(f) = 对所有相邻数据库取 d_ℳ(f(x), f(x′)) 的上确界。
- **附录 A（p. 282–284）。** (k, ε)-可模拟性（定义 4）、(k, ε)-不可区分性（定义 5）、(k, ε)-语义安全（定义 6）。通过 k 次单条记录改动构成的链，(1, ε/k)-不可区分 ⇒ (k, ε)-不可区分；断言 2：(k, ε)-不可区分 ⇒ (k, ε)-可模拟 ⇒ (k, 2ε)-不可区分；断言 3：(k, ε)-不可区分 ⇔ (k, ε)-语义安全。所以这个定义能抵御拥有任意先验知识的敌手。

## 主要结果（按论文顺序）

| 位置 | 内容 | 为什么重要 |
| --- | --- | --- |
| 例 1，p. 270 | {0,1}ⁿ 上的 f(x) = Σxᵢ，发布 f(x) + Lap(1/ε)：满足 ε-不可区分性，因为 h(y)/h(y′) ≤ e^{ε\|y−y′\|}，而相邻数据库的和相差 1 | 之后一切的模板 |
| p. 271 | 要在常数因子以内保持准确，就必须 ε = Ω(1/n)：如果相邻数据库的输出分布相差 o(1/n)，那么任意两个数据库都只相差 o(1)（n 步的链），什么也学不到 | leakage 必须不可忽略，这和密码学不同 |
| 例 2，p. 271 | 随机取 i，𝒯(x) = (i, xᵢ)：相邻数据库之间的统计差异只有 1/n，但每个输出都暴露一条记录；不满足定义 1（概率 0 对 1/n） | 为什么平均意义上的距离是错误的度量 |
| 例 3，p. 271–272 | {0,1} 上的求和：S = 1。d 个互不相交的桶构成的直方图：S = 2，与 d 无关 | 与维度无关的敏感度 |
| 命题 1，p. 272 | San_f(x) = f(x) + (Y₁,…,Y_d)，Yᵢ 独立同分布于 Lap(S(f)/ε)，满足 ε-不可区分性（向量拉普拉斯密度 ∝ exp(−‖y‖₁/λ)，所以 z+Y 与 z′+Y 的比值 ∈ exp(±‖z−z′‖₁/λ)） | **拉普拉斯机制** |
| 定理 1，p. 273 | 自适应的 query：transcript t = (a₁,…,a_d)，query fₜ 由之前的答案决定；用 Lap(λ) 作答，λ = maxₜ S(fₜ)/ε，满足 ε-不可区分性。证明：链式法则；每个条件因子都是一个拉普拉斯比值；乘积 = exp(‖fₜ(x) − fₜ(x′)‖₁/λ)。S(fₜ) 太大时服务器可以拒绝回答，拒绝本身不泄露信息 | ε 作为在多个 query 之间花费的**隐私预算**（视频“很多问题：隐私预算”一章的 RL 类比：分析者的选择在比值里约掉，和重要性采样比里约掉环境转移概率是同一个 trick） |
| §3.2，p. 273 | 直方图：早先的框架 [6] 在每个分量上加 O(√d/ε) 的噪声，总 L1 误差大 O(√d) 倍；互不相交的分析：S(f) ≤ 2 maxᵢ S(fᵢ) | 列联表上大幅节省 |
| §3.2，p. 274 | v(xᵢ) 的均值 μ 和协方差 C，γ = max‖v(x)‖₁：一条记录让 μ 在 L1 下最多变化 2γ/n，让 C 最多变化 8γ²/n；早先的框架对 C 要多加 O(d) 倍的噪声 | 在隐私数据上做线性代数 |
| §3.2，p. 274–275 | x 到集合 S ⊆ Dⁿ 的距离敏感度为 1；例如边权在 [0,1] 内的图的最小割权重（到一个不连通图的距离）、最小生成树权重 | 图统计量、“整体性”函数 |
| 引理 1，p. 275 | 如果随机算法 A 读取每个 xᵢ 的概率 ≤ α，并以 ≥ (1+α)/2 的概率做到 σ-准确，那么 S(f) ≤ 2σ。逆命题不成立（Reed–Solomon 码的例子） | 能用样本近似 ⇒ 敏感度低 |
| 定理 2，p. 276 | 任意度量空间：按密度 ∝ exp(ε·d_ℳ(y, f(x)) / (2S_ℳ(f))) 抽样 y（指数要带负号来读），满足 ε-不可区分性（因子 2 用来抵消归一化常数的变化；注 1：归一化常数不依赖于中心时可以去掉）。汉明立方体的例子：每个输出比特独立地以略低于 ½ 的概率翻转 | **指数机制**的前身（McSherry–Talwar 2007） |
| 定理 3，p. 277 | D = {0,1}^d，任意满足 ε-不可区分性的非交互式 San：对至少 2/3 的奇偶型 query f_g(x) = Σᵢ rᵢ⊙xᵢ（模 2 内积），在 f_g = 0 的条件下均匀抽取的 x 与在 f_g = n 的条件下均匀抽取的 x，San(x) 的统计差异为 O(n^{4/3} ε^{2/3} 2^{−d/3})；所以如果 n = o(2^{d/4}/√ε)，这些 query 就答不了 | **交互式 ≫ 非交互式** |
| 命题 2，p. 278 | 随机响应（每条记录独立扰动，Z(x₁),…,Z(xₙ)）：即使对所有记录用同一个谓词 r⊙x，对大多数 r 也估计不出来，除非 n = Ω(2^{d/3}/ε^{2/3}) | 本地扰动还要更弱 |
| 引理 2，p. 278 | 对随机的 r ≠ 0，半个域 D_r = {x : r⊙x = 0} 是 {0,1}^d 的一个两两独立样本；一个 e^{±ε} 有界的随机映射分不清 Z(D_r) 和 Z(D)：以 1−α 的概率 SD ≤ O((ε²/(α2^d))^{1/3}) | 分离结果的核心工具 |
| §4.2–4.3，p. 278–281 | hybrid argument（混合论证）：把记录一条一条地从均匀分布换成 D_r；每一步代价 σ，n 步代价 nσ；断言 1 用切比雪夫不等式控制估计量的方差 | 证明技巧 |

## 相对已有工作，新在哪里

- 已有工作 [Dinur–Nissim 2003, Dwork–Nissim 2004, Blum–Dwork–McSherry–Nissim 2005 “SuLQ”] 处理的是带噪声的**求和** f = Σ g(xᵢ)，g → [0,1]，用的是语义安全风格的定义，通过不可区分性来证明，并且针对的是**知情的**敌手。这篇论文：任意 f（向量值、自适应）、一个干净的定义、按 S(f) 校准的噪声、与维度无关的上界、度量空间，以及交互式与非交互式之间的分离。
- Dinur–Nissim 证明了：如果对很多子集求和 query 都答得很准，敌手就能重构数据库，除非噪声达到 Ω(√n)（多项式时间的敌手）或线性量级（计算能力不受限的敌手）。

## 勘误与阅读笔记

- p. 270：论文说 Lap(λ) 的“standard deviation”是 λ；其实 λ 是尺度，标准差是 √2λ。
- p. 266：“Pr[y] ∝ e^{−ε|y|/S(f)}”是噪声的密度；论文的命题 1 把它写成 Lap(S(f)/ε)。
- p. 272：“a histogram for B₁, …, B_m”应为 B_d。
- p. 276：h_{z,ε} 的指数印刷时漏了负号；密度应随距离衰减。
- p. 276 关于汉明立方体的注：翻转概率“roughly ½ − ε/(2S(f))”不够精确；由密度算出的每比特精确翻转概率是 1/(1 + e^{ε/(2S)})，当 ε/S 很小时 ≈ ½ − ε/(8S)。

## 新手词汇表

- **相邻数据库**：恰好相差一条记录。
- **transcript（交互历史）**：分析者看到的一切，包括问的问题和带噪声的答案。
- **统计距离（总变差距离）**：两个分布之间 L1 距离的一半；直观地说，就是最优的检验有多大机会把两者区分开。
- **L1 范数**：‖v‖₁ = Σ|vᵢ|。
- **拉普拉斯分布**：双边指数分布；取对数之后，它的密度是一个帐篷形。
- **hybrid argument（混合论证）**：经过一串中间分布，从一个分布走到另一个分布，每一步分别求上界，再把各步加起来。
- **交互式 vs 非交互式**：按需回答 query，还是一次性发布一份经过隐私处理的数据。
- **随机响应**：每个人在发布之前先自己扰动自己的记录（今天叫**本地化差分隐私**）。

## 后续发展（对应视频“这篇论文之后”一章的地图）

- C. Dwork, *Differential Privacy*, ICALP 2006：起了这个名字；证明 Dalenius 式的绝对披露防护不可能实现。
- Dwork, Kenthapadi, McSherry, Mironov, Naor, *Our Data, Ourselves*, Eurocrypt 2006：(ε, δ)-差分隐私（近似差分隐私），高斯 / 二项噪声。
- McSherry & Talwar, *Mechanism Design via Differential Privacy*, FOCS 2007：指数机制。
- Nissim, Raskhodnikova, Smith, *Smooth Sensitivity and Sampling*, STOC 2007：超越最坏情况的敏感度，即平滑敏感度（可用于中位数等）。
- Dwork, Rothblum, Vadhan, *Boosting and Differential Privacy*, FOCS 2010：高级组合定理。
- Erlingsson, Pihur, Korolova, *RAPPOR*, CCS 2014：Chrome 里的本地化差分隐私；苹果（2016 年起）。
- Abadi et al., *Deep Learning with Differential Privacy*, CCS 2016：DP-SGD（逐样本梯度裁剪 + 高斯噪声 + 隐私预算核算）。
- Dwork & Roth, *The Algorithmic Foundations of Differential Privacy*, 2014：教科书。
- US Census Bureau（美国人口普查局），2020 年人口普查披露规避系统（Disclosure Avoidance System，DAS）。
- 2017 年哥德尔奖（Dwork、McSherry、Nissim、Smith），获奖论文就是这一篇。

## 中英术语对照表

| English | 本片用词 | 常见变体 |
| --- | --- | --- |
| differential privacy | 差分隐私 | |
| ε-indistinguishability | ε-不可区分性（即 ε-差分隐私） | |
| sensitivity (global, L1) | 敏感度 S(f)（全局敏感度，论文中即 L1 敏感度） | 不是诊断试验的“灵敏度” |
| local / smooth sensitivity | 局部敏感度 / 平滑敏感度 | |
| Laplace mechanism | 拉普拉斯机制 | Laplace 机制 |
| noise scale | 噪声尺度 | |
| privacy budget / privacy accounting | 隐私预算 / 隐私预算核算 | |
| privacy loss | 隐私损失 | |
| leakage (the paper's word for ε) | leakage | 泄露量 |
| neighbouring databases | 相邻数据库 | 相邻数据集 / 兄弟数据集 |
| curator (trusted curator) | 数据管理者（可信的数据管理者） | |
| row | 记录 | |
| query / counting query | query / counting query | 查询 / 计数查询 |
| transcript | transcript | 交互历史 |
| adversary 𝒜 | 敌手 𝒜 | 攻击者 |
| statistical distance / total variation distance | 统计距离（即 TV 距离） | 总变差距离 / 全变差距离；论文用词：statistical difference（统计差异） |
| sequential / parallel composition; advanced composition | 序列组合 / 并行组合；高级组合定理 | 串行组合 |
| pure / approximate DP | 纯差分隐私 / 近似差分隐私 | |
| Gaussian mechanism / exponential mechanism | 高斯机制 / 指数机制 | |
| central DP (trusted-curator model) | 中心化差分隐私 | |
| randomized response / local DP | 随机响应 / 本地化差分隐私 | 本地差分隐私 / 局部差分隐私 |
| membership inference attack | 成员推理攻击 | 成员推断攻击 |
| reconstruction attack | 重构攻击 | |
| sub-linear queries (SuLQ) | 次线性数量的 query | 亚线性 |
| hybrid argument | hybrid argument | 混合论证 |
| per-example gradient clipping | 逐样本梯度裁剪 | |
| odds / likelihood ratio | 先验 / 后验概率比；似然比 | 几率（odds，即 p/(1−p)） |
| importance sampling (ratio) | 重要性采样（比） | |
| utility / privacy–utility trade-off | 可用性 / 隐私与可用性的权衡 | |
| de-identification vs anonymization | 去标识化（区别于匿名化） | |
| Hamming distance / metric space / Lipschitz constant | 汉明距离 / 度量空间 / Lipschitz 常数 | |
| semantic security / simulatability | 语义安全 / 可模拟性 | |
| contingency table / covariance matrix / minimum spanning tree | 列联表 / 协方差矩阵 / 最小生成树 | |
| pairwise independent / Reed–Solomon code / normalizing constant | 两两独立 / Reed–Solomon 码 / 归一化常数 | |
| Example / Remark / Claim / Appendix | 例 / 注 / 断言 / 附录 | |

注：视频和论文里的敏感度 S(f) 都指全局敏感度（global sensitivity），即一条记录最多能让 f 变化多少；它不是医学诊断里衡量真阳性率的“灵敏度”。
