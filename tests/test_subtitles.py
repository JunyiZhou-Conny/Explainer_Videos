"""Regression tests for explainer/subtitles.py: the cues the whole-video QA of both Chinese videos
flagged (the privacy video unless noted), with the exact cues the tool gives now.

    PYTHONPATH=. python -m pytest -q tests/test_subtitles.py
"""

from pathlib import Path

from explainer import subtitles as S

REPO = Path(__file__).resolve().parent.parent


def zh(text, dur=8.0, spoken=None):
    """The .zh.srt cues of one sentence (lines joined by ' / ')."""
    pair = (0.0, dur, text, "x", spoken) if spoken else (0.0, dur, text, "x")
    return [c[2].replace("\n", " / ") for c in S.tracks([pair])["zh"]]


def en(text, dur=8.0):
    """The .en.srt cues of one sentence of the Chinese video."""
    return [c[2].replace("\n", " / ") for c in S.tracks([(0.0, dur, "", text)])["en"]]


def bi(text, english, dur=8.0, spoken=None):
    """The bilingual (zh, en) cues of one sentence pair."""
    pair = (0.0, dur, text, english, spoken) if spoken else (0.0, dur, text, english)
    return [(c[2], c[3]) for c in S.tracks([pair])["zh-en"]]


SWEENEY = ("Latanya Sweeney 发现，光凭邮编、出生日期和性别，就能唯一识别大多数美国人；"
           "1997 年，她把号称匿名的病历和公开的选民名单一对照，就认出了马萨诸塞州州长。",
           "Latanya Sweeney showed that ZIP code, birth date and sex alone single out most Americans, "
           "and in 1997 she linked supposedly anonymous hospital records to a public voter list "
           "and found the governor of Massachusetts.")


# ---------------------------------------------------------------- A. Chinese line and cue breaks

def test_1_no_cut_inside_a_list_at_its_comma():
    assert bi(*SWEENEY, 14.6)[0][0] == "Latanya Sweeney 发现，光凭邮编、出生日期和性别"
    assert zh(SWEENEY[0], 14.6)[:2] == ["Latanya Sweeney 发现， / 光凭邮编、出生日期和性别",
                                        "就能唯一识别大多数美国人"]
    assert S.split_balanced("Dwork、Rothblum 和 Vadhan 还带来了一个惊喜", 22) == [
        "Dwork、Rothblum 和 Vadhan", "还带来了一个惊喜"]
    assert S._mark_cost("Dwork、Rothblum", 6) > S._mark_cost("邮编、出生", 3) > S._mark_cost("邮编，出生", 3)


def test_2_no_line_ends_on_de_or_a_negation():
    assert zh(SWEENEY[0], 14.6)[2] == ("1997 年，她把号称匿名的病历和公开的选民名单 / "
                                       "一对照，就认出了马萨诸塞州州长")
    for word in ("公开的", "不", "没"):
        assert S._cut_penalty(word + "选民名单", len(word)) >= 6


def test_3_no_line_starts_with_a_postposition():
    assert S.split_balanced("clip 到一定大小以内（梯度裁剪）", 12) == ["clip 到一定", "大小以内（梯度裁剪）"]


def test_4_a_gloss_stays_with_its_term():
    assert zh("这种链式 trick 叫 hybrid argument（混合论证），最后还会再出现。", 5) == [
        "这种链式 trick 叫 / hybrid argument（混合论证）", "最后还会再出现"]
    assert zh("每个桶单独算一个 counting query（计数查询），预算平均分配。", 4.2) == [
        "每个桶单独算一个 / counting query（计数查询），预算平均分配"]
    assert zh("分析者能看到的一切，原文叫 transcript（交互历史）；目前就是一个带噪声的答案。", 6.2) == [
        "分析者能看到的一切， / 原文叫 transcript（交互历史）", "目前就是一个带噪声的答案"]


def test_5_cuts_inside_quotes_only_as_a_last_resort():
    t = "一般来说，凡是“至少要改动多少条记录，才能让某件事成立”这类问题，敏感度都是 1。"
    e = ("In general, any question of the form, how many rows would you have to change to make something "
         "true, has sensitivity 1.")
    assert bi(t, e, 7.3) == [
        ("一般来说，凡是“至少要改动多少条记录，才能让某件事成立”",
         "In general, any question of the form, how many rows would you have to change to make something true,"),
        ("这类问题，敏感度都是 1", "has sensitivity 1.")]
    assert zh(t, 7.3) == ["一般来说，凡是“至少要改动多少条记录， / 才能让某件事成立”这类问题，敏感度都是 1"]


def test_6_no_cut_between_a_demonstrative_and_its_noun():
    assert zh("暂停想一想：分析者就不能把这些 query 也都拿去问交互式的管理者吗？", 5.8) == [
        "暂停想一想：分析者就不能把这些 query / 也都拿去问交互式的管理者吗？"]


def test_7_glossary_terms_are_words():
    assert S._word_bounds("它开创了我们今天所说的差分隐私") == frozenset({1, 3, 4, 6, 8, 10, 11, 15})
    assert 9 not in S._word_bounds("正是今天所说的本地化差分隐私")          # 本地化差分隐私 is one word
    assert S._cut_penalty("差分隐私", 2) >= 8 and S._cut_penalty("深度网络", 2) >= 8


def test_8_a_spoken_gloss_does_not_start_a_cue():
    assert S.split_balanced("它开创了我们今天所说的差分隐私，differential privacy，2017 年还获得了哥德尔奖。",
                            30, hang=True) == ["它开创了我们今天所说的差分隐私，differential privacy，",
                                               "2017 年还获得了哥德尔奖。"]
    assert S.split_balanced("所以隐私损失会累加，ε 就像一笔隐私预算，privacy budget。", 22) == [
        "所以隐私损失会累加，", "ε 就像一笔隐私预算，privacy budget。"]
    t = "这期视频讲它的三个核心想法：隐私的定义；一个数，叫敏感度，sensitivity；以及一个公式，算噪声加多少才够。"
    assert not any(p.startswith("sensitivity") for p in S.split_balanced(t, 30, hang=True))


def test_9_the_stronger_mark_wins_when_the_balance_is_close():
    assert bi("一开始是五五开的话，ε 取 0.1 最多有 52.5% 的把握；取 1 最多 73%。",
              "Starting from 50/50, ε = 0.1 leaves you at most 52.5% sure; ε = 1, at most 73%.", 9.4) == [
        ("一开始是五五开的话，ε 取 0.1 最多有 52.5% 的把握",
         "Starting from 50/50, ε = 0.1 leaves you at most 52.5% sure;"),
        ("取 1 最多 73%", "ε = 1, at most 73%.")]


def test_10_clause_cue_cuts_no_orphans_no_stray_lines():
    t = ("定理 3 表明，对其中至少 2/3 的 query，两个随机数据库的发布结果几乎一样：一个里每条记录的 mask 内都有"
         "偶数个 1，真实答案为 0；另一个里每条记录都有奇数个 1，真实答案为 n。")
    assert zh(t, 15.5) == ["定理 3 表明，对其中至少 2/3 的 query， / 两个随机数据库的发布结果几乎一样",
                           "一个里每条记录的 mask 内都有偶数个 1， / 真实答案为 0",
                           "另一个里每条记录都有奇数个 1，真实答案为 n"]
    assert zh("选中某个输出的概率，随它到真实答案的距离呈指数衰减，速率是 ε 除以两倍敏感度。", 8.2) == [
        "选中某个输出的概率， / 随它到真实答案的距离呈指数衰减", "速率是 ε 除以两倍敏感度"]
    assert S.split_balanced("2016 年，Abadi 和合作者让差分隐私深度学习真正可行", 22) == [
        "2016 年，Abadi 和合作者", "让差分隐私深度学习真正可行"]
    assert en("First: what is the sensitivity of the average of n numbers between 0 and 1?", 4.5) == [
        "First: what is the sensitivity / of the average of n numbers between 0 and 1?"]


def test_11_a_title_is_cut_before_its_opening_bracket():
    t = ("2006 年，Cynthia Dwork、Frank McSherry、Kobbi Nissim 和 Adam Smith，在这篇 paper 里回答了"
         "这两个问题：《Calibrating Noise to Sensitivity in Private Data Analysis》。")
    e = ("In 2006, Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith answered both questions in "
         "this paper: Calibrating Noise to Sensitivity in Private Data Analysis.")
    assert bi(t, e, 12.9) == [
        ("2006 年，Cynthia Dwork、Frank McSherry", "In 2006, Cynthia Dwork, Frank McSherry,"),
        ("Kobbi Nissim 和 Adam Smith", "Kobbi Nissim and Adam Smith"),
        ("在这篇 paper 里回答了这两个问题", "answered both questions in this paper:"),
        ("《Calibrating Noise to Sensitivity in Private Data Analysis》",
         "Calibrating Noise to Sensitivity in Private Data Analysis.")]
    assert zh(t, 12.9)[-1] == "《Calibrating Noise to Sensitivity / in Private Data Analysis》"


# ---------------------------------------------------------------- B. English lines

def test_12_no_english_line_ends_on_an_auxiliary_or_own():
    t = "Warner 的硬币，也就是随机响应：每个人自己扰动自己的记录，所以谁手里都没有原始数据；它的局限还要更大。"
    e = ("Warner's coin, randomized response, where each person scrambles their own row so nobody holds "
         "the raw data, is even more limited.")
    assert bi(t, e, 9.1) == [
        ("Warner 的硬币，也就是随机响应：每个人自己扰动自己的记录",
         "Warner's coin, randomized response, where each person scrambles their own row"),
        ("所以谁手里都没有原始数据；它的局限还要更大", "so nobody holds the raw data, is even more limited.")]


def test_13_names_and_set_phrases_stay_together():
    assert en("Then, in 2003, Irit Dinur and Kobbi Nissim proved something sobering.") == [
        "Then, in 2003, Irit Dinur and Kobbi Nissim / proved something sobering."]
    assert en("and it must hold whatever else the attacker knows.") == [
        "and it must hold whatever else / the attacker knows."]
    assert en(SWEENEY[1], 14.6)[0] == "Latanya Sweeney showed that ZIP code, / birth date and sex alone single out"
    assert S.split_balanced("For games that end on moves 7, 8 and 9, it gets much worse:", 48 * 0.55) == [
        "For games that end on moves 7, 8 and 9,", "it gets much worse:"]                   # tic-tac-toe
    e = ("Over the following decades, statisticians and computer scientists refined such tricks, in two "
         "flavours: scramble the data going in, or scramble the answers coming out.")
    assert en(e, 10) == ["Over the following decades, statisticians / and computer scientists refined such tricks,",
                         "in two flavours: scramble the data going in, / or scramble the answers coming out."]


def test_14_a_noun_phrase_stays_on_its_line():
    e = "The earlier framework's sharper analysis got this down to about √d, but it still grew with d."
    assert en(e, 6)[0] == "The earlier framework's sharper analysis / got this down to about √d,"


# ---------------------------------------------------------------- C. English line under each Chinese piece

def test_15_16_clause_pieces_up_to_the_measured_width():
    e = ("Answer too many questions too accurately, with errors much smaller than the square root of n, "
         "and an attacker can rebuild almost the entire database.")
    assert bi("问题答得太多、太准，误差远小于根号 n，攻击者就能重构出几乎整个数据库。", e, 7) == [
        ("问题答得太多、太准，误差远小于根号 n",
         "Answer too many questions too accurately, with errors much smaller than the square root of n,"),
        ("攻击者就能重构出几乎整个数据库", "and an attacker can rebuild almost the entire database.")]
    e = ("Fittingly, it appeared at a cryptography conference, where the habit is to define security "
         "against every possible attacker first, and then prove it.")
    t = "难怪它发表在密码学会议上：那里的习惯就是先定义安全性，要求能抵御所有可能的攻击者，再去证明。"
    assert bi(t, e, 8.9) == [
        ("难怪它发表在密码学会议上：那里的习惯就是先定义安全性",
         "Fittingly, it appeared at a cryptography conference, where the habit is to define security"),
        ("要求能抵御所有可能的攻击者，再去证明", "against every possible attacker first, and then prove it.")]
    t = "这不算侵犯隐私：同样的结论从其他人的数据里也能得出，所以就算把 Alice 的记录换成别人的，也照样会发生。"
    e = ("That is not a privacy violation: the same lesson could be learned from everyone else's data, "
         "so it would happen even if Alice's row were replaced by someone else's.")
    assert bi(t, e, 9.3) == [
        ("这不算侵犯隐私：同样的结论从其他人的数据里也能得出",
         "That is not a privacy violation: the same lesson could be learned from everyone else's data,"),
        ("所以就算把 Alice 的记录换成别人的，也照样会发生",
         "so it would happen even if Alice's row were replaced by someone else's.")]
    e = ("The ratio test catches it: the output showing Alice's real value has probability 1/n in one world, "
         "and 0 in the other.")
    assert bi("比值这一关能拦住它：显示 Alice 真实取值的输出，一个世界里概率是 1/n，另一个是 0。", e, 8.1) == [
        ("比值这一关能拦住它：显示 Alice 真实取值的输出",
         "The ratio test catches it: the output showing Alice's real value"),
        ("一个世界里概率是 1/n，另一个是 0", "has probability 1/n in one world, and 0 in the other.")]


def test_17_only_the_cut_without_a_stop_falls_back():
    assert [e for _, e in bi(*SWEENEY, 14.6)][2:] == [
        "and in 1997 she linked supposedly anonymous hospital records to a public voter list",
        "and found the governor of Massachusetts."]


def test_18_numbers_on_the_same_side_as_in_the_chinese():
    zp = ["一条拉普拉斯曲线的中心在 f(x)，也就是 41，另一条", "在 f(x′)，也就是 42：这就是两个世界的输出分布。"]
    e = "Center one Laplace curve at f(x), 41: and another at f(x′), 42, the output distributions of our two worlds."
    assert S._split_like(e, zp, 96 * 0.55) == (
        ["Center one Laplace curve at f(x), 41:",
         "and another at f(x′), 42, the output distributions of our two worlds."], False)
    zc = ["一条拉普拉斯曲线的中心在 f(x)，也就是这里，另一条", "在 f(y)，也就是那里：这就是两个世界的输出分布。"]
    e = ("Center one Laplace curve at f(x), here: and another at f(y), there, the output distributions of "
         "our two worlds.")
    assert S._split_like(e, zc, 96 * 0.55)[0][0].endswith("f(y),")           # by distance alone


def test_19_list_commas_whole_sentence_and_the_next_clause():
    assert bi("结论是：想对各种问题都答得准，又要强隐私，就让可信的管理者留在回路里。",
              "The lesson: for broad, flexible accuracy with strong privacy, keep the curator in the loop.", 6.6) == [
        ("结论是：想对各种问题都答得准", "The lesson: for broad, flexible accuracy"),
        ("又要强隐私，就让可信的管理者留在回路里", "with strong privacy, keep the curator in the loop.")]
    t = "同年她与 Kenthapadi、McSherry、Mironov 和 Naor 合作，在另一篇 paper 里引入了一个极小的松弛量 δ。"
    e = "Another 2006 paper, with Kenthapadi, McSherry, Mironov and Naor, added a tiny slack, δ."
    assert bi(t, e, 9.3) == [
        ("同年她与 Kenthapadi、McSherry、Mironov 和 Naor 合作",
         "Another 2006 paper, with Kenthapadi, McSherry, Mironov and Naor,"),
        ("在另一篇 paper 里引入了一个极小的松弛量 δ", "added a tiny slack, δ.")]
    t = ("2016 年，Abadi 和合作者让差分隐私深度学习真正可行：对每个样本的梯度做 clip（梯度裁剪），"
         "就像我们的收入上限，从而限制了敏感度；加上高斯噪声；并在成千上万步里跟踪预算。")
    e = ("In 2016, Abadi and colleagues made it practical to train deep networks privately: clip each "
         "example's gradient, like our income cap, which bounds its sensitivity; add Gaussian noise; and "
         "track the budget over thousands of steps.")
    assert bi(t, e, 16.2)[1:] == [
        ("对每个样本的梯度做 clip（梯度裁剪），就像我们的收入上限",
         "clip each example's gradient, like our income cap,"),
        ("从而限制了敏感度；加上高斯噪声；并在成千上万步里跟踪预算",
         "which bounds its sensitivity; add Gaussian noise; and track the budget over thousands of steps.")]
    # no clause stop near the Chinese cut, and it fits on one line: the whole sentence under both pieces
    e = "Games that end on move 8 or 9 have at most one empty square, so they were counted just once."
    assert bi("在第 8 步或第 9 步结束的对局，最多只剩一个空格子，所以它们只算了一次。", e, 6.5) == [   # tic-tac-toe
        ("在第 8 步或第 9 步结束的对局", e), ("最多只剩一个空格子，所以它们只算了一次", e)]


# ---------------------------------------------------------------- D. Other

def test_20_split_k_joins_where_the_halves_balance():
    t = "一个亿万富翁，就能让答案变动 10 亿，不封顶就根本没有上限。"
    assert S._split_k(t, 2, 30) == ["一个亿万富翁，就能让答案变动 10 亿，", "不封顶就根本没有上限。"]


def test_21_timing_follows_the_spoken_form():
    t = "满足差分隐私的机制，让比值处处接近 1：不超过 e^ε，也不低于 e^(−ε)。"
    say = "满足差分隐私的机制，让比值处处接近一：不超过 E 的艾普西隆次方，也不低于 E 的负艾普西隆次方。"
    e = "A private mechanism keeps that ratio close to 1 everywhere: never above e^ε, never below e^(−ε)."
    shown = S.tracks([(0.0, 8.75, t, e)])["zh-en"]
    spoken = S.tracks([(0.0, 8.75, t, e, say)])["zh-en"]
    assert [c[2:] for c in spoken] == [c[2:] for c in shown]
    assert round(shown[0][1], 2) == 4.89 and round(spoken[0][1], 2) == 3.59       # e^ε takes long to say
    gloss = S._spoken_weights("对 counting query（计数查询），比如医院那个",
                              ["对 counting query（计数查询），", "比如医院那个"], "对 counting query，比如医院那个")
    assert gloss == [S.units("对 counting query，"), 6.0]                          # the gloss is not read
    assert S.tracks([(0.0, 8.75, t, e, say)], timing="en") == S.tracks([(0.0, 8.75, t, e)], timing="en")


def test_21_sentence_pairs_pass_the_spoken_form():
    clip = {"start": 1.0, "end": 4.0, "text": "No. A computer can do more than count.",
            "marks": [[0, 0.0], [4, 1.0]], "tr": ["不是。", "电脑能做的，不只是统计对局。"],
            "tr_spans": [[0.0, 0.6], [0.9, 3.0]], "tr_say": ["不是。", "电脑能做的，不只是统计对局。"]}
    assert S.sentence_pairs(clip, 10.0) == [
        (11.0, 11.6, "不是。", "No.", "不是。"),
        (11.9, 14.0, "电脑能做的，不只是统计对局。", "A computer can do more than count.",
         "电脑能做的，不只是统计对局。")]


# ---------------------------------------------------------------- cases fixed before this round

def test_merged_cue_keeps_its_sentence_mark():                           # tic-tac-toe video
    tr = S.tracks([(0.0, 0.6, "不是。", "No."),
                   (0.92, 3.4, "电脑能做的，不只是统计对局。", "A computer can do more than count.")])
    assert tr["zh"] == [(0.0, 3.4, "不是。电脑能做的，不只是统计对局")]
    assert tr["zh-en"] == [(0.0, 3.4, "不是。电脑能做的，不只是统计对局", "No. A computer can do more than count.")]


def test_billionaire_sentence():
    t = "一个亿万富翁，就能让答案变动 10 亿，不封顶就根本没有上限。"
    e = "One billionaire can move that answer by a billion, and with no cap there is no limit at all."
    assert S._split_like(e, S._split_k(t, 2, 30), 88 * 0.55) == (
        ["One billionaire can move that answer by a billion,", "and with no cap there is no limit at all."], False)
    assert bi(t, e, 6) == [("一个亿万富翁，就能让答案变动 10 亿，不封顶就根本没有上限", e)]   # now fits one line


def test_no_sidecar_cue_needs_three_lines():
    """Every sentence of both videos: sidecar cues have at most 2 lines within the limits, and the
    bilingual lines stay within 30 units (35 for a whole 《…》 title) and 110 characters."""
    from explainer import i18n
    from explainer.voice import split_sentences

    for video in ("dwork2006-calibrating-noise", "tictactoe-255168"):
        pairs, t = [], 0.0
        for english, line in i18n.narration("zh", REPO / "videos" / video).items():
            ens = [s for _, s in split_sentences(english)]
            ens = [d or s for s, d in zip(ens, list(line.en_display) + [None] * len(ens))]
            for z, e, say in zip(line.sentences, ens, line.spoken):
                d = S.units(say) / 4.5
                pairs.append((t, t + d, z, e, say))
                t += d + S.SENTENCE_GAP
            t += 0.7
        for timing in ("tr", "en"):
            tr = S.tracks(pairs, timing=timing)
            for _, _, text in tr["zh"]:
                assert len(text.split("\n")) <= 2 and all(S.units(ln) <= 22 for ln in text.split("\n")), text
            for _, _, text in tr["en"]:
                assert len(text.split("\n")) <= 2 and all(len(ln) <= 48 for ln in text.split("\n")), text
            for _, _, z, e in tr["zh-en"]:
                assert S.units(z) <= (35 if z.startswith("《") else 30) and len(e) <= 110, (z, e)
