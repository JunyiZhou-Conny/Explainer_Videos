"""S13 · Platforms: arm64 vs amd64 (TRACKER B4 · extra for the whole scene; V7).

Beats (script.md "## S13", one voiceover block each):
 0  S12 ended on an empty frame: TRACKER B4 fades in with a 6-row laptop terminal; "this scene is all
    extras": the caption gets " · extra" and the row tag `extra` sits beside the typed command.
    `uname -m; docker image inspect simple-translate --format '{{.Os}}/{{.Architecture}}'` (laptop/35's
    own command; folded by hand onto 3 rows, one command per row, see UNAME_ROWS) -> laptop/35: 2–3. "Our machine is Intel or AMD": `x86_64` turns BLUE,
    row tag "this machine · Intel/AMD"; "the image says": `linux/amd64` BLUE, row tag "the image";
    "On an Apple Silicon Mac": a GREY brace over both and the GREY note "Apple Silicon Mac: arm64".
 1  V7 (the terminal goes). Two chips with their glyph rows ("machine instructions"): `arm64 · Apple
    Silicon` (GREY) over a GREY laptop, `amd64 · Intel/AMD · default GCP VM` (BLUE) over a BLUE VM.
    "Every program in an image": a TEAL image card; "bash, Python, uv" written in; "is machine code":
    each gets a row of amd64 glyphs. "amd64 for Intel and AMD": the BLUE row glows (with the image's
    rows); "arm64 for Apple Silicon": the GREY row glows. "A container's programs": the card slides
    down onto the BLUE chip, a copy of the chip's row lands on the card's rows (same shapes) and a
    GREEN check appears; "so unless an emulator steps in": GREY note "runs directly on the CPU /
    unless an emulator steps in"; "Docker Desktop has one built in": "Docker Desktop" and a GREY
    "emulator" box inside the laptop's screen; "a plain Linux VM doesn't": a dashed slot "no emulator"
    beside the VM.
 2  The picture goes; a 13-row terminal types `docker buildx imagetools inspect
    python:3.12-slim-bookworm` (folds) -> laptop-push/11: 2–3, 9, …, 30, …, 51, …, 72, …, 93. "lists
    five platforms": the five platforms turn YELLOW; the terminal shrinks to the strip (the command and
    line 3, `…index.v1+json`, with the row tag "index = a menu") while the five platforms fly up into the
    rows of a TEAL menu card `python:3.12-slim-bookworm` (amd64 BLUE, arm64/v8 GREY; each row with its
    dimmed "+ attestation"). "amd64", "two kinds of arm", "two rarer ones": the rows pulse as named.
    "Docker pulls the row": a BLUE VM glyph, a BLUE arrow and a BLUE frame on the amd64 row.
 3  The menu goes; the strip grows to 8 rows: `docker buildx imagetools inspect dlops/simple-translate`
    -> laptop-push/10: 2–4 (hash12). "is no menu": `manifest.v2+json` YELLOW, underlined, row tag
    "one image, not a menu" (the python `index` row above it stays for comparison); "one image, amd64
    only": above the terminal a BLUE VM glyph, "image inspect on the VM:" and a GREY chip `linux/amd64`
    (vm-debian12/08 line 3).
 4  The terminal clears; `stand_in_tag()` on its frame. `docker buildx imagetools inspect
    localhost:5000/student/simple-translate-ac215` (folds) -> laptop-push/09: 3, 9, 13. "a small
    menu": the strip keeps the command and line 3, the two platforms fly up into a menu "our push": a
    BLUE `linux/amd64` row and a dimmed `unknown/unknown` row; "plus an attestation": GREY note
    "attestation · how it was built"; "a record of how": a GREY dashed overlay right of the first row
    "built on a Mac: linux/arm64" and a GREY note under the menu "containerd image store · the older
    store pushes one image, no menu". Neither note is narrated: the picture holds 3 s after the
    narration so they can be read.
 5  The strip and the menu go. Top band: "You built on an M-series Mac": the GREY arm64 chip over a
    laptop builds an image card `linux/arm64` (arm64 glyphs); "and pushed": a PINK route carries it to a
    BLUE shelf "Docker Hub"; "Your VM is an ordinary": a BLUE VM with an `amd64 · default VM` chip and
    its dashed "no emulator" slot; "Will your image run there?": the image rides on to the VM.
    PONDER (8 s) in the bottom half (the picture stays above it).
 6  "No.": a RED cross on the card, the card goes; the VM sends a BLUE `amd64?` chip to the image:
    its `linux/arm64` turns RED with a RED cross, GREY "nothing it can run". "Here's the same
    failure": a 5-row terminal, tag "extra · arm64 image on an amd64 machine" on its frame; `docker run
    --rm --platform linux/arm64 debian:12 uname -m` (folds) -> laptop-push/12: 2, …, 10, line 10 RED;
    "exec format error": underlined RED. "Docker Desktop would just run it": GREY tag "no emulator here
    · Docker Desktop would run it" on the frame. "A Mac-built image on a default VM": the terminal
    shrinks to the strip (command + line 10); "fails like this": the image's cross pulses with line 10;
    "or with no matching manifest": the VM's `amd64?` bounces off the image and GREY "no matching
    manifest" lands where it hit.
 7  Everything goes; "Two fixes, neither in the README" as a GREY heading. "One: build for the VM's
    platform": the heading gives way to a one-line GREEN chip mid-frame (tags "fix 1", "not run here")
    that writes `docker build -t simple-translate --platform=linux/amd64 -f Dockerfile .`; "with the
    flag": `--platform=linux/amd64` BLUE, underlined; "equals linux slash amd64": a YELLOW circumscribe
    around `linux/amd64`. "It's the commented-out line 12": CODE(docker-shell.sh: 11–12) at the top,
    line 12 YELLOW bar, GREY tag "commented out · not in the README", and the chip's underline is copied
    up onto line 12's `--platform=linux/amd64` (the same flag). "On a Mac, it runs emulated": the chip moves down
    to make room for V7 between them: the GREY arm64 chip builds an image (`linux/arm64`, arm64 glyphs)
    that goes through a GREY "emulation" box and comes out `linux/amd64` with amd64 glyphs; "slower":
    GREY "slower, but it works" and a GREEN check. "Then tag and push again": the chip grows to three
    lines, its lines 2–3 the README's tag and push (`<USER NAME>` YELLOW).
 8  The panel, chip and picture go. Picture first: a PURPLE `buildx` box (tag "fix 2") over the GREY
    arm64 chip; "multi-platform builder": two lanes, the upper one through a GREY "emulation" box; "to
    build both": an amd64 image (through emulation: on a Mac the amd64 build is the emulated one) and an
    arm64 image; "and push one menu": a menu `<USER NAME>/simple-translate-ac215` (`<USER NAME>` YELLOW:
    what the viewer's run pushes after beat 9's edit of lines 7 and 11, not dlops's amd64-only image of
    beat 3) on a BLUE "Docker Hub" board, and each image rides its PINK route and becomes its row
    (linux/amd64 BLUE, linux/arm64 GREY). The
    narration is ~7 s, so CODE(docker-build-push.sh: 21–27) (line 27 cut after `--push`: 109 characters)
    comes in at "multi-platform builder", lines 23 and 27 YELLOW; tag `erratum · would push both · the
    published image has only amd64`, held 3 s after the narration.
 9  The picture goes; the panel becomes CODE(docker-build-push.sh: 7–11): line 11 (`"dlops"` boxed)
    and line 7 (`"simple-translate"` boxed) YELLOW as said, YELLOW caption "your username (11) ·
    simple-translate-ac215 (7)". A list of GREEN chips (no room for one row at >= 20 pt): `docker
    login` "first" · `bash docker-build-push.sh` "the script isn't executable" · `docker buildx use
    default` "afterwards: builds land on your laptop again" / "desktop-linux on Docker Desktop".
    Fade to an empty frame.
"""

import numpy as np  # noqa: I001  (manim first, then common: common must win)
from manim import *

from explainer import style as S
from explainer.components import ponder_card
from explainer.devops import MONO, cell_width, code_panel, code_span, cross_mark, laptop, line_bar
from explainer.scene import VoiceScene

from common import (AMD, ARM, CLOUD, ERR, IMAGE, INK, LAPTOP, LAPTOP_DIR, NARRATION, PUSH_DIR,
                    P_LAPTOP, PUSH_README, STRIP_ROWS, TAG_README, TOOL, TURN, VENV, VM12, PlatformMenu,
                    attach, bare_prompt, beside, box, builder_box, capture, check_mark, chip, code, cut,
                    erratum_tag, excerpt, glyph_row, hash12, label, laptop_term, mono, mono_line, outline_box,
                    platform_chip, resize, route, row_tag, shelf_glyph, stand_in_tag, steady, substring, tag,
                    track, tracker_b, type_cmd, under, vm_glyph)

SAY = NARRATION["S13"]

# ------------------------------------------------------------------ real outputs (file line numbers)
C35 = capture("35", LAPTOP_DIR)                       # laptop/35-platform.txt
UNAME = C35.cmd
assert UNAME == "uname -m; docker image inspect simple-translate --format '{{.Os}}/{{.Architecture}}'", UNAME
# Terminal.fold breaks before an option, which would split `uname \` from its `-m`; folded by hand instead,
# one command per row (house style: " \" + 4-space indent), so the rows still paste back as the command.
UNAME_ROWS = [f"{P_LAPTOP} uname -m; \\",
              "    docker image inspect simple-translate \\",
              "    --format '{{.Os}}/{{.Architecture}}'"]
assert " ".join([UNAME_ROWS[0][:-2], UNAME_ROWS[1][4:-2], UNAME_ROWS[2][4:]]) == f"{P_LAPTOP} {UNAME}"
assert max(len(r) for r in UNAME_ROWS) <= 65
OUT35 = C35.at((2, 3))
assert OUT35 == ["x86_64", "linux/amd64"], OUT35

C11 = capture("11", PUSH_DIR)                         # laptop-push/11-imagetools-python.txt
PY_CMD = C11.cmd
assert PY_CMD == "docker buildx imagetools inspect python:3.12-slim-bookworm", PY_CMD
OUT11 = C11.at((2, 3), 9, "…", 30, "…", 51, "…", 72, "…", 93)
PLATS = ["linux/amd64", "linux/arm/v7", "linux/arm64/v8", "linux/386", "linux/ppc64le"]
assert [C11.line(n).split()[-1] for n in (9, 30, 51, 72, 93)] == PLATS
# each platform image is followed by its attestation manifest (unknown/unknown)
assert [C11.line(n).split()[-1] for n in (22, 43, 64, 85, 106)] == ["unknown/unknown"] * 5
assert [C11.line(n).split()[-1] for n in (26, 45, 68, 89, 110)] == ["attestation-manifest"] * 5
assert OUT11[1].endswith("index.v1+json"), OUT11[1]

C10 = capture("10", PUSH_DIR)                         # laptop-push/10-imagetools-dlops.txt
DL_CMD = C10.cmd
assert DL_CMD == "docker buildx imagetools inspect dlops/simple-translate", DL_CMD
OUT10 = [hash12(s) for s in C10.at((2, 4))]
assert OUT10[1].endswith("distribution.manifest.v2+json") and OUT10[2].startswith("Digest:"), OUT10

VM08 = capture("08", VM12).line(3)                    # vm-debian12/08: image inspect on the VM
assert VM08.startswith("linux/amd64 created"), VM08
VM_PLAT = VM08.split()[0]

C09 = capture("09", PUSH_DIR)                         # laptop-push/09-imagetools-local.txt
SI_CMD = C09.cmd
assert SI_CMD == "docker buildx imagetools inspect localhost:5000/student/simple-translate-ac215", SI_CMD
OUT09 = C09.at(3, 9, 13)
assert OUT09[0].endswith("index.v1+json") and OUT09[1].endswith("linux/amd64") \
    and OUT09[2].endswith("unknown/unknown"), OUT09

C12 = capture("12", PUSH_DIR)                         # laptop-push/12-arm64-on-amd64.txt
ARM_CMD = C12.cmd
assert ARM_CMD == "docker run --rm --platform linux/arm64 debian:12 uname -m", ARM_CMD
OUT12 = C12.at(2, "…", 10)
ERR_LINE = OUT12[-1]
assert ERR_LINE == "exec /usr/bin/uname: exec format error", ERR_LINE

# ------------------------------------------------------------------ the fixes (script.md, not run here)
L12 = excerpt("docker-shell.sh", 12, 12)
assert L12 == "#docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .", L12
FIX1 = "docker build -t simple-translate --platform=linux/amd64 -f Dockerfile ."
PLAT_FLAG = "--platform=linux/amd64"
L23 = excerpt("docker-build-push.sh", 23, 23)
L27 = excerpt("docker-build-push.sh", 27, 27)
assert L23 == "docker buildx create --driver-opt network=host --use --name multi-arch", L23
assert L27.startswith("docker buildx build --platform linux/amd64,linux/arm64 --push -t "), L27
SRC_21_27 = excerpt("docker-build-push.sh", 21, 26) + "\n" + cut(L27, "--push", " …")   # 109 chars: cut
L07 = excerpt("docker-build-push.sh", 7, 7)
L11 = excerpt("docker-build-push.sh", 11, 11)
assert L07 == 'export IMAGE_NAME="simple-translate"' and L11 == 'DOCKER_USERNAME="dlops"', (L07, L11)

PONDER_Q = ("You built on an M-series Mac and pushed.\nYour VM is an ordinary Intel/AMD machine.\n"
            "Will your image run there?")
IMG_NAMES = ("bash", "python", "uv")

# ------------------------------------------------------------------ layout
XA, XB = -4.1, 3.35            # beat 1: the arm64 (GREY) and amd64 (BLUE) columns
CHIP_Y, MACH_Y = -0.45, -2.45  # beat 1: chip + glyph row, machine glyph


# ------------------------------------------------------------------ builders
def image_card(kind: str = "amd64", plat: str | None = None, names=IMG_NAMES, n: int = 6,
               glyph_h: float = 0.22, pitch: float = 0.42, size: float = 20) -> VGroup:
    """V7 · an image: a TEAL card; a header ("image", or the platform it was built for as a steady
    mono text); one row per program with its machine code in `kind`'s glyphs (names=None: glyph rows
    only). .frame .head .names .codes (.plat when plat is given)"""
    if plat:
        head = steady(plat, size, ARM if "arm" in plat else AMD, mono_font=True)
    else:
        head = label("image", size, IMAGE)
    codes = VGroup(*[glyph_row(kind, n, glyph_h) for _ in range(len(names) if names else 3)])
    nms = VGroup()
    x_code = (max(len(s) for s in names) * cell_width(size) + 0.3) if names else 0.0
    for i, c in enumerate(codes):
        y = -i * pitch
        if names:
            t = mono_line(names[i], size, INK)
            t.shift(np.array([-t.strut.get_left()[0], y - t.strut.get_center()[1], 0]))
            nms.add(t)
        c.move_to([x_code + c.width / 2, y, 0])
    body = VGroup(nms, codes) if names else VGroup(codes)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
    frame = box(max(inner.width, head.width) + 0.55, inner.height + 0.42, IMAGE, fill_opacity=0.08)
    inner.move_to(frame)
    g = VGroup(frame, head, nms, codes)
    g.frame, g.head, g.names, g.codes = frame, head, nms, codes
    g.plat = head if plat else None
    return g


def mini_image(kind: str, n: int = 4, glyph_h: float = 0.18) -> VGroup:
    """A small image: a TEAL box with one row of `kind` glyphs. .frame .codes"""
    row = glyph_row(kind, n, glyph_h)
    f = box(row.width + 0.45, 0.55, IMAGE, fill_opacity=0.1, radius=0.08)
    row.move_to(f)
    g = VGroup(f, row)
    g.frame, g.codes = f, row
    return g


def emulation_box(box_w: float, box_h: float, text: str = "emulation", inside: bool = False) -> VGroup:
    """The GREY emulation box (opaque: an image passing through it is hidden while it changes).
    .frame .text (above the box, or inside it with inside=True)"""
    f = box(box_w, box_h, LAPTOP, fill=S.GREY_DARKER, fill_opacity=0.96)
    t = label(text, 20, LAPTOP)
    if inside:
        t.move_to(f)
    else:
        t.next_to(f, UP, buff=0.1)
    g = VGroup(f, t)
    g.frame, g.text = f, t
    return g


def no_emulator(slot_w: float = 0.85, slot_h: float = 0.6) -> VGroup:
    """The VM's empty, dashed GREY slot with the label 'no emulator' under it. .slot .text"""
    s = outline_box(slot_w, slot_h, LAPTOP)
    t = label("no emulator", 20, LAPTOP).next_to(s, DOWN, buff=0.1)
    g = VGroup(s, t)
    g.slot, g.text = s, t
    return g


def note_lines(*lines, size: float = 22, color=LAPTOP) -> VGroup:
    return VGroup(*[label(s, size, color) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)


def on_frame(t, mob, right: float = 0.3, left: float | None = None):
    """Put `mob` on terminal t's top edge, right-aligned `right` inside its right edge (or
    left-aligned `left` inside its left edge)."""
    if left is not None:
        return mob.move_to([t.box.get_left()[0] + left + mob.width / 2, t.box.get_top()[1], 0])
    return mob.move_to([t.box.get_right()[0] - right - mob.width / 2, t.box.get_top()[1], 0])


def fix_chip(lines, size: float = 20, pad_y: float = 0.32) -> VGroup:
    """A GREEN text chip of commands (not run): mono_lines in a GREEN box (pad_y above and below, so tags
    on its top edge clear the first line). .frame .lines .first (a frame around the first line only, its
    top edge on .frame's: the chip can start with one line and grow)"""
    ls = VGroup(*[mono_line(s, size, INK) for s in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    f = box(ls.width + 0.6, ls.height + 2 * pad_y, VENV, fill_opacity=0.1)
    ls.move_to(f)
    first = box(f.width, ls[0].height + 2 * pad_y, VENV, fill_opacity=0.1)
    first.move_to([f.get_x(), f.get_top()[1] - first.height / 2, 0])   # not in the group: re-place it after moving g
    g = VGroup(f, ls)
    g.frame, g.lines, g.first = f, ls, first
    return g


def cmd_row(cmd: str, note, size: float = 20) -> VGroup:
    """A GREEN mono chip and its GREY note (a string, or a VGroup of lines). .chip .note"""
    c = chip(cmd, VENV, size=size, font=MONO, fill_opacity=0.12)
    n = label(note, size, LAPTOP) if isinstance(note, str) else note
    g = VGroup(c, n)
    g.chip, g.note = c, n
    return g


# ------------------------------------------------------------------ the scene
class Platforms(VoiceScene):
    def construct(self):
        assert len(SAY) == 10, f"S13 has {len(SAY)} SAY lines; this scene times 10"

        # ========================================================== 0 · uname + the image's platform
        tr = tracker_b(4)
        t = laptop_term(6)

        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=DOWN * 0.1), FadeIn(t), run_time=0.6)
            bare_prompt(self, t)
            t.fold = lambda text, first_prefix=0: list(UNAME_ROWS)
            c0 = type_cmd(self, t, UNAME, 1.5)
            del t.fold
            assert [r.text for r in c0.rows] == UNAME_ROWS, [r.text for r in c0.rows]
            vo.wait_until("this scene is all extras")
            x0 = beside(row_tag("extra"), c0.rows[-1])
            self.play(track(tr, 4, extra=True), FadeIn(x0, shift=LEFT * 0.1), run_time=0.5)
            attach(self, c0.rows[-1], x0)
            out0 = t.print(self, OUT35, run_time=0.4)
            bare_prompt(self, t)
            tag_m = row_tag("this machine · Intel/AMD", AMD)
            tag_i = row_tag("the image", AMD)
            x_tags = max(r.strut.get_right()[0] for r in out0) + 0.45
            for tg, r in zip((tag_m, tag_i), out0):
                tg.move_to([x_tags + tg.width / 2, r.strut.get_center()[1], 0])
            vo.wait_until("Our machine is Intel or AMD")
            self.play(out0[0].glyphs.animate.set_color(AMD), FadeIn(tag_m, shift=LEFT * 0.1), run_time=0.5)
            attach(self, out0[0], tag_m)
            self.play(Indicate(out0[0].glyphs, color=AMD, scale_factor=1.2), run_time=0.6)
            self.add(out0[0])
            vo.wait_until("and the image says")
            self.play(out0[1].glyphs.animate.set_color(AMD), FadeIn(tag_i, shift=LEFT * 0.1), run_time=0.5)
            attach(self, out0[1], tag_i)
            self.play(Indicate(out0[1].glyphs, color=AMD, scale_factor=1.15), run_time=0.6)
            self.add(out0[1])
            br = Brace(VGroup(tag_m, tag_i), RIGHT, color=LAPTOP, buff=0.15)
            mac = label("Apple Silicon Mac: arm64", 22, LAPTOP).next_to(br, RIGHT, buff=0.2)
            vo.wait_until("On an Apple Silicon Mac")
            self.play(GrowFromCenter(br), FadeIn(mac, shift=LEFT * 0.15), run_time=0.6)

        # ========================================================== 1 · V7: machine code for one kind of CPU
        chip_a = platform_chip("arm64").move_to([XA, CHIP_Y, 0])
        chip_b = platform_chip("amd64").move_to([XB, CHIP_Y, 0])
        lap_a = laptop(2.4, LAPTOP).move_to([XA, MACH_Y, 0])
        vm_b = vm_glyph(1.6).move_to([XB, MACH_Y, 0])
        instr = label("← machine instructions →", 20, LAPTOP)
        instr.move_to([(chip_a.glyphs.get_right()[0] + chip_b.glyphs.get_left()[0]) / 2, chip_a.glyphs.get_y(), 0])
        img = image_card("amd64").move_to([0, 1.72, 0])
        img_land = np.array([XB, chip_b.get_top()[1] + 0.22 + img.height / 2, 0])
        ok1 = check_mark(0.45, VENV).move_to(img_land + RIGHT * (img.width / 2 + 0.45))
        note1 = note_lines("runs directly on the CPU", "unless an emulator steps in")
        note1.move_to([-3.55, 1.3, 0])
        dd = label("Docker Desktop", 20, INK)
        emu_a = emulation_box(1.6, 0.46, "emulator", inside=True)
        VGroup(dd, emu_a).arrange(DOWN, buff=0.1).move_to(lap_a.screen)
        noemu_b = no_emulator().move_to([XB + 1.7, MACH_Y + 0.1, 0])

        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(t), FadeOut(VGroup(br, mac)), run_time=0.5)
            self.remove(*t.get_family())
            self.play(LaggedStart(FadeIn(VGroup(chip_a, lap_a), shift=UP * 0.15),
                                  FadeIn(VGroup(chip_b, vm_b), shift=UP * 0.15), lag_ratio=0.35),
                      FadeIn(instr), run_time=0.9)
            vo.wait_until("Every program in an image")
            self.play(Create(img.frame), FadeIn(img.head, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("bash, Python, uv")
            self.play(LaggedStart(*[Write(nm) for nm in img.names], lag_ratio=0.4), run_time=1.2)
            vo.wait_until("is machine code")
            self.play(LaggedStart(*[LaggedStart(*[GrowFromCenter(g) for g in row], lag_ratio=0.2) for row in img.codes],
                                  lag_ratio=0.3), run_time=1.4)
            vo.wait_until("amd64 for Intel and AMD")
            self.play(Indicate(chip_b.glyphs, color=AMD, scale_factor=1.25), Indicate(chip_b.chip, color=AMD, scale_factor=1.06),
                      Indicate(img.codes, color=AMD, scale_factor=1.1), run_time=0.9)
            vo.wait_until("arm64 for Apple Silicon")
            self.play(Indicate(chip_a.glyphs, color=INK, scale_factor=1.25), Indicate(chip_a.chip, color=INK, scale_factor=1.06),
                      run_time=0.9)
            vo.wait_until("A container's programs")
            self.play(img.animate.move_to(img_land), run_time=1.0)
            ghost = VGroup(*[g.copy() for g in chip_b.glyphs[:len(img.codes[0])]])
            self.play(ghost.animate.move_to(img.codes[0]), run_time=0.6)
            self.play(Indicate(VGroup(ghost, img.codes[0]), color=VENV, scale_factor=1.15), Create(ok1), run_time=0.6)
            self.play(FadeOut(ghost), run_time=0.3)
            vo.wait_until("so unless an emulator steps in")
            self.play(FadeIn(note1[0], shift=RIGHT * 0.1), run_time=0.4)
            self.play(FadeIn(note1[1], shift=RIGHT * 0.1), run_time=0.4)
            vo.wait_until("the CPU must speak")
            self.play(Indicate(img.codes, color=AMD, scale_factor=1.1), Indicate(chip_b.glyphs, color=AMD, scale_factor=1.2),
                      run_time=0.8)
            vo.wait_until("Docker Desktop has one built in")
            self.play(FadeIn(dd), FadeIn(emu_a, scale=0.7), run_time=0.6)
            self.play(Indicate(emu_a, color=INK, scale_factor=1.12), run_time=0.6)
            vo.wait_until("a plain Linux VM doesn't")
            self.play(Create(noemu_b.slot), FadeIn(noemu_b.text, shift=UP * 0.1), run_time=0.6)
        pic1 = VGroup(chip_a, chip_b, lap_a, vm_b, instr, img, ok1, note1, dd, emu_a, noemu_b)

        # ========================================================== 2 · python:3.12-slim-bookworm is a menu
        t2 = laptop_term(13)
        att_x = 2.75                                     # the attestation column, right of the row's left edge
        menu = PlatformMenu("python:3.12-slim-bookworm",
                            [("linux/amd64", AMD), ("linux/arm/v7", INK), ("linux/arm64/v8", ARM),
                             ("linux/386", INK), ("linux/ppc64le", INK)],
                            menu_w=0.3 + att_x + mono("+ attestation", 20).width + 0.35)
        menu.move_to([-1.85, 0.72, 0])
        atts = VGroup()
        for r in menu.rows:
            a = mono("+ attestation", 20, LAPTOP).set_opacity(0.6)
            a.move_to([menu.rows.get_left()[0] + att_x + a.width / 2, r.get_y(), 0])
            atts.add(a)
        vm2 = vm_glyph(1.3)
        mk0 = menu.mark(0, AMD)

        with self.voiceover(SAY[2]) as vo:
            self.play(FadeOut(pic1), run_time=0.5)
            self.play(FadeIn(t2), run_time=0.3)
            bare_prompt(self, t2)
            c2 = type_cmd(self, t2, PY_CMD, 1.0)
            x2 = beside(row_tag("extra"), c2.rows[-1])
            self.play(FadeIn(x2, shift=LEFT * 0.1), run_time=0.25)
            attach(self, c2.rows[-1], x2)
            out2 = t2.print(self, OUT11, run_time=0.6, lag=0.08)
            idx_row = out2[1]
            plat_rows = [out2[i] for i in (2, 4, 6, 8, 10)]
            assert [r.text.split()[-1] for r in plat_rows] == PLATS
            subs = [substring(r, p) for r, p in zip(plat_rows, PLATS)]
            vo.wait_until("This python tag lists five platforms")
            self.play(*[s.animate.set_color(TURN) for s in subs], run_time=0.4)
            self.add(*plat_rows)
            ghosts = [s.copy() for s in subs]
            self.add(*ghosts)
            resize(self, t2, STRIP_ROWS, keep=[*c2.rows, idx_row], run_time=0.8,
                   extra=[Transform(g, m.copy().set_color(TURN)) for g, m in zip(ghosts, menu.rows)])
            self.play(FadeIn(VGroup(menu.frame, menu.sep, menu.title)), FadeIn(atts),
                      *[ReplacementTransform(g, m) for g, m in zip(ghosts, menu.rows)], run_time=0.5)
            self.add(menu)
            idx = substring(idx_row, "index")
            u_idx = under(idx, IMAGE)
            t_idx = beside(row_tag("index = a menu", IMAGE), idx_row)
            self.play(idx.animate.set_color(IMAGE), Create(u_idx), FadeIn(t_idx, shift=LEFT * 0.1), run_time=0.5)
            self.add(idx_row)
            attach(self, idx_row, u_idx)
            attach(self, idx_row, t_idx)
            vo.wait_until("amd64, two kinds of arm")
            self.play(Indicate(menu.rows[0], color=AMD, scale_factor=1.15), run_time=0.6)
            vo.wait_until("two kinds of arm")
            self.play(Indicate(menu.rows[1], color=INK, scale_factor=1.15),
                      Indicate(menu.rows[2], color=INK, scale_factor=1.15), run_time=0.7)
            vo.wait_until("and two rarer ones")
            self.play(Indicate(menu.rows[3], color=INK, scale_factor=1.15),
                      Indicate(menu.rows[4], color=INK, scale_factor=1.15), run_time=0.7)
            vo.wait_until("Docker pulls the row")
            vm2.move_to([menu.frame.get_right()[0] + 2.3, menu.rows[0].get_y(), 0])
            arr2 = Arrow(vm2.get_left() + LEFT * 0.1, [menu.frame.get_right()[0] + 0.1, menu.rows[0].get_y(), 0],
                         buff=0, color=AMD, stroke_width=4, tip_length=0.2)
            self.play(FadeIn(vm2, shift=LEFT * 0.2), run_time=0.4)
            self.play(GrowArrow(arr2), Create(mk0), run_time=0.6)
            self.play(Indicate(menu.rows[0], color=AMD, scale_factor=1.2), run_time=0.6)

        # ========================================================== 3 · dlops/simple-translate: one image
        vm3 = vm_glyph(0.9)
        on_vm = label("image inspect on the VM:", 20, LAPTOP)
        vm_chip = chip(VM_PLAT, LAPTOP, size=22, font=MONO)
        g3 = VGroup(vm3, on_vm, vm_chip).arrange(RIGHT, buff=0.25)

        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(menu, atts, vm2, arr2, mk0)), run_time=0.4)
            resize(self, t2, 8, run_time=0.5)
            bare_prompt(self, t2)
            c3 = type_cmd(self, t2, DL_CMD, 0.9)
            x3 = beside(row_tag("extra"), c3.rows[-1])
            self.play(FadeIn(x3, shift=LEFT * 0.1), run_time=0.25)
            attach(self, c3.rows[-1], x3)
            out3 = t2.print(self, OUT10, run_time=0.4)
            g3.move_to([2.6, t2.box.get_top()[1] + 0.75, 0])
            vo.wait_until("is no menu")
            mf = substring(out3[1], "manifest.v2+json")
            u3 = under(mf, TURN)
            t3 = beside(row_tag("one image, not a menu", TURN), out3[2])
            self.play(mf.animate.set_color(TURN), Create(u3), FadeIn(t3, shift=LEFT * 0.1), run_time=0.5)
            self.add(out3[1])
            attach(self, out3[1], u3)
            attach(self, out3[2], t3)
            self.play(Indicate(VGroup(mf, u3), color=TURN, scale_factor=1.06), run_time=0.6)
            self.add(out3[1])
            vo.wait_until("one image, amd64 only")
            self.play(FadeIn(vm3, shift=RIGHT * 0.1), FadeIn(on_vm), FadeIn(vm_chip, scale=1.1), run_time=0.5)
            self.play(Indicate(vm_chip, color=AMD, scale_factor=1.12), run_time=0.6)

        # ========================================================== 4 · our stand-in push: a small menu
        sit = stand_in_tag(size=20)
        menu4 = PlatformMenu("x", [("linux/amd64", AMD), ("unknown/unknown", None)])
        menu4.remove(menu4.title)
        ttl4 = label("our push", 22, IMAGE).move_to(menu4.title, aligned_edge=LEFT)
        menu4.title = ttl4
        menu4.add(ttl4)
        menu4.move_to([-4.1, 0.85, 0])
        att4 = label("attestation · how it was built", 22, LAPTOP)
        att4.move_to([menu4.frame.get_right()[0] + 0.35 + att4.width / 2, menu4.rows[1].get_y(), 0])
        mac4_t = VGroup(label("built on a Mac:", 22, LAPTOP), mono("linux/arm64", 22, LAPTOP)).arrange(RIGHT, buff=0.15)
        mac4_t.move_to([menu4.frame.get_right()[0] + 0.35 + mac4_t.width / 2, menu4.rows[0].get_y(), 0])
        m0 = menu4.mark(0, LAPTOP)
        mac4_b = DashedVMobject(m0, num_dashes=36, dashed_ratio=0.55).set_stroke(LAPTOP, 2.5)
        cd4 = label("containerd image store · the older store pushes one image, no menu", 20, LAPTOP)
        cd4.move_to([menu4.frame.get_left()[0] + cd4.width / 2, menu4.frame.get_bottom()[1] - 0.42, 0])

        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(g3), run_time=0.3)
            t2.clear(self, run_time=0.25)
            on_frame(t2, sit, right=0.12)
            self.play(FadeIn(sit, shift=DOWN * 0.1), run_time=0.3)
            bare_prompt(self, t2)
            c4 = type_cmd(self, t2, SI_CMD, 1.0)
            x4 = beside(row_tag("extra"), c4.rows[-1])
            self.play(FadeIn(x4, shift=LEFT * 0.1), run_time=0.25)
            attach(self, c4.rows[-1], x4)
            out4 = t2.print(self, OUT09, run_time=0.4)
            p4 = [substring(out4[1], "linux/amd64"), substring(out4[2], "unknown/unknown")]
            ghosts4 = [s.copy() for s in p4]
            self.add(*ghosts4)
            vo.wait_until("is a small menu")
            resize(self, t2, STRIP_ROWS, keep=[*c4.rows, out4[0]], run_time=0.7,
                   extra=[sit.animate.shift(DOWN * (8 - STRIP_ROWS) * t2.pitch),
                          *[Transform(g, m.copy()) for g, m in zip(ghosts4, menu4.rows)]])
            self.play(FadeIn(VGroup(menu4.frame, menu4.sep, menu4.title)), run_time=0.4)
            self.remove(*ghosts4)
            self.add(menu4)
            vo.wait_until("amd64, plus an attestation")
            self.play(Indicate(menu4.rows[0], color=AMD, scale_factor=1.2), run_time=0.5)
            vo.wait_until("plus an attestation")
            self.play(FadeIn(att4, shift=LEFT * 0.15), menu4.rows[1].animate.set_opacity(1), run_time=0.5)
            self.play(menu4.rows[1].animate.set_opacity(0.6), run_time=0.3)
            vo.wait_until("a record of how")
            self.play(Create(mac4_b), FadeIn(mac4_t, shift=LEFT * 0.1), run_time=0.6)
            self.play(FadeIn(cd4, shift=UP * 0.1), run_time=0.5)
        self.wait(3.0)                    # neither note is narrated: time to read them before the picture goes

        # ========================================================== 5 · built on a Mac, pushed, pulled on a VM
        # top band (the ponder card takes the bottom half): Mac | Docker Hub | VM. Pushing and pulling copy
        # the image, so each station keeps one and the PINK routes always join two images.
        img5 = image_card("arm64", plat="arm64", names=None, n=4, glyph_h=0.17, pitch=0.27)
        st_mac = np.array([-2.75, 1.55, 0])                  # the image's three stations
        lap5 = laptop(1.5, LAPTOP).move_to([-4.85, 0.85, 0])
        chip5a = platform_chip("arm64", "arm64 · Mac", n=5).move_to([-4.85, 2.12, 0])
        shelf5 = shelf_glyph(1.2).move_to([-0.1, 0.8, 0])
        hub5 = label("Docker Hub", 20, CLOUD).next_to(shelf5, DOWN, buff=0.1)
        st_hub = np.array([shelf5.get_x(), shelf5.get_top()[1] + 0.08 + img5.height / 2, 0])
        chip5b = platform_chip("amd64", "amd64 · default VM", n=5).move_to([5.1, 1.55, 0])
        vm5 = vm_glyph(1.3).move_to([5.1, 2.8, 0])
        st_vm = np.array([2.75, 1.55, 0])
        noemu5 = VGroup(outline_box(0.85, 0.45, LAPTOP), label("no emulator", 20, LAPTOP)).arrange(RIGHT, buff=0.15)
        noemu5.slot, noemu5.text = noemu5[0], noemu5[1]
        noemu5.move_to([chip5b.get_left()[0] + 0.1 + noemu5.width / 2, 0.42, 0])
        img5.move_to(st_mac)
        hw = img5.width / 2 + 0.08
        draw_push = route(st_mac + RIGHT * hw, st_hub + LEFT * hw, arc=-0.5)
        draw_pull = route(st_hub + RIGHT * hw, st_vm + LEFT * hw, arc=-0.5)
        img_hub, img_vm = img5.copy(), img5.copy()

        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(t2), FadeOut(sit), FadeOut(VGroup(menu4, att4, mac4_t, mac4_b, cd4)), run_time=0.5)
            self.remove(*t2.get_family())
            vo.wait_until("You built on an M-series Mac")
            self.play(FadeIn(VGroup(chip5a, lap5), shift=UP * 0.15), run_time=0.5)
            self.play(Create(img5.frame), FadeIn(img5.head),
                      LaggedStart(*[LaggedStart(*[GrowFromCenter(g) for g in row], lag_ratio=0.2) for row in img5.codes],
                                  lag_ratio=0.25), run_time=1.0)
            vo.wait_until("and pushed")
            self.play(FadeIn(VGroup(shelf5, hub5), shift=DOWN * 0.1), run_time=0.4)
            self.play(GrowArrow(draw_push), MoveAlongPath(img_hub, ArcBetweenPoints(st_mac, st_hub, angle=-0.5)),
                      run_time=0.9)
            vo.wait_until("Your VM is an ordinary")
            self.play(FadeIn(VGroup(vm5, chip5b), shift=DOWN * 0.15), run_time=0.5)
            self.play(Create(noemu5.slot), FadeIn(noemu5.text, shift=LEFT * 0.1), run_time=0.5)
            vo.wait_until("Will your image run there")
            self.play(GrowArrow(draw_pull), MoveAlongPath(img_vm, ArcBetweenPoints(st_hub, st_vm, angle=-0.5)),
                      run_time=1.0)

        q = ponder_card(PONDER_Q)
        q.move_to([0, -3.45 + q.height / 2, 0])
        self.play(FadeIn(q, scale=0.95), run_time=0.6)
        bar = q[3]
        self.play(bar.animate(rate_func=linear).become(bar.copy().scale(0.001, about_point=bar.get_start())),
                  run_time=8)

        # ========================================================== 6 · No: exec format error
        no = cross_mark(0.45, ERR).next_to(q[1], RIGHT, buff=0.3)
        ask = chip("amd64?", AMD, size=20, font=MONO)
        ask_home = vm5.get_left() + LEFT * (0.15 + ask.width / 2)
        ask_at = np.array([st_vm[0], img_vm.get_top()[1] + 0.12 + ask.height / 2, 0])
        ask.move_to(ask_home)
        x_img = cross_mark(0.5, ERR).move_to(img_vm.codes)
        nothing = label("nothing it can run", 20, ERR).move_to(ask_at)
        nm6 = label("no matching manifest", 20, LAPTOP).move_to(ask_at)
        t6 = laptop_term(5)
        tg6 = row_tag("extra · arm64 image on an amd64 machine")
        tg6.move_to([t6.box.get_right()[0] - tg6.width / 2, t6.box.get_top()[1] + 0.12 + tg6.height / 2, 0])
        de6 = row_tag("no emulator here · Docker Desktop would run it")
        de6.move_to([t6.box.get_left()[0] + de6.width / 2, tg6.get_y(), 0])

        with self.voiceover(SAY[6]) as vo:
            self.play(Create(no), run_time=0.3)
            self.play(FadeOut(VGroup(q, no)), FadeIn(ask, shift=LEFT * 0.1), run_time=0.4)
            self.play(ask.animate.move_to(ask_at), run_time=0.5)
            self.play(img_vm.head.animate.set_color(ERR), img_vm.frame.animate.set_stroke(ERR), Create(x_img), run_time=0.4)
            self.play(ask.animate.move_to(ask_home), run_time=0.35)
            self.play(FadeOut(ask), run_time=0.15)
            self.play(FadeIn(nothing, shift=UP * 0.1), run_time=0.3)
            vo.wait_until("Here's the same failure")
            self.play(FadeIn(t6), FadeIn(tg6, shift=DOWN * 0.1), run_time=0.4)
            bare_prompt(self, t6)
            c6 = type_cmd(self, t6, ARM_CMD, 1.1)
            out6 = t6.print(self, [*OUT12[:-1], (ERR_LINE, ERR)], run_time=0.5, lag=0.12)
            err_row = out6[-1]
            vo.wait_until("exec format error")
            ef = substring(err_row, "exec format error")
            u6 = under(ef, ERR)
            self.play(Create(u6), Indicate(ef, color=ERR, scale_factor=1.12), run_time=0.7)
            self.add(err_row)
            attach(self, err_row, u6)
            vo.wait_until("Docker Desktop would just run it")
            self.play(FadeIn(de6, shift=DOWN * 0.1), run_time=0.4)
            self.play(Indicate(de6, color=INK, scale_factor=1.06), run_time=0.6)
            vo.wait_until("A Mac-built image on a default VM")
            resize(self, t6, STRIP_ROWS, keep=[*c6.rows, err_row], run_time=0.6,
                   extra=[VGroup(tg6, de6).animate.shift(DOWN * (5 - STRIP_ROWS) * t6.pitch)])
            vo.wait_until("fails like this")
            self.play(Indicate(x_img, color=ERR, scale_factor=1.3), Indicate(err_row.glyphs, color=ERR, scale_factor=1.05),
                      Indicate(nothing, color=ERR, scale_factor=1.1), run_time=0.8)
            self.add(err_row)
            vo.wait_until("or with no matching manifest")
            # the VM's order bounces off the image, and the refusal's words land where it hit
            ask.move_to(ask_home)
            self.play(FadeOut(nothing), FadeIn(ask, shift=LEFT * 0.1), run_time=0.25)
            self.play(ask.animate.move_to(ask_at), run_time=0.35)
            self.play(ask.animate.move_to(ask_home).set_opacity(0), FadeIn(nm6, shift=UP * 0.1), run_time=0.45)
            self.remove(ask)
        self.wait(0.6)

        # ========================================================== 7 · fix 1: --platform=linux/amd64
        pic5 = VGroup(chip5a, lap5, img5, img_hub, img_vm, shelf5, hub5, vm5, chip5b, noemu5, draw_push, draw_pull, x_img,
                      nm6)
        fx = fix_chip([FIX1, TAG_README, PUSH_README])
        fx.move_to([0, -3.45 + fx.height / 2, 0])
        fx.first.align_to(fx.frame, UP).set_x(fx.frame.get_x())     # .first is not in the group: place it too
        nr = row_tag("not run here")
        nr.move_to([fx.frame.get_right()[0] - 0.3 - nr.width / 2, fx.frame.get_top()[1], 0])
        fix1 = row_tag("fix 1")
        fix1.move_to([fx.frame.get_left()[0] + 0.3 + fix1.width / 2, fx.frame.get_top()[1], 0])
        two = label("two fixes · neither in the README", 30, LAPTOP).move_to([0, 0.9, 0])
        users = [substring(fx.lines[k], "<USER NAME>") for k in (1, 2)]
        p7 = code("docker-shell.sh", 11, 12)
        p7.move_to([0, 2.62 - p7.height / 2, 0])        # clear of the tracker's caption (its bottom is 2.9)
        bar12 = line_bar(p7.code, 1, TURN, 0.2)
        co7 = tag("commented out · not in the README", LAPTOP, size=20)
        co7.move_to([p7.code.get_right()[0] - 0.2 - co7.width / 2, p7.header.get_y(), 0])
        flag12 = code_span(p7.code, 1, PLAT_FLAG)
        u12 = under(flag12, AMD)
        pipe_y = (p7.get_bottom()[1] + fx.get_top()[1]) / 2 - 0.1
        chip7 = platform_chip("arm64").move_to([-4.85, pipe_y, 0])
        img7 = image_card("arm64", plat="linux/arm64", names=None, n=5, glyph_h=0.17, pitch=0.27)
        img7.move_to([-1.95, pipe_y, 0])
        emu7 = emulation_box(2.6, img7.height + 0.2, inside=True)
        emu7.move_to([0.95, pipe_y, 0])
        end7 = np.array([3.9, pipe_y, 0])
        slow7 = label("slower, but it works", 20, LAPTOP).next_to(emu7.frame, UP, buff=0.12)
        ok7 = check_mark(0.45, VENV).move_to(end7 + RIGHT * (img7.width / 2 + 0.45))
        # the chip starts mid-frame as a one-line chip (its first line is the whole story until "On a Mac"), moves
        # down to the positions above when the picture needs the room, and grows to three lines at "Then tag and
        # push again" (its lines 2-3 wait at the bottom, off-screen)
        lift = -0.1 - fx.first.get_y()
        fx_up = VGroup(fx.first, fx.lines[0], nr, fix1).shift(UP * lift)
        flag = substring(fx.lines[0], PLAT_FLAG)
        lin = substring(fx.lines[0], "linux/amd64")
        u_flag = under(flag, AMD)
        fx_up.add(u_flag)

        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(pic5), FadeOut(t6), FadeOut(VGroup(tg6, de6)), run_time=0.6)
            self.remove(*t6.get_family())
            self.play(FadeIn(two, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("One: build for the VM's platform")
            self.play(FadeOut(two, shift=UP * 0.3), FadeIn(fx.first), FadeIn(fix1, shift=DOWN * 0.1),
                      FadeIn(nr, shift=DOWN * 0.1), run_time=0.5)
            self.play(ShowIncreasingSubsets(fx.lines[0].glyphs, rate_func=linear), run_time=1.2)
            self.add(fx.lines[0])
            vo.wait_until("with the flag dash dash platform")
            self.play(flag.animate.set_color(AMD), Create(u_flag), run_time=0.5)
            self.add(fx.lines[0])
            vo.wait_until("equals linux slash amd64")
            self.play(Circumscribe(lin, color=TURN, buff=0.06, stroke_width=3), run_time=0.9)
            vo.wait_until("It's the commented-out line 12")
            self.play(FadeIn(p7, shift=DOWN * 0.15), run_time=0.5)
            self.play(FadeIn(bar12), FadeIn(co7, shift=LEFT * 0.1), run_time=0.4)
            # the same flag: the chip's underline is copied up onto line 12
            self.play(TransformFromCopy(u_flag, u12), run_time=0.7)
            vo.wait_until("On a Mac, it runs emulated")
            self.play(fx_up.animate.shift(DOWN * lift), run_time=0.6)
            self.play(FadeIn(chip7, shift=UP * 0.1), FadeIn(emu7), run_time=0.4)
            self.add(img7)
            self.bring_to_front(emu7)
            self.play(Create(img7.frame), FadeIn(img7.head),
                      LaggedStart(*[GrowFromCenter(g) for row in img7.codes for g in row], lag_ratio=0.05), run_time=0.6)
            self.play(img7.animate.move_to(emu7.frame.get_center()), run_time=0.6)
            for r in img7.codes:                         # inside the (opaque) box: arm64 -> amd64
                r.become(glyph_row("amd64", len(r), 0.17).move_to(r))
            img7.head.become(steady("linux/amd64", 20, AMD, mono_font=True).move_to(img7.head, aligned_edge=LEFT))
            self.play(Indicate(emu7.frame, color=INK, scale_factor=1.04), run_time=0.4)
            self.play(img7.animate.move_to(end7), run_time=0.7)
            vo.wait_until("slower, but it works")
            self.play(FadeIn(slow7, shift=DOWN * 0.1), Create(ok7), run_time=0.5)
            vo.wait_until("Then tag and push again")
            self.play(ReplacementTransform(fx.first, fx.frame),
                      LaggedStart(FadeIn(fx.lines[1], shift=UP * 0.1), FadeIn(fx.lines[2], shift=UP * 0.1), lag_ratio=0.4),
                      run_time=0.8)
            self.add(fx.lines, u_flag, nr, fix1)         # the grown frame was added on top: text and edge tags over it
            self.play(*[u.animate.set_color(TURN) for u in users], run_time=0.4)
            self.add(fx.lines[1], fx.lines[2])

        # ========================================================== 8 · fix 2: buildx builds both, pushes one menu
        pic7 = VGroup(chip7, img7, emu7, slow7, ok7)
        # left to right: buildx | emulation | the two images | PINK routes | the menu (6.25 wide: its title is
        # the README's long name)
        bx = builder_box("buildx", 1.7, 0.85, 22)
        bx.text.become(mono("buildx", 22, TOOL).move_to(bx.frame))
        bx.move_to([-5.6, 1.85, 0])
        fix2 = row_tag("fix 2")
        fix2.move_to([bx.frame.get_left()[0] + fix2.width / 2, bx.frame.get_top()[1] + 0.12 + fix2.height / 2, 0])
        chip8 = platform_chip("arm64")
        chip8.move_to([bx.frame.get_left()[0] + chip8.width / 2, 0.52, 0])
        lane_up, lane_lo = 2.35, 1.0
        emu8 = emulation_box(1.5, 0.6, inside=True).move_to([-3.4, lane_up, 0])
        mi_amd = mini_image("amd64", 3).move_to([-1.45, lane_up, 0])     # room for PINK routes of ~0.8 to the menu
        mi_arm = mini_image("arm64", 3).move_to([-1.45, lane_lo, 0])
        a_up = Arrow(bx.frame.get_right() + UP * 0.15, emu8.frame.get_left(), buff=0.08, color=LAPTOP, stroke_width=3,
                     tip_length=0.18)
        a_up2 = Arrow(emu8.frame.get_right(), mi_amd.get_left(), buff=0.08, color=LAPTOP, stroke_width=3, tip_length=0.18)
        a_lo = Arrow(bx.frame.get_right() + DOWN * 0.15, mi_arm.get_left(), buff=0.08, color=LAPTOP, stroke_width=3,
                     tip_length=0.18)
        # the viewer's own image after beat 9's edit (lines 7 and 11), not dlops/simple-translate: beat 3 showed
        # that one is a single amd64 image
        name8 = PUSH_README.removeprefix("docker push ")
        assert name8 == "<USER NAME>/simple-translate-ac215", name8
        menu8 = PlatformMenu(name8, [("linux/amd64", AMD), ("linux/arm64", ARM)])
        n_user = len("<USER NAME>".replace(" ", ""))   # Text glyphs skip spaces
        assert len(menu8.title) == len(name8.replace(" ", "")), len(menu8.title)
        menu8.title[:n_user].set_color(TURN)
        menu8.move_to([6.4 - menu8.frame.width / 2, 1.72, 0])
        assert menu8.frame.get_left()[0] - mi_amd.get_right()[0] > 0.7, "no room for the PINK routes"
        board8 = Line(menu8.frame.get_corner(DL) + np.array([-0.15, -0.1, 0]),
                      menu8.frame.get_corner(DR) + np.array([0.12, -0.1, 0]), color=CLOUD, stroke_width=4)
        hub8 = label("Docker Hub", 20, CLOUD).next_to(board8, DOWN, buff=0.1).align_to(board8, RIGHT)
        r_amd = route(mi_amd.get_right() + RIGHT * 0.1, np.array([menu8.frame.get_left()[0] - 0.08, menu8.rows[0].get_y(), 0]),
                      arc=-0.3)
        r_arm = route(mi_arm.get_right() + RIGHT * 0.1, np.array([menu8.frame.get_left()[0] - 0.08, menu8.rows[1].get_y(), 0]),
                      arc=0.3)
        p8 = code_panel(SRC_21_27, "docker-build-push.sh", 21, "bash", font_size=20)
        p8.move_to([0, -3.45 + p8.height / 2, 0])
        bar23 = line_bar(p8.code, 2, TURN, 0.2)
        bar27 = line_bar(p8.code, 6, TURN, 0.2)
        err8 = VGroup(erratum_tag(), label("would push both · the published image has only amd64", 20, LAPTOP))
        err8.arrange(RIGHT, buff=0.2)
        err8.move_to([6.4 - err8.width / 2, (hub8.get_bottom()[1] + p8.get_top()[1]) / 2, 0])

        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(p7, bar12, co7, u12)), FadeOut(VGroup(fx, u_flag, nr, fix1)), FadeOut(pic7), run_time=0.4)
            self.play(FadeIn(bx, shift=DOWN * 0.1), FadeIn(fix2, shift=DOWN * 0.1), FadeIn(chip8, shift=UP * 0.1),
                      run_time=0.4)
            vo.wait_until("uses buildx")
            self.play(Indicate(bx, color=TOOL, scale_factor=1.1), run_time=0.5)
            vo.wait_until("Docker's multi-platform builder")
            self.play(GrowArrow(a_lo), GrowArrow(a_up), FadeIn(emu8), run_time=0.5)
            self.play(GrowArrow(a_up2), FadeIn(p8, shift=UP * 0.15), run_time=0.4)
            self.play(FadeIn(bar23), Indicate(code_span(p8.code, 2, "--name multi-arch"), color=TURN, scale_factor=1.06),
                      run_time=0.5)
            vo.wait_until("to build both")
            self.play(GrowFromCenter(mi_arm), GrowFromCenter(mi_amd), Indicate(emu8.frame, color=INK, scale_factor=1.06),
                      FadeIn(bar27), run_time=0.6)
            vo.wait_until("and push one menu")
            self.play(FadeIn(VGroup(menu8.frame, menu8.sep, menu8.title)), Create(board8), FadeIn(hub8),
                      GrowArrow(r_amd), GrowArrow(r_arm), run_time=0.4)
            # each image rides its route and becomes its row of the menu
            riders = [mi_amd.copy(), mi_arm.copy()]
            self.play(FadeTransform(riders[0], menu8.rows[0], path_arc=-0.3),
                      FadeTransform(riders[1], menu8.rows[1], path_arc=0.3),
                      Indicate(code_span(p8.code, 6, "--platform linux/amd64,linux/arm64 --push"), color=TURN,
                               scale_factor=1.06), run_time=0.9)
            self.add(menu8)
            self.play(FadeIn(err8, shift=LEFT * 0.1), run_time=0.4)
        self.wait(3.0)                    # time to read line 27 and the erratum before the panel changes

        # ========================================================== 9 · DOCKER_USERNAME, IMAGE_NAME, bash, buildx use default
        pic8 = VGroup(bx, fix2, chip8, emu8, mi_amd, mi_arm, a_up, a_up2, a_lo, menu8, board8, hub8, r_amd, r_arm)
        p9 = code("docker-build-push.sh", 7, 11, focus=[0, 4])
        p9.move_to([0, 2.62 - p9.height / 2, 0])         # clear of the tracker caption
        bar7 = line_bar(p9.code, 0, TURN, 0.2)
        bar11 = line_bar(p9.code, 4, TURN, 0.2)
        b7 = SurroundingRectangle(code_span(p9.code, 0, '"simple-translate"'), color=TURN, buff=0.06, stroke_width=3)
        b11 = SurroundingRectangle(code_span(p9.code, 4, '"dlops"'), color=TURN, buff=0.06, stroke_width=3)
        cap_u = label("your username (11)", 22, TURN)
        cap_n = VGroup(mono("simple-translate-ac215", 22, TURN), label("(7)", 22, TURN)).arrange(RIGHT, buff=0.12)
        cap = VGroup(cap_u, label("·", 22, TURN), cap_n).arrange(RIGHT, buff=0.18)
        cap.next_to(p9, DOWN, buff=0.3)
        r1 = cmd_row("docker login", "first")
        r2 = cmd_row("bash docker-build-push.sh", "the script isn't executable")
        n3 = VGroup(label("afterwards: builds land on your laptop again", 20, LAPTOP),
                    VGroup(mono("desktop-linux", 20, LAPTOP), label("on Docker Desktop", 20, LAPTOP)).arrange(RIGHT, buff=0.12))
        n3.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        r3 = cmd_row("docker buildx use default", n3)
        y = cap.get_bottom()[1] - 0.6
        for r in (r1, r2, r3):                           # each note right after its chip
            r.chip.move_to([r.chip.width / 2, y, 0])
            r.note.move_to([r.chip.get_right()[0] + 0.3 + r.note.width / 2, y, 0])
            if r is r3:
                r.note.align_to(r.chip, UP).shift(UP * 0.02)
            y -= 0.78
        rows9 = VGroup(r1, r2, r3)
        rows9.shift(RIGHT * (-rows9.width / 2 - rows9.get_left()[0]))   # the block centred under the panel

        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(pic8), FadeOut(VGroup(bar23, bar27, err8)), run_time=0.5)
            self.play(FadeTransform(p8, p9), run_time=0.8)
            vo.wait_until("Put your user name on line 11")
            self.play(FadeIn(bar11), Create(b11), FadeIn(cap_u, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("and simple-translate-ac215 on line 7")
            self.play(FadeIn(bar7), Create(b7), FadeIn(cap[1]), FadeIn(cap_n, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("the README's name")
            self.play(Circumscribe(cap_n[0], color=TURN, buff=0.06, stroke_width=3), run_time=0.8)
            vo.wait_until("Log in first")
            self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("then run it with bash")
            self.play(FadeIn(r2, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("Afterwards, switch back")
            self.play(FadeIn(r3.chip, shift=UP * 0.1), FadeIn(r3.note[0], shift=UP * 0.1), run_time=0.4)
            vo.wait_until("with docker buildx use default")
            self.play(Indicate(r3.chip, color=VENV, scale_factor=1.08), run_time=0.6)
            vo.wait_until("or desktop linux on Docker Desktop")
            self.play(FadeIn(r3.note[1], shift=UP * 0.1), run_time=0.4)
            self.play(Indicate(r3.note[1][0], color=INK, scale_factor=1.1), run_time=0.6)

        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.remove(*self.mobjects)
