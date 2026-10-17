"""S04 · One script, two containers (README "Run Container" step 3). Lecture: none (no lecture tag).

Beats (script.md "## S04", one voiceover block each):
 0  TRACKER Run 3. A recap strip at the top, glyph-only pictures with GREY captions: two TEAL boxes
    on a rail ("lecture 4") and a GOLD key through a PINK route into a TEAL box ("lecture 3");
    both slide into one empty GREY laptop outline, centre, captioned "today: both at once"; inside
    it two GREY folders llm-rag/ and secrets/ side by side.
 1  The laptop moves to the upper left. Bottom: the PANEL docker-shell.sh · line 7 · after your
    edit (laptop/06 line 11 without its "+") over CODE(docker-shell.sh: 8–12) (line 8 wrapped).
    The three export lines light in turn as named; a PINK value chip lifts off each
    (your-project-id, /secrets/llm-service-account.json, llm-rag-cli) to the right of the laptop.
    Line 12 lights YELLOW, "--rm" flashes, and the llm-rag-cli chip drops onto $IMAGE_NAME.
 2  The script panels leave; the laptop becomes V2's GREY laptop zone (V2 fitted to the top, two
    chips wait at the right). A 3-row code strip along the bottom edge: CODE(docker-compose.yml:
    1–3) lays the TEAL rail llm-rag-network (line 3 lit); it Transforms into CODE(6–8): the TEAL
    "CLI container" box on the rail (line 6), then the GREEN "build: ." chip (line 8).
 3  CODE(10–12): the PINK route llm-rag/ → /app (line 12), then secrets/ → /secrets (line 11).
    CODE(13–15) (line 14 wrapped): two empty PINK "$" slots open on the box and the two waiting
    chips drop into them (lines 14, 15). CODE(16–17): the dashed "depends on" arrow to an empty
    dashed TEAL outline on the right.
 4  CODE(18–20): the BLUE Docker Hub shelf with chromadb/chroma:latest; a copy of the image flies
    into the outline, which fills as the "Chroma container" (line 19); its name tag
    llm-rag-chromadb (line 20). CODE(21–22): the GREY street door :8000 and the PINK 8000:8000
    arrow. CODE(23–24): docker-volumes/chromadb/ appears on the laptop with the PINK route to /data.
    The strip becomes an excerpt chip of line 26 with a GREY tag "lets the course's web tools in
    · S09".
 5  The strip leaves; CODE(Dockerfile: 18) and CODE(Dockerfile: 45) as two one-line panels. The
    GREEN /.venv appears inside the CLI box, outside /app; the /app route pulses and a GREY sheet
    "your repo" covers /app only (/.venv stays visible). A pencil edits a cli.py row on the laptop,
    the file blinks on both sides, GREY tag "no rebuild".
 6  The picture shrinks to the top: a glyph-only thumbnail of V2 (everything the run creates is
    a faint plan) and, beside it, the Docker Hub shelf at full size. Terminal (9 rows, `laptop`,
    ~/AC215/llm-rag) types `sh docker-shell.sh` -> laptop/07 lines 2–5; as lines 3–5 print, the
    image flies from the shelf into the thumbnail, the rail fills in, the Chroma box fills in.
    GREY tag on the row under line 5: "first build also pulls python:3.12-slim-bookworm (about
    48 MB)".
 7  laptop/07 line 6 and lines 7–8 joined (folded at spaces), RED; on the shelf an empty dashed
    slot llm-rag-cli flashes RED; the RED rows fade to GREY with a "harmless" tag.
 8  laptop/07 lines 9–10, 21, 22, 25, 26, …, 36 (BuildKit rows cut, times as GREY tags): 81.5s
    underlined YELLOW; TEAL badges "build step 2", "5", "6"; 112.26MB YELLOW. The terminal shrinks to
    the 3-row strip; above it a GREEN parcel "build context · 112 MB" opens: a big GREY block
    ".git · 103 MB" (laptop/05b) holding a small GREEN cylinder (the old database copy), a sliver
    "the rest" with a tiny GREEN chroma.sqlite3 (laptop/14b); an erratum tag "no .dockerignore →
    exercises" and a GREY caption "the mounts hide both at run time".
 9  The parcel leaves, the terminal grows back: laptop/07 lines 37–44. The run-container name
    (line 38) underlines GREY and the thumbnail's CLI box fills in; line 40 gets "Apple Silicon:
    aarch64 · both native"; 3.12.15 and 0.13.1 underline GREY + "at the time of recording";
    lines 41 and 44 get a GREY bracket and an erratum tag "says it before it does · cosmetic".
10  The prompt of line 45 alone (app@92c5bfd26089:/app$, nothing typed); the frame turns TEAL,
    title "container · llm-rag-cli"; the id underlines GREY + tag "container id · your numbers
    will differ"; the thumbnail's CLI box lights YELLOW; ▶ your turn. Hold 2 s, empty frame.
"""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    ManimColor,
    Polygon,
    ReplacementTransform,
    RoundedRectangle,
    Text,
    Transform,
    VGroup,
    VMobject,
)

import common as _common
from common import (
    BOTTOM,
    CTR,
    DATA,
    ERR,
    INK,
    LAPTOP,
    LOOKUP,
    NARRATION,
    P_CTR,
    P_REPO,
    TURN,
    ComposeView,
    at_bottom,
    beside,
    build_badge,
    capture,
    col_box,
    cylinder,
    enter_container,
    erratum_tag,
    excerpt,
    excerpt_chip,
    file_row,
    grey_tag,
    harmless_tag,
    key_glyph,
    note,
    pencil,
    pin,
    print_build,
    recording_tag,
    resize,
    sans,
    source_text,
    split_prompt,
    src_panel,
    term,
    tracker,
    type_cmd,
    under,
    your_turn,
)
from explainer import style as S
from explainer.devops import (
    CAPTION,
    MONO,
    TAG,
    box,
    chip,
    code_panel,
    code_span,
    folder_glyph,
    label,
    mono,
    substring,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S04"]

# ------------------------------------------------------------------ the real files and outputs
COMPOSE = "docker-compose.yml"
SHELL = "docker-shell.sh"
_c = source_text(COMPOSE).split("\n")
assert _c[2].strip() == "name: llm-rag-network" and _c[5].strip() == "llm-rag-cli:", _c[:6]
assert _c[7].strip() == "build: ." and _c[10].strip() == "- ../secrets:/secrets", _c[6:11]
assert _c[11].strip() == "- ../llm-rag:/app" and "GOOGLE_APPLICATION_CREDENTIALS" in _c[13], _c[11:14]
assert _c[14].strip() == "GCP_PROJECT: $GCP_PROJECT" and _c[16].strip() == "- chromadb", _c[14:17]
assert _c[18].strip() == "image: chromadb/chroma:latest" and _c[19].strip() == "container_name: llm-rag-chromadb"
assert _c[21].strip() == "- 8000:8000" and _c[23].strip() == "- ./docker-volumes/chromadb:/data", _c[20:24]
CORS = "CHROMA_CORS_ALLOW_ORIGINS: '[\"https://ac215-llm-rag.dlops.io\""   # line 26 (excerpt)
_s = source_text(SHELL).split("\n")
assert _s[7].startswith('export GOOGLE_APPLICATION_CREDENTIALS="/secrets/') and _s[8] == 'export IMAGE_NAME="llm-rag-cli"'
assert _s[11] == "docker compose run --rm $IMAGE_NAME", _s[11]
_d = source_text("Dockerfile").split("\n")
assert _d[17] == "ENV UV_PROJECT_ENVIRONMENT=/.venv" and _d[44] == "RUN uv sync --frozen", (_d[17], _d[44])

_diff = capture("06", "laptop")
assert _diff.cmd == "git diff docker-shell.sh"
LINE7 = _diff.line(11)
assert LINE7.startswith('+export GCP_PROJECT="your-project-id"'), LINE7
LINE7 = LINE7[1:]                                       # the line as it is now in your file

RUN = capture("07", "laptop")
assert RUN.cmd == "sh docker-shell.sh" and RUN.exit == 0, RUN.cmd
assert "Pulled" in RUN.line(3) and "Network llm-rag-network" in RUN.line(4), RUN.lines[:4]
assert RUN.line(6) == "Image llm-rag-cli Pulling" and RUN.line(8).endswith("not found"), RUN.lines[4:7]
assert "Building 81.5s" in RUN.line(10) and "112.26MB" in RUN.line(21), (RUN.line(10), RUN.line(21))
assert "[2/6]" in RUN.line(22) and "[5/6]" in RUN.line(25) and "[6/6]" in RUN.line(26)
assert RUN.line(36) == "Image llm-rag-cli Built" and "x86_64" in RUN.line(40)
assert "3.12.15" in RUN.line(42) and "0.13.1" in RUN.line(43) and RUN.line(44).startswith("Activating")
assert split_prompt(RUN.line(45)) == (P_CTR, "exit"), RUN.line(45)
CTR_NAME = "llm-rag-llm-rag-cli-run-90678535ddef"
assert CTR_NAME in RUN.line(38), RUN.line(38)
# BuildKit's [2/6] row: cut earlier than the generic 58 (with its "…") so its TEAL badge fits
# before the time tag; the time field stays the capture's own (build_row splits it off)
_r22 = RUN.line(22)
ROW22 = _r22[:_r22.index("-ex;") + 4] + " …   " + _r22.split()[-1]
assert _r22.split()[-1] == "20.2s", _r22

_git = capture("05b", "laptop")
assert _git.line(2).startswith("103M"), _git.line(2)        # .git is 103 MB
_img = capture("14b", "laptop")
assert _img.line(7).endswith("chroma.sqlite3"), _img.line(7)  # the image keeps a chroma.sqlite3

# ------------------------------------------------------------------ layout
TOP_Y = 2.82                  # nothing above this left of x = -2.8 (the tracker band)
CV_BOTTOM = -1.05             # V2's laptop zone ends here: room for the 4-row strip (lines 13–15)
KY = 0.85                     # V2 squeezed in height only (fit_v2): the zone then ends at y 2.78
TERM_ROWS = 9                 # beats 6–10 (SHOW: 12; 9 leaves the picture legible above it)
PARK_X = 6.4                  # right edge of the waiting value chips (beat 2)
RUN_PARTS = ("rail", "plug_cli", "plug_chroma", "chroma", "port_chip", "door", "cli", "venv", "slots",
             "build", "depends", "route_app", "route_secrets", "route_data", "route_port")
CLI_PARTS = ("cli", "venv", "slots", "build", "plug_cli", "depends", "route_app", "route_secrets")


# ------------------------------------------------------------------ small helpers
def at_left(m, x: float, y: float):
    """Put m's left edge at x and its centre at height y."""
    return m.shift(np.array([x - m.get_left()[0], y - m.get_center()[1], 0]))


def attach(scene, row, *mobs):
    """Make mobs (already on screen) part of terminal row `row`: they scroll and fade with it."""
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def strip(a: int, b: int, wrap=None):
    """A code strip of docker-compose.yml lines a–b along the bottom edge."""
    return at_bottom(src_panel(COMPOSE, a, b, wrap=wrap))


def value_chip(s: str) -> VGroup:
    """A PINK value chip (an exported value), opaque so it can travel over anything."""
    c = chip(s, LOOKUP, size=CAPTION, font=MONO, fill_opacity=1)
    c.box.set_fill(ManimColor(S.BG).interpolate(ManimColor(LOOKUP), 0.18), 1)
    return c


def ghost(m, k: float = 0.2):
    """Fade m to k of its own opacities at once (the thumbnail's plan: what the run will create)."""
    for f in m.get_family():
        if isinstance(f, VMobject):
            f._gop = (f.get_fill_opacity(), f.get_stroke_opacity())
            f.set_fill(opacity=f._gop[0] * k, family=False)
            f.set_stroke(opacity=f._gop[1] * k, family=False)
    return m


def unghost(m) -> Transform:
    """Animation: m back to its own opacities (the run made it real)."""
    target = m.copy()
    for f in target.get_family():
        op = getattr(f, "_gop", None)
        if isinstance(f, VMobject) and op is not None:
            f.set_fill(opacity=op[0], family=False)
            f.set_stroke(opacity=op[1], family=False)
    return Transform(m, target)


def l04_mini() -> VGroup:
    """Lecture 4 in one glyph: two TEAL boxes on a rail (port_toy's two containers, one network)."""
    rail = Line([-1.25, 0, 0], [1.25, 0, 0], color=CTR, stroke_width=5)
    boxes = VGroup()
    for x in (-0.65, 0.65):
        b = box(0.9, 0.62, CTR, fill_opacity=0.1, stroke=3).move_to([x, 0.62, 0])
        plug = Line([x, 0.31, 0], [x, 0, 0], color=CTR, stroke_width=3)
        boxes.add(VGroup(b, plug))
    cap = note("lecture 4").next_to(rail, DOWN, buff=0.18)
    return VGroup(rail, boxes, cap)


def l03_mini() -> VGroup:
    """Lecture 3 in one glyph: the GOLD key through a PINK route into a TEAL box."""
    b = box(1.0, 0.8, CTR, fill_opacity=0.1, stroke=3).move_to([0.75, 0.3, 0])
    k = key_glyph(0.26).move_to([-1.05, 0.3, 0])
    route = Line([-0.72, 0.3, 0], [0.25, 0.3, 0], color=LOOKUP, stroke_width=4)
    cap = note("lecture 3").move_to([0, -0.42, 0])
    g = VGroup(route, b, k, cap)
    g.key, g.route, g.box = k, route, b
    return g


def laptop_pic() -> VGroup:
    """The GREY laptop with ~/AC215's two folders side by side on its screen (names 20 pt at
    scale 1; shown larger in beat 0). .lap .folders .names"""
    lap = wide_laptop(3.2, 1.55)
    sx, sy = lap.screen.get_center()[0], lap.screen.get_center()[1]
    folders, names = VGroup(), VGroup()
    for k, n in enumerate(("llm-rag/", "secrets/")):
        x = sx + (-0.84 if k == 0 else 0.84)
        g = folder_glyph(0.46, LAPTOP).move_to([x, sy + 0.22, 0])
        t = mono(n, CAPTION, INK).next_to(g, DOWN, buff=0.12)
        folders.add(g)
        names.add(t)
    pic = VGroup(lap, folders, names)
    pic.lap, pic.folders, pic.names = lap, folders, names
    return pic


def wide_laptop(w: float, h: float) -> VGroup:
    """explainer.devops.laptop with a wider screen (two folder names side by side fit at 20 pt).
    .screen"""
    screen = RoundedRectangle(width=w, height=h, corner_radius=0.08, stroke_color=LAPTOP,
                              stroke_width=3).set_fill(S.GREY_DARKER, 1)
    bw = w * 0.56
    base = Polygon([-bw, 0, 0], [bw, 0, 0], [bw - 0.2, 0.2, 0], [-bw + 0.2, 0.2, 0], stroke_color=LAPTOP,
                   stroke_width=3).set_fill(LAPTOP, 0.3)
    base.next_to(screen, DOWN, buff=0.02)
    g = VGroup(screen, base)
    g.screen = screen
    return g


def print_rows(scene, t, rows: list, **kw) -> VGroup:
    """common.print_build, with time tags 0.36 tall: its tags are 0.42 tall on the terminal's
    0.40 row pitch, so the tags of neighbouring rows touch (lines 3–5, 21–26). Swaps
    common.time_tag for this call only."""
    orig = _common.time_tag

    def compact(time: str) -> VGroup:
        g = orig(time)
        b = g.box
        b.become(RoundedRectangle(width=b.width, height=0.36, corner_radius=0.18,
                                  stroke_color=b.get_stroke_color(), stroke_width=b.get_stroke_width())
                 .set_fill(S.BG, 0.92).move_to(b))
        return g

    _common.time_tag = compact
    try:
        return print_build(scene, t, rows, **kw)
    finally:
        _common.time_tag = orig


def word_fold(s: str, n: int) -> list[str]:
    """A long output line folded at spaces into rows of at most n characters (no token is cut)."""
    rows, cur = [], ""
    for w in s.split(" "):
        if cur and len(cur) + 1 + len(w) > n:
            rows.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}" if cur else w
    rows.append(cur)
    assert all(len(r) <= n for r in rows), rows
    return rows


def hub_slot() -> VGroup:
    """The empty dashed slot llm-rag-cli on the Docker Hub shelf (as V2's hub_slot)."""
    st = mono("llm-rag-cli", CAPTION, S.GREY)
    sf = DashedVMobject(RoundedRectangle(width=st.width + 0.3, height=0.42, corner_radius=0.06),
                        num_dashes=24).set_stroke(S.GREY, 2)
    g = VGroup(sf, st.move_to(sf))
    g.frame, g.text = sf, st
    return g


def tag2(lines, color: str = S.GREY, size: float = TAG) -> VGroup:
    """A two-row tag (house look: text in its colour, opaque dark fill, round ends)."""
    t = VGroup(*[label(s, size, color) for s in lines]).arrange(DOWN, buff=0.06)
    b = RoundedRectangle(width=t.width + 0.4, height=t.height + 0.2, corner_radius=0.2,
                         stroke_color=color, stroke_width=2).set_fill(S.BG, 0.92)
    t.move_to(b)
    g = VGroup(b, t)
    g.box, g.text = b, t
    return g


def fit_v2(cv: ComposeView, ky: float = KY, bottom: float = CV_BOTTOM) -> ComposeView:
    """V2 above the code strip. ComposeView.fit_top shrinks both ways and keeps every text and
    window at full size, so at 0.84 the windows and chips overflow the CLI box, docker-volumes/
    overflows the laptop and the titles touch their borders. Here the shapes shrink in height
    only (text, chips and kept glyphs keep their size: the same walk as Piece.rescale), then a
    few parts move apart; the routes are redrawn to their moved ends. The zone's bottom edge
    lands on `bottom` (what lies lower — the port route, the image — shows only above 3-row
    strips)."""
    units = []

    def walk(m):
        if getattr(m, "keep_size", False) or isinstance(m, Text) or hasattr(m, "pt"):
            units.append(m)
            return
        for s in m.submobjects:
            walk(s)

    for s in cv.submobjects:
        walk(s)
    cv.stretch(ky, 1, about_point=cv.get_center())
    for u in units:
        u.stretch(1 / ky, 1)
    P = cv.parts
    # the zone's caption with "~/AC215" in the mono font (CMU Sans draws "~" raised)
    zone = P["zone"]
    old = zone[1]
    cap = VGroup(sans("laptop ·", CAPTION, LAPTOP), mono("~/AC215", CAPTION, LAPTOP)).arrange(RIGHT, buff=0.12)
    zone.remove(old)
    zone.add(cap.move_to(old))
    # the folder rows: docker-volumes/ inside the zone; the data route passes under the rail's label
    r1, r2, r3b = cv.rows["repo"], cv.rows["secrets"], cv.rows["chromadb"]
    for r in (r1, r2):
        r.shift(LEFT * 0.08)
    P["row_volumes"].shift(LEFT * 0.08 + DOWN * 0.14)
    # windows and chips clear of their box's borders; the cylinder clear of the :8000 chip
    w_app, w_sec, w_data = cv.windows["app"], cv.windows["secrets"], cv.windows["data"]
    for w in (w_app, w_sec, w_data):
        w.shift(RIGHT * 0.05)
    P["build"].shift(RIGHT * 0.14 + DOWN * 0.06)
    P["port_chip"].shift(LEFT * 0.15)
    P["route_port"][1].shift(LEFT * 0.15)            # the arrow tip under :8000
    cv.cyl.shift(UP * 0.08)
    P["name"].shift(UP * 0.06)
    P["image"].shift(DOWN * 0.1)                     # clear of the "Docker Hub" caption
    VGroup(P["hub"], P["image"]).shift(DOWN * 0.2)   # the shelf's board clearly below the rail
    pc = P["port_chip"]
    cv.routes["app"].set_points_as_corners([[r1.get_right()[0] + 0.1, r1.get_center()[1], 0],
                                            [w_app.get_left()[0] - 0.02, w_app.get_center()[1], 0]])
    cv.routes["secrets"].set_points_as_corners([[r2.get_right()[0] + 0.1, r2.get_center()[1], 0],
                                                [w_sec.get_left()[0] - 0.02, w_sec.get_center()[1], 0]])
    yd, xd = r3b.get_center()[1], w_data.get_center()[0]
    cv.routes["data"].set_points_as_corners([[r3b.get_right()[0] + 0.1, yd, 0], [xd, yd, 0],
                                             [xd, w_data.get_bottom()[1] - 0.02, 0]])
    rp = cv.routes["port"]
    a, yp, xp = rp.get_start(), rp.get_start()[1], pc.get_center()[0]
    rp.set_points_as_corners([a, [xp, yp, 0], [xp, pc.get_bottom()[1] - 0.02, 0]])
    cv.shift(UP * (bottom - zone[0].get_bottom()[1]))
    return cv


def thumbnail() -> ComposeView:
    """V2 as a glyph-only thumbnail (no text: scale it freely): the laptop zone and folders as they
    are, and everything the run creates faint (the plan). Hub, Vertex AI and the phone book left
    out (the shelf stands beside it at full size)."""
    cv = ComposeView()
    for n in ("book", "cloud", "vertex", "key_ride", "hub", "hub_slot", "image", "name"):
        cv.remove(cv.parts[n])
    for s in cv.slot_list:                     # the script's values are in the slots
        s.fill_sq.set_fill(LOOKUP, 0.55)
    th = cv.glyph_only()
    for n in RUN_PARTS:
        ghost(th.parts[n])
    return th


# ------------------------------------------------------------------ the scene
class TwoContainers(VoiceScene):
    def construct(self):
        assert len(SAY) == 11, f"S04 has {len(SAY)} SAY lines; this scene times 11"

        # ========================================================== 0 · recap: L04 + L03, both at once
        tr = tracker("Run", 3)
        m4 = l04_mini().move_to([-2.4, 2.0, 0])
        m3 = l03_mini().move_to([2.4, 2.0, 0])
        pic = laptop_pic()
        pic.scale(1.25).move_to([0, -0.35, 0])
        today = sans("today: both at once", 24, INK).next_to(pic, DOWN, buff=0.3)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), run_time=0.6)
            self.play(Create(m4[0]), FadeIn(m4[2]), run_time=0.6)
            self.play(*[FadeIn(b, shift=DOWN * 0.2) for b in m4[1]], run_time=0.6)
            self.play(Indicate(m4[0], color=TURN, scale_factor=1.05), run_time=0.7)
            vo.wait_until("lecture 3 brought")
            self.play(FadeIn(m3.box), FadeIn(m3.key), FadeIn(m3[3]), run_time=0.5)
            self.play(Create(m3.route), run_time=0.5)
            self.play(m3.key.animate.move_to(m3.box.get_center()), run_time=0.9)
            vo.wait_until("Today")
            self.play(Create(pic.lap), run_time=0.7)
            ctr = pic.lap.screen.get_center()
            self.play(FadeOut(m4, target_position=ctr, scale=0.3),
                      FadeOut(m3, target_position=ctr, scale=0.3), run_time=0.8)
            self.play(FadeIn(today, shift=UP * 0.1),
                      *[FadeIn(f, scale=0.6) for f in pic.folders], FadeIn(pic.names), run_time=0.7)

        # ========================================================== 1 · docker-shell.sh: three exports
        p7 = code_panel(LINE7, SHELL, 7, "bash")
        hdr = VGroup(mono(SHELL, CAPTION, S.GREY), label("· line 7 · after your edit", CAPTION, S.GREY))
        hdr.arrange(RIGHT, buff=0.12)
        hdr.next_to(p7.code, UP, buff=0.1).align_to(p7.code, LEFT).shift(RIGHT * 0.12)
        p7.remove(p7.header)
        p7.header = hdr
        p7.add(hdr)
        p8 = src_panel(SHELL, 8, 12, wrap={8: ['"/secrets/']})
        p8.shift(np.array([-6.17 - p8.get_left()[0], BOTTOM - p8.get_bottom()[1], 0]))
        p7.shift(np.array([-6.17 - p7.get_left()[0], p8.get_top()[1] + 0.12 - p7.get_bottom()[1], 0]))
        lap_target = pic.copy().scale(0.8)
        lap_target.move_to([-4.6, 0, 0]).shift(UP * (TOP_Y - lap_target.get_top()[1]))
        b7 = line_bar_of(p7, 0, LOOKUP, 0.16)
        b8 = p8.bar(8, LOOKUP, 0.16)
        b9 = p8.bar(9, LOOKUP, 0.16)
        b12 = p8.bar(12, TURN, 0.2)
        ch_pid = value_chip("your-project-id")
        ch_key = value_chip("/secrets/llm-service-account.json")
        ch_img = value_chip("llm-rag-cli")
        src_pid = code_span(p7.code, 0, "your-project-id")
        src_key = p8.span(8, "/secrets/llm-service-account.json")
        src_img = p8.span(9, "llm-rag-cli")
        park_x = lap_target.get_right()[0] + 0.35
        park = {ch_pid: 2.52, ch_key: 1.92, ch_img: 1.32}

        def lift(ch, src, bar):
            ch.move_to(src)
            self.play(FadeIn(bar), Indicate(src, color=LOOKUP, scale_factor=1.08), run_time=0.5)
            self.play(FadeIn(ch, scale=0.8), run_time=0.25)
            self.play(ch.animate.move_to([park_x + ch.width / 2, park[ch], 0]), run_time=0.7)

        with self.voiceover(SAY[1]) as vo:
            self.play(Transform(pic, lap_target), FadeOut(today), run_time=0.8)
            self.play(FadeIn(p7, shift=UP * 0.2), FadeIn(p8, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("your project")
            lift(ch_pid, src_pid, b7)
            vo.wait_until("the key's path")
            lift(ch_key, src_key, b8)
            vo.wait_until("and the image name")
            lift(ch_img, src_img, b9)
            vo.wait_until("Then it calls")
            self.play(FadeOut(b7), FadeOut(b8), FadeOut(b9), FadeIn(b12), run_time=0.5)
            self.play(Indicate(p8.span(12, "docker compose run"), color=TURN, scale_factor=1.06), run_time=0.7)
            vo.wait_until("with dash dash")
            self.play(Indicate(p8.span(12, "--rm"), color=TURN, scale_factor=1.3), run_time=0.7)
            vo.wait_until("for that one service")
            slot_img = p8.span(12, "$IMAGE_NAME")
            self.play(ch_img.animate.move_to(slot_img), run_time=0.7)
            self.play(Indicate(ch_img.text, color=TURN, scale_factor=1.15), run_time=0.6)

        # ========================================================== 2 · the compose file: network, CLI service
        cv = fit_v2(ComposeView(show=("zone", "row_repo", "row_secrets")))
        zone, r_repo, r_sec = cv.parts["zone"], cv.parts["row_repo"], cv.parts["row_secrets"]
        s1 = strip(1, 3)
        bar3 = s1.bar(3, TURN, 0.2)
        s6 = strip(6, 8)
        bar6 = s6.bar(6, TURN, 0.2)
        bar8 = s6.bar(8, DATA, 0.22)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p7, p8, b12, ch_img)), run_time=0.5)
            self.play(ReplacementTransform(pic.lap.screen, zone[0].copy()),
                      FadeOut(pic.lap[1]),
                      ReplacementTransform(pic.folders[0], r_repo.glyph.copy()),
                      ReplacementTransform(pic.folders[1], r_sec.glyph.copy()),
                      ReplacementTransform(pic.names[0], r_repo.text.copy()),
                      ReplacementTransform(pic.names[1], r_sec.text.copy()),
                      FadeIn(zone[1]),
                      ch_pid.animate.move_to([PARK_X - ch_pid.width / 2, 2.4, 0]),
                      ch_key.animate.move_to([PARK_X - ch_key.width / 2, 1.8, 0]),
                      run_time=0.9)
            self.remove(*[m for m in self.mobjects if m not in (tr, ch_pid, ch_key)])
            self.add(cv)
            self.play(FadeIn(s1, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("one network")
            self.play(FadeIn(bar3), *cv.parts_in("rail", anim=Create), run_time=0.9)
            vo.wait_until("and the CLI service")
            self.play(FadeOut(bar3), ReplacementTransform(s1, s6), run_time=0.5)
            self.play(FadeIn(bar6), *cv.parts_in("cli", "plug_cli"), run_time=0.7)
            vo.wait_until("with an image built")
            self.play(FadeOut(bar6), FadeIn(bar8), *cv.parts_in("build"), run_time=0.6)
            self.play(Indicate(cv.parts["build"], color=DATA, scale_factor=1.15), run_time=0.7)

        # ========================================================== 3 · mounts, slots, depends_on
        s10 = strip(10, 12)
        bar12 = s10.bar(12, LOOKUP, 0.2)
        bar11 = s10.bar(11, LOOKUP, 0.2)
        s13 = strip(13, 15, wrap={14: ["$GOOGLE"]})
        bar14 = s13.bar(14, LOOKUP, 0.2)
        bar15 = s13.bar(15, LOOKUP, 0.2)
        s16 = strip(16, 17)
        bar17 = s16.bar(17, CTR, 0.22)
        cframe = cv.parts["chroma"].frame
        outline = box(cframe.width, cframe.height, CTR, dashed=True, stroke=3).move_to(cframe)
        slots = cv.slot_list

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(bar8), ReplacementTransform(s6, s10), run_time=0.5)
            self.play(FadeIn(bar12), *cv.parts_in("route_app", anim=Create), run_time=0.8)
            self.play(cv.blink("app"), run_time=0.7)
            vo.wait_until("and secrets onto")
            self.play(FadeOut(bar12), FadeIn(bar11), *cv.parts_in("route_secrets", anim=Create), run_time=0.8)
            self.play(cv.blink("secrets"), run_time=0.7)
            vo.wait_until("Two slots")
            self.play(FadeOut(bar11), ReplacementTransform(s10, s13), *cv.parts_in("slots"), run_time=0.6)
            self.play(FadeIn(bar14), FadeIn(bar15), run_time=0.3)
            self.play(FadeOut(ch_key, target_position=slots[0].get_center(), scale=0.25),
                      FadeOut(ch_pid, target_position=slots[1].get_center(), scale=0.25),
                      *cv.fill_slots(), run_time=0.9)
            vo.wait_until("and the service depends")
            self.play(FadeOut(bar14), FadeOut(bar15), ReplacementTransform(s13, s16), run_time=0.5)
            self.play(FadeIn(bar17), *cv.parts_in("depends"), Create(outline), run_time=0.8)

        # ========================================================== 4 · the Chroma service
        s18 = strip(18, 20)
        bar19 = s18.bar(19, CTR, 0.22)
        bar20 = s18.bar(20, CTR, 0.22)
        s21 = strip(21, 22)
        bar22 = s21.bar(22, LOOKUP, 0.2)
        s23 = strip(23, 24)
        bar24 = s23.bar(24, LOOKUP, 0.2)
        cors = excerpt_chip(CORS, f"{COMPOSE} · line 26 (excerpt)", line=excerpt(COMPOSE, 26, 26))
        cors.move_to([0, 0, 0]).shift(np.array([-6.3 - cors.get_left()[0], BOTTOM - cors.get_bottom()[1], 0]))
        web = grey_tag("lets the course's web tools in · S09")
        web.move_to([6.3 - web.width / 2, cors.chip.get_top()[1] + 0.32, 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(bar17), ReplacementTransform(s16, s18), *cv.parts_in("hub", "image"),
                      run_time=0.7)
            fly = cv.parts["image"].copy()
            self.add(fly)
            self.play(FadeIn(bar19), FadeOut(fly, target_position=cframe.get_center(), scale=0.4),
                      *cv.parts_in("chroma", "plug_chroma"), FadeOut(outline), run_time=1.0)
            vo.wait_until("under a fixed name")
            self.play(FadeOut(bar19), FadeIn(bar20), *cv.parts_in("name"), run_time=0.6)
            self.play(Indicate(cv.parts["name"], color=TURN, scale_factor=1.08), run_time=0.7)
            vo.wait_until("It publishes port")
            self.play(FadeOut(bar20), ReplacementTransform(s18, s21), run_time=0.5)
            self.play(FadeIn(bar22), *cv.parts_in("door", "port_chip"), run_time=0.5)
            self.play(*cv.parts_in("route_port", anim=Create), run_time=0.8)
            vo.wait_until("keeps its data")
            self.play(FadeOut(bar22), ReplacementTransform(s21, s23), *cv.parts_in("row_volumes"),
                      run_time=0.5)
            self.play(FadeIn(bar24), *cv.parts_in("route_data", anim=Create), run_time=0.8)
            vo.wait_until("and lets the course's")
            self.play(FadeOut(bar24), ReplacementTransform(s23, cors), run_time=0.6)
            self.play(FadeIn(web, shift=LEFT * 0.1), run_time=0.4)

        # ========================================================== 5 · /.venv outside /app: edit, rerun
        d18 = src_panel("Dockerfile", 18)
        d45 = src_panel("Dockerfile", 45)
        pair = VGroup(d18, d45).arrange(RIGHT, buff=0.4, aligned_edge=DOWN)
        at_bottom(pair)
        w_app = cv.window("app")
        venv_l = cv.parts["venv"].get_left()[0]
        sheet_w = min(w_app.frame.width, venv_l - w_app.frame.get_left()[0] - 0.04)  # /.venv stays whole
        sheet = VGroup(RoundedRectangle(width=sheet_w, height=w_app.frame.height + 0.06,
                                        corner_radius=0.08, stroke_color=S.GREY, stroke_width=2)
                       .set_fill(S.GREY_DARK, 1),
                       label("your repo", CAPTION, INK))
        sheet[1].move_to(sheet[0])
        at_left(sheet, w_app.frame.get_left()[0], w_app.get_center()[1])
        cli_row = file_row("cli.py")
        at_left(cli_row, r_repo.get_left()[0] + 0.42,
                (r_repo.get_bottom()[1] + r_sec.get_top()[1]) / 2)
        pen = pencil(0.55, S.GREY)
        nreb = grey_tag("no rebuild")
        cli_box = cv.parts["cli"].frame
        nreb.move_to([cli_box.get_center()[0], cli_box.get_top()[1] + 0.3, 0])

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(cors), FadeOut(web), FadeIn(pair, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("the virtual environment")
            self.play(Indicate(d18.span(18, "/.venv"), color=DATA, scale_factor=1.2),
                      *cv.parts_in("venv"), run_time=0.8)
            self.play(Indicate(cv.parts["venv"], color=DATA, scale_factor=1.12),
                      Indicate(d45.span(45, "uv sync"), color=DATA, scale_factor=1.1), run_time=0.8)
            vo.wait_until("outside slash app")
            self.play(Indicate(w_app, color=TURN, scale_factor=1.1), run_time=0.7)
            vo.wait_until("so the code mount")
            self.play(cv.pulse("app"), run_time=0.8)
            self.play(FadeIn(sheet, shift=DOWN * 0.25), run_time=0.6)
            self.play(Indicate(cv.parts["venv"], color=DATA, scale_factor=1.12), run_time=0.6)
            vo.wait_until("Edit cli.py")
            self.play(FadeIn(cli_row, shift=RIGHT * 0.1), run_time=0.4)
            pen.move_to(cli_row.get_right() + np.array([0.45, 0.35, 0]))
            self.play(FadeIn(pen, shift=LEFT * 0.2), run_time=0.3)
            a = cli_row.text.get_left() + RIGHT * 0.05
            self.play(pen.animate.shift(a - pen.tip_point()), run_time=0.4)
            self.play(pen.animate.shift(RIGHT * cli_row.text.width), cli_row.text.animate.set_color(TURN),
                      run_time=0.6)
            vo.wait_until("and rerun")
            self.play(FadeOut(pen), Indicate(cli_row, color=TURN, scale_factor=1.12),
                      Indicate(sheet, color=TURN, scale_factor=1.08), cv.pulse("app"), run_time=0.8)
            self.play(FadeIn(nreb, shift=DOWN * 0.1), run_time=0.4)
            vo.wait_until("no rebuild")
            self.play(Indicate(nreb, color=TURN, scale_factor=1.1), run_time=0.6)

        # ========================================================== 6 · sh docker-shell.sh: Chroma first
        t = term(P_REPO, rows=TERM_ROWS)
        th = thumbnail()
        th.scale((3.5 - t.box.get_top()[1] - 0.12) / th.height)
        th.shift(np.array([0.55 - th.get_center()[0], 3.5 - th.get_top()[1], 0]))
        hub, img = cv.parts["hub"], cv.parts["image"]
        hubg_target = VGroup(hub.copy(), img.copy())
        hubg_target.shift(np.array([6.42 - hubg_target.get_right()[0],
                                    3.42 - 0.47 - hubg_target.get_top()[1], 0]))
        slot = hub_slot().next_to(hubg_target[0].board, UP, buff=0.05)
        pull = grey_tag("first build also pulls python:3.12-slim-bookworm (about 48 MB)")

        with self.voiceover(SAY[6]) as vo:
            cv.remove(hub, img)
            self.add(hub, img)
            self.play(FadeOut(VGroup(pair, sheet, cli_row, nreb)),
                      Indicate(tr.caption, color=TURN, scale_factor=1.06), run_time=0.5)
            self.play(FadeOut(cv, target_position=th.get_center(), scale=th.width / cv.width),
                      FadeIn(th, target_position=cv.get_center(), scale=cv.width / th.width),
                      Transform(hub, hubg_target[0]), Transform(img, hubg_target[1]), run_time=1.0)
            self.play(FadeIn(t, shift=UP * 0.2), run_time=0.5)
            vo.wait_until("sh docker-shell.sh")
            type_cmd(self, t, RUN.cmd, 0.9)
            t.print(self, [RUN.line(2)], run_time=0.3)
            vo.wait_until("Compose pulls")
            l3 = print_rows(self, t, [RUN.line(3)], run_time=0.4)[0]
            fly = img.copy()
            self.add(fly)
            self.play(FadeOut(fly, target_position=th.parts["chroma"].get_center(), scale=0.25),
                      Indicate(substring(l3, "chromadb/chroma:latest"), color=TURN, scale_factor=1.06),
                      run_time=0.9)
            # on the row under line 5 (lines 4 and 5 print into the two rows above it)
            pull.move_to(t._slot(len(t.lines) + 2) + np.array([pull.width / 2, -t.pitch / 2, 0]))
            self.play(FadeIn(pull, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("creates the network")
            print_rows(self, t, [RUN.line(4)], run_time=0.4)
            self.play(unghost(th.parts["rail"]), run_time=0.6)
            vo.wait_until("and creates the Chroma")
            print_rows(self, t, [RUN.line(5)], run_time=0.4)
            self.play(*[unghost(th.parts[n]) for n in ("chroma", "plug_chroma", "port_chip", "door",
                                                       "route_port", "route_data")], run_time=0.8)

        # ========================================================== 7 · "not found": harmless
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(pull), run_time=0.3)
            l6 = t.print(self, [RUN.line(6)], run_time=0.3)[0]
            err = t.print(self, [(r, ERR) for r in word_fold(RUN.join(7, 8), t.max_chars)], run_time=0.5)
            vo.wait_until("Compose first asks")
            self.play(FadeIn(slot, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(slot, color=ERR, scale_factor=1.1),
                      Indicate(substring(l6, "llm-rag-cli"), color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("finds none")
            self.play(Indicate(substring(err[-1], "not found"), color=ERR, scale_factor=1.2), run_time=0.6)
            vo.wait_until("and builds it instead")
            hm = harmless_tag()
            beside(hm, t, err[-1], buff=0.4)
            self.play(*[r.animate.set_color(S.GREY) for r in err], run_time=0.6)
            pin(self, err[-1], hm, run_time=0.4)

        # ========================================================== 8 · the build: 81 s, 112 MB of context
        with self.voiceover(SAY[8]) as vo:
            rows = print_rows(self, t, [RUN.line(9), RUN.line(10), RUN.line(21), ROW22, RUN.line(25),
                                         RUN.line(26), "…", RUN.line(36)], run_time=0.9, lag=0.08)
            l10, l21, l22, l25, l26, l36 = rows[1], rows[2], rows[3], rows[4], rows[5], rows[7]
            box81 = under(substring(l10, "81.5s"), TURN, stroke=4)
            badges = [build_badge(2), build_badge(5, words=False), build_badge(6, words=False)]
            for bd, row in zip(badges, (l22, l25, l26)):
                beside(bd, t, row, buff=0.3)
            self.play(Create(box81), Indicate(substring(l10, "81.5s"), color=TURN, scale_factor=1.15),
                      run_time=0.6)
            self.play(*[FadeIn(b, scale=0.7) for b in badges], run_time=0.4)
            attach(self, l10, box81)
            for bd, row in zip(badges, (l22, l25, l26)):
                attach(self, row, bd)
            vo.wait_until("Its context")
            i_mb = l21.text.index("112.26MB")
            mbox = col_box(l21, i_mb, i_mb + 8, TURN)
            self.play(Create(mbox), substring(l21, "112.26MB").animate.set_color(TURN), run_time=0.5)
            attach(self, l21, mbox)
            # the parcel: the build context, mostly .git
            par = box(9.0, 0.95, DATA, fill_opacity=0.06, radius=0.12, stroke=3).move_to([0, 0.27, 0])
            phead = VGroup(sans("build context · 112 MB", CAPTION, DATA))
            phead.arrange(RIGHT, buff=0.12)
            at_left(phead, par.get_left()[0] + 0.1, par.get_top()[1] + 0.22)
            inner_l, inner_r = par.get_left()[0] + 0.12, par.get_right()[0] - 0.12
            w_all = inner_r - inner_l
            w_git = w_all * 103 / 112.26
            git = RoundedRectangle(width=w_git, height=0.7, corner_radius=0.06, stroke_color=S.GREY,
                                   stroke_width=2).set_fill(S.GREY, 0.3)
            at_left(git, inner_l, par.get_center()[1])
            git_lab = VGroup(mono(".git", TAG, INK), label("· 103 MB", TAG, INK)).arrange(RIGHT, buff=0.12)
            at_left(git_lab, git.get_left()[0] + 0.3, git.get_center()[1])
            old_db = cylinder(0.34, 0.48, DATA).move_to(git.get_right() + LEFT * 0.45)
            old_lab = note("an old database copy", INK).next_to(old_db, LEFT, buff=0.2)
            rest = RoundedRectangle(width=w_all - w_git - 0.06, height=0.7, corner_radius=0.04,
                                    stroke_color=S.GREY, stroke_width=1.5).set_fill(S.GREY_DARK, 0.6)
            at_left(rest, git.get_right()[0] + 0.06, par.get_center()[1])
            sq = RoundedRectangle(width=0.08, height=0.7, corner_radius=0.02, stroke_width=0) \
                .set_fill(DATA, 1).move_to(rest).align_to(rest, RIGHT).shift(LEFT * 0.1)
            rest_lab = note("the rest")
            rest_lab.move_to([par.get_right()[0] - rest_lab.width / 2, phead.get_center()[1], 0])
            sq_lab = mono("chroma.sqlite3", CAPTION, DATA)
            sq_lab.move_to([par.get_right()[0] - sq_lab.width / 2, par.get_bottom()[1] - 0.3, 0])
            sq_lead = Line(sq.get_bottom(), [sq.get_center()[0], sq_lab.get_top()[1] + 0.03, 0],
                           color=DATA, stroke_width=2)
            err_t = erratum_tag("no .dockerignore → exercises")
            at_left(err_t, par.get_left()[0], sq_lab.get_center()[1])
            hide = note("the mounts hide both at run time")
            at_left(hide, par.get_left()[0] + 0.1, err_t.get_bottom()[1] - 0.24)
            vo.wait_until("mostly git history")
            resize(self, t, 3, keep=[l10, l21, l36])
            self.play(Create(par), FadeIn(phead, shift=DOWN * 0.1), run_time=0.5)
            self.play(FadeIn(git, scale=0.9), FadeIn(git_lab), run_time=0.5)
            vo.wait_until("that still holds")
            self.play(FadeIn(old_db, shift=DOWN * 0.15), FadeIn(old_lab), run_time=0.6)
            self.play(FadeIn(rest), FadeIn(rest_lab), FadeIn(sq), Create(sq_lead), FadeIn(sq_lab), run_time=0.6)
            vo.wait_until("With no docker ignore")
            self.play(FadeIn(err_t, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(hide, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the image keeps it")
            self.play(Indicate(git, color=TURN, scale_factor=1.02), Indicate(sq, color=TURN), run_time=0.7)
        parcel = VGroup(par, phead, git, git_lab, old_db, old_lab, rest, rest_lab, sq, sq_lead, sq_lab,
                        err_t, hide)

        # ========================================================== 9 · the banner
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(parcel), run_time=0.4)
            resize(self, t, TERM_ROWS, keep=[l36])
            out = t.print(self, RUN.at((37, 44)), run_time=0.8)
            l38, l40, l41, l42, l43, l44 = out[1], out[3], out[4], out[5], out[6], out[7]
            vo.wait_until("Python 3.12.15")
            u42 = under(substring(l42, "3.12.15"), S.GREY, stroke=3)
            u43 = under(substring(l43, "0.13.1"), S.GREY, stroke=3)
            self.play(Create(u42), Indicate(substring(l42, "3.12.15"), color=TURN, scale_factor=1.1),
                      run_time=0.6)
            self.play(Create(u43), Indicate(substring(l43, "0.13.1"), color=TURN, scale_factor=1.1),
                      run_time=0.6)
            attach(self, l42, u42)
            attach(self, l43, u43)
            vo.wait_until("at the time of recording")
            rec = recording_tag()
            beside(rec, t, l42, buff=0.4)
            pin(self, l42, rec, run_time=0.4)
            # the run's unspoken lines, in the pause: the CLI container now exists (its name: S05)
            u38 = under(substring(l38, CTR_NAME), S.GREY, stroke=3)
            arch = grey_tag("Apple Silicon: aarch64 · both native")
            beside(arch, t, l40, buff=0.4)
            self.play(Create(u38), *[unghost(th.parts[n]) for n in CLI_PARTS], run_time=0.8)
            attach(self, l38, u38)
            pin(self, l40, arch, run_time=0.4)
            vo.wait_until("It says activated")
            # a small GREY bracket in the left margin, from line 41 to line 44
            xb = l41.strut.get_left()[0] - 0.14
            yt, yb = l41.strut.get_top()[1] - 0.03, l44.strut.get_bottom()[1] + 0.03
            brk = VMobject(stroke_color=S.GREY, stroke_width=3)
            brk.set_points_as_corners([[xb + 0.09, yt, 0], [xb, yt, 0], [xb, yb, 0], [xb + 0.09, yb, 0]])
            ua = under(substring(l41, "activated."), S.GREY, stroke=3)
            ub = under(substring(l44, "Activating"), S.GREY, stroke=3)
            err9 = tag("erratum · says it before it does · cosmetic", S.GREY, size=CAPTION)
            beside(err9, t, l44, buff=0.35)
            self.play(Create(ua), Create(ub), Create(brk), run_time=0.6)
            attach(self, l41, ua, brk)
            attach(self, l44, ub)
            pin(self, l44, err9, run_time=0.5)

        # ========================================================== 10 · the container's prompt
        with self.voiceover(SAY[10]) as vo:
            t.set_prompt(P_CTR)
            pr = t.type(self, "", type_time=0)
            self.play(*enter_container(t), th.light("cli"), run_time=0.7)
            vo.wait_until("The part after")
            cid = substring(pr, "92c5bfd26089")
            uid = under(cid, S.GREY, stroke=3)
            idt = grey_tag("container id · your numbers will differ")
            beside(idt, t, pr, buff=0.35)
            self.play(Create(uid), Indicate(cid, color=TURN, scale_factor=1.1), run_time=0.6)
            attach(self, pr, uid)
            pin(self, pr, idt, run_time=0.4)
            vo.wait_until("it changes")
            self.play(Indicate(idt, color=TURN, scale_factor=1.06), run_time=0.6)
            vo.wait_until("Pause")
            yt10 = your_turn()
            beside(yt10, t, pr, buff=0.3)
            yt10.next_to(idt, RIGHT, buff=0.25)
            self.play(FadeIn(yt10, scale=1.2), run_time=0.5)
        self.wait(2)                                   # ▶ beat: hold the frame
        self.play(FadeOut(VGroup(tr, t, th, hub, img, slot, yt10)), run_time=0.8)
        self.wait(0.3)


def line_bar_of(panel, k: int, color: str = LOOKUP, opacity: float = 0.16):
    """A line bar over row k (0-based) of a code_panel's code (as src_panel's .bar)."""
    from explainer.devops import line_bar
    return line_bar(panel.code, k, color, opacity)
