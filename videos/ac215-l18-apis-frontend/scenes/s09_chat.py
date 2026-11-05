"""S09 · A chat is a file, not a memory (AC215 L18, part 1, last scene). Tracker [B] "README › Tutorial:
Backend APIs" 9 → 10. Lecture: 18 · 27 (Frontend), beat 0 only.

Beats (script.md "## S09", one voiceover block each):
0. Tracker [B] 9, lecture_ref 27 (Frontend). A GREY card redraws slide 27's handler: route label /chat
   (PINK) and "use Gemini to generate text", with the tag "erratum · slide 27: /chat". Under it
   CODE(api/routers/chat.py: 58–67), line 58 @router.post("/chats") YELLOW; on "another continues it"
   the panel becomes 69–76 (line 70's middle elided), line 69 YELLOW. On "The real path" a PINK label
   /api/llm/chats writes beside the card.
1. Lecture off. V7 ChatFile alone (browser with the PINK key X-Session-ID, the API box and its memory
   bubble; illustration tag on the browser). The bubble pulses on the question; the key on "with
   every message"; a GREY chip "a random UUID · one per browser"; on "The API opens" a POST envelope
   carries the key and a message to the API, the GREEN file chat-history/llm-cnn/<session>/<chat>.json
   opens, the bubble fills, two rows (user, assistant) append, the file flashes ("saves") and the
   bubble empties ("forgets").
2. Tracker [B] 9 · extra. CODE(chat.py: 19–23) under V7 (line 20's regex cut, line 21's "str, "
   elided), line 21 YELLOW, X-Session-ID PINK. The panel gives way to a 4-row `second tab` strip (bar
   tag extra): b36 (folds) → b36:2 wrap, 3 (missing … X-Session-ID YELLOW, 422 RED); the envelope
   without a key bounces RED, 422 chip. b37 → b37:2–3; an empty envelope bounces, 422.
3. Strip: b39 (folds) → b39:2 from "\"role\":\"cnn\"" (wrap), 3; prediction_label … 58.22 YELLOW,
   [HTTP 200] GREEN. Chips: "photo step: offline" under the browser, "photo payload:
   news-letters/assets/blue-cheese.jpg" (the repo's own photo). The PURPLE CNN box under the API
   answers "a guess"; on "A follow-up question" the payload chip gives way to a GREY dashed arrow to a
   dashed chip "follow-up question → Gemini" (never taken).
4. Strip: extra b42 (folds) → b42:2–3 (wrap): llm-cnn/ and .json GREEN, the UUIDs GREY. V7's file
   now holds the identify chat (user: a photo · cnn: parmigiano, 58.22), its path flashes; the GREEN
   folder llm-cnn/images/ with a photo lands under it.
5. Strip: extra b38 (folds); on "and here it stops" a PINK arrow API → BLUE dashed "Vertex AI ·
   Gemini" cloud, GOLD cost tag "with your key: billed", a RED cross at the cloud; b38:2–3 RED. On
   "The API's terminal shows why" the strip becomes the uvicorn terminal (`laptop`): b21:92, 93, …,
   174–179 (GREY), …, 261 (RED, wrap). On "With your key" the strip goes, the cost tag moves under the
   cloud and EXPECTED(02-chat-contract: 11–15) appears, tag expected · docs/contract.md:38–42.
6. Tracker extra off. V7 fades. RECORDED(04-troubleshooting: 11–12), tag recorded · README:230–231;
   a GREEN chip "API answers 502" (llm_utils.py:85–86) beside the Gemini rows; under the card a GREY
   tag "not in the table" with an arrow to a RED chip "500 + RefreshError in the API terminal".
7. V7 returns. A README card (README.md · lines 134–138), its first bullet lit; on "so any copy" the
   card goes and V7's second TEAL API copy opens the same file ("any copy can answer"); on "And routes
   written with plain def" three PURPLE lanes in the API box: a slow GOLD dot holds lane 1 while PINK
   dots pass on lanes 2 and 3, twice.
8. Tracker [B] 10. V7 goes. A 10-row `laptop · new terminal` (…/cheese-app-v2/src/api-service$):
   ./docker-shell.sh → b44:2 (YELLOW, wrap), chip "already running · shelling in"; at the container
   prompt of b44:3 `pytest` → b44:5, 11, 13–14, 16 (wrap), line 16 GREEN; a GREEN "26 passed" badge
   grows out of it; ▶ your turn and "at the time of recording" on the bar.
9. The terminal goes; V5's laptop (API and vector-db boxes, cable) appears and the badge settles on
   the API box. A README card (README.md · line 145) "Keep this container running." The empty GREY
   browser at localhost:3000 (illustration); a PINK dashed arrow leaves the page and stops at a YELLOW
   "?" before the 9000 door. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S09"]

# ------------------------------------------------------------------ the real sources (checked)
CHAT = f"{V2}/src/api-service/api/routers/chat.py"
assert excerpt(CHAT, 58, 58).strip() == '@router.post("/chats")'
assert excerpt(CHAT, 69, 69).strip() == '@router.post("/chats/{chat_id}")'
assert excerpt(CHAT, 21, 21).startswith('SessionId = Annotated[str, Header(alias="X-Session-ID"')
ELIDE70 = {70: "message: ChatMessage, "}
CUT20 = {20: 'r"^[0-9a-fA-F]{8}-'}
ELIDE21 = {21: "str, "}
LLM_UTILS = f"{V2}/src/api-service/api/utils/llm_utils.py"
assert "status_code=502" in excerpt(LLM_UTILS, 86, 86) and "except errors.APIError" in excerpt(LLM_UTILS, 85, 85)

B21 = capture("b21")
B36 = capture("b36")
B37 = capture("b37")
B38 = capture("b38")
B39 = capture("b39")
B42 = capture("b42")
B44 = capture("b44")
assert B36.at(2, 3) == ['{"detail":[{"type":"missing","loc":["header","X-Session-ID"],"msg":"Field required",'
                        '"input":null}]}', "[HTTP 422]"], B36.at(2, 3)
assert B37.at(2, 3) == ['{"detail":"Message must contain text or an image"}', "[HTTP 422]"]
assert B38.at(2, 3) == ["Internal Server Error", "[HTTP 500]"]
assert B39.line(3) == "[HTTP 200]" and B39.line(2).endswith('"prediction_label":"parmigiano","accuracy":58.22}}]}')
assert "-d @/tmp/identify.json" in B39.cmd
B39_2 = from_phrase(B39.line(2), '"role":"cnn"')
assert B42.line(2).startswith("persistent-folder/chat-history/llm-cnn/images/") and B42.line(2).endswith(".png")
assert B42.line(3).startswith("persistent-folder/chat-history/llm-cnn/" + SESSION_ID) and B42.line(3).endswith(".json")
assert B21.line(92).endswith('"POST /api/llm/chats HTTP/1.1" 500 Internal Server Error')
assert B21.line(93) == "ERROR:    Exception in ASGI application"
assert B21.line(174).strip() == 'File "/app/api/routers/chat.py", line 67, in start_chat'
assert B21.line(178).strip() == 'File "/app/api/utils/llm_utils.py", line 94, in respond'
assert B21.line(261).startswith("google.auth.exceptions.RefreshError: ('invalid_grant: Invalid grant: account not found'")
assert B44.cmd == "./docker-shell.sh"
assert B44.line(2) == "Container 'cheese-app-api-service' is already running. Shelling into it..."
assert at_prompt(B44, 3)[1] == "pytest"
assert B44.line(11) == "collected 26 items" and "26 passed in 0.51s" in B44.line(16)
assert B44.line(5).startswith("platform linux -- Python 3.13.18, pytest-9.2.0")

R145 = md_plain(readme(145))
assert R145 == "Keep this container running.", R145
R134 = readme_lines(134, 138)
assert R134.split("\n")[0] == "Two things to notice in routers/chat.py:", R134
assert len(R134.split("\n")) == 5

CF_DOWN = DOWN * 0.3           # V7 alone (beat 1): a little under the middle
CF_UP = UP * 0.85              # from beat 2 on V7 sits higher (net +0.55), so a 4-row 20 pt strip fits under it
STRIP_ROWS, STRIP_PT = 4, 20


# ------------------------------------------------------------------ local helpers
def strip(prompt=P_V2_API, title=T_TAB) -> Terminal:
    """The house strip for this scene: 4 rows at 20 pt (72 characters), full width, on BOTTOM."""
    return term(prompt, STRIP_ROWS, title, size=STRIP_PT)


def bar_tag(scene, t: Terminal, tg, left: bool = False):
    """PLAYS: a row-sized tag on the terminal's title bar: right end (replacing the one there), or
    left=True just after the window dots (▶ your turn)."""
    if left:
        tg.move_to([t.dots.get_right()[0] + 0.3 + tg.width / 2, t.box.get_top()[1] - t.bar_h / 2, 0])
        scene.play(FadeIn(tg, shift=RIGHT * 0.1), run_time=0.4)
        scene.remove(tg)
        t.add(tg)
        scene.add(t)
        return tg
    old = getattr(t, "bar_tag", None)
    on_bar(t, tg)
    if old is not None:
        t.remove(old)
        scene.play(FadeOut(old), FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    else:
        scene.play(FadeIn(tg, shift=LEFT * 0.1), run_time=0.4)
    scene.remove(tg)
    t.add(tg)
    scene.add(t)
    t.bar_tag = tg
    return tg


def unbar(t: Terminal) -> list:
    """Take the title-bar tag off the terminal: returns [FadeOut(tag)] to play."""
    old = getattr(t, "bar_tag", None)
    if old is None:
        return []
    t.remove(old)
    t.bar_tag = None
    return [FadeOut(old)]


def clear_lines(scene, t: Terminal, run_time: float = 0.3):
    """PLAYS: every printed row fades and leaves the terminal."""
    gone = list(t.lines)
    if not gone:
        return
    for m in gone:
        t.lines.remove(m)
    scene.play(FadeOut(VGroup(*gone)), run_time=run_time)
    scene.remove(*gone)


def across(rows, sub: str, occurrence: int = 0) -> VGroup:
    """The glyphs of `sub` in a long line hard-wrapped over several printed rows (the rows join back
    to the line: no spaces in it)."""
    rows = list(rows)
    full = "".join(r.text for r in rows)
    i = -1
    for _ in range(occurrence + 1):
        i = full.find(sub, i + 1)
    if i < 0:
        raise ValueError(f"{sub!r} not in {full!r}")
    out_, pos = VGroup(), 0
    for r in rows:
        a, b = pos, pos + len(r.text)
        lo, hi = max(a, i), min(b, i + len(sub))
        if lo < hi:
            out_.add(*glyph_range(r, lo - a, hi - a))
        pos = b
    return out_


def file_flash(cf):
    """ANIM: the chat file's outline thickens and flashes YELLOW and back (the fill keeps its tint)."""
    return cf.file.frame.animate(rate_func=there_and_back).set_stroke(TURN, 7)


def paint(scene, t, glyphs, color, run_time: float = 0.4):
    """PLAYS: recolour glyphs of terminal t's rows, then re-seat t (split trap)."""
    scene.play(glyphs.animate.set_color(color), run_time=run_time)
    scene.add(t)


class ChatIsAFile(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S09"] == 10, len(SAY)

        # ========================================================== 0. slide 27 vs the two real routes
        trk = tracker_b(9)
        ref = lref("27 (Frontend)")
        route_row = VGroup(label("route", 20, S.GREY), mono("/chat", 22, ROUTE)).arrange(RIGHT, buff=0.18)
        slide = card([route_row, label("use Gemini to generate text", 22, INK)], head="the lecture's chat handler")
        slide.move_to([0, 0, 0]).align_to([-6.5, 0, 0], LEFT).set_y(1.75)
        err = erratum_tag("erratum · slide 27: /chat").next_to(slide, RIGHT, buff=0.35).align_to(slide, UP)
        p58 = code(CHAT, 58, 67, font_size=20, dedent=True)
        p58.move_to([0, 0, 0]).align_to([0, 0.62, 0], UP)
        p69 = code(CHAT, 69, 76, font_size=20, dedent=True, elide=ELIDE70)
        p69.move_to([0, 0, 0]).align_to([0, 0.62, 0], UP)
        real = VGroup(label("the real path", 20, S.GREY), mono("/api/llm/chats", 26, ROUTE)).arrange(RIGHT, buff=0.25)
        real.next_to(slide, RIGHT, buff=0.35).align_to(slide, DOWN)
        assert real.get_right()[0] < SAFE_X and err.get_right()[0] < SAFE_X, (real.get_right(), err.get_right())
        assert slide.get_bottom()[1] > p58.get_top()[1] + 0.05, (slide.get_bottom(), p58.get_top())
        assert slide.get_top()[1] < trk.get_bottom()[1] - 0.05
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk), FadeIn(ref), run_time=0.5)
            self.play(FadeIn(slide, shift=RIGHT * 0.15), run_time=0.6)
            self.play(Indicate(slide.body[1], color=TURN, scale_factor=1.06), FadeIn(err), run_time=0.8)
            vo.wait_until("In the repository")
            bar58 = line_bar(p58.code, 0, TURN)
            self.play(FadeIn(p58, shift=UP * 0.15), run_time=0.6)
            self.play(FadeIn(bar58), run_time=0.4)
            self.play(Indicate(code_span(p58.code, 1, "start_chat"), color=TURN, scale_factor=1.12), run_time=0.6)
            self.add(p58)
            vo.wait_until("and another continues it")
            bar69 = line_bar(p69.code, 0, TURN)
            self.play(FadeOut(VGroup(p58, bar58)), FadeIn(p69), run_time=0.6)
            self.play(FadeIn(bar69), run_time=0.4)
            self.play(Indicate(code_span(p69.code, 1, "continue_chat"), color=TURN, scale_factor=1.12),
                      run_time=0.6)
            self.add(p69)
            vo.wait_until("The real path names the mode")
            self.play(TransformFromCopy(route_row[1], real[1]), FadeIn(real[0]), run_time=0.8)
            self.play(Indicate(real[1], color=ROUTE, scale_factor=1.1), run_time=0.6)

        # ========================================================== 1. V7: the browser keeps the key
        cf = ChatFile()
        cf.shift(CF_DOWN)
        cf.file.shift(CF_DOWN)                      # the file is built but not yet a part: move it too
        ill = illustration_tag().next_to(cf.browser.frame, UP, buff=0.12).align_to(cf.browser.frame, LEFT)
        assert ill.get_top()[1] < trk.get_bottom()[1] - 0.02, ill.get_top()
        uuid = grey_chip("a random UUID · one per browser").next_to(cf.browser.frame, DOWN, buff=0.15)
        uuid.align_to(cf.browser.frame, LEFT)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(slide, err, real, p69, bar69)), FadeOut(ref), run_time=0.6)
            self.play(FadeIn(cf), FadeIn(ill), run_time=0.8)
            self.play(Indicate(cf.bubble, color=TURN, scale_factor=1.2), run_time=0.8)
            cf.heal(self)
            vo.wait_until("with every message")
            self.play(Indicate(cf.key, color=TURN, scale_factor=1.15), run_time=0.8)
            cf.heal(self)
            vo.wait_until("one random UUID")
            self.play(FadeIn(uuid, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("The API opens that session's chat file")
            cf.post(self, "your message", run_time=1.0)
            cf.open_file(self, run_time=0.7)
            cf.remove(cf.rows)                      # the rows draw over the file's opaque fill
            cf.add(cf.rows)
            cf.heal(self)
            vo.wait_until("adds your message")
            cf.remember(self, run_time=0.4)
            cf.append(self, ("user", "your message"), ("assistant", "the reply"), run_time=0.9)
            vo.wait_until("saves, and forgets")
            self.play(file_flash(cf), run_time=0.7)
            cf.heal(self)
            vo.wait_until("and forgets")
            cf.forget(self, run_time=0.6)

        # ========================================================== 2. extras: no key, no message -> 422
        p19 = code(CHAT, 19, 23, font_size=20, cuts=CUT20, elide=ELIDE21)
        p19.move_to([0, 0, 0]).align_to([0, BOTTOM + 0.05, 0], DOWN)
        t = strip()
        with self.voiceover(SAY[2]) as vo:
            self.play(track(trk, 9, True), FadeOut(uuid), cf.animate.shift(CF_UP), ill.animate.shift(CF_UP),
                      run_time=0.6)
            assert p19.get_top()[1] < cf.get_bottom()[1] - 0.1, (p19.get_top(), cf.get_bottom())
            assert t.box.get_top()[1] < cf.get_bottom()[1] - 0.05, (t.box.get_top(), cf.get_bottom())
            assert ill.get_top()[1] < trk.get_bottom()[1] - 0.02, ill.get_top()
            bar21 = line_bar(p19.code, 2, TURN)
            self.play(FadeIn(p19, shift=UP * 0.15), run_time=0.5)
            self.play(FadeIn(bar21), code_span(p19.code, 2, '"X-Session-ID"').animate.set_color(ROUTE), run_time=0.5)
            self.add(p19)
            vo.wait_until("no session ID")
            self.play(FadeOut(VGroup(p19, bar21)), FadeIn(t), run_time=0.5)
            bar_tag(self, t, extra_row())
            type_cmd(self, t, B36.cmd, soft=True)
            rows = out(self, t, B36.at(2), wrap=True)
            paint(self, t, across(rows, '"missing"') + across(rows, '"X-Session-ID"'), TURN)
            out(self, t, [(B36.line(3), ERR)])
            e1 = cf.post(self, "message", key=False, code="422", run_time=1.0)
            type_cmd(self, t, B37.cmd, soft=True)
            out(self, t, [B37.line(2), (B37.line(3), ERR)])
            cf.drop(self, e1, run_time=0.3)
            cf.post(self, "{}", key=True, ok=False, code="422", run_time=1.0)

        # ========================================================== 3. extra: Identify, offline
        offline = grey_chip("photo step: offline").next_to(cf.browser.frame, DOWN, buff=0.15)
        offline.align_to(cf.browser.frame, LEFT)
        payload = VGroup(label("photo payload:", 20, S.GREY), mono("news-letters/assets/blue-cheese.jpg", 20, INK))
        payload.arrange(RIGHT, buff=0.15)
        pbox = outline_box(payload.width + 0.4, payload.height + 0.3, S.GREY, solid=True)
        payload = VGroup(pbox, payload.move_to(pbox))
        payload.move_to([SAFE_X - 0.1 - payload.width / 2, -0.6, 0])
        with self.voiceover(SAY[3]) as vo:
            clear_lines(self, t)
            cf.drop(self, *list(cf.marks), run_time=0.3)
            self.play(FadeIn(offline, shift=UP * 0.1), run_time=0.4)
            type_cmd(self, t, B39.cmd, soft=True)
            vo.wait_until("We send the repository's own")
            self.play(FadeIn(payload, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and the CNN guesses parmigiano")
            rows = out(self, t, [B39_2], wrap=True)
            self.play(FadeOut(payload), run_time=0.3)
            cf.cnn(self, "a guess", run_time=0.6)
            paint(self, t, across(rows, '"prediction_label":"parmigiano"'), TURN)
            vo.wait_until("at 58 percent")
            paint(self, t, across(rows, '"accuracy":58.22'), TURN)
            out(self, t, [(B39.line(3), OWN)])
            vo.wait_until("A follow-up question")
            fu = dashed_chip("follow-up question → Gemini")
            fu.move_to([SAFE_X - 0.15 - fu.width / 2, -0.6, 0])
            fu_arrow = DashedLine(cf.api.frame.get_corner(DR) + UP * 0.15, fu.get_left() + LEFT * 0.05,
                                  color=S.GREY, stroke_width=3, dash_length=0.1)
            assert fu.get_left()[0] > cf.marks.get_right()[0] + 0.2, (fu.get_left(), cf.marks.get_right())
            self.play(Create(fu_arrow), FadeIn(fu), run_time=0.7)

        # ========================================================== 4. extra: the files on disk
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(offline, fu, fu_arrow)), run_time=0.4)
            cf.drop(self, *list(cf.marks), run_time=0.3)
            clear_lines(self, t)
            type_capture(self, t, B42)
            r2 = out(self, t, B42.at(2), wrap=True)
            r3 = out(self, t, B42.at(3), wrap=True)
            grey = (across(r2, B42.line(2).split("/")[4]) + across(r2, B42.line(2).split("/")[5][:-4])
                    + across(r3, SESSION_ID) + across(r3, B42.line(3).split("/")[4][:-5]))
            green = (across(r2, "llm-cnn/") + across(r3, "llm-cnn/") + across(r3, ".json"))
            self.play(grey.animate.set_color(S.GREY), green.animate.set_color(OWN), run_time=0.5)
            self.add(t)
            vo.wait_until("one JSON file per chat")
            cf.drop(self, *list(cf.rows), run_time=0.3)
            self.play(Indicate(cf.file.path, color=OWN, scale_factor=1.05), run_time=0.6)
            cf.heal(self)
            cf.append(self, ("user", "a photo"), ("cnn", "parmigiano, 58.22"), run_time=0.8)
            vo.wait_until("and the photo")
            cf.images(self, run_time=0.6)
            self.play(Indicate(cf.folder, color=OWN, scale_factor=1.08), run_time=0.6)
            cf.heal(self)

        # ========================================================== 5. extra: Ask -> Gemini -> 500
        cl = cloud_shape("Vertex AI\nGemini", CLOUD, cloud_w=1.8, dashed=True).move_to([4.6, -0.5, 0])
        g_arrow = Arrow(cf.api.frame.get_bottom() + RIGHT * 1.2, cl.get_left() + RIGHT * 0.12, buff=0.05,
                        color=ROUTE, stroke_width=4, tip_length=0.18)
        cross = cross_glyph(0.3, ERR).move_to(g_arrow.get_end() + LEFT * 0.3 + UP * 0.28)
        cost = cost_tag("with your key: billed").next_to(cf.api.frame, DOWN, buff=0.18)
        cost.align_to(cf.api.frame, LEFT).shift(LEFT * 0.3)
        cost_low = cost.copy().next_to(cl, DOWN, buff=0.15)
        exp = quote_card("02", (11, 15), "expected", "docs/contract.md:38–42", size=20, width_chars=80)
        exp.move_to([0, 0, 0]).align_to([-6.45, 0, 0], LEFT).align_to([0, BOTTOM, 0], DOWN)
        assert cost_low.get_left()[0] > exp.get_right()[0] + 0.1, (cost_low.get_left(), exp.get_right())
        assert cost_low.get_right()[0] < SAFE_X, cost_low.get_right()
        assert cost.get_left()[0] > cf.browser.frame.get_right()[0] + 0.1, cost.get_left()
        assert exp.get_top()[1] < cost.get_bottom()[1] - 0.05, (exp.get_top(), cost.get_bottom())
        log = B21.at(92, 93, "…", (174, 179), "…")
        with self.voiceover(SAY[5]) as vo:
            clear_lines(self, t)
            type_cmd(self, t, B38.cmd, soft=True)
            vo.wait_until("and here it stops")
            cf.drop(self, *list(cf.marks), run_time=0.3)
            self.play(FadeIn(cl), GrowArrow(g_arrow), FadeIn(cost), run_time=0.8)
            self.play(FadeIn(cross, scale=1.3), g_arrow.animate.set_color(ERR), run_time=0.5)
            vo.wait_until("Internal Server Error")
            out(self, t, [(B38.line(2), ERR), (B38.line(3), ERR)])
            vo.wait_until("The API's terminal shows why")
            clear_lines(self, t)
            self.play(retitle(t, T_LAPTOP), *unbar(t), run_time=0.4)
            self.add(t)
            out(self, t, [log[0], log[1], log[2]] + [(s, S.GREY) for s in log[3:9]] + [log[9]], wrap=True,
                chunk=STRIP_ROWS, run_time=2.0)
            vo.wait_until("the same invalid grant")
            rows = out(self, t, [(B21.line(261), ERR)], wrap=True, run_time=0.6)
            self.play(Indicate(across(rows, "account not found"), color=ERR,
                               scale_factor=1.05), run_time=0.8)
            self.add(t)
            vo.wait_until("With your key")
            self.play(FadeOut(t), Transform(cost, cost_low), run_time=0.6)
            self.play(FadeIn(exp, shift=UP * 0.15), run_time=0.6)
            flash_tag(self, cost)
            self.play(Indicate(exp.body[3], color=OWN, scale_factor=1.06), run_time=0.8)

        # ========================================================== 6. a small note: 403/404 -> 502, ours -> 500
        tab = quote_card("04-troubleshooting", (11, 12), "recorded", "README:230–231", size=22, width_chars=50)
        tab.move_to([-2.1, 0.75, 0])
        n_rows = len(tab.body)
        ok502 = VGroup(ok_chip("API answers 502"), mono("llm_utils.py:85–86", 20, S.GREY)).arrange(DOWN, buff=0.12)
        ok502.next_to(tab, RIGHT, buff=0.9)
        br = arrow(tab.get_right() + RIGHT * 0.05, ok502[0].get_left(), OWN, stroke=3, buff=0.08)
        notin = tag("not in the table", S.GREY).move_to([-4.4, -1.45, 0])
        e500 = err_chip("500 + RefreshError in the API terminal", mono_font=False).move_to([1.7, -1.45, 0])
        to500 = arrow(notin.get_right(), e500.get_left(), S.GREY, stroke=3)
        assert ok502.get_right()[0] < SAFE_X and e500.get_right()[0] < SAFE_X, (ok502.get_right(), e500.get_right())
        assert notin.get_top()[1] < tab.get_bottom()[1] - 0.2
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(cf), FadeOut(ill), FadeOut(VGroup(cl, g_arrow, cross, cost, exp)), track(trk, 9, False),
                      run_time=0.6)
            self.play(FadeIn(tab, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("Gemini 403 and 404")
            self.play(LaggedStart(*[Indicate(r, color=TURN, scale_factor=1.04) for r in tab.body], lag_ratio=0.2),
                      run_time=1.0)
            vo.wait_until("reported as 502")
            self.play(GrowArrow(br), FadeIn(ok502, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("A key Google cannot sign in with")
            self.play(FadeIn(notin, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("as a plain 500")
            self.play(GrowArrow(to500), FadeIn(e500, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("so check the API's terminal first")
            self.play(Indicate(e500, color=ERR, scale_factor=1.08), run_time=0.8)
        del n_rows

        # ========================================================== 7. two README notes: any copy, threads
        notes = readme_card((134, 138), R134, size=20)
        notes.move_to([0, 0, 0]).align_to([0, BOTTOM + 0.05, 0], DOWN)
        assert notes.width < 2 * SAFE_X - 0.1 and notes.get_top()[1] < cf.get_bottom()[1] - 0.1
        hl1 = hl_bar(VGroup(notes.body[1], notes.body[2]), TURN, opacity=0.18)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(tab, ok502, br, notin, e500, to500)), FadeIn(cf), FadeIn(ill),
                      FadeIn(notes, shift=UP * 0.15), run_time=0.8)
            vo.wait_until("Each message rebuilds")
            self.play(FadeIn(hl1), run_time=0.4)
            self.play(file_flash(cf), run_time=0.7)
            cf.heal(self)
            vo.wait_until("so any copy of the API")
            self.play(FadeOut(VGroup(notes, hl1), shift=DOWN * 0.2), run_time=0.4)
            cf.second_copy(self, run_time=0.9)
            vo.wait_until("And routes written with plain def")
            lanes = cf.threads(self, run_time=1.4)
            slow = cf.marks[-1]
            vo.wait_until("so one slow answer")
            for _ in range(2):
                fast = [Dot(radius=0.07, color=ROUTE).move_to(ln.get_start()) for ln in lanes[1:]]
                self.add(*fast)
                self.play(slow.animate.shift(RIGHT * 0.35),
                          *[f.animate.move_to(ln.get_end()) for f, ln in zip(fast, lanes[1:])],
                          run_time=1.0, rate_func=linear)
                self.remove(*fast)
                cf.heal(self)

        # ========================================================== 8. Tracker 10: pytest in a new terminal
        nt = new_term(10, P_V2_API)
        already = grey_chip("already running · shelling in")
        under_term(nt, already)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(cf), FadeOut(ill), track(trk, 10), run_time=0.6)
            self.play(FadeIn(nt, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("in the same folder")
            type_capture(self, nt, B44)
            out(self, nt, [(B44.line(2), TURN)], wrap=True)
            self.play(FadeIn(already, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Run pytest")
            type_at(self, nt, B44, 3)
            bar_tag(self, nt, time_row())
            rows = out(self, nt, B44.at(5, 11, (13, 14)), wrap=True, run_time=0.8)
            last = out(self, nt, [(B44.line(16), OWN)], wrap=True, run_time=0.4)
            vo.wait_until("26 passed")
            badge = ok_chip("26 passed").next_to(nt.box, UP, buff=0.18).align_to(nt.box, RIGHT)
            src = across([r for r in last if "26 passed" in r.text], "26 passed")
            self.play(FadeOut(already), TransformFromCopy(src, badge), run_time=0.8)
            self.add(nt)
            vo.wait_until("Pause and run it")
            bar_tag(self, nt, turn_row(), left=True)
            self.play(Indicate(badge, color=OWN, scale_factor=1.1), run_time=0.6)
        del rows

        # ========================================================== 9. keep it running; the parked question
        tr = RequestTrace("localhost:3000", rows=("api", "vdb"), front=None, caption=False)
        tr.shift(UP * 0.4)
        keep = readme_card(145, R145)
        keep.move_to([0, -2.7, 0])
        assert keep.get_top()[1] < tr.get_bottom()[1] - 0.1, (keep.get_top(), tr.get_bottom())
        api_box = tr.net.boxes["api"].frame
        b_target = api_box.get_top() + RIGHT * 0.45
        start = tr.browser.at(-0.35, 0.0)
        start[1] = tr.net.row_y("api")
        stop = np.array([tr.divider.get_x() - 0.22, start[1], 0])
        call = DashedVMobject(Arrow(start, stop, buff=0.02, color=ROUTE, stroke_width=4, tip_length=0.18,
                                    max_tip_length_to_length_ratio=0.35), num_dashes=7).set_stroke(ROUTE, 4)
        q = label("?", 36, TURN).move_to([tr.divider.get_x() + 0.12, start[1], 0])
        assert q.get_right()[0] < tr.net.door_point("api")[0] - 0.05, (q.get_right(), tr.net.door_point("api"))
        btag = illustration_tag().next_to(tr.browser.frame, UP, buff=0.12).align_to(tr.browser.frame, LEFT)
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(nt), FadeIn(tr.net), run_time=0.7)
            self.add(badge)                          # in front of the laptop's opaque frame
            self.play(badge.animate.move_to(b_target), run_time=0.7)
            self.play(FadeIn(keep, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("The API is ready")
            self.play(Indicate(badge, color=OWN, scale_factor=1.1), tr.net.door_pulse("api"), run_time=0.8)
            vo.wait_until("but nobody can use it from a browser yet")
            self.play(FadeIn(tr.browser), FadeIn(tr.divider), FadeIn(btag), run_time=0.6)
            self.remove(badge)
            tr.net.add(badge)
            self.add(tr)
            vo.wait_until("In part 2 the browser talks to port 3000")
            self.play(Indicate(tr.browser.address, color=ROUTE, scale_factor=1.15), run_time=0.6)
            tr.heal(self)
            tr.show(self, call, anims=[Create(call)], run_time=0.8, into=tr.marks)
            vo.wait_until("so how does that reach 9000")
            tr.show(self, q, anims=[FadeIn(q, scale=1.4)], extra=[tr.net.door_pulse("api")], run_time=0.7,
                    into=tr.marks)
            self.wait(0.8)
            self.play(FadeOut(VGroup(tr, btag, keep)), FadeOut(trk), run_time=0.8)
        self.wait(0.3)
