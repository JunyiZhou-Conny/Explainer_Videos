"""Isn't it just an API call? — 项目周记 E1, Swiss scenes.

Narration and exact budgets come from plan.json. The visual vocabulary is the shared swiss
style contract plus this series' conventions (docs/PORTAL_SERIES.md): the product's screens are
redrawn as light cards with verbatim strings, our code is an ink box, the model is a grey box,
red is danger or a blocking rule. Every string copied from the product is listed in SOURCES.md.
All content stays above y = -2.45 so the reserved caption band stays clear.
"""
import json
import os
import re
from functools import lru_cache
from pathlib import Path

from manim import *
from explainer.scene import VoiceScene
from explainer.styles import swiss
from explainer.styles.swiss import (PAPER, INK, RED, GRAY, FAINT,
                                    label, at, left, line, arrow)

swiss.setup_fonts()
config.background_color = PAPER

MONO = "DejaVu Sans Mono"
SCREEN = "#FCFBF8"   # the product's screens: a lighter paper, still inside the background tolerance
TOP, BOTTOM = 1.95, -2.35  # content area between the scene title and the caption band

# PR #36's own commits, Boston time, as hours after Tuesday 2026-10-27 00:00
# (videos/portal-series/weeks/2026-w44.md; git log main..claude/affectionate-franklin-igh419).
PR36_HOURS = [12.367, 12.567, 12.8, 12.95, 13.033, 13.033, 13.05, 14.2, 14.683, 14.517, 14.933,
              14.933, 15.017, 15.133, 18.65, 21.35, 21.417, 21.45, 21.533, 21.717, 21.8, 22.45,
              22.517, 22.583, 22.683, 22.7, 22.767, 22.85, 22.9, 22.983, 23.0, 23.083, 23.133,
              23.2, 23.267, 23.383, 23.433, 23.883, 23.967, 24.117, 25.867, 34.083, 34.1, 35.067,
              35.233, 35.317, 35.5, 35.883, 35.933, 37.683, 37.883, 42.767, 43.117, 43.333,
              43.333, 43.383, 45.067, 45.467, 47.267, 48.75]

# The receipt of the greeting, verbatim from Conny's screenshot of 2026-10-30.
RECEIPT = [
    ("过程", "思考 1.6 秒 → 写 1.5 秒（85 字）→ 检查通过"),
    ("依据", "这次没有写出依据"),
    ("检查", "通过（剂量、诊断、电话和金额的来源、紧急时先说行动）。"),
    ("判断", "只是规则或保险问题 · 给出规则或保险信息"),
    ("模型", "gpt-6-luna · 思考强度 中 · 模型用时 3.1 秒 · $0.0004"),
]
GREETING = "你好呀！我能参考本次对话里你告诉我的信息。"
PARENT_SUMMARY = "孩子目前只是打了招呼，没有提到身体不适或安全问题。家长暂时无需采取行动。"

# The form's thirteen boxes (prototypes/triage/src/llm/schema.ts, OUTPUT_SCHEMA) and the page's
# Chinese names for them (src/features/triage/labels.ts SECTION_ZH and the answer blocks).
FORM = [("acuity", "紧急程度"), ("disposition", "该去哪里"), ("followUp", "追问"),
        ("redFlagsPositive", "危险信号"), ("emergency", "现在就做"), ("options", "去处和步骤"),
        ("watchForZh", "注意"), ("bringZh", "要带的"), ("sayEn", "可以这样说"),
        ("parentSummaryZh", "给家长的摘要"), ("explanationZh", "说明"), ("unknownsZh", "待确认"),
        ("citations", "依据")]
ACUITY = [("emergency_911", "可能危及生命"), ("emergency_er", "紧急"), ("same_day", "今天就要看"),
          ("within_days", "这几天里看"), ("routine", "不急，可以预约"), ("info", "只是规则或保险问题")]

_CJK = "　-〿一-鿿＀-￯"
_TOKENS = re.compile(rf"[{_CJK}]|[^\s{_CJK}]+|\s+")


def mono(s, size=22, color=INK):
    return Text(s, font=MONO, font_size=size, color=color)


@lru_cache(maxsize=None)
def _width(token, size, bold):
    if token.isspace():
        return label("x x", size, bold=bold).width - label("xx", size, bold=bold).width
    return label(token, size, bold=bold).width


def wrap(s, width, size=24, color=INK, bold=False, buff=.1):
    """`s` broken greedily into lines no wider than `width` (CJK by character, Latin by word),
    left-aligned. Line breaks are only visual: the words are the source's, unchanged."""
    lines, cur, w = [], "", 0.0
    for tok in _TOKENS.findall(s):
        tw = _width(tok, size, bold)
        # Summed token widths run short of the set line (fonts differ per token), so near the
        # limit measure the real candidate line.
        over = w + tw > width or (w + tw > .75 * width and label(cur + tok, size, bold=bold).width > width)
        if cur and over and not tok.isspace():
            lines.append(cur.rstrip())
            cur, w = tok, label(tok, size, bold=bold).width
        elif not (tok.isspace() and not cur):
            cur, w = cur + tok, w + tw
    lines.append(cur.rstrip())
    return VGroup(*[label(t, size, color, bold=bold) for t in lines if t]).arrange(
        DOWN, aligned_edge=LEFT, buff=buff)


def place(m, x, y_top):
    """Put `m` with its top-left corner at (x, y_top)."""
    return m.move_to([x + m.width / 2, y_top - m.height / 2, 0])


def frame(x, y, w, h, color=INK, fill=PAPER, stroke=2, dashed=False):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=stroke,
                  fill_color=fill, fill_opacity=1).move_to([x, y, 0])
    return DashedVMobject(r, num_dashes=int((w + h) * 6)) if dashed else r


def screen(x, y, w, h):
    """The product's own screen, redrawn."""
    return RoundedRectangle(corner_radius=.14, width=w, height=h, stroke_color=INK, stroke_width=1.5,
                            fill_color=SCREEN, fill_opacity=1).move_to([x, y, 0])


def node(zh, en, x, y, w=2.6, h=1.0, kind="code"):
    """A box in a diagram: our code (ink), the model (grey), or the product's screen."""
    color = GRAY if kind == "model" else INK
    fill = SCREEN if kind == "screen" else PAPER
    box = (RoundedRectangle(corner_radius=.12, width=w, height=h, stroke_color=color, stroke_width=2,
                            fill_color=fill, fill_opacity=1) if kind == "screen" else
           frame(x, y, w, h, color, fill))
    box.move_to([x, y, 0])
    return VGroup(box, at(zh, x, y + .16, 26, color, w - .3, True), at(en, x, y - .24, 20, GRAY, w - .3))


def chip(text, x, y, color=INK, size=22, pad=.18, fill=PAPER):
    t = label(text, size, color)
    box = Rectangle(width=t.width + 2 * pad, height=t.height + 1.4 * pad, stroke_color=color,
                    stroke_width=2, fill_color=fill, fill_opacity=1)
    return VGroup(box, t).move_to([x, y, 0])


def marker(n, x, y):
    """A red circled number."""
    c = Circle(radius=.21, color=RED, stroke_width=2.5, fill_color=PAPER, fill_opacity=1).move_to([x, y, 0])
    return VGroup(c, at(str(n), x, y, 22, RED, bold=True))


def tag(text, x, y, color=GRAY, size=20):
    """A small provenance tag, e.g. 示意 illustration."""
    return chip(text, x, y, color, size, pad=.1)


def ponder(zh, en, y=-.3, title="想一想 / PAUSE AND PONDER", w=10.2):
    zt = wrap(zh, w - .8, 30, INK)
    et = wrap(en, w - .8, 22, GRAY)
    h = zt.height + et.height + 1.15
    box = frame(0, y, w, h, RED, stroke=3)
    head = at(title, 0, y + h / 2 - .32, 21, RED, bold=True)
    zt.move_to([0, y + h / 2 - .62 - zt.height / 2, 0])
    et.next_to(zt, DOWN, buff=.18)
    return VGroup(box, head, zt, et)


def receipt(x, y_top, w, rows=RECEIPT, size=21, head="思考了 3 秒"):
    """The opened thinking panel: label column + wrapped value column, verbatim strings."""
    title = label(f"{head} ›", size + 3, GRAY)
    place(title, x + .25, y_top - .18)
    out, y = [], y_top - .3 - title.height - .2
    for name, value in rows:
        k = label(name, size, GRAY)
        v = wrap(value, w - 1.35, size, INK, buff=.08)
        place(k, x + .3, y)
        place(v, x + 1.1, y)
        out.append(VGroup(k, v))
        y -= max(k.height, v.height) + .22
    h = y_top - y + .05
    box = RoundedRectangle(corner_radius=.12, width=w, height=h, stroke_color=FAINT, stroke_width=2,
                           fill_color=SCREEN, fill_opacity=1).move_to([x + w / 2, y_top - h / 2, 0])
    return VGroup(box, title, *out)


def flash(m, run_time=.6):
    """Emphasis for boxed groups: a red outline sweep. (Indicate would paint a filled box solid red.)"""
    return Circumscribe(m, color=RED, buff=.05, stroke_width=4, run_time=run_time)


def is_body(m):
    """Scene content, as opposed to the header (rule, series line, title, subtitle)."""
    return m.get_center()[1] < 2.2


class EpisodeScene(VoiceScene):
    pad_after_clip = .18
    total = "09"

    def setup(self):
        super().setup()
        self.camera.background_color = PAPER
        plan = json.loads(Path(os.environ["EPISODE_PLAN"]).read_text())
        self.spec = next(s for s in plan["scenes"] if s["id"].upper() == self.__class__.__name__)

    def header(self):
        """Series line, scene counter, and the scene's titles from script.json."""
        name = self.spec["title_en"]
        ident = self.spec["id"][1:]
        self.add(line(-6.3, 3.26, 6.3, 3.26),
                 left("项目周记 E1 · BUILD LOG", -6.3, 3.46, 20, GRAY),
                 at(f"{ident} / {self.total}", 5.85, 3.46, 20, RED))
        self.play(FadeIn(left(name, -6.3, 2.85, 44, INK, 12.5, True), shift=UP * .10), run_time=.4)
        self.add(left(self.spec["title_zh"], -6.3, 2.34, 24, GRAY))

    def say(self, i):
        return self.voiceover(self.spec["lines"][i]["en"])

    def hold(self, vo, f):
        """Wait until fraction `f` of the current narration line."""
        delay = vo.duration * f - vo.elapsed
        if delay > .04:
            self.wait(delay)

    def cue(self, vo, f, *anims, run_time=.65):
        self.hold(vo, f)
        self.play(*anims, run_time=run_time)

    def pause(self, after, reserve=2.0, most=4.5):
        """Hold the frame for thinking after narration line `after`, paid for out of the scene's slack:
        whatever the remaining lines and `reserve` (for their cues) do not need, up to `most` seconds."""
        speech = sum(a["duration"] + self.pad_after_clip for a in self.spec["audio"][after + 1:])
        slack = self.spec["duration"] - self.renderer.time - speech - reserve
        self.wait(max(.8, min(most, slack)))

    def body(self, keep=()):
        keep_ids = {id(m) for k in keep for m in k.get_family()}
        return [m for m in self.mobjects if id(m) not in keep_ids and is_body(m)]

    def clear_body(self, keep=(), run_time=.4):
        """Fade everything but the header and `keep`."""
        if self.body(keep):
            self.play(*[FadeOut(m) for m in self.body(keep)], run_time=run_time)

    def dim_body(self, opacity=.12, run_time=.5):
        self.play(*[m.animate.set_opacity(opacity) for m in self.body()], run_time=run_time)

    def finish(self):
        remaining = self.spec["duration"] - self.renderer.time
        if remaining > .37:
            self.wait(remaining - .30)
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=.30)
        elif remaining > .015:
            self.wait(remaining)


class S01(EpisodeScene):
    def construct(self):
        self.header()
        scr = screen(-3.75, -.2, 5.1, 4.3)
        bubble_t = label("你好", 26, INK)
        bubble = VGroup(RoundedRectangle(corner_radius=.18, width=bubble_t.width + .6, height=.62,
                                         stroke_width=0, fill_color=FAINT, fill_opacity=1), bubble_t)
        bubble_t.move_to(bubble[0])
        bubble.move_to([-1.45 - bubble.width / 2, 1.42, 0])
        illus = tag("示意 illustration", -4.3, 1.42)
        think = left("思考了 3 秒 ›", -5.7, .78, 22, GRAY)
        answer = place(wrap(GREETING, 4.25, 26), -5.7, .5)
        fold = left("▾ 给家长的摘要", -5.7, -.55, 23, INK, bold=True)
        summary = place(wrap(PARENT_SUMMARY, 4.25, 23, GRAY), -5.7, -.85)
        rec = receipt(-.85, TOP, 7.15, size=20)
        m1, m2, m3 = marker(1, -6.05, .27), marker(2, -6.05, -.55), marker(3, -1.05, TOP - .3)
        with self.say(0) as vo:
            self.cue(vo, .05, FadeIn(scr), run_time=.5)
            vo.wait_until("hello")
            self.play(FadeIn(bubble, shift=LEFT * .1), FadeIn(illus), run_time=.5)
        with self.say(1) as vo:
            vo.wait_until("A greeting")
            self.play(FadeIn(think), FadeIn(answer, shift=UP * .08), FadeIn(m1), run_time=.6)
            vo.wait_until("A summary")
            self.play(FadeIn(fold), FadeIn(summary, shift=UP * .08), FadeIn(m2), run_time=.6)
            vo.wait_until("folded away")
            self.play(Indicate(think, color=RED, scale_factor=1.08), run_time=.6)
            self.play(FadeIn(rec[0]), FadeIn(rec[1]), FadeIn(m3), run_time=.5)
            for i, phrase in enumerate(["thought for", "sources", "a check", "a judgment", "a model"]):
                vo.wait_until(phrase)
                self.play(FadeIn(rec[2 + i], shift=RIGHT * .06), run_time=.35)
        with self.say(2) as vo:
            q = ponder("一次 API 调用只返回一段文字。那是谁决定要有家长摘要？又是谁检查过它？",
                       "An API call returns text. So who decided there would be a parent summary, "
                       "and who checked it?", y=-.35, title="问题 / THE QUESTION")
            vo.wait_until("Nobody asked")
            self.dim_body()
            self.play(FadeIn(q, shift=UP * .1), run_time=.5)
        self.pause(2, reserve=.6, most=3.0)
        self.finish()


class S02(EpisodeScene):
    def construct(self):
        self.header()
        page = node("页面", "THE PAGE", -4.7, .55, 2.6, 1.1, "screen")
        model = node("模型", "OPENAI API", 4.7, .55, 2.6, 1.1, "model")
        go = arrow([-3.3, .85, 0], [3.3, .85, 0], INK)
        back = arrow([3.3, .25, 0], [-3.3, .25, 0], GRAY)
        go_l = at("你的话 · your words", 0, 1.2, 22, INK)
        back_l = at("一段文字 · text back", 0, -.1, 22, GRAY)
        with self.say(0) as vo:
            self.cue(vo, .1, FadeIn(page), FadeIn(model), run_time=.5)
            vo.wait_until("sends your words")
            self.play(GrowArrow(go), FadeIn(go_l), run_time=.6)
            vo.wait_until("sends words back")
            self.play(GrowArrow(back), FadeIn(back_l), run_time=.6)
        server = node("我们的服务器", "OUR SERVER", 0, .55, 2.9, 1.1)
        s_go = VGroup(arrow([-3.35, .85, 0], [-1.5, .85, 0], INK), arrow([1.5, .85, 0], [3.35, .85, 0], INK))
        s_back = VGroup(arrow([3.35, .25, 0], [1.5, .25, 0], GRAY), arrow([-1.5, .25, 0], [-3.35, .25, 0], GRAY))
        key = chip("API KEY · 只在这里", 0, -.55, RED, 21)
        with self.say(1) as vo:
            vo.wait_until("only to our own")
            self.play(FadeOut(VGroup(go, back, go_l, back_l)), FadeIn(server, shift=DOWN * .1), run_time=.6)
            self.play(*[GrowArrow(a) for a in [*s_go, *s_back]], run_time=.6)
            vo.wait_until("API key")
            self.play(FadeIn(key, shift=UP * .1), run_time=.5)
        harness = Rectangle(width=8.0, height=2.35, stroke_color=RED, stroke_width=3).move_to([-2.35, .32, 0])
        h_label = at("HARNESS · 我们的代码", -2.35, 1.75, 26, RED, bold=True)
        jobs = [("组装请求", "build the request"), ("规定格式", "set the form"),
                ("检查", "check it"), ("排成页面", "make the page")]
        cards = VGroup()
        for i, (zh, en) in enumerate(jobs):
            x = -4.65 + i * 3.1
            cards.add(VGroup(frame(x, -1.75, 2.8, 1.0), marker(i + 1, x - 1.12, -1.48),
                             at(zh, x + .15, -1.6, 26, INK, 2.1, True), at(en, x + .15, -1.98, 20, GRAY, 2.3)))
        with self.say(2) as vo:
            vo.wait_until("harness")
            self.play(Create(harness), FadeIn(h_label), run_time=.7)
            for card_, phrase in zip(cards, ["build the request", "set the shape", "check the reply", "back in the page"]):
                vo.wait_until(phrase)
                self.play(FadeIn(card_, shift=UP * .1), run_time=.45)
        self.finish()


class S03(EpisodeScene):
    def construct(self):
        self.header()
        x0, w = -6.2, 5.6
        cx = x0 + w / 2

        def block(zh, en, y, h, color=INK, width=w):
            return VGroup(frame(x0 + width / 2, y, width, h, color),
                          left(zh, x0 + .22, y + (.12 if en else 0), 24, color, width - .4, True),
                          *([left(en, x0 + .22, y - .2, 20, GRAY, width - .4)] if en else []))

        pages = block("BU 官方资料 · 15 份", "≈ 25,000 tokens · 一本小册子", 1.45, .95)
        facts = block("事实卡 · 89 条已核对的事实", "", .62, .44)
        rules = block("规则 · RULES", "", .06, .44)
        form = block("回答表 · THE FORM", "", -.48, .44)
        convo = block("前面的对话", "", -1.12, .42)
        ctx = block("情境 · 时间 · 学校医疗中心 SHS 此刻", "", -1.62, .42)
        hello = block("你好", "", -2.1, .38, RED, 1.5)
        right_x = .5

        with self.say(0) as vo:
            self.cue(vo, .1, FadeIn(hello, shift=UP * .1), run_time=.5)
            note = left("请求里最小的一块 · the smallest part", -4.4, -2.1, 22, GRAY)
            vo.wait_until("smallest part")
            self.play(FadeIn(note), run_time=.4)
        files = VGroup(*[mono(n, 20, INK) for n in ["bu-shs-hours.md", "bu-shs-costs.md",
                                                     "bu-shs-urgent-health-concerns.md",
                                                     "aetna-bu-sbc-2026-27.md", "aetna-bu-certificate-…"]],
                       label("… 共 15 份 · 15 files", 21, GRAY)).arrange(DOWN, aligned_edge=LEFT, buff=.14)
        place(files, right_x, 1.7)
        with self.say(1) as vo:
            self.cue(vo, .15, FadeOut(note), FadeIn(pages, shift=DOWN * .1), run_time=.6)
            vo.wait_until("cleaned into plain text")
            self.play(FadeIn(files, shift=LEFT * .1), run_time=.6)
        quote = place(wrap("原文：Contact Primary Care at 617-353-3575", 5.2, 21, GRAY), .8, .42)
        checked = place(label("核对 2026-10-27 · 30 天有效", 21, GRAY), .8, quote.get_bottom()[1] - .12)
        card = VGroup(frame(3.35, (1.95 + checked.get_bottom()[1] - .15) / 2, 5.6, 1.95 - checked.get_bottom()[1] + .15),
                      place(mono("bu.shs.phone", 21, GRAY), .8, 1.78),
                      place(label("SHS Primary Care 的电话", 24, INK, bold=True), .8, 1.4),
                      place(label("617-353-3575", 34, RED, bold=True), .8, 1.0), quote, checked)
        sent = VGroup(label("发给模型的只有这一行：", 21, RED),
                      wrap("bu.shs.phone：SHS Primary Care 的电话｜值：617-353-3575", 5.6, 20, INK)).arrange(
            DOWN, aligned_edge=LEFT, buff=.1)
        place(sent, .6, card[0].get_bottom()[1] - .2)
        with self.say(2) as vo:
            self.cue(vo, .1, FadeOut(files), FadeIn(facts, shift=DOWN * .1), run_time=.6)
            vo.wait_until("Each card quotes")
            self.play(FadeIn(card, shift=LEFT * .1), run_time=.6)
            vo.wait_until("the model gets just")
            self.play(FadeIn(sent, shift=UP * .06), run_time=.5)
        rule_chips = VGroup(*[chip(t, 0, 0, RED if i == 3 else INK, 22) for i, t in enumerate(
            ["不诊断 · never diagnose", "不给剂量 · never a dose", "紧急：先行动，后谈钱",
             "家长在中国拨 911 打不到波士顿"])]).arrange(DOWN, aligned_edge=LEFT, buff=.2)
        place(rule_chips, right_x, 1.6)
        with self.say(3) as vo:
            self.cue(vo, .08, FadeOut(card), FadeOut(sent), FadeIn(rules, shift=DOWN * .1), run_time=.5)
            for c, phrase in zip(rule_chips, ["Never diagnose", "Never give", "action before", "a parent in China"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=LEFT * .08), run_time=.35)
        brace = BraceBetweenPoints([-.45, 1.92, 0], [-.45, -.7, 0], direction=RIGHT, color=INK)
        same = VGroup(left("instructions", .25, .8, 26, INK, bold=True),
                      left("= 系统提示词 system prompt", .25, .4, 22, GRAY))
        cached = left("每次都一样 → 缓存 · CACHED", .25, 1.2, 24, RED, bold=True)
        prefix = VGroup(label("缓存从请求的第一个字开始比对：", 21, INK),
                        label("不变的必须放在最前面", 21, INK)).arrange(DOWN, aligned_edge=LEFT, buff=.1)
        place(prefix, .25, .9)
        bars = VGroup(
            left("Luna · 每百万 token 的价格", .35, -.25, 21, GRAY),
            VGroup(Rectangle(width=4.5, height=.3, stroke_width=0, fill_color=INK, fill_opacity=1),
                   label("新读 $0.10", 20, PAPER)),
            VGroup(Rectangle(width=.45, height=.3, stroke_width=0, fill_color=RED, fill_opacity=1),
                   label("缓存 $0.01", 20, RED)))
        place(bars[1][0], .35, -.6)
        bars[1][1].move_to(bars[1][0].get_left() + RIGHT * (bars[1][1].width / 2 + .1))
        place(bars[2][0], .35, -1.05)
        bars[2][1].next_to(bars[2][0], RIGHT, buff=.15)
        with self.say(4) as vo:
            self.cue(vo, .05, FadeOut(rule_chips), FadeIn(form, shift=DOWN * .1), run_time=.5)
            vo.wait_until("Together")
            self.play(GrowFromCenter(brace), FadeIn(same), run_time=.6)
        with self.say(5) as vo:
            self.cue(vo, .05, FadeOut(same), FadeIn(cached), run_time=.5)
            vo.wait_until("from its very first word")
            self.play(FadeIn(prefix, shift=UP * .06), run_time=.5)
            vo.wait_until("costs a tenth")
            self.play(FadeIn(bars), run_time=.6)
        ctx_list = VGroup(*[label(t, 22, INK) for t in
                            ["前面的对话（只含学生看到的）", "谁在问 · 保险", "波士顿时间 + 中国时间",
                             "SHS 此刻：开着 / 关着 / 待确认"]]).arrange(DOWN, aligned_edge=LEFT, buff=.16)
        place(ctx_list, .35, -.15)
        with self.say(6) as vo:
            self.cue(vo, .02, FadeOut(bars), FadeOut(prefix), FadeOut(cached), run_time=.3)
            vo.wait_until("the chat so far")
            self.play(FadeIn(convo, shift=DOWN * .1), FadeIn(ctx_list[0]), run_time=.45)
            vo.wait_until("who is asking")
            self.play(FadeIn(ctx, shift=DOWN * .1), FadeIn(ctx_list[1]), run_time=.45)
            vo.wait_until("the time in Boston")
            self.play(FadeIn(ctx_list[2]), run_time=.35)
            vo.wait_until("whether the student clinic")
            self.play(FadeIn(ctx_list[3]), run_time=.35)
            vo.wait_until("finally")
            self.play(flash(hello), run_time=.6)
        price = VGroup(label("gpt-6-luna", 24, GRAY), label("$0.0004", 54, RED, bold=True),
                       label("整本小册子 + 你好", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=.12)
        place(price, 3.2, -1.0)
        with self.say(7) as vo:
            self.cue(vo, .3, FadeIn(price, shift=UP * .1), run_time=.6)
        q = ponder("为什么由我们的代码告诉模型现在几点、诊所开没开门，而不让模型自己算？",
                   "Why does our code tell the model the time, and whether the clinic is open?", y=-.2)
        with self.say(8) as vo:
            self.hold(vo, .05)
            self.dim_body()
            self.play(FadeIn(q, shift=UP * .1), run_time=.5)
        self.pause(8)
        why = VGroup(
            frame(-3.9, -.1, 3.6, 1.6), at("营业时间表", -3.9, .25, 26, INK, 3.2, True),
            at("+ 时区 America/New_York", -3.9, -.3, 20, GRAY, 3.3),
            frame(0, -.1, 2.4, 1.6), at("代码", 0, .2, 28, INK, 2.0, True), at("每次同一套算法", 0, -.3, 20, GRAY, 2.2),
            frame(3.9, -.1, 3.6, 1.6, RED), at("SHS 此刻：", 3.9, .25, 24, INK, 3.2),
            at("开着 / 关着 / 待确认", 3.9, -.3, 24, RED, 3.3, True))
        links = VGroup(arrow([-2.05, -.1, 0], [-1.25, -.1, 0], INK), arrow([1.25, -.1, 0], [2.05, -.1, 0], INK))
        clock = at("模型没有钟 · a model has no clock", 0, -1.6, 26, GRAY)
        with self.say(9) as vo:
            self.clear_body()
            self.play(FadeIn(clock), run_time=.4)
            vo.wait_until("Code reads")
            self.play(FadeIn(why), *[GrowArrow(a) for a in links], run_time=.7)
        self.finish()


class S04(EpisodeScene):
    def construct(self):
        self.header()
        fx, fw = -6.3, 6.3
        sheet = frame(fx + fw / 2, -.2, fw, 4.3)
        title = left("回答表 · THE FORM · 13 格", fx + .2, 1.68, 22, INK, bold=True)
        rows = {}
        for i, (name, zh) in enumerate(FORM):
            y = 1.3 - i * .285
            box = Rectangle(width=fw - .3, height=.25, stroke_color=FAINT, stroke_width=1.5,
                            fill_color=PAPER, fill_opacity=1).move_to([fx + fw / 2, y, 0])
            n = mono(name, 20, INK)
            n.move_to([fx + .3 + n.width / 2, y, 0])
            z = label(zh, 20, GRAY)
            z.move_to([fx + fw - .3 - z.width / 2, y, 0])
            rows[name] = VGroup(box, n, z)
        all_rows = VGroup(*rows.values())
        with self.say(0) as vo:
            vo.wait_until("hand it a form")
            self.play(FadeIn(sheet), FadeIn(title), run_time=.5)
        levels = VGroup(*[VGroup(mono(a, 20, RED if i == 0 else INK), label(z, 20, GRAY)).arrange(RIGHT, buff=.2)
                          for i, (a, z) in enumerate(ACUITY)]).arrange(DOWN, aligned_edge=LEFT, buff=.14)
        lv_head = label("紧急程度：只能六选一", 22, INK, bold=True)
        place(lv_head, .55, 1.75)
        place(levels, .55, 1.3)
        with self.say(1) as vo:
            self.cue(vo, .05, LaggedStart(*[FadeIn(r) for r in all_rows], lag_ratio=.08), run_time=1.6)
            vo.wait_until("fixed choices")
            self.play(flash(rows["acuity"]), FadeIn(lv_head), run_time=.6)
            self.play(LaggedStart(*[FadeIn(l, shift=LEFT * .06) for l in levels], lag_ratio=.15), run_time=1.0)
        stamp = VGroup(frame(3.4, -.9, 5.4, 2.2, RED, stroke=3),
                       at("STRUCTURED OUTPUTS", 3.4, -.05, 26, RED, 5.1, True),
                       at("仍是一次调用、一段文字", 3.4, -.5, 22, INK),
                       at("只是长成了表的样子", 3.4, -.88, 22, INK),
                       at("strict: true → 不能少一格，也不能多一格", 3.4, -1.45, 21, RED, 5.1))
        with self.say(2) as vo:
            vo.wait_until("structured outputs")
            self.play(FadeOut(levels), FadeOut(lv_head), FadeIn(stamp[:2], scale=1.08), run_time=.5)
            vo.wait_until("still one call")
            self.play(FadeIn(stamp[2:4]), run_time=.4)
            vo.wait_until("In strict mode")
            self.play(FadeIn(stamp[4]), run_time=.4)
        rule = VGroup(label("规则原文 · from the rules", 20, GRAY),
                      wrap("parentSummaryZh 一定要写：给在中国的家长看的两三句话（孩子现在怎么了、"
                           "要去哪里、家长能做什么），紧急情况也要写。", 5.5, 22, INK)).arrange(
            DOWN, aligned_edge=LEFT, buff=.14)
        place(rule, .55, 1.75)
        with self.say(3) as vo:
            self.cue(vo, .05, FadeOut(stamp), run_time=.4)
            vo.wait_until("the parent summary")
            ps = rows["parentSummaryZh"]
            self.play(ps[0].animate.set_stroke(RED, 3), ps[1].animate.set_color(RED), run_time=.5)
            vo.wait_until("The rules give it")
            self.play(FadeIn(rule, shift=LEFT * .08), run_time=.6)
        empty = VGroup(frame(2.1, -1.15, 1.6, .5, RED, dashed=True), at("空", 2.1, -1.15, 22, RED),
                       Line([1.3, -1.4, 0], [2.9, -.9, 0], color=RED, stroke_width=4),
                       left("空着交上来：检查不让过", 3.1, -1.15, 22, RED))
        with self.say(4) as vo:
            vo.wait_until("one call fills")
            self.play(flash(all_rows), run_time=.8)
            vo.wait_until("the rules say")
            self.play(flash(rows["parentSummaryZh"]), run_time=.6)
            vo.wait_until("rejects it empty")
            self.play(FadeIn(empty), run_time=.5)
        mini = receipt(.55, -.4, 5.7, rows=[("依据", "← citations"), ("判断", "← acuity · disposition")],
                       head="收据 receipt")
        with self.say(5) as vo:
            self.cue(vo, .05, FadeOut(rule), FadeOut(empty), run_time=.4)
            self.play(FadeIn(mini[:2]), run_time=.4)
            vo.wait_until("Sources is")
            self.play(FadeIn(mini[2]), flash(rows["citations"]), run_time=.6)
            vo.wait_until("Judgment is")
            self.play(FadeIn(mini[3]), flash(VGroup(rows["acuity"], rows["disposition"])), run_time=.6)
        self.finish()


class S05(EpisodeScene):
    def construct(self):
        self.header()
        gate = VGroup(frame(-3.0, .0, .8, 3.2, RED, stroke=3), at("LINT", -3.0, 1.3, 22, RED, bold=True))
        gate_l = at("检查 · 20+ 条规则", -3.0, -1.85, 22, INK)
        doc = VGroup(frame(-5.4, .1, 1.4, 1.7), *[line(-5.85, .6 - .3 * k, -4.95, .6 - .3 * k, FAINT, 3) for k in range(4)],
                     at("表", -5.4, -.95, 22, INK))
        with self.say(0) as vo:
            self.cue(vo, .05, FadeIn(doc), run_time=.4)
            vo.wait_until("a checker")
            self.play(FadeIn(gate), FadeIn(gate_l), run_time=.5)
            self.play(doc.animate.shift(RIGHT * 1.0), run_time=.6)
        examples = [("no_dosing", "「每六小时两片」", "a dose"),
                    ("no_diagnosis", "「你得了……」", "A diagnosis"),
                    ("unsourced_phone / amount", "不在任何事实卡上的电话、金额", "phone number or price"),
                    ("emergency_first", "紧急时先谈钱", "Money before"),
                    ("parent_summary", "空着的家长摘要", "empty parent summary")]
        chips = VGroup()
        for i, (rule, text, _) in enumerate(examples):
            y = 1.6 - i * .78
            t = label(text, 22, INK)
            cross = Line(t.get_left() + LEFT * .05, t.get_right() + RIGHT * .05, color=RED, stroke_width=3)
            g = VGroup(mono(rule, 20, RED), VGroup(t, cross)).arrange(DOWN, aligned_edge=LEFT, buff=.08)
            chips.add(place(g, -1.9, y + .2))
        illus = tag("示意 illustration", 4.9, 1.72)
        with self.say(1) as vo:
            vo.wait_until("More than twenty rules")
            self.play(flash(gate), run_time=.5)
            for c, (_, _, phrase) in zip(chips, examples):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=LEFT * .08), *([FadeIn(illus)] if c is chips[0] else []), run_time=.35)
        self.clear_body()
        try1 = node("第一版", "1st try", -5.0, 1.15, 2.2, .9, "model")
        g1 = node("检查", "LINT", -1.9, 1.15, 2.0, .9)
        g1[0].set_stroke(RED)
        page = node("页面", "THE PAGE", 4.6, 1.15, 2.4, .9, "screen")
        ok1 = VGroup(arrow([-.85, 1.15, 0], [3.35, 1.15, 0], INK), at("通过 pass", 1.2, 1.42, 20, INK))
        note = VGroup(frame(-1.9, -.05, 5.6, .7, RED, dashed=True),
                      at("条子：改掉这几处，重新交一份完整的表", -1.9, -.05, 21, RED, 5.3))
        back = arrow([-1.9, .65, 0], [-1.9, .32, 0], RED)
        try2 = node("第二版", "2nd try", -5.0, -1.3, 2.2, .9, "model")
        g2 = node("检查", "LINT", -1.9, -1.3, 2.0, .9)
        g2[0].set_stroke(RED)
        a12 = VGroup(arrow([-3.85, 1.15, 0], [-2.95, 1.15, 0], INK), arrow([-3.85, -1.3, 0], [-2.95, -1.3, 0], INK),
                     arrow([-4.6, -.05, 0], [-5.0, -.8, 0], RED))
        ok2 = arrow([-.85, -1.15, 0], [3.4, .75, 0], INK)
        fall = VGroup(frame(3.6, -1.55, 5.2, 1.3, INK),
                      at("兜底（我们写好的）", 3.6, -1.12, 22, INK, 4.9, True),
                      at("紧急 → 现在就打 911", 3.6, -1.52, 20, RED),
                      at("不紧急 → 打 SHS 的电话", 3.6, -1.9, 20, INK))
        fail2 = VGroup(arrow([-.85, -1.45, 0], [.95, -1.55, 0], RED), at("✗", .1, -1.2, 24, RED))
        with self.say(2) as vo:
            self.play(FadeIn(try1), FadeIn(g1), GrowArrow(a12[0]), run_time=.5)
            self.play(FadeIn(page), FadeIn(ok1), run_time=.4)
            vo.wait_until("goes back")
            self.play(GrowArrow(back), FadeIn(note), run_time=.5)
            vo.wait_until("One rewrite")
            self.play(GrowArrow(a12[2]), FadeIn(try2), FadeIn(g2), GrowArrow(a12[1]), run_time=.6)
        with self.say(3) as vo:
            self.cue(vo, .05, GrowArrow(ok2), run_time=.4)
            vo.wait_until("still fails")
            self.play(FadeIn(fail2), run_time=.4)
            vo.wait_until("A fallback")
            self.play(FadeIn(fall, shift=UP * .08), run_time=.5)
        lock = VGroup(frame(4.4, 1.0, 3.7, 1.35, RED, stroke=3), at("紧急不收回", 4.4, 1.4, 26, RED, 3.4, True),
                      at("重写只改挑出的毛病", 4.4, 1.0, 20, INK, 3.4),
                      at("真要错，宁可错向 911", 4.4, .62, 20, RED, 3.4))
        with self.say(4) as vo:
            vo.wait_until("says emergency")
            self.play(FadeOut(page), FadeOut(ok1), FadeOut(ok2), run_time=.3)
            vo.wait_until("must stay emergency")
            self.play(FadeIn(lock[:2], scale=1.06), run_time=.5)
            vo.wait_until("A rewrite should")
            self.play(FadeIn(lock[2]), run_time=.4)
            vo.wait_until("rather be wrong")
            self.play(FadeIn(lock[3]), run_time=.4)
        q = ponder("规则里已经告诉过模型「不要诊断」，为什么还要再查一遍？",
                   "The rules already told the model never to diagnose. Why check again?", y=-.2)
        with self.say(5) as vo:
            self.hold(vo, .05)
            self.dim_body()
            self.play(FadeIn(q, shift=UP * .1), run_time=.5)
        self.pause(5)
        paths = VGroup(
            label("指令是请求，不是保证 · an instruction is a request, not a guarantee", 24, INK, 12.4, True),
            label("收据上的「检查」只会是这三种之一：", 22, GRAY),
            label("通过（剂量、诊断、电话和金额的来源、紧急时先说行动）。", 22, INK),
            label("第一次的回答没通过检查，让模型重写了一次，第二次通过。", 22, INK),
            label("换成了兜底文字：……", 22, RED)).arrange(DOWN, aligned_edge=LEFT, buff=.22)
        place(paths, -6.2, 1.6)
        with self.say(6) as vo:
            self.clear_body()
            self.play(FadeIn(paths[0]), run_time=.4)
            vo.wait_until("The check row")
            self.play(FadeIn(paths[1]), run_time=.3)
            for p, phrase in zip(paths[2:], ["passed", "rewritten once", "or replaced"]):
                vo.wait_until(phrase)
                self.play(FadeIn(p, shift=RIGHT * .06), run_time=.35)
        self.finish()


class S06(EpisodeScene):
    def construct(self):
        self.header()
        scr = screen(-3.45, -.2, 5.7, 4.3)
        x = -6.05

        def bars(y, n=2, w=4.6, color=FAINT):
            return VGroup(*[Rectangle(width=w - .9 * k, height=.13, stroke_width=0, fill_color=color,
                                      fill_opacity=1).move_to([x + (w - .9 * k) / 2, y - .24 * k, 0])
                            for k in range(n)])

        urgent = VGroup(frame(-3.45, 1.45, 5.2, .7, RED), left("现在就做", x + .15, 1.45, 24, RED, bold=True))
        parts = [
            VGroup(left("说明", x, .8, 20, GRAY), bars(.55)),
            VGroup(left("1.  去处和步骤", x, .05, 22, INK, bold=True), bars(-.2, 1, 4.2),
                   left("2.  ……", x, -.5, 22, INK)),
            VGroup(left("要带：……", x, -.95, 22, INK)),
            VGroup(left("可以这样说：", x, -1.35, 22, INK), left("“I'd like to …”", x + 1.7, -1.35, 20, GRAY)),
            VGroup(left("▸ 给家长的摘要", x, -1.75, 22, INK, bold=True),
                   chip("复制给家长（学生）", -4.7, -2.12, GRAY, 20, pad=.08)),
        ]
        schematic = tag("示意 schematic", -1.45, -2.12)
        page = VGroup(scr, urgent, *parts, schematic)
        with self.say(0) as vo:
            self.cue(vo, .1, FadeIn(scr), FadeIn(schematic), run_time=.5)
        with self.say(1) as vo:
            vo.wait_until("Urgent steps")
            self.play(FadeIn(urgent, shift=DOWN * .06), run_time=.4)
            for p_, phrase in zip(parts, ["the explanation", "the places to go", "what to bring",
                                          "a sentence to say", "the folded parent summary"]):
                vo.wait_until(phrase)
                self.play(FadeIn(p_, shift=UP * .06), run_time=.35)
        origin = ["页面的秒表", "表 · citations", "检查器 · checker",
                  "表 · acuity + disposition", "服务器 + 价目表"]
        rx = .55
        rows = VGroup()
        for i, ((name, _), src) in enumerate(zip(RECEIPT, origin)):
            y = 1.5 - i * .68
            rows.add(VGroup(frame(rx + .5, y, 1.0, .58), at(name, rx + .5, y, 24, INK, bold=True),
                            Arrow([rx + 1.9, y, 0], [rx + 1.1, y, 0], color=GRAY, stroke_width=2, buff=0,
                                  max_tip_length_to_length_ratio=.2),
                            left(src, rx + 2.05, y, 21, GRAY, 3.7)))
        head = left("收据 · the receipt", rx, 2.0, 22, GRAY)
        with self.say(2) as vo:
            self.cue(vo, .02, FadeIn(head), *[FadeIn(r[:2]) for r in rows], run_time=.5)
            for idx, phrase in [((1, 3), "Sources and judgment"), ((2,), "Check comes"), ((4,), "Model and price")]:
                vo.wait_until(phrase)
                self.play(*[FadeIn(rows[i][2:], shift=LEFT * .06) for i in idx], run_time=.45)
        # The process row, explained with the greeting's real timings (RECEIPT[0]).
        px = -6.15
        think_w, write_w = 1.6 * 1.45, 1.5 * 1.45
        lane = VGroup(
            Rectangle(width=think_w, height=.55, stroke_color=GRAY, stroke_width=2, fill_color=FAINT,
                      fill_opacity=1).move_to([px + think_w / 2, -.25, 0]),
            Rectangle(width=write_w, height=.55, stroke_color=INK, stroke_width=2, fill_color=PAPER,
                      fill_opacity=1).move_to([px + think_w + write_w / 2, -.25, 0]))
        lane_l = VGroup(at("思考 1.6 秒", px + think_w / 2, -.25, 21, INK),
                        at("写 1.5 秒", px + think_w + write_w / 2, -.25, 21, INK))
        first = VGroup(line(px + think_w, -.7, px + think_w, .2, RED, 3),
                       at("第一个字到达", px + think_w, .42, 20, RED))
        hidden = place(wrap("看不见的推理：付钱，但看不到 · hidden reasoning, billed", 5.3, 21, GRAY), px, -.75)
        model = VGroup(label("Luna · 推理模型 reasoning model", 24, INK, bold=True),
                       label("思考强度：低 / 中 / 高 · effort", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=.14)
        place(model, px, 1.45)
        real = place(label("思考是真的；它想了什么 → 下一集", 22, RED, bold=True), px, -1.7)
        with self.say(3) as vo:
            self.cue(vo, .02, FadeOut(page), rows[0][0].animate.set_stroke(RED, 3), run_time=.4)
            vo.wait_until("reasoning model")
            self.play(FadeIn(model[0]), run_time=.4)
            vo.wait_until("hidden steps")
            self.play(FadeIn(lane[0]), FadeIn(lane_l[0]), FadeIn(hidden), run_time=.5)
            vo.wait_until("the effort setting")
            self.play(FadeIn(model[1]), run_time=.4)
            vo.wait_until("The page times")
            self.play(FadeIn(rows[0][2:]), run_time=.4)
            vo.wait_until("until the first word")
            self.play(Create(first[0]), FadeIn(first[1]), run_time=.4)
            vo.wait_until("then writing")
            self.play(FadeIn(lane[1]), FadeIn(lane_l[1]), run_time=.4)
            vo.wait_until("So the thinking is real")
            self.play(FadeIn(real), run_time=.4)
        own = VGroup(*[at("模型写的 →", rx - .75, 1.5 - i * .68, 20, RED) for i in (1, 3)])
        qmark = at("?", -3.2, .2, 96, RED, bold=True)
        with self.say(4) as vo:
            self.cue(vo, .02, FadeOut(VGroup(lane, lane_l, first, hidden, model, real)),
                     rows[0][0].animate.set_stroke(INK, 2), run_time=.4)
            vo.wait_until("Two of the five")
            self.play(FadeIn(own), *[rows[i].animate.set_opacity(.3) for i in (0, 2, 4)], run_time=.5)
            vo.wait_until("Which one")
            self.play(FadeIn(qmark, scale=1.2), run_time=.4)
        self.pause(4, reserve=2.5)
        flag = place(chip("依据：运行时没有检查读它", 0, 0, RED, 22), -6.0, .9)
        ok = VGroup(place(label("判断：检查器读它，确保紧急排最前 ✓", 21, INK), -6.0, .0),
                    place(label("电话、金额：拿事实卡核对 ✓", 21, INK), -6.0, -.5))
        with self.say(5) as vo:
            self.play(FadeOut(qmark), rows[1][0].animate.set_stroke(RED, 3), rows[1][1].animate.set_color(RED),
                      FadeIn(flag, shift=RIGHT * .06), run_time=.5)
            vo.wait_until("reads the judgment")
            self.play(FadeIn(ok[0]), run_time=.4)
            vo.wait_until("phone number and price")
            self.play(FadeIn(ok[1]), run_time=.4)
        self.finish()


class S07(EpisodeScene):
    def construct(self):
        self.header()
        x_of = lambda h: -6.0 + (h - 12) * 12.0 / 37.0
        ay = .35
        axis = line(-6.1, ay, 6.1, ay, INK, 2)
        days = VGroup(*[VGroup(line(x_of(h), ay - .12, x_of(h), ay + .12, GRAY, 2),
                               at(t, max(x_of(h), -5.65), ay - .38, 20, GRAY))
                        for h, t in [(12, "周二 12:00"), (24, "周三 0:00"), (36, "周三 12:00"), (48, "周四 0:00")]])
        ticks = VGroup(*[line(x_of(h), ay, x_of(h), ay + .42, RED if h >= 21.35 else INK, 2) for h in PR36_HOURS])
        count = left("PR #36 · 60 个提交 · 36 小时（波士顿时间）", -6.1, 1.75, 24, INK, bold=True)
        with self.say(0) as vo:
            self.cue(vo, .05, Create(axis), FadeIn(days), FadeIn(count), run_time=.6)
            vo.wait_until("60 commits")
            self.play(LaggedStart(*[Create(t) for t in ticks], lag_ratio=.05), run_time=1.6)
        kb = VGroup(Brace(VGroup(ticks[0], ticks[6]), UP, color=INK, buff=.05),
                    )
        kb_l = at("知识库", x_of(12.7), 1.25, 22, INK)
        conflict = VGroup(frame(-2.9, -1.35, 6.2, 1.45),
                          left("自付上限 out-of-pocket maximum", -5.8, -.88, 21, GRAY),
                          left("$5,550", -5.8, -1.33, 34, RED, bold=True), left("SBC", -4.15, -1.33, 20, GRAY),
                          left("≠", -3.5, -1.33, 34, INK), left("$5,500", -3.0, -1.33, 34, RED, bold=True),
                          left("保险合同", -1.35, -1.33, 20, GRAY),
                          left("7 处冲突：逐条裁定，或标「待确认」", -5.8, -1.78, 20, INK))
        with self.say(1) as vo:
            self.cue(vo, .05, GrowFromCenter(kb), FadeIn(kb_l), run_time=.5)
            vo.wait_until("disagree")
            self.play(FadeIn(conflict, shift=UP * .08), run_time=.5)
        rules = VGroup(Brace(VGroup(ticks[2], ticks[14]), UP, color=GRAY, buff=.5))
        rules_card = VGroup(frame(3.0, -1.35, 6.2, 1.45),
                            left("第一版：规则引擎", .1, -.9, 22, INK, 5.8, True),
                            left("关键词表 → 紧急程度；模型只抽取、只解释", .1, -1.32, 20, GRAY, 5.8),
                            left("评估 6 组：搭好了，比较之前暂停", .1, -1.75, 20, GRAY, 5.8))
        with self.say(2) as vo:
            self.cue(vo, .05, FadeOut(conflict), FadeIn(rules_card, shift=UP * .08), run_time=.5)
            vo.wait_until("We also built")
            self.play(Indicate(ticks[14], color=RED, scale_factor=1.5), run_time=.6)
        turn_x = x_of(21.35)
        turn = VGroup(line(turn_x, ay - .1, turn_x, 1.05, RED, 3), at("21:21 转向", turn_x, 1.28, 24, RED, bold=True))
        turn_card = VGroup(frame(0, -1.35, 12.4, 1.45, RED),
                           left("推理模型带着整本资料自己判断 · 对输出的检查 = 唯一的安全层", -5.95, -.95, 23, INK, 11.9, True),
                           left("关键词表：一边漏判、一边误报，补一处坏一处 · 决策 0004（提议，等医疗审阅）", -5.95, -1.55, 20, GRAY, 11.9))
        with self.say(3) as vo:
            self.cue(vo, .05, FadeOut(kb), FadeOut(kb_l), run_time=.3)
            vo.wait_until("the turn")
            self.play(Create(turn[0]), FadeIn(turn[1]), run_time=.6)
            vo.wait_until("kept missing")
            self.play(FadeOut(rules_card), FadeIn(turn_card[0]), FadeIn(turn_card[2]), run_time=.5)
            vo.wait_until("So you decided")
            self.play(FadeIn(turn_card[1]), run_time=.5)
        box_x = x_of(21.717)
        chat = VGroup(line(box_x, ay + .5, box_x + .9, 1.1, INK, 2), left("21:43 聊天框", box_x + .95, 1.12, 22, INK))
        hard = Brace(VGroup(ticks[20], ticks[59]), UP, color=RED, buff=.5)
        hard_l = at("40 个提交：大多在堵坏句子溜过检查的路", 3.1, 1.7, 22, RED)
        with self.say(4) as vo:
            vo.wait_until("Twenty-two minutes")
            self.play(FadeIn(chat), run_time=.5)
            vo.wait_until("Forty more")
            self.play(GrowFromCenter(hard), FadeOut(turn[1]), FadeIn(hard_l), run_time=.6)
        twist = VGroup(frame(0, -1.35, 12.4, 1.45),
                       left("判断症状 ← 词语规则：放弃 ✗", -5.95, -.95, 24, GRAY, 11.9, True),
                       left("检查模型的句子 ← 词语规则：保留 ✓     → 第四集 E4", -5.95, -1.55, 24, RED, 11.9, True))
        with self.say(5) as vo:
            self.cue(vo, .05, FadeOut(turn_card), FadeIn(twist[0]), run_time=.4)
            vo.wait_until("dropped")
            self.play(FadeIn(twist[1]), run_time=.4)
            vo.wait_until("yet the safety net")
            self.play(FadeIn(twist[2]), run_time=.4)
        self.finish()


class S08(EpisodeScene):
    def construct(self):
        self.header()

        def column(x, title, items, color=INK):
            head = at(title, x, 1.75, 24, color, 5.6, True)
            boxes, ys = VGroup(), [1.0 - i * .78 for i in range(len(items))]
            for (zh, kind), y in zip(items, ys):
                c = GRAY if kind == "model" else (RED if kind == "check" else INK)
                boxes.add(VGroup(frame(x, y, 3.2, .55, c, SCREEN if kind == "screen" else PAPER),
                                 at(zh, x, y, 22, c, 3.0)))
            arrows = VGroup(*[Arrow([x, ys[i] - .29, 0], [x, ys[i + 1] + .29, 0], buff=0, color=GRAY,
                                    stroke_width=2, max_tip_length_to_length_ratio=.3) for i in range(len(ys) - 1)])
            return head, boxes, arrows

        lh, lb, la = column(-3.4, "通用聊天应用 · general chat app",
                            [("你的话", "screen"), ("模型", "model"), ("一段文字", "screen")], GRAY)
        l_note = at("系统提示词 + 模型的训练", -3.4, -1.35, 21, GRAY)
        rh, rb, ra = column(3.0, "我们 · ours",
                            [("你的话", "screen"), ("模型", "model"), ("回答表（13 格）", "code"),
                             ("检查", "check"), ("页面 + 收据", "screen")])
        facts = VGroup(frame(5.55, .22, 1.6, .55), at("事实卡", 5.55, .22, 20, INK))
        f_arrow = Arrow([4.75, .22, 0], [4.65, .22, 0], buff=0, color=GRAY, stroke_width=2)
        look = chip("外观：有意照着 Claude App 做 → 第三集", -3.4, -.4, GRAY, 21)
        sp = at("系统提示词 →", .55, .22, 20, GRAY)
        with self.say(0) as vo:
            self.cue(vo, .05, FadeIn(rb[0]), FadeIn(rb[1]), FadeIn(rb[4]), FadeIn(ra[0]), run_time=.5)
            vo.wait_until("borrowed")
            self.play(FadeIn(look), run_time=.4)
            vo.wait_until("Inside")
            self.play(FadeIn(rh), FadeIn(rb[2]), FadeIn(rb[3]), *[FadeIn(a) for a in ra[1:]], run_time=.6)
        with self.say(1) as vo:
            vo.wait_until("A general chat app")
            self.play(FadeOut(look), FadeIn(lh), FadeIn(lb), FadeIn(la), run_time=.6)
            vo.wait_until("guided by")
            self.play(FadeIn(l_note), run_time=.4)
            vo.wait_until("Ours has")
            self.play(flash(rb[1]), FadeIn(sp), run_time=.5)
            vo.wait_until("a form we designed")
            self.play(flash(rb[2]), run_time=.5)
            vo.wait_until("prices only")
            self.play(FadeIn(facts), FadeIn(f_arrow), run_time=.4)
            vo.wait_until("our own rules")
            self.play(flash(rb[3]), run_time=.5)
        self.clear_body()
        base = VGroup(*[VGroup(frame(-3.0, 1.6 - i * .3, 5.6, .26, FAINT),
                               left(n, -5.7, 1.6 - i * .3, 20, GRAY)) for i, (n, _) in enumerate(FORM[:8])])
        more = left("…… 共 13 格", -5.7, -.82, 20, GRAY)
        new = [("给室友的话 · a note for a roommate", "A note"),
               ("问医生的问题 · questions for the doctor", "Questions to ask")]
        new_rows = VGroup(*[VGroup(frame(-3.0, -1.3 - i * .46, 5.6, .38, RED, dashed=True),
                                   left("+ " + t, -5.7, -1.3 - i * .46, 21, RED, 5.3)) for i, (t, _) in enumerate(new)])
        with self.say(2) as vo:
            self.cue(vo, .02, FadeIn(base), FadeIn(more), run_time=.5)
            vo.wait_until("a new box")
            self.play(Indicate(more, color=RED), run_time=.4)
            for r, (_, phrase) in zip(new_rows, new):
                vo.wait_until(phrase)
                self.play(FadeIn(r, shift=DOWN * .06), run_time=.4)
        cols = ["表 + 说明", "检查 checker", "页面 page"]
        heads = VGroup(*[at(c, 1.6 + i * 1.75, -.85, 21, INK, 1.7, True) for i, c in enumerate(cols)])
        ticks = VGroup(*[at("✓", 1.6 + i * 1.75, -1.3 - r * .46, 26, RED, bold=True) for r in range(2) for i in range(3)])
        with self.say(3) as vo:
            vo.wait_until("three things")
            self.play(FadeIn(heads), run_time=.4)
            for i, phrase in enumerate(["a line on the form", "a rule in the checker", "a place on the page"]):
                vo.wait_until(phrase)
                self.play(*[FadeIn(ticks[r * 3 + i], scale=1.2) for r in range(2)], run_time=.35)
        self.finish()


class S09(EpisodeScene):
    def construct(self):
        self.header()
        items = [("组装请求", "不变的放前面 → 缓存"), ("一张表", "结构化输出 · 13 格"),
                 ("检查", "20+ 条规则 · 一次重写 · 兜底"), ("页面 + 收据", "每一行写明从哪来")]
        cards = VGroup()
        for i, (t, s) in enumerate(items):
            x = -3.15 + (i % 2) * 6.3
            y = 1.25 - (i // 2) * 1.35
            cards.add(VGroup(frame(x, y, 6.0, 1.1, RED if i == 2 else INK), marker(i + 1, x - 2.65, y + .22),
                             left(t, x - 2.3, y + .2, 28, INK, 4.9, True), left(s, x - 2.3, y - .25, 21, GRAY, 5.1)))
        with self.say(0) as vo:
            self.cue(vo, .2, FadeIn(cards[0], shift=UP * .08), run_time=.4)
        with self.say(1) as vo:
            for c, phrase in zip(cards[1:], ["Hand over a form", "Check every line", "Then lay"]):
                vo.wait_until(phrase)
                self.play(FadeIn(c, shift=UP * .08), run_time=.4)
        qs = VGroup(label("考考自己 · test yourself", 22, RED, bold=True),
                    label("1. 请求里哪部分会被缓存？为什么位置很重要？", 22, INK),
                    label("2. 为什么重写不准收回「紧急」？", 22, INK),
                    label("3. 加一段「给室友的话」，要改哪几处？", 22, INK)).arrange(DOWN, aligned_edge=LEFT, buff=.14)
        place(qs, -6.2, -.85)
        with self.say(2) as vo:
            self.cue(vo, .02, cards.animate.shift(UP * .25).set_opacity(.35), run_time=.4)
            self.play(FadeIn(qs[0]), run_time=.3)
            for q, phrase in zip(qs[1:], ["Which part", "Why may", "And what"]):
                vo.wait_until(phrase)
                self.play(FadeIn(q, shift=RIGHT * .06), run_time=.35)
        nxt = VGroup(frame(3.7, -1.45, 4.9, 1.3, RED, stroke=3), at("下一集 · NEXT", 3.7, -1.05, 21, RED, bold=True),
                     at("「思考了 3 秒」到底是什么", 3.7, -1.5, 25, INK, 4.6, True),
                     at("receipt vs. thoughts", 3.7, -1.88, 20, GRAY))
        with self.say(3) as vo:
            self.cue(vo, .05, FadeIn(nxt, shift=LEFT * .1), run_time=.5)
        self.finish()
