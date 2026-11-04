"""S15 · Tear down, recap, and what's next (AC215 L10) — tracker F2 · extra through beats 0–1 (it fades
with the key card at the recap), `lref("26, 31, 53")` the whole scene.

Beats (script.md, ## S15; one voiceover block each):
0. The map as S14 left it after the extra restart (laptop/73): both streets, Chroma lit, the frontend
   and API houses dark, the GREEN drawer. A 3-row strip at `llm-rag`: `docker compose down` (laptop/75,
   `▶ your turn` on the bar): the two warnings (lines 2–3) GREY and cut after `level=warning`, then
   4–5 (Chroma darkens), 6–7 (the house goes; the GREEN docker-volumes folder stays where it stood),
   8–9 (llm-rag-network vanishes). `docker network rm cheese-app-network` (laptop/76, `extra`) → its
   line 2: the cheese-app street, the dark houses and the API tube vanish. Left: drawer and folder.
1. The BLUE building with GREY lines 'this lecture started nothing in the cloud' / 'no VM · no
   bucket · no endpoint'; the GREEN key file card + a GOLD meter that ticks; the card turns over into
   the `extra` card 'key hygiene' (both gcloud commands folded, the console route in S03's words,
   the local-file line); a RED card (GitHub → delete in IAM; history rewriting is not enough); a
   turnstile arch `detect-private-key` with its caption.
2. The recap on V6: the empty laptop relights piece by piece (API + BLUE call, a GREEN badge and key riding it, the token desk and
   ticket · one GREEN IAM cell · the GREEN tubes · streets, houses and phone books · the loop · the
   doors · the Wi-Fi side · the three PINK calls past the GREY bouncer · the GREEN folder). S01's
   three riddle labels and the knock fly in under the map; each gets a GREEN check as its piece
   lights. Then everything unlit.
3. The debugging flowchart on its own: six error rows → layer, each with a thumbnail of its picture.
4. 'Test yourself': five questions one at a time (24 pt, ≤ 3 lines) with a thumbnail; earlier ones
   collapse into a numbered label list at left.
5. Footer cards (exercises.md; the study guide) and the GREY dashed 'Next' card. Empty frame.
"""

from manim import *  # noqa: I001  (manim first, then common: common must win)

from explainer.scene import VoiceScene

from common import (CLOUD, CONTAINERS, ERR, FUTURE, IMAGE, INK, KEY, LAPTOP, NARRATION, P_LLMRAG,
                    PASS, ROUTE, SA_EMAIL, SAY_COUNT, TOOL, TURN, AppMap, Ticket, capture, card, check_mark,
                    cut, desk_glyph, door_glyph, err_chip, extra_row, extra_tag, file_card, file_glyph,
                    flash_tag, folder_glyph, google_building, key_glyph, label, lref, magnifier, meter,
                    meter_tick, mono, note, on_bar, out, outline_box, person_icon, pin, beside, riddle_label,
                    route, step_badge, term, tracker, turn_row, type_cmd, KNOCK)
from explainer import style as S

SAY = NARRATION["S15"]
GUIDE = "MLOps_Learning · guides/L10-cloud-connect-cheese-app-v0.md"


# ------------------------------------------------------------------ helpers
def clear_but(scene, *keep, anims=(), run_time: float = 0.6):
    """Plays: everything on screen fades except the families of `keep` (tracker, lecture tag), then
    `keep` is re-added whole. Same as S04/S12's."""
    ids = {id(f) for k in keep for f in k.get_family()}
    drop = [x for x in scene.mobjects if not any(id(f) in ids for f in x.get_family())]
    scene.play(FadeOut(Group(*drop)), *anims, run_time=run_time)
    scene.remove(*drop)
    scene.add(*keep)


def book(m: AppMap, k: str, names) -> VGroup:
    """Street k's phone book right under its band (S10's placement)."""
    g = m.phone_book(k, names)
    band = m.streets[k].band
    g.next_to(band, DOWN, buff=0.03).align_to(band, RIGHT)
    g.shift(RIGHT * (0.26 if k == "cheese-app" else -0.12))
    return g


def volumes_folder() -> VGroup:
    """The GREEN docker-volumes/ folder (S14's survivor). .glyph .text"""
    g = VGroup(folder_glyph(0.34, KEY), mono("docker-volumes/", 20, KEY)).arrange(RIGHT, buff=0.12)
    g.glyph, g.text = g[0], g[1]
    return g


def mini_badge(color=KEY) -> VGroup:
    """The service account's badge, small enough to ride the map's lane (S09's, no text)."""
    fr = RoundedRectangle(width=0.42, height=0.52, corner_radius=0.07, stroke_color=color,
                          stroke_width=3).set_fill(S.GREY_DARKER, 1)
    clip = RoundedRectangle(width=0.2, height=0.09, corner_radius=0.03, stroke_color=color,
                            stroke_width=2).set_fill(S.BG, 1).move_to(fr.get_top())
    face = Circle(radius=0.09, stroke_color=color, stroke_width=2.5).move_to(fr.get_center() + UP * 0.06)
    line_ = Line(LEFT * 0.12, RIGHT * 0.12, color=color, stroke_width=2.5).move_to(fr.get_center() + DOWN * 0.14)
    return VGroup(fr, clip, face, line_)


def knock_label() -> VGroup:
    """S01's fourth card, small: a door with a knocker and the question (20 pt)."""
    d = door_glyph(0.3, 0.42, S.GREY)
    k = Circle(radius=0.06, stroke_color=TURN, stroke_width=2.5).move_to(d.get_center() + UP * 0.06)
    g = VGroup(VGroup(d, k), label(KNOCK, 20, INK)).arrange(RIGHT, buff=0.18)
    g.text = g[1]
    return g


def turnstile() -> VGroup:
    """L09's gate: an arch over two posts with a turning three-arm bar. .arms .name"""
    posts = VGroup(*[Line([x, 0, 0], [x, 0.75, 0], color=S.GREY, stroke_width=4) for x in (-0.6, 0.6)])
    arch = Arc(radius=0.6, start_angle=0, angle=PI, color=S.GREY, stroke_width=4).move_to([0, 1.05, 0])
    hub = Dot([0, 0.42, 0], radius=0.06, color=S.GREY)
    arms = VGroup(*[Line([0, 0.42, 0], [0.42 * np.cos(a), 0.42 + 0.42 * np.sin(a), 0], color=TOOL,
                         stroke_width=4) for a in (PI / 2 + 0.3, PI / 2 + 0.3 + 2 * PI / 3, PI / 2 + 0.3 + 4 * PI / 3)])
    name = mono("detect-private-key", 22, TOOL).next_to(arch, UP, buff=0.12)
    g = VGroup(posts, arch, arms, hub, name)
    g.arms, g.name, g.hub = arms, name, hub
    return g


def mini_grid(green=(1, 0), red=None, cell: float = 0.3) -> VGroup:
    """A text-free 2 x 3 IAM grid thumbnail: one GREEN cell (row, col)."""
    g = VGroup()
    for r in range(2):
        for c in range(3):
            col = PASS if (r, c) == green else (ERR if (r, c) == red else S.GREY)
            sq = Square(cell, stroke_color=col, stroke_width=2.5).set_fill(col, 0.35 if col != S.GREY else 0)
            g.add(sq.move_to([c * (cell + 0.06), -r * (cell + 0.06), 0]))
    return g.move_to(ORIGIN)


def tube_thumb(k: float = 1.0) -> VGroup:
    """The portal, text-free: a GREEN folder, a GREEN tube, a TEAL container box."""
    f = folder_glyph(0.4 * k, KEY)
    bx = RoundedRectangle(width=0.8 * k, height=0.55 * k, corner_radius=0.08, stroke_color=IMAGE, stroke_width=3)
    bx.next_to(f, RIGHT, buff=0.8 * k)
    t = Line(f.get_right() + RIGHT * 0.06, bx.get_left() + LEFT * 0.06, color=KEY, stroke_width=5)
    glow = t.copy().set_stroke(KEY, 12, opacity=0.18)
    return VGroup(f, glow, t, bx)


def bouncer_thumb(k: float = 1.0) -> VGroup:
    """The CORS bouncer beside a door, text-free."""
    return VGroup(person_icon(S.GREY, 0.55 * k), door_glyph(0.34 * k, 0.5 * k)).arrange(RIGHT, buff=0.2 * k)


def door_thumb() -> VGroup:
    """A door in a wall and a PINK street stub: doors and names."""
    d = door_glyph(0.34, 0.5)
    st = outline_box(1.0, 0.24, ROUTE, solid=True, fill_opacity=0.15)
    return VGroup(d, st).arrange(RIGHT, buff=0.25)


def arrows_thumb(k: float = 1.0) -> VGroup:
    """Two arrows: a PINK name dial and a GREY localhost ring."""
    a = Arrow(LEFT * 0.55 * k, RIGHT * 0.55 * k, buff=0, color=ROUTE, stroke_width=4, tip_length=0.16)
    b = Arrow(LEFT * 0.55 * k, RIGHT * 0.55 * k, buff=0, color=S.GREY, stroke_width=4, tip_length=0.16)
    return VGroup(a, b).arrange(DOWN, buff=0.25 * k)


def adc_thumb(k: float = 1.0) -> VGroup:
    """ADC's glass over three slots (1 GREEN, 2 and 3 GREY dashed)."""
    slots = VGroup(outline_box(0.9 * k, 0.2 * k, KEY, solid=True, fill_opacity=0.2),
                   outline_box(0.9 * k, 0.2 * k, S.GREY), outline_box(0.9 * k, 0.2 * k, S.GREY))
    slots.arrange(DOWN, buff=0.1 * k)
    gl = magnifier(0.2 * k).next_to(slots, LEFT, buff=0.15 * k)
    return VGroup(gl, slots)


def qline(parts, size: float = 24) -> VGroup:
    """One question line: (text, 'l'|'m') pieces, label or mono, on one baseline."""
    ms = [mono(s, size - 2, INK) if k == "m" else label(s, size, INK) for s, k in parts]
    g = VGroup(*ms).arrange(RIGHT, buff=0.12)
    for x in ms[1:]:
        x.align_to(ms[0], DOWN)
    return g


QUESTIONS = (
    ([[("Name ADC's three places,", "l")], [("and the one this tutorial fills.", "l")]], "ADC", adc_thumb),
    ([[("Why is", "l"), ("GOOGLE_APPLICATION_CREDENTIALS", "m")],
      [("set to", "l"), ("/secrets/…", "m"), ("and not", "l")],
      [("to a path on your Mac?", "l")]], "the portal", tube_thumb),
    ([[("The CLI dials", "l"), ("llm-rag-chromadb:8000;", "m")],
      [("your browser rings", "l"), ("localhost:8000.", "m")],
      [("Why can't they swap?", "l")]], "two addresses", arrows_thumb),
    ([[("You serve the frontend at", "l"), ("http://localhost:3300.", "m")],
      [("Which component breaks first,", "l")],
      [("and why does the API keep working?", "l")]], "origins", bouncer_thumb),
    ([[("You got a 403 on", "l"), ("/rag/embedding.", "m")],
      [("Three distinct causes:", "l")],
      [("how do you tell them apart?", "l")]], "403", lambda k: mini_grid((1, 0), (1, 2), cell=0.3 * k)),
)


class Recap(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S15"] == 6, len(SAY)
        tr = tracker("F", 2, True)
        ref = lref("26, 31, 53")

        # ========================================================== 0. tear down
        m0 = AppMap.at("S15", laid=("llm-rag", "cheese-app"), lit=("chroma",), gone=("loader",), folder=False)
        vf0 = volumes_folder().move_to(m0.folder)
        strip = term(P_LLMRAG, rows=3)
        c75, c76 = capture("75"), capture("76")
        assert c75.cmd == "docker compose down" and c76.cmd == "docker network rm cheese-app-network"
        warns = [(cut(s, "level=warning"), S.GREY) for s in c75.at(2, 3)]
        tt = on_bar(strip, turn_row())

        with self.voiceover(SAY[0]) as vo:
            # the narration names the command at ~1.7 s and the extra one at ~3.9 s: the down's output
            # runs fast from the first words, so the network rm and the 'Pause' flash land on their words
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(ref), FadeIn(m0, scale=1.03), FadeIn(strip),
                      FadeIn(tt, shift=LEFT * 0.1), run_time=0.7)
            type_cmd(self, strip, c75.cmd, type_time=0.6)
            out(self, strip, warns, run_time=0.3)
            out(self, strip, c75.at((4, 5)), run_time=0.3)
            self.play(m0.darken("chroma"), run_time=0.3)
            out(self, strip, c75.at((6, 7)), run_time=0.3)
            ch = m0.houses["chroma"]
            self.play(FadeOut(ch), FadeIn(vf0, scale=0.8), run_time=0.4)
            m0.remove(ch)
            out(self, strip, c75.at((8, 9)), run_time=0.3)
            self.play(m0.unlay("llm-rag"), run_time=0.4)
            m0.remove(m0.streets["llm-rag"])
            vo.wait_until("An extra command removes")
            ln = type_cmd(self, strip, c76.cmd, type_time=0.6)
            xt = beside(extra_row(), ln)
            pin(self, ln, xt, run_time=0.3)
            out(self, strip, c76.at(2), run_time=0.3)
            gone = VGroup(m0.streets["cheese-app"], m0.houses["frontend"], m0.houses["api"], m0.tubes["api"])
            self.play(FadeOut(gone), run_time=0.5)
            for x in gone:
                m0.remove(x)
            vo.wait_until("Pause, and leave")
            flash_tag(self, tt, TURN)
            vo.wait_until("your machine clean")
            self.play(Indicate(m0.drawer.text, color=KEY, scale_factor=1.15),
                      Indicate(vf0.text, color=KEY, scale_factor=1.1), run_time=0.9)

        # ========================================================== 1. nothing in the cloud; the key
        gb = google_building(2.2, 2.6, door=False, meter_=False).move_to([-4.6, 0.05, 0], aligned_edge=DOWN)
        n1 = note("this lecture started nothing in the cloud", S.GREY, 26)
        n2 = note("no VM · no bucket · no endpoint", S.GREY, 24)
        VGroup(n1, n2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(gb, RIGHT, buff=0.6)
        kfile = file_card("secrets/llm-service-account.json", KEY, size=22)
        kg = key_glyph(0.8).next_to(kfile, LEFT, buff=0.3)
        kc = VGroup(kg, kfile).move_to([-0.6, -1.6, 0])
        gm = meter(0.8).next_to(kc, RIGHT, buff=0.6)

        # the extra 'key hygiene' card
        acct = "--iam-account=" + SA_EMAIL
        rows = [mono("gcloud iam service-accounts keys list \\", 20, INK), mono(acct, 20, INK),
                mono("gcloud iam service-accounts keys delete KEY_ID \\", 20, INK), mono(acct, 20, INK)]
        cmds = VGroup(VGroup(rows[0], rows[1]).arrange(DOWN, aligned_edge=LEFT, buff=0.08),
                      VGroup(rows[2], rows[3]).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        cmds.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        pid = note("your-gcp-project: your project ID, as in GCP_PROJECT", S.GREY, 20)
        console = note("or the console: IAM & Admin → Service accounts → llm-service-account → KEYS → delete",
                       S.GREY, 20)
        local = note("deleted a key in IAM? delete secrets/llm-service-account.json too", S.GREY, 20)
        head = VGroup(label("key hygiene", 24, INK), extra_tag()).arrange(RIGHT, buff=0.35)
        body = VGroup(head, cmds, pid, console, local).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        hy_fr = RoundedRectangle(width=body.width + 0.5, height=body.height + 0.4, corner_radius=0.14,
                                 stroke_color=S.GREY, stroke_width=2.5).set_fill(S.GREY_DARKER, 1)
        hy_fr.move_to([0, 2.72 - hy_fr.height / 2, 0])
        body.move_to(hy_fr)
        kc_fr = kfile.box
        gh = card(["a key on GitHub → delete it in IAM now", "rewriting history is not enough"], color=ERR,
                  size=22)
        gh.move_to([-6.45 + gh.width / 2, -2.75, 0])
        ts = turnstile()
        cap = note("once added to the repo you commit from", S.GREY, 20)
        gate = VGroup(ts, cap)
        cap.next_to(ts, DOWN, buff=0.12)
        gate.move_to([3.6, -2.42, 0])

        with self.voiceover(SAY[1]) as vo:
            clear_but(self, tr, ref, run_time=0.6)
            self.play(FadeIn(gb, shift=UP * 0.2), run_time=0.7)
            self.play(FadeIn(n1, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(n2, shift=RIGHT * 0.2), run_time=0.5)
            vo.wait_until("What stays behind is the key")
            self.play(FadeIn(kc, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("and a leaked key can spend")
            self.play(FadeIn(gm), run_time=0.4)
            self.play(meter_tick(gm, run_time=0.8))
            vo.wait_until("Delete keys you no longer use")
            # the whole card is built inside this ~3.5 s sentence, so every row is up while it plays
            self.play(FadeOut(VGroup(gb, n1, n2, gm)), FadeOut(VGroup(kg, kfile.glyph, kfile.text)),
                      FadeTransform(kc_fr, hy_fr), run_time=0.6)          # a point-wise morph stripes the frame
            self.remove(kc)
            self.play(FadeIn(head), FadeIn(cmds[0], shift=DOWN * 0.1), run_time=0.45)
            self.play(FadeIn(cmds[1], shift=DOWN * 0.1), FadeIn(pid), run_time=0.4)
            self.play(FadeIn(console, shift=DOWN * 0.1), FadeIn(local, shift=DOWN * 0.1), run_time=0.45)
            vo.wait_until("and their local files")
            self.play(Indicate(local, color=KEY, scale_factor=1.05), run_time=0.7)
            vo.wait_until("If one reaches GitHub")
            # the card stays at full contrast: the GitHub card and the turnstile sit below it (y < -1.3)
            assert hy_fr.get_bottom()[1] > max(gh.get_top()[1], gate.get_top()[1]) + 0.1
            self.play(FadeIn(gh, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("delete it in IAM at once")
            self.play(Indicate(gh.body[0], color=ERR, scale_factor=1.06), run_time=0.8)
            vo.wait_until("last lecture's private key hook")
            self.play(FadeIn(ts, shift=UP * 0.15), run_time=0.6)
            self.play(Rotate(ts.arms, angle=2 * PI / 3, about_point=ts.hub.get_center()), run_time=0.8)
            vo.wait_until("once added to your repo")
            self.play(FadeIn(cap, shift=UP * 0.1), Indicate(ts.name, color=TOOL, scale_factor=1.08), run_time=0.7)

        # ========================================================== 2. the recap on V6
        m = AppMap(drawer=True)
        vf = volumes_folder()
        vf.move_to([-4.55 + vf.width / 2, m.header.get_center()[1], 0])      # top band, left of the drawer
        assert vf.get_right()[0] < m.drawer.get_left()[0] - 0.3
        mount = DashedLine(vf.glyph.get_bottom() + DOWN * 0.04, m.houses["chroma"].roof.get_top() + UP * 0.04,
                           color=KEY, stroke_width=3)
        pb_rag = book(m, "llm-rag", [CONTAINERS["chroma"]])
        pb_api = book(m, "cheese-app", [CONTAINERS["api"]])
        g_call = m.call("api", "google")
        # the token desk and the ticket, inside Google's hall
        desk = desk_glyph(0.8)
        tk = Ticket(1.45, timer=False)
        inner = VGroup(desk, tk).arrange(DOWN, buff=0.12)
        panel = RoundedRectangle(width=1.6, height=inner.height + 0.2, corner_radius=0.1, stroke_color=CLOUD,
                                 stroke_width=2).set_fill(S.BG, 1)
        hall_l = m.google.frame[1].get_left()[0]
        panel.move_to([hall_l + 0.06 + 0.8, m.google.text.get_bottom()[1] - 0.08 - panel.height / 2, 0])
        inner.move_to(panel)
        tk_start = tk.copy().move_to(m.google.door.get_center())
        rider = VGroup(mini_badge(), key_glyph(0.45)).arrange(RIGHT, buff=0.08)   # the GREEN badge and key
        rider.move_to(g_call.path.get_start())
        cell = Square(0.38, stroke_color=PASS, stroke_width=3).set_fill(PASS, 0.3)
        cell.next_to(m.google.guard, RIGHT, buff=0.15)
        cell_ok = check_mark(0.24, PASS).move_to(cell)
        wf = m.wifi()
        win = m.browser.window
        bouncer = person_icon(S.GREY, 0.42).next_to(win, UP, buff=0.04)
        calls = []                                         # ① :9000, ② :8000, ③ :9000, to just under each door's label
        for side, dy, p, ox, ey in ((RIGHT, 0.0, "9000", -0.1, -0.1), (LEFT, 0.1, "8000", 0.0, -0.08),
                                    (RIGHT, -0.2, "9000", 0.12, -0.3)):
            a = win.get_edge_center(side) + side * 0.06 + UP * dy
            t = m.doors[p].text
            calls.append(route(a, np.array([t.get_center()[0] + ox, t.get_bottom()[1] + ey, 0])))
        # S01's labels and the knock, under the map
        rl = [riddle_label(i) for i in range(3)]
        kn = knock_label()
        row1 = VGroup(rl[0], rl[1], rl[2]).arrange(RIGHT, buff=1.0)
        row1.move_to([-1.0, -2.45, 0])
        kn.move_to([-1.0, -3.15, 0])
        lbls = [rl[0], rl[1], rl[2], kn]
        ticks = [check_mark(0.3, PASS).next_to(x, RIGHT, buff=0.15) for x in lbls]

        def tick(i, *anims):
            self.play(Create(ticks[i]), Indicate(lbls[i][0] if i < 3 else lbls[i].text, color=PASS,
                                                 scale_factor=1.08), *anims, run_time=0.6)

        with self.voiceover(SAY[2]) as vo:
            clear_but(self, ref, run_time=0.6)           # the README tracker goes: this is the lecture's recap
            self.play(FadeIn(m, scale=1.03), run_time=0.7)
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 1.5) for x in lbls], lag_ratio=0.2), run_time=1.0)
            vo.wait_until("Your code's badge and key")
            self.play(m.light("api"), run_time=0.5)
            self.play(Create(g_call), FadeIn(rider, scale=0.6), run_time=0.7)
            vo.wait_until("buy a one-hour ticket")
            self.play(MoveAlongPath(rider, g_call.path), run_time=0.8)
            self.play(FadeIn(panel), FadeIn(desk, shift=UP * 0.1), run_time=0.5)
            self.play(FadeTransform(rider, tk_start), run_time=0.4)
            self.play(Transform(tk_start, tk), run_time=0.6)
            vo.wait_until("One IAM cell")
            self.play(FadeIn(cell, scale=0.6), run_time=0.4)
            self.play(Create(cell_ok), Indicate(m.google.guard[1], color=PASS, scale_factor=1.2), run_time=0.6)
            vo.wait_until("A mount carries the key")
            self.play(m.tube_on("api"), m.tube_on("loader"), run_time=0.8)
            self.play(Indicate(m.drawer.text, color=KEY, scale_factor=1.15), run_time=0.6)
            vo.wait_until("Containers dial names")
            self.play(m.lay("llm-rag"), m.lay("cheese-app"), m.light("chroma"), m.light("loader"),
                      m.light("frontend"), run_time=0.7)
            self.play(FadeIn(pb_rag, shift=DOWN * 0.1), FadeIn(pb_api, shift=DOWN * 0.1), run_time=0.5)
            tick(2)
            vo.wait_until("your browser dials localhost")
            self.play(FadeOut(VGroup(pb_rag, pb_api)), run_time=0.4)
            self.play(Indicate(m.loop[1], color=INK, scale_factor=1.12), Indicate(m.browser.text, color=INK),
                      run_time=0.7)
            tick(1)
            vo.wait_until("through doors like 3200")
            self.play(m.open_door("8000"), m.open_door("3200"), m.open_door("9000"), run_time=0.6)
            self.play(Indicate(m.doors["3200"].text, color=INK, scale_factor=1.2), run_time=0.5)
            tick(0)
            vo.wait_until("open to your Wi-Fi too")
            self.play(FadeIn(wf[0]), *[Create(r) for r in wf.reach.values()], run_time=0.7)
            tick(3)
            vo.wait_until("The browser stitches three calls")
            self.play(FadeOut(VGroup(wf[0], *wf.reach.values())), FadeIn(bouncer, shift=RIGHT * 0.1), run_time=0.5)
            for c in calls:
                self.play(Create(c), run_time=0.45)
            vo.wait_until("past the CORS bouncer")
            self.play(Indicate(bouncer, color=INK, scale_factor=1.2), run_time=0.6)
            vo.wait_until("and the vectors survive")
            self.play(FadeIn(vf, shift=DOWN * 0.1), run_time=0.5)
            self.play(Create(mount), run_time=0.5)
            self.play(Indicate(vf.text, color=KEY, scale_factor=1.1),
                      Indicate(m.houses["chroma"].text, color=INK, scale_factor=1.15), run_time=0.8)

        whole = Group(*[x for x in self.mobjects if x is not ref])
        self.play(whole.animate.fade(0.75), run_time=0.9)           # everything unlit

        # ========================================================== 3. the debugging flowchart
        def lrow(err, alt, layer, thumb, mono_font=True):
            c = err_chip(err, mono_font=mono_font)
            left = VGroup(c)
            if alt:
                left.add(note(alt, S.GREY, 20).next_to(c, DOWN, buff=0.06).align_to(c, RIGHT))
            return left, c, label(layer, 24, INK), thumb

        specs = [lrow("DefaultCredentialsError", None, "the path or the mount", tube_thumb()),
                 lrow("401", None, "no valid token", Ticket(1.45, timer=False, color=S.GREY)),
                 lrow("403", None, "role, project, or API", mini_grid((1, 0))),
                 lrow("Failed to fetch", "or a CORS line in the console", "the origin", bouncer_thumb()),
                 lrow("port is already allocated", "or a name conflict", "the doors and names", door_thumb()),
                 lrow("the script dies on the network", None, "line 14",
                      VGroup(file_glyph(0.4, LAPTOP), mono("14", 22, ERR)).arrange(RIGHT, buff=0.12),
                      mono_font=False)]
        y, rows_ = 2.0, []
        for left, c, lay, th in specs:
            cy = y - max(c.height, th.height, 0.45) / 2
            left.shift(np.array([-0.6 - c.get_right()[0], cy - c.get_center()[1], 0]))
            ar = Arrow([-0.45, cy, 0], [0.45, cy, 0], buff=0, color=S.GREY, stroke_width=3, tip_length=0.16)
            lay.move_to([0.65 + lay.width / 2, cy, 0])
            th.move_to([5.45, cy, 0])
            rows_.append(VGroup(left, ar, lay, th))
            y = min(left.get_bottom()[1], th.get_bottom()[1]) - 0.3
        heads = VGroup(note("error", S.GREY, 20), note("its layer", S.GREY, 20))
        y, rows_ = 2.0, []
        for left, c, lay, th in specs:
            h = max(left.height, th.height, 0.45)
            cy = y - h / 2
            left.move_to([-0.6 - left.width / 2, cy, 0])
            left.shift(UP * (cy - c.get_center()[1]) if len(left) > 1 else ORIGIN)
            ar = Arrow([-0.45, cy, 0], [0.45, cy, 0], buff=0, color=S.GREY, stroke_width=3, tip_length=0.16)
            lay.move_to([0.65 + lay.width / 2, cy, 0])
            th.move_to([5.45, cy, 0])
            rows_.append(VGroup(left, ar, lay, th))
            y -= h + 0.32
        heads[0].move_to([-0.6 - heads[0].width / 2, 2.35, 0])
        heads[1].move_to([0.65 + heads[1].width / 2, 2.35, 0])
        anchors = ("A credentials error", "A 401", "A 403", "A CORS line", "A taken port", "A dying script")

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(whole), run_time=0.5)
            self.remove(*whole)
            self.add(ref)
            vo.wait_until("find its layer")
            self.play(FadeIn(heads, shift=DOWN * 0.1), run_time=0.5)
            for r, a in zip(rows_, anchors):
                vo.wait_until(a)
                self.play(FadeIn(r[0], shift=RIGHT * 0.15), GrowArrow(r[1]), run_time=0.45)
                self.play(FadeIn(r[2], shift=RIGHT * 0.15), FadeIn(r[3], scale=0.8), run_time=0.45)

        # ========================================================== 4. test yourself
        title = label("Test yourself", 28, INK).move_to([-6.45, 2.45, 0], aligned_edge=LEFT)
        q_fr = RoundedRectangle(width=9.2, height=1.85, corner_radius=0.16, stroke_color=TURN,
                                stroke_width=2.5).set_fill(S.GREY_DARKER, 1).move_to([1.85, 1.2, 0])
        list_pos = [np.array([-6.45, 1.55 - i * 0.62, 0]) for i in range(5)]
        q_items = []
        for i, (lines, short, thumb) in enumerate(QUESTIONS):
            b = step_badge(i + 1, TURN)
            txt = VGroup(*[qline(p) for p in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            assert len(lines) <= 3 and txt.width < q_fr.width - 1.3, (i, txt.width)
            b.move_to(q_fr.get_corner(UL) + np.array([0.45, -0.45, 0]))
            txt.next_to(b, RIGHT, buff=0.3).align_to(b, UP).shift(UP * 0.04)
            th = thumb(1.6).move_to([1.85, -0.9, 0])
            lb_b = step_badge(i + 1, TURN).move_to(list_pos[i] + RIGHT * 0.22)
            lb_t = label(short, 22, INK).next_to(lb_b, RIGHT, buff=0.2)
            q_items.append((b, txt, th, lb_b, lb_t))
        q_anchors = ("One: the three places", "Two: why slash secrets", "Three: why can",
                     "Four: on port 3300", "Five: a 403")

        def collapse(i, *anims):
            b, txt, th, lb_b, lb_t = q_items[i]
            self.play(Transform(b, lb_b), FadeOut(txt, shift=LEFT * 0.3), FadeOut(th), FadeIn(lb_t, shift=LEFT * 0.3),
                      *anims, run_time=0.6)
            self.remove(b)
            self.add(lb_b)

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(Group(*rows_, heads)), run_time=0.5)
            self.remove(*rows_, heads)
            self.play(FadeIn(title, shift=RIGHT * 0.2), FadeIn(q_fr), run_time=0.6)
            for i, a in enumerate(q_anchors):
                vo.wait_until(a)
                if i:
                    collapse(i - 1)
                b, txt, th, _, _ = q_items[i]
                self.play(FadeIn(b, scale=0.7), FadeIn(txt, shift=UP * 0.15), run_time=0.5)
                self.play(FadeIn(th, scale=0.8), run_time=0.4)
            self.play(Indicate(q_items[4][1][1], color=TURN, scale_factor=1.05), run_time=0.8)

        # ========================================================== 5. answers, guide, next
        ans = card([VGroup(label("Answers:", 22, INK), mono("exercises.md", 22, INK)).arrange(RIGHT, buff=0.2)],
                   size=22)
        gd = card([label("Study guide + every command:", 22, INK), mono(GUIDE, 20, INK)], size=22)
        nxt = card(["L11 · data-service-account, real buckets, a bucket's CORS list",
                    "L13–L15 · ADC's third place, inside the cloud",
                    "L21+ · federation for CI"], color=FUTURE, size=22, dashed=True, head="Next")
        nxt.move_to([-2.9 + nxt.width / 2, 1.0, 0])
        ans.move_to([-2.9 + ans.width / 2, -1.25, 0])
        gd.move_to([-6.45 + gd.width / 2, -2.75, 0])

        with self.voiceover(SAY[5]) as vo:
            collapse(4, FadeOut(q_fr))
            vo.wait_until("Answers are in the exercises")
            self.play(FadeIn(ans, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("commands in the study guide")
            self.play(FadeIn(gd, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("Next lecture")
            self.play(FadeIn(nxt.frame), FadeIn(nxt.head), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(x, shift=RIGHT * 0.15) for x in nxt.body], lag_ratio=0.35), run_time=1.2)
            vo.wait_until("real buckets")
            self.play(Indicate(nxt.body[0], color=INK, scale_factor=1.05), run_time=0.8)

        self.wait(0.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
