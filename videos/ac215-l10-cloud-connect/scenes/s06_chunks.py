"""S06 · Chunks for free, embeddings need a key (AC215 L10) — tracker B3 → B5 · extra;
`Lecture 10 · slides 13` during the GOLD beat only.

Beats (script.md, ## S06; one voiceover block each):
0. TRACKER B3. A 10-row terminal at laptop/24's container prompt `app@f9965bfbee29:/app$` types
   README.md line 94 (folds); --chunk / --embed / --load flash in turn, then char-split; the
   container id in the prompt is ringed ('new every run'). TERM(24: 14–17, …, 43–44; the long
   'Processing file' row soft-wraps); line 15 and lines 43–44 get YELLOW bars.
1. The GOLD beat: `this bills your project` row tag on the command line; --embed flashes GOLD; a
   GOLD meter ticks; slide 13's warning as one GOLD line; `Lecture 10 · slides 13` top right.
2. TERM(24: 115–117, …, 125, …, 165–166, …, 185; wrap): line 166 YELLOW ('Authorization' flashes,
   the Bearer part underlined BLUE), line 185 RED. The terminal shrinks to a 3-row strip under the
   V1 teaser (AuthChain(teaser=True): GREEN key slot, four hollow slots) with a GREEN '/secrets/ ·
   empty' label over the key slot; the glass finds nothing, the chain greys; the hollow slots are
   circumscribed on 'The next scene builds that chain'.
3. A GREY card `recorded · cli.py prints (231, 236, 278, 285, 160–161) + README.md:98–105`, the
   success checkpoints in the code's own words (a literal N, no counts); README.md line 94 as a
   card with the GOLD cost tag and, on 'Pause and run it', `▶ your turn`.
4. TRACKER B4: straight cut to laptop/25's prompt `app@ae87a706e772:/app$` under the GREY chip 'our
   capture: a fresh container for each command · stay in yours'; README.md line 95 typed (folds) →
   TERM(25: 14–17, …, 185; wrap), line 17 YELLOW, 185 RED, the GOLD row tag again, `▶ your turn`.
   TRACKER B5: `exit` (25: 186–187), the llm-rag laptop prompt returns, `▶ your turn`. TRACKER B5 ·
   extra: the `wc -l` count (laptop/27: 2–3), 8248 / 14228 ringed with `at the time of recording`.
   CODE(llm-rag/cli.py: 184–200, 20 pt) in two windows (184–192 with 189 cut, 193–200): line 186
   then 199–200 YELLOW; caption 'default overlap: up to 200 · cuts at paragraph and word breaks'.
5. TRACKER B5 · extra. The app mount: llm-rag/ on the laptop and /app in a TEAL container, a GREY
   tube between them (docker-compose.yml line 12, `../llm-rag:/app`) flashes on 'app mount' and the
   chunk files appear on both sides. `ls -la outputs | head -16` (laptop/26: 5–15, soft-wrapped at
   the date) → the Womans Institute rows YELLOW. The strip shrinks under an `erratum` card:
   CODE(llm-rag/cli.py: 177–178), `filename.split(".")[0]` RED, caption. Then `head -1 …` (laptop/28:
   2; wrap) with 'the book the opening question asks about'.
6. A README card (README.md · line 106) + GREY chip 'we stop it in part 2'. The running map
   (AppMap.at("S06")) over a 3-row strip: `docker ps` (laptop/22: 2–3 as STATUS · PORTS · NAMES: the
   squeezed table is 143 columns), the 8000 cell ringed GREY ('hold this for part 2' on the bar), the
   map's GREY door 8000→8000 opens; `curl -s …/version` (laptop/23: 2) → "1.0.0" with `at the time
   of recording`. A GREY note on the optional tutorial. Empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, COST, ERR, IMAGE, INK, KEY, LAPTOP, NARRATION, P_LLMRAG, SAY_COUNT, TURN,
                    AppMap, AuthChain, beside, bare_prompt, capture, cd_prompt, code, code_span, cols,
                    cost_row, cost_tag, erratum_tag, extra_row, file_glyph, flash_tag, folder_glyph,
                    grey_chip, hl_bar, istep, label, line_bar, lref, meter, meter_tick, mono, mono_line,
                    note, on_bar, out, outline_box, pin, readme, readme_card, recorded_tag, resize, ring,
                    row_tag, substring, term, time_row, track, tracker, turn_row, type_cmd, under,
                    your_turn)
from common import card as note_card
from explainer import style as S

SAY = NARRATION["S06"]
CLI = "cheese-app-v0/llm-rag/cli.py"


# ------------------------------------------------------------------ local helpers
def clear_but(scene, *keep, anims=(), run_time: float = 0.6):
    """Plays: everything on screen fades except the families of `keep` (the tracker may have been
    split into parts by track()), then `keep` is re-added whole."""
    ids = {id(f) for k in keep for f in k.get_family()}
    drop = [x for x in scene.mobjects if not any(id(f) in ids for f in x.get_family())]
    scene.play(FadeOut(Group(*drop)), *anims, run_time=run_time)
    scene.remove(*drop)
    scene.add(*keep)


def bar_rows(scene, rows, color=TURN, opacity: float = 0.25, run_time: float = 0.5):
    """Plays: a translucent bar behind each terminal row in `rows`; each bar becomes part of its
    row (inserted behind the glyphs), so it scrolls and fades with it."""
    bars = [hl_bar(r.glyphs, color, opacity) for r in rows]
    scene.play(*[FadeIn(b) for b in bars], run_time=run_time)
    for r, b in zip(rows, bars):
        scene.remove(b)
        r.submobjects.insert(0, b)
    return bars


def recolor(rows, color):
    """Animation: the glyphs of terminal rows `rows` take `color`."""
    return AnimationGroup(*[r.glyphs.animate.set_color(color) for r in rows])


def attach_mark(scene, row, mob):
    """`mob` (already on the scene) becomes part of terminal row `row`."""
    scene.remove(mob)
    row.add(mob)


def mount_picture(size: float = 24) -> VGroup:
    """The app mount (docker-compose.yml line 12, `../llm-rag:/app`): llm-rag/ > outputs/ on the
    laptop (GREY), /app/ > outputs/ in a TEAL container, a GREY tube between llm-rag/ and /app/.
    .host .cont .tube (.core .glow) .spec .files_h .files_c (built, not added)"""
    def row(name, color, depth):
        g = VGroup(folder_glyph(0.3, color), mono_line(name, size, INK)).arrange(RIGHT, buff=0.16)
        g.level = depth
        return g

    host_rows = VGroup(row("llm-rag/", LAPTOP, 0), row("outputs/", LAPTOP, 1))
    host_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    host_rows[1].shift(RIGHT * 0.45)
    host_cap = label("your laptop", 22, LAPTOP).next_to(host_rows, UP, buff=0.4, aligned_edge=LEFT)
    host = VGroup(host_cap, host_rows).move_to([-4.0, 0.7, 0])
    host.rows = host_rows

    cont_rows = VGroup(row("/app/", IMAGE, 0), row("outputs/", IMAGE, 1))
    cont_rows.arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    cont_rows[1].shift(RIGHT * 0.45)
    fr = outline_box(4.6, 2.7, IMAGE, solid=True, fill_opacity=0.05).move_to([3.7, 0.55, 0])
    title = label("container", 22, IMAGE).move_to(fr.get_corner(UL) + np.array([0.25, -0.3, 0]), aligned_edge=LEFT)
    cont_rows.move_to(fr.get_center() + np.array([0, -0.2, 0])).align_to(fr, LEFT).shift(RIGHT * 0.5)
    cont = VGroup(fr, title, cont_rows)
    cont.rows = cont_rows
    # the host rows sit at the container rows' height
    host.shift(UP * (cont_rows[0].get_y() - host_rows[0].get_y()))

    a = host_rows[0][1].get_right() + RIGHT * 0.2
    b = cont_rows[0][0].get_left() + LEFT * 0.2
    core = Line(a, np.array([b[0], a[1], 0]), color=LAPTOP, stroke_width=5)
    glow = core.copy().set_stroke(LAPTOP, 16, opacity=0.18)
    tube = VGroup(glow, core)
    tube.core, tube.glow = core, glow
    spec = VGroup(mono("../llm-rag:/app", 22, INK), note("docker-compose.yml · line 12"))
    spec.arrange(DOWN, buff=0.12).next_to(core, DOWN, buff=0.75)

    def files(rw, color):
        return VGroup(*[file_glyph(0.3, color) for _ in range(3)]).arrange(RIGHT, buff=0.12) \
            .next_to(rw, RIGHT, buff=0.3)

    g = VGroup(host, cont, tube, spec)
    g.host, g.cont, g.tube, g.spec = host, cont, tube, spec
    g.files_h, g.files_c = files(host_rows[1], LAPTOP), files(cont_rows[1], LAPTOP)
    return g


class ChunksNeedAKey(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S06"] == 7, len(SAY)
        cap24, cap25 = capture("24"), capture("25")

        # ========================================================== 0. chunk, embed, load: chunking runs
        tr = tracker("B", 3)
        p24, cmd24 = cap24.istep(12)
        assert cmd24 == readme(94), cmd24
        t = term(p24, rows=10)
        src94 = note("README.md · line 94")
        src94.move_to([t.box.get_right()[0] - src94.width / 2 - 0.1, t.box.get_top()[1] + 0.3, 0])

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), run_time=0.8)
            bare_prompt(self, t)
            ln = istep(self, t, cap24.line(12), type_time=1.6)
            r0, r1 = ln.rows
            self.play(FadeIn(src94, shift=LEFT * 0.15), run_time=0.4)
            vo.wait_until("does three jobs")
            flags = [substring(r0, "--chunk"), substring(r0, "--embed"), substring(r0, "--load")]
            self.play(LaggedStart(*[Indicate(f, color=TURN, scale_factor=1.25) for f in flags], lag_ratio=0.5),
                      run_time=1.8)
            vo.wait_until("with char split")
            self.play(Indicate(substring(r1, "char-split"), color=TURN, scale_factor=1.2), run_time=0.8)
            vo.wait_until("The ID in the prompt")
            cid = substring(r0, "f9965bfbee29")
            id_ring = ring(cid, TURN, buff=0.06)
            id_note = note("new every run", TURN).align_to(id_ring, LEFT).set_y(t.box.get_top()[1] + 0.3)
            self.play(Create(id_ring), FadeIn(id_note, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("Chunking runs for real")
            out(self, t, cap24.at((14, 17)), wrap=True)
            vo.wait_until("11 books")
            bar_rows(self, [t.find("Number of files to process: 11")])
            vo.wait_until("and the Tolminc book")
            out(self, t, cap24.at("…", (43, 44)))
            vo.wait_until("24 chunks")
            bar_rows(self, [t.find("Tolminc Cheese.txt"), t.find("Number of chunks: 24")])

        # ========================================================== 1. the GOLD beat
        ref = lref("13")
        bill = beside(cost_row(), ln)
        m_ = meter(0.7)
        warn = label("an unprotected AI endpoint invites runaway bills", 22, COST)
        gold = VGroup(m_, warn).arrange(RIGHT, buff=0.3)
        gold.move_to([-6.4 + gold.width / 2, 2.2, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(id_ring, id_note)), FadeIn(ref), run_time=0.5)
            self.remove(id_ring, id_note)
            pin(self, ln, bill)
            vo.wait_until("The embed step sends")
            self.play(Indicate(flags[1], color=COST, scale_factor=1.3), run_time=0.9)
            vo.wait_until("to Google's embedding model")
            self.play(FadeIn(m_, shift=UP * 0.1), run_time=0.5)
            self.play(meter_tick(m_, -0.7), run_time=0.8)
            vo.wait_until("about 7 million characters")
            self.play(meter_tick(m_, -0.6), run_time=0.8)
            vo.wait_until("by our estimate")
            self.play(FadeIn(warn, shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("That bills your project")
            flash_tag(self, bill, COST)
            vo.wait_until("check the current pricing page")
            self.play(Indicate(warn, color=COST, scale_factor=1.05), run_time=0.8)

        # ========================================================== 2. the embed step dies at authentication
        chain = AuthChain(teaser=True)
        chain.shift(UP * 0.75)
        k0 = chain.slots[0].frame
        empty = VGroup(folder_glyph(0.26, KEY), mono("/secrets/", 22, KEY), note("empty")).arrange(RIGHT, buff=0.15)
        empty.next_to(k0, UP, buff=0.22).align_to(k0, LEFT)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(gold, ref, src94)), run_time=0.4)
            self.remove(gold, ref, src94)
            out(self, t, cap24.at((115, 117), "…", 125), wrap=True)
            out(self, t, cap24.at("…", (165, 166)), wrap=True)
            a166 = t.find("http_request.headers['Authorization']")
            b166 = t.find("{self._access_token()}'")
            vo.wait_until("the header named Authorization")
            self.play(recolor([a166, b166], TURN), run_time=0.6)
            vo.wait_until("Despite the name")
            self.play(Indicate(substring(a166, "'Authorization'"), color=TURN, scale_factor=1.15), run_time=0.8)
            vo.wait_until("a bearer token")
            u1, u2 = under(substring(a166, "f'Bearer"), CLOUD, stroke=3), under(b166.glyphs, CLOUD, stroke=3)
            self.play(Create(u1), Create(u2), run_time=0.6)
            attach_mark(self, a166, u1)
            attach_mark(self, b166, u2)
            vo.wait_until("Default credentials error")
            out(self, t, cap24.at("…", 185), wrap=True)
            a185 = t.find("google.auth.exceptions.DefaultCredentialsError")
            b185 = t.find("/secrets/llm-service-account.json was not found.")
            self.play(recolor([a185, b185], ERR), run_time=0.5)
            vo.wait_until("the key file was not found")
            self.play(Indicate(substring(b185, "/secrets/llm-service-account.json"), color=ERR, scale_factor=1.1),
                      run_time=0.8)
            vo.wait_until("No key, no token")
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(chain, shift=UP * 0.2), FadeIn(empty), run_time=0.6)
            cross = chain.break_at(self, 0)
            vo.wait_until("The next scene builds that chain")
            self.play(Circumscribe(VGroup(*chain.slots[1:]), color=TURN, buff=0.12, stroke_width=3), run_time=1.2)

        # ========================================================== 3. what a real key gives: recorded
        rec_lines = [mono(s, 20, INK) for s in (
            "embed()",
            "Number of files to process: 11",
            "Creating collection: char-split-collection",
            "Collection 'char-split-collection' did not exist. Creating new.",
            "Finished inserting N items into collection 'char-split-collection'")]
        rec = note_card(rec_lines, size=20, buff=0.2)
        rec.move_to([0, 1.25, 0])
        for x in rec_lines:
            x.set_opacity(0)
        rec_tag = recorded_tag("recorded · cli.py prints (231, 236, 278, 285, 160–161) + README.md:98–105")
        rec_tag.next_to(rec.frame, DOWN, buff=0.15).align_to(rec.frame, RIGHT)
        c94 = readme_card(94, mono(readme(94), 22, INK)).move_to([0, -2.75, 0])
        bill3 = cost_tag().next_to(c94, UP, buff=0.18).align_to(c94, LEFT)
        yt3 = your_turn().next_to(bill3, RIGHT, buff=0.3)

        with self.voiceover(SAY[3]) as vo:
            clear_but(self, tr)
            self.play(FadeIn(rec.frame), FadeIn(rec_tag, shift=LEFT * 0.15), FadeIn(c94, shift=UP * 0.15),
                      run_time=0.6)
            self.add(rec)
            vo.wait_until("it embeds every book")
            self.play(*[x.animate.set_opacity(1) for x in rec_lines[:2]], run_time=0.6)
            vo.wait_until("creates the char split collection")
            self.play(*[x.animate.set_opacity(1) for x in rec_lines[2:4]], run_time=0.6)
            vo.wait_until("and finishes inserting")
            self.play(rec_lines[4].animate.set_opacity(1), run_time=0.5)
            self.play(Indicate(substring_text(rec_lines[4], "N"), color=INK, scale_factor=1.4), run_time=0.6)
            self.play(FadeIn(bill3, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("Pause and run it")
            self.play(FadeIn(yt3, shift=LEFT * 0.15), run_time=0.4)
            flash_tag(self, yt3, TURN)

        # ========================================================== 4. recursive split, exit, an extra count
        p25, cmd25 = cap25.istep(12)
        assert cmd25 == readme(95), cmd25
        cap27 = capture("27")
        t4 = term(p25, rows=10)
        fresh = grey_chip("our capture: a fresh container for each command · stay in yours")
        fresh.move_to([t4.box.get_left()[0] + fresh.width / 2, t4.box.get_top()[1] + 0.38, 0])
        win_a = code(CLI, 184, 192, font_size=20, cuts={189: "chunk_overlap=chunk_overlap,"})
        win_b = code(CLI, 193, 200, font_size=20)
        for w in (win_a, win_b):
            w.move_to([0, 0.35, 0])
        cap_a = label("default overlap: up to 200", 22, INK)
        cap_b = label("· cuts at paragraph and word breaks", 22, INK)
        caps = VGroup(cap_a, cap_b).arrange(RIGHT, buff=0.15).next_to(win_b, DOWN, buff=0.45)

        with self.voiceover(SAY[4]) as vo:
            clear_but(self, tr, anims=[track(tr, 4)], run_time=0.5)
            self.play(FadeIn(t4), FadeIn(fresh, shift=DOWN * 0.1), run_time=0.5)
            ln4 = istep(self, t4, cap25.line(12), type_time=1.4)
            out(self, t4, cap25.at((14, 17)), wrap=True)
            out(self, t4, cap25.at("…", 185), wrap=True)
            vo.wait_until("Pause and run it")
            r17 = t4.find("Number of chunks: 2147")
            a, b = (t4.find("google.auth.exceptions.DefaultCredentialsError"),
                    t4.find("/secrets/llm-service-account.json was not found."))
            bar_rows(self, [r17], run_time=0.4)
            self.play(recolor([a, b], ERR), run_time=0.4)
            bill4 = beside(cost_row(), ln4)
            pin(self, ln4, bill4)
            yt4 = beside(turn_row(), ln4.rows[-1], min_x=bill4.get_right()[0] + 0.25)
            pin(self, ln4, yt4)
            vo.wait_until("then type exit")
            ex = istep(self, t4, cap25.line(186), type_time=0.3)
            self.play(track(tr, 5), run_time=0.4)
            out(self, t4, cap25.at(187), run_time=0.3)
            cd_prompt(self, t4, P_LLMRAG)
            yt5 = beside(turn_row(), ex)
            pin(self, ex, yt5)
            vo.wait_until("An extra count")
            self.play(track(tr, 5, extra=True), FadeOut(fresh), run_time=0.4)
            self.remove(fresh)
            wc = type_cmd(self, t4, cap27.cmd, type_time=1.4)
            xt = beside(extra_row(), wc)
            pin(self, wc, xt)
            out(self, t4, cap27.at((2, 3)))
            r_c, r_r = t4.find("8248 total"), t4.find("14228 total")
            vo.wait_until("8,248")
            n1 = ring(substring(r_c, "8248"), TURN, buff=0.06)
            self.play(Create(n1), run_time=0.5)
            attach_mark(self, r_c, n1)
            vo.wait_until("and 14,228")
            n2 = ring(substring(r_r, "14228"), TURN, buff=0.06)
            self.play(Create(n2), run_time=0.5)
            attach_mark(self, r_r, n2)
            vo.wait_until("at the time of recording")
            tt = beside(time_row(), r_r)
            pin(self, r_r, tt)
            vo.wait_until("Recursive split makes more chunks")
            clear_but(self, tr, run_time=0.5)
            self.play(FadeIn(win_a, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(line_bar(win_a.code, 186 - 184, TURN)), run_time=0.4)
            vo.wait_until("mostly from a default overlap")
            bars_b = VGroup(line_bar(win_b.code, 199 - 193, TURN), line_bar(win_b.code, 200 - 193, TURN))
            clear_but(self, tr, anims=[FadeIn(win_b, shift=UP * 0.2)], run_time=0.6)
            self.play(FadeIn(bars_b), FadeIn(cap_a, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and it cuts at paragraph")
            self.play(FadeIn(cap_b, shift=UP * 0.1), run_time=0.5)
            self.play(Indicate(code_span(win_b.code, 6, "RecursiveCharacterTextSplitter"), color=INK,
                               scale_factor=1.06), run_time=0.8)

        # ========================================================== 5. the chunk files, a slip, a chunk
        cap26, cap28 = capture("26"), capture("28")
        pic = mount_picture()
        t5 = term(P_LLMRAG, rows=10)
        xbar = on_bar(t5, extra_row())
        err_code = code(CLI, 177, 178)
        slip = code_span(err_code.code, 1, 'filename.split(".")[0]')
        e_a = label("cut at the first dot → no author metadata", 22, INK)
        e_b = VGroup(label("fix:", 22, INK), mono("os.path.splitext", 22, INK)).arrange(RIGHT, buff=0.15)
        e_caps = VGroup(e_a, e_b).arrange(RIGHT, buff=0.3)
        e_tag = erratum_tag()
        err_card = VGroup(e_tag, err_code, e_caps).arrange(DOWN, buff=0.25)
        e_tag.align_to(err_code, RIGHT)
        err_card.move_to([0, 0.75, 0])
        book = label("the book the opening question asks about", 22, INK)

        with self.voiceover(SAY[5]) as vo:
            clear_but(self, tr, run_time=0.5)
            self.play(FadeIn(pic.host), FadeIn(pic.cont), run_time=0.6)
            self.play(Create(pic.tube), FadeIn(pic.spec), run_time=0.8)
            vo.wait_until("through the app mount")
            self.play(pic.tube.glow.animate(rate_func=there_and_back).set_stroke(width=30, opacity=0.4),
                      pic.tube.core.animate(rate_func=there_and_back).set_stroke(width=8),
                      LaggedStart(*[FadeIn(f, scale=0.6) for f in pic.files_c], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(f, scale=0.6) for f in pic.files_h], lag_ratio=0.3), run_time=1.0)
            vo.wait_until("One small slip")
            clear_but(self, tr, run_time=0.4)
            self.play(FadeIn(t5), FadeIn(xbar), run_time=0.4)
            type_cmd(self, t5, cap26.cmd, type_time=0.8)
            out(self, t5, cap26.at((5, 15)), wrap=True, run_time=1.2)
            wa = t5.find("626707 Oct 19 22:13")
            wb = t5.find("chunks-char-split-Womans Institute Library of Cookery.jsonl")
            bar_rows(self, [wa, wb], run_time=0.4)
            vo.wait_until("A book title is cut")
            self.play(Indicate(substring(wb, "Womans Institute Library of Cookery.jsonl"), color=TURN,
                               scale_factor=1.06), FadeOut(xbar), run_time=0.7)
            self.remove(xbar)
            resize(self, t5, 3, run_time=0.6)
            self.play(FadeIn(err_card, shift=UP * 0.2), run_time=0.6)
            self.play(slip.animate.set_color(ERR), Create(under(slip, ERR, stroke=3)), run_time=0.6)
            vo.wait_until("never finds them")
            flash_tag(self, e_tag, INK)
            vo.wait_until("The fix is a Python function")
            self.play(Indicate(e_b[1], color=TURN, scale_factor=1.12), run_time=0.8)
            vo.wait_until("Last, one real Tolminc chunk")
            clear_but(self, tr, t5, run_time=0.4)
            resize(self, t5, 8, run_time=0.5)
            book.move_to([0, t5.box.get_top()[1] + 0.45, 0])
            self.play(FadeIn(book, shift=DOWN * 0.1), run_time=0.4)
            hd = type_cmd(self, t5, cap28.cmd, type_time=1.0)
            xh = beside(extra_row(), hd)
            pin(self, hd, xh)
            out(self, t5, cap28.at(2), wrap=True)
            vo.wait_until("the kind of passage")
            tol = t5.find("Tolminc: A Cheese")
            self.play(Indicate(substring(tol, "Tolminc"), color=TURN, scale_factor=1.2),
                      Indicate(book, color=INK, scale_factor=1.05), run_time=0.8)
        self.wait(1.2)                                   # time to read the chunk

        # ========================================================== 6. Chroma keeps running
        cap22, cap23 = capture("22"), capture("23")
        r106_1 = label("ChromaDB keeps running after you exit the CLI container …", 24, INK)
        r106_2 = label("To stop it, run docker compose down inside llm-rag.", 24, INK)
        c106 = readme_card(106, VGroup(r106_1, r106_2).arrange(DOWN, aligned_edge=LEFT, buff=0.18))
        c106.move_to([0, 0.5, 0])
        part2 = grey_chip("we stop it in part 2").next_to(c106, DOWN, buff=0.3).align_to(c106, RIGHT)
        mp = AppMap.at("S06")
        strip = term(P_LLMRAG, rows=3)
        ps_rows = cols(cap22.at((2, 3)), ["STATUS", "PORTS", "NAMES"])
        hold = row_tag("hold this for part 2", S.GREY)
        tut = note("Optional: LLM RAG Tutorial (README.md:110–122) · L05 material · exercises.md", size=22)
        tut.move_to([0, -2.3, 0])
        part2b = grey_chip("we stop it in part 2").next_to(tut, DOWN, buff=0.25)

        with self.voiceover(SAY[6]) as vo:
            clear_but(self, tr, run_time=0.5)
            self.play(FadeIn(c106, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("keeps running after you exit")
            self.play(Indicate(r106_1, color=INK, scale_factor=1.04), FadeIn(part2, shift=LEFT * 0.15), run_time=0.8)
            vo.wait_until("and an extra docker ps")
            self.play(FadeOut(VGroup(c106, part2)), run_time=0.4)
            self.remove(c106, part2)
            self.play(FadeIn(mp, scale=1.05), FadeIn(strip, shift=UP * 0.2), run_time=0.7)
            ps = type_cmd(self, strip, cap22.cmd, type_time=0.4)
            xp = beside(extra_row(), ps)
            pin(self, ps, xp)
            out(self, strip, ps_rows, run_time=0.4)
            data = strip.find("0.0.0.0:8000->8000/tcp")
            self.play(Indicate(mp.houses["chroma"].text, color=INK, scale_factor=1.2),
                      Indicate(substring(data, "Up About a minute"), color=INK, scale_factor=1.08), run_time=0.8)
            vo.wait_until("on port 8000")
            cell = ring(substring(data, "0.0.0.0:8000->8000/tcp"), S.GREY, buff=0.06)
            on_bar(strip, hold)
            self.play(Create(cell), FadeIn(hold), mp.open_door("8000"), run_time=0.7)
            attach_mark(self, data, cell)
            self.play(Indicate(mp.doors["8000"].text, color=INK, scale_factor=1.15), run_time=0.7)
            vo.wait_until("An extra curl")
            self.play(FadeOut(hold), run_time=0.3)
            self.remove(hold)
            cu = type_cmd(self, strip, cap23.cmd, type_time=0.9)
            xc = beside(extra_row(), cu)
            pin(self, cu, xc)
            vo.wait_until("1.0.0")
            ver = out(self, strip, cap23.at(2), run_time=0.3)[0]
            tv = beside(time_row(), ver)
            pin(self, ver, tv, anim=AnimationGroup(FadeIn(tv, shift=LEFT * 0.1),
                                                   Indicate(substring(ver, '"1.0.0"'), color=INK, scale_factor=1.2)),
                run_time=0.6)
            vo.wait_until("at the time of recording")
            flash_tag(self, tv, INK)
            vo.wait_until("Stopping it comes")
            self.play(FadeOut(strip), run_time=0.4)
            self.remove(strip, *strip.get_family())
            self.play(FadeIn(tut, shift=UP * 0.1), FadeIn(part2b, shift=UP * 0.1),
                      Indicate(mp.houses["chroma"].text, color=INK, scale_factor=1.2), run_time=0.7)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)


def substring_text(m, sub: str):
    """The glyphs of `sub` in a mono() Text (spaces are dropped from its glyph list)."""
    s = m.original_text if hasattr(m, "original_text") else m.text
    i = s.index(sub)
    start = len("".join(s[:i].split()))
    return VGroup(*m[start:start + len("".join(sub.split()))])
