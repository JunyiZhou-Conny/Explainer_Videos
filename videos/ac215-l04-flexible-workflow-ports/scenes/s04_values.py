"""S04 · Your bucket and your three values (README "Before you run": layout, cli.py, bucket).

Beats (script.md "## S04", one voiceover block each):
 0  TRACKER B/1. Upper half: the README's folder layout (README.md · lines 107–117) as a tree:
    <your-workspace>/ → mega-pipeline/ (GREY, five GREY component-folder glyphs, "five component
    folders") and secrets/ → mega-pipeline.json (dashed ghost row, flashes GOLD on "your key").
    secrets/ gets the GREY caption "outside the repo · mounted at runtime" ("outside the repo"
    flashes on "never inside it"). Lower half: the 8-row laptop terminal at ~/AC215/mega-pipeline.
    TRACKER B/1 · extra: `cd ..` (extra) → the dropped "/mega-pipeline" flashes BLUE on the typed
    line, the new prompt ~/AC215 too; <your-workspace>/ pulses YELLOW + tag "you are here".
    `mkdir secrets`, `ls` → mega-laptop/06 lines 2–3, `ls -la secrets` → lines 4–6 (all extra);
    secrets/ gets a GREEN check, the json row a GREY tag "next".
 1  TRACKER B/2. The tree fades. README.md · lines 128–130 (comment cut) at the top; the three
    names flash YELLOW and get GREY labels "project ID", "bucket", "group name" as said.
 2  TRACKER B/2 · extra. The panel goes, the terminal grows to 12 rows (cleared): `cd mega-pipeline`
    (extra) → prompt ~/AC215/mega-pipeline; the grep (extra; folds) → mega-laptop/07 lines 2–4, …,
    11–16 (cut). The blank values flash; the values of generate_text (lines 2–4) and translate_text
    (14–16) turn RED. Copies of the folder names and values lift off as the terminal shrinks to the
    strip and become a 5 × 3 grid card: GREY `""` cells, RED-outlined cells in the generate_text and
    translate_text rows; "course's project", "course's bucket", "instructor's group" write in as
    said (the values themselves stay in the strip only).
 3  TRACKER B/2. The strip fades; the grid shrinks into a glyph-only miniature at the top right.
    README chip README.md · line 134 "if you forget, the script stops before doing anything" +
    erratum tag. generate_text/cli.py · line 21: `!= ""` highlights; a GREEN tick lands on the
    miniature's RED generate_text row, note "not empty → passes". The chip and panel go; both RED
    rows flash; a PINK arrow runs from the row to a BLUE cloud "course project · not yours" and
    bounces RED (cross); RED chip "permission error".
 4  TRACKER B/2 · extra. Chip "all five folders" (top band). A GREY editor ("in your editor") with
    transcribe_audio/cli.py · lines 17–21: a YELLOW pencil sets lines 17, 18, 21 (the edited text is
    the capture's own `+` lines). The editor goes; the terminal returns (10 rows, ~/AC215/mega-
    pipeline): `cd transcribe_audio`, `git diff cli.py` (extra) → mega-laptop/11 lines 10–17, `-` RED,
    `+` GREEN; the three placeholders get YELLOW boxes as named and a YELLOW tag "type your own";
    `cd ..` (extra), prompt back. GREY chip "translate_text/cli.py · line 64: target_language="es" →
    "fr" · why: in a few minutes" ("es" / "fr" flash as said). ▶ your turn by "all five folders".
 5  TRACKER B/3. The terminal fades. A BLUE cabinet `your-team-bucket` (illustration) with the seven
    drawers of README.md:152–158 (the bonus dashed); the drawers light in turn; every drawer but
    input_audios/ opens a PINK `group-01/`; the GOLD tag "your project pays · storage (tiny)" slides
    onto the cabinet.
 6  Tag "erratum · no command given" (top band). A schematic console (browser, illustration tag on
    its bottom edge): "Cloud Storage › Buckets › Create", Name field, Create button. README.md ·
    line 313 · Appendix under the cabinet: `input_audios/test.mp3` struck through RED. On "Create
    the bucket": `your-team-bucket` types into the field, Create flashes, the cabinet's name flashes.
 7  The console shrinks away (and the 313 panel goes). A waveform file with the chip
    `input-<something>.mp3` slides into input_audios/ (file in the drawer, chip beside the cabinet).
    The chip slides down into a GREY `text_prompts/group-01/` folder and morphs .mp3 → .txt
    (caption "transcribe · cli.py line 62: same name, .txt"). The excerpt chip `"input-*.txt"`
    (transcribe_audio/cli.py · line 102 (excerpt)) stands beside the cabinet's text_prompts/ row:
    the .txt chip passes it (GREEN tick) into text_prompts/ group-01/; a `test.txt` chip bounces
    off it (GREY). Fade out to an empty frame.

Deviations from SHOW (and why):
- Beat 0: the tracker caption gets " · extra" while the four extra commands are typed (the script's
  convention for extras; the README's step 1 has no command). The tree draws the five component
  folders as five GREY folder glyphs with the note "five component folders" (nine rows of names
  do not fit above an 8-row terminal).
- Beat 0: the dropped "/mega-pipeline" flashes on the `cd ..` line, where it is still written
  (the new prompt no longer has it).
- Beat 1: README.md line 130 is 70 characters, so it is cut at its comment (script rule), header
  "· comment cut".
- Beat 3: the grid cannot shrink with text at >= 20 pt, so it becomes a glyph-only miniature (the
  script's rule for miniatures); the tick lands on its RED generate_text row.
- Beat 4: "all five folders" appears when the SAY says "in all five files" (start of the beat)
  and stays to the ▶; the ▶ your turn sits beside it (the checkpoint is an edit, not a command).
  One "type your own" tag (beside line 12, where there is room) and YELLOW boxes on the three
  placeholders: line 13 is 57 characters, no room for a tag beside it.
- Beat 4: the chip "translate_text/cli.py · line 64 …" is one GREY chip with mono parts.
- Beat 7: the `"input-*.txt"` gate stands beside the cabinet's text_prompts/ row (between the
  local folder and the bucket's text_prompts/ group-01/), the local folder below it.
"""

from common import *
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    TAU,
    UP,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    ShowIncreasingSubsets,
    Transform,
    TransformFromCopy,
    VGroup,
    Wiggle,
    linear,
    there_and_back,
)

from explainer import style as S
from explainer.devops import form_rows
from explainer.scene import VoiceScene

SAY = NARRATION["S04"]
assert len(SAY) == 8, len(SAY)

ML = "mega-laptop"
README = "mega-pipeline/README.md"
CLI_A = "mega-pipeline/transcribe_audio/cli.py"
CLI_B = "mega-pipeline/generate_text/cli.py"
CLI_D = "mega-pipeline/translate_text/cli.py"

# ------------------------------------------------------------------ commands and real outputs
CD_UP = "cd .."                                  # extra (script.md S04): a cd prints nothing
_sec = capture("06", ML)
MKDIR, LS, LS_SEC = _sec.cmd.split("; ")
assert (MKDIR, LS, LS_SEC) == ("mkdir secrets", "ls", "ls -la secrets")
LS_OUT = _sec.at((2, 3))
assert LS_OUT == ["mega-pipeline", "secrets"]
LA_OUT = _sec.at((4, 6))
assert LA_OUT[0] == "total 8" and LA_OUT[1].endswith(" .") and LA_OUT[2].endswith(" ..")

CD_REPO = capture("02", ML).cmd
assert CD_REPO == "cd mega-pipeline"
GREP = capture("07", ML)
assert GREP.cmd == "grep -n -E '^(gcp_project|bucket_name|group_name) *=' */cli.py"
GREP_OUT = GREP.at((2, 4), "…", (11, 16))
ROWS = {}                                        # folder -> [file lines of its three values]
for _n in range(2, 17):
    _f = GREP.line(_n).split("/")[0]
    ROWS.setdefault(_f, []).append(_n)
GRID_ROWS = list(ROWS)                           # grep order: alphabetical
assert GRID_ROWS == ["generate_text", "synthesis_audio", "synthesis_audio_en", "transcribe_audio",
                     "translate_text"]
VARS = ["gcp_project", "bucket_name", "group_name"]
BLANK = {f for f, ns in ROWS.items() if all(' = ""' in GREP.line(n) for n in ns)}
assert BLANK == {"synthesis_audio", "synthesis_audio_en", "transcribe_audio"}
SHIPPED = {2: '"ac215-project"', 3: '"mega-pipeline-bucket"', 4: '"pavlos-advanced"',
           14: '"ac215-project"', 15: '"mega-pipeline-bucket"', 16: '"pavlos-advanced"'}
for _n, _v in SHIPPED.items():
    assert f"= {_v}" in GREP.line(_n), (_n, _v)
COURSE = ["course's project", "course's bucket", "instructor's group"]

CD_A = "cd transcribe_audio"                     # extra (script.md S04)
EDIT = capture("11", ML)
assert EDIT.cmd == "git diff cli.py"
DIFF = EDIT.at((10, 17))
assert [s[0] for s in DIFF] == ["-", "-", "+", "+", " ", " ", "-", "+"]
DIFF_COL = {"-": ERR, "+": VENV, " ": OUTPUT}
PLACEHOLDERS = [VALUES["gcp_project"], VALUES["bucket_name"], VALUES["group_name"]]
for _p, _n in zip(PLACEHOLDERS, (12, 13, 17)):
    assert f'"{_p}"' in EDIT.line(_n)

# ------------------------------------------------------------------ sources
L134 = excerpt(README, 134, 134)
PH134 = "if you forget, the script stops before doing anything"
assert PH134 in L134
L21 = excerpt(CLI_B, 21, 21)
assert L21 == 'assert group_name != "", "Update group name"'
L64 = excerpt(CLI_D, 64, 64)
ES = 'target_language="es"'
assert ES in L64
L313 = excerpt(README, 313, 313)
TEST_MP3 = "input_audios/test.mp3"
assert TEST_MP3 in L313
L62 = excerpt(CLI_A, 62, 62)
assert 'uuid + ".txt"' in L62
L102 = excerpt(CLI_A, 102, 102)
GLOB = '"input-*.txt"'
assert GLOB in L102
# the editor: lines 17-21 before, and after the edit as the capture's diff shows them
BEFORE = excerpt(CLI_A, 17, 21).split("\n")
AFTER = [s[1:] for s in EDIT.at(12, 13, 14, 15, 17)]
assert BEFORE[2:4] == AFTER[2:4] and BEFORE[0] == EDIT.line(10)[1:] and BEFORE[4] == EDIT.line(16)[1:]
assert excerpt(README, 152, 158).count("`") == 14          # the seven prefixes of the cabinet

# ------------------------------------------------------------------ layout
Y_UNDER = 2.57          # the row under the tracker (tracker bottom 2.92)
Y_BAND = 3.21           # the top band, right of the tracker
X_L, X_R = -6.45, 6.32
TOP = 2.8               # top of the pictures under the tracker
CAB_TOP = 2.8           # cabinet frame top (beats 5-7)


def at_left(m, x: float, y: float):
    return m.move_to([x + m.width / 2, y, 0])


def at_right(m, x: float, y: float):
    return m.move_to([x - m.width / 2, y, 0])


def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def fit_tag(t, line, s: str = "extra"):
    """A GREY tag beside terminal line `line` (its last row): 22 pt, or 20 pt when the row leaves
    too little room. Positioned, not added."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    end = row.glyphs.get_right()[0]
    for size in (TAG, CAPTION):
        tg = beside(tag(s, S.GREY, size=size), t, line)
        if tg.get_left()[0] >= end + 0.1:
            return tg
    raise ValueError(f"no room for the tag {s!r} beside {row.text!r}")


def type_extra(scene, t, cmd: str, type_time: float = 0.5):
    """Type an extra command and pin its GREY `extra` tag beside it; when the row has no room
    (a long prompt), the tag sits at the right end of the terminal's title bar instead (as a
    member of the terminal, so it leaves with it). Returns the line."""
    ln = type_cmd(scene, t, cmd, type_time=type_time)
    try:
        pin(scene, ln, fit_tag(t, ln), run_time=0.25)
    except ValueError:
        tg = extra_tag()
        tg.move_to([t.box.get_right()[0] - 0.2 - tg.width / 2, t.title.get_center()[1], 0])
        scene.play(FadeIn(tg), run_time=0.25)
        scene.remove(tg)
        t.add(tg)
    return ln


# ------------------------------------------------------------------ beat 0: the folder layout
def build_tree():
    """README.md:107-117 as a tree (no frame): .header .ws .repo .five .five_note .sec .sec_note
    (.out .rest) .json .conns .check_at (where the GREEN check goes)."""
    size = TAG
    x0, pitch, ind = -6.3, 0.44, 0.55
    ws = file_row("<your-workspace>/", INK, LAPTOP, size=size)
    repo = file_row("mega-pipeline/", INK, LAPTOP, size=size)
    sec = file_row("secrets/", INK, LAPTOP, size=size)
    js = ghost_file("mega-pipeline.json")
    rows = [(ws, 0), (repo, 1), (sec, 1), (js, 2)]
    y0 = TOP - 0.62
    for i, (r, lvl) in enumerate(rows):
        r.shift(np.array([x0 + lvl * ind - r.glyph.get_left()[0], y0 - i * pitch - r.text.get_center()[1], 0]))
    five = VGroup(*[folder_glyph(0.2, LAPTOP) for _ in range(5)]).arrange(RIGHT, buff=0.1)
    five.next_to(repo.text, RIGHT, buff=0.35).match_y(repo.glyph)
    five_note = note("five component folders").next_to(five, RIGHT, buff=0.2).match_y(repo.text)
    out = note("outside the repo")
    rest = note("· mounted at runtime")
    sec_note = VGroup(out, rest).arrange(RIGHT, buff=0.12)
    sec_note.next_to(sec.text, RIGHT, buff=0.75).match_y(sec.text)
    sec_note.out, sec_note.rest = out, rest
    check_at = sec.text.get_right() + RIGHT * 0.37
    conns = VGroup()
    for parent, kids in ((ws, (repo, sec)), (sec, (js,))):
        x = parent.glyph.get_center()[0]
        top = parent.glyph.get_bottom()[1] - 0.04
        bot = kids[-1].glyph.get_center()[1]
        conns.add(Line([x, top, 0], [x, bot, 0], color=S.GREY_DARK, stroke_width=2))
        for k in kids:
            y = k.glyph.get_center()[1]
            conns.add(Line([x, y, 0], [k.glyph.get_left()[0] - 0.06, y, 0], color=S.GREY_DARK,
                           stroke_width=2))
    header = VGroup(mono("README.md", CAPTION, S.GREY), label("· lines 107–117", CAPTION, S.GREY))
    header.arrange(RIGHT, buff=0.12)
    at_left(header, x0 - 0.05, TOP - 0.16)
    g = VGroup(header, conns, ws, repo, five, five_note, sec, sec_note, js)
    g.header, g.ws, g.repo, g.five, g.five_note = header, ws, repo, five, five_note
    g.sec, g.sec_note, g.json, g.conns, g.check_at = sec, sec_note, js, conns, check_at
    return g


# ------------------------------------------------------------------ beat 2: the grid card
COL0, COLW, PITCH = 3.15, 2.62, 0.5


def build_grid():
    """The 5 x 3 grid of the shipped values. .frame .sep .heads .names[r] .cells[r][c]; a RED cell
    is VGroup(rect, label) with .rect .label; a blank cell is a GREY mono '""'."""
    heads = [mono(v, CAPTION, S.GREY) for v in VARS]
    names, cells = [], []
    w = 0.3 + COL0 + 3 * COLW + 0.15
    h = 0.45 + PITCH * (len(GRID_ROWS) + 1) + 0.1
    fr = box(w, h, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
    x0 = fr.get_left()[0] + 0.3
    ytop = fr.get_top()[1] - 0.25 - PITCH / 2
    for c, hd in enumerate(heads):
        hd.move_to([x0 + COL0 + (c + 0.5) * COLW, ytop, 0])
    sep = Line([fr.get_left()[0] + 0.15, ytop - PITCH / 2 - 0.02, 0],
               [fr.get_right()[0] - 0.15, ytop - PITCH / 2 - 0.02, 0], color=S.GREY_DARK, stroke_width=2)
    for r, f in enumerate(GRID_ROWS):
        y = ytop - (r + 1) * PITCH - 0.06
        nm = mono(f, CAPTION, INK).move_to([x0, y, 0], aligned_edge=LEFT)
        names.append(nm)
        row = []
        for c in range(3):
            cx = x0 + COL0 + (c + 0.5) * COLW
            if f in BLANK:
                cell = mono('""', CAPTION, S.GREY).move_to([cx, y, 0])
            else:
                lab = label(COURSE[c], CAPTION, INK)
                rect = box(COLW - 0.14, PITCH - 0.08, ERR, fill_opacity=0.1, radius=0.08, stroke=3)
                rect.move_to([cx, y, 0])
                lab.move_to(rect)
                cell = VGroup(rect, lab)
                cell.rect, cell.label = rect, lab
            row.append(cell)
        cells.append(row)
    g = VGroup(fr, sep, *heads, *names, *[c for r in cells for c in r])
    g.frame, g.sep, g.heads, g.names, g.cells = fr, sep, heads, names, cells
    return g


def mini_grid(grid, w: float = 3.4, h: float = 1.6):
    """A glyph-only miniature of the grid (w x h): frame, separator, GREY bars for names and
    headers, GREY dashes for blank cells, the RED cell outlines. .rows[r] (the row's shapes)."""
    kx, ky = w / grid.frame.width, h / grid.frame.height
    k = np.array([kx, ky, 1.0])
    fr = box(w, h, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.08)
    fr.move_to(grid.frame)

    def at(p):
        return grid.frame.get_center() + (p - grid.frame.get_center()) * k

    def bar(m, color=S.GREY, frac=1.0, stroke=3):
        a, b = at(m.get_left()), at(m.get_right())
        b = a + (b - a) * frac
        return Line(a, b, color=color, stroke_width=stroke)

    sep = Line(at(grid.sep.get_start()), at(grid.sep.get_end()), color=S.GREY_DARK, stroke_width=1.5)
    heads = VGroup(*[bar(h, S.GREY_DARK) for h in grid.heads])
    rows = []
    for r, f in enumerate(GRID_ROWS):
        parts = [bar(grid.names[r], S.GREY)]
        for c in range(3):
            cell = grid.cells[r][c]
            if f in BLANK:
                parts.append(Line(at(cell.get_left()), at(cell.get_right()), color=S.GREY_DARK,
                                  stroke_width=3))
            else:
                rr = box(cell.rect.width * kx, cell.rect.height * ky, ERR, fill_opacity=0.15, radius=0.03,
                         stroke=2.5)
                rr.move_to(at(cell.rect.get_center()))
                parts.append(rr)
        rows.append(VGroup(*parts))
    g = VGroup(fr, sep, heads, *rows)
    g.frame, g.rows = fr, rows
    return g


# ------------------------------------------------------------------ beat 4: the edit
def mixed_chip(parts, color: str = S.GREY):
    """One GREY chip of mixed serif / mono parts: parts = [(text, "mono"|"serif", colour)]."""
    mobs = VGroup(*[(mono if kind == "mono" else label)(s, CAPTION, col) for s, kind, col in parts])
    mobs.arrange(RIGHT, buff=0.14)
    for m in mobs:
        m.match_y(mobs[0])
    h = mono("|", CAPTION).height + 0.24
    fr = box(mobs.width + 0.48, h, color, fill=S.BG, fill_opacity=0.92, radius=h / 2.6)
    fr.move_to(mobs)
    g = VGroup(fr, mobs)
    g.frame, g.parts = fr, mobs
    return g


# ------------------------------------------------------------------ beats 6-7: console, files
def console():
    """The schematic Cloud Storage console (no logo): .win .head .form .create .ill"""
    win = browser_window("console.cloud.google.com", width=6.7, height=3.05)
    head = VGroup(label("Cloud Storage", TAG, INK), label("›", TAG, S.GREY), label("Buckets", TAG, INK),
                  label("›", TAG, S.GREY), label("Create", TAG, INK)).arrange(RIGHT, buff=0.14)
    form = form_rows([("Name", "x")], width=5.6, size=TAG)
    create = chip("Create", CLOUD, size=TAG)
    body = VGroup(head, form, create).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
    body.move_to(win.content).align_to(win.content, LEFT).shift(RIGHT * 0.3)
    value = mono(VALUES["bucket_name"], CAPTION, INK)
    value.move_to(form.rows[0].field).align_to(form.rows[0].field, LEFT).shift(RIGHT * 0.15)
    form.rows[0].remove(form.rows[0].value)
    ill = illustration_tag()
    ill.move_to(win.frame.get_corner(DOWN + RIGHT) + np.array([-ill.width / 2 - 0.3, 0, 0]))
    g = VGroup(win, body, ill, value)
    g.win, g.body, g.head, g.form, g.create, g.ill, g.value = win, body, head, form, create, ill, value
    return g


def wave_file(h: float = 0.5):
    """A small audio file: a GREY page with a waveform."""
    f = file_glyph(h, LAPTOP)
    hs = [0.08, 0.2, 0.13, 0.24, 0.1, 0.17]
    bars = VGroup(*[Line(UP * x / 2, DOWN * x / 2, color=INK, stroke_width=2.5) for x in hs])
    bars.arrange(RIGHT, buff=0.045).move_to(f).shift(DOWN * 0.03 + LEFT * 0.02)
    return VGroup(f, bars)


def name_chip(s: str):
    return chip(s, S.GREY, size=CAPTION, font=MONO, fill_opacity=0.12)


class YourValues(VoiceScene):
    def construct(self):
        tr = tracker("B", 1)
        t = term(P_REPO, rows=8)
        tree = build_tree()

        # ========================================================== 0 · the folder layout; secrets/
        here = tag("you are here", TURN)
        here.next_to(tree.ws.text, RIGHT, buff=0.35).match_y(tree.ws.text)
        nxt = grey_tag("next").next_to(tree.json.text, RIGHT, buff=0.3).match_y(tree.json.text)
        chk = check_mark(0.3, VENV).move_to(tree.check_at)
        rows0 = [tree.ws, tree.repo, VGroup(tree.five, tree.five_note), tree.sec, tree.json]
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.15), FadeIn(t), FadeIn(tree.header), run_time=0.6)
            bare_prompt(self, t)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.12) for r in rows0], lag_ratio=0.3),
                      Create(tree.conns), run_time=1.4)
            vo.wait_until("your key lives")
            self.play(flash(tree.json, KEY, 1.12, 0.8))
            vo.wait_until("in a secrets folder")
            self.play(flash(tree.sec, INK, 1.15, 0.6))
            vo.wait_until("beside the repo")
            self.play(FadeIn(tree.sec_note, shift=LEFT * 0.15), run_time=0.5)
            vo.wait_until("never inside it")
            self.play(flash(tree.sec_note.out, TURN, 1.12, 0.8))

            vo.wait_until("Go up one level")
            self.play(caption_extra(tr, True), run_time=0.3)
            up = type_extra(self, t, CD_UP, type_time=0.35)
            t.set_prompt(P_WS)
            bp = bare_prompt(self, t)
            self.play(flash(substring(up, "/mega-pipeline"), CLOUD, 1.15),
                      flash(glyph_range(bp, P_WS.index("~"), len(P_WS) - 1), CLOUD, 1.1), run_time=0.7)
            vo.wait_until("to your workspace")
            self.play(FadeIn(here, shift=LEFT * 0.15), flash(tree.ws, TURN, 1.1, 0.8), run_time=0.8)
            vo.wait_until("and create that folder")
            type_extra(self, t, MKDIR, type_time=0.5)
            bare_prompt(self, t)
            type_extra(self, t, LS, type_time=0.2)
            lo = t.print(self, LS_OUT, run_time=0.3)
            self.play(flash(lo[1].glyphs, INK, 1.15, 0.5), flash(tree.sec.text, INK, 1.1, 0.5))
            type_extra(self, t, LS_SEC, type_time=0.5)
            t.print(self, LA_OUT, run_time=0.35)
            self.play(Create(chk), FadeIn(nxt, shift=LEFT * 0.1), run_time=0.6)

        # ========================================================== 1 · the three values
        p130 = src_panel(README, 128, 130, cut_comments=True)
        at_left(p130, X_L, 0)
        p130.shift(UP * (TOP - p130.get_top()[1]))
        labs = []
        for n, s in zip((128, 129, 130), ("project ID", "bucket", "group name")):
            lb = note(s)
            lb.move_to([p130.code.background.get_right()[0] + 0.3 + lb.width / 2,
                        p130.span(n, VARS[n - 128]).get_center()[1], 0])
            labs.append(lb)
        with self.voiceover(SAY[1]) as vo:
            self.play(tr.goto(2), FadeOut(VGroup(tree, here, nxt, chk), shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(p130, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("three values near the top")
            self.play(*[flash(p130.span(n, v), TURN, 1.1, 0.8) for n, v in zip((128, 129, 130), VARS)])
            for n, lb, cue in zip((128, 129, 130), labs, ("your project ID", "your bucket", "and your group")):
                vo.wait_until(cue)
                self.play(FadeIn(lb, shift=LEFT * 0.12), flash(p130.span(n, VARS[n - 128]), TURN, 1.15, 0.6),
                          run_time=0.6)

        # ========================================================== 2 · the extra grep; the grid
        grid = build_grid()
        grid.move_to([0, 0, 0])
        grid.shift(UP * (STRIP_TOP + 0.22 - grid.frame.get_bottom()[1]))
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p130, *labs)), caption_extra(tr, True), run_time=0.4)
            resize(self, t, 12, keep=0, run_time=0.5)
            type_extra(self, t, CD_REPO, type_time=0.4)
            cd_prompt(self, t, P_REPO, run_time=0.5)
            type_extra(self, t, GREP.cmd, type_time=0.9)
            out = t.print(self, GREP_OUT, run_time=0.5, lag=0.06)
            by_line = dict(zip([2, 3, 4, None, 11, 12, 13, 14, 15, 16], out))
            dots = out[3]
            vo.wait_until("three files are blank")
            blanks = [substring(by_line[n], '""') for n in (11, 12, 13)]
            self.play(*[flash(b, INK, 1.4, 0.8) for b in blanks], flash(dots.glyphs, INK, 1.3, 0.8))
            vals = {n: substring(by_line[n], v) for n, v in SHIPPED.items()}
            vo.wait_until("but generate text")
            self.play(*[vals[n].animate.set_color(ERR) for n in (2, 3, 4)], run_time=0.3)
            self.play(*[flash(vals[n], ERR, 1.12, 0.6) for n in (2, 3, 4)])
            vo.wait_until("and translate text")
            self.play(*[vals[n].animate.set_color(ERR) for n in (14, 15, 16)], run_time=0.3)
            self.play(*[flash(vals[n], ERR, 1.12, 0.6) for n in (14, 15, 16)])

            # copies lift into the grid as the terminal shrinks to the strip
            pairs = []
            for r, f in enumerate(GRID_ROWS):
                ns = ROWS[f]
                if ns[0] in by_line:
                    pairs.append((substring(by_line[ns[0]], f), grid.names[r]))
                    for c, n in enumerate(ns):
                        src = vals[n] if n in vals else substring(by_line[n], '""')
                        dst = grid.cells[r][c].rect if n in vals else grid.cells[r][c]
                        pairs.append((src, dst))
            hidden_rows = VGroup(*[m for r, f in enumerate(GRID_ROWS) if ROWS[f][0] not in by_line
                                   for m in (grid.names[r], *grid.cells[r])])
            movers = [a.copy() for a, _ in pairs]
            dots_mv = dots.glyphs.copy()
            self.add(*movers, dots_mv)
            resize(self, t, 3, run_time=0.6)
            self.play(Create(grid.frame), FadeIn(grid.sep), *[FadeIn(h) for h in grid.heads],
                      *[Transform(m, b) for m, (_, b) in zip(movers, pairs)],
                      Transform(dots_mv, hidden_rows), run_time=1.2)
            self.remove(*movers, dots_mv)
            red_labels = [[grid.cells[r][c].label for r in (0, 4)] for c in range(3)]
            all_labels = [m for col in red_labels for m in col]
            fam = set(all_labels)
            no_labels = VGroup(*[m for m in grid.submobjects if m not in fam and not any(
                x in fam for x in m.get_family())], *[grid.cells[r][c].rect for r in (0, 4) for c in range(3)])
            self.add(no_labels)
            vo.wait_until("the course's project and bucket")
            self.play(*[FadeIn(m) for m in red_labels[0]], run_time=0.4)
            self.play(*[FadeIn(m) for m in red_labels[1]], run_time=0.4)
            vo.wait_until("and the instructor's group name")
            self.play(*[FadeIn(m) for m in red_labels[2]], run_time=0.5)
            self.remove(no_labels, *all_labels)
            self.add(grid)

        # ========================================================== 3 · the assert only rejects ""
        mini = mini_grid(grid)
        mini.move_to([0, 0, 0])
        mini.shift(np.array([X_R - mini.frame.get_right()[0], 2.22 - mini.frame.get_top()[1], 0]))
        ok_note = note("not empty → passes")
        ok_note.next_to(mini.frame, DOWN, buff=0.14).align_to(mini.frame, RIGHT)
        tick = check_mark(0.32, VENV).move_to(mini.rows[0][0].get_center() + UP * 0.02)
        chip134 = readme_chip("README.md · line 134", PH134, max_w=12.6)
        at_left(chip134, X_L, Y_UNDER)
        err134 = erratum_tag()
        err134.move_to(chip134.frame.get_corner(UP + RIGHT) + LEFT * (err134.width / 2 + 0.3) + UP * 0.1)
        p21 = src_panel(CLI_B, 21, 21)
        at_left(p21, X_L, 1.25)
        neq = p21.span(21, '!= ""')
        bar21 = p21.bar(21, TURN)
        cl = cloud(3.0, CLOUD).move_to([-1.2, -1.75, 0])
        cl_lab = note("course project · not yours", CLOUD).next_to(cl, DOWN, buff=0.15)
        start = mini.rows[0].get_left() + LEFT * 0.15
        end = cl.get_top() + np.array([0.75, -0.25, 0])
        arr = Arrow(start, end, color=LOOKUP, buff=0.05, stroke_width=5, max_tip_length_to_length_ratio=0.08)
        direction = (end - start) / np.linalg.norm(end - start)
        xm = cross_mark(0.3, ERR).move_to(end + direction * 0.1)
        perm = chip("permission error", ERR, size=CAPTION, text_color=ERR)
        perm.next_to(cl, RIGHT, buff=0.35)
        with self.voiceover(SAY[3]) as vo:
            self.play(caption_extra(tr, False), FadeOut(t), FadeTransform(grid, mini), run_time=1.0)
            vo.wait_until("the README says")
            self.play(FadeIn(chip134, shift=DOWN * 0.1), FadeIn(err134, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("an assert stops you")
            self.play(FadeIn(p21, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("but it only rejects")
            self.play(FadeIn(bar21), flash(neq, TURN, 1.2, 0.8))
            self.play(FadeIn(tick, shift=DOWN * 0.3), FadeIn(ok_note, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Those two files")
            self.play(FadeOut(VGroup(chip134, err134, p21, bar21)),
                      flash(mini.rows[0], ERR, 1.12), flash(mini.rows[4], ERR, 1.12), run_time=0.7)
            vo.wait_until("would send your calls")
            self.play(FadeIn(cl), FadeIn(cl_lab), run_time=0.5)
            self.play(GrowArrow(arr), run_time=0.9)
            vo.wait_until("where they fail")
            self.play(arr.animate.set_color(ERR), FadeIn(xm, scale=1.4), run_time=0.4)
            self.play(arr.animate(rate_func=there_and_back).shift(-direction * 0.35),
                      FadeIn(perm, shift=LEFT * 0.15), run_time=0.7)

        # ========================================================== 4 · set all three, in all five
        five_chip = chip("all five folders", S.GREY, size=CAPTION)
        at_right(five_chip, X_R, Y_BAND)
        before = src_panel(CLI_A, 17, 21, size=20)
        after = code_panel("\n".join(AFTER), "transcribe_audio/cli.py", 17, "python", font_size=20)
        ed = editor_inset(after)
        ed.move_to([0, 0, 0]).shift(UP * (TOP - 0.1 - ed.get_top()[1]))
        before.shift(after.code.get_corner(UP + LEFT) - before.code.get_corner(UP + LEFT))
        before.header.align_to(after.header, LEFT).match_y(after.header)
        pen = pencil(0.5, TURN)
        t4 = term(P_REPO, rows=10)
        yt = your_turn()
        at_right(yt, five_chip.get_left()[0] - 0.25, Y_BAND)
        es_chip = mixed_chip([("translate_text/cli.py", "mono", S.GREY), ("· line 64:", "serif", S.GREY),
                              (ES, "mono", INK), ("→", "serif", S.GREY), ('"fr"', "mono", INK),
                              ("· why: in a few minutes", "serif", S.GREY)])
        es_chip.move_to([0, strip_top(10) + 0.14 + es_chip.height / 2, 0])
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(mini, tick, ok_note, cl, cl_lab, arr, xm, perm)),
                      caption_extra(tr, True), run_time=0.5)
            self.play(FadeIn(VGroup(ed.frame, ed[1], ed.title)), FadeIn(before), run_time=0.5)
            vo.wait_until("in all five files")
            self.play(FadeIn(five_chip, shift=LEFT * 0.15), run_time=0.4)
            pen.move_to(before.code.code_lines[0].get_right() + RIGHT * 0.5 + UP * 0.2)
            self.play(FadeIn(pen), run_time=0.2)
            for i, k in enumerate((0, 1, 4)):
                tip = after.code.code_lines[k].get_right()
                anims = [Transform(before.code.code_lines[k], after.code.code_lines[k])]
                if i == 0:
                    anims.append(Transform(before.code.background, after.code.background))
                self.play(pen.animate.shift(tip - pen.tip_point() + UP * 0.05), *anims, run_time=0.45)
            vo.wait_until("An extra git diff")
            self.play(FadeOut(VGroup(ed.frame, ed[1], ed.title, before, pen)), FadeIn(t4), run_time=0.5)
            bare_prompt(self, t4)
            type_extra(self, t4, CD_A, type_time=0.45)
            cd_prompt(self, t4, p_comp("transcribe_audio"), run_time=0.5)
            type_extra(self, t4, EDIT.cmd, type_time=0.4)
            d = t4.print(self, [(s, DIFF_COL[s[0]]) for s in DIFF], run_time=0.5, lag=0.06)
            plus = {12: d[2], 13: d[3], 17: d[7]}
            boxes = []
            for (n, ln), p, cue in zip(plus.items(), PLACEHOLDERS,
                                       ("your-project-id,", "your-team-bucket and", "and group-01")):
                vo.wait_until(cue)
                i = ln.text.index(f'"{p}"') + 1
                bx = col_box(ln, i, i + len(p), TURN)
                pin(self, ln, bx, anim=Create(bx), run_time=0.35)
                boxes.append(bx)
            vo.wait_until("type your own")
            own = beside(tag("type your own", TURN), t4, plus[12], buff=0.35)
            pin(self, plus[12], own, run_time=0.4)
            self.play(*[flash(b, TURN, 1.1, 0.6) for b in boxes])
            type_extra(self, t4, CD_UP, type_time=0.3)
            cd_prompt(self, t4, P_REPO, run_time=0.5)
            vo.wait_until("In translate text")
            self.play(FadeIn(es_chip, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("from Spanish")
            self.play(flash(es_chip.parts[2], TURN, 1.08, 0.7))
            vo.wait_until("to French")
            self.play(flash(es_chip.parts[4], TURN, 1.3, 0.7))
            vo.wait_until("Pause and edit them")
            self.play(FadeIn(yt, shift=LEFT * 0.15), run_time=0.4)
            self.play(Wiggle(yt, scale_value=1.15, rotation_angle=0.025 * TAU), run_time=0.7)

        # ========================================================== 5 · step 3: your bucket
        cab = Cabinet()
        cab.shift(np.array([X_L - cab.frame.get_left()[0], CAB_TOP - cab.frame.get_top()[1], 0]))
        ill5 = illustration_tag()
        ill5.move_to(cab.frame.get_corner(UP + RIGHT) + LEFT * (ill5.width / 2 + 0.25))
        pays = cost_tag("your project pays · storage (tiny)")
        pays.move_to(cab.frame.get_bottom())
        with self.voiceover(SAY[5]) as vo:
            self.play(tr.goto(3), FadeOut(VGroup(t4, es_chip, five_chip, yt)), run_time=0.6)
            self.play(FadeIn(cab, shift=RIGHT * 0.2), FadeIn(ill5), run_time=0.8)
            vo.wait_until("read and write these prefixes")
            self.play(LaggedStart(*[cab.light(p, CLOUD, run_time=0.6) for p in PREFIXES], lag_ratio=0.25),
                      run_time=1.6)
            vo.wait_until("and every output lands")
            self.play(LaggedStart(*cab.parts_in(*[f"sub{i}" for i in range(1, 6)]), lag_ratio=0.2),
                      run_time=1.0)
            self.play(FadeIn(pays, shift=LEFT * 0.6), run_time=0.6)

        # ========================================================== 6 · erratum: no command; console
        err6 = erratum_tag("no command given")
        at_right(err6, X_R, Y_BAND)
        con = console()
        con.shift(np.array([X_R + 0.03 - con.win.frame.get_right()[0], TOP - con.win.frame.get_top()[1], 0]))
        p313 = src_panel(README, 313, suffix="Appendix")
        at_left(p313, X_L, 0)
        p313.shift(UP * (-2.2 - p313.get_top()[1]))
        test_span = p313.span(313, TEST_MP3)
        st = strike(test_span, ERR)
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeIn(err6, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("how to create the bucket")
            self.play(FadeIn(VGroup(con.win, con.body)), FadeIn(con.ill), run_time=0.7)
            vo.wait_until("and its sample upload")
            self.play(FadeIn(p313, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("test dot mp3")
            self.play(Create(st), test_span.animate.set_color(ERR), run_time=0.5)
            vo.wait_until("Create the bucket")
            self.play(ShowIncreasingSubsets(con.value, rate_func=linear), run_time=0.8)
            self.add(con.value)
            self.play(flash(con.create, CLOUD, 1.12, 0.6), flash(cab.title, TURN, 1.15, 0.6))

        # ========================================================== 7 · upload input-….mp3; transcribe
        d_in = cab.drawer("input_audios/")
        d_tp = cab.drawer("text_prompts/")
        sub_tp = cab.subs[1]
        wf = wave_file(0.5)
        mp3 = name_chip("input-<something>.mp3")
        arrive = VGroup(wf, mp3).arrange(RIGHT, buff=0.2).move_to([3.3, 1.2, 0])
        wf_end = np.array([d_in.handle.get_left()[0] - 0.45, d_in.get_center()[1], 0])
        mp3_end = np.array([cab.frame.get_right()[0] + 0.25 + mp3.width / 2, d_in.get_center()[1], 0])
        # the local folder text_prompts/group-01/ (GREY): bottom right
        fol_lab = VGroup(folder_glyph(0.22, LAPTOP), mono("text_prompts/group-01/", CAPTION, INK))
        fol_lab.arrange(RIGHT, buff=0.15)
        fol = box(5.3, 1.35, LAPTOP, fill_opacity=0.06, radius=0.12)
        at_right(fol, X_R, -1.15)
        fol_lab.move_to(fol.get_corner(UP + LEFT) + np.array([0.2 + fol_lab.width / 2, -0.32, 0]))
        slot = fol.get_bottom() + UP * 0.4
        txt = name_chip("input-<something>.txt").move_to(slot)
        cap62 = note("transcribe · cli.py line 62: same name, .txt").next_to(fol, DOWN, buff=0.15)
        cap62.align_to(fol, RIGHT)
        test = name_chip("test.txt").move_to(slot)
        gate = excerpt_chip(GLOB, "transcribe_audio/cli.py · line 102 (excerpt)", line=L102)
        gate.shift(np.array([cab.frame.get_right()[0] + 0.25 - gate.chip.get_left()[0],
                             d_tp.get_center()[1] - gate.chip.get_center()[1], 0]))
        g_tick = check_mark(0.3, VENV).next_to(gate.chip, DOWN, buff=0.12)
        wait_x = gate.chip.get_right()[0] + 0.15         # chips wait right of the gate
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(con, scale=0.4, target_position=cab.title.get_center()),
                      FadeOut(VGroup(p313, st, err6)), run_time=0.7)
            vo.wait_until("upload a short recording")
            self.play(FadeIn(arrive, shift=LEFT * 0.3), run_time=0.5)
            self.play(wf.animate.move_to(wf_end), mp3.animate.move_to(mp3_end), run_time=0.9)
            self.play(flash(d_in, CLOUD, 1.05, 0.6))
            vo.wait_until("as input, dash")
            self.play(flash(mp3, TURN, 1.12, 0.9))
            vo.wait_until("The transcript keeps")
            self.play(FadeIn(VGroup(fol, fol_lab)), run_time=0.4)
            self.play(Transform(mp3, txt), run_time=1.0)
            self.remove(mp3)
            self.add(txt)
            self.play(FadeIn(cap62, shift=UP * 0.1), flash(txt.text, INK, 1.08, 0.6))
            vo.wait_until("and upload only sends")
            self.play(FadeIn(gate, shift=LEFT * 0.15), run_time=0.5)
            self.play(txt.animate.move_to([wait_x + txt.width / 2, d_tp.get_center()[1], 0]), run_time=0.7)
            self.play(FadeOut(txt, target_position=sub_tp.get_center()),
                      flash(gate.chip, VENV, 1.1, 0.8), FadeIn(g_tick, scale=1.3), run_time=0.9)
            self.play(flash(sub_tp, LOOKUP, 1.2, 0.6), flash(d_tp, CLOUD, 1.05, 0.6))
            self.play(FadeIn(test, shift=UP * 0.1), run_time=0.4)
            self.play(test.animate.move_to([wait_x + test.width / 2, d_tp.get_center()[1], 0]), run_time=0.6)
            self.play(test.animate(rate_func=there_and_back).shift(LEFT * 0.35),
                      flash(gate.chip, S.GREY, 1.1, 0.6), run_time=0.6)
            self.play(test.animate.set_color(S.GREY_DARK), run_time=0.3)
            self.wait(0.6)
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)
