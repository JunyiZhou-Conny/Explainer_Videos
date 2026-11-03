"""S14 · What survives: volumes now, buckets next (AC215 L10) — tracker F1 → F2, lecture_ref 40–45.

Beats (script.md, ## S14; one voiceover block each):
0. TRACKER F1 (tracker F appears); GREY `lref("40–45")` top right for the whole scene. The running
   map (AppMap.at("S14")) over a 3-row strip, 20 pt. The API terminal ('laptop · API terminal', the
   container prompt) prints `^C` and the shutdown (laptop/33: 165–170), then `exit` (33: 172 typed,
   173 printed): the API house goes dark and door 9000 bricks up. The frontend terminal ('laptop ·
   frontend terminal') prints `^C` (51: 56), then `exit` (51: 64 typed, 65 printed; the npm notice
   58–62 is not printed): the frontend house goes dark, door 3200 bricks up. `▶ your turn` on the bar;
   a GREY `--rm` chip over each dark house; `docker ps` (extra) → 46: 2–3 without CREATED/STATUS:
   only Chroma (its row ringed, its house flashes).
1. TRACKER F2. Back in the API terminal: `cd ../llm-rag` (prompt changes), `docker compose down`
   (README.md line 106), `▶ your turn` on the bar → 70: 2–9 (wrapped) in chunks while the map follows:
   'Stopped' darkens Chroma, 'Removed' takes its house and door 8000 away, 'Network … Removed' takes the
   llm-rag street (and the loader house and tube on it). The map leaves and the strip scrolls back to
   all eleven rows; the two `variable is not set` warnings turn YELLOW. The strip keeps only them
   (5 rows) under CODE(llm-rag/docker-compose.yml 13–15), `$GOOGLE_APPLICATION_CREDENTIALS` and
   `$GCP_PROJECT` YELLOW, a GREY note that llm-rag/docker-shell.sh exports both before Compose runs.
   Then the map returns over a 3-row strip: `docker ps` (extra) → 71: 2, an empty table; a GREY dashed
   empty lot where the Chroma house stood. PONDER (6 s).
2. TRACKER F2 · extra. The strip grows to 5 rows so the command stays above its output:
   `ls -la docker-volumes/chromadb` (extra) → 72: 2–5, `chroma.sqlite3` GREEN; the
   GREEN docker-volumes folder lights on the empty lot. CODE(docker-compose.yml 18–24) above the strip,
   line 24 YELLOW, its host path GREEN and `/data` TEAL. `sh docker-shell.sh` (extra) → 73: 2–4
   (squashed), …, 12; `exit` (73: 13 typed, 14 printed); `curl -s http://localhost:8000/api/v2/version`
   (extra) → 74: 2, `"1.0.0"` GREEN, caption 'same folder, served again'. On "Deleting" the strip goes
   and the map returns as the restart left it: the llm-rag street and the lit Chroma house, the folder
   in the top band (S15 recap's spot) with a GREEN dashed mount line to the house, ringed RED; below
   the map a RED trash glyph hovers over `llm-rag/docker-volumes/`, caption 'this deletes them'. On "A fresh load" CODE(llm-rag/cli.py 280–288, 20 pt), line 282
   YELLOW, line 287 GREEN, caption 'a reload deletes, then creates'.
3. TRACKER F2. Slides 40–45 redrawn: the laptop folder (docker-volumes/ > chromadb/ > chroma.sqlite3,
   caption 'a folder this laptop can see') morphs into a BLUE bucket ('a folder any authorized machine
   can see'); its contents, a folder tree with the names dataset-creator writes, melt into a flat list
   of names whose shared prefix turns YELLOW (slide 41). CODE(llm-finetuning · dataset-creator/cli.py
   276–281, the first window of 276–294) with line 279 YELLOW and the chip 'no key path: ADC again';
   the read side in GREY, CODE(mega-pipeline · transcribe_audio/cli.py 36–39). On "a storage role" the
   second window 288–294 (line 291 cut after its prefix), line 294 GREEN.
4. The IAM grid as S13 left it (tokens); the GREY Storage Admin token pulses, caption 'this is what it
   was for' and a GREY dashed 'L11' chip. Slide 45's four rules as a card (head 'slide 45 · four
   rules', GREY dashed 'L11'), rule by rule on its own sentence, the last rule GOLD with the
   GOLD-on-GREY-dashed `future_cost_tag('storage and egress bill')`. Fade to an empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer.devops import Terminal

from common import (CLOUD, COST, ERR, IMAGE, INK, KEY, LAPTOP, NARRATION, P_API, P_FRONTEND, P_LLMRAG, PASS,
                    ROUTE, SAY_COUNT, TURN, AppMap, IamGridRig, _tree, capture, card, beside, cd_prompt, code,
                    code_span, cols, dashed_chip, each, excerpt, extra_row, flash_tag, future_cost_tag,
                    grey_chip, istep, label, line_bar, lref, mono, note, on_bar, out, outline_box, ponder_card,
                    row_tag,
                    readme, resize, ring, soft, squash, substring, term, track, tracker, turn_row, type_cmd)
from explainer import style as S

SAY = NARRATION["S14"]
SIZE = 20                                   # the scene's terminals: 72 columns
T_API = "laptop · API terminal"
T_FE = "laptop · frontend terminal"
COMPOSE = "cheese-app-v0/llm-rag/docker-compose.yml"
LOADER = "cheese-app-v0/llm-rag/cli.py"
DSC = "llm-finetuning/dataset-creator/cli.py"
MEGA = "mega-pipeline/transcribe_audio/cli.py"
PREFIX = "llm-finetune-dataset-small/"      # dataset-creator/cli.py:291
FILES = ("test.jsonl", "train.jsonl")       # dataset-creator/cli.py:270, 272 (sorted, as line 286 does)

# ------------------------------------------------------------------ quoted facts (asserted)
C33, C51, C46, C70, C71, C72, C73, C74 = (capture(k) for k in ("33", "51", "46", "70", "71", "72", "73", "74"))
assert C70.cmd == "docker compose down" and "`docker compose down`" in readme(106), readme(106)
assert C72.cmd == "ls -la docker-volumes/chromadb", C72.cmd
assert C73.cmd == "sh docker-shell.sh" and C46.cmd == C71.cmd == "docker ps"
assert C74.cmd == "curl -s http://localhost:8000/api/v2/version" and C74.at(2) == ['"1.0.0"']
assert C33.at(165) == ["^C"] and C51.at(56) == ["^C"] and C33.at(173) == C51.at(65) == ["exit"]
assert C33.istep(172)[1] == C51.istep(64)[1] == C73.istep(13)[1] == "exit"
assert "chroma.sqlite3" in C72.line(5)
assert '"llm-finetune-dataset-small"' in excerpt(DSC, 291, 291)
assert all(f'"{f}"' in excerpt(DSC, 270, 272) for f in FILES)
assert "storage.Client()" in excerpt(DSC, 279, 279) and "storage.Client()" in excerpt(MEGA, 36, 36)
assert "./docker-volumes/chromadb:/data" in excerpt(COMPOSE, 24, 24)


# ------------------------------------------------------------------ local helpers
def clear_but(scene, *keep, anims=(), run_time: float = 0.6):
    """Plays: everything on screen fades except the families of `keep` (as S13's)."""
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


def ponder_at(scene, question: str, seconds: float, card_w: float, center) -> VGroup:
    """pause_and_ponder, placed; opaque so the map does not ghost through (S08 critic)."""
    pc = ponder_card(question, width=card_w).move_to(center)
    pc[0].set_fill(opacity=1)
    scene.play(FadeIn(pc, scale=0.95), run_time=0.6)
    bar = pc[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return pc


def strip(prompt: str, title: str) -> Terminal:
    return term(prompt, rows=3, title=title, size=SIZE)


def grow_back(scene, t: Terminal, earlier: list, run_time: float = 0.8):
    """Plays: terminal t scrolls back: its box grows upward (bottom fixed) and the rows that scrolled
    off (`earlier`, copies stashed when they were printed) fade back in above the rows on screen.
    The same output, shown whole: nothing is re-run."""
    rows = len(earlier) + len(t.lines)
    title = t.title.text if t.title is not None else None
    ref = Terminal(prompt=t.prompt, width=t.box.width, rows=rows, size=t.size, title=title)
    ref.shift(np.array([t.box.get_center()[0] - ref.box.get_center()[0],
                        t.box.get_bottom()[1] - ref.box.get_bottom()[1], 0]))
    order = list(earlier) + list(t.lines.submobjects)
    anims = [Transform(t.box, ref.box), Transform(t.bar, ref.bar), t.dots.animate.move_to(ref.dots)]
    if t.title is not None:
        anims.append(t.title.animate.move_to(ref.title))
    for i, ln in enumerate(order):
        ln.target_slot = ref._slot(i) - ln.strut.get_corner(UL)
    for ln in earlier:
        ln.shift(ln.target_slot)
    for ln in t.lines.submobjects:
        anims.append(ln.animate.shift(ln.target_slot))
    scene.play(*anims, LaggedStart(*[FadeIn(ln) for ln in earlier], lag_ratio=0.06), run_time=run_time)
    t.lines.remove(*t.lines.submobjects)
    t.lines.add(*order)
    t.rows = rows
    scene.add(t)
    return t


def trash_glyph(h: float = 0.55, color=ERR) -> VGroup:
    """A trash can: lid, handle, a tapered can with three ribs."""
    w = h * 0.78
    can = Polygon([-w / 2, 0, 0], [w / 2, 0, 0], [w * 0.4, -h * 0.82, 0], [-w * 0.4, -h * 0.82, 0],
                  stroke_color=color, stroke_width=3).set_fill(color, 0.15)
    lid = Line([-w * 0.62, h * 0.08, 0], [w * 0.62, h * 0.08, 0], color=color, stroke_width=4)
    handle = Line([-w * 0.18, h * 0.18, 0], [w * 0.18, h * 0.18, 0], color=color, stroke_width=4)
    ribs = VGroup(*[Line([x, -h * 0.14, 0], [x * 0.85, -h * 0.7, 0], color=color, stroke_width=2.5)
                    for x in (-w * 0.2, 0, w * 0.2)])
    return VGroup(can, lid, handle, ribs).move_to(ORIGIN)


def bucket_glyph(bw: float = 1.7, bh: float = 1.25, color=CLOUD) -> VGroup:
    """A storage bucket (BLUE): a tapered pail with a rim and a bail handle. .body"""
    body = Polygon([-bw / 2, 0, 0], [bw / 2, 0, 0], [bw * 0.38, -bh, 0], [-bw * 0.38, -bh, 0],
                   stroke_color=color, stroke_width=3).set_fill(color, 0.18)
    rim = Ellipse(width=bw, height=0.26, stroke_color=color, stroke_width=3).set_fill(color, 0.3)
    bail = Arc(radius=bw * 0.42, start_angle=0.15, angle=PI - 0.3, color=color, stroke_width=3)
    bail.move_to([0, bw * 0.22, 0])
    g = VGroup(bail, body, rim).move_to(ORIGIN)
    g.body = body
    return g


def flat_name(f: str) -> Text:
    """One object name 'llm-finetune-dataset-small/<f>' (mono, 22 pt); .prefix = the folder part."""
    t = mono(PREFIX + f, 22, INK)
    assert len(t) == len(PREFIX + f), len(t)
    t.prefix = t[:len(PREFIX)]
    return t


class WhatSurvives(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S14"] == 5, len(SAY)
        tr = tracker("F", 1)
        ref = lref("40–45")

        # ========================================================== 0. Ctrl-C + exit, twice; docker ps
        m = AppMap.at("S14")
        api_t = strip(C33.istep(172)[0], T_API)
        fe_t = strip(C51.istep(64)[0], T_FE)
        ps46 = cols(C46.at((2, 3)), ["IMAGE", "PORTS", "NAMES"])
        # row-sized chips in the band between the secrets tubes (y 2.28) and the laptop frame (2.78),
        # clear of the drawer: a house-size chip over the frontend sat on the loader's tube
        rm_chips = [row_tag([("--rm", "mono")]).move_to([x, 2.53, 0]) for x in (-1.0, 1.45)]
        assert rm_chips[0].get_right()[0] < m.drawer.get_left()[0] - 0.08
        assert rm_chips[1].get_left()[0] > m.drawer.get_right()[0] + 0.08
        yt0, xt0 = turn_row(), extra_row()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(m, scale=1.03), run_time=0.9)
            self.play(FadeIn(api_t, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("In the API and frontend terminals")
            out(self, api_t, C33.at(165), run_time=0.3)
            self.play(Indicate(api_t.find("^C").glyphs, color=TURN, scale_factor=1.4), run_time=0.5)
            out(self, api_t, C33.at((166, 170)), chunk=3, run_time=0.8)
            self.play(m.darken("api"), m.brick("9000"), run_time=0.7)
            vo.wait_until("then type exit")
            istep(self, api_t, C33.line(172), type_time=0.3)
            out(self, api_t, C33.at(173), run_time=0.3)
            api_t.set_prompt(P_API)
            self.play(FadeOut(api_t), FadeIn(fe_t), run_time=0.4)
            self.remove(api_t)
            out(self, fe_t, C51.at(56), run_time=0.3)
            self.play(m.darken("frontend"), m.brick("3200"), run_time=0.6)
            istep(self, fe_t, C51.line(64), type_time=0.3)
            out(self, fe_t, C51.at(65), run_time=0.3)
            fe_t.set_prompt(P_FRONTEND)
            vo.wait_until("Pause and do it")
            on_bar(fe_t, yt0)
            self.play(FadeIn(yt0, shift=LEFT * 0.1), run_time=0.3)
            flash_tag(self, yt0, TURN)
            vo.wait_until("Both containers ran with dash dash rm")
            self.play(LaggedStart(*[FadeIn(c, shift=DOWN * 0.1) for c in rm_chips], lag_ratio=0.3), run_time=0.6)
            vo.wait_until("so an extra docker ps")
            on_bar(fe_t, xt0)
            self.play(FadeOut(yt0), FadeIn(xt0), track(tr, extra=True), run_time=0.4)
            self.remove(yt0)
            type_cmd(self, fe_t, C46.cmd, type_time=0.4)
            out(self, fe_t, ps46, run_time=0.4)
            r46 = fe_t.find("llm-rag-chromadb")
            g46 = ring(substring(r46, "llm-rag-chromadb"), TURN, buff=0.05)
            vo.wait_until("only the database left")
            self.play(Create(g46), Indicate(m.houses["chroma"].text, color=INK, scale_factor=1.2), run_time=0.7)

        # ========================================================== 1. docker compose down; two warnings
        stash = []
        chroma_spot = m.houses["chroma"].copy()
        lot = outline_box(chroma_spot.width, chroma_spot.height, S.GREY, solid=False, fill_opacity=0)
        lot.move_to(chroma_spot)
        yt1 = turn_row()
        p13 = code(COMPOSE, 13, 15, dedent=True, font_size=20)
        place_top(p13, 1.85, 0.0)
        envs = [code_span(p13.code, 1, "$GOOGLE_APPLICATION_CREDENTIALS"), code_span(p13.code, 2, "$GCP_PROJECT")]
        why = note("llm-rag/docker-shell.sh exports both, then runs Compose (part 1)")
        why.next_to(p13, UP, buff=0.3)
        xt1 = extra_row()
        bricked = list(m.bricked.values())

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(fe_t, xt0, g46, *rm_chips)), FadeIn(api_t), track(tr, 2, extra=False),
                      run_time=0.6)
            self.remove(fe_t, xt0, g46, *rm_chips)
            type_cmd(self, api_t, "cd ../llm-rag", type_time=0.4)
            cd_prompt(self, api_t, P_LLMRAG, run_time=0.4)
            vo.wait_until("docker compose down")
            ln = type_cmd(self, api_t, C70.cmd, type_time=0.6)
            stash.append(ln.copy())
            vo.wait_until("Pause and run it")
            on_bar(api_t, yt1)
            self.play(FadeIn(yt1, shift=LEFT * 0.1), run_time=0.3)
            flash_tag(self, yt1, TURN)

            vo.wait_until("The database and its network are removed")
            rows70 = soft(C70.at((2, 9)), api_t.max_chars)
            assert len(rows70) == 11, rows70          # line 2 wraps to 3 rows, line 3 to 2
            chunks = [rows70[0:3], rows70[3:5], rows70[5:7], rows70[7:9], rows70[9:11]]
            printed = []
            for i, ch in enumerate(chunks):
                new = out(self, api_t, ch, run_time=0.45)
                printed += list(new)
                stash += [r.copy() for r in new]
                for r in new:
                    if "llm-rag-chromadb" in r.text and "Container" in r.text:
                        substring(r, "llm-rag-chromadb").set_color(IMAGE)
                    if "llm-rag-network" in r.text and "Network" in r.text:
                        substring(r, "llm-rag-network").set_color(ROUTE)
                if i == 2:      # ... Stopped
                    self.play(m.darken("chroma"), Indicate(api_t.find("Stopped").glyphs[-7:], color=IMAGE),
                              run_time=0.5)
                elif i == 3:    # ... Removed
                    gone = VGroup(m.houses["chroma"], m.doors["8000"])
                    self.play(FadeOut(gone, scale=0.8),
                              Indicate(api_t.find("Container llm-rag-chromadb Removed").glyphs[-7:], color=IMAGE),
                              run_time=0.6)
                    m.remove(*gone)
                    self.remove(*gone)
                elif i == 4:    # Network ... Removed
                    gone = VGroup(m.houses["loader"], m.tubes["loader"])
                    self.play(m.unlay("llm-rag"), FadeOut(gone),
                              Indicate(api_t.find("Network llm-rag-network Removed").glyphs[-7:], color=ROUTE),
                              run_time=0.6)
                    m.remove(m.streets["llm-rag"], *gone)
                    self.remove(m.streets["llm-rag"], *gone)
            # the stash keeps copies in the colours they were printed in; recolour like the originals
            for r in stash:
                if "Container llm-rag-chromadb" in r.text:
                    substring(r, "llm-rag-chromadb").set_color(IMAGE)
                if "Network llm-rag-network" in r.text:
                    substring(r, "llm-rag-network").set_color(ROUTE)

            vo.wait_until("Two warnings say")
            self.play(FadeOut(VGroup(m, *bricked, yt1)), run_time=0.5)
            self.remove(m, *bricked, yt1)
            on_screen = len(api_t.lines)
            grow_back(self, api_t, stash[:len(stash) - on_screen])
            warn = list(api_t.lines.submobjects[1:6])
            assert all(("variable" in w.text or "warning" in w.text or "blank" in w.text) for w in warn), \
                [w.text for w in warn]
            self.play(*[w.glyphs.animate.set_color(TURN) for w in warn], run_time=0.5)
            vns = [substring(w, "is not set") for w in warn if "is not set" in w.text]
            self.play(each(vns, TURN, scale=1.15, lag=0.3), run_time=0.8)
            vo.wait_until("because we ran this outside")
            resize(self, api_t, 5, keep=warn, run_time=0.6)
            self.play(FadeIn(p13, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("and Compose fills those blanks")
            self.play(*[e.animate.set_color(TURN) for e in envs], run_time=0.4)
            self.play(each(envs, TURN, scale=1.12, lag=0.3), run_time=0.8)
            vo.wait_until("That is the mechanism from part 1")
            self.play(FadeIn(why, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("caught in the wild")
            self.play(Indicate(why, color=INK, scale_factor=1.05), run_time=0.6)
            drop(self, p13, why, run_time=0.4)
            resize(self, api_t, 3, keep=[], extra=[FadeIn(VGroup(m, *bricked))], run_time=0.6)
            api_t.set_prompt(P_LLMRAG)
            on_bar(api_t, xt1)
            self.play(FadeIn(xt1), track(tr, extra=True), run_time=0.3)
            type_cmd(self, api_t, C71.cmd, type_time=0.3)
            out(self, api_t, C71.at(2), run_time=0.3)
            vo.wait_until("the database is gone")
            self.play(Create(lot.frame), run_time=0.6)
            vo.wait_until("are your embeddings gone too")
            self.play(Indicate(lot.frame, color=INK, scale_factor=1.08), run_time=0.6)

        pc = ponder_at(self, "After docker compose down,\nare your embeddings gone?\nWhat would make them gone?",
                       6, 8.6, [0, 0.75, 0])

        # ========================================================== 2. the folder survives; a restart; deleting
        folder = m.folder
        p18 = code(COMPOSE, 18, 24, dedent=True)
        place_top(p18, 2.72, 0.0)
        bar24 = line_bar(p18.code, 6, TURN)
        host = code_span(p18.code, 6, "./docker-volumes/chromadb")
        data = code_span(p18.code, 6, "/data")
        served = note("same folder, served again", PASS)
        xt2 = extra_row()
        # after the restart the map shows Chroma back (lit, on its street) with the folder mounted from
        # the top band, as S15's opening and recap do; the trash and its caption take the strip's place
        m_back = AppMap.at("S14")
        house2, street2 = m_back.houses["chroma"], m_back.streets["llm-rag"]
        folder_top = [-4.55 + folder.width / 2, m.header.get_center()[1], 0]      # S15 recap's spot
        mount = DashedLine(folder[0].get_bottom() + (folder_top - folder.get_center()) + DOWN * 0.04,
                           house2.roof.get_top() + UP * 0.04, color=KEY, stroke_width=3)
        del_path = mono("llm-rag/docker-volumes/", 20, ERR)
        del_cap = VGroup(del_path, note("this deletes them", ERR)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        trash = trash_glyph()
        VGroup(trash, del_cap).arrange(RIGHT, buff=0.3).move_to([-6.1, -2.35, 0], aligned_edge=LEFT)
        trash.align_to(del_path, UP).shift(UP * 0.05)          # hovering over the path
        del_ring = ring(folder, ERR).move_to(folder_top)
        p280 = code(LOADER, 280, 288, dedent=True, font_size=20)
        place_top(p280, 2.4, 0.0)
        bar282, bar287 = line_bar(p280.code, 2, TURN), line_bar(p280.code, 7, PASS, opacity=0.2)
        reload_cap = note("a reload deletes, then creates", INK, 22).next_to(p280, DOWN, buff=0.3)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(pc), run_time=0.4)
            self.remove(pc)
            vo.wait_until("An extra listing")
            # 5 rows: the command stays above its four rows (a 3-row strip scrolled it off at once); the
            # taller strip sits in front of the map's floor like a window (the browser, the loopback and
            # the public street and Google, whose lower halves it would cut, step aside until the map returns)
            bar3_y = api_t.bar.get_center()[1]
            floor = [m.browser, m.loop, m.public, m.google]
            self.bring_to_front(api_t)
            resize(self, api_t, 5, keep=0, extra=[FadeOut(xt1), FadeOut(VGroup(*floor))], run_time=0.4)
            m.remove(*floor)
            self.remove(xt1, *floor)
            on_bar(api_t, xt2)
            self.play(FadeIn(xt2), run_time=0.2)
            type_cmd(self, api_t, C72.cmd, type_time=0.5)
            out(self, api_t, C72.at((2, 5)), run_time=0.5)
            sq = substring(api_t.find("chroma.sqlite3"), "chroma.sqlite3")
            self.play(sq.animate.set_color(PASS), run_time=0.3)
            self.play(Indicate(sq, color=PASS, scale_factor=1.15), run_time=0.5)
            vo.wait_until("in a folder on your laptop")
            self.play(ReplacementTransform(lot, folder), run_time=0.7)
            self.play(Indicate(folder[1], color=KEY, scale_factor=1.1), run_time=0.6)
            vo.wait_until("mounted into the container")
            resize(self, api_t, 3, extra=[FadeOut(VGroup(m, folder, *bricked)),
                                          xt2.animate.shift(UP * (bar3_y - api_t.bar.get_center()[1]))],
                   run_time=0.5)
            self.remove(m, folder, *bricked)
            self.play(FadeIn(p18, shift=UP * 0.2), run_time=0.5)
            self.play(FadeIn(bar24), data.animate.set_color(IMAGE), host.animate.set_color(KEY), run_time=0.5)
            vo.wait_until("Containers come and go")
            self.play(Indicate(data, color=IMAGE, scale_factor=1.2), run_time=0.6)
            vo.wait_until("mounted folders stay")
            self.play(Indicate(host, color=KEY, scale_factor=1.12), run_time=0.6)
            vo.wait_until("An extra restart")
            type_cmd(self, api_t, C73.cmd, type_time=0.4)
            out(self, api_t, squash(C73.at((2, 4))) + C73.at("…", 12), chunk=3, run_time=0.7)
            istep(self, api_t, C73.line(13), type_time=0.2)
            out(self, api_t, C73.at(14), run_time=0.2)
            api_t.set_prompt(P_LLMRAG)
            type_cmd(self, api_t, C74.cmd, type_time=0.6)
            r74 = out(self, api_t, C74.at(2), color=PASS, run_time=0.3)[0]
            beside(served, r74)
            self.play(FadeIn(served, shift=LEFT * 0.15), Indicate(r74.glyphs, color=PASS, scale_factor=1.2),
                      run_time=0.6)
            vo.wait_until("Deleting the docker volumes folder")
            folder.move_to(folder_top)
            m.add(*floor)
            self.play(FadeOut(VGroup(p18, bar24, api_t, xt2, served)), FadeIn(VGroup(m, folder, *bricked)),
                      run_time=0.4)
            self.remove(p18, bar24, api_t, xt2, served)
            # the restart brought Chroma back: its street and lit house, over the same folder
            self.play(FadeIn(street2), FadeIn(house2, scale=0.85), Create(mount), run_time=0.5)
            m.add(street2, house2)
            m.streets["llm-rag"], m.houses["chroma"] = street2, house2
            self.play(FadeIn(trash, shift=DOWN * 0.2), FadeIn(del_cap, shift=LEFT * 0.15), Create(del_ring),
                      run_time=0.5)
            self.play(Wiggle(trash, scale_value=1.15), run_time=0.7)
            vo.wait_until("A fresh load")
            clear_but(self, tr, ref, run_time=0.5)
            self.play(FadeIn(p280, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("the loader deletes")
            self.play(FadeIn(bar282), Indicate(code_span(p280.code, 2, "delete_collection"), color=TURN), run_time=0.6)
            vo.wait_until("and then recreates")
            self.play(FadeIn(bar287), Indicate(code_span(p280.code, 7, "create_collection"), color=PASS),
                      FadeIn(reload_cap, shift=UP * 0.1), run_time=0.7)

        # ========================================================== 3. the cloud version: a bucket
        tree = _tree([("docker-volumes/", KEY), ("  chromadb/", KEY), ("    chroma.sqlite3", KEY)], size=22)
        tree.move_to([-3.4, 1.0, 0])
        lap_cap = note("a folder this laptop can see", LAPTOP, 22).next_to(tree, DOWN, buff=0.35)
        bk = bucket_glyph().move_to([-3.4, 1.15, 0])
        bk_name = label("bucket", 22, CLOUD).move_to(bk.body).shift(DOWN * 0.1)
        cloud_cap = note("a folder any authorized machine can see", CLOUD, 22).next_to(bk, DOWN, buff=0.35)
        bucket = VGroup(bk, bk_name)
        objs = _tree([(PREFIX, S.GREY), *[("  " + f, LAPTOP) for f in FILES]], size=22)
        objs.move_to([2.8, 1.0, 0])
        flats = VGroup(*[flat_name(f) for f in FILES]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        flats.move_to([2.6, 1.0, 0])
        src = note("names: llm-finetuning · dataset-creator/cli.py · lines 270–272, 291")
        src.move_to([0, cloud_cap.get_bottom()[1] - 0.4, 0])
        links = VGroup(*[Line(bk.get_right() + RIGHT * 0.1, f.get_left() + LEFT * 0.15, color=CLOUD, stroke_width=2)
                         for f in flats])

        w1 = code(DSC, 276, 281)
        place_top(w1, 2.72, 0.0)
        bar279 = line_bar(w1.code, 3, TURN)
        adc = grey_chip("no key path: ADC again").next_to(w1, DOWN, buff=0.15).align_to(w1, RIGHT)
        w_mega = code(MEGA, 36, 39, font_size=20)
        place_top(w_mega, adc.get_bottom()[1] - 0.2, 0.0)
        read_cap = note("read side").next_to(w_mega.header, RIGHT, buff=0.4)
        w2 = code(DSC, 288, 294, dedent=True, font_size=20, cuts={291: '"llm-finetune-dataset-small",'})
        place_top(w2, 2.72, 0.0)
        bar294 = line_bar(w2.code, 6, PASS, opacity=0.2)

        with self.voiceover(SAY[3]) as vo:
            clear_but(self, tr, ref, anims=[track(tr, extra=False)], run_time=0.5)
            self.play(FadeIn(tree, shift=UP * 0.2), FadeIn(lap_cap), run_time=0.6)
            vo.wait_until("is a storage bucket")
            self.play(FadeTransform(tree, bucket), FadeTransform(lap_cap, cloud_cap), run_time=1.0)
            self.play(Indicate(cloud_cap, color=CLOUD, scale_factor=1.05), FadeIn(objs, shift=LEFT * 0.2),
                      FadeIn(src), run_time=0.7)
            vo.wait_until("Its folders are only name prefixes")
            self.play(FadeTransform(objs, flats), run_time=0.9)
            self.play(*[f.prefix.animate.set_color(TURN) for f in flats], Create(links), run_time=0.5)
            self.play(each([f.prefix for f in flats], TURN, scale=1.08, lag=0.3), run_time=0.7)
            vo.wait_until("The storage client takes no key path")
            clear_but(self, tr, ref, anims=[FadeIn(w1, shift=UP * 0.2)], run_time=0.6)
            self.play(FadeIn(bar279), FadeIn(adc, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("so ADC finds the same key")
            self.play(Indicate(code_span(w1.code, 3, "storage.Client()"), color=TURN, scale_factor=1.12),
                      FadeIn(w_mega, shift=UP * 0.15), FadeIn(read_cap), run_time=0.7)
            vo.wait_until("and a storage role")
            self.play(FadeOut(VGroup(w1, bar279, adc, w_mega, read_cap)), FadeIn(w2, shift=UP * 0.2), run_time=0.6)
            self.remove(w1, bar279, adc, w_mega, read_cap)
            self.play(FadeIn(bar294), Indicate(code_span(w2.code, 6, "upload_from_filename"), color=PASS),
                      run_time=0.7)

        # ========================================================== 4. Storage Admin, explained; four rules
        g = IamGridRig().move_to([0, 0.7, 0])
        toks = [g.token("Owner", S.GREY, mono_font=False), g.token("roles/aiplatform.user", PASS),
                g.token("Storage Admin", S.GREY, mono_font=False)]
        toks[0].move_to(g.slot_point(0, 0))
        toks[1].move_to(g.slot_point(1, 0, 0, 2))
        toks[2].move_to(g.slot_point(1, 0, 1, 2))
        grid = VGroup(g, *toks)
        sa = toks[2]
        what = note("this is what it was for", INK, 22)
        l11 = dashed_chip("L11")
        cap4 = VGroup(what, l11).arrange(RIGHT, buff=0.35).next_to(g, DOWN, buff=0.35)
        cap4.shift(RIGHT * (sa.get_center()[0] - what.get_center()[0]))
        cap4.shift(RIGHT * max(0, -6.4 - cap4.get_left()[0]))

        rules = ["Storage Object Admin over Storage Admin", "keep buckets private",
                 "prefix the globally unique name"]
        rows = [VGroup(label(f"{i + 1}.", 26, S.GREY), label(r, 26, INK)).arrange(RIGHT, buff=0.2)
                for i, r in enumerate(rules)]
        last = VGroup(label("4.", 26, S.GREY), label("delete what you don't need", 26, COST),
                      future_cost_tag("storage and egress bill")).arrange(RIGHT, buff=0.25)
        rows.append(last)
        rc = card(rows, size=26, head="slide 45 · four rules", buff=0.3,
                  card_w=max(r.width for r in rows) + 1.0)
        rc.move_to([0, -0.1, 0])
        l11b = dashed_chip("L11").next_to(rc.frame, UP, buff=0.12).align_to(rc.frame, RIGHT)

        with self.voiceover(SAY[4]) as vo:
            clear_but(self, tr, ref, anims=[FadeIn(grid, scale=1.03)], run_time=0.7)
            vo.wait_until("which is why Storage Admin sat gray")
            self.play(Indicate(sa.text, color=INK, scale_factor=1.2), run_time=0.8)
            self.play(sa.animate(rate_func=there_and_back).scale(1.15), FadeIn(what, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("next lecture uses one")
            self.play(FadeIn(l11, shift=LEFT * 0.15), run_time=0.4)
            self.play(Indicate(l11.text, color=INK, scale_factor=1.15), run_time=0.5)
            vo.wait_until("The lecture gives four rules")
            clear_but(self, tr, ref, anims=[FadeIn(rc.frame), FadeIn(rc.head), FadeIn(l11b)], run_time=0.6)
            for r, anchor in zip(rows, ("Grant object admin", "Keep buckets private", "Prefix their globally",
                                        "And delete what you no longer need")):
                vo.wait_until(anchor)
                self.play(FadeIn(r, shift=RIGHT * 0.25), run_time=0.5)
            vo.wait_until("because storage and downloads cost money")
            flash_tag(self, last[2], COST)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
