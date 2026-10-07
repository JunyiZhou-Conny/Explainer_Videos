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
    assert bi(*SWEENEY, 14.6)[1][0] == "光凭邮编、出生日期和性别，就能唯一识别大多数美国人"     # round 3: and
    assert zh(SWEENEY[0], 14.6)[:2] == ["Latanya Sweeney 发现",                               # 光凭……，就……
                                        "光凭邮编、出生日期和性别， / 就能唯一识别大多数美国人"]  # stays whole
    assert S.split_balanced("Dwork、Rothblum 和 Vadhan 还带来了一个惊喜", 22) == [
        "Dwork、Rothblum 和 Vadhan", "还带来了一个惊喜"]
    t = "光凭邮编{}出生日期和性别就能唯一识别大多数美国人"
    assert S._mark_cost("Dwork、Rothblum", 6) > S._mark_cost(t.format("、"), 5) > S._mark_cost(t.format("，"), 5)


def test_2_no_line_ends_on_de_or_a_negation():
    assert zh(SWEENEY[0], 14.6)[2] == ("1997 年，她把号称匿名的病历和公开的选民名单 / "
                                       "一对照，就认出了马萨诸塞州州长")
    for word in ("公开的", "不", "没"):
        assert S._cut_penalty(word + "选民名单", len(word)) >= 6


def test_3_no_line_starts_with_a_postposition():
    assert S.split_balanced("clip 到一定大小以内（梯度裁剪）", 12) == ["clip 到一定", "大小以内（梯度裁剪）"]


def test_4_a_gloss_stays_with_its_term():
    assert zh("这种链式 trick 叫 hybrid argument（混合论证），最后还会再出现。", 5) == [
        "这种链式 trick / 叫 hybrid argument（混合论证）", "最后还会再出现"]               # not "叫 /"
    assert zh("每个桶单独算一个 counting query（计数查询），预算平均分配。", 4.2) == [
        "每个桶单独算 / 一个 counting query（计数查询）", "预算平均分配"]                  # not "一个 /"
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
    assert bi(t, e, 9.1) == [                     # one clause per cue (round 2: no cue runs on across ；)
        ("Warner 的硬币，也就是随机响应", "Warner's coin, randomized response,"),
        ("每个人自己扰动自己的记录，所以谁手里都没有原始数据",
         "where each person scrambles their own row so nobody holds the raw data,"),
        ("它的局限还要更大", "is even more limited.")]


def test_13_names_and_set_phrases_stay_together():
    assert en("Then, in 2003, Irit Dinur and Kobbi Nissim proved something sobering.") == [
        "Then, in 2003, Irit Dinur and Kobbi Nissim / proved something sobering."]
    assert en("and it must hold whatever else the attacker knows.") == [
        "and it must hold / whatever else the attacker knows."]
    assert en(SWEENEY[1], 14.6) == [                   # round 2: no cue cut inside the list; round 3:
        "Latanya Sweeney showed",                       # nor a line break ("birth date / and sex"),
        "that ZIP code, birth date and sex alone / single out most Americans,",   # nor "anonymous / hospital"
        "and in 1997 she linked / supposedly anonymous hospital records",
        "to a public voter list / and found the governor of Massachusetts."]
    assert S.split_balanced("For games that end on moves 7, 8 and 9, it gets much worse:", 48 * 0.55) == [
        "For games that end on moves 7, 8 and 9,", "it gets much worse:"]                   # tic-tac-toe
    e = ("Over the following decades, statisticians and computer scientists refined such tricks, in two "
         "flavours: scramble the data going in, or scramble the answers coming out.")
    assert en(e, 10) == ["Over the following decades,",                       # round 4: not "statisticians /
                         "statisticians and computer scientists / refined such tricks,",   # and computer…"
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
        ("结论是：想对各种问题都答得准，又要强隐私", "The lesson: for broad, flexible accuracy with strong privacy,"),
        ("就让可信的管理者留在回路里", "keep the curator in the loop.")]      # round 2: 想……，又要…… stays whole
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
    assert bi(t, e, 16.2)[1:] == [                     # round 3: one ； run-on instead of two, not "// 从而"
        ("对每个样本的梯度做 clip（梯度裁剪）", "clip each example's gradient,"),
        ("就像我们的收入上限，从而限制了敏感度", "like our income cap, which bounds its sensitivity;"),
        ("加上高斯噪声；并在成千上万步里跟踪预算", "add Gaussian noise; and track the budget over thousands of steps.")]
    assert zh(t, 16.2)[1:] == ["对每个样本的梯度做 clip（梯度裁剪）， / 就像我们的收入上限，从而限制了敏感度",
                               "加上高斯噪声；并在成千上万步里跟踪预算"]
    # no clause stop near the Chinese cut: a clean gap a little further than a plain one may be
    e = "Games that end on move 8 or 9 have at most one empty square, so they were counted just once."
    assert bi("在第 8 步或第 9 步结束的对局，最多只剩一个空格子，所以它们只算了一次。", e, 6.5) == [   # tic-tac-toe
        ("在第 8 步或第 9 步结束的对局", "Games that end on move 8 or 9"),          # (round 2: the whole
        ("最多只剩一个空格子，所以它们只算了一次", "have at most one empty square, so they were counted just once.")]
    # nothing to cut at, and it fits on one line: the whole sentence under both pieces          # sentence)
    e = "Sweeney found the governor of Massachusetts in it."
    assert S._split_like(e, ["她就在里面，", "找到了马萨诸塞州州长的病历。"], 96 * 0.55) == ([e, e], True)


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
            for _, _, text in tr["zh"]:                  # (+1.5 for a list of Latin names, see test_r2_lists;
                assert len(text.split("\n")) <= 2 and all(S.units(ln) <= 23.5 for ln in text.split("\n")), text
                assert all(S.units(ln) <= 22 or S._NAME_LIST.search(ln)          # +0.5 for an item of a ；-list)
                           or (ln.endswith("；") and S.units(ln) <= 22.5 and S._SEMI_LIST.search(text.replace("\n", "")))
                           for ln in text.split("\n")), text
            for _, _, text in tr["en"]:
                assert len(text.split("\n")) <= 2 and all(len(ln) <= 48 for ln in text.split("\n")), text
            for _, _, z, e in tr["zh-en"]:
                assert S.units(z) <= (35 if z.startswith("《") else 30) and len(e) <= 110, (z, e)


# ---------------------------------------------------------------- round 2 (two reviewers' findings)

def test_r2_glossary_headwords_only():
    terms = S._glossary_terms()
    assert "差分隐私" in terms and "拉普拉斯机制" in terms
    for phrase in ("标题就叫", "公开的选民名单", "让可信", "一个极小", "列表里", "保持英文"):
        assert phrase not in terms
    t = "同一年，Dwork 的特邀论文标题就叫《Differential Privacy》，给这个领域起了沿用至今的名字。"
    assert zh(t, 7.45)[0] == "同一年，Dwork 的特邀论文标题 / 就叫《Differential Privacy》"


def test_r2_an_english_gloss_may_take_the_second_line():
    t = "它开创了我们今天所说的差分隐私（differential privacy），2017 年还获得了哥德尔奖。"
    assert zh(t, 7.35)[0] == "它开创了我们今天所说的差分隐私 / （differential privacy）"
    assert S.split_balanced("hybrid argument（混合论证）", 8) == ["hybrid argument（混合论证）"]   # never a cue cut


def test_r2_a_short_chinese_cue_gets_time_to_read():
    tr = S.tracks([(6.99, 10.52, "这里说的“一局”，指的是从第一步到最后一步、按顺序排好的全部走法。",
                    "By a game, we mean the whole list of moves, in order.")], timing="en")
    (a, b, z, _), (_, d, z2, _) = tr["zh-en"]
    assert z == "这里说的“一局”" and b - a >= 1.0                                 # was 0.68 s
    assert S.units(z2) / (d - b) <= 9.5                   # round 3: and not at the cost of its neighbour
    tr = S.tracks([(169.92, 174.52, "然后在 2003 年，Irit Dinur 和 Kobbi Nissim 证明了一个令人警醒的结论。",
                    "Then, in 2003, Irit Dinur and Kobbi Nissim proved something sobering.")], timing="en")
    assert [c[2] for c in tr["zh"]] == ["然后在 2003 年，Irit Dinur 和 Kobbi Nissim\n证明了一个令人警醒的结论"]
    # round 3: (was "然后在 2003 年" alone, 1.09 s): a line of Latin names may run 1.5 units over


def test_r2_lists_stay_whole():
    assert zh("第三，答案不一定是一个数：一个排名、一个集合、一个比特串，凡是答案之间能定义距离的都行。", 8.4) == [
        "第三，答案不一定是一个数", "一个排名、一个集合、一个比特串， / 凡是答案之间能定义距离的都行"]
    assert zh("这里说的“一局”，指的是从第一步到最后一步、按顺序排好的全部走法。", 5.8) == [
        "这里说的“一局”，指的是 / 从第一步到最后一步、按顺序排好的全部走法"]
    t = "同年她与 Kenthapadi、McSherry、Mironov 和 Naor 合作，在另一篇 paper 里引入了一个极小的松弛量 δ。"
    first = zh(t, 9.3)[0]                                  # a list of Latin names may run 1.5 units over
    assert first == "同年她与 / Kenthapadi、McSherry、Mironov 和 Naor 合作" and S.units(first.split(" / ")[1]) <= 23.5


def test_r2_the_stronger_mark_structures_the_cues():
    assert zh("我们用的编程语言叫 Python；在 Python 里，列表里的位置从零开始编号，所以格子的编号是 0 到 8。", 8.6) == [
        "我们用的编程语言叫 Python", "在 Python 里，列表里的位置从零开始编号， / 所以格子的编号是 0 到 8"]
    assert zh("接下来是一个函数：在编程里，函数就是一小段有名字的程序。", 5.2) == [
        "接下来是一个函数： / 在编程里，函数就是一小段有名字的程序"]
    t = ("第二：如果一个算法读到每条记录的概率都很小，比如只看一个小规模随机样本；而且大多数时候都能把 f 近似到 σ 以内，"
         "在每个数据库上都是这样；那么 f 的敏感度最多是两倍 σ。")
    assert zh(t, 16) == ["第二：如果一个算法读到每条记录的概率都很小， / 比如只看一个小规模随机样本",
                         "而且大多数时候都能把 f 近似到 σ 以内， / 在每个数据库上都是这样", "那么 f 的敏感度最多是两倍 σ"]
    e = ("Second: if an algorithm that rarely looks at any particular row, like one working from a small random "
         "sample, approximates f to within σ most of the time, on every database, then f has sensitivity at most 2σ.")
    assert bi(t, e, 16)[3:] == [("在每个数据库上都是这样", "on every database,"),     # no cue runs on across ；
                                ("那么 f 的敏感度最多是两倍 σ", "then f has sensitivity at most 2σ.")]


def test_r2_a_short_clause_stays_with_the_clause_it_continues_or_glosses():
    assert zh("下次有人说数据集匿名化了，所以很安全，你就知道真正该问的是：用的是多大的 ε，什么才算一个人的一条记录？",
              10)[0] == "下次有人说数据集匿名化了，所以很安全， / 你就知道真正该问的是"
    assert zh("这个函数叫 winner，意思是“赢家”，它会检查每一条线。", 4.8) == [
        "这个函数叫 winner，意思是“赢家”， / 它会检查每一条线"]
    assert bi("填满这 4 个空格子，有 4 乘 3 乘 2 乘 1，也就是 24 种不同的顺序。",      # at the end: not a gloss
              "The 4 empty squares can be filled in 4 times 3 times 2 times 1, so 24 ways.", 6) == [
        ("填满这 4 个空格子，有 4 乘 3 乘 2 乘 1", "The 4 empty squares can be filled in 4 times 3 times 2 times 1,"),
        ("也就是 24 种不同的顺序", "so 24 ways.")]


def test_r2_srt_cues_split_by_two_lines_are_timed_by_the_spoken_form():
    t = "让 λ 取敏感度除以 ε，比值就始终在 e^ε 以内，对任意输出、任意一对相邻数据库都成立。"
    say = "让 lambda 取敏感度除以艾普西隆，比值就始终在 E 的艾普西隆次方以内，对任意输出、任意一对相邻数据库都成立。"
    e = "Set λ to the sensitivity over ε, and the ratio stays within e^ε, for every output and every pair of neighbors."
    spoken = S.tracks([(0.0, 9.96, t, e, say)])
    assert spoken["zh"][0][1] == spoken["zh-en"][0][1]                           # the same switch point
    assert abs(S.tracks([(0.0, 9.96, t, e)])["zh"][0][1] - spoken["zh"][0][1]) > 0.5


def test_r2_english_float_width():
    assert S.units("x" * 48) <= 48 * 0.55
    e = "Cryptography often settles for something weaker:"                       # 48 characters: one line
    assert en(e, 3) == [e]


def test_r2_english_clause_cues_rather_than_mid_phrase_lines():
    cases = {
        "The hopeful flip side: with a limited number of questions, modest noise is enough.":
            ["The hopeful flip side:", "with a limited number of questions, / modest noise is enough."],
        "Each swap barely moves the output, and unless n is huge, all n swaps together barely move it.":
            ["Each swap barely moves the output, / and unless n is huge,", "all n swaps together barely move it."],
        "The noise outgrows n, bigger than the count could ever be, and the answer is pure noise.":
            ["The noise outgrows n, / bigger than the count could ever be,", "and the answer is pure noise."],
        "Games that end on move 8 or 9 have at most one empty square, so they were counted just once.":
            ["Games that end on move 8 or 9 / have at most one empty square,", "so they were counted just once."],
        "But SuLQ only covered sums, and its definition tolerated a tiny chance of a large leak.":
            ["But SuLQ only covered sums,", "and its definition tolerated / a tiny chance of a large leak."],
        "The program plays one game, filling the squares in order, until X makes a diagonal on move 7.":
            ["The program plays one game, / filling the squares in order,", "until X makes a diagonal on move 7."],
        "Remember the Gaussian whose ratio escaped the band in the tails?":           # a clean re-wrap
            ["Remember the Gaussian / whose ratio escaped the band in the tails?"],
        "Scoring every possible answer became McSherry and Talwar's exponential mechanism.":   # names
            ["Scoring every possible answer became / McSherry and Talwar's exponential mechanism."],
        "so it would happen even if Alice's row were replaced by someone else's.":     # not "even // if"
            ["so it would happen even if Alice's row / were replaced by someone else's."],
    }
    for e, cues in cases.items():
        assert en(e, 6.5) == cues, e


def test_r2_english_lines_keep_phrases():
    cases = {
        "Adding up absolute changes across coordinates like this is the L1 norm,":
            "Adding up absolute changes / across coordinates like this is the L1 norm,",
        "the US Census Bureau protected its published tables with differential privacy;":
            "the US Census Bureau protected / its published tables with differential privacy;",
        "The lesson: for broad, flexible accuracy with strong privacy,":
            "The lesson: for broad, flexible accuracy / with strong privacy,",
        "Center one Laplace curve at f(x), 41, and another at f(x′), 42:":
            "Center one Laplace curve at f(x), 41, / and another at f(x′), 42:",
        "Instead it draws random noise, Y, and releases f(x) + Y.":
            "Instead it draws random noise, Y, / and releases f(x) + Y.",
        "with a surprise from Dwork, Rothblum and Vadhan: allow that tiny δ,":
            "with a surprise from Dwork, Rothblum and Vadhan: / allow that tiny δ,",
        "that chess has at least 10 to the power of 120 possible games.":   # round 4: "has" is a main verb,
            "that chess has / at least 10 to the power of 120 possible games.",   # "at least / 10" costs more
        "Treat each bin as its own counting query and split the budget evenly.":
            "Treat each bin as its own counting query / and split the budget evenly.",
        "Multiplying the choices gives nine factorial, 362,880 orders.":
            "Multiplying the choices gives nine factorial, / 362,880 orders.",
    }
    for e, cue in cases.items():
        assert en(e, 5) == [cue], e
    assert S._list_comma("Latanya Sweeney showed that ZIP code, birth date and sex", 37)
    assert not S._list_comma("Over the following decades, statisticians and computer scientists", 27)
    assert not S._list_comma("In 1950, the mathematician and engineer", 8)


def test_r2_band_alignment():
    def pairs(t, e, d):
        return [e2 for _, e2 in bi(t, e, d)]
    assert pairs("早先的 SuLQ 框架分析得更细，把噪声降到大约根号 d，但还是随 d 增大。",          # a gap, not a repeat
                 "The earlier framework's sharper analysis got this down to about √d, but it still grew with d.",
                 6.2) == ["The earlier framework's sharper analysis",
                          "got this down to about √d, but it still grew with d."]
    assert [e for _, e in bi(*SWEENEY, 14.6)][:2] == [                                       # the list whole
        "Latanya Sweeney showed", "that ZIP code, birth date and sex alone single out most Americans,"]
    assert pairs("另一种做法是发布一张经过隐私处理的表，然后撒手不管，这叫非交互式。",
                 "The alternative, publishing one sanitized table and walking away, is non-interactive.", 6) == [
        "The alternative, publishing one sanitized table", "and walking away, is non-interactive."]
    assert pairs("像这样把各个分量变化的绝对值加起来，就是 L1 范数，原文就用它来衡量一列数的敏感度。",       # L1 under L1
                 "Adding up absolute changes across coordinates like this is the L1 norm, the paper's way to "
                 "measure sensitivity for lists of numbers.", 8.1)[1].startswith("is the L1 norm,")
    e = "We simply list all 8 winning lines, as groups of three square numbers."    # round 3: one number
    assert pairs("我们直接把所有能赢的线都列出来，一共 8 条，每条线写成一组三个格子编号。", e, 6.5) == [   # restated
        "We simply list all 8 winning lines,", "as groups of three square numbers."]  # by 一共 8 条: not a repeat
    assert pairs("在第 7、8、9 步结束的对局就麻烦多了：我们必须检查之前的每一步有没有人赢，而且下满的棋盘可能是有人赢，"
                 "也可能是平局。", "For games that end on moves 7, 8 and 9, it gets much worse: we'd have to check every "
                 "earlier move for a win, and a full board might be a win or a draw.", 11.5)[0] == (
        "For games that end on moves 7, 8 and 9, it gets much worse:")                        # ： under ：
    assert pairs("把每根柱子乘上各自被算的次数，再全部加起来，正好又是 9 的阶乘。",                    # clause counts
                 "Multiply each bar by its number, add them up, and you get exactly nine factorial again.", 6) == [
        "Multiply each bar by its number,", "add them up, and you get exactly nine factorial again."]
    assert pairs("我们的 explore 会沿着每一条分支往下走，一次走一条，再数一数走到了多少片叶子。",
                 "Explore walks down every branch, one at a time, and counts the leaves it reaches.", 7) == [
        "Explore walks down every branch,", "one at a time, and counts the leaves it reaches."]
    assert pairs("如果一条线上三个格子放的都一样，而且不是点，那这是谁的棋子，谁就赢了。",          # 而且 / and
                 "If all three squares on a line hold the same mark, and that mark isn't a dot, that player has won.",
                 6.1) == ["If all three squares on a line hold the same mark, and that mark isn't a dot,",
                          "that player has won."]
    assert pairs("第四，一张满足差分隐私的公开表，答不好大多数简单的奇偶 query，除非数据库大到指数级。",
                 "Four: one private published table cannot answer most simple parity counts unless the database "
                 "is exponentially large.", 8.2)[0] == "Four: one private published table"
    assert pairs("还记得吗，9 的阶乘把在第 5 步结束的每一局，都算了 24 次，每个幽灵对局算一次。",       # 5 under 5
                 "Remember, nine factorial counted each game that ends on move 5 a total of 24 times, once for "
                 "each ghost ending.", 7.2)[0] == "Remember, nine factorial counted each game that ends on move 5"


# ---------------------------------------------------------------- round 3 (two reviewers' findings)

SURPRISE = [(557.25, 559.79, "没想到吧：答案是边格，也就是每条边正中间的那一格，有 29,592 种对局。",
             "Surprise: the edge, with 29,592 games."),
            (560.11, 564.44, "每个角格有 27,732，而中心最少，只有 25,872。",
             "Each corner gives 27,732, and the center the fewest, just 25,872.")]


def test_r3_english_video_band_reads_at_9_units_a_second():
    tr = S.tracks(SURPRISE, timing="en")            # tic-tac-toe, English video (timed by the English)
    (a, b, z, _), (_, d, _, _), (f, _, _, _) = tr["zh-en"]
    assert S.units(z) / (b - a) <= 10.5 and d - b >= 1.0      # round 2: 24 units in 1.30 s (18.5 units/s)
    assert f - SURPRISE[1][0] <= 0.5 + 1e-9                   # the next sentence starts at most 0.5 s late
    assert [c[:2] for c in tr["zh"]] == [c[:2] for c in tr["zh-en"]]   # the sidecar switches with the band
    t = "同年她与 Kenthapadi、McSherry、Mironov 和 Naor 合作，在另一篇 paper 里引入了一个极小的松弛量 δ。"
    e = "Another 2006 paper, with Kenthapadi, McSherry, Mironov and Naor, added a tiny slack, δ."
    tr = S.tracks([(1228.96, 1234.76, t, e), (1235.08, 1239.35, "还记得高斯噪声的比值在尾部冲出带外吗？",
                    "Remember the Gaussian whose ratio escaped the band in the tails?")], timing="en")
    (_, b, _, _), (_, d, z2, _) = tr["zh-en"][:2]
    assert S.units(z2) / (d - b) <= 9.0 + 1e-6                # round 2: 21 units in 1.60 s
    slow = S.tracks([(0.0, 6.0, "两个随机数据库的发布结果几乎一样，一个里每条记录都有偶数个 1。",
                      "the release looks almost the same for a random database where every row has even parity,")],
                    timing="en")["zh-en"]
    english = S._proportional(0.0, 6.0, [c[3] for c in slow])          # readable at the English pace:
    assert [round(c[1], 6) for c in slow] == [round(c[1], 6) for c in english]   # the English stays put


def test_r3_sidecar_switches_where_the_band_switches_in_the_english_video():
    tr = S.tracks([(149.54, 164.12, *SWEENEY)], timing="en")
    band = {round(c[1], 6) for c in tr["zh-en"]}
    assert all(round(c[1], 6) in band for c in tr["zh"])        # round 2: 44 of 58 switches off by > 0.2 s


def test_r3_a_cue_that_cannot_linger_to_one_second_borrows_across_the_gap():
    tr = S.tracks([(0.0, 0.71, "为什么？", "Why?"),
                   (1.03, 5.0, "中心在 4 条获胜线上，角格在 3 条上，而边格只在 2 条上。",
                    "The center sits on 4 winning lines, a corner on 3, and an edge on just 2.")])
    for track in ("zh", "en", "zh-en"):
        assert all(c[1] - c[0] >= 1.0 - 1e-6 for c in tr[track]), track    # round 2: 0.98 s


def test_r3_english_cue_cuts():
    cases = {
        "Pause and ponder: couldn't an analyst just ask the interactive curator all of these queries too?":
            ["Pause and ponder: couldn't an analyst",           # round 4: a 3-line cue is cut at one of its own
             "just ask the interactive curator / all of these queries too?"],   # line breaks (not "…ask the //")
        "Third, the answer need not be a number: a ranking, a set, a string of bits, anything with a distance "
        "between answers.": ["Third, the answer need not be a number:",                    # no cut in a list
                             "a ranking, a set, a string of bits, / anything with a distance between answers."],
        "Unless the database is exponentially large: roughly, every 4 extra bits per row doubles the rows you "
        "would need.": ["Unless the database is exponentially large:",                       # not "roughly," alone
                        "roughly, every 4 extra bits per row / doubles the rows you would need."],
        "Pick an output with probability that decays exponentially with its distance from the true answer, at a "
        "rate of ε over twice the sensitivity.": ["Pick an output with probability / that decays exponentially",
                                                  "with its distance from the true answer, / at a rate of ε over twice the sensitivity."],
        "Section 4 only rules out one release that is accurate for most of a huge family of questions.":
            ["Section 4 only rules out one release", "that is accurate / for most of a huge family of questions."],
        "Trying a path, then stepping back to try the next one, is called backtracking.":      # tic-tac-toe
            ["Trying a path, then stepping back / to try the next one, is called backtracking."],
        "X plays moves 1, 3 and 5, so the fifth move is the first time anyone can have three marks.":
            ["X plays moves 1, 3 and 5,", "so the fifth move is the first time / anyone can have three marks."],
        "One: privacy means changing any one person's row changes the probability of any output by at most a "
        "factor of e^ε.": ["One: privacy means changing any one person's row",
                           "changes the probability of any output / by at most a factor of e^ε."],
    }
    for e, cues in cases.items():
        assert en(e, 6.5) == cues, e
    e = ("In 2006, Cynthia Dwork, Frank McSherry, Kobbi Nissim and Adam Smith answered both questions in this "
         "paper: Calibrating Noise to Sensitivity in Private Data Analysis.")
    assert en(e, 12.9)[:2] == ["In 2006, Cynthia Dwork, Frank McSherry, / Kobbi Nissim and Adam Smith",
                               "answered both questions in this paper:"]
    t = ("Theorem 3 shows that for at least 2/3 of these queries, the release looks almost the same for a random "
         "database where every row has even parity, true answer 0, as for one where every row is odd, true answer n.")
    assert en(t, 15.5)[2:] == ["where every row has even parity, true answer 0,",
                               "as for one / where every row is odd, true answer n."]
    q = "couldn't an analyst just ask the interactive curator"
    assert S._cue_cost(q, q.index("interactive")) >= 20                                   # never after "the"


def test_r3_english_lines():
    cases = {
        "A week later, one new patient, Alice, is admitted.": "A week later, / one new patient, Alice, is admitted.",
        "At the end, the paper proves the first is fundamentally more powerful.":    # not "the first / is…"
            "At the end, the paper proves / the first is fundamentally more powerful.",
        "the paper's way to measure sensitivity for lists of numbers.":
            "the paper's way to measure sensitivity / for lists of numbers.",
        "Three: Laplace noise with scale sensitivity/ε makes it private,":
            "Three: Laplace noise / with scale sensitivity/ε makes it private,",
        "Theorem 3 shows that for at least 2/3 of these queries,": "Theorem 3 shows / that for at least 2/3 of these queries,",
        "It founded what we now call differential privacy,": "It founded / what we now call differential privacy,",
        "that ZIP code, birth date and sex alone single out most Americans,":
            "that ZIP code, birth date and sex alone / single out most Americans,",
    }
    for e, cue in cases.items():
        assert en(e, 5) == [cue], e


def test_r3_english_video_srt_lines():
    from explainer import build

    def srt(t):
        return [c[2].replace("\n", " / ") for c in build.split_cues(0.0, len(t) / 15, t)]
    assert srt("The earlier framework's sharper analysis got this down to about the square root of d, but it "
               "still grew with d.") == ["The earlier framework's sharper analysis / got this down to about the "
                                         "square root of d,", "but it still grew with d."]   # not "…got / this"
    assert srt("Instead, teach a computer the rules, and let it play every possible game, one by one.") == [
        "Instead, teach a computer the rules,", "and let it play every possible game, / one by one."]   # "let / it"
    assert srt("Another 2006 paper, with Kenthapadi, McSherry, Mironov and Naor, added a tiny slack, delta.") == [
        "Another 2006 paper, / with Kenthapadi, McSherry, Mironov and Naor,", "added a tiny slack, delta."]
    assert srt("and in 1997 she linked supposedly anonymous hospital records to a public voter list and found "
               "the governor of Massachusetts.")[-1] == "to a public voter list / and found the governor of Massachusetts."


def test_r3_chinese_cue_cuts():
    t = "命题 2：即使每条记录都用同一个 mask，对大多数 mask，它也估计不出奇数记录的个数，除非 n 大到指数级。"
    e = ("Proposition 2: even when every row uses the same mask, for most masks it cannot estimate the odd count "
         "unless n is exponentially large.")
    assert zh(t, 9.2) == ["命题 2：即使每条记录都用同一个 mask",                     # a short scope phrase
                          "对大多数 mask，它也估计不出奇数记录的个数， / 除非 n 大到指数级"]   # starts its clause
    assert bi(t, e, 9.2) == [("命题 2：即使每条记录都用同一个 mask", "Proposition 2: even when every row uses the same mask,"),
                             ("对大多数 mask，它也估计不出奇数记录的个数", "for most masks it cannot estimate the odd count"),
                             ("除非 n 大到指数级", "unless n is exponentially large.")]
    t = "不如教电脑学会规则，再让它一局接一局，把所有可能的对局都下一遍。"                 # tic-tac-toe
    e = "Instead, teach a computer the rules, and let it play every possible game, one by one."
    assert zh(t, 5.8) == ["不如教电脑学会规则， / 再让它一局接一局，把所有可能的对局都下一遍"]
    assert bi(t, e, 5.8) == [("不如教电脑学会规则", "Instead, teach a computer the rules,"),     # 一局接一局
                             ("再让它一局接一局，把所有可能的对局都下一遍", "and let it play every possible game, one by one.")]
    assert zh("任何确定性的规则，只要答案会变，就一定在某处有这样的跳变。", 5.2) == [       # 只要……，就……
        "任何确定性的规则， / 只要答案会变，就一定在某处有这样的跳变"]
    assert zh("难怪它发表在密码学会议上：那里的习惯就是先定义安全性，要求能抵御所有可能的攻击者，再去证明。", 8.9) == [
        "难怪它发表在密码学会议上", "那里的习惯就是先定义安全性， / 要求能抵御所有可能的攻击者，再去证明"]   # 先……再……
    assert S._mark_cost("就像我们的收入上限，从而限制了敏感度", 10) >= 8                   # never "// 从而"


def test_r3_a_line_of_latin_names_may_run_over_rather_than_leave_a_scrap():
    t = ("隐私预算发展成了一套组合定理，Dwork、Rothblum 和 Vadhan 还带来了一个惊喜：只要允许那个极小的 δ，"
         "k 个问题的总损失就只按根号 k 增长。")
    assert zh(t, 12.7)[0] == "隐私预算发展成了一套组合定理， / Dwork、Rothblum 和 Vadhan 还带来了一个惊喜"
    assert zh("然后在 2003 年，Irit Dinur 和 Kobbi Nissim 证明了一个令人警醒的结论。", 4.6) == [
        "然后在 2003 年，Irit Dinur 和 Kobbi Nissim / 证明了一个令人警醒的结论"]           # round 2: "然后在 2003 年"
    assert S._wrapped("这篇 paper 迈出了一大步：适用于数据的任意函数，只用一个干净的定义和一条简单的噪声规则", 22) != (
        "这篇 paper 迈出了一大步：适用于数据的任意", "函数，只用一个干净的定义和一条简单的噪声规则")    # only for names


def test_r3_band_cuts():
    def pairs(t, e, d):
        return [e2 for _, e2 in bi(t, e, d)]
    assert pairs("第三，尺度为敏感度除以 ε 的拉普拉斯噪声，就能让它满足差分隐私，数据库再大，误差也不会变大。",
                 "Three: Laplace noise with scale sensitivity/ε makes it private, with error that does not grow "
                 "with the database.", 9.9) == ["Three: Laplace noise with scale sensitivity/ε",     # a plain gap
                                                "makes it private, with error that does not grow with the database."]
    assert pairs("如果没有一条线符合，winner 什么也没找到，就返回 None，意思是“没有人”。",          # 如果……，就……
                 "If no line matches, winner finds nothing, and hands back None, which means nobody.", 5.5) == [
        "If no line matches,", "winner finds nothing, and hands back None, which means nobody."]


# ---------------------------------------------------------------- round 4 (two reviewers' findings)

def test_r4_band_cuts():
    t = "而一段短短的递归程序，先试走一步，往下探索，再撤销，就把每一局真实对局都统计了一遍。"      # tic-tac-toe
    e = "And a short recursive program counts every real game by trying a move, exploring, and undoing it."
    assert bi(t, e, 8.1) == [("而一段短短的递归程序", "And a short recursive program"),       # round 3: the halves
                             ("先试走一步，往下探索，再撤销，就把每一局真实对局都统计了一遍",       # crossed
                              "counts every real game by trying a move, exploring, and undoing it.")]
    assert S._mark_cost(t, t.index("往下")) >= 8 and S._mark_cost(t, t.index("就把")) >= 8   # 先……再……，就……
    t = "保护 Alice 的噪声，比起她自己的贡献，也就是 1，算是很大，但比起总体微不足道。"            # 比起……，算是……
    e = ("Alice is protected by noise that is large compared to her own contribution, which is 1, but tiny "
         "compared to the population's.")
    assert bi(t, e, 7.2) == [("保护 Alice 的噪声，比起她自己的贡献，也就是 1，算是很大",
                              "Alice is protected by noise that is large compared to her own contribution, which is 1,"),
                             ("但比起总体微不足道", "but tiny compared to the population's.")]
    t = "X 下的是第 1、3、5 步，所以到了第 5 步，才可能有人凑齐三个棋子。"                         # 到了……，才……
    e = "X plays moves 1, 3 and 5, so the fifth move is the first time anyone can have three marks."
    assert bi(t, e, 6.9) == [("X 下的是第 1、3、5 步", "X plays moves 1, 3 and 5,"),
                             ("所以到了第 5 步，才可能有人凑齐三个棋子",
                              "so the fifth move is the first time anyone can have three marks.")]
    t = "最巧妙的部分来了：一个叫 explore 的函数，explore 就是“探索”的意思。"           # a restated term: no English
    assert bi(t, "Now for the clever part: a function called explore.", 6.1) == [   # (round 3: the English
        ("最巧妙的部分来了", "Now for the clever part:"),                                 # sentence twice)
        ("一个叫 explore 的函数，explore 就是“探索”的意思", "a function called explore.")]
    e = ("One: privacy means changing any one person's row changes the probability of any output by at most a "
         "factor of e^ε.")
    assert [x for _, x in bi("第一，隐私指的是：改动任何一个人的记录，任何输出的概率之比最多是 e^ε。", e, 7.8)] == [
        "One: privacy means changing any one person's row",                               # not "…row changes //
        "changes the probability of any output by at most a factor of e^ε."]              # the probability"


def test_r4_chinese_cues():
    t = "这期视频讲它的三个核心想法：隐私的定义；一个数叫敏感度（sensitivity）；以及一个公式，算噪声加多少才够。"
    assert zh(t, 9.0) == ["这期视频讲它的三个核心想法",                          # a ；-list stays whole (its first
                          "隐私的定义；一个数叫敏感度（sensitivity）； / 以及一个公式，算噪声加多少才够"]   # line 22.05)
    tr = S.tracks([(24.79, 25.54, "猜一猜。", "Take a guess."), (25.86, 26.54, "一百？", "A hundred?"),
                   (26.86, 27.56, "一百万？", "A million?"),
                   (27.88, 30.74, "暂停一下视频，把你猜的数写下来。", "Pause the video and write your guess down.")])
    assert [c[2] for c in tr["zh"]] == ["猜一猜。一百？一百万？", "暂停一下视频，把你猜的数写下来"]   # parallel
    assert [c[2] for c in tr["en"]] == ["Take a guess. A hundred? A million?",                   # questions
                                        "Pause the video and write your guess down."]            # together
    assert [c[2] for c in tr["zh-en"]] == ["猜一猜。一百？一百万？", "暂停一下视频，把你猜的数写下来"]


def test_r4_english_lines():
    cases = {                                                       # the Chinese video's English track
        "The joint density then depends on the L1 distance,": ["The joint density / then depends on the L1 distance,"],
        "Which first move for X leads to the most different games:":                  # tic-tac-toe
            ["Which first move for X / leads to the most different games:"],          # not "depends / on"
        "In 1950, the mathematician and engineer Claude Shannon estimated":            # not "the mathematician /
            ["In 1950, the mathematician and engineer / Claude Shannon estimated"],    # and engineer"
        "the budget makes the limit on questions explicit and measurable.":
            ["the budget makes the limit on questions / explicit and measurable."],
        "Plus a surprising limit on what one published table can achieve,":           # (a wh-clause after "on")
            ["Plus a surprising limit / on what one published table can achieve,"],
    }
    for e, cues in cases.items():
        assert en(e, 4) == cues, e
    w = 44 * 0.55                                                   # the English video's .srt
    for e, ls in {"Laplace noise of scale S of f over epsilon in every coordinate.":            # spoken math
                  ("Laplace noise of scale S of f over epsilon", "in every coordinate."),
                  "add Gaussian noise; and track the budget over thousands of steps.":          # not "track /
                  ("add Gaussian noise; and track the budget", "over thousands of steps."),     # the budget"
                  "Theorem 3 shows that for at least two thirds of these queries,":             # not "at least /
                  ("Theorem 3 shows that for at least two thirds", "of these queries,"),        # two thirds"
                  "Let's call those made-up endings ghost games.": ("Let's call those made-up endings", "ghost games."),
                  "a ratio of two and a ratio of one half count the same.":
                  ("a ratio of two and a ratio of one half", "count the same."),
                  "because going first gives X more chances to win.":                           # a gerund
                  ("because going first", "gives X more chances to win.")}.items():            # subject
        assert S.wrap_en(e, w) == ls, e
    assert S._binomial("the mathematician and engineer Claude", 18)
    assert not S._binomial("to a public voter list and found the governor", 23)
    assert S._gerund_subject("Multiplying the choices gives nine factorial", 24)


def test_r4_english_video_srt():
    from explainer import build

    def srt(t):
        return [c[2].replace("\n", " / ") for c in build.split_cues(0.0, len(t) / 15, t)]
    assert srt(" ".join(SWEENEY[1].split())) == [                         # the whole sentence (round 3 tested
        "Latanya Sweeney showed", "that ZIP code, birth date and sex alone / single out most Americans,",   # only
        "and in 1997 she linked / supposedly anonymous hospital records",                              # its last
        "to a public voter list / and found the governor of Massachusetts."]                           # cue)
    cases = {
        "Four: one private published table cannot answer most simple parity counts unless the database is "
        "exponentially large.": ["Four: one private published table / cannot answer most simple parity counts",
                                 "unless the database is exponentially large."],
        "Explore walks down every branch, one at a time, and counts the leaves it reaches.":     # tic-tac-toe
            ["Explore walks down every branch, / one at a time,", "and counts the leaves it reaches."],
        "The hopeful flip side: with a limited number of questions, modest noise is enough.":
            ["The hopeful flip side:", "with a limited number of questions, / modest noise is enough."],
        "Pause and ponder: if Alice's true answer is yes, how likely is she to say yes?":
            ["Pause and ponder:", "if Alice's true answer is yes, / how likely is she to say yes?"],
        "First: what is the sensitivity of the average of n numbers between zero and one?":    # no greedy
            ["First: what is the sensitivity", "of the average of n numbers / between zero and one?"],   # lines
        "Three: Laplace noise with scale sensitivity over epsilon makes it private, with error that does not grow "
        "with the database.": ["Three: Laplace noise / with scale sensitivity over epsilon",
                               "makes it private, with error / that does not grow with the database."],
        "In 1950, the mathematician and engineer Claude Shannon estimated that chess has at least 10 to the power "
        "of 120 possible games.": ["In 1950, the mathematician and engineer / Claude Shannon estimated",
                                   "that chess has at least / 10 to the power of 120 possible games."],
        "Over the following decades, statisticians and computer scientists refined such tricks, in two flavours: "
        "scramble the data going in, or scramble the answers coming out.":
            ["Over the following decades,", "statisticians and computer scientists / refined such tricks,",
             "in two flavours: scramble the data going in, / or scramble the answers coming out."],
    }
    for t, cues in cases.items():
        assert srt(t) == cues, t


def test_r4_english_video_srt_corpus():
    """Every narration clip of both videos: the English video's .srt cues have at most 2 lines of 44
    characters, laid out by subtitles.wrap_en (no greedy textwrap fallback), and stay up 1 s."""
    from explainer import build, i18n

    for video in ("dwork2006-calibrating-noise", "tictactoe-255168"):
        for english in i18n.narration("zh", REPO / "videos" / video):
            for a, b, text in build.split_cues(0.0, len(english) / 15, english):
                ls = text.split("\n")
                assert len(ls) <= 2 and all(len(x) <= 44 for x in ls), text
                assert tuple(ls) == S.wrap_en(" ".join(ls), 44 * 0.55), text
                assert b - a >= 1.0 - 1e-9, text
