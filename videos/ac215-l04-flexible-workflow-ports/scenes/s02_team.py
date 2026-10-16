"""S02 · Same pipeline, built like a team (concept scene: no README tracker).

Beats (script.md "## S02", one voiceover block each):
0. A GREY README card (README.md · lines 58–60: line 58 in part, then line 60) fades in; "a shared
   bucket" and "a shared service account" underline YELLOW as they are said. The card condenses:
   its frame becomes a two-column card "L03" (GREY) | "L04" (YELLOW), line 60 becomes a one-line
   README chip above it, and the two phrases become row 1 "a shared bucket" (BLUE drawer
   "course") and row 2 "one shared key, copied into five folders" (five GREY folders, each with a
   small GOLD key; chip main · README.md · line 97), in two steps: first the lines that are not
   carried over leave and line 60 rises into the chip, then the frame and the two phrases move,
   so the old lines never sit inside the new frame. On "This branch is …" the chip's phrase
   ("the same pipeline, built the way a real team would build it") underlines YELLOW and rows 1–2
   morph into the L04 column: "your own bucket" (BLUE drawer "your team"); "your own service
   account · one key outside the repo" (the five keys become one GOLD key outside a GREY repo
   outline).
1. README chip README.md · lines 62–63 under rows 1–2. Row 1's right cell pulses BLUE; "your own
   service account" flashes BLUE; the GOLD key slides a little further outside the repo outline.
2. The card grows to four rows (the chip becomes README.md · lines 64–65 under it). Row 3: "you
   wrote each Dockerfile" (GREY pencil) morphs into the GREEN recipe card (Dockerfile,
   pyproject.toml, uv.lock) "committed"; pyproject.toml and uv.lock flash. Row 4: a long GREY
   command chip `docker run --rm -ti -v …` "typed from memory" morphs into the PURPLE chip
   `docker-shell.sh`; on "that holds" `docker build …` and `docker run …` slide out of it.
3. The card clears. Lecture 3's relay in miniature (MiniRelay, glyph-only; GREY tag "from lecture
   3"): the five TEAL boxes flash; a GREY README card (README.md · lines 140–142) fades in; its
   "communicate indirectly by writing their outputs to storage" underlines YELLOW as a token hops
   drawer → box → drawer; then a dashed GREY arc between two boxes gets the GREY tag "part 2" and
   the card's "talk to each other through APIs" underlines GREY.
4. V1 (BuildOrPull) under a GREY README card (README.md · lines 67–72, "Two ways to work — and we
   support both"): Git shelf + GREEN recipe card | BLUE Docker Hub shelf (illustration); a PURPLE
   `docker build` arrow, a GREY laptop, and a copy of the card's outline turns into the TEAL image
   `Python 3.14.8 · uv`. "early in development": three GREY teammates; three PURPLE build arrows
   from the card, a small image on each laptop. "later in development": the build arrows, the
   middle laptop and its `docker build` arrow leave; a copy of the right teammate's image flies up
   onto the BLUE shelf and becomes the sealed box; BLUE pull arrows arc from it (over the shelf's
   left end, not through its plank) down to the other two, a sealed box lands on each laptop.
5. Teammates and README card leave and the rest of V1 moves down to the centre; the PINK signpost
   dlops/mega-pipeline-transcribe-audio:latest appears beside the box, its pointer on the box (the
   pointer and the box flash); a dashed GREY "?" line from the card to the box and the GREY
   caption "built on some day, from some commit". On "Nothing promises": the box slides left (the
   pointer and the "?" line follow it), a second sealed box is set down onto the shelf in its
   place (from above: rising from below, it crossed the "Docker Hub" caption), the signpost swings
   to the new box, then back.
6. The "?" line leaves; the two halves slide toward the centre; between them the PURPLE
   switchboard silhouette (V4, no labels) captioned `docker-shell.sh`. Fade out to an empty frame.

Deviations from SHOW (and why):
- Beat 3: the token's hop is built here (relay_hop): common.MiniRelay.hop() creates all its
  `.animate` steps up front, they share the token's one `.target`, and the token slid straight
  along the drawers to the last one without visiting a box.
- Beat 4: the Docker Hub shelf starts empty; the sealed box appears when the teammate pushes it
  (phase 2). With a box already on the shelf, phase 2's push and beat 5's "second box" would make
  three boxes; and "early in development" nothing has been published yet.
- Beat 4: V1's illustration tag sits under the "Docker Hub" caption (not beside it) so the BLUE
  pull arrows and the tag never cross and the piece stays inside x <= 6.6.
- Beat 4, phase 2: the middle laptop and its `docker build` arrow fade with the PURPLE build
  arrows ("later", nobody builds but the publisher): the BLUE pull arrows to the left teammates
  would otherwise cross the `Python 3.14.8 · uv` label. The publisher keeps its local image (a
  push copies it).
- Beat 5: no camera zoom (VoiceScene has a fixed camera): the focus on the shelf comes from
  clearing the teammates and the README card and moving what is left 0.7 down to the frame's
  centre. The old box slides left before the second box arrives, so the dashed "?" line from the
  card never runs through the new box. The signpost board is drawn above its pointer
  (z-index), so a pointer aimed at the left box leaves from under the board instead of crossing
  the tag's text; the post's stick likewise covers the "?" line where they cross.
- Beats 0 and 2: the glyphs morph L03 -> L04 (drawer, folders -> repo, keys -> one key, pencil
  -> recipe card, command chip -> script chip); the L04 texts slide in beside them instead of
  morphing letter by letter (a letter morph between two different sentences is unreadable).
- The small drawers, folders and keys inside the L03 | L04 card are icons, not schematics: no
  illustration tag on them (the Docker Hub shelf, the only schematic, keeps its tag).

Sources: README.md lines 58, 60, 62–65, 67, 140, 142 and mega-pipeline-main README.md lines 97
and 235 (the `docker run --rm -ti -v` prefix), all checked against assets/source below.
"""

import numpy as np
from common import (
    CLOUD,
    CTR,
    HUB,
    KEY,
    LAPTOP,
    LOOKUP,
    NARRATION,
    TOOL,
    TURN,
    VENV,
    BuildOrPull,
    MiniRelay,
    Switchboard,
    cmd_chip,
    drawer,
    excerpt,
    grey_tag,
    key_glyph,
    note,
    pencil,
    readme_card,
    readme_chip,
    recipe_card,
    sans,
    sealed_box,
    under,
)
from manim import (
    DOWN,
    LEFT,
    PI,
    RIGHT,
    UP,
    AnimationGroup,
    ArcBetweenPoints,
    Arrow,
    Create,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    FadeTransform,
    GrowArrow,
    Indicate,
    LaggedStart,
    Line,
    MoveAlongPath,
    ReplacementTransform,
    Restore,
    Succession,
    Text,
    Transform,
    TransformFromCopy,
    VGroup,
    VMobject,
    smooth,
)

from explainer import style as S
from explainer.devops import (
    CAPTION,
    INK,
    MONO,
    box,
    chip,
    folder_glyph,
    label,
    laptop,
    mono,
)
from explainer.scene import VoiceScene

SAY = NARRATION["S02"]
assert len(SAY) == 7, len(SAY)

README = "mega-pipeline/README.md"
L58 = excerpt(README, 58, 58)
L60 = excerpt(README, 60, 60).replace("**", "")
L62 = excerpt(README, 62, 62).replace("**", "")
L63 = excerpt(README, 63, 63).replace("**", "")
L64 = excerpt(README, 64, 64).replace("**", "")
L65 = excerpt(README, 65, 65).replace("**", "").replace("`", "")
L67 = excerpt(README, 67, 67)
L140 = excerpt(README, 140, 140)
L142 = excerpt(README, 142, 142).replace("**", "")
L235_MAIN = excerpt("mega-pipeline-main/README.md", 235, 235)

# the README card of beat 0 (line 58 in part, line 60)
R58A = "You've already built this pipeline once, with most of the scaffolding handed"
R58B = "to you — a shared bucket, a shared service account, a ready-made Docker setup. …"
R60 = "This branch is the same pipeline, built the way a real team would build it."
assert f"{R58A} {R58B[:-2]}" in L58 and R60 in L60
PH60 = "the same pipeline, built the way a real team would build it"
PH62 = "Your own GCS bucket. … Your own service account."
assert "Your own GCS bucket." in L62 and "Your own service account." in L63
PH64 = "already written for you … A docker-shell.sh script per component."
assert "already written for you" in L64 and "A docker-shell.sh script per component." in L65
# the README card of beat 3 (lines 140 and 142)
R140 = "In a production pipeline, containerized services talk to each other through APIs, …"
R142A = "… components will communicate indirectly by writing their outputs to storage,"
R142B = "which the next stage will then read as input."
assert R140[:-2] in L140 and f"{R142A[2:]} {R142B}" in L142
HEAD67 = "Two ways to work — and we support both"
assert HEAD67 in L67
RUN_L03 = "docker run --rm -ti -v"            # the main branch's docker run (README.md:235)
assert RUN_L03 in L235_MAIN

# ------------------------------------------------------------------ the L03 | L04 card's grid
TL, SLOT1, G1 = -6.2, 2.45, 0.25      # column 1: left edge, glyph slot, gap before the text
T1 = TL + SLOT1 + G1                  # column 1 text
XD = -0.19                            # the divider
C2, SLOT2, G2 = 0.01, 2.95, 0.2       # column 2
T2 = C2 + SLOT2 + G2
FRAME_L, FRAME_R = -6.345, 6.345
TOP = 2.8                             # the card's top edge (the line-60 chip sits above it)
HEAD_Y, SEP_Y = 2.49, 2.24
Y1 = 1.92                             # row 1
Y2_TOP, Y2_CHIP, Y2 = 1.2, 0.66, 0.95  # row 2: L03 top part, its chip, L04 centre
BOT12 = 0.235                         # the card's bottom edge with two rows
Y3 = -0.465                           # row 3
Y4 = -1.815                           # row 4
BOT = -2.465                          # the card's bottom edge with four rows
BASE = 0.0                            # V1's shelves (beat 4)
D5 = 0.7                              # beat 5 re-centres V1 this far down


def ltext(s: str, color: str = INK, size: float = CAPTION) -> Text:
    """Serif text whose submobjects index `s` one character each (spaces included)."""
    return label(s, size, color, disable_ligatures=True)


def chars(t: Text, s: str, sub: str) -> VGroup:
    """The glyphs of the substring `sub` of the ltext `t` (made from `s`)."""
    i = s.index(sub)
    return VGroup(*[m for m in t.submobjects[i:i + len(sub)] if m.has_points()])


def two_lines(a: str, b: str) -> VGroup:
    return VGroup(ltext(a), ltext(b)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)


def at_text(m, x: float, y: float):
    """Left edge at x, vertical centre at y."""
    return m.move_to([x + m.width / 2, y, 0])


def card_frame(bottom: float) -> VMobject:
    return box(FRAME_R - FRAME_L, TOP - bottom, S.GREY, fill=S.BG, fill_opacity=0.95,
               radius=0.14).move_to([(FRAME_L + FRAME_R) / 2, (TOP + bottom) / 2, 0])


def divider(bottom: float) -> Line:
    return Line([XD, SEP_Y - 0.1, 0], [XD, bottom + 0.1, 0], color=S.GREY_DARK, stroke_width=2)


def folders_with_keys() -> tuple[VGroup, VGroup]:
    """Five GREY folders (the component folders), each holding a small GOLD key."""
    fs = VGroup(*[folder_glyph(0.32, LAPTOP) for _ in range(5)]).arrange(RIGHT, buff=0.09)
    ks = VGroup()
    for f in fs:
        ks.add(key_glyph(0.15).move_to(f[1]))
    return fs, ks


def repo_outline() -> VGroup:
    fr = box(1.55, 0.62, LAPTOP, fill_opacity=0.06, radius=0.1)
    t = label("repo", CAPTION, S.GREY).move_to(fr)
    g = VGroup(fr, t)
    g.frame, g.text = fr, t
    return g


def small_image(sealed: bool = False) -> VGroup:
    """A small TEAL image on a teammate's laptop (sealed = pulled from the registry)."""
    b = sealed_box(0.3, CTR)
    if not sealed:
        b.remove(b.tape)
    return b


def relay_hop(relay, run_time: float = 3.2):
    """The token's relay through MiniRelay: drawer 0 -> box 0 -> drawer 1 -> box 1 ... -> drawer 5.
    Returns (token, Succession). Built here because MiniRelay.hop() creates every `.animate` step
    up front, so all steps share the token's one `.target` and it slides straight to drawer 5."""
    tok = Dot(radius=0.08, color=INK).move_to(relay.drawers[0])
    stops = []
    for j in range(5):
        stops += [relay.boxes[j].get_center(), relay.drawers[j + 1].get_center()]
    per = run_time / len(stops)
    prev, steps = relay.drawers[0].get_center(), []
    for q in stops:
        steps.append(MoveAlongPath(tok, Line(prev, q), rate_func=smooth, run_time=per))
        prev = q
    return tok, Succession(*steps)


def dashed_arc(a, b, color: str = S.GREY) -> VGroup:
    """A dashed arrow arcing up from the top of `a` to the top of `b`."""
    arc = ArcBetweenPoints(a.get_top() + UP * 0.08, b.get_top() + UP * 0.08, angle=-PI * 0.55)
    arc.add_tip(tip_length=0.16, tip_width=0.16)
    tip = arc.pop_tips()[0].set_color(color)
    dashed = DashedVMobject(arc, num_dashes=10, dashed_ratio=0.55).set_stroke(color, 3)
    return VGroup(dashed, tip)


def shell_morph(scene, src_shell, dst, dst_shell, dst_text, *extra, run_time: float = 1.0):
    """A copy of the shapes `src_shell` morphs into `dst_shell` (the shapes of `dst`) while the
    text `dst_text` of `dst` slides in: a letter-by-letter morph between two labels is unreadable.
    Leaves `dst` on the scene as one group."""
    wrap = VGroup(*dst_shell)
    scene.play(TransformFromCopy(VGroup(*src_shell), wrap), FadeIn(dst_text, shift=RIGHT * 0.3),
               *extra, run_time=run_time)
    scene.remove(wrap, dst_text)
    scene.add(dst)


class TeamWorkflow(VoiceScene):
    def construct(self):
        # ------------------------------------------------------------ objects of beats 0-2
        card = readme_card("README.md · lines 58–60", [R58A, R58B, R60])
        for i, s in enumerate((R58A, R58B, R60)):      # rows whose glyphs index the string
            card.rows.submobjects[i] = ltext(s).move_to(card.rows[i])
        card.move_to([0, 0.35, 0])
        r58a, r58b, r60 = card.rows
        u_bucket = under(chars(r58b, R58B, "a shared bucket"), TURN)
        u_sa = under(chars(r58b, R58B, "a shared service account"), TURN)

        chip60 = readme_chip("README.md · line 60", PH60, max_w=12.6).move_to([0, 3.18, 0])
        frame = card_frame(BOT12)
        frame_full = card_frame(BOT)
        head03 = label("L03", 24, S.GREY)
        head04 = label("L04", 24, TURN)
        at_text(head03, TL, HEAD_Y)
        at_text(head04, C2, HEAD_Y)
        sep = Line([FRAME_L + 0.15, SEP_Y, 0], [FRAME_R - 0.15, SEP_Y, 0], color=S.GREY_DARK,
                   stroke_width=2)
        div = divider(BOT12)
        div_full = divider(BOT)

        # row 1: the bucket
        d1_03 = drawer("course", 2.3).move_to([TL + SLOT1 / 2, Y1, 0])
        t1_03 = at_text(ltext("a shared bucket"), T1, Y1)
        d1_04 = drawer("your team", 2.3).move_to([C2 + SLOT2 / 2, Y1, 0])
        t1_04 = at_text(ltext("your own bucket"), T2, Y1)
        # row 2: the key
        folders, keys = folders_with_keys()
        VGroup(folders, keys).move_to([TL + SLOT1 / 2, Y2_TOP, 0])
        t2_03 = at_text(two_lines("one shared key,", "copied into five folders"), T1, Y2_TOP)
        chip97 = readme_chip("main · README.md · line 97")
        at_text(chip97, TL, Y2_CHIP)
        repo = repo_outline()
        key04 = key_glyph(0.3)
        rk = VGroup(repo, key04)
        key04.next_to(repo, RIGHT, buff=0.2)
        at_text(rk, C2 + 0.15, Y2)
        t2_04 = at_text(two_lines("your own service account", "one key outside the repo"), T2, Y2)
        # row 3: the Dockerfile
        pen = pencil(0.55, LAPTOP).move_to([TL + SLOT1 / 2, Y3, 0])
        t3_03 = at_text(ltext("you wrote each Dockerfile"), T1, Y3)
        recipe = recipe_card().move_to([C2 + SLOT2 / 2, Y3, 0])
        t3_04 = at_text(ltext("committed", VENV), T2, Y3)
        # row 4: the docker run command
        run_chip = cmd_chip(f"{RUN_L03} …")
        at_text(run_chip, TL, Y4 + 0.19)
        t4_03 = at_text(ltext("typed from memory"), T1, Y4 - 0.27)
        sh_chip = chip("docker-shell.sh", TOOL, size=CAPTION, font=MONO).move_to([C2 + SLOT2 / 2, Y4, 0])
        holds = VGroup(mono("docker build …", CAPTION, INK), mono("docker run …", CAPTION, INK))
        holds.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        at_text(holds, T2, Y4)

        chip62 = readme_chip("README.md · lines 62–63", PH62, max_w=12.6).move_to([0, BOT12 - 0.38, 0])
        chip64 = readme_chip("README.md · lines 64–65", PH64, max_w=12.6).move_to([0, BOT - 0.4, 0])

        # ------------------------------------------------------------ 0. L03 -> L04, rows 1-2
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(card), run_time=0.8)
            self.remove(card)                       # flat: the parts leave separately
            self.add(card.frame, card.header, r58a, r58b, r60)
            vo.wait_until("a shared bucket")
            self.play(Create(u_bucket), run_time=0.4)
            vo.wait_until("and one shared key")
            self.play(Create(u_sa), run_time=0.4)
            # the card condenses in two steps, so the old lines never sit inside the new frame:
            # 1. what is not carried over leaves, and line 60 becomes the chip above;
            # 2. the frame becomes the L03 | L04 card and the two phrases fly to their rows
            ph_b = chars(r58b, R58B, "a shared bucket")
            ph_sa = chars(r58b, R58B, "a shared service account")
            kept = set(ph_b.submobjects) | set(ph_sa.submobjects)
            rest_b = VGroup(*[m for m in r58b.submobjects if m.has_points() and m not in kept])
            # the lines line 60 flies past fade quickly, so they are gone when it reaches them
            self.play(AnimationGroup(FadeOut(card.header, run_time=0.25), FadeOut(r58a, run_time=0.2),
                                     FadeOut(rest_b, run_time=0.25), FadeTransform(r60, chip60, run_time=0.55)))
            self.play(ReplacementTransform(card.frame, frame), FadeOut(u_bucket), FadeOut(u_sa),
                      ReplacementTransform(ph_b, t1_03), FadeTransform(ph_sa, t2_03),
                      FadeIn(head03), FadeIn(head04), Create(sep), Create(div), FadeIn(d1_03),
                      run_time=0.8)
            self.remove(r58b)                       # its glyphs have all left or become row texts
            vo.wait_until("copied into")
            self.play(LaggedStart(*[FadeIn(VGroup(f, k), shift=DOWN * 0.15) for f, k in zip(folders, keys)],
                                  lag_ratio=0.18), run_time=1.0)
            self.play(FadeIn(chip97, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("This branch")
            u60 = under(VGroup(*chip60.phrase.submobjects[1:-1]), TURN)   # the words, not the quotes
            self.play(Create(u60), Indicate(head04, color=TURN, scale_factor=1.25), run_time=0.8)
            shell_morph(self, (d1_03.frame, d1_03.handle), d1_04, (d1_04.frame, d1_04.handle), d1_04.label,
                        FadeIn(t1_04, shift=RIGHT * 0.4))
            self.play(TransformFromCopy(folders, repo), TransformFromCopy(keys, key04),
                      FadeIn(t2_04, shift=RIGHT * 0.4), run_time=1.2)

        # ------------------------------------------------------------ 1. yours: bucket, account, key
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeIn(chip62, shift=UP * 0.1), FadeOut(u60),
                      Indicate(VGroup(d1_04, t1_04), color=CLOUD, scale_factor=1.08), run_time=1.0)
            vo.wait_until("You create your own service account")
            self.play(Indicate(t2_04[0], color=CLOUD, scale_factor=1.08), run_time=0.8)
            vo.wait_until("and keep its one key outside the repo")
            self.play(key04.animate.shift(RIGHT * 0.35),
                      Indicate(t2_04[1], color=KEY, scale_factor=1.08), run_time=0.9)

        # ------------------------------------------------------------ 2. rows 3-4: recipe, script
        with self.voiceover(SAY[2]) as vo:
            self.play(Transform(frame, frame_full), Transform(div, div_full),
                      FadeTransform(chip62, chip64), run_time=0.8)
            self.play(FadeIn(pen), FadeIn(t3_03), run_time=0.6)
            # the character-count estimate puts "it's committed" ~0.5 s late (the file names that
            # follow are spoken slowly): start the morph a little before it
            self.wait(max(0.0, vo.time_until("it's committed") - 0.4))
            self.play(TransformFromCopy(pen, recipe), FadeIn(t3_04, shift=RIGHT * 0.4), run_time=1.0)
            vo.wait_until("together with")
            self.play(Indicate(recipe.rows[1], color=VENV, scale_factor=1.12), run_time=0.8)
            # same skew, larger: the estimate for "and uv.lock" is ~0.9 s after the voice says it
            self.wait(max(0.0, vo.time_until("and uv.lock") - 0.8))
            self.play(Indicate(recipe.rows[2], color=VENV, scale_factor=1.12), run_time=0.8)
            vo.wait_until("And each component")
            self.play(FadeIn(run_chip), FadeIn(t4_03), run_time=0.7)
            vo.wait_until("one script")
            shell_morph(self, (run_chip.box,), sh_chip, (sh_chip.box,), sh_chip.text)
            for m in holds:
                m.save_state()
                m.move_to(sh_chip).set_opacity(0)
            vo.wait_until("that holds")
            self.play(Indicate(sh_chip.box, color=TOOL, scale_factor=1.06), run_time=0.8)
            vo.wait_until("the long docker build")
            self.play(Restore(holds[0]), run_time=0.7)
            vo.wait_until("and docker run")
            self.play(Restore(holds[1]), run_time=0.7)

        # ------------------------------------------------------------ 3. still a relay through the bucket
        relay = MiniRelay().move_to([0, 1.05, 0])
        tag_l3 = grey_tag("from lecture 3").next_to(relay, RIGHT, buff=0.35)
        card140 = readme_card("README.md · lines 140–142", [R140, R142A, R142B])
        rows140 = [ltext(s).move_to(card140.rows[i]) for i, s in enumerate((R140, R142A, R142B))]
        for i, r in enumerate(rows140):
            card140.rows.submobjects[i] = r
        card140.move_to([0, -1.9, 0])
        u_store = under(chars(rows140[1], R142A,
                              "communicate indirectly by writing their outputs to storage"), TURN)
        u_api = under(chars(rows140[0], R140, "talk to each other through APIs"), S.GREY)
        arc = dashed_arc(relay.boxes[1], relay.boxes[2])
        part2 = grey_tag("part 2").next_to(arc, UP, buff=0.08)
        with self.voiceover(SAY[3]) as vo:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.5)
            self.play(FadeIn(relay), FadeIn(tag_l3), run_time=0.6)
            self.play(LaggedStart(*[Indicate(b, color=CTR, scale_factor=1.15) for b in relay.boxes],
                                  lag_ratio=0.15), run_time=0.9)
            vo.wait_until("and they still never call each other")
            self.play(FadeIn(card140), run_time=0.6)
            vo.wait_until("each writes to the bucket")
            tok, hop = relay_hop(relay, run_time=3.2)
            self.play(hop, Create(u_store, run_time=0.6))
            if hop.group in self.mobjects:          # the Succession's wrapper group
                self.remove(hop.group)
                self.add(tok)
            vo.wait_until("Containers that talk directly")
            self.play(FadeOut(tok), Create(arc), FadeIn(part2, shift=DOWN * 0.1), Create(u_api),
                      run_time=0.9)

        # ------------------------------------------------------------ 4. V1: build or pull
        v1 = BuildOrPull(show=("git", "card", "hub", "hub_tag"))
        v1.shift(RIGHT * 0.05 + UP * (BASE - v1.base_y))
        hub_tag = v1.parts["hub_tag"]
        hub_tag.next_to(v1.hub_shelf.caption, DOWN, buff=0.12)
        card67 = readme_card("README.md · lines 67–72", [HEAD67])
        card67.move_to([0, 3.45 - card67.height / 2, 0])
        lp = laptop(1.75, LAPTOP).move_to(v1.laptop)
        img = sealed_box(0.85, CTR)
        img.remove(img.tape)
        img.move_to(v1.image)
        img_label = sans("Python 3.14.8 · uv", CAPTION, CTR).move_to(v1.image_label)
        mates = v1.teammates(3)
        for m, x in zip(mates, (-2.6, 0.0, 2.6)):
            m.move_to([x, BASE - 1.45, 0])
        mini = [small_image().move_to(m.laptop[0]) for m in mates]
        cap = note("early in development").move_to([0, BASE - 2.2, 0])
        with self.voiceover(SAY[4]) as vo:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.4)   # no crossfade:
            self.play(FadeIn(v1), FadeIn(card67), run_time=0.6)                    # the two overlap
            self.play(*v1.parts_in("build", anim=lambda m: FadeIn(m, shift=RIGHT * 0.2)), FadeIn(lp),
                      run_time=0.5)
            self.play(TransformFromCopy(v1.card.frame, img), FadeIn(img_label), run_time=0.8)
            vo.wait_until("Early in a project")
            self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.15) for m in mates], lag_ratio=0.2),
                      FadeIn(cap), run_time=0.9)
            b_arrows = [v1.build_arrow(m) for m in mates]
            self.play(LaggedStart(*[GrowArrow(a) for a in b_arrows], lag_ratio=0.25),
                      Indicate(v1.card, color=VENV, scale_factor=1.05), run_time=1.3)
            self.play(LaggedStart(*[FadeIn(s, scale=1.4) for s in mini], lag_ratio=0.2), run_time=0.5)
            vo.wait_until("Later, one person")
            cap2 = note("later in development").move_to(cap)
            self.play(Transform(cap, cap2), *[FadeOut(a) for a in b_arrows], FadeOut(mini[0]),
                      FadeOut(mini[1]), FadeOut(lp), FadeOut(img), FadeOut(img_label),
                      *v1.parts_out("build"), Indicate(mates[2][0], color=INK), run_time=0.8)
            box = sealed_box(1.3, CTR).move_to(v1.box)          # the pushed image (the box)
            self.play(TransformFromCopy(mini[2], box, path_arc=PI / 2), run_time=1.2)
            vo.wait_until("and everyone else pulls")
            # arcs that bow up over the shelf's left end instead of cutting through its plank; the
            # arc to the far teammate leaves higher and bows more, so the two never cross
            p_arrows = [Arrow(box.front.get_left() + LEFT * 0.04 + UP * dy, mates[i].laptop.get_top() + UP * 0.1,
                              buff=0.08, color=HUB, stroke_width=4, max_tip_length_to_length_ratio=0.12,
                              path_arc=arc_)
                        for i, dy, arc_ in ((0, 0.12, 1.1), (1, -0.12, 1.3))]
            pulled = [small_image(sealed=True).move_to(mates[i].laptop[0]) for i in (0, 1)]
            self.play(LaggedStart(*[GrowArrow(a) for a in p_arrows], lag_ratio=0.3), run_time=0.9)
            self.play(*[FadeIn(p, shift=DOWN * 0.1) for p in pulled], run_time=0.5)

        # ------------------------------------------------------------ 5. the tag is a signpost
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(mates), *[FadeOut(a) for a in p_arrows], *[FadeOut(p) for p in pulled],
                      FadeOut(mini[2]), FadeOut(cap), FadeOut(card67), v1.animate.shift(DOWN * D5),
                      box.animate.shift(DOWN * D5), run_time=0.8)
            v1.post.set_z_index(1)              # the board covers the pointer's start (see docstring)
            self.play(*v1.parts_in("post"), *v1.parts_in("pointer", anim=GrowArrow), run_time=0.8)
            vo.wait_until("It's a signpost")
            self.play(Indicate(v1.pointer, color=LOOKUP, scale_factor=1.15),
                      Indicate(box, color=CTR, scale_factor=1.08), run_time=0.9)
            vo.wait_until("built on some day")
            link = BuildOrPull.dashed_link(v1.card, box, text="?")
            self.play(Create(link[0]), FadeIn(link[1]), run_time=0.8)
            cap5 = note("built on some day, from some commit")
            cap5.move_to([-0.95, link[0].get_center()[1] - 0.42, 0])
            self.play(FadeIn(cap5, shift=UP * 0.1), run_time=0.5)
            vo.wait_until("Nothing promises")
            d = box.width + 0.35
            proxy = box.copy().shift(LEFT * d)
            link2 = BuildOrPull.dashed_link(v1.card, proxy, text="?")
            box2 = sealed_box(1.3, CTR).move_to(box)
            box2.save_state()
            box2.shift(UP * 0.45).set_opacity(0)    # set down onto the shelf (rising from below
            #                                         it crossed the "Docker Hub" caption)
            self.play(box.animate.shift(LEFT * d), v1.aim(proxy), Transform(link, link2), Restore(box2),
                      run_time=0.9)
            self.play(v1.aim(box2), run_time=0.8)
            self.play(v1.aim(box), run_time=0.8)

        # ------------------------------------------------------------ 6. one script decides
        sw = Switchboard(labels=False)
        vis = VGroup(sw.input, sw.junction, *sw.tracks.values(), *[st.dot for st in sw.stations.values()])
        sw.shift(np.array([-0.95, BASE - D5 + 0.65, 0]) - vis.get_center())
        sw_cap = mono("docker-shell.sh", CAPTION, TOOL).next_to(vis, DOWN, buff=0.25)
        left = [v1.git_shelf, v1.card, v1.parts["build"], v1.parts["local"]]
        right = [v1.hub_shelf, hub_tag, v1.post, v1.pointer, v1.box, box, box2]
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(link), FadeOut(cap5), *[m.animate.shift(RIGHT * 0.8) for m in left],
                      *[m.animate.shift(LEFT * 0.8) for m in right], run_time=0.9)
            self.play(FadeIn(sw), FadeIn(sw_cap, shift=UP * 0.1), run_time=0.8)
            vo.wait_until("First, the code")
            self.play(FadeOut(v1), FadeOut(box), FadeOut(box2), FadeOut(sw), FadeOut(sw_cap),
                      run_time=0.8)
