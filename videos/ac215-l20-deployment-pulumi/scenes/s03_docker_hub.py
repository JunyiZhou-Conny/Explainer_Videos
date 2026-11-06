"""S03 · Images to Docker Hub (AC215 L20). TRACKER [M] 2 (beats 0-2), [M] 3 (beats 3-8).
Lecture: 20 · 8 (stage 1 'Push', beat 0 only).

Beats (script.md "## S03", one voiceover block each):
0. TRACKER [M] 2. lecture_ref(20, "8"). Slide 8's four stage chips in a thin row under the top edge,
   '1 Push' YELLOW. A schematic GREY page 'Docker Hub · Account settings' / 'Personal access tokens'
   (tag `illustration`, no logo) with a 'Generate new token' button and an 'Access token' field
   that fills with dots and never reveals; on "never show it" a RED ring round the field.
1. Full-width `laptop` terminal. It types a01's command (README:21, as printed) -> TERM(a01: 2–3)
   RED (line 3 wraps). On "Angle brackets are redirections" every angle bracket on the typed line
   and on the echoed line turns PINK, and a PINK label 'redirections' points up at the echoed `<`s.
   On "replace the whole placeholder" both placeholders are underlined YELLOW.
2. A GREY ghost of `-p <ACCESS TOKEN>` lifts out of the typed line and is struck through; a GREY
   card (tag `extra`, no output panel): `echo "$TOKEN" | docker login -u <you> --password-stdin`
   with `<you>` YELLOW and `--password-stdin` GREEN, under a first row `read -s TOKEN` (GREY note
   'paste, Enter') so $TOKEN is defined and never typed on the command line.
3. TRACKER [M] 3. The terminal shrinks to a 3-row strip. CODE(src/frontend-react/docker-hub.sh:
   7–14) top left; line 11 `DOCKER_USERNAME="dlops"` YELLOW (bar + "dlops"); right of it 'line 11'
   (YELLOW) over a GREY chip '→ your Docker Hub user'.
4. The strip leaves (see deviations). The panel scrolls to CODE(…/docker-hub.sh: 25–35): line 27
   (`docker buildx create … --use --name multi-arch`) PURPLE with 'line 27', lines 31 and 35 YELLOW,
   `--push` PINK. On "The API script": the frontend panel narrows to its lines 31–35 (top), and
   CODE(src/api-service/docker-hub.sh: 31–35) slides in under it from the right with
   `linux/amd64,linux/arm64` PINK on 31 and 35; a TEAL crate 'one tag' splits into 'amd64' and
   'arm64'. On "the frontend script": its `linux/amd64` PINK and a single 'amd64' crate beside it.
5. The panels fade. README card 'README.md · lines 24–35': the three headings in README order, each
   with `sh docker-hub.sh`; the frontend row ringed YELLOW 'captured', the other two GREY 'same
   command'. A new full-width terminal 'laptop · new terminal' at 20 pt (so the long prompt and the
   command fit one row; row tag 'not a docker shell' on its title bar), prompt …/src/frontend-react$, types `sh docker-hub.sh` -> TERM(a02: 2–5, …, 124, 131,
   …, 172 wrap): line 2 YELLOW, 'multi-arch' PURPLE, `at the time of recording` beside Next.js 15.0.2,
   line 131 GREEN, line 172 ORANGE.
6. The card fades; a BLUE 'Docker Hub' panel on top. TERM(a02: 173, …, 254 wrap): line 254 RED; a TEAL
   crate 'frontend-react' bounces off a RED padlock 'dlops'; GREY chip 'not logged in'; a GREY-dashed
   chip 'with your name + login: pushed'.
7. The panel fades and the terminal shrinks to a strip. Three TEAL crates in README order:
   api-service (GREY-dashed, 'not captured here: / two platforms · TensorFlow'), frontend-react
   (GREEN tick 'captured'), vector-db-cli (GREY-dashed, 'not captured here: / two platforms'); above
   them the two folder prompts with `sh docker-hub.sh` as GREY ghost lines (no output). YELLOW
   `▶ your turn` and a GREY chip 'check your Docker Hub page: three repositories'.
8. The terminal and crates fade. A GREY card: "README's VM commands use dlops/… public images /
   → part 1 works even if you skip this stage"; a GREY-dashed clock 'a little older than the code';
   then a GREY chip `dlops/cheese-app-…` → `<you>/cheese-app-…`. Fade; empty frame.

Deviations from SHOW:
- Beat 1: the `>` brackets turn PINK with the `<` ones (the `>` before the newline is what bash
  complains about; the SAY says "angle brackets"); the label says 'redirections' and points at the
  echoed line (line 3), the only place with empty rows under it.
- Beat 2: the card adds a first row `read -s TOKEN` / 'paste, Enter' above the SHOW's command
  (whole-video QA 03:12: `$TOKEN` was defined nowhere, so a copied command piped an empty string).
- Beat 2: the ghost is struck in RED (RED = "don't" in the colour table).
- Beat 4: the 3-row strip leaves at the start of beat 4: CODE 25–35 (11 lines) does not fit over a
  strip, and two side-by-side panels do not fit the frame at >= 20 pt. The frontend panel therefore
  narrows to its own lines 31–35 when the API panel comes, the long lines cut/elided ('…'). Beat 5's
  terminal is the script's "new window".
- Beat 5: the GREY row status reads 'same command' (not '… · block 8', which means nothing on screen);
  the chip on the title bar reads 'not a docker shell' (the title already says 'new terminal').
"""

from manim import *  # noqa: F401,F403  (manim first, then common: common's names win)

from explainer.scene import VoiceScene

from common import *  # noqa: F401,F403

SAY = NARRATION["S03"]

# ------------------------------------------------------------------ the real sources (checked)
A01 = capture("a01")
A02 = capture("a02")
LOGIN = "docker login -u <USER NAME> -p <ACCESS TOKEN>"
assert A01.cmd == LOGIN, A01.cmd
assert LOGIN in readme(21), readme(21)
assert "syntax error near unexpected token `newline'" in A01.line(2), A01.line(2)
assert A01.line(3) == f"bash: -c: line 1: `{LOGIN}'", A01.line(3)
assert A02.cmd == "sh docker-hub.sh", A02.cmd
assert A02.line(2) == "Docker Username: dlops", A02.line(2)
assert A02.line(4) == "Creating new multi-arch builder...", A02.line(4)
assert A02.line(5) == "multi-arch", A02.line(5)
assert "Next.js 15.0.2" in A02.line(124), A02.line(124)
assert A02.line(131).endswith("✓ Compiled successfully"), A02.line(131)
assert A02.line(172).startswith("WARNING: No output specified"), A02.line(172)
assert A02.line(173) == "Pushing multi-arch image to registry...", A02.line(173)
assert A02.line(254).startswith("ERROR: failed to build:") and "push access denied" in A02.line(254)
assert "Access Token" in readme(19) and "new terminal" in readme(20)
for n, name in ((24, "api-service"), (28, "frontend-react"), (33, "vector-db-cli")):
    assert readme(n).strip() == f"#### Build, Tag & Push {name}", readme(n)
for n in (26, 31, 35):
    assert "sh docker-hub.sh" in readme(n), readme(n)

FE = "src/frontend-react/docker-hub.sh"
API = "src/api-service/docker-hub.sh"
assert excerpt(FE, 11, 11) == 'DOCKER_USERNAME="dlops"'
assert excerpt(FE, 27, 27).startswith("docker buildx create ") and "--use --name multi-arch" in excerpt(FE, 27, 27)
assert "--platform linux/amd64 -t" in excerpt(FE, 31, 31) and "--platform linux/amd64 --push" in excerpt(FE, 35, 35)
assert "linux/amd64,linux/arm64 -t" in excerpt(API, 31, 31)
assert "linux/amd64,linux/arm64 --push" in excerpt(API, 35, 35)

BETTER = 'echo "$TOKEN" | docker login -u <you> --password-stdin'   # extra (no capture, no output)
READ = "read -s TOKEN"   # defines $TOKEN without echo or shell history (QA 03:12: $TOKEN was undefined)
GHOST_PROMPTS = (P_API, P_VDB)


def token_page() -> VGroup:
    """The schematic Docker Hub token page (illustration, no logo). .frame .btn .field .dots .tag"""
    crumbs = label("Docker Hub · Account settings", 22, S.GREY)
    head = label("Personal access tokens", 26, INK)
    btn = chip("Generate new token", CLOUD, size=22)
    fl = label("Access token", 20, S.GREY)
    fbox = box(4.2, 0.56, S.GREY, fill=S.BG, fill_opacity=1)
    dots = mono("•" * 12, 22, INK)
    row = VGroup(fl, fbox).arrange(RIGHT, buff=0.3)
    dots.move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * 0.25)
    inner = VGroup(crumbs, head, btn, row).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    fr = box(inner.width + 0.9, inner.height + 0.8, S.GREY, fill=S.GREY_DARKER, fill_opacity=1)
    inner.move_to(fr).shift(DOWN * 0.06)
    dots.move_to(fbox).align_to(fbox, LEFT).shift(RIGHT * 0.25)
    tg = illustration_tag()
    tg.move_to(fr.get_corner(UR) + np.array([-tg.width / 2 - 0.25, 0, 0]))
    g = VGroup(fr, inner, dots, tg)
    g.frame, g.btn, g.field, g.dots, g.tag = fr, btn, fbox, dots, tg
    return g


def hub_body() -> VGroup:
    """README:24–35 condensed: three headings in README order, each with `sh docker-hub.sh` and a
    status cell. .rows[i] (.name .cmd .stat)"""
    rows = VGroup()
    names = ("api-service", "frontend-react", "vector-db-cli")
    for nm in names:
        h = VGroup(label("Build, Tag & Push", 22, INK), mono(nm, 22, CONTAINER)).arrange(RIGHT, buff=0.15)
        rows.add(VGroup(h))
    name_w = max(r.width for r in rows)
    for i, r in enumerate(rows):
        r.move_to([0, -i * 0.55, 0]).align_to(rows[0], LEFT)
    x_cmd = rows[0].get_left()[0] + name_w + 0.45
    stats = []
    for i, r in enumerate(rows):
        c = mono("sh docker-hub.sh", 22, INK)
        c.move_to([x_cmd + c.width / 2, r[0][0].get_center()[1], 0])
        r.add(c)
        r.name, r.cmd = r[0], c
    x_st = x_cmd + rows[0].cmd.width + 0.45
    for i, r in enumerate(rows):
        st = label("captured", 20, TURN) if i == 1 else label("same command", 20, S.GREY)
        st.move_to([x_st + st.width / 2, r.cmd.get_center()[1], 0])
        r.add(st)
        r.stat = st
        stats.append(st)
    body = VGroup(*rows)
    body.stats = stats
    return body


def clock_glyph(r: float = 0.32, color=PAST) -> VGroup:
    """A GREY-dashed clock (text-free)."""
    face = DashedVMobject(Circle(radius=r), num_dashes=18, dashed_ratio=0.55).set_stroke(color, 3)
    h1 = Line(ORIGIN, UP * r * 0.65, color=color, stroke_width=3)
    h2 = Line(ORIGIN, RIGHT * r * 0.5, color=color, stroke_width=3)
    return VGroup(face, h1, h2)


class DockerHub(VoiceScene):
    def construct(self):
        assert len(SAY) == SAY_COUNT["S03"] == 9, len(SAY)

        # ========================================================== 0. stage 1: a token page
        trk = tracker_m(2)
        ref8 = lref("8")
        stages = VGroup(*[chip(s, S.GREY, size=20) for s in STAGES_MANUAL]).arrange(RIGHT, buff=0.25)
        stages.move_to([0, 2.3, 0])
        assert stages.get_top()[1] < TRACK_BOTTOM - 0.1 and stages.get_left()[0] > -6.5
        page = token_page()
        page.move_to([0, -0.75, 0])
        assert page.get_top()[1] < stages.get_bottom()[1] - 0.3, (page.get_top(), stages.get_bottom())
        with self.voiceover(SAY[0]) as vo:
            self.play(FadeIn(trk, shift=RIGHT * 0.3), FadeIn(ref8), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(c) for c in stages], lag_ratio=0.15), run_time=0.6)
            self.play(stages[0].box.animate.set_stroke(TURN, width=4), run_time=0.4)
            self.play(Indicate(stages[0].text, color=TURN, scale_factor=1.15), run_time=0.6)
            self.add(stages)
            vo.wait_until("Create an access token")
            self.play(FadeIn(page.frame), FadeIn(page[1][0]), FadeIn(page[1][1]), FadeIn(page.tag),
                      run_time=0.6)
            self.play(FadeIn(page.btn, scale=0.9), FadeIn(page[1][3]), run_time=0.5)
            self.play(Indicate(page.btn, color=CLOUD, scale_factor=1.08), run_time=0.6)
            self.play(ShowIncreasingSubsets(page.dots, rate_func=linear), run_time=0.8)
            vo.wait_until("it is a password for scripts")
            self.play(Indicate(page.dots, color=INK, scale_factor=1.06), run_time=0.7)
            vo.wait_until("so never show it")
            rg = ring(page.field, ERR, buff=0.1, stroke=4)
            self.play(Create(rg), run_time=0.5)
            self.play(Indicate(rg, color=ERR, scale_factor=1.04), run_time=0.6)

        # ========================================================== 1. the README's login, as printed
        t = laptop_term(rows=6)
        with self.voiceover(SAY[1]) as vo:
            self.play(FadeOut(VGroup(page, rg, stages)), FadeOut(ref8), run_time=0.5)
            self.remove(page, rg, stages, ref8)
            self.play(FadeIn(t, shift=UP * 0.3), run_time=0.4)
            ln = type_capture(self, t, A01, type_time=1.4)[0]
            assert not hasattr(ln, "rows"), "the login line must fit one row"
            vo.wait_until("the login fails")
            rows = out(self, t, [(s, ERR) for s in A01.at(2, 3)], wrap=True, run_time=0.5)
            echo = next(r for r in rows if "`docker login" in r.text)
            self.play(Indicate(rows[0], color=ERR, scale_factor=1.03), run_time=0.6)
            self.add(t)
            vo.wait_until("Angle brackets are redirections")
            brackets = VGroup()
            for row in [ln, *rows]:
                for i, ch in enumerate(row.text):
                    if ch in "<>":
                        brackets.add(*glyph_range(row, i, i + 1))
            self.play(brackets.animate.set_color(ROUTE), run_time=0.4)
            self.play(*[Indicate(g, color=ROUTE, scale_factor=1.5) for g in brackets], run_time=0.7)  # each in place
            self.add(t)
            lts = [substring(echo, "<", 0), substring(echo, "<", 1)]
            y_lbl = rows[-1].strut.get_center()[1] - t.pitch * 1.3
            redir = label("redirections", 22, ROUTE)
            redir.move_to([(lts[0].get_center()[0] + lts[1].get_center()[0]) / 2, y_lbl, 0])
            ups = VGroup(*[arrow(np.array([g.get_center()[0], redir.get_top()[1] + 0.04, 0]),
                                 np.array([g.get_center()[0], g.get_bottom()[1] - 0.04, 0]), ROUTE, stroke=3)
                           for g in lts])
            self.play(FadeIn(redir, shift=UP * 0.1), LaggedStart(*[GrowArrow(a) for a in ups], lag_ratio=0.2),
                      run_time=0.6)
            attach(self, echo, redir)
            attach(self, echo, ups)
            vo.wait_until("so replace the whole placeholder")
            unders = VGroup(*[under(substring(ln, s), TURN, stroke=4) for s in ("<USER NAME>", "<ACCESS TOKEN>")])
            self.play(LaggedStart(*[Create(u) for u in unders], lag_ratio=0.4), run_time=0.8)
            attach(self, ln, unders)
            self.play(Indicate(substring(ln, "<USER NAME>"), color=TURN, scale_factor=1.08),
                      Indicate(substring(ln, "<ACCESS TOKEN>"), color=TURN, scale_factor=1.08), run_time=0.7)
            self.add(t)

        # ========================================================== 2. better: --password-stdin (extra)
        cmd = mono_line(BETTER, 20, INK)
        substring(cmd, "<you>").set_color(TURN)
        substring(cmd, "--password-stdin").set_color(OWN)
        rd = mono_line(READ, 20, INK)
        rd_note = label("paste, Enter", 20, S.GREY)
        rd_row = VGroup(rd, rd_note).arrange(RIGHT, buff=0.45)
        bc = card([rd_row, cmd])
        etag = extra_tag()
        bc.move_to([-6.45 + bc.width / 2, 1.74 - bc.height / 2, 0])
        etag.next_to(bc, UP, buff=0.12).align_to(bc, LEFT)
        ghost = mono("-p <ACCESS TOKEN>", 20, S.GREY)
        ghost.move_to([bc.get_right()[0] + 0.4 + ghost.width / 2, cmd.get_center()[1], 0])
        assert etag.get_top()[1] < TRACK_BOTTOM - 0.05, (etag.get_top(), TRACK_BOTTOM)
        assert ghost.get_right()[0] < 6.5, ghost.get_right()
        assert bc.get_bottom()[1] > t.box.get_top()[1] + 0.2 and bc.get_top()[1] < TRACK_BOTTOM
        with self.voiceover(SAY[2]) as vo:
            src = substring(ln, "-p <ACCESS TOKEN>").copy()
            self.add(src)
            self.play(ReplacementTransform(src, ghost), run_time=0.7)
            st = strike(ghost, ERR, stroke=4)
            self.play(Create(st), run_time=0.4)
            self.play(FadeIn(bc, shift=UP * 0.15), FadeIn(etag), run_time=0.6)
            vo.wait_until("the flag password standard in")
            self.play(Indicate(substring(cmd, "--password-stdin"), color=OWN, scale_factor=1.12), run_time=0.7)
            self.add(bc)
            vo.wait_until("keeps the token out of your shell history")
            self.play(Indicate(substring(cmd, '"$TOKEN"'), color=INK, scale_factor=1.12),
                      Indicate(substring(rd, "TOKEN"), color=INK, scale_factor=1.12),
                      Indicate(substring(cmd, "<you>"), color=TURN, scale_factor=1.12), run_time=0.8)
            self.add(bc)

        # ========================================================== 3. the Docker Hub script: line 11
        p1 = code(FE, 7, 14)
        p1.move_to([-6.45 + p1.width / 2, 2.72 - p1.height / 2, 0])
        assert p1.get_bottom()[1] > STRIP_TOP + 0.15, (p1.get_bottom(), STRIP_TOP)
        bar11 = line_bar(p1.code, 4, TURN)
        l11 = label("line 11", 20, TURN)
        pen = grey_chip("→ your Docker Hub user")
        note11 = VGroup(l11, pen).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        note11.move_to([p1.get_right()[0] + 0.25 + note11.width / 2, bar11.get_center()[1], 0])
        assert note11.get_right()[0] < 6.55, note11.get_right()
        with self.voiceover(SAY[3]) as vo:
            echo.remove(redir, ups)
            ln.remove(unders)
            self.play(FadeOut(VGroup(bc, etag, ghost, st, redir, ups, unders)), track(trk, 3), run_time=0.5)
            self.remove(bc, etag, ghost, st, redir, ups, unders)
            resize(self, t, 3, run_time=0.6)
            self.play(FadeIn(p1, shift=UP * 0.2), run_time=0.6)
            self.play(Indicate(p1.header, color=INK, scale_factor=1.06), run_time=0.6)
            self.add(p1)
            vo.wait_until("Line 11 sets the user name to dlops")
            self.play(FadeIn(bar11), code_span(p1.code, 4, '"dlops"').animate.set_color(TURN), FadeIn(l11),
                      run_time=0.6)
            p1.add(bar11)
            self.add(p1)
            vo.wait_until("the course account")
            self.play(Indicate(code_span(p1.code, 4, '"dlops"'), color=TURN, scale_factor=1.15), run_time=0.7)
            self.add(p1)
            vo.wait_until("change it to yours")
            self.play(FadeIn(pen, shift=LEFT * 0.2), run_time=0.5)
            self.play(Indicate(pen.text, color=INK, scale_factor=1.06), run_time=0.6)

        # ========================================================== 4. a builder, two builds, platforms
        p2 = code(FE, 25, 35, elide={27: "--driver-opt network=host"},
                  cuts={31: "linux/amd64", 35: "--push"})
        p2.move_to([-6.45 + p2.width / 2, 2.72 - p2.height / 2, 0])
        bar27, bar31, bar35 = line_bar(p2.code, 2, TOOL, 0.22), line_bar(p2.code, 6, TURN), line_bar(p2.code, 10, TURN)
        l27 = label("line 27", 20, TOOL)
        l27.move_to([p2.get_right()[0] + 0.25 + l27.width / 2, bar27.get_center()[1], 0])
        assert l27.get_right()[0] < 6.5 and p2.get_bottom()[1] > -3.5
        ck = dict(cuts={31: "linux/amd64", 35: "--push"},     # line 34 elided inside its quotes (lexer)
                  elide={31: "docker buildx build ", 34: " multi-arch image to registry...", 35: "docker buildx build "})
        fe_c = code(FE, 31, 35, **ck)
        api_c = code(API, 31, 35, cuts={31: "linux/arm64", 35: "--push"},
                     elide={31: "docker buildx build ", 34: " multi-arch image to registry...", 35: "docker buildx build "})
        fe_c.move_to([-6.45 + fe_c.width / 2, 2.72 - fe_c.height / 2, 0])
        api_c.move_to([-6.45 + api_c.width / 2, fe_c.get_bottom()[1] - 0.3 - api_c.height / 2, 0])
        assert api_c.get_bottom()[1] > -3.5, api_c.get_bottom()
        x_col = (api_c.get_right()[0] + 6.5) / 2
        one = crate("one tag", crate_w=2.0)
        one.move_to([x_col, api_c.code.get_center()[1] + 0.55, 0])
        c_amd, c_arm = crate("amd64", crate_w=1.8), crate("arm64", crate_w=1.8)
        VGroup(c_amd, c_arm).arrange(RIGHT, buff=0.25).move_to([x_col, one.get_center()[1] - 1.25, 0])
        fe_amd = crate("amd64", crate_w=1.8).move_to([x_col, fe_c.code.get_center()[1], 0])
        assert c_amd.get_left()[0] > api_c.get_right()[0] + 0.15 and c_arm.get_right()[0] < 6.5, \
            (c_amd.get_left(), api_c.get_right(), c_arm.get_right())
        with self.voiceover(SAY[4]) as vo:
            self.play(FadeOut(t, shift=DOWN * 0.3), FadeOut(note11), run_time=0.4)
            self.remove(t, note11)
            self.play(FadeOut(p1, shift=UP * 0.6), FadeIn(p2, shift=UP * 0.6), run_time=0.7)
            self.play(FadeIn(bar27), code_span(p2.code, 2, "--use").animate.set_color(TOOL), FadeIn(l27),
                      run_time=0.5)
            p2.add(bar27)
            self.add(p2)
            self.play(Indicate(code_span(p2.code, 2, "multi-arch"), color=TOOL, scale_factor=1.1), run_time=0.6)
            self.add(p2)
            vo.wait_until("the script builds")
            self.play(FadeIn(bar31), run_time=0.4)
            p2.add(bar31)
            self.add(p2)
            vo.wait_until("then builds again to push")
            push = code_span(p2.code, 10, "--push")
            self.play(FadeIn(bar35), push.animate.set_color(ROUTE), run_time=0.5)
            p2.add(bar35)
            self.add(p2)
            self.play(Indicate(push, color=ROUTE, scale_factor=1.2), run_time=0.6)
            self.add(p2)
            vo.wait_until("The API script builds for")
            self.play(FadeOut(VGroup(p2, l27), shift=UP * 0.3), run_time=0.35)   # no cross-fade of two panels
            self.remove(p2, l27)
            self.play(FadeIn(fe_c, shift=UP * 0.3), run_time=0.35)
            self.play(FadeIn(api_c, shift=LEFT * 1.2), run_time=0.6)
            spans = [code_span(api_c.code, k, "linux/amd64,linux/arm64") for k in (0, 4)]
            self.play(*[s.animate.set_color(ROUTE) for s in spans], FadeIn(one, scale=0.9), run_time=0.6)
            self.add(api_c)
            self.play(ReplacementTransform(one.copy(), c_amd), ReplacementTransform(one, c_arm), run_time=0.8)
            vo.wait_until("the frontend script")
            fspans = [code_span(fe_c.code, k, "linux/amd64") for k in (0, 4)]
            self.play(*[s.animate.set_color(ROUTE) for s in fspans], FadeIn(fe_amd, shift=LEFT * 0.3), run_time=0.6)
            self.play(*[Indicate(s, color=ROUTE, scale_factor=1.1) for s in fspans], run_time=0.6)
            self.add(fe_c)

        # ========================================================== 5. run it in frontend-react
        body = hub_body()
        rc = readme_card((24, 35), body)
        rc.move_to([-6.45 + rc.width / 2, 2.72 - rc.height / 2, 0])
        t2 = term(P_FRONTEND, rows=7, title=T_NEW, size=20)     # 20 pt: the prompt and command fit one row
        bar_tag = on_bar(t2, row_tag("not a docker shell"))
        assert rc.get_bottom()[1] > t2.box.get_top()[1] + 0.1, (rc.get_bottom(), t2.box.get_top())
        assert rc.get_right()[0] < 6.5, rc.get_right()
        assert bar_tag.get_left()[0] > t2.title.get_right()[0] + 0.2, (bar_tag.get_left(), t2.title.get_right())
        fe_row = body[1]
        fe_ring = ring(VGroup(fe_row, fe_row.stat), TURN, buff=0.1)
        with self.voiceover(SAY[5]) as vo:
            self.play(FadeOut(VGroup(fe_c, api_c, c_amd, c_arm, fe_amd)), run_time=0.4)
            self.remove(fe_c, api_c, c_amd, c_arm, fe_amd)
            self.play(FadeIn(rc, shift=UP * 0.15), run_time=0.5)
            self.play(Create(fe_ring), Indicate(fe_row.stat, color=TURN, scale_factor=1.15), run_time=0.6)
            self.add(rc, fe_ring)
            vo.wait_until("outside any docker shell")
            self.play(FadeIn(t2, shift=UP * 0.3), run_time=0.4)
            self.play(FadeIn(bar_tag), run_time=0.3)
            flash_tag(self, bar_tag, S.GREY)
            t2.add(bar_tag)                       # rides on the title bar (moved with it in beat 7)
            type_capture(self, t2, A02, type_time=0.7)
            first = out(self, t2, A02.at((2, 5)), run_time=0.5)
            vo.wait_until("It prints dlops")
            self.play(first[0].animate.set_color(TURN), run_time=0.4)
            self.play(Indicate(substring(first[0], "dlops"), color=TURN, scale_factor=1.2), run_time=0.6)
            self.add(t2)
            vo.wait_until("creates the builder")
            self.play(first[2].animate.set_color(TOOL), first[3].animate.set_color(TOOL), run_time=0.5)
            vo.wait_until("and builds")
            built = out(self, t2, ["…", A02.line(124), A02.line(131)], run_time=0.5)
            tr = beside(time_row(), built[1], buff=0.5)
            pin(self, built[1], tr)
            vo.wait_until("compiled successfully")
            self.play(built[2].animate.set_color(OWN), run_time=0.4)
            self.play(Indicate(substring(built[2], "✓ Compiled successfully"), color=OWN, scale_factor=1.08),
                      run_time=0.6)
            self.add(t2)
            vo.wait_until("The warning says")
            warn = out(self, t2, ["…", (A02.line(172), SHARED)], wrap=True, run_time=0.6)
            self.play(Indicate(warn[1:], color=SHARED, scale_factor=1.03), run_time=0.7)
            self.add(t2)

        # ========================================================== 6. the push: access denied
        hub = outline_box(5.7, 2.2, CLOUD, solid=True, fill_opacity=0.08)
        hub.move_to([6.45 - 2.85, 1.45, 0])
        hub_t = label("Docker Hub", 22, CLOUD).move_to(hub.get_corner(UL) + np.array([0.25, -0.3, 0]), aligned_edge=UL)
        lock = padlock(0.55, ERR, "dlops", size=22).move_to(hub.get_center() + np.array([0.9, 0.15, 0]))
        hub_g = VGroup(hub, hub_t, lock)
        box_ = crate("frontend-react", crate_w=2.7).move_to([-3.6, 1.6, 0])
        nl = grey_chip("not logged in").next_to(lock, DOWN, buff=0.22)
        yours = dashed_chip("with your name + login: pushed")
        yours.move_to([hub.get_center()[0], hub.get_bottom()[1] + 0.3 + yours.height / 2, 0])
        assert hub.get_bottom()[1] > t2.box.get_top()[1] + 0.1 and hub.get_top()[1] < PIC_TOP, hub.get_top()
        assert yours.width < hub.width - 0.2
        with self.voiceover(SAY[6]) as vo:
            self.play(FadeOut(VGroup(rc, fe_ring)), run_time=0.4)
            self.remove(rc, fe_ring)
            self.play(FadeIn(hub_g, shift=LEFT * 0.3), FadeIn(box_, shift=RIGHT * 0.3), run_time=0.6)
            out(self, t2, [A02.line(173)], run_time=0.4)
            vo.wait_until("access denied")
            out(self, t2, ["…", (A02.line(254), ERR)], wrap=True, run_time=0.5)
            self.play(bounce(box_, lock.glyph.get_left() + LEFT * (box_.width / 2 + 0.05)), run_time=1.0)
            self.play(Indicate(lock.glyph, color=ERR, scale_factor=1.25), run_time=0.6)
            vo.wait_until("We are not dlops")
            self.play(Indicate(lock.text, color=ERR, scale_factor=1.25), run_time=0.6)
            vo.wait_until("and not logged in")
            self.play(FadeIn(nl, shift=UP * 0.1), run_time=0.4)
            vo.wait_until("with your name and login")
            self.play(FadeOut(nl), FadeIn(yours, shift=UP * 0.1), run_time=0.6)
            self.play(Indicate(yours.text, color=INK, scale_factor=1.06), run_time=0.6)

        # ========================================================== 7. the other two: your turn
        xs = (-4.3, 0.0, 4.3)
        names = ("api-service", "frontend-react", "vector-db-cli")
        crates = VGroup(*[crate(n, crate_w=2.9, dashed=(i != 1)) for i, n in enumerate(names)])
        for c, x in zip(crates, xs):
            c.move_to([x, 1.15, 0])
        notes = VGroup(
            VGroup(label("not captured here:", 20, S.GREY), label("two platforms · TensorFlow", 20, S.GREY)),
            VGroup(check_glyph(0.3), label("captured", 20, OWN)),
            VGroup(label("not captured here:", 20, S.GREY), label("two platforms", 20, S.GREY)))
        notes[0].arrange(DOWN, buff=0.08)
        notes[2].arrange(DOWN, buff=0.08)
        notes[1].arrange(RIGHT, buff=0.15)
        for nt, c in zip(notes, crates):
            nt.next_to(c, DOWN, buff=0.2)
        keep_inside(notes[0])
        keep_inside(notes[2])
        ghosts = VGroup(*[mono_line(f"{p} sh docker-hub.sh", 20, S.GREY) for p in GHOST_PROMPTS])
        ghosts.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ghosts.move_to([0, 2.3, 0])
        assert ghosts.get_top()[1] < TRACK_BOTTOM - 0.05 and ghosts.get_bottom()[1] > crates.get_top()[1] + 0.2, \
            (ghosts.get_top(), ghosts.get_bottom(), crates.get_top())
        assert ghosts.get_left()[0] > -6.5 and ghosts.get_right()[0] < 6.5, (ghosts.get_left(), ghosts.get_right())
        yt = your_turn()
        chk = grey_chip("check your Docker Hub page: three repositories")
        foot = VGroup(yt, chk).arrange(RIGHT, buff=0.35).move_to([0, -0.85, 0])
        assert foot.get_bottom()[1] > STRIP_TOP + 0.1 and foot.get_top()[1] < notes.get_bottom()[1] - 0.15, \
            (foot.get_top(), notes.get_bottom())
        with self.voiceover(SAY[7]) as vo:
            self.play(FadeOut(VGroup(hub_g, box_, yours)), run_time=0.4)
            self.remove(hub_g, box_, yours)
            resize(self, t2, 3, run_time=0.6,
                   extra=(bar_tag.animate.move_to([bar_tag.get_x(), strip_top(3, 20) - t2.bar_h / 2, 0]),))
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in crates], lag_ratio=0.25), run_time=0.8)
            self.play(Indicate(crates[1], color=CONTAINER, scale_factor=1.06), FadeIn(notes[1]), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(g, shift=RIGHT * 0.3) for g in ghosts], lag_ratio=0.3), run_time=0.7)
            vo.wait_until("we did not capture those two-platform builds")
            self.play(FadeIn(notes[0]), FadeIn(notes[2]), run_time=0.5)
            self.play(Indicate(notes[0][1], color=S.GREY, scale_factor=1.05),
                      Indicate(notes[2][1], color=S.GREY, scale_factor=1.05), run_time=0.7)
            vo.wait_until("Pause, run all three")
            self.play(FadeIn(yt, shift=RIGHT * 0.2), run_time=0.4)
            flash_tag(self, yt, TURN)
            vo.wait_until("and check Docker Hub")
            self.play(FadeIn(chk, shift=UP * 0.1), run_time=0.5)
            self.play(each(crates, CONTAINER, 1.06, 0.25), run_time=0.9)
            self.add(crates)

        # ========================================================== 8. skip it: public dlops images
        ln1 = VGroup(label("README's VM commands use", 22, INK), mono("dlops/…", 22, CONTAINER),
                     label("public images", 22, INK)).arrange(RIGHT, buff=0.15)
        ln2 = label("→ part 1 works even if you skip this stage", 22, INK)
        sc = card([ln1, ln2])
        sc.move_to([0, 0.95, 0])
        clk = clock_glyph()
        old = label("a little older than the code", 22, S.GREY)
        aging = VGroup(clk, old).arrange(RIGHT, buff=0.25).move_to([0, -0.6, 0])
        swap = VGroup(mono("dlops/cheese-app-…", 22, INK), label("→", 22, INK),
                      mono("<you>/cheese-app-…", 22, TURN)).arrange(RIGHT, buff=0.2)
        swc = VGroup(box(swap.width + 0.5, swap.height + 0.3, S.GREY, fill_opacity=0.12), swap)
        swap.move_to(swc[0])
        swc.move_to([0, -2.0, 0])
        assert sc.get_top()[1] < TRACK_BOTTOM - 0.1 and swc.get_bottom()[1] > -3.5
        with self.voiceover(SAY[8]) as vo:
            self.play(FadeOut(VGroup(t2, bar_tag, crates, notes, ghosts, foot)), run_time=0.6)
            self.remove(t2, bar_tag, crates, notes, ghosts, foot)
            self.play(FadeIn(sc, shift=UP * 0.15), run_time=0.6)
            self.play(Indicate(ln2, color=INK, scale_factor=1.05), run_time=0.6)
            self.add(sc)
            vo.wait_until("using the public dlops images")
            self.play(Indicate(ln1[1], color=CONTAINER, scale_factor=1.12), run_time=0.6)
            self.add(sc)
            vo.wait_until("which are a little older than the code")
            self.play(Create(clk[0]), FadeIn(clk[1:]), FadeIn(old, shift=LEFT * 0.2), run_time=0.6)
            self.play(Rotate(clk[1], -PI, about_point=clk[0].get_center()), run_time=0.8)
            vo.wait_until("If you pushed yours")
            self.play(FadeIn(swc[0]), FadeIn(swap[0], shift=UP * 0.15), run_time=0.6)
            vo.wait_until("replace dlops with your user name")
            self.play(FadeIn(swap[1]), TransformFromCopy(swap[0], swap[2]), run_time=0.8)
            self.play(Indicate(swap[2], color=TURN, scale_factor=1.1), run_time=0.7)
        self.play(FadeOut(VGroup(sc, clk, old, swc, trk)), run_time=0.6)
        self.wait(0.3)
