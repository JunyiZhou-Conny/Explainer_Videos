"""S08 · Build once; every job starts empty (AC215 L21). TRACKER P5 8, STRIP Build Container.
Lecture: 21 · slides 27, 31 (beats 0–1 only). Set piece V5 ImageSuitcase.

Beats (script.md "## S08", one voiceover block each):
0. TRACKER P5 8; the Part 2 strip slides in under it, `Build Container` YELLOW. LECTURE 21 · 27, 31.
   A single BLUE box "remote CI server" (slide 31) and the GREY chip from slide 27 "Build Container:
   one environment, build problems found early".
1. The box splits into V5's six rooms (graph layout), each with an empty "Docker" shelf. A one-line
   CODE(ci.yml) strip bottom left shows lines 17, 43, 72, 107, 130, 174 in turn; each
   `runs-on: ubuntu-latest` flies to its room, which lights BLUE. The six shelves pulse: empty.
2. LECTURE off; rooms and strip leave. README(289–294) card on top (bullets 290, 292–294; 291 waits
   for beat 4), code below: CODE(ci.yml 25–27) → line 31 → CODE(33–38), each a Transform; each bullet
   lights with its line: 290 ↔ 27, 292 ↔ 27's `${{ github.sha }}` PINK, 293 ↔ 31 then 33–38, 294.
3. The card shrinks into the tracker caption; the code leaves. A small GRAPH(run1) (illustration):
   a GREY cursor dot clicks Build; STEPS(run1/build) opens beside it; the cursor clicks "Build Docker
   image" and LOG(run1/build/03: 2, 4–5, …, 653, 656) grows from that row while graph and steps go.
   On "from the Dockerfile" lines 4–5 light; the log folds to (2, …, 653) at the top and V5's build
   room appears below: Dockerfile layers stack into the TEAL cube stamped `cheese-app-api:b8458ff…`;
   line 653 turns TEAL. GREY chip "this commit's image · nothing else" (README 340).
4. Line 2 `building with "default" instance` lights YELLOW. README(291) card + GREY erratum chip. A
   GREY dashed "cache" box beside the build room stays empty, chip "no cache-to / cache-from"; the
   layers re-stack (rebuilt from scratch); GREY chip "see the exercises".
5. Card, cache box and log go to LOG(run1/build/04: heading only): the cube folds into the TEAL tar
   suitcase. LOG(run1/build/05: 2) (the stand-in's `ls -l`, the byte count masked by a GREY "≈ 176 MB"
   chip). The piece rises to its place, the other rooms and the BLUE artifact store appear; the
   suitcase flies to the store; GOLD cost tag "artifact · about 176 MB · 1 day". The build room
   dissolves.
6. The lint room zooms in (a big BLUE room): LOG(run1/lint-and-format/x1: 2) (extra), just the
   header; the big Docker shelf is empty and pulses.
7. In the big room: CODE(ci.yml 49–57), 49–53 PINK (a suitcase drops onto the shelf), 55–57 TEAL (it
   unfolds into the cube) → LOG(run1/lint-and-format/03: 2) `Loaded image: cheese-app-api:b8458ff…`.
   Zoom out: the lint room keeps its cube, copies fly from the store to the three test rooms and
   unfold; summary room chip "needs only bash"; README chip "Artifact Sharing" on the store. On
   "expires after a day" the store's suitcase pulses GOLD and fades; a RED cross on the empty store.
8. Everything but the unit-tests room goes; it moves centre left, CODE(ci.yml 84–86) on top. On
   "Delete" a GREY dashed strike crosses 84–86 and the room's cube fades; on "Which step fails" the
   empty shelf pulses. PONDER(8 s).
9. The card leaves. LOG(noload/x1: 2) (extra, empty header) → LOG(noload/x2: 2–3) (extra): line 2
   GREY, line 3 RED, badge "exit 125". The ORANGE Docker Hub door; V5 no_load: the room asks its
   shelf, walks to Docker Hub and is turned away RED; the room turns RED. Fade; empty frame.
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S08"]

# ------------------------------------------------------------------ the real sources (checked)
CI = ".github/workflows/ci.yml"
RUNS_ON = (("build", 17), ("lint-and-format", 43), ("unit-tests", 72), ("integration-tests", 107),
           ("system-tests", 130), ("test-summary", 174))
for _j, _n in RUNS_ON:
    assert excerpt(CI, _n, _n).strip() == "runs-on: ubuntu-latest", (_j, _n)
assert source_text(CI).count("runs-on: ubuntu-latest") == 6
assert excerpt(CI, 27, 27).strip() == "docker build -t cheese-app-api:${{ github.sha }} ."
assert excerpt(CI, 31, 31).strip() == "docker save cheese-app-api:${{ github.sha }} -o /tmp/cheese-app-api.tar"
assert excerpt(CI, 33, 33).strip() == "- name: Upload Docker image artifact"
assert excerpt(CI, 38, 38).strip() == "retention-days: 1"
assert excerpt(CI, 49, 49).strip() == "- name: Download Docker image"
assert excerpt(CI, 57, 57).strip() == "docker load -i /tmp/cheese-app-api.tar"
assert excerpt(CI, 84, 84).strip() == "- name: Load Docker image"
assert excerpt(CI, 86, 86).strip() == "docker load -i /tmp/cheese-app-api.tar"
assert readme(290) == "- Builds the Docker image once"
assert readme(291) == "- Uses Docker Buildx for efficient caching"
assert "github.sha" in readme(292) and "tar file" in readme(293) and "exact same" in readme(294)
assert readme(334).startswith("**Artifact Sharing**")
assert readme(340).startswith("**Unique Image Tags**")

B03 = capture("run1/build/03")
assert 'building with "default" instance' in B03.line(2), B03.line(2)
assert "load build definition from Dockerfile" in B03.line(4)
assert "naming to" in B03.line(653) and "cheese-app-api:" in B03.line(653), B03.line(653)
B05 = capture("run1/build/05")
assert "176112128" in B05.line(2) and B05.exit == 0
assert capture("run1/build/04").exit == 0
LX1 = capture("run1/lint-and-format/x1")
assert LX1.cmd_lines == ["docker images"] and LX1.line(2).split()[0] == "IMAGE"
LF03 = capture("run1/lint-and-format/03")
assert LF03.line(2).startswith("Loaded image: cheese-app-api:")
NX1 = capture("noload/x1")
assert NX1.cmd_lines == ["docker images"] and NX1.line(2).split()[0] == "IMAGE"
NX2 = capture("noload/x2")
assert NX2.line(2).startswith("Unable to find image") and "pull access denied" in NX2.line(3)
assert NX2.exit == 125
assert [s.name for s in steps("run1", "build")][2] == "Build Docker image"

PONDER_Q = "Delete the 'Load Docker image' step\nfrom unit-tests.\nWhich step fails, and with what error?"
ROOM_Y_LOW = -2.2          # beats 3–5: the build room's centre while the logs hold the top
LOG_TOP = 2.1              # Part 2 pictures stay below PIC_TOP2 (2.15)
UNIT_POS = np.array([-3.4, -2.65, 0])
HUB_POS = np.array([3.2, -2.65, 0])


def top_at(m, y: float = LOG_TOP, x: float = 0.0):
    """Place m with its top edge at y, centred on x."""
    return m.move_to([x, y - m.height / 2, 0])


def morph_log(a: RunLog, b: RunLog, pairs=None, rows_in: bool = True) -> list:
    """ANIMS: run-log panel a becomes panel b (frame, separator, title, heading, badge and tag morph;
    rows morph by FILE line where `pairs` maps a's line to b's line, the others fade)."""
    anims = [ReplacementTransform(a.frame, b.frame), ReplacementTransform(a[1], b[1]),
             ReplacementTransform(a.title, b.title)]
    for x, y in ((a.heading, b.heading), (a.badge, b.badge), (a.tag, b.tag)):
        if x is not None and y is not None:
            anims.append(ReplacementTransform(x, y))
        elif x is not None:
            anims.append(FadeOut(x))
        elif y is not None:
            anims.append(FadeIn(y))
    pairs = pairs or {}
    used_a, used_b = set(), set()
    for na, nb in pairs.items():
        ra, rb = a.row(na), b.row(nb)
        anims.append(ReplacementTransform(ra, rb))
        used_a.add(id(ra))
        used_b.add(id(rb))
    for r in a.rows:
        if id(r) not in used_a:
            anims.append(FadeOut(r))
    for r in b.rows:
        if id(r) not in used_b and rows_in:
            anims.append(FadeIn(r))
    return anims


def settle(scene, old, new):
    """After morph_log: take every piece of the old panel off, put the new one on whole."""
    scene.remove(old, *old.get_family())
    scene.add(new)


def morph_code(scene, cur, new, run_time: float = 0.5):
    """A code panel becomes another (Transform keeps `cur` on screen as the new panel)."""
    scene.play(Transform(cur, new), run_time=run_time)
    scene.remove(cur)
    scene.add(new)
    return new


def span_bar(code_m, a: int, b: int, color, opacity: float):
    """One translucent bar over code lines a..b (0-based): no stripes where per-line bars overlap."""
    top, bot = line_bar(code_m, a, color, opacity), line_bar(code_m, b, color, opacity)
    y0, y1 = top.get_top()[1], bot.get_bottom()[1]
    return Rectangle(width=top.width, height=y0 - y1, stroke_width=0).set_fill(color, opacity) \
        .move_to([top.get_center()[0], (y0 + y1) / 2, 0])


def mask_chip(row, sub: str, text: str):
    """A GREY chip laid over the glyphs of `sub` in a log row (the exact bytes masked)."""
    g = substring(row, sub)
    ch = grey_chip(text, size=20)
    bg = Rectangle(width=max(g.width, ch.width) + 0.12, height=row.height + 0.12, stroke_width=0) \
        .set_fill(TERM_BG, 1).move_to(g)
    ch.move_to(g)
    return VGroup(bg, ch)


class BuildOnce(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S08"] == 10, len(SAY)

        # ========================================================== 0. build container first
        tr = tracker_p5(8)
        strip = pipeline_strip("Build Container")
        ref = lref("27, 31")
        srv = github_box("remote CI server", box_w=5.2, box_h=2.0, size=26).move_to([0, 0.1, 0])
        why = grey_chip("Build Container: one environment, build problems found early", size=22) \
            .move_to([0, -2.3, 0])
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(tr, shift=RIGHT * 0.2), run_time=0.5)
            self.play(FadeIn(strip, shift=RIGHT * 0.6), run_time=0.7)
            vo.wait_until("First, build container")
            self.play(Indicate(strip.boxes[1], color=TURN, scale_factor=1.12), FadeIn(ref), run_time=0.7)
            vo.wait_until("the lecture builds it first")
            self.play(FadeIn(srv, shift=UP * 0.2), run_time=0.6)
            vo.wait_until("so every check runs in the same environment")
            self.play(FadeIn(why, shift=UP * 0.15), run_time=0.5)
            self.play(Indicate(srv, color=GITHUB, scale_factor=1.04), run_time=0.7)
            vo.wait_until("and build problems show up early")
            self.play(Indicate(why, color=INK, scale_factor=1.05), run_time=0.7)

        # ========================================================== 1. six machines, not one
        im = ImageSuitcase().move_to([0, -0.65, 0])
        rooms = im.rooms
        hidden = VGroup(im.store, im.hub)          # members later; they move with the piece
        im.remove(im.store, im.hub)
        line0 = code_strip(CI, 17)
        line0.move_to([-6.45 + line0.width / 2, -2.85, 0])
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(why), run_time=0.4)
            self.remove(why)
            self.play(Circumscribe(srv, color=GITHUB, buff=0.08), run_time=0.8)
            vo.wait_until("GitHub gives you a new one")
            frames = [rooms[j].frame for j in JOB_IDS]
            self.play(*[TransformFromCopy(srv.frame, f) for f in frames], FadeOut(srv), run_time=0.9)
            self.play(*[FadeIn(VGroup(rooms[j].text, rooms[j].shelf)) for j in JOB_IDS], run_time=0.4)
            self.remove(*frames)
            self.add(im)
            vo.wait_until("runs on, ubuntu latest")
            self.play(FadeIn(line0, shift=UP * 0.15), run_time=0.35)
            cur = line0
            for j, n in RUNS_ON:
                if n != 17:
                    cur = morph_code(self, cur, code_strip(CI, n).move_to(line0), run_time=0.25)
                fly = cur.code.code_lines[0].copy()
                self.play(FadeOut(fly, target_position=rooms[j].frame.get_center()),
                          Indicate(rooms[j], color=GITHUB, scale_factor=1.05), run_time=0.55)
            vo.wait_until("Each job starts on an empty machine")
            self.play(LaggedStart(*[Indicate(rooms[j].shelf, color=INK, scale_factor=1.15) for j in JOB_IDS],
                                  lag_ratio=0.12), run_time=1.2)

        # ========================================================== 2. the README's build job
        card = readme_panel(289, 294, lines=[290, 292, 293, 294])
        top_at(card)
        c1 = code(CI, 25, 27)
        top_at(c1, card.get_bottom()[1] - 0.25)
        c2 = code_panel(excerpt(CI, 31, 31).strip(), shown_path(CI), 31, "yaml", font_size=20)
        assert c2.width <= 12.6, c2.width
        top_at(c2, card.get_bottom()[1] - 0.25)
        c3 = code(CI, 33, 38)
        top_at(c3, card.get_bottom()[1] - 0.25)
        with self.voiceover(SAY[2]) as vo:
            gone = VGroup(im, cur)
            self.play(FadeOut(gone), FadeOut(ref), run_time=0.5)
            self.remove(gone, *gone.get_family(), ref)
            self.play(FadeIn(card, shift=DOWN * 0.15), FadeIn(c1, shift=UP * 0.15), run_time=0.6)
            vo.wait_until("builds the image once")
            hb = hl_bar(card.rows[290], TURN, 0.22)
            cb = line_bar(c1.code, 2, TURN, 0.22)
            self.play(FadeIn(hb), FadeIn(cb), run_time=0.4)
            vo.wait_until("tagged with the commit ID")
            hb2 = hl_bar(card.rows[292], ROUTE, 0.22)
            sha = code_span(c1.code, 2, "${{ github.sha }}")
            self.play(FadeOut(hb), FadeIn(hb2), sha.animate.set_color(ROUTE), run_time=0.4)
            self.play(Circumscribe(sha, color=ROUTE, buff=0.05), run_time=0.7)
            vo.wait_until("It saves it as a tar file")
            hb3 = hl_bar(card.rows[293], TURN, 0.22)
            self.play(FadeOut(hb2), FadeOut(cb), FadeIn(hb3), run_time=0.3)
            self.remove(hb, hb2, cb)
            cur = morph_code(self, c1, c2)
            cb = line_bar(c2.code, 0, TURN, 0.22)
            self.play(FadeIn(cb), run_time=0.3)
            vo.wait_until("and uploads it as an artifact")
            self.play(FadeOut(cb), run_time=0.2)
            self.remove(cb)
            cur = morph_code(self, c2, c3)
            cb = span_bar(c3.code, 0, 5, TURN, 0.18)
            self.play(FadeIn(cb), run_time=0.3)
            vo.wait_until("so every other job gets")
            hb4 = hl_bar(card.rows[294], TURN, 0.22)
            self.play(FadeOut(hb3), FadeIn(hb4), run_time=0.4)
            self.remove(hb3)
            self.play(Indicate(card.rows[294], color=TURN, scale_factor=1.04), run_time=0.7)

        # ========================================================== 3. open the build log; the cube
        g = run_graph("run1", labels="short", col_gap=0.45)
        g.move_to([-6.45 + g.width / 2, -0.55, 0])
        sl = steps_list("run1", "build", ((2, 6),))
        sl.move_to([6.45 - sl.width / 2, 0.2, 0])
        assert sl.get_left()[0] > g.get_right()[0] + 0.15, (sl.get_left()[0], g.get_right()[0])
        cursor = cursor_dot().move_to([0.5, -3.0, 0])
        full = run_log(B03, (2, (4, 5), "…", 653, 656))
        full.move_to([0, -0.55, 0])
        comp = run_log(B03, (2, "…", 653))
        top_at(comp)
        # the build room alone, low (the logs hold the top); everything else moves with it
        dy = ROOM_Y_LOW - rooms["build"].get_center()[1]
        others = [rooms[j] for j in JOB_IDS if j != "build"]
        for r in others:
            im.remove(r)
        VGroup(im, *others, hidden).shift(UP * dy)
        commit_chip = grey_chip("this commit's image · nothing else", size=22)
        commit_chip.next_to(rooms["build"], RIGHT, buff=0.5)
        with self.voiceover(SAY[3]) as vo:
            cap_copy = tr.caption.copy()
            out_code = VGroup(cur, cb, hb4)
            self.play(ReplacementTransform(card, cap_copy), FadeOut(out_code), run_time=0.6)
            self.remove(cap_copy, card, out_code, *out_code.get_family())
            self.add(tr)
            self.play(FadeIn(g), FadeIn(cursor), run_time=0.5)
            self.play(cursor.animate.move_to(g.nodes["build"].get_center()), run_time=0.5)
            self.play(Flash(cursor, color=S.GREY, flash_radius=0.3), g.pulse("build", TURN), run_time=0.5)
            self.add(g)
            self.play(FadeIn(sl, shift=LEFT * 0.2), run_time=0.4)
            vo.wait_until("then a step")
            row = sl.row(4)
            self.play(cursor.animate.move_to(row.name.get_center()), run_time=0.5)
            self.play(Flash(cursor, color=S.GREY, flash_radius=0.3), Indicate(row, color=TURN, scale_factor=1.05),
                      run_time=0.5)
            vo.wait_until("to open its log")
            self.play(FadeOut(VGroup(g, cursor)), FadeOut(VGroup(*[r for r in sl.rows if r is not row]), sl.frame,
                                                           sl.head, sl.tag),
                      ReplacementTransform(row, full), run_time=0.8)
            self.remove(g, cursor, sl, *sl.get_family())
            self.add(full)
            vo.wait_until("Docker builds the image")
            hb = VGroup(hl_bar(full.row(4), TURN, 0.22), hl_bar(full.row(5), TURN, 0.22))
            self.play(FadeIn(hb), run_time=0.4)
            self.play(Indicate(VGroup(full.row(4), full.row(5)), color=TURN, scale_factor=1.03), run_time=0.9)
            self.play(Indicate(full.row(653), color=IMAGE, scale_factor=1.03), run_time=0.7)
            self.play(FadeOut(hb), *morph_log(full, comp, {2: 2, 653: 653}), run_time=0.8)
            settle(self, full, comp)
            self.remove(hb)
            self.play(FadeIn(im), run_time=0.4)
            im.build_cube(self, per=0.25)
            vo.wait_until("and names it cheese app API")
            tagg = substring(comp.row(653), "cheese-app-api:")
            self.play(comp.row(653).animate.set_color(IMAGE), run_time=0.4)
            self.play(Indicate(tagg, color=IMAGE, scale_factor=1.08), Indicate(im.stamp, color=IMAGE, scale_factor=1.1),
                      run_time=0.7)
            vo.wait_until("That tag means")
            self.play(FadeIn(commit_chip, shift=LEFT * 0.15), run_time=0.5)
            self.play(Indicate(commit_chip, color=IMAGE, scale_factor=1.05), run_time=0.6)

        # ========================================================== 4. a small slip: no cache
        line2 = comp.row(2)
        c291 = readme_panel(291, 291)
        err = erratum_tag()
        slip = VGroup(c291, err).arrange(RIGHT, buff=0.25)
        slip.move_to([rooms["build"].get_right()[0] + 0.45 + slip.width / 2, -1.55, 0])
        cache = outline_box(1.5, 0.8, S.GREY)
        cache_t = label("cache", 22, S.GREY).move_to(cache)
        cache_box = VGroup(cache, cache_t)
        cache_box.move_to([rooms["build"].get_right()[0] + 0.45 + cache_box.width / 2, -2.85, 0])
        no_cache = grey_chip("no cache-to / cache-from", size=20).next_to(cache_box, RIGHT, buff=0.25)
        exer = grey_chip("see the exercises", size=20).next_to(no_cache, RIGHT, buff=0.2)
        assert exer.get_right()[0] <= 6.5, exer.get_right()[0]
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(commit_chip), run_time=0.3)
            self.remove(commit_chip)
            vo.wait_until("A small slip")
            self.play(FadeIn(slip, shift=UP * 0.15), run_time=0.5)
            vo.wait_until("the README promises Buildx caching")
            self.play(Circumscribe(c291.rows[291], color=TURN, buff=0.06), run_time=0.8)
            vo.wait_until("but the build runs on the default builder")
            hb = hl_bar(line2, TURN, 0.25)
            self.play(FadeIn(hb), line2.animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(substring(line2, '"default"'), color=TURN, scale_factor=1.15), run_time=0.7)
            vo.wait_until("and nothing saves a cache")
            self.play(FadeIn(cache_box), run_time=0.5)
            self.play(FadeIn(no_cache, shift=LEFT * 0.15), Indicate(cache_t, color=S.GREY, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("so every fresh machine rebuilds")
            layers = VGroup(*[Rectangle(width=1.2, height=0.18, stroke_color=IMAGE, stroke_width=2)
                              .set_fill(IMAGE, 0.3) for _ in range(3)]).arrange(UP, buff=0.04).move_to(im.cube)
            self.play(FadeOut(im.cube), run_time=0.25)
            self.play(LaggedStart(*[FadeIn(ly, shift=DOWN * 0.35) for ly in layers], lag_ratio=0.5), run_time=0.9)
            self.play(FadeOut(layers), FadeIn(im.cube), run_time=0.4)
            self.remove(layers)
            self.add(im)
            vo.wait_until("The exercises show how")
            self.play(FadeIn(exer, shift=LEFT * 0.15), run_time=0.5)

        # ========================================================== 5. save, upload, throw the machine away
        l04 = top_at(run_log("run1/build/04", ()))
        l05 = top_at(run_log(B05, (2,), wrap=True))
        mask = mask_chip(l05.row(2), "176112128", TAR_SIZE)
        cost = cost_tag("artifact · about 176 MB · 1 day")
        with self.voiceover(SAY[5]) as vo:
            gone = VGroup(slip, cache_box, no_cache, exer, hb)
            self.play(FadeOut(gone), *morph_log(comp, l04), run_time=0.7)
            self.remove(gone, *gone.get_family())
            settle(self, comp, l04)
            vo.wait_until("Docker save folds")
            im.fold(self)
            vo.wait_until("about 176 megabytes")
            self.play(*morph_log(l04, l05), run_time=0.6)
            settle(self, l04, l05)
            self.play(FadeIn(mask), run_time=0.3)
            self.play(Indicate(mask, color=INK, scale_factor=1.1), Indicate(im.case_tag, color=IMAGE, scale_factor=1.1),
                      run_time=0.6)
            vo.wait_until("The upload step carries it")
            self.play(FadeOut(VGroup(l05, mask)), run_time=0.4)
            self.remove(l05, *l05.get_family(), mask)
            self.play(im.animate.shift(DOWN * dy), run_time=0.7)
            VGroup(*others, hidden).shift(DOWN * dy)
            for r in others:
                im.add(r)
            im.add(im.store)
            self.play(FadeIn(VGroup(*others, im.store)), run_time=0.5)
            self.add(im)
            im.upload(self)
            cost.move_to([-6.45 + cost.width / 2, im.store.board.get_center()[1] + 0.55, 0])
            self.play(Transform(im.day, cost), run_time=0.6)
            vo.wait_until("kept for one day")
            self.play(Indicate(im.day, color=COST, scale_factor=1.08), run_time=0.7)
            vo.wait_until("Then the build machine is thrown away")
            im.dissolve_build(self)

        # ========================================================== 6. inside a fresh check job
        lint = rooms["lint-and-format"]
        big = box(12.6, 5.25, GITHUB, fill_opacity=0.08, radius=0.2).move_to([0, -0.85, 0])
        big_t = label(JOB_NAME["lint-and-format"], 26, GITHUB).next_to(big.get_corner(UL), DR, buff=0.2)
        big_shelf = shelf(2.6, 22).next_to(big.get_corner(DR), UL, buff=0.35)
        x1 = run_log(LX1, (2,), title="Lint and Format Check · extra: docker images")
        x1.move_to([0, big.get_center()[1] + 0.55, 0])
        xt = extra_tag().next_to(big_t, RIGHT, buff=0.3)
        with self.voiceover(SAY[6]) as vo:
            ghost = lint.frame.copy()
            self.play(FadeOut(im), ReplacementTransform(ghost, big), run_time=0.8)
            self.remove(im, *im.get_family())
            self.play(FadeIn(big_t), FadeIn(big_shelf), run_time=0.4)
            vo.wait_until("An extra command")
            self.play(FadeIn(x1, shift=UP * 0.15), FadeIn(xt), run_time=0.5)
            self.play(Indicate(x1.row(2), color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("No image at all")
            self.play(Indicate(big_shelf, color=INK, scale_factor=1.12), run_time=0.8)

        # ========================================================== 7. download, load: artifact sharing
        c49 = code(CI, 49, 57)
        c49.move_to([big.get_left()[0] + 0.3 + c49.width / 2, 0, 0])
        top_at(c49, big_t.get_bottom()[1] - 0.25, c49.get_center()[0])
        drop_case = suitcase_glyph(0.7).move_to([big_shelf.board.get_center()[0], big_t.get_center()[1], 0])
        big_cube = cube_glyph(0.75).next_to(big_shelf.board, UP, buff=0.04)
        lf03 = run_log(LF03, (2,))
        lf03.move_to([big.get_left()[0] + 0.3 + lf03.width / 2, big.get_center()[1] + 0.4, 0])
        bash = grey_chip("needs only bash", size=20)
        share = grey_chip("Artifact Sharing", size=22)
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(x1), FadeIn(c49), run_time=0.5)
            self.remove(x1, *x1.get_family())
            vo.wait_until("downloads the artifact")
            pk = span_bar(c49.code, 0, 4, ROUTE, 0.25)
            self.play(FadeIn(pk), run_time=0.3)
            self.play(FadeIn(drop_case, shift=DOWN * 0.3), run_time=0.3)
            self.play(drop_case.animate.next_to(big_shelf.board, UP, buff=0.04), run_time=0.6)
            vo.wait_until("and runs docker load")
            tl = span_bar(c49.code, 6, 8, IMAGE, 0.25)
            self.play(FadeIn(tl), run_time=0.3)
            self.play(ReplacementTransform(drop_case, big_cube), run_time=0.6)
            vo.wait_until("the same tag, unpacked")
            self.play(FadeOut(VGroup(c49, pk, tl)), FadeIn(lf03, shift=UP * 0.15), run_time=0.5)
            self.remove(c49, pk, tl)
            ltag = substring(lf03.row(2), "cheese-app-api:")
            self.play(ltag.animate.set_color(IMAGE), Indicate(big_cube, color=IMAGE, scale_factor=1.1), run_time=0.5)
            vo.wait_until("That's artifact sharing")
            # zoom out in two clean steps: the log leaves, then the big room shrinks back into its
            # place (frame, shelf and cube each become the small one) while the other rooms return
            self.play(FadeOut(VGroup(lf03, big_t, xt)), run_time=0.35)
            self.remove(lf03, *lf03.get_family(), big_t, xt)
            lc = cube_glyph(0.3).next_to(lint.shelf.board, UP, buff=0.03)
            g_frame, g_shelf = lint.frame.copy(), lint.shelf.copy()
            self.play(ReplacementTransform(big, g_frame), ReplacementTransform(big_shelf, g_shelf),
                      ReplacementTransform(big_cube, lc), FadeIn(im), run_time=0.8)
            self.remove(g_frame, *g_frame.get_family(), g_shelf, *g_shelf.get_family(), big, big_shelf, big_cube)
            self.add(im)
            im.cubes["lint-and-format"] = lc
            im.keep(self, lc)
            im.deliver(self, jobs=TEST_JOBS, run_time=0.8)
            cbs = {j: cube_glyph(0.3).next_to(rooms[j].shelf.board, UP, buff=0.03) for j in TEST_JOBS}
            self.play(*[ReplacementTransform(im.copies[j], cbs[j]) for j in TEST_JOBS], run_time=0.5)
            for j in TEST_JOBS:
                im.remove(im.copies[j])
                im.cubes[j] = cbs[j]
            im.keep(self, *cbs.values())
            share.next_to(im.store.board, RIGHT, buff=0.3)
            bash.next_to(rooms["test-summary"], DOWN, buff=0.2)
            self.play(FadeIn(share, shift=DOWN * 0.15), FadeIn(bash, shift=UP * 0.1), run_time=0.5)
            im.keep(self, share, bash)
            vo.wait_until("And the artifact expires after a day")
            self.play(Indicate(VGroup(im.case, im.day), color=COST, scale_factor=1.1), run_time=0.8)
            im.drop(self, im.case, run_time=0.6)
            vo.wait_until("so re-running a failed job tomorrow")
            gone_x = cross_mark(0.4, ERR).move_to(im.store.board.get_center() + UP * 0.32)
            self.play(FadeIn(gone_x, scale=1.4), run_time=0.4)
            im.keep(self, gone_x)

        # ========================================================== 8. ponder: no docker load
        unit = rooms["unit-tests"]
        c84 = top_at(code(CI, 84, 86))
        with self.voiceover(SAY[8]) as vo:
            rest = [m for m in im.submobjects if m is not unit and m is not im.cubes["unit-tests"]]
            im.drop(self, *rest, run_time=0.5)
            ucube = im.cubes["unit-tests"]
            self.play(VGroup(unit, ucube).animate.scale(1.4).move_to(UNIT_POS), run_time=0.7)
            self.play(FadeIn(c84, shift=DOWN * 0.15), run_time=0.5)
            vo.wait_until("Delete the load docker image step")
            strikes = VGroup(*[DashedLine(ln.get_left() + LEFT * 0.08, ln.get_right() + RIGHT * 0.08,
                                          color=S.GREY, stroke_width=4, dash_length=0.12)
                               for ln in c84.code.code_lines])
            self.play(c84.code.code_lines.animate.set_opacity(0.45), Create(strikes), run_time=0.7)
            im.drop(self, ucube, run_time=0.5)
            vo.wait_until("Which step fails")
            self.play(Indicate(unit.shelf, color=INK, scale_factor=1.15), run_time=0.8)
            # the centred ponder card would cover the strip's lower edge: the strip leaves first
            self.play(FadeOut(VGroup(c84, strikes), shift=UP * 0.1), run_time=0.4)
            self.remove(c84, *c84.get_family(), strikes)
        card8 = ponder(self, PONDER_Q, seconds=8)

        # ========================================================== 9. the answer: pull access denied
        n1 = top_at(run_log(NX1, (2,), title="Unit Tests · extra: docker images (no load)"))
        n2 = top_at(run_log(NX2, (2, 3), title="Unit Tests › Run unit tests (no load)", wrap=True,
                            colors={2: S.GREY, 3: ERR}))
        x2t = extra_tag().next_to(n2.frame, DOWN, buff=0.12).align_to(n2.frame, LEFT)
        hub = im.hub
        hub.move_to(HUB_POS)
        rows3 = VGroup(*n2.rows[1:])
        with self.voiceover(SAY[9]) as vo:
            self.play(FadeOut(card8), run_time=0.4)
            self.remove(card8)
            self.play(FadeIn(n1, shift=DOWN * 0.15), run_time=0.5)
            self.play(Indicate(n1.title, color=INK, scale_factor=1.04), run_time=0.6)
            vo.wait_until("Docker looks for the image")
            self.play(*morph_log(n1, n2, rows_in=False), run_time=0.6)
            settle(self, n1, n2)
            self.remove(*n2.rows)
            self.play(FadeIn(x2t), FadeIn(n2.rows[0]), run_time=0.4)
            vo.wait_until("and finds nothing")
            self.play(Indicate(unit.shelf, color=S.GREY, scale_factor=1.15), run_time=0.6)
            vo.wait_until("then asks Docker Hub")
            self.play(FadeIn(hub), run_time=0.4)
            im.add(hub)
            im.no_load(self, "unit-tests")
            vo.wait_until("pull access denied")
            self.play(FadeIn(rows3), run_time=0.4)
            self.remove(n2.rows)
            self.add(n2)
            self.play(Indicate(substring(n2.rows[1], "pull access denied"), color=ERR, scale_factor=1.08),
                      run_time=0.6)
            vo.wait_until("Exit code 125")
            self.play(Circumscribe(n2.badge, color=ERR, buff=0.06), run_time=0.8)
            vo.wait_until("the step fails, so the job fails")
            self.play(unit.frame.animate.set_stroke(ERR, 4), unit.text.animate.set_color(ERR), run_time=0.6)

        self.wait(0.3)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
        self.wait(0.2)
