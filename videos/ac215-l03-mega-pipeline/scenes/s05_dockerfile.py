r"""S05 · Write the Dockerfile, line by line (README › transcribe_audio step 4; V2 build-up).

Layout for the whole scene: the Dockerfile panel (files/transcribe_audio.Dockerfile, 20 pt, the
file a student ends up with) at the top, left edge fixed, so a "swap" reads as scrolling the same
file; its caption "from transcribe_audio/README.md · lines 41–90" in the top-right corner. V2 in
the bottom band (y −1.43 … −3.55): lecture 2's TEAL config card at left, the layer stack at right.
Each highlighted line sends a copy of its keyword down into the band, where it turns into its slab
or into its line on the card.

Beats (script.md "## S05", one voiceover block each):
 0  TRACKER A3→A4. A GREY README card (transcribe_audio/README.md · line 38: the README's two
    sentences) and a dashed ghost `Dockerfile` where the panel's header will be. On "so you write
    it yourself" V2 begins: the stack's floor (bottom right) and the empty config card (bottom left).
 1  The ghost becomes the header of PANEL(1–3), whose lines type in; the caption appears. Line 1
    gets the YELLOW bar; `FROM` drops into the band as the ORANGE base slab "Debian 12 + Python
    3.12". GREY note under the panel: "line 1: from the README's text, line 41".
 2  Bar on line 3; `ARG` drops onto the card as the ORANGE line "DEBIAN_PACKAGES · build time
    only" (no slab). `ffmpeg` underlines YELLOW. CODE(transcribe_audio/cli.py: 67–69) slides in at
    bottom left over the card, line 69 barred, GREY tag "runs the ffmpeg program".
 3  The inset leaves; the panel scrolls to PANEL(5–10). Six `ENV` copies write six card lines (no
    slabs); the card's title pulses on "no layers". Bar on lines 5–8; each card line ("no apt
    questions", "Unicode text", "print at once", "uv copies files") pulses with its value as named.
 4  Bar on line 9; its card line turns GREEN and grows: "the venv lives in /home/app/.venv · outside
    /app"; `/home/app/.venv` turns GREEN (no underline: it would sit on line 10's capitals);
    YELLOW tag "remember this line" (wiggles on "Soon").
 5  Bar on line 10; its card line turns PINK, "where the key is · a relative path", with a small
    PINK signpost glyph; `secrets/` underlines PINK.
 6  The panel scrolls to PANEL(12–21). The nine `\` pulse on "backslash", then the nine `&&` on
    "double ampersands"; `RUN` drops one fat ORANGE slab. The
    slab zooms up (an ORANGE inset over the card, dashed zoom lines to the slab): "apt lists" pages
    appear (line 12), ORANGE packages fill in (13–14), the pages crumple and vanish inside the slab
    (15–16); on "cost nothing" the "apt lists" label is struck through and the apt slab on the
    stack pulses.
 7  Bar on 17–18: an ORANGE `pip` chip, then a PURPLE `uv` chip drops in beside it. GREY note (two
    rows): "this Python is the image's own (/usr/local), / not Debian's → pip may install".
 8  Bar on 19–21: a GREY user glyph "app · uid 1000", an arrow "owns" to a TEAL folder `/app`. The
    caption gives way to a two-row README chip `transcribe_audio/README.md · line 72` "Running
    containers as root is a security risk". The zoom shrinks back into its slab.
 9  The panel scrolls to PANEL(23–30). `USER` writes "USER app" on the card; `WORKDIR` drops a
    hairline slab. `COPY` drops the thin GREY slab holding tiny file glyphs and a tiny GOLD key (not
    commented on). The `.` underlines YELLOW with "= everything in this folder" beside line 26;
    "everything" underlines YELLOW on "hold on to that word".
10  `RUN uv sync` drops the empty GREEN slab "venv · /home/app/.venv"; `ENTRYPOINT` and `CMD`
    become the label "start: bash, venv on" on top of the stack; on "from pyproject.toml" a
    label "from pyproject.toml" (GREEN) sits beside line 27 and the uv sync slab pulses. As the
    sentence ends (a ~4 s recap, mostly silent): the panel fades; top left the GREY file row
    `transcribe_audio/Dockerfile · 30 lines`; under it four GREY chips `lines 1–3`, `lines 5–10`,
    `lines 12–21`, `lines 23–30` appear one by one, each drawing thin lines to the slabs and card
    lines it made, which flash YELLOW. Lines to the card stop at its top edge; wires to slabs run
    along a bus above the card and down the gap between card and stack (nothing crosses text).
11  The chips give way to a GREY card headed `README.md · lines 175–225 · Appendix · Sample
    Dockerfile`: line numbers + lines 179, …, 199 and 200 (200 with its indent, cut before its
    `&& \` and ending in a GREY "…"). A GREY tag beside 199: "199–200: extra lines you can leave
    out". Line 179 is barred; `curl` turns RED with a RED tag "no ffmpeg"; a RED stamp "don't
    paste into transcribe_audio" under the card.
12  The appendix card fades. Under the file row a GREY card: "Dockerfile = FROM python:3.12-slim-
    bookworm (README line 41) / + the README's six code blocks, in order: / lines 45 · 50–55 ·
    60–69 · 76–77 · 82–83 · 88–89 / one blank line between blocks → 30 lines, numbered as in this
    video", and ▶ your turn beside the file row (together, so a paused frame shows the recipe);
    `Dockerfile` underlines, the FROM line, the six block numbers, then the blank-line row pulse
    as named ("30 lines" with the file row's "· 30 lines"). Everything fades: empty frame.
"""

from pathlib import Path

import numpy as np
from manim import *

from explainer import style as S
from explainer.components import person_icon
from explainer.devops import (MONO, PANEL, box, chip, code_span, file_glyph, folder_glyph, label,
                              line_bar, mono, mono_line, substring, tag)
from explainer.scene import VoiceScene

from common import (CTR, ERR, INK, LOOKUP, NARRATION, SYSTEM, TOOL, TURN, VENV, ConfigCard,
                    LayerStack, _drop_groups, file_panel, ghost_file, page_token, pkg_dots,
                    readme_card, sans, source_text, src_panel, stamp, strike, tracker, under,
                    your_turn)

SAY = NARRATION["S05"]

# ------------------------------------------------------------------ sources (checked on import)
DF = "files/transcribe_audio.Dockerfile"           # the file a student ends up with (ASSETS.md)
DF_PATH = "transcribe_audio/Dockerfile"
_df = Path(__file__).resolve().parent.parent / "assets" / "terminal" / DF
DF_LINES = _df.read_text(encoding="utf-8").rstrip("\n").split("\n")
assert len(DF_LINES) == 30 and DF_LINES[0] == "FROM python:3.12-slim-bookworm", DF_LINES[:1]
assert DF_LINES[2] == 'ARG DEBIAN_PACKAGES="build-essential ffmpeg"'
assert DF_LINES[8] == "ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv"
assert DF_LINES[9] == "ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json"
assert DF_LINES[25] == "COPY --chown=app:app . ./" and DF_LINES[26] == "RUN uv sync"

CLI = "transcribe_audio/cli.py"
assert source_text(CLI).split("\n")[68].strip() == "ffmpeg.run(stream)"

_ra = source_text("transcribe_audio/README.md").split("\n")
assert "there's no `Dockerfile` in this folder." in _ra[37] and "piece by piece" in _ra[37]
assert "`python:3.12-slim-bookworm`" in _ra[40]
assert "Running containers as root is a security risk." in _ra[71]
README38 = ["Notice: there's no Dockerfile in this folder.",
            "You write it yourself, from scratch, piece by piece — that's the point."]
assert README38[1][:-1] in _ra[37].replace("`", ""), _ra[37]
BLOCKS = [(45, 45), (50, 55), (60, 69), (76, 77), (82, 83), (88, 89)]     # the six code blocks
for a, b in BLOCKS:
    assert _ra[a - 2].startswith("```dockerfile") and _ra[b].startswith("```"), (a, b)
assert [_ra[a - 1] for a, _ in BLOCKS] == [DF_LINES[k] for k in (2, 4, 11, 22, 25, 28)]

_rm = source_text("README.md").split("\n")
APPX = {179: _rm[178], 199: _rm[198], 200: _rm[199]}
assert APPX[179] == 'ARG DEBIAN_PACKAGES="build-essential curl"', APPX[179]
assert APPX[199] == "RUN set -ex; \\", APPX[199]
LOOP = 'for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done'
assert APPX[200] == "    " + LOOP + " && \\", APPX[200]
ROW200 = "    " + LOOP + " …"        # line 200 with its indent; the GREY "…" marks the cut `&& \`
assert _rm[174] == "```dockerfile" and _rm[224] == "```"

# ------------------------------------------------------------------ layout
PT = 20                       # code size: the 10-line RUN panel must fit 12 wide and 4.1 tall
PANEL_LEFT = -6.0             # left edge of every panel's code background (the file stays put)
CODE_TOP = 2.47               # top edge of the code background (its header sits above)
STACK_X, FLOOR_Y = 4.4, -3.45
CARD_C = np.array([-2.25, -2.49, 0])       # ConfigCard(8.4 x 2.12): y -3.55 .. -1.43
ZOOM_W, ZOOM_H = 8.5, 2.12
ZOOM_C = np.array([-2.2, -2.49, 0])        # the RUN slab's zoom, over the card


def df_panel(a: int, b: int) -> VGroup:
    p = file_panel(DF, a, b, DF_PATH, size=PT)
    p.code.background.set_fill(PANEL, 1)
    p.shift(np.array([PANEL_LEFT - p.code.get_left()[0], CODE_TOP - p.code.get_top()[1], 0]))
    p.first = a
    return p


def span(p, n: int, sub: str, occ: int = 0) -> VGroup:
    """Glyphs of `sub` in file line n of panel p."""
    return code_span(p.code, n - p.first, sub, occ)


def row(p, n: int) -> VGroup:
    return p.code.code_lines[n - p.first]


def bar(p, a: int, b: int | None = None, color: str = TURN, opacity: float = 0.16) -> Rectangle:
    """A translucent bar over file lines a..b of panel p."""
    b = a if b is None else b
    ta = line_bar(p.code, a - p.first, color, opacity)
    tb = line_bar(p.code, b - p.first, color, opacity)
    top, bot = ta.get_top()[1], tb.get_bottom()[1]
    r = Rectangle(width=ta.width, height=top - bot, stroke_width=0).set_fill(color, opacity)
    return r.move_to([ta.get_center()[0], (top + bot) / 2, 0])


def caption() -> VGroup:
    """'from transcribe_audio/README.md · lines 41–90' as two rows in the top-right corner."""
    r1 = VGroup(label("from", PT, S.GREY), mono("transcribe_audio/README.md", PT, S.GREY))
    r1.arrange(RIGHT, buff=0.12)
    r2 = label("lines 41–90", PT, S.GREY)
    g = VGroup(r1, r2).arrange(DOWN, aligned_edge=RIGHT, buff=0.08)
    return g.move_to([6.45, 3.47, 0], aligned_edge=UR)


def readme_chip2(where: str, phrase: str) -> VGroup:
    """A README chip on two rows (the path, then the quoted phrase): the one-line chip is wider
    than the room right of the tracker."""
    path, _, rest = where.partition(" · ")
    w = VGroup(mono(path, PT, S.GREY), label(f"· {rest}", PT, S.GREY)).arrange(RIGHT, buff=0.12)
    ph = label(f"“{phrase}”", PT, INK)
    rows = VGroup(w, ph).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    fr = box(rows.width + 0.3, rows.height + 0.24, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.1)
    fr.move_to(rows)
    g = VGroup(fr, rows)
    g.frame, g.where, g.phrase = fr, w, ph
    return g


def small_signpost(h: float = 0.36, color: str = LOOKUP) -> VGroup:
    """A small PINK signpost (an arrow-shaped board on a post), no text."""
    w, bh, tip = h * 0.9, h * 0.42, h * 0.22
    board = Polygon([0, 0, 0], [w, 0, 0], [w + tip, bh / 2, 0], [w, bh, 0], [0, bh, 0],
                    stroke_color=color, stroke_width=2.5).set_fill(color, 0.25)
    post = Line([w * 0.2, 0, 0], [w * 0.2, -(h - bh), 0], color=color, stroke_width=3)
    g = VGroup(post, board)
    return g


def row_tag(text: str, color: str) -> VGroup:
    """A tag that fits inside one 20-pt code row (the house tag is taller than the row pitch)."""
    t = label(text, PT, color)
    h = 0.34
    fr = RoundedRectangle(width=t.width + 0.36, height=h, corner_radius=h / 2, stroke_color=color,
                          stroke_width=2).set_fill(S.BG, 0.95)
    t.move_to(fr)
    g = VGroup(fr, t)
    g.box, g.text = fr, t
    return g


def thin(a, b, color: str = S.GREY, opacity: float = 0.8) -> Line:
    return Line(a, b, color=color, stroke_width=1.8).set_stroke(opacity=opacity)


def wire(pts, color: str = S.GREY, opacity: float = 0.8) -> VMobject:
    """A thin polyline through the corner points `pts` (a wire routed around text)."""
    w = VMobject().set_points_as_corners([np.array(p, dtype=float) for p in pts])
    return w.set_stroke(color, 1.8, opacity)


class WriteDockerfile(VoiceScene):
    # ------------------------------------------------------------- helpers
    # The panel on screen is three scene-level parts that persist across swaps: the frame
    # (self.pbg), the header (self.phead) and the code lines (self.plines, the Code's Paragraph,
    # so code_span() on the current panel addresses the glyphs on screen).
    def type_in(self, p, run_time: float = 1.4, extra=()):
        """The panel's frame appears (its header comes from `extra`), then its characters type in."""
        self.pbg, self.phead, self.plines = p.code.background, p.header, p.code.code_lines
        chars = VGroup(*[ch for ln in p.code.code_lines for ch in ln])
        self.play(FadeIn(self.pbg), *extra, run_time=0.5)
        self.play(ShowIncreasingSubsets(chars, rate_func=linear), run_time=run_time)
        self.remove(chars)
        self.add(self.plines)

    def swap(self, new, extra=(), extra_in=(), run_time: float = 0.95):
        """Scroll the file: the old lines leave upward while the frame resizes and the header
        changes, then the new lines come up from below (two phases: old and new rows never
        overlap). `extra` plays with the first phase, `extra_in` with the second."""
        t_out = round(run_time * 0.4, 2)
        self.play(Transform(self.pbg, new.code.background), Transform(self.phead, new.header),
                  FadeOut(self.plines, shift=UP * 0.25), *extra, run_time=t_out)
        new_lines = [ln for ln in new.code.code_lines if len(ln)]
        lag = LaggedStart(*[FadeIn(ln, shift=UP * 0.2) for ln in new_lines], lag_ratio=0.06)
        self.play(lag, *extra_in, run_time=run_time - t_out)
        _drop_groups(self, [lag])
        self.remove(*new_lines)
        self.plines = new.code.code_lines
        self.add(self.plines)

    def panel_parts(self) -> VGroup:
        return VGroup(self.pbg, self.phead, self.plines)

    def write_card_lines(self, card, items, run_time: float = 1.6, lag: float = 0.25):
        """Several keyword copies turn into card lines together: items (text, colour, key, src)."""
        targets = [card.line(t, c, k) for t, c, k, _ in items]
        anims = [Transform(src, t) for (_, _, _, src), t in zip(items, targets)]
        grp = LaggedStart(*anims, lag_ratio=lag)
        self.play(grp, run_time=run_time)
        _drop_groups(self, [grp])
        for (_, _, _, src), t in zip(items, targets):
            self.remove(src)
            card.add(t)
        return targets

    # ------------------------------------------------------------- the scene
    def construct(self):
        assert len(SAY) == 13, f"S05 has {len(SAY)} SAY lines; this scene times 13"

        tr = tracker("A", 3)
        st = LayerStack()
        st.move_to([STACK_X, FLOOR_Y, 0], aligned_edge=DOWN)
        card = ConfigCard(width=8.4, rows=4, pitch=0.38).move_to(CARD_C)
        cap = caption()

        # ========================================================== 0 · no Dockerfile here
        notice = readme_card("transcribe_audio/README.md · line 38", README38)
        notice.move_to([0, 0.9, 0])
        ghost = ghost_file("Dockerfile")
        p1 = df_panel(1, 3)
        ghost.move_to(p1.header, aligned_edge=LEFT)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.5)
            self.play(tr.goto(4), run_time=0.6)
            vo.wait_until("there's no Dockerfile here")
            self.play(FadeIn(notice, shift=UP * 0.15), run_time=0.6)
            self.play(Create(ghost[0]), FadeIn(ghost[1]), run_time=0.6)
            vo.wait_until("so you write it yourself")
            self.play(Indicate(notice.rows[1], color=TURN, scale_factor=1.04),
                      Create(st.floor), FadeIn(card), run_time=1.0)

        # ========================================================== 1 · line 1: FROM
        note1 = label("line 1: from the README's text, line 41", PT, S.GREY)
        note1.next_to(p1.code, DOWN, buff=0.2).align_to(p1.code, LEFT).shift(RIGHT * 0.12)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(notice, shift=UP * 0.15), run_time=0.4)
            self.type_in(p1, 1.4, extra=[ReplacementTransform(ghost, p1.header), FadeIn(cap)])
            b = bar(p1, 1)
            self.play(FadeIn(b), run_time=0.3)
            vo.wait_until("image on Debian 12")
            st.drop(self, "base", src=span(p1, 1, "FROM").copy(), run_time=0.9)
            vo.wait_until("The README names it")
            self.play(FadeIn(note1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("not in a code block")
            self.play(Indicate(note1, color=INK, scale_factor=1.04), run_time=0.8)

        # ========================================================== 2 · line 3: ARG; ffmpeg
        cli = src_panel(CLI, 67, 69, size=PT)
        cli.code.background.set_fill(PANEL, 1)
        cli.move_to(card.get_corner(DL) + UR * 0.06, aligned_edge=DL)
        back = Rectangle(width=card.width + 0.1, height=card.height + 0.08, stroke_width=0)
        back.set_fill(S.BG, 1).move_to(card)          # the inset covers the card while it is up
        inset = VGroup(back, cli)
        icode = cli.code
        ib = line_bar(icode, 2, TURN)
        # the compact tag: the house tag (0.47 tall) would cover line 68's descenders
        itag = row_tag("runs the ffmpeg program", S.GREY)
        itag.next_to(icode.code_lines[2], RIGHT, buff=0.3).set_y(ib.get_y())
        assert itag.get_right()[0] < icode.background.get_right()[0] - 0.05, itag.get_right()
        with self.voiceover(SAY[2]) as vo:
            self.play(Transform(b, bar(p1, 3)), FadeOut(note1), run_time=0.5)
            vo.wait_until("a variable that exists")
            card.write(self, "DEBIAN_PACKAGES · build time only", SYSTEM, key="arg",
                       src=span(p1, 3, "ARG").copy(), run_time=0.9)
            self.play(Indicate(card.lines["arg"], color=SYSTEM, scale_factor=1.06), run_time=0.7)
            vo.wait_until("the Debian packages")
            u_ff = under(span(p1, 3, "ffmpeg"), TURN)
            self.play(Indicate(span(p1, 3, "build-essential"), color=SYSTEM, scale_factor=1.1),
                      run_time=0.7)
            self.play(Create(u_ff), Indicate(span(p1, 3, "ffmpeg"), color=SYSTEM, scale_factor=1.15),
                      run_time=0.7)
            vo.wait_until("The Python package")
            self.play(FadeIn(inset, shift=RIGHT * 0.6), run_time=0.7)
            vo.wait_until("just runs the ffmpeg program")
            self.play(FadeIn(ib), FadeIn(itag, shift=LEFT * 0.1), run_time=0.5)

        # ========================================================== 3 · lines 5-10: six ENV
        p5 = df_panel(5, 10)
        env = [("no apt questions", "e1", 5, "DEBIAN_FRONTEND=noninteractive"),
               ("Unicode text", "e2", 6, "LANG=C.UTF-8"),
               ("print at once", "e3", 7, "PYTHONUNBUFFERED=1"),
               ("uv copies files", "e4", 8, "UV_LINK_MODE=copy"),
               ("venv location", "uv", 9, None),
               ("key location", "gac", 10, None)]
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(inset, shift=LEFT * 0.6), FadeOut(ib), FadeOut(itag), run_time=0.5)
            self.swap(p5, extra=[FadeOut(b), FadeOut(u_ff)])
            b = bar(p5, 5, 10)
            self.play(FadeIn(b), run_time=0.4)
            vo.wait_until("As in lecture 2")
            items = [(t, INK, k, span(p5, n, "ENV").copy()) for t, k, n, _ in env]
            self.write_card_lines(card, items, run_time=2.0, lag=0.22)
            vo.wait_until("no layers")
            self.play(Indicate(card.title, color=CTR, scale_factor=1.1), run_time=0.8)
            vo.wait_until("The first four")
            self.play(Transform(b, bar(p5, 5, 8)), run_time=0.5)
            for (t, k, n, val), phrase in zip(env[:4], ["apt never asks", "text is Unicode",
                                                         "Python prints at once", "and uv copies"]):
                vo.wait_until(phrase)
                self.play(Indicate(card.lines[k], color=TURN, scale_factor=1.15),
                          Indicate(span(p5, n, val), color=TURN, scale_factor=1.03), run_time=0.8)

        # ========================================================== 4 · line 9: the venv outside /app
        with self.voiceover(SAY[4]) as vo:
            self.play(Transform(b, bar(p5, 9)), run_time=0.5)
            vo.wait_until("it tells uv")
            self.play(card.restyle("uv", "the venv lives in /home/app/.venv · outside /app", VENV),
                      run_time=1.0)
            vo.wait_until("in slash home")
            # no underline here: under row 9 it would sit on row 10's capitals
            v_path = span(p5, 9, "/home/app/.venv")
            self.play(v_path.animate.set_color(VENV), run_time=0.5)
            self.play(Indicate(v_path, color=VENV, scale_factor=1.12), run_time=0.7)
            vo.wait_until("outside slash app")
            self.play(Indicate(card.lines["uv"], color=VENV, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Soon, this line")
            rem = row_tag("remember this line", TURN)
            rem.next_to(row(p5, 9), RIGHT, buff=0.4).set_y(row(p5, 9).get_y() + 0.06)
            self.play(FadeIn(rem, shift=LEFT * 0.1), run_time=0.4)
            self.play(Wiggle(rem, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.8)

        # ========================================================== 5 · line 10: where the key is
        post = small_signpost()
        with self.voiceover(SAY[5]) as vo:
            self.play(Transform(b, bar(p5, 10)), FadeOut(rem), run_time=0.5)
            vo.wait_until("where the key is")
            self.play(card.restyle("gac", "where the key is · a relative path", LOOKUP), run_time=0.9)
            # the glyph is a member of the card but NOT one of its config lines (card.lines):
            # it sits right after the credentials line; USER app is shifted past it in beat 9
            post.next_to(card.lines["gac"], RIGHT, buff=0.18).align_to(card.lines["gac"], DOWN)
            card.attach(self, post, anims=[GrowFromEdge(post, DOWN)], run_time=0.4)
            vo.wait_until("secrets, slash")
            u_sec = under(span(p5, 10, "secrets/"), LOOKUP)
            self.play(Create(u_sec), span(p5, 10, "secrets/").animate.set_color(LOOKUP), run_time=0.7)
            vo.wait_until("a relative path")
            self.play(Indicate(card.lines["gac"], color=LOOKUP, scale_factor=1.08),
                      Indicate(span(p5, 10, "secrets/"), color=LOOKUP, scale_factor=1.15), run_time=0.9)

        # ========================================================== 6 · lines 12-21: one RUN, one layer
        p12 = df_panel(12, 21)
        zoom_bg = Rectangle(width=ZOOM_W, height=ZOOM_H, stroke_width=0).set_fill(S.BG, 1)
        zoom_fr = box(ZOOM_W, ZOOM_H, SYSTEM, fill_opacity=0.1, radius=0.1)
        zoom = VGroup(zoom_bg, zoom_fr).move_to(ZOOM_C)
        zx0 = zoom.get_left()[0]
        yg, yl = -1.95, -2.52                      # glyph row, label row
        pages = VGroup(*[page_token() for _ in range(3)])
        for i, pg in enumerate(pages):
            pg.move_to([zx0 + 0.63 + 0.22 * i, yg - 0.06 * i, 0]).rotate(0.12 - 0.12 * i)
        lab_lists = sans("apt lists", PT, S.GREY).move_to([zx0 + 0.85, yl, 0])
        gone = strike(lab_lists, S.GREY, 3)        # the label is struck through: deleted
        dots = pkg_dots(18, cols=6, color=SYSTEM).move_to([zx0 + 2.95, yg, 0])
        lab_pk = sans("build-essential, ffmpeg", PT, S.GREY).move_to([zx0 + 2.95, yl, 0])
        with self.voiceover(SAY[6]) as vo:
            self.swap(p12, extra=[FadeOut(b), FadeOut(u_sec)])
            vo.wait_until("ends in a backslash")
            slashes = [span(p12, n, "\\") for n in range(12, 21)]
            self.play(LaggedStart(*[Indicate(a, color=TURN, scale_factor=1.3) for a in slashes],
                                  lag_ratio=0.12), run_time=1.1)
            vo.wait_until("and double ampersands")
            amps = [span(p12, n, "&&") for n in range(12, 21)]
            self.play(LaggedStart(*[Indicate(a, color=TURN, scale_factor=1.3) for a in amps],
                                  lag_ratio=0.12), run_time=1.1)
            vo.wait_until("so they make one layer")
            b = bar(p12, 12, 21)
            self.play(FadeIn(b), run_time=0.3)
            apt = st.drop(self, "apt", src=span(p12, 12, "RUN").copy(), run_time=0.8)
            # the slab zooms up: an ORANGE inset over the card, dashed lines back to the slab
            zl = VGroup(DashedLine(apt.box.get_corner(UL), zoom.get_corner(UR), color=SYSTEM,
                                   stroke_width=2, dash_length=0.08),
                        DashedLine(apt.box.get_corner(DL), zoom.get_corner(DR), color=SYSTEM,
                                   stroke_width=2, dash_length=0.08))
            zoom.save_state()
            zoom.replace(apt.box, stretch=True)
            self.play(Restore(zoom), Create(zl), run_time=0.8)
            vo.wait_until("It updates Debian")
            self.play(Transform(b, bar(p12, 12)), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(pg, shift=DOWN * 0.15) for pg in pages], lag_ratio=0.3),
                      FadeIn(lab_lists), run_time=0.7)
            vo.wait_until("installs our packages")
            self.play(Transform(b, bar(p12, 13, 14)), run_time=0.3)
            self.play(LaggedStart(*[FadeIn(d, scale=0.4) for d in dots], lag_ratio=0.08),
                      FadeIn(lab_pk), run_time=1.0)
            vo.wait_until("and deletes the apt")
            self.play(Transform(b, bar(p12, 15, 16)), run_time=0.3)
            self.play(*[pg.animate.scale(0.12).rotate(1.2).set_opacity(0) for pg in pages],
                      run_time=0.9)
            self.remove(pages)
            vo.wait_until("so they cost nothing")
            # struck through in the zoom; the slab on the stack (what the image keeps) pulses
            self.play(Create(gone), lab_lists.animate.set_opacity(0.55),
                      Indicate(apt.box, color=SYSTEM, scale_factor=1.06), run_time=0.8)

        # ========================================================== 7 · pip, uv
        pip_c = chip("pip", SYSTEM, size=PT, font=MONO)
        uv_c = chip("uv", TOOL, size=PT, font=MONO, fill_opacity=0.3)
        VGroup(pip_c, uv_c).arrange(RIGHT, buff=0.18).move_to([zx0 + 5.15, yg, 0])
        note7 = VGroup(label("this Python is the image's own (/usr/local),", PT, S.GREY),
                       label("not Debian's → pip may install", PT, S.GREY))
        note7.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        note7.move_to([zx0 + 0.3, -3.06, 0], aligned_edge=LEFT)
        with self.voiceover(SAY[7]) as vo:
            self.play(Transform(b, bar(p12, 17, 18)), run_time=0.4)
            vo.wait_until("upgrades pip")
            self.play(FadeIn(pip_c, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("and installs uv")
            self.play(FadeIn(uv_c, shift=DOWN * 0.5), run_time=0.6)
            vo.wait_until("Unlike Debian's")
            self.play(FadeIn(note7[0], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("this Python belongs")
            self.play(FadeIn(note7[1], shift=UP * 0.1), run_time=0.6)
            vo.wait_until("so pip may install")
            self.play(Indicate(pip_c, color=SYSTEM, scale_factor=1.2), run_time=0.8)

        # ========================================================== 8 · user app owns /app
        who = person_icon(S.GREY, height=0.5).move_to([zx0 + 6.65, yg, 0])
        lab_who = sans("app · uid 1000", PT, S.GREY).move_to([who.get_x(), yl, 0])
        fold = folder_glyph(0.42, CTR)
        fold.move_to([zx0 + 8.05, yg, 0])
        lab_app = mono("/app", PT, CTR).move_to([fold.get_x(), yl, 0])
        own = Arrow(who.get_right() + RIGHT * 0.05, fold.get_left() + LEFT * 0.05, buff=0.05,
                    color=S.GREY, stroke_width=3, max_tip_length_to_length_ratio=0.25)
        own_t = sans("owns", PT, S.GREY).next_to(own, UP, buff=0.06)
        r72 = readme_chip2("transcribe_audio/README.md · line 72",
                           "Running containers as root is a security risk.")
        r72.move_to([6.55, 3.5, 0], aligned_edge=UR)
        assert r72.get_left()[0] > tr.get_right()[0] + 0.15, (r72.get_left(), tr.get_right())
        inside = VGroup(lab_lists, gone, dots, lab_pk, pip_c, uv_c, note7, who, lab_who, fold,
                        lab_app, own, own_t)
        with self.voiceover(SAY[8]) as vo:
            self.play(Transform(b, bar(p12, 19, 21)), run_time=0.4)
            vo.wait_until("it creates a user")
            self.play(FadeIn(who, shift=UP * 0.15), FadeIn(lab_who), run_time=0.6)
            vo.wait_until("who owns slash app")
            self.play(GrowArrow(own), FadeIn(own_t), FadeIn(fold), FadeIn(lab_app), run_time=0.7)
            vo.wait_until("as the README says")
            self.play(FadeOut(cap), FadeIn(r72, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("running as root")
            self.play(Indicate(r72.phrase, color=INK, scale_factor=1.04), run_time=0.8)
            # the slab settles back onto the stack
            self.play(FadeOut(inside, shift=(apt.box.get_center() - inside.get_center()) * 0.25),
                      zoom.animate.replace(apt.box, stretch=True).set_opacity(0),
                      Uncreate(zl), FadeOut(b), run_time=1.0)
            self.remove(inside, zoom, zl)
            self.play(Indicate(apt.box, color=SYSTEM, scale_factor=1.04), run_time=0.5)

        # ========================================================== 9 · lines 23-26: USER, WORKDIR, COPY
        p23 = df_panel(23, 30)
        ev = VGroup(sans("=", PT, INK), sans("everything", PT, INK), sans("in this folder", PT, INK))
        ev.arrange(RIGHT, buff=0.12)
        with self.voiceover(SAY[9]) as vo:
            self.swap(p23, extra=[FadeOut(r72), FadeIn(cap)])
            b = bar(p23, 23, 24)
            self.play(FadeIn(b), run_time=0.3)
            vo.wait_until("switch to that user")
            user = card.line("USER app", INK, key="user")          # flow position after gac ...
            if abs(user.get_y() - post.get_y()) < 0.3 and user.get_left()[0] < post.get_right()[0] + 0.3:
                user.shift(RIGHT * (post.get_right()[0] + 0.4 - user.get_left()[0]))   # ... past the glyph
            assert user.get_right()[0] < card.frame.get_right()[0] - 0.15, user.get_right()
            u_src = span(p23, 23, "USER").copy()
            self.play(Transform(u_src, user), run_time=0.8)
            self.remove(u_src)
            card.add(user)
            vo.wait_until("and make slash app")
            st.drop(self, "workdir", src=span(p23, 24, "WORKDIR").copy(), run_time=0.8)
            vo.wait_until("Line 26 copies")
            self.play(Transform(b, bar(p23, 26)), run_time=0.4)
            st.drop(self, "copy", src=span(p23, 26, "COPY").copy(), run_time=0.8)
            st.attach(self, st.files("copy", key=True),
                      anims=None, run_time=0.5)
            dot = span(p23, 26, ".")
            u_dot = under(dot, TURN)
            ev.next_to(row(p23, 26), RIGHT, buff=0.45)
            self.play(Create(u_dot), FadeIn(ev, shift=LEFT * 0.1), run_time=0.6)
            vo.wait_until("hold on to that word")
            u_ev = under(ev[1], TURN)
            self.play(Create(u_ev), ev[1].animate.set_color(TURN), run_time=0.6)
            self.play(Indicate(ev[1], color=TURN, scale_factor=1.15), run_time=0.8)

        # ========================================================== 10 · uv sync, start label; recap
        fr_icon = file_glyph(0.5, S.GREY)
        fr_name = mono(DF_PATH, 22, INK)
        fr_n = label("· 30 lines", 22, S.GREY)
        frow = VGroup(fr_icon, fr_name, fr_n).arrange(RIGHT, buff=0.16)
        frow.move_to([-6.25, 2.3, 0], aligned_edge=LEFT)
        chips = VGroup(*[chip(f"lines {a}–{b_}", S.GREY, size=PT) for a, b_ in
                         [(1, 3), (5, 10), (12, 21), (23, 30)]])
        chips.arrange(RIGHT, buff=0.35).move_to([-6.0, 1.2, 0], aligned_edge=LEFT)
        pj = VGroup(label("from", PT, S.GREY), mono("pyproject.toml", PT, VENV))
        pj.arrange(RIGHT, buff=0.12)
        with self.voiceover(SAY[10]) as vo:
            self.play(Transform(b, bar(p23, 27)), FadeOut(u_dot), FadeOut(u_ev), FadeOut(ev),
                      run_time=0.4)
            vo.wait_until("runs uv sync")
            st.drop(self, "sync", src=span(p23, 27, "RUN uv sync").copy(), run_time=0.9)
            vo.wait_until("from pyproject.toml")
            pj.next_to(row(p23, 27), RIGHT, buff=0.45)
            self.play(FadeIn(pj, shift=LEFT * 0.1),
                      Indicate(st.slabs["sync"].box, color=VENV, scale_factor=1.06), run_time=0.7)
            vo.wait_until("and lines 29 and 30")
            self.play(Transform(b, bar(p23, 29, 30)), FadeOut(pj), run_time=0.4)
            vo.wait_until("start bash")
            top = st.top_label()
            srcs = VGroup(span(p23, 29, "ENTRYPOINT").copy(), span(p23, 30, "CMD").copy())
            st.attach(self, top, anims=[ReplacementTransform(srcs, top)], run_time=0.9)
            vo.wait_until("as in lecture 2")
            self.play(Indicate(top, color=CTR, scale_factor=1.1), run_time=0.8)
            # the recap starts as the sentence ends: four chunks of the file made these pieces.
            # Lines to card lines stop at the card's top edge; wires to slabs run along a bus
            # above the card and down the gap between card and stack, so nothing crosses text.
            self.play(FadeOut(self.panel_parts()), FadeOut(b), FadeOut(cap),
                      FadeIn(frow, shift=RIGHT * 0.2), run_time=0.6)
            card_top = card.frame.get_top()[1]
            gx = (card.frame.get_right()[0] + st.slabs["base"].box.get_left()[0]) / 2
            bus = card_top + 0.45
            assert bus < top.get_bottom()[1] or gx < top.get_left()[0] - 0.3
            targets = [
                ([card.lines["arg"]], [st.slabs["base"].box]),
                ([card.lines[k] for k in ("e1", "e2", "e3", "e4", "uv", "gac")], []),
                ([], [st.slabs["apt"].box]),
                ([card.lines["user"]], [st.slabs[k].box for k in ("workdir", "copy", "sync")] + [top]),
            ]
            prev = None
            for c, (clines, pieces) in zip(chips, targets):
                ls = []
                for m in clines:
                    x = float(np.clip(m.get_x(), card.frame.get_left()[0] + 0.3,
                                      card.frame.get_right()[0] - 0.3))
                    ls.append(thin(c.get_bottom(), [x, card_top, 0]))
                for m in pieces:
                    cb, end = c.get_bottom(), m.get_left() + LEFT * 0.06
                    ls.append(wire([cb, [cb[0], bus, 0], [gx, bus, 0], [gx, end[1], 0], end]))
                ls = VGroup(*ls)
                flash = [Indicate(m, color=TURN, scale_factor=1.05) for m in clines + pieces]
                fade = [prev.animate.set_stroke(opacity=0.0)] if prev is not None else []
                self.play(FadeIn(c, shift=DOWN * 0.1), Create(ls), *flash, *fade, run_time=0.8)
                if prev is not None:
                    self.remove(prev)
                prev = ls
            self.play(prev.animate.set_stroke(opacity=0.0), run_time=0.3)
            self.remove(prev)

        # ========================================================== 11 · the appendix sample
        gut = 0.75
        rws = VGroup()
        for n, s_ in [("179", APPX[179]), ("…", ""), ("199", APPX[199]), ("200", ROW200)]:
            num = mono_line(n, PT, S.GREY)
            txt = mono_line(s_, PT, INK)
            if s_ == ROW200:
                substring(txt, "…").set_color(S.GREY)
            txt.shift(num.strut.get_corner(UL) + RIGHT * gut - txt.strut.get_corner(UL))
            rws.add(VGroup(num, txt))
        rws.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        inner = rws
        afr = box(inner.width + 0.6, inner.height + 0.44, S.GREY, fill=S.BG, fill_opacity=0.95,
                  radius=0.12)
        afr.move_to(inner)
        ahead = VGroup(mono("README.md", PT, S.GREY), label("· lines 175–225 · Appendix · Sample Dockerfile",
                                                              PT, S.GREY))
        ahead.arrange(RIGHT, buff=0.12).next_to(afr, UP, buff=0.08).align_to(afr, LEFT).shift(RIGHT * 0.1)
        appx = VGroup(afr, inner, ahead)
        appx.move_to([0.0, 0.0, 0]).align_to(frow, DOWN).shift(DOWN * (0.24 + appx.height))
        assert afr.get_left()[0] > -6.55 and afr.get_right()[0] < 6.55, afr.width
        r179 = rws[0]
        curl = substring(r179[1], "curl")
        b179 = Rectangle(width=afr.width - 0.2, height=r179.height + 0.14, stroke_width=0)
        b179.set_fill(TURN, 0.16).move_to([afr.get_x(), r179.get_y(), 0])
        noff = tag("no ffmpeg", ERR).next_to(r179, RIGHT, buff=0.35)
        # rows 199-200 are the appendix's extras (BRIEF: "it adds set -ex and the man-page loop")
        # a row-high tag (the house tag is taller than the row pitch and grazed row 200's glyphs),
        # centred on row 199's strut
        xtra = row_tag("199–200: extra lines you can leave out", S.GREY)
        xtra.next_to(rws[2], RIGHT, buff=0.35).set_y(rws[2][1].strut.get_y())
        nopaste = stamp("don't paste into transcribe_audio", ERR, size=PT, angle=0.04)
        nopaste.next_to(afr, DOWN, buff=0.1).align_to(afr, LEFT).shift(RIGHT * 0.35)
        assert nopaste.get_bottom()[1] > card.get_top()[1] + 0.05, nopaste.get_bottom()
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(chips, shift=DOWN * 0.1), FadeIn(appx, shift=UP * 0.1), run_time=0.8)
            self.play(FadeIn(xtra, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("but its build argument")
            self.play(FadeIn(b179), run_time=0.4)
            vo.wait_until("has curl instead")
            self.play(curl.animate.set_color(ERR), FadeIn(noff, shift=LEFT * 0.1), run_time=0.6)
            self.play(Indicate(curl, color=ERR, scale_factor=1.3), run_time=0.7)
            vo.wait_until("don't paste it")
            self.play(FadeIn(nopaste, scale=1.4), run_time=0.5)

        # ========================================================== 12 · your turn: write it
        fl = VGroup(sans("Dockerfile =", PT, INK), mono("FROM python:3.12-slim-bookworm", PT, INK),
                    label("(README line 41)", PT, S.GREY)).arrange(RIGHT, buff=0.18)
        sl = label("+ the README's six code blocks, in order:", PT, INK)
        nums = VGroup(*[mono(f"{a}" if a == b_ else f"{a}–{b_}", PT, INK) for a, b_ in BLOCKS])
        seps = [label("·", PT, S.GREY) for _ in BLOCKS[1:]]
        bl = VGroup(label("lines", PT, S.GREY))
        for i, n in enumerate(nums):
            if i:
                bl.add(seps[i - 1])
            bl.add(n)
        bl.arrange(RIGHT, buff=0.16)
        # the layout rule that keeps the student's line numbers equal to the video's (S06's
        # Docker warning names "line 10", S07 names lines 9 and 10)
        GAP_A, GAP_B = "one blank line between blocks →", "30 lines, numbered as in this video"
        gap = label(f"{GAP_A} {GAP_B}", PT, INK)           # one Text: one baseline, real spacing
        _na = len("".join(GAP_A.split()))                   # Text has no glyphs for spaces
        assert len(gap) == _na + len("".join(GAP_B.split())), len(gap)
        gap_a, gap_b = gap[:_na], gap[_na:]
        rows3 = VGroup(fl, sl, bl, gap).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        ffr = box(rows3.width + 0.6, rows3.height + 0.45, S.GREY, fill=S.BG, fill_opacity=0.95,
                  radius=0.12).move_to(rows3)
        final = VGroup(ffr, rows3).next_to(frow, DOWN, buff=0.45).align_to(frow, LEFT)
        yt = your_turn().next_to(frow, RIGHT, buff=0.4)
        u_name = under(fr_name[-10:], TURN)
        with self.voiceover(SAY[12]) as vo:
            self.play(FadeOut(appx), FadeOut(b179), FadeOut(noff), FadeOut(xtra), FadeOut(nopaste),
                      run_time=0.4)
            self.play(FadeIn(final, shift=UP * 0.1), FadeIn(yt, shift=LEFT * 0.1), run_time=0.5)
            self.play(Wiggle(yt, scale_value=1.12, rotation_angle=0.02 * TAU), run_time=0.7)
            vo.wait_until("a file named Dockerfile")
            self.play(Create(u_name), run_time=0.5)
            vo.wait_until("with no extension")
            self.play(Indicate(fr_name[-10:], color=TURN, scale_factor=1.12), run_time=0.7)
            vo.wait_until("Type the FROM line")
            self.play(Indicate(fl[1], color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("then copy the README's")
            self.play(LaggedStart(*[Indicate(n, color=TURN, scale_factor=1.25) for n in nums],
                                  lag_ratio=0.35), run_time=2.0)
            vo.wait_until("with one blank line")
            self.play(Indicate(gap_a, color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("so your line numbers")
            self.play(Indicate(gap_b, color=TURN, scale_factor=1.06),
                      Indicate(fr_n, color=TURN, scale_factor=1.12), run_time=0.8)
            self.wait(max(0.05, vo.remaining(0.05)))
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
