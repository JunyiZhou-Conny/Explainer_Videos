r"""S11 · Build, start, read the logs (port_toy README › Step 1, steps 3–6; V7's doors and rooms).

Beats (script.md "## S11", one voiceover block each):
 0  TRACKER P1/3. CODE(port_toy/gateway/Dockerfile: 1–5) at the top, line 2 wrapped at its two
    `&&` (header "gateway/Dockerfile · lines 1–5 · line 2 wrapped"). On "almost identical" a GREY
    chip "processor/Dockerfile: the same, except line 5" under it, and the GREY lecture tag
    "Lecture 4 · slide 12" (lecture_ref, top right; SLIDES.md S11 i: the chained apt RUN) that
    stays to beat 2's first play; line 1 (FROM python:3.14-slim)
    and line 2 (apt installs curl) get ORANGE bars as they are named, line 4 (COPY . .) a GREEN
    bar; `-u` in line 5 is circled YELLOW and the GREY tag "unbuffered: prints reach docker logs
    at once" appears under it.
 1  The panel becomes the thin GREEN gateway card (right) and the chip the processor card (left):
    each card holds the five Dockerfile lines (line 2 cut after `&&`, line 5 as `CMD [… "x.py"]`),
    FROM/RUN ORANGE, COPY GREEN. A 7-row terminal `laptop` (student@laptop:~/AC215/port_toy$)
    rises under them and types `docker build -t toy-processor ./processor` (on the row under the
    long prompt) -> port-laptop/07 lines 3, 13–15, 22 (BuildKit rows, GREY time tags). The
    `[2/4] RUN apt-get …` row gets the TEAL circled 2 and a TEAL box on `[2/4]`; its time tag
    turns YELLOW and a copy `6.4s` lands beside the processor card's RUN row. `Building 7.5s`
    underlines YELLOW; on "Your first build also pulls" the GREY note "first build: Docker also
    pulls python:3.14-slim" appears on the prompt row.
 2  `docker build -t toy-gateway ./gateway` -> 08 lines 3, 13–15, 22 (the processor's rows scroll
    away). On "from the cache" both `CACHED` words turn GREEN and two GREEN `CACHED` tags fly to
    the gateway card's RUN and WORKDIR rows; on "because the two files match" GREY `=` marks
    link lines 1–4 of the two cards one by one and a GREY `≠` sits on line 5 (both file names
    flash); on "up to the copy line" both COPY rows flash with the build's `[4/4] COPY . .` row (no
    CACHED), and the GREY tag "same line · different files copied → rebuilt" lands on that row
    (QA 20:04: an identical COPY line is not a cache hit). `Building 0.3s` underlines YELLOW on
    "It's done in under a second".
 3  TRACKER P1/4. The cards go. The README's two rows are typed under the prompt
    (`docker run -d --name processor --network toynet \` / `  -e PORT=9200 toy-processor`) ->
    10 line 3 (the ID, 64 characters: it fits). On "with PORT set to 9200" (spoken while the rows
    are typed) `PORT=9200` turns PINK; the terminal shrinks to the 3-row strip;
    CODE(port_toy/processor/processor.py: 42–43) top right and V6/V7 (ToyNet: the laptop outline,
    its zone and dashed wall, the processor box, the toynet rail) above the strip; `"PORT"` in
    line 42 turns PINK as the processor box plugs into the rail. On "and no dash p" the README
    chip `README.md · line 113` "There is no -p flag" (top band). On "It listens on 9200": the
    9200 cell of the processor's port strip lifts out (TransformFromCopy) and becomes the room
    door `:9200`, which glows TEAL; `""` in line 43 is circled YELLOW with the GREY tag "every
    address of its own box" (on "inside its own box"). On "but nothing on your laptop": a dashed
    GREY ghost door on the laptop's wall, GREY note "no street door".
 4  TRACKER P1/5. Panel and chip go; the terminal grows to 7 rows while V7 rises above it; the
    README's five rows of the gateway's `docker run` are typed -> 11 line 6 (the ID). The gateway
    box appears and plugs into the rail while `-p 127.0.0.1:8090:9100` is boxed PINK, and the GREY
    lecture tag "Lecture 4 · slide 35" (lecture_ref, top right; SLIDES.md S11 i) arrives with the
    box and stays to beat 5's first play. Still above
    the 7-row terminal: on "it opens a street door" the ghost door turns into the GREY door and
    `127.0.0.1:8090` lifts off the flag onto it (TransformFromCopy); on "that leads to a room"
    the gateway's cell 9100 lifts out and becomes the room `:9100`, and the PINK map arrow runs
    from the browser through the street door into the room. The terminal then shrinks to the
    strip (the -p row and the two -e rows stay) and V7 settles above it. On "The order is": the
    README chip `README.md · lines 224–228` "IP address : host port : container port" over the
    picture, each term flashing as it is said; then, in the spoken order, `127.0.0.1`, `8090`
    and `9100` are boxed YELLOW in the flag and lift off into a legend row under the chip, each
    landing with its label ("IP address · this laptop only", "host port · street door",
    "container port · room") while its place in V7 flashes (the door's address, the door, the
    room); "this laptop only" flashes on "meaning this laptop only". The block ends with 1.5 s
    of silence (pad) so the finished legend can be read.
 5  The legend and chip go. The two -e rows of the strip turn PINK; on "the name processor, port
    9200" V7's aim (a PINK dashed arrow from the gateway to the chip `processor : 9200` on the
    rail, not sent yet) draws itself while `processor` flashes in the strip, then `9200` and the
    chip flash on "port 9200". On "Lines 13 and 14": CODE(port_toy/gateway/gateway.py: 13–14) top
    right, `"PROCESSOR_HOST"` and `"PROCESSOR_PORT"` PINK; on "the values in quotes": `"processor"`
    and `"9200"` underlined GREY (at their baseline: an underline under the descender of
    "processor" would run into line 14) and the GREY tag "defaults" on the header row above them.
 6  TRACKER P1/6. The panel goes; the terminal is cleared into 5 rows while V7 rises above it.
    `docker logs processor` -> 12 line 2 and `docker logs gateway` -> 13 line 2; on "The
    processor listens on 9200" `9200` is boxed TEAL and the processor's room flashes; "(internal
    only)" underlines GREY; on "the gateway listens on 9100" `9100` is boxed TEAL and the
    gateway's room flashes. On "Pause and start both" the terminal and V7 give way to the static
    GREY "your turn" card with the six commands as typed (the runs in their README rows), ▶ your
    turn on the card. Fade out to an empty frame.

Deviations from SHOW (and why):
- Beats 1–2: the terminal has 7 rows, not 12: the two thin cards of beat 2 need the 2.6 units
  above it (above 12 rows there are 0.7). The cards come in with beat 1 (the panel and the chip
  turn into them, "what became what"), so the processor's RUN row can take its `6.4s` there; the
  gateway build then scrolls the processor's rows away, and the cards keep the comparison (6.4s
  vs CACHED). Each build command sits on the row under the 32-character prompt (common.type_cmd),
  so a build is 7 rows. The "build step 2" badge is the circled 2 (as S06), there is no room for
  its words in the row. The cards cut line 2 after `&&` (`RUN apt-get update && …`) and elide
  line 5's middle (`CMD [… "processor.py"]`): two full-width 36-character lines don't fit side by
  side at 20 pt.
- Beats 3–6: ToyNet is squashed vertically to 0.83 (shapes only, every text and glyph keeps its
  size and aspect) so that a 2-line code panel (1.55 units at 20 pt), the picture and the 3-row
  strip fit together; Piece.rescale shrinks the boxes horizontally too, and their texts then
  collide. Only the parts this scene explains are shown (no phone book, no second door, no
  outside machines); the gateway box is hidden until its `docker run` (it doesn't exist before).
- Beat 3: the README's rows are typed on the rows under the long prompt, indented 4 (the
  continuation row keeps the README's 2 spaces on top of that). The ID line is not cut: it is 64
  characters. "facing only the rail" is shown by the processor's plug into the rail and, on the
  laptop's side, a dashed ghost door with "no street door" (where beat 4's door opens).
- Beat 4: the terminal grows to 7 rows (prompt + 5 README rows + ID), not 8, so V7 can stay on
  screen above it while the command is typed. The README chip (8.8 wide) does not fit right of
  the tracker; it sits over the picture, and the three labels form a legend row under it (the
  numbers land there, in the README's order) instead of standing on the door: the door and the
  room are 2 units apart at the far left, too close for three labels of 2.6–3.5 units.
- Beat 2 has pad=1.0: the COPY row's tag (44 characters) lands on "up to the copy line", 2 s
  before the clip ends; the pad gives it 3 s on screen before beat 3 clears the cards.
- Beat 4's narration names the last number ("then room 9100") at the clip's very end, so the
  block has pad=1.5: the complete legend stays 2 s before beat 5 clears it.
- Timing: anchors inside a sentence go through cue(), with shifts measured on the cached Kokoro
  clips (PLAYBOOK §2.6): the character estimate puts "127.0.0.1" 1.2 s late and "meaning this
  laptop only" 1 s early (the address alone takes 3 s to say).
- Beats 3-6: the laptop outline's bottom edge is 0.05 lower than ToyNet draws it, so the rail
  label "toynet" no longer sits on it.
- Beat 6: instead of a 10-row terminal, a 5-row terminal (cleared: the -p/-e rows have done their
  job) under V7, so the logs' 9200 and 9100 light up the rooms they name.
"""

from common import (
    CTR,
    INK,
    LOOKUP,
    NARRATION,
    P_TOY,
    STRIP_TOP,
    SYSTEM,
    TURN,
    VENV,
    ToyNet,
    _drop_bare,
    bare_prompt,
    capture,
    excerpt,
    grey_tag,
    note,
    pin,
    print_build,
    readme_chip,
    resize,
    ring,
    src_panel,
    strip_top,
    term,
    time_tag,
    tracker,
    turn_card,
    type_cmd,
    under,
)
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UL,
    UP,
    AnimationGroup,
    Create,
    DashedVMobject,
    FadeIn,
    FadeOut,
    FadeTransform,
    Indicate,
    LaggedStart,
    Line,
    Rectangle,
    RoundedRectangle,
    ShowIncreasingSubsets,
    Text,
    TransformFromCopy,
    VGroup,
    linear,
)

from explainer import style as S
from explainer.devops import (
    CAPTION,
    box,
    cell_width,
    glyph_range,
    label,
    lecture_ref,
    line_pitch,
    mono,
    mono_line,
    step_badge,
    substring,
    tag,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S11"]
assert len(SAY) == 7, len(SAY)

# ------------------------------------------------------------------ captures (file line numbers)
PL = "port-laptop"
B_PR = capture("07", PL)
assert B_PR.cmd == "docker build -t toy-processor ./processor"
PR_ROWS = B_PR.at(3, (13, 15), 22)
assert PR_ROWS[0].startswith("[+] Building 7.5s") and "[2/4] RUN apt-get" in PR_ROWS[1]
assert PR_ROWS[1].rstrip().endswith("6.4s") and "naming to docker.io/library/toy-processor" in PR_ROWS[4]
B_GW = capture("08", PL)
assert B_GW.cmd == "docker build -t toy-gateway ./gateway"
GW_ROWS = B_GW.at(3, (13, 15), 22)
assert GW_ROWS[0].startswith("[+] Building 0.3s")
assert "CACHED [2/4]" in GW_ROWS[1] and "CACHED [3/4]" in GW_ROWS[2] and "[4/4] COPY" in GW_ROWS[3]
R_PR = capture("10", PL)
PR_RUN = [R_PR.cmd, R_PR.line(2)]                 # the README's two rows, as the capture typed them
PR_ID = R_PR.line(3)
R_GW = capture("11", PL)
GW_RUN = [R_GW.cmd] + R_GW.at((2, 5))             # the README's five rows
GW_ID = R_GW.line(6)
assert len(PR_ID) == len(GW_ID) == 64
L_PR, L_GW = capture("12", PL), capture("13", PL)
assert (L_PR.cmd, L_GW.cmd) == ("docker logs processor", "docker logs gateway")
LOG_PR, LOG_GW = L_PR.line(2), L_GW.line(2)
assert LOG_PR == "processor listening on port 9200 (internal only)"
assert LOG_GW.startswith("gateway listening on port 9100")

# ------------------------------------------------------------------ README and sources
TOY = "port_toy/README.md"
assert excerpt(TOY, 100, 101).split("\n") == [B_PR.cmd, B_GW.cmd]
assert excerpt(TOY, 109, 110).split("\n") == PR_RUN
assert excerpt(TOY, 120, 124).split("\n") == GW_RUN
assert excerpt(TOY, 132, 133).split("\n") == [L_PR.cmd, L_GW.cmd]
PH113 = "There is no -p flag"
assert excerpt(TOY, 113, 113).replace("`", "").startswith(PH113 + ".")
R227 = excerpt(TOY, 227, 227)
assert R227 == "IP address : host port : container port"
assert excerpt(TOY, 224, 224) == "The `-p` flag uses this order:"
FLAG = "127.0.0.1:8090:9100"
assert FLAG in GW_RUN[1]

DOCKERFILE = {n: f"port_toy/{n}/Dockerfile" for n in ("gateway", "processor")}
DF = {n: excerpt(p, 1, 5).split("\n") for n, p in DOCKERFILE.items()}
assert DF["gateway"][:4] == DF["processor"][:4] and DF["gateway"][4] != DF["processor"][4]
assert DF["gateway"][0] == "FROM python:3.14-slim" and DF["gateway"][3] == "COPY . ."
assert DF["gateway"][1].startswith("RUN apt-get update && ")
assert DF["gateway"][4] == 'CMD ["python", "-u", "gateway.py"]'
WRAP2 = {2: ["apt-get install", "rm -rf"]}         # line 2 broken after its two `&&`


def card_lines(name: str) -> list[str]:
    """The five lines of a Dockerfile for its thin card: line 2 cut after its first `&&`, line 5
    with its middle elided."""
    d = DF[name]
    return [d[0], d[1][:d[1].index("&&") + 2] + " …", d[2], d[3], "CMD [… " + d[4].split(", ")[-1]]


PROC_PY, GATE_PY = "port_toy/processor/processor.py", "port_toy/gateway/gateway.py"
assert excerpt(PROC_PY, 42, 43).split("\n") == ['port = int(os.environ.get("PORT", "9200"))',
                                                 'server = HTTPServer(("", port), Processor)']
assert excerpt(GATE_PY, 13, 13).endswith('"processor")') and excerpt(GATE_PY, 14, 14).endswith('"9200"))')

# ------------------------------------------------------------------ layout
TOP = 2.86                     # top of anything under the tracker (its bottom is 2.905)
BAND_Y = 3.2                   # the top band, right of the tracker (x 0.7 .. 6.5)
K_NET = 0.83                   # ToyNet's vertical squash (beats 3-6)
P20 = line_pitch(CAPTION)


# ------------------------------------------------------------------ helpers
def cue(scene, vo, phrase: str, shift: float = 0.0) -> None:
    """vo.wait_until(phrase), moved by `shift` seconds. Inside a sentence an anchor is interpolated
    by character count (PLAYBOOK §2.6); the shifts below were measured on the cached Kokoro clips
    (af_heart, 0.9): the clause pauses in the scene's audio, cross-checked by synthesizing each
    sentence up to the clause. "127.0.0.1" alone takes 3 s. Re-measure after a SAY edit."""
    t = vo.clip.time_of(phrase)
    if t is None:                     # logs "voiceover anchor not found" (an error, PLAYBOOK 2.6)
        vo.wait_until(phrase)
        return
    left = t + shift - vo.elapsed
    if left > 1 / 60:
        scene.wait(left)


def flash(m, color: str = TURN, k: float = 1.12, run_time: float = 0.7):
    return Indicate(m, color=color, scale_factor=k, run_time=run_time)


def base_under(span, color: str = S.GREY, stroke: float = 3, buff: float = 0.04):
    """An underline at the baseline of a code span (through any descender), so that a mark under
    one row does not run into the capitals of the row below (`under` goes below the descender of
    "processor", which is where line 14 starts)."""
    bots = sorted(g.get_bottom()[1] for g in span)
    y = bots[len(bots) // 2] - buff                   # the median glyph bottom: the baseline
    return Line([span.get_left()[0], y, 0], [span.get_right()[0], y, 0], color=color, stroke_width=stroke)


def glyph_box(line, sub: str, color: str = TURN, pad: float = 0.06, occurrence: int = 0):
    """A box around the glyphs of `sub` in a mono line, as tall as the row (not added)."""
    g = substring(line, sub, occurrence)
    r = box(g.width + 2 * pad + 0.04, line.strut.height + 0.06, color, fill_opacity=0.0, radius=0.06,
            stroke=3)
    return r.move_to([g.get_center()[0], line.strut.get_center()[1], 0])


def code_bar(panel, n: int, color: str, opacity: float = 0.22):
    """One translucent bar over all the rows of file line n of a src_panel. Its edges sit halfway
    between neighbouring rows, so the bars of adjacent lines tile without overlapping."""
    cl = panel.code.code_lines
    ys = [m.get_center()[1] for m in cl]
    ks = panel.rows_of(n)
    a, b = ks[0], ks[-1]
    top = (ys[a] + ys[a - 1]) / 2 if a > 0 else ys[a] + (ys[a] - ys[a + 1]) / 2
    bot = (ys[b] + ys[b + 1]) / 2 if b + 1 < len(ys) else ys[b] - (ys[b - 1] - ys[b]) / 2
    bg = panel.code.background
    r = Rectangle(width=bg.width - 0.12, height=top - bot, stroke_width=0).set_fill(color, opacity)
    return r.move_to([bg.get_center()[0], (top + bot) / 2, 0])


def hi_time(line, color: str = TURN):
    """Animations: a build row's GREY time tag turns `color`."""
    tg = line.time_tag
    return [tg.box.animate.set_stroke(color, 3), tg.text.animate.set_color(color)]


def slim_times(t, rows):
    """Build rows' time tags one row high (the house tag is taller than a row)."""
    for r in rows:
        tg = getattr(r, "time_tag", None)
        if tg is not None:
            tg.box.stretch_to_fit_height(t.pitch - 0.05)


def type_rows(scene, t, rows: list[str], type_time: float = 2.0, room_after: int = 0):
    """The README's rows of a multi-line command typed under the long prompt: the prompt alone on
    its row, then each README row indented 4 (continuations keep their own 2 spaces). Returns
    a VGroup with .rows (rows[0] is the prompt row). `room_after`: rows of output to make room
    for in the same scroll (one scroll instead of two before a one-line output)."""
    _drop_bare(scene, t)
    texts = [t.prompt] + ["    " + r for r in rows]
    assert all(len(s) <= t.max_chars for s in texts), texts
    t._make_room(scene, len(texts) + room_after)
    out = []
    for k, s in enumerate(texts):
        ln = mono_line(s, t.size, INK, t2c=t._prompt_colors(t.prompt) if k == 0 else None)
        t._place(ln, len(t.lines))
        t.lines.add(ln)
        out.append(ln)
    scene.add(out[0])
    typed = VGroup(*[g for r in out[1:] for g in glyph_range(r, 0)])
    scene.play(ShowIncreasingSubsets(typed, rate_func=linear), run_time=type_time)
    for r in out:
        scene.add(r)
    g = VGroup(*out)
    g.rows = out
    return g


def text_glyphs(t: Text, s: str, sub: str):
    """The glyphs of `sub` inside a Text built from the string `s` (spaces have no glyphs)."""
    i = s.index(sub)
    a = len("".join(s[:i].split()))
    n = len("".join(sub.split()))
    return VGroup(*t.submobjects[a:a + n])


def dockerfile_card(name: str, width: float) -> VGroup:
    """A thin GREEN card of one Dockerfile: header `<name>/Dockerfile` (GREY mono) above, its five
    lines (20 pt) inside; FROM and RUN ORANGE (system), COPY GREEN. .frame .rows .header"""
    cols = [SYSTEM, SYSTEM, INK, VENV, INK]
    rows = VGroup()
    for i, (s, c) in enumerate(zip(card_lines(name), cols)):
        ln = mono_line(s, CAPTION, c)
        ln.shift([0, -i * P20, 0] - ln.strut.get_corner(UL))
        rows.add(ln)
    fr = box(width, len(rows) * P20 + 0.3, VENV, fill_opacity=0.06, radius=0.12)
    fr.move_to(rows).align_to(rows, LEFT).shift(LEFT * 0.25)
    fr.shift(UP * (rows.get_top()[1] + 0.15 - fr.get_top()[1]))
    head = mono(f"{name}/Dockerfile", CAPTION, S.GREY).next_to(fr, UP, buff=0.08).align_to(fr, LEFT)
    head.shift(RIGHT * 0.1)
    g = VGroup(fr, rows, head)
    g.frame, g.rows, g.header = fr, rows, head
    return g


def unit(m):
    """Mark a mobject to keep its shape when the ToyNet is squashed."""
    m.squash_unit = True
    return m


def squash(net: ToyNet, k: float):
    """Shrink a ToyNet vertically by k about its centre: frames, lines and gaps shrink, every text,
    tag and glyph (door, loop, browser, arrow tip, chip) keeps its size and shape."""
    for b in net.boxes.values():
        unit(b.loop)
    unit(net.laptop_loop[0])
    unit(net.browser)
    for d in list(net.doors.values()) + list(net.rooms.values()):
        unit(d.frame)
    unit(net.parts["map"][1])
    unit(net.aim_chip)
    unit(net.parts["laptop_label"])
    units = []

    def walk(m):
        if getattr(m, "squash_unit", False) or getattr(m, "keep_size", False) or \
                isinstance(m, Text) or hasattr(m, "pt"):
            units.append(m)
            return
        for s in m.submobjects:
            walk(s)

    for s in net.submobjects:
        walk(s)
    c = net.get_center()
    net.stretch(k, 1, about_point=c)
    for u in units:
        u.stretch(1 / k, 1)
    return net


def ghost_door(frame) -> VGroup:
    """A dashed GREY outline where a street door could be."""
    r = RoundedRectangle(width=frame.width, height=frame.height, corner_radius=0.04)
    return DashedVMobject(r, num_dashes=14, dashed_ratio=0.55).set_stroke(S.GREY, 2.5).move_to(frame)


def legend_item(number: str, text: str) -> VGroup:
    """One column of the -p legend: the number (mono, lifted from the flag) over its label."""
    n = mono(number, CAPTION, INK)
    lb = label(text, CAPTION, S.GREY)
    g = VGroup(n, lb).arrange(DOWN, buff=0.12)
    g.number, g.label = n, lb
    return g


class BuildAndStart(VoiceScene):
    def construct(self):
        # ============================================================ 0 · the gateway's Dockerfile
        tr = tracker("P1", 3)
        df = src_panel(DOCKERFILE["gateway"], 1, 5, wrap=WRAP2)
        df.move_to([0, 0, 0]).shift(UP * (2.45 - df.get_top()[1]))
        bars = {1: code_bar(df, 1, SYSTEM), 2: code_bar(df, 2, SYSTEM), 4: code_bar(df, 4, VENV)}
        u_span = df.span(5, '"-u"')
        u_ring = ring(u_span, TURN, buff=0.06)
        u_tag = grey_tag("unbuffered: prints reach docker logs at once")
        u_tag.next_to(df, DOWN, buff=0.3).align_to(u_span, LEFT).shift(LEFT * 0.4)
        same = VGroup(mono("processor/Dockerfile", CAPTION, INK), label(": the same, except line 5", CAPTION, INK))
        same.arrange(RIGHT, buff=0.06)
        same[1].align_to(same[0], DOWN)
        same_box = box(same.width + 0.5, same.height + 0.3, S.GREY, fill_opacity=0.08, radius=0.14)
        same_box.move_to(same)
        chip_same = VGroup(same_box, same)
        chip_same.next_to(u_tag, DOWN, buff=0.35).set_x(0)
        lref12 = lecture_ref(4, "12")          # top right, to beat 2's first play (SLIDES.md S11 i)
        assert lref12.get_bottom()[1] > df.get_top()[1] + 0.1
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr), FadeIn(df, shift=DOWN * 0.15), run_time=0.8)
            vo.wait_until("The two Dockerfiles are almost identical")
            self.play(FadeIn(chip_same, shift=UP * 0.15), FadeIn(lref12, shift=DOWN * 0.1), run_time=0.6)
            vo.wait_until("a slim Python 3.14 image")
            self.play(FadeIn(bars[1]), flash(df.span(1, "python:3.14-slim"), SYSTEM, 1.08), run_time=0.7)
            vo.wait_until("plus curl from apt")
            self.play(FadeIn(bars[2]), flash(df.span(2, "curl"), SYSTEM, 1.2), run_time=0.7)
            vo.wait_until("Each copies its code")
            self.play(FadeIn(bars[4]), flash(df.span(4, "COPY . ."), VENV, 1.1), run_time=0.7)
            vo.wait_until("and runs it with dash u")
            self.play(Create(u_ring), run_time=0.5)
            vo.wait_until("so prints reach the logs at once")
            self.play(FadeIn(u_tag, shift=UP * 0.1), run_time=0.5)

        # ============================================================ 1 · the processor builds first
        CARD_W = 4.45
        c_pr = dockerfile_card("processor", CARD_W)
        c_gw = dockerfile_card("gateway", CARD_W)
        cards = VGroup(c_pr, c_gw)
        CX = -0.12                     # the pair's centre: the CACHED tags (right) are wider than 6.4s (left)
        c_pr.shift(RIGHT * (CX - 0.35 - c_pr.frame.get_right()[0]))
        c_gw.shift(RIGHT * (CX + 0.35 - c_gw.frame.get_left()[0]))
        t = term(P_TOY, rows=7, title="laptop")
        cards.shift(UP * ((TOP - 0.09) - c_pr.header.get_top()[1]))   # clear of the tracker's caption
        assert c_pr.frame.get_bottom()[1] > t.box.get_top()[1] + 0.08
        t6 = time_tag("6.4s")
        t6.next_to(c_pr.frame, LEFT, buff=0.1).set_y(c_pr.rows[1].strut.get_center()[1])
        pull = note("first build: Docker also pulls python:3.14-slim")
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(*bars.values(), u_ring, u_tag)), run_time=0.3)
            self.play(FadeTransform(df, c_gw), FadeTransform(chip_same, c_pr), FadeIn(t, shift=UP * 0.2),
                      run_time=0.8)
            bp = type_cmd(self, t, B_PR.cmd, type_time=1.1)
            rows = print_build(self, t, PR_ROWS, run_time=0.5, lag=0.1)
            slim_times(t, rows)
            vo.wait_until("and its apt layer takes a few seconds")
            b2 = step_badge(2, CTR, radius=0.17).move_to([t.box.get_left()[0] + 0.3, rows[1].strut.get_center()[1], 0])
            box24 = glyph_box(rows[1], "[2/4]", CTR)
            self.play(FadeIn(b2, scale=1.3), Create(box24), *hi_time(rows[1]), run_time=0.6)
            self.play(TransformFromCopy(rows[1].time_tag, t6), flash(c_pr.rows[1], SYSTEM, 1.05), run_time=0.8)
            u75 = under(substring(rows[0], "Building 7.5s"), TURN)
            self.play(Create(u75), run_time=0.4)
            vo.wait_until("Your first build also pulls")
            prow = bp.rows[0]
            pull.next_to(prow.glyphs, RIGHT, buff=0.45).set_y(prow.strut.get_center()[1])
            pin(self, prow, pull, run_time=0.5)

        # ============================================================ 2 · the gateway: cached up to COPY
        eqs = VGroup()
        for i in range(5):
            y = c_pr.rows[i].strut.get_center()[1]
            eqs.add(mono("=" if i < 4 else "≠", CAPTION, S.GREY).move_to([CX, y, 0]))
        cached = VGroup()
        for i in (1, 2):
            cg = tag("CACHED", VENV)
            cg.box.stretch_to_fit_height(P20 - 0.04)
            cg.next_to(c_gw.frame, RIGHT, buff=0.1).set_y(c_gw.rows[i].strut.get_center()[1])
            cached.add(cg)
        assert cached.get_right()[0] < 6.5 and t6.get_left()[0] > -6.5
        with self.voiceover(SAY[2], pad=1.0) as vo:     # the COPY tag lands 2 s before the clip ends
            self.play(FadeOut(VGroup(b2, box24, u75)), FadeOut(lref12), *[a for a in hi_time(rows[1], S.GREY)],
                      run_time=0.3)
            type_cmd(self, t, B_GW.cmd, type_time=1.0)
            g_rows = print_build(self, t, GW_ROWS, run_time=0.5, lag=0.1)
            slim_times(t, g_rows)
            vo.wait_until("from the cache")
            cw = [substring(g_rows[i], "CACHED") for i in (1, 2)]
            self.play(*[w.animate.set_color(VENV) for w in cw], run_time=0.4)
            # the boxes first (a FadeIn re-adds its mobject on top: in the same play it would cover the text)
            self.play(*[FadeIn(cached[j].box) for j in (0, 1)], run_time=0.25)
            self.play(*[TransformFromCopy(cw[j], cached[j].text) for j in (0, 1)], run_time=0.75)
            vo.wait_until("because the two files match")
            self.play(LaggedStart(*[FadeIn(e, scale=1.4) for e in eqs[:4]], lag_ratio=0.35), run_time=1.2)
            self.play(FadeIn(eqs[4], scale=1.4), flash(substring(c_pr.rows[4], '"processor.py"'), TURN, 1.1),
                      flash(substring(c_gw.rows[4], '"gateway.py"'), TURN, 1.1), run_time=0.7)
            vo.wait_until("up to the copy line")
            # an identical COPY line is still rebuilt: it copies another folder's files (the build
            # row above has no CACHED). The tag sits on that row, one row high (the cards have no
            # room for it); it is not pinned, beat 3 fades it with the cards.
            c_row = g_rows[3]
            c_txt = substring(c_row, "[4/4] COPY . .")
            c_tag = grey_tag("same line · different files copied → rebuilt")
            c_tag.box.stretch_to_fit_height(t.pitch - 0.05)
            c_tag.next_to(c_txt, RIGHT, buff=0.45).set_y(c_row.strut.get_center()[1])
            assert c_tag.get_right()[0] < c_row.time_tag.get_left()[0] - 0.2
            self.play(flash(c_pr.rows[3], VENV, 1.15), flash(c_gw.rows[3], VENV, 1.15),
                      flash(c_txt, TURN, 1.1), FadeIn(c_tag, shift=LEFT * 0.1), run_time=0.7)
            vo.wait_until("It's done in under a second")
            u03 = under(substring(g_rows[0], "Building 0.3s"), TURN)
            self.play(Create(u03), run_time=0.4)

        # ============================================================ 3 · start the processor: no -p
        net = ToyNet(show=("outline", "laptop_label", "zone", "boxes", "rail", "rail_label", "door"))
        d1 = net.doors["door"]
        net.part("door_frame", d1.frame, shown=False, into=d1)
        net.part("door_label", d1.label, shown=False, into=d1)
        net.part("gw_box", net.boxes["gateway"], shown=False, into=net.parts["boxes"])
        squash(net, K_NET)
        outline = net.parts["outline"]
        # the rail label's "y" would sit on the outline's bottom edge: lower that edge a little
        outline.stretch_to_fit_height(outline.height + 0.05, about_edge=UP)
        net.shift(UP * (STRIP_TOP + 0.06 - outline.get_bottom()[1]))
        assert net.parts["rail_label"].get_bottom()[1] - outline.get_bottom()[1] > 0.06
        pp = src_panel(PROC_PY, 42, 43, size=20)
        pp.shift([6.5 - pp.get_right()[0], TOP - pp.get_top()[1], 0])
        assert pp.get_bottom()[1] > net.parts["laptop_label"].get_top()[1] + 0.03
        port_span = pp.span(42, '"PORT"')
        empty = pp.span(43, '""')
        e_ring = ring(empty, TURN, buff=0.05)
        e_tag = grey_tag("every address of its own box")
        e_tag.next_to(pp, LEFT, buff=0.2).set_y(empty.get_center()[1])
        ch113 = readme_chip("README.md · line 113", PH113)
        ch113.move_to([0, BAND_Y, 0]).align_to([6.5, 0, 0], RIGHT)
        ghost = ghost_door(d1.frame)
        no_door = note("no street door").next_to(ghost, LEFT, buff=0.15)
        with self.voiceover(SAY[3]) as vo:
            self.play(FadeOut(VGroup(cards, t6, cached, eqs, u03, c_tag)), tr.goto(4), run_time=0.5)
            run_p = type_rows(self, t, PR_RUN, type_time=1.5, room_after=1)
            t.print(self, [PR_ID], run_time=0.35)
            # "with PORT set to 9200" is spoken while the rows are typed: light it at once
            cue(self, vo, "with PORT set to 9200", -0.48)
            p92 = substring(run_p.rows[2], "PORT=9200")
            self.play(p92.animate.set_color(LOOKUP), run_time=0.4)
            resize(self, t, 3, run_time=0.6, extra=[FadeIn(pp, shift=DOWN * 0.1), FadeIn(net)])
            self.play(port_span.animate.set_color(LOOKUP), *net.parts_in("plug_processor", anim=Create),
                      run_time=0.5)
            cue(self, vo, "and no dash p", -0.25)
            self.play(FadeIn(ch113, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("It listens on 9200 inside its own box")
            self.play(net.open_room("processor", 9200, run_time=0.9))
            room_p = net.rooms["processor"]
            cue(self, vo, "inside its own box", 0.62)
            self.play(flash(room_p, CTR, 1.25), Create(e_ring), FadeIn(e_tag, shift=RIGHT * 0.1), run_time=0.7)
            cue(self, vo, "but nothing on your laptop leads to it", 0.90)
            net.attach(self, ghost, no_door, anims=[Create(ghost), FadeIn(no_door)],
                       extra=[flash(net.wall, S.GREY, 1.0)], run_time=0.7)

        # ============================================================ 4 · start the gateway: -p, a street door to a room
        up_dy = TOP - net.parts["laptop_label"].get_top()[1]       # (its top is its BG patch)
        ch227 = readme_chip("README.md · lines 224–228", R227, max_w=9.0)
        ch227.move_to([0.25, 0, 0]).set_y(TOP - 0.05 - ch227.height / 2)
        terms = [text_glyphs(ch227.phrase, f"“{R227}”", w) for w in ("IP address", "host port", "container port")]
        legend = VGroup(legend_item("127.0.0.1", "IP address · this laptop only"),
                        legend_item("8090", "host port · street door"),
                        legend_item("9100", "container port · room"))
        legend.arrange(RIGHT, buff=0.6, aligned_edge=UP)
        legend.move_to([0.25, 0, 0]).shift(UP * (ch227.get_bottom()[1] - 0.12 - legend.get_top()[1]))
        lref35 = lecture_ref(4, "35")          # top right, with the -p box to beat 5's first play (SLIDES.md S11 i)
        assert lref35.get_bottom()[1] > max(TOP, ch227.get_top()[1]) + 0.1
        with self.voiceover(SAY[4], pad=1.5) as vo:      # the legend's last item lands at the very end
            self.play(FadeOut(VGroup(pp, e_ring, e_tag, ch113)), tr.goto(5), run_time=0.5)
            assert net.get_top()[1] + up_dy <= TOP + 0.01 < tr.get_bottom()[1]
            resize(self, t, 7, run_time=0.7, extra=[net.animate.shift(UP * up_dy)])
            assert outline.get_bottom()[1] > t.box.get_top()[1] + 0.04, (outline.get_bottom()[1], t.box.get_top()[1])
            run_g = type_rows(self, t, GW_RUN, type_time=1.9, room_after=1)
            t.print(self, [GW_ID], run_time=0.35)
            # the container exists: its box plugs in, and the -p flag is boxed ("Dash p publishes a
            # port" was spoken while it was typed), with the slide 35 tag. The door and the room then
            # open on their words, above the 7-row terminal; the strip comes after, for the legend's band.
            p_row = run_g.rows[2]
            p_box = glyph_box(p_row, "-p " + FLAG, LOOKUP)
            pin(self, p_row, p_box, run_time=0.5,
                anim=AnimationGroup(Create(p_box), *net.parts_in("gw_box"),
                                    *net.parts_in("plug_gateway", anim=Create), FadeIn(lref35, shift=DOWN * 0.1)))
            cue(self, vo, "it opens a street door on your laptop", 0.57)
            net.detach(self, ghost, no_door, anims=[FadeOut(ghost), FadeOut(no_door)],
                       extra=[*net.parts_in("door_frame"),
                              *net.parts_in("door_label", anim=lambda m: TransformFromCopy(substring(p_row, "127.0.0.1:8090"), m))],
                       run_time=0.9)
            self.play(flash(d1.frame, TURN, 1.2), run_time=0.5)
            cue(self, vo, "that leads to a room inside the container", 0.30)
            self.play(net.open_room("gateway", 9100, run_time=0.9))
            self.play(*net.parts_in("map", anim=Create), run_time=0.9)
            keep = [run_g.rows[2], run_g.rows[3], run_g.rows[4]]
            resize(self, t, 3, keep=keep, run_time=0.8, extra=[net.animate.shift(DOWN * up_dy)])
            vo.wait_until("The order is")
            self.play(FadeIn(ch227, shift=DOWN * 0.15), run_time=0.5)
            for w, (phrase, dt) in zip(terms, (("IP address", -0.60), ("host port", -0.85), ("container port", -1.05))):
                cue(self, vo, phrase, dt)
                self.play(flash(w, TURN, 1.1, 0.55))
            # the three numbers, in the spoken order: boxed in the flag, lifted into the legend
            targets = [text_glyphs(d1.label, "127.0.0.1:8090", "127.0.0.1"), d1.frame, net.rooms["gateway"]]
            subs = ["127.0.0.1", "8090", "9100"]
            spoken = [("127.0.0.1", -1.24), ("then door 8090", 0.06), ("then room 9100", 0.0)]
            boxes = VGroup()
            for k, (sub, item, tgt) in enumerate(zip(subs, legend, targets)):
                cue(self, vo, *spoken[k])
                assert p_row.text.count(sub) == 1
                src = substring(p_row, sub)
                bx = glyph_box(p_row, sub, TURN, pad=0.02)
                boxes.add(bx)
                self.play(Create(bx), run_time=0.3)
                self.play(TransformFromCopy(src, item.number), FadeIn(item.label, shift=DOWN * 0.1),
                          flash(tgt, TURN, 1.15, 0.8), run_time=0.8)
                if k == 0:
                    cue(self, vo, "meaning this laptop only", 1.03)
                    only = text_glyphs(item.label, "IP address · this laptop only", "this laptop only")
                    self.play(flash(only, TURN, 1.1), run_time=0.7)

        # ============================================================ 5 · -e: where the gateway will call
        gp = src_panel(GATE_PY, 13, 14, size=20)
        gp.shift([6.5 - gp.get_right()[0], TOP - gp.get_top()[1], 0])
        assert gp.get_bottom()[1] > net.parts["laptop_label"].get_top()[1] + 0.03
        names = [gp.span(13, '"PROCESSOR_HOST"'), gp.span(14, '"PROCESSOR_PORT"')]
        dflt = [gp.span(13, '"processor"'), gp.span(14, '"9200"')]
        d_lines = VGroup(*[base_under(m) for m in dflt])
        assert d_lines[0].get_center()[1] > gp.code.code_lines[1].get_top()[1] + 0.04   # clear of line 14
        # the tag on the panel's header row, right above the two values it names
        d_tag = grey_tag("defaults")
        d_tag.move_to([dflt[0].get_center()[0], gp.header.get_center()[1] + 0.05, 0])
        assert d_tag.get_left()[0] > gp.header.get_right()[0] + 0.3 and d_tag.get_right()[0] < 6.55
        assert d_tag.get_bottom()[1] > gp.code.background.get_top()[1] + 0.03
        e_rows = keep[1:]
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(ch227, legend)), FadeOut(boxes), FadeOut(lref35), run_time=0.5)
            self.play(*[r.glyphs.animate.set_color(LOOKUP) for r in e_rows], run_time=0.6)
            cue(self, vo, "the name processor, port 9200", -0.63)
            self.play(*net.parts_in("aim", anim=lambda m: AnimationGroup(Create(m[0]), FadeIn(m[1]))),
                      flash(substring(e_rows[0], "processor"), TURN, 1.15), run_time=0.8)
            cue(self, vo, "port 9200", -0.86)
            self.play(flash(substring(e_rows[1], "9200"), TURN, 1.15), flash(net.aim_chip, TURN, 1.1),
                      run_time=0.7)
            vo.wait_until("Lines 13 and 14 of its code read them")
            self.play(FadeIn(gp, shift=DOWN * 0.1), run_time=0.6)
            self.play(*[m.animate.set_color(LOOKUP) for m in names], run_time=0.5)
            cue(self, vo, "the values in quotes there are only defaults", 0.79)
            self.play(Create(d_lines), FadeIn(d_tag, shift=DOWN * 0.1), run_time=0.6)

        # ============================================================ 6 · docker logs: who listens where
        t5_top = strip_top(5)
        up6 = (t5_top + 0.06) - outline.get_bottom()[1]
        assert net.parts["laptop_label"].get_top()[1] + up6 < TOP
        card = turn_card([B_PR.cmd, B_GW.cmd, "\n".join(PR_RUN), "\n".join(GW_RUN), L_PR.cmd, L_GW.cmd])
        for item in (card.rows[2], card.rows[3]):         # the README's continuation rows keep their 2 spaces
            for row in item[1:]:
                row.shift(RIGHT * 2 * cell_width(CAPTION))
        card.move_to([0, 0, 0]).shift(UP * ((TOP - 0.05) - card.get_top()[1]))
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(gp, d_lines, d_tag)), tr.goto(6), run_time=0.5)
            resize(self, t, 5, keep=[], run_time=0.6, extra=[net.animate.shift(UP * up6)])
            type_cmd(self, t, L_PR.cmd, type_time=0.7)
            o_pr = t.print(self, [LOG_PR], run_time=0.3)[0]
            type_cmd(self, t, L_GW.cmd, type_time=0.7)
            o_gw = t.print(self, [LOG_GW], run_time=0.3)[0]
            bare_prompt(self, t)
            vo.wait_until("The processor listens on 9200")
            b92 = glyph_box(o_pr, "9200", CTR)
            self.play(Create(b92), flash(net.rooms["processor"], CTR, 1.3), run_time=0.7)
            vo.wait_until("internal only")
            u_int = under(substring(o_pr, "(internal only)"), S.GREY, 3)
            self.play(Create(u_int), run_time=0.4)
            vo.wait_until("the gateway listens on 9100")
            b91 = glyph_box(o_gw, "9100", CTR)
            self.play(Create(b91), flash(net.rooms["gateway"], CTR, 1.3), run_time=0.7)
            vo.wait_until("Pause and start both")
            self.play(FadeOut(VGroup(t, net, b92, b91, u_int)), run_time=0.4)
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.5)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.6)
        self.wait(0.2)
