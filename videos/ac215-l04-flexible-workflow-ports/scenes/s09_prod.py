"""S09 · prod, a stowaway key, and clean-up (README "How to Run a Component" step 4; transcribe_audio
README "Publish the container"; part 1 clean-up). End of part 1.

Beats (script.md "## S09", one voiceover block each):
 0  TRACKER R/4. V4 (compact, top right): the prod track lights. CODE(transcribe_audio/docker-shell.sh
    · lines 54-62, 13.1 wide, 21.4 pt): lines 55-57 (inspect, remove) get a YELLOW bar, then line
    62 (create); GREY caption "builder = a build engine that can target several processor types";
    `--use` turns PURPLE, a PURPLE tag under it "becomes the current builder · never switched
    back"; GREY "check with docker buildx ls" and a GREY command chip `docker buildx use default`
    "switch back afterwards".
 1  The panel swaps to CODE(… · lines 65-66 · line 66 wrapped): `--platform linux/amd64,linux/arm64`
    PURPLE, two TEAL boxes amd64 / arm64 appear; `--push` BLUE, the BLUE Docker Hub shelf
    (illustration) and the boxes land on it; the PINK signpost $DOCKER_USERNAME/$IMAGE_NAME with two
    arrows (one tag); GREY tag "lecture 2"; a GREY Apple-silicon Mac pulls arm64, a GREY cloud VM
    amd64 (BLUE pull arrows; the arch label flashes as it is pulled).
 2  TRACKER U/1, README chip transcribe_audio/README.md · line 129. 3-row strip (laptop):
    `docker login -u <USER NAME> -p <ACCESS TOKEN>` (command only, GREY "not run here"); `-p` ringed
    GOLD, a GOLD tag under it "the token stays in your shell history", GREY chip `--password-stdin`
    "avoids it" above the strip. CODE(docker-shell.sh · line 13) with `dlops` underlined + README
    chip README.md · line 76 "update DOCKER_USERNAME". TRACKER U/2 (GREY "= How to Run · step 4"):
    `./docker-shell.sh prod` (command only, GREY "not run here: needs a login · publishes an
    image"); YELLOW caption "first: check what it would publish".
 3  TRACKER R/2 · extra. The strip grows to 12 rows (laptop · lecture 3 clone, ~/AC215-l03/…/
    transcribe_audio, a bare prompt). Top right: a glyph-only V2 miniature, its GOLD key ringed;
    GREY "if you skipped the deletion in Get the Code". `./docker-shell.sh dev` (extra) ->
    mega-l03-laptop/12 lines 2, 4, 16, 24 (BuildKit rows): `[4/5] COPY --chown=app:app . ./` boxed
    YELLOW + GREY "not CACHED".
    `docker run --rm --entrypoint ls mega-pipeline-transcribe-audio -la /app /app/secrets`
    (extra; folds) -> 13 lines 2, …, 12, …, 15, 19: `mega-pipeline.json` RED, GREY tag "stand-in file
    · not a real key" above it.
 4  The terminal shrinks to the strip (the command's last row, /app/secrets:, line 19). V5 contrast
    above: lecture 3's laptop folder (~/AC215-l03/ … transcribe_audio/ secrets/ + GOLD key) and a
    TEAL image layer; CODE(transcribe_audio/Dockerfile · line 39) top right; COPY packs the folder,
    secrets/ and the key into the layer (copies: here the key really is copied). The GREY Git shelf
    (three GREEN tracked files on it) with the shield /secrets (transcribe_audio/.gitignore · line 3)
    in front of it, which flashes GREEN as a dashed GREY arrow from secrets/ stops at it; the key
    in the layer flashes RED ("not out of images");
    dashed GREY chip ".dockerignore: none, on every branch". The PURPLE prod track carries the
    layer to the BLUE Docker Hub shelf, which flashes RED.
 5  GREY tag erratum. README card README.md · line 203 (the canonical way … impossible, underlined)
    and GREY "for Git: yes ✓ · for images: no ✗". Fix card (rows write in as said): delete the
    secrets/ folder inside each component · add a .dockerignore listing secrets/ (lecture 3) · RED
    "a key was ever pushed? delete that key in IAM"; ▶ your turn on the card's header row, right.
 6  TRACKER R/4 · extra. Clean-up card for part 1, top right (rows write in as said). 7-row terminal
    (laptop, ~/AC215/mega-pipeline): `docker images` (extra) -> mega-laptop/70 lines 2-7, column
    view (IMAGE and DISK USAGE) with S16's GREY tag "2 of 5 columns" in the header row's gap (its
    end has no room): the transcribe row flashes, then 1.48GB is boxed YELLOW, the four ~830MB
    underlined.
 7  The terminal goes as the card moves down and grows: three GOLD rows (bucket in two cues, key +
    a tiny illustration of the console's key list beside that row, whose RED trash can flashes at
    "in the console", a pushed Docker Hub repo on two lines); card and console are centred
    together. Closing card "Part 2: containers that talk to each other directly" with two small
    TEAL boxes and a PINK arrow between them. Everything fades: an empty frame (end of part 1).

Deviations from SHOW (and why):
- Beats 0-1: V4 is the compact switchboard of S08 (mode word + what it does, half size) in the band
  right of the tracker: the 9-line panel takes the full width under it. Beat 1: the switchboard
  leaves while the shorter panel is up (the shelf, the signpost and the two machines need the
  height); the machines sit left and right of the shelf, not under it.
- Beat 0: the GREY fix chip is a command chip (GREY) with its note to its right.
- Beat 1: the "lecture 2" tag sits above the Mac (under the shelf there is no room left).
- Beat 2: the two README chips: line 129 in the band (no phrase: the line is the command itself),
  line 76 under the line-13 panel; "(and R/4)" is a GREY note beside the tracker's caption. The
  GOLD note is a GOLD tag in the strip's empty third row, right under `-p` (a line from `-p` to a
  note above the strip would cross the prompt row); the `--password-stdin` chip sits above the
  strip, right.
- Beat 3: the stand-in tag sits in the row above line 19, over the file name (line 19 has no room
  left for it); the miniature is the three piles only (glyph-only, its key enlarged so it reads).
- Beat 4: V5 is its laptop side (lecture 3's tree) and its image layer only: no container runs in
  a build. The image layer is shortened to 3.6 units. The Docker Hub shelf's illustration tag sits
  above it (under it the .gitignore header needs the room).
- Beat 6: the terminal has 7 rows (the column view is 7 rows), so the clean-up card fits above it
  in the band's right half (never beside the terminal); the card's header is its first row.
- Beat 7: the third GOLD row is two lines (one would be 10.8 units at 22 pt); its "·" becomes the
  line break.
- Timing: a few in-sentence anchors are shifted by hand with at() (PLAYBOOK §2.6), from a Kokoro
  synthesis of each sentence up to the phrase: beat 1's clauses after "amd64 and arm64" come
  0.35-0.8 s later than the character count says; elsewhere 0.3-0.6 s earlier.
"""

from common import *
from common import _header_text, _keep
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    Polygon,
    RoundedRectangle,
    Text,
    Transform,
    VGroup,
)

from explainer import style as S
from explainer.devops import laptop, server
from explainer.scene import VoiceScene

SAY = NARRATION["S09"]
assert len(SAY) == 8, len(SAY)

ML, L3 = "mega-laptop", "mega-l03-laptop"
SH = "mega-pipeline/transcribe_audio/docker-shell.sh"
DF = "mega-pipeline/transcribe_audio/Dockerfile"
GI = "mega-pipeline/transcribe_audio/.gitignore"
README = "mega-pipeline/README.md"
A_README = "mega-pipeline/transcribe_audio/README.md"

# ------------------------------------------------------------------ sources (checked)
assert excerpt(SH, 55, 55) == "    if docker buildx inspect multi-arch >/dev/null 2>&1; then"
assert excerpt(SH, 57, 57) == "        docker buildx rm multi-arch"
assert excerpt(SH, 62, 62) == "    docker buildx create --driver-opt network=host --use --name multi-arch"
L66 = excerpt(SH, 66, 66)
assert L66 == ("    docker buildx build --platform linux/amd64,linux/arm64 --push -t "
               "$DOCKER_USERNAME/$IMAGE_NAME -f Dockerfile .")
assert excerpt(SH, 13, 13) == 'DOCKER_USERNAME="dlops"'
assert excerpt(DF, 39, 39) == "COPY --chown=app:app . ./"
assert excerpt(GI, 3, 3) == "/secrets"
LOGIN = "docker login -u <USER NAME> -p <ACCESS TOKEN>"
assert excerpt(A_README, 129, 129) == LOGIN
L76 = excerpt(README, 76, 76)
assert "update `DOCKER_USERNAME`" in L76
L203 = excerpt(README, 203, 203)
Q203 = ("Never commit secrets/ to Git. Keeping the folder outside the repo",
        "(as this branch does) is the canonical way to make that mistake impossible.")
assert "Keeping the folder outside the repo (as this branch does) is the canonical way to make that " \
       "mistake impossible." in L203 and "**Never commit `secrets/` to Git.**" in L203
PROD = "./docker-shell.sh prod"
assert excerpt(README, 215, 215).startswith(PROD)

# ------------------------------------------------------------------ commands and real outputs
C12 = capture("12", L3)
assert C12.cmd == "./docker-shell.sh dev"
DEV_ROWS = C12.at(2, 4, 16, 24)
assert DEV_ROWS[0] == "Docker Username: dlops, Build Mode: dev"
assert DEV_ROWS[2].strip().startswith("=> [4/5] COPY --chown=app:app . ./")
assert "naming to docker.io/library/mega-pipeline-transcribe-audio:latest" in DEV_ROWS[3]
C13 = capture("13", L3)
assert C13.cmd == "docker run --rm --entrypoint ls mega-pipeline-transcribe-audio -la /app /app/secrets"
LS_ROWS = C13.at(2, "…", 12, "…", 15, 19)
assert LS_ROWS[0] == "/app:" and LS_ROWS[2].endswith(" secrets") and LS_ROWS[4] == "/app/secrets:"
assert LS_ROWS[5].endswith(" mega-pipeline.json")
C70 = capture("70", ML)
assert C70.cmd == "docker images"
IMG_ROWS = column_view(C70.at((2, 7)))
assert IMG_ROWS[0].startswith("IMAGE") and IMG_ROWS[0].endswith("DISK USAGE")
assert IMG_ROWS[4].startswith("mega-pipeline-transcribe-audio:latest") and IMG_ROWS[4].endswith("1.48GB")
SMALL_IMGS = {1: "821MB", 2: "833MB", 3: "833MB", 5: "836MB"}
for k, v in SMALL_IMGS.items():
    assert IMG_ROWS[k].endswith(v), IMG_ROWS[k]

# ------------------------------------------------------------------ layout
TOP = 2.78               # top of the pictures under the tracker (tracker bottom 2.92)
BAND_Y = 3.21            # the top band, right of the tracker
P_A = p_comp("transcribe_audio")
P_L3A = p_l03("transcribe_audio")


def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def at(scene, vo, phrase: str, dt: float = 0.0):
    """vo.wait_until(phrase), shifted by dt seconds. Inside a sentence an anchor is interpolated
    by character count; dt is a hand-set correction (PLAYBOOK §2.6) where a Kokoro synthesis of the
    sentence up to the phrase put it measurably earlier (dt < 0) or later ("amd64" is long)."""
    t = vo.clip.time_of(phrase)
    if t is None:
        vo.wait_until(phrase)                 # logs "voiceover anchor not found"
        return
    left = t + dt - vo.elapsed
    if left > 0.07:                           # (shorter waits round up to a frame anyway)
        scene.wait(left)


def stack(rows, pitch: float, head_gap: float = 0.0):
    """Arrange one-line mixed() rows top-down, left-aligned, on equal baselines (bounding boxes
    differ between serif-only and mono rows, so arrange() spaces them unevenly)."""
    def base(r):
        return r[0].get_center()[1] + r[0].ref_dy
    x0, y0 = rows[0].get_left()[0], base(rows[0])
    for k, r in enumerate(rows):
        y = y0 - k * pitch - (head_gap if k else 0.0)
        r.shift(np.array([x0 - r.get_left()[0], y - base(r), 0]))
    return rows


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


def _part(s: str, size: float, color: str, font: str | None = None) -> VGroup:
    """Text built after a "|" that is dropped again, so parts of a row share a baseline."""
    t = label("|" + s, size, color, **({"font": font} if font else {}))
    pipe = t.submobjects[0]
    g = VGroup(*t.submobjects[1:])
    g.ref_dy = pipe.get_center()[1] - g.get_center()[1]
    return g


def mixed(parts, size: float = CAPTION, color: str = S.GREY, buff: float = 0.12) -> VGroup:
    """One row of serif and mono parts on one baseline: parts = [str | ("mono", str[, colour]) |
    (str, colour) ...]."""
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
        if texts[k][:1] in (")", ",", ":") or texts[k - 1][-1:] in ("(",):
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


def type_tagged(scene, t, cmd: str, s: str = "extra", type_time: float = 0.5):
    """Type a command and pin a GREY tag (extra, not run here …) beside it."""
    ln = type_cmd(scene, t, cmd, type_time=type_time)
    tg = fit_tag(t, ln, s)
    assert tg is not None, (cmd, s)
    pin(scene, ln, tg, run_time=0.3)
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


def wipe(t):
    """(animation, cleanup): fade out every line of a terminal; cleanup() forgets them."""
    lines = list(t.lines.submobjects)

    def cleanup():
        for m in lines:
            t.lines.remove(m)
    return FadeOut(VGroup(*lines)), cleanup


def compact_switchboard(k: float = 0.5) -> Switchboard:
    """V4 at half size (as in S08): tracks and dots shrink, each station shows its mode word and
    what it does on one row (the line chips and "first word" stay out)."""
    sw = Switchboard(labels=False)
    sw.remove(sw.parts["chips"], sw.parts["input_label"])
    sw.rescale(k)
    for m in MODES:
        st = sw.stations[m]
        st.dot.scale(1.5)
        st.word.next_to(st.dot, RIGHT, buff=0.12).set_y(st.dot.get_center()[1] + 0.02)
        st.desc.next_to(st.word, RIGHT, buff=0.2).align_to(st.word, DOWN)
    return sw


def dashed_chip(parts) -> VGroup:
    """A dashed GREY chip around a mixed row (something that does not exist)."""
    row = mixed(parts, color=S.GREY)
    fr = box(row.width + 0.5, row.height + 0.3, S.GREY, fill_opacity=0.0, radius=0.12, dashed=True)
    fr.move_to(row)
    g = VGroup(fr, row)
    g.frame, g.row = fr, row
    return _keep(g)


def strip_text(m):
    """Remove every text from m (a glyph-only copy)."""
    for s in list(m.submobjects):
        if isinstance(s, Text) or hasattr(s, "pt"):
            m.remove(s)
        else:
            strip_text(s)
    return m


def piles_mini(h: float = 1.0) -> VGroup:
    """Beat 3: a glyph-only miniature of V2's three piles (frames, file glyphs, the pencil, the GOLD
    key in the ignored pile). .key"""
    v2 = ThreePiles()
    v2.key.is_key = True
    g = VGroup(*[v2.piles[k] for k in ("tracked", "untracked", "ignored")]).copy()
    strip_text(g)
    g.scale_to_fit_height(h)
    key = next(m for m in g.get_family() if getattr(m, "is_key", False))
    key.scale(2.0)
    key.shift(LEFT * 0.12)
    g.key = key
    return g


def arch_picture() -> VGroup:
    """Beat 1: the BLUE Docker Hub shelf with two TEAL boxes amd64 / arm64, the PINK signpost
    $DOCKER_USERNAME/$IMAGE_NAME above them (two arrows), a GREY cloud VM left and a GREY
    Apple-silicon Mac right. Centred at ORIGIN; parts as attributes."""
    hub = shelf("Docker Hub", 6.2, HUB)
    place(hub, cx=0, ref=hub.board)
    place(hub, cy=-1.0, ref=hub.board)
    ht = illustration_tag().next_to(hub.caption, RIGHT, buff=0.25)
    boxes = {}
    for name, x in (("amd64", -1.6), ("arm64", 1.6)):
        b = sealed_box(1.7, CTR)
        lb = mono(name, TAG, INK).move_to(b.front.get_center() + DOWN * 0.3)
        g = VGroup(b, lb)
        g.box, g.label = b, lb
        g.next_to(hub.board, UP, buff=0.04)
        g.set_x(x)
        boxes[name] = g
    post = signpost(["$DOCKER_USERNAME/", "$IMAGE_NAME"], post_h=0.0)
    post.remove(post.post, post.foot)
    place(post, cx=-0.15, bottom=boxes["amd64"].get_top()[1] + 0.55)
    arrows = VGroup()
    for name, dx in (("amd64", -0.75), ("arm64", 0.75)):
        a = post.board.get_bottom() + RIGHT * dx
        b_ = boxes[name].box.lid.get_top() + UP * 0.03
        arrows.add(Arrow(a, b_, buff=0.04, color=LOOKUP, stroke_width=4,
                         max_tip_length_to_length_ratio=0.3, max_stroke_width_to_length_ratio=10))
    vm = server(1.05, 3, LAPTOP)
    place(vm, cx=-5.2, cy=-0.45)
    vm_l = sans("cloud VM", CAPTION, LAPTOP).next_to(vm, DOWN, buff=0.12)
    mac = laptop(1.6, LAPTOP)
    place(mac, cx=5.0, cy=-0.5)
    mac_l = sans("Apple-silicon Mac", CAPTION, LAPTOP).next_to(mac, DOWN, buff=0.12)
    pull_vm = Arrow(boxes["amd64"].box.front.get_left() + LEFT * 0.08, vm.get_right() + RIGHT * 0.12,
                    buff=0.04, color=HUB, stroke_width=4, max_tip_length_to_length_ratio=0.12)
    pull_mac = Arrow(boxes["arm64"].box.side.get_right() + RIGHT * 0.08, mac.get_left() + LEFT * 0.12,
                     buff=0.04, color=HUB, stroke_width=4, max_tip_length_to_length_ratio=0.12)
    l2 = grey_tag("lecture 2")
    place(l2, cx=mac.get_center()[0], bottom=mac.get_top()[1] + 0.3)
    g = VGroup(hub, ht, *boxes.values(), post, arrows, vm, vm_l, mac, mac_l, pull_vm, pull_mac, l2)
    g.hub, g.hub_tag, g.boxes, g.post, g.arrows = hub, ht, boxes, post, arrows
    g.vm, g.vm_l, g.mac, g.mac_l, g.pull_vm, g.pull_mac, g.l2 = vm, vm_l, mac, mac_l, pull_vm, pull_mac, l2
    return g


def trash_glyph(h: float = 0.3, color: str = ERR) -> VGroup:
    body = Polygon([-h * 0.3, h * 0.35, 0], [h * 0.3, h * 0.35, 0], [h * 0.24, -h * 0.5, 0],
                   [-h * 0.24, -h * 0.5, 0], stroke_color=color, stroke_width=2.5).set_fill(color, 0.15)
    lid = Line([-h * 0.4, h * 0.45, 0], [h * 0.4, h * 0.45, 0], color=color, stroke_width=3)
    knob = Line([-h * 0.1, h * 0.55, 0], [h * 0.1, h * 0.55, 0], color=color, stroke_width=3)
    return VGroup(body, lid, knob)


def console_mini() -> VGroup:
    """Beat 7: a tiny schematic of the console's key list (glyph-only): a window, a key row with a
    RED trash can; the illustration tag under it."""
    fr = RoundedRectangle(width=1.9, height=1.05, corner_radius=0.08, stroke_color=CLOUD,
                          stroke_width=2.5).set_fill(CLOUD, 0.06)
    bar = Line(fr.get_corner(UP + LEFT) + DOWN * 0.25, fr.get_corner(UP + RIGHT) + DOWN * 0.25,
               color=CLOUD, stroke_width=2)
    dots = VGroup(*[Dot(radius=0.035, color=CLOUD) for _ in range(3)]).arrange(RIGHT, buff=0.06)
    dots.move_to(fr.get_corner(UP + LEFT) + np.array([0.25, -0.125, 0]))
    row = RoundedRectangle(width=1.6, height=0.4, corner_radius=0.06, stroke_color=S.GREY,
                           stroke_width=1.5).set_fill(S.GREY, 0.08)
    row.move_to(fr.get_center() + DOWN * 0.12)
    k = key_glyph(0.2).move_to(row).align_to(row, LEFT).shift(RIGHT * 0.15)
    tr = trash_glyph(0.3).move_to(row).align_to(row, RIGHT).shift(LEFT * 0.15)
    win = VGroup(fr, bar, dots, row, k, tr)
    tg = illustration_tag().next_to(win, DOWN, buff=0.1)
    g = VGroup(win, tg)
    g.trash, g.key = tr, k
    return _keep(g)


def part2_card() -> VGroup:
    """Beat 7: "Part 2: containers that talk to each other directly", two small TEAL boxes and a
    PINK arrow between them. .title .boxes .arrow"""
    t = label("Part 2: containers that talk to each other directly", 34, INK)
    b1 = box(1.5, 1.0, CTR, fill_opacity=0.12, radius=0.1)
    b2 = b1.copy()
    VGroup(b1, b2).arrange(RIGHT, buff=2.6)
    ar = Arrow(b1.get_right(), b2.get_left(), buff=0.12, color=LOOKUP, stroke_width=5,
               max_tip_length_to_length_ratio=0.12)
    g = VGroup(t, VGroup(b1, b2, ar)).arrange(DOWN, buff=0.7)
    g.title, g.boxes, g.arrow = t, VGroup(b1, b2), ar
    return g


def card_frame(rows, header: str | None = None, pad_x: float = 0.3, pad_y: float = 0.2) -> VGroup:
    """A GREY card around arranged rows (README card look), header above. .frame .rows .header"""
    fr = box(rows.width + 2 * pad_x, rows.height + 2 * pad_y, S.GREY, fill=S.BG, fill_opacity=0.95,
             radius=0.14)
    fr.move_to(rows)
    g = VGroup(fr, rows)
    g.frame, g.rows, g.header = fr, rows, None
    if header:
        h = _header_text(header).next_to(fr, UP, buff=0.08).align_to(fr, LEFT).shift(RIGHT * 0.1)
        g.add(h)
        g.header = h
    return g


def stage_out(scene, *keep, run_time: float = 0.5, extra=()):
    """Fade out every mobject on the scene except `keep` (and their families); a mobject that is
    part of another one being faded is faded with it, not twice."""
    fam = set()
    for k in keep:
        fam |= set(k.get_family())
    gone: list = []

    def collect(m):
        if m in fam:
            return
        if not any(x in fam for x in m.get_family()):
            gone.append(m)
            return
        for s_ in m.submobjects:       # a wrapper (an AnimationGroup's group) holding kept parts
            collect(s_)
    for m in list(scene.mobjects):
        collect(m)
    roots = [m for m in gone if not any(o is not m and m in o.get_family() for o in gone)]
    anims = [FadeOut(m) for m in roots] + list(extra)
    if anims:
        scene.play(*anims, run_time=run_time)


class ProdAndCleanup(VoiceScene):
    def construct(self):
        tr = tracker("R", 4)

        # ========================================================== 0 · prod: the builder
        sw = compact_switchboard()
        sw.parts_in("words", "descs")
        place(sw, right=6.4, top=3.42)
        p0 = src_panel(SH, 54, 62, width=13.1)
        place(p0, cx=0, top=1.76, ref=p0.code)
        bars_rm = VGroup(*[p0.bar(n) for n in (55, 56, 57)])
        bar_cr = p0.bar(62)
        use = p0.span(62, "--use")
        cap_b = note("builder = a build engine that can target several processor types")
        place(cap_b, left=-6.3, top=p0.get_bottom()[1] - 0.18)
        tg_use = _keep(tag("becomes the current builder · never switched back", TOOL))
        place(tg_use, right=6.4, top=cap_b.get_bottom()[1] - 0.14)
        link_use = Line(use.get_bottom() + DOWN * 0.06, [use.get_center()[0], tg_use.get_top()[1], 0],
                        color=TOOL, stroke_width=3)
        cap_ls = mixed(["check with", ("mono", "docker buildx ls")])
        fix_use = chip("docker buildx use default", S.GREY, size=CAPTION, font=MONO)
        fix_note = note("switch back afterwards")
        row_c = VGroup(cap_ls, fix_use, fix_note).arrange(RIGHT, buff=0.35)
        place(row_c, left=-6.3, top=tg_use.get_bottom()[1] - 0.14)
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(sw), run_time=0.6)
            self.play(sw.light("prod"), flash(tr.caption, TURN, 1.08), run_time=0.7)
            self.play(FadeIn(p0, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("It recreates")
            self.play(FadeIn(bars_rm), run_time=0.5)
            self.play(flash(p0.span(57, "docker buildx rm multi-arch"), TURN, 1.06), run_time=0.7)
            vo.wait_until("a builder named multi-arch")
            self.play(bars_rm.animate.set_opacity(0.0), FadeIn(bar_cr), run_time=0.5)
            self.play(flash(p0.span(62, "docker buildx create"), TURN, 1.06), run_time=0.6)
            at(self, vo, "a build engine", -0.3)
            self.play(FadeIn(cap_b, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("Dash dash use")
            self.play(use.animate.set_color(TOOL), Create(ring(use, TOOL, buff=0.05)), run_time=0.5)
            self.play(Create(link_use), FadeIn(tg_use, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("and the script never switches back")
            self.play(FadeIn(cap_ls, shift=RIGHT * 0.1), run_time=0.5)
            at(self, vo, "docker buildx use default", -0.45)
            self.play(FadeIn(fix_use, scale=0.9), FadeIn(fix_note, shift=RIGHT * 0.1), run_time=0.6)

        # ========================================================== 1 · one build, two architectures, one tag
        p1 = src_panel(SH, 65, 66, wrap={66: ["--push", "-f Dockerfile"]})
        place(p1, left=-6.3, top=TOP)
        plat = p1.span(66, "--platform linux/amd64,linux/arm64")
        push = p1.span(66, "--push")
        pic = arch_picture()
        place(pic, cx=0, top=p1.get_bottom()[1] - 0.3, ref=VGroup(pic.post, pic.hub))
        for b in pic.boxes.values():
            b.save_state()
            b.shift(UP * 0.35)
        with self.voiceover(SAY[1]) as vo:
            stage_out(self, tr, run_time=0.5)
            self.play(FadeIn(p1, shift=UP * 0.15), run_time=0.5)
            # one 13 s sentence: "amd64" / "arm64" are long when spoken, so the clauses after
            # them come later than the character count says (shifts measured on Kokoro)
            at(self, vo, "makes amd64 and arm64", -0.35)
            self.play(plat.animate.set_color(TOOL), run_time=0.4)
            self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in pic.boxes.values()], lag_ratio=0.3),
                      run_time=0.8)
            at(self, vo, "and pushes both", 0.8)
            self.play(push.animate.set_color(HUB), FadeIn(pic.hub), FadeIn(pic.hub_tag), run_time=0.5)
            self.play(*[b.animate.restore() for b in pic.boxes.values()], run_time=0.5)
            at(self, vo, "under one tag", 0.45)
            self.play(FadeIn(pic.post, shift=DOWN * 0.1), run_time=0.4)
            self.play(LaggedStart(*[GrowArrow(a) for a in pic.arrows], lag_ratio=0.3), run_time=0.7)
            at(self, vo, "as in lecture 2", 0.35)
            self.play(FadeIn(pic.l2, shift=UP * 0.1), run_time=0.4)
            at(self, vo, "an Apple-silicon Mac", 0.45)
            self.play(FadeIn(pic.mac), FadeIn(pic.mac_l), run_time=0.4)
            self.play(GrowArrow(pic.pull_mac), flash(pic.boxes["arm64"].label, TURN, 1.2), run_time=0.7)
            vo.wait_until("a cloud VM the other")
            self.play(FadeIn(pic.vm), FadeIn(pic.vm_l), run_time=0.4)
            self.play(GrowArrow(pic.pull_vm), flash(pic.boxes["amd64"].label, TURN, 1.2), run_time=0.7)

        # ========================================================== 2 · log in, your username, don't run prod yet
        t = term(P_A, rows=3, title="laptop")
        u_tr = tracker("U", 1)
        chip129 = readme_chip("transcribe_audio/README.md · line 129")
        place(chip129, left=u_tr.get_right()[0] + 0.35, cy=BAND_Y)
        p13 = src_panel(SH, 13, 13)
        place(p13, left=-6.3, top=TOP)
        dl = p13.span(13, "dlops")
        own = note("→ your own Docker Hub user").next_to(p13.code, RIGHT, buff=0.35)
        chip76 = readme_chip("README.md · line 76", "update DOCKER_USERNAME")
        place(chip76, left=-6.3, top=p13.get_bottom()[1] - 0.25)
        u4 = note("= How to Run · step 4")
        warn = note("first: check what it would publish", TURN)
        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(VGroup(p1, pic)), FadeOut(tr, shift=UP * 0.25), FadeIn(u_tr, shift=DOWN * 0.25),
                      run_time=0.6)
            tr = u_tr
            self.play(FadeIn(t, shift=UP * 0.2), FadeIn(chip129, shift=DOWN * 0.1), run_time=0.5)
            login = type_tagged(self, t, LOGIN, "not run here", type_time=0.9)
            vo.wait_until("dash p leaves it")
            pflag = substring(login.rows[-1], "-p")
            pr = ring(pflag, KEY, buff=0.05)
            gold = _keep(tag("the token stays in your shell history", KEY))
            place(gold, right=pflag.get_right()[0] + 1.3, cy=login.rows[-1].strut.get_center()[1] - t.pitch)
            stem = Line(pr.get_bottom(), [pr.get_center()[0], gold.get_top()[1], 0], color=KEY, stroke_width=3)
            self.play(Create(pr), run_time=0.4)
            self.play(Create(stem), FadeIn(gold, shift=UP * 0.1), run_time=0.6)
            stdin = chip("--password-stdin", S.GREY, size=CAPTION, font=MONO)
            stdin_n = note("avoids it")
            sg = VGroup(stdin, stdin_n).arrange(RIGHT, buff=0.15)
            place(sg, right=6.3, bottom=STRIP_TOP + 0.25)
            self.play(FadeIn(sg, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Set the Docker username")
            self.play(FadeIn(p13, shift=DOWN * 0.1), run_time=0.5)
            self.play(Create(under(dl, TURN)), FadeIn(own, shift=RIGHT * 0.1), run_time=0.6)
            self.play(FadeIn(chip76, shift=DOWN * 0.1), run_time=0.5)
            vo.wait_until("Don't run prod yet")
            self.play(tr.goto(2), FadeOut(chip129), FadeOut(VGroup(pr, gold, stem, sg)), run_time=0.5)
            place(u4, left=tr.caption.get_right()[0] + 0.3, cy=tr.caption.get_center()[1])
            self.play(FadeIn(u4, shift=LEFT * 0.1), run_time=0.3)
            type_tagged(self, t, PROD, "not run here: needs a login · publishes an image", type_time=0.5)
            vo.wait_until("first, check what")
            place(warn, right=6.3, bottom=STRIP_TOP + 0.3)
            self.play(FadeIn(warn, shift=UP * 0.1), run_time=0.5)

        # ========================================================== 3 · the lecture 3 clone: dev, and the key is inside
        mini = piles_mini(1.0)
        place(mini, right=6.35, top=3.42)
        skip = note("if you skipped the deletion in Get the Code")
        with self.voiceover(SAY[3]) as vo:
            out2, done2 = wipe(t)
            r_tr = tracker("R", 2)            # switch_section's lift/drop, in the same play
            r_tr.caption.become(caption_extra(r_tr, True).target_mobject)
            stage_out(self, tr, t, run_time=0.5,
                      extra=[out2, FadeOut(tr, shift=UP * 0.25), FadeIn(r_tr, shift=DOWN * 0.25),
                             retitle(t, "laptop · lecture 3 clone")])
            done2()
            tr = r_tr
            t.set_prompt(P_L3A)
            resize(self, t, 12, run_time=0.5)
            bare_prompt(self, t)
            vo.wait_until("In the switched lecture 3 clone")
            place(skip, left=-6.3, top=tr.get_bottom()[1] - 0.12)
            self.play(FadeIn(mini, shift=LEFT * 0.15), FadeIn(skip, shift=DOWN * 0.1), run_time=0.7)
            at(self, vo, "the old key still sits", -0.3)
            self.play(Create(ring(mini.key, TURN, buff=0.06)), flash(mini.key, TURN, 1.4), run_time=0.8)
            vo.wait_until("Build there with dev")
            type_tagged(self, t, C12.cmd, "extra", type_time=0.5)
            rows = print_build(self, t, DEV_ROWS, run_time=0.6, lag=0.1)
            slim_times(t, rows)
            cp = glyph_box(rows[2], "[4/5] COPY --chown=app:app . ./")
            pin(self, rows[2], cp, run_time=0.4, anim=Create(cp))
            nc = fit_tag(t, rows[2], "not CACHED")
            pin(self, rows[2], nc, run_time=0.3)
            vo.wait_until("and an extra command lists")
            run_ln = type_tagged(self, t, C13.cmd, "extra", type_time=1.2)
            ls = t.print(self, LS_ROWS, run_time=0.6)
            at(self, vo, "the key is inside", -0.4)
            kname = substring(ls[5], "mega-pipeline.json")
            st = standin_tag()
            place(st, cx=kname.get_center()[0], cy=ls[4].strut.get_center()[1])
            self.play(kname.animate.set_color(ERR), run_time=0.3)
            self.play(flash(kname, ERR, 1.1), run_time=0.5)
            pin(self, ls[4], st, run_time=0.4)

        # ========================================================== 4 · COPY takes the whole folder; prod would push it
        v5 = TwoWindows(show=("laptop", "image"), l03=True)
        for n in ("container", "venv", "route_app", "route_secrets", "post", "ghost", "never", "clock"):
            v5.remove(v5.parts[n])
        place(v5, left=-6.35, top=2.6, ref=v5.laptop_frame)
        img = v5.parts["image"]
        slab, slab_l = img[0], img[1]
        slab.stretch_to_fit_width(3.6)
        place(img, left=-0.55, cy=1.5, ref=slab)
        slab_l.move_to(slab).align_to(slab, LEFT).shift(RIGHT * 0.2)
        p39 = src_panel(DF, 39, 39)
        place(p39, left=-0.55, top=3.42)
        git = shelf("Git", 2.3, LAPTOP)
        place(git, left=2.35, cy=-0.75, ref=git.board)
        tracked = VGroup(*[file_glyph(0.34, VENV) for _ in range(3)]).arrange(RIGHT, buff=0.18)
        tracked.next_to(git.board, UP, buff=0.06)
        shd = shield("/secrets", S.GREY, h=0.75)
        place(shd, right=git.board.get_left()[0] - 0.3, bottom=git.caption.get_bottom()[1])
        gi_head = _header_text("transcribe_audio/.gitignore · line 3")
        place(gi_head, left=shd.get_left()[0] - 0.4, bottom=shd.get_top()[1] + 0.08)
        g_from = v5.key.get_right() + RIGHT * 0.15
        g_to = np.array([shd.body.get_left()[0] - 0.1, shd.body.get_center()[1], 0])
        git_try = DashedLine(g_from, g_to, color=S.GREY, stroke_width=3, dash_length=0.12)
        git_try.add_tip(tip_length=0.18, tip_width=0.18)
        dock = dashed_chip([("mono", ".dockerignore", S.GREY), ": none, on every branch"])
        place(dock, left=-1.5, top=slab.get_bottom()[1] - 0.15)     # clear of the laptop frame
        hub = shelf("Docker Hub", 1.9, HUB)
        place(hub, right=6.35, cy=slab.get_bottom()[1] + 0.02, ref=hub.board)
        hub_tag = illustration_tag()
        place(hub_tag, right=6.35, bottom=hub.board.get_center()[1] + 0.42)
        track = Line([slab.get_right()[0] + 0.1, slab.get_center()[1], 0],
                     [hub.board.get_left()[0] - 0.1, slab.get_center()[1], 0], color=TOOL, stroke_width=5)
        prod_l = mono("prod", CAPTION, TOOL).next_to(track, UP, buff=0.1)
        with self.voiceover(SAY[4]) as vo:
            # the packing has to be done before "The gitignore …" (2.5 s in): the strip's old
            # lines fade with the miniature, then the shrink, then the picture, then COPY
            keep4 = [run_ln.rows[-1], ls[4], ls[5]]
            gone4 = [ln for ln in t.lines.submobjects if ln not in keep4]
            stage_out(self, tr, t, run_time=0.35, extra=[FadeOut(VGroup(*gone4))])
            for ln in gone4:
                t.lines.remove(ln)
            resize(self, t, 3, keep=keep4, run_time=0.45)
            self.play(FadeIn(v5), FadeIn(p39, shift=DOWN * 0.1), run_time=0.4)
            copies, anims = v5.pack(run_time=1.0)
            self.add(copies)
            self.play(flash(p39.span(39, "COPY --chown=app:app . ./"), TURN, 1.06), *anims)
            vo.wait_until("The gitignore keeps secrets out of Git")
            self.play(FadeIn(git), FadeIn(tracked), FadeIn(shd), FadeIn(gi_head), run_time=0.5)
            self.play(Create(git_try), run_time=0.8)
            self.play(flash(shd.body, VENV, 1.15), run_time=0.5)
            at(self, vo, "not out of images", -0.5)
            kc = copies[2]
            self.play(Create(ring(kc, ERR, buff=0.06)), flash(kc, ERR, 1.4), run_time=0.7)
            at(self, vo, "and no branch has a dockerignore", -0.4)
            self.play(FadeIn(dock, shift=UP * 0.1), run_time=0.6)
            vo.wait_until("Prod would push your key")
            self.play(Create(track), FadeIn(prod_l), FadeIn(hub), FadeIn(hub_tag), run_time=0.5)
            layer = VGroup(slab.copy(), *[c.copy() for c in copies])
            self.add(layer)
            lw = hub.board.get_width() - 0.2
            self.play(layer.animate.scale(lw / slab.width).next_to(hub.board, UP, buff=0.04), run_time=0.8)
            self.play(hub.board.animate.set_color(ERR), hub.caption.animate.set_color(ERR), run_time=0.3)
            self.play(flash(VGroup(hub.board, layer), ERR, 1.1), run_time=0.6)

        # ========================================================== 5 · erratum: the promise holds for Git only; the fix
        q_rows = VGroup(
            mixed(["“Never commit", ("mono", "secrets/", INK), "to Git. Keeping the folder outside the repo"],
                  color=INK, size=TAG),
            mixed(["(as this branch does) is", "the canonical way to make that mistake impossible.”"],
                  color=INK, size=TAG),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        card203 = card_frame(q_rows, "README.md · line 203")
        place(card203, left=-6.3, top=TOP - 0.05)
        phrase = q_rows[1][1]
        err = erratum_tag().next_to(card203.header, RIGHT, buff=0.35)
        verdict = mixed(["for Git: yes"], size=TAG)
        ck = check_mark(0.26, VENV)
        v2_ = mixed(["· for images: no"], size=TAG)
        cx_ = cross_mark(0.24, ERR)
        vrow = VGroup(verdict, ck, v2_, cx_).arrange(RIGHT, buff=0.15)
        place(vrow, left=-6.0, top=card203.get_bottom()[1] - 0.2)
        fix_rows = VGroup(
            mixed(["delete the", ("mono", "secrets/", INK), "folder inside each component"], color=INK, size=SMALL),
            mixed(["add a", ("mono", ".dockerignore", INK), "listing", ("mono", "secrets/", INK),
                   "(lecture 3)"], color=INK, size=SMALL),
            mixed(["a key was ever pushed? delete that key in IAM"], color=ERR, size=SMALL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        fix = card_frame(fix_rows, None, pad_x=0.4, pad_y=0.3)
        fix_h = note("the fix").next_to(fix.frame, UP, buff=0.08).align_to(fix.frame, LEFT).shift(RIGHT * 0.12)
        place(VGroup(fix, fix_h), left=-6.3, top=vrow.get_bottom()[1] - 0.6)
        yt = your_turn()                   # on the card's header row, right (not on its border)
        place(yt, right=fix.frame.get_right()[0], bottom=fix.frame.get_top()[1] + 0.08)
        with self.voiceover(SAY[5]) as vo:
            stage_out(self, tr, run_time=0.5, extra=[caption_extra(tr, False)])
            t.lines.submobjects.clear()
            self.play(FadeIn(card203, shift=DOWN * 0.1), FadeIn(err, shift=LEFT * 0.1), run_time=0.5)
            self.play(Create(under(phrase, TURN)), run_time=0.5)
            at(self, vo, "holds for Git", -0.3)
            self.play(FadeIn(verdict), FadeIn(ck, scale=1.3), run_time=0.5)
            at(self, vo, "not for images", -0.6)
            self.play(FadeIn(v2_), FadeIn(cx_, scale=1.3), run_time=0.5)
            vo.wait_until("Delete any secrets folder")
            self.play(FadeIn(fix.frame), FadeIn(fix_h), FadeIn(fix_rows[0], shift=RIGHT * 0.1), run_time=0.6)
            at(self, vo, "add a dockerignore", -0.35)
            self.play(FadeIn(fix_rows[1], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("and if a key was ever pushed")
            self.play(FadeIn(fix_rows[2], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("Pause and check yours")
            self.play(FadeIn(yt, shift=LEFT * 0.1), run_time=0.4)
        self.wait(1.5)                    # the your-turn card stays up to be read / paused on

        # ========================================================== 6 · clean-up for part 1: docker images
        t6 = term(P_REPO, rows=7, title="laptop")
        pushed = [mixed(["pushed with prod? that Docker Hub repo is public"], color=COST, size=TAG),
                  mixed(["delete it if you don't need it"], color=COST, size=TAG)]
        lines = [
            mixed(["clean-up · part 1"], color=INK, size=SMALL),
            mixed(["exit each container ·", ("mono", "--rm", INK), "removes it"], color=INK, size=TAG),
            mixed([("mono", "docker image rm <name>", INK), "· your five images"], color=INK, size=TAG),
            mixed(["any", ("mono", "dlops/*", INK), "images you pulled"], color=INK, size=TAG),
            mixed(["the root-owned", ("mono", "Pipfile", INK)], color=INK, size=TAG),
            mixed(["ran prod?", ("mono", "docker buildx rm multi-arch", S.GREY)], color=S.GREY, size=TAG),
            mixed(["bucket: storage bills until you delete it", "· when the course is over"],   # 2 parts:
                  color=COST, size=TAG),                                                     # 2 cues
            mixed(["key: valid until you delete it · IAM › Service accounts › Keys"], color=COST, size=TAG),
            *pushed,
        ]
        stack(lines, 0.43, head_gap=0.06)          # equal baselines (serif and mono rows)
        pushed[1].shift(np.array([0.3, 0.07, 0]))   # its continuation: indented, a little closer
        crows = VGroup(*lines[:8], VGroup(*pushed))
        first6 = VGroup(*crows[:6])
        frA = box(first6.width + 0.6, first6.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        frA.move_to(first6).align_to(first6, LEFT).shift(LEFT * 0.3)
        place(VGroup(frA, crows), right=6.4, top=3.42, ref=frA)
        with self.voiceover(SAY[6]) as vo:
            stage_out(self, tr, run_time=0.5)
            self.play(tr.goto(4), FadeIn(t6, shift=UP * 0.2), FadeIn(frA), FadeIn(crows[0]), run_time=0.6)
            self.play(caption_extra(tr, True), run_time=0.3)
            vo.wait_until("Exit each container")
            self.play(FadeIn(crows[1], shift=RIGHT * 0.1), run_time=0.5)
            at(self, vo, "The transcribe image alone", -1.75)   # its output is up as that sentence starts
            type_tagged(self, t6, C70.cmd, "extra", type_time=0.4)
            imgs = t6.print(self, IMG_ROWS, run_time=0.6)
            # S16's honesty tag; the header row has no room at its end, so it sits in the gap
            cols = grey_tag("2 of 5 columns").next_to(substring(imgs[0], "IMAGE"), RIGHT, buff=0.45)
            cols.set_y(imgs[0].strut.get_center()[1])
            assert cols.get_right()[0] < substring(imgs[0], "DISK USAGE").get_left()[0] - 0.3
            pin(self, imgs[0], cols, run_time=0.3)
            vo.wait_until("The transcribe image alone")
            self.play(flash(substring(imgs[4], "mega-pipeline-transcribe-audio"), TURN, 1.04), run_time=0.7)
            at(self, vo, "is 1.48 gigabytes", -0.55)
            big = glyph_box(imgs[4], "1.48GB")
            self.play(Create(big), flash(substring(imgs[4], "1.48GB"), TURN, 1.1), run_time=0.6)
            vo.wait_until("remove all five")
            unders = [under(substring(imgs[k], v), TURN, stroke=3) for k, v in SMALL_IMGS.items()]
            self.play(LaggedStart(*[Create(u) for u in unders], lag_ratio=0.2), run_time=0.7)
            self.play(FadeIn(crows[2], shift=RIGHT * 0.1), run_time=0.5)
            vo.wait_until("plus any dlops images")
            self.play(FadeIn(crows[3], shift=RIGHT * 0.1), run_time=0.5)
            self.play(FadeIn(crows[4], shift=RIGHT * 0.1), run_time=0.5)
            self.play(FadeIn(crows[5], shift=RIGHT * 0.1), run_time=0.5)

        # ========================================================== 7 · the cloud; part 2 teaser; empty frame
        frB = box(crows.width + 0.6, crows.height + 0.4, S.GREY, fill=S.BG, fill_opacity=0.95, radius=0.14)
        frB.move_to(crows)
        con = console_mini()
        gap = 0.45                                 # the console sits beside the key row; both centred
        span = frB.width + gap + con.width
        dxy = np.array([-span / 2 - frB.get_left()[0], -0.25 - frB.get_center()[1], 0])
        frB.shift(dxy)
        place(con, left=frB.get_right()[0] + gap, cy=crows[7].get_center()[1] + dxy[1], ref=con[0])
        close = part2_card()
        with self.voiceover(SAY[7]) as vo:
            stage_out(self, tr, frA, *crows[:6], run_time=0.8,
                      extra=[*[r.animate.shift(dxy) for r in crows[:6]], Transform(frA, frB)])
            for r in crows[6:]:
                r.shift(dxy)
            vo.wait_until("the bucket bills")
            self.play(FadeIn(crows[6][0], shift=RIGHT * 0.1), run_time=0.5)
            at(self, vo, "when the course is over", -0.2)
            self.play(FadeIn(crows[6][1], shift=RIGHT * 0.1), run_time=0.5)
            at(self, vo, "the key works", -0.45)
            self.play(FadeIn(crows[7], shift=RIGHT * 0.1), FadeIn(con, shift=LEFT * 0.1), run_time=0.6)
            self.play(FadeIn(crows[8], shift=RIGHT * 0.1), run_time=0.5)
            at(self, vo, "in the console", -0.2)
            self.play(flash(con.trash, ERR, 1.3), run_time=0.6)
            vo.wait_until("In part 2")
            stage_out(self, run_time=0.6)
            self.play(FadeIn(close.title, shift=UP * 0.1), FadeIn(close.boxes), run_time=0.7)
            self.play(GrowArrow(close.arrow), run_time=0.6)
        self.wait(0.8)
        stage_out(self, run_time=0.8)
        self.wait(0.3)
