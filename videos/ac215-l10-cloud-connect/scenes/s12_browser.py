"""S12 · The browser is the integrator (AC215 L10) — tracker E1 → E3; `lref("11, 13")` on the
closing beat only (CORS itself is tutorial-only).

Beats (script.md, ## S12; one voiceover block each):
0. TRACKER E1 (tracker E appears). CODE(frontend-ai-chatbot/.env.development: 1–4), line 4 YELLOW;
   CODE(src/services/Common.js: 1–2) below it. Under the panels: the TEAL frontend house, a JavaScript
   bundle and your browser on the laptop floor; the address `http://localhost:9000` leaves the
   container inside the bundle, which flies to the browser. A GREEN check on `localhost:9000`; the
   API's container name struck RED ("never a container name").
1. TRACKER E1: a schematic browser at `localhost:3200/chunkviz` (`illustration`): book text splits into
   coloured chunks inside the window; GREY note 'no API · no cloud · no bill'. A 6-row strip (extra),
   in with the browser, types laptop/56's curl → 56:2–3 (on screen until "Step 2"). `▶ your turn`. TRACKER E2: the browser at
   `localhost:3200/chromaui` (`illustration`), the form's three defaults from
   CODE(src/app/chromaui/page.jsx: 22–27); "Connect" sends a PINK arrow to door :8000. The strip
   (extra) types laptop/63's curl (wrapped at a '/') → `[]`, caption 'ours: empty (no key in our capture)'; the panel gives way
   to a GREY card tagged `recorded · README.md:103, 206`. `▶ your turn`.
2. TRACKER E3. The /chat page (`illustration`, picker `char-split-collection ▾`), the README's
   question types in; GOLD cost tag 'each question: 1 embedding + 1 generation'; `▶ your turn`.
   Then V5 (CorsBouncer) under one GREY tag `recorded · README.md:217–222 · ChatComponent.jsx:161–173`
   (until block 5), CODE(ChatComponent.jsx: 163) under it: three call badges, then packet ①
   to door :9000, the BLUE ticket to Google and 256 bars back.
3. (a) Packet ② `POST :8000/…/collections/<id>/query` (ChatComponent.jsx · line 164) with
   CODE(src/services/DataService.js: 34–43), line 36 `"n_results": 10` YELLOW; the panel clears.
   (b) The origin card alone: three origins, scheme + host + port.
4. The rule card (no code panel), then V5 again: the OPTIONS preflight with the page's Origin
   stamp, Chroma's guest list (it never moves), a pass back to the bouncer, packet ② admitted, ten
   chunk cards back.
5. Packet ③ to :9000; the answer frame returns (GREY skeleton bars, no text). The recorded tag
   fades. A 15-row terminal (extra) types laptop/60's preflight → 60:2, 6 (6 GREEN, 'the pass'; the
   typed Origin header ringed GREY, 'curl writes its own'), then laptop/61's → 61:2–5, a RED dashed
   gap where the pass stood ('no pass'), 61:6; both 200 OK rows ringed GREY. Then the second terminal
   (extra) types laptop/38's preflight → 38:2, 6 (`access-control-allow-origin: *`) under
   CODE(api-service/api/service.py: 13–20, 20 pt), `allow_origins=["*"]` ringed.
6. PacketReplay: the page is restamped :3300; a fresh packet with a ':3300' stamp; both doors pulse.
   PONDER (8 s), opaque card over the picture.
7. The :3300 replay, step by step: ① GREEN at the API's '*'; ② the OPTIONS knock returns nothing,
   the bouncer stops ② RED; ③ GREY dashed 'awaits call 2 · ChatComponent.jsx:163–171'; the curl
   figure walks to door 8000 and gets an answer; last chip '127.0.0.1:3200 ≠ localhost:3200'.
8. lref top right. The /chat wireframe (`illustration`): picker, five GREY skeleton bars, the
   'References' drawer with ten empty rows under 'book · author · dist'; caption 'what to look for ·
   README.md · lines 217–222'. Closing: the map (AppMap.at("S12")), door :9000 neutral GREY with a
   GOLD meter beside it; slide 13's warning card 'an unprotected AI endpoint'. Fade to empty.

Deviations / local workarounds:
- `.env.development` is not in assets/source (the repo's `.gitignore` has `.env.*`): `env_panel()`
  uses code() when the file is there and otherwise the same four lines quoted from the upstream
  checkout (cheese-app-v0 cb6fb94, identical text), built with the same code_panel.
- Terminal.fold hard-breaks a URL longer than a row with ' \\' (and drops a character): the long
  curls of 60/61/63 are typed with explicit rows (fold at option boundaries, the URL soft-wrapped at
  the terminal edge), asserted to join back to the exact command.
- CODE(ChatComponent.jsx: 161–173) is 13 lines and does not fit beside the 12.8-wide V5: block 2
  shows line 163 (call ①) under the picture, block 3 names line 164, block 5 lines 165–171.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene
from explainer.components import ponder_card
from explainer.devops import code_panel

from common import (CONTAINERS, COST, ERR, IMAGE, INK, LAPTOP, MONO, NARRATION, P_API, P_LAPTOP_HOME, PASS,
                    QUESTION, ROUTE, SAY_COUNT, T_SECOND, TURN, AppMap, ChatWireframe, CorsBouncer,
                    PacketReplay, EmbeddingBars, beside, browser_glyph, capture, card, check_mark, chip, code,
                    code_span, cost_tag, each, extra_row, flash_tag, house, illustration_tag, label, line_bar,
                    lref, meter, meter_tick, mono, note, on_bar, out, pin, readme, recorded_tag, ring,
                    route, step_badge, strike, substring, term, track, tracker, turn_row, type_cmd, unpin,
                    your_turn, cut, excerpt, file_glyph, outline_box, door_glyph)
from explainer import style as S

SAY = NARRATION["S12"]
SIZE = 20                      # the scene's terminals: 72 columns
FRONT = "cheese-app-v0/frontend-ai-chatbot"
CHAT = f"{FRONT}/src/components/chat/ChatComponent.jsx"
PONDER_4 = ("You republish the frontend at -p 3300:3000\nand ask a question. Which of the three calls\n"
            "fails, and does curl care?")
# cheese-app-v0 @ cb6fb94, frontend-ai-chatbot/.env.development lines 1–4 (gitignored in assets/source)
ENV_DEV = ("REACT_APP_BASE_API_URL=http://localhost:9000\nCHOKIDAR_USEPOLLING=true\nPORT=3000\n"
           "NEXT_PUBLIC_BASE_API_URL=http://localhost:9000")


# ------------------------------------------------------------------ local helpers
def clear_but(scene, *keep, anims=(), run_time: float = 0.6):
    """Plays: everything on screen fades except the families of `keep` (the tracker may have been
    split into parts by track()), then `keep` is re-added whole. Same as S09/S11's."""
    ids = {id(f) for k in keep for f in k.get_family()}
    gone = [x for x in scene.mobjects if not any(id(f) in ids for f in x.get_family())]
    scene.play(FadeOut(Group(*gone)), *anims, run_time=run_time)
    scene.remove(*gone)
    scene.add(*keep)


def drop(scene, *mobs, anims=(), run_time: float = 0.3):
    """Plays: free overlays fade and leave the scene."""
    scene.play(FadeOut(VGroup(*mobs)), *anims, run_time=run_time)
    scene.remove(*mobs)


def env_panel():
    """CODE(frontend-ai-chatbot/.env.development: 1–4) — from assets/source when present."""
    try:
        return code(f"{FRONT}/.env.development", 1, 4)
    except FileNotFoundError:
        return code_panel(ENV_DEV, "frontend-ai-chatbot/.env.development", 1, "bash", font_size=22)


def type_rows(scene, t, cmd: str, rows: list[str], type_time: float | None = None):
    """Type `cmd` shown as explicit rows: rows ending ' \\' continue on a 4-space indented row (a
    fold), any other row break is the terminal's soft wrap. Asserted to join back to the prompt and
    the exact command."""
    full = t.prompt + " " + cmd
    joined = rows[0]
    for prev, r in zip(rows, rows[1:]):
        if prev.endswith(" \\"):
            assert r.startswith("    "), r
            joined = joined[:-2] + " " + r[4:]
        else:
            joined += r
    assert joined == full, (joined, full)
    assert all(len(r) <= t.max_chars for r in rows), [len(r) for r in rows]
    t.fold = lambda text, first_prefix=0: list(rows)
    try:
        return type_cmd(scene, t, cmd, type_time)
    finally:
        del t.fold


def preflight_rows(t, cmd: str) -> list[str]:
    """laptop/60, 61: fold before each -H and before the URL; the URL soft-wraps at the edge."""
    a, rest = cmd.split(" -H ", 1)
    h1, rest = rest.split(" -H ", 1)
    h2, url = rest.rsplit(" ", 1)
    rows = [f"{t.prompt} {a} \\", f"    -H {h1} \\", f"    -H {h2} \\"]
    last = "    " + url
    n = t.max_chars
    rows += [last[i:i + n] for i in range(0, len(last), n)]
    return rows


def ponder_at(scene, question: str, seconds: float, card_w: float, center) -> VGroup:
    """pause_and_ponder, placed; opaque so the picture does not ghost through (S08 critic)."""
    pc = ponder_card(question, width=card_w).move_to(center)
    pc[0].set_fill(opacity=1)
    scene.play(FadeIn(pc, scale=0.95), run_time=0.6)
    bar = pc[3]
    target = bar.copy().scale(0.001, about_point=bar.get_start())
    scene.play(bar.animate(rate_func=linear).become(target), run_time=seconds)
    return pc


def bundle_glyph() -> VGroup:
    """The JavaScript bundle the browser downloads: a GREY file with its name."""
    g = file_glyph(0.5, LAPTOP)
    t = label("JavaScript", SIZE, LAPTOP).next_to(g, DOWN, buff=0.1)
    out_ = VGroup(g, t)
    out_.glyph, out_.text = g, t
    return out_


def chunk_page(br) -> VGroup:
    """Inside a browser window: rows of book text as GREY bars (no glyphs)."""
    w = br.window[0]
    x0, x1 = w.get_left()[0] + 0.4, w.get_right()[0] - 0.4
    top = br.url.get_bottom()[1] - 0.3
    rows = VGroup()
    for i in range(4):
        rows.add(Rectangle(width=(x1 - x0) * (1.0 if i < 3 else 0.55), height=0.16, stroke_width=0)
                 .set_fill(S.GREY, 0.45))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([x0, top, 0], aligned_edge=UL)
    assert rows.get_bottom()[1] > br.window[0].get_bottom()[1] + 0.1, "chunk rows leave the window"
    return rows


def chunk_split(rows) -> VGroup:
    """The same rows cut into coloured chunks (alternating; a gap between chunks)."""
    cols = (S.TEAL, S.BLUE, S.PURPLE)
    out_ = VGroup()
    k = 0
    for r in rows:
        w = r.width
        cuts = (0.0, 0.31, 0.62, 1.0) if r.width > 3 else (0.0, 0.5, 1.0)
        for a, b in zip(cuts, cuts[1:]):
            seg = Rectangle(width=w * (b - a) - 0.06, height=r.height, stroke_width=0)
            seg.set_fill(cols[k % 3], 0.55).move_to(r.get_left() + RIGHT * (w * (a + b) / 2))
            out_.add(seg)
            k += 1
    return out_


def form_row(br, values) -> VGroup:
    """The chromaui form inside a browser window: three fields (the defaults) and a Connect button."""
    fields = VGroup()
    for v in values:
        t = mono(v, SIZE, INK)
        fr = RoundedRectangle(width=t.width + 0.3, height=t.height + 0.26, corner_radius=0.06,
                              stroke_color=S.GREY, stroke_width=2).set_fill(S.GREY_DARKER, 1)
        t.move_to(fr)
        f = VGroup(fr, t)
        f.text = t
        fields.add(f)
    btn_t = label("Connect", SIZE, INK)
    btn = RoundedRectangle(width=btn_t.width + 0.34, height=btn_t.height + 0.26, corner_radius=0.08,
                           stroke_color=ROUTE, stroke_width=2.5).set_fill(ROUTE, 0.18)
    button = VGroup(btn, btn_t.move_to(btn))
    fields.arrange(RIGHT, buff=0.2)
    button.next_to(fields, DOWN, buff=0.18).align_to(fields, RIGHT)
    row = VGroup(*fields, button)
    row.next_to(br.url, DOWN, buff=0.22).set_x(br.window[0].get_center()[0])
    w = br.window[0]
    assert w.get_left()[0] < row.get_left()[0] and row.get_right()[0] < w.get_right()[0], "form leaves the window"
    assert row.get_bottom()[1] > w.get_bottom()[1], "form leaves the window" 
    row.fields, row.button = fields, button
    return row


class BrowserIntegrator(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S12"] == 9, len(SAY)

        # ========================================================== 0. E1 · the address baked into JS
        tr = tracker("E", 1)
        env = env_panel()
        env.move_to([0, 0, 0]).align_to([0, 2.78, 0], UP)
        com = code(f"{FRONT}/src/services/Common.js", 1, 2)
        com.next_to(env, DOWN, buff=0.18)
        assert excerpt(f"{FRONT}/src/services/Common.js", 2, 2).endswith("process.env.NEXT_PUBLIC_BASE_API_URL;")
        addr = code_span(env.code, 3, "http://localhost:9000")
        bar4 = line_bar(env.code, 3, TURN)
        y_pic = (com.get_bottom()[1] - 3.5) / 2 - 0.05
        fh = house("frontend", 1.6, 0.8, lit=True).move_to([-4.6, y_pic - 0.55, 0], aligned_edge=DOWN)
        bun = bundle_glyph().move_to([-0.6, y_pic, 0])
        br0 = browser_glyph(name="your browser", glyph_w=1.4).move_to([5.0, y_pic + 0.1, 0])
        floor = Line([3.4, y_pic - 0.62, 0], [6.4, y_pic - 0.62, 0], color=LAPTOP, stroke_width=3)
        floor_t = note("your laptop", LAPTOP).next_to(floor, DOWN, buff=0.08).align_to(floor, RIGHT)
        chip_addr = chip("http://localhost:9000", S.GREY, size=SIZE, font=MONO)
        ok0 = check_mark(0.3, PASS)
        bad = chip(CONTAINERS["api"], ERR, size=SIZE, font=MONO, fill_opacity=0.12)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(env, shift=DOWN * 0.15), run_time=0.7)
            self.play(FadeIn(com, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(bar4), Indicate(addr, color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("baked into the JavaScript")
            self.play(FadeIn(fh), FadeIn(floor), FadeIn(floor_t), FadeIn(br0), run_time=0.5)
            chip_addr.move_to(addr)
            self.play(FadeIn(chip_addr), run_time=0.3)
            self.play(chip_addr.animate.next_to(fh, RIGHT, buff=0.2).shift(UP * 0.55), run_time=0.7)
            self.play(FadeIn(bun, shift=RIGHT * 0.2),
                      chip_addr.animate.next_to(bun.glyph, UP, buff=0.12), run_time=0.6)
            ride = VGroup(bun, chip_addr)
            self.play(ride.animate.next_to(br0.window, LEFT, buff=0.25), run_time=0.9)
            vo.wait_until("gives the page the API's address")
            self.play(Indicate(code_span(com.code, 1, "NEXT_PUBLIC_BASE_API_URL"), color=TURN, scale_factor=1.08),
                      FadeOut(bun), chip_addr.animate.next_to(br0.window, LEFT, buff=0.2), run_time=0.8)
            self.remove(bun)
            vo.wait_until("So it must be one your browser can reach")
            ok0.next_to(chip_addr, UP, buff=0.12)
            self.play(Indicate(br0.text, color=INK, scale_factor=1.15), Create(ok0), run_time=0.8)
            vo.wait_until("never a container name")
            bad.next_to(fh, UP, buff=0.1).align_to(fh, LEFT)
            x_bad = strike(bad, ERR)
            self.play(FadeIn(bad, shift=UP * 0.1), run_time=0.4)
            self.play(Create(x_bad), run_time=0.5)

        # ========================================================== 1. E1 chunkviz · E2 chromaui
        c56, c63 = capture("56"), capture("63")
        assert c56.cmd.startswith("curl -s --max-time 300 -o /tmp/l10-chunkviz.html"), c56.cmd
        assert c63.cmd == ("curl -s http://localhost:8000/api/v2/tenants/default_tenant/databases/"
                           "default_database/collections"), c63.cmd
        # laptop/56 folds to 4 rows + 2 output rows: a 6-row strip (QA 22:29), so the browser sits
        # higher and shorter, its name right of the window instead of under it
        strip = term(P_LAPTOP_HOME, rows=6, size=SIZE)
        strip2 = term(P_LAPTOP_HOME, rows=3, size=SIZE)
        brc = browser_glyph(url="localhost:3200/chunkviz", glyph_w=7.6, glyph_h=2.1, name="your browser")
        brc.shift([-2.1 - brc.window.get_center()[0], 2.3 - brc.window.get_top()[1], 0])
        brc.text.next_to(brc.window, RIGHT, buff=0.3).align_to(brc.window, DOWN)
        ill1 = illustration_tag().next_to(brc.window, UP, buff=0.1).align_to(brc.window, RIGHT)
        text_rows = chunk_page(brc)
        chunks = chunk_split(text_rows)
        local = note("no API · no cloud · no bill", LAPTOP).next_to(brc.window, RIGHT, buff=0.3)
        local.align_to(brc.window, UP).shift(DOWN * 0.3)
        yt1 = your_turn().next_to(local, DOWN, buff=0.3).align_to(local, LEFT)
        assert brc.window.get_bottom()[1] > strip.get_top()[1] + 0.2, "browser on the strip"
        xt1 = extra_row()

        # E2: the chromaui page
        pg = code(f"{FRONT}/src/app/chromaui/page.jsx", 22, 27, font_size=SIZE).move_to([0, 0, 0])
        pg.align_to([0, 2.78, 0], UP).align_to([-6.45, 0, 0], LEFT)
        vals = ("http://localhost:8000", "default_tenant", "default_database")
        spans = [code_span(pg.code, 2 + i, f"'{v}'") for i, v in enumerate(vals)]
        brd = browser_glyph(url="localhost:3200/chromaui", glyph_w=10.3, glyph_h=2.2, name=None)
        brd.move_to([-1.2, pg.get_bottom()[1] - 0.2 - 1.1, 0])
        form = form_row(brd, vals)
        ill2 = illustration_tag().next_to(brd.window, RIGHT, buff=0.15).align_to(brd.window, UP)
        door_box = door_glyph()
        d8 = VGroup(door_box, mono(":8000", SIZE, S.GREY).next_to(door_box, DOWN, buff=0.08))
        d8.move_to([5.4, 0, 0]).align_to(form.button, DOWN)
        conn = route(form.button.get_right() + RIGHT * 0.08, door_box.get_left() + LEFT * 0.06)
        yt2 = your_turn()
        xt2 = extra_row()
        rec2 = recorded_tag("recorded · README.md:103, 206")
        coll = card([mono("char-split-collection", SIZE, INK), mono("recursive-split-collection", SIZE, INK)],
                    size=SIZE)
        assert "char-split-collection" in readme(103) and "recursive-split-collection" in readme(206)

        with self.voiceover(SAY[1]) as vo:
            clear_but(self, tr, run_time=0.6)
            on_bar(strip, xt1)
            self.play(FadeIn(brc, shift=UP * 0.15), FadeIn(ill1), FadeIn(text_rows),
                      FadeIn(strip, shift=UP * 0.2), FadeIn(xt1), track(tr, extra=True), run_time=0.7)
            type_cmd(self, strip, c56.cmd, type_time=0.8)
            out(self, strip, c56.at((2, 3)), color=PASS, run_time=0.4)
            vo.wait_until("text chunking")
            self.play(ReplacementTransform(text_rows, chunks), run_time=1.0)
            vo.wait_until("runs in your browser")
            self.play(Indicate(brc.text, color=LAPTOP, scale_factor=1.15), FadeIn(local, shift=LEFT * 0.15),
                      FadeIn(yt1, shift=LEFT * 0.15), run_time=0.7)
            vo.wait_until("Step 2, the database UI")
            clear_but(self, tr, anims=[track(tr, 2, extra=False)], run_time=0.5)
            self.play(FadeIn(pg, shift=DOWN * 0.15), FadeIn(brd, shift=UP * 0.15), FadeIn(ill2),
                      *[FadeIn(f[0]) for f in form.fields], FadeIn(form.button), run_time=0.6)
            self.play(LaggedStart(*[TransformFromCopy(s, f.text) for s, f in zip(spans, form.fields)],
                                  lag_ratio=0.25), run_time=1.0)
            vo.wait_until("connects to localhost 8000")
            self.play(FadeIn(d8), Indicate(form.button[1], color=ROUTE, scale_factor=1.15), run_time=0.5)
            self.play(Create(conn), run_time=0.6)
            self.play(Indicate(d8[1], color=INK, scale_factor=1.2), run_time=0.5)
            vo.wait_until("Pause and try both")
            yt2.next_to(d8, DOWN, buff=0.2).align_to(d8, RIGHT)
            self.play(FadeIn(yt2, shift=DOWN * 0.1), run_time=0.3)
            flash_tag(self, yt2, TURN)
            vo.wait_until("Our extra listing is empty")
            on_bar(strip2, xt2)
            self.play(FadeOut(pg), run_time=0.3)
            self.remove(pg)
            self.play(VGroup(brd, form, d8, conn, yt2, ill2).animate.shift(UP * 1.35), FadeIn(strip2, shift=UP * 0.2),
                      FadeIn(xt2), track(tr, extra=True), run_time=0.6)
            # the URL (90 chars) cannot fit one 72-column row even folded: break at a '/' (QA 22:37)
            cut63 = "/api/v2/tenants/"
            r1 = f"{strip2.prompt} {c63.cmd[:c63.cmd.index(cut63) + len(cut63)]}"
            type_rows(self, strip2, c63.cmd, [r1, c63.cmd[len(r1) - len(strip2.prompt) - 1:]], type_time=0.7)
            r63 = out(self, strip2, c63.at(2), run_time=0.3)[0]
            empty = note("ours: empty (no key in our capture)", S.GREY, SIZE)
            beside(empty, r63)
            pin(self, r63, empty)
            vo.wait_until("yours shows two collections")
            coll.move_to([6.5 - coll.width / 2, 2.25, 0])
            rec2.next_to(coll, UP, buff=0.12).align_to(coll, RIGHT)
            self.play(FadeIn(coll, shift=DOWN * 0.15), FadeIn(rec2), run_time=0.6)
            self.play(each(list(coll.body), INK, scale=1.08, lag=0.3), run_time=0.8)

        # ========================================================== 2. E3 · chat; V5; call ①
        cw = ChatWireframe(picker="char-split-collection ▾", win_h=5.0).move_to([0, 0.1, 0])
        ill3 = illustration_tag().next_to(cw.window, UP, buff=0.1).align_to(cw.window, RIGHT)
        bill = cost_tag("each question: 1 embedding + 1 generation")
        yt3 = your_turn()
        VGroup(bill, yt3).arrange(RIGHT, buff=0.5).move_to([0, -3.08, 0])
        cb = CorsBouncer().move_to([0, 0.4, 0])
        rec = recorded_tag("recorded · README.md:217–222 · ChatComponent.jsx:161–173")
        rec.move_to([6.55 - rec.width / 2, 3.3, 0])
        c163 = code(CHAT, 163, 163, dedent=True, font_size=SIZE).move_to([0, -2.55, 0])
        badges = VGroup(*[step_badge(k, ROUTE) for k in (1, 2, 3)]).arrange(DOWN, buff=0.12)
        badges.next_to(cb.page.window, RIGHT, buff=0.25)

        with self.voiceover(SAY[2]) as vo:
            clear_but(self, tr, anims=[track(tr, 3, extra=False)], run_time=0.6)
            self.play(FadeIn(cw.shell, shift=UP * 0.15), FadeIn(ill3), run_time=0.7)
            vo.wait_until("has a gold tag")
            self.play(FadeIn(bill, shift=UP * 0.15), run_time=0.4)
            flash_tag(self, bill, COST)
            vo.wait_until("Pause, pick a collection")
            self.play(Indicate(cw.picker.text, color=TURN, scale_factor=1.1), FadeIn(yt3, shift=LEFT * 0.1),
                      run_time=0.6)
            self.play(cw.type_question(1.2))
            vo.wait_until("On your machine")
            clear_but(self, tr, run_time=0.5)
            self.play(FadeIn(cb, scale=0.97), FadeIn(rec), run_time=0.7)
            vo.wait_until("it makes three calls")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in badges], lag_ratio=0.3), run_time=0.8)
            vo.wait_until("Call one")
            self.play(FadeOut(badges), FadeIn(c163, shift=UP * 0.15), run_time=0.4)
            self.remove(badges)
            p1 = cb.send(self, 1, run_time=0.8)
            self.play(FadeIn(line_bar(c163.code, 0, ROUTE)), run_time=0.3)
            vo.wait_until("the API asks Google")
            bars = cb.cloud(self, run_time=0.9)
            vo.wait_until("256 numbers come back")
            n256 = note("256 numbers", S.BLUE).next_to(bars, DOWN, buff=0.12)
            self.play(FadeIn(n256), Indicate(bars, color=S.BLUE, scale_factor=1.1), run_time=0.7)

        # ========================================================== 3. call ② · three origins
        c_q = mono("POST :8000/…/collections/<id>/query", 22, ROUTE)
        p2 = step_badge(2, ROUTE)
        head2 = VGroup(p2, c_q).arrange(RIGHT, buff=0.2)
        l164 = note("ChatComponent.jsx · line 164", S.GREY)
        head = VGroup(head2, l164).arrange(DOWN, buff=0.1).move_to([0, 2.35, 0])
        ds = code(f"{FRONT}/src/services/DataService.js", 34, 43, cuts={43: "axios.post(url"})
        ds.next_to(head, DOWN, buff=0.25)
        n10 = code_span(ds.code, 2, '"n_results": 10')
        bar36 = line_bar(ds.code, 2, TURN)
        origins = [("http://", "localhost", ":3200"), ("http://", "localhost", ":9000"),
                   ("http://", "localhost", ":8000")]
        orows = VGroup()
        for i, (sch, host, port) in enumerate(origins):
            col = INK if i == 0 else S.GREY
            r = VGroup(mono(sch, 30, col), mono(host, 30, col), mono(port, 30, INK)).arrange(RIGHT, buff=0.04)
            orows.add(r)
        orows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.75, 0])
        names = VGroup(*[note(s, TURN, 22).next_to(orows[2][i], DOWN, buff=0.3)
                         for i, s in enumerate(("scheme", "host", "port"))])
        o_cap = label("scheme + host + port: three origins", 28, INK).next_to(names, DOWN, buff=0.45)
        cross = Arrow(orows[0][2].get_right() + RIGHT * 0.1, orows[2][2].get_right() + RIGHT * 0.1,
                                      path_arc=-1.6, color=ROUTE, stroke_width=4, buff=0.05, tip_length=0.2)
        cross_t = label("crosses origins", 24, ROUTE).next_to(cross, RIGHT, buff=0.2)

        with self.voiceover(SAY[3]) as vo:
            clear_but(self, tr, rec, run_time=0.5)
            self.play(FadeIn(head, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(ds, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("for the 10 nearest chunks")
            self.play(FadeIn(bar36), Indicate(n10, color=TURN, scale_factor=1.12), run_time=0.8)
            vo.wait_until("An origin is")
            clear_but(self, tr, rec, run_time=0.4)
            self.play(FadeIn(orows[0], shift=UP * 0.1), run_time=0.4)
            vo.wait_until("scheme, host and port")
            self.play(FadeIn(orows[1:], shift=UP * 0.1), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.1) for n in names], lag_ratio=0.3),
                      each([orows[2][0], orows[2][1], orows[2][2]], TURN, scale=1.15, lag=0.3), run_time=1.0)
            self.play(FadeIn(o_cap, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("so a page from 3200 calling 8000")
            self.play(Create(cross), FadeIn(cross_t, shift=LEFT * 0.1), run_time=0.8)
            self.play(each([orows[0][2], orows[2][2]], ROUTE, scale=1.15, lag=0.3), run_time=0.7)

        # ========================================================== 4. the rule; the preflight; admit
        rule = card(["default: a page may not see another origin's replies",
                     "CORS: the server names who may"], size=26).move_to([0, 0.4, 0])
        cb2 = CorsBouncer().move_to([0, 0.4, 0])

        with self.voiceover(SAY[4]) as vo:
            clear_but(self, tr, rec, run_time=0.5)
            self.play(FadeIn(rule.frame), FadeIn(rule.body[0], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("A server can allow named origins")
            self.play(FadeIn(rule.body[1], shift=UP * 0.1), run_time=0.5)
            vo.wait_until("that is CORS")
            self.play(Indicate(rule.body[1], color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("and it keeps other websites")
            self.play(Indicate(rule.body[0], color=INK, scale_factor=1.05), run_time=0.8)
            vo.wait_until("So the browser first sends a preflight")
            self.play(FadeOut(rule), run_time=0.4)
            self.remove(rule)
            self.play(FadeIn(cb2, scale=0.97), Create(cb2.routes[1]), run_time=0.6)
            ok = cb2.preflight(self, run_time=0.8)
            assert ok
            # the pass parks right of the bouncer ABOVE route ② (next_to(bouncer) put it on door :8000)
            ps = cb2.pass_
            y_r = cb2.doors["8000"][0].get_left()[1]
            ps_to = [cb2.bouncer[0].get_right()[0] + 0.25 + ps.width / 2, y_r + 0.24 + ps.height / 2, 0]
            vo.wait_until("The database checks its guest list")
            self.play(Indicate(cb2.guest[0], color=IMAGE, scale_factor=1.05), ps.animate.move_to(ps_to),
                      run_time=0.6)
            vo.wait_until("the course's site and localhost 3200")
            self.play(each(list(cb2.guest.rows), INK, scale=1.1, lag=0.4), run_time=0.9)
            vo.wait_until("and returns a pass, or nothing")
            self.play(Indicate(getattr(cb2.pass_, "text", cb2.pass_), color=PASS, scale_factor=1.15),
                      run_time=0.6)
            vo.wait_until("Your browser is the bouncer")
            self.play(Indicate(cb2.bouncer[1], color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("no pass, no query")
            cb2.captions[2].shift(DOWN * 0.28 + LEFT * 0.15)   # off the ':8000' door label
            chunks10 = cb2.admit(self, run_time=0.8)

        # ========================================================== 5. call ③; the curl preflights; 38
        c60, c61, c38 = capture("60"), capture("61"), capture("38")
        assert "-H 'Origin: http://localhost:3200'" in c60.cmd and "-H 'Origin: http://localhost:3300'" in c61.cmd
        assert c38.cmd.endswith("http://localhost:9000/rag/llm-response"), c38.cmd
        l3 = note("ChatComponent.jsx · lines 165–171", S.GREY).move_to([0, -2.3, 0])
        ans = RoundedRectangle(width=1.5, height=0.8, corner_radius=0.08, stroke_color=S.GREY, stroke_width=2)
        ans.set_fill(S.BG, 1)
        ans_bars = VGroup(*[RoundedRectangle(width=1.2 * f, height=0.1, corner_radius=0.05, stroke_width=0)
                            .set_fill(S.GREY, 0.5) for f in (1.0, 0.85, 0.6)])
        ans_bars.arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to(ans)
        answer = VGroup(ans, ans_bars)
        t5 = term(P_LAPTOP_HOME, rows=15, size=SIZE)
        xt5 = extra_row()
        svc = code("api-service/api/service.py", 13, 20, font_size=SIZE)
        t38 = term(P_API, rows=6, size=SIZE, title=T_SECOND)
        svc.move_to([6.55 - svc.width / 2, 0, 0]).align_to([0, 3.5, 0], UP)
        xt38 = extra_row()

        with self.voiceover(SAY[5]) as vo:
            p3 = cb2.send(self, 3, run_time=0.8)
            self.play(chunks10.animate.move_to(cb2.doors["9000"][0].get_left() + LEFT * 1.25 + UP * 0.42), FadeIn(l3),
                      run_time=0.6)
            vo.wait_until("and the answer returns")
            answer.move_to(cb2.doors["9000"][0].get_left() + LEFT * 0.9)
            self.play(FadeOut(chunks10), FadeOut(p3), FadeIn(answer), run_time=0.4)
            self.remove(chunks10, p3)
            self.play(answer.animate.move_to(cb2.landing()), run_time=0.8)
            vo.wait_until("An extra curl")
            clear_but(self, tr, anims=[track(tr, extra=True)], run_time=0.5)
            on_bar(t5, xt5)
            self.play(FadeIn(t5, shift=UP * 0.2), FadeIn(xt5), run_time=0.4)
            l60 = type_rows(self, t5, c60.cmd, preflight_rows(t5, c60.cmd), type_time=0.9)
            row_o = l60.rows[1]
            g_o = ring(substring(row_o, "-H 'Origin: http://localhost:3200'"), S.GREY, buff=0.05)
            own = note("curl writes its own", S.GREY, SIZE)
            beside(own, row_o)
            self.play(Create(g_o), FadeIn(own, shift=LEFT * 0.1), run_time=0.5)
            r60 = out(self, t5, c60.at(2, 6), run_time=0.4)
            self.play(r60[1].glyphs.animate.set_color(PASS), run_time=0.4)
            the_pass = note("the pass", PASS, SIZE)
            beside(the_pass, r60[1])
            pin(self, r60[1], the_pass)
            vo.wait_until("Both preflights get 200 OK")
            drop(self, g_o, own)
            l61 = type_rows(self, t5, c61.cmd, preflight_rows(t5, c61.cmd), type_time=0.7)
            a61 = c61.at((2, 5))
            assert a61[1].startswith("vary: origin, access-control-request-method,")
            a61[1] = cut(a61[1], "access-control-request-method,")
            r61a = out(self, t5, a61, run_time=0.4)
            r61b = out(self, t5, ["", c61.line(6)], run_time=0.3)
            y_gap = r61b[0].get_center()[1]
            gap = outline_box(r60[1].glyphs.width + 0.2, 0.32, ERR)
            gap.move_to([r61a[0].glyphs.get_left()[0] + gap.width / 2 - 0.1, y_gap, 0])
            g2 = [ring(substring(r60[0], "HTTP/1.1 200 OK"), S.GREY, buff=0.05),
                  ring(substring(r61a[0], "HTTP/1.1 200 OK"), S.GREY, buff=0.05)]
            everyone = note("the server answers everyone", S.GREY, SIZE)
            beside(everyone, r61a[0])
            self.play(*[Create(g) for g in g2], FadeIn(everyone, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("but only 3200 gets a pass")
            self.play(Indicate(r60[1].glyphs, color=PASS, scale_factor=1.05), Create(gap.frame), run_time=0.7)
            no_pass = note("no pass", ERR, SIZE).next_to(gap, RIGHT, buff=0.3)
            vo.wait_until("no pass is a refusal")
            self.play(FadeIn(no_pass, shift=LEFT * 0.1), run_time=0.4)
            self.play(Indicate(no_pass, color=ERR, scale_factor=1.15), run_time=0.6)
            clear_but(self, tr, run_time=0.4)
            on_bar(t38, xt38)
            self.play(FadeIn(t38, shift=UP * 0.2), FadeIn(xt38), FadeIn(svc, shift=DOWN * 0.15), run_time=0.5)
            type_cmd(self, t38, c38.cmd, type_time=0.6)
            r38 = out(self, t38, c38.at(2, 6), run_time=0.4)
            star = code_span(svc.code, 4, 'allow_origins=["*"]')
            self.play(r38[1].glyphs.animate.set_color(PASS), Create(ring(star, PASS, buff=0.05)), run_time=0.6)
            self.play(each([substring(r38[1], "*"), star], PASS, scale=1.2, lag=0.3), run_time=0.8)

        # ========================================================== 6. ponder: republish at :3300
        pr = PacketReplay("3300").move_to([0, 0.4, 0])
        old_url = pr.page.url
        old_url.become(mono("localhost:3200", 20, S.GREY).move_to(old_url))
        stamp = VGroup(step_badge("?", ROUTE), chip("Origin: :3300", ROUTE, size=SIZE, font=MONO))
        stamp.arrange(UP, buff=0.12).next_to(pr.page.window, RIGHT, buff=0.35).shift(UP * 0.2)

        with self.voiceover(SAY[6]) as vo:
            clear_but(self, tr, anims=[track(tr, extra=False)], run_time=0.5)
            self.play(FadeIn(pr, scale=0.97), run_time=0.6)
            vo.wait_until("You republish the frontend on port 3300")
            self.play(pr.restamp("3300"), run_time=0.7)
            self.play(FadeIn(stamp, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Which of the three calls fails")
            self.play(each([pr.doors["9000"][1], pr.doors["8000"][1]], INK, scale=1.25, lag=0.3), run_time=0.9)
            self.play(stamp.animate(rate_func=there_and_back).shift(UP * 0.12), run_time=0.6)
        pc = ponder_at(self, PONDER_4, 8, 8.4, [0, 0.2, 0])

        # ========================================================== 7. the :3300 replay
        last = chip("127.0.0.1:3200 ≠ localhost:3200", S.GREY, size=22, font=MONO).move_to([0, -3.1, 0])

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(pc), FadeOut(stamp), run_time=0.5)
            self.remove(pc, stamp)
            pr.send(self, 1, run_time=0.7)
            vo.wait_until("the API allows any origin")
            ok1 = check_mark(0.32, PASS).next_to(pr.api_list, UP, buff=0.1)
            self.play(Create(ok1), Indicate(pr.api_list[1], color=PASS), run_time=0.6)
            vo.wait_until("Call two never leaves the browser")
            got = pr.preflight(self, run_time=0.7)
            assert not got
            pr.refuse(self, run_time=0.6)
            vo.wait_until("Call three waits for it")
            pr.never_sent(self, run_time=0.7)
            vo.wait_until("And curl ignores it all")
            pr.curl_walk(self, run_time=1.1)
            vo.wait_until("CORS is enforced by the browser")
            self.play(Indicate(pr.bouncer[1], color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("configured by the server")
            self.play(Indicate(pr.guest.rows, color=INK, scale_factor=1.08), run_time=0.6)
            vo.wait_until("and keyed on the page's origin")
            self.play(Indicate(pr.page.url, color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("Even 127.0.0.1")
            self.play(FadeIn(last, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("so open the app at localhost")
            self.play(Indicate(last, color=TURN, scale_factor=1.08), run_time=0.7)

        # ========================================================== 8. what to look for; the open door
        ref = lref("11, 13")
        cw2 = ChatWireframe(picker="char-split-collection ▾", win_w=8.6, win_h=6.35)
        cw2.move_to([-1.75, -0.375, 0])
        head8 = label("book · author · dist", SIZE, S.GREY).move_to(cw2.drawer[0]).align_to(cw2.drawer[0], RIGHT)
        head8.shift(LEFT * 0.6)
        assert cw2.rows[0].height > 0.06, cw2.rows[0].height
        ill4 = illustration_tag()
        look = VGroup(label("what to look for", 24, INK), note("README.md · lines 217–222", S.GREY, SIZE))
        look.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        VGroup(ill4, look).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(cw2.window, RIGHT, buff=0.3)
        m = AppMap.at("S12")
        door9 = m.doors["9000"]
        gm = meter().next_to(door9.glyph, RIGHT, buff=0.2).align_to(door9.glyph, DOWN)
        warn = card(["an unprotected AI endpoint"], color=ERR, size=26).move_to([0, -2.95, 0])
        cors_note = note("CORS: which page may see a reply", S.GREY, SIZE)
        who = note("who may call? nothing here", S.GREY, SIZE)

        with self.voiceover(SAY[8]) as vo:
            clear_but(self, tr, run_time=0.5)
            self.play(FadeIn(cw2.shell, shift=UP * 0.15), FadeIn(ill4), FadeIn(look), FadeIn(ref), run_time=0.7)
            self.add(cw2.question)
            vo.wait_until("Look for an answer")
            self.play(cw2.grow_bars(0.9))
            vo.wait_until("and ten references")
            self.play(cw2.open_drawer(1.0), FadeIn(head8))
            vo.wait_until("with book, author and distance")
            self.play(Indicate(head8, color=INK, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Last thought")
            clear_but(self, tr, ref, run_time=0.5)
            self.play(FadeIn(m, scale=1.03), run_time=0.6)
            vo.wait_until("CORS decides which page may see a reply")
            cors_note.move_to([-6.3 + cors_note.width / 2, -1.68, 0])
            self.play(FadeIn(cors_note, shift=LEFT * 0.1), Indicate(m.browser, color=LAPTOP, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("nothing here decides who may call")
            who.next_to(cors_note, DOWN, buff=0.15).align_to(cors_note, LEFT)
            self.play(Indicate(door9.text, color=INK, scale_factor=1.25), FadeIn(who), run_time=0.8)
            vo.wait_until("An unprotected AI endpoint")
            self.play(FadeIn(warn, shift=UP * 0.15), FadeIn(gm), run_time=0.6)
            vo.wait_until("spending your key")
            self.play(meter_tick(gm, run_time=0.8))
            vo.wait_until("is running on your laptop")
            self.play(Indicate(warn.body, color=ERR, scale_factor=1.06), run_time=0.8)

        self.wait(0.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
