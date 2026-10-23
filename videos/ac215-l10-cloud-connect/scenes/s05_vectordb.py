"""S05 · A network, a compose file, a running Chroma (AC215 L10) — tracker A5 → B1 → B2,
`Lecture 10 · slides 9–10` for the whole scene. One 20 pt laptop terminal throughout (laptop/20's
sed is 201 characters with its prompt: three rows at 72 columns; at 22 pt it would need four, more
than the 3-row strip holds).

Beats (script.md, ## S05; one voiceover block each):
0. TRACKER A5. The running map (AppMap.at("S05"): drawer, two planned GREY dashed streets, hollow
   houses) over a 3-row strip at `student@laptop:~$`. README.md line 74's command types (folds);
   its two halves are ringed as the narration names them (inspect … quietly · || create);
   laptop/10: 2 prints and `cheese-app-network` turns solid PINK, no houses lit. `▶ your turn`.
1. TRACKER A5 · extra. A YELLOW '?' beside the command, held on the question; the map leaves and
   the strip grows to 9 rows; the same command again → laptop/11 (no output: the prompt returns);
   GREEN chip 'exit 0 · nothing new'. `docker network ls` → laptop/12: 2–6 (squeeze), the
   cheese-app-network row ringed PINK and its id ringed YELLOW together with laptop/10's id (one
   network). Caption 'safe to run twice' → 'idempotent'. A GREY sticky note 'inspect … || create ·
   remember this shape' rises from the command and parks in the top-right corner.
2. TRACKER B1. `cd cheese-app-v0/llm-rag` → prompt ~/cheese-app-v0/llm-rag. The strip shrinks,
   CODE(llm-rag/docker-shell.sh: 6–12, 20 pt) above it, line 7 RED. The sed of laptop/20 types
   (soft-wrapped at the edge: its one long quoted argument cannot fold at a space outside quotes;
   the rows join back to the command, asserted) with the GREY bar tag 'our editor; use yours' →
   laptop/20: 2–5 (line 4, 73 wide, cut with the house '…'), line 3 `export GCP_PROJECT="your-gcp-project"` ringed GREEN. `▶ your turn`.
3. TRACKER B2. The panel leaves, the map returns. `sh docker-shell.sh` (README.md line 88) with
   `▶ your turn` → laptop/21: 2–5 (squash), lines 3–5 ringed one by one: the llm-rag street lays
   PINK on line 4, the chroma house lights on line 5. On "Every service in this file" the map
   gives way to CODE(llm-rag/docker-compose.yml: 1–3), `llm-rag-network` ringed PINK there and in
   line 4, caption 'every service joins this network'. Then the panel leaves, the terminal grows:
   6–8 (line 7 soft-wrapped at a space), 'pull access denied' ringed GREY, GREY chip 'not on Docker
   Hub → built locally' on line 8; …, 34, …, 37–41: `x86_64` (GREY chip 'Apple Silicon: aarch64')
   and `Python 3.12.15` ringed, `at the time of recording`. The container prompt returns.
4. TRACKER B2 · extra. The strip shrinks, the map returns. At laptop/21's own prompt
   `app@3c41bc0606ad:/app$`: `ls -la /secrets` → 44–47, the file name ringed GREEN (not its size);
   the GREEN tube from the drawer into the loader draws. `echo $GOOGLE_APPLICATION_CREDENTIALS
   $GCP_PROJECT` → 49, both values ringed. The map gives way to CODE(llm-rag/docker-compose.yml:
   13–15, dedent, 20 pt), its two `$…` references YELLOW with the values, caption 'copied from the
   shell that runs compose'.
5. The terminal and panel leave (laptop/21: 50–51's `exit` is not shown). A GREY card 'one honest
   note' builds its three lines on their sentences. A small V1 outline (five hollow slots) appears;
   on "fails exactly the way a missing key fails" a RED `DefaultCredentialsError` chip flies onto its
   first, empty slot (the slot turns RED, a RED cross), GREY note 'what a missing key looks like'.
   A GREY `recorded` tag with 'a success you will see on your machine · source named' settles under
   the card. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (ERR, IMAGE, INK, KEY, NARRATION, P_LAPTOP_HOME, P_LLMRAG, PASS, ROUTE, SAY_COUNT, TURN,
                    AppMap, attach, beside, each, bare_prompt, capture, card, cd_prompt, code, code_span, cross_mark, cut,
                    editor_row, err_chip, extra_row, flash_tag, label, line_bar, lref, mono, note, on_bar, out,
                    outline_box, pin, readme, recorded_tag, resize, ring, row_tag, squash, squeeze, substring,
                    swap_tracker, term, time_row, track, tracker, turn_row, type_cmd, unpin, istep)
from explainer import style as S

SAY = NARRATION["S05"]
SIZE = 20                       # the scene's terminal: 72 columns (laptop/20's sed needs them)
SHELL = "cheese-app-v0/llm-rag/docker-shell.sh"
COMPOSE = "cheese-app-v0/llm-rag/docker-compose.yml"
NET_ID = "c0ebf9f7f30d"         # laptop/10:2's first 12 characters = laptop/12:4's NETWORK ID


def soft_type(scene, t, cmd: str, type_time: float | None = None):
    """Type a command whose long quoted argument cannot fold at a space outside quotes: it
    soft-wraps at the terminal's edge, as a terminal shows a long typed line (the rows join back
    to exactly the prompt and the command)."""
    full = t.prompt + " " + cmd
    n = t.max_chars
    rows = [full[i:i + n] for i in range(0, len(full), n)]
    assert "".join(rows) == full and all(len(r) <= n for r in rows)
    assert len(rows) <= t.rows, (len(rows), t.rows)
    t.fold = lambda text, first_prefix=0: list(rows)
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


def mark(scene, row, sub: str, color, occurrence: int = 0, run_time: float = 0.4):
    """Plays: ring `sub` in terminal row `row`; the ring is pinned (it scrolls and fades with it)."""
    rg = ring(substring(row, sub, occurrence), color)
    pin(scene, row, rg, anim=Create(rg), run_time=run_time)
    return rg


def fade_marks(scene, pinned, *loose, anims=(), run_time: float = 0.4):
    """Plays: fade pinned marks ((row, mark) pairs) and loose overlays together, then take the marks
    off their rows (a faded child left in its row would snap back when the row moves)."""
    mobs = [mk for _, mk in pinned] + list(loose)
    scene.play(FadeOut(VGroup(*mobs)), *anims, run_time=run_time)
    for row, mk in pinned:
        if mk in row.submobjects:
            row.remove(mk)
    scene.remove(*mobs)


def sticky_note() -> VGroup:
    """The GREY sticky note of the idempotent shape."""
    return card([mono("inspect … || create", 22, INK), label("remember this shape", 22, S.GREY)])


def chain_outline(slot_w: float = 1.6, slot_h: float = 0.9, gap: float = 0.45) -> VGroup:
    """A small V1 teaser: five hollow, unlabelled slots (AuthChain's hollow look) and their arrows.
    .slots .arrows"""
    xs = [(i - 2) * (slot_w + gap) for i in range(5)]
    slots = VGroup(*[outline_box(slot_w, slot_h, S.GREY_DARK, solid=False).move_to([x, 0, 0]) for x in xs])
    arrows = VGroup(*[Arrow([xs[j] + slot_w / 2 + 0.06, 0, 0], [xs[j + 1] - slot_w / 2 - 0.06, 0, 0], buff=0,
                            color=S.GREY_DARK, stroke_width=3, tip_length=0.16,
                            max_tip_length_to_length_ratio=0.5) for j in range(4)])
    g = VGroup(arrows, slots)
    g.slots, g.arrows = slots, arrows
    return g


class NetworkAndShell(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S05"] == 6, len(SAY)

        tr = tracker("A", 5)
        ref = lref("9–10")
        m = AppMap.at("S05")
        t = term(P_LAPTOP_HOME, rows=3, size=SIZE)
        net = capture("10")
        assert net.cmd == readme(74), (net.cmd, readme(74))
        assert net.at(2)[0].startswith(NET_ID)

        # ========================================================== 0. the network, README line 74
        yt0 = on_bar(t, turn_row())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), run_time=0.7)
            self.play(FadeIn(m, scale=1.1), FadeIn(t, shift=UP * 0.2), run_time=0.9)
            vo.wait_until("the Docker network")
            self.play(Indicate(m.streets["cheese-app"].text, color=INK, scale_factor=1.15), run_time=0.8)
            vo.wait_until("The README's command")
            cmd1 = type_cmd(self, t, net.cmd, type_time=1.8)
            r1a, r1b = cmd1.rows
            vo.wait_until("inspects it quietly")
            ring_a = VGroup(ring(substring(r1a, "docker network inspect cheese-app-network >/dev/null"), TURN),
                            ring(substring(r1b, "2>&1"), TURN))
            self.play(Create(ring_a), run_time=0.5)
            vo.wait_until("and creates it only if that fails")
            ring_b = ring(substring(r1b, "|| docker network create cheese-app-network"), TURN)
            self.play(ReplacementTransform(ring_a, ring_b), run_time=0.5)
            self.play(FadeOut(ring_b), run_time=0.3)
            self.remove(ring_b)
            id_row = out(self, t, net.at(2))[0]
            self.play(m.lay("cheese-app"), run_time=0.9)
            vo.wait_until("Pause and run it")
            self.play(FadeIn(yt0, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt0, TURN)

        # ========================================================== 1. extra: again, nothing new
        again, nls = capture("11"), capture("12")
        assert again.cmd == net.cmd and again.lines == [] and again.exit == 0, again.lines
        assert nls.cmd == "docker network ls"
        q = label("?", 40, TURN)
        beside(q, cmd1, buff=0.35)
        xt1 = extra_row()
        ok_chip = row_tag("exit 0 · nothing new", PASS).move_to([-3.6, 2.15, 0])
        cap1 = label("safe to run twice", 26, INK)
        cap2 = label("→ idempotent", 26, TURN)
        caps = VGroup(cap1, cap2).arrange(RIGHT, buff=0.25).next_to(ok_chip, DOWN, buff=0.35).align_to(ok_chip, LEFT)
        sticky = sticky_note()
        sticky_at = sticky.copy().move_to([6.4 - sticky.width / 2, 1.75, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(yt0), track(tr, extra=True), run_time=0.4)
            self.remove(yt0)
            pin(self, r1b, q, anim=FadeIn(q, scale=1.4))
            self.play(Indicate(q, color=TURN, scale_factor=1.25), run_time=0.8)
            self.play(FadeOut(m), run_time=0.5)
            self.remove(m)
            resize(self, t, 9)
            on_bar(t, xt1)                                   # the bar has moved: place the tag now
            self.play(FadeIn(xt1, shift=LEFT * 0.1), run_time=0.4)
            vo.wait_until("Nothing:")
            unpin(self, r1b, q)
            cmd2 = type_cmd(self, t, again.cmd, type_time=1.0)
            bare_prompt(self, t)                             # no output: the prompt returns
            self.play(FadeIn(ok_chip, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("no error")
            flash_tag(self, ok_chip, PASS)
            vo.wait_until("no second network")
            type_cmd(self, t, nls.cmd, type_time=0.5)
            out(self, t, squeeze(nls.at((2, 6))))
            row_ca = t.find("cheese-app-network  bridge")
            ring_ca = mark(self, row_ca, "cheese-app-network", ROUTE)
            id_rings = [ring(substring(row, NET_ID), TURN) for row in (id_row, row_ca)]
            self.play(*[Create(rg) for rg in id_rings], run_time=0.6)
            for rg, row in zip(id_rings, (id_row, row_ca)):
                attach(self, row, rg)
            vo.wait_until("A command that is safe to run twice")
            self.play(FadeIn(cap1, shift=RIGHT * 0.15), run_time=0.5)
            vo.wait_until("is called idempotent")
            self.play(FadeIn(cap2, shift=RIGHT * 0.15), run_time=0.5)
            self.play(Indicate(cap2, color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Remember this shape")
            sticky.move_to(VGroup(*cmd2.rows))
            self.play(FadeIn(sticky, scale=1.1), run_time=0.5)
            self.play(Transform(sticky, sticky_at), run_time=0.8)

        # ========================================================== 2. B1: edit GCP_PROJECT
        tr_b = tracker("B", 1)
        panel = code(SHELL, 6, 12, font_size=20).move_to([0, 0.75, 0])
        bar7 = line_bar(panel.code, 1, ERR, opacity=0.28)
        red7 = ring(code_span(panel.code, 1, '"ac215-project"'), ERR)
        sed = capture("20")
        assert sed.cmd.startswith("sed -i 's|export GCP_PROJECT=\"ac215-project\" # CHANGE TO YOUR PROJECT ID|")
        sed_lines = sed.at((2, 5))
        sed_lines[2] = cut(sed_lines[2], "llm-service-account")    # 20:4 is 73 wide: the house '…'
        ed = editor_row()
        yt2 = turn_row()

        with self.voiceover(SAY[2]) as vo:
            fade_marks(self, [(id_row, id_rings[0]), (row_ca, id_rings[1]), (row_ca, ring_ca)],
                       ok_chip, caps, xt1)
            tr = swap_tracker(self, tr, tr_b)
            type_cmd(self, t, "cd cheese-app-v0/llm-rag", type_time=0.6)
            cd_prompt(self, t, P_LLMRAG)
            vo.wait_until("the shell script ships")
            self.play(FadeOut(sticky), run_time=0.3)
            self.remove(sticky)
            resize(self, t, 3)
            self.play(FadeIn(panel, shift=DOWN * 0.2), run_time=0.7)
            vo.wait_until("that is not yours")
            self.play(FadeIn(bar7), Create(red7), run_time=0.6)
            vo.wait_until("Update the GCP project variable")
            soft_type(self, t, sed.cmd, type_time=2.0)
            vo.wait_until("we use the sed tool")
            on_bar(t, ed)
            self.play(FadeIn(ed, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, ed, INK)
            out(self, t, sed_lines)
            row_gp = t.find('export GCP_PROJECT="your-gcp-project"')
            mark(self, row_gp, 'export GCP_PROJECT="your-gcp-project"', PASS)
            vo.wait_until("Pause and edit it")
            yt2.next_to(ed, LEFT, buff=0.2)
            self.play(FadeIn(yt2, shift=LEFT * 0.1), run_time=0.4)
            flash_tag(self, yt2, TURN)

        # ========================================================== 3. B2: sh docker-shell.sh
        sh = capture("21")
        assert sh.cmd == readme(88) == "sh docker-shell.sh", sh.cmd
        c13 = code(COMPOSE, 1, 3).move_to([0, 1.0, 0])
        cap13 = note("every service joins this network", INK, 24).next_to(c13, DOWN, buff=0.3)
        yt3 = turn_row()
        hub = row_tag("not on Docker Hub → built locally", S.GREY)
        arm = row_tag("Apple Silicon: aarch64", S.GREY)
        tm = time_row()
        prompt43, typed43 = sh.istep(43)

        with self.voiceover(SAY[3]) as vo:
            gone2 = VGroup(panel, bar7, red7, ed, yt2)
            self.play(FadeOut(gone2), track(tr, 2), run_time=0.6)
            self.remove(gone2)
            self.play(FadeIn(m), run_time=0.7)
            vo.wait_until("Now the README's command")
            ln_sh = type_cmd(self, t, sh.cmd, type_time=0.6)
            vo.wait_until("Pause and run it")
            beside(yt3, ln_sh)
            pin(self, ln_sh, yt3)
            flash_tag(self, yt3, TURN)
            vo.wait_until("Compose pulls Chroma")
            out(self, t, squash(sh.at((2, 5))), chunk=2)
            r3, r4, r5 = t.find("chromadb/chroma:latest"), t.find("Network llm-rag-network"), \
                t.find("Container llm-rag-chromadb")
            g3 = mark(self, r3, "chromadb/chroma:latest Pulled", IMAGE)
            vo.wait_until("creates a network called")
            g4 = mark(self, r4, "Network llm-rag-network", ROUTE)
            self.play(m.lay("llm-rag"), run_time=0.9)
            vo.wait_until("and starts the database")
            g5 = mark(self, r5, "Container llm-rag-chromadb", IMAGE)
            self.play(m.light("chroma"), run_time=0.7)
            self.play(Indicate(m.houses["chroma"].text, color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("Every service in this file")
            self.play(FadeOut(m), run_time=0.5)
            self.remove(m)
            self.play(FadeIn(c13, shift=DOWN * 0.2), run_time=0.6)
            ring13 = ring(code_span(c13.code, 2, "llm-rag-network"), ROUTE)
            self.play(Create(ring13), FadeIn(cap13, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(substring(r4, "llm-rag-network"), color=ROUTE, scale_factor=1.15), run_time=0.7)
            vo.wait_until("The line that says pull access denied")
            fade_marks(self, [(r3, g3), (r4, g4), (r5, g5)], c13, ring13, cap13)
            resize(self, t, 9)
            out(self, t, sh.at((6, 8)), wrap=True)
            mark(self, t.find("pull access denied"), "pull access denied", S.GREY)
            vo.wait_until("that image is not on Docker Hub")
            r8 = t.find("Image llm-rag-cli Building")
            beside(hub, r8)
            pin(self, r8, hub)
            vo.wait_until("so Compose builds it locally")
            flash_tag(self, hub, INK)
            out(self, t, sh.at("…", 34, "…"), run_time=0.5)
            out(self, t, sh.at((37, 41)), run_time=0.8)
            vo.wait_until("The container's architecture")
            r38, r40 = t.find("Architecture: x86_64"), t.find("Python version: Python 3.12.15")
            g38 = mark(self, r38, "x86_64", INK)
            g40 = mark(self, r40, "Python 3.12.15", INK)
            beside(tm, r40)
            pin(self, r40, tm)
            vo.wait_until("Apple Silicon says")
            beside(arm, r38)
            pin(self, r38, arm)
            t.set_prompt(prompt43)
            bare_prompt(self, t)

        # ========================================================== 4. B2 · extra: inside the container
        ls_ = sh.at((44, 47))
        echo_out = sh.at(49)
        assert echo_out == ["/secrets/llm-service-account.json your-gcp-project"], echo_out
        c15 = code(COMPOSE, 13, 15, font_size=20, dedent=True).move_to([0, 1.1, 0])
        cap15 = note("copied from the shell that runs compose", INK, 24).next_to(c15, DOWN, buff=0.3)
        xt4 = extra_row()

        with self.voiceover(SAY[4]) as vo:
            fade_marks(self, [(r38, g38), (r38, arm), (r40, g40), (r40, tm)], anims=(track(tr, extra=True),))
            resize(self, t, 3)
            on_bar(t, xt4)
            self.play(FadeIn(m), FadeIn(xt4, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("Two extra checks inside")
            istep(self, t, sh.line(43), type_time=0.6)
            out(self, t, ls_)
            vo.wait_until("The key file shows up")
            row_key = t.find("llm-service-account.json")
            mark(self, row_key, "llm-service-account.json", KEY)
            vo.wait_until("through the portal")
            self.play(Indicate(m.drawer.text, color=KEY, scale_factor=1.15), run_time=0.6)
            self.play(m.tube_on("loader"), run_time=0.9)
            vo.wait_until("And both variables are set")
            istep(self, t, sh.line(48), type_time=0.9)
            row_env = out(self, t, echo_out)[0]
            g_a = mark(self, row_env, "/secrets/llm-service-account.json", TURN)
            g_b = mark(self, row_env, "your-gcp-project", TURN)
            vo.wait_until("copied by Compose")
            map_all = VGroup(m, m.tubes["loader"])
            self.play(FadeOut(map_all), run_time=0.4)
            self.remove(map_all)
            self.play(FadeIn(c15, shift=DOWN * 0.2), FadeIn(cap15, shift=UP * 0.1), run_time=0.6)
            refs = [code_span(c15.code, 1, "$GOOGLE_APPLICATION_CREDENTIALS"), code_span(c15.code, 2, "$GCP_PROJECT")]
            vo.wait_until("from the launching script")
            self.play(*[r.animate.set_color(TURN) for r in refs], run_time=0.4)
            self.play(each([refs[0], g_a, refs[1], g_b], TURN, scale=1.06, lag=0.3), run_time=1.2)
            vo.wait_until("which is why you always start there")
            self.play(Indicate(cap15, color=INK, scale_factor=1.06), run_time=0.8)

        # ========================================================== 5. an honest note
        note_card = card(["This recording machine has no Google account.",
                          "The key file in the folder listings is an obviously invalid stand-in.",
                          "It was removed before the cloud steps."], head="one honest note")
        note_card.move_to([0, 1.9, 0])
        rec = recorded_tag("recorded")
        rec_note = note("a success you will see on your machine · source named", S.GREY, 22)
        rec_row = VGroup(rec, rec_note).arrange(RIGHT, buff=0.3).next_to(note_card, DOWN, buff=0.35)
        ch = chain_outline().move_to([0, -2.1, 0])
        dce = err_chip("DefaultCredentialsError")
        dce.next_to(ch.slots[0], UP, buff=0.5).align_to(ch.slots[0], LEFT)
        dce_note = note("what a missing key looks like", S.GREY, 22).next_to(dce, RIGHT, buff=0.35)
        red0 = outline_box(ch.slots[0].width, ch.slots[0].height, ERR, solid=True, fill_opacity=0.08) \
            .move_to(ch.slots[0])
        x0 = cross_mark(0.45, ERR).move_to(ch.slots[0])
        sx = ch.slots[0].get_center()[0]
        down = Arrow([sx, dce.get_bottom()[1] - 0.04, 0], [sx, ch.slots[0].get_top()[1] + 0.04, 0], buff=0,
                     color=ERR, stroke_width=3, tip_length=0.14, max_tip_length_to_length_ratio=0.5)

        with self.voiceover(SAY[5]) as vo:
            keep = {id(f) for k in (tr, ref) for f in k.get_family()}
            gone4 = [x for x in self.mobjects if not any(id(f) in keep for f in x.get_family())]
            self.play(FadeOut(Group(*gone4)), track(tr, extra=False), run_time=0.7)
            self.remove(*gone4)
            self.add(tr, ref)
            self.play(FadeIn(note_card.frame), FadeIn(note_card.head), run_time=0.6)
            for i, anchor in enumerate(("This machine has no Google account", "The key file you just saw",
                                        "and it was removed before")):
                vo.wait_until(anchor)
                self.play(FadeIn(note_card.body[i], shift=RIGHT * 0.2), run_time=0.6)
            vo.wait_until("So from here on")
            self.play(FadeIn(ch, shift=UP * 0.2), run_time=0.7)
            vo.wait_until("fails exactly the way a missing key fails")
            self.play(FadeIn(dce, target_position=note_card.body[1].get_center(), scale=0.7), run_time=0.9)
            self.play(Create(down), Transform(ch.slots[0], red0), Create(x0), run_time=0.6)
            self.play(FadeIn(dce_note, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("so learn it on sight")
            flash_tag(self, dce, ERR)
            vo.wait_until("Every success you should expect")
            self.play(FadeIn(rec_row, shift=DOWN * 0.2), run_time=0.6)
            vo.wait_until("with its source")
            flash_tag(self, rec, INK)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
