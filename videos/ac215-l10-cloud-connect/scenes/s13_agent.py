"""S13 · The agent, and a model that isn't yours (AC215 L10) — tracker E4 → E5, no lecture_ref.

Beats (script.md, ## S13; one voiceover block each):
0. TRACKER E4. The /agent page (ChatWireframe, `illustration`): collection picker, README line 232's
   example question typed into the bubble (note 'README.md · line 232'). It shrinks away into the
   three-step strip (top left; each row `browser → <call>`, PINK): ① `GET :9000/rag/agent_call` with
   CODE(rag.py 158–163, the window of 150–171 that holds the choice and the swap), lines 160–163
   YELLOW and a 'search text' chip turning into 256 equal BLUE bars; the choice chips
   `get_book_by_author` / `get_book_by_search_content` (top right) flash on their words.
   ② `browser → Chroma :8000` with CODE(DataService.js 45–47) at 20 pt, line 47's `"where": {
   "author": author }` YELLOW, `get_book_by_author` ringed. ③ `POST :9000/rag/llm-agent-response`
   with CODE(rag.py 190–198, the window of 190–203 that holds the loop and the tools) at 20 pt, a
   YELLOW loop arrow on its left, chip `MAX_AGENT_STEPS = 5` (rag.py · line 83), the PURPLE tool
   chip `‹instructor›_fun_fact_tool` ('server-side', README.md · line 238, name masked by unname()).
   GOLD `cost_tag("1 embedding + 3 to 7 generation calls")`, then `▶ your turn` with the picker.
1. The answer frame (`illustration`): GREY skeleton bars, the last paragraph the box
   "‹instructor›'s fun fact" (README.md · line 239); CODE(ChatComponent.jsx 22–28) at 20 pt, line 24
   YELLOW. No answer text.
2. TRACKER E5. CODE(rag.py 18–22, the window of 14–27 that holds the endpoint), line 22's
   `"projects/129349313346/…` RED with the GREY label "the instructor's endpoint"; README card
   (line 247); it gives way to CODE(llm-finetuning · gemini-finetuner/cli.py 89–96), line 92 GREEN.
   A YELLOW chip 'your endpoint' lifts off line 92 and rides a YELLOW edit arrow into line 22;
   `▶ your turn`. The card 'rag.py is under api/ → reloads' / 'agent_tools.py is not → control C,
   uvicorn_server again' row by row; `api/` in the panel header flashes.
3. README card (line 249) and the /finetunechat page (`illustration`) with the same question.
   V2 reprise: the grid returns as S08 left it (tokens in place); a small browser at the bottom
   left re-fires S08's parked 'tuned model' request: path `projects/129349313346/…`, column 3
   pulses, the empty (SA, project 129349313346) cell pulses, the arrow lands: RED 403; GREY caption
   'nothing documents this error's exact text' (no error panel). CODE(rag.py 110–113) at 20 pt,
   line 111 wrapped once at a space (note 'line 111 · wrapped to fit'), `location="us"` YELLOW.
   GOLD `cost_tag("tuned-model calls bill the endpoint's project")`, then the README card 249 with
   `▶ your turn` and a RED '403' chip on "expect the 403". Fade to an empty frame.
"""

import re

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, INK, PASS, ROUTE, NARRATION, SAY_COUNT, TOOL, TURN, CAPTION,
                    ChatWireframe, EmbeddingBars, IamGridRig, card, chip, code, code_panel, code_span,
                    cost_tag, err_chip, excerpt, flash_tag, grey_chip, illustration_tag, label, line_bar,
                    mono, MONO, note, readme, readme_card, ring, shown_path, step_badge, tool_chip, track,
                    tracker, your_turn, browser_glyph, each)
from explainer import style as S

SAY = NARRATION["S13"]
RAG = "cheese-app-v0/api-service/api/routers/rag.py"
DS = "cheese-app-v0/frontend-ai-chatbot/src/services/DataService.js"
CC = "cheese-app-v0/frontend-ai-chatbot/src/components/chat/ChatComponent.jsx"
CLI = "llm-finetuning/gemini-finetuner/cli.py"
PICKER = "char-split-collection ▾"
TUNED = "129349313346"                       # quoted: rag.py:22's endpoint project (RED story beat)


# ------------------------------------------------------------------ quoted facts (asserted)
def readme_question() -> str:
    """README line 232's example question, as written (name masked by readme())."""
    s = readme(232)
    q = s.split('(e.g. "', 1)[1].split('")', 1)[0]
    assert q.startswith("Describe where cheese making"), q
    return q


QUESTION_AGENT = readme_question()
FUN_TOOL = re.search(r"`(\S+_fun_fact_tool)`", readme(238)).group(1)       # masked by unname()
assert FUN_TOOL in excerpt(RAG, 174, 174), FUN_TOOL
MAX_STEPS = excerpt(RAG, 83, 83).strip()
assert MAX_STEPS == "MAX_AGENT_STEPS = 5", MAX_STEPS
CHOICES = ("get_book_by_author", "get_book_by_search_content")
for _c in CHOICES:
    assert f"`{_c}`" in readme(236), _c
CALL_1 = "GET :9000/rag/agent_call"           # rag.py:235 @router.get("/agent_call") on the API's :9000
CALL_3 = "POST :9000/rag/llm-agent-response"  # rag.py:243 @router.post("/llm-agent-response")
assert '@router.get("/agent_call")' in excerpt(RAG, 235, 235)
assert '@router.post("/llm-agent-response")' in excerpt(RAG, 243, 243)


# ------------------------------------------------------------------ local helpers
def clear_but(scene, *keep, anims=(), run_time: float = 0.6):
    """Plays: everything on screen fades except the families of `keep` (the tracker may have been
    split into parts by track()), then `keep` is re-added whole. Same as S09's / S11's."""
    ids = {id(f) for k in keep for f in k.get_family()}
    gone = [x for x in scene.mobjects if not any(id(f) in ids for f in x.get_family())]
    scene.play(FadeOut(Group(*gone)), *anims, run_time=run_time)
    scene.remove(*gone)
    scene.add(*keep)


def drop(scene, *mobs, anims=(), run_time: float = 0.4):
    """Plays: mobjects fade and leave the scene."""
    scene.play(FadeOut(VGroup(*mobs)), *anims, run_time=run_time)
    scene.remove(*mobs)


def place_top(p, y: float, x: float | None = None):
    """Put a panel's top edge at y (its centre at x, when given)."""
    p.shift(UP * (y - p.get_top()[1]))
    if x is not None:
        p.shift(RIGHT * (x - p.get_center()[0]))
    return p


def step_row(k: int, target: VGroup) -> VGroup:
    """One row of the three-step strip: badge k, 'browser', a PINK arrow, the call. .badge .arrow .target"""
    b = step_badge(k, ROUTE)
    who = label("browser", 20, INK)
    ar = Arrow(ORIGIN, RIGHT * 0.45, buff=0, color=ROUTE, stroke_width=4, tip_length=0.15,
               max_tip_length_to_length_ratio=0.5)
    row = VGroup(b, who, ar, target).arrange(RIGHT, buff=0.12)
    row.badge, row.arrow, row.target = b, ar, target
    return row


def strip_rows() -> VGroup:
    """The three calls of the agent, top left under the tracker."""
    t2 = VGroup(label("Chroma", 20, ROUTE), mono(":8000", 20, ROUTE)).arrange(RIGHT, buff=0.12)
    rows = VGroup(step_row(1, mono(CALL_1, 20, ROUTE)), step_row(2, t2), step_row(3, mono(CALL_3, 20, ROUTE)))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    return rows.move_to([-6.45, 2.72, 0], aligned_edge=UL)


def dimmed(m, darkness: float = 0.7):
    return m.copy().fade(darkness)


def readme_plain(n: int) -> str:
    """README line n without Markdown link targets and backticks (the words a reader sees)."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", readme(n))
    return s.replace("`", "")


def rich_rows(rows, size: float = 22) -> VGroup:
    """Rows of (text, 'mono'|'label') pieces, label font baseline-aligned with mono."""
    out_ = VGroup()
    for parts in rows:
        r = VGroup(*[mono(s, size - 2, INK) if k == "mono" else label(s, size, INK) for s, k in parts])
        r.arrange(RIGHT, buff=0.18)
        out_.add(r)
    return out_.arrange(DOWN, aligned_edge=LEFT, buff=0.16)


def card_247() -> VGroup:
    rows = [[("Update", "label"), ("FINE_TUNE_GENERATIVE_MODEL", "mono"), ("in", "label"),
             ("api-service/api/routers/rag.py", "mono")],
            [("to your own fine-tuned model endpoint (from the", "label"), ("llm-finetuning", "label"),
             ("tutorial).", "label")]]
    joined = " ".join(s for r in rows for s, _ in r)
    assert joined == readme_plain(247), (joined, readme_plain(247))
    return readme_card(247, rich_rows(rows))


def card_249() -> VGroup:
    url = "http://localhost:3200/finetunechat"
    assert readme_plain(249) == f"Go to {url}.", readme_plain(249)
    body = VGroup(label("Go to", 22, INK), mono(url + ".", 20, INK)).arrange(RIGHT, buff=0.14)
    return readme_card(249, body)


def rag_ft_client() -> VGroup:
    """rag.py lines 110–113 at 20 pt; line 111 (80 characters) is wrapped once at a space before
    `location=`: whitespace only, the rows join back to the line exactly (as S07's line 26)."""
    l110, l111, l112, l113 = excerpt(RAG, 110, 113).split("\n")
    a, b = l111.split(" location=", 1)
    w1, w2 = a, "        location=" + b
    assert w1 + " " + w2.strip() == l111
    p = code_panel("\n".join([l110, w1, w2, l112, l113]), shown_path(RAG), 110, "python", font_size=20)
    old = p.header[1]
    p.header.submobjects[1] = label("· lines 110–113", CAPTION, S.GREY).move_to(old, aligned_edge=LEFT)
    return p


def req_chip_at(x: float, y: float, text: str) -> VGroup:
    """A PINK request chip (as S08's) centred at (x, y)."""
    return chip(text, ROUTE, size=20, font=MONO, fill_opacity=0.15).move_to([x, y, 0])


def path_text(middle: str) -> Text:
    """A request's resource path 'projects/<middle>/…' (PINK frame, the project WHITE), as S08's."""
    pre = "projects/"
    t = mono(pre + middle + "/…", 20, ROUTE)
    assert len(t) == len(pre) + len(middle) + 2, len(t)
    t[len(pre):len(pre) + len(middle)].set_color(INK)
    t.middle = t[len(pre):len(pre) + len(middle)]
    return t


class AgentAndTuned(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S13"] == 4, len(SAY)

        # ========================================================== 0. the agent: three calls, one twist
        tr = tracker("E", 4)
        cw = ChatWireframe(url="localhost:3200/agent", question=QUESTION_AGENT, picker=PICKER, win_w=10.4,
                           win_h=5.6).move_to([0, -0.55, 0])
        ill0 = illustration_tag().next_to(cw.window, UP, buff=0.12).align_to(cw.window, RIGHT)
        src0 = note("README.md · line 232").next_to(cw.window, UP, buff=0.2).align_to(cw.window, LEFT)

        rows = strip_rows()
        shown = [dimmed(r) for r in rows]

        p1 = place_top(code(RAG, 158, 163, dedent=True), 0.95, 0.0)
        _top, _bot = line_bar(p1.code, 2, TURN), line_bar(p1.code, 5, TURN)
        bars1 = Rectangle(width=_top.width, height=_top.get_top()[1] - _bot.get_bottom()[1], stroke_width=0) \
            .set_fill(TURN, 0.16).move_to([_top.get_center()[0], (_top.get_top()[1] + _bot.get_bottom()[1]) / 2, 0])
        emb_fn = code_span(p1.code, 3, "generate_query_embedding")
        q_chip = grey_chip("search text").move_to([-2.6, -2.75, 0])
        emb = EmbeddingBars(256, bars_w=3.2, bar_h=0.5).move_to([1.6, -2.75, 0])
        emb_ar = Arrow(q_chip.get_right(), emb.get_left(), buff=0.2, color=CLOUD, stroke_width=3,
                       tip_length=0.16, max_tip_length_to_length_ratio=0.3)

        pick_n = note("Gemini picks one")
        ch_a, ch_b = tool_chip(CHOICES[0]), tool_chip(CHOICES[1])
        choice = VGroup(pick_n, ch_a, ch_b).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        choice.move_to([6.55, 2.72, 0], aligned_edge=UR)

        p2 = place_top(code(DS, 45, 47, dedent=True, font_size=20, cuts={45: "async function ("}), 0.95, 0.0)
        bar2 = line_bar(p2.code, 2, TURN)
        where = code_span(p2.code, 2, '"where": { "author": author }')
        ring_a = ring(ch_a, TURN, buff=0.07)

        p3 = place_top(code(RAG, 190, 198, dedent=True, font_size=20,
                            cuts={191: "disable tools", 198: "cheese_expert_tool,"}), 0.95, 0.5)
        bar3 = line_bar(p3.code, 0, TURN)
        l0, l7 = p3.code.code_lines[0], p3.code.code_lines[7]
        x_l = p3.code.background.get_left()[0] - 0.12
        loop = CurvedArrow([x_l, l7.get_center()[1], 0], [x_l, l0.get_center()[1], 0], angle=-PI * 0.75,
                           color=TURN, stroke_width=4, tip_length=0.18)
        max_c = VGroup(grey_chip(MAX_STEPS, mono_font=True), note("rag.py · line 83")).arrange(RIGHT, buff=0.2)
        fun_c = VGroup(tool_chip(FUN_TOOL), note("server-side")).arrange(RIGHT, buff=0.2)
        fun_src = note("README.md · line 238")
        side3 = VGroup(max_c, fun_c, fun_src).arrange(DOWN, aligned_edge=RIGHT, buff=0.14)
        side3.move_to([6.55, 2.72, 0], aligned_edge=UR)
        tools98 = code_span(p3.code, 8, "tools=")

        gold = cost_tag("1 embedding + 3 to 7 generation calls").move_to([0, -0.2, 0])
        yt0 = your_turn()
        pick0 = chip(PICKER, S.GREY, size=20, font=MONO)
        turn0 = VGroup(yt0, pick0).arrange(RIGHT, buff=0.35).next_to(gold, DOWN, buff=0.45)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(cw.shell, shift=UP * 0.2), FadeIn(ill0),
                      run_time=0.9)
            self.play(cw.type_question(1.4), FadeIn(src0, shift=RIGHT * 0.15))
            self.play(Indicate(cw.picker.text, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("the chat's three calls")
            page = VGroup(cw, ill0, src0)
            self.play(FadeOut(page, scale=0.4, target_position=rows[0].badge.get_center()),
                      LaggedStart(*[FadeIn(s, shift=RIGHT * 0.2) for s in shown], lag_ratio=0.3), run_time=1.0)
            self.remove(page)
            vo.wait_until("with one twist")
            self.play(each([s.badge for s in shown], TURN, scale=1.25, lag=0.2), run_time=0.9)

            # ① GET :9000/rag/agent_call: Gemini picks a tool, the API swaps the text for an embedding
            vo.wait_until("Gemini first picks")
            self.play(Transform(shown[0], rows[0].copy()), FadeIn(p1, shift=UP * 0.2), FadeIn(pick_n),
                      run_time=0.7)
            self.play(Create(shown[0].arrow), run_time=0.4)
            vo.wait_until("search by author")
            self.play(FadeIn(ch_a, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("or search by content")
            self.play(FadeIn(ch_b, shift=LEFT * 0.2), run_time=0.5)
            vo.wait_until("The API turns the search text")
            self.play(FadeIn(bars1), Indicate(ch_b.text, color=TURN, scale_factor=1.08), run_time=0.6)
            self.play(FadeIn(q_chip, shift=UP * 0.15), run_time=0.4)
            self.play(GrowArrow(emb_ar), each(emb_fn, CLOUD, scale=1.15, lag=0.02), run_time=0.7)
            self.play(emb.grow(1.0))

            # ② browser → Chroma :8000, filtered by author when that tool won
            vo.wait_until("Then your browser queries")
            self.play(FadeOut(VGroup(p1, bars1, q_chip, emb_ar, emb)), Transform(shown[0], dimmed(rows[0])),
                      Transform(shown[1], rows[1].copy()), run_time=0.6)
            self.remove(p1, bars1, q_chip, emb_ar, emb)
            self.play(FadeIn(p2, shift=UP * 0.2), Create(shown[1].arrow), run_time=0.6)
            vo.wait_until("filtered by author")
            self.play(FadeIn(bar2), Create(ring_a), run_time=0.5)
            self.play(each(where, TURN, scale=1.12, lag=0.02), Indicate(ch_a.text, color=TURN, scale_factor=1.08),
                      run_time=0.9)

            # ③ POST :9000/rag/llm-agent-response: up to five rounds, a server-side fun fact tool
            vo.wait_until("The API loops up to five times")
            self.play(FadeOut(VGroup(p2, bar2, ring_a, choice)), Transform(shown[1], dimmed(rows[1])),
                      Transform(shown[2], rows[2].copy()), run_time=0.6)
            self.remove(p2, bar2, ring_a, choice)
            self.play(FadeIn(p3, shift=UP * 0.2), Create(shown[2].arrow), FadeIn(max_c, shift=LEFT * 0.2),
                      run_time=0.7)
            self.play(FadeIn(bar3), Create(loop), run_time=0.8)
            self.play(Indicate(max_c[0].text, color=TURN, scale_factor=1.1), run_time=0.6)
            vo.wait_until("and Gemini may call a fun fact tool")
            self.play(FadeIn(VGroup(fun_c, fun_src), shift=LEFT * 0.2), each(tools98, TOOL, scale=1.15, lag=0.03),
                      run_time=0.7)
            self.play(Indicate(fun_c[0].text, color=TOOL, scale_factor=1.08), run_time=0.6)

            # GOLD, then your turn
            vo.wait_until("A gold tag")
            self.play(FadeOut(VGroup(p3, bar3, loop, side3)), FadeIn(gold, shift=UP * 0.2), run_time=0.6)
            self.remove(p3, bar3, loop, side3)
            vo.wait_until("one agent question costs")
            flash_tag(self, gold, COST)
            vo.wait_until("three to seven generation calls")
            self.play(Indicate(gold.text, color=COST, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Pause, pick a collection")
            self.play(FadeIn(turn0, shift=UP * 0.15), run_time=0.5)
            flash_tag(self, yt0, TURN)

        # ========================================================== 1. what to look for: the fun fact
        cw2 = ChatWireframe(url="localhost:3200/agent", fun_fact=True, win_w=11.0)
        cw2.shift(np.array([0, 1.7, 0]) - cw2.answer.get_center())
        ans = VGroup(cw2.answer)
        ill1 = illustration_tag().next_to(cw2.answer, UP, buff=0.12).align_to(cw2.answer, RIGHT)
        src1 = note("README.md · line 239").next_to(cw2.answer, UP, buff=0.12).align_to(cw2.answer, LEFT)
        p4 = place_top(code(CC, 22, 28, dedent=True, font_size=20, cuts={25: "rounded-xl border"}), 0.55, 0.0)
        bar4 = line_bar(p4.code, 2, TURN)

        with self.voiceover(SAY[1]) as vo:
            clear_but(self, tr, anims=[FadeIn(ans), FadeIn(ill1)], run_time=0.5)
            self.play(cw2.grow_bars(0.9), FadeIn(p4, shift=UP * 0.2))
            vo.wait_until("highlighted fun fact paragraph")
            self.play(Indicate(cw2.fun[1], color=TURN, scale_factor=1.12), FadeIn(src1), FadeIn(bar4), run_time=0.7)
            self.play(Indicate(code_span(p4.code, 2, "startsWith"), color=TURN, scale_factor=1.1), run_time=0.7)

        # ========================================================== 2. step 5: your own tuned endpoint
        p5 = code(RAG, 18, 22, font_size=20, cuts={19: '"projects/', 21: "projects/", 22: "projects/129349313346/"})
        p5.move_to([-6.4, 2.75, 0], aligned_edge=UL)
        red = code_span(p5.code, 4, '"projects/129349313346/')
        ell = code_span(p5.code, 4, "…")
        bar5 = line_bar(p5.code, 4, ERR, opacity=0.18)
        lab5 = note("the instructor's endpoint").next_to(p5.code, RIGHT, buff=0.35)
        lab5.match_y(p5.code.code_lines[4])
        c247 = card_247().move_to([0, -2.1, 0])
        cli = code(CLI, 89, 96, font_size=20)
        place_top(cli, -0.05, 0.0)
        bar92 = line_bar(cli.code, 3, PASS, opacity=0.2)
        ep92 = code_span(cli.code, 3, "tuning_job.tuned_model.endpoint")
        l8 = note("your lecture 8 run printed it").next_to(cli.header, RIGHT, buff=0.4)
        yours = chip("your endpoint", TURN, size=20, font=MONO, fill_opacity=0.2).move_to(ep92)
        dest = red.get_left() + RIGHT * 1.35
        yt2 = your_turn()
        reload_rows = [VGroup(mono("rag.py", 20, INK), label("is under", 22, INK), mono("api/", 20, INK),
                              label("→ reloads", 22, PASS)),
                       VGroup(mono("agent_tools.py", 20, INK), label("is not → control C,", 22, INK),
                              mono("uvicorn_server", 20, INK), label("again", 22, INK))]
        for r in reload_rows:
            r.arrange(RIGHT, buff=0.14)
            for m in r[1:]:
                m.align_to(r[0], DOWN)
        rcard = card(reload_rows, size=22)
        rcard.move_to([0, -2.2, 0])
        hdr = p5.header[0]
        k_api = hdr.original_text.index("/api/") + 1
        api_glyphs = hdr[k_api:k_api + 4]

        with self.voiceover(SAY[2]) as vo:
            clear_but(self, tr, anims=[track(tr, 5)], run_time=0.6)
            self.play(FadeIn(p5, shift=UP * 0.2), run_time=0.6)
            self.play(FadeIn(bar5), red.animate.set_color(ERR), ell.animate.set_color(ERR),
                      FadeIn(lab5, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("The README says to swap")
            self.play(FadeIn(c247, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(c247.body[0][1], color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("the one your fine-tuning run printed")
            self.play(FadeOut(c247), FadeIn(cli, shift=UP * 0.2), run_time=0.6)
            self.remove(c247)
            self.play(FadeIn(bar92), ep92.animate.set_color(PASS), FadeIn(l8), run_time=0.6)
            vo.wait_until("Pause and paste yours")
            self.play(FadeIn(yours, scale=1.2), run_time=0.4)
            self.play(FadeOut(VGroup(cli, bar92, l8)), run_time=0.4)
            self.remove(cli, bar92, l8)
            path = ArcBetweenPoints(yours.get_center(), dest, angle=-0.6)
            edit = Arrow(yours.get_top(), dest + DOWN * 0.22, buff=0.05, color=TURN, stroke_width=4, path_arc=-0.6,
                         tip_length=0.18, max_tip_length_to_length_ratio=0.2)
            self.play(Create(edit), run_time=0.5)
            self.play(MoveAlongPath(yours, path), FadeOut(VGroup(red, ell, bar5, lab5)), FadeOut(edit),
                      run_time=1.0)
            p5.code.code_lines[4].remove(*red, *ell)
            self.remove(red, ell, bar5, lab5, edit)
            yt2.next_to(yours, RIGHT, buff=0.35)
            self.play(FadeIn(yt2, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt2, TURN)
            vo.wait_until("The server reloads by itself")
            self.play(FadeIn(rcard.frame), FadeIn(reload_rows[0], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("because this file sits under")
            self.play(each(api_glyphs, TURN, scale=1.25, lag=0.05), Indicate(reload_rows[0][2], color=TURN),
                      run_time=0.8)
            vo.wait_until("Its neighbor, the agent tools file")
            self.play(FadeIn(reload_rows[1], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("press control C")
            self.play(Indicate(reload_rows[1][1], color=TURN, scale_factor=1.06),
                      Indicate(reload_rows[1][2], color=TURN, scale_factor=1.08), run_time=0.8)

        # ========================================================== 3. /finetunechat: the part 1 puzzle lands
        c249 = card_249().move_to([0, 2.0, 0])
        page3 = browser_glyph(url="localhost:3200/finetunechat", glyph_w=9.4, glyph_h=2.6, name=None)
        page3.move_to([0, -1.2, 0])
        q3 = label(QUESTION_AGENT, 20, INK)
        bub3 = RoundedRectangle(width=q3.width + 0.5, height=q3.height + 0.35, corner_radius=0.16,
                                stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARK, 1)
        bub3.move_to(page3.window).shift(DOWN * 0.3)
        q3.move_to(bub3)
        ill3 = illustration_tag().next_to(page3.window, DOWN, buff=0.15).align_to(page3.window, RIGHT)
        src3 = note("README.md · line 232").next_to(page3.window, DOWN, buff=0.2).align_to(page3.window, LEFT)

        g = IamGridRig().move_to([0, 1.0, 0])
        toks = [g.token("Owner", S.GREY, mono_font=False), g.token("roles/aiplatform.user", PASS),
                g.token("Storage Admin", S.GREY, mono_font=False)]
        toks[0].move_to(g.slot_point(0, 0))
        toks[1].move_to(g.slot_point(1, 0, 0, 2))
        toks[2].move_to(g.slot_point(1, 0, 1, 2))
        grid = VGroup(g, *toks)
        col = g.cells[1][2]
        cx = col.get_center()[0]
        bottom = g.cells[-1][2].get_bottom()[1]
        req = req_chip_at(cx, bottom - 0.5, "tuned model")
        p_req = path_text(TUNED).next_to(req, DOWN, buff=0.2)
        p_req.shift(RIGHT * min(0, 6.5 - p_req.get_right()[0]))
        br3 = browser_glyph(glyph_w=1.2, name="your browser").move_to([-5.5, -2.4, 0])
        to_req = Arrow(br3.window.get_right() + RIGHT * 0.1, req.get_left() + LEFT * 0.1, buff=0, color=ROUTE,
                       stroke_width=4, path_arc=0.25, tip_length=0.2, max_tip_length_to_length_ratio=0.2)
        up = Arrow(req.get_top(), [cx, col.get_center()[1] + 0.05, 0], buff=0.05, color=ROUTE, stroke_width=4,
                   tip_length=0.18, max_tip_length_to_length_ratio=0.5)
        cap = note("nothing documents this error's exact text").move_to([0.6, -3.25, 0])

        p6 = rag_ft_client()
        place_top(p6, -1.0, 0.0)
        us = code_span(p6.code, 2, 'location="us"')
        ring6 = ring(us, TURN, buff=0.06)
        wrapped = note("line 111 · wrapped to fit").next_to(p6.header, RIGHT, buff=0.5)
        gold3 = cost_tag("tuned-model calls bill the endpoint's project").move_to([0, 1.9, 0])
        c249b = card_249().move_to([-1.6, 0.55, 0])
        yt3 = your_turn().next_to(c249b, RIGHT, buff=0.35)
        e403 = err_chip("403").next_to(yt3, RIGHT, buff=0.3)

        with self.voiceover(SAY[3]) as vo:
            clear_but(self, tr, anims=[FadeIn(c249, shift=UP * 0.2)], run_time=0.6)
            self.play(FadeIn(page3, shift=UP * 0.2), FadeIn(ill3), FadeIn(src3), run_time=0.6)
            self.play(Indicate(page3.url, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and ask the same question")
            self.play(FadeIn(bub3), run_time=0.3)
            self.add(q3)
            self.play(ShowIncreasingSubsets(q3, rate_func=linear), run_time=1.2)

            vo.wait_until("Here the part 1 puzzle")
            old3 = VGroup(c249, ill3, src3, bub3, q3)
            self.play(FadeOut(old3), ReplacementTransform(page3, br3), run_time=0.8)
            self.remove(old3)
            self.play(FadeIn(grid, scale=1.05), run_time=0.7)
            vo.wait_until("With the default, the endpoint path")
            self.play(Create(to_req), FadeIn(req, shift=RIGHT * 0.2), run_time=0.8)
            self.play(FadeIn(p_req, shift=DOWN * 0.15), run_time=0.4)
            self.play(Indicate(p_req.middle, color=ERR, scale_factor=1.15), g.pulse_col(2), run_time=0.9)
            vo.wait_until("where your account has no role")
            self.play(col.animate(rate_func=there_and_back).set_stroke(TURN, 6), run_time=0.8)
            vo.wait_until("so you get a 403")
            self.play(Create(up), run_time=0.5)
            mark = g.verdict(1, 2, ok=False)
            flash = col.copy().set_stroke(ERR, 5)
            self.play(FadeIn(mark, scale=1.3), FadeIn(flash), run_time=0.45)
            self.play(FadeOut(flash), FadeIn(cap), run_time=0.4)
            self.remove(flash)

            vo.wait_until("This call also uses a second client")
            drop(self, br3, to_req, req, p_req, up, run_time=0.5)
            self.play(FadeIn(p6, shift=UP * 0.2), FadeIn(wrapped), run_time=0.6)
            vo.wait_until("in the U S location")
            self.play(Create(ring6), each(us, TURN, scale=1.15, lag=0.04), run_time=0.8)
            vo.wait_until("A final gold tag")
            drop(self, grid, mark, cap, anims=[FadeIn(gold3, shift=UP * 0.2)], run_time=0.6)
            flash_tag(self, gold3, COST)
            vo.wait_until("whichever project owns the endpoint")
            self.play(Indicate(gold3.text, color=COST, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Pause and try it")
            self.play(FadeIn(c249b, shift=UP * 0.2), FadeIn(yt3, shift=LEFT * 0.15), run_time=0.6)
            flash_tag(self, yt3, TURN)
            vo.wait_until("expect the 403")
            self.play(FadeIn(e403, scale=1.2), run_time=0.5)
            self.play(Indicate(e403.text, color=ERR, scale_factor=1.15), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
