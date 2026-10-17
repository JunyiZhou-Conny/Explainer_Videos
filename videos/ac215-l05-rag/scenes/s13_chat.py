"""S13 · Chat: the prompt is the whole trick (README "Chat"). Lecture: A57–A62.

Beats (script.md "## S13", one voiceover block each):
 0  LECTURE A57–A59. TRACKER Chat (no step lit yet). The mini-map, its prompt and LLM boxes lit.
    V7: under a brace "final prompt" three blocks write in as named: "system prompt · how to
    behave" (GREY), "query · the user's input" (PINK), "context · retrieved text" (GREEN).
 1  CODE(cli.py: 379–386) along the bottom (the mini-map hides): lines 380–383 lit, GREY chip "no
    filter this time"; `n_results=10` YELLOW. Ten GREEN chunk cards drop out of the TEAL cylinder.
 2  The panel becomes CODE(cli.py: 388–391): the PINK question card and the ten cards stack into
    one prompt card (question, then the chunks); `"\\n"` underlined; an ORANGE chip "needs Python
    3.12" on line 390 (not narrated). The panel becomes CODE(cli.py: 394–396) as the prompt card
    flows into the BLUE LLM box (chip `gemini-3.1-flash-lite`, note "cli.py · line 27"); gray answer
    bars come out under it, with thin GREEN arrows back to the cards they should draw from.
 3  The system block returns above the prompt card and opens into the GREY dashed ghost card
    `SYSTEM_INSTRUCTION` holding CODE(cli.py: 40–41, line 41 wrapped), then CODE(cli.py: 47,
    wrapped) under it, the two rules underlined. It folds back into a small ghost card; lines
    394–396 flash (`contents=INPUT_PROMPT` underlined, "no config"); the ghost's RED cable hangs
    unplugged beside the LLM box; README chip "README.md · line 21" "grounded in your documents".
 4  Tag `erratum`. The cable plugs in GREEN with the two-row fix chip (`config=…` /
    `system_instruction=…`), tag "fix · not in the repo". The call panel becomes
    CODE(pipenv-branch/cli.py: 62–64), line 64 lit, tag "pipenv branch (March 2025) sent it". The
    README chip, then the prompt card's chunks, pulse.
 5  LECTURE A61–A62. The ghost and the fix leave. A GREY padlock "weights unchanged" on the LLM box;
    the cylinder empties (GREY dashed tag "delete the collection") and the answer's arrows fade away.
 6  TRACKER Chat 1 → Chat 2. The TEAL 3-row strip types both chat commands (no output panels; the
    strip clears between them); the mini-map above the strip; GREY note "no key: both stop at cli.py
    · line 373, embedding the question"; GOLD tag "per question: one embedding call + one Gemini
    call", a GOLD coin on the mini-map's embedding and LLM boxes.
 7  The GREY "with your key, look for" card above the strip, items writing in as named (cli.py lines
    365–399); the "??" boxed, a two-row tag "erratum · harmless / the README shows one".
 8  S01's chat box returns (the question, RED-edged answer bars, the YELLOW "?"). The "?" resolves
    into four GREEN chunk cards; three bars draw thin arrows to them and turn GREEN (tag
    "illustration · a shape, not an answer"). The grounding test card: GREEN "from your chunks" (Mara
    · her grandfather · the curd; excerpt chip `Tolminc Cheese.txt · line 4` "A fictional tale") and
    RED "not in your chunks" (real-world rules for Tolminc; GREY note: only 3 char-split chunks
    contain the word); GREY note "compare the char-split and recursive-split answers".
 9  TRACKER Chat 3. A GREY browser frame (tag illustration) at ac215-llm-rag.dlops.io/chat with a
    schematic chat page, GREY note "use Chrome"; the ▶ your-turn card: both chat commands, the link,
    "your own question: cli.py · line 372 · no rebuild", "404 NOT_FOUND for the model? change
    GENERATIVE_MODEL, cli.py · line 27". Hold 2 s, then everything fades: empty frame.

Deviations from SHOW (see the scene report): beat 0 keeps V7's LLM box hidden (it enters in beat 2,
where the SHOW introduces it with its model chip). Beat 1's PromptStack leaves, and beat 3 brings
its system block back as a copy above the tutorial's prompt card (PromptStack's own ghost and cables
assume its three-block layout, which the tutorial's prompt card replaces from beat 2 on). The ghost
card opens to full width to hold the two wrapped code panels (12 columns of 65 characters do not fit
in a 4-wide card), then folds back. Beat 5 removes the ghost and its (fixed) cable so the picture
shows the code as it is. Beat 6 types the two commands one after the other in a cleared strip:
with no output shown, a second prompt right under the first would read as "it printed nothing".
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    GrowFromPoint,
    Indicate,
    LaggedStart,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    VGroup,
    VMobject,
    Write,
)

from common import (
    CLOUD,
    CTR,
    DATA,
    ERR,
    INK,
    LLM_MODEL,
    LOOKUP,
    MINI_ABOVE_STRIP,
    MINI_CENTER,
    NARRATION,
    P_CTR2,
    QUESTION,
    QUESTION_CHAT,
    STORY_PATH,
    SYSTEM,
    TURN,
    LookFor,
    MiniMap,
    PromptStack,
    Prose,
    answer_bars,
    at_bottom,
    capture,
    chat_window,
    chunk_card,
    coin_glyph,
    concept_tag,
    cost_tag,
    cylinder,
    erratum_tag,
    excerpt,
    excerpt_chip,
    fix_tag,
    illustration_tag,
    lref,
    lref_swap,
    model_box,
    note,
    padlock,
    prompt_card,
    question_card,
    readme_chip,
    ring,
    src_panel,
    term,
    tracker,
    turn_card,
    type_cmd,
    under,
)
from explainer import style as S
from explainer.devops import CAPTION, MONO, box, chip, label, mono
from explainer.scene import VoiceScene

SAY = NARRATION["S13"]

# ------------------------------------------------------------------ the sources this scene quotes
CHAT1 = "python cli.py --chat --chunk_type char-split"          # README.md line 199
CHAT2 = "python cli.py --chat --chunk_type recursive-split"     # README.md line 200
CHAT_URL = "ac215-llm-rag.dlops.io/chat"                        # README.md line 211 (a link)
assert excerpt("README.md", 199, 200).split("\n") == [CHAT1, CHAT2]
assert f"https://{CHAT_URL})" in excerpt("README.md", 211, 211)
README21 = excerpt("README.md", 21, 21)
assert "grounded in your documents" in README21
assert excerpt("cli.py", 27, 27) == f'GENERATIVE_MODEL = "{LLM_MODEL}"'
assert excerpt("cli.py", 40, 40) == 'SYSTEM_INSTRUCTION = """'
assert "based solely on the information provided in the text chunks" in excerpt("cli.py", 41, 41)
assert "state that you don't have enough information" in excerpt("cli.py", 47, 47)
assert excerpt("cli.py", 365, 365).strip() == 'print("chat()")'
assert excerpt("cli.py", 372, 372).strip() == f'query = "{QUESTION_CHAT}"'
assert excerpt("cli.py", 373, 373).strip() == "query_embedding = generate_query_embedding(query)"
assert excerpt("cli.py", 374, 374).strip() == 'print("Query:", query)'
assert excerpt("cli.py", 375, 375).strip() == 'print("Embedding values:", query_embedding)'
assert excerpt("cli.py", 380, 380).strip() == "results = collection.query("
assert excerpt("cli.py", 382, 382).strip() == "n_results=10"
assert excerpt("cli.py", 384, 384).strip() == 'print("\\n\\nResults:", results)'
assert excerpt("cli.py", 386, 386).strip() == 'print(len(results["documents"][0]))'
assert excerpt("cli.py", 388, 388).strip() == 'INPUT_PROMPT = f"""'
assert excerpt("cli.py", 390, 390).strip() == '{"\\n".join(results["documents"][0])}'
assert excerpt("cli.py", 393, 393).strip() == 'print("INPUT_PROMPT: ", INPUT_PROMPT)'
assert excerpt("cli.py", 395, 395).strip() == "model=GENERATIVE_MODEL, contents=INPUT_PROMPT"
assert excerpt("cli.py", 399, 399).strip() == 'print("LLM Response:", generated_text)'
assert excerpt("pipenv-branch/cli.py", 64, 64).strip() == "system_instruction=[SYSTEM_INSTRUCTION]"
STORY4 = excerpt(STORY_PATH, 4, 4)
assert "A fictional tale" in STORY4
TOLMINC3 = capture("08", "recorded-embeddings").line(15)
assert TOLMINC3.startswith("any book, $contains 'Tolminc':") and TOLMINC3.split()[-1] == "3", TOLMINC3
FIX_ROWS = ("config=types.GenerateContentConfig(", "  system_instruction=SYSTEM_INSTRUCTION)")

# ------------------------------------------------------------------ layout (frame coordinates)
CYL_C = np.array([-5.55, 1.35, 0])       # the collection: x -6.1..-5.0, y 0.55..2.16
PC_C = np.array([-2.85, 1.05, 0])        # the prompt card (2.4 x 1.89): x -4.05..-1.65, y 0.1..2.0
GHOST_C = np.array([-2.8, 2.45, 0])      # the system block / SYSTEM_INSTRUCTION ghost above it
LLM_C = np.array([1.3, 1.25, 0])         # the LLM box (1.9 x 1.2): x 0.35..2.25, y 0.65..1.85
CODE_X = -0.4                            # code panels sit on the bottom edge, centred here
MID_Y = -0.9                             # the band between the picture and a 3-row code strip
BAND_Y = 3.22                            # README chip in the band right of the tracker


def curve(points, color: str, stroke: float = 5) -> VMobject:
    m = VMobject(stroke_color=color, stroke_width=stroke)
    m.set_points_smoothly([np.array([p[0], p[1], 0.0]) for p in points])
    return m


def two_row_tag(rows, color: str = S.GREY) -> VGroup:
    """A GREY tag of two centred rows (a long tag where the frame is narrow)."""
    t = VGroup(*[label(r, CAPTION, color) for r in rows]).arrange(DOWN, buff=0.08)
    b = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.24, corner_radius=0.14,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def mixed(parts, size: float = CAPTION, color: str = INK) -> VGroup:
    """One row of serif pieces and `mono` pieces (in backticks); (text, colour) for a colour."""
    mobs = []
    for p in parts:
        s, col = (p, color) if isinstance(p, str) else p
        if len(s) > 1 and s.startswith("`") and s.endswith("`"):
            mobs.append(mono(s[1:-1], size, col))
        else:
            mobs.append(label(s, size, col))
    return VGroup(*mobs).arrange(RIGHT, buff=0.12)


def code_rows(panel, n: int) -> VGroup:
    return VGroup(*[panel.code.code_lines[k] for k in panel.rows_of(n)])


def light_chat(mm: MiniMap) -> list:
    """Light the mini-map's prompt and LLM boxes (MiniMap.light lights one)."""
    return [mm.light("prompt"), mm.items["llm"].animate.set_stroke(TURN, 4)]


def collection() -> VGroup:
    """The TEAL cylinder with a GREEN fill level (the records); .level .cyl"""
    cyl = cylinder(1.1, 1.3)
    body = cyl.body
    level = Rectangle(width=body.width - 0.04, height=body.height * 0.82, stroke_width=0)
    level.set_fill(DATA, 0.4).align_to(body, DOWN)
    cyl.submobjects.insert(2, level)          # above the body's fill, under the disks and the top
    cyl.level = level
    return cyl.move_to(CYL_C)


class FinalPrompt(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, f"S13 has {len(SAY)} SAY lines; this scene times 10"

        tr = tracker("Chat")

        # ========================================================== 0 · the lecture's final prompt
        lr = lref("A57–A59")
        ps = PromptStack(show=()).shift(RIGHT * 3.4)       # the stack and its brace, centred
        mm = MiniMap(MINI_CENTER)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(mm), run_time=0.7)
            self.play(*light_chat(mm), run_time=0.5)
            vo.wait_until("The lecture's final prompt")
            self.add(ps)
            self.play(FadeIn(lr), *ps.parts_in("brace", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2)),
                      run_time=0.6)
            vo.wait_until("a system prompt")
            self.play(*ps.parts_in("system", anim=lambda m: FadeIn(m, shift=RIGHT * 0.3)), run_time=0.5)
            vo.wait_until("the user's query")
            self.play(*ps.parts_in("query", anim=lambda m: FadeIn(m, shift=RIGHT * 0.3)), run_time=0.5)
            vo.wait_until("and the context")
            self.play(*ps.parts_in("context", anim=lambda m: FadeIn(m, shift=RIGHT * 0.3)), run_time=0.5)
            self.play(Indicate(ps.parts["brace"], color=INK, scale_factor=1.05), run_time=0.7)
        sys_block = ps.block("system").copy()                 # it comes back in beat 3

        # ========================================================== 1 · query again: no filter, 10 results
        p1 = at_bottom(src_panel("cli.py", 379, 386), x=CODE_X)
        bars1 = VGroup(*[p1.bar(n, TURN) for n in range(380, 384)])
        ten = p1.span(382, "n_results=10")
        u_ten = under(ten, TURN)
        nofilt = chip("no filter this time", S.GREY, size=CAPTION)
        nofilt.move_to([p1.get_right()[0] + 0.3 + nofilt.width / 2, code_rows(p1, 381).get_center()[1], 0])
        cyl = collection()
        cards = VGroup(*[chunk_card(0.5, 0.3) for _ in range(10)]).arrange_in_grid(5, 2, buff=0.1)
        cards.move_to([CYL_C[0], -0.6, 0])
        spout = cyl.get_bottom() + UP * 0.2

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(ps, shift=UP * 0.2), FadeOut(mm), FadeIn(p1, shift=UP * 0.2), FadeIn(cyl),
                      run_time=0.6)
            vo.wait_until("the code queries again")
            self.play(FadeIn(bars1), Indicate(cyl, color=CTR, scale_factor=1.06), run_time=0.6)
            vo.wait_until("this time with no filter")
            self.play(FadeIn(nofilt, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("for 10 results")
            self.play(ten.animate.set_color(TURN), Create(u_ten), run_time=0.4)
            self.play(LaggedStart(*[GrowFromPoint(c, spout) for c in cards], lag_ratio=0.1), run_time=1.0)

        # ========================================================== 2 · the input prompt goes to Gemini
        p2 = at_bottom(src_panel("cli.py", 388, 391), x=CODE_X)
        b389 = p2.bar(389, LOOKUP, 0.14)
        b390 = p2.bar(390, DATA, 0.14)
        u_nl = under(p2.span(390, '"\\n"'), DATA)
        py = chip("needs Python 3.12", SYSTEM, size=CAPTION)
        py.move_to([p2.get_right()[0] + 0.3 + py.width / 2, code_rows(p2, 390).get_center()[1], 0])
        qcard = question_card(QUESTION_CHAT).move_to([-1.8, GHOST_C[1], 0])
        pc = prompt_card(10, 3.2).scale(0.75).move_to(PC_C)
        p3 = at_bottom(src_panel("cli.py", 394, 396), x=CODE_X)
        llm = model_box("LLM", 1.9, 1.2).move_to(LLM_C)
        mchip = chip(LLM_MODEL, CLOUD, size=CAPTION, font=MONO)
        mchip.move_to([llm.get_right()[0] + 0.25 + mchip.width / 2, LLM_C[1] + 0.2, 0])
        l27 = note("cli.py · line 27").next_to(mchip, DOWN, buff=0.15).align_to(mchip, LEFT)
        feed = Arrow([pc.get_right()[0] + 0.05, LLM_C[1], 0], [llm.get_left()[0] - 0.05, LLM_C[1], 0], buff=0,
                     color=DATA, stroke_width=5, tip_length=0.2)
        ans = answer_bars(3, 2.0)
        ans.move_to([llm.get_left()[0] + ans.width / 2, llm.get_bottom()[1] - 0.25 - ans.height / 2, 0])
        back = VGroup(*[Arrow([ans[b].get_left()[0] - 0.06, ans[b].get_center()[1], 0],
                              [pc.get_right()[0] + 0.04, pc.cards[r].get_center()[1], 0], buff=0,
                              color=DATA, stroke_width=2.5, tip_length=0.14)
                        for b, r in ((0, 5), (1, 7), (2, 9))])

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(bars1, u_ten, nofilt)), ReplacementTransform(p1, p2), run_time=0.7)
            vo.wait_until("the input prompt")
            self.play(Indicate(p2.span(388, "INPUT_PROMPT"), color=TURN, scale_factor=1.15), run_time=0.6)
            vo.wait_until("the question")
            self.play(FadeIn(b389), FadeIn(qcard, shift=DOWN * 0.2), run_time=0.5)
            vo.wait_until("followed by the 10 chunks")
            self.play(FadeIn(pc.frame), FadeIn(b390), ReplacementTransform(qcard, pc.question), run_time=0.6)
            self.play(LaggedStart(*[ReplacementTransform(cards[k], pc.cards[k]) for k in range(10)],
                                  lag_ratio=0.08), run_time=1.1)
            vo.wait_until("joined by newlines")
            self.play(Create(u_nl), FadeIn(py, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("The prompt goes to Gemini")
            self.play(FadeOut(VGroup(b389, b390, u_nl, py)), ReplacementTransform(p2, p3), FadeIn(llm),
                      run_time=0.7)
            fly = pc.copy()
            self.play(fly.animate.scale(0.15).move_to(llm).set_opacity(0), Create(feed),
                      FadeIn(mchip, shift=LEFT * 0.15), FadeIn(l27), run_time=0.8)
            self.remove(fly)
            self.play(Indicate(llm.frame, color=CLOUD, scale_factor=1.06),
                      LaggedStart(*[GrowFromEdge(b, LEFT) for b in ans], lag_ratio=0.4), run_time=0.8)
            self.play(LaggedStart(*[Create(a) for a in back], lag_ratio=0.25), run_time=0.7)

        # ========================================================== 3 · the system prompt: defined, never sent
        sys_block.move_to(GHOST_C)
        p41 = src_panel("cli.py", 40, 41, wrap=True)
        p47 = src_panel("cli.py", 47, 47, wrap=True)
        big_label = mono("SYSTEM_INSTRUCTION", 22, S.GREY)
        content = VGroup(big_label, p41, p47).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        big_h = content.height + 0.4
        big_frame = box(12.9, big_h, S.GREY, dashed=True, stroke=3).move_to([0, 2.78 - big_h / 2, 0])
        backing = Rectangle(width=12.9, height=big_h, stroke_width=0).set_fill(S.BG, 1).move_to(big_frame)
        content.move_to(big_frame).align_to(big_frame, LEFT).shift(RIGHT * 0.3)
        r41 = p41.rows_of(41)
        u41 = VGroup(under(p41.span(41, "based solely on the information provided in"), TURN),
                     under(p41.span(41, "the text chunks"), TURN))
        u47 = under(p47.span(47, "state that you don't have enough"), TURN)
        assert len(r41) == 5 and len(p47.rows_of(47)) == 3, (r41, p47.rows_of(47))

        g_frame = box(3.7, 0.6, S.GREY, dashed=True, stroke=3).move_to(GHOST_C)
        g_label = mono("SYSTEM_INSTRUCTION", 22, S.GREY).move_to(g_frame)
        ghost = VGroup(g_frame, g_label)
        gr = np.array([g_frame.get_right()[0], GHOST_C[1], 0])
        loose = curve([gr, gr + np.array([0.45, -0.03, 0]), gr + np.array([0.8, -0.25, 0]),
                       gr + np.array([0.9, -0.5, 0])], ERR)
        plug = Rectangle(width=0.2, height=0.3, stroke_color=ERR, stroke_width=3).set_fill(ERR, 0.5)
        plug.move_to(loose.get_end() + DOWN * 0.15)
        u_contents = under(p3.span(395, "contents=INPUT_PROMPT"), TURN)
        noconf = mixed(["no", "`config`"], color=ERR)
        noconf.move_to([p3.get_right()[0] + 0.3 + noconf.width / 2, code_rows(p3, 395).get_center()[1], 0])
        rm = readme_chip("README.md · line 21", "grounded in your documents")
        rm.move_to([-1.01, BAND_Y, 0])

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeIn(sys_block, shift=DOWN * 0.2), run_time=0.6)
            self.play(Indicate(sys_block, color=INK, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Line 40 defines one")
            self.add(backing, sys_block)
            self.play(FadeIn(backing), FadeOut(p3), ReplacementTransform(sys_block, VGroup(big_frame, big_label)),
                      run_time=0.7)
            self.play(FadeIn(p41, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("answer only from the chunks")
            self.play(LaggedStart(*[Create(u) for u in u41], lag_ratio=0.5), run_time=0.8)
            vo.wait_until("and say so")
            self.play(FadeIn(p47, shift=UP * 0.1), run_time=0.5)
            self.play(Create(u47), run_time=0.6)
            vo.wait_until("But look at the call")
            self.play(ReplacementTransform(VGroup(big_frame, big_label), ghost),
                      FadeOut(VGroup(p41, p47, u41, u47, backing)), FadeIn(p3), run_time=0.7)
            self.play(Indicate(code_rows(p3, 395), color=TURN, scale_factor=1.03), Create(u_contents),
                      FadeIn(noconf, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("It's never sent")
            self.play(Create(loose), FadeIn(plug), run_time=0.5)
            self.play(FadeIn(rm, shift=DOWN * 0.1), run_time=0.4)

        # ========================================================== 4 · the slip, the fix, last year's code
        cin = curve([gr, gr + np.array([0.7, 0.05, 0]), [0.4, 2.35, 0], [0.8, 2.05, 0],
                     [0.85, llm.get_top()[1], 0]], DATA)
        fix_txt = VGroup(*[mono(r, CAPTION, INK) for r in FIX_ROWS]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        fix_fr = box(fix_txt.width + 0.5, fix_txt.height + 0.3, DATA, fill=S.BG, fill_opacity=0.95, radius=0.12)
        fix = VGroup(fix_fr, fix_txt.move_to(fix_fr)).move_to([-0.2, MID_Y, 0])
        ftag = fix_tag()
        ftag.move_to([fix.get_right()[0] + 0.25 + ftag.width / 2, MID_Y, 0])
        err = erratum_tag()
        err.move_to([fix.get_left()[0] - 0.25 - err.width / 2, MID_Y, 0])
        p62 = src_panel("pipenv-branch/cli.py", 62, 64)
        at_bottom(p62, x=-6.45 + p62.width / 2)
        b64 = p62.bar(64, DATA)
        ptag = two_row_tag(["pipenv branch (March 2025)", "sent it"])
        ptag.move_to([p62.get_right()[0] + 0.3 + ptag.width / 2, p62.code.get_center()[1], 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeIn(err, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("pass it in a config argument")
            self.play(FadeOut(VGroup(loose, plug)), Create(cin), FadeIn(fix, shift=UP * 0.15), run_time=0.8)
            self.play(FadeIn(ftag, shift=LEFT * 0.15), Indicate(g_label, color=DATA, scale_factor=1.06),
                      run_time=0.6)
            vo.wait_until("The older pipenv branch")
            self.play(FadeOut(VGroup(u_contents, noconf)), ReplacementTransform(p3, p62), run_time=0.8)
            self.play(FadeIn(b64), FadeIn(ptag, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("the README's promise")
            self.play(Indicate(rm, color=TURN, scale_factor=1.05), run_time=0.8)
            vo.wait_until("rests on the chunks alone")
            self.play(Indicate(pc.cards, color=DATA, scale_factor=1.06), run_time=0.8)

        # ========================================================== 5 · the model didn't change
        lock = padlock(0.42, S.GREY)
        lock_t = label("weights unchanged", CAPTION, S.GREY)
        lock_g = VGroup(lock, lock_t).arrange(RIGHT, buff=0.15)
        lock_g.move_to([llm.get_left()[0] + lock_g.width / 2, llm.get_top()[1] + 0.2 + lock_g.height / 2, 0])
        dele = concept_tag("delete the collection")
        dele.move_to([-4.95, -0.35, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(err, fix, ftag, p62, b64, ptag, rm, ghost, cin)), run_time=0.5)
            lr = lref_swap(self, lr, "A61–A62", run_time=0.4)
            vo.wait_until("the model itself")
            self.play(Indicate(llm, color=CLOUD, scale_factor=1.08), run_time=0.7)
            vo.wait_until("No weights moved")
            self.play(FadeIn(lock_g, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Delete the collection")
            self.play(cyl.level.animate.stretch_to_fit_height(0.01, about_edge=DOWN),
                      FadeIn(dele, shift=UP * 0.1), run_time=0.9)
            cyl.remove(cyl.level)
            self.play(cyl.animate.set_stroke(opacity=0.45), run_time=0.4)
            vo.wait_until("and the knowledge is gone")
            self.play(FadeOut(back), pc.cards.animate.set_fill(S.GREY, 0.2), run_time=0.8)

        # ========================================================== 6 · steps 1 and 2: the commands
        t = term(P_CTR2, rows=3, container=True)
        mm2 = MiniMap(MINI_ABOVE_STRIP)
        nk = note("no key: both stop at cli.py · line 373, embedding the question")
        nk.move_to([-6.3 + nk.width / 2, -0.85, 0])
        gold = cost_tag("per question: one embedding call + one Gemini call")
        gold.move_to([-6.3 + gold.width / 2, -0.2, 0])
        coins = VGroup(coin_glyph(0.12).next_to(mm2.items["embedding"], RIGHT, buff=0.08).shift(UP * 0.2),
                       coin_glyph(0.12).next_to(mm2.items["llm"], UP, buff=0.08))

        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(cyl, pc, llm, mchip, l27, feed, ans, lock_g, dele, lr)), run_time=0.5)
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(mm2), tr.goto(1), run_time=0.6)
            self.play(*light_chat(mm2), run_time=0.3)
            vo.wait_until("python cli.py")
            c1 = type_cmd(self, t, CHAT1, type_time=1.6)
            assert hasattr(c1, "rows") and len(c1.rows) == 2, c1
            vo.wait_until("and for recursive split")
            self.play(tr.goto(2), run_time=0.4)
            t.clear(self, run_time=0.25)
            c2 = type_cmd(self, t, CHAT2, type_time=1.6)
            assert hasattr(c2, "rows") and len(c2.rows) == 2, c2
            vo.wait_until("Without a key")
            self.play(FadeIn(nk, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Each question costs")
            self.play(FadeIn(gold, shift=UP * 0.1), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c, scale=1.6) for c in coins], lag_ratio=0.4), run_time=0.8)

        # ========================================================== 7 · with your key, look for
        lf = LookFor([("`chat()`", "cli.py · line 365"),
                      ("`Query: How is tolminc cheese made??`", "cli.py · line 374"),
                      (mixed(["`Embedding values:`", "… 256 numbers"]), "cli.py · line 375"),
                      ("`Results:`", "cli.py · line 384"),
                      ("`10`", "cli.py · line 386"),
                      (mixed(["`INPUT_PROMPT:`", "…your chunks…"]), "cli.py · line 393"),
                      (mixed(["`LLM Response:`", "…"]), "cli.py · line 399")])
        lf.move_to([-6.3 + lf.width / 2, (t.box.get_top()[1] + 2.8) / 2, 0])
        qrow = lf.rows[1]
        qq = VGroup(*qrow[0][-2:])                       # the two question marks
        qbox = ring(qq, TURN, buff=0.05)
        etag = two_row_tag(["erratum · harmless", "the README shows one"])
        etag.move_to([lf.frame.get_right()[0] + 0.3 + etag.width / 2, qrow.get_center()[1], 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(nk, gold, mm2, coins)), FadeIn(lf.frame), FadeIn(lf.title), run_time=0.5)
            self.play(lf.write_item(0))
            vo.wait_until("look for the query")
            self.play(lf.write_item(1))
            vo.wait_until("printed with two question marks")
            self.play(Create(qbox), run_time=0.4)
            vo.wait_until("a harmless slip")
            self.play(FadeIn(etag, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("and its 256 embedding values")
            self.play(lf.write_item(2))
            vo.wait_until("Then the results")
            self.play(lf.write_item(3))
            vo.wait_until("the number 10")
            self.play(lf.write_item(4))
            vo.wait_until("the input prompt")
            self.play(lf.write_item(5))
            vo.wait_until("and the model's response")
            self.play(lf.write_item(6))

        # ========================================================== 8 · the opening question, answered
        win = chat_window("a chat with an LLM", 6.0, 2.6).move_to([-3.3, 1.5, 0])
        q = mono(QUESTION, 22, LOOKUP)
        q.move_to(win.field).align_to(win.field, LEFT).shift(RIGHT * 0.2)
        bars = VGroup(*[RoundedRectangle(width=(win.answer.width - 0.3) * k, height=0.14, corner_radius=0.07,
                                         stroke_width=0).set_fill(S.GREY, 0.8) for k in (1.0, 0.9, 0.96, 0.55)])
        bars.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        bars.move_to(win.answer).align_to(win.answer, LEFT).shift(RIGHT * 0.1)
        bars.set_stroke(ERR, 1.6, opacity=1)
        qmark = label("?", 72, TURN).move_to([1.6, 1.5, 0])
        src = VGroup(*[chunk_card(0.62, 0.36) for _ in range(4)]).arrange(DOWN, buff=0.18).move_to([1.6, 1.5, 0])
        links = VGroup()
        for b, c in ((0, 0), (1, 1), (3, 3)):
            links.add(Arrow([bars[b].get_right()[0] + 0.06, bars[b].get_center()[1], 0], src[c].get_left(), buff=0.08,
                            color=DATA, stroke_width=2.5, tip_length=0.14))
        ill = illustration_tag("a shape, not an answer")
        ill.move_to([6.45 - ill.width / 2, 2.55, 0])

        def column(head, head_col, rows, frame_col):
            items = VGroup(label(head, CAPTION + 2, head_col), *rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            fr = box(6.15, items.height + 0.5, frame_col, fill=S.BG, fill_opacity=0.95, radius=0.14)
            items.move_to(fr).align_to(fr, LEFT).shift(RIGHT * 0.3)
            g = VGroup(fr, items)
            g.frame, g.items = fr, items
            return g

        chip4 = excerpt_chip("A fictional tale", "Tolminc Cheese.txt · line 4 (excerpt)", line=STORY4)
        left = column("from your chunks", DATA, [label("Mara · her grandfather · the curd", CAPTION + 2, INK), chip4],
                      DATA)
        only3 = note("only 3 char-split chunks contain the word “Tolminc”")
        right = column("not in your chunks", ERR, [label("real-world rules for Tolminc", CAPTION + 2, INK), only3],
                       ERR)
        h = max(left.frame.height, right.frame.height)
        for g in (left, right):
            g.frame.stretch_to_fit_height(h)
            g.items.align_to(g.frame, UP).shift(DOWN * 0.25)
        cols = VGroup(left, right).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        cols.move_to([0, -0.15 - cols.height / 2, 0])
        gt_head = note("a grounding test").next_to(cols, UP, buff=0.08).align_to(cols, LEFT).shift(RIGHT * 0.12)
        cmp_note = note("compare the char-split and recursive-split answers")
        cmp_note.next_to(cols, DOWN, buff=0.18)

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(lf, qbox, etag, t)), run_time=0.5)
            self.play(FadeIn(win), FadeIn(q), FadeIn(bars), Write(qmark), run_time=0.8)
            vo.wait_until("The story is fiction")
            self.play(ReplacementTransform(qmark, src), FadeIn(ill, shift=LEFT * 0.15), run_time=0.8)
            self.play(LaggedStart(*[Create(a) for a in links], lag_ratio=0.3), run_time=0.8)
            self.play(*[bars[b].animate.set_fill(DATA, 0.85).set_stroke(DATA, 1.6) for b in (0, 1, 3)], run_time=0.5)
            vo.wait_until("an answer about Mara")
            self.play(FadeIn(gt_head), FadeIn(left.frame), FadeIn(left.items[0]), FadeIn(left.items[1]),
                      run_time=0.6)
            self.play(FadeIn(chip4, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("came from your chunks")
            self.play(Indicate(left.items[0], color=DATA, scale_factor=1.08),
                      Indicate(VGroup(*[bars[b] for b in (0, 1, 3)]), color=DATA, scale_factor=1.04), run_time=0.8)
            vo.wait_until("Real-world rules for Tolminc")
            self.play(FadeIn(right.frame), FadeIn(right.items[0]), FadeIn(right.items[1]),
                      Indicate(bars[2], color=ERR, scale_factor=1.06), run_time=0.7)
            self.play(FadeIn(only3, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Compare both chunk types")
            self.play(FadeIn(cmp_note, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 9 · step 3: the chat tool; your turn
        br = chat_window(CHAT_URL, 6.0, 2.5).move_to([-3.25, 1.5, 0])
        bq = mono(QUESTION, 22, LOOKUP)
        bq.move_to(br.field).align_to(br.field, LEFT).shift(RIGHT * 0.2)
        ill9 = illustration_tag()
        ill9.move_to([br.get_right()[0] + 0.3 + ill9.width / 2, br.get_top()[1] - 0.3, 0])
        chrome = note("use Chrome").next_to(ill9, DOWN, buff=0.25).align_to(ill9, LEFT)
        tc = turn_card([CHAT1, CHAT2, (CHAT_URL, "link · in Chrome"),
                        (Prose("your own question: cli.py · line 372 · no rebuild"), S.GREY),
                        (Prose("404 NOT_FOUND for the model? change GENERATIVE_MODEL, cli.py · line 27"), S.GREY)])
        tc.move_to([0, (br.get_bottom()[1] - 0.3 + -3.45) / 2, 0])

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(win, q, bars, src, links, ill, cols, gt_head, cmp_note)), run_time=0.5)
            self.play(tr.goto(3), FadeIn(br), FadeIn(ill9), run_time=0.6)
            self.play(FadeIn(bq), run_time=0.4)
            vo.wait_until("in Chrome")
            self.play(FadeIn(chrome, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Pause: run both chat commands")
            self.play(FadeIn(tc, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("For your own question")
            self.play(Indicate(tc.rows[3], color=TURN, scale_factor=1.04), run_time=0.9)
        self.wait(2)                                   # ▶ beat: hold the frame

        self.play(FadeOut(VGroup(tr, br, bq, ill9, chrome, tc)), run_time=0.8)
        self.wait(0.3)
