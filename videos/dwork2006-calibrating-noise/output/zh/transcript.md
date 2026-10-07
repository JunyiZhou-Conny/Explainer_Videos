# 【论文精读】差分隐私的开山之作：Calibrating Noise to Sensitivity（TCC 2006）

## 00:00 — 差分攻击（differencing attack）
这是一个医院数据库，每个病人一条记录。有位研究者问了个看似无害的问题：有多少病人患有疾病 X？医院不公开任何记录。它只给了一个数：41。
> Here is a hospital database, one row per patient. A researcher asks an innocent question: how many patients have condition X? The hospital releases no records. It just says: forty-one.

一周后，一位新病人 Alice 入院了。研究者又问了一遍。现在答案是 42。
> A week later, one new patient, Alice, is admitted. The researcher asks again. The answer is now forty-two.

两数一减，研究者就知道了 Alice 一件很具体的事，却一条记录都没看。继续之前，先自己试着补上这个漏洞。暂停想一想：人数四舍五入到十位，能保护 Alice 吗？需要多想一会儿的话，可以先暂停视频。
> Subtract, and the researcher has learned something very specific about Alice, without seeing a single record. Before we go on, try to fix this yourself. Pause and ponder: would rounding the count to the nearest ten protect Alice? Pause the video if you need more time.

大多数星期里，确实可以。但如果人数从 44 变成 45，取整后的答案就从 40 跳到 50，Alice 又暴露了。任何确定性的规则，只要答案会变，就一定在某处有这样的跳变。
> Most weeks, yes. But if the count goes from forty-four to forty-five, the rounded answer jumps from forty to fifty, and Alice is exposed again. Any fixed rule that ever changes its answer has a jump like that somewhere.

那发布统计量，到底怎样才算不泄露隐私？如果靠加噪声，那加多少才够？
> So what would it even mean for a statistic to be private? And if the fix is to add noise, how much is enough?

2006 年，Cynthia Dwork、Frank McSherry、Kobbi Nissim 和 Adam Smith，用这篇 paper 回答了这两个问题：《Calibrating Noise to Sensitivity in Private Data Analysis》。它开创了我们今天所说的差分隐私，differential privacy，2017 年还获得了哥德尔奖。
> In 2006, Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith answered both questions in this paper: Calibrating Noise to Sensitivity in Private Data Analysis. It founded what we now call differential privacy, and in 2017 it won the Gödel Prize.

这期讲三个核心想法：隐私的定义；一个数，叫敏感度，sensitivity；以及一个公式，算噪声加多少才够。还有个出人意料的限制：要按这个定义不泄露隐私，一张公开的表能做的有限。
> This video covers its three big ideas: a definition of privacy, a number called sensitivity, and a recipe for how much noise is enough. Plus a surprising limit on what one published table can achieve, if it must be private in this sense.


## 01:49 — 这篇论文从哪里来
先画一张地图，看看这篇 paper 从哪儿来。1965 年，Stanley Warner 为敏感问题调查提出了随机响应。在常见的版本里，你私下掷一枚硬币。正面，你就如实回答。反面，你就再掷一次：正面答“是”，反面答“否”。任何一个“是”，都可能只是硬币说的；但问上成千上万人，真实比例照样能估出来。记住这枚硬币。
> First, a map of where this paper comes from. In 1965, Stanley Warner proposed randomized response for sensitive surveys. In a popular version, you flip a coin in private. Heads, you answer truthfully. Tails, you flip again and say yes for heads, no for tails. Any single yes could be the coin talking, yet over thousands of people the true rate can still be estimated. Keep this coin in mind.

之后几十年，统计学家和计算机科学家，不断改进这类 trick，分成两种思路：要么扰动输入的数据，要么扰动输出的答案。
> Over the following decades, statisticians and computer scientists refined such tricks, in two flavours: scramble the data going in, or scramble the answers coming out.

与此同时，最容易想到的办法，也就是直接去掉姓名，却一再失败。Latanya Sweeney 发现，光凭邮编、出生日期和性别，就能唯一识别大多数美国人；1997 年，她把号称匿名的病历和公开的选民名单一对照，就认出了马萨诸塞州州长。教训是：隐私必须是发布过程的性质，而不在于发布出来的表看起来怎么样；而且无论攻击者还知道什么，它都必须成立。
> Meanwhile, the obvious fix, just remove the names, kept failing. Latanya Sweeney showed that ZIP code, birth date and sex alone single out most Americans, and in 1997 she linked supposedly anonymous hospital records to a public voter list and found the governor of Massachusetts. The lesson: privacy must be a property of the process, not of how the released table looks, and it must hold whatever else the attacker knows.

然后在 2003 年，Irit Dinur 和 Kobbi Nissim 证明了一个令人警醒的结论。问题答得太多、太准，误差远小于根号 n，攻击者就能重构出几乎整个数据库。我们那个做减法的攻击，其实就是这种攻击只问两个问题的版本。噪声，就是回答很多问题的代价。
> Then, in 2003, Irit Dinur and Kobbi Nissim proved something sobering. Answer too many questions too accurately, with errors much smaller than the square root of n, and an attacker can rebuild almost the entire database. Our subtraction was the two-question version of this attack. Noise is the price of answering many questions.

反过来也有好消息：问题数量有限，适量噪声就够了。Dwork、Nissim 和合作者据此做了个叫 SuLQ 的框架，意思是只问次线性数量的 query（查询）；它回答带噪声的求和，比如人数。记住这个上限。这篇 paper 把它变成了一笔预算。
> The hopeful flip side: with a limited number of questions, modest noise is enough. Dwork, Nissim and colleagues built this into a framework called SuLQ, for sub-linear queries, which answers noisy sums like counts. Remember that limit on questions. This paper turns it into a budget.

但 SuLQ 只能处理求和，而且它的定义容许以极小的概率发生大量泄露。这篇 paper 迈出了一大步：数据的任意函数、一个干净的定义和一条简单的噪声规则。很应景的是，它发表在密码学会议上，那里的习惯是先定义安全性，要求能抵御所有可能的攻击者，再去证明。
> But SuLQ only covered sums, and its definition tolerated a tiny chance of a large leak. This paper takes the leap: any function of the data, one clean definition, and one simple rule for the noise. Fittingly, it appeared at a cryptography conference, where the habit is to define security against every possible attacker first, and then prove it.


## 04:06 — 设定：可信的数据管理者
先交代一下 setting。可信的服务器，也就是数据管理者，持有数据库 x：n 条记录，每人一条。分析者发来 query f：数据库的任意函数，返回一个数或一列数。
> Here is the setting. A trusted server, the curator, holds a database x: n rows, one per person. An analyst sends a query f, any function of the database that returns a number, or a list of numbers.

数据管理者从不公开真实答案 f(x)。它的做法是先抽一个随机噪声 Y，再公开 f(x) 加 Y。因为分析者可以一直问下去，所以这叫交互式的 setting。另一种做法是发布一张经过隐私处理的表，然后撒手不管，这叫非交互式。原文最后证明了，前者从根本上更强大。
> The curator never releases the honest answer, f of x. Instead it draws random noise, Y, and releases f of x plus Y. Because the analyst can keep asking, this is called the interactive setting. The alternative, publishing one sanitized table and walking away, is non-interactive. At the end, the paper proves the first is fundamentally more powerful.

所以一切都归结到一个问题：Y 应该服从什么分布？噪声太少，Alice 就暴露了。太多，答案就没用了。标题已经给出了答案：按敏感度校准噪声。不过我们先要搞清楚：到底什么叫不泄露隐私？
> So everything hinges on one question: what distribution should Y have? Too little noise, and Alice is exposed. Too much, and the answer is useless. The title gives the answer: calibrate the noise to the sensitivity. But first, what does private actually mean?


## 05:04 — 定义隐私
关键是想象两个世界。一边是数据库 x。另一边是 x′：只有一条记录不同。比如 Alice 那条。这样的一对叫相邻数据库（也叫相邻数据集）。医院例子里多了 Alice；这里是她的记录变了。总之，谁的记录都不该影响太大。
> The key move is to imagine two worlds. In one, the database is x. In the other, it is x prime: identical except for one row. Say, Alice's. Databases like this are called neighbors. In the hospital, Alice was added; here, her row just says something different. Either way, no single person's row should matter much.

运行这个机制，也就是数据管理者随机作答的规则，两个世界各一次。分析者能看到的一切，原文叫 transcript（交互历史）；目前就是一个带噪声的答案。因为机制是随机的，每个世界都给出一整个输出分布。
> Run the mechanism, the curator's randomized answering rule, in each world. Whatever the analyst gets to see, the paper calls the transcript; for now, a single noisy answer. Because the mechanism is random, each world gives a whole distribution of possible outputs.

任取一个输出 t，比较两条曲线在这里的高度。滑动 t，看它们的比值。满足差分隐私的机制，让比值处处接近 1：不超过 e^ε，也不低于 e^(−ε)。
> Pick any output t, and compare the heights of the two curves there. Slide t along and watch their ratio. A private mechanism keeps that ratio close to one everywhere: never above e to the epsilon, never below e to the minus epsilon.

这就是原文的定义，叫作 ε-不可区分性（即 ε-差分隐私）。比值的对数，就是 t 处的隐私损失。对任意一对相邻数据库、任意分析者、任意输出，它的绝对值都不能超过 ε。取绝对值就对称了：比值是 2 还是 1/2，都算一样。ε 很小的时候，e^ε 约等于 1 + ε。
> That is the paper's definition, which it calls epsilon-indistinguishability. The log of the ratio is the privacy loss at t. For every pair of neighbors, every analyst and every output, it must be at most epsilon in absolute value. The absolute value makes it symmetric: a ratio of two and a ratio of one half count the same. For small epsilon, e to the epsilon is about one plus epsilon.

拿地图上 Warner 的硬币试试。暂停想一想：如果 Alice 的真实答案为“是”，她有多大概率说“是”？换成“否”呢？
> Let's test it on Warner's coin from our map. Pause and ponder: if Alice's true answer is yes, how likely is she to say yes? And if it is no?

真实答案为“是”，她说“是”的概率是 3/4：正面，或者先反后正。换成“否”，只有第二枚硬币能让她说“是”：1/4。最坏的比值是 3，所以硬币满足定义，ε 就等于 3 的对数，大约 1.1。
> If the truth is yes, she says yes three quarters of the time: heads, or tails then heads. If it is no, only the second coin can say yes: one quarter. The worst ratio is three, so the coin satisfies the definition with epsilon equal to the log of three, about one point one.

现在你是攻击者，想区分这两个世界。按贝叶斯公式，后验概率比恰好是先验概率比乘这个比值，所以变化倍数最多是 e^ε，无论你之前知道什么。从五五开出发，ε 取 0.1，最多有 52.5% 的把握；取 1，最多 73%。ε 是人为选定的；原文管它叫 leakage（泄露量）。
> Now be the attacker, trying to tell the two worlds apart. By Bayes' rule, your new odds are your old odds times exactly this ratio, so they move by at most a factor of e to the epsilon, whatever you knew before. Starting from fifty-fifty, epsilon one tenth leaves you at most fifty-two and a half percent sure; epsilon one, at most seventy-three. Epsilon is set by policy; the paper calls it the leakage.

再来看它不保证什么。假如研究发现吸烟者更容易得心脏病，而 Alice 吸烟，别人现在就可能觉得她风险更高。这不算侵犯隐私：同样的结论从其他人的数据里也能得出，所以就算把 Alice 的记录换成别人的，也照样会发生。
> Notice what this does not promise. If a study reveals that smokers get more heart disease, and Alice smokes, people may now think she is at higher risk. That is not a privacy violation: the same lesson could be learned from everyone else's data, so it would happen even if Alice's row were replaced by someone else's.


## 07:51 — 为什么这么严格？
为什么每个输出的比值都要有上界？密码学常常满足于更弱的东西：统计距离（即 TV 距离），也就是两条曲线间面积的一半。等价地说，就是任意事件的概率在两个世界间的最大差距。原文说明了它在这里为什么不够。
> Why demand a ratio bound for every single output? Cryptography often settles for something weaker: statistical distance, half the area between the two curves. Equivalently, the most the probability of any event can differ between the worlds. The paper shows why that is not enough here.

看这个机制：随机挑一条记录，原样发布。改动一个人的记录，输出分布只会变化 1/n。数据库很大时这点变化微不足道，所以按平均来衡量，它看起来不泄露隐私。
> Consider this mechanism: pick one row at random and publish it, word for word. Change one person's row, and the output distribution moves by only one over n. For a big database that is tiny, so by the averaged measure this looks private.

可每个输出都是某个人的完整记录。比值这一关能拦住它：显示 Alice 真实取值的输出，一个世界里概率是 1/n，另一个是 0。比值是无穷大。
> But every output is somebody's complete record. The ratio test catches it: the output showing Alice's real value has probability one over n in one world, and zero in the other. The ratio is infinite.

平均值会放过灾难，只要每场灾难对每个人都很罕见。而比值上界会处处把它们排除在外。它也解答了四舍五入那道题：在跳变处，一个世界给出这个答案的概率是 1，另一个是 0。想过这一关，机制就必须是随机的。
> Averages let catastrophes slip through, as long as each is rare for any single person. A ratio bound rules them out everywhere. It also settles our rounding question: at the jump, one world gives that answer with probability one, the other with probability zero. To pass this test, a mechanism has to be random.


## 08:57 — 敏感度（sensitivity）
那噪声到底要加多少？这只取决于 query 的一个性质：它的敏感度，也就是改变一条记录最多能让答案变化多少，取遍每一对相邻数据库，包括还不存在的那些。
> So how much noise do we need? It depends on a single property of the query: its sensitivity, the most that changing one row can ever change the answer, over all pairs of neighboring databases, including ones that do not exist yet.

对 counting query（计数查询），比如医院那个，一条记录最多让答案变 1。敏感度是 1。
> For a counting query, like our hospital count, one row changes the answer by at most one. Sensitivity one.

再看直方图：把一条记录的可能取值分成 d 个桶，发布每个桶的记录数。先别急着看答案，暂停一下：如果 Alice 的记录变了，整个直方图总共能变多少？这和桶的数量有关吗？
> Now a histogram: split the possible values of a row into d bins, and release how many rows fall in each. Before I show you, pause: if Alice's row changes, how much can the whole histogram change in total? Does it depend on the number of bins?

她从一个桶搬到另一个桶：一个桶少了 1，另一个桶多了 1。总变化量：2。像这样把各个分量变化的绝对值加起来，就是 L1 范数，原文就用它来衡量一列数的敏感度。而且它总是 2，不管是 5 个桶还是 5000 个桶。它和维度完全无关。
> She moves out of one bin and into another: one count goes down by one, another goes up by one. Total change: two. Adding up absolute changes across coordinates like this is the L1 norm, the paper's way to measure sensitivity for lists of numbers. And it is two whether there are five bins or five thousand. It does not depend on the dimension at all.

对比一下：数据库里最高的收入是多少？一个亿万富翁，就能让答案变动 10 亿，不封顶就根本没有上限。标准做法是先给每个值封顶，比如 100 万。这个 trick 要记住：差分隐私深度学习对梯度做的就是这个。
> Contrast that with: what is the largest income in the database? One billionaire can move that answer by a billion, and with no cap there is no limit at all. The standard fix is to cap every value, say at a million, first. Remember that trick: it is exactly what private deep learning does to gradients.

有两点要记住。敏感度只取决于函数本身，与具体的数据库无关，也不是人为选定的。ε 是选择。敏感度是事实。
> Two things to remember. Sensitivity is a property of the function alone, not of the particular database, and it is not chosen by policy. Epsilon is a choice. Sensitivity is a fact.


## 10:33 — 拉普拉斯机制（Laplace mechanism）
下面来看噪声。原文用的是拉普拉斯分布：左右对称，峰很尖，并且随着离中心的距离指数衰减。它的宽度由尺度参数 λ 决定。
> Now for the noise. The paper uses the Laplace distribution: symmetric, sharply peaked, and falling off exponentially with distance from the center. Its width is set by a scale parameter, lambda.

关键的 trick 来了。一条拉普拉斯曲线的中心在 f(x)，也就是 41，另一条在 f(x′)，也就是 42：这就是两个世界的输出分布。
> Here is the trick. Center one Laplace curve at f of x, forty-one, and another at f of x prime, forty-two: the output distributions of our two worlds.

现在对每个输出 t，画出两条曲线比值的对数。在 41 左边，它完全是个常数。在 42 右边，又是个常数。中间是一段笔直的斜坡。它从不超过 1/λ，也从不低于 −1/λ：也就是平移量除以尺度。
> Now plot the log of their ratio for every output t. To the left of forty-one, it is exactly constant. To the right of forty-two, constant again. In between, a straight ramp. It never rises above one over lambda, and never falls below minus one over lambda: the shift, divided by the scale.

为什么？取对数之后，拉普拉斯密度是个帐篷形，两边的斜率是 1/λ，绝不会更陡。把帐篷平移过去，两个帐篷的高度差，永远不超过平移量乘以这个斜率。这就是整个设计原则：隐私需要对数密度处处不陡的噪声。
> Why? On a log scale, a Laplace density is a tent whose sides have slope one over lambda, never steeper. Slide the tent over, and the gap between the tents can never exceed the slide times that slope. That is the whole design principle: privacy needs noise whose log density is never steep.

用符号写出来：到 t 的两段距离，最多相差两个中心之间的距离。所以任意输出的隐私损失，最多是敏感度除以 λ。让 λ 取敏感度除以 ε，比值就始终在 e^ε 以内，对任意输出、任意一对相邻数据库都成立。隐私，一个不等式就证完了。
> In symbols: two distances to t can differ by at most the distance between the centers. So the privacy loss of any output is at most the sensitivity divided by lambda. Set lambda to the sensitivity over epsilon, and the ratio stays within e to the epsilon, for every output and every pair of neighbors. Privacy, proven in one line.

如果 query 返回好几个数，就给每个数加上独立的拉普拉斯噪声。这时联合密度取决于 L1 距离，正因为这样，敏感度才用 L1 范数来衡量。这就是命题 1：在每个分量上加尺度为 S(f)/ε 的拉普拉斯噪声。
> If the query returns several numbers, add independent Laplace noise to each. The joint density then depends on the L1 distance, which is exactly why sensitivity is measured in the L1 norm. That is Proposition 1: Laplace noise of scale S of f over epsilon in every coordinate.

暂停想一想：为什么不用更简单的，比如均匀噪声，−10 到 +10 之间任意取值？
> Pause and ponder: why not something simpler, like uniform noise anywhere between minus ten and plus ten?

看看边缘。输出 51.5，真实人数是 42 就可能，是 41 就不可能：又是那个无穷大比值，随机发布一条记录的机制当初就栽在这上面。好的噪声，绝不能把任何输出排除在外。
> Look at the edges. An output of fifty-one and a half is possible if the true count is forty-two, but impossible if it is forty-one: the same infinite ratio that sank the random-row mechanism. Good noise must never rule an output out.

那为什么不用熟悉的钟形曲线？取对数之后，高斯是一条抛物线，越来越陡，所以两条平移开的抛物线，高度差会无限增大。到了尾部，比值会爆炸，没有哪个 ε 能管用。不过先记住这个高斯：它还会回来，用差分隐私训练神经网络时，实际用的就是它。
> And why not the familiar bell curve? On a log scale a Gaussian is a parabola, steeper and steeper, so the gap between two shifted parabolas grows without bound. In the tails the ratio explodes, and no single epsilon works. Hold on to that Gaussian, though: it comes back, and it is the noise you would actually use to train a neural network privately.

这就是标题里的那条公式：噪声尺度等于敏感度除以 ε。敏感度越高的 query，噪声越大。隐私越强，噪声越大。
> So here is the recipe in the title: noise scale equals sensitivity divided by epsilon. A more sensitive question needs more noise. Stronger privacy needs more noise.


## 13:32 — 隐私留给个体，准确留给总体
回到医院的例子，ε 取 0.5：尺度为 2 的拉普拉斯噪声。第一周，管理者报出大约 43.7。第二周，真实人数是 42，报出大约 40.6。跟之前一样做减法，Alice 好像让人数少了 3。原本对她的判断是五五开，现在最多能有大约 62% 的把握。
> Back to the hospital, with epsilon one half: Laplace noise of scale two. Week one, the curator reports about forty-three point seven. Week two, when the true count is forty-two, about forty point six. Subtract as before, and Alice seems to have lowered the count by three. A fifty-fifty guess about her can now move to at most about sixty-two percent.

再看噪声尺度取决于什么：敏感度和 ε。而不是数据库的规模。
> Now look at what the noise scale depends on: the sensitivity and epsilon. Not the size of the database.

有 100 个病人时，噪声一般在 2 左右，占答案的百分之几。到了 100 万人，这点噪声可以忽略不计。保护 Alice 的噪声，比起她自己的贡献，也就是 1，算是很大，但比起总体微不足道。
> With a hundred patients, noise of typical size two is a few percent of the answer. With a million, it is a rounding error. Alice is protected by noise that is large compared to her own contribution, which is one, but tiny compared to the population's.

隐私，留给个体。准确，留给总体。这就是差分隐私的取舍。
> Privacy for individuals. Accuracy for populations. That is the bargain.

这一题你可以自己回答。暂停想一想：噪声大约有 1/ε 那么大。如果 ε 远小于 1/n，会出什么问题？
> Here is one you can answer yourself. Pause and ponder: the noise has size about one over epsilon. What goes wrong if epsilon is much smaller than one over n?

噪声超过了 n，比人数可能取到的任何值都大，答案成了纯噪声。这不是拉普拉斯噪声的问题。任意两个数据库之间，都有一条最多 n 步的链，每步只改一条记录，概率之比最多是 e^ε，所以两端之比最多是 e^(nε)。如果 nε 极小，所有数据库看起来都一样，什么也学不到。这种链式 trick 叫 hybrid argument（混合论证），最后还会再出现。
> The noise outgrows n, bigger than the count could ever be, and the answer is pure noise. This is not Laplace's fault. Any two databases are linked by a chain of at most n single-row changes, each changing probabilities by at most e to the epsilon, so the ends differ by at most e to the n epsilon. If n epsilon is tiny, every database looks alike, and nothing can be learned. This chain trick is called a hybrid argument, and it comes back at the end.


## 15:23 — 很多问题：隐私预算（privacy budget）
一个问题永远不够。现实中的分析者会自适应地问很多个，每个都是看了前面的答案才选的。比如某个桶冒出尖峰，就放大看看。
> One question is never enough. Real analysts ask many, adaptively, each chosen after seeing earlier answers. Maybe you spot a spike in one bin, and zoom in.

原文的定理 1 处理的就是这个。看整份 transcript（交互历史）：把它的概率一步一步写成乘积。分析者怎么选下一个问题，在两个世界里都一样，所以在比值里会约掉，每个答案只剩一个拉普拉斯比值。懂强化学习的话，这就是算轨迹概率比时的那个 trick：凡是两个世界里相同的都约掉，每一步的对数比值相加。
> The paper's Theorem 1 handles this. Write the probability of the whole transcript as a product, step by step. The analyst's choice of the next question is the same in both worlds, so in the ratio it cancels, leaving one Laplace ratio per answer. If you know reinforcement learning, this is the trajectory-ratio trick: whatever is identical in both worlds cancels, and the per-step log ratios add up.

所以隐私损失会累加，ε 就像一笔隐私预算，privacy budget。每个答案花掉一部分；一旦花完，管理者就不答了。这就回应了 Dinur 和 Nissim：预算让提问的上限明确、可度量。
> So privacy losses add up, and epsilon behaves like a budget. Each answer spends part of it; once it is spent, the curator stops. That is the answer to Dinur and Nissim: the budget makes the limit on questions explicit and measurable.

现在你可以自己算算，实打实能省多少。暂停一下：直方图有 d 个桶，总预算是 ε。每个桶单独算一个 counting query（计数查询），预算平分。每个桶要加多大的噪声？
> You can now compute a real saving yourself. Pause: a histogram with d bins, total budget epsilon. Treat each bin as its own counting query and split the budget evenly. How much noise does each bin get?

每个桶分到 1/d 的预算，噪声尺度就是 d/ε。把整个直方图当成一个敏感度为 2 的 query，每个桶就都是 2/ε，不管 d 是多少。早先那个框架分析得更细，把噪声降到大约根号 d，但还是随 d 增大。
> Each bin gets one over d of the budget, so noise of scale d over epsilon. Treated as one query with sensitivity two, each bin gets two over epsilon, whatever d is. The earlier framework's sharper analysis got this down to about the square root of d, but it still grew with d.


## 17:06 — 不止于计数
敏感度的用处远不止 counting query。原文举了三个例子。
> Sensitivity reaches far beyond counts. Three examples from the paper.

第一，想象一个社交网络，每条可能的边都是数据库里的一条记录。至少要切断多少条边，才能把网络一分为二？这个最小割在改动一条边时最多变化 1，所以敏感度是 1。一般来说，凡是“至少要改动多少条记录才能让某件事成立”这类问题，敏感度都是 1。
> First, picture a social network where each possible link is one row of the database. How many links must you cut to split the network in two? That minimum cut moves by at most one when one link changes, so it is one-sensitive. In general, any question of the form, how many rows would you have to change to make something true, has sensitivity one.

第二：如果一个算法读到每条记录的概率都很小，比如只看一个小规模随机样本，而且大多数时候能把 f 近似到 σ 以内，对每个数据库都如此，那么 f 的敏感度最多是两倍 σ。这就是引理 1。
> Second: if an algorithm that rarely looks at any particular row, like one working from a small random sample, approximates f to within sigma most of the time, on every database, then f has sensitivity at most two sigma. That is Lemma 1.

第三，答案不一定是一个数：一个排名、一个集合、一个比特串，凡是答案之间能定义距离的都行。选中某个输出的概率，随它到真实答案的距离呈指数衰减，速率是 ε 除以两倍敏感度。对比特串来说，这就是每个比特以略低于 1/2 的概率翻转：又是 Warner 的硬币，这次用在了答案上。
> Third, the answer need not be a number: a ranking, a set, a string of bits, anything with a distance between answers. Pick an output with probability that decays exponentially with its distance from the true answer, at a rate of epsilon over twice the sensitivity. For bit strings, that flips each bit with probability a little below one half: Warner's coin again, applied to the answer.


## 18:20 — 交互式 vs 一次性发布
来看这篇 paper 的最后一部分。统计学家和数据挖掘研究者传统上偏爱非交互式模型：数据只做一次隐私处理，发布出去，谁想算什么都行。在这个定义下，行得通吗？
> Now the last part of the paper. Statisticians and data miners traditionally prefer the non-interactive model: sanitize the data once, publish it, and let anyone compute anything. Can that work under this definition?

原文证明了一个惊人的局限。假设每条记录都是一个 d 位的比特串。这里有一族简单的 counting query：给每条记录一个自己的 mask（掩码），也就是一组比特位置，统计有多少条记录在自己的 mask 内有奇数个 1。每个 query 的敏感度都是 1，所以交互式的管理者回答任意一个，噪声只要 1/ε 左右。
> The paper proves a striking limit. Let each row be a string of d bits. Here is a family of simple counting queries: give each row its own mask, a subset of bit positions, and count the rows with an odd number of ones inside their mask. Each query has sensitivity one, so an interactive curator can answer any one of them with noise of about one over epsilon.

但一次性发布必须同时为所有 query 做好准备。定理 3 表明，对其中至少 2/3 的 query，两个随机数据库的发布结果几乎一样：一个里每条记录的 mask 内都有偶数个 1，真实答案为 0；另一个里每条记录都有奇数个 1，真实答案为 n。这已经是最大的差别了，却根本看不出来，除非数据库大到指数级：粗略地说，每条记录每多 4 个比特，需要的记录数就翻一倍。
> But a one-shot release must prepare for all of them at once. Theorem 3 shows that for at least two thirds of these queries, the release looks almost the same for a random database where every row has even parity, true answer zero, as for one where every row is odd, true answer n. The most extreme difference possible, and it cannot be seen, unless the database is exponentially large: roughly, every four extra bits per row doubles the rows you would need.

暂停想一想：分析者就不能把这些 query 也都拿去问交互式的管理者吗？
> Pause and ponder: couldn't an analyst just ask the interactive curator all of these queries too?

不行：预算会用光。管理者只需回答真正有人问的那几个问题，而且是后来才选的。发布的结果没法预知会是哪几个，所以必须同时为所有问题做好准备。一次性发布就败在这里。
> No: the budget would run out. The curator only has to answer the few questions someone actually asks, chosen later. A published release cannot know which few those will be, so it must be ready for all of them at once. That is where it breaks.

证明思路用到两个事实。隐私迫使发布结果对每种可能的记录几乎一视同仁。而随机的 mask 把所有记录分成两半，像椒盐一样混在一起，所以偶数那一半就像对全体的随机抽样。接着是链式 trick：从完全随机的记录出发，一条一条地换成偶数记录。每次替换对输出几乎没影响；除非 n 极大，n 次加起来也几乎没影响。换成奇数记录也一样，所以两个数据库看起来都像随机记录。
> The proof idea uses two facts. Privacy forces the release to treat every possible row almost alike. And a random mask splits all rows into two halves mixed like salt and pepper, so the even half is like a random poll of everything. Then the chain trick: start from completely random rows, and swap them one at a time for even ones. Each swap barely moves the output, and unless n is huge, all n swaps together barely move it. The same goes for odd rows, so both databases look like random rows.

Warner 的硬币，也就是随机响应：每个人自己扰动自己的记录，所以谁手里都没有原始数据；它的局限还要更大。命题 2：即使每条记录都用同一个 mask，对大多数 mask，它也估计不出奇数记录的个数，除非 n 大到指数级。
> Warner's coin, randomized response, where each person scrambles their own row so nobody holds the raw data, is even more limited. Proposition 2: even when every row uses the same mask, for most masks it cannot estimate the odd count unless n is exponentially large.

注意量词。对任意单个、事先已知的 query，一次性发布都能答好。除非数据库大到指数级，单单一次发布不可能既满足差分隐私，又答好其中的大多数。结论是：想对各种问题都灵活地答准，又要强隐私，就让可信的管理者留在回路里。
> Careful with the quantifiers. For any one query known in advance, a one-shot release can answer it well. What is impossible, unless the database is exponentially large, is one private release that answers most of them. The lesson: for broad, flexible accuracy with strong privacy, keep the curator in the loop.


## 21:20 — 这篇论文之后
回到地图上，看看这篇 paper 的后续发展。同一年，Dwork 的特邀论文标题就叫《Differential Privacy》，给这个领域起了沿用至今的名字。同年她还与 Kenthapadi、McSherry、Mironov 和 Naor 合写了一篇 paper，引入了一个极小的松弛量 δ。还记得高斯噪声的比值在尾部冲出带外吗？δ 替罕见的尾部买单，让钟形曲线回来了。
> Back to our map, to see what grew from this paper. The same year, in an invited paper titled simply Differential Privacy, Dwork introduced the name the field still uses. Another 2006 paper, with Kenthapadi, McSherry, Mironov and Naor, added a tiny slack, delta. Remember the Gaussian whose ratio escaped the band in the tails? Delta pays for those rare tails, and lets the bell curve back in.

给每个可能的答案打分，后来成了 McSherry 和 Talwar 的指数机制。隐私预算发展成了一套组合定理，Dwork、Rothblum 和 Vadhan 还带来了一个惊喜：只要允许那个极小的 δ，k 个问题的总损失就只按根号 k 增长。
> Scoring every possible answer became McSherry and Talwar's exponential mechanism. The privacy budget grew into a theory of composition, with a surprise from Dwork, Rothblum and Vadhan: allow that tiny delta, and the total loss of k questions grows only like the square root of k.

Warner 的硬币，也就是第 4 节里证明局限最大的那个模型，正是今天所说的本地化差分隐私，Google 用在 Chrome 浏览器里，苹果用在 iPhone 上。为什么偏偏是最弱的模型？原始数据不用托付给任何人；用户上百万时，几个简单的统计量也扛得住噪声。
> Warner's coin, the model Section four showed is most limited, is what we now call local differential privacy, used by Google in Chrome and by Apple on iPhones. Why the weakest model? Nobody has to be trusted with the raw data, and with millions of users, a few simple statistics can afford the noise.

2016 年，Abadi 和合作者让深度网络在差分隐私下也能真正训练起来：把每个样本的梯度 clip（梯度裁剪）到一定大小以内，就像我们的收入上限，从而限制了敏感度；加上高斯噪声；并在成千上万步里跟踪预算。用病人数据训练模型的话，这就是你的切入点。训练好的网络不过是又一个 f(x)；问“某个病人在不在训练集里”的攻击，就是我们那个做减法的攻击的放大版。
> In 2016, Abadi and colleagues made it practical to train deep networks privately: clip each example's gradient, like our income cap, which bounds its sensitivity; add Gaussian noise; and track the budget over thousands of steps. If you train models on patient data, this is your entry point. A trained network is just another f of x, and attacks that ask whether a patient was in the training set are our subtraction attack, scaled up.

还有 2020 年的人口普查：美国人口普查局用差分隐私保护了公开发布的表；只有少数几项，比如各州人口，是精确的。但这是一次性发布。暂停想一想：这和第 4 节的结论矛盾吗？
> And for the 2020 census, the US Census Bureau protected its published tables with differential privacy; only a few counts, like state populations, were exact. But that is a one-shot release. Pause and ponder: does Section four forbid it?

不矛盾。人口普查局的发布，是针对一组事先选定的固定表格量身定制的。第 4 节排除的只是这样一种发布：对一大类问题里的大多数都答得准。
> No. The Census tuned its release for a fixed set of tables chosen in advance. Section four only rules out one release that is accurate for most of a huge family of questions.


## 23:41 — 回顾与思考题
我们来回顾一下。第一，隐私指的是：改动任何一个人的记录，任何输出的概率之比最多是 e^ε。第二，一个 query 的敏感度，就是一条记录最多能让它的答案变化多少。第三，尺度为敏感度除以 ε 的拉普拉斯噪声，就能让它满足差分隐私，数据库再大，误差也不会变大。第四，一张满足差分隐私的公开表，答不好大多数简单的奇偶 query，除非数据库大到指数级。
> Let's recap. One: privacy means changing any one person's row changes the probability of any output by at most a factor of e to the epsilon. Two: a query's sensitivity is the most one row can change its answer. Three: Laplace noise with scale sensitivity over epsilon makes it private, with error that does not grow with the database. Four: one private published table cannot answer most simple parity counts unless the database is exponentially large.

最后留几道题给大家自测，每道题后面都可以暂停一下。第一题：n 个 0 到 1 之间的数，平均值的敏感度是多少？
> Some questions to test yourself; pause after each. First: what is the sensitivity of the average of n numbers between zero and one?

第二题：在一个医学影像数据集里，每个病人贡献 50 张切片，每张切片的梯度都 clip 到 C 以内。一个病人能让梯度之和改变多少？
> Second: in a medical imaging dataset, each patient contributes fifty slices, and each slice's gradient is clipped to size C. How much can one patient change the summed gradient?

第三题：为什么中位数会给拉普拉斯机制带来麻烦？答案和更多练习，都在配套笔记里。
> Third: why does the median give the Laplace mechanism trouble? Answers, and more exercises, are in the companion notes.

下次有人说数据集匿名化了，所以很安全，你就知道真正该问的是：用的是多大的 ε，什么才算一个人的一条记录？
> Next time someone says a dataset is safe because it is anonymized, you will know the better questions: what is the epsilon, and what counts as one person's row?

