"""S10 · Exit, and the index survives (part 2 opens; README "Run Container" step 3 again, every other
command an extra). Lecture: none (no lecture tag).

Beats (script.md "## S10", one voiceover block each):
 0  Part 2 opens on V1 as S09 left it: the top lane in its colours with its three flags and GREEN
    ticks on chunking, embedding and the database (as "chunk, embed, load" is said); the bottom
    lane and its two flags GREY with the tag "part 2" (the lane flashes as "part 2" is said). The
    rest of V1 fades; the TEAL cylinder grows and Transforms into V2's cylinder while the Chroma
    box forms around it; V2 builds around it: the rail, the CLI box, the laptop zone with its
    folders, the PINK routes; a YELLOW "?" badge on the docker-volumes/chromadb/ folder. V2 then
    shrinks to the top: its parts Transform into a compact V2 (laptop zone with llm-rag/ and
    docker-volumes/chromadb/, the :8000 door, CLI box with /app, Chroma box with /data and the
    cylinder, the rail, the /app, /data and 8000:8000 routes) that fits above a 6-row terminal.
 1  TRACKER Run 3 · extra. Container terminal (3-row strip, TEAL, app@92c5bfd26089:/app$) types
    `exit` (extra) -> laptop/07 line 46; the CLI box dissolves into a dashed GREY outline. The frame
    turns GREY, title laptop, prompt ~/AC215/llm-rag$, and it grows to 6 rows. `docker ps -a`
    (extra) -> laptop/20 lines 2–3 sliced from STATUS on (GREY tag "3 of 7 columns"). The outline
    flashes at "gone"; "--rm / removed on exit" writes inside it; the Chroma row: "Up 2 minutes"
    boxed and the name YELLOW (the Chroma box flashes); 0.0.0.0:8000->8000/tcp PINK, the :8000
    door lights PINK, its route pulses.
 2  `docker compose down` (extra) -> laptop/21 lines 2–3 joined and 4 (word-folded, RED; the two
    variable names flash), fading to GREY with the tag "harmless: the values live only in
    docker-shell.sh"; the typed command flashes YELLOW at "the down command needs neither";
    lines 5–7 (Compose rows, times as tags) print together: as line 6 flashes the Chroma box, its
    name, port, /data and :8000 routes and the dashed outline leave and the door unlights; as
    line 7 flashes the rail leaves. Only the laptop zone remains.
 3  The terminal clears and grows to 13 rows; the zone fades and its docker-volumes/chromadb/
    folder (with the "?") moves to the top-right band. `docker ps -a; docker network ls; ls -la
    docker-volumes/chromadb` (extra; folded after "-a;") -> laptop/22 lines 2–12 (long rows cut
    with …): the empty container table boxed YELLOW, GREY note "no llm-rag-network" beside the
    network rows, "your numbers will differ" on the listing. The folder glows; chroma.sqlite3
    boxed YELLOW and the "?" becomes a GREEN tick; the two UUID folders boxed GREEN; then outputs/
    appears beside the folder with a GREEN tick.
 4  TRACKER Run 3. The terminal clears (13 rows): `sh docker-shell.sh` -> laptop/23 lines 2–12
    (Compose rows with time tags), then the prompt app@390fe47a277a:/app$ (TEAL frame; the id
    underlined + "container id · your numbers will differ"). As lines 3–4 and 5–6 print, a rail,
    a Chroma box (PINK route to the folder) and a CLI box land beside the same GREY folder.
    "[+] run 2/2" boxed YELLOW + GREY chip "no pull · no build: the image exists"; GREY note "after
    a git pull that changes pyproject.toml / or the Dockerfile: [docker compose build]" (the
    command in a slim GREY pill, so it never reads as output; it flashes YELLOW at "run docker
    compose build first"). ▶ your turn beside the typed command. Hold 2 s.
 5  TRACKER Run 3 · extra. After the hold (silent), the second laptop terminal (8 rows) replaces it;
    it opens on ~ (the ~ flashes) with the GREY caption "new terminal: cd here first" above its
    frame (it stays there, readable, until the terminal leaves). With the narration "~$" stretches
    into "~/AC215/llm-rag$" ("student@laptop:" stays put): the curl … | grep … line (extra;
    folded at spaces, and once inside the URL at "/databases" with no space before the "\" and no
    indent after it, so the rows join into the captured line) -> laptop/24 lines 2–5: the collection
    names GREEN, both "dimension":256 boxed YELLOW. The container terminal (6 rows): `python cli.py
    --get --chunk_type char-split` (extra; GREY note "not in the README · S12") -> cli-container/70
    line 6 cut after the ids list's "]" (word-folded; a GREY " …" after the "]": the line goes on
    with 'embeddings', 'metadatas', 'documents'); above it the PANEL of
    recorded-embeddings/05 line 6 cut the same way, header "the same command before exit" + tag
    "recorded · the staff's vectors (68e0bde)". The first and last id of each list turn GREEN with
    GREEN ticks in the margin; GREEN chip "10 of 10 match". The terminals leave; the band picture
    grows to the centre: both boxes fade to dashed GREY outlines ("disposable"), the folder glows.
    Empty frame.

Deviations from SHOW (see the scene report): V2 above the terminal is a compact V2 built here
(the full V2 does not fit above a 6-row terminal and its text cannot shrink): secrets/, the key,
/secrets, /.venv and the $ slots leave as it shrinks. With the 13-row terminals of beats 3–4 the
picture lives in the free band right of the tracker (y > 2.6): the folder, then the new boxes as
small glyphs beside it. laptop/20 is sliced from its STATUS column on (STATUS, PORTS, NAMES:
"Up 2 minutes" must show), not PORTS and NAMES only. laptop/21's WARN lines and the ids lines are
word-folded (cutting them at 65 would hide "is not set"; the ids stay whole). The curl line of
laptop/24 is folded here, not by type_cmd: fold_cmd's hard break inside the URL ends the row with
" \" and indents the next, which splits the URL into two words. The final picture (boxes dissolve,
folder glows) illustrates the last sentence; SHOW has no picture there. The second terminal's
"cd here first" caption sits above its frame, not beside the prompt (rows 0–3 fill with the curl
line, and beside the prompt it was readable for under a second).
"""

from types import SimpleNamespace

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    ReplacementTransform,
    RoundedRectangle,
    ShowPassingFlash,
    Transform,
    VGroup,
)

from common import (
    CTR,
    DATA,
    ERR,
    INK,
    LAPTOP,
    LOOKUP,
    NARRATION,
    P_CTR,
    P_CTR2,
    P_HOME,
    P_REPO,
    TERM_PT,
    TERM_W,
    TURN,
    ComposeView,
    RagMap,
    _type_rows,
    bare_prompt,
    beside,
    capture,
    caption_extra,
    col_box,
    cylinder,
    differ_tag,
    door,
    enter_container,
    extra_tag,
    file_row,
    grey_tag,
    leave_container,
    log_panel,
    note,
    pin,
    print_build,
    resize,
    sans,
    split_prompt,
    staff_tag,
    strip_top,
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
    box,
    check_mark,
    chip,
    glyph_range,
    mono,
    mono_line,
    step_badge,
    substring,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S10"]

# ------------------------------------------------------------------ the real captures
EXIT = capture("07", "laptop")
assert split_prompt(EXIT.line(45)) == (P_CTR, "exit") and EXIT.line(46) == "exit", EXIT.lines[-2:]

PSA = capture("20", "laptop")
assert PSA.cmd == "docker ps -a" and PSA.exit == 0
_st = PSA.line(2).index("STATUS")                 # the column view: STATUS, PORTS, NAMES (sliced)
PS_ROWS = [PSA.line(2)[_st:].rstrip(), PSA.line(3)[_st:].rstrip()]
assert PS_ROWS[0].split() == ["STATUS", "PORTS", "NAMES"], PS_ROWS
assert PS_ROWS[1] == "Up 2 minutes   0.0.0.0:8000->8000/tcp   llm-rag-chromadb", PS_ROWS[1]

DOWN_ = capture("21", "laptop")
assert DOWN_.cmd == "docker compose down" and DOWN_.exit == 0
# lines 2–3: one WARN line the 80-column terminal wrapped at a space (the space itself was lost)
assert len(DOWN_.line(2)) == 79 and DOWN_.line(2).endswith("Defaulting") and DOWN_.line(3) == "to a blank string."
WARN_CREDS = DOWN_.line(2) + " " + DOWN_.line(3)
WARN_PROJ = DOWN_.line(4)
assert '"GCP_PROJECT" variable is not set' in WARN_PROJ, WARN_PROJ
assert DOWN_.line(5) == "[+] down 2/2" and "llm-rag-chromadb Removed" in DOWN_.line(6)
assert "llm-rag-network    Removed" in DOWN_.line(7)

AFTER = capture("22", "laptop")
assert AFTER.cmd == "docker ps -a; docker network ls; ls -la docker-volumes/chromadb"
assert AFTER.line(2).startswith("CONTAINER ID") and AFTER.line(3).startswith("NETWORK ID")
assert AFTER.line(11).endswith("59781120 Oct 16 00:55 chroma.sqlite3"), AFTER.line(11)
UUIDS = ("ab125f80", "f460d2ab")
assert AFTER.line(10).endswith(UUIDS[0] + "-4e2e-4751-8eb4-8d7d06c87e93") and UUIDS[1] in AFTER.line(12)
_cmd22 = AFTER.cmd.split("; ", 1)                # folded after "-a;" (one valid line when joined)
AFTER_ROWS = [f"{P_REPO} {_cmd22[0]}; \\", f"    {_cmd22[1]}"]
assert all(len(r) <= 65 for r in AFTER_ROWS), AFTER_ROWS

AGAIN = capture("23", "laptop")
assert AGAIN.cmd == "sh docker-shell.sh" and AGAIN.line(2) == "[+] run 2/2"
assert "Network llm-rag-network" in AGAIN.line(3) and "Container llm-rag-chromadb" in AGAIN.line(4)
assert AGAIN.line(5).endswith("Creating") and AGAIN.line(12).startswith("Activating")
assert split_prompt(AGAIN.line(13)) == (P_CTR2, "exit"), AGAIN.line(13)   # S16 types that exit

NAMES = capture("24", "laptop")
assert NAMES.cmd.startswith("curl -s http://localhost:8000/api/v2/tenants/") and "| grep -oE" in NAMES.cmd
assert NAMES.at((2, 5)) == ['"name":"char-split-collection"', '"dimension":256',
                            '"name":"recursive-split-collection"', '"dimension":256'], NAMES.lines

# the curl line folds at spaces, and once inside its URL at a "/" with no space before the "\" and
# no indent after it (bash joins backslash-newline, so the URL stays one word)
_u = NAMES.cmd.split()
assert _u[:2] == ["curl", "-s"] and _u[3:6] == ["|", "grep", "-oE"] and len(_u) == 7, _u
_cut = _u[2].index("/databases")
CURL_ROWS = [f"{P_REPO} curl -s \\", f"    {_u[2][:_cut]}\\", f"{_u[2][_cut:]} | grep -oE \\", f"    {_u[6]}"]
_joined = "\n".join(CURL_ROWS)[len(P_REPO) + 1:].replace("\\\n", "")
assert " ".join(_joined.split()) == NAMES.cmd and all(len(r) <= 65 for r in CURL_ROWS), CURL_ROWS

GET = capture("70", "cli-container")
GET_BEFORE = capture("05", "recorded-embeddings")
assert GET.cmd == GET_BEFORE.cmd == "python cli.py --get --chunk_type char-split"
IDS = GET.cut(6, "]")
assert IDS == GET_BEFORE.cut(6, "]") and IDS.startswith("Results: {'ids': ['1021665fac86c5a5-0'"), IDS[:40]
FIRST_ID, LAST_ID = "1021665fac86c5a5-0", "1021665fac86c5a5-9"
assert IDS.endswith(f"'{LAST_ID}']") and IDS.count("1021665fac86c5a5-") == 10

# ------------------------------------------------------------------ layout
T6_TOP = strip_top(6)                    # -0.23: top of the 6-row terminal of beats 1–2
Y0 = T6_TOP + 0.15                       # the compact V2's bottom edge
BAND_Y = 3.08                            # the top-right band above the 13-row terminals (top 2.59)
BAND_RIGHT = 6.3
SHOW_V2 = ("zone", "row_repo", "row_secrets", "row_volumes", "key", "door", "cli", "venv", "chroma",
           "name", "port_chip", "rail", "plug_cli", "plug_chroma", "route_app", "route_secrets",
           "route_data", "route_port")
UNUSED_V2 = ("slots", "build", "depends", "book", "cloud", "vertex", "key_ride", "hub", "hub_slot", "image")


# ------------------------------------------------------------------ small helpers
def left_at(m, x: float, y: float):
    """Put m's left edge at x and its centre at height y."""
    return m.shift(np.array([x - m.get_left()[0], y - m.get_center()[1], 0]))


def right_at(m, x: float, y: float):
    return m.shift(np.array([x - m.get_right()[0], y - m.get_center()[1], 0]))


def stick(scene, line, *mobs):
    """Make mobs (already on screen) part of terminal row `line` (its last row when folded): they
    scroll and fade with it."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    for m in mobs:
        scene.remove(m)
        row.add(m)
    scene.add(row)


def word_fold(s: str, n: int = 65) -> list[str]:
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


IDS_ROWS = word_fold(IDS)
assert len(IDS_ROWS) == 4 and FIRST_ID in IDS_ROWS[0] and LAST_ID in IDS_ROWS[-1], IDS_ROWS
# both captured lines go on after the ids' "]" (", 'embeddings': None, 'metadatas': [..."; the rest
# of line 6 is never shown, so only cut() reads it): the scene marks the cut with a GREY " …"


def more_mark(row) -> VGroup:
    """A GREY ' …' after a row printed only up to its cut (the captured line goes on): the "…"
    glyph of a twin line row.text + ' …' laid over the row, so it sits one cell after it."""
    twin = mono_line(row.text + " …", row.pt, S.GREY)
    twin.shift(row.strut.get_corner(UP + LEFT) - twin.strut.get_corner(UP + LEFT))
    return glyph_range(twin, len(row.text) + 1)


def polyline(points, color: str = LOOKUP, stroke: float = 4):
    from manim import VMobject
    m = VMobject(stroke_color=color, stroke_width=stroke)
    m.set_points_as_corners([np.array([p[0], p[1], 0.0]) for p in points])
    return m


def q_badge():
    """The YELLOW "?" on the data folder: does it survive?"""
    return step_badge("?", TURN)


def tick_badge():
    """The answer: a GREEN tick in the same circle."""
    c = Circle(radius=0.22, stroke_color=DATA, stroke_width=2.5).set_fill(S.BG, 1)
    return VGroup(c, check_mark(0.22, DATA, 4).move_to(c))


def backlight(m, pad: float = 0.12):
    """A soft GREY glow behind m (starts invisible: animate it in)."""
    r = RoundedRectangle(width=m.width + 2 * pad, height=m.height + 2 * pad, corner_radius=0.14,
                         stroke_color=S.GREY, stroke_width=2, stroke_opacity=0).set_fill(S.GREY, 0)
    return r.move_to(m)


def compact_v2() -> SimpleNamespace:
    """V2 squeezed into y Y0..3.1, the full width (text at 20 pt), its parts shaped like
    ComposeView's so the full V2 Transforms into it part by part."""
    c = SimpleNamespace()
    zf = box(3.55, 2.86, LAPTOP, fill_opacity=0.05, radius=0.16)
    zf.move_to([-4.575, Y0 + 1.43, 0])
    zt = sans("laptop · ~/AC215", CAPTION, LAPTOP).move_to([-4.575, zf.get_top()[1] - 0.27, 0])
    c.zone = VGroup(zf, zt)
    x0 = -6.15
    r1 = left_at(file_row("llm-rag/"), x0, Y0 + 2.03)
    r3a = left_at(file_row("docker-volumes/"), x0, Y0 + 1.38)
    r3b = left_at(file_row("chromadb/"), x0 + 0.42, Y0 + 0.93)
    c.row_repo, c.row_volumes, c.chromadb = r1, VGroup(r3a, r3b), r3b
    dr = door(0.34, 0.56, LAPTOP).move_to([zf.get_right()[0], Y0 + 0.38, 0])
    dl = mono(":8000", CAPTION, LAPTOP).next_to(dr, LEFT, buff=0.12)
    c.door = VGroup(dr, dl)
    c.door_glyph, c.door_label = dr, dl

    # the CLI box: title, the /app window
    cb = box(2.2, 1.3, CTR, fill_opacity=0.08, radius=0.16, stroke=3).move_to([-1.35, Y0 + 2.18, 0])
    ct = left_at(sans("CLI container", CAPTION, CTR), cb.get_left()[0] + 0.15, cb.get_top()[1] - 0.25)
    w_app = ComposeView._window("/app", w=1.15, h=0.46).move_to([-1.62, Y0 + 1.92, 0])
    c.cli = VGroup(cb, ct, w_app)
    # the Chroma box: title, /data window, the cylinder; name tag above, :8000 port chip below
    hb = box(2.9, 1.3, CTR, fill_opacity=0.08, radius=0.16, stroke=3).move_to([2.05, Y0 + 2.18, 0])
    ht = left_at(sans("Chroma container", CAPTION, CTR), hb.get_left()[0] + 0.15, hb.get_top()[1] - 0.25)
    w_data = ComposeView._window("/data", w=1.05, h=0.46).move_to([1.3, Y0 + 1.92, 0])
    cyl = cylinder(0.6, 0.6).move_to([3.15, Y0 + 2.12, 0])
    c.chroma = VGroup(hb, ht, w_data, cyl)
    c.name = mono("llm-rag-chromadb", CAPTION, CTR).move_to([2.05, hb.get_top()[1] + 0.2, 0])
    pc = chip(":8000", CTR, size=CAPTION, font="DejaVu Sans Mono", fill_opacity=0.9)
    pc.box.set_fill(ManimColorMix(CTR, 0.15), 1)
    c.port_chip = pc.move_to([2.45, hb.get_bottom()[1] - 0.04, 0])

    # the rail (its name at its right end), the plugs
    rail_y = Y0 + 1.22
    rl = Line([-2.6, rail_y, 0], [3.65, rail_y, 0], color=CTR, stroke_width=7)
    rt = left_at(mono("llm-rag-network", CAPTION, CTR), 3.8, rail_y)
    c.rail = VGroup(rl, rt)
    c.plug_cli = Line([-0.75, cb.get_bottom()[1], 0], [-0.75, rail_y, 0], color=CTR, stroke_width=4)
    c.plug_chroma = Line([1.6, hb.get_bottom()[1], 0], [1.6, rail_y, 0], color=CTR, stroke_width=4)

    # the PINK routes: /app, /data, the published port
    c.route_app = polyline([(r1.get_right()[0] + 0.1, r1.get_center()[1]),
                            (w_app.get_left()[0] - 0.02, w_app.get_center()[1])])
    yd = r3b.get_center()[1]
    c.route_data = polyline([(r3b.get_right()[0] + 0.1, yd), (1.0, yd),
                             (1.0, w_data.get_bottom()[1] - 0.02)])
    yp = dr.get_center()[1]
    xp = c.port_chip.get_center()[0]
    rp = polyline([(dr.get_right()[0] + 0.02, yp), (xp, yp), (xp, c.port_chip.get_bottom()[1] - 0.02)])
    tip = Arrow([xp, c.port_chip.get_bottom()[1] - 0.4, 0], [xp, c.port_chip.get_bottom()[1] - 0.02, 0],
                buff=0, color=LOOKUP, stroke_width=4, tip_length=0.16, max_tip_length_to_length_ratio=0.5)
    lab = mono("8000:8000", CAPTION, LOOKUP).move_to([-0.4, (yp + yd) / 2, 0])
    c.route_port = VGroup(rp, tip, lab)
    c.route_port_line = rp

    q = q_badge()
    q.move_to([r3b.glyph.get_left()[0] - 0.3, yd, 0])
    c.qmark = q
    # back to front: what the scene adds, in this order
    c.order = [c.zone, c.route_app, c.route_data, c.route_port, c.row_repo, c.row_volumes, c.door,
               c.rail, c.plug_cli, c.plug_chroma, c.cli, c.chroma, c.name, c.port_chip, c.qmark]
    return c


def ManimColorMix(color, k: float):
    from manim import ManimColor
    return ManimColor(S.BG).interpolate(ManimColor(color), k)


def grey_out(m, k: float = 0.45):
    """V1's bottom lane before part 2: every stroke and every coloured fill GREY (a chip's dark
    fill stays dark), then faded to 1 - k."""
    from manim import ManimColor, VMobject
    bg = ManimColor(S.BG).to_hex().lower()
    for f in m.get_family():
        if not isinstance(f, VMobject):
            continue
        if f.get_stroke_width() > 0:
            f.set_stroke(S.GREY, family=False)
        if f.get_fill_opacity() > 0 and ManimColor(f.get_fill_color()).to_hex().lower() != bg:
            f.set_fill(S.GREY, family=False)
    m.fade(k)
    return m


def rm_note(ghost) -> VGroup:
    """'--rm' over 'removed on exit', GREY, inside the dashed outline the CLI box left behind (the
    outline is its frame)."""
    t = VGroup(mono("--rm", CAPTION, S.GREY), note("removed on exit")).arrange(DOWN, buff=0.1)
    assert t.width < ghost.width - 0.2, t.width
    return t.move_to(ghost)


def light_door(c, color: str):
    return [c.door_glyph.frame.animate.set_stroke(color, 4 if color != LAPTOP else 3),
            c.door_glyph[1].animate.set_color(color), c.door_label.animate.set_color(color)]


def flash(path, color: str = LOOKUP, run_time: float = 1.0):
    return ShowPassingFlash(path.copy().set_stroke(color, 9), time_width=0.6, run_time=run_time)


def band_minis(folder_row) -> SimpleNamespace:
    """S10's restart in the band: a CLI box and a Chroma box (glyphs) on a rail, the Chroma box's
    PINK route to the same folder."""
    m = SimpleNamespace()
    y = BAND_Y + 0.05
    chroma = box(0.72, 0.5, CTR, fill_opacity=0.1, radius=0.08, stroke=3)
    chroma = VGroup(chroma, cylinder(0.26, 0.24, stroke=2).move_to(chroma))
    chroma.move_to([folder_row.get_left()[0] - 0.95, y, 0])
    cli = box(0.72, 0.5, CTR, fill_opacity=0.1, radius=0.08, stroke=3)
    cli = VGroup(cli, RoundedRectangle(width=0.42, height=0.16, corner_radius=0.04, stroke_color=CTR,
                                       stroke_width=2).set_fill(S.BG, 0.9).move_to(cli))
    cli.move_to(chroma.get_center() + LEFT * 1.0)
    ry = chroma.get_bottom()[1] - 0.08
    m.rail = Line([cli.get_left()[0] - 0.1, ry, 0], [chroma.get_right()[0] + 0.1, ry, 0], color=CTR,
                  stroke_width=4)
    m.route = Line(chroma.get_right() + RIGHT * 0.02, folder_row.glyph.get_left() + LEFT * 0.06,
                   color=LOOKUP, stroke_width=4)
    m.chroma, m.cli = chroma, cli
    return m


# ------------------------------------------------------------------ the scene
class IndexSurvives(VoiceScene):
    def construct(self):
        assert len(SAY) == 6, f"S10 has {len(SAY)} SAY lines; this scene times 6"

        # ========================================================== 0 · part 2 opens: does the index survive?
        rm = RagMap(show=RagMap.TOP + RagMap.BOTTOM + RagMap.LABELS + RagMap.FLAGS)
        for n in RagMap.BOTTOM + ("lab_user", "lab_query", "lab_question", "flag_query", "flag_chat"):
            grey_out(rm.parts[n])
        ticks = [rm.tick(n).shift(np.array([0.1, -0.08, 0])) for n in ("chunking", "embedding", "database")]
        part2 = grey_tag("part 2").move_to([-3.7, -1.75, 0])
        db = rm.item("database").copy()

        cv = ComposeView(show=("chroma",))
        for n in UNUSED_V2:
            cv.remove(cv.parts[n])
        cv.shift(RIGHT * -(cv.get_left()[0] + cv.get_right()[0]) / 2)
        hb, ht, w_data, cyl = cv.parts["chroma"]
        forming = [hb.copy(), ht.copy(), w_data.copy()]
        cyl_target = cyl.copy()
        r_chroma = cv.rows["chromadb"]
        q0 = q_badge().move_to([r_chroma.glyph.get_left()[0] - 0.3, r_chroma.get_center()[1], 0])
        c = compact_v2()

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(rm), FadeIn(part2), run_time=0.9)
            self.play(rm.pulse_lane("top", DATA), run_time=1.0)
            vo.wait_until("chunk, embed, load")
            for tk in ticks:
                self.play(Create(tk), run_time=0.35)
            vo.wait_until("Part 2 asks it questions")
            self.play(rm.pulse_lane("bottom", TURN), Indicate(part2, color=TURN, scale_factor=1.15), run_time=1.1)
            vo.wait_until("But first, a test")
            self.add(db)
            self.play(FadeOut(rm), FadeOut(part2), *[FadeOut(tk) for tk in ticks],
                      db.animate.scale(1.3).move_to([db.get_center()[0], 0.2, 0]), run_time=0.6)
            self.play(Transform(db, cyl_target), *[FadeIn(m) for m in forming], run_time=0.7)
            self.remove(db, *forming)
            self.add(cv)
            self.play(*cv.parts_in("rail", "plug_chroma", "name", "port_chip", "cli", "venv", "plug_cli",
                                   "zone", "row_repo", "row_secrets", "row_volumes", "key", "door"),
                      run_time=0.6)
            self.play(*cv.parts_in("route_app", "route_secrets", "route_data", "route_port", anim=Create),
                      run_time=0.45)
            vo.wait_until("does the index survive")
            self.play(FadeIn(q0, scale=1.4), Indicate(r_chroma, color=TURN, scale_factor=1.1), run_time=0.55)
            # V2 shrinks to the top: each part becomes its compact twin
            P = cv.parts
            pairs = [(P["zone"][0], c.zone[0]), (P["zone"][1], c.zone[1]), (P["route_app"], c.route_app),
                     (P["route_data"], c.route_data), (P["route_port"], c.route_port),
                     (P["row_repo"], c.row_repo), (P["row_volumes"], c.row_volumes), (P["door"], c.door),
                     (P["rail"], c.rail), (P["plug_cli"], c.plug_cli), (P["plug_chroma"], c.plug_chroma),
                     (P["cli"][0], c.cli[0]), (P["cli"][1], c.cli[1]), (P["cli"][2], c.cli[2]),
                     (P["chroma"], c.chroma), (P["name"], c.name), (P["port_chip"], c.port_chip),
                     (q0, c.qmark)]
            gone = [P["cli"][3], P["row_secrets"], P["key"], P["venv"], P["route_secrets"]]
            srcs = [a.copy() for a, _ in pairs]
            gcop = [g.copy() for g in gone]
            self.remove(cv, q0)
            self.add(*srcs[:-1], *gcop, srcs[-1])
            self.play(*[ReplacementTransform(s, b) for s, (_, b) in zip(srcs, pairs)],
                      *[FadeOut(g) for g in gcop], run_time=1.0)
            self.remove(*[b for _, b in pairs])
            self.add(*c.order)

        # ========================================================== 1 · exit; docker ps -a: Chroma is still up
        tr = tracker("Run", 3)
        t = term(P_CTR, rows=3, container=True)
        ghost = box(c.cli[0].width, c.cli[0].height, S.GREY, dashed=True, stroke=2).move_to(c.cli[0])
        cols = grey_tag("3 of 7 columns")
        rmt = rm_note(ghost)

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t, shift=UP * 0.2), run_time=0.6)
            bare_prompt(self, t)
            self.play(caption_extra(tr, True), run_time=0.4)
            vo.wait_until("Type exit")
            ex = type_cmd(self, t, EXIT.typed(45), 0.4)
            pin(self, ex, beside(extra_tag(), t, ex), run_time=0.3)
            t.print(self, [EXIT.line(46)], run_time=0.3)
            self.play(FadeOut(c.cli, scale=0.85), FadeOut(c.plug_cli), FadeOut(c.route_app), FadeIn(ghost),
                      run_time=0.8)
            vo.wait_until("and on the laptop")
            self.play(*leave_container(t, P_REPO), run_time=0.5)
            resize(self, t, 6, run_time=0.6)
            vo.wait_until("list every container")
            ps = type_cmd(self, t, PSA.cmd, 0.5)
            pin(self, ps, beside(extra_tag(), t, ps), run_time=0.3)
            head, crow = t.print(self, PS_ROWS, run_time=0.4)
            pin(self, head, beside(cols, t, head, buff=0.6), run_time=0.3)
            vo.wait_until("The CLI container is gone")
            self.play(Indicate(ghost, color=TURN, scale_factor=1.04), run_time=0.7)
            vo.wait_until("removed on exit")
            self.play(FadeIn(rmt, scale=0.9), run_time=0.5)
            vo.wait_until("but Chroma is still up")
            up = col_box(crow, 0, len("Up 2 minutes"), TURN)
            self.play(Create(up), substring(crow, "llm-rag-chromadb").animate.set_color(TURN),
                      Indicate(c.chroma, color=TURN, scale_factor=1.05), run_time=0.8)
            stick(self, crow, up)
            vo.wait_until("and port 8000 is still taken")
            self.play(substring(crow, "0.0.0.0:8000->8000/tcp").animate.set_color(LOOKUP),
                      *light_door(c, LOOKUP), run_time=0.6)
            self.play(flash(c.route_port_line), Indicate(c.port_chip, color=LOOKUP, scale_factor=1.1), run_time=1.0)

        # ========================================================== 2 · docker compose down
        warn_rows = word_fold(WARN_CREDS) + word_fold(WARN_PROJ)
        assert len(warn_rows) == 4, warn_rows
        harm = grey_tag("harmless: the values live only in docker-shell.sh")

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(rmt), run_time=0.3)
            dn = type_cmd(self, t, DOWN_.cmd, 0.6)
            pin(self, dn, beside(extra_tag(), t, dn), run_time=0.3)
            vo.wait_until("Two warnings")
            w = t.print(self, [(r, ERR) for r in warn_rows], run_time=0.6)
            self.play(Indicate(substring(w[0], "GOOGLE_APPLICATION_CREDENTIALS"), color=TURN, scale_factor=1.06),
                      Indicate(substring(w[2], "GCP_PROJECT"), color=TURN, scale_factor=1.1), run_time=0.8)
            vo.wait_until("They're harmless")
            beside(harm, t, w[3], buff=0.4)
            self.play(*[r.animate.set_color(S.GREY) for r in w], run_time=0.6)
            pin(self, w[3], harm, run_time=0.4)
            vo.wait_until("and the down command needs neither")
            self.play(Indicate(substring(dn, DOWN_.cmd), color=TURN, scale_factor=1.06), run_time=0.8)
            vo.wait_until("Then Chroma and the network")
            gone = print_build(self, t, [DOWN_.line(n) for n in (5, 6, 7)], run_time=0.5)
            self.play(FadeOut(VGroup(c.chroma, c.name, c.port_chip, c.plug_chroma, c.route_data, c.route_port,
                                     ghost)), *light_door(c, LAPTOP),
                      Indicate(gone[1], color=TURN, scale_factor=1.03), run_time=0.7)
            self.play(FadeOut(c.rail), Indicate(gone[2], color=TURN, scale_factor=1.03), run_time=0.5)

        # ========================================================== 3 · nothing runs; the folder holds the data
        band = right_at(file_row("docker-volumes/chromadb/"), BAND_RIGHT, BAND_Y)
        q_at = np.array([band.glyph.get_left()[0] - 0.45, BAND_Y, 0])
        outs = right_at(file_row("outputs/"), q_at[0] - 1.1, BAND_Y)
        outs_tick = check_mark(0.24, DATA, 4).next_to(outs, RIGHT, buff=0.16)
        glow = backlight(band)
        ans = tick_badge().move_to(q_at)

        with self.voiceover(SAY[3]) as vo:
            t.clear(self, run_time=0.3)
            self.bring_to_front(c.row_volumes, c.qmark)
            resize(self, t, 13, run_time=0.9,
                   extra=[FadeOut(VGroup(c.zone, c.row_repo, c.door)),
                          ReplacementTransform(c.row_volumes, band), c.qmark.animate.move_to(q_at)])
            self.bring_to_back(glow)
            cmd = _type_rows(self, t, AFTER_ROWS, len(P_REPO) + 1, 1.0, len(AFTER.cmd))
            pin(self, cmd, beside(extra_tag(), t, cmd), run_time=0.3)
            out = t.print(self, AFTER.at((2, 12)), run_time=0.6)
            nets = out[1:5]
            empty = col_box(out[0], 0, len(out[0].text), TURN)
            nonet = note("no llm-rag-network")
            nonet.move_to([nets[0].get_right()[0] + 0.7 + nonet.width / 2, VGroup(*nets).get_center()[1], 0])
            self.play(Create(empty), FadeIn(nonet, shift=LEFT * 0.1), run_time=0.6)
            stick(self, out[0], empty)
            vo.wait_until("But the docker volumes folder")
            self.play(glow.animate.set_fill(S.GREY, 0.2).set_stroke(S.GREY, 2, opacity=1),
                      Indicate(band, color=INK, scale_factor=1.06), run_time=0.9)
            sq = out[9]
            i_sq = sq.text.index("chroma.sqlite3")
            sqb = col_box(sq, i_sq, i_sq + len("chroma.sqlite3"), TURN)
            self.play(Create(sqb), FadeOut(c.qmark, scale=0.6), FadeIn(ans, scale=1.5), run_time=0.7)
            stick(self, sq, sqb)
            ubs = [col_box(out[k], out[k].text.index(u), len(out[k].text), DATA) for k, u in ((8, UUIDS[0]), (10, UUIDS[1]))]
            dif = differ_tag()
            dif.move_to(out[5].strut).align_to(t.box, RIGHT).shift(LEFT * 0.12)
            vo.wait_until("and both index folders")
            self.play(*[Create(b) for b in ubs], FadeIn(dif), run_time=0.6)
            stick(self, out[8], ubs[0])
            stick(self, out[10], ubs[1])
            stick(self, out[5], dif)
            vo.wait_until("and your chunk files")
            self.play(FadeIn(outs, shift=DOWN * 0.15), run_time=0.5)
            self.play(Create(outs_tick), run_time=0.4)

        # ========================================================== 4 · back another day: sh docker-shell.sh
        mm = band_minis(band)
        np_chip = grey_tag("no pull · no build: the image exists")
        g1 = note("after a git pull that changes pyproject.toml")
        # a command shown, not output: a pill slim enough to sit on one terminal row
        build_chip = chip("docker compose build", S.GREY, size=CAPTION, font=MONO, pad_x=0.14, pad_y=0.04)
        assert build_chip.height < 0.36, build_chip.height
        g2 = VGroup(note("or the Dockerfile:"), build_chip).arrange(RIGHT, buff=0.15)
        gnote = VGroup(g1, g2)
        idt = grey_tag("container id · your numbers will differ")
        yt = your_turn()

        with self.voiceover(SAY[4]) as vo:
            self.play(caption_extra(tr, False), FadeOut(VGroup(outs, outs_tick, ans, nonet)),
                      glow.animate.set_fill(S.GREY, 0).set_stroke(opacity=0), run_time=0.5)
            t.clear(self, run_time=0.3)
            vo.wait_until("sh docker-shell.sh again")
            cmd4 = type_cmd(self, t, AGAIN.cmd, 0.7)
            l2 = t.print(self, [AGAIN.line(2)], run_time=0.25)[0]
            print_build(self, t, [AGAIN.line(3)], run_time=0.3)
            self.play(Create(mm.rail), run_time=0.3)
            print_build(self, t, [AGAIN.line(4)], run_time=0.3)
            self.play(FadeIn(mm.chroma, shift=DOWN * 0.3), run_time=0.4)
            self.play(Create(mm.route), Indicate(band, color=LOOKUP, scale_factor=1.05), run_time=0.5)
            vo.wait_until("No pull, no build")
            rb = col_box(l2, 0, len(l2.text), TURN)
            beside(np_chip, t, l2, buff=0.5)
            self.play(Create(rb), FadeIn(np_chip, shift=LEFT * 0.1), run_time=0.6)
            stick(self, l2, rb, np_chip)
            out4 = t.print(self, AGAIN.at((5, 12)), run_time=0.8)
            self.play(FadeIn(mm.cli, shift=DOWN * 0.3), Indicate(VGroup(out4[0], out4[1]), color=CTR, scale_factor=1.02),
                      run_time=0.6)
            t.set_prompt(P_CTR2)
            pr = bare_prompt(self, t)
            self.play(*enter_container(t, P_CTR2), run_time=0.5)
            cid = substring(pr, P_CTR2.split("@")[1].split(":")[0])
            uid = under(cid, S.GREY, stroke=3)
            beside(idt, t, pr, buff=0.35)
            self.play(Create(uid), FadeIn(idt, shift=LEFT * 0.1), run_time=0.45)
            stick(self, pr, uid)
            vo.wait_until("After a git pull")
            x_note = out4[2].get_right()[0] + 0.9         # right of the two short rows, one line each
            left_at(g1, x_note, out4[2].strut.get_center()[1])
            left_at(g2, x_note, out4[3].strut.get_center()[1])
            self.play(FadeIn(gnote, shift=LEFT * 0.15), run_time=0.6)
            vo.wait_until("run docker compose build first")
            self.play(Indicate(build_chip, color=TURN, scale_factor=1.08), run_time=0.8)
            vo.wait_until("Pause and restart")
            beside(yt, t, cmd4, buff=0.4)
            self.play(FadeIn(yt, scale=1.2), run_time=0.5)
        self.wait(2)                                   # ▶ beat: hold the frame

        # ========================================================== 5 · two extra checks: the data never lived in it
        t2 = term(P_HOME, rows=8, title="laptop · second terminal")
        ln = mono_line(P_HOME, t2.size, INK, t2c=t2._prompt_colors(P_HOME))   # it opens in ~
        t2._place(ln, 0)
        t2.lines.add(ln)
        ti = P_HOME.index("~")
        # above the frame, so it stays readable while the curl line is typed (rows 0–3 are full)
        cap2 = note("new terminal: cd here first").next_to(t2.box, UP, buff=0.15)
        cap2.align_to(t2.box, LEFT).shift(RIGHT * 0.3)
        tc = term(P_CTR2, rows=6, container=True)
        rmnote = note("not in the README · S12")
        panel = log_panel(IDS_ROWS, "the same command before exit", width=TERM_W, size=TERM_PT)
        stf = staff_tag()
        match = chip("10 of 10 match", DATA, size=CAPTION)

        # after the ▶ hold (silent): the second terminal opens in ~, the caption says cd first
        self.play(caption_extra(tr, True), FadeOut(VGroup(t, idt, yt, gnote)), FadeIn(t2, shift=UP * 0.2),
                  run_time=0.6)
        self.play(Indicate(glyph_range(ln, ti, ti + 1), color=TURN, scale_factor=1.4),
                  FadeIn(cap2, shift=DOWN * 0.1), run_time=0.6)
        with self.voiceover(SAY[5]) as vo:
            # after the cd: "~$" stretches into "~/AC215/llm-rag$"; "student@laptop:" stays put
            t2.set_prompt(P_REPO)
            ln2 = mono_line(P_REPO, t2.size, INK, t2c=t2._prompt_colors(P_REPO))
            t2._place(ln2, 0)
            t2.lines.remove(ln)
            head, tail = glyph_range(ln, 0, ti), glyph_range(ln, ti, len(P_HOME))
            tail2 = glyph_range(ln2, ti, len(P_REPO))
            self.add(head, tail)
            self.play(ReplacementTransform(tail, tail2), run_time=0.4)
            self.remove(head, tail2)             # the typed rows start with the same prompt
            cu = _type_rows(self, t2, CURL_ROWS, len(P_REPO) + 1, 0.9, len(NAMES.cmd))
            pin(self, cu, beside(extra_tag(), t2, cu), run_time=0.25)
            o = t2.print(self, NAMES.at((2, 5)), run_time=0.35)
            self.play(substring(o[0], "char-split-collection").animate.set_color(DATA),
                      substring(o[2], "recursive-split-collection").animate.set_color(DATA), run_time=0.35)
            vo.wait_until("with dimension 256")
            dims = [col_box(o[k], 0, len(o[k].text), TURN) for k in (1, 3)]
            self.play(*[Create(b) for b in dims], run_time=0.45)
            for k, b in zip((1, 3), dims):
                stick(self, o[k], b)
            vo.wait_until("and an extra command called get")
            self.play(FadeOut(VGroup(t2, cap2)), FadeIn(tc, shift=UP * 0.2), run_time=0.5)
            g = type_cmd(self, tc, GET.cmd, 0.7)
            ext = beside(extra_tag(), tc, g)
            beside(rmnote, tc, g.rows[0], buff=0.4)
            self.play(FadeIn(ext, shift=LEFT * 0.1), FadeIn(rmnote, shift=LEFT * 0.1), run_time=0.3)
            stick(self, g, ext)
            stick(self, g.rows[0], rmnote)
            got = tc.print(self, IDS_ROWS, run_time=0.4)
            # the PANEL above: the same command before exit (rows aligned with the terminal's)
            x_text = got[0].strut.get_left()[0]
            panel.shift(np.array([x_text - panel.rows[0].strut.get_left()[0],
                                  tc.box.get_top()[1] + 0.3 - panel.frame.get_bottom()[1], 0]))
            stf.next_to(panel.header, RIGHT, buff=0.35)
            match.move_to(panel.header).align_to(panel.frame, RIGHT)
            # both lists are cut after the ids' "]": a GREY " …" says the line goes on
            panel.add(more_mark(panel.rows[-1]))
            more_t = more_mark(got[-1])
            self.play(FadeIn(panel, shift=DOWN * 0.15), FadeIn(stf), FadeIn(more_t), run_time=0.45)
            stick(self, got[-1], more_t)
            marks = VGroup()
            colour = []
            for rows in (panel.rows, got):
                for k, sid in ((0, FIRST_ID), (3, LAST_ID)):
                    colour.append(substring(rows[k], sid).animate.set_color(DATA))
                    marks.add(check_mark(0.2, DATA, 4).move_to([rows[k].strut.get_left()[0] - 0.07,
                                                                rows[k].strut.get_center()[1], 0]))
            self.play(*colour, *[Create(m) for m in marks], run_time=0.5)
            self.play(FadeIn(match, scale=0.8), run_time=0.35)
            vo.wait_until("The container was disposable")
            self.play(FadeOut(VGroup(tc, panel, stf, match, marks)), run_time=0.5)
            pic = VGroup(mm.rail, mm.route, mm.cli, mm.chroma, band)
            self.play(pic.animate.scale(1.8).move_to([0, 0.3, 0]), run_time=0.8)
            ghosts = VGroup(*[box(m[0].width, m[0].height, S.GREY, dashed=True, stroke=2).move_to(m[0])
                              for m in (mm.cli, mm.chroma)])
            disp = grey_tag("disposable").next_to(ghosts, UP, buff=0.25)
            self.play(FadeOut(VGroup(mm.cli, mm.chroma, mm.rail, mm.route), scale=0.9), FadeIn(ghosts),
                      FadeIn(disp, shift=DOWN * 0.1), run_time=0.8)
            vo.wait_until("the data never lived in it")
            glow2 = backlight(band, pad=0.18)
            self.bring_to_back(glow2)
            self.play(glow2.animate.set_fill(S.GREY, 0.22).set_stroke(S.GREY, 2, opacity=1),
                      Indicate(band, color=INK, scale_factor=1.06), run_time=0.9)
        self.play(FadeOut(VGroup(tr, ghosts, disp, band, glow, glow2)), run_time=0.8)
        self.wait(0.3)
