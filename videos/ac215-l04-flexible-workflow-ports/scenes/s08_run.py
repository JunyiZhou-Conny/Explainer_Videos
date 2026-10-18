"""S08 · dev, run, and a stale image (README "How to Run a Component" steps 2-3; transcribe_audio
README "Python packages").

Beats (script.md "## S08", one voiceover block each):
 0  TRACKER R/2. A small V4 switchboard top right (tracks, mode words and what each does). A
    10-row terminal opens TEAL (container · synthesis_audio): `exit` -> mega-laptop/61 lines 95-96;
    the frame turns GREY (laptop); `cd ../transcribe_audio` -> the prompt changes, the new folder
    flashes BLUE. The dev track lights; `./docker-shell.sh dev` -> 17 lines 2-4, 14-17 (BuildKit
    rows, GREY time tags): "Build Mode: dev" boxed, the prompt returns with GREY "no container";
    each CACHED turns GREEN, "Building 0.3s" underlined; GREY note under the tracker "anything new
    in the folder (e.g. input_audios/ from --download) -> build steps 4-5 run again" and TEAL badges
    4 and 5 on those rows.
 1  TRACKER Y/1, README chip transcribe_audio/README.md · line 89 "inside the container". The
    terminal becomes the TEAL 3-row strip: `uv add <package>` (command only, GREY "placeholder ·
    lecture 3 ran it"). Above: V5's two halves, your laptop's transcribe_audio/ and the
    container's /app, the same GREEN pyproject.toml and uv.lock in both, joined by the PINK window;
    both pairs blink at once. The strip turns GREY: `./docker-shell.sh dev`; the chip's phrase
    becomes "baked into the image"; a TEAL image slab slides in under the container and a GREEN
    `<package>` chip drops from /app into it, "baked in".
 2  TRACKER R/3. V4 under the tracker, run track lit; RunDecision on the run track (PURPLE link).
    8-row terminal: `./docker-shell.sh run` -> 18 lines 2-6 (session: the TEAL container prompt
    app@631fac50f92b:/app$, `exit`), the laptop prompt returns. "Using local image..." boxed; the
    diamond takes "yes". The terminal shrinks to the strip; the static GREY your-turn card above
    it: ./docker-shell.sh dev, ./docker-shell.sh run, ▶ your turn.
 3  GREY tag erratum. README card README.md · line 74 "`run` to pull and run from the registry"
    (phrase underlined). CODE(transcribe_audio/docker-shell.sh: 82-89, 20 pt): the diamond
    (RunDecision's) moves beside line 83, PINK bar; line 85 YELLOW bar + GREY tag "yes: local,
    however old"; line 88 BLUE bar + BLUE tag "no: Docker Hub"; GREY note "pulled only if missing ·
    after that, the copy you have"; GREY chip README.md · line 214 "falls back to DockerHub" + GREEN
    tick.
 4  V1 returns at the top (recipe card left; your laptop with its TEAL image; BLUE shelf, sealed
    box, PINK signpost right). The diamond takes its place between them: "local image?", yes ->
    your laptop, no -> the signpost. A GREY teammate with an empty laptop, "never built it".
    PONDER(8 s) card bottom right.
 5  TRACKER R/3 · extra. 5-row terminal under V1: `docker image rm mega-pipeline-transcribe-audio`
    (extra) -> 71 lines 2-3 (cut); the TEAL image on your laptop dissolves; GREY "now we are that
    teammate" in its label's place.
 6  TRACKER R/3. `./docker-shell.sh run` -> 72 lines 2-6, …, 18-21 (cut): "Local image not found,
    using image from registry..." YELLOW; the diamond takes "no"; a BLUE arrow from the shelf box,
    a sealed copy lands on your laptop. "Creating a Pipfile for this project..." boxed, GREY tag
    "pipenv: the course's tool before uv".
 7  V1 leaves; the terminal clears and grows to 10 rows, TEAL (container · transcribe_audio):
    prompt (app) root@36615ab6e34b:/app# with root RED + RED tag "root"; session 72 lines 24-29, …,
    33, 38-39: `python --version` and `which python` are extras (GREY extra tags, the RED root tag
    stays on the prompt; TRACKER R/3 · extra until `python cli.py --help`, README line 98);
    "Python 3.8.17" boxed YELLOW; the virtualenvs path underlined; "optional arguments:" + GREY tag
    "Python 3.8's argparse wording"; `exit`.
 8  TRACKER R/3 · extra. Just before the block the container is gone: the terminal turns GREY
    (laptop), clears, goes to 20 pt and types the extra inspect as captured (74 line 1, its
    `docker image inspect` part, folded by hand: GREY ↪ rows, extra tag, GREY note "one command,
    folded to fit · type it as one line") -> 74 lines 4-7, the prompt returns. In the block the
    terminal goes; V1 returns. Under it PANEL(74: 4, 6-7, "docker image inspect --format …
    dlops/mega-pipeline-transcribe-audio · extra") and the excerpt chip PYTHON_VERSION=3.8.17
    (docker image inspect · env (excerpt)). The sealed box opens and turns RED (the stale dlops
    image; its pulled copy on your laptop too); the four labels rise as they are said
    (2025-02-18, Python 3.8.17, pipenv shell, user: root RED), each with its panel part lit.
 9  TRACKER R/3. Panel and chip clear (labels stay). CODE(pipenv-flexible-workflow ·
    transcribe_audio/Dockerfile · line 2) under V1; an older GREY card on a second shelf "branch
    pipenv-flexible-workflow", a dashed GREY line from the open box to it (your GREEN card dims).
    A GREY sheet (your folder) slides from your laptop over the box's front, inside its RED
    outline: "your code, their environment". Excerpt chip ImportError … (generate_text ·
    ./docker-shell.sh run (excerpt)) RED under it, YELLOW tick "puzzle 1".
10  TRACKER R/3 · extra. Second terminal strip (opens on ~, "new terminal: cd here first", just
    before the block): `ls -la` (extra) -> 73 …, 7; a GREY Pipfile glyph with a RED root badge
    drops out under the box and slides to your laptop; at "owned by root" the ls row's root turns
    RED and the badge flashes; `git status
    --short` (extra) -> …, 20; two GREY command chips: `rm Pipfile` (extra; GREY note under it
    "Linux asks first (root's file) → y"), `./docker-shell.sh dev` "your own image back".
11  The extras go; the box closes and is TEAL again; the fix card under V1: GREEN "build locally ·
    no argument, or dev" (the build arrow grows, your image returns), BLUE "run · only images your
    team pushed from this branch · your own DOCKER_USERNAME" (box and signpost flash), GREY "their
    newer push? docker pull <user>/<image>". Fade out to an empty frame.

Deviations from SHOW (and why):
- Beats 0-2: the switchboard shows each mode's word and what it does, not its line chips (no room
  for a fourth text row per station above a 10-row terminal); its shapes are V4 at half size.
- Beat 0: the note is three rows under the tracker (one row is 7.9 wide; the switchboard holds the
  right of the band).
- Beat 1: V5 is drawn as its two halves only (your laptop's component folder and /app), with the
  file names readable: the glyph-only thumbnail has no room for pyproject.toml and uv.lock at
  20 pt. The "arrow from the earlier line" is the order of the strip's rows (uv add, then dev).
- Beat 2: the terminal has 8 rows (the run session is 8 rows; V4 and the diamond need the band
  above it); the your-turn card sits ABOVE the strip (never beside a full-width terminal).
- Beat 4: "the switchboard between" is V4's run-track diamond between the recipe card and the
  shelf, wired to your laptop (yes) and to the signpost (no); V1's build arrow stays out until the
  fix (beat 11), so the diamond has room.
- Beats 5-6: the terminal has 5 rows, not 12, so V1 stays above it (the image that dissolves, the
  diamond's "no", the pull); the output scrolls, each highlight is on screen when it is said.
- Beat 3: the code panel's background is 0.45 wider than its text, so the line-88 tag sits inside.
- Beat 8: the strip leaves (the panel and the chip need the room under V1). The inspect is typed
  in the terminal BEFORE the block (the panel alone, captioned with a shorter command, could not be
  reproduced: typed as captioned, docker image inspect prints ~150 lines of JSON). The study guide
  lists only `--format '{{.Created}}'`, so the note doesn't send the viewer there (S06's does). The
  terminal goes to 20 pt (72 characters a row) for it: at 22 pt the 123-character --format string
  would fold inside its {{json …}} fields. Its rows break at spaces inside the single quotes, where
  a " \" would be literal, so those breaks are GREY ↪ rows (as S06 does); joined they are the
  captured command. The panel's caption names the --format … so it no longer reads as a command.
- Beats 8-10: the stale dlops image is RED (BRIEF colour table) from "opens the box" until the box
  closes in beat 11; the folder sheet is inset in the box's front so the RED outline stays visible.
- Beat 10: the Pipfile lands under your laptop (the screen holds the pulled copy); it travels
  under the shelf's caption, clear of the box's four labels. The second
  terminal opens between beats 9 and 10 (its ~ / "cd here first" opening takes 2.6 s, which the
  7.7 s SAY can't also hold). `ls -la` prints "…" and line 7 without the trailing "…": with it,
  the 3-row strip scrolled the command away as its output arrived; now the strip shows the
  command and its key line together, as `git status --short` with "…" and line 20 does after it.
- Beat 2: RunDecision's "yes" sits under the middle of its arrow (beside "local image?" it read
  "local image? yes").
- Beat 6: the command is typed and its first three lines print between beats 5 and 6, so "Local
  image not found" is on screen, and turns YELLOW, as the SAY begins with those words.
- Beats 2, 3, 8, 10: a short hold after the block keeps the your-turn card / README chip / the
  panel's "= root" / the command chips readable before the next beat clears them.
- Beat 10: `rm Pipfile` gets a GREY note under its chip: the file is root's (73 line 7), so GNU rm
  asks before removing a write-protected file (not captured, so a note, not output); the chips row
  is top-aligned under V1 to hold it above the strip.
- Beats 0-1 (SLIDES.md S08 i): the switchboard leaves at "after any change" for the "Lecture 4 ·
  slide 7" tag and the GREY "lecture's order" note; the "slides 37–38" tag sits between the slab and
  the strip, since chip89 holds the band.
"""

from common import *
from common import _header_text, _keep
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    AnimationGroup,
    Arrow,
    Create,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    Rectangle,
    ShowIncreasingSubsets,
    Succession,
    Transform,
    VGroup,
    VMobject,
    there_and_back,
)

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import PROMPT_PATH, PROMPT_USER, lecture_ref
from explainer.scene import VoiceScene

SAY = NARRATION["S08"]
assert len(SAY) == 12, len(SAY)

ML = "mega-laptop"
SH = "mega-pipeline/transcribe_audio/docker-shell.sh"
README = "mega-pipeline/README.md"
A_README = "mega-pipeline/transcribe_audio/README.md"
OLD_DF = "mega-pipeline-pipenv-flexible-workflow/transcribe_audio/Dockerfile"

# ------------------------------------------------------------------ sources (checked)
L89 = excerpt(A_README, 89, 89)
assert "`uv add <package>` **inside the container**" in L89 and "baked into the image" in L89
L74 = excerpt(README, 74, 74)
assert "`run` to pull and run from the registry" in L74
L214 = excerpt(README, 214, 214)
assert L214.startswith("./docker-shell.sh run") and "(falls back to DockerHub)" in L214
assert excerpt(SH, 83, 83) == "    if docker image inspect $IMAGE_NAME >/dev/null 2>&1; then"
assert excerpt(SH, 85, 85) == "        CONTAINER_IMAGE=$IMAGE_NAME"
assert excerpt(SH, 88, 88) == "        CONTAINER_IMAGE=$DOCKER_USERNAME/$IMAGE_NAME"
assert excerpt(OLD_DF, 2, 2) == "FROM python:3.8-slim-buster"

# ------------------------------------------------------------------ commands and real outputs
C61 = capture("61", ML)
assert C61.line(95) == "app@6172f2cd7728:/app$ exit" and C61.line(96) == "exit"
CD_A = "cd ../transcribe_audio"                    # script.md S08 (F4)
C17 = capture("17", ML)
assert C17.cmd == "./docker-shell.sh dev"
DEV_ROWS = C17.at((2, 4), (14, 17))
assert DEV_ROWS[0] == "Docker Username: dlops, Build Mode: dev"
assert DEV_ROWS[2].startswith("[+] Building 0.3s")
assert all("CACHED" in r for r in DEV_ROWS[3:])
assert "[4/5] COPY" in DEV_ROWS[5] and "[5/5] RUN uv sync" in DEV_ROWS[6]
UV_ADD = "uv add <package>"                         # transcribe_audio/README.md:89, command only
C18 = capture("18", ML)
assert C18.cmd == "./docker-shell.sh run"
assert C18.at(2, 3, 4) == ["Docker Username: dlops, Build Mode: run", "Run Docker container...",
                           "Using local image..."]
assert C18.line(5) == f"{P_RUN_LOCAL} exit" and C18.line(6) == "exit"
C71 = capture("71", ML)
assert C71.cmd == "docker image rm mega-pipeline-transcribe-audio"
C72 = capture("72", ML)
assert C72.cmd == "./docker-shell.sh run"
assert C72.line(4) == "Local image not found, using image from registry..."
assert C72.line(20) == "Creating a Pipfile for this project..."
assert C72.line(24) == f"{P_STALE} python --version" and C72.line(25) == "Python 3.8.17"
assert C72.typed(26) == "which python" and C72.typed(28) == "python cli.py --help"
assert C72.line(33) == "optional arguments:" and C72.typed(38) == "exit"
C73 = capture("73", ML)
LS, GS = C73.cmd.split("; ")
assert (LS, GS) == ("ls -la", "git status --short")
assert C73.line(7).split()[2] == "root" and C73.line(7).endswith(" Pipfile")
assert C73.line(20) == "?? Pipfile"
C74 = capture("74", ML)
assert C74.line(4).startswith("created 2025-02-18")
assert C74.line(6) == 'cmd ["-c","pipenv shell"]' and C74.line(7) == 'user ""'
assert '"PYTHON_VERSION=3.8.17"' in C74.line(5)
# the capture ran `docker image ls …; docker image inspect --format '…' …`: the inspect alone prints
# lines 4-7. Its --format string (123 characters) wraps INSIDE the single quotes, where a " \" would
# be literal: those breaks are GREY ↪ rows (the code panels' wrap mark), each at a space, never in a
# {{…}} field; the only " \" follows the closing quote. Joined, the rows are the captured command.
INSPECT = C74.cmd.split("; ", 1)[1]
INSPECT_ROWS = ["    docker image inspect --format 'created {{.Created}}{{println}}env",
                "      ↪ {{json .Config.Env}}{{println}}cmd",
                "      ↪ {{json .Config.Cmd}}{{println}}user \"{{.Config.User}}\"' \\",
                "    dlops/mega-pipeline-transcribe-audio"]
assert " ".join(r.strip().removesuffix(" \\").removeprefix("↪ ") for r in INSPECT_ROWS) == INSPECT
INSPECT_PT = 20          # 72 characters a row (22 pt: 65, too few for the rows above)
C76 = capture("76", ML)
IMPORT_ERR = "ImportError: cannot import name 'genai' from 'google'"
assert C76.line(25).startswith(IMPORT_ERR)

PONDER_Q = "A teammate has never built this image.\nThey type ./docker-shell.sh run.\nWhich Python do they get?"

# ------------------------------------------------------------------ layout
TOP = 2.78               # top of the pictures under the tracker (tracker bottom 2.92)
BAND_Y = 3.21            # the top band, right of the tracker
P_A = p_comp("transcribe_audio")


def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def flash_framed(frame, text, color: str = TURN, k: float = 1.1) -> list:
    """Flash a tag or a board with an opaque dark fill: its outline turns `color` and back, its
    text indicates (Indicate on the whole group would fill the frame with the colour). A list to
    splat into play(): an AnimationGroup would add Group(frame, text) to the scene on top of the
    tag, a second copy of the frame over its own text."""
    return [frame.animate(rate_func=there_and_back).set_stroke(color),
            Indicate(text, color=color, scale_factor=k)]


def code_row(panel, n: int):
    """The glyphs of file line n of a src_panel (first row when wrapped)."""
    return panel.code.code_lines[panel.rows_of(n)[0]]


def row_y(panel, n: int) -> float:
    return panel.bar(n).get_center()[1]


def _part(s: str, size: float, color: str, font: str | None = None) -> VGroup:
    """Text built after a "|" that is dropped again, so parts of a row share a baseline."""
    t = label("|" + s, size, color, **({"font": font} if font else {}))
    pipe = t.submobjects[0]
    g = VGroup(*t.submobjects[1:])
    g.ref_dy = pipe.get_center()[1] - g.get_center()[1]
    return g


def mixed(parts, size: float = CAPTION, color: str = S.GREY, buff: float = 0.12) -> VGroup:
    """One row of serif and mono parts on one baseline: parts = [str | ("mono", str[, colour]) |
    (str, colour) ...]; a part starting with ")" or "”" hugs the one before it."""
    mobs = VGroup()
    for p in parts:
        if isinstance(p, tuple) and p[0] == "mono":
            mobs.add(_part(p[1], size, p[2] if len(p) > 2 else color, MONO))
        elif isinstance(p, tuple):
            mobs.add(_part(p[0], size, p[1]))
        else:
            mobs.add(_part(p, size, color))
    mobs.arrange(RIGHT, buff=buff)
    texts = [p[1] if isinstance(p, tuple) and p[0] == "mono" else (p[0] if isinstance(p, tuple) else p)
             for p in parts]
    for k in range(1, len(mobs)):
        if texts[k][:1] in (")", "”", ",", ":") or texts[k - 1][-1:] in ("(", "“"):
            dx = mobs[k].get_left()[0] - mobs[k - 1].get_right()[0] - 0.04
            for m in mobs[k:]:
                m.shift(LEFT * dx)
    y = mobs[0].get_center()[1] + mobs[0].ref_dy
    for m in mobs[1:]:
        m.shift(UP * (y - m.get_center()[1] - m.ref_dy))
    return mobs


def fit_tag(t, line, s: str = "extra", color: str = S.GREY):
    """A tag beside terminal line `line` (its last row): 22 pt, or 20 pt when the row leaves too
    little room. Positioned, not added; None when even 20 pt doesn't fit."""
    row = line.rows[-1] if hasattr(line, "rows") else line
    end = row.glyphs.get_right()[0]
    for size in (TAG, CAPTION):
        tg = beside(_keep(tag(s, color, size=size)), t, line)
        if tg.get_left()[0] >= end + 0.1:
            return tg
    return None


def type_rows(scene, t, rows_text, type_time: float = 0.5):
    """Type a command folded by hand: the prompt alone on its row, then `rows_text` (the command's
    rows, indented as in type_cmd's 'under the prompt' layout; a ↪ in a row is drawn GREY, as in
    the code panels). Returns a VGroup with .rows."""
    from common import _drop_bare
    _drop_bare(scene, t)
    texts = [t.prompt] + list(rows_text)
    assert all(len(s) <= t.max_chars for s in texts[1:]), rows_text
    t._make_room(scene, len(texts))
    rows = []
    for k, s in enumerate(texts):
        t2c = t._prompt_colors(t.prompt) if k == 0 else ({"↪": S.GREY} if "↪" in s else None)
        ln = mono_line(s, t.size, INK, t2c=t2c)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        rows.append(ln)
    scene.add(rows[0])
    typed = VGroup(*[g for r in rows[1:] for g in glyph_range(r, 0)])
    scene.play(ShowIncreasingSubsets(typed, rate_func=linear), run_time=type_time)
    for r in rows:
        scene.add(r)
    g = VGroup(*rows)
    g.rows, g.text = rows, " ".join(r.text.strip() for r in rows)
    return g


def type_under(scene, t, cmd: str, type_time: float = 0.5):
    """Type `cmd` on the row under the prompt, indented 4 (the house layout for long prompts), even
    when it would fit after it: the row keeps room for its tag. Returns a VGroup with .rows."""
    return type_rows(scene, t, ["    " + cmd], type_time=type_time)


def pin_extra(scene, tr, line, tg, run_time: float = 0.3):
    """Show a positioned GREY extra tag `tg` and pin it to terminal line `line` (its last row when
    folded) while the tracker caption gains ' · extra' (no change when it has it)."""
    scene.play(FadeIn(tg, shift=LEFT * 0.1), caption_extra(tr, True), run_time=run_time)
    row = line.rows[-1] if hasattr(line, "rows") else line
    scene.remove(tg)
    row.add(tg)
    scene.add(row)
    return tg


def type_extra(scene, t, cmd: str, type_time: float = 0.5, under_prompt: bool = False):
    """Type an extra command and pin its GREY `extra` tag beside it."""
    ln = (type_under if under_prompt else type_cmd)(scene, t, cmd, type_time=type_time)
    tg = fit_tag(t, ln)
    assert tg is not None, cmd
    pin(scene, ln, tg, run_time=0.25)
    return ln


def glyph_box(line, sub: str, color: str = TURN, pad: float = 0.06):
    """A box around the glyphs of `sub` in a mono line, as tall as the row (not added)."""
    g = substring(line, sub)
    r = box(g.width + 2 * pad + 0.04, line.strut.height + 0.06, color, fill_opacity=0.0, radius=0.06,
            stroke=3)
    return r.move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def slim_times(t, rows):
    """Build rows' time tags one row high (stacked tags of consecutive rows would overlap)."""
    for r in rows:
        tg = getattr(r, "time_tag", None)
        if tg is not None:
            tg.box.stretch_to_fit_height(t.pitch - 0.05)


def faded(m, k: float):
    """A copy of m with every fill and stroke opacity multiplied by k (dims a set-piece member
    without filling it in)."""
    c = m.copy()
    for f in c.get_family():
        if isinstance(f, VMobject):
            f.set_fill(opacity=f.get_fill_opacity() * k, family=False)
            f.set_stroke(opacity=f.get_stroke_opacity() * k, family=False)
    return c


def wipe(t):
    """(animation, cleanup): fade out every line of a terminal; cleanup() forgets them."""
    lines = list(t.lines.submobjects)

    def cleanup():
        for m in lines:
            t.lines.remove(m)
    return FadeOut(VGroup(*lines)), cleanup


def cd_into(scene, t, new_prompt: str, part: str, color: str = CLOUD):
    """After a `cd`: a bare prompt in the new folder, its folder part flashing."""
    t.set_prompt(new_prompt)
    ln = bare_prompt(scene, t)
    i = new_prompt.rindex(part)
    scene.play(Indicate(glyph_range(ln, i, i + len(part)), color=color, scale_factor=1.12), run_time=0.7)
    return ln


def stale_colors(prompt: str) -> dict:
    """Prompt colours for the dlops image's pipenv shell: (app) GREEN, root RED, @host GREEN, path
    BLUE (a Terminal._prompt_colors stand-in for this beat)."""
    a = prompt.index("root")
    c = prompt.index(":")
    d = len(prompt.rstrip("$# "))
    return {f"[0:{a - 1}]": S.GREEN, f"[{a}:{a + 4}]": ERR, f"[{a + 4}:{c}]": PROMPT_USER,
            f"[{c + 1}:{d}]": PROMPT_PATH}


def compact_switchboard(k: float = 0.5) -> Switchboard:
    """V4 at half size: tracks and dots shrink, each station shows its mode word and what it does
    on one row (the line chips and "first word" stay out)."""
    sw = Switchboard(labels=False)
    sw.remove(sw.parts["chips"], sw.parts["input_label"])
    sw.rescale(k)
    for m in MODES:
        st = sw.stations[m]
        st.dot.scale(1.5)
        st.word.next_to(st.dot, RIGHT, buff=0.12).set_y(st.dot.get_center()[1] + 0.02)
        st.desc.next_to(st.word, RIGHT, buff=0.2).align_to(st.word, DOWN)
    return sw


def bounds(*mobs) -> VGroup:
    return VGroup(*mobs)


def place(m, left=None, right=None, top=None, bottom=None, cx=None, cy=None, ref=None):
    """Move m so that its (or ref's) edges land where given."""
    r = ref if ref is not None else m
    dx = dy = 0.0
    if left is not None:
        dx = left - r.get_left()[0]
    if right is not None:
        dx = right - r.get_right()[0]
    if cx is not None:
        dx = cx - r.get_center()[0]
    if top is not None:
        dy = top - r.get_top()[1]
    if bottom is not None:
        dy = bottom - r.get_bottom()[1]
    if cy is not None:
        dy = cy - r.get_center()[1]
    m.shift(np.array([dx, dy, 0]))
    return m


def card_frame(rows, header: str | None, color: str = S.GREY) -> VGroup:
    """A GREY card around arranged rows, header above (README card look). .frame .rows .header"""
    fr = box(rows.width + 0.5, rows.height + 0.4, color, fill=S.BG, fill_opacity=0.92, radius=0.12)
    fr.move_to(rows)
    g = VGroup(fr, rows)
    g.frame, g.rows, g.header = fr, rows, None
    if header:
        h = _header_text(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        g.add(h)
        g.header = h
    return g


def package_picture() -> VGroup:
    """Beat 1: V5's two halves, readable. Left your laptop's transcribe_audio/ with pyproject.toml
    and uv.lock (GREEN); right the container's /app window with the same two files; the PINK window
    between; a TEAL image slab under the container (hidden). .lfiles .rfiles .route .app .slab
    .slab_label"""
    lf = box(4.1, 2.3, LAPTOP, fill_opacity=0.04).move_to([-4.3, 1.25, 0])
    lt = sans("your laptop", CAPTION, LAPTOP).move_to(lf.get_corner(UP + LEFT) + np.array([0.2, -0.27, 0]),
                                                       aligned_edge=LEFT)
    folder = file_row("transcribe_audio/", INK, LAPTOP)
    folder.move_to(lf.get_corner(UP + LEFT) + np.array([0.3, -0.85, 0]), aligned_edge=LEFT)
    lfiles = VGroup(file_row("pyproject.toml", INK, VENV), file_row("uv.lock", INK, VENV))
    lfiles.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    lfiles.next_to(folder, DOWN, buff=0.2, aligned_edge=LEFT).shift(RIGHT * 0.45)
    cf = box(6.9, 2.3, CTR, fill_opacity=0.05).move_to([2.9, 1.25, 0])
    ct = sans("container", CAPTION, CTR).move_to(cf.get_corner(UP + LEFT) + np.array([0.2, -0.27, 0]),
                                                 aligned_edge=LEFT)
    app = box(3.6, 1.45, CTR, fill_opacity=0.08, radius=0.08)
    app.move_to([cf.get_left()[0] + 0.25 + 1.8, cf.get_center()[1] - 0.22, 0])
    app_l = mono("/app", CAPTION, INK).move_to(app.get_corner(UP + LEFT) + np.array([0.15, -0.24, 0]),
                                               aligned_edge=LEFT)
    rfiles = lfiles.copy()
    rfiles.move_to(app.get_center() + np.array([0.2, -0.17, 0]))
    a = folder.get_right() + RIGHT * 0.15
    b = app.get_left() + LEFT * 0.06
    mx = (a[0] + b[0]) / 2
    route = VMobject(stroke_color=LOOKUP, stroke_width=5)
    route.set_points_as_corners([a, [mx, a[1], 0], [mx + 0.3, b[1], 0], b])
    slab = box(6.9, 0.5, CTR, fill_opacity=0.25, radius=0.06).next_to(cf, DOWN, buff=0.16)
    sl = sans("image", CAPTION, CTR).move_to(slab).align_to(slab, LEFT).shift(RIGHT * 0.2)
    g = VGroup(lf, lt, folder, lfiles, cf, ct, app, app_l, rfiles, route)
    g.lfiles, g.rfiles, g.route, g.app, g.slab, g.slab_label = lfiles, rfiles, route, app, slab, sl
    g.folder, g.cf = folder, cf
    return g


class DevAndRun(VoiceScene):
    def construct(self):
        tr = tracker("R", 2)

        # ========================================================== 0 · exit, cd back, dev only builds
        sw = compact_switchboard()
        sw.parts_in("words", "descs")             # shown from the start (FadeIn(sw) brings them)
        place(sw, right=6.4, top=3.38)
        t = term(rows=10, component="synthesis_audio")
        note0 = VGroup(note("anything new in the folder"),
                       mixed(["(e.g.", ("mono", "input_audios/"), "from", ("mono", "--download"), ")"]),
                       note("→ build steps 4–5 run again"))
        note0.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        place(note0, left=-6.3, cy=(2.9 + t.box.get_top()[1]) / 2)
        # SLIDES.md S08 (i): at "after any change" the switchboard has done its job (dev lit, "only
        # builds" flashed); the slide 7 tag and the lecture's order take the top right until beat 1
        lref7 = lecture_ref(4, "7")
        order7 = note("lecture's order: lock files first, code last")
        place(order7, right=6.6, cy=2.85)
        assert order7.get_top()[1] < lref7.get_bottom()[1] - 0.05, (order7.get_top()[1], lref7.get_bottom()[1])
        assert order7.get_bottom()[1] > t.box.get_top()[1] + 0.15, (order7.get_bottom()[1], t.box.get_top()[1])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(t), FadeIn(sw), run_time=0.7)
            session(self, t, C61, 95, 96, type_time=0.3, out_time=0.3)
            self.play(*leave_container(t, p_comp("synthesis_audio")), run_time=0.5)
            vo.wait_until("and cd back")
            type_cmd(self, t, CD_A, type_time=0.6)
            cd_into(self, t, P_A, "transcribe_audio")
            vo.wait_until("Step 2 of How to Run")
            self.play(flash(tr.caption, TURN, 1.08), run_time=0.6)
            vo.wait_until("docker-shell.sh dev")
            self.play(sw.light("dev"), run_time=0.5)
            type_cmd(self, t, C17.cmd, type_time=0.6)
            rows = print_build(self, t, DEV_ROWS, run_time=0.9, lag=0.1)
            slim_times(t, rows)
            mode_box = glyph_box(rows[0], "Build Mode: dev")
            pin(self, rows[0], mode_box, run_time=0.5, anim=Create(mode_box))
            vo.wait_until("only builds")
            self.play(flash(sw.stations["dev"].desc, TURN, 1.15), run_time=0.7)
            vo.wait_until("no container starts")
            back = bare_prompt(self, t)
            noc = fit_tag(t, back, "no container")
            assert noc is not None
            pin(self, back, noc, run_time=0.4)
            vo.wait_until("Here, all was cached")
            cached = [substring(r, "CACHED") for r in rows[3:]]
            self.play(LaggedStart(*[c.animate.set_color(VENV) for c in cached], lag_ratio=0.25), run_time=0.9)
            u03 = under(substring(rows[2], "Building 0.3s"), TURN)
            pin(self, rows[2], u03, run_time=0.5, anim=Create(u03))
            vo.wait_until("after any change")
            # the switchboard goes first, then the tag and note come in (no crossfade over its words)
            self.play(FadeIn(note0[0], shift=DOWN * 0.1), FadeIn(note0[1], shift=DOWN * 0.1),
                      Succession(FadeOut(sw), AnimationGroup(FadeIn(lref7, shift=DOWN * 0.1),
                                                             FadeIn(order7, shift=DOWN * 0.1))), run_time=0.8)
            vo.wait_until("the copy and uv sync")
            badges = []
            for r, k in ((rows[5], 4), (rows[6], 5)):
                b = build_badge(k, words=False).move_to([t.box.get_left()[0] + 0.24, r.strut.get_center()[1], 0])
                badges.append((r, b))
            self.play(*[FadeIn(b, scale=1.3) for _, b in badges], FadeIn(note0[2], shift=DOWN * 0.1),
                      run_time=0.6)
            for r, b in badges:
                self.remove(b)
                r.add(b)
                self.add(r)

        # ========================================================== 1 · uv add inside, dev bakes it in
        pic = package_picture()
        chip89 = readme_chip("transcribe_audio/README.md · line 89", "inside the container")
        y_tr = tracker("Y", 1)
        place(chip89, left=y_tr.get_right()[0] + 0.3, cy=BAND_Y)
        chip89b = readme_chip("transcribe_audio/README.md · line 89", "baked into the image")
        place(chip89b, left=chip89.get_left()[0], cy=BAND_Y)
        pkg = chip("<package>", VENV, size=CAPTION, font=MONO, fill_opacity=0.2)
        pkg.move_to([(pic.app.get_right()[0] + pic.cf.get_right()[0]) / 2, pic.rfiles[0].get_center()[1], 0])
        baked = note("baked in", VENV)
        # SLIDES.md S08 (i): slides 37-38 in the gap between the picture's slab and the strip (chip89
        # holds the band), from "Adding a package" to beat 2's first play
        lref37 = lecture_ref(4, "37–38")
        place(lref37, right=6.35, cy=-1.0)
        assert lref37.get_top()[1] < pic.slab.get_bottom()[1] - 0.15, (lref37.get_top()[1], pic.slab.get_bottom()[1])
        assert lref37.get_bottom()[1] > STRIP_TOP + 0.15, (lref37.get_bottom()[1], STRIP_TOP)
        with self.voiceover(SAY[1]) as vo:
            # the lines go while the frame turns TEAL, then it shrinks straight to the strip (no
            # empty 10-row terminal on screen)
            out0, done0 = wipe(t)
            self.play(out0, FadeOut(note0), FadeOut(lref7), FadeOut(order7), FadeOut(tr, shift=UP * 0.25),
                      FadeIn(y_tr, shift=DOWN * 0.25), *enter_container(t, "transcribe_audio"), run_time=0.6)
            done0()
            tr = y_tr
            resize(self, t, 3, run_time=0.6, extra=[FadeIn(chip89, shift=DOWN * 0.1)])
            vo.wait_until("Adding a package")
            self.play(FadeIn(pic), FadeIn(lref37, shift=DOWN * 0.1), run_time=0.7)
            vo.wait_until("uv add")
            ua = type_cmd(self, t, UV_ADD, type_time=0.5)
            ph = fit_tag(t, ua, "placeholder · lecture 3 ran it")
            pin(self, ua, ph, run_time=0.4)
            vo.wait_until("inside the container")
            self.play(flash(pic.app, CTR, 1.04), run_time=0.6)
            vo.wait_until("updates pyproject.toml")
            self.play(flash(pic.lfiles, TURN, 1.1), flash(pic.rfiles, TURN, 1.1),
                      Indicate(pic.route, color=TURN, scale_factor=1.0), run_time=0.9)
            vo.wait_until("through the window")
            self.play(flash(pic.lfiles, TURN, 1.1), flash(pic.rfiles, TURN, 1.1),
                      Indicate(pic.route, color=TURN, scale_factor=1.0), run_time=0.8)
            vo.wait_until("then dev bakes it")
            self.play(*leave_container(t, P_A), Transform(chip89, chip89b), FadeIn(pic.slab, shift=UP * 0.15),
                      FadeIn(pic.slab_label, shift=UP * 0.15), FadeIn(pkg, scale=0.8), run_time=0.5)
            type_cmd(self, t, C17.cmd, type_time=0.4)
            target = pic.slab.get_center() + RIGHT * 0.6
            baked.next_to(pic.slab, LEFT, buff=0.3)
            assert lref37.get_top()[1] < baked.get_bottom()[1] - 0.15 or lref37.get_left()[0] > baked.get_right()[0] + 0.15
            self.play(pkg.animate.move_to(target), FadeIn(baked, shift=LEFT * 0.1), run_time=0.7)
            self.play(flash(pic.slab, CTR, 1.04), run_time=0.5)
        self.wait(0.6)

        # ========================================================== 2 · run uses the local image; your turn
        r_tr = tracker("R", 3)
        place(sw, left=-6.35, top=TOP)
        rd = RunDecision()
        dia_full = rd.diamond[0].copy()
        run_st = sw.stations["run"]
        run_y = run_st.dot.get_center()[1]
        place(rd, right=6.4)
        rd.shift(UP * (run_y - rd.diamond[0].get_center()[1]))
        # "yes" under its arrow's middle, so it doesn't read on as "local image? yes"
        ya = rd.yes.arrow
        u = (ya.get_end() - ya.get_start()) / np.linalg.norm(ya.get_end() - ya.get_start())
        rd.yes.word.move_to(ya.get_center() + 0.3 * np.array([u[1], -u[0], 0]))
        link = Line(run_st.desc.get_right() + RIGHT * 0.15, rd.diamond[0].get_left() + LEFT * 0.04,
                    color=TOOL, stroke_width=5)
        link.set_y(run_y)
        card2 = turn_card([C17.cmd, C18.cmd])
        with self.voiceover(SAY[2]) as vo:
            out1, done1 = wipe(t)
            self.play(out1, FadeOut(VGroup(pic, pic.slab, pic.slab_label, pkg, baked, chip89)), FadeOut(lref37),
                      FadeOut(tr, shift=UP * 0.25), FadeIn(r_tr, shift=DOWN * 0.25), FadeIn(sw), run_time=0.6)
            done1()
            tr = r_tr
            resize(self, t, 8, run_time=0.6, extra=[sw.unlight("dev"), sw.light("run"), Create(link),
                                                    FadeIn(rd, shift=LEFT * 0.2)])
            rcmd = type_cmd(self, t, C18.cmd, type_time=0.5)
            outs = session(self, t, C18, (2, 4), out_time=0.4)
            vo.wait_until("using local image")
            ub = glyph_box(outs[4], "Using local image...")
            pin(self, outs[4], ub, run_time=0.4, anim=Create(ub))
            vo.wait_until("because one exists")
            self.play(rd.take("yes"), run_time=0.8)
            self.play(*enter_container(t, "transcribe_audio", P_RUN_LOCAL), run_time=0.3)
            session(self, t, C18, 5, 6, type_time=0.3, out_time=0.25)
            self.play(*leave_container(t, P_A), run_time=0.3)
            bare_prompt(self, t)
            vo.wait_until("Pause and try")
            resize(self, t, 3, keep=[*rcmd.rows, outs[4]], run_time=0.5)
            place(card2, left=-6.3, bottom=STRIP_TOP + 0.2)
            self.play(FadeIn(card2, shift=UP * 0.15), run_time=0.5)
        self.wait(2.0)                             # the your-turn card stays up to be read / paused on

        # ========================================================== 3 · erratum: run prefers ANY local image
        rows74 = mixed(["“", ("mono", "run", INK), ("to pull and run from the registry”", INK)], CAPTION, INK)
        card74 = card_frame(rows74, "README.md · line 74")
        place(card74, left=-6.3, top=TOP)
        err = erratum_tag().next_to(card74.frame, RIGHT, buff=0.3)
        u74 = under(VGroup(*rows74[2][:-1]), TURN)
        p3 = src_panel(SH, 82, 89, size=20)
        # the panel's background reaches 0.45 further right, so the "no: Docker Hub" tag on line 88
        # sits inside it (the bars follow the background's width)
        p3.code.background.stretch_to_fit_width(p3.code.background.width + 0.45, about_edge=LEFT)
        place(p3, left=-6.3, top=card74.frame.get_bottom()[1] - 0.25)
        bar83, bar85, bar88 = p3.bar(83, LOOKUP, 0.22), p3.bar(85, TURN, 0.2), p3.bar(88, CLOUD, 0.22)
        dia = rd.diamond[0]
        dia_t = dia.copy().scale(0.62)
        dia_t.move_to([p3.get_right()[0] + 0.55, row_y(p3, 83), 0])
        t85 = grey_tag("yes: local, however old")
        t85.next_to(code_row(p3, 85), RIGHT, buff=0.35).set_y(row_y(p3, 85))
        t88 = _keep(tag("no: Docker Hub", CLOUD))
        t88.next_to(code_row(p3, 88), RIGHT, buff=0.3).set_y(row_y(p3, 88))
        assert t88.get_right()[0] <= p3.code.get_right()[0] - 0.08, (t88.get_right(), p3.code.get_right())
        n89 = note("pulled only if missing · after that, the copy you have")
        place(n89, left=-6.1, top=p3.get_bottom()[1] - 0.2)
        c214 = readme_chip("README.md · line 214", "falls back to DockerHub")
        place(c214, left=-6.3, top=n89.get_bottom()[1] - 0.25)
        tick214 = check_mark(0.32, VENV).next_to(c214, RIGHT, buff=0.25)
        with self.voiceover(SAY[3]) as vo:
            self.remove(dia)
            rd.diamond.remove(dia)
            dia.set_z_index(5)
            self.add(dia)
            self.play(FadeOut(VGroup(sw, rd, link)), FadeOut(t), FadeOut(card2), run_time=0.5)
            self.play(FadeIn(card74, shift=DOWN * 0.1), FadeIn(err, shift=LEFT * 0.1),
                      dia.animate.scale(0.62).move_to([4.9, 2.2, 0]), run_time=0.6)
            vo.wait_until("the README's overview")
            self.play(Create(u74), run_time=0.6)
            vo.wait_until("In fact")
            self.play(FadeIn(p3, shift=UP * 0.1), run_time=0.6)
            self.play(FadeIn(bar83), dia.animate.move_to(dia_t), run_time=0.6)
            vo.wait_until("any local image")
            self.play(FadeIn(bar85), FadeIn(t85, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("however old")
            self.play(*flash_framed(t85.box, t85.text, TURN, 1.08), run_time=0.6)
            vo.wait_until("otherwise it runs")
            self.play(FadeIn(bar88), FadeIn(t88, shift=LEFT * 0.1), run_time=0.5)
            self.play(FadeIn(c214, shift=UP * 0.1), run_time=0.4)      # the README's step list is right
            self.play(Create(tick214), run_time=0.4)
            vo.wait_until("pulled only the first time")
            self.play(FadeIn(n89, shift=UP * 0.1), run_time=0.5)
        self.wait(1.0)

        # ========================================================== 4 · V1 + the diamond; ponder
        v1 = BuildOrPull(show=("git", "card", "local", "hub", "hub_tag", "box", "post", "pointer"))
        hub_tag = v1.parts["hub_tag"]
        v1.shift(UP * (TOP - v1.post.board.get_top()[1]))
        place(hub_tag, right=6.4, cy=BAND_Y)          # the band is free from here on
        img_full = v1.image.copy()
        card_full = v1.card.copy()
        lbl_full = v1.image_label.copy()
        # the diamond between: yes -> your laptop, no -> the signpost (the tag)
        scr = v1.laptop.screen
        d_c = np.array([scr.get_center()[0] - 0.1, scr.get_top()[1] + 0.95, 0])
        dia4 = dia_full.copy().move_to(d_c)
        dia4.set_fill(LOOKUP, 0.12)
        d_lab = sans("local image?", CAPTION, LOOKUP).next_to(dia4, LEFT, buff=0.25)
        yes_a = Arrow(dia4.get_bottom(), [d_c[0], scr.get_top()[1] + 0.02, 0], buff=0.02, color=LOOKUP,
                      stroke_width=4, max_tip_length_to_length_ratio=0.45)
        yes_l = sans("yes", CAPTION, LOOKUP).next_to(yes_a, RIGHT, buff=0.1)
        no_a = Arrow(dia4.get_right(), [v1.post.board.get_left()[0] - 0.02, d_c[1], 0], buff=0.03, color=LOOKUP,
                     stroke_width=4, max_tip_length_to_length_ratio=0.2)
        no_l = sans("no", CAPTION, LOOKUP).next_to(no_a, UP, buff=0.06)
        wiring = VGroup(d_lab, yes_a, yes_l, no_a, no_l)
        mate = v1.teammates(1)[0]
        mate.scale(1.5)
        never = note("never built it")
        mate_g = VGroup(mate, never)
        never.next_to(mate, DOWN, buff=0.18)
        place(mate_g, cx=-4.6, cy=-1.9)
        q = ponder_card(PONDER_Q, width=8.6, size=22)
        place(q, right=6.4, bottom=-3.45)
        assert q.get_top()[1] < v1.get_bottom()[1] - 0.1, (q.get_top()[1], v1.get_bottom()[1])
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(VGroup(card74, err, u74, p3, bar83, bar85, bar88, t85, t88, n89, c214, tick214)),
                      run_time=0.5)
            self.play(FadeIn(v1), dia.animate.move_to(dia4).set_fill(LOOKUP, 0.12), run_time=0.8)
            self.remove(dia)
            self.add(dia4)
            self.play(FadeIn(d_lab), GrowArrow(yes_a), FadeIn(yes_l), GrowArrow(no_a), FadeIn(no_l), run_time=0.7)
            vo.wait_until("A teammate")
            self.play(FadeIn(mate, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("never built")
            self.play(FadeIn(never), flash(mate[1], TURN, 1.15), run_time=0.7)
            vo.wait_until("and types")
            self.play(flash(dia4, TURN, 1.15), run_time=0.7)
            vo.wait_until("Which Python")
            self.play(flash(yes_a, TURN, 1.1), flash(no_a, TURN, 1.1), run_time=0.8)
        self.play(FadeIn(q, scale=0.95), run_time=0.6)
        bar = q[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 5 · delete the local image: we are the teammate
        t = term(P_A, rows=5)
        gone = note("now we are that teammate").move_to(v1.image_label)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(q), FadeOut(mate_g), run_time=0.4)
            self.play(caption_extra(tr, True), FadeIn(t, shift=UP * 0.15), run_time=0.5)
            type_extra(self, t, C71.cmd, type_time=0.8)
            t.print(self, C71.at(2, 3), run_time=0.4)
            vo.wait_until("so we become")
            self.play(v1.image.animate.set_opacity(0).scale(0.6), v1.image_label.animate.set_opacity(0),
                      run_time=0.8)
            self.play(FadeIn(gone, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 6 · run: no local image -> the dlops image
        copy = v1.box.copy()
        copy_t = sealed_box(0.85, CTR).move_to(img_full)
        pull = Arrow(v1.box.front.get_left() + LEFT * 0.1, [scr.get_right()[0] + 0.12, v1.box.front.get_center()[1], 0],
                     buff=0, color=HUB, stroke_width=5, max_tip_length_to_length_ratio=0.08)
        pull.set_z_index(2)
        # between the blocks: the command runs, so its first lines are there when the SAY reads them
        self.play(caption_extra(tr, False), run_time=0.3)
        type_cmd(self, t, C72.cmd, type_time=0.5)
        o6 = t.print(self, C72.at(2, 3, 4), run_time=0.4)
        nf = o6[2]
        with self.voiceover(SAY[6]) as vo:
            self.play(nf.animate.set_color(TURN), run_time=0.4)
            self.play(flash(dia4, TURN, 1.15), no_a.animate.set_color(TURN), no_l.animate.set_color(TURN),
                      run_time=0.7)
            vo.wait_until("so it pulls")
            t.print(self, C72.at(5, 6), run_time=0.4)
            self.play(GrowArrow(pull), FadeOut(gone), run_time=0.6)
            t.print(self, C72.at("…", 18, 19), run_time=0.5)
            self.add(copy)
            self.play(Transform(copy, copy_t), run_time=0.8)
            self.play(FadeOut(pull), run_time=0.3)
            vo.wait_until("Then, a surprise")
            o20 = t.print(self, C72.at(20, 21), run_time=0.4)
            pf = glyph_box(o20[0], "Creating a Pipfile")
            pin(self, o20[0], pf, run_time=0.4, anim=Create(pf))
            vo.wait_until("That's pipenv")
            pv = fit_tag(t, o20[0], "pipenv: the course's tool before uv")
            assert pv is not None
            pin(self, o20[0], pv, run_time=0.4)

        # ========================================================== 7 · inside: root, Python 3.8.17, pipenv
        comp = VGroup(dia4, wiring, copy)
        out6, done6 = wipe(t)                      # between the blocks: the picture makes way
        self.play(out6, FadeOut(v1), FadeOut(comp), *enter_container(t, "transcribe_audio", P_STALE),
                  run_time=0.5)
        done6()
        resize(self, t, 10, run_time=0.5)
        t._prompt_colors = stale_colors
        pr = bare_prompt(self, t)
        rt = _keep(tag("root", ERR))
        # at column 48, clear of the first command (line 24 is 46 characters), so the tag can stay
        # on that row when the typed line replaces the bare prompt
        rt.move_to([pr.strut.get_left()[0] + 48 * cell_width(t.size), pr.strut.get_center()[1], 0],
                   aligned_edge=LEFT)
        with self.voiceover(SAY[7]) as vo:
            pin(self, pr, rt, run_time=0.4)
            self.play(flash(substring(pr, "root"), ERR, 1.25), run_time=0.7)
            vo.wait_until("Python is 3.8.17")
            pr.remove(rt)
            self.add(rt)
            o24 = session(self, t, C72, 24, type_time=0.5)[24]
            self.remove(rt)
            o24.add(rt)
            self.add(o24)
            # python --version and which python are extras (not in the README): GREY tags, the
            # RED root tag stays on the prompt's row before them
            pin_extra(self, tr, o24, extra_tag().next_to(rt, RIGHT, buff=0.15))
            o25 = session(self, t, C72, 25, out_time=0.3)[25]
            pyb = glyph_box(o25, "Python 3.8.17")
            pin(self, o25, pyb, run_time=0.4, anim=Create(pyb))
            vo.wait_until("in an environment")
            o26 = session(self, t, C72, 26, type_time=0.4)[26]
            x26 = fit_tag(t, o26)
            assert x26 is not None
            pin_extra(self, tr, o26, x26, run_time=0.25)
            o27 = session(self, t, C72, 27, out_time=0.3)[27]
            uvenv = under(substring(o27, "/root/.local/share/virtualenvs/app-4PlAip0Q"), TURN)
            pin(self, o27, uvenv, run_time=0.4, anim=Create(uvenv))
            vo.wait_until("Help still works")
            self.play(caption_extra(tr, False), run_time=0.25)     # python cli.py --help: README line 98
            o7 = session(self, t, C72, 28, 29, "…", 33, type_time=0.45, out_time=0.5)
            vo.wait_until("in the older wording")
            oa = fit_tag(t, o7[33], "Python 3.8's argparse wording")
            pin(self, o7[33], oa, run_time=0.4)
            vo.wait_until("Then type exit")
            session(self, t, C72, 38, 39, type_time=0.3, out_time=0.3)
            del t._prompt_colors

        # ========================================================== 8 · the box opens: what's inside
        # between the blocks: the container is gone; back on the laptop, the extra inspect is typed
        # as captured (20 pt, so its --format string folds at spaces into whole {{…}} fields)
        out7, done7 = wipe(t)
        self.play(out7, *leave_container(t, P_A), caption_extra(tr, True), run_time=0.5)
        done7()
        t.size, t.pitch = INSPECT_PT, line_pitch(INSPECT_PT)
        t.max_chars = int((t.box.width - 0.6) / cell_width(INSPECT_PT))
        resize(self, t, 10, run_time=0.4)
        insp = type_rows(self, t, INSPECT_ROWS, type_time=1.6)
        x74 = beside(_keep(tag("extra", S.GREY, size=CAPTION)), t, insp)    # 20 pt: the rows' height
        one = note("one command, folded to fit · type it as one line")
        place(one, left=t.box.get_left()[0] + 0.15, bottom=t.box.get_top()[1] + 0.15)
        self.play(FadeIn(x74, shift=LEFT * 0.1), FadeIn(one, shift=UP * 0.1), run_time=0.4)
        self.remove(x74)
        insp.rows[-1].add(x74)
        self.add(insp.rows[-1])
        t.print(self, C74.at(4, 5, 6, 7), run_time=0.5)          # line 5 (env, 533 characters) cut with …
        bare_prompt(self, t)
        self.wait(1.2)

        lp = log_panel(C74.at(4, 6, 7), "docker image inspect --format … dlops/mega-pipeline-transcribe-audio · extra",
                       width=6.9)
        place(lp, left=-6.3, top=-0.62)
        env = excerpt_chip("PYTHON_VERSION=3.8.17", "docker image inspect · env (excerpt)", line=C74.line(5))
        place(env, right=6.3, cy=lp.frame.get_center()[1] + 0.1)
        assert lp.header.get_bottom()[1] > env.get_top()[1] + 0.1, (lp.header.get_bottom(), env.get_top())
        root8 = note("= root", ERR).next_to(lp.rows[2].glyphs, RIGHT, buff=0.25)   # plain text: no pill to touch the underline above
        labels, oanims = v1.open_box([("2025-02-18", INK), ("Python 3.8.17", TURN), ("pipenv shell", INK),
                                      ("user: root", ERR)])
        tape, rise = oanims[1], oanims[2].animations
        # the lid opens and the stale dlops image turns RED (BRIEF colour table: avoid this); built
        # after open_box, whose own lid animation (oanims[0]) would keep it TEAL
        bx = v1.box
        lid = bx.lid.animate.rotate(-PI * 0.55, about_point=bx.front.get_corner(UP + RIGHT)).set_color(ERR)
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(t), FadeOut(one), run_time=0.4)
            self.play(FadeIn(v1), FadeIn(copy), run_time=0.6)
            self.play(FadeIn(lp, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("opens the box")
            self.play(lid, tape, bx.front.animate.set_color(ERR), bx.side.animate.set_color(ERR),
                      copy.animate.set_color(ERR), run_time=0.7)
            vo.wait_until("created on")
            d8 = under(substring(lp.rows[0], "2025-02-18"), TURN)
            self.play(Create(d8), rise[0], run_time=0.8)
            vo.wait_until("with Python")
            self.play(FadeIn(env, shift=LEFT * 0.1), rise[1], run_time=0.8)
            vo.wait_until("starting pipenv shell")
            p8 = under(substring(lp.rows[1], "pipenv shell"), TURN)
            self.play(Create(p8), rise[2], run_time=0.8)
            vo.wait_until("as root")
            self.play(FadeIn(root8, shift=LEFT * 0.1), rise[3], run_time=0.8)
        self.wait(0.8)                             # the panel's "= root" stays readable a moment

        # ========================================================== 9 · an older branch's recipe; puzzle 1
        p9 = src_panel(OLD_DF, 2, 2)
        h9 = VGroup(label("pipenv-flexible-workflow ·", CAPTION, S.GREY),
                    _header_text("transcribe_audio/Dockerfile · line 2")).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        h9.next_to(p9.code, UP, buff=0.1).align_to(p9.code, LEFT).shift(RIGHT * 0.12)
        p9.remove(p9.header)
        p9.header = h9
        p9.add(h9)
        old = v1.old_card()
        place(old, right=6.35, top=-0.6)
        place(p9, left=-6.3, top=-0.75)
        link9 = BuildOrPull.dashed_link(v1.box, old.card, text=None)
        # inset in the box's front: the stale image's RED outline stays visible around your folder
        sheet = Rectangle(width=v1.box.front.width - 0.16, height=v1.box.front.height - 0.16)
        sheet.set_stroke(LAPTOP, 2).set_fill(LAPTOP, 0.55).move_to(copy_t)
        sheet.set_z_index(3)
        yours = note("your code, their environment", INK)
        place(yours, cx=scr.get_center()[0] - 0.4, top=-0.62)
        ie = excerpt_chip(IMPORT_ERR, "generate_text · ./docker-shell.sh run (excerpt)", ERR, frame=ERR,
                          line=C76.line(25))
        place(ie, right=6.35, bottom=-3.4)
        puzzle = VGroup(check_mark(0.3, TURN), label("puzzle 1", CAPTION, TURN)).arrange(RIGHT, buff=0.12)
        place(puzzle, right=6.3, cy=ie.header.get_center()[1])
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(VGroup(lp, env, root8, d8, p8)), caption_extra(tr, False), run_time=0.5)
            self.play(FadeIn(p9, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("an older branch")
            self.play(FadeIn(old, shift=UP * 0.15), run_time=0.6)
            self.play(Create(link9), Transform(v1.card, faded(v1.card, 0.4)), run_time=0.8)
            vo.wait_until("not your recipe")
            self.play(flash(old.card, TURN, 1.06), run_time=0.6)
            vo.wait_until("Your folder slides")
            self.play(FadeOut(p9), run_time=0.3)
            labels.set_z_index(5)                  # the sheet slides behind the box's labels
            self.add(sheet)
            self.play(sheet.animate.move_to(v1.box.front), run_time=1.2)
            vo.wait_until("your code, their environment")
            self.play(FadeIn(yours, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("For generate text")
            self.play(FadeIn(ie, shift=LEFT * 0.4), run_time=0.7)
            vo.wait_until("the first puzzle")
            self.play(Create(puzzle[0]), FadeIn(puzzle[1]), run_time=0.6)

        # ========================================================== 10 · a Pipfile owned by root
        pip = VGroup(file_row("Pipfile", INK, S.GREY), _keep(tag("root", ERR, size=CAPTION)))
        pip.arrange(RIGHT, buff=0.12)
        pip_end = pip.copy().move_to([scr.get_center()[0], v1.image_label.get_center()[1] - 0.05, 0])
        # the Pipfile appears under the box, below the shelf's caption (clear of the labels left of
        # the box and of the caption), slides left and rises into your laptop's folder
        y_low = v1.hub_shelf.caption.get_bottom()[1] - 0.24 - pip.height / 2
        pip_low = pip.copy().move_to([v1.box.get_center()[0], y_low, 0])
        pip_low.shift(LEFT * max(0.0, pip_low.get_right()[0] - 6.35))     # inside the safe frame
        pip_path = VMobject().set_points_as_corners([pip_low.get_center(), [pip_end.get_center()[0], y_low, 0],
                                                     pip_end.get_center()])
        pip.move_to(v1.box.front)
        pip.set_z_index(4)                         # above the GREY sheet it starts on
        rm_row = VGroup(cmd_chip("rm Pipfile"), extra_tag()).arrange(RIGHT, buff=0.2)
        # the Pipfile is root's (73 line 7): GNU rm asks before removing a write-protected file
        rm_note = note("Linux asks first (root's file) → y")
        rm_note.next_to(rm_row, DOWN, buff=0.06).align_to(rm_row, LEFT).shift(RIGHT * 0.1)
        rm_chip = VGroup(rm_row, rm_note)
        dev_chip = VGroup(cmd_chip(C17.cmd), note("your own image back")).arrange(RIGHT, buff=0.2)
        chips10 = VGroup(rm_chip, dev_chip).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        # top-aligned under V1's lowest visible parts (the shelves' captions, the landed Pipfile)
        v1_low = min(v1.git_shelf.caption.get_bottom()[1], v1.hub_shelf.caption.get_bottom()[1],
                     pip_end.get_bottom()[1])
        place(chips10, cx=0, top=v1_low - 0.12)
        assert chips10.get_bottom()[1] >= STRIP_TOP + 0.05, (chips10.get_bottom(), STRIP_TOP)
        # between the blocks: beat 9's extras leave and the second terminal opens (in ~ first)
        self.play(FadeOut(VGroup(old, link9, ie, puzzle, yours)), Transform(v1.card, card_full),
                  caption_extra(tr, True), run_time=0.5)
        t2 = second_terminal(self, P_A, rows=3, top=STRIP_TOP)
        with self.voiceover(SAY[10]) as vo:
            type_extra(self, t2, LS, type_time=0.3, under_prompt=True)
            # "…", line 7 (no trailing "…"): the 3-row strip then holds the command and its key line
            ls_rows = t2.print(self, ["…", C73.line(7)], run_time=0.4)
            vo.wait_until("in your folder")
            pip.move_to(pip_low)
            self.play(FadeIn(pip, shift=DOWN * 0.3), run_time=0.5)
            self.play(MoveAlongPath(pip, pip_path), run_time=1.0)
            vo.wait_until("owned by root")
            self.play(substring(ls_rows[1], "root").animate.set_color(ERR), flash(pip[1][1], ERR, 1.3),
                      run_time=0.6)
            vo.wait_until("If you tried this")
            type_extra(self, t2, GS, type_time=0.4)
            t2.print(self, ["…", C73.line(20)], run_time=0.3)
            vo.wait_until("delete it")
            self.play(FadeIn(rm_chip, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("and run dev")
            self.play(FadeIn(dev_chip, shift=UP * 0.1), run_time=0.4)
        self.wait(1.2)

        # ========================================================== 11 · the fix
        r1 = mixed([("build locally · no argument, or", VENV), ("mono", "dev", VENV)], CAPTION)
        r2 = mixed([("mono", "run", CLOUD), ("· only images your team pushed from this branch · your own", CLOUD),
                    ("mono", "DOCKER_USERNAME", CLOUD)], CAPTION)
        r3 = mixed(["their newer push?", ("mono", "docker pull <user>/<image>", S.GREY)], CAPTION, S.GREY)
        fix_rows = VGroup(r1, r2, r3).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        fix = card_frame(fix_rows, None)
        fix_h = note("the fix").next_to(fix.frame, UP, buff=0.08).align_to(fix.frame, LEFT).shift(RIGHT * 0.12)
        fix_g = VGroup(fix, fix_h)
        place(fix_g, cx=0, cy=(v1.get_bottom()[1] - 3.45) / 2)
        # the box closes and is a plain TEAL image again (the shelf for your team's pushes)
        lid_back = bx.lid.animate.rotate(PI * 0.55, about_point=bx.front.get_corner(UP + RIGHT)).set_color(CTR)
        with self.voiceover(SAY[11]) as vo:
            self.play(FadeOut(VGroup(t2, chips10, labels, sheet, pip)), caption_extra(tr, False), run_time=0.5)
            self.play(lid_back, bx.tape.animate.set_opacity(0.8), bx.front.animate.set_color(CTR),
                      bx.side.animate.set_color(CTR), run_time=0.6)
            self.play(FadeIn(fix.frame), FadeIn(fix_h), FadeIn(r1, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("with no argument")
            self.play(*v1.parts_in("build", anim=lambda m: FadeIn(m, shift=RIGHT * 0.25)), FadeOut(copy),
                      v1.image.animate.become(img_full), v1.image_label.animate.become(lbl_full), run_time=0.9)
            vo.wait_until("and use run only")
            self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.5)
            self.play(flash(v1.box, TURN, 1.08), *flash_framed(v1.post.board, v1.post.text, TURN, 1.04),
                      run_time=0.7)
            vo.wait_until("under your own")
            self.play(flash(r2[2], TURN, 1.1), run_time=0.7)
        self.play(FadeIn(r3, shift=UP * 0.1), run_time=0.5)
        self.wait(1.6)
        self.play(FadeOut(*self.mobjects), run_time=0.8)
        self.wait(0.3)
